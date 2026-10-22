# p1b38.py - sha256-r38: the P8 two-block procedure with the P1 sum-claw on a 2^27-candidate a0 set, loaded into a bucket table of
# 2^23 seven-lane 256-bit words with an exact 9-bit tag per lane (own code, standard library only).
# Derivative, credited (proof.md, introduction): the P1 sum-claw, its post-filter chain, step 3b, the counted pricing and q3_model are
# Jbenisek's (e4243e7a); the 2^32-word scan is newjordan's (711c4bf8); the measured online memory cell follows 0xplemonade's a32131ff and the
# capped Step-1 cell is 377cb363's; the seven-entry bucket table with exact tags, the common low bits of the 20 heads (one w per scan word)
# and the head address chain follow 0xplemonade's b561f523 and its predecessor e6a33086 (our layout, test and counts are our own); the
# characteristic P8, its semi-free-start pair S and its accepted event are ours (1a695f0b), the event as transcribed in e4243e7a.  New here:
# 2^27 candidates of the set P (the best class of the exact C1 C2 G count) fill the 7-lane buckets (occupancy 0.99916); one 256-bit word
# per bucket holds 7 lanes of (9-bit tag, 27-bit offset); one SWAR pass tests the 14 tags of a head's two windows (buckets b, b + 2); the
# group bound of Lemma 5 with the measured full-scan link rate; our own exact counts and paired q3 measurement on P.  No program of
# another participant is executed; the event cells below are data (P8's printed cells, rows 7..22, and its two-bit conditions).
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
    cv_begin=30 + 38 + 1 + 1 + 1 + 2 + 3,
                                        # first-block words 30 (2 random 256-bit words, 16 fields), claw scalars 38, u0 1, the rotation R of the
                                        # insertion order (a random word) 1, V add 1, cap test 2, loop 3 = 76
    reset=5,                            # per 256-bit table word: store 1, address add 1, loop 3
    build=2 + 4 + 5 + 26 + 1 + 1 + 1 + 2 + 3 + 3 + 1 + 1 + 1 + 1 + 2 + 3,
                                        # per candidate n (inserting path; a full bucket skips 12 of these): (n + R) mod 2^27 2, offset
                                        # o = rotr2(n + R) 4, a0 map 5,
                                        # F 26, bucket b = F >> 9 1 (the table occupies RAM words 0 .. 2^23 + 2, so b is the address), load 1,
                                        # count 1, count < 7 branch 2, lane shift 36c 3, entry 3, shift 1, or 1, count + 1 1, store 1, padding test
                                        # b < 3 2, loop 3 = 57
    pad=2,                              # a padding copy (bucket b < 3): address 2^23 + b 1, store 1
    u=1 + 8 + 1 + 3,                    # per scan word: u0 + n 1, s0 8, sub 1, loop 3 = 13
    upre=4 + 10 + 2,                    # per scan word: W0 1, w 1, bucket b0 = W0 >> 9 1, spare 1; broadcast of w to the 14 fields and C = K512 - Wb 10;
                                        # straddle test w >= 507 2 = 16
    head=2 + 1 + 2 + 4 + 1 + 2 + 3 + 2, # per head: bucket b = (b0 + DH[h]) & (2^23 - 1) 2 (also its address), load b 1, address b + 2 and load 2,
                                        # combine the two tag sets 4, r = v + C 1, y = (r ^ X200) & M3FA 2, zero test ((y | G10) - L0) & G10 3,
                                        # compare-and-branch 2 = 17
    strad=20 * (4 + 4 + 1 + 1 + 3 + 2) + 1,
                                        # a straddling scan word (w >= 507): per head the buckets b+1, b+3: two loads 4, combine 4, r 1, y = r & M3FA 1,
                                        # zero test 3, branch 2 = 15; V add 1: 301
    event=1,                            # a head with a match: mm = z ^ G10
    match=18 + 5 + 3 + 5 + 5 + 3 + 4 + 1,
                                        # per matching field: locate the lowest set field (3 levels of and, branch, shift, add 5 each; field 3) 18,
                                        # word select, entry, tag, offset 5, full-bucket test 3, a0 map 5, F from bucket and tag 5, a1 3,
                                        # clear the bit and loop 4, V add 1 = 44
    notfull=2,                          # a match in a bucket that is not full: lane < count test
    pf=(7, 22, 29, 30),                 # post-filter segments reached (C1, C2, G, F7), each ending with its V add
)
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

