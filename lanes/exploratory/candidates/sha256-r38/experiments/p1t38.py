# p1t38.py - sha256-r38: the P8 two-block procedure with the P1 sum-claw on a 2^27-candidate a0 set (own code, standard library only).
# Derivative, credited (proof.md, introduction): the P1 sum-claw, its post-filter chain, step 3b, the counted pricing and q3_model are
# Jbenisek's (e4243e7a); the 2^32-word scan is newjordan's (711c4bf8); the measured online memory cell follows 0xplemonade's a32131ff and the
# capped Step-1 cell is 377cb363's; the characteristic P8, its semi-free-start pair S and its accepted event are ours (1a695f0b), the event
# as transcribed in e4243e7a (E18 = E17 not imposed).  New here: the table loads 2^27 candidates a0 from the set P (the best class of the
# exact C1 C2 G count) into the 2^26 slots with 5-bit residues, a residue pass recomputes F(a0); the group bound of Lemma 5 with the
# measured full-scan link rate; our own exact counts, our own paired q3 measurement on P, our own code throughout.  No program of another
# participant is executed; the event cells below are data (P8's printed cells, rows 7..22, and its two-bit conditions).
# Sections: (1) reference; (2) the P1 pair, S160, P; (3) event and step 3b; (4) counted machine; (5) one chaining value; (6) ledger;
# (7) organizer experiments; (8) selftest, main.
import sys, json, hashlib, struct, bisect
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
    """A[i], E[i] (i = -4..n-1, dicts) and W[0..n-1] of the first n steps from the chaining value cv."""
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

GL = [549441552, 549441553, 549441556, 549441557, 549442576, 549442577, 549442580, 549442581, 1891627024, 1891627025, 1891627028, 1891627029, 1891628048, 1891628049, 1891628052, 1891628053, 2698498064, 2698498065, 2698498068, 2698498069, 2698499088, 2698499089, 2698499092, 2698499093, 2699022352, 2699022353, 2699022356, 2699022357, 2699023376, 2699023377, 2699023380, 2699023381, 2700595216, 2700595217, 2700595220, 2700595221, 2700596240, 2700596241, 2700596244, 2700596245, 3988787216, 3988787217, 3988787220, 3988787221, 3988788240, 3988788241, 3988788244, 3988788245, 3989303312, 3989303313, 3989303316, 3989303317, 3989304336, 3989304337, 3989304340, 3989304341, 3989311504, 3989311505, 3989311508, 3989311509, 3989312528, 3989312529, 3989312532, 3989312533, 3989827600, 3989827601, 3989827604, 3989827605, 3989828624, 3989828625, 3989828628, 3989828629, 3990884368, 3990884369, 3990884372, 3990884373, 3990885392, 3990885393, 3990885396, 3990885397, 3991400464, 3991400465, 3991400468, 3991400469, 3991401488, 3991401489, 3991401492, 3991401493, 3991408656, 3991408657, 3991408660, 3991408661, 3991409680, 3991409681, 3991409684, 3991409685, 3991924752, 3991924753, 3991924756, 3991924757, 3991925776, 3991925777, 3991925780, 3991925781, 4040167440, 4040167441, 4040167444, 4040167445, 4040168464, 4040168465, 4040168468, 4040168469, 4040683536, 4040683537, 4040683540, 4040683541, 4040684560, 4040684561, 4040684564, 4040684565, 4040691728, 4040691729, 4040691732, 4040691733, 4040692752, 4040692753, 4040692756, 4040692757, 4041207824, 4041207825, 4041207828, 4041207829, 4041208848, 4041208849, 4041208852, 4041208853, 4042264592, 4042264593, 4042264596, 4042264597, 4042265616, 4042265617, 4042265620, 4042265621, 4042780688, 4042780689, 4042780692, 4042780693, 4042781712, 4042781713, 4042781716, 4042781717, 4042788880, 4042788881, 4042788884, 4042788885, 4042789904, 4042789905, 4042789908, 4042789909]
PCV = [2510440793, 3020242837, 468731710, 514538364, 1695310803, 3863559483, 3976220445, 3950947027]
PMX = [3171188373, 499730577, 1270760843, 3353099274, 2338469345, 2641768686, 1453171616, 2497556930, 1179538525, 2818885938, 2901196405, 3358065010, 2588764008, 370382130, 3758975641, 1605534331]
PMY = [3171188373, 499730577, 1270760843, 3353099274, 2338469345, 2641768686, 1453171616, 3034427842, 1108237405, 2282015026, 2850925791, 3357543794, 2588764008, 370382130, 3758975641, 1542621819]

# ---- P8's printed cells, rows 7..22 (A, E, W of member x): u/n the signed difference, 0/1 a fixed value, '+' equal to the same bit one row
# up (data, as printed in the proof of 1a695f0b and transcribed in e4243e7a); the '+' pair E18 = E17 is not part of the accepted event.
_ROWS = ("=nu============================= uuu============================= ==n=============================|"
 "=========n=====n====n======n==== ==n=u====n==nu=====nu===u==n==== =====u===u==========n===========|"
 "================================ ======nn===n================n=nn ==u=============================|"
 "===============n===========u==== =u=============n===========u==== =====u=n=======n===u==u=n=u=n=n=|"
 "====n===============n========u== ==n==n==u=====un================ ============u=======nn==========|"
 "==u====u==u==========uu=======u= =nu=u==n==n=====u=n=nn=========u ================================|"
 "==n============================= =========n============n=nuu==uu= ================================|"
 "====n=========n=========n==n==== ====u=========n================= ================================|"
 "======n=u======un=============== ====================n===u======= =====u===n==========n===========|"
 "================================ =u==1====n===+u====u0=u=0==+==== ==u=============================|"
 "==u============================= =0=====++0===+0=+==01=0=0==+==== ================================|"
 "================================ =0=====++1===n1=+==1==1====n==== ================================|"
 "================================ ==+====nn=======u=============== ================================|"
 "================================ ==+====00====1==0==========1==== ================================|"
 "================================ ==u====10=======1=============== ================================|"
 "================================ ==0============================= ================================").split('|')
