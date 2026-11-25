"""P2 of the filing of O. Goldzweig's 38-step SHA-256 collision attack (ePrint 2026/2913): an independent Python port
of the construction of the upper-pair table, run by the organizer on a slice of A14 values.

The normative statement of steps 1 to 4 of P2 (proof.md Section 5) is the C program of proof.md Appendix A, which
built the full table. This port computes the same functions under the same names; the trials below compare it with
the records that C build stored for the same A14 values.

Functions, in the order P2 applies them to one A14 survivor:
  a14ok(A14)          the conditions on A14 alone (dE14 = -0x21000 with XOR 0x21000, dE15 = 0x200, dW15 = 4)
  pairs_for(A14)      the valid upper pairs (A14, A15): steps 14..16 follow the characteristic with XOR digits
                      E14 0x21000, A15 0x08010000, E15 0x200, W15 4, and rows 17 and 30 hold (piok); solved over
                      x = E15 with the step-16 difference as a GF(2)-affine system per sign class (walk)
  kpi(pi, cls16)      K(pi): the keys c with step 17 following the characteristic, E16 XOR = 0x00200224 and
                      A16 XOR = 4 (minimal carries) and the bit-27 rule E16[27] = E15[27]; solved over x = E16
  live(pi, c)         some E17 with minimal carries (E17 XOR = 0x08800200) passes step 18; the affine solution
                      space is walked if it has at most 1024 points, else 1024 points are drawn from it with a
                      splitmix64 stream seeded by mix3(A14, A15, c)
An entry (c, pi) of the table is a live key c in K(pi) of a valid pair pi.

Trials (each returns a non-colliding marker pair only if every comparison holds; trials >= 2 return no pair):
  0  A14 = 5bde5962, the published one: a14ok; the solver on the first 2^16 points of each affine space of x = E15
     (Gray-code order) finds the expected pairs; each of the 192 valid pairs of the C build passes piok with its
     class; for the published pair (A15 9b3a6d8a, class 7) K(pi) has the expected size, contains the published
     key 00b50618, and its live keys are exactly the 789 that the C build stored (every entry of the pair tested)
  1  A14 = 4f9d3ed0: the same walk prefix and validity checks; then K(pi) of all 256 valid pairs (1,024 entries, as
     in the C build) and the liveness of every entry: the live keys are exactly the 304 that the C build stored,
     in the same 2 pairs
"""
import hashlib
import json
import sys

M = 0xFFFFFFFF
M64 = (1 << 64) - 1
CA = 0xf8010000
A10 = (0x959ea855, 0xd935a3b4)
A11 = (0x9871db5e, 0x9991eb9f)
A12 = (0x6a30e20f, 0x63b1f047)
A13 = (0xdad82f20, 0xd2793d21)
E10 = (0x1e38fd64, 0x85ade09b)
E11 = (0xe66f7c72, 0x2017f638)
E12 = (0xa994479e, 0xaff6c796)
E13 = (0xc21a9d0d, 0x86580f08)
K14, K15, K16, K17 = 0x9bdc06a7, 0xc19bf174, 0xe49b69c1, 0xefbe4786
R_S1, R_S0 = (6, 11, 25), (2, 13, 22)
WALKMAX = 1024


def rr(x, n):
    return ((x >> n) | (x << (32 - n))) & M


def S0(x):
    return rr(x, 2) ^ rr(x, 13) ^ rr(x, 22)


def S1(x):
    return rr(x, 6) ^ rr(x, 11) ^ rr(x, 25)


def s0(x):
    return rr(x, 7) ^ rr(x, 18) ^ (x >> 3)


def s1(x):
    return rr(x, 17) ^ rr(x, 19) ^ (x >> 10)


def ch(x, y, z):
    return (x & y) ^ (~x & z & M)


def mj(x, y, z):
    return (x & y) ^ (x & z) ^ (y & z)


