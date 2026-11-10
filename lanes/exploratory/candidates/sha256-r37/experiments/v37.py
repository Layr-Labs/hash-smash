#!/usr/bin/env python3
# v37.py - organizer experiments of the sha256-r37 variant-family package (proof.md Sections 5, 9 and 10).
# Standard library only, deterministic in the request seeds.  Reads one JSON request on stdin, writes one JSON
# document.  "v37-first-blocks": real first blocks M0 = the two RAND words of the counted program (SHAKE-256 of the
# trial seed); the counted program LISTING (proof.md Section 5, identical text) is executed instruction by instruction
# against an on-demand bucket and compared decision by decision with a direct computation; every valid pair's cells
# of rows -4..15 are checked; trial 0 runs the program end to end on the published pair's chaining value.
# "v37-sfs": reduced replicates of the q3 estimator of proof.md Section 6 whose tail draws a random variant of V per
# proposal; every success is rebuilt into a 37-step semi-free-start collision of that variant, verified, and found
# again by the counted program from its chaining value.
import hashlib, json, math, sys

M = 0xffffffff
W256 = (1 << 256) - 1
KC = (0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
      0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
      0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
      0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
      0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354)
IV = (0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19)
R = 37


def rotr(x, n): return ((x >> n) | (x << (32 - n))) & M
def S0(x): return rotr(x, 2) ^ rotr(x, 13) ^ rotr(x, 22)
def S1(x): return rotr(x, 6) ^ rotr(x, 11) ^ rotr(x, 25)
def s0(x): return rotr(x, 7) ^ rotr(x, 18) ^ (x >> 3)
def s1(x): return rotr(x, 17) ^ rotr(x, 19) ^ (x >> 10)
def IF(x, y, z): return (x & y) ^ (~x & z & M)
def MAJ(x, y, z): return (x & y) ^ (x & z) ^ (y & z)


def expand(w16, r=R):
    w = list(w16)
    for i in range(16, r):
        w.append((s1(w[i - 2]) + w[i - 7] + s0(w[i - 15]) + w[i - 16]) & M)
    return w


def steps(cv, w, r=R):
    A = {-1: cv[0], -2: cv[1], -3: cv[2], -4: cv[3]}
    E = {-1: cv[4], -2: cv[5], -3: cv[6], -4: cv[7]}
    for i in range(r):
        E[i] = (A[i - 4] + E[i - 4] + S1(E[i - 1]) + IF(E[i - 1], E[i - 2], E[i - 3]) + KC[i] + w[i]) & M
        A[i] = (E[i] - A[i - 4] + S0(A[i - 1]) + MAJ(A[i - 1], A[i - 2], A[i - 3])) & M
    return A, E


def F37(cv, w16):
    A, E = steps(cv, expand(w16))
    return tuple((c + o) & M for c, o in zip(cv, (A[36], A[35], A[34], A[33], E[36], E[35], E[34], E[33])))


def pack(ws):
    v = 0
    for w in ws: v = (v << 32) | w
    return v


def unpack(v, n): return [(v >> (32 * (n - 1 - i))) & M for i in range(n)]


# the 37-step characteristic of ePrint 2026/1120 (rows with a non-'=' cell; i: (A_i, E_i, W_i), MSB first, a
# shorter string is padded with '=')
CHS = {4: ("", "000", ""), 5: ("", "111=0=====1==0=====01===++01====", ""),
       6: ("=nu", "uuu=1011=00=10111=0111=0++1011==", "==n"),
       7: ("==========n====n====n======n====", "10n=u01001n00n00010nu110unuu0001", "=====u===u==========n"),
       8: ("", "011=1n+1=n11u1101=001u1u1010=u=1", "==u"),
       9: ("", "1=0110+=001=1100=+110100111u=0=+", "=====u=u=======n===u==n=u=n=u=n="),
       10: ("======u===========u", "10n001u110101==01+u1101011=1110+", "============n======u=n"),
       11: ("====u=====u=========u=n====u==n=", "=01un000011101=n0n0u1uu101011u1u", ""),
       12: ("=nu", "01101uuuuunu010110110n1u0u0uu0n0", ""),
       13: ("====u=========u=u=======n==u====", "0+10n110111unn+0n101110110001001", ""),
       14: ("======u=n=======n", "=+0=1000000111+=1==1n010u0=0101=", "=0===u===n=1=1====1=u=1=====1=1="),
       15: ("", "=u==01===n=011n01==u0=u=1==+====", "==u"),
       16: ("==u", "=0=====+00===11=+==01=0=0==+====", ""), 17: ("", "=0=====+01===u1=+==0==1===1u====", ""),
       18: ("", "==10===uu====0==n===111===01==1=", ""), 19: ("", "==1====00====1==0==========1====", ""),
       20: ("", "==u====10=======1===00==========", ""), 21: ("", "==0", ""),
       22: ("", "==1", "=====0=nn=====1=u=1"), 24: ("", "", "==n")}


def masks(s):
    eq = u = n = z = o = 0
    for p, c in enumerate((s + "=" * 32)[:32]):
        b = 1 << (31 - p)
        if c in "=+": eq |= b
        elif c == "u": u |= b
        elif c == "n": n |= b
        elif c == "0": z |= b
        else: o |= b
    return eq, u, n, z, o


CM = {i: tuple(masks(CHS.get(i, ("", "", ""))[j]) for j in range(3)) for i in range(-4, R)}
PLUS = []                                   # '+' cells pair vertically in E: E_r[b] = E_{r+1}[b]
for b in range(32):
    rs = sorted(i for i, t in CHS.items() if len(t[1]) == 32 and t[1][31 - b] == "+")
    PLUS += [(rs[j], b) for j in range(0, len(rs), 2)]


