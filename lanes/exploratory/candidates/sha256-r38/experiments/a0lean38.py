#!/usr/bin/env python3
# a0lean38.py - sha256-r38, the A0-variant attack of ePrint 2026/1120 priced for a program that fits in about one mebibyte.
# Credit and contents: proof.md Sections 2 and 9.  Standard library only; no participant's program is executed.
# Sections: (1) reference, (2) builder/allocator, (3) E16x filter, (4) machine/online program, (5) experiments, (6) checks.
import sys, json, hashlib, struct, math, random, zlib, base64
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

# ePrint 2026/1120 Tables 3-5 (member x = the message printed second).  CELLS[kind][row] = (mask, x-value, x^y difference); kinds A, E, W.
# PQ[i]: bits where E_i = E_{i-1} (the '+' pairs).  X2: two-bit conditions (kind1, row1, bit1, equal, kind2, row2, bit2, keyed row).
PCV = [0xcd278980, 0x1b12a052, 0xb87cc8a6, 0xa9e059c5, 0xc9c3db85, 0x6ca4b5b5, 0x63d13ac1, 0xc0329f1e]
PMX = [0x48fc271b, 0x9fca20cd, 0xcc89f96f, 0xfc40396f, 0x8b328cb4, 0x6b91ef78, 0x97f9b767, 0xc2450045, 0x3f416758, 0xfe9804cb, 0x63a88c0f,
       0x0ceb1f8d, 0xa28cd15a, 0x77a1e994, 0xd28e48a0, 0x9f1f65bb]
PMY = [0x48fc271b, 0x9fca20cd, 0xcc89f96f, 0xfc40396f, 0x8b328cb4, 0x6b91ef78, 0x97f9b767, 0xe2450045, 0x3b016f58, 0xde9804cb, 0x66a99ea5,
       0x0ce30b8d, 0xa28cd15a, 0x77a1e994, 0xd28e48a0, 0x9b5f6dbb]
_CH = [{7: (1610612736, 536870912, 1610612736, 0), 8: (4261904, 16, 4261904, 0), 11: (2060, 2056, 2060, 0), 12: (1142965762, 1073758720, 1142965762, 0), 13: (536936448, 0, 536936448, 0), 14: (134414480, 134217872, 134414480, 0), 15: (41975808, 8388608, 41975808, 0), 17: (536870912, 536870912, 536870912, 0)}, {5: (0, 0, 0, 3758096384), 6: (138678416, 134480016, 0, 3758622720), 7: (3939897499, 3804237825, 3758096384, 67635200), 8: (3957292027, 2299865209, 139204752, 67108864), 9: (4278190015, 3329275675, 76546059, 0), 10: (1040153503, 683879063, 4261888, 0), 11: (3187670975, 2163392958, 536899588, 64), 12: (4261412799, 1570574870, 1008926725, 64), 13: (4293918591, 901856013, 67450, 128), 14: (2086891391, 537027697, 134283264, 4224), 15: (1246957562, 1242762074, 2176, 4096), 16: (1279466112, 1208156800, 1078071808, 262160), 17: (1086462592, 2048, 0, 17072144), 18: (1086722608, 4330000, 262160, 16809984), 19: (830770738, 805569584, 25198592, 0), 20: (562331664, 537133072, 0, 0), 21: (562072576, 553682944, 536870912, 0), 22: (536870912, 0, 0, 0), 23: (536870912, 536870912, 0, 0)}, {7: (536870912, 0, 536870912, 0), 8: (71305216, 71303168, 71305216, 0), 9: (536870912, 536870912, 536870912, 0), 10: (83956394, 16777226, 83956394, 0), 11: (529408, 529408, 529408, 0), 15: (71305216, 67108864, 71305216, 0), 16: (536870912, 536870912, 536870912, 0), 23: (92446720, 92446720, 25198592, 0), 25: (536870912, 0, 536870912, 0)}]
CELLS = [[(0, 0, 0, 0)] * NR for _ in range(3)]
for _k in range(3):
    for _i, _c in _CH[_k].items(): CELLS[_k][_i] = _c