def par(x):
    return bin(x).count("1") & 1


class SM:                      # splitmix64
    def __init__(self, s):
        self.s = s & M64

    def next(self):
        self.s = (self.s + 0x9e3779b97f4a7c15) & M64
        z = self.s
        z = ((z ^ (z >> 30)) * 0xbf58476d1ce4e5b9) & M64
        z = ((z ^ (z >> 27)) * 0x94d049bb133111eb) & M64
        return z ^ (z >> 31)


def mix3(a, b, c):
    return SM(((a << 32) | b) ^ ((c * 0x9e3779b97f4a7c15) & M64)).next()


# ---------- the two executions of steps 14..17 for an upper pair
class Up:
    def __init__(self, A14, A15):
        self.A14 = A14
        self.A15 = (A15, (A15 + CA) & M)
        self.E14 = tuple((A14 + A10[k] - S0(A13[k]) - mj(A13[k], A12[k], A11[k])) & M for k in (0, 1))
        self.E15 = tuple((self.A15[k] + A11[k] - S0(A14) - mj(A14, A13[k], A12[k])) & M for k in (0, 1))
        self.W15 = tuple((self.E15[k] - A11[k] - E11[k] - S1(self.E14[k]) - ch(self.E14[k], E13[k], E12[k]) - K15) & M
                         for k in (0, 1))
        self.W14 = (self.E14[0] - A10[0] - E10[0] - S1(E13[0]) - ch(E13[0], E12[0], E11[0]) - K14) & M


def set16(d):          # dE16 in {e1 2^21 - 2^9 + e2 2^5 + e3 2^2}: class 1..8 or 0
    for m in range(8):
        v = ((0x200000 if m & 1 else -0x200000) - 0x200 + (0x20 if m & 2 else -0x20) + (4 if m & 4 else -4)) & M
        if d == v:
            return m + 1
    return 0


def set17(d):          # dE17 in {e4 2^27 + e5 2^23 - 2^9}: class 1..4 or 0
    for m in range(4):
        v = ((0x8000000 if m & 1 else -0x8000000) + (0x800000 if m & 2 else -0x800000) - 0x200) & M
        if d == v:
            return m + 1
    return 0


def a14ok(A14):
    e0 = (A14 + A10[0] - S0(A13[0]) - mj(A13[0], A12[0], A11[0])) & M
    e1 = (A14 + A10[1] - S0(A13[1]) - mj(A13[1], A12[1], A11[1])) & M
    if (e1 - e0) & M != (-0x21000) & M or e0 ^ e1 != 0x21000:
        return False
    if (CA + (A11[1] - A11[0]) - (mj(A14, A13[1], A12[1]) - mj(A14, A13[0], A12[0]))) & M != 0x200:
        return False
    g0 = -S0(A14) - mj(A14, A13[0], A12[0]) - E11[0] - S1(e0) - ch(e0, E13[0], E12[0])
    g1 = -S0(A14) - mj(A14, A13[1], A12[1]) - E11[1] - S1(e1) - ch(e1, E13[1], E12[1])
    return (CA + g1 - g0) & M == 4


def piok(u):
    """Validity of an upper pair; returns the dE16 class (1..8) or 0."""
    if u.A15[0] ^ u.A15[1] != 0x08010000:
        return 0
    if (u.E15[1] - u.E15[0]) & M != 0x200 or u.E15[0] ^ u.E15[1] != 0x200:
        return 0
    if (u.W15[1] - u.W15[0]) & M != 4 or u.W15[0] ^ u.W15[1] != 4:
        return 0
    if (s1(u.W15[1]) - s1(u.W15[0])) & M != (-0x28000) & M:       # row 17
        return 0
    if (s0(u.W15[1]) - s0(u.W15[0])) & M != CA:                   # row 30
        return 0
    E16 = [(A12[k] + E12[k] + S1(u.E15[k]) + ch(u.E15[k], u.E14[k], E13[k]) + K16) & M for k in (0, 1)]
    A16 = [(E16[k] - A12[k] + S0(u.A15[k]) + mj(u.A15[k], u.A14, A13[k])) & M for k in (0, 1)]
    if (A16[1] - A16[0]) & M != 4:
        return 0
    return set16((E16[1] - E16[0]) & M)


