"""Sub-class search with a beta pre-filter for 2-round BLAKE3 (blake3-r2-prefix-v1).

Implements proof.md. The half-collision construction, the class of Y4, the D0
family, Lemma E and the shape of the packed batch are from submission
04638ed8 by Jbenisek (co-author tekkac); the seven-lane layout and the masked
rotation are from ticket 2bf40fb. New here: the sub-class S of 256 members
(proof 3.3), the beta pre-filter (Lemma B), lanes that hold seven values of
alpha, and the counted program below.

The organizer request is read from stdin and one 60-byte/62-byte message pair
(or a null pair) is returned per trial. Only the standard library is used; no
OS randomness, wall time or ambient state. SHAKE-256 only expands the
organizer's seed. The program evaluates G itself and never calls an
implementation of BLAKE3; the organizer recomputes both complete digests.

Experiments (proof.md Section 9):
  half-collision     one trial per seed; digest words 0,2,5,7 agree (exact).
                     Observations: the counted group (set-up, one batch,
                     continuation) of the same context, member and seven
                     alphas, and its lanes equal to a forward computation.
  class-walk         64 consecutive members of S for one context and alpha;
                     returns the seed member's pair; observations from the
                     forward computation: Y4 = member, eta, filter passes.
  early-test-bits    trials in algorithm order (at most 256) until dO1 has
                     its low 4 bits and dO4 its bits 25..28 zero, so that the
                     low 4 bits of the Lemma E word dO1 ^ ROL(dO4,7) vanish.
  filtered-residual  trials in algorithm order through the batch up to the
                     beta filter; among the first 8 filter passes, the first
                     whose dO3 bits 28,27,23,22 and dO6 bits 20,19,15,14 are
                     zero (an event model M predicts at 8.7 x uniform).

Self-test (not an organizer mode):  python3 classsearch.py --selftest N [seed]
"""
import hashlib, json, struct, sys
from itertools import islice

M = 0xFFFFFFFF
IV = (0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A, 0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19)
K = (IV[2] + IV[6]) & M
X3, X7, X11, X15 = 0xA6C3B8C5, 0x793C473A, 0x5C32535C, 0x8367C7BB
W4, W13 = 0x60000001, 0x29BD3F58
W4B = (((K + W4) & M) ^ 2) - K & M
DEL5 = (W4 - W4B) & M
Y3A, Y3B, Y11A, Y11B = 0xC952EC69, 0x36AC1396, 0x31FC40B2, 0xA28739E3
ETA, CMASK, CVAL = 0xE96D6D6B, 0x6D6BE96D, 0x00096120
FK, FP = 0x008D0953, 0x00010811                 # beta filter: (c1 AND FK) == FP
B2 = (0x953908D0, 0x953F08D0)
FREEPOS = [i for i in range(32) if not CMASK >> i & 1]
POS5, PATTERNS = (1, 4, 7, 12, 20), ("01000", "10100")
GROUPS = 613566756                               # alpha = 7g + i, 0 <= g < GROUPS, 0 <= i < 7
LANES, LB = 7, 36
WORD = (1 << 256) - 1
ONES = sum(1 << (LB * i) for i in range(LANES))
REGISTERS = 64
SCAN_SEEDS = 20                                  # self-test: filter_passes against a scalar c1 scan


def ror(v, n):
    return ((v >> n) | (v << (32 - n))) & M


def rol(v, n):
    return ((v << n) | (v >> (32 - n))) & M


def G(a, b, c, d, x, y):
    a = (a + b + x) & M; d = ror(d ^ a, 16); c = (c + d) & M; b = ror(b ^ c, 12)
    a = (a + b + y) & M; d = ror(d ^ a, 8); c = (c + d) & M; b = ror(b ^ c, 7)
    return a, b, c, d


def col(j, sb, sc, d0):
    b1 = rol(sb, 7) ^ sc; c1 = rol(b1, 12) ^ IV[4 + j]; sd = (sc - c1) & M
    d1 = (c1 - IV[j]) & M; a1 = rol(d1, 16) ^ d0
    return rol(sd, 8) ^ d1, sd, (a1 - IV[j] - IV[4 + j]) & M, (rol(sd, 8) ^ d1) - a1 - b1 & M