CELLS = [[(0, 0, 0)] * NR for _ in range(3)]; PQ = [0] * NR; _PL = {}
for _r, _l in enumerate(_ROWS):
    for _k, _s in enumerate(_l.split()):
        m_ = v_ = x_ = p_ = 0
        for _j, _c in enumerate(_s):
            b_ = 1 << (31 - _j); m_ |= b_ * (_c in 'un01'); v_ |= b_ * (_c in 'u1'); x_ |= b_ * (_c in 'un'); p_ |= b_ * (_c == '+')
        CELLS[_k][_r + 7] = (m_, v_, x_); _PL[_r + 7] = _PL.get(_r + 7, 0) | p_
for _i in _PL: PQ[_i] = _PL[_i] & _PL.get(_i - 1, 0)
PQE = list(PQ); PQE[18] = 0
for _i in (7, 8): CELLS[2][_i] = (0, 0, 0)      # W7, W8: only their modular and s0 differences matter (F7, C1, G); not tested by step 3b
# two-bit conditions of rows 16..21: (kind1, row1, bit1, equal, kind2, row2, bit2, closing row), member x
X2 = []
for _t in ('E16 7 = E16 26,E16 14 ! E16 28,A15 4 = A16 4,E16 11 = E16 16,A15 7 = A16 7,A14 15 = A16 15,A14 16 = A16 16,A15 17 = A16 17,'
           'A14 23 = A16 23,A14 25 = A16 25,A15 27 = A16 27,E16 3 ! E16 8,E16 4 = E16 23,W16 20 ! W16 27,W16 22 = W16 31,W16 4 ! W16 6,'
           'A15 29 = A16 29,W16 14 = W16 18,W16 8 = W16 25,W16 1 ! W16 12,A17 9 ! A17 20,A16 15 = A17 15,A17 6 = A17 18,A16 16 ! A17 16,'
           'A16 23 = A17 23,A16 25 = A17 25,A17 8 ! A17 17,E18 0 = E18 13,E18 17 = E18 22,E18 5 ! E18 23,A16 29 = A18 29,E18 9 = E18 23,'
           'E21 10 = E21 15,E21 11 = E21 24,E21 2 = E21 16').split(','):
    _a, _b, _e, _c, _d = _t.split()
    X2.append(('AEW'.index(_a[0]), int(_a[1:]), int(_b), int(_e == '='), 'AEW'.index(_c[0]), int(_c[1:]), int(_d), max(int(_a[1:]), int(_c[1:]))))

# ---------------------------------------------------------------------------------------------- (2) the P1 pair, S160, the a0 set P
_tx, _ty = trace(PCV, PMX), trace(PCV, PMY)
SA = [{i: t[0][i] for i in range(-4, 16)} for t in (_tx, _ty)]       # A rows of S, member x (0) and y (1)
SE = [{i: t[1][i] for i in range(-4, 16)} for t in (_tx, _ty)]       # E rows of S
SW = [PMX, PMY]
# the base words the claw keeps (A2..A15, E6..E15 of both members) and the differences of the words they fix
assert all(SA[0][i] == SA[1][i] for i in range(-4, 7)) and all(SE[0][i] == SE[1][i] for i in range(-4, 7))
D7 = (PMY[7] - PMX[7]) & M; D8 = (PMY[8] - PMX[8]) & M; D9 = (PMY[9] - PMX[9]) & M
T7 = (s0(PMY[7]) - s0(PMX[7])) & M; T8 = (s0(PMY[8]) - s0(PMX[8])) & M; T9 = (s0(PMY[9]) - s0(PMX[9])) & M
def inF7(w): return ((s0((w + D7) & M) - s0(w)) & M) == T7

def pair_words(cv, a0, a1):
    """W0..W15 of both members of the P1 pair: A0 = a0, A1 = a1, A2..A15 and E6..E15 of S, rows -4..-1 from cv (step equations)."""
    out = []
    for m in (0, 1):
        A = {-1: cv[0], -2: cv[1], -3: cv[2], -4: cv[3], 0: a0, 1: a1}; E = {-1: cv[4], -2: cv[5], -3: cv[6], -4: cv[7]}
        for i in range(2, 16): A[i] = SA[m][i]
        for i in range(6): E[i] = (A[i] + A[i-4] - S0(A[i-1]) - MAJ(A[i-1], A[i-2], A[i-3])) & M
        for i in range(6, 16): E[i] = SE[m][i]
        out.append([(E[i] - A[i-4] - E[i-4] - S1(E[i-1]) - CH(E[i-1], E[i-2], E[i-3]) - K[i]) & M for i in range(16)])
    return out

# Row 16.  W16 = s1(W14) + W9 + s0(W1) + W0 with W9 = c9 - E5, E5 = a1 + c5, W0 = a0 + k0(cv), W1 = a1 + h(a0, cv) (Lemma 1), so
# E16x = C16 + W16 = F(a0) + s0(u) - u with u = W1 and F(a0) = CC2 + a0 + k0 + h(a0); CC2 = C16 + s1(W14) + c9 - c5 depends on S only.
C5 = (SA[0][5] - S0(SA[0][4]) - MAJ(SA[0][4], SA[0][3], SA[0][2])) & M
C9 = (SE[0][9] - SA[0][5] - S1(SE[0][8]) - CH(SE[0][8], SE[0][7], SE[0][6]) - K[9]) & M
C16 = (SA[0][12] + SE[0][12] + S1(SE[0][15]) + CH(SE[0][15], SE[0][14], SE[0][13]) + K[16]) & M
CC2 = (C16 + s1(PMX[14]) + C9 - C5) & M
S160 = sorted((C16 + g) & M for g in GL)          # the E16x values that pass row 16 with all its conditions (exhaustive, 160 words)
R16F = 0x405                                       # the 160 words are 20 heads times the 8 values of bits 0, 2, 10
HEADS = sorted(set(e & ~R16F & M for e in S160))
OFFS = (0, 1, 4, 5, 1024, 1025, 1028, 1029)
assert len(HEADS) == 20 and sorted((h + o) & M for h in HEADS for o in OFFS) == S160