PQ = [0, 0, 0, 0, 0, 0, 3758096384, 526336, 67108864, 0, 0, 0, 64, 0, 128, 4096, 0, 262160, 16809984, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
X2 = [(0, 14, 15, 1, 0, 16, 15, 16), (0, 14, 23, 1, 0, 16, 23, 16), (0, 14, 25, 1, 0, 16, 25, 16), (0, 15, 4, 1, 0, 16, 4, 16), (0, 15, 7, 1, 0, 16, 7, 16), (0, 15, 16, 0, 0, 16, 16, 16), (0, 15, 17, 1, 0, 16, 17, 16), (0, 15, 27, 1, 0, 16, 27, 16), (0, 15, 29, 1, 0, 16, 29, 16), (0, 16, 15, 1, 0, 17, 15, 17), (0, 16, 23, 1, 0, 17, 23, 17), (0, 16, 25, 1, 0, 17, 25, 17), (0, 17, 9, 1, 0, 17, 20, 17), (0, 17, 6, 1, 0, 17, 18, 17), (0, 17, 8, 1, 0, 17, 17, 17), (0, 16, 29, 1, 0, 18, 29, 18), (0, 18, 29, 1, 0, 19, 29, 19), (1, 16, 4, 0, 1, 16, 23, 16), (1, 16, 3, 0, 1, 16, 8, 16), (1, 16, 14, 1, 1, 16, 28, 16), (1, 16, 4, 1, 1, 17, 4, 17), (1, 16, 18, 1, 1, 17, 18, 17), (1, 18, 0, 0, 1, 18, 13, 18), (1, 17, 15, 1, 1, 18, 15, 18), (1, 17, 24, 1, 1, 18, 24, 18), (1, 19, 6, 0, 1, 19, 19, 19), (1, 19, 20, 1, 1, 19, 2, 19), (1, 21, 2, 1, 1, 21, 16, 21), (2, 7, 8, 0, 2, 7, 25, 7), (2, 7, 14, 0, 2, 7, 18, 7), (2, 7, 1, 1, 2, 7, 12, 7), (2, 8, 0, 0, 2, 8, 28, 8), (2, 8, 30, 0, 2, 8, 9, 8), (2, 8, 1, 1, 2, 8, 18, 8), (2, 16, 1, 0, 2, 16, 12, 16), (2, 16, 20, 0, 2, 16, 27, 16), (2, 16, 8, 1, 2, 16, 25, 16), (2, 16, 14, 1, 2, 16, 18, 16), (2, 16, 4, 0, 2, 16, 6, 16), (2, 16, 22, 0, 2, 16, 31, 16), (2, 23, 0, 0, 2, 23, 30, 23), (2, 23, 1, 0, 2, 23, 31, 23), (2, 23, 14, 1, 2, 23, 21, 23), (2, 23, 16, 1, 2, 23, 25, 23), (2, 25, 4, 1, 2, 25, 6, 25), (2, 25, 22, 1, 2, 25, 31, 25), (2, 25, 20, 1, 2, 25, 27, 25)]
def cellok(k, i, x, y):
    m, v, df = CELLS[k][i][:3]
    return (x & m) == v and (x ^ y) == df
P19 = (0x00040832, 0x10000010, 0x20000c12, 0x30040430); M19 = 0x30040e32; B29 = 1 << 29
def ecell(i, Ex, Ey):
    """E cell of row i in the accepted event: row 19 takes any of the four patterns P19 on the bits M19, row 20 the tie E20[29] = E19[29]
    in place of its value bit 29; every other value bit and every XOR difference as printed."""
    m, v, d = CELLS[1][i][:3]
    t = (Ex[19] & M19) in P19 if i == 19 else not (Ex[20] ^ Ex[19]) & B29 if i == 20 else True
    m &= ~(M19 if i == 19 else B29 if i == 20 else 0)
    return t and (Ex[i] & m) == (v & m) and (Ex[i] ^ Ey[i]) == d
def exact(tx, ty): return all(tx[k][i] == ty[k][i] for k in (0, 1) for i in range(34, 38))
def rowok(tx, ty, i):
    """Row i of both traces in the accepted event: cells of A, E (ecell), W (not the W cells of rows 7..10), '+' pair, two-bit conditions keyed at i."""
    if i < 0: return True
    (Ax, Ex, Wx), (Ay, Ey, Wy) = tx, ty
    if not (cellok(0, i, Ax[i], Ay[i]) and ecell(i, Ex, Ey)): return False
    if (i < 7 or i > 10) and not cellok(2, i, Wx[i], Wy[i]): return False
    if (Ex[i] ^ Ex[i-1]) & PQ[i]: return False
    for (k1, i1, b1, eq, k2, i2, b2, row) in X2:
        if row == i and (((tx[k1][i1] >> b1) ^ (tx[k2][i2] >> b2)) & 1) != (0 if eq else 1): return False
    return True
_tx = trace(PCV, PMX); _ty = trace(PCV, PMY)
SAx = [_tx[0][i] for i in range(14)]; SAy = [_ty[0][i] for i in range(14)]
SE = {i: _tx[1][i] for i in range(4, 14)}
D7, T7 = 0x20000000, 0x03bff800                 # W7y = W7x + D7; the exact filter F7 (no W6 filter at 38 steps)
def inF7(w): return ((s0((w + D7) & M) - s0(w)) & M) == T7

# ---- the A0-variants of S: replace A0 by a0 in both members ----
C4 = (SAx[4] - S0(SAx[3]) - MAJ(SAx[3], SAx[2], SAx[1])) & M          # E4 = a0 + C4
W8C = (SE[8] - SAx[4] - S1(SE[7]) - CH(SE[7], SE[6], SE[5]) - K[8]) & M   # W8x = W8C - E4
D8 = (PMY[8] - PMX[8]) & M
def in_G(a0):
    w = (W8C - ((a0 + C4) & M)) & M; y = (w + D8) & M
    m, v, df = CELLS[2][8][:3]
    if (w & m) != v or (w ^ y) != df: return False
    b = lambda k: (w >> k) & 1
    return b(0) != b(28) and b(30) != b(9) and b(1) == b(18)
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
# the 90 classes (advice): `c7 base mask-low-16-bits program`; a class = {base ^ s : s subset of mask, in_G, c7of == c7}, 3840 members each.
# The 64 smallest c7 are the earlier filing's classes; the 26 others are the remaining size-3840 classes of the same family and shapes.
_CT = zlib.decompress(base64.b64decode('eNpd1N1xhDAMReH3VLElyCwoUA4Cu/8SYn7OxLqv+WZzB8ScvS1rrWf7mO/FSvHPMp/lM//sN9QvMGVo/GK6frGVT3mgGb+YJoFfoAoEsGfY3g1b+sbSx/2F/QtMAr9AFQhgzxBs+Psc0wsHGz4JsOFVgA3fM/B2Td5u4+2avN1W2ShVgI2yZ+Aelu/RjHtYvkcHNvI9OrCR7nH0j6FcsPSPYX7Gv8ACmMAJrAma8a+m+dkwgH81mcAGHAJsTGuG/d2wZX5uvgALYAIbcAicwJrhYMPn4eYXsOEmwIYfAmz4moHXbvLaG6/d5LW3ykY5BNjI9+g3ZyPfowMb+R4d2Mj36MDGeA8nMiGRcSITEhknMiGRcSITEhknMiGRcSITEhknMiGRcSITEhknMiGRcSITEhknMiGRcSITEhknMiGRcSITEhknMiGRcSITEhknMiGRcSITEhknMiGRcSLT/275Hm9kbqgCAYz3IDJl7t/08LU7kbnBBE5gTfBE5oLxo3Yic4MJbMAhwEb6qIlMB7MhMk5kbjCBDTgETmDNcLAxRsaJzA0mwMYYGScyN6wZ6vgc40us43MkGJ8jwfgc//BG5oJ8jzcyN5gAG/keb2Ru4B5/WsYVUg==')).decode().split('\n')
CLASSES = [(int(a, 16), int(b, 16), int('91eb' + m, 16)) for a, b, m, g in map(str.split, _CT)]
GRP = [int(l.split()[3]) for l in _CT]
def class_members(c7, base, mask):
    out, s = [], 0
    while True:
        a = base ^ s
        if in_G(a) and c7of(a) == c7: out.append(a)
        s = (s - mask) & mask
        if s == 0: break
    return sorted(out)
# row 16: E16x = C16 + W0 + s0(W1); its exact pass set (32 words, additive: R16B + any subset sum of R16F) and the ten cell bits
_A, _E = _tx[0], _tx[1]
C16 = (_A[12] + _E[12] + S1(_E[15]) + CH(_E[15], _E[14], _E[13]) + K[16] + s1(PMX[14]) + PMX[9]) & M
R16B, R16F = 0x481b02f9, 0x82405
def r16ok(e): return ((e - R16B) & M & ~R16F) == 0
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
    def schedule(s, outs, regs=REGS):
        """Belady allocation over the creation order with `regs` registers.  Returns (instrs, result registers).  Every instruction is one
        counted primitive: ('ld', r, name) absolute-address plane, ('ldp', r, name) plane at base register + offset, ('lds', r, slot) reload of
        a spilled value, ('st', slot, r), (op, rd, ra, rb) with op in xor/and/or, ('not', rd, ra)."""
        nodes = s.nodes; N = len(nodes); END = N; NEVER = N + 1
        live = set(n for n, _ in outs); stack = list(live)
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
        elif op == 'xor': R[ins[1]] = R[ins[2]] ^ R[ins[3]]
        elif op == 'and': R[ins[1]] = R[ins[2]] & R[ins[3]]
        elif op == 'or': R[ins[1]] = R[ins[2]] | R[ins[3]]
        elif op == 'not': R[ins[1]] = R[ins[2]] ^ ONES
        else: raise ValueError(op)
    return R

# ---------------------------------------------------------------- (3) the bit-sliced prefilter of E16x
# Lane L of every plane is variant a0 = (member L).  Per first block the broadcast planes (all-zero or all-one words) of the scalars
# HH = d - S0(a) - MAJ(a,b,c), PP = a & b, QQ = a | b, EF = e ^ f, FF = f, K1 = A1(S) - g - K1c and KP = C16 + W0 - a0 are loaded.
#   E0 = a0 + HH;  W1 = K1 - S0(a0) - MAJ(a0,a,b) - S1(E0) - CH(E0,e,f);  E16x = KP + a0 + s0(W1)   (all mod 2^32)
# and the lane passes iff E16x agrees with the row-16 set on the TBITS (the ten cell bits and TX further bits that the 32 words share).
def _r16words():
    fb = [1, 4, 0x400, 0x2000, 0x80000]
    return sorted((R16B + sum(f for k, f in enumerate(fb) if (t >> k) & 1)) & M for t in range(32))
R16W = _r16words()
_inv = M
for _w in R16W: _inv &= ~(_w ^ R16W[0]) & M
TK = 12                                          # tested bits: the TK lowest bits that the 32 words share (the ledger scan, Section 11, picks TK)
TBITS = [j for j in range(32) if (_inv >> j) & 1][:TK]
TVAL = R16W[0]
PERM = (1, 3, 2, 0)                              # order of the operands SA, MAJ, S1, CH in the carry-save layers (a scan of all 24 orders)
def build_e16(mask, base, shared=0):
    """The program for a class shape: bits of a0 in `mask` are batch planes, bits in `shared` are per-class inputs C<j>, the rest is the
    constant `base`.  One pass over the bit positions j = 0..31 computes S1, CH, MAJ, SA of bit j, the three carry-save layers and the
    ripple step of W1; then the E16x sum is formed up to the highest tested bit."""
    P = Prog(); one = P.const(1); zero = P.const(0); nt = P.notv
    A = []
    for j in range(32):
        if (mask >> j) & 1: A.append(P.inp('P:A%d' % j))
        elif (shared >> j) & 1: A.append(P.inp('P:C%d' % j))
        else: A.append(P.const((base >> j) & 1))
    bc = lambda nm: [P.inp('%s%d' % (nm, j)) for j in range(32)]
    HH, EF, FF, K1, KP, PPi, QQi = (bc(n) for n in ('HH', 'EF', 'FF', 'K1', 'KP', 'PP', 'QQ'))
    E0 = P.add(A, HH)
    s3 = [None] * 32; c3 = [one] + [None] * 31; cc1 = one; cc2 = one; W1 = [None] * 32; cw = one
    for j in range(32):
        S1j = P.xor(P.xor(E0[(j+6) % 32], E0[(j+11) % 32]), E0[(j+25) % 32])
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
    s, c = P.csa(KP, A, s0w)
    E16 = P.add(s, c, need=set(TBITS))
    ok = None
    for j in TBITS:
        t = P.xor(E16[j], P.const(1 - ((TVAL >> j) & 1)))
        ok = t if ok is None else P.and_(ok, t)
    return P, ok
_PROG = {}
def shape_of(g):
    """Shared constant positions of plane program g: the positions outside the mask where its classes differ."""
    cls = [c for c, h in zip(CLASSES, GRP) if h == g]; mask = cls[0][2]
    sh = 0
    for c in cls: sh |= (c[1] ^ cls[0][1]) & ~mask & M
    return sh, cls[0][1] & ~mask & ~sh & M
def program(g):
    if g not in _PROG:
        sh, cb = shape_of(g); P, ok = build_e16(CLASSES[GRP.index(g)][2], cb, sh); ins, res = P.schedule([ok]); _PROG[g] = (ins, res[0], sh)
    return _PROG[g]

# ---------------------------------------------------------------- (4) the counting machine and the online program
# 256-bit word RAM.  Cost 1 per executed load, store, add, sub, and, or, xor, not, shift, rotate-free primitive, immediate load, random
# word; 2 per compare-and-branch; one target compression (f38) is 1 unit.  Immediates and shift amounts are instruction fields.  A
# 32-bit value lives in the low bits of a word and is masked by one AND where the program needs it exact.  Straight-line plane programs
# are charged their instruction count (Section 2: every load, store and spill included, 64 registers).
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
class ClassData:
    """Planes of the 15 batches of a class (bit L of 'P:A<j>' of batch b = bit j of member 256 b + L) and its shared-constant words."""
    def __init__(s, ci):
        c7, base, mask = CLASSES[ci]; s.ci = ci; s.members = class_members(c7, base, mask)
        assert len(s.members) == 3840
        s.batches = []
        for b in range(15):
            mem = s.members[256 * b:256 * b + 256]
            s.batches.append({'P:A%d' % j: sum(((x >> j) & 1) << k for k, x in enumerate(mem)) for j in range(32) if (mask >> j) & 1})
        s.sh = shape_of(GRP[ci])[0]; s.cw = {'P:C%d' % j: (ONES if (base >> j) & 1 else 0) for j in range(32) if (s.sh >> j) & 1}
        s.mask = mask; s.base = base
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
def lane_value(m, cd, b, ell):
    """a0 of lane ell of batch b from the stored planes (conditional shifts by 128, 64, ..., 1, then the bit of each plane)."""
    mask = cd.mask; js = [j for j in range(32) if (mask >> j) & 1]
    xs = [m.ld(('plane', cd.ci, b, j)) for j in js]
    for k in range(8):
        m.br()
        if (ell >> k) & 1: xs = [m.shr(x, 1 << k) for x in xs]
    acc = None
    for j, x in zip(js, xs):
        bit = m.and_(x, 1); bit = m.shl(bit, j) if j else bit
        acc = bit if acc is None else m.or_(acc, bit)
    return m.or_(acc, cd.base & ~mask & M)                  # the constant bits of the class are an immediate
def scalar_e16(m, fb, a0):
    """E16x of the variant a0 from the per-first-block scalars (the Step-2 equations; 38 operations)."""
    e0 = m.and_(m.add(a0, fb['HH']), M)
    t = m.add(sg(m, a0, 'S0'), m.or_(fb['PP'], m.and_(a0, fb['QQ'])))
    t = m.add(t, sg(m, e0, 'S1')); t = m.add(t, m.xor(fb['FF'], m.and_(e0, fb['EF'])))
    w1 = m.and_(m.sub(fb['K1'], t), M)
    return m.and_(m.add(m.add(fb['KP'], a0), sg(m, w1, 's0')), M)
def row16_pass(m, e):
    m.br()
    return m.and_(m.sub(e, R16B), M & ~R16F) == 0

def row_check(m, i, tx, ty):
    """The tests of row i (rows 16..21; rows 22..37 carry none, the exact event is tested after row 37): member x against the cells
    (row 19: one AND, then one compare-and-branch per pattern of P19, the published one last; row 20: value bit 29 dropped, the tie
    E20[29] = E19[29] by xor, and, branch), x ^ y against the differences, the '+' pair, the two-bit conditions."""
    if i >= 22: return True
    for k in range(3):
        msk, val, df = CELLS[k][i][:3]
        x, y = tx[k][i], ty[k][i]
        if msk and k == 1 and i == 19:
            t = m.and_(x, msk)
            for p in sorted(P19, key=lambda q: q == val & M19):
                m.br()
                if t == (val & ~M19) | p: break
            else: return False
        elif msk and k == 1 and i == 20:
            t = m.and_(x, msk & ~B29); m.br()
            if t != val & ~B29: return False
            t = m.and_(m.xor(x, tx[1][19]), B29); m.br()
            if t: return False
        elif msk:
            t = m.and_(x, msk); m.br()
            if t != val: return False
        d = m.xor(x, y); m.br()
        if d != df: return False
    if PQ[i]:
        t = m.and_(m.xor(tx[1][i], tx[1][i-1]), PQ[i]); m.br()
        if t: return False
    for (k1, i1, b1, eq, k2, i2, b2, row) in X2:
        if row != i: continue
        v = m.and_(m.xor(m.shr(tx[k1][i1], b1), m.shr(tx[k2][i2], b2)), 1); m.br()
        if v != (0 if eq else 1): return False
    return True
def majm(m, a, b, c): return m.or_(m.and_(a, b), m.and_(c, m.or_(a, b)))
def step3b(m, cv, fb, a0):
    """Rows 16..37 of both members for a row-16 pass.  Step 2 (Lemma 4.1: E0..E4 and W0..W8 from the first-block scalars, the other state
    words are the published ones), then the rows with an early abort at the first failing test.  Returns (tx, ty) iff all rows hold."""
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
_CD = {}
def classdata(ci):
    if ci not in _CD: _CD[ci] = ClassData(ci)
    return _CD[ci]
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
def process_class(m, ci, cv, fb, st, check=True, vmax=None):
    cd = classdata(ci); ins, res, sh = program(GRP[ci])
    for b in range(15):
        for name, w in cd.batches[b].items(): m.mem[('plane', ci, b, int(name[3:]))] = w
    inputs = dict(fb['planes'])
    m.li(0); m.li(0); m.li(0)                         # batch pointer, end pointer, class constants
    for b in range(15):
        m.ops += len(ins)                             # the straight-line program of the shape: every load, store and operation
        R = run_prog(ins, inputs, {**cd.batches[b], **cd.cw}); ok = R[res]
        st.good += 256
        if check:
            for k in range(256):
                if pre_ok(cv, cd.members[256 * b + k]) != bool((ok >> k) & 1): st.lane_mism += 1
        m.br()
        x = ok
        while x:
            ell = first_lane(m, x)
            a0 = lane_value(m, cd, b, ell)
            if check and a0 != cd.members[256 * b + ell]: st.lane_mism += 1
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
def process_fb(m, st, check=True, only_first=False, vmax=None):
    """One first block: two random words, CV1, the 64 W7 tests, and, if a class passes, the per-first-block scalars, the broadcast planes
    and the bit-sliced program on each passing class."""
    r0 = m.rand(); r1 = m.rand()
    M0 = unpack16(m, r0, r1); cv = m.f38(M0); a = cv[0]
    m.ops += 3; st.fb += 1                            # first-block counter, cap compare and branch
    if vmax is not None and m.ops - 35 * st.fb + 2 > vmax: st.halt = 1; return cv, [], M0  # cap test on every block
    hits = []
    for ci, (c7, base, mask) in enumerate(CLASSES):
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
        for ci in (hits[:1] if only_first else hits):
            process_class(m, ci, cv, fb, st, check, vmax)
            if st.halt: break
    return cv, hits, M0

# ---------------------------------------------------------------- (5) organizer experiments
VARIANTS = list(struct.unpack('<512I', zlib.decompress(base64.b64decode('eNoNlP9vU9cZh4/R9X3p2Lpz6bn3jFZrR0gcEr5kJCgQp5R7yXWy0Aau4RoUmKZ1X0TXTuKHTUXqNDp12zmbtrUbsHNYNdHaaWxs187i0ASbihBHdhqnNiTZ0trpyloK28pKu/5A1a1i8z/w6nnf9/N5kihiBPBl8RaOwSotZ5xxIiA8c+wb9m5+EM+KG05O/cAuUosMG7/AZcCmj/8ENcNxVFP/btYEUQrqd0hFjYaq/D17WNVRTO50w/RxJa4+iUfVa3aefpWk2LfxovgIF4G4e/geJcx+jArGxlCAT2sLcgQ30C94U7IJR6UIzvJTnrRaUfaDj3TziLKWnwgtsCErbpzVi7wtNEpdkuZHlSnK0AK7Zc/yFd5BII4PuoJFYyOJqQ16jU1oVfE2rsJnSoFNe7vobpKAbzmD/HkzDC/qaTUdWgufusPCsIN8M5ljKwJ+0JQR42duke0M+Om/SDPPhPL8SbQMHYGasY9Y8NvAJnjV3QTXlIj4Ohlmk/qo0aT45HP2Ltri8ckJbUE8TTbQPrJFHrFrxr1OSY2iZdVnZTjos+INEjbWoKjRHcyLK25RlXjKyGs11ohj6n9QPz9mtsg7ZgM/GwzwY8pu6eJeKKPLxjIZMvqDw+J+ZPEms0hXhWaNBssPu80gLLuWXKmn4VGUFh/beVbCY3zGzhn/tMuiAe8CiuMiilr5K6SZHsNV+UtSlj4zz7utuGjWsgJCLXK/kqEHyDwkQrPQHMzKVivB/qfMS9M7oi4qYWNSm6IPaTne4FlU3zOHYYWng6925xl3MsYe0gITnqTwBlJ0hXcdtGk1o2gtsGa3gV7EYXUJJ3jMyom7tD5p4xi74Ybhm24ZTrr98ozTBXG3KFZ7EuxtM89+RLplZyjBaTBrTHty4n6yDHfsGmS0RficNwIvOWn1Zn1up3eOCy3C8mhRLZOoQVBU/ZUdMaQ1a5zGfdznrcJ6dxNvxMOceqbleWdYnQwl5GqS5LozLJ5B7XDes5evMX103BNhF71J9rqbBl8gx3rJnDqANsuTVliur+dzCM0KGWqhJTsC13FBTOIpGg028CtuFKI4yHd4C/IpXGU38CBsUSrGlGfGWEKL3Occ4hdwQvY5GXpcibAH9Rg0BlLqBA6LJ5wtlOqL8rQ3Bh36FG0NRmCc5NjL3gLb7jTxi7ikNjoV9TNUYV9yomxcseAuPSCTAUtGg/38pjslryi98AnaQHPBODR6R+DVeg/70CH5AzNinDSr9FlcYjdJUv63zvtrMsKEvQ/+aDfxNmWOxty8vG6n6aNKr3wAV42IFlfvxXk4gg7TT5U22uAZZQ2hiPph/dYpp2IcMv3wAs6K9kA/H/es40OhEn3fqbGH8bKxOdTK07iHH1Gy4ixqg5XBAh9DPXKrUuRXlRKN2VW5UkuxHZ69NI5joor65FVSk7ie+X+YmyETbOW/QSnxQp35uNLNL6B18m59HWz07oWPnDL/GknxHm3ROOpkja0oxh/De2FEnxPX3bSQuJtuJ5chiIrGDIlQzR2QbdYC9QVa4XEly47hHroPjYFd986D+gjsx1njb04vf0Dpkp16O+z0dst/u3vkNjdDqZ2j6z2XeRQt8LeUEXXIqsoJd8qYtLL0lFlR31HKMuwU5HHFDxOBVnnLCbNtuCaqZET2eRdpUkvSTVZZJPRF9Skyz55FQ+xuq8aSoQV6AeWFX5kCVme6p54JEirwqOvnO60SfRONwPfrez1BeuQBdxQe0rtgyE3Q0+4Ab7AGwRMoy4NmydhrhuW5Op9fX8dvKXk1F5plB+w4fxrN0yWnHU5pRfV8vVePKNG6n+JGCfv5+2aOrdDH2AlzLX8XtcKQZ5pedRLiDN7Px5Ut/B0SFa+gipy0qmJSa5e3yC64aFn8HlQyvmunjYtoF/i1QfgdHpAvuz4gnmFG9Bne6VaZTir0IErQDk9NrPaOsT/hCttttsBhJW8Y5iDESZT2ehc4IxkYrPdpxp4XN8l+2al18DeUC+Jdc5Tfxmt5p55l99X/9LG5D+4js8ITSMmoZ4H/lGTrtzwEy2ZJnCMxXrAKxgdKUb6kN8GXUcV4xKnAc84gpUpGrg6OQi/KqC4qsw/rrtyhz4g3STM06gX1KumgwqrB1kBFNUMDfB+eZtutAdgU8MmHUdz4vDfKT1iRej6HRY93lCYDfrnGTcnf2xW6ZGbYWCgrn3Ez7Ciqya+EKqpfm4NCsLfeqw76upNSx7S8XBXKi786ZfEX3EzPBcrqTTQtb5Ac/9SN0kt1l19CFXhN8cE2q10mvaNyhiTkH7TN8oRZZX9WhqELzRiNnhmokKwa1dbyLwaDdI2Toj8nBfE8mlI/URbESbOddpE0vW1X1R/ae2DccxhmlHnjMTICS2iQ38H9/DWrCQw9x66Zs7TTauGXcB+ccEfVZCAul2w//x65TF8MDvD1TpHfdmqwQSvR/wMYgQsU'))))                          # 512 variants drawn once, uniformly, from the 245,760 selected ones (advice for the replica)
C7SET = frozenset(c[0] for c in CLASSES)
def variant_ok(a0): return in_G(a0) and c7of(a0) in C7SET
def step_row(A, E, W, i):
    E[i] = (A[i-4] + E[i-4] + S1(E[i-1]) + CH(E[i-1], E[i-2], E[i-3]) + K[i] + W[i]) & M
    A[i] = (E[i] - A[i-4] + S0(A[i-1]) + MAJ(A[i-1], A[i-2], A[i-3])) & M
DWT = [(_ty[2][i] - _tx[2][i]) & M for i in range(NR)]           # published modular differences of the words (member y minus member x)
def rebuild(Wx, a0, w8):
    """A tail success -> a real semi-free-start pair: W7..W0 by the inverse expansion (member x words W16..W23 and W8..W15), CV1 by
    inverting steps 7..0 of the variant a0.  Returns (cv, mx, my) iff the pair passes every check (equal outputs, m != m', Step 2 returns the
    words, rows -4..21 of the accepted event except the W7 XOR cell, W7 in F7)."""
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
    if mx == my or compress(cv, mx) != compress(cv, my) or not inF7(mx[7]): return None
    wx, wy = words_from_cv(cv, a0)
    if wx != mx[:14] or wy != my[:14]: return None
    tx, ty = trace(cv, mx), trace(cv, my)
    if not all(rowok(tx, ty, i) for i in range(22)): return None
    return cv, mx, my
NP_R, CH_R, NT_R = 64, (32, 8, 2, 2, 2), 384
SIG = [(int(a, 16), int(b)) for a, b in (x.split(':') for x in '3ff:63 177:14 357:9 377:7 367:7 167:7 1f7:5 3c7:5 347:5 3e5:4 3ed:4 1d7:4 3d7:4 1c7:3 157:3 3e7:3 3f7:3 147:2 355:2 345:2 3c5:2 1e7:1 3d5:1 3f5:1 365:1 375:1 165:1'.split())]
def smc_replicate(rng):
    """One replicate of the sequential Monte-Carlo estimate of q3: row 16 exact (the 32 words), rows 17..21 by proposals with the E cell and
    '+' bits imposed (row 19: one of the four patterns, weight 4 x 2^-f; row 20: bit 29 = E19[29]), tail: W23 drawn in one of the
    classes SIG of its ten printed conditions with probability (n + 2)/218, uniform inside it (weight 218 2^-10 / (n + 2)), W7 in F7, W6 uniform, a
    variant's W8, rows 22..37 computed and the exact event tested.  Every success is rebuilt
    and run through the counted program step3b, which must accept it.  Returns (log2 estimate or None, verified pairs, failed checks,
    successes, stage logs, successes with an E19 pattern other than the published one)."""
    lg = [-27.0]; P = []
    for _ in range(NP_R):
        e16 = R16W[rng.below(32)]
        Ax = {i: _tx[0][i] for i in range(-4, 16)}; Ex = {i: _tx[1][i] for i in range(-4, 16)}; Wx = {i: PMX[i] for i in range(16)}
        Ay = {i: _ty[0][i] for i in range(-4, 16)}; Ey = {i: _ty[1][i] for i in range(-4, 16)}; Wy = {i: PMY[i] for i in range(16)}
        Wx[16] = (e16 - (Ax[12] + Ex[12] + S1(Ex[15]) + CH(Ex[15], Ex[14], Ex[13]) + K[16])) & M
        Wy[16] = (Wx[16] + ((s1(PMY[14]) + PMY[9] - s1(PMX[14]) - PMX[9]) & M)) & M
        for (A, E, W) in ((Ax, Ex, Wx), (Ay, Ey, Wy)): step_row(A, E, W, 16)
        P.append((Ax, Ex, Wx, Ay, Ey, Wy))
    for i in range(17, 22):
        cm, cvv = CELLS[1][i][:2]; pq = PQ[i]; imp = cm | pq; f = bin(imp).count('1') - 2 * (i == 19); Mi = CH_R[i - 17]; surv = []
        for (Ax, Ex, Wx, Ay, Ey, Wy) in P:
            rx = (Ax[i-4] + Ex[i-4] + S1(Ex[i-1]) + CH(Ex[i-1], Ex[i-2], Ex[i-3]) + K[i]) & M
            fixed = cvv | (Ex[i-1] & pq & ~cm & M)
            if i == 20: fixed = (fixed & ~B29) | (Ex[19] & B29)
            for _ in range(Mi):
                e = (rng.u32() & ~imp & M) | (fixed if i != 19 else (fixed & ~M19) | P19[rng.below(4)])
                Wxi = (e - rx) & M; Wyi = (Wxi + DWT[i]) & M
                nA = {**Ax}; nE = {**Ex}; nW = {**Wx}; mA = {**Ay}; mE = {**Ey}; mW = {**Wy}
                nW[i] = Wxi; mW[i] = Wyi; step_row(nA, nE, nW, i); step_row(mA, mE, mW, i)
                if nE[i] == e and rowok((nA, nE, nW), (mA, mE, mW), i): surv.append((nA, nE, nW, mA, mE, mW))
        if not surv: return None, [], 0, 0, lg, 0
        lg.append(math.log2(len(surv) / (len(P) * Mi)) - f)
        P = [surv[rng.below(len(surv))] for _ in range(NP_R)]
    cm, cvv = CELLS[2][23][:2]; imposed = cm; plan = []
    for (k1, i1, b1, eq, k2, i2, b2, row) in X2:
        if row != 23: continue
        if not (imposed >> b2) & 1: plan.append((b1, b2, 0 if eq else 1)); imposed |= 1 << b2
        elif not (imposed >> b1) & 1: plan.append((b2, b1, 0 if eq else 1)); imposed |= 1 << b1
        else: raise ValueError('over-determined row-23 condition')
    tailw = 2.0 ** 22 / 287309824; cb = [b for b in range(32) if cm >> b & 1]; ns = sum(n + 2 for _, n in SIG); ws = 0.0
    pairs = []; bad = 0; succ = 0; alt = 0
    for (Ax, Ex, Wx, Ay, Ey, Wy) in P:
        for _ in range(NT_R):
            a0 = VARIANTS[rng.below(len(VARIANTS))]; w8 = (W8C - (a0 + C4)) & M
            r = rng.below(ns)
            for sg_, n in SIG:
                r -= n + 2
                if r < 0: break
            w23 = rng.u32()
            for t, b in enumerate(cb): w23 = w23 & ~(1 << b) | ((cvv >> b ^ ~sg_ >> t) & 1) << b
            for t, (bs_, bd, fl) in enumerate(plan): w23 = w23 & ~(1 << bd) | ((w23 >> bs_ ^ fl ^ ~sg_ >> (6 + t)) & 1) << bd
            w7 = (w23 - s1(Wx[21]) - Wx[16] - s0(w8)) & M
            if not inF7(w7): continue
            w6 = rng.u32()
            nA = {**Ax}; nE = {**Ex}; nW = {**Wx}; mA = {**Ay}; mE = {**Ey}; mW = {**Wy}
            for i, v in ((7, w7), (8, w8)): nW[i] = v; mW[i] = (v + DWT[i]) & M
            nW[6] = w6; mW[6] = w6
            for i in range(22, NR):
                nW[i] = (s1(nW[i-2]) + nW[i-7] + s0(nW[i-15]) + nW[i-16]) & M
                mW[i] = (s1(mW[i-2]) + mW[i-7] + s0(mW[i-15]) + mW[i-16]) & M
                step_row(nA, nE, nW, i); step_row(mA, mE, mW, i)
            if exact((nA, nE), (mA, mE)):
                succ += 1; ws += ns / (n + 2); r = rebuild(nW, a0, w8); alt += (nE[19] & M19) != 0x30040430
                if r and step3b(Mach(), r[0], fb_scalars(Mach(), r[0]), a0): pairs.append(r)
                else: bad += 1
    if succ == 0: return None, pairs, bad, 0, lg, alt
    lg.append(math.log2(ws * tailw / (NP_R * NT_R)))
    return sum(lg), pairs, bad, succ, lg, alt

def pair_check15(cv, a0):
    """Reference check of a good pair: the Step-2 words of (cv, a0) give a trace that follows every cell of rows -4..15 (the W7 XOR cell
    excepted) and every printed two-bit condition of rows 8..15; W7 is in F7."""
    wx, wy = words_from_cv(cv, a0)
    mx = wx + [PMX[14], PMX[15]]; my = wy + [PMY[14], PMY[15]]
    tx, ty = trace(cv, mx, 16), trace(cv, my, 16)
    if not inF7(mx[7]): return False
    if not all(rowok(tx, ty, i) for i in range(-4, 16)): return False
    for (k1, i1, b1, eq, k2, i2, b2, row) in X2:
        if 8 <= row < 16 and (((tx[k1][i1] >> b1) ^ (tx[k2][i2] >> b2)) & 1) != (0 if eq else 1): return False
    return True
def online_experiment(req):
    out = []
    for tr in req['trials']:
        t = tr['trial']; rec = dict(trial=t, message_a_hex=None, message_b_hex=None)
        if t < 6:
            rng = Shake(req['experiment_id'] + '|' + tr['seed']); m = Mach(rng.word); st = Stats(); fm = 0; ncell = 0; cm = 0; nfb = 0; hits = []
            while nfb < 16 and not hits:
                nfb += 1; cv, hits, M0 = process_fb(m, st, True, True)
                ref = [ci for ci, c in enumerate(CLASSES) if inF7((c[0] - cv[0]) & M)]
                fm += int(ref != hits)
            if hits:
                cd = classdata(hits[0])
                for a0 in cd.members[::480]:
                    ncell += 1; cm += int(not pair_check15(cv, a0))
                a0 = cd.members[0]; wx, wy = words_from_cv(cv, a0)
            rec['observations'] = dict(first_blocks=st.fb, w7_classes=len(hits), classes_processed=st.classes, good_pairs=st.good, prefilter_passes=st.pre,
                                       row16_passes=st.r16, counted_ops=m.ops, units=m.units, filter_mismatches=fm, cell_mismatches=cm,
                                       lane_mismatches=st.lane_mism, pairs_cell_checked=ncell)
            if hits and fm == 0 and cm == 0 and st.lane_mism == 0:
                rec['message_a_hex'] = struct.pack('>32I', *(M0 + wx + [PMX[14], PMX[15]])).hex()
                rec['message_b_hex'] = struct.pack('>32I', *(M0 + wy + [PMY[14], PMY[15]])).hex()
        out.append(rec)
    return dict(schema_version=1, trials=out)
Q3_THRESH = -98.4338                          # log2 threshold of the pooled mean (frozen before the calibration, Section 7.3)
def q3_experiment(req):
    out = []; est = []; bad_total = 0; last = None
    for tr in req['trials']:
        t = tr['trial']; rec = dict(trial=t, message_a_hex=None, message_b_hex=None)
        if t < 20:
            rng = Shake(req['experiment_id'] + '|' + tr['seed']); z, pairs, bad, succ, lg, alt = smc_replicate(rng)
            rec['observations'] = dict(log2_estimate=z if z is not None else 0.0, estimate_zero=int(z is None), successes=succ, failed_rebuilds=bad, other_pattern_successes=alt,
                                       verified_pairs=len(pairs), tail_log2=lg[-1] if z is not None else 0.0)
            est.append(0.0 if z is None else 2.0 ** z); bad_total += bad
            if pairs:
                cv, mx, my = pairs[0]; last = pairs[-1]
                rec['message_a_hex'] = struct.pack('>24I', *(cv + mx)).hex(); rec['message_b_hex'] = struct.pack('>24I', *(cv + my)).hex()
        elif t == 20 and len(est) == 20:
            mean = sum(est) / 20; lz = math.log2(mean) if mean > 0 else -1000.0
            rec['observations'] = dict(log2_pooled_mean=lz, pooled_zero=int(mean == 0), replicates=20, failed_rebuilds=bad_total, pass_threshold_log2=Q3_THRESH)
            if lz >= Q3_THRESH and bad_total == 0 and last:
                cv, mx, my = last
                rec['message_a_hex'] = struct.pack('>24I', *(cv + mx)).hex(); rec['message_b_hex'] = struct.pack('>24I', *(cv + my)).hex()
        out.append(rec)
    return dict(schema_version=1, trials=out)
def run_request(req):
    return online_experiment(req) if 'online' in req['experiment_id'] else q3_experiment(req)

# ---------------------------------------------------------------- (6) selftest, calibrate (every counted constant), ledger
HIT0 = 2992758256           # number of values of A_{-1} (of 2^32) for which none of the 90 classes passes F7 (exhaustive pass, Appendix A.2)
def lane_cost(ci, ell):
    """Operations of one stage-3a lane from the isolated lowest lane to the end of its row-16 test (lane k = ell of batch 0)."""
    cd = classdata(ci); m = Mach()
    for j in range(32):
        if (cd.mask >> j) & 1: m.mem[('plane', ci, 0, j)] = cd.batches[0]['P:A%d' % j]
    fb = fb_scalars(Mach(), PCV); fb['planes'] = {}
    ok = 1 << ell; k0 = m.ops
    e = first_lane(m, ok); a0 = lane_value(m, cd, 0, e); assert e == ell and a0 == cd.members[ell]
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
    m = Mach(); r = step3b(m, PCV, fb, 0xb75dae71); assert r is not None; cal['step3b'] = m.ops + 1
    rr = Shake('cal'); m = Mach(rr.word); r0 = m.rand(); r1 = m.rand(); M0 = unpack16(m, r0, r1); m.ops += 3; m.br(); cal['fixed'] = m.ops
    cal['prog'] = {g: len(program(g)[0]) for g in sorted(set(GRP))}
    cal['classes_of'] = {g: GRP.count(g) for g in cal['prog']}
    if full:
        cal['w7'] = w7_distribution()
        cal['lane_max'] = {mk: max(lane_cost(next(i for i, c in enumerate(CLASSES) if c[2] == mk), ell) for ell in range(256)) for mk in sorted({c[2] for c in CLASSES})}
    return cal
def ledger(cal=None, tx=None, show=True, q3_log2='-97.7838', h3_log2='-9.5', eps_log2=16, succ='0.39', A_C=2**78, A_S=2**74, DEV=2**70):
    from decimal import Decimal, getcontext
    getcontext().prec = 80
    cal = cal or calibrate()
    C = 2728; p7 = Fraction(287309824, 2**32); K = len(CLASSES); g = K * 3840 * p7; assert g == Fraction(92475, 4)
    ntb = len(TBITS); two = Decimal(2)
    pany = Fraction(2**32 - HIT0, 2**32); khit = K * p7
    w7 = (sum(c * p for (c, ok), p in cal['w7'].items()) + 4) * K
    cls = sum(p7 * (7 + 15 * (cal['prog'][h] + 6)) for h in GRP)
    lanes = sum(p7 * 3840 * Fraction(1, 2**ntb) * cal['lane_max'][c[2]] for c in CLASSES)
    r16 = g * Fraction(32, 2**32) * cal['step3b']
    vbar = w7 + 2 * khit + pany * (cal['fb_scalars'] + cal['planes']) + cls + lanes + r16
    class_max = max(7 + 15 * (cal['prog'][h] + 6) + 3840 * (cal['lane_max'][c[2]] + cal['step3b']) for c, h in zip(CLASSES, GRP))
    wmax = max(c for c, ok in cal['w7']); P0 = K * (wmax + 2 + 4) + cal['fb_scalars'] + cal['planes']
    vmax_f = P0 + K * class_max
    F = cal['fixed']; PRE = sum(v for _, v in pre_terms()); FIN = 1600
    q3 = two ** Decimal(q3_log2); h3 = 1 - two ** Decimal(h3_log2); eps = Fraction(1, 2**eps_log2)
    need = Decimal(1) - Decimal(succ) - two ** -60
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
            ('precomputation (member tests, batch planes, program generation)', PRE), ('final verification (6 compressions and 1600 operations)', 6 * C + FIN)]
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
        cal = calibrate(); print(json.dumps({k: (v if not isinstance(v, dict) else {str(a): str(b) for a, b in v.items()}) for k, v in cal.items()}, indent=1))
    elif len(sys.argv) > 1 and sys.argv[1] == 'selftest':
        selftest()
    else:
        sys.stdout.write(json.dumps(run_request(json.load(sys.stdin))))
