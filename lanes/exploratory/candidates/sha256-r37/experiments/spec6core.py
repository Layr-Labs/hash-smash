#!/usr/bin/env python3
# spec6core.py - sha256-r37: the A0-variant attack on 37-step SHA-256 with 222 classes, a counted online program whose W6 filter is
# a decision DAG over the bits of two per-first-block scalars, and the exact ledger.  Standard library only.
# Data: IACR ePrint 2026/1120 (characteristic, two-bit conditions, semi-free-start pair) as transcribed in earlier filings (6c77089c,
# 087a18c4, 1c368173, b947b377); every function below was written for this filing.
#   python3 spec6core.py ledger      exact ledger (about 15 minutes, one core)      stdin JSON request: organizer experiments
import hashlib, json, struct, sys
from fractions import Fraction as Fr
from functools import lru_cache

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

# ---- the straight-line builder over 256-bit planes (and, or, xor, not; load).  A literal is (node, neg) or ('c', 0|1); a NOT is
# emitted only when two literals of different stored polarity meet in an and/or; stored planes are prepared in either polarity ----
class B:
    def __init__(self):
        self.ops = []; self.notc = {}; self.ldc = {}
    def _new(self, kind, a=None, b=None):
        self.ops.append((kind, a, b)); return len(self.ops) - 1
    def ld(self, name):
        if name not in self.ldc: self.ldc[name] = self._new('ld', (name, None))
        n = self.ldc[name]; sp = self.ops[n][1][1]
        return ('f', n, 0) if sp is None else (n, sp)
    def res(self, lit, want=None):
        if lit[0] != 'f': return lit
        _, n, off = lit; name, sp = self.ops[n][1]
        if sp is None:
            sp = off ^ (0 if want is None else want); self.ops[n] = ('ld', (name, sp), None)
        return (n, sp ^ off)
    def isfree(self, lit): return lit[0] == 'f' and self.ops[lit[1]][1][1] is None
    def NOTl(self, lit):
        if lit[0] == 'c': return ('c', 1 - lit[1])
        if lit[0] == 'f': return ('f', lit[1], 1 - lit[2])
        return (lit[0], 1 - lit[1])
    NOT = NOTl
    def _flip(self, lit, wantneg):
        if lit[1] == wantneg: return lit
        if lit[0] not in self.notc: self.notc[lit[0]] = self._new('not', lit[0])
        return (self.notc[lit[0]], wantneg)
    def _bin(self, kpp, knn, a, b):
        fa, fb = self.isfree(a), self.isfree(b)
        if not fa: a = self.res(a)
        if not fb: b = self.res(b)
        if fa and not fb: a = self.res(a, b[1])
        elif fb and not fa: b = self.res(b, a[1])
        elif fa and fb: a = self.res(a, 0); b = self.res(b, 0)
        if a[1] != b[1]:
            if a[0] in self.notc: a = self._flip(a, b[1])
            else: b = self._flip(b, a[1])
        return (self._new(kpp, a[0], b[0]), 0) if a[1] == 0 else (self._new(knn, a[0], b[0]), 1)
    def AND(self, a, b):
        if a[0] == 'c': return b if a[1] else a
        if b[0] == 'c': return a if b[1] else b
        return self._bin('and', 'or', a, b)
    def OR(self, a, b):
        if a[0] == 'c': return a if a[1] else b
        if b[0] == 'c': return b if b[1] else a
        return self._bin('or', 'and', a, b)
    def XOR(self, a, b):
        if a[0] == 'c': return self.NOTl(b) if a[1] else b
        if b[0] == 'c': return self.NOTl(a) if b[1] else a
        a = self.res(a, 0); b = self.res(b, 0)
        return (self._new('xor', a[0], b[0]), a[1] ^ b[1])
    def FA(self, a, b, c, need_sum=True):
        """full adder without a NOT: carry = x ^ ((x ^ y) & (x ^ z)) for the pair (y, z) of equal stored polarity"""
        ops = [a, b, c]; cs = [x for x in ops if x[0] == 'c']
        if cs:
            rest = [x for x in ops if x[0] != 'c']; k = sum(x[1] for x in cs)
            if len(rest) == 2:
                u, v = rest
                if k == 0: return (self.XOR(u, v) if need_sum else None), self.AND(u, v)
                return (self.NOTl(self.XOR(u, v)) if need_sum else None), self.OR(u, v)
            if len(rest) == 1:
                x = rest[0]
                if k == 0: return x, ('c', 0)
                if k == 1: return self.NOTl(x), x
                return x, ('c', 1)
            t = sum(x[1] for x in ops); return ('c', t & 1), ('c', t >> 1)
        fixed = [not self.isfree(x) for x in ops]
        ops = [self.res(x) if f else x for x, f in zip(ops, fixed)]
        pols = [x[1] for x, f in zip(ops, fixed) if f]
        want = pols[0] if (len(pols) >= 2 and pols[0] == pols[1]) or len(pols) == 1 else 0
        ops = [x if f else self.res(x, want) for x, f in zip(ops, fixed)]
        P = [x[1] for x in ops]
        ia = 0 if P[1] == P[2] else (1 if P[0] == P[2] else 2)
        a_, b_, c_ = ops[ia], ops[(ia + 1) % 3], ops[(ia + 2) % 3]
        xy = self.XOR(a_, b_); xz = self.XOR(a_, c_)
        carry = self.XOR(a_, self.AND(xy, xz))
        return (self.XOR(xy, c_) if need_sum else None), carry

