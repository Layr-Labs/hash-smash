"""v8 experiments (proof.md): B' with its budget (2.2), S and the connector (2.3), E on a window (2.4), the
driver (2.5).  The trail is P's output; each advice is re-derived from its label by B'.  rows_for() follows
the manifest.  PASS = (00^135, 01||00^134), FAIL = (00^135, 02||00^134); the evidence is this code's run."""
import hashlib
import json
import sys
import collections
from fractions import Fraction
# Bit i = 64*(x+5y)+z.  Affine form over x = L(A0): int, bits 0..1599 coefficients, bit 1600 constant.
N = 1600
MASK = (1 << N) - 1
M64 = (1 << 64) - 1
RHO = (0, 1, 62, 28, 27, 36, 44, 6, 55, 20, 3, 10, 43, 25, 39, 41, 45, 15, 21, 8, 18, 2, 61, 56, 14)
RCS = (0x1, 0x8082, 0x800000000000808A, 0x8000000080008000, 0x808B)
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
  """L = pi o rho o theta."""
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
  """All affine subsets of GF(2)^5, by dimension, each as a sorted list; each list sorted."""
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
  """Basis (m, c) of the equations <m, v> = c satisfied by every v of the affine set W."""
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
  """Echelon set of affine forms keyed by leading (highest) coefficient bit, with undo log.
  budget = [work units so far, cap], shared by the systems of one attempt (hard work cap); one unit
  is one call of reduce() or one row addition inside it."""
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
    """1 = added, 0 = implied, -1 = inconsistent (not added)."""
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
  """rows[j] = form of output bit j of the linear map fn (as coefficients over the input)."""
  rows = [0] * N
  for i in range(N):
    c = fn(1 << i)
    while c:
      lb = c & -c
      rows[lb.bit_length() - 1] |= 1 << i
      c ^= lb
  return rows
def Linv_map(s):
  """L^-1 = theta^-1 o rho^-1 o pi^-1, theta^-1 by solving the column-parity system."""
  B = lanes(s)
  A = [0] * 25
  for y in range(5):
    for x in range(5):
      i = x + 5 * y
      A[i] = rot(B[y + 5 * ((2 * x + 3 * y) % 5)], 64 - RHO[i])
  return _theta_inv(unlanes(A))
def _theta_inv_setup():
  # theta^-1(b) = b + E((I+T)^-1 P(b)), P = column parity; (I+T)^-1 by Gauss-Jordan.
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
  """Rows of L^-1 (= linear_rows(Linv_map), checked in facts()) via the rows of (I+T)^-1."""
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
# -- advice and trail (proof 2)
# BETA2 and ALPHA3_BITS: the trail core output by the search P (proof 2.1).
BETA2 = unlanes([0x1, 0, 0x4, 0, 0, 0x4, 0x4, 0x4, 0x20000, 0, 0x2000000000000000, 0, 0x200000, 0, 0,
        0x2000000000000000, 0, 0, 0x20000, 0, 0x200001, 0, 0x200000, 0, 0x1])
ALPHA3_BITS = (0, 130, 450, 529, 701, 789, 1021, 1169, 1280, 1429)
# -- work counters (B', proof 2.2)
class BudgetExceeded(Exception):
  pass
class _WKMeta(type):
  """Every counter update re-checks the budget: once WK.cap is set (integer, in 1/1355 units),
  the first update that takes the charged cost above it raises BudgetExceeded (hard cap)."""
  def __setattr__(cls, k, v):
    type.__setattr__(cls, k, v)
    if cls.cap is not None and cls.cost() > cls.cap:
      raise BudgetExceeded()
class WK(metaclass=_WKMeta):
  row = 0  # operations on one <= 2585-bit integer (XOR, AND-test, element copy, compare): 256 primitives
  small = 0  # word operations on <= 64-bit values (table lookups, loop steps): 8 primitives
  keccak = 0  # Keccak-f[1600] calls (SHAKE-256 coin expansion): 5 units
  sha256 = 0  # SHA-256 compression calls (seeds): 2 units
  r2 = 0  # 2-round state evaluations in verification: 1 unit
  cap = None
  @staticmethod
  def snap():
    return (WK.row, WK.small, WK.keccak, WK.sha256, WK.r2)
  @staticmethod
  def cost():
    """Charged cost so far in 1/1355 units (exact integer)."""
    return 256 * WK.row + 8 * WK.small + 1355 * (5 * WK.keccak + 2 * WK.sha256 + WK.r2)
