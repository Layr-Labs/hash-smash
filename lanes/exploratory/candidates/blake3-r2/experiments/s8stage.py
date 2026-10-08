#!/usr/bin/env python3
"""Staged S8 search for 2-round BLAKE3 (blake3-r2-prefix-v1), order S2K14 with one stage-A test per four positions and
an early exit in stage C; implements proof.md (credits there): Subflatus3's 5ca02dfb program (winglock's c19feef, the
stride 2^14, the pair test) with the quad test, hit tree, early exit and continuation of this version.  Stage A 70 ops
per quad, stage B 66 (+ hit tests and spills <= 10 per entry), stage C 61, continuation <= K_OPS.  Organizer mode: one
JSON request on stdin, one JSON document out; standard library only.
  python3 s8stage.py --selftest N [seed] | --ledger      (the model count: count_s8.py, proof.md Appendix D)
"""
import copy, hashlib, json, math, os, struct, sys
from fractions import Fraction

M32 = 0xffffffff
LW, NL = 36, 7
LANEMASK = (1 << LW) - 1
W256 = (1 << 256) - 1

def ror(x, r): r %= 32; return ((x >> r) | (x << (32 - r))) & M32 if r else x & M32
def rol(x, r): return ror(x, (32 - r) % 32)
IV = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]
X3, X7, X11, X15 = 0x29d4fa98, 0xbee3af28, 0x44036000, 0x40c58500
W4, W13 = 0x97475638, 0x0007c006
K = (IV[2] + IV[6]) & M32
W4p = (((K + W4) & M32) ^ 8) - K & M32
DELTA = (W4 - W4p) & M32
Y3, Y3p, Y11, Y11p = 0x8127c181, 0x7edf3e7e, 0x7af77f38, 0x850000c3
DY3 = (Y3p - Y3) & M32
ETA = 0x830303cf
CLASS_MASK, CLASS_VAL = 0x03cf8303, 0x030c0303
MF, VF = 0x00098188, 0x00008000   # beta filter on c1 of E1 (part of the event good of H1)
KF = MF & ~VF                     # 00090188: c1 passes iff (c1 + KF) AND MF == MF (Lemma F2)
ALLA = 0x0B000300                 # bits 8, 9, 24, 25, 27 (Lemma A3)
# S8: e1 bits 2,3 = 1 and bit 21 == bit 26.  Member order: i bit0 -> e1 bit 14, bit1 -> 30, bit2 -> 31, rest increasing.
FREE16 = [4, 5, 6, 7, 10, 11, 12, 13, 14, 20, 21, 27, 28, 29, 30, 31]
ORDER = [14, 30, 31] + [b for b in FREE16 if b not in (14, 30, 31)]
NMEM = 1 << 16                    # members of S8
KS = 14                            # lane stride 2^KS in C2.a1 (c19feef: 16)
NPOS = 1 << KS                     # positions per group
NRV = 1 << (32 - KS)               # values r of C2.a1 >> KS
NBATCH = (NRV + NL - 1) // NL      # 37,450 groups per member
NLAST = NRV - NL * (NBATCH - 1)    # distinct lanes of the last group: 1
NBLK = NPOS >> 8                   # blocks of 256 positions per group: 64
def dval(r): return ror((r << KS) & M32, 16)   # C2.d1 at position 0 for C2.a1 = r 2^KS: ((r & 3) << 30) | (r >> 2)

def member(i):
    e1 = CLASS_VAL | 0xc
    for t, b in enumerate(ORDER):
        if (i >> t) & 1: e1 |= 1 << b
    if (e1 >> 21) & 1: e1 |= 1 << 26
    return (e1 - Y3) & M32

def in_S8(y):
    e1 = (Y3 + y) & M32
    return (e1 & CLASS_MASK) == CLASS_VAL and (e1 & 0xc) == 0xc and ((e1 >> 21) & 1) == ((e1 >> 26) & 1)

def bc(v): return sum((v & LANEMASK) << (LW * l) for l in range(NL))     # broadcast into 7 lanes
def lanes(x): return [(x >> (LW * l)) & LANEMASK for l in range(NL)]
def pack(vals): return sum((v & LANEMASK) << (LW * l) for l, v in enumerate(vals))

# == the construction of 60f94c5c (Jbenisek), proof.md Section 2: steps O, M, Y, T ==
K2A = (K + W4) & M32; K2D = ror(K2A ^ 55, 16); K2C = (IV[2] + K2D) & M32; K2B = ror(IV[6] ^ K2C, 12)

def outer(six):
    """Step O: the lines that read only the six words (C0.c1, C0.d1, D3.d1, S15, S9, w5)."""
    c0c, c0d, d3d, s15, s9, w5 = six
    v = {'C0.c1': c0c, 'C0.d1': c0d, 'D3.d1': d3d, 'S15': s15, 'S9': s9, 'w5': w5}
    v['S2'] = (K2A + K2B + w5) & M32; v['S14'] = ror(K2D ^ v['S2'], 8)
    v['S10'] = (K2C + v['S14']) & M32; v['S6'] = ror(K2B ^ v['S10'], 7)
    v['D3.a1'] = rol(d3d, 16) ^ v['S14']; v['D3.c1'] = (s9 + d3d) & M32
    v['D3.b1'] = (X3 - v['D3.a1']) & M32; v['S4'] = rol(v['D3.b1'], 12) ^ v['D3.c1']
    v['S3'] = (v['D3.a1'] - v['S4']) & M32; v['X14'] = ror(d3d ^ X3, 8)
    v['X9'] = (v['D3.c1'] + v['X14']) & M32; v['X4'] = ror(v['D3.b1'] ^ v['X9'], 7)
    v['K3.d1'] = rol(s15, 8) ^ v['S3']; v['K3.c1'] = (IV[3] + v['K3.d1']) & M32
    v['K3.b1'] = ror(IV[7] ^ v['K3.c1'], 12); v['S11'] = (v['K3.c1'] + s15) & M32
    v['S7'] = ror(v['K3.b1'] ^ v['S11'], 7); v['K3.a1'] = rol(v['K3.d1'], 16) ^ 11
    v['w6'] = (v['K3.a1'] - IV[3] - IV[7]) & M32; v['w7'] = (v['S3'] - v['K3.a1'] - v['K3.b1']) & M32
    v['X8'] = (c0c - c0d) & M32; v['C0.b1'] = ror(v['X4'] ^ c0c, 12)
    v['D2.b1'] = rol(X7, 7) ^ v['X8']; v['D2.c1'] = rol(v['D2.b1'], 12) ^ v['S7']
    v['X13'] = (v['X8'] - v['D2.c1']) & M32
    return v

def middle(o, X2):
    """Step M: the lines that read X2 (and not the member)."""
    v = dict(o, X2=X2)
    v['D2.a1'] = (X2 - v['D2.b1'] - W13) & M32; v['D2.d1'] = rol(v['X13'], 8) ^ X2
    v['S13'] = rol(v['D2.d1'], 16) ^ v['D2.a1']; v['S8'] = (v['D2.c1'] - v['D2.d1']) & M32
    v['w12'] = (v['D2.a1'] - v['S2'] - v['S7']) & M32
    v['K1.c1'] = (v['S9'] - v['S13']) & M32; v['K1.d1'] = (v['K1.c1'] - IV[1]) & M32
    v['K1.a1'] = rol(v['K1.d1'], 16); v['K1.b1'] = ror(IV[5] ^ v['K1.c1'], 12)
    v['S1'] = rol(v['S13'], 8) ^ v['K1.d1']; v['S5'] = ror(v['K1.b1'] ^ v['S9'], 7)
    v['w2'] = (v['K1.a1'] - IV[1] - IV[5]) & M32; v['w3'] = (v['S1'] - v['K1.a1'] - v['K1.b1']) & M32
    v['K0.b1'] = rol(v['S4'], 7) ^ v['S8']; v['K0.c1'] = rol(v['K0.b1'], 12) ^ IV[4]
    v['K0.d1'] = (v['K0.c1'] - IV[0]) & M32; v['K0.a1'] = rol(v['K0.d1'], 16)
    v['S12'] = (v['S8'] - v['K0.c1']) & M32; v['S0'] = rol(v['S12'], 8) ^ v['K0.d1']
    v['w0'] = (v['K0.a1'] - IV[0] - IV[4]) & M32; v['w1'] = (v['S0'] - v['K0.a1'] - v['K0.b1']) & M32
    return v

def member_vals(o, y):
    """Step Y: the lines that read the member and the outer step, not X2."""
    Y8 = rol(y, 7) ^ o['C0.b1']; Y12 = (Y8 - o['C0.c1']) & M32; Y0 = rol(Y12, 8) ^ o['C0.d1']
    ca = (Y0 - o['C0.b1'] - o['w6']) & M32; X12 = rol(o['C0.d1'], 16) ^ ca
    dc = (X11 - X12) & M32; db = ror(o['S6'] ^ dc, 12); X6 = ror(db ^ X11, 7); dd = (dc - o['S11']) & M32
    X1 = rol(X12, 8) ^ dd
    return {'Y12': Y12, 'C0.a1': ca, 'X12': X12, 'D1.b1': db, 'X6': X6, 'D1.d1': dd, 'X1': X1}

def trial_words(v, y):
    """Step T and steps S2, S3: the sixteen words of A and B and the two messages."""
    r = member_vals(v, y)
    X0 = (r['C0.a1'] - v['X4'] - v['w2']) & M32
    fd = rol(X15, 8) ^ X0; fc = (v['S10'] + fd) & M32; fb = ror(v['S5'] ^ fc, 12)
    fa = rol(fd, 16) ^ v['S15']; ga = rol(r['D1.d1'], 16) ^ v['S12']
    w8 = (fa - v['S0'] - v['S5']) & M32; w9 = (X0 - fa - fb) & M32
    w10 = (ga - v['S1'] - v['S6']) & M32; w11 = (r['X1'] - ga - r['D1.b1']) & M32
    w = [v['w0'], v['w1'], v['w2'], v['w3'], W4, v['w5'], v['w6'], v['w7'], w8, w9, w10, w11, v['w12'], W13, 0, 0]
    wp = list(w); wp[4] = W4p; wp[5] = (v['w5'] + DELTA) & M32
    A = struct.pack('<16I', *w)[:55]; B = struct.pack('<16I', *wp)[:63]
    assert struct.pack('<16I', *w)[55:] == b'\0' * 9 and struct.pack('<16I', *wp)[55:] == b'\0' * 9
    return A, B, w, wp

def G(A, B, C, D, x, y):
    a1 = (A + B + x) & M32; d1 = ror(D ^ a1, 16); c1 = (C + d1) & M32; b1 = ror(B ^ c1, 12)
    a2 = (a1 + b1 + y) & M32; d2 = ror(d1 ^ a2, 8); c2 = (c1 + d2) & M32; b2 = ror(b1 ^ c2, 7)
    return (a1, d1, c1, b1, a2, d2, c2, b2)

