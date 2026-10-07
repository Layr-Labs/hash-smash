#!/usr/bin/env python3
"""Staged S8 search for 2-round BLAKE3 (blake3-r2-prefix-v1), order S2K14: trial generator, counted 64-register pieces,
exact stage rates, ledger and organizer experiments; implements proof.md (credits there).  winglock's c19feef program
(order S2K) with the lane stride 2^16 changed to 2^14 by Subflatus3 (KS; four D slots; last group of one lane).
Lane l of a batch: C2.a1 = (7g + l) 2^14 + i, group g < 37,450, position i < 2^14 (X2 = C2.a1 - X6 - w7; last group
lane 0 only).  Stage A 19 ops per batch, stage B 66, stage C 119 (proof.md Sections 4, 5).
Organizer mode: one JSON request on stdin, one JSON document out; standard library only; SHAKE-256 only expands seeds;
`trace` is the program's own 2-round compression.  Experiments: half-collision, class-filter.
  python3 s8stage.py --selftest N [seed]   (from the repository root; also checks digests with verifier/blake3.py)
  python3 s8stage.py --count [all]         (exact S8 count 185,350,144 and exact stage rates)
  python3 s8stage.py --ledger              (operation count, budgets, Chernoff exponents, time_log2)
"""
import hashlib, json, math, os, struct, sys
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
    def __init__(self, resident):
        self.reg = dict(resident); self.resident = set(resident)
        self.ops = {}; self.part = None; self.prog = []    # (part, dst, srcs) trace for liveness
        # static per-lane upper bounds (exclusive), valid for ALL inputs: constants by value, other words < 2^32
        self.bnd = {k: (max(lanes(v)) + 1 if k in GLOBAL_NAMES else 1 << 32) for k, v in resident.items()}
        self.maxbnd = {}
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
        self._c(); self.reg[dst] = v; self.prog.append((self.part, dst, [a] + ([b] if b is not None else [])))
        ba = self.bnd[a]; bb = self.bnd[b] if b is not None else None
        if kind == 'add': nb = ba + bb - 1
        elif kind in ('xor', 'or'):
            B = 1 << 32   # an operand below 2^32 changes only the low 32 bits: the guard part of the other is kept
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
    def sop(self, n, dst, srcs, val=None):   # n scalar operations (address or counter arithmetic, compare, branch)
        self._c(n); self.prog.append((self.part, dst, list(srcs)))
        if dst is not None: self.reg[dst] = val
    def load(self, dst, val, addr_reg):
        self._c(); self.reg[dst] = val; self.prog.append((self.part, dst, [addr_reg]))
        self.bnd[dst] = (max(lanes(val)) + 1) if dst in GLOBAL_NAMES else 1 << 32
    def store(self, name):                   # write a register to memory: 1 operation
        self._c(); self.prog.append((self.part, None, [name])); return self.reg[name]
    def cmp_branch(self, a, b):              # compare a with b, branch: 2 ops; returns a != b
        self._c(2); self.prog.append((self.part, None, [a, b])); return self.reg[a] != self.reg[b]
    def cmp_branch_zero(self, a):            # compare a with 0 (immediate), branch: 2 ops; returns a != 0
        self._c(2); self.prog.append((self.part, None, [a])); return self.reg[a] != 0
    def ror(self, dst, a, r):                # packed per-lane ROR by r: 5 ops, masks A_r, B_r resident
        self.op('shr', '_t1', a, imm=r); self.op('and', '_t1', '_t1', 'MA%d' % r)
        self.op('shl', '_t2', a, imm=32 - r); self.op('and', '_t2', '_t2', 'MB%d' % r)
        self.op('or', dst, '_t1', '_t2')

def masks(rs=(16, 12, 8, 7, 1)):
    d = {}
    for r in rs:
        d['MA%d' % r] = bc((1 << (32 - r)) - 1); d['MB%d' % r] = bc(((1 << r) - 1) << (32 - r))
    return d

GLOBAL_NAMES = {'M300', 'SEVEN', 'Fb', 'Gb'}
def batch_consts(b32=bc(1 << 32)):
    """the constants that stay in registers during the batches"""
    g = masks()
    g.update(M=bc(M32), R15=bc(rol(X15, 8)), nX15=bc((-X15) & M32), Y11=bc(Y11), Y11p=bc(Y11p), Y11K=bc((Y11 + KF) & M32),
             ETA=bc(ETA), DY3=bc(DY3), ALLA=bc(ALLA), NALLA=bc((1 << 32) - ALLA), B32=b32, MFw=bc(MF),
             NMF=bc((1 << 32) - MF), STEP16=bc(1 << 16))
    GLOBAL_NAMES.update(g)
    return g

def outer_regs(o):
    """the seven per-outer-step registers of the batch (X14 = 0: no register)"""
    k4 = (o['S10'] + X15) & M32
    return dict(k4=bc(k4), X13=bc(o['X13']), X9=bc(o['X9']), S15=bc(o['S15']), w5=bc(o['w5']),
                w5d=bc((o['w5'] + DELTA) & M32), nk4s=bc((-k4 - (1 << 16)) & M32))

def member_regs(o, y):
    """the seven per-member registers of the batch"""
    r = member_vals(o, y)
    return dict(XAm=bc((r['C0.a1'] - o['X4']) & M32), X6m=bc(r['X6']), X1m=bc(r['X1']), Rm=bc(rol(r['D1.d1'], 16)),
                Y12m=bc(r['Y12']), Ym=bc(y), E1m=bc((y + Y3) & M32))

# == scalar pieces: outer step and member step (every primitive counted) ==
class Scalar:
    def __init__(self): self.n = 0
    def add(self, a, b): self.n += 2; return (a + b) & M32          # add + mask
    def sub(self, a, b): self.n += 2; return (a - b) & M32          # subtract + mask
    def xor(self, a, b): self.n += 1; return a ^ b
    def ror(self, x, r): self.n += 4; return ror(x, r)              # shr, shl, or, and
    def rol(self, x, r): self.n += 4; return rol(x, r)
    def bc(self, v): self.n += 8; return bc(v)                      # broadcast to 7 lanes (7) and store (1)
    def bcr(self, v): self.n += 7; return bc(v)                     # broadcast into a register (7)
    def st(self, v): self.n += 1; return v                          # store a scalar word (1)

def outer_step(six):
    """Step O in scalar form; packed words of the table (9) and the batch (7), broadcast and stored; scalar words of the
    member step (9, stored); next w5; loads of the seven batch registers.  D3.d1 = X3, so X14 = 0 and X9 = D3.c1."""
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
               w7=S.bc(w7),                                                                   # table (step M)
               k4=S.bc(k4), X13=S.bc(x13), X9=S.bc(x9), S15=S.bc(s15), w5=S.bc(w5), w5d=S.bc(S.add(w5, DELTA)),
               nk4s=S.bc(S.sub(-(1 << 16) & M32, k4)),                                        # batch
               sCb=S.st(cb), snCc=S.st(S.sub(0, c0c)), sCd=S.st(c0d), skCa=S.st(S.sub(S.sub(0, cb), w6)),
               sRCd=S.st(S.rol(c0d, 16)), sS6=S.st(s6), snS11=S.st(S.sub(0, s11)), snX4=S.st(S.sub(0, x4)), sw7=S.st(w7))
    S.n += 4 + 2                       # next w5 (add, mask, compare, branch); its store and the store of w5 + delta
    S.n += 7                           # loads of the seven batch registers
    return mem, S.n

