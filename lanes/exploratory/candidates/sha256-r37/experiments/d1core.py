#!/usr/bin/env python3
# d1core.py - counted program of the d1 package (sha256-r37-prefix-v1).
# The two-block collision attack of Li, Zhang, Li, Liu, Qian and Zhu, "Pushing Collision Attacks on SHA-2 to
# 39 Steps", IACR ePrint 2026/1120 (CC BY), in the memory-efficient framework of [LLWS26] (Li, Liu, Wang, Shi,
# CRYPTO 2026), with their characteristic (Table 15) and SFS pair (Table 17).  This file holds:
# the reduced SHA-256 (scalar reference), the characteristic cells, the SFS pairs, the Step-1 solution S read
# off the SFS pair, the exact freedom set L*, the counted bit-sliced first-block batch (256 lanes) with its Step-2
# filters, the counted rare path, the counted scalar Step 3 (early abort), the target verification, the attack driver
# with fixed caps, and the entry point of the two organizer experiments (stdin JSON -> stdout JSON): the
# first-block check and, for 37 steps, a reduced standard-library replica of smc.py.  Python 3.9+, stdlib.
import sys, json, hashlib, struct, math, random

M32 = 0xffffffff
WORD = (1 << 256) - 1
K = [0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,0xd807aa98,0x12835b01,
     0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,
     0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,
     0x06ca6351,0x14292967,0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,
     0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,0x19a4c116,0x1e376c08,
     0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,
     0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2]
IV = [0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19]
C_REF = {37: 2644, 38: 2728}

def ror(x, n): return ((x >> n) | (x << (32 - n))) & M32
def S0(x): return ror(x, 2) ^ ror(x, 13) ^ ror(x, 22)
def S1(x): return ror(x, 6) ^ ror(x, 11) ^ ror(x, 25)
def s0(x): return ror(x, 7) ^ ror(x, 18) ^ (x >> 3)
def s1(x): return ror(x, 17) ^ ror(x, 19) ^ (x >> 10)
def IF(x, y, z): return (x & y) ^ (~x & z & M32)
def MAJ(x, y, z): return (x & y) ^ (x & z) ^ (y & z)

def compress(cv, w16, R):
    """Target compression: R steps (0..R-1) of SHA-256 from chaining value cv, with feed-forward."""
    w = list(w16)
    for i in range(16, R): w.append((s1(w[i-2]) + w[i-7] + s0(w[i-15]) + w[i-16]) & M32)
    a, b, c, d, e, f, g, h = cv
    for i in range(R):
        t1 = (h + S1(e) + IF(e, f, g) + K[i] + w[i]) & M32
        t2 = (S0(a) + MAJ(a, b, c)) & M32
        a, b, c, d, e, f, g, h = (t1 + t2) & M32, a, b, c, (d + t1) & M32, e, f, g
    return [(x + y) & M32 for x, y in zip(cv, (a, b, c, d, e, f, g, h))]

def blocks(msg):
    """FIPS 180-4 padding; list of 16-word blocks."""
    n = len(msg)
    p = msg + b'\x80' + b'\x00' * ((55 - n) % 64) + struct.pack('>Q', 8 * n)
    return [list(struct.unpack('>16I', p[i:i+64])) for i in range(0, len(p), 64)]

def digest(msg, R):
    cv = list(IV)
    for blk in blocks(msg): cv = compress(cv, blk, R)
    return struct.pack('>8I', *cv)

# ---------------------------------------------------------------------------------------------------------
# ePrint 2026/1120 Table 15 (37 steps): rows not listed are all '='.  MSB first.
# Member x is the message the paper prints second (M'); 'n' = (x, y) bits (0, 1), 'u' = (1, 0), '0'/'1' fixed
# and equal, '=' equal, '+' (undefined in the paper) read as E_i[b] = E_{i-1}[b] for vertical '+' pairs.
# X: Table 16 two-bit conditions as printed (word, step, bit, op, word, step, bit); not used by the attack.
CH = {37: dict(
 A={6:'=nu=============================',7:'==========n====n====n======n====',10:'======u===========u=============',
    11:'====u=====u=========u=n====u==n=',12:'=nu=============================',13:'====u=========u=u=======n==u====',
    14:'======u=n=======n===============',16:'==u============================='},
 E={4:'000=============================',5:'111=0=====1==0=====01===++01====',6:'uuu=1011=00=10111=0111=0++1011==',
    7:'10n=u01001n00n00010nu110unuu0001',8:'011=1n+1=n11u1101=001u1u1010=u=1',9:'1=0110+=001=1100=+110100111u=0=+',
    10:'10n001u110101==01+u1101011=1110+',11:'=01un000011101=n0n0u1uu101011u1u',12:'01101uuuuunu010110110n1u0u0uu0n0',
    13:'0+10n110111unn+0n101110110001001',14:'=+0=1000000111+=1==1n010u0=0101=',15:'=u==01===n=011n01==u0=u=1==+====',
    16:'=0=====+00===11=+==01=0=0==+====',17:'=0=====+01===u1=+==0==1===1u====',18:'==10===uu====0==n===111===01==1=',
    19:'==1====00====1==0==========1====',20:'==u====10=======1===00==========',21:'==0=============================',
    22:'==1============================='},
 W={6:'==n=============================',7:'=====u===u==========n===========',8:'==u=============================',
    9:'=====u=u=======n===u==n=u=n=u=n=',10:'============n======u=n==========',14:'=0===u===n=1=1====1=u=1=====1=1=',
    15:'==u=============================',22:'=====0=nn=====1=u=1=============',24:'==n============================='},
 X=[('A',15,15,'!','A',16,15),('A',15,23,'=','A',16,23),('A',15,25,'=','A',16,25),('A',16,9,'!','A',16,20),
    ('A',16,18,'!','A',16,6),('A',16,8,'=','A',16,17),('A',16,29,'=','A',17,29),('A',17,29,'=','A',18,29),
    ('E',15,4,'=','E',16,4),('E',17,0,'!','E',17,13),('E',16,24,'=','E',17,24),('E',16,15,'=','E',17,15),
    ('E',18,6,'!','E',18,19),('E',18,2,'=','E',18,20),('E',20,2,'!','E',20,16),
    ('W',6,1,'=','W',6,12),('W',6,8,'!','W',6,25),('W',6,14,'=','W',6,18),
    ('W',7,0,'=','W',7,28),('W',7,9,'=','W',7,30),('W',7,1,'=','W',7,18),
    ('W',8,1,'!','W',8,12),('W',8,8,'!','W',8,25),('W',8,14,'=','W',8,18),
    ('W',22,31,'!','W',22,1),('W',22,30,'!','W',22,0),('W',22,16,'!','W',22,25),('W',22,14,'!','W',22,21),
    ('W',24,4,'!','W',24,6),('W',24,22,'=','W',24,31),('W',24,20,'!','W',24,27)])}

def _h(s): return [int(t, 16) for t in s.split()]
# Table 17: chaining value, M (printed first), M' (printed second = member x), printed hash.
PAIRS = {
 37: dict(cv=_h('63b4986c 35d83dc0 c98894e4 784e08fc 78a7f752 5ed877a8 315a2db3 d5614eb4'),
  m=_h('4d7f86ff 32ece589 d8accfc4 2cc2e433 068b5b34 eba68a28 2fe12cad 6aa26b0c 9f0d78e1 681b8277 faa9c7e0 56aed439 cc2dbbc2 dd2ba0fc b95d377b 5dd43a81'),
  mp=_h('4d7f86ff 32ece589 d8accfc4 2cc2e433 068b5b34 eba68a28 0fe12cad 6ee2630c bf0d78e1 6d1a90dd faa1d3e0 56aed439 cc2dbbc2 dd2ba0fc bd1d3f7b 7dd43a81'),
  hash=_h('a856d46e 4b46eb28 4935248c 92a2fc98 e0fb2610 10a9951f 54264f5b 80954580'))}

# Exact sizes of the Step-2 sets F = {w : s0(w + d) - s0(w) = t mod 2^32} (exhaustive counts over 2^32 words,
# proof.md Section 4.3; reproduced by fcount.c and sampled by selftest.py).
FSIZE = {(37, 7): 68157440, (37, 6): 287309824}

def trace(cv, w16, R):
    """A[i], E[i] for i = -4..R-1 (A[-1..-4] = cv[0..3], E[-1..-4] = cv[4..7]) and the expanded W."""
    A = {-1: cv[0], -2: cv[1], -3: cv[2], -4: cv[3]}; E = {-1: cv[4], -2: cv[5], -3: cv[6], -4: cv[7]}
    W = list(w16)
    for i in range(16, R): W.append((s1(W[i-2]) + W[i-7] + s0(W[i-15]) + W[i-16]) & M32)
    for i in range(R):
        E[i] = (A[i-4] + E[i-4] + S1(E[i-1]) + IF(E[i-1], E[i-2], E[i-3]) + K[i] + W[i]) & M32
        A[i] = (E[i] - A[i-4] + S0(A[i-1]) + MAJ(A[i-1], A[i-2], A[i-3])) & M32
    return A, E, W

def cell(s):
    """(m, v, d, p): x-value mask, x-values, XOR-difference mask, '+' mask."""
    m = v = d = p = 0
    for c, sym in enumerate(s):
        b = 31 - c
        if sym in '01un': m |= 1 << b
        if sym in '1u': v |= 1 << b
        if sym in 'un': d |= 1 << b
        if sym == '+': p |= 1 << b
    return m, v, d, p

def row(ch, k, i): return cell(ch[k].get(i, '=' * 32))

def follows(ch, k, i, x, y, xprev=None):
    m, v, d, p = row(ch, k, i)
    ok = (x & m) == v and (x ^ y) == d
    if p and k == 'E':
        q = p & row(ch, 'E', i - 1)[3]
        if q: ok = ok and ((x ^ xprev) & q) == 0
    return ok

def cellcheck(R, cv, wx, wy):
    """Mismatching cells of the pair (x, y) from cv on rows -4..R-1; and the two traces."""
    ch = CH[R]; Ax, Ex, Wx = trace(cv, wx, R); Ay, Ey, Wy = trace(cv, wy, R); bad = []
    for i in range(-4, R):
        if not follows(ch, 'A', i, Ax[i], Ay[i]): bad.append(('A', i))
        if not follows(ch, 'E', i, Ex[i], Ey[i], Ex.get(i-1)): bad.append(('E', i))
        if i >= 0 and not follows(ch, 'W', i, Wx[i], Wy[i]): bad.append(('W', i))
    return bad, (Ax, Ex, Wx), (Ay, Ey, Wy)

