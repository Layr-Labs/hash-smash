#!/usr/bin/env python3
"""Staged two-level S8 search for 2-round BLAKE3 (blake3-r2-prefix-v1): trial generator, counted 64-register
pieces (outer step with its fresh random word, table build, middle step, the three stages of a batch, block test),
exact stage rates, ledger and organizer experiments.  Implements proof.md.

Credits: length cancellation, the six constants, the class of Y4, rule A and Lemma N: c66f230d (Jbenisek, co-author
tekkac).  The three-level construction (steps O, M, Y, T), its table reused for 2^32 values of X2, and the staged
batch under budgets that halt the run: 60f94c5c (Jbenisek).  Member values once per outer step: df8bd46d (Th0rgal).
Lanes and masked rotation: ticket 2bf40fb (tekkac).  Complement propagation: 8c81a219 (Th0rgal).  winglock (18a7fc52,
d26a3c5f, 2bb5d604, 098e66f4): S8, the beta filter (Lemma B, here the stage-B test), Lemmas D and D', the block
accumulator, the exact S8 count, a fresh random word per outer step, exact stage rates, budgets and their bound.
Stage-B premise 0.60 p_B: 52bb50ee (Subflatus3); budget 0.6001 p_B: 5266c5ce (leech1996).
Fixed-X14 construction and preregistered sample: 21252124 (winglock).  This derivative changes only the
stage-B run-average premise to 0.585 p_B and hard budget to 0.5851 p_B, after reading that sample.

Stage A (every batch, 28 operations): C2 to z and rule A in seven lanes (Lemma A').  Stage B (73, if some lane
passes): C2, D0, C1, E1 to c1, rule A and the filter per lane (Lemma F).  Stage C (112, if some lane passes both):
the full 128-bit residual of all lanes (Lemmas D, D') ANDed into the block accumulator, tested once per X2 value.
Stages B and C count down a budget each and halt the run when it is spent.

Organizer mode: one JSON request on stdin, one JSON document on stdout; standard library only; SHAKE-256 only
expands seeds; no BLAKE3 import (pairs are built with G alone; `trace` is the program's own 2-round compression,
used only to check the packed pieces).  Experiments: half-collision (one trial per seed: stage ops, flags,
decisions, residual words, block test, pieces) and class-filter (nine batches of one context in the staged flow;
also counts rule-A, filter and both lanes and stage-B and stage-C batches).
  python3 s8stage.py --selftest N [seed]   (from the repository root; also checks digests with verifier/blake3.py)
  python3 s8stage.py --count [all]         (exact S8 count 185,350,144, about 2.5 minutes, and exact stage rates)
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
MF, VF = 0x00098188, 0x00008000   # beta filter on c1 of E1 (part of the event good of H1; not a branch)
# S8: e1 bits 2,3 = 1 and bit 21 == bit 26.  Member order: i bit0 -> e1 bit 14, bit1 -> 30, bit2 -> 31, rest increasing.
FREE16 = [4, 5, 6, 7, 10, 11, 12, 13, 14, 20, 21, 27, 28, 29, 30, 31]
ORDER = [14, 30, 31] + [b for b in FREE16 if b not in (14, 30, 31)]
NMEM = 1 << 16
NBATCH = (NMEM + NL - 1) // NL     # 9363

def member(i):
    e1 = CLASS_VAL | 0xc
    for t, b in enumerate(ORDER):
        if (i >> t) & 1: e1 |= 1 << b
    if (e1 >> 21) & 1: e1 |= 1 << 26
    return (e1 - Y3) & M32

def in_S8(y):
    e1 = (Y3 + y) & M32
    return (e1 & CLASS_MASK) == CLASS_VAL and (e1 & 0xc) == 0xc and ((e1 >> 21) & 1) == ((e1 >> 26) & 1)

def bc(v):  # broadcast a 32-bit value into 7 lanes
    return sum((v & LANEMASK) << (LW * l) for l in range(NL))

def lanes(x): return [(x >> (LW * l)) & LANEMASK for l in range(NL)]

def pack(vals): return sum((v & LANEMASK) << (LW * l) for l, v in enumerate(vals))

# ---------------- the construction of 60f94c5c (Jbenisek), proof.md Section 2: steps O, M, Y, T ----------------
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

def context(seven): return middle(outer(seven[:6]), seven[6])

def member_vals(o, y):
    """Step Y: the lines that read the member and the outer step, not X2 (one row of the table)."""
    Y8 = rol(y, 7) ^ o['C0.b1']; Y12 = (Y8 - o['C0.c1']) & M32; Y0 = rol(Y12, 8) ^ o['C0.d1']
    ca = (Y0 - o['C0.b1'] - o['w6']) & M32; X12 = rol(o['C0.d1'], 16) ^ ca
    dc = (X11 - X12) & M32; db = ror(o['S6'] ^ dc, 12); X6 = ror(db ^ X11, 7); dd = (dc - o['S11']) & M32
    X1 = rol(X12, 8) ^ dd
    return {'Y12': Y12, 'C0.a1': ca, 'X12': X12, 'D1.b1': db, 'X6': X6, 'D1.d1': dd, 'X1': X1}

def table_row(o, y):
    """the five words of the table for one member (proof.md Section 4)"""
    r = member_vals(o, y)
    return {'XA': (r['C0.a1'] - o['X4']) & M32, 'X6': r['X6'], 'X1': r['X1'], 'R': rol(r['D1.d1'], 16), 'Y12': r['Y12']}

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
    tr['Z'] = v[:]
    tr['digest'] = tuple(v[i] ^ v[i + 8] for i in range(8))
    return tr

def ruleA_h1(h1):
    return (h1 & 1) == 0 and (h1 >> 16) & 1 == 0 and (h1 >> 17) & 1 == 0 and (h1 >> 1) & 1 == 1 and ((h1 >> 2) & 1) != ((h1 >> 3) & 1)

# ---------------- the counting machine ----------------
MEMONLY = ()                           # packed constants kept in memory and loaded once per batch

class Machine:
    def __init__(self, resident):
        self.memory = {k: resident[k] for k in MEMONLY if k in resident}
        resident = {k: v for k, v in resident.items() if k not in MEMONLY}
        self.reg = dict(resident)          # resident constants (name -> packed value)
        self.resident = set(resident)
        self.ops = {}; self.part = None; self.maxlane = {}
        self.prog = []                     # (part, dst, srcs) trace for liveness
        # static per-lane upper bounds (exclusive), valid for ALL inputs: constants by value, list words < 2^32
        self.bnd = {k: (max(lanes(v)) + 1 if k in GLOBAL_NAMES else 1 << 32) for k, v in resident.items()}
        self.maxbnd = {}
    def _c(self, n=1):
        self.ops[self.part] = self.ops.get(self.part, 0) + n
    def _chk(self, v):
        m = max(lanes(v)); self.maxlane[self.part] = max(self.maxlane.get(self.part, 0), m)
        assert v >> (LW * NL) == 0, 'overflow beyond 7 lanes'
    def op(self, kind, dst, a, b=None, imm=None):
        for s in (a, b):                   # a constant kept in memory is loaded at its first use in the batch
            if s in self.memory and s not in self.reg: self.load(s, self.memory[s], 'ptr')
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
            B = 1 << 32
            # an operand below 2^32 changes only the low 32 bits: the guard part of the other is kept
            nb = -(-max(ba, bb) // B) * B if min(ba, bb) <= B else 1 << (max(ba, bb) - 1).bit_length()
        elif kind == 'and': nb = min(ba, bb)
        elif kind == 'shl': nb = ((ba - 1) << imm) + 1 if ((ba - 1) << imm) < (1 << LW) else (1 << LW) + 1   # > 2^36 marks 'polluted'
        elif kind == 'shr': nb = (1 << LW) + 1 if imm else ba   # next lane's bits enter the top: polluted until masked
        if kind == 'and' and (a in self.resident or b in self.resident):
            nb = min(nb, self.bnd[b if b in self.resident else a])
        if kind in ('add', 'xor', 'or'):
            assert ba <= (1 << LW) and bb <= (1 << LW), 'polluted operand %s %s' % (a, b)
        self.bnd[dst] = nb
        if kind == 'add': self.maxbnd[self.part] = max(self.maxbnd.get(self.part, 0), nb)
        assert nb <= (1 << LW) or kind in ('shl', 'shr'), 'bound exceeds lane'
        if kind == 'add': self._chk(v)
        return v
    def load(self, dst, val, addr_reg):
        self._c(); self.reg[dst] = val; self.prog.append((self.part, dst, [addr_reg]))
        self.bnd[dst] = (max(lanes(val)) + 1) if dst in GLOBAL_NAMES else 1 << 32
    def cmp_branch(self, a, b):  # compare a with b, branch: 2 ops; returns a != b
        self._c(2); self.prog.append((self.part, None, [a, b])); return self.reg[a] != self.reg[b]
    def cmp_branch_zero(self, a):  # compare a with 0 (immediate), branch: 2 ops; returns a != 0
        self._c(2); self.prog.append((self.part, None, [a])); return self.reg[a] != 0
    def ror(self, dst, a, r):    # packed per-lane ROR by r: 5 ops, masks A_r, B_r resident
        self.op('shr', '_t1', a, imm=r); self.op('and', '_t1', '_t1', 'MA%d' % r)
        self.op('shl', '_t2', a, imm=32 - r); self.op('and', '_t2', '_t2', 'MB%d' % r)
        self.op('or', dst, '_t1', '_t2')


def _store(self, name):              # write a register to memory (the table): 1 operation
    self._c(); self.prog.append((self.part, None, [name])); return self.reg[name]
Machine.store = _store

def masks(rs=(16, 12, 8, 7, 1)):
    d = {}
    for r in rs:
        d['MA%d' % r] = bc((1 << (32 - r)) - 1)
        d['MB%d' % r] = bc(((1 << r) - 1) << (32 - r))
    return d

GLOBAL_NAMES = set()
def global_consts():
    g = masks()
    g.update(dict(M=bc(M32), R15=bc(rol(X15, 8)), nX15=bc((-X15) & M32), Y11=bc(Y11), Y11p=bc(Y11p),
                  ETA=bc(ETA), Y3=bc(Y3), DY3=bc(DY3)))
    GLOBAL_NAMES.update(g)
    return g

def outer_consts(o):
    """the six per-outer-step constants that the batch keeps in registers (X14 = 0: no register)"""
    return dict(k4=bc((o['S10'] + X15) & M32), X13=bc(o['X13']), X9=bc(o['X9']), S15=bc(o['S15']),
                w5=bc(o['w5']), w5d=bc((o['w5'] + DELTA) & M32))

def mid_consts(v):
    """the nine per-X2 constants that the batch keeps in registers"""
    return dict(nw2=bc((-v['w2']) & M32), k7=bc((v['X2'] + v['w7']) & M32), w0=bc(v['w0']), S5=bc(v['S5']), w3=bc(v['w3']),
                S12=bc(v['S12']), kA=bc((-v['S1'] - v['S6']) & M32), kw12=bc(v['w12']), kw8=bc((-v['S0'] - v['S5']) & M32))

# ---------------- the outer step (scalar, every primitive counted) ----------------
class Scalar:
    """Scalar 32-bit work on the 256-bit machine, every primitive counted (outer step)."""
    def __init__(self): self.n = 0
    def add(self, a, b): self.n += 2; return (a + b) & M32          # add + mask
    def sub(self, a, b): self.n += 2; return (a - b) & M32          # subtract + mask
    def xor(self, a, b): self.n += 1; return a ^ b
    def ror(self, x, r): self.n += 4; return ror(x, r)              # shr, shl, or, and
    def rol(self, x, r): self.n += 4; return rol(x, r)
    def bc(self, v): self.n += 8; return bc(v)                      # broadcast to 7 lanes (7) and store (1)

def outer_step(six):
    """Step O in scalar form, every primitive counted, and the packed words that the build, the middle step and
    the batch read (each broadcast and stored once), the next-w5 loop step and the loads of the six per-outer
    batch registers.  D3.d1 = X3 (an instruction constant), so X14 = 0 and X9 = D3.c1.  Returns (memory, count)."""
    S = Scalar(); c0c, c0d, d3d, s15, s9, w5 = six
    assert d3d == X3
    s2 = S.add(K2A + K2B & M32, w5); s14 = S.ror(S.xor(K2D, s2), 8); s10 = S.add(K2C, s14); s6 = S.ror(S.xor(K2B, s10), 7)
    d3a = S.xor(rol(X3, 16), s14); d3c = S.add(s9, X3); d3b = S.sub(X3, d3a); s4 = S.xor(S.rol(d3b, 12), d3c)
    s3 = S.sub(d3a, s4); x9 = d3c; x4 = S.ror(S.xor(d3b, x9), 7)
    k3d = S.xor(S.rol(s15, 8), s3); k3c = S.add(IV[3], k3d); k3b = S.ror(S.xor(IV[7], k3c), 12); s11 = S.add(k3c, s15)
    s7 = S.ror(S.xor(k3b, s11), 7); k3a = S.xor(S.rol(k3d, 16), 11); w6 = S.sub(k3a, IV[3] + IV[7] & M32); w7 = S.sub(S.sub(s3, k3a), k3b)
    x8 = S.sub(c0c, c0d); cb = S.ror(S.xor(x4, c0c), 12); d2b = S.xor(rol(X7, 7), x8); d2c = S.xor(S.rol(d2b, 12), s7)
    x13 = S.sub(x8, d2c)
    mem = dict(  # table build
               Cb=S.bc(cb), nCc=S.bc(S.sub(0, c0c)), Cd=S.bc(c0d), kCa=S.bc(S.sub(S.sub(0, cb), w6)), nX4=S.bc(S.sub(0, x4)),
               RCd=S.bc(S.rol(c0d, 16)), S6=S.bc(s6), nS11=S.bc(S.sub(0, s11)),
               # middle step
               nD2bW=S.bc(S.sub(S.sub(0, d2b), W13)), RX13=S.bc(S.rol(x13, 8)), nS2S7=S.bc(S.sub(S.sub(0, s2), s7)),
               S9p1=S.bc(S.add(s9, 1)), S9=S.bc(s9), omS6=S.bc(S.sub(1, s6)), D2cp1=S.bc(S.add(d2c, 1)), RS4=S.bc(S.rol(s4, 7)),
               w7=S.bc(w7),
               # batch (loaded into registers once per outer step)
               k4=S.bc(S.add(s10, X15)), X13=S.bc(x13), X9=S.bc(x9), S15=S.bc(s15), w5=S.bc(w5),
               w5d=S.bc(S.add(w5, DELTA)))
    S.n += 4 + 2                       # next w5 (add, mask, compare, branch); its store and the store of w5 + delta
    S.n += 6                           # loads of the six batch constants into their registers
    return mem, S.n

OUTER_RAND_OPS = 6
def outer_step_rand(r, c0d, w5):
    """Outer step of the run: draw a fresh 256-bit word r (1), take C0.c1, S15, S9 from its words 0-2 (5); D3.d1 = X3;
    then step O.  Returns (memory, operation count, six words)."""
    six = [r & M32, c0d, X3, (r >> 32) & M32, (r >> 64) & M32, w5]
    mem, n = outer_step(six)
    return mem, n + OUTER_RAND_OPS, six

def rand_word(seven, extra):
    """the 256-bit word whose words 0..2 are the coin words C0.c1, S15, S9 of a context; extra fills 3..7"""
    return seven[0] | seven[3] << 32 | seven[4] << 64 | (extra & ((1 << 160) - 1)) << 96

def alg(w):
    """the algorithm's context: D3.d1 (word 2) = X3"""
    w = list(w); w[2] = X3; return w

