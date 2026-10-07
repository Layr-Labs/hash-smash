"""SHA3-r6 128-byte linear-prefix experiment; organizer execution pending.

Based directly on winglock 5e73af65, with material upstream credit in proof.md.
This derivative replaces the message family: 768 free bits in twelve lanes, two
neutral lanes 4 and 14, four dependent lanes. Padding is lane16=0x8000000000000006.
It maintains 975 read A2 words and patches 499 O2P words. A fixed492-word storage polarity is used. An explicit64-register hot-leaf
compiler and interpreter are embedded for organizer-only equivalence audits. The source counted program is absent. Our new hot-leaf generator charges
spills/reloads and is statically bounded at31378 operations; it has NOT executed.
An explicit cold ABI now saves/restores64 registers, decodes both128-byte
messages and charges at most256 ordinary operations plus2 selected permutations.
It is unexecuted, with dedicated and forced hot/cold checks declared below.

Every returned masked pair comes from the bitsliced evaluator. Independent
single-block sponge comparisons, support checks, A2/O2P rebuilds, dependency
cone poisoning, two transpose implementations and the tagged table checks
remain. The first batch checks all32 paired flips and rebuilds. Prefixes are
expanded deterministically from each organizer seed with three domain-separated
SHA256 calls; this is reproducibility, not evidence of full-scale independent
coins or a proof of the changed H1. Only organizer isolation may execute this
program. The conditional124.270 bound is an analytical claim; no execution result exists yet.
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

def swap_gray_coordinates(z):
    """Swap bits0/15; an involution, implemented by six ordinary operations."""
    a = ((z >> 15) ^ z) & 1
    return z ^ a ^ (a << 15)


def gray_z(t):
    return swap_gray_coordinates(t ^ (t >> 1))


GRAY_LEAF = tuple(15 if k == 0 else 0 if k == 15 else k for k in range(32))


LAYOUTS = {   # groups per trial, list of z in processing order
    "k6r6-bs-full-width": (256, [gray_z(t) for t in range(2)]),
    "k6r6-bs-spread": (16, [gray_z(t) for t in range(32)]),
    "k6r6-bs-single-group": (1, [gray_z(t) for t in range(512)]),
    "k6r6-bs-high-z": (4, [swap_gray_coordinates((t ^ (t >> 1)) << 25) for t in range(128)]),
}
# Kept last-round planes (counted program, proof.md Lemma 9); 4 x 35 = 140 digest bits.
KEEP = (0, 1, 2, 3, 4, 9, 10, 11, 16, 17, 18, 22, 23, 24, 25, 29, 30, 31, 32, 37, 38, 39, 40,
        44, 45, 46, 47, 51, 52, 53, 54, 58, 59, 60, 61)
NP = len(KEEP)
ROWOF = {(x, b): 4 * k + x for k, b in enumerate(KEEP) for x in range(4)}


def _mask_hex(bits):
    """18 digest bits (lane x, plane b) -> mask_hex (little-endian digest bytes)."""
    m = 0
    for x, b in bits:
        m |= 1 << (64 * x + b)
    return m.to_bytes(32, "little").hex()


MASKS = {
    "k6r6-bs-full-width": _mask_hex([(0, b) for b in (0, 1, 2, 3, 4)] + [(1, b) for b in (9, 10, 11, 16, 17)]
                                    + [(2, b) for b in (22, 23, 24, 25)] + [(3, b) for b in (29, 30, 31, 32)]),
    "k6r6-bs-spread": _mask_hex([(0, b) for b in (16, 17, 18, 22, 23)] + [(1, b) for b in (37, 38, 39, 40, 44)]
                                + [(2, b) for b in (44, 45, 46, 47)] + [(3, b) for b in (37, 38, 39, 40)]),
    "k6r6-bs-single-group": _mask_hex([(0, b) for b in (54, 58, 59, 60, 61)] + [(1, b) for b in (54, 58, 59, 60, 61)]
                                      + [(2, b) for b in (58, 59, 60, 61)] + [(3, b) for b in (58, 59, 60, 61)]),
    "k6r6-bs-high-z": _mask_hex([(0, b) for b in (29, 30, 31, 32, 37)] + [(1, b) for b in (44, 45, 46, 47, 51)]
                                + [(2, b) for b in (51, 52, 53, 54)] + [(3, b) for b in (0, 1, 2, 3)]),
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
    """LE32(z) XORed into bytes 32..35 and 112..115 (lanes 4 and 14)."""
    m = bytearray(prefix)
    for k in range(4):
        m[32 + k] ^= (z >> (8 * k)) & 0xFF
        m[112 + k] ^= (z >> (8 * k)) & 0xFF
    return bytes(m)


def _rotl64(v, r):
    r %= 64
    return ((v << r) | (v >> (64 - r))) & M64 if r else v


def structured_prefix(r768):
    """Inject 768 free bits into a 128-byte, rank-256 constrained prefix.

    The free lanes are 0,1,2,3,4,6,7,9,10,11,13,14. With PAD in lane16,
    C4 is unchanged by equal z in lanes4/14. D3=all-ones and L5=L15=D0;
    hence theta lanes5/15 are zero and lanes8/23 are all-ones. These are
    exactly the four chi neighbours needed to make round1 change only in
    the rho/pi images of lanes4/14.
    """
    L = [0] * 16
    for k, lane in enumerate((0,1,2,3,4,6,7,9,10,11,13,14)):
        L[lane] = (r768 >> (64*k)) & M64
    c4 = L[4] ^ L[9] ^ L[14]
    c1 = L[1] ^ L[6] ^ L[11] ^ 0x8000000000000006
    L[5] = L[15] = c4 ^ _rotl64(c1, 1)
    L[8] = 0
    L[12] = M64 ^ _rotl64(c4, 1) ^ L[2] ^ L[7]
    return b"".join(x.to_bytes(8, "little") for x in L)


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
BSP = {}      # source plane -> [(p, xs)]: outputs whose source word lies on that plane
for _Y in range(5):
    for _X in range(5):
        _xs, _ys = _pi_src(_X, _Y)
        _L = _xs + 5 * _ys
        for _b in range(64):
            _bs = (_b - RHO[_L]) % 64
            BSP.setdefault(_bs, []).append((len(SRC), _xs))
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
KEYMASK = 0              # stored key = key_of_digest(digest): kept bits moved to ROWOF, XOR KEYMASK
for (_x, _b), _r in ROWOF.items():
    KEYMASK |= ((LASTPLAN[_b][1] >> _x) & 1) << _r


def key_of_digest(d):
    """Stored key of a digest d (little-endian int): bit 64x + b -> row ROWOF[(x, b)], XOR KEYMASK."""
    k = 0
    for (x, b), r in ROWOF.items():
        k |= ((d >> (64 * x + b)) & 1) << r
    return k ^ KEYMASK


def key_mask_of(mask_le):
    """Digest mask -> key mask; every mask bit must be a kept digest bit."""
    km = 0
    for i in range(256):
        if (mask_le >> i) & 1:
            if (i >> 6, i & 63) not in ROWOF:
                raise ValueError("mask bit %d is not a kept digest bit" % i)
            km |= 1 << ROWOF[(i >> 6, i & 63)]
    return km

PLAN2 = chi_plan(0, P34, RC[1])
PLAN3 = chi_plan(Q3, P34, RC[2])
PLAN4 = chi_plan(Q3, P34, RC[3])
PLAN5 = chi_plan(Q3, P5, RC[4])


def chi(B, plan):
    return [B[a] ^ am ^ ((((B[b] ^ bm) | (B[c] ^ cm)) if g else ((B[b] ^ bm) & (B[c] ^ cm))) ^ om)
            for a, am, b, bm, c, cm, g, om in plan]


def round_ts(src, fix, fp_in, plan, start):
    """Round with theta'd input (plane fp_in lacking fix[x] unless fix is None),
    lane-complement chi, and the next round's D added before the store on every
    plane except this round's start plane `start` (stored raw, as the program's
    rotating plane schedule does); returns (stored state, fix words
    D_next[x][start])."""
    B = [src[s] for s in SRC]
    if fix is not None:
        for p, xs in BSP[fp_in]:
            B[p] ^= fix[xs]
    out = chi(B, plan)
    D = d_words(out)
    fix_out = [D[64 * x + start] for x in range(5)]
    for x in range(5):
        D[64 * x + start] = 0
    return [o ^ D[k] for o, k in zip(out, DCOL)], fix_out


def build_o2p(A2):
    out, fix = round_ts(A2, None, None, PLAN2, 0)
    for L in range(25):
        out[64 * L] ^= fix[L % 5]
    return out


def last_rows(S, fix):
    """Last round on the kept planes only; rows not in ROWOF stay 0."""
    rows = [0] * 256
    for b in KEEP:
        B = []
        for X in range(5):
            L = DIAG[X]
            bs = (b - RHO[L]) % 64
            B.append(S[64 * L + bs] ^ (fix[X] if bs == STARTS[2] else 0))
        (_, Sset, plan), _ = LASTPLAN[b]
        for x in range(4):
            ca, cb, cc, gate, on = plan[x]
            a = B[x] ^ (W if ca else 0)
            u = B[(x + 1) % 5] ^ (W if cb else 0)
            v = B[(x + 2) % 5] ^ (W if cc else 0)
            rows[ROWOF[(x, b)]] = a ^ ((u | v) if gate == "or" else (u & v)) ^ (W if on else 0)
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
STEP_ORDER = (1, 2, 4, 8, 16, 32, 64, 128)   # reference order of the full transpose; stages commute


def _par(r):
    return bin(r).count("1") & 1


def _rotl(x, n):
    n %= 256
    return ((x << n) | (x >> (256 - n))) & W if n else x


def _rot_cost(za, zb, ib):
    if za and zb:
        return 0
    if not za and not zb:
        return 5
    return 2 if (za if _par(ib) == 0 else zb) else 3


def _best_order(zero, rows, bits):
    """Cheapest stage order given the statically zero rows (as the program)."""
    best = None
    for order in itertools.permutations(bits):
        z = dict(zero); c = 0
        for d in order:
            for r in rows:
                if r & d:
                    continue
                c += _rot_cost(z[r], z[r | d], r | d)
                if z[r] != z[r | d]:
                    z[r] = z[r | d] = False
        if best is None or (c, order) < best:
            best = (c, order)
    return best[1]


KEYROWS = frozenset(ROWOF.values())
BLOCKS = sorted({r >> 5 for r in KEYROWS})
P1ORDER = {g: _best_order({32 * g + q: (32 * g + q) not in KEYROWS for q in range(32)},
                          [32 * g + q for q in range(32)], (1, 2, 4, 8, 16)) for g in BLOCKS}
P2ORDER = {gi: _best_order({32 * i + gi: i not in BLOCKS for i in range(8)},
                           [32 * i + gi for i in range(8)], (32, 64, 128)) for gi in range(32)}


def transpose_z(rows):
    """Lemma 9 (v4): the program's rotating-frame delta swaps with statically
    zero rows.  Row r is held in a frame: physical bit q is logical bit
    (q + OFF[r]) mod 256.  In a stage d the even-parity row of a pair stays in
    frame 0 and the odd-parity row is rotated into its frame (a zero row needs
    no rotation); cost 5 per pair, 2 if the moving row is zero, 3 if the other
    row is zero, 0 if both are.  Phase 1: stages 1,2,4,8,16 in each block
    with a key row; phase 2: stages 32,64,128 on rows 32i + gi; then one
    rotation per row not in frame 0.  Returns (rows, ops)."""
    R, Z, OFF, ops = list(rows), [r not in KEYROWS for r in range(256)], [0] * 256, 0

    def swap(ia, ib, d):
        nonlocal ops
        za, zb = Z[ia], Z[ib]
        if za and zb:
            return
        ops += _rot_cost(za, zb, ib)
        if _par(ib) == 0:                          # b even: a moves
            u = 0 if za else _rotl(R[ia], OFF[ia] - d)
            t = (u ^ R[ib]) & MASKD[d]
            R[ib] ^= t; R[ia] = u ^ t; OFF[ia] = d % 256
        else:                                      # a even: b moves
            v = 0 if zb else _rotl(R[ib], OFF[ib] + d)
            t = (R[ia] ^ v) & (W ^ MASKD[d])
            R[ia] ^= t; R[ib] = v ^ t; OFF[ib] = (-d) % 256
        Z[ia] = Z[ib] = False
    for g in BLOCKS:
        for d in P1ORDER[g]:
            for q in range(32):
                r = 32 * g + q
                if not r & d:
                    swap(r, r + d, d)
    for gi in range(32):
        for d in P2ORDER[gi]:
            for i in range(8):
                r = 32 * i + gi
                if not r & d:
                    swap(r, r + d, d)
    for r in range(256):
        if OFF[r]:
            R[r] = _rotl(R[r], OFF[r]); ops += 1
    return R, ops


def decode_slot(q):
    """Processing index q (0..255) of a z-step -> group slot (bit position)."""
    return 32 * (q & 7) + (q >> 3)


PROC = [decode_slot(q) for q in range(256)]
assert sorted(PROC) == list(range(256))
assert transpose_z([0] * 256)[1] == 3418   # Lemma 9 / ledger: 1,770 + 1,520 + 128 frame fixes


# ---------------- linear-structure support and incremental round 2 ----------
def _dst(L, b):
    """A2 word (lane L, bit b) -> round-2 chi position (X, Y, plane)."""
    x, y = L % 5, L // 5
    return y, (2 * x + 3 * y) % 5, (b + RHO[L]) % 64


def support(j):
    """Lemma 3: the 22 A2 words flipped (by all-ones, in every group) by z-bit j:
    the two round-1 chi outputs carrying z and the 4 x 5 words of the round-2
    D columns they change."""
    S = set()
    for L in (4, 14):
        X, Y, p = _dst(L, j)
        S.add((X + 5 * Y, p))
    for L, b in list(S):
        for xx, bb in (((L % 5 + 1) % 5, b), ((L % 5 - 1) % 5, (b + 1) % 64)):
            for y in range(5):
                S ^= {(xx + 5 * y, bb)}
    return sorted(S)


SUPPORT = [support(j) for j in range(32)]
assert all(len(s) == 22 for s in SUPPORT)
WT = -1      # the all-ones term of a patch expression


def patch_exprs(j):
    """Lemma 6: O2P word -> set of terms (A2 word indices of the NEW A2, WT)
    whose XOR is the change of that O2P word when z-bit j flips."""
    S = SUPPORT[j]
    flips = {64 * L + b for L, b in S}
    rows = {}
    for L, b in S:
        X, Y, p = _dst(L, b)
        rows.setdefault((Y, p), set()).add(X)
    dout = {}
    for (Y, p), Xs in rows.items():
        c = [1 if X in Xs else 0 for X in range(5)]
        for k in range(5):
            k1, k2 = (k + 1) % 5, (k + 2) % 5
            e = set()
            if c[k] ^ c[k2] ^ (c[k1] & c[k2]):
                e ^= {WT}
            if c[k2]:
                L_, b_ = _bsrc(k1, Y, p)
                e ^= {64 * L_ + b_}
            if c[k1]:
                L_, b_ = _bsrc(k2, Y, p)
                e ^= {64 * L_ + b_}
            if e:
                dout[(k, Y, p)] = frozenset(e)
    dC = {}
    for (x, Y, b), v in dout.items():
        dC[(x, b)] = dC.get((x, b), frozenset()) ^ v
    patch = {64 * (x + 5 * Y) + b: v for (x, Y, b), v in dout.items()}
    for (x, b), v in dC.items():
        for xx, bb in (((x + 1) % 5, b), ((x - 1) % 5, (b + 1) % 64)):
            for Y in range(5):
                w = 64 * (xx + 5 * Y) + bb
                patch[w] = patch.get(w, frozenset()) ^ v
    out = {}
    for w, v in patch.items():
        v = set(v)
        for t in list(v):
            if t != WT and t in flips:     # read after the flip: old = new ^ all-ones
                v ^= {WT}
        if v:
            out[w] = frozenset(v)
    return out


PATCH = [patch_exprs(j) for j in range(32)]
READS = frozenset(t for pe in PATCH for e in pe.values() for t in e if t != WT)
# The program flips only support words that some patch expression reads, and
# stores A2 word i complemented iff i is in PI (a compile-time storage polarity
# chosen to minimise NOTs); every patch term is read in that encoding.
FLIPS = [sorted({64 * L + b for L, b in SUPPORT[j]} & READS) for j in range(32)]
PI = frozenset(i for i in range(1600) if (int.from_bytes(bytes.fromhex("5172f5dfeb4f1b05000000000000000044010000231b433b001a39db5ddf0f0040000080010000005a95ffff3b2305000000000000000000f8fc6f5781202aa600303da862090000fb1c00000000f6bee17d77bfffbb4b4400000000000000009600feb75d8184020070d14eff060000725e624042b07d6adf7735260faa48aadd704e000000008f0300271b432380980000e07dd7731200c1002400000000d60098eef75d8d7d000400944d00000000c084202210001100ab45cf2d00000000d42f000000000049"), "little") >> i) & 1)
PATCHP = []
for _pe in PATCH:
    _q = {}
    for _w, _e in _pe.items():
        _e = set(_e)
        for _t in list(_e):
            if _t != WT and _t in PI:
                _e ^= {WT}
        if _e:
            _q[_w] = (sorted(t for t in _e if t != WT), W if WT in _e else 0)
    PATCHP.append(sorted(_q.items()))
assert (len(READS), len(PI), sorted({len(p) for p in PATCHP}), sorted({len(f) for f in FLIPS})) == \
    (975, 492, [499], [3, 4, 5, 6, 7, 8, 9, 10])


def incr_round2(A2S, O2P, j):
    """Flip the read support words of A2 (stored with polarity PI), then patch
    O2P with the exact round-2 output change of Lemma 6 (all terms read from
    the new A2; theta of round 3 included)."""
    for w in FLIPS[j]:
        A2S[w] ^= W
    for w, (ts, c) in PATCHP[j]:
        v = c
        for t in ts:
            v ^= A2S[t]
        O2P[w] ^= v


# ---- Explicit physical instruction generator, organizer-only execution ----
from collections import Counter, defaultdict, deque
from functools import lru_cache

def _ir_q(p):
    columns = [sum((p >> (x+5*y)) & 1 for y in range(5)) % 2 for x in range(5)]
    return tuple(((p >> l) & 1) ^ columns[(l%5-1)%5] ^ columns[(l%5+1)%5] for l in range(25))

class IRG:
    P34 = P34
    P5 = P5
    RC = RC
    KEEP = KEEP
    input_address = staticmethod(_bsrc)
    polarity_after_theta = staticmethod(_ir_q)

@lru_cache(None)
def ir_plan(q, p, outs, iota):
    best = None
    for copies in range(32):
        row = []
        cost = copies.bit_count()
        for x in outs:
            choices = []
            for ca, cb, cc in itertools.product((0, 1), repeat=3):
                ids = (x, (x + 1) % 5, (x + 2) % 5)
                if any((c and (not copies >> i & 1) for c, i in zip((ca, cb, cc), ids))):
                    continue
                a, b, c = (q[i] ^ v for i, v in zip(ids, (ca, cb, cc)))
                if (b, c) == (1, 0):
                    op, pol = ('AND', 0)
                elif (b, c) == (0, 1):
                    op, pol = ('OR', 1)
                else:
                    continue
                inv = a ^ pol ^ p[x] ^ (iota if x == 0 else 0)
                choices.append((inv, ca, cb, cc, op))
            if not choices:
                cost = 999
                break
            choice = min(choices)
            cost += choice[0]
            row.append((x, choice))
        result = (cost, copies, tuple(row))
        if best is None or result[0] < best[0]:
            best = result
    return best

def ir_dependencies(stores, fixes, start):
    ds = {(l % 5, b) for l, b in stores if b != start} | {(x, start) for x in fixes}
    ps = {key for x, b in ds for key in (((x - 1) % 5, b), ((x + 1) % 5, (b - 1) % 64))}
    outs = set(stores) | {(x + 5 * y, b) for x, b in ps for y in range(5)}
    ins = {IRG.input_address((l % 5 + dx) % 5, l // 5, b) for l, b in outs for dx in range(3)}
    return (ds, ps, outs, ins)

class IRSSA:

    def __init__(self):
        self.code = []
        self.seq = 0
        self.section = ''

    def emit(self, op, args=(), addr=None):
        dst = None if op == 'STORE' else self.seq
        if dst is not None:
            self.seq += 1
        self.code.append((op, dst, tuple(args), addr, self.section))
        return dst

    def load(self, addr):
        return self.emit('LOAD', addr=addr)

    def store(self, addr, v):
        self.emit('STORE', (v,), addr)

    def xor(self, a, b):
        return self.emit('XOR', (a, b))

    def reduce(self, vals):
        v = vals[0]
        for w in vals[1:]:
            v = self.xor(v, w)
        return v

def ir_emit_round(s, ri, stores, fixes, start, previous_start, pout, oldfix, order=(0, 1, 2, 3, 4), save_first=False, save_fix=False):
    s.section = f'R{ri}'
    ds, ps, outs, ins = ir_dependencies(stores, fixes, start)
    qr = IRG.polarity_after_theta(IRG.P34)
    chi = {}
    par = {}
    outfix = {}
    for off in range(64):
        b = (start + off) % 64
        for y in order:
            xs = tuple((x for x in range(5) if (x + 5 * y, b) in outs))
            if not xs:
                continue
            q = tuple((qr[IRG.input_address(x, y, 0)[0]] for x in range(5)))
            p = tuple((pout >> x + 5 * y & 1 for x in range(5)))
            _, copies, plans = ir_plan(q, p, xs, IRG.RC[ri - 1] >> b & 1 if y == 0 else 0)
            needed = {x for out in xs for x in (out, (out + 1) % 5, (out + 2) % 5)}
            vals = {}
            for x in sorted(needed):
                l, k = IRG.input_address(x, y, b)
                v = s.load((f'O{ri - 1}', l, k))
                if k == previous_start:
                    fix = s.load((f'F{ri - 1}', l % 5)) if save_fix else oldfix[l % 5]
                    v = s.xor(v, fix)
                vals[x, 0] = v
                if copies >> x & 1:
                    vals[x, 1] = s.emit('NOT', (v,))
            for x, (inv, ca, cb, cc, op) in plans:
                gate = s.emit(op, (vals[(x + 1) % 5, cb], vals[(x + 2) % 5, cc]))
                v = s.xor(vals[x, ca], gate)
                if inv:
                    v = s.emit('NOT', (v,))
                chi[x + 5 * y, b] = v
        for x in range(5):
            if (x, b) in ps:
                par[x, b] = s.reduce([chi[x + 5 * y, b] for y in range(5)])
        if off == 0:
            if save_first:
                for x in fixes:
                    s.store((f'C{ri}', (x - 1) % 5), par[(x - 1) % 5, start])
            for l in range(25):
                if (l, b) in stores:
                    s.store((f'O{ri}', l, b), chi[l, b])
        else:
            for x in range(5):
                if (x, b) not in ds:
                    continue
                d = s.xor(par[(x - 1) % 5, b], par[(x + 1) % 5, (b - 1) % 64])
                for y in range(5):
                    l = x + 5 * y
                    if (l, b) in stores:
                        s.store((f'O{ri}', l, b), s.xor(chi[l, b], d))
    for x in sorted(fixes):
        first = s.load((f'C{ri}', (x - 1) % 5)) if save_first else par[(x - 1) % 5, start]
        outfix[x] = s.xor(first, par[(x + 1) % 5, (start - 1) % 64])
        if save_fix:
            s.store((f'F{ri}', x), outfix[x])
    return outfix

def ir_generate(save_first=False, save_fix=False):
    need5 = {IRG.input_address(x, 0, b) for b in IRG.KEEP for x in range(5)}
    ds, ps, out, need4 = ir_dependencies(need5, set(), 34)
    fix4 = {l % 5 for l, b in need4 if b == 39}
    ds, ps, out, need3 = ir_dependencies(need4, fix4, 39)
    fix3 = {l % 5 for l, b in need3 if b == 2}
    s = IRSSA()
    f3 = ir_emit_round(s, 3, need3, fix3, 2, None, IRG.P34, {}, save_first=save_first, save_fix=save_fix)
    f4 = ir_emit_round(s, 4, need4, fix4, 39, 2, IRG.P34, f3, save_first=save_first, save_fix=save_fix)
    ir_emit_round(s, 5, need5, set(), 34, 39, IRG.P5, f4, save_first=save_first, save_fix=save_fix)
    return s.code

class IRR:
    SSA = IRSSA
    generate = staticmethod(ir_generate)
    plan = staticmethod(ir_plan)
    g = IRG

def ir_normalized(j,pi=frozenset()):
    # PATCH already uses new-A2 variables. Convert its all-ones token and
    # apply this program's immutable A2 storage polarity.
    out = {}
    for w,form in PATCH[j].items():
        p = {1600 if t == WT else t for t in form}
        if len((p-{1600}) & pi) % 2:
            p.symmetric_difference_update((1600,))
        out[divmod(w,64)] = frozenset(p)
    return set(FLIPS[j]),out

def ir_fused(j, pi=frozenset(), full=False):
    s = IRR.SSA()
    s.section = 'INC'
    flips, patch = ir_normalized(j, pi)
    for w in sorted(flips):
        a = ('A2', w)
        v = s.load(a)
        v = s.emit('NOT', (v,))
        s.store(a, v)
    defs = {}
    one = frozenset((1600,))
    unsigned = {p - one for p in patch.values() if p - one}

    def expr(p):
        if p in defs:
            return defs[p]
        if p & one:
            v = s.emit('NOT', (expr(p - one),))
        elif len(p) == 1:
            v = s.load(('A2', next(iter(p))))
        else:
            proper = sorted((x for x in unsigned if x < p), key=lambda x: (-len(x), tuple(sorted(x))))
            a = proper[0] if proper else frozenset((min(p),))
            v = s.xor(expr(a), expr(p - a))
        defs[p] = v
        return v
    raw = IRR.generate(True, False)
    mapping = {}
    for op, dst, args, addr, sec in raw:
        if sec != 'R3' and (not full):
            break
        args = tuple((mapping[x] for x in args))
        s.section = sec
        if sec == 'R3' and op == 'LOAD' and (addr[0] == 'O2') and (addr[1:] in patch):
            p = patch[addr[1:]]
            s.section = 'INC'
            delta = expr(p) if p != one else None
            old = s.load(addr)
            v = s.emit('NOT', (old,)) if p == one else s.xor(old, delta)
            s.store(addr, v)
            mapping[dst] = v
        else:
            v = s.emit(op, args, addr)
            if dst is not None:
                mapping[dst] = v
    used = {x for op, dst, args, addr, sec in raw if sec != 'R3' for x in args if x in mapping}
    s.section = 'R3'
    if not full:
        for x in sorted(used):
            s.store(('FIXOUT', x), mapping[x])
    return (s.code, {'flips': len(flips), 'patches': len(patch), 'affine_nodes': len(defs)})

def ir_allocate(code, registers=64):
    """Offline next-use allocator; charge every spill store and reload.
    Direct LOAD values and explicitly STOREd values have known RAM backing.
    Any overwritten backing is invalidated. This is instruction generation,
    not an interpreter. Two physical registers are reserved for outer state.
    """
    uses = defaultdict(deque)
    for i, (_, _, args, _, _) in enumerate(code):
        for v in set(args):
            uses[v].append(i)
    free = list(range(2, registers))
    loc = {}
    home = {}
    ataddr = defaultdict(set)
    physical = []
    spills = loads = 0
    peak = 2

    def ins(op, dst, args, addr, sec, why='program'):
        physical.append((op, dst, args, addr, sec, why))

    def bind(v, a):
        if v in home:
            ataddr[home[v]].discard(v)
        home[v] = a
        ataddr[a].add(v)

    def vacant(pinned, sec):
        nonlocal spills
        if free:
            return free.pop()
        candidates = [v for v in loc if v not in pinned]
        assert candidates, 'operation requires too many simultaneous operands'
        v = max(candidates, key=lambda v: (uses[v][0] if uses[v] else 10 ** 30, v in home))
        reg = loc.pop(v)
        if uses[v] and v not in home:
            a = ('SPILL', v)
            bind(v, a)
            ins('STORE', None, (reg,), a, sec, 'spill')
            spills += 1
        return reg
    for i, (op, dst, args, addr, sec) in enumerate(code):
        for v in set(args):
            if v not in loc:
                assert v in home, ('undefined', v, i)
                reg = vacant(set(args), sec)
                loc[v] = reg
                ins('LOAD', reg, (), home[v], sec, 'reload')
                loads += 1
        ar = tuple((loc[v] for v in args))
        for v in set(args):
            assert uses[v][0] == i
            uses[v].popleft()
            if not uses[v]:
                free.append(loc.pop(v))
        rd = None
        if dst is not None:
            rd = vacant(set(), sec)
            loc[dst] = rd
        ins(op, rd, ar, addr, sec)
        if op == 'LOAD':
            bind(dst, addr)
        elif op == 'STORE':
            for v in list(ataddr[addr]):
                if v != args[0]:
                    del home[v]
                    ataddr[addr].remove(v)
            bind(args[0], addr)
        peak = max(peak, len(loc) + 2)
        if dst is not None and (not uses[dst]):
            free.append(loc.pop(dst))
    assert not loc
    counts = Counter((op for op, _, _, _, _, _ in physical))
    secs = Counter((sec for _, _, _, _, sec, _ in physical))
    return (physical, {'instructions': len(physical), 'peak': peak, 'spill_stores': spills, 'reloads': loads, 'opcodes': dict(counts), 'sections': dict(secs)})

def ir_simplify(code):
    """Exact SSA involution simplification and dead pure-instruction removal."""
    defs = {}
    alias = {}
    new = []

    def resolve(v):
        while v in alias:
            v = alias[v]
        return v
    for op, dst, args, addr, sec in code:
        args = tuple((resolve(v) for v in args))
        if op == 'NOT' and args[0] in defs and (defs[args[0]][0] == 'NOT'):
            alias[dst] = resolve(defs[args[0]][1][0])
            continue
        new.append((op, dst, args, addr, sec))
        if dst is not None:
            defs[dst] = (op, args)
    live = set()
    result = []
    for op, dst, args, addr, sec in reversed(new):
        if op in ('STORE', 'STOREIND_C', 'BRANCH', 'CINC') or dst in live:
            live.update(args)
            result.append((op, dst, args, addr, sec))
    return list(reversed(result))

def ir_memory_ssa(code):
    """Alias repeated reads to the last stored/read SSA value. Allocation
    subsequently retains it or emits charged reloads from its RAM backing."""
    known = {}
    alias = {}
    out = []

    def resolve(v):
        while v in alias:
            v = alias[v]
        return v
    for op, dst, args, addr, sec in code:
        args = tuple((resolve(v) for v in args))
        if op == 'LOAD' and addr in known:
            alias[dst] = resolve(known[addr])
            continue
        if op == 'LOAD':
            known[addr] = dst
        if op == 'STORE':
            known[addr] = args[0]
        out.append((op, dst, args, addr, sec))
    return out

def ir_remove_unused_scratch_stores(physical, spaces=('O3', 'O4', 'C3', 'C4', 'SPILL')):
    read = {addr for op, _, _, addr, _, _ in physical if op == 'LOAD'}
    out = [i for i in physical if not (i[0] == 'STORE' and i[3][0] in spaces and (i[3] not in read))]
    return out

class IRF:
    r = IRR

class IRBuilder(IRF.r.SSA):

    def emit(self, op, args=(), addr=None):
        dst = None if op in ('STORE', 'STOREIND_C', 'BRANCH', 'CINC') else self.seq
        if dst is not None:
            self.seq += 1
        self.code.append((op, dst, tuple(args), addr, self.section))
        return dst

@lru_cache(None)
def ir_order(indices, live, bits):
    best = None
    for seq in itertools.permutations(bits):
        nz = set(live)
        cost = 0
        for d in seq:
            for a in indices:
                if a & d:
                    continue
                b = a + d
                if a not in nz and b not in nz:
                    continue
                mover = a if b.bit_count() % 2 == 0 else b
                stayer = b if mover == a else a
                cost += 5 if mover in nz and stayer in nz else 3 if mover in nz else 2
                nz.update((a, b))
        choice = (cost, seq)
        if best is None or choice < best:
            best = choice
    return best

@lru_cache(None)
def ir_last_plan(b):
    q = tuple((IRG.polarity_after_theta(IRG.P5)[IRG.input_address(x, 0, 0)[0]] for x in range(5)))
    best = None
    for pbits in range(16):
        p = tuple((pbits >> x & 1 for x in range(5)))
        p0 = IRF.r.plan(q, p, (0, 1, 2, 3), IRG.RC[5] >> b & 1)
        if best is None or p0[0] < best[0][0]:
            best = (p0, pbits)
    assert best[0][0] == 0
    return best

def ir_swaps(s, rows, off, indices, bits):
    _, seq = ir_order(tuple(indices), tuple(sorted((k for k, v in rows.items() if v is not None))), tuple(bits))
    for d in seq:
        masks = {}
        for a in indices:
            if a & d:
                continue
            b = a + d
            if rows[a] is None and rows[b] is None:
                continue
            mover = a if b.bit_count() % 2 == 0 else b
            stayer = b if mover == a else a
            target = d if mover == a else -d
            pol = 0 if mover == a else 1
            if pol not in masks:
                masks[pol] = s.load(('MASK', d, pol))
            u = rows[mover]
            v = rows[stayer]
            if u is not None:
                u = s.emit('ROT', (u,), (off[mover] - target) % 256)
            off[mover] = target % 256
            if u is None:
                t = s.emit('AND', (v, masks[pol]))
                rows[mover] = t
                rows[stayer] = s.xor(v, t)
            elif v is None:
                t = s.emit('AND', (u, masks[pol]))
                rows[stayer] = t
                rows[mover] = s.xor(u, t)
            else:
                t = s.emit('AND', (s.xor(u, v), masks[pol]))
                rows[mover] = s.xor(u, t)
                rows[stayer] = s.xor(v, t)

def ir_append_last(raw):
    s = IRBuilder()
    s.seq = max((d for _, d, _, _, _ in raw if d is not None)) + 1
    inserts = {}
    finaloff = {}
    ready = {}
    write = {a: i for i, (op, _, _, a, _) in enumerate(raw) if op == 'STORE'}
    for group in range(5):
        planes = list(enumerate(IRG.KEEP))[8 * group:8 * group + 8]
        needed = {('O5',) + IRG.input_address(x, 0, b) for _, b in planes for x in range(5)}
        after = max((write[a] for a in needed))
        ready[group] = after
        s.code = []
        s.section = 'LAST1'
        indices = list(range(32 * group, 32 * group + 32))
        rows = {i: None for i in indices}
        off = {i: 0 for i in indices}
        for k, b in planes:
            (_, copies, plans), _ = ir_last_plan(b)
            assert copies == 0
            inp = [s.load(('O5',) + IRG.input_address(x, 0, b)) for x in range(5)]
            for x, (inv, ca, cb, cc, op) in plans:
                assert inv == ca == cb == cc == 0
                rows[4 * k + x] = s.xor(inp[x], s.emit(op, (inp[(x + 1) % 5], inp[(x + 2) % 5])))
        ir_swaps(s, rows, off, indices, (1, 2, 4, 8, 16))
        for i in indices:
            s.store(('ROWS', i), rows[i])
        finaloff.update(off)
        inserts.setdefault(after, []).extend(s.code)
    joined = []
    for i, item in enumerate(raw):
        joined.append(item)
        if i in inserts:
            joined.extend(inserts[i])
    s.code = []
    s.section = 'LAST2'
    for gi in range(32):
        indices = [32 * i + gi for i in range(8)]
        rows = {i: s.load(('ROWS', i)) if i // 32 < 5 else None for i in indices}
        off = {i: finaloff.get(i, 0) for i in indices}
        ir_swaps(s, rows, off, indices, (32, 64, 128))
        for i in indices:
            key = rows[i]
            if off[i]:
                key = s.emit('ROT', (key,), off[i])
            w = s.emit('LOADIND', (key,))
            x = s.emit('XORC', (w,))
            flag = s.emit('CMPIMM', (x,), 1 << 128)
            s.emit('BRANCH', (flag, w), 'COLD')
            s.emit('STOREIND_C', (key,))
            s.emit('CINC', (), 1)
    joined.extend(s.code)
    return (joined, {'block_ready_indices': ready, 'keymask': sum(((ir_last_plan(b)[1] >> x & 1) << 4 * k + x for k, b in enumerate(IRG.KEEP) for x in range(4)))})

def compile_hot_leaf(j):
    raw,_ = ir_fused(j,PI,True)
    raw,info = ir_append_last(raw)
    if info['keymask'] != KEYMASK:
        raise RuntimeError("IR last-round polarity differs from key encoding")
    raw = ir_simplify(ir_memory_ssa(raw))
    physical,stats = ir_allocate(raw)
    physical = ir_remove_unused_scratch_stores(physical,('O3','O4','O5','C3','C4','ROWS','SPILL'))
    if len(physical)+18 != IR_HOT_COUNTS[j] or stats['peak'] > 64:
        raise RuntimeError("generated hot leaf differs from static register/cost audit")
    return physical


def execute_hot_leaf(program,old_a2,old_o2):
    """Organizer-only hot interpreter, including a forced garbage cold call.
    Its synthetic cold prefix memory is separate from the batch's mathematical
    state; audit_cold independently checks real prefix decoding. Every taken
    branch preserves all64 hot registers before continuing the instruction.
    """
    regs=[W]*64;regs[0]=0;regs[1]=1<<128
    mem={('A2',i):v for i,v in enumerate(old_a2) if i in READS}
    mem.update({('O2',i//64,i%64):v for i,v in enumerate(old_o2)})
    for d in MASKD:
        mem['MASK',d,0]=MASKD[d];mem['MASK',d,1]=W^MASKD[d]
    table={};keys=[];cold=0;first_lookup=True
    coldmem={('VCNT',):0}
    for hot_pc,(op,dst,args,addr,section,why) in enumerate(program):
        a=regs[args[0]] if args else 0
        b=regs[args[1]] if len(args)>1 else 0
        if op=='LOAD':v=mem[addr]
        elif op=='STORE':mem[addr]=a;continue
        elif op=='XOR':v=a^b
        elif op=='AND':v=a&b
        elif op=='OR':v=a|b
        elif op=='NOT':v=a^W
        elif op=='ROT':v=_rotl(a,addr)
        elif op=='LOADIND':
            if not 0<=a<1<<140:raise RuntimeError("IR key outside table")
            v=table.get(a,(1<<128)|((1<<127)+256) if first_lookup else 0)
            first_lookup=False
        elif op=='XORC':v=a^regs[1]
        elif op=='CMPIMM':v=int(a<addr)
        elif op=='BRANCH':
            if a:
                saved=list(regs)
                result,ops,perms,_=execute_cold(regs,args[1],coldmem,hot_pc+1)
                if result!='CONTINUE' or saved!=regs or ops>256 or perms>2:
                    raise RuntimeError("hot/cold calling convention failed")
                cold+=1
            continue
        elif op=='STOREIND_C':table[a]=regs[1];keys.append(a);continue
        elif op=='CINC':regs[1]=(regs[1]+1)&W;continue
        else:raise RuntimeError("unknown physical opcode")
        regs[dst]=v
    if len(keys)!=256 or cold<1:raise RuntimeError("IR table/cold count mismatch")
    return mem,keys,cold


# Cold ABI: each branch-site clone fixes both raw-word register and literal
# continuation address; no implicit link register or free return. All64 hot
# registers are saved/restored. Arguments below are register numbers, never
# free host arithmetic inside the charged stream.
PREF_BASE = 1 << 140
COLD_CAP = ((255 << 120)**2 >> 141) + ((255 << 120)**2 >> 148) + (1 << 91) + (1 << 61)


def compile_cold(rawreg,return_site=0):
    code=[]
    def e(op,dst=None,args=(),imm=None):code.append((op,dst,tuple(args),imm))
    for r in range(64):e('STORE',args=(r,),imm=('SAVE',r))
    e('LOAD',2,imm=('SAVE',rawreg));e('LOAD',3,imm=('SAVE',1))
    e('LOAD',24,imm=('VCNT',));e('ADDI',24,(24,),1)
    e('STORE',args=(24,),imm=('VCNT',));e('GT',24,(24,),COLD_CAP);e('BRANCH',args=(24,),imm='ABORT')
    for raw,out in ((2,8),(3,16)):
        e('ANDI',raw,(raw,),(1<<128)-1)
        e('SHR',4,(raw,),40);e('SHR',5,(raw,),8);e('ANDI',5,(5,),(1<<32)-1)
        e('ANDI',6,(raw,),255);e('ANDI',7,(6,),7);e('SHL',7,(7,),5);e('SHR',6,(6,),3);e('OR',7,(7,6))
        e('SHR',6,(5,),1);e('XOR',5,(5,6))
        e('SHR',6,(5,),15);e('XOR',6,(6,5));e('ANDI',6,(6,),1)
        e('XOR',5,(5,6));e('SHL',6,(6,),15);e('XOR',5,(5,6))
        e('SHL',4,(4,),10);e('SHL',7,(7,),2);e('ADD',4,(4,7));e('ADDI',4,(4,),PREF_BASE)
        for k in range(4):
            if k:e('ADDI',4,(4,),1)
            e('LOADIND',out+k,(4,))
        e('XOR',out+1,(out+1,5));e('SHL',5,(5,),128);e('XOR',out+3,(out+3,5))
    e('XOR',24,(8,16))
    for a,b in ((9,17),(10,18),(11,19)):e('XOR',25,(a,b));e('OR',24,(24,25))
    e('EQ',24,(24,),0);e('BRANCH',args=(24,),imm='RESTORE')
    for out in (8,16):
        e('CONST',out+4,imm=0x8000000000000006);e('CONST',out+5,imm=0);e('CONST',out+6,imm=0)
        e('PERM',args=tuple(range(out,out+7)))
    e('XOR',24,(8,16));e('EQ',24,(24,),0);e('BRANCH',args=(24,),imm='HIT')
    restore=len(code)
    for r in range(64):e('LOAD',r,imm=('SAVE',r))
    e('RETURN',imm=return_site)
    assert len(code)==218 and sum(op=='PERM' for op,_,_,_ in code)==2
    return code,restore


def execute_cold(regs,rawreg,memory,return_site=0):
    """Organizer-only physical cold interpreter. PERM is exactly the selected
    one-block,6-round permutation; for diagnostics its low256 output is read
    through the independent sponge. Unused permutation outputs are poisoned.
    Debug message snapshots are not algorithmic work or evidence of free copies.
    A HIT is charged separately for re-decoding both ids and eight output stores.
    """
    code,restore=compile_cold(rawreg,return_site);pc=0;ordinary=perms=0;messages=[]
    while pc<len(code):
        op,dst,args,imm=code[pc];pc+=1
        a=regs[args[0]] if args else 0;b=regs[args[1]] if len(args)>1 else 0
        if op=='PERM':
            if [regs[r] for r in args[4:]] != [0x8000000000000006,0,0]:raise RuntimeError('cold padding')
            msg=b''.join(regs[r].to_bytes(32,'little') for r in args[:4]);messages.append(msg)
            digest=int.from_bytes(sponge6(msg),'little');perms+=1
            for r in args:regs[r]=W
            regs[args[0]]=digest;continue
        ordinary+=1
        if op=='LOAD':v=memory[imm]
        elif op=='STORE':memory[imm]=a;continue
        elif op=='LOADIND':v=memory.get(a,0)
        elif op=='CONST':v=imm
        elif op=='ADDI':v=(a+imm)&W
        elif op=='ADD':v=(a+b)&W
        elif op=='ANDI':v=a&imm
        elif op=='SHR':v=a>>imm
        elif op=='SHL':v=(a<<imm)&W
        elif op=='OR':v=a|b
        elif op=='XOR':v=a^b
        elif op=='EQ':v=int(a==imm)
        elif op=='GT':v=int(a>imm)
        elif op=='BRANCH':
            if a:
                if imm=='RESTORE':pc=restore
                else:return imm,ordinary+(70 if imm=='HIT' else 0),perms,messages
            continue
        elif op=='RETURN':
            if imm!=return_site:raise RuntimeError('cold continuation mismatch')
            return 'CONTINUE',ordinary,perms,messages
        else:raise RuntimeError('cold opcode')
        regs[dst]=v
    raise RuntimeError('cold did not return')


def audit_cold(prefixes):
    mem={('VCNT',):0}
    for p,prefix in enumerate(prefixes):
        for k in range(4):mem[PREF_BASE+4*p+k]=int.from_bytes(prefix[32*k:32*k+32],'little')
    # Current, equal, distinct, out-of-generation and maximal-width raw ids.
    for old,new in ((0,0),(0,256),(255,(1<<40)|31),((1<<128)-1,0),
                    ((1<<15)<<8,((1<<15)-1)<<8),((1<<16)<<8,((1<<16)-1)<<8)):
        regs=[(k+1)*0x123456789abcdef for k in range(64)]
        regs[1]=(7<<128)|new;regs[37]=(7<<128)|old;saved=list(regs)
        result,ops,perms,msgs=execute_cold(regs,37,mem)
        if result!='CONTINUE' or regs!=saved or ops>256 or perms>2:raise RuntimeError('cold ABI restore/bound')
        if msgs:
            reference=[]
            for raw in (old,new):
                beta=raw>>40;t=(raw>>8)&((1<<32)-1);p=decode_slot(raw&255)
                base=PREF_BASE+(beta<<10)+(p<<2)
                prefix=b''.join(mem.get(base+k,0).to_bytes(32,'little') for k in range(4))
                reference.append(message(prefix,gray_z(t)))
            if msgs!=reference:raise RuntimeError('cold physical decode differs from reference')
    mem[('VCNT',)]=COLD_CAP
    regs=[0]*64
    if execute_cold(regs,37,mem)[0]!='ABORT':raise RuntimeError('cold cap failed')


def audit_hot_pair(batch,j,repetitions=2):
    program=compile_hot_leaf(j)
    for _ in range(repetitions):
        old_a2=list(batch.A2S);old_o2=list(batch.O2P)
        batch.flip(j);batch.check_o2p()
        mem,keys,cold=execute_hot_leaf(program,old_a2,old_o2)
        if any(mem['A2',i]!=batch.A2S[i] for i in READS):
            raise RuntimeError("physical A2 update differs from rebuild")
        if any(mem['O2',i//64,i%64]!=batch.O2P[i] for i in range(1600)):
            raise RuntimeError("physical O2P update differs from rebuild")
        reference=batch.keys()
        if keys != [reference[p] for p in PROC]:
            raise RuntimeError("physical hot leaf keys differ from reference evaluator")
    # One leaf at a time: do not keep32 programs in the bounded executor.
    del program

IR_HOT_COUNTS = (31373, 31362, 31363, 31373, 31378, 31355, 31377, 31358, 31357, 31342, 31372, 31340, 31348, 31353, 31358, 31339, 31349, 31343, 31358, 31352, 31350, 31352, 31357, 31353, 31359, 31361, 31362, 31360, 31367, 31373, 31350, 31374)


def audit_gray_order():
    """Organizer-only arithmetic/control audit; no claim to prove H1.