# ---- the W6 filter of a batch of <= 256 variants (lane L = variant L), specialised on the bits of A_{-1} and cb = C6 - A_{-2} ----
# bit-serial: W6x = cb + MAJ(A1, a0, A_{-1}) + ~CH(E5, E4, E3) + 1, E3 = K3 + A_{-1};  y_j = E5_j ? ~E4_j : ~E3_j
PAIRS = {'x3': (1, 12), 'y3': (2, 13), 's': (3, 14), 'x1': (14, 18), 'y1': (15, 19), 'q': (16, 20), 'x2': (8, 25), 'y2': (9, 26), 'r': (10, 27)}
NEEDED_W = sorted({b for pr in PAIRS.values() for b in pr} | {29, 30, 31})
ACC_BIRTH = {'x3': 12, 'y3': 13, 's': 14, 'cm': 18, 'bp': 19, 'q': 20, 'common': 25, 'bc': 26, 'r': 27}
ACC_DEATH = {'x3': 18, 'y3': 19, 'cm': 25, 'bp': 26}
def retained_after(j):
    return [p for p in NEEDED_W if p <= j and (p in (29, 30, 31) or any(p in pr and max(pr) > j for pr in PAIRS.values()))]
def acc_after(j): return [nm for nm, b in ACC_BIRTH.items() if b <= j and ACC_DEATH.get(nm, 99) > j]
CANON = {'w:2': 1, 'w:8': 1, 'w:14': 1, 'acc:x3': 1, 'acc:r': 1}          # stored polarity of the state values between bits (default 0)
CARRIES = ('c_e3', 'c_csa', 'k_rip')
def mk_lit(Bd, v, name):
    if v == 'V':
        n = Bd._new('ld', ('STATE:' + name, CANON.get(name, 0))); return (n, CANON.get(name, 0))
    return ('c', v)
def force_canon(Bd, lit, key):
    if lit[0] == 'c': return lit
    lit = Bd.res(lit, CANON.get(key, 0))
    return Bd._flip(lit, CANON.get(key, 0))

def bit_slice(Bd, St, j, sig, ab, z):
    a0s, k3s, e4s = sig
    inp = lambda kind, v: ('c', v) if v != 'V' else Bd.ld('%s:%d' % (kind, j))
    a0j = inp('A0', a0s)
    maj = Bd.OR(a0j, ab) if (A1 >> j) & 1 else Bd.AND(a0j, ab)
    if (E5 >> j) & 1:
        y = inp('NE4', e4s)
        if j < 28: _, St['c_e3'] = Bd.FA(inp('K3', k3s), ab, St['c_e3'], need_sum=False)
    else:
        sm, cn = Bd.FA(inp('K3', k3s), ab, St['c_e3'], need_sum=True)
        y = Bd.NOTl(sm)
        if j < 28: St['c_e3'] = cn
    s, nxt = Bd.FA(maj, y, z)
    wj, kn = Bd.FA(s, St['c_csa'], St['k_rip'], need_sum=True)
    St['w'][j] = wj
    if j < 31: St['k_rip'] = kn; St['c_csa'] = nxt
    W, a = St['w'], St['acc']; X, O_, N = Bd.XOR, Bd.OR, Bd.NOT
    if j == 12: a['x3'] = X(W[1], W[12])
    if j == 13: a['y3'] = X(W[2], W[13])
    if j == 14: a['s'] = X(W[3], W[14])
    if j == 18: a['cm'] = O_(X(W[14], W[18]), a['x3'])
    if j == 19: a['bp'] = O_(X(W[15], W[19]), a['y3'])
    if j == 20: a['q'] = X(W[16], W[20])
    if j == 25: a['common'] = O_(a['cm'], N(X(W[8], W[25])))
    if j == 26: a['bc'] = O_(a['bp'], N(X(W[9], W[26])))
    if j == 27: a['r'] = X(W[10], W[27])

PROG = {}
@lru_cache(maxsize=None)
def step(j, sig, state, ab, z):
    """the segment (bit j) for one batch: class-constant signature sig = (a0, k3, ne4) of bit j in {0, 1, 'V'}, abstract state (the carries are 0, 1
    or 'V'; every retained value is a register 'V'), the scalar bits ab, z.  Returns (executed ops, next abstract state)."""
    Bd = B(); sd = dict(state); npseudo = 0; St = dict(w={}, acc={})
    for nm in CARRIES: St[nm] = mk_lit(Bd, sd[nm], nm); npseudo += sd[nm] == 'V'
    for k, v in sd.items():
        if k.startswith('w:'): St['w'][int(k[2:])] = mk_lit(Bd, v, k); npseudo += 1
        if k.startswith('acc:'): St['acc'][k[4:]] = mk_lit(Bd, v, k); npseudo += 1
    bit_slice(Bd, St, j, sig, ('c', ab), ('c', z))
    outl = {}
    for nm in CARRIES: outl[nm] = force_canon(Bd, St[nm], nm) if (nm != 'c_e3' or j < 28) else St[nm]
    for p in retained_after(j): outl['w:%d' % p] = force_canon(Bd, St['w'][p], 'w:%d' % p)
    for nm in acc_after(j): outl['acc:' + nm] = force_canon(Bd, St['acc'][nm], 'acc:' + nm)
    ns = tuple(sorted((k, (l[1] if l[0] == 'c' else 'V') if k in CARRIES else 'V') for k, l in outl.items()))
    PROG[(j, sig, state, ab, z)] = (tuple(Bd.ops), outl)
    return len(Bd.ops) - npseudo, ns