def step16(u, c):
    W16 = (s1(u.W14) + c) & M
    E16 = [(A12[k] + E12[k] + S1(u.E15[k]) + ch(u.E15[k], u.E14[k], E13[k]) + K16 + W16) & M for k in (0, 1)]
    A16 = [(E16[k] - A12[k] + S0(u.A15[k]) + mj(u.A15[k], u.A14, A13[k])) & M for k in (0, 1)]
    return E16, A16


def step17(u, E16, A16, W17):
    E17 = [(A13[k] + E13[k] + S1(E16[k]) + ch(E16[k], u.E15[k], u.E14[k]) + K17 + W17) & M for k in (0, 1)]
    A17 = [(E17[k] - A13[k] + S0(A16[k]) + mj(A16[k], u.A15[k], u.A14)) & M for k in (0, 1)]
    return E17, A17


# ---------- a modular equation  cst + sum_i (feature_i ? v1_i : v0_i), feature_i = parity(word & mask_i)
class Eq:
    def __init__(self):
        self.mask, self.v0, self.v1, self.cst = [], [], [], 0

    def add(self, mask, v0, v1, fixm, fixv):
        v0 &= M
        v1 &= M
        if v0 == v1:
            self.cst = (self.cst + v0) & M
            return
        if not (mask & ~fixm & M):
            self.cst = (self.cst + (v1 if par(fixv & mask) else v0)) & M
            return
        for i, m in enumerate(self.mask):
            if m == mask:
                self.v0[i] = (self.v0[i] + v0) & M
                self.v1[i] = (self.v1[i] + v1) & M
                return
        self.mask.append(mask)
        self.v0.append(v0)
        self.v1.append(v1)

    def sigma(self, D, r, fixm, fixv):      # F(w ^ D) - F(w) = Y - 2 (F(w) & Y), Y = F(D), F a rotation sum
        Y = 0
        for k in r:
            Y ^= rr(D, k)
        for j in range(32):
            if Y >> j & 1:
                m = 0
                for k in r:
                    m ^= 1 << ((j + k) & 31)
                self.add(m, 1 << j, -(1 << j), fixm, fixv)

    def bitwise(self, isch, D, b0, c0, b1, c1, fixm, fixv):
        for i in range(32):
            bi0, ci0, bi1, ci1, d = b0 >> i & 1, c0 >> i & 1, b1 >> i & 1, c1 >> i & 1, D >> i & 1
            val = []
            for v in (0, 1):
                w = v ^ d
                if isch:
                    o1 = (w & bi1) | ((~w & 1) & ci1)
                    o0 = (v & bi0) | ((~v & 1) & ci0)
                else:
                    o1 = (w & bi1) | (w & ci1) | (bi1 & ci1)
                    o0 = (v & bi0) | (v & ci0) | (bi0 & ci0)
                val.append(((o1 - o0) << i) & M)
            self.add(1 << i, val[0], val[1], fixm, fixv)

    def value(self, a):
        s = self.cst
        for i in range(len(self.mask)):
            s += self.v1[i] if a >> i & 1 else self.v0[i]
        return s & M


# ---------- GF(2) system on the 32 bits of x (rows kept in reduced form, pivot = top bit)
def gs_add(rows, m, b):
    for i in range(len(rows)):
        rm, rb = rows[i]
        if m >> (rm.bit_length() - 1) & 1:
            m ^= rm
            b ^= rb
    if not m:
        return b == 0
    p = m.bit_length() - 1
    for i in range(len(rows)):
        rm, rb = rows[i]
        if rm >> p & 1:
            rows[i] = (rm ^ m, rb ^ b)
    rows.append((m, b))
    return True


