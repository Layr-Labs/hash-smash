# -*- coding: utf-8 -*-
"""Bit-sliced grouped round-skip birthday search on reduced-round SHA-256 (r37/r38): scaled evidence and
a counted witness of the physically scheduled batch program.

Organizer-executed (python-message-pairs-v1). Standard library only; deterministic from the trial seeds.
Reads one JSON request from stdin and writes one JSON document to stdout. Five experiments share this
file and branch on request["experiment_id"]; the round count R comes from request["target_profile"]
("sha256-r38-prefix-v1" -> 38, "sha256-r37-prefix-v1" -> 37).

Message family (proof.md): 55-byte single-block messages m(P, u) = BE32(W0) || ... || BE32(W12) || BE24(u),
W0..W12 the group prefix, u a 24-bit index (full scale: u = 256*b + L, batch b, lane L). Padding gives
W13 = (u << 8) | 0x80, W14 = 0, W15 = 440. Key (144 bits) = the raw state words a, b, e, f entering
round R-2 and the low 16 bits of e entering round R-1 (word-wise bijective with digest words c, d, g, h
and f[0:16]); round R-1 is skipped.

Fast path (all trials): the same symbolic circuit, compiled once into chunked straight-line Python over
256 lanes, where every lane carries its own prefix planes and its own 24 u planes, so lanes of one batch
may belong to different trials (bitwise operations never mix lanes). The scaled searches key on the low
18 bits of digest word h (= f + IV7, computed from the key's f word), the equivalence check on 12.

Counted witness (trial 0 of every experiment): the counted program of proof Appendix A is regenerated
(generator -> dead-code elimination -> furthest-next-use register allocation over 58 registers with
explicit loads and stores) and EXECUTED by a counting VM on one batch of the full-scale family (one
group prefix and one 16-bit batch index from the seed, 256 lanes): the circuit, the batch setup, the
zero-aware delta-swap transpose (rows 0..110 zero, 111..254 the key planes, 255 all-ones; a delta swap
costs 6 ops, 3 when the lower row is zero, 4 when the upper row is zero) and the 256 table sinks
(idx = Kw >> 111; e = LOAD T[idx]; x = Kw ^ BIDL; y = x ^ e; z = y >> 128; compare z with 0; branch;
STORE T[idx] = x; BIDL += 1, with BIDL = (RTAG << 128) | (g*2^24 + b*2^8 + L)). All 256 key words and
transposed addresses are compared with the scalar reference; any mismatch aborts with a nonzero exit. The exact
totals asserted are 47,932 ops at R = 37 and 50,276 at R = 38 (including the eight delta-swap mask
loads per batch; transpose and table counts as charged).
Numeric observations are untrusted.
"""
import hashlib
import json
import sys

M = (1 << 256) - 1
MASK32 = 0xFFFFFFFF
IV = (0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19)
K = (
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
)
LANE_PLANES = [sum(((L >> i) & 1) << L for L in range(256)) for i in range(8)]
EXPECTED_TOTAL = {37: 47932, 38: 50276}
NREGS = 58
F_BITS = 16
KEY_ROW0 = 111            # key plane i is transpose row 111 + i; row 255 is all-ones; rows 0..110 zero


def require(cond, msg):
    if not cond:
        sys.stderr.write(msg + "\n")
        sys.exit(1)


# ---------------------------------------------------------------- scalar reference
def ror(v, r):
    return ((v >> r) | (v << (32 - r))) & MASK32


def scalar_state(msg55, R):
    """(state entering round R-2, e entering round R-1, digest words) of the reduced hash."""
    padded = msg55 + b"\x80" + (440).to_bytes(8, "big")
    w = list(int.from_bytes(padded[4 * i:4 * i + 4], "big") for i in range(16))
    for t in range(16, R):
        s0 = ror(w[t - 15], 7) ^ ror(w[t - 15], 18) ^ (w[t - 15] >> 3)
        s1 = ror(w[t - 2], 17) ^ ror(w[t - 2], 19) ^ (w[t - 2] >> 10)
        w.append((w[t - 16] + s0 + w[t - 7] + s1) & MASK32)
    a, b, c, d, e, f, g, h = IV
    states = []
    for t in range(R):
        states.append((a, b, c, d, e, f, g, h))
        S1 = ror(e, 6) ^ ror(e, 11) ^ ror(e, 25)
        t1 = (h + S1 + ((e & f) ^ (~e & g)) + K[t] + w[t]) & MASK32
        S0 = ror(a, 2) ^ ror(a, 13) ^ ror(a, 22)
        t2 = (S0 + ((a & b) ^ (a & c) ^ (b & c))) & MASK32
        a, b, c, d, e, f, g, h = (t1 + t2) & MASK32, a, b, c, (d + t1) & MASK32, e, f, g
    digest = b"".join(((x + iv) & MASK32).to_bytes(4, "big") for x, iv in zip((a, b, c, d, e, f, g, h), IV))
    return states[R - 2], states[R - 1][4], digest