def cell(m, x, y):
    eq, u, n, z, o = m
    return not ((x ^ y) & eq) and (x & u) == u and not (y & u) and not (x & n) and (y & n) == n \
        and not ((x | y) & z) and (x & y & o) == o


def rows_ok(cv, wx, wy, lo, hi, skip_w=(6, 7)):
    Wx, Wy = expand(wx, hi + 1), expand(wy, hi + 1)
    Ax, Ex = steps(cv, Wx, hi + 1)
    Ay, Ey = steps(cv, Wy, hi + 1)
    for i in range(lo, hi + 1):
        m = CM[i]
        if not (cell(m[0], Ax[i], Ay[i]) and cell(m[1], Ex[i], Ey[i])):
            return False
        if i >= 0 and i not in skip_w and not cell(m[2], Wx[i], Wy[i]):
            return False
        if any(r + 1 == i and (Ex[r] ^ Ex[i]) >> b & 1 for (r, b) in PLUS):
            return False
    return True


def h2w(s): return [int(t, 16) for t in s.split()]


PCV = tuple(h2w("63b4986c 35d83dc0 c98894e4 784e08fc 78a7f752 5ed877a8 315a2db3 d5614eb4"))
PMY = h2w("4d7f86ff 32ece589 d8accfc4 2cc2e433 068b5b34 eba68a28 2fe12cad 6aa26b0c 9f0d78e1 681b8277 faa9c7e0 "
          "56aed439 cc2dbbc2 dd2ba0fc b95d377b 5dd43a81")
PMX = h2w("4d7f86ff 32ece589 d8accfc4 2cc2e433 068b5b34 eba68a28 0fe12cad 6ee2630c bf0d78e1 6d1a90dd faa1d3e0 "
          "56aed439 cc2dbbc2 dd2ba0fc bd1d3f7b 7dd43a81")
PH = tuple(h2w("a856d46e 4b46eb28 4935248c 92a2fc98 e0fb2610 10a9951f 54264f5b 80954580"))
D6, D7, T6, T7 = 0x20000000, 0xfbc00800, 0x03c00800, 0x017f8000
W14X, W14Y = 0xbd1d3f7b, 0xb95d377b
LW15 = [hi | mid | lo for hi in (0x7dd40000, 0xfdb40000) for mid in (0x1680, 0x1a80, 0x3680, 0x3a80)
        for lo in (0x00, 0x01, 0x20, 0x21)]
VIABLE = [l for l in range(32) if l not in (0, 2, 16, 18)]
NF6 = 287309824


def inF(w, d, t): return ((s0((w + d) & M) - s0(w)) & M) == t


# F7 is the disjoint union of two affine spaces (exhaustive count): F7a = {w26 = w22 = 1, w11 = 0, w0 = w28, w30 = w9,
# w1 = w18} (2^26 words) and F7b = 08800800 + span of the 20 vectors below (2^20 words).
F7A_OFF, F7B_OFF = 0x04400000, 0x08800800
F7A_BASIS = [1 << b for b in range(32) if b not in (26, 22, 11, 0, 28, 30, 9, 1, 18)] + \
    [(1 << 0) | (1 << 28), (1 << 30) | (1 << 9), (1 << 1) | (1 << 18)]
F7B_BASIS = [0x80000400, 0x40000200, 0x20040002, 0x10000001, 0x02000000, 0x01000000, 0x00200000, 0x00100000,
             0x00080004, 0x00020000, 0x00010000, 0x00008000, 0x00004000, 0x00002000, 0x00000100, 0x00000080,
             0x00000040, 0x00000020, 0x00000010, 0x00000008]


def draw_F7(rnd):
    """Exactly uniform on F7: x uniform on [0, 2^26 + 2^20) by rejection from 27 bits, then the affine part."""
    while True:
        x = rnd.u32() >> 5
        if x < (1 << 26) + (1 << 20):
            break
    off, basis = (F7A_OFF, F7A_BASIS) if x < 1 << 26 else (F7B_OFF, F7B_BASIS)
    x &= (1 << 26) - 1
    w = off
    for v in basis:
        if x & 1: w ^= v
        x >>= 1
    return w


