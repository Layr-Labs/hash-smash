#!/usr/bin/env python3
# xtab.py - sha256-r37: the A0-variant attack on 37-step SHA-256 (ePrint 2026/1120 two-block attack, the whole variant family G of 12,103,680 A0-variants in
# 22,976 c7 classes) with an x-indexed precomputed table of merged W6 fibres.  Standard library only.  The 32-bit value x = A_{-1} of the chaining value takes only
# 2^32 values while the run draws about 2^55 first blocks, so everything that depends on x alone (the W7 class test, the values W6x - cb of the variants of every
# passing class, their partition into fibres of equal value whatever the class, the choice of the fibres of at least THETA members, the member blocks) is computed once
# for all x (charged preprocessing, memory reported only) and read online.  Online, one first block costs one compression, one table read and, per batch of 256 fibres,
# one 32-bit bit-sliced addition of the scalar cb to the fibre values with the F6 test, and the packed row-16 stage over the member blocks of the passing fibres
# with one direct lookup of the row-16 l-mask per lane.
# Definitions, constants, the characteristic tables, the variant family G, the classes, the packed good-pair arithmetic and the rows 16..36 check are those of the
# earlier filings 6c77089c, 1c368173, b947b377, 087a18c4, 1f12a09a, 7319bba and d3ec5c41 (re-read, not executed, and re-typed here); the direct row-16 mask table is the idea of
# 8aeaed1c and def128fc, the MAJ identity of f2fe1d4d; the table, the fibre merging, the fibre test, the segment scan, the cost model and the ledger are new here.
# The organizer experiments run this program with the table restricted to the 222 embedded classes (the sandbox cannot hold the whole family).
#   python3 xtab.py selftest     fast consistency checks        python3 xtab.py ledger   the exact ledger        stdin JSON: organizer experiments
import hashlib, json, math, struct, sys
from fractions import Fraction as Fr
from decimal import Decimal, getcontext

M32 = 0xffffffff
ONE = (1 << 256) - 1
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

def trace(cv, w16, n=R):
    A = {-1: cv[0], -2: cv[1], -3: cv[2], -4: cv[3]}; E = {-1: cv[4], -2: cv[5], -3: cv[6], -4: cv[7]}
    W = list(w16)
    for i in range(16, max(n, 16)): W.append((s1(W[i-2]) + W[i-7] + s0(W[i-15]) + W[i-16]) & M32)
    for i in range(n):
        E[i] = (A[i-4] + E[i-4] + S1(E[i-1]) + CH(E[i-1], E[i-2], E[i-3]) + K[i] + W[i]) & M32
        A[i] = (E[i] - A[i-4] + S0(A[i-1]) + MAJ(A[i-1], A[i-2], A[i-3])) & M32
    return A, E, W
def compress(cv, w16):
    A, E, _ = trace(cv, w16)
    return [(c + o) & M32 for c, o in zip(cv, [A[R-1], A[R-2], A[R-3], A[R-4], E[R-1], E[R-2], E[R-3], E[R-4]])]
def digest(msg):
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
W14X = 0xbd1d3f7b
LW15 = h8("""7dd41680 7dd41681 7dd416a0 7dd416a1 7dd41a80 7dd41a81 7dd41aa0 7dd41aa1 7dd43680 7dd43681 7dd436a0 7dd436a1
 7dd43a80 7dd43a81 7dd43aa0 7dd43aa1 fdb41680 fdb41681 fdb416a0 fdb416a1 fdb41a80 fdb41a81 fdb41aa0 fdb41aa1
 fdb43680 fdb43681 fdb436a0 fdb436a1 fdb43a80 fdb43a81 fdb43aa0 fdb43aa1""")
def lstar(l): return (W14X, LW15[l]), (W14X ^ 0x04400800, LW15[l] ^ 0x20000000)
D6, T6, D7, T7, D8, T8 = 0x20000000, 0x03c00800, 0xfbc00800, 0x017f8000, 0xe0000000, 0x043ff800
def inF(w, d, t): return ((s0((w + d) & M32) - s0(w)) & M32) == t
F6 = lambda w: inF(w, D6, T6)
F7 = lambda w: inF(w, D7, T7)

# ---- S (member x rows 0..13), the variant family G and the c7 classes ----
_tx = trace(CV0, MX, 14)
SA = [_tx[0][i] for i in range(14)]; SE = _tx[1]
A1, A2, A3, A4 = SA[1], SA[2], SA[3], SA[4]
E5, E6, E7 = SE[5], SE[6], SE[7]
C4 = (A4 - S0(A3) - MAJ(A3, A2, A1)) & M32                                    # E4 = a0 + C4
W8C = (SE[8] - A4 - S1(E7) - CH(E7, E6, E5) - K[8]) & M32                      # W8x = W8C - E4
C6 = (E6 - 2 * A2 + S0(A1) - S1(E5) - K[6]) & M32                              # W6x = C6 - A_{-2} + MAJ(A1,a0,A_{-1}) - CH(E5,E4,E3)
K3C = (A3 - S0(A2)) & M32                                                      # E3 = K3C - MAJ(A2,A1,a0) + A_{-1}
def in_G(a0):
    e4 = (a0 + C4) & M32
    if e4 >> 29: return False
    w = (W8C - e4) & M32
    b = lambda k: (w >> k) & 1
    return b(29) == 1 and b(1) != b(12) and b(8) != b(25) and b(14) == b(18)
def k3of(a0): return (K3C - MAJ(A2, A1, a0)) & M32
def ne4of(a0): return ~(a0 + C4) & M32
def c7of(a0):
    e4 = (a0 + C4) & M32
    return (E7 - A3 - k3of(a0) - S1(E6) - CH(E6, E5, e4) - K[7]) & M32
def w6of(a0, am1, am2):
    e4 = (a0 + C4) & M32; e3 = (k3of(a0) + am1) & M32
    return (C6 - am2 + MAJ(A1, a0, am1) - CH(E5, e4, e3)) & M32
def class_members(c7, base, mask):
    out, s = [], 0
    while True:
        a = base ^ s
        if in_G(a) and c7of(a) == c7: out.append(a)
        s = (s - mask) & mask
        if s == 0: break
    return sorted(out)