def scalar_digest(msg55, R):
    return scalar_state(msg55, R)[2]


def ref_key(msg55, R):
    st, e1, _ = scalar_state(msg55, R)
    return (st[0], st[1], st[4], st[5], e1 & ((1 << F_BITS) - 1))


def message(prefix, u):
    return b"".join(w.to_bytes(4, "big") for w in prefix) + (u & 0xFFFFFF).to_bytes(3, "big")


# ---------------------------------------------------------------- symbolic circuit
class Circuit:
    """Signals: ("c", bit) or (kind, id, flag) with kind 'g' (group / per-batch-constant) or 'v'.
    Gates: op in 0 xor, 1 and, 2 or, 3 andn (a & ~b). Inputs are ids 0..nin-1."""

    def __init__(self):
        self.op, self.ga, self.gb, self.gk = [], [], [], []
        self.nin = 0
        self.names = {}

    def inp(self, name, kind):
        i = self.nin
        self.nin += 1
        self.names[name] = i
        return (kind, i, 0)

    def new(self, kind, op, a, b):
        self.op.append(op); self.ga.append(a); self.gb.append(b); self.gk.append(kind)
        return self.nin + len(self.op) - 1

    @staticmethod
    def const(b):
        return ("c", 1 if b else 0)

    @staticmethod
    def kind(a, b):
        return "v" if a[0] == "v" or b[0] == "v" else "g"

    @staticmethod
    def flag(a):
        return a[2] if a[0] != "c" else None

    def xor(self, a, b):
        if a[0] == "c" and b[0] == "c":
            return ("c", a[1] ^ b[1])
        if a[0] == "c":
            a, b = b, a
        if b[0] == "c":
            return (a[0], a[1], a[2] ^ b[1])
        k = self.kind(a, b)
        return (k, self.new(k, 0, a[1], b[1]), a[2] ^ b[2])

    def neg(self, a):
        return ("c", 1 - a[1]) if a[0] == "c" else (a[0], a[1], a[2] ^ 1)

    def band(self, a, b):
        if a[0] == "c" and b[0] == "c":
            return ("c", a[1] & b[1])
        if a[0] == "c":
            a, b = b, a
        if b[0] == "c":
            return a if b[1] else ("c", 0)
        k = self.kind(a, b)
        if a[2] == 0 and b[2] == 0:
            return (k, self.new(k, 1, a[1], b[1]), 0)
        if a[2] == 1 and b[2] == 1:
            return (k, self.new(k, 2, a[1], b[1]), 1)
        if a[2] == 1:
            a, b = b, a
        return (k, self.new(k, 3, a[1], b[1]), 0)

    def bor(self, a, b):
        return self.neg(self.band(self.neg(a), self.neg(b)))

    def fa(self, x, y, c):
        ops = [x, y, c]
        fl = [self.flag(o) for o in ops]
        if any(f is None for f in fl):
            p = self.xor(x, y)
            return self.xor(p, c), self.bor(self.band(x, y), self.band(p, c))
        for i in range(3):
            j, k = (i + 1) % 3, (i + 2) % 3
            if fl[j] == fl[k]:
                x, y, c = ops[i], ops[j], ops[k]
                break
        p = self.xor(y, c)
        s = self.xor(x, p)
        x0 = (x[0], x[1], 0)
        if self.flag(x) == self.flag(y):
            if self.flag(x) == 0:
                return s, self.bor(self.band(y, c), self.band(p, x))
            return s, self.neg(self.bor(self.band(self.neg(y), self.neg(c)), self.band(p, x0)))
        if self.flag(x) == 1:
            return s, self.xor(self.bor(y, c), self.band(p, x0))
        return s, self.neg(self.xor(self.bor(self.neg(y), self.neg(c)), self.band(p, x0)))

    def addbit(self, xi, yi, c, last):
        if xi[0] == "c" and yi[0] != "c":
            xi, yi = yi, xi
        if yi[0] == "c":
            if yi[1]:
                return self.xor(self.neg(xi), c), (None if last else self.bor(xi, c))
            return self.xor(xi, c), (None if last else self.band(xi, c))
        if last:
            return self.xor(self.xor(xi, yi), c), None
        return self.fa(xi, yi, c)


