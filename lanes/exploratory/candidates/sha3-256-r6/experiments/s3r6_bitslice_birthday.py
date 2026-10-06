"""Scaled analogue of the bitsliced grouped birthday search of proof.md (sha3-256-r6).

Stdlib only. Organizer mode (default): read one JSON request on stdin and write
one JSON result. Every digest used for matching is computed ONLY by the
bitsliced grouped evaluator of proof.md Sections 4-5, in the same order and
with the same encodings as the counted program:

  * a batch is 256 bit positions; bit position p of every 256-bit word belongs
    to one group (one 64-byte prefix); word P(L, b) holds bit b of lane L for
    all 256 groups at once;
  * per batch: A2 (round-1 output + round-2 theta) for z = 0, the coefficient
    words COEF[j] on the 62 support positions of Lemma 3, and O2P = the round-2
    output with round-3 theta applied, in lane-complement encoding Q3;
  * each Gray step on z-bit j XORs COEF[j] into A2 and patches O2P with the
    exact chi difference of the affected round-2 rows plus the induced change
    of the round-3 D words (incremental round 2, Lemma 6);
  * rounds 3, 4 and 5 read a theta'd input, use lane-complement chi (gates and
    complemented copies chosen per chi row from the lane polarities, round
    constants folded into polarity), and add the next round's D words before
    storing (plane 0 is fixed up from 5 words) (Lemma 7);
  * the last round computes only chi row 0, lanes 0..3: 256 key rows in the
    encoding KEYMASK (stored key = digest read little-endian XOR KEYMASK);
  * the 256 x 256 delta-swap transpose runs stages 1, 2, 4, 64, 128 then
    8, 16, 32 and the keys are offered in processing order q = 0..255, slot
    decode_slot(q).

Several trials share one batch (each trial owns G consecutive bit positions);
bitwise operations never mix bit positions and the transpose only relocates
bits, so trials stay independent: each trial's output depends on its own seed.

Scale: N_t = 2^9 messages per trial and an 18-bit digest mask, so
N_t^2 / 2^18 = 1 = N^2 / 2^256 as in the full attack. Layouts (G groups per
trial x Z values of z, z in Gray order):

  k6r6-bs-full-width   : 256 groups x 2,  z = gray(t), t < 2
  k6r6-bs-spread       : 16 groups x 32,  z = gray(t), t < 32
  k6r6-bs-single-group : 1 group x 512,   z = gray(t), t < 512
  k6r6-bs-high-z       : 4 groups x 128,  z = gray(t) << 25, t < 128

Self-checks (any failure raises, so the organizer run fails visibly):
  * per trial, the first EXACT_CHECKS keys in processing order, and the first
    key of the trial at every step t = 2^i (one step of every Gray block used),
    are compared at full 256-bit width with an independent direct 6-round
    sponge (sponge6: own rho offsets and round constants);
  * for every coefficient column built, A2(e_j) XOR A2(0) vanishes outside the
    62 support positions;
  * after the last step of every batch, the incrementally maintained O2P is
    compared word for word with O2P rebuilt from the current A2.

The first pair of distinct messages whose masked digests agree is returned; a
trial with no such pair returns two nulls. Observations are informational.

Local modes (not used by the organizer):
  python3 FILE --local LAYOUT TRIALS SEED   real target, local seeds
"""

import hashlib
import itertools
import json
import sys

M64 = (1 << 64) - 1
W = (1 << 256) - 1
RC = (0x0000000000000001, 0x0000000000008082, 0x800000000000808A,
      0x8000000080008000, 0x000000000000808B, 0x0000000080000001)
RHO = (0, 1, 62, 28, 27, 36, 44, 6, 55, 20, 3, 10, 43, 25, 39,
       41, 45, 15, 21, 8, 18, 2, 61, 56, 14)
DIAG = (0, 6, 12, 18, 24)
EXACT_CHECKS = 4

LAYOUTS = {   # groups per trial, list of z in processing order
    "k6r6-bs-full-width": (256, [t ^ (t >> 1) for t in range(2)]),
    "k6r6-bs-spread": (16, [t ^ (t >> 1) for t in range(32)]),
    "k6r6-bs-single-group": (1, [t ^ (t >> 1) for t in range(512)]),
    "k6r6-bs-high-z": (4, [(t ^ (t >> 1)) << 25 for t in range(128)]),
}
MASKS = {
    "k6r6-bs-full-width": "1f00000000000000001f00000000000000000f00000000000000000f00000000",
    "k6r6-bs-spread": "0000f80000000000000000001f0000000000000000f00000000000000f000000",
    "k6r6-bs-single-group": "00000000000000f800000000000000f800000000000000f000000000000000f0",
    "k6r6-bs-high-z": "000000001f00000000000000001f00000000000000000f00000f000000000000",
}