def gs_space(rows):
    piv = 0
    x0 = 0
    for rm, rb in rows:
        piv |= 1 << (rm.bit_length() - 1)
        if rb:
            x0 |= 1 << (rm.bit_length() - 1)
    basis = []
    for f in range(32):
        if not piv >> f & 1:
            v = 1 << f
            for rm, rb in rows:
                if rm >> f & 1:
                    v |= 1 << (rm.bit_length() - 1)
            basis.append(v)
    return x0, basis


def ctz(n):
    return (n & -n).bit_length() - 1


def system(fxm, fxv, ex, ax):
    rows = []
    for b in range(32):
        if fxm >> b & 1 and not gs_add(rows, 1 << b, fxv >> b & 1):
            return None
    for i, m in enumerate(ex.mask):
        if not gs_add(rows, m, ax >> i & 1):
            return None
    return rows


def solve(fxm, fxv, ex, tx, kappa, fym, fyv, ey, ty, stop_first, seed=None, out=None):
    """Solutions x (fixed bits, ex in the target set) with y = x + kappa meeting fym/fyv and ey = ty[target]."""
    cnt = 0
    nx, ny = len(ex.mask), len(ey.mask)
    for ax in range(1 << nx):
        s = ex.value(ax)
        ti = -1
        for t in range(len(tx)):
            if s == tx[t]:
                ti = t
        if ti < 0:
            continue
        rows = system(fxm, fxv, ex, ax)
        if rows is None:
            continue
        yok = [ey.value(ay) == ty[ti] for ay in range(1 << ny)]
        if not any(yok):
            continue
        x0, B = gs_space(rows)
        k = len(B)
        rnd = stop_first and (1 << k) > WALKMAX
        x = x0
        for it in range(WALKMAX if rnd else 1 << k):
            if rnd:
                r = seed.next()
                x = x0
                for b in range(k):
                    if r >> b & 1:
                        x ^= B[b]
            elif it:
                x ^= B[ctz(it)]
            y = (x + kappa) & M
            if y & fym != fyv:
                continue
            ay = 0
            for i in range(ny):
                ay |= par(y & ey.mask[i]) << i
            if yok[ay]:
                cnt += 1
                if out is not None:
                    out.append(x)
                if stop_first:
                    return cnt
    return cnt


def pairs_for(A14, limit=None):
    """Valid upper pairs (A15, dE16 class) for one A14, in solver order; the base variable is x = E15.
    Every point of the affine solution spaces is tested with piok; two necessary conditions of piok are tested first
    (A15 bit 16 = 0 and bit 27 = 1, which is A15 XOR A15' = 0x08010000; W15 bit 2 = 0, which is W15 XOR W15' = 4).
    limit (organizer trials only) walks the first `limit` points of each space in Gray-code order."""
    E14 = [(A14 + A10[k] - S0(A13[k]) - mj(A13[k], A12[k], A11[k])) & M for k in (0, 1)]
    fxm, fxv = 1 << 9, 0
    ex = Eq()
    ex.cst = ((A12[1] - A12[0]) + (E12[1] - E12[0])) & M
    ex.sigma(0x200, R_S1, fxm, fxv)
    ex.bitwise(1, 0x200, E14[0], E13[0], E14[1], E13[1], fxm, fxv)
    tx = [(((0x200000 if m & 1 else -0x200000) - 0x200 + (0x20 if m & 2 else -0x20) + (4 if m & 4 else -4)) & M)
          for m in range(8)]
    h0 = (A11[0] - S0(A14) - mj(A14, A13[0], A12[0])) & M                 # A15 = E15 - h0
    cw = (A11[0] + E11[0] + S1(E14[0]) + ch(E14[0], E13[0], E12[0]) + K15) & M   # W15 = E15 - cw
    out = []
    for ax in range(1 << len(ex.mask)):
        if ex.value(ax) not in tx:
            continue
        rows = system(fxm, fxv, ex, ax)
        if rows is None:
            continue
        x0, B = gs_space(rows)
        x = x0
        n = 1 << len(B)
        for it in range(n if limit is None else min(n, limit)):
            if it:
                x ^= B[ctz(it)]
            A15 = (x - h0) & M
            if A15 & 0x08010000 != 0x08000000 or (x - cw) & 4:
                continue
            cl = piok(Up(A14, A15))
            if cl:
                out.append((A15, cl))
    return out


