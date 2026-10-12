"""Collision search on sha3-256-r6-prefix-v1 at a reduced digest width: 256 walks advanced in lockstep by a dense bit-sliced program.

f(x) = lanes 0..3 of Keccak-f rounds 0-5 on the state of the one-block message x (32 little-endian bytes) || 103 zero bytes.
The 256-bit word RAM holds one bit plane of the state in each word: plane (lane, z) has bit i = bit z of that Keccak lane for walk i.
One step of all 256 walks is the register program built below (loads, stores, xor, and, or, shr, sub on at most 64 registers; the
experiment executes exactly these instructions on Python integers; an integer may hold the planes of all trials of a request side
by side, trial t in bits 256 t .. 256 t + 255, so every instruction acts on all trials at once and the trials never interact).
Walks end at distinguished points (the low H bits of the kept digest are zero in this experiment); a table keeps end -> (trail id,
length); two trails with the same end are replayed (scalar program) to the first point where they merge: two different inputs
with equal f. The experiment keeps the low W bits of f(x): after each step the planes above W are set to zero (this reduction is
the only step that is not part of the full-size program).
"""
import sys, json, hashlib

M64 = (1 << 64) - 1
ALL = (1 << 256) - 1
RC = [0x1, 0x8082, 0x800000000000808A, 0x8000000080008000, 0x808B, 0x80000001]
ROT = [[0, 36, 3, 41, 18], [1, 44, 10, 45, 2], [62, 6, 43, 15, 61], [28, 55, 25, 21, 56], [27, 20, 39, 8, 14]]
Q_FIX = 4361286          # polarity (bit X+5Y) of the stored chi outputs: a fixed point of a whole round, found by search
PAD = 0x8600000000000000  # lane 16
PF_K = 16                # planes of lane 3 in the DP prefilter


def xmap(X, Y):
    return (3 * Y + X) % 5           # old column x of the lane that lands on B(X, Y)  (X = old y)


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


IOTA_Z = (0, 1, 3, 7, 15, 31, 63)       # union of the set bits of RC[0..4]


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


def gen_phase1(dst, pIn, q=Q_FIX):
    """Reads the 256 input planes (buffer 2, lanes 0..3, stored polarity pIn[l]) and writes T0 (theta added to the dense-input state) to dst."""
    Qp, pC, pD, pT = polarities(q)
    P = Prog()
    kz = {57, 58, 63}
    cache = {}

    def lane_in(l, z):
        z %= 64
        if (l, z) not in cache:
            cache[(l, z)] = (P.ld(addr(2, l, z)), pIn[l])      # true value = reg ^ pol
        return cache[(l, z)]

    def flipk(u, z):
        return (u[0], u[1] ^ (1 if z in kz else 0))

    def cx(a, b):
        if a is None:
            return b
        if b is None:
            return a
        return (P.xor(a[0], b[0]), a[1] ^ b[1])

    for z in range(64):
        zm = (z - 1) % 64
        for key in [k for k in cache if k[1] not in (z, zm)]:
            del cache[key]
        C = [lane_in(0, z), flipk(lane_in(1, z), z), lane_in(2, z), lane_in(3, z), None]
        Cm = [lane_in(0, zm), flipk(lane_in(1, zm), zm), lane_in(2, zm), lane_in(3, zm), None]
        D = [cx(C[4], Cm[1]), cx(C[0], Cm[2]), cx(C[1], Cm[3]), cx(C[2], Cm[4]), cx(C[3], Cm[0])]
        T = {}
        for x in range(5):
            for y in range(5):
                if y == 0:
                    T[(x, y)] = cx(lane_in(x, z) if x < 4 else None, D[x])
                elif (x, y) == (1, 3):
                    T[(x, y)] = (D[1][0], D[1][1] ^ (1 if z in kz else 0))
                else:
                    T[(x, y)] = D[x]
        nots = {}
        for x in range(5):
            for y in range(5):
                r, p = T[(x, y)]
                if p != pT[(x, y)]:
                    if r not in nots:
                        nots[r] = P.not_(r)
                    r = nots[r]
                P.st(addr(dst, x + 5 * y, z), r)
    return P


def gen_R5(src, q=Q_FIX, qwant=None):
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
            if X == 0 and z in (0, 31):
                v = P.not_(v)            # iota of round 5 (RC = 0x80000001)
            P.st(addr(2, X, z), v)
            if X == 3 and z < PF_K:
                pf = v if pf is None else (P.or_(pf, v) if pOut[3] == 0 else P.and_(pf, v))
    return P, pOut, pf