class Adder:
    def __init__(self, cp, x, y):
        self.cp, self.x, self.y, self.c = cp, x, y, cp.const(0)

    def bit(self, j):
        s, self.c = self.cp.addbit(self.x[j], self.y[j], self.c, j == 31)
        return s


def build(R, layout):
    """layout 'fast': W13 bits 8..31 are 24 per-lane planes U0..U23 ('v'), prefix planes P ('g' per lane).
    layout 'counted': W13 bits 8..15 = fixed lane planes LN ('g'), bits 16..31 = batch planes B ('v')."""
    cp = Circuit()
    P = [[cp.inp("P%d" % (32 * w + i), "g") for i in range(32)] for w in range(13)]
    if layout == "fast":
        W13 = [cp.const((0x80 >> i) & 1) for i in range(8)] + [cp.inp("U%d" % i, "v") for i in range(24)]
    else:
        W13 = [cp.const((0x80 >> i) & 1) for i in range(8)] + [cp.inp("LN%d" % i, "g") for i in range(8)] + \
              [cp.inp("B%d" % i, "v") for i in range(16)]
    W = {i: P[i] for i in range(13)}
    W[13] = W13
    W[14] = [cp.const(0)] * 32
    W[15] = [cp.const((440 >> i) & 1) for i in range(32)]

    def constw(v):
        return [cp.const((v >> i) & 1) for i in range(32)]

    def sig_bits(x, rots, sh=None):
        def bit(j):
            terms = [x[(j + r) % 32] for r in rots]
            if sh is not None:
                terms.append(x[j + sh] if j + sh < 32 else cp.const(0))
            acc = terms[0]
            for tt in terms[1:]:
                acc = cp.xor(acc, tt)
            return acc
        return bit

    class Sched:
        def __init__(self, t):
            self.w7, self.w16 = word(t - 7), word(t - 16)
            self.b1 = sig_bits(word(t - 2), (17, 19), 10); self.b0 = sig_bits(word(t - 15), (7, 18), 3)
            self.s1w = [None] * 32; self.s0w = [None] * 32; self.tmp1 = [None] * 32; self.tmp2 = [None] * 32
            self.out = [None] * 32
            self.a1 = Adder(cp, self.s1w, self.w7); self.a2 = Adder(cp, self.s0w, self.w16); self.a3 = Adder(cp, self.tmp1, self.tmp2)

        def bit(self, j):
            self.s1w[j] = self.b1(j); self.s0w[j] = self.b0(j)
            self.tmp1[j] = self.a1.bit(j); self.tmp2[j] = self.a2.bit(j)
            self.out[j] = self.a3.bit(j)
            return self.out[j]

    def word(t):
        if t not in W:
            sc = Sched(t)
            W[t] = [sc.bit(j) for j in range(32)]
        return W[t]

    def ch_bit(e, f, g, j):
        p = cp.xor(f[j], g[j])
        fe, fp = cp.flag(e[j]), cp.flag(p)
        if fe is None or fp is None or fe == fp:
            return cp.xor(g[j], cp.band(e[j], p))
        return cp.xor(f[j], cp.band(cp.neg(e[j]), p))

    def maj_bit(a, b, c, bc, j, ab):
        fa_, fb, fc = cp.flag(a[j]), cp.flag(b[j]), cp.flag(c[j])
        abi = cp.xor(a[j], b[j]); ab[j] = abi
        if None in (fa_, fb, fc) or fa_ == fc:
            bci = bc[j] if bc is not None else cp.xor(b[j], c[j])
            return cp.xor(b[j], cp.band(abi, bci))
        if fb == fc:
            return cp.xor(a[j], cp.band(abi, cp.xor(a[j], c[j])))
        bci = bc[j] if bc is not None else cp.xor(b[j], c[j])
        return cp.xor(c[j], cp.band(cp.xor(a[j], c[j]), bci))

    a, b, c, d, e, f, g, h = [constw(v) for v in IV]
    bc = None
    f_out = None
    for t in range(R - 1):
        last = (t == R - 2)
        nb = F_BITS if last else 32
        wt = W.get(t)
        sc = None
        if wt is None:
            for uu in (t - 2, t - 7, t - 15, t - 16):
                word(uu)
            sc = Sched(t); wt = sc.out; W[t] = wt
        kwv = [None] * 32; s1w = [None] * 32; chw = [None] * 32; s0w = [None] * 32; mjw = [None] * 32
        tmpA = [None] * 32; tmpB = [None] * 32; t1 = [None] * 32; t2 = [None] * 32
        en = [None] * 32; an = [None] * 32; ab = [None] * 32
        kw_add = Adder(cp, wt, constw(K[t])); t1a = Adder(cp, h, s1w); t1b = Adder(cp, tmpA, chw); t1c = Adder(cp, tmpB, kwv)
        ea = Adder(cp, d, t1); t2a = Adder(cp, s0w, mjw); aa = Adder(cp, t1, t2)
        S1b = sig_bits(e, (6, 11, 25)); S0b = sig_bits(a, (2, 13, 22))
        for j in range(nb):
            if sc is not None:
                sc.bit(j)
            kwv[j] = kw_add.bit(j)
            s1w[j] = S1b(j)
            chw[j] = ch_bit(e, f, g, j)
            tmpA[j] = t1a.bit(j); tmpB[j] = t1b.bit(j); t1[j] = t1c.bit(j)
            en[j] = ea.bit(j)
            if not last:
                s0w[j] = S0b(j)
                mjw[j] = maj_bit(a, b, c, bc, j, ab)
                t2[j] = t2a.bit(j)
                an[j] = aa.bit(j)
        if last:
            f_out = en[:F_BITS]
            break
        h, g, f, e = g, f, e, en
        d, c, b, a = c, b, a, an
        bc = ab
    key = list(a) + list(b) + list(e) + list(f) + list(f_out)     # 144 signals
    return cp, key


