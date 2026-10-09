"""v22 experiments (proof.md). PASS = (00^135, 01||00^134), FAIL = (00^135, 02||00^134)."""
import hashlib
import json
import math
import sys
import collections
import itertools
from fractions import Fraction
N = 1600
MASK = (1 << N) - 1
M64 = (1 << 64) - 1
RHO = (0,1,62,28,27,36,44,6,55,20,3,10,43,25,39,41,45,15,21,8,18,2,61,56,14)
RCS = (0x1,0x8082,0x800000000000808A,0x8000000080008000,0x808B)
def rot(v, a):
 a %= 64
 return ((v << a) | (v >> (64 - a))) & M64 if a else v
def lanes(s):
 return [(s >> (64 * i)) & M64 for i in range(25)]
def unlanes(A):
 s = 0
 for i, v in enumerate(A):
  s |= v << (64 * i)
 return s
def Lmap(s):
 A = lanes(s)
 P = [A[x] ^ A[x + 5] ^ A[x + 10] ^ A[x + 15] ^ A[x + 20] for x in range(5)]
 T = [P[(x - 1) % 5] ^ rot(P[(x + 1) % 5], 1) for x in range(5)]
 B = [0] * 25
 for y in range(5):
  for x in range(5):
   i = x + 5 * y
   B[y + 5 * ((2 * x + 3 * y) % 5)] = rot(A[i] ^ T[x], RHO[i])
 return unlanes(B)
def chi(s):
 A = lanes(s)
 O = [0] * 25
 for y in range(5):
  for x in range(5):
   O[x + 5 * y] = A[x + 5 * y] ^ ((~A[(x + 1) % 5 + 5 * y]) & A[(x + 2) % 5 + 5 * y] & M64)
 return unlanes(O)
def rnd(s, r):
 return chi(Lmap(s)) ^ RCS[r]
def par(v):
 return bin(v).count("1") & 1
def chi5(v):
 o = 0
 for i in range(5):
  o |= (((v >> i) & 1) ^ ((1 ^ ((v >> ((i + 1) % 5)) & 1)) & ((v >> ((i + 2) % 5)) & 1))) << i
 return o
CHI5 = [chi5(v) for v in range(32)]
DDT = [[0] * 32 for _ in range(32)]
for _d in range(32):
 for _v in range(32):
  DDT[_d][CHI5[_v] ^ CHI5[_v ^ _d]] += 1
ROWS = [(y, z) for y in range(5) for z in range(64)]
def rowbits(y, z):
 return [64 * (x + 5 * y) + z for x in range(5)]
def getrow(s, y, z):
 return sum(((s >> (64 * (x + 5 * y) + z)) & 1) << x for x in range(5))
def _affine_subsets():
 lin = {0: {(0,)}}
 for k in range(1, 6):
  lin[k] = set()
  for S in lin[k - 1]:
   Sset = set(S)
   for v in range(1, 32):
    if v not in Sset:
     lin[k].add(tuple(sorted(Sset | {s ^ v for s in Sset})))
 out = {}
 for k in range(6):
  aff = set()
  for S in lin[k]:
   for b in range(32):
    aff.add(tuple(sorted(s ^ b for s in S)))
  out[k] = sorted(list(W) for W in aff)
 return out
AFFL = _affine_subsets()
VSET = {(d, o): frozenset(v for v in range(32) if CHI5[v] ^ CHI5[v ^ d] == o)
  for d in range(32) for o in range(32) if DDT[d][o]}
COMPAT = {o: [d for d in range(32) if DDT[d][o]] for o in range(32)}
AFFIN = {o: {k: [W for W in AFFL[k] if set(W) <= set(COMPAT[o])] for k in (0, 1, 2)} for o in range(1, 32)}
_ANN = {}
def annih(W):
 key = tuple(sorted(W))
 r = _ANN.get(key)
 if r is not None:
  return r
 base = key[0]
 dirs = [w ^ base for w in key]
 out = []
 for m in range(1, 32):
  if all(par(m & u) == 0 for u in dirs):
   mm = m
   for q in sorted(out, reverse=True):
    if mm ^ q < mm:
     mm ^= q
   if mm:
    out.append(mm)
 r = [(m, par(m & base)) for m in out]
 _ANN[key] = r
 return r
def row_forms(W, rb):
 fl = []
 for (m, c) in annih(W):
  f = c << N
  for x in range(5):
   if (m >> x) & 1:
    f |= 1 << rb[x]
  fl.append(f)
 return fl
class CapExceeded(Exception):
 pass
class Ech:
 def __init__(s, budget=None):
  s.piv = {}
  s.log = []
  s.budget = budget if budget is not None else [0, 1 << 62]
 def reduce(s, f):
  piv = s.piv
  bud = s.budget
  bud[0] += 1
  if bud[0] > bud[1]:
   raise CapExceeded()
  while True:
   low = f & MASK
   if not low:
    return f
   r = piv.get(low.bit_length() - 1)
   if r is None:
    return f
   f ^= r
   bud[0] += 1
   if bud[0] > bud[1]:
    raise CapExceeded()
 def add(s, f):
  f = s.reduce(f)
  if not (f & MASK):
   return -1 if f else 0
  p = (f & MASK).bit_length() - 1
  s.piv[p] = f
  s.log.append(p)
  return 1
 def mark(s):
  return len(s.log)
 def undo(s, m):
  while len(s.log) > m:
   del s.piv[s.log.pop()]
 def rank(s):
  return len(s.piv)
def linear_rows(fn):
 rows = [0] * N
 for i in range(N):
  c = fn(1 << i)
  while c:
   lb = c & -c
   rows[lb.bit_length() - 1] |= 1 << i
   c ^= lb
 return rows
def Linv_map(s):
 B = lanes(s)
 A = [0] * 25
 for y in range(5):
  for x in range(5):
   i = x + 5 * y
   A[i] = rot(B[y + 5 * ((2 * x + 3 * y) % 5)], 64 - RHO[i])
 return _theta_inv(unlanes(A))
def _theta_inv_setup():
 def T(p):
  P = [(p >> (64 * x)) & M64 for x in range(5)]
  return sum((P[(x - 1) % 5] ^ rot(P[(x + 1) % 5], 1)) << (64 * x) for x in range(5))
 n = 320
 rows = [0] * n
 for i in range(n):
  c = (1 << i) ^ T(1 << i)
  for j in range(n):
   if (c >> j) & 1:
    rows[j] |= 1 << i
 aug = [(rows[j], 1 << j) for j in range(n)]
 A = [a for a, _ in aug]
 Bm = [b for _, b in aug]
 for col in range(n):
  p = next(k for k in range(col, n) if (A[k] >> col) & 1)
  A[col], A[p] = A[p], A[col]
  Bm[col], Bm[p] = Bm[p], Bm[col]
  for k in range(n):
   if k != col and (A[k] >> col) & 1:
    A[k] ^= A[col]
    Bm[k] ^= Bm[col]
 return T, Bm
_T, _IPT_ROWS = _theta_inv_setup()
def _theta_inv(b):
 Lb = lanes(b)
 P = sum((Lb[x] ^ Lb[x + 5] ^ Lb[x + 10] ^ Lb[x + 15] ^ Lb[x + 20]) << (64 * x) for x in range(5))
 Q = 0
 for j in range(320):
  if par(_IPT_ROWS[j] & P):
   Q |= 1 << j
 E = _T(Q)
 El = [(E >> (64 * x)) & M64 for x in range(5)]
 return unlanes([Lb[i] ^ El[i % 5] for i in range(25)])
def linv_rows():
 rows = [0] * N
 for o in range(N):
  lane, z = divmod(o, 64)
  x = lane % 5
  m = _IPT_ROWS[64 * ((x - 1) % 5) + z] ^ _IPT_ROWS[64 * ((x + 1) % 5) + (z - 1) % 64]
  A = lanes((m | (m << 320) | (m << 640) | (m << 960) | (m << 1280)) ^ (1 << o))
  B = [0] * 25
  for yy in range(5):
   for xx in range(5):
    i = xx + 5 * yy
    B[yy + 5 * ((2 * xx + 3 * yy) % 5)] = rot(A[i], RHO[i])
  rows[o] = unlanes(B)
 return rows
BETA2 = unlanes([0x1,0,0x4,0,0,0x4,0x4,0x4,0x20000,0,0x2000000000000000,0,0x200000,0,0,
    0x2000000000000000,0,0,0x20000,0,0x200001,0,0x200000,0,0x1])
ALPHA3_BITS = (0,130,450,529,701,789,1021,1169,1280,1429)
class BudgetExceeded(Exception):
 pass
class _WKMeta(type):
 def __setattr__(cls, k, v):
  type.__setattr__(cls, k, v)
  if cls.cap is not None and cls.cost() > cls.cap or cls.tcap is not None and cls.cost() + cls.d > cls.tcap:
   raise BudgetExceeded()
class WK(metaclass=_WKMeta):
 row = 0
 small = 0
 keccak = 0
 sha256 = 0
 r2 = 0
 cap = tcap = None
 d = 0
 @staticmethod
 def snap():
  return (WK.row, WK.small, WK.keccak, WK.sha256, WK.r2)
 @staticmethod
 def cost(s=None):
  r, sm, k, h, r2 = s or WK.snap()
  return 256 * r + 8 * sm + 1355 * (5 * k + 2 * h + r2)
def sha256(b):
 WK.sha256 += (len(b) + 9 + 63) // 64
 return hashlib.sha256(b).digest()
class Coins:
 def __init__(s, seed):
  s.seed, s.k, s.buf, s.pos, s.draws = seed, 0, b"", 0, 0
 def word(s):
  if s.pos >= len(s.buf):
   s.buf = hashlib.shake_256(s.seed + s.k.to_bytes(4, "little")).digest(4096)
   WK.keccak += 31
   s.k += 1
   s.pos = 0
  w = int.from_bytes(s.buf[s.pos:s.pos + 32], "little")
  s.pos += 32
  s.draws += 1
  WK.small += 4
  return w
 def perm(s, a):
  for i in range(len(a) - 1, 0, -1):
   j = (s.word() & M64) % (i + 1)
   a[i], a[j] = a[j], a[i]
   WK.small += 4
def run_seed(label, i):
 return hashlib.sha256(label + i.to_bytes(8, "little")).digest()
class Base:
 def __init__(s, a3b=ALPHA3_BITS, b2=BETA2):
  for k in range(6):
   for Wl in AFFL[k]:
    annih(Wl)
  WK.small += 2451 * 2048
  s.Lrow = linear_rows(Lmap)
  s.Linv = linv_rows()
  WK.row += 2 * N * 30
  s.FIX = list(range(1080, N))
  s.fixval = {j: 0 for j in s.FIX}
  for k in range(8):
   s.fixval[1080 + k] = (0x86 >> k) & 1
  s.beta2 = b2
  s.alpha2 = Linv_map(b2)
  a3 = 0
  for b in a3b:
   a3 |= 1 << b
  s.alpha3 = a3
  s.a2rows = [(y, z, getrow(s.alpha2, y, z)) for (y, z) in ROWS if getrow(s.alpha2, y, z)]
  assert len(s.a2rows) == 59
  s.e_rows = [(y, z, VSET[(getrow(s.beta2, y, z), getrow(s.alpha3, y, z))])
     for (y, z) in ROWS if getrow(s.beta2, y, z)]
KW, MW, LB, PREF = 1.0, 1.0, 1.0, 1.0
def rand_min_beta1(base, coins):
 b = 0
 for (y, z, o2) in base.a2rows:
  best = max(DDT[d][o2] for d in range(32))
  opts = [d for d in range(32) if DDT[d][o2] == best]
  coins.perm(opts)
  d = opts[0]
  rb = rowbits(y, z)
  for x in range(5):
   if (d >> x) & 1:
    b |= 1 << rb[x]
  WK.small += 64
 return b