def stats(P):
    ins = P.ins
    last = {}
    defi = {}
    for i, (k, d, a, b) in enumerate(ins):
        srcs = [] if k == 'ld' else ([a] if k == 'st' else [a, b])
        for s in srcs:
            if isinstance(s, int):
                last[s] = i
        if k != 'st':
            defi[d] = i
    delta = [0] * (len(ins) + 2)
    for v, d in defi.items():
        l = last.get(v, d)
        delta[d] += 1
        delta[l + 1] -= 1
    cur = 0
    peak = 0
    for i in range(len(ins)):
        cur += delta[i]
        k, d, a, b = ins[i]
        dying = 0
        if k not in ('ld', 'st'):
            dying = sum(1 for s in {a, b} if isinstance(s, int) and last.get(s) == i)
        peak = max(peak, cur - (1 if dying else 0))
    cnt = {}
    for k, *_ in ins:
        cnt[k] = cnt.get(k, 0) + 1
    return len(ins), cnt, peak


def regalloc(P):
    """Linear-scan allocation of the virtual registers to physical registers 0.. (a source that dies at an instruction
    frees its register for that instruction's result). Returns (map, number of registers used)."""
    ins = P.ins
    last = {}
    for i, (k, d, a, b) in enumerate(ins):
        for s in ([] if k == 'ld' else ([a] if k == 'st' else [a, b])):
            if isinstance(s, int):
                last[s] = i
    free = []
    nxt = 0
    phys = {}
    for i, (k, d, a, b) in enumerate(ins):
        srcs = [] if k == 'ld' else ([a] if k == 'st' else [a, b])
        for s in set(x for x in srcs if isinstance(x, int)):
            if last[s] == i:
                free.append(phys[s])
        if k != 'st':
            if free:
                free.sort()
                phys[d] = free.pop(0)
            else:
                phys[d] = nxt
                nxt += 1
            if d not in last:
                free.append(phys[d])
    return phys, nxt


def to_python(P, name, allw='ALLW'):
    """Straight-line python over the physical registers: memory list M, registers p<k> as locals."""
    phys, nreg = regalloc(P)
    L = ["def %s(M, RC=0):" % name]

    def v(x):
        if isinstance(x, tuple):
            return allw if x[1] == ALL else "%d" % x[1]
        return "p%d" % phys[x]
    for k, d, a, b in P.ins:
        if k == 'ld':
            L.append("    p%d = %s" % (phys[d], "RC" if isinstance(a, tuple) else "M[%d]" % a))
        elif k == 'st':
            L.append("    M[%d] = p%d" % (d, phys[a]))
        elif k == 'xor':
            L.append("    p%d = %s ^ %s" % (phys[d], v(a), v(b)))
        elif k == 'and':
            L.append("    p%d = %s & %s" % (phys[d], v(a), v(b)))
        elif k == 'or':
            L.append("    p%d = %s | %s" % (phys[d], v(a), v(b)))
        elif k == 'shr':
            L.append("    p%d = %s >> %s" % (phys[d], v(a), v(b)))
        elif k == 'sub':
            L.append("    p%d = (%s - %s) & %s" % (phys[d], v(a), v(b), allw))
        else:
            raise ValueError(k)
    L.append("    return")
    return chr(10).join(L), nreg

RC_ALL = [0x1, 0x8082, 0x800000000000808A, 0x8000000080008000, 0x808B, 0x80000001, 0x8000000080008081,
          0x8000000000008009, 0x8A, 0x88, 0x80008009, 0x8000000A, 0x8000808B, 0x800000000000008B,
          0x8000000000008089, 0x8000000000008003, 0x8000000000008002, 0x8000000000000080, 0x800A,
          0x800000008000000A, 0x8000000080008081, 0x8000000000008080, 0x80000001, 0x8000000080008008]


