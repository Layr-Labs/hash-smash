"""v8 experiments (proof 2.1, 2.4, 6).  r5-trail-g: P's counts for the start lanes of group g (T1 nodes per
lane; for the cores owned by the group: C1, P45 > 0, C2) against GROUP_LOG.  r5-ecount: counted programs of
E's stage 1 and of one T3 pass.  PASS/FAIL sentinels as in r5_connector.py."""
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
ALLOW = sum(1 << q for q in range(32) if DDT[q][0] + DDT[q][16])   # digest-plane rows with PZ > 0

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
  """T1 from bit (lane, z = 0): at a node, branch on the 5 bits of the smallest odd alpha-column, else of the
  smallest odd beta-column; a node with no odd column is a core (canonical form).  Returns (nodes, cores)."""
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
  """P45 > 0 iff some alpha4 compatible with beta3 makes every digest-plane row of L(alpha4) a row q with
  DDT[q][0] + DDT[q][16] > 0 (T2's sum has only nonnegative terms).  Rows of beta3 are assigned in order;
  a digest-plane position is checked once no later row can change it."""
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

  dead = set()          # (k, v on the positions rows k.. can change): known to fail; the rest is checked

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

# The executed run of P (October 6; proof 2.1): nodes per start lane, and per group (nodes, cores owned,
# sum C1 over them, cores with P45 > 0, sum C2 over those).  A core is owned by the group of its smallest lane.
LANE_NODES = [345923, 346741, 347335, 347245, 346861, 346213, 348343, 346483, 347031, 348147, 347363, 346239,
       346119, 346755, 347715, 346837, 347449, 346491, 346881, 346221, 346885, 347921, 346649, 347657, 347329]
GROUPS = [(0, 1), (2, 3, 4, 5, 6, 7), tuple(range(8, 17)), tuple(range(17, 25))]
GROUP_LOG = [(692664, 1023, 974737408, 204, 608900651514), (2082480, 646, 600711168, 251, 735420810384),
      (3123655, 72, 63639552, 12, 34953937452), (2776034, 0, 0, 0, 0)]  # lanes 8..24 logged as one group
# totals: 8,674,833 nodes; 1741 cores; sum C1 = 1,639,088,128; 467 cores with P45 > 0; sum C2 = 1,379,275,399,350

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
  got = (nodes, len(own), c1, len(kept), c2)
  return lanes_ok and got == GROUP_LOG[g], {"nodes": nodes, "cores": len(own), "sum_c1": c1,
                      "kept": len(kept), "sum_c2": c2}

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
  """comparison + conditional branch (2 primitives); FORCE[0] = k forces the first k tests to pass."""
  OPS[0] += 2
  if FORCE[0] is not None:
    FORCE[0] -= 1
    return FORCE[0] >= 0
  return cond

def crot(v, r):
  return ((v << r) | (v >> (64 - r))) & M64 if r else v

def cchi(a, rc):
  o = [a[x + 5 * y] ^ ((~a[(x + 1) % 5 + 5 * y]) & a[(x + 2) % 5 + 5 * y]) for y in range(5) for x in range(5)]
  o[0] = o[0] ^ rc
  return o

def cround1(a):
  C = [a[x] ^ a[x + 5] ^ a[x + 10] ^ a[x + 15] ^ a[x + 20] for x in range(5)]
  D = [C[(x - 1) % 5] ^ crot(C[(x + 1) % 5], 1) for x in range(5)]
  e = [None] * 25
  for y in range(5):
    for x in range(5):
      e[y + 5 * ((2 * x + 3 * y) % 5)] = crot(a[x + 5 * y] ^ D[x], RHO[x + 5 * y])
  return cchi(e, RC1)

