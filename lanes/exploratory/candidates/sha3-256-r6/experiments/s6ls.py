"""S6LS: distinguished-point collision search on sha3-256-r6-prefix-v1, linear-structure message embedding, bit-sliced
step of 256 walks on a machine with a 1,024-word register file (every load, store and move is an instruction).

Chain function on 256-bit points u (little-endian lanes u0..u3):
  m(u) = 128 bytes = lanes 0..15 of the absorbed state: lane 1 = u0, lane 6 = u1, lane 11 = u0^u1^K11,
  lane 4 = u2, lane 9 = u3, lane 14 = u2^u3^K14, the other lanes 0..15 the constants K below; padding gives lane 16 =
  0x8000000000000006.  F(u) = SHA3-256-r6(m(u)) XOR PD (PD a fixed 256-bit mask).  m is injective, so F(u) = F(u') with
  u != u' gives two distinct messages with equal complete digests.
This program regenerates the program of proof.md Section 3 (the same construction as the C generator gen_s6ls.c of
Appendix B, with the polarity pattern and boundary size that the generator selects; the text listing must hash to
LISTING_SHA256, else the program stops), executes it against a plain six-round implementation, and runs
  rho-w22   : the search of proof.md Section 4 at width 22 (planes 22..255 zeroed after each step), one pair per trial;
  proj-w256 : eight chained full-width steps from 256 random points, first pair agreeing on the 22 low digest bits.
One Python integer holds a plane for all trials of the request (trial t in bits 256t..256t+255); trials never interact.
"""
import sys, json, hashlib, heapq

KR = 1018                          # registers for the program (6 more hold the loop state: 1,024)
KB = 975                           # boundary set size (selected by the generator, Section 3.4)
LISTING_SHA256 = "e7fdf75c69a8fee561ce9874b14426d1af59daf2b74c7ef149b22e92613ccadc"
NSTEP = 36863                      # listing lines (GA and GB counted twice) + 19 loop operations; the prefilter adds 15


M64 = (1 << 64) - 1


ALL = (1 << 256) - 1


RC = [0x1, 0x8082, 0x800000000000808A, 0x8000000080008000, 0x808B, 0x80000001]


ROT = [[0, 36, 3, 41, 18], [1, 44, 10, 45, 2], [62, 6, 43, 15, 61], [28, 55, 25, 21, 56], [27, 20, 39, 8, 14]]


Q_FIX = 1336081


PF_K = 16


def xmap(X, Y):
    return (3 * Y + X) % 5


def polarities(q=Q_FIX):
    Q = {(X, Y): (q >> (X + 5 * Y)) & 1 for X in range(5) for Y in range(5)}
    pC = [sum(Q[(X, Y)] for Y in range(5)) % 2 for X in range(5)]
    pD = [(pC[(X - 1) % 5] ^ pC[(X + 1) % 5]) for X in range(5)]
    pT = {(X, Y): Q[(X, Y)] ^ pD[X] for X in range(5) for Y in range(5)}     # stored polarity of T(x=X, y=Y)
    return Q, pC, pD, pT


def plan_row(pB, qwant, need=(0, 1, 2, 3, 4)):
    """Cheapest way to compute the chi outputs X in `need` of one row from stored planes with polarities pB[0..4] so that
    output X has stored polarity qwant[X] (None = any). Returns (cost, S, choices); choices[X] = (v1, v2, op, resinv, qq)."""
    best = None
    for S in range(32):
        cS = bin(S).count('1')
        opts = []
        ok = True
        for X in need:
            o = []
            a, b = (X + 1) % 5, (X + 2) % 5
            for v1 in ((0, 1) if (S >> a) & 1 else (0,)):
                for v2 in ((0, 1) if (S >> b) & 1 else (0,)):
                    p1, p2 = pB[a] ^ v1, pB[b] ^ v2
                    if p1 == p2:
                        continue
                    op, flip = ('and', 0) if p1 == 1 else ('or', 1)
                    for ri in (0, 1):
                        qq = pB[X] ^ flip ^ ri
                        if qwant[X] is None or qq == qwant[X]:
                            o.append((ri, (v1, v2, op, ri, qq)))
            if not o:
                ok = False
                break
            opts.append(o)
        if not ok:
            continue
        c = cS + sum(min(r for r, _ in o) for o in opts)
        if best is None or c < best[0]:
            ch = {}
            for X, o in zip(need, opts):
                m = min(r for r, _ in o)
                ch[X] = [c2 for r, c2 in o if r == m][0]
            best = (c, S, ch)
    return best


class Prog:
    def __init__(self):
        self.ins = []          # (kind, dst, a, b): a/b are vregs (int) or ('i', imm); ld: a = address; st: dst = address, a = vreg
        self.nv = 0

    def new(self):
        self.nv += 1
        return self.nv - 1

    def ld(self, addr):
        d = self.new()
        self.ins.append(('ld', d, addr, None))
        return d

    def st(self, addr, r):
        self.ins.append(('st', addr, r, None))

    def op(self, kind, a, b):
        d = self.new()
        self.ins.append((kind, d, a, b))
        return d

    def xor(self, a, b):
        return self.op('xor', a, b)

    def and_(self, a, b):
        return self.op('and', a, b)

    def or_(self, a, b):
        return self.op('or', a, b)

    def not_(self, a):
        return self.op('xor', a, ('i', ALL))