def sha256(b):
  WK.sha256 += (len(b) + 9 + 63) // 64
  return hashlib.sha256(b).digest()
# -- coins (proof 4.1)
class Coins:
  """Coin word j: bytes 32j..32j+31 (little-endian) of SHAKE-256(seed || k)[4096 bytes], k = 0, 1, ...
  (4 bytes LE).  perm(): Fisher-Yates, j = (low 64 bits of one word) mod (i+1) (proof 4.1)."""
  def __init__(s, seed):
    s.seed, s.k, s.buf, s.pos, s.draws = seed, 0, b"", 0, 0
  def word(s):
    if s.pos >= len(s.buf):
      s.buf = hashlib.shake_256(s.seed + s.k.to_bytes(4, "little")).digest(4096)
      WK.keccak += 31  # 1 absorb + 30 further squeeze calls for 4096 bytes at rate 136
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
  """Seed of attempt i of a labelled run: SHA-256(label || i as 8 little-endian bytes)."""
  return hashlib.sha256(label + i.to_bytes(8, "little")).digest()
# -- setup S (proof 2.3)
class Base:
  """The advice-independent part of S (also B's base): L, L^-1, fixed bits, trail, E's row tests."""
  def __init__(s):
    for k in range(6):  # equations of every affine subset of GF(2)^5
      for Wl in AFFL[k]:
        annih(Wl)
    WK.small += 2451 * 2048
    s.Lrow = linear_rows(Lmap)
    s.Linv = linv_rows()  # = linear_rows(Linv_map); facts() checks it
    WK.row += 2 * N * 30
    s.FIX = list(range(1080, N))
    s.fixval = {j: 0 for j in s.FIX}
    for k in range(8):
      s.fixval[1080 + k] = (0x86 >> k) & 1
    s.beta2 = BETA2
    s.alpha2 = Linv_map(BETA2)
    a3 = 0
    for b in ALPHA3_BITS:
      a3 |= 1 << b
    s.alpha3 = a3
    s.a2rows = [(y, z, getrow(s.alpha2, y, z)) for (y, z) in ROWS if getrow(s.alpha2, y, z)]
    assert len(s.a2rows) == 59
    # round-2 test of E: row r of the round-2 chi input must lie in V(beta2_r, alpha3_r)
    s.e_rows = [(y, z, VSET[(getrow(s.beta2, y, z), getrow(s.alpha3, y, z))])
          for (y, z) in ROWS if getrow(s.beta2, y, z)]
# -- advice run B' (proof 2.2)
# B' parameters (pre-registered): D2u candidate ordering weights
KW, MW, LB, PREF = 1.0, 0.25, 1.0, 1.0
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
  """The beta1-dependent part of S (proof 2.3): round-1 conditions, masks, linearisation table."""
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
# -- affine spaces stored transposed
class Aff:
  """T[j]: bit 0 = coordinate j of a particular solution, bit i+1 = coefficient of free parameter i."""
  __slots__ = ("T", "rank")
  def __init__(s, T, rank=0):
    s.T, s.rank = T, rank
  def copy(s):
    WK.row += len(s.T)
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
  """Bit mask (over 2^n values) of the values of coordinates cs allowed by the space."""
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
# -- difference side: links, D2u
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
  """Base value space (fixed bits only), used for the link constants x_b1 + x_b2 = c."""
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
  """Port-uniform test of an affine set Wd of differences: same fixed port combos for every d in
  Wd and constants affine in d.  Returns [(mask, lam, c0)] with kappa_mask(d) = c0 + lam.d."""
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
# -- value side: Model, M2
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
  """Coordinates x and u_{r,k} = b_{r,k} . chi(x_r) (basis of the row's masks); candidates (d, W) per row."""
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
# -- driver
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
B_R, B_DMIN = 16, 40  # B' constants (with KW, MW, LB, PREF): fixed by development runs
B_BUDGET = 1355 << 34  # hard cap of B' (2^34 units), counted from the start of B'
def bprime(base, OB, label, budget=B_BUDGET, log=None):
  """B' (proof 2.2): candidates c = 0, 1, ..., R attempts each; (beta1, beta0, c, j, DF) at the first
  accepted attempt, None when the budget is exhausted."""
  WK.cap = WK.cost() + budget
  try:
    c = 0
    while True:
      s0 = WK.snap()
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
      c += 1
  except BudgetExceeded:
    return None
  finally:
    WK.cap = None