# The 24 equations <m, u_row> = c of the 10 round-2 rows (u = L(b), b = round-1 output), in the early-abort
# order: row (1,2) = row 66 first, then row (1,17) = row 81 (order of Th0rgal 7deb1595), then the others.
EQS = [(1, 2, 8, 1), (1, 2, 16, 1), (1, 2, 3, 0), (1, 2, 5, 1), (1, 17, 4, 1), (1, 17, 16, 0), (0, 0, 2, 0),
   (0, 0, 16, 1), (0, 2, 2, 1), (0, 2, 8, 0), (2, 21, 2, 1), (2, 21, 8, 0), (2, 61, 2, 0), (2, 61, 16, 1),
   (3, 17, 4, 1), (3, 17, 16, 0), (3, 61, 2, 0), (3, 61, 16, 1), (4, 0, 2, 1), (4, 0, 8, 1), (4, 0, 17, 0),
   (4, 21, 2, 0), (4, 21, 8, 0), (4, 21, 16, 1)]
COST = [384, 400, 418, 427, 435, 443, 451, 459, 467, 475, 483, 491, 499, 507, 515, 523, 531, 539, 547, 555, 569,
    577, 585, 593, 593]                     # primitives of stage 1 by exit (24 = all equations hold)
BLOCK = 15                                      # loop control per block of 16 unrolled Gray steps
T3_STEP = 1750                                  # T3: one pass, 9 leaves + Gray step (proof 2.1; charged 9 x 256)
BETA2 = [0x1, 0, 0x4, 0, 0, 0x4, 0x4, 0x4, 0x20000, 0, 0x2000000000000000, 0, 0x200000, 0, 0,
    0x2000000000000000, 0, 0, 0x20000, 0, 0x200001, 0, 0x200000, 0, 0x1]
ALPHA3_BITS = (0, 130, 450, 529, 701, 789, 1021, 1169, 1280, 1429)

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

def stage1(xr, bj):
  """x ^= b_j (25 loads, 25 XOR), round 0 (chi, iota), round 1, then each equation from the bits of
  u = L(b) it needs: bit u[X,Y,z] = b[i] >> k ^ C[xs-1] >> k ^ C[xs+1] >> (k-1) (bit 0), with lane i = xs + 5ys
  the rho-pi source of (X, Y), k = z - rho_i mod 64, and column parities C of b computed on first use."""
  for i in range(25):
    xr[i] = xr[i] ^ load(bj[i])
  b = cround1(cchi(xr, RC0))
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

def block_control(m, end):
  """Control of one block of 16 unrolled Gray steps: m += 1; the step at the block boundary flips basis
  vector 4 + ctz(m), found from m & -m by a 5-level comparison tree; loop test."""
  m = m + 1
  low = m & (0 - m)
  j, lo, hi = 4, 0, 32
  while hi - lo > 1:
    mid = (lo + hi) // 2
    if test(low >= (1 << mid)):
      lo = mid
    else:
      hi = mid
  test(m < end)
  return m, 4 + lo

def ecount_trial(seed, k=None):
  st = hashlib.shake_256(seed).digest(400)
  x = [int.from_bytes(st[8 * i:8 * i + 8], "little") for i in range(25)]
  bj = [int.from_bytes(st[200 + 8 * i:208 + 8 * i], "little") for i in range(25)]
  xr = [W(v) for v in x]
  OPS[0], FORCE[0] = 0, k
  ex, b = stage1(xr, bj)
  ops = OPS[0]
  FORCE[0] = None
  if k is not None:
    return ex == k and ops == COST[k], {"exit": ex, "ops": ops}
  a = chi([x[i] ^ bj[i] for i in range(25)])
  a[0] ^= RC0
  ref = chi(L(a))
  ref[0] ^= RC1
  u, kk = L(ref), 0
  for (y, z, m, c) in EQS:
    row = sum(((u[x + 5 * y] >> z) & 1) << x for x in range(5))
    if bin(m & row).count("1") % 2 != c:
      break
    kk += 1
  return [int(v) for v in b] == ref and ex == kk and ops == COST[ex], {"exit": ex, "ops": ops}

def st(v):
  """store (1 primitive)"""
  OPS[0] += 1
  return v

