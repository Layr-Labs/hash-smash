# a0p_ref.py - part 1 of experiments/a0p38.py: target, characteristic P8 and the reference construction of the A0-variant attack (own code).
# The attack design (A0-variants of one Step-1 solution, c7 classes decided by one W7 test, bit-sliced row-16 filter, accepted event with a
# direct output comparison) is that of the public packages 2d1c4fc2 (itseasypop) and fb176310 (Jbenisek) on the framework of ePrint
# 2026/1120 / 2026/1080; this code, the characteristic P8 and its accepted event (row 19 on signed differences) are ours.
import sys, json, hashlib, struct, zlib, base64, math
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

# ---- the characteristic P8 (proof.md Section 3); member x = M, member y = M'.  PCV/PMX/PMY: a 38-step semi-free-start pair in the accepted
# event whose rows 0..15 are the Step-1 solution S.  Cells per kind (A, E, W) and row: (mask, x-value, x^y difference, 0) = the signed trail with
# its one-bit conditions; PQ[i]: bits with E_i = E_{i-1}; X2: the other two-bit conditions (k1, i1, b1, equal, k2, i2, b2, row), member x.
_CH = [{7: (1610612736, 536870912, 1610612736, 0), 8: (4261904, 0, 4261904, 0), 10: (65552, 16, 65552, 0), 11: (134219780, 4, 134219780, 0), 12: (555746818, 555746818, 555746818, 0), 13: (536870912, 0, 536870912, 0), 14: (134348944, 0, 134348944, 0), 15: (42041344, 8454144, 42041344, 0), 17: (536870912, 536870912, 536870912, 0)}, {5: (536870912, 536870912, 0, 0), 6: (675811328, 4718592, 0, 0), 7: (3897036800, 3892318208, 3758096384, 0), 8: (3897301136, 3355707520, 676075664, 0), 9: (51380235, 0, 51380235, 0), 10: (1073807376, 1073741840, 1073807376, 0), 11: (612564992, 8519680, 612564992, 0), 12: (1763748865, 671121409, 1763748865, 0), 13: (4195046, 102, 4195046, 0), 14: (134348800, 134217728, 134348800, 0), 15: (2176, 128, 2176, 0), 16: (1212291712, 1208095232, 1078071808, 0), 17: (1078073984, 2048, 0, 0), 18: (1078333968, 4329984, 262160, 0), 19: (25460752, 32784, 25198592, 0), 20: (25460752, 262160, 0, 0), 21: (562069504, 553680896, 536870912, 0), 22: (536870912, 0, 0, 0), 23: (536870912, 536870912, 0, 0)}, {7: (536870912, 0, 536870912, 0), 8: (71305216, 71303168, 71305216, 0), 9: (536870912, 536870912, 536870912, 0), 10: (83956394, 67113504, 83956394, 0), 11: (527360, 524288, 527360, 0), 15: (71305216, 67108864, 71305216, 0), 16: (536870912, 536870912, 536870912, 0), 23: (25337856, 25165824, 25198592, 0), 25: (536870912, 0, 536870912, 0)}]
PQ = [0, 0, 0, 0, 0, 0, 3221225472, 264336, 0, 0, 0, 0, 0, 0, 0, 0, 0, 262160, 25198592, 0, 536870912, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
X2 = [(1, 16, 7, 1, 1, 16, 26, 16), (1, 16, 14, 0, 1, 16, 28, 16), (0, 15, 4, 1, 0, 16, 4, 16), (1, 16, 11, 1, 1, 16, 16, 16), (0, 15, 7, 1, 0, 16, 7, 16), (0, 14, 15, 1, 0, 16, 15, 16), (0, 14, 16, 1, 0, 16, 16, 16), (0, 15, 17, 1, 0, 16, 17, 16), (0, 14, 23, 1, 0, 16, 23, 16), (0, 14, 25, 1, 0, 16, 25, 16), (0, 15, 27, 1, 0, 16, 27, 16), (1, 16, 3, 0, 1, 16, 8, 16), (1, 16, 4, 1, 1, 16, 23, 16), (0, 17, 9, 0, 0, 17, 20, 17), (2, 16, 20, 0, 2, 16, 27, 16), (2, 16, 22, 1, 2, 16, 31, 16), (0, 16, 15, 1, 0, 17, 15, 17), (0, 17, 6, 1, 0, 17, 18, 17), (0, 16, 16, 0, 0, 17, 16, 17), (2, 16, 4, 0, 2, 16, 6, 16), (0, 16, 23, 1, 0, 17, 23, 17), (0, 16, 25, 1, 0, 17, 25, 17), (0, 17, 8, 0, 0, 17, 17, 17), (0, 15, 29, 1, 0, 16, 29, 16), (1, 18, 0, 1, 1, 18, 13, 18), (1, 18, 17, 1, 1, 18, 22, 18), (1, 18, 5, 0, 1, 18, 23, 18), (0, 16, 29, 1, 0, 18, 29, 18), (1, 18, 9, 1, 1, 18, 23, 18), (1, 19, 10, 1, 1, 19, 29, 19), (1, 19, 2, 0, 1, 19, 20, 19), (1, 19, 5, 0, 1, 19, 18, 19), (1, 19, 6, 1, 1, 19, 19, 19), (1, 19, 10, 0, 1, 19, 28, 19), (1, 19, 11, 1, 1, 19, 29, 19), (1, 19, 1, 1, 1, 19, 28, 19), (0, 18, 29, 1, 0, 19, 29, 19), (1, 19, 4, 0, 1, 19, 9, 19), (1, 19, 5, 0, 1, 19, 10, 19), (1, 21, 10, 1, 1, 21, 15, 21), (1, 21, 11, 1, 1, 21, 24, 21), (1, 21, 2, 1, 1, 21, 16, 21), (2, 23, 14, 0, 2, 23, 21, 23), (2, 23, 16, 0, 2, 23, 25, 23), (2, 23, 17, 0, 2, 23, 26, 23), (2, 23, 0, 1, 2, 23, 30, 23), (2, 23, 1, 1, 2, 23, 31, 23), (2, 25, 20, 1, 2, 25, 27, 25), (2, 25, 22, 0, 2, 25, 31, 25), (2, 25, 4, 1, 2, 25, 6, 25), (2, 16, 14, 1, 2, 16, 18, 16), (2, 16, 8, 1, 2, 16, 25, 16), (2, 16, 1, 0, 2, 16, 12, 16)]
GL = [549441552, 549441553, 549441556, 549441557, 549442576, 549442577, 549442580, 549442581, 1891627024, 1891627025, 1891627028, 1891627029, 1891628048, 1891628049, 1891628052, 1891628053, 2698498064, 2698498065, 2698498068, 2698498069, 2698499088, 2698499089, 2698499092, 2698499093, 2699022352, 2699022353, 2699022356, 2699022357, 2699023376, 2699023377, 2699023380, 2699023381, 2700595216, 2700595217, 2700595220, 2700595221, 2700596240, 2700596241, 2700596244, 2700596245, 3988787216, 3988787217, 3988787220, 3988787221, 3988788240, 3988788241, 3988788244, 3988788245, 3989303312, 3989303313, 3989303316, 3989303317, 3989304336, 3989304337, 3989304340, 3989304341, 3989311504, 3989311505, 3989311508, 3989311509, 3989312528, 3989312529, 3989312532, 3989312533, 3989827600, 3989827601, 3989827604, 3989827605, 3989828624, 3989828625, 3989828628, 3989828629, 3990884368, 3990884369, 3990884372, 3990884373, 3990885392, 3990885393, 3990885396, 3990885397, 3991400464, 3991400465, 3991400468, 3991400469, 3991401488, 3991401489, 3991401492, 3991401493, 3991408656, 3991408657, 3991408660, 3991408661, 3991409680, 3991409681, 3991409684, 3991409685, 3991924752, 3991924753, 3991924756, 3991924757, 3991925776, 3991925777, 3991925780, 3991925781, 4040167440, 4040167441, 4040167444, 4040167445, 4040168464, 4040168465, 4040168468, 4040168469, 4040683536, 4040683537, 4040683540, 4040683541, 4040684560, 4040684561, 4040684564, 4040684565, 4040691728, 4040691729, 4040691732, 4040691733, 4040692752, 4040692753, 4040692756, 4040692757, 4041207824, 4041207825, 4041207828, 4041207829, 4041208848, 4041208849, 4041208852, 4041208853, 4042264592, 4042264593, 4042264596, 4042264597, 4042265616, 4042265617, 4042265620, 4042265621, 4042780688, 4042780689, 4042780692, 4042780693, 4042781712, 4042781713, 4042781716, 4042781717, 4042788880, 4042788881, 4042788884, 4042788885, 4042789904, 4042789905, 4042789908, 4042789909]
PCV = [2510440793, 3020242837, 468731710, 514538364, 1695310803, 3863559483, 3976220445, 3950947027]
PMX = [3171188373, 499730577, 1270760843, 3353099274, 2338469345, 2641768686, 1453171616, 2497556930, 1179538525, 2818885938, 2901196405, 3358065010, 2588764008, 370382130, 3758975641, 1605534331]
PMY = [3171188373, 499730577, 1270760843, 3353099274, 2338469345, 2641768686, 1453171616, 3034427842, 1108237405, 2282015026, 2850925791, 3357543794, 2588764008, 370382130, 3758975641, 1542621819]
A0S = 0xc500a7ff
MASK = 0x7fe96c7c
VS_B64 = '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'
CLASSES = [(0x2a7beb1b, 0x9b649791), (0x2a7bfb1b, 0x9b648791), (0x2a7feb1b, 0x9b609793), (0x2a7ffb1b, 0x9b608793), (0xaa7beb1b, 0x1b649791), (0xaa7bfb1b, 0x1b648791), (0xaa7feb1b, 0x1b609793), (0xaa7ffb1b, 0x1b608793)]
CELLS = [[(0, 0, 0, 0)] * NR for _ in range(3)]
for _k in range(3):
    for _i, _c in _CH[_k].items(): CELLS[_k][_i] = _c
_tx, _ty = trace(PCV, PMX), trace(PCV, PMY)
SAx = {i: _tx[0][i] for i in range(-4, 16)}; SEx = {i: _tx[1][i] for i in range(-4, 16)}
SAy = {i: _ty[0][i] for i in range(-4, 16)}; SEy = {i: _ty[1][i] for i in range(-4, 16)}
DWT = [(_ty[2][i] - _tx[2][i]) & M for i in range(NR)]          # modular differences of the words (y - x) of the pair
D7 = DWT[7]; T7 = 0x03bff800                                   # s0(W7y) - s0(W7x) required by rows 22/23 (the trail)
def inF7(w): return ((s0((w + D7) & M) - s0(w)) & M) == T7
R19 = 19                                                         # the row checked on its signed differences only (accepted event)

def rowok(tx, ty, i, relax=True):
    """Row i of both traces: cells (x-value on the mask, XOR difference), '+' pairs and two-bit conditions keyed at row i (member x).
    The W cells of rows 7..10 are not part of the event (W7: F7; W8..W10: modular differences).  With relax, row R19 is checked on its
    signed differences only (XOR difference and member-x value on the difference bits)."""
    (Ax, Ex, Wx), (Ay, Ey, Wy) = tx, ty
    sig = relax and i == R19
    for k, (x, y) in enumerate(((Ax[i], Ay[i]), (Ex[i], Ey[i]), (Wx[i], Wy[i]))):
        if k == 2 and 7 <= i <= 10: continue
        m, v, d, _ = CELLS[k][i]
        if (x ^ y) != d: return False
        if (x & (d if sig else m)) != (v & (d if sig else m)): return False
    if sig: return True
    if (Ex[i] ^ Ex[i-1]) & PQ[i]: return False
    for (k1, i1, b1, eq, k2, i2, b2, row) in X2:
        if row == i and (((tx[k1][i1] >> b1) ^ (tx[k2][i2] >> b2)) & 1) != (0 if eq else 1): return False
    return True

def accepted(tx, ty):
    """The accepted event: rows 16..22 (row 19 on signed differences) and equal outputs after step 37."""
    return all(rowok(tx, ty, i) for i in range(16, 23)) and all(tx[k][i] == ty[k][i] for k in (0, 1) for i in range(34, 38))

# ---- A0-variants (proof.md Section 4) ----
C4 = (SAx[4] - S0(SAx[3]) - MAJ(SAx[3], SAx[2], SAx[1])) & M                                    # E4 = a0 + C4 (both members)
W8C = [(E[8] - A[4] - S1(E[7]) - CH(E[7], E[6], E[5]) - K[8]) & M for A, E in ((SAx, SEx), (SAy, SEy))]   # W8 = W8C - E4
D8 = DWT[8]; DS8 = (s0(PMY[8]) - s0(PMX[8])) & M
def in_G(a0):
    e4 = (a0 + C4) & M; x = (W8C[0] - e4) & M; y = (W8C[1] - e4) & M
    return ((y - x) & M) == D8 and ((s0(y) - s0(x)) & M) == DS8
def c7of(a0):
    """W7x = c7(a0) - A_{-1}."""
    return (SEx[7] - 2 * SAx[3] + S0(SAx[2]) + MAJ(SAx[2], SAx[1], a0) - S1(SEx[6]) - CH(SEx[6], SEx[5], (a0 + C4) & M) - K[7]) & M
def words(cv, a0):
    """Step 2: the message words W0..W15 of both members connecting cv to the variant a0 of S."""
    out = []
    for SA, SE, wp in ((SAx, SEx, PMX), (SAy, SEy, PMY)):
        A = dict(SA); E = dict(SE); A[0] = a0
        for j in range(4): A[-1-j] = cv[j]; E[-1-j] = cv[4+j]
        for i in range(5): E[i] = (A[i] + A[i-4] - S0(A[i-1]) - MAJ(A[i-1], A[i-2], A[i-3])) & M
        w = [(E[i] - A[i-4] - E[i-4] - S1(E[i-1]) - CH(E[i-1], E[i-2], E[i-3]) - K[i]) & M for i in range(9)]
        out.append(w + list(wp[9:16]))
    return out
def e16x(cv, a0): return trace(cv, words(cv, a0)[0], 17)[1][16]
C16 = (SAx[12] + SEx[12] + S1(SEx[15]) + CH(SEx[15], SEx[14], SEx[13]) + K[16]) & M
R16 = sorted((C16 + g) & M for g in GL)                          # the E16x values with row 16 holding (exhaustive, 160 words)
R16SET = frozenset(R16)
_sh = M
for _v in R16: _sh &= ~(_v ^ R16[0]) & M
SHARED = _sh                                                       # bits on which all row-16 words agree
TK = 12                                                            # tested bits of the row-16 filter: the TK lowest shared bits
TBITS = [j for j in range(32) if (SHARED >> j) & 1][:TK]

# ---- classes (proof.md Section 5): class i = {base ^ s : s subset of MASK, a0 in G, c7(a0) = c7_i}, 24,576 variants each ----
def dep(t, mask):
    """bits of t deposited on the set bits of mask (lowest first)"""
    r = 0; j = 0
    while mask:
        b = mask & -mask
        if (t >> j) & 1: r |= b
        mask ^= b; j += 1
    return r
def members(ci, count, start=0):
    """the members number start..start+count-1 of class ci in the canonical order (increasing t of base ^ dep(t, MASK))"""
    c7, base = CLASSES[ci]; out = []; t = 0; k = 0
    while len(out) < count and t < (1 << bin(MASK).count('1')):
        a0 = base ^ dep(t, MASK); t += 1
        if in_G(a0) and c7of(a0) == c7:
            if k >= start: out.append(a0)
            k += 1
    return out

def rebuild(W, a0):
    """A success of the estimator (member-x words W[7..22] with W7 in F7, rows 16..22 sampled) and its variant a0 -> (cv, Mx, My):
    W0..W6 by the inverse expansion, CV1 by inverting steps 7..0 of the variant."""
    W = dict(W)
    for i in range(22, 15, -1): W[i - 16] = (W[i] - s1(W[i - 2]) - W[i - 7] - s0(W[i - 15])) & M
    A = {i: SAx[i] for i in range(8)}; A[0] = a0; E = {i: SEx[i] for i in range(4, 8)}; E[4] = (a0 + C4) & M
    for i in range(7, -1, -1):
        A[i - 4] = (E[i] - A[i] + S0(A[i - 1]) + MAJ(A[i - 1], A[i - 2], A[i - 3])) & M
        E[i - 4] = (E[i] - A[i - 4] - S1(E[i - 1]) - CH(E[i - 1], E[i - 2], E[i - 3]) - K[i] - W[i]) & M
    cv = [A[-1], A[-2], A[-3], A[-4], E[-1], E[-2], E[-3], E[-4]]
    wx, wy = words(cv, a0)
    return cv, wx, wy

# ---- the bit-sliced row-16 program (proof.md Section 7.2) ----
# Bit L of every 256-bit plane belongs to lane L (one variant).  The program computes, for 256 variants of one batch, the TK tested bits of
# E16x = KP + a0 + s0(W1), W1 = K1 - S0(a0) - MAJ(a0, a, b) - S1(E0) - CH(E0, e, f), E0 = a0 + HH (Lemma 4.1), and their AND with the
# tested values.  Inputs: the planes of the bits of a0 that vary in the batch (A<j>), the class constants (C<j>, broadcast words), and the
# per-first-block broadcast planes of HH, PP = a & b, QQ = a | b, EF = e ^ f, FF = f, K1 = A1 - g - K1, KP (7 x 32).  Constant bits of a0 are
# folded.  Nodes: xor, and, or, not; equal nodes are shared.  The allocator gives an instruction list over 64 registers in which every
# load, store and spill is one instruction; the list is the charge.
ONES = (1 << 256) - 1
class Prog:
    def __init__(s): s.nodes = [None, None]; s.cache = {}; s.inputs = {}
    def inp(s, name):
        if name not in s.inputs: s.nodes.append(('in', name)); s.inputs[name] = len(s.nodes) - 1
        return s.inputs[name]
    def _mk(s, op, a, b=None):
        key = (op, a, b) if op == 'not' or b is None else (op,) + tuple(sorted((a, b)))
        if key not in s.cache: s.nodes.append(key); s.cache[key] = len(s.nodes) - 1
        return s.cache[key]
    def not_(s, a):
        if a < 2: return 1 - a
        n = s.nodes[a]
        return n[1] if n[0] == 'not' else s._mk('not', a)
    def xor(s, a, b):
        if a == 0: return b
        if b == 0: return a
        if a == b: return 0
        if a == 1: return s.not_(b)
        if b == 1: return s.not_(a)
        return s._mk('xor', a, b)
    def and_(s, a, b):
        if a == 0 or b == 0: return 0
        if a == 1: return b
        if b == 1 or a == b: return a
        return s._mk('and', a, b)
    def or_(s, a, b):
        if a == 1 or b == 1: return 1
        if a == 0: return b
        if b == 0 or a == b: return a
        return s._mk('or', a, b)
    def add(s, x, y, cin=0, n=32):
        """ripple addition of two bit lists (LSB first), n result bits"""
        out = []; c = cin
        for j in range(n):
            t = s.xor(x[j], y[j]); out.append(s.xor(t, c))
            c = s.or_(s.and_(x[j], y[j]), s.and_(c, t))
        return out

def build_e16(cbits, nlane):
    """cbits[j]: 'L' (lane-varying bit of a0), 'C' (class constant, input), 0 or 1 (folded).  Returns (Prog, ok node)."""
    p = Prog()
    a0 = [p.inp('A%d' % j) if cbits[j] == 'L' else p.inp('C%d' % j) if cbits[j] == 'C' else cbits[j] for j in range(32)]
    bc = lambda nm: [p.inp('%s%d' % (nm, j)) for j in range(32)]
    HH, PP, QQ, EF, FF, K1, KP = (bc(n) for n in ('HH', 'PP', 'QQ', 'EF', 'FF', 'K1', 'KP'))
    rot = lambda w, r: [w[(j + r) % 32] for j in range(32)]
    x3 = lambda u, v, w: [p.xor(p.xor(u[j], v[j]), w[j]) for j in range(32)]
    E0 = p.add(a0, HH)
    # bit-interleaved: at bit j the four operands of T = S0(a0) + MAJ + S1(E0) + CH, the three adders of T and the subtraction K1 - T
    c = [0, 0, 0, 1]; T1 = []; W1 = []
    def fa(x, y, ci):
        t = p.xor(x, y); return p.xor(t, ci), p.or_(p.and_(x, y), p.and_(ci, t))
    for j in range(32):
        sa = p.xor(p.xor(a0[(j + 2) % 32], a0[(j + 13) % 32]), a0[(j + 22) % 32])
        mj = p.or_(PP[j], p.and_(a0[j], QQ[j]))
        ss = p.xor(p.xor(E0[(j + 6) % 32], E0[(j + 11) % 32]), E0[(j + 25) % 32])
        cv = p.xor(FF[j], p.and_(E0[j], EF[j]))
        u, c[0] = fa(sa, mj, c[0]); v, c[1] = fa(ss, cv, c[1]); t, c[2] = fa(u, v, c[2])
        w, c[3] = fa(K1[j], p.not_(t), c[3]); W1.append(w)
    n = max(TBITS) + 1; d = [0, 0]; ok = 1
    for j in range(n):
        s0w = p.xor(p.xor(W1[(j + 7) % 32], W1[(j + 18) % 32]), W1[j + 3] if j + 3 < 32 else 0)
        u, d[0] = fa(KP[j], a0[j], d[0]); e, d[1] = fa(u, s0w, d[1])
        if j in TBITS: ok = p.and_(ok, e if (R16[0] >> j) & 1 else p.not_(e))
    return p, ok

def schedule(p, root, nreg=64):
    """Belady allocation of the nodes root depends on, in creation order: instruction list [(op, dst, src...)] with 'ld' (input or spill
    slot), 'st' (spill), 'xor', 'and', 'or', 'not', 'out'; returns (instructions, spill slots used)."""
    need = set(); st = [root]
    while st:
        x = st.pop()
        if x < 2 or x in need: continue
        need.add(x); n = p.nodes[x]
        if n[0] != 'in': st.extend(n[1:] if n[0] != 'not' else n[1:2])
    order = [x for x in range(2, len(p.nodes)) if x in need and p.nodes[x][0] != 'in']
    uses = {}
    for t, x in enumerate(order):
        n = p.nodes[x]
        for o in (n[1:] if n[0] != 'not' else n[1:2]):
            if o >= 2: uses.setdefault(o, []).append(t)
    uses.setdefault(root, []).append(len(order))
    ptr = {x: 0 for x in uses}
    def nxt(x):
        u = uses.get(x, []); i = ptr.get(x, 0)
        return u[i] if i < len(u) else 1 << 40
    reg = {}; free = list(range(nreg)); inmem = set(x for x in need if p.nodes[x][0] == 'in'); slots = {}; ins = []; maxslot = 0
    def evict(t, keep):
        nonlocal maxslot
        v = max((x for x in reg if x not in keep), key=nxt)
        if nxt(v) < (1 << 40) and v not in inmem:
            if v not in slots: slots[v] = len(slots); maxslot = max(maxslot, len(slots))
            ins.append(('st', ('S', slots[v]), reg[v])); inmem.add(v)
        free.append(reg.pop(v))
    def getreg(t, keep):
        if not free: evict(t, keep)
        return free.pop()
    def load(x, t, keep):
        if x in reg: return reg[x]
        r = getreg(t, keep); src = ('I', p.nodes[x][1]) if p.nodes[x][0] == 'in' else ('S', slots[x])
        ins.append(('ld', r, src)); reg[x] = r; return r
    CONST = {0: 'Z', 1: 'O'}
    for t, x in enumerate(order):
        n = p.nodes[x]; ops = n[1:] if n[0] != 'not' else n[1:2]
        keep = set(o for o in ops if o >= 2)
        rs = []
        for o in ops:
            if o < 2: rs.append(CONST[o])
            else: rs.append(load(o, t, keep))
        for o in ops:
            if o >= 2: ptr[o] += 1
        dead = [o for o in ops if o >= 2 and nxt(o) >= (1 << 40) and o in reg]
        if dead: r = reg.pop(dead[0]); [free.append(reg.pop(d)) for d in dead[1:] if d in reg]
        else: r = getreg(t, keep)
        ins.append((n[0], r) + tuple(rs)); reg[x] = r
    ins.append(('out', reg[root] if root >= 2 else CONST[root]))
    return ins, maxslot

def run_prog(ins, inputs):
    """execute an instruction list on 256-bit planes; inputs: name -> plane.  Returns (ok plane, executed instructions)."""
    R = {}; S = {}; v = lambda a: 0 if a == 'Z' else ONES if a == 'O' else R[a]
    for i in ins:
        op = i[0]
        if op == 'ld': R[i[1]] = inputs[i[2][1]] if i[2][0] == 'I' else S[i[2][1]]
        elif op == 'st': S[i[1][1]] = R[i[2]]
        elif op == 'xor': R[i[1]] = v(i[2]) ^ v(i[3])
        elif op == 'and': R[i[1]] = v(i[2]) & v(i[3])
        elif op == 'or': R[i[1]] = v(i[2]) | v(i[3])
        elif op == 'not': R[i[1]] = v(i[2]) ^ ONES
        elif op == 'out': return v(i[1]), len(ins) - 1
    raise ValueError('no out')

# ---- counted scalar routines (proof.md Section 7.1) ----
# Machine: 256-bit word RAM; every executed primitive counts 1 (add, sub, and, or, xor, not, shl, shr, ld, st, li, rand), a compare-and-branch
# counts 2, one target compression counts 1 unit.  32-bit values are reduced with one AND where the program needs a masked value.  The
# routines below are written with the counting primitives of Mach and executed; broadcast, lane_value, first_lane, r16test, step_m and deep add
# itemised declared counts (stated in their docstrings) instead of counting each primitive (the `calibrate` command).
class Mach:
    def __init__(s): s.ops = 0; s.units = 0
    def op(s, v, n=1): s.ops += n; return v
    def add(s, a, b): return s.op((a + b) & M)
    def sub(s, a, b): return s.op((a - b) & M)
    def xor(s, a, b): return s.op(a ^ b)
    def and_(s, a, b): return s.op(a & b)
    def or_(s, a, b): return s.op(a | b)
    def shr(s, a, n): return s.op(a >> n)
    def ld(s, v): return s.op(v)
    def br(s, c): s.ops += 2; return c
def sg(m, x, r1, r2, r3, shr3):
    """ROTR(x,r1) ^ ROTR(x,r2) ^ (SHR or ROTR)(x,r3) of a masked 32-bit x: the doubled word D = x | x << 32 makes a rotation one shift; 8 ops"""
    m.op(0, 2)                                                       # D = x << 32, D |= x
    t = m.op(ror(x, r1) ^ ror(x, r2), 3); u = m.op((x >> r3) if shr3 else ror(x, r3), 1); return m.op((t ^ u) & M, 2)
def S0m(m, x): return sg(m, x, 2, 13, 22, False)
def S1m(m, x): return sg(m, x, 6, 11, 25, False)
def s0m(m, x): return sg(m, x, 7, 18, 3, True)
def s1m(m, x): return sg(m, x, 17, 19, 10, True)
def CHm(m, e, f, g): return m.xor(g, m.and_(e, m.xor(f, g)))                    # 3
def MAJm(m, a, b, c): return m.or_(m.and_(a, b), m.and_(c, m.or_(a, b)))       # 4

def w7test(m, c7, a):
    """W7 = c7 - A_{-1} in F7, computed (no table): s0(w + D7) - s0(w) = T7; 24 operations including the branch"""
    w = m.and_(m.sub(c7, a), M); w2 = m.and_(m.add(w, D7), M)
    d = m.and_(m.sub(s0m(m, w2), s0m(m, w)), M)
    return m.br(d == T7)

def fb_scalars(m, cv):
    """per first block: HH, PP, QQ, EF, FF, K1, KP of the program (Lemma 4.1) and A1-independent words"""
    a, b, c, d, e, f, g, h = cv
    hh = m.and_(m.sub(m.sub(d, S0m(m, a)), MAJm(m, a, b, c)), M)
    kw0 = m.and_(m.sub(m.sub(m.sub(m.sub(m.sub(hh, d), h), S1m(m, e)), CHm(m, e, f, g)), K[0]), M)
    sc = dict(HH=hh, PP=m.and_(a, b), QQ=m.or_(a, b), EF=m.xor(e, f), FF=f, K1=m.and_(m.sub(KK1, g), M), KP=m.and_(m.add(KKP, kw0), M))
    return sc
KK1 = (SAx[1] - K[1]) & M                                          # K1 = A1 - g - K1
KKP = (C16 + s1(PMX[14]) + PMX[9]) & M                            # KP = C16 + s1(W14) + W9 + (W0 - a0)
PLANE_OPS = 4                                                       # one broadcast plane: shift, and, negate, store

def broadcast(m, sc):
    """the 7 x 32 broadcast planes (plane j = 0 - ((x >> j) & 1)); 4 operations each"""
    out = {}
    for nm, v in sc.items():
        for j in range(32): out['%s%d' % (nm, j)] = ONES if (v >> j) & 1 else 0
    m.ops += PLANE_OPS * 32 * len(sc); return out

def lane_value(m, planes, L, cmask, base):
    """a0 of lane L from the stored planes of the varying bits: per bit one shift, and, shift-left, or (4), plus the class base (1)"""
    v = base
    for j in range(32):
        if (cmask >> j) & 1:
            v |= ((planes[j] >> L) & 1) << j
    m.ops += 4 * bin(cmask).count('1') + 1; return v

def first_lane(m, ok):
    """lowest set lane of a nonzero 256-bit word: binary search, 8 steps of (and, compare-and-branch, shift) = 32 operations"""
    m.ops += 32; return (ok & -ok).bit_length() - 1

def scalar_e16(m, sc, a0):
    """E16x of one variant (Lemma 4.1): E0, S0(a0), MAJ, S1(E0), CH, W1, s0(W1), E16x"""
    e0 = m.and_(m.add(a0, sc['HH']), M)
    mj = m.or_(sc['PP'], m.and_(a0, sc['QQ']))
    ch = m.xor(sc['FF'], m.and_(e0, sc['EF']))
    w1 = m.and_(m.sub(m.sub(m.sub(m.sub(sc['K1'], S0m(m, a0)), mj), S1m(m, e0)), ch), M)
    return m.and_(m.add(m.add(sc['KP'], a0), s0m(m, w1)), M)

def r16test(m, e):
    """E16x in the 160-word row-16 set: binary search in the sorted table (8 steps of load, compare-and-branch, shift: 5 each) + 2"""
    m.ops += 8 * 5 + 2; return e in R16SET

def step_m(m, A, E, W, i):
    """one step of one member: 2 sigma (16), CH 3, MAJ 4, 9 additions/subtractions, 2 masks"""
    m.ops += 16 + 3 + 4 + 9 + 2
    E[i] = (A[i-4] + E[i-4] + S1(E[i-1]) + CH(E[i-1], E[i-2], E[i-3]) + K[i] + W[i]) & M
    A[i] = (E[i] - A[i-4] + S0(A[i-1]) + MAJ(A[i-1], A[i-2], A[i-3])) & M

def rowtest_m(m, tx, ty, i):
    """the accepted tests of row i (Section 6): per word (A, E, W) one xor and compare-and-branch for the difference and one and +
    compare-and-branch for the x-value bits (6 each, 18), the '+' pair (xor, and, branch: 4), per two-bit condition (2 shifts, xor, and,
    branch: 6)"""
    m.ops += 18 + (4 if PQ[i] and i != R19 else 0) + (6 * sum(1 for x in X2 if x[7] == i) if i != R19 else 0)
    return rowok(tx, ty, i)

def deep(m, cv, a0):
    """a row-16 pass: the words of both members (Step 2: 5 E words and 9 W words each, 13 operations per word), the expansion W16..W37
    (s0, s1, 3 additions, mask: 20 each), rows 16..37 of both members with the tests of rows 16..22 (early abort), the output comparison
    (8 xor, 7 or, branch).  Returns True iff the pair is in the accepted event."""
    wx, wy = words(cv, a0); m.ops += 2 * 14 * 13
    tx = trace(cv, wx); ty = trace(cv, wy)
    for i in range(16, 38):
        m.ops += 2 * 20 + 2 * 34
        if i <= 22 and not rowtest_m(m, tx, ty, i): return False
    m.ops += 8 + 7 + 2
    return all(tx[k][i] == ty[k][i] for k in (0, 1) for i in range(34, 38))

# ---- the online algorithm on one first block (proof.md Section 6) ----
CBITS = ['L' if (MASK >> j) & 1 else 'C' if ((CLASSES[0][1] ^ CLASSES[-1][1] | CLASSES[1][1] ^ CLASSES[2][1] | 0x80041002) >> j) & 1 and not (MASK >> j) & 1 else (CLASSES[0][1] >> j) & 1 for j in range(32)]
_PROG = {}
def program():
    if 'p' not in _PROG:
        p, ok = build_e16(CBITS, 256); _PROG['p'] = schedule(p, ok)[0]
    return _PROG['p']
BATCH_CTL = 6          # per batch: ok test (compare-and-branch 2) and pointer advance, compare and branch (4)
CLASS_CTL = 3 + 4      # per passing class: setup 3 (batch pointer, end pointer, class constants) and end of class (work counter, cap test) 4
LANE_CTL = 3           # per passing lane: clear the lane (xor) and the loop test (compare-and-branch)
FB_FIXED = 30 + 5      # per first block: two random words and their 16 fields (30), counter, cap test and hit-list test (5)
W7_LOOP = 4            # per class: load c7, advance the class pointer, compare and branch

def batch_planes(mem):
    """the stored planes of a batch: plane j = bits j of the 256 variants (lane L = variant L)"""
    return {j: sum(((x >> j) & 1) << L for L, x in enumerate(mem)) for j in range(32)}

def process_batch(m, ins, inp, planes, ci, cv, sc, found):
    """one batch of one passing class: the plane program, then every passing lane in scalar form; row-16 passes go to the deep check"""
    for j in range(32):
        if CBITS[j] == 'L': inp['A%d' % j] = planes[j]
        elif CBITS[j] == 'C': inp['C%d' % j] = ONES if (CLASSES[ci][1] >> j) & 1 else 0
    ok, n = run_prog(ins, inp); m.ops += n + BATCH_CTL
    while ok:
        L = first_lane(m, ok); ok &= ok - 1; m.ops += LANE_CTL
        a0 = lane_value(m, planes, L, MASK, CLASSES[ci][1] & ~MASK & M)
        e = scalar_e16(m, sc, a0)
        if r16test(m, e) and deep(m, cv, a0): found.append(a0)
    return found

def process_fb(m, cv, batches_of, check=None):
    """one first block with chaining value cv: the W7 tests of all classes; for each passing class all its batches (batches_of(ci) yields
    the member lists).  Returns the accepted variants found.  check(ci, mem, ok-plane-recomputation) may verify lanes."""
    m.ops += FB_FIXED
    hits = []
    for ci, (c7, base) in enumerate(CLASSES):
        m.ops += W7_LOOP
        if w7test(m, c7, cv[0]): hits.append(ci); m.ops += 2
    found = []
    if not hits: return found, hits
    sc = fb_scalars(m, cv); inp = broadcast(m, sc); ins = program()
    for ci in hits:
        m.ops += CLASS_CTL
        for mem in batches_of(ci):
            process_batch(m, ins, inp, batch_planes(mem), ci, cv, sc, found)
    return found, hits

# ---- organizer experiments (proof.md Section 13).  Randomness: SHAKE-256 of (experiment id | trial seed) ----
class Shake:
    def __init__(self, seed): self.seed = seed.encode(); self.k = 0; self.buf = b''; self.pos = 0
    def word(self):
        if self.pos + 32 > len(self.buf):
            self.buf = hashlib.shake_256(self.seed + b'|' + str(self.k).encode()).digest(1 << 14); self.k += 1; self.pos = 0
        v = int.from_bytes(self.buf[self.pos:self.pos + 32], 'little'); self.pos += 32; return v
    def u32(self): return self.word() & M
    def below(self, n): return self.word() % n

def vsample():
    return list(struct.unpack('<512I', zlib.decompress(base64.b64decode(VS_B64))))

def f7_sample(rng):
    """W7 uniform on F7 = {w : s0(w + D7) - s0(w) = T7} via its three affine families (2^28, 2^24 and 2^21 words; proof.md 5.1)"""
    w = rng.u32(); r = (w >> 4) % 274                                 # family by its share 256, 16, 2 of 274
    b = lambda x, j: (x >> j) & 1
    def setb(x, j, v): return (x & ~(1 << j)) | (v << j)
    if r < 256: w = setb(w, 29, 0)
    elif r < 272: w = setb(setb(w, 29, 1), 30, 0)
    else: w = setb(setb(w, 29, 1), 30, 1)
    w = setb(w, 18, b(w, 14) ^ 1); w = setb(w, 25, b(w, 8) ^ 1); w = setb(w, 12, b(w, 1))
    if r >= 256:
        w = setb(w, 19, b(w, 15) ^ 1); w = setb(w, 26, b(w, 9) ^ 1); w = setb(w, 13, b(w, 2))
    if r >= 272:
        w = setb(w, 20, b(w, 16) ^ b(w, 31) ^ 1); w = setb(w, 27, b(w, 10) ^ b(w, 31) ^ 1); w = setb(w, 14, b(w, 3) ^ b(w, 31))
        w = setb(w, 18, b(w, 14) ^ 1)
    return w

def step_row(A, E, W, i):
    E[i] = (A[i-4] + E[i-4] + S1(E[i-1]) + CH(E[i-1], E[i-2], E[i-3]) + K[i] + W[i]) & M
    A[i] = (E[i] - A[i-4] + S0(A[i-1]) + MAJ(A[i-1], A[i-2], A[i-3])) & M

def erow_plan(i, cm, pq):
    """bits of E_i imposed on a row-i proposal: x-value cells, '+' pairs, two-bit conditions with an earlier E row (prev) and inside E_i
    (inner), each imposed once from a bit fixed before it (as in vt38n.py)"""
    imp = cm | pq; prev = []; inner = []
    for (k1, i1, b1, eq, k2, i2, b2, row) in X2:
        if row != i or k1 != 1 or k2 != 1 or i2 != i: continue
        fl = 0 if eq else 1
        if i1 < i:
            if not (imp >> b2) & 1: prev.append((i1, b1, b2, fl)); imp |= 1 << b2
        elif not (imp >> b2) & 1: inner.append((b1, b2, fl)); imp |= 1 << b2
        elif not (imp >> b1) & 1: inner.append((b2, b1, fl)); imp |= 1 << b1
    done = cm | pq | sum(1 << b2 for (_, _, b2, _) in prev); out = []; todo = list(inner)
    while todo:
        nx = [t for t in todo if (done >> t[0]) & 1 or not any(u[1] == t[0] for u in todo)]
        if not nx: imp &= ~sum(1 << t[1] for t in todo); break
        for t in nx: out.append(t); done |= 1 << t[1]; todo.remove(t)
    return imp, prev, out

NP_R, CH_R, NT_R = 64, (64, 8, 8, 4, 2, 1), 192
P19F = 1 << 18; P19A = ((10, 28), (11, 29)); P19B = ((5, 10),)   # the row-19 pattern flips: A = E19[18], conditions 6 and 7; B = condition 11
def smc_replicate(rng, VS):
    """one replicate of the estimator of q3 for the accepted event: row 16 exact (the 160 W16 words), rows 17..22 by proposals of E_i^x
    with the row's E bits imposed (row 19: only its difference bits), tail: a variant of the sample, W7 uniform in F7, rows 23..37,
    output comparison.  Returns (log2 estimate or None, accepted pairs, failed rebuilds)."""
    lg = [math.log2(len(GL)) - 32]; P = []
    for _ in range(NP_R):
        w = GL[rng.below(len(GL))]; st = []
        for (SA, SE, wp, dw) in ((SAx, SEx, PMX, 0), (SAy, SEy, PMY, DWT[16])):
            A = dict(SA); E = dict(SE); W = {i: wp[i] for i in range(16)}; W[16] = (w + dw) & M; step_row(A, E, W, 16); st += [A, E, W]
        P.append(st)
    for i in range(17, 23):
        cm, cvv, d, _ = CELLS[1][i]; pq = PQ[i] & ~cm
        imp, prev, inner = erow_plan(i, cm, pq); f = bin(imp).count('1'); Mi = CH_R[i - 17]; surv = []
        if i == R19:                     # one of the four row-19 patterns (proof.md 6.1), drawn uniformly: weight 4 x 2^-f
            f -= 2; inners = []
            for fa, fb in ((0, 0), (0, 1), (1, 0), (1, 1)):
                fl = {(b1, b2) for b1, b2 in (P19A if fa else ()) + (P19B if fb else ())}
                inners.append(([(bs, bd, x ^ ((bs, bd) in fl or (bd, bs) in fl)) for (bs, bd, x) in inner], cvv ^ (P19F if fa else 0)))
        for (Ax, Ex, Wx, Ay, Ey, Wy) in P:
            rx = (Ax[i-4] + Ex[i-4] + S1(Ex[i-1]) + CH(Ex[i-1], Ex[i-2], Ex[i-3]) + K[i]) & M
            for _ in range(Mi):
                inn, cv0 = inners[rng.below(4)] if i == R19 else (inner, cvv)
                fixed = cv0 | (Ex[i-1] & pq)
                for (i1, b1, b2, fl) in prev: fixed |= (((Ex[i1] >> b1) & 1) ^ fl) << b2
                e = (rng.u32() & ~imp & M) | fixed
                for (bs, bd, fl) in inn: e = (e & ~(1 << bd)) | (((e >> bs) & 1) ^ fl) << bd
                Wxi = (e - rx) & M
                nA = dict(Ax); nE = dict(Ex); nW = dict(Wx); mA = dict(Ay); mE = dict(Ey); mW = dict(Wy)
                nW[i] = Wxi                                          # W_i^y = W_i^x + the schedule difference (W0..W6 carry none)
                mW[i] = (Wxi + s1(mW[i-2]) - s1(nW[i-2]) + mW[i-7] - nW[i-7] + (T7 if i == 22 else s0(mW[i-15]) - s0(nW[i-15]))) & M
                step_row(nA, nE, nW, i); step_row(mA, mE, mW, i)
                if nE[i] == e and rowok((nA, nE, nW), (mA, mE, mW), i): surv.append((nA, nE, nW, mA, mE, mW))
        if not surv: return None, [], 0
        lg.append(math.log2(len(surv) / (len(P) * Mi)) - f)
        P = [surv[rng.below(len(surv))] for _ in range(NP_R)]
    pairs = []; bad = 0; succ = 0
    Kt = K
    for (Ax, Ex, Wx, Ay, Ey, Wy) in P:
        bx = [Ax[18], Ax[19], Ax[20], Ax[21], Ax[22], Ex[18], Ex[19], Ex[20], Ex[21], Ex[22]]
        by = [Ay[18], Ay[19], Ay[20], Ay[21], Ay[22], Ey[18], Ey[19], Ey[20], Ey[21], Ey[22]]
        wxb = [Wx[i] for i in range(23)]; wyb = [Wy[i] for i in range(23)]
        for _ in range(NT_R):
            a0 = VS[rng.below(len(VS))]
            w7 = f7_sample(rng)
            w8 = (W8C[0] - ((a0 + C4) & M)) & M
            ok = True; outs = []
            for (b0, wb, d7, d8) in ((bx, wxb, 0, 0), (by, wyb, D7, D8)):
                W = list(wb); W[7] = (w7 + d7) & M; W[8] = (w8 + d8) & M
                a4, a3, a2, a1, a = b0[0], b0[1], b0[2], b0[3], b0[4]; e4, e3, e2, e1, e = b0[5], b0[6], b0[7], b0[8], b0[9]
                for i in range(23, NR):                          # the step and expansion inlined; a3 = A[i-4], a = A[i-1]
                    x = W[i-2]; y = W[i-15]; d = (x | x << 32); z = (y | y << 32)
                    w = ((((d >> 17) ^ (d >> 19)) & M ^ (x >> 10)) + W[i-7] + (((z >> 7) ^ (z >> 18)) & M ^ (y >> 3)) + W[i-16]) & M; W.append(w)
                    d = e | e << 32; ne = (a3 + e3 + ((d >> 6) ^ (d >> 11) ^ (d >> 25)) + ((e & e1) ^ (~e & e2)) + Kt[i] + w) & M
                    d = a | a << 32; na = (ne - a3 + ((d >> 2) ^ (d >> 13) ^ (d >> 22)) + ((a & a1) ^ (a & a2) ^ (a1 & a2))) & M
                    a4, a3, a2, a1, a = a3, a2, a1, a, na; e4, e3, e2, e1, e = e3, e2, e1, e, ne
                outs.append((a, a1, a2, a3, e, e1, e2, e3))
            if outs[0] == outs[1]:
                succ += 1; cv, wx, wy = rebuild({i: (wxb[i] if i > 8 else w7 if i == 7 else w8) for i in range(7, 23)}, a0)
                tx, ty = trace(cv, wx), trace(cv, wy)
                if compress(cv, wx) == compress(cv, wy) and wx != wy and accepted(tx, ty) and inF7(wx[7]) and wx[7] == w7: pairs.append((cv, wx, wy, a0))
                else: bad += 1
    if succ == 0: return None, pairs, bad
    lg.append(math.log2(succ / (NP_R * NT_R))); return sum(lg), pairs, bad

Q3_REPS = 10
ONLINE_TRIALS = 8
Q3_THRESH = -98.6       # log2 threshold of the pooled mean of the 10 replicates (fixed from 48 development requests before any validation run)

def class_of(a0):
    c = c7of(a0)
    for ci, (c7, base) in enumerate(CLASSES):
        if c == c7 and in_G(a0) and (a0 ^ base) & ~MASK & M == 0: return ci
    return None

def q3_experiment(req):
    VS = vsample(); out = []; est = []; allok = True; last = None
    for tr in req['trials']:
        t = tr['trial']; rec = dict(trial=t, message_a_hex=None, message_b_hex=None)
        if t < Q3_REPS:
            z, pairs, bad = smc_replicate(Shake(req['experiment_id'] + '|' + tr['seed']), VS)
            est.append(z); allok = allok and bad == 0
            rec['observations'] = dict(log2_estimate=z if z is not None else -1000.0, accepted_pairs=len(pairs), failed_rebuilds=bad)
            if pairs:
                cv, mx, my, a0 = pairs[0]; last = pairs[0]
                rec['message_a_hex'] = struct.pack('>24I', *(cv + mx)).hex(); rec['message_b_hex'] = struct.pack('>24I', *(cv + my)).hex()
        elif t == Q3_REPS and len(est) == Q3_REPS:
            mean = sum(2.0 ** z for z in est if z is not None) / Q3_REPS; lz = math.log2(mean) if mean > 0 else -1000.0
            rec['observations'] = dict(log2_pooled_mean=lz)
            if allok and Q3_THRESH is not None and lz >= Q3_THRESH and last:
                cv, mx, my, a0 = last
                rec['message_a_hex'] = struct.pack('>24I', *(cv + mx)).hex(); rec['message_b_hex'] = struct.pack('>24I', *(cv + my)).hex()
        out.append(rec)
    return dict(schema_version=1, trials=out)

def online_experiment(req):
    """the counted online program on organizer-seeded first blocks (real compressions): first blocks are drawn until one has a passing
    class (at most 64); its first passing class is run on two batches (the class's first 512 members) and every lane is compared with
    the scalar definition (E16x from the Step-2 words and the 38-step trace); trial 0 also runs the batch of the semi-free-start pair's
    variant on its chaining value and requires the counted program to find and accept it"""
    out = []
    for tr in req['trials']:
        rng = Shake(req['experiment_id'] + '|' + tr['seed']); rec = dict(trial=tr['trial'], message_a_hex=None, message_b_hex=None)
        if tr['trial'] >= ONLINE_TRIALS: out.append(rec); continue          # trials 8..255 return no pair by design
        for k in range(64):
            r0, r1 = rng.word(), rng.word()
            M0 = [(r0 >> (32 * q)) & M for q in range(8)] + [(r1 >> (32 * q)) & M for q in range(8)]
            cv = compress(IV, M0); m = Mach()
            hits = [ci for ci, (c7, b) in enumerate(CLASSES) if inF7((c7 - cv[0]) & M)]
            if hits: break
        bad = 0; lanes = 0; passed = 0
        if hits:
            ci = hits[0]; mem = members(ci, 512)
            sc = fb_scalars(m, cv); inp = broadcast(m, sc); ins = program()
            for b in range(2):
                bm = mem[256 * b:256 * b + 256]; planes = batch_planes(bm)
                for j in range(32):
                    if CBITS[j] == 'L': inp['A%d' % j] = planes[j]
                    elif CBITS[j] == 'C': inp['C%d' % j] = ONES if (CLASSES[ci][1] >> j) & 1 else 0
                ok, n = run_prog(ins, inp)
                for L, a0 in enumerate(bm):
                    wx = words(cv, a0)[0]; e = trace(cv, wx, 17)[1][16]
                    want = all(((e >> j) & 1) == ((R16[0] >> j) & 1) for j in TBITS)
                    bad += want != bool((ok >> L) & 1) or wx[7] != (CLASSES[ci][0] - cv[0]) & M or not inF7(wx[7]); lanes += 1; passed += want
            if not bad:
                wx, wy = words(cv, mem[0])
                rec['message_a_hex'] = struct.pack('>32I', *(M0 + wx)).hex(); rec['message_b_hex'] = struct.pack('>32I', *(M0 + wy)).hex()
        if tr['trial'] == 0:                                               # positive lanes: the batch of the semi-free-start pair's variant
            ci = class_of(A0S); mem = members(ci, 256)
            if A0S not in mem: mem[17] = A0S
            m2 = Mach(); sc2 = fb_scalars(m2, PCV); inp2 = broadcast(m2, sc2); fnd = []
            process_batch(m2, program(), inp2, batch_planes(mem), ci, PCV, sc2, fnd); bad += A0S not in fnd
        rec['observations'] = dict(first_blocks=k + 1, passing_classes=len(hits), lanes=lanes, stage3a_passes=passed, mismatches=bad)
        out.append(rec)
    return dict(schema_version=1, trials=out)

def calibrate():
    """the executed counts used by the ledger (proof.md Section 7)"""
    import random
    rr = random.Random(9); m = Mach(); cv = [rr.getrandbits(32) for _ in range(8)]
    w7 = []
    for _ in range(200): m = Mach(); w7test(m, rr.getrandbits(32), rr.getrandbits(32)); w7.append(m.ops)
    m = Mach(); sc = fb_scalars(m, cv); n_sc = m.ops; m = Mach(); broadcast(m, sc); n_bc = m.ops
    m = Mach(); a0 = members(0, 1)[0]; lane_value(m, {j: 0 for j in range(32)}, 0, MASK, 0); n_lv = m.ops
    m = Mach(); scalar_e16(m, sc, a0); n_e16 = m.ops
    m = Mach(); deep(m, PCV, A0S); n_deep = m.ops
    return dict(prog=len(program()) - 1, w7=max(w7), fb_fixed=FB_FIXED, w7_loop=W7_LOOP, scalars=n_sc, planes=n_bc, batch_ctl=BATCH_CTL,
                class_ctl=CLASS_CTL, lane=32 + LANE_CTL + n_lv + n_e16 + 42, deep=n_deep, tk=TK, classes=len(CLASSES), class_size=24576)

def selftest():
    import random
    rr = random.Random(5); ok = True
    def chk(name, cond, extra=''):
        nonlocal ok; ok = ok and bool(cond); print('%-70s %s %s' % (name, 'ok' if cond else 'FAIL', extra), flush=True)
    tx, ty = trace(PCV, PMX), trace(PCV, PMY)
    chk('1 the semi-free-start pair collides, M != M\', accepted event, W7 in F7', compress(PCV, PMX) == compress(PCV, PMY) and PMX != PMY and accepted(tx, ty) and inF7(PMX[7]))
    chk('  its variant A0 is in G and in a selected class', in_G(A0S) and class_of(A0S) is not None, '(class %s)' % class_of(A0S))
    def g16(w):
        A = dict(SAx); E = dict(SEx); W = {i: PMX[i] for i in range(16)}; B = dict(SAy); F = dict(SEy); V = {i: PMY[i] for i in range(16)}
        W[16] = w; V[16] = (w + DWT[16]) & M; step_row(A, E, W, 16); step_row(B, F, V, 16)
        return rowok((A, E, W), (B, F, V), 16)
    cand = list(GL) + [rr.getrandbits(32) for _ in range(20000)] + [g ^ (1 << b) for g in GL[:40] for b in range(32)]
    gs = set(GL); chk('2 row 16: the 160 W16 words hold it; 20,000 random words and 1,280 neighbours agree', all(g16(w) == (w in gs) for w in cand))
    bad = 0
    for _ in range(20):
        cv = [rr.getrandbits(32) for _ in range(8)]; ci = rr.randrange(len(CLASSES)); a0 = members(ci, 1, rr.randrange(40))[0]
        wx, wy = words(cv, a0); t = trace(cv, wx, 17); u = trace(cv, wy, 17); m = Mach(); sc = fb_scalars(m, cv)
        bad += scalar_e16(m, sc, a0) != t[1][16] or wx[7] != (CLASSES[ci][0] - cv[0]) & M or not all(rowok(t, u, i) for i in range(11, 16))
        bad += any(((wy[i] - wx[i]) & M) != DWT[i] for i in range(16))
    chk('3 Lemma 4.1: E16x formula, W7 = c7 - A_-1, rows 11..15 and the word differences on 20 chaining values', bad == 0)
    ins = program(); from collections import Counter
    cs = Counter(i[0] for i in ins)
    chk('4 row-16 program: instructions, loads, spill stores', True, '%d (%d loads, %d stores)' % (len(ins) - 1, cs['ld'], cs['st']))
    r = online_experiment(dict(experiment_id='a0p-online-r38', trials=[dict(trial=t, seed='%064x' % t) for t in range(2)]))
    chk('  program against the definition on 2 x 512 lanes of real first blocks', all(t['observations']['mismatches'] == 0 for t in r['trials']), str([t['observations'] for t in r['trials']]))
    ci = class_of(A0S); mem = members(ci, 256); found = []
    if A0S not in mem: mem[17] = A0S
    m = Mach(); sc = fb_scalars(m, PCV); inp = broadcast(m, sc); process_batch(m, program(), inp, batch_planes(mem), ci, PCV, sc, found)
    chk('5 the counted program finds the semi-free-start pair in its batch', A0S in found, '(%d operations)' % m.ops)
    z, pairs, bad = smc_replicate(Shake('selftest'), vsample())
    chk('6 replicate: estimate, accepted pairs rebuilt and verified, failed rebuilds 0', bad == 0, '(log2 %s, %d pairs)' % (None if z is None else round(z, 3), len(pairs)))
    print('   calibrate:', calibrate())
    print('SELFTEST', 'PASSED' if ok else 'FAILED'); return ok

def run_request(req): return online_experiment(req) if 'online' in req['experiment_id'] else q3_experiment(req)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'selftest': sys.exit(0 if selftest() else 1)
    if len(sys.argv) > 1 and sys.argv[1] == 'calibrate': print(json.dumps(calibrate())); sys.exit(0)
    sys.stdout.write(json.dumps(run_request(json.loads(sys.stdin.read())), separators=(',', ':')))