BUILD_CONSTS = ('Cb', 'nCc', 'Cd', 'kCa', 'nX4', 'RCd', 'S6', 'nS11')
def build_machine(mem):
    """registers for the table build of one outer step: masks, M, X11, X11 + 1 and the eight build words
    (loaded once per outer step: charged as 'build entry')"""
    g = masks((24, 16, 12, 7)); g.update(M=bc(M32), X11=bc(X11), X11p1=bc((X11 + 1) & M32))
    GLOBAL_NAMES.update(g)
    g.update({k: mem[k] for k in BUILD_CONSTS})
    return Machine(dict(g, ptr=0))
BUILD_ENTRY = len(BUILD_CONSTS) + 14 + 3 + 1     # loads of the build words, masks, M, X11, X11 + 1; pointer reset

def table_build(m, U):
    """One list word of the table of an outer step: from U = ROL(y,7) in each lane, the five words
    XA = C0.a1 - X4, X6, X1, R = ROL(D1.d1,16) and Y12 of step Y, each reduced below 2^32 and stored."""
    m.part = 'T'
    m.load('U', U, 'ptr')
    m.op('xor', 'Y8', 'U', 'Cb')                                   # Y8 = ROL(y,7) ^ C0.b1
    m.op('add', 'Y12', 'Y8', 'nCc'); m.op('and', 'Y12', 'Y12', 'M'); m.store('Y12')   # Y12 = Y8 - C0.c1
    m.ror('Y0', 'Y12', 24); m.op('xor', 'Y0', 'Y0', 'Cd')          # Y0 = ROL(Y12,8) ^ C0.d1
    m.op('add', 'ca', 'Y0', 'kCa')                                 # C0.a1 = Y0 - C0.b1 - w6
    m.op('add', 'XA', 'ca', 'nX4'); m.op('and', 'XA', 'XA', 'M'); m.store('XA')       # XA = C0.a1 - X4
    m.op('xor', 'X12', 'ca', 'RCd')                                # X12 = ROL(C0.d1,16) ^ C0.a1
    m.op('xor', 'nX12', 'X12', 'M'); m.op('add', 'dc', 'nX12', 'X11p1')   # D1.c1 = X11 - X12
    m.op('xor', 'db', 'dc', 'S6'); m.ror('db', 'db', 12)           # D1.b1 = ROR(S6 ^ D1.c1, 12)
    m.op('xor', 'X6', 'db', 'X11'); m.ror('X6', 'X6', 7); m.store('X6')    # X6 = ROR(D1.b1 ^ X11, 7)
    m.op('add', 'dd', 'dc', 'nS11')                                # D1.d1 = D1.c1 - S11
    m.ror('X1', 'X12', 24); m.op('xor', 'X1', 'X1', 'dd'); m.op('and', 'X1', 'X1', 'M'); m.store('X1')   # X1 = ROL(X12,8) ^ D1.d1
    m.ror('R', 'dd', 16); m.store('R')                             # R = ROL(D1.d1,16)
    m._c(3)                                                        # next list position, compare, branch
    return {k: m.reg[k] for k in ('XA', 'X6', 'X1', 'R', 'Y12')}