# ---------------------------------------------------------------------------------------------------------
# Step 1 (from the published SFS pair) and the derived constants.
def stepE(A, E, i, w): return (A[i-4] + E[i-4] + S1(E[i-1]) + IF(E[i-1], E[i-2], E[i-3]) + K[i] + w) & M32
def stepA(A, E, i): return (E[i] - A[i-4] + S0(A[i-1]) + MAJ(A[i-1], A[i-2], A[i-3])) & M32
def sgn(s):
    v = 0
    for c, sym in enumerate(s):
        if sym == 'n': v += 1 << (31 - c)
        if sym == 'u': v -= 1 << (31 - c)
    return v & M32

def enum_L(R, Sx, Sy, Wsx, Wsy, need):
    """Exact freedom set: all (W14, W15) (x side; y side follows) with rows 14 and 15 of A and E following
    the cells for both members, '+' pairs with row 13/14, and the four sigma differences of W14, W15 equal to
    `need`.  Returns (L, number of E14 candidates, number of E15 candidates)."""
    ch = CH[R]; out = []; n14 = n15 = 0
    def cands(i, Eprev):
        m, v, d, p = row(ch, 'E', i)
        q = p & row(ch, 'E', i - 1)[3]
        m |= q; v |= Eprev & q
        free = [b for b in range(32) if not (m >> b) & 1]
        for bits in range(1 << len(free)):
            x = v
            for j, b in enumerate(free):
                if (bits >> j) & 1: x |= 1 << b
            yield x, d
    Ax, Ex = dict(Sx[0]), dict(Sx[1]); Ay, Ey = dict(Sy[0]), dict(Sy[1])
    for e14, d14 in cands(14, Ex[13]):
        n14 += 1
        w14 = (e14 - stepE(Ax, Ex, 14, 0)) & M32; e14y = e14 ^ d14; w14y = (e14y - stepE(Ay, Ey, 14, 0)) & M32
        Ex[14] = e14; Ey[14] = e14y; a14 = stepA(Ax, Ex, 14); a14y = stepA(Ay, Ey, 14)
        if not follows(ch, 'A', 14, a14, a14y): continue
        if ((s1(w14y) - s1(w14)) & M32, (s0(w14y) - s0(w14)) & M32) != need[0]: continue
        Ax[14] = a14; Ay[14] = a14y
        for e15, d15 in cands(15, e14):
            n15 += 1
            e15y = e15 ^ d15
            w15 = (e15 - stepE(Ax, Ex, 15, 0)) & M32; w15y = (e15y - stepE(Ay, Ey, 15, 0)) & M32
            Ex[15] = e15; Ey[15] = e15y
            a15 = stepA(Ax, Ex, 15); a15y = stepA(Ay, Ey, 15)
            if not follows(ch, 'A', 15, a15, a15y): continue
            if ((s1(w15y) - s1(w15)) & M32, (s0(w15y) - s0(w15)) & M32) != need[1]: continue
            out.append((w14, w15, w14y, w15y))
    return out, n14, n15

def lstar_ok(R, P, l):
    """Row-16 modular differences dE16, dA16 (independent of the first block) equal the characteristic's."""
    ch = CH[R]; w14, w15, w14y, w15y = l
    Ax, Ex = dict(P['Sx'][0]), dict(P['Sx'][1]); Ay, Ey = dict(P['Sy'][0]), dict(P['Sy'][1])
    for i, wx, wy in ((14, w14, w14y), (15, w15, w15y)):
        Ex[i] = stepE(Ax, Ex, i, wx); Ey[i] = stepE(Ay, Ey, i, wy); Ax[i] = stepA(Ax, Ex, i); Ay[i] = stepA(Ay, Ey, i)
    dW16 = (s1(w14y) - s1(w14) + P['Wy'][9] - P['Wx'][9]) & M32
    dE16 = (Ay[12] + Ey[12] + S1(Ey[15]) + IF(Ey[15], Ey[14], Ey[13]) - Ax[12] - Ex[12] - S1(Ex[15])
            - IF(Ex[15], Ex[14], Ex[13]) + dW16) & M32
    dA16 = (dE16 - (Ay[12] - Ax[12]) + S0(Ay[15]) - S0(Ax[15]) + MAJ(Ay[15], Ay[14], Ay[13])
            - MAJ(Ax[15], Ax[14], Ax[13])) & M32
    return dE16 == sgn(row_str(ch, 'E', 16)) and dA16 == sgn(row_str(ch, 'A', 16)), (Ax, Ex, Ay, Ey)

def row_str(ch, k, i): return ch[k].get(i, '=' * 32)

LSTAR = {37: [(0xbd1d3f7b, w) for w in (0x7dd41680,0x7dd41681,0x7dd416a0,0x7dd416a1,0x7dd41a80,0x7dd41a81,0x7dd41aa0,
         0x7dd41aa1,0x7dd43680,0x7dd43681,0x7dd436a0,0x7dd436a1,0x7dd43a80,0x7dd43a81,0x7dd43aa0,0x7dd43aa1,0xfdb41680,
         0xfdb41681,0xfdb416a0,0xfdb416a1,0xfdb41a80,0xfdb41a81,0xfdb41aa0,0xfdb41aa1,0xfdb43680,0xfdb43681,0xfdb436a0,
         0xfdb436a1,0xfdb43a80,0xfdb43a81,0xfdb43aa0,0xfdb43aa1)]}

def setup(R, full=False):
    """All constants of the attack for R steps.  full=True re-enumerates L and L* (slow: about 2 s / 20 s);
    otherwise the recorded L* is used and each element is re-checked exactly (rows 14..16 conditions)."""
    ch = CH[R]; pr = PAIRS[R]
    bad, X, Y = cellcheck(R, pr['cv'], pr['mp'], pr['m'])
    assert not bad, bad
    (Ax, Ex, Wx), (Ay, Ey, Wy) = X, Y
    P = dict(R=R, C=C_REF[R], Wx=Wx[:16], Wy=Wy[:16])
    P['Sx'] = ({i: Ax[i] for i in range(14)}, {i: Ex[i] for i in range(14)})
    P['Sy'] = ({i: Ay[i] for i in range(14)}, {i: Ey[i] for i in range(14)})
    A, E = Ax, Ex
    for i in range(6):                 # rows <= 5 and W0..W5 carry no difference in either characteristic
        assert Ax[i] == Ay[i] and (i < 4 or Ex[i] == Ey[i]) and Wx[i] == Wy[i]
    # Step 2 constants (W7 = c7 - A[-1]; W6 = c6 + 2 + ~A[-2] + MAJ(A1,A0,A[-1]) + ~IF(E5,E4,E3) mod 2^32)
    P['c7'] = (E[7] - 2 * A[3] + S0(A[2]) + MAJ(A[2], A[1], A[0]) - S1(E[6]) - IF(E[6], E[5], E[4]) - K[7]) & M32
    P['k3'] = (A[3] - S0(A[2]) - MAJ(A[2], A[1], A[0])) & M32
    P['c6'] = (E[6] - 2 * A[2] + S0(A[1]) - S1(E[5]) - K[6]) & M32
    for i in (6, 7):
        P['d%d' % i] = (Wy[i] - Wx[i]) & M32; P['t%d' % i] = (s0(Wy[i]) - s0(Wx[i])) & M32
    assert (P['c7'] - pr['cv'][0]) & M32 == Wx[7]
    need = (((s1(Wy[14]) - s1(Wx[14])) & M32, (s0(Wy[14]) - s0(Wx[14])) & M32),
            ((s1(Wy[15]) - s1(Wx[15])) & M32, (s0(Wy[15]) - s0(Wx[15])) & M32))
    P['need'] = need
    if full:
        L, n14, n15 = enum_L(R, P['Sx'], P['Sy'], Wx, Wy, need)
        P['L'] = L; P['nE14'] = n14; P['nE15'] = n15
        Ls = [l for l in L if lstar_ok(R, P, l)[0]]
        assert sorted((a, b) for a, b, _, _ in Ls) == sorted(LSTAR[R]), 'L* differs from the recorded list'
        Ls = sorted(Ls, key=lambda l: LSTAR[R].index(l[:2]))
    else:
        Ls = []
        for (w14, w15) in LSTAR[R]:
            Axx, Exx = dict(P['Sx'][0]), dict(P['Sx'][1])
            e14 = stepE(Axx, Exx, 14, w14); Exx[14] = e14; Axx[14] = stepA(Axx, Exx, 14)
            e15 = stepE(Axx, Exx, 15, w15)
            d14 = row(ch, 'E', 14)[2]; d15 = row(ch, 'E', 15)[2]
            Ayy, Eyy = dict(P['Sy'][0]), dict(P['Sy'][1])
            w14y = ((e14 ^ d14) - stepE(Ayy, Eyy, 14, 0)) & M32; Eyy[14] = e14 ^ d14; Ayy[14] = stepA(Ayy, Eyy, 14)
            w15y = ((e15 ^ d15) - stepE(Ayy, Eyy, 15, 0)) & M32
            Ls.append((w14, w15, w14y, w15y))
    # exact re-check of every element of L*: rows 14/15 cells (A, E, W), '+' pairs, sigma differences, row-16 dE/dA
    P['Lstar'] = []
    for l in Ls:
        ok, (Ax2, Ex2, Ay2, Ey2) = lstar_ok(R, P, l)
        w14, w15, w14y, w15y = l
        for i, wx_, wy_ in ((14, w14, w14y), (15, w15, w15y)):
            assert follows(ch, 'A', i, Ax2[i], Ay2[i]) and follows(ch, 'E', i, Ex2[i], Ey2[i], Ex2[i-1])
            assert follows(ch, 'W', i, wx_, wy_)
        assert ok and (((s1(w14y) - s1(w14)) & M32, (s0(w14y) - s0(w14)) & M32), ((s1(w15y) - s1(w15)) & M32,
                (s0(w15y) - s0(w15)) & M32)) == need
        P['Lstar'].append(dict(w=l, Ax=Ax2, Ex=Ex2, Ay=Ay2, Ey=Ey2))
    assert (Wx[14], Wx[15]) in [(d['w'][0], d['w'][1]) for d in P['Lstar']]
    # stage 3a: x-value cells of E16 plus the '+' pairs with E15 (value known per l); W16 = k16 + s0(W1) + W0
    m16, v16, _, p16 = row(ch, 'E', 16); q16 = p16 & row(ch, 'E', 15)[3]
    P['m16'] = m16 | q16
    for d in P['Lstar']:
        Axl, Exl = d['Ax'], d['Ex']
        d['k16'] = (s1(d['w'][0]) + Wx[9]) & M32
        d['c16'] = (Axl[12] + Exl[12] + S1(Exl[15]) + IF(Exl[15], Exl[14], Exl[13]) + K[16]) & M32
        d['v16'] = v16 | (Exl[15] & q16); d['ck16'] = (d['c16'] + d['k16']) & M32
    P['f16'] = bin(P['m16']).count('1')
    # rows R-4..R-1 of A and E carry no difference: the cells of rows >= 16 imply equal outputs
    for i in range(R - 4, R): assert row(ch, 'A', i)[2] == 0 and row(ch, 'E', i)[2] == 0
    P['rows'] = {i: (row(ch, 'A', i), row(ch, 'E', i), row(ch, 'W', i), row(ch, 'E', i)[3] & row(ch, 'E', i - 1)[3])
                 for i in range(16, R)}
    P['F7'] = FSIZE[(R, 7)]; P['F6'] = FSIZE.get((R, 6), 1 << 32); P['s3c'] = stage3_constants(P)
    assert (P['d6'] == 0) == (R == 38)
    return P