def kpi(u, cls16):
    """K(pi) under the bit-27 rule with minimal carries in E16 and A16; the base variable is x = E16."""
    m = cls16 - 1
    D = 0x00200224
    fxm = D | (1 << 27)
    fxv = (0 if m & 1 else 1 << 21) | (1 << 9) | (0 if m & 2 else 1 << 5) | (0 if m & 4 else 1 << 2)
    fxv |= u.E15[0] & (1 << 27)
    ex = Eq()
    ex.cst = ((A13[1] - A13[0]) + (E13[1] - E13[0])) & M
    ex.sigma(D, R_S1, fxm, fxv)
    ex.bitwise(1, D, u.E15[0], u.E14[0], u.E15[1], u.E14[1], fxm, fxv)
    tx = [(((0x8000000 if q & 1 else -0x8000000) + (0x800000 if q & 2 else -0x800000) - 0x200) & M) for q in range(4)]
    ty = [((A13[1] - A13[0]) - t) & M for t in tx]
    fym, fyv = 4, 0
    ey = Eq()
    ey.sigma(4, R_S0, fym, fyv)
    ey.bitwise(0, 4, u.A15[0], u.A14, u.A15[1], u.A14, fym, fyv)
    kappa = (-A12[0] + S0(u.A15[0]) + mj(u.A15[0], u.A14, A13[0])) & M
    P16 = (A12[0] + E12[0] + S1(u.E15[0]) + ch(u.E15[0], u.E14[0], E13[0]) + K16 + s1(u.W14)) & M
    xs = []
    solve(fxm, fxv, ex, tx, kappa, fym, fyv, ey, ty, False, out=xs)
    return [(x - P16) & M for x in xs[:1 << 16]]


def live(u, c):
    """Liveness of the entry (c, pi): some E17 with minimal carries passes step 18 (probe cap 1024)."""
    E16, A16 = step16(u, c)
    E17, A17 = step17(u, E16, A16, 0)
    c17 = set17((E17[1] - E17[0]) & M)
    if not c17 or A17[0] != A17[1]:
        return False
    m = c17 - 1
    D = 0x08800200
    fxm, fxv = D, (1 << 9) | (0 if m & 1 else 1 << 27) | (0 if m & 2 else 1 << 23)
    ex = Eq()
    ex.cst = (u.E14[1] - u.E14[0]) & M
    ex.sigma(D, R_S1, fxm, fxv)
    ex.bitwise(1, D, E16[0], u.E15[0], E16[1], u.E15[1], fxm, fxv)
    ey = Eq()
    for i in range(32):
        a0, a1, b0, b1 = A16[0] >> i & 1, A16[1] >> i & 1, u.A15[0] >> i & 1, u.A15[1] >> i & 1
        val = [((((v & a1) | (v & b1) | (a1 & b1)) - ((v & a0) | (v & b0) | (a0 & b0))) << i) & M for v in (0, 1)]
        ey.add(1 << i, val[0], val[1], 0, 0)
    seed = SM(mix3(u.A14, u.A15[0], c))
    return solve(fxm, fxv, ex, [0], (A17[0] - E17[0]) & M, 0, 0, ey, [0], True, seed=seed) > 0