# ---------------- the middle step (packed, every primitive and load counted) ----------------
MID_LOADS = ('nD2bW', 'RX13', 'nS2S7', 'S9p1', 'S9', 'omS6', 'D2cp1', 'RS4', 'w7')
def mid_globals():
    g = masks((24, 20)); g.update(ONE=bc(1), END=bc(0), ALL=W256, nIV1=bc((-IV[1]) & M32), IV15p1=bc((IV[1] + IV[5] + 1) & M32),
                                  IV5=bc(IV[5]), IV4=bc(IV[4]), nIV0=bc((-IV[0]) & M32), nIV04=bc((-IV[0] - IV[4]) & M32))
    GLOBAL_NAMES.update(g)
    return g

def middle_step(m, mem, X2prev):
    """Per X2 value: next X2 and end test, step M in seven lanes, the nine per-X2 batch registers (reduced),
    accumulator set to all ones, pointer reset; memory words are loaded (1 each)."""
    m.part = 'M'; gl = mid_globals(); loaded = set()
    def ld(n):
        if n not in loaded:
            loaded.add(n); m.load(n, mem[n] if n in mem else gl[n], 'ptr')
        return n
    m.reg['X2'] = X2prev; m.bnd['X2'] = 1 << 32
    m.op('add', 'X2', 'X2', ld('ONE')); m.op('and', 'X2', 'X2', 'M'); m.cmp_branch('X2', ld('END'))   # next X2, end test
    m.op('add', 'k7', 'X2', ld('w7')); m.op('and', 'k7', 'k7', 'M')                    # X2 + w7
    m.op('add', 'd2a', 'X2', ld('nD2bW'))                                              # D2.a1 = X2 - D2.b1 - W13
    m.op('xor', 'd2d', 'X2', ld('RX13'))                                               # D2.d1 = ROL(X13,8) ^ X2
    m.ror('S13', 'd2d', 16); m.op('xor', 'S13', 'S13', 'd2a')                          # S13 = ROL(D2.d1,16) ^ D2.a1
    m.op('add', 'kw12', 'd2a', ld('nS2S7')); m.op('and', 'kw12', 'kw12', 'M')          # w12 = D2.a1 - S2 - S7
    m.op('xor', 'k1c', 'S13', 'M'); m.op('add', 'k1c', 'k1c', ld('S9p1'))              # K1.c1 = S9 - S13
    m.op('add', 'k1d', 'k1c', ld('nIV1'))                                              # K1.d1 = K1.c1 - IV1
    ld('MA24'); ld('MB24'); m.ror('S1', 'S13', 24); m.op('xor', 'S1', 'S1', 'k1d')                             # S1 = ROL(S13,8) ^ K1.d1
    m.op('xor', 'kA', 'S1', 'M'); m.op('add', 'kA', 'kA', ld('omS6')); m.op('and', 'kA', 'kA', 'M')   # -S1 - S6
    m.ror('k1a', 'k1d', 16)                                                            # K1.a1 = ROL(K1.d1,16)
    m.op('xor', 'nw2', 'k1a', 'M'); m.op('add', 'nw2', 'nw2', ld('IV15p1')); m.op('and', 'nw2', 'nw2', 'M')   # -w2
    m.op('xor', 'k1b', 'k1c', ld('IV5')); m.ror('k1b', 'k1b', 12)                     # K1.b1 = ROR(IV5 ^ K1.c1, 12)
    m.op('add', 'w3', 'k1a', 'k1b'); m.op('xor', 'w3', 'w3', 'M'); m.op('add', 'w3', 'w3', 'S1')
    m.op('add', 'w3', 'w3', 'ONE'); m.op('and', 'w3', 'w3', 'M')                       # w3 = S1 - K1.a1 - K1.b1
    m.op('xor', 'S5', 'k1b', ld('S9')); m.ror('S5', 'S5', 7)                           # S5 = ROR(K1.b1 ^ S9, 7)
    m.op('xor', 's8', 'd2d', 'M'); m.op('add', 's8', 's8', ld('D2cp1'))                # S8 = D2.c1 - D2.d1
    m.op('xor', 'k0b', 's8', ld('RS4'))                                                # K0.b1 = ROL(S4,7) ^ S8
    ld('MA20'); ld('MB20'); m.ror('k0c', 'k0b', 20); m.op('xor', 'k0c', 'k0c', ld('IV4'))                      # K0.c1 = ROL(K0.b1,12) ^ IV4
    m.op('xor', 'S12', 'k0c', 'M'); m.op('add', 'S12', 'S12', 'ONE'); m.op('add', 'S12', 'S12', 's8')
    m.op('and', 'S12', 'S12', 'M')                                                     # S12 = S8 - K0.c1
    m.op('add', 'k0d', 'k0c', ld('nIV0'))                                              # K0.d1 = K0.c1 - IV0
    m.ror('k0a', 'k0d', 16)                                                            # K0.a1 = ROL(K0.d1,16)
    m.op('add', 'w0', 'k0a', ld('nIV04')); m.op('and', 'w0', 'w0', 'M')                # w0 = K0.a1 - IV0 - IV4
    m.ror('S0', 'S12', 24); m.op('xor', 'S0', 'S0', 'k0d')                             # S0 = ROL(S12,8) ^ K0.d1
    m.op('add', 'kw8', 'S0', 'S5'); m.op('xor', 'kw8', 'kw8', 'M'); m.op('add', 'kw8', 'kw8', 'ONE')
    m.op('and', 'kw8', 'kw8', 'M')                                                     # -S0 - S5
    m.load('acc', W256, 'ptr'); m.reg['acc'] = W256                                    # block accumulator = all ones
    m._c(1); m.reg['ptr'] = 0                                                          # list pointer reset
    return {k: m.reg[k] for k in ('nw2', 'k7', 'w0', 'S5', 'w3', 'S12', 'kA', 'kw12', 'kw8')}, m.reg['X2']