def live_gates(cp, key):
    nin = cp.nin
    need = bytearray(len(cp.op))
    stack = [s[1] for s in key if s[0] != "c" and s[1] >= nin]
    while stack:
        n = stack.pop()
        gi = n - nin
        if need[gi]:
            continue
        need[gi] = 1
        for s in (cp.ga[gi], cp.gb[gi]):
            if s >= nin:
                stack.append(s)
    return [i for i in range(len(cp.op)) if need[i]]


# ---------------------------------------------------------------- fast path: chunked compile
def compile_fast(R):
    cp, key = build(R, "fast")
    live = live_gates(cp, key)
    nin = cp.nin
    OPS = ("v[%d]=v[%d]^v[%d]", "v[%d]=v[%d]&v[%d]", "v[%d]=v[%d]|v[%d]", "v[%d]=v[%d]&(v[%d]^M)")
    g_lines, v_lines = [], []
    for gi in live:
        line = OPS[cp.op[gi]] % (nin + gi, cp.ga[gi], cp.gb[gi])
        (g_lines if cp.gk[gi] == "g" else v_lines).append(line)

    def chunked(lines, tag):
        funcs = []
        for c0 in range(0, len(lines), 1500):
            src = "def C(v):\n " + "\n ".join(lines[c0:c0 + 1500]) + "\n"
            env = {"M": M}
            exec(compile(src, "<%s-%d>" % (tag, c0), "exec"), env)
            funcs.append(env["C"])
        return funcs

    gf = chunked(g_lines, "group-r%d" % R)
    vf = chunked(v_lines, "step-r%d" % R)
    outs = []
    for s in key:
        if s[0] == "c":
            outs.append("M" if s[1] else "0")
        elif s[2]:
            outs.append("(v[%d]^M)" % s[1])
        else:
            outs.append("v[%d]" % s[1])
    env = {"M": M}
    exec(compile("def OUT(v):\n return [" + ",".join(outs) + "]\n", "<out-r%d>" % R, "exec"), env)
    OUT = env["OUT"]
    nslots = nin + len(cp.op)
    counts = {"g_gates": len(g_lines), "v_gates": len(v_lines)}
    pid = [cp.names["P%d" % i] for i in range(416)]
    uid = [cp.names["U%d" % i] for i in range(24)]

    def G(P):
        v = [0] * nslots
        for i, s in enumerate(pid):
            v[s] = P[i]
        for fn in gf:
            fn(v)
        return v

    def F(v, U):
        for i, s in enumerate(uid):
            v[s] = U[i]
        for fn in vf:
            fn(v)
        return OUT(v)

    del cp
    return G, F, counts