class Setup:
    def __init__(self):
        assert F37(PCV, PMX) == PH == F37(PCV, PMY) and PMX != PMY
        assert rows_ok(PCV, PMX, PMY, -4, 36, skip_w=()) and LW15[13] == PMX[15]
        self.Wx, self.Wy = expand(PMX), expand(PMY)
        self.Ax, self.Ex = steps(PCV, self.Wx)
        self.Ay, self.Ey = steps(PCV, self.Wy)
        A, E = self.Ax, self.Ex
        self.C8X = (E[8] - A[4] - S1(E[7]) - IF(E[7], E[6], E[5]) - KC[8]) & M
        self.C8Y = (self.Ey[8] - self.Ay[4] - S1(self.Ey[7]) - IF(self.Ey[7], self.Ey[6], self.Ey[5]) - KC[8]) & M
        self.A0B = (A[0] - E[4]) & M
        self.c6 = (E[6] - 2 * A[2] + S0(A[1]) - S1(E[5]) - KC[6]) & M
        self.T8 = (s0(self.Wy[8]) - s0(self.Wx[8])) & M
        self.C16, self.Q17, self.E15 = [], [], []
        for w15 in LW15:
            Ax, Ex = steps(PCV, expand(list(PMX[:14]) + [W14X, w15], 16), 16)
            self.E14 = Ex[14]
            self.E15.append(Ex[15])
            self.C16.append((Ax[12] + Ex[12] + S1(Ex[15]) + IF(Ex[15], Ex[14], Ex[13]) + KC[16] + s1(W14X) + PMX[9]) & M)
            self.Q17.append((s1(w15) + PMX[10]) & M)
        m16, m17 = CM[16][1], CM[17][1]
        self.F16 = m16[1] | m16[2] | m16[3] | m16[4] | 1 << 4
        self.V16 = [m16[1] | m16[4] | (e15 & 1 << 4) for e15 in self.E15]
        self.F17, self.V17, self.P17 = m17[1] | m17[2] | m17[3] | m17[4], m17[1] | m17[4], 1 << 24 | 1 << 15
        self.R17 = (A[13] + E[13] + KC[17]) & M
        assert len(F7A_BASIS) == 26 and len(F7B_BASIS) == 20 and inF(F7A_OFF, D7, T7) and inF(F7B_OFF, D7, T7)
        for v in F7A_BASIS: assert inF(F7A_OFF ^ v, D7, T7)
        for v in F7B_BASIS: assert inF(F7B_OFF ^ v, D7, T7) and not ((F7B_OFF ^ v) & 0x04400800) == 0x04400000

    def variant(self, j):
        """V (K = 2^18), proof.md Section 4.2: W8x(j) and E4'(j) = C8X - W8x(j)."""
        t = (j * 0x9E3779B1) & 0x7fffff
        w = 0xbc000000 | (t & 1) | ((t >> 1) & 0x3f) << 2 | ((t >> 7) & 0x1f) << 9 | ((t >> 12) & 0x7ff) << 15
        if not w >> 12 & 1: w |= 2
        if not w >> 25 & 1: w |= 1 << 8
        if w >> 18 & 1: w |= 1 << 14
        return (self.C8X - w) & M

    def valid_variant(self, e4):
        w8x, w8y = (self.C8X - e4) & M, (self.C8Y - e4) & M
        return e4 < 1 << 29 and w8x ^ w8y == 1 << 29 and w8x >> 29 & 1 and (s0(w8y) - s0(w8x)) & M == self.T8

    def consts(self, e4):
        A, E = self.Ax, self.Ex
        a0 = (e4 + self.A0B) & M
        c7 = (E[7] - 2 * A[3] + S0(A[2]) + MAJ(A[2], A[1], a0) - S1(E[6]) - IF(E[6], E[5], e4) - KC[7]) & M
        k3 = (A[3] - S0(A[2]) - MAJ(A[2], A[1], a0)) & M
        return a0, c7, k3

    def words(self, cv, e4, l):
        """Lemma 1: the second-block words of both members connecting cv to S'(e4), with l in L*."""
        A, E = dict(self.Ax), dict(self.Ex)
        A[0], E[4] = (e4 + self.A0B) & M, e4
        A.update({-1: cv[0], -2: cv[1], -3: cv[2], -4: cv[3]})
        E.update({-1: cv[4], -2: cv[5], -3: cv[6], -4: cv[7]})
        for i in (3, 2, 1, 0):
            E[i] = (A[i] + A[i - 4] - S0(A[i - 1]) - MAJ(A[i - 1], A[i - 2], A[i - 3])) & M
        W = [(E[i] - A[i - 4] - E[i - 4] - S1(E[i - 1]) - IF(E[i - 1], E[i - 2], E[i - 3]) - KC[i]) & M for i in range(8)]
        wx = W + [(self.C8X - e4) & M] + list(self.Wx[9:14]) + [W14X, LW15[l]]
        wy = W[:6] + [(W[6] + D6) & M, (W[7] + D7) & M, (self.C8Y - e4) & M] + list(self.Wy[9:14]) + \
            [W14Y, (LW15[l] - (1 << 29)) & M]
        return wx, wy


