#!/usr/bin/env python3
"""S8 sub-class search for 2-round BLAKE3 (blake3-r2-prefix-v1): trial generator,
counted 64-register batch, and organizer experiments.  Implements proof.md.

Credits: the 55/63-byte construction (steps S1, T, S2, S3), the six constants, the
class of Y4 (eta = 830303cf), rule A and Lemma N are from submission c66f230d by
Jbenisek (co-author tekkac); the 7 x 36-bit lane layout and the masked rotation are
from ticket 2bf40fb (tekkac); complement propagation and the unmasked shifts follow
submission 8c81a219 (Th0rgal).  New here: the sub-class S8, the member order, the
beta filter (Lemma B), the folded single-rotation X6 identity, and the counted batch below,
which computes the full 128-bit residual of every trial (four words equivalent to the
digest differences, Lemma D') with no data-dependent branch; a per-lane indicator is
ANDed into a block accumulator and tested once per X14 block of 65,536 trials (so no
stage budgets).

Organizer mode: one JSON request on stdin, one JSON document on stdout.  Only the
standard library; no OS randomness, wall time or ambient state.  SHAKE-256 only
expands seeds.  No BLAKE3 library is imported in organizer mode; returned pairs are
built with G alone and the organizer recomputes both digests.  `trace` below is the
program's own 2-round compression (proof.md Section 1); it is used only to check the
packed batch against the trial's real messages.

  half-collision  one trial per seed (7 context words and an S8 member number from
                  the seed); digest words 0,2,5,7 agree (exact, Theorem 1).
                  Observations: operation count of the batch holding that member, of
                  the block test, its lanes whose packed residual words and indicator
                  equal the forward computation, and whether the block test is right.
  class-filter    nine consecutive batches (63 members) of one context; returns the
                  seed member's pair; observations check Lemma Q/S8, Y4, eta, the
                  packed residual words of every lane, the block test, Lemma B, and
                  count the lanes with rule A and with the beta filter.

Self-test (not an organizer mode):  python3 s8search.py --selftest N [seed]
  run from the repository root, it also compares every lane's digests with
  verifier/blake3.py blake3(m, 2) when that module can be imported.
Model count (not an organizer mode):  python3 s8search.py --count [all]
  recomputes the exact count of proof.md Section 8 for S8 and the six betas of T6:
  per outcome N1 and N3 with rule A, per-beta parts, total 185,350,144 (about 2.5 minutes);
  with 'all' also N3 without a rule on h1 (about 8 minutes).  Exit status 0 iff the
  rule-A total is 185,350,144 (and, with 'all', the total without rule is the same).
"""
import hashlib, json, os, struct, sys

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
MF, VF = 0x00098188, 0x00008000   # beta filter on c1 of E1 (part of the event good of H1; not a branch) (keeps betas 18b0e098 18b1a098 18d0e098 18d1a098 18b3e098 18d3e098)
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

def bc(v):  # broadcast a 32-bit value into 7 lanes (setup, not batch)
    return sum((v & LANEMASK) << (LW * l) for l in range(NL))

def lanes(x): return [(x >> (LW * l)) & LANEMASK for l in range(NL)]