def outer_step_rand(r, c0d, w5):
    """Outer step of the run: draw a fresh 256-bit word r (1), take C0.c1, S15, S9 from its words 0-2 (5); D3.d1 = X3;
    then step O.  Returns (memory, operation count, six words)."""
    six = [r & M32, c0d, X3, (r >> 32) & M32, (r >> 64) & M32, w5]
    mem, n = outer_step(six)
    return mem, n + 6, six

def rand_word(seven, extra):
    """the 256-bit word whose words 0..2 are the coin words C0.c1, S15, S9 of a context; extra fills 3..7"""
    return seven[0] | seven[3] << 32 | seven[4] << 64 | (extra & ((1 << 160) - 1)) << 96

def alg(w):
    """the algorithm's context: D3.d1 (word 2) = X3"""
    w = list(w); w[2] = X3; return w

def expected_mem(o):
    """the words that step O must leave (from the lines of step O)"""
    return dict(nD2bW=bc(-o['D2.b1'] - W13 & M32), RX13=bc(rol(o['X13'], 8)), nS2S7=bc(-o['S2'] - o['S7'] & M32),
                S9p1=bc(o['S9'] + 1 & M32), S9=bc(o['S9']), omS6=bc(1 - o['S6'] & M32), D2cp1=bc(o['D2.c1'] + 1 & M32),
                RS4=bc(rol(o['S4'], 7)), w7=bc(o['w7']), **outer_regs(o), sCb=o['C0.b1'], snCc=-o['C0.c1'] & M32,
                sCd=o['C0.d1'], skCa=-o['C0.b1'] - o['w6'] & M32, sRCd=rol(o['C0.d1'], 16), sS6=o['S6'],
                snS11=-o['S11'] & M32, snX4=-o['X4'] & M32, sw7=o['w7'])

def member_step(mem, y):
    """Per member: loads; step Y; c = X6 + w7; pointer of group 0; seven member registers (broadcast); four D slots :=
    D0S (load, store each); group counter := 0; next member (3)."""
    S = Scalar(); S.n += 1 + 9
    Cb, nCc, Cd, kCa, RCd, S6, nS11, nX4, w7 = (mem[k] for k in ('sCb', 'snCc', 'sCd', 'skCa', 'sRCd', 'sS6', 'snS11', 'snX4', 'sw7'))
    Y12 = S.add(S.xor(S.rol(y, 7), Cb), nCc); ca = S.add(S.xor(S.rol(Y12, 8), Cd), kCa); X12 = S.xor(ca, RCd)
    dc = S.sub(X11, X12); X6 = S.ror(S.xor(S.ror(S.xor(S6, dc), 12), X11), 7); dd = S.add(dc, nS11)
    X1 = S.xor(S.rol(X12, 8), dd); R = S.rol(dd, 16); XA = S.add(ca, nX4); e1 = S.add(y, Y3)
    c = S.add(X6, w7); ptr = S.sub(0, c) << 3; S.n += 1
    regs = dict(XAm=S.bcr(XA), X6m=S.bcr(X6), X1m=S.bcr(X1), Rm=S.bcr(R), Y12m=S.bcr(Y12), Ym=S.bcr(y), E1m=S.bcr(e1))
    S.n += 8 + 1 + 3
    return regs, ptr, c, S.n

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
    """One table word T[a]: next X2 word (+1 per lane, mod 2^32), step M per lane, eight words reduced below 2^32 and
    stored (-w2, X2 + w7 + w0, S5, w3, S12, w12 - S1 - S6, -S1 - S6, -S0 - S5), loop step (3).  94 operations.  The lines
    are those of step M (function middle) on packed words; subtraction x - y is (y XOR M) + (x + 1)."""
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
# Lemma A3: with K' = (d1 AND 0300) + F[(d1 >> 24) AND 15] (F below), rule A holds for z = a2 ^ d1 iff bits 8, 9, 24,
# 25 and 27 of (a2 + K') mod 2^32 are all 1.  In a group d1 = i 2^16 + D (D = dval(7g + l), i < 2^14; d1 bits 16..29
# are i), so K' changes only every 256 positions (block b = i >> 8 gives d1 bits 24..27 = b AND 15).  G[b] = 2^32 + 1 - F[b], so that
# NR + G[b] = 2^33 - K' with NR = (D AND 0300) XOR M.
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
    """before each group: compare each budget register with 2^14 (an immediate) and branch to the halt if below
    (2 + 2 operations); a group has at most 2^14 entries of each stage.  Returns True iff the run continues."""
    go = True
    for name in ('cB', 'cC'):
        m.sop(2, None, [name]); go = go and m.reg[name] >= NPOS
    return go

def count_down(m, name):
    """an entry of stage B or C: budget register minus 1 (1 operation)"""
    m._c(1); m.prog.append((m.part, name, [name])); m.reg[name] -= 1
    assert m.reg[name] >= 0, 'budget register below 0'

def group_setup(m, Dslot, last):
    """before a group: halt test (4), acc = all ones, D = dval(7g + l) from slot g mod 4 (last group DLAST, B32 :=
    lane 0), E = k4 + D, X6R = X6 + (D AND 0300), NR = (D AND 0300) XOR M, D + 7 = dval(7 (g + 4) + l) stored back."""
    m.part = 'G'
    go = budget_check(m)
    m.load('acc', W256, 'ptr')
    if last: m.load('D', pack(DLAST), 'ptr'); m.load('B32', B32_01, 'ptr')
    else: m.load('D', Dslot, 'ptr')
    m.bnd['D'] = 1 << 32
    m.op('add', 'E', 'D', 'k4')
    m.load('M300', bc(0x300), 'ptr'); m.op('and', 'DM', 'D', 'M300')
    m.op('add', 'X6R', 'X6m', 'DM'); m.op('xor', 'NR', 'DM', 'M')
    nxt = None
    if not last: m.load('SEVEN', bc(7), 'ptr'); m.op('add', 'D', 'D', 'SEVEN'); nxt = m.store('D')
    m.bnd['E'] = (1 << 33) + (1 << 30)        # E grows by 2^16 per batch over 2^14 batches: below 2^33 + 2^30
    return go, nxt

def group_end(m, last):
    """after the block test of a group: next pointer (add, and), group counter (load, add, store, compare, branch) and
    the jump to the next copy of the group code (1); after the last group of a member, B32 is restored (load)."""
    if last: m.part = 'N'; m.load('B32', bc(1 << 32), 'ptr'); return
    m.part = 'L'
    m.sop(2, 'ptr', ['ptr'], (m.reg['ptr'] + PSTEP) & PMASK)
    m.sop(1, 'gc', ['ptr'], 0); m.sop(1, 'gc', ['gc'], 0); m.sop(1, None, ['gc']); m.sop(2, None, ['gc']); m.sop(1, None, [])

