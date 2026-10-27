"""frontline.py: the counter search of proof.md 9.1, 9.8, 9.9 and amendments J to Q (flags 3, counter t by step CT; a trial is one context and one block).
Standard library only.  python3 frontline.py < request   |   python3 frontline.py --selftest
"""
import hashlib
import json
import struct
import sys
from math import isqrt

M = 0xFFFFFFFF
IV = (0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A, 0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19)
K = (IV[2] + IV[6]) & M
LEN_A, LEN_B = 55, 63
X3, X7, X11, X15 = 0xBF1C5F38, 0xC0E3A0C8, 0xC4036000, 0xC0C5FB02
W4, W13 = 0x7FFFFFFA, 0x00074004
W4B = (((W4 + K) & M) ^ LEN_A ^ LEN_B) - K & M
DELTA5 = (W4 - W4B) & M
ETA, EPS, MU, BETA = 0x830303CF, 0x6E21BE55, 0x9AED22BD, 0x18B0E098
FLAGS, ROOT_FLAGS = 3, 11
PERM = (2, 6, 3, 10, 7, 0, 4, 13, 1, 11, 12, 5, 9, 14, 15, 8)
GCALLS = ((0, 4, 8, 12), (1, 5, 9, 13), (2, 6, 10, 14), (3, 7, 11, 15),
          (0, 5, 10, 15), (1, 6, 11, 12), (2, 7, 8, 13), (3, 4, 9, 14))
TRIAL_BLOCKS = 1
T2_EVERY = 1


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
assert (Y7, Y15) == (Y7B, Y15B) and (Y3, DY3, Y11, DY11) == (0xFF27C181, 0x01B77CFD, 0x84F77F38, 0xF608818B)
assert DELTA5 == (-8) & M and ror(ETA ^ EPS, 8) == MU

CLASS_MASK, CLASS_VALUE, FREE_MASK = 0x03CF8303, 0x010C0303, 0xFC307CFC
CLASS_FREE = [i for i in range(32) if FREE_MASK >> i & 1]
SPL = [sum((k >> n & 1) << i for n, i in enumerate(CLASS_FREE)) for k in range(1024)]
SPH = [sum((k >> n & 1) << CLASS_FREE[n + 10] for n in range(9)) for k in range(512)]


def member(k):
  e1 = CLASS_VALUE | SPL[k & 1023] | SPH[k >> 10]
  return e1, (e1 - Y3) & M


def cmember(g, j):
  k = g & 63 | j << 6 | g >> 6 << 11
  return member(k) + (k,)


TAUS = (0x175020A0, 0x185020A0, 0x275020A0, 0x285020A0, 0x385020A0, 0x675020A0, 0x685020A0)
S_MASK = 0x5F
LOW_TAUS = {0x175020A0, 0x275020A0, 0x675020A0}
VMASK = [0, 0, 0x3F80, 0x3FFF, 0x3FFF, 0x3F80, 0, 0]
QSTAR_MASK, QSTAR_VALUE = 0x0E09818B, 0x0C008000
SHARE, E_COUNT = 18289159183466496, 233715456
ONCE = sum((2 ** 21, 2 ** 25, 2 ** 27, 2 ** 26, 2 ** 20, 2 ** 20, 2 ** 20, 4 * 2 ** 26, 2 ** 50, 40,
      11 * 2 ** 20, 2 ** 34, 3 * 2 ** 20, 14 * 2 ** 20, 2 * 2 ** 22, 2 ** 29, 2 ** 28, 2 ** 20, 2 ** 22, 2 ** 19))