def mid_machine(o):
    """the registers at a middle step: global constants of the batch, the per-outer batch constants, the X2 loop
    register; temporaries of the step use the remaining registers"""
    return Machine(dict(global_consts(), **stage_consts(), **outer_consts(o), ptr=0, acc=W256))

# ---------------- the counted batch: three stages ----------------
# Stage tests (Lemma A' and Lemma F of proof.md).  zr = z + 2^26 leaves bits 8, 9, 24, 25 of each lane and puts
# z26 XOR z27 in bit 27; rule A holds iff (zr XOR KA) AND ALLA == 0.  The filter holds iff (c1 XOR VF) AND MF == 0.
# A per-lane flag word has bit 32 = 1 iff the lane FAILS; a stage is entered iff some lane's bit 32 is 0.
C26, KA, ALLA = 1 << 26, 0x0A000300, 0x0B000300
STAGE_NAMES = ('C26', 'KA', 'ALLA', 'B32', 'VFw', 'MFw', 'cB', 'cC')

def stage_consts(budget_b=1 << 200, budget_c=1 << 200):
    """the constants of the two stage tests (kept in registers) and the two count-down budget registers"""
    g = dict(C26=bc(C26), KA=bc(KA), ALLA=bc(ALLA), B32=bc(1 << 32), VFw=bc(VF), MFw=bc(MF))
    GLOBAL_NAMES.update(g)
    g.update(cB=budget_b, cC=budget_c)
    return g

def count_down(m, name):
    """budget register minus 1, compare with 0, branch to halt when it reaches 0: 3 operations"""
    m._c(3); m.prog.append((m.part, name, [name])); m.reg[name] -= 1
    return m.reg[name] > 0

def stage_a_test(m):
    """rule A in all seven lanes from z (Lemma A'); flag fA (bit 32 = 1 iff the lane fails); branch: 7 operations"""
    m.op('add', 'zr', 'z', 'C26')               # bit 27 of a lane = z27 XOR z26; bits 8, 9, 24, 25 unchanged
    m.op('xor', 'tA', 'zr', 'KA'); m.op('and', 'tA', 'tA', 'ALLA')
    m.op('add', 'fA', 'tA', 'M')                # bit 32 = 1 iff tA != 0, i.e. iff the lane fails rule A
    m.op('and', 'xA', 'fA', 'B32')
    return m.cmp_branch('xA', 'B32')            # True (enter stage B) iff some lane passes rule A

def stage_b_test(m):
    """rule A and the filter per lane from fA and E1's c1 (Lemma F); branch: 7 operations"""
    m.op('xor', 'wF', 'C1', 'VFw'); m.op('and', 'wF', 'wF', 'MFw')
    m.op('add', 'fF', 'wF', 'M')                # bit 32 = 1 iff the lane fails the filter
    m.op('or', 'fAF', 'fA', 'fF')               # bit 32 = 1 iff the lane fails rule A or the filter
    m.op('and', 'xF', 'fAF', 'B32')
    return m.cmp_branch('xF', 'B32')            # True (enter stage C) iff some lane passes both

