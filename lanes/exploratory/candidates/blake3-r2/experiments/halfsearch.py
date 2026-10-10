#!/usr/bin/env python3
"""halfsearch.py - the search of proof.md 9.1 and 9.8 run on the root instance (one chunk, counter 0, flags 11).

Exact computation on 32-bit words, Python 3 standard library only. No BLAKE3 library is imported.

One organizer trial = one run of the search on TRIAL_BATCHES batches drawn from the seed:
  step 1   whole-class sampler (9.1), packed step CO compiled from the lines (9.6), the widened filter of 9.8
           for the nine outcomes of S9 (automaton (2) on omega in all seven lanes, then automaton (1) on Y9),
           the E and pass counts with their budgets;
  9.7      pre-check: nu from Y9, y, C2.c1, C2.b1; T = X_S AND VMASK[nu]; the bits X_3 are never dropped;
  step 2   joint solver of 9.4 with guards (a)-(g), (G7) and (G15) on the rows of T; the guarded generic
           solver of 9.8 (both guesses of a20, (G7), (G15b) and (G20b)) on the rows of X_3;
  step 3   certificate of each root with the cube, beta and eps of its outcome (inverse of Lemma IP, step CT,
           t = 0 for this instance, E1, J words, chaining values); "certified" needs every test;
  ledger   Section 11: 341 per batch, 13 per E lane, 512 per passing lane, and steps 2 and 3 by the block
           allowances of Section 11 on the nodes visited, tested against the caps 17,504 and C_row.
The returned pair is built by step CT on the trial's first passing outer step (the trial's first outer step if
none passes), with the one c1 for which the counter word that step CT forces is t = 0. For every outer step and
that c1 the two messages, hashed as the harness hashes them (counter 0, flags 11), agree on digest words 0, 2, 5
and 7: the only differing state words after the first half of round 2 are Y3 and Y11, and the only differing
message word of the diagonal step is w5; none of them enters diagonals 0 and 2.

  python3 halfsearch.py                    organizer request on stdin, response on stdout
  python3 halfsearch.py --selftest N [seed]
"""
import hashlib
import json
import struct
import sys

M = 0xFFFFFFFF
IV = (0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A, 0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19)
K = (IV[2] + IV[6]) & M
LEN_A, LEN_B = 55, 63
X3, X7, X11, X15 = 0x29D4FA98, 0xBEE3AF28, 0x44036000, 0x40C58500
W4, W13 = 0x97475638, 0x0007C006
W4B = (((W4 + K) & M) ^ LEN_A ^ LEN_B) - K & M
DELTA5 = (W4 - W4B) & M
ETA, EPS, MU, BETA_STAR = 0x830303CF, 0x6E21BE55, 0x9AED22BD, 0x18B0E098
FLAGS, COUNTER = 11, 0                       # the root instance: CHUNK_START | CHUNK_END | ROOT, counter 0
PERM = (2, 6, 3, 10, 7, 0, 4, 13, 1, 11, 12, 5, 9, 14, 15, 8)
GCALLS = ((0, 4, 8, 12), (1, 5, 9, 13), (2, 6, 10, 14), (3, 7, 11, 15),
          (0, 5, 10, 15), (1, 6, 11, 12), (2, 7, 8, 13), (3, 4, 9, 14))
TRIAL_BATCHES = 256                          # 1,792 outer steps per organizer trial


def ror(v, n):
    n &= 31
    return ((v >> n) | (v << (32 - n))) & M if n else v


def rol(v, n):
    return ror(v, 32 - (n & 31))


def bit(x, i):
    return (x >> i) & 1


def maj(a, b, c):
    return (a & b) | (a & c) | (b & c)


def g(a, b, c, d, x, y):
    a = (a + b + x) & M; d = ror(d ^ a, 16); c = (c + d) & M; b = ror(b ^ c, 12)
    a = (a + b + y) & M; d = ror(d ^ a, 8); c = (c + d) & M; b = ror(b ^ c, 7)
    return a, b, c, d


Y3, Y7, Y11, Y15 = g(X3, X7, X11, X15, W4, W13)
Y3B, Y7B, Y11B, Y15B = g(X3, X7, X11, X15, W4B, W13)
DY3 = (Y3B - Y3) & M
K2A = (K + W4) & M
K2D = ror(K2A ^ LEN_A, 16)
K2C = (IV[2] + K2D) & M
K2B = ror(IV[6] ^ K2C, 12)
assert (Y7, Y15) == (Y7B, Y15B) and Y3 == 0x8127C181 and DY3 == 0xFDB77CFD and ror(ETA ^ EPS, 8) == MU

# ---- the class (Lemma Q): 13 fixed bits of e1 = Y3 + y, 19 free bits ----------------------------------------------
CLASS_MASK, CLASS_VALUE, FREE_MASK = 0x03CF8303, 0x030C0303, 0xFC307CFC
CLASS_FREE = tuple(i for i in range(32) if FREE_MASK >> i & 1)
Y_PEND = (CLASS_VALUE - Y3) & M