PERM = (2, 6, 3, 10, 7, 0, 4, 13, 1, 11, 12, 5, 9, 14, 15, 8)
def trace(w, n):
    v = IV[:] + IV[:4] + [0, 0, n, 11]; s = list(w); tr = {}
    for rnd in range(2):
        for name, (a, b, c, d), (i, j) in [('C0', (0, 4, 8, 12), (0, 1)), ('C1', (1, 5, 9, 13), (2, 3)), ('C2', (2, 6, 10, 14), (4, 5)), ('C3', (3, 7, 11, 15), (6, 7)),
                                           ('E0', (0, 5, 10, 15), (8, 9)), ('E1', (1, 6, 11, 12), (10, 11)), ('E2', (2, 7, 8, 13), (12, 13)), ('E3', (3, 4, 9, 14), (14, 15))]:
            o = G(v[a], v[b], v[c], v[d], s[i], s[j]); tr[(rnd, name)] = o
            v[a], v[d], v[c], v[b] = o[4], o[5], o[6], o[7]
        s = [s[PERM[k]] for k in range(16)]
    tr['digest'] = tuple(v[i] ^ v[i + 8] for i in range(8))
    return tr

def ruleA_h1(h1):
    return (h1 & 1) == 0 and (h1 >> 16) & 1 == 0 and (h1 >> 17) & 1 == 0 and (h1 >> 1) & 1 == 1 and ((h1 >> 2) & 1) != ((h1 >> 3) & 1)

def ruleA_z(z):   # Lemma A: rule A on h1 = ROR(z, 24) ^ ROR(e1, 16) for an e1 of the class
    return ruleA_h1(ror(z & M32, 24) ^ ror(CLASS_VAL | 0xc, 16))