def build_ops():
    """Straight-line program of f. A lane is a 64-bit value in a 256-bit RAM word. An int is an immediate (a
    constant folded when the program is built), a str names a RAM word. Every emitted op is ONE word operation:
    xor, and, or of two words or of a word and an immediate, shl or shr of a word by an immediate.
    Inputs in0..in3; the result is lanes 0..3. Returns (ops, outs); ops = (dst, op, x, y, round)."""
    ops = []
    rnd = [0]

    def emit(op, x, y, mask=False):
        cx, cy = isinstance(x, int), isinstance(y, int)
        if cx and cy:
            return {'xor': x ^ y, 'and': x & y, 'or': x | y, 'shl': x << y, 'shr': x >> y}[op]
        if cx and op in ('xor', 'and', 'or'):
            x, y, cx, cy = y, x, cy, cx
        if not mask:
            if op in ('xor', 'or') and cy and y == 0:
                return x                       # x ^ 0, x | 0
            if op == 'and' and cy and y == 0:
                return 0
            if op == 'and' and cy and y == M64:
                return x                       # x is already a 64-bit lane
            if op == 'or' and cy and y == M64:
                return M64
        name = 't%d' % len(ops)
        ops.append((name, op, x, y, rnd[0]))
        return name

    def rot(v, r):                             # shl, shr, or, and (the mask): 4 operations
        if r == 0:
            return v
        return emit('and', emit('or', emit('shl', v, r), emit('shr', v, 64 - r)), M64, True)

    a = ['in0', 'in1', 'in2', 'in3'] + [0] * 12 + [0x8600000000000000] + [0] * 8
    for r in range(6):
        rnd[0] = r
        c = []
        for x in range(5):
            t = a[x]
            for y in range(1, 5):
                t = emit('xor', t, a[x + 5 * y])
            c.append(t)
        d = [emit('xor', c[(x + 4) % 5], rot(c[(x + 1) % 5], 1)) for x in range(5)]
        b = [0] * 25
        for x in range(5):
            for y in range(5):
                b[y + 5 * ((2 * x + 3 * y) % 5)] = rot(emit('xor', a[x + 5 * y], d[x]), ROT[x][y])
        a = [0] * 25
        for y in range(5):
            for x in range(5):
                nb = emit('xor', b[(x + 1) % 5 + 5 * y], M64)       # NOT = xor with all ones; no fused AND-NOT
                a[x + 5 * y] = emit('xor', b[x + 5 * y], emit('and', nb, b[(x + 2) % 5 + 5 * y]))
        a[0] = emit('xor', a[0], RC[r])
    outs = a[:4]                       # lanes 4..24 of the last round are never read: their ops are dropped
    live = {o for o in outs if isinstance(o, str)}
    kept = []
    for op in reversed(ops):
        if op[0] in live:
            kept.append(op)
            live |= {v for v in op[2:4] if isinstance(v, str)}
    kept.reverse()
    return kept, outs


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


def msg_of(x):
    return x.to_bytes(32, "little") + bytes(103)


def _compile():
    ops, outs = build_ops()
    sym = {'shl': '<<', 'shr': '>>', 'xor': '^', 'and': '&', 'or': '|'}
    L = ["def fast(in0, in1, in2, in3):"]
    L += ["    %s = %s %s %s" % (n, x, sym[op], y) for n, op, x, y, _ in ops]
    L.append("    return " + ", ".join(map(str, outs)))
    env = {}
    exec(chr(10).join(L), env)
    return env["fast"], len(ops)


FAST, F = _compile()        # F word operations per evaluation


def selftest():
    for m in (b"", b"abc", bytes(135)):
        assert digest(m, 24) == hashlib.sha3_256(m).digest()
    for x in [0, 1, 2 ** 14 - 1, 2 ** 64, 2 ** 256 - 1] + [int.from_bytes(hashlib.sha256(b"%d" % i).digest(), "little") for i in range(40)]:
        lanes = [(x >> (64 * i)) & M64 for i in range(4)]
        out = FAST(*lanes)
        assert b"".join(v.to_bytes(8, "little") for v in out) == digest(msg_of(x))
    assert len(msg_of(1)) == 135 and F == len(build_ops()[0])


def build_sections():
    P5, pOut, pf = gen_R5(1, qwant=[0, 1, 1, 0])
    pIn = [pOut[i] for i in range(4)]
    secs = {'phase1': gen_phase1(0, pIn), 'GA': gen_G(0, 1), 'GB': gen_G(1, 0), 'R5': P5}
    return secs, pIn, pOut


def step_count(secs):
    """Word operations of one batch step, as executed: phase 1, five generic rounds (GA GB GA GB GA), the last round, the loop
    control (pointer init 1, pointer step 5, exit test after each GA 3 x 2, jump after each GB 2 x 1), the prefilter test 2, the counter 3."""
    n1, nG, n5 = len(secs['phase1'].ins), len(secs['GA'].ins), len(secs['R5'].ins)
    assert nG == len(secs['GB'].ins)
    return n1 + 5 * nG + n5 + (1 + 5 + 3 * 2 + 2 * 1) + 2 + 3


