#!/usr/bin/env python3
# xtab.py - sha256-r37: the A0-variant attack on 37-step SHA-256 (ePrint 2026/1120 two-block attack, 222 classes of A0-variants) with an
# x-indexed precomputed table.  Standard library only.  The 32-bit value x = A_{-1} of the chaining value takes only 2^32 values while the
# run draws about 2^58 first blocks, so everything that depends on x alone (the W7 class test, the values W6x - cb of the variants of each
# passing class, their partition into fibres of equal value, and the member lists) is computed once for all x (charged preprocessing, memory
# reported only) and read online.  Online, one first block costs one compression, one table read and, for a passing class, one 32-bit
# bit-sliced addition of the scalar cb over the fibre values of 256 lanes, the F6 test, and the packed row-16 stage of the earlier filings.
# Definitions, constants, the characteristic tables, the variant family G, the classes, the packed good-pair arithmetic, the presence word and the
# rows 16..36 check are those of the earlier filings 6c77089c, 1c368173, b947b377, 087a18c4, 1f12a09a and 7319bba (re-read, not executed, and
# re-typed here); the table, the fibre test, the segment scan and the ledger are new.
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
# first-level probe: presence word of the 8-bit window 16..23 of (u + PRES_C); |PRES_P| = 56 of 256 values (offline, appendix)
PRES_C, PRES_P, PRES_S = 0x43579466, 0x3e3e38383e3e3c3e3e3e3c302000003c0, 16

class Shake:
    def __init__(self, seed): self.seed = seed.encode(); self.k = 0; self.buf = b''; self.pos = 0
    def __call__(self):
        if self.pos + 32 > len(self.buf):
            self.buf = hashlib.shake_256(self.seed + b'|' + str(self.k).encode()).digest(1 << 14); self.k += 1; self.pos = 0
        v = int.from_bytes(self.buf[self.pos:self.pos + 32], 'little'); self.pos += 32; return v
    def below(self, n): return self() % n

class Mach:
    def __init__(self): self.n = 0
CTRL_FB, CTRL_HIT, SCAN_LANE, GATHER_LANE, RARE_LOOKUP = 16, 8, 4, 3, 2
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
    """lowest-first lane indices of the set bits: per chunk the extraction and a zero branch; per lane the table load of the pre-shifted
    batch-offset index (stored at address T_c + x), x - 1, x & (x - 1) and the loop branch: 4"""
    mc.n += chunk_fixed_ops(nl); out = [L for L in range(nl) if (plane >> L) & 1]; mc.n += SCAN_LANE * len(out); return out
def S0pack(a0): return a0 | (S0(a0) << 32)
def cv_pre(mc, cv):
    """per first block, at its first good group: the constants of W0 = a0 + kap0 and W1 (35 operations)"""
    Am1, Am2, Am3, Am4, Em1, Em2, Em3, Em4 = cv
    mc.n += 4; mj = (Am1 & Am2) | (Am3 & (Am1 | Am2))
    mc.n += 11; e0b = (Am4 - S0(Am1) - mj) & M32
    mc.n += 3; ch = (Em1 & (Em2 ^ Em3)) ^ Em3
    mc.n += 16; kap0 = (e0b - Am4 - Em4 - S1(Em1) - ch - K[0]) & M32
    mc.n += 4; n12 = Am1 & Am2
    return dict(e0b=e0b, kap0=kap0, x12=Am1 ^ Am2, n12=n12, X=Em1 ^ Em2, Em2=Em2, kap1=(A1 - K[1] - Em3 - n12) & M32)
GROUP_OPS, PROBE_OPS = 34, [3, 4, 4, 4]                   # direct R16[u] table probe: lane extraction (1 for k=0, 2 for k>=1), load, branch
def packed_u(recs, pre):
    """W0 + s0(W1) of four variants held in the four 64-bit lanes of one 256-bit word (lane-safe: S0(a0) <= 0xffffbb5c < 2^32 - 1 on G so a carry
    of 1 from the low 32 bits of G + bc(e0b) or G + bc(kap0) cannot overflow bit 63; MAJ(a0, Am1, Am2) = (a0 & (Am1 ^ Am2)) + (Am1 & Am2) with
    Am1 & Am2 folded into kap1; the minuend of W1 carries the bias 2^34).  Returns U; lane k holds u_k in its low 32 bits."""
    G = 0
    for k in range(4): G |= (recs[k] if k < len(recs) else 0) << (64 * k)
    s0a = (G >> 32) & LM
    E0 = (G + bc(pre['e0b'])) & LM
    W0 = (G + bc(pre['kap0'])) & M256
    mj = G & bc(pre['x12'])
    ch = (E0 & bc(pre['X'])) ^ bc(pre['Em2'])
    d = (E0 | (E0 << 32)) & M256
    S1E = (((d >> 6) ^ (d >> 11)) ^ (d >> 25)) & LM
    W1 = (sum((pre['kap1'] + (1 << 34)) << (64 * k) for k in range(4)) - s0a - mj - S1E - ch) & LM
    d1 = (W1 | (W1 << 32)) & M256
    s0W = (((d1 >> 7) ^ (d1 >> 18)) ^ (W1 >> 3)) & LM
    return (W0 + s0W) & M256
