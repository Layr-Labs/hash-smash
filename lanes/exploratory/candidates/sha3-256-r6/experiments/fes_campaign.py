"""Reduced run of the campaign of proof.md on the exact target (Sections 5 to 7, 12.2, 13)."""
import sys, json, hashlib
from math import comb, isqrt
N_DIR, DEG, LANES, NPL = 9, 8, 256, 175
G = 1202250025869134545910402
KCH = 19345871228983
M64, M128, M256 = (1 << 64) - 1, (1 << 128) - 1, (1 << 256) - 1
RC = (0x0000000000000001, 0x0000000000008082, 0x800000000000808A, 0x8000000080008000, 0x000000000000808B,
 0x0000000080000001, 0x8000000080008081, 0x8000000000008009, 0x000000000000008A, 0x0000000000000088,
 0x0000000080008009, 0x000000008000000A, 0x000000008000808B, 0x800000000000008B, 0x8000000000008089,
 0x8000000000008003, 0x8000000000008002, 0x8000000000000080, 0x000000000000800A, 0x800000008000000A,
 0x8000000080008081, 0x8000000000008080, 0x0000000080000001, 0x8000000080008008)
RHO = (0, 1, 62, 28, 27, 36, 44, 6, 55, 20, 3, 10, 43, 25, 39, 41, 45, 15, 21, 8, 18, 2, 61, 56, 14)
W40 = [int(h, 16) for h in """
00000000000000000000000040000004100100000000000000002000200000000000000000000000
000000000000000000000000800200002000000a0000202000000001400000040000200000000800
00000000000000000000000200000020800800000000000000010001000000000000000000000000
00000000000000000000410010000104000100400000140000802000000000800000000040000010
00000000000000000000820000820000000000080082000000040001000040000000200000200820
00000000000000000020000000000000000000000000000000000000000004000000000000020800
00000000000000000100000010000000000000000040040000800000000000800000000000000000
00000000000000000800000000820000002000080000000000000001004004000000200000000800
00000000000000008000020000000000000000002080000000000000000000000000000000200020
00000000000000030000020010800100040000422082042000040000680040840000000040200020
00000000000000410000020000820100000000002082000000040009200040000000200040200020
00000000000008010041020012820500858000406892040010240000290040800000200040201020
00000000000100010000020000000004000100802080000000002010200040000000080000208020
00000000000200010000020010820101040040482082240000040001280040800000200040200820
00000000000400010001020010800100040000406082440000040000280040800000200040200020
00000000010000010041020010000100040000406092040000040000280040800000000040201020
00000000040000010000020010820100808000402882040010840000210040800000200040200020
00000000080000010041020010000100040000406010040000200000280000800000000040001020
00000000800000010000020000820000900000002082000010040000000040000000200000200020
00000001000000010000030010800100200000422082042000840000600040840000000040200030
00000004000000010000020010820100840000406082040000040000280040800000200040200020
00000080000000010041020010820500050000486092041000240021280040800000200040201020
00000100000000010001020010800100040000406082042000040000280040800000000040201020
00000200200000000000090000000000000000000000000000800000000000400000000000000000
00000400000000010000000000000100000000402000000000000000200000000000000040000020
00001000200000000000080010000104000100400000140000002000000002800000000040000000
00008000000000010000020002820004808108002882100010042100210040000000200000200020
00020000000000010001020010000100040000406080040000000000280000800000000040200020
00100000000000010000020000000004000000002080000000000000200040000000000000200020
004000000000000100000200108201000000004820c2040000840001200844800000200040220820
00800000000000010041020010820120040000406082040000040001280040800000200040201020
020000000000000100000200100001000020004020c2040000840000200040800000000040200020
04000000000000010000020000000000000000002080000000000000200000000000000040000020
08000000000040000400000002000104008100400000140000002100000002800000000040000000
40000000000000010000020010820100840000402882040010040000200040800000200040200020
0a8094012901484005004a005200842021a008000010000402000000000000000000000000000001
080090012801480104004a0052008400318008002000000000000000000000000000000000000020
08009001200048020400480012000001208009000000000000000000000080000000000000010000
0a0294052801480185014a0052028400b1a008000000000000001000000000000008000000000000
00001200040008000000010002000000000001000000000000000000000000400000000000000000
""".split()]
KAT = ((0, '75f9117eb56131a655b34d93115a9781b7899716653c9b79f80902a99e3399f6'),
 (W40[0] ^ W40[39], 'f3025c162a37654390d8b807a6970cbae2a22b8e745218666f323f572066b8f2'))
def need(cond, what):
 if not cond:
  raise SystemExit('check failed: ' + what)
def keccak_f(L, rounds):
 L = list(L)
 for r in range(rounds):
  C = [L[x] ^ L[x + 5] ^ L[x + 10] ^ L[x + 15] ^ L[x + 20] for x in range(5)]
  D = [C[x - 1] ^ ((C[(x + 1) % 5] << 1 | C[(x + 1) % 5] >> 63) & M64) for x in range(5)]
  B = [0] * 25
  for i in range(25):
   x, y, s = i % 5, i // 5, RHO[i]
   v = L[i] ^ D[x]
   B[y + 5 * ((2 * x + 3 * y) % 5)] = (v << s | v >> (64 - s)) & M64
  L = [B[i] ^ (~B[i - i % 5 + (i + 1) % 5] & B[i - i % 5 + (i + 2) % 5]) for i in range(25)]
  L[0] ^= RC[r]
 return L
def sha3_256(msg, rounds=6):
 p = bytearray(msg) + b'\x06'
 p += bytes(-len(p) % 136)
 p[-1] |= 0x80
 L = [0] * 25
 for o in range(0, len(p), 136):
  for k in range(17):
   L[k] ^= int.from_bytes(p[o + 8 * k:o + 8 * k + 8], 'little')
  L = keccak_f(L, rounds)
 return b''.join(v.to_bytes(8, 'little') for v in L[:4])
def message(t):
 u = t.to_bytes(40, 'little')
 return u + bytes(40) + u + bytes(15)
def lanes(t):
 u = [(t >> 64 * k) & M64 for k in range(5)]
 return u + [0] * 5 + u + [0, 0x86 << 56] + [0] * 8
def rank(vs):
 piv = {}
 for v in vs:
  while v:
   b = v.bit_length() - 1
   if b not in piv:
    piv[b] = v
    break
   v ^= piv[b]
 return len(piv)
def setup_checks():
 for t, hx in KAT:
  m = message(t)
  need(sha3_256(m, 6).hex() == hx, 'known-answer digest')
  need(sha3_256(m, 24) == hashlib.sha3_256(m).digest(), '24-round SHA3-256 against hashlib')
 need(rank(W40) == 40, 'rank of W40')
 F0 = keccak_f(lanes(0), 2)
 F = [keccak_f(lanes(w), 2) for w in W40]
 n = 0
 for i in range(40):
  for j in range(i + 1, 40):
   G2 = keccak_f(lanes(W40[i] ^ W40[j]), 2)
   need(not any(a ^ b ^ c ^ d for a, b, c, d in zip(G2, F[i], F[j], F0)), 'polarization %d %d' % (i, j))
   n += 1
 need(n == 780, 'number of polarizations')
