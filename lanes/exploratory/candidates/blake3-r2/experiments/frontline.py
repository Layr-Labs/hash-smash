import hashlib
import json
import struct
import sys
from math import isqrt
M = 0xFFFFFFFF
IV = (0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A, 0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19)
K = (IV[2] + IV[6]) & M
LEN_A, LEN_B = 55, 63
X3, X7, X11, X15 = 0x29D4FA98, 0xBEE3AF28, 0x44036000, 0x40C58500
W4, W13 = 0x97475638, 0x0007C006
W4B = (((W4 + K) & M) ^ LEN_A ^ LEN_B) - K & M
DELTA5 = (W4 - W4B) & M
ETA, EPS, MU, BETA = 0x830303CF, 0x6E21BE55, 0x9AED22BD, 0x18B0E098
FLAGS, ROOT_FLAGS = 3, 11
PERM = (2, 6, 3, 10, 7, 0, 4, 13, 1, 11, 12, 5, 9, 14, 15, 8)
GCALLS = ((0, 4, 8, 12), (1, 5, 9, 13), (2, 6, 10, 14), (3, 7, 11, 15),
  (0, 5, 10, 15), (1, 6, 11, 12), (2, 7, 8, 13), (3, 4, 9, 14))
KB, TB, MEMBERS, FULL_EVERY, TRIAL_WORDS = 7, 19, 8, 8, 8
def ror(v, n):
 n &= 31
 return ((v >> n) | (v << (32 - n))) & M if n else v
def rol(v, n):
 return ror(v, 32 - (n & 31))
def bit(x, i):
 return x >> i & 1
def maj(a, b, c):
 return (a & b) | (a & c) | (b & c)
def g(a, b, c, d, x, y):
 a = (a + b + x) & M; d = ror(d ^ a, 16); c = (c + d) & M; b = ror(b ^ c, 12)
 a = (a + b + y) & M; d = ror(d ^ a, 8); c = (c + d) & M; b = ror(b ^ c, 7)
 return a, b, c, d
Y3, Y7, Y11, Y15 = g(X3, X7, X11, X15, W4, W13)
Y3B, Y7B, Y11B, Y15B = g(X3, X7, X11, X15, W4B, W13)
DY3, DY11 = (Y3B - Y3) & M, (Y11B - Y11) & M
K2A = (K + W4) & M
K2D = ror(K2A ^ LEN_A, 16)
K2C = (IV[2] + K2D) & M
K2B = ror(IV[6] ^ K2C, 12)
assert (Y7, Y15) == (Y7B, Y15B) and (Y3, DY3, Y11, DY11) == (0x8127C181, 0xFDB77CFD, 0x7AF77F38, 0x0A08818B)
assert DELTA5 == (-8) & M and ror(ETA ^ EPS, 8) == MU
CLASS_MASK, CLASS_VALUE, FREE_MASK = 0x03CF8303, 0x030C0303, 0xFC307CFC
CLASS_FREE = [i for i in range(32) if FREE_MASK >> i & 1]
SPL = [sum((k >> n & 1) << i for n, i in enumerate(CLASS_FREE)) for k in range(1024)]
SPH = [sum((k >> n & 1) << CLASS_FREE[n + 10] for n in range(9)) for k in range(512)]
def member(k):
 e1 = CLASS_VALUE | SPL[k & 1023] | SPH[k >> 10]
 return e1, (e1 - Y3) & M
TYPE16 = tuple(((member(k)[1] >> 4) ^ (member(k)[1] >> 5)) & 1 for k in range(16))
EPS2, BETA2 = 0x6E61BE55, 0x18D0E098
QSTAR_MASK, QSTAR_VALUE = 0x0E09818B, 0x02008000
SPECS = ((EPS, BETA, QSTAR_MASK, QSTAR_VALUE, None), (EPS2, BETA2, 0x0E09818D, 0x02008001, 0),
  (EPS2, BETA2, 0x0E09818D, 0x02008001, 1))