# the 222 classes: (c7, base, mask, size); class = {base ^ s : s subset of mask, in_G, c7of == c7}; exactly the classes of G with >= 3456 variants
CLASSES = [tuple(int(v, 16) for v in ln.split()[:3]) + (int(ln.split()[3]),) for ln in """
cc8e8c4c 1c010142 01fec08d 3456
cc8e8c5c 1c010112 01fec08d 3456
cc8e8c6c 1c010122 01fec08d 3456
cc8e8c7c 1c010132 01fec08d 3456
cc8e8c8c 1c010102 01fec08d 3456
cc8e8e1c 1c010352 01fec08d 3456
cc8e8e2c 1c010362 01fec08d 3456
cc8e8e3c 1c010372 01fec08d 3456
cc8e8e4c 1c010342 01fec08d 3456
cc8e8e5c 1c010312 01fec08d 3456
cc8e8e6c 1c010322 01fec08d 3456
cc8e8e7c 1c010332 01fec08d 3456
cc8e8e8c 1c010302 01fec08d 3456
cc8e901c 1c010152 01fec48d 3456
cc8e902c 1c010162 01fec48d 3456
cc8e903c 1c010172 01fec48d 3456
cc8e904c 1c010542 01fec08d 3456
cc8e905c 1c010512 01fec08d 3456
cc8e906c 1c010522 01fec08d 3456
cc8e907c 1c010532 01fec08d 3456
cc8e908c 1c010502 01fec08d 3456
cc8e9228 1c010760 01fec09d 3456
cc8e9238 1c010760 01fec09d 3456
cc8e9248 1c010740 01fec09d 3456
cc8e9258 1c010700 01fec0dd 3456
cc8e9268 1c010720 01fec09d 3456
cc8e9278 1c010720 01fec09d 3456
cc8e9288 1c010700 01fec09d 3456
cc8e9448 1c010940 01fec09d 3456
cc8e9458 1c010900 01fec0dd 3456
cc8e9468 1c010920 01fec09d 3456
cc8e9478 1c010920 01fec09d 3456
cc8e9488 1c010900 01fec09d 3456
cc968c4c 1c010142 01fec08d 3600
cc968c5c 1c010112 01fec08d 3600
cc968c6c 1c010122 01fec08d 3600
cc968c7c 1c010132 01fec08d 3600
cc968c8c 1c010102 01fec08d 3600
cc968e1c 1c010352 01fec08d 3600
cc968e2c 1c010362 01fec08d 3600
cc968e3c 1c010372 01fec08d 3600
cc968e4c 1c010342 01fec08d 3600
cc968e5c 1c010312 01fec08d 3600
cc968e6c 1c010322 01fec08d 3600
cc968e7c 1c010332 01fec08d 3600
cc968e8c 1c010302 01fec08d 3600
cc96901c 1c010152 01fec48d 3600
cc96902c 1c010162 01fec48d 3600
cc96903c 1c010172 01fec48d 3600
cc96904c 1c010542 01fec08d 3600
cc96905c 1c010512 01fec08d 3600
cc96906c 1c010522 01fec08d 3600
cc96907c 1c010532 01fec08d 3600
cc96908c 1c010502 01fec08d 3600
cc969228 1c010760 01fec09d 3584
cc969238 1c010760 01fec09d 3584
cc969248 1c010740 01fec09d 3584
cc969258 1c010700 01fec0dd 3584
cc969268 1c010720 01fec09d 3584
cc969278 1c010720 01fec09d 3584
cc969288 1c010700 01fec09d 3584
cc969448 1c010940 01fec09d 3584
cc969458 1c010900 01fec0dd 3584
cc969468 1c010920 01fec09d 3584
cc969478 1c010920 01fec09d 3584
cc969488 1c010900 01fec09d 3584
ce8e8d1c 1e010052 01fec08d 3456
ce8e8d2c 1e010062 01fec08d 3456
ce8e8d3c 1e010072 01fec08d 3456
ce8e8d4c 1e010042 01fec08d 3456
ce8e8d5c 1e010012 01fec08d 3456
ce8e8d6c 1e010022 01fec08d 3456
ce8e8d7c 1e010032 01fec08d 3456
ce8e8d8c 1e010002 01fec08d 3456
ce8e8f1c 1e010252 01fec08d 3456
ce8e8f2c 1e010262 01fec08d 3456
ce8e8f3c 1e010272 01fec08d 3456
ce8e8f4c 1e010242 01fec08d 3456
ce8e8f5c 1e010212 01fec08d 3456
ce8e8f6c 1e010222 01fec08d 3456
ce8e8f7c 1e010232 01fec08d 3456
ce8e8f8c 1e010202 01fec08d 3456
ce8e911c 1e010452 01fec08d 3456
ce8e912c 1e010462 01fec08d 3456
ce8e913c 1e010472 01fec08d 3456
ce8e914c 1e010442 01fec08d 3456
ce8e915c 1e010412 01fec08d 3456
ce8e916c 1e010422 01fec08d 3456
ce8e917c 1e010432 01fec08d 3456
ce8e918c 1e010402 01fec08d 3456
ce8e931c 1e010652 01fec08d 3456
ce8e932c 1e010662 01fec08d 3456
ce8e933c 1e010672 01fec08d 3456
ce8e934c 1e010642 01fec08d 3456
ce8e935c 1e010612 01fec08d 3456
ce8e936c 1e010622 01fec08d 3456
ce8e937c 1e010632 01fec08d 3456
ce8e938c 1e010602 01fec08d 3456
ce8e9528 1e010860 01fec09d 3456
ce8e9538 1e010860 01fec09d 3456
ce8e9548 1e010840 01fec09d 3456
ce8e9558 1e010800 01fec0dd 3456
ce8e9568 1e010820 01fec09d 3456
ce8e9578 1e010820 01fec09d 3456
ce8e9588 1e010800 01fec09d 3456
ce968d1c 1e010052 01fec08d 3600
ce968d2c 1e010062 01fec08d 3600
ce968d3c 1e010072 01fec08d 3600
ce968d4c 1e010042 01fec08d 3600
ce968d5c 1e010012 01fec08d 3600
ce968d6c 1e010022 01fec08d 3600
ce968d7c 1e010032 01fec08d 3600
ce968d8c 1e010002 01fec08d 3600
ce968f1c 1e010252 01fec08d 3600
ce968f2c 1e010262 01fec08d 3600
ce968f3c 1e010272 01fec08d 3600
ce968f4c 1e010242 01fec08d 3600
ce968f5c 1e010212 01fec08d 3600
ce968f6c 1e010222 01fec08d 3600
ce968f7c 1e010232 01fec08d 3600
ce968f8c 1e010202 01fec08d 3600
ce96911c 1e010452 01fec08d 3600
ce96912c 1e010462 01fec08d 3600
ce96913c 1e010472 01fec08d 3600
ce96914c 1e010442 01fec08d 3600
ce96915c 1e010412 01fec08d 3600
ce96916c 1e010422 01fec08d 3600
ce96917c 1e010432 01fec08d 3600
ce96918c 1e010402 01fec08d 3600
ce96931c 1e010652 01fec08d 3600
ce96932c 1e010662 01fec08d 3600
ce96933c 1e010672 01fec08d 3600
ce96934c 1e010642 01fec08d 3600
ce96935c 1e010612 01fec08d 3600
ce96936c 1e010622 01fec08d 3600
ce96937c 1e010632 01fec08d 3600
ce96938c 1e010602 01fec08d 3600
ce969528 1e010860 01fec09d 3584
ce969538 1e010860 01fec09d 3584
ce969548 1e010840 01fec09d 3584
ce969558 1e010800 01fec0dd 3584
ce969568 1e010820 01fec09d 3584
ce969578 1e010820 01fec09d 3584
ce969588 1e010800 01fec09d 3584
d28e8d1c 1a010052 01fec08d 3456
d28e8d2c 1a010062 01fec08d 3456
d28e8d3c 1a010072 01fec08d 3456
d28e8d4c 1a010042 01fec08d 3456
d28e8d5c 1a010012 01fec08d 3456
d28e8d6c 1a010022 01fec08d 3456
d28e8d7c 1a010032 01fec08d 3456
d28e8d8c 1a010002 01fec08d 3456
d28e8f1c 1a010252 01fec08d 3456
d28e8f2c 1a010262 01fec08d 3456
d28e8f3c 1a010272 01fec08d 3456
d28e8f4c 1a010242 01fec08d 3456
d28e8f5c 1a010212 01fec08d 3456
d28e8f6c 1a010222 01fec08d 3456
d28e8f7c 1a010232 01fec08d 3456
d28e8f8c 1a010202 01fec08d 3456
d28e911c 1a010452 01fec08d 3456
d28e912c 1a010462 01fec08d 3456
d28e913c 1a010472 01fec08d 3456
d28e914c 1a010442 01fec08d 3456
d28e915c 1a010412 01fec08d 3456
d28e916c 1a010422 01fec08d 3456
d28e917c 1a010432 01fec08d 3456
d28e918c 1a010402 01fec08d 3456
d28e931c 1a010652 01fec08d 3456
d28e932c 1a010662 01fec08d 3456
d28e933c 1a010672 01fec08d 3456
d28e934c 1a010642 01fec08d 3456
d28e935c 1a010612 01fec08d 3456
d28e936c 1a010622 01fec08d 3456
d28e937c 1a010632 01fec08d 3456
d28e938c 1a010602 01fec08d 3456
d28e9528 1a010860 01fec09d 3456
d28e9538 1a010860 01fec09d 3456
d28e9548 1a010840 01fec09d 3456
d28e9558 1a010800 01fec0dd 3456
d28e9568 1a010820 01fec09d 3456
d28e9578 1a010820 01fec09d 3456
d28e9588 1a010800 01fec09d 3456
d2968d1c 1a010052 01fec08d 3600
d2968d2c 1a010062 01fec08d 3600
d2968d3c 1a010072 01fec08d 3600
d2968d4c 1a010042 01fec08d 3600
d2968d5c 1a010012 01fec08d 3600
d2968d6c 1a010022 01fec08d 3600
d2968d7c 1a010032 01fec08d 3600
d2968d8c 1a010002 01fec08d 3600
d2968f1c 1a010252 01fec08d 3600
d2968f2c 1a010262 01fec08d 3600
d2968f3c 1a010272 01fec08d 3600
d2968f4c 1a010242 01fec08d 3600
d2968f5c 1a010212 01fec08d 3600
d2968f6c 1a010222 01fec08d 3600
d2968f7c 1a010232 01fec08d 3600
d2968f8c 1a010202 01fec08d 3600
d296911c 1a010452 01fec08d 3600
d296912c 1a010462 01fec08d 3600
d296913c 1a010472 01fec08d 3600
d296914c 1a010442 01fec08d 3600
d296915c 1a010412 01fec08d 3600
d296916c 1a010422 01fec08d 3600
d296917c 1a010432 01fec08d 3600
d296918c 1a010402 01fec08d 3600
d296931c 1a010652 01fec08d 3600
d296932c 1a010662 01fec08d 3600
d296933c 1a010672 01fec08d 3600
d296934c 1a010642 01fec08d 3600
d296935c 1a010612 01fec08d 3600
d296936c 1a010622 01fec08d 3600
d296937c 1a010632 01fec08d 3600
d296938c 1a010602 01fec08d 3600
d2969528 1a010860 01fec09d 3584
d2969538 1a010860 01fec09d 3584
d2969548 1a010840 01fec09d 3584
d2969558 1a010800 01fec0dd 3584
d2969568 1a010820 01fec09d 3584
d2969578 1a010820 01fec09d 3584
d2969588 1a010800 01fec09d 3584
""".strip().splitlines()]
NCLS = len(CLASSES)
# ---- L* and the row-16 enumeration (Section 6.2); the exact table has 1,052,672 (u, l) pairs, enumerated offline (appendix r16.c) ----
def new_rows(tx, ty): return [({**t[0]}, {**t[1]}, {i: t[2][i] for i in range(16)}) for t in (tx, ty)]
def step_rows(X, Y, t):
    for (A_, E_, W_) in (X, Y):
        E_[t] = (A_[t-4] + E_[t-4] + S1(E_[t-1]) + CH(E_[t-1], E_[t-2], E_[t-3]) + K[t] + W_[t]) & M32
        A_[t] = (E_[t] - A_[t-4] + S0(A_[t-1]) + MAJ(A_[t-1], A_[t-2], A_[t-3])) & M32
def setup_l():
    L = []
    for l in range(32):
        (x14, x15), (y14, y15) = lstar(l)
        tx = trace(CV0, MX[:14] + [x14, x15], 16); ty = trace(CV0, MY[:14] + [y14, y15], 16)
        base = (tx[0][12] + tx[1][12] + S1(tx[1][15]) + CH(tx[1][15], tx[1][14], tx[1][13]) + K[16]) & M32
        L.append(dict(l=l, tx=tx, ty=ty, base=base, C16=(base + s1(x14) + MX[9]) & M32,
                      dW16=(s1(y14) - s1(x14) + MY[9] - MX[9]) & M32))
    return L
def row16_ok(Ld, e16):
    X, Y = new_rows(Ld['tx'], Ld['ty'])
    X[2][16] = (e16 - Ld['base']) & M32; Y[2][16] = (X[2][16] + Ld['dW16']) & M32
    step_rows(X, Y, 16)
    return row_ok(X, Y, 16) and x2_ok(X, 16)
E16M, E16V = CELLS['E'][16][0], CELLS['E'][16][1]
FEASIBLE_L = [l for l in range(32) if l not in (0, 2, 16, 18)]
def make_R16(Lt):
    """u -> mask of the l in L* whose row 16 holds for E16x = C16_l + u (evaluated; the offline table is its enumeration)"""
    def R16(u):
        mask = 0
        for l in FEASIBLE_L:
            Ld = Lt[l]; e = (Ld['C16'] + u) & M32
            if (e & E16M) == E16V and row16_ok(Ld, e): mask |= 1 << l
        return mask
    return R16
class Shake:
    def __init__(self, seed): self.seed = seed.encode(); self.k = 0; self.buf = b''; self.pos = 0
    def __call__(self):
        if self.pos + 32 > len(self.buf):
            self.buf = hashlib.shake_256(self.seed + b'|' + str(self.k).encode()).digest(1 << 14); self.k += 1; self.pos = 0
        v = int.from_bytes(self.buf[self.pos:self.pos + 32], 'little'); self.pos += 32; return v
    def below(self, n): return self() % n

class Mach:
    def __init__(self): self.n = 0