# ---------- expected values from the stored C build (table/chunk*.bin records and single-A14 runs)
EXPECT = [
{
"A14": 1541298530,
"walk_limit": 65536,
"prefix_digest": "1c4673c827d1818b0b97b3ad",
"n_pairs": 192,
"pairs": "fb2889ca7 fb288dca7 fb2885ca7 fb2881ca7 fb2a81ca7 fb2a85ca7 fb2a8dca7 fb2a89ca7 fb3a89ca7 fb3a8dca7 fb3a85ca7 fb3a81ca7 fb3881ca7 fb3885ca7 fb388dca7 fb3889ca7 fb6289ca7 fb628dca7 fb6285ca7 fb6281ca7 fb6081ca7 fb6085ca7 fb608dca7 fb6089ca7 fc3889ea7 fc388dea7 fc3885ea7 fc3881ea7 fc3a81ea7 fc3a85ea7 fc3a8dea7 fc3a89ea7 fc2a89ea7 fc2a8dea7 fc2a85ea7 fc2a81ea7 fc2881ea7 fc2885ea7 fc288dea7 fc2889ea7 fe6289ca7 fe628dca7 fe6285ca7 fe6281ca7 fe6081ca7 fe6085ca7 fe608dca7 fe6089ca7 1e60618a7 1e60658a7 1e606d8a7 1e60698a7 1e62698a7 1e626d8a7 1e62658a7 1e62618a7 1c2861aa7 1c2865aa7 1c286daa7 1c2869aa7 1c2a69aa7 1c2a6daa7 1c2a65aa7 1c2a61aa7 1c3a61aa7 1c3a65aa7 1c3a6daa7 1c3a69aa7 1c3869aa7 1c386daa7 1c3865aa7 1c3861aa7 1b60618a7 1b60658a7 1b606d8a7 1b60698a7 1b62698a7 1b626d8a7 1b62658a7 1b62618a7 1b38618a7 1b38658a7 1b386d8a7 1b38698a7 1b3a698a7 1b3a6d8a7 1b3a658a7 1b3a618a7 1b2a618a7 1b2a658a7 1b2a6d8a7 1b2a698a7 1b28698a7 1b286d8a7 1b28658a7 1b28618a7 9b28618a7 9b28658a7 9b286d8a7 9b28698a7 9b2a698a7 9b2a6d8a7 9b2a658a7 9b2a618a7 9b3a618a7 9b3a658a7 9b3a6d8a7 9b3a698a7 9b38698a7 9b386d8a7 9b38658a7 9b38618a7 9b62618a7 9b62658a7 9b626d8a7 9b62698a7 9b60698a7 9b606d8a7 9b60658a7 9b60618a7 9c3861aa7 9c3865aa7 9c386daa7 9c3869aa7 9c3a69aa7 9c3a6daa7 9c3a65aa7 9c3a61aa7 9c2a61aa7 9c2a65aa7 9c2a6daa7 9c2a69aa7 9c2869aa7 9c286daa7 9c2865aa7 9c2861aa7 9e62618a7 9e62658a7 9e626d8a7 9e62698a7 9e60698a7 9e606d8a7 9e60658a7 9e60618a7 7e6089ca7 7e608dca7 7e6085ca7 7e6081ca7 7e6281ca7 7e6285ca7 7e628dca7 7e6289ca7 7c2889ea7 7c288dea7 7c2885ea7 7c2881ea7 7c2a81ea7 7c2a85ea7 7c2a8dea7 7c2a89ea7 7c3a89ea7 7c3a8dea7 7c3a85ea7 7c3a81ea7 7c3881ea7 7c3885ea7 7c388dea7 7c3889ea7 7b6089ca7 7b608dca7 7b6085ca7 7b6081ca7 7b6281ca7 7b6285ca7 7b628dca7 7b6289ca7 7b3889ca7 7b388dca7 7b3885ca7 7b3881ca7 7b3a81ca7 7b3a85ca7 7b3a8dca7 7b3a89ca7 7b2a89ca7 7b2a8dca7 7b2a85ca7 7b2a81ca7 7b2881ca7 7b2885ca7 7b288dca7 7b2889ca7",
"entries": 2496,
"only_pair": 2604297610,
"sub_mask": 0,
"n_sub": 2496,
"n_live_sub": 789,
"live_sub_digest": "5231191b569ea4eccbaf75bf",
"pairs_live": 64
},
{
"A14": 1335705296,
"walk_limit": 65536,
"prefix_digest": "4f53cda18c2baa0c0354bb5f",
"n_pairs": 256,
"pairs": "582002b07 583aeef07 583aeaf07 583ae6f07 483c42307 483c2e307 483c2a307 483c26307 583a02b07 5838e6f07 5838eaf07 5838eef07 483e26307 483e2a307 483e2e307 483e42307 482e42307 482e2e307 482e2a307 482e26307 583002b07 5828eef07 5828eaf07 5828e6f07 582a02b07 482c26307 482c2a307 482c2e307 482c42307 582ae6f07 582aeaf07 582aeef07 5b2002907 5b3aeed07 5b3aead07 5b3ae6d07 4b3c42107 4b3c2e107 4b3c2a107 4b3c26107 5b3a02907 5b38e6d07 5b38ead07 5b38eed07 4b3e26107 4b3e2a107 4b3e2e107 4b3e42107 4b2e42107 4b2e2e107 4b2e2a107 4b2e26107 5b3002907 5b28eed07 5b28ead07 5b28e6d07 5b2a02907 4b2c26107 4b2c2a107 4b2c2e107 4b2c42107 5b2ae6d07 5b2aead07 5b2aeed07 7b2ac6d07 7b2acad07 7b2aced07 7b2ae2d07 6b2c06107 6b2c0a107 6b2c0e107 6b2c22107 7b28e2d07 7b28ced07 7b28cad07 7b28c6d07 6b2e22107 6b2e0e107 6b2e0a107 6b2e06107 6b3e06107 6b3e0a107 6b3e0e107 6b3e22107 7b38c6d07 7b38cad07 7b38ced07 7b38e2d07 6b3c22107 6b3c0e107 6b3c0a107 6b3c06107 7b3ae2d07 7b3aced07 7b3acad07 7b3ac6d07 782ac6f07 782acaf07 782acef07 782ae2f07 682c06307 682c0a307 682c0e307 682c22307 7828e2f07 7828cef07 7828caf07 7828c6f07 682e22307 682e0e307 682e0a307 682e06307 683e06307 683e0a307 683e0e307 683e22307 7838c6f07 7838caf07 7838cef07 7838e2f07 683c22307 683c0e307 683c0a307 683c06307 783ae2f07 783acef07 783acaf07 783ac6f07 f83ac6f07 f83acaf07 f83acef07 f83ae2f07 e83c06307 e83c0a307 e83c0e307 e83c22307 f838e2f07 f838cef07 f838caf07 f838c6f07 e83e22307 e83e0e307 e83e0a307 e83e06307 e82e06307 e82e0a307 e82e0e307 e82e22307 f828c6f07 f828caf07 f828cef07 f828e2f07 e82c22307 e82c0e307 e82c0a307 e82c06307 f82ae2f07 f82acef07 f82acaf07 f82ac6f07 fb3ac6d07 fb3acad07 fb3aced07 fb3ae2d07 eb3c06107 eb3c0a107 eb3c0e107 eb3c22107 fb38e2d07 fb38ced07 fb38cad07 fb38c6d07 eb3e22107 eb3e0e107 eb3e0a107 eb3e06107 eb2e06107 eb2e0a107 eb2e0e107 eb2e22107 fb28c6d07 fb28cad07 fb28ced07 fb28e2d07 eb2c22107 eb2c0e107 eb2c0a107 eb2c06107 fb2ae2d07 fb2aced07 fb2acad07 fb2ac6d07 db2aeed07 db2aead07 db2ae6d07 cb2c42107 cb2c2e107 cb2c2a107 cb2c26107 db2a02907 db28e6d07 db28ead07 db28eed07 db3002907 cb2e26107 cb2e2a107 cb2e2e107 cb2e42107 cb3e42107 cb3e2e107 cb3e2a107 cb3e26107 db38eed07 db38ead07 db38e6d07 db3a02907 cb3c26107 cb3c2a107 cb3c2e107 cb3c42107 db3ae6d07 db3aead07 db3aeed07 db2002907 d82aeef07 d82aeaf07 d82ae6f07 c82c42307 c82c2e307 c82c2a307 c82c26307 d82a02b07 d828e6f07 d828eaf07 d828eef07 d83002b07 c82e26307 c82e2a307 c82e2e307 c82e42307 c83e42307 c83e2e307 c83e2a307 c83e26307 d838eef07 d838eaf07 d838e6f07 d83a02b07 c83c26307 c83c2a307 c83c2e307 c83c42307 d83ae6f07 d83aeaf07 d83aeef07 d82002b07",
"entries": 1024,
"only_pair": 0,
"sub_mask": 0,
"n_sub": 1024,
"n_live_sub": 304,
"live_sub_digest": "5f9be58a176f1ccd0e81a104",
"pairs_live": 2
}
]