TAU, S_MASK = 0x285020A0, 0x07
TYPE_E = (23820160, 34028800)
KEPT16 = [(20034560, 20092800, 28620800, 28704000)[c >> 2 & 2 | (c & 7 in (3, 5))] for c in range(16)]
E_KEPT = sum(KEPT16) // 16
SHARE, E_COUNT = 14110208 * 28924480, 28924480
FE_P6, FP_P6, MU_P6, ALPHA_P6 = 1000173, 1002882, 4652, 1000048
FACTOR = 974 * 77309411328 // 1000
STEPS_CTX = MEMBERS * KB << 16
RUN_CONTEXTS = -(-(-(-(24797 << 128) // (50000 * FACTOR * ((1 << 21) - 1)))) // STEPS_CTX)
RUN_STEPS = RUN_CONTEXTS * STEPS_CTX
_S = isqrt(10 * RUN_CONTEXTS - 1) + 1
LIVE16, NBLK, ALPHA_B = 4160, KB * MEMBERS, ALPHA_P6
E_BUDGET = -(-(FE_P6 * RUN_STEPS * E_KEPT) // (10 ** 6 << 32)) + _S * STEPS_CTX
P_BUDGET = -(-(FP_P6 * RUN_STEPS * SHARE) // (10 ** 6 << 64)) + _S * STEPS_CTX
U_SC0, U_SC1 = 64, 20
PASS1 = (8778240,) * 3
CMJ = (8080,) * 3
MU_D = MU_P6
_MC = -(-(MU_D * RUN_STEPS) // 10 ** 6)
U_PRE = 15
CAPX = 3 * 7466 + 614 + U_SC0 + 3 * U_SC1 + U_PRE
_LC = CAPX * STEPS_CTX
CREDIT = _MC + isqrt(40 * _LC * _MC - 1) + 1 + 14 * _LC + CAPX
U_GLOBAL, U_FAMILY, U_ROW, U_FORCED, U_SELECTED, U_G15, U_FREE, U_LEAF, U_ROOT = 614, 2304, 1354, 20, 4, 64, 48, 80, 120
U_CONTEXT, U_MEMBER, U_BLOCK, U_E, U_PASS = 436, 71, 11, 3, 39
U_WORD = 1 + 3 + 33 + 3
U_E_LIST = 1 + 1 + 1
U_PASS_X = 1
U_SCAN = 12
U_PF = 1 + 1 + 1 + 1 + 1 + 1 + 1
U_WT, U_KF = 3, 3 + 7
PF_CHECK_EVERY = 61
Q_PF_NUM, Q_PF_DEN = 11, 100
U_LIVE_LIST = (2 + 6) + (1 + 1 + 6) + 3 + 1 + 2 + 2
LIST_BUILD = 1 << 24
assert (U_WORD, U_E_LIST, U_PASS_X, U_SCAN, U_LIVE_LIST) == (40, U_E, 1, 12, 24)
LIVE_BUDGET = -(-(ALPHA_B * LIVE16 * NBLK * RUN_CONTEXTS) // (10 ** 6 << 16)) + NBLK * _S
WORDS_BUDGET = -(-(E_BUDGET + 6 * LIVE_BUDGET) // 7)
PF_BUDGET = -(-(Q_PF_NUM * WORDS_BUDGET) // Q_PF_DEN) + _S * (-(-STEPS_CTX // 7) + NBLK)
EPF_BUDGET = 7 * PF_BUDGET
BUILD = 834078790425024
ONCE = BUILD + 1128752545267752 + (1 << 17) + (1 << 40) + (1 << 38) + LIST_BUILD + (1 << 48) + (1 << 30) + (1 << 50) + (1 << 38) + (1 << 36) + (1 << 24) + (1 << 17)
S_OLD = 116 * 18021 * (1 << 42) // 2 + 116 * ((1 << 51) + (1 << 10)) + (1 << 50)
TMAX = (1 << 51) - 1
FINAL = (430 + 64) * 2 + 128 * (TMAX + 1) + 430 * 2 ** 38
U_PP = U_PASS + U_PASS_X + U_SCAN
WB = ((U_WORD + U_PF - U_WT) * WORDS_BUDGET + U_LIVE_LIST * LIVE_BUDGET + U_E * EPF_BUDGET
 + (U_WT + U_KF) * PF_BUDGET + U_PP * P_BUDGET)
W_CTX = ((U_WORD + U_PF + U_KF + 7 * U_E) * (-(-STEPS_CTX // 7) + NBLK) + U_PP * STEPS_CTX + U_LIVE_LIST * NBLK)
N = ((U_CONTEXT + 7 + U_MEMBER * MEMBERS) * (RUN_CONTEXTS + 1) + U_BLOCK * NBLK * RUN_CONTEXTS + WB + W_CTX
 + CREDIT + ONCE + S_OLD + FINAL)
TEXT = dict(RUN_CONTEXTS=291192107719524, LIVE_BUDGET=1035149651946890, E_BUDGET=6058892113753469726,
   P_BUDGET=23910504180632184, CREDIT=4975609607346059155, PF_BUDGET=95337056377640282,
   EPF_BUDGET=667359394643481974, N=53233506092972185742)
assert all(globals()[k] == v for k, v in TEXT.items())
def Sum(*t):
 return ('sum', t)
def Neg(x):
 return ('neg', x)
def X(a, b):
 return ('xor', a, b)
def R(a, r):
 return ('ror', a, r)
def L(a, r):
 return ('ror', a, 32 - r)
LINES = [
 ('X2', Sum('D2.a1', 'D2.b1', W13)), ('X8', X(rol(X7, 7), 'D2.b1')), ('C0.c1', Sum('X8', 'C0.d1')),
 ('K3.a1', Sum((IV[3] + IV[7]) & M, 'w6')), ('K3.d1', R(X('K3.a1', 'fl'), 16)), ('K3.c1', Sum(IV[3], 'K3.d1')),
 ('S15', Sum('S11', Neg('K3.c1'))), ('S3', X(L('S15', 8), 'K3.d1')), ('K3.b1', R(X(IV[7], 'K3.c1'), 12)),
 ('D3.a1', Sum('S3', 'S4')), ('S7', R(X('K3.b1', 'S11'), 7)), ('D3.b1', Sum(X3, Neg('D3.a1'))),
 ('D2.c1', X(L('D2.b1', 12), 'S7')), ('D3.c1', X(L('D3.b1', 12), 'S4')), ('X4', R(X('D3.b1', 'X9'), 7)),
 ('X13', Sum('X8', Neg('D2.c1'))), ('X14', Sum('X9', Neg('D3.c1'))), ('C0.b1', R(X('X4', 'C0.c1'), 12)),
 ('D2.d1', X(L('X13', 8), 'X2')), ('D3.d1', X(L('X14', 8), X3)), ('Y8', X(L('Y4', 7), 'C0.b1')),
 ('S13', X(L('D2.d1', 16), 'D2.a1')), ('S9', Sum('D3.c1', Neg('D3.d1'))), ('Y12', Sum('Y8', Neg('C0.c1'))),
 ('K1.c1', Sum('S9', Neg('S13'))), ('Y0', X(L('Y12', 8), 'C0.d1')), ('K1.d1', Sum('K1.c1', Neg(IV[1]))),
 ('C0.a1', Sum('Y0', Neg('C0.b1'), Neg('w6'))), ('K1.a1', X(L('K1.d1', 16), 'thi')),
 ('w2', Sum('K1.a1', Neg(IV[1]), Neg(IV[5]))), ('X0', Sum('C0.a1', Neg('X4'), Neg('w2'))),
 ('S14', X(L('D3.d1', 16), 'D3.a1')), ('K1.b1', R(X(IV[5], 'K1.c1'), 12)), ('S10', Sum(K2C, 'S14')),
 ('D0.d1', X(rol(X15, 8), 'X0')), ('S5', R(X('K1.b1', 'S9'), 7)), ('D0.c1', Sum('S10', 'D0.d1')),
 ('D0.b1', R(X('S5', 'D0.c1'), 12)), ('X10', Sum('D0.c1', X15)), ('X5', R(X('D0.b1', 'X10'), 7)),
 ('S1', X(L('S13', 8), 'K1.d1')), ('w3', Sum('S1', Neg('K1.a1'), Neg('K1.b1'))),
 ('X12', X(L('C0.d1', 16), 'C0.a1')), ('D1.c1', Sum(X11, Neg('X12'))), ('D1.d1', Sum('D1.c1', Neg('S11'))),
 ('S8', Sum('D2.c1', Neg('D2.d1'))), ('K0.b1', X(L('S4', 7), 'S8')), ('S2', X(L('S14', 8), K2D)),
 ('S6', R(X(K2B, 'S10'), 7)), ('X1', X(L('X12', 8), 'D1.d1')), ('K0.c1', X(L('K0.b1', 12), IV[4])),
 ('D1.b1', R(X('S6', 'D1.c1'), 12)), ('C1.a1', Sum('X1', 'X5', 'w3')), ('S12', Sum('S8', Neg('K0.c1'))),
 ('w7', Sum('S3', Neg('K3.a1'), Neg('K3.b1'))), ('X6', R(X('D1.b1', X11), 7)),
 ('C1.d1', R(X('X13', 'C1.a1'), 16)), ('D1.a1', X(L('D1.d1', 16), 'S12')), ('C1.c1', Sum('X9', 'C1.d1')),
 ('C2.a1', Sum('X2', 'X6', 'w7')), ('w10', Sum('D1.a1', Neg('S1'), Neg('S6'))),
 ('C1.b1', R(X('X5', 'C1.c1'), 12)), ('C2.d1', R(X('X14', 'C2.a1'), 16)),
 ('w12', Sum('D2.a1', Neg('S2'), Neg('S7'))), ('Y1', Sum('C1.a1', 'C1.b1', 'w10')),
 ('C2.c1', Sum('X10', 'C2.d1')), ('Y13', R(X('C1.d1', 'Y1'), 8)), ('C2.b1', R(X('X6', 'C2.c1'), 12)),
 ('K0.d1', Sum('K0.c1', Neg(IV[0]))), ('Y9', Sum('C1.c1', 'Y13')), ('S0', X(L('S12', 8), 'K0.d1')),
 ('D0.a1', X(L('D0.d1', 16), 'S15')), ('w8', Sum('D0.a1', Neg('S0'), Neg('S5'))),
 ('w5', Sum('S2', Neg(K2A), Neg(K2B))), ('w9', Sum('X0', Neg('D0.a1'), Neg('D0.b1'))),
 ('w11', Sum('X1', Neg('D1.a1'), Neg('D1.b1'))), ('Y5', R(X('C1.b1', 'Y9'), 7)),
]
DEF = dict(LINES)
OUTER_WORDS = ('C0.d1', 'D2.a1', 'D2.b1', 'S11', 'S4', 'X9', 'w6')
def deps(e, out):
 if isinstance(e, str):
  out.add(e)
 elif isinstance(e, tuple):
  for t in (e[1] if e[0] == 'sum' else e[1:2] if e[0] in ('neg', 'ror') else e[1:]):
   deps(t, out)
 return out
def closure(names):
 need, st = set(), list(names)
 while st:
  n = st.pop()
  if n in DEF and n not in need:
   need.add(n)
   st += deps(DEF[n], set())
 return need
NEEDED, MARKED = closure(['Y9', 'w8']), set()
for _n, _e in LINES:
 if deps(_e, set()) & (MARKED | {'Y4'}):
  MARKED.add(_n)
MEMBER_LINES = [n for n, _ in LINES if n in NEEDED and n in MARKED]
CONTEXT_LINES = [n for n, _ in LINES if n in NEEDED and n not in MARKED]
OMEGA_SIDE = [n for n in MEMBER_LINES if n in closure(['w8'])]
Y9_PATH = [n for n in MEMBER_LINES if n not in OMEGA_SIDE]
assert len(NEEDED) == 64 and MEMBER_LINES == ('Y8 Y12 Y0 C0.a1 X0 D0.d1 D0.c1 D0.b1 X10 X5 X12 D1.c1 D1.d1 X1 C1.a1 '
           'C1.d1 D1.a1 C1.c1 w10 C1.b1 Y1 Y13 Y9 D0.a1 w8').split()
assert CONTEXT_LINES == ('X2 X8 C0.c1 K3.a1 K3.d1 K3.c1 S15 S3 K3.b1 D3.a1 S7 D3.b1 D2.c1 D3.c1 X4 X13 X14 C0.b1 '
      'D2.d1 D3.d1 S13 S9 K1.c1 K1.d1 K1.a1 w2 S14 K1.b1 S10 S5 S1 w3 S8 K0.b1 S6 K0.c1 S12 '
      'K0.d1 S0').split()
assert OMEGA_SIDE == 'Y8 Y12 Y0 C0.a1 X0 D0.d1 D0.a1 w8'.split() and set(Y9_PATH) <= closure(['Y9'])
assert {'C0.a1', 'D0.d1'} == {d for n in Y9_PATH for d in deps(DEF[n], set())} & set(OMEGA_SIDE)
def nm(s):
 return s.replace('.', '_')
def src(e, tmp):
 if isinstance(e, int):
  return str(e)
 if isinstance(e, str):
  return nm(e)
 if e[0] == 'sum':
  return '((%s) & M)' % ' '.join('- ' + src(t[1], tmp) if type(t) is tuple and t[0] == 'neg' else
         '+ ' + src(t, tmp) for t in e[1])
 if e[0] == 'xor':
  return '(%s ^ %s)' % (src(e[1], tmp), src(e[2], tmp))
 tmp.append(1)
 t = '_t%d' % len(tmp)
 return '((((%s := %s) >> %d) | (%s << %d)) & M)' % (t, src(e[1], tmp), e[2], t, 32 - e[2])
def compile_lines(name, args, lines, ret):
 tmp = []
 body = "\n    ".join('%s = %s' % (nm(n), src(DEF[n], tmp)) for n in lines)
 ns = {'M': M}
 exec("def %s(%s):\n    %s\n    return %s\n" % (name, ', '.join(args), body, ret), ns)
 return ns[name]
ARGS = [nm(n) for n in OUTER_WORDS]
co_full = compile_lines('co_full', ARGS + ['Y4', 'fl', 'thi=0'], [n for n, _ in LINES], 'locals()')
co_ref = compile_lines('co_ref', ARGS + ['Y4', 'fl', 'thi=0'], [n for n, _ in LINES], '(%d + Y4 + w8) & M, Y9' % Y3)
co_ctx = compile_lines('co_ctx', ARGS + ['fl', 'thi=0'], CONTEXT_LINES, 'locals()')
def rebuild(ow, y, e1, fl=FLAGS, thi=0):
 v = co_full(*ow, y, fl, thi)
 v['e1'], v['omega'] = e1, (Y3 + y + v['w8']) & M
 return v
def cut_ok():
 for L0 in range(1 << 16):
  for f in (1, 0):
   if f or L0 < 65535:
    c = cut16(L0, f)
    if sorted(c) != sorted(dyadic(*((0, L0) if f else (L0 + 1, 65535)))[0]) or len(c) > 16 or len({z for _, z in c}) != len(c):
     return False
 return True
def plain_pass():
 cnt = {0: 1}
 for _ in range(3):
  nxt = {}
  for s, c in cnt.items():
   for b in range(256):
    nxt[F1[s + b]] = nxt.get(F1[s + b], 0) + c
  cnt = nxt
 return sum(c for s, c in cnt.items() for b in range(256) if F1[s + b])
def theta_of(tau):
 return rol(tau ^ ror(tau, 1), 12)
def automaton(targets, dy, n=32):
 layer, trans = [(0, (1,) * len(targets))], []
 for i in range(n):
  ids, rows, e = {}, [], dy >> i & 1
  for k, sets in layer:
   row = []
   for a in (0, 1):
    b, new = a ^ e ^ k, []
    for m, (dz, out) in zip(sets, targets):
     d, r = dz >> i & 1, 0
     for c in range(4):
      if m >> c & 1 and (c >> 1) ^ (c & 1) == (out >> i & 1) ^ a ^ b ^ d:
       for v in (0, 1):
        r |= 1 << ((a + v + (c >> 1)) >> 1) * 2 + ((b + (v ^ d) + (c & 1)) >> 1)
     new.append(r)
    state = ((a + e + k) >> 1, tuple(new)) if any(new) else (0, (0,) * len(new))
    row.append(ids.setdefault(state, len(ids)))
   rows.append(row)
  trans.append(rows)
  layer = list(ids)
 final, tables = [sum(1 << j for j, m in enumerate(sets) if m) for _, sets in layer], []
 for p in range(0, n, 8):
  table = []
  for s in range(len(trans[p])):
   row = [s]
   for j in range(min(8, n - p)):
    row = [trans[p + j][row[x & (1 << j) - 1]][x >> j] for x in range(2 << j)]
   table += [final[row[x % len(row)]] if p + 8 >= n else row[x % len(row)] << 8 for x in range(256)]
  tables.append(table)
 return tables
def flat(tables):
 bases, f = [], []
 for t in tables:
  bases.append(len(f))
  f += t
 for p in range(3):
  for i in range(bases[p], bases[p] + len(tables[p])):
   f[i] += bases[p + 1]
 return f
THETAS = [theta_of(TAU)] * 3
SIGMAS = [TAU ^ ror(TAU, 1)] * 3
AUT1 = automaton([(ETA, x) for x in THETAS], 0)
AUT1[3] = [m & S_MASK for m in AUT1[3]]
F1 = flat(AUT1)
def rel_flat(rels):
 first = {i: (i, j, c) for i, j, c in rels}; second = {j: (i, j, c) for i, j, c in rels}
 sig, eps = SIGMAS[0], (SPECS[0][0], SPECS[1][0])
 init = (0, frozenset(((0, 0, ()),)), frozenset(((0, 0, ()),)))
 def adv(z, k, e):
  cp, s0, s1 = z; d = DY3 >> k & 1; epk = e ^ d ^ cp; ncp = maj(e, d, cp); out = []
  for ep, S in zip(eps, (s0, s1)):
   N = set(); ss, tt = sig >> k & 1, ep >> k & 1
   for a, ap, pend in S:
    for f in (0, 1):
     if (e ^ f ^ a) ^ (epk ^ f ^ ss ^ ap) != tt: continue
     pd = dict(pend)
     if k in second:
      i, _, c = second[k]
      if pd.pop(i) ^ f != c: continue
     if k in first: pd[k] = f
     N.add((maj(e, f, a), maj(epk, f ^ ss, ap), tuple(sorted(pd.items()))))
   out.append(frozenset(N))
  return None if not (out[0] or out[1]) else (ncp, out[0], out[1])
 levels, trans = [{init: 0}], []
 for k in range(32):
  cur, nxt, T = levels[-1], {}, []
  for z, i in cur.items():
   row = []
   for e in (0, 1):
    q = adv(z, k, e)
    if q is None: row.append(-1); continue
    if q not in nxt: nxt[q] = len(nxt)
    row.append(nxt[q])
   T.append(row)
  dead = len(nxt); T = [[dead if q < 0 else q for q in row] for row in T] + [[dead, dead]]
  trans.append(T); levels.append(nxt)
 final = [(bool(z[1]) * 1) | (bool(z[2]) * 2) for z in levels[32]] + [0]
 tabs = []
 for p in range(0, 32, 8):
  tab = []
  for s in range(len(trans[p])):
   row = [s]
   for j in range(min(8, 32 - p)):
    row = [trans[p + j][row[x & ((1 << j) - 1)]][x >> j] for x in range(2 << j)]
   tab += [final[row[x % len(row)]] if p + 8 >= 32 else row[x % len(row)] << 8 for x in range(256)]
  tabs.append(tab)
 return flat(tabs)
F2T = (rel_flat(((9, 10, 1), (24, 25, 1))), rel_flat(((9, 10, 1), (24, 25, 0))))
def T1(x):
 f = F1
 return f[f[f[f[x & 255] + (x >> 8 & 255)] + (x >> 16 & 255)] + (x >> 24)]
def T2(x, t=0):
 f = F2T[t]
 return f[f[f[f[x & 255] + (x >> 8 & 255)] + (x >> 16 & 255)] + (x >> 24)]
def T2P(x, t=0):
 return T2(x & M, t)
def fld(a):
 return a >> 36 * max(0, (a.bit_length() - 1) // 36)
def T2R(a, t=0):
 return T2(fld(a) & M, t)
def T1R(a):
 return T1(fld(a) - B34)
class RotT:
 def __init__(self, r):
  self.r = r
 def __getitem__(self, x):
  return ror(x, self.r)
RT7, RT12, RT16 = RotT(7), RotT(12), RotT(16)
def cond1(x, theta):
 gamma = ETA ^ theta
 if gamma & 1:
  return 0
 st = {0}
 for i in range(32):
  q, e_, gi = bit(x, i), bit(ETA, i), bit(gamma, i)
  st = {maj(q, v, u) for u in st for v in (0, 1)
   if i == 31 or maj(q, v ^ e_, u ^ gi) == maj(q, v, u) ^ bit(gamma, i + 1)}
  if not st:
   return 0
 return 1
def mask1_ref(x):
 return sum(cond1(x, THETAS[j]) << j for j in range(3))
assert EPS2 & 511 == EPS & 511
S7 = sum(1 << w for w in range(128) if any(((v + f) ^ ((v + DY3) + (f ^ s))) & 511 == EPS & 511 for v in
          range(w, 512, 128) for s in set(SIGMAS[j] & 511 for j in range(3))
          for f in range(512)))
assert S7 == (1 << 0x3F) - (1 << 0x25) + (1 << 0x5F) - (1 << 0x45)
B34, L36 = 1 << 34, (1 << 36) - 1
LANES, LB = 7, 36
ONES = sum(1 << LB * i for i in range(LANES))
M_ALL = M * ONES
PFC, PF1, PFF, PFK, PFB = (0x004 * ONES, (1 << 6) * ONES, 0x387 * ONES, 0x3FF * ONES, (1 << 10) * ONES)
LO = [((1 << 32 - r) - 1) * ONES for r in range(33)]
HI = [(M ^ ((1 << 32 - r) - 1)) * ONES for r in range(33)]
RX15, PX15, QM, X11P = rol(X15, 8) * ONES, X15 * ONES, B34 | M, X11 + 1
QL = [QM << LB * i for i in range(LANES)]
M16V = 0xFFFF * ONES
def pror(x, r):
 return x >> r & LO[r] | x << 32 - r & HI[r]
def operands(cx):
 n = lambda w: -w & M
 w = (cx['C0_b1'], n(cx['C0_c1']), cx['C0_d1'], n(cx['C0_b1'] + cx['w6']), rol(cx['C0_d1'], 16),
  (X11 + 1 - cx['S11']) & M, cx['S12'], n(cx['C0_b1'] + cx['w6'] + cx['X4'] + cx['w2']), n(cx['S1'] + cx['S6']),
  cx['S15'] ^ ror(X15, 8), cx['S10'], cx['S5'], cx['w3'], cx['X13'], cx['X9'], n(cx['S0'] + cx['S5']))
 return tuple(x * ONES for x in w)
def y9_member(C0, P):
 rC0d1, K5, S12, nS1S6 = P[4], P[5], P[6], P[8]
 X12 = C0 ^ rC0d1
 D1d1 = (X12 ^ M_ALL) + K5
 D1a1 = pror(D1d1, 16) ^ S12
 return pror(X12, 24) ^ D1d1, D1a1 + nS1S6
def y9_fill_lo(X0, W3, X1, w10, P):
 S10, S5, X13, X9 = P[10], P[11], P[13], P[14]
 D0d1 = X0 ^ RX15
 D0c1 = D0d1 + S10
 X10 = D0c1 + PX15
 X5 = pror(pror(S5 ^ D0c1, 12) ^ X10, 7)
 C1a1 = X1 + X5 + W3
 C1d1 = pror(X13 ^ C1a1, 16)
 C1c1 = X9 + C1d1
 t1 = X5 ^ C1c1
 Y1_lo = C1a1 + (t1 >> 12 & LO[12]) + w10
 return C1c1 + ((C1d1 ^ Y1_lo) >> 8 & LO[8]), Y1_lo, D0d1, C1c1, C1d1, t1
def y9_fill_hi(Y1_lo, C1c1, C1d1, t1):
 Y1 = Y1_lo + (t1 << 20 & HI[12])
 return C1c1 + pror(C1d1 ^ Y1, 8), Y1
class Row:
 def __init__(self, j):
  self.j, self.tau, self.sigma = j, TAU, TAU ^ ror(TAU, 1)
  self.eps, self.beta, self.qm, self.qv, self.cfix = SPECS[j]
  self.mu, self.theta = ror(ETA ^ self.eps, 8), rol(self.sigma, 12)
  self.gamma = ETA ^ self.theta
  self.D = (self.sigma ^ self.eps) & 0x7FFFFFFF
  fixed = {7, 10, 11, 12, 16, 17, 18, 19, 20, 24, 25, 26, 29}
  self.free = [i for i in range(7, 32) if i not in fixed and not (i < 31 and bit(self.gamma, i))
     and not ((i + 20) % 32 < 31 and bit(self.D, (i + 20) % 32))]
ROWS = [Row(j) for j in range(3)]
def forced_bit(i, Qi, b):
 return {0: 0, 1: 1, 2: 1 ^ b, 10: b, 16: 0, 17: 0, 18: 1 ^ Qi, 19: Qi}.get(i)
SC0 = frozenset((0, 0, g_, gp, g_, gp) for g_ in (0, 1) for gp in (0, 1))
def scr_step(sub, i, Qi, yi, Ek, Epk, b, row):
 sg, gm, k = row.sigma, row.gamma, (i + 20) & 31
 kap, fh, out = ((sg ^ row.eps) >> k & 1) ^ Ek ^ Epk, forced_bit(i, Qi, b), set()
 for u, up, a, ap, g_, gp in sub:
  if i == 12:
   a = ap = 0
  if a ^ ap != kap or u ^ up != gm >> i & 1:
   continue
  for hb in ((0, 1) if fh is None else (fh,)):
   f = yi ^ Qi ^ hb ^ u
   an, apn = maj(Ek, f, a), maj(Epk, f ^ (sg >> k & 1), ap)
   if i < 31 or (an, apn) == (g_, gp):
    out.add((maj(Qi, hb, u), maj(Qi, hb ^ (ETA >> i & 1), up), an, apn, g_, gp))
 return frozenset(out)
def screen(Q, y, E, e1, j):
 row, Ep, sub = ROWS[j], (E + DY3) & M, SC0
 b = e1 >> 2 & 1 if row.cfix is None else row.cfix
 for i in range(32):
  k = (i + 20) & 31
  sub = scr_step(sub, i, Q >> i & 1, y >> i & 1, E >> k & 1, Ep >> k & 1, b, row)
  if not sub:
   return False
 return True
def is_joint_root(Q, y, E, h, row):
 gg = (Q + h) & M
 if gg ^ ((Q + (h ^ ETA)) & M) != row.theta:
  return False
 f = ror(y ^ gg, 12)
 e2 = (E + f) & M
 if e2 ^ ((((E + DY3) & M) + (f ^ row.sigma)) & M) != row.eps:
  return False
 h2 = ror(h ^ e2, 8)
 return ((gg + h2) & M) ^ (((gg ^ row.theta) + (h2 ^ row.mu)) & M) == row.tau
def arc_of(d, u, a, v):
 Qi, yi, Ek, Epk, etai, gi, sk, kk, gi1, kk1, hasc, cval, li, lk = d
 gg = Qi ^ v ^ u
 u1, up1 = maj(Qi, v, u), maj(Qi, v ^ etai, u ^ gi)
 if not li and up1 != (u1 ^ gi1):
  return 0
 f = yi ^ gg
 e2 = Ek ^ f ^ a
 a1, ap1 = maj(Ek, f, a), maj(Epk, f ^ sk, a ^ kk)
 if not lk and ap1 != (a1 ^ kk1):
  return 0
 return 0x10 | (0 if li else u1) << 3 | (0 if lk else a1) << 2 | v << 1 | e2
def build_arrays():
 forced, dual, selected = [0] * (1 << 16), [0] * (1 << 16), [0] * (1 << 17)
 for key14 in range(1 << 14):
  d = tuple(key14 >> 13 - t & 1 for t in range(14))
  Qi, yi, Ek, Epk, etai, gi, sk, kk, gi1, kk1, hasc, cval, li, lk = d
  prescribed = (not li and gi) or (not lk and (kk ^ Ek ^ Epk))
  for cp in range(4):
   arcs = [arc_of(d, cp >> 1, cp & 1, 0), arc_of(d, cp >> 1, cp & 1, 1)]
   key = key14 << 2 | cp
   dual[key] = arcs[0] | arcs[1] << 5
   if hasc:
    forced[key] = arcs[cval]
   else:
    passing = [x for x in arcs if x]
    if len(passing) == 1:
     forced[key] = passing[0]
    assert not (len(passing) == 2 and prescribed), 'Lemma S5'
   for want in (0, 1):
    cand = [x for x in ((arcs[cval],) if hasc else arcs) if x and x & 1 == want]
    assert len(cand) <= 1
    selected[key << 1 | want] = cand[0] if cand else 0
 return forced, dual, selected
FORCED, DUAL, SELECTED = build_arrays()
def descriptor(row, Q, y, E, Ep, kappa, i, hasc=0, cval=0):
 k = (i + 20) % 32
 key = 0
 for b_ in (bit(Q, i), bit(y, i), bit(E, k), bit(Ep, k), bit(ETA, i), bit(row.gamma, i), bit(row.sigma, k),
   bit(kappa, k), bit(row.gamma, i + 1) if i < 31 else 0, bit(kappa, k + 1) if k < 31 else 0,
   hasc, cval, int(i == 31), int(k == 31)):
  key = key << 1 | b_
 return key
def nu_of(Q, e1, C, B):
 r = (((Q >> 16) ^ e1) & 4) ^ 7
 return ((((r + C) & M) ^ B) ^ 1) & 7
def g7_value(h6, e1, C, B):
 x = h6 ^ bit(e1, 22)
 return bit(e1, 23) ^ 1 ^ bit(C, 23) ^ bit(B, 23) ^ maj(x, bit(C, 22), x ^ bit(C, 22) ^ bit(B, 22))
def prescription(Ek, Epk, sk, kk1, a):
 return (Ek ^ sk ^ kk1) if a == Ek else (Epk ^ kk1)
def row_setup(row, Q, y, E, Ep, e1, kappa, C, B, notes):
 b, u, sg, gm = bit(e1, 2) if row.cfix is None else row.cfix, bit(e1, 21), row.sigma, row.gamma
 Eb, Epb, kb, sb = (lambda k: bit(E, k)), (lambda k: bit(Ep, k)), (lambda k: bit(kappa, k)), (lambda k: bit(sg, k))
 kept = []
 for a20 in (0, 1):
  a, ap, ok = a20, a20 ^ kb(20), True
  for k in (20, 21):
   a1, ap1 = maj(Eb(k), 0, a), maj(Epb(k), sb(k), ap)
   if ap1 != a1 ^ kb(k + 1):
    ok = False
    break
   a, ap = a1, ap1
  if ok:
   kept.append((a20, a))
 if not kept:
  return None
 if len({a22 for _, a22 in kept}) != 1:
  notes.append('two kept guesses with different a[22]')
 a22 = kept[0][1]
 f22 = prescription(Eb(22), Epb(22), sb(22), kb(23), a22) if row.cfix is None else 1 ^ b ^ bit(y, 2) ^ bit(Q, 2)
 a23 = maj(Eb(22), f22, a22)
 f23 = prescription(Eb(23), Epb(23), sb(23), kb(24), a23) if bit(gm, 3) == 0 else 1 ^ bit(Q, 3) ^ bit(y, 3)
 a = a22
 for k, fk in ((22, f22), (23, f23)):
  a1 = maj(Eb(k), fk, a)
  if maj(Epb(k), fk ^ sb(k), a ^ kb(k)) != a1 ^ kb(k + 1):
   return None
  a = a1
 a24 = a
 h = {0: 0, 1: 1}
 h[2] = bit(y, 2) ^ f22 ^ bit(Q, 2)
 if h[2] != 1 ^ b:
  return None
 u3 = maj(h[2], bit(Q, 2), 0)
 h[3] = bit(y, 3) ^ f23 ^ bit(Q, 3) ^ u3
 if row.cfix is not None and h[3] != b:
  return None
 u4 = maj(h[3], bit(Q, 3), u3)
 h[10] = b
 h[11] = 1 ^ h[3]
 u11 = maj(h[10], bit(Q, 10), bit(Q, 9)) if bit(gm, 10) == 0 else bit(Q, 10)
 u12 = maj(h[11], bit(Q, 11), u11)
 f0 = prescription(Eb(0), Epb(0), sb(0), kb(1), 0)
 a1_ = maj(Eb(0), f0, 0)
 h[12] = bit(y, 12) ^ f0 ^ bit(Q, 12) ^ u12
 u13 = maj(h[12], bit(Q, 12), u12)
 h[24] = h[3] ^ h[12] ^ u
 f24 = h[24] ^ Eb(24) ^ a24
 h[4] = bit(y, 4) ^ f24 ^ bit(Q, 4) ^ u4
 a25 = maj(Eb(24), f24, a24)
 if maj(Epb(24), f24 ^ sb(24), a24 ^ kb(24)) != a25 ^ kb(25):
  return None
 u5 = maj(h[4], bit(Q, 4), u4)
 f25 = prescription(Eb(25), Epb(25), sb(25), kb(26), a25)
 a26 = maj(Eb(25), f25, a25)
 h[5] = bit(y, 5) ^ f25 ^ bit(Q, 5) ^ u5
 h[6] = bit(y, 13) ^ bit(Q, 13) ^ u13 ^ Eb(1) ^ a1_ ^ u
 h[16] = h[17] = 0
 h[18] = 1 ^ bit(Q, 18)
 h[19] = bit(Q, 19)
 if bit(gm, 7):
  h[7] = 1 ^ bit(gm, 8) ^ h[6]
 v7 = g7_value(h[6], e1, C, B)
 if 7 in h and h[7] != v7:
  return None
 h[7] = v7
 states, e2_26 = set(), set()
 for a20, _ in kept:
  uu, aa, ok = 0, a20, True
  for i in range(7):
   arc = FORCED[descriptor(row, Q, y, E, Ep, kappa, i, 1, h[i]) << 2 | uu << 1 | aa]
   if not arc:
    ok = False
    break
   uu, aa = arc >> 3 & 1, arc >> 2 & 1
   if i == 6:
    e2_26.add(arc & 1)
  if ok:
   states.add((uu, aa))
 if not states:
  return None
 if len(states) > 1:
  notes.append('kept guesses reach different states at depth 7')
 if len(e2_26) != 1:
  notes.append('e2[26] differs between guesses')
 h[26] = min(e2_26)
 return h, sorted(states)
def g15_meta(h6, e1, bk, row):
 C, B, V = bk['C2_c1'], bk['C2_b1'], bk['Y12']
 A = (bk['Y1'] + bk['w12']) & M
 alpha22 = h6 ^ bit(e1, 22) ^ bit(C, 22) ^ bit(B, 22)
 v16 = bit(V, 16) ^ 1 ^ bit(A, 16) ^ row.qv & 1
 return e1 >> 22, (C >> 22) + alpha22, B >> 22, (A >> 16 & 511) + v16, V >> 16 & 511
def c_star(H, meta):
 E22, CA22, B22, A16v, V16 = meta
 zeta = ((((H >> 6) ^ E22) + CA22 ^ B22) >> 1) & 511
 return (Y11 & 511) + (((zeta + A16v) & 511) ^ V16)
def traverse(row, Q, y, E, Ep, kappa, e1, h, states, cnt, meta):
 u = bit(e1, 21)
 free = set(row.free) - ({15} if meta else set())
 keys = {i: descriptor(row, Q, y, E, Ep, kappa, i, 1, h[i]) if i in h else
   descriptor(row, Q, y, E, Ep, kappa, i) for i in range(7, 32)}
 pref0, out = sum(h[i] << i for i in range(7)), []
 stack = [(7, uu, aa, pref0, 0) for (uu, aa) in states]
 while stack:
  i, uu, aa, pref, e29 = stack.pop()
  if i == 32:
   cnt[6] += 1
   cnt[7] += U_LEAF
   if is_joint_root(Q, y, E, pref, row):
    out.append(pref)
    cnt[7] += U_ROOT
   continue
  cp = uu << 1 | aa
  if i in free:
   cnt[4] += 1
   cnt[7] += U_FREE
   w = DUAL[keys[i] << 2 | cp]
   arcs = (w & 0x1F, w >> 5 & 0x1F)
  else:
   cnt[0] += 1
   cnt[7] += U_FORCED
   key = keys[i]
   if i == 15 and meta:
    cnt[2] += 1
    cnt[7] += U_G15
    cs = c_star(pref, meta)
    if cs & row.qm & 0xFF != row.qv & 0xFF:
     continue
    arcs = (FORCED[(key | 8 | (cs >> 8 & 1) << 2) << 2 | cp],)
   elif i == 20:
    cnt[1] += 1
    cnt[7] += U_SELECTED
    arcs = (SELECTED[(key << 2 | cp) << 1 | bit(pref, 8)],)
   elif i == 25:
    arcs = (FORCED[(key | 8 | (bit(pref, 6) ^ bit(pref, 13) ^ u) << 2) << 2 | cp],)
   elif i == 29:
    arcs = (FORCED[(key | 8 | (1 ^ e29) << 2) << 2 | cp],)
   else:
    arcs = (FORCED[key << 2 | cp],)
  for arc in arcs:
   if arc:
    stack.append((i + 1, arc >> 3 & 1, arc >> 2 & 1, pref | (arc >> 1 & 1) << i,
       arc & 1 if i == 9 else e29))
 return out
def solve(bk, rows, g15, cnt, notes):
 Q, y, E, e1, C, B = bk['Y9'], bk['Y4'], bk['omega'], bk['e1'], bk['C2_c1'], bk['C2_b1']
 Ep, out = (E + DY3) & M, []
 for j in rows:
  row = ROWS[j]
  kappa = row.sigma ^ row.eps ^ E ^ Ep
  res = row_setup(row, Q, y, E, Ep, e1, kappa, C, B, notes)
  if res is not None:
   meta = g15_meta(res[0][6], e1, bk, row) if g15 else None
   out += [(r, j) for r in traverse(row, Q, y, E, Ep, kappa, e1, res[0], res[1], cnt, meta)]
 return out
def tree(row):
 free, n = [i for i in row.free if i != 15], [0] * 5
 for i in range(7, 32):
  k = 1 << sum(f < i for f in free)
  if i in free:
   n[3] += k
  else:
   n[0] += k
   n[1] += k * (i == 20)
   n[2] += k * (i == 15)
 n[4] = 1 << len(free)
 return n
def families(rows):
 return len(rows)
def rows_of(T):
 return [j for j in range(3) if T >> j & 1]
ROW_CAP = [U_ROW + sum(a * b for a, b in zip(tree(r), (U_FORCED, U_SELECTED, U_G15, U_FREE, U_LEAF + U_ROOT))) for r in ROWS]
CT = [1024 + U_FAMILY * families(rows_of(T)) + sum(ROW_CAP[j] for j in rows_of(T)) if T else 0 for T in range(8)]
A_T = [U_GLOBAL + (U_FAMILY + U_ROW) * len(rows_of(T)) if T else 0 for T in range(8)]
CM = [A_T[T] + sum(ROW_CAP[j] - U_ROW for j in rows_of(T)) for T in range(8)]
CTW = [CM[T] | A_T[T] << 16 for T in range(8)]
assert ROW_CAP == [5162] * 3 and CM[7] == 23012 and CMJ == tuple(CM[1 << j] for j in range(3))
assert CAPX == CM[7] + U_SC0 + 3 * U_SC1 + U_PRE and all(31 not in r.free for r in ROWS)
def compress2(msg, t, flags):
 n = len(msg)
 w = list(struct.unpack('<16I', msg + bytes(64 - n)))
 v = list(IV) + list(IV[:4]) + [t & M, t >> 32, n, flags]
 s, yst = w, None
 for r in range(2):
  for i, (a, b, c, d) in enumerate(GCALLS):
   if r == 1 and i == 4:
    yst = list(v)
   v[a], v[b], v[c], v[d] = g(v[a], v[b], v[c], v[d], s[2 * i], s[2 * i + 1])
  s = [s[p] for p in PERM]
 return w, [v[i] ^ v[i + 8] for i in range(8)], yst
def c1_of(v, h):
 y6 = ror((((rol(h, 16) ^ v['e1']) + v['C2_c1']) & M) ^ v['C2_b1'], 7)
 return (Y11 + ror(((y6 + v['Y1'] + v['w12']) & M) ^ v['Y12'], 16)) & M
def c1_t0(v):
 w0 = (rol(v['K0_d1'], 16) - IV[0] - IV[4]) & M
 y14 = ror(((w0 + v['C2_a1'] + v['C2_b1']) & M) ^ v['C2_d1'], 8)
 return c1_of(v, ror(y14 ^ v['e1'], 16))
def step_ct(v, c1):
 u = dict(v)
 u['E1_a1'] = rol((c1 - Y11) & M, 16) ^ u['Y12']
 u['Y6'] = (u['E1_a1'] - u['Y1'] - u['w12']) & M
 u['Y10'] = rol(u['Y6'], 7) ^ u['C2_b1']
 u['Y14'] = (u['Y10'] - u['C2_c1']) & M
 u['E1_b1'] = ror(u['Y6'] ^ c1, 12)
 u['Y2'] = rol(u['Y14'], 8) ^ u['C2_d1']
 u['E3_h1'] = ror(u['Y14'] ^ u['e1'], 16)
 u['w0'] = (u['Y2'] - u['C2_a1'] - u['C2_b1']) & M
 u['K0_a1'] = (IV[0] + IV[4] + u['w0']) & M
 u['t'] = u.get('thi', 0) << 32 | rol(u['K0_d1'], 16) ^ u['K0_a1']
 u['w1'] = (u['S0'] - u['K0_a1'] - u['K0_b1']) & M
 w = [u.get('w%d' % i, 0) for i in range(16)]
 w[4], w[13] = W4, W13
 b = list(w)
 b[4], b[5] = W4B, (w[5] + DELTA5) & M
 pa, pb = struct.pack('<16I', *w), struct.pack('<16I', *b)
 assert not any(pa[LEN_A:]) and not any(pb[LEN_B:])
 u['A'], u['B'], u['c1'] = pa[:LEN_A], pb[:LEN_B], c1
 return u
def e1_g(y, w):
 a1 = (y[1] + y[6] + w[12]) & M
 d1 = ror(y[12] ^ a1, 16)
 c1 = (y[11] + d1) & M
 b1 = ror(y[6] ^ c1, 12)
 a2 = (a1 + b1 + w[5]) & M
 return a1, b1, c1, d1, a2, (c1 + ror(d1 ^ a2, 8)) & M
def chart(u, flags=FLAGS):
 t = u['t'] if flags == FLAGS else 0
 wa, cva, ya = compress2(u['A'], t, flags)
 wb, cvb, yb = compress2(u['B'], t, flags)
 ea, eb = e1_g(ya, wa), e1_g(yb, wb)
 j = []
 for y_, w_ in ((ya, wa), (yb, wb)):
  a1 = (y_[3] + y_[4] + w_[15]) & M
  d1 = ror(y_[14] ^ a1, 16)
  c1 = (y_[9] + d1) & M
  a2 = (a1 + ror(y_[4] ^ c1, 12) + w_[8]) & M
  j.append((c1, a2, (c1 + ror(d1 ^ a2, 8)) & M, d1))
 cons = (all(ya[i] == u['Y%d' % i] for i in (0, 1, 2, 4, 5, 6, 8, 9, 10, 12, 13, 14))
   and (ya[3], ya[11], yb[3], yb[11], yb[4]) == (Y3, Y11, Y3B, Y11B, u['Y4'])
   and (ea[2], ea[1], j[0][3]) == (u['c1'], u['E1_b1'], u['E3_h1']))
 return dict(cons=cons, ea=ea, eb=eb, j=tuple(j[0][k] ^ j[1][k] for k in range(3)), cva=cva, cvb=cvb)
def pvals(bk, h, row):
 y14 = rol(h, 16) ^ bk['e1']
 t = bk.get('thi', 0) << 32 | rol(bk['K0_d1'], 16) ^ ((IV[0] + IV[4] + (rol(y14, 8) ^ bk['C2_d1']) - bk['C2_a1'] - bk['C2_b1']) & M)
 y6 = ror(((y14 + bk['C2_c1']) & M) ^ bk['C2_b1'], 7)
 a1 = (y6 + bk['Y1'] + bk['w12']) & M
 d = ror(a1 ^ bk['Y12'], 16)
 c = (Y11 + d) & M
 b = ror(y6 ^ c, 12)
 a = (a1 + b + bk['w5']) & M
 return t, c, a, b, b & row.beta, d, ror(d ^ a, 8)
def test_a(a, s, row):
 return a & row.tau == ((row.tau - row.beta + 8 + 2 * s) & M) >> 1
def test_c(c, z, row):
 return ((c + z) & M) ^ ((((c + DY11) & M) + (z ^ ror(row.tau, 8))) & M) == row.eps
def predicate(bk, h, j):
 row = ROWS[j]
 t, c, a, b, s, d, z = pvals(bk, h, row)
 return (t != 0 and c & row.qm == row.qv and test_a(a, s, row) and test_c(c, z, row)), c, t
def cert_full(v, h, j):
 row, c1 = ROWS[j], c1_of(v, h)
 u = step_ct(v, c1)
 if c1 & row.qm != row.qv or u['t'] == 0:
  return False
 r = chart(u)
 return (r['cons'] and r['j'] == (row.theta, row.eps, row.tau) and r['cva'] == r['cvb']
   and (r['ea'][4] ^ r['eb'][4], r['ea'][5] ^ r['eb'][5], r['ea'][1] ^ r['eb'][1]) == (row.tau, row.eps, row.beta))
def chart_check(v, c1, row):
 u = step_ct(v, c1)
 r, h = chart(u), u['E3_h1']
 t, c, a, b, s, d, z = pvals(v, h, row)
 ea, eb = r['ea'], r['eb']
 Q, y, E = v['Y9'], v['Y4'], v['omega']
 ga, gb = (Q + h) & M, (Q + (h ^ ETA)) & M
 fa, fb = (E + ror(y ^ ga, 12)) & M, (E + DY3 + ror(y ^ gb, 12)) & M
 ok = (r['cons'] and all(r['cva'][i] == r['cvb'][i] for i in (0, 2, 5, 7))
  and r['j'] == (ga ^ gb, fa ^ fb, ((ga + ror(h ^ fa, 8)) ^ (gb + ror(h ^ ETA ^ fb, 8))) & M)
  and (t, c, a, b, d) == (u['t'], c1, ea[4], ea[1], ea[3]) and eb[1] == b ^ row.beta
  and eb[4] == (a + row.beta - 2 * s - 8) & M and eb[5] == (c + DY11 + ror(d ^ eb[4], 8)) & M
  and test_a(a, s, row) == (ea[4] ^ eb[4] == TAU))
 if ok and ea[4] ^ eb[4] == TAU:
  ok = test_c(c, z, row) == (ea[5] ^ eb[5] == row.eps)
 x14 = rol(h, 16) ^ v['e1']
 y6 = ror(((x14 + v['C2_c1']) & M) ^ v['C2_b1'], 7)
 A = (v['Y1'] + v['w12']) & M
 meta = g15_meta(bit(h, 6), v['e1'], v, row)
 g15 = (((x14 + v['C2_c1']) ^ x14 ^ v['C2_c1']) >> 22 & 1) == meta[1] - (v['C2_c1'] >> 22) and \
  (((y6 + A) ^ y6 ^ A) >> 16 & 1) == meta[3] - (A >> 16 & 511)
 if g15:
  cs = c_star(h & 0x7FFF, meta)
  ok = ok and cs & row.qm & 0xFF == row.qv & 0xFF and cs >> 8 & 1 == bit(h, 15)
 return ok, g15
L31, PLANT_EVERY = 0x7FFFFFFF, 8
SOLS = {}
class Rng:
 def __init__(self, seed):
  self.s = int.from_bytes(hashlib.sha256(b'frontline plant' + seed).digest()[:8], 'little')
 def __call__(self, n=32):
  self.s = (self.s + 0x9E3779B97F4A7C15) & (1 << 64) - 1
  z = (self.s ^ self.s >> 30) * 0xBF58476D1CE4E5B9 & (1 << 64) - 1
  z = (z ^ z >> 27) * 0x94D049BB133111EB & (1 << 64) - 1
  return (z ^ z >> 31) & (1 << n) - 1
def jroot_words(Q, y, E, h, row):
 ga, gb = (Q + h) & M, (Q + (h ^ ETA)) & M
 fa, fb = (E + ror(y ^ ga, 12)) & M, (E + DY3 + ror(y ^ gb, 12)) & M
 return (ga ^ gb == row.theta and fa ^ fb == row.eps
   and ((ga + ror(h ^ fa, 8)) ^ (gb + ror(h ^ ETA ^ fb, 8))) & M == row.tau)
def low_sample(rng, c, free, fixed, target):
 feas = [None] * 31 + [(1, 1)]
 def opts(i, cin):
  r = []
  for a in ((0, 1) if free >> i & 1 else (fixed >> i & 1,)):
   co = maj(a, c >> i & 1, cin)
   if (target >> i & 1 or not (a ^ c >> i ^ cin) & 1) and feas[i + 1][co]:
    r.append((a, co))
  return r
 for i in range(30, -1, -1):
  feas[i] = (len(opts(i, 0)) > 0, len(opts(i, 1)) > 0)
 if not feas[0][0]:
  return None
 a = cin = 0
 for i in range(31):
  o = opts(i, cin)
  b_, cin = o[rng(1) % len(o)]
  a |= b_ << i
 return a
def plant(row, rng):
 tau, EPS, MU = row.tau, row.eps, row.mu
 s = tau ^ ror(tau, 1)
 th = rol(s, 12)
 k1, k2, k3 = (ETA - th & M) >> 1, (EPS - DY3 - s & M) >> 1, (tau - th - MU & M) >> 1
 if tau not in SOLS:
  s1, x = [], ETA & L31
  while True:
   if not (x - k1) & L31 & ~th:
    s1.append((x, (x - k1) & L31))
   if not x:
    break
   x = (x - 1) & ETA & L31
  SOLS[tau] = s1
 both = ETA & EPS & L31
 fixm = ror(both, 8)
 for _ in range(64):
  e1 = CLASS_VALUE | rng() & FREE_MASK
  y = (e1 - Y3) & M
  opts = [(x, gf) for x, gt in SOLS[tau] for gf in ((gt, gt | 1 << 31) if th >> 31 else (gt,))
    if not ((ror((y ^ gf) & th, 12) & L31) + k2) & L31 & ~EPS]
  if not opts:
   continue
  x, gf = opts[rng() % len(opts)]
  ee = ((ror((y ^ gf) & th, 12) & L31) + k2) & L31
  fv = ror((x ^ ee) & both, 8)
  m = low_sample(rng, (k3 + gf) & L31, MU & L31 & ~fixm, fv & MU, tau & L31)
  if m is None:
   continue
  pt = (k3 + gf + m) & L31
  for _ in range(1 << 14):
   g_ = rng() & ~th & M | gf
   h2 = rng() & ~(MU & L31 | fixm) & M | m | fv
   p = (g_ + h2) & M
   if p & tau & L31 == pt and p ^ ((g_ ^ th) + (h2 ^ MU)) & M == tau:
    break
  else:
   continue
  r8, ep = rol(h2, 8), EPS & L31 & ~ETA
  h = rng() & ~(ETA & L31) & M | x
  h = h & ~ep & M | (r8 ^ ee) & ep
  Q, E = (g_ - h) & M, ((r8 ^ h) - ror(y ^ g_, 12)) & M
  if not jroot_words(Q, y, E, h, row):
   continue
  C = rng()
  S_ = ((rol(h, 16) ^ e1) + C) & M
  B = rng() & ~(3 << 22) & M | bit(S_, 22) << 22 | (bit(S_, 23) ^ 1) << 23
  Y1, A = rng(), rng()
  cc = row.qv | rng() & ~row.qm & M
  return dict(Y9=Q, Y4=y, omega=E, e1=e1, C2_c1=C, C2_b1=B, Y1=Y1, w12=(A - Y1) & M,
     Y12=rol((cc - Y11) & M, 16) ^ (ror(S_ ^ B, 7) + A) & M), h
 return None
def plant_check(seed, k):
 j = k // PLANT_EVERY % 3
 r = plant(ROWS[j], Rng(seed))
 if r is None:
  return 1, 1
 bk, h = r
 j = j if ROWS[j].cfix is None else 2 - bit(h, 2)
 cnt = [0] * 8
 new, old = solve(bk, [j], True, cnt, []), solve(bk, [j], False, [0] * 8, [])
 scr = screen(bk['Y9'], bk['Y4'], bk['omega'], bk['e1'], j)
 units = (U_GLOBAL + U_FAMILY + U_ROW + U_FORCED * cnt[0] + U_SELECTED * cnt[1] + U_G15 * cnt[2] + U_FREE * cnt[4]
   + U_LEAF * cnt[6] + U_ROOT * len(new))
 T = 1 << j
 bad = (((h, j) not in new) + (not kept(bk['omega'], bk['Y4'], bk['e1'])) + ((h, j) not in old) + (not set(new) <= set(old)) + (not scr)
  + (not all(jroot_words(bk['Y9'], bk['Y4'], bk['omega'], h_, ROWS[j_]) for h_, j_ in old)) + (units > CT[T])
  + meter_bad(U_GLOBAL + U_FAMILY + U_ROW + cnt[7], units, T))
 return bad, 8
def meter_bad(d, units, T):
 return d != units or d > CM[T]
OBS = ('blocks', 'live', 'ranges', 'words', 'e_lanes', 'passes', 'prechecked', 'solver_calls', 'roots',
 'certified', 'units', 'solver_units', 'checks', 'mismatches', 'halted', 'live_steps')
OBS_X = ('members', 'block_steps', 'pieces', 'partial_words', 'setup', 'lane_slots', 'leaves', 'solver_debits',
  'scans', 'screen_debits', 'screened_out', 'pf_words', 'pf_skipped', 'listed')
class Halt(Exception):
 pass
class Found(Exception):
 pass
def steps23(ow, y, e1, T, o, A, bk, thi=0):
 v = rebuild(ow, y, e1, thi=thi)
 rows = rows_of(T)
 bad0 = A != U_GLOBAL + U_FAMILY * families(rows) + U_ROW * len(rows)
 bad0 += any(bk[k] != v[k] for k in bk)
 cnt, notes = [0] * 8, []
 roots = solve(bk, rows, True, cnt, notes)
 d = A + cnt[7]
 units = (A + U_FORCED * cnt[0] + U_SELECTED * cnt[1] + U_G15 * cnt[2] + U_FREE * cnt[4] + U_LEAF * cnt[6]
   + U_ROOT * len(roots))
 o['units'] += d
 o['solver_units'] += units
 o['leaves'] += cnt[6]
 o['roots'] += len(roots)
 old = solve(v, rows, False, [0] * 8, [])
 full = {r for r in old if cert_full(v, *r)}
 bad = (bad0 + len(set(roots) - set(old)) + len(full - set(roots)) + (units > CT[T]) + len(notes)
  + meter_bad(d, units, T))
 found = None
 for h, j in roots:
  ok, c, t = predicate(bk, h, j)
  bad += ok != ((h, j) in full)
  if ok:
   o['certified'] += 1
   found = found or (c, t)
 if found:
  u = step_ct(v, found[0])
  cva, cvb = compress2(u['A'], u['t'], FLAGS)[1], compress2(u['B'], u['t'], FLAGS)[1]
  bad += u['t'] != found[1] or cva != cvb
  if cva == cvb:
   o['mismatches'] += bad
   raise Found(u)
 return bad, d
def bc(w):
 w |= w << 36
 w |= w << 72
 return w | w << 108
_L16, _LISTS, KN, _KEPT = {}, {}, {}, {}
_D = 0xFFFE0000007FFFFFFF8000000001FFFF
KD = ({1280: 0xFFFC000000FFFFFFFF0000000003FFFF, 1792: 1 << 87, 2560: _D}, {1792: 0xFFFE000000FFFFFFFF8000000001FFFF},
 {2048: _D}, {1536: _D, 1792: 1 << 113, 2304: _D}, {1792: 0xFFFE000000FFFFFFFF0000000003FFFF})
KC = (0, 1, 0, 2, 3, 2, 3, 4)
def level16(t=0):
 if t not in _L16:
  f, p3, p16 = F2T[t], {}, {}
  st = [f[f[lo & 255] + (lo >> 8)] for lo in range(1 << 16)]
  for s2 in sorted(set(st)):
   bm = bytearray(1 << 16)
   for b2 in range(256):
    s3 = f[s2 + b2]
    if s3 not in p3:
     p3[s3] = [b3 << 8 for b3 in range(256) if f[s3 + b3]]
    for h in p3[s3]:
     bm[b2 | h] = 1
   p16[s2] = bm
  dead = [s2 for s2 in p16 if not any(p16[s2])]
  assert len(p16) == 7 and len(dead) == 1
  _L16[t] = (st, p16, dead[0])
 return _L16[t]
def get_lists(t=0, k=0):
 if (t, k) not in KN:
  f, (st, p16, dead), KN[t, k] = F2T[t], level16(t), {}
  for s2, bm in p16.items():
   dm = KD[k].get(s2, 0)
   if s2 == dead or (t, s2, dm) in _LISTS:
    KN[t, k][s2] = _LISTS.get((t, s2, dm))
    continue
   bm = bytes(bm[h] > dm >> (h & 127) & 1 for h in range(1 << 16))
   hs = [h for h in range(1 << 16) if bm[h]]
   pc, c = [0] * ((1 << 17) + 1), 0
   for h in range(1 << 17):
    pc[h] = c
    if bm[h & 0xFFFF]:
     c += 1
   pc[1 << 17] = c
   hs, words = hs + hs, []
   for q in range(0, len(hs), 7):
    v = 0
    for i, h in enumerate(hs[q:q + 7]):
     v |= (h | (f[f[s2 + (h & 255)] + (h >> 8)]) << 16) << LB * i
    words.append(v)
   KN[t, k][s2] = _LISTS[t, s2, dm] = (words, pc)
  _KEPT[t, k] = sum(level16(t)[0].count(s2) * v[1][1 << 16] for s2, v in KN[t, k].items() if v)
 return KN[t, k]
def kept_count(t, k):
 get_lists(t, k)
 return _KEPT[t, k]
def kept(E, y, e1):
 t = (y >> 4 ^ y >> 5) & 1
 s2 = level16(t)[0][E & 0xFFFF]
 return level16(t)[1][s2][E >> 16] > KD[KC[e1 >> 2 & 1 | e1 >> 25 & 6]].get(s2, 0) >> (E >> 16 & 127) & 1
SG = TAU ^ ror(TAU, 1)
TH = rol(SG, 12)
def _s1(j, g, s, h):
 b, c = s & 1, s >> 1
 q, e = g ^ h ^ b, h ^ (ETA >> j & 1)
 if q ^ e ^ c != g ^ (TH >> j & 1):
  return -1
 return (~g & h | ~(g ^ h) & b) & 1 | maj(q, e, c) << 1
def _s3(mu, j, g, s, h):
 a, b = s & 1, s >> 1
 x, m = g ^ (TH >> j & 1), h ^ (mu >> j & 1)
 if g ^ h ^ a ^ x ^ m ^ b != TAU >> j & 1:
  return -1
 return maj(g, h, a) | maj(x, m, b) << 1
_AT, _H = {}, {}
def _nx(fn, st, *a):
 return sum(1 << n for n in {fn(*a, s, h) for s in range(4) if st >> s & 1 for h in (0, 1)} if n >= 0)
def _hn(k):
 S, m, mu = k >> 9, k >> 3 & 31, ror(ETA ^ (EPS, EPS2)[k >> 8 & 1], 8)
 return sum(1 << n for n in {G * 16 + n1 + 4 * n3 for G in range(4) for st in range(16) if S >> G * 16 + st & 1
  for h in (0, 1) for n1, n3 in [(_s1(m, k & 1, st & 3, h), _s3(mu, m + 24 & 31, k >> 1 & 1, 0 if m == 8 else st >> 2, h ^ (k >> 2 & 1)))] if n1 >= 0 and n3 >= 0})
# Lemma CP: omega E is alive for member y (J1 to J3 of 9.4)
def alive(E, y):
 Ep = E + DY3 & M
 for ei, ep in enumerate((EPS, EPS2)):
  mu = ror(ETA ^ ep, 8)
  if mu not in _AT:
   _AT[mu] = [[[_nx(_s1, m, j, g) for m in range(16)] for g in (0, 1)] for j in range(32)], [[[_nx(_s3, m, mu, j, g) for m in range(16)] for g in (0, 1)] for j in range(32)]
  P1, P3 = _AT[mu]
  stk = [(0, 0, 0, 0, 15, 15)]
  while stk:
   i, f, a, b, m1, m3 = stk.pop()
   if i == 32:
    g = (f << 12 | f >> 20) & M ^ y
    g8, e2, S = (g << 8 | g >> 24) & M, E + f & M, 1 | 1 << 20 | 1 << 40 | 1 << 60
    for m in range(32):
     k = S << 9 | ei << 8 | m << 3 | g >> m & 1 | (g8 >> m & 1) << 1 | (e2 >> m & 1) << 2
     if k not in _H:
      _H[k] = _hn(k)
     S = _H[k]
     if not S:
      break
    if S & 0xF0000F0000F0000F:
     return True
    continue
   if ((E ^ Ep ^ SG ^ ep) >> i ^ a ^ b) & 1:
    continue
   j = i + 12 & 31
   if j == 0:
    m1 = m3 = 1
   for fb in (1, 0):
    gb = fb ^ (y >> j & 1)
    n1, n3 = P1[j][gb][m1], P3[j][gb][m3]
    if n1 and n3:
     stk.append((i + 1, f | fb << i, maj(E >> i & 1, fb, a), maj(Ep >> i & 1, fb ^ (SG >> i & 1), b), n1, n3))
 return False
_LV = {}
def cut_words(rng, km, n, keep):
 e1, y = member(km)
 t = TYPE16[km & 15]
 st, p16, dead = level16(t)
 if t not in _LV:
  _LV[t] = [lo for lo in range(1 << 16) if st[lo] != dead]
 out = []
 while len(out) < n:
  lo, h = _LV[t][rng() % LIVE16], rng(16)
  if p16[st[lo]][h] and kept(lo | h << 16, y, e1) == keep:
   out.append((lo | h << 16, y))
 return out
def dyadic(a, b):
 out, x, end, ops = [], a, b + 1, 0
 while True:
  ops += 2
  if not x < end:
   break
  lb = (x & -x) if x else (1 << 16)
  ops += 4
  sz = lb
  while True:
   ops += 3
   if x + sz <= end:
    break
   sz >>= 1
   ops += 1
  out.append((x, sz))
  x += sz
  ops += 1
 return out, ops
def cut16(L0, first):
 out = []
 if first:
  t = L0 + 1
  while t:
   l = t & -t
   t -= l
   out.append((t, l))
 else:
  x = L0 + 1
  while x < 1 << 16:
   l = x & -x
   out.append((x, l))
   x += l
 return out
def ref_check(u, ref):
 c = [ref._compress(IV, struct.unpack('<16I', u[k].ljust(64, b"\0")), u['t'], len(u[k]), FLAGS, 2)[:8] for k in 'AB']
 return all(c[0][i] == c[1][i] for i in (0, 2, 5, 7)) and [tuple(x) for x in c] == [
  tuple(compress2(u[k], u['t'], FLAGS)[1]) for k in 'AB']
def walk_thi(seed, WR=0, credit=CREDIT, words_cap=TRIAL_WORDS, members=MEMBERS, full_every=FULL_EVERY, ref=None):
 sh = hashlib.shake_256(b'frontline context' + seed).digest(160)
 ow = struct.unpack('<7I', sh[:28])
 tm = (1 << TB) - 1
 kms = [struct.unpack('<I', sh[28:32])[0] & 0x7FFFF] + [w & 0x7FFFF for w in struct.unpack(
  '<%dI' % (members - 1), hashlib.shake_256(b'thi members' + seed).digest(4 * (members - 1)))]
 draws = [ROWS[i & 1].qv | w & ~ROWS[i & 1].qm & M for i, w in enumerate(struct.unpack('<32I', sh[32:]))]
 rng = Rng(b'thi walk checks' + seed)
 o = dict.fromkeys(OBS + OBS_X, 0)
 o['units'] = U_CONTEXT
 first, bad, chk, done = None, 0, 0, False
 try:
  if WR > WB:
   raise Halt(1)
  cx = co_ctx(*ow, FLAGS)
  P = operands(cx)
  PF = P[:14] + (P[14] + B34 * ONES, P[15])
  XW, S6, X14 = cx['X2'] + cx['S3'] - cx['K3_a1'] - cx['K3_b1'] & M, cx['S6'], cx['X14']
  S2 = rol(cx['S14'], 8) ^ K2D
  BW = dict(w5=S2 - (K2A + K2B) & M, w12=cx['D2_a1'] - S2 - cx['S7'] & M, K0_d1=cx['K0_d1'])
  C0b1, nC0c1, C0d1, nC0w6 = cx['C0_b1'], -cx['C0_c1'] & M, cx['C0_d1'], -(cx['C0_b1'] + cx['w6']) & M
  K0r = rol(cx['K1_d1'], 16)
  KS, Kb = K0r & tm, K0r & ~tm & M
  KX0 = IV[1] + IV[5] - cx['X4'] - Kb & M
  W3b = cx['S1'] - Kb - cx['K1_b1'] & M
  S15p, NS = cx['S15'] ^ ror(X15, 8), -(cx['S0'] + cx['S5']) & M
  S15L, NSL, NSH = S15p & 0xFFFF, NS & 0xFFFF, NS >> 16
  Spp = S15p >> 16
  SPV = bc(Spp)
  o['units'] += 7
  for km in kms:
   e1, y = member(km)
   typ, cls = TYPE16[km & 15], km & 1 | km >> 12 & 6
   bad += typ != (y >> 4 ^ y >> 5) & 1 or cls != e1 >> 2 & 1 | e1 >> 25 & 6
   st16, p16, dead = level16(typ)
   lists = get_lists(typ, KC[cls])
   bad += kept_count(typ, KC[cls]) != KEPT16[8 * typ + cls]
   Y8 = rol(y, 7) ^ C0b1
   Y12 = Y8 + nC0c1 & M
   Y0 = rol(Y12, 8) ^ C0d1
   C0a1 = Y0 + nC0w6 & M
   X0b = C0a1 + KX0 & M
   DW3 = bc(W3b - X0b & M)
   C0v, Ev = bc(C0a1), bc(e1)
   X1v, w10v = y9_member(C0v, P)
   X1wv = X1v + DW3
   clo, ka0 = (e1 & 0xFFFF) + NSL, (e1 >> 16) + NSH
   L0, hi0 = X0b & 0xFFFF, X0b >> 16
   o['members'] += 1
   o['units'] += U_MEMBER
   v0 = rebuild(ow, y, e1)
   bad += (v0['Y12'], v0['Y0'], v0['C0_a1'], v0['X0'], v0['w3']) != (Y12, Y0, C0a1, X0b - KS & M, W3b - KS & M)
   bs0, bl0 = o['block_steps'], o['blocks']
   for b in range(KB):
    hi = hi0 + 0xFFFF - b & 0xFFFF
    cb = L0 + (b << 16) + 0x10000
    o['blocks'] += 1
    o['block_steps'] += 1 << 16
    o['units'] += U_BLOCK
    tot = clo + (hi ^ S15L)
    lo = tot & 0xFFFF
    ka = ka0 + (tot >> 16) & 0xFFFF
    st2 = st16[lo]
    s7 = S7 >> (int(lo) & 127) & 1
    for x_ in {0, 0xFFFF} | {rng(16) for _ in range(2)}:
     s_ = cb - x_
     rom = co_ref(*ow, y, FLAGS, s_ ^ int(KS))[0]
     bad += (not L0 < s_ <= L0 + (KB << 16) or (s_ ^ int(KS)) >> TB
       or rom != lo | ((x_ ^ Spp) + ka & 0xFFFF) << 16 or (st2 == dead and T2(rom, typ) != 0))
     chk += 1
    if st2 == dead:
     continue
    bad += not s7
    o['live'] += 1
    o['live_steps'] += 1 << 16
    lw, pc = lists[st2]
    n_st = pc[1 << 16]
    nfull = -(-n_st // 7)
    nw = nfull if words_cap is None else min(nfull, words_cap)
    bad += len(lw) < nfull
    WR += U_LIVE_LIST
    o['units'] += U_LIVE_LIST
    KAN = bc((0x10000 - ka) & 0xFFFF)
    SXHV = bc(hi << 16) | SPV
    e0, listed, listed_all = o['e_lanes'], 0, 0
    for w in range(nw):
     i0, i1 = 0, min(n_st - 7 * w, 7)
     listed_all += i1
     o['listed'] += i1
     o['words'] += 1
     o['units'] += U_WORD - U_WT
     WR += U_WORD - U_WT
     o['lane_slots'] += 7
     Hw = lw[w]
     X0v = (Hw + KAN) & M16V ^ SXHV
     Y9_lo, Y1_lo, D0d1p, C1c1, C1d1, t1 = y9_fill_lo(X0v, X0v, X1wv, w10v, PF)
     o['units'] += U_PF
     WR += U_PF
     if ((((Y9_lo ^ PFC) + PF1 & PFF) + PFK) & PFB) == PFB:
      o['pf_skipped'] += 1
      if o['pf_skipped'] % PF_CHECK_EVERY == 0:
       Y9p_chk, _ = y9_fill_hi(Y1_lo, C1c1, C1d1, t1)
       bad += any(T1R(int(Y9p_chk) & QL[i]) for i in range(i0, i1))
       chk += 1
      continue
     Y9p, Y1p = y9_fill_hi(Y1_lo, C1c1, C1d1, t1)
     o['pf_words'] += 1
     o['units'] += U_WT + U_KF
     WR += U_E * 7 + U_WT + U_KF
     cand = []
     for i in range(i0, i1):
      o['e_lanes'] += 1
      o['units'] += U_E_LIST
      sh_ = LB * i
      y9i = Y9p & QL[i]
      m1 = T1R(int(y9i))
      Hwi = int(Hw) >> sh_
      m2, hli = Hwi >> 16 & 0x7F, Hwi & 0xFFFF
      x = m1 & m2
      x0lo = int(X0v) >> sh_ & 0xFFFF
      s_ = cb - x0lo
      thi = s_ ^ int(KS)
      omi = lo | hli << 16
      y9 = int(y9i) >> sh_
      listed += 1
      if o['e_lanes'] % full_every == 0:
       rom, ry9 = co_ref(*ow, y, FLAGS, thi)
       bad += rom != omi or y9 != B34 + ry9 or m1 != mask1_ref(ry9) or m2 != T2(rom, typ) or not kept(rom, y, e1)
       u = step_ct(rebuild(ow, y, e1, thi=thi), draws[o['e_lanes'] & 31])
       wr, _, ys = compress2(u['A'], u['t'], FLAGS)
       bad += (ys[4], ys[9] + B34, (ys[3] + ys[4] + wr[15] + wr[8]) & M) != (y, y9, omi)
       bad += u['t'] >> 32 != thi or 1024 * u['t'] + LEN_B >= 1 << 61
       bad += ref is not None and not ref_check(u, ref)
       chk += 4
      if x:
       cand.append((sh_, x, thi, omi, y9))
     if cand:
      o['scans'] += 1
      o['units'] += U_SCAN
     for sh_, x, thi, omi, y9 in cand:
      o['passes'] += 1
      o['units'] += U_PASS + U_PASS_X
      first = km if first is None else first
      WR += U_PP
      es = Ev >> sh_ & M
      d1c = ((C0v ^ P[4]) >> sh_ ^ M) + X11P & M
      x6 = RT7[RT12[S6 ^ d1c] ^ X11]
      C2a = x6 + XW & M
      C2d = RT16[X14 ^ C2a]
      X10 = ((D0d1p + P[10]) >> sh_) + X15 & M
      C = X10 + C2d & M
      B = RT12[x6 ^ C]
      r = (Y9p >> sh_ + 16 ^ es) & 4 ^ 3
      v = rebuild(ow, y, e1, thi=thi)
      bad += (v['Y9'] + B34, v['omega'], v['C2_c1'], v['C2_b1'], v['C2_a1'], v['C2_d1'], v['Y1'],
        v['Y12'], e1) != (y9, omi, C, B, C2a, C2d, int(Y1p) >> sh_ & M, Y12, es)
      T = x if nu_of(v['Y9'], e1, v['C2_c1'], v['C2_b1']) in (3, 4) else 0
      ok, gc = chart_check(v, draws[2 + o['passes'] % 30], ROWS[o['passes'] & 1])
      bad, chk = bad + (not ok), chk + 3 + gc
      if ((r + C) ^ B ^ 5) + 5 & 6:
       bad += T != 0
       continue
      bad += T != x
      o['prechecked'] += 1
      ds = U_SC0 + U_SC1 * bin(x).count('1') + U_PRE
      if (CTW[x] & 65535) + ds > credit:
       raise Halt(3)
      credit -= ds
      o['screen_debits'] += ds
      o['units'] += ds
      x2 = sum(1 << j for j in rows_of(x) if screen(y9 & M, y, omi, e1, j))
      for j in rows_of(x & ~x2):
       bad += len(solve(v, [j], False, [0] * 8, [])) != 0
       chk += 1
      if not x2:
       o['screened_out'] += 1
       continue
      ct = CTW[x2]
      a = ct >> 16
      o['solver_calls'] += 1
      bk = dict(Y9=y9 & M, Y4=y, omega=omi, e1=e1, C2_a1=C2a, C2_b1=B, C2_c1=C, C2_d1=C2d,
        Y1=int(Y1p) >> sh_ & M, Y12=Y12, thi=thi, **BW)
      oo = dict.fromkeys(('units', 'solver_units', 'leaves', 'roots', 'certified', 'mismatches'), 0)
      try:
       b2, d = steps23(ow, y, e1, x2, oo, a, bk, thi)
      finally:
       for k_ in oo:
        o['solver_debits' if k_ == 'units' else k_] += oo[k_]
       o['units'] += oo['units']
      credit -= d
      bad += b2 + (d != oo['solver_units']) + (d > CM[x2]) + (credit < 0) + (oo['roots'] > oo['leaves'])
      chk += 2
    bad += o['e_lanes'] - e0 != listed or listed_all != min(n_st, 7 * nw)
   bad += o['block_steps'] - bs0 != KB << 16 or o['blocks'] - bl0 != KB
  done = True
 except Halt as e_:
  o['halted'] = e_.args[0]
 except Found:
  pass
 if done:
  bad += (o['e_lanes'] > 7 * o['pf_words'] or o['pf_words'] + o['pf_skipped'] != o['words']
    or o['e_lanes'] > o['lane_slots'] or o['passes'] > o['e_lanes'] or o['scans'] > o['passes']
    or not o['solver_calls'] <= o['prechecked'] <= o['passes']
    or o['solver_debits'] != o['solver_units'] or o['solver_debits'] + o['screen_debits'] > CREDIT
    or o['screened_out'] + o['solver_calls'] != o['prechecked']
    or not o['certified'] <= o['roots'] <= o['leaves'] or o['blocks'] != KB * members
    or o['block_steps'] != members * KB << 16
    or o['units'] != U_CONTEXT + 7 + U_MEMBER * o['members'] + U_BLOCK * o['blocks'] + U_LIVE_LIST * o['live']
    + (U_WORD + U_PF - U_WT) * o['words'] + (U_WT + U_KF) * o['pf_words'] + U_E_LIST * o['e_lanes'] + U_SCAN * o['scans'] + (U_PASS + U_PASS_X) * o['passes']
    + o['solver_debits'] + o['screen_debits'])
 o['mismatches'] += bad
 o['checks'] += chk
 return ow, kms, first, o, WR
def root_pair(ow, k):
 e1, y = member(k)
 v = rebuild(ow, y, e1, ROOT_FLAGS)
 u = step_ct(v, c1_t0(v))
 da, db = compress2(u['A'], 0, ROOT_FLAGS)[1], compress2(u['B'], 0, ROOT_FLAGS)[1]
 return u['A'], u['B'], u['t'] == 0 and all(da[i] == db[i] for i in (0, 2, 5, 7))
def trial(seed, k=0):
 ow, kms, first, o, _ = walk_thi(seed)
 a, b, ok = root_pair(ow, kms[0] if first is None else first)
 o['checks'] += 1
 o['mismatches'] += not ok
 if k % PLANT_EVERY == 0:
  bad, n = plant_check(seed, k)
  o['checks'] += n
  o['mismatches'] += bad
 if k % 8 == 4:
  cw = cut_words(Rng(b'cut check' + seed), kms[k % MEMBERS], 1, False)
  if any(alive(E, y) for E, y in cw):
   raise ValueError('a cut word is alive')
  o['checks'] += len(cw)
 return a, b, {k_: o[k_] for k_ in OBS}
def selftest(n):
 rep = {'constants': TEXT is not None and all(globals()[k] == x for k, x in TEXT.items()) and U_LIVE_LIST == 24 and U_PP == 52}
 tq, te = [(ETA & 255, r.theta & 255) for r in ROWS], [(ror(r.theta, 12) & 255, r.eps & 255) for r in ROWS]
 a1, a2 = automaton(tq, 0, 8)[0], automaton(te, DY3 & 255, 8)[0]
 bf = lambda tg, dy, x: sum(1 << j for j, (dz, out) in enumerate(tg)
       if any(((x + v) ^ (x + dy + (v ^ dz))) & 255 == out for v in range(256)))
 rep['automata_vs_bruteforce_w8'] = sum(a1[x] == bf(tq, 0, x) and a2[x] == bf(te, DY3, x) for x in range(256))
 rep['SHARE_E_COUNT'] = TYPE_E == (23820160, 34028800) and E_COUNT == sum(TYPE_E) // 2 and SHARE == plain_pass() * E_COUNT
 rep['screen_counts'] = PASS1 == (8778240,) * 3 and plain_pass() == 14110208
 rep['cut_all_L0'] = cut_ok()
 rep['type_by_k15'] = all((member(k)[1] >> 4 ^ member(k)[1] >> 5) & 1 == TYPE16[k & 15]
       and member(k)[0] >> 2 & 1 | member(k)[0] >> 25 & 6 == k & 1 | k >> 12 & 6 for k in range(1 << 19))
 rep['class_lists'] = 16 * E_KEPT == sum(KEPT16) == 389525760 and all(kept_count(c >> 3, KC[c & 7]) == KEPT16[c] for c in range(16))
 rr = Rng(b'cut selftest')
 cw, kw = [[w for c in range(16) for w in cut_words(rr, next(km for km in range(1 << 19) if TYPE16[km & 15] == c >> 3 and km & 1 | km >> 12 & 6 == c & 7), 3, q)] for q in (0, 1)]
 rep['cut_words'], rep['kept_words'] = [[len(x), sum(alive(*w) for w in x)] for x in (cw, kw)]
 rnd = hashlib.shake_256(b'frontline selftest').digest(8 * n)
 xs = struct.unpack('<%dI' % (2 * n), rnd)
 rep['T1_T2_vs_bitserial'] = sum(T1(x) == mask1_ref(x) for x in xs)
 al = [any(((w + f) ^ ((w + DY3) + (f ^ s))) & 511 == EPS & 511 for s in set(SIGMAS[j] & 511 for j in range(3))
   for f in range(512)) for w in range(512)]
 rep['S7_partition'] = (sum(al) == 208 and all(al[w] == S7 >> (w & 127) & 1 for w in range(512))
      and all(S7 >> (x & 127) & 1 for x in xs if T2(x)))
 rep['precheck'] = all(((((a >> 16 ^ b) & 4 ^ 3) + c ^ d ^ 5) + 5 & 6 == 0) == (nu_of(a, b, c, d) in (3, 4))
      for a, b, c, d in zip(xs, xs[1:], xs[2:], xs[3:]))
 rep['replicas'] = all(T2R(x << 36 * l) == T2P(x) and T1R(B34 + x << 36 * l) == T1(x) and RT12[x] == ror(x, 12)
      for x in xs[:256] for l in range(7))
 pf = lambda x: ((x ^ 4) + 64 & 0x387) == 0
 rep['prefilter'] = (all(pf(x) == (x & 0x3C7 in (4, 0x3C4)) for x in range(1 << 12))
      and all(not T1(x) or pf(x) for x in xs)
      and all((not pf(x)) == (((((x + B34 << 36 * l) ^ PFC) + PF1 & PFF) + PFK & PFB) == PFB) for x in xs[:64] for l in range(7)))
 rep['level16'] = True
 for q in (0, 1):
  st, p16, dead = level16(q)
  rep['level16'] &= sum(z != dead for z in st) == LIVE16
  rep['level16'] &= sum(p16[st[x]].count(1) for x in range(65536)) == TYPE_E[q]
  rep['level16'] &= all(p16[st[x & 0xFFFF]][x >> 16] == (T2(x, q) > 0) for x in xs)
 fc = [walk_thi(b'full context %d' % s, words_cap=None, full_every=64)[3] for s in range(2)]
 rep['full_contexts'] = [{k: o[k] for k in OBS + OBS_X} for o in fc]
 rep['full_identities'] = sum(o['live'] for o in fc) > 0 and all(
  o['block_steps'] == STEPS_CTX and o['blocks'] == NBLK
  and o['mismatches'] == 0 and o['halted'] == 0 and o['pf_words'] + o['pf_skipped'] == o['words'] and o['e_lanes'] <= 7 * o['pf_words']
  and o['units'] == U_CONTEXT + 7 + U_MEMBER * o['members'] + U_BLOCK * o['blocks'] + U_LIVE_LIST * o['live']
  + (U_WORD + U_PF - U_WT) * o['words'] + (U_WT + U_KF) * o['pf_words'] + U_E_LIST * o['e_lanes'] + U_SCAN * o['scans'] + (U_PASS + U_PASS_X) * o['passes']
  + o['solver_debits'] + o['screen_debits'] for o in fc)
 drills = {}
 for name, kw, code in (('W', dict(WR=WB + 1), 1), ('C', dict(credit=0), 3), ('R', dict(credit=CAPX), 0)):
  for s in range(4096):
   o = walk_thi(b'drill%d' % s, **kw)[3]
   if o['halted'] if code else o['solver_calls']:
    break
  drills[name] = (o['halted'] in (0, 3) and o['solver_calls'] >= 1 and not o['mismatches'] if name == 'R' else
      o['halted'] == code and (o['members'] == 0 and o['units'] == U_CONTEXT if name == 'W'
      else o['solver_calls'] == 0 and o['passes'] >= 1), s)
 _, _, _, o, w = walk_thi(b'drill%d' % drills['R'][1], WR=WB)
 drills['WB'] = (o['halted'] == 0 and WB < w <= WB + W_CTX and not o['mismatches'], drills['R'][1])
 rep['halt_drills'] = drills
 rep['ok'] = (rep['constants'] and rep['automata_vs_bruteforce_w8'] == 256 and rep['SHARE_E_COUNT'] and rep['precheck']
    and rep['screen_counts'] and rep['cut_all_L0'] and rep['type_by_k15'] and rep['class_lists']
    and rep['T1_T2_vs_bitserial'] == 2 * n and rep['S7_partition'] and rep['replicas'] and rep['level16'] and rep['prefilter']
    and rep['cut_words'][1] == 0 and rep['full_identities'] and all(d[0] for d in drills.values()))
 json.dump(rep, sys.stdout, separators=(',', ':'))
 sys.stdout.write("\n")
 return 0 if rep['ok'] else 1
def main():
 if len(sys.argv) > 1:
  if sys.argv[1] != '--selftest':
   raise SystemExit('usage: frontline.py [--selftest [N]]   (else: organizer request on stdin)')
  raise SystemExit(selftest(int(sys.argv[2]) if len(sys.argv) > 2 else 2000))
 request = json.load(sys.stdin)
 if request['schema_version'] != 1 or request['target_profile'] != 'blake3-r2-prefix-v1':
  raise ValueError('unexpected organizer target')
 if request['event'].get('kind') != 'digest-xor-mask' or request['experiment_id'] != 'frontline-search':
  raise ValueError('unexpected organizer event or experiment')
 trials = []
 for tr in request['trials']:
  a, b, obs = trial(bytes.fromhex(tr['seed']), tr['trial'])
  trials.append({'trial': tr['trial'], 'message_a_hex': a.hex(), 'message_b_hex': b.hex(), 'observations': obs})
 json.dump({'schema_version': 1, 'trials': trials}, sys.stdout, separators=(',', ':'), sort_keys=True)
 sys.stdout.write("\n")
if __name__ == '__main__':
 main()