def row16_full(e):
    """Every cell of row 16 of both members and every two-bit condition closing at row 16, as a function of E16x (rows 12..15 are those of S)."""
    A, E = _tx[0], _tx[1]; Ay, Ey = _ty[0], _ty[1]
    w16x = (e - (A[12] + E[12] + S1(E[15]) + CH(E[15], E[14], E[13]) + K[16])) & M
    w16y = (w16x + ((s1(PMY[14]) + PMY[9] - s1(PMX[14]) - PMX[9]) & M)) & M
    tr = []
    for (a, ee, w) in ((A, E, w16x), (Ay, Ey, w16y)):
        e16_ = (a[12] + ee[12] + S1(ee[15]) + CH(ee[15], ee[14], ee[13]) + K[16] + w) & M
        tr.append(((e16_ - a[12] + S0(a[15]) + MAJ(a[15], a[14], a[13])) & M, e16_, w))
    X = {0: {**{i: A[i] for i in range(-4, 16)}, 16: tr[0][0]}, 1: {**{i: E[i] for i in range(-4, 16)}, 16: tr[0][1]}, 2: {**{i: PMX[i] for i in range(16)}, 16: tr[0][2]}}
    for k in range(3):
        m, v, d = CELLS[k][16][:3]
        if (tr[0][k] & m) != v or (tr[0][k] ^ tr[1][k]) != d: return False
    if (tr[0][1] ^ E[15]) & PQ[16]: return False
    return all((((X[k1][i1] >> b1) ^ (X[k2][i2] >> b2)) & 1) == (0 if eq else 1) for (k1, i1, b1, eq, k2, i2, b2, row) in X2 if row == 16)