def tables_digest(R):
    """SHA-256 of the data the attack and smc.py use (cells, pair, S, L*, row masks, Step-2 constants)."""
    P = setup(R)
    obj = dict(ch=CH[R], pair=PAIRS[R], S=[P['Sx'], P['Sy']], W=[P['Wx'], P['Wy']], rows=P['rows'],
               L=[[d['w'], d['Ax'], d['Ex'], d['Ay'], d['Ey'], d['ck16'], d['v16']] for d in P['Lstar']],
               c=[P[k] for k in ('c7', 'd7', 't7', 'c6', 'd6', 't6', 'k3', 'F6', 'F7', 'm16')])
    return hashlib.sha256(json.dumps(obj, sort_keys=True).encode()).hexdigest()

# ---------------------------------------------------------------------------------------------------------
# Program constants, group setup, rare path.
def varying(R):
    """Schedule words that depend on W15 (structural)."""
    v = {15}
    for i in range(16, R):
        if any(j in v for j in (i - 2, i - 7, i - 15, i - 16)): v.add(i)
    return v

def foldK(R, i):
    """K_i is folded into W_i's group constant when W_i has a constant part and no later schedule use."""
    return i in varying(R) and i >= 21 and all(j >= R for j in (i + 2, i + 7, i + 15, i + 16)) and \
        any(j not in varying(R) for j in (i - 2, i - 7, i - 15, i - 16))

class Sc:
    """Counted scalar machine (group setup, rare path, Step 3): one 32-bit value per 256-bit word.  Every
    primitive counts 1: ld (load), add, sub, and, or, xor, shr, shl, compare, branch.  Arithmetic is mod 2^256
    (lazy) and m() masks to 32 bits.  A rotation uses the doubled word x | x << 32 (2 ops), so S0, S1, s0 and
    s1 cost 8 each; every input of a doubling or a compare is asserted to be masked."""
    def __init__(self): self.n = 0
    def ld(self, v): self.n += 1; return v
    def add(self, a, b): self.n += 1; return (a + b) & WORD
    def sub(self, a, b): self.n += 1; return (a - b) & WORD
    def m(self, a): self.n += 1; return a & M32
    def xor(self, a, b): self.n += 1; return a ^ b
    def and_(self, a, b): self.n += 1; return a & b
    def or_(self, a, b): self.n += 1; return a | b
    def shr(self, a, k): self.n += 1; return a >> k
    def dbl(self, x):
        assert 0 <= x <= M32; self.n += 2; return x | (x << 32)
    def S0(self, x): d = self.dbl(x); self.n += 6; return ((d >> 2) ^ (d >> 13) ^ (d >> 22)) & M32
    def S1(self, x): d = self.dbl(x); self.n += 6; return ((d >> 6) ^ (d >> 11) ^ (d >> 25)) & M32
    def s0(self, x): d = self.dbl(x); self.n += 6; return (((d >> 7) ^ (d >> 18)) & M32) ^ (x >> 3)
    def s1(self, x): d = self.dbl(x); self.n += 6; return (((d >> 17) ^ (d >> 19)) & M32) ^ (x >> 10)
    def IF(self, x, y, z): return self.xor(self.and_(x, self.xor(y, z)), z)
    def MAJ(self, x, y, z): return self.xor(self.and_(self.xor(x, y), self.xor(y, z)), y)
    def eq(self, a, b):
        assert 0 <= a <= M32 and 0 <= b <= M32; self.n += 2; return a == b

def batch_constants(P):
    """Step-2 constants of the batch circuit (instruction constants): W7 = ~A_{R-1} + c7m; E3 = A_{R-1} + k3i;
    W6 = ~A_{R-2} + MAJ(A1, A0, A[-1]) + ~IF(E5, E4, E3) + k6i (mod 2^32)."""
    A, E = P['Sx']
    return {'c7m': (P['c7'] - IV[0] + 1) & M32, 'k3i': (IV[0] + P['k3']) & M32, 'A1^A0': A[1] ^ A[0],
            'A1&A0': A[1] & A[0], 'E5': E[5], 'E4': E[4], 'k6i': (P['c6'] + 2 - IV[1]) & M32}

