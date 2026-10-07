"""Experiments (proof 2.1, 2.1a, 2.4, 4.5, 6): r5-trail-g, r5-ecount (trials 90, 100: T3 on two cores)."""
import hashlib
import json
import math
import sys
RHO = (0, 1, 62, 28, 27, 36, 44, 6, 55, 20, 3, 10, 43, 25, 39, 41, 45, 15, 21, 8, 18, 2, 61, 56, 14)
RC0, RC1 = 0x1, 0x8082
M64 = (1 << 64) - 1
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
ALLOW = sum(1 << q for q in range(32) if DDT[q][0] + DDT[q][16])  # digest-plane rows with PZ > 0
def rot(v, a):
  return ((v << a) | (v >> (64 - a))) & M64 if a % 64 else v
def L(A):
  """pi o rho o theta on 25 lanes."""
  P = [A[x] ^ A[x + 5] ^ A[x + 10] ^ A[x + 15] ^ A[x + 20] for x in range(5)]
  T = [P[(x - 1) % 5] ^ rot(P[(x + 1) % 5], 1) for x in range(5)]
  B = [0] * 25
  for y in range(5):
    for x in range(5):
      B[y + 5 * ((2 * x + 3 * y) % 5)] = rot(A[x + 5 * y] ^ T[x], RHO[x + 5 * y])
  return B
def chi(A):
  return [A[x + 5 * y] ^ (~A[(x + 1) % 5 + 5 * y] & A[(x + 2) % 5 + 5 * y]) for y in range(5) for x in range(5)]
# -- P, stage T1 (proof 2.1)
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
  """T1 from bit (lane, z = 0) (proof 2.1).  Returns (nodes, cores)."""
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
  """P45 > 0 iff some alpha4 compatible with beta3 has every digest-plane row q of L(alpha4) in ALLOW."""
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
# P's log (proof 2.1): nodes per lane; per group (nodes, cores owned, sum C1, cores with P45 > 0, sum C2)
LANE_NODES = [345923, 346741, 347335, 347245, 346861, 346213, 348343, 346483, 347031, 348147, 347363, 346239,
       346119, 346755, 347715, 346837, 347449, 346491, 346881, 346221, 346885, 347921, 346649, 347657, 347329]