Each internal decision node has AND, compare and branch. Leaf destinations
are fixed labels GRAY_LEAF[k], so no run-time permutation table lookup occurs.
"""
    nodes = {}
    def build(lo,width):
        if width==1:return ('LEAF',GRAY_LEAF[lo])
        half=width//2;label=(lo,width)
        nodes[label]=(((1<<half)-1)<<lo,build(lo,half),build(lo+half,half))
        return label
    root=build(0,32)
    def choose(t):
        label=root;ops=0
        while label[0]!='LEAF':
            mask,left,right=nodes[label]
            flag=(t&mask)==0;ops+=3
            label=right if flag else left
        if ops!=15:raise RuntimeError('Gray dispatch cost')
        return label[1]
    indices=set(range(1,1025))|{v for k in range(32) for v in ((1<<k)-1,1<<k,(1<<k)+1) if 0<v<1<<32}
    for t in sorted(indices):
        delta=gray_z(t)^gray_z(t-1)
        if delta!=(1<<choose(t)):raise RuntimeError('Gray decision tree mapping')
        if swap_gray_coordinates(swap_gray_coordinates(t))!=t:raise RuntimeError('coordinate involution')
    counts=[0]*32
    for t in range(1,1<<16):counts[choose(t)]+=1
    for k in range(16):
        if counts[GRAY_LEAF[k]]!=1<<(15-k):raise RuntimeError('scaled exact Gray frequencies')
    weighted=IR_HOT_COUNTS[15]+sum(IR_HOT_COUNTS[GRAY_LEAF[k]]*(1<<(31-k)) for k in range(32))
    if weighted!=134654837523281:raise RuntimeError('whole traversal instruction bound')

# ---------------- dependency cone (proof Lemma 10), checked by poisoning ----------
STARTS = (2, 39, 34)    # start plane of rounds 3, 4, 5 (stored raw; its D is the fix word)


def round_needs(ns, nf, fp_out, fp_in):
    """Needed stored words ns {(L, b)} and fix columns nf of a theta-at-store round
    with start plane fp_out whose input lacks D on plane fp_in ->
    (chi outputs, parities, needed input words, needed input fix columns)."""
    dd = {(L % 5, b) for L, b in ns if b != fp_out} | {(x, fp_out) for x in nf}
    par = set()
    for x, b in dd:
        par.add(((x - 1) % 5, b)); par.add(((x + 1) % 5, (b - 1) % 64))
    chi = set(ns) | {(x + 5 * y, b) for x, b in par for y in range(5)}
    ins = set()
    for L, b in chi:
        X, Y = L % 5, L // 5
        for k in range(3):
            ins.add(_bsrc((X + k) % 5, Y, b))
    return chi, par, ins, {L % 5 for L, b in ins if b == fp_in}


NEED5 = frozenset((L, (b - RHO[L]) % 64) for L in DIAG for b in KEEP)
FIX5 = frozenset(L % 5 for L, b in NEED5 if b == STARTS[2])
_c5, _p5, NEED4, FIX4 = round_needs(NEED5, FIX5, STARTS[2], STARTS[1])
_c4, _p4, NEED3, FIX3 = round_needs(NEED4, FIX4, STARTS[1], STARTS[0])
assert (len(NEED5), len(FIX5), len(_c5), len(_p5), len(NEED4), len(FIX4), len(_p4), len(NEED3), len(FIX3)) == \
    (175, 0, 1161, 229, 1363, 5, 320, 1600, 5)
POISON = [int.from_bytes(hashlib.sha256(b"poison" + i.to_bytes(2, "little")).digest(), "little") for i in range(1600)]


def poison(S, fix, need, fneed):
    """Replace every word outside the cone by an unrelated constant (Lemma 10 says none is read)."""
    return ([S[i] if (i >> 6, i & 63) in need else POISON[i] for i in range(1600)],
            [fix[x] if x in fneed else POISON[x] for x in range(5)])


# ---------------- batch ------------------------------------------------------
class Batch:
    """256 groups (bit positions); prefixes[p] is a structured 128-byte prefix."""

    def __init__(self, prefixes, zbits):
        self.prefixes = prefixes
        self.z = 0
        A2 = self.a2_true(0)
        for j in zbits:
            A2j = self.a2_true(1 << j)
            supp = {64 * L + b for L, b in SUPPORT[j]}
            for i in range(1600):
                if A2j[i] ^ A2[i] != (W if i in supp else 0):
                    raise RuntimeError("A2(e_j) ^ A2(0) is not all-ones exactly on the 22-word support")
        self.A2S = [v ^ (W if i in PI else 0) for i, v in enumerate(A2)]
        self.O2P = build_o2p(A2)

    def a2_true(self, z):
        """A2 (round 1 + round-2 theta) of the batch at z, computed from scratch."""
        S = [0] * 1600
        msgs = [message(p, z) for p in self.prefixes]
        for w in range(4):
            rows = [int.from_bytes(m[32 * w:32 * w + 32], "little") for m in msgs]
            S[256 * w:256 * w + 256] = transpose(rows, SETUP_ORDER)
        S[64 * 16 + 1] = W
        S[64 * 16 + 2] = W
        S[64 * 16 + 63] = W
        out, D2 = round_pass(S, d_words(S), RC[0])
        return [out[i] ^ D2[DCOL[i]] for i in range(1600)]

    def flip(self, j):
        self.z ^= 1 << j
        incr_round2(self.A2S, self.O2P, j)

    def check_o2p(self):
        A2 = self.a2_true(self.z)
        if any(self.A2S[i] != A2[i] ^ (W if i in PI else 0) for i in READS):
            raise RuntimeError("maintained A2 differs from A2 rebuilt from the prefixes")
        if build_o2p(A2) != self.O2P:
            raise RuntimeError("incrementally maintained O2P differs from O2P rebuilt from A2")

    def keys(self):
        """Stored keys key_of_digest(digest) indexed by slot."""
        S, fix = round_ts(self.O2P, None, None, PLAN3, STARTS[0])
        S, fix = round_ts(S, fix, STARTS[0], PLAN4, STARTS[1])
        S, fix = poison(S, fix, NEED4, FIX4)
        S, fix = round_ts(S, fix, STARTS[1], PLAN5, STARTS[2])
        S, fix = poison(S, fix, NEED5, FIX5)
        rows = last_rows(S, fix)
        if any(rows[r] for r in range(256) if r not in KEYROWS):
            raise RuntimeError("a key row outside ROWOF is nonzero")
        out, _ = transpose_z(rows)
        if out != transpose(rows, STEP_ORDER):
            raise RuntimeError("zero-row transpose differs from the full transpose")
        return out


def trial_prefixes(seed, groups):
    return [structured_prefix(int.from_bytes(b"".join(
        hashlib.sha256(b"s3r6-linear128-v1" + seed + g.to_bytes(2, "little")
                       + bytes((part,))).digest() for part in range(3)), "little"))
        for g in range(groups)]


def _check(prefix, z, key):
    if key_of_digest(int.from_bytes(sponge6(message(prefix, z)), "little")) != key:
        raise RuntimeError("bitsliced evaluator disagrees with direct sponge")


M128 = (1 << 128) - 1
KEYBITS = 4 * NP


class TagTable:
    """The program's tagged-id table (proof Section 5.3), run on the 140-bit keys
    of one batch as a self-check.  Slot S[K] (K < 2^140 is the address) holds
    TAG * 2^128 + n; a lookup is a candidate iff the high half equals TAG.
    Never-written words are adversarial garbage: 1/16 of the addresses return
    TAG in the high half with a junk id (forcing the verify-and-continue
    path), the rest a word whose high half differs from TAG."""

    def __init__(self, tag_seed):
        self.tag = int.from_bytes(hashlib.sha256(b"s3r6-tag" + tag_seed).digest()[:16], "little")
        self.mem = {}
        self.n = 0
        self.key_of = {}                # message number -> stored key
        self.garbage_candidates = 0

    def garbage(self, K):
        h = hashlib.sha256(b"s3r6-garbage" + K.to_bytes(18, "little")).digest()
        junk = int.from_bytes(h[:16], "little")
        hi = self.tag if h[16] < 16 else self.tag ^ (1 + int.from_bytes(h[17:25], "little"))
        return (hi << 128) | junk

    def step(self, K, verify):
        if not 0 <= K < 1 << KEYBITS:
            raise RuntimeError("key is not a 140-bit table address")
        w = self.mem[K] if K in self.mem else self.garbage(K)
        if (w ^ (self.tag << 128)) >> 128 == 0:            # candidate
            i = w & M128
            if i < self.n and self.mem.get(K) == w:
                if self.key_of[i] != K:
                    raise RuntimeError("stored id does not decode to a message with this key")
                verify(i, self.n)                           # full digests compared; continue
            else:
                self.garbage_candidates += 1                # verified and continued in the program
        self.mem[K] = (self.tag << 128) | self.n
        self.key_of[self.n] = K
        self.n += 1

    def check_ids(self):
        for K, w in self.mem.items():
            if w >> 128 != self.tag or self.key_of[w & M128] != K:
                raise RuntimeError("table word does not decode to a message with its key")


def run_trials(seeds, layout, mask_le):
    kmask = key_mask_of(mask_le)
    G, zs = LAYOUTS[layout]
    per = 256 // G
    zbits = sorted({(a ^ b).bit_length() - 1 for a, b in zip(zs, zs[1:])})
    results = []
    for c0 in range(0, len(seeds), per):
        chunk = seeds[c0:c0 + per]
        pres = [trial_prefixes(s, G) for s in chunk]
        slots = [p for ps in pres for p in ps]
        slots += [structured_prefix(0)] * (256 - len(slots))
        batch = Batch(slots, zbits)
        if c0 == 0:
            audit_gray_order()
            audit_cold(slots)
            batch.flip(15)
            audit_hot_pair(batch,15,repetitions=1)
            if batch.z!=0:raise RuntimeError('Gray warm-entry convention')
            for j in range(32):
                audit_hot_pair(batch,j)
            if batch.z != 0:
                raise RuntimeError("paired flips failed to restore the starting index")
        table = TagTable(b"".join(chunk))

        def verify(i, n, pres=pres):
            """Rebuild both messages from their numbers and compare full digests."""
            ms = []
            for v in (i, n):
                t_, q_ = v >> 8, v & 255
                ti_, g_ = divmod(decode_slot(q_), G)
                ms.append(message(pres[ti_][g_], zs[t_]) if ti_ < len(pres) else None)
            if ms[0] is not None and ms[0] != ms[1] and sponge6(ms[0]) == sponge6(ms[1]):
                raise RuntimeError("full collision at experiment scale (not expected)")
        state = [{"seen": {}, "first": None, "pairs": 0, "checks": 0} for _ in chunk]
        for t, z in enumerate(zs):
            if t:
                batch.flip((z ^ zs[t - 1]).bit_length() - 1)
            keys = batch.keys()
            pow2 = t > 0 and not t & (t - 1)
            done = set()
            for p in PROC:                  # processing order of the program
                table.step(keys[p], verify)
                ti, g = divmod(p, G)
                if ti >= len(chunk):
                    continue
                st = state[ti]
                key = keys[p]
                if st["checks"] < EXACT_CHECKS or (pow2 and ti not in done):
                    _check(pres[ti][g], z, key)
                    st["checks"] += 1
                    done.add(ti)
                k = key & kmask             # equal masked keys <=> equal masked digests
                hit = st["seen"].get(k)
                if hit is None:
                    st["seen"][k] = [(g, z)]
                else:
                    st["pairs"] += len(hit)
                    if st["first"] is None:
                        st["first"] = (hit[0], (g, z))
                    hit.append((g, z))
        batch.check_o2p()
        table.check_ids()
        if table.garbage_candidates == 0 and len(zs) * 256 >= 512:
            raise RuntimeError("the adversarial garbage path was never taken")
        for ti, st in enumerate(state):
            obs = {"masked_pairs": st["pairs"], "messages": G * len(zs), "exactness_checks": st["checks"],
                   "support_columns_checked": len(zbits), "o2p_rebuild_checked": 1,
                   "physical_hot_leaves": 32 if c0==0 else 0, "physical_cold_audit": int(c0==0)}
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
        sq = sum(o["masked_pairs"] ** 2 for _, _, o in res)
        print(json.dumps({"layout": layout, "trials": trials, "successes": succ, "masked_pairs": pairs,
                          "masked_pairs_sq": sq}))
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