# ---------------- step S1 (context) and step T (member), from the c66f230d proof text ----------------
def ctx_words(vc, vd, S11, S4, X13, X14, w0):
    c = {}
    ka = (IV[0] + IV[4] + w0) & M32; kd = ror(ka, 16); kc = (IV[0] + kd) & M32; kb = ror(IV[4] ^ kc, 12)
    S8 = rol(S4, 7) ^ kb; S12 = (S8 - kc) & M32; S0 = rol(S12, 8) ^ kd; w1 = (S0 - ka - kb) & M32
    X8 = (vc - vd) & M32; tc = (X8 - X13) & M32; td = (tc - S8) & M32; tb = rol(X7, 7) ^ X8
    S7 = rol(tb, 12) ^ tc; X2 = rol(X13, 8) ^ td; ta = (X2 - tb - W13) & M32; S13 = rol(td, 16) ^ ta
    mb = rol(S7, 7) ^ S11; mc = rol(mb, 12) ^ IV[7]; md = (mc - IV[3]) & M32
    S15 = (S11 - mc) & M32; S3 = rol(S15, 8) ^ md; ma = rol(md, 16) ^ 11
    w6 = (ma - IV[3] - IV[7]) & M32; w7 = (S3 - ma - mb) & M32
    p = (K + W4) & M32; q = ror(p ^ 55, 16); r = (IV[2] + q) & M32; u = ror(IV[6] ^ r, 12)
    ea = (S3 + S4) & M32; eb = (X3 - ea) & M32; ec = rol(eb, 12) ^ S4
    ed = rol(X14, 8) ^ X3; S9 = (ec - ed) & M32; S14 = rol(ed, 16) ^ ea; X9 = (ec + X14) & M32; X4 = ror(eb ^ X9, 7)
    S10 = (r + S14) & M32; S6 = ror(u ^ S10, 7); S2 = rol(S14, 8) ^ q; w5 = (S2 - p - u) & M32
    w12 = (ta - S2 - S7) & M32
    nc = (S9 - S13) & M32; nd = (nc - IV[1]) & M32; na = rol(nd, 16); nb = ror(IV[5] ^ nc, 12)
    S1 = rol(S13, 8) ^ nd; S5 = ror(nb ^ S9, 7); w2 = (na - IV[1] - IV[5]) & M32; w3 = (S1 - na - nb) & M32
    vb = ror(X4 ^ vc, 12)
    c.update(dict(vc=vc, vd=vd, S11=S11, S4=S4, X13=X13, X14=X14, w0=w0, w1=w1, w2=w2, w3=w3, w5=w5, w6=w6, w7=w7,
                  w12=w12, S0=S0, S1=S1, S5=S5, S6=S6, S10=S10, S12=S12, S15=S15, X2=X2, X4=X4, X9=X9, vb=vb))
    return c

def trial_words(c, y):
    vb, vc, vd = c['vb'], c['vc'], c['vd']
    Y8 = rol(y, 7) ^ vb; Y12 = (Y8 - vc) & M32; Y0 = rol(Y12, 8) ^ vd
    va = (Y0 - vb - c['w6']) & M32; X0 = (va - c['X4'] - c['w2']) & M32; X12 = rol(vd, 16) ^ va
    fd = rol(X15, 8) ^ X0; fc = (c['S10'] + fd) & M32; X10 = (fc + X15) & M32; fb = ror(c['S5'] ^ fc, 12); X5 = ror(fb ^ X10, 7)
    fa = rol(fd, 16) ^ c['S15']; w8 = (fa - c['S0'] - c['S5']) & M32; w9 = (X0 - fa - fb) & M32
    gc = (X11 - X12) & M32; gb = ror(c['S6'] ^ gc, 12); X6 = ror(gb ^ X11, 7); gd = (gc - c['S11']) & M32; X1 = rol(X12, 8) ^ gd
    ga = rol(gd, 16) ^ c['S12']; w10 = (ga - c['S1'] - c['S6']) & M32; w11 = (X1 - ga - gb) & M32
    w = [c['w0'], c['w1'], c['w2'], c['w3'], W4, c['w5'], c['w6'], c['w7'], w8, w9, w10, w11, c['w12'], W13, 0, 0]
    wp = list(w); wp[4] = W4p; wp[5] = (c['w5'] + DELTA) & M32
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

def masks():
    d = {}
    for r in (24, 19, 16, 12, 8, 7, 1):
        d['MA%d' % r] = bc((1 << (32 - r)) - 1)
        d['MB%d' % r] = bc(((1 << r) - 1) << (32 - r))
    return d

GLOBAL_NAMES = set()
def global_consts():
    g = masks()
    g.update(dict(M=bc(M32), R15=bc(rol(X15, 8)), k5=bc((X11 + 1) & M32), nX15=bc((-X15) & M32),
                  Y11=bc(Y11), Y11p=bc(Y11p), ETA=bc(ETA), Y3=bc(Y3), DY3=bc(DY3)))
    GLOBAL_NAMES.update(g)
    return g