def init_state(): return tuple(sorted({'c_e3': 0, 'c_csa': 1, 'k_rip': 0}.items()))

def tail_prog(state, lanemask):
    """fail = common | (w29 & (bc | (w30 & ((q^w31) | ~(r^w31) | (s^w31)))));  pass = ~fail, AND the lane mask of a partial batch"""
    Bd = B(); lit = {}; npseudo = 0
    for k, v in state:
        if k.startswith('w:') or k.startswith('acc:'): lit[k] = mk_lit(Bd, v, k); npseudo += 1
    w = lambda p: lit['w:%d' % p]; a = lambda nm: lit['acc:' + nm]
    X, O_, A_, N = Bd.XOR, Bd.OR, Bd.AND, Bd.NOT
    Xc = O_(O_(X(a('q'), w(31)), N(X(a('r'), w(31)))), X(a('s'), w(31)))
    fail = O_(a('common'), A_(w(29), O_(a('bc'), A_(w(30), Xc))))
    passl = Bd.res(N(fail))
    if passl[1] == 1: passl = (Bd._new('not', passl[0]), 0)
    if lanemask:
        m = Bd._new('ld', ('LANEMASK', 0)); npseudo += 1; passl = (Bd._new('and', passl[0], m), 0)
    return tuple(Bd.ops), passl, len(Bd.ops) - npseudo
@lru_cache(maxsize=None)
def tail_cost(state, lanemask): return tail_prog(state, lanemask)[2]

def sigs_of(members):
    out = []
    for j in range(32):
        row = []
        for f in (lambda a: a, k3of, ne4of):
            bits = {(f(a) >> j) & 1 for a in members}
            row.append(bits.pop() if len(bits) == 1 else 'V')
        out.append(tuple(row))
    return tuple(out)
def make_planes(members):
    lanes = members + [members[0]] * (256 - len(members)); d = {}
    for kind, f in (('A0', lambda a: a), ('K3', k3of), ('NE4', ne4of)):
        vs = [f(a) for a in lanes]
        for j in range(32): d['%s:%d' % (kind, j)] = int(''.join('1' if (v >> j) & 1 else '0' for v in reversed(vs)), 2)
    return d

def exec_ops(ops, getload, getstate):
    val = []
    for kind, a, b in ops:
        if kind == 'ld':
            name, sp = a
            v = getstate(name[6:]) if name.startswith('STATE:') else getload(name)
            val.append(v ^ (ONE if sp else 0))
        elif kind == 'not': val.append(val[a] ^ ONE)
        elif kind == 'and': val.append(val[a] & val[b])
        elif kind == 'or': val.append(val[a] | val[b])
        else: val.append(val[a] ^ val[b])
    return val
def lit_val(val, lit): return (ONE if lit[1] else 0) if lit[0] == 'c' else val[lit[0]] ^ (ONE if lit[1] else 0)
V_ADDS = 32            # one addition to V per bit of a group (immediate = the executed cost of the segments of the bit)
JUMPS = 32             # one unconditional jump per bit of a group: the segment of the bit continues at the (merged) test code of the next bit
TESTS = 128            # per group: for each of 32 bits, and + branch on the bit of A_{-1} and on the bit of cb
def run_group(batches, am1, cbv):
    """execute the decision DAG of a group of <= 4 batches on the scalars; batches = [(sigs, planes, nlanes)].
    Returns (pass planes, executed ops: tests + segments + tails; the V additions are charged by the caller)."""
    ops = TESTS; sa = [init_state() for _ in batches]
    sv = [{k: (ONE if v == 1 else 0) for k, v in init_state()} for _ in batches]
    for j in range(32):
        ab = (am1 >> j) & 1; z = (cbv >> j) & 1
        for q, (sigs, planes, nl) in enumerate(batches):
            c, ns = step(j, sigs[j], sa[q], ab, z)
            prog, outl = PROG[(j, sigs[j], sa[q], ab, z)]
            val = exec_ops(prog, lambda name: planes[name], lambda k: sv[q][k])
            sv[q] = {k: lit_val(val, l) for k, l in outl.items()}; sa[q] = ns; ops += c
    outs = []
    for q, (sigs, planes, nl) in enumerate(batches):
        tprog, passl, tc = tail_prog(sa[q], nl < 256)
        val = exec_ops(tprog, lambda name: (1 << nl) - 1, lambda k: sv[q][k])
        outs.append(lit_val(val, passl)); ops += tc
    return outs, ops

