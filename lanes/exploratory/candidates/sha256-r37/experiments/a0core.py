#!/usr/bin/env python3
# a0core.py - the A0-variant attack on 37-step SHA-256 (sha256-r37-exploratory): exact data, the counted online program,
# and checks.  Standard library only.  The characteristic, its two-bit conditions, the semi-free-start pair and L* are
# those of IACR ePrint 2026/1120 (37 steps) as transcribed and verified in earlier filings; everything else (the variant
# family G, the c7 classes, the filters and the counted program) is defined and checked here.
import hashlib, json, struct, sys

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

# the 64 selected classes: (c7, base, mask); class = {base ^ s : s subset of mask, in_G, c7of == c7}, 3600 each
CLASSES = [tuple(int(v, 16) for v in ln.split()) for ln in """
cc968c4c 1c2f8142 01fec08d
cc968c5c 1c2f8112 01fec08d
cc968c6c 1c2f8122 01fec08d
cc968c7c 1c2f8132 01fec08d
cc968c8c 1c2f8102 01fec08d
cc968e1c 1c2f8352 01fec08d
cc968e2c 1c2f8362 01fec08d
cc968e3c 1c2f8372 01fec08d
cc968e4c 1c2f8342 01fec08d
cc968e5c 1c2f8312 01fec08d
cc968e6c 1c2f8322 01fec08d
cc968e7c 1c2f8332 01fec08d
cc968e8c 1c2f8302 01fec08d
cc96901c 1c2f81d2 01fec48d
cc96902c 1c2f81e2 01fec48d
cc96903c 1c2f81f2 01fec48d
cc96904c 1c2f8542 01fec08d
cc96905c 1c2f8512 01fec08d
cc96906c 1c2f8522 01fec08d
cc96907c 1c2f8532 01fec08d
cc96908c 1c2f8502 01fec08d
ce968d1c 1e2f8052 01fec08d
ce968d2c 1e2f8062 01fec08d
ce968d3c 1e2f8072 01fec08d
ce968d4c 1e2f8042 01fec08d
ce968d5c 1e2f8012 01fec08d
ce968d6c 1e2f8022 01fec08d
ce968d7c 1e2f8032 01fec08d
ce968d8c 1e2f8002 01fec08d
ce968f1c 1e2f8252 01fec08d
ce968f2c 1e2f8262 01fec08d
ce968f3c 1e2f8272 01fec08d
ce968f4c 1e2f8242 01fec08d
ce968f5c 1e2f8212 01fec08d
ce968f6c 1e2f8222 01fec08d
ce968f7c 1e2f8232 01fec08d
ce968f8c 1e2f8202 01fec08d
ce96911c 1e2f8452 01fec08d
ce96912c 1e2f8462 01fec08d
ce96913c 1e2f8472 01fec08d
ce96914c 1e2f8442 01fec08d
ce96915c 1e2f8412 01fec08d
ce96916c 1e2f8422 01fec08d
ce96917c 1e2f8432 01fec08d
ce96918c 1e2f8402 01fec08d
ce96931c 1e2f8652 01fec08d
ce96932c 1e2f8662 01fec08d
ce96933c 1e2f8672 01fec08d
ce96934c 1e2f8642 01fec08d
ce96935c 1e2f8612 01fec08d
ce96936c 1e2f8622 01fec08d
ce96937c 1e2f8632 01fec08d
ce96938c 1e2f8602 01fec08d
d2968d1c 1a2f8052 01fec08d
d2968d2c 1a2f8062 01fec08d
d2968d3c 1a2f8072 01fec08d
d2968d4c 1a2f8042 01fec08d
d2968d5c 1a2f8012 01fec08d
d2968d6c 1a2f8022 01fec08d
d2968d7c 1a2f8032 01fec08d
d2968d8c 1a2f8002 01fec08d
d2968f1c 1a2f8252 01fec08d
d2968f2c 1a2f8262 01fec08d
d2968f3c 1a2f8272 01fec08d
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
def make_R16(Lt):
    """The row-16 table R16[u] = mask of the l in L* whose row 16 holds for E16x = C16_l + u (emulated)."""
    def R16(u):
        mask = 0
        for Ld in Lt:
            e = (Ld['C16'] + u) & M32
            if (e & _M16) == _V16 and row16_ok(Ld, e): mask |= 1 << Ld['l']
        return mask
    return R16
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

def gen_w6(members):
    """W6x = cb + MAJ(A1, a0, A_{-1}) + ~CH(E5, E4, E3) + 1 with cb = C6 - A_{-2}, E3 = k3 + A_{-1}: MAJ bit j is
    (a0_j | AB_j) if A1_j else (a0_j & AB_j); CH bit j is E4_j if E5_j else E3_j; carry-save add of (MAJ, ~CH, CB)
    then a ripple add with carry-in 1; then the exact F6 test.  Returns (program, fail value)."""
    P = Prog()
    a0c, k3c, e4c = const_bits(members, lambda a: a), const_bits(members, k3of), const_bits(members, ne4of)
    inp = lambda kind, c, j: c[j] if c[j] is not None else P.ld('%s%d' % (kind, j))
    W6 = {}; c_e3 = ('c', 0); c_csa = ('c', 1); k_rip = ('c', 0)
    for j in range(32):
        ab = P.ld('AB%d' % j); a0j = inp('A0', a0c, j)
        maj = P.OR(a0j, ab) if (A1 >> j) & 1 else P.AND(a0j, ab)
        if (E5 >> j) & 1:
            y = inp('NE4', e4c, j)
            if j < 28:
                k3 = inp('K3', k3c, j); t = P.XOR(k3, ab); c_e3 = P.OR(P.AND(k3, ab), P.AND(c_e3, t))
        else:
            k3 = inp('K3', k3c, j); t = P.XOR(k3, ab); y = P.NOT(P.XOR(t, c_e3))
            if j < 28: c_e3 = P.OR(P.AND(k3, ab), P.AND(c_e3, t))
        z = P.ld('CB%d' % j)
        xy = P.XOR(maj, y); s = P.XOR(xy, z)
        nxt = P.OR(P.AND(maj, y), P.AND(z, xy)) if j < 31 else None
        t2 = P.XOR(s, c_csa); W6[j] = P.XOR(t2, k_rip)
        if j < 31: k_rip = P.OR(P.AND(s, c_csa), P.AND(k_rip, t2)); c_csa = nxt
    w = W6; X, O, N = P.XOR, P.OR, P.NOT
    common = O(O(X(w[14], w[18]), N(X(w[8], w[25]))), X(w[1], w[12]))
    bc = O(O(X(w[15], w[19]), N(X(w[9], w[26]))), X(w[2], w[13]))
    b_bad = O(bc, w[30])
    c_bad = O(O(O(O(bc, N(w[30])), X(X(w[16], w[20]), w[31])), N(X(X(w[10], w[27]), w[31]))), X(X(w[3], w[14]), w[31]))
    return P, O(common, P.AND(P.AND(w[29], b_bad), c_bad))

def peak_live(P, out):
    last = {}
    for i, (op, a) in enumerate(P.ops):
        for x in a:
            if isinstance(x, tuple) and x[0] == 'v': last[x[1]] = i
    last[out[1]] = len(P.ops)
    ends = {}
    for k, v in last.items(): ends.setdefault(v, []).append(k)
    live = peak = 0
    for i in range(len(P.ops)):
        live += 1 if i in last else 0
        peak = max(peak, live)
        live -= len(ends.get(i, []))
    return peak

def run_w6(P, out, data, bc):
    val = []
    g = lambda a: (ONE if a[1] else 0) if a[0] == 'c' else val[a[1]]
    for op, a in P.ops:
        if op == 'ld': val.append(bc[a[0]] if a[0][:2] in ('AB', 'CB') else data[a[0]])
        elif op == 'not': val.append(g(a[0]) ^ ONE)
        elif op == 'and': val.append(g(a[0]) & g(a[1]))
        elif op == 'or': val.append(g(a[0]) | g(a[1]))
        else: val.append(g(a[0]) ^ g(a[1]))
    return g(out)

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

def w7_scan(mc, a):
    """One W7 test per selected class (W7x = c7 - A_{-1} in F7): ld, sub, and, bitmap (6), branch: 10 per class."""
    hits = []
    for c in range(len(CLASSES)):
        w = mc.m(mc.sub(mc.ld(CLASSES[c][0]), a))
        if mc.br(mc.bit(F7, w)): hits.append(c)
    return hits

def broadcast(mc, a, b):
    """Per first block with a hit: the 64 broadcast planes AB_j (bit j of A_{-1}) and CB_j (bit j of C6 - A_{-2}),
    each 0 - ((x >> j) & 1) and stored (4 operations), after cb = (C6 - b) & M (2): 258 operations."""
    cb = mc.m(mc.sub(C6, b)); d = {}
    for name, x in (('AB', a), ('CB', cb)):
        for j in range(32):
            v = mc.sub(0, mc.and_(mc.shr(x, j), 1)); mc.st()
            d['%s%d' % (name, j)] = ONE if v else 0
    return d

def scan_lanes(mc, plane):
    """Indices of the set bits of a 256-bit plane: per 32-bit chunk extract (shr, and; 1 for chunk 0 and 7) and a
    zero branch; per set bit: isolate (sub, and), index by a 2^16-entry table on the low or high half (and, branch,
    shr, add base, ld, add 16 or add base, ld: at most 6), clear (xor), lane (add), loop branch: 11."""
    out = []
    for c in range(8):
        x = plane >> (32 * c)
        mc.n += 1 if c in (0, 7) else 2
        x &= M32
        while mc.br(x != 0):
            lb = x & (-x); mc.n += 2
            mc.n += 6
            out.append(32 * c + lb.bit_length() - 1)
            x ^= lb; mc.n += 2
    return out

def cv_pre(mc, cv):
    """Per first block, at its first good pair: the constants of W0 = a0 + kap0 and W1 (35 operations)."""
    Am1, Am2, Am3, Am4, Em1, Em2, Em3, Em4 = cv
    mj = mc.or_(mc.and_(Am1, Am2), mc.and_(Am3, mc.or_(Am1, Am2)))
    e0b = mc.m(mc.sub(mc.sub(Am4, mc.S0(Am1)), mj))
    ch = mc.xor(mc.and_(Em1, mc.xor(Em2, Em3)), Em3)
    kap0 = mc.sub(mc.sub(mc.sub(mc.sub(mc.sub(e0b, Am4), Em4), mc.S1(Em1)), ch), K[0])
    return dict(e0b=e0b, kap0=kap0, o12=mc.or_(Am1, Am2), n12=mc.and_(Am1, Am2), X=mc.xor(Em1, Em2), Em2=Em2,
                kap1=mc.sub((A1 - K[1]) & M32, Em3))

def good_pair(mc, a0, s0a, pre, R16):
    """u = W0 + s0(W1) and the row-16 table lookup R16[u] (u >> 3, add base, ld, (u & 7) << 5, shr, and, branch)."""
    E0 = mc.m(mc.add(a0, pre['e0b'])); W0 = mc.add(a0, pre['kap0'])
    mj = mc.or_(mc.and_(a0, pre['o12']), pre['n12'])
    ch = mc.xor(mc.and_(E0, pre['X']), pre['Em2'])
    W1 = mc.m(mc.sub(mc.sub(mc.sub(mc.sub(pre['kap1'], s0a), mj), mc.S1(E0)), ch))
    u = mc.m(mc.add(W0, mc.s0(W1)))
    mc.n += 7
    mask = R16(u)
    return mc.br(mask != 0), mask, u, W0 & M32, W1

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
        self.prog, self.out = gen_w6(self.members)
        self.nb = (len(self.members) + 255) // 256
        self._planes = {}
        self.names = {a[0] for op, a in self.prog.ops if op == 'ld' and a[0][:2] not in ('AB', 'CB')}
    def planes(self, b):
        if b not in self._planes: self._planes[b] = batch_planes(self.members, b, self.names)
        return self._planes[b]

def process_class(mc, cd, bc, cv, state, R16, Lt, check=None):
    """One W7-passing class: the counted bit-sliced W6 program on each batch, the lane scan, and every good pair."""
    a, b = cv[0], cv[1]
    found = None
    for bt in range(cd.nb):
        fail = run_w6(cd.prog, cd.out, cd.planes(bt), bc); mc.n += len(cd.prog.ops)
        nl = min(256, len(cd.members) - 256 * bt)
        lanes_mask = (1 << nl) - 1
        passp = (fail ^ ONE) & lanes_mask; mc.n += 2                 # NOT, AND with the batch's lane mask
        for L in scan_lanes(mc, passp):
            i = 256 * bt + L; a0 = mc.ld(cd.members[i]); s0a = mc.ld(S0(a0)); mc.n += 1     # index add
            mc.n += VC
            if check is not None: check('good', cv, a0, cd)
            if state.get('pre') is None: state['pre'] = cv_pre(mc, cv); mc.n += VC
            hit, mask, u, W0, W1 = good_pair(mc, a0, s0a, state['pre'], R16)
            state['good'] += 1
            if not hit: continue
            state['r16'] += 1; mc.n += VC
            w6, w7 = recompute_w67(mc, a0, a, b, cd.c7)
            f = step3b(mc, cv, a0, w6, w7, mask, Lt)
            if f and found is None: found = (a0, f)
        if check is not None:
            check('plane', cv, None, cd, bt=bt, fail=fail, nl=nl)
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
        for name, f, a in (('fb', first_block, (rng,)), ('w7scan', w7_scan, (cv[0],)), ('broadcast', broadcast, (cv[0], cv[1])),
                           ('pre', cv_pre, (cv,))):
            n, r = cnt(f, *a); seen.setdefault(name, set()).add(n)
        mc = Mach(); pre = cv_pre(mc, cv); a0 = class_members(*CLASSES[0])[rr.randrange(3600)]
        n, r = cnt(good_pair, a0, S0(a0), pre, R16); seen.setdefault('gp', set()).add(n)
    for k, v in seen.items():
        assert len(v) == 1, (k, v); cal[k] = v.pop()
    # step 3b on the published pair (variant a0 = published A0, l = 13): every row passes, so the count is the full path
    mc = Mach(); f = step3b(mc, CV0, SAx[0], MX[6], MX[7], 1 << 13, Lt)
    assert f is not None and f[0] == 13 and f[1] == MX and f[2] == MY
    cal['step3b_full'] = mc.n
    assert mc.n == 201 + 2 + 6 + 21 * (ROWCOMP + ROWCHECK + 1), mc.n
    mc = Mach(); recompute_w67(mc, SAx[0], CV0[0], CV0[1], c7of(SAx[0])); cal['recompute'] = mc.n
    progs = []
    for c in range(len(CLASSES)):
        mem = class_members(*CLASSES[c]) if full or c < 2 else None
        if mem is None: progs.append(None); continue
        P, out = gen_w6(mem); progs.append((len(P.ops), sum(1 for o in P.ops if o[0] == 'ld'), peak_live(P, out), len(mem)))
    cal['w6prog'] = progs
    return cal

# ---- the ledger (exact rationals) ----
def ledger(cal, q3_log2=-74.02, show=True, A_C=2 ** 60, scalar_w6=False):
    from fractions import Fraction as Fr
    import math
    C = 2644
    p7, p6 = Fr(68157440, 1 << 32), Fr(287309824, 1 << 32)
    r16 = Fr(1052672, 1 << 32)                         # sum over l of |R16_l| / 2^32 (exact enumeration, smc.c / C tools)
    k, n_c = len(CLASSES), 3600
    g = k * n_c * p7 * p6                               # expected good pairs per first block (exact under H1)
    progs = cal['w6prog']; assert all(p is not None for p in progs)
    w6_per_class = [15 * (p[0] + 2) for p in progs]     # 15 batches: the program, NOT and lane AND
    if scalar_w6: w6_per_class = [4 + 3600 * 18 for p in progs]   # sensitivity: scalar W6 test (setup 4, 18 per variant)
    scan_fixed = 15 * (2 * 1 + 6 * 2 + 8)               # per batch: chunk extraction and zero branches
    per_pass = 11                                        # per set lane of a pass plane
    per_good = per_pass + 3 + VC + cal['gp']             # scan + ld a0, ld S0(a0), index add + V update + good_pair
    c3b_pair = 201 + 23 + VC                             # per row-16 pair: W0..W5 and W8 (201), recomputed W6/W7 (23), V update
    c3b_l = 2 + 6 + 2 * (ROWCOMP + ROWCHECK + 1)         # per (pair, l) in the mask: rows 16 and 17 (always executed)
    rows_extra = 19 * Fr(1, 512)                         # rows 18..36 executed with probability <= 2^-9 each
    c3b_row = ROWCOMP + ROWCHECK + 1
    fixed = cal['fb'] + cal['w7scan'] + CTRL_FB          # every first block (plus one target compression)
    vbar = (k * p7) * (VC + cal['broadcast'] + cal['pre'] + VC) \
         + p7 * sum(CTRL_HIT + VC + w + scan_fixed + 2 for w in w6_per_class) \
         + g * per_good + g * r16 * (c3b_pair + c3b_l + rows_extra * c3b_row)
    q3 = Fr(2) ** int(round(q3_log2 * 100)) if False else None
    q3f = 2.0 ** q3_log2
    mu_target = Fr(1, 2) * (1 + Fr(1, 1 << 9))           # Section 10: E[X] >= (1 + 2^-9)/2
    nfb = math.ceil(float(mu_target) / (float(g) * 32 * q3f))
    eps = Fr(1, 256)
    VMAX = math.ceil((1 + eps) * nfb * vbar)
    vmax_last = 0                                        # the run halts as soon as V exceeds V_MAX (checked per class)
    vmax_class = max(w6_per_class) + scan_fixed + 2 + VC + n_c * (per_pass + per_good) + n_c * (c3b_pair + 32 * (c3b_l + 19 * c3b_row))
    A_S, DEV = 2 ** 50, 2 ** 40
    pre_ops = 2 ** 40                                    # all precomputation, bounded (Section 8)
    fin_units, fin_ops = 6, 600 + 1000                   # final verification; the next first block's setup after the last cap test
    T = Fr(A_C + A_S + DEV) + nfb + Fr(nfb * fixed + VMAX + vmax_class + pre_ops + fin_ops, C) + fin_units
    out = dict(g=float(g), log2_g=math.log2(g), vbar=float(vbar), nfb=nfb, log2_nfb=math.log2(nfb), VMAX=VMAX,
               per_fb_units=float(1 + Fr(fixed, C) + vbar / C), log2_T=math.log2(T),
               time_log2=math.ceil(math.log2(T) * 1e5) / 1e5, fixed=fixed, per_good=per_good,
               w6_class_mean=sum(w6_per_class) / k, vmax_class=vmax_class,
               preprocessing_log2=math.log2(A_C + A_S + DEV + pre_ops / C))
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
    def check(kind, cv, a0, cd, bt=None, fail=None, nl=None):
        if kind == 'good':
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
        print('W6 programs: ops per batch min %d max %d; loads max %d; peak live values %d; class sizes %s' %
              (min(p[0] for p in pr), max(p[0] for p in pr), max(p[1] for p in pr), max(p[2] for p in pr), sorted({p[3] for p in pr})))
        ledger(cal)
    else:
        req = json.loads(sys.stdin.read())
        sys.stdout.write(json.dumps(run_request(req), separators=(',', ':')))
