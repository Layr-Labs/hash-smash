#!/usr/bin/env python3
# d1core.py - counted program of the d1 packages (sha256-r37-prefix-v1 / sha256-r38-prefix-v1).
# The two-block collision attack of Li, Zhang, Li, Liu, Qian and Zhu, "Pushing Collision Attacks on SHA-2 to
# 39 Steps", IACR ePrint 2026/1120 (CC BY), in the memory-efficient framework of [LLWS26] (Li, Liu, Wang, Shi,
# CRYPTO 2026), with their characteristics (Tables 15 / 3) and SFS pairs (Tables 17 / 5).  This file holds:
# the reduced SHA-256 (scalar reference), the characteristic cells, the SFS pairs, the Step-1 solution S read
# off the SFS pair, the exact freedom set L*, the counted 7x36 SWAR first-block batch with its Step-2 filter,
# the counted rare path, the counted scalar Step 3 (early abort), the target verification, the attack driver
# with fixed caps, and the entry point of three organizer experiments (stdin JSON -> stdout JSON): the
# first-block check, for 38 steps a reduced standard-library replica of smc.py, and the sigma1 identity check.
# Python 3.9+, stdlib.
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
# ePrint 2026/1120 Table 15 (37 steps) and Table 3 (38 steps): rows not listed are all '='.  MSB first.
# Member x is the message the paper prints second (M'); 'n' = (x, y) bits (0, 1), 'u' = (1, 0), '0'/'1' fixed
# and equal, '=' equal, '+' (undefined in the paper) read as E_i[b] = E_{i-1}[b] for vertical '+' pairs.
# X: Tables 16 / 4 two-bit conditions as printed (word, step, bit, op, word, step, bit); not used by the attack.
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
    ('W',24,4,'!','W',24,6),('W',24,22,'=','W',24,31),('W',24,20,'!','W',24,27)]),
 38: dict(
 A={7:'=nu=============================',8:'=========n=====n====n======u====',11:'====================u=======un==',
    12:'=u===n====n======u===nu=======n=',13:'==n============n================',14:'====u=========nn========u==u====',
    15:'======n=u=======n===============',17:'==u============================='},
 E={5:'+++=============================',6:'+++=1====0==+1=====0+===1==1====',7:'uuu=0+1=11=0+00====1+===0==00=01',
    8:'100=u+010n=1nu01=01nu=00n11u1=01',9:'11000u1=n11u0000101101110=01u0uu',10:'==1010=01u00001u=010u=101==10111',
    11:'1=n000=0111100101unn00011+111u10',12:'01nuuu=110n111nu000100100+010u1n',13:'00110101110=000u00111nuu+nnnu1n1',
    14:'=010n0===00===1n=11+0100+1110001',15:'=1==1=1==0=1==11===+u011n1011=1=',16:'=u==10===n===+u1===n0=u=1==+====',
    17:'=0=====+00===+0=+==01=0=0==+====',18:'=0=====+01===n1=+==1==1===0u====',19:'==11===nn====1==n===010===11==0=',
    20:'==1====00====1==0==========1====',21:'==u====10=======1===10==========',22:'==0=============================',
    23:'==1============================='},
 W={7:'==n=============================',8:'=====u===u==========n===========',9:'==u=============================',
    10:'=====n=u=======n===n==n=n=n=u=u=',11:'============u======u=u==========',15:'=====u===n==========n===========',
    16:'==u=============================',23:'=====1=uu=====1=u=1=============',25:'==n============================='},
 X=[('A',14,15,'=','A',16,15),('A',14,23,'=','A',16,23),('A',14,25,'=','A',16,25),('A',15,4,'=','A',16,4),
    ('A',15,7,'=','A',16,7),('A',15,16,'!','A',16,16),('A',15,17,'=','A',16,17),('A',15,27,'=','A',16,27),('A',15,29,'=','A',16,29),
    ('A',16,15,'=','A',17,15),('A',16,23,'=','A',17,23),('A',16,25,'=','A',17,25),('A',17,9,'=','A',17,20),
    ('A',17,6,'=','A',17,18),('A',17,8,'=','A',17,17),('A',16,29,'=','A',18,29),('A',18,29,'=','A',19,29),
    ('E',16,4,'!','E',16,23),('E',16,3,'!','E',16,8),('E',16,14,'=','E',16,28),('E',16,4,'=','E',17,4),('E',16,18,'=','E',17,18),
    ('E',18,0,'!','E',18,13),('E',17,15,'=','E',18,15),('E',17,24,'=','E',18,24),('E',19,6,'!','E',19,19),('E',19,20,'=','E',19,2),
    ('E',21,2,'=','E',21,16),
    ('W',7,8,'!','W',7,25),('W',7,14,'!','W',7,18),('W',7,1,'=','W',7,12),
    ('W',8,0,'!','W',8,28),('W',8,30,'!','W',8,9),('W',8,1,'=','W',8,18),
    ('W',16,1,'!','W',16,12),('W',16,20,'!','W',16,27),('W',16,8,'=','W',16,25),('W',16,14,'=','W',16,18),('W',16,4,'!','W',16,6),('W',16,22,'!','W',16,31),
    ('W',23,0,'!','W',23,30),('W',23,1,'!','W',23,31),('W',23,14,'=','W',23,21),('W',23,16,'=','W',23,25),
    ('W',25,4,'=','W',25,9),('W',25,22,'=','W',25,31),('W',25,20,'=','W',25,27)])}

def _h(s): return [int(t, 16) for t in s.split()]
# Tables 17 / 5: chaining value, M (printed first), M' (printed second = member x), printed hash.
PAIRS = {
 37: dict(cv=_h('63b4986c 35d83dc0 c98894e4 784e08fc 78a7f752 5ed877a8 315a2db3 d5614eb4'),
  m=_h('4d7f86ff 32ece589 d8accfc4 2cc2e433 068b5b34 eba68a28 2fe12cad 6aa26b0c 9f0d78e1 681b8277 faa9c7e0 56aed439 cc2dbbc2 dd2ba0fc b95d377b 5dd43a81'),
  mp=_h('4d7f86ff 32ece589 d8accfc4 2cc2e433 068b5b34 eba68a28 0fe12cad 6ee2630c bf0d78e1 6d1a90dd faa1d3e0 56aed439 cc2dbbc2 dd2ba0fc bd1d3f7b 7dd43a81'),
  hash=_h('a856d46e 4b46eb28 4935248c 92a2fc98 e0fb2610 10a9951f 54264f5b 80954580')),
 38: dict(cv=_h('cd278980 1b12a052 b87cc8a6 a9e059c5 c9c3db85 6ca4b5b5 63d13ac1 c0329f1e'),
  m=_h('48fc271b 9fca20cd cc89f96f fc40396f 8b328cb4 6b91ef78 97f9b767 e2450045 3b016f58 de9804cb 66a99ea5 0ce30b8d a28cd15a 77a1e994 d28e48a0 9b5f6dbb'),
  mp=_h('48fc271b 9fca20cd cc89f96f fc40396f 8b328cb4 6b91ef78 97f9b767 c2450045 3f416758 fe9804cb 63a88c0f 0ceb1f8d a28cd15a 77a1e994 d28e48a0 9f1f65bb'),
  hash=_h('5d9ca5f4 59ace3a3 26c9c26c 4252c585 4c0803b7 1b4d5ccd 25c3ccc0 90645c4d'))}