def ctx_consts(c):
    w = c
    return dict(vb=bc(w['vb']), nvc=bc((-w['vc']) & M32), vd=bc(w['vd']), c1k=bc((-w['vb'] - w['w6']) & M32),
                k2=bc(rol(w['vd'], 16) ^ M32), k3=bc((-w['X4'] - w['w2']) & M32), k4=bc((w['S10'] + X15) & M32),
                S6x=bc(w['S6'] ^ rol(X11, 12)), k7=bc((w['X2'] + w['w7']) & M32), X14=bc(w['X14']), w0=bc(w['w0']), S5=bc(w['S5']),
                S11=bc(w['S11']), nS12=bc(w['S12'] ^ M32), w3=bc(w['w3']), X13=bc(w['X13']), X9=bc(w['X9']),
                kA=bc((-w['S1'] - w['S6']) & M32), kw12=bc(w['w12']), S15=bc(w['S15']), kw8=bc((-w['S0'] - w['S5']) & M32),
                w5=bc(w['w5']), w5d=bc((w['w5'] + DELTA) & M32))

def run_batch(m, U, V):
    """One batch of seven trials: every lane is computed to the four residual words D1, D3, D4, D6
    (digest words 1, 3, 4, 6 of A XOR those of B) with no data-dependent branch except the final
    test 'some lane has R = 0'.  U holds ROL(y,7) and V holds y per lane (two list words)."""
    out = {}
    m.part = 'A'                                # C0, D0/D1 pieces, X6, first half of C2
    m.load('Y8', U, 'ptr')                      # list word: ROL(y,7) per lane (offset is an instruction field)
    m.op('xor', 'Y8', 'Y8', 'vb')               # Y8
    m.op('add', 'Y12', 'Y8', 'nvc')             # Y12 = Y8 - vc
    m.ror('Y0', 'Y12', 24); m.op('xor', 'Y0', 'Y0', 'vd')   # Y0 = ROL(Y12,8) ^ vd
    m.op('add', 'va', 'Y0', 'c1k')              # va = Y0 - vb - w6
    m.op('xor', 'nX12', 'va', 'k2')             # ~X12 (low 32 bits)
    m.op('add', 'X0', 'va', 'k3')               # X0
    m.op('xor', 'fd', 'X0', 'R15')              # fd = ROL(X15,8) ^ X0
    m.op('add', 'X10', 'fd', 'k4')              # X10 = fd + S10 + X15
    m.op('add', 'gc', 'nX12', 'k5')             # gc = X11 - X12
    m.op('xor', 'X6', 'gc', 'S6x'); m.ror('X6', 'X6', 19)          # X6 = ROR(ROR(S6^gc,12) ^ X11, 7) = ROR(gc ^ S6 ^ ROL(X11,12), 19)
    m.op('add', 'a1', 'X6', 'k7')               # C2 first value
    m.op('xor', 'd1', 'a1', 'X14'); m.ror('d1', 'd1', 16)
    m.op('add', 'c1', 'X10', 'd1')
    m.op('xor', 'b1', 'X6', 'c1'); m.ror('b1', 'b1', 12)
    m.op('add', 'z', 'a1', 'b1'); m.op('add', 'z', 'z', 'w0')     # a2 = Y2
    m.op('xor', 'z', 'z', 'd1')                 # z = a2 ^ d1
    m.part = 'B'                                # rest of C2, X5, X1, C1 (Y1, Y9), first half of E1
    m.ror('Y14', 'z', 8)
    m.op('add', 'c2', 'c1', 'Y14')
    m.op('xor', 'Y6', 'b1', 'c2'); m.ror('Y6', 'Y6', 7)
    m.op('add', 'fc', 'X10', 'nX15')            # fc = X10 - X15
    m.op('xor', 'X5', 'fc', 'S5'); m.ror('X5', 'X5', 12); m.op('xor', 'X5', 'X5', 'X10'); m.ror('X5', 'X5', 7)
    m.op('xor', 'ngd', 'gc', 'M'); m.op('add', 'ngd', 'ngd', 'S11')   # ~gd = ~gc + S11
    m.ror('X1', 'nX12', 24); m.op('xor', 'X1', 'X1', 'ngd')         # X1 = ROL(~X12,8) ^ ~gd
    m.ror('ga', 'ngd', 16); m.op('xor', 'ga', 'ga', 'nS12')         # ga = ROL(gd,16) ^ S12
    m.op('add', 'p1', 'X1', 'X5'); m.op('add', 'p1', 'p1', 'w3')      # C1 first
    m.op('xor', 'p2', 'p1', 'X13'); m.ror('p2', 'p2', 16)           # C1 d1
    m.op('add', 'p3', 'p2', 'X9')                                   # C1 c1
    m.op('xor', 'p4', 'p3', 'X5'); m.ror('p4', 'p4', 12)            # C1 b1
    m.op('add', 'Y1', 'p1', 'p4'); m.op('add', 'Y1', 'Y1', 'ga'); m.op('add', 'Y1', 'Y1', 'kA')   # Y1 = a2 of C1 (w10 = ga - S1 - S6)
    m.op('xor', 'Y13', 'p2', 'Y1'); m.ror('Y13', 'Y13', 8)          # Y13 = d2 of C1
    m.op('add', 'Y9', 'p3', 'Y13')                                  # Y9 = c2 of C1
    m.op('add', 'A1', 'Y1', 'Y6'); m.op('add', 'A1', 'A1', 'kw12')  # E1 a1 = Y1 + Y6 + w12
    m.op('xor', 'D1', 'A1', 'Y12'); m.ror('D1', 'D1', 16)           # E1 d1 (shared)
    m.op('add', 'C1', 'D1', 'Y11')                                  # E1 c1 (A)
    m.part = 'C'                                # second half of E1 for both messages
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
    m.op('xor', 'h1p', 'h1', 'ETA')             # h1' = h1 ^ eta (Lemma T: eta is the same for every member)
    m.op('add', 'g1', 'Y9', 'h1'); m.op('add', 'g1p', 'Y9', 'h1p')
    m.op('xor', 'f1', 'Y4', 'g1'); m.ror('f1', 'f1', 12)
    m.op('xor', 'f1p', 'Y4', 'g1p'); m.ror('f1p', 'f1p', 12)
    m.ror('fa', 'fd', 16); m.op('xor', 'fa', 'fa', 'S15')            # fa = ROL(fd,16) ^ S15, w8 = fa - S0 - S5
    m.op('add', 'ew', 'e1', 'fa'); m.op('add', 'ew', 'ew', 'kw8')     # e1 + w8 (shared; e1' = e1 + DY3)
    m.op('add', 'e2', 'ew', 'f1')
    m.op('add', 'e2p', 'ew', 'f1p'); m.op('add', 'e2p', 'e2p', 'DY3')
    m.op('xor', 'h2', 'h1', 'e2'); m.ror('h2', 'h2', 8)
    m.op('xor', 'h2p', 'h1p', 'e2p'); m.ror('h2p', 'h2p', 8)
    m.op('add', 'g2', 'g1', 'h2'); m.op('add', 'g2p', 'g1p', 'h2p')
    m.part = 'R'                                # residual words, the per-lane zero indicator and the block accumulator
    m.op('xor', 'R1', 'P', 'g2'); m.op('xor', 'R1', 'R1', 'g2p')    # D1 = (a2^a2') ^ (g2^g2')
    m.op('xor', 'R3', 'e2', 'e2p'); m.op('xor', 'R3', 'R3', 'Q')    # D3 = (e2^e2') ^ (c2^c2')
    m.ror('R4', 'P', 1); m.op('xor', 'R4', 'R4', 'P')               # R4 = ROL(D4,7) ^ D1 = (f1^f1') ^ P ^ ROR(P,1)
    m.op('xor', 'R4', 'R4', 'f1'); m.op('xor', 'R4', 'R4', 'f1p')
    m.op('xor', 'R6', 'R6', 'h2'); m.op('xor', 'R6', 'R6', 'h2p')   # D6 = (b2^b2') ^ (h2^h2')
    out.update(R1=m.reg['R1'], R3=m.reg['R3'], R4=m.reg['R4'], R6=m.reg['R6'])
    m.op('or', 'T', 'R1', 'R3'); m.op('or', 'T', 'T', 'R4'); m.op('or', 'T', 'T', 'R6'); m.op('and', 'T', 'T', 'M')
    m.op('add', 'u', 'T', 'M')                  # bit 32 of a lane is 1 iff its R != 0
    m.op('and', 'acc', 'acc', 'u')              # block accumulator: bit 32 of a lane stays 1 iff no trial of that lane so far has R = 0
    out['T'] = m.reg['T']; out['u'] = m.reg['u']
    return out