# ---------------------------------------------------------------- the counted program (proof.md Section 5.2)
# One instruction per line: "op dst a b [c]"; a register name, an integer immediate or a symbol of SYM.
# Each executed line costs one primitive, except: b<cond> = compare + conditional branch (2); call = one target
# compression (1 unit) plus 4 operand moves (4).  Block labels (CV, ENTRY, HIT, RARE, BIT, FINAL, SUCCESS) only
# attribute the count.  BIT is instantiated once per viable l (symbols with suffix _l).
LISTING = """
CV  TOP:  rand r0
CV        rand r1
CV        call Y IVW r0 r1
CV        shr a1 Y 224
CV        shr t Y 192
CV        and a2 t M32
CV        shr t Y 160
CV        and a3 t M32
CV        shr t Y 128
CV        and a4 t M32
CV        shr t Y 96
CV        and e1 t M32
CV        shr t Y 64
CV        and e2 t M32
CV        shr t Y 32
CV        and e3 t M32
CV        and e4 Y M32
CV        add q a1 CNT0
CV        ld n q
CV        add Ve Ve n
CV        beq n 0 NEXT
CV        shr x a1 2
CV        shl y a1 30
CV        or u x y
CV        shr x a1 13
CV        shl y a1 19
CV        or v x y
CV        xor u u v
CV        shr x a1 22
CV        shl y a1 10
CV        or v x y
CV        xor u u v
CV        and S0a u M32
CV        and x a1 a2
CV        or y a1 a2
CV        and y a3 y
CV        or MJ1 x y
CV        shr x e1 6
CV        shl y e1 26
CV        or u x y
CV        shr x e1 11
CV        shl y e1 21
CV        or v x y
CV        xor u u v
CV        shr x e1 25
CV        shl y e1 7
CV        or v x y
CV        xor u u v
CV        and S1e u M32
CV        xor x e2 e3
CV        and x e1 x
CV        xor IF1 e3 x
CV        sub G0 0 S0a
CV        sub G0 G0 MJ1
CV        sub G0 G0 e4
CV        sub G0 G0 S1e
CV        sub G0 G0 IF1
CV        sub G0 G0 K0
CV        sub Ec a4 S0a
CV        sub Ec Ec MJ1
CV        xor Xe e1 e2
CV        or Ao a1 a2
CV        and Aa a1 a2
CV        sub C1 A1MK1 e3
CV        add q a1 IDX0
CV        ld p q
ENTRY L:  ld e p
ENTRY     add p p 1
ENTRY     sub w e a2
ENTRY     ld t w
ENTRY     beq t 0 L
HIT       beq t 2 NEXT
HIT       add q p DA0M1
HIT       ld a0 q
HIT       add q p DS0M1
HIT       ld sa0 q
HIT       add W0 a0 G0
HIT       add E0 a0 Ec
HIT       and E0 E0 M32
HIT       shr x E0 6
HIT       shl y E0 26
HIT       or u x y
HIT       shr x E0 11
HIT       shl y E0 21
HIT       or v x y
HIT       xor u u v
HIT       shr x E0 25
HIT       shl y E0 7
HIT       or v x y
HIT       xor S1E0 u v
HIT       and x E0 Xe
HIT       xor IFE e2 x
HIT       and x a0 Ao
HIT       or MJ Aa x
HIT       sub W1 C1 sa0
HIT       sub W1 W1 MJ
HIT       sub W1 W1 S1E0
HIT       sub W1 W1 IFE
HIT       and W1 W1 M32
HIT       shr x W1 7
HIT       shl y W1 25
HIT       or u x y
HIT       shr x W1 18
HIT       shl y W1 14
HIT       or v x y
HIT       xor u u v
HIT       shr x W1 3
HIT       xor s0w u x
HIT       add X0 s0w W0
HIT       and X X0 M31
HIT       add q X T3B
HIT       ld m q
HIT       add Vh Vh 1
HIT       bne m 0 RARE
HIT       jmp L
RARE RARE: add Vr Vr 1
RARE      add E1 a3 A1
RARE      sub E1 E1 sa0
RARE      sub E1 E1 MJ
RARE      and E1 E1 M32
RARE      or x a0 a1
RARE      and x x A1
RARE      and y a0 a1
RARE      or MJ2 x y
RARE      add E2 a2 A2MS0A1
RARE      sub E2 E2 MJ2
RARE      and E2 E2 M32
RARE      shr x E1 6
RARE      shl y E1 26
RARE      or u x y
RARE      shr x E1 11
RARE      shl y E1 21
RARE      or v x y
RARE      xor u u v
RARE      shr x E1 25
RARE      shl y E1 7
RARE      or v x y
RARE      xor S1E1 u v
RARE      xor x E0 e1
RARE      and x E1 x
RARE      xor IFE1 e1 x
RARE      sub W2 E2 a2
RARE      sub W2 W2 e2
RARE      sub W2 W2 S1E1
RARE      sub W2 W2 IFE1
RARE      sub W2 W2 K2
RARE      and W2 W2 M32
RARE      shr x W2 7
RARE      shl y W2 25
RARE      or u x y
RARE      shr x W2 18
RARE      shl y W2 14
RARE      or v x y
RARE      xor u u v
RARE      shr x W2 3
RARE      xor u u x
RARE      add R17 u W1
RARE      @BITS
RARE      jmp L
BIT  B_l: shr x m L_l
BIT       and x x 1
BIT       beq x 0 N_l
BIT       add Vb Vb 1
BIT       add E16 X0 C16_l
BIT       and E16 E16 M32
BIT       add W17 R17 Q17_l
BIT       shr x E16 6
BIT       shl y E16 26
BIT       or u x y
BIT       shr x E16 11
BIT       shl y E16 21
BIT       or v x y
BIT       xor u u v
BIT       shr x E16 25
BIT       shl y E16 7
BIT       or v x y
BIT       xor S1E16 u v
BIT       and x E16 X1514_l
BIT       xor IF2 x E14
BIT       add E17 W17 R17C
BIT       add E17 E17 S1E16
BIT       add E17 E17 IF2
BIT       and E17 E17 M32
BIT       and x E17 F17
BIT       bne x V17 N_l
BIT       xor x E17 E16
BIT       and x x P17
BIT       bne x 0 N_l
FINAL     add Vf Vf 1
FINAL     and x a0 A21O
FINAL     or x x A21A
FINAL     add E3 a1 A3MS0A2
FINAL     sub E3 E3 x
FINAL     and E3 E3 M32
FINAL     sub E4p a0 A0B
FINAL     and E4p E4p M32
FINAL     shr x E2 6
FINAL     shl y E2 26
FINAL     or u x y
FINAL     shr x E2 11
FINAL     shl y E2 21
FINAL     or v x y
FINAL     xor u u v
FINAL     shr x E2 25
FINAL     shl y E2 7
FINAL     or v x y
FINAL     xor S1E2 u v
FINAL     xor x E1 E0
FINAL     and x E2 x
FINAL     xor x E0 x
FINAL     sub W3 E3 a1
FINAL     sub W3 W3 e1
FINAL     sub W3 W3 S1E2
FINAL     sub W3 W3 x
FINAL     sub W3 W3 K3
FINAL     and W3 W3 M32
FINAL     shr x E3 6
FINAL     shl y E3 26
FINAL     or u x y
FINAL     shr x E3 11
FINAL     shl y E3 21
FINAL     or v x y
FINAL     xor u u v
FINAL     shr x E3 25
FINAL     shl y E3 7
FINAL     or v x y
FINAL     xor S1E3 u v
FINAL     xor x E2 E1
FINAL     and x E3 x
FINAL     xor x E1 x
FINAL     sub W4 E4p a0
FINAL     sub W4 W4 E0
FINAL     sub W4 W4 S1E3
FINAL     sub W4 W4 x
FINAL     sub W4 W4 K4
FINAL     and W4 W4 M32
FINAL     shr x E4p 6
FINAL     shl y E4p 26
FINAL     or u x y
FINAL     shr x E4p 11
FINAL     shl y E4p 21
FINAL     or v x y
FINAL     xor u u v
FINAL     shr x E4p 25
FINAL     shl y E4p 7
FINAL     or v x y
FINAL     xor S1E4 u v
FINAL     xor x E3 E2
FINAL     and x E4p x
FINAL     xor x E2 x
FINAL     sub W5 E5MA1K5 E1
FINAL     sub W5 W5 S1E4
FINAL     sub W5 W5 x
FINAL     and W5 W5 M32
FINAL     sub W6 e a2
FINAL     and W6 W6 M32
FINAL     and x a0 A21O
FINAL     or x x A21A
FINAL     and y E4p NE6
FINAL     add W7 C7C x
FINAL     sub W7 W7 y
FINAL     sub W7 W7 a1
FINAL     and W7 W7 M32
FINAL     sub W8x C8X E4p
FINAL     sub W8y C8Y E4p
FINAL     and W0 W0 M32
FINAL     shl x W0 32
FINAL     or x x W1
FINAL     shl x x 32
FINAL     or x x W2
FINAL     shl x x 32
FINAL     or x x W3
FINAL     shl x x 32
FINAL     or x x W4
FINAL     shl x x 32
FINAL     or x x W5
FINAL     shl hx x 64
FINAL     shl y W6 32
FINAL     or y y W7
FINAL     or x0 hx y
FINAL     shl y W8x 224
FINAL     or x1 y CW1X_l
FINAL     add u W6 D6
FINAL     and u u M32
FINAL     add v W7 D7
FINAL     and v v M32
FINAL     shl u u 32
FINAL     or u u v
FINAL     or y0 hx u
FINAL     shl y W8y 224
FINAL     or y1 y CW1Y_l
FINAL     call Zx Y x0 x1
FINAL     call Zy Y y0 y1
FINAL     bne Zx Zy N_l
FINAL     jmp SUCCESS_l
BIT  N_l: nop
CV  NEXT: bgt Ve EMAX HALT
CV        bgt Vh HMAX HALT
CV        bgt Vr RMAX HALT
CV        bgt Vb BMAX HALT
CV        bgt Vf FMAX HALT
CV        add i i 1
CV        blt i N TOP
"""
# SUCCESS (once): digests of both 128-byte messages from the IV (6 compressions), compare, output, halt; it is
# charged 6 units + 64 operations in the ledger and is not interpreted here.