# == the counting machine ==
class Machine:
    def __init__(self, resident, mem=None):
        self.reg = dict(resident); self.resident = set(resident); self.mem = dict(mem or {})
        self.ops = {}; self.part = None; self.prog = []; self.loc = None   # trace (part, dst, srcs, location) for liveness
        # static per-lane bounds (exclusive) for all inputs: constants by value, other words < 2^32
        self.bnd = {k: (max(lanes(v)) + 1 if k in GLOBAL_NAMES else 1 << 32) for k, v in resident.items()}
        self.maxbnd = {}
    def fork(self):                          # same registers, bounds, memory; empty counts and trace
        m = copy.copy(self); m.reg, m.bnd, m.mem = dict(self.reg), dict(self.bnd), dict(self.mem)
        m.ops, m.prog, m.maxbnd = {}, [], {}; return m
    def _c(self, n=1): self.ops[self.part] = self.ops.get(self.part, 0) + n
    def op(self, kind, dst, a, b=None, imm=None):
        x = self.reg[a]; y = self.reg[b] if b is not None else None
        if kind == 'add': v = (x + y) & W256
        elif kind == 'xor': v = x ^ y
        elif kind == 'and': v = x & y
        elif kind == 'or': v = x | y
        elif kind == 'shr': v = x >> imm
        elif kind == 'shl': v = (x << imm) & W256
        else: raise ValueError(kind)
        self._c(); self.reg[dst] = v; self.tr(dst, [a] + ([b] if b is not None else []))
        ba = self.bnd[a]; bb = self.bnd[b] if b is not None else None
        if kind == 'add': nb = ba + bb - 1
        elif kind in ('xor', 'or'):
            B = 1 << 32   # an operand below 2^32 changes only the low 32 bits
            nb = -(-max(ba, bb) // B) * B if min(ba, bb) <= B else 1 << (max(ba, bb) - 1).bit_length()
        elif kind == 'and': nb = min(ba, bb)
        elif kind == 'shl': nb = ((ba - 1) << imm) + 1 if ((ba - 1) << imm) < (1 << LW) else (1 << LW) + 1   # > 2^36: polluted
        elif kind == 'shr': nb = (1 << LW) + 1 if imm else ba   # next lane's bits enter the top: polluted until masked
        if kind in ('add', 'xor', 'or'):
            assert ba <= (1 << LW) and bb <= (1 << LW), 'polluted operand %s %s' % (a, b)
        self.bnd[dst] = nb
        if kind == 'add':
            self.maxbnd[self.part] = max(self.maxbnd.get(self.part, 0), nb)
            assert v >> (LW * NL) == 0 and nb <= (1 << LW), 'bound exceeds lane'
        return v
    def tr(self, dst, srcs):                 # location: (code location, index) in shared quad code, else None
        self.prog.append((self.part, dst, srcs, self.loc and (self.loc, len(self.prog))))
    def sop(self, n, dst, srcs, val=None):   # n scalar operations (address or counter arithmetic, compare, branch)
        self._c(n); self.tr(dst, list(srcs))
        if dst is not None: self.reg[dst] = val
    def load(self, dst, val, addr_reg):
        self._c(); self.reg[dst] = val; self.tr(dst, [addr_reg])
        self.bnd[dst] = (max(lanes(val)) + 1) if dst in GLOBAL_NAMES else 1 << 32
    def ld(self, *ks):                       # words kept in memory: one load each where read
        for k in ks: self.load(k, self.mem[k], 'ptr')
    def store(self, name):                   # write a register to memory: 1 operation
        self._c(); self.tr(None, [name]); return self.reg[name]
    def cmp_branch(self, a, b):              # compare a with b, branch: 2 ops; returns a != b
        self._c(2); self.tr(None, [a, b]); return self.reg[a] != self.reg[b]
    def cmp_branch_zero(self, a):            # compare a with 0 (immediate), branch: 2 ops; returns a != 0
        self._c(2); self.tr(None, [a]); return self.reg[a] != 0
    def ror(self, dst, a, r):                # packed per-lane ROR by r: 5 ops; r = 16 reads A_16 twice (no B_16)
        self.op('shr', '_t1', a, imm=r); self.op('and', '_t1', '_t1', 'MA%d' % r)
        if r == 16: self.op('and', '_t2', a, 'MA16'); self.op('shl', '_t2', '_t2', imm=16)
        else: self.op('shl', '_t2', a, imm=32 - r); self.op('and', '_t2', '_t2', 'MB%d' % r)
        self.op('or', dst, '_t1', '_t2')

def masks(rs=(16, 12, 8, 7, 1)):
    d = {}
    for r in rs:
        d['MA%d' % r] = bc((1 << (32 - r)) - 1)
        if r != 16: d['MB%d' % r] = bc(((1 << r) - 1) << (32 - r))
    return d

GLOBAL_NAMES = {'M300', 'SEVEN', 'Fb', 'Gb', 'DY3'}
def batch_consts(b32=bc(1 << 32)):
    """the 20 global constants in registers during the batches"""
    g = masks((16, 12, 8, 7))
    g.update(M=bc(M32), R15=bc(rol(X15, 8)), nX15=bc((-X15) & M32), Y11=bc(Y11), Y11p=bc(Y11p), Y11K=bc((Y11 + KF) & M32),
             ETA=bc(ETA), ALLA=bc(ALLA), NALLA=bc((1 << 32) - ALLA), B32=b32, MFw=bc(MF), NMF=bc((1 << 32) - MF),
             STEP16=bc(1 << 16))
    GLOBAL_NAMES.update(g)
    return g
MEMG = dict(masks((1,)), DY3=bc(DY3)); GLOBAL_NAMES.update(MEMG)   # global words kept in memory
DN = ('nk4s4', 'nk4s3', 'nk4s2', 'nk4s')                          # C2.d1 of quad batch j = E + DN[j] after stage A

def outer_regs(o):
    """per-outer-step words of the batch (X14 = 0: none): seven registers, three in memory"""
    k4 = (o['S10'] + X15) & M32
    return (dict(k4=bc(k4), X13=bc(o['X13']), X9=bc(o['X9']), **{DN[j]: bc((-k4 - ((4 - j) << 16)) & M32) for j in range(4)}),
            dict(S15=bc(o['S15']), w5=bc(o['w5']), w5d=bc((o['w5'] + DELTA) & M32)))

def member_regs(o, y):
    """per-member words: five registers; y and e1 = y + Y3 in memory"""
    r = member_vals(o, y)
    return (dict(XAm=bc((r['C0.a1'] - o['X4']) & M32), X6m=bc(r['X6']), X1m=bc(r['X1']), Rm=bc(rol(r['D1.d1'], 16)),
                 Y12m=bc(r['Y12'])), dict(Ym=bc(y), E1m=bc((y + Y3) & M32)))

# == scalar pieces: outer step and member step (every primitive counted) ==
class Scalar:
    def __init__(self): self.n = 0
    def add(self, a, b): self.n += 2; return (a + b) & M32          # add, mask
    def sub(self, a, b): self.n += 2; return (a - b) & M32
    def xor(self, a, b): self.n += 1; return a ^ b
    def ror(self, x, r): self.n += 4; return ror(x, r)              # shr, shl, or, and
    def rol(self, x, r): self.n += 4; return rol(x, r)
    def bc(self, v): self.n += 8; return bc(v)                      # broadcast (7), store
    def bcr(self, v): self.n += 7; return bc(v)                     # broadcast into a register
    def st(self, v): self.n += 1; return v                          # store a scalar word

def outer_step(six):
    """Step O in scalar form; packed words of the table (9) and the batch (10), broadcast and stored; scalar words of the
    member step (9); next w5; after the table build, loads of 7 per-outer and 20 global batch registers.  D3.d1 = X3."""
    S = Scalar(); c0c, c0d, d3d, s15, s9, w5 = six
    assert d3d == X3
    s2 = S.add(K2A + K2B & M32, w5); s14 = S.ror(S.xor(K2D, s2), 8); s10 = S.add(K2C, s14); s6 = S.ror(S.xor(K2B, s10), 7)
    d3a = S.xor(rol(X3, 16), s14); d3c = S.add(s9, X3); d3b = S.sub(X3, d3a); s4 = S.xor(S.rol(d3b, 12), d3c)
    s3 = S.sub(d3a, s4); x9 = d3c; x4 = S.ror(S.xor(d3b, x9), 7)
    k3d = S.xor(S.rol(s15, 8), s3); k3c = S.add(IV[3], k3d); k3b = S.ror(S.xor(IV[7], k3c), 12); s11 = S.add(k3c, s15)
    s7 = S.ror(S.xor(k3b, s11), 7); k3a = S.xor(S.rol(k3d, 16), 11); w6 = S.sub(k3a, IV[3] + IV[7] & M32); w7 = S.sub(S.sub(s3, k3a), k3b)
    x8 = S.sub(c0c, c0d); cb = S.ror(S.xor(x4, c0c), 12); d2b = S.xor(rol(X7, 7), x8); d2c = S.xor(S.rol(d2b, 12), s7)
    x13 = S.sub(x8, d2c); k4 = S.add(s10, X15)
    mem = dict(nD2bW=S.bc(S.sub(S.sub(0, d2b), W13)), RX13=S.bc(S.rol(x13, 8)), nS2S7=S.bc(S.sub(S.sub(0, s2), s7)),
               S9p1=S.bc(S.add(s9, 1)), S9=S.bc(s9), omS6=S.bc(S.sub(1, s6)), D2cp1=S.bc(S.add(d2c, 1)), RS4=S.bc(S.rol(s4, 7)),
               w7=S.bc(w7),
               k4=S.bc(k4), X13=S.bc(x13), X9=S.bc(x9), S15=S.bc(s15), w5=S.bc(w5), w5d=S.bc(S.add(w5, DELTA)),
               **{DN[j]: S.bc(S.sub(-((4 - j) << 16) & M32, k4)) for j in range(4)},
               sCb=S.st(cb), snCc=S.st(S.sub(0, c0c)), sCd=S.st(c0d), skCa=S.st(S.sub(S.sub(0, cb), w6)),
               sRCd=S.st(S.rol(c0d, 16)), sS6=S.st(s6), snS11=S.st(S.sub(0, s11)), snX4=S.st(S.sub(0, x4)), sw7=S.st(w7))
    S.n += 4 + 2
    S.n += 7 + 20
    return mem, S.n

def outer_step_rand(r, c0d, w5):
    """a fresh 256-bit word r (1); C0.c1, S15, S9 from its words 0-2 (5); D3.d1 = X3; step O"""
    six = [r & M32, c0d, X3, (r >> 32) & M32, (r >> 64) & M32, w5]
    mem, n = outer_step(six)
    return mem, n + 6, six

def rand_word(seven, extra):
    """the 256-bit word with the coin words C0.c1, S15, S9 of a context as words 0..2"""
    return seven[0] | seven[3] << 32 | seven[4] << 64 | (extra & ((1 << 160) - 1)) << 96

def alg(w):
    """the algorithm's context: D3.d1 (word 2) = X3"""
    w = list(w); w[2] = X3; return w

def expected_mem(o):
    """the words step O must leave"""
    r, mw = outer_regs(o)
    return dict(nD2bW=bc(-o['D2.b1'] - W13 & M32), RX13=bc(rol(o['X13'], 8)), nS2S7=bc(-o['S2'] - o['S7'] & M32),
                S9p1=bc(o['S9'] + 1 & M32), S9=bc(o['S9']), omS6=bc(1 - o['S6'] & M32), D2cp1=bc(o['D2.c1'] + 1 & M32),
                RS4=bc(rol(o['S4'], 7)), w7=bc(o['w7']), **r, **mw, sCb=o['C0.b1'], snCc=-o['C0.c1'] & M32,
                sCd=o['C0.d1'], skCa=-o['C0.b1'] - o['w6'] & M32, sRCd=rol(o['C0.d1'], 16), sS6=o['S6'],
                snS11=-o['S11'] & M32, snX4=-o['X4'] & M32, sw7=o['w7'])

def member_step(mem, y):
    """loads; step Y; c = X6 + w7; pointer of group 0; five member registers, y and e1 stored; four D slots := D0S
    (load, store each); group counter := 0; next member (3)"""
    S = Scalar(); S.n += 1 + 9
    Cb, nCc, Cd, kCa, RCd, S6, nS11, nX4, w7 = (mem[k] for k in ('sCb', 'snCc', 'sCd', 'skCa', 'sRCd', 'sS6', 'snS11', 'snX4', 'sw7'))
    Y12 = S.add(S.xor(S.rol(y, 7), Cb), nCc); ca = S.add(S.xor(S.rol(Y12, 8), Cd), kCa); X12 = S.xor(ca, RCd)
    dc = S.sub(X11, X12); X6 = S.ror(S.xor(S.ror(S.xor(S6, dc), 12), X11), 7); dd = S.add(dc, nS11)
    X1 = S.xor(S.rol(X12, 8), dd); R = S.rol(dd, 16); XA = S.add(ca, nX4); e1 = S.add(y, Y3)
    c = S.add(X6, w7); ptr = S.sub(0, c) << 3; S.n += 1
    regs = dict(XAm=S.bcr(XA), X6m=S.bcr(X6), X1m=S.bcr(X1), Rm=S.bcr(R), Y12m=S.bcr(Y12)); mw = dict(Ym=S.bc(y), E1m=S.bc(e1))
    S.n += 8 + 1 + 3
    return regs, mw, ptr, c, S.n
# == the X2 table (per outer step, every primitive counted) ==
TBL_LOADS = ('nD2bW', 'RX13', 'nS2S7', 'S9p1', 'S9', 'omS6', 'D2cp1', 'RS4', 'w7')
def table_machine(mem):
    """table build of one outer step: masks, constants, nine outer words, X2 word (lanes l 2^14 - 1), each loaded once
    per outer step, and the pointer reset (part 'E')"""
    g = masks((24, 20, 16, 12, 7)); g.update(M=bc(M32), ONE=bc(1), nIV1=bc((-IV[1]) & M32), IV15p1=bc((IV[1] + IV[5] + 1) & M32),
                                             IV5=bc(IV[5]), IV4=bc(IV[4]), nIV0=bc((-IV[0]) & M32), nIV04=bc((-IV[0] - IV[4]) & M32))
    GLOBAL_NAMES.update(g)
    r = dict(g, **{k: mem[k] for k in TBL_LOADS}, X2w=pack([((l << KS) - 1) & M32 for l in range(NL)]), ptr=0)
    m = Machine(r); m.part = 'E'; m._c(len(r))
    return m

def table_word(m):
    """One table word T[a]: next X2 word, step M per lane, eight words reduced below 2^32 and stored, loop step (3): 94
    operations; x - y is (y XOR M) + (x + 1)."""
    m.part = 'W'
    m.op('add', 'X2', 'X2w', 'ONE'); m.op('and', 'X2', 'X2', 'M'); m.reg['X2w'] = m.reg['X2']; m.bnd['X2w'] = 1 << 32
    m.op('add', 'k7', 'X2', 'w7')
    m.op('add', 'd2a', 'X2', 'nD2bW')
    m.op('xor', 'd2d', 'X2', 'RX13')
    m.ror('S13', 'd2d', 16); m.op('xor', 'S13', 'S13', 'd2a')
    m.op('add', 'kw12', 'd2a', 'nS2S7')
    m.op('xor', 'k1c', 'S13', 'M'); m.op('add', 'k1c', 'k1c', 'S9p1')
    m.op('add', 'k1d', 'k1c', 'nIV1')
    m.ror('S1', 'S13', 24); m.op('xor', 'S1', 'S1', 'k1d')
    m.op('xor', 'kA', 'S1', 'M'); m.op('add', 'kA', 'kA', 'omS6'); m.op('and', 'kA', 'kA', 'M'); m.store('kA')
    m.op('add', 'kAw12', 'kw12', 'kA'); m.op('and', 'kAw12', 'kAw12', 'M'); m.store('kAw12')
    m.ror('k1a', 'k1d', 16)
    m.op('xor', 'nw2', 'k1a', 'M'); m.op('add', 'nw2', 'nw2', 'IV15p1'); m.op('and', 'nw2', 'nw2', 'M'); m.store('nw2')
    m.op('xor', 'k1b', 'k1c', 'IV5'); m.ror('k1b', 'k1b', 12)
    m.op('add', 'w3', 'k1a', 'k1b'); m.op('xor', 'w3', 'w3', 'M'); m.op('add', 'w3', 'w3', 'S1')
    m.op('add', 'w3', 'w3', 'ONE'); m.op('and', 'w3', 'w3', 'M'); m.store('w3')
    m.op('xor', 'S5', 'k1b', 'S9'); m.ror('S5', 'S5', 7); m.store('S5')
    m.op('xor', 's8', 'd2d', 'M'); m.op('add', 's8', 's8', 'D2cp1')
    m.op('xor', 'k0b', 's8', 'RS4')
    m.ror('k0c', 'k0b', 20); m.op('xor', 'k0c', 'k0c', 'IV4')
    m.op('xor', 'S12', 'k0c', 'M'); m.op('add', 'S12', 'S12', 'ONE'); m.op('add', 'S12', 'S12', 's8')
    m.op('and', 'S12', 'S12', 'M'); m.store('S12')
    m.op('add', 'k0d', 'k0c', 'nIV0')
    m.ror('k0a', 'k0d', 16)
    m.op('add', 'T1', 'k0a', 'nIV04'); m.op('add', 'T1', 'T1', 'k7'); m.op('and', 'T1', 'T1', 'M'); m.store('T1')
    m.ror('S0', 'S12', 24); m.op('xor', 'S0', 'S0', 'k0d')
    m.op('add', 'kw8', 'S0', 'S5'); m.op('xor', 'kw8', 'kw8', 'M'); m.op('add', 'kw8', 'kw8', 'ONE')
    m.op('and', 'kw8', 'kw8', 'M'); m.store('kw8')
    m.sop(3, None, ['ptr'])
    return {k: m.reg[k] for k in ('nw2', 'T1', 'S5', 'w3', 'S12', 'kAw12', 'kA', 'kw8')}, m.reg['X2w']

def want_word(o, a):
    vs = [middle(o, (a + (l << KS)) & M32) for l in range(NL)]
    return dict(nw2=pack([-v['w2'] & M32 for v in vs]), T1=pack([(v['X2'] + v['w7'] + v['w0']) & M32 for v in vs]),
                S5=pack([v['S5'] for v in vs]), w3=pack([v['w3'] for v in vs]), S12=pack([v['S12'] for v in vs]),
                kAw12=pack([(v['w12'] - v['S1'] - v['S6']) & M32 for v in vs]), kA=pack([(-v['S1'] - v['S6']) & M32 for v in vs]),
                kw8=pack([(-v['S0'] - v['S5']) & M32 for v in vs]))


# == groups, blocks and budgets ==
# Lemma A3: K' = (d1 AND 0300) + F[(d1 >> 24) AND 15]; in a group d1 = i 2^16 + D, so K' changes every 256 positions
# (block b = i >> 8: d1 bits 24..27 = b AND 15).  NR + G[b] = 2^33 - K' with NR = (D AND 0300) XOR M.
FK = [(0 if b & 1 else 1 << 24) | (b & 2) << 24 | 1 << 26 | ((b >> 2 ^ b >> 3) & 1) << 27 for b in range(NBLK)]
GK = [(1 << 32) + 1 - f for f in FK]
def kprime(d1): return (d1 & 0x300) + FK[(d1 >> 24) & 15]
RLAST = [(NL * (NBATCH - 1) + l) % NRV for l in range(NL)]   # 262,143 and 0..5: lanes 1..6 repeat group 0 (masked)
DLAST = [dval(r) for r in RLAST]
B32_01 = sum(1 << (LW * l + 32) for l in range(NLAST))      # bits 32 of the distinct lanes of the last group (lane 0)
D0S = [[dval(NL * k + l) for l in range(NL)] for k in range(4)]   # initial D slots (groups 0..3); slot g mod 4 gains 7
PSTEP, PMASK = (7 << KS) << 3, (1 << 35) - 1   # pointer step and mask (8 words per table entry)
def rvals(g): return RLAST if g == NBATCH - 1 else [NL * g + l for l in range(NL)]
def base(c, g): return (7 * g * NPOS - c) & M32

def budget_check(m):
    """before each group: cB, cC compared with 2^14, branch to the halt if below (2 + 2); True iff the run continues"""
    go = True
    for name in ('cB', 'cC'):
        m.sop(2, None, [name]); go = go and m.reg[name] >= NPOS
    return go

def count(m, name, flow):
    """an entry of stage B or C: budget minus 1 (1 op); a forced entry counts without subtracting"""
    m._c(1); m.tr(name, [name])
    if flow: m.reg[name] -= 1; assert m.reg[name] >= 0, 'budget register below 0'

def group_setup(m, Dslot, last):
    """halt test (4), D from slot g mod 4 (last group DLAST, B32 := lane 0), E = k4 + D, X6R = X6 + (D AND 0300),
    NR = (D AND 0300) XOR M, D + 7 stored back"""
    m.part = 'G'
    go = budget_check(m)
    if last: m.load('D', pack(DLAST), 'ptr'); m.load('B32', B32_01, 'ptr')
    else: m.load('D', Dslot, 'ptr')
    m.bnd['D'] = 1 << 32
    m.op('add', 'E', 'D', 'k4')
    m.load('M300', bc(0x300), 'ptr'); m.op('and', 'DM', 'D', 'M300')
    m.op('add', 'X6R', 'X6m', 'DM'); m.op('xor', 'NR', 'DM', 'M')
    nxt = None
    if not last: m.load('SEVEN', bc(7), 'ptr'); m.op('add', 'D', 'D', 'SEVEN'); nxt = m.store('D')
    m.bnd['E'] = (1 << 33) + (1 << 30)
    return go, nxt

def group_end(m, last):
    """next pointer (2), group counter (load, add, store, compare, branch), jump to the next copy (1); after the last
    group B32 is restored (load)"""
    if last: m.part = 'N'; m.load('B32', bc(1 << 32), 'ptr'); return
    m.part = 'L'
    m.sop(2, 'ptr', ['ptr'], (m.reg['ptr'] + PSTEP) & PMASK)
    m.sop(1, 'gc', ['ptr'], 0); m.sop(1, 'gc', ['gc'], 0); m.sop(1, None, ['gc']); m.sop(2, None, ['gc']); m.sop(1, None, [])

def block_update(m, b):
    """before positions 256 b ..: X6K = X6R + F[b], nKp = NR + G[b] = 2^33 - K' (4)"""
    m.part = 'U'
    m.load('Fb', bc(FK[b]), 'ptr'); m.op('add', 'X6K', 'X6R', 'Fb')
    m.load('Gb', bc(GK[b]), 'ptr'); m.op('add', 'nKp', 'NR', 'Gb')

# == the counted quad: stage A of four positions, the quad test, the hit tree, stages B and C, the continuation ==
def stage_a(m, W, j):
    """position j of the quad (16 ops): X0, fd, c1 = fd + E (E = k4 + C2.d1), E + 2^16, b1 = ROR(X6 ^ c1, 12),
    Z = T1 + X6K + b1 = C2.a2 + K', flag pA = (Z AND ALLA) + (2^32 - ALLA) (bit 32: rule A, Lemma A3)"""
    s = str(j)
    m.load('NW2', W['nw2'], 'ptr'); m.op('add', 'X0', 'XAm', 'NW2'); m.op('xor', 'fd' + s, 'X0', 'R15')
    m.op('add', 'c1' + s, 'fd' + s, 'E'); m.op('add', 'E', 'E', 'STEP16')
    m.op('xor', 'b1' + s, 'X6m', 'c1' + s); m.ror('b1' + s, 'b1' + s, 12)
    m.load('T1', W['T1'], 'ptr'); m.op('add', 'zK' + s, 'T1', 'X6K'); m.op('add', 'zK' + s, 'zK' + s, 'b1' + s)
    stage_a_flag(m, s)

def stage_a_flag(m, s):
    m.op('and', 'tA', 'zK' + s, 'ALLA'); m.op('add', 'pA' + s, 'tA', 'NALLA')

def quad_test(m):
    """Lemma P4: ((pA0 OR pA1) OR (pA2 OR pA3)) AND B32 is 0 iff no lane taking part passes rule A (6 ops)"""
    m.op('or', 'U3', 'pA0', 'pA1'); m.op('or', 'U12', 'pA2', 'pA3'); m.op('or', 'U15', 'U3', 'U12')
    m.op('and', 'x15', 'U15', 'B32')
    return m.cmp_branch_zero('x15')

# hit tree (proof.md Section 5): (W, parts, subtree if (OR of parts) AND B32 != 0, else); leaf = S
TREE = (3, (3,), (1, (1,), (14, (2, 12), (2, (2,), (4, (4,), (8, (8,), 15, 7), (8, (8,), 11, 3)), (4, (4,), (8, (8,), 13, 5), 9)), 1),
        (12, (12,), (4, (4,), (8, (8,), 14, 6), 10), 2)), (4, (4,), (8, (8,), 12, 4), 8))
WORDS = ('zK', 'c1', 'b1', 'fd', 'xA')
SPILL = {15: {3: WORDS}}   # leaf -> {batch: words stored after the tree and loaded before its stage B} (part H)

def hit_tree(m, S=None):
    """walk TREE: OR two built words if new (1), AND B32 (1), compare with 0, branch (2); S forces the branches.  Returns
    the leaf and per leaf batch xA = pA AND B32: a tested word meeting the leaf only there, else pA AND B32 (1)"""
    built = {1: 'pA0', 2: 'pA1', 4: 'pA2', 8: 'pA3', 3: 'U3', 12: 'U12'}; tested = {}; node = TREE; m.loc = 'T'
    while isinstance(node, tuple):
        W, parts, nz, z = node
        if W not in built: built[W] = 'U%d' % W; m.op('or', built[W], *(built[p] for p in parts))
        x = tested[W] = 'x%d' % W; m.op('and', x, built[W], 'B32'); r = m.cmp_branch_zero(x)
        r = r if S is None else bool(S & W); node = nz if r else z; m.loc += '%d%s' % (W, 'nz'[not r])
    xa = {}; m.loc = None
    for j in range(4):
        if node >> j & 1:
            xa[j] = next((t for W, t in tested.items() if W & node == 1 << j), None)
            if xa[j] is None: xa[j] = 'xA%d' % j; m.op('and', xa[j], 'pA%d' % j, 'B32')
    return node, xa

def stage_b(m, W, s, dn, xa, flow):
    """stage B (66 ops; 65 without the count in the continuation): C2.d1 = E + DN[j], C2.a2 = Z + nKp, z, X10; C2, D0,
    C1 and E1 to c1; the test of rule A and the filter on the lanes of xA (Lemma F2)"""
    if flow is not None: m.part = 'B'; count(m, 'cB', flow)
    m.op('add', 'd1', 'E', dn); m.op('add', 'a2', 'zK' + s, 'nKp'); m.op('xor', 'z', 'a2', 'd1')
    m.op('add', 'X10', 'fd' + s, 'k4'); m.ror('Y14', 'z', 8); m.op('add', 'c2', 'c1' + s, 'Y14')
    m.op('xor', 'Y6', 'b1' + s, 'c2'); m.ror('Y6', 'Y6', 7); m.op('add', 'fc', 'X10', 'nX15')
    m.load('S5', W['S5'], 'ptr'); m.op('xor', 'X5', 'fc', 'S5'); m.ror('X5', 'X5', 12); m.op('xor', 'X5', 'X5', 'X10'); m.ror('X5', 'X5', 7)
    m.load('w3', W['w3'], 'ptr'); m.op('add', 'p1', 'X1m', 'X5'); m.op('add', 'p1', 'p1', 'w3')
    m.op('xor', 'p2', 'p1', 'X13'); m.ror('p2', 'p2', 16); m.op('add', 'p3', 'p2', 'X9')
    m.op('xor', 'p4', 'p3', 'X5'); m.ror('p4', 'p4', 12)
    m.load('S12', W['S12'], 'ptr'); m.op('xor', 'ga', 'Rm', 'S12'); m.op('add', 'sY', 'p1', 'p4'); m.op('add', 'sY', 'sY', 'ga')
    m.load('kAw12', W['kAw12'], 'ptr'); m.op('add', 'A1', 'sY', 'Y6'); m.op('add', 'A1', 'A1', 'kAw12')
    m.op('xor', 'D1', 'A1', 'Y12m'); m.ror('D1', 'D1', 16); m.op('add', 'C1K', 'D1', 'Y11K')
    return stage_b_test(m, xa)

def stage_b_test(m, xa):
    m.op('and', 'wF', 'C1K', 'MFw'); m.op('add', 'pF', 'wF', 'NMF'); m.op('and', 'xF', 'pF', xa)
    return m.cmp_branch_zero('xF')

def ea_test(m, w, x):
    """some lane of x (bit 32) has w = 0 (low 32 bits): ((w AND M) + M) AND x != x (5 ops)"""
    m.op('and', 'T', w, 'M'); m.op('add', 'u', 'T', 'M'); m.op('and', 'v', 'u', x)
    return m.cmp_branch('v', x)

def e3(m, W):   # C1 and E3: Y1, Y13, Y9, h1, h1' = h1 ^ eta, g1, g1' (21)
    m.load('kA', W['kA'], 'ptr'); m.op('add', 'Y1', 'sY', 'kA'); m.op('xor', 'Y13', 'p2', 'Y1'); m.ror('Y13', 'Y13', 8)
    m.op('add', 'Y9', 'p3', 'Y13'); m.ld('E1m'); m.op('xor', 'h1', 'Y14', 'E1m'); m.ror('h1', 'h1', 16)
    m.op('xor', 'h1p', 'h1', 'ETA'); m.op('add', 'g1', 'Y9', 'h1'); m.op('add', 'g1p', 'Y9', 'h1p')

def e1(m):      # E1 of A and B to a2, a2' and P = a2 ^ a2' (21)
    m.op('add', 'C1', 'D1', 'Y11'); m.op('xor', 'b', 'C1', 'Y6'); m.ror('b', 'b', 12)
    m.op('add', 'C1p', 'D1', 'Y11p'); m.op('xor', 'bp', 'C1p', 'Y6'); m.ror('bp', 'bp', 12)
    m.ld('w5'); m.op('add', 'a2', 'A1', 'b'); m.op('add', 'a2', 'a2', 'w5')
    m.ld('w5d'); m.op('add', 'a2p', 'A1', 'bp'); m.op('add', 'a2p', 'a2p', 'w5d'); m.op('xor', 'P', 'a2', 'a2p')

def stage_c(m, W, flow):
    """stage C with the early exit (61 ops): the count, E3 to g1, g1', E1 to P, the test word
    W4 = P ^ ROR(P, 1) ^ ROR(g1 ^ g1', 12) (Lemma E), the early-exit test on the lanes of xF"""
    m.part = 'C'; count(m, 'cC', flow); e3(m, W)
    m.op('xor', 'Gd', 'g1', 'g1p'); m.ror('Fd', 'Gd', 12); e1(m)
    m.ld('MA1', 'MB1'); m.ror('W4', 'P', 1); m.op('xor', 'W4', 'W4', 'P'); m.op('xor', 'W4', 'W4', 'Fd')
    return ea_test(m, 'W4', 'xF')

def cont_budget(m, flow):
    """load cR, compare with 0 and branch to the halt, subtract 1, store (5); True iff the run continues"""
    m.load('cR', m.mem['cR'], 'ptr'); go = m.cmp_branch_zero('cR'); m.sop(1, 'cR', ['cR'], m.reg['cR'] - 1); m.store('cR')
    if flow and go: m.mem['cR'] -= 1
    return go

def cont(m, W, j, flow, out):
    """continuation (part K): its budget (5); batch j recomputed from its table words, E and the resident words: stage A
    to xA, stage B without the count, 5ca02dfb's full residual D1, D3, W4 = ROL(D4, 7) ^ D1, D6 (Lemmas D, D') and the
    exact test on the lanes of xF (8); taken: step 3"""
    m.part = 'K'; out['go'] = cont_budget(m, flow)
    m.load('NW2', W['nw2'], 'ptr'); m.op('add', 'X0', 'XAm', 'NW2'); m.op('xor', 'fdk', 'X0', 'R15')
    m.op('add', 'kd1', 'E', DN[j]); m.op('add', 'c1k', 'fdk', 'kd1'); m.op('add', 'c1k', 'c1k', 'k4')
    m.op('xor', 'b1k', 'X6m', 'c1k'); m.ror('b1k', 'b1k', 12)
    m.load('T1', W['T1'], 'ptr'); m.op('add', 'zKk', 'T1', 'X6K'); m.op('add', 'zKk', 'zKk', 'b1k')
    stage_a_flag(m, 'k'); m.op('and', 'xAk', 'pAk', 'B32'); stage_b(m, W, 'k', DN[j], 'xAk', None); e3(m, W); e1(m)
    m.op('xor', 'd2', 'a2', 'D1'); m.ror('d2', 'd2', 8); m.op('xor', 'd2p', 'a2p', 'D1'); m.ror('d2p', 'd2p', 8)
    m.op('add', 'cc', 'C1', 'd2'); m.op('add', 'ccp', 'C1p', 'd2p'); m.op('xor', 'Q', 'cc', 'ccp')
    m.op('xor', 'R6', 'b', 'bp'); m.op('xor', 'R6', 'R6', 'Q'); m.ror('R6', 'R6', 7)
    m.ld('Ym'); m.op('xor', 'f1', 'Ym', 'g1'); m.ror('f1', 'f1', 12); m.op('xor', 'f1p', 'Ym', 'g1p'); m.ror('f1p', 'f1p', 12)
    m.ld('S15'); m.ror('fa', 'fdk', 16); m.op('xor', 'fa', 'fa', 'S15'); m.load('kw8', W['kw8'], 'ptr')
    m.op('add', 'ew', 'E1m', 'fa'); m.op('add', 'ew', 'ew', 'kw8'); m.op('add', 'e2', 'ew', 'f1')
    m.ld('DY3'); m.op('add', 'e2p', 'ew', 'f1p'); m.op('add', 'e2p', 'e2p', 'DY3')
    m.op('xor', 'h2', 'h1', 'e2'); m.ror('h2', 'h2', 8); m.op('xor', 'h2p', 'h1p', 'e2p'); m.ror('h2p', 'h2p', 8)
    m.op('add', 'g2', 'g1', 'h2'); m.op('add', 'g2p', 'g1p', 'h2p')
    m.op('xor', 'R1', 'P', 'g2'); m.op('xor', 'R1', 'R1', 'g2p'); m.op('xor', 'R3', 'e2', 'e2p'); m.op('xor', 'R3', 'R3', 'Q')
    m.ld('MA1', 'MB1'); m.ror('R4', 'P', 1); m.op('xor', 'R4', 'R4', 'P'); m.op('xor', 'R4', 'R4', 'f1'); m.op('xor', 'R4', 'R4', 'f1p')
    m.op('xor', 'R6', 'R6', 'h2'); m.op('xor', 'R6', 'R6', 'h2p')
    out.update(R1=m.reg['R1'], R3=m.reg['R3'], R4=m.reg['R4'], R6=m.reg['R6'], kxF=m.reg['xF'])
    m.op('or', 'TR', 'R1', 'R3'); m.op('or', 'TR', 'TR', 'R4'); m.op('or', 'TR', 'TR', 'R6')
    out['found'] = ea_test(m, 'TR', 'xF'); out['T'] = m.reg['T']; out['u'] = m.reg['u']

def run_quad(m, Ws, S=None, CS=15, KS=15):
    """positions 4q .. 4q + 3: stage A (64), quad test (6); if taken, hit tree and spills (H), then per leaf batch: stage
    B, stage C if xF != 0, the continuation if the early exit is taken (waiting words stored and reloaded, KS).  S forces
    the leaf, CS stage C, KS the continuation; budgets change only as in the staged flow."""
    outs = [{} for _ in range(4)]; m.part = m.loc = 'A'
    for j in range(4): outs[j]['E_used'] = m.reg['E']; stage_a(m, Ws[j], j); outs[j]['pA'] = m.reg['pA%d' % j]
    taken = quad_test(m); real = sum(1 << j for j in range(4) if m.reg['pA%d' % j] & m.reg['B32'])
    for j, o in enumerate(outs): o.update(decA=bool(taken and real >> j & 1), decB=False, ranC=False, decK=False, ranK=False)
    if not (taken if S is None else S): m.loc = None; return outs, 0
    m.part = 'H'; leaf, xa = hit_tree(m, S); sp = SPILL.get(leaf, {})
    nm = lambda i, w: xa[i] if w == 'xA' else w + str(i)
    held = {nm(i, w): (m.store(nm(i, w)), m.bnd[nm(i, w)]) for i, ws in sp.items() for w in ws}
    for j in range(4):
        if not leaf >> j & 1: continue
        m.part = 'H'
        for w in sp.get(j, ()): k = nm(j, w); v, b = held.pop(k); m.load(k, v, 'ptr'); m.bnd[k] = b
        o = outs[j]; fl = o['decA']
        o['decB'] = stage_b(m, Ws[j], str(j), DN[j], xa[j], fl) and fl; o['xF'] = m.reg['xF']
        if not (o['decB'] or (S and CS >> j & 1)): continue
        o['ranC'] = o['decB']; o['decK'] = stage_c(m, Ws[j], o['decB']) and o['decB']; o['W4'] = m.reg['W4']
        if not (o['decK'] or (S and KS >> j & 1)): continue
        wait = [nm(i, w) for i in range(j + 1, 4) if leaf >> i & 1 for w in WORDS if nm(i, w) not in held]
        m.part = 'KS'; k0 = m.ops.get('K', 0) + m.ops.get('KS', 0); sv = [(k, m.store(k), m.bnd[k]) for k in wait]
        o['ranK'] = o['decK']; cont(m, Ws[j], j, o['decK'], o)
        m.part = 'KS'
        for k, v, b in sv: m.load(k, v, 'ptr'); m.bnd[k] = b
        o['k_ops'] = m.ops.get('K', 0) + m.ops.get('KS', 0) - k0
    return outs, leaf

def liveness(prog, resident, U=None):
    """Peak registers: the resident ones plus every value (SSA version) live from its write to its last read; with U,
    the live sets at located (shared) instructions go to U[location] instead."""
    ver = {}; defs = []; uses = []
    for i, (_, d, srcs, _) in enumerate(prog):
        uses.append([(s, ver.get(s, 0)) for s in srcs if s not in resident])
        if d is not None and d not in resident:
            ver[d] = ver.get(d, 0) + 1; defs.append((d, ver[d]))
        else: defs.append(None)
    last = {}
    for i, us in enumerate(uses):
        for u in us: last[u] = i
    live = set(); peak = 0
    for i in range(len(prog)):
        if defs[i] is not None: live.add(defs[i])
        if U is not None and prog[i][3]: U.setdefault(prog[i][3], set()).update(live)
        else: peak = max(peak, len(resident) + len(live))
        for u in uses[i]:
            if last.get(u) == i: live.discard(u)
        if defs[i] is not None and last.get(defs[i], -1) <= i: live.discard(defs[i])
    return peak

def cfg_peak(progs, resident):
    """peak over the forced leaf paths; at an instruction shared by several paths (stage A, the quad test, the tree) the
    union of the values live on any of them"""
    U = {}; pk = max(liveness(p, resident, U) for p in progs)
    return max([pk] + [len(resident) + len(s) for s in U.values()])
# == Lemma B: the beta filter contains the six heaviest betas ==
T6 = (0x18b0e098, 0x18b1a098, 0x18d0e098, 0x18d1a098, 0x18b3e098, 0x18d3e098)
DY11 = (Y11p - Y11) & M32

def beta_conditions(beta):
    """The c1 with ROR(c1 ^ (c1 + DY11), 12) == beta: carry analysis of one addition.
    Returns (mask, value) of the bits of c1 that are fixed, or None if no c1 exists."""
    x = rol(beta, 12); carry = [0] * 33; mask = val = 0
    for i in range(32):
        carry[i] = ((x >> i) ^ (DY11 >> i)) & 1          # bit i of c1 ^ (c1 + D) is D_i ^ carry_i
    if carry[0] != 0: return None
    for i in range(31):
        d = (DY11 >> i) & 1
        if d == carry[i]:
            if carry[i + 1] != d: return None            # majority of (c, d, d) is d
        else:
            mask |= 1 << i; val |= carry[i + 1] << i     # majority of (c, 0, 1) is c: fixes bit i
    return mask, val

def lemma_b():
    """number of the six betas whose c1 set lies inside the filter (c1 & MF) == VF"""
    n = 0
    for b in T6:
        mv = beta_conditions(b)
        n += mv is not None and (mv[0] & MF) == MF and (mv[1] & MF) == VF
    return n

# == seeds ==
class Rng:
    def __init__(self, text): self.h = hashlib.shake_256(text if isinstance(text, bytes) else text.encode()); self.k = 0; self.buf = b''
    def getrandbits(self, n):
        nb = (n + 7) // 8
        while len(self.buf) < nb:
            self.buf += hashlib.shake_256(self.h.digest(32) + struct.pack('<Q', self.k)).digest(64); self.k += 1
        v = int.from_bytes(self.buf[:nb], 'little') & ((1 << n) - 1); self.buf = self.buf[nb:]; return v
    def randrange(self, n): return self.getrandbits(64) % n
    def choice(self, s): return s[self.randrange(len(s))]

def seed_trial(seed):
    w = struct.unpack('<8I', hashlib.shake_256(seed).digest(32))
    return alg(w[:7]), w[7] & (NMEM - 1)

def forward(v, y):
    A, B, w, wp = trial_words(v, y)
    ta, tb = trace(w, 55), trace(wp, 63)
    E1a, E1b = ta[(1, 'E1')], tb[(1, 'E1')]
    h1 = ta[(1, 'E3')][1]
    beta = E1a[3] ^ E1b[3]; eps = E1a[6] ^ E1b[6]
    dA, dB = ta['digest'], tb['digest']
    X = [ta[(0, c)] for c in ('E0', 'E1', 'E2', 'E3')]
    xs = {3: X[3][4], 7: X[2][7], 11: X[1][6], 15: X[0][5]}
    return dict(A=A, B=B, w=w, y4a=ta[(1, 'C0')][7], y4b=tb[(1, 'C0')][7], eta=h1 ^ tb[(1, 'E3')][1], h1=h1,
                ruleA=ruleA_h1(h1), c1=E1a[2], filt=(E1a[2] & MF) == VF, beta=beta, n=eps ^ rol(beta ^ eps, 1) ^ ETA,
                nd=(dA[3] ^ dB[3]) ^ rol(dA[6] ^ dB[6], 8), half=all(dA[i] == dB[i] for i in (0, 2, 5, 7)), dA=dA, dB=dB,
                pinned=xs == {3: X3, 7: X7, 11: X11, 15: X15})

def residual_words(f):
    """the four words the batch tests, from the two real digests: D1, D3, ROL(D4,7) ^ D1, D6 (Lemma D')"""
    D = {i: f['dA'][i] ^ f['dB'][i] for i in (1, 3, 4, 6)}
    return {'R1': D[1], 'R3': D[3], 'R4': rol(D[4], 7) ^ D[1], 'R6': D[6]}

def bit32(x, l): return (x >> (LW * l + 32)) & 1

class Case:
    """counted outer step, member step, end of group g - 1 (g > 0), set-up of group g, then quads; ok = every word the
    pieces leave equals the construction"""
    def __init__(self, seven, mi, g, extra=0):
        self.o = o = outer(seven[:6]); self.y = y = member(mi); self.g = g; self.last = last = g == NBATCH - 1
        self.mem, self.outer_ops, six = outer_step_rand(rand_word(seven, extra), seven[1], seven[5])
        ok = six == list(seven[:6]) and self.mem == expected_mem(o) and o['X14'] == 0
        regs, mw, ptr0, c, self.member_ops = member_step(self.mem, y)
        self.c = c; self.X6 = member_vals(o, y)['X6']; orr, omw = outer_regs(o)
        ok = ok and (regs, mw) == member_regs(o, y) and c == (self.X6 + o['w7']) & M32 and ptr0 == base(c, 0) << 3
        mem = dict(MEMG, **{k: self.mem[k] for k in omw}, **mw, cR=1 << 200)
        m = self.m = Machine(dict(batch_consts(), **{k: self.mem[k] for k in orr}, **regs, X6R=0, NR=0, E=0, X6K=0, nKp=0,
                                  cB=1 << 200, cC=1 << 200, ptr=ptr0), mem)
        if g: m.reg['ptr'] = base(c, g - 1) << 3; group_end(m, False)
        ok = ok and m.reg['ptr'] == base(c, g) << 3
        self.R = rvals(g); self.D = D = DLAST if last else [dval(r) for r in self.R]
        go, nxt = group_setup(m, None if last else pack(D), last)
        self.k4 = k4 = (o['S10'] + X15) & M32; self.E0 = m.reg['E']
        ok = ok and go and self.E0 == pack([k4 + d for d in D]) and lanes(m.reg['X6R']) == [self.X6 + (d & 0x300) for d in D]
        ok = ok and lanes(m.reg['NR']) == [M32 - (d & 0x300) for d in D] and (last or nxt == pack([d + 7 for d in D]))
        ok = ok and m.reg['B32'] == (B32_01 if last else bc(1 << 32))
        self.tm = table_machine(self.mem); self.ok = ok; self.blk = None; self.updates = 0; self.leafst = None
    def word(self, i):
        """table word of position i (counted), checked against step M"""
        o, c = self.o, self.c; a = base(c, self.g) + i
        tm = self.tm; tm.reg['X2w'] = pack([(a - 1 + (l << KS)) & M32 for l in range(NL)])
        n0 = tm.ops.get('W', 0); W, X2w = table_word(tm); self.tw_ops = tm.ops['W'] - n0
        X2s = [(a + (l << KS)) & M32 for l in range(NL)]
        self.ok = self.ok and W == want_word(o, a) and X2w == pack(X2s)
        return W, X2s
    def leaf_paths(self, m, Ws):
        """every leaf S forced with stages B, C and the continuation for each batch: counts, largest continuation, peak"""
        st = {}; progs = []
        for S in range(1, 16):
            f = m.fork(); outs, leaf = run_quad(f, Ws, S, S, S); n = bin(S).count('1'); progs.append(f.prog)
            st[S] = (leaf == S, f.ops['A'], f.ops['H'], f.ops['B'] == B_OPS * n, f.ops['C'] == C_OPS * n,
                     max(o['k_ops'] for o in outs if 'k_ops' in o), liveness(f.prog, f.resident))
        self.leafst = st; self.cfgpk = cfg_peak(progs, m.resident)
    def quad(self, i, first, verify=None, leaves=False):
        """positions i .. i + 3 forced (every batch through stages B, C and the continuation) and in the staged flow on a
        fork (compared); per batch: lanes, flags and decisions right"""
        m, o, c, y = self.m, self.o, self.c, self.y; b = i >> 8
        if b != self.blk:
            block_update(m, b); self.blk = b; self.updates += 1; Kp = [kprime(((i << 16) + d) & M32) for d in self.D]
            self.ok = self.ok and lanes(m.reg['X6K']) == [self.X6 + k for k in Kp] and lanes(m.reg['nKp']) == [(1 << 33) - k for k in Kp]
        if first: m.reg['E'] = self.E0 + i * bc(1 << 16)
        WX = [self.word(i + j) for j in range(4)]; Ws = [w for w, _ in WX]
        if leaves: self.leaf_paths(m, Ws)
        mr = m.fork(); b0 = m.reg['cB'], m.reg['cC'], m.mem['cR']
        outs, _ = run_quad(m, Ws, 15); ro, leaf = run_quad(mr, Ws)
        d = {p: mr.ops.get(p, 0) for p in ('A', 'H', 'B', 'C', 'K', 'KS')}
        self.flow = n = (leaf, b0[0] - mr.reg['cB'], b0[1] - mr.reg['cC'], b0[2] - mr.mem['cR'])
        ok = all([x[k] for x in ro] == [x[k] for x in outs] for k in ('decA', 'decB', 'ranC', 'decK', 'ranK'))
        ok = ok and leaf == sum(1 << j for j in range(4) if outs[j]['decA']) and n[1] == bin(leaf).count('1')
        ok = ok and n[2] == sum(x['ranC'] for x in ro) and n[3] == sum(x['ranK'] for x in ro) and d['A'] == A_OPS
        ok = ok and d['H'] <= H_OPS * n[1] and d['B'] == B_OPS * n[1] and d['C'] == C_OPS * n[2] and d['K'] + d['KS'] <= K_OPS * n[3]
        ok = ok and all(mr.reg[k] == m.reg[k] for k in ('E', 'cB', 'cC')) and mr.mem['cR'] == m.mem['cR']
        self.ok = self.ok and ok and m.reg['E'] == self.E0 + (i + 4) * bc(1 << 16)
        res = []; anyA = False
        for j, (out, (W, X2s)) in enumerate(zip(outs, WX)):
            self.ok = self.ok and [(e - self.k4) & M32 for e in lanes(out['E_used'])] == [ror((x + c) & M32, 16) for x in X2s]
            self.ok = self.ok and all((x + c) & M32 == ((r << KS) + i + j) & M32 for x, r in zip(X2s, self.R))
            L = {k: lanes(out[k]) for k in ('R1', 'R3', 'R4', 'R6', 'W4', 'T', 'u')}; right = flags = 0; fs = []
            for l in range(NL):
                f = forward(middle(o, X2s[l]), y); fs.append(f); R = residual_words(f); f['R4'] = R['R4']
                lok = (in_S8(y) and f['half'] and f['pinned'] and f['y4a'] == y == f['y4b'] and f['eta'] == ETA and len(f['A']) == 55
                       and len(f['B']) == 63 and all(L[k][l] & M32 == R[k] for k in R) and L['W4'][l] & M32 == R['R4']
                       and L['T'][l] == R['R1'] | R['R3'] | R['R4'] | R['R6'] and f['nd'] == f['n'] and L['u'][l] >> 32 & 1 == (f['dA'] != f['dB']))
                if verify is not None:
                    lok = lok and struct.unpack('<8I', verify(f['A'], 2)) == f['dA'] and struct.unpack('<8I', verify(f['B'], 2)) == f['dB']
                af = int((not self.last or l < NLAST) and f['ruleA'] and f['filt'])
                right += lok; flags += bit32(out['pA'], l) == f['ruleA'] and bit32(out['xF'], l) == af == bit32(out['kxF'], l)
            val = fs[:NLAST] if self.last else fs; AF = [f for f in val if f['ruleA'] and f['filt']]
            wA = any(f['ruleA'] for f in val); anyA = anyA or wA
            dec = (out['decA'] == wA and out['decB'] == bool(AF) and out['decK'] == any(f['R4'] == 0 for f in AF)
                   and out['found'] == any(f['dA'] == f['dB'] for f in AF))
            res.append([right, flags, dec, out, fs])
        for r in res: r[2] = int(r[2] and bool(leaf) == anyA)
        return res

def check_run(seven, mi, g, pos, verify=None, extra=0, leaves=False):
    """quads at positions pos (0 mod 4); after the last group its end"""
    cs = Case(seven, mi, g, extra); right = flags = decs = 0; allf = []; outs = []; cs.nat = [0, 0, 0]
    for k, i in enumerate(pos):
        for r, fl, dc, out, fs in cs.quad(i, k == 0, verify, leaves and k == 0):
            right += r; flags += fl; decs += dc; allf.append(fs); outs.append(out)
        cs.nat = [a + b for a, b in zip(cs.nat, cs.flow[1:])]     # staged-flow entries of B, C, continuation
    if cs.last: group_end(cs.m, True)
    return cs, right, flags, decs, outs, allf

A_OPS, B_OPS, H_OPS, C_OPS, K_OPS = 70, 66, 10, 61, 235   # stage A per quad; hit tests and spills per stage-B entry
OUTER_OPS, TABLE_ENTRY_OPS, TABLE_WORD_OPS, MEMBER_OPS = 324, 28, 94, 120
GROUP_PARTS = {False: {'G': 13, 'L': 8}, True: {'G': 11, 'N': 1}}   # set-up and end
GROUP_OPS, GROUP_LAST_OPS, BLOCK_OPS = 21, 12, 4

def group_right(cs):
    """group set-up, end of group g - 1 (L) and of the last group (N) as in the ledger"""
    o = cs.m.ops; w = GROUP_PARTS[cs.last]
    return int(o['G'] == w['G'] and o.get('L', 0) == (8 if cs.g else 0) and o.get('N', 0) == (1 if cs.last else 0))

def obs_common(cs, outs):
    o = cs.m.ops; nq = len(outs) // 4
    return {'stage_a_ops': o['A'] // nq, 'stage_b_ops': o['B'] // len(outs), 'stage_c_ops': o['C'] // len(outs),
            'hit_spill_ops': o['H'] // nq, 'cont_ops': max(x['k_ops'] for x in outs), 'outer_ops': cs.outer_ops,
            'table_word_ops': cs.tw_ops, 'member_ops': cs.member_ops, 'group_ops_right': group_right(cs),
            'block_ops': o['U'] // cs.updates, 'pieces_right': int(cs.ok)}

def ex_half(seed):
    seven, mi = seed_trial(seed)
    o = outer(seven[:6]); a1 = (seven[6] + member_vals(o, member(mi))['X6'] + o['w7']) & M32
    r, i = a1 >> KS, a1 & (NPOS - 1); g = r // NL
    cs, right, flags, decs, outs, allf = check_run(seven, mi, g, [i & ~3], extra=int.from_bytes(hashlib.shake_256(seed + b'r').digest(16), 'little'))
    f = allf[i & 3][r - NL * g]
    return f['A'], f['B'], dict(obs_common(cs, outs), lanes_right=right, flags_right=flags, decisions_right=decs,
                                member_in_s8=int(in_S8(member(mi))))

def ex_class(seed):
    seven, mi = seed_trial(seed)
    w = struct.unpack('<2I', hashlib.shake_256(seed + b'g').digest(8))
    g, i0 = w[0] % (NBATCH - 1), 256 * (w[1] % (NBLK - 1)) + 252
    cs, right, flags, decs, outs, allf = check_run(seven, mi, g, [i0, i0 + 4, i0 + 8],
                                                   extra=int.from_bytes(hashlib.shake_256(seed + b'r').digest(16), 'little'))
    fl = [f for fs in allf for f in fs]
    obs = dict(trials=len(fl), y4_equal=sum(f['y4a'] == cs.y == f['y4b'] for f in fl), eta_equal=sum(f['eta'] == ETA for f in fl),
               lanes_right=right, flags_right=flags, decisions_right=decs, pieces_right=int(cs.ok),
               group_ops_right=group_right(cs), block_updates=cs.updates, lemma_b=lemma_b(),
               rule_a_lanes=sum(f['ruleA'] for f in fl), filter_lanes=sum(f['filt'] for f in fl),
               filter_and_rule_a_lanes=sum(f['ruleA'] and f['filt'] for f in fl),
               stage_b_batches=cs.nat[0], stage_c_batches=cs.nat[1], cont_batches=cs.nat[2])
    return allf[0][0]['A'], allf[0][0]['B'], {k: int(v) for k, v in obs.items()}

def pattern_tests(rng):
    """Constructed words: (1) flags and quad test: 128 rule-A patterns on each batch, others failing, and on batch 0 with
    random others; (2) the hit tree: every S, three lane patterns each, full and last-group B32; (3) early-exit, (4) exact
    and (5) stage-B tests: all 128 x 128 lane patterns"""
    res = dict(stage_a_patterns=0, stage_a_right=0, tree_patterns=0, tree_right=0, ea_patterns=0, ea_right=0,
               exact_patterns=0, exact_right=0, stage_b_patterns=0, stage_b_right=0)
    BC = batch_consts(); m = Machine(dict(BC, ptr=0)); m.part = 'P'
    def put(k, v, b): m.reg[k] = v; m.bnd[k] = b
    def zk_lane(ok):
        while True:
            d1 = rng.getrandbits(32); z = rng.getrandbits(32)
            if ok: z = (z | 0x300 | 1 << 25) & ~(1 << 24 | 1 << 27) | (1 - (z >> 26 & 1)) << 27
            elif rng.getrandbits(1): z ^= 1 << (8, 9, 24, 25, 27)[rng.randrange(5)]
            if ruleA_z(z) == ok: return ((z ^ d1) + kprime(d1)) + (rng.randrange(3) << 32)
    for rep in range(5):
        for P in range(128):
            pats = [P if j == rep or (rep == 4 and j == 0) else (rng.getrandbits(NL) if rep == 4 else 0) for j in range(4)]
            for j in range(4): put('zK%d' % j, pack([zk_lane(pats[j] >> l & 1) for l in range(NL)]), 1 << 35); stage_a_flag(m, str(j))
            ok = quad_test(m) == any(pats) and all(bit32(m.reg['pA%d' % j] & m.reg['B32'], l) == pats[j] >> l & 1 for j in range(4) for l in range(NL))
            res['stage_a_patterns'] += 1; res['stage_a_right'] += ok
    for last in (False, True):
        put('B32', B32_01 if last else BC['B32'], (1 << 32) + 1); part = 1 if last else 0x7f
        for S in range(16):
            for rep in range(3):
                for j in range(4):
                    p = (rng.getrandbits(NL) & part or 1 << rng.randrange(NLAST if last else NL)) if S >> j & 1 else 0
                    p |= rng.getrandbits(NL) & ~part & 0x7f
                    put('pA%d' % j, pack([1 << 32 if p >> l & 1 else (1 << 32) - 1 - rng.randrange(ALLA) for l in range(NL)]), (1 << 32) + 1)
                ok = quad_test(m) == (S > 0)
                if S:
                    leaf, xa = hit_tree(m); ok = ok and leaf == S and all(m.reg[xa[j]] == m.reg['pA%d' % j] & m.reg['B32'] for j in xa)
                res['tree_patterns'] += 1; res['tree_right'] += ok
    put('B32', BC['B32'], (1 << 32) + 1)
    def word(zm):
        return sum(((0 if zm >> l & 1 else (rng.getrandbits(32) if rng.getrandbits(1) else 1 << rng.randrange(32)) or 1)
                    | rng.getrandbits(4) << 32) << (LW * l) for l in range(NL))
    for Z in range(128):
        for X in range(128):
            put('xF', pack([(X >> l & 1) << 32 for l in range(NL)]), (1 << 32) + 1)
            put('W4', word(Z), 1 << LW); res['ea_patterns'] += 1; res['ea_right'] += ea_test(m, 'W4', 'xF') == (Z & X != 0)
            zs = [rng.getrandbits(NL) | Z for _ in range(4)]
            for k, w in enumerate(('R1', 'R3', 'R4', 'R6')): put(w, word(zs[k]), 1 << LW)
            m.op('or', 'TR', 'R1', 'R3'); m.op('or', 'TR', 'TR', 'R4'); m.op('or', 'TR', 'TR', 'R6')
            res['exact_patterns'] += 1; res['exact_right'] += ea_test(m, 'TR', 'xF') == (zs[0] & zs[1] & zs[2] & zs[3] & X != 0)
            def c1_lane(ok):
                while True:
                    c = rng.getrandbits(33)
                    if (((c & M32) & MF) == VF) == ok: return c + KF
                    if ok: return ((c & ~MF) | VF) + KF
            put('xA', pack([(Z >> l & 1) << 32 for l in range(NL)]), (1 << 32) + 1)
            put('C1K', pack([c1_lane(X >> l & 1) for l in range(NL)]), (1 << 33) + KF)
            ok = stage_b_test(m, 'xA') == (Z & X != 0) and all(bit32(m.reg['xF'], l) == (Z & X) >> l & 1 for l in range(NL))
            res['stage_b_patterns'] += 1; res['stage_b_right'] += ok
            m.prog.clear()
    return res

def lemma_a3(rng):
    """Lemma A3: 64 x 64 patterns of the six bits of C2.d1 and C2.a2, four random fillings each: disagreements"""
    P = (8, 9, 24, 25, 26, 27); bad = 0
    for p in range(64):
        for q in range(64):
            for _ in range(4):
                d1 = rng.getrandbits(32) & ~0x0F000300; a2 = rng.getrandbits(32) & ~0x0F000300
                for t, bt in enumerate(P): d1 |= (p >> t & 1) << bt; a2 |= (q >> t & 1) << bt
                bad += (((a2 + (rng.randrange(3) << 32) + kprime(d1)) & ALLA) == ALLA) != ruleA_z(a2 ^ d1)
    return bad

def stage_rates():
    """Exact stage rates under M: passing patterns of the bits read (0-3, 16, 17 of h1; six filter bits of c1) times
    2^26; p_B = share of batches with a rule-A trial (37,449 groups of 7 distinct trials, one of 1; proof.md 8.2)."""
    RB = (0, 1, 2, 3, 16, 17); FB = [b for b in range(32) if MF >> b & 1]
    nA = sum(ruleA_h1(sum(((k >> i) & 1) << b for i, b in enumerate(RB))) for k in range(64)) << 26
    nF = sum((sum(((k >> i) & 1) << b for i, b in enumerate(FB)) & MF) == VF for k in range(64)) << 26
    nAF = nA * nF                                   # pairs (h1, c1) in 2^64; independent words under M
    q = 1 - Fraction(nA, 1 << 32); last = NLAST
    pB = ((NBATCH - 1) * (1 - q ** NL) + 1 - q ** last) / NBATCH
    return {'filter_bits': FB, 'ruleA_count': nA, 'ruleA_rate_log2': math.log2(nA / 2 ** 32), 'filter_count': nF,
            'ruleA_filter_count_2_64': nAF, 'ruleA_filter_rate_log2': math.log2(nAF / 2 ** 64),
            'p_B': [pB.numerator, pB.denominator], 'p_B_float': float(pB), 'full_batch_B': float(1 - q ** NL),
            'exact': nA == 1 << 27 and nF == 1 << 26 and nAF == 1 << 53 and last == 1 and NBATCH == 37450}, pB

# == the ledger of proof.md Section 9 (participant mode --ledger) ==
V_RANGE = 1512538                     # values of C0.d1: 0 .. V - 1
F_H1 = 92675072                       # the factor of H1 (185,350,144 / 2)
# H1 (ii): stage-B share <= [0] p_B, rule A and filter <= [1] 2^-11 (5ca02dfb's sample), and with W4 = 0 <= [2] (8.2)
PREMISE = (Fraction(377, 1000), Fraction(1003, 1000), Fraction(1, 1 << 24))
BUDGET = tuple(p * Fraction(6001, 6000) for p in PREMISE)   # budgets 1/6000 above the premises (5266c5ce)
def ledger():
    N = V_RANGE << 80; n_out = V_RANGE << 32; m_out = NBATCH * NPOS * NMEM
    sr, pB = stage_rates(); nb = n_out * m_out
    EB = -(-(BUDGET[0] * pB * nb) // 1); EC = -(-(BUDGET[1] * N) // 2048); ER = -(-(BUDGET[2] * N) // 1)
    body = NBLK * BLOCK_OPS + (NPOS // 4) * A_OPS
    per_member = MEMBER_OPS + (NBATCH - 1) * GROUP_OPS + GROUP_LAST_OPS + NBATCH * body
    per_outer = OUTER_OPS + TABLE_ENTRY_OPS + ((1 << 32) + NPOS) * TABLE_WORD_OPS + NMEM * per_member
    ops = n_out * per_outer + EB * (B_OPS + H_OPS) + EC * C_OPS + ER * K_OPS + (V_RANGE << 6) + (1 << 22) + (1 << 25)
    T = Fraction(ops, 430) + 2 + (1 << 86)
    lam = Fraction(N * F_H1, 1 << 128)
    out = {'premise': [str(p) for p in PREMISE], 'budget': [str(b) for b in BUDGET], 'E_B': EB, 'E_C': EC, 'E_R': ER}
    ex = []
    for name, cnt, mean, so, slack in (('B', EB, PREMISE[0] * pB * nb, B_OPS + H_OPS, NPOS), ('C', EC, PREMISE[1] * N / 2048, C_OPS, NPOS),
                                       ('R', ER, PREMISE[2] * N, K_OPS, 0)):
        muH = mean / m_out
        delta = Fraction(cnt - slack, m_out) / muH - 1
        ex.append(float(delta * delta * muH / 3))
        out[name] = {'budget_log2': math.log2(cnt), 'mu_H': float(muH), 'delta': float(delta), 'chernoff_exponent': ex[-1],
                     'ops_per_trial': float(Fraction(cnt * so, N))}
    tl = math.log2(T)
    out.update(N_log2=math.log2(N), per_outer=per_outer, per_member=per_member, fixed_per_trial=float(Fraction(n_out * per_outer, N)),
               ops_per_trial=float(Fraction(ops, N)), time_log2=round(tl, 6), claim=math.ceil(tl * 10000 - 1e-9) / 10000,
               lam=float(lam), success=1 - math.exp(-float(lam)) - 0.002 - sum(math.exp(-e) for e in ex), stage_rates=sr)
    print(json.dumps(out, indent=1))
    return 0

def dslot_test():
    """D slots: group g < 37,449 reads dval(7g + l) from slot g mod 4, stores +7; DLAST; (r, i) cover 2^32 once"""
    slots = [list(d) for d in D0S]; ok = True
    for g in range(NBATCH - 1):
        k = g & 3
        ok = ok and slots[k] == [dval(NL * g + l) for l in range(NL)]
        slots[k] = [d + 7 for d in slots[k]]
    rs = [r for g in range(NBATCH - 1) for r in rvals(g)] + rvals(NBATCH - 1)[:NLAST]
    ok = ok and DLAST == [dval(r) for r in RLAST] and sorted(rs) == list(range(NRV)) and NLAST == 1
    ok = ok and all(dval(r) == ((r & 3) << 30 | r >> 2) for r in range(0, NRV, 97))
    return int(ok)

def budget_test():
    """cB, cC = 2^14 k + r (k < 3, r = 0, 1, 2^14 - 1), 2^14 or random entries per group: at most E entries, never
    below 0, halt only below 2^14; cR = E < 4: exactly E continuations, then the halt"""
    ok = True; rng = Rng('budget test v103')
    for k in range(3):
        for r in (0, 1, NPOS - 1):
            for which in ('cB', 'cC'):
                E = NPOS * k + r
                for rep in range(2):
                    m = Machine(dict(cB=E if which == 'cB' else 1 << 200, cC=E if which == 'cC' else 1 << 200, ptr=0))
                    done = 0; m.part = 'G'
                    while budget_check(m):
                        m.part = 'B'
                        for _ in range(NPOS if rep == 0 else rng.randrange(NPOS + 1)): count(m, which, True); done += 1
                        m.prog.clear(); m.part = 'G'
                    ok = ok and done <= E and 0 <= m.reg[which] < NPOS and m.reg[which] == E - done
    for E in range(4):
        m = Machine(dict(ptr=0), dict(cR=E)); m.part = 'K'; done = 0
        while cont_budget(m, True): done += 1
        ok = ok and done == E and m.mem['cR'] == 0
    return int(ok)

LEDGER = {'A': 70, 'H': 29, 'B': 264, 'C': 244}   # forced quad (leaf 15) without the continuations
def selftest(N, seed):
    root = os.environ.get('S8_VERIFIER_ROOT') or os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), *(['..'] * 5)))
    try:
        sys.path.insert(0, root); from verifier.blake3 import blake3 as verify
    except Exception:
        verify = None
    rng = Rng('s8stage quad selftest %s' % seed)
    st = dict(cases=N, lanes=0, lanes_right=0, flags_right=0, decisions_right=0, pieces_right=0, group_ops_right=0,
              verifier_used=int(verify is not None), last_group_cases=0, leaf_cases=0, stage_b_batches=0, stage_c_batches=0, cont_batches=0)
    counts = None; same = True; maxbnd = {}; regs = tregs = 0; other = set(); leaves = {}; kmax = 0
    for case in range(N):
        cw = [rng.getrandbits(32) for _ in range(7)]
        if case % 5 == 4: cw = [rng.choice([0, M32, v]) for v in cw]
        cw = alg(cw)
        mi = (0, NMEM - 1)[case % 2] if case % 7 == 6 else rng.randrange(NMEM)
        g = NBATCH - 1 if case % 4 == 3 else (0 if case % 9 == 8 else rng.randrange(NBATCH - 1))
        i = (0, NPOS - 1, 256 * rng.randrange(NBLK))[case % 3] if case % 6 == 5 else rng.randrange(NPOS)
        lv = case % 10 == 0
        cs, right, flags, decs, outs, allf = check_run(cw, mi, g, [i & ~3], verify, rng.getrandbits(128), lv)
        st['lanes'] += 4 * NL; st['lanes_right'] += right; st['flags_right'] += flags; st['decisions_right'] += decs
        st['pieces_right'] += cs.ok; st['group_ops_right'] += group_right(cs); st['last_group_cases'] += cs.last
        for k, v in zip(('stage_b_batches', 'stage_c_batches', 'cont_batches'), cs.nat): st[k] += v
        bo = {k: cs.m.ops[k] for k in LEDGER}; kmax = max([kmax] + [o['k_ops'] for o in outs])
        if counts is None: counts = bo
        same = same and bo == counts and cs.m.ops['U'] == BLOCK_OPS
        other.add((cs.outer_ops, cs.member_ops, cs.tw_ops, cs.tm.ops['E']))
        for mm in (cs.m, cs.tm):
            for k, v in mm.maxbnd.items(): maxbnd[k] = max(maxbnd.get(k, 0), v)
        regs = max(regs, liveness(cs.m.prog, cs.m.resident))
        cs.tm.prog.append(('W', None, ['X2w'], None)); tregs = max(tregs, liveness(cs.tm.prog, cs.tm.resident))
        if lv:
            st['leaf_cases'] += 1; regs = max(regs, cs.cfgpk)
            for S, v in cs.leafst.items(): leaves.setdefault(S, set()).add(v)
    st['pattern_tests'] = pt = pattern_tests(rng)
    st['budget_test'] = budget_test(); st['dslot_test'] = dslot_test(); st['lemma_a3_bad'] = lemma_a3(rng)
    mem = [member(i) for i in range(NMEM)]
    s8 = len(set(mem)) == NMEM and all(in_S8(y) for y in mem)
    oo = sorted(other); lv = {S: sorted(v) for S, v in leaves.items()}
    lok = len(lv) == 15 and all(len(v) == 1 and v[0][:2] == (True, A_OPS) and v[0][2] <= H_OPS * bin(S).count('1') and v[0][3] and v[0][4]
                                and v[0][5] <= K_OPS and v[0][6] <= 64 for S, v in lv.items())
    st.update(counts=counts, same_counts=same, counts_equal_ledger=counts == LEDGER, cont_ops_max=kmax,
              leaf_paths={S: v[0][2:] for S, v in lv.items()}, leaf_paths_right=int(lok), outer_member_tableword_tableentry_ops=oo,
              static_bound_over_2_32={k: round(v / 2 ** 32, 3) for k, v in maxbnd.items()}, peak_registers=regs,
              batch_resident=len(cs.m.resident), table_peak_registers=tregs, s8_members=NMEM, s8_ok=int(s8), lemma_b=lemma_b())
    print(json.dumps(st, separators=(',', ':')))
    ok = (st['verifier_used'] == 1 and st['lanes_right'] == st['lanes'] and st['flags_right'] == st['lanes']
          and st['decisions_right'] == 4 * N and all(st[k] == N for k in ('pieces_right', 'group_ops_right'))
          and same and counts == LEDGER and lok and kmax <= K_OPS and oo == [(OUTER_OPS, MEMBER_OPS, TABLE_WORD_OPS, TABLE_ENTRY_OPS)]
          and max(maxbnd.values()) < 1 << LW and regs <= 64 and tregs <= 64 and s8 and st['lemma_b'] == 6 and st['lemma_a3_bad'] == 0
          and all(pt[k + '_right'] == pt[k + '_patterns'] for k in ('stage_a', 'tree', 'ea', 'exact', 'stage_b'))
          and st['budget_test'] == 1 and st['dslot_test'] == 1)
    return 0 if ok else 1

def main():
    if len(sys.argv) > 1:
        if sys.argv[1:] == ['--ledger']: raise SystemExit(ledger())
        if sys.argv[1] != '--selftest' or len(sys.argv) not in (3, 4):
            raise SystemExit('usage: s8stage.py --selftest N [seed] | --ledger   (no arguments: organizer request on stdin)')
        raise SystemExit(selftest(int(sys.argv[2]), sys.argv[3] if len(sys.argv) == 4 else '1'))
    req = json.load(sys.stdin)
    if req['schema_version'] != 1 or req['target_profile'] != 'blake3-r2-prefix-v1':
        raise ValueError('unexpected organizer target')
    run = {'half-collision': ex_half, 'class-filter': ex_class}[req['experiment_id']]
    out = []
    for t in req['trials']:
        a, b, obs = run(bytes.fromhex(t['seed']))
        out.append({'trial': t['trial'], 'message_a_hex': a.hex(), 'message_b_hex': b.hex(), 'observations': obs})
    json.dump({'schema_version': 1, 'trials': out}, sys.stdout, separators=(',', ':'), sort_keys=True)
    sys.stdout.write('\n')

if __name__ == '__main__':
    main()
