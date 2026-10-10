#!/usr/bin/env python3
# a0core38.py - the A0-variant attack on 38-step SHA-256 (sha256-r38-exploratory): exact data, the counted online program,
# and checks.  Standard library only.  The characteristic, its two-bit conditions, the semi-free-start pair and L* are
# those of IACR ePrint 2026/1120 (37 steps) as transcribed and verified in earlier filings; everything else (the variant
# family G, the c7 classes, the filters and the counted program) is defined and checked here.
import hashlib, json, struct, sys

M32 = 0xffffffff
K = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
     0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
     0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
     0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
     0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb]
IV = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]
R = 38

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
CHA = {7:'=nu=============================',8:'=========n=====n====n======u====',11:'====================u=======un==',
    12:'=u===n====n======u===nu=======n=',13:'==n============n================',14:'====u=========nn========u==u====',
    15:'======n=u=======n===============',17:'==u============================='}
CHE = {5:'+++=============================',6:'+++=1====0==+1=====0+===1==1====',7:'uuu=0+1=11=0+00====1+===0==00=01',
    8:'100=u+010n=1nu01=01nu=00n11u1=01',9:'11000u1=n11u0000101101110=01u0uu',10:'==1010=01u00001u=010u=101==10111',
    11:'1=n000=0111100101unn00011+111u10',12:'01nuuu=110n111nu000100100+010u1n',13:'00110101110=000u00111nuu+nnnu1n1',
    14:'=010n0===00===1n=11+0100+1110001',15:'=1==1=1==0=1==11===+u011n1011=1=',16:'=u==10===n===+u1===n0=u=1==+====',
    17:'=0=====+00===+0=+==01=0=0==+====',18:'=0=====+01===n1=+==1==1===0u====',19:'==11===nn====1==n===010===11==0=',
    20:'==1====00====1==0==========1====',21:'==u====10=======1===10==========',22:'==0=============================',
    23:'==1============================='}
CHW = {7:'==n=============================',8:'=====u===u==========n===========',9:'==u=============================',
    10:'=====n=u=======n===n==n=n=n=u=u=',11:'============u======u=u==========',15:'=====u===n==========n===========',
    16:'==u=============================',23:'=====1=uu=====1=u=1=============',25:'==n============================='}
# printed two-bit conditions (Table 4), with the corrected reading W25[4] = W25[6] (printed: W25[9])
X2 = [('A',14,15,'=','A',16,15),('A',14,23,'=','A',16,23),('A',14,25,'=','A',16,25),('A',15,4,'=','A',16,4),
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
    ('W',25,4,'=','W',25,6),('W',25,22,'=','W',25,31),('W',25,20,'=','W',25,27)]

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
CV0 = h8('cd278980 1b12a052 b87cc8a6 a9e059c5 c9c3db85 6ca4b5b5 63d13ac1 c0329f1e')
MY = h8('48fc271b 9fca20cd cc89f96f fc40396f 8b328cb4 6b91ef78 97f9b767 e2450045 3b016f58 de9804cb 66a99ea5 0ce30b8d a28cd15a 77a1e994 d28e48a0 9b5f6dbb')
MX = h8('48fc271b 9fca20cd cc89f96f fc40396f 8b328cb4 6b91ef78 97f9b767 c2450045 3f416758 fe9804cb 63a88c0f 0ceb1f8d a28cd15a 77a1e994 d28e48a0 9f1f65bb')
HASH0 = h8('5d9ca5f4 59ace3a3 26c9c26c 4252c585 4c0803b7 1b4d5ccd 25c3ccc0 90645c4d')
LSTAR = [((0xd28e48a0, 0x9f1f65bb), (0xd28e48a0, 0x9b5f6dbb))]     # the single element of L* (x side), (y side)

D7, T7 = 0x20000000, 0x03bff800                    # W7y = W7x + D7; the exact filter F7 (38 steps have no W6 filter)
def inF(w, d, t): return ((s0((w + d) & M32) - s0(w)) & M32) == t

# ---- S, the variant family G and the c7 classes ----
_tx = trace(CV0, MX); _ty = trace(CV0, MY)
SAx = [_tx[0][i] for i in range(14)]; SAy = [_ty[0][i] for i in range(14)]
SE = _tx[1]                                          # E4..E13 of member x (E4..E5 carry no difference)
C4 = (SAx[4] - S0(SAx[3]) - MAJ(SAx[3], SAx[2], SAx[1])) & M32            # E4 = a0 + C4
W8C = (SE[8] - SAx[4] - S1(SE[7]) - CH(SE[7], SE[6], SE[5]) - K[8]) & M32  # W8x = W8C - E4
D8 = (MY[8] - MX[8]) & M32; T8 = (s0(MY[8]) - s0(MX[8])) & M32            # W8y = W8x + D8; s0 difference T8
K3C = (SAx[3] - S0(SAx[2])) & M32
A1 = SAx[1]

def in_G(a0):
    """38 steps (E4 has no cell): W8x = W8C - E4 with W8y = W8x + D8 follows the W8 cell (x-values at its u/n bits, XOR
    difference exactly there) and the printed two-bit conditions W8[0] != W8[28], W8[30] != W8[9], W8[1] = W8[18]."""
    w = (W8C - ((a0 + C4) & M32)) & M32; y = (w + D8) & M32
    m, v, d, _ = CELLS['W'][8]
    if (w & m) != v or (w ^ y) != d: return False
    b = lambda k: (w >> k) & 1
    return b(0) != b(28) and b(30) != b(9) and b(1) == b(18)

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