ALU = {"add": lambda a, b: a + b, "sub": lambda a, b: a - b, "and": lambda a, b: a & b,
       "or": lambda a, b: a | b, "xor": lambda a, b: a ^ b, "shl": lambda a, b: (a << b) if b < 256 else 0,
       "shr": lambda a, b: a >> b}


class Halt(Exception):
    pass


class Machine:
    """Interpreter of LISTING.  Memory: T6 at addresses [0, 2^34], CNT/IDX/entries/T3 at the bases of SYM."""
    def __init__(self, St, bucket, a1, Y0=None, rand=None):
        self.St, self.bucket, self.a1, self.Y0, self.randq = St, bucket, a1, Y0, list(rand or [])
        self.count = {b: 0 for b in ("CV", "ENTRY", "HIT", "RARE", "BIT", "FINAL")}
        self.units = 0
        self.final_equal = []          # (l, a0) of FINAL blocks whose two outputs agreed
        self.trace = []                # per hit: (a0, W1, X, m)
        St_ = St
        A, E = St_.Ax, St_.Ex
        self.sym = {"M32": M, "M31": 0x7fffffff, "CNT0": 1 << 35, "IDX0": 1 << 36, "T3B": 1 << 50,
                    "DA0M1": (1 << 47) - 1, "DS0M1": (1 << 48) - 1, "K0": KC[0], "K2": KC[2], "K3": KC[3], "K4": KC[4],
                    "A1MK1": (A[1] - KC[1]) & M, "A1": A[1], "A2MS0A1": (A[2] - S0(A[1])) & M,
                    "A3MS0A2": (A[3] - S0(A[2])) & M, "A21O": A[2] | A[1], "A21A": A[2] & A[1], "A0B": St_.A0B,
                    "E5MA1K5": (E[5] - A[1] - KC[5]) & M, "NE6": ~E[6] & M,
                    "C7C": (E[7] - 2 * A[3] + S0(A[2]) - S1(E[6]) - (E[6] & E[5]) - KC[7]) & M,
                    "C8X": St_.C8X, "C8Y": St_.C8Y, "D6": D6, "D7": D7, "E14": St_.E14, "R17C": St_.R17,
                    "F17": St_.F17, "V17": St_.V17, "P17": St_.P17, "IVW": pack(IV),
                    "EMAX": 1 << 200, "HMAX": 1 << 200, "RMAX": 1 << 200, "BMAX": 1 << 200, "FMAX": 1 << 200,
                    "N": 1}
        for l in VIABLE:
            self.sym.update({f"L_{l}": l, f"C16_{l}": St_.C16[l], f"Q17_{l}": St_.Q17[l],
                             f"X1514_{l}": St_.E15[l] ^ St_.E14,
                             f"CW1X_{l}": pack(list(St_.Wx[9:14]) + [W14X, LW15[l]]),
                             f"CW1Y_{l}": pack(list(St_.Wy[9:14]) + [W14Y, (LW15[l] - (1 << 29)) & M])})
        self.prog, self.lab = self.assemble()

    def assemble(self):
        main, tmpl = [], []
        for raw in LISTING.strip().splitlines():
            blk, rest = raw.split(None, 1)
            lab = None
            if rest.split()[0].endswith(":"):
                lab, rest = rest.split(None, 1)
                lab = lab[:-1]
            (tmpl if blk in ("BIT", "FINAL") else main).append((blk, lab, rest.split()))
        prog = []
        for blk, lab, toks in main:
            if toks == ["@BITS"]:
                for l in VIABLE:
                    sub = lambda s: s.replace("_l", f"_{l}")
                    prog += [(b2, None if lb2 is None else sub(lb2), [sub(t) for t in t2]) for b2, lb2, t2 in tmpl]
                continue
            prog.append((blk, lab, toks))
        return prog, {ln[1]: i for i, ln in enumerate(prog) if ln[1]}

    def val(self, R, a):
        if a in R: return R[a]
        if a in self.sym: return self.sym[a]
        if a.lstrip("-").isdigit(): return int(a)
        return 0                       # registers start at zero

    def load(self, addr):
        St = self.St
        if addr <= 1 << 34:
            return 2 if addr >= 1 << 33 else (1 if inF(addr & M, D6, T6) else 0)
        if addr == (1 << 35) + self.a1: return len(self.bucket) - 1
        if addr == (1 << 36) + self.a1: return 1 << 40
        if (1 << 40) <= addr < (1 << 40) + len(self.bucket): return self.bucket[addr - (1 << 40)][0]
        if (1 << 47) + (1 << 40) <= addr < (1 << 47) + (1 << 40) + len(self.bucket):
            return self.bucket[addr - (1 << 47) - (1 << 40)][1]
        if (1 << 48) + (1 << 40) <= addr < (1 << 48) + (1 << 40) + len(self.bucket):
            return self.bucket[addr - (1 << 48) - (1 << 40)][2]
        if (1 << 50) <= addr < (1 << 50) + (1 << 31):
            x, m = addr - (1 << 50), 0
            for l in VIABLE:
                if ((St.C16[l] + x) & St.F16) == St.V16[l]: m |= 1 << l
            return m
        raise ValueError(hex(addr))

    def run(self):
        R, pc, prog = {}, self.lab["TOP"], self.prog
        try:
            while pc < len(prog):                     # falling off the end = halt after the last CV
                blk, _, tk = prog[pc]
                op = tk[0]
                pc += 1
                if op == "nop":
                    continue
                self.count[blk] += 2 if op[0] == "b" else 1
                if op in ("add", "sub", "and", "or", "xor", "shl", "shr"):
                    a, b = self.val(R, tk[2]), self.val(R, tk[3])
                    R[tk[1]] = ALU[op](a, b) & W256
                elif op == "ld":
                    R[tk[1]] = self.load(self.val(R, tk[2]))
                elif op == "rand":
                    R[tk[1]] = self.randq.pop(0)
                elif op == "call":                       # one target compression: 1 unit + 4 operand moves
                    self.count[blk] += 3
                    self.units += 1
                    out = F37(unpack(self.val(R, tk[2]), 8), unpack(self.val(R, tk[3]), 8) + unpack(self.val(R, tk[4]), 8))
                    if tk[1] == "Y" and self.Y0 is not None:
                        out = self.Y0                    # test hook: start from a given chaining value
                    R[tk[1]] = pack(out)
                elif op == "jmp":
                    if tk[1].startswith("SUCCESS_"):     # SUCCESS would verify, output and halt; record and go on
                        l = tk[1][8:]
                        self.final_equal.append((int(l), R["a0"]))
                        pc = self.lab["N_" + l]
                    else:
                        pc = self.lab[tk[1]]
                else:
                    a, b = self.val(R, tk[1]), self.val(R, tk[2])
                    if op == "bne" and tk[3] == "RARE":
                        self.trace.append((R["a0"], R["W1"], R["X"], R["m"]))
                    if {"beq": a == b, "bne": a != b, "bgt": a > b, "blt": a < b}[op]:
                        if tk[3] == "HALT":
                            raise Halt()
                        pc = self.lab[tk[3]]
        except Halt:
            pass
        self.R = R
        return self