def step_s1(X1, X2, X5, X6, X9, X10, X12, X13, X14):
    """Step S1 (proof.md 3): the context for nine free words."""
    w, S, X = [0] * 16, [0] * 16, [0] * 16
    X[1], X[2], X[5], X[6], X[9], X[10], X[12], X[13], X[14] = X1, X2, X5, X6, X9, X10, X12, X13, X14
    X[3], X[7], X[11], X[15] = X3, X7, X11, X15
    w[4], w[13] = W4, W13
    p = (K + W4) & M; q = ror(p ^ 60, 16); r = (q + IV[2]) & M; u = ror(r ^ IV[6], 12)
    bD1 = rol(X6, 7) ^ X11; c = (X11 - X12) & M; dD1 = rol(X12, 8) ^ X1
    S[6] = rol(bD1, 12) ^ c; S[11] = (c - dD1) & M; S[10] = u ^ rol(S[6], 7)
    b = rol(X5, 7) ^ X10; c = (X10 - X15) & M; S[5] = rol(b, 12) ^ c
    S[14] = (S[10] - r) & M; S[2] = rol(S[14], 8) ^ q; w[5] = (S[2] - p - u) & M
    d = rol(X14, 8) ^ X3; aD3 = rol(d, 16) ^ S[14]; b = (X3 - aD3) & M
    X[4] = ror(b ^ X9, 7); c = (X9 - X14) & M; S[4] = rol(b, 12) ^ c; S[9] = (c - d) & M
    S[1], S[13], w[2], w[3] = col(1, S[5], S[9], 0)
    d = rol(X13, 8) ^ X2; a = rol(d, 16) ^ S[13]; b = (X2 - a - W13) & M
    X[8] = b ^ rol(X7, 7); c = (X[8] - X13) & M; S[7] = rol(b, 12) ^ c; S[8] = (c - d) & M
    w[12] = (a - S[2] - S[7]) & M
    S[0], S[12], w[0], w[1] = col(0, S[4], S[8], 0)
    S[3], S[15], w[6], w[7] = col(3, S[7], S[11], 11)
    return dict(w=w, S=S, X=X, bD1=bD1, aD3=aD3)


def e1_of(k):
    e1 = CVAL
    for i, p in enumerate(FREEPOS):
        if k >> i & 1:
            e1 |= 1 << p
    return e1


SUB = [(e1_of(k) - Y3A) & M for k in range(4096)
       if "".join(str(e1_of(k) >> p & 1) for p in POS5) in PATTERNS]


def trial(ctx, alpha, y):
    """The trial of proof.md 4.2: message words for context, alpha, member y."""
    w = list(ctx["w"]); S = list(ctx["S"]); X = list(ctx["X"])
    c = (alpha - X15) & M; dD0 = (c - S[10]) & M; X[0] = rol(X15, 8) ^ dD0
    bD0 = ror(S[5] ^ c, 12); X[5] = ror(bD0 ^ alpha, 7); X[10] = alpha
    pa = (X[0] + X[4] + w[2]) & M; pd = ror(X[12] ^ pa, 16); pc = (X[8] + pd) & M; pb = ror(X[4] ^ pc, 12)
    Y12 = (rol(y, 7) ^ pb) - pc & M; w[6] = (rol(Y12, 8) ^ pd) - pa - pb & M
    ka = (IV[3] + IV[7] + w[6]) & M; kd = ror(ka ^ 11, 16); kc = (IV[3] + kd) & M; kb = ror(IV[7] ^ kc, 12)
    S[11] = rol(S[7], 7) ^ kb; S[15] = (S[11] - kc) & M; S[3] = rol(S[15], 8) ^ kd; w[7] = (S[3] - ka - kb) & M
    d = (X11 - X[12] - S[11]) & M; X[1] = rol(X[12], 8) ^ d
    a = rol(d, 16) ^ S[12]; w[10] = (a - S[1] - S[6]) & M; w[11] = (X[1] - a - ctx["bD1"]) & M
    a = rol(dD0, 16) ^ S[15]; w[8] = (a - S[0] - S[5]) & M; w[9] = (X[0] - a - bD0) & M
    w[14] = (ctx["aD3"] - S[3] - S[4]) & M
    return w


def messages(w):
    wb = list(w); wb[4] = W4B; wb[5] = (w[5] + DEL5) & M
    return struct.pack("<16I", *w)[:60], struct.pack("<16I", *wb)[:62], wb


PERM = (2, 6, 3, 10, 7, 0, 4, 13, 1, 11, 12, 5, 9, 14, 15, 8)
CALLS = ((0, 4, 8, 12), (1, 5, 9, 13), (2, 6, 10, 14), (3, 7, 11, 15),
         (0, 5, 10, 15), (1, 6, 11, 12), (2, 7, 8, 13), (3, 4, 9, 14))


