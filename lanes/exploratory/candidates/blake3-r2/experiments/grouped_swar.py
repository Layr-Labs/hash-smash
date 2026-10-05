"""Scaled replay of the grouped partial-evaluation + 8-way SWAR two-round BLAKE3
birthday search.

Messages are 64-byte single root blocks. They are evaluated in groups that share
the fresh uniform words m0..m14 and enumerate m15. m15 enters only in the second
half of round 1's last G call G(3,4,9,14,m14,m15) and in round 2's last G call,
so round 1 up to that point is a group constant (group setup, scalar). The
m15-dependent inner body (round-1 tail + full round 2 + eight-word feed-forward)
is computed by the submitted 8-way SWAR packed evaluator: eight consecutive m15
values are packed into 256-bit words as eight disjoint 32-bit lanes, with
per-field carry-isolated addition, masked 32-bit rotation and field-wise XOR; lane
j's 256-bit digest is unpacked from o0..o7 = v[i]^v[i+8]. The organizer re-verifies
every returned pair against verifier/blake3.py:blake3(.,2), so a returned masked
match also certifies the grouped SWAR evaluator on those inputs.

Experiment ids select the message layout (both reuse the same evaluator):
  b3r2-grouped-swar-spread : 32 groups x 32 consecutive m15 (N_t = 1024)
  b3r2-grouped-swar-single : 1 group x 1024 consecutive m15 (most structured case)

With N_t = 1024 = 2^10 and a w = 20-bit digest mask, N_t^2/2^w = 1 = N^2/2^256 at
the full width. Under the independent-uniform model (heuristic H1) a trial has a
masked collision with probability 1 - prod_{i<1024}(1 - i/2^20) = 0.39327. All
N_t samples are evaluated; the first masked-equal pair is returned (else two
nulls). Observations report the 1-based first-match index and masked-pair count.
"""

import hashlib
import json
import struct
import sys

M = 0xFFFFFFFF
MASK256 = (1 << 256) - 1
IV = (0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A,
      0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19)
PERM = (2, 6, 3, 10, 7, 0, 4, 13, 1, 11, 12, 5, 9, 14, 15, 8)
SAMPLES = 1024
LAYOUT = {"b3r2-grouped-swar-spread": (32, 32), "b3r2-grouped-swar-single": (1, 1024)}


def _bc(v):
    r = 0
    for j in range(8):
        r |= (v & M) << (32 * j)
    return r


_H = _bc(0x80000000)
_NOTH = _bc(0x7FFFFFFF)
_ROT = {r: (_bc((1 << (32 - r)) - 1), _bc(((1 << r) - 1) << (32 - r))) for r in (16, 12, 8, 7)}


def _padd(x, y):
    return (((x & _NOTH) + (y & _NOTH)) & MASK256) ^ ((x ^ y) & _H)


def _pror(x, r):
    rm, lm = _ROT[r]
    return ((x >> r) & rm) | (((x << (32 - r)) & MASK256) & lm)


def _gp(v, a, b, c, d, x, y):
    v[a] = _padd(_padd(v[a], v[b]), x); v[d] = _pror(v[d] ^ v[a], 16)
    v[c] = _padd(v[c], v[d]);           v[b] = _pror(v[b] ^ v[c], 12)
    v[a] = _padd(_padd(v[a], v[b]), y); v[d] = _pror(v[d] ^ v[a], 8)
    v[c] = _padd(v[c], v[d]);           v[b] = _pror(v[b] ^ v[c], 7)


def _ror(x, r):
    return ((x >> r) | (x << (32 - r))) & M


def _gs(v, a, b, c, d, x, y):
    v[a] = (v[a] + v[b] + x) & M; v[d] = _ror(v[d] ^ v[a], 16)
    v[c] = (v[c] + v[d]) & M;     v[b] = _ror(v[b] ^ v[c], 12)
    v[a] = (v[a] + v[b] + y) & M; v[d] = _ror(v[d] ^ v[a], 8)
    v[c] = (v[c] + v[d]) & M;     v[b] = _ror(v[b] ^ v[c], 7)


