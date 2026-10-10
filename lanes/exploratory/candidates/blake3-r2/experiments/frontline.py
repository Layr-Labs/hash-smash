"""frontline.py - the counter search of proof.md 9.1 and 9.8 in the layout of 9.8 and 9.9, executed, with the batch
cache of the packed Y9 (9.8), the work register W of the four budgets (9.1) and the work meter of the credit (9.7).

Exact 32-bit arithmetic, Python 3 standard library only, no BLAKE3 library. Instance: the last chunk of the 55/63-byte
pair on a non-root chunk, flags 3, counter t solved by step CT. One organizer trial = one context of a run (seven
fresh outer words from the seed) walked by the clustered member loop: representative batches 0..TRIAL_REPS-2 and the
context's last (four-lane) representative batch, with the partners of every opened cluster.
  step 0  automata of (1) and (2) restricted to S; every entry read of T2' (word 0), T1 (word 2^34) and the folded
          gate table (word 2^35) is computed on demand by the rule that fills it; VMASK, CT, transition arrays tabled.
  step 1  context: the W test against WB, the 39 lines of Lemma Y once, sixteen packed operands (X9 + 2^34 for the
          Y9 path), the gate base; clusters of 32 members (e1 bits 10..14); a representative batch: omega side,
          packed gate key, gate test per lane; a closed gate skips its cluster (no T2); an opened one adds its units
          to W, then the representative's test (2) and paths and five partner batches. Test (2); E lane: W add; at
          the batch's first E lane the packed Y9 path, cached for the batch; Y9 from the cache, T1, X; passing lane:
          W add, C2.c1 and C2.b1 from the batch words, the pre-check of 9.7, preflight of CM(T) against the credit.
  step 2  scalar rebuild into the source bank (CD 11.2); joint solver of 9.4 with (G7) and the G15 guard; the meter
          debits A(T) and, per executed block, its unit cost.
  step 3  the exact 120-unit root predicate (CF 6.5), in traversal order; for the first certified root the pair is
          formed by step CT and both last-chunk compressions (counter t, flags 3) are compared on 256 bits.
In-run reference (counted in checks / mismatches): every member of every walked cluster recomputed straight-line (all
77 lines of step CO, no partition, no packing) and its omega mod 512 tested against the exact two prefixes of CI 1.2;
every member of a closed cluster tested bit-serially for (2) (a pass is a skipped_pass); every folded gate entry
against the gate of 9.9; T2 entries against a bit-serial decision of (2), T1 entries against one of (1); cross-lane
carries and table ranges; every cached Y9 against a fresh packed Y9 path; every passing lane's C2.c1, C2.b1 and
pre-check against a scalar rebuild; every metered debit against the solver ledger U (debit = U <= CM(T)); every
solver call repeated by the old traversal (9.4 with (G7), no G15) whose roots are certified by real compressions;
step CT charts; on every E lane the step-CT message compressed; every 8th trial a joint root planted from J1-J3.
The returned pair is the root-instance pair (counter 0, flags 11, the c1 that forces t = 0) of the trial's context
and first passing member, from the same lines; the organizer checks its 128-bit half-collision.
  python3 frontline.py              organizer request on stdin, response on stdout
  python3 frontline.py --selftest   constants, automata, mask equivalence, S7 and partition, halt and gate drills
"""
import hashlib
import json
import struct
import sys
from math import isqrt

M = 0xFFFFFFFF
IV = (0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A, 0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19)
K = (IV[2] + IV[6]) & M
LEN_A, LEN_B = 55, 63
X3, X7, X11, X15 = 0x29D4FA98, 0xBEE3AF28, 0x44036000, 0x40C58500
W4, W13 = 0x97475638, 0x0007C006
W4B = (((W4 + K) & M) ^ LEN_A ^ LEN_B) - K & M
DELTA5 = (W4 - W4B) & M
ETA, EPS, MU, BETA = 0x830303CF, 0x6E21BE55, 0x9AED22BD, 0x18B0E098
FLAGS, ROOT_FLAGS = 3, 11                    # the searched instance (CHUNK_START | CHUNK_END); the harness's (| ROOT)
PERM = (2, 6, 3, 10, 7, 0, 4, 13, 1, 11, 12, 5, 9, 14, 15, 8)
GCALLS = ((0, 4, 8, 12), (1, 5, 9, 13), (2, 6, 10, 14), (3, 7, 11, 15),
          (0, 5, 10, 15), (1, 6, 11, 12), (2, 7, 8, 13), (3, 4, 9, 14))
REP_BATCHES, TRIAL_REPS = 2341, 5             # 16384 representatives in 7-lane batches; a trial: 0..3 and the last
T2_EVERY = 1                                # bit-serial check of the T2 entry: every E lane and every k-th member


def ror(v, n):
    n &= 31
    return ((v >> n) | (v << (32 - n))) & M if n else v


def rol(v, n):
    return ror(v, 32 - (n & 31))


def bit(x, i):
    return x >> i & 1


def maj(a, b, c):
    return (a & b) | (a & c) | (b & c)


def g(a, b, c, d, x, y):
    a = (a + b + x) & M; d = ror(d ^ a, 16); c = (c + d) & M; b = ror(b ^ c, 12)
    a = (a + b + y) & M; d = ror(d ^ a, 8); c = (c + d) & M; b = ror(b ^ c, 7)
    return a, b, c, d


Y3, Y7, Y11, Y15 = g(X3, X7, X11, X15, W4, W13)
Y3B, Y7B, Y11B, Y15B = g(X3, X7, X11, X15, W4B, W13)
DY3, DY11 = (Y3B - Y3) & M, (Y11B - Y11) & M
K2A = (K + W4) & M
K2D = ror(K2A ^ LEN_A, 16)
K2C = (IV[2] + K2D) & M
K2B = ror(IV[6] ^ K2C, 12)
assert (Y7, Y15) == (Y7B, Y15B) and (Y3, DY3, Y11, DY11) == (0x8127C181, 0xFDB77CFD, 0x7AF77F38, 0x0A08818B)
assert DELTA5 == (-8) & M and ror(ETA ^ EPS, 8) == MU

CLASS_MASK, CLASS_VALUE, FREE_MASK = 0x03CF8303, 0x030C0303, 0xFC307CFC
CLASS_FREE = [i for i in range(32) if FREE_MASK >> i & 1]
SPL = [sum((k >> n & 1) << i for n, i in enumerate(CLASS_FREE)) for k in range(1024)]
SPH = [sum((k >> n & 1) << CLASS_FREE[n + 10] for n in range(9)) for k in range(512)]


def member(k):
    e1 = CLASS_VALUE | SPL[k & 1023] | SPH[k >> 10]
    return e1, (e1 - Y3) & M


def cmember(g, j):
    k = g & 63 | j << 6 | g >> 6 << 11
    return member(k) + (k,)