def prefix_planes(prefixes):
    planes = [0] * 416
    for j, pref in enumerate(prefixes):
        bit = 1 << j
        for w in range(13):
            v = pref[w]
            base = 32 * w
            for i in range(32):
                if (v >> i) & 1:
                    planes[base + i] |= bit
    return planes


def u_planes(us):
    planes = [0] * 24
    for j, u in enumerate(us):
        for i in range(24):
            if (u >> i) & 1:                # W13 bit 8+i = u bit i
                planes[i] |= 1 << j
    return planes


def lane_values(planes):
    rows = [format(p, "0256b") for p in reversed(planes)]
    vals = [int("".join(col), 2) for col in zip(*rows)]
    vals.reverse()
    return vals


def key_words(key, j):
    out = []
    for w in range(4):
        out.append(sum(((key[32 * w + i] >> j) & 1) << i for i in range(32)))
    out.append(sum(((key[128 + i] >> j) & 1) << i for i in range(F_BITS)))
    return out


def h_low(key, bits):
    """low `bits` bits of digest word h = f + IV7 (f = e entering round R-3) for every lane"""
    e_low = lane_values(key[96:96 + bits])
    mask = (1 << bits) - 1
    return [(v + IV[7]) & mask for v in e_low]


# ---------------------------------------------------------------- counted program (proof Appendix A)
def allocate(cp, order, outputs, nregs, group_ids):
    """Furthest-next-use allocation over `nregs` physical registers. Emits instructions with register
    numbers: (0 xor | 1 and | 2 or, rd, ra, rb, n, a, b) ; (4 load, r, v) ; (5 store, r, v) ; (6 not, rd, ra, n, b).
    The value ids carried alongside let the VM detect a stale register."""
    nin = cp.nin
    uses = {}
    for i, gi in enumerate(order):
        uses.setdefault(cp.ga[gi], []).append(i); uses.setdefault(cp.gb[gi], []).append(i)
    L = len(order)
    for o in outputs:
        uses.setdefault(o, []).append(L)
    ptr = {}
    BIG = 1 << 40

    def next_use(v, i):
        lst = uses.get(v, ())
        p = ptr.get(v, 0)
        while p < len(lst) and lst[p] <= i:
            p += 1
        ptr[v] = p
        return lst[p] if p < len(lst) else BIG

    reg_of, val_of = {}, {}
    in_mem = set(range(nin)) | set(group_ids)      # inputs and group-constant results live in memory
    free = list(range(nregs))
    prog = []
    cnt = {"load": 0, "store": 0, "xor": 0, "and": 0, "or": 0, "andnot": 0}

    def evict(i, protect):
        best = None; bestv = None
        for r, v in val_of.items():
            if v in protect:
                continue
            sc = (next_use(v, i), 1 if v in in_mem else 0)
            if best is None or sc > best:
                best, bestv = sc, v
        r = reg_of.pop(bestv); del val_of[r]
        if best[0] < BIG and bestv not in in_mem:
            prog.append((5, r, bestv)); cnt["store"] += 1; in_mem.add(bestv)
        return r

    def ensure(v, i, protect):
        if v in reg_of:
            return reg_of[v]
        r = free.pop() if free else evict(i, protect)
        reg_of[v] = r; val_of[r] = v
        prog.append((4, r, v)); cnt["load"] += 1
        return r

    for i, gi in enumerate(order):
        a, b, n = cp.ga[gi], cp.gb[gi], nin + gi
        ra = ensure(a, i, {a, b}); rb = ensure(b, i, {a, b})
        for v in (a, b):
            if next_use(v, i) >= BIG and v in reg_of:
                r = reg_of.pop(v); del val_of[r]; free.append(r)
        rd = free.pop() if free else evict(i, {a, b})
        reg_of[n] = rd; val_of[rd] = n
        op = cp.op[gi]
        if op == 3:                                   # n = a & ~b, two instructions, clobber-safe
            cnt["andnot"] += 1
            if rd == ra:
                prog.append((2, rd, ra, rb, n, a, b))          # rd = a | b
                prog.append((0, rd, rd, rb, n, n, b))          # rd = (a | b) ^ b
            else:
                prog.append((6, rd, rb, n, b))                 # rd = ~b
                prog.append((1, rd, ra, rd, n, a, n))          # rd = a & ~b
        else:
            prog.append((op, rd, ra, rb, n, a, b)); cnt[("xor", "and", "or")[op]] += 1
        if next_use(n, i) >= BIG:
            r = reg_of.pop(n); del val_of[r]; free.append(r)
    for o in outputs:
        if o not in in_mem:
            prog.append((5, reg_of[o], o)); cnt["store"] += 1; in_mem.add(o)
    return prog, cnt


