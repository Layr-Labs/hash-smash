#!/usr/bin/env python3
# d1core.py - counted program of the d1 packages (sha256-r37-prefix-v1 / sha256-r38-prefix-v1), version bs1.
# The two-block collision attack of Li, Zhang, Li, Liu, Qian and Zhu, "Pushing Collision Attacks on SHA-2 to
# 39 Steps", IACR ePrint 2026/1120 (CC BY), in the memory-efficient framework of [LLWS26] (CRYPTO 2026), with
# their characteristics (Tables 15 / 3) and SFS pairs (Tables 17 / 5): reduced SHA-256, cells, SFS pairs, S, L*,
# a counted 256-lane bit-sliced first-block batch with the Step-2 and stage-3a filters in circuit, the counted
# rare path and Step 3 (early abort), verification, the driver with fixed caps, and the two organizer
# experiments (stdin JSON -> stdout JSON), for 38 steps with a reduced replica of smc.py.  Python 3.9+, stdlib.
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

class Sc:
    """Counted scalar machine: one 32-bit value per word; every primitive 1 (ld, add, sub, and, or, xor, shr, shl,
    compare, branch); m() masks; S0, S1, s0, s1 cost 8 (doubled word x | x << 32, 2 ops); inputs asserted masked."""
    def __init__(self): self.n = 0
    def ld(self, v): self.n += 1; return v
    def add(self, a, b): self.n += 1; return (a + b) & WORD
    def sub(self, a, b): self.n += 1; return (a - b) & WORD
    def m(self, a): self.n += 1; return a & M32
    def xor(self, a, b): self.n += 1; return a ^ b
    def and_(self, a, b): self.n += 1; return a & b
    def or_(self, a, b): self.n += 1; return a | b
    def shl(self, a, k): self.n += 1; return (a << k) & WORD
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

# Structural sets.
def varying(R):
    """Schedule words that depend on W15 (structural)."""
    v = {15}
    for i in range(16, R):
        if any(j in v for j in (i - 2, i - 7, i - 15, i - 16)): v.add(i)
    return v


# Step 3 (counted on Sc).
def stage3_constants(P):
    A, E = P['Sx']; c = {}
    c['kE1'] = (A[1] - S0(A[0])) & M32; c['kE2'] = (A[2] - S0(A[1])) & M32
    c['A1&A0'] = A[1] & A[0]; c['A1|A0'] = A[1] | A[0]
    c['kW4'] = (E[4] - A[0] - K[4]) & M32; c['kW5'] = (E[5] - A[1] - S1(E[4]) - K[5]) & M32
    c['kW6'] = (E[6] - A[2] - S1(E[5]) - K[6]) & M32; c['E5&E4'] = E[5] & E[4]; c['~E5'] = E[5] ^ M32
    return c