def Setup(base, beta1, beta0):
  """S for one advice (beta1', beta0'): Base plus the round-1 conditions and linearisation table of
  beta1' (class Cand); D2 and M2 steer toward beta0' (st.ref)."""
  st = Cand(base, beta1)
  st.ref = beta0
  return st
# -- one connector attempt (proof 2.3)
def attempt(st, coins, dmin=33, xor_cap=1 << 18):
  """One connector attempt.  Returns (status, info); info["xors"] = work units, info["draws"] = coin words."""
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
  for j in st.FIX:  # D1
    if ED.add(Linv[j]) < 0:
      return "dinc", None
  for (y, z) in ROWS:
    if rows_a1[(y, z)] == 0:
      for b in rowbits(y, z):
        if ED.add(1 << b) < 0:
          return "dinc", None
  order = list(st.act)  # D2
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
  EM = Ech(budget)  # M1
  for j in st.FIX:
    if EM.add(Linv[j] | (st.fixval[j] << N)) < 0:
      return "minc", None
  beta0 = 0
  Srow = {}
  for (y, z) in order:  # M2
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
  for r in st.lin_rows:  # M3
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
  for (parts, c) in st.condparts:  # M4
    f = c << N
    for r, m in parts.items():
      f ^= aff[(r, m)]
    if EM.add(f) < 0:
      return "cond", None
  DF = N - EM.rank()  # M5
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
# -- space and enumeration E (proof 2.4)
def enum_basis(EM, beta0, nb=32):
  """Offset v0 and the enumeration basis b_1..b_nb of proof 2.4 (kept free-variable solutions)."""
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
  """E on coordinates lo..lo+count-1 (c: x = v0 + sum of b_j, j in c): if the 10 rows of beta2 of
  u = L(chi(L(chi(x) + RC0)) + RC1) lie in V(beta2_r, alpha3_r), compare the 5-round digests of L^-1(x),
  L^-1(x + beta0).  Returns (round-2 passes, first output)."""
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
# -- exact facts (proof Section 3)
SENTINEL = (bytes(135), b"\x01" + bytes(134))
STATUS = {"ok": 0, "dinc": 1, "minc": 2, "tda": 3, "lin": 4, "cond": 5, "lowdf": 6, "cap": 7}
def kernel(s):
  L = lanes(s)
  return all((L[x] ^ L[x + 5] ^ L[x + 10] ^ L[x + 15] ^ L[x + 20]) == 0 for x in range(5))
def active_rows(s):
  return [(y, z, getrow(s, y, z)) for (y, z) in ROWS if getrow(s, y, z)]
def wt(d, o):
  return 5 - (DDT[d][o].bit_length() - 1)
