"""v10 experiments (proof 2.1, 2.4, 6).  r5-trail-g: P's counts for the start lanes of group g (T1 nodes per
lane; for the cores owned by the group: C1, P45 > 0, C2, T3 batches and groups) against GROUP_LOG.
r5-count: the counted programs of an E batch, a T3 batch and a T2 leaf: every operator on class W, load() and
st() count one primitive, test() two; words are 256-bit, bit p belongs to pair (leaf) p; fld(w, s, m) = (w >> s) & m.
Cap constants are instruction fields.  PASS/FAIL as in r5_connector.py; comments are omitted for the 64 KiB
budget (proof 2.1, 2.4 describe the code)."""
import hashlib
import json
import math
import sys

RHO = (0, 1, 62, 28, 27, 36, 44, 6, 55, 20, 3, 10, 43, 25, 39, 41, 45, 15, 21, 8, 18, 2, 61, 56, 14)
RC0, RC1 = 0x1, 0x8082
M64 = (1 << 64) - 1
ONES = (1 << 256) - 1
SENTINEL = (bytes(135), b"\x01" + bytes(134))
FAIL_PAIR = (bytes(135), b"\x02" + bytes(134))

def chi5(v):
  return sum((((v >> i) & 1) ^ ((1 ^ ((v >> ((i + 1) % 5)) & 1)) & ((v >> ((i + 2) % 5)) & 1))) << i
       for i in range(5))

CHI5 = [chi5(v) for v in range(32)]
DDT = [[0] * 32 for _ in range(32)]
for _d in range(32):
  for _v in range(32):
    DDT[_d][CHI5[_v] ^ CHI5[_v ^ _d]] += 1
NOUT = [sum(1 for o in range(32) if DDT[d][o]) for d in range(32)]
NIN = [sum(1 for d in range(32) if DDT[d][o]) for o in range(32)]
ALLOW = sum(1 << q for q in range(32) if DDT[q][0] + DDT[q][16])

def rot(v, a):
  return ((v << a) | (v >> (64 - a))) & M64 if a % 64 else v

def L(A):
  P = [A[x] ^ A[x + 5] ^ A[x + 10] ^ A[x + 15] ^ A[x + 20] for x in range(5)]
  T = [P[(x - 1) % 5] ^ rot(P[(x + 1) % 5], 1) for x in range(5)]
  B = [0] * 25
  for y in range(5):
    for x in range(5):
      B[y + 5 * ((2 * x + 3 * y) % 5)] = rot(A[x + 5 * y] ^ T[x], RHO[x + 5 * y])
  return B

def chi(A):
  return [A[x + 5 * y] ^ (~A[(x + 1) % 5 + 5 * y] & A[(x + 2) % 5 + 5 * y]) for y in range(5) for x in range(5)]

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

LANE_NODES = [345923, 346741, 347335, 347245, 346861, 346213, 348343, 346483, 347031, 348147, 347363, 346239,
       346119, 346755, 347715, 346837, 347449, 346491, 346881, 346221, 346885, 347921, 346649, 347657, 347329]
GROUPS = [(0, 1), (2, 3, 4, 5, 6, 7), tuple(range(8, 17)), tuple(range(17, 25))]
GROUP_LOG = [(692664, 1023, 974737408, 204, 608900651514, 2507358321, 616),
             (2082480, 646, 600711168, 251, 735420810384, 3028126761, 759),
             (3123655, 72, 63639552, 12, 34953937452, 143843364, 36), (2776034, 0, 0, 0, 0, 0, 0)]