def block_update(m, b):
    """before positions 256 b .. 256 b + 255 of a group: X6K = X6R + F[b], nKp = NR + G[b] = 2^33 - K' (4 operations)"""
    m.part = 'U'
    m.load('Fb', bc(FK[b]), 'ptr'); m.op('add', 'X6K', 'X6R', 'Fb')
    m.load('Gb', bc(GK[b]), 'ptr'); m.op('add', 'nKp', 'NR', 'Gb')

# == the counted batch: three stages ==
def stage_a_test(m):
    """rule A from zK = C2.a2 + K' (Lemma A3); pA bit 32 = 1 iff the lane passes; branch: 5 operations"""
    m.op('and', 'tA', 'zK', 'ALLA')
    m.op('add', 'pA', 'tA', 'NALLA')            # bit 32 = 1 iff tA == ALLA
    m.op('and', 'xA', 'pA', 'B32')              # bits 32 only (last group: lanes 0, 1 only)
    return m.cmp_branch_zero('xA')              # True (enter stage B) iff some lane passes rule A

def stage_b_test(m):
    """rule A and the filter per lane from xA and c1K = c1 + KF of E1 (Lemma F2); branch: 5 operations"""
    m.op('and', 'wF', 'C1K', 'MFw')
    m.op('add', 'pF', 'wF', 'NMF')              # bit 32 = 1 iff wF == MF, i.e. iff the lane passes the filter
    m.op('and', 'xF', 'pF', 'xA')               # bit 32 = 1 iff the lane passes rule A and the filter; other bits 0
    return m.cmp_branch_zero('xF')              # True (enter stage C) iff some lane passes both

def run_batch(m, W, force=False):
    """One batch: W holds the eight table words at the position (loaded from ptr + 8 i + q).  force=True computes
    stages B and C whatever the decisions (for checking); accumulator and budgets change only as in the staged flow."""
    out = {}
    m.part = 'A'
    m.load('NW2', W['nw2'], 'ptr')              # table: -w2 per lane
    m.op('add', 'X0', 'XAm', 'NW2')             # X0 = C0.a1 - X4 - w2
    m.op('xor', 'fd', 'X0', 'R15')              # D0.d1 = ROL(X15,8) ^ X0
    out['E_used'] = m.reg['E']
    m.op('add', 'c1', 'fd', 'E')                # C2.c1 = X10 + C2.d1 = fd + S10 + X15 + C2.d1
    m.op('add', 'E', 'E', 'STEP16')             # the next position's E
    m.op('xor', 'b1', 'X6m', 'c1'); m.ror('b1', 'b1', 12)
    m.load('T1', W['T1'], 'ptr')                # table: X2 + w7 + w0 per lane
    m.op('add', 'zK', 'T1', 'X6K'); m.op('add', 'zK', 'zK', 'b1')   # C2.a2 + K' (C2.a1 = X2 + X6 + w7)
    out['decA'] = decA = stage_a_test(m); out['pA'] = m.reg['pA']
    if not (decA or force): return out
    m.part = 'B'
    if decA: count_down(m, 'cB')
    else: m._c(1); m.prog.append((m.part, 'cB', ['cB']))
    m.op('add', 'd1', 'E', 'nk4s')              # C2.d1 = E - k4 - 2^16
    m.op('add', 'a2', 'zK', 'nKp')              # C2.a2 (+ 2^33)
    m.op('xor', 'z', 'a2', 'd1')                # z = Y2 ^ C2.d1
    m.op('add', 'X10', 'fd', 'k4')
    m.ror('Y14', 'z', 8)
    m.op('add', 'c2', 'c1', 'Y14')              # Y10
    m.op('xor', 'Y6', 'b1', 'c2'); m.ror('Y6', 'Y6', 7)
    m.op('add', 'fc', 'X10', 'nX15')            # D0.c1 = X10 - X15
    m.load('S5', W['S5'], 'ptr')
    m.op('xor', 'X5', 'fc', 'S5'); m.ror('X5', 'X5', 12); m.op('xor', 'X5', 'X5', 'X10'); m.ror('X5', 'X5', 7)
    m.load('w3', W['w3'], 'ptr')
    m.op('add', 'p1', 'X1m', 'X5'); m.op('add', 'p1', 'p1', 'w3')       # C1.a1
    m.op('xor', 'p2', 'p1', 'X13'); m.ror('p2', 'p2', 16)              # C1.d1
    m.op('add', 'p3', 'p2', 'X9')                                      # C1.c1
    m.op('xor', 'p4', 'p3', 'X5'); m.ror('p4', 'p4', 12)               # C1.b1
    m.load('S12', W['S12'], 'ptr')
    m.op('xor', 'ga', 'Rm', 'S12')                                     # D1.a1 = ROL(D1.d1,16) ^ S12
    m.op('add', 'sY', 'p1', 'p4'); m.op('add', 'sY', 'sY', 'ga')       # sY = Y1 + S1 + S6
    m.load('kAw12', W['kAw12'], 'ptr')
    m.op('add', 'A1', 'sY', 'Y6'); m.op('add', 'A1', 'A1', 'kAw12')    # E1 a1 = Y1 + Y6 + w12
    m.op('xor', 'D1', 'A1', 'Y12m'); m.ror('D1', 'D1', 16)             # E1 d1 (shared)
    m.op('add', 'C1K', 'D1', 'Y11K')                                   # E1 c1 (A) + KF
    out['decB'] = decB = stage_b_test(m); out['xF'] = m.reg['xF']
    flowC = decA and decB
    if not (flowC or force): return out
    m.part = 'C'                                # second half of E1 for both messages
    if flowC: count_down(m, 'cC')
    else: m._c(1); m.prog.append((m.part, 'cC', ['cC']))
    m.op('add', 'C1', 'D1', 'Y11'); m.op('add', 'C1p', 'D1', 'Y11p')
    m.op('xor', 'b', 'C1', 'Y6'); m.ror('b', 'b', 12)
    m.op('xor', 'bp', 'C1p', 'Y6'); m.ror('bp', 'bp', 12)
    m.op('add', 'a2', 'A1', 'b'); m.op('add', 'a2', 'a2', 'w5')
    m.op('add', 'a2p', 'A1', 'bp'); m.op('add', 'a2p', 'a2p', 'w5d')
    m.op('xor', 'd2', 'a2', 'D1'); m.ror('d2', 'd2', 8)
    m.op('xor', 'd2p', 'a2p', 'D1'); m.ror('d2p', 'd2p', 8)
    m.op('add', 'cc', 'C1', 'd2'); m.op('add', 'ccp', 'C1p', 'd2p')
    m.op('xor', 'P', 'a2', 'a2p'); m.op('xor', 'Q', 'cc', 'ccp')
    m.op('xor', 'R6', 'b', 'bp'); m.op('xor', 'R6', 'R6', 'Q'); m.ror('R6', 'R6', 7)
    m.part = 'D'                                # Y1, Y13, Y9; E3 for both messages
    m.load('kA', W['kA'], 'ptr')
    m.op('add', 'Y1', 'sY', 'kA')                                      # Y1 = C1.a2
    m.op('xor', 'Y13', 'p2', 'Y1'); m.ror('Y13', 'Y13', 8)             # Y13 = C1.d2
    m.op('add', 'Y9', 'p3', 'Y13')                                     # Y9 = C1.c2
    m.op('xor', 'h1', 'Y14', 'E1m'); m.ror('h1', 'h1', 16)             # e1 = y + Y3 (member register)
    m.op('xor', 'h1p', 'h1', 'ETA')             # h1' = h1 ^ eta (Lemma T)
    m.op('add', 'g1', 'Y9', 'h1'); m.op('add', 'g1p', 'Y9', 'h1p')
    m.op('xor', 'f1', 'Ym', 'g1'); m.ror('f1', 'f1', 12)
    m.op('xor', 'f1p', 'Ym', 'g1p'); m.ror('f1p', 'f1p', 12)
    m.ror('fa', 'fd', 16); m.op('xor', 'fa', 'fa', 'S15')              # D0.a1 = ROL(D0.d1,16) ^ S15
    m.load('kw8', W['kw8'], 'ptr')
    m.op('add', 'ew', 'E1m', 'fa'); m.op('add', 'ew', 'ew', 'kw8')     # e1 + w8 (shared; e1' = e1 + DY3)
    m.op('add', 'e2', 'ew', 'f1')
    m.op('add', 'e2p', 'ew', 'f1p'); m.op('add', 'e2p', 'e2p', 'DY3')
    m.op('xor', 'h2', 'h1', 'e2'); m.ror('h2', 'h2', 8)
    m.op('xor', 'h2p', 'h1p', 'e2p'); m.ror('h2p', 'h2p', 8)
    m.op('add', 'g2', 'g1', 'h2'); m.op('add', 'g2p', 'g1p', 'h2p')
    m.part = 'R'                                # residual words, zero indicator, accumulator, jump back
    m.op('xor', 'R1', 'P', 'g2'); m.op('xor', 'R1', 'R1', 'g2p')       # D1 = (a2^a2') ^ (g2^g2')
    m.op('xor', 'R3', 'e2', 'e2p'); m.op('xor', 'R3', 'R3', 'Q')       # D3 = (e2^e2') ^ (c2^c2')
    m.ror('R4', 'P', 1); m.op('xor', 'R4', 'R4', 'P')                  # W4 = ROL(D4,7) ^ D1 = (f1^f1') ^ P ^ ROR(P,1)
    m.op('xor', 'R4', 'R4', 'f1'); m.op('xor', 'R4', 'R4', 'f1p')
    m.op('xor', 'R6', 'R6', 'h2'); m.op('xor', 'R6', 'R6', 'h2p')      # D6 = (b2^b2') ^ (h2^h2')
    out.update(R1=m.reg['R1'], R3=m.reg['R3'], R4=m.reg['R4'], R6=m.reg['R6'])
    m.op('or', 'T', 'R1', 'R3'); m.op('or', 'T', 'T', 'R4'); m.op('or', 'T', 'T', 'R6'); m.op('and', 'T', 'T', 'M')
    m.op('add', 'u', 'T', 'M')                  # bit 32 of a lane is 1 iff its R != 0
    acc0 = m.reg['acc']
    m.op('and', 'acc', 'acc', 'u')              # block accumulator
    if not flowC: m.reg['acc'] = acc0           # forced (checking) run only
    m._c(1); m.prog.append((m.part, None, []))  # jump back to the next position
    out['T'] = m.reg['T']; out['u'] = m.reg['u']; out['ranC'] = flowC
    return out

