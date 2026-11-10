#!/usr/bin/env python3
# a0core.py - the A0-variant attack on 37-step SHA-256 (sha256-r37-exploratory): exact data, the counted online program,
# and checks.  Standard library only.  The characteristic, its two-bit conditions, the semi-free-start pair and L* are
# those of IACR ePrint 2026/1120 (37 steps) as transcribed and verified in earlier filings; everything else (the variant
# family G, the c7 classes, the filters and the counted program) is defined and checked here.  Version of the filing that
# builds on 087a18c4: 222 classes (W7 test of all classes by one bit-sliced program), W6 programs for up to four batches
# at once, lane scan by 24-bit chunks, good pairs in packed groups of four (64-bit lanes), row-16 presence by blocks.
import hashlib, json, struct, sys
from fractions import Fraction as Fr

M32 = 0xffffffff
K = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
     0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
     0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
     0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
     0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354]
IV = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]
R = 37

def ror(x, n): return ((x >> n) | (x << (32 - n))) & M32
def S0(x): return ror(x, 2) ^ ror(x, 13) ^ ror(x, 22)
def S1(x): return ror(x, 6) ^ ror(x, 11) ^ ror(x, 25)
def s0(x): return ror(x, 7) ^ ror(x, 18) ^ (x >> 3)
def s1(x): return ror(x, 17) ^ ror(x, 19) ^ (x >> 10)
def CH(x, y, z): return (x & y) ^ (~x & z & M32)
def MAJ(x, y, z): return (x & y) ^ (x & z) ^ (y & z)

def expand(w16, n=R):
    W = list(w16)
    for i in range(16, n): W.append((s1(W[i-2]) + W[i-7] + s0(W[i-15]) + W[i-16]) & M32)
    return W

def trace(cv, w16, n=R):
    A = {-1: cv[0], -2: cv[1], -3: cv[2], -4: cv[3]}; E = {-1: cv[4], -2: cv[5], -3: cv[6], -4: cv[7]}
    W = expand(w16, max(n, 16))
    for i in range(n):
        E[i] = (A[i-4] + E[i-4] + S1(E[i-1]) + CH(E[i-1], E[i-2], E[i-3]) + K[i] + W[i]) & M32
        A[i] = (E[i] - A[i-4] + S0(A[i-1]) + MAJ(A[i-1], A[i-2], A[i-3])) & M32
    return A, E, W

def compress(cv, w16):
    A, E, _ = trace(cv, w16)
    return [(c + o) & M32 for c, o in zip(cv, [A[R-1], A[R-2], A[R-3], A[R-4], E[R-1], E[R-2], E[R-3], E[R-4]])]

def digest(msg):
    """The complete sha256-r37 hash (FIPS 180-4 padding, standard IV, 37 steps on every block)."""
    m = msg + b'\x80' + b'\x00' * ((55 - len(msg)) % 64) + struct.pack('>Q', 8 * len(msg))
    h = IV
    for k in range(0, len(m), 64): h = compress(h, list(struct.unpack('>16I', m[k:k+64])))
    return struct.pack('>8I', *h)

# ---- the characteristic (MSB first; member x = the message printed second in the paper) ----
CHA = {6:'=nu=============================',7:'==========n====n====n======n====',10:'======u===========u=============',
    11:'====u=====u=========u=n====u==n=',12:'=nu=============================',13:'====u=========u=u=======n==u====',
    14:'======u=n=======n===============',16:'==u============================='}
CHE = {4:'000=============================',5:'111=0=====1==0=====01===++01====',6:'uuu=1011=00=10111=0111=0++1011==',
    7:'10n=u01001n00n00010nu110unuu0001',8:'011=1n+1=n11u1101=001u1u1010=u=1',9:'1=0110+=001=1100=+110100111u=0=+',
    10:'10n001u110101==01+u1101011=1110+',11:'=01un000011101=n0n0u1uu101011u1u',12:'01101uuuuunu010110110n1u0u0uu0n0',
    13:'0+10n110111unn+0n101110110001001',14:'=+0=1000000111+=1==1n010u0=0101=',15:'=u==01===n=011n01==u0=u=1==+====',
    16:'=0=====+00===11=+==01=0=0==+====',17:'=0=====+01===u1=+==0==1===1u====',18:'==10===uu====0==n===111===01==1=',
    19:'==1====00====1==0==========1====',20:'==u====10=======1===00==========',21:'==0=============================',
    22:'==1============================='}
CHW = {6:'==n=============================',7:'=====u===u==========n===========',8:'==u=============================',
    9:'=====u=u=======n===u==n=u=n=u=n=',10:'============n======u=n==========',14:'=0===u===n=1=1====1=u=1=====1=1=',
    15:'==u=============================',22:'=====0=nn=====1=u=1=============',24:'==n============================='}
X2 = [('A',15,15,'!','A',16,15),('A',15,23,'=','A',16,23),('A',15,25,'=','A',16,25),('A',16,9,'!','A',16,20),
    ('A',16,18,'!','A',16,6),('A',16,8,'=','A',16,17),('A',15,29,'=','A',17,29),('A',17,29,'=','A',18,29),
    ('E',15,4,'=','E',16,4),('E',17,0,'!','E',17,13),('E',16,24,'=','E',17,24),('E',16,15,'=','E',17,15),
    ('E',18,6,'!','E',18,19),('E',18,2,'=','E',18,20),('E',20,2,'!','E',20,16),
    ('W',6,1,'=','W',6,12),('W',6,8,'!','W',6,25),('W',6,14,'=','W',6,18),
    ('W',7,0,'=','W',7,28),('W',7,9,'=','W',7,30),('W',7,1,'=','W',7,18),
    ('W',8,1,'!','W',8,12),('W',8,8,'!','W',8,25),('W',8,14,'=','W',8,18),
    ('W',22,31,'!','W',22,1),('W',22,30,'!','W',22,0),('W',22,16,'!','W',22,25),('W',22,14,'!','W',22,21),
    ('W',24,4,'!','W',24,6),('W',24,22,'=','W',24,31),('W',24,20,'!','W',24,27)]

def cell(s):
    m = v = d = p = 0
    for c, sym in enumerate(s):
        b = 31 - c
        if sym in '01un': m |= 1 << b
        if sym in '1u': v |= 1 << b
        if sym in 'un': d |= 1 << b
        if sym == '+': p |= 1 << b
    return m, v, d, p
EQ = '=' * 32
CELLS = {k: {i: cell(t.get(i, EQ)) for i in range(-4, R)} for k, t in (('A', CHA), ('E', CHE), ('W', CHW))}

def row_ok(x, y, i, checkW=True):
    """Cells of row i for the pair of traces x = (A, E, W), y; '+' pairs with row i-1."""
    for k, X, Y in (('A', x[0], y[0]), ('E', x[1], y[1])):
        m, v, d, p = CELLS[k][i]
        if (X[i] & m) != v or (X[i] ^ Y[i]) != d: return False
        if k == 'E' and i > -4:
            q = p & CELLS['E'][i-1][3]
            if q and ((X[i] ^ X[i-1]) & q): return False
    if checkW and i >= 0:
        m, v, d, _ = CELLS['W'][i]
        if (x[2][i] & m) != v or (x[2][i] ^ y[2][i]) != d: return False
    return True

def x2_ok(x, r):
    D = {'A': x[0], 'E': x[1], 'W': x[2]}
    for (k1, i1, b1, op, k2, i2, b2) in X2:
        if max(i1, i2) != r: continue
        a, c = (D[k1][i1] >> b1) & 1, (D[k2][i2] >> b2) & 1
        if (op == '=') != (a == c): return False
    return True

def h8(s): return [int(t, 16) for t in s.split()]
CV0 = h8('63b4986c 35d83dc0 c98894e4 784e08fc 78a7f752 5ed877a8 315a2db3 d5614eb4')
MY = h8('4d7f86ff 32ece589 d8accfc4 2cc2e433 068b5b34 eba68a28 2fe12cad 6aa26b0c 9f0d78e1 681b8277 faa9c7e0 56aed439 cc2dbbc2 dd2ba0fc b95d377b 5dd43a81')
MX = h8('4d7f86ff 32ece589 d8accfc4 2cc2e433 068b5b34 eba68a28 0fe12cad 6ee2630c bf0d78e1 6d1a90dd faa1d3e0 56aed439 cc2dbbc2 dd2ba0fc bd1d3f7b 7dd43a81')
HASH0 = h8('a856d46e 4b46eb28 4935248c 92a2fc98 e0fb2610 10a9951f 54264f5b 80954580')
W14X = 0xbd1d3f7b
LW15 = h8("""7dd41680 7dd41681 7dd416a0 7dd416a1 7dd41a80 7dd41a81 7dd41aa0 7dd41aa1 7dd43680 7dd43681 7dd436a0 7dd436a1
 7dd43a80 7dd43a81 7dd43aa0 7dd43aa1 fdb41680 fdb41681 fdb416a0 fdb416a1 fdb41a80 fdb41a81 fdb41aa0 fdb41aa1
 fdb43680 fdb43681 fdb436a0 fdb436a1 fdb43a80 fdb43a81 fdb43aa0 fdb43aa1""")
def lstar(l):
    """(x side W14, W15), (y side W14, W15) of element l of L*."""
    return (W14X, LW15[l]), (W14X ^ 0x04400800, LW15[l] ^ 0x20000000)

D6, T6, D7, T7, D8, T8 = 0x20000000, 0x03c00800, 0xfbc00800, 0x017f8000, 0xe0000000, 0x043ff800
def inF(w, d, t): return ((s0((w + d) & M32) - s0(w)) & M32) == t