def run_batch(m, row, V, force=False):
    """One batch of seven trials (seven consecutive S8 members, one context) in three stages (proof.md Section 5).
    force=True computes stages B and C whatever the decisions (for checking); accumulator and budgets then change
    only as in the staged flow.  row: the five table words; V: the list word (y per lane)."""
    out = {}
    m.part = 'A'                                # D0 to X10, C2 to z
    m.load('XA', row['XA'], 'ptr')              # table word: C0.a1 - X4
    m.op('add', 'X0', 'XA', 'nw2')              # X0 = C0.a1 - X4 - w2
    m.op('xor', 'fd', 'X0', 'R15')              # D0.d1 = ROL(X15,8) ^ X0
    m.op('add', 'X10', 'fd', 'k4')              # X10 = D0.d1 + S10 + X15
    m.load('X6', row['X6'], 'ptr')              # table word: X6
    m.op('add', 'a1', 'X6', 'k7')               # C2.a1 = X2 + X6 + w7
    m.ror('d1', 'a1', 16)                       # C2.d1 = ROR(C2.a1 ^ X14, 16), X14 = 0
    m.op('add', 'c1', 'X10', 'd1')
    m.op('xor', 'b1', 'X6', 'c1'); m.ror('b1', 'b1', 12)
    m.op('add', 'z', 'a1', 'b1'); m.op('add', 'z', 'z', 'w0')     # Y2 = C2.a2
    m.op('xor', 'z', 'z', 'd1')                 # z = Y2 ^ C2.d1
    out['decA'] = decA = stage_a_test(m)
    out['fA'] = m.reg['fA']
    if not (decA or force): return out
    m.part = 'B'                                # rest of C2, rest of D0, C1, first half of E1, the second test
    if decA: out['budgetB'] = count_down(m, 'cB')
    else: m._c(3); m.prog.append((m.part, 'cB', ['cB']))
    m.ror('Y14', 'z', 8)
    m.op('add', 'c2', 'c1', 'Y14')              # Y10
    m.op('xor', 'Y6', 'b1', 'c2'); m.ror('Y6', 'Y6', 7)
    m.op('add', 'fc', 'X10', 'nX15')            # D0.c1 = X10 - X15
    m.op('xor', 'X5', 'fc', 'S5'); m.ror('X5', 'X5', 12); m.op('xor', 'X5', 'X5', 'X10'); m.ror('X5', 'X5', 7)
    m.load('X1', row['X1'], 'ptr')              # table word: X1
    m.op('add', 'p1', 'X1', 'X5'); m.op('add', 'p1', 'p1', 'w3')      # C1.a1
    m.op('xor', 'p2', 'p1', 'X13'); m.ror('p2', 'p2', 16)           # C1.d1
    m.op('add', 'p3', 'p2', 'X9')                                   # C1.c1
    m.op('xor', 'p4', 'p3', 'X5'); m.ror('p4', 'p4', 12)            # C1.b1
    m.load('Rw', row['R'], 'ptr')               # table word: ROL(D1.d1,16)
    m.op('xor', 'ga', 'Rw', 'S12')              # D1.a1 = ROL(D1.d1,16) ^ S12, w10 = D1.a1 - S1 - S6
    m.op('add', 'Y1', 'p1', 'p4'); m.op('add', 'Y1', 'Y1', 'ga'); m.op('add', 'Y1', 'Y1', 'kA')   # Y1 = C1.a2
    m.op('xor', 'Y13', 'p2', 'Y1'); m.ror('Y13', 'Y13', 8)          # Y13 = C1.d2
    m.op('add', 'Y9', 'p3', 'Y13')                                  # Y9 = C1.c2
    m.op('add', 'A1', 'Y1', 'Y6'); m.op('add', 'A1', 'A1', 'kw12')  # E1 a1 = Y1 + Y6 + w12
    m.load('Y12', row['Y12'], 'ptr')            # table word: Y12
    m.op('xor', 'D1', 'A1', 'Y12'); m.ror('D1', 'D1', 16)           # E1 d1 (shared)
    m.op('add', 'C1', 'D1', 'Y11')                                  # E1 c1 (A)
    out['decB'] = decB = stage_b_test(m)       # some lane passes rule A and the filter (implies decA)
    out['fAF'] = m.reg['fAF']
    flowC = decA and decB
    if not (flowC or force): return out
    m.part = 'C'                                # budget, second half of E1 for both messages
    if flowC: out['budgetC'] = count_down(m, 'cC')
    else: m._c(3); m.prog.append((m.part, 'cC', ['cC']))
    m.op('add', 'C1p', 'D1', 'Y11p')                                # E1 c1 (B)
    m.op('xor', 'b', 'C1', 'Y6'); m.ror('b', 'b', 12)
    m.op('xor', 'bp', 'C1p', 'Y6'); m.ror('bp', 'bp', 12)
    m.op('add', 'a2', 'A1', 'b'); m.op('add', 'a2', 'a2', 'w5')
    m.op('add', 'a2p', 'A1', 'bp'); m.op('add', 'a2p', 'a2p', 'w5d')
    m.op('xor', 'd2', 'a2', 'D1'); m.ror('d2', 'd2', 8)
    m.op('xor', 'd2p', 'a2p', 'D1'); m.ror('d2p', 'd2p', 8)
    m.op('add', 'cc', 'C1', 'd2'); m.op('add', 'ccp', 'C1p', 'd2p')
    m.op('xor', 'P', 'a2', 'a2p'); m.op('xor', 'Q', 'cc', 'ccp')                                   # E1 parts of the residual
    m.op('xor', 'R6', 'b', 'bp'); m.op('xor', 'R6', 'R6', 'Q'); m.ror('R6', 'R6', 7)                # b2 ^ b2'
    m.part = 'D'                                # E3 for both messages
    m.load('Y4', V, 'ptr')                      # list word: y per lane
    m.op('add', 'e1', 'Y4', 'Y3')
    m.op('xor', 'h1', 'Y14', 'e1'); m.ror('h1', 'h1', 16)
    m.op('xor', 'h1p', 'h1', 'ETA')             # h1' = h1 ^ eta (Lemma T)
    m.op('add', 'g1', 'Y9', 'h1'); m.op('add', 'g1p', 'Y9', 'h1p')
    m.op('xor', 'f1', 'Y4', 'g1'); m.ror('f1', 'f1', 12)
    m.op('xor', 'f1p', 'Y4', 'g1p'); m.ror('f1p', 'f1p', 12)
    m.ror('fa', 'fd', 16); m.op('xor', 'fa', 'fa', 'S15')            # D0.a1 = ROL(D0.d1,16) ^ S15, w8 = D0.a1 - S0 - S5
    m.op('add', 'ew', 'e1', 'fa'); m.op('add', 'ew', 'ew', 'kw8')     # e1 + w8 (shared; e1' = e1 + DY3)
    m.op('add', 'e2', 'ew', 'f1')
    m.op('add', 'e2p', 'ew', 'f1p'); m.op('add', 'e2p', 'e2p', 'DY3')
    m.op('xor', 'h2', 'h1', 'e2'); m.ror('h2', 'h2', 8)
    m.op('xor', 'h2p', 'h1p', 'e2p'); m.ror('h2p', 'h2p', 8)
    m.op('add', 'g2', 'g1', 'h2'); m.op('add', 'g2p', 'g1p', 'h2p')
    m.part = 'R'                                # residual words, the per-lane zero indicator, the accumulator, jump back
    m.op('xor', 'R1', 'P', 'g2'); m.op('xor', 'R1', 'R1', 'g2p')    # D1 = (a2^a2') ^ (g2^g2')
    m.op('xor', 'R3', 'e2', 'e2p'); m.op('xor', 'R3', 'R3', 'Q')    # D3 = (e2^e2') ^ (c2^c2')
    m.ror('R4', 'P', 1); m.op('xor', 'R4', 'R4', 'P')               # W4 = ROL(D4,7) ^ D1 = (f1^f1') ^ P ^ ROR(P,1)
    m.op('xor', 'R4', 'R4', 'f1'); m.op('xor', 'R4', 'R4', 'f1p')
    m.op('xor', 'R6', 'R6', 'h2'); m.op('xor', 'R6', 'R6', 'h2p')   # D6 = (b2^b2') ^ (h2^h2')
    out.update(R1=m.reg['R1'], R3=m.reg['R3'], R4=m.reg['R4'], R6=m.reg['R6'])
    m.op('or', 'T', 'R1', 'R3'); m.op('or', 'T', 'T', 'R4'); m.op('or', 'T', 'T', 'R6'); m.op('and', 'T', 'T', 'M')
    m.op('add', 'u', 'T', 'M')                  # bit 32 of a lane is 1 iff its R != 0
    acc0 = m.reg['acc']
    m.op('and', 'acc', 'acc', 'u')              # block accumulator
    if not flowC: m.reg['acc'] = acc0           # forced (checking) run of a batch that the flow does not take to stage C
    m._c(1); m.prog.append((m.part, None, []))  # jump back to the batch loop
    out['T'] = m.reg['T']; out['u'] = m.reg['u']; out['ranC'] = flowC
    return out

def block_test(m):
    """After the last batch of a value of X2 (once per 65,536 trials): branch to step 4 iff some lane of some batch
    that ran stage C had R = 0."""
    m.part = 'Z'
    m.load('B32z', bc(1 << 32), 'ptr'); m.op('and', 'acc', 'acc', 'B32z')
    return m.cmp_branch('acc', 'B32z')

def liveness(prog, resident):
    """Peak number of registers in use: the resident constants plus every value (SSA version) that is
    live from the instruction that writes it to its last read; a result needs its register at the
    instruction that writes it."""
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

# ---------------- Lemma B: the beta filter contains the six heaviest betas ----------------
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

