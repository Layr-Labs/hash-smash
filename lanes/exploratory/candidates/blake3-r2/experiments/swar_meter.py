"""SWAR (4 lanes x 64-bit slots per 256-bit word) Word-op meter + matched-scale
masked birthday (python-message-pairs-v1).

Accounting: every +,-,&,|,^,<<,>> on a 256-bit Word counts 1 (organizer
convention of scripts/reference_operation_costs.py); results reduced mod 2^256.
A 256-bit word rotation is charged ROT_COST=3 (shr + shl + or), i.e. we do NOT
rely on the cost model's listed "rotation" primitive.  Lane rotations inside a
slot are (t>>n)|(t<<(32-n)) then &M4 (4 ops for four lanes at once).

Per message the metered body is: 2 counter-register increments, R1 diagonal
second half (13), undiagonalize (3 rot), R2 column G4 (30), diagonalize (3 rot),
R2 diagonal G4 (30), feed-forward (2 rot + 2 xor), pack K = H0 | H1<<32 (2).
Expected total = 103 with ROT_COST=3 (87 with ROT_COST=1).

Each digest is checked bit-for-bit against an inlined 2-round root compression
identical to verifier/blake3.py, and K is checked to equal the fixed bit
permutation of that digest.  Observation op counts are untrusted labels.
"""
from __future__ import annotations

import hashlib
import json
import operator
import struct
import sys

W = (1 << 256) - 1
MASK = 0xFFFFFFFF
IV = (0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A,
      0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19)
PERM = (2, 6, 3, 10, 7, 0, 4, 13, 1, 11, 12, 5, 9, 14, 15, 8)
SCHED = [
    (0, 4, 8, 12, 0, 1), (1, 5, 9, 13, 2, 3), (2, 6, 10, 14, 4, 5), (3, 7, 11, 15, 6, 7),
    (0, 5, 10, 15, 8, 9), (1, 6, 11, 12, 10, 11), (2, 7, 8, 13, 12, 13), (3, 4, 9, 14, 14, 15),
]
FLAGS = 1 | 2 | 8
ROT_COST = 3
EXPECTED_BODY = 103


class Word(int):
    ops = 0

    def _c(self, f, o):
        Word.ops += 1
        return Word(f(int(self), int(o)) & W)

    __add__ = lambda s, o: s._c(operator.add, o)
    __and__ = lambda s, o: s._c(operator.and_, o)
    __or__ = lambda s, o: s._c(operator.or_, o)
    __xor__ = lambda s, o: s._c(operator.xor, o)
    __lshift__ = lambda s, o: s._c(operator.lshift, o)
    __rshift__ = lambda s, o: s._c(operator.rshift, o)


def rot256(x, k):
    Word.ops += ROT_COST
    v = int(x)
    return Word(((v >> k) | (v << (256 - k))) & W)


M4 = Word(sum(MASK << (64 * j) for j in range(4)))


def sw(vals):
    return Word(sum((int(x) & MASK) << (64 * j) for j, x in enumerate(vals)))


def unsw(w):
    return [(int(w) >> (64 * j)) & MASK for j in range(4)]


def ror4(t, n):
    return ((t >> n) | (t << (32 - n))) & M4


def G4(S, X, Y):
    A, B, C, D = S
    A = (A + B + X) & M4
    D = ror4(D ^ A, 16)
    C = (C + D) & M4
    B = ror4(B ^ C, 12)
    A = (A + B + Y) & M4
    D = ror4(D ^ A, 8)
    C = (C + D) & M4
    B = ror4(B ^ C, 7)
    return [A, B, C, D]


def diag(S):
    A, B, C, D = S
    return [A, rot256(B, 64), rot256(C, 128), rot256(D, 192)]


def undiag(S):
    A, B, C, D = S
    return [A, rot256(B, 192), rot256(C, 128), rot256(D, 64)]


# ---------------- reference (inlined, identical to verifier/blake3.py for 1 block)
def _ror(v, n):
    return ((v >> n) | (v << (32 - n))) & MASK


def _g(v, a, b, c, d, x, y):
    v[a] = (v[a] + v[b] + x) & MASK
    v[d] = _ror(v[d] ^ v[a], 16)
    v[c] = (v[c] + v[d]) & MASK
    v[b] = _ror(v[b] ^ v[c], 12)
    v[a] = (v[a] + v[b] + y) & MASK
    v[d] = _ror(v[d] ^ v[a], 8)
    v[c] = (v[c] + v[d]) & MASK
    v[b] = _ror(v[b] ^ v[c], 7)


def reference_digest(m014, m15):
    m = list(m014) + [m15]
    v = list(IV) + list(IV[:4]) + [0, 0, 64, FLAGS]
    for _ in range(2):
        for a, b, c, d, x, y in SCHED:
            _g(v, a, b, c, d, m[x], m[y])
        m = [m[i] for i in PERM]
    return struct.pack("<8I", *[(v[i] ^ v[i + 8]) & MASK for i in range(8)])