def compress(w, n):
    """Two rounds forward; returns the state Y after the round-1 column step and the digest words o[0..7]."""
    v = list(IV) + list(IV[:4]) + [0, 0, n, 11]; s = list(w); Y = None
    for rnd in range(2):
        for j, (a, b, c, d) in enumerate(CALLS):
            v[a], v[b], v[c], v[d] = G(v[a], v[b], v[c], v[d], s[2 * j], s[2 * j + 1])
            if rnd == 1 and j == 3:
                Y = list(v)
        s = [s[PERM[i]] for i in range(16)]
    return Y, [v[i] ^ v[i + 8] for i in range(8)]


def forward(ctx, alpha, y):
    """Forward reference for one trial, from its message words only (no shortcut of the batch)."""
    w = trial(ctx, alpha, y); A, B, wb = messages(w)
    Ya, oa = compress(w, 60); Yb, ob = compress(wb, 62)
    def e1(Y, w5):
        a1 = (Y[1] + Y[6] + w[12]) & M; d1 = ror(Y[12] ^ a1, 16); c1 = (Y[11] + d1) & M
        return c1, (a1 + ror(Y[6] ^ c1, 12) + w5) & M
    def e3(Y):
        e = (Y[3] + Y[4]) & M; h1 = ror(Y[14] ^ e, 16); return h1, ror(Y[4] ^ ((Y[9] + h1) & M), 12)
    c1, a2 = e1(Ya, w[5]); c1b, a2b = e1(Yb, wb[5]); h1, f1 = e3(Ya); h1b, f1b = e3(Yb)
    t = a2 ^ a2b; d = [oa[i] ^ ob[i] for i in range(8)]
    return dict(A=A, B=B, y4=Ya[4], y4b=Yb[4], c1=c1, beta=ror(c1 ^ c1b, 12), eta=h1 ^ h1b,
                ew=f1 ^ f1b ^ t ^ ror(t, 1), d=d, half=d[0] | d[2] | d[5] | d[7])


# ---------------------------------------------------------------- counted packed machine
def rep(v):
    return (v & M) * ONES


def lanes(z):
    return [z >> (LB * i) & ((1 << LB) - 1) for i in range(LANES)]


class V:
    __slots__ = ("z", "b", "e")

    def __init__(s, z, b):
        s.z, s.b, s.e = z, b, b


class Mach:
    """Every ALU primitive is one operation, PROR is five, every load is one; resident constants are registers."""

    def __init__(s, res):
        s.res, s.ops, s.lds, s.top, s.part, s.t, s.vals, s.used = res, {}, {}, {}, None, 0, [], {}

    def at(s, p):
        s.part = p
        for d in (s.ops, s.lds, s.top):
            d.setdefault(p, 0)

    def new(s, z, *u):
        s.t += 1
        for o in u:
            o.e = s.t
        v = V(z, s.t); s.vals.append(v); return v

    def k(s, n):
        s.used.setdefault(s.part, set()).add(n); return V(s.res[n], None)

    def ld(s, z):
        s.lds[s.part] += 1; return s.new(z)

    def op(s, z, *u):
        s.ops[s.part] += 1; return s.new(z, *u)

    def add(s, x, y):
        s.top[s.part] = max([s.top[s.part]] + [a + b for a, b in zip(lanes(x.z), lanes(y.z))])
        return s.op((x.z + y.z) & WORD, x, y)

    def xor(s, x, y): return s.op(x.z ^ y.z, x, y)
    def band(s, x, y): return s.op(x.z & y.z, x, y)
    def bor(s, x, y): return s.op(x.z | y.z, x, y)
    def shr(s, x, r): return s.op(x.z >> r, x)
    def shl(s, x, r): return s.op((x.z << r) & WORD, x)

    def ror(s, z, r):
        return s.bor(s.band(s.shr(z, r), s.k("A%d" % r)), s.band(s.shl(z, 32 - r), s.k("B%d" % r)))

    def rol(s, z, r): return s.ror(z, 32 - r)

    def cmpbr(s, x, y):
        s.ops[s.part] += 2; s.t += 1
        for o in (x, y):
            o.e = s.t
        return x.z != y.z

    def live(s):
        ch = [0] * (s.t + 2)
        for v in s.vals:
            ch[v.b] += 1; ch[v.e] -= 1
        h = pk = 0
        for c in ch:
            h += c; pk = max(pk, h)
        return pk