def delta_mask(s):
    return sum(1 << i for i in range(256) if not (i & s))


def counted_witness(R, rng, nregs=NREGS, check_total=True):
    """Regenerate, allocate and execute the counted batch program on one full-scale batch."""
    cp, key = build(R, "counted")
    live = live_gates(cp, key)
    nin = cp.nin
    gg = [gi for gi in live if cp.gk[gi] == "g"]
    vv = [gi for gi in live if cp.gk[gi] == "v"]
    outputs = [s[1] for s in key if s[0] != "c"]
    prog, cnt = allocate(cp, vv, outputs, nregs, set(nin + gi for gi in gg))
    prefix = [rng.getrandbits(32) for _ in range(13)]
    bidx = rng.getrandbits(16)
    gidx = rng.getrandbits(104)                 # group index g < 2^104
    rtag = rng.getrandbits(128)                 # RTAG: one uniform 128-bit word per run
    mem = {}
    for w in range(13):
        for i in range(32):
            mem[cp.names["P%d" % (32 * w + i)]] = M if (prefix[w] >> i) & 1 else 0
    for i in range(8):
        mem[cp.names["LN%d" % i]] = LANE_PLANES[i]
    setup = 0
    for i in range(16):                          # batch setup: 16 batch planes x 4 ops
        t = bidx >> i; t &= 1; p = (0 - t) & M; mem[cp.names["B%d" % i]] = p; setup += 4
    bidl = (rtag << 128) | ((gidx << 24) | (bidx << 8)); setup += 3   # batch id word: shl, or, or
    setup += 3                                                        # loop: add, compare, branch
    for gi in gg:                                # group gates: per group, not charged per batch
        x, y = mem[cp.ga[gi]], mem[cp.gb[gi]]
        op = cp.op[gi]
        mem[nin + gi] = x ^ y if op == 0 else (x & y if op == 1 else (x | y if op == 2 else x & (y ^ M)))
    # physical register machine: the circuit registers 0..nregs-1 hold (value id, word)
    regs = [None] * nregs

    def rd_(r, v):
        require(regs[r] is not None and regs[r][0] == v, "stale register %d" % r)
        return regs[r][1]

    for ins in prog:
        k = ins[0]
        if k == 4:
            regs[ins[1]] = (ins[2], mem[ins[2]])
        elif k == 5:
            mem[ins[2]] = rd_(ins[1], ins[2])
        elif k == 6:
            regs[ins[1]] = (ins[3], rd_(ins[2], ins[4]) ^ M)
        else:
            x = rd_(ins[2], ins[5]); y = rd_(ins[3], ins[6])
            regs[ins[1]] = (ins[4], x ^ y if k == 0 else (x & y if k == 1 else x | y))
    stored = []                                  # the STORED key plane words (polarity not applied)
    pol = 0
    for i, sg in enumerate(key):
        if sg[0] == "c":
            stored.append(M if sg[1] else 0)
        else:
            stored.append(mem[sg[1]])
            if sg[2]:
                pol |= 1 << i
    # transpose of the stored words: rows 0..110 zero, 111..254 key planes, 255 all-ones
    rows = [0] * KEY_ROW0 + stored + [M]
    require(len(rows) == 256, "row layout")
    zero = [r < KEY_ROW0 for r in range(256)]    # zero-row cases from the layout, not from data
    masks = {s: delta_mask(s) for s in (1, 2, 4, 8, 16, 32, 64, 128)}
    t_ops = 0
    t_loads = 8                                  # the eight swap masks m_1..m_128, loaded once per batch
    t_stores = 0

    def swap(r1, r2, s):
        nonlocal t_ops
        if zero[r1] and zero[r2]:
            return
        t_ops += 3 if zero[r1] else (4 if zero[r2] else 6)
        zero[r1] = zero[r2] = False
        x, y = rows[r1], rows[r2]
        t = ((x >> s) ^ y) & masks[s]
        rows[r2] = y ^ t
        rows[r1] = x ^ (t << s)

    for blk in range(8):
        rr = range(32 * blk, 32 * blk + 32)
        if all(zero[r] for r in rr):
            continue
        t_loads += sum(1 for r in rr if not zero[r])
        for s in (1, 2, 4, 8, 16):
            for r in rr:
                if not (r & s):
                    swap(r, r + s, s)
        t_stores += sum(1 for r in rr if not zero[r])
    table = {}
    tab_ops = 0
    cand = 0
    BIDL = bidl                                  # (RTAG << 128) | id, id = g*2^24 + b*2^8 + L; += 1 per lane
    for r0 in range(32):
        rr = [r0 + 32 * k for k in range(8)]
        t_loads += sum(1 for r in rr if not zero[r])
        for s in (32, 64, 128):
            for r in rr:
                if not (r & s):
                    swap(r, r + s, s)
        for r in rr:                            # table sink: 9 ops per lane
            Kw = rows[r]
            idx = Kw >> KEY_ROW0                # 1: addresses in [2^144, 2^145)
            e = table.get(idx)                  # 2: LOAD T[idx] (never-written slots hold seeded garbage)
            if e is None:
                e = int.from_bytes(hashlib.sha256(b"garbage%d" % idx).digest() * 8, "big") & M
            x = Kw ^ BIDL                       # 3
            y = x ^ e                           # 4
            zc = y >> 128                       # 5
            if zc == 0:                         # 6 compare, 7 branch to CANDIDATE
                cand += 1
            table[idx] = x                      # 8: STORE T[idx] = x
            BIDL = BIDL + 1                     # 9: next lane's id (no carry into RTAG: id < 2^128)
            tab_ops += 9
    # reference check of every lane: key words (polarity applied in the check) and the addresses of the
    # stored words, i.e. the reference key XOR the public polarity constant pol
    bad = 0
    planes = [w ^ (M if (pol >> i) & 1 else 0) for i, w in enumerate(stored)]
    for L in range(256):
        u = 256 * bidx + L
        rk = ref_key(message(prefix, u), R)
        if key_words(planes, L) != list(rk):
            bad += 1
        kint = rk[0] | (rk[1] << 32) | (rk[2] << 64) | (rk[3] << 96) | (rk[4] << 128)
        exp = ((kint ^ pol) << KEY_ROW0) | (1 << 255)
        if rows[L] != exp:
            bad += 1
    require(bad == 0, "counted program disagrees with the scalar reference on %d lanes" % bad)
    circuit = cnt["xor"] + cnt["and"] + cnt["or"] + 2 * cnt["andnot"]
    total = circuit + cnt["load"] + cnt["store"] + t_ops + t_loads + t_stores + tab_ops + setup
    ledger = {"w_xor": cnt["xor"], "w_and": cnt["and"], "w_or": cnt["or"], "w_andnot": cnt["andnot"],
              "loads": cnt["load"], "stores": cnt["store"], "transpose_ops": t_ops, "transpose_loads": t_loads,
              "transpose_stores": t_stores, "table_ops": tab_ops, "setup_ops": setup, "total": total}
    if check_total:
        require(total == EXPECTED_TOTAL[R], "counted batch total %d differs from the charged %d" % (total, EXPECTED_TOTAL[R]))
    mem_ops = cnt["load"] + cnt["store"] + t_loads + t_stores
    return ledger, mem_ops, cand