def facts(st):
  ok = []
  a3 = st.alpha3
  b3 = Lmap(a3)
  ok.append(kernel(a3) and kernel(b3) and bin(b3).count("1") == 10)
  a2 = st.alpha2
  r2 = active_rows(a2)
  w1 = sum(min(wt(d, o) for d in COMPAT[o]) for (_, _, o) in r2)
  ok.append(len(r2) == 59 and w1 == 127)
  rb2 = active_rows(BETA2)
  ok.append([(y, z) for (y, z, _) in rb2] == [(y, z) for (y, z, _) in active_rows(a3)])
  ok.append(all(DDT[d][getrow(a3, y, z)] for (y, z, d) in rb2))
  ok.append(sum(wt(d, getrow(a3, y, z)) for (y, z, d) in rb2) == 24)
  c2 = 1
  for (_, _, o) in active_rows(a3):
    c2 *= len(COMPAT[o])
  ok.append(c2 == 3486784401)
  # P45 (proof 3)
  M320 = (1 << 320) - 1
  opts = []
  for (y, z, d) in active_rows(b3):
    ol = []
    for o in range(32):
      if DDT[d][o]:
        s = 0
        for x in range(5):
          if (o >> x) & 1:
            s |= 1 << (64 * (x + 5 * y) + z)
        ol.append((Lmap(s) & M320, DDT[d][o]))
    opts.append(ol)
  def combos(group):
    out = [(0, 1)]
    for ol in group:
      out = [(v ^ w, p * q) for (v, p) in out for (w, q) in ol]
    return out
  ga, gb = combos(opts[:5]), combos(opts[5:])
  pz = [DDT[d][0] + DDT[d][16] for d in range(32)]
  p45 = Fraction(0)
  nz = 0
  for (va, pa) in ga:
    for (vb, pb) in gb:
      v = va ^ vb
      l4 = (v >> 256) & M64
      if ((v | (v >> 64) | (v >> 128) | (v >> 192)) & M64) & ~l4:
        continue
      num, den = pa * pb, 32 ** len(opts)
      for z in range(64):
        if (l4 >> z) & 1:
          num *= pz[sum(((v >> (64 * x + z)) & 1) << x for x in range(5))]
          den *= 32
      if num:
        nz += 1
        p45 += Fraction(num, den)
  ok.append(len(ga) * len(gb) == 1 << 19 and nz == 192 and p45 == Fraction(55, 1 << 19))
  # advice facts of proof 3
  b1, b0 = st.beta1, st.ref
  ok.append([(y, z) for (y, z, _) in active_rows(b1)] == [(y, z) for (y, z, _) in r2])
  ok.append(all(DDT[getrow(b1, y, z)][o] for (y, z, o) in r2)
       and sum(wt(getrow(b1, y, z), o) for (y, z, o) in r2) == 127)
  alpha1 = Linv_map(b1)
  ok.append(len(active_rows(alpha1)) == len(st.act))
  ok.append(all(DDT[getrow(b0, y, z)][getrow(alpha1, y, z)] for (y, z) in ROWS))
  a0 = Linv_map(b0)
  ok.append(a0 != 0 and all(((a0 >> j) & 1) == 0 for j in st.FIX))
  ok.append(len(st.e_rows) == 10)
  # the fast rows of L^-1 (linv_rows) act as the map Linv_map on 16 fixed states
  good_linv = True
  for k in range(16):
    sv = int.from_bytes(hashlib.shake_256(b"linv" + bytes([k])).digest(200), "little")
    img = Linv_map(sv)
    good_linv = good_linv and all(par(st.Linv[j] & sv) == (img >> j) & 1 for j in range(N))
  ok.append(good_linv)
  return all(ok), ok
def verify_space(st, info, coins):
  """Lemmas 1-2 on two solutions of the accepted space (free variables from coin words)."""
  EM, beta0 = info["EM"], info["beta0"]
  alpha0 = Linv_map(beta0)
  for _ in range(2):
    xv = 0
    for i in range(N):
      if i not in EM.piv and coins.word() & 1:
        xv |= 1 << i
    x = solve(EM, xv)
    A, B = Linv_map(x), Linv_map(x ^ beta0)
    if A ^ B != alpha0:
      return False
    for S in (A, B):
      if any(((S >> j) & 1) != st.fixval[j] for j in st.FIX):
        return False
    if A == B:
      return False
    if rnd(rnd(A, 0), 1) ^ rnd(rnd(B, 0), 1) != st.alpha2:
      return False
  return True