S_OLD = 116 * 5 * 2 ** 53 + 116 * (2 ** 51 + 2 ** 10) + 2 ** 50
U_GLOBAL, U_FAMILY, U_ROW, U_FORCED, U_SELECTED, U_G15, U_FREE, U_LEAF, U_ROOT = 184, 0, 1089, 16, 0, 11, 17, 35, 88
CM_MAX = 7115
U_U = 65117111395830  # amendment F: declared mean of the refunded ledger per outer step, over 2^48
FACTOR = 98 * 138512695296 // 100
RUN_CONTEXTS = -(-(-(-(12359 << 128) // (25000 * FACTOR * ((1 << 21) - 1)))) >> 19)
RUN_STEPS = RUN_CONTEXTS << 19
_S = isqrt(10 * RUN_CONTEXTS - 1) + 1
PASS_BUDGET = -(-(1000176 * RUN_STEPS * SHARE) // (10 ** 6 << 64)) + (_S << 19)
_MC, _LC = -(-(RUN_STEPS * U_U) >> 48), CM_MAX << 19
CREDIT = _MC + isqrt(40 * _LC * _MC - 1) + 1 + 14 * _LC + CM_MAX
CALL_BUDGET = -(-_MC // (U_GLOBAL + 68)) + (_S << 19)
FB_BUDGET = -(-9 * RUN_CONTEXTS // 4) + (_S << 7)
U_REP_T2, U_E, U_FILL, U_PASS, U_CALL, U_IX, U_PART, U_PART_TAIL, U_BOOK, U_SEL = 8, 10, 56, 43, 6, 18, 72, 40, 3, 5
U_BCAST, U_CHUNK_A, U_CHUNK_B, U_PAIR, U_HDR, U_PL = 5, 11, 13, 104, 32, 8  # D: two chunk headers, 8 per partner lane walked
U_LIVE, U_BN, U_BL, U_M2, U_PRE, U_T1, L_Z = 89, 17, 16, 10, 3, 9, 693450  # J to Q (no test of H, I or K, code at each site); premise H_LZ
U_RET = 14  # entry into and return from the copy of the straddling path (C, O): no statement here
U_BT, U_CMB, U_BSL, U_LB, U_ER, U_FR, U_N0 = (31, 41), 10, 8, 4 + 4 * (5 + 17 + U_IX), U_E + 2, U_FILL + 1, 2688  # N, P
U_SC = 4 + U_REP_T2 + U_ER + 9 + 4 * U_PART + U_PART_TAIL + 5 * U_FILL + 31 * U_E + 25 + U_RET + 1  # N, P: a straddling cluster
U_OPEN = U_REP_T2 + U_BOOK + U_SEL + U_BCAST + U_HDR + U_CHUNK_A + U_CHUNK_B + U_RET
Z_BLK = U_BT[1] + U_CMB + U_BSL + U_LB + 26 * (U_LIVE + U_BN + 2 * U_BL + 9 * (U_PRE + U_T1 + U_M2))
Z_MAX = 256 * Z_BLK
Z_BUDGET = L_Z * RUN_CONTEXTS + Z_MAX * _S
U_PC = U_PASS + U_CALL
U_CONTEXT = 509 + 160 + 12800 + 16 + 3 + 64 + 83 + U_N0 + 2
WB = U_PASS * PASS_BUDGET + U_CALL * CALL_BUDGET + U_SC * FB_BUDGET + Z_BUDGET
W_CTX = U_PC * (1 << 19) + U_SC * 128 + Z_MAX
N = U_CONTEXT * (RUN_CONTEXTS + 1) + WB + W_CTX + CREDIT + ONCE + S_OLD + 430 * 2 ** 38
_C = lambda n: n and 16 + 8 * n
assert U_PAIR == max(_C(a) + _C(b) for a in range(1, 8) for b in range(8) if a + b < 10) and U_PART == _C(7)
assert U_OPEN == 91 == U_LIVE + 5 + U_REP_T2 - 1 + U_RET + 16 + 6 + U_CHUNK_B - 3 - U_FILL and U_PAIR == U_HDR + 9 * U_PL and U_PART_TAIL == _C(3) and U_FILL == 54 + 2
assert U_IX == 9 + 4 + 1 + 3 + 1 and U_PASS == 1 + 35 + 7 and U_BCAST == 2 + 1 + 2 and (U_CONTEXT, U_LB, U_SC, Z_BLK) == (16325, 164, 991, 8959)
assert ONCE == 1125918441996328 + 2 ** 21
assert S_OLD == 5486510246044225536
assert _MC == 136707627336736912199 and (WB, W_CTX) == (812565113579960297603, 28110464) and N == 973165132973595978672
TEXT = dict(RUN_CONTEXTS=1127113088900472, PASS_BUDGET=586042493902474223, CREDIT=136712143855319043944,
      CALL_BUDGET=542546246010770826, FB_BUDGET=2536018039220686, Z_BUDGET=781596814989221581232,
      N=973165132973595978672)



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
  ('C0.a1', Sum('Y0', Neg('C0.b1'), Neg('w6'))), ('K1.a1', L('K1.d1', 16)),
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
co_full = compile_lines('co_full', ARGS + ['Y4', 'fl'], [n for n, _ in LINES], 'locals()')
co_ref = compile_lines('co_ref', ARGS + ['Y4', 'fl'], [n for n, _ in LINES], '(%d + Y4 + w8) & M, Y9' % Y3)
co_ctx = compile_lines('co_ctx', ARGS + ['fl'], CONTEXT_LINES, 'locals()')


def rebuild(ow, y, e1, fl=FLAGS):
  v = co_full(*ow, y, fl)
  v['e1'], v['omega'] = e1, (Y3 + y + v['w8']) & M
  return v


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


THETAS = [theta_of(t) for t in TAUS]
SIGMAS = [t ^ ror(t, 1) for t in TAUS]
AUT1 = automaton([(ETA, x) for x in THETAS], 0)
AUT2 = automaton([(ror(x, 12), EPS) for x in THETAS], DY3)
AUT1[3], AUT2[3] = [m & S_MASK for m in AUT1[3]], [m & S_MASK for m in AUT2[3]]
F1, F2 = flat(AUT1), flat(AUT2)


def T1(x):
  f = F1
  return f[f[f[f[x & 255] + (x >> 8 & 255)] + (x >> 16 & 255)] + (x >> 24)]


def T2(x):
  f = F2
  return f[f[f[f[x & 255] + (x >> 8 & 255)] + (x >> 16 & 255)] + (x >> 24)]


B33, B34, B35, M26, L16 = 1 << 33, 1 << 34, 1 << 35, (1 << 26) - 1, 0xFFFF
S2B, T3B, K7 = len(AUT2[0]) + len(AUT2[1]), len(F1) - len(AUT1[3]), ror(X11, 7)
S1B, B1 = len(AUT1[0]) + len(AUT1[1]), B34 + (1 << 26)


def classes(f, sb, n, w):
  k = [tuple(tuple(f[t:t + w]) for t in f[sb + 256 * s:sb + 256 * s + 256]) for s in range(n)]
  u = list(dict.fromkeys(k))
  return [u.index(x) for x in k], [k.index(x) for x in u]


C1, P1 = classes(F1, S1B, 43, 4)
C2, P2 = classes(F2, S2B, 7, 256)
HE16 = [0] * 65536  # amendments H and N
for _s in P2:
  for _h in range(1 << 16):
    HE16[_h] |= F2[F2[S2B + 256 * _s + (_h & 255)] + (_h >> 8)] > 0
HCNT = (33696, 35424, 34560)
HWT, HMT = [HE16[h - 1] | HE16[h] | HE16[h + 1 & 65535] for h in range(65536)], [HE16[h - 1] | HE16[h] for h in range(65536)]


def R1(f):
  assert B33 <= f < 1 << 36
  lo = f - B34
  assert lo >> 16 == 0
  return B1 + C1[F1[F1[lo & 255] + (lo >> 8)] - S1B >> 8] - lo


def L1(f):
  assert B33 <= f < 1 << 36
  v, h = f - B1 & L16, f - B1 >> 16
  assert v < 35 and h >> 10 == 0
  return F1[F1[S1B + 256 * P1[v] + (h & 255)] + (h >> 8)]


def R2(f):
  assert B33 <= f < 1 << 36
  lo = f - B35
  assert lo >> 16 == 0
  return B33 + C2[F2[F2[lo & 255] + (lo >> 8)] - S2B >> 8] - lo


def L2(f):
  assert B33 <= f < 1 << 36
  v, h = f - B33 & L16, f - B33 >> 16
  assert v < 4 and h >> 16 == 0
  return F2[F2[S2B + 256 * P2[v] + (h & 255)] + (h >> 8)]


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


TR2 = [0] * 256
for _k in range(256):
  for _a in range(4):
    if _k >> _a & 1 and (_a >> 1) ^ (_a & 1) == _k >> 7:
      for _f in (0, 1):
        TR2[_k] |= 1 << 2 * maj(_k >> 4 & 1, _f, _a >> 1) + maj(_k >> 5 & 1, _f ^ (_k >> 6 & 1), _a & 1)


def group_table(nb):
  tab = [0] * (16 << 4 * nb)
  for st in range(16):
    for inp in range(1 << 4 * nb):
      s = st
      for k in range(nb):
        s = TR2[s | (inp >> k & 1) << 4 | (inp >> nb + k & 1) << 5 | (inp >> 2 * nb + k & 1) << 6
            | (inp >> 3 * nb + k & 1) << 7]
      tab[st | inp << 4] = s
  return tab


G3, G2 = group_table(3), group_table(2)
SIG3 = [(j, [(SIGMAS[j] >> i & 7) * 0x240 for i in range(0, 30, 3)], (SIGMAS[j] >> 30) * 0x50)
    for j in range(7) if S_MASK >> j & 1]


def mask1_ref(x):
  return sum(cond1(x, THETAS[j]) << j for j in range(7) if S_MASK >> j & 1)


def mask2_ref(x):
  xd = (x + DY3) & M
  r0 = EPS ^ x ^ xd
  base = [(x >> i & 7) | (xd >> i & 7) << 3 | (r0 >> i & 7) << 9 for i in range(0, 30, 3)]
  tail, m = x >> 30 | (xd >> 30) << 2 | (r0 >> 30) << 6, 0
  for j, sg, st2 in SIG3:
    st = 1
    for bg, sx in zip(base, sg):
      st = G3[st | (bg ^ sx) << 4]
      if not st:
        break
    else:
      m |= (G2[st | (tail ^ st2) << 4] > 0) << j
  return m


S7 = sum(1 << w for w in range(128) if any(((v + f) ^ ((v + DY3) + (f ^ s))) & 511 == EPS & 511 for v in
                                           range(w, 512, 128) for s in {SIGMAS[j] & 511 for j, _, _ in SIG3}
                                           for f in range(512)))
assert S7 == (1 << 0x3F) - (1 << 0x25) + (1 << 0x5F) - (1 << 0x45)


L36 = (1 << 36) - 1


def hbad(b, c, d, A):
  return sum((min(l0, l1) < A & 255 <= max(l0, l1)) << i for i, t in enumerate((0xF2, 0xFA, 0x02, 0x0A))
               for h in [(t ^ b >> 24) - (c >> 24) & 255] for l0, l1 in [(h ^ d & 255, (h - 1 & 255) ^ d & 255)])


LW = (0xE000001F, 0xF000001F)
DB, IXM = 1 << 32, 1 << 9 | 1 << 10 | 1 << 17 | 1 << 25
IXADDRMASK = IXM | DB
assert IXM + 512 < 1 << 26


def ixoff(ix):
  return (ix & 1) << 17 | (ix >> 1 & 1) << 25 | (ix >> 2 & 1) << 9 | (ix >> 3) << 10


def ixdec(f):
  return f >> 17 & 1 | (f >> 25 & 1) << 1 | (f >> 9 & 1) << 2 | (f >> 10 & 1) << 3

OLD = [(j0, min(j0 + 7, 32)) for j0 in range(1, 32, 7)]


O8 = sum(1 << 8 * j for j in range(32))
J16, H8, M5 = sum(16 + j << 8 * j for j in range(32)), sum(1 + 2 * (j & 15) << 8 * j for j in range(32)), 31 * O8


def ds_build(P):  # amendment G: o(IX, j) for all j in 8-bit fields of one word, survivors by two packed tests
  C0b1, nC0c1, C0d1, Kp, S15p, nS0S5 = (P[k] & M for k in (0, 1, 2, 7, 9, 15))
  ds, dj, ow = {}, {}, {}
  for ix in range(16):
    X = (J16 ^ (C0b1 >> 17 & 31) * O8) + ((nC0c1 >> 17 & 31) + (ix & 1)) * O8 & M5
    X = (X ^ (C0d1 >> 25 & 31) * O8) + ((Kp >> 25 & 31) + (ix >> 1 & 1)) * O8 & M5
    X = (X ^ (S15p >> 9 & 31) * O8) + ((nS0S5 >> 9 & 31) + (ix >> 2 & 1)) * O8 & M5
    X = X + H8 + (ix >> 3) * O8 & M5
    TT = (X + 3 * O8 & 24 * O8, (X + 4 * O8 & M5) + 7 * O8 & 48 * O8)
    for j in range(32):
      ow[ix, j] = X >> 8 * j & 255
    for b8 in (0, 1):
      sv = [j for j in range(32) if not TT[b8] >> 8 * j & 255]  # P: the representative is walked in its own chunks
      ch = (sv[:7], sv[7:])  # J: chunk A is the first 7 survivors, the 0 to 2 others go to the pending batch
      assert len(ch[1]) <= 2
      a = DB + ixoff(ix) + (b8 << 8)
      dj[a] = ch
      for s, c in zip((0, 4), ch):
        ds[a + s] = len(c)
        ds[a + s + 1] = sum(j << 17 << LB * t for t, j in enumerate(c))
        ds[a + s + 2] = sum(j << 10 << LB * t for t, j in enumerate(c))
  for ix in range(16):
    for b8 in (0, 1):
      ds.setdefault(DB + ixoff(ix) + (b8 << 8) + 128, 0)
      ds.setdefault(DB + ixoff(ix) + (b8 << 8) + 128 + 4, 0)
  return ds, dj, ow


def prefixes(cw, y, e1):
  b, c, d, A, L, SS = cw
  r = rol(y, 7) ^ b
  H = (r >> 24) - (c >> 24) & 255
  p = rol(r - c & M, 8) ^ d
  u = (p >> 16) - (A >> 16)
  return {e1 - SS + ((u - (256 * (p >> 8 & 255) + (h ^ d & 255) < (A & 65535)) & 511) ^ L) & 511 for h in (H, H - 1 & 255)}


LANES, LB = 7, 36
ONES = sum(1 << LB * i for i in range(LANES))
DB_PACKED = DB * ONES
assert DB_PACKED.bit_length() <= 256
M_ALL = M * ONES
BOUND = sum(1 << LB * i for i in range(1, LANES + 1))
LO = [((1 << 32 - r) - 1) * ONES for r in range(33)]
HI = [(M ^ ((1 << 32 - r) - 1)) * ONES for r in range(33)]
RX15, PX15 = rol(X15, 8) * ONES, X15 * ONES
QM, X11P = B34 | L16, X11 + 1
N9, N10, N17, N25 = (1 << 9) * ONES, (1 << 10) * ONES, (1 << 17) * ONES, (1 << 25) * ONES
LQ, LX, QL, XL = B35 | L16, M, QM, M26
BC = [(1 << LB * n) - 1 for n in range(8)]


def pror(x, r):
  return x >> r & LO[r] | x << 32 - r & HI[r]


def operands(cx):
  n = lambda w: -w & M
  w = (cx['C0_b1'], n(cx['C0_c1']), cx['C0_d1'], n(cx['C0_b1'] + cx['w6']), rol(cx['C0_d1'], 16),
         (X11 + 1 - cx['S11']) & M, cx['S12'], n(cx['C0_b1'] + cx['w6'] + cx['X4'] + cx['w2']), n(cx['S1'] + cx['S6']),
         cx['S15'] ^ ror(X15, 8), cx['S10'], cx['S5'], cx['w3'], cx['X13'], cx['X9'], n(cx['S0'] + cx['S5']) | B35)
  return tuple(x * ONES for x in w)


def omega_side(U, E, P):
  C0b1, nC0c1, C0d1, _, _, _, _, Kp, _, S15p, _, _, _, _, _, nS0S5 = P
  Y8 = U ^ C0b1
  Y12 = Y8 + nC0c1
  Y0 = pror(Y12, 24) ^ C0d1
  X0 = Y0 + Kp
  D0a1 = pror(X0, 16) ^ S15p
  cg = E + nS0S5
  om = D0a1 + cg
  ov = Y12 ^ Y8 ^ nC0c1 | X0 ^ Y0 ^ Kp | cg ^ E ^ nS0S5 | om ^ D0a1 ^ cg
  return X0, Y0, Y12, Y8, D0a1, cg, om, ov


def pack(ms):
  U = E = 0
  for i, (e1, y, _) in enumerate(ms):
    U |= rol(y, 7) << LB * i
    E |= e1 << LB * i
  return U, E


def y9_path(X0, Y0, P):
  _, _, _, nC0b1w6, rC0d1, K5, S12, _, nS1S6, _, S10, S5, w3, X13, X9, _ = P
  C0a1 = Y0 + nC0b1w6
  D0d1 = X0 ^ RX15
  X12 = C0a1 ^ rC0d1
  X12n = X12 ^ M_ALL
  D1d1 = X12n + K5
  X1 = pror(X12, 24) ^ D1d1
  D1a1 = pror(D1d1, 16) ^ S12
  w10 = D1a1 + nS1S6
  D0c1 = D0d1 + S10
  D0b1 = pror(S5 ^ D0c1, 12)
  X10 = D0c1 + PX15
  X5 = pror(D0b1 ^ X10, 7)
  s1 = X1 + X5
  C1a1 = s1 + w3
  C1d1 = pror(X13 ^ C1a1, 16)
  C1c1 = X9 + C1d1
  C1b1 = pror(X5 ^ C1c1, 12)
  s2 = C1a1 + C1b1
  Y1 = s2 + w10
  Y13 = pror(C1d1 ^ Y1, 8)
  Y9 = C1c1 + Y13
  ov = (D1d1 ^ X12n ^ K5 | w10 ^ D1a1 ^ nS1S6 | D0c1 ^ D0d1 ^ S10 | X10 ^ D0c1 ^ PX15 | s1 ^ X1 ^ X5
          | C1a1 ^ s1 ^ w3 | C1c1 ^ X9 ^ C1d1 | s2 ^ C1a1 ^ C1b1 | Y1 ^ s2 ^ w10 | Y9 ^ C1c1 ^ Y13 | C0a1 ^ Y0 ^ nC0b1w6)
  return Y9, ov, Y1, C0a1, D0d1


class Row:

  def __init__(self, tau):
    self.tau, self.sigma = tau, tau ^ ror(tau, 1)
    self.theta = rol(self.sigma, 12)
    self.gamma = ETA ^ self.theta
    self.D = (self.sigma ^ EPS) & 0x7FFFFFFF
    self.low = tau in LOW_TAUS
    self.family = (self.low, bit(self.gamma, 10), tau if self.low else 0)
    fixed = {7, 10, 11, 12, 16, 17, 18, 19, 20, 24, 25, 26, 29}
    self.free = [i for i in range(7, 32) if i not in fixed and not (i < 31 and bit(self.gamma, i))
                     and not ((i + 20) % 32 < 31 and bit(self.D, (i + 20) % 32))]


ROWS = {t: Row(t) for t in TAUS}


def is_joint_root(Q, y, E, h, tau):
  sigma = tau ^ ror(tau, 1)
  gg = (Q + h) & M
  if gg ^ ((Q + (h ^ ETA)) & M) != rol(sigma, 12):
    return False
  f = ror(y ^ gg, 12)
  e2 = (E + f) & M
  if e2 ^ ((((E + DY3) & M) + (f ^ sigma)) & M) != EPS:
    return False
  h2 = ror(h ^ e2, 8)
  return ((gg + h2) & M) ^ (((gg ^ rol(sigma, 12)) + (h2 ^ MU)) & M) == tau


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


def word_of(key14):
  """(word, field j): the word holds the 8 entries of the 8 values of (eta[i], gamma[i], gamma[i+1])"""
  return (key14 >> 10) << 7 | (key14 >> 6 & 3) << 5 | key14 & 31, (key14 >> 9 & 1) << 2 | (key14 >> 8 & 1) << 1 | key14 >> 5 & 1


def ent(A, key14, low, nlow, m):
  w, j = word_of(key14)
  return A[w << nlow | low] >> 32 * j & m


def build_arrays():
  forced, dual, selected = [0] * (1 << 13), [0] * (1 << 13), [0] * (1 << 14)
  for key14 in range(1 << 14):
    d = tuple(key14 >> 13 - t & 1 for t in range(14))
    Qi, yi, Ek, Epk, etai, gi, sk, kk, gi1, kk1, hasc, cval, li, lk = d
    prescribed = (not li and gi) or (not lk and (kk ^ Ek ^ Epk))
    w, j = word_of(key14)
    for cp in range(4):
      arcs = [arc_of(d, cp >> 1, cp & 1, 0), arc_of(d, cp >> 1, cp & 1, 1)]
      dual[w << 2 | cp] |= (arcs[0] | arcs[1] << 5) << 32 * j
      if hasc:
        forced[w << 2 | cp] |= arcs[cval] << 32 * j
      else:
        passing = [x for x in arcs if x]
        if len(passing) == 1:
          forced[w << 2 | cp] |= passing[0] << 32 * j
        assert not (len(passing) == 2 and prescribed), 'Lemma S5'
      for want in (0, 1):
        cand = [x for x in ((arcs[cval],) if hasc else arcs) if x and x & 1 == want]
        assert len(cand) <= 1
        selected[w << 3 | cp << 1 | want] |= (cand[0] if cand else 0) << 32 * j
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
  b, u, sg, gm = bit(e1, 2), bit(e1, 21), row.sigma, row.gamma
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
  f22 = prescription(Eb(22), Epb(22), sb(22), kb(23), a22)
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
  if row.low:
    if Eb(1) == a1_:
      f2 = prescription(Eb(2), Epb(2), sb(2), kb(3), Eb(1))
      e2_2 = Eb(2) ^ f2 ^ Eb(1)
    else:
      if kb(2) == 1:
        return None
      e2_2 = Eb(2) ^ kb(3)
    h[26] = 1 ^ h[2] ^ e2_2 ^ bit(Q, 26) ^ bit(Q, 25)
    h[6] = h[26] ^ Eb(26) ^ a26 ^ bit(y, 6) ^ bit(gm, 7)
  else:
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
      arc = ent(FORCED, descriptor(row, Q, y, E, Ep, kappa, i, 1, h[i]), uu << 1 | aa, 2, 31)
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
  if not row.low:
    if len(e2_26) != 1:
      notes.append('e2[26] differs between guesses')
    h[26] = min(e2_26)
  return h, sorted(states)


def g15_meta(h6, e1, bk):
  C, B, V = bk['C2_c1'], bk['C2_b1'], bk['Y12']
  A = (bk['Y1'] + bk['w12']) & M
  alpha22 = h6 ^ bit(e1, 22) ^ bit(C, 22) ^ bit(B, 22)
  v16 = bit(V, 16) ^ 1 ^ bit(A, 16)
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
      if is_joint_root(Q, y, E, pref, row.tau):
        out.append(pref)
        cnt[7] += U_ROOT
      continue
    cp = uu << 1 | aa
    if i in free:
      cnt[4] += 1
      cnt[7] += U_FREE
      w = ent(DUAL, keys[i], cp, 2, 1023)
      arcs = (w & 0x1F, w >> 5 & 0x1F)
    else:
      cnt[0] += 1
      cnt[7] += U_FORCED
      key = keys[i]
      if i == 15 and meta:
        cnt[2] += 1
        cnt[7] += U_G15
        cs = c_star(pref, meta)
        if cs & 0x8B:
          continue
        arcs = (ent(FORCED, key | 8 | (cs >> 8 & 1) << 2, cp, 2, 31),)
      elif i == 20:
        cnt[1] += 1
        cnt[7] += U_SELECTED
        arcs = (ent(SELECTED, key, cp << 1 | bit(pref, 8), 3, 31),)
      elif i == 25:
        arcs = (ent(FORCED, key | 8 | (bit(pref, 6) ^ bit(pref, 13) ^ u) << 2, cp, 2, 31),)
      elif i == 29:
        arcs = (ent(FORCED, key | 8 | (1 ^ e29) << 2, cp, 2, 31),)
      else:
        arcs = (ent(FORCED, key, cp, 2, 31),)
    for arc in arcs:
      if arc:
        stack.append((i + 1, arc >> 3 & 1, arc >> 2 & 1, pref | (arc >> 1 & 1) << i,
                               arc & 1 if i == 9 else e29))
  return out


def solve(bk, rows, g15, cnt, notes):
  Q, y, E, e1, C, B = bk['Y9'], bk['Y4'], bk['omega'], bk['e1'], bk['C2_c1'], bk['C2_b1']
  Ep, out = (E + DY3) & M, []
  for t in rows:
    row = ROWS[t]
    kappa = row.sigma ^ EPS ^ E ^ Ep
    res = row_setup(row, Q, y, E, Ep, e1, kappa, C, B, notes)
    if res is not None:
      meta = g15_meta(res[0][6], e1, bk) if g15 else None
      out += [(r, t) for r in traverse(row, Q, y, E, Ep, kappa, e1, res[0], res[1], cnt, meta)]
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
  return len({ROWS[t].family for t in rows})


def rows_of(T):
  return [t for j, t in enumerate(TAUS) if T >> j & 1 and S_MASK >> j & 1]


ROW_CAP = {t: U_ROW + sum(a * b for a, b in zip(tree(ROWS[t]), (U_FORCED, U_SELECTED, U_G15, U_FREE, U_LEAF + U_ROOT)))
           for t in TAUS}
CT = [1024 + U_FAMILY * families(rows_of(T)) + sum(ROW_CAP[t] for t in rows_of(T)) if rows_of(T) else 0
      for T in range(128)]
assert all(ROW_CAP[t] == (3516 if len(ROWS[t].free) == 4 else 2326) for t in TAUS if t != 0x675020A0)
ENVELOPES = (0x04, 0x01, 0x18, 0x52)
assert max(CT[T] for e in ENVELOPES for T in range(128) if T & ~e == 0) == 9192
A_T = [U_GLOBAL + U_FAMILY * families(rows_of(T)) + U_ROW * len(rows_of(T)) if rows_of(T) else 0 for T in range(128)]
CM = [A_T[T] + sum(max(ROW_CAP[t] - U_ROW for t in rows_of(T) if ROWS[t].family == f) for f in
                   {ROWS[t].family for t in rows_of(T)}) for T in range(128)]
CTW = [CM[T] | A_T[T] << 16 for T in range(128)]
assert max(CM[T] for e in ENVELOPES for T in range(128) if T & ~e == 0) == CM[0x52] == CM_MAX and max(CM) < 65536
assert all(31 not in ROWS[t].free for t in TAUS)


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
  u['t'] = rol(u['K0_d1'], 16) ^ u['K0_a1']
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


def pvals(bk, h):
  y14 = rol(h, 16) ^ bk['e1']
  t = rol(bk['K0_d1'], 16) ^ ((IV[0] + IV[4] + (rol(y14, 8) ^ bk['C2_d1']) - bk['C2_a1'] - bk['C2_b1']) & M)
  y6 = ror(((y14 + bk['C2_c1']) & M) ^ bk['C2_b1'], 7)
  a1 = (y6 + bk['Y1'] + bk['w12']) & M
  d = ror(a1 ^ bk['Y12'], 16)
  c = (Y11 + d) & M
  b = ror(y6 ^ c, 12)
  a = (a1 + b + bk['w5']) & M
  return t, c, a, b, b & BETA, d, ror(d ^ a, 8)


def test_a(a, s, tau):
  return a & tau == ((tau - BETA + 8 + 2 * s) & M) >> 1


def test_c(c, z, tau):
  return ((c + z) & M) ^ ((((c + DY11) & M) + (z ^ ror(tau, 8))) & M) == EPS


def predicate(bk, h, tau):
  t, c, a, b, s, d, z = pvals(bk, h)
  return (t != 0 and c & QSTAR_MASK == QSTAR_VALUE and test_a(a, s, tau) and test_c(c, z, tau)), c, t


def cert_full(v, h, tau):
  c1 = c1_of(v, h)
  u = step_ct(v, c1)
  if c1 & QSTAR_MASK != QSTAR_VALUE or u['t'] == 0:
    return False
  r = chart(u)
  return (r['cons'] and r['j'] == (theta_of(tau), EPS, tau) and r['cva'] == r['cvb']
      and (r['ea'][4] ^ r['eb'][4], r['ea'][5] ^ r['eb'][5], r['ea'][1] ^ r['eb'][1]) == (tau, EPS, BETA))


def chart_check(v, c1):
  u = step_ct(v, c1)
  r, h = chart(u), u['E3_h1']
  t, c, a, b, s, d, z = pvals(v, h)
  ea, eb = r['ea'], r['eb']
  Q, y, E = v['Y9'], v['Y4'], v['omega']
  ga, gb = (Q + h) & M, (Q + (h ^ ETA)) & M
  fa, fb = (E + ror(y ^ ga, 12)) & M, (E + DY3 + ror(y ^ gb, 12)) & M
  ok = (r['cons'] and all(r['cva'][i] == r['cvb'][i] for i in (0, 2, 5, 7))
          and r['j'] == (ga ^ gb, fa ^ fb, ((ga + ror(h ^ fa, 8)) ^ (gb + ror(h ^ ETA ^ fb, 8))) & M)
          and (t, c, a, b, d) == (u['t'], c1, ea[4], ea[1], ea[3]) and eb[1] == b ^ BETA
          and eb[4] == (a + BETA - 2 * s - 8) & M and eb[5] == (c + DY11 + ror(d ^ eb[4], 8)) & M
          and all(test_a(a, s, tau) == (ea[4] ^ eb[4] == tau) for tau in TAUS))
  if ok and ea[4] ^ eb[4] in TAUS:
    ok = test_c(c, z, ea[4] ^ eb[4]) == (ea[5] ^ eb[5] == EPS)
  x14 = rol(h, 16) ^ v['e1']
  y6 = ror(((x14 + v['C2_c1']) & M) ^ v['C2_b1'], 7)
  A = (v['Y1'] + v['w12']) & M
  meta = g15_meta(bit(h, 6), v['e1'], v)
  g15 = (((x14 + v['C2_c1']) ^ x14 ^ v['C2_c1']) >> 22 & 1) == meta[1] - (v['C2_c1'] >> 22) and \
    (((y6 + A) ^ y6 ^ A) >> 16 & 1) == meta[3] - (A >> 16 & 511)
  if g15:
    cs = c_star(h & 0x7FFF, meta)
    ok = ok and not cs & 0x8B and cs >> 8 & 1 == bit(h, 15)
  return ok, g15


L31, PLANT_EVERY = 0x7FFFFFFF, 8
S_ROWS = [t for j, t in enumerate(TAUS) if S_MASK >> j & 1]
SOLS = {}


class Rng:

  def __init__(self, seed):
    self.s = int.from_bytes(hashlib.sha256(b'frontline plant' + seed).digest()[:8], 'little')

  def __call__(self, n=32):
    self.s = (self.s + 0x9E3779B97F4A7C15) & (1 << 64) - 1
    z = (self.s ^ self.s >> 30) * 0xBF58476D1CE4E5B9 & (1 << 64) - 1
    z = (z ^ z >> 27) * 0x94D049BB133111EB & (1 << 64) - 1
    return (z ^ z >> 31) & (1 << n) - 1


def jroot_words(Q, y, E, h, tau):
  ga, gb = (Q + h) & M, (Q + (h ^ ETA)) & M
  fa, fb = (E + ror(y ^ ga, 12)) & M, (E + DY3 + ror(y ^ gb, 12)) & M
  return (ga ^ gb == rol(tau ^ ror(tau, 1), 12) and fa ^ fb == EPS
      and ((ga + ror(h ^ fa, 8)) ^ (gb + ror(h ^ ETA ^ fb, 8))) & M == tau)


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


def plant(tau, rng):
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
    if not jroot_words(Q, y, E, h, tau):
      continue
    C = rng()
    S_ = ((rol(h, 16) ^ e1) + C) & M
    B = rng() & ~(3 << 22) & M | bit(S_, 22) << 22 | (bit(S_, 23) ^ 1) << 23
    Y1, A = rng(), rng()
    cc = QSTAR_VALUE | rng() & ~QSTAR_MASK & M
    return dict(Y9=Q, Y4=y, omega=E, e1=e1, C2_c1=C, C2_b1=B, Y1=Y1, w12=(A - Y1) & M,
          Y12=rol((cc - Y11) & M, 16) ^ (ror(S_ ^ B, 7) + A) & M), h
  return None


def plant_check(seed, k):
  tau = S_ROWS[k // PLANT_EVERY % len(S_ROWS)]
  r = plant(tau, Rng(seed))
  if r is None:
    return 1, 1
  bk, h = r
  cnt = [0] * 8
  new, old = solve(bk, [tau], True, cnt, []), solve(bk, [tau], False, [0] * 8, [])
  units = (U_GLOBAL + U_FAMILY + U_ROW + U_FORCED * cnt[0] + U_SELECTED * cnt[1] + U_G15 * cnt[2] + U_FREE * cnt[4]
             + U_LEAF * cnt[6] + U_ROOT * len(new))
  T = 1 << TAUS.index(tau)
  bad = (((h, tau) not in new) + ((h, tau) not in old) + (not set(new) <= set(old))
           + (not all(jroot_words(bk['Y9'], bk['Y4'], bk['omega'], *t) for t in old)) + (units > CT[T])
           + meter_bad(U_GLOBAL + U_FAMILY + U_ROW + cnt[7], units, T))
  return bad, 6


def meter_bad(d, units, T):
  return d != units or d > CM[T]


OBS = ('members', 'e_lanes', 'passes', 'solver_calls', 'leaves', 'roots', 'certified', 'units', 'solver_units',
       'opened', 'closed', 'skipped_pass', 'checks', 'mismatches', 'fills', 'halted')


class Halt(Exception):
  pass


class Found(Exception):
  pass


def steps23(ow, y, e1, T, o, A, bk):
  v = rebuild(ow, y, e1)
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
  for h, tau in roots:
    ok, c, t = predicate(bk, h, tau)
    bad += ok != ((h, tau) in full)
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


def olists(b_, c_, d_, A, L_, SS):  # N0: the opened lists of the four block classes (Lemma NA)
  sl = [x >> s & 127 for x, s in ((b_, 8), (c_, 8), (d_, 16), (A, 16), (L_, 0), (SS, 0))]
  return {(r, q): [u for u in range(64) for z in [(2 * u - 63) % 128] if S7 >> (1 + 2 * z + ((((((z ^ sl[0]) - sl[1] - r)
          ^ sl[2]) - sl[3] - q) ^ sl[4]) - sl[5])) % 128 & 1] for r in (0, 1) for q in (0, 1)}


def bkey(cw, HB, beta):  # N: the block words of Lemma NA
  b_, c_, d_, A = cw[:4]
  eb, yb = member(beta << 11)
  ib, A8 = eb >> 20 & 3, A >> 8 & 255
  r0 = (rol(yb, 7) ^ b_) & 255
  p8 = (r0 - c_ & 255) ^ d_ >> 8 & 255
  lo = [h ^ d_ & 255 for H in [(0xF2 + 8 * ib ^ b_ >> 24) - (c_ >> 24) & 255] for h in (H, H - 1 & 255)]
  return eb, yb, ib, p8, lo, (int(r0 < c_ & 255), int(p8 < A8 if p8 != A8 else lo[0] < A & 255)), p8 == A8 and HB >> ib & 1


def na_check(ow):
  cx = co_ctx(*ow, FLAGS)
  cw = (cx['C0_b1'], cx['C0_c1'], cx['C0_d1'], cx['C0_b1'] + cx['w6'] + cx['X4'] + cx['w2'] & M, rol(X15, 24) ^ cx['S15'], cx['S0'] + cx['S5'] & M)
  OL, HB, n = olists(*cw), hbad(*cw[:4]), 0
  for beta in range(256):
    eb, yb, _, _, _, key, strad = bkey(cw, HB, beta)
    n += strad or OL[key] == [u for u in range(64) if S7 >> (co_ref(*ow, yb + 4 * u & M, FLAGS)[0] & 127) & 1]
  return n


def walk(seed, nb=TRIAL_BLOCKS, WR=0, credit=CREDIT, t2_every=T2_EVERY, gt=None, mk=True):
  diagnostic_gate = gt is not None
  gt = gt or (lambda v: v)
  sh = hashlib.shake_256(b'frontline context' + seed).digest(160)
  ow = struct.unpack('<7I', sh[:28])
  draws = [QSTAR_VALUE | w & ~QSTAR_MASK & M for w in struct.unpack('<32I', sh[32:])]
  o = dict.fromkeys(OBS, 0)
  o['units'] = U_CONTEXT
  first, bad, chk = None, 0, 0
  cx = co_ctx(*ow, FLAGS)
  P = operands(cx)
  PF = P[:14] + (P[14] + B34 * ONES, P[15])
  XW, S6, X14 = cx['X2'] + cx['S3'] - cx['K3_a1'] - cx['K3_b1'] & M, cx['S6'], cx['X14']
  S2 = rol(cx['S14'], 8) ^ K2D
  BW = dict(w5=S2 - (K2A + K2B) & M, w12=cx['D2_a1'] - S2 - cx['S7'] & M, K0_d1=cx['K0_d1'])
  A = cx['C0_b1'] + cx['w6'] + cx['X4'] + cx['w2'] & M
  HB = hbad(cx['C0_b1'], cx['C0_c1'], cx['C0_d1'], A)
  DS, DJ, OW9 = ds_build(P)
  Rj = [(16 + j ^ cx['C0_b1'] >> 17) & 63 | (cx['C0_b1'] >> 23 & 1) << 6 for j in range(32)]
  Cc = cx['C0_c1'] >> 17 & 127
  sc = not (all(r < Cc for r in Rj) or all(r > Cc for r in Rj))  # N: a context that is not plain runs the second copy

  def lane(ms, E, i, om, X0, Y0, Y12, W, cy, md=0):  # md: U_FILL a representative, 0 a straddling partner, -1 chunk A or pending (L)
    nonlocal WR, credit, first, bad, chk
    sh_ = LB * i
    t = om >> sh_
    lo = t & LQ
    omi = om >> sh_ & M
    e1, y, _ = ms[i]
    rom, ry9 = co_ref(*ow, y, FLAGS)
    rm2 = T2(rom)
    rx = T1(ry9) & rm2 if rm2 else 0
    x = m1 = 0
    bad += om >> sh_ & L36 ^ B35 >= 3 << 32
    if md < 0:  # L: prepaid fill always run, mask (1) first, the lane test of (2) only after a nonzero mask (1)
      if not cy:
        o['fills'] += 1
        cy.append(y9_path(X0, Y0, PF))
      m2 = 0
    else:
      m2 = L2(R2(lo) + (t & LX))
    if m2 or md < 0:
      if not cy:  # J: fills are prepaid, except that of a representative batch
        o['fills'] += 1
        o['units'] += md
        WR += md
        cy.append(y9_path(X0, Y0, PF))
      Y9p, ov2, Y1p, C0a1, D0d1 = cy[0]
      bad += cy[0] != y9_path(X0, Y0, PF)
      t9 = Y9p >> sh_
      if md < 0 and t9 & 3:  # M: bit 0 or 1 of Y9 set gives a zero mask of (1)
        bad += mask1_ref(ry9) != 0
      else:
        if md < 0:
          o['units'] += U_T1
          WR += U_T1
        y9a, y9x = t9 & QL, t9 & XL
        m1 = L1(R1(y9a) + y9x)
        bad += m1 != mask1_ref(ry9) or (y9a, y9x) != (B34 + (ry9 & L16), ry9 & M26) or bool(ov2 & BOUND)
      if md < 0 and m1:
        o['units'] += U_M2
        WR += U_M2
        m2 = L2(R2(lo) + (t & LX))
      if md > 0 and m2:
        o['units'] += U_ER
        WR += U_ER
    if m2:
      o['e_lanes'] += 1
      x = m1 & m2
      u = step_ct(rebuild(ow, y, e1), draws[o['e_lanes'] & 31])
      wr, _, ys = compress2(u['A'], u['t'], FLAGS)
      bad += (ys[4], ys[9] + B34, (ys[3] + ys[4] + wr[15] + wr[8]) & M) != (y, Y9p >> sh_ & (B34 | M), omi)
      chk += 3
    bad += omi != rom or (md >= 0 or m1) and m2 != rm2 or x != rx or rom & 511 not in W
    chk += 1
    if (md >= 0 or m1) and (m2 or ms[i][2] % t2_every == 0):
      bad += m2 != mask2_ref(omi)
      chk += 1
    if not x:
      return lo
    o['passes'] += 1
    if first is None:
      first = ms[i][2]
    es = E >> sh_ & M
    d1c = ((C0a1 ^ P[4]) >> sh_ ^ M) + X11P & M
    x6 = ror(S6 ^ d1c, 19) ^ K7
    C2a = x6 + XW & M
    C2d = ror(X14 ^ C2a, 16)
    X10 = ((D0d1 + P[10]) >> sh_) + X15 & M
    C = X10 + C2d & M
    B = ror(x6 ^ C, 12)
    r = (Y9p >> sh_ + 16 ^ es) & 4 ^ 3
    v = rebuild(ow, y, e1)
    bad += (v['Y9'], v['omega'], v['C2_c1'], v['C2_b1'], v['C2_a1'], v['C2_d1'], e1) != (
      Y9p >> sh_ & M, omi, C, B, C2a, C2d, es)
    T = x & VMASK[nu_of(v['Y9'], e1, v['C2_c1'], v['C2_b1'])]
    ok, gc = chart_check(v, draws[2 + o['passes'] % 30])
    bad, chk = bad + (not ok), chk + 3 + gc
    if ((r + C) ^ B ^ 5) + 5 & 6:
      o['units'] += U_PASS
      WR += U_PASS
      bad += T != 0
      return lo
    o['units'] += U_PC
    WR += U_PC
    bad += T != x
    ct = CTW[x]
    a = ct >> 16
    if ct & 65535 > credit:
      raise Halt(3)
    o['solver_calls'] += 1
    bk = dict(Y9=Y9p >> sh_ & M, Y4=es - Y3 & M, omega=omi, e1=es, C2_a1=C2a, C2_b1=B, C2_c1=C, C2_d1=C2d,
                  Y1=Y1p >> sh_ & M, Y12=Y12 >> sh_ & M, **BW)
    b, d = steps23(ow, y, es, x, o, a, bk)
    credit -= d
    bad += b
    chk += 2
    return lo

  try:
    if WR > WB:
      raise Halt(1)
    PB = []

    def flush():  # J: the pending batch (lanes of different clusters of this context), its omega side and lanes
      nonlocal bad, chk
      if PB:
        ms = [m for m, _ in PB]
        pU, pE = pack(ms)
        pX0, pY0, pY12, _, _, _, pom, pov = omega_side(pU, pE, P)
        o['members'] += len(ms)
        pc, WU = [], set().union(*(w for _, w in PB))
        for t in range(len(ms)):
          lane(ms, pE, t, pom, pX0, pY0, pY12, WU, pc, -1)
        bad += bool(pov & BOUND)
        chk += 1
        PB.clear()
    e1, y = member(0)
    v = rebuild(ow, y, e1)
    for c1 in draws[:2]:
      ok, gc = chart_check(v, c1)
      bad, chk = bad + (not ok), chk + 1 + gc
    cw = (v['C0_b1'], v['C0_c1'], v['C0_d1'], v['C0_b1'] + v['w6'] + v['X4'] + v['w2'] & M,
              rol(X15, 24) ^ v['S15'], v['S0'] + v['S5'])
    b_, c_, d_, _, L_, SS = cw
    SS &= M
    HT, OL = HMT if SS & L16 > 32767 else HWT, olists(*cw)
    for bi in range(nb):
      beta = sh[31] + bi & 255
      eb, yb, ib, p8, lo, key, strad = bkey(cw, HB, beta)
      hv = {((p8 << 8) + lo[l] - A & L16 ^ L_ >> 16) + (eb >> 16) - (SS >> 16) & L16 for l in ((0, 1) if sc else (int(Rj[0] < Cc),))}
      ub, dead = U_BT[sc], not any(HT[h] for h in hv)
      for m in range(0, 2048, 1 if dead else 31):  # members of the block: omega >> 16 in the window (Lemma NB), T2 0 if dead
        rom = co_ref(*ow, member(beta << 11 | m)[1], FLAGS)[0]
        z = dead and (T2(rom) > 0 if m % 9 else mask2_ref(rom) > 0)
        o['skipped_pass'] += z
        bad += z or min((rom >> 16) - h + 1 & L16 for h in hv) > 1 + (HT is HWT)
        chk += 1
      if dead and mk and not diagnostic_gate:  # N: a dead block is skipped
        o['units'] += ub
        WR += ub
        o['closed'] += 64
        continue
      ub += U_CMB + U_BSL * (p8 == A >> 8 & 255)
      ol = OL[key]
      bad += not strad and ol != [u for u in range(64) if S7 >> (co_ref(*ow, yb + 4 * u & M, FLAGS)[0] & 127) & 1]
      chk += 1
      if strad or diagnostic_gate or not mk:
        ol = list(range(64))
      if not strad:
        ub += U_LB
      o['units'] += ub
      WR += ub
      Ub, Eb = bc(rol(yb, 7)), bc(eb)
      for k in range(0, len(ol), 7):
        us = ol[k:k + 7]
        JU = sum(u << 9 << LB * t for t, u in enumerate(us))
        reps = [cmember(beta << 6 | u, 0) for u in us]
        U, E = pack(reps)
        bad += (U, E) != (Ub + JU & BC[len(us)], Eb + (JU >> 7) & BC[len(us)])
        X0, Y0, Y12, Y8, D0a1, cg, om, ov = omega_side(U, E, P)
        w8 = D0a1 + P[15]
        IX = (Y12 ^ Y8 ^ P[1]) & N17 | (X0 ^ Y0 ^ P[7]) & N25 | (w8 ^ D0a1 ^ P[15]) & N9 | (om ^ E ^ w8) << 1 & N10
        IX |= DB_PACKED  # one charged OR in U_IX per batch
        o['members'] += len(reps)
        rc = []
        for i in range(len(reps)):
          g, sh_ = beta << 6 | us[i], LB * i
          W = prefixes(cw, *reps[i][1::-1])
          rv = co_full(*ow, reps[i][1], FLAGS)
          ro = Y3 + reps[i][1] + rv['w8'] & M
          real_gv = gv = 2 if strad else S7 >> (ro & 127) & 1
          bad += (len(W) > 1) != bool(strad) or ro != om >> sh_ & M
          chk += 1
          gv = gt(gv)
          if not gv:
            o['closed'] += 1
            for j in range(32):
              rom = co_ref(*ow, cmember(g, j)[1], FLAGS)[0]
              m = mask2_ref(rom) > 0
              o['skipped_pass'] += m
              bad += m or rom & 511 not in W or S7 >> (rom & 127) & 1
              chk += 1
            continue
          o['opened'] += 1
          fb = gv > 1 or not mk
          lok = lane(reps, E, i, om, X0, Y0, Y12, W, rc, 0) if fb else om >> sh_ & LQ  # P: no representative lane test
          o['units'] += U_SC if fb else U_LIVE
          WR += U_SC if fb else U_LIVE
          if fb:
            for j0, j1 in OLD:
              ms = [cmember(g, j) for j in range(j0, j1)]
              pU, pE = pack(ms)
              pX0, pY0, pY12, _, _, _, pom, pov = omega_side(pU, pE, P)
              o['members'] += len(ms)
              pc = []
              for t in range(len(ms)):
                lane(ms, pE, t, pom, pX0, pY0, pY12, W, pc)
              bad += bool(pov & BOUND)
              chk += 1
            continue
          da = (IX >> sh_ & IXADDRMASK) + (lok & 256)
          # forced-open diagnostics only: empty descriptor
          if diagnostic_gate and real_gv == 0:
            da += 128
          ch, ixr = DJ.get(da, ((), ())), ixdec(IX >> sh_ & IXM)
          for j in range(32):
            rom = co_ref(*ow, cmember(g, j)[1], FLAGS)[0]
            sv = j in ch[0] or j in ch[1]
            m = not sv and mask2_ref(rom) > 0
            o['skipped_pass'] += m
            bad += m or rom & 511 != om >> sh_ & 511 or OW9[ixr, j] != rom >> 9 & 31 or sv != (
              S7 >> (rom & 127) & LW[rom >> 8 & 1] >> (rom >> 9 & 31) & 1)
            chk += 1
          n0 = DS[da]
          bu, be = bc(rol(reps[i][1], 7)), bc(reps[i][0])
          bad += bool(n0 == 0 and DS[da + 4]) or (bu, be) != (Ub + bc(us[i] << 9), Eb + bc(us[i] << 2))
          for s in (0, 4):
            n = DS[da + s] if s else n0
            if s and n:  # J: the lanes of chunk B join the pending batch, flushed first when they would not fit
              o['units'] += U_BN + (U_PRE + U_BL) * n
              WR += U_BN + (U_PRE + U_BL) * n
              if len(PB) + n > 7:
                flush()
              bad += DS[da + 5] != sum(j << 17 << LB * t for t, j in enumerate(ch[1]))
              PB.extend((cmember(g, j), W) for j in ch[1])
              break
            k_ = 4 if n > 3 else 0
            k_ += 2 if n > k_ + 1 else 0
            k_ += 1 if n > k_ else 0
            if not k_:
              break
            JU_ = DS[da + (s + 1)]
            cU = bu + JU_
            cE = be + (JU_ >> 7)
            bad += JU_ >> 7 != DS[da + (s + 2)]
            cX0, cY0, cY12, _, _, _, com, cov = omega_side(cU, cE, P)
            ms = [cmember(g, j) for j in ch[s >> 2]]
            o['members'] += k_
            o['units'] += U_PRE * k_ * (not s)
            WR += U_PRE * k_ * (not s)
            pc = []
            for t in range(k_):
              lane(ms, cE, t, com, cX0, cY0, cY12, W, pc, -1)
            bad += bool(cov & BOUND) + (len(ms) != k_)
            chk += 1
        bad += bool(ov & BOUND)
        chk += 1
    flush()  # J: the last pending batch of the context, paid by the context
  except Halt as e:
    o['halted'] = e.args[0]
  except Found:
    pass
  o['mismatches'] += bad
  o['checks'] += chk
  return ow, first, o, WR


def root_pair(ow, k):
  e1, y = member(k)
  v = rebuild(ow, y, e1, ROOT_FLAGS)
  u = step_ct(v, c1_t0(v))
  da, db = compress2(u['A'], 0, ROOT_FLAGS)[1], compress2(u['B'], 0, ROOT_FLAGS)[1]
  return u['A'], u['B'], u['t'] == 0 and all(da[i] == db[i] for i in (0, 2, 5, 7))


def trial(seed, k=0):
  ow, first, o, _ = walk(seed)
  a, b, ok = root_pair(ow, 0 if first is None else first)
  o['checks'] += 1
  o['mismatches'] += not ok
  if k % PLANT_EVERY == 0:
    bad, n = plant_check(seed, k)
    o['checks'] += n
    o['mismatches'] += bad
  return a, b, o


def selftest(n):
  rep = {'constants': all(globals()[k] == x for k, x in TEXT.items())}
  th = [theta_of(t) for t in TAUS]
  tq, te = [(ETA & 255, x & 255) for x in th], [(ror(x, 12) & 255, EPS & 255) for x in th]
  a1, a2 = automaton(tq, 0, 8)[0], automaton(te, DY3 & 255, 8)[0]
  bf = lambda tg, dy, x: sum(1 << j for j, (dz, out) in enumerate(tg)
                               if any(((x + v) ^ (x + dy + (v ^ dz))) & 255 == out for v in range(256)))
  rep['automata_vs_bruteforce_w8'] = sum(a1[x] == bf(tq, 0, x) and a2[x] == bf(te, DY3, x) for x in range(256))
  cnt = []
  for t in (AUT1, AUT2):
    cur = {}
    for b in range(256):
      cur[t[0][b]] = cur.get(t[0][b], 0) + 1
    for tb in t[1:]:
      nxt = {}
      for s, c in cur.items():
        for b in range(256):
          nxt[tb[s + b]] = nxt.get(tb[s + b], 0) + c
      cur = nxt
    cnt.append(cur)
  rep['SHARE_E_COUNT'] = (sum(c1 * c2 for p, c1 in cnt[0].items() for q, c2 in cnt[1].items() if p & q) == SHARE
              and sum(c for q, c in cnt[1].items() if q) == E_COUNT)
  rnd = hashlib.shake_256(b'frontline selftest').digest(8 * n)
  xs = struct.unpack('<%dI' % (2 * n), rnd)
  rep['T1_T2_vs_bitserial'] = sum(T1(x) == mask1_ref(x) and T2(x) == mask2_ref(x) for x in xs)
  rep['M2bit'] = not any(F1[u + e] for b in range(256) if b & 3 for u in {F1[t + d] for t in {F1[F1[b] + c] for c in range(256)} for d in range(256)} for e in range(256)) and not any(T1(x) for x in xs if x & 3)  # M
  rep['HW'] = all(HWT[x >> 16] and HMT[x >> 16] for x in xs if T2(x)) and (sum(HE16), sum(HWT), sum(HMT)) == HCNT
  al = [any(((w + f) ^ ((w + DY3) + (f ^ s))) & 511 == EPS & 511 for s in {SIGMAS[j] & 511 for j, _, _ in SIG3}
              for f in range(512)) for w in range(512)]
  rep['S7_partition'] = (sum(al) == 208 and all(al[w] == S7 >> (w & 127) & 1 for w in range(512))
                           and all(S7 >> (x & 127) & 1 for x in xs if T2(x))
                           and len({g & 63 | j << 6 | g >> 6 << 11 for g in range(1 << 14) for j in range(32)}) == 1 << 19
                           and all(cmember(g, j)[0] >> 10 & 31 == j for g in (0, 9999, 16383) for j in range(32)))
  rep['precheck'] = all(((((a >> 16 ^ b) & 4 ^ 3) + c ^ d ^ 5) + 5 & 6 == 0) == (VMASK[nu_of(a, b, c, d)] & S_MASK > 0)
                          for a, b, c, d in zip(xs, xs[1:], xs[2:], xs[3:]))
  sd = st = 0
  for s in range(16):
    b, c, d, A, L, SS = struct.unpack('<6I', hashlib.shake_256(b'xg %d' % s).digest(24))
    for g in range(s, 1 << 14, 997):
      e1, y, _ = cmember(g, 0)
      p = rol((rol(y, 7) ^ b) - c & M, 8) ^ d
      sd += y >> 16 & 511 != (0xF2, 0xFA, 0x02, 0x0A)[e1 >> 20 & 3] << 1
      for a in range(256):
        A = A >> 16 << 16 | p & 0xFF00 | a
        r = hbad(b, c, d, A) >> (e1 >> 20 & 3) & 1
        st += r
        sd += r != (len(prefixes((b, c, d, A, L, SS), y, e1)) > 1)
  rep['XG'] = [sd, st, all((w + 0x5B & 0x5F) + 0x66 >> 7 == 1 - (S7 >> w & 1) for w in range(128))]
  na = sum(na_check(struct.unpack('<7I', hashlib.shake_256(b'na %d' % s).digest(28))) for s in range(6))  # N
  rep['NA'] = na
  rep['tables'] = all(L2(R2(t & LQ) + (t & LX)) == T2(x) and L1(R1(u & QL) + (u & XL)) == T1(x)
            and bc(x) == x * ONES
            for x in xs[:256] for l in range(7)
            for t, u in [((B35 + x << LB * l) >> LB * l, (B34 + x << LB * l) >> LB * l)]) and all(F1[s + b] == F1[s + (b & 3)] for s in range(
    T3B, len(F1), 256) for b in range(256)) and {F2[F2[b & 255] + (b >> 8)] for b in range(1 << 16)} == set(
    range(S2B, S2B + 7 * 256, 256)) and {F1[F1[b & 255] + (b >> 8)] for b in range(1 << 16)} == set(
    range(S1B, S1B + 43 * 256, 256))
  rep['classes'] = len(P1) == 35 and len(P2) == 4 and all(F2[F2[S2B + 256 * s + (h & 255)] + (h >> 8)] == L2(
    B33 + C2[s] + (h << 16)) for s in range(7) for h in range(1 << 16)) and all(F1[F1[S1B + 256 * s + (h & 255)] + (
    h >> 8)] == L1(B1 + C1[s] + (h << 16)) for s in range(43) for h in range(1 << 10))
  f1 = 0
  for s in range(32):
    ow = struct.unpack('<7I', hashlib.shake_256(b'f1 %d' % s).digest(28))
    P = operands(co_ctx(*ow, FLAGS))
    ms = [member(k & 0x7FFFF) + (0,) for k in struct.unpack('<7I', hashlib.shake_256(b'f1 m%d' % s).digest(28))]
    U, E = pack(ms)
    X0, Y0, Y12, _, D0a1, _, om, _ = omega_side(U, E, P)
    Y9, _, Y1, C0a1, D0d1 = y9_path(X0, Y0, P)
    for i, (e1, y, _) in enumerate(ms):
      v = rebuild(ow, y, e1)
      f1 += [w >> LB * i & M for w in (om, X0, Y0, Y12, C0a1, D0d1, D0a1, Y9, Y1)] == [v[k] for k in (
        'omega', 'X0', 'Y0', 'Y12', 'C0_a1', 'D0_d1', 'D0_a1', 'Y9', 'Y1')]
  rep['F1_fill'] = f1
  drills = {}
  for name, kw, code in (('W', dict(WR=WB + 1), 1), ('C', dict(credit=0), 3), ('R', dict(credit=15012), 0)):
    for s in range(64):
      o = walk(b'drill%d' % s, **kw)[2]
      if o['halted'] if code else o['solver_calls']:
        break
    drills[name] = (o['halted'] in (0, 3) and o['solver_calls'] >= 1 and not o['mismatches'] if name == 'R' else
            o['halted'] == code and (o['members'] == 0 and o['units'] == U_CONTEXT if name == 'W'
            else o['solver_calls'] == 0 and o['passes'] >= 1), s)
  _, _, o, w = walk(b'drill0', WR=WB)
  drills['WB'] = (o['halted'] == 0 and WB < w <= WB + W_CTX and not o['mismatches'], 0)
  rep['halt_drills'] = drills
  gd = {}
  for name, gt, mk in (('table', None, True), ('open', lambda v: v | 1, True), ('closed', lambda v: 0, True),
                         ('nomask', None, False)):
    r = [walk(b'gate%d' % s, gt=gt, mk=mk)[2] for s in range(8)]
    gd[name] = [sum(o[k] for o in r) for k in ('opened', 'closed', 'e_lanes', 'passes', 'skipped_pass', 'mismatches',
                                                   'fills', 'members')]
  t, op, cl, nm_ = gd['table'], gd['open'], gd['closed'], gd['nomask']
  rep['gate_drills'] = gd
  rep['ok'] = (rep['constants'] and rep['HW'] and rep['M2bit'] and rep['automata_vs_bruteforce_w8'] == 256 and rep['SHARE_E_COUNT'] and rep['precheck']
                 and rep['T1_T2_vs_bitserial'] == 2 * n and all(d[0] for d in drills.values()) and rep['S7_partition']
                 and t[4] == t[5] == op[4] == op[5] == op[1] == cl[0] == cl[6] == 0 and t[2:4] == op[2:4]
                 and 0 < t[6] <= op[6] and cl[4] == nm_[2] > 0 and cl[5] >= cl[4] and rep['F1_fill'] == 224
                 and rep['XG'][0] == 0 < rep['XG'][1] and rep['XG'][2] and rep['tables'] and rep['classes'] and na == 1536
                 and nm_[0] >= t[0] and nm_[3:6] == t[3:6] and t[6] <= nm_[6] and t[7] < nm_[7])
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