# ---------------------------------------------------------------- experiments
LAYOUTS = {
    "r-bs-full-width": (256, [0, 1]),
    "r-bs-spread": (16, list(range(32))),
    "r-bs-single-group": (1, list(range(512))),
    "r-bs-high-z": (4, [v << 17 for v in range(128)]),
}


def run_batch(G, F, items):
    """items: up to 256 (prefix, u). Returns the 144 key planes."""
    v = G(prefix_planes([it[0] for it in items]))
    return F(v, u_planes([it[1] for it in items]))


def equivalence_trial(G, F, rng, R, obs):
    prefixes = [[rng.getrandbits(32) for _ in range(13)] for _ in range(256)]
    us = [rng.getrandbits(24) for _ in range(256)]
    key = run_batch(G, F, list(zip(prefixes, us)))
    for j in (0, 85, 170, 255):
        if key_words(key, j) != list(ref_key(message(prefixes[j], us[j]), R)):
            sys.stderr.write("bit-sliced key words differ from the scalar reference\n")
            sys.exit(1)
    obs["checked_lanes"] = 4
    vals = h_low(key, 12)
    seen = {}
    for j in range(256):
        if vals[j] in seen:
            i0 = seen[vals[j]]
            return message(prefixes[i0], us[i0]), message(prefixes[j], us[j])
        seen[vals[j]] = j
    return None