def good_group(mc, recs, pre, nvalid, probe):
    """one group of up to four good pairs: u (GROUP_OPS operations), then per valid lane the direct lookup in the 2^32-entry row-16 mask table
    R16[u] (address R16_BASE + u, load, branch on mask != 0: 3 operations for lane 0, 4 for lanes 1..3).  Returns [(lane, u)]."""
    mc.n += GROUP_OPS
    U = packed_u(recs, pre); hits = []
    for k in range(nvalid):
        mc.n += PROBE_OPS[k]
        u = (U >> (64 * k)) & M32
        if probe(u): hits.append((k, u))
    return hits
def recompute_w67(mc, a0, a, b, c7):
    mc.n += 23; return w6of(a0, a, b), (c7 - a) & M32
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
def passing_classes(x): return [c for c in range(NCLS) if F7((C7S[c] - x) & M32)]
class XEntry:
    """the table record of (x, class): the distinct values phi of the variants (fibres, sorted), their member lists, and the bit planes of the
    fibre values (256 fibres per batch; unused lanes repeat lane 0).  Built offline for every x (Section 8.2); read online."""
    def __init__(self, c, x):
        self.c = c; mem = cdata(c); groups = {}
        for a0 in mem: groups.setdefault(phi(a0, x), []).append(a0)
        self.vals = sorted(groups); self.nf = len(self.vals)
        self.recs = []; self.fib = []                        # fib[i] = (offset, length) into recs (stored as 32-bit offset | (ngroups << 12) | (rem << 22))
        for v in self.vals:
            self.fib.append((len(self.recs), len(groups[v]))); self.recs += [S0pack(a) for a in groups[v]]
        self.batches = []
        for b in range(0, self.nf, 256):
            lanes = self.vals[b:b + 256]; nl = len(lanes); lanes = lanes + [lanes[0]] * (256 - nl)
            pl = [sum(((v >> j) & 1) << L for L, v in enumerate(lanes)) for j in range(32)]
            self.batches.append((pl, nl))
NEEDW = (1, 2, 3, 8, 9, 10, 12, 13, 14, 15, 16, 18, 19, 20, 25, 26, 27, 29, 30, 31)
W6_OPS = 188          # exact count of w6_batch (asserted); +1 for the lane mask of a partial batch
def w6_batch(dl, z, nl):
    """pass plane of the F6 test for the fibre values dl (32 planes) plus the scalar cb (broadcast planes z): w = dl + z ripple (NOT-free full adder
    carry = a ^ ((a ^ b) & (a ^ c)) in 4 ops + 1 sum op at the 19 needed sum bits, and 3-op carry (a & b) | (c & (a ^ b)) at the 10 unreferenced
    sum bits {4,5,6,7,11,21,22,23,24,28}), then F6 in 25 ops with w[8] ^ w[25] pulled into the final pass mask.  Returns (plane, executed operations)."""
    ops = 32; w = {}                                          # 32 loads of the planes
    c = dl[0] & z[0]; ops += 1
    for j in range(1, 31):
        xy = dl[j] ^ z[j]
        if j in NEEDW:
            xz = dl[j] ^ c; carry = dl[j] ^ (xy & xz); w[j] = xy ^ c; ops += 5
        else:
            carry = (dl[j] & z[j]) | (c & xy); ops += 3
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
T0_OPS, ZPLANE_OPS, CLASS_OVH, SEG_OVH, FBFIX = 5, 95, 8, 6, 16 + 30 + 5

class Env:
    def __init__(self):
        self.Lt = setup_l(); self.R16 = make_R16(self.Lt); self.cache = {}; self.xc = {}
    def probe(self, u):
        if u not in self.cache: self.cache[u] = self.R16(u)
        return self.cache[u] != 0
    def xent(self, x, c):
        k = (x, c)
        if k not in self.xc:
            if len(self.xc) > 400: self.xc.clear()
            self.xc[k] = XEntry(c, x)
        return self.xc[k]

