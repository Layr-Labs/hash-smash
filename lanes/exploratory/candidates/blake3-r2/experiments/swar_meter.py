"""SWAR (4 lanes x 64-bit slots per 256-bit word) Word-op meter + matched-scale
masked birthday (python-message-pairs-v1).

Accounting: every +,-,&,|,^,<<,>> on a 256-bit Word counts 1 (organizer
convention of scripts/reference_operation_costs.py); results reduced mod 2^256.
A 256-bit word rotation is charged ROT_COST=3 (shr + shl + or), i.e. we do NOT
rely on the cost model's listed "rotation" primitive.  Lane rotations inside a
slot are (t>>n)|(t<<(32-n)) then &M4 (4 ops for four lanes at once).

Per message the metered body is: 2 counter-register increments, R1 diagonal
second half (13), undiagonalize (3 rot x 3), R2 column G4 (30), diagonalize
(3 rot x 3), R2 diagonal G4 (30), fused feed-forward+pack (8):
  K = (A | (B<<32)) ^ rot256(C | (D<<32), 128)
which is algebraically identical to the 126.241 H0/H1 then K=H0|(H1<<32)
programme (10 ops) under Lemma S cleanliness. Expected total = 101 with
ROT_COST=3 (was 103 in ef428b33 / draft_swar_126.241).

Word-meter is sampled once per trial (segment/body count is straight-line);
every birthday digest uses a plain-int twin; a sample (first REF_SAMPLE=8
messages of group 0, plus both messages of any returned pair) is checked
bit-for-bit against an inlined 2-round root compression identical to
verifier/blake3.py, with K checked against the fixed bit-permutation. (Checking
every message was dropped for the organizer's 20s Docker timeout; the host
independently recomputes digests of returned pairs.) Observation op counts are untrusted
labels. Flat numeric observations only.
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
EXPECTED_BODY = 101
REF_SAMPLE = 8


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


def digest_from_k(K):
    """Recover 8 little-endian lanes from the fixed K bit-permutation."""
    h = [0] * 8
    kv = int(K)
    for j in range(4):
        slot = (kv >> (64 * j)) & ((1 << 64) - 1)
        h[j] = slot & MASK
        h[4 + (j + 1) % 4] = (slot >> 32) & MASK
    return struct.pack("<8I", *h)


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
    # Fused FF+pack (8 ops): algebraically = (A^rotC) | ((B^rotD)<<32)
    # under clean slots (Lemma S). Saves 2 vs separate H0/H1 then pack.
    AB = A | (B << 32)
    CD = C | (D << 32)
    CD = rot256(CD, 128)
    K = AB ^ CD
    return K, digest_from_k(K)


# Plain-int twin (no Word accounting) for birthday throughput.
def _psw(vals):
    return sum((int(x) & MASK) << (64 * j) for j, x in enumerate(vals))


def _punsw(w):
    return [(int(w) >> (64 * j)) & MASK for j in range(4)]


_PM4 = sum(MASK << (64 * j) for j in range(4))


def _pror4(t, n):
    return ((t >> n) | (t << (32 - n))) & _PM4


def _prot256(x, k):
    v = int(x) & W
    return ((v >> k) | (v << (256 - k))) & W


def _pG4(S, X, Y):
    A, B, C, D = S
    A = (A + B + X) & _PM4
    D = _pror4(D ^ A, 16)
    C = (C + D) & _PM4
    B = _pror4(B ^ C, 12)
    A = (A + B + Y) & _PM4
    D = _pror4(D ^ A, 8)
    C = (C + D) & _PM4
    B = _pror4(B ^ C, 7)
    return [A, B, C, D]


def _pdiag(S):
    A, B, C, D = S
    return [A, _prot256(B, 64), _prot256(C, 128), _prot256(D, 192)]


def _pundiag(S):
    A, B, C, D = S
    return [A, _prot256(B, 192), _prot256(C, 128), _prot256(D, 64)]


def group_setup_plain(m014):
    m = list(m014) + [0]
    v = list(IV) + list(IV[:4]) + [0, 0, 64, FLAGS]
    S = [_psw(v[0:4]), _psw(v[4:8]), _psw(v[8:12]), _psw(v[12:16])]
    S = _pG4(S, _psw([m[0], m[2], m[4], m[6]]), _psw([m[1], m[3], m[5], m[7]]))
    S = _pdiag(S)
    A, B, C, D = S
    A = (A + B + _psw([m[8], m[10], m[12], m[14]])) & _PM4
    D = _pror4(D ^ A, 16)
    C = (C + D) & _PM4
    B = _pror4(B ^ C, 12)
    mp = [m[i] for i in PERM]
    Q = (A + B + _psw([m[9], m[11], m[13], 0])) & W
    X2, Y2 = _psw([mp[0], mp[2], mp[4], mp[6]]), _psw([mp[1], mp[3], mp[5], mp[7]])
    X3 = _psw([mp[8], mp[10], mp[12], 0])
    Y3 = _psw([mp[9], mp[11], mp[13], mp[15]])
    return (B, C, D), Q, X2, Y2, X3, Y3


def message_body_plain(st, Qm, X3m):
    (B, C, D), Q, X2, Y2, X3, Y3 = st
    A = Qm & _PM4
    D = _pror4(D ^ A, 8)
    C = (C + D) & _PM4
    B = _pror4(B ^ C, 7)
    S = _pundiag([A, B, C, D])
    S = _pG4(S, X2, Y2)
    S = _pdiag(S)
    A, B, C, D = _pG4(S, X3m, Y3)
    AB = (A | ((B << 32) & W)) & W
    CD = (C | ((D << 32) & W)) & W
    CD = _prot256(CD, 128)
    K = AB ^ CD
    return K, digest_from_k(K)


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
    prefixes = expand_prefixes(seed_hex, n_groups)
    # Word-meter once (straight-line body; count message-independent at ROT_COST).
    st_w = group_setup(prefixes[0])
    Qm_w, X3m_w = Word(int(st_w[1])), Word(int(st_w[4]))
    Word.ops = 0
    K_w, dig_w = message_body(st_w, Qm_w, X3m_w)
    Qm_w = Qm_w + Word(1 << 192)
    X3m_w = X3m_w + Word(1 << 192)
    n = Word.ops
    ref0 = reference_digest(prefixes[0], 0)
    if n == EXPECTED_BODY and dig_w == ref0 and int(K_w) == k_perm(ref0):
        stats["meter_ok"] = 1
    else:
        stats["meter_fail"] = 1

    inc = 1 << 192
    # Reference check: the first REF_SAMPLE messages of group 0 plus both
    # messages of any returned pair (the host re-verifies returned pairs anyway).
    # Checking every message doubled runtime against the 20s Docker timeout.
    def _check(m014, y, K, dig):
        ref = reference_digest(m014, y)
        stats["ref_ok" if dig == ref else "ref_fail"] += 1
        stats["k_ok" if int(K) == k_perm(ref) else "k_fail"] += 1
    seen = {}
    for gi, m014 in enumerate(prefixes):
        st = group_setup_plain(m014)
        Qm, X3m = int(st[1]) & W, int(st[4]) & W
        for y in range(per_group):
            K, dig = message_body_plain(st, Qm, X3m)
            Qm = (Qm + inc) & W
            X3m = (X3m + inc) & W
            if gi == 0 and y < REF_SAMPLE:
                _check(m014, y, K, dig)
            msg = struct.pack("<16I", *(list(m014) + [y]))
            inserts += 1
            key = key_spread20(dig)
            if key in bags and bags[key] != msg:
                pg, py, pK, pdig = seen[key]
                if not (pg == 0 and py < REF_SAMPLE):
                    _check(prefixes[pg], py, pK, pdig)
                if not (gi == 0 and y < REF_SAMPLE):
                    _check(m014, y, K, dig)
                obs = dict(stats, messages=inserts, body_ops=n, expected_body_ops=EXPECTED_BODY, rot_cost=ROT_COST)
                return bags[key].hex(), msg.hex(), obs
            bags[key] = msg
            seen[key] = (gi, y, K, dig)
    return None, None, dict(stats, messages=inserts, body_ops=n, expected_body_ops=EXPECTED_BODY, rot_cost=ROT_COST)


def main():
    request = json.load(sys.stdin)
    rows = []
    for trial in request["trials"]:
        a, b, obs = run_trial(trial["seed"])
        for key, value in obs.items():
            if type(key) is not str or type(value) not in (int, float, bool):
                raise SystemExit(f"non-flat observation: {key}={type(value).__name__}")
        if len(obs) > 16:
            raise SystemExit(f"too many observation keys: {len(obs)}")
        rows.append({"trial": trial["trial"], "message_a_hex": a, "message_b_hex": b, "observations": obs})
    json.dump({"schema_version": 1, "trials": rows}, sys.stdout, sort_keys=True)


if __name__ == "__main__":
    main()