# ---------------- seeds ----------------
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
    n = eps ^ rol(beta ^ eps, 1) ^ ETA
    dA, dB = ta['digest'], tb['digest']
    X = [ta[(0, c)] for c in ('E0', 'E1', 'E2', 'E3')]
    xs = {3: X[3][4], 7: X[2][7], 11: X[1][6], 15: X[0][5]}   # X3 (a of D3), X7 (b of D2), X11 (c of D1), X15 (d of D0)
    return dict(A=A, B=B, w=w, y4a=ta[(1, 'C0')][7], y4b=tb[(1, 'C0')][7], eta=h1 ^ tb[(1, 'E3')][1], h1=h1,
                ruleA=ruleA_h1(h1), c1=E1a[2], filt=(E1a[2] & MF) == VF, beta=beta, n=n,
                nd=(dA[3] ^ dB[3]) ^ rol(dA[6] ^ dB[6], 8), half=all(dA[i] == dB[i] for i in (0, 2, 5, 7)), dA=dA, dB=dB,
                pinned=xs == {3: X3, 7: X7, 11: X11, 15: X15})

def batch_members(j): return [min(7 * j + l, NMEM - 1) for l in range(NL)]

def residual_words(f):
    """the four words the batch tests, from the two real digests: D1, D3, ROL(D4,7) ^ D1, D6 (Lemma D')"""
    D = {i: f['dA'][i] ^ f['dB'][i] for i in (1, 3, 4, 6)}
    return {'R1': D[1], 'R3': D[3], 'R4': rol(D[4], 7) ^ D[1], 'R6': D[6]}

def expected_mem(o):
    """the packed words that step O must leave (from the scalar lines of step O)"""
    return dict(Cb=bc(o['C0.b1']), nCc=bc(-o['C0.c1'] & M32), Cd=bc(o['C0.d1']), kCa=bc(-o['C0.b1'] - o['w6'] & M32),
                nX4=bc(-o['X4'] & M32), RCd=bc(rol(o['C0.d1'], 16)), S6=bc(o['S6']), nS11=bc(-o['S11'] & M32),
                nD2bW=bc(-o['D2.b1'] - W13 & M32), RX13=bc(rol(o['X13'], 8)), nS2S7=bc(-o['S2'] - o['S7'] & M32),
                S9p1=bc(o['S9'] + 1 & M32), S9=bc(o['S9']), omS6=bc(1 - o['S6'] & M32), D2cp1=bc(o['D2.c1'] + 1 & M32),
                RS4=bc(rol(o['S4'], 7)), w7=bc(o['w7']), **outer_consts(o))

class Case:
    """One context: counted outer step (from a random word holding the coin words), table words of the list words
    js, middle step, and a batch machine; pieces_right = every word they leave equals the construction."""
    def __init__(self, seven, js, extra=0):
        self.seven = seven; self.o = outer(seven[:6]); self.v = middle(self.o, seven[6])
        self.mem, self.outer_ops, six = outer_step_rand(rand_word(seven, extra), seven[1], seven[5])
        ok = six == list(seven[:6]) and self.mem == expected_mem(self.o) and self.o['X14'] == 0
        bm = build_machine(self.mem); self.rows = {}
        for j in js:
            ys = [member(i) for i in batch_members(j)]
            n0 = bm.ops.get('T', 0)
            self.rows[j] = table_build(bm, pack([rol(y, 7) for y in ys]))
            self.build_ops = bm.ops['T'] - n0
            want = [table_row(self.o, y) for y in ys]
            ok = ok and all(lanes(self.rows[j][k]) == [r[k] for r in want] for k in ('XA', 'X6', 'X1', 'R', 'Y12'))
        self.build_regs = liveness(bm.prog, bm.resident)
        mm = mid_machine(self.o)
        mc, x2 = middle_step(mm, self.mem, bc((seven[6] - 1) & M32))
        mm.prog.append(('M', None, ['nw2', 'k7', 'w0', 'S5', 'w3', 'S12', 'kA', 'kw12', 'kw8', 'X2', 'acc']))   # live into the batches
        self.mid_ops = mm.ops['M']; self.mid_regs = liveness(mm.prog, mm.resident)
        ok = ok and mc == mid_consts(self.v) and x2 == bc(seven[6])
        self.mc = mc; self.pieces_right = int(ok)
    def machine(self, budget_b=1 << 200, budget_c=1 << 200):
        return Machine(dict(global_consts(), **stage_consts(budget_b, budget_c), **outer_consts(self.o), **self.mc,
                            ptr=0, acc=W256))

def bit32(x, l): return (x >> (LW * l + 32)) & 1

def check_batch(case, j, m, verify=None):
    """Batch j on machine m with force=True; per lane: stage-A flag (bit 32) = fails rule A, stage-B flag = fails
    rule A or the filter, the four residual words and the indicator equal those of the real digests of A and B;
    both decisions equal "some lane passes"."""
    ys = [member(i) for i in batch_members(j)]
    out = run_batch(m, case.rows[j], pack(ys), force=True)
    Rw = {k: lanes(out[k]) for k in ('R1', 'R3', 'R4', 'R6')}; Tw = lanes(out['T']); Uw = lanes(out['u'])
    right = flags = 0; fs = []
    for l, y in enumerate(ys):
        f = forward(case.v, y); fs.append(f)
        R = residual_words(f)
        ok = (in_S8(y) and f['half'] and f['pinned'] and f['y4a'] == y == f['y4b'] and f['eta'] == ETA and len(f['A']) == 55
              and len(f['B']) == 63 and all((Rw[k][l] & M32) == R[k] for k in Rw) and Tw[l] == R['R1'] | R['R3'] | R['R4'] | R['R6']
              and f['nd'] == f['n'] and (Uw[l] >> 32) & 1 == int(f['dA'] != f['dB']))
        if verify is not None:
            ok = ok and struct.unpack('<8I', verify(f['A'], 2)) == f['dA'] and struct.unpack('<8I', verify(f['B'], 2)) == f['dB']
        right += ok
        flags += bit32(out['fA'], l) == int(not f['ruleA']) and bit32(out['fAF'], l) == int(not (f['ruleA'] and f['filt']))
    dec = int(out['decA'] == any(f['ruleA'] for f in fs) and out['decB'] == any(f['ruleA'] and f['filt'] for f in fs))
    return right, flags, dec, out, fs

def check_block(seven, js, verify=None, extra=0):
    """The counted pieces, the batches js on one machine in the staged flow, the block test (right iff taken
    exactly when some lane of a batch that ran stage C has equal digests)."""
    case = Case(seven, js, extra); m = case.machine(); right = flags = decs = 0; allf = []; outs = []
    for j in js:
        r, fl, dc, out, fs = check_batch(case, j, m, verify); right += r; flags += fl; decs += dc; allf.append(fs); outs.append(out)
    taken = block_test(m)
    want = any(f['dA'] == f['dB'] for out, fs in zip(outs, allf) if out['ranC'] for f in fs)
    return case, m, right, flags, decs, int(taken == want), outs, allf

LEDGER = {'A': 28, 'B': 73, 'C': 43, 'D': 48, 'R': 21}   # stage A 28; stage B 73; stage C 43 + 48 + 21 = 112
STAGE_OPS = (28, 73, 112)
BUILD_OPS, MID_OPS, OUTER_OPS = 49, 107, 318

def stage_ops(m, nb=1):
    o = m.ops
    return o['A'] // nb, o['B'] // nb, (o['C'] + o['D'] + o['R']) // nb