# -- the algorithm (proof 2): phases and hard caps
K_SPACES, A_ADV, A_MAX, S2CAP = 56, 1 << 12, 1 << 16, 1 << 11
def algorithm(label):
  """Driver (proof 2.5) after P; label-derived coins (fresh words in the algorithm).  B' resumes after a
  discarded advice under one 2^34-unit budget; caps K, A_ADV, A_MAX, S2CAP; E on the K spaces in order."""
  base, OB = Base(), own_bits()
  WK.cap = WK.cost() + B_BUDGET
  c, att = 0, 0
  try:
    while att < A_MAX:
      adv = None
      while adv is None:
        cs = CandSetup(base, OB, label, c)
        for j in range(B_R):
          res, b0 = b_attempt(cs, label, j, B_DMIN)
          if res["st"] == "ok":
            adv = (cs.beta1, b0)
            break
        c += 1
      WK.cap, cap, h = None, WK.cap, WK.cost()
      st = Setup(base, *adv)
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
      WK.cap = cap + WK.cost() - h  # connector and S work is charged to their own terms, not to B'
  except BudgetExceeded:
    return None
  finally:
    WK.cap = None
  return None
# -- pre-registered runs (proof 4)
# B' runs k = 0..8 (label blabel(k)).  BRUNS[k] = (c, j of the output, DF, setup row ops of c, [(BCODE
# status, DF, row ops) of attempts 0..j of c], whole-run cost in 1/1355 units, advice hash).
LABEL_B = b"hashsmash sha3-256-r5 v6 B-prime advice run 1"
BCODE = {"ok": 0, "d2u": 1, "m2": 2, "lowdf": 3, "r1inc": 4, "verifyfail": 5}
BRUNS = [
  (5,9,41,9455652,[(3,28,22643603),(2,-1,16402616),(1,-1,4354998),(1,-1,4179068),(2,-1,11679482),(2,-1,4919172),(1,-1,3925603),(3,20,22051186),(1,-1,4245337),(0,41,23444127)],197406782652,"df21a71e7c62733c"),
  (0,2,42,9396804,[(1,-1,4796644),(2,-1,19742471),(0,42,25889567)],15477633191,"00204020a47686d2"),
  (14,5,42,9406316,[(1,-1,4720211),(2,-1,8020036),(2,-1,6742127),(2,-1,6343411),(2,-1,5330972),(0,42,25675211)],422981197118,"9ac1346b704e2c6f"),
  (9,10,49,9563576,[(2,-1,5618710),(2,-1,6582312),(2,-1,4764262),(1,-1,2305190),(1,-1,2561435),(2,-1,4191856),(1,-1,2342680),(2,-1,9112648),(2,-1,17325648),(2,-1,7156877),(0,49,30730486)],176961614948,"6b30dc9d72ee95a9"),
  (11,2,66,9492701,[(2,-1,7858756),(1,-1,3782543),(0,66,26157660)],308830018024,"ce139e77121543cb"),
  (2,11,40,9426553,[(1,-1,4651719),(2,-1,17179270),(2,-1,7957189),(3,34,23466530),(2,-1,7588098),(2,-1,7040094),(1,-1,5192853),(1,-1,4655979),(3,39,23684776),(1,-1,5380802),(1,-1,4921839),(0,40,23431698)],104491855877,"019fb5861f8592f5"),
  (7,6,47,9562407,[(1,-1,4512662),(2,-1,8851237),(2,-1,7459743),(2,-1,5329546),(1,-1,4771760),(1,-1,4480380),(0,47,29996425)],302626228894,"22fcc6e37c13fad2"),
  (6,10,50,9470713,[(2,-1,5558291),(2,-1,5562425),(2,-1,9023704),(2,-1,5102554),(2,-1,5002579),(2,-1,6292298),(1,-1,5237673),(2,-1,5060240),(1,-1,3883346),(2,-1,5142630),(0,50,26750922)],204120587481,"6d3cb04f43e88ca0"),
  (2,4,41,9333564,[(2,-1,19868556),(3,31,23488369),(2,-1,10846031),(3,23,22292276),(0,41,23725093)],36540767234,"e4d6d59a82d82271")]