def group_setup(sc, R, words):
    """Per group (scalar machine): two RAND words, W0..W14 (shift + mask), rounds 0..14, the group constants;
    W0..W14, A11..A14, E11..E14 STOREd for the rare path."""
    w = [sc.m(sc.shr(words[j // 8], 32 * (j % 8))) for j in range(15)]
    a, b, c, d, e, f, g, h = [sc.ld(x) for x in IV]
    for i in range(15):
        t1 = sc.add(sc.add(sc.add(sc.add(h, sc.S1(e)), sc.IF(e, f, g)), sc.ld(K[i])), w[i])
        t2 = sc.add(sc.S0(a), sc.MAJ(a, b, c))
        a, b, c, d, e, f, g, h = sc.m(sc.add(t1, t2)), a, b, c, sc.m(sc.add(d, t1)), e, f, g
    A14, A13, A12, A11, E14, E13, E12, E11 = a, b, c, d, e, f, g, h
    t1c = sc.add(sc.add(sc.add(h, sc.S1(e)), sc.IF(e, f, g)), sc.ld(K[15]))
    t2c = sc.add(sc.S0(a), sc.MAJ(a, b, c))
    Wc = dict(enumerate(w))
    for i in (16, 18, 20):
        Wc[i] = sc.m(sc.add(sc.add(sc.s1(Wc[i-2]), Wc[i-7]), sc.add(sc.s0(Wc[i-15]), Wc[i-16])))
    G = {}
    G['ke15'] = sc.add(A11, t1c); G['ka15'] = sc.add(t1c, t2c); G['E14'] = E14; G['E13'] = E13
    G['k16'] = sc.add(sc.add(E12, sc.ld(K[16])), Wc[16]); G['A14'] = A14; G['A13'] = A13; G['A12'] = A12
    G['k17'] = sc.add(E13, sc.ld(K[17])); G['k18'] = sc.add(sc.add(E14, sc.ld(K[18])), Wc[18])
    G['k20'] = sc.add(sc.ld(K[20]), Wc[20])
    var = varying(R)
    for i in sorted(var - {15}):
        cst = None
        for (j, fn) in ((i - 2, 's1'), (i - 7, None), (i - 15, 's0'), (i - 16, None)):
            if j in var: continue
            t = sc.s1(Wc[j]) if fn == 's1' else sc.s0(Wc[j]) if fn == 's0' else Wc[j]
            cst = t if cst is None else sc.add(cst, t)
        if cst is not None and foldK(R, i): cst = sc.add(cst, sc.ld(K[i]))
        if cst is not None: G['W%d' % i] = cst
    G = dict((k, sc.m(v)) for k, v in G.items())
    sc.n += 2 + 23                                      # the two RAND words; the 23 STOREs
    return G, dict(W=w, A=(A11, A12, A13, A14), E=(E11, E12, E13, E14))

LSCAN0, LSCAN1 = 3, 45
def lanes_of(sc, F):
    """Lanes with a clear fail bit: z = F XOR ones; per lane: lowest bit (negate, and), index by 8 tests on the lane
    planes (load, and, compare, branch, or), clear (xor), loop test (compare, branch)."""
    z = F ^ WORD; out = []; sc.n += LSCAN0
    while z:
        lo = z & -z; z ^= lo; out.append(lo.bit_length() - 1); sc.n += LSCAN1
    return out

def lane_cv(sc, gs, k, L, R):
    """CV1 of lane L of batch k: W15 = 2^8 k + L (shift, or), schedule, rounds 15..R-1 from the stored state."""
    ld = sc.ld; W = [ld(x) for x in gs['W']] + [(k << 8) | L]; sc.n += 2
    for i in range(16, R): W.append(sc.m(sc.add(sc.add(sc.s1(W[i-2]), W[i-7]), sc.add(sc.s0(W[i-15]), W[i-16]))))
    a, b, c, d = [ld(gs['A'][i]) for i in (3, 2, 1, 0)]; e, f, g, h = [ld(gs['E'][i]) for i in (3, 2, 1, 0)]
    for i in range(15, R):
        t1 = sc.add(sc.add(sc.add(sc.add(h, sc.S1(e)), sc.IF(e, f, g)), ld(K[i])), W[i])
        t2 = sc.add(sc.S0(a), sc.MAJ(a, b, c))
        a, b, c, d, e, f, g, h = sc.m(sc.add(t1, t2)), a, b, c, sc.m(sc.add(d, t1)), e, f, g
    return [sc.m(sc.add(x, ld(v))) for x, v in zip((a, b, c, d, e, f, g, h), IV)]

# ---------------------------------------------------------------------------------------------------------
# The bit-sliced batch: plane j of a word holds bit j of 256 lanes.  Lane L of batch k uses W15 = 2^8 k + L.  The
# batch is a circuit on planes (XOR, AND, OR; NOT is a polarity flag; column adders) for rounds 15..R-1 and both
# Step-2 tests; gates of group-fixed inputs (group constants, lane-index planes) are computed once per group.
# emit() maps it onto POOL registers with every LOAD and STORE explicit; c_B = its length + BFIX.
ONE, ZERO = ('C', 1), ('C', 0)
POOL = 64          # every register is free inside the circuit (k is stored before it and reloaded after it)

class Net:
    """Literals (node, neg) or ('C', bit); cached gates; a gate of two group-fixed nodes is hoisted."""
    def __init__(s): s.nodes, s.cse, s.inputs, s.grp, s.hdef = [], {}, {}, set(), {}
    def inp(s, name, grp=True):
        if name not in s.inputs:
            s.nodes.append(('in', name)); s.inputs[name] = len(s.nodes) - 1
            if grp: s.grp.add(len(s.nodes) - 1)
        return (s.inputs[name], 0)
    def gate(s, op, a, b):
        if a > b: a, b = b, a
        k = (op, a, b)
        if k not in s.cse:
            h = a in s.grp and b in s.grp
            s.nodes.append(('in', 'H') if h else k); n = len(s.nodes) - 1; s.cse[k] = n
            if h: s.hdef[n] = k; s.grp.add(n)
        return s.cse[k]
    def NOT(s, x): return (x[0], 1 - x[1])
    def XOR(s, x, y):
        if x[0] == 'C': x, y = y, x
        if y[0] == 'C': return (x[0], x[1] ^ y[1])
        if x[0] == y[0]: return ('C', x[1] ^ y[1])
        return (s.gate('xor', x[0], y[0]), x[1] ^ y[1])
    def AND(s, x, y):
        if x[0] == 'C': x, y = y, x
        if y[0] == 'C': return x if y[1] else ZERO
        if x[0] == y[0]: return x if x[1] == y[1] else ZERO
        if not x[1] and not y[1]: return (s.gate('and', x[0], y[0]), 0)
        if x[1] and y[1]: return (s.gate('or', x[0], y[0]), 1)
        if x[1]: x, y = y, x
        return (s.gate('xor', s.gate('or', x[0], y[0]), y[0]), 0)
    def OR(s, x, y): return s.NOT(s.AND(s.NOT(x), s.NOT(y)))
    def CH(s, e, f, g):
        if e[0] == 'C': return f if e[1] else g
        d = s.XOR(f, g)
        if d[0] == 'C': return s.XOR(g, s.AND(e, d))
        if d[1] == 0: return s.XOR(g if e[1] == 0 else f, (s.gate('and', e[0], d[0]), 0))
        return s.NOT(s.XOR(f if e[1] == 0 else g, (s.gate('or', e[0], d[0]), 0)))
    def MAJ(s, a, b, c):
        d1, d2 = s.XOR(a, b), s.XOR(b, c)
        if d1[0] == 'C' or d2[0] == 'C': return s.XOR(b, s.AND(d1, d2))
        if d1[1] == d2[1]: return (s.XOR(b, (s.gate('and', d1[0], d2[0]), 0)) if d1[1] == 0 else
                                   s.NOT(s.XOR(b, (s.gate('or', d1[0], d2[0]), 0))))
        return s.NOT(s.XOR(c if d1[1] == 0 else a, (s.gate('or', d1[0], d2[0]), 0)))

class Col:
    """Column adder mod 2^32, one bit column per step."""
    def __init__(s, net): s.n, s.carry, s.j = net, [], 0
    def step(s, bits):
        n = s.n; col = s.carry + list(bits); s.carry = []; last = s.j == 31
        k = sum(l[1] for l in col if l[0] == 'C'); col = [l for l in col if l[0] != 'C']
        if k >= 2 and not last: s.carry += [ONE] * (k // 2)
        if k % 2: col.append(ONE)
        while len(col) >= 3:
            if col[-1] is ONE:
                pr = [(i, j) for i in range(len(col) - 1) for j in range(i + 1, len(col) - 1) if col[i][1] == col[j][1]]
                if pr:
                    i, j = pr[0]; b = col.pop(j); a = col.pop(i); col.pop()
                    if not last: s.carry.append(n.OR(a, b))
                    col.append(n.NOT(n.XOR(a, b))); continue
            a, b, c = col.pop(0), col.pop(0), col.pop(0)
            if last: col.append(n.XOR(n.XOR(a, b), c)); continue
            if c is ONE: s.carry.append(n.OR(a, b)); col.append(n.NOT(n.XOR(a, b))); continue
            t = n.XOR(a, b); col.append(n.XOR(t, c))
            s.carry.append(n.CH(t, c, a) if t[1] == 0 else n.CH((t[0], 0), a, c))
        if len(col) == 2:
            a, b = col
            if not last: s.carry.append(n.AND(a, b))
            col = [n.XOR(a, b)]
        s.j += 1
        return col[0] if col else ZERO

def gconst(R):
    var = varying(R); g = ['ke15', 'ka15', 'E14', 'E13', 'k16', 'A14', 'A13', 'A12', 'k17', 'k18', 'k20']
    return g + ['W%d' % i for i in sorted(var - {15}) if any(j not in var for j in (i - 2, i - 7, i - 15, i - 16))]

def circuit(R, P):
    """(net, fail literal, A_{R-1}, A_{R-2}); fail bit L = lane L fails W7 in F7 or W6 in F6."""
    n = Net(); var = varying(R); gk = set(gconst(R))
    G = lambda k: [n.inp('%s.%d' % (k, j)) for j in range(32)]
    cw = lambda v: [ONE if (v >> j) & 1 else ZERO for j in range(32)]
    def add(*ws):
        c = Col(n); return [c.step([w[j] for w in ws]) for j in range(32)]
    X3 = lambda x, y, z: n.XOR(n.XOR(x, y), z)
    S1f = lambda e: lambda j: X3(e[(j + 6) % 32], e[(j + 11) % 32], e[(j + 25) % 32])
    S0f = lambda a: lambda j: X3(a[(j + 2) % 32], a[(j + 13) % 32], a[(j + 22) % 32])
    s0f = lambda x: lambda j: X3(x[(j + 7) % 32], x[(j + 18) % 32], x[j + 3] if j < 29 else ZERO)
    s1f = lambda x: lambda j: X3(x[(j + 17) % 32], x[(j + 19) % 32], x[j + 10] if j < 22 else ZERO)
    CHf = lambda e, f, g: lambda j: n.CH(e[j], f[j], g[j])
    wf = lambda w: lambda j: w[j]
    sg0 = lambda x: [s0f(x)(j) for j in range(32)]
    w15 = [n.inp('L%d' % j) for j in range(8)] + [n.inp('U%d' % j, False) for j in range(24)]
    Wv = {15: w15}
    def terms(i):
        ts = [f(Wv[j]) if f else wf(Wv[j]) for j, f in ((i - 2, s1f), (i - 7, None), (i - 15, s0f), (i - 16, None)) if j in var]
        return ts + ([wf(G('W%d' % i))] if 'W%d' % i in gk else [])
    def rnd(t1, d, a, b, c, wops=None, last=False):
        """One round, bit columns interleaved: T1 = sum(t1) (+ W_i), E = d + T1, A = T1 + S0(a) + MAJ(a, b, c)."""
        cs = [Col(n) for _ in range(4)]; Eo, Ao, Wo = [], [], []
        for j in range(32):
            ops = [f(j) for f in t1]
            if wops is not None: Wo.append(cs[3].step([f(j) for f in wops])); ops = [Wo[-1]] + ops
            t = cs[0].step(ops)
            if not last: Eo.append(cs[1].step([d[j], t]))
            Ao.append(cs[2].step([t, S0f(a)(j), n.MAJ(a[j], b[j], c[j])]))
        return Eo, Ao, Wo
    E15 = add(w15, G('ke15')); A15 = add(w15, G('ka15'))
    E16, A16, _ = rnd([S1f(E15), CHf(E15, G('E14'), G('E13')), wf(G('k16'))], G('A12'), A15, G('A14'), G('A13'))
    E17, A17, Wv[17] = rnd([wf(G('k17')), S1f(E16), CHf(E16, E15, G('E14'))], G('A13'), A16, A15, G('A14'), terms(17))
    E18, A18, _ = rnd([S1f(E17), CHf(E17, E16, E15), wf(G('k18'))], G('A14'), A17, A16, A15)
    a, b, c, d, e, f, g, h = A18, A17, A16, A15, E18, E17, E16, E15
    for i in range(19, R):
        hs = [wf(h), S1f(e), CHf(e, f, g)]
        if i == 20: Eo, Ao, _ = rnd([wf(G('k20'))] + hs, d, a, b, c, last=i == R - 1)
        elif foldK(R, i): Eo, Ao, _ = rnd(terms(i) + hs, d, a, b, c, last=i == R - 1)     # K_i folded into W_i's constant
        else: Eo, Ao, Wv[i] = rnd([lambda j, i=i: ONE if (K[i] >> j) & 1 else ZERO] + hs, d, a, b, c, terms(i), i == R - 1)
        if i < R - 1: a, b, c, d, e, f, g, h = Ao, a, b, c, Eo, e, f, g
    T2a = Ao
    A1, A2 = T2a, a                                                     # A_{R-1}, A_{R-2}
    C = batch_constants(P)
    W7 = add([n.NOT(x) for x in A1], cw(C['c7m']))                      # W7 = c7 - IV0 - A_{R-1}
    z = [n.XOR(x, y) for x, y in zip(sg0(add(W7, cw(P['d7']))), add(sg0(W7), cw(P['t7'])))]
    X = add(A1, cw(IV[0])); E3 = add(A1, cw(C['k3i']))                  # A[-1]; E3 = k3 + A[-1]
    mj = [X[j] if (C['A1^A0'] >> j) & 1 else cw(C['A1&A0'])[j] for j in range(32)]
    iv = [cw(C['E4'])[j] if (C['E5'] >> j) & 1 else E3[j] for j in range(32)]
    W6 = add([n.NOT(x) for x in A2], mj, [n.NOT(x) for x in iv], cw(C['k6i']))
    z += [n.XOR(x, y) for x, y in zip(sg0(add(W6, cw(P['d6']))), add(sg0(W6), cw(P['t6'])))]
    acc = z[0]
    for y in z[1:]: acc = n.OR(acc, y)
    return n, acc, A1, A2

def need(net, roots):
    nd, st = set(), list(roots)
    while st:
        x = st.pop()
        if x not in nd:
            nd.add(x)
            if net.nodes[x][0] != 'in': st += net.nodes[x][1:]
    return nd

def emit(net, root):
    """Gates in creation order on POOL registers: evict the furthest next use (STORE if used later and not in
    memory); LOAD every operand not in a register.  ('ld', r, node), ('st', node, r), (op, rd, ra, rb)."""
    nd = need(net, [root]); order = [x for x in sorted(nd) if net.nodes[x][0] != 'in']
    assert order[-1] == root
    uses = {}
    for p, x in enumerate(order):
        for o in net.nodes[x][1:]: uses.setdefault(o, []).append(p)
    INF = 1 << 60; ptr = {}
    def nxt(v, p):
        u = uses.get(v, ()); i = ptr.get(v, 0)
        while i < len(u) and u[i] < p: i += 1
        ptr[v] = i; return u[i] if i < len(u) else INF
    reg = {}; free = list(range(POOL))[::-1]; inmem = set(x for x in nd if net.nodes[x][0] == 'in'); prog = []
    def evict(p, keep):
        v = max((v for v in reg if v not in keep), key=lambda v: nxt(v, p)); r = reg.pop(v)
        if nxt(v, p) < INF and v not in inmem: prog.append(('st', v, r)); inmem.add(v)
        free.append(r)
    for p, x in enumerate(order):
        op, a, b = net.nodes[x]
        for o in (a, b):
            if o not in reg:
                if not free: evict(p, (a, b))
                r = free.pop(); prog.append(('ld', r, o)); reg[o] = r
        src = (reg[a], reg[b])
        for o in set((a, b)):
            if nxt(o, p + 1) >= INF: free.append(reg.pop(o))
        if not free: evict(p + 1, ())
        rd = free.pop(); reg[x] = rd; prog.append((op, rd) + src)
    return prog

def run(prog, mem):
    r = [0] * POOL
    for ins in prog:
        o = ins[0]
        if o == 'ld': r[ins[1]] = mem[ins[2]]
        elif o == 'st': mem[ins[1]] = r[ins[2]]
        elif o == 'xor': r[ins[1]] = r[ins[2]] ^ r[ins[3]]
        elif o == 'and': r[ins[1]] = r[ins[2]] & r[ins[3]]
        else: r[ins[1]] = r[ins[2]] | r[ins[3]]
    return r

def compile_net(net, roots):
    gl = [(x, ('xor', 'and', 'or').index(net.nodes[x][0]), net.nodes[x][1], net.nodes[x][2])
          for x in sorted(need(net, roots)) if net.nodes[x][0] != 'in']
    n = len(net.nodes)
    def f(I):
        v = [0] * n
        for k, w in I.items(): v[k] = w
        for x, o, a, b in gl:
            v[x] = v[a] ^ v[b] if o == 0 else v[a] & v[b] if o == 1 else v[a] | v[b]
        return tuple(v[r] for r in roots)
    return f

class Batch:
    def __init__(s, R, P):
        s.R = R; s.net, s.fail, s.A1, s.A2 = circuit(R, P); net = s.net
        s.prog = emit(net, s.fail[0]); net.cse = None
        s.roots = [s.fail[0]] + [x[0] for x in s.A1 + s.A2]
        assert all(x[0] != 'C' for x in s.A1 + s.A2)
        s.f = compile_net(net, s.roots)
        s.hoist = sorted(set(s.net.hdef))
        s.lanes = [sum(1 << L for L in range(256) if (L >> j) & 1) for j in range(8)]
        cats = {}
        for ins in s.prog: cats[ins[0]] = cats.get(ins[0], 0) + 1
        s.cats = cats
        s.cB = len(s.prog) + BFIX
    def group(s, sc, gc):
        """Group planes (shift, and, negate, store: 4 each) and hoisted gates (load, load, gate, store: 4 each)."""
        net = s.net; mem = {}
        for name, x in net.inputs.items():
            if name[0] == 'L' and name[1:].isdigit(): mem[x] = s.lanes[int(name[1:])]
            elif name[0] != 'U':
                k, j = name.rsplit('.', 1); mem[x] = WORD if (gc[k] >> int(j)) & 1 else 0; sc.n += 4
        for x in s.hoist:
            op, a, b = net.hdef[x]; mem[x] = mem[a] ^ mem[b] if op == 'xor' else mem[a] & mem[b] if op == 'and' else mem[a] | mem[b]
            sc.n += 4
        return mem
    def planes(s, mem, k):
        for j in range(24): mem[s.net.inputs['U%d' % j]] = WORD if (k >> j) & 1 else 0
    def fast(s, mem):
        v = s.f(mem); pol = [s.fail[1]] + [x[1] for x in s.A1 + s.A2]
        v = [x ^ (WORD if p else 0) for x, p in zip(v, pol)]
        return v[0], v[1:33], v[33:65]
    def counted(s, mem):
        r = run(s.prog, dict(mem)); return r[s.prog[-1][1]] ^ (WORD if s.fail[1] else 0)

# per batch besides the circuit: 24 batch planes (shift, and, negate, store), STORE k; after it LOAD ones,
# compare, branch (fail test); LOAD k, add, compare, branch (batch control)
BFIX = 4 * 24 + 1 + 3 + 4

def lane_word(planes, L): return sum(((p >> L) & 1) << j for j, p in enumerate(planes))

# ---------------------------------------------------------------------------------------------------------
# Step 3 (counted on Sc).
def stage3_constants(P):
    A, E = P['Sx']; c = {}
    c['kE1'] = (A[1] - S0(A[0])) & M32; c['kE2'] = (A[2] - S0(A[1])) & M32
    c['A1&A0'] = A[1] & A[0]; c['A1|A0'] = A[1] | A[0]
    c['kW4'] = (E[4] - A[0] - K[4]) & M32; c['kW5'] = (E[5] - A[1] - S1(E[4]) - K[5]) & M32
    c['kW6'] = (E[6] - A[2] - S1(E[5]) - K[6]) & M32; c['E5&E4'] = E[5] & E[4]; c['~E5'] = E[5] ^ M32
    return c

def step3(sc, P, cv, cost=None):
    """Counted Step 3 for one valid lane, cv = (A[-1], A[-2], A[-3], A[-4], E[-1], E[-2], E[-3], E[-4]).
    Stage 3a, for every l in L* in order: E16 = (c16 + k16) + s0(W1) + W0 must match the x-value cells of E16
    and the E15/E16 '+' pairs.  At the first pass W2..W7 are completed; stage 3b runs rows 16..R-1 of both
    members, checking every cell of the row and aborting at the first failing row.  Returns
    (index in L*, X words, Y words, stage-3b entries) for the first l passing every row, else (None, ...)."""
    R = P['R']; ld = sc.ld; A, E = P['Sx']; c = P['s3c']; n0 = sc.n
    a1, a2, a3, a4, e1, e2, e3, e4 = cv
    E0 = sc.m(sc.sub(sc.sub(sc.add(ld(A[0]), a4), sc.S0(a1)), sc.MAJ(a1, a2, a3)))
    W0 = sc.m(sc.sub(sc.sub(sc.sub(sc.sub(sc.sub(E0, a4), e4), sc.S1(e1)), sc.IF(e1, e2, e3)), ld(K[0])))
    E1 = sc.m(sc.sub(sc.add(ld(c['kE1']), a3), sc.MAJ(ld(A[0]), a1, a2)))
    W1 = sc.m(sc.sub(sc.sub(sc.sub(sc.sub(sc.sub(E1, a3), e3), sc.S1(E0)), sc.IF(E0, e1, e2)), ld(K[1])))
    q = sc.add(sc.s0(W1), W0)
    sc.keep = [E0, W0, E1, W1, q]                 # (bookkeeping for rare_liveness only; no operation)
    if cost is not None: cost['c01'] = sc.n - n0
    rest = None; n3b = 0
    for li, d in enumerate(P['Lstar']):
        n1 = sc.n
        e16 = sc.m(sc.add(ld(d['ck16']), q))
        p3a = sc.eq(sc.xor(sc.and_(e16, ld(P['m16'])), ld(d['v16'])), 0)
        if cost is not None: cost['c3a'] = sc.n - n1
        if not p3a: continue
        n3b += 1; sc.n += FLAG3B + V3B; n2 = sc.n    # flag test (are W2..W7 computed yet?), V update, register spill
        if rest is None:
            E2 = sc.m(sc.sub(sc.add(ld(c['kE2']), a2), sc.or_(ld(c['A1&A0']), sc.and_(a1, ld(c['A1|A0'])))))
            E3 = sc.m(sc.add(ld(P['k3']), a1))
            W2 = sc.m(sc.sub(sc.sub(sc.sub(sc.sub(sc.sub(E2, a2), e2), sc.S1(E1)), sc.IF(E1, E0, e1)), ld(K[2])))
            W3 = sc.m(sc.sub(sc.sub(sc.sub(sc.sub(sc.sub(E3, a1), e1), sc.S1(E2)), sc.IF(E2, E1, E0)), ld(K[3])))
            W4 = sc.m(sc.sub(sc.sub(sc.sub(ld(c['kW4']), E0), sc.S1(E3)), sc.IF(E3, E2, E1)))
            W5 = sc.m(sc.sub(sc.sub(ld(c['kW5']), E1), sc.IF(ld(E[4]), E3, E2)))
            W6 = sc.m(sc.sub(sc.sub(ld(c['kW6']), E2), sc.xor(ld(c['E5&E4']), sc.and_(E3, ld(c['~E5'])))))
            W7 = sc.m(sc.sub(ld(P['c7']), a1))
            rest = [W0, W1, W2, W3, W4, W5, W6, W7]
            rest_y = rest[:6] + [sc.m(sc.add(W6, ld(P['d6']))) if P['d6'] else W6, sc.m(sc.add(W7, ld(P['d7'])))]
            sc.keep_rest = rest + rest_y[6:]
            if cost is not None: cost['crest'] = sc.n - n2
        n4 = sc.n
        X = rest + [ld(P['Wx'][i]) for i in range(8, 14)] + [ld(d['w'][0]), ld(d['w'][1])]
        Y = rest_y + [ld(P['Wy'][i]) for i in range(8, 14)] + [ld(d['w'][2]), ld(d['w'][3])]
        Ax = dict((i, ld(d['Ax'][i])) for i in range(12, 16)); Ex = dict((i, ld(d['Ex'][i])) for i in range(12, 16))
        Ay = dict((i, ld(d['Ay'][i])) for i in range(12, 16)); Ey = dict((i, ld(d['Ey'][i])) for i in range(12, 16))
        ok = True
        for i in range(16, R):
            for Z in (X, Y):
                Z.append(sc.m(sc.add(sc.add(sc.add(sc.s1(Z[i-2]), Z[i-7]), sc.s0(Z[i-15])), Z[i-16])))
            k = ld(K[i])
            for (Aa, Ee, Z) in ((Ax, Ex, X), (Ay, Ey, Y)):
                t = sc.add(sc.add(sc.add(sc.add(sc.add(Aa[i-4], Ee[i-4]), sc.S1(Ee[i-1])),
                                         sc.IF(Ee[i-1], Ee[i-2], Ee[i-3])), k), Z[i])
                Ee[i] = sc.m(t)
                Aa[i] = sc.m(sc.add(sc.add(sc.sub(Ee[i], Aa[i-4]), sc.S0(Aa[i-1])), sc.MAJ(Aa[i-1], Aa[i-2], Aa[i-3])))
            (mA, vA, dA, _), (mE, vE, dE, _), (mW, vW, dW, _), pq = P['rows'][i]
            acc = None
            for (xv, yv, mm, vv, dd) in ((Ax[i], Ay[i], mA, vA, dA), (Ex[i], Ey[i], mE, vE, dE), (X[i], Y[i], mW, vW, dW)):
                t = sc.xor(xv, yv)
                if dd: t = sc.xor(t, ld(dd))
                if mm:
                    u = sc.and_(xv, ld(mm))
                    if vv: u = sc.xor(u, ld(vv))
                    t = sc.or_(t, u)
                acc = t if acc is None else sc.or_(acc, t)
            if pq: acc = sc.or_(acc, sc.and_(sc.xor(Ex[i], Ex[i-1]), ld(pq)))
            if not sc.eq(acc, 0): ok = False; break
        if cost is not None and ok: cost['c3b'] = sc.n - n4
        if ok: return li, X[:16], Y[:16], n3b
    return None, None, None, n3b

class ScLive(Sc):
    """Sc with a register-liveness trace: every value is live from the operation that defines it to the last
    operation that reads it (a result may reuse a dying input's register); a rotation function holds two extra
    temporaries (the doubled word and a partial result).  Used only by rare_liveness()."""
    class Vw:
        __slots__ = ('v', 'id')
        def __init__(s, v, i): s.v = v; s.id = i
    def __init__(self):
        Sc.__init__(self); self.t = 0; self.nid = 0; self.defs = {}; self.last = {}; self.tmp = []
    @staticmethod
    def u(x): return x.v if isinstance(x, ScLive.Vw) else x
    def _op(self, xs, v=None, extra=0):
        self.t += 1
        for x in xs:
            if isinstance(x, ScLive.Vw): self.last[x.id] = self.t
        if extra: self.tmp.append((self.t, extra))
        if v is None: return None
        self.nid += 1; self.defs[self.nid] = self.t; return ScLive.Vw(v, self.nid)
    def ld(self, v): self.n += 1; return self._op((), self.u(v))
    def add(self, a, b): self.n += 1; return self._op((a, b), (self.u(a) + self.u(b)) & WORD)
    def sub(self, a, b): self.n += 1; return self._op((a, b), (self.u(a) - self.u(b)) & WORD)
    def m(self, a): self.n += 1; return self._op((a,), self.u(a) & M32)
    def xor(self, a, b): self.n += 1; return self._op((a, b), self.u(a) ^ self.u(b))
    def and_(self, a, b): self.n += 1; return self._op((a, b), self.u(a) & self.u(b))
    def or_(self, a, b): self.n += 1; return self._op((a, b), self.u(a) | self.u(b))
    def shr(self, a, k): self.n += 1; return self._op((a,), self.u(a) >> k)
    def S0(self, x): self.n += 8; return self._op((x,), S0(self.u(x)), 2)
    def S1(self, x): self.n += 8; return self._op((x,), S1(self.u(x)), 2)
    def s0(self, x): self.n += 8; return self._op((x,), s0(self.u(x)), 2)
    def s1(self, x): self.n += 8; return self._op((x,), s1(self.u(x)), 2)
    def eq(self, a, b):
        assert 0 <= self.u(a) <= M32 and 0 <= self.u(b) <= M32; self.n += 2; self._op((a, b)); return self.u(a) == self.u(b)
    def peak(self, pinned=()):
        """Largest number of simultaneously live values; pinned values stay live to the end of the trace."""
        ev = []; end = self.t + 1; pin = set(x.id for x in pinned if isinstance(x, ScLive.Vw))
        for i, d in self.defs.items():
            u = end if i in pin else self.last.get(i)
            if u is not None and u > d: ev.append((d, 1)); ev.append((u, -1))
        for t, e in self.tmp: ev.append((t, e)); ev.append((t + 1, -e))
        ev.sort(key=lambda z: (z[0], z[1])); live = best = 0
        for _, x in ev: live += x; best = max(best, live)
        return best

def rare_liveness(R, P):
    """Register demand of the scalar rare path, traced with ScLive.  lane_cv of one lane (group state of a fixed
    group; its eight outputs stay live to the end).  Step 3 from the published pair's chaining value: the lane path
    (c01 and the 32 stage-3a tests, no stage-3b entry; the chaining value, E0, W0, E1, W1 and q kept to the end) and
    stage 3b (the published element passes every row), which runs after the register file is saved (SPILL3B), so
    only its own values and V occupy registers; W0..W7, W'6, W'7 are stored once computed and q is restored with the
    file.  Returns (lane_cv peak, lane peak, stage-3b peak) of the traced values."""
    gs = group_setup(Sc(), R, (1, 2))[1]; sc = ScLive(); cv = lane_cv(sc, gs, 0, 0, R); pcv = sc.peak(pinned=cv)
    cv0 = PAIRS[R]['cv']; li0 = [d['w'][:2] for d in P['Lstar']].index(tuple(P['Wx'][14:16]))
    sc = ScLive(); cv = [sc.ld(c) for c in cv0]
    P2 = dict(P); P2['Lstar'] = [d for i, d in enumerate(P['Lstar']) if i != li0]
    out = step3(sc, P2, cv); assert out[0] is None and out[3] == 0
    lane = sc.peak(pinned=cv + sc.keep)
    sc = ScLive(); cv = [sc.ld(c) for c in cv0]
    li, X, Y, n3b = step3(sc, P, cv); assert li == li0 and n3b == 1
    return pcv, lane, sc.peak()

def ref_words(P, cv):
    """Reference (uncounted) W0..W7 of member x from CV1 by the paper's Step-2 equations."""
    A = dict(P['Sx'][0]); E = dict(P['Sx'][1])
    A[-1], A[-2], A[-3], A[-4], E[-1], E[-2], E[-3], E[-4] = cv
    for i in range(4): E[i] = (A[i] + A[i-4] - S0(A[i-1]) - MAJ(A[i-1], A[i-2], A[i-3])) & M32
    return [(E[i] - A[i-4] - E[i-4] - S1(E[i-1]) - IF(E[i-1], E[i-2], E[i-3]) - K[i]) & M32 for i in range(8)]

def inF(w, d, t): return d == 0 or ((s0((w + d) & M32) - s0(w)) & M32) == t

VFIN_UNITS, VFIN_OPS = 6, 512
FLAG3B = 2
# Bookkeeping of the rare path, counted into V like every other rare-path operation: VLANE = 1 per passing lane
# (V += the lane's fixed cost, one ADD with an immediate); per stage-3b entry V3B = VENT + SPILL3B with VENT = 1
# (V += the cost of the executed stage-3b path, one ADD with an immediate at its exit) and SPILL3B = 148: STORE all
# 64 registers at entry and LOAD them back at exit (128), so stage 3b has the whole register file, plus STORE of
# W0..W7, W'6, W'7 after they are first computed and their LOAD at a later entry (20); see rare_liveness().
VLANE, VENT, SPILL3B = 1, 1, 148
V3B = VENT + SPILL3B

def verify(R, M0, X, Y):
    """Target verification (charged VFIN_UNITS target compressions + VFIN_OPS operations, at most once):
    the complete 128-byte messages M0||M1 and M0||M1' are distinct and have equal R-step digests."""
    mx = struct.pack('>16I', *M0) + struct.pack('>16I', *X); my = struct.pack('>16I', *M0) + struct.pack('>16I', *Y)
    if mx != my and digest(mx, R) == digest(my, R): return mx, my
    return None

# ---------------------------------------------------------------------------------------------------------
# The attack with fixed caps: NG groups of NBG = 7 x 2^21 batches of 256 trials (W15 < 7 x 2^29).  V counts every
# rare-path operation (scan, Sc operations, VCTRL per batch with a valid lane: V update, cap test and its branch,
# VLANE per valid lane, V3B per stage-3b entry); V changes and is tested only on such batches; halt when V > VMAX.
# GCTRL = 4 per group (zero k; add, compare, branch), charged by cert.py.  coins() returns a uniform 256-bit word.
OPS, BATCH = {}, {}
VCTRL, GCTRL, CINIT = 3, 4, 16

NBG = 7 << 21

def attack(R, P, NG, VMAX, coins, nbatch=NBG, hook=None):
    if R not in OPS: calibrate(R, P)
    B = BATCH[R]; V = 0
    for gi in range(NG):
        r0, r1 = coins(), coins(); gc, gs = group_setup(Sc(), R, (r0, r1)); mem = B.group(Sc(), gc)
        M0 = [(r0 >> (32 * j)) & M32 for j in range(8)] + [(r1 >> (32 * j)) & M32 for j in range(7)]
        for kb in range(nbatch):
            B.planes(mem, kb); F, A1, A2 = B.fast(mem); found = []
            if F != WORD:
                v = Sc(); v.n += VCTRL
                for L in lanes_of(v, F):
                    v.n += VLANE; cv = lane_cv(v, gs, kb, L, R)
                    li, X, Y, n3b = step3(v, P, cv); found.append((L, cv, li, n3b))
                    if li is not None:
                        res = verify(R, M0 + [(kb << 8) | L], X, Y)
                        if res:
                            if hook: hook(M0, kb, F, A1, A2, found)
                            return dict(pair=res, V=V + v.n, group=gi, batch=kb)
                V += v.n
                if V > VMAX: return dict(pair=None, V=V, group=gi, batch=kb, halted=True)
            if hook: hook(M0, kb, F, A1, A2, found)
    return dict(pair=None, V=V, group=NG, batch=0)

def calibrate(R, P):
    """Counts asserted equal over three groups: c_init, c_G, c_B (with categories), registers; one batch per group
    run by the emitted program equals the fast evaluator; Step-3 parts on the published pair's CV."""
    if R not in BATCH: BATCH[R] = Batch(R, P)
    B = BATCH[R]; res = None
    for seed in (1, 2, 3):
        cn = [seed]
        def coins():
            cn[0] += 1; return int.from_bytes(hashlib.sha256(b'cal%d' % cn[0]).digest(), 'big')
        sc = Sc(); gc, gs = group_setup(sc, R, (coins(), coins())); mem = B.group(sc, gc); cG = sc.n
        kb = coins() % NBG; B.planes(mem, kb); F = B.fast(mem)[0]
        assert B.counted(mem) == F, 'emitted program differs'
        sc2 = Sc(); lane_cv(sc2, gs, kb, 5, R); ccv = sc2.n
        cost = {}; sc3 = Sc(); out = step3(sc3, P, PAIRS[R]['cv'], cost)
        assert out[0] is not None and out[1] == PAIRS[R]['mp'] and out[2] == PAIRS[R]['m']
        regs = 1 + max(max(i[1], i[2], i[3]) if i[0] not in ('ld', 'st') else i[1] if i[0] == 'ld' else i[2] for i in B.prog)
        assert regs <= POOL
        lv = rare_liveness(R, P)
        cur = dict(c_init=CINIT, c_G=cG, groupconsts=len(gc), hoisted=len(B.hoist), c_B=B.cB, prog=len(B.prog),
                   cats=dict(sorted(B.cats.items())), regs=regs, scan=(LSCAN0, LSCAN1), c_cv=ccv, c01=cost['c01'],
                   c3a=cost['c3a'], crest=cost['crest'], c3b=cost['c3b'], live_cv=lv[0], live_lane=lv[1], live_3b=lv[2])
        assert res is None or res == cur, (res, cur)
        res = cur
    OPS[R] = res
    return res

# ---------------------------------------------------------------------------------------------------------
# Organizer experiment (python-message-pairs-v1).  Per seed: one group (W0..W14 from SHAKE-256(seed)), one batch of
# the driver above.  The hook recomputes every lane (ref_lanes; compress() too for lane 0 and valid lanes) and checks
# A_{R-1}, A_{R-2}, the W7/W6 decisions, the valid set and its CVs, and rows -4..15 of every valid lane's pair for the
# published l and l = trial mod 32.  Returns M0||M1, M0||M1' of the first valid lane (published l) if all pass.
NB_EXP = 1

def ref_lanes(M0, kb, R):
    """Scalar reference CVs of the 256 first blocks M0 || (2^8 kb + L)."""
    W = list(M0) + [0] * (R - 15); a, b, c, d, e, f, g, h = IV
    for i in range(15):
        t1 = (h + S1(e) + IF(e, f, g) + K[i] + W[i]) & M32; t2 = (S0(a) + MAJ(a, b, c)) & M32
        a, b, c, d, e, f, g, h = (t1 + t2) & M32, a, b, c, (d + t1) & M32, e, f, g
    st = (a, b, c, d, e, f, g, h); out = []; M = M32; Ks = K
    for L in range(256):
        W[15] = (kb << 8) | L
        for i in range(16, R):
            x, y = W[i - 2], W[i - 15]
            W[i] = ((((x >> 17) | (x << 15)) ^ ((x >> 19) | (x << 13)) ^ (x >> 10)) + W[i - 7] +
                    (((y >> 7) | (y << 25)) ^ ((y >> 18) | (y << 14)) ^ (y >> 3)) + W[i - 16]) & M
        a, b, c, d, e, f, g, h = st
        for i in range(15, R):
            t1 = h + ((((e >> 6) | (e << 26)) ^ ((e >> 11) | (e << 21)) ^ ((e >> 25) | (e << 7))) & M) + \
                ((e & f) ^ (~e & g)) + Ks[i] + W[i]
            t2 = ((((a >> 2) | (a << 30)) ^ ((a >> 13) | (a << 19)) ^ ((a >> 22) | (a << 10))) & M) + \
                ((a & b) ^ (a & c) ^ (b & c))
            a, b, c, d, e, f, g, h = (t1 + t2) & M, a, b, c, (d + t1) & M, e, f, g
        out.append([(x + y) & M32 for x, y in zip(IV, (a, b, c, d, e, f, g, h))])
    return out

def experiment(req):
    R = {'sha256-r37-prefix-v1': 37}[req['target_profile']]
    P = setup(R); cal = calibrate(R, P); lsfs = [d['w'][:2] for d in P['Lstar']].index(tuple(P['Wx'][14:16]))
    rows = []
    for tr in req['trials']:
        seed = bytes.fromhex(tr['seed']); ctr = [0]; lx = tr['trial'] % len(P['Lstar'])
        def coins():
            ctr[0] += 1; return int.from_bytes(hashlib.shake_256(seed + bytes([ctr[0]])).digest(32), 'big')
        obs = dict(lanes=0, mismatches=0, w7_pass=0, valid=0, stage3b=0, deepest_row=15, batch_ops=cal['c_B'])
        first = []
        def hook(M0, kb, F, A1, A2, found):
            fl = dict((f[0], f) for f in found); cvs = ref_lanes(M0, kb, R)
            pl = lambda w, k: [sum((((v[k] - IV[k]) & M32) >> j & 1) << L for L, v in enumerate(cvs)) for j in range(32)]
            obs['mismatches'] += (pl(cvs, 0) != A1) + (pl(cvs, 1) != A2)
            for L, cv in enumerate(cvs):
                blk = M0 + [(kb << 8) | L]; obs['lanes'] += 1
                p7 = inF((P['c7'] - cv[0]) & M32, P['d7'], P['t7'])
                W = ref_words(P, cv) if p7 else None; valid = p7 and inF(W[6], P['d6'], P['t6'])
                bad = valid != ((F >> L) & 1 == 0) or valid != (L in fl) or (L in fl and fl[L][1] != cv)
                bad |= (L == 0 or valid) and compress(IV, blk, R) != cv
                obs['w7_pass'] += p7
                if valid:
                    obs['valid'] += 1; obs['stage3b'] += fl[L][3]
                    Wy = W[:6] + [(W[6] + P['d6']) & M32, (W[7] + P['d7']) & M32]
                    for li in sorted({lsfs, lx}):
                        d = P['Lstar'][li]
                        X = W + P['Wx'][8:14] + list(d['w'][:2]); Y = Wy + P['Wy'][8:14] + list(d['w'][2:])
                        b = cellcheck(R, cv, X, Y)[0]
                        bad |= any(i < 16 and (k, i) not in (('W', 6), ('W', 7)) for k, i in b)
                        obs['deepest_row'] = max(obs['deepest_row'], min([i for _, i in b] + [R]) - 1)
                        if li == lsfs and not first: first.append((blk, X, Y))
                obs['mismatches'] += bad
        attack(R, P, 1, 1 << 60, coins, nbatch=NB_EXP, hook=hook)
        row = dict(trial=tr['trial'], message_a_hex=None, message_b_hex=None, observations=obs)
        if first and obs['mismatches'] == 0:
            blk, X, Y = first[0]
            row['message_a_hex'] = (struct.pack('>16I', *blk) + struct.pack('>16I', *X)).hex()
            row['message_b_hex'] = (struct.pack('>16I', *blk) + struct.pack('>16I', *Y)).hex()
        rows.append(row)
    return dict(schema_version=1, trials=rows)

# ---------------------------------------------------------------------------------------------------------
# Organizer experiment d1-q3-smc-r37 (H2; proof.md Section 10.2): smc.py's estimator of q3 at reduced size, with
# exact row 16 and exact draws from F7; every tail success is rebuilt and checked as a 37-step SFS collision.
FIX = {('A', 16, 29, '=', 'A', 17, 29): ('A', 15, 29, '=', 'A', 17, 29)}   # Section 3.3
KI = {'A': 0, 'E': 1, 'W': 4}
Q3X = dict(K=20, NP=64, MS={17: 4, 18: 4, 19: 1, 20: 1, 21: 1}, MT=512, POOL_LOG2=-74.35)

def xlist(R):
    out = {}
    for x in CH[R]['X']:
        x = FIX.get(x, x)
        if max(x[1], x[5]) >= 16: out.setdefault(max(x[1], x[5]), []).append(x)
    return out

def recipe(P, XL, kind, i):
    """As smc.propose: x-value cells, '+' bits, same-kind two-bit conditions of row i fixed; weight 2^-f."""
    m0, v, _, _ = row(CH[P['R']], kind, i); pq = P['rows'][i][3] if kind == 'E' else 0; m = det = m0 | pq; steps = []
    for w1, i1, b1, op, w2, i2, b2 in XL.get(i, ()):
        if w1 != kind or w2 != kind: continue
        for ia, ba, ib, bb in ((i2, b2, i1, b1), (i1, b1, i2, b2)):
            if ia == i and not det >> ba & 1 and (ib < i or det >> bb & 1 or ib == i and not m >> bb & 1):
                steps.append((ba, ib, bb, op == '!')); m |= 1 << ba; det |= 1 << ba | 1 << bb; break
    return i, m0, v & m0, pq, steps, bin(m).count('1')

def propose(rc, Wd, rnd):
    i, m0, v, pq, steps, f = rc; e = v | rnd & ~m0 & M32
    if pq: e = e & ~pq | Wd[i - 1] & pq
    for ba, ib, bb, fl in steps: e = e & ~(1 << ba) | ((Wd[ib] if ib < i else e) >> bb & 1 ^ fl) << ba
    return e

def rowok(P, XL, p, i):
    (mA, vA, dA, _), (mE, vE, dE, _), (mW, vW, dW, _), pq = P['rows'][i]; a, e, x = p[0][i], p[1][i], p[4][i]
    if a ^ p[2][i] != dA or a & mA != vA or e ^ p[3][i] != dE or e & mE != vE or x ^ p[5][i] != dW or x & mW != vW \
            or (e ^ p[1][i - 1]) & pq: return False
    return all((p[KI[w1]][i1] >> b1 ^ p[KI[w2]][i2] >> b2) & 1 == (op == '!') for w1, i1, b1, op, w2, i2, b2 in XL.get(i, ()))

def stp(A, E, Z, i): E[i] = stepE(A, E, i, Z[i]); A[i] = stepA(A, E, i)
def sch(Z, i): return (s1(Z[i-2]) + Z[i-7] + s0(Z[i-15]) + Z[i-16]) & M32

def particle(P, d):
    p = [[0] * P['R'] for _ in range(6)]
    for i in range(12, 16): p[0][i], p[1][i], p[2][i], p[3][i] = d['Ax'][i], d['Ex'][i], d['Ay'][i], d['Ey'][i]
    p[4][8:16] = P['Wx'][8:14] + list(d['w'][:2]); p[5][8:16] = P['Wy'][8:14] + list(d['w'][2:])
    return p

def r16(P, XL, d):
    """Row 16 of l: word k of p is e + c[k] (e = E16^x); every condition as parities by bit (see nx)."""
    p = particle(P, d); AX, EX, AY, EY, X, Y = p; rw = P['rows'][16]; cs = []
    X[16] = -stepE(AX, EX, 16, 0) & M32; Y[16] = (X[16] + s1(Y[14]) - s1(X[14]) + Y[9] - X[9]) & M32
    stp(AX, EX, X, 16); stp(AY, EY, Y, 16)
    for b in range(32):
        for (m, v, dd, _), x, y in ((rw[0], 0, 2), (rw[1], 1, 3), (rw[2], 4, 5)):
            cs += [([(x, b), (y, b)], dd >> b & 1)] + [([(x, b)], v >> b & 1)] * (m >> b & 1)
        cs += [([(1, b)], EX[15] >> b & 1)] * (rw[3] >> b & 1)
    for w1, i1, b1, op, w2, i2, b2 in XL[16]:
        t = ((w1, i1, b1), (w2, i2, b2))
        cs.append(([(KI[w], b) for w, i, b in t if i == 16], (op == '!') ^ sum(p[KI[w]][i] >> b for w, i, b in t if i < 16) & 1))
    by = [[] for _ in range(32)]; ns = 0
    for rf, v in cs:
        bs = sorted(set(b for _, b in rf)); j = ns if len(bs) > 1 else -1; ns += len(bs) > 1
        for b in bs: by[b].append((sum(1 << w for w, b_ in rf if b_ == b), j, b == bs[-1], int(v)))
    return [w[16] for w in p], by

def nx(c, by, b, s, e):
    """State after bit b = e (bits 0..5 carries, 6 + j open parity j), None if a condition fails."""
    w = 0; s2 = s >> 6 << 6
    for i in range(6):
        t = e + (c[i] >> b & 1) + (s >> i & 1); w |= (t & 1) << i; s2 |= (t >> 1) << i
    for m, j, last, v in by[b]:
        x = bin(w & m).count('1') & 1
        if j >= 0: x ^= s2 >> 6 + j & 1; s2 &= ~(1 << 6 + j)
        if not last: s2 |= x << 6 + j
        elif x != v: return None
    return s2

def cnt(c, by, memo, b, s):
    if b == 32: return 1
    if (b, s) not in memo:
        memo[b, s] = sum(cnt(c, by, memo, b + 1, t) for t in (nx(c, by, b, s, 0), nx(c, by, b, s, 1)) if t is not None)
    return memo[b, s]

def unrank(c, by, memo, r):
    s = e = 0
    for b in range(32):
        for x in (0, 1):
            t = nx(c, by, b, s, x); n = 0 if t is None else cnt(c, by, memo, b + 1, t)
            if r < n: e |= x << b; s = t; break
            r -= n
    return e

def row16(P, XL):
    out = []
    for d in P['Lstar']: c, by = r16(P, XL, d); memo = {}; out.append((c, by, memo, cnt(c, by, memo, 0, 0)))
    return out

def gauss(eqs):
    pv = {}
    for r, v in eqs:
        for b, (q, u) in pv.items():
            if r >> b & 1: r ^= q; v ^= u
        if not r:
            if v: return None
            continue
        b = r.bit_length() - 1
        for b2, (q, u) in list(pv.items()):
            if q >> b & 1: pv[b2] = (q ^ r, u ^ v)
        pv[b] = (r, v)
    x0 = sum(u << b for b, (q, u) in pv.items())
    return x0, [1 << f | sum(1 << b for b, (q, u) in pv.items() if q >> f & 1) for f in range(32) if f not in pv]

def fparts(d, t):
    """{w : s0(w + d) - s0(w) = t}: disjoint affine spaces, one per carry pattern c of w + d (proof.md 10.2)."""
    sr = [sum((s0(1 << i) >> j & 1) << i for i in range(32)) for j in range(32)]; out = []; n = [0]
    def walk(j, c, eqs):
        if j < 31:
            if (c ^ d) >> j & 1:
                for x in (0, 1): walk(j + 1, c | x << j + 1, eqs + [(1 << j, x)])
            else: walk(j + 1, c | (d & 1 << j) << 1, eqs)
            return
        M = s0(d ^ c); u = (M - t) & M32
        if u & 1 or u >> 1 & ~M & 0x7fffffff: return
        a = gauss(eqs + [(sr[i], u >> i + 1 & 1) for i in range(31) if M >> i & 1])
        if a: out.append((n[0],) + a); n[0] += 1 << len(a[1])
    walk(0, 0, [])
    return out, n[0]

def fdraw(F, r):
    i = len(F[0]) - 1
    while F[0][i][0] > r: i -= 1
    s, x, bs = F[0][i]; r -= s
    for v in bs:
        if r & 1: x ^= v
        r >>= 1
    return x

def sfs(P, p, W7):
    X, Y = p[4], p[5]; W = [0] * 6 + [(X[22] - s1(X[20]) - X[15] - s0(W7)) & M32, W7]
    for i in range(5, -1, -1): W[i] = (X[i+16] - s1(X[i+14]) - X[i+9] - s0(W[i+1])) & M32
    wx = W + X[8:16]; wy = W[:6] + [(W[6] + P['d6']) & M32, (W7 + P['d7']) & M32] + Y[8:16]
    A = dict(P['Sx'][0]); E = dict(P['Sx'][1])
    for i in range(7, -1, -1):
        a = (E[i] - A[i] + S0(A[i-1]) + MAJ(A[i-1], A[i-2], A[i-3])) & M32
        if i >= 4 and a != A[i-4]: return None
        A[i-4] = a; E[i-4] = (E[i] - a - S1(E[i-1]) - IF(E[i-1], E[i-2], E[i-3]) - K[i] - wx[i]) & M32
    cv = [A[-1], A[-2], A[-3], A[-4], E[-1], E[-2], E[-3], E[-4]]; R = P['R']
    ok = wx != wy and compress(cv, wx, R) == compress(cv, wy, R) and ref_words(P, cv) == wx[:8] and inF(W7, P['d7'], P['t7']) \
        and inF(W[6], P['d6'], P['t6']) and set(cellcheck(R, cv, wx, wy)[0]) <= {('W', 6), ('W', 7)}
    return (cv, wx, wy) if ok else None

def mini_smc(P, XL, V, rng, NP, MS, MT):
    V16, F7 = V; R = P['R']; n16 = sum(v[3] for v in V16); est = n16 / (len(V16) * 2.0 ** 32); st = [(16, n16)]; ps = []
    for _ in range(NP):
        r = rng.randrange(n16); li = 0
        while r >= V16[li][3]: r -= V16[li][3]; li += 1
        p = particle(P, P['Lstar'][li]); e = unrank(*V16[li][:3], r)
        for w, c in zip(p, V16[li][0]): w[16] = (e + c) & M32
        assert rowok(P, XL, p, 16); ps.append(p)
    for i in range(17, 22):
        rc = recipe(P, XL, 'E', i); sv = []
        for p in ps:
            AX, EX, AY, EY, X, Y = p; c = stepE(AX, EX, i, 0)
            dy = s1(Y[i-2]) - s1(X[i-2]) + Y[i-7] - X[i-7] + (P['t6'] if i == 21 else 0)
            for _ in range(MS[i]):
                X[i] = (propose(rc, EX, rng.getrandbits(32)) - c) & M32; Y[i] = (X[i] + dy) & M32
                stp(AX, EX, X, i); stp(AY, EY, Y, i)
                if rowok(P, XL, p, i): sv.append([z[:] for z in p])
        st.append((i, len(sv))); est *= len(sv) * 2.0 ** -rc[5] / (NP * MS[i])
        if not sv: return 0.0, st, 0, [], 0
        ps = [sv[rng.randrange(len(sv))] for _ in range(NP)]
    rc = recipe(P, XL, 'W', 22); hits = bad = 0; pairs = []; d6, t6, d7 = P['d6'], P['t6'], P['d7']
    for p in ps:
        AX, EX, AY, EY, X, Y = p; b6 = (s1(X[20]) + X[15]) & M32; y6 = s1(Y[20]) + Y[15] + d6
        b7 = s1(X[21]) + X[16] + s0(X[8]); y7 = s1(Y[21]) + Y[16] + s0(Y[8]) + d7
        for _ in range(MT):
            w22 = propose(rc, X, rng.getrandbits(32)); W7 = fdraw(F7, rng.randrange(F7[1])); W6 = (w22 - b6 - s0(W7)) & M32
            if not inF(W6, d6, t6): continue
            X[22] = w22; Y[22] = (y6 + s0((W7 + d7) & M32) + W6) & M32; X[23] = (b7 + W7) & M32; Y[23] = (y7 + W7) & M32
            for i in range(22, R):
                if i > 23: X[i] = sch(X, i); Y[i] = sch(Y, i)
                stp(AX, EX, X, i); stp(AY, EY, Y, i)
                if not rowok(P, XL, p, i): break
            else:
                hits += 1; r = sfs(P, p, W7)
                if r is None: bad += 1
                else: pairs.append(r)
    st.append(('tail', hits))
    return est * hits * 2.0 ** (32 - rc[5]) / P['F6'] / (NP * MT), st, hits, pairs, bad

def q3_experiment(req):
    """Trial t < K: a replicate, its first pair iff all verify; K: the last pair iff all did and mean >= 2^POOL_LOG2."""
    R = {'sha256-r37-prefix-v1': 37}[req['target_profile']]; P = setup(R); XL = xlist(R); K_ = Q3X['K']
    F7 = fparts(P['d7'], P['t7']); assert F7[1] == P['F7']; V = (row16(P, XL), F7); rows, zs, last = [], [], []
    def put(o, pr): o['message_a_hex'], o['message_b_hex'] = (struct.pack('>24I', *pr[0], *w).hex() for w in pr[1:])
    for tr in req['trials']:
        t = tr['trial']; o = dict(trial=t, message_a_hex=None, message_b_hex=None)
        if t < K_:
            rng = random.Random(int.from_bytes(hashlib.shake_256(b'd1-q3' + bytes.fromhex(tr['seed'])).digest(32), 'big'))
            z, st, hits, pairs, bad = mini_smc(P, XL, V, rng, Q3X['NP'], Q3X['MS'], Q3X['MT']); zs.append(z)
            o['observations'] = dict(log2_estimate=math.log2(z) if z else -1000.0, row16_words=st[0][1], tail_successes=hits,
                                     verified_pairs=len(pairs), failed_rebuilds=bad, **{'survivors_%s' % s: n for s, n in st[1:6]})
            if hits and not bad: put(o, pairs[0]); last.append(pairs[-1])
        elif t == K_:
            zb = sum(zs) / len(zs); o['observations'] = dict(log2_pooled_mean=math.log2(zb) if zb else -1000.0, replicates=len(zs))
            if len(last) == K_ and zb >= 2.0 ** Q3X['POOL_LOG2']: put(o, last[-1])
        rows.append(o)
    return dict(schema_version=1, trials=rows)

if __name__ == '__main__':
    req = json.loads(sys.stdin.read())
    out = q3_experiment(req) if req['experiment_id'].startswith('d1-q3-smc') else experiment(req)
    sys.stdout.write(json.dumps(out, sort_keys=True, separators=(',', ':')))