def block_test(m):
    """After the last batch of a group: branch to step 3 iff some lane of some batch that ran stage C had R = 0."""
    m.part = 'Z'
    m.load('B32z', bc(1 << 32), 'ptr'); m.op('and', 'acc', 'acc', 'B32z')
    return m.cmp_branch('acc', 'B32z')

def liveness(prog, resident):
    """Peak registers: the resident ones plus every value (SSA version) live from its write to its last read."""
    ver = {}; defs = []; uses = []
    for i, (_, d, srcs) in enumerate(prog):
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
        peak = max(peak, len(resident) + len(live))
        for u in uses[i]:
            if last.get(u) == i: live.discard(u)
        if defs[i] is not None and last.get(defs[i], -1) <= i: live.discard(defs[i])
    return peak

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
    xs = {3: X[3][4], 7: X[2][7], 11: X[1][6], 15: X[0][5]}   # X3 (a of D3), X7 (b of D2), X11 (c of D1), X15 (d of D0)
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
    """Counted outer step (from a random word holding the coin words), member step, end of group g - 1 (g > 0), set-up
    of group g, then batches; ok = every word the pieces leave equals the construction."""
    def __init__(self, seven, mi, g, extra=0):
        self.o = o = outer(seven[:6]); self.y = y = member(mi); self.g = g; self.last = last = g == NBATCH - 1
        self.mem, self.outer_ops, six = outer_step_rand(rand_word(seven, extra), seven[1], seven[5])
        ok = six == list(seven[:6]) and self.mem == expected_mem(o) and o['X14'] == 0
        regs, ptr0, c, self.member_ops = member_step(self.mem, y)
        self.c = c; self.X6 = member_vals(o, y)['X6']
        ok = ok and regs == member_regs(o, y) and c == (self.X6 + o['w7']) & M32 and ptr0 == base(c, 0) << 3
        m = self.m = Machine(dict(batch_consts(), **outer_regs(o), **regs, X6R=0, NR=0, E=0, X6K=0, nKp=0, acc=W256,
                                  cB=1 << 200, cC=1 << 200, ptr=ptr0))
        if g: m.reg['ptr'] = base(c, g - 1) << 3; group_end(m, False)
        ok = ok and m.reg['ptr'] == base(c, g) << 3
        self.R = rvals(g); self.D = D = DLAST if last else [dval(r) for r in self.R]
        go, nxt = group_setup(m, None if last else pack(D), last)
        self.k4 = k4 = (o['S10'] + X15) & M32; self.E0 = m.reg['E']
        ok = ok and go and self.E0 == pack([k4 + d for d in D]) and lanes(m.reg['X6R']) == [self.X6 + (d & 0x300) for d in D]
        ok = ok and lanes(m.reg['NR']) == [M32 - (d & 0x300) for d in D] and (last or nxt == pack([d + 7 for d in D]))
        ok = ok and m.reg['B32'] == (B32_01 if last else bc(1 << 32))
        self.tm = table_machine(self.mem); self.ok = ok; self.blk = None; self.updates = 0
    def batch(self, i, first, verify=None):
        m, o, c, y = self.m, self.o, self.c, self.y; b = i >> 8
        if b != self.blk:
            block_update(m, b); self.blk = b; self.updates += 1
            Kp = [kprime(((i << 16) + d) & M32) for d in self.D]
            self.ok = self.ok and lanes(m.reg['X6K']) == [self.X6 + k for k in Kp] and lanes(m.reg['nKp']) == [(1 << 33) - k for k in Kp]
        if first: m.reg['E'] = self.E0 + i * bc(1 << 16)    # E after i batches (stage A adds 2^16 per batch)
        a = base(c, self.g) + i                             # table index of the position (below 2^32 + 2^14)
        tm = self.tm; tm.reg['X2w'] = pack([(a - 1 + (l << KS)) & M32 for l in range(NL)])
        n0 = tm.ops.get('W', 0); W, X2w = table_word(tm); self.tw_ops = tm.ops['W'] - n0
        X2s = [(a + (l << KS)) & M32 for l in range(NL)]
        self.ok = self.ok and W == want_word(o, a) and X2w == pack(X2s)
        out = run_batch(m, W, force=True)
        self.ok = self.ok and [(e - self.k4) & M32 for e in lanes(out['E_used'])] == [ror((x + c) & M32, 16) for x in X2s]
        self.ok = self.ok and all((x + c) & M32 == ((r << KS) + i) & M32 for x, r in zip(X2s, self.R))
        Rw = {k: lanes(out[k]) for k in ('R1', 'R3', 'R4', 'R6')}; Tw = lanes(out['T']); Uw = lanes(out['u'])
        right = flags = 0; fs = []
        for l in range(NL):
            f = forward(middle(o, X2s[l]), y); fs.append(f); R = residual_words(f)
            lok = (in_S8(y) and f['half'] and f['pinned'] and f['y4a'] == y == f['y4b'] and f['eta'] == ETA and len(f['A']) == 55
                   and len(f['B']) == 63 and all((Rw[k][l] & M32) == R[k] for k in Rw) and Tw[l] == R['R1'] | R['R3'] | R['R4'] | R['R6']
                   and f['nd'] == f['n'] and (Uw[l] >> 32) & 1 == int(f['dA'] != f['dB']))
            if verify is not None:
                lok = lok and struct.unpack('<8I', verify(f['A'], 2)) == f['dA'] and struct.unpack('<8I', verify(f['B'], 2)) == f['dB']
            valid = not self.last or l < NLAST
            right += lok
            flags += bit32(out['pA'], l) == int(f['ruleA']) and bit32(out['xF'], l) == int(valid and f['ruleA'] and f['filt'])
        val = fs[:NLAST] if self.last else fs
        dec = int(out['decA'] == any(f['ruleA'] for f in val) and out['decB'] == any(f['ruleA'] and f['filt'] for f in val))
        return right, flags, dec, out, fs