class Fast(Mach):
    """The same programs without counting (used only to find filter passes quickly)."""

    def new(s, z, *u): return V(z, 0)
    def k(s, n): return V(s.res[n], 0)
    def ld(s, z): return V(z, 0)
    def at(s, p): pass
    def op(s, z, *u): return V(z, 0)
    def add(s, x, y): return V((x.z + y.z) & WORD, 0)
    def cmpbr(s, x, y): s.t = 0; return x.z != y.z


def residents(ctx):
    """Constants held in registers during the batches of a context (formed per context, outside the batch)."""
    w, S, X = ctx["w"], ctx["S"], ctx["X"]
    r = {}
    for n in (1, 7, 8, 12, 16, 24):
        r["A%d" % n] = rep((1 << (32 - n)) - 1); r["B%d" % n] = rep(((1 << n) - 1) << (32 - n))
    for n, v in (("M", M), ("1", 1), ("11", 11), ("IV3", IV[3]), ("IV7", IV[7]), ("Y11", Y11A), ("Y11'", Y11B),
                 ("eta", ETA), ("FK", FK), ("FP", FP), ("ROL(S7,7)", rol(S[7], 7)), ("X2+X6+1", X[2] + X[6] + 1),
                 ("X11-X12+1", X11 - X[12] + 1), ("ROL(X12,8)", rol(X[12], 8)), ("S12", S[12]), ("X13", X[13]),
                 ("X9", X[9]), ("-S1-S6", -S[1] - S[6]), ("X14", X[14]), ("X6", X[6]), ("w0", w[0]),
                 ("w12", w[12]), ("w5", w[5]), ("w5+d", w[5] + DEL5)):
        r[n] = rep(v)
    r["bit32"] = ONES << 32
    return r


SETUP_MEM = lambda ctx: dict((n, rep(v)) for n, v in (
    ("7", 7), ("-X15", -X15), ("-S10", -ctx["S"][10]), ("ROL(X15,8)", rol(X15, 8)),
    ("X4+w2", ctx["X"][4] + ctx["w"][2]), ("X12", ctx["X"][12]), ("X8", ctx["X"][8]), ("1-X8", 1 - ctx["X"][8]),
    ("X4", ctx["X"][4]), ("IV3+IV7+2", IV[3] + IV[7] + 2), ("S5", ctx["S"][5]), ("w3", ctx["w"][3])))


def group_setup(m, ctx, avec):
    """Per group of seven alphas: the seven per-alpha lane constants from the alpha vector (counted).
    Constants used only here are loaded from memory. Returns new resident values and the next alpha vector."""
    mem = SETUP_MEM(ctx)
    L = lambda n: m.ld(mem[n])
    m.at("setup")
    a = m.new(avec)                                          # alpha vector register (resident across groups)
    c = m.add(a, L("-X15"))                                  # c = alpha - X15
    x0 = m.xor(m.add(c, L("-S10")), L("ROL(X15,8)"))         # X0 = ROL(X15,8) XOR (c - S10)
    pa = m.band(m.add(x0, L("X4+w2")), m.k("M"))             # pa = X0 + X4 + w2, reduced
    pd = m.ror(m.xor(pa, L("X12")), 16)
    pb = m.ror(m.xor(m.add(pd, L("X8")), L("X4")), 12)       # pb = ROR(X4 XOR (X8 + pd), 12)
    npc = m.band(m.add(m.xor(pd, m.k("M")), L("1-X8")), m.k("M"))           # -pc = (pd XOR M) + 1 - X8
    ivp = m.band(m.add(m.add(m.xor(pa, m.k("M")), m.xor(pb, m.k("M"))), L("IV3+IV7+2")), m.k("M"))
    x5 = m.ror(m.xor(m.ror(m.xor(c, L("S5")), 12), a), 7)   # X5 = ROR(ROR(S5 XOR c, 12) XOR alpha, 7)
    x5w3 = m.band(m.add(x5, L("w3")), m.k("M"))
    out = {"pb": pb.z, "-pc": npc.z, "pd": pd.z, "IV3+IV7-pa-pb": ivp.z, "X5": x5.z, "X5+w3": x5w3.z, "alpha": avec}
    m.at("group loop")
    nxt = m.add(a, L("7"))                                   # next alpha vector
    m.cmpbr(m.new(0), m.new(1))                             # group counter end test and branch
    m.op(0)                                                  # group counter increment
    m.cmpbr(m.new(0), m.new(1))                             # continuation cap: countdown register below zero? branch
    for v in (pb, npc, pd, ivp, x5, x5w3):
        v.e = m.t
    return out, nxt.z


