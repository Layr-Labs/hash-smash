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
and EXECUTED on one batch of the full-scale family (one group prefix, one 16-bit batch index and
the run tag from the seed, 256 lanes). One straight-line SSA program holds the circuit (every
multi-operand sum with its constant and group-constant addends folded into one group word; mixed-
polarity carries taken as one AND with the sum's stored word, so no NOT is materialised), the zero-
aware delta-swap transpose (rows 0..110 zero, 111..254 the key planes, 255 all-ones; 6 ops per swap,
3 when the lower row is zero, 4 when the upper row is zero; the swap masks and the all-ones row are
memory words loaded like any operand) and the 256 table sinks (idx = Kw >> 111; e = LOAD T[idx];
x = Kw ^ BIDL; y = x ^ e; z = y >> 128; compare; branch; STORE T[idx] = x; BIDL += 1; the sinks run in
the phase-2 order L = rotr8(n, 3) for n = 0..255, so lane L's stored id has lane field rotl8(L, 3), and the
witness decodes every stored entry back to (g, b, L) and the run tag). It is
allocated over 58 registers by furthest-next-use eviction with explicit loads and stores and run
on a register machine that reads operands by register number (a stale register aborts). The key
planes are compared with the scalar reference and every sunk row with the transpose of the planes;
any mismatch aborts. The exact totals asserted are 45773 ops at R = 37 and 48091 at R = 38.
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
EXPECTED_TOTAL = {37: 45773, 38: 48091}
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

    def raw_and(self, a, b, resflag):
        k = self.kind(a, b)
        return (k, self.new(k, 1, a[1], b[1]), resflag)

    def mixed_carry(self, u, v, s, k):
        """carry = u AND v (k = 0) or u OR v (k = 1) for non-constant u, v of different polarity, given the
        sum s whose stored word is U ^ V: one AND of the right operand's stored word with S."""
        if not OPT.get("nonot", True):
            return self.band(u, v) if k == 0 else self.bor(u, v)
        if self.flag(u) == self.flag(v):
            return self.band(u, v) if k == 0 else self.bor(u, v)
        want = 0 if k == 0 else 1
        w = u if self.flag(u) == want else v
        return self.raw_and(w, s, k)

    def addbit(self, xi, yi, c, last):
        if xi[0] == "c" and yi[0] != "c":
            xi, yi = yi, xi
        if yi[0] == "c":
            k = yi[1]
            s = self.xor(self.neg(xi) if k else xi, c)
            if last:
                return s, None
            if c[0] == "c":
                return s, (self.bor(xi, c) if k else self.band(xi, c))
            return s, self.mixed_carry(xi, c, s, k)
        if last:
            return self.xor(self.xor(xi, yi), c), None
        if c[0] == "c":
            k = c[1]
            s = self.xor(self.neg(xi) if k else xi, yi)
            return s, self.mixed_carry(xi, yi, s, k)
        return self.fa(xi, yi, c)


class Adder:
    def __init__(self, cp, x, y):
        self.cp, self.x, self.y, self.c = cp, x, y, cp.const(0)

    def bit(self, j):
        s, self.c = self.cp.addbit(self.x[j], self.y[j], self.c, j == 31)
        return s


OPT_BY_R = {38: {'g_first': True, 'evict': 'clean', 't1_perm': (3, 4, 0, 2, 1), 's_perm': (3, 1, 0, 2), 't2_swap': True, 'a_first': True}, 37: {'g_first': True, 'evict': 'clean', 't1_perm': (3, 4, 0, 2, 1), 's_perm': (3, 1, 0, 2), 't2_swap': True, 'a_first': True}}
BLOCK_ORDER = {38: [6, 3, 4, 7, 5], 37: [6, 7, 3, 4, 5]}
OPT = {}


def build(R, layout, order=None):
    """layout 'fast': W13 bits 8..31 are 24 per-lane planes U0..U23 ('v'), prefix planes P ('g' per lane).
    layout 'counted': W13 bits 8..15 = fixed lane planes LN ('g'), bits 16..31 = batch planes B ('v').
    v2: every multi-operand sum folds its constant and group-constant addends (including K_t) into one
    group word (group gates, computed once per group), so the per-batch program adds only the
    message-dependent addends plus at most one folded word. `order` is a tuple of options for the search."""
    opt = dict(OPT); opt.update(order or {})
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

    def wkind(word):
        k = "c"
        for s in word:
            if s[0] == "v":
                return "v"
            if s[0] == "g":
                k = "g"
        return k

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

    class Lazy:
        """a word whose bits are produced on demand in lock step; kind fixed at construction"""
        def __init__(self, kind, fn):
            self.kind, self.fn, self.cache = kind, fn, {}

        def __getitem__(self, j):
            if j not in self.cache:
                self.cache[j] = self.fn(j)
            return self.cache[j]

    def sigma_word(x, rots, sh=None):
        k = wkind(x)
        f = sig_bits(x, rots, sh)
        if k != "v":
            return [f(j) for j in range(32)], k          # group/const: whole word now (hoisted)
        return Lazy("v", f), "v"

    def full_word_add(x, y):
        ad = Adder(cp, x, y)
        return [ad.bit(j) for j in range(32)]

    class MSum:
        """sum of terms (word, kind). Constants and group words are folded first (group gates);
        message-dependent words are chained in the given order, the folded word added last
        (or first if opt['g_first'])."""
        def __init__(self, terms, nbits=32):
            cval = 0
            gw = []
            vw = []
            for word, k in terms:
                if k == "c":
                    cval = (cval + sum(((word[i][1]) << i) for i in range(32))) & MASK32
                elif k == "g":
                    gw.append(word)
                else:
                    vw.append(word)
            G = None
            for w_ in gw:
                G = w_ if G is None else full_word_add(G, w_)
            if cval:
                G = constw(cval) if G is None else full_word_add(G, constw(cval))
            elif G is None and not vw:
                G = constw(0)
            ops = list(vw)
            if G is not None:
                if opt.get("g_first"):
                    ops = [G] + ops
                else:
                    ops = ops + [G]
            self.ops = ops
            self.single = len(ops) == 1
            self.adders = []
            self.out = [None] * 32
            if not self.single:
                acc = ops[0]
                for nxt in ops[1:]:
                    prev = self.out if False else None
                    ad = Adder(cp, acc if not isinstance(acc, Adder) else None, nxt)
                    self.adders.append(ad)
                    acc = ad

        def bit(self, j):
            if self.single:
                self.out[j] = self.ops[0][j]
                return self.out[j]
            x = self.ops[0][j]
            for k, ad in enumerate(self.adders):
                y = self.ops[k + 1][j]
                s, ad.c = cp.addbit(x, y, ad.c, j == 31)
                x = s
            self.out[j] = x
            return x

    def msum_kind(terms):
        ks = [k for _, k in terms]
        return "v" if "v" in ks else ("g" if "g" in ks else "c")

    def word(t):
        """materialise W_t as a complete word (used for words needed before their round)."""
        if t not in W:
            for uu in (t - 2, t - 7, t - 15, t - 16):
                word(uu)
            terms = sched_terms(t)
            ms = MSum(terms)
            W[t] = [ms.bit(j) for j in range(32)]
        return W[t]

    def sched_terms(t):
        s1, k1 = sigma_word(word(t - 2), (17, 19), 10)
        s0, k0 = sigma_word(word(t - 15), (7, 18), 3)
        w7, w16 = word(t - 7), word(t - 16)
        tl = [(s1, k1), (w7, wkind(w7)), (s0, k0), (w16, wkind(w16))]
        p = opt.get("s_perm")
        return [tl[i] for i in p] if p else tl

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
        # schedule word W_t: existing, or built in lock step from its folded terms
        if t in W:
            wt, wk = W[t], wkind(W[t])
            sched = None
        else:
            for uu in (t - 2, t - 7, t - 15, t - 16):
                word(uu)
            sterms = sched_terms(t)
            sk = msum_kind(sterms)
            if sk != "v":
                ms = MSum(sterms); W[t] = [ms.bit(j) for j in range(32)]
                wt, wk, sched = W[t], sk, None
            else:
                sched = MSum(sterms)
                wt, wk = Lazy("v", sched.bit), "v"
                W[t] = None
        ek, fk, gk = wkind(e), wkind(f), wkind(g)
        S1, s1k = (Lazy("v", sig_bits(e, (6, 11, 25))), "v") if ek == "v" else sigma_word(e, (6, 11, 25))
        chk = "v" if "v" in (ek, fk, gk) else ("g" if "g" in (ek, fk, gk) else "c")
        if chk == "v":
            CH = Lazy("v", lambda j, e=e, f=f, g=g: ch_bit(e, f, g, j))
        else:
            CH = [ch_bit(e, f, g, j) for j in range(32)]
        t1terms = [(h, wkind(h)), (S1, s1k), (CH, chk), (constw(K[t]), "c"), (wt, wk)]
        if opt.get("t1_order") == "w_first":
            t1terms = [t1terms[4], t1terms[0], t1terms[1], t1terms[2], t1terms[3]]
        if opt.get("t1_perm"):
            t1terms = [t1terms[i] for i in opt["t1_perm"]]
        T1 = MSum(t1terms)
        t1w = Lazy("v", T1.bit) if msum_kind(t1terms) == "v" else None
        if t1w is None:
            t1full = [T1.bit(j) for j in range(32)]
            t1src, t1k = t1full, msum_kind(t1terms)
        else:
            t1src, t1k = t1w, "v"
        dk = wkind(d)
        EA = MSum([(t1src, t1k), (d, dk)] if opt.get("ea_swap") else [(d, dk), (t1src, t1k)])
        en = [None] * 32
        an = [None] * 32
        ab = [None] * 32
        if not last:
            ak, bk, ck = wkind(a), wkind(b), wkind(c)
            S0, s0k = (Lazy("v", sig_bits(a, (2, 13, 22))), "v") if ak == "v" else sigma_word(a, (2, 13, 22))
            mk = "v" if "v" in (ak, bk, ck) else "g"
            MJ = Lazy(mk, lambda j, a=a, b=b, c=c, bc=bc, ab=ab: maj_bit(a, b, c, bc, j, ab))
            if mk != "v":
                MJ = [MJ[j] for j in range(32)]
            T2 = MSum([(MJ, mk), (S0, s0k)] if opt.get("t2_swap") else [(S0, s0k), (MJ, mk)])
            t2k = "v" if "v" in (s0k, mk) else "g"
            t2src = Lazy("v", T2.bit) if t2k == "v" else [T2.bit(j) for j in range(32)]
            AA = MSum([(t2src, t2k), (t1src, t1k)] if opt.get("aa_swap") else [(t1src, t1k), (t2src, t2k)])
        for j in range(nb):
            if sched is not None:
                wt[j]
            if not last and opt.get("t2_early") and t2k == "v":
                t2src[j]
            if t1w is not None:
                t1w[j]
            if not last and opt.get("a_first"):
                an[j] = AA.bit(j)
                en[j] = EA.bit(j)
            else:
                en[j] = EA.bit(j)
                if not last:
                    an[j] = AA.bit(j)
        if sched is not None:
            W[t] = [wt[j] for j in range(32)] if not last else None
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
    OPT.clear(); OPT.update(OPT_BY_R[R])
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
def delta_mask(s):
    return sum(1 << i for i in range(256) if not (i & s))


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
        OPT.clear(); OPT.update(OPT_BY_R[R])
        led = counted_witness2(R, wrng, nregs, block_order=BLOCK_ORDER[R])
        if nregs == NREGS:
            require(led["total"] == EXPECTED_TOTAL[R],
                    "counted batch total %d differs from the charged %d" % (led["total"], EXPECTED_TOTAL[R]))
        obs_list[0] = {"rounds": R, "w_total": led["total"], "w_xor": led["xor"], "w_and": led["and"],
                       "w_or": led["or"], "w_andnot": led["andnot"], "w_shift": led["shift"],
                       "w_loads": led["loads"], "w_stores": led["stores"], "w_table": led["table"],
                       "w_setup": led["setup"], "w_garbage": led["garbage"]}
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




# ---------------------------------------------------------------- v2: one allocation for circuit + transpose + sinks
TOPS = {"xor": 0, "and": 1, "or": 2, "andn": 3}


def build_program(cp, key, vv, rowmap, block_order, set_order):
    """Return (ops, outputs_consumed, zero_info). ops: tuples (kind, n, a, b, imm):
       kind in xor/and/or/andn (circuit; a, b value ids), shr/shl (a, imm), sink (a)."""
    nin = cp.nin
    ops = [(("xor", "and", "or", "andn")[cp.op[gi]], nin + gi, cp.ga[gi], cp.gb[gi], None) for gi in vv]
    nxt = [nin + len(cp.op) + 16]
    MASKID = {s: nin + len(cp.op) + i for i, s in enumerate((1, 2, 4, 8, 16, 32, 64, 128))}
    ONES = nin + len(cp.op) + 8

    def new():
        nxt[0] += 1
        return nxt[0]

    rows = [None] * 256                     # None = structurally zero row
    for i, sg in enumerate(key):
        rows[rowmap[i]] = sg[1]
    rows[255] = ONES

    def swap(r1, r2, s):
        x, y = rows[r1], rows[r2]
        if x is None and y is None:
            return
        m = MASKID[s]
        if x is None:                       # lower row zero: t = y & m ; y' = y ^ t ; x' = t << s
            t = new(); ops.append(("and", t, y, m, None))
            y2 = new(); ops.append(("xor", y2, y, t, None))
            x2 = new(); ops.append(("shl", x2, t, None, s))
        elif y is None:                     # upper row zero: t = (x >> s) & m ; y' = t ; x' = x ^ (t << s)
            a1 = new(); ops.append(("shr", a1, x, None, s))
            t = new(); ops.append(("and", t, a1, m, None))
            y2 = t
            a2 = new(); ops.append(("shl", a2, t, None, s))
            x2 = new(); ops.append(("xor", x2, x, a2, None))
        else:
            a1 = new(); ops.append(("shr", a1, x, None, s))
            a2 = new(); ops.append(("xor", a2, a1, y, None))
            t = new(); ops.append(("and", t, a2, m, None))
            y2 = new(); ops.append(("xor", y2, y, t, None))
            a3 = new(); ops.append(("shl", a3, t, None, s))
            x2 = new(); ops.append(("xor", x2, x, a3, None))
        rows[r1], rows[r2] = x2, y2

    for blk in block_order:
        rr = range(32 * blk, 32 * blk + 32)
        if all(rows[r] is None for r in rr):
            continue
        for s in (1, 2, 4, 8, 16):
            for r in rr:
                if not (r & s):
                    swap(r, r + s, s)
    for r0 in set_order:
        rr = [r0 + 32 * k for k in range(8)]
        for s in (32, 64, 128):
            for r in rr:
                if not (r & s):
                    swap(r, r + s, s)
        for r in rr:
            ops.append(("sink", None, rows[r], None, r))
    return ops, MASKID, ONES


def allocate2(ops, mem_ids, nregs):
    """Furthest-next-use over nregs; every operand not in a register is loaded; evicted values still
    needed and not in memory are stored. Emits register-numbered instructions:
      (op, rd, ra, rb, n, a, b) op 0 xor 1 and 2 or ; (4 load r v) ; (5 store r v) ; (6 not rd ra n b) ;
      (7 shr rd ra n a imm) ; (8 shl rd ra n a imm) ; (9 sink ra a row)."""
    uses = {}
    for i, o in enumerate(ops):
        for v in (o[2], o[3]):
            if v is not None:
                uses.setdefault(v, []).append(i)
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
    in_mem = set(mem_ids)
    free = list(range(nregs))
    prog = []
    cnt = {"load": 0, "store": 0, "xor": 0, "and": 0, "or": 0, "andnot": 0, "shift": 0, "sink": 0,
           "c_load": 0, "c_store": 0}
    phase = ["c"]

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
            if phase[0] == "c":
                cnt["c_store"] += 1
        return r

    def ensure(v, i, protect):
        if v in reg_of:
            return reg_of[v]
        r = free.pop() if free else evict(i, protect)
        reg_of[v] = r; val_of[r] = v
        prog.append((4, r, v)); cnt["load"] += 1
        if phase[0] == "c":
            cnt["c_load"] += 1
        return r

    def release(v, i):
        if v is not None and next_use(v, i) >= BIG and v in reg_of:
            r = reg_of.pop(v); del val_of[r]; free.append(r)

    for i, o in enumerate(ops):
        kind, n, a, b, imm = o
        if kind in ("shr", "shl", "sink"):
            phase[0] = "t"
        prot = {a, b}
        ra = ensure(a, i, prot)
        rb = ensure(b, i, prot) if b is not None else None
        if kind == "sink":
            prog.append((9, ra, a, imm)); cnt["sink"] += 1
            release(a, i)
            continue
        release(a, i); release(b, i)
        rd = free.pop() if free else evict(i, prot)
        reg_of[n] = rd; val_of[rd] = n
        if kind == "andn":
            cnt["andnot"] += 1
            if rd == ra:
                prog.append((2, rd, ra, rb, n, a, b))
                prog.append((0, rd, rd, rb, n, n, b))
            else:
                prog.append((6, rd, rb, n, b))
                prog.append((1, rd, ra, rd, n, a, n))
        elif kind in ("shr", "shl"):
            cnt["shift"] += 1
            prog.append((7 if kind == "shr" else 8, rd, ra, n, a, imm))
        else:
            prog.append((TOPS[kind], rd, ra, rb, n, a, b)); cnt[kind] += 1
        release(n, i)
    return prog, cnt


def counted_witness2(R, rng, nregs=NREGS, rowmap=None, block_order=None, set_order=None):
    cp, key = build(R, "counted")
    live = live_gates(cp, key)
    nin = cp.nin
    gg = [gi for gi in live if cp.gk[gi] == "g"]
    vv = [gi for gi in live if cp.gk[gi] == "v"]
    require(all(s[0] != "c" for s in key), "constant key plane")
    if rowmap is None:
        rowmap = [KEY_ROW0 + i for i in range(144)]
    require(sorted(rowmap) == list(range(KEY_ROW0, 255)), "row map must be a permutation of rows 111..254")
    block_order = block_order or [3, 4, 5, 6, 7]
    set_order = set_order or list(range(32))
    ops, MASKID, ONES = build_program(cp, key, vv, rowmap, block_order, set_order)
    mem_ids = set(range(nin)) | set(nin + gi for gi in gg) | set(MASKID.values()) | {ONES}
    prog, cnt = allocate2(ops, mem_ids, nregs)
    # ---- execute
    prefix = [rng.getrandbits(32) for _ in range(13)]
    bidx = rng.getrandbits(16); gidx = rng.getrandbits(104); rtag = rng.getrandbits(128)
    mem = {}
    for w in range(13):
        for i in range(32):
            mem[cp.names["P%d" % (32 * w + i)]] = M if (prefix[w] >> i) & 1 else 0
    for i in range(8):
        mem[cp.names["LN%d" % i]] = LANE_PLANES[i]
    setup = 0
    for i in range(16):
        mem[cp.names["B%d" % i]] = (0 - ((bidx >> i) & 1)) & M; setup += 4
    BIDL = (rtag << 128) | ((gidx << 24) | (bidx << 8)); setup += 3
    setup += 3
    for s, vid in MASKID.items():
        mem[vid] = delta_mask(s)
    mem[ONES] = M
    for gi in gg:
        x, y = mem[cp.ga[gi]], mem[cp.gb[gi]]
        op = cp.op[gi]
        mem[nin + gi] = x ^ y if op == 0 else (x & y if op == 1 else (x | y if op == 2 else x & (y ^ M)))
    regs = [None] * nregs

    def rd_(r, v):
        require(regs[r] is not None and regs[r][0] == v, "stale register %d" % r)
        return regs[r][1]

    table = {}
    cand = 0
    sunk = {}
    stored_x = {}
    for ins in prog:
        k = ins[0]
        if k == 4:
            regs[ins[1]] = (ins[2], mem[ins[2]])
        elif k == 5:
            mem[ins[2]] = rd_(ins[1], ins[2])
        elif k == 6:
            regs[ins[1]] = (ins[3], rd_(ins[2], ins[4]) ^ M)
        elif k in (7, 8):
            x = rd_(ins[2], ins[4])
            regs[ins[1]] = (ins[3], (x >> ins[5]) if k == 7 else ((x << ins[5]) & M))
        elif k == 9:
            Kw = rd_(ins[1], ins[2])
            sunk[ins[3]] = Kw
            idx = Kw >> KEY_ROW0
            e = table.get(idx)
            if e is None:
                e = int.from_bytes(hashlib.sha256(b"garbage%d" % idx).digest() * 8, "big") & M
            x = Kw ^ BIDL
            if ((x ^ e) >> 128) == 0:
                cand += 1
            table[idx] = x
            stored_x[ins[3]] = x
            BIDL += 1
        else:
            x = rd_(ins[2], ins[5]); y = rd_(ins[3], ins[6])
            regs[ins[1]] = (ins[4], x ^ y if k == 0 else (x & y if k == 1 else x | y))
    # ---- check: key planes against the scalar reference; sunk rows against the transpose of the plane matrix
    require(sorted(sunk) == list(range(256)), "every row sunk once")
    planes_true = []
    stored = []
    # stored plane words: recompute by evaluating the circuit (values are in mem or were in registers);
    # evaluate the per-batch gates directly from mem/group values for the check (independent of registers)
    val = dict(mem)
    for gi in vv:
        x, y = val[cp.ga[gi]], val[cp.gb[gi]]
        op = cp.op[gi]
        val[nin + gi] = x ^ y if op == 0 else (x & y if op == 1 else (x | y if op == 2 else x & (y ^ M)))
    for i, sg in enumerate(key):
        w = val[sg[1]]
        stored.append(w)
        planes_true.append(w ^ (M if sg[2] else 0))
    bad = 0
    for L in range(256):
        rk = ref_key(message(prefix, 256 * bidx + L), R)
        if key_words(planes_true, L) != list(rk):
            bad += 1
        exp = 1 << 255
        for i in range(144):
            if (stored[i] >> L) & 1:
                exp |= 1 << rowmap[i]
        if sunk[L] != exp:
            bad += 1
    # every stored entry decodes to its own message: id = x XOR Kw (low 128 bits), lane field = rotl8(L, 3)
    for L in range(256):
        idv = (stored_x[L] ^ sunk[L]) & ((1 << 128) - 1)
        lane = idv & 0xFF
        lane = ((lane >> 3) | (lane << 5)) & 0xFF
        if lane != L or (idv >> 8) & 0xFFFF != bidx or (idv >> 24) != gidx or (stored_x[L] ^ sunk[L]) >> 128 != rtag:
            bad += 1
    require(bad == 0, "counted program disagrees on %d lanes" % bad)
    circuit = cnt["xor"] + cnt["and"] + cnt["or"] + 2 * cnt["andnot"] + cnt["shift"]
    total = circuit + cnt["load"] + cnt["store"] + 9 * cnt["sink"] + setup
    return {"xor": cnt["xor"], "and": cnt["and"], "or": cnt["or"], "andnot": cnt["andnot"], "shift": cnt["shift"],
            "loads": cnt["load"], "stores": cnt["store"], "circuit_loads": cnt["c_load"], "circuit_stores": cnt["c_store"],
            "table": 9 * cnt["sink"], "setup": setup, "total": total, "garbage": cand}


if __name__ == "__main__":
    main()
