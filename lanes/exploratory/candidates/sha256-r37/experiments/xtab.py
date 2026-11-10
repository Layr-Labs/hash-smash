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
c-k$T$${iL4h8RJMVcV)q!a%<{#!B;58a0XQ{oC@2h{)l?{`1{{k8qObG`F@^Zm8+o8SJ<{cHEvcAxj$_SfETd}plt*T3I5-`IDI
zuta*zqR}K*E_>5UG`rezka?p={tY@>vw$LSbu#vux&c*-+rS{hn?R#{cH5SzrAK}{iFSUEX#a<<NLMQ=KH?&H`;HuuhVz*-~L8x
{`ng$w_7^TU;F0G!}Xiz_VxXZ{cG<&p6<WFYWKeWH|~$aOj{i6vXlKcIoRlTjj#PpmO69skd^jnot|^JYqme<Z+)8y@84X%J-cg9
&UEiu<8QLan!W^ogH3E!|C<j~w72Hp`hIt__3v-B-<tdKsQ>Q!PT%Wq4Mw-aOAgcfn4o#B-}x3ZuKin#TxY+(b$;*c)&JJ@)O|S*
hnXA1Z_u`x=Ca;qmD>i5{(En{_Wt$&Cu4UyPVRNSd%sBsPO~$Fbq?rhfBUeD!RhyPJB`PGTa;Z8aXwdG-=*1p?cU!1PUphr06{!t
nUACXot&lh_IK8gYvXGF&i)<Faqr&&VY3g$Ug&V2xBd>;YM$tR-X5oCuNP{2y?uX|HQG54>jhii*Z=PPF>Wq4aF<wr`|oZ^r_J+s
A?dLkcz>K4YGShYyOPrTa!HT3k4uLD=HKhTv-eu>?+pl%J^ejNYjB3Y$Nc^6{`a`?)!*DO#p4L@!QW#65co0j{Te5Mi@xu7Sn(S)
+i$e9X>bC_W-XcnvIF^G5?X=*HVpZ(2qfR^$}vDYQ?`#QAJ^Ah2H5P~>EV@+J8SK8&Ii4;#+7?3boxOU<9qO5YhH(#0V!<m>^xk*
d%D9}=X+ci%#IA`Y|p0`;#u8}9B4F0cdz~J+a^mP0(jsA-CLPlE=^hGv+IQ9K6s8MM9l7K>>sSxAmIl0vp2_jAXt01<(v;X<ZhbW
KlsbD;pOL9hX*b_X?mckq=NJNT8c6lf2`M-6UJwYUEu}akKu9TdobE*ahwHTA~-<m8;}W`|7{tZQTBiA5T;*EG{f|8>b-73uHRw;
rtfUPe)7q;SwgP=AZ*rv=jZe~VfhY{JTg2#j{V^Ic@QH$Q(#W}fvz63!tyuQ3(Frwl9aN<R%cl_eynT&hM!La!0_}xbf?{v0yes2
aM%e9zrCX^8GlMM#Dmv$l>Q(pw*a$e8}Rx#gX4e`n7t3L4QB6$6=*?S!`b9@It;qW>T+0v)se8nw}{|3SqV;8k9--+88-ZcXaZr&
)!=o7VUyMQGvG1qH&jIfR{Vy9DyxrZrTGJ?N0x!t*_;iJAUijB9n?A<!USEy-e7g~18d6b2boH%{Vuwp!Rd_Zce^OezMWNG=U6`B
7P4D-9l;RZ39GX+S-mL*8?25xL@|EoC(bl!w%=3H!RK=x6s26=kxr0{g5(`Lt)GMnp1GXWXdI=U!>+{sp*m=@`^!Mtdu;?gO=f?>
Ubl&EmAAQc8dG@|-K-4ZTHz{G%9$Af`m-i{4TsrFw*J)LP!ROPIb>-REe#Y#KRy{MD&SOg!C8+syH`N<uAD{n(Lz4Cpxiv(gf6<8
+!IBQOATE{mKM88{7hJnCJgX>cAM_c?ZC&}G;71gF!5)vqtx;d^S`6@02iZcu`@tDTyjM#T-=mX*cV`I!o?jfe%DuuqutmAEZmgN
eePT~TZM(62#0|e!fp8oB{5iLDTlg~%f8<AQm`UQm|TsWPM8G;dP5K~_p_5!Gf<@6ZlK<kqpr84ptg4NDr?lGonT$qm&ssVBoQ<L
=VrmJgd2(ktORz&c=%Ss#9^^(fLD369S_?&H(a}zhg}^752KE<4bIT^8viy5(`v=gKzgD#IxM@u5lDw&yA%z-f>|3XHn#}BPPXQS
z^+3Yg<J1zjJlFL^T4anoEwo<RekUpLPnN=Q@4x5sF3emUN)@Sy*fEHS`9Wp{;?XIipY{;WmD&tO<#!rY3$i|E0_=){l%;VUg^W(
ObkOp>56@224-H^9gzx(xDV6}BxfJBBb0*`sUAj3(%4$0+M`EO06H^tLQ5LtN%Zg0q-?DwYF^?+`O{QY(HZs}lJ$T)hsPK#M1uOk
GSGAaYMi2mhekJ;=17P+DAi6~BZXmI*`5bO)d|#+!_cL*emNkF`Ow@Du96$bmOn3Zbgg+{^lQcpZxFz&Ui%o4SHLNAvyA-M?IF=&
VtPIpQj`oO;j)he&GQ+f4PqbK(O1J<i%P>CPSnC0+R!~%SDA`X8S$lYR2M)*6x_qSuwgC%HpJq!q2Wvyb*S>lCTM`XU??pxP7p5i
g?47wBhW5q3osxiJy08y->}~T_sEH%=G?jrUFiVo;6A++R2K3j^Q$(!Hkc2^#57vS5Z};1hUUCm4P=jY;!!ZoiJ=da)UrZMV<8Lz
anS$`;ttLO>Fzh2=PdX4FqddNmc(_zU{TBt?O|ut9M+T>R{{p;pXl?jvevMNzOf=fi~2ExVnVuGc+P{puiOY)s28S}<50q0<I_N)
D=c>$^8VrW#s0arkZuB<IFJIn9kw!MH(3AbU1^g7^bb%L^OF*M4hHbfXe@*nZkDXZb<jA9X5i(PHx!LsjeNm5lZoviqd_WYUDWLK
!H^=6Qwl8>fy<8XF%R$+(^V-CPzrZ@=rZBvd3rQI?i(ED7|mHEBn>v&^#rv$)S@6s=>(KyU9W3&*agnjVME}D8fVm=hl9Vipi3;*
L%?BEFg0rqjip8gZrx<v%@PMwZKq<JDm$L*r=s9^pr&&lD!RE@7VdItnTw;-KvOWKzA4TOmPnMs)I`-P7a#DJ*Ro=KAx|LlpVtCw
;gK>3#^M@*ajtQVVJvmU)ESLkHQ_8b3S)62KrWx3@YPe=z@gkUfJ?#_qoFnisL`<3*{6=Dw*XTisePb1&F)laTKlxLQ|O}4d72IH
UMTfzTBB65t}K;xj&3tR(*Il$j%wluj#Bhs&*khIo|sw3qukK`l%=L!Zb{b(Prc=ASC1dSr0^RJ=LB2@L}t@o!`)YA<IhhO7?0s5
*7Ub7C17ftfNyw7={%pr^qS=KP7d;<QO_O&^Ka=$x(ApWN(6w=;ZJ2XfGsvntOX}+fkv_MhV#p)tI$6*a%`-1jps*0=>*WR!so<H
U#hEZAC-!*X4I0zGo}G03D79d8D69rb~l6|C#<dy0_X;am{2CN19yWNLj#qa4&1m4X*&872D-RUw4Cy9$w1BBjoPF}qv~SC_hX?E
uNkQH0BjvR!zgkOKv&7`IvIZ}F`kT{EhkVhJ%5g<7>swQUndAPm>uilX=HF$Kl{g6;Xv{Yzu_D356mrN2XKkoJ6IzagKLzWYef)Y
Fo0L1JS$g>KGLdkU|sRfaj#QF7Xf-~8`Q?n_zyBjx?FIKo80=+T)>X_#T;Q)blZ|!_<iDcvOSrF?(j<Nymd0$QJixYIAoTDU8gP<
4nepBpZ(N0%B%%<@G#+*{8WSkxPsxGscfDP)QtwFn2f)Yv2?v)4Woh!-q4o8P3QE0t`%ZP3*Hc^su_`|nsFZ04El*i?f|~P_yjuL
AHE}lj3Dv{>;j+>H1m#z0Za{VpKHwdfJ;CFZS{+fbJpeqV*=mbR==PqX*4D7Hi~kcv1yD0W`x3S31$JkRimU^zF-CT;$~p&5VkmI
Wg0Lpe=!S@db@Z6U+5>>;ey}=X1Gids96uVx~&d;+3?WW@gO6&x>YJ@;X!LCd$vZ~wPQ`EMxiear7EC!VjBW60;nDTWTp*M_&}0-
z~OFZD45NuO#H1l_3g>qtJlcVGkSEx4@fv*E7WMA;o9yM8MS2xF$_ESQX#rTg|?ZG<M#sVpm4*%)}#TU@K@dkj39N#{AVdGGRDdZ
Pk20ooN#<80dJKC6thne$WbamCcYW<!~i9e9+}>b-Y6u!j}*t<8U+JJ18?{N6=b6>AVCVc-MY}L3F@}>c?3J&(Joc7<%juYcwK<(
fWF!<r+h|f!2!H5e3{TGaMe#p;|yu#<(%pW4<IiLBeLMXgP!wwm2jc9BTyR#fOJE)KUxVe0yXCcFr;w|JhbgV{iVO7jzEQ+78QPE
1T-ZLHpl3e`G6~<b!C=sBaJWse@3(qT)-4sSXjpW(Da}u9t?wfnCci?0DDK{ilw?i3*Vj$7H3|;>0am=?#lpkPC2wJxUFLt5X2sx
6~z4+2{odj&Iqp`N#7mJ1QwZ26N&+nywPdh6aLCSI3~1K_9o4vWKMLzk>;VMV;~=&?m*)lo!(M+^M%eLcZ9Zfdr<ZB=?f0GaWqI1
f5?+<BTz!^K%Xvcsbd75orH|BTbLY5X6;CHW<D*yx;Yb|;{3#y@Le?5iB!*9c@z+)I#-S5nQv}EVeSz%bQq+=jvEguAYR5oyE;k7
$T^DS+@N3M1{yuD<*s7eprp<V`XE{C=p)54qZEs5Kd&fEk9-Tk#^3$4L6Gyb!b%r{<p|eUxUu}tP25kqy1<h$pfkTR0~Go&pKnML
%-t4Ab1M!8T<I0}C$BSyE;g&hZuz^0z90sU4N|X$KPJjmE@NfVK=AQ*tEz#L;x_f*D1g^^mBHvAgxDPk9|9Ffb}*O@Fg5UZV}YpA
uR&&BOLFv{@h*TXy)`>L)~vxZ@p0trHIxk3z;>R)#1W);^?D(ayJ8kx15e+v_l@~+r9CE(KovGA<Qg9~Pa^ePGeQ03t@;9>ZQ^X9
yqic8$38j+EOnw?aZEDD3D;ib=9kA@vx%2NFf_Mw%Qwin(!9ThByqJLP*?Zns<f<~Q89^cN<)&n3Q1;)jJ$?zH%NHynTaA5x1liD
E*%^UkVKva0tPz`SAX$97ci?o{ZAu197@7@5*v*8LTpdtAf1(A@1Hn)O+tBwUpv~ER+#7Mb}|x@LkPWC1wMsd?VTA6<!Ii$m;z5)
dw>}Of=1-cgVs>zuSaM-GozpO!yBH27eiu)*50TyMB%eb6+VBrI{DC0cD`Yx3J_dCewEJ333MC>?`G{E8pI*+_fna^sQL!XJV|VL
pqZ0Ei1t~z3LEah^jO&bg#?8sQ|lXYP=(+3lpSw};h**`qa*%U*_fut+gVZ)gu!UUo_!}#WMGXooPx1|=awapeEKB8(T<OEgD3p@
_f*<wws%z-FDe_LiSw?U?hG2PY{JMSf6Wzv#T&#$<S`J^14YXx<{Sar{2Q<?3(9l<PaL6P^;WN$KaJ8R#6%Os=(FLK0X+AyVbVSM
kS`9JQ1xb~A~T@TC}E9l?%KIkxMl>qp0^{TXaQZ96PWlAFb2CJd)hnp1&vdE^|+IkG=(foz{c66vcOt4iFLOuf!T8=hLXXv7M8y3
p+emzCcjx@p{(JKjkTNH`ShdAJbp?vF=yC8FpU)e<8No9D}ogGg2{yM><T3vr_wN->A7n$Lv`t3blgoOl_hLh!w5oO_B{Vis5Hx)
(tb3~zX$ghRG6PO4GW?TK$)s36yH%;yQPb1M4khUO$%emoFr~P1rD%~rQx^C@<LbvE9Wz)ZFcI5OfwN1qDmw3yO}vQg>5S*PR@9w
Ase;ii(S$ju^B(}!bv2X2{uJn*<T6NjBi$nylP4IZVfXN&h?}R|K@h}gqsQ7JddB}F3L}7rf)rvx!e3ya|m@}h3@imhH^|=i+N^x
+MMjMQ3Pc6RXetsajgg3rMGU5)e%Y~pD$5zlKR#fbDwL~<dTrLoAjx3tvcaWBj-fB_G$DtKMkX$5j(z_D3z^RY9TV`DQ(<Lg^o-v
3FU$EPby2Mvx!ltrRTnGAyPFMsM)w3e2eZ(XZCb7s^kuC^k_4KDgBwZG{0dO@R!{DPISJtS0bR5{4pgd51DmO$$?P6$=v%_r!m=x
`EMhrG|_khTm9@&0xg-vC0zBKTQ_do%q2GO*%ab#X>={lX1;KHZOIW@4gifP222M&=Nh$!`s}7&Ao&KNCSNKELcyl|99NkIN0x*!
$7deb%$~JN$?N5}oGU!l%^2#G$Ia#Slp~ZtHf@(ugcUE@hSI;8r&E;ms4V4i-?ijF@-Q=(pNTcQRqZDCx^Kj@xi?9|jN7ehhgqA7
qG~4D492t`6=e~GqD)h$^&$}yY5}7_^puUA32q(k8gzHT_x-AT!dfh0h@*!%PF^Shg}Lb@!?2l}DKN>(%$LH~v{$Mxc5Zyc6l$it
!tkRAB?&KoYI=WW$<1zAiDGig@vW43Go$4)$`UK2n%OJ+nX__+9+Dcp$bQ7<Yv!v`Z(zF0-{Y&^%8?_S^>~*kFb^fenSN3jCix`j
wW%4+Yvze{PoC`RP*TVAQWTnLrLocg;Q|9j9>~;Do)-dkvKua?7bm79hD=>Si8f--2w^hs$efS^PH1VQS}KhhqB8wsg22|T8I&4U
LL|*2?m`9jxbYENQaP^i{@sV}*v=aRX@V8*OS;B^@8+7#&Ri9VxtLVKXjgnTwx}}kqJd(03wJF^nQ0N%$*?rxP8_!-p(0cU1m=Kd
QBpnQO-s77uDVhu!W&Co^GjNtsqPV$@HQKgf*kHPML3#7CbZg&1>4MhD8<Zqw9Ke!;R>m~^T8@Z#>9pjGeo=dd}b%BZpw5<3i*sP
L{gf-P}C%GAxLzmnYU<`PBhaMRt@d2hq(&<3Z29JK1r$AFixMD{@E8vNhngxM0nb02D{#W=<<#wtfU(R38gr~OZLV4cM)YQm_10j
(hHtU74#}RO2n&~D`<j5F4M{tn-q}6Oa_d=ZW6&p=3OQ14gB}~ys>6h83z^bcNwo)Fk^xl#+T)c-fK%3wJ#WcN|1i7>`!;t4XfyV
6-&{n6ySoJV;X1oP7+`@)YFWtx4^pZgwidSvZFf2$az4VvSz4!2L_dn<bp(jUW8jXk(LI-<=|CUW9&O*WYl}OV>3ZHvyQ6ZN(9EV
vq3ep(<Btq3}xF%&eP^uuejQvHM(lqiVN5bQ}?`yY~SHM>#tf(Y!F(;O7Pi!5w1?qvQdM~^GhRlVOV+9@0#%6o$O+?1dVqp$GDV$
5QH(})QjB+G=syn%B)#a`zp-gccnvY#27dHEADp+T7|)>f!>irs7&32Iy9AMGy2@A)SiN}?hV;G;3Vd2#b~s(fmv^1pW0?!k^$M>
M_Ofm8FQ8H4YsEKO~Xmhe>w9D?;A~(Xl>o79^<D{iGkB4h+s5s8t*LOQo%oy&iJVM%)n@Sd9Y(oC)$|_d!6(o^CjH5<`YXu+sIg^
Q<N!WEVBjfGW`r$`di7TBu=PO@K4?un-oJvCFL=rl37?z@ea-k3mcTomRFfz#vxNwdLqwKrWbX1cI=;o9$lY{@Z_f)9D|IG)^_Qs
=d11A60(L9?PUnuxo$$A%?M#1hPB%%j!0Nga0=Xd7|D6Rs-&?Mv30-F1_lC$z>JL@)k=aMgDWvV!49Px<V!_hFDZ13F%s7^Qqc_Q
Ib9D2-^7%K#gMnmiyKQ+7z@<+T?#&L-GgzvmgkyQuBP$egH@DhNG{WY{}*j*P%ba(u(E^~W;8B9@5lv;Aq>Nf{H*S36+t35K0kHn
^KY5+Z@ZCO4oH}{8Dx`E4X?RvJqyL6akU`l{X2EpjEShtyubc_aU_HhstKCC{LXZS$?}na!s-Z1SQ-(NED{UL@0;#M!Fq~B69E&H
ls58Z|6XdzfLA~d4l2H7<$9v^?G<k%sO8|9h)jDWoD5j`bcOX3s2X`)Ldgi#3e0u9q+Wf!OTfOuzcHwmGnD1_l0y{+@2{#0EC>B!
xx9a7nn9&`Q#*R=(67#-2yz+gN39wCbpCAcTp(tJBDNb2@~I|vpo{h|p~Y!8GmVy+MoCzQ?c|mkXLK@$7N5HH{#ByT#?0%8{BGPP
MRQ*a=ANjHAPPy#K1&#?!L9PmibdVOQoa2P2D_0MJML6A*w{JYuD2&{Q%{UV0QN0(73<S(w^qINS`S!o<5qWLB~B@oIxHo+LJNDW
jnyi$n)S=c41gR#jMCl`sf9p$D+C(ua9GH(S3$eKrNY3SUZT$$(bS>)Ah9rEt)gfU&hH;oX>@}XhSa*j3imW?6-^j{{McIxNQK&2
R{d&ETl}wBPb-3@w@77^a=&clM4xoy45{bUUyyzhX0WdJ%bNG!B^XNZZCu4}K*3H1GX;J|BdobnJ}C@kCU($-u}OO`A>54@EQ!s?
KuUZq5)tfQYJ}tE31{x67cx^6oKj+g{|*~jRZm}>rl{8n<M@bag%5jt_tYC}xb*n#g7Pi9e!8pgdaENQsJZpTojZl<DNqhA_rg_=
(sFRLR*!$}uv<IUuXgmSw@GAK$;{<*eYUc+ez4D5VpTm}Z?n9a9ib_#+;nTB@GwGDHp-pty0ZcDwEYSZda<sqziO52h(1qaWVw`*
2&=n<lWOUrkFkqGQkIxuiJc20XLK|zs~yqb-P%H5Mr#PCdb{gdx`v@iLC9V=a#(U5)@`<Oz!~F6A1V?ouA-n=R0lCN*+m_32z?z1
-}U>3vSg-!$4YG_S{lhFcKx}X!tL-++&Dqx#4OQMC1uua@7l^vq_69Nb?2yikGu7yQIp)-e=PYP4@*!Cn!2o+;_(<MJ-(G7$J3*-
(z{4O_i0$`T`Zy7WIed1`AE@tk@PB3&`mOH*L8^Ud`8OY1W5^Tek><1;UAC3qH^fQ7+BZC3HbNCgx!jT(Bsw!Qm<>-c~GSLlG5{T
QmX5iIQ5H&(kp3!3H9~;Pk!oqSc+a!Q-{Oq^B%HK`HJ5I>{wG>Kf}lIFN9goQWPf|xvqE>@=AFXmJ?@8v39%#XDZ5$&*0B(Fr(`c
Waz2oP7S@el%054j~5WAd(u-5UnkH_wkZA!O=;IFLt@WcAs;ujYs6a=-zz-Uwbk9hDOyccfwl58YgV;@rSmHOG;$v&i3wqHk^R)Y
Xep<h-f{<jzgW&aCbA%&c8?8=|JOBkWz<`DpmDqXvLsfmAhesTv}N}_l%vsV&3&RK{mzo)WwQ2|tbxTHrj(s&)!S7{?Up1>T38SQ
(d<m+eh_rSNAlY(0jiOys7~(I$Axum%GCDPy=qGa#5VLhmtX4qiy~txTJE3ZNY@fHvfZ@-0}{3F+I&h;ZNBA^wf20!BHmuS8)49+
5vRFSHe7%4A{~9BHD0MjO*40(QQ?;YiGz=%>I8mI<W~dYWoU^7>;j@^XofkmtgxZI72qC*)>eMqOegU?q2{F@8t72@oxzvRyB1Y|
`OSe5Bul`*RC<grT7HzxG|FZgrke6DOgp}KSVPmuPiH-ah4)GQ2(o`oA9U1+<s-=ETB<CCyQ;@qk<4fnOB*d=7{6UeG-_y_Y*#tn
rJpzk-1>E8+@bB^5)rQ>UtamGLO#gIcMZy`kt~BC-s*@kA&B4{z4jLy!k-Z*Lz}^3eJuqm*?VYU<hvSybUk{^dK;%6pWLGsfkSGm
s`?>_ZXG=me<Um}*!k6B;EyQskyg0Pk2upU=H3`3wTFs%Teh#p^>+mDP_r(-nCOW)k7(0;I+627iTe3O_M;9J%`-ed)SV(HO4Cm%
B<hiXr=L^g@F~|8$SyWc)Y&lfm~Sg$vW{8XP}%uKM0t5*RV-?(*8f3e?Wk~{Feh9wT*itR9IMQ=u_8vsD&$A~2#Zoz1aqbg%Z(MO
H&jE-FENrqwviQfEUU4L<)VIs5qVbex~bGB3W@@Et(yRoAXwOS*Qx6BLyedq)}rO9X0P9BWJ8JMjC?Atlj@6}IZ}d#mpM-HaZ1Pp
W$X{dzi$(N6b8=<f9G)J>!%!r_7godP9Z_jFX}1^G9vl~3FwT}F8Ps1(0nV7G)mwP1wE2>M8sP^<i|x$tr*W|A5#oQZrlAP^F0*M
ehX5(7;j!eeuef|R9BLCyju7b8kE1jE3CgnX~!$ld(q!R*=v_wT@+!{-zBA9bi!1+`iV!#eSRVA`Sto$T5KvCkKcvVi2V<EqM2mA
pN8ZvXM~>Lhgb;YM;!UWTA;}~^KG=C9`^dB`Q;}glEF-7*)K)RVfvX!eA}5!tDlF&yq=Luej76XeIt@(<Fp9s*NQba<9+x|h+<*J
oA84Wu`(4Re$mmRrsk;p=p0dUGrqv^+mP&jR87Q;$uG#h$1ZS#j}Z=@Wt-0tN}384Klk|RmkydgHNE{v#Cx5wtNl`B=U1F}zZ3~l
6cZyKjMNNK<a5=ft$cnel!4|7oy--=m?@O^TanD8H1JcB*le@R%HtOxUvkTHhgxS$JwN`4i8sTjg5+anYG3^TB-@u!w_kr`XD6Sf
`N>D{8h-P`4uf@m&5=E69W6iQ$h5Z-1M}8VZ%l!CBM|3})$dmuw_r5Qd=c^U)kVDM>X`_UA8k~Zm!gcNy&#Bzu)YcrEY-Xf_bpDu
idOc^i!UXIt0f|{5*+aB3Rhb_Zotz2%@-119!8C<QPYoAKxKCQm?1yC;o~O@?r*JlX=}x7U-1^)krLR?3z9MNtAm}NBfkCGA(E9i
zh4{7yu9@=484?i*N+KO@!;11+5D}MF(>^rAV^w?Tlz^rz0@Sg2LQ7FDlxJWsk5yA3yAL7U#@U}8MrINGOVokE_V;IcWM<ZsCT!!
f&jb65!$1sn>B%6ofYx%$ONvuLzvc?=VAPiREz6yS@oT@5+6>LcRDL9t;R07f3$>B;%rT_)ynSvL}ND_!OEEx?m5L~NA}p(3A^su
DFd*6H+|Iu)(yWB3jUWZKSAW+O$;aXr*^)I3QJQX9dA;_g8Wh%SWy}Uar4!aRi9sqJ3~&loRE8?T3?SJ^rSfdCyX%m8<FlWCV~}s
37&qD!&ab0Ra;?}q()Uoq%7wvn7eJQ7_=qEk`#RKqMx0Z?JN~!rjY0V2hr#|m;
'''
# ---- the ledger (exact rationals).  The table statistics are Tungsten sample means over uniform x (Section 13.3) scaled by STAT_SAFETY
#      (up for costs, down for the yield g); Q3_LOG2 = q3_model of the earlier preregistered studies ----
Q3_LOG2 = -74.08; STAT_SAFETY = Fr(101, 100)
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