# ---- outcomes: S of beta* (bits 0..6, mask 5f), X3 of beta3 (bits 7..9); the cubes; constants and budgets of 9.1 --
TAUS = (0x175020A0, 0x185020A0, 0x275020A0, 0x285020A0, 0x385020A0, 0x675020A0, 0x685020A0)
X3_TAUS = (0x185020A0, 0x285020A0, 0x385020A0)
S_MASK, X3_MASK = 0x5F, 0x380
S9_MASK = S_MASK | X3_MASK
LOW_TAUS = {0x175020A0, 0x275020A0, 0x675020A0}
VMASK = [0, 0, 0x3F80, 0x3FFF, 0x3FFF, 0x3F80, 0, 0]
QSTAR_MASK, QSTAR_VALUE = 0x0E09818B, 0x02008000
BETA3, EPS3 = 0x18D0E098, 0x6E61BE55
MU3 = ror(ETA ^ EPS3, 8)
Q3_MASK, Q3_VALUE = 0x0E09818D, 0x02008001
SHARE, E_COUNT, R9 = 23384160813285376, 305100224, 96993280
FACTOR = 5 * 2 ** 10 * R9 // 7
RUN_STEPS = -(-(12419 << 128) // (25000 * FACTOR * ((1 << 22) - 1)))
E_BUDGET = -(-(17 * RUN_STEPS * E_COUNT) >> 36)
PASS_BUDGET = -(-(17 * RUN_STEPS * SHARE) >> 68)
RUN_BATCHES = -(-RUN_STEPS // 7)
TEXT_CONSTANTS = {"FACTOR": 70943656228, "RUN_STEPS": 568084180184553153661, "E_BUDGET": 42876990928602462880,
                  "PASS_BUDGET": 765144922463168754, "RUN_BATCHES": 81154882883507593381}

# ---- Section 11 charges ---------------------------------------------------------------------------------------------
LANES, LANE_BITS = 7, 36
ONES = sum(1 << (LANE_BITS * i) for i in range(LANES))
M_ALL, F_ALL, LIMIT = M * ONES, FREE_MASK * ONES, 1 << LANE_BITS
CHARGE_BATCH_COUNT, CHARGE_DISPATCH = 3, 16                # inside the counted batch of 9.6 (424 with the automaton)
CHARGE_BATCH, CHARGE_LANE_TESTS, CHARGE_E_LANE, CHARGE_PASS = 341, 41, 13, 512
U_GLOBAL, U_FAMILY, U_ROW = 1024, 2304, 1408               # steps 2 and 3 on the rows of T (S): C15(T) <= 17,504
U_FORCED, U_SELECTED_EXTRA, U_FREE, U_G15, U_LEAF = 20, 4, 48, 64, 200
CAP_S = 17504
X_SETUP, X_NODE, X_LEAF, X_GUARD = 8576, 512, 8192, 64     # one row of X3 in the generic solver of 9.8
X_CAPS = {0x185020A0: 78788992, 0x285020A0: 157489536, 0x385020A0: 157489536}
CAP_X3 = 2 * 157489536
CAP_UNION = CAP_S + CAP_X3
OUTER_WORDS = ("C0.d1", "D2.a1", "D2.b1", "S11", "S4", "X9", "w6")


# ---- the lines of step CO ------------------------------------------------------------------------------------------
def Sum(*t):
    return ("sum", t)


def Neg(x):
    return ("neg", x)


def X(a, b):
    return ("xor", a, b)


def R(a, r):
    return ("ror", a, r)


def L(a, r):
    return ("ror", a, 32 - r)


LINES = [
    ("X2", Sum("D2.a1", "D2.b1", W13)), ("X8", X(rol(X7, 7), "D2.b1")), ("C0.c1", Sum("X8", "C0.d1")),
    ("K3.a1", Sum((IV[3] + IV[7]) & M, "w6")), ("K3.d1", R(X("K3.a1", FLAGS), 16)), ("K3.c1", Sum(IV[3], "K3.d1")),
    ("S15", Sum("S11", Neg("K3.c1"))), ("S3", X(L("S15", 8), "K3.d1")), ("K3.b1", R(X(IV[7], "K3.c1"), 12)),
    ("D3.a1", Sum("S3", "S4")), ("S7", R(X("K3.b1", "S11"), 7)), ("D3.b1", Sum(X3, Neg("D3.a1"))),
    ("D2.c1", X(L("D2.b1", 12), "S7")), ("D3.c1", X(L("D3.b1", 12), "S4")), ("X4", R(X("D3.b1", "X9"), 7)),
    ("X13", Sum("X8", Neg("D2.c1"))), ("X14", Sum("X9", Neg("D3.c1"))), ("C0.b1", R(X("X4", "C0.c1"), 12)),
    ("D2.d1", X(L("X13", 8), "X2")), ("D3.d1", X(L("X14", 8), X3)), ("Y8", X(L("Y4", 7), "C0.b1")),
    ("S13", X(L("D2.d1", 16), "D2.a1")), ("S9", Sum("D3.c1", Neg("D3.d1"))), ("Y12", Sum("Y8", Neg("C0.c1"))),
    ("K1.c1", Sum("S9", Neg("S13"))), ("Y0", X(L("Y12", 8), "C0.d1")), ("K1.d1", Sum("K1.c1", Neg(IV[1]))),
    ("C0.a1", Sum("Y0", Neg("C0.b1"), Neg("w6"))), ("K1.a1", L("K1.d1", 16)),
    ("w2", Sum("K1.a1", Neg(IV[1]), Neg(IV[5]))), ("X0", Sum("C0.a1", Neg("X4"), Neg("w2"))),
    ("S14", X(L("D3.d1", 16), "D3.a1")), ("K1.b1", R(X(IV[5], "K1.c1"), 12)), ("S10", Sum(K2C, "S14")),
    ("D0.d1", X(rol(X15, 8), "X0")), ("S5", R(X("K1.b1", "S9"), 7)), ("D0.c1", Sum("S10", "D0.d1")),
    ("D0.b1", R(X("S5", "D0.c1"), 12)), ("X10", Sum("D0.c1", X15)), ("X5", R(X("D0.b1", "X10"), 7)),
    ("S1", X(L("S13", 8), "K1.d1")), ("w3", Sum("S1", Neg("K1.a1"), Neg("K1.b1"))),
    ("X12", X(L("C0.d1", 16), "C0.a1")), ("D1.c1", Sum(X11, Neg("X12"))), ("D1.d1", Sum("D1.c1", Neg("S11"))),
    ("S8", Sum("D2.c1", Neg("D2.d1"))), ("K0.b1", X(L("S4", 7), "S8")), ("S2", X(L("S14", 8), K2D)),
    ("S6", R(X(K2B, "S10"), 7)), ("X1", X(L("X12", 8), "D1.d1")), ("K0.c1", X(L("K0.b1", 12), IV[4])),
    ("D1.b1", R(X("S6", "D1.c1"), 12)), ("C1.a1", Sum("X1", "X5", "w3")), ("S12", Sum("S8", Neg("K0.c1"))),
    ("w7", Sum("S3", Neg("K3.a1"), Neg("K3.b1"))), ("X6", R(X("D1.b1", X11), 7)),
    ("C1.d1", R(X("X13", "C1.a1"), 16)), ("D1.a1", X(L("D1.d1", 16), "S12")), ("C1.c1", Sum("X9", "C1.d1")),
    ("C2.a1", Sum("X2", "X6", "w7")), ("w10", Sum("D1.a1", Neg("S1"), Neg("S6"))),
    ("C1.b1", R(X("X5", "C1.c1"), 12)), ("C2.d1", R(X("X14", "C2.a1"), 16)),
    ("w12", Sum("D2.a1", Neg("S2"), Neg("S7"))), ("Y1", Sum("C1.a1", "C1.b1", "w10")),
    ("C2.c1", Sum("X10", "C2.d1")), ("Y13", R(X("C1.d1", "Y1"), 8)), ("C2.b1", R(X("X6", "C2.c1"), 12)),
    ("K0.d1", Sum("K0.c1", Neg(IV[0]))), ("Y9", Sum("C1.c1", "Y13")), ("S0", X(L("S12", 8), "K0.d1")),
    ("D0.a1", X(L("D0.d1", 16), "S15")), ("w8", Sum("D0.a1", Neg("S0"), Neg("S5"))),
    ("w5", Sum("S2", Neg(K2A), Neg(K2B))), ("w9", Sum("X0", Neg("D0.a1"), Neg("D0.b1"))),
    ("w11", Sum("X1", Neg("D1.a1"), Neg("D1.b1"))), ("Y5", R(X("C1.b1", "Y9"), 7)),
]


def ev(e, v):
    if isinstance(e, int):
        return e
    if isinstance(e, str):
        return v[e]
    if e[0] == "sum":
        s = 0
        for t in e[1]:
            s += -ev(t[1], v) if isinstance(t, tuple) and t[0] == "neg" else ev(t, v)
        return s & M
    if e[0] == "xor":
        return ev(e[1], v) ^ ev(e[2], v)
    return ror(ev(e[1], v), e[2])


def member_y(w):
    'e1 = 030c0303 OR (W AND fc307cfc), y = e1 - Y3; the member number is the 19 free bits in order.'
    e1 = CLASS_VALUE | (w & FREE_MASK)
    return (e1 - Y3) & M, e1, sum((w >> i & 1) << n for n, i in enumerate(CLASS_FREE))


def scalar_outer(eight):
    'Step CO on scalar words: every name, plus y, e1, member and omega = Y3 + y + w8.'
    v = dict(zip(OUTER_WORDS, eight[:7]))
    v["Y4"], v["e1"], v["member"] = member_y(eight[7])
    for name, e in LINES:
        v[name] = ev(e, v)
    v["omega"] = (Y3 + v["Y4"] + v["w8"]) & M
    return v


def deps(e, out):
    if isinstance(e, str):
        out.add(e)
    elif isinstance(e, tuple):
        if e[0] == "sum":
            for t in e[1]:
                deps(t, out)
        elif e[0] in ("neg", "ror"):
            deps(e[1], out)
        elif e[0] == "xor":
            deps(e[1], out)
            deps(e[2], out)


def slice_lines(targets=("Y9", "w8")):
    need, keep = set(targets), []
    for name, e in reversed(LINES):
        if name in need:
            keep.append((name, e))
            d = set()
            deps(e, d)
            need |= d
    return list(reversed(keep))


# ---- the exact outer filter: carry automata (1) on Y9 and (2) on omega ----------------------------------------------
def theta_of(tau):
    return rol(tau ^ ror(tau, 1), 12)


def automaton(targets, dy, n=32):
    layer, trans = [(0, (1,) * len(targets))], []
    for i in range(n):
        ids, rows, e = {}, [], dy >> i & 1
        for k, sets in layer:
            row = []
            for a in (0, 1):
                b, new = a ^ e ^ k, []
                for m, (dz, out) in zip(sets, targets):
                    d, r = dz >> i & 1, 0
                    for c in range(4):
                        if m >> c & 1 and (c >> 1) ^ (c & 1) == (out >> i & 1) ^ a ^ b ^ d:
                            for v in (0, 1):
                                r |= 1 << ((a + v + (c >> 1)) >> 1) * 2 + ((b + (v ^ d) + (c & 1)) >> 1)
                    new.append(r)
                state = ((a + e + k) >> 1, tuple(new)) if any(new) else (0, (0,) * len(new))
                row.append(ids.setdefault(state, len(ids)))
            rows.append(row)
        trans.append(rows)
        layer = list(ids)
    final, tables = [sum(1 << j for j, m in enumerate(sets) if m) for _, sets in layer], []
    for p in range(0, n, 8):
        table = []
        for s in range(len(trans[p])):
            row = [s]
            for j in range(min(8, n - p)):
                row = [trans[p + j][row[x & (1 << j) - 1]][x >> j] for x in range(2 << j)]
            table += [final[row[x % len(row)]] if p + 8 >= n else row[x % len(row)] << 8 for x in range(256)]
        tables.append(table)
    return tables


def filter_targets(width=32):
    'Targets of (1) and (2) for the ten bits: the seven outcomes of beta* (eps), then X3 (the same (1), eps3).'
    mk = (1 << width) - 1
    th = [theta_of(t) for t in TAUS + X3_TAUS]
    eps = [EPS] * 7 + [EPS3] * 3
    return [(ETA & mk, x & mk) for x in th], [(ror(x, 12) & mk, e & mk) for x, e in zip(th, eps)]


def build_tables():
    tq, te = filter_targets()
    t1, t2 = automaton(tq, 0), automaton(te, DY3)
    return [t1[:3] + [[m & S9_MASK for m in t1[3]]], t2[:3] + [[m & S9_MASK for m in t2[3]]]]


def look(tables, x):
    s = 0
    for p, t in enumerate(tables):
        s = t[s + (x >> 8 * p & 255) if p else x & 255]
    return s


def flatten(tables):
    bases, flat = [], []
    for t in tables:
        bases.append(len(flat))
        flat += t
    for p in range(3):
        for i in range(bases[p], bases[p] + len(tables[p])):
            flat[i] += bases[p + 1]
    return flat, bases[0]


def pattern_counts(tables):
    'Exact number of 32-bit words per final pattern.'
    cur = {}
    for b in range(256):
        cur[tables[0][b]] = cur.get(tables[0][b], 0) + 1
    for t in tables[1:]:
        nxt = {}
        for s, c in cur.items():
            for b in range(256):
                nxt[t[s + b]] = nxt.get(t[s + b], 0) + c
        cur = nxt
    return cur


# ---- the packed batch of 9.6 with the operation counter -------------------------------------------------------------
class Val:
    __slots__ = ("var", "bound", "pend")

    def __init__(self, var, bound, pend=0):
        self.var, self.bound, self.pend = var, bound, pend


class Packed:
    'Straight-line code on 256-bit packed words; one unit per emitted operation or load; static lane bounds.'

    def __init__(self):
        self.code, self.n, self.units, self.part = [], 0, {}, None
        self.vals, self.bounds, self.maxbound, self.consts = {}, {}, 0, {}

    def at(self, part):
        self.part = part
        self.units.setdefault(part, 0)

    def emit(self, src, bound, cost):
        v = "t%d" % self.n
        self.n += 1
        self.code.append("%s = %s" % (v, src))
        self.units[self.part] += cost
        self.bounds[v] = bound
        self.maxbound = max(self.maxbound, bound)
        assert bound < LIMIT
        return v

    def const(self, c):
        name = "C%08x" % c
        self.consts[name] = c * ONES
        return name

    def reduce(self, a):
        return Val(self.emit("%s & M_ALL" % a.var, M, 1), M, a.pend)

    def mat(self, a):
        'Form a pending constant addition before a read by XOR, shift, rotation or table index.'
        if not a.pend:
            return a
        if a.bound + a.pend >= LIMIT:
            a = self.reduce(a)
        return Val(self.emit("%s + %s" % (a.var, self.const(a.pend)), a.bound + a.pend, 1), a.bound + a.pend)

    def add(self, a, b):
        while a.bound + b.bound >= LIMIT:
            if a.bound >= b.bound:
                a = self.reduce(a)
            else:
                b = self.reduce(b)
        return Val(self.emit("%s + %s" % (a.var, b.var), a.bound + b.bound, 1), a.bound + b.bound,
                   (a.pend + b.pend) & M)

    def operand(self, e):
        if isinstance(e, str):
            a = self.mat(self.vals[e])
            self.vals[e] = a
            return a
        return self.comp(e, read=True)

    def comp(self, e, read=False):
        if isinstance(e, str):
            return self.operand(e) if read else self.vals[e]
        k = e[0]
        if k == "sum":
            acc, pend = None, 0
            for t in e[1]:
                neg = isinstance(t, tuple) and t[0] == "neg"
                x = t[1] if neg else t
                if isinstance(x, int):
                    pend += -x if neg else x
                    continue
                if neg:                   # x - z = x + (z XOR M) + 1
                    z = self.operand(x)
                    b = (1 << max(32, z.bound.bit_length())) - 1
                    v = Val(self.emit("%s ^ M_ALL" % z.var, b, 1), b, 1)
                else:
                    v = self.comp(x)
                acc = v if acc is None else self.add(acc, v)
            acc = Val(acc.var, acc.bound, (acc.pend + pend) & M)
            return self.mat(acc) if read else acc
        if k == "xor":
            a, b = e[1], e[2]
            if isinstance(a, int):
                a, b = b, a
            x = self.operand(a)
            if isinstance(b, int):
                bd = (1 << max(32, x.bound.bit_length())) - 1
                return Val(self.emit("%s ^ %s" % (x.var, self.const(b)), bd, 1), bd)
            y = self.operand(b)
            bd = (1 << max(x.bound.bit_length(), y.bound.bit_length(), 32)) - 1
            return Val(self.emit("%s ^ %s" % (x.var, y.var), bd, 1), bd)
        x = self.operand(e[1])
        r = e[2]
        return Val(self.emit("((%s >> %d) & A%d) | ((%s << %d) & B%d)" % (x.var, r, r, x.var, 32 - r, r), M, 5), M)


def rot_masks():
    ns = {}
    for r in range(1, 32):
        ns["A%d" % r] = ((1 << (32 - r)) - 1) * ONES
        ns["B%d" % r] = (((1 << r) - 1) << (32 - r)) * ONES
    return ns


def compile_batch(fe_base):
    P = Packed()
    P.at("random words")
    for k in range(7):                   # the draw (charged one unit) and an AND with M
        P.units["random words"] += 1
        P.vals[OUTER_WORDS[k]] = Val(P.emit("R%d & M_ALL" % k, M, 1), M)
    P.units["random words"] += 1
    P.vals["Y4"] = Val(P.emit("R7 & F_ALL", FREE_MASK, 1), FREE_MASK, Y_PEND)
    P.at("CO lines to Y9 and omega")
    for name, e in slice_lines():
        P.vals[name] = P.comp(e)
    P.vals["Y9"] = P.operand("Y9")
    P.at("omega")
    om = P.comp(Sum("Y4", "w8", Y3), read=True)
    P.vals["omega"] = om
    P.at("automaton (2), 7 lanes")
    masks = []
    for i in range(LANES):
        s = None
        for p in range(4):
            sh = 36 * i + 8 * p
            b = P.emit("(%s >> %d) & 255" % (om.var, sh), 255, 2) if sh else P.emit("%s & 255" % om.var, 255, 1)
            s = P.emit("FE[%s + %d]" % (b, fe_base), 0, 2) if p == 0 else P.emit("FE[%s + %s]" % (s, b), 0, 2)
        P.units[P.part] += 2             # test of the mask, branch
        masks.append(s)
    P.code.append("return %s, %s, (%s,)" % (P.vals["Y9"].var, om.var, ", ".join(masks)))
    src = "def batch(%s):\n    %s\n" % (", ".join("R%d" % k for k in range(8)), "\n    ".join(P.code))
    return src, dict(P.units), P.vals, P.bounds, P.maxbound, P.consts


class Search:
    'Tables, the compiled batch and its charge.'

    def __init__(self, check_bounds=False):
        self.t1, self.t2 = build_tables()
        self.fe, fe_base = flatten(self.t2)
        self.fq, self.fq_base = flatten(self.t1)
        src, self.units, self.vals, self.bounds, self.maxbound, consts = compile_batch(fe_base)
        ns = dict(rot_masks(), M_ALL=M_ALL, F_ALL=F_ALL, FE=self.fe, **consts)
        exec(src, ns)
        self.batch = ns["batch"]
        if check_bounds:                 # a variant returning every temporary, for the lane-bound check
            exec(src.replace("\n    return ", "\n    return locals(), "), ns)
            self.batch_all = ns["batch"]
        self.batch_units = sum(self.units.values()) + CHARGE_BATCH_COUNT + CHARGE_DISPATCH
        # direct tables (9.8): the 125 units of the automaton of (2) with its bases become 41 lane tests; + 1 kept
        self.batch_charge = self.batch_units - self.units["automaton (2), 7 lanes"] + CHARGE_LANE_TESTS + 1

    def q_path(self, y9):
        fq = self.fq
        s = fq[(y9 & 255) + self.fq_base]
        s = fq[s + (y9 >> 8 & 255)]
        s = fq[s + (y9 >> 16 & 255)]
        return fq[s + (y9 >> 24 & 255)]


def draw(seed, b):
    'The eight fresh uniform 256-bit words of batch b of a trial (SHAKE-256 of a label, the seed, b).'
    buf = hashlib.shake_256(b"halfsearch batch" + seed + b.to_bytes(8, "little")).digest(256)
    return [int.from_bytes(buf[32 * k:32 * k + 32], "little") for k in range(8)]


def lane(x, i):
    return x >> (36 * i) & M


class Halt(Exception):
    pass


def iter_passes(seed, b0, b1, S, c, verify=False, e_budget=E_BUDGET, pass_budget=PASS_BUDGET):
    """Batches b0..b1-1 of step 1; yields (step, eight words, names of step CO, X) for every passing outer step.
    c receives batches, steps, e_count, passes, outer units (and verify counts). Halt at a budget (9.1)."""
    for key in ("batches", "steps", "e_count", "passes", "outer_units", "verified_lanes", "verify_fail",
                "bound_fail"):
        c.setdefault(key, 0)
    for b in range(b0, b1):
        Rw = draw(seed, b)
        if verify:
            env, y9p, omp, masks = S.batch_all(*Rw)
            for v, bd in S.bounds.items():
                if bd:
                    c["bound_fail"] += any((env[v] >> 36 * i) & (LIMIT - 1) > bd for i in range(LANES))
        else:
            y9p, omp, masks = S.batch(*Rw)
        c["batches"] += 1
        c["outer_units"] += S.batch_charge
        c["steps"] += LANES
        for i in range(LANES):
            m2 = masks[i]
            if verify:
                v = scalar_outer([lane(Rw[k], i) for k in range(8)])
                ok = lane(y9p, i) == v["Y9"] and lane(omp, i) == v["omega"] and m2 == look(S.t2, v["omega"])
                ok &= all((lane(env[val.var], i) + val.pend) & M == v[n] for n, val in S.vals.items() if n in v)
                ok &= S.q_path(v["Y9"]) == look(S.t1, v["Y9"])
                c["verified_lanes"] += 1
                c["verify_fail"] += not ok
            if not m2:
                continue
            c["e_count"] += 1
            c["outer_units"] += CHARGE_E_LANE
            if c["e_count"] > e_budget:
                raise Halt("E count exceeds E_BUDGET")
            m1 = S.q_path(lane(y9p, i))
            x = m1 & m2
            if not x:
                continue
            c["passes"] += 1
            c["outer_units"] += CHARGE_PASS
            if c["passes"] > pass_budget:
                raise Halt("pass count exceeds PASS_BUDGET")
            eight = [lane(Rw[k], i) for k in range(8)]
            v = scalar_outer(eight)
            if v["Y9"] != lane(y9p, i) or v["omega"] != lane(omp, i):
                c["verify_fail"] += 1
            yield 7 * b + i, eight, v, x


# ---- the joint solver of 9.4, pre-check, (G7) and (G15) of 9.7; the generic solver of 9.8 for X3 ------------------
def is_joint_root(Q, y, E, h, tau, eps=EPS, mu=MU):
    'The words (J1), (J2), (J3) of an outcome with its eps and mu (Lemmas V and V9).'
    sigma = tau ^ ror(tau, 1)
    theta = rol(sigma, 12)
    gg = (Q + h) & M
    if (gg ^ ((Q + (h ^ ETA)) & M)) != theta:
        return False
    f = ror(y ^ gg, 12)
    e2 = (E + f) & M
    if (e2 ^ ((((E + DY3) & M) + (f ^ sigma)) & M)) != eps:
        return False
    h2 = ror(h ^ e2, 8)
    return (((gg + h2) & M) ^ (((gg ^ theta) + (h2 ^ mu)) & M)) == tau


class Row:
    'Static descriptor of an outcome (eps of beta* for S, eps3 for X3).'

    def __init__(self, tau, eps=EPS):
        self.tau, self.eps, self.mu = tau, eps, ror(ETA ^ eps, 8)
        self.sigma = tau ^ ror(tau, 1)
        self.theta = rol(self.sigma, 12)
        self.gamma = ETA ^ self.theta
        self.D = (self.sigma ^ eps) & 0x7FFFFFFF
        self.low = tau in LOW_TAUS
        self.family = (self.low, bit(self.gamma, 10))
        self.const_pos = {10, 11, 12, 16, 17, 18, 19, 24, 26}
        self.guard_pos = {25, 29}
        self.select_pos = 20

    def prescribed(self, i):
        k = (i + 20) % 32
        return (i < 31 and bit(self.gamma, i)) or (k < 31 and bit(self.D, k))

    def free_positions(self):
        'Free positions of the joint solver of 9.4 on S: (G7) takes 7 and (G15) takes 15.'
        return [i for i in range(7, 32) if i not in self.const_pos | self.guard_pos | {self.select_pos, 7, 15}
                and not self.prescribed(i)]

    def generic_free(self):
        'Free positions of the generic solver of 9.8: (G7), (G15b) and (G20b) take 7, 15 and 20.'
        return [i for i in range(32) if not self.prescribed(i) and i not in (7, 15, 20)]


ROWS = {t: Row(t) for t in TAUS}
XROWS = {t: Row(t, EPS3) for t in X3_TAUS}


def arc_of(desc, u, a, v):
    'Transition relation of 9.4 for one position: a 5-bit arc, or 0.'
    Qi, yi, Ek, Epk, etai, gi, sk, kk, gi1, kk1, hasc, cval, li, lk = desc
    gg = Qi ^ v ^ u
    u1 = maj(Qi, v, u)
    up1 = maj(Qi, v ^ etai, u ^ gi)
    if not li and up1 != (u1 ^ gi1):
        return 0
    f = yi ^ gg
    e2 = Ek ^ f ^ a
    a1 = maj(Ek, f, a)
    ap1 = maj(Epk, f ^ sk, a ^ kk)
    if not lk and ap1 != (a1 ^ kk1):
        return 0
    if lk:
        a1 = 0
    if li:
        u1 = 0
    return 0x10 | (u1 << 3) | (a1 << 2) | (v << 1) | e2


def build_arrays():
    'The forced (2^16), dual (2^16) and selected (2^17) arrays, built from the relation.'
    forced, dual, selected = [0] * (1 << 16), [0] * (1 << 16), [0] * (1 << 17)
    for key14 in range(1 << 14):
        d = tuple((key14 >> (13 - t)) & 1 for t in range(14))
        Qi, yi, Ek, Epk, etai, gi, sk, kk, gi1, kk1, hasc, cval, li, lk = d
        prescribed = (not li and gi) or (not lk and (kk ^ Ek ^ Epk))
        for cp in range(4):
            arcs = [arc_of(d, cp >> 1, cp & 1, 0), arc_of(d, cp >> 1, cp & 1, 1)]
            key = (key14 << 2) | cp
            dual[key] = arcs[0] | (arcs[1] << 5)
            if hasc:
                forced[key] = arcs[cval]
            else:
                passing = [x for x in arcs if x]
                if len(passing) == 1:
                    forced[key] = passing[0]
                assert not (len(passing) == 2 and prescribed), "Lemma S5"
            for want in (0, 1):
                cand = [x for x in ((arcs[cval],) if hasc else arcs) if x and (x & 1) == want]
                assert len(cand) <= 1
                selected[(key << 1) | want] = cand[0] if cand else 0
    return forced, dual, selected


FORCED = DUAL = SELECTED = None


def arrays():
    global FORCED, DUAL, SELECTED
    if FORCED is None:
        FORCED, DUAL, SELECTED = build_arrays()


def descriptor(row, Q, y, E, Ep, kappa, i, hasc=0, cval=0):
    k = (i + 20) % 32
    d = (bit(Q, i), bit(y, i), bit(E, k), bit(Ep, k), bit(ETA, i), bit(row.gamma, i), bit(row.sigma, k),
         bit(kappa, k), bit(row.gamma, i + 1) if i < 31 else 0, bit(kappa, k + 1) if k < 31 else 0,
         hasc, cval, int(i == 31), int(k == 31))
    key = 0
    for b_ in d:
        key = (key << 1) | b_
    return key


def mask_X(Q):
    'Bit j iff some h has (J1) for the outcome of bit j (X3 shares (1) with the S row of its tau).'
    X_ = 0
    for j, tau in enumerate(TAUS + X3_TAUS):
        if j1_exists(Q, theta_of(tau)):
            X_ |= 1 << j
    return X_


def j1_exists(Q, theta):
    gamma = ETA ^ theta
    if bit(gamma, 0):
        return False
    states = {0}
    for i in range(32):
        nxt = set()
        for u in states:
            for v in (0, 1):
                u1 = maj(bit(Q, i), v, u)
                up1 = maj(bit(Q, i), v ^ bit(ETA, i), u ^ bit(gamma, i))
                if i == 31 or up1 == u1 ^ bit(gamma, i + 1):
                    nxt.add(u1)
        states = nxt
        if not states:
            return False
    return True


def nu_of(Q, e1, C, B):
    'The s-pattern of 9.7 from (V).'
    r = (((Q >> 16) ^ e1) & 4) ^ 7
    return ((((r + C) & M) ^ B) ^ 1) & 7


def g7_value(h6, e1, C, B):
    'Guard (G7): h[7] from h[6], e1, C2.c1 and C2.b1 (the same for beta* and beta3).'
    x = h6 ^ bit(e1, 22)
    a22 = x ^ bit(C, 22) ^ bit(B, 22)
    return bit(e1, 23) ^ 1 ^ bit(C, 23) ^ bit(B, 23) ^ maj(x, bit(C, 22), a22)


def cstar_of(pref, gw, x3):
    'cstar of (G15) (x3 False) or (G15b) (x3 True) from the prefix h[0..14]; gw = (e1, C, B, A, V).'
    e1, C, B, A, V = gw
    a22 = bit(pref, 6) ^ bit(e1, 22) ^ bit(C, 22) ^ bit(B, 22)
    v16 = bit(V, 16) ^ bit(A, 16) ^ (0 if x3 else 1)
    L_ = ((pref & 0x7FFF) >> 6) ^ (e1 >> 22)
    zeta = (((L_ + (C >> 22) + a22) ^ (B >> 22)) >> 1) & 0x1FF
    p15 = (zeta + ((A >> 16) & 0x1FF) + v16) & 0x1FF
    return (Y11 & 0x1FF) + (p15 ^ ((V >> 16) & 0x1FF))


def g15_value(pref, gw, x3):
    'h[15] by (G15) or (G15b), or None when the low-cube test drops the prefix.'
    cs = cstar_of(pref, gw, x3)
    if (cs & (0x8D if x3 else 0x8B)) != (1 if x3 else 0):
        return None
    return (cs >> 8) & 1


def prescription(Ek, Epk, sk, kk1, a):
    'f[k] for D[k] = 1 (Lemma S5).'
    return (Ek ^ sk ^ kk1) if a == Ek else (Epk ^ kk1)


def row_setup(row, Q, y, E, Ep, e1, kappa, C, B, notes, cnt):
    'Constants and guards (a)-(g) of 9.4, (G7), and the walks of bits 0..6. None if the row is dropped.'
    b, u = bit(e1, 2), bit(e1, 21)
    sg, gm = row.sigma, row.gamma

    def Eb(k):
        return bit(E, k)

    def Epb(k):
        return bit(Ep, k)

    def kb(k):
        return bit(kappa, k)

    def sb(k):
        return bit(sg, k)
    kept = []                                            # (a) carry into bit 22
    for a20 in (0, 1):
        a, ap, ok = a20, a20 ^ kb(20), True
        for k in (20, 21):
            a1 = maj(Eb(k), 0, a)
            ap1 = maj(Epb(k), sb(k), ap)
            if ap1 != a1 ^ kb(k + 1):
                ok = False
                break
            a, ap = a1, ap1
        if ok:
            kept.append((a20, a))
    if not kept:
        return None
    if len({a22 for _, a22 in kept}) != 1:
        notes.append("two kept guesses with different a[22]")
    a22 = kept[0][1]
    f22 = prescription(Eb(22), Epb(22), sb(22), kb(23), a22)          # (b)
    a23 = maj(Eb(22), f22, a22)
    f23 = prescription(Eb(23), Epb(23), sb(23), kb(24), a23) if bit(gm, 3) == 0 else 1 ^ bit(Q, 3) ^ bit(y, 3)
    a = a22
    for k, fk in ((22, f22), (23, f23)):
        a1 = maj(Eb(k), fk, a)
        if maj(Epb(k), fk ^ sb(k), a ^ kb(k)) != a1 ^ kb(k + 1):
            return None
        a = a1
    a24 = a
    h = {0: 0, 1: 1}                                     # (c)
    h[2] = bit(y, 2) ^ f22 ^ bit(Q, 2)
    if h[2] != 1 ^ b:
        return None
    u3 = maj(h[2], bit(Q, 2), 0)
    h[3] = bit(y, 3) ^ f23 ^ bit(Q, 3) ^ u3
    u4 = maj(h[3], bit(Q, 3), u3)
    h[10] = b
    h[11] = 1 ^ h[3]
    u11 = maj(h[10], bit(Q, 10), bit(Q, 9)) if bit(gm, 10) == 0 else bit(Q, 10)
    u12 = maj(h[11], bit(Q, 11), u11)
    f0 = prescription(Eb(0), Epb(0), sb(0), kb(1), 0)                 # (d)
    a1_ = maj(Eb(0), f0, 0)
    h[12] = bit(y, 12) ^ f0 ^ bit(Q, 12) ^ u12
    u13 = maj(h[12], bit(Q, 12), u12)
    h[24] = h[3] ^ h[12] ^ u
    f24 = h[24] ^ Eb(24) ^ a24                                        # (e)
    h[4] = bit(y, 4) ^ f24 ^ bit(Q, 4) ^ u4
    a25 = maj(Eb(24), f24, a24)
    if maj(Epb(24), f24 ^ sb(24), a24 ^ kb(24)) != a25 ^ kb(25):
        return None
    u5 = maj(h[4], bit(Q, 4), u4)
    f25 = prescription(Eb(25), Epb(25), sb(25), kb(26), a25)
    a26 = maj(Eb(25), f25, a25)
    h[5] = bit(y, 5) ^ f25 ^ bit(Q, 5) ^ u5
    if row.low:                                                       # (f)
        if Eb(1) == a1_:
            f2 = prescription(Eb(2), Epb(2), sb(2), kb(3), Eb(1))
            e2_2 = Eb(2) ^ f2 ^ Eb(1)
        else:
            if kb(2) == 1:
                return None
            e2_2 = Eb(2) ^ kb(3)
        h[26] = 1 ^ h[2] ^ e2_2 ^ bit(Q, 26) ^ bit(Q, 25)
        h[6] = h[26] ^ Eb(26) ^ a26 ^ bit(y, 6) ^ bit(gm, 7)
    else:
        h[6] = bit(y, 13) ^ bit(Q, 13) ^ u13 ^ Eb(1) ^ a1_ ^ u
    h[16] = h[17] = 0                                                 # (g)
    h[18] = 1 ^ bit(Q, 18)
    h[19] = bit(Q, 19)
    if bit(gm, 7):
        h[7] = 1 ^ bit(gm, 8) ^ h[6]
    v7 = g7_value(h[6], e1, C, B)                                     # (G7)
    if 7 in h and h[7] != v7:
        return None
    h[7] = v7
    states, e2_26 = set(), set()
    for a20, _ in kept:                                  # walks of bits 0..6: each lookup is charged as a
        uu, aa, ok = 0, a20, True                        # forced node (U_FORCED), counted in cnt["walk"]
        for i in range(7):
            cnt["walk"] += 1
            arc = FORCED[(descriptor(row, Q, y, E, Ep, kappa, i, 1, h[i]) << 2) | (uu << 1) | aa]
            if not arc:
                ok = False
                break
            uu, aa = (arc >> 3) & 1, (arc >> 2) & 1
            if i == 6:
                e2_26.add(arc & 1)
        if ok:
            states.add((uu, aa))
    if not states:
        return None
    if len(states) > 1:
        notes.append("kept guesses reach different states at depth 7")
    if not row.low:
        if len(e2_26) != 1:
            notes.append("e2[26] differs between guesses")
        h[26] = min(e2_26)
    return h, sorted(states)


def traverse(row, Q, y, E, Ep, kappa, e1, h, states, gw, cnt):
    'Positions 7..31 of 9.4 from the states of row_setup; (G15) at position 15 (Lemma G15).'
    u = bit(e1, 21)
    free = set(row.free_positions())
    keys = {i: descriptor(row, Q, y, E, Ep, kappa, i, 1, h[i]) if i in h else
            descriptor(row, Q, y, E, Ep, kappa, i, 0, 0) for i in range(7, 32)}
    pref0 = sum(h[i] << i for i in range(7))
    roots = []
    stack = [(7, uu, aa, pref0, 0) for (uu, aa) in states]
    while stack:
        i, uu, aa, pref, e29 = stack.pop()
        if i == 32:
            cnt["leaves"] += 1
            if is_joint_root(Q, y, E, pref, row.tau):
                roots.append(pref)
            continue
        cp = (uu << 1) | aa
        if i in free:
            cnt["free"] += 1
            w = DUAL[(keys[i] << 2) | cp]
            arcs = [w & 0x1F, (w >> 5) & 0x1F]
        elif i == 15:
            cnt["forced"] += 1
            cnt["g15"] += 1
            v15 = g15_value(pref, gw, False)
            arcs = [] if v15 is None else [FORCED[((keys[15] | 8 | (v15 << 2)) << 2) | cp]]
        else:
            arcs = [fixed_arc(i, keys[i], cp, pref, e29, u, cnt)]
        for arc in arcs:
            if arc:
                stack.append((i + 1, (arc >> 3) & 1, (arc >> 2) & 1, pref | (((arc >> 1) & 1) << i),
                              (arc & 1) if i == 9 else e29))
    return roots


def fixed_arc(i, key, cp, pref, e29, u, cnt):
    'A non-free position: Lemma J0 at 20, the guards at 25 and 29, else forced (each a forced node).'
    cnt["forced"] += 1
    if i == 20:
        cnt["selected"] += 1
        return SELECTED[(((key << 2) | cp) << 1) | bit(pref, 8)]
    if i == 25:
        return FORCED[((key | 8 | ((bit(pref, 6) ^ bit(pref, 13) ^ u) << 2)) << 2) | cp]
    if i == 29:
        return FORCED[((key | 8 | ((1 ^ e29) << 2)) << 2) | cp]
    return FORCED[(key << 2) | cp]


def new_count():
    return dict(forced=0, selected=0, free=0, g15=0, leaves=0, walk=0)


def solve(Q, y, E, C, B, rows, gw):
    'The joint solver on the rows of T; units by the blocks of Section 11: C15(T) <= 17,504.'
    arrays()
    e1 = (Y3 + y) & M
    assert e1 & CLASS_MASK == CLASS_VALUE
    Ep = (E + DY3) & M
    notes, roots, cnt = [], [], new_count()
    if not rows:
        return dict(roots=[], units=0, counts=cnt, notes=notes)
    for t in rows:
        row = ROWS[t]
        kappa = row.sigma ^ EPS ^ E ^ Ep
        res = row_setup(row, Q, y, E, Ep, e1, kappa, C, B, notes, cnt)
        if res is not None:
            roots += [(r, t, False) for r in traverse(row, Q, y, E, Ep, kappa, e1, res[0], res[1], gw, cnt)]
    units = (U_GLOBAL + U_FAMILY * len({ROWS[t].family for t in rows}) + U_ROW * len(rows)
             + U_FORCED * cnt["forced"] + U_SELECTED_EXTRA * cnt["selected"] + U_FREE * cnt["free"]
             + U_G15 * cnt["g15"] + U_LEAF * cnt["leaves"])
    return dict(roots=roots, units=units, counts=cnt, notes=notes)


def xsolve(row, Q, y, E, gw, guards=True, leaf=None, g20=None):
    """The generic solver of 9.8 on one row of X3: (J1) and (J2) bit by bit from bit 0, both guesses of the carry
    a20, at most one child at a prescribed position, (G7) at 7, (G15b) at 15 and (G20b) at 20 (the selected array
    with the desired bit h[8]); (J1)-(J3) as words at every leaf."""
    arrays()
    Ep = (E + DY3) & M
    kappa = row.sigma ^ row.eps ^ E ^ Ep
    e1, C, B = gw[:3] if guards else (0, 0, 0)
    g20 = guards if g20 is None else g20
    keys = [descriptor(row, Q, y, E, Ep, kappa, i) for i in range(32)]
    pres = [row.prescribed(i) for i in range(32)]
    roots, nodes, gn, leaves = [], 0, 0, 0
    for a20 in (0, 1):
        stack = [(0, 0, a20, 0)]
        while stack:
            i, uu, aa, pref = stack.pop()
            if i == 32:
                leaves += 1
                if (leaf(pref) if leaf else is_joint_root(Q, y, E, pref, row.tau, row.eps, row.mu)):
                    roots.append((pref, row.tau, True))
                continue
            nodes += 1
            key = (keys[i] << 2) | (uu << 1) | aa
            if guards and (i == 7 or i == 15):
                gn += 1
                v = g7_value(bit(pref, 6), e1, C, B) if i == 7 else g15_value(pref, gw, True)
                arcs = () if v is None else ((DUAL[key] >> 5 * v) & 0x1F,)
            elif g20 and i == 20:
                gn += 1
                arcs = (SELECTED[(key << 1) | bit(pref, 8)],)
            elif pres[i]:
                arcs = (FORCED[key],)
            else:
                arcs = (DUAL[key] & 0x1F, DUAL[key] >> 5)
            for arc in arcs:
                if arc:
                    stack.append((i + 1, (arc >> 3) & 1, (arc >> 2) & 1, pref | (((arc >> 1) & 1) << i)))
    units = X_SETUP + X_NODE * nodes + X_LEAF * leaves + X_GUARD * gn
    return dict(roots=roots, units=units, nodes=nodes, leaves=leaves)


def static_row(row):
    'Static tree of a row of X3 per guess (9.8): N nodes at positions 0..31, L leaves, n7, n15, n20, and C_row.'
    free = row.generic_free()
    n = [1 << sum(1 for f in free if f < i) for i in range(33)]
    N = sum(n[:32])
    guarded = n[7] + n[15] + n[20]
    return N, n[32], n[7], n[15], n[20], X_SETUP + 2 * (X_NODE * N + X_LEAF * n[32] + X_GUARD * guarded)


def g20b_check():
    """Lemma G20b on every row of X3, exhaustively: (J2) depends on f only through pf = f AND sigma (e2' = e2 + d,
    d = DY3 + sigma - 2 pf); for every pf, whether some e2 has e2 XOR (e2 + d) = eps3 (bit-serial over the carry);
    no such pf may have bit 20 (sigma[20] = 1). With g[0] = y[0] XOR f[20] = 0, (J3) at bits 0 and 1 forces h2[0] = 0
    for every g[1] and h2[0..1]. Returns {row: [pf that admit (J2), those with f[20] = 1]} and the low-bit result."""
    out, low = {}, (CLASS_MASK & 1) == 1 and (CLASS_VALUE - Y3) & 1 == 0
    for t in X3_TAUS:
        sg, ok, bad = XROWS[t].sigma, 0, 0
        p = sg
        while True:
            d, st = (DY3 + sg - 2 * p) & M, {0}
            for i in range(32):
                st = {maj(e, bit(d, i), c) for c in st if bit(d, i) ^ c == bit(EPS3, i) for e in (0, 1)}
                if not st:
                    break
            if st:
                ok += 1
                bad += bit(p, 20)
            if p == 0:
                break
            p = (p - 1) & sg
        out["%08x" % t] = [ok, bad]
        th = theta_of(t)
        low &= bit(sg, 20) == 1 and ok > 0 and bad == 0 and all(
            j & 1 == 0 for g_ in (0, 2) for j in range(4) if (((g_ + j) ^ ((g_ ^ th) + (j ^ MU3))) & 3) == t & 3)
    return out, low



# ---- step 3: the certificate, and the pair of the trial -------------------------------------------------------------
def compress2(msg, t=COUNTER, flags=FLAGS):
    'The 2-round compression of one block: (message words, chaining value, state before the second diagonal step).'
    n = len(msg)
    w = list(struct.unpack("<16I", msg + bytes(64 - n)))
    v = list(IV) + list(IV[:4]) + [t & M, t >> 32, n, flags]
    s, yst = list(w), None
    for r in range(2):
        for i, (a, b, c, d) in enumerate(GCALLS):
            if r == 1 and i == 4:
                yst = list(v)
            v[a], v[b], v[c], v[d] = g(v[a], v[b], v[c], v[d], s[2 * i], s[2 * i + 1])
        s = [s[p] for p in PERM]
    return w, [v[i] ^ v[i + 8] for i in range(8)], yst


def c1_of(v, h):
    'Inverse of Lemma IP: Y14 = ROL(h,16) XOR (Y3 + y), Y6, E1.a1, c1.'
    y14 = rol(h, 16) ^ ((Y3 + v["Y4"]) & M)
    y6 = ror(((y14 + v["C2.c1"]) & M) ^ v["C2.b1"], 7)
    return (Y11 + ror(((y6 + v["Y1"] + v["w12"]) & M) ^ v["Y12"], 16)) & M


def c1_t0(v):
    'The one c1 for which step CT forces t = 0: K0.a1 = ROL(K0.d1,16), w0, Y2, Y14, then Lemma IP.'
    w0 = (rol(v["K0.d1"], 16) - IV[0] - IV[4]) & M
    y14 = ror(((w0 + v["C2.a1"] + v["C2.b1"]) & M) ^ v["C2.d1"], 8)
    return c1_of(v, ror(y14 ^ ((Y3 + v["Y4"]) & M), 16))


def step_ct(v, c1):
    'The lines of step CT for E1.c1 = c1: Y names, w0, w1, the counter word t, blocks A and B.'
    u = dict(v)
    u["E1.d1"] = (c1 - Y11) & M
    u["E1.a1"] = rol(u["E1.d1"], 16) ^ u["Y12"]
    u["Y6"] = (u["E1.a1"] - u["Y1"] - u["w12"]) & M
    u["Y10"] = rol(u["Y6"], 7) ^ u["C2.b1"]
    u["Y14"] = (u["Y10"] - u["C2.c1"]) & M
    u["E1.b1"] = ror(u["Y6"] ^ c1, 12)
    u["Y2"] = rol(u["Y14"], 8) ^ u["C2.d1"]
    u["E3.h1"] = ror(u["Y14"] ^ ((Y3 + u["Y4"]) & M), 16)
    u["w0"] = (u["Y2"] - u["C2.a1"] - u["C2.b1"]) & M
    u["K0.a1"] = (IV[0] + IV[4] + u["w0"]) & M
    u["t"] = rol(u["K0.d1"], 16) ^ u["K0.a1"]
    u["w1"] = (u["S0"] - u["K0.a1"] - u["K0.b1"]) & M
    w = [u.get("w%d" % i, 0) for i in range(16)]
    w[4], w[13] = W4, W13
    b = list(w)
    b[4], b[5] = W4B, (w[5] + DELTA5) & M
    pa, pb = struct.pack("<16I", *w), struct.pack("<16I", *b)
    assert not any(pa[LEN_A:]) and not any(pb[LEN_B:])
    u["A"], u["B"], u["c1"] = pa[:LEN_A], pb[:LEN_B], c1
    return u


def e_steps(yy, w):
    'E1 (diagonal 1,6,11,12 with w12, w5) and E3 (diagonal 3,4,9,14 with w15, w8).'
    e1c = (yy[11] + ror(yy[12] ^ ((yy[1] + yy[6] + w[12]) & M), 16)) & M
    e1 = g(yy[1], yy[6], yy[11], yy[12], w[12], w[5])
    a1 = (yy[3] + yy[4] + w[15]) & M
    d1 = ror(yy[14] ^ a1, 16)
    c1 = (yy[9] + d1) & M
    a2 = (a1 + ror(yy[4] ^ c1, 12) + w[8]) & M
    c2 = (c1 + ror(d1 ^ a2, 8)) & M
    return dict(e1c=e1c, e1b=ror(yy[6] ^ e1c, 12), e1a=e1[0], e1c2=e1[2], d1=d1, c1=c1, a2=a2, c2=c2)


def evaluate(u, t):
    'Both compressions at counter t, flags 11: names, E1 and E3 differences, chaining values.'
    wa, cva, ya = compress2(u["A"], t)
    wb, cvb, yb = compress2(u["B"], t)
    ea, eb = e_steps(ya, wa), e_steps(yb, wb)
    cons = (all(ya[i] == u["Y%d" % i] for i in (0, 1, 2, 4, 5, 6, 8, 9, 10, 12, 13, 14))
            and (ya[3], ya[11], yb[3], yb[11], yb[4]) == (Y3, Y11, Y3B, Y11B, u["Y4"])
            and ea["e1c"] == u["c1"] and ea["e1b"] == u["E1.b1"] and ea["d1"] == u["E3.h1"])
    return dict(cons=cons, b1x=ea["e1b"] ^ eb["e1b"], ax=ea["e1a"] ^ eb["e1a"], cx=ea["e1c2"] ^ eb["e1c2"],
                j=(ea["c1"] ^ eb["c1"], ea["a2"] ^ eb["a2"], ea["c2"] ^ eb["c2"]), cv_equal=cva == cvb)


def certificate(v, h, tau, x3):
    """Step 3 for one root (h, tau) on the root instance with the cube, beta and eps of its outcome (beta* or beta3):
    the first failing test, or "certified" (every test holds)."""
    eps, beta, cm, cv = (EPS3, BETA3, Q3_MASK, Q3_VALUE) if x3 else (EPS, BETA_STAR, QSTAR_MASK, QSTAR_VALUE)
    c1 = c1_of(v, h)
    if c1 & cm != cv:
        return "c1 not in its cube"
    u = step_ct(v, c1)
    if u["t"] != COUNTER:
        return "t != 0"
    ev_ = evaluate(u, u["t"])
    if not ev_["cons"]:
        return "names differ from the compression"
    if ev_["j"] != (theta_of(tau), eps, tau):
        return "J words"
    if (ev_["ax"], ev_["cx"], ev_["b1x"]) != (tau, eps, beta):
        return "E1 differences"
    if not ev_["cv_equal"]:
        return "chaining values differ"
    return "certified"


def pair_of(v):
    'The pair of an outer step: step CT with the c1 that forces t = 0 (the harness counter).'
    u = step_ct(v, c1_t0(v))
    assert u["t"] == COUNTER
    return u["A"], u["B"]


# ---- one trial of the pipeline --------------------------------------------------------------------------------------
SEARCH = None


def get_search():
    global SEARCH
    if SEARCH is None:
        SEARCH = Search()
        arrays()
    return SEARCH


def pipeline(v, X_, c):
    """Pre-check of 9.7, step 2 and step 3 on one passing outer step: the joint solver on T, the generic solver on
    every row of X_3; the units of steps 2 and 3 by the blocks of Section 11, tested against the caps."""
    Q, y, E, e1, C, B = v["Y9"], v["Y4"], v["omega"], v["e1"], v["C2.c1"], v["C2.b1"]
    gw = (e1, C, B, (v["Y1"] + v["w12"]) & M, v["Y12"])
    T = X_ & S_MASK & VMASK[nu_of(Q, e1, C, B)]
    x3 = [t for j, t in enumerate(X3_TAUS) if X_ >> (7 + j) & 1]
    roots, su, xu = [], 0, 0
    if T:
        c["s_steps"] += 1
        r = solve(Q, y, E, C, B, [t for j, t in enumerate(TAUS) if T >> j & 1], gw)
        su, roots = r["units"], r["roots"]
    if x3:
        c["x3_steps"] += 1
        for t in x3:
            r = xsolve(XROWS[t], Q, y, E, gw)
            c["x3_rows"] += 1
            c["over_cap"] += r["units"] > X_CAPS[t]
            xu += r["units"]
            roots += r["roots"]
    c["over_cap"] += (su > CAP_S) + (xu > CAP_X3) + (len(x3) > 2 or x3[:2] == [0x185020A0, 0x285020A0])
    c["solver_units"] += su + xu
    c["solver_units_max"] = max(c["solver_units_max"], su + xu)
    for h, tau, is3 in roots:
        c["roots"] += 1
        c["certified"] += certificate(v, h, tau, is3) == "certified"


def run_trial(seed):
    'One organizer trial: TRIAL_BATCHES batches of the search; the outer step of the pair; the counts.'
    S = get_search()
    oc = {}
    c = dict(s_steps=0, x3_steps=0, x3_rows=0, solver_units=0, solver_units_max=0, over_cap=0, roots=0, certified=0)
    first, halted = None, 0
    try:
        for step, eight, v, X_ in iter_passes(seed, 0, TRIAL_BATCHES, S, oc):
            if first is None:
                first = (step, eight, v)
            pipeline(v, X_, c)
    except Halt:
        halted = 1
    if first is None:
        eight = [lane(w, 0) for w in draw(seed, 0)]
        first = (-1, eight, scalar_outer(eight))
    # The organizer accepts at most 16 numeric observations per trial: 14 here.
    obs = dict(outer_steps=oc["steps"], passes=oc["passes"], halted=halted, verify_fail=oc["verify_fail"], **c)
    obs["units"] = oc["outer_units"] + c["solver_units"]
    obs["pair_step"] = first[0]
    return first, obs


def half_collision(seed):
    (step, eight, v), obs = run_trial(seed)
    a, b = pair_of(v)
    return a, b, obs


# ---- self-test (outside the organizer protocol) ---------------------------------------------------------------------
def brute_masks(n, targets, dy, x):
    m, mk = 0, (1 << n) - 1
    for t, (dz, out) in enumerate(targets):
        for v in range(1 << n):
            if ((x + v) ^ (x + dy + (v ^ dz))) & mk == out & mk:
                m |= 1 << t
                break
    return m


def look_n(tables, x, n):
    s = 0
    for p, t in enumerate(tables):
        b = x >> 8 * p & ((1 << min(8, n - 8 * p)) - 1)
        s = t[s + b if p else b]
    return s


def plant_check(words):
    """The generic traversal of 9.8 with (G20b), without (G7) and (G15b), on a planted word: Q, y, E and h from the
    words, bit 8 of E set so that e2[8] = h[8], sigma and eps the J1 and J2 targets that h meets (a synthetic row);
    h must be among the leaves that meet (J1) and (J2)."""
    Q, y, E, h = words
    gg = (Q + h) & M
    E ^= ((E + ror(y ^ gg, 12)) ^ h) & 0x100
    row = Row(X3_TAUS[0], EPS3)
    row.theta = gg ^ ((Q + (h ^ ETA)) & M)
    row.sigma = ror(row.theta, 12)
    row.gamma = ETA ^ row.theta
    f = ror(y ^ gg, 12)
    row.eps = ((E + f) & M) ^ ((((E + DY3) & M) + (f ^ row.sigma)) & M)
    row.D = (row.sigma ^ row.eps) & 0x7FFFFFFF

    def leaf(x):
        g_ = (Q + x) & M
        f_ = ror(y ^ g_, 12)
        return (g_ ^ ((Q + (x ^ ETA)) & M)) == row.theta and (
            ((E + f_) & M) ^ ((((E + DY3) & M) + (f_ ^ row.sigma)) & M)) == row.eps
    r = xsolve(row, Q, y, E, None, guards=False, leaf=leaf, g20=True)
    return h in [x for x, _, _ in r["roots"]]


def guard_check(v, c1, x3):
    """(G7) and (G15) or (G15b) on the E3.h1 of a word c1 of the cube with Z[22] = 0 and Z[23] = 1 (Lemmas G7,
    G15 and G15b): None when c1 does not have these two bits, else whether both guards give the bits of h."""
    u = step_ct(v, c1)
    C, B, e1 = v["C2.c1"], v["C2.b1"], v["e1"]
    Z = ((u["Y14"] + C) & M) ^ B
    if bit(Z, 22) or not bit(Z, 23):
        return None
    h = u["E3.h1"]
    gw = (e1, C, B, (v["Y1"] + v["w12"]) & M, v["Y12"])
    return g7_value(bit(h, 6), e1, C, B) == bit(h, 7) and g15_value(h, gw, x3) == bit(h, 15)


def selftest(cases, seed):
    rnd = hashlib.shake_256(b"halfsearch selftest" + seed.encode()).digest(64 * cases + 64)
    words = list(struct.unpack("<%dI" % (16 * cases + 16), rnd))
    rep = {}
    rep["constants"] = all(globals()[k] == x for k, x in TEXT_CONSTANTS.items())
    tq, te = filter_targets(8)
    a1, a2 = automaton(tq, 0, 8), automaton(te, DY3 & 255, 8)
    bf = sum(look_n(a1, x, 8) == brute_masks(8, tq, 0, x) and look_n(a2, x, 8) == brute_masks(8, te, DY3, x)
             for x in range(256))
    rep["automata_bruteforce_width8"] = "%d of 256" % bf
    S = Search(check_bounds=True)
    n1, n2 = pattern_counts(S.t1), pattern_counts(S.t2)
    share = {m: sum(c1 * c2 for p, c1 in n1.items() for q, c2 in n2.items() if p & q & m) for m in (S_MASK, S9_MASK)}
    ecount = {m: sum(c2 for q, c2 in n2.items() if q & m) for m in (S_MASK, S9_MASK)}
    rep["S9_SHARE_E_COUNT_from_tables"] = [share[S9_MASK], ecount[S9_MASK]]
    rep["S_SHARE_E_COUNT_from_tables"] = [share[S_MASK], ecount[S_MASK]]
    tables_ok = (share[S9_MASK] == SHARE and ecount[S9_MASK] == E_COUNT
                 and share[S_MASK] == 18289159183466496 and ecount[S_MASK] == 233715456)
    rep["J1_masks_x3_bits_never_185_with_285"] = all(p & 0x180 != 0x180 for p in n1)
    st = {"%08x" % t: static_row(XROWS[t]) for t in X3_TAUS}
    rep["x3_static_N_L_n7_n15_n20_Crow"] = st
    st_ok = all(st["%08x" % t][5] == X_CAPS[t] for t in X3_TAUS) and CAP_UNION == 314996576
    rep["G20b_J2_pf_admitted_and_with_f20"], g20_ok = g20b_check()
    rep["G20b_lemma"] = g20_ok
    oc = {}
    sb = seed.encode()
    npass = len(list(iter_passes(sb, 0, max(1, cases * 64 // 7), S, oc, verify=True)))
    rep["packed_vs_scalar"] = dict(lanes=oc["verified_lanes"], fail=oc["verify_fail"], bound_fail=oc["bound_fail"],
                                   passes=npass, max_lane_bound_bits=S.maxbound.bit_length())
    drills = []
    for eb, pb in ((3, PASS_BUDGET), (E_BUDGET, 0)):
        d = {}
        try:
            for _ in iter_passes(sb, 0, 2048, S, d, e_budget=eb, pass_budget=pb):
                pass
            drills.append(None)
        except Halt:
            drills.append([d["e_count"], d["passes"]])
    rep["halt_drills_E3_P0"] = drills
    rep["batch_units_counted_with_automaton"] = S.batch_units
    rep["batch_charge_direct_tables"] = S.batch_charge
    mx = cons = inv = jid = t0 = half = plant = 0
    gchk = {False: [0, 0], True: [0, 0]}
    arrays()
    for n in range(cases):
        wd = words[16 * n:16 * n + 16]
        mx += mask_X(wd[8]) & S9_MASK == look(S.t1, wd[8])
        v = scalar_outer(wd[:8])
        c1 = wd[9]
        u = step_ct(v, c1)
        ev_ = evaluate(u, u["t"])
        cons += ev_["cons"]
        inv += c1_of(v, u["E3.h1"]) == c1
        h, Q, y, E = u["E3.h1"], v["Y9"], v["Y4"], v["omega"]
        ga, gb = (Q + h) & M, (Q + (h ^ ETA)) & M
        ea, eb = (E + ror(y ^ ga, 12)) & M, (E + DY3 + ror(y ^ gb, 12)) & M
        ca, cb = (ga + ror(h ^ ea, 8)) & M, (gb + ror(h ^ ETA ^ eb, 8)) & M
        jid += ev_["j"] == (ga ^ gb, ea ^ eb, ca ^ cb)
        u0 = step_ct(v, c1_t0(v))
        t0 += u0["t"] == 0 and evaluate(u0, 0)["cons"]
        da, db = compress2(u0["A"])[1], compress2(u0["B"])[1]
        half += all(da[i] == db[i] for i in (0, 2, 5, 7))
        plant += plant_check(wd[10:14])
        for x3, cm, cv in ((False, QSTAR_MASK, QSTAR_VALUE), (True, Q3_MASK, Q3_VALUE)):
            for k in range(8):
                r = guard_check(v, ((wd[14 + (k & 1)] ^ (k * 0x9E3779B9)) & ~cm & M) | cv, x3)
                if r is not None:
                    gchk[x3][0] += 1
                    gchk[x3][1] += r
    rep["maskX_vs_automaton_1"] = "%d of %d" % (mx, cases)
    rep["step_CT_consistent"] = "%d of %d" % (cons, cases)
    rep["inverse_IP"] = "%d of %d" % (inv, cases)
    rep["J_words_equal_E3"] = "%d of %d" % (jid, cases)
    rep["t0_c1_consistent"] = "%d of %d" % (t0, cases)
    rep["half_collision_counter0_flags11"] = "%d of %d" % (half, cases)
    rep["generic_traversal_planted"] = "%d of %d" % (plant, cases)
    rep["G7_G15_on_Qstar"] = "%d of %d" % (gchk[False][1], gchk[False][0])
    rep["G7_G15b_on_Q3"] = "%d of %d" % (gchk[True][1], gchk[True][0])
    rep["seed"] = seed
    json.dump(rep, sys.stdout, separators=(",", ":"))
    sys.stdout.write("\n")
    good = (rep["constants"] and bf == 256 and tables_ok and rep["J1_masks_x3_bits_never_185_with_285"] and st_ok
            and g20_ok
            and oc["verify_fail"] == 0 and oc["bound_fail"] == 0 and S.batch_units == 424
            and drills[0] is not None and drills[0][0] == 4 and drills[1] is not None and drills[1][1] == 1
            and S.batch_charge == CHARGE_BATCH and mx == cons == inv == jid == t0 == half == plant == cases
            and all(a == b and a > 0 for a, b in gchk.values()))
    return 0 if good else 1


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] != "--selftest" or len(sys.argv) not in (3, 4) or not sys.argv[2].isdecimal() or \
                int(sys.argv[2]) < 1:
            raise SystemExit("usage: halfsearch.py [--selftest N [seed]]   (else: organizer request on stdin)")
        raise SystemExit(selftest(int(sys.argv[2]), sys.argv[3] if len(sys.argv) == 4 else "1"))
    request = json.load(sys.stdin)
    if request["schema_version"] != 1 or request["target_profile"] != "blake3-r2-prefix-v1":
        raise ValueError("unexpected organizer target")
    if request["event"].get("kind") != "digest-xor-mask":
        raise ValueError("unexpected organizer event")
    if request["experiment_id"] != "union-search":
        raise ValueError("unexpected experiment")
    trials = []
    for trial_request in request["trials"]:
        first, second, observations = half_collision(bytes.fromhex(trial_request["seed"]))
        row = {"trial": trial_request["trial"],
               "message_a_hex": None if first is None else first.hex(),
               "message_b_hex": None if second is None else second.hex()}
        if observations:
            row["observations"] = observations
        trials.append(row)
    json.dump({"schema_version": 1, "trials": trials}, sys.stdout, separators=(",", ":"), sort_keys=True)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