# The a0 set P: bits 25..27 = 010 and bits 30..31 = 00 (2^27 words; the four 2^25-windows k = 2, 10, 18, 26 of the best class of the exact
# C1 C2 G count, proof.md Section 6).  Offset o (27 bits) -> a0.
PBASE = 2 << 25
def p_a0(o): return (o & 0x1ffffff) | PBASE | ((o >> 25) << 28)
def p_off(a0): return (a0 & 0x1ffffff) | (((a0 >> 28) & 3) << 25)
def in_P(a0): return (a0 >> 25) & 7 == 2 and a0 >> 30 == 0

def cvc(cv):
    """the claw scalars of one chaining value: k0 (W0 = a0 + k0), E0 base, MAJ and CH helpers, KF (F = a0 + KF - S0 - MAJ - S1 - CH),
    K2 = CC2 + k0 (a1 = u - F + K2 + a0) and the F7 constant KK7 (W7x = KK7 + MAJ(A2, a1, a0) - CH(E6, E5, E4))."""
    a, b, c, d, e, f, g, h = cv
    k0 = (-S0(a) - MAJ(a, b, c) - h - S1(e) - CH(e, f, g) - K[0]) & M
    return dict(k0=k0, E0b=(d - S0(a) - MAJ(a, b, c)) & M, PP=a & b, QQ=a | b, EF=e ^ f, FF=f, KF=(CC2 + k0 - g - K[1]) & M,
                K2=(CC2 + k0) & M, KK7=(SE[0][7] - 2 * SA[0][3] - a + S0(SA[0][2]) - S1(SE[0][6]) - K[7]) & M)
def Ffun(c, a0):
    E0 = (a0 + c['E0b']) & M
    return (a0 + c['KF'] - S0(a0) - (c['PP'] | (a0 & c['QQ'])) - S1(E0) - (c['FF'] ^ (E0 & c['EF']))) & M
def hfun(c, a0): return (Ffun(c, a0) - CC2 - a0 - c['k0']) & M

# post-filter constants (member x; A2..A5 and E6 are equal in the two members)
CE4 = (SA[0][4] - S0(SA[0][3])) & M; MA = SA[0][3] & SA[0][2]; MB = SA[0][3] | SA[0][2]          # E4 = a0 + CE4 - MAJ(A3, A2, a1)
KW8 = (SE[0][8] - SA[0][4] - S1(SE[0][7]) - K[8]) & M; CA = SE[0][7] & SE[0][6]; CB = ~SE[0][7] & M  # W8x = KW8 - E4 - (CA ^ (CB & E5))
CW9 = (C9 - C5) & M                                                                                 # W9x = CW9 - a1
# C1: dW8 = D8 holds iff the CH(E7, E6, E5) difference has its one admissible value: a condition on E5's bits 29..31 (E7 differs there)
_DCH = ((SE[1][8] - SE[0][8]) - (S1(SE[1][7]) - S1(SE[0][7])) - D8) & M
C1V = [p for p in range(8) if ((CH(SE[1][7], SE[1][6], p << 29) - CH(SE[0][7], SE[0][6], p << 29)) & M) == _DCH]
assert len(C1V) == 1; C1V = C1V[0] << 29; C1MASK = 0xe0000000

def pf_ref(cv, a0, a1):
    """the four post-filters on the real words of the two members: C1 dW8 = D8, C2 s0(W9) diff, G s0(W8) diff, F7 s0(W7) diff (W7y - W7x
    = D7 and W9y - W9x = D9 always); the cumulative stage flags"""
    wx, wy = pair_words(cv, a0, a1)
    c1 = ((wy[8] - wx[8]) & M) == D8; c2 = ((s0(wy[9]) - s0(wx[9])) & M) == T9; g = ((s0(wy[8]) - s0(wx[8])) & M) == T8
    f7 = ((s0(wy[7]) - s0(wx[7])) & M) == T7 and ((wy[7] - wx[7]) & M) == D7
    return (int(c1), int(c1 and c2), int(c1 and c2 and g), int(c1 and c2 and g and f7))

# ---------------------------------------------------------------------------------------------- (3) the accepted event and step 3b
def cellok(k, i, x, y):
    m, v, d = CELLS[k][i]; return (x & m) == v and (x ^ y) == d
def rowok(tx, ty, i):
    (Ax, Ex, Wx), (Ay, Ey, Wy) = tx, ty
    if not (cellok(0, i, Ax[i], Ay[i]) and cellok(1, i, Ex[i], Ey[i]) and cellok(2, i, Wx[i], Wy[i])): return False
    if (Ex[i] ^ Ex[i-1]) & PQE[i]: return False
    for (k1, i1, b1, eq, k2, i2, b2, row) in X2:
        if row == i and (((tx[k1][i1] >> b1) ^ (tx[k2][i2] >> b2)) & 1) != (0 if eq else 1): return False
    return True
def outputs_equal(tx, ty): return all(tx[k][i] == ty[k][i] for k in (0, 1) for i in range(34, 38))
def accepted(tx, ty): return all(rowok(tx, ty, i) for i in range(16, 22)) and outputs_equal(tx, ty)

# ---------------------------------------------------------------------------------------------- (4) the counted machine
# collision-frontier-v5 on the 256-bit word RAM (proof.md Section 4): load, store, add, sub, and, or, xor, not, shift, immediate, random word
# 1; compare-and-branch 2; S0, S1, s0, s1 8; CH 3; MAJ 4; one target compression C = 2728.  A packed 32-bit table read (index shift, lane
# and + shift, address add, 256-bit load, shift, and) is 7; a packed write (read-modify-write) is 11.  Every work-counter add V += k is 1.
C_UNIT = 2728
class Mach:
    __slots__ = ('ops',)
    def __init__(self): self.ops = 0
    def op(self, n=1): self.ops += n