def expected_cost(sigs, lanemask):
    """exact expectation of the executed ops of one batch (excluding tests and V additions) over uniform independent bits of A_{-1} and cb"""
    dist = {init_state(): Fr(1)}; tot = Fr(0)
    for j in range(32):
        nd = {}
        for st, pr in dist.items():
            for ab in (0, 1):
                for z in (0, 1):
                    c, ns = step(j, sigs[j], st, ab, z)
                    tot += pr * Fr(1, 4) * c; nd[ns] = nd.get(ns, 0) + pr * Fr(1, 4)
        dist = nd
    for st, pr in dist.items(): tot += pr * tail_cost(st, lanemask)
    return tot
def worst_cost(sigs, lanemask):
    best = {init_state(): 0}
    for j in range(32):
        nb_ = {}
        for st, cc in best.items():
            for ab in (0, 1):
                for z in (0, 1):
                    c, ns = step(j, sigs[j], st, ab, z)
                    if nb_.get(ns, -1) < cc + c: nb_[ns] = cc + c
        best = nb_
    return max(cc + tail_cost(st, lanemask) for st, cc in best.items())

# ---- the W7 test of all 222 classes (lane = class): W7x = c7 - A_{-1} in F7, F7 = {w : w1 = w18, w0 = w28, w9 = w30 and
#      [w11 = 0, w22 = 1, w26 = 1] or [w11 = 1, w12 = 0, w22 = 0, w23 = 1, w26 = 0, w27 = 1, w2 = w19, w1 = w29, w10 = w31]} (exhaustive check, appendix) ----
C7S = [c[0] for c in CLASSES]
C7CC = [({(c >> j) & 1 for c in C7S}.pop() if len({(c >> j) & 1 for c in C7S}) == 1 else 'V') for j in range(32)]
C7PL = {'NC:%d' % j: sum(((1 - ((c >> j) & 1)) << i) for i, c in enumerate(C7S)) for j in range(32)}
W7_NEED = (0, 1, 2, 9, 10, 11, 12, 18, 19, 22, 23, 26, 27, 28, 29, 30, 31)
def w7_build(am1):
    """the path for A_{-1} = am1: borrow chain of c7 - A_{-1} with half subtractors (the bit of A_{-1} is a constant of the path)"""
    Bd = B(); b = ('c', 0); w = {}
    for j in range(32):
        a = (am1 >> j) & 1
        if C7CC[j] != 'V': C = ('c', C7CC[j]); NC = ('c', 1 - C7CC[j])
        else: NC = Bd.ld('NC:%d' % j); C = Bd.NOTl(NC)
        if j in W7_NEED: w[j] = Bd.XOR(Bd.XOR(C, ('c', a)), b)
        if j < 31: b = Bd.OR(NC, b) if a else Bd.AND(NC, b)
    X, O_, A_, N = Bd.XOR, Bd.OR, Bd.AND, Bd.NOT
    cm = O_(O_(X(w[1], w[18]), X(w[0], w[28])), X(w[9], w[30]))
    viol0 = O_(N(w[22]), N(w[26]))
    viol1 = O_(O_(O_(w[12], w[22]), O_(N(w[23]), w[26])), O_(O_(N(w[27]), X(w[2], w[19])), O_(X(w[1], w[29]), X(w[10], w[31]))))
    fail = O_(cm, O_(A_(w[11], viol1), A_(N(w[11]), viol0)))
    passl = N(fail)
    if passl[0] == 'c': return Bd, ('c', passl[1])
    passl = Bd.res(passl)
    if passl[1] == 1: passl = (Bd._new('not', passl[0]), 0)
    m = Bd._new('ld', ('LANEMASK', 0))
    return Bd, (Bd._new('and', passl[0], m), 0)
W7_TESTS, W7_JUMPS, W7_BOUND = 64, 32, 95   # and + branch per bit of A_{-1}; one jump per bit; structural bound on the executed ops of any path (Section 9.3)
W7COST = W7_TESTS + W7_JUMPS + W7_BOUND
def w7_run(am1):
    Bd, passl = w7_build(am1); mask = (1 << NCLS) - 1
    val = []
    for kind, a, b in Bd.ops:
        if kind == 'ld': name, sp = a; val.append((C7PL[name] if name != 'LANEMASK' else mask) ^ (ONE if sp else 0))
        elif kind == 'not': val.append(val[a] ^ ONE)
        elif kind == 'and': val.append(val[a] & val[b])
        elif kind == 'or': val.append(val[a] | val[b])
        else: val.append(val[a] ^ val[b])
    n = len(Bd.ops) - sum(1 for o in Bd.ops if o[0] == 'ld' and o[1][0] == 'LANEMASK')
    return lit_val(val, passl) & mask, n

# ---- the counted online program ----
class Shake:
    def __init__(self, seed): self.seed = seed.encode(); self.k = 0; self.buf = b''; self.pos = 0
    def __call__(self):
        if self.pos + 32 > len(self.buf):
            self.buf = hashlib.shake_256(self.seed + b'|' + str(self.k).encode()).digest(1 << 14); self.k += 1; self.pos = 0
        v = int.from_bytes(self.buf[self.pos:self.pos + 32], 'little'); self.pos += 32; return v
    def below(self, n): return self() % n