def process_cv(mc, cv, w, env, stats, check=None, max_classes=None, only=None):
    """everything the online phase does with one chaining value cv = F_37(IV, w): the table read, the fibre tests of the passing classes, the scans,
    the packed row-16 stage over the member blocks of the passing fibres, and rows 16..36 of every row-16 pass."""
    found = []
    mc.n += T0_OPS; hits = passing_classes(cv[0])           # the table read (the list is the stored record of x)
    if not hits: return found
    stats['hits_found'] = stats.get('hits_found', 0) + len(hits)
    mc.n += 2 + ZPLANE_OPS; cbv = (C6 - cv[1]) & M32; z = [ONE if (cbv >> j) & 1 else 0 for j in range(32)]
    segs = []
    for c in (hits if max_classes is None else hits[:max_classes]):
        if only is not None and c != only: continue
        stats['hits'] += 1; mc.n += CLASS_OVH; en = env.xent(cv[0], c); good = set()
        for b, (dl, nl) in enumerate(en.batches):
            plane, ops = w6_batch(dl, z, nl); mc.n += ops
            if check: check('plane', cv, (en, b), plane)
            for L in scan_plane(mc, plane, nl):
                off, ln = en.fib[256 * b + L]; mc.n += 1 + SEG_OVH
                segs.append((c, en.recs[off:off + ln])); good.update(r & M32 for r in en.recs[off:off + ln])
        if check: check('class', cv, c, good)
    stats['good'] += sum(len(s[1]) for s in segs)
    if segs:
        mc.n += 1; pre = cv_pre(mc, cv)
        for c, recs in segs:
            for g in range(0, len(recs), 4):
                chunk = recs[g:g + 4]
                for (k, u) in good_group(mc, chunk, pre, len(chunk), env.probe):
                    stats['r16'] += 1; mc.n += 1 + RARE_LOOKUP
                    a0 = chunk[k] & M32; ls = [l for l in FEASIBLE_L if (env.R16(u) >> l) & 1]
                    w6, w7 = recompute_w67(mc, a0, cv[0], cv[1], CLASSES[c][0])
                    r = step3b(mc, cv, a0, w6, w7, ls, env.Lt)
                    if r: found.append((w, a0, r))
    return found

def online(nfb, rng, env, stats, check=None, max_classes=None):
    mc = Mach(); found = []
    for f in range(nfb):
        mc.n += 16
        w = first_block(mc, rng); cv = compress(IV, w); stats['fb'] += 1; stats['m0'] = w
        found += process_cv(mc, cv, w, env, stats, check, max_classes)
    return mc.n, found

def detect(env, cv, mx, my, c, a0):
    mc = Mach(); st = dict(fb=0, hits=0, good=0, r16=0)
    fnd = process_cv(mc, cv, None, env, st, None, None, only=c)
    return int(any(f[1] == a0 and f[2][1] == mx and f[2][2] == my for f in fnd)), mc.n