# Exact sizes of the Step-2 sets F = {w : s0(w + d) - s0(w) = t mod 2^32} (exhaustive counts over 2^32 words,
# proof.md Section 4.3; reproduced by fcount.c and sampled by selftest.py).
FSIZE = {(37, 7): 68157440, (37, 6): 287309824, (38, 7): 287309824}

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
         0xfdb436a1,0xfdb43a80,0xfdb43a81,0xfdb43aa0,0xfdb43aa1)],
         38: [(0xd28e48a0, 0x9f1f65bb)]}

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
# Machines.  A program is a sequence of calls on a machine m.  FastM executes it; CountM executes it and also
# counts every primitive by category, tracks a per-lane upper bound of every value (asserting that no ADD can
# carry across a 36-bit lane), and records definitions and uses for the register-liveness check.
L7, LW = 7, 36
CATS = ('rand', 'load', 'store', 'add', 'and', 'or', 'xor', 'shift', 'cmp', 'branch')
def pk(v): return sum((v & M32) << (LW * l) for l in range(L7))
def pkl(vals): return sum((vals[l] & M32) << (LW * l) for l in range(L7))
def unpk(x): return [(x >> (LW * l)) & M32 for l in range(L7)]
ROTS = (2, 6, 7, 11, 13, 17, 18, 19, 22, 25)
LANEMAX = (1 << LW) - 1

class FastM:
    """Uncounted execution (same program, same results)."""
    def __init__(self, mem=None):
        self.mem = {} if mem is None else mem
        self.M = pk(M32); self.G = sum(1 << (LW * l + 32) for l in range(L7)); self.ONE = pk(1)
        self.rlo = {r: pk(M32 >> r) for r in ROTS}; self.rhi = {r: pk((M32 << (32 - r)) & M32) for r in ROTS}
        self.sm = {3: pk(M32 >> 3), 10: pk(M32 >> 10)}
        self.coins = None
    def val(self, x): return x
    def LD(self, key): return self.mem[key]
    def ST(self, key, x): self.mem[key] = x
    def RAND(self): return self.coins()
    def ADD(self, a, b): return (a + b) & WORD
    def AND(self, a, b): return a & b
    def OR(self, a, b): return a | b
    def XOR(self, a, b): return a ^ b
    def SHR(self, a, k): return a >> k
    def SHL(self, a, k): return (a << k) & WORD
    def EQ(self, a, b): return a == b                       # compare + branch
    def IMM(self, v): return v                                # immediate operand (instruction field)
    # composites (each counts its parts)
    def mask(self, x): return self.AND(x, self.M)
    def ROTR(self, x, r): return self.OR(self.AND(self.SHR(x, r), self.rlo[r]), self.AND(self.SHL(x, 32 - r), self.rhi[r]))
    def SHR32(self, x, k): return self.AND(self.SHR(x, k), self.sm[k])
    def sig0(self, x): return self.XOR(self.XOR(self.ROTR(x, 7), self.ROTR(x, 18)), self.SHR32(x, 3))
    def sig1(self, x):
        # Clean guard bits; the shared shift cannot cross a 36-bit lane.
        x = self.mask(x)
        t = self.XOR(x, self.SHL(x, 2))
        right = self.AND(self.SHR(t, 19), self.rlo[17])
        left = self.AND(self.SHL(t, 13), self.rhi[19])
        return self.XOR(self.XOR(right, left), self.SHR32(x, 10))
    def BS0(self, x): return self.XOR(self.XOR(self.ROTR(x, 2), self.ROTR(x, 13)), self.ROTR(x, 22))
    def BS1(self, x): return self.XOR(self.XOR(self.ROTR(x, 6), self.ROTR(x, 11)), self.ROTR(x, 25))

class Val:
    __slots__ = ('v', 'b', 'id')
    def __init__(self, v, b, i): self.v = v; self.b = b; self.id = i

class CountM(FastM):
    """Counted execution: tick per primitive; per-lane bound; liveness trace (resident registers excluded)."""
    def __init__(self, mem=None):
        FastM.__init__(self, mem)
        self.ct = dict((c, 0) for c in CATS); self.t = 0; self.uses = {}; self.defs = {}; self.nid = 0
        self.resident = 3 + 2 * len(ROTS) + len(self.sm) + 2      # M, G, ONE, rotation and shift masks, w15, k
        R_ = lambda x, b: Val(x, b, None)
        self.M = R_(self.M, M32); self.G = R_(self.G, 1 << 32); self.ONE = R_(self.ONE, 1)
        self.rlo = dict((r, R_(v, M32 >> r)) for r, v in self.rlo.items())
        self.rhi = dict((r, R_(v, (M32 << (32 - r)) & M32)) for r, v in self.rhi.items())
        self.sm = dict((k, R_(v, M32 >> k)) for k, v in self.sm.items())
    def total(self): return sum(self.ct.values())
    def _new(self, v, b, cat):
        self.ct[cat] += 1; self.t += 1; self.nid += 1
        x = Val(v, b, self.nid); self.defs[self.nid] = self.t; return x
    def _use(self, *xs):
        for x in xs:
            if isinstance(x, Val) and x.id is not None: self.uses[x.id] = self.t + 1
    def val(self, x): return x.v if isinstance(x, Val) else x
    def LD(self, key):
        v, b = self.mem[key]; return self._new(v, b, 'load')
    def ST(self, key, x):
        self._use(x); self.ct['store'] += 1; self.t += 1; self.mem[key] = (x.v, x.b)
    def RAND(self): return self._new(self.coins(), WORD, 'rand')
    def ADD(self, a, b):
        self._use(a, b); bb = a.b + b.b
        assert bb <= LANEMAX, 'lane overflow possible'
        return self._new((a.v + b.v) & WORD, bb, 'add')
    def AND(self, a, b): self._use(a, b); return self._new(a.v & b.v, min(a.b, b.b), 'and')
    def OR(self, a, b): self._use(a, b); return self._new(a.v | b.v, (1 << max(a.b.bit_length(), b.b.bit_length())) - 1, 'or')
    def XOR(self, a, b): self._use(a, b); return self._new(a.v ^ b.v, (1 << max(a.b.bit_length(), b.b.bit_length())) - 1, 'xor')
    def SHR(self, a, k): self._use(a); return self._new(a.v >> k, LANEMAX, 'shift')
    def SHL(self, a, k): self._use(a); return self._new((a.v << k) & WORD, LANEMAX, 'shift')
    def EQ(self, a, b):
        self._use(a, b); self.ct['cmp'] += 1; self.ct['branch'] += 1; self.t += 2
        return self.val(a) == self.val(b)
    def IMM(self, v): return Val(v, v, None)
    def liveout(self, *xs): self._use(*xs)
    def maxlive(self):
        """Maximum number of simultaneously live values (defined, with a later use) over the program."""
        ev = []
        for i, d in self.defs.items():
            u = self.uses.get(i)
            if u is not None: ev.append((d, 1)); ev.append((u, -1))
        ev.sort(key=lambda z: (z[0], z[1])); live = best = 0
        for _, s in ev: live += s; best = max(best, live)
        return best

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

