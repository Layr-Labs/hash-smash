#!/usr/bin/env python3
# lowm.py - sha256-r37: memory-tight A0-variant attack on 37-step SHA-256 over the 222 largest classes of G (< 2^20 bytes; stdlib only).
# Usage: python3 lowm.py selftest | ledger | memory | stdin JSON (organizer experiments)
import hashlib, json, math, random, struct, sys
from fractions import Fraction as Fr
from decimal import Decimal, getcontext
from math import comb

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
  16:'=0=====+=0===11=+==01=0=0==+====',17:'=0======01===u1=+==0==1===1u====',18:'=======uu=======n=====1====1====',
  19:'=======00====1==0==========1====',20:'==u====10=======1===00==========',21:'==0=============================',
  22:'==1============================='}
CHW = {6:'==n=============================',7:'=====u===u==========n===========',8:'==u=============================',
  9:'=====u=u=======n===u==n=u=n=u=n=',10:'============n======u=n==========',14:'=0===u===n=1=1====1=u=1=====1=1=',
  15:'==u=============================',22:'=====0=nn=====1=u=1=============',24:'==n============================='}
X2 = [('A',15,15,'!','A',16,15),('A',15,23,'=','A',16,23),('A',15,25,'=','A',16,25),('A',16,9,'!','A',16,20),
  ('A',16,18,'!','A',16,6),('A',16,8,'=','A',16,17),('A',15,29,'=','A',17,29),('A',17,29,'=','A',18,29),
  ('E',15,4,'=','E',16,4),('E',17,0,'!','E',17,13),('E',16,15,'=','E',17,15),
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
C4 = (A4 - S0(A3) - MAJ(A3, A2, A1)) & M32
W8C = (SE[8] - A4 - S1(E7) - CH(E7, E6, E5) - K[8]) & M32
C6 = (E6 - 2 * A2 + S0(A1) - S1(E5) - K[6]) & M32
K3C = (A3 - S0(A2)) & M32
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

# 222 classes: c7 and base of each (in LISTID order)
LMASK = (0x01fec08d, 0x01fec48d, 0x01fec09d, 0x01fec09d, 0x01fec0dd, 0x01fec08d, 0x01fec48d, 0x01fec09d, 0x01fec09d, 0x01fec0dd)
LSIZE = (3456, 3456, 3456, 3456, 3456, 3600, 3600, 3584, 3584, 3584)
LISTID = ('000000000000011100000232423224232555555555555566655555787978779787000000000000000000000000000000002324232555555'
     '555555555555555555555555557879787000000000000000000000000000000002324232555555555555555555555555555555557879787')
_CB = """
cc8e8c4c 1c010142 cc8e8c5c 1c010112 cc8e8c6c 1c010122 cc8e8c7c 1c010132 cc8e8c8c 1c010102 cc8e8e1c 1c010352
cc8e8e2c 1c010362 cc8e8e3c 1c010372 cc8e8e4c 1c010342 cc8e8e5c 1c010312 cc8e8e6c 1c010322 cc8e8e7c 1c010332
cc8e8e8c 1c010302 cc8e901c 1c010152 cc8e902c 1c010162 cc8e903c 1c010172 cc8e904c 1c010542 cc8e905c 1c010512
cc8e906c 1c010522 cc8e907c 1c010532 cc8e908c 1c010502 cc8e9228 1c010760 cc8e9238 1c010760 cc8e9248 1c010740
cc8e9258 1c010700 cc8e9268 1c010720 cc8e9278 1c010720 cc8e9288 1c010700 cc8e9448 1c010940 cc8e9458 1c010900
cc8e9468 1c010920 cc8e9478 1c010920 cc8e9488 1c010900 cc968c4c 1c010142 cc968c5c 1c010112 cc968c6c 1c010122
cc968c7c 1c010132 cc968c8c 1c010102 cc968e1c 1c010352 cc968e2c 1c010362 cc968e3c 1c010372 cc968e4c 1c010342
cc968e5c 1c010312 cc968e6c 1c010322 cc968e7c 1c010332 cc968e8c 1c010302 cc96901c 1c010152 cc96902c 1c010162
cc96903c 1c010172 cc96904c 1c010542 cc96905c 1c010512 cc96906c 1c010522 cc96907c 1c010532 cc96908c 1c010502
cc969228 1c010760 cc969238 1c010760 cc969248 1c010740 cc969258 1c010700 cc969268 1c010720 cc969278 1c010720
cc969288 1c010700 cc969448 1c010940 cc969458 1c010900 cc969468 1c010920 cc969478 1c010920 cc969488 1c010900
ce8e8d1c 1e010052 ce8e8d2c 1e010062 ce8e8d3c 1e010072 ce8e8d4c 1e010042 ce8e8d5c 1e010012 ce8e8d6c 1e010022
ce8e8d7c 1e010032 ce8e8d8c 1e010002 ce8e8f1c 1e010252 ce8e8f2c 1e010262 ce8e8f3c 1e010272 ce8e8f4c 1e010242
ce8e8f5c 1e010212 ce8e8f6c 1e010222 ce8e8f7c 1e010232 ce8e8f8c 1e010202 ce8e911c 1e010452 ce8e912c 1e010462
ce8e913c 1e010472 ce8e914c 1e010442 ce8e915c 1e010412 ce8e916c 1e010422 ce8e917c 1e010432 ce8e918c 1e010402
ce8e931c 1e010652 ce8e932c 1e010662 ce8e933c 1e010672 ce8e934c 1e010642 ce8e935c 1e010612 ce8e936c 1e010622
ce8e937c 1e010632 ce8e938c 1e010602 ce8e9528 1e010860 ce8e9538 1e010860 ce8e9548 1e010840 ce8e9558 1e010800
ce8e9568 1e010820 ce8e9578 1e010820 ce8e9588 1e010800 ce968d1c 1e010052 ce968d2c 1e010062 ce968d3c 1e010072
ce968d4c 1e010042 ce968d5c 1e010012 ce968d6c 1e010022 ce968d7c 1e010032 ce968d8c 1e010002 ce968f1c 1e010252
ce968f2c 1e010262 ce968f3c 1e010272 ce968f4c 1e010242 ce968f5c 1e010212 ce968f6c 1e010222 ce968f7c 1e010232
ce968f8c 1e010202 ce96911c 1e010452 ce96912c 1e010462 ce96913c 1e010472 ce96914c 1e010442 ce96915c 1e010412
ce96916c 1e010422 ce96917c 1e010432 ce96918c 1e010402 ce96931c 1e010652 ce96932c 1e010662 ce96933c 1e010672
ce96934c 1e010642 ce96935c 1e010612 ce96936c 1e010622 ce96937c 1e010632 ce96938c 1e010602 ce969528 1e010860
ce969538 1e010860 ce969548 1e010840 ce969558 1e010800 ce969568 1e010820 ce969578 1e010820 ce969588 1e010800
d28e8d1c 1a010052 d28e8d2c 1a010062 d28e8d3c 1a010072 d28e8d4c 1a010042 d28e8d5c 1a010012 d28e8d6c 1a010022
d28e8d7c 1a010032 d28e8d8c 1a010002 d28e8f1c 1a010252 d28e8f2c 1a010262 d28e8f3c 1a010272 d28e8f4c 1a010242
d28e8f5c 1a010212 d28e8f6c 1a010222 d28e8f7c 1a010232 d28e8f8c 1a010202 d28e911c 1a010452 d28e912c 1a010462
d28e913c 1a010472 d28e914c 1a010442 d28e915c 1a010412 d28e916c 1a010422 d28e917c 1a010432 d28e918c 1a010402
d28e931c 1a010652 d28e932c 1a010662 d28e933c 1a010672 d28e934c 1a010642 d28e935c 1a010612 d28e936c 1a010622
d28e937c 1a010632 d28e938c 1a010602 d28e9528 1a010860 d28e9538 1a010860 d28e9548 1a010840 d28e9558 1a010800
d28e9568 1a010820 d28e9578 1a010820 d28e9588 1a010800 d2968d1c 1a010052 d2968d2c 1a010062 d2968d3c 1a010072
d2968d4c 1a010042 d2968d5c 1a010012 d2968d6c 1a010022 d2968d7c 1a010032 d2968d8c 1a010002 d2968f1c 1a010252
d2968f2c 1a010262 d2968f3c 1a010272 d2968f4c 1a010242 d2968f5c 1a010212 d2968f6c 1a010222 d2968f7c 1a010232
d2968f8c 1a010202 d296911c 1a010452 d296912c 1a010462 d296913c 1a010472 d296914c 1a010442 d296915c 1a010412
d296916c 1a010422 d296917c 1a010432 d296918c 1a010402 d296931c 1a010652 d296932c 1a010662 d296933c 1a010672
d296934c 1a010642 d296935c 1a010612 d296936c 1a010622 d296937c 1a010632 d296938c 1a010602 d2969528 1a010860
d2969538 1a010860 d2969548 1a010840 d2969558 1a010800 d2969568 1a010820 d2969578 1a010820 d2969588 1a010800
""".split()
CLASSES = [(int(_CB[2 * i], 16), int(_CB[2 * i + 1], 16), LMASK[int(l)], LSIZE[int(l)]) for i, l in enumerate(LISTID)]
NCLS = len(CLASSES)

# ---- L* and row-16 (Section 6.2) ----
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
FEASIBLE_L = list(range(32))     # with E16[23] free (R16x) every l has 65,536 row-16 values
class Shake:
  def __init__(self, seed): self.seed = seed.encode(); self.k = 0; self.buf = b''; self.pos = 0
  def __call__(self):
    if self.pos + 32 > len(self.buf):
      self.buf = hashlib.shake_256(self.seed + b'|' + str(self.k).encode()).digest(1 << 14); self.k += 1; self.pos = 0
    v = int.from_bytes(self.buf[self.pos:self.pos + 32], 'little'); self.pos += 32; return v
  def below(self, n): return self() % n

class Mach:
  def __init__(self): self.n = 0
LM = sum(M32 << (64 * k) for k in range(4)); M256 = ONE
def bc(x): return sum((x & M32) << (64 * k) for k in range(4))
def first_block(mc, rng):
  r = [rng(), rng()]; mc.n += 2; w = []
  for k in range(16):
    x = r[k // 8]
    if k % 8: x >>= 32 * (k % 8); mc.n += 1
    if k % 8 != 7: x &= M32; mc.n += 1
    w.append(x & M32)
  return w
RBASE = 0
def cv_pre(mc, cv):
  Am1, Am2, Am3, Am4, Em1, Em2, Em3, Em4 = cv
  mc.n += 4; mj = (Am1 & Am2) | (Am3 & (Am1 | Am2))
  mc.n += 11; e0b = (Am4 - S0(Am1) - mj) & M32
  mc.n += 3; ch = (Em1 & (Em2 ^ Em3)) ^ Em3
  mc.n += 16; kap0 = (e0b - Am4 - Em4 - S1(Em1) - ch - K[0]) & M32
  mc.n += 5 + 42; n12 = Am1 & Am2
  return dict(e0b=e0b, kap0=kap0, C=((kap0 - e0b) & M32) + RBASE, x12=Am1 ^ Am2, n12=n12, X=Em1 ^ Em2, Em2=Em2, kap1=(A1 - K[1] - Em3 - n12) & M32)
M64 = (1 << 64) - 1
def bc64(x): return sum(x << (64 * k) for k in range(4))
def recompute_w67(mc, a0, a, b):
  mc.n += RECOMP; return w6of(a0, a, b), (c7of(a0) - a) & M32
def step3b(mc, cv, a0, w6, w7, ls, Lt):
  Am1, Am2, Am3, Am4, Em1, Em2, Em3, Em4 = cv
  Ar = {-1: Am1, -2: Am2, -3: Am3, -4: Am4, 0: a0, 1: SA[1], 2: SA[2], 3: SA[3], 4: SA[4], 5: SA[5]}
  Er = {-1: Em1, -2: Em2, -3: Em3, -4: Em4}
  for i in range(6): Er[i] = (Ar[i] + Ar[i-4] - S0(Ar[i-1]) - MAJ(Ar[i-1], Ar[i-2], Ar[i-3])) & M32
  W = {i: (Er[i] - Ar[i-4] - Er[i-4] - S1(Er[i-1]) - CH(Er[i-1], Er[i-2], Er[i-3]) - K[i]) & M32 for i in range(6)}
  mc.n += 201
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
  a = {i: Av[i] for i in range(4, 8)}; e = {i: Ev[i] for i in range(4, 8)}
  for i in range(7, -1, -1):
    T1 = (a[i] - S0(a[i-1]) - MAJ(a[i-1], a[i-2], a[i-3])) & M32
    a[i-4] = (e[i] - T1) & M32
    e[i-4] = (T1 - S1(e[i-1]) - CH(e[i-1], e[i-2], e[i-3]) - K[i] - W[i]) & M32
  return [a[-1], a[-2], a[-3], a[-4], e[-1], e[-2], e[-3], e[-4]]
def words_from_cv(cv, a0):
  out = []
  for Sx in (SA, SAy):
    A = {-1: cv[0], -2: cv[1], -3: cv[2], -4: cv[3]}; E = {-1: cv[4], -2: cv[5], -3: cv[6], -4: cv[7]}
    for i in range(14): A[i] = Sx[i]
    A[0] = a0
    for i in range(14): E[i] = (A[i] + A[i-4] - S0(A[i-1]) - MAJ(A[i-1], A[i-2], A[i-3])) & M32
    out.append([(E[i] - A[i-4] - E[i-4] - S1(E[i-1]) - CH(E[i-1], E[i-2], E[i-3]) - K[i]) & M32 for i in range(14)])
  return out
SAy = [trace(CV0, MY, 14)[0][i] for i in range(14)]

IMP = {18: (0x30040c22, 0x20000c02), 19: (1 << 29, 1 << 29)}
PAT = ((0, 0), (0x20040420, 1 << 29), (0x10040822, 0), (0x30000c02, 1 << 29),
   (0x10040820, 0), (0x30000c00, 1 << 29), (0x00000002, 0), (0x20040422, 1 << 29))
L28 = [l for l in range(32) if l not in (0, 2, 16, 18)]
def sfs_trial(rng, Lt, cls=None, env=None, cap=1 << 11, restarts=12, tail_cap=1 << 14, pat=0):
  c = rng.below(NCLS) if cls is None else cls; members = env.members(c); a0 = members[rng.below(len(members))]
  LL = FEASIBLE_L if pat > 3 else L28; l = LL[rng.below(len(LL))]; Ld = Lt[l]
  for attempt in range(restarts):
    X, Y = new_rows(Ld['tx'], Ld['ty']); tries = []; dead = False
    for t in range(16, 22):
      m, v, _, _ = CELLS['E'][t]
      if t == 16: m |= 1 << 23; v |= (1 << 23) if pat > 3 else 0
      if t == 17: m |= 1 << 24; v |= (((X[1][16] >> 24) & 1) ^ (1 if pat > 3 else 0)) << 24
      if t in IMP: m |= IMP[t][0]; v |= IMP[t][1] ^ PAT[pat][t - 18]
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
  return cv, mx, my, dict(class_index=c, variant_index=members.index(a0), l=l, pattern=pat, checks_passed=int(ok), restarts=attempt, proposals_row16=tries[0], proposals_tail=tries[-1])

# ======================= NEW: the memory-tight online program (222 classes, no x-indexed table) =======================
class CN: n = 0; flips = 0
class Pl:
  __slots__ = ('v', 'c', 'f')
  def __init__(s, v, c=None, f=0): s.v = v; s.c = c; s.f = f
  def tv(s): return s.v ^ (ONE if s.f else 0)
Z0 = Pl(0, 0); Z1 = Pl(ONE, 1)
def dyn(v): return Pl(v)
def inv(a):
  if a.c is None: CN.flips += 1
  return (Z1 if a.c == 0 else Z0) if a.c is not None else Pl(a.v, None, a.f ^ 1)
def xor(a, b):
  if a.c is not None: return b if a.c == 0 else inv(b)
  if b.c is not None: return a if b.c == 0 else inv(a)
  CN.n += 1; return Pl(a.v ^ b.v, None, a.f ^ b.f)
def and_(a, b):
  if a.c is not None: return Z0 if a.c == 0 else b
  if b.c is not None: return Z0 if b.c == 0 else a
  if a.f and b.f: CN.n += 1; return Pl(a.v | b.v, None, 1)
  if not a.f and not b.f: CN.n += 1; return Pl(a.v & b.v)
  CN.n += 2; return Pl(a.tv() & b.tv())
def or_(a, b):
  if a.c is not None: return Z1 if a.c == 1 else b
  if b.c is not None: return Z1 if b.c == 1 else a
  if a.f and b.f: CN.n += 1; return Pl(a.v & b.v, None, 1)
  if not a.f and not b.f: CN.n += 1; return Pl(a.v | b.v)
  CN.n += 2; return Pl(a.tv() | b.tv())
def force(a):
  if a.c is not None or not a.f: return a
  CN.n += 1; return Pl(a.v ^ ONE)
def to_f1(a): return a if (a.c is not None or a.f == 1) else inv(force(inv(a)))
def and1(a, b): return (Z0 if a.c == 0 else b) if a.c is not None else ((Z0 if b.c == 0 else a) if b.c is not None else and_(to_f1(a), to_f1(b)))
def or1(a, b): return (b if a.c == 0 else Z1) if a.c is not None else ((a if b.c == 0 else Z1) if b.c is not None else or_(to_f1(a), to_f1(b)))
def sel(c, t, f):
  if c.c is not None: return t if c.c else f
  return xor(f, and_(c, xor(t, f))) if f.f == 0 else xor(t, and_(inv(c), xor(t, f)))
def fa_step2(a, b, c, need_s=True, need_c=True):
  if c.c is not None: b, c = c, b
  if a.c is not None: a, b = b, a
  if b.c is not None:
    xy = a if b.c == 0 else inv(a)
    return (xor(xy, c) if need_s else None), ((and_(a, c) if b.c == 0 else or_(a, c)) if need_c else Z0)
  if b.f != c.f:
    if a.f == b.f: a, c = c, a
    else: a, b = b, a
  yc = xor(b, c); s = xor(a, yc) if need_s else None
  co = (xor(b, and_(yc, xor(a, b))) if a.f == b.f else xor(c, and_(yc, xor(inv(a), b)))) if need_c else Z0
  return s, co
def fa_carry2(a, b, c): return fa_step2(a, b, c, False, True)[1]
def add(A, B, cin=Z0, need=None):
  n = len(A); out = [None] * n; c = cin; top = max(need) if need is not None else n - 1
  for j in range(top + 1): out[j], c = fa_step2(A[j], B[j], c, need is None or j in need, j < top)
  return out
def sub(A, B, need=None): return add(A, [inv(b) for b in B], Z1, need)
def scal(s): return [dyn(ONE if (s >> j) & 1 else 0) for j in range(32)]
def bgen(js): return sum(2 if j == 0 else 3 for j in js)
def planes_from_values(vals): return [sum(((v >> j) & 1) << L for L, v in enumerate(vals)) for j in range(32)]

# ---- constants of the plane programs ----
FA, AA = A1 ^ A2, A1 & A2
MASK17 = 0x01fec4dd; ALWAYS = 0x01fec08d; A1_EFF = A1 ^ (MASK17 ^ (1 << 6) ^ (1 << 19))
M_KZ = ((~E5) ^ (1 << 16) ^ (1 << 11)) & M32
NEEDW = (1, 2, 3, 8, 9, 10, 12, 13, 14, 15, 16, 18, 19, 20, 25, 26, 27, 29, 30, 31)
NEEDF7 = (0, 1, 2, 9, 10, 11, 12, 18, 19, 22, 23, 26, 27, 28, 29, 30, 31)
MB = [j for j in range(32) if (MASK17 >> j) & 1]
MB_NZ = [j for j in MB if j > 0]
MB_S = [j for j in MB if j != 19]
KZB = [8, 10, 11, 12, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 25, 28]
ZC = list(range(1, 32)); C7_CONST = 0xc0868008
C7_DYN_BITS = [2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 19, 20, 25, 26, 27, 28]
def H4_of(base, lid): return (((base + C4) & M32) ^ (0x800 if lid in (1, 6) else 0)) & E5
def make_zNKZ(KZ):
  NKZ = (~KZ) & M32; NKZ2 = (NKZ & (NKZ << 1)) & M32; NKZ3 = (NKZ2 & (NKZ >> 1)) & M32
  out = {j: dyn(ONE if (NKZ >> j) & 1 else 0) for j in (10, 14, 15, 16, 18, 19, 20, 21, 22, 23)}
  out[11] = dyn(ONE if (KZ >> 11) & 1 else 0)
  for j in (17, 28): out[j] = dyn(ONE if (NKZ2 >> j) & 1 else 0)
  for j in (8, 12, 25): out[j] = dyn(ONE if (NKZ3 >> j) & 1 else 0)
  return out
def cls_offset(base, lid, B):
  neg = sum(1 << j for j in (2, 3, 14, 15, 17, 18, 20, 21, 22, 23, 24) if not ((B >> j) & 1)) | (16 if lid in (2, 7) else 0)
  return (-H4_of(base, lid) - neg - ((2 << 19) if lid < 5 else 0) - 0x20114000) & M32
def CB3_of(CB2, base, q, KZ, lid, B):
  return (CB2 + (((base | (1 << 19)) if lid < 5 else base) & q) + cls_offset(base, lid, B) - (KZ & M_KZ)) & M32
def f7_test(w):
  c1 = or_(or_(xor(w[1], w[18]), xor(w[0], w[28])), xor(w[9], w[30]))
  c2 = or_(or_(xor(w[2], w[19]), xor(w[1], w[29])), xor(w[10], w[31]))
  A = and1(and_(w[22], w[26]), inv(w[11])); Bp = and_(and_(w[11], w[23]), w[27])
  Bn = and_(and_(inv(w[12]), inv(w[22])), and_(inv(w[26]), inv(c2)))
  return and_(inv(c1), or_(A, and1(Bp, Bn)))
def w6_sums(SP, znq, zCB3, zNKZ, lid, B, need):
  b10 = and_(SP[7], zNKZ[8]); b11 = fa_carry2(SP[10], zNKZ[10], b10); b14 = and_(b11, zNKZ[12])
  b15 = fa_carry2(SP[14], zNKZ[14], b14); b16 = and_(b15, zNKZ[15]); b18 = and_(b16, zNKZ[17]); s18 = SP[18]
  b20 = xor(s18, or_(xor(s18, zNKZ[19]), and_(xor(s18, b18), xor(s18, zNKZ[18])))) if lid < 5 else xor(s18, and_(xor(s18, b18), and_(xor(s18, zNKZ[18]), xor(s18, zNKZ[19]))))
  b21 = fa_carry2(SP[20], zNKZ[20], b20); b22 = fa_carry2(SP[21], zNKZ[21], b21)
  b23 = fa_carry2(SP[22], zNKZ[22], b22); b24 = fa_carry2(SP[23], zNKZ[23], b23)
  b27 = and_(b24, zNKZ[25]); b29 = and_(b27, zNKZ[28]); A = [Z0] * 32
  for j in (2, 3, 15, 17, 21, 22, 23, 24):
    if not ((B >> j) & 1): A[j] = inv(and_(SP[j], znq[j]))
  if lid in (3, 4, 8, 9): t4 = and_(SP[4], znq[4]); A[4] = t4; A[5] = xor(SP[4], t4)
  elif lid in (2, 7): A[4] = inv(and_(SP[4], znq[4]))
  A[6] = and_(SP[6], znq[6]); t7 = and_(SP[7], znq[7]); A[7] = t7; A[8] = xor(SP[7], t7)
  t10 = and_(SP[10], znq[10]); A[10] = t10; x11 = xor(SP[10], t10); y11 = xor(b11, zNKZ[11])
  A[11] = xor(x11, y11); A[12] = and_(x11, y11); A[16] = xor(b16, zNKZ[16])
  t19 = and_(s18, znq[19]); A[19] = inv(t19) if lid < 5 else t19; A[27] = b27; A[29] = inv(b29)
  B2 = {14: (inv(and_(SP[14], znq[14])), inv(b14)), 18: (inv(and_(s18, znq[18])), b18), 20: (inv(and_(SP[20], znq[20])), inv(b20))}
  out = [None] * 32; top = max(need) if need is not None else 31; c = Z0; c2 = Z0
  for j in range(1, top + 1):
    ns = (need is None) or (j in need); nc = (j < top)
    if j in B2:
      s1, ca = fa_step2(B2[j][0], B2[j][1], c, True, nc); out[j], c2 = fa_step2(s1, zCB3[j], c2, ns, nc); c = ca
    elif c2.c == 0: out[j], c = fa_step2(A[j], zCB3[j], c, ns, nc)
    elif A[j].c == 0: out[j], c = fa_step2(c2, zCB3[j], c, ns, nc); c2 = Z0
    else:
      s1, ca = fa_step2(A[j], c2, c, True, nc); out[j], c2 = fa_step2(s1, zCB3[j], Z0, ns, nc); c = ca
  return out
def f6_ok_upper(w8, w9, w10, w14, w15, w16, w18, w19, w20, w25, w26, w27, w29, w30, w31):
  u1 = xor(w14, w18); u2 = or_(xor(w15, w19), inv(xor(w9, w26)))
  u3 = or_(xor(xor(w16, w20), w31), inv(xor(xor(w10, w27), w31)))
  return and_(xor(w8, w25), inv(or_(u1, and1(w29, or_(u2, and_(w30, u3))))))
def f6_combine_pre(m, w1, w2, w3, w12, w13, w14_31, w29, w30):
  bad_lo = or_(xor(w1, w12), and1(w29, or_(xor(w2, w13), and_(w30, xor(w3, w14_31)))))
  return and_(m, inv(bad_lo))
def borrow_step(wj, c, next_f): return (or1(wj, c) if next_f else or_(wj, c)) if wj.f != c.f else or_(wj, c)
def w6_batch(SP, znq, zCB3, zNKZ, lid, B, full=False):
  W = w6_sums(SP, znq, zCB3, zNKZ, lid, B, set(range(1, 32)) if full else set(NEEDW))
  m0 = f6_ok_upper(W[8], W[9], W[10], W[14], W[15], W[16], W[18], W[19], W[20], W[25], W[26], W[27], W[29], W[30], W[31])
  w14_31_0 = xor(W[14], W[31]); p0 = f6_combine_pre(m0, W[1], W[2], W[3], W[12], W[13], w14_31_0, W[29], W[30])
  if not full: return p0, None
  W1 = {}
  if B == 0x1: W1[1] = inv(W[1]); c = W[1]; start_j = 2
  else: c = W[4]; start_j = 5
  for j in range(start_j, 32):
    if j in NEEDW: W1[j] = xor(inv(W[j]), c)
    if j < 31: c = borrow_step(W[j], c, W[j + 1].f)
  m1 = f6_ok_upper(W1[8], W1[9], W1[10], W1[14], W1[15], W1[16], W1[18], W1[19], W1[20], W1[25], W1[26], W1[27], W1[29], W1[30], W1[31])
  w14_31_1 = xor(W1[14], W1[31])
  st = (m1, W1[1], W1[2], W1[3], W1[12], W1[13], w14_31_1, W1[29], W1[30]) if B == 0x1 else (W[1], W[2], W[3], m0, W[12], W[13], w14_31_0, W[29], W[30], m1, W1[12], W1[13], w14_31_1, W1[29], W1[30])
  return p0, st
def f6_sub(state, cu):
  if len(state) == 9: return f6_combine_pre(*state)
  (W1_0, W2_0, W3_0, m0, W12_0, W13_0, w14_31_0, W29_0, W30_0, m1, W12_1, W13_1, w14_31_1, W29_1, W30_1) = state
  b0, b2, b3 = cu & 1, (cu >> 2) & 1, (cu >> 3) & 1
  if b0 == 0:
    w1 = W1_0; w2 = W2_0 if b2 == 0 else inv(W2_0)
    if b2 == 0: w3 = inv(W3_0); c4 = W3_0
    elif b3 == 0: w3 = xor(inv(W3_0), W2_0); c4 = or_(W2_0, W3_0)
    else: w3 = xor(W3_0, W2_0); c4 = and_(W2_0, W3_0)
  else:
    w1 = inv(W1_0); c2 = W1_0
    if b2 == 0: w2 = xor(inv(W2_0), c2); c3 = or1(W2_0, c2) if (b3 == 1 and W2_0.f != c2.f) else or_(W2_0, c2)
    else: w2 = xor(W2_0, c2); c3 = and_(W2_0, c2)
    if b3 == 0: w3 = xor(inv(W3_0), c3); c4 = or_(W3_0, c3)
    else: w3 = xor(W3_0, c3); c4 = and_(W3_0, c3)
  return sel(c4, f6_combine_pre(m0, w1, w2, w3, W12_0, W13_0, w14_31_0, W29_0, W30_0), f6_combine_pre(m1, w1, w2, w3, W12_1, W13_1, w14_31_1, W29_1, W30_1))
def measure_ops():
  r = random.Random(7); w6 = {}; sub_ = {}
  znq = {j: (dyn(r.getrandbits(256)) if (MASK17 >> j) & 1 else Z0) for j in range(32)}
  zC = scal(r.getrandbits(32)); zK = {j: dyn(r.getrandbits(256)) for j in KZB}
  for k, cube, lid in ((3, 0xd, 0), (1, 0x1, 7)):
    SP = {j: (Z0 if (cube >> j) & 1 else dyn(r.getrandbits(256))) for j in MB_S}
    if not ((LMASK[lid] >> 4) & 1): SP[4] = Z0
    for full in (False, True):
      CN.n = 0; p, st = w6_batch(SP, znq, zC, zK, lid, cube, full); w6[(k, full)] = CN.n + (1 if p.f else 0)
    for cu in (1, 4, 5, 8, 9, 12, 13):
      if cu & ~cube: continue
      CN.n = 0; p = f6_sub(st, cu); sub_[(k, cu)] = CN.n + (1 if p.f else 0)
  C7 = [dyn(r.getrandbits(256)) if j in C7_DYN_BITS else Z0 for j in range(32)]
  CN.n = 0; W = add(C7, scal(r.getrandbits(32)), need=set(NEEDF7)); p = f7_test({j: W[j] for j in NEEDF7}); f7 = CN.n + (1 if p.f else 0)
  return w6, sub_, f7
W6_OPS, SUBF_OPS, F7_OPS = measure_ops()

# ---- prices of the stages (every one is the number of primitives of the straight-line text; see proof.md Section 9) ----
CTRL_FB = 16
PARTCH = [(0, 13), (13, 13), (26, 13), (39, 13), (52, 12)]
def part_fixed(r): return (1 if r in (0, 3) else 2) + sum((1 if k in (0, 4) else 2) + 1 for k in range(5))
SCAN_FIX = sum(part_fixed(r) for r in range(4))
SCAN_LANE = 8
CLS_LANE = 6
EXTR = (1, 2, 2, 1)
PLACE = 7
GROUP_BODY = 31
PROBE = (11, 12, 12, 12)
SURV_FIX, SURV_LANE, EX_OPS = 8, 7, 34
ZLOADS = len(MB_NZ) + len(KZB) + len(ZC)
SWEEP_OVH = 3 + 2 * ZLOADS
CUBE_CAND = (0, 2, 3)
def sp_loads(k): return 2 * (len(MB_S) - k) + 2
RUN_CU = 7
SPILL_K = {3: 30, 1: 18}      # 15 spilled planes (30 ops) for k = 3, 9 spilled planes (18 ops) for k = 1
CF_CLASS = 8
CUBE_D = {c: c | (S0(c) << 32) for c in range(16) if c & ~0xd == 0}
def cprep_ops(): return 10 + 14 + bgen(ZC) + bgen(KZB) + 2 * (len(ZC) + len(KZB)) + 1
FB_DET = 2 + 1 + 1 + 1 + 2 + 2 + bgen(MB_NZ) + 2 * len(MB_NZ) - 1 + 81
CT_DET = 2 + bgen(range(32)) + (2 * len(C7_DYN_BITS) - 1) + F7_OPS + 1 + SCAN_FIX
FIXED = 30 + CTRL_FB + FB_DET + CT_DET
RARE_LOOKUP, RECOMP, ROWCHECK, ROWCOMP = 2, 35, 53, 106
PAD_OPS = 7

# ---- the lists, classes, tables ----
def S0pack(a0): return a0 | ((~S0(a0) & M32) << 32)
def entry_of(s): return s | (S0(s) << 32)
REP_ORDER = {
  0: [19, 10, 20, 7, 4, 18, 22, 17, 15, 6, 21, 23, 14, 24],
  1: [10, 18, 20, 22, 17, 15, 7, 23, 24, 6, 4, 14, 19, 21],
  2: [24, 10, 20, 6, 21, 14, 7, 19, 17, 18, 22, 3, 15, 23, 2, 4],
  3: [24, 10, 20, 6, 21, 14, 7, 19, 17, 18, 22, 3, 15, 23, 2, 4],
  4: [4, 19, 14, 2, 10, 6, 3, 22, 15, 24, 17, 18, 23, 20, 21, 7],
  5: [19, 15, 24, 6, 4, 23, 7, 14, 17, 18, 10, 20, 22, 21],
  6: [10, 22, 21, 20, 19, 15, 17, 14, 18, 6, 4, 23, 24, 7],
  7: [6, 18, 4, 17, 10, 20, 22, 2, 23, 19, 14, 7, 21, 15, 24, 3],
  8: [19, 18, 4, 20, 6, 2, 7, 10, 14, 23, 22, 21, 17, 24, 3, 15],
  9: [19, 6, 17, 20, 10, 7, 24, 18, 22, 4, 14, 3, 2, 23, 21, 15],
}
def plane_pat(P): return tuple((p.c if p.c is not None else 2) for p in P)
class ListData:
  def __init__(self, mask, s, lid=None, order=None):
    Ss = set(s); self.cube = sum(1 << b for b in CUBE_CAND if all((t ^ (1 << b)) in Ss for t in s))
    self.mask = mask; self.s = s; self.n = len(s); self.k = bin(self.cube).count('1'); self.lid = lid
    self.spill = SPILL_K[self.k]
    reps = [t for t in s if not t & self.cube]; assert len(reps) << self.k == self.n
    order = order if order is not None else REP_ORDER.get(lid)
    if order: reps.sort(key=lambda t: tuple((t >> j) & 1 for j in order))
    self.reps = reps; self.nr = len(reps); self.nb = (self.nr + 255) // 256; self.nl = [min(256, self.nr - 256 * b) for b in range(self.nb)]
    self.planes = []; self.words = []; self.pat = []
    for b in range(self.nb):
      lanes = [reps[256 * b + L] if L < self.nl[b] else reps[256 * b] for L in range(256)]
      pv = planes_from_values(lanes); P = {}
      for j in MB_S:
        if (self.cube >> j) & 1: continue
        P[j] = Z0 if pv[j] == 0 else (Z1 if pv[j] == ONE else dyn(pv[j]))
      self.planes.append(P); self.pat.append(plane_pat([P[j] for j in sorted(P)]))
      self.words.append([sum(entry_of(lanes[64 * r + i]) << (64 * r) for r in range(4)) for i in range(64)])
    self.dyn = [sum(1 for j in P if P[j].c is None) for P in self.planes]
    self.measure()
  def zq_need(self, b):
    u = {j for j, p in self.planes[b].items() if p.c != 0}
    if self.planes[b][18].c != 0: u.add(19)
    return u
  def swp(self, sw):
    u = set()
    for b in (2 * sw, 2 * sw + 1):
      if b < self.nb: u |= self.zq_need(b)
    return 3 + 2 * (len(u) + len(KZB) + len(ZC))
  def spl(self, b): return 2 * self.dyn[b] + 2
  def measure(self):
    r = random.Random(7); self.w6 = {}; self.sub = {}; self.keys = {}; self.w6f = {}; self.subf = {}
    znq = {j: (dyn(r.getrandbits(256)) if (MASK17 >> j) & 1 else Z0) for j in range(32)}
    zC = scal(r.getrandbits(32)); zK = {j: dyn(r.getrandbits(256)) for j in KZB}
    for b in range(self.nb):
      SP = dict(self.planes[b]); SP.update({bb: Z0 for bb in CUBE_CAND if (self.cube >> bb) & 1})
      for full in (False, True):
        CN.n = 0; CN.flips = 0; p, st = w6_batch(SP, znq, zC, zK, self.lid, self.cube, full)
        self.w6[(b, full)] = CN.n + (1 if p.f else 0); self.w6f[(b, full)] = CN.flips; self.keys[(self.pat[b], full, None)] = self.w6[(b, full)]
        if full:
          for cu in (1, 4, 5, 8, 9, 12, 13):
            if cu & ~self.cube: continue
            CN.n = 0; CN.flips = 0; p = f6_sub(st, cu)
            self.sub[(b, cu)] = CN.n + (1 if p.f else 0); self.subf[(b, cu)] = CN.flips; self.keys[(self.pat[b], True, cu)] = self.sub[(b, cu)]

class Env:
  def __init__(self):
    self.Lt = setup_l(); self.lid = [int(c) for c in LISTID]; self.lists = {}; self.rep = {}
    self.cls = [dict(c7=c7, base=base, mask=mask, n=n, lid=self.lid[ci], BP=S0pack(base)) for ci, (c7, base, mask, n) in enumerate(CLASSES)]
    for ci, l in enumerate(self.lid): self.rep.setdefault(l, ci)
    c7s = [c['c7'] for c in self.cls]
    pv = planes_from_values(c7s + [c7s[0]] * (256 - NCLS))
    self.C7 = [Z0 if pv[j] in (0, ONE) else dyn(pv[j]) for j in range(32)]
    assert [j for j in range(32) if self.C7[j].c is None] == C7_DYN_BITS
    assert sum(1 << j for j in range(32) if pv[j] == ONE) == C7_CONST
    self.build_r16()
  def getlist(self, lid):
    if lid not in self.lists:
      c7, base, mask, n = CLASSES[self.rep[lid]]; self.lists[lid] = ListData(mask, sorted(a ^ base for a in class_members(c7, base, mask)), lid)
    return self.lists[lid]
  def members(self, ci): return [self.cls[ci]['base'] | s for s in self.getlist(self.lid[ci]).s]
  def memset(self, ci):
    if not hasattr(self, 'ms'): self.ms = {}
    if ci not in self.ms: self.ms[ci] = set(self.members(ci))
    return self.ms[ci]
  def build_r16(self):
    self.LC = {}; self.VA = {}
    for l in FEASIBLE_L:
      L = self.Lt[l]; tx = L['tx']; a12, a13, a14, a15 = (tx[0][i] for i in (12, 13, 14, 15))
      self.LC[l] = dict(C=L['C16'], cxA=(-a12 + S0(a15) + MAJ(a15, a14, a13)) & M32, Ex15=tx[1][15], Ax15=a15)
      self.VA[l] = 0x20000000 | ((~a15) & 0x8000) | (a15 & 0x00800000) | (a15 & 0x02000000)
    ML, VL, MM, VM = E16M & 0xfff, E16V & 0xfff, (E16M >> 12) & 0xfff, (E16V >> 12) & 0xfff
    LOp = [0] * 4096; LOc = [0] * 4096; MID0 = [0] * 4096; MID1 = [0] * 4096
    for l in FEASIBLE_L:
      c = self.LC[l]; Clo = c['C'] & 0xfff; Cmid = (c['C'] >> 12) & 0xfff
      for lo in range(4096):
        t = lo + Clo; el = t & 0xfff
        if (el & ML) == VL and not ((el ^ c['Ex15']) & 0x10): LOp[lo] |= 1 << l
        if t >> 12: LOc[lo] |= 1 << l
      for mid in range(4096):
        for cin, T in ((0, MID0), (1, MID1)):
          if (((mid + Cmid + cin) & 0xfff) & MM) == VM: T[mid] |= 1 << l
    self.LOw = [LOp[i] | ((LOp[i] & LOc[i]) << 64) for i in range(4096)]; self.MIDw = [MID0[i] | ((MID0[i] ^ MID1[i]) << 64) for i in range(4096)]
  def filt(self, u):
    T = self.LOw[u & 0xfff] & self.MIDw[(u >> 12) & 0xfff]
    return (T ^ (T >> 64)) & M32
  def exact(self, u, l):
    c = self.LC[l]; e = (u + c['C']) & M32; A = (e + c['cxA']) & M32
    t = ((e & E16M) ^ E16V) | ((e ^ c['Ex15']) & 0x10) | ((A & 0x22808000) ^ self.VA[l])
    x1, x2, x3 = A ^ (A >> 11), A ^ (A >> 12), A ^ (A >> 9)
    return (t | (((x1 & 0x200) | (x2 & 0x40) | (x3 & 0x100)) ^ 0x240)) == 0, EX_OPS
def r16_ref(Env_, u, l):
  e = (Env_.LC[l]['C'] + u) & M32
  return (e & E16M) == E16V and row16_ok(Env_.Lt[l], e)

# ---- the counted online program ----
class Mc:
  def __init__(self): self.n = 0; self.cat = {}; self.cnt = {}
  def add(self, c, k): self.n += k; self.cat[c] = self.cat.get(c, 0) + k
  def count(self, c, k=1): self.cnt[c] = self.cnt.get(c, 0) + k
def scan_parts(mc, cat, plane, per_lane):
  out = []
  for r in range(4):
    part = (plane >> (64 * r)) & M64
    for (sh, w) in PARTCH:
      c = (part >> sh) & ((1 << w) - 1)
      while c: out.append((r, sh + (c & -c).bit_length() - 1)); c &= c - 1
  mc.add(cat, SCAN_FIX + per_lane * len(out)); return out
def packed_u(Gw, pre):
  Sw = Gw >> 32; E0 = (Gw + bc(pre['e0b'])) & LM; mj = Gw & bc(pre['x12']); ch = (E0 & bc(pre['X'])) ^ bc(pre['Em2'])
  d = (E0 | (E0 << 32)) & M256; S1E = (((d >> 6) ^ (d >> 11)) ^ (d >> 25)) & LM
  W1 = (sum((pre['kap1'] + 1 + (3 << 32)) << (64 * k) for k in range(4)) + Sw - mj - S1E - ch) & LM
  d1 = (W1 | (W1 << 32)) & M256; s0W = (((d1 >> 7) ^ (d1 >> 18)) ^ (W1 >> 3)) & LM
  U = (E0 + s0W + bc64(pre['C'])) & M256
  for k in range(4): assert (U >> (64 * k)) & M64 < 3 << 32
  return U
def process_cv(mc, cv, env, stats, check=None, only=None):
  found = []; x, am2 = cv[0], cv[1]
  mc.add('ct', 2 + bgen(range(32)) + (2 * len(C7_DYN_BITS) - 1))
  CN.n = 0; W = add(env.C7, scal((C7_CONST - x) & M32), need=set(NEEDF7)); p = f7_test({j: W[j] for j in NEEDF7}); assert CN.n + (1 if p.f else 0) == F7_OPS
  mc.add('ct', F7_OPS + 1); plane = force(p).v & ((1 << NCLS) - 1)
  if check: check('classes', cv, None, plane)
  if only is not None: plane &= sum(1 << c for c in only); mc.add('ct', 1)
  cls = [64 * r + i for (r, i) in scan_parts(mc, 'ct', plane, CLS_LANE)]
  stats['classes'] = stats.get('classes', 0) + len(cls)
  cb = (C6 - am2) & M32; q = A1 ^ x; q_eff = A1_EFF ^ x; CB2 = (cb + (A1 & x)) & M32; KXA = (K3C - AA + x) & M32
  mc.add('fb', FB_DET)
  znq = {j: (dyn(ONE if (q_eff >> j) & 1 else 0) if (MASK17 >> j) & 1 else Z0) for j in range(32)}
  pre = cv_pre(Mach(), cv); reg = []; gset = set(); stats['goodset'] = gset
  def run_group(grp):
    Gw = 0
    for k in range(4): Gw |= grp[k][0] << (64 * k)
    U = packed_u(Gw, pre); mc.add('group', GROUP_BODY); mc.count('groups')
    for k in range(4):
      mc.add('probe', PROBE[k]); u = (U >> (64 * k)) & M32; G = env.filt(u)
      if check: check('filt', cv, (grp[k], u), G)
      if not G: continue
      mc.add('surv', SURV_FIX); mc.count('survlanes'); ls = []
      for l in FEASIBLE_L:
        if (G >> l) & 1:
          ok, ops = env.exact(u, l); mc.add('surv', SURV_LANE + ops); mc.count('survl')
          if ok: ls.append(l)
      if ls:
        a0 = grp[k][0] & M32; stats['r16'] = stats.get('r16', 0) + 1; mc.add('rare', 1 + RARE_LOOKUP)
        w6, w7 = recompute_w67(Mach(), a0, x, am2); mc.add('rare', RECOMP)
        r = step3b(mc, cv, a0, w6, w7, ls, env.Lt)
        if r: found.append((a0, r))
  def place(e, ci):
    reg.append((e, ci, 0)); stats['pairs'] = stats.get('pairs', 0) + 1
    if check: gset.add((ci, e & M32))
    if len(reg) == 4: run_group(list(reg)); reg.clear()
  for ci in cls:
    c = env.cls[ci]; lid = c['lid']; lst = env.getlist(lid); base = c['base']; B = lst.cube
    KZ = (KXA - (base & FA)) & M32; CB3 = CB3_of(CB2, base, q, KZ, lid, B)
    mc.add('cprep', cprep_ops() + CF_CLASS); mc.count('cls_l%d' % lid); zCB3 = scal(CB3); zNKZ = make_zNKZ(KZ)
    I = (q & B) | (CB3 & 1); Q0 = B ^ I; m = 1 << bin(I).count('1'); full = Q0 != 0; wst = {}
    def gather(pv, cu, nl, b):
      BPc = c['BP'] ^ CUBE_D[cu]; mc.count('planes')
      for (r, i) in scan_parts(mc, 'scan', pv, SCAN_LANE):
        e = ((lst.words[b][i] >> (64 * r)) & M64) ^ BPc; mc.count('rep_r%d_m%d' % (r, m))
        if not I: mc.add('member', EXTR[r] + PLACE); place(e, ci)
        else:
          mc.add('member', EXTR[r] + 12 * m - 2); place(e, ci); ii = 0
          while True:
            ii = (ii - I) & I
            if not ii: break
            place(e ^ CUBE_D[ii], ci)
    for sw in range((lst.nb + 1) // 2):
      mc.add('sweep', lst.swp(sw)); mc.count('sweeps'); mc.count('swp_%d_%d' % (lid, sw))
      for b in [b for b in (2 * sw, 2 * sw + 1) if b < lst.nb]:
        mc.add('sweep', lst.spl(b)); mc.count('mb_%d_%d_%d' % (lid, b, full)); SP = dict(lst.planes[b]); SP.update({bb: Z0 for bb in CUBE_CAND if (B >> bb) & 1})
        CN.n = 0; p, st = w6_batch(SP, znq, zCB3, zNKZ, lid, B, full); assert CN.n + (1 if p.f else 0) == lst.w6[(b, full)]
        mc.add('w6', lst.w6[(b, full)]); pv = force(p).v
        if lst.nl[b] < 256: pv &= (1 << lst.nl[b]) - 1; mc.add('w6', 1); mc.count('partial')
        if full: wst[b] = st; mc.add('spill', lst.spill); mc.count('spills')
        if check: check('plane', cv, (ci, b, 0), pv)
        mc.count('runs_l%d' % lid); gather(pv, 0, lst.nl[b], b)
    if full:
      for b in range(lst.nb):
        mc.add('spill', lst.spill); mc.count('spills'); cu = 0
        while True:
          cu = (cu - Q0) & Q0
          if not cu: break
          mc.add('runs', RUN_CU); mc.count('sb_%d_%d_%d' % (lid, b, cu)); CN.n = 0; p = f6_sub(wst[b], cu); assert CN.n + (1 if p.f else 0) == lst.sub[(b, cu)]
          mc.add('w6', lst.sub[(b, cu)]); pv = force(p).v
          if lst.nl[b] < 256: pv &= (1 << lst.nl[b]) - 1; mc.add('w6', 1); mc.count('partial')
          if check: check('plane', cv, (ci, b, cu), pv)
          mc.count('runs_l%d' % lid); gather(pv, cu, lst.nl[b], b)
  if reg:
    mc.add('member', PAD_OPS); mc.count('pad', 4 - len(reg)); grp = reg + [reg[-1]] * (4 - len(reg)); run_group(grp); reg.clear()
  return found

# ---- reference computations used by the organizer experiments and the self-test ----
def u_ref(cv, a0):
  Ar = {-1: cv[0], -2: cv[1], -3: cv[2], -4: cv[3], 0: a0}; Er = {-1: cv[4], -2: cv[5], -3: cv[6], -4: cv[7]}
  Er[0] = (Ar[0] + Ar[-4] - S0(Ar[-1]) - MAJ(Ar[-1], Ar[-2], Ar[-3])) & M32
  W0 = (Er[0] - Ar[-4] - Er[-4] - S1(Er[-1]) - CH(Er[-1], Er[-2], Er[-3]) - K[0]) & M32
  Er[1] = (A1 + Ar[-3] - S0(a0) - MAJ(a0, Ar[-1], Ar[-2])) & M32
  W1 = (Er[1] - Ar[-3] - Er[-3] - S1(Er[0]) - CH(Er[0], Er[-1], Er[-2]) - K[1]) & M32
  return (W0 + s0(W1)) & M32
def online_trial(rng, env, max_fb=64, sample=12, ncls=3, uncond_fb=64):
  bad = dict(cls=0, plane=0, goodset=0, addr=0, row16=0, cells=0); st = dict(); mc = Mc(); firstpair = []; nprobe = [0]
  def check(kind, cv, a, b):
    if kind == 'classes':
      for c in range(NCLS): bad['cls'] += ((b >> c) & 1) != int(F7((env.cls[c]['c7'] - cv[0]) & M32))
      bad['cls'] += (b >> NCLS) != 0
    elif kind == 'plane':
      ci, bi, cc = a; lst = env.getlist(env.cls[ci]['lid']); base = env.cls[ci]['base']
      for L in range(256):
        want = int(F6(w6of(base | lst.reps[256 * bi + L] | cc, cv[0], cv[1]))) if L < lst.nl[bi] else 0
        bad['plane'] += ((b >> L) & 1) != want
    else:
      (ent, ci, idx), u = a; G = b; a0 = ent & M32; nprobe[0] += 1
      bad['addr'] += u != u_ref(cv, a0) or a0 not in env.memset(ci)
      if G or nprobe[0] % 16 == 0:
        for l in FEASIBLE_L:
          r = r16_ref(env, u, l); bad['row16'] += (r and not (G >> l) & 1) or env.exact(u, l)[0] != r
  for f in range(max_fb):
    w = first_block(Mach(), rng); cv = compress(IV, w); st['fb'] = st.get('fb', 0) + 1; mc.add('fixed', 30 + CTRL_FB)
    pc = [c for c in range(NCLS) if F7((env.cls[c]['c7'] - cv[0]) & M32)]
    if not pc: mc.add('fixed', FB_DET + CT_DET); continue
    use = pc[:ncls]; st['m0'] = w
    found = process_cv(mc, cv, env, st, check, use)
    want = {(c, a0) for c in use for a0 in env.members(c) if F6(w6of(a0, cv[0], cv[1]))}
    got = st['goodset']; bad['goodset'] += want != got
    for (c, a0) in sorted(got)[:2]:
      wx, wy = words_from_cv(cv, a0)
      if not (inF(wx[7], D7, T7) and inF(wx[6], D6, T6) and F7((c7of(a0) - cv[0]) & M32)): bad['cells'] += 1
      if len(firstpair) < sample:
        for l in range(32):
          (x14, x15), (y14, y15) = lstar(l); tx = trace(cv, wx + [x14, x15], 16); ty = trace(cv, wy + [y14, y15], 16)
          if not all(row_ok(tx, ty, i, i not in (6, 7)) for i in range(-4, 16)): bad['cells'] += 1
        firstpair.append((wx, wy))
    break
  uncond_passes = 0
  for _ in range(uncond_fb):
    w = first_block(Mach(), rng); cv = compress(IV, w)
    W = add(env.C7, scal((C7_CONST - cv[0]) & M32), need=set(NEEDF7)); plane = force(f7_test({j: W[j] for j in NEEDF7})).v & ((1 << NCLS) - 1)
    check('classes', cv, None, plane); uncond_passes += bin(plane).count('1')
  q3_lz, q3_ps, q3_r16x = q3_smc_check(rng, env)
  if firstpair: firstpair[0] = (st['m0'],) + firstpair[0]
  obs = dict(uncond_first_blocks=uncond_fb, uncond_class_passes=uncond_passes, first_blocks=st.get('fb', 0), classes=st.get('classes', 0), good_pairs=st.get('pairs', 0),
       groups=mc.cnt.get('groups', 0), survivors=mc.cnt.get('survl', 0), row16_pairs=st.get('r16', 0), counted_ops=mc.n, class_lane_mismatches=bad['cls'],
       pass_lane_mismatches=bad['plane'], goodset_mismatches=bad['goodset'], address_mismatches=bad['addr'], row16_mismatches=int(bad['row16']),
       cell_mismatches=bad['cells'], pairs_cell_checked=len(firstpair), q3_log2_est=q3_lz, q3_full_passes=q3_ps, q3_r16x_passes=q3_r16x)
  return (firstpair[0] if firstpair else None), obs
def q3_smc_check(rng, env, NP=48):
  P, (m16, v16, _, _) = [], CELLS['E'][16]
  while len(P) < NP:
    Ld = env.Lt[rng.below(32)]; X, Y = new_rows(Ld['tx'], Ld['ty'])
    dW = (s1(Y[2][14]) - s1(X[2][14]) + Y[2][9] - X[2][9]) & M32
    base = (X[0][12] + X[1][12] + S1(X[1][15]) + CH(X[1][15], X[1][14], X[1][13]) + K[16]) & M32
    while True:
      X[2][16] = (((rng() & M32) & ~m16 | v16) - base) & M32; Y[2][16] = (X[2][16] + dW) & M32; step_rows(X, Y, 16)
      if row_ok(X, Y, 16) and x2_ok(X, 16): P.append((X, Y)); break
  lsum, M_st = -16.0, {17: 24, 18: 24, 19: 16, 20: 8, 21: 8, 22: 384}
  mw22, vw22, _, _ = CELLS['W'][22]; w22_m = mw22 | 3 | (1 << 25) | (1 << 21); lz22_w = math.log2((1 << 24) / 287309824.0)
  for t in range(17, 23):
    chl, M_t = [], M_st[t]
    if t <= 21:
      m0, v0, _, _ = CELLS['E'][t]; w_log2 = -(bin(m0).count('1') + (1 if t in (17, 19) else (5 if t == 18 else 0)))
      for X, Y in P:
        e23 = (X[1][16] >> 23) & 1; dW = (s1(Y[2][t-2]) - s1(X[2][t-2]) + Y[2][t-7] - X[2][t-7] + (T6 if t == 21 else 0)) & M32
        base = (X[0][t-4] + X[1][t-4] + S1(X[1][t-1]) + CH(X[1][t-1], X[1][t-2], X[1][t-3]) + K[t]) & M32
        for _ in range(M_t):
          m, v = m0, v0
          if t == 17: m |= 1 << 24; v |= (((X[1][16] >> 24) & 1) ^ e23) << 24
          elif t == 18: pat = (4 if e23 else 0) + (rng() & 3); m |= IMP[18][0]; v |= IMP[18][1] ^ PAT[pat][0]
          elif t == 19: m |= 1 << 29; v |= ((X[1][18] >> 10) & 1) << 29
          wx = (((rng() & M32) & ~m | v) - base) & M32; wy = (wx + dW) & M32; X[2][t], Y[2][t] = wx, wy; step_rows(X, Y, t)
          if row_ok(X, Y, t) and x2_ok(X, t): chl.append((X, Y, wx, wy))
    else:
      w_log2 = lz22_w
      for X, Y in P:
        s1x, w15x, s1y, w15y = s1(X[2][20]), X[2][15], s1(Y[2][20]), Y[2][15]
        for _ in range(M_t):
          r = (rng() & M32 & ~w22_m) | vw22
          w22 = r | ((1 - ((r >> 31) & 1)) << 1) | (1 - ((r >> 30) & 1)) | ((1 - ((r >> 16) & 1)) << 25) | ((1 - ((r >> 14) & 1)) << 21)
          w7 = draw_F7(rng); w6 = (w22 - s1x - w15x - s0(w7)) & M32
          if not inF(w6, D6, T6): continue
          X[2][6], Y[2][6], X[2][7], Y[2][7] = w6, (w6 + D6) & M32, w7, (w7 + D7) & M32
          X[2][22], Y[2][22] = w22, (s1y + w15y + s0(Y[2][7]) + Y[2][6]) & M32; step_rows(X, Y, 22)
          if row_ok(X, Y, 22) and x2_ok(X, 22): chl.append((X, Y, w6, w7))
    if not chl: return -99.0, 0, 0
    lsum += math.log2(len(chl)) + w_log2 - math.log2(NP * M_t); Q = []
    for _ in range(NP):
      Xp, Yp, a, b = chl[rng.below(len(chl))]; Xc, Yc = [dict(d) for d in Xp], [dict(d) for d in Yp]
      if t <= 21: Xc[2][t], Yc[2][t] = a, b; step_rows(Xc, Yc, t)
      else:
        Xc[2][6], Yc[2][6], Xc[2][7], Yc[2][7] = a, (a + D6) & M32, b, (b + D7) & M32
        Xc[2][22], Yc[2][22] = (s1(Xc[2][20]) + Xc[2][15] + s0(b) + a) & M32, (s1(Yc[2][20]) + Yc[2][15] + s0(Yc[2][7]) + Yc[2][6]) & M32
        step_rows(Xc, Yc, 22)
      Q.append((Xc, Yc))
    P = Q
  passes = r16x = 0; MT = 64; mw24, vw24, dw24, _ = CELLS['W'][24]
  for X, Y in P:
    Zx, Zy = (s1(X[2][22]) + X[2][17] + s0(X[2][9])) & M32, (s1(Y[2][22]) + Y[2][17] + s0(Y[2][9])) & M32
    for _ in range(MT):
      while True:
        c, idx = rng.below(NCLS), rng.below(3600)
        if idx < CLASSES[c][3]: a0 = env.members(c)[idx]; break
      w8x = (W8C - ((a0 + C4) & M32)) & M32; wx24, wy24 = (Zx + w8x) & M32, (Zy + w8x + D8) & M32
      if (wx24 & mw24) != vw24 or (wx24 ^ wy24) != dw24 or not (((wx24 >> 16) ^ (wx24 >> 25)) & 1) or not (((wx24 >> 18) ^ (wx24 >> 29)) & 1): continue
      Xc, Yc = [dict(d) for d in X], [dict(d) for d in Y]; Xc[2][8], Yc[2][8] = w8x, (w8x + D8) & M32; ok = True
      for r in range(23, R):
        for (_, _, W_) in (Xc, Yc): W_[r] = (s1(W_[r-2]) + W_[r-7] + s0(W_[r-15]) + W_[r-16]) & M32
        step_rows(Xc, Yc, r)
        if not (row_ok(Xc, Yc, r) and x2_ok(Xc, r)): ok = False; break
      if ok: passes += 1; r16x += bool(((Xc[1][16] >> 23) & 1) or (((Xc[1][16] ^ Xc[1][17]) >> 24) & 1))
  return (-99.0, 0, 0) if not passes else (round(lsum + math.log2(passes) - math.log2(NP * MT), 4), passes, r16x)
def detect(env, cv, mx, my, c, a0):
  mc = Mc(); st = dict(); fnd = process_cv(mc, cv, env, st, None, [c])
  return int(any(f[0] == a0 and f[1][1] == mx and f[1][2] == my for f in fnd)), mc.n
def run_request(req):
  env = Env(); eid = req['experiment_id']; out = []
  for tr in req['trials']:
    t = tr['trial']; rng = Shake(eid + '|' + tr['seed']); rec = dict(trial=t, message_a_hex=None, message_b_hex=None)
    if eid.startswith('a0-sfs') and t < 128:
      r = sfs_trial(rng, env.Lt, (7 * t) % NCLS, env, pat=t % 8)
      if r:
        cv, mx, my, obs = r
        if t < 16:
          a0v = env.members(obs['class_index'])[obs['variant_index']]
          obs['detected_by_counted_program'], obs['counted_ops'] = detect(env, cv, mx, my, obs['class_index'], a0v)
        rec['message_a_hex'] = struct.pack('>24I', *(cv + mx)).hex(); rec['message_b_hex'] = struct.pack('>24I', *(cv + my)).hex(); rec['observations'] = obs
    elif eid.startswith('a0-online') and t < 8:
      pair, obs = online_trial(rng, env); rec['observations'] = obs
      if pair and obs['class_lane_mismatches'] == obs['pass_lane_mismatches'] == obs['goodset_mismatches'] == obs['address_mismatches'] == obs['row16_mismatches'] == obs['cell_mismatches'] == 0:
        m0, wx, wy = pair; (x14, x15), (y14, y15) = lstar(13)
        rec['message_a_hex'] = struct.pack('>32I', *(m0 + wx + [x14, x15])).hex(); rec['message_b_hex'] = struct.pack('>32I', *(m0 + wy + [y14, y15])).hex()
    out.append(rec)
  return dict(schema_version=1, trials=out)

# ---- the ledger (exact rationals) ----
C_REF = 2644
P7 = Fr(68157440, 1 << 32); P6 = Fr(287309824, 1 << 32); R16F = Fr(2097152, 1 << 32)
NSURV = len(FEASIBLE_L); MU = Fr(NSURV, 256); PNZ = Fr(1521152, 1 << 24)
Q3_LOG2 = -71.47; PRE_OPS = 1 << 38; SLACK = Fr(1, 1 << 11); NVAR = sum(c[3] for c in CLASSES)
CLASS_TYPES = [(3456, 3, 85), (3456, 1, 26), (3600, 3, 85), (3584, 1, 26)]
def lane_costs(nls): return sum(SCAN_LANE + EXTR[L // 64] for nl in nls for L in range(nl))
def memcost(j): return PLACE if j == 0 else 12 * (1 << j) - 2
def subsets(mask): return [s for s in range(16) if s & ~mask == 0]
FLIPCOST = 0
_LISTS = {}
def LST(lid):
  if lid not in _LISTS:
    ci = LISTID.index(str(lid)); c7, base, mask, n = CLASSES[ci]; _LISTS[lid] = ListData(mask, sorted(a ^ base for a in class_members(c7, base, mask)), lid)
  return _LISTS[lid]
def lid_types(): return [(int(l), LISTID.count(l)) for l in sorted(set(LISTID))]
def class_det(lid, Q0):
  L = LST(lid); nb = L.nb; nsw = (nb + 1) // 2; part = 1 if L.nr % 256 else 0; full = Q0 != 0
  tot = cprep_ops() + CF_CLASS + sum(L.swp(sw) for sw in range(nsw)) + sum(L.spl(b) + L.w6[(b, full)] + FLIPCOST * L.w6f[(b, full)] + SCAN_FIX for b in range(nb)) + part
  if full:
    tot += 2 * nb * L.spill
    for cu in subsets(Q0):
      if cu: tot += sum(RUN_CU + L.sub[(b, cu)] + FLIPCOST * L.subf[(b, cu)] + SCAN_FIX for b in range(nb)) + part
  return tot
def class_run_cost(lid, Q0):
  L = LST(lid); j = L.k - bin(Q0).count('1')
  return lane_costs(L.nl) + L.nr * memcost(j)
def class_expected(lid):
  L = LST(lid); cube = {3: 0xd, 1: 0x1}[L.k]; tot = Fr(0)
  for Q0 in subsets(cube):
    w = Fr(1 if (Q0 & 1) else 3, 1 << (L.k + 1))
    tot += w * (class_det(lid, Q0) + (1 << bin(Q0).count('1')) * P6 * class_run_cost(lid, Q0))
  return tot
def class_max(lid):
  L = LST(lid); cube = {3: 0xd, 1: 0x1}[L.k]
  return max(class_det(lid, Q0) + (1 << bin(Q0).count('1')) * class_run_cost(lid, Q0) for Q0 in subsets(cube))
def expected():
  ct_var = CLS_LANE * NCLS * P7; perclass = pairs = Fr(0)
  for (lid, cnt) in lid_types():
    perclass += cnt * P7 * class_expected(lid); pairs += cnt * P7 * P6 * LST(lid).n
  groups = (pairs + 3) / 4; grp = groups * (GROUP_BODY + sum(PROBE)) + PAD_OPS; lanes = 4 * groups
  surv = lanes * (PNZ * SURV_FIX + MU * (SURV_LANE + EX_OPS))
  c3b_row = ROWCOMP + ROWCHECK + 1; c3b_pair = 201 + RECOMP + 1 + RARE_LOOKUP; c3b_l = 2 + 6 + 2 * c3b_row
  rare = lanes * R16F * (c3b_pair + c3b_l + 19 * Fr(1, 512) * c3b_row)
  return dict(ct_var=ct_var, perclass=perclass, grp=grp, surv=surv, rare=rare, g=pairs, vbar=ct_var + perclass + grp + surv + rare)
def vmax_fb_value():
  tot = Fr(0); c3b_row = ROWCOMP + ROWCHECK + 1; c3b_pair = 201 + RECOMP + 1 + RARE_LOOKUP; c3b_l = 2 + 6 + 2 * c3b_row
  for (lid, cnt) in lid_types(): tot += cnt * class_max(lid)
  lanes = NVAR + 3
  tot += Fr(lanes, 4) * (GROUP_BODY + sum(PROBE)) + PAD_OPS + lanes * (SURV_FIX + NSURV * (SURV_LANE + EX_OPS)) + lanes * Fr(11, 10) * (c3b_pair + NSURV * (c3b_l + 19 * c3b_row))
  return tot + 24 + CLS_LANE * NCLS
def ledger(q3_log2=Q3_LOG2, show=True, ac_log2=60, slack=SLACK, pre_ops=PRE_OPS):
  C = C_REF; ex = expected(); g, vbar = ex['g'], ex['vbar']; vmax_fb = vmax_fb_value()
  fl = math.floor(q3_log2); q3ex = Fr(2) ** fl * Fr(math.floor(2 ** (q3_log2 - fl) * 2 ** 40), 2 ** 40)
  getcontext().prec = 60
  def mu_req(pcap):
    x = Decimal('0.61') - Decimal(pcap.numerator) / Decimal(pcap.denominator) - Decimal(2) ** -60
    return Fr(int(math.floor(-x.ln() / (Decimal(1) - (Decimal(-10.4) * Decimal(2).ln()).exp()) * 10 ** 8)) + 1, 10 ** 8)
  pa = Fr(1, 1 << 24)
  for _ in range(8):
    XREQ = mu_req(pa); nfb = int(-(-XREQ // (g * 32 * q3ex))); pcap = Fr(vmax_fb) / (slack * slack * nfb * vbar); pa2 = Fr(math.ceil(pcap * 10 ** 8), 10 ** 8)
    if pa2 == pa: break
    pa = pa2
  assert pcap <= pa and XREQ >= mu_req(pa)
  VMAX = math.ceil((1 + slack) * nfb * vbar)
  T = Fr(2 ** ac_log2 + 2 ** 50 + 2 ** 40) + nfb + Fr(nfb * FIXED + VMAX + math.ceil(vmax_fb) + pre_ops + 1600, C) + 6
  tl = math.ceil(math.log2(T) * 1e5) / 1e5; p5 = int(round(tl * 100000))
  out = dict(g=float(g), vbar=float(vbar), fixed=FIXED, mu_req=float(XREQ), nfb=nfb, log2_nfb=math.log2(nfb), VMAX=VMAX, vmax_fb=float(vmax_fb), pcap_log2=math.log2(float(pcap)),
       time_log2=tl, log2_T=math.log2(T), T_num=T.numerator, T_den=T.denominator,
       tight_up=T.numerator ** 100000 <= (2 ** p5) * T.denominator ** 100000, tight_down=T.numerator ** 100000 > (2 ** (p5 - 1)) * T.denominator ** 100000,
       success_lower_bound=1 - math.exp(-(1 - 2.0 ** -10.4) * float(XREQ)) - float(pa) - 2.0 ** -60, pcap_assumed=pa,
       per_fb_units=float(1 + Fr(FIXED, C) + vbar / C), preprocessing_log2=math.log2(2 ** ac_log2 + 2 ** 50 + 2 ** 40 + Fr(pre_ops, C)), slack=str(slack),
       parts={k: float(v) for k, v in ex.items() if k not in ('g', 'vbar')})
  assert out['tight_up'] and out['tight_down'] and out['success_lower_bound'] > 0.39
  if show:
    for k, v in out.items(): print('%-18s %s' % (k, v))
  return out
def selftest():
  rr = random.Random(1); env = Env(); bad = 0
  tot = 0
  for ci in range(NCLS):
    c7, base, mask, n = CLASSES[ci]; mem = env.members(ci); tot += len(mem)
    bad += len(mem) != n or any((not in_G(a)) or c7of(a) != c7 or (a & mask) != (a ^ base) for a in mem)
  print('classes %d, variants %d (782,800), mismatches %d' % (NCLS, tot, bad))
  print('W6_OPS (k, full):', W6_OPS, 'SUBF_OPS:', SUBF_OPS, 'F7_OPS', F7_OPS, 'FIXED', FIXED)
  bad = 0
  for _ in range(20000): bad += not F7(draw_F7(Shake(str(rr.random()))))
  print('F7 sampler violations', bad)
  bad = sum(1 for ci in range(NCLS) if env.getlist(env.lid[ci]).cube & 12 and not env.cls[ci]['base'] & 2)
  ks = sorted(set((len(env.getlist(l).s), env.getlist(l).k) for l in set(env.lid)))
  print('lists (size, cube bits):', ks, ' classes with a cube bit 2 or 3 and base bit 1 clear:', bad)
  bad = tot = 0
  for ci in (0, 17, 40, 77, 111, 150, 200, 221):
    lid = env.lid[ci]; lst = env.getlist(lid); base = env.cls[ci]['base']; B = lst.cube
    for _ in range(60):
      x = rr.getrandbits(32); am2 = rr.getrandbits(32); cb = (C6 - am2) & M32; q = A1 ^ x
      CB2 = (cb + (A1 & x)) & M32; KZ = (K3C - AA + x - (base & FA)) & M32
      CB3 = CB3_of(CB2, base, q, KZ, lid, B)
      I = (q & B) | (CB3 & 1)
      for t_ in rr.sample(lst.reps, 8):
        for f in range(16):
          if f & ~B: continue
          tot += 1; bad += F6(w6of(base | t_ | f, x, am2)) != F6(w6of(base | t_ | (f & ~I), x, am2))
  print('invariance of F6(W6x) under the flips of the bits of I: %d checks, %d mismatches' % (tot, bad))
  bad = tot = ps = 0
  for ci in (0, 17, 40, 77, 111, 150, 200, 221):
    lid = env.lid[ci]; lst = env.getlist(lid); base = env.cls[ci]['base']; B = lst.cube
    for _ in range(3):
      x = rr.getrandbits(32); am2 = rr.getrandbits(32); cb = (C6 - am2) & M32; q = A1 ^ x; q_eff = A1_EFF ^ x
      znq = {j: (dyn(ONE if (q_eff >> j) & 1 else 0) if (MASK17 >> j) & 1 else Z0) for j in range(32)}
      CB2 = (cb + (A1 & x)) & M32; KZ = (K3C - AA + x - (base & FA)) & M32
      CB3 = CB3_of(CB2, base, q, KZ, lid, B)
      zC = scal(CB3); zK = make_zNKZ(KZ); I = (q & B) | (CB3 & 1); Q0 = B ^ I
      for b in range(lst.nb):
        SP = dict(lst.planes[b]); SP.update({bb: Z0 for bb in CUBE_CAND if (B >> bb) & 1})
        for full in (False, True):
          CN.n = 0; p, st = w6_batch(SP, znq, zC, zK, lid, B, full); assert CN.n + (1 if p.f else 0) == lst.w6[(b, full)]; pv = force(p).v
          for L in range(lst.nl[b]):
            e = F6(w6of(base | lst.reps[256 * b + L], x, am2)); tot += 1; ps += e; bad += e != bool((pv >> L) & 1)
        for cu in subsets(Q0):
          if not cu: continue
          CN.n = 0; p = f6_sub(st, cu); assert CN.n + (1 if p.f else 0) == lst.sub[(b, cu)]; pv = force(p).v
          for L in range(lst.nl[b]):
            e = F6(w6of(base | lst.reps[256 * b + L] | cu, x, am2)); tot += 1; ps += e; bad += e != bool((pv >> L) & 1)
  print('w6 plane lanes %d, F6 passes %d, mismatches %d' % (tot, ps, bad))
  bad = tot = 0
  for _ in range(200):
    x = rr.getrandbits(32) if rr.random() < 0.5 else (env.cls[rr.randrange(NCLS)]['c7'] - draw_F7(Shake(str(rr.random())))) & M32
    W = add(env.C7, scal((C7_CONST - x) & M32), need=set(NEEDF7)); pv = force(f7_test({j: W[j] for j in NEEDF7})).v
    for c in range(NCLS): tot += 1; bad += ((pv >> c) & 1) != int(F7((env.cls[c]['c7'] - x) & M32))
  print('class-test lanes %d, mismatches %d' % (tot, bad))
  bad = nm = 0
  for _ in range(300):
    u = rr.getrandbits(32); G = env.filt(u)
    for l in FEASIBLE_L:
      r = r16_ref(env, u, l); nm += r; bad += env.exact(u, l)[0] != r or (r and not (G >> l) & 1)
  for _ in range(6000):
    l = rr.choice(FEASIBLE_L); e = (rr.getrandbits(32) & ~E16M & M32) | E16V; u = (e - env.LC[l]['C']) & M32; G = env.filt(u)
    r = r16_ref(env, u, l); nm += r; bad += env.exact(u, l)[0] != r or (r and not (G >> l) & 1)
  print('row-16 checks: members seen %d, mismatches %d' % (nm, bad))
  bad = tot = 0; ext = [0, 1, M32, M32 - 1, 1 << 31, (1 << 31) - 1]
  for _ in range(100):
    cv = [rr.choice(ext) if rr.random() < 0.3 else rr.getrandbits(32) for _ in range(8)]; pre = cv_pre(Mach(), cv)
    ci = rr.randrange(NCLS); mem = env.members(ci); chunk = [rr.choice(mem) for _ in range(4)]
    U = packed_u(sum(S0pack(a) << (64 * k) for k, a in enumerate(chunk)), pre)
    for k, a0 in enumerate(chunk): tot += 1; bad += ((U >> (64 * k)) & M64) % (1 << 32) != u_ref(cv, a0)
  print('packed u lanes %d, mismatches %d' % (tot, bad))
  mx = max(S0(a) for c in range(NCLS) for a in env.members(c)); print('max S0 over the 782,800 variants %#x' % mx, mx <= 0xffffff58)

def attack(nfb, vmax, seed='attack'):
  env = Env(); rng = Shake(seed); V = 0
  for f in range(nfb):
    w = first_block(Mach(), rng); cv = compress(IV, w); mc = Mc()
    for (a0, (l, bx, by)) in process_cv(mc, cv, env, {}):
      ma, mb = struct.pack('>32I', *(w + bx)), struct.pack('>32I', *(w + by))
      if ma != mb and digest(ma) == digest(mb): return ma, mb
    V += mc.n
    if V > vmax: return None
  return None
BYTES_PER_OP = 6
CODE_REST = 8 * (8192 - sum(W6_OPS.values()) - sum(SUBF_OPS.values()))
def code_ops():
  keys = {}
  for lid in sorted(set(int(c) for c in LISTID)):
    L = LST(lid)
    for (pat, full, cu), n in L.keys.items(): keys[(lid,) + (pat, full, cu)] = n
  return sum(keys.values()), len(keys)
def memory_bytes(env=None):
  env = env or Env(); W = 32; lists = [env.getlist(l) for l in sorted(set(env.lid))]
  tab = dict(
    s_planes=sum(sum(L.dyn) for L in lists) * W, s_entries=sum(L.nb for L in lists) * 64 * W, cube_deltas=8 * W, sum_spill=63 * W, c7_planes=len(C7_DYN_BITS) * W,
    lo_table=4096 * W, mid_table=4096 * W, scan_table=8192 * W, class_descriptors=NCLS * 4 * W, row16_constants=len(FEASIBLE_L) * 4 * W,
    z_planes=ZLOADS * W, characteristic_and_Lstar=1280 * W, chaining_value_constants=64 * W, code=CODE_REST + BYTES_PER_OP * code_ops()[0])
  return tab, sum(tab.values())

if __name__ == '__main__':
  if len(sys.argv) > 1 and sys.argv[1] == 'ledger': ledger()
  elif len(sys.argv) > 3 and sys.argv[1] == 'attack': r = attack(int(sys.argv[2]), int(sys.argv[3])); print('collision found' if r else 'no collision (cap reached)', r)
  elif len(sys.argv) > 1 and sys.argv[1] == 'memory':
    tab, tot = memory_bytes()
    for k, v in tab.items(): print('%-26s %9d' % (k, v))
    print('total %d bytes = 2^%.4f (limit 2^20 = %d)' % (tot, math.log2(tot), 1 << 20))
  elif len(sys.argv) > 1 and sys.argv[1] == 'selftest': selftest()
  else: sys.stdout.write(json.dumps(run_request(json.loads(sys.stdin.read())), separators=(',', ':')))