# The bucket table (proof.md Section 3).  2^23 buckets b = F >> 9, one 256-bit word each (plus 3 padding words, copies of buckets 0, 1, 2).
# Lane i < 7 of a word, bits [36i, 36i + 36): the 9-bit tag F mod 512 and the 27-bit offset o of a0 = p(o); bits 252..254: the count of
# lanes in use (lanes are filled in order).  Candidates n = 0 .. NC - 1 are inserted in order, o = rotr2((n + R) mod 2^27) with R a fresh
# random 27-bit word per chaining value (the window o >> 25 cycles), first 7 per bucket kept: the kept candidates favour small n, and the
# random rotation R makes the law of a kept a0, averaged over R, exactly uniform on P.  All 20 heads are equal mod 2^13, so w = (H - P) mod 512 is one value per scan word and the head's
# bucket is b0 + DH[h]; the two windows W and W + 1024 of a head are the buckets b and b + 2 with the same w.  One SWAR pass tests the 14
# tags of the two buckets: field 0 (lane bits 0..10) holds b's tag, field 1 (lane bits 11..21) b + 2's; r = t + 512 - w per field (no borrow),
# a field matches iff r - 512 is in {0, 1, 4, 5}, i.e. ((r ^ 0x200) & 0x3fa) == 0, detected with bit 10 of the field as headroom.
NBK = 1 << 23; LANE = 36; NL = 7; OMASK = (1 << 27) - 1; W256 = (1 << 256) - 1
def _rep(v, pos): return sum(v << (LANE * i + pos) for i in range(NL))
TM0 = _rep(511, 0); TM1 = _rep(511, 11); LM7 = _rep((1 << 22) - 1, 0)
K512 = _rep(512, 0) | _rep(512, 11); M3FA = _rep(0x3fa, 0) | _rep(0x3fa, 11); G10 = _rep(1, 10) | _rep(1, 21); L0 = _rep(1, 0) | _rep(1, 11)
H0 = HEADS[0]; assert all((h - H0) & 0x1fff == 0 for h in HEADS)
DH = [((h - H0) & M) >> 9 for h in HEADS]                    # bucket deltas of the heads (multiples of 16)
def rotr2(n): return (n >> 2) | ((n & 3) << 25)
def build_table(c, NC, m=None, R=0):
    T = {}
    for n in range(NC):
        o = rotr2((n + R) & OMASK); a0 = p_a0(o); F = Ffun(c, a0); b = F >> 9; wd = T.get(b, 0); cnt = wd >> 252
        if cnt < 7:
            wd = wd | (((o << 9) | (F & 511)) << (LANE * cnt)); wd += 1 << 252; T[b] = wd
            if b < 3: T[NBK + b] = wd
            if m: m.op(COST['build'] + (COST['pad'] if b < 3 else 0))
        elif m: m.op(COST['build'] - 12)
    return T
def entries(T):
    """(F, o) of every stored entry (padding words excluded)"""
    out = []
    for b, wd in T.items():
        if b >= NBK: continue
        for i in range(wd >> 252):
            e = (wd >> (LANE * i)) & ((1 << LANE) - 1); out.append(((b << 9) | (e & 511), e >> 9))
    return out