# ---- S, the variant family G and the c7 classes ----
_tx = trace(CV0, MX); _ty = trace(CV0, MY)
SAx = [_tx[0][i] for i in range(14)]; SAy = [_ty[0][i] for i in range(14)]
SE = _tx[1]                                          # E4..E13 of member x (E4..E5 carry no difference)
C4 = (SAx[4] - S0(SAx[3]) - MAJ(SAx[3], SAx[2], SAx[1])) & M32            # E4 = a0 + C4
W8C = (SE[8] - SAx[4] - S1(SE[7]) - CH(SE[7], SE[6], SE[5]) - K[8]) & M32  # W8x = W8C - E4
C6 = (SE[6] - 2 * SAx[2] + S0(SAx[1]) - S1(SE[5]) - K[6]) & M32           # W6x = C6 - A-2 + MAJ(A1,a0,A-1) - CH(E5,E4,E3)
K3C = (SAx[3] - S0(SAx[2])) & M32                                          # E3 = K3C - MAJ(A2,A1,a0) + A-1
A1, E5 = SAx[1], SE[5]
NE5 = ~E5 & M32

def in_G(a0):
    """E4 = a0 + C4 has E4[31:29] = 000 (row-4 cells) and W8x = W8C - E4 satisfies the W8 cell (bit 29 = 1, so W8y =
    W8x - 2^29 differs only there) and the printed W8 two-bit conditions."""
    e4 = (a0 + C4) & M32
    if e4 >> 29: return False
    w = (W8C - e4) & M32
    b = lambda k: (w >> k) & 1
    return b(29) == 1 and b(1) != b(12) and b(8) != b(25) and b(14) == b(18)

def c7of(a0):
    e4 = (a0 + C4) & M32
    e3k = (K3C - MAJ(SAx[2], SAx[1], a0)) & M32
    return (SE[7] - SAx[3] - e3k - S1(SE[6]) - CH(SE[6], SE[5], e4) - K[7]) & M32

def words_from_cv(cv, a0):
    """Second-block words W0..W13 of both members connecting cv to the state rows of the variant a0 (Lemma 1)."""
    out = []
    for SA in (SAx, SAy):
        A = {-1: cv[0], -2: cv[1], -3: cv[2], -4: cv[3]}; E = {-1: cv[4], -2: cv[5], -3: cv[6], -4: cv[7]}
        for i in range(14): A[i] = SA[i]
        A[0] = a0
        for i in range(14): E[i] = (A[i] + A[i-4] - S0(A[i-1]) - MAJ(A[i-1], A[i-2], A[i-3])) & M32
        out.append([(E[i] - A[i-4] - E[i-4] - S1(E[i-1]) - CH(E[i-1], E[i-2], E[i-3]) - K[i]) & M32 for i in range(14)])
    return out

# the 222 selected classes: (c7, base, mask); class = {base ^ s : s subset of mask, in_G, c7of == c7}; all the classes with
# at least 3456 variants (85 of 3600, 26 of 3584, 111 of 3456), in the order of decreasing size, ties by smaller c7
CLASSES = [tuple(int(v, 16) for v in ln.split()) for ln in """
cc968c4c 1c010142 01fec08d
cc968c5c 1c010112 01fec08d
cc968c6c 1c010122 01fec08d
cc968c7c 1c010132 01fec08d
cc968c8c 1c010102 01fec08d
cc968e1c 1c010352 01fec08d
cc968e2c 1c010362 01fec08d
cc968e3c 1c010372 01fec08d
cc968e4c 1c010342 01fec08d
cc968e5c 1c010312 01fec08d
cc968e6c 1c010322 01fec08d
cc968e7c 1c010332 01fec08d
cc968e8c 1c010302 01fec08d
cc96901c 1c010152 01fec48d
cc96902c 1c010162 01fec48d
cc96903c 1c010172 01fec48d
cc96904c 1c010542 01fec08d
cc96905c 1c010512 01fec08d
cc96906c 1c010522 01fec08d
cc96907c 1c010532 01fec08d
cc96908c 1c010502 01fec08d
ce968d1c 1e010052 01fec08d
ce968d2c 1e010062 01fec08d
ce968d3c 1e010072 01fec08d
ce968d4c 1e010042 01fec08d
ce968d5c 1e010012 01fec08d
ce968d6c 1e010022 01fec08d
ce968d7c 1e010032 01fec08d
ce968d8c 1e010002 01fec08d
ce968f1c 1e010252 01fec08d
ce968f2c 1e010262 01fec08d
ce968f3c 1e010272 01fec08d
ce968f4c 1e010242 01fec08d
ce968f5c 1e010212 01fec08d
ce968f6c 1e010222 01fec08d
ce968f7c 1e010232 01fec08d
ce968f8c 1e010202 01fec08d
ce96911c 1e010452 01fec08d
ce96912c 1e010462 01fec08d
ce96913c 1e010472 01fec08d
ce96914c 1e010442 01fec08d
ce96915c 1e010412 01fec08d
ce96916c 1e010422 01fec08d
ce96917c 1e010432 01fec08d
ce96918c 1e010402 01fec08d
ce96931c 1e010652 01fec08d
ce96932c 1e010662 01fec08d
ce96933c 1e010672 01fec08d
ce96934c 1e010642 01fec08d
ce96935c 1e010612 01fec08d
ce96936c 1e010622 01fec08d
ce96937c 1e010632 01fec08d
ce96938c 1e010602 01fec08d
d2968d1c 1a010052 01fec08d
d2968d2c 1a010062 01fec08d
d2968d3c 1a010072 01fec08d
d2968d4c 1a010042 01fec08d
d2968d5c 1a010012 01fec08d
d2968d6c 1a010022 01fec08d
d2968d7c 1a010032 01fec08d
d2968d8c 1a010002 01fec08d
d2968f1c 1a010252 01fec08d
d2968f2c 1a010262 01fec08d
d2968f3c 1a010272 01fec08d
d2968f4c 1a010242 01fec08d
d2968f5c 1a010212 01fec08d
d2968f6c 1a010222 01fec08d
d2968f7c 1a010232 01fec08d
d2968f8c 1a010202 01fec08d
d296911c 1a010452 01fec08d
d296912c 1a010462 01fec08d
d296913c 1a010472 01fec08d
d296914c 1a010442 01fec08d
d296915c 1a010412 01fec08d
d296916c 1a010422 01fec08d
d296917c 1a010432 01fec08d
d296918c 1a010402 01fec08d
d296931c 1a010652 01fec08d
d296932c 1a010662 01fec08d
d296933c 1a010672 01fec08d
d296934c 1a010642 01fec08d
d296935c 1a010612 01fec08d
d296936c 1a010622 01fec08d
d296937c 1a010632 01fec08d
d296938c 1a010602 01fec08d
cc969228 1c010760 01fec09d
cc969238 1c010760 01fec09d
cc969248 1c010740 01fec09d
cc969258 1c010700 01fec0dd
cc969268 1c010720 01fec09d
cc969278 1c010720 01fec09d
cc969288 1c010700 01fec09d
cc969448 1c010940 01fec09d
cc969458 1c010900 01fec0dd
cc969468 1c010920 01fec09d
cc969478 1c010920 01fec09d
cc969488 1c010900 01fec09d
ce969528 1e010860 01fec09d
ce969538 1e010860 01fec09d
ce969548 1e010840 01fec09d
ce969558 1e010800 01fec0dd
ce969568 1e010820 01fec09d
ce969578 1e010820 01fec09d
ce969588 1e010800 01fec09d
d2969528 1a010860 01fec09d
d2969538 1a010860 01fec09d
d2969548 1a010840 01fec09d
d2969558 1a010800 01fec0dd
d2969568 1a010820 01fec09d
d2969578 1a010820 01fec09d
d2969588 1a010800 01fec09d
cc8e8c4c 1c010142 01fec08d
cc8e8c5c 1c010112 01fec08d
cc8e8c6c 1c010122 01fec08d
cc8e8c7c 1c010132 01fec08d
cc8e8c8c 1c010102 01fec08d
cc8e8e1c 1c010352 01fec08d
cc8e8e2c 1c010362 01fec08d
cc8e8e3c 1c010372 01fec08d
cc8e8e4c 1c010342 01fec08d
cc8e8e5c 1c010312 01fec08d
cc8e8e6c 1c010322 01fec08d
cc8e8e7c 1c010332 01fec08d
cc8e8e8c 1c010302 01fec08d
cc8e901c 1c010152 01fec48d
cc8e902c 1c010162 01fec48d
cc8e903c 1c010172 01fec48d
cc8e904c 1c010542 01fec08d
cc8e905c 1c010512 01fec08d
cc8e906c 1c010522 01fec08d
cc8e907c 1c010532 01fec08d
cc8e908c 1c010502 01fec08d
cc8e9228 1c010760 01fec09d
cc8e9238 1c010760 01fec09d
cc8e9248 1c010740 01fec09d
cc8e9258 1c010700 01fec0dd
cc8e9268 1c010720 01fec09d
cc8e9278 1c010720 01fec09d
cc8e9288 1c010700 01fec09d
cc8e9448 1c010940 01fec09d
cc8e9458 1c010900 01fec0dd
cc8e9468 1c010920 01fec09d
cc8e9478 1c010920 01fec09d
cc8e9488 1c010900 01fec09d
ce8e8d1c 1e010052 01fec08d
ce8e8d2c 1e010062 01fec08d
ce8e8d3c 1e010072 01fec08d
ce8e8d4c 1e010042 01fec08d
ce8e8d5c 1e010012 01fec08d
ce8e8d6c 1e010022 01fec08d
ce8e8d7c 1e010032 01fec08d
ce8e8d8c 1e010002 01fec08d
ce8e8f1c 1e010252 01fec08d
ce8e8f2c 1e010262 01fec08d
ce8e8f3c 1e010272 01fec08d
ce8e8f4c 1e010242 01fec08d
ce8e8f5c 1e010212 01fec08d
ce8e8f6c 1e010222 01fec08d
ce8e8f7c 1e010232 01fec08d
ce8e8f8c 1e010202 01fec08d
ce8e911c 1e010452 01fec08d
ce8e912c 1e010462 01fec08d
ce8e913c 1e010472 01fec08d
ce8e914c 1e010442 01fec08d
ce8e915c 1e010412 01fec08d
ce8e916c 1e010422 01fec08d
ce8e917c 1e010432 01fec08d
ce8e918c 1e010402 01fec08d
ce8e931c 1e010652 01fec08d
ce8e932c 1e010662 01fec08d
ce8e933c 1e010672 01fec08d
ce8e934c 1e010642 01fec08d
ce8e935c 1e010612 01fec08d
ce8e936c 1e010622 01fec08d
ce8e937c 1e010632 01fec08d
ce8e938c 1e010602 01fec08d
ce8e9528 1e010860 01fec09d
ce8e9538 1e010860 01fec09d
ce8e9548 1e010840 01fec09d
ce8e9558 1e010800 01fec0dd
ce8e9568 1e010820 01fec09d
ce8e9578 1e010820 01fec09d
ce8e9588 1e010800 01fec09d
d28e8d1c 1a010052 01fec08d
d28e8d2c 1a010062 01fec08d
d28e8d3c 1a010072 01fec08d
d28e8d4c 1a010042 01fec08d
d28e8d5c 1a010012 01fec08d
d28e8d6c 1a010022 01fec08d
d28e8d7c 1a010032 01fec08d
d28e8d8c 1a010002 01fec08d
d28e8f1c 1a010252 01fec08d
d28e8f2c 1a010262 01fec08d
d28e8f3c 1a010272 01fec08d
d28e8f4c 1a010242 01fec08d
d28e8f5c 1a010212 01fec08d
d28e8f6c 1a010222 01fec08d
d28e8f7c 1a010232 01fec08d
d28e8f8c 1a010202 01fec08d
d28e911c 1a010452 01fec08d
d28e912c 1a010462 01fec08d
d28e913c 1a010472 01fec08d
d28e914c 1a010442 01fec08d
d28e915c 1a010412 01fec08d
d28e916c 1a010422 01fec08d
d28e917c 1a010432 01fec08d
d28e918c 1a010402 01fec08d
d28e931c 1a010652 01fec08d
d28e932c 1a010662 01fec08d
d28e933c 1a010672 01fec08d
d28e934c 1a010642 01fec08d
d28e935c 1a010612 01fec08d
d28e936c 1a010622 01fec08d
d28e937c 1a010632 01fec08d
d28e938c 1a010602 01fec08d
d28e9528 1a010860 01fec09d
d28e9538 1a010860 01fec09d
d28e9548 1a010840 01fec09d
d28e9558 1a010800 01fec0dd
d28e9568 1a010820 01fec09d
d28e9578 1a010820 01fec09d
d28e9588 1a010800 01fec09d
""".strip().splitlines()]
def class_members(c7, base, mask):
    out, s = [], 0
    while True:
        a = base ^ s
        if in_G(a) and c7of(a) == c7: out.append(a)
        s = (s - mask) & mask
        if s == 0: break
    return sorted(out)