def k_perm(dig):
    h = struct.unpack("<8I", dig)
    k = 0
    for j in range(4):
        k |= h[j] << (64 * j)
        k |= h[4 + (j + 1) % 4] << (64 * j + 32)
    return k


# ---------------- algorithm
def group_setup(m014):
    m = list(m014) + [0]
    v = list(IV) + list(IV[:4]) + [0, 0, 64, FLAGS]
    S = [sw(v[0:4]), sw(v[4:8]), sw(v[8:12]), sw(v[12:16])]
    S = G4(S, sw([m[0], m[2], m[4], m[6]]), sw([m[1], m[3], m[5], m[7]]))
    S = diag(S)
    A, B, C, D = S
    A = (A + B + sw([m[8], m[10], m[12], m[14]])) & M4
    D = ror4(D ^ A, 16)
    C = (C + D) & M4
    B = ror4(B ^ C, 12)
    mp = [m[i] for i in PERM]
    Q = A + B + sw([m[9], m[11], m[13], 0])
    X2, Y2 = sw([mp[0], mp[2], mp[4], mp[6]]), sw([mp[1], mp[3], mp[5], mp[7]])
    X3 = sw([mp[8], mp[10], mp[12], 0])
    Y3 = sw([mp[9], mp[11], mp[13], mp[15]])
    return (B, C, D), Q, X2, Y2, X3, Y3


def message_body(st, Qm, X3m):
    """Metered per-message body; Qm/X3m are the live counter registers."""
    (B, C, D), Q, X2, Y2, X3, Y3 = st
    A = Qm & M4
    D = ror4(D ^ A, 8)
    C = (C + D) & M4
    B = ror4(B ^ C, 7)
    S = undiag([A, B, C, D])
    S = G4(S, X2, Y2)
    S = diag(S)
    A, B, C, D = G4(S, X3m, Y3)
    H0 = A ^ rot256(C, 128)
    H1 = B ^ rot256(D, 128)
    K = H0 | (H1 << 32)
    h = unsw(H0) + [0] * 4
    h1 = unsw(H1)
    for j in range(4):
        h[4 + (j + 1) % 4] = h1[j]
    return K, struct.pack("<8I", *h)


def expand_prefixes(seed_hex, n_groups):
    raw = bytes.fromhex(seed_hex)
    out, counter = [], 0
    while len(out) < n_groups:
        words = []
        while len(words) < 15:
            words.extend(struct.unpack("<8I", hashlib.sha256(raw + counter.to_bytes(4, "little")).digest()))
            counter += 1
        out.append(words[:15])
    return out


def key_spread20(dig):
    o = struct.unpack("<8I", dig)
    return (o[0] & 0xFF) | ((o[1] & 0xFF) << 8) | ((o[2] & 0xF) << 16)


def run_trial(seed_hex, n_groups=32, per_group=32):
    bags = {}
    stats = {"meter_ok": 0, "meter_fail": 0, "ref_ok": 0, "ref_fail": 0, "k_ok": 0, "k_fail": 0}
    inserts = 0
    inc = Word(1 << 192)
    for m014 in expand_prefixes(seed_hex, n_groups):
        st = group_setup(m014)
        Qm, X3m = Word(int(st[1])), Word(int(st[4]))
        for y in range(per_group):
            Word.ops = 0
            K, dig = message_body(st, Qm, X3m)
            Qm = Qm + inc
            X3m = X3m + inc
            n = Word.ops
            stats["meter_ok" if n == EXPECTED_BODY else "meter_fail"] += 1
            ref = reference_digest(m014, y)
            stats["ref_ok" if dig == ref else "ref_fail"] += 1
            stats["k_ok" if int(K) == k_perm(ref) else "k_fail"] += 1
            msg = struct.pack("<16I", *(list(m014) + [y]))
            inserts += 1
            key = key_spread20(dig)
            if key in bags and bags[key] != msg:
                obs = dict(stats, messages=inserts, body_ops=n, expected_body_ops=EXPECTED_BODY, rot_cost=ROT_COST)
                return bags[key].hex(), msg.hex(), obs
            bags[key] = msg
    return None, None, dict(stats, messages=inserts, expected_body_ops=EXPECTED_BODY, rot_cost=ROT_COST)


def main():
    request = json.load(sys.stdin)
    rows = []
    for trial in request["trials"]:
        a, b, obs = run_trial(trial["seed"])
        rows.append({"trial": trial["trial"], "message_a_hex": a, "message_b_hex": b, "observations": obs})
    json.dump({"schema_version": 1, "trials": rows}, sys.stdout, sort_keys=True)


if __name__ == "__main__":
    main()