def _group_setup(m):
    v = list(IV) + list(IV[:4]) + [0, 0, 64, 11]
    _gs(v, 0, 4, 8, 12, m[0], m[1]); _gs(v, 1, 5, 9, 13, m[2], m[3])
    _gs(v, 2, 6, 10, 14, m[4], m[5]); _gs(v, 3, 7, 11, 15, m[6], m[7])
    _gs(v, 0, 5, 10, 15, m[8], m[9]); _gs(v, 1, 6, 11, 12, m[10], m[11])
    _gs(v, 2, 7, 8, 13, m[12], m[13])
    # m15-invariant first half of G(3,4,9,14,m14,m15)
    v[3] = (v[3] + v[4] + m[14]) & M; v[14] = _ror(v[14] ^ v[3], 16)
    v[9] = (v[9] + v[14]) & M;        v[4] = _ror(v[4] ^ v[9], 12)
    v[3] = (v[3] + v[4]) & M          # precombine v3_half + v4_half
    m2 = [m[PERM[i]] for i in range(16)]
    return v, m2


def _inner_swar8(base, m2, m15_packed):
    v = [_bc(x) for x in base]
    v[3] = _padd(v[3], m15_packed); v[14] = _pror(v[14] ^ v[3], 8)
    v[9] = _padd(v[9], v[14]);      v[4] = _pror(v[4] ^ v[9], 7)
    mm = [_bc(x) for x in m2]; mm[14] = m15_packed
    _gp(v, 0, 4, 8, 12, mm[0], mm[1]); _gp(v, 1, 5, 9, 13, mm[2], mm[3])
    _gp(v, 2, 6, 10, 14, mm[4], mm[5]); _gp(v, 3, 7, 11, 15, mm[6], mm[7])
    _gp(v, 0, 5, 10, 15, mm[8], mm[9]); _gp(v, 1, 6, 11, 12, mm[10], mm[11])
    _gp(v, 2, 7, 8, 13, mm[12], mm[13]); _gp(v, 3, 4, 9, 14, mm[14], mm[15])
    return [v[i] ^ v[i + 8] for i in range(8)]


def _group_digests(prefix, per_group):
    """prefix: m0..m14 (15 words). Returns per_group digests (32-byte), m15 = 0..per_group-1."""
    base, m2 = _group_setup(list(prefix) + [0])
    out = []
    for b in range(0, per_group, 8):
        m15p = 0
        for j in range(8):
            m15p |= (b + j) << (32 * j)
        o = _inner_swar8(base, m2, m15p)
        for j in range(8):
            out.append(b"".join(struct.pack("<I", (o[i] >> (32 * j)) & M) for i in range(8)))
    return out[:per_group]


def _prefix(seed, g):
    data = hashlib.shake_256(b"b3r2-grouped-prefix|" + seed + struct.pack("<I", g)).digest(60)
    return struct.unpack("<15I", data)


def _message(prefix, m15):
    return b"".join(struct.pack("<I", w) for w in prefix) + struct.pack("<I", m15)


def _trial(seed, groups, per_group, mask):
    seen = {}
    first = (None, None, 0)
    pairs = 0
    idx = 0
    for g in range(groups):
        pre = _prefix(seed, g)
        digs = _group_digests(pre, per_group)
        for u in range(per_group):
            idx += 1
            d = int.from_bytes(digs[u], "big") & mask
            bucket = seen.setdefault(d, [])
            if bucket:
                pairs += len(bucket)
                if first[0] is None:
                    pg, pu = bucket[0]
                    first = (_message(_prefix(seed, pg), pu).hex(), _message(pre, u).hex(), idx)
            bucket.append((g, u))
    return first[0], first[1], first[2], pairs


def main():
    request = json.loads(sys.stdin.read())
    groups, per_group = LAYOUT[request["experiment_id"]]
    assert groups * per_group == SAMPLES
    mask = int(request["event"]["mask_hex"], 16)
    out = []
    for item in request["trials"]:
        a, b, fi, pairs = _trial(bytes.fromhex(item["seed"]), groups, per_group, mask)
        out.append({"trial": item["trial"], "message_a_hex": a, "message_b_hex": b,
                    "observations": {"first_match_sample": fi, "masked_pairs": pairs}})
    sys.stdout.write(json.dumps({"schema_version": 1, "trials": out}, separators=(",", ":")))


if __name__ == "__main__":
    main()