def check_run(seven, mi, g, pos, verify=None, extra=0):
    """Batches at consecutive positions pos in the staged flow, the block test (right iff taken exactly when some lane
    of a batch that ran stage C has equal digests); after the last group its end."""
    cs = Case(seven, mi, g, extra); right = flags = decs = 0; allf = []; outs = []
    for k, i in enumerate(pos):
        r, fl, dc, out, fs = cs.batch(i, k == 0, verify); right += r; flags += fl; decs += dc; allf.append(fs); outs.append(out)
    taken = block_test(cs.m)
    want = any(f['dA'] == f['dB'] for out, fs in zip(outs, allf) if out['ranC'] for f in fs)
    if cs.last: group_end(cs.m, True)
    return cs, right, flags, decs, int(taken == want), outs, allf

LEDGER = {'A': 19, 'B': 66, 'C': 42, 'D': 56, 'R': 21}   # stage A 19; stage B 66; stage C 42 + 56 + 21 = 119
STAGE_OPS = (19, 66, 119)
OUTER_OPS, TABLE_ENTRY_OPS, TABLE_WORD_OPS, MEMBER_OPS = 274, 29, 94, 118
GROUP_PARTS = {False: {'G': 14, 'Z': 4, 'L': 8}, True: {'G': 12, 'Z': 4, 'N': 1}}   # set-up, block test, end
GROUP_OPS, GROUP_LAST_OPS, BLOCK_OPS = 26, 17, 4

def stage_ops(m): return m.ops['A'], m.ops['B'], m.ops['C'] + m.ops['D'] + m.ops['R']

def group_right(cs):
    """set-up and block test of the group as in the ledger; the end of the previous group (g > 0, part L) and the end
    of the last group (part N) likewise"""
    o = cs.m.ops; w = GROUP_PARTS[cs.last]
    return int(o['G'] == w['G'] and o['Z'] == w['Z'] and o.get('L', 0) == (8 if cs.g else 0) and o.get('N', 0) == (1 if cs.last else 0))