COST = dict(
    cv_begin=30 + 38 + 1 + 1 + 2 + 3,   # first-block words 30 (2 random 256-bit words, 16 fields), claw scalars 38, u0 1, V add 1, cap test 2, loop 3
    reset=5,                            # per 256-bit table word: store 1, address add 1, loop 3
    build=1 + 5 + 26 + 1 + 3 + 3 + 11,  # per candidate: offset 1, a0 map 5, F 26, slot 1, entry 3, loop 3, packed store 11 = 50
    u=1 + 8 + 1 + 3,                    # per scan word: u0 + n 1, s0 8, sub 1, loop 3 = 13
    head=5,                             # per head: W 1, W + 1024 1, low bits 1, straddle test 2
    look=1 + 7 + 2 + 2,                 # per lookup: index 1, packed load 7, residue sub + and 2, branch 2 = 12
    sent=3,                             # residue pass: entry = SENT? compare-and-branch 2, V add 1
    rec=1 + 5 + 26 + 2 + 2 + 1,         # residue pass on an occupied slot: offset 1, a0 map 5, F 26, dd sub + and 2, branch 2, V add 1 = 37
    strad_head=1,                       # a straddling head: V add 1 (its next-slot lookups are counted below)
    look2=2 + 7 + 2,                    # straddle lookup: next index (add, and) 2, packed load 7, entry = SENT? branch 2 = 11
    near=3 + 2 + 2 + 1,                 # straddle on an occupied slot: candidate F' 3, dd sub + and 2, branch 2, V add 1 = 8
    rec2=1 + 5 + 26 + 3 + 2 + 1,        # straddle candidate passing: offset 1, a0 map 5, F 26, bit test 3, branch 2, V add 1 = 38
    claw=3,                             # a claw: a1 = u - F + K2 + a0
    pf=(7, 22, 29, 30),                 # post-filter segments reached (C1, C2, G, F7), each ending with its V add
)
SENT = M

def postfilters(m, c, a0, a1):
    """the counted post-filter chain on (a0, a1); returns the stage flags (c1, c2, g, f7)"""
    E5 = (a1 + C5) & M
    m.op(COST['pf'][0])                                   # E5 1, mask and 1, compare-and-branch 2, a1 3 counted in claw, V add 1, segment 2
    if (E5 & C1MASK) != C1V: return (0, 0, 0, 0)
    w9 = (CW9 - a1) & M; w9y = (w9 + D9) & M
    m.op(COST['pf'][1])                                   # w9 1, w9y 1, s0 x 2 16, sub 1, compare-and-branch 2, V add 1
    if ((s0(w9y) - s0(w9)) & M) != T9: return (1, 0, 0, 0)
    E4 = (a0 + CE4 - (MA | (a1 & MB))) & M; w8 = (KW8 - E4 - (CA ^ (CB & E5))) & M; w8y = (w8 + D8) & M
    m.op(COST['pf'][2])                                   # MAJ 2, E4 2, CH 2, w8 2, w8y 1, s0 x 2 16, sub 1, branch 2, V add 1
    if ((s0(w8y) - s0(w8)) & M) != T8: return (1, 1, 0, 0)
    w7 = (c['KK7'] + MAJ(SA[0][2], a1, a0) - CH(SE[0][6], E5, E4)) & M; w7y = (w7 + D7) & M
    m.op(COST['pf'][3])                                   # MAJ 4, CH 3, w7 2, w7y 1, s0 x 2 16, sub 1, branch 2, V add 1
    if ((s0(w7y) - s0(w7)) & M) != T7: return (1, 1, 1, 0)
    return (1, 1, 1, 1)

STEP3B_MAX = None    # the longest path of step 3b (every test executed): counted on the S pair below, where every test passes
def rowtest(m, tx, ty, i):
    """the counted tests of row i: per word A, E, W the cell value (and, compare-and-branch: 3, when the cell fixes bits) and the XOR
    difference (xor, compare-and-branch: 3); the '+' pairs (xor, and, branch: 4); every two-bit condition closing at row i (2 shifts,
    xor, and, branch: 6).  Stops at the first failing test."""
    for k in range(3):
        x, y = tx[k][i], ty[k][i]; msk, v, d = CELLS[k][i]
        if msk:
            m.op(3)
            if (x & msk) != v: return False
        m.op(3)
        if (x ^ y) != d: return False
    if PQE[i]:
        m.op(4)
        if (tx[1][i] ^ tx[1][i-1]) & PQE[i]: return False
    for (k1, i1, b1, eq, k2, i2, b2, row) in X2:
        if row == i:
            m.op(6)
            if (((tx[k1][i1] >> b1) ^ (tx[k2][i2] >> b2)) & 1) != (0 if eq else 1): return False
    return True
def step3b(m, cv, a0, a1):
    """Step 3b on a good pair: Step 2 of both members, rows 16..37 of both members with the tests of rows 16..21 after each of those rows
    (early abort), the comparison of the eight output words; accepts iff rows 16..21 pass and the outputs are equal (Lemma 2)."""
    m.op(2 * (6 * 15 + 10 * 16))
    wx, wy = pair_words(cv, a0, a1); tx, ty = trace(cv, wx), trace(cv, wy); ok = True
    for i in range(16, 22):
        m.op(100)
        if not rowtest(m, tx, ty, i): ok = False; break
    if ok:
        m.op(100 * 16 + 17); ok = outputs_equal(tx, ty)
    m.op(1)
    return ok, wx, wy

_m = Mach(); assert step3b(_m, PCV, SA[0][0], SA[0][1])[0]; STEP3B_MAX = _m.ops    # 3,014 operations
# ---------------------------------------------------------------------------------------------- (5) one chaining value (proof.md Section 3)
def u0_of(cv):
    """the scan start u0 of a chaining value (a fresh random word in the procedure; in the experiments derived from cv)"""
    st = (0x9E3779B97F4A7C15 ^ ((cv[0] << 32) | cv[1])) & 0xFFFFFFFFFFFFFFFF
    st ^= (st << 13) & 0xFFFFFFFFFFFFFFFF; st ^= st >> 7; st ^= (st << 17) & 0xFFFFFFFFFFFFFFFF
    return (st >> 16) & M