# the 64 selected classes: (c7, base, mask); class = {base ^ s : s subset of mask, in_G, c7of == c7}, 3840 each
CLASSES = [tuple(int(v, 16) for v in ln.split()) for ln in """
af58eedf 06a10116 91eb54d1
af58eee3 06a10112 91eb54d1
af58eeff 06a10126 91eb5491
af58ef03 06a10122 91eb5491
af58ef07 06a1012e 91eb5491
af58ef0b 06a1012a 91eb5491
af58ef9f 06a10056 91eb55d1
af58efa3 06a10052 91eb55d1
af58efa7 06a1005e 91eb55d1
af58efab 06a1005a 91eb55d1
af58efbf 06a10066 91eb5491
af58efc3 06a10062 91eb5491
af58efc7 06a1006e 91eb5491
af58efcb 06a1006a 91eb5491
af58efdf 06a10016 91eb54d1
af58efe3 06a10012 91eb54d1
af58efe7 06a1001e 91eb54d1
af58efeb 06a1001a 91eb54d1
af58efff 06a10026 91eb5491
af58f003 06a10022 91eb5491
af58f007 06a1002e 91eb5491
af58f00b 06a1002a 91eb5491
af5ceee1 06a50114 91eb54d1
af5ceee5 06a50110 91eb54d1
af5ceeed 06a50118 91eb54d1
af5cef01 06a50124 91eb5491
af5cef05 06a50120 91eb5491
af5cef09 06a5012c 91eb5491
af5cef0d 06a50128 91eb5491
af5cefa1 06a50054 91eb55d1
af5cefa5 06a50050 91eb55d1
af5cefa9 06a5005c 91eb55d1
af5cefad 06a50058 91eb55d1
af5cefc1 06a50064 91eb5491
af5cefc5 06a50060 91eb5491
af5cefc9 06a5006c 91eb5491
af5cefcd 06a50068 91eb5491
af5cefe1 06a50014 91eb54d1
af5cefe5 06a50010 91eb54d1
af5cefe9 06a5001c 91eb54d1
af5cefed 06a50018 91eb54d1
af5cf001 06a50024 91eb5491
af5cf005 06a50020 91eb5491
af5cf009 06a5002c 91eb5491
af5cf00d 06a50028 91eb5491
af68eedf 06b10116 91eb54d1
af68eee3 06b10112 91eb54d1
af68eeff 06b10126 91eb5491
af68ef03 06b10122 91eb5491
af68ef07 06b1012e 91eb5491
af68ef0b 06b1012a 91eb5491
af68ef9f 06b10056 91eb55d1
af68efa3 06b10052 91eb55d1
af68efa7 06b1005e 91eb55d1
af68efab 06b1005a 91eb55d1
af68efbf 06b10066 91eb5491
af68efc3 06b10062 91eb5491
af68efc7 06b1006e 91eb5491
af68efcb 06b1006a 91eb5491
af68efdf 06b10016 91eb54d1
af68efe3 06b10012 91eb54d1
af68efe7 06b1001e 91eb54d1
af68efeb 06b1001a 91eb54d1
af68efff 06b10026 91eb5491
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


# ---- row 16 (the single element of L*): rows 12..15 of both members do not depend on the chaining value or the variant
_TX = trace(CV0, MX, 16); _TY = trace(CV0, MY, 16)
BASE16 = (_TX[0][12] + _TX[1][12] + S1(_TX[1][15]) + CH(_TX[1][15], _TX[1][14], _TX[1][13]) + K[16]) & M32
C16 = (BASE16 + s1(MX[14]) + MX[9]) & M32                  # E16x = C16 + W0 + s0(W1)
DW16 = (s1(MY[14]) - s1(MX[14]) + MY[9] - MX[9]) & M32
M3A, V3A = CELLS['E'][16][0], CELLS['E'][16][1]            # the ten fixed x-bits of E16 (stage 3a)
# the exact row-16 set: the 32 values of E16x for which every cell of row 16 (both members) and every two-bit condition
# closing at row 16 holds (exhaustive enumeration of the 2^22 values with the ten fixed bits; re-checked by setup())
R16SET = frozenset(h8("""481b02f9 481b02fa 481b02fd 481b02fe 481b06f9 481b06fa 481b06fd 481b06fe 481b22f9 481b22fa 481b22fd 481b22fe
 481b26f9 481b26fa 481b26fd 481b26fe 482302f9 482302fa 482302fd 482302fe 482306f9 482306fa 482306fd 482306fe 482322f9 482322fa
 482322fd 482322fe 482326f9 482326fa 482326fd 482326fe"""))

def new_rows():
    return [({**t[0]}, {**t[1]}, {i: t[2][i] for i in range(16)}) for t in (_TX, _TY)]

def step_rows(X, Y, t):
    for (A, E, W) in (X, Y):
        E[t] = (A[t-4] + E[t-4] + S1(E[t-1]) + CH(E[t-1], E[t-2], E[t-3]) + K[t] + W[t]) & M32
        A[t] = (E[t] - A[t-4] + S0(A[t-1]) + MAJ(A[t-1], A[t-2], A[t-3])) & M32

def row16_ok(e16):
    X, Y = new_rows()
    X[2][16] = (e16 - BASE16) & M32; Y[2][16] = (X[2][16] + DW16) & M32
    step_rows(X, Y, 16)
    return row_ok(X, Y, 16) and x2_ok(X, 16)

F7 = lambda w: inF(w, D7, T7)
R16 = lambda e: e in R16SET

# ---- the counted online program ----
VC = 1
CTRL_FB, CTRL_HIT = 16, 8
ROWCHECK, ROWCOMP = 53, 106


# ---- the bit-sliced E16 program (38 steps): 256 variants of one class per batch, bit L of a plane = variant L ----
# E16x = KP + a0 + s0(W1) with KP = kap0 + C16, W1 = kap1 - S0(a0) - MAJ(a0, A_{-1}, A_{-2}) - S1(E0) - CH(E0, E_{-1}, E_{-2}),
# E0 = a0 + e0b.  Per-CV broadcast planes: EB (e0b), P (A_{-1} & A_{-2}), Q (A_{-1} | A_{-2}), X (E_{-1} ^ E_{-2}),
# Y (E_{-2}), K1 (kap1), KP.  Three phases with every intermediate plane stored and reloaded (so only carries live in
# registers): A: E0 = a0 + EB (stored); B: per bit S1(E0), CH, MAJ, S0(a0) summed by two carry-save layers and a
# ripple, W1 = K1 - T by a ripple borrow (stored); C: per bit s0(W1), E16 = KP + a0 + s0(W1) by a carry-save layer and a
# ripple, and the ten fixed bits of E16 (stage 3a) accumulated into the fail plane.
ONE = (1 << 256) - 1
class Prog:
    def __init__(self): self.ops = []
    def new(self, op, *a): self.ops.append((op, a)); return ('v', len(self.ops) - 1)
    def ld(self, name): return self.new('ld', name)
    def st(self, name, v): self.ops.append(('st', (name, v)))
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

def const_bits(members, f):
    vals = [f(a) for a in members]
    return [('c', (vals[0] >> j) & 1) if all(((v ^ vals[0]) >> j) & 1 == 0 for v in vals) else None for j in range(32)]

def gen_e16(members):
    P = Prog()
    a0c, sac = const_bits(members, lambda a: a), const_bits(members, S0)
    def a0(j): return a0c[j] if a0c[j] is not None else P.ld('A0%d' % j)
    def sa(j): return sac[j] if sac[j] is not None else P.ld('SA%d' % j)
    # phase A
    c = ('c', 0)
    for j in range(32):
        x = a0(j); b = P.ld('EB%d' % j); t = P.XOR(x, b)
        P.st('E0_%d' % j, P.XOR(t, c))
        if j < 31: c = P.OR(P.AND(x, b), P.AND(c, t))
    # phase B
    v1 = v2 = rc = br = ('c', 0)
    for j in range(32):
        s1 = P.XOR(P.XOR(P.ld('E0_%d' % ((j + 6) % 32)), P.ld('E0_%d' % ((j + 11) % 32))), P.ld('E0_%d' % ((j + 25) % 32)))
        ch = P.XOR(P.AND(P.ld('E0_%d' % j), P.ld('X%d' % j)), P.ld('Y%d' % j))
        mj = P.OR(P.ld('P%d' % j), P.AND(a0(j), P.ld('Q%d' % j)))
        x, y, z = sa(j), mj, s1
        p = P.XOR(x, y); u1 = P.XOR(p, z); v1n = P.OR(P.AND(x, y), P.AND(z, p))
        q = P.XOR(u1, v1); u2 = P.XOR(q, ch); v2n = P.OR(P.AND(u1, v1), P.AND(ch, q))
        r = P.XOR(u2, v2); T = P.XOR(r, rc); rcn = P.OR(P.AND(u2, v2), P.AND(rc, r))
        k = P.ld('K1%d' % j); kt = P.XOR(k, T)
        P.st('W1_%d' % j, P.XOR(kt, br))
        if j < 31:
            br = P.OR(P.AND(P.NOT(k), T), P.AND(br, P.NOT(kt)))
            v1, v2, rc = v1n, v2n, rcn
    # phase C
    m3a, v3a = M3A, V3A
    cs = rp = ('c', 0); fail = ('c', 0)
    for j in range(32):
        s = P.XOR(P.ld('W1_%d' % ((j + 7) % 32)), P.ld('W1_%d' % ((j + 18) % 32)))
        if j + 3 <= 31: s = P.XOR(s, P.ld('W1_%d' % (j + 3)))
        x, y, z = P.ld('KP%d' % j), a0(j), s
        p = P.XOR(x, y); u = P.XOR(p, z); csn = P.OR(P.AND(x, y), P.AND(z, p))
        r = P.XOR(u, cs); e = P.XOR(r, rp); rpn = P.OR(P.AND(u, cs), P.AND(rp, r))
        if (m3a >> j) & 1:
            bad = P.XOR(e, ('c', (v3a >> j) & 1)); fail = P.OR(fail, bad)
        cs, rp = csn, rpn
    return P, fail

def run_prog(P, out, data, bc):
    val = []; mem = {}
    g = lambda a: (ONE if a[1] else 0) if a[0] == 'c' else val[a[1]]
    for op, a in P.ops:
        if op == 'st': mem[a[0]] = g(a[1]); val.append(None); continue
        if op == 'ld':
            n = a[0]
            val.append(mem[n] if n in mem else bc[n] if n in bc else data[n])
        elif op == 'not': val.append(g(a[0]) ^ ONE)
        elif op == 'and': val.append(g(a[0]) & g(a[1]))
        elif op == 'or': val.append(g(a[0]) | g(a[1]))
        else: val.append(g(a[0]) ^ g(a[1]))
    return g(out)

def count_ops(P): return len(P.ops)                         # every op, load and store is one primitive

def batch_planes(members, b, names):
    lanes = members[256 * b: 256 * b + 256]
    d = {}
    for name, f in (('A0', lambda a: a), ('SA', S0)):
        vs = None
        for j in range(32):
            key = '%s%d' % (name, j)
            if key not in names: continue
            if vs is None: vs = [f(a) for a in lanes]
            d[key] = int(''.join('1' if (v >> j) & 1 else '0' for v in reversed(vs)), 2)
    return d

def broadcast_planes(mc, pre, cv):
    """Per first block with a passing class: 7 x 32 broadcast planes (0 - ((x >> j) & 1), stored: 4 operations each)."""
    vals = dict(EB=pre['e0b'], P=pre['n12'], Q=pre['o12'], X=pre['X'], Y=pre['Em2'], K1=pre['kap1'] & M32, KP=pre['kap0'] & M32)
    d = {}
    for name, x in vals.items():
        for j in range(32):
            mc.n += 4; d['%s%d' % (name, j)] = ONE if (x >> j) & 1 else 0
    return d

def first_block(mc, rng):
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

def cv_pre(mc, cv):
    """Per first block with a passing class: the constants of W0 = a0 + kap0, E0 = a0 + e0b and W1 (35 operations)."""
    Am1, Am2, Am3, Am4, Em1, Em2, Em3, Em4 = cv
    mj = mc.or_(mc.and_(Am1, Am2), mc.and_(Am3, mc.or_(Am1, Am2)))
    e0b = mc.m(mc.sub(mc.sub(Am4, mc.S0(Am1)), mj))
    ch = mc.xor(mc.and_(Em1, mc.xor(Em2, Em3)), Em3)
    kap0 = mc.sub(mc.sub(mc.sub(mc.sub(mc.sub(e0b, Am4), Em4), mc.S1(Em1)), ch), K[0])
    return dict(e0b=e0b, kap0=mc.add(kap0, C16), o12=mc.or_(Am1, Am2), n12=mc.and_(Am1, Am2), X=mc.xor(Em1, Em2),
                Em2=Em2, kap1=mc.sub((A1 - K[1]) & M32, Em3))

def variant(mc, a0, s0a, pre):
    """One variant of a passing class (a good pair): E16x = C16 + W0 + s0(W1) and the stage-3a test of its ten fixed
    bits.  Loads (2), E0 (add, and), W0 + C16 (add), MAJ (and, or), CH (and, xor), S1 (8), W1 (4 subs, and), s0 (8),
    E16 (add, and), 3a (and, xor, branch), loop (add, compare-branch): 38 operations."""
    a0 = mc.ld(a0); s0a = mc.ld(s0a)
    E0 = mc.m(mc.add(a0, pre['e0b'])); W0c = mc.add(a0, pre['kap0'])
    mj = mc.or_(mc.and_(a0, pre['o12']), pre['n12'])
    ch = mc.xor(mc.and_(E0, pre['X']), pre['Em2'])
    W1 = mc.m(mc.sub(mc.sub(mc.sub(mc.sub(pre['kap1'], s0a), mj), mc.S1(E0)), ch))
    e16 = mc.m(mc.add(W0c, mc.s0(W1)))
    hit = mc.br(mc.xor(mc.and_(e16, M3A), V3A) == 0)
    mc.n += 2
    return hit, e16, W1

def step3b(mc, cv, a0):
    """A stage-3a pass: the exact row-16 test (bitmap, 6 + branch), then for a row-16 pass the words W0..W8 of both
    members (Lemma 4.1) and rows 16..37 with early abort.  Returns (M1, M1') on success."""
    Am1, Am2, Am3, Am4, Em1, Em2, Em3, Em4 = cv
    A = {-1: Am1, -2: Am2, -3: Am3, -4: Am4, 0: a0}
    for i in range(1, 8): A[i] = SAx[i]
    E = {-1: Em1, -2: Em2, -3: Em3, -4: Em4}
    for i in range(8):
        mj = mc.or_(mc.and_(A[i-1], A[i-2]), mc.and_(A[i-3], mc.or_(A[i-1], A[i-2])))
        E[i] = mc.m(mc.sub(mc.sub(mc.add(A[i], A[i-4]), mc.S0(A[i-1])), mj))
    W = {}
    for i in range(8):
        ch = mc.xor(mc.and_(E[i-1], mc.xor(E[i-2], E[i-3])), E[i-3])
        W[i] = mc.m(mc.sub(mc.sub(mc.sub(mc.sub(mc.sub(E[i], A[i-4]), E[i-4]), mc.S1(E[i-1])), ch), K[i]))
    w8 = mc.m(mc.sub(W8C, E[4]))
    (x14, x15), (y14, y15) = LSTAR[0]
    Wx = [W[i] for i in range(8)] + [w8] + MX[9:14] + [x14, x15]
    Wy = [W[i] for i in range(7)] + [(W[7] + D7) & M32, (w8 + D8) & M32] + MY[9:14] + [y14, y15]
    mc.n += 4
    X, Y = new_rows()
    for i in range(16): X[2][i] = Wx[i]; Y[2][i] = Wy[i]
    for t in range(16, R):
        for (Aa, Ee, Ww) in (X, Y):
            Ww[t] = mc.m(mc.add(mc.add(mc.add(mc.s1(Ww[t-2]), Ww[t-7]), mc.s0(Ww[t-15])), Ww[t-16]))
            ch = mc.xor(mc.and_(Ee[t-1], mc.xor(Ee[t-2], Ee[t-3])), Ee[t-3])
            Ee[t] = mc.m(mc.add(mc.add(mc.add(mc.add(mc.add(Aa[t-4], Ee[t-4]), mc.S1(Ee[t-1])), ch), K[t]), Ww[t]))
            mj = mc.or_(mc.and_(Aa[t-1], Aa[t-2]), mc.and_(Aa[t-3], mc.or_(Aa[t-1], Aa[t-2])))
            Aa[t] = mc.m(mc.add(mc.sub(Ee[t], Aa[t-4]), mc.add(mc.S0(Aa[t-1]), mj)))
        mc.n += ROWCHECK
        if not mc.br(row_ok(X, Y, t) and x2_ok(X, t)): return None
    return Wx, Wy

class ClassData:
    def __init__(self, c):
        self.c7 = CLASSES[c][0]; self.members = class_members(*CLASSES[c]); self.s0 = [S0(a) for a in self.members]
        self.prog, self.out = gen_e16(self.members)
        self.names = {a[0] for op, a in self.prog.ops if op == 'ld' and a[0][:2] in ('A0', 'SA')}
        self._planes = {}
    def planes(self, b):
        if b not in self._planes: self._planes[b] = batch_planes(self.members, b, self.names)
        return self._planes[b]

def scan_lanes(mc, plane):
    """Indices of the set bits of a 256-bit plane (as in our r37 program): per 32-bit chunk extraction (1 or 2) and a
    zero branch: 22; per set bit: isolate (sub, and), index by a 2^16-entry table (at most 6), clear and lane (xor, add),
    loop branch: 11."""
    out = []
    for c in range(8):
        x = (plane >> (32 * c)) & M32; mc.n += 1 if c in (0, 7) else 2
        while mc.br(x != 0):
            lb = x & (-x); mc.n += 2; mc.n += 6
            out.append(32 * c + lb.bit_length() - 1); x ^= lb; mc.n += 2
    return out

def process_class(mc, cd, cv, pre, bc, stats, found, w, check=None):
    """One passing class: the bit-sliced E16 program on its 15 batches (stage 3a of all 3840 variants), the lane scan of
    the rare batches with a stage-3a pass, the scalar E16 of each passing lane, the row-16 bitmap and step 3b."""
    for b in range(15):
        fail = run_prog(cd.prog, cd.out, cd.planes(b), bc); mc.n += len(cd.prog.ops)
        passp = fail ^ ONE; mc.n += 1
        stats['good'] += 256
        if check is not None: check('batch', cv, None, cd, b, fail)
        if not mc.br(passp != 0): continue
        for L in scan_lanes(mc, passp):
            i = 256 * b + L; a0 = cd.members[i]; mc.n += 1             # index add
            hit, e16, W1 = variant(mc, a0, cd.s0[i], pre)              # scalar E16 of this lane (37)
            stats['s3a'] += 1; mc.n += VC
            if not mc.br(mc.bit(R16, e16)): continue
            stats['r16'] += 1; mc.n += VC
            r = step3b(mc, cv, a0)
            if r: found.append((w, r))
    mc.n += 2                                            # compare V with V_MAX, branch

def online(nfb, rng, CD, stats, check=None, max_classes=None):
    """The online phase on nfb first blocks.  Returns (operation count, found pairs)."""
    mc = Mach(); found = []
    for f in range(nfb):
        mc.n += CTRL_FB
        w = first_block(mc, rng); cv = compress(IV, w); stats['fb'] += 1; stats['m0'] = w
        hits = w7_scan(mc, cv[0]); mc.n += CTRL_HIT * len(hits)
        stats['hits_found'] = stats.get('hits_found', 0) + len(hits)
        if not hits: continue
        pre = cv_pre(mc, cv); bc = broadcast_planes(mc, pre, cv); mc.n += VC
        for c in (hits if max_classes is None else hits[:max_classes]):
            stats['hits'] += 1; mc.n += VC
            if c not in CD: CD[c] = ClassData(c)
            process_class(mc, CD[c], cv, pre, bc, stats, found, w, check)
    return mc.n, found

def setup():
    """Checks of the advice: the published pair, every cell, S, the row-16 set (each of its 32 words passes row 16 and
    32 random words with the fixed bits do not, as a spot check), the variant of the published pair is in G."""
    ok = compress(CV0, MX) == compress(CV0, MY) == HASH0
    tx, ty = trace(CV0, MX), trace(CV0, MY)
    ok = ok and all(row_ok(tx, ty, i) for i in range(-4, R)) and all(x2_ok(tx, r) for r in range(R))
    wx, wy = words_from_cv(CV0, SAx[0]); ok = ok and wx == MX[:14] and wy == MY[:14] and in_G(SAx[0])
    ok = ok and all(row16_ok(e) for e in R16SET) and len(R16SET) == 32
    ok = ok and ((C16 + MX[0] + s0(MX[1])) & M32) in R16SET     # the published pair's E16x
    assert ok, 'setup check failed'
    return ok

# ---- calibration and ledger ----
def calibrate():
    import random
    rr = random.Random(20261009); seen = {}
    for trial in range(20):
        rng = Shake('calibrate-%d' % trial); cv = [rr.getrandbits(32) for _ in range(8)]
        for name, f, a in (('fb', first_block, (rng,)), ('w7scan', w7_scan, (cv[0],)), ('pre', cv_pre, (cv,))):
            mc = Mach(); f(mc, *a); seen.setdefault(name, set()).add(mc.n)
        mc = Mach(); pre = cv_pre(mc, cv); a0 = class_members(*CLASSES[0])[rr.randrange(3840)]
        mc = Mach(); variant(mc, a0, S0(a0), pre); seen.setdefault('variant', set()).add(mc.n)
    cal = {}
    for k, v in seen.items():
        assert len(v) == 1, (k, v); cal[k] = v.pop()
    # the full step-3b path on the published pair (every row passes)
    mc = Mach(); r = step3b(mc, CV0, SAx[0]); assert r is not None and r[0] == MX and r[1] == MY
    cal['step3b_full'] = mc.n
    mc = Mach(); broadcast_planes(mc, cv_pre(Mach(), CV0), CV0); cal['broadcast'] = mc.n
    cal['e16prog'] = [len(gen_e16(class_members(*cl))[0].ops) for cl in CLASSES]
    return cal

def ledger(cal, q3_log2=-101.05, show=True, A_C=2 ** 78, A_S=2 ** 74, DEV=2 ** 64):
    from fractions import Fraction as Fr
    import math
    C = 2728
    p7 = Fr(287309824, 1 << 32)
    k, n_c = len(CLASSES), 3840
    g = k * n_c * p7                                   # good pairs per first block (every variant of a passing class)
    p3a, r16 = Fr(1, 1024), Fr(32, 1 << 32)
    per_hit = CTRL_HIT + VC + 2                        # control, V update, cap test
    progs = cal['e16prog']
    p_nz = 1 - (1 - p3a) ** 256                        # a batch has a stage-3a pass
    batch_fixed = [prog + 1 + 1 for prog in progs]     # the program, NOT, nonzero branch
    per_lane3a = 11 + 1 + cal['variant'] + VC          # scan, index add, scalar E16, V update
    per_r16 = 7 + VC                                   # row-16 bitmap and branch (charged per stage-3a pass), V update
    full = cal['step3b_full']
    fixed = cal['fb'] + cal['w7scan'] + CTRL_FB + cal['pre'] + VC + cal['broadcast']   # per first block (setup charged always)
    vbar = p7 * sum(per_hit + 15 * bf + 15 * p_nz * 22 for bf in batch_fixed) \
         + g * p3a * (per_lane3a + per_r16) + g * r16 * full
    mu_target = Fr(1, 2) * (1 + Fr(1, 1 << 9))
    nfb = math.ceil(float(mu_target) / (float(g) * 2.0 ** q3_log2))
    VMAX = math.ceil((1 + Fr(1, 256)) * nfb * vbar)
    vmax_class = per_hit + 15 * (max(batch_fixed) + 22) + n_c * (per_lane3a + per_r16 + full)
    pre_ops, fin_units, fin_ops = 2 ** 40, 6, 1600
    T = Fr(A_C + A_S + DEV) + nfb + Fr(nfb * fixed + VMAX + vmax_class + pre_ops + fin_ops, C) + fin_units
    out = dict(g=float(g), vbar=float(vbar), nfb=nfb, log2_nfb=math.log2(nfb), VMAX=VMAX, fixed=fixed,
               per_fb_units=float(1 + Fr(fixed, C) + vbar / C), log2_T=math.log2(T), time_log2=math.ceil(math.log2(T) * 1e5) / 1e5,
               vmax_class=vmax_class, T_times_C=T * C, preprocessing_log2=math.log2(A_C + A_S + DEV + pre_ops / C))
    if show:
        for kk, v in out.items(): print('%-18s %s' % (kk, v))
    return out

from fractions import Fraction as Fr
import math

# ---- the q3 replica (organizer experiment a0-q3-r38): reduced replicates of the SMC estimator of proof.md Section 7 ----
Q3_NP, Q3_M, Q3_MT = 64, {17: 32, 18: 8, 19: 2, 20: 2, 21: 2}, 96
Q3_TRIALS = 20
Q3_POOL_LOG2 = -101.7                                    # frozen pass threshold of the pooled mean (calibrated on 48 local requests, 960 replicates)
F7_SIZE = 287309824

def draw_variant(rng):
    """A uniform variant of a uniform selected class (rejection inside the class's base ^ mask cube): uniform on the
    245,760 selected variants."""
    c7, base, mask = CLASSES[rng.below(len(CLASSES))]
    while True:
        a = base ^ (rng() & mask)
        if in_G(a) and c7of(a) == c7: return a

def q3_replicate(rng):
    """One replicate: returns (estimate, stage means, list of verified (cv, M1, M1') successes, failed rebuilds)."""
    r16 = sorted(R16SET); parts = []
    for p in range(Q3_NP):
        X, Y = new_rows(); e16 = r16[rng.below(32)]
        X[2][16] = (e16 - BASE16) & M32; Y[2][16] = (X[2][16] + DW16) & M32; step_rows(X, Y, 16); parts.append((X, Y))
    means = [Fr(32, 1 << 32)]
    for t in range(17, 22):
        m, v, _, pt = CELLS['E'][t]; q = pt & CELLS['E'][t-1][3]
        f = bin(m).count('1') + bin(q).count('1'); kids = []; npass = 0
        for (X, Y) in parts:
            dW = (s1(Y[2][t-2]) - s1(X[2][t-2]) + Y[2][t-7] - X[2][t-7]) & M32
            base = (X[0][t-4] + X[1][t-4] + S1(X[1][t-1]) + CH(X[1][t-1], X[1][t-2], X[1][t-3]) + K[t]) & M32
            for k in range(Q3_M[t]):
                e = (((rng() & M32) & ~m & ~q) | v | (X[1][t-1] & q))
                Xc = [dict(d) for d in X]; Yc = [dict(d) for d in Y]
                Xc[2][t] = (e - base) & M32; Yc[2][t] = (Xc[2][t] + dW) & M32; step_rows(Xc, Yc, t)
                if row_ok(Xc, Yc, t) and x2_ok(Xc, t): npass += 1; kids.append((Xc, Yc))
        means.append(Fr(npass, len(parts) * Q3_M[t] * (1 << f)))
        if not kids: return 0.0, means, [], 0
        parts = [kids[rng.below(len(kids))] for _ in range(Q3_NP)]
    mw, vw, _, _ = CELLS['W'][23]; wsum = 0; succ = []; bad = 0
    for (X, Y) in parts:
        a0 = draw_variant(rng); w8x = (W8C - ((a0 + C4) & M32)) & M32; w8y = (w8x + D8) & M32
        for k in range(Q3_MT):
            w23 = ((rng() & M32) & ~mw) | vw
            b = lambda j: (w23 >> j) & 1
            w23 = (w23 & ~((1 << 30) | (1 << 31) | (1 << 21) | (1 << 25))) | ((1 - b(0)) << 30) | ((1 - b(1)) << 31) | (b(14) << 21) | (b(16) << 25)
            w7 = (w23 - s1(X[2][21]) - X[2][16] - s0(w8x)) & M32
            if not inF(w7, D7, T7): continue
            w6 = rng() & M32
            Xc = [dict(d) for d in X]; Yc = [dict(d) for d in Y]
            Xc[2][6], Xc[2][7], Xc[2][8] = w6, w7, w8x; Yc[2][6], Yc[2][7], Yc[2][8] = w6, (w7 + D7) & M32, w8y
            ok = True
            for t in range(22, R):
                for (A_, E_, W_) in (Xc, Yc): W_[t] = (s1(W_[t-2]) + W_[t-7] + s0(W_[t-15]) + W_[t-16]) & M32
                step_rows(Xc, Yc, t)
                if not (row_ok(Xc, Yc, t) and x2_ok(Xc, t)): ok = False; break
            if not ok: continue
            wsum += 1
            W = dict(Xc[2])
            W[5] = (W[21] - s1(W[19]) - W[14] - s0(W[6])) & M32; W[4] = (W[20] - s1(W[18]) - W[13] - s0(W[5])) & M32
            W[3] = (W[19] - s1(W[17]) - W[12] - s0(W[4])) & M32; W[2] = (W[18] - s1(W[16]) - W[11] - s0(W[3])) & M32
            W[1] = (W[17] - s1(W[15]) - W[10] - s0(W[2])) & M32; W[0] = (W[16] - s1(W[14]) - W[9] - s0(W[1])) & M32
            mx = [W[i] for i in range(16)]; my = mx[:7] + [Yc[2][i] for i in range(7, 16)]
            Avar = {i: SAx[i] for i in range(14)}; Avar[0] = a0
            cv = invert_cv(Avar, {4: (a0 + C4) & M32, 5: SE[5], 6: SE[6], 7: SE[7]}, W)
            wx, wy = words_from_cv(cv, a0)
            okc = wx == mx[:14] and wy == my[:14] and compress(cv, mx) == compress(cv, my) and mx != my and inF(mx[7], D7, T7)
            tx, ty = trace(cv, mx), trace(cv, my)
            okc = okc and all(row_ok(tx, ty, i, i != 7) for i in range(-4, R)) and all(x2_ok(tx, r) for r in range(8, R))
            if okc: succ.append((cv, mx, my))
            else: bad += 1
    means.append(Fr(wsum * (1 << 22), len(parts) * Q3_MT * F7_SIZE))
    est = 1
    for mm in means: est *= mm
    return float(est), means, succ, bad

# ---- experiments (organizer executor: one JSON request on stdin, one JSON document on stdout) ----
def invert_cv(A, E, W):
    """Chaining value from the state rows 4..7 of member x and W0..W7 (inverting steps 7..0)."""
    a = {i: A[i] for i in range(4, 8)}; e = {i: E[i] for i in range(4, 8)}
    for i in range(7, -1, -1):
        T1 = (a[i] - S0(a[i-1]) - MAJ(a[i-1], a[i-2], a[i-3])) & M32
        a[i-4] = (e[i] - T1) & M32
        e[i-4] = (T1 - S1(e[i-1]) - CH(e[i-1], e[i-2], e[i-3]) - K[i] - W[i]) & M32
    return [a[-1], a[-2], a[-3], a[-4], e[-1], e[-2], e[-3], e[-4]]

def sfs_trial(rng, cap=1 << 12, restarts=12, tail_cap=1 << 15):
    """A 38-step semi-free-start collision whose second-block state uses a seed-chosen variant of a seed-chosen class:
    row 16 from the exact row-16 set (E16x uniform among its 32 words), rows 17..21 by proposals with each row's fixed
    x-bits of E imposed (restart from row 16 after `cap` proposals at a row), then W23 proposals with its x-cells and
    two-bit conditions imposed, W7 = W23 - s1(W21) - W16 - s0(W8) accepted iff in F7, W6 uniform, rows 22..37 with the
    variant's W8; W0..W5 by the inverse expansion and CV1 by inverting steps 7..0."""
    c = rng.below(len(CLASSES)); members = class_members(*CLASSES[c]); vi = rng.below(len(members)); a0 = members[vi]
    w8x = (W8C - ((a0 + C4) & M32)) & M32; w8y = (w8x + D8) & M32
    r16 = sorted(R16SET)
    for attempt in range(restarts):
        X, Y = new_rows(); tries = []; dead = False
        e16 = r16[rng.below(32)]
        X[2][16] = (e16 - BASE16) & M32; Y[2][16] = (X[2][16] + DW16) & M32; step_rows(X, Y, 16)
        assert row_ok(X, Y, 16) and x2_ok(X, 16)
        for t in range(17, 22):
            m, v, _, _ = CELLS['E'][t]
            dW = (s1(Y[2][t-2]) - s1(X[2][t-2]) + Y[2][t-7] - X[2][t-7]) & M32
            base = (X[0][t-4] + X[1][t-4] + S1(X[1][t-1]) + CH(X[1][t-1], X[1][t-2], X[1][t-3]) + K[t]) & M32
            n = 0
            while True:
                n += 1
                if n > cap: dead = True; break
                X[2][t] = ((((rng() & M32) & ~m) | v) - base) & M32; Y[2][t] = (X[2][t] + dW) & M32
                step_rows(X, Y, t)
                if row_ok(X, Y, t) and x2_ok(X, t): break
            if dead: break
            tries.append(n)
        if not dead: break
    if dead: return None
    mw, vw, _, _ = CELLS['W'][23]
    n = 0
    while True:
        n += 1
        if n > tail_cap: return None
        w23 = ((rng() & M32) & ~mw) | vw
        b = lambda k: (w23 >> k) & 1
        w23 = (w23 & ~((1 << 30) | (1 << 31) | (1 << 21) | (1 << 25))) | ((1 - b(0)) << 30) | ((1 - b(1)) << 31) | (b(14) << 21) | (b(16) << 25)
        w7 = (w23 - s1(X[2][21]) - X[2][16] - s0(w8x)) & M32
        if not inF(w7, D7, T7): continue
        w6 = rng() & M32
        Xc = [dict(d) for d in X]; Yc = [dict(d) for d in Y]
        Xc[2][6], Xc[2][7], Xc[2][8] = w6, w7, w8x
        Yc[2][6], Yc[2][7], Yc[2][8] = w6, (w7 + D7) & M32, w8y
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
    mx = [W[i] for i in range(16)]; my = mx[:7] + [Yc[2][i] for i in range(7, 16)]
    Avar = {i: SAx[i] for i in range(14)}; Avar[0] = a0
    Evar = {4: (a0 + C4) & M32, 5: SE[5], 6: SE[6], 7: SE[7]}
    cv = invert_cv(Avar, Evar, W)
    wx, wy = words_from_cv(cv, a0)
    ok = wx == mx[:14] and wy == my[:14] and compress(cv, mx) == compress(cv, my) and mx != my
    tx, ty = trace(cv, mx), trace(cv, my)
    ok = ok and all(row_ok(tx, ty, i, i != 7) for i in range(-4, R)) and all(x2_ok(tx, r) for r in range(8, R))
    ok = ok and in_G(a0) and c7of(a0) == CLASSES[c][0] and mx[8] != MX[8] and inF(mx[7], D7, T7)
    obs = dict(class_index=c, variant_index=vi, checks_passed=int(ok), restarts=attempt, proposals_row17=tries[0], proposals_tail=tries[-1])
    return cv, mx, my, obs

def online_trial(rng, max_fb=16, sample=8, max_classes=1):
    """The counted online program on seed-drawn first blocks until one with a passing class (at most max_fb),
    processing one passing class (3840 good pairs, 15 bit-sliced batches): every lane's stage-3a decision is checked
    against the scalar definition (E16x = C16 + W0 + s0(W1) from the Step-2 equations, W7 in F7), and `sample` good
    pairs against every cell of rows -4..15."""
    CD = {}; bad = [0, 0, 0]; firstpair = []
    def check(kind, cv, a0, cd, b, fail):
        for L in range(256):
            a0 = cd.members[256 * b + L]; wx, wy = words_from_cv(cv, a0)
            if not (inF(wx[7], D7, T7) and wx[7] == (cd.c7 - cv[0]) & M32): bad[0] += 1
            e16 = (C16 + wx[0] + s0(wx[1])) & M32
            if ((fail >> L) & 1) == ((e16 & M3A) == V3A): bad[2] += 1
            if len(firstpair) < sample:
                (x14, x15), (y14, y15) = LSTAR[0]
                tx = trace(cv, wx + [x14, x15], 16); ty = trace(cv, wy + [y14, y15], 16)
                if not all(row_ok(tx, ty, i, i != 7) for i in range(-4, 16)): bad[1] += 1
                firstpair.append((wx, wy))
    stats = dict(fb=0, hits=0, good=0, s3a=0, r16=0); ops = 0
    for f in range(max_fb):
        n, found = online(1, rng, CD, stats, check, max_classes)
        ops += n
        if stats['hits']: break
    obs = dict(first_blocks=stats['fb'], w7_classes=stats.get('hits_found', 0), classes_processed=stats['hits'],
               good_pairs=stats['good'], stage3a_passes=stats['s3a'], row16_passes=stats['r16'], counted_ops=ops,
               filter_mismatches=bad[0], cell_mismatches=bad[1], lane_mismatches=bad[2], pairs_cell_checked=len(firstpair))
    return ((stats['m0'],) + firstpair[0]) if firstpair else None, obs

def run_request(req):
    setup()
    eid = req['experiment_id']; out = []; q3_state = []; q3_first = []
    for tr in req['trials']:
        t = tr['trial']; rng = Shake(eid + '|' + tr['seed'])
        rec = dict(trial=t, message_a_hex=None, message_b_hex=None)
        if eid.startswith('a0-sfs') and t < 12:
            r = sfs_trial(rng)
            if r:
                cv, mx, my, obs = r
                rec['message_a_hex'] = struct.pack('>24I', *(cv + mx)).hex()
                rec['message_b_hex'] = struct.pack('>24I', *(cv + my)).hex()
                rec['observations'] = obs
        elif eid.startswith('a0-q3') and t <= Q3_TRIALS:
            if t < Q3_TRIALS:
                est, means, succ, bad = q3_replicate(rng); q3_state.append((est, bad))
                rec['observations'] = dict(log2_estimate=(round(math.log2(est), 4) if est > 0 else None), successes=len(succ), failed_rebuilds=bad,
                                           stage_log2=[(round(math.log2(m), 4) if m > 0 else None) for m in means])
                if succ and bad == 0:
                    cv, mx, my = succ[0]
                    rec['message_a_hex'] = struct.pack('>24I', *(cv + mx)).hex(); rec['message_b_hex'] = struct.pack('>24I', *(cv + my)).hex()
                    q3_first.append(rec['message_a_hex'] + ':' + rec['message_b_hex'])
            else:
                ests = [e for e, b in q3_state]; nbad = sum(b for e, b in q3_state)
                pooled = sum(ests) / len(ests) if ests else 0.0
                rec['observations'] = dict(log2_pooled_mean=(round(math.log2(pooled), 4) if pooled > 0 else None), replicates=len(ests), failed_rebuilds=nbad,
                                           pass_threshold_log2=Q3_POOL_LOG2)
                if Q3_POOL_LOG2 is not None and pooled > 0 and math.log2(pooled) >= Q3_POOL_LOG2 and nbad == 0 and q3_first:
                    a, b = q3_first[0].split(':'); rec['message_a_hex'] = a; rec['message_b_hex'] = b
        elif eid.startswith('a0-online') and t < 6:
            pair, obs = online_trial(rng)
            rec['observations'] = obs
            if pair and obs['filter_mismatches'] == obs['cell_mismatches'] == obs['lane_mismatches'] == 0:
                m0, wx, wy = pair; (x14, x15), (y14, y15) = LSTAR[0]
                rec['message_a_hex'] = struct.pack('>32I', *(m0 + wx + [x14, x15])).hex()
                rec['message_b_hex'] = struct.pack('>32I', *(m0 + wy + [y14, y15])).hex()
        out.append(rec)
    return dict(schema_version=1, trials=out)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'ledger':
        setup(); cal = calibrate(); print(json.dumps(cal)); ledger(cal)
    else:
        req = json.loads(sys.stdin.read())
        sys.stdout.write(json.dumps(run_request(req), separators=(',', ':')))
