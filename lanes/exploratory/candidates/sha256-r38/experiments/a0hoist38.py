#!/usr/bin/env python3
# a0hoist38.py - sha256-r38, the A0-variant attack of ePrint 2026/1120 with the characteristic P8 of dariolina's 1a695f0b (data, credited) and
# per (class, G1) one hoisted plane program (stage 1, the y-independent planes) and per batch one stage-2 plane program (idea: sraiw ff74d392, own code).  Own code (no program of another participant is executed; P8's cells, pair and row-19 conditions are data
# read from the public proof of 1a695f0b, credited in proof.md Section 2).  Standard library only.
# Sections: (1) reference and variant family, (2) plane-program builder and 64-register allocator, (3) bit-sliced E16x filter, (4) counting
# machine and online program, (5) organizer experiments (stdin JSON -> stdout JSON), (6) `selftest`, `calibrate`, `ledger`.
import sys, json, hashlib, struct, math, random
from fractions import Fraction

# ---------------------------------------------------------------- (1) reference
M = 0xffffffff
NR = 38
K = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5, 0xd807aa98, 0x12835b01, 0x243185be,
     0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174, 0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa,
     0x5cb0a9dc, 0x76f988da, 0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967, 0x27b70a85,
     0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb]
IV = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]
def ror(x, n): return ((x >> n) | (x << (32 - n))) & M
def S0(x): return ror(x, 2) ^ ror(x, 13) ^ ror(x, 22)
def S1(x): return ror(x, 6) ^ ror(x, 11) ^ ror(x, 25)
def s0(x): return ror(x, 7) ^ ror(x, 18) ^ (x >> 3)
def s1(x): return ror(x, 17) ^ ror(x, 19) ^ (x >> 10)
def CH(x, y, z): return (x & y) ^ (~x & z & M)
def MAJ(x, y, z): return (x & y) ^ (x & z) ^ (y & z)
def trace(cv, w16, n=NR):
    """A[i], E[i] (i = -4..n-1) and W[0..n-1] of the first n steps from the chaining value cv."""
    W = list(w16)
    for i in range(16, n): W.append((s1(W[i-2]) + W[i-7] + s0(W[i-15]) + W[i-16]) & M)
    A = {-1-i: cv[i] for i in range(4)}; E = {-1-i: cv[4+i] for i in range(4)}
    for i in range(n):
        E[i] = (A[i-4] + E[i-4] + S1(E[i-1]) + CH(E[i-1], E[i-2], E[i-3]) + K[i] + W[i]) & M
        A[i] = (E[i] - A[i-4] + S0(A[i-1]) + MAJ(A[i-1], A[i-2], A[i-3])) & M
    return A, E, W
def compress(cv, w16, n=NR):
    A, E, W = trace(cv, w16, n)
    f = [A[n-1], A[n-2], A[n-3], A[n-4], E[n-1], E[n-2], E[n-3], E[n-4]]
    return [(cv[i] + f[i]) & M for i in range(8)]

# P8 (proof.md Section 3; 1a695f0b Section 3.1 and Appendix C, our transcription).  Member x = M, member y = M'.  Rows 7..22 of A, E, W, MSB
# first: n = (x, y) = (0, 1), u = (1, 0), 0/1 fixed and equal, = equal, + equal to the same bit of the + directly above or below.  Row 19 is
# given on its signed differences only (the accepted event).  CELLS[kind][row] = (mask, x-value, x^y); PQ[i]: bits with E_i = E_{i-1}.
PCV = [0x95a24959, 0xb4053f95, 0x1bf0473e, 0x1eab3b7c, 0x650c63d3, 0xe6493d3b, 0xed004f1d, 0xeb7eaad3]
PMX = [0xbd047e95, 0x1dc94891, 0x4bbe458b, 0xc7dc3c0a, 0x8b6235e1, 0x9d7630ee, 0x569da3a0, 0x94ddb1c2, 0x464e545d, 0xa804c932, 0xacecbe75,
       0xc8280172, 0x9a4d6768, 0x16139532, 0xe00d6a99, 0x5fb2827b]
PMY = [0xbd047e95, 0x1dc94891, 0x4bbe458b, 0xc7dc3c0a, 0x8b6235e1, 0x9d7630ee, 0x569da3a0, 0xb4ddb1c2, 0x420e5c5d, 0x8804c932, 0xa9edacdf,
       0xc8200d72, 0x9a4d6768, 0x16139532, 0xe00d6a99, 0x5bf28a7b]
_ROWS = """=nu============================= uuu============================= ==n=============================
=========n=====n====n======n==== ==n=u====n==nu=====nu===u==n==== =====u===u==========n===========
================================ ======nn===n================n=nn ==u=============================
===============n===========u==== =u=============n===========u==== =====u=n=======n===u==u=n=u=n=n=
====n===============n========u== ==n==n==u=====un================ ============u=======nn==========
==u====u==u==========uu=======u= =nu=u==n==n=====u=n=nn=========u ================================
==n============================= =========n============n=nuu==uu= ================================
====n=========n=========n==n==== ====u=========n================= ================================
======n=u======un=============== ====================n===u======= =====u===n==========n===========
================================ =u==1====n===+u====u0=u=0==+==== ==u=============================
==u============================= =0=====++0===+0=+==01=0=0==+==== ================================
================================ =0=====++1===n1=+==1==1====n==== ================================
================================ ==+====nn=======u=============== ================================
================================ ==+====00====1==0==========1==== ================================
================================ ==u====10=======1=============== ================================
================================ ==0============================= ================================""".split('\n')
CELLS = [[(0, 0, 0)] * NR for _ in range(3)]; PQ = [0] * NR; _PL = {}
for _r, _l in enumerate(_ROWS):
    for _k, _s in enumerate(_l.split()):
        m = v = x = p = 0
        for _j, _c in enumerate(_s):
            b = 1 << (31 - _j); m |= b * (_c in 'un01'); v |= b * (_c in 'u1'); x |= b * (_c in 'un'); p |= b * (_c == '+')
        CELLS[_k][_r + 7] = (m, v, x); _PL[_r + 7] = _PL.get(_r + 7, 0) | p
for _i in _PL: PQ[_i] = _PL[_i] & _PL.get(_i - 1, 0)
PQE = list(PQ); PQE[18] = 0                       # the accepted event does not impose E18 = E17 on bits 24, 23, 15 (Section 6.1); PQ keeps the printed pairs
# two-bit conditions of rows 16..21 (kind1, row1, bit1, equal, kind2, row2, bit2, keyed row = the larger row)
X2 = []
for _t in ('E16 7 = E16 26,E16 14 ! E16 28,A15 4 = A16 4,E16 11 = E16 16,A15 7 = A16 7,A14 15 = A16 15,A14 16 = A16 16,A15 17 = A16 17,'
           'A14 23 = A16 23,A14 25 = A16 25,A15 27 = A16 27,E16 3 ! E16 8,E16 4 = E16 23,W16 20 ! W16 27,W16 22 = W16 31,W16 4 ! W16 6,'
           'A15 29 = A16 29,W16 14 = W16 18,W16 8 = W16 25,W16 1 ! W16 12,A17 9 ! A17 20,A16 15 = A17 15,A17 6 = A17 18,A16 16 ! A17 16,'
           'A16 23 = A17 23,A16 25 = A17 25,A17 8 ! A17 17,E18 0 = E18 13,E18 17 = E18 22,E18 5 ! E18 23,A16 29 = A18 29,E18 9 = E18 23,'
           'E21 10 = E21 15,E21 11 = E21 24,E21 2 = E21 16').split(','):
    _a, _b, _e, _c, _d = _t.split()
    X2.append(('AEW'.index(_a[0]), int(_a[1:]), int(_b), int(_e == '='), 'AEW'.index(_c[0]), int(_c[1:]), int(_d), max(int(_a[1:]), int(_c[1:]))))
def cellok(k, i, x, y):
    m, v, df = CELLS[k][i]
    return (x & m) == v and (x ^ y) == df
def exact(tx, ty): return all(tx[k][i] == ty[k][i] for k in (0, 1) for i in range(34, 38))
def rowok(tx, ty, i):
    """Row i of both traces in the accepted event: cells of A, E, W (not the W cells of rows 7 and 8, replaced by F7 and G), '+' pair,
    two-bit conditions keyed at i."""
    if i < 0: return True
    (Ax, Ex, Wx), (Ay, Ey, Wy) = tx, ty
    if not (cellok(0, i, Ax[i], Ay[i]) and cellok(1, i, Ex[i], Ey[i])): return False
    if i not in (7, 8) and not cellok(2, i, Wx[i], Wy[i]): return False
    if (Ex[i] ^ Ex[i-1]) & PQE[i]: return False
    for (k1, i1, b1, eq, k2, i2, b2, row) in X2:
        if row == i and (((tx[k1][i1] >> b1) ^ (tx[k2][i2] >> b2)) & 1) != (0 if eq else 1): return False
    return True
_tx = trace(PCV, PMX); _ty = trace(PCV, PMY)
SAx = [_tx[0][i] for i in range(16)]; SAy = [_ty[0][i] for i in range(16)]
SE = {i: _tx[1][i] for i in range(4, 16)}
D7, T7 = 0x20000000, 0x03bff800                 # W7y = W7x + D7; the exact filter F7 (no W6 filter at 38 steps)
def inF7(w): return ((s0((w + D7) & M) - s0(w)) & M) == T7

# ---- the A0-variants of S: replace A0 by a0 in both members ----
C4 = (SAx[4] - S0(SAx[3]) - MAJ(SAx[3], SAx[2], SAx[1])) & M          # E4 = a0 + C4
W8C = (SE[8] - SAx[4] - S1(SE[7]) - CH(SE[7], SE[6], SE[5]) - K[8]) & M   # W8x = W8C - E4
D8 = (PMY[8] - PMX[8]) & M; T8 = (s0(PMY[8]) - s0(PMX[8])) & M          # fbc00800, fe808000
def in_G(a0):
    """a0 is a valid variant iff s0(W8y) - s0(W8x) is S's (W8 reaches rows >= 16 only through W23 and W24)."""
    w = (W8C - ((a0 + C4) & M)) & M
    return ((s0((w + D8) & M) - s0(w)) & M) == T8