def selftest():
    ok = lambda s: print('ok  ' + s)
    assert compress(PCV, PMX) == compress(PCV, PMY) and compress(PCV, PMX)[0] == 0x5d9ca5f4
    assert all(rowok(_tx, _ty, i) for i in range(-4, NR)) and all(cellok(1, i, _tx[1][i], _ty[1][i]) for i in range(NR)); ok('published pair: equal 38-step outputs (hash 5d9ca5f4 ...), every printed cell and condition of rows -4..37')
    assert in_G(0xb75dae71) and c7of(0xb75dae71) == 0x8f6c89c5 and words_from_cv(PCV, 0xb75dae71)[0] == PMX[:14]; ok('published A0 is in G, c7 = 8f6c89c5, Step 2 returns the published words')
    cs = set()
    for ci, (c7, base, mask) in enumerate(CLASSES):
        mem = class_members(c7, base, mask); assert len(mem) == 3840 and all(c7of(a) == c7 for a in mem); cs.add(c7)
    assert len(cs) == 90 and len(set(GRP)) == 7; ok('90 classes of 3840 members in 7 plane programs, distinct c7 values, masks %s' % sorted({hex(c[2]) for c in CLASSES}))
    assert all(r16ok(w) and row16_full(w) for w in R16W); rr = random.Random(5)
    nb = 0
    for _ in range(3000):
        e = (EV | (rr.getrandbits(32) & ~EM)) & M
        assert row16_full(e) == r16ok(e); nb += r16ok(e)
    for w in R16W:
        for _ in range(40):
            e = w ^ (1 << rr.randrange(32)) ^ (1 << rr.randrange(32)); assert row16_full(e) == r16ok(e)
    ok('row-16 set: 32 words pass the full row-16 test; 3000 random words with the ten cell bits and 1280 two-bit neighbours of the members agree with the affine description')
    for _ in range(300):
        cv_ = [rr.getrandbits(32) for _ in range(8)]; a_ = rr.choice(VARIANTS)
        assert e16x(cv_, a_) == e16x_ref(cv_, a_)
    assert all(((w ^ TVAL) >> j) & 1 == 0 for w in R16W for j in TBITS); ok('the %d prefilter bits are shared by all 32 words' % len(TBITS))
    for _ in range(4000):
        w = rr.getrandbits(32)
        for t_ in (0, 1):
            if t_: w = (w & ~(1 << 14 | 1 << 8 | 2)) | (((w >> 18) & 1 ^ 1) << 14) | (((w >> 25) & 1 ^ 1) << 8) | (((w >> 12) & 1) << 1)
            assert w7test(Mach(), w, 0) == inF7(w)
    ok('W7 decision tree agrees with the definition of F7 on 8000 words')
    m = Mach(); fb = fb_scalars(m, PCV); r = step3b(m, PCV, fb, 0xb75dae71); assert r is not None
    A, E, W = trace(PCV, PMX); assert all(r[0][0][i] == A[i] and r[0][1][i] == E[i] and r[0][2][i] == W[i] for i in range(NR))
    ok('step 3b on the published pair: all rows pass, exact event, traces equal the reference (%d operations)' % m.ops)
    acc = []; bits = [b for b in range(32) if M19 >> b & 1]
    for v in range(512):
        X = [dict(d) for d in r[0]]; Y = [dict(d) for d in r[1]]; p = sum((v >> j & 1) << b for j, b in enumerate(bits))
        X[1][19] = X[1][19] & ~M19 | p; Y[1][19] = X[1][19] ^ _tx[1][19] ^ _ty[1][19]
        c = row_check(Mach(), 19, X, Y); assert c == ecell(19, X[1], Y[1]); acc += [p] * c
    for v in range(4):
        X = [dict(d) for d in r[0]]; Y = [dict(d) for d in r[1]]; X[1][19] ^= (v & 1) * B29; X[1][20] ^= (v >> 1) * B29; Y[1][20] ^= (v >> 1) * B29
        assert row_check(Mach(), 20, X, Y) == ecell(20, X[1], Y[1]) == (v in (0, 3))
    assert sorted(acc) == sorted(P19)
    ok('counted rows 19 and 20 equal the definition: row 19 accepts exactly the patterns %s of 512, row 20 exactly when E20[29] = E19[29]' % [hex(p) for p in sorted(acc)])
    for g in sorted(set(GRP)):
        ci = GRP.index(g); cd = classdata(ci); ins, res, sh = program(g); bad = 0
        for t in range(3):
            cv = [rr.getrandbits(32) for _ in range(8)]; fm = Mach(); f2 = fb_scalars(fm, cv); inp = {}
            for nm in ('HH', 'PP', 'QQ', 'EF', 'FF', 'K1', 'KP'):
                for j in range(32): inp['%s%d' % (nm, j)] = ONES if (f2[nm] >> j) & 1 else 0
            okp = run_prog(ins, inp, {**cd.batches[t], **cd.cw})[res]
            bad += sum(pre_ok(cv, cd.members[256 * t + k]) != bool((okp >> k) & 1) for k in range(256))
        assert bad == 0
    ok('bit-sliced prefilter equals the scalar definition on 768 lanes of each of the 7 plane programs (%s instructions)' % [len(program(g)[0]) for g in sorted(set(GRP))])
    st = Stats(); rng = Shake('selftest'); mm = Mach(rng.word); nf = 0
    while not st.classes and nf < 40: nf += 1; process_fb(mm, st, True, True)
    assert st.classes == 1 and st.lane_mism == 0; ok('online program: first block %d, one class of 3840 good pairs, %d lane mismatches' % (nf, st.lane_mism))
    zs = smc_replicate(Shake('selftest-q3')); assert zs[2] == 0; ok('q3 replicate: estimate 2^%.2f, %d verified 38-step semi-free-start collisions accepted by step3b, %d failed checks, %d with another E19 pattern' % (zs[0] if zs[0] else 0, len(zs[1]), zs[2], zs[5]))
    st = Stats(); mm = Mach(Shake('cap').word); process_fb(mm, st, True, True, 1000); o = mm.ops; st.halt = 0; process_fb(mm, st, True, True, 1000)
    assert st.halt and mm.ops - o <= 35; ok('cap test on every block: V > V_MAX halts at the next block start, before its 90 W7 tests')
    assert all(variant_ok(a) for a in VARIANTS) and len(set(VARIANTS)) == 512; ok('512 embedded variants are in G and in the selected classes')
    pk, (on, pr, ad), _ = peak_memory(calibrate()); assert pk < 2 ** 20
    ok('memory: online %d, precomputation %d, advice %d; peak %d = 2^%.6f < 2^20' % (on, pr, ad, pk, math.log2(pk)))