def search_trials(G, F, R, trials, groups, us_list, obs_list):
    """Each trial: `groups` prefixes x us_list (512 messages), processed in the fixed order
    (group-major within the trial, u ascending); a trial's messages are spread over batches of
    256 lanes shared with other trials. First match of two distinct messages ends the trial."""
    per_trial = groups * len(us_list)
    items = []          # (trial k, prefix, u)
    for k, (tid, rng) in enumerate(trials):
        prefixes = [[rng.getrandbits(32) for _ in range(13)] for _ in range(groups)]
        for gi in range(groups):
            for u in us_list:
                items.append((k, prefixes[gi], u))
    tables = [dict() for _ in trials]
    result = [None] * len(trials)
    for b0 in range(0, len(items), 256):
        chunk = items[b0:b0 + 256]
        key = run_batch(G, F, [(p, u) for _, p, u in chunk])
        vals = h_low(key, 18)
        for j, (k, p, u) in enumerate(chunk):
            if result[k] is not None:
                continue
            kv = vals[j]
            tab = tables[k]
            if kv in tab:
                p0, u0 = tab[kv]
                ma, mb = message(p0, u0), message(p, u)
                if ma == mb:
                    continue
                result[k] = (ma, mb)
            else:
                tab[kv] = (p, u)
    for k in range(len(trials)):
        obs_list[k]["inserted"] = len(tables[k])
        obs_list[k]["messages"] = per_trial
    return result


def main():
    req = json.loads(sys.stdin.read())
    exp = req["experiment_id"]
    prof = req.get("target_profile", "sha256-r38-prefix-v1")
    R = 37 if "r37" in prof else 38
    G, F, counts = compile_fast(R)
    trials = req["trials"]
    rows = [None] * len(trials)
    obs_list = []
    rngs = []
    for t in trials:
        rngs.append(random_from_seed(t["seed"]))
        obs_list.append(dict(counts))
        obs_list[-1]["rounds"] = R
    # counted witness on trial 0 (its own derived seed; the trial's search uses the trial rng unchanged)
    if trials:
        wrng = random_from_seed(hashlib.sha256(("witness" + trials[0]["seed"]).encode()).hexdigest())
        nregs = NREGS
        if "--nregs" in sys.argv:                      # development switch only; the shipped run uses 58
            nregs = int(sys.argv[sys.argv.index("--nregs") + 1])
        led, _, _ = counted_witness(R, wrng, nregs, check_total=(nregs == NREGS))
        obs_list[0] = {"rounds": R, "w_total": led["total"], "w_xor": led["w_xor"], "w_and": led["w_and"],
                       "w_or": led["w_or"], "w_andnot": led["w_andnot"], "w_loads": led["loads"],
                       "w_stores": led["stores"],
                       "w_transpose": led["transpose_ops"] + led["transpose_loads"] + led["transpose_stores"],
                       "w_table": led["table_ops"], "w_setup": led["setup_ops"]}
    if exp == "r-bs-fullwidth-equivalence":
        pairs = [equivalence_trial(G, F, rngs[i], R, obs_list[i]) for i in range(len(trials))]
    else:
        groups, us_list = LAYOUTS[exp]
        pairs = search_trials(G, F, R, list(zip(range(len(trials)), rngs)), groups, us_list, obs_list)
    mask_bits = 12 if exp == "r-bs-fullwidth-equivalence" else 18
    out = []
    for i, t in enumerate(trials):
        pr = pairs[i]
        if pr is None:
            ma = mb = None
        else:
            a, b = pr
            da, db = scalar_digest(a, R), scalar_digest(b, R)
            require(a != b and (int.from_bytes(da[28:32], "big") ^ int.from_bytes(db[28:32], "big")) & ((1 << mask_bits) - 1) == 0,
                    "returned pair fails its own check")
            ma, mb = a.hex(), b.hex()
        out.append({"trial": t["trial"], "message_a_hex": ma, "message_b_hex": mb, "observations": obs_list[i]})
    sys.stdout.write(json.dumps({"schema_version": 1, "trials": out}, sort_keys=True, separators=(",", ":")))


def random_from_seed(seed_hex):
    import random
    return random.Random(int(seed_hex, 16))


if __name__ == "__main__":
    main()