def obs_common(cs, outs):
    m = cs.m; sa, sb, sc = stage_ops(m); nb = len(outs)
    return {'stage_a_ops': sa // nb, 'stage_b_ops': sb // nb, 'stage_c_ops': sc // nb, 'block_test_ops': m.ops['Z'],
            'outer_ops': cs.outer_ops, 'table_word_ops': cs.tw_ops, 'member_ops': cs.member_ops,
            'group_ops_right': group_right(cs), 'block_ops': m.ops['U'] // cs.updates, 'pieces_right': int(cs.ok)}

def ex_half(seed):
    seven, mi = seed_trial(seed)
    o = outer(seven[:6]); a1 = (seven[6] + member_vals(o, member(mi))['X6'] + o['w7']) & M32
    r, i = a1 >> KS, a1 & (NPOS - 1); g = r // NL
    cs, right, flags, decs, br, outs, allf = check_run(seven, mi, g, [i], extra=int.from_bytes(hashlib.shake_256(seed + b'r').digest(16), 'little'))
    f = allf[0][r - NL * g]
    return f['A'], f['B'], dict(obs_common(cs, outs), lanes_right=right, flags_right=flags, decisions_right=decs, tests_right=br,
                                member_in_s8=int(in_S8(member(mi))))

def ex_class(seed):
    seven, mi = seed_trial(seed)
    w = struct.unpack('<2I', hashlib.shake_256(seed + b'g').digest(8))
    g, i0 = w[0] % (NBATCH - 1), 256 * (w[1] % (NBLK - 1)) + 252  # a group other than the last; positions across a block end
    cs, right, flags, decs, br, outs, allf = check_run(seven, mi, g, list(range(i0, i0 + 9)),
                                                        extra=int.from_bytes(hashlib.shake_256(seed + b'r').digest(16), 'little'))
    fl = [f for fs in allf for f in fs]
    obs = dict(trials=len(fl), y4_equal=sum(f['y4a'] == cs.y == f['y4b'] for f in fl), eta_equal=sum(f['eta'] == ETA for f in fl),
               lanes_right=right, flags_right=flags, decisions_right=decs, tests_right=br, pieces_right=int(cs.ok),
               group_ops_right=group_right(cs), block_updates=cs.updates, lemma_b=lemma_b(),
               rule_a_lanes=sum(f['ruleA'] for f in fl), filter_lanes=sum(f['filt'] for f in fl),
               filter_and_rule_a_lanes=sum(f['ruleA'] and f['filt'] for f in fl),
               stage_b_batches=sum(o['decA'] for o in outs), stage_c_batches=sum(o['ranC'] for o in outs))
    return allf[0][0]['A'], allf[0][0]['B'], {k: int(v) for k, v in obs.items()}

def pattern_tests(rng):
    """Constructed words: (1) zero indicator and block test, blocks of 1-3 batches, 128 lane patterns, twice; (2) stage
    A (Lemma A3), 128 rule-A patterns, random C2.d1, twice; (3) stage B, 16,384 rule-A and filter pattern pairs."""
    res = dict(ztest_patterns=0, ztest_right=0, stage_a_patterns=0, stage_a_right=0, stage_b_patterns=0, stage_b_right=0)
    def word(zero_mask):
        return sum(((0 if (zero_mask >> l) & 1 else (rng.getrandbits(32) if rng.getrandbits(1) else 1 << rng.randrange(32)) or 1)
                    | rng.getrandbits(4) << 32) << (LW * l) for l in range(NL))
    for k in (1, 2, 3):
        for P in range(128):
            for rep in range(2):
                m = Machine(dict(batch_consts(), ptr=0, acc=W256)); m.part = 'R'; want = False
                for b in range(k):
                    zm = P if b == k - 1 else (rng.getrandbits(NL) if rep else 0)
                    want = want or zm != 0
                    m.reg['T'] = word(zm); m.bnd['T'] = 1 << LW
                    m.op('and', 'T', 'T', 'M'); m.op('add', 'u', 'T', 'M'); m.op('and', 'acc', 'acc', 'u')
                taken = block_test(m)
                res['ztest_patterns'] += 1; res['ztest_right'] += (taken == want)
    def zk_lane(ok):
        while True:
            d1 = rng.getrandbits(32); z = rng.getrandbits(32)
            if ok: z = (z | 0x300 | 1 << 25) & ~(1 << 24 | 1 << 27) | (1 - (z >> 26 & 1)) << 27
            elif rng.getrandbits(1): z ^= 1 << (8, 9, 24, 25, 27)[rng.randrange(5)]
            if ruleA_z(z) == ok: return ((z ^ d1) + kprime(d1)) + (rng.randrange(3) << 32)
    for rep in range(2):
        for P in range(128):
            m = Machine(dict(batch_consts(), ptr=0, acc=W256)); m.part = 'A'
            m.reg['zK'] = pack([zk_lane((P >> l) & 1) for l in range(NL)]); m.bnd['zK'] = 1 << 35
            dec = stage_a_test(m)
            ok = dec == (P != 0) and all(bit32(m.reg['pA'], l) == ((P >> l) & 1) for l in range(NL))
            res['stage_a_patterns'] += 1; res['stage_a_right'] += ok
    for PA in range(128):
        for PF in range(128):
            m = Machine(dict(batch_consts(), ptr=0, acc=W256)); m.part = 'B'
            def c1_lane(ok):
                while True:
                    c = rng.getrandbits(33)
                    if (((c & M32) & MF) == VF) == ok: return c + KF   # the register holds c1 + KF
                    if ok: return ((c & ~MF) | VF) + KF
            m.reg['xA'] = pack([((PA >> l) & 1) << 32 for l in range(NL)]); m.bnd['xA'] = (1 << 32) + 1
            m.reg['C1K'] = pack([c1_lane((PF >> l) & 1) for l in range(NL)]); m.bnd['C1K'] = (1 << 33) + KF
            dec = stage_b_test(m)
            ok = dec == ((PA & PF) != 0) and all(bit32(m.reg['xF'], l) == ((PA & PF) >> l & 1) for l in range(NL))
            res['stage_b_patterns'] += 1; res['stage_b_right'] += ok
    return res

def lemma_a3(rng):
    """Lemma A3: 64 patterns of C2.d1 bits 8, 9, 24..27 times 64 of C2.a2 on them, four random fillings each (guard
    bits 0..2): disagreements with rule A on z = a2 ^ d1."""
    P = (8, 9, 24, 25, 26, 27); bad = 0
    for p in range(64):
        for q in range(64):
            for _ in range(4):
                d1 = rng.getrandbits(32) & ~0x0F000300; a2 = rng.getrandbits(32) & ~0x0F000300
                for t, bt in enumerate(P): d1 |= (p >> t & 1) << bt; a2 |= (q >> t & 1) << bt
                bad += (((a2 + (rng.randrange(3) << 32) + kprime(d1)) & ALLA) == ALLA) != ruleA_z(a2 ^ d1)
    return bad

# == exact model count of proof.md Section 8 (participant mode --count) ==
# A Python port of the participant's C counter (carry automata, exact integers, no sampling).
# The listed outcomes (tau per beta of T6, with its eps) are the 85 outcomes of the six betas;
# parts are non-negative, so the sum over any listed subset is a lower bound on r.
OUTCOMES = {
    0x18b0e098: (0x6e21be55, '175020a0 175060a0 185020a0 185060a0 275020a0 275060a0 285020a0 285060a0 385020a0 385060a0 '
                             '675020a0 675060a0 685020a0 685060a0'),
    0x18b1a098: (0x6e203e55, '185060a0 189060a0 18d060a0 195060a0 285060a0 289060a0 28d060a0 295060a0 385060a0 389060a0 '
                             '38d060a0 395060a0 685060a0 689060a0 68d060a0 695060a0'),
    0x18d0e098: (0x6e61be55, '175020a0 175060a0 17d020a0 185020a0 185060a0 275020a0 275060a0 27d020a0 285020a0 285060a0 '
                             '2850a0a0 385020a0 385060a0 675020a0 675060a0 67d020a0 685020a0 685060a0 6850a0a0'),
    0x18d1a098: (0x6e603e55, '185060a0 18d060a0 195060a0 285060a0 2850a0a0 28d060a0 28d0a0a0 295060a0 2950a0a0 385060a0 '
                             '38d060a0 395060a0 685060a0 6850a0a0 68d060a0 68d0a0a0 695060a0 6950a0a0'),
    0x18b3e098: (0x6e23be55, '185020a0 185060a0 195020a0 195060a0 285020a0 285060a0 295020a0 295060a0'),
    0x18d3e098: (0x6e63be55, '185020a0 185060a0 195020a0 195060a0 285020a0 285060a0 2850a0a0 295020a0 295060a0 2950a0a0'),
}

def popc(x): return bin(x).count('1')

def subs(m):
    """submasks of m in increasing order (the k-th one has pext index k)"""
    s = 0
    while True:
        yield s
        if s == m: return
        s = (s - m) & m

def pext(x, m):
    r = k = 0
    while m:
        lo = m & -m
        if x & lo: r |= 1 << k
        k += 1; m ^= lo
    return r

def solve_sub(Mk, D):
    """subsets S of Mk with sum_{i in Mk} (1 - 2[i in S]) 2^i == D mod 2^32"""
    t = (Mk - D) & M32
    if t & 1: return []
    return [s for s in (t >> 1, (t >> 1) | 1 << 31) if not s & ~Mk]

def aut1(Bc, nu, eps, fm1, fv1, fm2, fv2):
    """#(d1, d2): c1 = d1 + Y11, c1 + DY11 == c1 ^ Bc, (c1 + d2) ^ ((c1 ^ Bc) + (d2 ^ nu)) == eps,
    d1 = fv1 on fm1, d2 = fv2 on fm2 (16-state carry automaton over the 32 bit positions)"""
    st = {0: 1}
    for i in range(32):
        y, dy, bb, nb, e = (Y11 >> i) & 1, (DY11 >> i) & 1, (Bc >> i) & 1, (nu >> i) & 1, (eps >> i) & 1
        d1s = ((fv1 >> i) & 1,) if (fm1 >> i) & 1 else (0, 1)
        d2s = ((fv2 >> i) & 1,) if (fm2 >> i) & 1 else (0, 1)
        ns = {}
        for s, n in st.items():
            for d1 in d1s:
                t = d1 + y + (s & 1); c1 = t & 1; t2 = c1 + dy + ((s >> 1) & 1)
                if (t2 & 1) != c1 ^ bb: continue
                for d2 in d2s:
                    u = c1 + d2 + ((s >> 2) & 1); v = (c1 ^ bb) + (d2 ^ nb) + (s >> 3)
                    if (u ^ v) & 1 != e: continue
                    k = (t >> 1) | (t2 >> 1) << 1 | (u >> 1) << 2 | (v >> 1) << 3
                    ns[k] = ns.get(k, 0) + n
        st = ns
    return sum(st.values())

def N1(beta, tau, eps):
    """#(d1, b1, a2) in 2^96 (E1, message A) giving beta, tau = a2 ^ a2' and eps = c2 ^ c2'"""
    Bc, nu, tot = rol(beta, 12), ror(tau, 8), 0
    for pa in subs(tau):                                               # bits of a2 on tau
        w = len(solve_sub(beta, (tau - 2 * pa - DELTA) & M32))         # patterns of b1 on beta
        if w:
            for px in subs(tau):                                       # bits of d1 ^ a2 on tau
                tot += w * aut1(Bc, nu, eps, tau, pa ^ px, nu, ror(px, 8))
    return tot << (32 - popc(beta))

def aut3(Pm, Q, tau, pg, Irot, hv):
    """#(g1, h2): g1 = pg on Pm, h2 = hv on Irot, (g1 + h2) ^ ((g1 ^ Pm) + (h2 ^ Q)) == tau"""
    st = [1, 0, 0, 0]
    for i in range(32):
        p, q, t = (Pm >> i) & 1, (Q >> i) & 1, (tau >> i) & 1
        gs = ((pg >> i) & 1,) if p else (0, 1)
        hs = ((hv >> i) & 1,) if (Irot >> i) & 1 else (0, 1)
        ns = [0, 0, 0, 0]
        for s in range(4):
            if st[s]:
                for g in gs:
                    for h in hs:
                        u = g + h + (s & 1); v = (g ^ p) + (h ^ q) + (s >> 1)
                        if (u ^ v) & 1 == t: ns[(u >> 1) | (v >> 1) << 1] += st[s]
        st = ns
    return sum(st)

def N3(tau, eps, members, full):
    """(#rule A, #all or None) of (Y4 in members, h1, g1, e2) in E3 giving eta, psi = tau ^ ROR(tau,1), eps, tau"""
    psi = tau ^ ror(tau, 1); Pm = rol(psi, 12); Q = ror(ETA ^ eps, 8); I = ETA & eps; Irot = ror(I, 8)
    sh = 32 - popc(ETA | eps)
    me = [[pext(p & I, I) for p in solve_sub(eps, (DY3 + psi - 2 * ror(q, 12)) & M32)] for q in subs(Pm)]
    cnt = {}
    for y in members:
        k = pext(y, Pm); cnt[k] = cnt.get(k, 0) + 1
    NI = 1 << popc(I); groups = {}                                     # g1 pattern -> #h1 patterns per (I bits, rule A)
    for ph in subs(ETA):
        for sg in solve_sub(Pm, (ETA - 2 * ph) & M32):
            g = groups.setdefault(sg, [[0, 0] for _ in range(NI)]); g[pext(ph & I, I)][ruleA_h1(ph)] += 1
    tr = ta = 0
    for pg, phs in groups.items():
        if not full and not any(c[1] for c in phs): continue
        pgi = pext(pg, Pm)
        Fin = [aut3(Pm, Q, tau, pg, Irot, ror(m, 8)) << sh for m in subs(I)]
        Hm = [0] * NI
        for x, c in cnt.items():
            for b in me[x ^ pgi]: Hm[b] += c
        for a in range(NI):
            if phs[a][0] or phs[a][1]:
                s = sum(Hm[b] * Fin[a ^ b] for b in range(NI) if Hm[b])
                ta += s * (phs[a][0] + phs[a][1]); tr += s * phs[a][1]
    return tr, ta if full else None

def model_count(full):
    """r for S8 and the six betas of T6: sum of N1 * N3 / 2^80 (2^16 members, 2^64 for h1, g1, e2 of E3)"""
    S8 = [member(i) for i in range(NMEM)]
    tot_r = tot_a = nz = 0; parts = {}
    for beta, (eps, taus) in OUTCOMES.items():
        pr = pa = 0
        for t in taus.split():
            tau = int(t, 16); n1 = N1(beta, tau, eps); n3r, n3a = N3(tau, eps, S8, full) if n1 else (0, 0 if full else None)
            nz += n1 * n3r > 0; pr += n1 * n3r; pa += n1 * (n3a or 0)
            row = {'beta': '%08x' % beta, 'tau': t, 'eps': '%08x' % eps, 'N1': n1, 'N3_ruleA': n3r}
            if full: row['N3_all'] = n3a
            print(json.dumps(row), flush=True)
        parts['%08x' % beta] = (pr >> 80, pa >> 80, pr % (1 << 80) == 0 and pa % (1 << 80) == 0)
        tot_r += pr; tot_a += pa
    res = {'outcomes': sum(len(v[1].split()) for v in OUTCOMES.values()), 'nonzero_ruleA': nz,
           'part_ruleA': {k: v[0] for k, v in parts.items()}, 'part_all': {k: v[1] for k, v in parts.items()},
           'integral': all(v[2] for v in parts.values()), 'r_ruleA': tot_r / 2 ** 80, 'r_all': tot_a / 2 ** 80,
           'claimed_F': 92675072, 'margin_over_F': tot_r / 2 ** 80 / 92675072}
    if not full: del res['part_all'], res['r_all']
    sr = stage_rates()[0]; res['stage_rates'] = sr
    print(json.dumps(res))
    return 0 if tot_r == 185350144 << 80 and (not full or tot_a == tot_r) and sr['exact'] else 1


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
PREMISE = (Fraction(377, 1000), Fraction(1003, 1000))   # preregistered rule, proof.md 8.2; H1 (ii): stage-B share <= [0] p_B, rule A and filter <= [1] 2^-11
BUDGET = tuple(p * Fraction(6001, 6000) for p in PREMISE)   # budgets 1/6000 above the premises (5266c5ce)
def ledger():
    N = V_RANGE << 80; n_out = V_RANGE << 32; m_out = NBATCH * NPOS * NMEM
    sr, pB = stage_rates(); nb = n_out * m_out
    EB = -(-(BUDGET[0] * pB * nb) // 1); EC = -(-(BUDGET[1] * N) // 2048)
    body = NBLK * BLOCK_OPS + NPOS * STAGE_OPS[0]
    per_member = MEMBER_OPS + (NBATCH - 1) * GROUP_OPS + GROUP_LAST_OPS + NBATCH * body
    per_outer = OUTER_OPS + TABLE_ENTRY_OPS + ((1 << 32) + NPOS) * TABLE_WORD_OPS + NMEM * per_member
    ops = n_out * per_outer + EB * STAGE_OPS[1] + EC * STAGE_OPS[2] + (V_RANGE << 6) + (1 << 22) + (1 << 25)
    T = Fraction(ops, 430) + 2 + (1 << 86)
    lam = Fraction(N * F_H1, 1 << 128)
    out = {'premise': [str(p) for p in PREMISE], 'budget': [str(b) for b in BUDGET], 'E_B': EB, 'E_C': EC}
    ex = []
    for name, cnt, mean, so in (('B', EB, PREMISE[0] * pB * nb, STAGE_OPS[1]), ('C', EC, PREMISE[1] * N / 2048, STAGE_OPS[2])):
        muH = mean / m_out                  # upper bound on E[sum X_k], X_k = (entries of outer step k) / m_out
        delta = Fraction(cnt - NPOS, m_out) / muH - 1        # a halt needs more than E - 2^14 entries
        ex.append(float(delta * delta * muH / 3))
        out[name] = {'budget_log2': math.log2(cnt), 'mu_H': float(muH), 'delta': float(delta), 'chernoff_exponent': ex[-1],
                     'ops_per_trial': float(Fraction(cnt * so, N))}
    tl = math.log2(T)
    out.update(N_log2=math.log2(N), per_outer=per_outer, per_member=per_member,
               ops_per_trial=float(Fraction(ops, N)), time_log2=round(tl, 6), claim=math.ceil(tl * 10000 - 1e-9) / 10000,
               lam=float(lam), success=1 - math.exp(-float(lam)) - 0.002 - math.exp(-ex[0]) - math.exp(-ex[1]), stage_rates=sr)
    print(json.dumps(out, indent=1))
    return 0

def dslot_test():
    """D slots from D0S: group g < 37,449 reads dval(7g + l) from slot g mod 4, stores +7; DLAST; (r, i) cover 2^32 once."""
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
    """Budget E (= 2^14 k + r, k < 3, r = 0, 1, 2^14 - 1): at most E entries, never below 0, halt only below 2^14."""
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
                        for _ in range(NPOS if rep == 0 else rng.randrange(NPOS + 1)): count_down(m, which); done += 1
                        m.prog.clear(); m.part = 'G'
                    ok = ok and done <= E and 0 <= m.reg[which] < NPOS and m.reg[which] == E - done
    return int(ok)

def selftest(N, seed):
    root = os.environ.get('S8_VERIFIER_ROOT') or os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), *(['..'] * 5)))
    try:
        sys.path.insert(0, root); from verifier.blake3 import blake3 as verify
    except Exception:
        verify = None
    rng = Rng('s8stage S2K14 selftest %s' % seed)
    st = dict(cases=N, lanes=0, lanes_right=0, flags_right=0, decisions_right=0, tests_right=0, pieces_right=0,
              group_ops_right=0, verifier_used=int(verify is not None), last_group_cases=0, stage_b_batches=0, stage_c_batches=0)
    counts = None; same = True; maxbnd = {}; regs = tregs = resident = 0; other = set()
    for case in range(N):
        cw = [rng.getrandbits(32) for _ in range(7)]
        if case % 5 == 4: cw = [rng.choice([0, M32, v]) for v in cw]
        cw = alg(cw)
        mi = (0, NMEM - 1)[case % 2] if case % 7 == 6 else rng.randrange(NMEM)
        g = NBATCH - 1 if case % 4 == 3 else (0 if case % 9 == 8 else rng.randrange(NBATCH - 1))
        i = (0, NPOS - 1, 256 * rng.randrange(NBLK))[case % 3] if case % 6 == 5 else rng.randrange(NPOS)
        cs, right, flags, decs, br, outs, allf = check_run(cw, mi, g, [i], verify, extra=rng.getrandbits(128)); fs = allf[0]
        st['lanes'] += NL; st['lanes_right'] += right; st['flags_right'] += flags; st['decisions_right'] += decs
        st['tests_right'] += br; st['pieces_right'] += cs.ok; st['group_ops_right'] += group_right(cs); st['last_group_cases'] += cs.last
        st['stage_b_batches'] += outs[0]['decA']; st['stage_c_batches'] += outs[0]['ranC']
        bo = {k: cs.m.ops[k] for k in LEDGER}
        if counts is None: counts = bo
        same = same and bo == counts and cs.m.ops['U'] == BLOCK_OPS
        other.add((cs.outer_ops, cs.member_ops, cs.tw_ops, cs.tm.ops['E']))
        for mm in (cs.m, cs.tm):
            for k, v in mm.maxbnd.items(): maxbnd[k] = max(maxbnd.get(k, 0), v)
        regs = max(regs, liveness(cs.m.prog, cs.m.resident)); resident = len(cs.m.resident)
        cs.tm.prog.append(('W', None, ['X2w'])); tregs = max(tregs, liveness(cs.tm.prog, cs.tm.resident))
    st['pattern_tests'] = pt = pattern_tests(rng)
    st['budget_test'] = budget_test(); st['dslot_test'] = dslot_test(); st['lemma_a3_bad'] = lemma_a3(rng)
    mem = [member(i) for i in range(NMEM)]
    s8 = len(set(mem)) == NMEM and all(in_S8(y) for y in mem)
    oo = sorted(other)
    st.update(counts=counts, same_counts=same, counts_equal_ledger=counts == LEDGER, outer_member_tableword_tableentry_ops=oo,
              static_bound_over_2_32={k: round(v / 2 ** 32, 3) for k, v in maxbnd.items()}, peak_registers=regs,
              batch_resident=resident, table_peak_registers=tregs, s8_members=NMEM, s8_ok=int(s8), lemma_b=lemma_b())
    print(json.dumps(st, separators=(',', ':')))
    ok = (st['verifier_used'] == 1 and st['lanes_right'] == st['lanes'] and st['flags_right'] == st['lanes']
          and all(st[k] == N for k in ('decisions_right', 'tests_right', 'pieces_right', 'group_ops_right'))
          and same and counts == LEDGER and oo == [(OUTER_OPS, MEMBER_OPS, TABLE_WORD_OPS, TABLE_ENTRY_OPS)]
          and max(maxbnd.values()) < 1 << LW and regs <= 64 and tregs <= 64 and s8 and st['lemma_b'] == 6
          and st['lemma_a3_bad'] == 0 and pt['ztest_right'] == pt['ztest_patterns'] == 768
          and pt['stage_a_right'] == pt['stage_a_patterns'] == 256 and pt['stage_b_right'] == pt['stage_b_patterns'] == 16384
          and st['budget_test'] == 1 and st['dslot_test'] == 1)
    return 0 if ok else 1

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == '--count' and sys.argv[2:] in ([], ['all']): raise SystemExit(model_count(sys.argv[2:] == ['all']))
        if sys.argv[1:] == ['--ledger']: raise SystemExit(ledger())
        if sys.argv[1] != '--selftest' or len(sys.argv) not in (3, 4):
            raise SystemExit('usage: s8stage.py --selftest N [seed] | --count [all] | --ledger   (no arguments: organizer request on stdin)')
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