def chi_row(P, s, pB, plan, need=(0, 1, 2, 3, 4)):
    cost, S, ch = plan
    inv = {j: P.not_(s[j]) for j in range(5) if (S >> j) & 1}
    out = {}
    for X in need:
        v1, v2, op, ri, qq = ch[X]
        a, b = (X + 1) % 5, (X + 2) % 5
        e1 = inv[a] if v1 else s[a]
        e2 = inv[b] if v2 else s[b]
        u = P.and_(e1, e2) if op == 'and' else P.or_(e1, e2)
        if ri:
            u = P.not_(u)
        out[X] = P.xor(s[X], u)
    return out


def addr(buf, lane, z):
    return buf * 1600 + lane * 64 + z


IOTA_Z = (0, 1, 3, 7, 15, 31, 63)


def gen_G(src, dst, q=Q_FIX):
    """One generic round: reads T planes (theta already added, stored polarity pT) from buffer src, writes T' to buffer dst.
    The round constant is a 64-bit word loaded from the RC cell; iota is applied from it at the 7 positions in IOTA_Z."""
    Qp, pC, pD, pT = polarities(q)
    P = Prog()
    plans = []
    for Y in range(5):
        pB = [pT[(xmap(X, Y), X)] for X in range(5)]
        plans.append((pB, plan_row(pB, [Qp[(X, Y)] for X in range(5)])))
    rcv = P.ld(('rc',))
    C0 = None
    Cprev = None
    for z in range(64):
        o = {}
        Cc = [None] * 5
        for Y in range(5):
            s = []
            for X in range(5):
                x = xmap(X, Y)
                s.append(P.ld(addr(src, x + 5 * X, (z - ROT[x][X]) % 64)))
            res = chi_row(P, s, plans[Y][0], plans[Y][1])
            for X in range(5):
                v = res[X]
                if Y == 0 and X == 0 and z in IOTA_Z:           # iota: o ^= -(bit z of RC)
                    m = P.op('shr', rcv, ('i', z))
                    m = P.op('and', m, ('i', 1))
                    m = P.op('sub', m, ('i', 1))                # rcv holds the complement of the round constant: (1 - bit) - 1 = -bit
                    v = P.xor(v, m)
                o[(X, Y)] = v
                Cc[X] = v if Cc[X] is None else P.xor(Cc[X], v)
        if z == 0:
            for (X, Y), v in o.items():
                P.st(addr(dst, X + 5 * Y, 0), v)
            C0 = Cc
        else:
            D = [P.xor(Cc[(X - 1) % 5], Cprev[(X + 1) % 5]) for X in range(5)]   # D[X][z] = C[X-1][z] ^ C[X+1][z-1]
            for (X, Y), v in o.items():
                P.st(addr(dst, X + 5 * Y, z), P.xor(v, D[X]))
        Cprev = Cc
    D = [P.xor(C0[(X - 1) % 5], Cprev[(X + 1) % 5]) for X in range(5)]       # slice 0 last: needs C[.][63]
    for Y in range(5):
        for X in range(5):
            r = P.ld(addr(dst, X + 5 * Y, 0))
            P.st(addr(dst, X + 5 * Y, 0), P.xor(r, D[X]))
    return P


def gen_R5(src, q=Q_FIX, qwant=None, ls=False):
    """Last round: row 0 only, outputs lanes 0..3 into buffer 2 (the input planes of the next step); builds the DP prefilter on lane 3."""
    Qp, pC, pD, pT = polarities(q)
    P = Prog()
    pB = [pT[(xmap(X, 0), X)] for X in range(5)]
    plan = plan_row(pB, (list(qwant) + [None]) if qwant else [None] * 5, need=(0, 1, 2, 3))
    pOut = {X: plan[2][X][4] for X in range(4)}
    pf = None
    for z in range(64):
        s = [P.ld(addr(src, xmap(X, 0) + 5 * X, (z - ROT[xmap(X, 0)][X]) % 64)) for X in range(5)]
        res = chi_row(P, s, pB, plan, need=(0, 1, 2, 3))
        for X in range(4):
            v = res[X]
            if X == 0 and z in (0, 31) and not ls:
                v = P.not_(v)            # iota of round 5 (RC = 0x80000001)
            P.st(addr(2, X, z), v)
            if X == 3 and z < PF_K and not ls:
                pf = v if pf is None else (P.or_(pf, v) if pOut[3] == 0 else P.and_(pf, v))
    return P, pOut, pf