CTRL_FB, SCAN_LANE, SEG_OVH, BATCH_OVH, RARE_LOOKUP, RECOMP = 16, 6, 6, 71, 2, 35     # BATCH_OVH: loop 3, pointers 2, cost word 3, reload of the 32 z planes 63
ROWCHECK, ROWCOMP = 53, 106
LM = sum(M32 << (64 * k) for k in range(4)); M256 = ONE
def bc(x): return sum((x & M32) << (64 * k) for k in range(4))
def first_block(mc, rng):
    """two uniform 256-bit words; W0..W15 are their sixteen 32-bit fields (30 operations)"""
    r = [rng(), rng()]; mc.n += 2; w = []
    for k in range(16):
        x = r[k // 8]
        if k % 8: x >>= 32 * (k % 8); mc.n += 1
        if k % 8 != 7: x &= M32; mc.n += 1
        w.append(x & M32)
    return w
def chunk_fixed_ops(nl):
    """24-bit chunk extraction and zero branches of a plane with nl live lanes (zeros above): first chunk and top chunk one operation"""
    nch = (nl + 23) // 24; ops = 0
    for c in range(nch): ops += (0 if nch == 1 else (1 if c in (0, nch - 1) else 2)) + 1
    return ops
def scan_plane(mc, plane, nl):
    """lowest-first lane indices of the set bits: per chunk the extraction and a zero branch; per lane the address of the table entry (add of the
    chunk's table base), the load of the lane index, the add of the entry base, x - 1, x & (x - 1) and the loop branch: 6 (SCAN_LANE)"""
    mc.n += chunk_fixed_ops(nl); out = [L for L in range(nl) if (plane >> L) & 1]; mc.n += SCAN_LANE * len(out); return out
CVPRE_OPS = 81                                # 39 for the constants + 28 for the broadcasts to four lanes + 14 for unpacking the chaining value
RBASE = 0                                     # base address of the row-16 mask table (any value; it is folded into the per-first-block constant C)
def cv_pre(mc, cv):
    """per first block, the constants of W0 = a0 + kap0 and W1 (39 operations as counted: 4 + 11 + 3 + 16 + 5)"""
    Am1, Am2, Am3, Am4, Em1, Em2, Em3, Em4 = cv
    mc.n += 4; mj = (Am1 & Am2) | (Am3 & (Am1 | Am2))
    mc.n += 11; e0b = (Am4 - S0(Am1) - mj) & M32
    mc.n += 3; ch = (Em1 & (Em2 ^ Em3)) ^ Em3
    mc.n += 16; kap0 = (e0b - Am4 - Em4 - S1(Em1) - ch - K[0]) & M32
    mc.n += 5 + 42; n12 = Am1 & Am2            # n12, kap1', RBASE + kap0, the biases (5), the broadcasts and the unpacking (42)
    return dict(e0b=e0b, kap0=kap0, C=kap0 + RBASE, x12=Am1 ^ Am2, n12=n12, X=Em1 ^ Em2, Em2=Em2, kap1=(A1 - K[1] - Em3 - n12) & M32)
GROUP_OPS, PROBE_OPS = 32, [3, 4, 4, 3]       # group body: address adds 2 (pointers of the A and S arrays), ld A 1, ld S 1, E0 2, mj 1, ch 2, S1 8, W1 5, s0 8, U = A + s0W + C 2; probe: extraction (1|2|2|1), load, branch
GROUP_FULL = GROUP_OPS + sum(PROBE_OPS)       # 46: every lane of every group is probed (the padding lanes repeat the last member)
LOOP_SEG, UNROLL, LOOP_ITER = 9, 8, 3         # a segment of g groups is run as floor(g/8) iterations of an 8-group block (control 4 each) and then blocks of 4, 2, 1 groups chosen by the bits of the remainder (11 in all, plus the entry test)
def seg_ops(n):
    """operations of one segment of n members after its set-up: the loop control and 46 per group"""
    g = (n + 3) // 4; return LOOP_SEG + LOOP_ITER * (g // UNROLL) + GROUP_FULL * g
def packed_u(recs, pre):
    """The row-16 table address of four variants held in the four 64-bit lanes of 256-bit words: A = a0 per lane, S = S0(a0) per lane (two arrays in memory, zero high halves),
    address = a0 + s0(W1) + (RBASE + kap0) = RBASE + u + (0 or 2^32 or 2^32 + ...), u = W0 + s0(W1) mod 2^32 with W0 = a0 + kap0.  The table Rmask3 holds Rmask three times
    (3 x 2^32 words), so no reduction mod 2^32 is needed: a0 < 2^31, s0W < 2^32, kap0 < 2^32.  Lane-safe: every intermediate lane stays below 2^35 (the minuend of W1 carries the
    bias 2^34); MAJ(a0, Am1, Am2) = (a0 & (Am1 ^ Am2)) + (Am1 & Am2) with the second term folded into kap1.  Lane k of the result holds the address (< 2^34) and nothing above."""
    Aw = 0; Sw = 0
    for k in range(4): Aw |= recs[k] << (64 * k); Sw |= S0(recs[k]) << (64 * k)
    E0 = (Aw + bc(pre['e0b'])) & LM
    mj = Aw & bc(pre['x12'])
    ch = (E0 & bc(pre['X'])) ^ bc(pre['Em2'])
    d = (E0 | (E0 << 32)) & M256
    S1E = (((d >> 6) ^ (d >> 11)) ^ (d >> 25)) & LM
    W1 = (sum((pre['kap1'] + (1 << 34)) << (64 * k) for k in range(4)) - Sw - mj - S1E - ch) & LM
    d1 = (W1 | (W1 << 32)) & M256
    s0W = (((d1 >> 7) ^ (d1 >> 18)) ^ (W1 >> 3)) & LM
    U = (Aw + s0W + bc64(pre['C'])) & M256
    for k in range(4): assert (U >> (64 * k)) & M64 < 3 << 32
    return U
M64 = (1 << 64) - 1
def bc64(x): return sum(x << (64 * k) for k in range(4))
def mask_lookup(U, k):
    """the direct lookup of lane k of U in the row-16 mask table Rmask3 (3 x 2^32 words from RBASE, word i = the l-mask of i mod 2^32, 0 iff that value is not in the row-16 table):
    extraction of the address (k = 0: and with a 64-bit mask; k = 1, 2: shr, and; k = 3: shr, nothing lies above the top lane), the load, the branch on zero; each primitive
    counted where it executes.  Returns (address, operations)."""
    ops = 0
    if k: U >>= 64 * k; ops += 1
    if k < 3: U &= M64; ops += 1
    ops += 1; ops += 1                                         # load Rmask3[address]; branch on zero
    assert ops == PROBE_OPS[k]
    return U, ops
def good_group(mc, recs, pre, probe):
    """one group of four members (a segment's padding lanes repeat its last member): the address word (GROUP_OPS operations), then the direct lookup of every lane
    (PROBE_OPS).  probe(address) -> the l-mask.  Returns [(lane, u, mask)] for the members of the row-16 table, u = address mod 2^32."""
    mc.n += GROUP_OPS
    U = packed_u(recs, pre); hits = []
    for k in range(4):
        ad, ops = mask_lookup(U, k); mc.n += ops
        m = probe(ad)
        if m: hits.append((k, (ad - RBASE) & M32, m))
    return hits
def recompute_w67(mc, a0, a, b):
    mc.n += RECOMP; return w6of(a0, a, b), (c7of(a0) - a) & M32
def step3b(mc, cv, a0, w6, w7, ls, Lt):
    """for each l in the row-16 mask: both members' words and rows 16..36 with early abort (counted)"""
    Am1, Am2, Am3, Am4, Em1, Em2, Em3, Em4 = cv
    Ar = {-1: Am1, -2: Am2, -3: Am3, -4: Am4, 0: a0, 1: SA[1], 2: SA[2], 3: SA[3], 4: SA[4], 5: SA[5]}
    Er = {-1: Em1, -2: Em2, -3: Em3, -4: Em4}
    for i in range(6): Er[i] = (Ar[i] + Ar[i-4] - S0(Ar[i-1]) - MAJ(Ar[i-1], Ar[i-2], Ar[i-3])) & M32
    W = {i: (Er[i] - Ar[i-4] - Er[i-4] - S1(Er[i-1]) - CH(Er[i-1], Er[i-2], Er[i-3]) - K[i]) & M32 for i in range(6)}
    mc.n += 201                                               # W0..W5 and W8
    w8 = (W8C - (a0 + C4)) & M32
    for l in ls:
        mc.n += 2 + 6
        Ld = Lt[l]; (x14, x15), (y14, y15) = lstar(l)
        Wx = [W[0], W[1], W[2], W[3], W[4], W[5], w6, w7, w8] + MX[9:14] + [x14, x15]
        Wy = [W[0], W[1], W[2], W[3], W[4], W[5], (w6 + D6) & M32, (w7 + D7) & M32, (w8 + D8) & M32] + MY[9:14] + [y14, y15]
        X, Y = new_rows(Ld['tx'], Ld['ty'])
        for i in range(16): X[2][i] = Wx[i]; Y[2][i] = Wy[i]
        ok = True
        for t in range(16, R):
            for (_, _, Ww) in (X, Y): Ww[t] = (s1(Ww[t-2]) + Ww[t-7] + s0(Ww[t-15]) + Ww[t-16]) & M32
            step_rows(X, Y, t); mc.n += ROWCOMP + ROWCHECK + 1
            if not (row_ok(X, Y, t) and x2_ok(X, t)): ok = False; break
        if ok: return l, Wx[:16], Wy[:16]
    return None
# ---- semi-free-start collisions with variant dense parts (organizer experiment a0-sfs-r37) ----
def draw_F7(rng):
    """uniform on F7 from its affine decomposition: 2^26 words with probability 64/65, 2^20 words with probability 1/65"""
    r = rng(); w = r & M32
    def setb(w, k, v): return (w & ~(1 << k)) | (v << k)
    bit = lambda k: (w >> k) & 1
    if (r >> 32) % 65:
        for k, v in ((11, 0), (22, 1), (26, 1)): w = setb(w, k, v)
        w = setb(w, 18, bit(1)); w = setb(w, 30, bit(9)); w = setb(w, 28, bit(0))
    else:
        for k, v in ((11, 1), (12, 0), (22, 0), (23, 1), (26, 0), (27, 1)): w = setb(w, k, v)
        w = setb(w, 18, bit(1)); w = setb(w, 19, bit(2)); w = setb(w, 30, bit(9)); w = setb(w, 31, bit(10))
        w = setb(w, 28, bit(0)); w = setb(w, 29, bit(1))
    assert inF(w, D7, T7)
    return w
def invert_cv(Av, Ev, W):
    """chaining value from the state rows 4..7 of member x and W0..W7 (inverting steps 7..0)"""
    a = {i: Av[i] for i in range(4, 8)}; e = {i: Ev[i] for i in range(4, 8)}
    for i in range(7, -1, -1):
        T1 = (a[i] - S0(a[i-1]) - MAJ(a[i-1], a[i-2], a[i-3])) & M32
        a[i-4] = (e[i] - T1) & M32
        e[i-4] = (T1 - S1(e[i-1]) - CH(e[i-1], e[i-2], e[i-3]) - K[i] - W[i]) & M32
    return [a[-1], a[-2], a[-3], a[-4], e[-1], e[-2], e[-3], e[-4]]
def words_from_cv(cv, a0):
    """W0..W13 of both members that connect cv to the state rows of the variant a0 (Lemma 4.1)"""
    out = []
    for Sx in (SA, SAy):
        A = {-1: cv[0], -2: cv[1], -3: cv[2], -4: cv[3]}; E = {-1: cv[4], -2: cv[5], -3: cv[6], -4: cv[7]}
        for i in range(14): A[i] = Sx[i]
        A[0] = a0
        for i in range(14): E[i] = (A[i] + A[i-4] - S0(A[i-1]) - MAJ(A[i-1], A[i-2], A[i-3])) & M32
        out.append([(E[i] - A[i-4] - E[i-4] - S1(E[i-1]) - CH(E[i-1], E[i-2], E[i-3]) - K[i]) & M32 for i in range(14)])
    return out
SAy = [trace(CV0, MY, 14)[0][i] for i in range(14)]

def sfs_trial(rng, Lt, cls=None, cap=1 << 11, restarts=12, tail_cap=1 << 14):
    c = rng.below(NCLS) if cls is None else cls; members = class_members(*CLASSES[c][:3]); a0 = members[rng.below(len(members))]
    l = FEASIBLE_L[rng.below(len(FEASIBLE_L))]; Ld = Lt[l]
    for attempt in range(restarts):
        X, Y = new_rows(Ld['tx'], Ld['ty']); tries = []; dead = False
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
    mw, vw, _, _ = CELLS['W'][22]; n = 0
    while True:
        n += 1
        if n > tail_cap: return None
        w22 = ((rng() & M32) & ~mw) | vw
        b = lambda k: (w22 >> k) & 1
        w22 = (w22 & ~((1 << 1) | (1 << 0) | (1 << 25) | (1 << 21))) | ((1 - b(31)) << 1) | ((1 - b(30)) << 0) | ((1 - b(16)) << 25) | ((1 - b(14)) << 21)
        w7 = draw_F7(rng); w6 = (w22 - s1(X[2][20]) - X[2][15] - s0(w7)) & M32
        if not inF(w6, D6, T6): continue
        Xc = [dict(d) for d in X]; Yc = [dict(d) for d in Y]
        Xc[2][6], Xc[2][7], Xc[2][8] = w6, w7, w8x
        Yc[2][6], Yc[2][7], Yc[2][8] = (w6 + D6) & M32, (w7 + D7) & M32, (w8x + D8) & M32
        ok = True
        for t in range(22, R):
            for (_, _, W_) in (Xc, Yc): W_[t] = (s1(W_[t-2]) + W_[t-7] + s0(W_[t-15]) + W_[t-16]) & M32
            step_rows(Xc, Yc, t)
            if not (row_ok(Xc, Yc, t) and x2_ok(Xc, t)): ok = False; break
        if ok: break
    tries.append(n)
    W = dict(Xc[2])
    for i in range(5, -1, -1): W[i] = (W[i + 16] - s1(W[i + 14]) - W[i + 9] - s0(W[i + 1])) & M32
    mx = [W[i] for i in range(16)]; my = mx[:6] + [Yc[2][i] for i in range(6, 16)]
    Avar = {i: SA[i] for i in range(14)}; Avar[0] = a0
    Evar = {4: (a0 + C4) & M32, 5: SE[5], 6: SE[6], 7: SE[7]}
    cv = invert_cv(Avar, Evar, W)
    wx, wy = words_from_cv(cv, a0)
    ok = wx == mx[:14] and wy == my[:14] and compress(cv, mx) == compress(cv, my) and mx != my
    tx, ty = trace(cv, mx), trace(cv, my)
    ok = ok and all(row_ok(tx, ty, i, i not in (6, 7)) for i in range(-4, R)) and all(x2_ok(tx, r) for r in range(8, R))
    ok = ok and in_G(a0) and c7of(a0) == CLASSES[c][0] and mx[8] != MX[8] and inF(mx[6], D6, T6) and inF(mx[7], D7, T7)
    return cv, mx, my, dict(class_index=c, variant_index=members.index(a0), l=l, checks_passed=int(ok), restarts=attempt, proposals_row16=tries[0], proposals_tail=tries[-1])

# ======================= NEW: the x-indexed table, the fibre test, the segment scan =======================
CDATA = {}
def cdata(c):
    """members of class c (sorted)"""
    if c not in CDATA:
        c7, base, mask, n = CLASSES[c]; m = class_members(c7, base, mask); assert len(m) == n; CDATA[c] = m
    return CDATA[c]
C7S = [c[0] for c in CLASSES]
def phi(a0, x):
    """W6x - cb for the variant a0 and A_{-1} = x:  W6x = cb + phi, cb = C6 - A_{-2}  (equal to w6of(a0, x, am2) - cb)"""
    e4 = (a0 + C4) & M32; e3 = (k3of(a0) + x) & M32
    return (MAJ(A1, a0, x) - CH(E5, e4, e3)) & M32
def passing_classes(x, cls=None): return [c for c in (range(NCLS) if cls is None else cls) if F7((C7S[c] - x) & M32)]
THETA = 40                    # the table keeps only fibres of at least THETA members (the parameter of the table build, not of the online program)
class XRec:
    """the table record of x: the variants of every class that passes the W7 test at x (F7(c7 - x)), grouped by the value phi (a fibre is the set of
    all such variants with equal phi, whatever their class), the fibres of at least `theta` members sorted by phi; member blocks padded to a multiple
    of four records by repeating the last member; the bit planes of the fibre values (256 fibres per batch, unused lanes repeat lane 0); per fibre
    the entry (first block word, end block word, V cost).  Built offline for every x (Section 8.2); read online."""
    def __init__(self, x, cls=None, theta=THETA):
        pc = passing_classes(x, cls); cnt = {}
        for c in pc:
            for a0 in cdata(c): v = phi(a0, x); cnt[v] = cnt.get(v, 0) + 1
        self.x = x; self.vals = sorted(v for v, m in cnt.items() if m >= theta); self.nf = len(self.vals)
        keep = {v: [] for v in self.vals}
        if keep:
            for c in pc:
                for a0 in cdata(c):
                    m = keep.get(phi(a0, x))
                    if m is not None: m.append(a0)
        del cnt
        self.recs = []; self.fib = []; self.members = []
        for v in self.vals:
            mem = sorted(keep[v]); ng = (len(mem) + 3) // 4; blk = list(mem); blk += [blk[-1]] * (4 * ng - len(blk))
            self.fib.append((len(self.recs) // 4, len(self.recs) // 4 + ng, SCAN_LANE + SEG_OVH + seg_ops(len(mem)))); self.recs += blk; self.members.append(mem)
        self.batches = []
        for b in range(0, self.nf, 256):
            lanes = self.vals[b:b + 256]; nl = len(lanes); lanes = lanes + [lanes[0]] * (256 - nl)
            pl = [sum(((v >> j) & 1) << L for L, v in enumerate(lanes)) for j in range(32)]
            self.batches.append((pl, nl))
NEEDW = (1, 2, 3, 8, 9, 10, 12, 13, 14, 15, 16, 18, 19, 20, 25, 26, 27, 29, 30, 31)
W6_OPS = 230          # exact count of w6_batch (asserted); +1 for the lane mask of a partial batch
def w6_batch(dl, z, nl):
    """pass plane of the F6 test for the fibre values dl (32 planes) plus the scalar cb (broadcast planes z): w = dl + z ripple (NOT-free full adder
    carry = a ^ ((a ^ b) & (a ^ c)), 4 operations, 5 with the sum), then F6 with w[8] ^ w[25] moved into the final mask.  The 32 plane loads each need
    an address: 31 adds after the first.  Returns (plane, executed operations)."""
    ops = 32 + 31; w = {}                                     # 32 loads of the planes, 31 address adds
    c = dl[0] & z[0]; ops += 1
    for j in range(1, 31):
        xy = dl[j] ^ z[j]; xz = dl[j] ^ c; carry = dl[j] ^ (xy & xz); ops += 4
        if j in NEEDW: w[j] = xy ^ c; ops += 1
        c = carry
    xy = dl[31] ^ z[31]; w[31] = xy ^ c; ops += 2
    common = (w[14] ^ w[18]) | (w[1] ^ w[12]); ops += 3
    bcc = (w[15] ^ w[19]) | (ONE ^ (w[9] ^ w[26])) | (w[2] ^ w[13]); ops += 6
    X = ((w[16] ^ w[20]) ^ w[31]) | (ONE ^ ((w[10] ^ w[27]) ^ w[31])) | ((w[3] ^ w[14]) ^ w[31]); ops += 9
    fail = common | (w[29] & (bcc | (w[30] & X))); ops += 4
    p = (w[8] ^ w[25]) & (ONE ^ fail); ops += 3
    assert ops == W6_OPS
    if nl < 256: p &= (1 << nl) - 1; ops += 1
    return p, ops
T0_OPS, HDR_LOADS, ZPLANE_OPS = 5, 3, 95
FBFIX = 30 + CTRL_FB + T0_OPS + HDR_LOADS + 2 + ZPLANE_OPS + CVPRE_OPS + 32      # 189: first block 30, control 16, table read 5 + 3 header loads, cb 2, planes 95, cv_pre 38

class Env:
    def __init__(self):
        self.Lt = setup_l(); self.R16 = make_R16(self.Lt); self.cache = {}; self.xc = {}
    def probe(self, ad):
        u = (ad - RBASE) & M32
        if u not in self.cache: self.cache[u] = self.R16(u)
        return self.cache[u]
    def xrec(self, x, cls, theta):
        k = (x, None if cls is None else tuple(cls), theta)
        if k not in self.xc:
            if len(self.xc) > 1: self.xc.clear()
            self.xc[k] = XRec(x, cls, theta)
        return self.xc[k]

def process_cv(mc, cv, w, env, stats, check=None, cls=None, theta=THETA):
    """everything the online phase does with one chaining value cv = F_37(IV, w): the table read, the fibre tests, the scans, the packed row-16
    stage over the member blocks of the passing fibres, and rows 16..36 of every row-16 pass."""
    found = []
    en = env.xrec(cv[0], cls, theta); stats['fibres'] = stats.get('fibres', 0) + en.nf
    mc.n += T0_OPS + HDR_LOADS
    if not en.nf: return found
    mc.n += 2 + ZPLANE_OPS + CVPRE_OPS + 32; cbv = (C6 - cv[1]) & M32; z = [ONE if (cbv >> j) & 1 else 0 for j in range(32)]
    pre = cv_pre(Mach(), cv); segs = []
    for b, (dl, nl) in enumerate(en.batches):
        plane, ops = w6_batch(dl, z, nl); mc.n += ops + BATCH_OVH
        if check: check('plane', cv, (en, b), plane)
        for L in scan_plane(mc, plane, nl):
            fid = 256 * b + L; mc.n += SEG_OVH; segs.append(fid)
    good = set(); stats['hits'] += 1
    for fid in segs:
        s, e, cost = en.fib[fid]; stats['seg'] = stats.get('seg', 0) + 1; mc.n += LOOP_SEG + LOOP_ITER * ((e - s) // UNROLL)
        good.update(en.members[fid])
        for g in range(s, e):
            recs = en.recs[4 * g:4 * g + 4]
            for (k, u, m) in good_group(mc, recs, pre, env.probe):
                stats['r16'] += 1; mc.n += 1 + RARE_LOOKUP
                a0 = recs[k]; ls = [l for l in FEASIBLE_L if (m >> l) & 1]
                w6, w7 = recompute_w67(mc, a0, cv[0], cv[1])
                r = step3b(mc, cv, a0, w6, w7, ls, env.Lt)
                if r: found.append((w, a0, r))
    stats['good'] += len(good)
    if check: check('class', cv, en, good)
    return found

def online(nfb, rng, env, stats, check=None, cls=None, theta=THETA):
    mc = Mach(); found = []
    for f in range(nfb):
        mc.n += CTRL_FB                                                   # control allowance (the 30 first-block operations are counted in first_block)
        w = first_block(mc, rng); cv = compress(IV, w); stats['fb'] += 1; stats['m0'] = w
        found += process_cv(mc, cv, w, env, stats, check, cls, theta)
    return mc.n, found

def detect(env, cv, mx, my, c, a0):
    mc = Mach(); st = dict(fb=0, hits=0, good=0, r16=0)
    fnd = process_cv(mc, cv, None, env, st, None, [c], 1)
    return int(any(f[1] == a0 and f[2][1] == mx and f[2][2] == my for f in fnd)), mc.n
THETA_EXP = 8                 # the experiments run the table build with this smaller THETA on the 222 embedded classes (the online program is the same for every THETA)
def online_trial(rng, env, max_fb=64, sample=12):
    """the counted online program on seed-drawn first blocks until one has a record with fibres (at most max_fb), the table restricted to the 222
    embedded classes with theta = THETA_EXP: every pass plane lane is checked against the scalar F6 test of its fibre value, the good set of the record
    against the brute-force definition over all variants of its passing classes, `sample` good pairs against every cell of rows -4..15 for all 32 l"""
    bad = [0, 0, 0]; firstpair = []
    def check(kind, cv, a, b):
        if kind == 'plane':
            en, bi = a; plane = b; cbv = (C6 - cv[1]) & M32
            for L in range(en.batches[bi][1]):
                if ((plane >> L) & 1) != F6((cbv + en.vals[256 * bi + L]) & M32): bad[0] += 1
            return
        en, good = a, b                                   # kind == 'class' (the whole record)
        pc = passing_classes(cv[0]); cnt = {}
        for c in pc:
            for a0 in cdata(c): ph = phi(a0, cv[0]); cnt[ph] = cnt.get(ph, 0) + 1
        want = {a0 for c in pc for a0 in cdata(c) if cnt[phi(a0, cv[0])] >= THETA_EXP and F6(w6of(a0, cv[0], cv[1]))}
        if want != good: bad[1] += 1
        for a0 in sorted(good)[:2]:
            wx, wy = words_from_cv(cv, a0)
            if not (inF(wx[7], D7, T7) and inF(wx[6], D6, T6) and F7((c7of(a0) - cv[0]) & M32)): bad[1] += 1
            if len(firstpair) < sample:
                for l in range(32):
                    (x14, x15), (y14, y15) = lstar(l)
                    tx = trace(cv, wx + [x14, x15], 16); ty = trace(cv, wy + [y14, y15], 16)
                    if not all(row_ok(tx, ty, i, i not in (6, 7)) for i in range(-4, 16)): bad[2] += 1
                firstpair.append((wx, wy))
    stats = dict(fb=0, hits=0, good=0, r16=0); ops = 0
    for f in range(max_fb):
        n, found = online(1, rng, env, stats, check, None, THETA_EXP); ops += n
        if stats['hits']: break
    if firstpair: firstpair[0] = (stats['m0'],) + firstpair[0]
    obs = dict(first_blocks=stats['fb'], records_with_fibres=stats['hits'], fibres=stats.get('fibres', 0), passing_fibres=stats.get('seg', 0), good_pairs=stats['good'],
               row16_pairs=stats['r16'], counted_ops=ops, lane_mismatches=bad[0], filter_mismatches=bad[1], cell_mismatches=bad[2],
               pairs_cell_checked=len(firstpair))
    return (firstpair[0] if firstpair else None), obs

def run_request(req):
    env = Env(); eid = req['experiment_id']; out = []
    for tr in req['trials']:
        t = tr['trial']; rng = Shake(eid + '|' + tr['seed'])
        rec = dict(trial=t, message_a_hex=None, message_b_hex=None)
        if eid.startswith('a0-sfs') and t < 128:
            r = sfs_trial(rng, env.Lt, (7 * t) % NCLS)
            if r:
                cv, mx, my, obs = r
                if t < 16:
                    a0v = class_members(*CLASSES[obs['class_index']][:3])[obs['variant_index']]
                    obs['detected_by_counted_program'], obs['counted_ops'] = detect(env, cv, mx, my, obs['class_index'], a0v)
                rec['message_a_hex'] = struct.pack('>24I', *(cv + mx)).hex(); rec['message_b_hex'] = struct.pack('>24I', *(cv + my)).hex()
                rec['observations'] = obs
        elif eid.startswith('a0-online') and t < 8:
            pair, obs = online_trial(rng, env); rec['observations'] = obs
            if pair and obs['lane_mismatches'] == obs['filter_mismatches'] == obs['cell_mismatches'] == 0:
                m0, wx, wy = pair; (x14, x15), (y14, y15) = lstar(13)
                rec['message_a_hex'] = struct.pack('>32I', *(m0 + wx + [x14, x15])).hex(); rec['message_b_hex'] = struct.pack('>32I', *(m0 + wy + [y14, y15])).hex()
        out.append(rec)
    return dict(schema_version=1, trials=out)
HIST_Z = '''
c-l3b$${*!4F&HLMTa2nWD-6*|496*@I8kCrKY%I2gv{Y_c!{--(TCmG4B2DZfpFt^J}}E-S%I*zrF4p^IL!I{aXLtn)k1Nzc$bA
Ys~T2+po2+oo{`Az30=}Zrdr3)NgC{)StiG#{1TJ>#whTJjXfxukT;K-+bRo`TY85r|(q1zrMe|&pGX{r`tPUe)${UZ|!xyz1!bt
405-7|3?4y`Ms~*@$J7c7|u6F>d)V7`^+}~Mml|MUEc0r`fO+3_czjMU-zX#`n+$nm8R3<%J1*{o0;esEp^iJOqZ$h-M^V0_gSO0
^*2Y#={RrauYZ}?y!~%3rf}xUXPM;dUu*4e(%sj_{G0c;R=@3=J2l?#yzzSfTOS)S=iPs+u^xH&Tm3iIeq*KQmEOL5meTyK>|K`h
Z>6&{znQA(>r20xN@|?nIDKU+*8R=VSIcNtCO7u(^KXB@EaYr08?@6|ALH!5ozAizeSCj={IW@xpC?;+Pw*h~+|KRJR8Dte-u(UT
^Go|H&8Dw&_xHx%PG8xtOyPXL$;@y2J1xsk#nXT5_OVws|BUo{vJEF&cHZUZ^_%Nvv;R)8^E=;M=kKt9JrnplH!GDrxOw@0cbyFE
erdYjv-<eE*{pun{QhoFLs{JUcUine#q3mC9-02%UBBSy+kbawOZE!^+ylzx?ccq@)%9L`@9)0!7_#_#LBq^7UHv_<Fq=F7Ue>LB
JL~=Tf`NCf%;tfBS-|u6GMmRrzbx6#DDJuA?=hVhI(rwC`}#{wkYSJe7bH%T@B4xmp|4D5PfD52yP?z+)6tsQhoI4~uLGLBJgh8c
mwdndoBMtJq!?_-4%0$*D7brfNd3ze&DT@4WmaErRBd2Ga5|;X^EcMm5Ke0&)5+$hG=FIpED8xgWSbV!*_@%^v>P7sGH<GeupkPm
zKrHl3Imxl=x`ekE!YXsgw9eS$e*6WJwhIfm-9C=;V&57!aITr*{m!^1|D3vG?4uYYEt*oF8j)q!a7)$l;9lw1b<UxCBx}b3KeHL
(_qR$z;KXs9Hx;e%N1c76BJD`IM`=?par`7Y*wZbzLVnn?a=LC3(E){WpPq79HVE(X(}8e%{8_ah7mSO2{g?9yl~N=S$2Cff-sCC
fvoj!-pT%lU(D2<VZ-4T!9tck+~Q`?J9{2(ksnxsaEokh=#DbHu<?Dk#n`>E+>14Qeh*=V?>s6TmIa(y;Ntv(v<+r)H%q)>Oc`IO
H4iYtEO<&RVSC_ZxJ9@pRYCgE!|5{!Fap%sNSF_l3Zod}=7zT33SXmUX!u5eM2s+GS0tRGhwbwcya+Q4&WBU1>{JSw(Rw?qr-fDY
4<gLEL|%me7+ZKn7L^f&SFEr<Y6c?)=o3~EOg++BSVhELz6hrX%eaWZu!<IH%E-ej@<Yfh6A!O=$g?a;&>?J(cjvb|qquOSkUj6x
&4fXQe1E6I03v-dZ@LSo2qzt<ffwNwqccTV#f!vCiTw$GO({4Y%v-EEtfGNmu!_j-M@{%^);>}kM!Q3GDW@M;QwINoz#@p@6Iq&_
QhLdD??_>|#0xD(UeF(6H!MPi8}i5pJB!=-I(!du2(4tMjWK4=)5+jnhp}e|Qq0aAIu3JKp}RB<Z&>sj)(}RQzx0B70jo+0)^Kb(
oZ+A|gfWB_z=gVOp`}_!{ss9`%0v!rz!S2!7jfNT3TLQ&Wcwrdc^As*Or^8;!HEnIO=4vSLh;$~%cn4d=q)HKh;*oyx8oP0&G_L3
A<6bqT+nw$6HbunX46v4)?XXEzn~H$M0a>-NN5f>I|NS&;|On!@a<s(K{dXe@X|#^*jxAm)zZgh#uK*PEg@D9zh$jPKcSeEvm+o#
w35iK&G4ju+Ff$&+F6u^{wRdeWcxC{5Pt|MBU%4&D<YE5-TA=Fs1`~Zq|X{`M0W%_#SqG4oi}RUxs*`yd?nkwUj$Il3s!)7mw8-R
O|&Hx3<_DQ3yF2KgAe2g$!96&NUxGSsCeL)XQQL_gC3%W$aXBgmE!3?1RsQg#e}{8qMQZ>dBfFd?eSrH2(_c{xkD%h>+&*a6^>46
FcS36`HQ?AK|UybfEQBwV<AH59pM*Z|J|r#4Ga&Zhh3!}O2Jv+riAXR4rf3^4wYv{{5F4KFcBSLkKhLdRJO?T%m5k>Vy19WOF>Xb
JUATH_XGb}hVdbuGq%W}On&vKv7vAfVtmNu5oIXFYyzw<v`q(D`v|%q6AjROFzTdOA~Ndq2agQhMXAj?@}?vG<_dZZXgi}GA?>`2
F_8Vu20_okCNOFEQeGH{T<kW>CI`2}v9h2u8gW|dZUHYlc*&eX*{p43ENa_k9M}m_JW|LOz|n*LziXw7;68&&w2x8`O-Gic_0V)M
CD7Fgw;GrPs0SnToQ8O_5Uhb4!kk&Cln;tb;AIH0JO;!Zo)9|%#WIRON+2j}8A^t6r`Ci7SRD2LS05~X%}|x)gEv`wCIcPcjGb4K
aZHmB-C|>;r1cPV3JUQR{Wj%+sSr4k`%D8OZhW{=5HVgB<Q2>rA>fW?8PWJdu}lZbjkPg+&{o5oq6z$>sb(D@-^D^ezR}DWa;SHQ
7Yvm9=;WDUh!_1Wn-S&_?9F09yq)%u*V+5@7}{lgDX^>g67wqJZBuKaqNhU$_cEIhZnU8d@<O;Yk4k?K*aI=mVj-oYzohX{EdngP
$7l$T8PF`YAF6y1EM$ufw~)4h;X8{R49zYu=Au4@L8gRgPD7#B0e4O*%o%(MxkkUb(L=|B<K(lDYbHXSumcb_#2UH5%7s=NI}NG6
$&1I#V%ddKqo9X9rr4|$+{>u5D-%hK?iphZ345s%RDplRv_jZ~K7yg)5>&bvtw@~-od##ZuYSh{S`!B*R2l?}Z3&HHn?j@Cv+_de
3k;r2?BkPi)UU=nIDOV^LZMVfB@gSTPDgFU%FT)(k75n}P$VYQ8LVQKq0Yq^L!1}MGEu@K1yTUR@8P!xzQjWQz$gmXw7{NOyzq|{
QM6Jwq#5}}L!r%}avDO?BHmKMlI6Py52X4GWp)OHl+AWBkja8%tRc*WZaR^$OiZ%GUdrzNG`F$HceXtIG~3Aw<acP2{h0q&dZ8gs
Itx_}YGH>Tkawb2e{_ag4P%ckqVSm*;GqjFd}xx@N1r~y{n(K|eG2H(5lfjo1ljNqbY)W7*+no@aT)`Q1;O6Vex<PCObjj*iS0Vk
p@aJ)s1=F~_5Vem3dac%%+TXxWkZg8hry;a;01vZbLEZz_xL9CGC=ehT0Bhb;DTZF=M^qMiV=g^=9HU^YeI~Zc0!D}EW%QM7&*8%
ut9-gu!E(>re?>msH0AQ84d<DbslC+INf}zu7NmoAi(*G$|rI&#%T%>3e7rrao%7!Aw?{L5FO?z?O@c-zl8z)#fV9%L8XDnv@oj$
AzB5y=tgj)2+!Vuh?|2i=HMj=L?ECvEv4oCi-qxfIH4Ana`q!E0l!POBAj4hCgZk&5Tkphu>RH3UDEgoVgaJn(Q>HJzVNI?{Dmzp
q-54$;ZuwJPQxKX>ty=|9wH><`EU>+g0m5;{~K~>FrppBHtNBTRzib8yi^GdMt}yg$S=ZhVf!+1Nbs;Y*u9$<NPrz$T4=feP&wPX
pg){R(BJ$V1KzR8D+FVt)WXgkK$bYFT&5HPyu8V9KlHtYRK%5af7<uaMSnN~R){awNM0ZjeG#K6JDK)FdxPc?hqxLR(hz@GNN)$}
Q^?{*C0!8ShpD+xW|;=MZ0wPjuOK}z0@6GFmR$qPe}><J>>6*NI!1{O%OFE^QG~3VwN3NLzz-Q1ne&S_v(R26|9DYbhOrv#NFjWJ
XN-t<qLZc!WdN~<V}7iIPMM*F<U$TKd;hI1t}J-{3c)cFgx`8}faF_zgR_y9MO)=PG=Xnyh1$@8R;Vq@mNr6dv=L&<BE+1GCH`Z9
AN$2PFhnO`?B9D}7lf8R$^uOvp|iBGLuS!`ZWbg6mi-F|ZowfoWOi{iBJSv9e=swCNu!Ob87Baz!wZF^Sd1*x#Pst5BD=t>YKIVZ
8!lN`V3^ViT*`;+b<BVK2^;?tFZ2?&6rSB+UPj2KLa2*QAg&e_eRrg1Kw2D{kh>QZ>=4%p3T^}(!w79fcu;u3+P^)p^zaXF#2YWz
rG3-MfCMuAP!?X44PjXW$>wBnK!@LMC~L>q*#k$&-=1Z$V5sb=x*Q0T2_N53R$80Lh?bq&c$+70HV*Q@BL+p+%T@-ZQ^NL5TTA|u
epZu7Z8Xi-d4bUzK%-&&8#fVvCf!?gOum2};^;-5r3M<NX6{zM3{W)=4DP2|DC&gMq#*8Z>B;IrCx9AMriBDceFPYj2`z;SZ)oYm
OGG&|nhtOhGxmcqn-=i;OnuM{F+jfp1+4MB4<*GU&^g_}@r|eFu`VGb0jzp~0J?(%a4#~uE9Z-*7Ig=1xo=VDMuCiZkwSCWsE;lj
GAmqv<Iy?%zTn@1FzM_%uMWIsBe1OT)Krdc9L%6obQF;X>%@KT=A2Kr$BAKhq$6H!%=193(}0U1PvL>j2eU3nd>UTQR1XbBic>%U
_CPpODCVdv25kL+DI8Yngo03!4g?g?F>`xtq!b(5f1seZDQHCp(jwF8c>e;nfs7P_mAt;_E{B@1q`xRM=_x%H`J4gsB$#xDcz*QA
Zk}}~2C_NdjbJ|*ZG;cB*=Xb0N62U4ojX%+Z=f8R_yQa$AV_&XtFk@7AUcifa}BsGH7z_pz)0Jy0NP-BL>Y`horPP~VhG1sgl-6U
7>VirF4v6N4_ghCz+))=)6$RL)PU^F17@q!{>Eh!syG`nnD?19!H!)sRtSa1GV~&xbFfm=;gJl_(W8|aXoLmC2BW`F%>mFJ{3W{S
&-Yg~>fkj=2hhxiL2*JeOkC3|6Aa0K5co<A;zcE{-@_-volZ%fQ=t={WxeNND2CC*qI3aJ@;33Y*vIhEgRvFKb)Xk^`?<@6caG!7
(mD+A;gI~hp_UM2Q1yON;6=H6JmO#vz<7(yy`ST|pIXOC;nXu5a)}zb!?9vQg&EInt)8QDL={b8NIO@*CJ-(jfbSqCWJ(8=xVkgb
KNb}YAZ#$MFPdC_??~DaILjQm5D4!vp{OQTxOgnTh}YX|Tm$z&K0|TK=mxfXw2f52cFG4sPk3OO%YS4G%R!ieZlR5+rPo;I!B)Go
W;i9?z`>5(@?Ydj{E%sPGOjcbia3C)^2G1>MgAi5ei-=|9WB2@5d@<yk|h79QPdRBqj<6LeGzaw{*HEbczn)ltE{Jf=z(1zv=E+u
Ll2k7NdV;wg4|F<#NmY?h~@3tPE8?ViFa3nxD~%3+$G|e|MKTd{y?v(cBVS)Ju0P_C}UPM1&4<WVN*g4ED_YOFzYVSg8UD)vgVh-
Wq@t*jENZ#+&F3L%JOb#fuL*(wQ|aiynnX!&_Tk(ZwMhBJQxYk?Nn-n(}(h|;lcm|CxP<1hx&!pm6F@~@HY5}ULP=xsJxUM+zTO~
5kBZ3|7~rifRg<8@Gt}$o<YC>8pC{jnl%ATHQho5i~141S^uX=6M#(P=V}dm<|8`ziU^(xR|W?W1YJ@n{`>IqMQ3^)M_GVjLm1M-
jqn#%neiN=tF1l=AzbM7VZWpyl&p}`!+*ddW*j2&K?uCKnmG^K<?j)u!`JjC*zqQ=4q&x~YBg~kzga5Vn>3ekPucG?9yfR|vb|+S
M4-I#>4i^EDGhofSkDfG7J~8*=X(s(6l!RzknLfoq;^Ol)O1-j0`mloQK-|r?)Cs&fkc`^3jDf>kOtNkKnbm?V`2Y2qVFukDf~b%
U`4zGp}wQPD3Az80CJEZPt23>y8yj@flutgD)|U~UxFF|T{3#1gj5P4#JI`FAp~9`1$mMV-i3w7l6c63JS!8z5+5W$ra)Sd2p+<K
&Y#UF3Rr!-Zah1~KsjWvAvk+TQTa*~1mde90RE{%1mgN74F1WzajpbW{Y3T_h+e;*b>6Rn?w?9h3J@wTAL1T_*qd~Z`u!Vr+}Mc#
>@VWiVP*f?xL6`M!SS!rdT&<6`MoV@BL*78{~)$J;3x$eLZNW}y|_wwk_Bq=*dGKZzYqp9ML=vqsUP|iV4{%_$FC8EG7vv0xSE7*
l>8|?M;6+cX@+m6+D>5CVS(B1N`yet2g8^(acp{5e!A6x;Is>jF+VFY0n5l&qqfPgG?@&mTG84tnc!Rh28Wy=8vLzS4P$S74i`g%
aO=0V3j!yua!c!9Wn371joRc7*$!80KNm;aouQoC6|z#MTU%-qGU|62;#sxcA&?_#g+8WV!m4Nz3L(7$!xcYaimf*7B5B!H+}6`K
h)3rIrC1kQ@x`fTf{(K~zxxVjADS|-Id)8r>lm@wY4xqzE`mx;Gz_U6hy5H}Gmb=p#-}w+K`bGKBo=tH2+=i@N2WDuOGzBrRiWC#
LT8#Jj8G5qIAm6sDFT?daw#nPAVWmzAV0(xS1%0m$u2`Av8OuYD=Hx+1Z%395CX^+6Hc#G5MY>}&(&gAOKFspwT;{l^vc%CzG&oq
4CjTztNBau1hPDcDN{QC-soT@;e{~hHuc5DH>0C|ks?Uum?Afs9OPM$$6@Y8`$rNaakOr;vv8RVj^=DuHM->U7`LshnlN^SRTu2G
k+iYwSHChVwQ4u8C?c7e`j%ahopJo7b_0_F$=S%uFcpNf3~7{PjIchYw`(V~!g)S5G6S*@JQ)~{9WSz(K7}nIi-%U)nyFc|eyXX^
gXu0LTKHwCfovaAE3UaCBv#m2Xu!E+JRH&VAL^4xL7=daM?p<}#G9ql&IY20F#A`S5X^Uch4|!1%<(`iG9#wYog*pYz|={JV86(S
ctX6W&<HsYyg(k9hExb|_QSDIEny+ha4YU(+C!}xSr690kH8mQ^NLr!R)sW&?l6e90Q4DJV~NS6H^jbZy%%zl+fc&+#UUf|8TbJc
8XBWG>J5Qmpg75ZMh%D*CLe2tL^_9!7n*ksXZpZ8c=Y}cy-8Alvy!4fL&Q*~a)q=6C7oFbG_p#UZ@qB3@)4|w)PQKnKp<&{3<R^J
NI;+}x{xVcy^xyR11s)o%0LM@sjX`vGooFhl3W8BGpPnV2d6iEp$C~Z*2@BHW){F@NGvcv4JL1+M`lb?fhd6;5Ly7?dfCOT-+$<I
Yu_&Nf^JA1@cpUx_g8sm<O-0^+Q<+fJkdxHpbB9QD=a&GW+eJT<A#E(Vm1I$ixdEY){V&jM0ybSzkuzA50(5z$RC@ajlyKY{mg+N
e+*1260HE4Mwz#56tkv)gAQ1q!lNhIU54*TlOrr>>RhkB4M&(@=i(8s2c0Qt6*QyuR2arwDY%;i=p7a+%CLYC1XkbkGl1BL!}Hp-
ItvmYA$V4A`f5wfL$1p=LCbCBCG{F)Ck>$yV)s2*0Q|QC!A^qyZOCf<L|#HrebsUjK5#(AV~wMCJJ}_l2%{s82%?)u2y<jBM=2l#
(4F$B8KHl`!^f!^5jkM-i^~!=Ket)G+B;VsPpG`9p^bm&NQB(SFj=R6S3Pe6#uRP|0Yc&c0t1W-&U)3Ahxw~O9Tko6w<2d4Y9nb8
u4*bIv2H;OV}OQAGtPaHU$c}7qTGy<7`KlG=8w6O7<hc!{^^=Tvf+?ZHVW?{dToXzY}9Aha2houHL|;i1g;yb)PVK;d{y0xn%0z}
_{GQ=P=-fry80@VBrq*&ARH~zA_@)K6MT*;3HO>BkvNR;aZ#vmXPNSCstWkcsfrhag{03<<&PLMeJq?iCWB6wag`vM8jQomz*eLN
{*q<3XjeKII;JV|FYmLY)<xKOTJfmB5;V@jQK;1m2Cl}8PsIW()&%ghQ}a|y=buJMc$hI9`RWw+TtoESDzJ5Yc~@2068<dR)+lf%
laHj;Vje_)`3au*EKJ$!EM`c+ml$&+%*&b+-9>?-q{Fij-Gvqj>P}o>%~-BAuHN#tiv1D5RqH2k8-nrGs9$EaUK*<*TVxuMTBv5V
(nl&#>o47{Gfe9b)lUB>E(y}oQLjxfGK<<mKvoG&AQt>zg>TE8LtuS}8zcIhDY~Pu-!QDt5-vel61SS6S0T}I20LpKa6-PrB<sFc
F(b-~JY1!G5@VeYvLUvL9<xjm<jdu@5mBAy4MQ?8aKfj2P{P>Y>Gbt3GiQ}A0=0}NDf_u}KUkQc#yVx`5)&QuzUYhi=Q3gWpWaCL
)2!r67V9-tdCQpA{kJj~x*~7+BVK|%<G5jI&-XP>%q6N5*>p4DXQU+KQ^q&eh-8wsj4y2fr#3oa%jVCQwIUVz(@G>bIhHS`diwq+
Mu|x-Fo#$qzl%86-0A89DcXRe9+AWB!qzVgJoUpZCbxST4+I_=%4h|GMx-B*e4@N2+Gt+(t^t+8XQZ*xwEvO))(s3a)0x7qp-+t;
nk<ANdT0e)y=2Yr5}X7LA-r8|%90FXm%JoIh+?+?u_{7>_xr#-qk;bPPfG7%N<;y9UDgLdK!W}p=J_cti1{sF)Z!34H>VsShMTt$
<Ac74?QMSw75L0y7<$qR3+$#uwf$-~NIez|gQ7V|SPr@8B$S}I5tw7t=bxA(Fn6$h2+NUh9yIZZt{$1}|74r-Hx`|^8x`R%+rovA
jIUh_UC~QaZ3BoI0RO30MA2YIX2gF^?3Dk9_!%6G=$VgGflJV=fAzyvP!J^Z!~nrDa^t7II|{qh9b;jDtB@iTX14uTmM<}|V~cCn
4<a0)uj$+RdX=+|+&}}xl)4p*YY^&Ev>D>^#i;?JE3tJ%wwz&MgORP_^Hi!FZBHv+5tQJSBL)W;8QvDx4~79C)sQKm^Z+pCyIj;b
6oY&<8?b<_E~}C#l;4S^#GoRFJWtTUSAtHh`&`~4qD~+a(WWea<Fvu&pl_?_OS>g`3@-t|2<u&0&(%_-g4wdbst-yKCT#?eXs7@G
gBly`fnQN*n9wZ&L%0YH$UxEc{dIK>5a}DbrCl2zqUJ2}z9mkG3;Fhvwnd@(11<O%te{zpJbnf%7zb$a4I47{1FSDMAqPI$MOFlR
hKF$o^3cXE2YI{29f<Al8fAGj4`IxD@vpB_n?@9euRsSdir|evqPiaK;OkP2iQ06bmKxuK9*(R8385OScVaZ2jzoY=3)fEx#?-No
S~`O-8$E}pi@>vu90&Q7C<IuvAPB6WvlvkE2gm+O#U+sPCRrxU5DF(kI8{kSc!Kbj7l2R+^~OKr=+(v(An|F{uMqjMbn1PH-HMMi
10)bDp%K9>8Ttwf2#7FhWQ2!SK1C{#k2=Uh%maKU*g+t>JxzN~wGfWrmo48Rn&B|@)dKHNvy8X}{D6SP^Lg4ciUKl#$OK*EZ?yr>
?*I{@gti+22*LgLi}HxLgU4s|AyL@1TiHd9!DJIT9M_E^JRtbei6LBHgOr_s0q0(b67ZF0<t#8v&QgU3aYlwv0OxF4weE)YiU$CD
J(j-Marien>9Vq}d!Non`Of=injX+Wcf9x1!*jzCj!#>p<FV)0N#-?>a|}Qz36qKwKsE5?`B@6XmezE*%b*Jd7&zyIFusA+GD3X&
9*YuqYvkAyfR5?jzp^1ZesfOveC`^jH*j84@m70ReIFM|HG_>XI4_Lbn{htG4UjlBaGQqO@o{s;2<5F?a7poKZ_X-Vaz5b2x!7@A
3(_qqKP(3vxi=&FKsU-micGxK7U6n!gK;_g44(4ckn?pM%N%NM2IPTTou=bOrr!KqfhKz;9o>20Ip)Aa*I~>+r#`ukcbM0z=iP&S
(`S_qj#j%Lc!WJ{g;xT$)p7hfA>tv_EFT0XYdFQn5v;G8V2_0VRsi?Hc8n-gj6oBxH?u*2h&j@;IcG;93=nV}qKuQ%TwkrYt^|gh
En{N{OAMdM0_L>Whl<<v$Z|sK)8WwZzzTE&KS~fTXPD?7zw71mRw&b3X+>T4DhI~MC<eN5cv8E~V}t=TV>)hA-e%j#q2zp$)rTUx
_fboLPn6^El&U@Cp^#7<=g+>H%~E`I+?#@}bBhD!@WzfW6NKzWbAg4(I4)^U6_{>Rb2{$H%~7nbq15$F0(O1P4spH>cbo<I50GR-
V6}?63wq#nr17T~!MQMhhV{|u@U$@y=J|aV-Q4ljI^Z+pxE4Oc?b$gZ_COgBe!<Q`nvP$P-+LjI?m)mb;M#HiMUZrye=OrrAa&2;
#8B!Uz~StjX{8k84?``4lX~hOUB4cWMI}RJl<xkK$50#XIPtheU}%w$m5PIof@W7AyNDG(ov)+caf}kb97Kpi4%EW)=G_E%+<Y%a
dPIflS$%3@nobMVoLNvnnZ7<YK(R*rYyRq?aLx?E6St=aT|(Vw2WV?}%Q((AOXA=tV=7a=<uSwJ!1%*JoLTrkOHt^v_?E6O8Yi)c
+9uq=fb?}yQOmJ=0D~RJ(=`!JIJh`}Sm_ZIt_D$`rTq0-yb3=S{V%k#j`xb4!DR)edbj~keV>K-c%;B6JW&FaCw|t=)bTHof!cL1
0czPiTmZN=kN0m3ucS5(Bx*ggL-|e>zT-gRB;;4q_e_A#^WU>;t;-0ASdU@fP3Py#Wh?sA1B61>asBwBHft5W<LSXa%rQ&_&iaS%
czCF879(dfKgkR4jgRy9@60A^%ZbfT1YPofe!xu)kUH_nFe>nRZRU?p#*?5fGf<~U*8v0gH{T;q*6mWyr+${2*FT28YRSzs7uMq3
qCNa9Ji6jO*U&uE2vqLrRpE$eA@%;JM(IOYoGO(u?N;K@q;7z&9nM4g2zTM*;w^YdwjXx~wEwYmld%E8KMtb)L+GtDt>X%zry*M5
0O2ST*D8QV`ab|A#7vb2boqe3jp=)}4bz^5ZW}HQkHKy?Uv~z-ddUT_lr{Yno`RKv@lh~LUG=2US67ACI4bUP4W7&e#{}=6KB&G+
?J;Y3Snwzu1@%+B54>)rK;nAvq$)m#DHL;XIgmu(@i8FNPc5k)1|)*{xd0uU-RxWVwEhDCnOs203hw}iaPefbKKKTjFI;=`UXKTN
<xS?f0(OClbM>S9r(@|elQZiHg%2pEp2AdYeaFS&qhnVk`OHA&5HL&?C~GqBl>YxO__X1nOH6o9{(g=~!ySMwHaIpc^=P$oEEwU}
8S2%c2UPFIEQk7TFA~xGMp@C`_Qk&+V5&4+R(99Qen9nJjv%`Rcm3-TdS|@LX<ZYDf#M$~Gc4RRNLup<3Q(lRAhvcX4H(3i;7=!!
(Id_Jyt<|@EFa6)<IVpD_f$c!chToGcRBN1H1JB{ex5!C+R1A*LM+_vMLuO1Vc>EmI_q|XvmUSE`);Bipmf+*+!AvY-RYHb@N|9m
=P7%-oH}^;t_;$SA?k_il0l~20c!EFK{+|mO{Mb`_LV7VbMk!TGq08ple4*A7@KVGE53-S*?lcbdBqQ3xe2;<CFiX@A+spJX$FQQ
XRnFT0!Y8|TsKT%Xh=37%QZ|X^YPT<^&?NR0MSJ`0gm<0L2$U%_)69cj72(Bk^^C;<8#^gS(!6FIp6qHtOh0`r>(yd+XMR#0K*d!
ni^Vro+<wv59<}2=a(~_2JU+R!f{~TQQL432Q5kJ9hh(&HO7J)oI#hAhj-inrU8J_zUr&4qXD`y*lV6sM?ms(cVu1-1K=DgN7qfS
rQj^F%J9_=%rTz5g#~zhBq$<Oix}qHaL64U1PCi0%}58ZT$BTgiq3FN0;(&_DL}PcB6VOq+48M%60_i-e2pfk<DvRjEj)Y2PFl}X
^v=A?oCfxh$LYl?tf2uQP{!GM8#IlCO1;()YsW+NwHg>ZG>EdzqL}XisJ4)W&$IYA;DLqFT_HHIXn5MSFBmk(pLGEYEEu|~)xdBW
yuJDnh6W3uMsWX)@45GwC$?1i&lFrl%oNV=e~Q~NG!(}_6J?mrz!Cl~V;Yzs-UJYpo%6B-+hYLi8k3{>D28is0D8Tha`NGkeSTiL
mj-D9yp|rgg8&mkAQBH{7I$g6?iH8^)`YMKm_0VY>RvM76s9?>z*&#33L5`jTst5Ysp<3Dv})kQ5FUoLc|TNE1`50Nrt>%a3{WW<
Xy=WtR{ctv!}8JsSqN%6wRa6<*SFgxQZ<J>W}$Y4ejf#$&qL*#K5))(wZZ2;sbmB2Sp#itl>swQscD2DE0646RBqC@t=4M;mXcwh
M{`Aj*7{ig_E0sNHl}L)Kz-&L%t9_v_=mWwFc#gIUsXHCD$f=7X5bDPrSx)k<F}5N$K4v3LUAlZ)IjIBwc0GWVp|t4w=L-CA1Jom
m;kq${NDe)@4D58fjzEbP;DQ(2-7oy-q7Htpsd0?P*VA3df5<{HMkFGqx7*IILask*fqYw%Q{F0bj}`<<4T85e&dNaKz07=iI}^0
JV-Stm|V{A$*|BTC)ohw6dy*BghhHH3^42M)i@oeXb$xePJ;GGn_%doktN-qBCeyj9>+j4u)eJcp(TPgXovi$b~rrH#4e%`a%%;_
A8(bYQ5UyGDfEH~lB9w4Z7~;BL4adG^=sV9QL5iS<zwGa_zu7@>p;=tf(p|^xR1hHl4z}n?-nAe#sLalJ?;X~t{Mh7xUQm-a=D99
+_<$Ls%1QukWlXeMBX8(UoneU8-u<D6F|?Ra@RXG(6fAWs;{sNwaVKthWs2g>H(^~>C8OLz>ljwS@okAivV3g4;|oS8|q5ji%~=M
ehzNOVER+nx_4y!d(=dos6bqD(dw;d5P{c63>3h>x}zfPQ&%>3YH$k@pgz{ln4jy*flOc4GEZIA04$%0&O*aiMRb0Wz(hBpxqkzO
JAWkkOtlk$UwP#ocWktJi{#-pj(Y04ny0D801#?6<;!d)sR12KbCqYS;iGQwp{Jp^=0m>A5pJ&R;o6Ss038D03h8I%Q3G*$9oXdl
4H?ozP2e_<(w?{n#kYmdv+_*6?ZbhfAkfIDTI$==>#T(JR-B$XJ^{Uee)idG>AQ$Ay#oq>sxtLf0%kpl)^ij#czY3-gsA^cggEK_
QwJhHc%u(cKRvgS`q`|{@Hw#~qgeeMdPX>jjo6+#@VG)mZ1Ub1AM0&-MJK}8>qVS3GMU>!K4&ruNs+-MP)w7{xG-dh5PHkFZNyEU
v%Z;XHB<i>uO*&|Y~}usSr~{E?OsfBs|&5Ii45ib5UG7GxzaRasR13SUMODI=9w<UwIu4aa}|n}ES$(fe%xQRpn#tUzr}4OwR=nb
Ywqe4S$3j;OuaJzhqV9osvCw&OS)is@PUHMw+k<J<pa!J@uR6vgy%A)rU@B`3ruVqVZ$9IpX_xW<EHccLkffpl{zZdJQ_U{nZgAv
p7I5_Qc4tB*oIRk;(|+1<WCc^z{}^$`&A5a%JjM6q!+NRte#s=%rBd_NaNOq8#d>y?0(*wyXHCHc>0~|Ph8e(P7{#SZLUDs?gc!X
n^0<Y@aQ?X{RHiQYTR<aNg<E6>jT;o{FYCPBN)^4@)DeGfGco5>(lgJpImBvy<RF976zmjqI_P-Q8wW!uF4%*KN?-;=dVxNUa(3U
cjH!b<CX_Wyb=XLI4IZ>b{AKtRJ&zuEx8_0`L{e}0N4U~-GbL~ABtR#8&Z60az2-&*tgaV7o_;TW{dZuIHImPw0boT3*r_Fco1LS
`civqjcR;|?Q2xy-Z#eeC^j<`Fl*F^D=ffswNor(mH&QugA-Sxu&ryV&aNr7EcgXa-WLkAy}9bGI{2E}5^L5%Om&yFDk!iZeXczz
ztZwrlIOK2@ZYsm9hSLohpSJ_H&~^lE(n>cO!WOPu03(w>Xlr5g0GCjzU(iA+NdMRtbMDFcFQ_iChOD&9NiDAl)Huc7A2BG{d!DF
U!{_*Bdb}rtp0UtN3Y_3ne76A(3j3KZaLW^XQ@l;o~nZY2N;iE`mDIuL;`q)XecpU#q(-mb^CCWi33qN8C+z-K5acNTv6hF?Qhmw
8``Q8+*hL4Z#OYzH>bZ#!f($4Jqpt1ZW;=^Fn5;?zw2}f7m;+|>P_9EE_aTw)Vo*kX%7|Cjo{;o5NE%QOmTAvw75Y$?g)_rc45;l
G}?+AZUbQvx273afpq&YPT|ELPQj~bxZ49QVDB2T*Ryc3ha=x^#?~XwH5}V**rExyc-R1pnwac1@r=7V99Xg4U7GgRi^?S&Y9_mQ
=Pp%wn+3$p8{pDbtL2)Ft<=~mmRy<f72wNb76sR2fDp$F25!i>zI3?`8^^U5Zo;X3I~7~!@(WacuBy<@aC$Ewm2i^<SaUpR!tE9M
^v|q=I@~D%4RPl;^6gBQ<;?2PlxMDo&{ul2ak)DJ1Uajmxo6c-ms`pO?Ah+4oaD-hqOqe<1YljyQLQ-;50@sC;5sEpj_Q5qssxbh
nnS`x2$1zHefHK8T#t`&ZMJOVR_NY43Sbo1vnX6XAg$g}PU%~yct?GtZ-a{lShYJVKzoaOU9YtHIIhnE+*7?H=IPdZM>vF!33HE|
d-c_G#vWX}PrdS%CGkGpX0N$`PcgvZaaF?CMWk1!bvQ8&k9vBAI43?mPi}M1iwHT^-94wRiThY-ZsHbMIT=i=oB}p)@#{4e4%qHG
VJpsaeD$kCrN%!w{^|Qx_D%D2smC4_?9F3$9#vFywpKcGGrQa)fUD}4Le)%kTporq6UwBZItW(juZDs>yW;{j9YJ+q<*UOC^`TnI
Gw0s4#Wln!l8969f8T(zT>
'''
# ---- the ledger (exact rationals).  The table statistics are Tungsten sample means over uniform x (Section 13.3) scaled by STAT_SAFETY
#      (up for costs, down for the yield g); Q3_LOG2 = q3_model of the earlier preregistered studies ----
Q3_LOG2 = -74.08; STAT_SAFETY = Fr(1006, 1000)
PRE_OPS = 1 << 58                                                            # bound on all preprocessing operations (Section 8.2)
SLACK = Fr(1, 1024)                                                          # cap slack
NVAR = 12103680; P6 = Fr(287309824, 1 << 32); R16F = Fr(1052672, 1 << 32)
HMIN = 16
def load_hist():
    """HIST_Z: the pooled Tungsten histogram of fibre sizes (zlib + base85 of the text 'NX n' then 'size count' lines, sizes >= HMIN; the text itself is in proof.md A.11)"""
    import base64, zlib
    nx = 0; hist = []
    for ln in zlib.decompress(base64.b85decode(HIST_Z.replace('\n', ''))).decode().strip().splitlines():
        p = ln.split()
        if p[0] == 'NX': nx = int(p[1])
        else: hist.append((int(p[0]), int(p[1])))
    return nx, hist
def table_stats(theta=THETA):
    """per first block, means over uniform x of the kept fibres, kept variants and four-groups (fibres of at least theta variants)"""
    nx, hist = load_hist(); assert theta >= HMIN
    return (Fr(sum(c for s, c in hist if s >= theta), nx), Fr(sum(s * c for s, c in hist if s >= theta), nx), Fr(sum(((s + 3) // 4) * c for s, c in hist if s >= theta), nx),
            Fr(sum(seg_ops(s) * c for s, c in hist if s >= theta), nx))
def ledger(q3_log2=Q3_LOG2, show=True, ac_log2=60, slack=SLACK, safety=STAT_SAFETY, theta=THETA, pre_ops=PRE_OPS):
    C = 2644; VC = 1
    Fm, Vm, GRm, SOm = table_stats(theta)
    g = P6 * Vm / safety                                                     # yield: expected good pairs per first block (lower bound)
    F, GR, SO = Fm * safety, GRm * safety, SOm * safety                       # cost: kept fibres, four-groups and segment operations (upper bounds)
    chunk256 = chunk_fixed_ops(256)
    batch_cost = W6_OPS + 1 + BATCH_OVH + chunk256                           # every batch charged as a full batch with its lane mask
    c3b_pair = 201 + RECOMP + VC + RARE_LOOKUP; c3b_row = ROWCOMP + ROWCHECK + 1; c3b_l = 2 + 6 + 2 * c3b_row
    w6_part = (F / 256 + 1) * batch_cost                                     # ceil(F/256) <= F/256 + 1 batches
    seg_part = P6 * F * (SCAN_LANE + SEG_OVH)
    grp_part = P6 * SO
    rare = 4 * P6 * GR * R16F * (c3b_pair + c3b_l + 19 * Fr(1, 512) * c3b_row)    # every probed lane (padding lanes repeat a member) may hit
    vbar = w6_part + seg_part + grp_part + rare
    fixed = FBFIX
    fl = math.floor(q3_log2); q3ex = Fr(2) ** fl * Fr(math.floor(2 ** (q3_log2 - fl) * 2 ** 40), 2 ** 40)
    vmax_fb = NVAR * (GROUP_FULL + SCAN_LANE + SEG_OVH + 2 + Fr(11, 10) * (c3b_pair + 32 * (c3b_l + 19 * c3b_row))) + 2 * (batch_cost + 2 * ZPLANE_OPS) + 200
    getcontext().prec = 60
    def mu_req(pcap):
        x = Decimal('0.61') - Decimal(pcap.numerator) / Decimal(pcap.denominator) - Decimal(2) ** -60
        d = Decimal(1) - (Decimal(-10.4) * Decimal(2).ln()).exp()
        mu = -x.ln() / d
        return Fr(int(math.floor(mu * 10 ** 8)) + 1, 10 ** 8)
    pcap = Fr(1, 1 << 24)
    for _ in range(6):
        XREQ = mu_req(pcap); nfb = int(-(-XREQ // (g * 32 * q3ex)))
        pcap = Fr(vmax_fb) / (slack * slack * nfb * vbar)                    # Chebyshev, deviation slack N_FB vbar
    assert XREQ >= mu_req(pcap)
    VMAX = math.ceil((1 + slack) * nfb * vbar)
    T = Fr(2 ** ac_log2 + 2 ** 50 + 2 ** 40) + nfb + Fr(nfb * fixed + VMAX + math.ceil(vmax_fb) + pre_ops + 1600, C) + 6
    tl = math.ceil(math.log2(T) * 1e5) / 1e5; p5 = int(round(tl * 100000))
    out = dict(theta=theta, kept_fibres=float(Fm), kept_variants=float(Vm), kept_groups=float(GRm), g=float(g), vbar=float(vbar), fixed=fixed, mu_req=float(XREQ), nfb=nfb,
               log2_nfb=math.log2(nfb), VMAX=VMAX, vmax_fb=float(vmax_fb), pcap_log2=math.log2(float(pcap)), time_log2=tl, log2_T=math.log2(T), T_num=T.numerator, T_den=T.denominator,
               tight_up=T.numerator ** 100000 <= (2 ** p5) * T.denominator ** 100000, tight_down=T.numerator ** 100000 > (2 ** (p5 - 1)) * T.denominator ** 100000,
               success_lower_bound=1 - math.exp(-(1 - 2.0 ** -10.4) * float(XREQ)) - float(pcap) - 2.0 ** -60,
               w6_part=float(w6_part), seg_part=float(seg_part), grp_part=float(grp_part), rare_part=float(rare),
               per_fb_units=float(1 + Fr(fixed, C) + vbar / C), preprocessing_log2=math.log2(2 ** ac_log2 + 2 ** 50 + 2 ** 40 + Fr(pre_ops, C)), slack=str(slack))
    assert out['tight_up'] and out['tight_down'] and out['success_lower_bound'] > 0.39
    if show:
        for k, v in out.items(): print('%-18s %s' % (k, v))
    return out
def selftest():
    import random
    rr = random.Random(1); env = Env(); bad = 0
    for _ in range(20000):
        w = draw_F7(Shake(str(rr.random()))); bad += not F7(w)
    print('F7 sampler violations', bad)
    tot = bad = ps = nfib = 0
    for c in (0, 17, 40, 77, 111, 150, 200, 221):
        for _ in range(2):
            w = draw_F7(Shake(str(rr.random()))); x = (C7S[c] - w) & M32; am2 = rr.getrandbits(32); cbv = (C6 - am2) & M32
            for th in (1, 8):
                en = XRec(x, None, th); z = [ONE if (cbv >> j) & 1 else 0 for j in range(32)]; good = set(); nfib += en.nf
                for b, (dl, nl) in enumerate(en.batches):
                    plane, ops = w6_batch(dl, z, nl)
                    for L in range(nl):
                        e = F6((cbv + en.vals[256 * b + L]) & M32); tot += 1; bad += e != bool((plane >> L) & 1)
                        if (plane >> L) & 1: good.update(en.members[256 * b + L])
                cnt = {}
                for cc in passing_classes(x):
                    for a in cdata(cc): ph = phi(a, x); cnt[ph] = cnt.get(ph, 0) + 1
                want = {a for cc in passing_classes(x) for a in cdata(cc) if cnt[phi(a, x)] >= th and F6(w6of(a, x, am2))}
                ps += len(want); bad += good != want
                for mem_, (s_, e_, cost_) in zip(en.members, en.fib): bad += cost_ != SCAN_LANE + SEG_OVH + seg_ops(len(mem_)) or e_ - s_ != (len(mem_) + 3) // 4
    print('fibres %d, fibre lanes %d, good pairs %d, mismatches %d' % (nfib, tot, ps, bad))
    # all 782,800 embedded variants: the lane-safety bound
    mx = max(S0(a) for c in range(NCLS) for a in cdata(c)); print('max S0 over the embedded variants %#x (G: 0xffffff58)' % mx, mx <= 0xffffff58)
    bad = tot = 0; ext = [0, 1, M32, M32 - 1, 1 << 31, (1 << 31) - 1]
    allm = [a for c in range(0, NCLS, 7) for a in cdata(c)]
    for _ in range(300):
        cv = [rr.choice(ext) if rr.random() < 0.3 else rr.getrandbits(32) for _ in range(8)]; pre = cv_pre(Mach(), cv)
        for g in range(5):
            chunk = [rr.choice(allm) for _ in range(4)]; U = packed_u(chunk, pre)
            for k, a0 in enumerate(chunk):
                Ar = {-1: cv[0], -2: cv[1], -3: cv[2], -4: cv[3], 0: a0}; Er = {-1: cv[4], -2: cv[5], -3: cv[6], -4: cv[7]}
                Er[0] = (Ar[0] + Ar[-4] - S0(Ar[-1]) - MAJ(Ar[-1], Ar[-2], Ar[-3])) & M32
                W0 = (Er[0] - Ar[-4] - Er[-4] - S1(Er[-1]) - CH(Er[-1], Er[-2], Er[-3]) - K[0]) & M32
                Ar[1] = A1; Er[1] = (A1 + Ar[-3] - S0(a0) - MAJ(a0, Ar[-1], Ar[-2])) & M32
                W1 = (Er[1] - Ar[-3] - Er[-3] - S1(Er[0]) - CH(Er[0], Er[-1], Er[-2]) - K[1]) & M32
                tot += 1; bad += ((U >> (64 * k)) & M64) % (1 << 32) != 0 and False; bad += (((U >> (64 * k)) & M64) - RBASE) % (1 << 32) != ((W0 + s0(W1)) & M32)
    print('packed u: lanes %d mismatches %d' % (tot, bad))
    bad = 0
    for _ in range(2000):
        U = rr.getrandbits(256)
        for k in range(4): u, o = mask_lookup(U, k); bad += u != ((U >> (64 * k)) & M64 if k < 3 else U >> 192) or o != PROBE_OPS[k]
    print('mask_lookup mismatches', bad)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'ledger': ledger()
    elif len(sys.argv) > 1 and sys.argv[1] == 'selftest': selftest()
    else: sys.stdout.write(json.dumps(run_request(json.loads(sys.stdin.read())), separators=(',', ':')))
