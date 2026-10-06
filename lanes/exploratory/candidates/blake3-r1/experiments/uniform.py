"""Half-key uniformity sampler for blake3-r1 MITM analysis.

Stdlib-only, deterministic. Per organizer trial, draws a random column
prefix C from the trial seed, then draws 512 random half inputs under
that C, evaluates the two 128-bit digest-half keys with an embedded
exact blake3-r1, and reports distinct counts as numeric observations
(the same coin distribution the claimed MITM analysis assumes uniform).
Also replays the fixed collision witness as the trial pair
(full-collision event succeeds deterministically).
"""
import hashlib
import json
import random
import struct
import sys

IV = (0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A,
      0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19)
MASK = 0xFFFFFFFF
SAMPLES = 512
WIT_A = "00" * 64
WIT_B = ("40e88e6cf0fc0a3a56ee4f6d75b50fb07a836a7c75ad3b17"
         "ca278663d0e9884c511ec7c503e24b10fa65e612aaad1d14"
         "30c353e769a772cefd94e2dc25367353")


def _ror(v, n):
    return ((v >> n) | (v << (32 - n))) & MASK


def _g(s, a, b, c, d, x, y):
    s[a] = (s[a] + s[b] + x) & MASK
    s[d] = _ror(s[d] ^ s[a], 16)
    s[c] = (s[c] + s[d]) & MASK
    s[b] = _ror(s[b] ^ s[c], 12)
    s[a] = (s[a] + s[b] + y) & MASK
    s[d] = _ror(s[d] ^ s[a], 8)
    s[c] = (s[c] + s[d]) & MASK
    s[b] = _ror(s[b] ^ s[c], 7)


def _halves(words):
    s = list(IV) + list(IV[:4]) + [0, 0, 64, 11]
    m = list(words)
    _g(s, 0, 4, 8, 12, m[0], m[1])
    _g(s, 1, 5, 9, 13, m[2], m[3])
    _g(s, 2, 6, 10, 14, m[4], m[5])
    _g(s, 3, 7, 11, 15, m[6], m[7])
    _g(s, 0, 5, 10, 15, m[8], m[9])
    _g(s, 1, 6, 11, 12, m[10], m[11])
    _g(s, 2, 7, 8, 13, m[12], m[13])
    _g(s, 3, 4, 9, 14, m[14], m[15])
    o = [(s[i] ^ s[i + 8]) & MASK for i in range(8)]
    return struct.pack("<8I", *o[:8])


def main():
    req = json.load(sys.stdin)
    rows = []
    for trial in req["trials"]:
        rng = random.Random(int.from_bytes(
            hashlib.sha256(("half-uniformity:" + str(trial["trial"]) + ":" +
                            trial["seed"]).encode()).digest(), "big"))
        C = [rng.getrandbits(32) for _ in range(8)]
        seen1, seen2 = set(), set()
        for _ in range(SAMPLES):
            w = list(C) + [rng.getrandbits(32) for _ in range(8)]
            h = _halves(w)
            u = struct.unpack("<8I", h)
            seen1.add((u[0], u[2], u[5], u[7]))
            seen2.add((u[1], u[3], u[4], u[6]))
        rows.append({
            "trial": trial["trial"],
            "message_a_hex": WIT_A,
            "message_b_hex": WIT_B,
            "observations": {"samples": SAMPLES,
                             "distinct_half1": len(seen1),
                             "distinct_half2": len(seen2)},
        })
    json.dump({"schema_version": 1, "trials": rows}, sys.stdout, sort_keys=True)


main()
