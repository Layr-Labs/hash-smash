"""Half-key uniformity sampler for blake3-r1 MITM analysis.

Stdlib-only, deterministic. Per organizer trial, draws a random column
prefix C from the trial seed, then draws 512 random half inputs under
that C, evaluates the two 128-bit digest-half keys with an embedded
exact blake3-r1, and reports distinct counts as numeric observations
(the same coin distribution the claimed MITM analysis assumes uniform).
Returned pairs are the first two fresh samples (no collision expected;
the collision witness lives in the certificate, verified separately).
"""
import hashlib
import json
import random
import struct
import sys

IV = (0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A,
      0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19)
MASK = 0xFFFFFFFF
SAMPLES = 384


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
        first_a = first_b = None
        for _ in range(SAMPLES):
            w = list(C) + [rng.getrandbits(32) for _ in range(8)]
            if first_a is None:
                first_a = struct.pack("<16I", *w)
            elif first_b is None:
                first_b = struct.pack("<16I", *w)
            h = _halves(w)
            u = struct.unpack("<8I", h)
            seen1.add((u[0], u[2], u[5], u[7]))
            seen2.add((u[1], u[3], u[4], u[6]))
        if first_b is None or first_a == first_b:
            first_b = struct.pack("<16I", *([rng.getrandbits(32) for _ in range(16)]))
        rows.append({
            "trial": trial["trial"],
            "message_a_hex": first_a.hex(),
            "message_b_hex": first_b.hex(),
            "observations": {"samples": SAMPLES,
                             "distinct_half1": len(seen1),
                             "distinct_half2": len(seen2)},
        })
    json.dump({"schema_version": 1, "trials": rows}, sys.stdout, sort_keys=True)


main()