def bucket_for(St, a1, Vlist):
    """Bucket a1 exactly as the preprocessing builds it (proof.md Section 5.1): (u + 2^32, a0, S0(a0))."""
    b = []
    for e4 in Vlist:
        a0, c7, k3 = St.consts(e4)
        if inF((c7 - a1) & M, D7, T7):
            u = (St.c6 + MAJ(St.Ax[1], a0, a1) - IF(St.Ex[5], e4, (k3 + a1) & M)) & M
            b.append((u + (1 << 32), a0, S0(a0), e4))
    b.append((1 << 34, 0, 0, None))
    return b


def reference(St, cv, bucket):
    """Direct computation for the same bucket: the valid entries and their (a0, W1, X, l-mask)."""
    out = []
    for (u, a0, sa0, e4) in bucket[:-1]:
        wx, wy = St.words(cv, e4, 13)
        if not inF(wx[6], D6, T6):
            continue
        assert inF(wx[7], D7, T7) and (u - (1 << 32) - cv[1]) & M == wx[6]
        X = (s0(wx[1]) + wx[0]) & 0x7fffffff
        m = sum(1 << l for l in VIABLE if ((St.C16[l] + X) & St.F16) == St.V16[l])
        out.append((a0, wx[1], X, m, e4))
    return out


def shake(seed, tag, n): return hashlib.shake_256(bytes.fromhex(seed) + tag).digest(n)