TAUS = (0x175020A0, 0x185020A0, 0x275020A0, 0x285020A0, 0x385020A0, 0x675020A0, 0x685020A0)
S_MASK = 0x5F
LOW_TAUS = {0x175020A0, 0x275020A0, 0x675020A0}
VMASK = [0, 0, 0x3F80, 0x3FFF, 0x3FFF, 0x3F80, 0, 0]
QSTAR_MASK, QSTAR_VALUE = 0x0E09818B, 0x02008000
SHARE, E_COUNT, ONCE = 18289159183466496, 233715456, 1128735095914536
U_M = 92113900425963                         # the mean of the solver ledger U per outer step in model M: U_M / 2^46
FACTOR = 10 * 138512695296 // 11            # H1' (i): ten elevenths
RUN_CONTEXTS = -(-(-(-(24797 << 128) // (50000 * FACTOR * ((1 << 21) - 1)))) >> 19)
RUN_STEPS = RUN_CONTEXTS << 19
_S = isqrt(10 * RUN_CONTEXTS - 1) + 1        # s = ceil(sqrt(10K)): reserves 2^19 s (E, pass), 16384 s (opened), 84261 s (G)
E_BUDGET = -(-(1000026 * RUN_STEPS * E_COUNT) // (10 ** 6 << 32)) + (_S << 19)        # H4': 1.000026 p_E
PASS_BUDGET = -(-(1000176 * RUN_STEPS * SHARE) // (10 ** 6 << 64)) + (_S << 19)       # H4': 1.000176 pi
_MC, _LC = -(-(101 * RUN_STEPS * U_M) // (100 << 46)), 17504 << 19   # H5_exec: m at 1.01 U_M (V = U); L
CREDIT = _MC + isqrt(40 * _LC * _MC - 1) + 1 + 14 * _LC + 17504   # B and the preflight reserve 17,504 = max CM(T)
A_BUDGET = -(-962570401 * RUN_CONTEXTS >> 17) + 16384 * _S        # opening budget; p <= 962570401 / 2^31 (Lemma OR)
G_BUDGET = 12466 * RUN_CONTEXTS + 84261 * _S                       # H_G_cluster: 12,466 fills per context
S_OLD = 5486510246044225536
U_CONTEXT, U_REP, U_REP_TAIL, U_E, U_FILL, U_PASS = 600, 61, 47, 7, 54, 61
U_PART, U_PART_TAIL, U_NEST, U_REP_T2 = 52, 33, 21, 5
U_OPEN = 4 * U_PART + U_PART_TAIL + U_NEST + U_REP_T2
U_EG = U_E + U_FILL                                # the one W addition of a batch's first E lane
WB = U_OPEN * A_BUDGET + U_E * E_BUDGET + U_FILL * G_BUDGET + U_PASS * PASS_BUDGET
W_CTX = U_OPEN * 16384 + U_E * (1 << 19) + U_FILL * 84261 + U_PASS * (1 << 19)   # the most one context adds to W
N = ((U_REP * (REP_BATCHES - 1) + U_REP_TAIL) * RUN_CONTEXTS + U_CONTEXT * (RUN_CONTEXTS + 1) + WB + W_CTX + CREDIT
     + ONCE + S_OLD + 430 * 2 ** 38)
assert U_OPEN == 267 and U_REP * 2340 + U_REP_TAIL == 142787
TEXT = dict(RUN_CONTEXTS=1218911201562375, E_BUDGET=34776155800492855966, PASS_BUDGET=633770615067648623,
            CREDIT=844924266982639699337, A_BUDGET=8951477670003828575, G_BUDGET=15194956341454300182,
            N=4517853323071879663378)
U_GLOBAL, U_FAMILY, U_ROW, U_FORCED, U_SELECTED, U_G15, U_FREE, U_LEAF, U_ROOT = 1024, 2304, 1408, 20, 4, 64, 48, 80, 120



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
    ("K3.a1", Sum((IV[3] + IV[7]) & M, "w6")), ("K3.d1", R(X("K3.a1", "fl"), 16)), ("K3.c1", Sum(IV[3], "K3.d1")),
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
DEF = dict(LINES)
OUTER_WORDS = ("C0.d1", "D2.a1", "D2.b1", "S11", "S4", "X9", "w6")


def deps(e, out):
    if isinstance(e, str):
        out.add(e)
    elif isinstance(e, tuple):
        for t in (e[1] if e[0] == "sum" else e[1:2] if e[0] in ("neg", "ror") else e[1:]):
            deps(t, out)
    return out


def closure(names):
    need, st = set(), list(names)
    while st:
        n = st.pop()
        if n in DEF and n not in need:
            need.add(n)
            st += deps(DEF[n], set())
    return need


NEEDED, MARKED = closure(["Y9", "w8"]), set()
for _n, _e in LINES:
    if deps(_e, set()) & (MARKED | {"Y4"}):
        MARKED.add(_n)
MEMBER_LINES = [n for n, _ in LINES if n in NEEDED and n in MARKED]
CONTEXT_LINES = [n for n, _ in LINES if n in NEEDED and n not in MARKED]
OMEGA_SIDE = [n for n in MEMBER_LINES if n in closure(["w8"])]
Y9_PATH = [n for n in MEMBER_LINES if n not in OMEGA_SIDE]
assert len(NEEDED) == 64 and MEMBER_LINES == ("Y8 Y12 Y0 C0.a1 X0 D0.d1 D0.c1 D0.b1 X10 X5 X12 D1.c1 D1.d1 X1 C1.a1 "
                                              "C1.d1 D1.a1 C1.c1 w10 C1.b1 Y1 Y13 Y9 D0.a1 w8").split()
assert CONTEXT_LINES == ("X2 X8 C0.c1 K3.a1 K3.d1 K3.c1 S15 S3 K3.b1 D3.a1 S7 D3.b1 D2.c1 D3.c1 X4 X13 X14 C0.b1 "
                         "D2.d1 D3.d1 S13 S9 K1.c1 K1.d1 K1.a1 w2 S14 K1.b1 S10 S5 S1 w3 S8 K0.b1 S6 K0.c1 S12 "
                         "K0.d1 S0").split()
assert OMEGA_SIDE == "Y8 Y12 Y0 C0.a1 X0 D0.d1 D0.a1 w8".split() and set(Y9_PATH) <= closure(["Y9"])
assert {"C0.a1", "D0.d1"} == {d for n in Y9_PATH for d in deps(DEF[n], set())} & set(OMEGA_SIDE)


def nm(s):
    return s.replace(".", "_")


def src(e, tmp):
    if isinstance(e, int):
        return str(e)
    if isinstance(e, str):
        return nm(e)
    if e[0] == "sum":
        return "((%s) & M)" % " ".join("- " + src(t[1], tmp) if type(t) is tuple and t[0] == "neg" else
                                       "+ " + src(t, tmp) for t in e[1])
    if e[0] == "xor":
        return "(%s ^ %s)" % (src(e[1], tmp), src(e[2], tmp))
    tmp.append(1)
    t = "_t%d" % len(tmp)
    return "((((%s := %s) >> %d) | (%s << %d)) & M)" % (t, src(e[1], tmp), e[2], t, 32 - e[2])


def compile_lines(name, args, lines, ret):
    tmp = []
    body = "\n    ".join("%s = %s" % (nm(n), src(DEF[n], tmp)) for n in lines)
    ns = {"M": M}
    exec("def %s(%s):\n    %s\n    return %s\n" % (name, ", ".join(args), body, ret), ns)
    return ns[name]


ARGS = [nm(n) for n in OUTER_WORDS]
co_full = compile_lines("co_full", ARGS + ["Y4", "fl"], [n for n, _ in LINES], "locals()")      # step CO, scalar
co_ref = compile_lines("co_ref", ARGS + ["Y4", "fl"], [n for n, _ in LINES], "(%d + Y4 + w8) & M, Y9" % Y3)
co_ctx = compile_lines("co_ctx", ARGS + ["fl"], CONTEXT_LINES, "locals()")                      # the 39 lines


def rebuild(ow, y, e1, fl=FLAGS):
    v = co_full(*ow, y, fl)
    v["e1"], v["omega"] = e1, (Y3 + y + v["w8"]) & M
    return v


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


def flat(tables):
    bases, f = [], []
    for t in tables:
        bases.append(len(f))
        f += t
    for p in range(3):
        for i in range(bases[p], bases[p] + len(tables[p])):
            f[i] += bases[p + 1]
    return f


THETAS = [theta_of(t) for t in TAUS]
SIGMAS = [t ^ ror(t, 1) for t in TAUS]
AUT1 = automaton([(ETA, x) for x in THETAS], 0)
AUT2 = automaton([(ror(x, 12), EPS) for x in THETAS], DY3)
AUT1[3], AUT2[3] = [m & S_MASK for m in AUT1[3]], [m & S_MASK for m in AUT2[3]]
F1, F2 = flat(AUT1), flat(AUT2)


def T1(x):
    f = F1
    return f[f[f[f[x & 255] + (x >> 8 & 255)] + (x >> 16 & 255)] + (x >> 24)]


def T2(x):
    f = F2
    return f[f[f[f[x & 255] + (x >> 8 & 255)] + (x >> 16 & 255)] + (x >> 24)]


def T1P(x):
    return T1(x - B34)


def T2P(x):
    return T2(x & M)


def cond1(x, theta):
    gamma = ETA ^ theta
    if gamma & 1:
        return 0
    st = {0}
    for i in range(32):
        q, e_, gi = bit(x, i), bit(ETA, i), bit(gamma, i)
        st = {maj(q, v, u) for u in st for v in (0, 1)
              if i == 31 or maj(q, v ^ e_, u ^ gi) == maj(q, v, u) ^ bit(gamma, i + 1)}
        if not st:
            return 0
    return 1


TR2 = [0] * 256                              # carry-pair sets of condition (2): (xi, ti, si, parity, set) -> set
for _k in range(256):
    for _a in range(4):
        if _k >> _a & 1 and (_a >> 1) ^ (_a & 1) == _k >> 7:
            for _f in (0, 1):
                TR2[_k] |= 1 << 2 * maj(_k >> 4 & 1, _f, _a >> 1) + maj(_k >> 5 & 1, _f ^ (_k >> 6 & 1), _a & 1)


def group_table(nb):
    tab = [0] * (16 << 4 * nb)
    for st in range(16):
        for inp in range(1 << 4 * nb):
            s = st
            for k in range(nb):
                s = TR2[s | (inp >> k & 1) << 4 | (inp >> nb + k & 1) << 5 | (inp >> 2 * nb + k & 1) << 6
                        | (inp >> 3 * nb + k & 1) << 7]
            tab[st | inp << 4] = s
    return tab


G3, G2 = group_table(3), group_table(2)      # bits 0..29 in ten groups of three, bits 30 and 31
SIG3 = [(j, [(SIGMAS[j] >> i & 7) * 0x240 for i in range(0, 30, 3)], (SIGMAS[j] >> 30) * 0x50)
        for j in range(7) if S_MASK >> j & 1]


def mask1_ref(x):
    return sum(cond1(x, THETAS[j]) << j for j in range(7) if S_MASK >> j & 1)


def mask2_ref(x):
    xd = (x + DY3) & M
    r0 = EPS ^ x ^ xd                        # the parity of the two witness carries is r0 XOR sigma, bit by bit
    base = [(x >> i & 7) | (xd >> i & 7) << 3 | (r0 >> i & 7) << 9 for i in range(0, 30, 3)]
    tail, m = x >> 30 | (xd >> 30) << 2 | (r0 >> 30) << 6, 0
    for j, sg, st2 in SIG3:
        st = 1
        for bg, sx in zip(base, sg):
            st = G3[st | (bg ^ sx) << 4]
            if not st:
                break
        else:
            m |= (G2[st | (tail ^ st2) << 4] > 0) << j
    return m


S7 = sum(1 << w for w in range(128) if any(((v + f) ^ ((v + DY3) + (f ^ s))) & 511 == EPS & 511 for v in
                                           range(w, 512, 128) for s in {SIGMAS[j] & 511 for j, _, _ in SIG3}
                                           for f in range(512)))
assert S7 == (1 << 0x3F) - (1 << 0x25) + (1 << 0x5F) - (1 << 0x45)                 # [25, 3e] and [45, 5e] (CI 1.3)


def gate(i):
    a, c, q = i & 127, i >> 7 & 127, i >> 14
    return S7 >> ((a ^ q) + c & 127) & 1 | S7 >> (((a - 1 & 127) ^ q) + c & 127) & 1


B34, PB, L36 = 1 << 34, 1 << 35, (1 << 36) - 1         # T1 at word 2^34, the folded gate table at 2^35 (9.9)


def gtab(x):
    return gate(((x >> 7) + (x >> 14) & 127) | ((x + (x >> 21)) & 127) << 7 | (x >> 28 & 127) << 14)


def prefixes(cw, y, e1):
    b, c, d, A, L, SS = cw
    r = rol(y, 7) ^ b
    H = (r >> 24) - (c >> 24) & 255
    p = rol(r - c & M, 8) ^ d
    u = (p >> 16) - (A >> 16)
    return {e1 - SS + ((u - (256 * (p >> 8 & 255) + (h ^ d & 255) < (A & 65535)) & 511) ^ L) & 511 for h in (H, H - 1 & 255)}


LANES, LB = 7, 36
ONES = sum(1 << LB * i for i in range(LANES))
M_ALL = M * ONES
BOUND = sum(1 << LB * i for i in range(1, LANES + 1))      # a carry into one of these bits leaves its lane
LO = [((1 << 32 - r) - 1) * ONES for r in range(33)]
HI = [(M ^ ((1 << 32 - r) - 1)) * ONES for r in range(33)]
RX15, PX15, R7 = rol(X15, 8) * ONES, X15 * ONES, 127 * ONES
R7H, QM, X11P = R7 << 7, B34 | M, X11 + 1             # immediates: the key mask, the T1 address mask, X11 + 1


def pror(x, r):
    return x >> r & LO[r] | x << 32 - r & HI[r]


def operands(cx):
    n = lambda w: -w & M
    w = (cx["C0_b1"], n(cx["C0_c1"]), cx["C0_d1"], n(cx["C0_b1"] + cx["w6"]), rol(cx["C0_d1"], 16),
         (X11 + 1 - cx["S11"]) & M, cx["S12"], n(cx["X4"] + cx["w2"]), n(cx["S1"] + cx["S6"]), cx["S15"],
         cx["S10"], cx["S5"], cx["w3"], cx["X13"], cx["X9"], n(cx["S0"] + cx["S5"]))
    return tuple(x * ONES for x in w)


def omega_side(U, E, P):
    C0b1, nC0c1, C0d1, nC0b1w6, _, _, _, nX4w2, _, S15, _, _, _, _, _, nS0S5 = P
    Y8 = U ^ C0b1
    Y12 = Y8 + nC0c1
    Y0 = pror(Y12, 24) ^ C0d1
    C0a1 = Y0 + nC0b1w6
    X0 = C0a1 + nX4w2
    D0d1 = X0 ^ RX15
    D0a1 = pror(D0d1, 16) ^ S15
    w8 = D0a1 + nS0S5
    om = E + w8
    ov = Y12 ^ Y8 ^ nC0c1 | C0a1 ^ Y0 ^ nC0b1w6 | X0 ^ C0a1 ^ nX4w2 | w8 ^ D0a1 ^ nS0S5 | om ^ E ^ w8
    return C0a1, D0d1, om, ov, Y0


def pack(ms):
    U = E = 0
    for i, (e1, y, _) in enumerate(ms):
        U |= rol(y, 7) << LB * i
        E |= e1 << LB * i
    return U, E


def y9_path(C0a1, D0d1, P):
    _, _, _, _, rC0d1, Kp, S12, _, nS1S6, _, S10, S5, w3, X13, X9, _ = P
    X12 = C0a1 ^ rC0d1
    X12n = X12 ^ M_ALL
    D1d1 = X12n + Kp
    X1 = pror(X12, 24) ^ D1d1
    D1a1 = pror(D1d1, 16) ^ S12
    w10 = D1a1 + nS1S6
    D0c1 = D0d1 + S10
    D0b1 = pror(S5 ^ D0c1, 12)
    X10 = D0c1 + PX15
    X5 = pror(D0b1 ^ X10, 7)
    s1 = X1 + X5
    C1a1 = s1 + w3
    C1d1 = pror(X13 ^ C1a1, 16)
    C1c1 = X9 + C1d1
    C1b1 = pror(X5 ^ C1c1, 12)
    s2 = C1a1 + C1b1
    Y1 = s2 + w10
    Y13 = pror(C1d1 ^ Y1, 8)
    Y9 = C1c1 + Y13
    ov = (D1d1 ^ X12n ^ Kp | w10 ^ D1a1 ^ nS1S6 | D0c1 ^ D0d1 ^ S10 | X10 ^ D0c1 ^ PX15 | s1 ^ X1 ^ X5
          | C1a1 ^ s1 ^ w3 | C1c1 ^ X9 ^ C1d1 | s2 ^ C1a1 ^ C1b1 | Y1 ^ s2 ^ w10 | Y9 ^ C1c1 ^ Y13)
    return Y9, ov


class Row:

    def __init__(self, tau):
        self.tau, self.sigma = tau, tau ^ ror(tau, 1)
        self.theta = rol(self.sigma, 12)
        self.gamma = ETA ^ self.theta
        self.D = (self.sigma ^ EPS) & 0x7FFFFFFF
        self.low = tau in LOW_TAUS
        self.family = (self.low, bit(self.gamma, 10), tau if self.low else 0)   # 175/275 count as two (9.7)
        fixed = {7, 10, 11, 12, 16, 17, 18, 19, 20, 24, 25, 26, 29}
        self.free = [i for i in range(7, 32) if i not in fixed and not (i < 31 and bit(self.gamma, i))
                     and not ((i + 20) % 32 < 31 and bit(self.D, (i + 20) % 32))]


ROWS = {t: Row(t) for t in TAUS}


def is_joint_root(Q, y, E, h, tau):
    sigma = tau ^ ror(tau, 1)
    gg = (Q + h) & M
    if gg ^ ((Q + (h ^ ETA)) & M) != rol(sigma, 12):
        return False
    f = ror(y ^ gg, 12)
    e2 = (E + f) & M
    if e2 ^ ((((E + DY3) & M) + (f ^ sigma)) & M) != EPS:
        return False
    h2 = ror(h ^ e2, 8)
    return ((gg + h2) & M) ^ (((gg ^ rol(sigma, 12)) + (h2 ^ MU)) & M) == tau


def arc_of(d, u, a, v):
    Qi, yi, Ek, Epk, etai, gi, sk, kk, gi1, kk1, hasc, cval, li, lk = d
    gg = Qi ^ v ^ u
    u1, up1 = maj(Qi, v, u), maj(Qi, v ^ etai, u ^ gi)
    if not li and up1 != (u1 ^ gi1):
        return 0
    f = yi ^ gg
    e2 = Ek ^ f ^ a
    a1, ap1 = maj(Ek, f, a), maj(Epk, f ^ sk, a ^ kk)
    if not lk and ap1 != (a1 ^ kk1):
        return 0
    return 0x10 | (0 if li else u1) << 3 | (0 if lk else a1) << 2 | v << 1 | e2


def build_arrays():
    forced, dual, selected = [0] * (1 << 16), [0] * (1 << 16), [0] * (1 << 17)
    for key14 in range(1 << 14):
        d = tuple(key14 >> 13 - t & 1 for t in range(14))
        Qi, yi, Ek, Epk, etai, gi, sk, kk, gi1, kk1, hasc, cval, li, lk = d
        prescribed = (not li and gi) or (not lk and (kk ^ Ek ^ Epk))
        for cp in range(4):
            arcs = [arc_of(d, cp >> 1, cp & 1, 0), arc_of(d, cp >> 1, cp & 1, 1)]
            key = key14 << 2 | cp
            dual[key] = arcs[0] | arcs[1] << 5
            if hasc:
                forced[key] = arcs[cval]
            else:
                passing = [x for x in arcs if x]
                if len(passing) == 1:
                    forced[key] = passing[0]
                assert not (len(passing) == 2 and prescribed), "Lemma S5"
            for want in (0, 1):
                cand = [x for x in ((arcs[cval],) if hasc else arcs) if x and x & 1 == want]
                assert len(cand) <= 1
                selected[key << 1 | want] = cand[0] if cand else 0
    return forced, dual, selected


FORCED, DUAL, SELECTED = build_arrays()


def descriptor(row, Q, y, E, Ep, kappa, i, hasc=0, cval=0):
    k = (i + 20) % 32
    key = 0
    for b_ in (bit(Q, i), bit(y, i), bit(E, k), bit(Ep, k), bit(ETA, i), bit(row.gamma, i), bit(row.sigma, k),
               bit(kappa, k), bit(row.gamma, i + 1) if i < 31 else 0, bit(kappa, k + 1) if k < 31 else 0,
               hasc, cval, int(i == 31), int(k == 31)):
        key = key << 1 | b_
    return key


def nu_of(Q, e1, C, B):
    r = (((Q >> 16) ^ e1) & 4) ^ 7
    return ((((r + C) & M) ^ B) ^ 1) & 7


def g7_value(h6, e1, C, B):
    x = h6 ^ bit(e1, 22)
    return bit(e1, 23) ^ 1 ^ bit(C, 23) ^ bit(B, 23) ^ maj(x, bit(C, 22), x ^ bit(C, 22) ^ bit(B, 22))


def prescription(Ek, Epk, sk, kk1, a):
    return (Ek ^ sk ^ kk1) if a == Ek else (Epk ^ kk1)


def row_setup(row, Q, y, E, Ep, e1, kappa, C, B, notes):
    b, u, sg, gm = bit(e1, 2), bit(e1, 21), row.sigma, row.gamma
    Eb, Epb, kb, sb = (lambda k: bit(E, k)), (lambda k: bit(Ep, k)), (lambda k: bit(kappa, k)), (lambda k: bit(sg, k))
    kept = []                                            # (a) carry into bit 22
    for a20 in (0, 1):
        a, ap, ok = a20, a20 ^ kb(20), True
        for k in (20, 21):
            a1, ap1 = maj(Eb(k), 0, a), maj(Epb(k), sb(k), ap)
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
    for a20, _ in kept:                                               # walks of bits 0..6
        uu, aa, ok = 0, a20, True
        for i in range(7):
            arc = FORCED[descriptor(row, Q, y, E, Ep, kappa, i, 1, h[i]) << 2 | uu << 1 | aa]
            if not arc:
                ok = False
                break
            uu, aa = arc >> 3 & 1, arc >> 2 & 1
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


def g15_meta(h6, e1, bk):
    C, B, V = bk["C2_c1"], bk["C2_b1"], bk["Y12"]
    A = (bk["Y1"] + bk["w12"]) & M
    alpha22 = h6 ^ bit(e1, 22) ^ bit(C, 22) ^ bit(B, 22)
    v16 = bit(V, 16) ^ 1 ^ bit(A, 16)
    return e1 >> 22, (C >> 22) + alpha22, B >> 22, (A >> 16 & 511) + v16, V >> 16 & 511


def c_star(H, meta):
    E22, CA22, B22, A16v, V16 = meta
    zeta = ((((H >> 6) ^ E22) + CA22 ^ B22) >> 1) & 511
    return (Y11 & 511) + (((zeta + A16v) & 511) ^ V16)


def traverse(row, Q, y, E, Ep, kappa, e1, h, states, cnt, meta):
    u = bit(e1, 21)
    free = set(row.free) - ({15} if meta else set())
    keys = {i: descriptor(row, Q, y, E, Ep, kappa, i, 1, h[i]) if i in h else
            descriptor(row, Q, y, E, Ep, kappa, i) for i in range(7, 32)}
    pref0, out = sum(h[i] << i for i in range(7)), []
    stack = [(7, uu, aa, pref0, 0) for (uu, aa) in states]
    while stack:
        i, uu, aa, pref, e29 = stack.pop()
        if i == 32:                                                   # the meter (cnt[7]): each block its unit cost
            cnt[6] += 1
            cnt[7] += U_LEAF                                          # debited at its parent, position 31
            if is_joint_root(Q, y, E, pref, row.tau):
                out.append(pref)
                cnt[7] += U_ROOT
            continue
        cp = uu << 1 | aa
        if i in free:
            cnt[4] += 1
            cnt[7] += U_FREE
            w = DUAL[keys[i] << 2 | cp]
            arcs = (w & 0x1F, w >> 5 & 0x1F)
        else:
            cnt[0] += 1
            cnt[7] += U_FORCED
            key = keys[i]
            if i == 15 and meta:                                      # G15: test c0,c1,c3,c7; prescribe h15
                cnt[2] += 1
                cnt[7] += U_G15
                cs = c_star(pref, meta)
                if cs & 0x8B:
                    continue
                arcs = (FORCED[(key | 8 | (cs >> 8 & 1) << 2) << 2 | cp],)
            elif i == 20:                                             # Lemma J0
                cnt[1] += 1
                cnt[7] += U_SELECTED
                arcs = (SELECTED[(key << 2 | cp) << 1 | bit(pref, 8)],)
            elif i == 25:
                arcs = (FORCED[(key | 8 | (bit(pref, 6) ^ bit(pref, 13) ^ u) << 2) << 2 | cp],)
            elif i == 29:
                arcs = (FORCED[(key | 8 | (1 ^ e29) << 2) << 2 | cp],)
            else:
                arcs = (FORCED[key << 2 | cp],)
        for arc in arcs:
            if arc:
                stack.append((i + 1, arc >> 3 & 1, arc >> 2 & 1, pref | (arc >> 1 & 1) << i,
                               arc & 1 if i == 9 else e29))
    return out


def solve(bk, rows, g15, cnt, notes):
    Q, y, E, e1, C, B = bk["Y9"], bk["Y4"], bk["omega"], bk["e1"], bk["C2_c1"], bk["C2_b1"]
    Ep, out = (E + DY3) & M, []
    for t in rows:
        row = ROWS[t]
        kappa = row.sigma ^ EPS ^ E ^ Ep
        res = row_setup(row, Q, y, E, Ep, e1, kappa, C, B, notes)
        if res is not None:
            meta = g15_meta(res[0][6], e1, bk) if g15 else None
            out += [(r, t) for r in traverse(row, Q, y, E, Ep, kappa, e1, res[0], res[1], cnt, meta)]
    return out


def tree(row):
    free, n = [i for i in row.free if i != 15], [0] * 5
    for i in range(7, 32):
        k = 1 << sum(f < i for f in free)
        if i in free:
            n[3] += k
        else:
            n[0] += k
            n[1] += k * (i == 20)
            n[2] += k * (i == 15)
    n[4] = 1 << len(free)
    return n


def families(rows):
    return len({ROWS[t].family for t in rows})


def rows_of(T):
    return [t for j, t in enumerate(TAUS) if T >> j & 1 and S_MASK >> j & 1]


ROW_CAP = {t: U_ROW + sum(a * b for a, b in zip(tree(ROWS[t]), (U_FORCED, U_SELECTED, U_G15, U_FREE, U_LEAF + U_ROOT)))
           for t in TAUS}
CT = [U_GLOBAL + U_FAMILY * families(rows_of(T)) + sum(ROW_CAP[t] for t in rows_of(T)) if rows_of(T) else 0
      for T in range(128)]                   # the credit table: C_G(T) (CD 11.3)
assert all(ROW_CAP[t] == (5216 if len(ROWS[t].free) == 4 else 3328) for t in TAUS if t != 0x675020A0)
ENVELOPES = (0x04, 0x01, 0x18, 0x52)         # T lies in one of {275}, {175}, {285,385}, {185,385,685} (CD 11.3)
assert max(CT[T] for e in ENVELOPES for T in range(128) if T & ~e == 0) == 17504 and all(CT[T] == (U_GLOBAL + U_FAMILY * families(rows_of(T)) + sum(
    5216 if len(ROWS[t].free) == 4 else 3328 for t in rows_of(T)) if T & S_MASK else 0) for T in range(128))
CM = CT                                      # the metered cap: the debit is U itself (Lemma ME), at most C15(T)
CTW = [CM[T] | (U_GLOBAL + U_FAMILY * families(rows_of(T)) + U_ROW * len(rows_of(T)) if rows_of(T) else 0) << 16
       for T in range(128)]                  # the preflight word: CM(T) in bits 0..15, A(T) above
assert max(CM) < 65536
assert all(31 not in ROWS[t].free for t in TAUS)                  # every leaf's parent is a forced node at 31


def compress2(msg, t, flags):
    n = len(msg)
    w = list(struct.unpack("<16I", msg + bytes(64 - n)))
    v = list(IV) + list(IV[:4]) + [t & M, t >> 32, n, flags]
    s, yst = w, None
    for r in range(2):
        for i, (a, b, c, d) in enumerate(GCALLS):
            if r == 1 and i == 4:
                yst = list(v)
            v[a], v[b], v[c], v[d] = g(v[a], v[b], v[c], v[d], s[2 * i], s[2 * i + 1])
        s = [s[p] for p in PERM]
    return w, [v[i] ^ v[i + 8] for i in range(8)], yst


def c1_of(v, h):
    y6 = ror((((rol(h, 16) ^ v["e1"]) + v["C2_c1"]) & M) ^ v["C2_b1"], 7)
    return (Y11 + ror(((y6 + v["Y1"] + v["w12"]) & M) ^ v["Y12"], 16)) & M


def c1_t0(v):
    w0 = (rol(v["K0_d1"], 16) - IV[0] - IV[4]) & M
    y14 = ror(((w0 + v["C2_a1"] + v["C2_b1"]) & M) ^ v["C2_d1"], 8)
    return c1_of(v, ror(y14 ^ v["e1"], 16))


def step_ct(v, c1):
    u = dict(v)
    u["E1_a1"] = rol((c1 - Y11) & M, 16) ^ u["Y12"]
    u["Y6"] = (u["E1_a1"] - u["Y1"] - u["w12"]) & M
    u["Y10"] = rol(u["Y6"], 7) ^ u["C2_b1"]
    u["Y14"] = (u["Y10"] - u["C2_c1"]) & M
    u["E1_b1"] = ror(u["Y6"] ^ c1, 12)
    u["Y2"] = rol(u["Y14"], 8) ^ u["C2_d1"]
    u["E3_h1"] = ror(u["Y14"] ^ u["e1"], 16)
    u["w0"] = (u["Y2"] - u["C2_a1"] - u["C2_b1"]) & M
    u["K0_a1"] = (IV[0] + IV[4] + u["w0"]) & M
    u["t"] = rol(u["K0_d1"], 16) ^ u["K0_a1"]
    u["w1"] = (u["S0"] - u["K0_a1"] - u["K0_b1"]) & M
    w = [u.get("w%d" % i, 0) for i in range(16)]
    w[4], w[13] = W4, W13
    b = list(w)
    b[4], b[5] = W4B, (w[5] + DELTA5) & M
    pa, pb = struct.pack("<16I", *w), struct.pack("<16I", *b)
    assert not any(pa[LEN_A:]) and not any(pb[LEN_B:])
    u["A"], u["B"], u["c1"] = pa[:LEN_A], pb[:LEN_B], c1
    return u


def e1_g(y, w):
    a1 = (y[1] + y[6] + w[12]) & M
    d1 = ror(y[12] ^ a1, 16)
    c1 = (y[11] + d1) & M
    b1 = ror(y[6] ^ c1, 12)
    a2 = (a1 + b1 + w[5]) & M
    return a1, b1, c1, d1, a2, (c1 + ror(d1 ^ a2, 8)) & M


def chart(u, flags=FLAGS):
    t = u["t"] if flags == FLAGS else 0
    wa, cva, ya = compress2(u["A"], t, flags)
    wb, cvb, yb = compress2(u["B"], t, flags)
    ea, eb = e1_g(ya, wa), e1_g(yb, wb)
    j = []
    for y_, w_ in ((ya, wa), (yb, wb)):
        a1 = (y_[3] + y_[4] + w_[15]) & M
        d1 = ror(y_[14] ^ a1, 16)
        c1 = (y_[9] + d1) & M
        a2 = (a1 + ror(y_[4] ^ c1, 12) + w_[8]) & M
        j.append((c1, a2, (c1 + ror(d1 ^ a2, 8)) & M, d1))
    cons = (all(ya[i] == u["Y%d" % i] for i in (0, 1, 2, 4, 5, 6, 8, 9, 10, 12, 13, 14))
            and (ya[3], ya[11], yb[3], yb[11], yb[4]) == (Y3, Y11, Y3B, Y11B, u["Y4"])
            and (ea[2], ea[1], j[0][3]) == (u["c1"], u["E1_b1"], u["E3_h1"]))
    return dict(cons=cons, ea=ea, eb=eb, j=tuple(j[0][k] ^ j[1][k] for k in range(3)), cva=cva, cvb=cvb)


def pvals(bk, h):
    y14 = rol(h, 16) ^ bk["e1"]
    t = rol(bk["K0_d1"], 16) ^ ((IV[0] + IV[4] + (rol(y14, 8) ^ bk["C2_d1"]) - bk["C2_a1"] - bk["C2_b1"]) & M)
    y6 = ror(((y14 + bk["C2_c1"]) & M) ^ bk["C2_b1"], 7)
    a1 = (y6 + bk["Y1"] + bk["w12"]) & M
    d = ror(a1 ^ bk["Y12"], 16)
    c = (Y11 + d) & M
    b = ror(y6 ^ c, 12)
    a = (a1 + b + bk["w5"]) & M
    return t, c, a, b, b & BETA, d, ror(d ^ a, 8)


def test_a(a, s, tau):
    return a & tau == ((tau - BETA + 8 + 2 * s) & M) >> 1


def test_c(c, z, tau):
    return ((c + z) & M) ^ ((((c + DY11) & M) + (z ^ ror(tau, 8))) & M) == EPS


def predicate(bk, h, tau):
    t, c, a, b, s, d, z = pvals(bk, h)
    return (t != 0 and c & QSTAR_MASK == QSTAR_VALUE and test_a(a, s, tau) and test_c(c, z, tau)), c, t


def cert_full(v, h, tau):
    c1 = c1_of(v, h)
    u = step_ct(v, c1)
    if c1 & QSTAR_MASK != QSTAR_VALUE or u["t"] == 0:
        return False
    r = chart(u)
    return (r["cons"] and r["j"] == (theta_of(tau), EPS, tau) and r["cva"] == r["cvb"]
            and (r["ea"][4] ^ r["eb"][4], r["ea"][5] ^ r["eb"][5], r["ea"][1] ^ r["eb"][1]) == (tau, EPS, BETA))


def chart_check(v, c1):
    u = step_ct(v, c1)
    r, h = chart(u), u["E3_h1"]
    t, c, a, b, s, d, z = pvals(v, h)
    ea, eb = r["ea"], r["eb"]
    Q, y, E = v["Y9"], v["Y4"], v["omega"]
    ga, gb = (Q + h) & M, (Q + (h ^ ETA)) & M
    fa, fb = (E + ror(y ^ ga, 12)) & M, (E + DY3 + ror(y ^ gb, 12)) & M
    ok = (r["cons"] and all(r["cva"][i] == r["cvb"][i] for i in (0, 2, 5, 7))
          and r["j"] == (ga ^ gb, fa ^ fb, ((ga + ror(h ^ fa, 8)) ^ (gb + ror(h ^ ETA ^ fb, 8))) & M)
          and (t, c, a, b, d) == (u["t"], c1, ea[4], ea[1], ea[3]) and eb[1] == b ^ BETA
          and eb[4] == (a + BETA - 2 * s - 8) & M and eb[5] == (c + DY11 + ror(d ^ eb[4], 8)) & M
          and all(test_a(a, s, tau) == (ea[4] ^ eb[4] == tau) for tau in TAUS))
    if ok and ea[4] ^ eb[4] in TAUS:
        ok = test_c(c, z, ea[4] ^ eb[4]) == (ea[5] ^ eb[5] == EPS)
    x14 = rol(h, 16) ^ v["e1"]
    y6 = ror(((x14 + v["C2_c1"]) & M) ^ v["C2_b1"], 7)
    A = (v["Y1"] + v["w12"]) & M
    meta = g15_meta(bit(h, 6), v["e1"], v)
    g15 = (((x14 + v["C2_c1"]) ^ x14 ^ v["C2_c1"]) >> 22 & 1) == meta[1] - (v["C2_c1"] >> 22) and \
        (((y6 + A) ^ y6 ^ A) >> 16 & 1) == meta[3] - (A >> 16 & 511)
    if g15:
        cs = c_star(h & 0x7FFF, meta)
        ok = ok and not cs & 0x8B and cs >> 8 & 1 == bit(h, 15)
    return ok, g15


L31, PLANT_EVERY = 0x7FFFFFFF, 8
S_ROWS = [t for j, t in enumerate(TAUS) if S_MASK >> j & 1]
SOLS = {}


class Rng:

    def __init__(self, seed):
        self.s = int.from_bytes(hashlib.sha256(b"frontline plant" + seed).digest()[:8], "little")

    def __call__(self, n=32):
        self.s = (self.s + 0x9E3779B97F4A7C15) & (1 << 64) - 1
        z = (self.s ^ self.s >> 30) * 0xBF58476D1CE4E5B9 & (1 << 64) - 1
        z = (z ^ z >> 27) * 0x94D049BB133111EB & (1 << 64) - 1
        return (z ^ z >> 31) & (1 << n) - 1


def jroot_words(Q, y, E, h, tau):
    ga, gb = (Q + h) & M, (Q + (h ^ ETA)) & M
    fa, fb = (E + ror(y ^ ga, 12)) & M, (E + DY3 + ror(y ^ gb, 12)) & M
    return (ga ^ gb == rol(tau ^ ror(tau, 1), 12) and fa ^ fb == EPS
            and ((ga + ror(h ^ fa, 8)) ^ (gb + ror(h ^ ETA ^ fb, 8))) & M == tau)


def low_sample(rng, c, free, fixed, target):
    feas = [None] * 31 + [(1, 1)]

    def opts(i, cin):
        r = []
        for a in ((0, 1) if free >> i & 1 else (fixed >> i & 1,)):
            co = maj(a, c >> i & 1, cin)
            if (target >> i & 1 or not (a ^ c >> i ^ cin) & 1) and feas[i + 1][co]:
                r.append((a, co))
        return r
    for i in range(30, -1, -1):
        feas[i] = (len(opts(i, 0)) > 0, len(opts(i, 1)) > 0)
    if not feas[0][0]:
        return None
    a = cin = 0
    for i in range(31):
        o = opts(i, cin)
        b_, cin = o[rng(1) % len(o)]
        a |= b_ << i
    return a


def plant(tau, rng):
    s = tau ^ ror(tau, 1)
    th = rol(s, 12)
    k1, k2, k3 = (ETA - th & M) >> 1, (EPS - DY3 - s & M) >> 1, (tau - th - MU & M) >> 1
    if tau not in SOLS:
        s1, x = [], ETA & L31
        while True:
            if not (x - k1) & L31 & ~th:
                s1.append((x, (x - k1) & L31))
            if not x:
                break
            x = (x - 1) & ETA & L31
        SOLS[tau] = s1
    both = ETA & EPS & L31                            # h and e2 both fixed there: ROL(h2, 8) fixed
    fixm = ror(both, 8)
    for _ in range(64):
        e1 = CLASS_VALUE | rng() & FREE_MASK
        y = (e1 - Y3) & M
        opts = [(x, gf) for x, gt in SOLS[tau] for gf in ((gt, gt | 1 << 31) if th >> 31 else (gt,))
                if not ((ror((y ^ gf) & th, 12) & L31) + k2) & L31 & ~EPS]
        if not opts:
            continue
        x, gf = opts[rng() % len(opts)]               # h AND eta, g AND theta; then f AND sigma and e2 AND eps
        ee = ((ror((y ^ gf) & th, 12) & L31) + k2) & L31
        fv = ror((x ^ ee) & both, 8)
        m = low_sample(rng, (k3 + gf) & L31, MU & L31 & ~fixm, fv & MU, tau & L31)   # h2 AND mu
        if m is None:
            continue
        pt = (k3 + gf + m) & L31
        for _ in range(1 << 14):
            g_ = rng() & ~th & M | gf
            h2 = rng() & ~(MU & L31 | fixm) & M | m | fv
            p = (g_ + h2) & M
            if p & tau & L31 == pt and p ^ ((g_ ^ th) + (h2 ^ MU)) & M == tau:
                break
        else:
            continue
        r8, ep = rol(h2, 8), EPS & L31 & ~ETA
        h = rng() & ~(ETA & L31) & M | x
        h = h & ~ep & M | (r8 ^ ee) & ep
        Q, E = (g_ - h) & M, ((r8 ^ h) - ror(y ^ g_, 12)) & M
        if not jroot_words(Q, y, E, h, tau):
            continue
        C = rng()
        S_ = ((rol(h, 16) ^ e1) + C) & M
        B = rng() & ~(3 << 22) & M | bit(S_, 22) << 22 | (bit(S_, 23) ^ 1) << 23
        Y1, A = rng(), rng()
        cc = QSTAR_VALUE | rng() & ~QSTAR_MASK & M     # E1.c1 in Q*
        return dict(Y9=Q, Y4=y, omega=E, e1=e1, C2_c1=C, C2_b1=B, Y1=Y1, w12=(A - Y1) & M,
                    Y12=rol((cc - Y11) & M, 16) ^ (ror(S_ ^ B, 7) + A) & M), h
    return None


def plant_check(seed, k):
    tau = S_ROWS[k // PLANT_EVERY % len(S_ROWS)]
    r = plant(tau, Rng(seed))
    if r is None:
        return 1, 1
    bk, h = r
    cnt = [0] * 8
    new, old = solve(bk, [tau], True, cnt, []), solve(bk, [tau], False, [0] * 8, [])
    units = (U_GLOBAL + U_FAMILY + U_ROW + U_FORCED * cnt[0] + U_SELECTED * cnt[1] + U_G15 * cnt[2] + U_FREE * cnt[4]
             + U_LEAF * cnt[6] + U_ROOT * len(new))
    T = 1 << TAUS.index(tau)
    bad = (((h, tau) not in new) + ((h, tau) not in old) + (not set(new) <= set(old))
           + (not all(jroot_words(bk["Y9"], bk["Y4"], bk["omega"], *t) for t in old)) + (units > CT[T])
           + meter_bad(U_GLOBAL + U_FAMILY + U_ROW + cnt[7], units, T))
    return bad, 6


def meter_bad(d, units, T):
    return d != units or d > CM[T]


OBS = ("members", "e_lanes", "passes", "solver_calls", "leaves", "roots", "certified", "units", "solver_units",
       "opened", "closed", "skipped_pass", "checks", "mismatches", "fills", "halted")


class Halt(Exception):
    pass


class Found(Exception):
    pass


def steps23(ow, y, e1, T, o, A):
    v = rebuild(ow, y, e1)                                            # the second rebuild: the source bank
    rows = rows_of(T)
    bad0 = A != U_GLOBAL + U_FAMILY * families(rows) + U_ROW * len(rows)    # reference: A(T) of the preflight word
    cnt, notes = [0] * 8, []
    roots = solve(v, rows, True, cnt, notes)
    d = A + cnt[7]                                                    # the meter: A(T), then the block debits
    units = (A + U_FORCED * cnt[0] + U_SELECTED * cnt[1] + U_G15 * cnt[2] + U_FREE * cnt[4] + U_LEAF * cnt[6]
             + U_ROOT * len(roots))                                   # the ledger U, from the node counts
    o["units"] += d
    o["solver_units"] += units
    o["leaves"] += cnt[6]
    o["roots"] += len(roots)
    old = solve(v, rows, False, [0] * 8, [])                          # reference: 9.4 with (G7), no G15
    full = {r for r in old if cert_full(v, *r)}
    bad = (bad0 + len(set(roots) - set(old)) + len(full - set(roots)) + (units > CT[T]) + len(notes)    # ledger within C_G(T)
           + meter_bad(d, units, T))
    found = None
    for h, tau in roots:                                              # step 3, in traversal order
        ok, c, t = predicate(v, h, tau)
        bad += ok != ((h, tau) in full)
        if ok:
            o["certified"] += 1
            found = found or (c, t)
    if found:                                                         # the first certified root: the pair
        u = step_ct(v, found[0])
        cva, cvb = compress2(u["A"], u["t"], FLAGS)[1], compress2(u["B"], u["t"], FLAGS)[1]
        bad += u["t"] != found[1] or cva != cvb
        if cva == cvb:                                                # 256-bit equality: output and halt
            o["mismatches"] += bad
            raise Found(u)
    return bad, d


def walk(seed, nr=TRIAL_REPS, WR=0, credit=CREDIT, t2_every=T2_EVERY, gt=None):
    gt = gt or gtab
    sh = hashlib.shake_256(b"frontline context" + seed).digest(160)
    ow = struct.unpack("<7I", sh[:28])                                # word 7 of the fresh word is unused
    draws = [QSTAR_VALUE | w & ~QSTAR_MASK & M for w in struct.unpack("<32I", sh[32:])]   # c1 in Q* for charts
    o = dict.fromkeys(OBS, 0)
    o["units"] = U_CONTEXT
    first, bad, chk = None, 0, 0
    cx = co_ctx(*ow, FLAGS)                                           # the 39 context lines, once
    P = operands(cx)
    PF = P[:14] + (P[14] + B34 * ONES, P[15])                         # X9' = X9 + 2^34: Y9' = Y9 + 2^34 (T1 at 2^34)
    cx["XW"] = cx["X2"] + cx["S3"] - cx["K3_a1"] - cx["K3_b1"] & M    # X2 + w7, stored by the context
    nA = -((cx["C0_b1"] + cx["w6"] + cx["X4"] + cx["w2"] & M) >> 16) & 127    # -(A >> 16) mod 128
    q = (rol(X15, 24) ^ cx["S15"]) & 127                              # L mod 128
    B19 = (PB + (nA << 14) + ((P[15] & 127) << 21) + (q << 28)) * ONES   # gate base in every lane: nA, K, q folded

    def lane(ms, E, i, om, C0a1, D0d1, W, cy):
        nonlocal WR, credit, first, bad, chk
        sh_ = LB * i                                                  # the lane's position in the written-out code
        ix = om >> sh_ if i == 6 else om >> sh_ & L36                 # lane test: omega of lane i, the T2' address
        m2 = T2P(ix)                                                  # test (2): the T2' entry at that address
        omi = ix & M                                                  # reference from here: omega mod 2^32,
        e1, y, _ = ms[i]                                              # the member's e1 and y,
        rom, ry9 = co_ref(*ow, y, FLAGS)                              # the straight-line step CO
        rm2 = T2(rom)
        rx = T1(ry9) & rm2 if rm2 else 0
        x = y9i = 0
        bad += ix >= 3 << 32
        if m2:                                                        # lane test: the branch; E lane
            o["e_lanes"] += 1
            if not cy:                                                # not ready: W += u_E + u_G, fill the cache
                o["fills"] += 1
                o["units"] += U_EG
                WR += U_EG
                cy.append(y9_path(C0a1, D0d1, PF))                    # the packed Y9' of all lanes, once per batch
            else:
                o["units"] += U_E
                WR += U_E
            Y9p, ov2 = cy[0]
            bad += cy[0] != y9_path(C0a1, D0d1, PF)                   # reference: the cache against a fresh Y9 path
            y9i = Y9p >> sh_ & QM                                     # the T1 address 2^34 + Y9
            m1 = T1P(y9i)
            x = m1 & m2
            bad += m1 != mask1_ref(ry9) or y9i != B34 + ry9 or bool(ov2 & BOUND)
            u = step_ct(rebuild(ow, y, e1), draws[o["e_lanes"] & 31])
            wr, _, ys = compress2(u["A"], u["t"], FLAGS)
            bad += (ys[4], ys[9] + B34, (ys[3] + ys[4] + wr[15] + wr[8]) & M) != (y, y9i, omi)
            chk += 3
        bad += omi != rom or m2 != rm2 or x != rx or rom & 511 not in W
        chk += 1
        if m2 or ms[i][2] % t2_every == 0:
            bad += m2 != mask2_ref(omi)
            chk += 1
        if not x:                                                     # E lane: compare and branch
            return
        o["passes"] += 1                                              # passing lane
        o["units"] += U_PASS
        WR += U_PASS
        if first is None:
            first = ms[i][2]
        es = E >> sh_ & M                                             # shortcut (9.6): e1 out of lane i
        Q = Y9p >> sh_ & QM                                           # Q (2^34 + Y9) out of lane i
        d1c = ((C0a1 ^ P[4]) >> sh_ & M ^ M) + X11P & M               # D1.c1 = X11 - X12
        x6 = ror(ror(cx["S6"] ^ d1c, 12) ^ X11, 7)                    # X6 from D1.b1
        X10 = ((D0d1 + P[10]) >> sh_) + X15 & M                       # X10 = D0.c1 + X15
        C = X10 + ror(cx["X14"] ^ (x6 + cx["XW"] & M), 16) & M        # C2.c1 = X10 + C2.d1
        B = ror(x6 ^ C, 12)                                           # C2.b1
        v = rebuild(ow, y, e1)                                        # reference: the scalar rebuild,
        bad += (v["Y9"] + B34, v["omega"], v["C2_c1"], v["C2_b1"], e1) != (Q, omi, C, B, es)
        T = x & VMASK[nu_of(v["Y9"], e1, v["C2_c1"], v["C2_b1"])]   # the outcomes kept by 9.7,
        ok, gc = chart_check(v, draws[2 + o["passes"] % 30])          # and step CT
        bad, chk = bad + (not ok), chk + 3 + gc
        if ((Q >> 16 ^ es | 3) + C ^ B ^ 5) + 5 & 6:                  # pre-check (9.7): nonzero ends the outer step
            bad += T != 0
            return
        bad += T != x
        ct = CTW[x]                                                   # preflight: CM(T) | A(T) << 16, one load
        a = ct >> 16                                                  # A(T)
        if ct & 65535 > credit:                                       # CM(T) against the credit
            raise Halt(3)
        o["solver_calls"] += 1
        b, d = steps23(ow, y, es, x, o, a)
        credit -= d                                                   # the executed, metered debit
        bad += b
        chk += 2

    try:
        if WR > WB:                                                   # the one W test of a context (in the 600)
            raise Halt(1)
        e1, y = member(0)
        v = rebuild(ow, y, e1)
        for c1 in draws[:2]:
            ok, gc = chart_check(v, c1)
            bad, chk = bad + (not ok), chk + 1 + gc
        cw = (v["C0_b1"], v["C0_c1"], v["C0_d1"], v["C0_b1"] + v["w6"] + v["X4"] + v["w2"] & M,
              rol(X15, 24) ^ v["S15"], v["S0"] + v["S5"])            # reference: b, c, d, A, L, S0 + S5 of CI 1.1
        for rb in list(range(nr - 1)) + [REP_BATCHES - 1]:            # representative batches, the last of 4 lanes
            reps = [cmember(g, 0) for g in range(7 * rb, min(7 * rb + 7, 1 << 14))]
            U, E = pack(reps)
            C0a1, D0d1, om, ov, Y0 = omega_side(U, E, P)
            key = (Y0 >> 9 & R7H) | (E & R7) | B19                   # e1 mod 128 | a_raw << 7 | base, every lane
            ref = ((Y0 >> 16 & R7) + nA * ONES & R7) | (E + P[15] & R7) << 7     # reference: the key a | c << 7
            o["units"] += U_REP if len(reps) == 7 else U_REP_TAIL
            o["members"] += len(reps)
            rc = []                                                   # the batch's cache, kept across its partners
            for i in range(len(reps)):
                g = 7 * rb + i
                W = prefixes(cw, *reps[i][1::-1])
                kx = key >> LB * i if i == 6 else key >> LB * i & L36
                bad += not PB <= kx < 2 * PB or gtab(kx) != gate(q << 14 | ref >> LB * i & 0x3FFF)
                chk += 1
                if not gt(kx):                                        # closed: no T2 load, the next gate test
                    o["closed"] += 1
                    for j in range(32):                               # reference: all 32 members fail (2)
                        rom = co_ref(*ow, cmember(g, j)[1], FLAGS)[0]
                        m = mask2_ref(rom) > 0
                        o["skipped_pass"] += m
                        bad += m or rom & 511 not in W or (j == 0 and (rom != om >> LB * i & M or any(
                            S7 >> (w & 127) & 1 for w in W)))                 # both exact prefixes dead
                        chk += 1
                    continue
                o["opened"] += 1                                      # opened: W, then partner work
                o["units"] += U_OPEN
                WR += U_OPEN
                lane(reps, E, i, om, C0a1, D0d1, W, rc)               # the representative's T2 and paths
                for j0 in range(1, 32, 7):                            # five partner batches, j = 1..31
                    ms = [cmember(g, j) for j in range(j0, min(j0 + 7, 32))]
                    pE = pack(ms)
                    pa, pd, pom, pov, _ = omega_side(*pE, P)
                    o["members"] += len(ms)
                    pc = []                                           # the partner batch's cache: not ready
                    for t in range(len(ms)):
                        lane(ms, pE[1], t, pom, pa, pd, W, pc)
                    bad += bool(pov & BOUND)
                    chk += 1
            bad += bool(ov & BOUND)                                   # Lemma MB (d): no lane reaches 2^36
            chk += 1
    except Halt as e:
        o["halted"] = e.args[0]
    except Found:
        pass
    o["mismatches"] += bad
    o["checks"] += chk
    return ow, first, o, WR


def root_pair(ow, k):
    e1, y = member(k)
    v = rebuild(ow, y, e1, ROOT_FLAGS)
    u = step_ct(v, c1_t0(v))
    da, db = compress2(u["A"], 0, ROOT_FLAGS)[1], compress2(u["B"], 0, ROOT_FLAGS)[1]
    return u["A"], u["B"], u["t"] == 0 and all(da[i] == db[i] for i in (0, 2, 5, 7))


def trial(seed, k=0):
    ow, first, o, _ = walk(seed)
    a, b, ok = root_pair(ow, 0 if first is None else first)
    o["checks"] += 1
    o["mismatches"] += not ok
    if k % PLANT_EVERY == 0:                                          # reference: a planted joint root
        bad, n = plant_check(seed, k)
        o["checks"] += n
        o["mismatches"] += bad
    return a, b, o


def selftest(n):
    rep = {"constants": all(globals()[k] == x for k, x in TEXT.items())}
    th = [theta_of(t) for t in TAUS]
    tq, te = [(ETA & 255, x & 255) for x in th], [(ror(x, 12) & 255, EPS & 255) for x in th]
    a1, a2 = automaton(tq, 0, 8)[0], automaton(te, DY3 & 255, 8)[0]
    bf = lambda tg, dy, x: sum(1 << j for j, (dz, out) in enumerate(tg)
                               if any(((x + v) ^ (x + dy + (v ^ dz))) & 255 == out for v in range(256)))
    rep["automata_vs_bruteforce_w8"] = sum(a1[x] == bf(tq, 0, x) and a2[x] == bf(te, DY3, x) for x in range(256))
    cnt = []
    for t in (AUT1, AUT2):
        cur = {}
        for b in range(256):
            cur[t[0][b]] = cur.get(t[0][b], 0) + 1
        for tb in t[1:]:
            nxt = {}
            for s, c in cur.items():
                for b in range(256):
                    nxt[tb[s + b]] = nxt.get(tb[s + b], 0) + c
            cur = nxt
        cnt.append(cur)
    rep["SHARE_E_COUNT"] = (sum(c1 * c2 for p, c1 in cnt[0].items() for q, c2 in cnt[1].items() if p & q) == SHARE
                            and sum(c for q, c in cnt[1].items() if q) == E_COUNT)
    rnd = hashlib.shake_256(b"frontline selftest").digest(8 * n)
    xs = struct.unpack("<%dI" % (2 * n), rnd)
    rep["T1_T2_vs_bitserial"] = sum(T1(x) == mask1_ref(x) and T2(x) == mask2_ref(x) for x in xs)
    al = [any(((w + f) ^ ((w + DY3) + (f ^ s))) & 511 == EPS & 511 for s in {SIGMAS[j] & 511 for j, _, _ in SIG3}
              for f in range(512)) for w in range(512)]               # Alive9: four copies of S7 (CI 1.3)
    rep["S7_partition"] = (sum(al) == 208 and all(al[w] == S7 >> (w & 127) & 1 for w in range(512))
                           and all(S7 >> (x & 127) & 1 for x in xs if T2(x))
                           and len({g & 63 | j << 6 | g >> 6 << 11 for g in range(1 << 14) for j in range(32)}) == 1 << 19
                           and all(cmember(g, j)[0] >> 10 & 31 == j for g in (0, 9999, 16383) for j in range(32)))
    rep["precheck"] = all((((a >> 16 ^ b | 3) + c ^ d ^ 5) + 5 & 6 == 0) == (VMASK[nu_of(a, b, c, d)] & S_MASK > 0)
                          for a, b, c, d in zip(xs, xs[1:], xs[2:], xs[3:]))
    drills = {}
    for name, kw, code in (("W", dict(WR=WB + 1), 1), ("C", dict(credit=0), 3), ("R", dict(credit=17504), 0)):
        for s in range(64):
            o = walk(b"drill%d" % s, **kw)[2]
            if o["halted"] if code else o["solver_calls"]:
                break
        drills[name] = (o["halted"] in (0, 3) and o["solver_calls"] >= 1 and not o["mismatches"] if name == "R" else
                        o["halted"] == code and (o["members"] == 0 and o["units"] == U_CONTEXT if name == "W"
                        else o["solver_calls"] == 0 and o["passes"] >= 1), s)
    _, _, o, w = walk(b"drill0", WR=WB)        # W = WB: the context runs to its end and adds at most W_CTX
    drills["WB"] = (o["halted"] == 0 and WB < w <= WB + W_CTX and not o["mismatches"], 0)
    rep["halt_drills"] = drills                # R: a credit of the reserve 17,504 = max CM(T) admits any first call
    gd = {}                                  # gate drills: the table against no gate (lossless) and against a dead gate
    for name, gt in (("table", gtab), ("open", lambda i: 1), ("closed", lambda i: 0)):
        r = [walk(b"gate%d" % s, gt=gt)[2] for s in range(8)]
        gd[name] = [sum(o[k] for o in r) for k in ("opened", "closed", "e_lanes", "passes", "skipped_pass", "mismatches",
                                                   "fills")]
    t, op, cl = gd["table"], gd["open"], gd["closed"]
    rep["gate_drills"] = gd
    rep["ok"] = (rep["constants"] and rep["automata_vs_bruteforce_w8"] == 256 and rep["SHARE_E_COUNT"] and rep["precheck"]
                 and rep["T1_T2_vs_bitserial"] == 2 * n and all(d[0] for d in drills.values()) and rep["S7_partition"]
                 and t[4] == t[5] == op[4] == op[5] == op[1] == cl[0] == cl[6] == 0 and t[2:4] == op[2:4]
                 and t[6] == op[6] > 0 and cl[4] == op[2] > 0 and cl[5] >= cl[4])
    json.dump(rep, sys.stdout, separators=(",", ":"))
    sys.stdout.write("\n")
    return 0 if rep["ok"] else 1


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] != "--selftest":
            raise SystemExit("usage: frontline.py [--selftest [N]]   (else: organizer request on stdin)")
        raise SystemExit(selftest(int(sys.argv[2]) if len(sys.argv) > 2 else 2000))
    request = json.load(sys.stdin)
    if request["schema_version"] != 1 or request["target_profile"] != "blake3-r2-prefix-v1":
        raise ValueError("unexpected organizer target")
    if request["event"].get("kind") != "digest-xor-mask" or request["experiment_id"] != "frontline-search":
        raise ValueError("unexpected organizer event or experiment")
    trials = []
    for tr in request["trials"]:
        a, b, obs = trial(bytes.fromhex(tr["seed"]), tr["trial"])
        trials.append({"trial": tr["trial"], "message_a_hex": a.hex(), "message_b_hex": b.hex(), "observations": obs})
    json.dump({"schema_version": 1, "trials": trials}, sys.stdout, separators=(",", ":"), sort_keys=True)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