def member_words(j):
    y = SUB[j]
    return rep(rol(y, 7)), rep((Y3A + y) & M)


def batch(m, j):
    """Batch for member j in all seven lanes (unrolled: U[j] at a constant address). 105 ALU + 1 load."""
    U, _ = member_words(j); k = m.k
    m.at("C0 backwards")
    y12 = m.add(m.xor(m.ld(U), k("pb")), k("-pc"))
    ka = m.add(m.xor(m.rol(y12, 8), k("pd")), k("IV3+IV7-pa-pb"))
    m.at("K3")
    kd = m.ror(m.xor(ka, k("11")), 16); kc = m.add(kd, k("IV3")); kb = m.ror(m.xor(kc, k("IV7")), 12)
    s11 = m.xor(kb, k("ROL(S7,7)"))
    s3 = m.xor(m.rol(m.add(m.add(s11, m.xor(kc, k("M"))), k("1")), 8), kd)
    first = m.add(m.add(s3, m.xor(m.add(ka, kb), k("M"))), k("X2+X6+1"))
    m.at("D1")
    d = m.add(m.xor(s11, k("M")), k("X11-X12+1")); x1 = m.xor(d, k("ROL(X12,8)")); a = m.xor(m.rol(d, 16), k("S12"))
    m.at("C1 to Y1")
    qa = m.add(x1, k("X5+w3")); qd = m.ror(m.xor(qa, k("X13")), 16); qc = m.add(qd, k("X9"))
    qb = m.ror(m.xor(qc, k("X5")), 12); y1 = m.add(m.add(m.add(qa, qb), a), k("-S1-S6"))
    m.at("C2")
    rd = m.ror(m.xor(first, k("X14")), 16); rc = m.add(rd, k("alpha")); rb = m.ror(m.xor(rc, k("X6")), 12)
    ra = m.add(m.add(first, rb), k("w0")); y14 = m.ror(m.xor(ra, rd), 8); y6 = m.ror(m.xor(m.add(rc, y14), rb), 7)
    m.at("E1 to c1")
    a1 = m.add(m.add(y1, y6), k("w12")); d1 = m.ror(m.xor(a1, y12), 16); c1 = m.add(d1, k("Y11"))
    m.at("filter")
    z = m.band(m.xor(c1, k("FP")), k("FK"))
    fl = m.band(m.add(z, k("M")), k("bit32"))
    taken = m.cmpbr(fl, k("bit32"))
    flags = [1 - (fl.z >> (LB * i + 32) & 1) for i in range(LANES)]
    # taken = some lane passes: the branch "fl = bit32" is then not taken and execution falls into the continuation
    return c1, flags, taken, dict(qc=qc, qd=qd, y1=y1, y6=y6, y14=y14, a1=a1, d1=d1, c1=c1)


def continuation(m, st, j):
    """Only when some lane passes the filter: Y9, E1 for A and B, E3 first halves, Lemma E word. 53 ALU + 1 load."""
    _, Vj = member_words(j); k = m.k
    m.at("cont")
    m.op(0)                                                  # continuation countdown (register), tested per group
    y9 = m.add(st["qc"], m.ror(m.xor(st["y1"], st["qd"]), 8))
    c1b = m.add(st["d1"], k("Y11'"))
    b1 = m.ror(m.xor(st["c1"], st["y6"]), 12); b1b = m.ror(m.xor(c1b, st["y6"]), 12)
    a2 = m.add(m.add(st["a1"], b1), k("w5")); a2b = m.add(m.add(st["a1"], b1b), k("w5+d"))
    h1 = m.ror(m.xor(st["y14"], m.ld(Vj)), 16); h1b = m.xor(h1, k("eta"))
    fx = m.ror(m.xor(m.add(y9, h1), m.add(y9, h1b)), 12)
    t = m.xor(a2, a2b)
    word = m.band(m.xor(m.xor(fx, t), m.ror(t, 1)), k("M"))
    fl = m.band(m.add(word, k("M")), k("bit32"))
    taken = m.cmpbr(fl, k("bit32"))
    return [x & M for x in lanes(word.z)], taken