def first_blocks(St, req):
    Vsub = [St.variant(j) for j in range(1 << 14)]     # the first 2^14 elements of V (time budget)
    bad = sum(1 for e4 in Vsub if not St.valid_variant(e4))
    out = []
    for tr in req["trials"]:
        rec = {"trial": tr["trial"], "message_a_hex": None, "message_b_hex": None}
        t = tr["trial"]
        if 1 <= t <= 64:
            r = shake(tr["seed"], b"m0", 64)
            r0, r1 = int.from_bytes(r[:32], "big"), int.from_bytes(r[32:], "big")
            m0 = unpack(r0, 8) + unpack(r1, 8)
            cv = F37(IV, m0)
            bucket = bucket_for(St, cv[0], Vsub)
            mc = Machine(St, bucket, cv[0], rand=[r0, r1]).run()
            ref = reference(St, cv, bucket)
            mism = int([tuple(x) for x in mc.trace] != [x[:4] for x in ref])
            cells = r16 = 0
            hv = []                                    # W16..W22 (l = 13) of each valid pair, for H3
            for idx, x in enumerate(ref):
                l = VIABLE[idx % 28]
                wx, wy = St.words(cv, x[4], l)
                cells += not rows_ok(cv, wx, wy, -4, 15)
                r16 += rows_ok(cv, wx, wy, 16, 16)
                if idx < 64:                           # first 64 valid pairs of the block
                    hv.append(pack(expand(St.words(cv, x[4], 13)[0], 23)[16:23]))
            hn = hs = hs2 = 0
            hmin = 224
            for i in range(len(hv)):                   # pairwise Hamming distances over 224 bits
                for j in range(i):
                    d = bin(hv[i] ^ hv[j]).count("1")
                    hn += 1; hs += d; hs2 += d * d; hmin = min(hmin, d)
            nr = sum(1 for x in ref if x[3])
            nb = sum(bin(x[3]).count("1") for x in ref)
            ne = len(bucket) - 1
            nf = mc.R.get("Vf", 0)                     # FINAL blocks entered
            ops_ok = mc.units == 1 + 2 * nf and mc.count["CV"] == (83 if ne else 38) and \
                mc.count["ENTRY"] == (6 * (ne + 1) if ne else 0) and \
                mc.count["HIT"] == ((2 + 46 * (len(ref) - nr) + 45 * nr) if ne else 0) and \
                mc.count["RARE"] == 43 * nr and 112 * nr + 24 * nb <= mc.count["BIT"] <= 112 * nr + 28 * nb and \
                113 * nf <= mc.count["FINAL"] <= 114 * nf
            rec["observations"] = {"bucket_entries": ne, "valid_pairs": len(ref), "decision_mismatch": mism,
                                   "cells_rows_m4_15_failures": cells, "row16_pass": r16, "rare": nr, "bits": nb,
                                   "ops_total": sum(mc.count.values()), "ops_ok": int(ops_ok),
                                   "hamming_pairs": hn, "hamming_sum": hs, "hamming_sumsq": hs2, "hamming_min": hmin,
                                   "variant_failures": bad}
            if ref and not mism and not cells and ops_ok:
                wx, wy = St.words(cv, ref[0][4], 13)
                rec["message_a_hex"] = b"".join(w.to_bytes(4, "big") for w in m0 + wx).hex()
                rec["message_b_hex"] = b"".join(w.to_bytes(4, "big") for w in m0 + wy).hex()
        elif t == 0:
            # end to end: the published pair's CV1 with a bucket holding the published S (E4 = 1b2d044e) and V'
            e4p = St.Ex[4]
            b = bucket_for(St, PCV[0], [e4p] + Vsub[:4096])
            mc = Machine(St, b, PCV[0], Y0=PCV, rand=[0, 0]).run()
            ok = any(l == 13 and a0 == St.Ax[0] for (l, a0) in mc.final_equal)
            rec["observations"] = {"end_to_end_final_equal": len(mc.final_equal), "published_pair_found": int(ok),
                                   "ops_final": mc.count["FINAL"], "units": mc.units}
            if ok:
                rec["message_a_hex"] = b"".join(w.to_bytes(4, "big") for w in list(PCV) + PMX).hex()
                rec["message_b_hex"] = b"".join(w.to_bytes(4, "big") for w in list(PCV) + PMY).hex()
        out.append(rec)
    return out


# ---------------------------------------------------------------- q3 replica with random variants (Section 6)
class Rng:
    def __init__(self, key): self.key, self.ctr, self.buf, self.pos = key, 0, b"", 0
    def u32(self):
        if self.pos + 4 > len(self.buf):
            self.buf, self.pos = hashlib.shake_256(self.key + self.ctr.to_bytes(8, "big")).digest(1 << 14), 0
            self.ctr += 1
        v = int.from_bytes(self.buf[self.pos:self.pos + 4], "big")
        self.pos += 4
        return v
    def below(self, n): return (self.u32() * n) >> 32


def row(p, i, ex, dw):
    Ax, Ex, Wx, Ay, Ey, Wy = p
    wx = (ex - (Ax[i - 4] + Ex[i - 4] + S1(Ex[i - 1]) + IF(Ex[i - 1], Ex[i - 2], Ex[i - 3]) + KC[i])) & M
    wy = (wx + dw) & M
    ey = (Ay[i - 4] + Ey[i - 4] + S1(Ey[i - 1]) + IF(Ey[i - 1], Ey[i - 2], Ey[i - 3]) + KC[i] + wy) & M
    m = CM[i]
    if not (cell(m[1], ex, ey) and cell(m[2], wx, wy)):
        return None
    ax = (ex - Ax[i - 4] + S0(Ax[i - 1]) + MAJ(Ax[i - 1], Ax[i - 2], Ax[i - 3])) & M
    ay = (ey - Ay[i - 4] + S0(Ay[i - 1]) + MAJ(Ay[i - 1], Ay[i - 2], Ay[i - 3])) & M
    if not cell(m[0], ax, ay) or any(r + 1 == i and (Ex[r] ^ ex) >> b & 1 for (r, b) in PLUS):
        return None
    q = tuple(dict(d) for d in p)
    for d, v in zip(q, (ax, ex, wx, ay, ey, wy)): d[i] = v
    return q