def block_test(m):
    """End of an X14 block (once per 65,536 trials): branch to step 3 iff some lane of some batch had R = 0."""
    m.part = 'Z'
    m.load('B32', bc(1 << 32), 'ptr'); m.op('and', 'acc', 'acc', 'B32')
    return m.cmp_branch('acc', 'B32')

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

class Scalar:
    """Scalar 32-bit work on the 256-bit machine, every primitive counted (for the per-X14 setup)."""
    def __init__(self): self.n = 0
    def add(self, a, b): self.n += 2; return (a + b) & M32          # add + mask
    def sub(self, a, b): self.n += 2; return (a - b) & M32          # subtract + mask
    def xor(self, a, b): self.n += 1; return a ^ b
    def ror(self, x, r): self.n += 4; return ror(x, r)              # shr, shl, or, and
    def rol(self, x, r): self.n += 4; return rol(x, r)
    def bc(self, v): self.n += 7; return bc(v)                      # 3 x (shift, or) + clear the 8th partial lane

def setup_x14(c, pre):
    """Per-X14 work: the lines of step S1 that read X14 and the X14-dependent packed constants, from the
    values stored per (vc, vd) in `pre`.  Returns (packed constants, operation count incl. the X14 loop)."""
    S = Scalar(); X14 = c['X14']
    ed = S.xor(S.rol(X14, 8), X3); S9 = S.sub(pre['ec'], ed); S14 = S.xor(S.rol(ed, 16), pre['ea'])
    X9 = S.add(pre['ec'], X14); X4 = S.ror(S.xor(pre['eb'], X9), 7)
    S10 = S.add(pre['r'], S14); S6 = S.ror(S.xor(pre['u'], S10), 7); S2 = S.xor(S.rol(S14, 8), pre['q'])
    w5 = S.sub(S2, pre['pu']); w12 = S.sub(pre['taS7'], S2)
    nc = S.sub(S9, pre['S13']); nd = S.sub(nc, IV[1]); na = S.rol(nd, 16); nb = S.ror(S.xor(IV[5], nc), 12)
    S1 = S.xor(pre['rS13'], nd); S5 = S.ror(S.xor(nb, S9), 7); w2 = S.sub(na, pre['iv15']); w3 = S.sub(S.sub(S1, na), nb)
    vb = S.ror(S.xor(X4, pre['vc']), 12)
    out = dict(vb=S.bc(vb), c1k=S.bc(S.sub(pre['nw6'], vb)), k3=S.bc(S.sub(S.sub(0, X4), w2)), k4=S.bc(S.add(S10, X15)),
               S6x=S.bc(S.xor(S6, rol(X11, 12))), X14=S.bc(X14), S5=S.bc(S5), w3=S.bc(w3), X9=S.bc(X9), kA=S.bc(S.sub(S.sub(0, S1), S6)),
               kw12=S.bc(w12), kw8=S.bc(S.sub(pre['nS0'], S5)), w5=S.bc(w5), w5d=S.bc(S.add(w5, DELTA)))
    S.n += 3 + 1                      # next X14, end test, branch; reset of the list pointer
    S.n += 1 + 4                      # acc = all ones (load); block test after the last batch: load 2^32, and, compare, branch
    return out, S.n