def ex_half(seed):
    seven, i = seed_trial(seed)
    case, m, right, flags, decs, br, outs, allf = check_block(seven, [i // NL], extra=int.from_bytes(hashlib.shake_256(seed + b'r').digest(16), 'little'))
    fs = allf[0]
    f = fs[i % NL] if batch_members(i // NL)[i % NL] == i else forward(case.v, member(i))
    sa, sb, sc = stage_ops(m)
    return f['A'], f['B'], {'stage_a_ops': sa, 'stage_b_ops': sb, 'stage_c_ops': sc, 'block_test_ops': m.ops['Z'],
                            'lanes_right': right, 'flags_right': flags, 'decisions_right': decs, 'tests_right': br,
                            'member_in_s8': int(in_S8(member(i))), 'pieces_right': case.pieces_right,
                            'outer_ops': case.outer_ops, 'build_ops': case.build_ops, 'middle_ops': case.mid_ops}

def ex_class(seed):
    seven, i = seed_trial(seed)
    j0 = min(i // NL, NBATCH - 9) // 9 * 9
    obs = dict(members=0, in_s8=0, y4_equal=0, eta_equal=0, lanes_right=0, flags_right=0, decisions_right=0, tests_right=0,
               pieces_right=0, rule_a_lanes=0, filter_lanes=0, filter_and_rule_a_lanes=0, stage_b_batches=0, stage_c_batches=0,
               lemma_b=lemma_b())
    pair = None; seen = set()
    case, m, right, flags, decs, br, outs, allf = check_block(seven, list(range(j0, j0 + 9)),
                                                              extra=int.from_bytes(hashlib.shake_256(seed + b'r').digest(16), 'little'))
    obs['lanes_right'] += right; obs['flags_right'] += flags; obs['decisions_right'] += decs; obs['tests_right'] += br
    obs['pieces_right'] = case.pieces_right
    obs['stage_b_batches'] = sum(o['decA'] for o in outs); obs['stage_c_batches'] = sum(o['ranC'] for o in outs)
    for j, fs in zip(range(j0, j0 + 9), allf):
        for idx, f in zip(batch_members(j), fs):
            if idx in seen: continue
            seen.add(idx); y = member(idx)
            obs['members'] += 1; obs['in_s8'] += in_S8(y); obs['y4_equal'] += f['y4a'] == y == f['y4b']
            obs['eta_equal'] += f['eta'] == ETA; obs['rule_a_lanes'] += f['ruleA']; obs['filter_lanes'] += f['filt']
            obs['filter_and_rule_a_lanes'] += f['ruleA'] and f['filt']
            if idx == i: pair = (f['A'], f['B'])
    if pair is None:
        f = forward(case.v, member(i)); pair = (f['A'], f['B'])
    return pair[0], pair[1], {k: int(v) for k, v in obs.items()}

def pattern_tests(rng):
    """Checks on constructed packed words: (1) zero indicator and block test, blocks of 1-3 batches, all 128 lane
    patterns, twice; (2) the stage-A test, all 128 patterns of rule-A lanes, twice; (3) the stage-B test, all 16,384
    pairs of rule-A and filter patterns."""
    res = dict(ztest_patterns=0, ztest_right=0, stage_a_patterns=0, stage_a_right=0, stage_b_patterns=0, stage_b_right=0)
    def word(zero_mask):
        return sum(((0 if (zero_mask >> l) & 1 else (rng.getrandbits(32) if rng.getrandbits(1) else 1 << rng.randrange(32)) or 1)
                    | rng.getrandbits(4) << 32) << (LW * l) for l in range(NL))
    for k in (1, 2, 3):
        for P in range(128):
            for rep in range(2):
                m = Machine(dict(global_consts(), ptr=0, acc=W256)); m.part = 'R'; want = False
                for b in range(k):
                    zm = P if b == k - 1 else (rng.getrandbits(NL) if rep else 0)
                    want = want or zm != 0
                    m.reg['T'] = word(zm); m.bnd['T'] = 1 << LW
                    m.op('and', 'T', 'T', 'M'); m.op('add', 'u', 'T', 'M'); m.op('and', 'acc', 'acc', 'u')
                taken = block_test(m)
                res['ztest_patterns'] += 1; res['ztest_right'] += (taken == want)
    CONDS = [(8, 1), (9, 1), (24, 0), (25, 1)]
    def z_lane(ok):
        while True:
            z = rng.getrandbits(32)
            for b, v in CONDS: z = (z & ~(1 << b)) | v << b
            z = (z & ~(1 << 27)) | (1 - ((z >> 26) & 1)) << 27
            if not ok:
                for c in range(5):
                    if c == 0 or rng.getrandbits(1):
                        b = (8, 9, 24, 25, 27)[rng.randrange(5)]; z ^= 1 << b
            h1 = ror(z, 24) ^ ror((CLASS_VAL | 0xc) & M32, 16)   # h1 for an e1 with the class bits (Lemma A (a))
            if ruleA_h1(h1) == ok: return z | rng.getrandbits(2) << 32
    for rep in range(2):
        for P in range(128):
            m = Machine(dict(global_consts(), **stage_consts(), ptr=0, acc=W256)); m.part = 'A'
            m.reg['z'] = pack([z_lane((P >> l) & 1) for l in range(NL)]); m.bnd['z'] = 1 << 34
            dec = stage_a_test(m)
            ok = dec == (P != 0) and all(bit32(m.reg['fA'], l) == 1 - ((P >> l) & 1) for l in range(NL))
            res['stage_a_patterns'] += 1; res['stage_a_right'] += ok
    for PA in range(128):
        for PF in range(128):
            m = Machine(dict(global_consts(), **stage_consts(), ptr=0, acc=W256)); m.part = 'B'
            fA = pack([rng.getrandbits(32) | (1 - ((PA >> l) & 1)) << 32 for l in range(NL)])
            def c1_lane(ok):
                while True:
                    c = rng.getrandbits(33)
                    if (((c & M32) & MF) == VF) == ok: return c
                    if ok: return (c & ~MF) | VF
            m.reg['fA'] = fA; m.bnd['fA'] = 1 << 33
            m.reg['C1'] = pack([c1_lane((PF >> l) & 1) for l in range(NL)]); m.bnd['C1'] = 1 << 33
            dec = stage_b_test(m)
            ok = dec == ((PA & PF) != 0) and all(bit32(m.reg['fAF'], l) == 1 - ((PA & PF) >> l & 1) for l in range(NL))
            res['stage_b_patterns'] += 1; res['stage_b_right'] += ok
    return res

# ---------------- exact model count of proof.md Section 8 (participant mode --count) ----------------
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
    """Exact stage rates under M (h1 and E1's d1 independent uniform; c1 = d1 + Y11 uniform): passing patterns on the
    bits read (0-3, 16, 17 of h1; the six filter bits of c1), enumerated, times 2^26; p_B: a batch's distinct trials
    independent under M (as in H1 (i)), 9,362 batches of 7 and one of 2: the share of batches with a rule-A trial."""
    RB = (0, 1, 2, 3, 16, 17); FB = [b for b in range(32) if MF >> b & 1]
    nA = sum(ruleA_h1(sum(((k >> i) & 1) << b for i, b in enumerate(RB))) for k in range(64)) << 26
    nF = sum((sum(((k >> i) & 1) << b for i, b in enumerate(FB)) & MF) == VF for k in range(64)) << 26
    nAF = nA * nF                                   # pairs (h1, c1) in 2^64; independent words under M
    q = 1 - Fraction(nA, 1 << 32); last = NMEM - NL * (NBATCH - 1)
    pB = ((NBATCH - 1) * (1 - q ** NL) + 1 - q ** last) / NBATCH
    return {'filter_bits': FB, 'ruleA_count': nA, 'ruleA_rate_log2': math.log2(nA / 2 ** 32), 'filter_count': nF,
            'ruleA_filter_count_2_64': nAF, 'ruleA_filter_rate_log2': math.log2(nAF / 2 ** 64),
            'p_B': [pB.numerator, pB.denominator], 'p_B_float': float(pB), 'full_batch_B': float(1 - q ** NL),
            'union_bound_per_batch_stageC': NMEM * nAF / (NBATCH * 2 ** 64),
            'exact': nA == 1 << 27 and nF == 1 << 26 and nAF == 1 << 53 and last == 2}, pB

# ---------------- the ledger of proof.md Section 9 (participant mode --ledger) ----------------
V_RANGE = 1512538                     # values of C0.d1: 0 .. V - 1
F_H1 = 92675072                       # the factor of H1 (185,350,144 / 2)
PREMISE = (Fraction(585, 1000), Fraction(125, 100))    # H1 (ii): stage-B batch share <= 0.585 p_B (this derivative); rule A and filter <= 1.25 * 2^-11
BUDGET = (Fraction(5851, 10000), Fraction(127, 100))  # E_B = 0.5851 p_B per batch (this derivative), E_C = 1.27 * 2^-11 per trial
def ledger():
    N = V_RANGE << 80; n_out = V_RANGE << 32; n_x2 = V_RANGE << 64; m_out = NBATCH << 32
    sr, pB = stage_rates(); nb = n_x2 * NBATCH
    EB = -(-(BUDGET[0] * pB * nb) // 1); EC = -(-(BUDGET[1] * N) // 2048)
    per_x2 = NBATCH * STAGE_OPS[0] + 3 * 147 + MID_OPS + 4
    per_outer = OUTER_OPS + 26 + NBATCH * BUILD_OPS
    ops = n_x2 * per_x2 + (EB + 1) * STAGE_OPS[1] + (EC + 1) * STAGE_OPS[2] + n_out * per_outer + (V_RANGE << 6) + (1 << 22) + (1 << 22)
    T = Fraction(ops, 430) + 2 + (1 << 86)
    lam = Fraction(N * F_H1, 1 << 128)
    out = {'E_B': EB, 'E_C': EC}
    for name, cnt, mean, ops_stage in (('B', EB, PREMISE[0] * pB * nb, STAGE_OPS[1]), ('C', EC, PREMISE[1] * N / 2048, STAGE_OPS[2])):
        muH = mean / m_out           # upper bound on E[sum X_k], X_k = (batches of outer step k entering) / m_out
        delta = Fraction(cnt) / m_out / muH - 1
        out[name] = {'budget_batches_log2': math.log2(cnt), 'budget_per_batch': float(Fraction(cnt) / nb),
                     'mu_H': float(muH), 'delta': float(delta), 'chernoff_exponent': float(delta * delta * muH / 3),
                     'ops_per_trial': float(Fraction((cnt + 1) * ops_stage, N))}
    per_trial = Fraction(ops, N)
    out.update(N_log2=math.log2(N), per_x2_fixed=per_x2, per_outer=per_outer, ops_per_trial=float(per_trial),
               time_log2=math.log2(T), lam=float(lam), success=1 - math.exp(-float(lam)) - 0.002,
               stage_rates=sr)
    print(json.dumps(out, indent=1))
    return 0


def selftest(N, seed):
    verify = None
    root = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), *(['..'] * 5)))
    try:
        sys.path.insert(0, root); from verifier.blake3 import blake3 as verify
    except Exception:
        verify = None
    rng = Rng('s8stage selftest %s' % seed)
    st = dict(cases=N, lanes=0, lanes_right=0, flags_right=0, decisions_right=0, tests_right=0, pieces_right=0,
              verifier_used=int(verify is not None), rule_a_lanes=0, rule_a_filter_lanes=0, stage_b_batches=0, stage_c_batches=0)
    counts = None; same = True; maxlane = {}; maxbnd = {}; regs = {'batch': 0, 'build': 0, 'middle': 0}; resident = 0
    other = set()
    for case in range(N):
        cw = [rng.getrandbits(32) for _ in range(7)]
        if case % 5 == 4: cw = [rng.choice([0, M32, v]) for v in cw]
        cw = alg(cw)
        j = NBATCH - 1 if case % 4 == 3 else rng.randrange(NBATCH)
        c, m, right, flags, decs, br, outs, allf = check_block(cw, [j], verify, extra=rng.getrandbits(128)); fs = allf[0]
        st['lanes'] += NL; st['lanes_right'] += right; st['flags_right'] += flags; st['decisions_right'] += decs
        st['tests_right'] += br; st['pieces_right'] += c.pieces_right
        st['rule_a_lanes'] += sum(f['ruleA'] for f in fs); st['rule_a_filter_lanes'] += sum(f['ruleA'] and f['filt'] for f in fs)
        st['stage_b_batches'] += outs[0]['decA']; st['stage_c_batches'] += outs[0]['ranC']
        bo = {k: v for k, v in m.ops.items() if k != 'Z'}
        if counts is None: counts = bo
        same = same and bo == counts and m.ops['Z'] == 4
        other.add((c.outer_ops, c.build_ops, c.mid_ops))
        for k, v in m.maxlane.items(): maxlane[k] = max(maxlane.get(k, 0), v)
        for k, v in m.maxbnd.items(): maxbnd[k] = max(maxbnd.get(k, 0), v)
        regs['batch'] = max(regs['batch'], liveness(m.prog, m.resident)); resident = len(m.resident)
        regs['build'] = max(regs['build'], c.build_regs); regs['middle'] = max(regs['middle'], c.mid_regs)
    st['pattern_tests'] = pattern_tests(rng)
    st['budget_test'] = budget_test()
    mem = [member(i) for i in range(NMEM)]
    s8 = len(set(mem)) == NMEM and all(in_S8(y) for y in mem)
    oo = sorted(other)
    st.update(counts=counts, stage_ops=list(STAGE_OPS) if counts == LEDGER else None, same_counts=same,
              counts_equal_ledger=counts == LEDGER, outer_build_middle_ops=oo,
              static_bound_over_2_32={k: round(v / 2 ** 32, 3) for k, v in maxbnd.items()},
              largest_lane_over_2_32={k: round(v / 2 ** 32, 3) for k, v in maxlane.items()},
              peak_registers=regs, batch_resident=resident, s8_members=NMEM, s8_ok=int(s8), lemma_b=lemma_b())
    print(json.dumps(st, separators=(',', ':')))
    pt = st['pattern_tests']
    ok = (st['verifier_used'] == 1 and st['lanes_right'] == st['lanes'] and st['flags_right'] == st['lanes']
          and st['decisions_right'] == N and st['tests_right'] == N and st['pieces_right'] == N
          and same and counts == LEDGER and oo == [(OUTER_OPS, BUILD_OPS, MID_OPS)]
          and max(maxbnd.values()) < 1 << LW and max(regs.values()) <= 64 and s8 and st['lemma_b'] == 6
          and pt['ztest_right'] == pt['ztest_patterns'] == 768 and pt['stage_a_right'] == pt['stage_a_patterns'] == 256
          and pt['stage_b_right'] == pt['stage_b_patterns'] == 16384 and st['budget_test'] == 1)
    return 0 if ok else 1

def budget_test():
    """A budget register holding k lets exactly k - 1 entries pass before the halt branch (k = 1, 2, 3; both)."""
    ok = True
    for k in (1, 2, 3):
        for which in ('cB', 'cC'):
            m = Machine(dict(global_consts(), **stage_consts(k if which == 'cB' else 1 << 200, k if which == 'cC' else 1 << 200),
                             ptr=0, acc=W256)); m.part = 'B'
            entries = 0
            while count_down(m, which): entries += 1
            ok = ok and entries == k - 1 and m.reg[which] == 0
    return int(ok)

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