class Mach:
    def __init__(self): self.n = 0
CTRL_FB, CTRL_HIT, SCAN_LANE, GATHER_LANE, RARE_LOOKUP = 16, 8, 5, 3, 132
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
    """lowest-first lane indices of the set bits: per chunk the extraction and a zero branch; per lane the table load of the index (the chunk
    offset is in the table), the add of the batch base, x - 1, x & (x - 1) and the loop branch: 5"""
    mc.n += chunk_fixed_ops(nl); out = [L for L in range(nl) if (plane >> L) & 1]; mc.n += SCAN_LANE * len(out); return out

class ClassData:
    def __init__(self, c):
        self.c7, base, mask, n = CLASSES[c]
        self.members = class_members(self.c7, base, mask); assert len(self.members) == n
        self.nbt = (n + 255) // 256
        self.batches = []
        for b in range(self.nbt):
            m = self.members[256 * b:256 * b + 256]; self.batches.append((sigs_of(m), make_planes(m), len(m)))
        self.groups = [list(range(g, min(self.nbt, g + 4))) for g in range(0, self.nbt, 4)]

def S0pack(a0): return a0 | (S0(a0) << 32)
def cv_pre(mc, cv):
    """per first block, at its first good group: the constants of W0 = a0 + kap0 and W1 (35 operations)"""
    Am1, Am2, Am3, Am4, Em1, Em2, Em3, Em4 = cv
    mc.n += 4; mj = (Am1 & Am2) | (Am3 & (Am1 | Am2))
    mc.n += 11; e0b = (Am4 - S0(Am1) - mj) & M32
    mc.n += 3; ch = (Em1 & (Em2 ^ Em3)) ^ Em3
    mc.n += 16; kap0 = (e0b - Am4 - Em4 - S1(Em1) - ch - K[0]) & M32
    mc.n += 4
    return dict(e0b=e0b, kap0=kap0, o12=Am1 | Am2, n12=Am1 & Am2, X=Em1 ^ Em2, Em2=Em2, kap1=(A1 - K[1] - Em3) & M32)
GROUP_OPS, PRES_OPS, PROBE_OPS = 37, 5, [8, 9, 9, 9]     # probe: lane extraction, address, bit index, load, shift, and, branch, V addition
def packed_u(recs, pre):
    """W0 + s0(W1) of four variants held in the four 64-bit lanes of one 256-bit word (lane-safe: every subtrahend is reduced to 32 bits and the
    minuend of W1 carries the bias 2^34; the sums stay below 2^35).  Returns U; lane k holds u_k (+ possible carry bits above bit 31)."""
    G = 0
    for k in range(4): G |= (recs[k] if k < len(recs) else 0) << (64 * k)
    a0 = G & LM; s0a = (G >> 32) & LM
    E0 = (a0 + bc(pre['e0b'])) & LM
    W0 = a0 + bc(pre['kap0'])
    mj = (a0 & bc(pre['o12'])) | bc(pre['n12'])
    ch = (E0 & bc(pre['X'])) ^ bc(pre['Em2'])
    d = (E0 | (E0 << 32)) & M256
    S1E = (((d >> 6) ^ (d >> 11)) ^ (d >> 25)) & LM
    W1 = (sum((pre['kap1'] + (1 << 34)) << (64 * k) for k in range(4)) - s0a - mj - S1E - ch) & LM
    d1 = (W1 | (W1 << 32)) & M256
    s0W = (((d1 >> 7) ^ (d1 >> 18)) ^ (W1 >> 3)) & LM
    return (W0 + s0W) & M256
def good_group(mc, recs, pre, nvalid, probe):
    """one group of up to four good pairs: u (GROUP_OPS operations), then per valid lane the presence word of the window (u + PRES_C) >> 16 & 255
    and, if present, the exact row-16 probe.  probe(u) -> bool is the exact membership of u in the row-16 table (a bitmap lookup).  Returns [(lane, u)]."""
    mc.n += GROUP_OPS
    U = packed_u(recs, pre); Up = (U + bc(PRES_C)) & M256; hits = []
    for k in range(nvalid):
        mc.n += PRES_OPS
        if not (PRES_P >> ((Up >> (64 * k + PRES_S)) & 255)) & 1: continue
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

class Env:
    def __init__(self):
        self.Lt = setup_l(); self.R16 = make_R16(self.Lt); self.CD = {}; self.cache = {}
    def cd(self, c):
        if c not in self.CD: self.CD[c] = ClassData(c)
        return self.CD[c]
    def probe(self, u):
        if u not in self.cache: self.cache[u] = self.R16(u)
        return self.cache[u] != 0