def pre_vcvd(c):
    """values stored per (vc, vd) for the X14 loop (uncounted here; bounded per pair in the ledger)"""
    # recompute the lines of step S1 that do not read X14
    ka = (IV[0] + IV[4] + c['w0']) & M32; kd = ror(ka, 16); kc = (IV[0] + kd) & M32; kb = ror(IV[4] ^ kc, 12)
    S8 = rol(c['S4'], 7) ^ kb; S12 = (S8 - kc) & M32; S0 = rol(S12, 8) ^ kd
    X8 = (c['vc'] - c['vd']) & M32; tc = (X8 - c['X13']) & M32; td = (tc - S8) & M32; tb = rol(X7, 7) ^ X8
    S7 = rol(tb, 12) ^ tc; X2 = rol(c['X13'], 8) ^ td; ta = (X2 - tb - W13) & M32; S13 = rol(td, 16) ^ ta
    mb = rol(S7, 7) ^ c['S11']; mc = rol(mb, 12) ^ IV[7]; md = (mc - IV[3]) & M32; S15 = (c['S11'] - mc) & M32; S3 = rol(S15, 8) ^ md
    p = (K + W4) & M32; q = ror(p ^ 55, 16); r = (IV[2] + q) & M32; u = ror(IV[6] ^ r, 12)
    ea = (S3 + c['S4']) & M32; eb = (X3 - ea) & M32; ec = rol(eb, 12) ^ c['S4']
    return dict(ec=ec, ea=ea, eb=eb, r=r, u=u, q=q, pu=(p + u) & M32, taS7=(ta - S7) & M32, S13=S13, rS13=rol(S13, 8),
                iv15=(IV[1] + IV[5]) & M32, vc=c['vc'], nw6=(-c['w6']) & M32, nS0=(-S0) & M32)


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
    return ctx_words(*w[:7]), w[7] & (NMEM - 1)