class Shake:
    """Deterministic uniform 256-bit words from SHAKE-256 of a seed string (reproducibility only; the attack's coins
    are fresh uniform random words)."""
    def __init__(self, seed): self.seed = seed.encode(); self.k = 0; self.buf = b''; self.pos = 0
    def __call__(self):
        if self.pos + 32 > len(self.buf):
            self.buf = hashlib.shake_256(self.seed + b'|' + str(self.k).encode()).digest(1 << 14); self.k += 1; self.pos = 0
        v = int.from_bytes(self.buf[self.pos:self.pos + 32], 'little'); self.pos += 32; return v
    def below(self, n): return self() % n

# ---- counted machine: every executed primitive of the online program is one call ----
class Mach:
    def __init__(self): self.n = 0
    def ld(self, v): self.n += 1; return v
    def st(self): self.n += 1
    def rnd(self, rng): self.n += 1; return rng()
    def add(self, a, b): self.n += 1; return a + b
    def sub(self, a, b): self.n += 1; return a - b
    def and_(self, a, b): self.n += 1; return a & b
    def or_(self, a, b): self.n += 1; return a | b
    def xor(self, a, b): self.n += 1; return a ^ b
    def shr(self, a, k): self.n += 1; return a >> k
    def shl(self, a, k): self.n += 1; return a << k
    def br(self, c): self.n += 1; return c
    def m(self, a): return self.and_(a, M32)                   # reduce mod 2^32 (one AND)
    def rot3(self, x, r1, r2, r3=None, sh=None):
        """32-bit rotations of a reduced value x: d = x | (x << 32) (2 ops), shifts and XORs, one mask (8 ops)."""
        d = self.or_(x, self.shl(x, 32))
        t = self.xor(self.shr(d, r1), self.shr(d, r2))
        if sh is None: return self.m(self.xor(t, self.shr(d, r3)))
        return self.xor(self.m(t), self.shr(x, sh))
    def S0(self, x): return self.rot3(x, 2, 13, 22)
    def S1(self, x): return self.rot3(x, 6, 11, 25)
    def s0(self, x): return self.rot3(x, 7, 18, sh=3)
    def s1(self, x): return self.rot3(x, 17, 19, sh=10)
    def bit(self, pred, w):
        """Lookup in a 2^32-bit bitmap held in 256-bit words: shr 8, add base, ld, and 255, shr, and 1 (6 ops).
        The bitmap's content is the predicate pred (here emulated by evaluating it)."""
        self.n += 6; return 1 if pred(w) else 0

# ---- per-l data: rows 12..15 of both members (independent of the chaining value and of the variant) ----
def setup_l():
    L = []
    for l in range(32):
        (x14, x15), (y14, y15) = lstar(l)
        tx = trace(CV0, MX[:14] + [x14, x15], 16); ty = trace(CV0, MY[:14] + [y14, y15], 16)
        base = (tx[0][12] + tx[1][12] + S1(tx[1][15]) + CH(tx[1][15], tx[1][14], tx[1][13]) + K[16]) & M32
        L.append(dict(l=l, tx=tx, ty=ty, base=base, C16=(base + s1(x14) + MX[9]) & M32,
                      dW16=(s1(y14) - s1(x14) + MY[9] - MX[9]) & M32, w=((x14, x15), (y14, y15))))
    return L

def new_rows(tx, ty):
    """Mutable copies (A, E, W dicts) of two traces' rows -4..15."""
    return [({**t[0]}, {**t[1]}, {i: t[2][i] for i in range(16)}) for t in (tx, ty)]

def step_rows(X, Y, t):
    for (A, E, W) in (X, Y):
        E[t] = (A[t-4] + E[t-4] + S1(E[t-1]) + CH(E[t-1], E[t-2], E[t-3]) + K[t] + W[t]) & M32
        A[t] = (E[t] - A[t-4] + S0(A[t-1]) + MAJ(A[t-1], A[t-2], A[t-3])) & M32

def row16_ok(Ld, e16):
    X, Y = new_rows(Ld['tx'], Ld['ty'])
    X[2][16] = (e16 - Ld['base']) & M32; Y[2][16] = (X[2][16] + Ld['dW16']) & M32
    step_rows(X, Y, 16)
    return row_ok(X, Y, 16) and x2_ok(X, 16)

_M16, _V16 = CELLS['E'][16][0], CELLS['E'][16][1]
_MA, _VA, _DA = CELLS['A'][16][0], CELLS['A'][16][1], CELLS['A'][16][2]
_Q16 = CELLS['E'][16][3] & CELLS['E'][15][3]
def row16_consts(Ld):
    """Row 16 of both members is linear in E16x = e: E16y - E16x, A16x - e and A16y - e are constants of l; the cells and
    the printed two-bit conditions closing at row 16 are then tests on e + constant (the same decision as row16_ok)."""
    X, Y = new_rows(Ld['tx'], Ld['ty']); X[2][16] = (-Ld['base']) & M32; Y[2][16] = (X[2][16] + Ld['dW16']) & M32
    step_rows(X, Y, 16)
    return (Ld['dW16'] == 0, (Y[1][16] - X[1][16]) & M32, X[0][16], Y[0][16], X[1][15], X[0][15], Ld['C16'])

def row16_fast(c, e):
    z, dE, ax0, ay0, e15, a15, _ = c
    if not z or (e & _M16) != _V16 or ((e ^ e15) & _Q16) or (e ^ ((e + dE) & M32)) != CELLS['E'][16][2]: return False
    ax = (e + ax0) & M32
    if (ax & _MA) != _VA or (ax ^ ((e + ay0) & M32)) != _DA: return False
    b = lambda w, k: (w >> k) & 1
    return (b(a15, 15) != b(ax, 15) and b(a15, 23) == b(ax, 23) and b(a15, 25) == b(ax, 25) and b(ax, 9) != b(ax, 20)
            and b(ax, 18) != b(ax, 6) and b(ax, 8) == b(ax, 17))

def make_R16(Lt):
    """The row-16 table R16[u] = mask of the l in L* whose row 16 holds for E16x = C16_l + u (emulated by the exact
    conditions of row 16, row16_fast; the self-test compares it with the whole-row check row16_ok)."""
    cs = [row16_consts(Ld) for Ld in Lt]
    def R16(u):
        mask = 0
        for l, c in enumerate(cs):
            e = (c[6] + u) & M32
            if (e & _M16) == _V16 and row16_fast(c, e): mask |= 1 << l
        return mask
    R16.blk = {}; R16.cs = cs
    return R16

def blockword(R16, b):
    """Presence word of block b of the row-16 table: bit i is set iff R16[256 b + i] is not zero (a 2^24-word table).
    Emulated per l by the two high parts (e >> 8) the block's e-range can have, then the candidates below bit 8."""
    if b in R16.blk: return R16.blk[b]
    w = 0; mh, vh, ml, vl = _M16 >> 8, _V16 >> 8, _M16 & 255, _V16 & 255
    for c in R16.cs:
        lo = (c[6] + (b << 8)) & M32; r = lo & 255
        for hi, i0, i1 in ((lo >> 8, 0, 256 - r), (((lo >> 8) + 1) & 0xffffff, 256 - r, 256)):
            if (hi & mh) != vh: continue
            for i in range(i0, i1):
                e = ((hi << 8) | ((r + i) & 255)) & M32
                if (e & ml) == vl and row16_fast(c, e): w |= 1 << i
    R16.blk[b] = w
    return w