LEDGER = {"setup": (40, 11), "group loop": (6, 1), "C0 backwards": (9, 1), "K3": (27, 0), "D1": (9, 0),
          "C1 to Y1": (17, 0), "C2": (28, 0), "E1 to c1": (9, 0), "filter": (6, 0), "cont": (53, 1)}


def avec_of(g):
    return sum((7 * g + i) << (LB * i) for i in range(LANES))


def run_group(ctx, g, j, cont=True):
    """Counted: set-up of group g, batch of member j, and (always, for checking) the continuation."""
    m = Mach(residents(ctx))
    out, nxt = group_setup(m, ctx, avec_of(g))
    setup_live = m.live()
    m.res.update(out)
    c1, flags, taken, st = batch(m, j)
    words, etaken = continuation(m, st, j) if cont else (None, None)
    return m, c1, flags, taken, words, etaken, nxt, setup_live


def check_group(ctx, g, j):
    """Lane-by-lane comparison with forward(): c1, filter flag, Lemma E word; returns counts and flags."""
    m, c1, flags, taken, words, etaken, nxt, sl = run_group(ctx, g, j)
    eq = 0; zero_ew = 0
    for i in range(LANES):
        f = forward(ctx, 7 * g + i, SUB[j])
        ok = (lanes(c1.z)[i] & M) == f["c1"] and flags[i] == int(f["c1"] & FK == FP)
        ok = ok and words[i] == f["ew"] and f["ew"] == f["d"][1] ^ rol(f["d"][4], 7)
        ok = ok and f["half"] == 0 and f["y4"] == f["y4b"] == SUB[j] and f["eta"] == ETA
        ok = ok and (f["beta"] not in B2 or flags[i] == 1)
        eq += ok; zero_ew += f["ew"] == 0
    ok_taken = taken == (1 in flags) and etaken == (0 in words) and nxt == avec_of(g + 1)
    return m, eq, ok_taken, sl


# ---------------------------------------------------------------- experiments
def params(seed, n):
    return struct.unpack("<%dI" % n, hashlib.shake_256(seed).digest(4 * n))


def seed_context(s):
    """Coins X2, X5, X6, X9; X1 = X10 = 0; context (X12 < 2^10, X13, X14); group, lane, member."""
    ctx = step_s1(0, s[0], s[1], s[2], s[3], 0, s[4] & 1023, s[5], s[6])
    return ctx, s[7] % GROUPS, s[8] % LANES, s[9] % len(SUB)


def counted_obs(ctx, g, j):
    m, eq, okt, _ = check_group(ctx, g, j)
    return {"setup_ops": m.ops["setup"] + m.ops["group loop"], "setup_loads": m.lds["setup"] + m.lds["group loop"],
            "batch_ops": sum(m.ops[p] for p in m.ops if p not in ("setup", "group loop", "cont")),
            "batch_loads": sum(m.lds[p] for p in m.lds if p not in ("setup", "group loop", "cont")),
            "cont_ops": m.ops["cont"], "cont_loads": m.lds["cont"], "lanes_equal": eq if okt else 0}


def ex_half(seed):
    s = params(seed, 10); ctx, g, i, j = seed_context(s)
    f = forward(ctx, 7 * g + i, SUB[j])
    return f["A"], f["B"], counted_obs(ctx, g, j)


def ex_walk(seed):
    s = params(seed, 10); ctx, g, i, j = seed_context(s)
    alpha, j0 = 7 * g + i, j & ~63
    y4 = eta = filt = 0
    for jj in range(j0, j0 + 64):
        f = forward(ctx, alpha, SUB[jj])
        y4 += f["y4"] == SUB[jj] == f["y4b"]; eta += f["eta"] == ETA; filt += f["c1"] & FK == FP
        if jj == j:
            pair = (f["A"], f["B"])
    return pair[0], pair[1], {"members_walked": 64, "y4_equal": y4, "eta_equal": eta, "filter_passes": filt}


def walk_order(s):
    """Trials from the seed's start in algorithm order: member j outer, lane i inner, then the next group."""
    ctx, g, i, j = seed_context(s)
    while True:
        for jj in range(j, len(SUB)):
            for ii in range(LANES):
                yield ctx, 7 * g + ii, SUB[jj]
        j, g = 0, (g + 1) % GROUPS


EW_MASK1, EW_MASK4 = 0xF, ror(0xF, 7)