def step3(sc, P, cv, cost=None):
    """Counted Step 3 for one valid lane (cv = CV1).  Stage 3a per l in L*, then W2..W7 and stage 3b."""
    R = P['R']; ld = sc.ld; A, E = P['Sx']; c = P['s3c']; n0 = sc.n
    a1, a2, a3, a4, e1, e2, e3, e4 = cv
    e0_ = sc.sub(sc.sub(ld(A[0]), sc.S0(a1)), sc.MAJ(a1, a2, a3)); E0 = sc.m(sc.add(e0_, a4))
    w0 = sc.sub(sc.sub(sc.sub(e0_, e4), sc.S1(e1)), sc.IF(e1, e2, e3))
    e1_ = sc.sub(ld(c['kE1']), sc.MAJ(ld(A[0]), a1, a2)); E1 = sc.m(sc.add(e1_, a3))
    W1 = sc.m(sc.sub(sc.sub(sc.sub(sc.sub(e1_, e3), sc.S1(E0)), sc.IF(E0, e1, e2)), ld(K[1])))
    q = sc.add(sc.s0(W1), w0)
    if R == 37: m16 = ld(P['m16']); v16 = ld(P['Lstar'][0]['v16']); sc.keep = [E0, w0, E1, W1, q, m16, v16]
    else: sc.keep = [E0, w0, E1, W1, q]
    if cost is not None: cost['c01'] = sc.n - n0
    rest = None; n3b = 0
    for li, d in enumerate(P['Lstar']):
        n1 = sc.n
        e16 = sc.m(sc.add(ld((d['ck16'] - K[0]) & M32), q))
        p3a = sc.eq(sc.and_(e16, m16 if R == 37 else ld(P['m16'])), v16 if R == 37 else ld(d['v16']))
        if cost is not None: cost['c3a'] = sc.n - n1
        if not p3a: continue
        n3b += 1; sc.n += FLAG3B + V3B; n2 = sc.n
        if rest is None:
            W0 = sc.m(sc.sub(w0, ld(K[0])))
            e2_ = sc.sub(ld((c['kE2'] - c['A1&A0']) & M32), sc.and_(a1, ld(A[1] ^ A[0]))); E2 = sc.m(sc.add(e2_, a2))
            e3_ = ld(P['k3']); E3 = sc.m(sc.add(e3_, a1))
            W2 = sc.m(sc.sub(sc.sub(sc.sub(sc.sub(e2_, e2), sc.S1(E1)), sc.IF(E1, E0, e1)), ld(K[2])))
            W3 = sc.m(sc.sub(sc.sub(sc.sub(sc.sub(e3_, e1), sc.S1(E2)), sc.IF(E2, E1, E0)), ld(K[3])))
            W4 = sc.m(sc.sub(sc.sub(sc.sub(ld(c['kW4']), E0), sc.S1(E3)), sc.IF(E3, E2, E1)))
            W5 = sc.m(sc.sub(sc.sub(ld(c['kW5']), E1), sc.IF(ld(E[4]), E3, E2)))
            W6 = sc.m(sc.sub(sc.sub(ld((c['kW6'] - c['E5&E4']) & M32), E2), sc.and_(E3, ld(c['~E5']))))
            W7 = sc.m(sc.sub(ld(P['c7']), a1))
            rest = [W0, W1, W2, W3, W4, W5, W6, W7]
            rest_y = rest[:6] + [sc.m(sc.add(W6, ld(P['d6']))) if P['d6'] else W6, sc.m(sc.add(W7, ld(P['d7'])))]
            sc.keep_rest = rest + rest_y[6:]
            if cost is not None: cost['crest'] = sc.n - n2
        n4 = sc.n
        wx = P['Wx'][:14] + list(d['w'][:2]); wy = P['Wy'][:14] + list(d['w'][2:])
        X = rest + [ld(wx[i]) for i in range(8, 16)]; Y = rest_y + [ld(wy[i]) for i in range(8, 16)]
        Ax = dict((i, ld(d['Ax'][i])) for i in range(13, 16)); Ex = dict((i, ld(d['Ex'][i])) for i in range(13, 16))
        Ay = dict((i, ld(d['Ay'][i])) for i in range(13, 16)); Ey = dict((i, ld(d['Ey'][i])) for i in range(13, 16))
        ok = True
        for i in range(16, R):
            if i == 16:
                X.append(sc.m(sc.sub(e16, ld(d['c16'])))); Y.append(sc.m(sc.add(X[16], ld((s1(wy[14]) - s1(wx[14]) + wy[9] - wx[9]) & M32))))
            else:
                sh = sc.add(sc.s0(X[i-15]), X[i-16]) if i <= (20 if P['d6'] else 21) or (i >= 32 and i not in (37, 38, 39, 40) if P['d6'] else i >= 33 and i not in (38, 39, 40, 41)) else sc.s0(X[i-15]) if (i in (31, 37, 40) if P['d6'] else i in (32, 38, 41)) else None
                for Z, wz in ((X, wx), (Y, wy)):
                    w = sc.add(ld((s1(wz[15]) + wz[10]) & M32), sh) if i == 17 else \
                        sc.add(sc.s1(Z[i-2]), sc.add(Z[i-7], sh)) if i <= (20 if P['d6'] else 21) or (i >= 32 and i not in (37, 38, 39, 40) if P['d6'] else i >= 33 and i not in (38, 39, 40, 41)) else \
                        sc.add(sc.s1(Z[i-2]), sc.add(ld((wz[i-7] + s0(wz[i-15])) & M32) if i == 22 else Z[i-7], Z[6] if i == 22 else ld((s0(wz[i-15]) + wz[i-16]) & M32) if 24 <= i <= 30 else sc.add(ld(s0(wz[8])) if i == 23 else sh if sh is not None else sc.s0(Z[i-15]), Z[i-16])))
                    Z.append(sc.m(w))
            k = ld(K[i]) if i >= 20 else 0
            for (Aa, Ee, Z, dA, dE) in ((Ax, Ex, X, d['Ax'], d['Ex']), (Ay, Ey, Y, d['Ay'], d['Ey'])):
                ae = ld((dA[i-4] + dE[i-4] + K[i]) & M32) if i < 20 else sc.add(sc.add(Aa[i-4], Ee[i-4]), k)
                Ee[i] = e16 if i == 16 and Aa is Ax else sc.m(sc.add(ld((dA[12] + dE[12] + S1(dE[15]) + IF(dE[15], dE[14], dE[13]) + K[16]) & M32), Z[16]) if i == 16 else sc.add(sc.add(sc.add(ae, sc.S1(Ee[i-1])), sc.IF(Ee[i-1], Ee[i-2], Ee[i-3])), Z[i]))
                Aa[i] = sc.m(sc.add(Ee[16], ld((S0(dA[15]) + MAJ(dA[15], dA[14], dA[13]) - dA[12]) & M32)) if i == 16 else sc.add(sc.add(sc.sub(Ee[i], ld(dA[i-4]) if i < 20 else Aa[i-4]), sc.S0(Aa[i-1])), sc.MAJ(Aa[i-1], Aa[i-2], Aa[i-3])))
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
    """Sc with a liveness trace (value live from definition to last read; a rotation holds 2 temporaries)."""
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
    """Register demand of Step 3 for one lane on the published pair's CV."""
    cv0 = PAIRS[R]['cv']; li0 = [d['w'][:2] for d in P['Lstar']].index(tuple(P['Wx'][14:16]))
    sc = ScLive(); cv = [sc.ld(c) for c in cv0]
    P2 = dict(P); P2['Lstar'] = [d for i, d in enumerate(P['Lstar']) if i != li0]
    out = step3(sc, P2, cv); assert out[0] is None and out[3] == 0
    lane = sc.peak(pinned=cv + sc.keep)
    sc = ScLive(); cv = [sc.ld(c) for c in cv0]
    li, X, Y, n3b = step3(sc, P, cv); assert li == li0 and n3b == 1
    return lane, sc.peak()

def ref_words(P, cv):
    """Reference (uncounted) W0..W7 of member x from CV1 by the paper's Step-2 equations."""
    A = dict(P['Sx'][0]); E = dict(P['Sx'][1])
    A[-1], A[-2], A[-3], A[-4], E[-1], E[-2], E[-3], E[-4] = cv
    for i in range(4): E[i] = (A[i] + A[i-4] - S0(A[i-1]) - MAJ(A[i-1], A[i-2], A[i-3])) & M32
    return [(E[i] - A[i-4] - E[i-4] - S1(E[i-1]) - IF(E[i-1], E[i-2], E[i-3]) - K[i]) & M32 for i in range(8)]