def rebuild(St, p, l, w6x, w7x, e4):
    """W0..W5 by the inverse expansion, CV1 by inverting steps 7..0 from S'(e4) (proof.md Lemma 1)."""
    W = {i: p[2][i] for i in range(16, 22)}
    W.update({6: w6x, 7: w7x, 8: (St.C8X - e4) & M, 14: W14X, 15: LW15[l]})
    for j in range(9, 14): W[j] = St.Wx[j]
    for j in (5, 4, 3, 2, 1, 0):
        W[j] = (W[j + 16] - s1(W[j + 14]) - W[j + 9] - s0(W[j + 1])) & M
    A, E = dict(St.Ax), dict(St.Ex)
    A[0], E[4] = (e4 + St.A0B) & M, e4
    for i in range(7, -1, -1):
        A[i - 4] = (E[i] - A[i] + S0(A[i - 1]) + MAJ(A[i - 1], A[i - 2], A[i - 3])) & M
        E[i - 4] = (E[i] - A[i - 4] - S1(E[i - 1]) - IF(E[i - 1], E[i - 2], E[i - 3]) - KC[i] - W[i]) & M
    return (A[-1], A[-2], A[-3], A[-4], E[-1], E[-2], E[-3], E[-4])


def replicate(St, l, rnd, nV):
    """Reduced SMC replicate (NP 64; children 8, 32, 8, 8, 2, 4; 384 tail proposals per particle)."""
    wx = list(St.Wx[:14]) + [W14X, LW15[l]]
    wy = list(St.Wy[:14]) + [W14Y, (LW15[l] - (1 << 29)) & M]
    Ax, Ex = steps(PCV, expand(wx, 16), 16)
    Ay, Ey = steps(PCV, expand(wy, 16), 16)
    dW = {16: (s1(wy[14]) - s1(wx[14]) + wy[9] - wx[9]) & M, 17: (s1(wy[15]) - s1(wx[15]) + wy[10] - wx[10]) & M,
          18: 0, 19: 0, 20: 0, 21: (wy[14] - wx[14] + T6) & M}
    keep = lambda d: {i: d[i] for i in range(12, 16)}
    NP, TP = 64, 384
    P = [(keep(Ax), keep(Ex), {}, keep(Ay), keep(Ey), {})] * NP
    children = {16: 8, 17: 32, 18: 8, 19: 8, 20: 2, 21: 4}
    log2est = 0.0
    for i in range(16, 22):
        m = CM[i][1]
        fix, val = m[1] | m[2] | m[3] | m[4], m[1] | m[4]
        pm = sum(1 << b for (r, b) in PLUS if r + 1 == i)
        surv, props = [], 0
        for p in P:
            for _ in range(children[i]):
                props += 1
                q = row(p, i, (rnd.u32() & ~(fix | pm) & M) | val | (p[1][i - 1] & pm), dW[i])
                if q: surv.append(q)
        if not surv:
            return {"l": l, "log2_estimate": None, "successes": 0, "verified": 0, "distinct_variants": 0, "refind_attempts": 0,
                "refound_by_counted_program": 0}, None
        log2est += math.log2(len(surv) / props) - bin(fix | pm).count("1")
        P = [surv[rnd.below(len(surv))] for _ in range(NP)]
    m22 = CM[22][2]
    fix22, val22 = m22[1] | m22[2] | m22[3] | m22[4], m22[1] | m22[4]
    wgt = 2.0 ** (32 - bin(fix22).count("1")) / NF6
    wsum, succ, ver, found, tried, first, kinds = 0.0, 0, 0, 0, 0, None, set()
    for p in P:
        for _ in range(TP):
            w22x = (rnd.u32() & ~fix22 & M) | val22
            w7x = draw_F7(rnd)
            w6x = (w22x - s1(p[2][20]) - LW15[l] - s0(w7x)) & M
            if not inF(w6x, D6, T6):
                continue
            e4 = St.variant(rnd.below(nV))
            cv1 = rebuild(St, p, l, w6x, w7x, e4)
            mx, my = St.words(cv1, e4, l)
            if not rows_ok(cv1, mx, my, 16, 36, skip_w=()):
                continue
            succ += 1
            wsum += wgt
            if F37(cv1, mx) == F37(cv1, my) and mx != my and rows_ok(cv1, mx, my, -4, 36):
                ver += 1
                kinds.add(e4)
                if first is None: first = (cv1, mx, my)
                if tried < 2:          # the counted program finds it again from CV1 (bucket holding e4)
                    tried += 1
                    b = bucket_for(St, cv1[0], [e4])
                    mc = Machine(St, b, cv1[0], Y0=cv1, rand=[0, 0]).run()
                    found += any(a0 == (e4 + St.A0B) & M for (_, a0) in mc.final_equal)
    est = log2est + math.log2(wsum / (NP * TP)) if wsum else None
    return {"l": l, "log2_estimate": est, "successes": succ, "verified": ver, "distinct_variants": len(kinds),
            "refind_attempts": tried, "refound_by_counted_program": found}, first


def sfs(St, req):
    out = []
    for tr in req["trials"]:
        t = tr["trial"]
        rec = {"trial": t, "message_a_hex": None, "message_b_hex": None}
        if t < 10:
            res, first = replicate(St, VIABLE[(t * 11) % 28], Rng(shake(tr["seed"], b"smc", 32)), 1 << 18)
            rec["observations"] = {k: v for k, v in res.items() if v is not None}
            if first:
                cv1, mx, my = first
                rec["message_a_hex"] = b"".join(w.to_bytes(4, "big") for w in list(cv1) + mx).hex()
                rec["message_b_hex"] = b"".join(w.to_bytes(4, "big") for w in list(cv1) + my).hex()
        out.append(rec)
    return out


def main():
    req = json.loads(sys.stdin.read())
    St = Setup()
    trials = first_blocks(St, req) if req["experiment_id"] == "v37-first-blocks" else sfs(St, req)
    sys.stdout.write(json.dumps({"schema_version": 1, "trials": trials}, separators=(",", ":")))


if __name__ == "__main__":
    main()