def dense_selftest(secs, pIn, pOut):
    """The dense program on 256 inputs at once (the 256 lanes of one trial), two chained steps, against the plain permutation."""
    env = {'ALLW': ALL}
    for k, P in secs.items():
        exec(to_python(P, k)[0], env)
    xs = [int.from_bytes(hashlib.sha256(b"dense%d" % i).digest(), "little") for i in range(256)]
    M = [0] * 4800
    for l in range(4):
        for z in range(64):
            w = 0
            for i, x in enumerate(xs):
                w |= ((x >> (64 * l + z)) & 1) << i
            M[addr(2, l, z)] = w ^ (ALL if pIn[l] else 0)
    rc = [(~r) & M64 for r in RC]
    for _ in range(2):
        env['phase1'](M)
        env['GA'](M, rc[0]); env['GB'](M, rc[1]); env['GA'](M, rc[2]); env['GB'](M, rc[3]); env['GA'](M, rc[4])
        env['R5'](M)
        want = [int.from_bytes(digest(msg_of(x)), "little") for x in xs]
        got = []
        for i in range(256):
            y = 0
            for l in range(4):
                for z in range(64):
                    y |= (((M[addr(2, l, z)] ^ (ALL if pOut[l] else 0)) >> i) & 1) << (64 * l + z)
            got.append(y)
        assert got == want
        xs = want
    return len(xs)


# ===================================================================== the search (driver) =====================================
# 256 walks (lanes) are advanced in lockstep by the dense program; the digest planes of a step are the input planes of the next.
# Parameters of this experiment (the full-size values are in proof.md): W digest bits kept, H distinguished-point bits.
W = 18           # reduced digest width in bits (the full target keeps 256)
H = 4            # distinguished point: the low H bits of the kept digest are zero (the full target: 116 bits of lanes 3 and 2)
LC = 256         # trail cap in steps (the full target: 2^120 - 2)
TB = 200         # batch steps per attempt
U = 3000         # trails per attempt (table slots)
LANES = 256


def shake(data, n):
    return hashlib.shake_256(data).digest(n)