class Cand:
 def __init__(s, base, beta1):
  s.base = base
  s.Lrow, s.Linv, s.FIX, s.fixval = base.Lrow, base.Linv, base.FIX, base.fixval
  s.alpha2 = base.alpha2
  s.beta2, s.alpha3, s.e_rows = base.beta2, base.alpha3, base.e_rows
  s.beta1 = beta1
  alpha1 = Linv_map(beta1)
  WK.row += 64
  s.a1rows = {(y, z): getrow(alpha1, y, z) for (y, z) in ROWS}
  s.act = [(y, z) for (y, z) in ROWS if s.a1rows[(y, z)]]
  conds = []
  for (y, z, o2) in base.a2rows:
   d1 = getrow(beta1, y, z)
   rb = rowbits(y, z)
   for (m, c) in annih(VSET[(d1, o2)]):
    ym = 0
    for x in range(5):
     if (m >> x) & 1:
      ym ^= s.Lrow[rb[x]]
      WK.row += 1
    conds.append((ym, c ^ par(ym & RCS[0])))
  s.rowmasks, s.condparts = {}, []
  for (ym, c) in conds:
   parts = {}
   v = ym
   while v:
    lb = v & -v
    i = lb.bit_length() - 1
    v ^= lb
    lane, z = divmod(i, 64)
    parts[(lane // 5, z)] = parts.get((lane // 5, z), 0) | (1 << (lane % 5))
    WK.small += 8
   s.condparts.append((parts, c))
   for r, m in parts.items():
    s.rowmasks.setdefault(r, set()).add(m)
  s.lin_rows = [r for r in ROWS if r in s.rowmasks]
  s.lin = {}
  full = frozenset(range(32))
  for r in s.lin_rows:
   masks = tuple(sorted(s.rowmasks[r]))
   o = s.a1rows[r]
   Ss = [VSET[(d, o)] for d in COMPAT[o]] if o else [full]
   for S in Ss:
    s.lin[(r, S)] = s._lin_options(S, masks)
 def _is_aff(s, Wl, masks):
  Wl = sorted(Wl)
  b = Wl[0]
  for m in masks:
   for u in Wl:
    for w in Wl:
     WK.small += 8
     if par(m & (CHI5[u ^ w ^ b] ^ CHI5[u] ^ CHI5[w] ^ CHI5[b])):
      return False
  return True
 def _lin_options(s, S, masks):
  if s._is_aff(S, masks):
   return (S, None)
  for k in range(len(S).bit_length() - 2, -1, -1):
   opts = []
   for Wl in AFFL[k]:
    WK.small += 8
    if set(Wl) <= S and s._is_aff(Wl, masks):
     opts.append(frozenset(Wl))
   if opts:
    return (None, opts)
  return (None, [])
class Aff:
 __slots__ = ("T", "rank")
 def __init__(s, T, rank=0):
  s.T, s.rank = T, rank
 def copy(s):
  WK.row += len(s.T)
  WK.d -= len(s.T) * (253 - 2 * ((len(s.T) + 256) // 256))
  return Aff(list(s.T), s.rank)
 def add(s, idx, c):
  T = s.T
  a = 0
  for j in idx:
   a ^= T[j]
  WK.row += len(idx) + 1
  coef = a >> 1
  if not coef:
   return 0 if (a & 1) == c else -1
  pb = (coef & -coef) << 1
  af = a ^ c
  s.T = [t ^ af if t & pb else t for t in T]
  WK.row += 2 * len(T)
  WK.d += 4 * ((len(T) + 256) // 256) * sum(1 for t in T if t & pb) - 505 * len(T)
  s.rank += 1
  return 1
PARMW = {}
def parmw(n):
 if n not in PARMW:
  tab = []
  for lam in range(1 << n):
   m0 = m1 = 0
   for v in range(1 << n):
    if par(lam & v):
     m1 |= 1 << v
    else:
     m0 |= 1 << v
   tab.append((m0, m1))
  PARMW[n] = tab
  WK.small += (1 << n) * (1 << n)
 return PARMW[n]
def projn(T, cs):
 n = len(cs)
 tab = parmw(n)
 piv = []
 mask = (1 << (1 << n)) - 1
 for i in range(n):
  t_ = T[cs[i]]
  cf, k, cb = t_ >> 1, t_ & 1, 1 << i
  WK.row += 2
  for (pc, pk, pcb, lb) in piv:
   WK.row += 1
   if cf & lb:
    cf ^= pc
    k ^= pk
    cb ^= pcb
    WK.row += 1
  if cf:
   piv.append((cf, k, cb, cf & -cf))
   WK.row += 1
  else:
   mask &= tab[cb][k]
   WK.row += 1
 return mask
def form_idx(f):
 idx = []
 v = f & MASK
 while v:
  lb = v & -v
  idx.append(lb.bit_length() - 1)
  v ^= lb
 WK.row += len(idx) + 1
 return idx, (f >> N) & 1
WT = [0] * 32
for _d in range(1, 32):
 WT[_d] = 5 - (max(DDT[_d]).bit_length() - 1)
def base_D(t):
 D = Aff([1 << (j + 1) for j in range(N)])
 for j in t.FIX:
  idx, _ = form_idx(t.Linv[j])
  assert D.add(idx, 0) >= 0
 for r in ROWS:
  if t.a1rows[r] == 0:
   for b in rowbits(*r):
    assert D.add([b], 0) >= 0
 return D
def own_bits():
 out = []
 for b in range(N):
  Bl = lanes(1 << b)
  A = [0] * 25
  for y in range(5):
   for x in range(5):
    i = x + 5 * y
    A[i] = rot(Bl[y + 5 * ((2 * x + 3 * y) % 5)], 64 - RHO[i])
  out.append(unlanes(A).bit_length() - 1)
  WK.small += 200
 return out
def link_constants(t):
 X = Aff([1 << (j + 1) for j in range(N)])
 for j in t.FIX:
  idx, _ = form_idx(t.Linv[j])
  assert X.add(idx, t.fixval[j]) >= 0
 return X
def build_links(t, OB):
 X0 = link_constants(t)
 fs = set(t.FIX)
 colfix = collections.defaultdict(list)
 for r in ROWS:
  rb = rowbits(*r)
  for i in range(5):
   a = OB[rb[i]]
   if a in fs:
    lane, z = divmod(a, 64)
    colfix[(lane % 5, z)].append((r, i, rb[i]))
 links = []
 for key in sorted(colfix):
  v = colfix[key]
  if len(v) == 2:
   (r1, i1, b1), (r2, i2, b2) = v
   a = X0.T[b1] ^ X0.T[b2]
   WK.row += 1
   assert (a >> 1) == 0
   links.append((r1, i1, b1, r2, i2, b2, a & 1))
 ports = collections.defaultdict(list)
 for (r1, i1, b1, r2, i2, b2, c) in links:
  ports[r1].append(i1)
  ports[r2].append(i2)
 return links, {r: sorted(v) for r, v in ports.items()}
def fixed_combos(S, P):
 out = {}
 for m in range(1, 1 << len(P)):
  vals = set()
  for v in sorted(S):
   vals.add(sum((v >> P[k]) & 1 for k in range(len(P)) if (m >> k) & 1) & 1)
   WK.small += 4
  if len(vals) == 1:
   out[m] = vals.pop()
 return out
def combo_basis(ms):
 basis = []
 for m in sorted(ms):
  v = m
  for b in basis:
   if v ^ b < v:
    v ^= b
  if v:
   basis.append(m)
 return basis
def uniform_info(Wd, o, P):
 fcs = [fixed_combos(VSET[(d, o)], P) for d in Wd]
 if len(set(tuple(sorted(f)) for f in fcs)) != 1:
  return None
 ms = combo_basis(list(fcs[0]))
 a0 = Wd[0]
 dirs = [d ^ a0 for d in Wd[1:]]
 out = []
 for m in ms:
  tgt = [fcs[i][m] ^ fcs[0][m] for i in range(1, len(Wd))]
  lam = None
  for L in range(32):
   WK.small += 4
   if all(par(L & dirs[i]) == tgt[i] for i in range(len(dirs))):
    lam = L
    break
  if lam is None:
   return None
  out.append((m, lam, fcs[0][m] ^ par(lam & a0)))
 return out
class PortSys:
 __slots__ = ("piv",)
 def __init__(s):
  s.piv = {}
 def copy(s):
  p = PortSys()
  p.piv = dict(s.piv)
  WK.row += len(s.piv)
  return p
 def add(s, lhs, rhs):
  piv = s.piv
  while lhs:
   p = lhs.bit_length() - 1
   e = piv.get(p)
   WK.row += 2
   if e is None:
    piv[p] = (lhs, rhs)
    return None
   lhs ^= e[0]
   rhs ^= e[1]
  return rhs
def make_cost(t):
 out = {}
 for r in t.act:
  o = t.a1rows[r]
  for d in COMPAT[o]:
   S = VSET[(d, o)]
   lc = 0
   if r in t.rowmasks:
    Wl, best = t.lin[(r, S)]
    if Wl is None:
     k = max((len(x) for x in best), default=1)
     lc = (len(S).bit_length() - 1) - (k.bit_length() - 1)
   out[(r, d)] = WT[d] + lc
   WK.small += 8
 return out
def d2u_cands(t, ports):
 cands = {}
 for r in t.act:
  o = t.a1rows[r]
  P = ports.get(r, [])
  cl = []
  for k in (2, 1, 0):
   for Wd in AFFIN[o][k]:
    ui = uniform_info(Wd, o, P)
    if ui is not None:
     cl.append((k, Wd, ui))
  cands[r] = cl
 return cands
def d2u(t, D, ports, links, cands, COST, coins):
 linkof = collections.defaultdict(list)
 for L in links:
  linkof[L[0]].append(L)
  linkof[L[3]].append(L)
 PS = PortSys()
 un = list(t.act)
 coins.perm(un)
 A = {}
 rb_of = {r: rowbits(*r) for r in t.act}
 added_links = set()
 def viable(Dv, r):
  m = projn(Dv.T, rb_of[r])
  WK.small += 4 * len(cands[r])
  return [c for c in cands[r] if any((m >> d) & 1 for d in c[1])]
 dom = {r: viable(D, r) for r in un}
 nlinkc = 0
 while un:
  WK.small += 2 * len(un)
  r = min(un, key=lambda q: (len(dom[q]) > 0, len(dom[q])))
  if not dom[r]:
   return None, D, len(A), nlinkc
  cl = list(dom[r])
  coins.perm(cl)
  cl.sort(key=lambda c: (2 - c[0]) * KW + PREF * (min(COST[(r, d)] for d in c[1]) + MW * sum(COST[(r, d)] for d in c[1]) / len(c[1])) - LB * len(c[2]))
  WK.small += 16 * len(cl)
  un.remove(r)
  chosen = None
  for (k, Wd, ui) in cl:
   D2 = D.copy()
   PS2 = PS.copy()
   rb = rb_of[r]
   good = True
   for m, c in annih(Wd):
    if D2.add([rb[x] for x in range(5) if (m >> x) & 1], c) < 0:
     good = False
     break
   if not good:
    continue
   P = ports.get(r, [])
   newc = 0
   for (m, lam, c0) in ui:
    lhs = 0
    for kk in range(len(P)):
     if (m >> kk) & 1:
      lhs |= 1 << rb[P[kk]]
    rhs = c0 << N
    for x in range(5):
     if (lam >> x) & 1:
      rhs ^= 1 << rb[x]
    WK.row += 4
    res = PS2.add(lhs, rhs)
    if res is not None:
     idx, cc = form_idx(res)
     if D2.add(idx, cc) < 0:
      good = False
      break
     newc += 1
   if not good:
    continue
   for L in linkof[r]:
    key = (L[2], L[5])
    if key in added_links:
     continue
    res = PS2.add((1 << L[2]) | (1 << L[5]), L[6] << N)
    if res is not None:
     idx, cc = form_idx(res)
     if D2.add(idx, cc) < 0:
      good = False
      break
     newc += 1
   if not good:
    continue
   nd = {}
   dead = False
   for q in un:
    rq = rb_of[q]
    WK.row += 5
    if all(D2.T[j] is D.T[j] for j in rq):
     nd[q] = dom[q]
     continue
    v = viable(D2, q)
    if not v:
     dead = True
     break
    nd[q] = v
   if dead:
    continue
   chosen = (Wd, D2, PS2, nd, newc)
   break
  if chosen is None:
   return None, D, len(A), nlinkc
  Wd, D, PS, dom, newc = chosen
  nlinkc += newc
  for L in linkof[r]:
   added_links.add((L[2], L[5]))
  A[r] = Wd
 return A, D, len(A), nlinkc
def mask_basis(masks):
 out = []
 for m in sorted(masks):
  v = m
  for b in out:
   if v ^ b < v:
    v ^= b
  if v:
   out.append(m)
 return out
def express(m, basis):
 n = len(basis)
 for c in range(1 << n):
  v = 0
  for i in range(n):
   if (c >> i) & 1:
    v ^= basis[i]
  if v == m:
   return c
 raise ValueError
class Model:
 def __init__(s, t):
  s.t = t
  s.mb, s.ucoord = {}, {}
  nxt = N
  for r in ROWS:
   ms = sorted(t.rowmasks.get(r, ()))
   b = mask_basis(ms)
   s.mb[r] = b
   s.ucoord[r] = list(range(nxt, nxt + len(b)))
   nxt += len(b)
  s.NC = nxt
  s.conds = []
  for (parts, c) in t.condparts:
   idx = set()
   for r, m in sorted(parts.items()):
    co = express(m, s.mb[r])
    for i in range(len(s.mb[r])):
     if (co >> i) & 1:
      idx ^= {s.ucoord[r][i]}
    WK.small += 64
   s.conds.append((sorted(idx), c))
  s.cands = {}
  full = frozenset(range(32))
  for r in ROWS:
   o = t.a1rows[r]
   ds = COMPAT[o] if o else [0]
   lst = []
   for d in ds:
    S = VSET[(d, o)] if o else full
    if r in t.rowmasks:
     Wl, best = t.lin[(r, S)]
     Ws = [Wl] if Wl is not None else list(best)
    else:
     Ws = [S]
    for Wl in Ws:
     lst.append(s._cand(r, d, frozenset(Wl)))
   s.cands[r] = lst
  s.coords = {r: rowbits(*r) + s.ucoord[r] for r in ROWS}
 def _cand(s, r, d, Wl):
  b = s.mb[r]
  k = len(b)
  g = 0
  for x in sorted(Wl):
   u = 0
   for i in range(k):
    u |= par(b[i] & CHI5[x]) << i
   g |= 1 << (x | (u << 5))
  rb = rowbits(*r)
  eqs = []
  for m, c in annih(Wl):
   eqs.append(([rb[x] for x in range(5) if (m >> x) & 1], c))
  Ws = sorted(Wl)
  b0 = Ws[0]
  ech = []
  for w in Ws:
   v = w ^ b0
   for (pp, ee) in ech:
    if (v >> pp) & 1:
     v ^= ee
   if v:
    pp = v.bit_length() - 1
    ech = [(q, e ^ v if (e >> pp) & 1 else e) for (q, e) in ech]
    ech.append((pp, v))
  for i in range(k):
   m = b[i]
   idx = [s.ucoord[r][i]]
   c = par(m & CHI5[b0])
   for (pp, e) in ech:
    if par(m & (CHI5[b0 ^ e] ^ CHI5[b0])):
     idx.append(rb[pp])
     c ^= (b0 >> pp) & 1
   eqs.append((idx, c))
  WK.small += 512
  return (d, Wl, g, eqs, 5 - (len(Wl).bit_length() - 1))
def base_X(t, M):
 X = Aff([1 << (j + 1) for j in range(M.NC)])
 for j in t.FIX:
  idx, _ = form_idx(t.Linv[j])
  assert X.add(idx, t.fixval[j]) >= 0
 for idx, c in M.conds:
  if X.add(idx, c) < 0:
   return None
 return X
def dom_of(M, X, D, r, Ar):
 ax = projn(X.T, M.coords[r])
 ad = projn(D.T, rowbits(*r))
 WK.small += 4 * len(M.cands[r])
 return [c for c in M.cands[r] if c[0] in Ar and (ad >> c[0]) & 1 and (c[2] & ax)]
def m2(M, X, D, A, coins):
 un = list(ROWS)
 coins.perm(un)
 Afull = {r: (set(A[r]) if r in A else {0}) for r in ROWS}
 dom = {r: dom_of(M, X, D, r, Afull[r]) for r in un}
 choice = {}
 while un:
  WK.small += 2 * len(un)
  r = min(un, key=lambda q: len(dom[q]))
  if not dom[r]:
   return None, choice, X, D
  cl = list(dom[r])
  coins.perm(cl)
  cl.sort(key=lambda c: c[4])
  un.remove(r)
  chosen = None
  rb = rowbits(*r)
  tent = []
  for c in cl:
   d, Wl, g, eqs, cost = c
   X2, D2 = X.copy(), D.copy()
   good = True
   for x in range(5):
    if D2.add([rb[x]], (d >> x) & 1) < 0:
     good = False
     break
   if good:
    for idx, cc in eqs:
     if X2.add(idx, cc) < 0:
      good = False
      break
   if good:
    tent.append((X2.rank - X.rank, len(tent), c, X2, D2))
  tent.sort(key=lambda z: (z[0], z[1]))
  for (_, _, c, X2, D2) in tent:
   nd = {}
   dead = False
   for q in un:
    cs = M.coords[q]
    WK.row += len(cs) + 5
    if all(X2.T[j] is X.T[j] for j in cs) and all(D2.T[j] is D.T[j] for j in rowbits(*q)):
     nd[q] = dom[q]
     continue
    v = dom_of(M, X2, D2, q, Afull[q])
    if not v:
     dead = True
     break
    nd[q] = v
   if dead:
    continue
   chosen = (c, X2, D2, nd)
   break
  if chosen is None:
   return None, choice, X, D
  c, X, D, dom = chosen
  choice[r] = c
 return True, choice, X, D
def point(X, coins):
 T = X.T
 live = 0
 for v in T[:N]:
  live |= v
 live >>= 1
 pv = 0
 i = 0
 while live >> i:
  if (live >> i) & 1 and coins.word() & 1:
   pv |= 1 << i
  i += 1
 x = 0
 for j in range(N):
  v = T[j]
  if (v & 1) ^ par((v >> 1) & pv):
   x |= 1 << j
 WK.row += 3 * N
 return x
def verify(t, X, beta0, coins, npts=64):
 alpha0 = Linv_map(beta0)
 good = 0
 for _ in range(npts):
  x = point(X, coins)
  A1, A2 = Linv_map(x), Linv_map(x ^ beta0)
  WK.row += 2 * 64
  ok = (A1 ^ A2 == alpha0) and A1 != A2
  ok = ok and all(((A1 >> j) & 1) == t.fixval[j] for j in t.FIX) and all(((A2 >> j) & 1) == t.fixval[j] for j in t.FIX)
  WK.r2 += 2
  ok = ok and (rnd(rnd(A1, 0), 1) ^ rnd(rnd(A2, 0), 1)) == t.alpha2
  good += ok
 return good
class CandSetup:
 def __init__(s, base, OB, label, c):
  s.c = c
  s.beta1 = rand_min_beta1(base, Coins(sha256(label + b"beta1" + c.to_bytes(4, "little"))))
  s.t = Cand(base, s.beta1)
  s.COST = make_cost(s.t)
  s.M = Model(s.t)
  s.X0 = base_X(s.t, s.M)
  s.D0 = base_D(s.t)
  s.links, s.ports = build_links(s.t, OB)
  s.cands = d2u_cands(s.t, s.ports)
def b_attempt(cs, label, j, dmin):
 coins = Coins(sha256(label + b"att" + cs.c.to_bytes(4, "little") + j.to_bytes(4, "little")))
 if cs.X0 is None:
  return {"st": "r1inc"}, None
 A, D, na, nlc = d2u(cs.t, cs.D0.copy(), cs.ports, cs.links, cs.cands, cs.COST, coins)
 if A is None:
  return {"st": "d2u", "rows": na}, None
 ok, ch, X, D2 = m2(cs.M, cs.X0.copy(), D, A, coins)
 if not ok:
  return {"st": "m2", "rows": len(ch), "nlc": nlc}, None
 DF = cs.M.NC - X.rank
 beta0 = 0
 for r, cc in ch.items():
  rb = rowbits(*r)
  for x in range(5):
   if (cc[0] >> x) & 1:
    beta0 |= 1 << rb[x]
 res = {"st": "ok" if DF >= dmin else "lowdf", "DF": DF, "nlc": nlc,
  "sumwt": sum(WT[cc[0]] for cc in ch.values()), "cost": sum(cc[4] for cc in ch.values())}
 if DF >= dmin:
  res["verified"] = verify(cs.t, X, beta0, coins)
  if res["verified"] != 64:
   res["st"] = "verifyfail"
 return res, beta0
B_R, B_DMIN = 1 << 62, 33
B_BUDGET, CCAP, B_TRUE = 1355 << 32, 1355 << 26, 1355 << 29
def bprime(base, OB, label, budget=B_BUDGET, log=None, c=0, ccap=CCAP, tb=None):
 top = WK.cost() + budget
 WK.tcap = None if tb is None else WK.cost() + WK.d + tb
 try:
  while True:
   WK.cap = min(top, WK.cost() + ccap)
   s0 = WK.snap()
   try:
    cs = CandSetup(base, OB, label, c)
    if log:
     log("cand", c, -1, {"st": "r1inc" if cs.X0 is None else "setup"}, s0)
    for j in range(B_R):
     s1 = WK.snap()
     res, b0 = b_attempt(cs, label, j, B_DMIN)
     if log:
      log("att", c, j, res, s1)
     if res["st"] == "ok":
      return cs.beta1, b0, c, j, res["DF"]
   except BudgetExceeded:
    if WK.cap == top or WK.tcap is not None and WK.cost() + WK.d > WK.tcap:
     raise
   c += 1
 except BudgetExceeded:
  return None
 finally:
  WK.cap = WK.tcap = None
def Setup(base, beta1, beta0):
 st = Cand(base, beta1)
 st.ref = beta0
 return st
X_MAX = 1 << 20
def attempt(st, coins, dmin=33, xor_cap=X_MAX):
 budget = [0, xor_cap]
 try:
  status, info = _attempt(st, coins, dmin, budget)
 except CapExceeded:
  status, info = "cap", None
 info = dict(info or {})
 info["xors"] = budget[0]
 info["draws"] = coins.draws
 return status, info
def _attempt(st, coins, dmin, budget):
 rows_a1 = st.a1rows
 ref = st.ref
 Linv = st.Linv
 ED = Ech(budget)
 for j in st.FIX:
  if ED.add(Linv[j]) < 0:
   return "dinc", None
 for (y, z) in ROWS:
  if rows_a1[(y, z)] == 0:
   for b in rowbits(y, z):
    if ED.add(1 << b) < 0:
     return "dinc", None
 order = list(st.act)
 coins.perm(order)
 A2sel = {}
 for (y, z) in order:
  o = rows_a1[(y, z)]
  rb = rowbits(y, z)
  rv = getrow(ref, y, z)
  sel = None
  for k in (2, 1, 0):
   cands = list(AFFIN[o][k])
   coins.perm(cands)
   cands = [W for W in cands if rv in W]
   for W in cands:
    mk = ED.mark()
    good = True
    for f in row_forms(W, rb):
     if ED.add(f) < 0:
      good = False
      break
    if good:
     sel = W
     break
    ED.undo(mk)
   if sel is not None:
    break
  if sel is None:
   return "dinc", None
  A2sel[(y, z)] = sel
 EM = Ech(budget)
 for j in st.FIX:
  if EM.add(Linv[j] | (st.fixval[j] << N)) < 0:
   return "minc", None
 beta0 = 0
 Srow = {}
 for (y, z) in order:
  o = rows_a1[(y, z)]
  rb = rowbits(y, z)
  rv = getrow(ref, y, z)
  cands = list(A2sel[(y, z)])
  coins.perm(cands)
  cands.sort(key=lambda d: -DDT[d][o])
  cands.sort(key=lambda d: d != rv)
  ok = False
  for d in cands:
   md, mm = ED.mark(), EM.mark()
   good = True
   for x in range(5):
    if ED.add(1 << rb[x] | (((d >> x) & 1) << N)) < 0:
     good = False
     break
   if good:
    for f in row_forms(VSET[(d, o)], rb):
     if EM.add(f) < 0:
      good = False
      break
   if good:
    ok = True
    Srow[(y, z)] = VSET[(d, o)]
    for x in range(5):
     if (d >> x) & 1:
      beta0 |= 1 << rb[x]
    break
   ED.undo(md)
   EM.undo(mm)
  if not ok:
   return "tda", None
 aff = {}
 full = frozenset(range(32))
 for r in st.lin_rows:
  y, z = r
  rb = rowbits(y, z)
  masks = tuple(sorted(st.rowmasks[r]))
  W, best = st.lin[(r, Srow.get(r, full))]
  if W is None:
   best = list(best)
   coins.perm(best)
   forms = {Wo: row_forms(Wo, rb) for Wo in best}
   implied = [Wo for Wo in best if all(EM.reduce(f) == 0 for f in forms[Wo])]
   if implied:
    W = implied[0]
   else:
    for Wo in best:
     mk = EM.mark()
     good = True
     for f in forms[Wo]:
      if EM.add(f) < 0:
       good = False
       break
     if good:
      W = Wo
      break
     EM.undo(mk)
    if W is None:
     return "lin", None
  Ws = sorted(W)
  b = Ws[0]
  ech = []
  for w in Ws:
   v = w ^ b
   for (pp, ee) in ech:
    if (v >> pp) & 1:
     v ^= ee
   if v:
    pp = v.bit_length() - 1
    ech = [(q, e ^ v if (e >> pp) & 1 else e) for (q, e) in ech]
    ech.append((pp, v))
  for m in masks:
   f = par(m & CHI5[b]) << N
   for (pp, e) in ech:
    if par(m & (CHI5[b ^ e] ^ CHI5[b])):
     f ^= (1 << rb[pp]) ^ (((b >> pp) & 1) << N)
   aff[(r, m)] = f
 for (parts, c) in st.condparts:
  f = c << N
  for r, m in parts.items():
   f ^= aff[(r, m)]
  if EM.add(f) < 0:
   return "cond", None
 DF = N - EM.rank()
 if DF < dmin:
  return "lowdf", {"DF": DF}
 return "ok", {"EM": EM, "beta0": beta0, "DF": DF}
def solve(EM, xfree):
 piv = EM.piv
 xv = xfree
 for p in sorted(piv):
  f = piv[p]
  if par(f & ((1 << p) - 1) & xv) ^ ((f >> N) & 1):
   xv |= 1 << p
 return xv
def enum_basis(EM, beta0, nb=32):
 free = [i for i in range(N) if i not in EM.piv]
 v0 = solve(EM, 0)
 piv = {}
 def addv(w):
  v = w
  while v:
   p = v.bit_length() - 1
   if p in piv:
    v ^= piv[p]
   else:
    piv[p] = v
    return True
  return False
 addv(beta0)
 basis = []
 for i in free:
  if len(basis) == nb:
   break
  b = solve(EM, 1 << i) ^ v0
  if addv(b):
   basis.append(b)
 return v0, basis
def digest5(A0):
 s = A0
 for r in range(5):
  s = rnd(s, r)
 return s & ((1 << 256) - 1)
def message(A0):
 return (A0 & ((1 << 1080) - 1)).to_bytes(135, "little")
def e_window(st, v0, basis, beta0, lo, count, s2cap=None):
 passes = 0
 out = None
 for c in range(lo, lo + count):
  x = v0
  for j in range(len(basis)):
   if (c >> j) & 1:
    x ^= basis[j]
  u = Lmap(chi(Lmap(chi(x) ^ RCS[0])) ^ RCS[1])
  if all(getrow(u, y, z) in V for (y, z, V) in st.e_rows):
   passes += 1
   if s2cap is not None and passes > s2cap:
    break
   A, B = Linv_map(x), Linv_map(x ^ beta0)
   if out is None and digest5(A) == digest5(B):
    out = (c, message(A), message(B))
 return passes, out
SENTINEL = (bytes(135), b"\x01" + bytes(134))
STATUS = {"ok": 0, "dinc": 1, "minc": 2, "tda": 3, "lin": 4, "cond": 5, "lowdf": 6, "cap": 7}
def kernel(s):
 L=lanes(s)
 return all((L[x]^L[x+5]^L[x+10]^L[x+15]^L[x+20])==0 for x in range(5))
def active_rows(s):
 return [(y,z,getrow(s,y,z)) for (y,z) in ROWS if getrow(s,y,z)]
def wt(d,o):
 return 5-(DDT[d][o].bit_length()-1)
def facts(st):
 ok=[]
 a3=st.alpha3
 b3=Lmap(a3)
 ok.append(kernel(a3) and kernel(b3) and bin(b3).count("1")==10)
 a2=st.alpha2
 r2=active_rows(a2)
 w1=sum(min(wt(d,o) for d in COMPAT[o]) for (_,_,o) in r2)
 ok.append(len(r2)==59 and w1==127)
 rb2=active_rows(st.beta2)
 ok.append([(y,z) for (y,z,_) in rb2]==[(y,z) for (y,z,_) in active_rows(a3)])
 ok.append(all(DDT[d][getrow(a3,y,z)] for (y,z,d) in rb2))
 ok.append(sum(wt(d,getrow(a3,y,z)) for (y,z,d) in rb2)==24)
 c2=1
 for (_,_,o) in active_rows(a3):
  c2 *= len(COMPAT[o])
 ok.append(c2==3486784401)
 M320=(1<<320)-1
 opts=[]
 for (y,z,d) in active_rows(b3):
  ol=[]
  for o in range(32):
   if DDT[d][o]:
    s=0
    for x in range(5):
     if (o>>x)&1:
      s |= 1<<(64*(x+5*y)+z)
    ol.append((Lmap(s)&M320,DDT[d][o]))
  opts.append(ol)
 def combos(group):
  out=[(0,1)]
  for ol in group:
   out=[(v^w,p*q) for (v,p) in out for (w,q) in ol]
  return out
 ga,gb=combos(opts[:5]),combos(opts[5:])
 pz=[DDT[d][0]+DDT[d][16] for d in range(32)]
 p45=Fraction(0)
 nz=0
 for (va,pa) in ga:
  for (vb,pb) in gb:
   v=va^vb
   l4=(v>>256)&M64
   if ((v|(v>>64)|(v>>128)|(v>>192))&M64)&~l4:
    continue
   num,den=pa*pb,32 ** len(opts)
   for z in range(64):
    if (l4>>z)&1:
     num *= pz[sum(((v>>(64*x+z))&1)<<x for x in range(5))]
     den *= 32
   if num:
    nz += 1
    p45 += Fraction(num,den)
 ok.append(len(ga)*len(gb)==1<<19 and nz==192 and p45==Fraction(55,1<<19))
 b1,b0=st.beta1,st.ref
 ok.append([(y,z) for (y,z,_) in active_rows(b1)]==[(y,z) for (y,z,_) in r2])
 ok.append(all(DDT[getrow(b1,y,z)][o] for (y,z,o) in r2)
   and sum(wt(getrow(b1,y,z),o) for (y,z,o) in r2)==127)
 alpha1=Linv_map(b1)
 ok.append(len(active_rows(alpha1))==len(st.act))
 ok.append(all(DDT[getrow(b0,y,z)][getrow(alpha1,y,z)] for (y,z) in ROWS))
 a0=Linv_map(b0)
 ok.append(a0!=0 and all(((a0>>j)&1)==0 for j in st.FIX))
 ok.append(len(st.e_rows)==10)
 good_linv=True
 for k in range(16):
  sv=int.from_bytes(hashlib.shake_256(b"linv"+bytes([k])).digest(200),"little")
  img=Linv_map(sv)
  good_linv=good_linv and all(par(st.Linv[j]&sv)==(img>>j)&1 for j in range(N))
 ok.append(good_linv)
 return all(ok),ok
def verify_space(st,info,coins):
 EM,beta0=info["EM"],info["beta0"]
 alpha0=Linv_map(beta0)
 for _ in range(2):
  xv=0
  for i in range(N):
   if i not in EM.piv and coins.word()&1:
    xv |= 1<<i
  x=solve(EM,xv)
  A,B=Linv_map(x),Linv_map(x^beta0)
  if A^B!=alpha0:
   return False
  for S in (A,B):
   if any(((S>>j)&1)!=st.fixval[j] for j in st.FIX):
    return False
  if A==B:
   return False
  if rnd(rnd(A,0),1)^rnd(rnd(B,0),1)!=st.alpha2:
   return False
 return True
K_SPACES, A_ADV, A_MAX, S2CAP = 50, 1067, 4268, 1 << 11
WINDOW = 1 << 12
FAIL_PAIR = (bytes(135), b"\x02" + bytes(134))
B2L = lanes(BETA2)
RC0, RC1 = 0x1, 0x8082
ONES = (1 << 256) - 1
NOUT = [sum(1 for o in range(32) if DDT[d][o]) for d in range(32)]
NIN = [sum(1 for d in range(32) if DDT[d][o]) for o in range(32)]
ALLOW = sum(1 << q for q in range(32) if DDT[q][0] + DDT[q][16])
def L(A):
 P = [A[x] ^ A[x + 5] ^ A[x + 10] ^ A[x + 15] ^ A[x + 20] for x in range(5)]
 T = [P[(x - 1) % 5] ^ rot(P[(x + 1) % 5], 1) for x in range(5)]
 B = [0] * 25
 for y in range(5):
  for x in range(5):
   B[y + 5 * ((2 * x + 3 * y) % 5)] = rot(A[x + 5 * y] ^ T[x], RHO[x + 5 * y])
 return B
def chiL(A):
 return [A[x+5*y]^(~A[(x+1)%5+5*y]&A[(x+2)%5+5*y]) for y in range(5) for x in range(5)]
def fwd(i):
 lane, z = i >> 6, i & 63
 x, y = lane % 5, lane // 5
 return 64 * (y + 5 * ((2 * x + 3 * y) % 5)) + ((z + RHO[lane]) & 63)
FWD = [fwd(i) for i in range(1600)]
BWD = [0] * 1600
for _i in range(1600):
 BWD[FWD[_i]] = _i
COLA = [((i >> 6) % 5) * 64 + (i & 63) for i in range(1600)]
COLB = [((FWD[i] >> 6) % 5) * 64 + (FWD[i] & 63) for i in range(1600)]
def canon(b):
 return min(tuple(sorted(64 * (i >> 6) + (((i & 63) - t) & 63) for i in b)) for t in range(64))
def lane_dfs(lane, kmax=10):
 cA, cB, cur, found, nodes = [0] * 320, [0] * 320, [], set(), [0]
 def dfs():
  nodes[0] += 1
  ca = min((COLA[i] for i in cur if cA[COLA[i]] & 1), default=-1)
  cb = -1 if ca >= 0 else min((COLB[i] for i in cur if cB[COLB[i]] & 1), default=-1)
  if ca < 0 and cb < 0:
   found.add(canon(cur))
   return
  if len(cur) >= kmax:
   return
  c = ca if ca >= 0 else cb
  for y in range(5):
   i = 64 * (c // 64 + 5 * y) + c % 64
   if ca < 0:
    i = BWD[i]
   if i in cur:
    continue
   cur.append(i)
   cA[COLA[i]] += 1
   cB[COLB[i]] += 1
   dfs()
   cur.pop()
   cA[COLA[i]] -= 1
   cB[COLB[i]] -= 1
 cur.append(64 * lane)
 cA[COLA[64 * lane]] += 1
 cB[COLB[64 * lane]] += 1
 dfs()
 return nodes[0], found
def rows_of(bits):
 r = {}
 for b in bits:
  r[((b >> 6) // 5, b & 63)] = r.get(((b >> 6) // 5, b & 63), 0) | (1 << ((b >> 6) % 5))
 return sorted(r.items())
def p45pos(core):
 opts, sup = [], []
 for (y, z), d in rows_of([FWD[b] for b in core]):
  ol, s = [], 0
  for o in range(32):
   if DDT[d][o]:
    A = [0] * 25
    for x in range(5):
     if (o >> x) & 1:
      A[x + 5 * y] |= 1 << z
    v = L(A)[:5]
    ol.append(v)
    s |= v[0] | v[1] | v[2] | v[3] | v[4]
  opts.append(ol)
  sup.append(s)
 n = len(opts)
 rest = [0] * (n + 1)
 for k in range(n - 1, -1, -1):
  rest[k] = rest[k + 1] | sup[k]
 def ok(v, z):
  while z:
   p = (z & -z).bit_length() - 1
   z &= z - 1
   if not (ALLOW >> sum(((v[x] >> p) & 1) << x for x in range(5))) & 1:
    return False
  return True
 dead = set()
 def dfs(k, v):
  if k == n:
   return True
  key = (k,) + tuple(w & rest[k] for w in v)
  if key in dead:
   return False
  fin = sup[k] & ~rest[k + 1]
  for w in opts[k]:
   u = [v[x] ^ w[x] for x in range(5)]
   if ok(u, fin) and dfs(k + 1, u):
    return True
  dead.add(key)
  return False
 return dfs(0, [0] * 5)
LANE_NODES = [345923,346741,347335,347245,346861,346213,348343,346483,347031,348147,347363,346239,
   346119,346755,347715,346837,347449,346491,346881,346221,346885,347921,346649,347657,347329]
GROUPS = [(0,1),(2,3,4,5,6,7),tuple(range(8,17)),tuple(range(17,25))]
GROUP_LOG = [(692664,1023,974737408,204,608900651514,21466134),(2082480,646,600711168,251,735420810384,
      25918866),(3123655,72,63639552,12,34953937452,1207224),(2776034,0,0,0,0,0)]
def trail_group(g):
 nodes,reach,lanes_ok=0,set(),True
 for lane in GROUPS[g]:
  n,f=lane_dfs(lane)
  lanes_ok=lanes_ok and n==LANE_NODES[lane]
  nodes += n
  reach |= f
 own=[c for c in reach if min(b>>6 for b in c) in GROUPS[g]]
 c1=sum(math.prod(NOUT[d] for _,d in rows_of([FWD[b] for b in c])) for c in own)
 kept=[c for c in own if p45pos(c)]
 ms=[[NIN[o] for _,o in rows_of(c)] for c in kept]
 hv=sum(min(math.prod(m[:k])+math.prod(m[k:]) for k in range(1,len(m))) for m in ms)
 got=(nodes,len(own),c1,len(kept),sum(math.prod(m) for m in ms),hv)
 return lanes_ok and got==GROUP_LOG[g],dict(zip(("nodes","cores","sum_c1","kept","sum_c2","half_vectors"),got))
OPS = [0]
class W(int):
 pass
def _op(f):
 def g(a, b=None):
  OPS[0] += 1
  return W(f(int(a)) if b is None else f(int(a), int(b)))
 return g
for _n, _f in (("xor", int.__xor__), ("and", int.__and__), ("or", int.__or__), ("lshift", lambda a, b: a << b & ONES),
   ("rshift", int.__rshift__), ("add", int.__add__), ("sub", int.__sub__)):
 setattr(W, "__%s__" % _n, _op(_f))
W.__invert__ = _op(lambda a: a ^ ONES)
def load(v):
 OPS[0] += 1
 return W(v)
def st():
 OPS[0] += 1
def test(c):
 OPS[0] += 2
 return c
def gstep(H,base,T,w2=None):
 f,G=H
 j=load(f[0])
 st()
 f[0]=0
 if test(j == len(G)):
  return None
 g=load(G[j])
 n=load(T[0][g])
 st()
 G[j]=int(n)
 if w2 is not None:
  w2=w2 + load(T[2][g])
 for i,d in enumerate(T[1][g]):
  base[i]=base[i] ^ load(d)
  if w2 is not None:
   st()
 if w2 is not None:
  st()
  W(0) + 23
 if test(n < g):
  k=j + 1
  f[j]=int(load(f[int(k)]))
  st()
  f[int(k)]=int(k)
  st()
 return True if w2 is None else w2
def gtab(R,wt=None):
 T,G=([],[],[]),[]
 for j,V in enumerate(R):
  m,o=len(V),len(T[0])
  G.append(o)
  for s in range(2 * m - 2):
   a,e=(s // 2,1) if s % 2 == 0 else (m - 1 - s // 2,-1)
   b=a + e
   T[0].append(o + ((2 * b if b < m - 1 else 1) if e > 0 else (2 * (m - 1 - b) + 1 if b else 0)))
   T[1].append([W(x ^ y) for x,y in zip(V[a],V[b])])
   if wt:
    T[2].append(W(wt[j][b] - wt[j][a]))
 return T,[list(range(len(R) + 1)),G]
def gpos(G,G0,ms):
 return [(s // 2) if s % 2 == 0 else m - 1 - s // 2 for s,m in zip([g - o for g,o in zip(G,G0)],ms)]
def gray_init(ms):
 n=len(ms)
 return [list(range(n+1)),[0]*n,[1]*n,ms,None]
EQS = [(1,2,8,1),(1,2,16,1),(1,2,3,0),(1,2,5,1),(1,17,4,1),(1,17,16,0),(0,0,2,0),
 (0,0,16,1),(0,2,2,1),(0,2,8,0),(2,21,2,1),(2,21,8,0),(2,61,2,0),(2,61,16,1),
 (3,17,4,1),(3,17,16,0),(3,61,2,0),(3,61,16,1),(4,0,2,1),(4,0,8,1),(4,0,17,0),
 (4,21,2,0),(4,21,8,0),(4,21,16,1)]
CERT_A = bytes.fromhex(
 "596c1eb8c532269112fb3a27efabf03448de94ffc28d41fe76deb6d001dcb72cdd90391bfe9962ccd17deffd3a2368d37a6ff7cb4b"
 "17963f9fee9d0652da52bd155d5f257573acd09933fd445dfdc411d659b6c4f7dbe37637289f4ee2dd1116a959c18fad016ec5b4"
 "5031f6100c30e2dd08f5e007e2494b7c7ec6552f452e0c16273ef8b5a121")
def eqs_ok():
 a3=[0]*25
 for b in ALPHA3_BITS:
  a3[b>>6] |= 1<<(b&63)
 good=True
 for (y,z),d in rows_of([64*i+z for i in range(25) for z in range(64) if (B2L[i]>>z)&1]):
  o=sum(((a3[x+5*y]>>z)&1)<<x for x in range(5))
  V=[v for v in range(32) if CHI5[v]^CHI5[v^d]==o]
  E=[(m,c) for (yy,zz,m,c) in EQS if (yy,zz)==(y,z)]
  sat=[v for v in range(32) if all(bin(m&v).count("1")%2==c for (m,c) in E)]
  good=good and len(V)==DDT[d][o] and sat==V
 return good and len(EQS)==24
def e_plain(x):
 A=[(x>>(64*i))&M64 for i in range(25)]
 a=chiL(A)
 a[0] ^= 1
 b=chiL(L(a))
 b[0] ^= 0x8082
 u=L(b)
 return [int(bin(m&sum(((u[xx+5*y]>>z)&1)<<xx for xx in range(5))).count("1")%2==c)
     for (y,z,m,c) in EQS]
CN = [[math.comb(n, k) for k in range(5)] for n in range(24)]
def gray(i):
 return i^(i>>1)
def fes_setup(v0,basis,no=24):
 nv,val=8+no,{}
 pts=[sum(1<<b for b in cb) for w in range(5) for cb in itertools.combinations(range(nv),w)]
 for S in pts:
  x=v0
  for j in range(nv):
   if (S>>j)&1:
    x ^= basis[j]
  val[S]=sum((1-r)<<k for k,r in enumerate(e_plain(x)))
 G={}
 for S in pts:
  cf,T=0,S
  while True:
   cf ^= val[T]
   if T==0:
    break
   T=(T-1)&S
  g=G.setdefault(S>>8,[0]*24)
  for k in range(24):
   if (cf>>k)&1:
    g[k] ^= sum(1<<l for l in range(256) if l&S&255==S&255)
 def deriv(K,y):
  out=list(G.get(K,[0]*24))
  fr=[b for b in range(no) if (y>>b)&1 and not (K>>b)&1]
  for e in range(1,5-bin(K).count("1")):
   for cb in itertools.combinations(fr,e):
    out=[p^q for p,q in zip(out,G.get(K|sum(1<<b for b in cb),[0]*24))]
  return out
 D=[{},{},{},{},{}]
 for w in range(1,5):
  for cb in itertools.combinations(range(no),w):
   K=sum(1<<b for b in cb)
   D[w][sum(CN[b][i+1] for i,b in enumerate(cb))]=deriv(K,gray(K-1) if w < 4 else 0)
 return deriv(0,0),D
def ctz(low):
 lo,hi=0,24
 while hi - lo > 1:
  mid=(lo + hi) // 2
  if test(low >= (1 << mid)):
   lo=mid
  else:
   hi=mid
 W(lo) ^ 0
 return lo
def pro(t):
 t=load(t)
 test(t + 256 == 1 << 24)
 st()
 for _ in range(4):
  if test(t == 0):
   break
  low=t & (W(0) - t)
  ctz(low)
  t=t ^ low
 for _ in range(16):
  load(0) + 0
  st()
def fes_step(i,f,D):
 i=i + 1
 b,t,o=[],i,OPS[0]
 while len(b) < 4 and t:
  b.append((t & -t).bit_length() - 1)
  t &= t - 1
 if not i & 255:
  pro(i)
 po,d=OPS[0] - o,len(b)
 rk=[sum(CN[b[v]][v + 1] for v in range(w + 1)) for w in range(d)]
 for p in b:
  if p > 7:
   load(0) + 0
 if sum(p > 7 for p in b) > 3:
  st()
  load(0)
 g=b[0] == 0
 h=g and d > 1 and b[1] == 1
 for k in range(24):
  x=None
  for w in range(d - 1,0,-1):
   r=w < 2 and g or w == 2 and h and k < 11
   if x is None:
    x=(W if d == 2 and h and k < 11 else load)(D[w + 1][rk[w]][k])
   x=x ^ (W if r else load)(D[w][rk[w - 1]][k])
   if not r:
    st()
   D[w][rk[w - 1]][k]=int(x)
  f[k]=f[k] ^ (x if x is not None else (W if g else load)(D[1][rk[0]][k]))
 acc=f[0]
 for k in range(1,24):
  acc=acc | f[k]
 test(acc != ONES)
 return i,int(acc) ^ ONES,po,sum(p > 7 for p in b),d
def e_ops(i,dy,d):
 v=((0,2,5,8,11),(0,1,3,6,9))[i & 1][d]
 return 25 + 2 * dy + 2 * (dy > 3) + 24 * v - (11 * (d - 1) if d < 3 else 22) * (i & 3 == 3)
def e_block(seed):
 D=[None] + [collections.defaultdict(lambda: [0] * 24) for _ in range(4)]
 f,i,s,mx=[W(0)] * 24,256 * (h64(seed) % (1 << 16) | 15) - 1,0,0
 for r in range(256):
  OPS[0]=0
  i,_,po,dy,d=fes_step(i,f,D)
  s += OPS[0] - po
 for b in range(1,1 << 16):
  OPS[0]=0
  pro(256 * b)
  mx=max(mx,OPS[0])
 return s == E_STEPS and mx == E_PRO,{"block_steps": s,"pro_max": mx}
def fes_trial(seed,no=9):
 s=hashlib.shake_256(seed).digest(200*33)
 basis=[int.from_bytes(s[200*i:200*i+200],"little") for i in range(32)]
 p=s[-1]
 v0=sum(w<<(64*i) for i,w in enumerate(L([int.from_bytes((CERT_A+b"\x86"+bytes(65))[8*i:8*i+8],"little") for i in range(25)])))
 for j in range(8):
  if (p>>j)&1:
   v0 ^= basis[j]
 f,D=fes_setup(v0,basis,no)
 f=[W(w) for w in f]
 ok,worst,i,ps=True,0,0,0
 for step in range(1<<no):
  if step:
   OPS[0]=0
   i,ps,po,dy,d=fes_step(i,f,D)
   ok=ok and OPS[0]-po==e_ops(step,dy,d) and po<=E_PRO
   worst=max(worst,po)
  else:
   for w in f:
    ps |= int(w)
   ps ^= ONES
   ok=(ps>>p)&1==1
  y=gray(step)
  for q in ((p,77,200) if step==0 else (step*37%256,)):
   x=v0
   for j in range(8+no):
    if (((y<<8)|q)>>j)&1:
     x ^= basis[j]
   r=e_plain(x)
   ok=ok and all(((f[k]>>q)&1)==1-r[k] for k in range(24)) and ((ps>>q)&1)==int(all(r))
 return ok and worst > 0,{"pro_max": worst}
E_PRO, E_STEPS = 117, 66714
def linv(A):
 B = [rot(A[y + 5 * ((2 * x + 3 * y) % 5)], 64 - RHO[x + 5 * y]) for y in range(5) for x in range(5)]
 Q = [B[x] ^ B[x + 5] ^ B[x + 10] ^ B[x + 15] ^ B[x + 20] for x in range(5)]
 for _ in range(191):
  Q = [Q[x] ^ Q[(x - 1) % 5] ^ rot(Q[(x + 1) % 5], 1) for x in range(5)]
 return sum((B[i] ^ Q[(i - 1) % 5] ^ rot(Q[(i + 1) % 5], 1)) << (64 * i) for i in range(25))
def one_row(y, z, v):
 A = [0] * 25
 for x in range(5):
  A[x + 5 * y] |= ((v >> x) & 1) << z
 return A
def gray_walk(ms,steps):
 H=gray_init(ms)
 for _ in range(steps):
  j=H[0][0]
  H[0][0]=0
  if j==len(ms):
   break
  H[1][j] += H[2][j]
  if H[1][j] in (0,ms[j]-1):
   H[2][j]=-H[2][j]
   H[0][j]=H[0][j+1]
   H[0][j+1]=j+1
 return H
CACHE = {}
def core_tables(bits):
 if bits not in CACHE:
  rows = rows_of(bits)
  ins = [[d for d in range(32) if DDT[d][o]] for (_, o) in rows]
  LI = []
  for ((y, z), _) in rows:
   u = [linv(one_row(y, z, 1 << x)) for x in range(5)]
   LI.append([0] * 32)
   for d in range(1, 32):
    LI[-1][d] = LI[-1][d & (d - 1)] ^ u[(d & -d).bit_length() - 1]
  CACHE[bits] = rows, ins, LI
 return CACHE[bits]
def t2_leaf(base):
 w,v=base
 u=w ^ (w ^ v) & (w << 128)
 g=u | u << 64
 if test(g < 1 << 192):
  st()
 return int(g) < 1 << 192
DUP = 1 << 128 | 1 << 192
def t2_trial(seed):
 h=hashlib.sha256(seed).digest()
 rows=rows_of([FWD[b] for b in ALPHA3_BITS])
 outs=[[o for o in range(32) if DDT[d][o]] for (_,d) in rows]
 def pl(A,c=0):
  v=L(A)
  return [v[2]|v[3]<<64|v[0]<<128|v[1]<<192,(v[4]^c)*DUP]
 def alpha4(a):
  A=[0]*25
  for j,aj in enumerate(a):
   (y,z),_=rows[j]
   B=one_row(y,z,outs[j][aj])
   A=[A[i]^B[i] for i in range(25)]
  return A
 ms=[len(o) for o in outs]
 K=gray_walk(ms,int.from_bytes(h[:3],"little")%20000)
 T,H=gtab([[pl(one_row(y,z,d)) for d in outs[j]] for j,((y,z),_) in enumerate(rows)])
 G0=list(H[1])
 H=[K[0],[g+(2*a if o > 0 else 2*(m-1-a)+1) for g,a,o,m in zip(G0,K[1],K[2],ms)]]
 base=[W(w) for w in pl(alpha4(K[1]),M64)]
 ok,worst=all(t2_leaf([W(sum((q>>x&1)*M64<<64*((x+2)%4) for x in range(4))),W(M64*(1-(q>>4&1))*DUP)])==ALLOW>>q&1 for q in range(32)),0
 for _ in range(64):
  v=L(alpha4(gpos(H[1],G0,ms)))[:5]
  plain=all((ALLOW>>sum(((v[x]>>z)&1)<<x for x in range(5)))&1 for z in range(64))
  OPS[0]=0
  kept=t2_leaf(base)
  gstep(H,base,T)
  worst=max(worst,OPS[0])
  ok=ok and kept==plain and [int(w) for w in base]==pl(alpha4(gpos(H[1],G0,ms)),M64) and OPS[0]<=T2_LEAF
 return ok,{"ops_max": worst}
T2_LEAF = 26
M_CAP = 1 << 24
NBL = (1,2,4,8,16,32,64)
class CapReached(Exception):
 pass
MINW = [min(5 - (DDT[d][o].bit_length() - 1) for d in range(32) if DDT[d][o]) if o else 0 for o in range(32)]
BLK = [((r % 64) + 13 * (r // 64)) % 64 for r in range(320)]
POS = [0] * 320
for _t in range(64):
 for _i, _r in enumerate([r for r in range(320) if BLK[r] == _t]):
  POS[_r] = 25 * _t + 5 * _i
FM = sum(1 << 5 * r for r in range(320))
def rowmaj(s):
 return sum(getrow(s, r // 64, r % 64) << POS[r] for r in range(320))
def halves(bits):
 rows, ins, LI = core_tables(bits)
 ms, n = [len(v) for v in ins], len(ins)
 h = min(range(1, n), key=lambda k: (math.prod(ms[:k]) + math.prod(ms[k:]), k))
 vec = [[rowmaj(LI[j][d]) for d in ins[j]] for j in range(n)]
 out = []
 for lo, hi in ((0, h), (h, n)):
  V, W2, CH = [], [], []
  for cb in itertools.product(*[range(ms[j]) for j in range(hi - 1, lo - 1, -1)]):
   cb = cb[::-1]
   v, w = 0, 0
   for j, i in zip(range(lo, hi), cb):
    v ^= vec[j][i]
    w += 5 - (DDT[ins[j][i]][rows[j][1]].bit_length() - 1)
   V.append(v)
   W2.append(w)
   CH.append(cb)
  out.append((V, W2, CH))
 return out
BR = {nb: [[POS[r] for r in range(320) if BLK[r] % nb == t] for t in range(nb)] for nb in NBL}
def mkey(v, nb, t):
 if nb == 64:
  return (v >> 25 * t) & 0x1FFFFFF
 k, p = 0, 0
 for q in BR[nb][t]:
   c = (v >> q) & 31
   k ^= (c << p) & 0x3FFFFFF
   if p > 21:
    k ^= c >> (26 - p)
   p = p + 5 - (26 if p >= 21 else 0)
 return k
def mitm_core(H, nb, M, mcap):
 (VA, WA, CA), (VB, WB, CB) = H
 best, f = None, 0
 for t in range(nb):
  D = {}
  for i, v in enumerate(VB):
   D.setdefault(mkey(v, nb, t), []).append(i)
  for a, v in enumerate(VA):
   for b in D.get(mkey(v, nb, t), ()):
    M[0] += 1
    if M[0] > mcap:
     raise CapReached()
    x = v ^ VB[b]
    if ((x | x >> 1 | x >> 2 | x >> 3 | x >> 4) & FM).bit_count() < nb:
     f += 1
     c = (sum(MINW[(x >> 5 * r) & 31] for r in range(320)), WA[a] + WB[b], CA[a] + CB[b])
     best = c if best is None or c < best else best
 return best, f
def trail_search(mcap=M_CAP, cores=None):
 if cores is None:
  reach = set()
  for lane in range(25):
   reach |= lane_dfs(lane)[1]
  cores = [c for c in sorted(reach) if p45pos(c)]
 M, bl = [0], {nb: None for nb in NBL}
 for c in cores:
  H = halves(c)
  CACHE.clear()
  for nb in NBL:
   r, _ = mitm_core(H, nb, M, mcap)
   if r and (bl[nb] is None or (r[0], r[1]) < bl[nb][0][:2]):
    bl[nb] = (r, c)
  del H
 for nb in NBL:
  if bl[nb] and bl[nb][0][0] < 2 * nb:
   r, c = bl[nb]
   rows, ins, _ = core_tables(c)
   b2 = 0
   for ((y, z), _), v, i in zip(rows, ins, r[2]):
    for x in range(5):
     b2 |= ((v[i] >> x) & 1) << (64 * (x + 5 * y) + z)
   return (c, b2, r[0], r[1]), M[0]
 return None, M[0]
def algorithm(label):
 try:
  tr, _ = trail_search()
 except CapReached:
  return None
 if tr is None:
  return None
 base, OB = Base(tr[0], tr[1]), own_bits()
 left, tl, c, att = B_BUDGET, B_TRUE, 0, 0
 while att < A_MAX:
  h, g = WK.cost(), WK.cost() + WK.d
  r = bprime(base, OB, label, left, None, c, CCAP, tl)
  if r is None:
   return None
  left -= WK.cost() - h
  tl -= WK.cost() + WK.d - g
  c = r[2] + 1
  st = Setup(base, r[0], r[1])
  spaces = []
  for i in range(A_ADV):
   att += 1
   status, info = attempt(st, Coins(run_seed(label + b"conn" + c.to_bytes(4, "little"), i)))
   if status == "ok":
    spaces.append(info)
   if len(spaces) == K_SPACES or att == A_MAX:
    break
  if len(spaces) == K_SPACES:
   for info in spaces:
    v0, basis = enum_basis(info["EM"], info["beta0"], 32)
    _, out = e_window(st, v0, basis, info["beta0"], 0, 1 << 32, S2CAP)
    if out:
     return out[1:]
   return None
 return None
def to_planes(v):
 w=[0]*7
 for r in range(320):
  for x in range(5):
   if v>>POS[r]+x&1:
    w[x if r < 256 else 5+x//4] |= 1<<(r if r < 256 else 64*(x%4)+r-256)
 return w
KOFF = {nb: sum(n for n in NBL if n < nb) for nb in NBL}
def keywords(v):
 kw=[0]*15
 for nb in NBL:
  for t in range(nb):
   q=KOFF[nb]+t
   kw[q//9] |= mkey(v,nb,t)<<26*(q%9)
 return kw
SW = [sum(c << 8 * i for i in range(32)) for c in (0x55, 0x33, 0x0F)]
HM = sum(255 << 16 * i for i in range(16))
S1 = SW[1] & M64
UNR = 16
def per_a(A,e,M,mcap):
 a=[load(w) for w in A]
 e=W(e) - 0
 M[0]=M[0] + e
 if test(M[0] > mcap):
  raise CapReached()
 q=e & UNR - 1
 p=W(0) + q
 load(0)
 test(q)
 test(e < UNR)
 return a,q,p,e
def match_run(A,R,nb,M,mcap):
 a,q,p,e=per_a(A,len(R),M,mcap)
 out=[match_step(a,R[i],nb) for i in range(q)]
 while e >= UNR:
  out += [match_step(a,R[int(p) + k],nb) for k in range(UNR)]
  p=p + UNR
  if test(p >= e):
   break
 return out
def match_step(a,B,nb):
 load(0)
 x=[a[i] ^ load(B[i]) for i in range(7)]
 h=x[0] | x[1] | x[2] | x[3] | x[4]
 t=x[5] | (x[5] >> 128)
 t=(t | (t >> 64)) | x[6]
 h,t=h - ((h >> 1) & SW[0]),t - ((t >> 1) & SW[0])
 c=(h & SW[1]) + ((h >> 2) & SW[1]) + (t & S1) + ((t >> 2) & S1)
 c=(c & SW[2]) + ((c >> 4) & SW[2])
 c=(c + (c >> 8)) & HM
 for s in (16,32,64,128):
  c=c + (c << s)
 return test(c < nb << 240),int(c) >> 240
HV_STEP, MATCH_STEP, PER_A = 83, 56, 18
def hv_trial():
 c=ALPHA3_BITS
 rows,ins,LI=core_tables(c)
 ms=[len(v) for v in ins]
 h=min(range(1,10),key=lambda k: (math.prod(ms[:k])+math.prod(ms[k:]),k))
 ok,mx,n=True,0,0
 for (lo,hi),(V,W2,CH) in zip(((0,h),(h,10)),halves(c)):
  R=range(lo,hi)
  vs=[[to_planes(rowmaj(LI[j][x]))+keywords(rowmaj(LI[j][x])) for x in ins[j]] for j in R]
  T,G=gtab(vs,[[5-(DDT[d][rows[j][1]].bit_length()-1) for d in ins[j]] for j in R])
  G0=list(G[1])
  v0=0
  for j in R:
   v0 ^= rowmaj(LI[j][ins[j][0]])
  vec,w2=[W(w) for w in to_planes(v0)+keywords(v0)],W(sum(5-(DDT[ins[j][0]][rows[j][1]].bit_length()-1) for j in R))
  idx={ch: i for i,ch in enumerate(CH)}
  while True:
   OPS[0]=0
   w2=gstep(G,vec,T,w2)
   if w2 is None:
    break
   mx,n=max(mx,OPS[0]),n+1
   if n%4099==1:
    i=idx[tuple(gpos(G[1],G0,ms[lo:hi]))]
    ok=ok and [int(w) for w in vec]==to_planes(V[i])+keywords(V[i]) and int(w2)==W2[i]
 return ok and mx==HV_STEP and n==2*(9 ** 5-1),{"steps": n,"ops_max": mx}
def match_trial(seed):
 (VA,_,_),(VB,_,_)=halves(ALPHA3_BITS)
 CACHE.clear()
 M,mx,ok,n=[W(0)],[],True,0
 for t in {h64(seed,bytes([i]))%64 for i in range(4)}:
  D={}
  for i,v in enumerate(VB):
   D.setdefault(v>>25*t&0x1FFFFFF,[]).append(i)
  for v in VA:
   r=D.get(v>>25*t&0x1FFFFFF)
   if r:
    OPS[0]=0
    res=match_run(to_planes(v),[to_planes(VB[b]) for b in r],64,M,M_CAP)
    ok=ok and OPS[0]==PER_A+MATCH_STEP*len(r)+3*(len(r)//UNR) and len(res)==len(r)
    mx.append(len(r))
    for (dec,asn),b in zip(res,r):
     x=v^VB[b]
     AS=((x|x>>1|x>>2|x>>3|x>>4)&FM).bit_count()
     ok,n=ok and asn==AS and dec==(AS < 64),n+1
 v=VA[h64(seed)%len(VA)]
 OPS[0]=0
 res=match_run(to_planes(v),[to_planes(VB[i]) for i in range(37)],64,[W(0)],M_CAP)
 ok=ok and OPS[0]==PER_A+37*MATCH_STEP+6
 for i,(dec,asn) in enumerate(res):
  x=v^VB[i]
  ok=ok and asn==((x|x>>1|x>>2|x>>3|x>>4)&FM).bit_count()
 return ok and n==M[0] > 0 and len(res)==37,{"matches": n,"runs": len(mx),"longest_run": max(mx)}
MT6 = (
 "0emt06m306ws0amr049i006x05tq0biy02wq05ji0bcq08o808hk04mn03q60gsq001i11us051t024g0jjm01xu0c0j0ewd003f0dfi0fn508ix"
 "004p09jx00sp0a2d0iql00ke0bkr0b9a04ya0ydk00fv00yx01nr02k90egu0gmw00el0gro0dhq09s0044v078p04zz01y612yf058g06oi0hbv"
 "0ec405wx1n1s08r10gqj09ij0bux00lt0f2u06b308tq090r093i04ji002907l60bxm0cn303310blg05dk00k2099w07f801sc0g1v072x09vg"
 "0h2k0rmc0gza0e3e13qc06sh07wl065t07ol005d0q4005qj0f140bda0cfu0g0i08d2043d09at0rt5052y009t0lev0eiy00uw026m04rd0gq0"
 "01bs0dmq06w604830lzd04wc0apn0iyn0awj0an906uk055w0khb0f2t02wd004s0n9u0cyl02he07e303ij05tm07vz0i6l07bx08or000k0g7c"
 "0904002s00uq0cg80jr60adh0fof04tz0j3e000v06h80k4506sa0a4x0isp00fz08190yuf00po0jqw04h7000004jx06og07f30g140aej06gk"
 "07w702yi0q1i046s06ft0cv6015s06mp02u608tg066m05wq0n4e005r0gpr01up09vi089v09vs0l3d0e0k005a05zy0ezi0ald001k00fe05up"
 "0l1s035g00k80dqv00sk0b1x05r1000u036x07ba05rf03k81eis0c5g04aq0apj0axu0j470cs503ra0071012806ga066s07au166907s10j62"
 "0687002j0gv308jq033v05i616hm01a60u71025i0bmq03t006cj042g0hda0fv90jhm07jf02hk0cfd01ww097n000f00000iun03fe14i10en7"
 "00bk07vq003g0gf50bna077c000k05bd0ig30ctt0eks0gup0hzd04va08td01n90bfo0dai0a3404wz08tf0026003b0e1y0rvc09m90aa106lt"
 "006z098w032c08ws034f00eo08md08zh05pk00000cz507hv04yg0e630j5b07pi0h1l0est0uvt0los0etn07gl09vg000r01c70dtu019i00no"
 "000m03yo0hwx01mw0zlw0cax0c490fqd07qi03n0026s08h604ml0431030j05650gsc00zn07s700280ffv08zg0wyo0a460dzh0cam092204fw"
 "004d0dch12oe07qp081i0d8405d105ia033f028100op01tp03tv041v0hfv083t1qe006va097a073i07m7009309ry0bjd0eq504qu086706lh"
 "0i4206370duq0buc0b8y0fmb0e0t0fvq00l80af6095t0lrq03nk09ey0cfc01gg0gje0a7a0vsy09ww03k608jo0ese003j06va05pc052j017g"
 "001m061k0ttw03kf0b4z088g040p06cr0f2f0bb2072805qb04gf05pl06tj009t0ryh04m702bk0g8204cb06cx093k07ck0z010h27058h0gg1"
 "0e620ia80bi9006x00m407ia046l02ty02wf0avx0085001506a600zy000o03de0l810azs06x20qqs027v0cpb00jg0aft07hj075h08oq03f3"
 "0gpc06m0005e04vi03g7002g054b0hp607ph006y03eg07qn045b033u05y40731098v0asd007o"
)
LANEM = (
 "100100400000000000002020000000000000804000000000000000007000200010010000060100100000001000000400000c00100000000000840080010000000000000000000000",
 "36c13b38104af075a5c8d55f610056001b380e319812c3721ea587a5fca02b80380200545087dca7b6bc7cea6d3e26bb276028",
 "3ca686c1b9479a41ea6ae46c00e40a9060e6a30df258b813889", "412d235ccf1c79297479", "0",
 "1fce80060806f27cc11450800118300823884ad3bc7185", "2400203e45abc3011821dc1a7850f2", "fb78001001c8", "3", "0",
 "40000674", "20", "20", "0", "0", "1"
)
C874 = (64,229,397,613,1024,1037,1189,1253)
C1136 = (128,226,1186,1263,1408,1583)
OUT_CORE,OUT_LOG = 17,(127,24,(0,0,3,0,0,0,0,0,3,1))
def p_trial(t):
 try:
  tr,m=trail_search(0 if t else M_CAP,[C874,C1136])
 except CapReached:
  return t==1,{"cap_reached": 1}
 return t==0 and tr is None and m==102,{"matches": m}
def kept_core(q):
 n=0
 for lane,hx in enumerate(LANEM):
  m=int(hx,16)
  if q < n+bin(m).count("1"):
   own=sorted(c for c in lane_dfs(lane)[1] if min(b>>6 for b in c)==lane)
   return [c for i,c in enumerate(own) if (m>>i)&1][q-n]
  n += bin(m).count("1")
def mitm_trial(q):
 c,M=kept_core(q),[0]
 r,f=mitm_core(halves(c),64,M,M_CAP)
 CACHE.clear()
 ok=p45pos(c) and M[0]==int(MT6[4*q:4*q+4],36)
 if q==OUT_CORE:
  rows,ins,_=core_tables(c)
  b2=sum(((ins[j][i]>>x)&1)<<(64*(x+5*y)+z) for j,(((y,z),_),i) in enumerate(zip(rows,r[2])) for x in range(5))
  ok=ok and c==ALPHA3_BITS and r==OUT_LOG and f==30 and b2==BETA2
 else:
  ok=ok and r is None and f==0
 return ok,{"core": q,"matches": M[0],"evals": f,"w1": r[0] if r else -1}
def rlab(t,k):
 return b"hashsmash sha3-256-r5 R%d run %d"%(t,k)
RUNS = [
(2,46,35,"c77293bd8cc36bc5",0,50,0x00000000,0,""),
(0,13,41,"93441f6d8ef1c998",29,35,0x14afb8c6,38,"5A5AAAAAAA55AAAAAAAAAAAAAAAAAAA55A5A"),
(0,13,46,"1a053b00d974731b",18,83,0x3f841d38,42,"55A55555555AA5A5555A55555A5555A5A5A555555A555A55555555A5555555555A55555A555A5A55A55A"),
(3,11,64,"ed18bb096de7e629",6,5,0x7b036919,58,"AAAAAA"),
(1,0,44,"d8ff2e2f9d27bb33",12,40,0xea8b24fb,42,"55AA55555AA5A5A55AA5555555A55AA555555555A"),
(0,9,36,"98e524f22bce3628",46,309,0xcf0d4d9d,34,"5555555555A55555555A55AA5555A55A5555555555555AA55A55555555555555A5555A55555A5555555555AA55555555555A5A55A5555555555555A55555A555555AA5555555A555A55A55A555555555555555555A55555555A55555A5555A5A5555555555555A5A55A5555555555A5A555A55555A555555A5555A55555555555555555555555555A555555A555A5A55555555555A55555555A55A"),
(0,2,51,"abb122235c4adbe6",0,63,0x00000000,0,""),
(3,10,52,"fbaf37444aad12b9",7,8,0x701bd5c0,48,"A5A5AAAAA"),
(0,22,53,"ccb18ee87d9d191a",37,78,0xa39eedce,53,"5AA55A5A5AA55A5AA5AA5A5A55A555A5A5A5555A5AAAA5AA5A5555555AA5A5A5A55AA55A55A5AAA"),
(0,10,36,"fddf5180a8ca2813",25,43,0x46d9e789,35,"A5AAAA5AA5A5555AAA55A5A55555AAAA5AAA5AA5AA5A"),
(10,11,51,"b79426b76d04f41f",28,31,0x099dbac3,46,"AAAAA5AA5AA5A5AAAAAAAAAAAAAAAAAA"),
(0,17,43,"c4ce8f0c8901cf72",6,5,0xd6ddbc42,42,"AAAAAA"),
(3,6,46,"3fa981f80b948630",0,133,0x00000000,0,""),
(5,22,34,"61abdc6a7e6182bd",11,10,0x0f571823,34,"AAAAAAAAAAA"),
(1,0,55,"a2b5d3279e774592",28,44,0x8874542d,49,"AA55AA555A55AA5A5AA5A55AAAAAAAA5AAAA5AA5A55AA"),
(0,4,43,"ac15905391f68258",27,26,0x17cbaca4,41,"AAAAAAAAAAAAAAAAAAAAAAAAAAA"),
(2,19,45,"18818fa2a136d8b4",21,43,0xd4bf3291,37,"AA55555AA5A5555A555A5A5A55AA5AA5A55A5AAA5AAA"),
(2,17,41,"637b852bf5ddc045",31,32,0xef731b50,38,"AAAAAAAAAAAAAAAAAAAAA5AAAAAAAA5AA"),
(0,17,53,"95e448982407b2c5",36,73,0x28f6dafe,45,"A5A5A555AA5A5AA5A555555AAAA5A55AAA555AA5A5AA5555AAA5A5A5555AA5AAA5AAA5555A"),
(0,28,41,"a9d599fa604d6501",1,0,0x90f42c45,40,"A"),
(2,13,45,"e9549a18989c7518",14,20,0x9bdb3915,43,"5A5AAAAA55AA5AA55AAAA"),
(1,37,44,"2a3999b8aaf98499",25,24,0xc8c8a787,43,"AAAAAAAAAAAAAAAAAAAAAAAAA"),
(0,22,34,"f92d23303be1dd52",26,386,0x2517d4eb,33,"55A55A555555555555555555555555555A555A555555A55A5555555555555A5555555A5A555555555555555555A55A555555555555A555A555555555A5555555555555555555555555555555555555555A55555555555555555555A55555555555555555555555555555555555555555555555555555555555555555555555A555555555555555A5555555555555555555555A5A5555555555555555555555555555555555555555555555555AA55555555A55555555555555555A5555555555A5A"),
(0,11,35,"ddcc3e19ee60a957",36,56,0xa32a9ebe,33,"555AAA5A55AAAA5A5555AA5AAAAAAAA555A5AA55AA5AA5AAAAA5AAAAA"),
(1,53,51,"4f9e4e217b2de888",10,13,0xefd6d6e4,51,"AA555AAAAA5AAA"),
(0,2,37,"9ac10084122c6e93",0,149,0x00000000,0,""),
(4,6,40,"0c0b6086331ecea3",10,37,0xc8bb7651,35,"55566A555655A56A565555A66656A56AA5AA5A"),
(0,9,35,"f17b2b118903399a",0,49,0x00000000,0,""),
(3,17,41,"5c6ace3df80889ce",0,49,0x00000000,0,""),
(0,38,34,"d9dfb5304f2dc12b",0,111,0x00000000,0,""),
(5,19,57,"e6010c2cf39b5f0f",0,102,0x00000000,0,""),
(2,5,35,"3d0b87a51b8a22eb",0,49,0x00000000,0,""),
(11,0,34,"2c7856ac76b55201",23,50,0xd6b309ed,33,"A66A6AAA666A66A66AAA666A666666AA666A6A66AA666AAAAAA"),
(0,4,54,"19f57b569b6b95fd",13,17,0x02e46ab6,52,"A5AAAA5A5A5A5AAAAA"),
(2,22,46,"7f146b852380cc50",1,0,0x771c8283,43,"A"),
(6,7,35,"30583b097e294faf",10,9,0x5067a7b7,35,"AAAAAAAAAA"),
(1,1,40,"9df8f3bec19fcb6c",11,25,0x85c7c5ff,38,"AA555A5AA5A5555A555A5A55AA"),
(0,0,36,"d5f11b4090d2aa4e",40,363,0xd3f097a2,33,"666666666666A6666666666656666AA6656666666AA666A66A6666A666666666666A66666665A666666666666A666A666666666A6A66A66666566666666666666566655666666666666666666666A6A6666A66666666666A666A5666A66666A6666A665666666566655666666665A66666A556666A66AA6666666666A66665666656666666666A65656656666666A666666666A666A66666A66666666666656666A65666655A66665A6656A66666665666666666A66A"),
(1,1,38,"b6d85578fe2729db",7,18,0x4ef230d9,37,"A555AA5555555A5AA5A"),
(0,24,33,"d176bb5436b917e7",44,321,0x186c8baf,33,"65A555566666655666A655566555666556666666A56A66AAA55A6565655656656A6665656556AA5666A66A556A6555665A5665666556656665666565A66566556A656656555665A56566A65A56A56A656A6665666556AA66666666A555A66666656655A6A5565666666566665566555556656AA65566A566A655A6666565566655666655AA56565556A56A6665665AAA66A665566556A66555666655566565656A"),
(0,9,44,"ec7a37b04adfb4db",23,27,0x6f3c6bcc,41,"AAAAAA555AA5AAAAAAA5AAAAAAAA"),
(2,67,60,"1810e29c96d7594f",11,10,0x4d6abffd,57,"AAAAAAAAAAA"),
(2,54,53,"8d60990b16b4a398",13,56,0xbe9110d3,49,"5A555555A55555A55A55A555555AAA555555A55555A5555555555A5AA"),
(0,29,39,"47e81ff204f3b35b",4,3,0x2cea1adb,39,"AAAA"),
(1,25,63,"66225c5e82cf75c2",21,36,0x269333df,55,"AAA5A555AA55A5AA5A5A55AAAA5AAA5555AAA"),
(0,12,57,"171072fba820027a",38,39,0xb890cd6b,50,"AAAAAAAAAAAAAAAAA5AAAAAAAAAAAAAAAA5AAAAA"),
(4,17,35,"cca5e7d7f5020ecb",20,19,0xa1ee8ada,33,"AAAAAAAAAAAAAAAAAAAA"),
(0,3,42,"63866873ed912295",30,33,0x4d570e93,39,"AAAAA5AAAAA5AAAA5AAAA5AAAAAAAAAAAA")]
R7S = [k for k in range(48) if RUNS[k][4]]
RPL = [k for k in R7S if k not in (22,)]
CHEAP = {37: 11331166259, 33: 13220514578, 6: 16446246658}
def h64(seed,t=b""):
 return int.from_bytes(sha256(bytes.fromhex(seed)+t)[:8],"little")
def replay(base,OB,k,seed):
 c,j,df,h,idx,i,coord,dfp,s=RUNS[k]
 lab=rlab(7,k)
 cs=CandSetup(base,OB,lab,c)
 res,b0=b_attempt(cs,lab,j,B_DMIN)
 st=cs.t
 st.ref=b0
 ok=res["st"]=="ok" and res["DF"]==df and hashlib.sha256((hex(cs.beta1)+hex(b0)).encode()).hexdigest()[:16]==h
 ok=ok and facts(st)[0] and len(s)==i+1 and s[i]=="A" and s.count("A")==idx<=K_SPACES
 pool=list(range(i))
 for q in range(min(23,i)):
  r=q+h64(seed,b"a%d"%q)%(i-q)
  pool[q],pool[r]=pool[r],pool[q]
 run=sorted(pool[:23])+[i]
 got=""
 for a in run:
  status,info=attempt(st,Coins(run_seed(lab+b"conn"+(c+1).to_bytes(4,"little"),a)))
  got += "A" if status=="ok" else str(STATUS[status])
 ok=ok and got=="".join(s[a] for a in run) and info.get("DF")==dfp
 obs={"k": k,"attempt": i,"space": idx,"rechecked": len(run),"status_ok": ok}
 if ok:
  v0,basis=enum_basis(info["EM"],info["beta0"],32)
  p,o=e_window(st,v0,basis,info["beta0"],coord-coord%WINDOW,WINDOW)
  obs["window_round2_passes"]=p
  if o and o[0]==coord:
   return o[1:],obs
 return None,obs
def cp_lower(x,n):
 lo,hi=0.0,1.0
 for _ in range(100):
  m=(lo+hi) / 2
  if sum(math.comb(n,i)*m ** i*(1-m) ** (n-i) for i in range(x,n+1)) < 0.05:
   lo=m
  else:
   hi=m
 return lo
def bp_rows(trials):
 n=len(trials)
 out=[(None,{}) for _ in range(n)]
 base,OB=Base(),own_bits()
 k=sorted(CHEAP)[h64(trials[0]["seed"])%3]
 c,j,df,h=RUNS[k][:4]
 c0,d0=WK.cost(),WK.d
 r=bprime(base,OB,rlab(7,k))
 sp=WK.cost()-c0
 ok=r is not None and r[2:]==(c,j,df) and sp==CHEAP[k] and hashlib.sha256((hex(r[0])+hex(r[1])).encode()).hexdigest()[:16]==h
 st=Setup(base,r[0],r[1]) if ok else None
 out[0]=(SENTINEL if ok and facts(st)[0] else FAIL_PAIR,{"k": k,"cost": sp,"true": sp+WK.d-d0})
 bud,c0,lg=1355<<22,WK.cost(),[]
 r=bprime(base,OB,rlab(5,2),bud,lambda *a: lg.append(a),0,CCAP>>5)
 sp=WK.cost()-c0
 cd=[WK.cost(a[4])-c0 for a in lg if a[0]=="cand"]
 ok=r is None and bud < sp<=bud+(1355<<13) and len(cd)==2 and bud / 2 < cd[1]<=bud / 2+(1355<<13)
 out[1]=(SENTINEL if ok else FAIL_PAIR,{"cost": sp,"cands": len(cd),"cand1": cd[-1]})
 x=len(R7S)
 p0=cp_lower(x,len(RUNS))
 ok=len(RUNS)==48 and x==39 and all(len(RUNS[q][8])==RUNS[q][5]+1 for q in R7S) and p0>=0.40
 out[2]=(SENTINEL if ok else FAIL_PAIR,{"runs": len(RUNS),"successes": x,"cp95_lower_x1e4": int(p0*10000)})
 for t in range(3,min(n,27)):
  if st is None:
   break
  coins=Coins(bytes.fromhex(trials[t]["seed"]))
  status,info=attempt(st,coins)
  obs={"status": STATUS[status],"df": info.get("DF",-1),"work_units": info["xors"]}
  out[t]=(SENTINEL if status=="ok" and verify_space(st,info,coins) else FAIL_PAIR,obs)
 return out
def rows_for(mode,trials):
 n=len(trials)
 out=[(None,{}) for _ in range(n)]
 if mode.startswith("r5-trail-"):
  for t,g in enumerate(mode[9:]):
   ok,obs=trail_group(int(g))
   out[t]=(SENTINEL if ok else FAIL_PAIR,obs)
  return out
 if mode=="r5-count":
  if eqs_ok():
   for t,tr in enumerate(trials[:12]):
    ok,obs=e_block(tr["seed"]) if t==11 else mitm_trial(OUT_CORE) if t==10 else p_trial(t-8) if t>=8 else (fes_trial,t2_trial)[t%2](bytes.fromhex(tr["seed"]))
    out[t]=(SENTINEL if ok else FAIL_PAIR,obs)
  return out
 if mode.startswith("r5-mitm-"):
  q=OUT_CORE if mode[8:]=="out" else h64(trials[0]["seed"],mode.encode())%len(MT6)//4
  for t,(ok,obs) in enumerate((mitm_trial(q),)+((hv_trial(),match_trial(trials[0]["seed"])) if mode[8:]=="1" else ())):
   out[t]=(SENTINEL if ok else FAIL_PAIR,obs)
  return out
 if mode=="r5-bpfull":
  return bp_rows(trials)
 g=int(mode[5:])
 L=RPL[g::8]
 q0=h64(trials[0]["seed"])%len(L)
 q1=(q0+1+h64(trials[1]["seed"])%(len(L)-1))%len(L)
 base,OB=Base(),own_bits()
 for t,q in enumerate((q0,q1)):
  out[t]=replay(base,OB,L[q],trials[t]["seed"])
 return out
def main():
 req=json.loads(sys.stdin.read())
 rows=[]
 for tr,(pair,obs) in zip(req["trials"],rows_for(req["experiment_id"],req["trials"])):
  rows.append({"trial": tr["trial"],"message_a_hex": pair[0].hex() if pair else None,
     "message_b_hex": pair[1].hex() if pair else None,"observations": obs})
 sys.stdout.write(json.dumps({"schema_version": 1,"trials": rows},separators=(",",":")))
if __name__ == "__main__":
 main()