# ---------------------------------------------------------------------------------------------------------
# Program constants (written once at start: c_init stores), group setup, batch, rare path.
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

# Mask sites the structural lane-bound check of CountM proved unnecessary (found by nomask_search(); every
# ADD of the batch still satisfies bound <= 2^36 - 1, asserted on every counted run).
SKIP = {37: {('A', 20), ('A', 21), ('A', 25), ('A', 35), ('E', 35)} | set(('W', i) for i in range(17, 37) if i not in (18, 20)),
        38: {('A', 20), ('A', 21), ('A', 25), ('A', 36), ('E', 36)} | set(('W', i) for i in range(17, 38) if i not in (18, 20))}

def program_constants(R, P):
    c = {}
    for i in range(R): c[('K', i)] = pk(K[i])
    c['c7m'] = pk((P['c7'] - IV[0] + 1) & M32); c['d7'] = pk(P['d7']); c['t7'] = pk(P['t7'])
    c['IV0'] = pk(IV[0]); c['IV1'] = pk(IV[1]); c['base15'] = pkl([l << 29 for l in range(L7)])
    if R == 37:
        A, E = P['Sx']
        c['k3'] = pk(P['k3']); c['A1|A0'] = pk(A[1] | A[0]); c['A1&A0'] = pk(A[1] & A[0])
        c['E5&E4'] = pk(E[5] & E[4]); c['~E5'] = pk(E[5] ^ M32); c['k6'] = pk((P['c6'] + 2) & M32)
        c['d6'] = pk(P['d6']); c['t6'] = pk(P['t6'])
    return c

def install(m, R, P):
    """Write the packed program constants to memory; returns c_init (one store each)."""
    c = program_constants(R, P)
    for k, v in c.items(): m.mem[k] = (v, M32) if isinstance(m, CountM) else v
    return len(c)

BCAST = 7     # broadcast of a 32-bit value to 7 lanes: 3 shl + 3 or + 1 and