def process_cv(mc, cv, w, env, stats, check=None, max_classes=None, only=None):
    """everything the online phase does with one chaining value cv = F_37(IV, w): W7 DAG, class scan, W6 DAGs, lane scans, good-pair groups,
    presence words, row-16 probes and rows 16..36 of every row-16 pass.  `only` restricts the processed classes (used by the experiments)."""
    found = []
    p7, n7 = w7_run(cv[0]); assert n7 <= W7_BOUND; mc.n += W7_TESTS + W7_JUMPS + n7
    hits = scan_plane(mc, p7, NCLS); mc.n += CTRL_HIT * len(hits)
    if not hits: return found
    stats['hits_found'] = stats.get('hits_found', 0) + len(hits)
    mc.n += 2; cbv = (C6 - cv[1]) & M32
    recs = []
    for c in (hits if max_classes is None else hits[:max_classes]):
        if only is not None and c != only: continue
        stats['hits'] += 1; mc.n += 1; cd = env.cd(c)
        for grp in cd.groups:
            outs, ops = run_group([cd.batches[b] for b in grp], cv[0], cbv); mc.n += ops + V_ADDS + JUMPS; stats['w6ops'] = stats.get('w6ops', 0) + ops + V_ADDS + JUMPS
            for q, b in enumerate(grp):
                if check: check('plane', cv, (cd, b), outs[q])
                for L in scan_plane(mc, outs[q], cd.batches[b][2]):
                    a0 = cd.members[256 * b + L]; mc.n += GATHER_LANE; recs.append((a0, S0pack(a0), c))
                    if check: check('good', cv, a0, cd)
        mc.n += 2
    stats['good'] += len(recs)
    if recs:
        mc.n += 40; pre = cv_pre(mc, cv); mc.n += 1
        for g in range(0, len(recs), 4):
            chunk = recs[g:g + 4]
            for (k, u) in good_group(mc, [r[1] for r in chunk], pre, len(chunk), env.probe):
                stats['r16'] += 1; mc.n += 1 + RARE_LOOKUP
                a0, _, c = chunk[k]; ls = [l for l in FEASIBLE_L if (env.R16(u) >> l) & 1]
                w6, w7 = recompute_w67(mc, a0, cv[0], cv[1], CLASSES[c][0])
                r = step3b(mc, cv, a0, w6, w7, ls, env.Lt)
                if r: found.append((w, a0, r))
    return found

def online(nfb, rng, env, stats, check=None, max_classes=None):
    """the online phase on nfb first blocks drawn from rng.  Returns (operation count, found pairs)."""
    mc = Mach(); found = []
    for f in range(nfb):
        mc.n += CTRL_FB
        w = first_block(mc, rng); cv = compress(IV, w); stats['fb'] += 1; stats['m0'] = w
        found += process_cv(mc, cv, w, env, stats, check, max_classes)
    return mc.n, found

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

def detect(env, cv, mx, my, c, a0):
    """feed a constructed chaining value to the counted program (class c only): returns 1 iff the program finds exactly the constructed pair
    (W7 DAG hit, W6 DAG pass, packed u, presence word, row-16 probe, rows 16..36)"""
    mc = Mach(); st = dict(fb=0, hits=0, good=0, r16=0)
    fnd = process_cv(mc, cv, None, env, st, None, None, only=c)
    return int(any(f[1] == a0 and f[2][1] == mx and f[2][2] == my for f in fnd)), mc.n

def online_trial(rng, env, max_fb=64, sample=12, max_classes=6):
    """the counted online program on seed-drawn first blocks until one has a W7-passing class (at most max_fb), processing at most
    max_classes of its passing classes: every lane of every pass plane is checked against the scalar W6 definition, every good pair
    against the Step-2 equations, `sample` good pairs against every cell of rows -4..15 for all 32 l"""
    bad = [0, 0, 0]; firstpair = []
    def check(kind, cv, a0, cd):
        if kind == 'plane':
            (cdd, b), plane = a0, cd
            for L in range(cdd.batches[b][2]):
                if ((plane >> L) & 1) != F6(w6of(cdd.members[256 * b + L], cv[0], cv[1])): bad[0] += 1
            return
        wx, wy = words_from_cv(cv, a0)
        if not (inF(wx[7], D7, T7) and inF(wx[6], D6, T6) and wx[7] == (cd.c7 - cv[0]) & M32): bad[1] += 1
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

# ---- the ledger (exact rationals) ----
Q3_LOG2 = -74.03                      # q3_model of the second preregistered study (Section 7.4)
def _batch_costs(args):
    ci, b = args
    c7, base, mask, n = CLASSES[ci]; mem = class_members(c7, base, mask); m = mem[256 * b:256 * b + 256]
    sg = sigs_of(m); return ci, b, expected_cost(sg, len(m) < 256), worst_cost(sg, len(m) < 256)