BGROUPS = [(0, 1), (2, 3), (4, 5), (6, 7), (8,)]
T_CONN = 32
def blabel(k):
  return LABEL_B if k == 0 else b"hashsmash sha3-256-r5 v8 B-prime fresh run %d" % k
def b_check(base, OB, k, j, cs=None):
  """Re-run candidate c of B' run k from its label (unless cs is given) and its attempt j; compare with BRUNS[k]."""
  c, J, df, srow, atts, cost, h = BRUNS[k]
  s0 = WK.row
  if cs is None:
    cs = CandSetup(base, OB, blabel(k), c)
    srow_got = WK.row - s0
  else:
    srow_got = srow  # cs was built and checked by the previous trial
  s1 = WK.row
  res, b0 = b_attempt(cs, blabel(k), j, B_DMIN)
  got = (BCODE[res["st"]], res.get("DF", -1), WK.row - s1)
  ok = srow_got == srow and got == tuple(atts[j]) and cost <= B_BUDGET
  if j == J:
    ok = ok and res["st"] == "ok" and hashlib.sha256((hex(cs.beta1) + hex(b0)).encode()).hexdigest()[:16] == h
  return ok, {"k": k, "c": c, "j": j, "status": got[0], "df": got[1], "rows": got[2], "setup_rows": srow_got}, cs, b0
# v6 run (proof 4.2): REPLAYS = (attempt, coordinate); AUDIT_LOG[i] = "-" (rejected) or chr(97 + DF - 33).
LABEL = b"hashsmash sha3-256-r5 v6 run"
REPLAYS = [(38,0x3a3dfc53),(126,0xe7bb4868),(128,0x03527ad5),(184,0x93151f93),(205,0x17a92e95),(210,0xc4b6d61e),(232,0xd83a2af9),(246,0xbaf5b430),(253,0x893eed61),(275,0x03232068),(317,0x38473f47),(327,0x8ff14754),(390,0xb23e6790),(462,0xb49b4036)]
WINDOW = 1 << 12
AUDIT_LOG = "iijijiiiiji--ih-hji-hihhj--iiii-hh-ijiiihiihjhiiihiiihhiihii-ihhiijihijjihjhjjhiiiiijiij-j-jihiijiijiijhiiiiiihiijiiiiijihjijiiihhiihijjjhi-ihiiiiiiiiiiihijiiihhhih-i--j-hjhhiijiih-iihjhijjihjjhhiij-ihhiiihiijihii-ijhiiiiijiiihhiiiiiijhiiiihihiiiihhihhihjiiiijijhijiiiji-iiijjihihiijiijjjihiiiijiijiihhijjjii-hjihjhjhij-hihihhhihhjjjiiihiiiiihjiiiihjjihiiihijjijhjijhhi-hhihhiiijhihijiiiijihiijiihhhijiiijiiijijjhiijiiiijhijihihiiiihhijihiiijiii-ijijiiijihhiihiiiihijiiiiiiiiihhiijhiiiiihijjjjjhiiihiihj-hhiijihiihiijhiihjiiihihijiih-hiii"
DEN_N = 180
FAIL_PAIR = (bytes(135), b"\x02" + bytes(134))
# E-check collisions with fresh advice (proof 4.3): (k, connector attempt index, coordinate)
REPLAYS8 = [(4,0,0x13c3cc2f),(4,0,0x9707a665),(7,2,0x1e5fa912)]
def replay(st, lab, i, coord):
  """Re-run attempt i of run lab, rebuild its basis, run E on the 2^12 aligned coordinates containing coord."""
  status, info = attempt(st, Coins(run_seed(lab, i)))
  obs = {"status": STATUS[status], "df": info.get("DF", -1)}
  if status != "ok":
    return obs, None
  v0, basis = enum_basis(info["EM"], info["beta0"], 32)
  passes, out = e_window(st, v0, basis, info["beta0"], coord - coord % WINDOW, WINDOW)
  obs["window_round2_passes"] = passes
  if out is None or out[0] != coord:
    return obs, None
  obs["coordinate"] = coord
  return obs, out[1:]
