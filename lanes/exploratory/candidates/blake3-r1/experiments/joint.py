"""Joint mini-join experiment for blake3-r1 MITM independence.

Stdlib-only, deterministic. Per organizer trial, draws a random column
prefix C from the trial seed, then runs reduced-scale joins mirroring
the claimed attack's digest relation against the fixed all-zero target
T: half H1 tables 2^8 (w8,w9) truncated keys versus 2^8 (w12,w13)
probes mapped through (T0,T2,T5,T7); half H2 likewise with (T1,T3,T4,T6).
Keys are truncated to 18 bits (E[hits]=0.25 per half). Reports per-half
hit indicators as numeric observations, directly measuring the joint
H1/H2 outcome distribution the independence heuristic concerns.
Returned pairs are fresh random samples; collisions are not expected.
Only diagonal G fragments are evaluated (column state computed once).
"""
import hashlib
import json
import random
import struct
import sys

IV = (0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A,
      0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19)
MASK = 0xFFFFFFFF
NS = 1 << 8
KM = (1 << 9) - 1
T = (0x924A17E9, 0x5B44D964, 0x01A0D272, 0x3F28A25C,
     0xCB0E7C49, 0xB2E49E5D, 0xC6610D02, 0x88BAC908)


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


def _col_round(m8):
    s = list(IV) + list(IV[:4]) + [0, 0, 64, 11]
    m = list(m8)
    _g(s, 0, 4, 8, 12, m[0], m[1])
    _g(s, 1, 5, 9, 13, m[2], m[3])
    _g(s, 2, 6, 10, 14, m[4], m[5])
    _g(s, 3, 7, 11, 15, m[6], m[7])
    return s


def _mini_join(s_col, rng, half):
    """True digest-relation join at 18-bit truncation. Returns 0/1."""
    table = set()
    for _ in range(NS):
        a = (rng.getrandbits(32), rng.getrandbits(32))
        s = list(s_col)
        if half == 1:
            _g(s, 0, 5, 10, 15, a[0], a[1])
            table.add(((s[0] & KM) << 9) | (s[5] & KM))
        else:
            _g(s, 1, 6, 11, 12, a[0], a[1])
            table.add(((s[1] & KM) << 9) | (s[6] & KM))
    for _ in range(NS):
        b = (rng.getrandbits(32), rng.getrandbits(32))
        s = list(s_col)
        if half == 1:
            _g(s, 2, 7, 8, 13, b[0], b[1])
            k = (((T[0] ^ s[8]) & KM) << 9) | ((T[5] ^ s[13]) & KM)
            if k in table:
                return 1
        else:
            _g(s, 3, 4, 9, 14, b[0], b[1])
            k = (((T[1] ^ s[9]) & KM) << 9) | ((T[6] ^ s[14]) & KM)
            if k in table:
                return 1
    return 0


def main():
    req = json.load(sys.stdin)
    rows = []
    for trial in req["trials"]:
        rng = random.Random(int.from_bytes(
            hashlib.sha256(("joint-minijoin:" + str(trial["trial"]) + ":" +
                            trial["seed"]).encode()).digest(), "big"))
        C = [rng.getrandbits(32) for _ in range(8)]
        s_col = _col_round(C)
        h1 = _mini_join(s_col, rng, 1)
        h2 = _mini_join(s_col, rng, 2)
        a = struct.pack("<16I", *([rng.getrandbits(32) for _ in range(16)]))
        b = struct.pack("<16I", *([rng.getrandbits(32) for _ in range(16)]))
        if a == b:
            b = b[:-1] + bytes([b[-1] ^ 1])
        rows.append({
            "trial": trial["trial"],
            "message_a_hex": a.hex(),
            "message_b_hex": b.hex(),
            "observations": {"h1_hit": h1, "h2_hit": h2},
        })
    json.dump({"schema_version": 1, "trials": rows}, sys.stdout, sort_keys=True)


main()