F6 = lambda w: inF(w, D6, T6)
F7 = lambda w: inF(w, D7, T7)

# ---- the bit-sliced W6 test: one straight-line program per class over 256-bit planes ----
ONE = (1 << 256) - 1
class Prog:
    """SSA program with constant folding; values ('c', 0|1) or ('v', id); ops ld(name), not, and, or, xor."""
    def __init__(self): self.ops = []
    def new(self, op, *a): self.ops.append((op, a)); return ('v', len(self.ops) - 1)
    def ld(self, name): return self.new('ld', name)
    def NOT(self, a): return ('c', 1 - a[1]) if a[0] == 'c' else self.new('not', a)
    def AND(self, a, b):
        if a[0] == 'c': return b if a[1] else a
        if b[0] == 'c': return a if b[1] else b
        return self.new('and', a, b)
    def OR(self, a, b):
        if a[0] == 'c': return a if a[1] else b
        if b[0] == 'c': return b if b[1] else a
        return self.new('or', a, b)
    def XOR(self, a, b):
        if a[0] == 'c': return self.NOT(b) if a[1] else b
        if b[0] == 'c': return self.NOT(a) if b[1] else a
        return self.new('xor', a, b)

def k3of(a0): return (K3C - MAJ(SAx[2], SAx[1], a0)) & M32       # E3 = k3 + A_{-1}
def ne4of(a0): return ~(a0 + C4) & M32                            # ~E4
def const_bits(members, f):
    vals = [f(a) for a in members]
    return [('c', (vals[0] >> j) & 1) if all(((v ^ vals[0]) >> j) & 1 == 0 for v in vals) else None for j in range(32)]

GB = 4                                               # batches per W6 program (the AB/CB loads are shared; peak live values below 64)

def gen_w6(blocks):
    """The bit-major straight-line program for len(blocks) <= GB batches of 256 variants (blocks: their member lists).
    W6x = cb + MAJ(A1, a0, A_{-1}) + ~CH(E5, E4, E3) + 1 with cb = C6 - A_{-2}, E3 = k3 + A_{-1}: MAJ bit j is
    (a0_j | AB_j) if A1_j else (a0_j & AB_j); CH bit j is E4_j if E5_j else E3_j; carry-save add of (MAJ, ~CH, CB)
    then a ripple add with carry-in 1; the exact F6 test is folded into accumulators as soon as both bits of each
    condition exist.  Constant bits of a batch's a0, k3, ~E4 planes are folded per batch.  Returns (program, fail values)."""
    P = Prog(); X, O, N, An = P.XOR, P.OR, P.NOT, P.AND
    cbs = [tuple(const_bits(m, f) for f in (lambda a: a, k3of, ne4of)) for m in blocks]
    sh = {}
    def sld(name):
        if name not in sh: sh[name] = P.ld(name)
        return sh[name]
    St = [dict(c_e3=('c', 0), c_csa=('c', 1), k_rip=('c', 0), w={}, com=('c', 0), bc=('c', 0), u={}) for _ in blocks]
    outs = [None] * len(blocks)
    for j in range(32):
        ab, z = sld('AB%d' % j), sld('CB%d' % j)
        for bi, S in enumerate(St):
            a0c, k3c, e4c = cbs[bi]
            inp = lambda kind, c: c[j] if c[j] is not None else P.ld('%s%d@%d' % (kind, j, bi))
            a0j = inp('A0', a0c)
            maj = O(a0j, ab) if (A1 >> j) & 1 else An(a0j, ab)
            c_e3 = S['c_e3']
            if (E5 >> j) & 1:
                y = inp('NE4', e4c)
                if j < 28: k3 = inp('K3', k3c); t = X(k3, ab); S['c_e3'] = O(An(k3, ab), An(c_e3, t))
            else:
                k3 = inp('K3', k3c); t = X(k3, ab); y = N(X(t, c_e3))
                if j < 28: S['c_e3'] = O(An(k3, ab), An(c_e3, t))
            xy = X(maj, y); s = X(xy, z)
            t2 = X(s, S['c_csa']); w = S['w']; w[j] = X(t2, S['k_rip'])
            if j < 31: S['k_rip'] = O(An(s, S['c_csa']), An(S['k_rip'], t2)); S['c_csa'] = O(An(maj, y), An(z, xy))
            if j == 12: S['com'] = O(S['com'], X(w[1], w[12]))
            elif j == 13: S['bc'] = O(S['bc'], X(w[2], w[13]))
            elif j == 14: S['u'][3] = X(w[3], w[14])
            elif j == 18: S['com'] = O(S['com'], X(w[14], w[18]))
            elif j == 19: S['bc'] = O(S['bc'], X(w[15], w[19]))
            elif j == 20: S['u'][16] = X(w[16], w[20])
            elif j == 25: S['com'] = O(S['com'], N(X(w[8], w[25])))
            elif j == 26: S['bc'] = O(S['bc'], N(X(w[9], w[26])))
            elif j == 27: S['u'][10] = X(w[10], w[27])
            elif j == 31:
                u, bc = S['u'], S['bc']; b_bad = O(bc, w[30])
                c_bad = O(O(O(O(bc, N(w[30])), X(u[16], w[31])), N(X(u[10], w[31]))), X(u[3], w[31]))
                outs[bi] = O(S['com'], An(An(w[29], b_bad), c_bad))
    return P, outs

def peak_live(P, outs):
    last = {}
    for i, (op, a) in enumerate(P.ops):
        for x in a:
            if isinstance(x, tuple) and x[0] == 'v': last[x[1]] = i
    for o in outs: last[o[1]] = len(P.ops)
    ends = {}
    for k, v in last.items(): ends.setdefault(v, []).append(k)
    live = peak = 0
    for i in range(len(P.ops)):
        live += 1 if i in last else 0
        peak = max(peak, live)
        live -= len(ends.get(i, []))
    return peak

def run_w6(P, outs, data, bc):
    """Evaluate the program: data[bi] holds batch bi's stored planes, bc the broadcast planes; returns the fail planes."""
    val = []
    g = lambda a: (ONE if a[1] else 0) if a[0] == 'c' else val[a[1]]
    for op, a in P.ops:
        if op == 'ld':
            if a[0][:2] in ('AB', 'CB'): val.append(bc[a[0]])
            else: nm, bi = a[0].split('@'); val.append(data[int(bi)][nm])
        elif op == 'not': val.append(g(a[0]) ^ ONE)
        elif op == 'and': val.append(g(a[0]) & g(a[1]))
        elif op == 'or': val.append(g(a[0]) | g(a[1]))
        else: val.append(g(a[0]) ^ g(a[1]))
    return [g(o) for o in outs]

def batch_planes(members, b, names=None):
    """Stored planes of batch b of a class (lane L = member 256 b + L; unused lanes repeat member 0); only the
    planes the class program loads (names) are built."""
    lanes = [members[256 * b + L] if 256 * b + L < len(members) else members[0] for L in range(256)]
    d = {}
    for name, f in (('A0', lambda a: a), ('K3', k3of), ('NE4', ne4of)):
        vs = None
        for j in range(32):
            key = '%s%d' % (name, j)
            if names is not None and key not in names: continue
            if vs is None: vs = [f(a) for a in lanes]
            d[key] = int(''.join('1' if (v >> j) & 1 else '0' for v in reversed(vs)), 2)
    return d

# ---- the counted online program ----
VC = 1                                                   # one ADD into the global work counter V