WW = [(v & M256, v >> 256) for v in W40]
PLANES = [(p % 5, p // 5) for p in range(NPL)]
MASK = {s: sum(((1 << s) - 1) << (2 * s * k) for k in range(128 // s)) for s in (1, 2, 4, 8, 16, 32, 64, 128)}
SUBS = sorted((S for S in range(1 << N_DIR) if S.bit_count() <= DEG), key=lambda S: (S.bit_count(), S))
IDX = {S: k for k, S in enumerate(SUBS)}
QR, NST = LANES << N_DIR, (1 << N_DIR) - 1
CSB, WB = 1 << 130, 1 << 131
WF, PL, TW = WB, WB + 512, WB + 832
INF = TW + 3
RB, DW = INF + 320, INF + 8320
ACO = DW + 320
TABB = ACO + NPL * len(SUBS)
TBY = TABB + NPL * len(SUBS)
FCW, HSP = TBY + 2560, TBY + 2561
CMR = HSP + 1
FR = CMR + 256 * len(SUBS)
SPL = FR + len(SUBS)
AFO = SPL + 61
TFO = AFO + 8 * len(SUBS)
FFR = TFO + 8 * len(SUBS)
ACB = FFR + 8 * len(SUBS)
WEND = ACB + (1 << N_DIR) + 1
CACHED = list(range(1, 32)) + [32 | t for t in range(3, 32)]
CSET = set(CACHED)
STRIDE = 36
MARK = 1 << 3 * STRIDE + 35
KEYMASK = sum(((1 << 35) - 1) << STRIDE * x for x in range(4)) | MARK
ROWS = [None] * 256
for _p, (_x, _z) in enumerate(PLANES):
 ROWS[STRIDE * _x + _z] = _p
 if _x == 0:
  ROWS[5 * STRIDE + _z] = _p
SPREAD = [sum((v >> b & 1) << 4 * b for b in range(6)) for v in range(64)]
def ev24(k):
 return sum(SPREAD[k >> STRIDE * x & 63] << x for x in range(4))
def cap(num, den):
 r = -(-num // den)
 s = isqrt(KCH * r)
 return r + s + (s * s < KCH * r)
def shapes(i):
 T, sh = 0, []
 while i and len(sh) < DEG:
  b = i & -i
  T |= b
  i ^= b
  sh.append(T)
 return sh
def fcoset(n):
 n1 = (1 << n) - 1
 links = sum(comb(n, k) * min(DEG, k) for k in range(1, n + 1)) - n1
 lc = sum((1 << n - T.bit_length()) - 1 for T in CACHED)
 ulast = sum(comb(n - 1, k) for k in range(1, DEG)) - len(CACHED)
 return len(CACHED) + 1 + (n1 - len(CACHED)) + n1 + 3 * links - 2 * lc - ulast
SITES = [(sh[-1], [(T, i + (1 << T.bit_length()) > NST) for T in sh[-2::-1]])
 for i, sh in ((i, shapes(i)) for i in range(1, NST + 1))]
COST = [(top not in CSET) + sum(1 if T in CSET else 3 - last for T, last in ch) + 1 for top, ch in SITES]
FCOSET = fcoset(N_DIR)
need(len(CACHED) == 60 and FCOSET == 61 + sum(COST), 'FES per coset: 61 initial loads and the step counts')
need(fcoset(40) == 18794671433175, 'FES per coset at n = 40 (17.0937 per candidate)')
RTR = 4 * (66 + 198 + 5 * 196 + 66) + 2 * 128 * 10
def popsum(n):
 s = 0
 for k in range(320):
  m = sum(W40[b] >> k & 1 for b in range(n))
  s += sum(comb(m, j) * sum(comb(n - m, l) for l in range(DEG + 1 - j)) for j in range(1, DEG + 1, 2))
 return s
POP = popsum(N_DIR)
need(popsum(40) == 4592341856, 'Section 6.3 popcount sum at n = 40')
CAPF = cap(QR * (QR - 1), 1 << 141)
GM = 0x9E3779B97F4A7C15F39CC0605CEDC8341082276BF3A27251F86C6A11D0C18E95
J_D = sum(S.bit_count() for S in SUBS)
def vd(n):
 return sum(comb(j, r) * comb(n - j, r) * sum(comb(r, k) for k in range(min(r, DEG - j) + 1))
 for j in range(1, min(DEG, n) + 1) for r in range(min(j, n - j) + 1))
V_D = vd(N_DIR)
SECS = {s: [0] for s in ('once', 'leader', 'sgroup', 'spoint', 'transform', 'phase', 'rtr', 'buf', 'fes', 'cht',
 'table', 'verify', 'vcheck', 'cs', 'ct', 'cp', 'cfa', 'cfb')}
K = SECS['once']
SPARSE, WRK, CREC, CALLS, GBASE = {}, [], {}, [0], [0]
def sec(name):
 global K
 K = SECS[name]
def LDS(a):
 K[0] += 1
 v = SPARSE.get(a)
 if v is None:
  x = (a * GM) & M256
  x ^= x >> 127
  v = x if x >> 255 else GBASE[0] + x % (2 * QR)
 return v
def STS(a, v): K[0] += 1; SPARSE[a] = v
def LDW(a):
 K[0] += 1
 v = WRK[a - WB]
 if v is None:
  raise SystemExit('check failed: read of a never-written work word')
 return v
def STW(a, v): K[0] += 1; WRK[a - WB] = v
def LDC(a):
 K[0] += 1
 need(a in CREC, 'read of a never-written coset record')
 return CREC[a]
def STC(a, v): K[0] += 1; CREC[a] = v
def XOR(a, b): K[0] += 1; return a ^ b
def AND(a, b): K[0] += 1; return a & b
def OR(a, b): K[0] += 1; return a | b
def NOT(a): K[0] += 1; return a ^ M256
def ADD(a, b): K[0] += 1; return (a + b) & M256
def SUB(a, b): K[0] += 1; return (a - b) & M256
def SHL(a, s): K[0] += 1; return (a << s) & M256
def SHR(a, s): K[0] += 1; return a >> s
def EQ(a, b): K[0] += 1; return int(a == b)
def LT(a, b): K[0] += 1; return int(a < b)
def BR(f): K[0] += 1; return f != 0
def MOV(v): K[0] += 1; return v
def RAND(src): K[0] += 1; return next(src)
def coins(seed):
 s = hashlib.shake_256(seed.encode()).digest(64)
 return iter((int.from_bytes(s[:32], 'little'), int.from_bytes(s[32:], 'little')))
def rot(v, s):
 return AND(OR(SHL(v, s), SHR(v, 64 - s)), M64)
def lanes5(w0, w1):
 need(w1 >> 64 == 0, 'second source word below 2^64')
 return [AND(w0, M64), AND(SHR(w0, 64), M64), AND(SHR(w0, 128), M64), SHR(w0, 192), w1]
class SGen:
 def __init__(s):
  s.n, s.code = 6, []
 def op(s, *o):
  s.n += 1
  s.code.append((o[0], s.n) + o[1:] + (0,) * (3 - len(o)))
  return s.n
 def x(s, a, b):
  ca, cb = type(a) is tuple, type(b) is tuple
  if ca and cb:
   return (a[0] ^ b[0],)
  if a == (0,) or b == (0,):
   return b if a == (0,) else a
  if a == b:
   return (0,)
  return s.op('xi', b, a[0]) if ca else s.op('xi', a, b[0]) if cb else s.op('x', a, b)
 def rot(s, a, k):
  if type(a) is tuple:
   return ((a[0] << k | a[0] >> (64 - k)) & M64,) if k else a
  return s.op('r', a, k) if k else a
 def chi(s, a, b, c):
  if type(b) is tuple and type(c) is tuple:
   return s.x(a, (~b[0] & c[0] & M64,))
  if c == (0,) or b == (M64,):
   return a
  if b == (0,):
   return s.x(a, c)
  if type(b) is tuple:
   return s.x(a, s.op('ai', c, ~b[0] & M64))
  nb = s.op('n', b)
  if c == (M64,):
   return s.x(a, nb)
  return s.x(a, s.op('ai', nb, c[0]) if type(c) is tuple else s.op('a', nb, c))
 def round(s, L, r):
  C = []
  for x in range(5):
   v = L[x]
   for y in range(1, 5):
    v = s.x(v, L[x + 5 * y])
   C.append(v)
  D = [s.x(C[x - 1], s.rot(C[(x + 1) % 5], 1)) for x in range(5)]
  B = [None] * 25
  for i in range(25):
   x, y = i % 5, i // 5
   B[y + 5 * ((2 * x + 3 * y) % 5)] = s.rot(s.x(L[i], D[x]), RHO[i])
  A = [s.chi(B[i], B[i - i % 5 + (i + 1) % 5], B[i - i % 5 + (i + 2) % 5]) for i in range(25)]
  A[0] = s.x(A[0], (RC[r],))
  return A
def scode():
 g, codes = SGen(), []
 L = [2, 3, 4, 5, 6] + [(0,)] * 5 + [2, 3, 4, 5, 6, (0,), (0x86 << 56,)] + [(0,)] * 8
 for r in range(6):
  g.code = []
  L = g.round(L, r)
  codes.append(g.code)
 need(all(type(v) is int for v in L[:4]), 'digest lanes in registers')
 return codes, L[:4], g.n
def dce_s(codes, out):
 live, keep = set(out), []
 for code in reversed(codes):
  k = []
  for op in reversed(code):
   if op[1] in live:
    live.discard(op[1])
    live.update((op[2], op[3]) if op[0] in ('x', 'a') else (op[2],))
    k.append(op)
  keep.append(k[::-1])
 return keep[::-1]
SCODE, SOUT, SREG = scode()
SCODE = dce_s(SCODE, SOUT)
SRND = (67, 236, 242, 242, 242, 79)
def srun(code, R):
 for t, d, a, b in code:
  if t == 'x':
   R[d] = XOR(R[a], R[b])
  elif t == 'xi':
   R[d] = XOR(R[a], b)
  elif t == 'r':
   R[d] = rot(R[a], b)
  elif t == 'a':
   R[d] = AND(R[a], R[b])
  elif t == 'ai':
   R[d] = AND(R[a], b)
  else:
   R[d] = XOR(R[a], M64)
def rounds6(L):
 R = [None] * (SREG + 1)
 R[2:7] = L
 for r in range(6):
  k0 = K[0]
  srun(SCODE[r], R)
  need(K[0] - k0 == SRND[r], 'folded round %d: %d operations' % (r, SRND[r]))
 return [R[v] for v in SOUT]
def leaders(seeds):
 sec('leader')
 per, origins = [], []
 H8 = SHL(REGS['h'], 8)
 for c in range(LANES):
  k0 = K[0]
  src = coins(seeds[c])
  j = OR(H8, c)
  w0 = RAND(src)
  w1 = AND(RAND(src), M64)
  a = ADD(SHL(j, 1), CSB)
  STC(a, w0)
  STC(ADD(a, 1), w1)
  STW(WF + 2 * c, w0)
  STW(WF + 2 * c + 1, w1)
  per.append(K[0] - k0)
  origins.append(w0 | w1 << 256)
 return per, origins
CIDX = [tuple(64 * (x + 5 * y) + z for y in range(5)) for x in range(5) for z in range(64)]
DIDX = [(64 * ((x - 1) % 5) + z, 64 * ((x + 1) % 5) + (z - 1) % 64) for x in range(5) for z in range(64)]
SRC = [None] * 1600
for _l in range(25):
 for _z in range(64):
  _x, _y = _l % 5, _l // 5
  SRC[64 * (_y + 5 * ((2 * _x + 3 * _y) % 5)) + (_z + RHO[_l]) % 64] = (64 * _l + _z, 64 * _x + _z)
CHI = [(o, o - o % 320 + (o + 64) % 320, o - o % 320 + (o + 128) % 320) for o in range(1600)]
IOTA = [[z for z in range(64) if RC[r] >> z & 1] for r in range(6)]
SRC_SEL = [SRC[64 * x + z] for x, z in PLANES]
def ref_round(A, r):
 C = [A[a] ^ A[b] ^ A[c] ^ A[d] ^ A[e] for a, b, c, d, e in CIDX]
 D = [C[a] ^ C[b] for a, b in DIDX]
 B = [A[s] ^ D[d] for s, d in SRC]
 A = [B[a] ^ (~B[b] & B[c]) for a, b, c in CHI]
 for z in IOTA[r]:
  A[z] ^= M256
 return A
def ref_values(P):
 def two(Pv):
  A = [0] * 1600
  A[0:320], A[640:960] = Pv, Pv
  for z in (57, 58, 63):
   A[1024 + z] = M256
  return ref_round(ref_round(A, 0), 1)
 S0 = two(P)
 DEL = [[a ^ b for a, b in zip(two([p ^ M256 if w >> k & 1 else p for k, p in enumerate(P)]), S0)]
 for w in W40[:N_DIR]]
 val = {}
 def dfs(S, A, last):
  B = A
  for r in (2, 3, 4):
   B = ref_round(B, r)
  C = [B[a] ^ B[b] ^ B[c] ^ B[d] ^ B[e] for a, b, c, d, e in CIDX]
  D = [C[a] ^ C[b] for a, b in DIDX]
  val[S] = [B[s] ^ D[d] for s, d in SRC_SEL]
  if S.bit_count() < DEG:
   for j in range(last + 1, N_DIR):
    dfs(S | 1 << j, [a ^ b for a, b in zip(A, DEL[j])], j)
 dfs(0, S0, -1)
 return val
def ldr(a):
 return MOV(a[0]) if type(a) is tuple else LDW(a)
def tr64(src, dst, sh):
 R = [0, 0] + [ldr(a) for a in src[2:]]
 for k in (0, 1):
  STW(TW + k, ldr(src[k]))
 for b in range(6):
  s, m = 1 << b, MASK[1 << b]
  for k in range(64):
   if k & s:
    continue
   kk = k + s
   if k >= 2:
    t = AND(XOR(SHR(R[k], s), R[kk]), m)
    R[k], R[kk] = XOR(R[k], SHL(t, s)), XOR(R[kk], t)
   elif kk >= 2:
    u = LDW(TW + k)
    t = AND(XOR(SHR(u, s), R[kk]), m)
    R[kk] = XOR(R[kk], t)
    STW(TW + k, XOR(u, SHL(t, s)))
   else:
    u, v = LDW(TW), LDW(TW + 1)
    STW(TW + 2, u)
    t = AND(XOR(SHR(u, s), v), m)
    STW(TW + 1, XOR(v, t))
    t = SHL(t, s)
    STW(TW, XOR(LDW(TW + 2), t))
 for k in range(64):
  v = R[k] if k >= 2 else LDW(TW + k)
  STW(dst[k], OR(LDW(dst[k]), SHL(v, sh)) if sh else v)
def transpose():
 for g in range(4):
  tr64([WF + 2 * c for c in range(64 * g, 64 * g + 64)], range(PL + 64 * g, PL + 64 * g + 64), 0)
 for s in (64, 128):
  for k in range(256):
   if not k & s:
    u, v = LDW(PL + k), LDW(PL + k + s)
    t = AND(XOR(SHR(u, s), v), MASK[s])
    STW(PL + k, XOR(u, SHL(t, s)))
    STW(PL + k + s, XOR(v, t))
 for g in range(4):
  tr64([WF + 2 * c + 1 for c in range(64 * g, 64 * g + 64)], range(PL + 256, PL + 320), 64 * g)
def rtrans(base, dst, mark):
 rows = [(0,) if p is None else base + p for p in ROWS]
 if mark:
  rows[143] = (M256,)
 for g in range(4):
  tr64(rows[64 * g:64 * g + 64], range(dst + 64 * g, dst + 64 * g + 64), 0)
 for s in (64, 128):
  for k in range(256):
   if not k & s:
    u, v = LDW(dst + k), LDW(dst + k + s)
    t = AND(XOR(SHR(u, s), v), MASK[s])
    STW(dst + k, XOR(u, SHL(t, s)))
    STW(dst + k + s, XOR(v, t))
class Gen:
 def __init__(s, n):
  s.n, s.code = n, []
 def x(s, a, b):
  if a < 2 and b < 2:
   return a ^ b
  if a == 0 or b == 0:
   return b if a == 0 else a
  if a == b:
   return 0
  s.n += 1
  s.code.append((4, s.n, b, 0) if a == 1 else (4, s.n, a, 0) if b == 1 else (2, s.n, a, b))
  return s.n
 def a(s, a, b):
  if a < 2 and b < 2:
   return a & b
  if a == 0 or b == 0:
   return 0
  if a == 1 or b == 1:
   return b if a == 1 else a
  s.n += 1
  s.code.append((3, s.n, a, b))
  return s.n
 def nt(s, a):
  if a < 2:
   return 1 - a
  s.n += 1
  s.code.append((4, s.n, a, 0))
  return s.n
def bgen(g, st, mem, r, fm=0):
 C, D, pc, dc = [[0] * 64 for _ in range(5)], [[0] * 64 for _ in range(5)], [], []
 for z in range(64):
  g.code, have = [], set()
  for x in range(5):
   v = None
   for y in range(5):
    t = st[x + 5 * y][z]
    if t > 1 and t not in have:
     have.add(t)
     g.code.append((0, t, mem[t], 0))
    v = t if v is None else g.x(v, t)
   C[x][z] = v
  pc.append(g.code)
 for z in range(64):
  g.code = []
  for x in range(5):
   D[x][z] = g.x(C[x - 1][z], C[(x + 1) % 5][z - 1])
  dc.append(g.code)
 cc, dd = all(v < 2 for c in C for v in c), all(v < 2 for d in D for v in d)
 need(dd or not cc, 'constant parities give constant D words')
 code, dad = [], {}
 if not cc:
  code += pc[63]
  for z in range(64):
   code += pc[z] if z < 63 else []
   if not dd:
    code += dc[z]
    for x in range(5):
     if D[x][z] > 1 and D[x][z] not in dad:
      dad[D[x][z]] = DW + 64 * x + z
      code.append((1, DW + 64 * x + z, D[x][z], 0))
 if r == 5 and fm:
  pv = {}
  for z in (0, 1):
   for x in range(5):
    g.code, vz = [], (z - RHO[6 * x]) % 64
    s, d = st[6 * x][vz], D[x][vz]
    for t in (s, d):
     if t > 1:
      g.code.append((0, t, dad.get(t, mem.get(t)), 0))
    pv[x, z] = g.x(s, d)
    code += g.code
  for f, (z, xs) in enumerate(FORMS):
   g.code, v = [], pv[xs[0], z]
   for x in xs[1:]:
    v = g.x(v, pv[x, z])
   code += g.code + [(5, f, v, 0)]
  return code, None
 if r == 5:
  for p, (x, z) in enumerate(PLANES):
   g.code, vz = [], (z - RHO[6 * x]) % 64
   s, d = st[6 * x][vz], D[x][vz]
   for t in (s, d):
    if t > 1:
     g.code.append((0, t, dad.get(t, mem.get(t)), 0))
   v = g.x(s, d)
   code += g.code + [(5, p, v, 0)]
  return code, None
 nxt, new = [[0] * 64 for _ in range(25)], {}
 for z in range(64):
  g.code, have, B = [], set(), [0] * 25
  for i in range(25):
   x, y, vz = i % 5, i // 5, (z - RHO[i]) % 64
   s, d = st[i][vz], D[x][vz]
   for t in (s, d):
    if t > 1 and t not in have:
     have.add(t)
     g.code.append((0, t, dad.get(t, mem.get(t)), 0))
   B[y + 5 * ((2 * x + 3 * y) % 5)] = g.x(s, d)
  A = [g.x(B[k], g.a(g.nt(B[k - k % 5 + (k + 1) % 5]), B[k - k % 5 + (k + 2) % 5])) for k in range(25)]
  if RC[r] >> z & 1:
   A[0] = g.x(A[0], 1)
  for k in range(25):
   v = nxt[k][z] = A[k]
   if v > 1 and v not in mem and v not in new:
    new[v] = RB + 1600 * r + 64 * k + z
    g.code.append((1, new[v], v, 0))
  code += g.code
 mem.update(new)
 return code, nxt
def bcode(fm=0):
 st, mem = [[0] * 64 for _ in range(25)], {}
 for k in range(5):
  for z in range(64):
   st[k][z] = st[10 + k][z] = 2 + 64 * k + z
   mem[2 + 64 * k + z] = PL + 64 * k + z
 for z in (57, 58, 63):
  st[16][z] = 1
 g, codes = Gen(321), []
 for r in range(6):
  c, st = bgen(g, st, mem, r, fm)
  need(None not in [o[2] for o in c if o[0] == 0], 'every LOAD has an address')
  codes.append([(6, a, b - PL, 0) if t == 0 and PL <= b < PL + 320 else (0, a, b - WB, 0) if t == 0 else (1, a - WB, b, d) if t == 1
 else (t, a, b, d) for t, a, b, d in c])
 return codes, g.n
FORMS = ((0, (0, 1)), (0, (1, 2)), (0, (2, 3)), (0, (3, 4)), (1, (1,)), (1, (3,)), (1, (0, 2)), (1, (2, 4)))
BCODE, BREG = bcode()
BRND = (1978, 11651, 14725, 14723, 14725, 4220)
need(sorted(o[2] for o in BCODE[0] if o[0] == 6) == sorted(2 * list(range(320))), 'round 0 LOADs each plane twice')
def peak(ops, out=()):
 live, top = set(out), len(out)
 for d, src in reversed(ops):
  live.discard(d)
  live.update(src)
  top = max(top, len(live))
 return top
def sops(codes):
 ops, n = [], 0
 for code in codes:
  for t, d, a, b in code:
   if t == 'r':
    n -= 3
    ops += [(n, {a}), (n + 1, {a}), (n + 2, {n, n + 1}), (d, {n + 2})]
   else:
    ops.append((d, {a, b} if t in ('x', 'a') else {a}))
 return ops
def bpeak(codes):
 return [peak([(a, ()) if t in (0, 6) else (None, (b,)) if t in (1, 5) else (a, (b, d) if t < 4 else (b,))
 for t, a, b, d in c]) for c in codes]
BPEAK = bpeak(BCODE)
SPEAK = peak(sops(SCODE), SOUT)
need(BPEAK == [11, 28, 28, 28, 28, 16] and SPEAK + 4 + 1 == 39 and len(CACHED) + 2 + 2 == 64,
 'register peaks: setup rounds, verification 39 of the 61 freed and v, main loop 64')
PLR, INR = PL - WB, INF - WB
def run(code, R, base, w, done):
 n, W, o = len(code), WRK, base - WB
 for t, a, b, c in code:
  if t == 2:
   R[a] = R[b] ^ R[c]
  elif t == 0:
   R[a] = v = W[b]
   if v is None:
    raise SystemExit('check failed: read of a never-written work word')
  elif t == 1:
   W[a] = R[b]
  elif t == 4:
   R[a] = R[b] ^ M256
  elif t == 3:
   R[a] = R[b] & R[c]
  elif t == 6:
   if not w >> b & 1:
    R[a] = W[PLR + b]
   elif b in done:
    R[a] = W[INR + b]
   else:
    done.add(b)
    R[a] = W[INR + b] = W[PLR + b] ^ M256
    n += 2
  else:
   W[o + a] = R[b]
 K[0] += n
NS = 5
KAF, KBF = (15, 15, 14, 14), (13, 13, 13, 13)
SETUP_PT = (1347, 11651, 14725, 13666, 3865, 244)
need(sum(KAF) + 4 + 2 == 64 and sum(KBF) + 4 + 7 + 1 == 64, 'registers of the two passes')
def dce_b(codes):
 nr, na, keep = set(), set(), []
 for code in reversed(codes):
  k = []
  for t, a, b, c in reversed(code):
   if t == 5 or (t == 1 and a in na) or (t in (0, 6, 2, 3, 4) and a in nr):
    if t in (0, 6, 2, 3, 4):
     nr.discard(a)
    if t == 1:
     na.discard(a)
    if t == 0:
     na.add(b)
    if t in (1, 4, 5):
     nr.add(b)
    if t in (2, 3):
     nr.update((b, c))
    k.append((t, a, b, c))
  keep.append(k[::-1])
 return keep[::-1]
FCODE, FREG = bcode(1)
FCODE = dce_b(FCODE)
need([len(c) for c in FCODE] == list(SETUP_PT) and all(map(int.__le__, bpeak(FCODE), BPEAK)), 'setup code of the forms: counts, register peaks')
def sav(T, n):
 m = T.bit_length() - 1
 if T.bit_count() < DEG:
  return 2 * ((1 << (n - 1 - m)) - 1 if m <= n - 2 else 0) - 1
 return (1 << (n - 1 - m)) - 1
def cache_set(k, n):
 return set(sorted((T for T in range(1, 1 << n) if T.bit_count() <= DEG), key=lambda T: (-sav(T, n), T))[:k])
def fes_f(n, CR):
 n1 = (1 << n) - 1
 links = sum(comb(n, k) * min(DEG, k) for k in range(1, n + 1)) - n1
 lcr = tcr = 0
 for T in CR:
  m = T.bit_length() - 1
  if T.bit_count() < DEG:
   lcr += (1 << (n - 1 - m)) - 1 if m <= n - 2 else 0
   tcr += 1
  else:
   tcr += (1 << (n - 1 - m)) if m <= n - 1 else 0
 uall = sum(comb(n - 1, k) for k in range(1, DEG))
 unc = uall - sum(1 for T in CR if T.bit_count() < DEG and T.bit_length() - 1 <= n - 2)
 return len(CR) + 1 + n1 + (n1 - tcr) + 3 * links - 2 * lcr - unc
def forms_setup():
 SB = [S for S in SUBS if S < 1 << NS]
 sec('cs')
 R0, pop = [0, M256] + [None] * (FREG - 1), 0
 for S in SB:
  w = 0
  for b in range(NS):
   if S >> b & 1:
    w ^= W40[b]
  R, cnt, done = R0[:], [], set()
  for r in range(6):
   k0 = K[0]
   run(FCODE[r], R, AFO + 8 * IDX[S], w, done)
   cnt.append(K[0] - k0)
  need(cnt == [SETUP_PT[0] + 2 * w.bit_count(), *SETUP_PT[1:]], 'forms setup: 1347 + 2 popcount, 11651, 14725, 13666, 3865, 244')
  pop += w.bit_count()
 need(pop == popsum(NS) and SECS['cs'][0] == sum(SETUP_PT) * len(SB) + 2 * pop, 'forms setup: 45498 per point')
 sec('ct')
 for j in range(NS):
  for S in SB:
   if S >> j & 1:
    bs, bt = AFO + 8 * IDX[S], AFO + 8 * IDX[S ^ 1 << j]
    for f in range(8):
     STW(bs + f, XOR(LDW(bs + f), LDW(bt + f)))
 need(SECS['ct'][0] == 32 * sum(S.bit_count() for S in SB), 'forms transform 4 * 8 * J')
 sec('cp')
 nt = 0
 for T in SB[1:]:
  R, k = (T >> 1) & ~T, DEG - T.bit_count()
  Vs, V = [], R
  while True:
   if V.bit_count() <= k:
    Vs.append(AFO + 8 * IDX[T | V])
   if not V:
    break
   V = (V - 1) & R
  nt += len(Vs)
  for f in range(8):
   acc = LDW(Vs[0] + f)
   for b in Vs[1:]:
    acc = XOR(acc, LDW(b + f))
   STW(TFO + 8 * IDX[T] + f, acc)
 need(SECS['cp'][0] == 16 * nt and nt == vd(NS), 'forms phase 2 * 8 * V')
def forms_fes(K24):
 SB = [S for S in SUBS if S < 1 << NS]
 for T in SUBS:
  for f, (z, xs) in enumerate(FORMS):
   e = 0
   for x in xs:
    e ^= WRK[(ACO if T == 0 else TABB) - WB + NPL * IDX[T] + x + 5 * z]
   WRK[FFR - WB + 8 * IDX[T] + f] = e
 need(all(WRK[(AFO if T == 0 else TFO) - WB + 8 * IDX[T] + f] == WRK[FFR - WB + 8 * IDX[T] + f] for T in SB for f in range(8)),
 'counted form records equal the XOR of the reference plane records, T within the first NS directions')
 exp = [0] * (1 << N_DIR)
 for n_, k in enumerate(K24):
  if k & 255 == 1:
   exp[n_ >> 8] |= 1 << (n_ & 255)
 sw = [0] * (1 << N_DIR)
 for pas, (fl, ks) in enumerate(((range(4), KAF), (range(4, 8), KBF))):
  sec('cfa' if pas == 0 else 'cfb')
  STW(ACB + (1 << N_DIR), 0)
  CR = [cache_set(k, N_DIR) for k in ks]
  reg = [{T: LDW(FFR + 8 * IDX[T] + f) for T in CR[q]} for q, f in enumerate(fl)]
  x = [LDW(FFR + f) if f in (1, 2, 3) else NOT(LDW(FFR + f)) for f in fl]
  for i in range(1 << N_DIR):
   for q, f in enumerate(fl):
    if i:
     top, chain = SITES[i - 1]
     w = reg[q][top] if top in CR[q] else LDW(FFR + 8 * IDX[top] + f)
     for T, last in chain:
      if T in CR[q]:
       w = reg[q][T] = XOR(reg[q][T], w)
      else:
       a = FFR + 8 * IDX[T] + f
       w = XOR(LDW(a), w)
       if last:
        WRK[a - WB] = None
       else:
        STW(a, w)
     x[q] = XOR(x[q], w)
   t = AND(AND(AND(x[0], x[1]), x[2]), x[3])
   if pas == 0:
    STW(ACB + i, t)
   else:
    sw[i] = AND(t, LDW(ACB + i))
  for q, f in enumerate(fl):
   for T, v in reg[q].items():
    STW(FFR + 8 * IDX[T] + f, v)
   STW(FFR + f, x[q])
  c = LDW(ACB + (1 << N_DIR))
  c = ADD(c, 1)
  STW(ACB + (1 << N_DIR), c)
  BR(EQ(c, 1))
  for b in (ACB, FFR, TFO):
   ADD(c, b)
  need(K[0] == sum(fes_f(N_DIR, CR[q]) + k + 1 for q, k in enumerate(ks)) + (1, 4)[pas] + (4 + pas) * (1 << N_DIR) + 9, 'pass %s count' % 'AB'[pas])
 need(sw == exp, 'the filter word equals the survivors of the emitted keys at every Gray point')
def build_tables():
 for b in range(5):
  for k in range(2):
   base = TBY + 512 * b + 256 * k
   STW(base, 0)
   for v in range(1, 256):
    j = (v & -v).bit_length() - 1
    STW(base + v, XOR(LDW(base + (v ^ 1 << j)), WW[8 * b + j][k]))
def jaddr(cid):
 return ADD(SHL(OR(SHL(SHR(cid, 48), 8), AND(SHR(cid, N_DIR), 255)), 1), CSB)
def cold_msg(cid):
 k0 = K[0]
 i = AND(cid, (1 << N_DIR) - 1)
 a = jaddr(cid)
 w0, w1 = LDC(a), LDC(ADD(a, 1))
 g = XOR(i, SHR(i, 1))
 for b in range(5):
  v = AND(SHR(g, 8 * b), 255) if b else AND(g, 255)
  w0 = XOR(w0, LDW(ADD(v, TBY + 512 * b)))
  w1 = XOR(w1, LDW(ADD(v, TBY + 512 * b + 256)))
 L = lanes5(w0, w1)
 need(K[0] - k0 == 58, 'earlier candidate 58 operations')
 return w0 | w1 << 256, L
def cur_msg(v, i):
 k0 = K[0]
 g, m0, m1 = i ^ i >> 1, 0, 0
 for b in range(N_DIR):
  if g >> b & 1:
   m0, m1 = m0 ^ WW[b][0], m1 ^ WW[b][1]
 a = jaddr(AND(v, M128))
 w0 = XOR(LDC(a), m0)
 w1 = XOR(LDC(ADD(a, 1)), m1)
 L = lanes5(w0, w1)
 need(K[0] - k0 == 19, 'current candidate 19 operations')
 return w0 | w1 << 256, L
def verify(cold, live, i):
 prev = K
 sec('verify' if prev is not SECS['vcheck'] else 'vcheck')
 f = ADD(LDW(FCW), 1)
 STW(FCW, f)
 out = ('cap', None, None, None, None, live)
 if not BR(EQ(f, CAPF)):
  for k, w in enumerate(live):
   STW(SPL + k, w)
  ta, la = cold_msg(cold)
  da = rounds6(la)
  tb, lb = cur_msg(REGS['v'], i)
  db = rounds6(lb)
  st = 'equal'
  for k in range(4):
   if not BR(EQ(da[k], db[k])):
    st = 'differ'
    break
  out = (st, ta, tb, da, db, [LDW(SPL + k) for k in range(len(live))])
 globals()['K'] = prev
 return out
def probe(k):
 cid = REGS['cid']
 v = REGS['v']
 s = LDS(k)
 if BR(SHR(XOR(s, v), 128)):
  STS(k, v)
  REGS['I'] += 1
  REGS['v'] = ADD(v, 1)
  REGS['cid'] = REGS['v'] & M128
  return None
 s = LDS(k)
 if BR(LT(s, v)):
  c2 = AND(LDS(k), M128)
  need(c2 < cid, 'hit: an earlier identifier')
  return c2
 STS(k, v)
 REGS['X'] += 1
 REGS['I'] += 1
 f = ADD(LDW(FCW), 1)
 STW(FCW, f)
 if BR(EQ(f, CAPF)):
  return 'cap'
 REGS['v'] = ADD(v, 1)
 REGS['cid'] = REGS['v'] & M128
 return None
REGS = {'h': 0, 'F': 0, 'cid': 0, 'M': 0, 'X': 0, 'I': 0, 'r': 0, 'R_HI': 0, 'v': 0}
def run_group(h, seeds, mode):
 global SPARSE, WRK, CREC
 for s in SECS.values():
  s[0] = 0
 CALLS[0] = 0
 SPARSE, WRK, CREC = {}, [None] * (WEND - WB), {}
 GBASE[0] = h << 48
 REGS.update(M=0, X=0, I=0)
 sec('once')
 REGS['h'], REGS['F'] = MOV(h), MOV(0)
 rval = (((h + 1) * GM) & ((1 << 127) - 1)) | 1
 REGS['r'] = MOV(rval)
 REGS['R_HI'] = SHL(REGS['r'], 128)
 REGS['v'] = OR(REGS['R_HI'], SHL(REGS['h'], 48))
 build_tables()
 need(SECS['once'][0] == 6 + 7660, 'one-time control 6 (group index, count F, tag r and v) and byte tables 7660')
 per, origins = leaders(seeds)
 for c in range(LANES):
  j = 256 * h + c
  need(CREC[CSB + 2 * j] | CREC[CSB + 2 * j + 1] << 256 == origins[c] < 1 << 320, 'coset record')
  need(per[c] == 11, 'leader count 11 per coset')
 own = [{} for _ in range(LANES)]
 sec('fes')
 STW(HSP, REGS['h'])
 STW(FCW, REGS['F'])
 REGS['h'] = REGS['F'] = None
 sec('sgroup')
 transpose()
 P = [sum((t >> k & 1) << c for c, t in enumerate(origins)) for k in range(320)]
 need(SECS['sgroup'][0] == 13616 and WRK[PL - WB:PL - WB + 320] == P, 'transpose 13616, bitplanes equal the origins')
 sec('spoint')
 pop, R0 = 0, [0, M256] + [None] * (BREG - 1)
 for S in SUBS:
  w = 0
  for b in range(N_DIR):
   if S >> b & 1:
    w ^= W40[b]
  R, cnt, done = R0[:], [], set()
  for r in range(6):
   k0 = K[0]
   run(BCODE[r], R, ACO + NPL * IDX[S], w, done)
   cnt.append(K[0] - k0)
  need(cnt == [BRND[0] + 2 * w.bit_count(), *BRND[1:]], 'rounds 0..4 (1978 + 2 popcount, 11651, 14725, 14723, '
 '14725), linear step 4220')
  pop += w.bit_count()
 need(pop == POP and SECS['spoint'][0] == 62022 * len(SUBS) + 2 * POP, 'setup points: 62022 P + 2 popcount sum')
 val = ref_values(P)
 need(all(WRK[ACO - WB + NPL * IDX[S]:ACO - WB + NPL * IDX[S] + NPL] == val[S] for S in SUBS),
 'counted setup equals the reference at every point and lane')
 del val, P
 sec('transform')
 for j in range(N_DIR):
  for S in SUBS:
   if S >> j & 1:
    bs, bt = ACO + NPL * IDX[S], ACO + NPL * IDX[S ^ 1 << j]
    for p in range(NPL):
     STW(bs + p, XOR(LDW(bs + p), LDW(bt + p)))
 need(SECS['transform'][0] == 4 * NPL * J_D, 'transform 4 * 175 * J_D')
 sec('phase')
 for T in SUBS[1:]:
  R, k = (T >> 1) & ~T, DEG - T.bit_count()
  Vs, V = [], R
  while True:
   if V.bit_count() <= k:
    Vs.append(ACO + NPL * IDX[T | V])
   if not V:
    break
   V = (V - 1) & R
  bt = TABB + NPL * IDX[T]
  for p in range(NPL):
   acc = LDW(Vs[0] + p)
   for b in Vs[1:]:
    acc = XOR(acc, LDW(b + p))
   STW(bt + p, acc)
 need(SECS['phase'][0] == 2 * NPL * V_D, 'phase 2 * 175 * V_D')
 sec('rtr')
 for S in SUBS:
  rtrans(ACO if S == 0 else TABB + NPL * IDX[S], CMR + 256 * IDX[S], S == 0)
 need(SECS['rtr'][0] == RTR * len(SUBS) and RTR == 7800, 'record transposes 7800 per record')
 A0 = WRK[ACO - WB:ACO - WB + NPL]
 need(all(WRK[CMR - WB + c] == sum((A0[p] >> c & 1) << r for r, p in enumerate(ROWS) if p is not None) | MARK
 for c in range(LANES)), 'candidate-major current values equal the planes')
 sec('fes')
 REGS['h'] = LDW(HSP)
 sec('leader')
 REGS['cid'] = SHL(REGS['h'], 48)
 REGS['h'] = None
 st = {'checks': 0, 'mismatch': 0}
 K24 = [0] * QR
 found = key0 = None
 for c in range(LANES):
  sec('buf')
  for k in range(len(SUBS)):
   STW(FR + k, LDW(CMR + 256 * k + c))
  sec('fes')
  f0, t0, m0, x0 = SECS['fes'][0], SECS['table'][0], REGS['M'], REGS['X']
  reg = {T: LDW(FR + IDX[T]) for T in CACHED}
  x = LDW(FR)
  o = own[c]
  for i in range(1 << N_DIR):
   if i:
    sec('fes')
    k1 = K[0]
    top, chain = SITES[i - 1]
    w = reg[top] if top in CSET else LDW(FR + IDX[top])
    for T, last in chain:
     if T in CSET:
      w = reg[T] = XOR(reg[T], w)
     else:
      a = FR + IDX[T]
      w = XOR(LDW(a), w)
      if last:
       WRK[a - WB] = None
      else:
       STW(a, w)
    x = XOR(x, w)
    need(K[0] - k1 == COST[i - 1], 'FES count per Gray step')
   sec('cht')
   t1 = SHR(x, 2 * STRIDE)
   t2 = AND(SHR(x, STRIDE), t1)
   key = AND(XOR(XOR(t1, t2), x), KEYMASK)
   sec('table')
   need(REGS['cid'] == (h << 48) + (c << N_DIR) + i, 'identifier of candidate (h, c, i)')
   e = ev24(key)
   K24[LANES * i + c] = e
   o[e & 0xFFFF] = o.get(e & 0xFFFF, 0) + 1
   if c == i % LANES:
    d = sha3_256(message(point(origins[c], i)))
    kn = sum(((int.from_bytes(d[8 * y:8 * y + 8], 'little') ^ (RC[5] if y == 0 else 0)) & (1 << 35) - 1)
 << STRIDE * y for y in range(4))
    st['checks'] += 1
    st['mismatch'] += kn | MARK != key
   if c == i == 0:
    key0 = key
   t1, x1 = K[0], REGS['X']
   r = probe(key)
   if r == 'cap':
    need(K[0] - t1 == 13 and WRK[FCW - WB] == CAPF, 'false pass halted at the cap after 13 operations')
    found = ('cap', None, None, None, None, None)
    break
   if r is not None:
    REGS['M'] += 1
    v = verify(r, [reg[T] for T in CACHED] + [x], i)
    if v[0] != 'differ':
     found = v
     break
    reg, x = dict(zip(CACHED, v[5])), v[5][-1]
    REGS['v'] = ADD(REGS['v'], 1)
    REGS['cid'] = REGS['v'] & M128
   need(K[0] - t1 == (10 if r is not None else 14 if REGS['X'] > x1 else 6), 'table path 6, 14 or 10')
  if found:
   break
  dm, dx = REGS['M'] - m0, REGS['X'] - x0
  need(SECS['fes'][0] - f0 == FCOSET, 'FES count per coset')
  need(SECS['table'][0] - t0 == 6 * ((1 << N_DIR) - dm - dx) + 14 * dx + 10 * dm, 'table 6 / 14 / 10')
 if not found:
  sec('leader')
  BR(EQ(SHR(REGS['cid'], 48), G))
  need(SECS['leader'][0] == 11 * LANES + 5, 'leader 11 per coset, group control 5')
  need(SECS['fes'][0] == LANES * FCOSET + 3 and SECS['cht'][0] == 6 * QR and
 SECS['buf'][0] == 2 * len(SUBS) * LANES, 'FES (256 cosets, h and F 3), chi 6 per candidate, frame copies')
  need(REGS['I'] == QR - REGS['M'] and REGS['cid'] == (h << 48) + QR, 'sparse inserts, identifiers')
  need(WRK[FCW - WB] == REGS['M'] + REGS['X'] < CAPF, 'F counts verifications and false passes, below the cap')
  sec('vcheck')
  k1 = K[0]
  r = probe(key0)
  REGS['v'] = ADD(REGS['v'], 1)
  REGS['cid'] = REGS['v'] & M128
  need(r == h << 48 and K[0] - k1 == 10, 'valid hit 10 operations')
  k1, saved, WRK[FCW - WB] = K[0], WRK[FCW - WB], 0
  REGS['cid'] = (h << 48) + (80 << N_DIR) + 1
  REGS['v'] = REGS['R_HI'] | REGS['cid']
  v = verify(r, [reg[T] for T in CACHED] + [x], 1)
  WRK[FCW - WB] = saved
  for t0, dd, tt in ((origins[0], v[3], v[1]), (origins[80] ^ W40[0], v[4], v[2])):
   need(tt == t0, 'reconstructed source')
   need(b''.join(w.to_bytes(8, 'little') for w in dd) == sha3_256(message(tt)), 'reconstructed digest')
  need(v[0] == 'differ' and CALLS[0] == 0 and K[0] - k1 <= 2428, 'verification <= 2428, no permutation call')
  forms_setup()
  forms_fes(K24)
 need(SECS['verify'][0] <= 2428 * REGS['M'], 'verification bound')
 need(found or (c, i) == (LANES - 1, NST), 'all cosets and Gray points')
 need(SECS['once'][0] == 7666, 'once ops 7666')
 obs = {'fes_ops': SECS['fes'][0], 'buffer_reads': SECS['buf'][0],
 'chi_transpose_ops': SECS['cht'][0] + SECS['rtr'][0],
 'table_ops': SECS['table'][0], 'sparse_inserts': REGS['I'],
 'in_range_mismatches': REGS['X'], 'key_matches': REGS['M'], 'leader_ops': SECS['leader'][0],
 'setup_group_ops': SECS['sgroup'][0], 'setup_point_ops': SECS['spoint'][0],
 'transform_phase_ops': SECS['transform'][0] + SECS['phase'][0],
 'verify_check_ops': SECS['vcheck'][0], 'perm_calls': CALLS[0], 'native_checks': st['checks'],
 'key_mismatch': st['mismatch']}
 out = [None] * LANES
 if found and found[0] == 'equal':
  ma, mb = message(found[1]), message(found[2])
  if ma != mb and sha3_256(ma) == sha3_256(mb):
   out[0] = (ma.hex(), mb.hex())
 if mode is None:
  return [dict(own_pairs16=sum(n * (n - 1) // 2 for n in o.values()), **obs) for o in own], out
 del obs['buffer_reads'], obs['sparse_inserts']
 if found:
  obs.update(pairs16_within=-1, pairs16_cross=-1, pairs24_cross=-1)
 else:
  counts, out = premise_test(K24, origins, mode)
  obs.update(counts)
 return [obs] * LANES, out
def point(t, i):
 g = i ^ i >> 1
 for b in range(N_DIR):
  if g >> b & 1:
   t ^= W40[b]
 return t
def pairs(vals):
 vals.sort()
 tot, run = 0, 1
 for a, b in zip(vals, vals[1:]):
  if a == b:
   tot += run
   run += 1
  else:
   run = 1
 return tot
PASS = {'pairs16_within': (421, 601), 'pairs16_cross': (129115, 132005), 'pairs24_cross': (420, 600)}
MASK16 = {'kind': 'digest-xor-mask', 'mask_hex': '0f00000000000000' * 4, 'expected_hex': '00' * 32}
MODES = {'fes-campaign-reduced': (None, {'kind': 'full-collision'}), 'hcoset-within16': ('within16', MASK16),
 'hcoset-cross16': ('cross16', MASK16), 'hcoset-filter8': ('filter8', MASK16)}
def filter8(K24, origins):
 sv = [n for n, k in enumerate(K24) if k & 255 == 1]
 need(422 <= len(sv) <= 602, 'survivor count')
 byv = {}
 for n in sv:
  byv.setdefault(K24[n] >> 8 & 255, []).append(n)
 npair, e = sum(len(v) * (len(v) - 1) // 2 for v in byv.values()), len(sv) * (len(sv) - 1) / 512
 need(abs(npair - e) <= 4 * e ** .5, 'pairs of survivors on event bits 8..15')
 out = [None] * LANES
 for t, (a, b) in enumerate([(v[j], v[j + 1]) for u, v in sorted(byv.items()) for j in range(len(v) - 1)][:LANES]):
  ma, mb = (message(point(origins[n % LANES], n // LANES)) for n in (a, b))
  da, db = sha3_256(ma), sha3_256(mb)
  need(ma != mb and all(da[8 * x] & 3 == 0 == db[8 * x] & 3 and (da[8 * x] ^ db[8 * x]) & 15 == 0 for x in range(4)),
 'returned survivor pair')
  out[t] = (ma.hex(), mb.hex())
 return {'survivors8': len(sv), 'pairs8_survivors': npair}, out
def premise_test(K24, origins, mode):
 col = [K24[c::LANES] for c in range(LANES)]
 w16 = sum(pairs([k & 0xFFFF for k in v]) for v in col)
 w24 = sum(pairs(list(v)) for v in col)
 counts = {'pairs16_within': w16, 'pairs16_cross': pairs([k & 0xFFFF for k in K24]) - w16,
 'pairs24_cross': pairs(list(K24)) - w24}
 for name, (lo, hi) in PASS.items():
  need(lo <= counts[name] <= hi, name + ' inside its pass interval')
 if mode == 'filter8':
  return filter8(K24, origins)
 out, half = [], 1 << N_DIR - 1
 for c in range(LANES):
  first, hit = {}, None
  if mode == 'within16':
   for i, k in enumerate(col[c]):
    if k & 0xFFFF in first:
     hit = ((c, first[k & 0xFFFF]), (c, i))
     break
    first[k & 0xFFFF] = i
  else:
   for i in range(half):
    first.setdefault(col[c][i] & 0xFFFF, i)
   for i in range(half, 2 * half):
    if col[c ^ 1][i] & 0xFFFF in first:
     hit = ((c, first[col[c ^ 1][i] & 0xFFFF]), (c ^ 1, i))
     break
  if hit:
   ma, mb = (message(point(origins[cc], ii)) for cc, ii in hit)
   da, db = sha3_256(ma), sha3_256(mb)
   need(ma != mb and all((da[8 * x] ^ db[8 * x]) & 15 == 0 for x in range(4)), 'returned pair on the mask')
   hit = (ma.hex(), mb.hex())
  out.append(hit)
 return counts, out
import ast, random
KBUD, GENBUD = 37950, 10370000
class Over(Exception):
 pass
GREG = ('NN', 'GC', 'EPB', 'CP', 'FC')
BIN = (ast.Add, ast.Sub, ast.BitXor, ast.BitAnd, ast.BitOr, ast.LShift, ast.RShift)
def isc(e, C):
 return isinstance(e, ast.Constant) or isinstance(e, ast.Name) and e.id in C or isinstance(e, ast.BinOp) and isc(e.left, C) and isc(e.right, C)
def cost(e, C):
 if isinstance(e, (ast.Constant, ast.Name)):
  return 0
 if isinstance(e, ast.BinOp):
  assert isinstance(e.op, BIN)
  return cost(e.left, C) + cost(e.right, C) + (0 if isc(e, C) else 1)
 if isinstance(e, ast.Compare):
  assert len(e.ops) == 1
  return 1 + cost(e.left, C) + cost(e.comparators[0], C)
 if isinstance(e, ast.Subscript):
  assert e.value.id == 'mem'
  return 1 + cost(e.slice, C)
 assert isinstance(e, ast.Call) and e.func.id in C['@F']
 return 2 + len(e.args) + sum(cost(a, C) for a in e.args)
def ops1(s, C):
 if isinstance(s, ast.Assign):
  t, v = s.targets[0], s.value
  if isinstance(t, ast.Subscript):
   return cost(v, C) + cost(t, C) + (1 if isc(v, C) else 0)
  c = cost(v, C)
  return c if c or isinstance(v, ast.Call) else 1
 if isinstance(s, ast.Expr):
  return cost(s.value, C)
 if isinstance(s, ast.Return):
  return 1 + (cost(s.value, C) if s.value else 0)
 if isinstance(s, (ast.Break, ast.Continue)):
  return 1
 assert isinstance(s, (ast.Pass, ast.Raise))
 return 0
def tcost(t, C):
 return 1 if isinstance(t, ast.Constant) else cost(t, C) + 1
def ub(b, C):
 t = 0
 for s in b:
  if isinstance(s, ast.If):
   t += tcost(s.test, C) + max(ub(s.body, C), ub(s.orelse, C))
  elif isinstance(s, ast.While):
   t += tcost(s.test, C) + 3
  elif isinstance(s, ast.For):
   t += 7
  else:
   t += ops1(s, C)
 return t
def stmt(src):
 return ast.parse(src).body
def block(b, C, reg, pend=0):
 out, pend = [], [pend]
 def flush():
  if pend[0]:
   out.extend(stmt('GC += %d' % (pend[0] + 1)))
   pend[0] = 0
 for s in b:
  if isinstance(s, (ast.Assign, ast.Expr, ast.Pass)):
   pend[0] += ops1(s, C)
   out.append(s)
  elif isinstance(s, (ast.Return, ast.Break, ast.Continue, ast.Raise)):
   pend[0] += ops1(s, C)
   flush()
   out.append(s)
  elif isinstance(s, ast.If):
   pend[0] += tcost(s.test, C)
   flush()
   out.append(ast.If(test=s.test, body=block(s.body, C, reg) or [ast.Pass()], orelse=block(s.orelse, C, reg)))
  elif isinstance(s, ast.While):
   flush()
   tc = tcost(s.test, C)
   reg.append(tc + 3 + ub(s.body, C))
   head = stmt('GC += %d\nif GC > BUD: raise Over' % (tc + 3))
   if not isinstance(s.test, ast.Constant):
    head.append(ast.If(test=ast.UnaryOp(op=ast.Not(), operand=s.test), body=[ast.Break()], orelse=[]))
   out.append(ast.While(test=ast.Constant(True), body=head + block(s.body, C, reg), orelse=[]))
  else:
   assert isinstance(s, ast.For)
   pend[0] += 1
   flush()
   reg.append(6 + ub(s.body, C))
   out.append(ast.For(target=s.target, iter=s.iter, body=stmt('GC += 6\nif GC > BUD: raise Over') + block(s.body, C, reg), orelse=[]))
 flush()
 return out
def compile_ram(src, C, bud):
 mod = ast.parse(src)
 C = dict(C)
 C['@F'] = {f.name for f in mod.body}
 reg = []
 for f in mod.body:
  reg.append(3 + ub(f.body, C))
  f.body = [ast.Global(names=list(GREG))] + stmt('GC += 3\nif GC > BUD: raise Over') + block(f.body, C, reg)
 ast.fix_missing_locations(mod)
 ns = dict(C)
 ns.update(Over=Over, BUD=bud, NN=0, GC=0, EPB=0, CP=0, FC=0)
 exec(compile(mod, '<ram>', 'exec'), ns)
 return ns, max(reg)
GENSRC = r'''
def new(op, a, b, im, sg):
 NN = NN + 1
 if NN < NMAX:
  pass
 else:
  raise Over
 mem[OPA + NN] = op
 mem[AA + NN] = a
 mem[BA + NN] = b
 mem[IMA + NN] = im
 if sg:
  mem[SGA + NN] = sg
 else:
  mem[SGA + NN] = mem[SIGA + NN]
 return NN
def xv(va, vb):
 p = (va ^ vb) & 1
 na = va >> 1
 nb = vb >> 1
 if na:
  if nb:
   sg = mem[SGA + na] ^ mem[SGA + nb]
   if sg:
    q = sg & HMASK
    while True:
     v = mem[HTA + q]
     if v < EPB:
      n = new(OXOR, na, nb, 0, sg)
      mem[HTA + q] = EPB + n
      return (n << 1) | p
     m = v - EPB
     if mem[SGA + m] == sg:
      return (m << 1) | p
     q = (q + 1) & HMASK
   return p
  return (na << 1) | p
 return (nb << 1) | p
def an(v1, v2):
 n1 = v1 >> 1
 n2 = v2 >> 1
 if n2:
  if n1:
   if n1 == n2:
    if (v1 ^ v2) & 1:
     return v2
    return 0
   if v1 & 1:
    u = new(OAND, n1, n2, 0, 0)
    if v2 & 1:
     return xv(u << 1, n1 << 1)
    return u << 1
   if v2 & 1:
    u = new(OOR, n1, n2, 0, 0)
    return (u << 1) | 1
   u = new(OOR, n1, n2, 0, 0)
   return xv(u << 1, n1 << 1)
  if v1 & 1:
   return 0
  return v2
 if v2 & 1:
  return v1 ^ 1
 return 0
def flip(v):
 n = v >> 1
 f = mem[FLA + n]
 if f < EPB:
  f = new(ONOT, n, 0, 0, 0)
  mem[FLA + n] = EPB + f
 else:
  f = f - EPB
 return (f << 1) | ((v & 1) ^ 1)
def chirow(src, st, dst, dt, sel):
 a = src
 v0 = mem[a]
 a = a + st
 v1 = mem[a]
 a = a + st
 v2 = mem[a]
 a = a + st
 v3 = mem[a]
 a = a + st
 v4 = mem[a]
 n0 = v0 >> 1
 n1 = v1 >> 1
 n2 = v2 >> 1
 n3 = v3 >> 1
 n4 = v4 >> 1
 ok = (n0 != 0) & (n1 != 0) & (n2 != 0) & (n3 != 0) & (n4 != 0)
 ok = ok & (n0 != n1) & (n0 != n2) & (n0 != n3) & (n0 != n4) & (n1 != n2) & (n1 != n3) & (n1 != n4) & (n2 != n3) & (n2 != n4) & (n3 != n4)
 u0 = v0
 u1 = v1
 u2 = v2
 u3 = v3
 u4 = v4
 if ok:
  pk = (v0 & 1) | ((v1 & 1) << 1) | ((v2 & 1) << 2) | ((v3 & 1) << 3) | ((v4 & 1) << 4)
  f = mem[PLN + (sel << 5) + pk]
  if f & 1:
   u0 = flip(v0)
  if f & 2:
   u1 = flip(v1)
  if f & 4:
   u2 = flip(v2)
  if f & 8:
   u3 = flip(v3)
  if f & 16:
   u4 = flip(v4)
 mem[dst] = xv(v0, an(u1, u2))
 a = dst + dt
 mem[a] = xv(v1, an(u2, u3))
 a = a + dt
 mem[a] = xv(v2, an(u3, u4))
 a = a + dt
 mem[a] = xv(v3, an(u4, u0))
 if sel:
  return 0
 a = a + dt
 mem[a] = xv(v4, an(u0, u1))
 return 0
def kround(src, dst, rc):
 for x in range(5):
  c = mem[src + x] ^ mem[src + x + 5] ^ mem[src + x + 10] ^ mem[src + x + 15] ^ mem[src + x + 20]
  mem[CX + x] = c
  mem[CX + x + 5] = c
 for x in range(5):
  c = mem[CX + x + 1]
  mem[DX + x] = mem[CX + x + 4] ^ (((c << 1) & M64) | (c >> 63))
 i = 0
 for y in range(5):
  for x in range(5):
   v = mem[src + i] ^ mem[DX + x]
   s = mem[RHT + i]
   mem[BQ + mem[PIT + i]] = ((v << s) & M64) | (v >> (64 - s))
   i = i + 1
 i = 0
 rw = BQ
 for y in range(5):
  for x in range(5):
   mem[dst + i] = mem[rw + x] ^ ((mem[rw + mem[T1 + x]] ^ M64) & mem[rw + mem[T2 + x]])
   i = i + 1
  rw = rw + 5
 mem[dst] = mem[dst] ^ rc
 return 0
def ev2(dst):
 kround(LN, X1, RC0C)
 kround(X1, dst, RC1C)
 return 0
def tr64():
 for s in range(6):
  sh = 32 >> s
  ms = mem[MST + s]
  for k in range(64):
   if k & sh:
    pass
   else:
    a = R64 + k
    x = mem[a]
    y = mem[a + sh]
    t = ((x >> sh) ^ y) & ms
    mem[a + sh] = y ^ t
    mem[a] = x ^ (t << sh)
 return 0
def forms():
 for k in range(5):
  v = mem[BASE + k]
  mem[LN + k] = v
  mem[LN + k + 10] = v
 ev2(S0)
 wp = WL
 dp = DF
 for b in range(30):
  for k in range(5):
   v = mem[BASE + k] ^ mem[wp + k]
   mem[LN + k] = v
   mem[LN + k + 10] = v
  wp = wp + 5
  ev2(SB)
  for i in range(25):
   mem[dp + i] = mem[SB + i] ^ mem[S0 + i]
  dp = dp + 25
 fm = FM
 for i in range(25):
  dp = DF + i
  for b in range(30):
   mem[R64 + b] = mem[dp]
   dp = dp + 25
  for b in range(34):
   mem[R64 + b + 30] = 0
  tr64()
  s = mem[S0 + i]
  for z in range(64):
   mem[fm + z] = mem[R64 + z]
   mem[fm + z + 1600] = (s >> z) & 1
  fm = fm + 64
 return 0
def netphase():
 for e in range(1600):
  mk = mem[FM + e]
  if mk:
   h = (mk ^ (mk >> 10) ^ (mk >> 20)) & 1023
   while True:
    k = mem[FKY + h]
    if k == mk:
     break
    if k:
     h = (h + 1) & 1023
    else:
     raise Over
   sym = mem[FSM + h]
   mem[SYM + e] = sym
   mem[NEA + sym] = EPB
 for t in range(NNET):
  e = NNET - 1 - t
  if mem[NEA + mem[NSY + e]] == EPB:
   a = mem[NAB + e]
   b = mem[NBB + e]
   if a > 29:
    mem[NEA + a] = EPB
   if b > 29:
    mem[NEA + b] = EPB
 for e in range(NNET):
  sym = mem[NSY + e]
  if mem[NEA + sym] == EPB:
   mem[VAL + sym] = xv(mem[VAL + mem[NAB + e]], mem[VAL + mem[NBB + e]])
 e = 0
 for i in range(25):
  na = NETA + i
  for z in range(64):
   v = 0
   if mem[FM + e]:
    v = mem[VAL + mem[SYM + e]]
   mem[na] = v ^ mem[FCN + e]
   na = na + 25
   e = e + 1
 return 0
def thetaz(z, aa, c, cm1, dst):
 for x in range(5):
  mem[DX2 + x] = xv(mem[c + x + 4], mem[cm1 + x + 1])
 i = 0
 for y in range(5):
  for x in range(5):
   mem[dst + (mem[PIT + i] << 6) + ((z + mem[RHT + i]) & 63)] = xv(mem[aa + i], mem[DX2 + x])
   i = i + 1
 return 0
def rnd(first, src, dst, rc):
 z = 0
 na = NETA
 while z < 64:
  if first:
   for i in range(25):
    mem[AS + i] = mem[na + i]
   na = na + 25
  else:
   sp = src + z
   dp = AS
   for r5 in range(5):
    chirow(sp, 64, dp, 1, 0)
    sp = sp + 320
    dp = dp + 5
   if (rc >> z) & 1:
    mem[AS] = mem[AS] ^ 1
  for x in range(5):
   v = xv(mem[AS + x], mem[AS + x + 5])
   v = xv(v, mem[AS + x + 10])
   v = xv(v, mem[AS + x + 15])
   v = xv(v, mem[AS + x + 20])
   mem[CN + x] = v
   mem[CN + x + 5] = v
  if z:
   thetaz(z, AS, CN, CPV, dst)
  else:
   for i in range(25):
    mem[A0 + i] = mem[AS + i]
   for x in range(10):
    mem[C0 + x] = mem[CN + x]
  for x in range(10):
   mem[CPV + x] = mem[CN + x]
  z = z + 1
 thetaz(0, A0, C0, CPV, dst)
 return 0
def feed(r):
 j = mem[FST + r]
 e = mem[FST + r + 1]
 while j < e:
  op = mem[ROP + j]
  n = new(op, mem[RES + mem[RAC + j]], mem[RES + mem[RBC + j]], mem[RIM + j], 0)
  mem[RES + 257 + j] = n
  if op == OPROBE:
   mem[LVA + n] = EPB
  j = j + 1
 return 0
def final():
 r = 0
 while r < 256:
  if r < 132:
   if (r & 3) == 0:
    chirow(BR2 + (r >> 2) + 2, 64, OB, 1, 1)
   o = mem[OB + (r & 3)]
   if o >> 1:
    pass
   else:
    raise Over
   if o & 1:
    o = flip(o)
   mem[RES + r + 1] = o >> 1
  else:
   if r == 143:
    mem[RES + 144] = new(OMOVI, 0, 0, ONES, 0)
  feed(r)
  r = r + 1
 return 0
def sweep():
 n = NN
 while n:
  if mem[LVA + n] == EPB:
   a = mem[AA + n]
   if a:
    mem[LVA + a] = EPB
   b = mem[BA + n]
   if b:
    mem[LVA + b] = EPB
  n = n - 1
 m = 0
 n = 1
 while n <= NN:
  if mem[LVA + n] == EPB:
   mem[RGA + n] = 0
   mem[INA + n] = 0
   mem[LSA + n] = INF
   op = mem[OPA + n]
   if op != OINP:
    if op != OMOVI:
     mem[ORD + m] = n
     m = m + 1
  n = n + 1
 return m
def emit(w0, w1):
 mem[CP] = w0
 mem[CP + 1] = w1
 CP = CP + 2
 return 0
def release(c, r):
 mem[RGA + c] = 0
 mem[FRE + FC] = r
 FC = FC + 1
 return 0
def getreg(ea, eb):
 if FC:
  FC = FC - 1
  return mem[FRE + FC]
 sa = mem[NXR + ea]
 mem[NXR + ea] = 0
 sb = mem[NXR + eb]
 mem[NXR + eb] = 0
 best = 0
 p = NXR + 4
 bp = p
 while p < NXR + 64:
  x = mem[p]
  if x > best:
   best = x
   bp = p
  x = mem[p + 1]
  if x > best:
   best = x
   bp = p + 1
  x = mem[p + 2]
  if x > best:
   best = x
   bp = p + 2
  x = mem[p + 3]
  if x > best:
   best = x
   bp = p + 3
  x = mem[p + 4]
  if x > best:
   best = x
   bp = p + 4
  x = mem[p + 5]
  if x > best:
   best = x
   bp = p + 5
  p = p + 6
 mem[NXR + eb] = sb
 mem[NXR + ea] = sa
 br = bp - NXR
 bn = mem[OCC + br]
 mem[RGA + bn] = 0
 if mem[INA + bn]:
  pass
 else:
  op = mem[OPA + bn]
  if op != OINP:
   if op != OMOVI:
    emit((ISTI << 18) | (br << 6), SPILL + bn)
    mem[INA + bn] = 1
 return br
def load(n, ea, eb):
 r = getreg(ea, eb)
 op = mem[OPA + n]
 if op == OINP:
  emit((IADDI << 18) | (RT1 << 12) | (RP << 6), mem[IMA + n])
  emit((ILD << 18) | (r << 12) | (RT1 << 6), 0)
 else:
  if op == OMOVI:
   emit((IMOVI << 18) | (r << 12), mem[IMA + n])
  else:
   emit((ILDI << 18) | (r << 12), SPILL + n)
 mem[RGA + n] = r
 mem[OCC + r] = n
 return r
def alloc(m):
 i = m
 while i:
  i = i - 1
  n = mem[ORD + i]
  a = mem[AA + n]
  b = mem[BA + n]
  mem[NDA + i] = mem[LSA + n]
  mem[NAA + i] = mem[LSA + a]
  if b:
   mem[NBA + i] = mem[LSA + b]
  mem[LSA + a] = i
  if b:
   mem[LSA + b] = i
 FC = 60
 for k in range(60):
  mem[FRE + k] = 63 - k
 i = 0
 while i < m:
  n = mem[ORD + i]
  a = mem[AA + n]
  b = mem[BA + n]
  ra = mem[RGA + a]
  if ra:
   pass
  else:
   ra = load(a, 0, mem[RGA + b])
  rb = 0
  if b:
   rb = mem[RGA + b]
   if rb:
    pass
   else:
    rb = load(b, ra, 0)
  x = mem[NAA + i]
  mem[NXR + ra] = x
  if x == INF:
   release(a, ra)
  if b:
   x = mem[NBA + i]
   mem[NXR + rb] = x
   if x == INF:
    if mem[RGA + b]:
     release(b, rb)
  op = mem[OPA + n]
  if op == OPROBE:
   emit((IADDI << 18) | (RT2 << 12) | (RVB << 6), mem[IMA + n])
   emit((ILD << 18) | (RT1 << 12) | (ra << 6), 0)
   emit((IXOR << 18) | (RT1 << 12) | (RT1 << 6) | RT2, 0)
   emit((ISHRI << 18) | (RT1 << 12) | (RT1 << 6), 128)
   emit(IBRNZ << 18 | (RT1 << 6), 0)
   emit((IST << 18) | (ra << 6) | RT2, 0)
  else:
   rd = getreg(ra, rb)
   emit((op << 18) | (rd << 12) | (ra << 6) | rb, mem[IMA + n])
   mem[RGA + n] = rd
   mem[OCC + rd] = n
   x = mem[NDA + i]
   mem[NXR + rd] = x
   if x == INF:
    raise Over
  i = i + 1
 return 0
def gen():
 NN = NTPL
 EPB = EPB + EPSTEP
 CP = PROG
 forms()
 for b in range(29):
  mem[VAL + b] = xv(mem[IWT + b] << 1, mem[IWT + b + 1] << 1)
 mem[VAL + 29] = mem[IWT + 29] << 1
 netphase()
 rnd(1, 0, BR1, 0)
 rnd(0, BR1, BR2, RC2C)
 rnd(0, BR2, BR1, RC3C)
 rnd(0, BR1, BR2, RC4C)
 final()
 m = sweep()
 alloc(m)
 k = ((CP - PROG) >> 1) + 5
 if k > KBUD:
  raise Over
 return k
'''
OPC = dict(XOR=1, AND=2, OR=3, NOT=4, ANDI=5, SHL=6, SHR=7, INP=8, MOVI=9, PROBE=10)
SIGIN = (6, 7, 5, 2, 3, 1, 4, 0)
ONES = (1 << 256) - 1
MASKS = {1 << b: sum(1 << c for c in range(256) if not c & 1 << b) for b in range(8)}
class Gr:
 def __init__(s):
  s.op, s.a, s.b, s.imm = [], [], [], []
 def new(s, op, a=None, b=None, imm=None):
  s.op.append(op); s.a.append(a); s.b.append(b); s.imm.append(imm)
  return len(s.op) - 1
class Tr:
 def __init__(s, g):
  s.g = g
 def sh(s, w, k, left):
  n, m = w
  m2 = (m << k) & ONES if left else m >> k
  return (None, 0) if n is None or not m2 else (s.g.new('SHL' if left else 'SHR', n, imm=k), m2)
 def andi(s, w, k):
  n, m = w
  m2 = m & k
  return (None, 0) if n is None or not m2 else w if m2 == m else (s.g.new('ANDI', n, imm=k), m2)
 def xor(s, a, b):
  return b if a[0] is None else a if b[0] is None else (s.g.new('XOR', a[0], b[0]), a[1] | b[1])
 def pairX(s, Ak, Ad, d):
  M = MASKS[d]
  t = s.andi(s.xor(s.sh(Ak, d, 0), Ad), M)
  return (Ak, Ad) if t[0] is None else (s.xor(Ak, s.sh(t, d, 1)), s.xor(Ad, t))
 def pairD(s, Ak, Ad, d):
  M = MASKS[d]
  H = (M << d) & ONES
  a1, a2 = s.andi(Ak, ONES ^ H), s.sh(s.andi(Ad, M), d, 1)
  d1, d2 = s.andi(Ad, ONES ^ M), s.andi(s.sh(Ak, d, 0), M)
  return s.xor(a1, a2), s.xor(d1, d2)
 def pair(s, Ak, Ad, d):
  g, n0 = s.g, len(s.g.op)
  s.pairX(Ak, Ad, d); c1 = len(g.op) - n0
  for l in (g.op, g.a, g.b, g.imm): del l[n0:]
  s.pairD(Ak, Ad, d); c2 = len(g.op) - n0
  for l in (g.op, g.a, g.b, g.imm): del l[n0:]
  return (s.pairX if c1 <= c2 else s.pairD)(Ak, Ad, d)
class Stream:
 def __init__(s, g, cb=None, sig=range(8)):
  s.T, s.stack, s.cb, s.sig = Tr(g), [], cb, list(sig)
 def f(s, v):
  return sum(1 << s.sig[m] for m in range(8) if v >> m & 1)
 def feed(s, w):
  grp, m = [w], 0
  while s.stack and s.stack[-1][0] == m:
   left = s.stack.pop()[1]
   d, sh = 1 << m, 1 << s.sig[m]
   for k in range(d):
    left[k], grp[k] = s.T.pair(left[k], grp[k], sh)
    if m == 7 and s.cb:
     s.cb(s.f(k), left[k]); s.cb(s.f(k + d), grp[k])
   grp, m = left + grp, m + 1
  s.stack.append((m, grp))
 def result(s):
  out = [None] * 256
  for v, w in enumerate(s.stack[0][1]):
   out[s.f(v)] = w
  return out
def hk_once():
 rng = random.Random(0x5EED)
 sig = [rng.getrandbits(256) | 1 for _ in range(1 << 16)]
 g = Gr(); st = Stream(g, sig=SIGIN)
 for v in range(256):
  st.feed((g.new('INP', imm=st.f(v)), (1 << 30) - 1))
 iw = st.result()
 tpl = [(OPC[g.op[n]], 0 if g.a[n] is None else g.a[n] + 1, 0 if g.b[n] is None else g.b[n] + 1, g.imm[n] or 0, sig[n]) for n in range(len(g.op))]
 rows = list(range(132)) + [143]
 g2 = Gr(); ph = {r: g2.new('IN') for r in rows}; nph = len(rows)
 so = Stream(g2, lambda c, w: g2.new('PROBE', w[0], imm=c))
 fst = []
 for r in range(256):
  fst.append(len(g2.op) - nph)
  so.feed((ph[r], ONES) if r in ph else (None, 0))
 fst.append(len(g2.op) - nph)
 rowof = {i: r for r, i in ph.items()}
 cd = lambda x: 0 if x is None else rowof[x] + 1 if x < nph else 257 + x - nph
 rec = [(OPC[g2.op[n]], cd(g2.a[n]), cd(g2.b[n]), g2.imm[n] or 0) for n in range(nph, len(g2.op))]
 pln = []
 for need_ in (range(5), range(4)):
  for pk in range(32):
   best = None
   for F in range(32):
    q = [(pk ^ F) >> j & 1 for j in range(5)]
    c = bin(F).count('1') + sum(q[(i + 1) % 5] == q[(i + 2) % 5] for i in need_)
    if best is None or c < best[0]:
     best = (c, F)
   pln.append(best[1])
 P0, lin = bits_pre(0), {}
 for b in range(30):
  Pb = bits_pre(W40[b])
  for i in range(25):
   for z in range(64):
    if (Pb[i] ^ P0[i]) >> z & 1:
     lin[(i, z)] = lin.get((i, z), 0) | 1 << b
 U = set()
 for i in range(25):
  j, k = i - i % 5 + (i % 5 + 1) % 5, i - i % 5 + (i % 5 + 2) % 5
  for z in range(64):
   fi, fj, fk = lin.get((i, z), 0), lin.get((j, z), 0), lin.get((k, z), 0)
   U |= {fi, fi ^ fj, fi ^ fk}
 U.discard(0)
 sets = {m: {b for b in range(30) if m >> b & 1} for m in sorted(U)}
 net, nxt = [], 30
 while True:
  cnt = {}
  for r in sets.values():
   for p in ((a, b) for a in sorted(r) for b in sorted(r) if a < b):
    cnt[p] = cnt.get(p, 0) + 1
  if not cnt:
   break
  (a, b), c = max(cnt.items(), key=lambda kv: (kv[1], -kv[0][0], -kv[0][1]))
  if c < 2:
   break
  net.append((nxt, a, b))
  for r in sets.values():
   if a in r and b in r:
    r -= {a, b}; r.add(nxt)
  nxt += 1
 fin = {}
 for m, r in sorted(sets.items()):
  r = sorted(r); cur = r[0]
  for x in r[1:]:
   net.append((nxt, cur, x)); cur = nxt; nxt += 1
  fin[m] = cur
 return sig, tpl, [iw[b][0] + 1 for b in range(30)], rec, fst, pln, net, fin
def bits_pre(t):
 L = keccak_f(lanes(t), 1)
 C = [L[x] ^ L[x + 5] ^ L[x + 10] ^ L[x + 15] ^ L[x + 20] for x in range(5)]
 D = [C[x - 1] ^ ((C[(x + 1) % 5] << 1 | C[(x + 1) % 5] >> 63) & M64) for x in range(5)]
 B = [0] * 25
 for i in range(25):
  v = L[i] ^ D[i % 5]
  B[i // 5 + 5 * ((2 * (i % 5) + 3 * (i // 5)) % 5)] = (v << RHO[i] | v >> (64 - RHO[i])) & M64
 return B
NMAX = 1 << 16
SPILL = 1 << 24
class HK:
 def __init__(s, bud=GENBUD, kbud=KBUD):
  sig, tpl, iw, rec, fst, pln, net, fin = hk_once()
  C = dict(NMAX=NMAX, HMASK=(1 << 17) - 1, M64=M64, ONES=ONES, INF=1 << 60, SPILL=SPILL, NTPL=len(tpl), EPSTEP=1 << 20, KBUD=kbud, NNET=len(net),
 RC0C=RC[0], RC1C=RC[1], RC2C=RC[2], RC3C=RC[3], RC4C=RC[4], OXOR=1, OAND=2, OOR=3, ONOT=4, OANDI=5, OSHL=6, OSHR=7, OINP=8, OMOVI=9, OPROBE=10,
 ILDI=11, ISTI=12, IADDI=13, ILD=14, IST=15, IBRNZ=17, IXOR=1, ISHRI=7, IMOVI=9, RP=0, RVB=1, RT1=2, RT2=3)
  sz, nr = dict.fromkeys('OPA AA BA IMA SGA FLA LVA RGA INA LSA ORD NAA NBA NDA SIGA'.split(), NMAX), len(rec) + 300
  sz.update(HTA=1 << 17, PROG=1 << 18, RES=nr, ROP=nr, RAC=nr, RBC=nr, RIM=nr)
  pos = 0
  for nm in list(sz) + 'FST PLN IWT FKY FSM NSY NAB NBB NEA VAL SYM NETA FM FCN BR1 BR2 WL RHT PIT T1 T2 MST LN X1 S0 SB DF R64 CX DX BQ BASE AS A0 C0 CN CPV DX2 OB FRE OCC NXR'.split():
   C[nm] = pos; pos += sz.get(nm, 1600)
  m = s.mem = [0] * pos
  s.C = C
  for n, (op, a, b, im, sg) in enumerate(tpl, 1):
   m[C['OPA'] + n], m[C['AA'] + n], m[C['BA'] + n], m[C['IMA'] + n], m[C['SGA'] + n] = op, a, b, im, sg
  m[C['SIGA'] + 1:C['SIGA'] + NMAX] = sig[:NMAX - 1]
  for j, (op, a, b, im) in enumerate(rec):
   m[C['ROP'] + j], m[C['RAC'] + j], m[C['RBC'] + j], m[C['RIM'] + j] = op, a, b, im
  for nm, vals in (('FST', fst), ('PLN', pln), ('IWT', iw)):
   m[C[nm]:C[nm] + len(vals)] = vals
  for mk, sym in fin.items():
   h = (mk ^ mk >> 10 ^ mk >> 20) & 1023
   while m[C['FKY'] + h]:
    h = h + 1 & 1023
   m[C['FKY'] + h], m[C['FSM'] + h] = mk, sym
  for e, (sym, a, b) in enumerate(net):
   m[C['NSY'] + e], m[C['NAB'] + e], m[C['NBB'] + e] = sym, a, b
  for b in range(30):
   for k in range(5):
    m[C['WL'] + 5 * b + k] = W40[b] >> 64 * k & M64
  for i in range(25):
   m[C['RHT'] + i], m[C['PIT'] + i] = RHO[i], i // 5 + 5 * ((2 * (i % 5) + 3 * (i // 5)) % 5)
  for x in range(5):
   m[C['T1'] + x], m[C['T2'] + x] = (x + 1) % 5, (x + 2) % 5
  for k in range(6):
   m[C['MST'] + k] = sum(1 << c for c in range(64) if not c & (32 >> k))
  m[C['LN'] + 16] = 0x86 << 56
  s.ns, s.over = compile_ram(GENSRC, C, bud)
  s.ns['mem'], s.ns['EPB'] = m, 1 << 20
 def gen(s, base):
  ns, m, C = s.ns, s.mem, s.C
  for k in range(5):
   m[C['BASE'] + k] = base >> 64 * k & M64
  ns['GC'] = 0
  try:
   return ns['gen'](), ns['GC']
  except Over:
   return None, ns['GC']
 def prog(s):
  m, C = s.mem, s.C
  out = []
  for p in range(C['PROG'], s.ns['CP'], 2):
   w, im = m[p], m[p + 1]
   out.append((w >> 18, w >> 12 & 63, w >> 6 & 63, w & 63, im))
  return out
def hk_exec(prog, mem, P, tag):
 R = [0] * 64
 R[0], R[1] = P, P + tag
 M = ONES
 for o, d, a, b, im in prog:
  if o == 1: R[d] = R[a] ^ R[b]
  elif o == 2: R[d] = R[a] & R[b]
  elif o == 3: R[d] = R[a] | R[b]
  elif o == 4: R[d] = R[a] ^ M
  elif o == 5: R[d] = R[a] & im
  elif o == 6: R[d] = R[a] << im & M
  elif o == 7: R[d] = R[a] >> im
  elif o == 9: R[d] = im
  elif o == 11: R[d] = mem[im]
  elif o == 12: mem[im] = R[a]
  elif o == 13: R[d] = R[a] + im & M
  elif o == 14: R[d] = mem.get(R[a], 1 << 255 | 12345)
  elif o == 15: mem[R[a]] = R[b]
  else: need(o == 17, 'opcode')
 return R
def keyword(t):
 L = keccak_f(lanes(t), 6)
 return sum(((L[x] >> z & 1) ^ (x == 0 and RC[5] >> z & 1)) << 4 * (z - 2) + x for z in range(2, 35) for x in range(4)) | 1 << 143
def pt40(t, i):
 g = i ^ i >> 1
 for b in range(40):
  if g >> b & 1:
   t ^= W40[b]
 return t
def survivor(t):
 L = keccak_f(lanes(t), 6)
 return all(L[x] & 3 == 0 for x in range(4))
def pearson(x, y):
 mx, my = sum(x) / len(x), sum(y) / len(y)
 sx, sy = sum((u - mx) ** 2 for u in x), sum((v - my) ** 2 for v in y)
 return sum((u - mx) * (v - my) for u, v in zip(x, y)) / (sx * sy) ** .5 if sx * sy else 0.0
HKN = 20
HKS = 10
def hk_list(seed):
 s = hashlib.shake_256(seed.encode()).digest(72)
 return int.from_bytes(s[:32], 'little') | (int.from_bytes(s[32:64], 'little') & M64) << 256, int.from_bytes(s[64:], 'little') % 1024
def hk_main(req):
 need(req['event'] == {'kind': 'full-collision'}, 'event')
 need(sha3_256(message(0)).hex() == KAT[0][1], 'known answer')
 hk = HK()
 mem, tag, res = {}, 0xABCDEF123456789 << 128, []
 for j in range(HKN):
  t, I = hk_list(req['trials'][j]['seed'])
  base = pt40(t, I << 30)
  kk, gn = hk.gen(base)
  ov = kk is None or kk > KBUD or gn > GENBUD
  if not ov:
   prog, rng = hk.prog(), random.Random(j)
   lo = rng.sample(range(1 << 30), 256)
   P = (1 << 30) + 256 * j
   for c in range(256):
    mem[P + c] = lo[c]
   hk_exec(prog, mem, P, tag)
   bad = sum(mem.get(keyword(pt40(base, lo[c]))) != tag + P + c for c in range(256))
   need(bad == 0, 'every table word of the generated program is the tag plus the slot')
  res.append((ov, kk or 0, gn, sum(survivor(pt40(base, i)) for i in range(1 << HKS))))
 Os, Ks, Gs, Ss = ([r[i] for r in res] for i in range(4))
 med = sorted(Ss)[HKN // 2]
 lo_, hi_ = sum(o for o, s in zip(Os, Ss) if s < med), sum(o for o, s in zip(Os, Ss) if s >= med)
 need(lo_ + hi_ == 0, 'no list over budget, in either stratum of the survivor count')
 rK, rG = pearson(Ks, Ss), pearson(Gs, Ss)
 need(abs(rK) < .7 and abs(rG) < .7, 'correlation of K and of the generation with the survivor count below 0.7')
 obs = dict(lists=HKN, over_low=lo_, over_high=hi_, k_min=min(Ks), k_max=max(Ks), gen_min=min(Gs), gen_max=max(Gs), surv_min=min(Ss), surv_max=max(Ss),
 corr_k_x1000=round(1000 * rK), corr_gen_x1000=round(1000 * rG), lists_surv_below_median=sum(s < med for s in Ss))
 out = [{'trial': t['trial'], 'message_a_hex': None, 'message_b_hex': None, 'observations': dict(obs, k=Ks[i], gen=Gs[i], surv=Ss[i]) if i < HKN else {}}
 for i, t in enumerate(req['trials'])]
 sys.stdout.write(json.dumps({'schema_version': 1, 'trials': out}, separators=(',', ':')))

def main():
 req = json.loads(sys.stdin.read())
 eid = req.get('experiment_id')
 if eid == 'hk-kernel':
  return hk_main(req)
 need(eid in MODES and req.get('event') == MODES[eid][1], 'experiment id and its event')
 setup_checks()
 trials = req['trials']
 out = []
 for g in range(0, len(trials), LANES):
  grp = trials[g:g + LANES]
  seeds = [t['seed'] for t in grp] + [grp[0]['seed'] + '/%d' % c for c in range(len(grp), LANES)]
  obs, pairs_out = run_group(int(grp[0]['seed'], 16) % G, seeds, MODES[eid][0])
  for c, t in enumerate(grp):
   a, b = pairs_out[c] or (None, None)
   out.append({'trial': t['trial'], 'message_a_hex': a, 'message_b_hex': b, 'observations': dict(obs[c])})
 sys.stdout.write(json.dumps({'schema_version': 1, 'trials': out}, separators=(',', ':')))
if __name__ == '__main__':
 main()