def c7of(a0):
    """W7x = c7 - A_{-1}."""
    e4 = (a0 + C4) & M
    return (SE[7] - 2 * SAx[3] + S0(SAx[2]) + MAJ(SAx[2], SAx[1], a0) - S1(SE[6]) - CH(SE[6], SE[5], e4) - K[7]) & M
def words_from_cv(cv, a0):
    """W0..W13 of both members connecting cv to the state rows of the variant a0 (Step 2)."""
    out = []
    for SA in (SAx, SAy):
        A = {-1: cv[0], -2: cv[1], -3: cv[2], -4: cv[3]}; E = {-1: cv[4], -2: cv[5], -3: cv[6], -4: cv[7]}
        for i in range(14): A[i] = SA[i]
        A[0] = a0
        for i in range(14): E[i] = (A[i] + A[i-4] - S0(A[i-1]) - MAJ(A[i-1], A[i-2], A[i-3])) & M
        out.append([(E[i] - A[i-4] - E[i-4] - S1(E[i-1]) - CH(E[i-1], E[i-2], E[i-3]) - K[i]) & M for i in range(14)])
    return out
# The 8 classes (advice): (c7, base); a class = {base ^ s : s subset of MASK, in_G, c7of == c7}, 24,576 members each (exhaustive pass,
# Appendix A.1).  Each class is the product LANES x G1 x G3 over the constant bits of its base: 7 free bits and the pair (bit 10, bit 11) in
# {01, 10} (the 256 lanes of a batch), bits 5..4 in G1, bits 30..21 in G3 (96 batches; batch b = (G1[b % 3], G3[b // 3])).
MASK = 0x7fe96c7c
CLASSES = [(0x2a7beb1b, 0x9b649791), (0x2a7bfb1b, 0x9b648791), (0x2a7feb1b, 0x9b609793), (0x2a7ffb1b, 0x9b608793),
           (0xaa7beb1b, 0x1b649791), (0xaa7bfb1b, 0x1b648791), (0xaa7feb1b, 0x1b609793), (0xaa7ffb1b, 0x1b608793)]