def online_trial(rng, env, max_fb=64, sample=12, max_classes=6):
    """the counted online program on seed-drawn first blocks until one has a W7-passing class (at most max_fb), processing at most max_classes
    passing classes: every pass plane lane is checked against the scalar F6 test of its fibre value, the good set of each class against the
    brute-force definition over all its variants, `sample` good pairs against every cell of rows -4..15 for all 32 l"""
    bad = [0, 0, 0]; firstpair = []
    def check(kind, cv, a, b):
        if kind == 'plane':
            en, bi = a; plane = b; cbv = (C6 - cv[1]) & M32
            for L in range(en.batches[bi][1]):
                if ((plane >> L) & 1) != F6((cbv + en.vals[256 * bi + L]) & M32): bad[0] += 1
            return
        c, good = a, b                                    # kind == 'class'
        want = {a0 for a0 in cdata(c) if F6(w6of(a0, cv[0], cv[1]))}
        if want != good: bad[1] += 1
        for a0 in sorted(good)[:2]:
            wx, wy = words_from_cv(cv, a0)
            if not (inF(wx[7], D7, T7) and inF(wx[6], D6, T6) and wx[7] == (CLASSES[c][0] - cv[0]) & M32): bad[1] += 1
            if len(firstpair) < sample:
                for l in range(32):
                    (x14, x15), (y14, y15) = lstar(l)
                    tx = trace(cv, wx + [x14, x15], 16); ty = trace(cv, wy + [y14, y15], 16)
                    if not all(row_ok(tx, ty, i, i not in (6, 7)) for i in range(-4, 16)): bad[2] += 1
                firstpair.append((wx, wy))
    stats = dict(fb=0, hits=0, good=0, r16=0); ops = 0
    for f in range(max_fb):
        n, found = online(1, rng, env, stats, check, max_classes); ops += n
        if stats['hits']: break
    if firstpair: firstpair[0] = (stats['m0'],) + firstpair[0]
    obs = dict(first_blocks=stats['fb'], w7_classes=stats.get('hits_found', 0), classes_processed=stats['hits'], good_pairs=stats['good'],
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
STATS = '''
0 3456 274.0142 1.46178 899.8649 143.4596
1 3456 274.6729 1.46844 900.1920 144.7680
2 3456 282.2889 1.49200 902.6133 154.4533
3 3456 283.8644 1.50067 903.8133 159.2533
4 3456 274.7956 1.46578 900.1067 144.4267
5 3456 272.9951 1.46200 900.3822 145.5289
6 3456 273.0373 1.46222 898.7707 139.0827
7 3456 283.0027 1.49822 904.5991 162.3964
8 3456 281.8178 1.48467 902.8889 155.5556
9 3456 276.7351 1.47600 900.9964 147.9858
10 3456 276.2622 1.47467 901.9449 151.7796
11 3456 271.7160 1.44889 898.7822 139.1289
12 3456 279.9347 1.48067 902.6827 154.7307
13 3456 272.4964 1.45622 899.8693 143.4773
14 3456 277.4804 1.48089 900.9351 147.7404
15 3456 277.6738 1.48067 901.4764 149.9058
16 3456 274.6267 1.45956 901.2640 149.0560
17 3456 280.5071 1.48667 903.9396 159.7582
18 3456 276.6333 1.47844 900.7947 147.1787
19 3456 273.8018 1.46311 900.7147 146.8587
20 3456 281.8560 1.49444 903.7013 158.8053
21 3456 325.0827 1.66133 923.5978 238.3911
22 3456 375.6333 1.84422 947.2244 332.8978
23 3456 323.8353 1.65400 922.4236 233.6942
24 3456 380.9542 1.86356 947.6582 334.6329
25 3456 320.8049 1.65156 923.1556 236.6222
26 3456 367.4649 1.81311 943.4658 317.8631
27 3456 332.8884 1.69000 927.3587 253.4347
28 3456 326.4840 1.66133 923.9129 239.6516
29 3456 368.4600 1.81200 942.8373 315.3493
30 3456 321.6796 1.64133 924.1244 240.4978
31 3456 375.4853 1.84311 946.0729 328.2916
32 3456 328.3160 1.67622 925.4302 245.7209
33 3600 260.2476 1.42800 931.0604 124.2418
34 3600 258.7147 1.42667 928.5867 114.3467
35 3600 259.1449 1.42867 928.8222 115.2889
36 3600 266.0404 1.44689 930.7858 123.1431
37 3600 254.9764 1.41289 927.3956 109.5822
38 3600 260.8613 1.42667 930.1378 120.5511
39 3600 262.2969 1.44022 931.1058 124.4231
40 3600 265.3076 1.44356 930.8756 123.5022
41 3600 261.9676 1.43733 929.8782 119.5129
42 3600 264.2564 1.44644 930.0027 120.0107
43 3600 259.6133 1.42044 930.2222 120.8889
44 3600 266.6169 1.44311 930.4533 121.8133
45 3600 260.2151 1.43067 928.6267 114.5067
46 3600 264.3004 1.44733 929.8978 119.5911
47 3600 257.6662 1.41578 927.8284 111.3138
48 3600 258.0653 1.42267 927.9707 111.8827
49 3600 262.5120 1.43778 929.3822 117.5289
50 3600 259.6271 1.42400 929.9716 119.8862
51 3600 267.1871 1.45400 931.6773 126.7093
52 3600 261.4244 1.43333 929.7404 118.9618
53 3600 264.2280 1.43689 930.2160 120.8640
54 3584 309.6629 1.61556 945.4493 197.7973
55 3584 353.8460 1.76000 962.3733 265.4933
56 3584 312.9551 1.62200 945.2907 197.1627
57 3584 357.8980 1.77578 963.6360 270.5440
58 3584 306.3573 1.60156 945.0480 196.1920
59 3584 355.2351 1.77178 961.3276 261.3102
60 3584 311.0538 1.61156 944.0178 192.0711
61 3584 305.9080 1.59689 944.4382 193.7529
62 3584 361.2369 1.79756 964.5911 274.3644
63 3584 322.6422 1.65844 949.7262 214.9049
64 3584 356.1542 1.76733 961.5671 262.2684
65 3584 315.0298 1.62356 945.3351 197.3404
66 3456 271.7498 1.46644 900.0693 144.2773
67 3456 272.5329 1.46289 901.4364 149.7458
68 3456 278.0516 1.49089 903.2178 156.8711
69 3456 279.4418 1.48133 901.4951 149.9804
70 3456 283.6253 1.49867 904.5244 162.0978
71 3456 275.9329 1.46867 899.9538 143.8151
72 3456 272.5787 1.47000 902.3840 153.5360
73 3456 277.2498 1.48289 901.3778 149.5111
74 3456 273.0631 1.45889 897.5636 134.2542
75 3456 277.6311 1.47933 902.4924 153.9698
76 3456 278.3582 1.48333 901.9796 151.9182
77 3456 277.1596 1.48578 902.7840 155.1360
78 3456 270.9564 1.45356 900.3804 145.5218
79 3456 275.5133 1.47444 900.0871 144.3484
80 3456 277.4760 1.48578 901.7920 151.1680
81 3456 277.3160 1.47711 902.1849 152.7396
82 3456 272.7062 1.46444 900.1529 144.6116
83 3456 279.5449 1.49089 903.6036 158.4142
84 3456 272.9058 1.46511 899.6338 142.5351
85 3456 276.2342 1.47289 900.5511 146.2044
86 3456 274.3071 1.46711 900.4640 145.8560
87 3456 280.6489 1.48467 901.1111 148.4444
88 3456 271.6942 1.46200 899.6693 142.6773
89 3456 278.9831 1.48067 900.7609 147.0436
90 3456 274.5142 1.46556 900.5253 146.1013
91 3456 273.7627 1.46467 899.9138 143.6551
92 3456 279.4227 1.48044 900.0907 144.3627
93 3456 277.1809 1.47689 903.2693 157.0773
94 3456 278.7138 1.49333 902.1493 152.5973
95 3456 277.9867 1.48311 901.8196 151.2782
96 3456 284.0498 1.50133 903.4524 157.8098
97 3456 271.4742 1.45600 899.2604 141.0418
98 3456 323.5978 1.65756 922.7484 234.9938
99 3456 376.3516 1.83911 946.6187 330.4747
100 3456 329.8800 1.67578 926.6604 250.6418
101 3456 375.3680 1.83556 944.0627 320.2507
102 3456 325.5151 1.65867 924.9680 243.8720
103 3456 372.9462 1.83156 944.7698 323.0791
104 3456 327.1573 1.67044 924.3049 241.2196
105 3600 264.0462 1.43733 928.7769 115.1076
106 3600 262.0804 1.43356 929.8622 119.4489
107 3600 256.9751 1.41600 927.5929 110.3716
108 3600 262.9018 1.43289 930.1084 120.4338
109 3600 266.0293 1.44844 930.8222 123.2889
110 3600 261.1444 1.43089 930.1209 120.4836
111 3600 258.4440 1.41733 929.3200 117.2800
112 3600 259.6587 1.43267 930.8240 123.2960
113 3600 260.9209 1.42444 929.2711 117.0844
114 3600 261.5093 1.43867 929.4187 117.6747
115 3600 260.0911 1.42044 930.3236 121.2942
116 3600 260.9182 1.43133 929.7573 119.0293
117 3600 260.5187 1.42711 929.0320 116.1280
118 3600 262.3244 1.43978 930.9787 123.9147
119 3600 261.3876 1.42733 928.8116 115.2462
120 3600 258.6240 1.41556 927.7236 110.8942
121 3600 263.2240 1.44067 931.2631 125.0524
122 3600 262.8498 1.43556 930.3253 121.3013
123 3600 261.9556 1.43600 930.7493 122.9973
124 3600 261.7836 1.43844 931.3200 125.2800
125 3600 260.9289 1.42178 929.0391 116.1564
126 3600 266.2080 1.44444 930.2222 120.8889
127 3600 263.8231 1.43289 930.0444 120.1778
128 3600 261.2249 1.43533 931.2284 124.9138
129 3600 257.2520 1.41911 928.5413 114.1653
130 3600 270.7498 1.47133 931.2151 124.8604
131 3600 260.7458 1.43356 929.9040 119.6160
132 3600 264.4449 1.44200 930.0560 120.2240
133 3600 264.8947 1.44289 930.8827 123.5307
134 3600 262.2627 1.43756 929.5840 118.3360
135 3600 262.6409 1.43578 930.2107 120.8427
136 3600 258.8916 1.41778 927.4444 109.7778
137 3584 322.9618 1.66000 948.6631 210.6524
138 3584 364.2764 1.79644 965.0000 276.0000
139 3584 312.5440 1.61644 947.4587 205.8347
140 3584 361.9018 1.79000 963.6720 270.6880
141 3584 309.6502 1.60311 945.8542 199.4169
142 3584 361.3040 1.78400 964.4738 273.8951
143 3584 314.0009 1.62533 946.0271 200.1084
144 3456 290.1862 1.52956 903.3778 157.5111
145 3456 295.0169 1.54867 907.2036 172.8142
146 3456 297.2631 1.55889 907.4133 173.6533
147 3456 295.1836 1.54533 904.2133 160.8533
148 3456 299.8489 1.56556 906.4213 169.6853
149 3456 292.7858 1.54200 902.4569 153.8276
150 3456 294.3156 1.54511 903.0524 156.2098
151 3456 296.3582 1.54867 905.0880 164.3520
152 3456 294.3836 1.54489 905.2427 164.9707
153 3456 294.2724 1.54489 904.2302 160.9209
154 3456 296.3009 1.55733 907.5609 174.2436
155 3456 296.3116 1.55822 906.3947 169.5787
156 3456 291.2287 1.52889 904.9387 163.7547
157 3456 297.5676 1.55822 907.5538 174.2151
158 3456 296.5347 1.55289 904.8729 163.4916
159 3456 295.2658 1.54889 905.0827 164.3307
160 3456 291.0142 1.53711 905.4524 165.8098
161 3456 296.7658 1.56311 905.9360 167.7440
162 3456 295.3782 1.55511 905.1716 164.6862
163 3456 299.7173 1.56311 907.5111 174.0444
164 3456 287.2893 1.52311 903.3458 157.3831
165 3456 298.9436 1.56400 908.7751 179.1004
166 3456 290.3307 1.53667 905.5769 166.3076
167 3456 296.2173 1.55356 905.0151 164.0604
168 3456 295.6458 1.54778 903.9360 159.7440
169 3456 296.4593 1.55600 907.7316 174.9262
170 3456 299.7811 1.56600 906.0676 168.2702
171 3456 297.1600 1.56200 907.8916 175.5662
172 3456 292.6840 1.54267 906.0142 168.0569
173 3456 295.4658 1.55133 905.8702 167.4809
174 3456 301.5489 1.56911 907.2267 172.9067
175 3456 301.0171 1.57356 907.5111 174.0444
176 3456 352.4569 1.76911 933.4844 277.9378
177 3456 406.0831 1.96733 957.9147 375.6587
178 3456 358.7111 1.79644 933.8427 279.3707
179 3456 402.5964 1.95244 954.0240 360.0960
180 3456 344.4782 1.74600 929.4658 261.8631
181 3456 407.9516 1.96800 957.9644 375.8578
182 3456 355.4880 1.77822 934.1089 280.4356
183 3600 278.7293 1.51356 934.6373 138.5493
184 3600 282.2382 1.52956 936.5129 146.0516
185 3600 278.9013 1.51156 933.6356 134.5422
186 3600 279.9956 1.52844 936.3369 145.3476
187 3600 283.8653 1.53067 935.1182 140.4729
188 3600 277.0116 1.51578 934.7778 139.1111
189 3600 279.7671 1.52133 933.2676 133.0702
190 3600 284.8307 1.52933 935.1618 140.6471
191 3600 284.3109 1.53356 935.3502 141.4009
192 3600 281.1756 1.51956 935.6542 142.6169
193 3600 290.3487 1.55133 938.5831 154.3324
194 3600 277.5809 1.50889 932.5191 130.0764
195 3600 286.2116 1.53822 937.3813 149.5253
196 3600 279.5516 1.51378 933.8347 135.3387
197 3600 277.9547 1.51000 932.3813 129.5253
198 3600 278.4242 1.51244 934.3840 137.5360
199 3600 281.4076 1.52489 936.2213 144.8853
200 3600 282.3831 1.52867 935.2009 140.8036
201 3600 286.8249 1.54511 935.4267 141.7067
202 3600 278.4582 1.51756 935.7849 143.1396
203 3600 291.0391 1.56244 938.6764 154.7058
204 3600 284.0151 1.52489 933.7804 135.1218
205 3600 287.3524 1.54911 937.1413 148.5653
206 3600 289.1942 1.55533 935.3582 141.4329
207 3600 286.9813 1.54644 937.3876 149.5502
208 3600 284.3178 1.53400 935.1404 140.5618
209 3600 281.0262 1.52133 933.8391 135.3564
210 3600 281.7573 1.52644 935.9627 143.8507
211 3600 281.9776 1.52400 935.1422 140.5689
212 3600 285.5778 1.54089 934.1191 136.4764
213 3600 281.6431 1.52644 936.7884 147.1538
214 3600 288.1476 1.55556 937.9031 151.6124
215 3584 334.4520 1.71244 953.0933 228.3733
216 3584 384.7733 1.89000 973.5627 310.2507
217 3584 338.7480 1.73111 956.9182 243.6729
218 3584 389.1636 1.90911 974.7280 314.9120
219 3584 343.3227 1.74911 957.8658 247.4631
220 3584 387.3302 1.90533 974.3187 313.2747
221 3584 337.5487 1.72978 954.7040 234.8160
'''

def load_stats():
    out = {}
    for ln in STATS.strip().splitlines():
        ci, n, fb, bt, gr, pd = ln.split(); out[int(ci)] = (int(n), Fr(fb), Fr(bt), Fr(gr), Fr(pd))
    return out
# ---- the ledger (exact rationals).  Table statistics are Tungsten sample means (1500 values of x per class, conditional on the class passing)
#      scaled up by STAT_SAFETY; Q3_LOG2 = q3_model of the earlier preregistered studies ----
Q3_LOG2 = -74.03; STAT_SAFETY = Fr(102, 100); PXUB = Fr(16, 100)            # P(some class passes W7) <= 0.16 (measured 0.153)
PRE_OPS = 1 << 58                                                            # bound on all preprocessing operations (Section 8.2)
def ledger(q3_log2=Q3_LOG2, show=True, ac_log2=60, slack=Fr(1, 64), safety=STAT_SAFETY):
    C = 2644; VC = 1
    p7, p6, r16 = Fr(68157440, 1 << 32), Fr(287309824, 1 << 32), Fr(1052672, 1 << 32)
    st = load_stats(); nvar = sum(c[3] for c in CLASSES); g = nvar * p7 * p6
    chunk256 = chunk_fixed_ops(256)
    GPAIR = Fr(sum(PROBE_OPS), 4)                                            # direct R16[u] table probe per good pair (3 for lane 0, 4 for lanes 1..3)
    cls_cost = []; cls_worst = []
    for ci, (c7, base, mask, n) in enumerate(CLASSES):
        n_, fb, bt, gr, pd = st[ci]; assert n_ == n
        fb, bt, gr = fb * safety, bt * safety, gr * safety
        lanes = p6 * fb * (SCAN_LANE + 1 + SEG_OVH)                          # scan, (offset, length) load, segment set-up per passing fibre
        cls_cost.append(CLASS_OVH + bt * (W6_OPS + 1 + chunk256) + lanes + p6 * gr * GROUP_OPS)
        nb = (n + 255) // 256
        cls_worst.append(CLASS_OVH + nb * (W6_OPS + 1 + chunk256) + n * (SCAN_LANE + 1 + SEG_OVH) + n * GROUP_OPS)
    fixed = FBFIX
    c3b_pair = 201 + 23 + VC + RARE_LOOKUP; c3b_row = ROWCOMP + ROWCHECK + 1; c3b_l = 2 + 6 + 2 * c3b_row
    setup = PXUB * (2 + ZPLANE_OPS + 1 + 35)
    good_part = g * GPAIR
    rare = g * r16 * (c3b_pair + c3b_l + 19 * Fr(1, 512) * c3b_row)
    vbar = setup + p7 * sum(cls_cost) + good_part + rare
    fl = math.floor(q3_log2); q3ex = Fr(2) ** fl * Fr(math.floor(2 ** (q3_log2 - fl) * 2 ** 40), 2 ** 40)
    vmax_fb = sum(cls_worst) + nvar * (GPAIR + 3 + c3b_pair + 32 * (c3b_l + 19 * c3b_row)) + 200 + 2 * ZPLANE_OPS
    getcontext().prec = 60
    def mu_req(pcap):
        x = Decimal('0.61') - Decimal(pcap.numerator) / Decimal(pcap.denominator) - Decimal(2) ** -60
        d = Decimal(1) - (Decimal(-10.4) * Decimal(2).ln()).exp()
        mu = -x.ln() / d
        return Fr(int(math.floor(mu * 10 ** 8)) + 1, 10 ** 8)
    pcap = Fr(1, 1 << 24)
    for _ in range(4):
        XREQ = mu_req(pcap); nfb = int(-(-XREQ // (g * 32 * q3ex)))
        pcap = Fr(vmax_fb) / (Fr(1, 1 << 12) * nfb * vbar)
    VMAX = math.ceil((1 + slack) * nfb * vbar)
    T = Fr(2 ** ac_log2 + 2 ** 50 + 2 ** 40) + nfb + Fr(nfb * fixed + VMAX + math.ceil(vmax_fb) + PRE_OPS + 1600, C) + 6
    tl = math.ceil(math.log2(T) * 1e5) / 1e5; p5 = int(round(tl * 100000))
    out = dict(g=float(g), vbar=float(vbar), fixed=fixed, mu_req=float(XREQ), nfb=nfb, log2_nfb=math.log2(nfb), VMAX=VMAX, vmax_fb=float(vmax_fb),
               pcap_log2=math.log2(float(pcap)), time_log2=tl, log2_T=math.log2(T), T_num=T.numerator, T_den=T.denominator,
               tight_up=T.numerator ** 100000 <= (2 ** p5) * T.denominator ** 100000, tight_down=T.numerator ** 100000 > (2 ** (p5 - 1)) * T.denominator ** 100000,
               success_lower_bound=1 - math.exp(-(1 - 2.0 ** -10.4) * float(XREQ)) - float(pcap) - 2.0 ** -60,
               w6_part=float(p7 * sum(cls_cost)), good_part=float(good_part), setup_part=float(setup), rare_part=float(rare),
               per_fb_units=float(1 + Fr(fixed, C) + vbar / C), preprocessing_log2=math.log2(2 ** ac_log2 + 2 ** 50 + 2 ** 40 + Fr(PRE_OPS, C)))
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
    tot = bad = ps = 0
    for c in (0, 17, 40, 77, 111, 150, 200, 221):
        for _ in range(4):
            w = draw_F7(Shake(str(rr.random()))); x = (C7S[c] - w) & M32; am2 = rr.getrandbits(32); cbv = (C6 - am2) & M32
            en = XEntry(c, x); z = [ONE if (cbv >> j) & 1 else 0 for j in range(32)]; good = set()
            for b, (dl, nl) in enumerate(en.batches):
                plane, ops = w6_batch(dl, z, nl)
                for L in range(nl):
                    e = F6((cbv + en.vals[256 * b + L]) & M32); tot += 1; bad += e != bool((plane >> L) & 1)
                    if (plane >> L) & 1:
                        off, ln = en.fib[256 * b + L]; good.update(r & M32 for r in en.recs[off:off + ln])
            want = {a for a in cdata(c) if F6(w6of(a, x, am2))}; ps += len(want); bad += good != want
    print('fibre lanes %d, good pairs %d, mismatches %d' % (tot, ps, bad))
    bad = tot = 0
    for _ in range(40):
        cv = [rr.getrandbits(32) for _ in range(8)]; pre = cv_pre(Mach(), cv); mem = cdata(rr.randrange(NCLS))
        for g in range(0, 200, 4):
            chunk = mem[g:g + 4]; U = packed_u([S0pack(a) for a in chunk], pre)
            for k, a0 in enumerate(chunk):
                Ar = {-1: cv[0], -2: cv[1], -3: cv[2], -4: cv[3], 0: a0}; Er = {-1: cv[4], -2: cv[5], -3: cv[6], -4: cv[7]}
                Er[0] = (Ar[0] + Ar[-4] - S0(Ar[-1]) - MAJ(Ar[-1], Ar[-2], Ar[-3])) & M32
                W0 = (Er[0] - Ar[-4] - Er[-4] - S1(Er[-1]) - CH(Er[-1], Er[-2], Er[-3]) - K[0]) & M32
                Ar[1] = A1; Er[1] = (A1 + Ar[-3] - S0(a0) - MAJ(a0, Ar[-1], Ar[-2])) & M32
                W1 = (Er[1] - Ar[-3] - Er[-3] - S1(Er[0]) - CH(Er[0], Er[-1], Er[-2]) - K[1]) & M32
                tot += 1; bad += ((U >> (64 * k)) & M32) != ((W0 + s0(W1)) & M32)
    print('packed u: lanes %d mismatches %d' % (tot, bad))
    miss = sum(1 for u in random.Random(2).sample(range(1 << 32), 3000) if env.probe(u) and not (PRES_P >> ((((u + PRES_C) & M32) >> PRES_S) & 255)) & 1)
    print('presence word false negatives on 3000 random u:', miss)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'ledger': ledger()
    elif len(sys.argv) > 1 and sys.argv[1] == 'selftest': selftest()
    else: sys.stdout.write(json.dumps(run_request(json.loads(sys.stdin.read())), separators=(',', ':')))