RC_ALL = [0x1, 0x8082, 0x800000000000808A, 0x8000000080008000, 0x808B, 0x80000001, 0x8000000080008081,
          0x8000000000008009, 0x8A, 0x88, 0x80008009, 0x8000000A, 0x8000808B, 0x800000000000008B,
          0x8000000000008089, 0x8000000000008003, 0x8000000000008002, 0x8000000000000080, 0x800A,
          0x800000008000000A, 0x8000000080008081, 0x8000000000008080, 0x80000001, 0x8000000080008008]


def perm(a, rounds):
    """Reference Keccak-f, used only to check the straight-line program and the digests."""
    for rc in RC_ALL[:rounds]:
        c = [a[x] ^ a[x + 5] ^ a[x + 10] ^ a[x + 15] ^ a[x + 20] for x in range(5)]
        d = [c[(x + 4) % 5] ^ (((c[(x + 1) % 5] << 1) | (c[(x + 1) % 5] >> 63)) & M64) for x in range(5)]
        b = [0] * 25
        for x in range(5):
            for y in range(5):
                v = a[x + 5 * y] ^ d[x]
                r = ROT[x][y]
                b[y + 5 * ((2 * x + 3 * y) % 5)] = ((v << r) | (v >> (64 - r))) & M64 if r else v
        for y in range(5):
            for x in range(5):
                a[x + 5 * y] = b[x + 5 * y] ^ (~b[(x + 1) % 5 + 5 * y] & b[(x + 2) % 5 + 5 * y])
        a[0] ^= rc
    return a


def digest(msg, rounds=6):
    st = [0] * 25
    blk = bytearray(136)
    blk[:len(msg)] = msg
    blk[len(msg)] ^= 6
    blk[135] ^= 0x80
    for i in range(17):
        st[i] ^= int.from_bytes(blk[8 * i:8 * i + 8], "little")
    perm(st, rounds)
    return b"".join(st[i].to_bytes(8, "little") for i in range(4))


K = [0xc9a9d386ab38e13a, 0, 0x9be65c0f48819e78, 0xa42df10543300344, 0, 0x9d9a486de15a3242, 0, 0x62628f16871056a6,
     0x8d7196f55bc91f8b, 0, 0x793ea2677e200f74, 0x7e8d7d4cce830045, 0xfe58db5a1de5126a, 0x1b571a79774b02ce,
     0x8a2d82f8f9dcb705, 0xf01a6a80f9aae74b, 0x8000000000000006] + [0] * 8


VAR = {1: (0,), 6: (1,), 11: (0, 1), 4: (2,), 9: (3,), 14: (2, 3)}


CONST = 1 << 256


def msg_ls(u):
    """u: 4 lanes (u0..u3). 128-byte message, lanes 0..15."""
    ln = list(K[:16])
    for lane, us in VAR.items():
        for j in us:
            ln[lane] ^= u[j]
    return b"".join(v.to_bytes(8, "little") for v in ln)


def forms_t1():
    """Affine forms (bit 64*l+z = u_l[z], bit 256 = constant 1) of T1 = theta_1(round 0(state)), lane x+5y, z."""
    A = [[0] * 64 for _ in range(25)]
    for i in range(25):
        for z in range(64):
            f = CONST if (K[i] >> z) & 1 else 0
            for j in VAR.get(i, ()):
                f ^= 1 << (64 * j + z)
            A[i][z] = f

    def theta(A):
        C = [[0] * 64 for _ in range(5)]
        for x in range(5):
            for z in range(64):
                C[x][z] = A[x][z] ^ A[x + 5][z] ^ A[x + 10][z] ^ A[x + 15][z] ^ A[x + 20][z]
        return [[A[i][z] ^ C[(i % 5 - 1) % 5][z] ^ C[(i % 5 + 1) % 5][(z - 1) % 64] for z in range(64)] for i in range(25)]
    A = theta(A)
    B = [None] * 25
    for x in range(5):
        for y in range(5):
            B[y + 5 * ((2 * x + 3 * y) % 5)] = [A[x + 5 * y][(z - ROT[x][y]) % 64] for z in range(64)]
    V = CONST - 1
    a = [[0] * 64 for _ in range(25)]
    for y in range(5):
        for x in range(5):
            for z in range(64):
                nb, c = B[(x + 1) % 5 + 5 * y][z] ^ CONST, B[(x + 2) % 5 + 5 * y][z]
                if not nb & V:
                    p = c if nb & CONST else 0
                elif not c & V:
                    p = nb if c & CONST else 0
                else:
                    raise ValueError('round 0 not linear')
                a[x + 5 * y][z] = B[x + 5 * y][z] ^ p
    for z in range(64):
        if (RC[0] >> z) & 1:
            a[0][z] ^= CONST
    return a, theta(a)