def inF(w, d, t): return d == 0 or ((s0((w + d) & M32) - s0(w)) & M32) == t

VFIN_UNITS, VFIN_OPS = 6, 512
FLAG3B = 2
VLANE, VENT, SPILL3B = 1, 1, 148
V3B = VENT + SPILL3B

def verify(R, M0, X, Y):
    """Target verification: distinct, equal R-step digests."""
    mx = struct.pack('>16I', *M0) + struct.pack('>16I', *X); my = struct.pack('>16I', *M0) + struct.pack('>16I', *Y)
    if mx != my and digest(mx, R) == digest(my, R): return mx, my
    return None

CONE, CZERO = ('C', 1), ('C', 0)

class Net:
    def __init__(self): self.nodes, self.cse, self.inputs, self.grp, self.hdef = [], {}, {}, set(), {}
    def inp(self, name, grp=True):
        if name not in self.inputs:
            self.nodes.append(('in', name)); n = len(self.nodes) - 1; self.inputs[name] = n
            if grp: self.grp.add(n)
        return (self.inputs[name], 0)
    def gate(self, op, a, b):
        if a > b: a, b = b, a
        key = (op, a, b)
        if key in self.cse: return self.cse[key]
        if a in self.grp and b in self.grp:
            self.nodes.append(('in', 'H%d' % len(self.nodes))); n = len(self.nodes) - 1; self.hdef[n] = key; self.grp.add(n)
        else:
            self.nodes.append(key); n = len(self.nodes) - 1
        self.cse[key] = n; return n
    @staticmethod
    def isc(x): return x[0] == 'C'
    def NOT(self, x): return (x[0], 1 - x[1])
    def XOR(self, x, y):
        if self.isc(x): x, y = y, x
        if self.isc(y): return ('C', x[1] ^ y[1]) if self.isc(x) else (x[0], x[1] ^ y[1])
        if x[0] == y[0]: return ('C', x[1] ^ y[1])
        return (self.gate('xor', x[0], y[0]), x[1] ^ y[1])
    def AND(self, x, y):
        if self.isc(x): x, y = y, x
        if self.isc(y): return x if y[1] else CZERO
        if x[0] == y[0]: return x if x[1] == y[1] else CZERO
        if not x[1] and not y[1]: return (self.gate('and', x[0], y[0]), 0)
        if x[1] and y[1]: return (self.gate('or', x[0], y[0]), 1)
        if x[1]: x, y = y, x
        return (self.gate('and', self.gate('xor', x[0], y[0]), x[0]), 0)
    def OR(self, x, y): return self.NOT(self.AND(self.NOT(x), self.NOT(y)))
    def CH(self, e, f, g):
        if self.isc(e): return f if e[1] else g
        d = self.XOR(f, g)
        if self.isc(d): return self.XOR(g, self.AND(e, d))
        if d[1] == 0: return self.XOR(g if e[1] == 0 else f, (self.gate('and', e[0], d[0]), 0))
        return self.NOT(self.XOR(f if e[1] == 0 else g, (self.gate('or', e[0], d[0]), 0)))
    def MAJ(self, a, b, c):
        d1, d2 = self.XOR(a, b), self.XOR(b, c)
        if self.isc(d1) or self.isc(d2): return self.XOR(b, self.AND(d1, d2))
        if d1[1] == d2[1]:
            t = (self.gate('and' if d1[1] == 0 else 'or', d1[0], d2[0]), 0)
            return self.XOR(b, t) if d1[1] == 0 else self.NOT(self.XOR(b, t))
        return self.NOT(self.XOR(c if d1[1] == 0 else a, (self.gate('or', d1[0], d2[0]), 0)))