def run_cv(cv, LU, ls=26, count=True, ref=False, collect=False, u0=None):
    """One chaining value: reset the 2^ls-slot table, load the 2^(ls+1) candidates a0 = p_a0(o), o < 2^(ls+1) (last write wins), scan the
    2^LU distinct words u = u0 + n, test every claw with the post-filters and run step 3b on every good pair.  Full scale: ls = 26,
    LU = 32.  Entries: (o << RB) | (F mod 2^RB), RB = 31 - ls; slot = F >> TB, TB = 32 - ls; the bit F[RB] (TB - RB = 1) is not stored,
    so a residue pass on an occupied slot recomputes F(a0).  count: charge every operation (Section 4).  ref: claws also by an
    independent sorted-array search over the visible entries."""
    TB = 32 - ls; RB = 31 - ls; NS = 1 << ls; NC = 1 << (ls + 1)
    tmask = (1 << TB) - 1; rmask = (1 << RB) - 1; rtest = rmask & ~5
    m = Mach() if count else None; c = cvc(cv)
    if m: m.op(COST['cv_begin'])
    if u0 is None: u0 = u0_of(cv)
    tab = [SENT] * NS
    if m: m.op(COST['reset'] * max(1, NS >> 3))
    for o in range(NC):
        F = Ffun(c, p_a0(o)); tab[F >> TB] = (o << RB) | (F & rmask)
    if m: m.op(COST['build'] * NC)
    occ = sum(1 for e in tab if e != SENT)
    st = dict(claws=0, refclaws=0, passes=[0, 0, 0, 0], good=[], coll=[], allclaws=[], respass=0, recomputes=0, strad=0)
    def claw(a0, u, F):
        st['claws'] += 1; a1 = (u - F + c['K2'] + a0) & M
        if m: m.op(COST['claw'])
        fl = postfilters(m or Mach(), c, a0, a1)
        for j in range(4): st['passes'][j] += fl[j]
        if collect: st['allclaws'].append((a0, a1, u, fl))
        if fl[3]:
            st['good'].append((a0, a1, u)); ok, wx, wy = step3b(m or Mach(), cv, a0, a1)
            if ok: st['coll'].append((a0, a1, u, wx, wy))
    if ref:
        import bisect
        vis = sorted(Ffun(c, p_a0(tab[s] >> RB)) for s in range(NS) if tab[s] != SENT)
    for n in range(1 << LU):
        u = (u0 + n) & M; P = (s0(u) - u) & M
        if m: m.op(COST['u'])
        for H in HEADS:
            W = (H - P) & M
            if m: m.op(COST['head'] + (3 if TB > 10 else 0))
            sd = (W & tmask) >= tmask - 4 or ((W + 1024) & tmask) >= tmask - 4
            if sd and m: m.op(COST['strad_head'])
            for Wsub in (W, (W + 1024) & M):
                idx = Wsub >> TB; e = tab[idx]
                if m: m.op(COST['look'])
                if ((e - Wsub) & rtest) == 0:
                    st['respass'] += 1
                    if m: m.op(COST['sent'])
                    if e != SENT:
                        st['recomputes'] += 1; a0 = p_a0(e >> RB); F = Ffun(c, a0)
                        if m: m.op(COST['rec'])
                        if ((F - Wsub) & M & ~5) == 0: claw(a0, u, F)
                if (Wsub & tmask) >= tmask - 4:                # a candidate F in [Wsub, Wsub + 5] may sit in the next slot
                    st['strad'] += 1
                    idx2 = (idx + 1) & (NS - 1); e2 = tab[idx2]
                    if m: m.op(COST['look2'])
                    if e2 != SENT:
                        Fp = ((idx2 << TB) | (e2 & rmask)) & M   # the candidate with its unstored bit F[RB] = 0 (the only value <= Wsub + 5)
                        if m: m.op(COST['near'])
                        if ((Fp - Wsub) & M & ~5) == 0:
                            st['recomputes'] += 1; a0 = p_a0(e2 >> RB); F = Ffun(c, a0)
                            if m: m.op(COST['rec2'])
                            if F == Fp: claw(a0, u, F)
        if ref:
            for H in HEADS:
                for o_ in OFFS:
                    want = ((H + o_) - P) & M; k = bisect.bisect_left(vis, want)
                    if k < len(vis) and vis[k] == want: st['refclaws'] += 1
    st.update(occ=occ, occ_frac=occ / NS, ops=(m.ops if m else 0), u0=u0)
    return st

# ---------------------------------------------------------------------------------------------- (6) the ledger (proof.md Sections 5 to 7)
from decimal import Decimal as Dm, getcontext
getcontext().prec = 90
def _L2(): return Dm(2).ln()
def P2(x): return (Dm(x) * _L2()).exp()
def lg2(x): return float(Dm(x).ln() / _L2())
# exact post-filter counts (own exhaustive programs, proof.md Section 6): P(C1) = 1/8; |C1 and C2| over a1; the C1 C2 G count of a0 in each
# 2^25-window of P (a1 summed over C1 and C2); |F7|
N_C1C2 = 53096854
G_WIN = {2: 29047307906207, 10: 29047307906362, 18: 29047307910144, 26: 29047307910144}
G_MIN = 4 * min(G_WIN.values())                    # charged: the smallest window count for all four (a lower bound for any mix)
N_F7 = 287309824
Q3_MODEL = '-96.0133'                              # the registered accepted-event rate of the A0-variant family (e4243e7a Section 9)
D_LB = '-0.0305'                                   # min(0, D_LB(A0), D_LB(A0sel)) of the registered paired runs on P, rounded down (proof.md Section 9)
A_C, A_S, DEV = 2 ** 78, 2 ** 74, 2 ** 70
BONF = 7                                           # Pr[X_j >= 1] >= (1 - 2^-BONF) E[X_j]: E[L]/E[K] <= 0.0051 (the full-scan partner count, proof.md Section 8)