def forward(c, y):
    A, B, w, wp = trial_words(c, y)
    ta, tb = trace(w, 55), trace(wp, 63)
    E1a, E1b = ta[(1, 'E1')], tb[(1, 'E1')]
    h1 = ta[(1, 'E3')][1]
    beta = E1a[3] ^ E1b[3]; eps = E1a[6] ^ E1b[6]
    n = eps ^ rol(beta ^ eps, 1) ^ ETA
    dA, dB = ta['digest'], tb['digest']
    return dict(A=A, B=B, w=w, y4a=ta[(1, 'C0')][7], y4b=tb[(1, 'C0')][7], eta=h1 ^ tb[(1, 'E3')][1], h1=h1,
                ruleA=ruleA_h1(h1), c1=E1a[2], filt=(E1a[2] & MF) == VF, beta=beta, n=n,
                nd=(dA[3] ^ dB[3]) ^ rol(dA[6] ^ dB[6], 8), half=all(dA[i] == dB[i] for i in (0, 2, 5, 7)), dA=dA, dB=dB)

def batch_members(j): return [min(7 * j + l, NMEM - 1) for l in range(NL)]

def new_machine(c):
    """registers at the start of an X14 block: global and per-pair/per-X14 constants, the list pointer and
    the block accumulator acc (set to all ones by the per-X14 set-up)"""
    return Machine(dict(global_consts(), **ctx_consts(c), ptr=0, acc=W256))

def counted_batch(c, j, m=None):
    m = m or new_machine(c)
    ys = [member(i) for i in batch_members(j)]
    out = run_batch(m, sum(rol(y, 7) << (LW * l) for l, y in enumerate(ys)), sum(y << (LW * l) for l, y in enumerate(ys)))
    return m, ys, out

def residual_words(f):
    """the four words the batch tests, from the two real digests: D1, D3, ROL(D4,7) ^ D1, D6 (Lemma D')"""
    D = {i: f['dA'][i] ^ f['dB'][i] for i in (1, 3, 4, 6)}
    return {'R1': D[1], 'R3': D[3], 'R4': rol(D[4], 7) ^ D[1], 'R6': D[6]}