class Col:
    def __init__(self, net, nb=32): self.n, self.nb, self.carry, self.j = net, nb, [], 0
    def step(self, bits):
        n = self.n; col = self.carry + list(bits); self.carry = []; last = self.j == self.nb - 1
        k = sum(l[1] for l in col if n.isc(l)); col = [l for l in col if not n.isc(l)]
        if k >= 2 and not last: self.carry += [CONE] * (k // 2)
        if k % 2: col.append(CONE)
        while len(col) >= 3:
            if col[-1] is CONE:
                pr = next(((i, j) for i in range(len(col) - 1) for j in range(i + 1, len(col) - 1) if col[i][1] == col[j][1]), None)
                if pr:
                    b = col.pop(pr[1]); a = col.pop(pr[0]); col.pop()
                    if not last: self.carry.append(n.OR(a, b))
                    col.append(n.NOT(n.XOR(a, b))); continue
            a, b, c = col.pop(0), col.pop(0), col.pop(0)
            if last: col.append(n.XOR(n.XOR(a, b), c)); continue
            if c is CONE:
                self.carry.append(n.OR(a, b)); col.append(n.NOT(n.XOR(a, b))); continue
            t = n.XOR(a, b); col.append(n.XOR(t, c))
            self.carry.append(n.CH(t, c, a) if t[1] == 0 else n.CH((t[0], 0), a, c))
        if len(col) == 2:
            a, b = col
            if not last: self.carry.append(n.AND(a, b))
            col = [n.XOR(a, b)]
        self.j += 1
        return col[0] if col else CZERO

def operands(nd): return () if nd[0] == 'in' else (nd[1], nd[2])

class Cw:
    __slots__ = ('e',)
    def __init__(self, e): self.e = e

def lits(v): return [CONE if (v >> j) & 1 else CZERO for j in range(32)]
SIG = {'S0': (2, 13, 22, None), 'S1': (6, 11, 25, None), 's0': (7, 18, None, 3), 's1': (17, 19, None, 10)}

class Bld:
    def __init__(self, R): self.R = R; self.net = Net(); self.reg = {}
    def planes(self, w):
        if isinstance(w, list): return w
        if w.e[0] in ('K', 'IMM'): return lits(w.e[1] if w.e[0] == 'IMM' else K[w.e[1]])
        i = self.reg.setdefault(w.e, len(self.reg)); return [self.net.inp('G%d[%d]' % (i, j)) for j in range(32)]
    def fn(self, kind, ws):
        if all(isinstance(w, Cw) for w in ws): return Cw((kind,) + tuple(w.e for w in ws))
        n = self.net; p = [self.planes(w) for w in ws]
        if kind in SIG:
            r1, r2, r3, sh = SIG[kind]; q = p[0]
            def f(j):
                x = n.XOR(q[(j + r1) % 32], q[(j + r2) % 32])
                return n.XOR(x, q[(j + r3) % 32]) if r3 else n.XOR(x, q[j + sh] if j + sh < 32 else CZERO)
            return f
        if kind == 'CH': return lambda j: n.CH(p[0][j], p[1][j], p[2][j])
        return lambda j: n.MAJ(p[0][j], p[1][j], p[2][j])
    def prep(self, items, k=None):
        cs = [w.e for w in items if isinstance(w, Cw)]; fs = []
        for w in items:
            if isinstance(w, list): fs.append(lambda j, p=w: p[j])
            elif not isinstance(w, Cw): fs.append(w)
        if k is not None:
            if cs: cs.append(('K', k))
            else: fs.append(lambda j, p=lits(K[k]): p[j])
        if cs:
            cp = self.planes(Cw(('ADD',) + tuple(cs)) if len(cs) > 1 else Cw(cs[0])); fs.append(lambda j, p=cp: p[j])
        return fs
    def add(self, items, k=None):
        fs = self.prep(items, k); c = Col(self.net); return [c.step([f(j) for f in fs]) for j in range(32)]

def build(R):
    """Lock-step emission (W_t, T1, E_t, A_t at bit j).  Bit L of the fail plane is 0 iff lane L is valid."""
    b = Bld(R); n = b.net; var = varying(R); inl = {R - 2, R - 1}
    W = {i: Cw(('W', i)) for i in list(range(15)) + [i for i in range(16, R) if i not in var]}
    W[15] = ([n.inp('gb[%d]' % j) for j in range(8)] + [n.inp('uhi[%d]' % i, False) for i in range(16)]
             + [n.inp('lane[%d]' % i) for i in range(8)])
    A = {i: Cw(('A', i)) for i in range(11, 15)}; E = {i: Cw(('E', i)) for i in range(11, 15)}
    P = setup(R); Sa, Se = P['Sx']; A1, A0, E5, E4 = Sa[1], Sa[0], Se[5], Se[4]
    imm = lambda v: Cw(('IMM', v & M32)); neg = lambda p: [n.NOT(x) for x in p]
    wi = lambda t: [b.fn(fn, [W[u]]) if fn else W[u] for u, fn in ((t-2, 's1'), (t-7, None), (t-15, 's0'), (t-16, None))]
    for t in range(15, R):
        a, bb, c, d, e, f, g, h = A[t-1], A[t-2], A[t-3], A[t-4], E[t-1], E[t-2], E[t-3], E[t-4]
        dep = t in var and t > 15 and t not in inl; last = t == R - 1
        if dep: wf = b.prep(wi(t)); wc = Col(n); W[t] = []
        t1 = [b.fn('S1', [e]), h, b.fn('CH', [e, f, g])] + (wi(t) if t in inl else ([] if dep else [W[t]]))
        s0a, mj = b.fn('S0', [a]), b.fn('MAJ', [a, bb, c])
        nv = sum(not isinstance(x, Cw) for x in t1) + dep
        if last and P['d6']:
            af = b.prep(t1 + [s0a, mj, Cw(('IV', 0))], t); ac = Col(n); A[t] = []
        elif last:
            tf = b.prep(t1, t); tc = Col(n); ef = b.prep([d, imm(IV[4])]); ec = Col(n); af = b.prep([s0a, mj, imm(IV[0])]); ac = Col(n); E[t], A[t] = [], []
        elif nv >= 2:
            tf = b.prep(t1, t); tc = Col(n); ef = b.prep([d]); ec = Col(n); af = b.prep([s0a, mj]); ac = Col(n); E[t], A[t] = [], []
        else:
            ef = b.prep(t1 + [d], t); ec = Col(n); af = b.prep(t1 + [s0a, mj], t); ac = Col(n); E[t], A[t] = [], []
        for j in range(32):
            wj = []
            if dep: W[t].append(wc.step([q(j) for q in wf])); wj = [W[t][j]]
            if last and P['d6']: A[t].append(ac.step([q(j) for q in af] + wj))
            elif nv >= 2 or last:
                tj = tc.step([q(j) for q in tf] + wj)
                E[t].append(ec.step([tj] + [q(j) for q in ef])); A[t].append(ac.step([tj] + [q(j) for q in af]))
            else:
                E[t].append(ec.step([q(j) for q in ef] + wj)); A[t].append(ac.step([q(j) for q in af] + wj))
    am1 = A[R-1]
    def fails(w, dd, tt):
        if dd == 0x20000000 and tt == 0x03bff800:
            f0 = n.OR(n.OR(n.XOR(w[1], w[12]), n.NOT(n.XOR(w[8], w[25]))), n.NOT(n.XOR(w[14], w[18])))
            f1 = n.OR(n.OR(n.XOR(w[2], w[13]), n.NOT(n.XOR(w[9], w[26]))), n.NOT(n.XOR(w[15], w[19])))
            w3_14 = n.XOR(w[3], w[14])
            f2 = n.OR(n.OR(n.XOR(w3_14, w[31]), n.NOT(n.XOR(w3_14, n.XOR(w[10], w[27])))), n.NOT(n.XOR(w3_14, n.XOR(w[16], w[20]))))
            return n.OR(f0, n.AND(w[29], n.OR(f1, n.AND(w[30], f2))))
        u = b.fn('s0', [b.add([w, imm(dd)]) if dd else w]); v = b.add([b.fn('s0', [w]), imm(tt)]); acc = None
        for j in range(32):
            x = n.XOR(u(j), v[j]); acc = x if acc is None else n.OR(acc, x)
        return acc
    fail = fails(b.add([neg(am1), imm(P['c7'] + 1)]), P['d7'], P['t7'])
    if P['d6']:
        e3 = b.add([am1, imm(P['k3'])])
        mjw = [am1[j] if ((A1 ^ A0) >> j) & 1 else lits(A1)[j] for j in range(32)]
        ivw = [lits(E4)[j] if (E5 >> j) & 1 else e3[j] for j in range(32)]
        w6 = b.add([neg(A[R-2]), mjw, neg(ivw), imm(P['c6'] - IV[1] + 2)])
        return b, n.OR(fail, fails(w6, P['d6'], P['t6']))
    e1 = E[R-1]; c = P['s3c']; ngate = lambda f: (lambda j, f=f: n.NOT(f(j)))
    a2 = b.add([A[R-2], imm(IV[1])]); a3 = b.add([A[R-3], imm(IV[2])]); e2 = b.add([E[R-2], imm(IV[5])])
    s0a1, mjA = b.fn('S0', [am1]), b.fn('MAJ', [am1, a2, a3]); Smj = b.add([s0a1, mjA])
    E0 = b.add([A[R-4], neg(Smj), imm(A0 + IV[3] + 1)])
    mjB = b.fn('MAJ', [lits(A0), am1, a2]); s1E0, ifE0 = b.fn('S1', [E0]), b.fn('CH', [E0, e1, e2])
    W1 = b.add([ngate(s1E0), ngate(ifE0), ngate(mjB), neg(E[R-3]), imm(c['kE1'] - K[1] - IV[6] + 4)])
    e3f = b.prep([E[R-3], imm(IV[6])]); e3c = Col(n, nb=31)
    e3 = [e3c.step([q(j) for q in e3f]) for j in range(31)] + [CZERO]
    s1e1, ife = b.fn('S1', [e1]), b.fn('CH', [e1, e2, e3])
    d = P['Lstar'][0]
    assert not d['v16'] & ~P['m16'] & M32
    fs = b.prep([b.fn('s0', [W1]), ngate(ife), neg(E[R-4]), ngate(s1e1), neg(Smj), imm(A0 - K[0] - IV[7] + 4 + d['ck16'])])
    col_e16 = Col(n, nb=31); e16 = [col_e16.step([f(j) for f in fs]) for j in range(31)]; acc = fail
    for j in range(31):
        if (P['m16'] >> j) & 1:
            acc = n.OR(acc, n.XOR(e16[j], CONE if (d['v16'] >> j) & 1 else CZERO))
    return b, acc

NREG, BCTRL, TEST = 64, 3, 2

def emit(net, fail, nreg=NREG):
    """Furthest-next-use allocation; r[0..15] batch planes, r[nreg-1] the spillable counter b; every load and
    store explicit.  'test' reads the fail plane (and the ones plane if unnegated), 'loop' reads b."""
    need, st = set(), [fail[0]]
    while st:
        x = st.pop()
        if x not in need: need.add(x); st.extend(operands(net.nodes[x]))
    ones = net.inp('ones')[0]; need.add(ones)
    order = [i for i in range(len(net.nodes)) if i in need and net.nodes[i][0] != 'in'] + ['test', 'loop']
    def opd(x):
        if x == 'test': return (fail[0],) if fail[1] else (fail[0], ones)
        return ('B',) if x == 'loop' else operands(net.nodes[x])
    uses = {}
    for pos, x in enumerate(order):
        for o in opd(x): uses.setdefault(o, []).append(pos)
    INF = 1 << 60; ptr = {}
    def nxt(v, pos):
        u = uses.get(v, ()); i = ptr.get(v, 0)
        while i < len(u) and u[i] < pos: i += 1
        ptr[v] = i; return u[i] if i < len(u) else INF
    uh = [net.inputs['uhi[%d]' % i] for i in range(16)]
    reg = dict((v, i) for i, v in enumerate(uh)); reg['B'] = nreg - 1
    free = [r for r in range(nreg) if r not in reg.values()][::-1]
    inmem = set(i for i in need if net.nodes[i][0] == 'in' and i not in uh); prog = []
    def take(pos, prot):
        if not free:
            v = max((v for v in reg if v not in prot), key=lambda v: nxt(v, pos)); r = reg.pop(v)
            if nxt(v, pos) < INF and v not in inmem: prog.append(('st', v, r)); inmem.add(v)
            free.append(r)
        return free.pop()
    for pos, x in enumerate(order):
        ops = opd(x)
        for o in ops:
            if o not in reg: reg[o] = take(pos, set(ops)); prog.append(('ld', reg[o], o))
        src = [reg[o] for o in ops]
        for o in set(ops):
            if nxt(o, pos + 1) >= INF: free.append(reg.pop(o))
        if x in ('test', 'loop'): prog.append((x,) + tuple(src)); continue
        rd = take(pos + 1, set()); reg[x] = rd; prog.append((net.nodes[x][0], rd, src[0], src[1]))
    return prog

def run_vm(prog, mem, b, fpol, nreg=NREG):
    r = [0] * nreg; r[nreg - 1] = b; ops = 0
    for i in range(16): r[i] = (0 - ((r[nreg - 1] >> i) & 1)) & WORD; ops += 3
    hit = fl = None
    for ins in prog:
        o = ins[0]
        if o == 'ld': r[ins[1]] = mem[ins[2]]; ops += 1
        elif o == 'st': mem[ins[1]] = r[ins[2]]; ops += 1
        elif o == 'xor': r[ins[1]] = r[ins[2]] ^ r[ins[3]]; ops += 1
        elif o == 'and': r[ins[1]] = r[ins[2]] & r[ins[3]]; ops += 1
        elif o == 'or': r[ins[1]] = r[ins[2]] | r[ins[3]]; ops += 1
        elif o == 'test':
            fl = r[ins[1]] ^ (WORD if fpol else 0); hit = (r[ins[1]] != 0) if fpol else (r[ins[1]] != r[ins[2]]); ops += TEST
        else: r[nreg - 1] = r[ins[1]] + 1; ops += BCTRL
    return ops, fl, hit, r[nreg - 1]

class Prog:
    def __init__(self, R):
        self.R = R; self.b, self.fail = build(R); net = self.b.net
        need, st = set(), [self.fail[0]]
        while st:
            x = st.pop()
            if x not in need: need.add(x); st.extend(net.hdef[x][1:] if x in net.hdef else operands(net.nodes[x]))
        oc = {'xor': 0, 'and': 1, 'or': 2}; self.ins, self.code, self.nv = [], [], len(net.nodes); net.cse = None
        for x in sorted(need):
            nd = net.nodes[x]
            if x in net.hdef: op, p, q = net.hdef[x]; self.code.append((x, oc[op], p, q))
            elif nd[0] == 'in': self.ins.append((x, nd[1]))
            else: self.code.append((x, oc[nd[0]], nd[1], nd[2]))
    def f(s, I):
        v = [0] * s.nv
        for x, nm in s.ins: v[x] = I[nm]
        for x, o, p, q in s.code: v[x] = v[p] ^ v[q] if o == 0 else v[p] & v[q] if o == 1 else v[p] | v[q]
        return v[s.fail[0]] ^ (WORD if s.fail[1] else 0)
    def inputs(self, base, gb, b):
        I = {}; reg = self.b.reg; sc = Sc(); memo = {}
        for e, i in reg.items():
            v = cval_sc(sc, e, base, memo)
            for j in range(32): I['G%d[%d]' % (i, j)] = WORD if (v >> j) & 1 else 0
        for j in range(8): I['gb[%d]' % j] = WORD if (gb >> j) & 1 else 0
        for i in range(16): I['uhi[%d]' % i] = WORD if (b >> i) & 1 else 0
        for i in range(8): I['lane[%d]' % i] = sum(1 << L for L in range(256) if (L >> i) & 1)
        I['ones'] = WORD; return I
    def fail_plane(s, base, gb, b): return s.f(s.inputs(base, gb, b))


def group_base(sc, R, w):
    base = dict((('W', i), w[i]) for i in range(15)); a, b, c, d, e, f, g, h = [sc.ld(x) for x in IV]
    for i in range(15):
        t1 = sc.add(sc.add(sc.add(sc.add(h, sc.S1(e)), sc.IF(e, f, g)), sc.ld(K[i])), w[i])
        t2 = sc.add(sc.S0(a), sc.MAJ(a, b, c))
        a, b, c, d, e, f, g, h = sc.m(sc.add(t1, t2)), a, b, c, sc.m(sc.add(d, t1)), e, f, g
        base[('A', i)], base[('E', i)] = a, e
    var = varying(R)
    for i in range(16, R):
        if i not in var:
            base[('W', i)] = sc.m(sc.add(sc.add(sc.s1(base[('W', i-2)]), base[('W', i-7)]), sc.add(sc.s0(base[('W', i-15)]), base[('W', i-16)])))
    return base

def cval_sc(sc, e, base, memo):
    if e in memo: return memo[e]
    o = e[0]
    if o in ('W', 'A', 'E'): v = base[e]
    elif o in ('K', 'IV', 'IMM'): v = sc.ld(K[e[1]] if o == 'K' else IV[e[1]] if o == 'IV' else e[1])
    else:
        a = [cval_sc(sc, x, base, memo) for x in e[1:]]
        if o == 'ADD':
            v = a[0]
            for x in a[1:]: v = sc.add(v, x)
            v = sc.m(v)
        elif o in SIG: v = getattr(sc, o)(a[0])
        else: v = (sc.IF if o == 'CH' else sc.MAJ)(*a)
    memo[e] = v; return v

GPLANE = 4

def group_setup(sc, pg, R, r0, r1):
    """Counted: 2 RAND, unpack, rounds 0..14, constant words and planes, gb planes, hoisted gates, stores."""
    w = [(r0 >> (32 * j)) & M32 for j in range(8)] + [(r1 >> (32 * j)) & M32 for j in range(7)]; gb = (r1 >> 224) & 255
    sc.n += 2 + 2 * 15 + 2
    base = group_base(sc, R, w); memo = {}
    for e, idx in pg.b.reg.items(): base[idx] = cval_sc(sc, e, base, memo)
    sc.n += (GPLANE * 32 + 1) * len(pg.b.reg) + GPLANE * 8 + 4 * len(pg.b.net.hdef) + 15 + 1 + 8
    return base, w, gb

def lane_cv(sc, R, base, gb, b, L):
    """CV1 of lane L of batch b recomputed from the stored group state (rounds 15..R-1, feed-forward)."""
    ld = sc.ld
    if 0 in base:
        w15 = sc.or_(sc.or_(sc.shl(L, 24), sc.shl(b, 8)), ld(gb)); W = {15: w15, 20: ld(base[('W', 20)])}
        a, b_, c = [ld(base[('A', i)]) for i in (14, 13, 12)]; e, f, g = [ld(base[('E', i)]) for i in (14, 13, 12)]
        a, b_, c, d, e, f, g, h = sc.m(sc.add(ld(base[1]), w15)), a, b_, c, sc.m(sc.add(ld(base[0]), w15)), e, f, g
        wc = {17: 8, 19: 11, 21: 13, 22: 14, 23: 15, 24: 16, 25: 17, 26: 18, 27: 19, 28: 20, 29: 21, 30: ('W', 14), 31: 23, 32: ('W', 16), 33: 25, 34: ('W', 18), 35: 27, 36: 28}
        tc = {16: 6, 18: 10, 20: 12}
        for i in range(16, R):
            if i not in tc:
                wi = sc.add(sc.s1(W[i-2]), ld(base[wc[i]])) if i in (17, 19, 21, 23, 25, 27) else \
                     sc.add(W[15], ld(base[14])) if i == 22 else \
                     sc.add(sc.add(sc.s1(W[i-2]), W[i-7]), ld(base[wc[i]])) if i <= 29 else \
                     sc.add(sc.add(sc.add(sc.s1(W[i-2]), W[i-7]), sc.s0(W[i-15])), W[i-16]) if i == 37 else \
                     sc.add(sc.add(sc.add(sc.s1(W[i-2]), W[i-7]), ld(base[wc[i]]) if i % 2 else sc.s0(W[i-15])), W[i-16] if i % 2 else ld(base[wc[i]]))
                if i < R - 2: W[i] = sc.m(wi)
            t1 = sc.add(sc.add(sc.S1(e), sc.IF(e, f, g)) if i <= 18 else sc.add(sc.add(h, sc.S1(e)), sc.IF(e, f, g)),
                        ld(base[tc[i]]) if i in tc else sc.add(ld(base[9]), W[17]) if i == 17 else wi if (i == 35 and R == 37) or i == 36 else sc.add(ld(K[i]), wi if i >= R - 2 else W[i]))
            t2 = sc.add(sc.S0(a), sc.MAJ(a, b_, c))
            a, b_, c, d, e, f, g, h = sc.m(sc.add(t1, t2)), a, b_, c, sc.m(sc.add(sc.sub(d, ld(IV[0])) if i == 36 and R == 37 else d, t1)), e, f, g
        return [sc.m(sc.add(x, ld(v))) if j or R > 37 else a for j, (x, v) in enumerate(zip((a, b_, c, d, e, f, g, h), IV))]
    W = dict((i, ld(base[('W', i)])) for i in range(15))
    W[15] = sc.or_(sc.or_(sc.shl(L, 24), sc.shl(b, 8)), ld(gb))
    for i in range(16, R): W[i] = sc.m(sc.add(sc.add(sc.s1(W[i-2]), W[i-7]), sc.add(sc.s0(W[i-15]), W[i-16])))
    a, b_, c, d = [ld(base[('A', i)]) for i in (14, 13, 12, 11)]; e, f, g, h = [ld(base[('E', i)]) for i in (14, 13, 12, 11)]
    for i in range(15, R):
        t1 = sc.add(sc.add(sc.add(sc.add(h, sc.S1(e)), sc.IF(e, f, g)), ld(K[i])), W[i])
        t2 = sc.add(sc.S0(a), sc.MAJ(a, b_, c))
        a, b_, c, d, e, f, g, h = sc.m(sc.add(t1, t2)), a, b_, c, sc.m(sc.add(d, t1)), e, f, g
    return [sc.m(sc.add(x, ld(v))) for x, v in zip((a, b_, c, d, e, f, g, h), IV)]

SCANB, SCANL = 4, 45

def lanes_passing(sc, fl):
    x = fl ^ WORD; sc.n += SCANB; out = []
    while x:
        low = x & -x; out.append(low.bit_length() - 1); x ^= low; sc.n += SCANL
    return out

OPS = {}; PROG = {}
VCTRL, GCTRL, NBATCH = 3, 4, 1 << 16

def prog(R):
    if R not in PROG: PROG[R] = Prog(R)
    return PROG[R]

def attack(R, P, NG, VMAX, coins, nbatch=NBATCH, hook=None):
    pg = prog(R); V = 0
    for gi in range(NG):
        r0, r1 = coins(), coins(); base, M0, gb = group_setup(Sc(), pg, R, r0, r1); I = pg.inputs(base, gb, 0)
        for kb in range(nbatch):
            for i in range(16): I['uhi[%d]' % i] = WORD if (kb >> i) & 1 else 0
            fl = pg.f(I); found = []
            if fl != WORD:
                v = Sc(); v.n += VCTRL
                for L in lanes_passing(v, fl):
                    v.n += VLANE; cv = lane_cv(v, R, base, gb, kb, L)
                    li, X, Y, n3b = step3(v, P, cv); found.append((L, cv, li, n3b))
                    if li is not None:
                        res = verify(R, M0 + [(L << 24) | (kb << 8) | gb], X, Y)
                        if res:
                            if hook: hook(M0, gb, kb, fl, found)
                            return dict(pair=res, V=V + v.n, group=gi, batch=kb)
                V += v.n
            if hook: hook(M0, gb, kb, fl, found)
            if V > VMAX: return dict(pair=None, V=V, group=gi, batch=kb, halted=True)
    return dict(pair=None, V=V, group=NG, batch=0)

def calibrate(R, P):
    """Exact counts over three groups: c_G, c_B, categories, registers, c_cv, Step-3 parts, liveness."""
    pg = prog(R); net = pg.b.net; pr = emit(net, pg.fail); res = None
    for seed in (1, 2, 3):
        h = lambda i: int.from_bytes(hashlib.sha256(b'cal%d-%d' % (seed, i)).digest(), 'big')
        sc = Sc(); base, M0, gb = group_setup(sc, pg, R, h(0), h(1)); cG = sc.n
        I = pg.inputs(base, gb, 0); mem = {}
        for x, nd in enumerate(net.nodes):
            if nd[0] == 'in':
                if x in net.hdef: op, p, q = net.hdef[x]; mem[x] = {'xor': mem[p] ^ mem[q], 'and': mem[p] & mem[q], 'or': mem[p] | mem[q]}[op]
                else: mem[x] = I.get(nd[1], 0)
        kb = h(2) & 0xffff
        for i in range(16): I['uhi[%d]' % i] = WORD if (kb >> i) & 1 else 0
        cB, fl, hit, nb = run_vm(pr, mem, kb, pg.fail[1])
        assert fl == pg.f(I) and hit == (fl != WORD) and nb == kb + 1
        cats = dict((k, sum(1 for i in pr if i[0] == k)) for k in ('ld', 'st', 'xor', 'and', 'or'))
        mx = max(max(i[1:]) for i in pr if i[0] in ('xor', 'and', 'or'))
        s2 = Sc(); lane_cv(s2, R, base, gb, kb, 7); ccv = s2.n
        cost = {}; out = step3(Sc(), P, PAIRS[R]['cv'], cost); lv = rare_liveness(R, P)
        assert out[0] is not None and out[1] == PAIRS[R]['mp'] and out[2] == PAIRS[R]['m']
        cur = dict(c_init=9, c_G=cG, groupconsts=len(pg.b.reg), hoisted=len(net.hdef), c_B=cB, cats=cats, maxreg=mx,
                   scanb=SCANB, scanl=SCANL, c_cv=ccv, live_lane=lv[0], live_3b=lv[1], **cost)
        assert res is None or res == cur, (res, cur)
        res = cur
    OPS[R] = res
    return res

NB_EXP, CHK = {37: 1, 38: 6}, 24

def experiment(req):
    R = {'sha256-r37-prefix-v1': 37, 'sha256-r38-prefix-v1': 38}[req['target_profile']]
    P = setup(R); lsfs = [d['w'][:2] for d in P['Lstar']].index(tuple(P['Wx'][14:16])); rows = []; cal = None
    for tr in req['trials']:
        seed = bytes.fromhex(tr['seed']); ctr = [0]
        if cal is None: cal = calibrate(R, P)
        def coins():
            ctr[0] += 1; return int.from_bytes(hashlib.shake_256(seed + bytes([ctr[0]])).digest(32), 'big')
        obs = dict(lanes_checked=0, mismatches=0, w7_pass=0, valid=0, stage3b=0, deepest_row=15, batch_ops=cal['c_B'])
        first = []
        def hook(M0, gb, kb, fl, found):
            fd = dict((f[0], f) for f in found)
            pick = set(hashlib.shake_256(seed + b'chk' + bytes([kb & 255, kb >> 8])).digest(CHK)) | set(fd) | \
                set(L for L in range(256) if not (fl >> L) & 1)
            for L in sorted(pick):
                blk = M0 + [(L << 24) | (kb << 8) | gb]; cv = compress(IV, blk, R); obs['lanes_checked'] += 1
                W = ref_words(P, cv); p7 = inF(W[7], P['d7'], P['t7'])
                qq = (s0(W[1]) + W[0]) & M32
                p3a = any((((qq + d['ck16']) & M32) & P['m16']) == d['v16'] for d in P['Lstar'])
                valid = p7 and (inF(W[6], P['d6'], P['t6']) if R == 37 else p3a)
                bad = valid != (not (fl >> L) & 1) or valid != (L in fd) or (L in fd and fd[L][1] != cv)
                obs['w7_pass'] += p7
                if valid:
                    obs['valid'] += 1; obs['stage3b'] += fd[L][3]
                    Wy = W[:6] + [(W[6] + P['d6']) & M32, (W[7] + P['d7']) & M32]
                    for li, d in enumerate(P['Lstar']):
                        X = W + P['Wx'][8:14] + list(d['w'][:2]); Y = Wy + P['Wy'][8:14] + list(d['w'][2:])
                        bc = cellcheck(R, cv, X, Y)[0]
                        bad |= any(i < 16 and (k, i) not in (('W', 6), ('W', 7)) for k, i in bc)
                        obs['deepest_row'] = max(obs['deepest_row'], min([i for _, i in bc] + [R]) - 1)
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

FIX = {38: {('W', 25, 4, '=', 'W', 25, 9): ('W', 25, 4, '=', 'W', 25, 6)}}
KI = {'A': 0, 'E': 1, 'W': 4}
Q3X = dict(K=20, NP=64, MS={17: 128, 18: 4, 19: 4, 20: 1, 21: 1, 22: 1}, MT=512, POOL_LOG2=-101.40)

def xlist(R):
    out = {}
    for x in CH[R]['X']:
        x = FIX[R].get(x, x)
        if max(x[1], x[5]) >= 16: out.setdefault(max(x[1], x[5]), []).append(x)
    return out

def recipe(P, XL, kind, i):
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

if __name__ == '__main__':
    req = json.loads(sys.stdin.read())
    out = q3_experiment(req) if req['experiment_id'].startswith('d1-q3-smc') else experiment(req)
    sys.stdout.write(json.dumps(out, sort_keys=True, separators=(',', ':')))