def group_setup(m, sc, R, words):
    """Per group: W0..W14 of M0 from two RAND words (shift + mask each), rounds 0..14 and the group constants
    on the scalar machine; each constant is masked, broadcast to the 7 lanes and stored."""
    w = [sc.m(sc.shr(words[j // 8], 32 * (j % 8))) for j in range(15)]
    a, b, c, d, e, f, g, h = [sc.ld(x) for x in IV]
    for i in range(15):
        t1 = sc.add(sc.add(sc.add(sc.add(h, sc.S1(e)), sc.IF(e, f, g)), sc.ld(K[i])), w[i])
        t2 = sc.add(sc.S0(a), sc.MAJ(a, b, c))
        a, b, c, d, e, f, g, h = sc.m(sc.add(t1, t2)), a, b, c, sc.m(sc.add(d, t1)), e, f, g
    A14, A13, A12, A11, E14, E13, E12 = a, b, c, d, e, f, g
    t1c = sc.add(sc.add(sc.add(h, sc.S1(e)), sc.IF(e, f, g)), sc.ld(K[15]))
    t2c = sc.add(sc.S0(a), sc.MAJ(a, b, c))
    Wc = dict(enumerate(w))
    for i in (16, 18, 20):
        Wc[i] = sc.m(sc.add(sc.add(sc.s1(Wc[i-2]), Wc[i-7]), sc.add(sc.s0(Wc[i-15]), Wc[i-16])))
    G = {}
    G['ke15'] = sc.add(A11, t1c); G['ka15'] = sc.add(t1c, t2c)
    G['E14^E13'] = sc.xor(E14, E13); G['E13'] = E13; G['k16'] = sc.add(sc.add(E12, sc.ld(K[16])), Wc[16])
    G['A14|A13'] = sc.or_(A14, A13); G['A14&A13'] = sc.and_(A14, A13); G['A12'] = A12
    G['E14'] = E14; G['k17'] = sc.add(E13, sc.ld(K[17])); G['A14'] = A14; G['A13'] = A13
    G['k18'] = sc.add(sc.add(E14, sc.ld(K[18])), Wc[18]); G['k20'] = sc.add(sc.ld(K[20]), Wc[20])
    var = varying(R)
    for i in sorted(var - {15}):
        cst = None
        for (j, fn) in ((i - 2, 's1'), (i - 7, None), (i - 15, 's0'), (i - 16, None)):
            if j in var: continue
            t = sc.s1(Wc[j]) if fn == 's1' else sc.s0(Wc[j]) if fn == 's0' else Wc[j]
            cst = t if cst is None else sc.add(cst, t)
        if cst is not None and foldK(R, i): cst = sc.add(cst, sc.ld(K[i]))
        if cst is not None: G[('W', i)] = cst
    cm = isinstance(m, CountM)
    for k, v in G.items():
        v = sc.m(v); sc.n += BCAST
        m.ST(('g', k), Val(pk(v), M32, None) if cm else pk(v))
    return len(G)

def batch(m, R):
    """The counted batch: rounds 15..R-1 of the 7 first blocks of the group whose W15 lanes are in m.w15, and
    the Step-2 W7 filter.  Returns (some lane passes W7, live-out registers for the rare path)."""
    LD = m.LD; var = varying(R); Wv = {15: m.w15}; sk = SKIP[R]
    def mk(name, x): return x if name in sk else m.mask(x)
    def sched(i):
        terms = []
        for (j, fn) in ((i - 2, 's1'), (i - 7, None), (i - 15, 's0'), (i - 16, None)):
            if j in var:
                x = Wv[j]; terms.append(m.sig1(x) if fn == 's1' else m.sig0(x) if fn == 's0' else x)
        x = terms[0]
        for t in terms[1:]: x = m.ADD(x, t)
        if ('g', ('W', i)) in m.mem: x = m.ADD(x, LD(('g', ('W', i))))
        Wv[i] = mk(('W', i), x)
    w15 = m.w15
    E15 = m.mask(m.ADD(LD(('g', 'ke15')), w15)); A15 = m.mask(m.ADD(LD(('g', 'ka15')), w15))
    # round 16: f, g, h, b, c, d are group constants
    ch = m.XOR(m.AND(E15, LD(('g', 'E14^E13'))), LD(('g', 'E13')))
    T1 = m.ADD(m.ADD(m.BS1(E15), ch), LD(('g', 'k16')))
    mj = m.OR(m.AND(A15, LD(('g', 'A14|A13'))), LD(('g', 'A14&A13')))
    T2 = m.ADD(m.BS0(A15), mj)
    E16 = m.mask(m.ADD(LD(('g', 'A12')), T1)); A16 = m.mask(m.ADD(T1, T2))
    # round 17: g, h, c, d constant; W17 varying
    sched(17)
    g_ = LD(('g', 'E14')); ch = m.XOR(m.AND(E16, m.XOR(E15, g_)), g_)
    T1 = m.ADD(m.ADD(m.ADD(m.BS1(E16), ch), Wv[17]), LD(('g', 'k17')))
    bc = m.XOR(A15, LD(('g', 'A14'))); ab = m.XOR(A16, A15); mj = m.XOR(m.AND(ab, bc), A15)
    T2 = m.ADD(m.BS0(A16), mj)
    E17 = m.mask(m.ADD(LD(('g', 'A13')), T1)); A17 = m.mask(m.ADD(T1, T2))
    # round 18: h, d constant; W18 constant
    ch = m.XOR(m.AND(E17, m.XOR(E16, E15)), E15)
    T1 = m.ADD(m.ADD(m.BS1(E17), ch), LD(('g', 'k18')))
    ab2 = m.XOR(A17, A16); mj = m.XOR(m.AND(ab2, ab), A16)
    T2 = m.ADD(m.BS0(A17), mj)
    E18 = m.mask(m.ADD(LD(('g', 'A14')), T1)); A18 = m.mask(m.ADD(T1, T2))
    a, b, c, d, e, f, g, h = A18, A17, A16, A15, E18, E17, E16, E15; prev = ab2
    for i in range(19, R):
        if i in var: sched(i)
        ch = m.XOR(m.AND(e, m.XOR(f, g)), g)
        if i == 20: T1 = m.ADD(m.ADD(m.ADD(h, m.BS1(e)), ch), LD(('g', 'k20')))
        elif foldK(R, i): T1 = m.ADD(m.ADD(m.ADD(h, m.BS1(e)), ch), Wv[i])
        else: T1 = m.ADD(m.ADD(m.ADD(m.ADD(h, m.BS1(e)), ch), Wv[i]), LD(('K', i)))
        xab = m.XOR(a, b); mj = m.XOR(m.AND(xab, prev), b); T2 = m.ADD(m.BS0(a), mj); prev = xab
        if i < R - 1:
            a, b, c, d, e, f, g, h = mk(('A', i), m.ADD(T1, T2)), a, b, c, mk(('E', i), m.ADD(d, T1)), e, f, g
        else:
            Alast = m.ADD(T1, T2)
    # Step-2 filter: W7 = c7 - IV0 - A[R-1]; a lane passes iff s0(W7 + d7) - s0(W7) = t7 (mod 2^32)
    xm = m.mask(Alast)
    W7 = m.mask(m.ADD(m.XOR(xm, m.M), LD('c7m')))
    W7p = m.mask(m.ADD(W7, LD('d7')))
    z = m.XOR(m.mask(m.ADD(m.sig0(W7), LD('t7'))), m.sig0(W7p))
    y = m.AND(m.ADD(z, m.M), m.G)                  # bit 32 of a lane is set iff the lane fails
    hit = not m.EQ(y, m.G)
    live = dict(xm=xm, a=a, b=b, c=c, d=d, T1=T1, e=e, f=f, g=g, y=y)
    if isinstance(m, CountM): m.liveout(*live.values())
    return hit, live

def batch_control(m):
    """Advance the 7 lane words (W15 += 1 in every lane) and the batch counter: add, add, compare, branch."""
    m.w15 = m.ADD(m.w15, m.ONE); m.k = m.ADD(m.k, m.IMM(1)); return m.EQ(m.k, m.IMM(1 << 29))

def w6_filter(m, live):
    """r37 rare path (once per batch with a W7 pass): SWAR W6 test, combined lane flags (bit 32 = fail)."""
    LD = m.LD
    A1 = m.mask(m.ADD(live['xm'], LD('IV0'))); A2 = m.mask(m.ADD(live['a'], LD('IV1')))
    E3 = m.mask(m.ADD(A1, LD('k3')))
    mj = m.OR(m.AND(A1, LD('A1|A0')), LD('A1&A0'))
    iv = m.XOR(LD('E5&E4'), m.AND(E3, LD('~E5')))
    W6 = m.mask(m.ADD(m.ADD(m.ADD(m.XOR(A2, m.M), mj), m.XOR(iv, m.M)), LD('k6')))
    W6p = m.mask(m.ADD(W6, LD('d6')))
    z = m.XOR(m.mask(m.ADD(m.sig0(W6), LD('t6'))), m.sig0(W6p))
    return m.OR(live['y'], m.AND(m.ADD(z, m.M), m.G))

def lanes_passing(m, y):
    """Scan the 7 lane flags (shift, and, compare, branch per lane)."""
    out = []
    for j in range(L7):
        if m.EQ(m.AND(m.SHR(y, LW * j + 32), m.IMM(1)), m.IMM(0)): out.append(j)
    return out

# ---------------------------------------------------------------------------------------------------------
# Step 3 (counted on Sc).
def lane_cv(sc, m, live, j):
    """CV1 of lane j: A[-1..-4] = (A_{R-1}, A_{R-2}, A_{R-3}, A_{R-4}) + IV0..3, E[-1] = d + T1 + IV4,
    E[-2..-4] = (E_{R-2}, E_{R-3}, E_{R-4}) + IV5..7 (shift the lane down, add, mask)."""
    g = lambda x: sc.shr(m.val(live[x]), LW * j)
    cv = [sc.m(sc.add(g(k), sc.ld(IV[i]))) for i, k in enumerate(('xm', 'a', 'b', 'c'))]
    cv.append(sc.m(sc.add(sc.add(g('d'), g('T1')), sc.ld(IV[4]))))
    cv += [sc.m(sc.add(g(k), sc.ld(IV[5 + i]))) for i, k in enumerate(('e', 'f', 'g'))]
    return cv

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
    if cost is not None: cost['c01'] = sc.n - n0
    rest = None; n3b = 0
    for li, d in enumerate(P['Lstar']):
        n1 = sc.n
        e16 = sc.m(sc.add(ld(d['ck16']), q))
        p3a = sc.eq(sc.xor(sc.and_(e16, ld(P['m16'])), ld(d['v16'])), 0)
        if cost is not None: cost['c3a'] = sc.n - n1
        if not p3a: continue
        n3b += 1; sc.n += FLAG3B; n2 = sc.n      # flag test at each stage-3b entry: are W2..W7 computed yet?
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

def ref_words(P, cv):
    """Reference (uncounted) W0..W7 of member x from CV1 by the paper's Step-2 equations."""
    A = dict(P['Sx'][0]); E = dict(P['Sx'][1])
    A[-1], A[-2], A[-3], A[-4], E[-1], E[-2], E[-3], E[-4] = cv
    for i in range(4): E[i] = (A[i] + A[i-4] - S0(A[i-1]) - MAJ(A[i-1], A[i-2], A[i-3])) & M32
    return [(E[i] - A[i-4] - E[i-4] - S1(E[i-1]) - IF(E[i-1], E[i-2], E[i-3]) - K[i]) & M32 for i in range(8)]

def inF(w, d, t): return d == 0 or ((s0((w + d) & M32) - s0(w)) & M32) == t

VFIN_UNITS, VFIN_OPS = 6, 512
FLAG3B = 2

def verify(R, M0, X, Y):
    """Target verification (charged VFIN_UNITS target compressions + VFIN_OPS operations, at most once):
    the complete 128-byte messages M0||M1 and M0||M1' are distinct and have equal R-step digests."""
    mx = struct.pack('>16I', *M0) + struct.pack('>16I', *X); my = struct.pack('>16I', *M0) + struct.pack('>16I', *Y)
    if mx != my and digest(mx, R) == digest(my, R): return mx, my
    return None

# ---------------------------------------------------------------------------------------------------------
# The attack with fixed caps.  NG groups of NB = 2^29 batches (7 trials each).  V counts every operation of the
# rare path (the SWAR W6 test and the lane scan at their exact straight-line counts OPS[R], every Sc operation,
# and VCTRL = 3 for the update of V and its cap test); the run halts with failure as soon as V exceeds VMAX.  The
# group loop costs GCTRL = 4 per group (zero the batch counter; add, compare, branch on the group counter),
# charged by cert.py with c_G.  coins() returns a uniform 256-bit word.
OPS = {}
VCTRL, GCTRL = 3, 4

def attack(R, P, NG, VMAX, coins, nbatch=1 << 29, hook=None):
    if R not in OPS: calibrate(R, P)
    m = FastM(); install(m, R, P); m.coins = coins; V = 0
    for gi in range(NG):
        sc = Sc(); r0, r1 = m.RAND(), m.RAND(); group_setup(m, sc, R, (r0, r1))
        M0 = [(r0 >> (32 * j)) & M32 for j in range(8)] + [(r1 >> (32 * j)) & M32 for j in range(7)]
        m.w15 = m.LD('base15'); m.k = m.IMM(0)
        for kb in range(nbatch):
            hit, live = batch(m, R); found = []
            if hit:
                v = Sc(); y = live['y']
                if R == 37: y = w6_filter(m, live); v.n += OPS[R]['w6']
                v.n += OPS[R]['scan'] + VCTRL
                for j in lanes_passing(m, y):
                    cv = lane_cv(v, m, live, j)
                    li, X, Y, n3b = step3(v, P, cv)
                    found.append((j, cv, li, n3b))
                    if li is not None:
                        res = verify(R, M0 + [(j << 29) + kb], X, Y)
                        if res:
                            if hook: hook(M0, kb, live, hit, found)
                            return dict(pair=res, V=V + v.n, group=gi, batch=kb)
                V += v.n
            if hook: hook(M0, kb, live, hit, found)
            if V > VMAX: return dict(pair=None, V=V, group=gi, batch=kb, halted=True)
            batch_control(m)
    return dict(pair=None, V=V, group=NG, batch=0)

def calibrate(R, P):
    """Exact operation counts, each asserted equal over three groups: c_init, c_G, c_B (batch + control) with
    categories, the r37 SWAR W6 test, the lane scan, the register high-water mark of the batch; and the Step-3
    parts on the published pair's chaining value: c_cv (lane_cv), c01, c3a (per l), crest, c3b (full pass)."""
    res = None
    for seed in (1, 2, 3):
        def coins(s=[seed]):
            s[0] += 1; return int.from_bytes(hashlib.sha256(b'cal%d' % s[0]).digest(), 'big')
        m = CountM(); ci = install(m, R, P); m.coins = coins; sc = Sc()
        r = (m.RAND(), m.RAND()); ng = group_setup(m, sc, R, (r[0].v, r[1].v))
        m.w15 = m.LD('base15'); m.w15.id = None; m.k = m.IMM(0)
        cG = m.total() + sc.n
        m.ct = dict((c, 0) for c in CATS); m.defs = {}; m.uses = {}; m.t = 0
        hit, live = batch(m, R); body = m.total(); cats = dict(m.ct); mx = m.maxlive()
        batch_control(m); cB = m.total()
        m2 = CountM(m.mem); w6 = 0
        if R == 37: w6_filter(m2, dict((k, Val(v.v, v.b, None)) for k, v in live.items())); w6 = m2.total()
        m3 = CountM(); lanes_passing(m3, Val(0, WORD, None)); scan = m3.total()
        sc2 = Sc(); lane_cv(sc2, m, live, 3); ccv = sc2.n
        cost = {}; sc3 = Sc(); out = step3(sc3, P, PAIRS[R]['cv'], cost)
        assert out[0] is not None and out[1] == PAIRS[R]['mp'] and out[2] == PAIRS[R]['m']
        cur = dict(c_init=ci, c_G=cG, groupconsts=ng, c_B=cB, body_filter=body, cats=cats, w6=w6, scan=scan,
                   maxlive=mx, resident=m.resident, c_cv=ccv, c01=cost['c01'], c3a=cost['c3a'],
                   crest=cost['crest'], c3b=cost['c3b'])
        assert res is None or res == cur, (res, cur)
        res = cur
    OPS[R] = res
    return res

def nomask_search(R, P):
    """Greedy: drop each mask site (schedule words, then state words from the last round down) when the
    structural per-lane bound check still passes for the whole batch and the W6 test."""
    sites = [('W', i) for i in sorted(varying(R) - {15})] + [(k, i) for i in range(R - 2, 18, -1) for k in ('E', 'A')]
    SKIP[R] = set()
    for s_ in sites:
        SKIP[R].add(s_)
        try:
            OPS.pop(R, None); calibrate(R, P)
        except AssertionError:
            SKIP[R].discard(s_)
    OPS.pop(R, None); calibrate(R, P)
    return sorted(SKIP[R])

# ---------------------------------------------------------------------------------------------------------
# Organizer experiment (python-message-pairs-v1).  Per organizer seed: one group of the attack with W0..W14 of
# M0 from SHAKE-256(seed), NB_EXP[R] batches of the driver above (same program; caps irrelevant here).  A hook
# checks every lane against the scalar compression (all 8 chaining-value words via lane_cv, the W7 decision, and
# for r37 the W6 decision), checks that every valid lane is exactly the set the driver sends to Step 3, and that
# for every valid lane and every l in L* the pair (M1, M1') follows every cell of rows -4..15.  The pair
# M0||M1, M0||M1' of the first valid lane (published W14, W15) is returned if every check passed, else nulls.
NB_EXP = {37: 16, 38: 3}

def experiment(req):
    R = {'sha256-r37-prefix-v1': 37, 'sha256-r38-prefix-v1': 38}[req['target_profile']]
    P = setup(R); cal = calibrate(R, P); lsfs = [d['w'][:2] for d in P['Lstar']].index(tuple(P['Wx'][14:16]))
    rows = []
    for tr in req['trials']:
        seed = bytes.fromhex(tr['seed']); ctr = [0]
        def coins():
            ctr[0] += 1; return int.from_bytes(hashlib.shake_256(seed + bytes([ctr[0]])).digest(32), 'big')
        obs = dict(lanes=0, mismatches=0, w7_pass=0, valid=0, stage3b=0, deepest_row=15, batch_ops=cal['c_B'])
        first = []
        def hook(M0, kb, live, hit, found):
            fl = dict((f[0], f) for f in found)
            for j in range(L7):
                blk = M0 + [(j << 29) + kb]; cv = compress(IV, blk, R); obs['lanes'] += 1
                bad = lane_cv(Sc(), FastM(), live, j) != cv
                p7 = inF((P['c7'] - cv[0]) & M32, P['d7'], P['t7'])
                bad |= p7 != ((live['y'] >> (LW * j + 32)) & 1 == 0)
                W = ref_words(P, cv); valid = p7 and inF(W[6], P['d6'], P['t6'])
                bad |= valid != (j in fl)
                obs['w7_pass'] += p7
                if valid:
                    obs['valid'] += 1; obs['stage3b'] += fl[j][3]
                    Wy = W[:6] + [(W[6] + P['d6']) & M32, (W[7] + P['d7']) & M32]
                    for li, d in enumerate(P['Lstar']):
                        X = W + P['Wx'][8:14] + list(d['w'][:2]); Y = Wy + P['Wy'][8:14] + list(d['w'][2:])
                        b = cellcheck(R, cv, X, Y)[0]
                        bad |= any(i < 16 and (k, i) not in (('W', 6), ('W', 7)) for k, i in b)
                        obs['deepest_row'] = max(obs['deepest_row'], min([i for _, i in b] + [R]) - 1)
                        if li == lsfs and not first: first.append((blk, X, Y))
                obs['mismatches'] += bad
        attack(R, P, 1, 1 << 60, coins, nbatch=NB_EXP[R], hook=hook)
        row = dict(trial=tr['trial'], message_a_hex=None, message_b_hex=None, observations=obs)
        if first and obs['mismatches'] == 0:
            blk, X, Y = first[0]
            row['message_a_hex'] = (struct.pack('>16I', *blk) + struct.pack('>16I', *X)).hex()
            row['message_b_hex'] = (struct.pack('>16I', *blk) + struct.pack('>16I', *Y)).hex()
        rows.append(row)
    return dict(schema_version=1, trials=rows)

# ---------------------------------------------------------------------------------------------------------
# Organizer experiment d1-q3-smc-r38 (H2; proof.md Section 10.2): smc.py's estimator of q3 for 38 steps,
# re-implemented with the standard library at reduced size.  Row 16 exactly: every E16 word with the proposal's
# constraints (x-value cells, '+' bits, E16-to-E16 two-bit conditions; 2^19 words) is checked against the whole
# row 16.  Rows 17..22: propose E_i^x (weight 2^-f, exact), W_i^x = E_i^x - (rest of step i), W_i^y = W_i^x + its
# exact difference, check the row, resample NP survivors uniformly.  Tail: propose W23 (cells and W23 conditions
# imposed), imply W7 (weight 1{W7 in F7} 2^(32-f) / |F7|), rows 23..37 deterministic.  Every tail success is
# rebuilt (W0..W7 by the inverse expansion, CV1 by inverting steps 7..0 from S) and checked with the reference
# compression as a 38-step semi-free-start collision whose CV1 passes Step 2 and whose cells hold on rows 16..37.
FIX = {38: {('W', 25, 4, '=', 'W', 25, 9): ('W', 25, 4, '=', 'W', 25, 6)}}   # the corrected reading (Section 3.3)
KI = {'A': 0, 'E': 1, 'W': 4}
Q3X = dict(K=20, NP=64, MS={17: 128, 18: 4, 19: 4, 20: 1, 21: 1, 22: 1}, MT=512, POOL_LOG2=-101.40)

def xlist(R):
    """X': the printed two-bit conditions with a word in rows >= 16 (one corrected), keyed by the later row."""
    out = {}
    for x in CH[R]['X']:
        x = FIX[R].get(x, x)
        if max(x[1], x[5]) >= 16: out.setdefault(max(x[1], x[5]), []).append(x)
    return out

def recipe(P, XL, kind, i):
    """Proposal of the x-side word of row i (as smc.propose): its x-value cells, '+' bits (E) and the same-kind
    two-bit conditions imposed; a step (ba, ib, bb, flip) sets bit ba to bit bb of row ib's word (of the word
    itself if ib == i), flipped for '!'.  2^-f is the exact probability of the constraints for a uniform word."""
    m0, v, _, _ = row(CH[P['R']], kind, i); m = m0; f = bin(m0).count('1'); pq = 0
    if kind == 'E': pq = P['rows'][i][3]; m |= pq; f += bin(pq).count('1')
    det = m; steps = []
    for (w1, i1, b1, op, w2, i2, b2) in XL.get(i, ()):
        if w1 != kind or w2 != kind: continue
        for (ia, ba, ib, bb) in ((i2, b2, i1, b1), (i1, b1, i2, b2)):
            if ia != i or (det >> ba) & 1: continue
            if ib < i or (det >> bb) & 1 or (ib == i and not (m >> bb) & 1):
                steps.append((ba, ib, bb, int(op == '!'))); m |= 1 << ba; det |= (1 << ba) | (1 << bb); f += 1
                break
    return i, m0, v & m0, pq, steps, f, M32 ^ m

def propose(rc, Wd, rnd):
    i, m0, v, pq, steps, f, _ = rc
    e = v | (rnd & (M32 ^ m0))
    if pq: e = (e & (M32 ^ pq)) | (Wd[i - 1] & pq)
    for ba, ib, bb, fl in steps: e = (e & (M32 ^ (1 << ba))) | (((((Wd[ib] if ib < i else e) >> bb) & 1) ^ fl) << ba)
    return e

def rowok(P, XL, p, i):
    """Row i of particle p = [AX, EX, AY, EY, X, Y]: every cell (A, E, W), the '+' pairs and X' of row i."""
    AX, EX, AY, EY, X, Y = p
    (mA, vA, dA, _), (mE, vE, dE, _), (mW, vW, dW, _), pq = P['rows'][i]
    if (AX[i] ^ AY[i]) != dA or (AX[i] & mA) != vA or (EX[i] ^ EY[i]) != dE or (EX[i] & mE) != vE or \
            (X[i] ^ Y[i]) != dW or (X[i] & mW) != vW or (EX[i] ^ EX[i - 1]) & pq: return False
    for (w1, i1, b1, op, w2, i2, b2) in XL.get(i, ()):
        if (((p[KI[w1]][i1] >> b1) ^ (p[KI[w2]][i2] >> b2)) & 1) != (op == '!'): return False
    return True

def cx(A, E, i): return (A[i-4] + E[i-4] + S1(E[i-1]) + IF(E[i-1], E[i-2], E[i-3]) + K[i]) & M32
def ca(A, i): return (S0(A[i-1]) + MAJ(A[i-1], A[i-2], A[i-3]) - A[i-4]) & M32
def stp(A, E, Z, i): E[i] = (cx(A, E, i) + Z[i]) & M32; A[i] = (E[i] + ca(A, i)) & M32
def sch(Z, i): return (s1(Z[i-2]) + Z[i-7] + s0(Z[i-15]) + Z[i-16]) & M32

def particle(P, d):
    p = [[0] * P['R'] for _ in range(6)]
    for i in range(12, 16): p[0][i], p[1][i], p[2][i], p[3][i] = d['Ax'][i], d['Ex'][i], d['Ay'][i], d['Ey'][i]
    p[4][8:16] = P['Wx'][8:14] + list(d['w'][:2]); p[5][8:16] = P['Wy'][8:14] + list(d['w'][2:])
    return p

def set16(p, e, dw):
    AX, EX, AY, EY, X, Y = p
    EX[16] = e; X[16] = (e - cx(AX, EX, 16)) & M32; Y[16] = (X[16] + dw) & M32
    AX[16] = (e + ca(AX, 16)) & M32; stp(AY, EY, Y, 16)

def row16(P, XL):
    """Exact row 16 for every l in L*: [(l index, E16^x)] over all 2^(32-f) proposal words, and f."""
    rc = recipe(P, XL, 'E', 16); free = [b for b in range(32) if (rc[6] >> b) & 1]
    lo = [sum(((x >> j) & 1) << b for j, b in enumerate(free[:11])) for x in range(1 << 11)]
    hi = [sum(((x >> j) & 1) << b for j, b in enumerate(free[11:])) for x in range(1 << (len(free) - 11))]
    out = []
    for li, d in enumerate(P['Lstar']):
        p = particle(P, d); AX, EX, AY, EY, X, Y = p
        c, a, dw, cy, ay = cx(AX, EX, 16), ca(AX, 16), (s1(Y[14]) - s1(X[14]) + Y[9] - X[9]) & M32, cx(AY, EY, 16), ca(AY, 16)
        for h in hi:
            for l_ in lo:
                e = propose(rc, EX, h | l_); EX[16] = e; AX[16] = (e + a) & M32; X[16] = (e - c) & M32
                Y[16] = (X[16] + dw) & M32; EY[16] = (cy + Y[16]) & M32; AY[16] = (EY[16] + ay) & M32
                if rowok(P, XL, p, 16): out.append((li, e))
    return out, rc[5]

def sfs(P, p, W7):
    """Rebuild a tail success: W0..W7, CV1 and the pair; None unless it is a verified semi-free-start collision."""
    X, Y = p[4], p[5]; W = {7: W7}
    W[6] = (X[22] - s1(X[20]) - X[15] - s0(W7)) & M32
    for i in (5, 4, 3, 2, 1, 0): W[i] = (X[i+16] - s1(X[i+14]) - X[i+9] - s0(W[i+1])) & M32
    wx = [W[i] for i in range(8)] + X[8:16]; wy = wx[:6] + [(W[6] + P['d6']) & M32, (W7 + P['d7']) & M32] + Y[8:16]
    A = dict(P['Sx'][0]); E = dict(P['Sx'][1])
    for i in range(7, -1, -1):
        a = (E[i] - A[i] + S0(A[i-1]) + MAJ(A[i-1], A[i-2], A[i-3])) & M32
        if i >= 4 and a != A[i-4]: return None
        A[i-4] = a; E[i-4] = (E[i] - a - S1(E[i-1]) - IF(E[i-1], E[i-2], E[i-3]) - K[i] - wx[i]) & M32
    cv = [A[-1], A[-2], A[-3], A[-4], E[-1], E[-2], E[-3], E[-4]]; R = P['R']
    ok = wx != wy and compress(cv, wx, R) == compress(cv, wy, R) and ref_words(P, cv) == wx[:8] and \
        inF(W7, P['d7'], P['t7']) and set(cellcheck(R, cv, wx, wy)[0]) <= {('W', 7)}
    return (cv, wx, wy) if ok else None

def below(rng, n):
    k = n.bit_length()
    while True:
        r = rng.getrandbits(k)
        if r < n: return r

def mini_smc(P, XL, V16, rng, NP, MS, MT):
    """One replicate: an unbiased estimate of q3 (smc.py's estimator at reduced size).  Returns (estimate,
    [(stage, survivors)], tail successes, rebuilt pairs, failed rebuilds)."""
    sets, f16 = V16; est = len(sets) / (len(P['Lstar']) * 2.0 ** 32); stages = [(16, len(sets))]; parts = []
    for _ in range(NP):
        li, e = sets[below(rng, len(sets))]; p = particle(P, P['Lstar'][li]); X, Y = p[4], p[5]
        set16(p, e, (s1(Y[14]) - s1(X[14]) + Y[9] - X[9]) & M32); parts.append(p)
    for i in range(17, 23):
        rc = recipe(P, XL, 'E', i); surv = []
        for p in parts:
            AX, EX, AY, EY, X, Y = p; c = cx(AX, EX, i)
            dy = s1(Y[i-2]) - s1(X[i-2]) + Y[i-7] - X[i-7]
            if i - 15 in (6, 7): dy += P['t%d' % (i - 15)]
            if i - 16 in (6, 7): dy += P['d%d' % (i - 16)]
            for _ in range(MS[i]):
                X[i] = (propose(rc, EX, rng.getrandbits(32)) - c) & M32; Y[i] = (X[i] + dy) & M32
                stp(AX, EX, X, i); stp(AY, EY, Y, i)
                if rowok(P, XL, p, i): surv.append([z[:] for z in p])
        stages.append((i, len(surv))); est *= len(surv) * 2.0 ** -rc[5] / (NP * MS[i])
        if not surv: return 0.0, stages, 0, [], 0
        parts = [surv[below(rng, len(surv))] for _ in range(NP)]
    rc = recipe(P, XL, 'W', 23); wt = 2.0 ** (32 - rc[5]) / P['F7']; hits = bad = 0; pairs = []
    for p in parts:
        AX, EX, AY, EY, X, Y = p; base = (s1(X[21]) + X[16] + s0(X[8])) & M32
        ybase = (s1(Y[21]) + Y[16] + s0(Y[8]) + P['d7']) & M32
        for _ in range(MT):
            w23 = propose(rc, X, rng.getrandbits(32)); W7 = (w23 - base) & M32
            if not inF(W7, P['d7'], P['t7']): continue
            X[23] = w23; Y[23] = (ybase + W7) & M32; ok = True
            for i in range(23, P['R']):
                if i > 23: X[i] = sch(X, i); Y[i] = sch(Y, i)
                stp(AX, EX, X, i); stp(AY, EY, Y, i)
                if not rowok(P, XL, p, i): ok = False; break
            if ok:
                hits += 1; r_ = sfs(P, p, W7)
                if r_ is None: bad += 1
                else: pairs.append(r_)
    stages.append(('tail', hits))
    return est * hits * wt / (NP * MT), stages, hits, pairs, bad

def q3_experiment(req):
    """Trials 0..K-1: one replicate each (randomness from SHAKE-256 of the organizer seed); trial t returns its
    first rebuilt pair (CV1 || M1, CV1 || M1', 96 bytes each) iff it has a tail success and every success was
    verified.  Trial K returns the last rebuilt pair iff every replicate passed and the mean of the K estimates
    is at least 2^POOL_LOG2.  Later trials return no pair by design."""
    R = {'sha256-r38-prefix-v1': 38}[req['target_profile']]; P = setup(R); XL = xlist(R); V16 = row16(P, XL)
    K_, rows, zs, allp, okall = Q3X['K'], [], [], [], True
    for tr in req['trials']:
        t = tr['trial']; row_ = dict(trial=t, message_a_hex=None, message_b_hex=None)
        if t < K_:
            seed = bytes.fromhex(tr['seed'])
            rng = random.Random(int.from_bytes(hashlib.shake_256(b'd1-q3' + seed).digest(32), 'big'))
            z, st, hits, pairs, bad = mini_smc(P, XL, V16, rng, Q3X['NP'], Q3X['MS'], Q3X['MT'])
            zs.append(z); allp += pairs; good = hits > 0 and bad == 0 and len(pairs) == hits; okall &= good
            row_['observations'] = dict([('log2_estimate', math.log2(z) if z > 0 else -1000.0), ('row16_words', len(V16[0])),
                                         ('tail_successes', hits), ('verified_pairs', len(pairs)), ('failed_rebuilds', bad)] +
                                        [('survivors_%s' % s, n) for s, n in st[1:7]])
            if good:
                cv, wx, wy = pairs[0]
                row_['message_a_hex'] = (struct.pack('>8I', *cv) + struct.pack('>16I', *wx)).hex()
                row_['message_b_hex'] = (struct.pack('>8I', *cv) + struct.pack('>16I', *wy)).hex()
        elif t == K_:
            zbar = sum(zs) / len(zs)
            row_['observations'] = dict(log2_pooled_mean=math.log2(zbar) if zbar > 0 else -1000.0, replicates=len(zs))
            if okall and len(zs) == K_ and zbar >= 2.0 ** Q3X['POOL_LOG2']:
                cv, wx, wy = allp[-1]
                row_['message_a_hex'] = (struct.pack('>8I', *cv) + struct.pack('>16I', *wx)).hex()
                row_['message_b_hex'] = (struct.pack('>8I', *cv) + struct.pack('>16I', *wy)).hex()
        rows.append(row_)
    return dict(schema_version=1, trials=rows)

def sigma1_identity(req):
    """Linear-map basis check, dirty guards and seed-derived words; no attack inference."""
    rows = []
    for tr in req['trials']:
        raw = hashlib.shake_256(bytes.fromhex(tr['seed'])).digest(16 * 32)
        xs = [int.from_bytes(raw[j:j+32], 'big') for j in range(0, len(raw), 32)]
        if tr['trial'] == 0:
            xs += [0, WORD] + [1 << j for j in range(256)] + [WORD ^ (1 << j) for j in range(256)]
        bad = 0
        for x in xs:
            expected = sum(s1((x >> (36 * lane)) & M32) << (36 * lane) for lane in range(7))
            bad += FastM().sig1(x) != expected
        cm = CountM(); cm.sig1(Val(WORD, LANEMAX, None))
        assert not bad and cm.total() == 11
        rows.append(dict(trial=tr['trial'], message_a_hex=None, message_b_hex=None,
                         observations=dict(vectors=len(xs), mismatches=bad, sigma1_ops=cm.total())))
    return dict(schema_version=1, trials=rows)

if __name__ == '__main__':
    req = json.loads(sys.stdin.read())
    out = sigma1_identity(req) if req['experiment_id'] == 'shared-sigma1-r38' else (
        q3_experiment(req) if req['experiment_id'].startswith('d1-q3-smc') else experiment(req))
    sys.stdout.write(json.dumps(out, sort_keys=True, separators=(',', ':')))