GROUPS = [(0, 1), (2, 3, 4, 5, 6, 7), tuple(range(8, 17)), tuple(range(17, 25))]
GROUP_LOG = [(692664, 1023, 974737408, 204, 608900651514, 1374952320), (2082480, 646, 600711168, 251, 735420810384,
      1660673664), (3123655, 72, 63639552, 12, 34953937452, 77262336), (2776034, 0, 0, 0, 0, 0)]  # lanes 8..24 logged as one group
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
  e3 = sum(64 * sum(math.prod(NIN[o] for _, o in r[s]) for s in (slice((len(r) + 1) // 2), slice((len(r) + 1) // 2, 99)))
       for r in map(rows_of, kept))  # T3 half-list entries
  got = (nodes, len(own), c1, len(kept), c2, e3)
  return lanes_ok and got == GROUP_LOG[g], {"nodes": nodes, "cores": len(own), "sum_c1": c1,
                      "kept": len(kept), "sum_c2": c2, "sum_e3": e3}
# -- E, stage 1, counted (proof 2.4, 6)
OPS = [0]
class W(int):
  """A 256-bit register value; every operator below counts one primitive."""
def _op(f):
  def g(a, b=None):
    OPS[0] += 1
    return W(f(int(a)) if b is None else f(int(a), int(b)))
  return g
for _n, _f in (("xor", int.__xor__), ("and", int.__and__), ("or", int.__or__), ("lshift", int.__lshift__),
       ("rshift", int.__rshift__), ("add", int.__add__), ("sub", int.__sub__), ("rsub", lambda a, b: b - a)):
  setattr(W, "__%s__" % _n, _op(_f))
W.__invert__ = _op(int.__invert__)
FORCE = [None]
def load(v):
  OPS[0] += 1
  return W(v)
def test(cond):
  """compare + branch (2 primitives); FORCE[0] = k: the first k tests pass."""
  OPS[0] += 2
  if FORCE[0] is not None:
    FORCE[0] -= 1
    return FORCE[0] >= 0
  return cond
def cchi(a, rc):
  o = [a[x + 5 * y] ^ ((~a[(x + 1) % 5 + 5 * y]) & a[(x + 2) % 5 + 5 * y]) for y in range(5) for x in range(5)]
  o[0] = o[0] ^ rc
  return o
# The 24 round-2 row equations in early-abort order (row 66, then row 81; proof 2.4)
EQS = [(1, 2, 8, 1), (1, 2, 16, 1), (1, 2, 3, 0), (1, 2, 5, 1), (1, 17, 4, 1), (1, 17, 16, 0), (0, 0, 2, 0),
   (0, 0, 16, 1), (0, 2, 2, 1), (0, 2, 8, 0), (2, 21, 2, 1), (2, 21, 8, 0), (2, 61, 2, 0), (2, 61, 16, 1),
   (3, 17, 4, 1), (3, 17, 16, 0), (3, 61, 2, 0), (3, 61, 16, 1), (4, 0, 2, 1), (4, 0, 8, 1), (4, 0, 17, 0),
   (4, 21, 2, 0), (4, 21, 8, 0), (4, 21, 16, 1)]
COST_FES = [217, 233, 251, 260, 268, 276, 284, 292, 300, 308, 316, 324, 332, 340, 348, 356, 364, 372, 380, 388, 402,
    410, 418, 426, 426]  # FES stage 1 by exit
BLOCK_FES = 47  # block of 16 FES steps
FES_JK = [(4, None), (5, None), (4, 5), (6, None), (4, 6), (5, 6), (4, 5), (7, None), (4, 7), (5, 7), (4, 5),
    (6, 7), (4, 6), (5, 6), (4, 5), (8, None)]
BETA2 = [0x1, 0, 0x4, 0, 0, 0x4, 0x4, 0x4, 0x20000, 0, 0x2000000000000000, 0, 0x200000, 0, 0,
    0x2000000000000000, 0, 0, 0x20000, 0, 0x200001, 0, 0x200000, 0, 0x1]
ALPHA3_BITS = (0, 130, 450, 529, 701, 789, 1021, 1169, 1280, 1429)
T3M = ((320, 440, 449, 528, 960, 1080, 1084, 1168, 1404, 1409), 95969)
def eqs_ok():
  """EQS is a basis of the equations of V(beta2_r, alpha3_r) for each of the 10 rows of beta2."""
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
def eqs_from(b):
  C, t = {}, {}
  def col(x):
    if x not in C:
      C[x] = b[x] ^ b[x + 5] ^ b[x + 10] ^ b[x + 15] ^ b[x + 20]
    return C[x]
  def bit(X, Y, z):
    if (X, Y, z) not in t:
      xs, i = (3 * (Y - 3 * X)) % 5, (3 * (Y - 3 * X)) % 5 + 5 * X
      k = (z - RHO[i]) % 64
      v = None
      for (w, s) in ((b[i], k), (col((xs - 1) % 5), k), (col((xs + 1) % 5), (k - 1) % 64)):
        w = w >> s if s else w
        v = w if v is None else v ^ w
      t[(X, Y, z)] = v
    return t[(X, Y, z)]
  for k, (y, z, m, c) in enumerate(EQS):
    v = None
    for X in range(5):
      if (m >> X) & 1:
        v = bit(X, y, z) if v is None else v ^ bit(X, y, z)
    if not test((v & 1) == c):
      return k, b
  return 24, b
# -- E stage 1 by FES (proof 2.4)
def fes_f(p):
  a = chi(p)
  a[0] ^= RC0
  return L(a)
def _x(*v):
  return [_r(w[l] for w in v) for l in range(25)]
def _r(it):
  r = 0
  for w in it:
    r ^= w
  return r
def fes_check(seed, n=10):
  s = hashlib.shake_256(seed).digest(200 * (n + 1))
  wd = [int.from_bytes(s[8 * i:8 * i + 8], "little") for i in range(25 * (n + 1))]
  v0, B = wd[:25], [wd[25 * (i + 1):25 * (i + 2)] for i in range(n)]
  z = fes_f(v0)
  fi = [fes_f(_x(v0, B[i])) for i in range(n)]
  c = [[_x(fes_f(_x(v0, B[i], B[j])), fi[i], fi[j], z) if i != j else None for j in range(n)] for i in range(n)]
  D = [_x(fi[k], z, c[k][k - 1]) if k else _x(fi[0], z) for k in range(n)]
  ok = True
  for t in range(1, 1 << n):
    k1 = (t & -t).bit_length() - 1
    r = t >> (k1 + 1)
    if r:
      D[k1] = _x(D[k1], c[k1][k1 + (r & -r).bit_length()])
    z = _x(z, D[k1])
    g = t ^ (t >> 1)
    ok = ok and z == fes_f(_x(v0, *[B[i] for i in range(n) if (g >> i) & 1]))
  return ok, {"points": 1 << n}
def stage1_fes(zr, Dk, Ck):
  for i in range(25):
    d = load(Dk[i]) ^ load(Ck[i])
    st(d)
    zr[i] = zr[i] ^ d
  return eqs_from(cchi(zr, RC1))
def _tree(low):
  lo, hi = 0, 32
  while hi - lo > 1:
    mid = (lo + hi) // 2
    if test(low >= (1 << mid)):
      lo = mid
    else:
      hi = mid
  return W(lo) + 4
def block_control_fes(m, end):
  """One block of 16 FES steps."""
  m = m + 1
  j, k2 = _tree(m & (0 - m)), None
  m2 = m & (m - 1)
  if not test(m2 == 0):
    k2 = _tree(m2 & (0 - m2))
    (j << 13) + (k2 << 8) + 0
  (j << 8) + 0
  for r in (1, 2, 4, 8):
    (j << 8) + r
  test(m < end)
  return m, int(j), (None if k2 is None else int(k2))
def ecount_fes_trial(seed, k=None):
  s = hashlib.shake_256(b"fes" + seed).digest(600)
  w = [int.from_bytes(s[8 * i:8 * i + 8], "little") for i in range(75)]
  zr = [W(v) for v in w[:25]]
  OPS[0], FORCE[0] = 0, k
  ex, b = stage1_fes(zr, w[25:50], w[50:75])
  ops, FORCE[0] = OPS[0], None
  if k is not None:
    return ex == k and ops == COST_FES[k], {"exit": ex, "ops": ops}
  zn = _x(w[:25], w[25:50], w[50:75])
  ref = chi(zn)
  ref[0] ^= RC1
  u, kk = L(ref), 0
  for (y, z, m, c) in EQS:
    if bin(m & sum(((u[x + 5 * y] >> z) & 1) << x for x in range(5))).count("1") % 2 != c:
      break
    kk += 1
  return [int(v) for v in zr] == zn and [int(v) for v in b] == ref and ex == kk and ops == COST_FES[ex], {
    "exit": ex, "ops": ops}
def st(v):
  """store (1 primitive)"""
  OPS[0] += 1
  return v
# -- P, T3: full w1 evaluations of the output core (proof 2.1a)
# -- P, T3: block meet-in-the-middle (proof 2.1, 2.1a)
BS = {}
def Li(t):
  if not BS:  # L^-1 by elimination
    for i in range(1600):
      v, p = sum(w << 64 * j for j, w in enumerate(L([1 << i % 64 if j == i >> 6 else 0 for j in range(25)]))), 1 << i
      while v.bit_length() in BS:
        v, p = v ^ BS[v.bit_length()][0], p ^ BS[v.bit_length()][1]
      BS[v.bit_length()] = v, p
  p = 0
  while t:
    v, q = BS[t.bit_length()]
    t, p = t ^ v, p ^ q
  return p
pos = lambda r, x: 64 * (x + 5 * (r // 64)) + r % 64  # row r = 64 y + z
cell = lambda r, d: sum((d >> x & 1) << pos(r, x) for x in range(5))
M = sum(M64 << 320 * y for y in range(5))
AS = lambda v: ((v | v >> 64 | v >> 128 | v >> 192 | v >> 256) & M).bit_count()
def t3m(core):
  """T3 on one core: leaves with AS(alpha2) <= 63 (a block of 64 is zero), as matches of half-sums per block."""
  rw = sorted({b // 320 * 64 + b % 64 for b in core})
  ro = [sum((pos(r, x) in core) << x for x in range(5)) for r in rw]
  ins = [[d for d in range(32) if DDT[d][o]] for o in ro]
  LI = [[Li(cell(r, d)) for d in ins[j]] for j, r in enumerate(rw)]
  def half(js):
    out = [(0, ())]
    for j in js:
      out = [(v ^ LI[j][k], c + (k,)) for v, c in out for k in range(len(ins[j]))]
    return out
  h = (len(rw) + 1) // 2
  A, B = half(range(h)), half(range(h, len(rw)))
  hits, nm = set(), 0
  for b in range(64):  # block b: rows 51 r mod 320, 5 b <= r < 5 b + 5
    K, d = sum(cell(51 * r % 320, 31) for r in range(5 * b, 5 * b + 5)), {}
    for i, (v, _) in enumerate(A):
      d.setdefault(v & K, []).append(i)
    for v, c in B:
      for i in d.get(v & K, ()):
        nm += 1
        if AS(A[i][0] ^ v) < 64:
          hits.add(A[i][1] + c)
  return {"leaves": math.prod(map(len, ins)), "entries": 64 * (len(A) + len(B)), "matches": nm, "hits": len(hits)}, hits, rw, ins
def t3cap():
  obs, hits, rw, ins = t3m(ALPHA3_BITS)
  if len(hits) != 1 or obs["matches"] != 52087:
    return False, obs
  c = hits.pop()
  al = sum(cell(r, ins[j][c[j]]) for j, r in enumerate(rw))
  obs["AS"] = AS(Li(al))
  return (obs["AS"] == 59 and al == sum(w << 64 * i for i, w in enumerate(BETA2)) and p45pos(ALPHA3_BITS)
          and canon(ALPHA3_BITS) == ALPHA3_BITS), obs
def rows_for(mode, trials):
  out = [(None, {}) for _ in trials]
  if mode.startswith("r5-trail-"):
    ok, obs = trail_group(int(mode[9:]))
    out[0] = (SENTINEL if ok else None, obs)
  elif mode == "r5-ecount" and eqs_ok():
    for t, tr in enumerate(trials):
      if t < 64:
        ok, obs = ecount_fes_trial(bytes.fromhex(tr["seed"]))
      elif t < 89:
        ok, obs = ecount_fes_trial(b"forced", t - 64)
      elif t == 89:
        OPS[0], m, jk, cs = 0, W(0), [], []
        for _ in range(16):
          o = OPS[0]
          m, j, k2 = block_control_fes(m, 1 << 28)
          jk.append((j, k2))
          cs.append(OPS[0] - o)
        ok, obs = jk == FES_JK and max(cs) == BLOCK_FES, {"ops": max(cs)}
      elif t == 90:  # the core with the most matches; no leaf with AS <= 63
        obs = t3m(T3M[0])[0]
        ok = obs["matches"] == T3M[1] and obs["hits"] == 0
      elif t == 91:
        continue
      elif t < 100:
        ok, obs = fes_check(bytes.fromhex(tr["seed"]), 10)
      elif t == 100:
        ok, obs = t3cap()
      else:
        break
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