def check_batch(c, j, verify=None, m=None):
    """Run the counted batch j of context c (on machine m, continuing its block accumulator) and compare
    every lane with the forward computation of its trial: the four packed words must equal D1, D3,
    ROL(D4,7) ^ D1 and D6 of the real digests of A and B, and bit 32 of the lane's indicator must be 1 iff
    the digests differ.  Returns (machine, lanes right, forward results)."""
    m, ys, out = counted_batch(c, j, m)
    Rw = {k: lanes(out[k]) for k in ('R1', 'R3', 'R4', 'R6')}; Tw = lanes(out['T']); Uw = lanes(out['u'])
    right = 0; fs = []
    for l, y in enumerate(ys):
        f = forward(c, y); fs.append(f)
        R = residual_words(f)
        ok = (in_S8(y) and f['half'] and f['y4a'] == y == f['y4b'] and f['eta'] == ETA and len(f['A']) == 55 and len(f['B']) == 63
              and all((Rw[k][l] & M32) == R[k] for k in Rw) and Tw[l] == R['R1'] | R['R3'] | R['R4'] | R['R6'] and f['nd'] == f['n']
              and (Uw[l] >> 32) & 1 == int(f['dA'] != f['dB']))
        if verify is not None:
            ok = ok and struct.unpack('<8I', verify(f['A'], 2)) == f['dA'] and struct.unpack('<8I', verify(f['B'], 2)) == f['dB']
        right += ok
    return m, right, fs

def check_block(c, js, verify=None):
    """Batches js of context c on one machine, then the block test; returns (machine, lanes right,
    test right (branch taken iff some lane of these batches has equal digests), forward results by batch)"""
    m = new_machine(c); right = 0; allf = []
    for j in js:
        m, r, fs = check_batch(c, j, verify, m); right += r; allf.append(fs)
    taken = block_test(m)
    return m, right, int(taken == any(f['dA'] == f['dB'] for fs in allf for f in fs)), allf

X14_OPS = 189
LEDGER = {'A': 38, 'B': 73, 'C': 40, 'D': 48, 'R': 20}   # 219 per batch