def rows_for(mode, trials):
  n = len(trials)
  out = [(None, {}) for _ in range(n)]
  base = Base()
  if mode == "r5-bpfull":
    OB, c, J, df, _, _, cost, h = (own_bits(),) + BRUNS[1]
    for t, bud in enumerate((B_BUDGET, 1355 << 20)):
      c0 = WK.cost()
      r = bprime(base, OB, blabel(1), bud)
      sp = WK.cost() - c0
      ok = (r is None and bud < sp <= bud + (1355 << 13)) if t else (
        r is not None and r[2:] == (c, J, df) and sp == cost and hashlib.sha256((hex(r[0]) + hex(r[1])).encode()).hexdigest()[:16] == h)
      out[t] = (SENTINEL if ok else FAIL_PAIR, {"cost": sp})
    return out
  if mode.startswith("r5-bp-") or mode == "r5-replay8":
    OB = own_bits()
    if mode == "r5-replay8":
      sts = {}
      for t, (k, i, coord) in enumerate(REPLAYS8):
        if k not in sts:
          ok, _, cs, b0 = b_check(base, OB, k, BRUNS[k][1])
          cs.t.ref = b0
          sts[k] = cs.t if ok and facts(cs.t)[0] else None
        if sts[k] is not None:
          obs, pair = replay(sts[k], b"hashsmash sha3-256-r5 v8 conn run %d" % k, i, coord)
          out[t] = (pair, obs)
      return out
    ks = BGROUPS[int(mode[6:])]
    sts = []
    for q, k in enumerate(ks):
      J = BRUNS[k][1]
      ok, obs, cs, b0 = b_check(base, OB, k, J)
      cs.t.ref = b0
      sts.append(cs.t if ok and facts(cs.t)[0] else None)
      out[2 * q] = (SENTINEL if ok else None, obs)
      j = int.from_bytes(sha256(bytes.fromhex(trials[2 * q + 1]["seed"]))[:8], "little") % J
      ok, obs, _, _ = b_check(base, OB, k, j, cs)
      out[2 * q + 1] = (SENTINEL if ok else None, obs)
    for t in range(2 * len(ks), min(n, 2 * len(ks) + T_CONN * len(ks))):
      st = sts[t % len(ks)]
      if st is None:
        continue
      coins = Coins(bytes.fromhex(trials[t]["seed"]))
      status, info = attempt(st, coins)
      obs = {"k": ks[t % len(ks)], "status": STATUS[status], "df": info.get("DF", -1), "work_units": info["xors"]}
      pair = FAIL_PAIR
      if status == "ok" and verify_space(st, info, coins):
        pair = SENTINEL
      out[t] = (pair, obs)
    return out
  ok, _, cs, b0 = b_check(base, own_bits(), 0, BRUNS[0][1])
  st = cs.t
  st.ref = b0
  if not (ok and facts(st)[0]):
    return out
  if mode == "r5-replay":
    for t, (i, coord) in enumerate(REPLAYS):
      obs, pair = replay(st, LABEL, i, coord)
      out[t] = (pair, obs)
  elif mode.startswith("r5-den-"):
    for t in range(min(n, DEN_N)):
      i = DEN_N * int(mode[7:]) + t
      if i >= len(AUDIT_LOG):
        break
      status, info = attempt(st, Coins(run_seed(LABEL, i)))
      got = chr(ord("a") + info["DF"] - 33) if status == "ok" else "-"
      if got == AUDIT_LOG[i]:
        out[t] = (SENTINEL if status == "ok" else FAIL_PAIR, {"index": i, "status": STATUS[status]})
  return out
def main():
  req = json.loads(sys.stdin.read())
  rows = []
  for tr, (pair, obs) in zip(req["trials"], rows_for(req["experiment_id"], req["trials"])):
    rows.append({"trial": tr["trial"], "message_a_hex": pair[0].hex() if pair else None,
          "message_b_hex": pair[1].hex() if pair else None, "observations": obs})
  sys.stdout.write(json.dumps({"schema_version": 1, "trials": rows}, separators=(",", ":")))
if __name__ == "__main__":
  main()