def member_test(m, a):
    """Counted test of one candidate a0 = base ^ s: a0 in G (W8's cell and its three two-bit conditions) and its c7 (the longest path is charged)."""
    e4 = m.and_(m.add(a, C4), M); w = m.and_(m.sub(W8C, e4), M); y = m.and_(m.add(w, D8), M)
    cm_, cv_, cd_ = CELLS[2][8][:3]
    t = m.and_(w, cm_); m.br()
    if t != cv_: return None
    t = m.xor(w, y); m.br()
    if t != cd_: return None
    for (b1, b2, eq) in ((0, 28, 0), (30, 9, 0), (1, 18, 1)):
        v = m.and_(m.xor(m.shr(w, b1), m.shr(w, b2)), 1); m.br()
        if v != (0 if eq else 1): return None
    mj = m.or_(m.and_(a, SAx[2] | SAx[1]), SAx[2] & SAx[1])
    ch = m.xor(m.and_(e4, ~SE[6] & M), SE[6] & SE[5])
    c7 = m.and_(m.sub(m.add((SE[7] - 2 * SAx[3] + S0(SAx[2]) - S1(SE[6]) - K[7]) & M, mj), ch), M)
    return c7
def memory(cal, spill=15):
    """Bytes of the program's memory: batch planes, class constants, broadcast planes, the spill slots the allocator actually uses,
    scalars, class table, and code at 32 bytes (one word) per instruction."""
    K = len(CLASSES); planes = sum(15 * bin(c[2]).count('1') * 32 for c in CLASSES)
    shared = sum(bin(shape_of(h)[0]).count('1') * 32 for h in GRP)
    ninstr = sum(cal['prog'].values()); nw7 = 52 + 5; nother = 600
    parts = [('batch planes of the %d classes (15 batches, one word per variable bit of a0)' % K, planes), ('shared-constant words of the classes', shared),
             ('per-first-block broadcast planes (7 x 32 words)', 7 * 32 * 32), ('spill slots of the plane programs (%d used)' % spill, spill * 32),
             ('scalars, counters, hit list and F7 constants (64 words)', 64 * 32), ('class table (c7, base, mask: 3 words each)', K * 3 * 32),
             ('code of the %d plane programs: %d instructions at 32 bytes' % (len(cal['prog']), ninstr), ninstr * 32),
             ('code of the W7 test loop: %d instructions at 32 bytes (the 52-instruction tree once, 5 for the loop)' % nw7, nw7 * 32),
             ('code of the other routines (first-block words, scalars, planes, lane scan, row 16, step 3b, loops): %d instructions at 32 bytes' % nother, nother * 32)]
    return parts, sum(v for _, v in parts)
def peak_memory(cal):
    """Peak = max(online, one class of precomputation, stored advice); the H4 searches are time charges (A_C, A_S, DEV), not resident data."""
    parts, online = memory(cal); pre = 3840 * 4 + max(15 * bin(c[2]).count('1') * 32 for c in CLASSES) + 256; advice = 2104
    return max(online, pre, advice), (online, pre, advice), parts
def pre_terms():
    """Preprocessing as counted code: member lists of the 64 classes (every subset of the mask is tested), the batch planes (4 operations per
    member and variable bit), program generation (charged 2^32 operations)."""
    worst = 0
    for a in (0xb75dae71,):
        m = Mach(); member_test(m, a); worst = max(worst, m.ops)
    cands = sum(2 ** bin(c[2]).count('1') for c in CLASSES)
    return [('member tests: %d candidates x %d operations (longest path)' % (cands, worst), cands * worst),
            ('batch planes: %d member-bits x 4 operations' % sum(3840 * bin(c[2]).count('1') for c in CLASSES), 4 * sum(3840 * bin(c[2]).count('1') for c in CLASSES)),
            ('program generation (charged in full)', 2 ** 32)]
if __name__ == '__main__': main()