def ex_half(seed):
    c, i = seed_trial(seed)
    m, right, br, allf = check_block(c, [i // NL]); fs = allf[0]
    f = fs[i % NL] if batch_members(i // NL)[i % NL] == i else forward(c, member(i))
    return f['A'], f['B'], {'batch_ops': sum(v for k, v in m.ops.items() if k != 'Z'), 'block_test_ops': m.ops['Z'],
                            'lanes_right': right, 'tests_right': br,
                            'member_in_s8': int(in_S8(member(i)))}

def ex_class(seed):
    c, i = seed_trial(seed)
    j0 = min(i // NL, NBATCH - 9) // 9 * 9
    obs = dict(members=0, in_s8=0, y4_equal=0, eta_equal=0, lanes_right=0, tests_right=0, rule_a_lanes=0,
               filter_lanes=0, filter_and_rule_a_lanes=0, lemma_b=lemma_b())
    pair = None; seen = set()
    m, right, br, allf = check_block(c, list(range(j0, j0 + 9)))
    obs['lanes_right'] += right; obs['tests_right'] += br
    for j, fs in zip(range(j0, j0 + 9), allf):
        for idx, f in zip(batch_members(j), fs):
            if idx in seen: continue
            seen.add(idx); y = member(idx)
            obs['members'] += 1; obs['in_s8'] += in_S8(y); obs['y4_equal'] += f['y4a'] == y == f['y4b']
            obs['eta_equal'] += f['eta'] == ETA; obs['rule_a_lanes'] += f['ruleA']; obs['filter_lanes'] += f['filt']
            obs['filter_and_rule_a_lanes'] += f['ruleA'] and f['filt']
            if idx == i: pair = (f['A'], f['B'])
    if pair is None:
        f = forward(c, member(i)); pair = (f['A'], f['B'])
    return pair[0], pair[1], {k: int(v) for k, v in obs.items()}

def pattern_tests(rng):
    """Check of the per-lane indicator and the block test on constructed packed words: for blocks of
    1, 2 and 3 batches, every pattern of zero and nonzero lanes in one batch (all 128) with the other
    batches' lanes random or zero, nonzero lanes random or a single bit, guard bits random."""
    res = dict(ztest_patterns=0, ztest_right=0)
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
    print(json.dumps(res))
    return 0 if tot_r == 185350144 << 80 and (not full or tot_a == tot_r) else 1

def selftest(N, seed):
    verify = None
    root = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), *(['..'] * 5)))
    try:
        sys.path.insert(0, root); from verifier.blake3 import blake3 as verify
    except Exception:
        verify = None
    rng = Rng('s8search selftest %s' % seed)
    st = dict(cases=N, lanes=0, lanes_right=0, tests_right=0, verifier_used=int(verify is not None), rule_a_lanes=0)
    counts = None; same = True; maxlane = {}; maxbnd = {}; regs = 0; resident = 0
    for case in range(N):
        cw = [rng.getrandbits(32) for _ in range(7)]
        if case % 5 == 4: cw = [rng.choice([0, M32, v]) for v in cw]
        c = ctx_words(*cw)
        j = NBATCH - 1 if case % 4 == 3 else rng.randrange(NBATCH)
        m, right, br, allf = check_block(c, [j], verify); fs = allf[0]
        st['lanes'] += NL; st['lanes_right'] += right; st['tests_right'] += br
        st['rule_a_lanes'] += sum(f['ruleA'] for f in fs)
        bo = {k: v for k, v in m.ops.items() if k != 'Z'}
        if counts is None: counts = bo
        same = same and bo == counts and m.ops['Z'] == 4
        for k, v in m.maxlane.items(): maxlane[k] = max(maxlane.get(k, 0), v)
        for k, v in m.maxbnd.items(): maxbnd[k] = max(maxbnd.get(k, 0), v)
        regs = max(regs, liveness(m.prog, m.resident)); resident = len(m.resident)
    st['pattern_tests'] = pattern_tests(rng)
    sok = 0; sn = set()
    for t in range(50):
        c = ctx_words(*[rng.getrandbits(32) for _ in range(7)])
        o, n = setup_x14(c, pre_vcvd(c)); cc = ctx_consts(c); sn.add(n); sok += all(o[k] == cc[k] for k in o)
    mem = [member(i) for i in range(NMEM)]
    s8 = len(set(mem)) == NMEM and all(in_S8(y) for y in mem)
    st.update(counts=counts, batch_ops=sum(counts.values()), same_counts=same, counts_equal_ledger=counts == LEDGER, x14_setup_ops=sorted(sn), x14_setup_right=sok,
              static_bound_over_2_32={k: round(v / 2 ** 32, 3) for k, v in maxbnd.items()},
              largest_lane_over_2_32={k: round(v / 2 ** 32, 3) for k, v in maxlane.items()},
              peak_registers=regs, resident_constants=resident, s8_members=NMEM, s8_ok=int(s8), lemma_b=lemma_b())
    print(json.dumps(st, separators=(',', ':')))
    pt = st['pattern_tests']
    ok = (st['verifier_used'] == 1 and st['lanes_right'] == st['lanes'] and st['tests_right'] == N and same and counts == LEDGER and sok == 50 and sn == {X14_OPS}
          and max(maxbnd.values()) < 1 << LW and regs <= 64 and s8 and st['lemma_b'] == 6 and pt['ztest_right'] == pt['ztest_patterns'] == 768)
    return 0 if ok else 1

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == '--count' and sys.argv[2:] in ([], ['all']): raise SystemExit(model_count(sys.argv[2:] == ['all']))
        if sys.argv[1] != '--selftest' or len(sys.argv) not in (3, 4):
            raise SystemExit('usage: s8search.py --selftest N [seed] | --count [all]   (no arguments: organizer request on stdin)')
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
