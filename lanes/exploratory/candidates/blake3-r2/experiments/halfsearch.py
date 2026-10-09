#!/usr/bin/env python3
"""halfsearch.py - the search of proof.md 9.1 run on the root instance (one chunk, counter 0, flags 11).

Exact computation on 32-bit words, Python 3 standard library only. No BLAKE3 library is imported.

One organizer trial = one run of the current pipeline on TRIAL_BATCHES batches drawn from the seed:
  step 1   whole-class sampler (9.1), packed step CO compiled from the lines (9.6), exact outer filter of
           Section 8 (automaton (2) on omega in all seven lanes, then automaton (1) on Y9), budgets;
  9.7      s-pattern pre-check: nu from Y9, y, C2.c1, C2.b1; T = X AND VMASK[nu];
  step 2   joint solver of 9.4 with guards (a)-(g) and (G7), on the rows of T;
  step 3   certificate of each root (inverse of Lemma IP, Q*, step CT, t = 0 for this instance, E1, J words,
           chaining values); "certified" needs every test;
  counter  Section 11 ledger: outer charges (batch, E lane, pass) plus the solver's ledger for steps 2 and 3.
The returned pair is built by step CT on the trial's first passing outer step (the trial's first outer step if
none passes), with the one c1 for which the counter word that step CT forces is t = 0. For every outer step and
that c1 the two messages, hashed as the harness hashes them (counter 0, flags 11), agree on digest words 0, 2, 5
and 7: the only differing state words after the first half of round 2 are Y3 and Y11, and the only differing
message word of the diagonal step is w5; none of them enters diagonals 0 and 2.

  python3 halfsearch.py                    organizer request on stdin, response on stdout
  python3 halfsearch.py --selftest N [seed]
  slot32 (either mode, default ON): step 2 by the 32-slot one-success slot of proof.md 9.8, at most one root per
  solver step; --no-slot32 restores the full traversal of 9.4 (the earlier behaviour).
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
RESIDUAL_TRIES = 131072


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
CLASS_SIZE = 1 << len(CLASS_FREE)
Y_PEND = (CLASS_VALUE - Y3) & M

# ---- outcomes, S, Q*, constants and budgets of 9.1 ----------------------------------------------------------------
TAUS = (0x175020A0, 0x185020A0, 0x275020A0, 0x285020A0, 0x385020A0, 0x675020A0, 0x685020A0)
S_MASK = 0x5F
S_TAUS = [t for t in TAUS if t != 0x675020A0]
LOW_TAUS = {0x175020A0, 0x275020A0, 0x675020A0}
VMASK = [0, 0, 0x3F80, 0x3FFF, 0x3FFF, 0x3F80, 0, 0]
QSTAR_MASK, QSTAR_VALUE = 0x0E09818B, 0x02008000
SHARE, E_COUNT, V_COUNT = 18289159183466496, 233715456, 558140844222
FACTOR = 5 * 138512695296 // 7
RUN_STEPS = -(-(12419 << 128) // (25000 * FACTOR * ((1 << 21) - 1)))
E_BUDGET = -(-(17 * RUN_STEPS * E_COUNT) >> 36)
PASS_BUDGET = -(-(17 * RUN_STEPS * SHARE) >> 68)
SOLVER_BUDGET = -(-(17 * RUN_STEPS * V_COUNT) >> 55)
RUN_BATCHES = -(-RUN_STEPS // 7)
TEXT_CONSTANTS = {"FACTOR": 98937639497, "RUN_STEPS": 814694561164316144946, "E_BUDGET": 47103299361697960684,
                  "PASS_BUDGET": 858218304486124116, "SOLVER_BUDGET": 214554576121531029,
                  "RUN_BATCHES": 116384937309188020707}

# ---- Section 11 charges ---------------------------------------------------------------------------------------------
LANES, LANE_BITS = 7, 36
ONES = sum(1 << (LANE_BITS * i) for i in range(LANES))
M_ALL, F_ALL, LIMIT = M * ONES, FREE_MASK * ONES, 1 << LANE_BITS
CHARGED_BATCH, CHARGE_E_LANE, CHARGE_PASS, CHARGE_BATCH_COUNT, CHARGE_DISPATCH = 424, 35, 512, 3, 16
U_STEP, U_FAMILY, U_ROW = 4096, 2304, 1280
U_FORCED, U_SELECTED_EXTRA, U_FREE, U_LEAF, U_ROOT = 20, 4, 48, 80, 288
CAP_G7 = 31456
# Guard nodes pay a forced node plus their own word operations, counted from traverse/fixed_arc:
#   node 25: gv = bit(pref,6) ^ bit(pref,13) ^ u  (2 shifts, 2 ANDs, 2 XORs) and the key (OR 8, shift, OR) = 9;
#   node 29: gv = 1 ^ e29 (1 XOR) and the key (3) = 4; e2[29] = arc AND 1 at position 9: 1 per arc kept there.
U_G25, U_G29, U_E29 = 9, 4, 1
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


def member_word(k):
    'The word W whose free bits are member number k.'
    return sum((k >> n & 1) << i for n, i in enumerate(CLASS_FREE))


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


def build_tables():
    th = [theta_of(t) for t in TAUS]
    t1 = automaton([(ETA, x) for x in th], 0)
    t2 = automaton([(ror(x, 12), EPS) for x in th], DY3)
    return [t1[:3] + [[m & S_MASK for m in t1[3]]], t2[:3] + [[m & S_MASK for m in t2[3]]]]


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
    """Batches b0..b1-1 of step 1; yields (step, eight words, names of step CO, X, mask1) for every pass.
    c receives batches, steps, e_count, passes, outer units (and verify counts)."""
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
        c["outer_units"] += S.batch_units
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
            yield 7 * b + i, eight, v, x, m1


# ---- the joint solver of 9.4, pre-check and (G7) of 9.7 -------------------------------------------------------------
def j1(Q, h, theta):
    return (((Q + h) & M) ^ ((Q + (h ^ ETA)) & M)) == theta


def is_joint_root(Q, y, E, h, tau):
    'The words (J1), (J2), (J3).'
    sigma = tau ^ ror(tau, 1)
    theta = rol(sigma, 12)
    gg = (Q + h) & M
    if (gg ^ ((Q + (h ^ ETA)) & M)) != theta:
        return False
    f = ror(y ^ gg, 12)
    e2 = (E + f) & M
    if (e2 ^ ((((E + DY3) & M) + (f ^ sigma)) & M)) != EPS:
        return False
    h2 = ror(h ^ e2, 8)
    return (((gg + h2) & M) ^ (((gg ^ theta) + (h2 ^ MU)) & M)) == tau


class Row:
    'Static descriptor of an outcome.'

    def __init__(self, tau):
        self.tau = tau
        self.sigma = tau ^ ror(tau, 1)
        self.theta = rol(self.sigma, 12)
        self.gamma = ETA ^ self.theta
        self.D = (self.sigma ^ EPS) & 0x7FFFFFFF
        self.low = tau in LOW_TAUS
        self.family = (self.low, bit(self.gamma, 10))
        self.const_pos = {10, 11, 12, 16, 17, 18, 19, 24, 26}
        self.guard_pos = {25, 29}
        self.select_pos = 20

    def free_positions(self):
        free = []
        for i in range(7, 32):
            k = (i + 20) % 32
            if i in self.const_pos or i in self.guard_pos or i == self.select_pos or i == 7:
                continue
            if i < 31 and bit(self.gamma, i):
                continue
            if k < 31 and bit(self.D, k):
                continue
            free.append(i)
        return free


ROWS = {t: Row(t) for t in TAUS}


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
    'Bit j-1 iff some h has (J1) for outcome j.'
    X_ = 0
    for j, tau in enumerate(TAUS):
        if j1_exists(Q, ROWS[tau].theta):
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
    'Guard (G7): h[7] from h[6], e1, C2.c1 and C2.b1.'
    x = h6 ^ bit(e1, 22)
    a22 = x ^ bit(C, 22) ^ bit(B, 22)
    return bit(e1, 23) ^ 1 ^ bit(C, 23) ^ bit(B, 23) ^ maj(x, bit(C, 22), a22)


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


def traverse(row, Q, y, E, Ep, kappa, e1, h, states, cnt):
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
                cnt["roots"] += 1
                roots.append(pref)
            continue
        cp = (uu << 1) | aa
        if i in free:
            cnt["free"] += 1
            w = DUAL[(keys[i] << 2) | cp]
            arcs = [w & 0x1F, (w >> 5) & 0x1F]
        else:
            arcs = [fixed_arc(i, keys[i], cp, pref, e29, u, cnt)]
        for arc in arcs:
            if arc:
                if i == 9:
                    cnt["e29"] += 1
                stack.append((i + 1, (arc >> 3) & 1, (arc >> 2) & 1, pref | (((arc >> 1) & 1) << i),
                              (arc & 1) if i == 9 else e29))
    return roots


def fixed_arc(i, key, cp, pref, e29, u, cnt):
    'A non-free position: Lemma J0 at 20, the guards at 25 and 29 (charged U_G25, U_G29 extra), else forced.'
    cnt["forced"] += 1
    if i == 20:
        cnt["selected"] += 1
        return SELECTED[(((key << 2) | cp) << 1) | bit(pref, 8)]
    if i == 25:
        cnt["g25"] += 1
        return FORCED[((key | 8 | ((bit(pref, 6) ^ bit(pref, 13) ^ u) << 2)) << 2) | cp]
    if i == 29:
        cnt["g29"] += 1
        return FORCED[((key | 8 | ((1 ^ e29) << 2)) << 2) | cp]
    return FORCED[(key << 2) | cp]


def new_count():
    return dict(forced=0, selected=0, free=0, leaves=0, roots=0, walk=0, g25=0, g29=0, e29=0)


def node_units(cnt, u_free):
    return (U_FORCED * (cnt["forced"] + cnt["walk"]) + U_SELECTED_EXTRA * cnt["selected"] + u_free * cnt["free"]
            + U_G25 * cnt["g25"] + U_G29 * cnt["g29"] + U_E29 * cnt["e29"] + U_LEAF * cnt["leaves"]
            + U_ROOT * cnt["roots"])


def solve(Q, y, E, C, B, rows):
    'The joint solver on the rows of T; units by the ledger of Section 11 (steps 2 and 3).'
    arrays()
    e1 = (Y3 + y) & M
    assert e1 & CLASS_MASK == CLASS_VALUE
    Ep = (E + DY3) & M
    notes, roots = [], []
    cnt = new_count()
    if not rows:
        return dict(roots=[], units=0, counts=cnt, notes=notes)
    units = U_STEP + U_FAMILY * len({ROWS[t].family for t in rows}) + U_ROW * len(rows)
    for t in rows:
        row = ROWS[t]
        kappa = row.sigma ^ EPS ^ E ^ Ep
        res = row_setup(row, Q, y, E, Ep, e1, kappa, C, B, notes, cnt)
        if res is not None:
            roots += [(r, t) for r in traverse(row, Q, y, E, Ep, kappa, e1, res[0], res[1], cnt)]
    units += node_units(cnt, U_FREE)
    return dict(roots=sorted(roots), units=units, counts=cnt, notes=notes)


# ---- option --slot32: the 32-slot repair of BA 1.3 (one row, one leaf path per solver step) -------------------------
SLOT32 = True                                         # default; main() sets False for --no-slot32
ENVELOPES = (((0x175020A0, 8),), ((0x275020A0, 16),), ((0x285020A0, 16), (0x385020A0, 16)),
             ((0x185020A0, 8), (0x385020A0, 16), (0x685020A0, 8)))
assert all(len(ROWS[t].free_positions()) == n.bit_length() - 1 for e in ENVELOPES for t, n in e)
U_SEL, U_FREE_ONE, U_SAVE = 64, U_FORCED + 8, 1      # selection; a free node taking ONE dual arc; raw-word move/batch


def envelope(m1):
    'The first static envelope (in the order of BA 1.3) that contains the J1 mask m1.'
    for env in ENVELOPES:
        if not m1 & ~sum(1 << TAUS.index(t) for t, _ in env):
            return env
    return ()


def selector(raw):
    'J in 0..31 from bits 0, 1, 8, 9, 15 of the raw member word (outside FREE_MASK, unused by the member).'
    return (raw & 3) | (raw >> 6 & 12) | (raw >> 11 & 16)


def solve32(Q, y, E, C, B, rows, m1, raw):
    'Slot J of the envelope of m1 gives one row and its rank; a padded slot or a row not in T fails.'
    arrays()
    e1, Ep, notes, cnt = (Y3 + y) & M, (E + DY3) & M, [], new_count()
    units, J, start, pick, root = U_STEP + U_SEL, selector(raw), 0, None, []
    for t, n in envelope(m1):
        if start <= J < start + n:
            pick = (ROWS[t], J - start)
        start += n
    if pick and pick[0].tau in rows:
        row, rank = pick
        units += U_FAMILY + U_ROW
        kappa = row.sigma ^ EPS ^ E ^ Ep
        res = row_setup(row, Q, y, E, Ep, e1, kappa, C, B, notes, cnt)
        if res is not None:
            h = path32(row, Q, y, E, Ep, kappa, e1, res[0], res[1][0], rank, cnt)
            root = [] if h is None else [(h, row.tau)]
    else:
        pick = None
    units += node_units(cnt, U_FREE_ONE)
    return dict(roots=root, units=units, counts=cnt, notes=notes, row=int(pick is not None))


def path32(row, Q, y, E, Ep, kappa, e1, h, state, rank, cnt):
    'One leaf path of 9.4 from the first state: at the n-th free position the dual arc of rank bit n.'
    u, free = bit(e1, 21), row.free_positions()
    (uu, aa), pref, e29 = state, sum(h[i] << i for i in range(7)), 0
    for i in range(7, 32):
        key = descriptor(row, Q, y, E, Ep, kappa, i, 1, h[i]) if i in h else descriptor(row, Q, y, E, Ep, kappa, i)
        cp = (uu << 1) | aa
        if i in free:
            cnt["free"] += 1
            arc = DUAL[(key << 2) | cp] >> 5 * (rank >> free.index(i) & 1) & 0x1F
        else:
            arc = fixed_arc(i, key, cp, pref, e29, u, cnt)
        if not arc:
            return None
        if i == 9:
            cnt["e29"] += 1
            e29 = arc & 1
        uu, aa, pref = (arc >> 3) & 1, (arc >> 2) & 1, pref | (((arc >> 1) & 1) << i)
    cnt["leaves"] += 1
    if is_joint_root(Q, y, E, pref, row.tau):
        cnt["roots"] += 1
        return pref
    return None


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


def certificate(v, h, tau):
    'Step 3 for one root (h, tau) on the root instance: the first failing test, or "certified" (every test holds).'
    c1 = c1_of(v, h)
    u = step_ct(v, c1)
    ev_ = evaluate(u, u["t"])
    j_match = ev_["j"] == (theta_of(tau), EPS, tau)
    e1_ok = (ev_["ax"], ev_["cx"], ev_["b1x"]) == (tau, EPS, BETA_STAR)
    if c1 & QSTAR_MASK != QSTAR_VALUE:
        return "c1 not in Q*"
    if u["t"] != COUNTER:
        return "t != 0"
    if not ev_["cons"]:
        return "names differ from the compression"
    if not j_match:
        return "J words"
    if not e1_ok:
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
        SEARCH.batch_units += U_SAVE if SLOT32 else 0    # --slot32 keeps the raw member word: 425 per batch
        arrays()
    return SEARCH


def pipeline(v, X_, mask1, c, raw=0):
    'Pre-check of 9.7, step 2 and step 3 on one passing outer step.'
    Q, y, E, e1, C, B = v["Y9"], v["Y4"], v["omega"], v["e1"], v["C2.c1"], v["C2.b1"]
    T =X_ & VMASK[nu_of(Q, e1, C, B)]
    if not T:
        return
    c["solver_steps"] += 1
    if c["solver_steps"] > SOLVER_BUDGET:
        raise Halt("solver count exceeds SOLVER_BUDGET")
    rows = [t for j, t in enumerate(TAUS) if T >> j & 1 and t in S_TAUS]
    if SLOT32:
        r = solve32(Q, y, E, C, B, rows, mask1, raw)
        c["slot_rows"] += r["row"]
    else:
        r = solve(Q, y, E, C, B, rows)
    c["solver_units"] += r["units"]
    c["solver_units_max"] = max(c["solver_units_max"], r["units"])
    c["over_cap"] += r["units"] > CAP_G7
    for h, tau in r["roots"]:
        c["roots"] += 1
        res = certificate(v, h, tau)
        c["certified"] += res == "certified"
        c["roots_t0"] += res not in ("c1 not in Q*", "t != 0")


def run_trial(seed):
    'One organizer trial: TRIAL_BATCHES batches of the pipeline; the outer step of the pair; the counts.'
    S = get_search()
    oc = {}
    c = dict(solver_steps=0, solver_units=0, solver_units_max=0, over_cap=0, roots=0, roots_t0=0, certified=0,
             **({"slot_rows": 0} if SLOT32 else {}))
    first, halted = None, 0
    try:
        for step, eight, v, X_, m1 in iter_passes(seed, 0, TRIAL_BATCHES, S, oc):
            if first is None:
                first = (step, eight, v)
            pipeline(v, X_, m1, c, eight[7])
    except Halt:
        halted = 1
    if first is None:
        eight = [lane(w, 0) for w in draw(seed, 0)]
        first = (-1, eight, scalar_outer(eight))
    # The organizer accepts at most 16 numeric observations per trial: 14 here, 16 with residual-search.
    obs = dict(outer_steps=oc["steps"], passes=oc["passes"], halted=halted, verify_fail=oc["verify_fail"], **c)
    obs["units"] = oc["outer_units"] + c["solver_units"]
    obs["pair_step"] = first[0]
    return first, obs


def half_collision(seed):
    (step, eight, v), obs = run_trial(seed)
    a, b = pair_of(v)
    return a, b, obs


def residual_word1(a, b):
    'Low byte of digest word 1 of A XOR that of B (counter 0, flags 11).'
    return (compress2(a)[1][1] ^ compress2(b)[1][1]) & 0xFF


# Units of the member loop, one per 32-bit word operation (add, subtract, XOR, AND, OR, shift, compare); a
# rotation is 3 (two shifts and an OR); constants and renamings are free. Per try: member_y 3 (AND, OR, SUB),
# the 77 lines of step CO (LINE_OPS, 202), omega 2; c1_t0 33 (w0 5, Y14 6, h 5, c1_of 5+5+7), step_ct 36
# (E1.d1 1, E1.a1 4, Y6 2, Y10 4, Y14 1, E1.b1 4, Y2 4, E3.h1 5, w0 2, K0.a1 2, t 4, w1 2, w5 of B 1) and the
# t = 0 test 1; two 2-round compressions of 16 G calls (6 adds, 4 XORs, 4 rotations = 22) and 8 output XORs
# (360 each); the residual test 3 (XOR, AND, test) and the loop 2 (increment, compare). The next member costs 3
# (OR CLASS_MASK, add 1, AND FREE_MASK) from the second try on; the first costs 1 (raw word AND FREE_MASK).
def line_ops(e):
    if isinstance(e, (int, str)):
        return 0
    if e[0] == "sum":
        return len(e[1]) - 1 + sum(line_ops(t[1] if isinstance(t, tuple) and t[0] == "neg" else t) for t in e[1])
    return (1 if e[0] == "xor" else 3) + sum(line_ops(x) for x in e[1:] if not isinstance(x, int))


LINE_OPS = sum(line_ops(e) for _, e in LINES)
U_COMP = 16 * (6 + 4 + 4 * 3) + 8
U_TRY = 3 + LINE_OPS + 2 + 33 + 36 + 1 + 2 * U_COMP + 3 + 2


# The loop below is the same computation, arranged for speed: within a trial only the member word changes, so
# the lines of step CO that do not read Y4, the round-1 column step and the round-1 diagonal G calls on words
# 12-15 (no word of them depends on the member once step CT gives t = 0) are computed once per trial, and the rest
# is inlined. units are not counted inside the loop: member_units is tries times the charge above, which counts
# every operation of a try as if nothing were shared, so it is not less than what the loop executes.
def r1_fixed(m, n):
    'State after the round-1 column step and the round-1 diagonal G calls on words 12-15 (counter 0, flags 11).'
    v = list(IV) + list(IV[:4]) + [COUNTER & M, COUNTER >> 32, n, FLAGS]
    for i in (0, 1, 2, 3, 6, 7):
        a, b, c, d = GCALLS[i]
        v[a], v[b], v[c], v[d] = g(v[a], v[b], v[c], v[d], m[2 * i], m[2 * i + 1])
    return v


def word1(v, m, x8, x9, x10, x11):
    'Digest word 1 of the 2-round compression from r1_fixed state v, message m and its words 8 to 11.'
    v0, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15 = v
    m0, m2, m3, m4, m5, m6, m7, m12, m13, m15 = m
    # round 1, G(0,5,10,15) with w8, w9 and G(1,6,11,12) with w10, w11
    v0 = (v0 + v5 + x8) & M; v15 ^= v0; v15 = (v15 >> 16 | v15 << 16) & M; v10 = (v10 + v15) & M
    v5 ^= v10; v5 = (v5 >> 12 | v5 << 20) & M; v0 = (v0 + v5 + x9) & M; v15 ^= v0; v15 = (v15 >> 8 | v15 << 24) & M
    v10 = (v10 + v15) & M; v5 ^= v10; v5 = (v5 >> 7 | v5 << 25) & M
    v1 = (v1 + v6 + x10) & M; v12 ^= v1; v12 = (v12 >> 16 | v12 << 16) & M; v11 = (v11 + v12) & M
    v6 ^= v11; v6 = (v6 >> 12 | v6 << 20) & M; v1 = (v1 + v6 + x11) & M; v12 ^= v1; v12 = (v12 >> 8 | v12 << 24) & M
    v11 = (v11 + v12) & M; v6 ^= v11; v6 = (v6 >> 7 | v6 << 25) & M
    # round 2 columns: (0,4,8,12) w2, w6; (1,5,9,13) w3, w10; (2,6,10,14) w7, w0; (3,7,11,15) w4, w13
    v0 = (v0 + v4 + m2) & M; v12 ^= v0; v12 = (v12 >> 16 | v12 << 16) & M; v8 = (v8 + v12) & M
    v4 ^= v8; v4 = (v4 >> 12 | v4 << 20) & M; v0 = (v0 + v4 + m6) & M; v12 ^= v0; v12 = (v12 >> 8 | v12 << 24) & M
    v8 = (v8 + v12) & M; v4 ^= v8; v4 = (v4 >> 7 | v4 << 25) & M
    v1 = (v1 + v5 + m3) & M; v13 ^= v1; v13 = (v13 >> 16 | v13 << 16) & M; v9 = (v9 + v13) & M
    v5 ^= v9; v5 = (v5 >> 12 | v5 << 20) & M; v1 = (v1 + v5 + x10) & M; v13 ^= v1; v13 = (v13 >> 8 | v13 << 24) & M
    v9 = (v9 + v13) & M; v5 ^= v9; v5 = (v5 >> 7 | v5 << 25) & M
    v2 = (v2 + v6 + m7) & M; v14 ^= v2; v14 = (v14 >> 16 | v14 << 16) & M; v10 = (v10 + v14) & M
    v6 ^= v10; v6 = (v6 >> 12 | v6 << 20) & M; v2 = (v2 + v6 + m0) & M; v14 ^= v2; v14 = (v14 >> 8 | v14 << 24) & M
    v10 = (v10 + v14) & M; v6 ^= v10; v6 = (v6 >> 7 | v6 << 25) & M
    v3 = (v3 + v7 + m4) & M; v15 ^= v3; v15 = (v15 >> 16 | v15 << 16) & M; v11 = (v11 + v15) & M
    v7 ^= v11; v7 = (v7 >> 12 | v7 << 20) & M; v3 = (v3 + v7 + m13) & M; v15 ^= v3; v15 = (v15 >> 8 | v15 << 24) & M
    v11 = (v11 + v15) & M; v7 ^= v11; v7 = (v7 >> 7 | v7 << 25) & M
    # round 2 diagonals: a of (1,6,11,12) with w12, w5 and c of (3,4,9,14) with w15, w8; word 1 = v1 XOR v9
    v1 = (v1 + v6 + m12) & M; v12 ^= v1; v12 = (v12 >> 16 | v12 << 16) & M; v11 = (v11 + v12) & M
    v6 ^= v11; v6 = (v6 >> 12 | v6 << 20) & M; v1 = (v1 + v6 + m5) & M
    v3 = (v3 + v4 + m15) & M; v14 ^= v3; v14 = (v14 >> 16 | v14 << 16) & M; v9 = (v9 + v14) & M
    v4 ^= v9; v4 = (v4 >> 12 | v4 << 20) & M; v3 = (v3 + v4 + x8) & M; v14 ^= v3; v14 = (v14 >> 8 | v14 << 24) & M
    return v1 ^ ((v9 + v14) & M)


def residual_search(seed):
    'The members of the class in order from the member of the pair step, at most RESIDUAL_TRIES of them.'
    (step, eight, v), obs = run_trial(seed)
    w, a = eight[7] & FREE_MASK, None
    c = scalar_outer(eight[:7] + [w])                    # its lines that do not read Y4 hold for every member
    C0b, C0c, C0d, w6, X4, w2, S10, S5, S15, S0, S11, S6, S12, S1, w3, X13, X9, X2, w7, X14, w12, K0b, w5 = (
        c[k] for k in ("C0.b1", "C0.c1", "C0.d1", "w6", "X4", "w2", "S10", "S5", "S15", "S0", "S11", "S6", "S12",
                       "S1", "w3", "X13", "X9", "X2", "w7", "X14", "w12", "K0.b1", "w5"))
    RX15, RC0d, RK0d = rol(X15, 8), rol(C0d, 16), rol(c["K0.d1"], 16)
    W0 = (RK0d - IV[0] - IV[4]) & M                      # c1_t0; with t = 0 step CT gives w0 = W0 and w1 = W1
    W1 = (S0 - RK0d - K0b) & M
    ma = (W0, W1, w2, w3, W4, w5, w6, w7, 0, 0, 0, 0, w12, W13, 0, 0)
    mb = ma[:4] + (W4B, (w5 + DELTA5) & M) + ma[6:]
    pa, pb = r1_fixed(ma, LEN_A), r1_fixed(mb, LEN_B)
    qa, qb = [tuple(m[j] for j in (0, 2, 3, 4, 5, 6, 7, 12, 13, 15)) for m in (ma, mb)]
    for i in range(RESIDUAL_TRIES):
        if i:
            w = ((w | CLASS_MASK) + 1) & FREE_MASK           # member number + 1 (mod 2^19), in the free bits
        y = ((CLASS_VALUE | w) - Y3) & M
        # step CO, the lines that read Y4
        y8 = ((y << 7 | y >> 25) & M) ^ C0b; y12 = (y8 - C0c) & M; y0 = ((y12 << 8 | y12 >> 24) & M) ^ C0d
        c0a = (y0 - C0b - w6) & M; x0 = (c0a - X4 - w2) & M; d0d = RX15 ^ x0; d0c = (S10 + d0d) & M
        t = S5 ^ d0c; d0b = (t >> 12 | t << 20) & M; x10 = (d0c + X15) & M; t = d0b ^ x10; x5 = (t >> 7 | t << 25) & M
        x12 = RC0d ^ c0a; d1c = (X11 - x12) & M; d1d = (d1c - S11) & M; x1 = ((x12 << 8 | x12 >> 24) & M) ^ d1d
        t = S6 ^ d1c; d1b = (t >> 12 | t << 20) & M; c1a = (x1 + x5 + w3) & M; t = d1b ^ X11; x6 = (t >> 7 | t << 25) & M
        t = X13 ^ c1a; c1d = (t >> 16 | t << 16) & M; d1a = ((d1d << 16 | d1d >> 16) & M) ^ S12; c1c = (X9 + c1d) & M
        c2a = (X2 + x6 + w7) & M; w10 = (d1a - S1 - S6) & M; t = x5 ^ c1c; c1b = (t >> 12 | t << 20) & M
        t = X14 ^ c2a; c2d = (t >> 16 | t << 16) & M; y1 = (c1a + c1b + w10) & M; c2c = (x10 + c2d) & M
        t = x6 ^ c2c; c2b = (t >> 12 | t << 20) & M; d0a = ((d0d << 16 | d0d >> 16) & M) ^ S15
        w8 = (d0a - S0 - S5) & M; w9 = (x0 - d0a - d0b) & M; w11 = (x1 - d1a - d1b) & M
        # c1_t0 (inverse of Lemma IP) and step CT; t = 0 fixes w0 = W0 and w1 = W1
        e = (Y3 + y) & M; t = ((W0 + c2a + c2b) & M) ^ c2d; y14 = (t >> 8 | t << 24) & M
        t = y14 ^ e; h = (t >> 16 | t << 16) & M; t = ((((h << 16 | h >> 16) & M) ^ e) + c2c) & M ^ c2b
        y6 = (t >> 7 | t << 25) & M; t = ((y6 + y1 + w12) & M) ^ y12; c1 = (Y11 + ((t >> 16 | t << 16) & M)) & M
        t = (c1 - Y11) & M; t = ((t << 16 | t >> 16) & M) ^ y12; t = (t - y1 - w12) & M
        t = ((t << 7 | t >> 25) & M) ^ c2b; t = (t - c2c) & M; t = ((t << 8 | t >> 24) & M) ^ c2d
        t = RK0d ^ ((IV[0] + IV[4] + ((t - c2a - c2b) & M)) & M)
        assert t == COUNTER
        if (word1(pa, qa, w8, w9, w10, w11) ^ word1(pb, qb, w8, w9, w10, w11)) & 0xFF == 0:
            a, b = pair_of(scalar_outer(eight[:7] + [w]))    # the pair as half-collision builds it
            assert residual_word1(a, b) == 0
            break
    tries = i + 1
    if a is None:
        b = None
    mu = 1 + 3 * (tries - 1) + U_TRY * tries
    return a, b, dict(obs, tries=tries, member_units=mu, units=obs["units"] + mu)


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


def selftest(cases, seed):
    rnd = hashlib.shake_256(b"halfsearch selftest" + seed.encode()).digest(64 * cases + 64)
    words = list(struct.unpack("<%dI" % (16 * cases + 16), rnd))
    rep = {}
    rep["constants"] = all(globals()[k] == x for k, x in TEXT_CONSTANTS.items())
    # automata against brute force at width 8: the real targets truncated
    th = [theta_of(t) for t in TAUS]
    tq, te = [(ETA & 255, x & 255) for x in th], [(ror(x, 12) & 255, EPS & 255) for x in th]
    a1, a2 = automaton(tq, 0, 8), automaton(te, DY3 & 255, 8)
    bf = sum(look_n(a1, x, 8) == brute_masks(8, tq, 0, x) and look_n(a2, x, 8) == brute_masks(8, te, DY3, x)
             for x in range(256))
    rep["automata_bruteforce_width8"] = "%d of 256" % bf
    S = Search(check_bounds=True)
    n1, n2 = pattern_counts(S.t1), pattern_counts(S.t2)
    share = sum(c1 * c2 for p, c1 in n1.items() for q, c2 in n2.items() if p & q & S_MASK)
    ecount = sum(c2 for q, c2 in n2.items() if q & S_MASK)
    rep["SHARE_E_COUNT_from_tables"] = share == SHARE and ecount == E_COUNT
    rep["slot32_envelope_per_J1_mask"] = all(envelope(p) for p in n1 if p)
    oc = {}
    sb = seed.encode()
    npass = len(list(iter_passes(sb, 0, max(1, cases * 64 // 7), S, oc, verify=True)))
    rep["packed_vs_scalar"] = dict(lanes=oc["verified_lanes"], fail=oc["verify_fail"], bound_fail=oc["bound_fail"],
                                   passes=npass, max_lane_bound_bits=S.maxbound.bit_length())
    rep["batch_units"] = S.batch_units
    mx = cons = inv = jid = t0 = half = 0
    arrays()
    for n in range(cases):
        wd = words[16 * n:16 * n + 16]
        mx += mask_X(wd[8]) & S_MASK == look(S.t1, wd[8])
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
    rep["maskX_vs_automaton_1"] = "%d of %d" % (mx, cases)
    rep["step_CT_consistent"] = "%d of %d" % (cons, cases)
    rep["inverse_IP"] = "%d of %d" % (inv, cases)
    rep["J_words_equal_E3"] = "%d of %d" % (jid, cases)
    rep["t0_c1_consistent"] = "%d of %d" % (t0, cases)
    rep["half_collision_counter0_flags11"] = "%d of %d" % (half, cases)
    rep["seed"] = seed
    json.dump(rep, sys.stdout, separators=(",", ":"))
    sys.stdout.write("\n")
    good = (rep["constants"] and bf == 256 and rep["SHARE_E_COUNT_from_tables"] and oc["verify_fail"] == 0
            and rep["slot32_envelope_per_J1_mask"]
            and oc["bound_fail"] == 0 and S.batch_units == CHARGED_BATCH
            and mx == cons == inv == jid == t0 == half == cases)
    return 0 if good else 1


def main():
    global SLOT32
    argv = [a for a in sys.argv if a not in ("--slot32", "--no-slot32")]
    SLOT32 = "--no-slot32" not in sys.argv
    if len(argv) > 1:
        modes = {"--selftest": selftest}
        if argv[1] not in modes or len(argv) not in (3, 4) or not argv[2].isdecimal() or int(argv[2]) < 1:
            raise SystemExit("usage: halfsearch.py [--no-slot32] [--selftest N [seed]]   (else: organizer request on stdin)")
        raise SystemExit(modes[argv[1]](int(argv[2]), argv[3] if len(argv) == 4 else "1"))
    request = json.load(sys.stdin)
    if request["schema_version"] != 1 or request["target_profile"] != "blake3-r2-prefix-v1":
        raise ValueError("unexpected organizer target")
    if request["event"].get("kind") != "digest-xor-mask":
        raise ValueError("unexpected organizer event")
    run = {"half-collision": half_collision, "residual-search": residual_search}[request["experiment_id"]]
    trials = []
    for trial_request in request["trials"]:
        first, second, observations = run(bytes.fromhex(trial_request["seed"]))
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