def popc(v):
  """64-bit popcount, 17 primitives (no multiply)"""
  v = v - ((v >> 1) & 0x5555555555555555)
  v = (v & 0x3333333333333333) + ((v >> 2) & 0x3333333333333333)
  v = (v + (v >> 4)) & 0x0F0F0F0F0F0F0F0F
  v = v + (v >> 8)
  v = v + (v >> 16)
  v = v + (v >> 32)
  return v & 127

def t3_step(seed, m0=9):
  """One pass of T3's loop (trail3c.cpp), counted: step counters and T, m0 leaves on the longest non-full
  path (5 planes), the Gray step's longest branch.  alpha2 (al), T, loop variables in registers; arrays
  loaded.  AS per leaf and the alpha2 update are checked against a plain evaluation."""
  s = hashlib.shake_256(seed).digest(200 * (m0 + 1))
  wd = [int.from_bytes(s[8 * i:8 * i + 8], "little") for i in range(25 * (m0 + 1))]
  L0, LI, al = [wd[25 * k:25 * k + 25] for k in range(m0)], wd[25 * m0:], [W(v) for v in wd[:25]]
  ref = [sum(len({z for x in range(5) for z in range(64) if (wd[5 * y + x] ^ l[5 * y + x]) >> z & 1})
             for y in range(5)) for l in L0]
  OPS[0], got = 0, []
  st(load(0) + m0)                                  # leaves += m0
  test(st(load(0) + m0) > 1 << 50)                  # gleaves += m0, cap test
  T = load(1 << 20)                                 # T = min(bw1, gbest)
  test(load(1 << 20) < T)
  k, p = W(0), W(0)
  for l0 in L0:
    a = W(0) ^ 0
    for y in range(5):
      v = al[5 * y] ^ load(l0[5 * y])
      for x in range(1, 5):
        v = v | (al[5 * y + x] ^ load(l0[5 * y + x]))
      a = a + popc(v)
      test((a << 1) > T)
    test(W(5) < 5)                                  # if (y < 5) continue
    got.append(int(a))
    p, k = p + 200, k + 1
    test(k < m0)
  j = load(0)                                       # Gray step: j = f[0]; f[0] = 0; j == n1?
  st(0)
  test(j == 7)
  aj = load(j + 1)
  old = load(((j + 1) << 5) + aj)
  aj = aj + load(j + 2)
  st(aj)
  nw = load(((j + 1) << 5) + aj)
  q = (((j + 1) << 5) + (old ^ nw)) << 8            # address of LI[j+1][old ^ nw]
  al = [al[i] ^ load(LI[i]) for i in range(25)]
  ro = load(j + 3)
  load(0) + (load((nw << 5) + ro) - load((old << 5) + ro))    # w2o update
  mj = load(j + 4)
  test(aj == 0)
  test(aj == mj - 1)                                # longest branch: flip o[j], f[j] = f[j+1], f[j+1] = j+1
  st(0 - load(j + 5))
  st(load(j + 6))
  st(j + 1)
  ok = got == ref and [int(v) for v in al] == [wd[i] ^ LI[i] for i in range(25)] and q >= 0
  return ok, OPS[0]

def rows_for(mode, trials):
  out = [(None, {}) for _ in trials]
  if mode.startswith("r5-trail-"):
    ok, obs = trail_group(int(mode[9:]))
    out[0] = (SENTINEL if ok else None, obs)
  elif mode == "r5-ecount" and eqs_ok():
    OPS[0] = 0
    m, js = W(0), []
    for _ in range(16):
      m, j = block_control(m, 1 << 28)
      js.append(j)
    ctl = OPS[0]
    for t, tr in enumerate(trials):
      if t < 64:
        ok, obs = ecount_trial(bytes.fromhex(tr["seed"]))
      elif t < 89:
        ok, obs = ecount_trial(b"forced", t - 64)
      elif t == 89:
        ok, obs = ctl == 16 * BLOCK and js == [4, 5, 4, 6, 4, 5, 4, 7, 4, 5, 4, 6, 4, 5, 4, 8], {"ops": ctl}
      elif t < 92:
        ok, n = t3_step(bytes.fromhex(tr["seed"]))
        ok, obs = ok and n == T3_STEP and n <= 9 * 256, {"ops": n}
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