def ex_early(seed):
    s = params(seed, 10)
    for n, (ctx, alpha, y) in enumerate(walk_order(s)):
        if n == 256:
            return None, None, {"tries": n}
        f = forward(ctx, alpha, y)
        if f["d"][1] & EW_MASK1 == 0 and f["d"][4] & EW_MASK4 == 0:
            return f["A"], f["B"], {"tries": n + 1, "ew_low4_zero": int(f["ew"] & 0xF == 0)}


def c1_only(ctx, alpha, y):
    w = trial(ctx, alpha, y)
    Y, _ = compress(w, 60)
    a1 = (Y[1] + Y[6] + w[12]) & M
    return (Y[11] + ror(Y[12] ^ a1, 16)) & M


def filter_passes(s):
    """Trials passing the beta filter, in algorithm order from the seed's group and member: the set-up and the
    batch of proof.md 5.2-5.3 up to the filter on plain integers (uncounted). The self-test compares its first
    passes with a scalar scan of c1 from forward-computed states (filter_scan_ok)."""
    ctx, g, _, j = seed_context(s); r = residents(ctx)
    A = {n: r["A%d" % n] for n in (1, 7, 8, 12, 16, 24)}; B = {n: r["B%d" % n] for n in (1, 7, 8, 12, 16, 24)}
    def R(z, n): return (z >> n) & A[n] | (z << (32 - n)) & B[n]
    Mk, one, i11, iv3, iv7, s7, x26, xx, x12, s12, x13, x9, s16, x14, x6, w0, w12, y11, fk, fp, b32 = (r[n] for n in (
        "M", "1", "11", "IV3", "IV7", "ROL(S7,7)", "X2+X6+1", "X11-X12+1", "ROL(X12,8)", "S12", "X13", "X9", "-S1-S6",
        "X14", "X6", "w0", "w12", "Y11", "FK", "FP", "bit32"))
    U = [member_words(jj)[0] for jj in range(len(SUB))]
    while True:
        m = Fast(dict(r)); o, _ = group_setup(m, ctx, avec_of(g))
        pb, npc, pd, ivp, x5, x5w3, al = (o[n] for n in ("pb", "-pc", "pd", "IV3+IV7-pa-pb", "X5", "X5+w3", "alpha"))
        for jj in range(j, len(SUB)):
            y12 = (U[jj] ^ pb) + npc; ka = (R(y12, 24) ^ pd) + ivp
            kd = R(ka ^ i11, 16); kc = kd + iv3; kb = R(kc ^ iv7, 12); s11 = kb ^ s7
            s3 = R(s11 + (kc ^ Mk) + one, 24) ^ kd; first = s3 + ((ka + kb) ^ Mk) + x26
            d = (s11 ^ Mk) + xx; x1 = d ^ x12; a = R(d, 16) ^ s12
            qa = x1 + x5w3; qd = R(qa ^ x13, 16); qc = qd + x9; qb = R(qc ^ x5, 12); y1 = qa + qb + a + s16
            rd = R(first ^ x14, 16); rc = rd + al; rb = R(rc ^ x6, 12); ra = first + rb + w0
            y14 = R(ra ^ rd, 8); y6 = R((rc + y14) ^ rb, 7)
            c1 = R((y1 + y6 + w12) ^ y12, 16) + y11
            fl = (((c1 ^ fp) & fk) + Mk) & b32
            if fl != b32:
                for i in range(LANES):
                    if not fl >> (LB * i + 32) & 1:
                        yield ctx, 7 * g + i, SUB[jj]
        j, g = 0, (g + 1) % GROUPS


E8 = ((3, 0x18C00000), (6, 0x0018C000))          # digest words 3 and 6: bits 28,27,23,22 and 20,19,15,14


def ex_filtered(seed):
    s = params(seed, 10)
    for n, (ctx, alpha, y) in enumerate(filter_passes(s)):
        if n == 8:
            return None, None, {"filter_passes": n}
        f = forward(ctx, alpha, y)
        if all(f["d"][w] & b == 0 for w, b in E8):
            return f["A"], f["B"], {"filter_passes": n + 1, "beta_in_B2": int(f["beta"] in B2)}