def model(ls=26, LU=32):
    """expected and maximal counted work per scan word and per chaining value at table size 2^ls (Sections 4, 5)"""
    TB = 32 - ls; RB = 31 - ls; NS = 2 ** ls; NC = 2 ** (ls + 1)
    occ = 1 - (1 - Dm(1) / NS) ** NC                                 # expected occupied fraction (last write wins)
    p_r = Dm(4) / 2 ** RB                                            # residue pass of a lookup (SENT or a uniform residue)
    p_s = Dm(5) / 2 ** TB                                            # a window straddles into the next slot
    p_near = Dm(2) / 2 ** RB                                         # a straddle candidate F' falls in [Wsub, Wsub + 5] (mean over the 5 cases)
    p1, p12, p12g = Dm(1) / 8, Dm(N_C1C2) / 2 ** 32, Dm(G_MIN) / 2 ** 59
    q_pf = p12g * Dm(N_F7) / 2 ** 32
    pf_mean = COST['claw'] + COST['pf'][0] + p1 * COST['pf'][1] + p12 * COST['pf'][2] + p12g * COST['pf'][3]
    claws_u = 160 * occ / 2 ** TB
    head = COST['head'] + (3 if TB > 10 else 0)
    if TB <= 10:   # the two windows of a head have the same low bits: one straddle test, both straddle together
        strad = 20 * p_s * (COST['strad_head'] + 2 * (COST['look2'] + occ * (COST['near'] + p_near * COST['rec2'])))
    else:
        strad = 40 * p_s * (COST['look2'] + occ * (COST['near'] + p_near * COST['rec2'])) + 20 * (1 - (1 - p_s) ** 2) * COST['strad_head']
    look = 40 * (COST['look'] + p_r * (COST['sent'] + occ * COST['rec']))
    per_u = COST['u'] + 20 * head + strad + look + claws_u * (pf_mean + q_pf * STEP3B_MAX)
    fixed = C_UNIT + COST['cv_begin'] + COST['reset'] * max(1, NS // 8) + COST['build'] * NC
    umax = (COST['u'] + 20 * (head + COST['strad_head'] + 2 * (COST['look2'] + COST['near'] + COST['rec2'])) + 40 * (COST['look'] + COST['sent'] + COST['rec'])
            + 80 * (COST['claw'] + sum(COST['pf']) + STEP3B_MAX))
    return dict(occ=occ, p_r=p_r, p_s=p_s, claws_u=claws_u, pf_mean=pf_mean, q_pf=q_pf, p12g=p12g, per_u=per_u, umax=umax, fixed=fixed,
                wbar=fixed + Dm(2) ** LU * per_u, vmax=fixed + Dm(2) ** LU * umax, strad=strad, look=look, LU=LU, ls=ls)

def ledger(show=True, q3_log2=None, d_lb=None, succ='0.39', eps_log2=16):
    md = model()
    q3m = Dm(q3_log2 if q3_log2 is not None else Q3_MODEL)
    d = Dm(d_lb if d_lb is not None else (D_LB if D_LB is not None else 0))
    q3p1 = q3m + min(Dm(0), d)
    q3r = P2(q3p1) * Dm(2) ** 32 / 160
    claws_lb = md['claws_u'] - Dm(160) / 2 ** 32 / 32               # an entry equal to SENT (only the last candidate; probability 1/32) is skipped
    EX = Dm(2) ** md['LU'] * claws_lb * md['q_pf'] * q3r * (1 - Dm(2) ** -BONF)     # Lemma 5: groups of linked good pairs (Section 8)
    target = 1 - Dm(succ) - Dm(2) ** -60
    n = int(-(target).ln() / EX) + 1
    while 1 - (-(n - 1) * EX).exp() - Dm(2) ** -60 >= Dm(succ): n -= 1
    eps = Dm(2) ** -eps_log2
    VMAX = int(((1 + eps) * n * md['wbar']).to_integral_value(rounding='ROUND_CEILING'))
    OVER = int(md['vmax'].to_integral_value(rounding='ROUND_CEILING'))
    FIN = 6 * C_UNIT + 1600
    N = (A_C + A_S + DEV) * C_UNIT + VMAX + OVER + FIN
    bern = (eps ** 2 * n * md['wbar']) / (2 * md['vmax'] * (1 + eps / 3))
    succ_lb = 1 - (-n * EX).exp() - Dm(2) ** -60
    t = lg2(Dm(N) / C_UNIT)
    out = dict(time_log2=t, N=N, N_CV=n, VMAX=VMAX, OVER=OVER, FIN=FIN, wbar=float(md['wbar']), vmax=float(md['vmax']), per_u=float(md['per_u']),
               claws_u=float(md['claws_u']), occ=float(md['occ']), q_pf_log2=lg2(md['q_pf']), q3_P1=float(q3p1), q3r_log2=lg2(q3r),
               EX=float(EX), bernstein=float(bern), success_lb=str(succ_lb)[:24], ops_per_claw=float(md['wbar'] / (Dm(2) ** md['LU'] * md['claws_u'])),
               preprocessing_log2=lg2(Dm(A_C + A_S + DEV)))
    if show:
        print('model (2^26 slots, 2^27 candidates, 2^32 scan words per chaining value):')
        print('  occupancy %.6f  claws per u %.6f  residue pass %.5f  straddle %.5f' % (md['occ'], md['claws_u'], md['p_r'], md['p_s']))
        print('  per u: fixed %d + heads %d + lookups %.4f + straddles %.4f + claws %.6f x (post-filters %.4f + q_pf x %d) = %.4f' % (
            COST['u'], 20 * COST['head'], md['look'], md['strad'], md['claws_u'], md['pf_mean'], STEP3B_MAX, md['per_u']))
        print('  q_pf = 2^%.5f (C1 C2 G 2^%.5f, F7 2^%.5f); per u max %d' % (lg2(md['q_pf']), lg2(md['p12g']), lg2(Dm(N_F7) / 2 ** 32), md['umax']))
        print('  wbar %.6e  vmax %d  operations per claw %.3f' % (md['wbar'], md['vmax'], out['ops_per_claw']))
        print('q3_P1 = %s + min(0, %s) = %s; q3r = 2^%.5f; E[X_j] = %.6e' % (q3m, d, q3p1, lg2(q3r), EX))
        print('N_CV %d  V_MAX %d  OVER %d  FIN %d' % (n, VMAX, OVER, FIN))
        print('N = %d  time_log2 = %.5f  preprocessing_log2 = %.5f' % (N, t, out['preprocessing_log2']))
        print('Bernstein exponent %.4e; success lower bound %s' % (bern, out['success_lb']))
    return out

# ---------------------------------------------------------------------------------------------- (7) organizer experiments
class Shake:
    def __init__(self, seed): self.seed = seed.encode(); self.k = 0; self.buf = b''; self.pos = 0
    def word(self):
        if self.pos + 32 > len(self.buf):
            self.buf = hashlib.shake_256(self.seed + b'|' + str(self.k).encode()).digest(1 << 14); self.k += 1; self.pos = 0
        v = int.from_bytes(self.buf[self.pos:self.pos + 32], 'little'); self.pos += 32; return v
    def u32(self): return self.word() & M
def first_block(rng):
    r0, r1 = rng.word(), rng.word()
    M0 = [(r0 >> (32 * q)) & M for q in range(8)] + [(r1 >> (32 * q)) & M for q in range(8)]
    return M0, compress(IV, M0)
EXP_LS, EXP_LU, EXP_TRIALS = 16, 12, 6
ROWS_LU, ROWS_TRIALS = 13, 4
def online_experiment(req):
    """the counted procedure on organizer-seeded first blocks (real compressions), reduced size: 2^16 slots, 2^17 candidates of P, 2^12
    scan words.  Every claw is checked against an independent sorted-array search, against the real E16 of member x (in S160) and the
    counted post-filters against the real words of the two members; step 3b runs on every good pair and a pair is returned only if step 3b
    accepts (Lemma 2: then it is a collision of the target; none is expected at this size).  Trial EXP_TRIALS runs step 3b on S's own
    pair; trials above return no pair."""
    out = []
    for tr in req['trials']:
        t = tr['trial']; rec = dict(trial=t, message_a_hex=None, message_b_hex=None)
        if t > EXP_TRIALS: out.append(rec); continue
        if t == EXP_TRIALS:
            m = Mach(); ok, wx, wy = step3b(m, PCV, SA[0][0], SA[0][1])
            rec['observations'] = dict(s_pair_step3b_accepts=int(ok), s_pair_step3b_ops=m.ops, s_pair_words_equal_pmx=int(wx == PMX and wy == PMY))
            out.append(rec); continue
        rng = Shake(req['experiment_id'] + '|' + tr['seed']); M0, cv = first_block(rng)
        st = run_cv(cv, EXP_LU, ls=EXP_LS, count=True, ref=True, collect=True, u0=rng.u32())
        bad_e16 = bad_pf = 0
        for (a0, a1, u, fl) in st['allclaws']:
            wx, wy = pair_words(cv, a0, a1)
            bad_e16 += trace(cv, wx, 17)[1][16] not in S160_SET or wx[1] != u or not in_P(a0)
            bad_pf += pf_ref(cv, a0, a1) != fl
        md = model(EXP_LS, EXP_LU)
        if st['coll']:
            a0, a1, u, wx, wy = st['coll'][0]
            rec['message_a_hex'] = struct.pack('>32I', *(M0 + wx)).hex(); rec['message_b_hex'] = struct.pack('>32I', *(M0 + wy)).hex()
        rec['observations'] = dict(claws=st['claws'], reference_claws=st['refclaws'], distinct_pairs=len(set((a, b) for a, b, _, _ in st['allclaws'])),
                                   bad_e16=bad_e16, bad_postfilters=bad_pf, c1=st['passes'][0], c1c2=st['passes'][1], c1c2g=st['passes'][2],
                                   all4=st['passes'][3], step3b_accepts=len(st['coll']), occupancy=round(st['occ_frac'], 6),
                                   counted_ops=st['ops'], model_ops=int(md['wbar']), residue_passes=st['respass'], recomputes=st['recomputes'])
        out.append(rec)
    return dict(schema_version=1, trials=out)
def rows_experiment(req):
    """rows 16..21 and the outputs on every claw of a reduced-size run (2^16 slots, 2^13 scan words) on organizer-seeded first blocks:
    the number of claws passing each row of the accepted event (all claws pass row 16 by construction) and the post-filter stages; returns
    a pair only if a claw is accepted (none is expected)."""
    out = []
    for tr in req['trials']:
        t = tr['trial']; rec = dict(trial=t, message_a_hex=None, message_b_hex=None)
        if t >= ROWS_TRIALS: out.append(rec); continue
        rng = Shake(req['experiment_id'] + '|' + tr['seed']); M0, cv = first_block(rng)
        st = run_cv(cv, ROWS_LU, ls=EXP_LS, count=False, collect=True, u0=rng.u32())
        rows = [0] * 6; acc = 0
        for (a0, a1, u, fl) in st['allclaws']:
            wx, wy = pair_words(cv, a0, a1); tx, ty = trace(cv, wx), trace(cv, wy)
            for k, i in enumerate(range(16, 22)):
                if not rowok(tx, ty, i): break
                rows[k] += 1
            if accepted(tx, ty):
                acc += 1
                if rec['message_a_hex'] is None:
                    rec['message_a_hex'] = struct.pack('>32I', *(M0 + wx)).hex(); rec['message_b_hex'] = struct.pack('>32I', *(M0 + wy)).hex()
        rec['observations'] = dict(claws=st['claws'], row16=rows[0], row17=rows[1], row18=rows[2], row19=rows[3], row20=rows[4], row21=rows[5],
                                   accepted=acc, c1=st['passes'][0], c1c2=st['passes'][1], c1c2g=st['passes'][2], all4=st['passes'][3])
        out.append(rec)
    return dict(schema_version=1, trials=out)
def run_request(req): return rows_experiment(req) if 'rows' in req['experiment_id'] else online_experiment(req)

# ---------------------------------------------------------------------------------------------- (8) selftest, main
S160_SET = frozenset(S160)
def selftest():
    import random
    rr = random.Random(7); ok = True
    def chk(name, cond, extra=''):
        nonlocal ok; ok = ok and bool(cond); print('%-78s %s %s' % (name, 'ok' if cond else 'FAIL', extra), flush=True)
    tx, ty = trace(PCV, PMX), trace(PCV, PMY)
    chk('1 S pair: outputs equal, accepted event (rows 16..21, outputs), W7 in F7', accepted(tx, ty) and inF7(PMX[7]) and PMX != PMY)
    chk('  pair_words(PCV, A0, A1) reproduces both members', pair_words(PCV, SA[0][0], SA[0][1]) == [PMX, PMY])
    chk('  the four post-filters hold on the S pair', pf_ref(PCV, SA[0][0], SA[0][1]) == (1, 1, 1, 1))
    m = Mach(); a, wx, wy = step3b(m, PCV, SA[0][0], SA[0][1])
    chk('  step 3b accepts the S pair at its longest path', a and m.ops == STEP3B_MAX, '(%d operations)' % m.ops)
    def row16(e16):
        A = dict(SA[0]); E = dict(SE[0]); B = dict(SA[1]); F = dict(SE[1])
        w16 = (e16 - C16) & M; v16 = (w16 + (_ty[2][16] - _tx[2][16])) & M
        for (AA, EE, w) in ((A, E, w16), (B, F, v16)):
            T1 = (EE[12] + S1(EE[15]) + CH(EE[15], EE[14], EE[13]) + K[16] + w) & M
            EE[16] = (AA[12] + T1) & M; AA[16] = (T1 + S0(AA[15]) + MAJ(AA[15], AA[14], AA[13])) & M
        WX = dict(enumerate(PMX)); WY = dict(enumerate(PMY)); WX[16] = w16; WY[16] = v16
        return rowok((A, E, WX), (B, F, WY), 16)
    cand = S160 + [rr.getrandbits(32) for _ in range(20000)] + [g ^ (1 << b) for g in S160[:40] for b in range(32)]
    chk('2 S160: 160 words, 20 heads x bits 0, 2, 10; row 16 on S160, 20,000 random words and 1,280 neighbours', all(row16(e) == (e in S160_SET) for e in cand))
    bad = 0
    for _ in range(300):
        cv = [rr.getrandbits(32) for _ in range(8)]; c = cvc(cv); a0 = p_a0(rr.getrandbits(27)); a1 = rr.getrandbits(32)
        wx, wy = pair_words(cv, a0, a1); t = trace(cv, wx, 17); tt = trace(cv, wy, 17)
        bad += wx[0] != (a0 + c['k0']) & M or wx[1] != (a1 + hfun(c, a0)) & M
        bad += t[1][16] != (Ffun(c, a0) + s0(wx[1]) - wx[1]) & M
        bad += any(t[0][i] != SA[0][i] or tt[0][i] != SA[1][i] for i in range(2, 16)) or any(t[1][i] != SE[0][i] or tt[1][i] != SE[1][i] for i in range(6, 16))
        bad += ((wy[7] - wx[7]) & M) != D7 or ((wy[9] - wx[9]) & M) != D9
    chk('3 Lemma 1 on 300 random (cv, a0 in P, a1): W0, W1, E16x = F(a0) + s0(u) - u, rows 2..15 = S, dW7, dW9', bad == 0)
    bad = 0; stages = [0, 0, 0, 0]
    for _ in range(60000):
        cv = [rr.getrandbits(32) for _ in range(8)]; c = cvc(cv); a0 = p_a0(rr.getrandbits(27)); a1 = rr.getrandbits(32)
        if rr.random() < 0.5: a1 = (C1V + (a1 & 0x1fffffff) - C5) & M          # half of the samples pass C1
        fl = postfilters(Mach(), c, a0, a1); bad += fl != pf_ref(cv, a0, a1)
        for j in range(4): stages[j] += fl[j]
    chk('4 counted post-filters = the real-word definition on 60,000 pairs', bad == 0, str(stages))
    o = rr.getrandbits(27); chk('  the a0 set P: offset map is a bijection on 2^27 offsets (samples) and lands in P', all(p_off(p_a0(x)) == x and in_P(p_a0(x)) for x in [o, 0, (1 << 27) - 1] + [rr.getrandbits(27) for _ in range(1000)]))
    cv5 = [rr.getrandbits(32) for _ in range(8)]; st = run_cv(cv5, 13, ls=16, count=True, ref=True, collect=True)
    md = model(16, 13)
    chk('5 run at 2^16 slots, 2^17 candidates, 2^13 scan words: claws = reference search', st['claws'] == st['refclaws'], '(%d claws, occupancy %.5f vs %.5f)' % (st['claws'], st['occ_frac'], md['occ']))
    chk('  claws distinct and every claw\'s real E16 in S160', len(set((a, b) for a, b, _, _ in st['allclaws'])) == st['claws'] and
        all(trace(cv5, pair_words(cv5, a, b)[0], 17)[1][16] in S160_SET and in_P(a) for a, b, _, _ in st['allclaws']))
    ratio = st['ops'] / float(md['wbar'])
    chk('  counted operations against the model mean (wbar at that size)', 0.9 < ratio < 1.1 and st['ops'] <= md['vmax'], '(counted %d, model %.0f, ratio %.4f)' % (st['ops'], md['wbar'], ratio))
    r = online_experiment(dict(experiment_id='p1t-online-r38', trials=[dict(trial=t, seed='%064x' % t) for t in (0, 1, EXP_TRIALS)]))
    obs = [t['observations'] for t in r['trials']]
    chk('6 organizer experiment p1t-online-r38 (3 trials): claws = reference, 0 bad E16, 0 bad post-filters, S pair accepted',
        all(o['claws'] == o['reference_claws'] and o['bad_e16'] == 0 and o['bad_postfilters'] == 0 for o in obs[:2]) and obs[2]['s_pair_step3b_accepts'] == 1, str(obs))
    lg = ledger(show=False)
    chk('7 ledger: success lower bound >= 0.39', Dm(lg['success_lb']) >= Dm('0.39'), '(time_log2 %.5f)' % lg['time_log2'])
    print('SELFTEST', 'PASSED' if ok else 'FAILED'); return ok

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'selftest': sys.exit(0 if selftest() else 1)
    if len(sys.argv) > 1 and sys.argv[1] == 'ledger': ledger(); sys.exit(0)
    sys.stdout.write(json.dumps(run_request(json.loads(sys.stdin.read())), separators=(',', ':')))