def run_cv(cv, LU, nc=27, count=True, ref=False, collect=False, u0=None, R=None):
    """One chaining value: reset the 2^23 + 3 table words, insert the 2^nc candidates n -> a0 = p(rotr2(n)), scan the 2^LU distinct words
    u = u0 + n, test every claw with the post-filters and run step 3b on every good pair.  Full scale: nc = 27, LU = 32.  count: charge every
    operation (Section 4).  ref: claws also by an independent sorted search over the stored entries (with multiplicity)."""
    NC = 1 << nc
    m = Mach() if count else None; c = cvc(cv)
    if m: m.op(COST['cv_begin'] + COST['reset'] * (NBK + 3))
    if u0 is None: u0 = u0_of(cv)
    if R is None: R = (u0_of(cv[::-1]) << 5 ^ cv[2]) & OMASK
    T = build_table(c, NC, m, R)
    st = dict(claws=0, refclaws=0, passes=[0, 0, 0, 0], good=[], coll=[], allclaws=[], events=0, matches=0, spurious=0, strad=0,
              stored=sum(wd >> 252 for b, wd in T.items() if b < NBK), buckets=sum(1 for b in T if b < NBK))
    def claw(a0, u, F):
        st['claws'] += 1; a1 = (u - F + c['K2'] + a0) & M
        fl = postfilters(m or Mach(), c, a0, a1)
        for j in range(4): st['passes'][j] += fl[j]
        if collect: st['allclaws'].append((a0, a1, u, fl))
        if fl[3]:
            st['good'].append((a0, a1, u)); ok, wx, wy = step3b(m or Mach(), cv, a0, a1)
            if ok: st['coll'].append((a0, a1, u, wx, wy))
    def matches(z, wa, wb, bh, extra, u):
        mm = z ^ G10; st['events'] += 1
        if m: m.op(COST['event'])
        while mm:
            x = mm; i = 0
            if x & ((1 << 144) - 1) == 0: x >>= 144; i += 4
            if x & ((1 << 72) - 1) == 0: x >>= 72; i += 2
            if x & ((1 << 36) - 1) == 0: x >>= 36; i += 1
            f = 0 if x & (1 << 10) else 1
            wd = wa if f == 0 else wb; e = wd >> (LANE * i); t = e & 511; o = (e >> 9) & OMASK; cnt = wd >> 252
            st['matches'] += 1
            if m: m.op(COST['match'])
            if cnt != 7:
                if m: m.op(COST['notfull'])
                if i >= cnt: st['spurious'] += 1; mm &= mm - 1; continue
            a0 = p_a0(o); F = ((((bh + 2 * f + extra) & (NBK - 1)) << 9) | t)
            claw(a0, u, F)
            mm &= mm - 1
    if ref:
        import bisect
        vis = sorted(F for F, o in entries(T))
    for n in range(1 << LU):
        u = (u0 + n) & M; P = (s0(u) - u) & M
        W0 = (H0 - P) & M; w = W0 & 511; b0 = W0 >> 9
        x = w | (w << 11); x |= x << 36; x |= x << 72; x |= x << 144; x &= LM7; C = K512 - x
        if m: m.op(COST['u'] + COST['upre'] + 20 * COST['head'])
        strad = w >= 507
        if strad:
            st['strad'] += 1
            if m: m.op(COST['strad'])
        for d in DH:
            bh = (b0 + d) & (NBK - 1)
            w1 = T.get(bh, 0); w2 = T.get(bh + 2, 0)
            v = (w1 & TM0) | ((w2 << 11) & TM1); r = v + C; y = (r ^ K512) & M3FA; z = ((y | G10) - L0) & G10
            if z != G10: matches(z, w1, w2, bh, 0, u)
            if strad:
                w3 = T.get(bh + 1, 0); w4 = T.get(bh + 3, 0)
                v = (w3 & TM0) | ((w4 << 11) & TM1); r = v + C; y = r & M3FA; z = ((y | G10) - L0) & G10
                if z != G10: matches(z, w3, w4, bh, 1, u)
        if ref:
            for t in S160:
                want = (t - P) & M; k = bisect.bisect_left(vis, want); k2 = bisect.bisect_right(vis, want); st['refclaws'] += k2 - k
    st.update(ops=(m.ops if m else 0), u0=u0)
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
BONF = '6.5'                                       # Pr[X_j >= 1] >= E[X_j]^2/E[X_j^2] >= (1 - 2^-BONF) q3r E[K_j]: 2 E[L]/E[K] + q3r E[K^2]/E[K] <= 2^-6.5 (proof.md Sections 7, 8)

def binom_min7(n, p):
    """E[min(X, 7)] for X ~ Binomial(n, p), exactly (Decimal): the expected stored lanes of a bucket"""
    p = Dm(p); q = 1 - p; pk = q ** n; tot = Dm(0); cdf = Dm(0)
    for k in range(7):
        tot += k * pk; cdf += pk; pk = pk * (n - k) / (k + 1) * p / q
    return tot + 7 * (1 - cdf)