LB = (11, 2, 3, 6, 13, 14, 16, 19)               # lane bit k -> bit LB[k] of a0; bit 10 of a0 = NOT bit 11
G1 = (0x10, 0x20, 0x30)
G3 = [int(t, 16) << 20 for t in '1b6 1b8 236 238 240 246 248 24e 250 256 258 260 266 268 26e 270 3b6 3b8 436 438 440 446 448 44e 450 456 458 460 466 468 46e 470'.split()]
NB = 96
def bconst(ci, b): return (CLASSES[ci][1] & ~MASK & M) | G1[b % 3] | G3[b // 3]
def lane_a0(c, L):
    a = c | (0x800 if L & 1 else 0x400)
    for k in range(1, 8): a |= ((L >> k) & 1) << LB[k]
    return a
def class_members(ci): return [lane_a0(bconst(ci, b), L) for b in range(NB) for L in range(256)]
# row 16: E16x = C16 + W0 + s0(W1); its exact pass set R16W (160 words: the 20 heads R16H, any value of the bits 0, 2, 10)
_A, _E = _tx[0], _tx[1]
C16 = (_A[12] + _E[12] + S1(_E[15]) + CH(_E[15], _E[14], _E[13]) + K[16] + s1(PMX[14]) + PMX[9]) & M
R16H = [int(t, 16) for t in ('4b02d320 7b1ab320 7b22b320 7b3ab320 c802f320 c80ad320 c80af320 c812d320 c822f320 c82ad320 c82af320 c832d320 '
                             'cb12f320 cb1ad320 cb1af320 cb22d320 cb32f320 cb3ad320 cb3af320 fb02b320').split()]
R16F = 0x405
R16W = sorted(h | (t & 1) | (t & 2) << 1 | (t & 4) << 8 for h in R16H for t in range(8))
def r16ok(e): return (e & ~R16F & M) in R16H
EM, EV = CELLS[1][16][0], CELLS[1][16][1]
def e16x_ref(cv, a0):
    wx = words_from_cv(cv, a0)[0]
    return (C16 + wx[0] + s0(wx[1])) & M
def e16x(cv, a0):
    """E16x = C16 + W0 + s0(W1) from the Step-2 equations of steps 0 and 1 (the same value as e16x_ref)."""
    a, b, c, d, e, f, g, h = cv
    E0 = (a0 + d - S0(a) - MAJ(a, b, c)) & M
    W0 = (E0 - d - h - S1(e) - CH(e, f, g) - K[0]) & M
    E1 = (SAx[1] + c - S0(a0) - MAJ(a0, a, b)) & M
    W1 = (E1 - c - g - S1(E0) - CH(E0, e, f) - K[1]) & M
    return (C16 + W0 + s0(W1)) & M
# ---------------------------------------------------------------- (2) plane programs: builder, register allocator, interpreter
ONES = (1 << 256) - 1
REGS = 64
class Prog:
    """A DAG of 256-bit plane operations.  A value is (node, neg): the plane of the node, complemented when neg = 1 (complements cost
    nothing: they are absorbed into the next operation, except a mixed and/or, which costs one more).  Node None = constant plane."""
    def __init__(s): s.nodes = []; s.cache = {}
    def _mk(s, op, a, b=None, name=None):
        key = (op, a, b, name)
        if key not in s.cache: s.nodes.append(key); s.cache[key] = len(s.nodes) - 1
        return s.cache[key]
    def const(s, bit): return (None, bit & 1)
    def inp(s, name): return (s._mk('in', None, None, name), 0)
    def notv(s, x): return (x[0], x[1] ^ 1)
    def xor(s, x, y):
        if x[0] is None: return (y[0], y[1] ^ x[1])
        if y[0] is None: return (x[0], x[1] ^ y[1])
        if x[0] == y[0]: return (None, x[1] ^ y[1])
        a, b = (x[0], y[0]) if x[0] < y[0] else (y[0], x[0])
        return (s._mk('xor', a, b), x[1] ^ y[1])
    def and_(s, x, y):
        if x[0] is None: return (None, 0) if x[1] == 0 else y
        if y[0] is None: return (None, 0) if y[1] == 0 else x
        if x[0] == y[0]: return x if x[1] == y[1] else (None, 0)
        if x[1] == 0 and y[1] == 0:
            a, b = (x[0], y[0]) if x[0] < y[0] else (y[0], x[0]); return (s._mk('and', a, b), 0)
        if x[1] == 1 and y[1] == 1:
            a, b = (x[0], y[0]) if x[0] < y[0] else (y[0], x[0]); return (s._mk('or', a, b), 1)
        if x[1] == 1: x, y = y, x
        return s.xor(x, s.and_(x, (y[0], 0)))            # x & ~y' = x ^ (x & y')
    def or_(s, x, y): return s.notv(s.and_(s.notv(x), s.notv(y)))
    def add(s, X, Y, cin=None, need=None):
        """Ripple adder (5 operations per live bit); sum bits only where `need` (default all), carries up to max(need)."""
        n = len(X); c = cin if cin is not None else s.const(0); out = []
        hi = n - 1 if need is None else max(need)
        for j in range(n):
            if j > hi: out.append(None); continue
            t = s.xor(X[j], Y[j])
            out.append(s.xor(t, c) if (need is None or j in need) else None)
            if j < hi: c = s.xor(X[j], s.and_(t, s.xor(X[j], c)))
        return out
    def csa1(s, x, y, z):
        """3:2 compressor on one bit: (sum, carry into the next bit)."""
        t = s.xor(x, y)
        return s.xor(t, z), s.xor(x, s.and_(t, s.xor(x, z)))
    def csa(s, X, Y, Z):
        n = len(X); sm = []; cr = [s.const(0)]
        for j in range(n):
            a, b = s.csa1(X[j], Y[j], Z[j]); sm.append(a)
            if j < n - 1: cr.append(b)
        return sm, cr
    def schedule(s, outs, regs=REGS, stores={}):
        """Belady allocation over the creation order with `regs` registers.  Returns (instrs, result registers).  Every instruction is one
        counted primitive: ('ld', r, name) absolute-address plane, ('ldp', r, name) plane at base register + offset, ('lds', r, slot) reload of
        a spilled value, ('st', slot, r), (op, rd, ra, rb) with op in xor/and/or, ('not', rd, ra)."""
        nodes = s.nodes; N = len(nodes); END = N; NEVER = N + 1
        live = set(n for n, _ in outs) | set(stores); stack = list(live)
        while stack:                                      # dead-code elimination: only nodes that an output depends on are emitted
            n = stack.pop(); op, a, b, nm = nodes[n]
            if op != 'in':
                for x in (a, b):
                    if x not in live: live.add(x); stack.append(x)
        uses = [[] for _ in range(N)]
        for i, (op, a, b, nm) in enumerate(nodes):
            if op == 'in' or i not in live: continue
            uses[a].append(i)
            if b != a: uses[b].append(i)
        for nid, _ in outs: uses[nid].append(END)
        ptr = [0] * N
        def nextuse(n, p):
            u = uses[n]
            while ptr[n] < len(u) and u[ptr[n]] <= p: ptr[n] += 1
            return u[ptr[n]] if ptr[n] < len(u) else NEVER
        reg_of = {}; val_in = {}; free = list(range(regs - 1, -1, -1)); instrs = []; inmem = {}; nslot = [0]
        def evict(p, pinned):
            best = None; bd = -1
            for r, n in val_in.items():
                if r in pinned: continue
                d = nextuse(n, p - 1)
                if d > bd: bd = d; best = r
            n = val_in[best]
            if bd != NEVER and nodes[n][0] != 'in' and n not in inmem:
                instrs.append(('st', nslot[0], best)); inmem[n] = nslot[0]; nslot[0] += 1
            del val_in[best]; del reg_of[n]; free.append(best)
        def getreg(p, pinned):
            if not free: evict(p, pinned)
            return free.pop()
        def need(n, p, pinned):
            if n in reg_of: return reg_of[n]
            r = getreg(p, pinned); op, a, b, nm = nodes[n]
            if op == 'in': instrs.append(('ldp' if nm.startswith('P:') else 'ld', r, nm))
            else: instrs.append(('lds', r, inmem[n]))
            reg_of[n] = r; val_in[r] = n; return r
        for i, (op, a, b, nm) in enumerate(nodes):
            if op == 'in' or i not in live: continue
            pinned = set()
            ra = need(a, i, pinned); pinned.add(ra)
            rb = need(b, i, pinned); pinned.add(rb)
            for n in (a, b):
                if n in reg_of and nextuse(n, i) == NEVER:
                    r = reg_of.pop(n); del val_in[r]; free.append(r)
            rd = getreg(i, {r for r in pinned if r in val_in})
            instrs.append((op, rd, ra, rb)); reg_of[i] = rd; val_in[rd] = i
            if i in stores:
                instrs.append(('sth', stores[i], rd))
                if nextuse(i, i) == NEVER: del reg_of[i]; del val_in[rd]; free.append(rd)
        res = []
        for (nid, neg) in outs:
            r = need(nid, END, set(res))
            if neg: instrs.append(('not', r, r))
            res.append(r)
        return instrs, res

def run_prog(instrs, inputs, planes):
    """Execute on python ints (256-bit words).  inputs: name -> word (absolute addresses); planes: name -> word (batch area)."""
    R = [0] * REGS; mem = {}
    for ins in instrs:
        op = ins[0]
        if op == 'ld': R[ins[1]] = inputs[ins[2]]
        elif op == 'ldp': R[ins[1]] = planes[ins[2]]
        elif op == 'lds': R[ins[1]] = mem[ins[2]]
        elif op == 'st': mem[ins[1]] = R[ins[2]]
        elif op == 'sth': inputs['H%d' % ins[1]] = R[ins[2]]
        elif op == 'xor': R[ins[1]] = R[ins[2]] ^ R[ins[3]]
        elif op == 'and': R[ins[1]] = R[ins[2]] & R[ins[3]]
        elif op == 'or': R[ins[1]] = R[ins[2]] | R[ins[3]]
        elif op == 'not': R[ins[1]] = R[ins[2]] ^ ONES
        else: raise ValueError(op)
    return R

# ---------------------------------------------------------------- (3) the bit-sliced prefilter of E16x
# Lane L of every plane is the variant a0 = lane_a0(c, L) of the batch constant c.  Per first block the broadcast planes (all-zero or all-one
# words) of the scalars HH = d - S0(a) - MAJ(a,b,c), PP = a & b, QQ = a | b, EF = e ^ f, FF = f, K1 = A1(S) - g - K1c and KP = C16 + W0 - a0 are
# loaded.   E0 = a0 + HH;  W1 = K1 - S0(a0) - MAJ(a0,a,b) - S1(E0) - CH(E0,e,f);  E16x = KP + a0 + s0(W1)   (all mod 2^32)
# and the lane passes iff E16x agrees with the row-16 set on the TBITS (the TK lowest bits that the 160 words share).
_inv = M
for _w in R16W: _inv &= ~(_w ^ R16W[0]) & M
TK = 8                                           # tested bits: bits 1, 3..9 (the ledger scan, Section 11, picks TK)
TBITS = [j for j in range(32) if (_inv >> j) & 1][:TK]
TVAL = R16W[0]
PERM = (1, 3, 2, 0)                              # order of the operands SA, MAJ, S1, CH in the carry-save layers (a scan of all 24 orders)
YLO = 20                                         # lowest bit of a0 that changes with the batch's G3 value (y); lower bits of E0 are y-independent
def build_e16(c):
    """Plane DAG of one batch: lane bits are the planes P:A<j> (bit 10 = NOT bit 11), the other bits of a0 the constant c.  One pass over the bit
    positions computes S1, CH, MAJ, SA, three carry-save layers and the ripple step of W1; then E16x = (KP + a0) + s0(W1) up to the highest
    tested bit.  The operands of the S1 xor trees are ordered y-independent first."""
    P = Prog(); one = P.const(1); nt = P.notv
    A = [P.inp('P:A%d' % j) if j in LB else P.const((c >> j) & 1) for j in range(32)]
    A[10] = nt(A[11])
    bc = lambda nm: [P.inp('%s%d' % (nm, j)) for j in range(32)]
    HH, EF, FF, K1, KP, PPi, QQi = (bc(n) for n in ('HH', 'EF', 'FF', 'K1', 'KP', 'PP', 'QQ'))
    E0 = P.add(A, HH)
    s3 = [None] * 32; c3 = [one] + [None] * 31; cc1 = one; cc2 = one; W1 = [None] * 32; cw = one
    for j in range(32):
        k3 = sorted(((j+6) % 32, (j+11) % 32, (j+25) % 32), key=lambda k: (k >= YLO, k))
        S1j = P.xor(P.xor(E0[k3[0]], E0[k3[1]]), E0[k3[2]])
        CHj = P.xor(FF[j], P.and_(E0[j], EF[j]))
        MAJj = (PPi[j] if A[j][1] == 0 else QQi[j]) if A[j][0] is None else P.or_(PPi[j], P.and_(A[j], QQi[j]))
        SAj = P.xor(P.xor(A[(j+2) % 32], A[(j+13) % 32]), A[(j+22) % 32])
        o = [nt(x) for x in (SAj, MAJj, S1j, CHj)]; o = [o[k] for k in PERM]
        a1, n1 = P.csa1(K1[j], o[0], o[1])
        a2, n2 = P.csa1(a1, cc1, o[2])
        a3, n3 = P.csa1(a2, cc2, o[3])
        s3[j] = a3; cc1, cc2 = n1, n2
        if j < 31: c3[j+1] = n3
        t = P.xor(s3[j], c3[j]); W1[j] = P.xor(t, cw)       # W1 = K1 + ~SA + ~MAJ + ~S1 + ~CH + 4 = K1 - (SA + MAJ + S1 + CH)
        if j < 31: cw = P.xor(s3[j], P.and_(t, P.xor(s3[j], cw)))
    zero = P.const(0)
    s0w = [P.xor(P.xor(W1[(j+7) % 32], W1[(j+18) % 32]), W1[j+3] if j + 3 < 32 else zero) for j in range(32)]
    KA = P.add(KP, A, need=set(range(max(TBITS) + 1)))      # KP + a0 (y-independent below bit YLO)
    E16 = P.add(KA[:max(TBITS) + 1] + [zero] * (31 - max(TBITS)), s0w, need=set(TBITS))
    ok = None; P.c0 = len(P.nodes)
    for j in TBITS:
        t = P.xor(E16[j], P.const(1 - ((TVAL >> j) & 1)))
        ok = t if ok is None else P.and_(ok, t)
    return P, ok
_IV = {}
def _sig(P):
    V = []; out = {}; X = (1 << 512) - 1                  # value of every node on one pseudo-random 512-bit input assignment (up to complement)
    for i, (op, a, b, nm) in enumerate(P.nodes):
        if op == 'in': v = _IV.setdefault(nm, int.from_bytes(hashlib.shake_256(nm.encode()).digest(64), 'big'))
        else: x, y = V[a], V[b]; v = x ^ y if op == 'xor' else x & y if op == 'and' else x | y
        V.append(v)
        if op != 'in': out[i] = ((id(P), i), 0) if i >= P.c0 else (min(v, v ^ X), v > v ^ X)
    return out
def _live(P, roots):
    live = set(roots); st = list(live)
    while st:
        n = st.pop(); op, a, b, nm = P.nodes[n]
        if op != 'in':
            for x in (a, b):
                if x not in live: live.add(x); st.append(x)
    return live
_GRP = {}
def group(ci, g1):
    """(stage-1 instructions, [stage-2 (instructions, result register) for the 32 y]).  A node is y-independent if its value (up to complement)
    occurs in the DAG of all 32 batches; stage 1 computes those y-independent nodes that a y-dependent node uses and stores them as planes H<k>."""
    if _GRP and next(iter(_GRP))[0] != ci: _GRP.clear()
    if (ci, g1) in _GRP: return _GRP[(ci, g1)]
    D = []
    for y in range(32):
        P, ok = build_e16(bconst(ci, g1 + 3 * y)); D.append((P, ok, _sig(P)))
    com = set.intersection(*[set(v[0] for v in sg.values()) for _, _, sg in D]); use = set()
    for P, ok, sg in D:
        for n in _live(P, [ok[0]]):
            if P.nodes[n][0] != 'in' and sg[n][0] not in com:
                for x in P.nodes[n][1:3]:
                    if P.nodes[x][0] != 'in' and sg[x][0] in com: use.add(sg[x][0])
    idx = {k: i for i, k in enumerate(sorted(use))}; P0, ok0, sg0 = D[0]
    rep0 = {idx[v[0]]: (n, v[1]) for n, v in sg0.items() if v[0] in idx}
    i1, _ = P0.schedule([], REGS, {rep0[k][0]: k for k in rep0}); st2 = []
    for P, ok, sg in D:
        Q = Prog(); mp = {}
        def val(n):
            if n in mp: return mp[n]
            op, a, b, nm = P.nodes[n]
            if op == 'in': r = Q.inp(nm)
            elif sg[n][0] in idx: r = (Q._mk('in', None, None, 'H%d' % idx[sg[n][0]]), sg[n][1] ^ rep0[idx[sg[n][0]]][1])
            else: r = {'xor': Q.xor, 'and': Q.and_, 'or': Q.or_}[op](val(a), val(b))
            mp[n] = r; return r
        v = val(ok[0]); o = (v[0], v[1] ^ ok[1]); ins, res = Q.schedule([o]); st2.append((ins, res[0]))
    _GRP[(ci, g1)] = (i1, st2); return _GRP[(ci, g1)]
def program(ci, b): return group(ci, b % 3)[1][b // 3]
ORD = [g + 3 * y for g in range(3) for y in range(32)]      # G1 outer, y inner
LPL = {'P:A%d' % j: sum(((L >> k) & 1) << L for L in range(256)) for k, j in enumerate(LB)}   # the 8 lane planes (the same for every batch)
# ---------------------------------------------------------------- (4) the counting machine and the online program
# 256-bit word RAM.  Cost 1 per executed load, store, add, sub, and, or, xor, not, shift, rotate-free primitive, immediate load, random
# word; 2 per compare-and-branch; one target compression (f38) is 1 unit.  Immediates and shift amounts are instruction fields.  A
# 32-bit value lives in the low bits of a word and is masked by one AND where the program needs it exact.  Straight-line plane programs
# are charged their instruction count (Section 9.2: every load, store and spill included, 64 registers).
class Mach:
    def __init__(s, rnd=None): s.ops = 0; s.units = 0; s.mem = {}; s.rnd = rnd
    def li(s, v): s.ops += 1; return v
    def add(s, x, y): s.ops += 1; return x + y
    def sub(s, x, y): s.ops += 1; return x - y
    def and_(s, x, y): s.ops += 1; return x & y
    def or_(s, x, y): s.ops += 1; return x | y
    def xor(s, x, y): s.ops += 1; return x ^ y
    def shl(s, x, n): s.ops += 1; return x << n
    def shr(s, x, n): s.ops += 1; return x >> n
    def ld(s, a): s.ops += 1; return s.mem[a]
    def st(s, a, v): s.ops += 1; s.mem[a] = v
    def br(s): s.ops += 2
    def rand(s): s.ops += 1; return s.rnd()
    def f38(s, m16): s.units += 1; return compress(IV, m16)
def sg(m, x, kind):
    """S0, S1, s0 or s1 of the masked 32-bit x: 8 operations (doubled word, shifts, xors, one mask)."""
    d = m.or_(x, m.shl(x, 32))
    if kind == 'S0': r = m.xor(m.xor(m.shr(d, 2), m.shr(d, 13)), m.shr(d, 22))
    elif kind == 'S1': r = m.xor(m.xor(m.shr(d, 6), m.shr(d, 11)), m.shr(d, 25))
    elif kind == 's0': r = m.xor(m.xor(m.shr(d, 7), m.shr(d, 18)), m.shr(x, 3))
    else: r = m.xor(m.xor(m.shr(d, 17), m.shr(d, 19)), m.shr(x, 10))
    return m.and_(r, M)
def chm(m, e, f, g): return m.xor(g, m.and_(e, m.xor(f, g)))                       # CH: 3 operations
def majm(m, a, b, c): return m.or_(m.and_(a, b), m.and_(c, m.or_(a, b)))          # MAJ: 4 operations
def w7test(m, c7, a):
    r = _w7core(m, c7, a); m.ops += 1                   # one operation: work counter update at the exit taken
    return r
def _w7core(m, c7, a):
    """W7x = c7 - a in F7?  Decision tree on the affine description of F7 (early exits; Section 5.1)."""
    w = m.and_(m.sub(c7, a), M)
    t = m.xor(m.shr(w, 4), w)                                    # bits 14, 15, 16: 14^18, 15^19, 16^20
    m.br()
    if not m.and_(t, 1 << 14): return False
    u = m.xor(m.shr(w, 17), w)                                   # bits 8, 9, 10: 8^25, 9^26, 10^27
    m.br()
    if not m.and_(u, 1 << 8): return False
    v = m.xor(m.shr(w, 11), w)                                   # bits 1, 2, 3: 1^12, 2^13, 3^14
    m.br()
    if m.and_(v, 2): return False
    m.br()
    if not m.and_(w, 1 << 29): return True                       # w29 = 0
    x = m.or_(m.or_(m.and_(t, 1 << 15), m.and_(u, 1 << 9)), m.and_(v, 4))
    m.br()
    if x != (1 << 15 | 1 << 9): return False
    m.br()
    if not m.and_(w, 1 << 30): return True                       # w29 = 1, w30 = 0
    h = m.shr(w, 31)
    y = m.or_(m.or_(m.and_(t, 1 << 16), m.and_(u, 1 << 10)), m.and_(v, 8))
    z = m.or_(m.or_(m.shl(h, 16), m.shl(h, 10)), m.shl(h, 3))
    y = m.xor(y, z)
    m.br()
    return y == (1 << 16 | 1 << 10)
def fb_scalars(m, cv):
    """Per first block: HH = d - S0(a) - MAJ(a,b,c), PP = a & b, QQ = a | b, EF = e ^ f, FF = f, K1 = A1 - g - K1c, KP = C16 + W0 - a0
    (37 operations)."""
    a, b, c, d, e, f, g, h = cv
    pp = m.and_(a, b); qq = m.or_(a, b)
    hh = m.and_(m.sub(m.sub(d, sg(m, a, 'S0')), m.or_(pp, m.and_(c, qq))), M)
    ef = m.xor(e, f)
    kap0 = m.and_(m.sub(m.sub(m.sub(m.sub(m.sub(hh, d), h), sg(m, e, 'S1')), chm(m, e, f, g)), K[0]), M)
    k1 = m.and_(m.sub((SAx[1] - K[1]) & M, g), M)
    kp = m.and_(m.add(kap0, C16), M)
    return dict(HH=hh, PP=pp, QQ=qq, EF=ef, FF=f, K1=k1, KP=kp, KAP0=kap0)
def planes_of(m, name, x):
    """The 32 broadcast planes of a scalar: plane j = 0 - ((x >> j) & 1), stored (3 or 4 operations each)."""
    for j in range(32):
        v = x if j == 0 else m.shr(x, j)
        if j < 31: v = m.and_(v, 1)
        m.st(name + str(j), m.sub(0, v) & ONES)
def first_lane(m, ok):
    """Index of the lowest set lane of the 256-bit word ok (chunk scan, then binary search)."""
    q = 0
    while True:
        t = m.and_(m.shr(ok, 32 * q), M) if q else m.and_(ok, M)
        m.br()
        if t: break
        q += 1
    lb = m.and_(t, m.sub(0, t)); pos = 0
    for k in (16, 8, 4, 2, 1):
        x = m.shr(lb, k); m.br()
        if x: lb = x; pos = m.add(pos, k)
    return m.add(pos, 32 * q) if q else pos
LT = [lane_a0(0, L) for L in range(256)]          # the lane offsets (static table of 256 words)
def static(m):
    """The static tables of the online program (precomputed once): the row-16 heads and the lane offsets."""
    for j in range(32): m.mem[('r16', j)] = R16T[j]
    for L in range(256): m.mem[('lt', L)] = LT[L]
def lane_value(m, c, ell):
    """a0 of lane ell of the batch with constant c: the lane offset from the table, OR the batch constant (an immediate of the batch's code)."""
    return m.or_(m.ld(('lt', ell)), c)
def scalar_e16(m, fb, a0):
    """E16x of the variant a0 from the per-first-block scalars (the Step-2 equations; 38 operations)."""
    e0 = m.and_(m.add(a0, fb['HH']), M)
    t = m.add(sg(m, a0, 'S0'), m.or_(fb['PP'], m.and_(a0, fb['QQ'])))
    t = m.add(t, sg(m, e0, 'S1')); t = m.add(t, m.xor(fb['FF'], m.and_(e0, fb['EF'])))
    w1 = m.and_(m.sub(fb['K1'], t), M)
    return m.and_(m.add(m.add(fb['KP'], a0), sg(m, w1, 's0')), M)
R16T = R16H + [M] * 12                           # the table of the 20 heads, padded to 32 words
def row16_pass(m, e):
    """E16x in the 160-word set: h = E16x with bits 0, 2, 10 cleared, then a fixed-length binary search of h in R16T (5 probes) and one
    comparison (29 operations on every path)."""
    h = m.and_(e, M & ~R16F); lo = 0
    for st in (16, 8, 4, 2, 1):
        j = m.add(lo, st); x = m.ld(('r16', j)); m.br(); m.ops += 1
        if x <= h: lo = j
    x = m.ld(('r16', lo)); m.br()
    return x == h
def row_check(m, i, tx, ty):
    """The tests of row i (rows 16..21; rows 22..37 carry none, the outputs are compared after row 37): member x against the cells, x ^ y
    against the differences, the '+' pair, the two-bit conditions."""
    if i >= 22: return True
    for k in range(3):
        msk, val, df = CELLS[k][i]
        x, y = tx[k][i], ty[k][i]
        if msk:
            t = m.and_(x, msk); m.br()
            if t != val: return False
        d = m.xor(x, y); m.br()
        if d != df: return False
    if PQE[i]:
        t = m.and_(m.xor(tx[1][i], tx[1][i-1]), PQE[i]); m.br()
        if t: return False
    for (k1, i1, b1, eq, k2, i2, b2, row) in X2:
        if row != i: continue
        v = m.and_(m.xor(m.shr(tx[k1][i1], b1), m.shr(tx[k2][i2], b2)), 1); m.br()
        if v != (0 if eq else 1): return False
    return True
def step3b(m, cv, fb, a0):
    """Rows 16..37 of both members for a row-16 pass.  Step 2 (Lemma 4.1: E0..E4 and W0..W8 from the first-block scalars, the other state
    words are those of S), then the rows with an early abort at the first failing test.  Returns (tx, ty) iff all rows hold."""
    a, b, c, d, e, f, g, h = cv
    A = {-1: a, -2: b, -3: c, -4: d, 0: a0}; E = {-1: e, -2: f, -3: g, -4: h}
    for i in range(1, 14): A[i] = SAx[i]
    E[0] = m.and_(m.add(a0, fb['HH']), M)
    for i in (1, 2, 3):
        t = m.sub(m.add(A[i], A[i-4]), sg(m, A[i-1], 'S0'))
        E[i] = m.and_(m.sub(t, majm(m, A[i-1], A[i-2], A[i-3])), M)
    E[4] = m.and_(m.add(a0, C4), M)
    for i in range(5, 14): E[i] = SE[i]
    W = {0: m.and_(m.add(a0, fb['KAP0']), M)}
    for i in range(1, 8):
        t = m.sub(m.sub(E[i], A[i-4]), E[i-4]); t = m.sub(t, sg(m, E[i-1], 'S1')); t = m.sub(t, chm(m, E[i-1], E[i-2], E[i-3]))
        W[i] = m.and_(m.sub(t, K[i]), M)
    W[8] = m.and_(m.sub(W8C, E[4]), M)
    for i in range(9, 16): W[i] = PMX[i]
    Ay = dict(A); Ey = dict(E); Wy = dict(W)
    for i in range(7, 14): Ay[i] = SAy[i]; Ey[i] = _ty[1][i]
    Wy[7] = m.and_(m.add(W[7], D7), M); Wy[8] = m.and_(m.add(W[8], D8), M)
    for i in range(9, 16): Wy[i] = PMY[i]
    for j in (14, 15):
        A[j] = _tx[0][j]; E[j] = _tx[1][j]; Ay[j] = _ty[0][j]; Ey[j] = _ty[1][j]
    tx = (A, E, W); ty = (Ay, Ey, Wy)
    for i in range(16, NR):
        for (Am, Em, Wm) in (tx, ty):
            Wm[i] = m.and_(m.add(m.add(sg(m, Wm[i-2], 's1'), Wm[i-7]), m.add(sg(m, Wm[i-15], 's0'), Wm[i-16])), M)
            t = m.add(m.add(Am[i-4], Em[i-4]), sg(m, Em[i-1], 'S1')); t = m.add(t, chm(m, Em[i-1], Em[i-2], Em[i-3]))
            Em[i] = m.and_(m.add(m.add(t, K[i]), Wm[i]), M)
            t = m.add(m.sub(Em[i], Am[i-4]), sg(m, Am[i-1], 'S0')); Am[i] = m.and_(m.add(t, majm(m, Am[i-1], Am[i-2], Am[i-3])), M)
        if not row_check(m, i, tx, ty): return None
    acc = None
    for k in (0, 1):
        for i in range(34, 38):
            d = m.xor(tx[k][i], ty[k][i]); acc = d if acc is None else m.or_(acc, d)
    m.br()
    return (tx, ty) if acc == 0 else None

class Stats:
    def __init__(s): s.fb = 0; s.hits = 0; s.good = 0; s.pre = 0; s.r16 = 0; s.lane_mism = 0; s.cell_mism = 0; s.classes = 0; s.found = []; s.halt = 0
class Shake:
    """Words from SHAKE-256 of a seed string (the organizer's seed is the only source of randomness)."""
    def __init__(s, seed): s.seed = seed.encode(); s.k = 0; s.buf = b''; s.pos = 0
    def word(s):
        if s.pos + 32 > len(s.buf):
            s.buf = hashlib.shake_256(s.seed + b'|' + str(s.k).encode()).digest(1 << 14); s.k += 1; s.pos = 0
        v = int.from_bytes(s.buf[s.pos:s.pos + 32], 'little'); s.pos += 32; return v
    def below(s, n): return s.word() % n
    def u32(s): return s.word() & M
def unpack16(m, r0, r1):
    out = []
    for r in (r0, r1):
        for k in range(8):
            v = r if k == 0 else m.shr(r, 32 * k)
            out.append(m.and_(v, M) if k < 7 else v)
    return out
def pre_ok(cv, a0):
    """The scalar definition of the prefilter: E16x agrees with the row-16 set on the TBITS."""
    e = e16x(cv, a0)
    return all(((e ^ TVAL) >> j) & 1 == 0 for j in TBITS)
def process_class(m, ci, cv, fb, st, check=True, vmax=None, batches=NB):
    """The 96 batches of class ci: per batch its straight-line program (the batch constant folded), then the passing lanes."""
    inputs = dict(fb['planes'])
    m.li(0); m.li(0); m.li(0)                         # batch pointer, end pointer, class constants
    for k, b in enumerate(ORD[:batches]):
        if k % 32 == 0:
            i1 = group(ci, b % 3)[0]; m.ops += len(i1) + 4; run_prog(i1, inputs, LPL)       # stage 1 of (class, G1)
        ins, res = program(ci, b); c = bconst(ci, b)
        m.ops += len(ins)                             # the straight-line stage-2 program of the batch: every load, store and operation
        ok = run_prog(ins, inputs, LPL)[res]
        st.good += 256
        if check:
            for k in range(256): st.lane_mism += pre_ok(cv, lane_a0(c, k)) != bool((ok >> k) & 1)
        m.br()
        x = ok
        while x:
            ell = first_lane(m, x)
            a0 = lane_value(m, c, ell)
            if check and a0 != lane_a0(c, ell): st.lane_mism += 1
            e = scalar_e16(m, fb, a0); st.pre += 1; m.ops += 1          # work counter update
            if row16_pass(m, e):
                st.r16 += 1
                r = step3b(m, cv, fb, a0); m.ops += 1
                if r: st.found.append((a0, r))
            x = m.and_(x, m.sub(x, 1)); m.br()
        m.ops += 4                                    # batch pointer, loop test
    m.ops += 4                                        # work counter update and cap test
    st.classes += 1
    if vmax is not None and m.ops - 35 * st.fb > vmax: st.halt = 1
def process_fb(m, st, check=True, only_first=False, vmax=None, batches=NB):
    """One first block: two random words, CV1, the 8 W7 tests, and, if a class passes, the per-first-block scalars, the broadcast planes
    and the plane programs of each passing class."""
    r0 = m.rand(); r1 = m.rand()
    M0 = unpack16(m, r0, r1); cv = m.f38(M0); a = cv[0]
    m.ops += 3; st.fb += 1                            # first-block counter, cap compare and branch
    if vmax is not None and m.ops - 35 * st.fb + 2 > vmax: st.halt = 1; return cv, [], M0  # cap test on every block
    hits = []
    for ci, (c7, base) in enumerate(CLASSES):
        m.ops += 4                                    # loop over the class table: load c7, advance the pointer, compare and branch (2)
        if w7test(m, c7, a): hits.append(ci); m.ops += 2        # append to the hit list
    m.br(); st.hits += len(hits)
    if hits:
        m.ops += 1                                    # work counter update
        fb = fb_scalars(m, cv); fb['planes'] = {}
        m.mem.clear()
        for nm in ('HH', 'PP', 'QQ', 'EF', 'FF', 'K1', 'KP'):
            planes_of(m, nm, fb[nm])
        fb['planes'] = {k: v for k, v in m.mem.items() if isinstance(k, str)}
        static(m)
        for ci in (hits[:1] if only_first else hits):
            process_class(m, ci, cv, fb, st, check, vmax, batches)
            if st.halt: break
    return cv, hits, M0

# ---------------------------------------------------------------- (5) organizer experiments
C7SET = frozenset(c[0] for c in CLASSES)
def variant_ok(a0): return in_G(a0) and c7of(a0) in C7SET
def step_row(A, E, W, i):
    E[i] = (A[i-4] + E[i-4] + S1(E[i-1]) + CH(E[i-1], E[i-2], E[i-3]) + K[i] + W[i]) & M
    A[i] = (E[i] - A[i-4] + S0(A[i-1]) + MAJ(A[i-1], A[i-2], A[i-3])) & M
DWT = [(_ty[2][i] - _tx[2][i]) & M for i in range(NR)]           # modular differences of the pair's words (member y minus member x)
def rebuild(Wx, a0, w8):
    """A tail success -> a real semi-free-start pair: W7..W0 by the inverse expansion (member x words W16..W23 and W8..W15), CV1 by
    inverting steps 7..0 of the variant a0.  Returns (cv, mx, my) iff the pair passes every check (equal outputs, m != m', Step 2 returns the
    words, rows -4..21 of the accepted event, W7 in F7, a0 a selected variant)."""
    W = dict(Wx); W[8] = w8
    for i in range(9, 16): W[i] = PMX[i]
    W[7] = (W[23] - s1(W[21]) - W[16] - s0(W[8])) & M
    for i in range(6, -1, -1): W[i] = (W[i+16] - s1(W[i+14]) - W[i+9] - s0(W[i+1])) & M
    Aa = {i: SAx[i] for i in range(8)}; Aa[0] = a0; Ea = {4: (a0 + C4) & M, 5: SE[5], 6: SE[6], 7: SE[7]}
    for i in range(7, -1, -1):
        Aa[i-4] = (Ea[i] - Aa[i] + S0(Aa[i-1]) + MAJ(Aa[i-1], Aa[i-2], Aa[i-3])) & M
        Ea[i-4] = (Ea[i] - Aa[i-4] - S1(Ea[i-1]) - CH(Ea[i-1], Ea[i-2], Ea[i-3]) - K[i] - W[i]) & M
    cv = [Aa[-1], Aa[-2], Aa[-3], Aa[-4], Ea[-1], Ea[-2], Ea[-3], Ea[-4]]
    mx = [W[i] for i in range(16)]; my = list(mx)
    for i in range(7, 16): my[i] = (mx[i] + DWT[i]) & M
    if mx == my or compress(cv, mx) != compress(cv, my) or not inF7(mx[7]) or not variant_ok(a0): return None
    wx, wy = words_from_cv(cv, a0)
    if wx != mx[:14] or wy != my[:14]: return None
    tx, ty = trace(cv, mx), trace(cv, my)
    if not all(rowok(tx, ty, i) for i in range(-4, 22)): return None
    return cv, mx, my
def f7_draw(rng):
    """W7 uniform on F7: one of its three affine families (2^28, 2^24, 2^21 words, Section 5.1) with probability by size, uniform inside."""
    r = rng.below(287309824); w = [rng.u32()]
    def put(k, v): w[0] = w[0] & ~(1 << k) | (v & 1) << k
    b = lambda k: (w[0] >> k) & 1
    put(29, r >= 1 << 28); put(14, b(18) ^ 1); put(8, b(25) ^ 1); put(1, b(12))
    if r >= 1 << 28:
        put(30, r >= 285212672); put(15, b(19) ^ 1); put(9, b(26) ^ 1); put(2, b(13))
        if r >= 285212672: put(16, b(20) ^ b(31) ^ 1); put(10, b(27) ^ b(31) ^ 1); put(3, b(14) ^ b(31))
    return w[0]
# Row-19 proposal of the replica: the ten imposed relations of the row-19 conditions 1-9 and 11 of 1a695f0b (data, Section 7.3): (bit, source,
# flip) sets E19[bit] = E19[source] ^ flip (source -1: the constant flip); set B violates conditions 2, 7 and 8, set A none.
R19A = [(4, -1, 1), (18, -1, 0), (10, 29, 0), (20, 2, 1), (5, 18, 1), (19, 6, 0), (28, 10, 1), (11, 29, 0), (1, 28, 0), (9, 4, 1)]
R19B = [(4, -1, 1), (18, -1, 1), (10, 29, 0), (20, 2, 1), (5, 18, 1), (19, 6, 0), (28, 10, 0), (11, 29, 1), (1, 28, 0), (9, 4, 1)]
# F23 = {w : s1(w + D23) - s1(w) = T23} (the pair's W23 differences; |F23| = 9,830,400, exhaustive pass f23.c, Appendix A.1) by XOR pattern
# w ^ (w + D23): (pattern, size, bits fixed to 1, bits fixed to 0 in the pattern).  Uniform draw: a pattern by size, then rejection in its cylinder.
D23, T23 = DWT[23], (s1(_ty[2][23]) - s1(_tx[2][23])) & M
F23P = [(0x02808000, 1 << 22, 0x02000000, 0x0082a000), (0x01808000, 1 << 22, 0x05800000, 0x0002a000), (0x02818000, 1 << 20, 0x02208000, 0x00836000),
        (0x03818000, 1 << 18, 0x06a08000, 0x01036000), (0x07818000, 1 << 16, 0x04a08000, 0x03036000), (0x06818000, 1 << 16, 0x04608000, 0x03836000)]
NF23 = sum(p[1] for p in F23P)
def f23_draw(rng):
    r = rng.below(NF23)
    for (x, n, f1, f0) in F23P:
        r -= n
        if r < 0: break
    while True:
        w = (rng.u32() | f1) & ~f0
        if (w ^ ((w + D23) & M)) == x and ((s1((w + D23) & M) - s1(w)) & M) == T23: return w
NP_R, CH_R, NT_R = 64, (256, 32, 4, 8, 8), 48
def smc_replicate(rng):
    """One replicate of the sequential Monte-Carlo estimate of q3: row 16 exact (the 160 words), rows 17..21 by proposals with the E cell and
    '+' bits imposed (row 19: one of the two relation sets R19A/R19B, weight 2 x 2^-f), the row and its two-bit conditions checked, multinomial
    resampling; tail: a selected variant (W8), W23 uniform in F23 and W7 = W23 - s1(W21) - W16 - s0(W8) kept iff in F7 (weight |F23|/|F7|), E22x with bit 29 = 0 (W6 = W22 - s1(W20) - W15 - s0(W7), weight 1/2), rows
    22..37 computed with an abort at the first row whose A or E words differ, and the outputs compared.  Every success is rebuilt and run
    through the counted program step3b, which must accept it.  Returns (log2 estimate or None, verified pairs, failed checks, successes, stage logs)."""
    lg = [math.log2(160) - 32]; P = []
    dw16 = (s1(PMY[14]) + PMY[9] - s1(PMX[14]) - PMX[9]) & M
    for _ in range(NP_R):
        e16 = R16W[rng.below(160)]
        Ax = {i: _tx[0][i] for i in range(-4, 16)}; Ex = {i: _tx[1][i] for i in range(-4, 16)}; Wx = {i: PMX[i] for i in range(16)}
        Ay = {i: _ty[0][i] for i in range(-4, 16)}; Ey = {i: _ty[1][i] for i in range(-4, 16)}; Wy = {i: PMY[i] for i in range(16)}
        Wx[16] = (e16 - (Ax[12] + Ex[12] + S1(Ex[15]) + CH(Ex[15], Ex[14], Ex[13]) + K[16])) & M; Wy[16] = (Wx[16] + dw16) & M
        for (A, E, W) in ((Ax, Ex, Wx), (Ay, Ey, Wy)): step_row(A, E, W, 16)
        P.append(((Ax, Ex, Wx), (Ay, Ey, Wy)))
    for i in range(17, 22):
        cm, cvv = CELLS[1][i][:2]; pq = PQ[i]; imp = cm | pq; f = bin(imp).count('1') + 9 * (i == 19); Mi = CH_R[i - 17]; surv = []
        for (tx, ty) in P:
            (Ax, Ex, Wx), (Ay, Ey, Wy) = tx, ty
            rx = (Ax[i-4] + Ex[i-4] + S1(Ex[i-1]) + CH(Ex[i-1], Ex[i-2], Ex[i-3]) + K[i]) & M
            dw = (s1(Wy[i-2]) - s1(Wx[i-2]) + Wy[i-7] - Wx[i-7]) & M
            fixed = cvv | (Ex[i-1] & pq & ~cm & M)
            for _ in range(Mi):
                e = (rng.u32() & ~imp & M) | fixed
                if i == 19:
                    for (bt, sr, fl) in (R19A, R19B)[rng.below(2)]: e = e & ~(1 << bt) | (((e >> sr) & 1 if sr >= 0 else 0) ^ fl) << bt
                wx = (e - rx) & M
                nx = ({**Ax}, {**Ex}, {**Wx, i: wx}); ny = ({**Ay}, {**Ey}, {**Wy, i: (wx + dw) & M})
                step_row(*nx, i); step_row(*ny, i)
                if rowok(nx, ny, i): surv.append((nx, ny))
        if not surv: return None, [], 0, 0, lg
        lg.append(math.log2(len(surv) / (len(P) * Mi)) - f)
        P = [surv[rng.below(len(surv))] for _ in range(NP_R)]
    pairs = []; bad = 0; succ = 0; B29 = 1 << 29
    for (tx, ty) in P:
        (Ax, Ex, Wx), (Ay, Ey, Wy) = tx, ty
        r22 = (Ax[18] + Ex[18] + S1(Ex[21]) + CH(Ex[21], Ex[20], Ex[19]) + K[22]) & M
        for _ in range(NT_R):
            ci, b, L = rng.below(8), rng.below(NB), rng.below(256); a0 = lane_a0(bconst(ci, b), L); w8 = (W8C - (a0 + C4)) & M
            w23 = f23_draw(rng); w7 = (w23 - s1(Wx[21]) - Wx[16] - s0(w8)) & M
            if not inF7(w7): continue
            e22 = rng.u32() & ~B29
            nW = {**Wx}; mW = {**Wy}; nW[7] = w7; mW[7] = (w7 + D7) & M; nW[8] = w8; mW[8] = (w8 + D8) & M
            nW[22] = (e22 - r22) & M; w6 = (nW[22] - s1(Wx[20]) - Wx[15] - s0(w7)) & M
            mW[22] = (s1(Wy[20]) + Wy[15] + s0(mW[7]) + w6) & M
            nA = {**Ax}; nE = {**Ex}; mA = {**Ay}; mE = {**Ey}; ok = True
            for i in range(22, NR):
                if i > 22:
                    nW[i] = (s1(nW[i-2]) + nW[i-7] + s0(nW[i-15]) + nW[i-16]) & M; mW[i] = (s1(mW[i-2]) + mW[i-7] + s0(mW[i-15]) + mW[i-16]) & M
                step_row(nA, nE, nW, i); step_row(mA, mE, mW, i)
                if nA[i] != mA[i] or nE[i] != mE[i]: ok = False; break
            if ok and exact((nA, nE), (mA, mE)):
                succ += 1; r = rebuild(nW, a0, w8)
                if r and step3b(Mach(), r[0], fb_scalars(Mach(), r[0]), a0): pairs.append(r)
                else: bad += 1
    if succ == 0: return None, pairs, bad, 0, lg
    lg.append(math.log2(succ * NF23 / (2 * 287309824 * NP_R * NT_R)))
    return sum(lg), pairs, bad, succ, lg

def pair_check15(cv, a0):
    """Reference check of a good pair: the Step-2 words of (cv, a0) give a trace whose rows 1..15 (A) and 5..15 (E) are S's in both members
    and that follows every cell of rows -4..15 (the W7 and W8 cells excepted); W7 is in F7 and a0 in G."""
    wx, wy = words_from_cv(cv, a0)
    mx = wx + [PMX[14], PMX[15]]; my = wy + [PMY[14], PMY[15]]
    tx, ty = trace(cv, mx, 16), trace(cv, my, 16)
    if not (inF7(mx[7]) and in_G(a0)): return False
    if any(tx[0][i] != SAx[i] or ty[0][i] != SAy[i] for i in range(1, 16)) or any(tx[1][i] != _tx[1][i] or ty[1][i] != _ty[1][i] for i in range(5, 16)): return False
    return all(rowok(tx, ty, i) for i in range(-4, 16))
def online_experiment(req):
    out = []
    for tr in req['trials']:
        t = tr['trial']; rec = dict(trial=t, message_a_hex=None, message_b_hex=None)
        if t < 6:
            rng = Shake(req['experiment_id'] + '|' + tr['seed']); m = Mach(rng.word); st = Stats(); fm = 0; ncell = 0; cm = 0; nfb = 0; hits = []
            while nfb < 64 and not hits:
                nfb += 1; cv, hits, M0 = process_fb(m, st, True, True)
                ref = [ci for ci, c in enumerate(CLASSES) if inF7((c[0] - cv[0]) & M)]
                fm += int(ref != hits)
            if hits:
                mem = class_members(hits[0])
                for a0 in mem[::3072]:
                    ncell += 1; cm += int(not pair_check15(cv, a0))
                wx, wy = words_from_cv(cv, mem[0])
            rec['observations'] = dict(first_blocks=st.fb, w7_classes=len(hits), classes_processed=st.classes, good_pairs=st.good, prefilter_passes=st.pre,
                                       row16_passes=st.r16, counted_ops=m.ops, units=m.units, filter_mismatches=fm, cell_mismatches=cm,
                                       lane_mismatches=st.lane_mism, pairs_cell_checked=ncell)
            if hits and fm == 0 and cm == 0 and st.lane_mism == 0:
                rec['message_a_hex'] = struct.pack('>32I', *(M0 + wx + [PMX[14], PMX[15]])).hex()
                rec['message_b_hex'] = struct.pack('>32I', *(M0 + wy + [PMY[14], PMY[15]])).hex()
        elif t < 14:                                  # coverage: every batch program of class t - 6 on a seed-drawn first block
            ci = t - 6; rng = Shake(req['experiment_id'] + '|' + tr['seed']); m = Mach(rng.word); M0 = unpack16(m, m.rand(), m.rand()); cv = compress(IV, M0)
            fb = fb_scalars(m, cv); inp = {'%s%d' % (nm, j): (ONES if (fb[nm] >> j) & 1 else 0) for nm in ('HH', 'PP', 'QQ', 'EF', 'FF', 'K1', 'KP') for j in range(32)}
            lm = 0; pp = 0
            for b in ORD:
                if b // 3 == 0: run_prog(group(ci, b % 3)[0], inp, LPL)
                ins, res = program(ci, b); okp = run_prog(ins, inp, LPL)[res]; c = bconst(ci, b)
                for k in range(256):
                    v = pre_ok(cv, lane_a0(c, k)); lm += v != bool((okp >> k) & 1); pp += v
            rec['observations'] = dict(class_index=ci, programs=NB, lanes=NB * 256, prefilter_passes=pp, lane_mismatches=lm)
            if lm == 0:
                wx, wy = words_from_cv(cv, bconst(ci, 0) | LT[0])
                rec['message_a_hex'] = struct.pack('>32I', *(M0 + wx + [PMX[14], PMX[15]])).hex()
                rec['message_b_hex'] = struct.pack('>32I', *(M0 + wy + [PMY[14], PMY[15]])).hex()
        out.append(rec)
    return dict(schema_version=1, trials=out)
NREP = 20
Q3_THRESH = -97.0                             # log2 threshold of the pooled mean (frozen before the calibration, Section 7.3)
def q3_experiment(req):
    out = []; est = []; bad_total = 0; last = None
    for tr in req['trials']:
        t = tr['trial']; rec = dict(trial=t, message_a_hex=None, message_b_hex=None)
        if t < NREP:
            rng = Shake(req['experiment_id'] + '|' + tr['seed']); z, pairs, bad, succ, lg = smc_replicate(rng)
            rec['observations'] = dict(log2_estimate=z if z is not None else 0.0, estimate_zero=int(z is None), successes=succ, failed_rebuilds=bad,
                                       verified_pairs=len(pairs), tail_log2=lg[-1] if z is not None else 0.0)
            est.append(0.0 if z is None else 2.0 ** z); bad_total += bad
            if pairs:
                cv, mx, my = pairs[0]; last = pairs[-1]
                rec['message_a_hex'] = struct.pack('>24I', *(cv + mx)).hex(); rec['message_b_hex'] = struct.pack('>24I', *(cv + my)).hex()
        elif t == NREP and len(est) == NREP:
            mean = sum(est) / NREP; lz = math.log2(mean) if mean > 0 else -1000.0
            rec['observations'] = dict(log2_pooled_mean=lz, pooled_zero=int(mean == 0), replicates=NREP, failed_rebuilds=bad_total, pass_threshold_log2=Q3_THRESH)
            if lz >= Q3_THRESH and bad_total == 0 and last:
                cv, mx, my = last
                rec['message_a_hex'] = struct.pack('>24I', *(cv + mx)).hex(); rec['message_b_hex'] = struct.pack('>24I', *(cv + my)).hex()
        out.append(rec)
    return dict(schema_version=1, trials=out)
def run_request(req):
    return online_experiment(req) if 'online' in req['experiment_id'] else q3_experiment(req)

# ---------------------------------------------------------------- (6) selftest, calibrate (every counted constant), ledger
HIT0 = 3137339392           # number of values of A_{-1} (of 2^32) for which none of the 8 classes passes F7 (exhaustive pass, Appendix A.2)
def lane_cost(ell):
    """Operations of one stage-3a lane from the isolated lowest lane to the end of its row-16 test (the same code for every batch)."""
    m = Mach(); fb = fb_scalars(Mach(), PCV); c = bconst(3, 0)
    static(m)
    ok = 1 << ell; k0 = m.ops
    e = first_lane(m, ok); a0 = lane_value(m, c, e); assert e == ell and a0 == lane_a0(c, ell)
    scalar_e16(m, fb, a0); row16_pass(m, e16x(PCV, a0))
    m.and_(ok, m.sub(ok, 1)); m.br(); m.ops += 1
    return m.ops - k0
def w7_distribution():
    """Exact distribution of the cost of one W7 test (20 relevant bits of the word, all assignments)."""
    bits = [14, 18, 8, 25, 1, 12, 29, 30, 15, 19, 9, 26, 2, 13, 16, 20, 31, 10, 27, 3]; cnt = {}
    for x in range(1 << len(bits)):
        w = sum(1 << b for k, b in enumerate(bits) if (x >> k) & 1); m = Mach(); g = w7test(m, w, 0)
        cnt[(m.ops, g)] = cnt.get((m.ops, g), 0) + 1
    return {k: Fraction(v, 1 << len(bits)) for k, v in cnt.items()}
def calibrate(full=True):
    cal = {}
    m = Mach(); fb = fb_scalars(m, PCV); cal['fb_scalars'] = m.ops + 1
    m = Mach()
    for nm in ('HH', 'PP', 'QQ', 'EF', 'FF', 'K1', 'KP'): planes_of(m, nm, fb[nm])
    cal['planes'] = m.ops
    m = Mach(); r = step3b(m, PCV, fb, _tx[0][0]); assert r is not None; cal['step3b'] = m.ops + 1
    rr = Shake('cal'); m = Mach(rr.word); r0 = m.rand(); r1 = m.rand(); M0 = unpack16(m, r0, r1); m.ops += 3; m.br(); cal['fixed'] = m.ops
    if full:
        cal['prog'] = [[len(group(ci, g)[0]) + 4 for g in range(3)] + [len(program(ci, b)[0]) + 6 for b in range(NB)] for ci in range(len(CLASSES))]
        cal['w7'] = w7_distribution()
        cal['lane_max'] = max(lane_cost(ell) for ell in range(256))
        cal['lane_mean'] = Fraction(sum(lane_cost(ell) for ell in range(256)), 256)
    return cal
Q3M, H3M = '-96.2903', '-8.5'                    # q3_model (Section 7.4) and the pair term of H3 (Section 13.5), log2
def ledger(cal=None, show=True, q3_log2=Q3M, h3_log2=H3M, eps_log2=16, succ='0.39', A_C=2**56, A_S=2**56, DEV=2**56):
    from decimal import Decimal, getcontext
    getcontext().prec = 80
    cal = cal or calibrate()
    C = 2728; p7 = Fraction(287309824, 2**32); Kc = len(CLASSES); g = Kc * 24576 * p7; assert g == 13152
    ntb = len(TBITS); two = Decimal(2)
    pany = Fraction(2**32 - HIT0, 2**32); khit = Kc * p7
    w7 = (sum(c * p for (c, ok), p in cal['w7'].items()) + 4) * Kc
    cls = sum(p7 * (7 + sum(cal['prog'][ci])) for ci in range(Kc))
    lanes = Kc * p7 * 24576 * Fraction(1, 2**ntb) * cal['lane_mean']
    r16 = g * Fraction(160, 2**32) * cal['step3b']
    vbar = w7 + 2 * khit + pany * (cal['fb_scalars'] + cal['planes']) + cls + lanes + r16
    class_max = max(7 + sum(cal['prog'][ci]) + 24576 * (cal['lane_max'] + cal['step3b']) for ci in range(Kc))
    wmax = max(c for c, ok in cal['w7']); P0 = Kc * (wmax + 2 + 4) + cal['fb_scalars'] + cal['planes']
    vmax_f = P0 + Kc * class_max
    F = cal['fixed']; PRE = sum(v for _, v in pre_terms()); FIN = 1600
    q3 = two ** Decimal(q3_log2); h3 = 1 - two ** Decimal(h3_log2); eps = Fraction(1, 2**eps_log2)
    N = 1
    for _ in range(6):
        vb = Decimal(vbar.numerator) / Decimal(vbar.denominator)
        pcap = Decimal(vmax_f) / (Decimal(eps.denominator) ** 2 * Decimal(N) * vb) if N > 1 else Decimal(0)
        x = -(Decimal(1) - Decimal(succ) - two ** -60 - pcap).ln()
        N = int((x / (Decimal(g.numerator) / Decimal(g.denominator) * q3 * h3)).to_integral_value(rounding='ROUND_CEILING'))
    VMAX = -((-N * vbar * (1 + eps)).__floor__())
    rows = [('allowance A_C (characteristic search)', A_C * C), ('allowance A_S (Step-1 solve)', A_S * C), ('allowance DEV (development)', DEV * C),
            ('first-block compressions, N_FB x C', N * C), ('fixed operations per first block, N_FB x %d' % F, N * F),
            ('data-dependent operations, cap V_MAX', VMAX), ('overshoot past V_MAX: the work before the first class cap test of a block plus one class at its maximum', P0 + class_max),
            ('precomputation (lane planes, program generation)', PRE), ('final verification (6 compressions and 1600 operations)', 6 * C + FIN)]
    info = dict(N_FB=N, vbar=vbar, VMAX=VMAX, vmax_f=vmax_f, pcap=pcap, g=g, pany=pany, rows=rows)
    if show:
        print('N_FB = %d (2^%.5f); vbar = %.4f (w7 tests %.2f, hit list %.3f, per-first-block scalars and planes %.2f, classes %.2f, lanes %.4f, row 16 %.5f);'
              % (N, math.log2(N), float(vbar), float(w7), float(2 * khit), float(pany * (cal['fb_scalars'] + cal['planes'])), float(cls), float(lanes), float(r16)))
        print('P_cap = %.3e; V_MAX = %d; class max = %d; fixed per first block = %d' % (pcap, VMAX, class_max, F))
    return rows, info
def certificate(N, C, P=100000, digits=5):
    """Smallest a with 2^a C^P <= N^P < 2^(a+1) C^P, and the claim: ceil((a+1)/P) at `digits` decimals."""
    NP, CP = N ** P, C ** P; a = (NP // CP).bit_length() - 1
    while (1 << (a + 1)) * CP <= NP: a += 1
    while (1 << a) * CP > NP: a -= 1
    sc = 10 ** digits
    return a, Fraction(-(-(a + 1) * sc // P), sc)
def report(rows, C=2728, P=100000):
    N = sum(int(v) for _, v in rows); w = max(len(k) for k, _ in rows)
    for k, v in rows: print('%s  %48s' % (k.ljust(w), format(int(v), ',')))
    a, claim = certificate(N, C, P)
    print('N = %d' % N)
    print('certificate: 2^%d * %d^%d <= N^%d < 2^%d * %d^%d' % (a, C, P, P, a + 1, C, P))
    print('log2(N/C) = %.10f' % (math.log2(N) - math.log2(C)))
    print('time_log2 = %.5f' % float(claim))
    return N, claim
def main():
    if len(sys.argv) > 1 and sys.argv[1] == 'ledger':
        rows, info = ledger(); report(rows)
    elif len(sys.argv) > 1 and sys.argv[1] == 'calibrate':
        cal = calibrate(); pr = cal.pop('prog'); print(json.dumps({k: (v if not isinstance(v, dict) else {str(a): str(b) for a, b in v.items()}) for k, v in cal.items()}, indent=1, default=str))
        for ci in range(len(pr)): print('class %d, stage 1 (G1 = 0, 1, 2): %s; stage 2 (batches 0..95): %s' % (ci, ' '.join(str(len(group(ci, g)[0])) for g in range(3)), ' '.join(str(len(program(ci, b)[0])) for b in range(NB))))
    elif len(sys.argv) > 1 and sys.argv[1] == 'selftest':
        selftest()
    else:
        sys.stdout.write(json.dumps(run_request(json.load(sys.stdin))))
def row16_full(e):
    """Every cell of row 16 of both members, its '+' bits and every two-bit condition closing at row 16, as a function of E16x (rows 12..15 are S's)."""
    A, E = _tx[0], _tx[1]; Ay, Ey = _ty[0], _ty[1]
    w16x = (e - (A[12] + E[12] + S1(E[15]) + CH(E[15], E[14], E[13]) + K[16])) & M
    w16y = (w16x + ((s1(PMY[14]) + PMY[9] - s1(PMX[14]) - PMX[9]) & M)) & M
    tr = []
    for (a, ee, w) in ((A, E, w16x), (Ay, Ey, w16y)):
        e16_ = (a[12] + ee[12] + S1(ee[15]) + CH(ee[15], ee[14], ee[13]) + K[16] + w) & M
        tr.append(((e16_ - a[12] + S0(a[15]) + MAJ(a[15], a[14], a[13])) & M, e16_, w))
    X = {0: {**{i: A[i] for i in range(-4, 16)}, 16: tr[0][0]}, 1: {**{i: E[i] for i in range(-4, 16)}, 16: tr[0][1]}, 2: {**{i: PMX[i] for i in range(16)}, 16: tr[0][2]}}
    for k in range(3):
        m, v, d = CELLS[k][16]
        if (tr[0][k] & m) != v or (tr[0][k] ^ tr[1][k]) != d: return False
    if (tr[0][1] ^ E[15]) & PQ[16]: return False
    return all((((X[k1][i1] >> b1) ^ (X[k2][i2] >> b2)) & 1) == (0 if eq else 1) for (k1, i1, b1, eq, k2, i2, b2, row) in X2 if row == 16)
def selftest():
    ok = lambda s: print('ok  ' + s)
    assert compress(PCV, PMX) == compress(PCV, PMY) and PMX != PMY and compress(PCV, PMX)[0] == 0xc7dfd8a1
    assert all(rowok(_tx, _ty, i) for i in range(-4, 22)) and inF7(PMX[7]); ok('P8 pair: equal 38-step outputs (c7dfd8a1 ...), rows -4..21 of the accepted event, W7 in F7')
    a0 = _tx[0][0]
    assert variant_ok(a0) and c7of(a0) == CLASSES[3][0] and words_from_cv(PCV, a0)[0] == PMX[:14]; ok('its A0 %08x is in G and in class 3 (c7 %08x); Step 2 returns its words' % (a0, c7of(a0)))
    for ci, (c7, base) in enumerate(CLASSES):
        mem = class_members(ci); assert len(set(mem)) == 24576 and all(a & ~MASK & M == base & ~MASK & M and in_G(a) and c7of(a) == c7 for a in mem)
    ok('8 classes: 24,576 distinct members each from the product description, every one in G with its c7 and base ^ (subset of %08x)' % MASK)
    assert all(r16ok(w) and row16_full(w) for w in R16W) and len(set(R16W)) == 160; rr = random.Random(5)
    for _ in range(20000):
        e = (EV | (rr.getrandbits(32) & ~EM)) & M; assert row16_full(e) == r16ok(e)
    for w in R16W:
        for _ in range(8):
            e = w ^ (1 << rr.randrange(32)) ^ (1 << rr.randrange(32)); assert row16_full(e) == r16ok(e)
    ok('row-16 set: 160 words pass the full row-16 test; 20,000 random words with the fixed cell bits and 1,280 two-bit neighbours agree with the head test')
    for _ in range(300):
        cv_ = [rr.getrandbits(32) for _ in range(8)]; a_ = lane_a0(bconst(rr.randrange(8), rr.randrange(NB)), rr.randrange(256))
        assert e16x(cv_, a_) == e16x_ref(cv_, a_)
    assert all(((w ^ TVAL) >> j) & 1 == 0 for w in R16W for j in TBITS); ok('E16x formula on 300 chaining values; the %d prefilter bits %s are shared by all 160 words' % (len(TBITS), TBITS))
    for _ in range(4000):
        w = rr.getrandbits(32)
        for t_ in (0, 1):
            if t_: w = (w & ~(1 << 14 | 1 << 8 | 2)) | (((w >> 18) & 1 ^ 1) << 14) | (((w >> 25) & 1 ^ 1) << 8) | (((w >> 12) & 1) << 1)
            assert w7test(Mach(), w, 0) == inF7(w)
    ok('W7 decision tree agrees with the definition of F7 on 8000 words')
    fb = fb_scalars(Mach(), PCV); m = Mach(); r = step3b(m, PCV, fb, a0); assert r is not None
    A, E, W = _tx; assert all(r[0][0][i] == A[i] and r[0][1][i] == E[i] and r[0][2][i] == W[i] for i in range(NR))
    ok('step 3b on the P8 pair: rows 16..21 pass, equal outputs, traces equal the reference (%d operations; 1 more for the work counter)' % m.ops)
    for e in rr.sample(R16W, 8) + [rr.getrandbits(32) for _ in range(8)]:
        m = Mach(); static(m)
        assert row16_pass(m, e) == r16ok(e) and m.ops == 29
    bad = 0
    for t in range(6):
        ci, b = rr.randrange(8), rr.randrange(NB); ins, res = program(ci, b); c = bconst(ci, b)
        cv = [rr.getrandbits(32) for _ in range(8)]; f2 = fb_scalars(Mach(), cv)
        inp = {'%s%d' % (nm, j): (ONES if (f2[nm] >> j) & 1 else 0) for nm in ('HH', 'PP', 'QQ', 'EF', 'FF', 'K1', 'KP') for j in range(32)}
        run_prog(group(ci, b % 3)[0], inp, LPL); okp = run_prog(ins, inp, LPL)[res]; bad += sum(pre_ok(cv, lane_a0(c, k)) != bool((okp >> k) & 1) for k in range(256))
    assert bad == 0; ok('counted row-16 test (29 operations) equals the definition; bit-sliced programs equal the scalar definition on 6 x 256 lanes')
    st = Stats(); m = Mach(); fb = fb_scalars(m, PCV); fb['planes'] = {}
    for nm in ('HH', 'PP', 'QQ', 'EF', 'FF', 'K1', 'KP'): planes_of(m, nm, fb[nm])
    fb['planes'] = {k: v for k, v in m.mem.items() if isinstance(k, str)}
    static(m)
    bp = next(b for b in range(NB) if a0 in [lane_a0(bconst(3, b), L) for L in range(256)])
    bp = ORD.index(bp); k0 = m.ops; process_class(m, 3, PCV, fb, st, True, None, bp + 1)
    assert st.lane_mism == 0 and any(x == a0 for x, _ in st.found); ok('the counted program finds and accepts the P8 pair in batch %d of class 3 (%d operations for batches 0..%d)' % (bp, m.ops - k0, bp))
    st = Stats(); rng = Shake('selftest'); mm = Mach(rng.word); nf = 0
    while not st.classes and nf < 64: nf += 1; process_fb(mm, st, True, True)
    assert st.classes == 1 and st.lane_mism == 0; ok('online program: first block %d, one class of 24,576 good pairs, %d lane mismatches' % (nf, st.lane_mism))
    zs = smc_replicate(Shake('selftest-q3')); assert zs[2] == 0; ok('q3 replicate: estimate 2^%.2f, %d verified 38-step semi-free-start collisions accepted by step3b, %d failed checks' % (zs[0] if zs[0] else 0, len(zs[1]), zs[2]))
    st = Stats(); mm = Mach(Shake('cap').word)
    while not st.halt: process_fb(mm, st, True, True, 1000, 1)
    o = mm.ops; st.halt = 0; process_fb(mm, st, True, True, 1000, 1)
    assert st.halt and mm.ops - o <= 35; ok('cap test on every block: V > V_MAX halts at the next block start, before its 8 W7 tests')
def memory(cal):
    """Bytes of the online program's memory: code at 32 bytes (one word) per instruction, lane planes, broadcast planes, spill slots,
    scalars, the row-16 table and the class table."""
    ninstr = sum(sum(p) - 4 * 3 - 6 * NB for p in cal['prog']); spill = max(sum(1 for x in program(ci, b)[0] if x[0] == 'st') for ci in range(8) for b in range(NB)); nh = max(len(set(i[1] for i in group(ci, g)[0] if i[0] == 'sth')) for ci in range(8) for g in range(3))
    parts = [('code of the %d stage-1 and %d stage-2 programs: %d instructions at 32 bytes' % (24, 8 * NB, ninstr), ninstr * 32), ('hoisted planes H<k> (at most %d)' % nh, nh * 32), ('lane planes (8 words)', 8 * 32),
             ('per-first-block broadcast planes (7 x 32 words)', 7 * 32 * 32), ('spill slots of the batch programs (at most %d used)' % spill, spill * 32),
             ('scalars, counters, hit list, F7 constants and the two traces of step 3b (128 words)', 128 * 32), ('row-16 table (32 words) and lane table (256 words)', 288 * 32),
             ('class table (c7, base: 2 words each)', 8 * 2 * 32), ('code of the W7 test loop: 57 instructions at 32 bytes', 57 * 32),
             ('code of the other routines (first-block words, scalars, planes, lane scan, row 16, step 3b, loops): 700 instructions at 32 bytes', 700 * 32)]
    return parts, sum(v for _, v in parts)
def pre_terms():
    """Precomputation as counted work: the 8 lane planes and the lane table (256 lanes x 8 bits x 4 operations each), and the generation of
    the 768 batch programs (charged 2^32 operations each)."""
    return [('lane planes and lane table: 2 x 256 x 8 x 4 operations', 2 * 256 * 8 * 4), ('generation of the %d plane DAGs, %d stage-1 and %d stage-2 programs (2^32 operations each)' % (8 * NB, 24, 8 * NB), 8 * (2 * NB + 3) * 2 ** 32)]
if __name__ == '__main__': main()