def gen_aff(dst=1, q=Q_FIX):
    """Ld/st program: loads u planes (buffer 2, lanes 0..3, raw), stores T1 ^ pT into buffer dst."""
    Qp, pC, pD, pT = polarities(q)
    a, T = forms_t1()
    V = CONST - 1
    P = Prog()
    cache = {}                                       # variable mask -> (vreg, pol): vreg value = form ^ pol

    def var(m):
        if m in cache:
            return cache[m]
        bits = [b for b in range(256) if (m >> b) & 1]
        if len(bits) == 1:
            b = bits[0]
            cache[m] = (P.ld(addr(2, b // 64, b % 64)), 0)
            return cache[m]
        hi = 1 << bits[-1]
        r1, p1 = var(m ^ hi); r2, p2 = var(hi)
        cache[m] = (P.xor(r1, r2), p1 ^ p2)
        return cache[m]

    def xr(f, g):                                    # (vreg, pol) of the variable part f ^ g, from cached f and g
        m = (f ^ g) & V
        if m in cache:
            return cache[m]
        (r1, p1), (r2, p2) = cache[f & V], cache[g & V]
        cache[m] = (P.xor(r1, r2), p1 ^ p2)
        return cache[m]

    def C1(x, z):
        f = 0
        for y in range(5):
            g = a[x + 5 * y][z]
            if g & V:
                var(g & V)
                if f & V:
                    xr(f, g)
            f ^= g
        return f
    nots = {}
    for zz in range(64):
        z = (zz + 1) % 64                            # z = 1..63, 0: C1[.][z-1] of the previous slice is reused
        Cz = [C1(x, z) for x in range(5)]
        Cm = [C1(x, (z - 1) % 64) for x in range(5)]
        for x in range(5):
            d = Cz[(x - 1) % 5] ^ Cm[(x + 1) % 5]
            assert d & V
            xr(Cz[(x - 1) % 5], Cm[(x + 1) % 5])
            # outputs that equal D (constant a) first, so D lands in a plane register
            ys = sorted(range(5), key=lambda y: (a[x + 5 * y][z] & V) != 0)
            rd, pdd = cache[d & V]
            for y in ys:
                t = T[x + 5 * y][z]
                assert t == a[x + 5 * y][z] ^ d
                want = (1 if t & CONST else 0) ^ pT[(x, y)]
                if want != pdd and rd not in nots:       # ~D once per (x, z), shared by every output that needs it
                    nots[rd] = P.not_(rd)
                dw = rd if want == pdd else nots[rd]
                if a[x + 5 * y][z] & V:
                    ra, pa = var(a[x + 5 * y][z] & V)
                    assert pa == 0
                    r = P.xor(ra, dw)                    # a ^ D (or a ^ ~D): stored polarity = want
                else:
                    r = dw
                P.st(addr(dst, x + 5 * y, z), r)
    return P


def pd_of(pOut):
    pd = [M64 if pOut[l] else 0 for l in range(4)]
    pd[0] ^= RC[5]                                    # iota of round 5 not executed: folded into PD
    return pd


def resident(P, name):
    """Return (ops, nMreg, ntemp, nmov). ops = (kind, dest, a, b) over names 'M<addr>', 'T<k>', ('i',imm), 'RC'."""
    ins = P.ins
    stores = {}                              # vreg -> list of addresses stored
    for k, d, a, b in ins:
        if k == 'st': stores.setdefault(a, []).append(d)
    alias = {}                               # vreg -> register name
    # first pass: name for each defining vreg
    ld_alias = {}
    for k, d, a, b in ins:
        if k == 'ld' and not isinstance(a, tuple): ld_alias[d] = 'M%d' % a
    name = {}
    for k, d, a, b in ins:
        if k in ('ld', 'st'): continue
        if d in stores: name[d] = 'M%d' % stores[d][0]
    # temps: linear scan over remaining defined vregs (ops with unstored result, and rc loads)
    last = {}
    for i, (k, d, a, b) in enumerate(ins):
        for s in ([] if k == 'ld' else ([a] if k == 'st' else [a, b])):
            if isinstance(s, int): last[s] = i
    free, nxt, tmp = [], 0, {}
    out = []; nmov = 0
    def nm(x):
        if isinstance(x, tuple): return x
        if x in ld_alias: return ld_alias[x]
        if x in name: return name[x]
        return 'T%d' % tmp[x]
    stored_once = set()
    for i, (k, d, a, b) in enumerate(ins):
        srcs = [] if k == 'ld' else ([a] if k == 'st' else [a, b])
        dying = [s for s in set(srcs) if isinstance(s, int) and s in tmp and last.get(s) == i]
        if k == 'ld':
            if isinstance(a, tuple):             # round-constant cell: one counted load into a temp
                tmp[d] = free.pop(0) if free else nxt
                if tmp[d] == nxt: nxt += 1
                out.append(('ld', 'T%d' % tmp[d], 'RC', None))
                if d not in last: free.append(tmp[d])
            continue
        if k == 'st':
            v = a
            tgt = 'M%d' % d
            if nm(v) != tgt:
                out.append(('mov', tgt, nm(v), None)); nmov += 1
            continue
        for s in dying: free.append(tmp[s])
        if d not in name:
            free.sort()
            tmp[d] = free.pop(0) if free else nxt
            if tmp[d] == nxt: nxt += 1
            if d not in last: free.append(tmp[d])
        out.append((k, nm(d), nm(a), nm(b)))
    Ms = set()
    for k, d, a, b in out:
        for x in (d, a, b):
            if isinstance(x, str) and x[0] == 'M': Ms.add(x)
    return out, len(Ms), nxt, nmov


INF = 10 ** 9


isreg = lambda x: isinstance(x, str) and x[0] in 'MT'


def bufof(name):
    return int(name[1:]) // 1600 if name[0] == 'M' else None


def analyse(ops):
    ver = {}; uses = []; defs = []
    for k, d, a, b in ops:
        srcs = [] if k == 'ld' else [x for x in (a, b) if isreg(x)]
        uses.append(tuple((r, ver.get(r, 0)) for r in srcs))
        ver[d] = ver.get(d, 0) + 1
        defs.append((d, ver[d]))
    entry = []; seen = set()
    for u in uses:
        for v in u:
            if v[1] == 0 and v not in seen:
                seen.add(v); entry.append(v[0])
    return uses, defs, ver, entry


def alloc(ops, Emap, Xmap, outs, emit=False):
    """Emap: entry name -> preg (resident, not in memory). Xmap: output name -> preg required at exit.
    outs: output names that must be in memory at exit unless in Xmap. Returns (code, nld, nst, nmov)."""
    uses, defs, ver, entry = analyse(ops)
    n = len(ops)
    final = {nm: (nm, ver[nm]) for nm in ver}
    Xv = {final[nm]: p for nm, p in Xmap.items()}
    outv = {final[nm] for nm in outs if nm in final}
    nxt = {v: n for v in Xv}; nu = [None] * n
    for i in range(n - 1, -1, -1):
        d = defs[i]
        nu[i] = ([nxt.get(v, INF) for v in uses[i]], nxt.get(d, INF))
        nxt.pop(d, None)
        for v in uses[i]:
            nxt[v] = i
    reg = {}; occ = [None] * KR; key = {}; inmem = set(); heap = []
    for nm in entry:
        v = (nm, 0)
        if nm in Emap:
            reg[v] = Emap[nm]; occ[Emap[nm]] = v
        else:
            inmem.add(v)
    for v in list(reg):
        key[v] = nxt.get(v, INF); heapq.heappush(heap, (-key[v], v))
    reserved = set(p for p in Xv.values() if p is not None)
    freeset = set(p for p in range(KR) if occ[p] is None)
    code = []; c = {'ld': 0, 'st': 0, 'mov': 0}

    def take(p):
        freeset.discard(p)

    def release(p):
        occ[p] = None; freeset.add(p)

    def free_reg(protect, avoid=True):
        if freeset:
            good = [p for p in freeset if p not in reserved] if avoid else []
            return min(good) if good else min(freeset)
        aside = []
        while True:
            k_, v = heapq.heappop(heap)
            if v not in reg or key[v] != -k_:
                continue
            if v in protect:
                aside.append((k_, v)); continue
            break
        for x in aside:
            heapq.heappush(heap, x)
        p = reg.pop(v); release(p)
        if v not in inmem and (key[v] < INF or v in outv or v in Xv):
            c['st'] += 1; inmem.add(v)
            if emit: code.append(('st', v, p))
        return p

    def put(v, p, k_):
        reg[v] = p; occ[p] = v; take(p); key[v] = k_; heapq.heappush(heap, (-k_, v))

    def drop(v):
        p = reg.pop(v); release(p)
        if v in outv and v not in Xv and v not in inmem:
            c['st'] += 1; inmem.add(v)
            if emit: code.append(('st', v, p))

    for i, op in enumerate(ops):
        unu, dnu = nu[i]; u = uses[i]
        for v, k_ in zip(u, unu):
            if v not in reg:
                p = Xv.get(v)
                if p is None or occ[p] is not None:
                    p = free_reg(set(u))
                c['ld'] += 1
                if emit: code.append(('ld', v, p))
                put(v, p, k_)
            else:
                key[v] = k_; heapq.heappush(heap, (-k_, v))
        ureg = [reg[v] for v in u]
        for v, k_ in zip(u, unu):
            if k_ == INF and v in reg:
                drop(v)
        d = defs[i]
        if Xv.get(d) is not None:
            p = Xv[d]
            if occ[p] is not None:                      # relocate the occupant
                w = occ[p]; del reg[w]; release(p)
                take(p)
                hold = [r for r in ureg if r in freeset]
                for r in hold: take(r)
                q = free_reg(set(u) | {w})
                for r in hold: freeset.add(r)
                c['mov'] += 1
                if emit: code.append(('mov', w, q, p))
                reg[w] = q; occ[q] = w; take(q); release(p)
        else:
            p = free_reg(set(u))
        if emit: code.append(('op', op, d, p, ureg, u))
        put(d, p, dnu)
        if dnu == INF:
            drop(d)
    # exit: X values into their registers, other outputs in memory
    placed = set()
    for v, p in Xv.items():
        if p is None:
            if v not in reg:
                q = free_reg(set(placed), avoid=False); c['ld'] += 1; reg[v] = q; occ[q] = v; take(q); heapq.heappush(heap, (-key[v], v))
                if emit: code.append(('ld', v, q))
            placed.add(v)
            continue
        if reg.get(v) == p:
            placed.add(v)
            continue
        if occ[p] is not None:                           # p holds another (X) value: move it away first
            w = occ[p]; release(p); take(p)
            q = free_reg({w, v} | placed, avoid=False); occ[q] = w; reg[w] = q; take(q); c['mov'] += 1; release(p)
            if emit: code.append(('mov', w, q, p))
        if v in reg:
            if emit: code.append(('mov', v, p, reg[v]))
            release(reg[v]); c['mov'] += 1
        else:
            c['ld'] += 1
            if emit: code.append(('ld', v, p))
        reg[v] = p; occ[p] = v; take(p); placed.add(v); heapq.heappush(heap, (-key[v], v))
    for v in sorted(outv):
        if v not in Xv and v not in inmem:
            c['st'] += 1
            if emit: code.append(('st', v, reg[v]))
    exitmap = {v[0]: reg[v] for v in Xv}
    alloc.exitmap = exitmap
    return code, c['ld'], c['st'], c['mov']


# ---------------- the S6LS program (proof.md Section 3) ----------------
def build_program():
    P5, pOut, pf = gen_R5(1, qwant=[None, None, None, 0], ls=True)
    secs = {'AFF': gen_aff(1), 'GA': gen_G(0, 1), 'GB': gen_G(1, 0), 'R5': P5}
    res = {k: resident(P, k)[0] for k, P in secs.items()}
    first = {k: analyse(res[k])[3] for k in res}
    outs = {k: [nm for nm in analyse(res[k])[2] if nm[0] == 'M'] for k in res}
    OUTN = ['M%d' % addr(2, l, z) for l in range(4) for z in range(64)]
    S1 = [nm for nm in first['GB'] if bufof(nm) == 1][:KB]
    S0 = [nm for nm in first['GA'] if bufof(nm) == 0][:KB]
    p1 = {nm: i for i, nm in enumerate(S1)}
    code = {}
    code['GB'] = alloc(res['GB'], p1, {nm: None for nm in S0}, outs['GB'], emit=True)[0]; p0 = dict(alloc.exitmap)
    code['GA'] = alloc(res['GA'], p0, p1, outs['GA'], emit=True)[0]
    code['R5'] = alloc(res['R5'], p1, {nm: None for nm in OUTN}, OUTN, emit=True)[0]; pO = dict(alloc.exitmap)
    code['AFF'] = alloc(res['AFF'], pO, p1, outs['AFF'], emit=True)[0]
    return code, pO, pOut, OUTN


def listing(code):
    lines = []
    for k in ('AFF', 'GB', 'GA', 'R5'):
        lines.append('== %s' % k)
        for e in code[k]:
            if e[0] in ('ld', 'st'):
                lines.append('%s r%d %s' % (e[0], e[2], e[1][0]))
            elif e[0] == 'mov':
                lines.append('mov r%d r%d' % (e[2], e[3]))
            else:
                kind, dn, a, b = e[1]
                it = iter(e[4])
                f = lambda x: ('#%x' % x[1]) if isinstance(x, tuple) else 'RC' if x == 'RC' else '-' if x is None else 'r%d' % next(it)
                lines.append('%s r%d %s %s' % (kind, e[3], f(a), f(b)))
    return '\n'.join(lines) + '\n'


def compile_sections(code):
    """Each section becomes a Python function over the register list R, the memory cells M and the all-ones word A."""
    fns = {}
    for k in ('AFF', 'GB', 'GA', 'R5'):
        L = ['def S(R, M, A, rc):']
        for e in code[k]:
            if e[0] == 'ld':
                L.append(' R[%d] = M[%d]' % (e[2], int(e[1][0][1:])))
            elif e[0] == 'st':
                L.append(' M[%d] = R[%d]' % (int(e[1][0][1:]), e[2]))
            elif e[0] == 'mov':
                L.append(' R[%d] = R[%d]' % (e[2], e[3]))
            else:
                kind, dn, a, b = e[1]
                it = iter(e[4])
                def v(x):
                    if isinstance(x, tuple): return 'A' if x[1] == ALL else '%d' % x[1]
                    if x == 'RC': return 'rc'
                    return 'R[%d]' % next(it)
                p = e[3]
                if kind == 'ld': L.append(' R[%d] = rc' % p)
                elif kind == 'mov': L.append(' R[%d] = %s' % (p, v(a)))
                elif kind == 'sub':
                    x = v(a); L.append(' R[%d] = (%s - %s) & A' % (p, x, v(b)))
                else:
                    x = v(a); L.append(' R[%d] = %s %s %s' % (p, x, {'xor': '^', 'and': '&', 'or': '|', 'shr': '>>'}[kind], v(b)))
        env = {}
        exec(compile('\n'.join(L), 's6ls_' + k, 'exec'), env)
        fns[k] = env['S']
    return fns


def setup():
    for m in (b"", b"abc", bytes(135)):
        assert digest(m, 24) == hashlib.sha3_256(m).digest()
    code, pO, pOut, OUTN = build_program()
    lst = listing(code)
    nstep = sum((2 if k in ('GA', 'GB') else 1) * len(code[k]) for k in code) + 19
    assert hashlib.sha256(lst.encode()).hexdigest() == LISTING_SHA256 and nstep == NSTEP
    fns = compile_sections(code)
    regs = [pO[nm] for nm in OUTN]                 # plane j (lane j // 64, bit j % 64) lives in register regs[j]
    rc = [(~r) & M64 for r in RC]
    Rint = [0] * KR
    Mem = [0] * 4800

    def step(Rl, A):
        for j in range(256): Rint[regs[j]] = Rl[j]
        fns['AFF'](Rint, Mem, A, 0)
        fns['GB'](Rint, Mem, A, rc[1]); fns['GA'](Rint, Mem, A, rc[2])
        fns['GB'](Rint, Mem, A, rc[3]); fns['GA'](Rint, Mem, A, rc[4])
        fns['R5'](Rint, Mem, A, 0)
        for j in range(256): Rl[j] = Rint[regs[j]]
    return step, pd_int(pd_of(pOut))


def pd_int(pd):
    return sum(v << (64 * l) for l, v in enumerate(pd))


def msg_of(u):
    return msg_ls([(u >> (64 * i)) & M64 for i in range(4)])


def F_ref(u, PD):
    return int.from_bytes(digest(msg_of(u)), "little") ^ PD


def to_planes(points, T):
    """points[t][l] (256-bit) -> 256 planes with bit 256 t + l."""
    planes = [0] * 256
    for t in range(T):
        for l, u in enumerate(points[t]):
            g = 256 * t + l
            j = 0
            while u:
                if u & 1: planes[j] |= 1 << g
                u >>= 1; j += 1
    return planes


def lane_value(R, g, width=256):
    v = 0
    for j in range(width):
        v |= ((R[j] >> g) & 1) << j
    return v


def check_step(step, PD):
    import random
    rnd = random.Random(1)
    pts = [[rnd.getrandbits(256) for _ in range(256)]]
    R = to_planes(pts, 1)
    A = (1 << 256) - 1
    cur = pts[0]
    for _ in range(2):
        step(R, A)
        cur = [F_ref(u, PD) for u in cur]
        for l in range(0, 256, 15):
            assert lane_value(R, l) == cur[l]


def shake(data, n):
    return hashlib.shake_256(data).digest(n)


# ---------------- rho-w22: the search of proof.md Section 4 at width W ----------------
W, H, LC, U, TB = 22, 4, 128, 3000, 400


def rho_w(trials, step, PD):
    T = len(trials)
    A = (1 << (256 * T)) - 1
    mask = (1 << W) - 1
    R = [0] * 256
    seeds = [bytes.fromhex(t["seed"]) for t in trials]
    rho, nid, att, astart = [0] * T, [0] * T, [-1] * T, [0] * T
    table = [dict() for _ in range(T)]
    done = [None] * T
    obs = [dict(steps=0, trails=0, dead=0, attempts=0, stored=0, replay_evals=0) for _ in range(T)]
    lid, lst = [0] * (256 * T), [0] * (256 * T)
    due, pend = {}, []

    def f_small(u):
        return F_ref(u, PD) & mask

    def new_attempt(t, c):
        att[t] += 1; obs[t]['attempts'] += 1
        rho[t] = int.from_bytes(shake(seeds[t] + att[t].to_bytes(4, 'little'), 8), 'little') & mask
        table[t].clear(); nid[t] = 256; astart[t] = c
        for l in range(256):
            g = 256 * t + l
            lid[g] = l; lst[g] = c
            due.setdefault(c + LC, []).append((g, l, att[t]))
            pend.append((g, (rho[t] + l) & mask))
        obs[t]['trails'] += 256

    def apply_pending():
        if not pend: return
        clr = 0
        for g, _ in pend: clr |= 1 << g
        for j in range(W):
            st = 0
            for g, x in pend:
                if (x >> j) & 1: st |= 1 << g
            R[j] = (R[j] & ~clr & A) | st
        del pend[:]

    def replay(sa, la, sb, lb, t):
        a, b = sa, sb
        for _ in range(abs(la - lb)):
            if la > lb: a = f_small(a)
            else: b = f_small(b)
        obs[t]['replay_evals'] += abs(la - lb)
        if a == b: return None
        for _ in range(min(la, lb) + 1):
            na, nb = f_small(a), f_small(b)
            obs[t]['replay_evals'] += 2
            if na == nb: return a, b
            a, b = na, nb
        return None

    for t in range(T): new_attempt(t, 0)
    apply_pending()
    c = 0
    while any(d is None for d in done):
        c += 1
        if c > 4000: raise RuntimeError("no pair")
        step(R, A)
        for j in range(W, 256): R[j] = 0               # width reduction (this experiment only)
        anyv = 0
        for j in range(H): anyv |= R[j]
        dpm = A ^ anyv
        events = []
        while dpm:
            low = dpm & -dpm
            events.append((low.bit_length() - 1, 1))
            dpm ^= low
        for g, ident, at in due.pop(c, []):
            if lid[g] == ident and att[g >> 8] == at: events.append((g, 2))
        events.sort()
        seen, fresh = set(), set()
        for g, kind in events:
            t = g >> 8
            if g in seen or done[t] is not None or t in fresh: continue
            seen.add(g)
            if kind == 1:
                x = lane_value(R, g, W)
                ln = c - lst[g]
                tb = table[t]
                if x in tb:
                    ida, la = tb[x]
                    if ida != lid[g]:
                        r = replay((rho[t] + ida) & mask, la, (rho[t] + lid[g]) & mask, ln, t)
                        if r is not None:
                            done[t] = r; obs[t]['steps'] = c - astart[t]; obs[t]['stored'] = len(tb)
                            continue
                else:
                    tb[x] = (lid[g], ln)
            else:
                obs[t]['dead'] += 1
            if nid[t] >= U:
                new_attempt(t, c); fresh.add(t); continue
            i = nid[t]; nid[t] += 1; obs[t]['trails'] += 1
            lid[g] = i; lst[g] = c
            due.setdefault(c + LC, []).append((g, i, att[t]))
            pend.append((g, (rho[t] + i) & mask))
        for t in range(T):
            if done[t] is None and c - astart[t] >= TB: new_attempt(t, c)
        apply_pending()
    return done, obs


# ---------------- proj-w256: chained full-width steps, 22-bit agreement ----------------
def proj_w(trials, step, PD, steps=8, bits=22):
    T = len(trials)
    A = (1 << (256 * T)) - 1
    pts = []
    for tr in trials:
        raw = shake(bytes.fromhex(tr["seed"]) + b"proj", 32 * 256)
        pts.append([int.from_bytes(raw[32 * l:32 * l + 32], "little") for l in range(256)])
    R = [0] * 256
    R[:256] = to_planes(pts, T)
    from array import array
    allkeys = []                            # allkeys[s][g]: the 22 low image bits of lane g at step s

    def point(t, l, s):                     # input of step s on lane l (reference chain from the start point)
        u = pts[t][l]
        for _ in range(s): u = F_ref(u, PD)
        return u

    for s in range(steps):
        step(R, A)
        cols = [bin(R[j] | (1 << (256 * T)))[:2:-1] for j in range(bits)]   # bit g of plane j = cols[j][g]
        allkeys.append(array("I", (int("".join(c[g] for c in reversed(cols)), 2) for g in range(256 * T))))
        del cols
    done = [None] * T
    for t in range(T):
        st = {}
        for s in range(steps):
            ks = allkeys[s]
            for l in range(256):
                key = ks[256 * t + l]
                o = st.get(key)
                if o is None:
                    st[key] = (l, s)
                else:
                    a, b = point(t, o[0], o[1]), point(t, l, s)
                    if a != b:
                        done[t] = (a, b, s); break
            if done[t] is not None: break
    return done


def main():
    step, PD = setup()
    check_step(step, PD)
    req = json.load(sys.stdin)
    if req["schema_version"] != 1 or req["target_profile"] != "sha3-256-r6-prefix-v1":
        raise ValueError("unexpected organizer target")
    mask = ((1 << 22) - 1).to_bytes(32, "little")
    if req["event"] != {"kind": "digest-xor-mask", "mask_hex": mask.hex(), "expected_hex": "00" * 32}:
        raise ValueError("unexpected organizer event")
    trials = req["trials"]
    out = []
    if req["experiment_id"] == "rho-w22":
        done, obs = rho_w(trials, step, PD)
        for t, tr in enumerate(trials):
            a, b = done[t]
            ma, mb = msg_of(a), msg_of(b)
            assert ma != mb and (int.from_bytes(digest(ma), "little") ^ int.from_bytes(digest(mb), "little")) & ((1 << W) - 1) == 0
            out.append({"trial": tr["trial"], "message_a_hex": ma.hex(), "message_b_hex": mb.hex(), "observations": obs[t]})
    elif req["experiment_id"] == "proj-w256":
        done = proj_w(trials, step, PD)
        for t, tr in enumerate(trials):
            if done[t] is None:
                out.append({"trial": tr["trial"], "message_a_hex": None, "message_b_hex": None})
            else:
                a, b, s = done[t]
                out.append({"trial": tr["trial"], "message_a_hex": msg_of(a).hex(), "message_b_hex": msg_of(b).hex(), "observations": {"step": s}})
    else:
        raise ValueError("unknown experiment")
    json.dump({"schema_version": 1, "trials": out}, sys.stdout, separators=(",", ":"), sort_keys=True)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