def model(nc=27, LU=32):
    """expected and maximal counted work per scan word and per chaining value with 2^nc candidates (Sections 4, 5)"""
    NC = 2 ** nc
    stored = binom_min7(NC, Dm(1) / NBK)                            # expected lanes in use per bucket
    empty = 7 - stored
    p1, p12, p12g = Dm(1) / 8, Dm(N_C1C2) / 2 ** 32, Dm(G_MIN) / 2 ** 59
    q_pf = p12g * Dm(N_F7) / 2 ** 32
    pf_mean = COST['pf'][0] + p1 * COST['pf'][1] + p12 * COST['pf'][2] + p12g * COST['pf'][3]
    claws_u = 160 * stored / 512                                     # 20 heads x 8 targets, each held by a stored lane with probability stored/512
    spur_u = 40 * empty / 512 + 40 * empty * 3 / 512                # empty lanes match only when w = 0 (normal pass) or w in {507, 508, 511}
    matches_u = claws_u + spur_u
    per_fix = COST['u'] + COST['upre'] + 20 * COST['head']
    per_var = Dm(5) / 512 * COST['strad'] + matches_u * (COST['event'] + COST['match'] + COST['notfull']) + claws_u * (pf_mean + q_pf * STEP3B_MAX)
    per_u = per_fix + per_var
    fixed = C_UNIT + COST['cv_begin'] + COST['reset'] * (NBK + 3) + COST['build'] * NC + COST['pad'] * 21
    umax = per_fix + COST['strad'] + 40 * COST['event'] + 560 * (COST['match'] + COST['notfull'] + sum(COST['pf']) + STEP3B_MAX)
    return dict(occ=stored / 7, stored=stored, claws_u=claws_u, spur_u=spur_u, pf_mean=pf_mean, q_pf=q_pf, p12g=p12g, per_u=per_u, per_fix=per_fix,
                per_var=per_var, umax=umax, fixed=fixed, wbar=fixed + Dm(2) ** LU * per_u, vmax=fixed + Dm(2) ** LU * umax, LU=LU, nc=nc)