def first_block(mc, rng):
    """Two uniform 256-bit words; W0..W15 of M0 are their eight 32-bit fields each (30 operations).
    CV1 = F_37(IV, M0) is one target compression, charged one unit (not counted here)."""
    r = [mc.rnd(rng), mc.rnd(rng)]; w = []
    for k in range(16):
        x = r[k // 8]
        if k % 8: x = mc.shr(x, 32 * (k % 8))
        w.append(mc.m(x) if k % 8 != 7 else x)
    return w

def gen_w7():
    """The bit-sliced W7 test of all classes at once (lane = class): W7x = c7 + ~A_{-1} + 1 by a ripple adder over the class
    planes C7_j (stored) and the broadcast planes NA_j (bit j of ~A_{-1}, formed in 3 operations each by the driver), then the
    exact F7 test of Section 5.1 (two affine spaces: parity checks of the sum bits); returns (program, pass plane)."""
    P = Prog(); X, O, N, An = P.XOR, P.OR, P.NOT, P.AND
    w, c = {}, ('c', 1)
    for j in range(32):
        c7, na = P.ld('C7%d' % j), P.ld('NA%d' % j); t = X(c7, na); w[j] = X(t, c)
        if j < 31: c = O(An(c7, na), An(c, t))
    eq = lambda x, v: x if v else N(x)
    t1, t2, t3 = X(X(w[1], w[18]), w[22]), X(X(w[9], w[26]), w[30]), X(X(w[0], w[11]), w[28])
    p0 = [eq(w[11], 0), eq(w[22], 1), eq(w[26], 1), eq(t1, 1), eq(t2, 1), eq(t3, 0)]
    p1 = [eq(w[11], 1), eq(w[12], 0), eq(w[22], 0), eq(w[23], 1), eq(w[26], 0), eq(w[27], 1), eq(t1, 0),
          eq(X(X(w[2], w[19]), w[23]), 1), eq(t2, 0), eq(X(X(w[10], w[27]), w[31]), 1), eq(t3, 1), eq(X(X(w[1], w[12]), w[29]), 0)]
    def conj(ps):
        r = ps[0]
        for p in ps[1:]: r = An(r, p)
        return r
    return P, O(conj(p0), conj(p1))

_W7 = []
def w7_scan(mc, a):
    """The W7 test of every selected class: 32 broadcast planes NA_j = (bit j of a) - 1 (shr, and, sub: 3 each), the
    bit-sliced program above (its loads of the stored class planes counted; no load of NA), the AND with the mask of the
    classes' lanes and the scan of the pass plane.  Returns the indices of the classes whose variants pass the W7 test."""
    if not _W7:
        P, out = gen_w7(); pl = {}
        for j in range(32): pl['C7%d' % j] = sum(((c[0] >> j) & 1) << i for i, c in enumerate(CLASSES))
        _W7.extend([P, out, pl])
    P, out, pl = _W7
    val = []; g = lambda x: (ONE if x[1] else 0) if x[0] == 'c' else val[x[1]]
    for op, x in P.ops:
        if op == 'ld': val.append(pl[x[0]] if x[0][0] == 'C' else (0 if (a >> int(x[0][2:])) & 1 else ONE))
        elif op == 'not': val.append(g(x[0]) ^ ONE)
        elif op == 'and': val.append(g(x[0]) & g(x[1]))
        elif op == 'or': val.append(g(x[0]) | g(x[1]))
        else: val.append(g(x[0]) ^ g(x[1]))
    mc.n += 3 * 32 + len(P.ops) - 32 + 1                 # NA planes, program (the 32 NA are not loads), lane mask
    return scan_lanes(mc, g(out) & ((1 << len(CLASSES)) - 1))

def broadcast(mc, a, b):
    """Per first block with a hit: the 64 broadcast planes AB_j (bit j of A_{-1}) and CB_j (bit j of C6 - A_{-2}),
    each 0 - ((x >> j) & 1) and stored (4 operations), after cb = (C6 - b) & M (2): 258 operations."""
    cb = mc.m(mc.sub(C6, b)); d = {}
    for name, x in (('AB', a), ('CB', cb)):
        for j in range(32):
            v = mc.sub(0, mc.and_(mc.shr(x, j), 1)); mc.st()
            d['%s%d' % (name, j)] = ONE if v else 0
    return d

CHK, NCH = 24, 11                                       # lane-scan chunk (bits) and chunks per plane (ten of 24 bits, one of 16)
SCAN_FIXED = 1 + 1 + 2 * (NCH - 2) + NCH + 2 * NCH      # per batch: extraction (20), zero branches (11), entry loads (22): 53
SCAN_LANE = 4                                           # per set lane: and 31, add base, shr 6, loop branch

def scan_lanes(mc, plane):
    """Indices of the set bits of a 256-bit plane by 24-bit chunks: extract (shr, and; one op for the first and the last
    chunk), a zero branch, and for a nonzero chunk add base + ld of its entry in a 2^24-entry table whose entry lists the
    chunk's set positions as 6-bit fields (position | 32), lowest first.  Per set lane: and 31, add base, shr 6 and a
    loop branch (4).  The ledger charges every chunk as nonzero."""
    out = []
    for c in range(NCH):
        x = (plane >> (CHK * c)) & ((1 << CHK) - 1); mc.n += 1 if c in (0, NCH - 1) else 2
        if mc.br(x != 0):
            mc.n += 2
            for i in range(CHK):
                if (x >> i) & 1: mc.n += SCAN_LANE; out.append(CHK * c + i)
    return out

PM = sum(M32 << (64 * k) for k in range(4))

def cv_pre(mc, cv):
    """Per first block, at its first good pair: the constants of W0 = a0 + kap0 and W1 (35 operations), reduced
    (kap0, 1) or made positive (kap1 + 2^35, 1), each broadcast to the four 64-bit lanes (x | x << 64, then | << 128: 4)
    and the lane mask (1): 66."""
    Am1, Am2, Am3, Am4, Em1, Em2, Em3, Em4 = cv
    mj = mc.or_(mc.and_(Am1, Am2), mc.and_(Am3, mc.or_(Am1, Am2)))
    e0b = mc.m(mc.sub(mc.sub(Am4, mc.S0(Am1)), mj))
    ch = mc.xor(mc.and_(Em1, mc.xor(Em2, Em3)), Em3)
    kap0 = mc.m(mc.sub(mc.sub(mc.sub(mc.sub(mc.sub(e0b, Am4), Em4), mc.S1(Em1)), ch), K[0]))
    pre = dict(e0b=e0b, kap0=kap0, o12=mc.or_(Am1, Am2), n12=mc.and_(Am1, Am2), X=mc.xor(Em1, Em2), Em2=Em2,
               kap1=mc.add(mc.sub((A1 - K[1]) & M32, Em3), 1 << 35))
    for k in list(pre):
        t = mc.or_(pre[k], mc.shl(pre[k], 64)); pre[k] = mc.or_(t, mc.shl(t, 128))
    pre['pm'] = mc.ld(PM)
    return pre

def rot3p(mc, x, pm, r1, r2, r3=None, sh=None):
    """rot3 on four 32-bit values in the low halves of the 64-bit lanes of x: d = x | x << 32 stays in each lane; the
    shifts bring in other lanes' bits above bit 31 only, removed by the final masks (8 operations; 9 with a plain shift)."""
    d = mc.or_(x, mc.shl(x, 32)); t = mc.xor(mc.shr(d, r1), mc.shr(d, r2))
    if sh is None: return mc.and_(mc.xor(t, mc.shr(d, r3)), pm)
    return mc.xor(mc.and_(t, pm), mc.and_(mc.shr(x, sh), pm))

def good_group(mc, acc, pre):
    """u = W0 + s0(W1) of up to four good pairs at once; acc holds a0 | S0(a0) << 32 in the low 64 bits of lane k.
    Every value of a lane stays below 2^64 (kap1 + 2^35 - (sum of four 32-bit words) > 0), so no lane borrows or carries
    into its neighbour.  34 operations."""
    pm = pre['pm']
    a = mc.and_(acc, pm); sa = mc.and_(mc.shr(acc, 32), pm)
    E0 = mc.and_(mc.add(a, pre['e0b']), pm); W0 = mc.add(a, pre['kap0'])
    mj = mc.or_(mc.and_(a, pre['o12']), pre['n12'])
    ch = mc.xor(mc.and_(E0, pre['X']), pre['Em2'])
    T = mc.add(mc.add(mc.add(sa, mj), rot3p(mc, E0, pm, 6, 11, 25)), ch)
    W1 = mc.and_(mc.sub(pre['kap1'], T), pm)
    return mc.and_(mc.add(W0, rot3p(mc, W1, pm, 7, 18, sh=3)), pm)

def step3b(mc, cv, a0, w6, w7, mask, Lt):
    """For each l in the row-16 mask: both members' words and rows 17..36 with early abort (counted).  Returns
    (l, M1, M1') of the first l whose rows 16..36 follow every cell and two-bit condition, else None."""
    Am1, Am2, Am3, Am4, Em1, Em2, Em3, Em4 = cv
    A = {-1: Am1, -2: Am2, -3: Am3, -4: Am4, 0: a0, 1: SAx[1], 2: SAx[2], 3: SAx[3], 4: SAx[4], 5: SAx[5]}
    E = {-1: Em1, -2: Em2, -3: Em3, -4: Em4}
    for i in range(6):
        mj = mc.or_(mc.and_(A[i-1], A[i-2]), mc.and_(A[i-3], mc.or_(A[i-1], A[i-2])))
        E[i] = mc.m(mc.sub(mc.sub(mc.add(A[i], A[i-4]), mc.S0(A[i-1])), mj))
    W = {}
    for i in range(6):
        ch = mc.xor(mc.and_(E[i-1], mc.xor(E[i-2], E[i-3])), E[i-3])
        W[i] = mc.m(mc.sub(mc.sub(mc.sub(mc.sub(mc.sub(E[i], A[i-4]), E[i-4]), mc.S1(E[i-1])), ch), K[i]))
    w8 = mc.m(mc.sub(W8C, mc.add(a0, C4)))
    for l in range(32):
        if not (mask >> l) & 1: continue
        mc.n += 2
        Ld = Lt[l]; (x14, x15), (y14, y15) = Ld['w']
        Wx = [W[0], W[1], W[2], W[3], W[4], W[5], w6, w7, w8] + MX[9:14] + [x14, x15]
        Wy = [W[0], W[1], W[2], W[3], W[4], W[5], (w6 + D6) & M32, (w7 + D7) & M32, (w8 + D8) & M32] + MY[9:14] + [y14, y15]
        mc.n += 6                                        # the three y-words with a difference: add, and each
        X, Y = new_rows(Ld['tx'], Ld['ty'])
        for i in range(16): X[2][i] = Wx[i]; Y[2][i] = Wy[i]
        ok = True
        for t in range(16, R):            # row 16 recomputed (its values are needed), then rows 17..36
            for (Aa, Ee, Ww) in (X, Y):
                Ww[t] = mc.m(mc.add(mc.add(mc.add(mc.s1(Ww[t-2]), Ww[t-7]), mc.s0(Ww[t-15])), Ww[t-16]))
                ch = mc.xor(mc.and_(Ee[t-1], mc.xor(Ee[t-2], Ee[t-3])), Ee[t-3])
                Ee[t] = mc.m(mc.add(mc.add(mc.add(mc.add(mc.add(Aa[t-4], Ee[t-4]), mc.S1(Ee[t-1])), ch), K[t]), Ww[t]))
                mj = mc.or_(mc.and_(Aa[t-1], Aa[t-2]), mc.and_(Aa[t-3], mc.or_(Aa[t-1], Aa[t-2])))
                Aa[t] = mc.m(mc.add(mc.sub(Ee[t], Aa[t-4]), mc.add(mc.S0(Aa[t-1]), mj)))
            mc.n += ROWCHECK
            if not mc.br(row_ok(X, Y, t) and x2_ok(X, t)): ok = False; break
        if ok: return l, Wx[:16], Wy[:16]
    return None
# cells of a row (A, E, W of both members: and, xor, xor, xor, or per word = 15; the '+' pair: xor, and, or = 3) and
# the two-bit conditions closing at the row (at most 7, each shr, shr, xor, and, or = 5), charged uniformly at the
# maximum 15 + 3 + 35 = 53 (the branch is counted separately).
ROWCHECK = 53
ROWCOMP = 106                                            # one row of both members: W (20), CH (3), E (14), MAJ (4), A (12) each

# ---- the selected classes, their variant data and their W6 programs ----
class ClassData:
    def __init__(self, c):
        self.c7, base, mask = CLASSES[c]
        self.members = class_members(self.c7, base, mask)
        n = len(self.members); self.nb = (n + 255) // 256
        lanes = lambda b: [self.members[256 * b + L] if 256 * b + L < n else self.members[0] for L in range(256)]
        self.groups = []                                # (batches, program, fail values, plane names per batch)
        for b0 in range(0, self.nb, GB):
            bs = list(range(b0, min(b0 + GB, self.nb)))
            P, outs = gen_w6([lanes(b) for b in bs]); names = [set() for _ in bs]
            for op, a in P.ops:
                if op == 'ld' and a[0][:2] not in ('AB', 'CB'): nm, bi = a[0].split('@'); names[int(bi)].add(nm)
            self.groups.append((bs, P, outs, names))
        self._planes = {}
    def planes(self, b, names):
        if b not in self._planes: self._planes[b] = batch_planes(self.members, b, names)
        return self._planes[b]

def entry(a0, k): return (a0 | (S0(a0) << 32)) << (64 * k)   # variant table k: a0 | S0(a0) << 32 placed in lane k

def process_class(mc, cd, bc, cv, state, R16, Lt, check=None):
    """One W7-passing class: the counted bit-sliced W6 program on each batch, the lane scan, and every good pair, which
    are processed in groups of four (a group is closed at the end of the class: the pairs of the class are packed into a
    word one lane each (ld of the variant's table entry for lane k, or into the word), u of the four by good_group, then
    per pair: lane extraction (shr, and), the row-16 presence lookup (6) and a branch)."""
    a, b = cv[0], cv[1]
    found = None; grp = []
    def flush():
        nonlocal found
        if state.get('pre') is None: state['pre'] = cv_pre(mc, cv); mc.n += VC
        acc = 0
        for k, a0 in enumerate(grp):
            e = mc.ld(entry(a0, k)); acc = mc.or_(acc, e) if k else e
        u4 = good_group(mc, acc, state['pre']); mc.n += VC            # one V update per group (immediate: the group's cost)
        for k, a0 in enumerate(grp):
            x = mc.and_(mc.shr(u4, 64 * k + 8), (1 << 24) - 1); mc.n += 1       # u >> 8 (24 bits), add base
            wd = mc.ld(blockword(R16, x))                                        # the presence word of u's block of 256
            u = (u4 >> (64 * k)) & M32                                           # (uncounted: the check below and the rare path)
            if check is not None: check('u', cv, a0, cd, u=u)
            state['good'] += 1
            if not mc.br(wd != 0): continue                                      # 6.3% of the pairs at most
            idx = mc.and_(mc.shr(u4, 64 * k) if k else u4, 255)                  # u & 255 (2 operations, 1 for lane 0)
            if not mc.br(mc.and_(mc.shr(wd, idx), 1)): continue
            mc.n += 7 + 2; mask = R16(u)            # the pair's mask word of R16; a0 extracted from the packed word (shr, and)
            state['r16'] += 1; mc.n += VC
            w6, w7 = recompute_w67(mc, a0, a, b, cd.c7)
            f = step3b(mc, cv, a0, w6, w7, mask, Lt)
            if f and found is None: found = (a0, f)
        grp.clear()
    for bs, P, outs, names in cd.groups:
        fails = run_w6(P, outs, [cd.planes(b, nm) for b, nm in zip(bs, names)], bc); mc.n += len(P.ops)
        for bt, fail in zip(bs, fails):
            nl = min(256, len(cd.members) - 256 * bt)
            lanes_mask = (1 << nl) - 1
            passp = (fail ^ ONE) & lanes_mask; mc.n += 2                 # NOT, AND with the batch's lane mask
            for L in scan_lanes(mc, passp):
                a0 = cd.members[256 * bt + L]; mc.n += 1                  # index add (the table load is in flush)
                if check is not None: check('good', cv, a0, cd)
                grp.append(a0)
                if len(grp) == 4: flush()
            if check is not None:
                check('plane', cv, None, cd, bt=bt, fail=fail, nl=nl)
    if grp: flush()
    mc.n += 2                                                        # compare V with V_MAX, branch
    return found

def recompute_w67(mc, a0, a, b, c7):
    """W6x and W7x of one good pair (rare path, counted: 23 operations)."""
    maj1 = mc.or_(mc.and_(A1, a0), mc.and_(a, mc.or_(A1, a0)))
    e4 = mc.m(mc.add(a0, C4))
    mj2 = mc.or_(mc.and_(SAx[2], SAx[1]), mc.and_(a0, mc.or_(SAx[2], SAx[1])))
    e3 = mc.m(mc.add(mc.sub(K3C, mj2), a))
    ch = mc.xor(mc.and_(E5, mc.xor(e4, e3)), e3)
    w6 = mc.m(mc.sub(mc.add(mc.sub(C6, b), maj1), ch))
    w7 = mc.m(mc.sub(mc.ld(c7), a))
    return w6, w7

CTRL_FB, CTRL_HIT = 16, 8
# control allowances, charged in the ledger and counted by the program: per first block the loop counter (add,
# compare-branch), the hit-list initialisation and the `if hits` branch (4 counted) plus 12 for any further address or
# loop arithmetic; per passing class appending it to the hit list (store, add) and iterating (load, add, branch)
# (5 counted) plus 3.

def online(nfb, rng, CD, Lt, R16, stats, check=None, max_classes=None):
    """The online phase on nfb first blocks drawn from rng (max_classes limits the classes processed per first block,
    for bounded experiment runs only).  Returns (operation count, found pairs)."""
    mc = Mach(); found = []
    for f in range(nfb):
        mc.n += CTRL_FB
        w = first_block(mc, rng); cv = compress(IV, w); stats['fb'] += 1; stats['m0'] = w
        hits = w7_scan(mc, cv[0]); mc.n += CTRL_HIT * len(hits)
        if not hits: continue
        mc.n += VC
        bc = broadcast(mc, cv[0], cv[1]); state = dict(pre=None, good=0, r16=0)
        stats['hits_found'] = stats.get('hits_found', 0) + len(hits)
        for c in (hits if max_classes is None else hits[:max_classes]):
            stats['hits'] += 1; mc.n += VC
            if c not in CD: CD[c] = ClassData(c)
            r = process_class(mc, CD[c], bc, cv, state, R16, Lt, check)
            if r: found.append((w, r))
        stats['good'] += state['good']; stats['r16'] += state['r16']
    return mc.n, found

# ---- calibration: every count of the ledger, produced by running the counted routines ----
def w7_fixed(mc, a):
    """Operations of w7_scan except the 4 per passing class of its scan; also checks the pass plane against the scalar test."""
    hits = w7_scan(mc, a)
    assert hits == [c for c in range(len(CLASSES)) if F7((CLASSES[c][0] - a) & M32)]
    mc.n += 2 * (NCH - len({h // CHK for h in hits})) - SCAN_LANE * len(hits)    # every chunk charged as nonzero, the lanes excluded

def calibrate(full=False):
    import random
    rr = random.Random(20261009)
    Lt = setup_l(); R16 = make_R16(Lt)
    cal = {}
    def cnt(f, *a):
        mc = Mach(); r = f(mc, *a); return mc.n, r
    seen = {}
    for trial in range(20):
        rng = Shake('calibrate-%d' % trial); cv = [rr.getrandbits(32) for _ in range(8)]
        for name, f, a in (('fb', first_block, (rng,)), ('w7scan', w7_fixed, (cv[0],)), ('broadcast', broadcast, (cv[0], cv[1])),
                           ('pre', cv_pre, (cv,))):
            n, r = cnt(f, *a); seen.setdefault(name, set()).add(n)
        mc = Mach(); pre = cv_pre(mc, cv); mem = class_members(*CLASSES[trial])
        for ng in (4, 3):                              # a full group and a padded one: the count is the same; every lane equals the scalar u
            a0s = [mem[rr.randrange(len(mem))] for _ in range(ng)]; acc = 0
            for k, a0 in enumerate(a0s): acc |= entry(a0, k)
            mc2 = Mach(); u4 = good_group(mc2, acc, pre); seen.setdefault('gp', set()).add(mc2.n)
            for k, a0 in enumerate(a0s):
                w = words_from_cv(cv, a0)[0]; assert (u4 >> (64 * k)) & M32 == (w[0] + s0(w[1])) & M32 and (u4 >> (64 * k + 32)) & M32 == 0
        pl = rr.getrandbits(256) & rr.getrandbits(256) & rr.getrandbits(256)
        mc3 = Mach(); idx = scan_lanes(mc3, pl); assert idx == [i for i in range(256) if (pl >> i) & 1]
        nz = sum(1 for c in range(NCH) if (pl >> (CHK * c)) & ((1 << CHK) - 1))
        assert mc3.n == 20 + NCH + 2 * nz + SCAN_LANE * len(idx) and SCAN_FIXED == 20 + NCH + 2 * NCH
    for k, v in seen.items():
        assert len(v) == 1, (k, v); cal[k] = v.pop()
    # the emulated row-16 table (row16_fast, blockword) equals the whole-row check row16_ok on 300 positive and random words
    slow = lambda u: sum(1 << Ld['l'] for Ld in Lt if (((Ld['C16'] + u) & M32) & _M16) == _V16 and row16_ok(Ld, (Ld['C16'] + u) & M32))
    n = 0
    while n < 300:
        Ld = Lt[rr.randrange(32)]; e = (rr.getrandbits(32) & ~_M16 | _V16) & M32
        if not row16_ok(Ld, e): continue
        u = (e - Ld['C16']) & M32; n += 1
        assert R16(u) == slow(u) and (blockword(R16, u >> 8) >> (u & 255)) & 1
        if n % 25 == 0: assert blockword(R16, u >> 8) == sum(1 << i for i in range(256) if slow(((u >> 8) << 8) | i))
    for _ in range(300): u = rr.getrandbits(32); assert R16(u) == slow(u)
    # step 3b on the published pair (variant a0 = published A0, l = 13): every row passes, so the count is the full path
    mc = Mach(); f = step3b(mc, CV0, SAx[0], MX[6], MX[7], 1 << 13, Lt)
    assert f is not None and f[0] == 13 and f[1] == MX and f[2] == MY
    cal['step3b_full'] = mc.n
    assert mc.n == 201 + 2 + 6 + 21 * (ROWCOMP + ROWCHECK + 1), mc.n
    mc = Mach(); recompute_w67(mc, SAx[0], CV0[0], CV0[1], c7of(SAx[0])); cal['recompute'] = mc.n
    progs = []
    for c in range(len(CLASSES)):
        if not (full or c < 2): progs.append(None); continue
        cx = ClassData(c); gs = [(P, o) for _, P, o, _ in cx.groups]
        progs.append((sum(len(P.ops) for P, o in gs), sum(1 for P, o in gs for op in P.ops if op[0] == 'ld'),
                      max(peak_live(P, o) for P, o in gs), len(cx.members)))
    cal['w6prog'] = progs
    return cal

# ---- the ledger (exact rationals) ----
from decimal import Decimal as Dec, getcontext
getcontext().prec = 60
H3D, EPS = Dec(2) ** Dec('-10.4'), Fr(1, 256)

def xreq(e):
    """H7: the smallest 8-decimal number strictly above -ln(0.61 - 2^-e - 2^-60) / (1 - 2^-10.4), with e the exponent of
    the Chebyshev cap-failure allowance (Section 10); with E[X] >= xreq the success bound is above 0.39."""
    mu = -(Dec('0.61') - Dec(2) ** (-Dec(Fr(e).numerator) / Dec(Fr(e).denominator)) - Dec(2) ** -60).ln() / (1 - H3D)
    return Fr(int(mu * 10 ** 8) + 1, 10 ** 8)

def ledger(cal, q3_log2=-74.0252, show=True, A_C=2 ** 60, scalar_w6=False, scalar_u=False, mu=None):
    from fractions import Fraction as Fr
    import math
    C = 2644
    p7, p6 = Fr(68157440, 1 << 32), Fr(287309824, 1 << 32)
    r16 = Fr(1052672, 1 << 32)                         # sum over l of |R16_l| / 2^32 (exact enumeration, smc.c / C tools)
    progs = cal['w6prog']; assert all(p is not None for p in progs)
    k = len(CLASSES); ns = [p[3] for p in progs]; nbs = [(n + 255) // 256 for n in ns]
    g = sum(ns) * p7 * p6                               # expected good pairs per first block (exact under H1)
    w6_per_class = [p[0] + 2 * nb for nb, p in zip(nbs, progs)]     # the programs, and NOT and lane AND per batch
    if scalar_w6: w6_per_class = [4 + n * 18 for n in ns]           # sensitivity: scalar W6 test (setup 4, 18 per variant)
    scan_fixed = [nb * SCAN_FIXED for nb in nbs]        # per batch: every chunk charged as nonzero
    pnz = 256 * r16                                     # Pr[u's block of 256 holds an element of U] <= |sum_l R16_l| / 2^24
    per_good = SCAN_LANE + 1 + 1 + 1 + 5 + 5 * pnz      # scan, index add, ld, or, block lookup (shr, and, add, ld, br), bit test (5)
    gp = (4 * 30 if scalar_u else cal['gp']) + VC       # one packed group of four and its V update (sensitivity: four scalar u of 30 operations)
    group_class = [Fr(gp) * (n * p6 + 3) / 4 for n in ns]   # ceil(n/4) <= (n + 3)/4 groups per class, E[n] = n p6
    c3b_pair = 201 + 23 + VC + 7 + 2                    # per row-16 pair: W0..W5 and W8 (201), W6/W7 (23), V update, mask word, a0
    c3b_l = 2 + 6 + 2 * (ROWCOMP + ROWCHECK + 1)        # per (pair, l) in the mask: rows 16 and 17 (always executed)
    rows_extra = 19 * Fr(1, 512)                        # rows 18..36 executed with probability <= 2^-9 each
    c3b_row = ROWCOMP + ROWCHECK + 1
    fixed = cal['fb'] + cal['w7scan'] + CTRL_FB         # every first block (plus one target compression)
    vbar = min(Fr(1), k * p7) * (VC + cal['broadcast'] + cal['pre'] + VC) \
         + p7 * sum(CTRL_HIT + SCAN_LANE + VC + w + sf + 2 + gc for w, sf, gc in zip(w6_per_class, scan_fixed, group_class)) \
         + g * per_good + g * r16 * (c3b_pair + c3b_l + rows_extra * c3b_row)
    q3_log2 = Fr(q3_log2).limit_denominator(10 ** 6) if isinstance(q3_log2, float) else Fr(q3_log2)
    fl = math.floor(q3_log2)
    q3ex = Fr(2) ** fl * Fr(math.floor(2 ** (float(q3_log2) - fl) * 2 ** 40), 2 ** 40)   # exact rational <= 2^q3_log2
    vmax_c = [p[0] + nb * (2 + SCAN_FIXED) + 2 + VC + n * (SCAN_LANE + 1 + 1 + 1 + 5 + 5) + gp * ((n + 3) // 4)
              + n * (c3b_pair + 32 * (c3b_l + 19 * c3b_row)) for nb, p, n in zip(nbs, progs, ns)]
    vmax_class = max(vmax_c); vmax_fb = sum(vmax_c) + k * (CTRL_HIT + SCAN_LANE) + 2 * VC + cal['broadcast'] + cal['pre']   # one class's / one first block's maximum work
    e = Fr(21)
    for _ in range(4):                                  # Chebyshev allowance 2^-e and mu0 = xreq(e) depend on each other
        mu_target = xreq(e) if mu is None else Fr(mu); nfb = int(-(-mu_target // (g * 32 * q3ex)))
        cheb = Fr(vmax_fb * 2 ** 16) / (nfb * vbar)     # E[v^2] <= vmax_fb vbar, deviation 2^-8 N vbar
        e = Fr(math.floor(-math.log2(cheb) * 10), 10)
    assert nfb * g * 32 * q3ex >= mu_target
    VMAX = math.ceil((1 + EPS) * nfb * vbar)
    A_S, DEV = 2 ** 50, 2 ** 40
    pre_ops = 2 ** 40                                   # all precomputation, bounded (Section 11.1)
    fin_units, fin_ops = 6, 600 + 1000                  # final verification; the next first block's setup after the last cap test
    T = Fr(A_C + A_S + DEV) + nfb + Fr(nfb * fixed + VMAX + vmax_class + pre_ops + fin_ops, C) + fin_units
    tl = math.ceil(math.log2(T) * 1e5) / 1e5; tli = int(round(tl * 100000))
    sb = 1 - (-(1 - H3D) * Dec(mu_target.numerator) / Dec(mu_target.denominator)).exp() - Dec(2) ** (-Dec(e.numerator) / Dec(e.denominator)) - Dec(2) ** -60
    out = dict(g=float(g), log2_g=math.log2(g), vbar=float(vbar), nfb=nfb, log2_nfb=math.log2(nfb), VMAX=VMAX,
               per_fb_units=float(1 + Fr(fixed, C) + vbar / C), log2_T=math.log2(T), time_log2=tl, fixed=fixed,
               per_good=per_good, w6_class_mean=sum(w6_per_class) / k, vmax_class=vmax_class, vmax_fb=vmax_fb,
               cheb_exp=float(e), mu_target=float(mu_target), T_num=T.numerator, T_den=T.denominator,
               tight_up=T.numerator ** 100000 <= (2 ** tli) * T.denominator ** 100000,
               tight_down=T.numerator ** 100000 > (2 ** (tli - 1)) * T.denominator ** 100000,
               # success bound: 1 - exp(-(1-2^-10.4) mu) - 2^-e - 2^-60 (Section 10, H3 + Chebyshev + repeat block)
               success_lower_bound=float(sb), preprocessing_log2=math.log2(A_C + A_S + DEV + pre_ops / C))
    assert out['tight_up'] and out['tight_down'] and sb > Dec('0.39')
    if show:
        for kk, v in out.items(): print('%-14s %s' % (kk, v))
    return out

# ---- experiments (organizer executor: one JSON request on stdin, one JSON document on stdout) ----
FEASIBLE_L = [l for l in range(32) if l not in (0, 2, 16, 18)]      # the 28 elements of L* whose row 16 can hold

def invert_cv(A, E, W):
    """Chaining value from the state rows 4..7 of member x and W0..W7 (inverting steps 7..0)."""
    a = {i: A[i] for i in range(4, 8)}; e = {i: E[i] for i in range(4, 8)}
    for i in range(7, -1, -1):
        T1 = (a[i] - S0(a[i-1]) - MAJ(a[i-1], a[i-2], a[i-3])) & M32
        a[i-4] = (e[i] - T1) & M32
        e[i-4] = (T1 - S1(e[i-1]) - CH(e[i-1], e[i-2], e[i-3]) - K[i] - W[i]) & M32
    return [a[-1], a[-2], a[-3], a[-4], e[-1], e[-2], e[-3], e[-4]]

def draw_F7(rng):
    """Uniform on F7 from its affine decomposition (Section 5.1): 2^26 + 2^20 words."""
    r = rng(); w = r & M32
    bit = lambda k: (w >> k) & 1
    def setb(w, k, v): return (w & ~(1 << k)) | (v << k)
    if (r >> 32) % 65:                                   # the 2^26-word space with probability 64/65
        for k, v in ((11, 0), (22, 1), (26, 1)): w = setb(w, k, v)
        w = setb(w, 18, bit(1)); w = setb(w, 30, bit(9)); w = setb(w, 28, bit(0))
    else:
        for k, v in ((11, 1), (12, 0), (22, 0), (23, 1), (26, 0), (27, 1)): w = setb(w, k, v)
        w = setb(w, 18, bit(1)); w = setb(w, 19, bit(2)); w = setb(w, 30, bit(9)); w = setb(w, 31, bit(10))
        w = setb(w, 28, bit(0)); w = setb(w, 29, bit(1))
    assert inF(w, D7, T7)
    return w

def sfs_trial(rng, Lt, cap=1 << 11, restarts=12, tail_cap=1 << 14):
    """A 37-step semi-free-start collision whose second-block state uses a seed-chosen variant of a seed-chosen class:
    rows 16..21 by proposals with each row's fixed x-bits of E imposed, row 22 by W22 proposals (x-cells and two-bit
    conditions imposed), W7 uniform on F7, W6 = W22 - s1(W20) - W15 - s0(W7) accepted iff in F6, then rows 22..36
    with the variant's W8; W0..W5 by the inverse expansion and CV1 by inverting steps 7..0."""
    c = rng.below(len(CLASSES)); members = class_members(*CLASSES[c]); vi = rng.below(len(members)); a0 = members[vi]
    l = FEASIBLE_L[rng.below(len(FEASIBLE_L))]; Ld = Lt[l]
    for attempt in range(restarts):
        X, Y = new_rows(Ld['tx'], Ld['ty'])
        tries = []; dead = False
        for t in range(16, 22):
            m, v, _, _ = CELLS['E'][t]
            dW = (s1(Y[2][t-2]) - s1(X[2][t-2]) + Y[2][t-7] - X[2][t-7] + (T6 if t == 21 else 0)) & M32
            base = (X[0][t-4] + X[1][t-4] + S1(X[1][t-1]) + CH(X[1][t-1], X[1][t-2], X[1][t-3]) + K[t]) & M32
            n = 0
            while True:
                n += 1
                if n > cap: dead = True; break
                X[2][t] = (((rng() & M32) & ~m | v) - base) & M32; Y[2][t] = (X[2][t] + dW) & M32
                step_rows(X, Y, t)
                if row_ok(X, Y, t) and x2_ok(X, t): break
            if dead: break
            tries.append(n)
        if not dead: break
    if dead: return None
    w8x = (W8C - ((a0 + C4) & M32)) & M32
    mw, vw, _, _ = CELLS['W'][22]
    n = 0
    while True:
        n += 1
        if n > tail_cap: return None
        w22 = ((rng() & M32) & ~mw) | vw
        b = lambda k: (w22 >> k) & 1
        w22 = (w22 & ~((1 << 1) | (1 << 0) | (1 << 25) | (1 << 21))) | ((1 - b(31)) << 1) | ((1 - b(30)) << 0) | ((1 - b(16)) << 25) | ((1 - b(14)) << 21)
        w7 = draw_F7(rng)
        w6 = (w22 - s1(X[2][20]) - X[2][15] - s0(w7)) & M32
        if not inF(w6, D6, T6): continue
        Xc = [dict(d) for d in X]; Yc = [dict(d) for d in Y]
        Xc[2][6], Xc[2][7], Xc[2][8] = w6, w7, w8x
        Yc[2][6], Yc[2][7], Yc[2][8] = (w6 + D6) & M32, (w7 + D7) & M32, (w8x + D8) & M32
        ok = True
        for t in range(22, R):
            for (A_, E_, W_) in (Xc, Yc): W_[t] = (s1(W_[t-2]) + W_[t-7] + s0(W_[t-15]) + W_[t-16]) & M32
            step_rows(Xc, Yc, t)
            if not (row_ok(Xc, Yc, t) and x2_ok(Xc, t)): ok = False; break
        if ok: break
    tries.append(n)
    W = dict(Xc[2])
    W[5] = (W[21] - s1(W[19]) - W[14] - s0(W[6])) & M32
    W[4] = (W[20] - s1(W[18]) - W[13] - s0(W[5])) & M32
    W[3] = (W[19] - s1(W[17]) - W[12] - s0(W[4])) & M32
    W[2] = (W[18] - s1(W[16]) - W[11] - s0(W[3])) & M32
    W[1] = (W[17] - s1(W[15]) - W[10] - s0(W[2])) & M32
    W[0] = (W[16] - s1(W[14]) - W[9] - s0(W[1])) & M32
    mx = [W[i] for i in range(16)]; my = mx[:6] + [Yc[2][i] for i in range(6, 16)]
    Avar = {i: SAx[i] for i in range(14)}; Avar[0] = a0
    Evar = {4: (a0 + C4) & M32, 5: SE[5], 6: SE[6], 7: SE[7]}
    cv = invert_cv(Avar, Evar, W)
    # checks: Step-2 words of (cv, a0) are exactly W0..W13; equal 37-step outputs; distinct blocks; every cell of rows
    # -4..36 (the XOR cells of W6/W7 excepted) and every printed two-bit condition of rows 8..36; class membership
    wx, wy = words_from_cv(cv, a0)
    ok = wx == mx[:14] and wy == my[:14] and compress(cv, mx) == compress(cv, my) and mx != my
    tx, ty = trace(cv, mx), trace(cv, my)
    ok = ok and all(row_ok(tx, ty, i, i not in (6, 7)) for i in range(-4, R)) and all(x2_ok(tx, r) for r in range(8, R))
    ok = ok and in_G(a0) and c7of(a0) == CLASSES[c][0] and mx[8] != MX[8] and inF(mx[6], D6, T6) and inF(mx[7], D7, T7)
    obs = dict(class_index=c, variant_index=vi, l=l, checks_passed=int(ok), restarts=attempt, proposals_row16=tries[0], proposals_tail=tries[-1])
    return cv, mx, my, obs

def online_trial(rng, Lt, R16, max_fb=64, sample=12, max_classes=2):
    """The counted online program on seed-drawn first blocks until one W7-passing class occurs (at most max_fb);
    every lane of every batch is checked against the scalar W6 definition, every good pair against the Step-2
    equations (W7, W6 in F7, F6), and `sample` good pairs against every cell of rows -4..15 for all 32 l in L*."""
    CD = {}; bad = [0, 0, 0]; firstpair = []
    def check(kind, cv, a0, cd, bt=None, fail=None, nl=None, u=None):
        if kind == 'u':
            wx = words_from_cv(cv, a0)[0]
            if u != (wx[0] + s0(wx[1])) & M32: bad[1] += 1
        elif kind == 'good':
            wx, wy = words_from_cv(cv, a0)
            if not (inF(wx[7], D7, T7) and inF(wx[6], D6, T6) and wx[7] == (cd.c7 - cv[0]) & M32): bad[1] += 1
            if len(firstpair) < sample:
                for l in range(32):
                    (x14, x15), (y14, y15) = lstar(l)
                    tx = trace(cv, wx + [x14, x15], 16); ty = trace(cv, wy + [y14, y15], 16)
                    if not all(row_ok(tx, ty, i, i not in (6, 7)) for i in range(-4, 16)): bad[2] += 1
                firstpair.append((wx, wy))
        else:
            for L in range(nl):
                a0 = cd.members[256 * bt + L]
                w6 = (C6 - cv[1] + MAJ(A1, a0, cv[0]) - CH(E5, (a0 + C4) & M32, (k3of(a0) + cv[0]) & M32)) & M32
                if ((fail >> L) & 1) == inF(w6, D6, T6): bad[0] += 1
    stats = dict(fb=0, hits=0, good=0, r16=0); ops = 0
    for f in range(max_fb):
        n, found = online(1, rng, CD, Lt, R16, stats, check, max_classes)
        ops += n
        if stats['hits']: break
    if firstpair: firstpair[0] = (stats['m0'],) + firstpair[0]
    obs = dict(first_blocks=stats['fb'], w7_classes=stats.get('hits_found', 0), classes_processed=stats['hits'],
               good_pairs=stats['good'], row16_pairs=stats['r16'],
               counted_ops=ops, lane_mismatches=bad[0], filter_mismatches=bad[1], cell_mismatches=bad[2],
               pairs_cell_checked=len(firstpair))
    return firstpair[0] if firstpair else None, obs

def run_request(req):
    Lt = setup_l(); R16 = make_R16(Lt)
    eid = req['experiment_id']; out = []
    for tr in req['trials']:
        t = tr['trial']; rng = Shake(eid + '|' + tr['seed'])
        rec = dict(trial=t, message_a_hex=None, message_b_hex=None)
        if eid.startswith('a0-sfs') and t < 16:
            r = sfs_trial(rng, Lt)
            if r:
                cv, mx, my, obs = r
                rec['message_a_hex'] = struct.pack('>24I', *(cv + mx)).hex()
                rec['message_b_hex'] = struct.pack('>24I', *(cv + my)).hex()
                rec['observations'] = obs
        elif eid.startswith('a0-online') and t < 8:
            pair, obs = online_trial(rng, Lt, R16)
            rec['observations'] = obs
            if pair and obs['lane_mismatches'] == obs['filter_mismatches'] == obs['cell_mismatches'] == 0:
                # the complete 128-byte messages M0 || M1 and M0 || M1' of the trial's first good pair, with l = 13
                # (the published element of L*); they are not expected to collide (that needs rows 16..36)
                m0, wx, wy = pair; (x14, x15), (y14, y15) = lstar(13)
                rec['message_a_hex'] = struct.pack('>32I', *(m0 + wx + [x14, x15])).hex()
                rec['message_b_hex'] = struct.pack('>32I', *(m0 + wy + [y14, y15])).hex()
        out.append(rec)
    return dict(schema_version=1, trials=out)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'ledger':
        cal = calibrate(full=True)
        print(json.dumps({k: v for k, v in cal.items() if k != 'w6prog'}))
        pr = cal['w6prog']
        print('W6 programs per class: ops min %d max %d; loads max %d; peak live values max %d; class sizes %s' %
              (min(p[0] for p in pr), max(p[0] for p in pr), max(p[1] for p in pr), max(p[2] for p in pr), sorted({p[3] for p in pr})))
        ledger(cal)
    else:
        req = json.loads(sys.stdin.read())
        sys.stdout.write(json.dumps(run_request(req), separators=(',', ':')))