def digest(obj):
    return hashlib.sha256(json.dumps(obj).encode()).hexdigest()[:24]


def slice_check(e, pub=None):
    """One A14 of the slice: the solver on a Gray-code prefix of its spaces, the validity and class of every valid
    pair of the C build, the total |K(pi)|, and the live verdicts on the subsample against the stored C records."""
    A14 = e["A14"]
    if not a14ok(A14):
        return False
    if digest(pairs_for(A14, limit=e["walk_limit"])) != e["prefix_digest"]:
        return False
    pairs = [(int(p[:8], 16), int(p[8:])) for p in e["pairs"].split()]
    if len(pairs) != e["n_pairs"] or any(piok(Up(A14, A15)) != cl for A15, cl in pairs):
        return False
    entries, live_sub, n_sub, pairs_live = 0, [], 0, set()
    for A15, cl in pairs:
        if e.get("only_pair") and A15 != e["only_pair"]:
            continue
        u = Up(A14, A15)
        keys = kpi(u, cl)
        entries += len(keys)
        for c in keys:
            if (mix3(A14, A15, c) >> 40) & e["sub_mask"] == 0:
                n_sub += 1
                if live(u, c):
                    live_sub.append([A15, c])
                    pairs_live.add(A15)
        if pub and A15 == pub[0]:
            if cl != pub[2] or pub[1] not in keys or not live(u, pub[1]):
                return False
    live_sub.sort()
    ok = entries == e["entries"] and n_sub == e["n_sub"]
    ok = ok and len(live_sub) == e["n_live_sub"] and digest(live_sub) == e["live_sub_digest"]
    if e["sub_mask"] == 0 and not e.get("only_pair"):   # every entry of the A14: pairs with live keys as in the C build
        ok = ok and len(pairs_live) == e["pairs_live"]
    return ok


def main():
    req = json.loads(sys.stdin.read())
    out = []
    for row in req["trials"]:
        t = row["trial"]
        pair = (None, None)
        if t < len(EXPECT):
            e = EXPECT[t]
            pub = (0x9b3a6d8a, 0x00b50618, 7) if t == 0 else None
            if slice_check(e, pub):
                marker = ("ePrint 2026/2913 P2 slice %d matches the stored build" % t).encode().hex()
                pair = (marker, marker + "00")
        out.append({"trial": t, "message_a_hex": pair[0], "message_b_hex": pair[1]})
    sys.stdout.write(json.dumps({"schema_version": 1, "trials": out}, sort_keys=True))


if __name__ == "__main__":
    main()