def selftest(cases, seed):
    eq = good = 0; shape = None; same = True; tops = {}; regs = 0; sl_max = 0
    for case in range(cases):
        s = params(("classsearch selftest %s %d" % (seed, case)).encode(), 10)
        if case % 5 == 4:
            s = [(0, M, v, v)[s[9] >> 2 * i & 3] for i, v in enumerate(s)]
        ctx, g, i, j = seed_context(s)
        if case % 7 == 3:
            g = GROUPS - 1
        m, e, okt, sl = check_group(ctx, g, j)
        eq += e; good += okt
        sh = {p: (m.ops[p], m.lds[p]) for p in m.ops}
        shape = shape or sh; same = same and sh == shape
        for p, t in m.top.items():
            tops[p] = max(tops.get(p, 0), t)
        names = set().union(*m.used.values())
        regs = max(regs, len(names) + m.live() + 3)          # + group counter, group end, continuation countdown
    flags_ok = 0
    for pat in range(1 << LANES):
        fkbits = [b for b in range(32) if FK >> b & 1]
        vals = [(FP | (0x5A5A5A5A & ~FK) | (i & 1) << 32) if pat >> i & 1 else FP ^ (1 << fkbits[(i + pat) % 10])
                | (i & 1) << 32 for i in range(LANES)]
        mm = Mach({"FK": rep(FK), "FP": rep(FP), "M": rep(M), "bit32": ONES << 32}); mm.at("filter")
        c1 = mm.ld(sum(v << (LB * i) for i, v in enumerate(vals)))
        fl = mm.band(mm.add(mm.band(mm.xor(c1, mm.k("FP")), mm.k("FK")), mm.k("M")), mm.k("bit32"))
        tk = mm.cmpbr(fl, mm.k("bit32"))
        flags_ok += [1 - (fl.z >> (LB * i + 32) & 1) for i in range(LANES)] == [pat >> i & 1 for i in range(LANES)] \
            and tk == (pat != 0)
    scan_ok = 0
    for case in range(SCAN_SEEDS):
        s = params(("classsearch filter scan %s %d" % (seed, case)).encode(), 10)
        a = [(ctx["X"][12], alpha, y) for ctx, alpha, y in islice(filter_passes(s), 3)]
        b = [(ctx["X"][12], alpha, y) for ctx, alpha, y in islice(
            ((c, al, y) for c, al, y in walk_order(s) if c1_only(c, al, y) & FK == FP), 3)]
        scan_ok += a == b and len(a) == 3
    member_ok = len(SUB) == 256 and len(set(SUB)) == 256 and all(
        ((Y3A + y) & M) & CMASK == CVAL and ror(((Y3A + y) & M) ^ ((Y3B + y) & M), 16) == ETA for y in SUB)
    rep_ = {"cases": cases, "lanes": LANES * cases, "lanes_equal": eq, "branches_right": good,
            "counts": {p: {"ops": o, "loads": l} for p, (o, l) in shape.items()}, "same_counts": same,
            "counts_equal_ledger": shape == LEDGER, "largest_lane_bits": max(tops.values()).bit_length(),
            "registers": regs, "members": len(SUB), "members_ok": member_ok,
            "flag_patterns_right": flags_ok, "filter_scan_ok": scan_ok, "filter_scan_seeds": SCAN_SEEDS}
    print(json.dumps(rep_, separators=(",", ":")))
    ok = (eq == LANES * cases and good == cases and same and shape == LEDGER and max(tops.values()) < 1 << LB
          and regs <= REGISTERS and member_ok and flags_ok == 128 and scan_ok == SCAN_SEEDS)
    return 0 if ok else 1


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] != "--selftest" or len(sys.argv) not in (3, 4):
            raise SystemExit("usage: classsearch.py --selftest N [seed]   (no arguments: organizer request on stdin)")
        raise SystemExit(selftest(int(sys.argv[2]), sys.argv[3] if len(sys.argv) == 4 else "1"))
    req = json.load(sys.stdin)
    if req["schema_version"] != 1 or req["target_profile"] != "blake3-r2-prefix-v1":
        raise ValueError("unexpected organizer target")
    run = {"half-collision": ex_half, "class-walk": ex_walk, "early-test-bits": ex_early,
           "filtered-residual": ex_filtered}[req["experiment_id"]]
    out = []
    for t in req["trials"]:
        a, b, obs = run(bytes.fromhex(t["seed"]))
        row = {"trial": t["trial"], "message_a_hex": None if a is None else a.hex(),
               "message_b_hex": None if b is None else b.hex()}
        if obs:
            row["observations"] = obs
        out.append(row)
    json.dump({"schema_version": 1, "trials": out}, sys.stdout, separators=(",", ":"), sort_keys=True)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