def ledger(show=True, q3_log2=None, d_lb=None, succ='0.39', eps_log2=16):
    md = model()
    q3m = Dm(q3_log2 if q3_log2 is not None else Q3_MODEL)
    d = Dm(d_lb if d_lb is not None else (D_LB if D_LB is not None else 0))
    q3p1 = q3m + min(Dm(0), d)
    q3r = P2(q3p1) * Dm(2) ** 32 / 160
    claws_lb = md['claws_u']
    EX = Dm(2) ** md['LU'] * claws_lb * md['q_pf'] * q3r * (1 - Dm(2) ** -Dm(BONF))     # Lemma 5: the second-moment bound with the measured link rate (Section 8)
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
        print('model (2^23 buckets of 7 lanes, 2^27 candidates, 2^32 scan words per chaining value):')
        print('  stored lanes per bucket %.6f (occupancy %.6f)  claws per u %.6f  spurious matches per u %.3e' % (md['stored'], md['occ'], md['claws_u'], md['spur_u']))
        print('  per u: fixed %d (u %d + pre %d + 20 heads x %d) + straddle %.4f + matches %.6f x %d + claws x (post-filters %.4f + q_pf x %d) = %.4f' % (
            md['per_fix'], COST['u'], COST['upre'], COST['head'], Dm(5) / 512 * COST['strad'], md['claws_u'] + md['spur_u'],
            COST['event'] + COST['match'] + COST['notfull'], md['pf_mean'], STEP3B_MAX, md['per_u']))
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
EXP_NC, EXP_LU, EXP_TRIALS = 17, 11, 5
ROWS_LU, ROWS_TRIALS = 13, 4
def online_experiment(req):
    """the counted procedure on organizer-seeded first blocks (real compressions), reduced size: the full 2^23-bucket table with 2^17
    candidates of P (full scale 2^27; the buckets are sparse, so empty lanes produce spurious matches when w = 0 or w in {507, 508, 511}),
    2^11 scan words.  Every claw is checked against an independent sorted-array search, against the real E16 of member x (in S160) and the
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
        u0 = rng.u32(); st = run_cv(cv, EXP_LU, nc=EXP_NC, count=True, ref=True, collect=True, u0=u0, R=rng.u32() & OMASK)
        bad_e16 = bad_pf = 0
        for (a0, a1, u, fl) in st['allclaws']:
            wx, wy = pair_words(cv, a0, a1)
            bad_e16 += trace(cv, wx, 17)[1][16] not in S160_SET or wx[1] != u or not in_P(a0)
            bad_pf += pf_ref(cv, a0, a1) != fl
        md = model(EXP_NC, EXP_LU)
        if st['coll']:
            a0, a1, u, wx, wy = st['coll'][0]
            rec['message_a_hex'] = struct.pack('>32I', *(M0 + wx)).hex(); rec['message_b_hex'] = struct.pack('>32I', *(M0 + wy)).hex()
        rec['observations'] = dict(claws=st['claws'], reference_claws=st['refclaws'], distinct_pairs=len(set((a, b) for a, b, _, _ in st['allclaws'])),
                                   bad_e16=bad_e16, bad_postfilters=bad_pf, c1=st['passes'][0], c1c2=st['passes'][1], c1c2g=st['passes'][2],
                                   all4=st['passes'][3], step3b_accepts=len(st['coll']), stored_lanes=st['stored'],
                                   counted_ops=st['ops'], model_ops=int(md['wbar']), match_events=st['events'], spurious_matches=st['spurious'], straddle_words=st['strad'])
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
        u0 = rng.u32(); st = run_cv(cv, ROWS_LU, nc=EXP_NC, count=False, collect=True, u0=u0, R=rng.u32() & OMASK)
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
    bad = 0
    for _ in range(4000):                                       # the SWAR field test against the direct predicate, on random bucket words
        wa = rr.getrandbits(256); wb = rr.getrandbits(256); w = rr.choice([rr.getrandbits(9), 0, 506, 507, 508, 511, 5, 4])
        x = w | (w << 11); x |= x << 36; x |= x << 72; x |= x << 144; x &= LM7; C = K512 - x
        for strad in (0, 1):
            v = (wa & TM0) | ((wb << 11) & TM1); r = v + C; y = (r & M3FA) if strad else ((r ^ K512) & M3FA); z = ((y | G10) - L0) & G10
            got = {k for k in range(14) if not (z >> (LANE * (k // 2) + 10 + 11 * (k % 2))) & 1}
            want = set()
            for k in range(14):
                t = ((wa if k % 2 == 0 else wb) >> (LANE * (k // 2))) & 511; d = t + 512 - w
                if (d < 512 and (d & ~5) == 0) if strad else (d >= 512 and ((d - 512) & ~5) == 0): want.add(k)
            bad += got != want
    chk('5 the SWAR field test equals the direct predicate (4,000 random word pairs, both passes)', bad == 0)
    cv5 = [rr.getrandbits(32) for _ in range(8)]; st = run_cv(cv5, 12, nc=17, count=True, ref=True, collect=True)
    md = model(17, 12)
    chk('  run with 2^17 candidates in the 2^23-bucket table, 2^12 scan words: claws = reference search', st['claws'] == st['refclaws'], '(%d claws, %d stored lanes, %d spurious matches)' % (st['claws'], st['stored'], st['spurious']))
    chk('  claws distinct and every claw\'s real E16 in S160', len(set((a, b) for a, b, _, _ in st['allclaws'])) == st['claws'] and
        all(trace(cv5, pair_words(cv5, a, b)[0], 17)[1][16] in S160_SET and in_P(a) for a, b, _, _ in st['allclaws']))
    ratio = st['ops'] / float(md['wbar'])
    chk('  counted operations against the model mean (wbar at that size)', 0.9 < ratio < 1.1 and st['ops'] <= md['vmax'], '(counted %d, model %.0f, ratio %.4f)' % (st['ops'], md['wbar'], ratio))
    r = online_experiment(dict(experiment_id='p1b-online-r38', trials=[dict(trial=t, seed='%064x' % t) for t in (0, 1, EXP_TRIALS)]))
    obs = [t['observations'] for t in r['trials']]
    chk('6 organizer experiment p1b-online-r38 (3 trials): claws = reference, 0 bad E16, 0 bad post-filters, S pair accepted',
        all(o['claws'] == o['reference_claws'] and o['bad_e16'] == 0 and o['bad_postfilters'] == 0 for o in obs[:2]) and obs[2]['s_pair_step3b_accepts'] == 1, str(obs))
    lg = ledger(show=False)
    chk('7 ledger: success lower bound >= 0.39', Dm(lg['success_lb']) >= Dm('0.39'), '(time_log2 %.5f)' % lg['time_log2'])
    print('SELFTEST', 'PASSED' if ok else 'FAILED'); return ok

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'selftest': sys.exit(0 if selftest() else 1)
    if len(sys.argv) > 1 and sys.argv[1] == 'ledger': ledger(); sys.exit(0)
    sys.stdout.write(json.dumps(run_request(json.loads(sys.stdin.read())), separators=(',', ':')))