def inner(ms):
  P, k = 1, 0
  while k < len(ms) and P * ms[k] <= 256:
    P, k = P * ms[k], k + 1
  if k == len(ms):
    return k, 1, 1, 1
  g = min(ms[k], 256 // P)
  G = -(-ms[k] // g)
  return k, g, G, G * math.prod(ms[k + 1:])

def trail_group(g):
  nodes, reach, lanes_ok = 0, set(), True
  for lane in GROUPS[g]:
    n, f = lane_dfs(lane)
    lanes_ok = lanes_ok and n == LANE_NODES[lane]
    nodes += n
    reach |= f
  own = [c for c in reach if min(b >> 6 for b in c) in GROUPS[g]]
  c1 = sum(math.prod(NOUT[d] for _, d in rows_of([FWD[b] for b in c])) for c in own)
  kept = [c for c in own if p45pos(c)]
  c2 = sum(math.prod(NIN[o] for _, o in rows_of(c)) for c in kept)
  lay = [inner([NIN[o] for _, o in rows_of(c)]) for c in kept]
  got = (nodes, len(own), c1, len(kept), c2, sum(x[3] for x in lay), sum(x[2] for x in lay))
  return lanes_ok and got == GROUP_LOG[g], dict(zip(("nodes", "cores", "sum_c1", "kept", "sum_c2", "batches",
                                                     "groups"), got))


OPS = [0]

class W(int):
  pass

def _op(f):
  def g(a, b=None):
    OPS[0] += 1
    return W(f(int(a)) if b is None else f(int(a), int(b)))
  return g

for _n, _f in (("xor", int.__xor__), ("and", int.__and__), ("or", int.__or__), ("lshift", int.__lshift__),
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

def fld(w, s, m):
  return (w >> s if s else w) & m

def gstep(H, base, DL):
  f, a, o, m, ins = H
  j = load(f[0])
  st()
  f[0] = 0
  if test(j == len(a)):
    return False
  r = j << 5
  aj, oj = load(a[j]), load(o[j])
  old = load(ins[j][int(r + aj) & 31])
  aj = aj + oj
  st()
  a[j] = int(aj)
  nw = load(ins[j][int(r + aj) & 31])
  d = (r + (old ^ nw)) << 3
  dl = DL[j][int(d) >> 3 & 31]
  for i in range(len(base)):
    base[i] = base[i] ^ load(dl[i])
  mj = load(m[j])
  if test(aj == 0) or test(aj == mj - 1):
    o[j] = int(W(0) - oj)
    st()
    f[j] = int(load(f[int(j + 1)]))
    st()
    f[j + 1] = int(j + 1)
    st()
  return True

def gray_init(ms):
  n = len(ms)
  return [list(range(n + 1)), [0] * n, [1] * n, ms, None]

EQS = [(1, 2, 8, 1), (1, 2, 16, 1), (1, 2, 3, 0), (1, 2, 5, 1), (1, 17, 4, 1), (1, 17, 16, 0), (0, 0, 2, 0),
   (0, 0, 16, 1), (0, 2, 2, 1), (0, 2, 8, 0), (2, 21, 2, 1), (2, 21, 8, 0), (2, 61, 2, 0), (2, 61, 16, 1),
   (3, 17, 4, 1), (3, 17, 16, 0), (3, 61, 2, 0), (3, 61, 16, 1), (4, 0, 2, 1), (4, 0, 8, 1), (4, 0, 17, 0),
   (4, 21, 2, 0), (4, 21, 8, 0), (4, 21, 16, 1)]
BETA2 = [0x1, 0, 0x4, 0, 0, 0x4, 0x4, 0x4, 0x20000, 0, 0x2000000000000000, 0, 0x200000, 0, 0,
    0x2000000000000000, 0, 0, 0x20000, 0, 0x200001, 0, 0x200000, 0, 0x1]
ALPHA3_BITS = (0, 130, 450, 529, 701, 789, 1021, 1169, 1280, 1429)
CERT_A = bytes.fromhex(
  "596c1eb8c532269112fb3a27efabf03448de94ffc28d41fe76deb6d001dcb72cdd90391bfe9962ccd17deffd3a2368d37a6ff7cb4b"
  "17963f9fee9d0652da52bd155d5f257573acd09933fd445dfdc411d659b6c4f7dbe37637289f4ee2dd1116a959c18fad016ec5b4"
  "5031f6100c30e2dd08f5e007e2494b7c7ec6552f452e0c16273ef8b5a121")

def eqs_ok():
  a3 = [0] * 25
  for b in ALPHA3_BITS:
    a3[b >> 6] |= 1 << (b & 63)
  good = True
  for (y, z), d in rows_of([64 * i + z for i in range(25) for z in range(64) if (BETA2[i] >> z) & 1]):
    o = sum(((a3[x + 5 * y] >> z) & 1) << x for x in range(5))
    V = [v for v in range(32) if CHI5[v] ^ CHI5[v ^ d] == o]
    E = [(m, c) for (yy, zz, m, c) in EQS if (yy, zz) == (y, z)]
    sat = [v for v in range(32) if all(bin(m & v).count("1") % 2 == c for (m, c) in E)]
    good = good and len(V) == DDT[d][o] and sat == V
  return good and len(EQS) == 24

def src(X, Y, z):
  xs = (3 * (Y - 3 * X)) % 5
  return xs, X, (z - RHO[xs + 5 * X]) % 64

U = sorted({(X, y, z) for (y, z, m, c) in EQS for X in range(5) if (m >> X) & 1})
UB = {k: src(*k) for k in U}
C1 = {c for (xs, ys, k) in UB.values() for c in (((xs - 1) % 5, k), ((xs + 1) % 5, (k - 1) % 64))}
BD = set(UB.values())
BN = BD | {(x, y, k) for (x, k) in C1 for y in range(5)}
EN = {((x + d) % 5, y, k) for (x, y, k) in BN for d in range(3)}
AN = {k: src(*k) for k in EN}
ANS = set(AN.values())

def e_setup(v0, basis):
  pat = [0] * 1600
  for p in range(256):
    x = 0
    for j in range(8):
      if (p >> j) & 1:
        x ^= basis[j]
    for i in range(1600):
      if (x >> i) & 1:
        pat[i] |= 1 << p

  def rowc(y, z, v):
    X = [pat[64 * (x + 5 * y) + z] ^ (ONES if (v >> x) & 1 else 0) for x in range(5)]
    return [X[x] ^ ((X[(x + 1) % 5] ^ ONES) & X[(x + 2) % 5]) ^ (ONES if y == z == x == 0 else 0)
            for x in range(5)]

  def TP(z, h, v):
    a, b = rowc(2 * h, z, v & 31), rowc(2 * h + 1, z, v >> 5)
    return [a[x] ^ b[x] for x in range(5)] + a + b

  def packed(s):
    w = [0] * 12
    for z in range(64):
      v = [sum(((s >> (64 * (x + 5 * y) + z)) & 1) << x for x in range(5)) for y in range(5)]
      for f, val in ((0, (v[0] | v[1] << 5) << 4), (1, (v[2] | v[3] << 5) << 4), (2, v[4] << 3)):
        w[(3 * z + f) // 16] |= val << (16 * ((3 * z + f) % 16))
    return w
  return (TP, rowc), packed(v0), [packed(basis[j]) for j in range(8, 32)]

def e_batch(T0, base):
  TP, rowc = T0
  mem = {}

  def slice_a(z):
    f = [fld(base[(3 * z + i) // 16], 16 * ((3 * z + i) % 16), 0xF8 if i == 2 else 0x3FF0) for i in range(3)]
    e01, e23, e4 = TP(z, 0, int(f[0]) >> 4), TP(z, 1, int(f[1]) >> 4), rowc(4, z, int(f[2]) >> 3)
    P01, P23, a4 = [load(e01[x]) for x in range(5)], [load(e23[x]) for x in range(5)], [load(w) for w in e4]
    return (e01, e23, a4), [P01[x] ^ P23[x] ^ a4[x] for x in range(5)]
  _, Cp = slice_a(63)
  for z in range(64):
    (e01, e23, a4), C = slice_a(z)
    for x in range(5):
      ys = [y for y in range(5) if (x, y, z) in ANS]
      if ys:
        D = C[(x - 1) % 5] ^ Cp[(x + 1) % 5]
        for y in ys:
          a = a4[x] if y == 4 else load((e01, e23)[y // 2][5 + 5 * (y % 2) + x])
          mem[(x, y, z)] = a ^ D
          st()
    Cp = C
  for k in range(64):
    e = {(X, Y): load(mem[AN[(X, Y, z)]]) for (X, Y, z) in sorted(EN) if z == k}
    b = {}
    for (x, y, z) in sorted(BN):
      if z == k:
        b[(x, y)] = e[(x, y)] ^ (~e[((x + 1) % 5, y)] & e[((x + 2) % 5, y)])
        if x == y == 0 and (0x8082 >> k) & 1:
          b[(x, y)] = ~b[(x, y)]
    for x in range(5):
      if (x, k) in C1:
        mem[("C", x, k)] = b[(x, 0)] ^ b[(x, 1)] ^ b[(x, 2)] ^ b[(x, 3)] ^ b[(x, 4)]
        st()
    for (x, y), w in b.items():
      if (x, y, k) in BD:
        mem[("B", x, y, k)] = w
        st()
  u = {}
  for key in U:
    xs, ys, k = UB[key]
    u[key] = load(mem[("B", xs, ys, k)]) ^ load(mem[("C", (xs - 1) % 5, k)]) ^ load(mem[("C", (xs + 1) % 5, (k - 1) % 64)])
  eqw, ok = [], None
  for (y, z, m, c) in EQS:
    v = None
    for X in range(5):
      if (m >> X) & 1:
        v = u[(X, y, z)] if v is None else v ^ u[(X, y, z)]
    v = v if c else ~v
    eqw.append(int(v))
    ok = v if ok is None else ok & v
  test(ok != 0)
  return eqw, int(ok)

def e_control(m, base, DL):
  m = m + 1
  low = m & (W(0) - m)
  lo, hi = 0, 32
  while hi - lo > 1:
    mid = (lo + hi) // 2
    if test(low >= (1 << mid)):
      lo = mid
    else:
      hi = mid
  dl = DL[lo]
  W(lo) << 4
  for i in range(12):
    base[i] = base[i] ^ load(dl[i])
  test(m < 1 << 24)
  return m, 8 + lo

def e_plain(x):
  A = [(x >> (64 * i)) & M64 for i in range(25)]
  a = chi(A)
  a[0] ^= 1
  b = chi(L(a))
  b[0] ^= 0x8082
  u = L(b)
  return [int(bin(m & sum(((u[xx + 5 * y] >> z) & 1) << xx for xx in range(5))).count("1") % 2 == c)
          for (y, z, m, c) in EQS]

def e_trial(seed):
  s = hashlib.shake_256(seed).digest(200 * 33)
  basis = [int.from_bytes(s[200 * i:200 * i + 200], "little") for i in range(32)]
  p = s[-1]
  x = 0
  for i, w in enumerate(L([int.from_bytes((CERT_A + b"\x86" + bytes(65))[8 * i:8 * i + 8], "little")
                           for i in range(25)])):
    x |= w << (64 * i)
  v0 = x
  for j in range(8):
    if (p >> j) & 1:
      v0 ^= basis[j]
  T0, base, DL = e_setup(v0, basis)
  base = [W(w) for w in base]
  OPS[0] = 0
  eqw, ok = e_batch(T0, base)
  n1 = OPS[0]
  OPS[0] = 0
  e_control(W(int.from_bytes(s[:3], "little") & 0x7FFFFF), base, DL)
  n2 = OPS[0]
  good = n1 == E_BATCH and n2 == E_CTRL and (ok >> p) & 1 == 1
  for q in range(0, 256, 3) if seed[-1] & 1 else range(1, 256, 3):
    xq = v0
    for j in range(8):
      if (q >> j) & 1:
        xq ^= basis[j]
    good = good and e_plain(xq) == [(w >> q) & 1 for w in eqw]
  return good, {"ops": n1, "ctrl": n2, "pass_bits": bin(ok).count("1")}

E_BATCH = 6072
E_CTRL = 40

TRI = [(3 * t, 3 * t + 1, 3 * t + 2) for t in range(106)] + [(318, 319)]

def rowv(s, r):
  return sum(((s >> (64 * (x + 5 * (r // 64)) + r % 64)) & 1) << x for x in range(5))

def t3_packed(s):
  w = [0] * 7
  for t, rs in enumerate(TRI):
    w[t // 16] |= sum(rowv(s, r) << (5 * i) for i, r in enumerate(rs)) << (16 * (t % 16))
  return w

class T3Group:
  def __init__(s, IV):
    pat = [0] * 1600
    for p, v in enumerate(IV):
      for i in range(1600):
        if (v >> i) & 1:
          pat[i] |= 1 << p
    s.act = [[0] * 32 for _ in range(320)]
    for r in range(320):
      for v in range(32):
        a = 0
        for x in range(5):
          a |= pat[64 * (x + 5 * (r // 64)) + r % 64] ^ (ONES if (v >> x) & 1 else 0)
        s.act[r][v] = a
    s.valid = (1 << len(IV)) - 1

  def tab(s, t, v):
    a = [s.act[r][(v >> (5 * i)) & 31] for i, r in enumerate(TRI[t])] + [0]
    return a[0] ^ a[1] ^ a[2], (a[0] & a[1]) | (a[2] & (a[0] ^ a[1]))

def t3_cmp(bits, tau):
  if test(tau >= 512):
    return W(ONES)
  gt, eq = W(0), W(ONES)
  for i in range(8, -1, -1):
    if test(fld(tau, i, 1) == 1):
      eq = eq & bits[i]
    else:
      gt = gt | (eq & bits[i])
      eq = eq & ~bits[i]
  return ~gt

def t3_batch(grp, base, T, ctr):
  ctr = ctr + 1
  test(ctr > 5679328446)
  tau = W(T) >> 1
  lv = [[] for _ in range(10)]

  def push(w, x):
    lv[w].append(x)
    if len(lv[w]) == 3:
      a, b, c = lv[w]
      t = a ^ b
      lv[w] = [t ^ c]
      push(w + 1, (a & b) | (t & c))
  for t in range(107):
    v = int(fld(base[t // 16], 16 * (t % 16), 0x7FFF))
    S, C = grp.tab(t, v)
    push(0, load(S))
    push(1, load(C))
  for w in range(10):
    if len(lv[w]) == 2:
      a, b = lv[w]
      lv[w] = [a ^ b]
      push(w + 1, a & b)
  bits = [lv[w][0] if lv[w] else W(0) for w in range(9)]
  ps = t3_cmp(bits, tau) & grp.valid
  test(ps != 0)
  return int(ps), [int(b) for b in bits]

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

def gray_walk(ms, steps):
  H = gray_init(ms)
  for _ in range(steps):
    j = H[0][0]
    H[0][0] = 0
    if j == len(ms):
      break
    H[1][j] += H[2][j]
    if H[1][j] in (0, ms[j] - 1):
      H[2][j] = -H[2][j]
      H[0][j] = H[0][j + 1]
      H[0][j + 1] = j + 1
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

def act(s, R=320):
  A = [(s >> (64 * i)) & M64 for i in range(25)]
  return sum(bin((A[5 * y] | A[5 * y + 1] | A[5 * y + 2] | A[5 * y + 3] | A[5 * y + 4]) &
                 ((1 << max(0, min(64, R - 64 * y))) - 1)).count("1") for y in range(5))

def t3_trial(seed):
  h = hashlib.sha256(seed).digest()
  rows, ins, LI = core_tables(ALPHA3_BITS)
  ms = [len(v) for v in ins]
  k, g, G, _ = inner(ms)
  gam = h[0] % G
  P = math.prod(ms[:k])
  gl = min(g, ms[k] - gam * g)
  IV = []
  for sl in range(P * gl):
    v, r = 0, sl
    for j in range(k):
      v ^= LI[j][ins[j][r % ms[j]]]
      r //= ms[j]
    IV.append(v ^ LI[k][ins[k][gam * g + r]])
  if gam not in CACHE:
    CACHE[gam] = T3Group(IV)
  grp = CACHE[gam]
  oms = ms[k + 1:]
  H = gray_walk(oms, int.from_bytes(h[1:4], "little") % 5000)
  H[4] = [ins[k + 1 + j] for j in range(len(oms))]
  if "DL" not in CACHE:
    CACHE["DL"] = [[[W(w) for w in t3_packed(LI[k + 1 + j][d])] for d in range(32)] for j in range(len(oms))]
  DL = CACHE["DL"]
  def outer(a):
    v = 0
    for j, aj in enumerate(a):
      v ^= LI[k + 1 + j][ins[k + 1 + j][aj]]
    return v
  base = [W(w) for w in t3_packed(outer(H[1]))]
  ok, worst = True, 0
  for step in range(4):
    ob = outer(H[1])
    asv = [act(ob ^ v) for v in IV]
    T = (1 << 30, 2 * min(asv), 2 * min(asv) - 1, 127, h[5 + step] * 3)[(h[4] + step) % 5]
    OPS[0] = 0
    ps, bits = t3_batch(grp, base, T, W(0))
    gstep(H, base, DL)
    worst = max(worst, OPS[0])
    got = [sum(((bits[i] >> p) & 1) << i for i in range(9)) for p in range(len(IV))]
    ok = ok and got == asv and OPS[0] <= T3_BATCH
    ok = ok and ps == sum((a <= T >> 1) << p for p, a in enumerate(asv))
    ok = ok and [int(w) for w in base] == t3_packed(outer(H[1]))
  cm, zb = 0, 0
  for tau in range(513):
    OPS[0] = 0
    t3_cmp([W(0)] * 9, W(tau))
    cm = max(cm, OPS[0])
    OPS[0] = 0
    t3_batch(ZG, [W(0)] * 7, 2 * tau, W(0))
    zb = max(zb, OPS[0])
  H = gray_init([2])
  H[4] = [range(32)]
  OPS[0] = 0
  gstep(H, [W(0)] * 7, [[[0] * 7] * 32])
  return ok and cm == T3_CMP and zb + OPS[0] == T3_BATCH, {"ops_max": worst, "cmp_max": cm, "batch_max": zb,
                                                           "gray_max": OPS[0]}

class ZG:
  valid = ONES

  def tab(t, v):
    return 0, 0

T3_CMP = 74
T3_BATCH = 1583

def t2_leaf(base, BAD2, ctr):
  ctr = ctr + 1
  test(ctr > 1639088128)
  bad = W(0)
  for q in range(32):
    bad = bad | load(BAD2[int(fld(base[q // 16], 16 * (q % 16), 0x3FF))])
  if test(bad == 0):
    st()
  return int(bad) == 0

def t2_trial(seed):
  h = hashlib.sha256(seed).digest()
  rows = rows_of([FWD[b] for b in ALPHA3_BITS])
  outs = [[o for o in range(32) if DDT[d][o]] for (_, d) in rows]
  def plane0(A):
    v = L(A)[:5]
    w = [0, 0]
    for z in range(64):
      w[z // 32] |= sum(((v[x] >> z) & 1) << x for x in range(5)) << (16 * (z // 2 % 16) + 5 * (z % 2))
    return w
  def alpha4(a):
    A = [0] * 25
    for j, aj in enumerate(a):
      (y, z), _ = rows[j]
      B = one_row(y, z, outs[j][aj])
      A = [A[i] ^ B[i] for i in range(25)]
    return A
  BAD2 = [int(not (ALLOW >> (v & 31)) & 1 or not (ALLOW >> (v >> 5)) & 1) for v in range(1024)]
  ms = [len(o) for o in outs]
  H = gray_walk(ms, int.from_bytes(h[:3], "little") % 20000)
  H[4] = outs
  DL = [{d: [W(w) for w in plane0(one_row(y, z, d))] for d in range(32)} for ((y, z), _) in rows]
  base = [W(w) for w in plane0(alpha4(H[1]))]
  ok, worst = True, 0
  for _ in range(3):
    v = L(alpha4(H[1]))[:5]
    plain = all((ALLOW >> sum(((v[x] >> z) & 1) << x for x in range(5))) & 1 for z in range(64))
    OPS[0] = 0
    kept = t2_leaf(base, BAD2, W(0))
    gstep(H, base, DL)
    worst = max(worst, OPS[0])
    ok = ok and kept == plain and [int(w) for w in base] == plane0(alpha4(H[1])) and OPS[0] <= T2_LEAF
  return ok, {"ops_max": worst}

T2_LEAF = 166

def rows_for(mode, trials):
  out = [(None, {}) for _ in trials]
  if mode.startswith("r5-trail-"):
    ok, obs = trail_group(int(mode[9:]))
    out[0] = (SENTINEL if ok else None, obs)
  elif mode == "r5-count" and eqs_ok():
    for t, tr in enumerate(trials[:24]):
      sd = bytes.fromhex(tr["seed"])
      ok, obs = (e_trial, t3_trial, t2_trial)[t % 3](sd)
      out[t] = (SENTINEL if ok else FAIL_PAIR, obs)
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