def ledger(procs=1, q3_log2=Q3_LOG2, show=True, wc=None, ac_log2=60, w6_generic=None):
    import math
    from decimal import Decimal, getcontext
    getcontext().prec = 60
    C = 2644; VC = 1
    p7, p6, r16 = Fr(68157440, 1 << 32), Fr(287309824, 1 << 32), Fr(1052672, 1 << 32)
    nvar = sum(c[3] for c in CLASSES); g = nvar * p7 * p6
    if wc is None:
        jobs = [(ci, b) for ci in range(NCLS) for b in range((CLASSES[ci][3] + 255) // 256)]
        if procs > 1:
            import multiprocessing as mp
            with mp.Pool(procs) as p: res = p.map(_batch_costs, jobs, chunksize=8)
        else: res = [_batch_costs(j) for j in jobs]
        wc = {(ci, b): (e, w) for ci, b, e, w in res}
    cls_cost, cls_worst = [], []
    for ci, (c7, base, mask, n) in enumerate(CLASSES):
        nbt = (n + 255) // 256; tot = Fr(0); worst = 0
        if w6_generic is not None:
            tot = Fr(258 + sum(w6_generic + 2 + chunk_fixed_ops(min(256, n - 256 * b)) for b in range(nbt))); cls_cost.append(tot + CTRL_HIT + VC + 2 + SCAN_LANE); cls_worst.append(tot); continue
        for gs in range(0, nbt, 4):
            grp = range(gs, min(nbt, gs + 4))
            tot += V_ADDS + JUMPS + TESTS + sum(wc[(ci, b)][0] for b in grp); worst += V_ADDS + JUMPS + TESTS + sum(wc[(ci, b)][1] for b in grp)
        for b in range(nbt):
            f = chunk_fixed_ops(min(256, n - 256 * b)); tot += f; worst += f
        cls_cost.append(tot + CTRL_HIT + VC + 2 + SCAN_LANE); cls_worst.append(worst)
    fixed = 30 + CTRL_FB + W7COST + chunk_fixed_ops(NCLS)
    RHO = Fr(bin(PRES_P).count('1'), 256)
    GL = SCAN_LANE + GATHER_LANE + Fr(GROUP_OPS + 4 * PRES_OPS, 4) + RHO * Fr(sum(PROBE_OPS), 4)
    c3b_pair = 201 + 23 + VC + RARE_LOOKUP; c3b_row = ROWCOMP + ROWCHECK + 1; c3b_l = 2 + 6 + 2 * c3b_row
    vbar = (NCLS * p7) * (2 + 40 + 35 + 1) + p7 * sum(cls_cost) + g * GL + g * r16 * (c3b_pair + c3b_l + 19 * Fr(1, 512) * c3b_row)
    fl = math.floor(q3_log2); q3ex = Fr(2) ** fl * Fr(math.floor(2 ** (q3_log2 - fl) * 2 ** 40), 2 ** 40)
    vmax_fb = sum(cls_worst) + sum(c[3] for c in CLASSES) * (GL + 3 + c3b_pair + 32 * (c3b_l + 19 * c3b_row)) + 76 + NCLS * 10
    def mu_req(pcap):
        x = Decimal(1) / Decimal(10) ** 0 * (Decimal('0.61') - Decimal(pcap.numerator) / Decimal(pcap.denominator) - Decimal(2) ** -60)
        d = Decimal(1) - (Decimal(-10.4) * Decimal(2).ln()).exp()
        mu = -x.ln() / d
        return Fr(int(math.floor(mu * 10 ** 8)) + 1, 10 ** 8)
    pcap = Fr(1, 1 << 24)
    for _ in range(4):
        XREQ = mu_req(pcap); nfb = int(-(-XREQ // (g * 32 * q3ex)))
        pcap = Fr(vmax_fb) / (Fr(1, 1 << 12) * nfb * vbar)
    VMAX = math.ceil((1 + Fr(1, 64)) * nfb * vbar)
    T = Fr(2 ** ac_log2 + 2 ** 50 + 2 ** 40) + nfb + Fr(nfb * fixed + VMAX + math.ceil(vmax_fb) + 2 ** 40 + 1600, C) + 6
    tl = math.ceil(math.log2(T) * 1e5) / 1e5; p5 = int(round(tl * 100000))
    out = dict(g=float(g), vbar=float(vbar), fixed=fixed, GL=float(GL), mu_req=float(XREQ), nfb=nfb, log2_nfb=math.log2(nfb), VMAX=VMAX,
               vmax_fb=float(vmax_fb), pcap_log2=math.log2(float(pcap)), time_log2=tl, log2_T=math.log2(T), T_num=T.numerator, T_den=T.denominator,
               tight_up=T.numerator ** 100000 <= (2 ** p5) * T.denominator ** 100000, tight_down=T.numerator ** 100000 > (2 ** (p5 - 1)) * T.denominator ** 100000,
               success_lower_bound=1 - math.exp(-(1 - 2.0 ** -10.4) * float(XREQ)) - float(pcap) - 2.0 ** -60,
               w6_part=float(p7 * sum(cls_cost)), good_part=float(g * GL), setup_part=float(NCLS * p7 * (2 + 40 + 35 + 1)),
               rare_part=float(g * r16 * (c3b_pair + c3b_l + 19 * Fr(1, 512) * c3b_row)), per_fb_units=float(1 + Fr(fixed, C) + vbar / C),
               preprocessing_log2=math.log2(2 ** 60 + 2 ** 50 + 2 ** 40 + Fr(2 ** 40, C)))
    assert out['tight_up'] and out['tight_down'] and out['success_lower_bound'] > 0.39
    if show:
        for k, v in out.items(): print('%-18s %s' % (k, v))
    return out

# ---- size of the compiled decision DAGs and register pressure (Section 9.4) ----
def _peak(ops, outl):
    n = len(ops); last = [-1] * n
    for i, (k, a, b) in enumerate(ops):
        for x in (a, b):
            if isinstance(x, int): last[x] = i
    for l in outl.values():
        if l[0] != 'c': last[l[0]] = n
    ends = {}
    for v in range(n):
        if last[v] >= 0: ends.setdefault(last[v], []).append(v)
    live = peak = 0
    for i in range(n):
        if last[i] >= 0: live += 1
        peak = max(peak, live); live -= len(ends.get(i, []))
    return peak
def _nstate(state): return sum(1 for k, v in state if v == 'V' or k[:2] in ('w:', 'ac'))
def _dag_group(args):
    ci, gs = args
    c7, base, mask, n = CLASSES[ci]; mem = class_members(c7, base, mask); nbt = (n + 255) // 256
    grp = list(range(gs, min(nbt, gs + 4))); sg = [sigs_of(mem[256 * b:256 * b + 256]) for b in grp]
    joint = {tuple(init_state() for _ in grp)}; nodes = instr = mxj = live_max = 0
    for j in range(32):
        nj = set()
        for js in joint:
            for ab in (0, 1):
                for z in (0, 1):
                    ns = []; ins = []; outs = []; pk = []; tot = 0
                    for q in range(len(grp)):
                        c, s2 = step(j, sg[q][j], js[q], ab, z); ops, outl = PROG[(j, sg[q][j], js[q], ab, z)]
                        ns.append(s2); tot += c; ins.append(_nstate(js[q])); outs.append(_nstate(s2)); pk.append(_peak(ops, outl))
                    for q in range(len(grp)): live_max = max(live_max, pk[q] + sum(outs[:q]) + sum(ins[q + 1:]))
                    instr += tot + 2; nj.add(tuple(ns))        # segments, the V addition and the jump of the variant
        nodes += len(joint); instr += 6 * len(joint); mxj = max(mxj, len(joint)); joint = nj      # per node: the test of A_{-1} and, in each branch, the test of cb (2 instructions each)
    for js in joint:
        for q in range(len(grp)): instr += tail_cost(js[q], len(mem[256 * grp[q]:256 * grp[q] + 256]) < 256)
    return nodes, instr, mxj, live_max
def dag_stats(procs=1):
    jobs = [(ci, gs) for ci in range(NCLS) for gs in range(0, (CLASSES[ci][3] + 255) // 256, 4)]
    if procs > 1:
        import multiprocessing as mp
        with mp.Pool(procs) as p: res = p.map(_dag_group, jobs, chunksize=4)
    else: res = [_dag_group(j) for j in jobs]
    print('groups %d joint nodes %d instructions %d (2^%.2f) max joint nodes per bit %d max live values %d' % (
        len(jobs), sum(r[0] for r in res), sum(r[1] for r in res), __import__('math').log2(sum(r[1] for r in res)), max(r[2] for r in res), max(r[3] for r in res)))

def selftest():
    """fast checks: F7 decomposition vs definition on random words, the W7 test, the W6 groups vs the scalar definition, the packed good-pair
    arithmetic vs the scalar definition of u, the row-16 evaluation vs the stored presence word"""
    import random
    rr = random.Random(1); env = Env(); bad = 0
    for _ in range(20000):
        w = draw_F7(Shake(str(rr.random()))); bad += not F7(w)
    print('F7 sampler violations', bad)
    tot = bad = ps = 0
    for _ in range(300):
        a = rr.getrandbits(32); res, n = w7_run(a); assert n <= W7_BOUND
        for i, c in enumerate(C7S): e = F7((c - a) & M32); tot += 1; ps += e; bad += e != bool((res >> i) & 1)
    print('W7: lanes %d passes %d mismatches %d' % (tot, ps, bad))
    tot = bad = ps = 0
    for ci in (0, 40, 77, 150, 221):
        cd = env.cd(ci)
        for grp in cd.groups:
            am1, am2 = rr.getrandbits(32), rr.getrandbits(32)
            outs, _ = run_group([cd.batches[b] for b in grp], am1, (C6 - am2) & M32)
            for q, b in enumerate(grp):
                for L in range(cd.batches[b][2]):
                    e = F6(w6of(cd.members[256 * b + L], am1, am2)); tot += 1; ps += e; bad += e != bool((outs[q] >> L) & 1)
    print('W6 groups: lanes %d passes %d mismatches %d' % (tot, ps, bad))
    # packed u against the definition of Lemma 4.1 (W0, W1 from the chaining value and the variant)
    bad = tot = 0
    for _ in range(40):
        cv = [rr.getrandbits(32) for _ in range(8)]; pre = cv_pre(Mach(), cv); mem = env.cd(rr.randrange(NCLS)).members
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
    print('presence word: false negatives on 3000 random u (and 0 on the 1,042,240 members: appendix) :', miss)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'ledger':
        ledger(int(sys.argv[2]) if len(sys.argv) > 2 else 1)
    elif len(sys.argv) > 1 and sys.argv[1] == 'dag':
        dag_stats(int(sys.argv[2]) if len(sys.argv) > 2 else 1)
    elif len(sys.argv) > 1 and sys.argv[1] == 'selftest':
        selftest()
    else:
        sys.stdout.write(json.dumps(run_request(json.loads(sys.stdin.read())), separators=(',', ':')))