# ---------------- independent direct sponge (exactness reference) ----------
def _keccak_tables():
    rho = [[0] * 5 for _ in range(5)]
    x, y = 1, 0
    for t in range(24):
        rho[x][y] = ((t + 1) * (t + 2) // 2) % 64
        x, y = y, (2 * x + 3 * y) % 5
    rc, r = [], 1
    for _ in range(6):
        c = 0
        for j in range(7):
            if r & 1:
                c |= 1 << ((1 << j) - 1)
            r = ((r << 1) ^ 0x71) & 0xFF if r & 0x80 else r << 1
        rc.append(c)
    return rho, rc


_TABLES = _keccak_tables()


def sponge6(msg):
    """Direct SHA3-256 sponge with Keccak rounds 0..5 on one 136-byte block."""
    rho, rc = _TABLES
    block = bytearray(msg) + bytearray(136 - len(msg))
    block[len(msg)] ^= 0x06
    block[135] ^= 0x80
    a = [[int.from_bytes(block[8 * (x + 5 * y):8 * (x + 5 * y) + 8], "little") if x + 5 * y < 17 else 0
          for y in range(5)] for x in range(5)]
    for rnd in range(6):
        c = [a[x][0] ^ a[x][1] ^ a[x][2] ^ a[x][3] ^ a[x][4] for x in range(5)]
        d = [c[(x - 1) % 5] ^ (((c[(x + 1) % 5] << 1) | (c[(x + 1) % 5] >> 63)) & M64) for x in range(5)]
        b = [[0] * 5 for _ in range(5)]
        for x in range(5):
            for y in range(5):
                v, r = a[x][y] ^ d[x], rho[x][y]
                b[y][(2 * x + 3 * y) % 5] = ((v << r) | (v >> (64 - r))) & M64 if r else v
        a = [[b[x][y] ^ ((~b[(x + 1) % 5][y]) & b[(x + 2) % 5][y]) for y in range(5)] for x in range(5)]
        a[0][0] ^= rc[rnd]
    return b"".join(a[x][0].to_bytes(8, "little") for x in range(4))


def message(prefix, z):
    m = bytearray(prefix)
    for k in range(4):
        m[k] ^= (z >> (8 * k)) & 0xFF
        m[40 + k] ^= (z >> (8 * k)) & 0xFF
    return bytes(m)


# ---------------- bitsliced geometry -----------------------------------------
# word index of P(L, b) is 64*L + b
def _pi_src(X, Y):
    return ((Y - 3 * X) * 3) % 5, X


def _bsrc(X, Y, b):
    """A2 word (L, b') read by rho/pi output position (X, Y) at plane b."""
    xs, ys = _pi_src(X, Y)
    L = xs + 5 * ys
    return L, (b - RHO[L]) % 64


SRC = []      # source word index, output order p = 64*(X + 5Y) + b
DIDX = []     # D word index of the source
BS0 = []      # (p, xs) with source plane 0: receives the plane-0 fix-up
for _Y in range(5):
    for _X in range(5):
        _xs, _ys = _pi_src(_X, _Y)
        _L = _xs + 5 * _ys
        for _b in range(64):
            _bs = (_b - RHO[_L]) % 64
            if _bs == 0:
                BS0.append((len(SRC), _xs))
            SRC.append(64 * _L + _bs)
            DIDX.append(64 * _xs + _bs)
CHI1 = [64 * ((X + 1) % 5 + 5 * Y) + b for Y in range(5) for X in range(5) for b in range(64)]
CHI2 = [64 * ((X + 2) % 5 + 5 * Y) + b for Y in range(5) for X in range(5) for b in range(64)]
DPREV = [64 * ((x - 1) % 5) + b for x in range(5) for b in range(64)]
DNEXT = [64 * ((x + 1) % 5) + (b - 1) % 64 for x in range(5) for b in range(64)]
DCOL = [64 * ((i // 64) % 5) + i % 64 for i in range(1600)]


def d_words(S):
    """Theta D words (index 64x + b) of a bitsliced state."""
    C = [S[i] ^ S[i + 320] ^ S[i + 640] ^ S[i + 960] ^ S[i + 1280] for i in range(320)]
    return [C[p] ^ C[n] for p, n in zip(DPREV, DNEXT)]


def round_pass(S, D, rc):
    """Setup round 1 (plain encoding): theta + rho + pi + chi + iota; returns (state, D of output)."""
    B = [S[s] ^ D[d] for s, d in zip(SRC, DIDX)]
    out = [v ^ ((B[i] ^ W) & B[j]) for v, i, j in zip(B, CHI1, CHI2)]
    for b in range(64):
        if (rc >> b) & 1:
            out[b] ^= W
    return out, d_words(out)


# ---------------- lane-complement polarity (Keccak team; tekkac b001199a) ----
def lanepol(p, L):
    return (p >> L) & 1


def fpol(pout):
    """Polarity of the theta'd next-round input given chi-output polarity pout."""
    pc = [0] * 5
    for L in range(25):
        pc[L % 5] ^= lanepol(pout, L)
    q = 0
    for L in range(25):
        x = L % 5
        q |= (lanepol(pout, L) ^ pc[(x - 1) % 5] ^ pc[(x + 1) % 5]) << L
    return q


_ROWCACHE = {}


def solve_row(q, p, iota, outs):
    """Cheapest gate plan of one chi row: inputs with polarity bits q, wanted
    output polarities p, iota flip of output 0. plan[X] = (ca, cb, cc, gate,
    outnot): c* = 1 uses a complemented copy of that input."""
    key = (q, p, iota, tuple(outs))
    if key in _ROWCACHE:
        return _ROWCACHE[key]
    qb = [(q >> k) & 1 for k in range(5)]
    pb_ = [(p >> k) & 1 for k in range(5)]
    best = None
    for Sm in range(32):
        S = [k for k in range(5) if (Sm >> k) & 1]
        cost = len(S)
        plan = {}
        for X in outs:
            ib = iota if X == 0 else 0
            bo = None
            for ca, cb, cc in itertools.product((0, 1), repeat=3):
                if (ca and X not in S) or (cb and (X + 1) % 5 not in S) or (cc and (X + 2) % 5 not in S):
                    continue
                pa = qb[X] ^ ca
                pbb = qb[(X + 1) % 5] ^ cb
                pcc = qb[(X + 2) % 5] ^ cc
                if (pbb, pcc) == (1, 0):
                    gate, pT = "and", 0
                elif (pbb, pcc) == (0, 1):
                    gate, pT = "or", 1
                else:
                    continue
                on = int(pa ^ pT ^ ib != pb_[X])
                if bo is None or on < bo[0]:
                    bo = (on, (ca, cb, cc, gate, on))
            if bo is None:
                cost = 99
                break
            cost += bo[0]
            plan[X] = bo[1]
        if best is None or cost < best[0]:
            best = (cost, S, plan)
    _ROWCACHE[key] = best
    return best


P34 = 1336081           # chi-output polarity of rounds 3 and 4 (and of round 2 into O2P)
P5 = 1188625            # chi-output polarity of round 5
Q3 = fpol(P34)          # polarity of O2P and of the round-4 and round-5 inputs
QLAST = fpol(P5)        # polarity of the round-6 input


def _rowq(qin, Y):
    return sum(lanepol(qin, _pi_src(X, Y)[0] + 5 * _pi_src(X, Y)[1]) << X for X in range(5))


def chi_plan(qin, pout, rc):
    """Per output word p = 64(X+5Y)+b: (a, amask, b, bmask, c, cmask, is_or, outmask)."""
    plan = []
    for Y in range(5):
        qrow, prow = _rowq(qin, Y), (pout >> (5 * Y)) & 31
        for X in range(5):
            for b in range(64):
                io = (rc >> b) & 1 if Y == 0 else 0
                ca, cb, cc, gate, on = solve_row(qrow, prow, io, range(5))[2][X]
                plan.append((64 * (X + 5 * Y) + b, W if ca else 0,
                             64 * ((X + 1) % 5 + 5 * Y) + b, W if cb else 0,
                             64 * ((X + 2) % 5 + 5 * Y) + b, W if cc else 0,
                             gate == "or", W if on else 0))
    return plan


def last_plan(b):
    q = sum(lanepol(QLAST, DIAG[X]) << X for X in range(5))
    io = (RC[5] >> b) & 1
    best = None
    for p in range(16):
        r = solve_row(q, p, io, range(4))
        if best is None or r[0] < best[0][0]:
            best = (r, p)
    return best


LASTPLAN = [last_plan(b) for b in range(64)]
KEYMASK = 0              # stored key = digest (little-endian int) XOR KEYMASK
for _b in range(64):
    for _x in range(4):
        KEYMASK |= ((LASTPLAN[_b][1] >> _x) & 1) << (64 * _x + _b)

PLAN2 = chi_plan(0, P34, RC[1])
PLAN3 = chi_plan(Q3, P34, RC[2])
PLAN4 = chi_plan(Q3, P34, RC[3])
PLAN5 = chi_plan(Q3, P5, RC[4])


def chi(B, plan):
    return [B[a] ^ am ^ ((((B[b] ^ bm) | (B[c] ^ cm)) if g else ((B[b] ^ bm) & (B[c] ^ cm))) ^ om)
            for a, am, b, bm, c, cm, g, om in plan]


def round_ts(src, fix, plan):
    """Round with theta'd input (plane 0 lacking fix[x] unless fix is None),
    lane-complement chi, and the next round's D added before the store for
    planes b >= 1; returns (stored state, fix-up words D_next[x][0])."""
    B = [src[s] for s in SRC]
    if fix is not None:
        for p, xs in BS0:
            B[p] ^= fix[xs]
    out = chi(B, plan)
    D = d_words(out)
    fix_out = [D[64 * x] for x in range(5)]
    for x in range(5):
        D[64 * x] = 0
    return [o ^ D[k] for o, k in zip(out, DCOL)], fix_out


def build_o2p(A2):
    out, fix = round_ts(A2, None, PLAN2)
    for L in range(25):
        out[64 * L] ^= fix[L % 5]
    return out


def last_rows(S, fix):
    rows = [0] * 256
    for b in range(64):
        B = []
        for X in range(5):
            L = DIAG[X]
            bs = (b - RHO[L]) % 64
            B.append(S[64 * L + bs] ^ (fix[X] if bs == 0 else 0))
        (_, Sset, plan), _ = LASTPLAN[b]
        for x in range(4):
            ca, cb, cc, gate, on = plan[x]
            a = B[x] ^ (W if ca else 0)
            u = B[(x + 1) % 5] ^ (W if cb else 0)
            v = B[(x + 2) % 5] ^ (W if cc else 0)
            rows[64 * x + b] = a ^ ((u | v) if gate == "or" else (u & v)) ^ (W if on else 0)
    return rows


# ---------------- transpose ----------------------------------------------------
def _mask(d):
    m = 0
    for c in range(256):
        if not c & d:
            m |= 1 << c
    return m


MASKD = {d: _mask(d) for d in (1, 2, 4, 8, 16, 32, 64, 128)}


def transpose(rows, order):
    """256 x 256 bit transpose by delta swaps; the stages commute, `order` mirrors the program."""
    R = list(rows)
    for d in order:
        m = MASKD[d]
        for i0 in range(256):
            if not i0 & d:
                a, b = R[i0], R[i0 + d]
                t = ((a >> d) ^ b) & m
                R[i0] = a ^ (t << d)
                R[i0 + d] = b ^ t
    return R


SETUP_ORDER = (1, 2, 4, 8, 16, 32, 64, 128)
STEP_ORDER = (1, 2, 4, 64, 128, 8, 16, 32)


def decode_slot(q):
    """Processing index q (0..255) of a z-step -> group slot (bit position)."""
    gi, i = q >> 3, q & 7
    return 64 * (gi >> 3) + 8 * i + (gi & 7)


PROC = [decode_slot(q) for q in range(256)]
assert sorted(PROC) == list(range(256))


# ---------------- Gray support and incremental round 2 -------------------------
def support(j):
    jp = (j + 36) % 64
    pos = set()
    for x, b in ((1, j), (4, j + 1), (1, jp), (4, jp + 1), (4, j), (2, j + 1),
                 (0, j), (3, j + 1), (0, jp), (3, jp + 1), (2, jp), (0, jp + 1)):
        for y in range(5):
            pos.add((x + 5 * y, b % 64))
    pos.add((3, j))
    pos.add((19, jp))
    return sorted(pos)


SUPPORT = [support(j) for j in range(32)]
assert all(len(s) == 62 for s in SUPPORT)


def incr_rows(j):
    """Affected round-2 chi rows of z-bit j: {(Y, plane): {X: (k, L, b)}}."""
    rows = {}
    for k, (L, b) in enumerate(SUPPORT[j]):
        x, y = L % 5, L // 5
        X, Y = y, (2 * x + 3 * y) % 5
        rows.setdefault((Y, (b + RHO[L]) % 64), {})[X] = (k, L, b)
    return sorted(rows.items())


ROWS2 = [incr_rows(j) for j in range(32)]


def incr_round2(A2, O2P, coef, j):
    """A2 ^= COEF[j] on the support; O2P ^= exact chi difference + induced dD3 (Lemma 6)."""
    dout = {}
    for (Y, bp), d in ROWS2[j]:
        if len(d) == 1:
            (X, (k, L, bs)), = d.items()
            c = coef[k]
            A2[64 * L + bs] ^= c
            Lp, bp1 = _bsrc((X + 1) % 5, Y, bp)
            Lm, bm1 = _bsrc((X - 1) % 5, Y, bp)
            dout[(X, Y, bp)] = c
            if c == W:
                dout[((X - 1) % 5, Y, bp)] = A2[64 * Lp + bp1]
                dout[((X - 2) % 5, Y, bp)] = A2[64 * Lm + bm1] ^ W
            else:
                dout[((X - 1) % 5, Y, bp)] = c & A2[64 * Lp + bp1]
                dout[((X - 2) % 5, Y, bp)] = (A2[64 * Lm + bm1] ^ W) & c
        else:
            xs = sorted(d.keys())
            if xs == [2, 4]:
                B = [A2[64 * _bsrc(X, Y, bp)[0] + _bsrc(X, Y, bp)[1]] for X in range(5)]
                for X in (2, 4):
                    L, bs = _bsrc(X, Y, bp)
                    if coef[d[X][0]] != W:
                        raise RuntimeError("expected c=W on 2-input row [2,4]")
                    A2[64 * L + bs] = B[X] ^ W
                dout[(0, Y, bp)] = B[1] ^ W
                dout[(1, Y, bp)] = B[3]
                dout[(2, Y, bp)] = B[3]
                dout[(3, Y, bp)] = B[0]
                dout[(4, Y, bp)] = W
            elif xs == [1, 2]:
                B = [A2[64 * _bsrc(X, Y, bp)[0] + _bsrc(X, Y, bp)[1]] for X in range(4)]
                if coef[d[1][0]] != W:
                    raise RuntimeError("expected c1=W on 2-input row [1,2]")
                c2 = coef[d[2][0]]
                L1, bs1 = _bsrc(1, Y, bp)
                L2, bs2 = _bsrc(2, Y, bp)
                A2[64 * L1 + bs1] = B[1] ^ W
                A2[64 * L2 + bs2] = B[2] ^ c2
                dout[(0, Y, bp)] = B[2] ^ (B[1] & c2)
                dout[(1, Y, bp)] = (c2 & B[3]) ^ W
                dout[(2, Y, bp)] = c2
                dout[(4, Y, bp)] = B[0] ^ W
            else:
                raise RuntimeError("unexpected 2-input row pattern")
    dC = {}
    for (x, Y, b), v in dout.items():
        dC[(x, b)] = dC.get((x, b), 0) ^ v
    dD = {}
    for (x, b), v in dC.items():
        for key in (((x + 1) % 5, b), ((x - 1) % 5, (b + 1) % 64)):
            dD[key] = dD.get(key, 0) ^ v
    # Check that the two cancelled dD columns (1, (41+j)%64) and (3, (40+j)%64) vanish identically
    if dD.get((1, (41 + j) % 64), 0) != 0 or dD.get((3, (40 + j) % 64), 0) != 0:
        raise RuntimeError("expected linear cancellation in dD columns (1,41+j) and (3,40+j)")
    for (x, Y, b), v in dout.items():
        O2P[64 * (x + 5 * Y) + b] ^= v
    for (x, b), v in dD.items():
        if (x, b) in ((1, (41 + j) % 64), (3, (40 + j) % 64)):
            continue
        for Y in range(5):
            O2P[64 * (x + 5 * Y) + b] ^= v


# ---------------- batch ------------------------------------------------------
class Batch:
    """256 groups (bit positions); prefixes[p] is a 64-byte prefix (or zeros)."""

    def __init__(self, prefixes, zbits):
        S = [0] * 1600
        for w in range(2):
            rows = [int.from_bytes(p[32 * w:32 * w + 32], "little") for p in prefixes]
            S[256 * w:256 * w + 256] = transpose(rows, SETUP_ORDER)
        S[64 * 8 + 1] = W
        S[64 * 8 + 2] = W
        S[64 * 16 + 63] = W
        D1 = d_words(S)                     # round-1 D, independent of z (Lemma 1)
        out, D2 = round_pass(S, D1, RC[0])
        self.A2 = [out[i] ^ D2[DCOL[i]] for i in range(1600)]
        self.coef = {}
        for j in zbits:
            S2 = list(S)
            S2[j] ^= W
            S2[64 * 5 + j] ^= W
            if d_words(S2) != D1:
                raise RuntimeError("round-1 theta not invariant under the z flip")
            o2, D22 = round_pass(S2, D1, RC[0])
            A2j = [o2[i] ^ D22[DCOL[i]] for i in range(1600)]
            supp = {64 * L + b for L, b in SUPPORT[j]}
            for i in range(1600):
                if i not in supp and A2j[i] != self.A2[i]:
                    raise RuntimeError("z-dependence outside the 62-word support")
            col = [A2j[64 * L + b] ^ self.A2[64 * L + b] for L, b in SUPPORT[j]]
            if sum(1 for v in col if v == W) < 20 or len({v for v in col if v != W}) > 8:
                raise RuntimeError("COEF[j] failed 20-all-ones / 8-basis-word invariant")
            self.coef[j] = col
        self.O2P = build_o2p(self.A2)

    def flip(self, j):
        incr_round2(self.A2, self.O2P, self.coef[j], j)

    def check_o2p(self):
        if build_o2p(self.A2) != self.O2P:
            raise RuntimeError("incrementally maintained O2P differs from O2P rebuilt from A2")

    def keys(self):
        """Stored keys (digest XOR KEYMASK) indexed by slot."""
        S, fix = round_ts(self.O2P, None, PLAN3)
        S, fix = round_ts(S, fix, PLAN4)
        S, fix = round_ts(S, fix, PLAN5)
        return transpose(last_rows(S, fix), STEP_ORDER)


def trial_prefixes(seed, groups):
    return [b"".join(hashlib.sha256(b"s3r6-bitslice-v1" + seed + g.to_bytes(2, "little") + bytes((k,))).digest()
                     for k in (0, 1)) for g in range(groups)]


def _check(prefix, z, key):
    if int.from_bytes(sponge6(message(prefix, z)), "little") ^ KEYMASK != key:
        raise RuntimeError("bitsliced evaluator disagrees with direct sponge")


UNCOMP_BASE0 = (
    (0, 1, 40), (0, 4, 40), (1, 0, 44), (1, 1, 45), (1, 2, 8), (1, 2, 9),
    (1, 2, 44), (1, 2, 45), (1, 4, 14), (2, 1, 33), (2, 1, 62), (3, 0, 0),
    (3, 0, 37), (3, 1, 1), (3, 1, 28), (3, 2, 1), (3, 2, 37), (3, 3, 0),
    (3, 3, 28), (3, 4, 34), (3, 4, 63), (4, 3, 9),
)


def _mod_o2p_set(j):
    jp = (j + 36) % 64
    C = {(0, j): frozenset(["W"]), (3, j): frozenset(["u3"]), (4, j): frozenset(["u4"]),
         (0, jp): frozenset(["v0"]), (1, jp): frozenset(["W"]), (4, jp): frozenset(["v4"])}
    D = {}
    for (cx, cb), val in C.items():
        for dx, db in (((cx + 1) % 5, cb), ((cx - 1) % 5, (cb + 1) % 64)):
            D[(dx, db)] = D.get((dx, db), frozenset()) ^ val
    A2 = {}
    for (dx, db), val in D.items():
        if val:
            for y in range(5):
                A2[(dx + 5 * y, db)] = val
    for (L, b), val in (((0, j), frozenset(["W"])), ((3, j), frozenset(["u3"])), ((4, j), frozenset(["u4"])),
                        ((15, jp), frozenset(["v0"])), ((16, jp), frozenset(["W"])), ((19, jp), frozenset(["v4"]))):
        A2[(L, b)] = A2.get((L, b), frozenset()) ^ val
        if not A2[(L, b)]:
            del A2[(L, b)]
    rows = {}
    for (L, bs), val in A2.items():
        x, y = L % 5, L // 5
        rows.setdefault(((2 * x + 3 * y) % 5, (bs + RHO[L]) % 64), {})[y] = (L, bs, val)
    uncomp_j = {(x, Y, (b + j) % 64) for x, Y, b in UNCOMP_BASE0}
    dout = {}
    for (Y, bp), d in sorted(rows.items()):
        if len(d) == 1:
            (X, (L, bs, val)), = d.items()
            Lp, bp1 = _bsrc((X + 1) % 5, Y, bp)
            Lm, bm1 = _bsrc((X - 1) % 5, Y, bp)
            dout[(X, Y, bp)] = frozenset(("LIN", s) for s in val)
            dout[((X - 1) % 5, Y, bp)] = frozenset([("POS", val, (Lp, bp1))])
            pos_neg = ((X - 2) % 5, Y, bp)
            if pos_neg in uncomp_j:
                dout[pos_neg] = frozenset([("POS", val, (Lm, bm1))]) ^ frozenset(("LIN", s) for s in val)
            else:
                dout[pos_neg] = frozenset([("NEG", val, (Lm, bm1))])
        else:
            xs = sorted(d.keys())
            if xs == [2, 4]:
                dout[(0, Y, bp)] = (frozenset([("POS", frozenset(["W"]), _bsrc(1, Y, bp)), ("LIN", "W")])
                                    if (0, Y, bp) in uncomp_j else frozenset([("NEG", frozenset(["W"]), _bsrc(1, Y, bp))]))
                dout[(1, Y, bp)] = frozenset([("POS", frozenset(["W"]), _bsrc(3, Y, bp))])
                dout[(2, Y, bp)] = frozenset([("POS", frozenset(["W"]), _bsrc(3, Y, bp))])
                dout[(3, Y, bp)] = frozenset([("POS", frozenset(["W"]), _bsrc(0, Y, bp))])
                dout[(4, Y, bp)] = frozenset([("LIN", "W")])
            elif xs == [1, 2]:
                c2 = d[2][2]
                dout[(0, Y, bp)] = frozenset([("ROW12_0", c2, _bsrc(2, Y, bp), _bsrc(1, Y, bp))])
                dout[(1, Y, bp)] = (frozenset([("POS", c2, _bsrc(3, Y, bp)), ("LIN", "W")])
                                    if (1, Y, bp) in uncomp_j else frozenset([("NEG", c2, _bsrc(3, Y, bp))]))
                dout[(2, Y, bp)] = frozenset(("LIN", s) for s in c2)
                dout[(4, Y, bp)] = (frozenset([("POS", frozenset(["W"]), _bsrc(0, Y, bp)), ("LIN", "W")])
                                    if (4, Y, bp) in uncomp_j else frozenset([("NEG", frozenset(["W"]), _bsrc(0, Y, bp))]))
    dC = {}
    for (x, Y, b), v in dout.items():
        dC[(x, b)] = dC.get((x, b), frozenset()) ^ v
        if not dC[(x, b)]:
            del dC[(x, b)]
    dD = {}
    for (x, b), v in dC.items():
        for key in (((x + 1) % 5, b), ((x - 1) % 5, (b + 1) % 64)):
            dD[key] = dD.get(key, frozenset()) ^ v
            if not dD[key]:
                del dD[key]
    o2p = {}
    for (x, Y, b), v in dout.items():
        o2p[(x, Y, b)] = o2p.get((x, Y, b), frozenset()) ^ v
    for (x, b), v in dD.items():
        for Y in range(5):
            o2p[(x, Y, b)] = o2p.get((x, Y, b), frozenset()) ^ v
            if not o2p[(x, Y, b)]:
                del o2p[(x, Y, b)]
    return {(x + 5 * Y, b) for (x, Y, b) in o2p.keys()}, len(o2p)


def verify_schedule_counts():
    for j in range(32):
        m, o2p_len = _mod_o2p_set(j)
        if o2p_len != 1081:
            raise RuntimeError("expected 1081 modified O2P words")
        r0 = max(sum(1 for X in range(5) if _bsrc(X, Y, 0) in m) for Y in range(5))
        avail = [sum(1 for Y in range(5) for X in range(5) if _bsrc(X, Y, b) in m) for b in range(5)]
        # 56-register schedule (planes 0..3):
        s_ge3_56 = min(avail[3], 16)
        s_ge2_56 = min(avail[2] + s_ge3_56, 21)
        tot_56 = min(avail[0] + avail[1], (56 - 10 + r0) - s_ge2_56) + s_ge2_56
        # 64-register schedule (planes 0..4):
        s_ge3_64 = min(avail[3] + avail[4], 24)
        s_ge2_64 = min(avail[2] + s_ge3_64, 29)
        tot_64 = min(avail[0] + avail[1], (64 - 10 + r0) - s_ge2_64) + s_ge2_64
        if tot_56 < 47 or tot_64 < 55:
            raise RuntimeError("cross-phase Block (b) -> R3 count below bound")


verify_schedule_counts()


def run_trials(seeds, layout, mask_le):
    G, zs = LAYOUTS[layout]
    per = 256 // G
    zbits = sorted({(a ^ b).bit_length() - 1 for a, b in zip(zs, zs[1:])})
    results = []
    for c0 in range(0, len(seeds), per):
        chunk = seeds[c0:c0 + per]
        pres = [trial_prefixes(s, G) for s in chunk]
        slots = [p for ps in pres for p in ps]
        slots += [bytes(64)] * (256 - len(slots))
        batch = Batch(slots, zbits)
        state = [{"seen": {}, "first": None, "pairs": 0, "checks": 0} for _ in chunk]
        for t, z in enumerate(zs):
            if t:
                batch.flip((z ^ zs[t - 1]).bit_length() - 1)
            keys = batch.keys()
            pow2 = t > 0 and not t & (t - 1)
            done = set()
            for p in PROC:                  # processing order of the program
                ti, g = divmod(p, G)
                if ti >= len(chunk):
                    continue
                st = state[ti]
                key = keys[p]
                if st["checks"] < EXACT_CHECKS or (pow2 and ti not in done):
                    _check(pres[ti][g], z, key)
                    st["checks"] += 1
                    done.add(ti)
                k = key & mask_le           # equal masked keys <=> equal masked digests
                hit = st["seen"].get(k)
                if hit is None:
                    st["seen"][k] = [(g, z)]
                else:
                    st["pairs"] += len(hit)
                    if st["first"] is None:
                        st["first"] = (hit[0], (g, z))
                    hit.append((g, z))
        batch.check_o2p()
        for ti, st in enumerate(state):
            obs = {"masked_pairs": st["pairs"], "messages": G * len(zs), "exactness_checks": st["checks"],
                   "support_columns_checked": len(zbits), "o2p_rebuild_checked": 1,
                   "zstep_ops_64reg": 40802, "zstep_ops_56reg": 40890}
            if st["first"] is None:
                results.append((None, None, obs))
            else:
                (ga, za), (gb, zb) = st["first"]
                results.append((message(pres[ti][ga], za).hex(), message(pres[ti][gb], zb).hex(), obs))
    return results


def main():
    if len(sys.argv) == 5 and sys.argv[1] == "--local":
        layout, trials, seed = sys.argv[2], int(sys.argv[3]), sys.argv[4]
        mask = int.from_bytes(bytes.fromhex(MASKS[layout]), "little")
        seeds = [hashlib.sha256(("local-" + seed + "-" + str(t)).encode()).digest() for t in range(trials)]
        res = run_trials(seeds, layout, mask)
        succ = sum(1 for a, _, _ in res if a is not None)
        pairs = sum(o["masked_pairs"] for _, _, o in res)
        print(json.dumps({"layout": layout, "trials": trials, "successes": succ, "masked_pairs": pairs}))
        return
    request = json.load(sys.stdin)
    if request["schema_version"] != 1 or request["target_profile"] != "sha3-256-r6-prefix-v1":
        raise ValueError("unexpected organizer target")
    event = request["event"]
    if event.get("kind") != "digest-xor-mask" or int(event["expected_hex"], 16) != 0:
        raise ValueError("unexpected organizer event")
    layout = request["experiment_id"]
    if layout not in LAYOUTS:
        raise ValueError("unexpected experiment id")
    mask_le = int.from_bytes(bytes.fromhex(event["mask_hex"]), "little")
    items = request["trials"]
    res = run_trials([bytes.fromhex(it["seed"]) for it in items], layout, mask_le)
    rows = []
    for it, (a, b, obs) in zip(items, res):
        rows.append({"trial": it["trial"], "message_a_hex": a, "message_b_hex": b, "observations": obs})
    json.dump({"schema_version": 1, "trials": rows}, sys.stdout, separators=(",", ":"), sort_keys=True)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