def run_all(trials, secs, pIn, pOut):
    T = len(trials)
    NB = 32 * T
    ALLW = (1 << (256 * T)) - 1
    env = {'ALLW': ALLW}
    for k, P in secs.items():
        exec(to_python(P, k)[0], env)
    M = [0] * 4800
    for l in range(4):
        for z in range(64):
            M[addr(2, l, z)] = ALLW if pIn[l] else 0
    mask = (1 << W) - 1
    dpm = (1 << H) - 1
    seeds = [bytes.fromhex(t["seed"]) for t in trials]
    rho = [0] * T
    nid = [0] * T
    table = [dict() for _ in range(T)]
    att = [-1] * T
    astart = [0] * T
    done = [None] * T
    obs = [dict(steps=0, trails=0, dead=0, attempts=0, stored=0, replay_evals=0) for _ in range(T)]
    lid = [0] * (256 * T)
    lst = [0] * (256 * T)
    due = {}
    rc = [(~r) & M64 for r in RC]
    pend_g, pend_x = [], []

    def new_attempt(t, c):
        att[t] += 1
        obs[t]['attempts'] += 1
        rho[t] = int.from_bytes(shake(seeds[t] + att[t].to_bytes(4, 'little'), 8), 'little') & mask
        table[t].clear()
        nid[t] = LANES
        astart[t] = c
        for l in range(LANES):
            g = 256 * t + l
            lid[g] = l
            lst[g] = c
            due.setdefault(c + LC, []).append((g, l, att[t]))
            pend_g.append(g)
            pend_x.append((rho[t] + l) & mask)
        obs[t]['trails'] += LANES

    def apply_pending():
        if not pend_g:
            return
        for b in range(W):
            clr, st = bytearray(NB), bytearray(NB)
            for g, x in zip(pend_g, pend_x):
                clr[g >> 3] |= 1 << (g & 7)
                if (x >> b) & 1:
                    st[g >> 3] |= 1 << (g & 7)
            a = addr(2, 0, b)
            pol = ALLW if pIn[0] else 0
            c_ = int.from_bytes(clr, 'little')
            M[a] = ((((M[a] ^ pol) | c_) ^ c_) | int.from_bytes(st, 'little')) ^ pol
        del pend_g[:], pend_x[:]

    def f_small(x):
        return FAST(x & M64, 0, 0, 0)[0] & mask

    def replay(sa, la, sb, lb, t):
        """Starts sa, sb whose trails (la, lb steps) end at the same point: step the longer one la - lb, then both until the
        images agree. Returns two different inputs with equal f, or None (one start lies on the other trail)."""
        a, b = sa, sb
        n = abs(la - lb)
        for _ in range(n):
            if la > lb:
                a = f_small(a)
            else:
                b = f_small(b)
        obs[t]['replay_evals'] += n
        if a == b:
            return None
        for _ in range(min(la, lb) + 1):
            na, nbb = f_small(a), f_small(b)
            obs[t]['replay_evals'] += 2
            if na == nbb:
                return a, b
            a, b = na, nbb
        return None

    for t in range(T):
        new_attempt(t, 0)
    apply_pending()
    c = 0
    while any(d is None for d in done):
        c += 1
        if c > 20000:
            raise RuntimeError("no collision")
        env['phase1'](M)
        env['GA'](M, rc[0]); env['GB'](M, rc[1]); env['GA'](M, rc[2]); env['GB'](M, rc[3]); env['GA'](M, rc[4])
        env['R5'](M)
        for b in range(W, 256):                       # reduction to W bits (this experiment only): the planes above W are zero
            M[addr(2, b // 64, b % 64)] = ALLW if pIn[b // 64] else 0
        anyv = 0
        for z in range(H):
            anyv |= M[addr(2, 0, z)] ^ (ALLW if pOut[0] else 0)
        dpmask = ALLW ^ anyv
        events = []
        if dpmask:
            by = dpmask.to_bytes(NB, 'little')
            events = [(i * 8 + j, 1) for i, v in enumerate(by) if v for j in range(8) if (v >> j) & 1]
        for g, ident, at in due.pop(c, []):
            if lid[g] == ident and att[g >> 8] == at:
                events.append((g, 2))
        events.sort()
        if events:
            pb = [(M[addr(2, 0, b)] ^ (ALLW if pOut[0] else 0)).to_bytes(NB, 'little') for b in range(W)]
        seen = set()
        fresh = set()
        for g, kind in events:
            t = g >> 8
            if g in seen or done[t] is not None or t in fresh:
                continue
            seen.add(g)
            if kind == 1:
                x = 0
                for b in range(W):
                    x |= ((pb[b][g >> 3] >> (g & 7)) & 1) << b
                tb = table[t]
                ln = c - lst[g]
                if x in tb:
                    ida, la = tb[x]
                    if ida != lid[g]:
                        r = replay((rho[t] + ida) & mask, la, (rho[t] + lid[g]) & mask, ln, t)
                        if r is not None:
                            done[t] = r
                            obs[t]['steps'] = c
                            obs[t]['stored'] = len(tb)
                            continue
                else:
                    tb[x] = (lid[g], ln)
            else:
                obs[t]['dead'] += 1
            if nid[t] >= U:
                new_attempt(t, c)
                fresh.add(t)
                continue
            i = nid[t]
            nid[t] += 1
            obs[t]['trails'] += 1
            lid[g] = i
            lst[g] = c
            due.setdefault(c + LC, []).append((g, i, att[t]))
            pend_g.append(g)
            pend_x.append((rho[t] + i) & mask)
        for t in range(T):
            if done[t] is None and c - astart[t] >= TB:
                new_attempt(t, c)
        apply_pending()
    return done, obs, c


def main():
    selftest()
    secs, pIn, pOut = build_sections()
    dense_selftest(secs, pIn, pOut)
    req = json.load(sys.stdin)
    if req["schema_version"] != 1 or req["target_profile"] != "sha3-256-r6-prefix-v1":
        raise ValueError("unexpected organizer target")
    mask = ((1 << W) - 1).to_bytes(32, "little")
    if req["event"] != {"kind": "digest-xor-mask", "mask_hex": mask.hex(), "expected_hex": "00" * 32}:
        raise ValueError("unexpected organizer event")
    done, obs, steps = run_all(req["trials"], secs, pIn, pOut)
    bstep = step_count(secs)
    out = []
    for t, tr in enumerate(req["trials"]):
        a, b = done[t]
        ma, mb = msg_of(a), msg_of(b)
        assert ma != mb
        da, db = digest(ma), digest(mb)
        assert (int.from_bytes(da, "little") ^ int.from_bytes(db, "little")) & ((1 << W) - 1) == 0
        o = obs[t]
        o["ops"] = o["steps"] * bstep + o["replay_evals"] * (F + 7)
        out.append({"trial": tr["trial"], "message_a_hex": ma.hex(), "message_b_hex": mb.hex(), "observations": o})
    json.dump({"schema_version": 1, "trials": out}, sys.stdout, separators=(",", ":"), sort_keys=True)
    sys.stdout.write(chr(10))


if __name__ == "__main__":
    main()
