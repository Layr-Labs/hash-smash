"""The v110 program (proof.md 6.4, 9.2, 9.3 and Section 11): the walk of the counter search by contexts, representative
batches, the straddle gate and the masked partner walk with its two chunks under one joint dispatch, executed on the
counted packed machine and checked member by member against step CO, test (2) and the filter (the organizer experiment cluster-walk, which
returns a root-instance pair of 6.1 per seed); the chunk-counter construction, the filter for the outcomes of S, and the
ledger of Section 11 with its integer test (the self-test)."""
import hashlib
import json
import math
import struct
import sys
MASK = 0xFFFFFFFF
IV = (0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A,
      0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19)
K = (IV[2] + IV[6]) & MASK
LEN_A, LEN_B = 55, 63
X3, X7, X11, X15 = 0x29D4FA98, 0xBEE3AF28, 0x44036000, 0x40C58500
W4, W13 = 0x97475638, 0x0007C006
W4B = (((W4 + K) & MASK) ^ LEN_A ^ LEN_B) - K & MASK
DELTA5 = (W4 - W4B) & MASK
ETA = 0x830303CF
CUBE = (0x04200000, 0x00000000)
CONTEXT_WORDS = ("C0.c1", "C0.d1", "D3.d1", "S15", "S9", "w5", "X2")
def ror(v, n):
    return ((v >> n) | (v << (32 - n))) & MASK
def rol(v, n):
    return ((v << n) | (v >> (32 - n))) & MASK
def g(a, b, c, d, x, y):
    a = (a + b + x) & MASK; d = ror(d ^ a, 16); c = (c + d) & MASK; b = ror(b ^ c, 12)
    a = (a + b + y) & MASK; d = ror(d ^ a, 8); c = (c + d) & MASK; b = ror(b ^ c, 7)
    return a, b, c, d
Y3, _, Y11, _ = g(X3, X7, X11, X15, W4, W13)
Y3B, _, Y11B, _ = g(X3, X7, X11, X15, W4B, W13)
K2A = (K + W4) & MASK
K2D = ror(K2A ^ LEN_A, 16)
K2C = (IV[2] + K2D) & MASK
K2B = ror(IV[6] ^ K2C, 12)
def class_pattern():
    'Lemma Q and the sub-class: the bits of e1 = Y3 + Y4 that eta or CUBE fixes (mask, value), the free positions.'
    x = rol(ETA, 16)
    v = (Y3B - Y3 + x) & MASK
    if v & 1 or (v >> 1) & ~x & MASK:
        raise ValueError("no Y4 gives this eta")
    mask = x & 0x7FFFFFFF
    if CUBE[0] & mask or CUBE[1] & ~CUBE[0]:
        raise ValueError("CUBE names a bit that eta fixes, or a value outside its bits")
    mask, value = mask | CUBE[0], ~(v >> 1) & mask | CUBE[1]
    return mask, value, tuple(i for i in range(32) if not mask >> i & 1)
CLASS_MASK, CLASS_VALUE, CLASS_FREE = class_pattern()
CLASS_SIZE = 1 << len(CLASS_FREE)
CTR_FLAGS = 3
CTR_MASK, CTR_VALUE, CTR_BETA = 0x0E09818B, 0x02008000, 0x18B0E098
CTR_FREE = tuple(i for i in range(32) if not CTR_MASK >> i & 1)
CTR_BASIS = ("C0.d1", "D2.a1", "D2.b1", "S11", "S4", "X9", "w6")
CTR_MEMBERS = 1 << len(CTR_FREE)
# Y4 runs over the whole class of eta (Lemma Q: 2^19 members); no sub-class, no rule A.
CTR_CLASS = rol(ETA, 16) & 0x7FFFFFFF
CTR_CFREE = tuple(i for i in range(32) if not CTR_CLASS >> i & 1)
CTR_CSIZE = 1 << len(CTR_CFREE)
# The seven outcomes (tau, eps) of beta* whose tau ends in 5020a0 (the automata of proof.md Section 8), their parts
# (L * N3 / 2^83, Section 17), the listed set S = 5f (all but 675020a0; count 67,633,152), and the constants of
# proof.md 9.1: the factor of H1' at ten elevenths, the run for 0.49594 expected listed good trials, the four budgets
# with their reserves over contexts, and the metered credit of the solver.
CTR_TAUS = (0x175020A0, 0x185020A0, 0x275020A0, 0x285020A0, 0x385020A0, 0x675020A0, 0x685020A0)
CTR_EPS = 0x6E21BE55
CTR_PARTS = (6291456, 16777216, 1048576, 25165824, 16777216, 65536, 1572864)
S_MASK = 0x5F
S_COUNT = sum(p for j, p in enumerate(CTR_PARTS) if S_MASK >> j & 1)
FACTOR = 10 * (S_COUNT << 11) // 11
RUN_STEPS_MIN = -(-(24797 << 128) // (50000 * FACTOR * (CTR_MEMBERS - 1)))
RUN_CONTEXTS = -(-RUN_STEPS_MIN >> 19)
RUN_STEPS = RUN_CONTEXTS << 19
def ceil_sqrt(x):
    r = math.isqrt(x)
    return r + (r * r < x)
RESERVE_S = ceil_sqrt(10 * RUN_CONTEXTS)
SHARE, E_COUNT = 18289159183466496, 233715456
A_BUDGET = -(-852139 * RUN_CONTEXTS >> 7) + 16384 * RESERVE_S
E_BUDGET = -(-1000026 * RUN_STEPS * E_COUNT // (1000000 << 32)) + (RESERVE_S << 19)
G_BUDGET = 12466 * RUN_CONTEXTS + 84261 * RESERVE_S
PASS_BUDGET = -(-1000176 * RUN_STEPS * SHARE // (1000000 << 64)) + (RESERVE_S << 19)
U_MODEL = 92113900425963
CAP = 15296
M_0 = -(-101 * RUN_STEPS * U_MODEL // (100 << 46))
M_C = -(-478 * M_0 // 487)
L_C = CAP << 19
CREDIT = M_C + ceil_sqrt(40 * L_C * M_C) + 14 * L_C + CAP
def class_member(k):
    'Y4 of class member number k: the bits of k fill the free positions of e1 in increasing order.'
    e1 = CLASS_VALUE
    for j, i in enumerate(CLASS_FREE):
        e1 |= (k >> j & 1) << i
    return (e1 - Y3) & MASK
def outer(six):
    'Step S1, first part: the lines that read neither X2 nor the member, for the six words of an outer step.'
    c0c, c0d, d3d, s15, s9, w5 = six
    v = {"C0.c1": c0c, "C0.d1": c0d, "D3.d1": d3d, "S15": s15, "S9": s9, "w5": w5}
    v["S2"] = (K2A + K2B + w5) & MASK
    v["S14"] = ror(K2D ^ v["S2"], 8)
    v["S10"] = (K2C + v["S14"]) & MASK
    v["S6"] = ror(K2B ^ v["S10"], 7)
    v["D3.a1"] = rol(d3d, 16) ^ v["S14"]
    v["D3.c1"] = (s9 + d3d) & MASK
    v["D3.b1"] = (X3 - v["D3.a1"]) & MASK
    v["S4"] = rol(v["D3.b1"], 12) ^ v["D3.c1"]
    v["S3"] = (v["D3.a1"] - v["S4"]) & MASK
    v["X14"] = ror(d3d ^ X3, 8)
    v["X9"] = (v["D3.c1"] + v["X14"]) & MASK
    v["X4"] = ror(v["D3.b1"] ^ v["X9"], 7)
    v["K3.d1"] = rol(s15, 8) ^ v["S3"]
    v["K3.c1"] = (IV[3] + v["K3.d1"]) & MASK
    v["K3.b1"] = ror(IV[7] ^ v["K3.c1"], 12)
    v["S11"] = (v["K3.c1"] + s15) & MASK
    v["S7"] = ror(v["K3.b1"] ^ v["S11"], 7)
    v["K3.a1"] = rol(v["K3.d1"], 16) ^ 11
    v["w6"] = (v["K3.a1"] - IV[3] - IV[7]) & MASK
    v["w7"] = (v["S3"] - v["K3.a1"] - v["K3.b1"]) & MASK
    v["C0.b1"] = ror(v["X4"] ^ c0c, 12)
    v["X8"] = (c0c - c0d) & MASK
    v["D2.b1"] = rol(X7, 7) ^ v["X8"]
    v["D2.c1"] = rol(v["D2.b1"], 12) ^ v["S7"]
    v["X13"] = (v["X8"] - v["D2.c1"]) & MASK
    return v
def middle(o, x2):
    'Step S1, second part: the lines that read X2, for the values o of an outer step. Returns o with them.'
    v = dict(o, X2=x2)
    v["D2.a1"] = (x2 - v["D2.b1"] - W13) & MASK
    v["D2.d1"] = rol(v["X13"], 8) ^ x2
    v["S13"] = rol(v["D2.d1"], 16) ^ v["D2.a1"]
    v["S8"] = (v["D2.c1"] - v["D2.d1"]) & MASK
    v["w12"] = (v["D2.a1"] - v["S2"] - v["S7"]) & MASK
    v["K1.c1"] = (v["S9"] - v["S13"]) & MASK
    v["K1.d1"] = (v["K1.c1"] - IV[1]) & MASK
    v["K1.a1"] = rol(v["K1.d1"], 16)
    v["K1.b1"] = ror(IV[5] ^ v["K1.c1"], 12)
    v["S1"] = rol(v["S13"], 8) ^ v["K1.d1"]
    v["S5"] = ror(v["K1.b1"] ^ v["S9"], 7)
    v["w2"] = (v["K1.a1"] - IV[1] - IV[5]) & MASK
    v["w3"] = (v["S1"] - v["K1.a1"] - v["K1.b1"]) & MASK
    v["K0.b1"] = rol(v["S4"], 7) ^ v["S8"]
    v["K0.c1"] = rol(v["K0.b1"], 12) ^ IV[4]
    v["K0.d1"] = (v["K0.c1"] - IV[0]) & MASK
    v["K0.a1"] = rol(v["K0.d1"], 16)
    v["S12"] = (v["S8"] - v["K0.c1"]) & MASK
    v["S0"] = rol(v["S12"], 8) ^ v["K0.d1"]
    v["w0"] = (v["K0.a1"] - IV[0] - IV[4]) & MASK
    v["w1"] = (v["S0"] - v["K0.a1"] - v["K0.b1"]) & MASK
    return v
def context(free):
    'Step S1 for the seven words of CONTEXT_WORDS: every value of the two parts by its name.'
    return middle(outer(free[:6]), free[6])
def member(o, y4):
    'The lines that read the member and no word of the middle step: one row of the table of an outer step.'
    y12 = ((rol(y4, 7) ^ o["C0.b1"]) - o["C0.c1"]) & MASK
    a1 = ((rol(y12, 8) ^ o["C0.d1"]) - o["C0.b1"] - o["w6"]) & MASK
    x12 = rol(o["C0.d1"], 16) ^ a1
    c_d1 = (X11 - x12) & MASK
    b_d1 = ror(o["S6"] ^ c_d1, 12)
    d_d1 = (c_d1 - o["S11"]) & MASK
    return {"Y12": y12, "C0.a1": a1, "X12": x12, "D1.b1": b_d1, "X6": ror(b_d1 ^ X11, 7), "D1.d1": d_d1,
            "X1": rol(x12, 8) ^ d_d1}
def messages(w):
    'Steps S2 and S3.'
    other = list(w)
    other[4] = W4B
    other[5] = (w[5] + DELTA5) & MASK
    return struct.pack("<16I", *w)[:LEN_A], struct.pack("<16I", *other)[:LEN_B]
def trial(v, y4):
    'The trial of proof.md 6.1 for the context v and class member y4: returns (words, values of the trial).'
    r = member(v, y4)
    x0 = (r["C0.a1"] - v["X4"] - v["w2"]) & MASK
    d_d0 = rol(X15, 8) ^ x0
    c_d0 = (v["S10"] + d_d0) & MASK
    x10 = (c_d0 + X15) & MASK
    b_d0 = ror(v["S5"] ^ c_d0, 12)
    a_d0 = rol(d_d0, 16) ^ v["S15"]
    a_d1 = rol(r["D1.d1"], 16) ^ v["S12"]
    words = [v["w0"], v["w1"], v["w2"], v["w3"], W4, v["w5"], v["w6"], v["w7"],
             (a_d0 - v["S0"] - v["S5"]) & MASK, (x0 - a_d0 - b_d0) & MASK,
             (a_d1 - v["S1"] - v["S6"]) & MASK, (r["X1"] - a_d1 - r["D1.b1"]) & MASK, v["w12"], W13, 0, 0]
    return words, dict(r, X0=x0, X5=ror(b_d0 ^ x10, 7), X10=x10)
PERMUTATION = (2, 6, 3, 10, 7, 0, 4, 13, 1, 11, 12, 5, 9, 14, 15, 8)
G_CALLS = ((0, 4, 8, 12), (1, 5, 9, 13), (2, 6, 10, 14), (3, 7, 11, 15),
           (0, 5, 10, 15), (1, 6, 11, 12), (2, 7, 8, 13), (3, 4, 9, 14))
def compress2(message, counter=0, flags=11):
    'The complete 2-round compression of proof.md Section 1 for one message of at most 64 bytes (or one last chunk).'
    n = len(message)
    w = list(struct.unpack("<16I", message + bytes(64 - n)))
    v = list(IV) + list(IV[:4]) + [counter & MASK, counter >> 32, n, flags]
    s, y = list(w), None
    for r in range(2):
        for i, (a, b, c, d) in enumerate(G_CALLS):
            if r == 1 and i == 4:
                y = list(v)
            v[a], v[b], v[c], v[d] = g(v[a], v[b], v[c], v[d], s[2 * i], s[2 * i + 1])
        s = [s[p] for p in PERMUTATION]
    return w, [v[i] ^ v[i + 8] for i in range(8)], y
def seeded(seed):
    'The seven words of a context and a class member number from the organizer seed.'
    stream = struct.unpack("<8I", hashlib.shake_256(seed).digest(32))
    return stream[:7], stream[7] % CLASS_SIZE
def half_collision(seed):
    free, k = seeded(seed)
    return messages(trial(context(free), class_member(k))[0]) + ({},)
def ctr_c1(j):
    'E1.c1 of cube member j: the bits of j fill the free positions of (c1 AND CTR_MASK) = CTR_VALUE in increasing order.'
    c1 = CTR_VALUE
    for n, i in enumerate(CTR_FREE):
        c1 |= (j >> n & 1) << i
    return c1
def ctr_outer(eight, y4=None):
    'The unstarred lines of the counter order, in its sequence, for the words of CTR_BASIS and class member eight[7].'
    v = dict(zip(CTR_BASIS, eight), Y4=ctr_member(eight[7] & CTR_CSIZE - 1) if y4 is None else y4)
    v["X2"] = (v["D2.a1"] + v["D2.b1"] + W13) & MASK
    v["X8"] = rol(X7, 7) ^ v["D2.b1"]
    v["C0.c1"] = (v["X8"] + v["C0.d1"]) & MASK
    v["K3.a1"] = (IV[3] + IV[7] + v["w6"]) & MASK
    v["K3.d1"] = ror(v["K3.a1"] ^ CTR_FLAGS, 16)
    v["K3.c1"] = (IV[3] + v["K3.d1"]) & MASK
    v["S15"] = (v["S11"] - v["K3.c1"]) & MASK
    v["S3"] = rol(v["S15"], 8) ^ v["K3.d1"]
    v["K3.b1"] = ror(IV[7] ^ v["K3.c1"], 12)
    v["D3.a1"] = (v["S3"] + v["S4"]) & MASK
    v["S7"] = ror(v["K3.b1"] ^ v["S11"], 7)
    v["D3.b1"] = (X3 - v["D3.a1"]) & MASK
    v["D2.c1"] = rol(v["D2.b1"], 12) ^ v["S7"]
    v["D3.c1"] = rol(v["D3.b1"], 12) ^ v["S4"]
    v["X4"] = ror(v["D3.b1"] ^ v["X9"], 7)
    v["X13"] = (v["X8"] - v["D2.c1"]) & MASK
    v["X14"] = (v["X9"] - v["D3.c1"]) & MASK
    v["C0.b1"] = ror(v["X4"] ^ v["C0.c1"], 12)
    v["D2.d1"] = rol(v["X13"], 8) ^ v["X2"]
    v["D3.d1"] = rol(v["X14"], 8) ^ X3
    v["Y8"] = rol(v["Y4"], 7) ^ v["C0.b1"]
    v["S13"] = rol(v["D2.d1"], 16) ^ v["D2.a1"]
    v["S9"] = (v["D3.c1"] - v["D3.d1"]) & MASK
    v["Y12"] = (v["Y8"] - v["C0.c1"]) & MASK
    v["K1.c1"] = (v["S9"] - v["S13"]) & MASK
    v["Y0"] = rol(v["Y12"], 8) ^ v["C0.d1"]
    v["K1.d1"] = (v["K1.c1"] - IV[1]) & MASK
    v["C0.a1"] = (v["Y0"] - v["C0.b1"] - v["w6"]) & MASK
    v["K1.a1"] = rol(v["K1.d1"], 16)
    v["w2"] = (v["K1.a1"] - IV[1] - IV[5]) & MASK
    v["X0"] = (v["C0.a1"] - v["X4"] - v["w2"]) & MASK
    v["S14"] = rol(v["D3.d1"], 16) ^ v["D3.a1"]
    v["K1.b1"] = ror(IV[5] ^ v["K1.c1"], 12)
    v["S10"] = (K2C + v["S14"]) & MASK
    v["D0.d1"] = rol(X15, 8) ^ v["X0"]
    v["S5"] = ror(v["K1.b1"] ^ v["S9"], 7)
    v["D0.c1"] = (v["S10"] + v["D0.d1"]) & MASK
    v["D0.b1"] = ror(v["S5"] ^ v["D0.c1"], 12)
    v["X10"] = (v["D0.c1"] + X15) & MASK
    v["X5"] = ror(v["D0.b1"] ^ v["X10"], 7)
    v["S1"] = rol(v["S13"], 8) ^ v["K1.d1"]
    v["w3"] = (v["S1"] - v["K1.a1"] - v["K1.b1"]) & MASK
    v["X12"] = rol(v["C0.d1"], 16) ^ v["C0.a1"]
    v["D1.c1"] = (X11 - v["X12"]) & MASK
    v["D1.d1"] = (v["D1.c1"] - v["S11"]) & MASK
    v["S8"] = (v["D2.c1"] - v["D2.d1"]) & MASK
    v["K0.b1"] = rol(v["S4"], 7) ^ v["S8"]
    v["S2"] = rol(v["S14"], 8) ^ K2D
    v["S6"] = ror(K2B ^ v["S10"], 7)
    v["X1"] = rol(v["X12"], 8) ^ v["D1.d1"]
    v["K0.c1"] = rol(v["K0.b1"], 12) ^ IV[4]
    v["D1.b1"] = ror(v["S6"] ^ v["D1.c1"], 12)
    v["C1.a1"] = (v["X1"] + v["X5"] + v["w3"]) & MASK
    v["S12"] = (v["S8"] - v["K0.c1"]) & MASK
    v["w7"] = (v["S3"] - v["K3.a1"] - v["K3.b1"]) & MASK
    v["X6"] = ror(v["D1.b1"] ^ X11, 7)
    v["C1.d1"] = ror(v["X13"] ^ v["C1.a1"], 16)
    v["D1.a1"] = rol(v["D1.d1"], 16) ^ v["S12"]
    v["C1.c1"] = (v["X9"] + v["C1.d1"]) & MASK
    v["C2.a1"] = (v["X2"] + v["X6"] + v["w7"]) & MASK
    v["w10"] = (v["D1.a1"] - v["S1"] - v["S6"]) & MASK
    v["C1.b1"] = ror(v["X5"] ^ v["C1.c1"], 12)
    v["C2.d1"] = ror(v["X14"] ^ v["C2.a1"], 16)
    v["w12"] = (v["D2.a1"] - v["S2"] - v["S7"]) & MASK
    v["Y1"] = (v["C1.a1"] + v["C1.b1"] + v["w10"]) & MASK
    v["C2.c1"] = (v["X10"] + v["C2.d1"]) & MASK
    v["Y13"] = ror(v["C1.d1"] ^ v["Y1"], 8)
    v["C2.b1"] = ror(v["X6"] ^ v["C2.c1"], 12)
    v["K0.d1"] = (v["K0.c1"] - IV[0]) & MASK
    v["Y9"] = (v["C1.c1"] + v["Y13"]) & MASK
    v["S0"] = rol(v["S12"], 8) ^ v["K0.d1"]
    v["D0.a1"] = rol(v["D0.d1"], 16) ^ v["S15"]
    v["w8"] = (v["D0.a1"] - v["S0"] - v["S5"]) & MASK
    v["w5"] = (v["S2"] - K2A - K2B) & MASK
    v["w9"] = (v["X0"] - v["D0.a1"] - v["D0.b1"]) & MASK
    v["w11"] = (v["X1"] - v["D1.a1"] - v["D1.b1"]) & MASK
    v["Y5"] = ror(v["C1.b1"] ^ v["Y9"], 7)
    return v
def ctr_trial(o, c1):
    'The starred lines for E1.c1 = c1: (block A, block B, t, words), or None for t = 0 (one chunk: root, flags 11).'
    v = dict(o, **{"E1.c1": c1, "E1.d1": (c1 - Y11) & MASK})
    v["E1.a1"] = rol(v["E1.d1"], 16) ^ v["Y12"]
    v["Y6"] = (v["E1.a1"] - v["Y1"] - v["w12"]) & MASK
    v["Y10"] = rol(v["Y6"], 7) ^ v["C2.b1"]
    v["Y14"] = (v["Y10"] - v["C2.c1"]) & MASK
    v["E1.b1"] = ror(v["Y6"] ^ c1, 12)
    v["Y2"] = rol(v["Y14"], 8) ^ v["C2.d1"]
    v["E3.h1"] = ror(v["Y14"] ^ ((Y3 + v["Y4"]) & MASK), 16)
    v["w0"] = (v["Y2"] - v["C2.a1"] - v["C2.b1"]) & MASK
    v["E3.g1"] = (v["Y9"] + v["E3.h1"]) & MASK
    v["K0.a1"] = (IV[0] + IV[4] + v["w0"]) & MASK
    v["E3.f1"] = ror(v["Y4"] ^ v["E3.g1"], 12)
    v["T0"] = rol(v["K0.d1"], 16) ^ v["K0.a1"]
    v["w1"] = (v["S0"] - v["K0.a1"] - v["K0.b1"]) & MASK
    v["E1.a2"] = (v["E1.a1"] + v["E1.b1"] + v["w5"]) & MASK
    v["E3.e2"] = (Y3 + v["Y4"] + v["E3.f1"] + v["w8"]) & MASK
    if v["T0"] == 0:
        return None
    w = [v.get("w%d" % i, 0) for i in range(16)]
    w[4], w[13] = W4, W13
    b = list(w)
    b[4], b[5] = W4B, (w[5] + DELTA5) & MASK
    return struct.pack("<16I", *w), struct.pack("<16I", *b), v["T0"], v
def ctr_lane(o, c1):
    'One counter trial against the 2-round compressions of its two last chunks (counter t, flags 3): its checks and h1.'
    r = ctr_trial(o, c1)
    if r is None:
        return False, None
    a, b, t, v = r
    (wa, da, ya), (wb, db, yb) = compress2(a[:LEN_A], t, CTR_FLAGS), compress2(b[:LEN_B], t, CTR_FLAGS)
    e = []
    for w, y in ((wa, ya), (wb, yb)):
        c = (y[11] + ror(y[12] ^ ((y[1] + y[6] + w[12]) & MASK), 16)) & MASK
        e.append((c, ror(y[6] ^ c, 12), (y[3] + y[4] + w[15]) & MASK))
    h1 = ror(ya[14] ^ e[0][2], 16)
    good = (all(ya[i] == v["Y%d" % i] for i in (0, 1, 2, 4, 5, 6, 8, 9, 10, 12, 13, 14))
            and (ya[3], ya[11], yb[3], yb[11], yb[4], e[0][1], h1) == (Y3, Y11, Y3B, Y11B, v["Y4"], v["E1.b1"], v["E3.h1"])
            and wa == list(struct.unpack("<16I", a)) and wb == list(struct.unpack("<16I", b)) and t >> 32 == 0
            and all(da[i] == db[i] for i in (0, 2, 5, 7)) and e[0][2] & CTR_CLASS == CLASS_VALUE & CTR_CLASS
            and e[0][0] == c1 and c1 & CTR_MASK == CTR_VALUE and e[0][1] ^ e[1][1] == CTR_BETA
            and ror(e[0][2] ^ e[1][2], 16) == ETA)
    return good, h1
def ctr_g(tau):
    "G(tau) = ROL(tau ^ ROR(tau, 1), 12): the difference g1 ^ g1' that R = 0 with outcome tau needs (condition (1))."
    return rol(tau ^ ror(tau, 1), 12)
def ctr_automaton(targets, dy, n=32):
    """The carry automaton of outer_filter.py on the n low bits of a word x, as byte tables. Target i = (dz, out) holds
    when some v gives (x + v) ^ (x' + (v ^ dz)) = out, x' = x + dy: condition (1) on Q (dy = 0, dz = eta, out = G) or (2)
    on E (dy = DY3, dz = ROR(G, 12), out = eps). A state is the carry of x + dy and, per target, the set of reachable
    carry pairs (4 bits); tables[p][s + byte p] is the next state times 256, the last table gives the pattern."""
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
CTR_FILTER = []
def ctr_tables():
    """The filter's two automata for the seven outcomes, built once per run on first use, with every entry of their last
    tables ANDed with S (proof.md Section 8): (1) on Q = Y9, (2) on E = omega with E' = E + DY3."""
    if not CTR_FILTER:
        g = [ctr_g(t) for t in CTR_TAUS]
        for tables in (ctr_automaton([(ETA, x) for x in g], 0),
                       ctr_automaton([(ror(x, 12), CTR_EPS) for x in g], (Y3B - Y3) & MASK)):
            tables[-1] = [x & S_MASK for x in tables[-1]]
            CTR_FILTER.append(tables)
    return CTR_FILTER
def ctr_look(tables, x):
    'The automaton on the word x, a byte at a time, one table load per byte; the last table gives the pattern.'
    for p, t in enumerate(tables):
        b = x >> 8 * p if p else x
        b = b if p == 3 else b & 255
        i = s + b if p else b
        s = Word.m.load(t[i]) if type(x) is Word else t[i]
    return s
def ctr_filter(q, y4, w8):
    'The filter of one outer step: the outcomes of S (bits of 5f) with (1) solvable for Q = Y9 and (2) for E = omega.'
    fq, fe = ctr_tables()
    return ctr_look(fq, q) & ctr_look(fe, (Y3 + y4 + w8) & MASK)
class Cnt:
    """The machine of proof.md Section 11: one unit for every executed primitive (operation, load, store, comparison,
    branch, random word); constant operands and shift distances are instruction fields; 64 registers. Parts are counted
    separately; Word values record when they are made and last read, for the register count."""
    def __init__(s):
        s.units, s.part, s.t, s.vals = {}, None, 0, []
    def at(s, part):
        s.part = part
        s.units.setdefault(part, 0)
    def tick(s, n=1):
        s.units[s.part] += n
    def new(s, z):
        s.t += 1
        w = Word(z)
        w.b = w.l = s.t
        s.vals.append(w)
        return w
    def load(s, z):
        s.tick()
        return s.new(z)
    def branch(s, *used):
        'A comparison and the branch on it: two units.'
        s.tick(2)
        s.t += 1
        for w in used:
            if type(w) is Word:
                w.l = s.t
    def registers(s):
        change = [0] * (s.t + 2)
        for w in s.vals:
            change[w.b] += 1
            change[w.l + 1] -= 1
        held = peak = 0
        for d in change:
            held += d
            peak = max(peak, held)
        return peak
class Word(int):
    'A scalar word whose operations are counted on Word.m, one unit each; an int operand is an immediate.'
    m = None
    def c(s, o, z):
        m = Word.m
        m.tick()
        w = m.new(z)
        s.l = w.b
        if type(o) is Word:
            o.l = w.b
        return w
    __add__ = __radd__ = lambda s, o: s.c(o, int(s) + int(o))
    __sub__ = lambda s, o: s.c(o, int(s) - int(o))
    __rsub__ = lambda s, o: s.c(o, int(o) - int(s))
    __xor__ = __rxor__ = lambda s, o: s.c(o, int(s) ^ int(o))
    __or__ = __ror__ = lambda s, o: s.c(o, int(s) | int(o))
    __and__ = __rand__ = lambda s, o: s.c(o, int(s) & int(o))
    __rshift__ = lambda s, o: s.c(o, int(s) >> o)
    __lshift__ = lambda s, o: s.c(o, int(s) << o)
CTR_MEMBER_TABLE = {}
def ctr_member(k):
    'Y4 of class member number k (19 bits): the bits of k fill the free positions of e1 = Y3 + Y4 in increasing order.'
    if k not in CTR_MEMBER_TABLE:
        e1 = CLASS_VALUE & CTR_CLASS
        for n, i in enumerate(CTR_CFREE):
            e1 |= (k >> n & 1) << i
        CTR_MEMBER_TABLE[k] = (e1 - Y3) & MASK
    return CTR_MEMBER_TABLE[k]
def ctr_eight(r):
    'The eight 32-bit words of a random 256-bit word: seven outer words (CTR_BASIS) and the member number (19 bits).'
    return [r >> 32 * i & MASK for i in range(7)] + [r >> 224 & CTR_CSIZE - 1]
def ctr_count(r):
    """One outer step on scalar words, counted on the machine: the random word, its eight words, the member's Y4 (one
    load), all 77 lines of step CO as ctr_outer computes them, the filter (omega and two automata, one load per byte)
    and the test of its mask (the scalar count behind the passing lane's rebuild, proof.md 9.8 and Section 11).
    Returns (machine, values of step CO, mask)."""
    m = Word.m = Cnt()
    m.at("outer step")
    w = m.load(r)
    eight = [w & MASK] + [w >> 32 * i & MASK for i in range(1, 7)] + [w >> 224 & CTR_CSIZE - 1]
    y4 = m.load(ctr_member(int(eight[7])))
    o = ctr_outer(eight, y4)
    m.at("filter")
    z = ctr_filter(o["Y9"], o["Y4"], o["w8"])
    m.branch(z)
    return m, o, int(z)
# == the exact E3 solver of proof.md 8.4 (Lemma E3) ==
DY3 = (Y3B - Y3) & MASK
def ctr_inverse(o, h1):
    'Lemma IP read backwards: the c1 of the outer step o whose trial has E3.h1 = h1 (step 3 of proof.md 9.1).'
    y14 = rol(h1, 16) ^ ((Y3 + o["Y4"]) & MASK)
    y6 = ror(((y14 + o["C2.c1"]) & MASK) ^ o["C2.b1"], 7)
    return (ror(((y6 + o["Y1"] + o["w12"]) & MASK) ^ o["Y12"], 16) + Y11) & MASK
def ctr_r(text):
    return int.from_bytes(hashlib.shake_256(text.encode()).digest(32), "little")
# == v110: the walk of proof.md 9.8 and 9.9 (contexts, representative batches, the straddle gate, the byte guard and
# the masked partner walk with its two chunks under one joint dispatch), executed on the counted packed machine and
# checked against step CO ==
LANE_BITS = 36
LANE = (1 << LANE_BITS) - 1
def spread(x):
    'The value x (below 2^36) in all seven 36-bit lanes of a packed word.'
    return sum(x << LANE_BITS * i for i in range(7))
M_ALL = spread(MASK)
def lane(z, i):
    return int(z) >> LANE_BITS * i & LANE
class Bound:
    'An exclusive upper bound on every lane of a packed value, carried through the lines (Lemma MB).'
    seen = []
    def __init__(s, b):
        s.b = b
        Bound.seen.append(b)
    def __add__(s, o):
        return Bound(s.b + (o.b if type(o) is Bound else (o & LANE) + 1) - 1)
    def __xor__(s, o):
        return Bound(1 << (max(s.b, o.b if type(o) is Bound else (o & LANE) + 1) - 1).bit_length())
    __radd__, __rxor__ = __add__, __xor__
def pror(z, r):
    'PROR of proof.md 6.5: every lane rotated right by r, five operations; its result is below 2^32 in every lane.'
    if type(z) is Bound:
        return Bound(1 << 32)
    return ((z >> r) & spread((1 << 32 - r) - 1)) | ((z << 32 - r) & spread(((1 << r) - 1) << 32 - r))
class Run(Cnt):
    'The counted machine of Section 11 without the register bookkeeping (the walk keeps no history of values).'
    def new(s, z):
        w = Word(z)
        w.b = w.l = 0
        return w
S7 = frozenset(list(range(0x25, 0x3F)) + list(range(0x45, 0x5F)))
LW = (0xE000001F, 0xF000001F)
R7, YM, EM = spread(0x7F), spread(0xFF00), spread(3 << 20)
N1, N2, N4, N8 = spread(1), spread(2), spread(4), spread(8)
GATE_BASE, T1_BASE = 1 << 35, 1 << 34
REP_BATCHES = -(-16384 // 7)
OLD_BATCHES = ((1, 8), (8, 15), (15, 22), (22, 29), (29, 32))
def rep_number(g):
    'The member number of the representative of cluster g: g fills the 14 free positions of e1 other than 10 to 14.'
    return (g & 63) | (g >> 6) << 11
def cluster_member(g, j):
    'Member j of cluster g, j = 0 the representative: e1 = e_g + 2^10 j (bits 6 to 10 of the member number).'
    return ctr_member(rep_number(g) | j << 6)
def t2(x):
    'The entry of T2 (Lemma DT): the mask of (2) on the word x, restricted to S.'
    return ctr_look(ctr_tables()[1], x)
def t1(x):
    return ctr_look(ctr_tables()[0], x)
def gate_entry(key):
    """The gate table at word address key = 2^35 + w + 2^8 m + 2^16 h + 2^20 i + 2^22 a (9.9), computed on demand by the
    rule that fills it: 1 when w mod 128 lies in S7, or when m = a and bit i of h is 1."""
    if not GATE_BASE <= key < GATE_BASE + (1 << 30):
        raise ValueError("gate address out of its table")
    k = key - GATE_BASE
    w, m, h, i, a = k & 127, k >> 8 & 255, k >> 16 & 15, k >> 20 & 3, k >> 22
    return int(w in S7 or (m == a and h >> i & 1 == 1))
def hbad(b, c, d, a):
    'The four flags hbad_i of a context (9.9) as Hbad = sum 2^i hbad_i.'
    h = 0
    for i, ti in enumerate((0xF2, 0xFA, 0x02, 0x0A)):
        hh = ((ti ^ b >> 24) - (c >> 24)) & 255
        lo0, lo1 = hh ^ d & 255, ((hh - 1) & 255) ^ d & 255
        h |= (min(lo0, lo1) < (a & 255) <= max(lo0, lo1)) << i
    return h
def v110_context(seven):
    """A context (proof.md 9.8): step CO for its seven outer words (the 39 lines of Lemma Y read no member; y = 0 here),
    the sixteen packed operands, the four flags and the gate base BG6, A[8..15], and the descriptor table of the masked
    walk with its case words (9.9)."""
    o = ctr_outer(list(seven) + [0], 0)
    w = {"C0.b1": o["C0.b1"], "-C0.c1": -o["C0.c1"], "C0.d1": o["C0.d1"],
         "K'": -o["C0.b1"] - o["w6"] - o["X4"] - o["w2"], "S15'": o["S15"] ^ ror(X15, 8),
         "-S0-S5": -o["S0"] - o["S5"], "-C0.b1-w6": -o["C0.b1"] - o["w6"], "ROL(C0.d1,16)": rol(o["C0.d1"], 16),
         "K": X11 + 1 - o["S11"], "S12": o["S12"], "-S1-S6": -o["S1"] - o["S6"], "S10": o["S10"],
         "S5": o["S5"], "w3": o["w3"], "X13": o["X13"]}
    w = {k: v & MASK for k, v in w.items()}
    c = {k: spread(v) for k, v in w.items()}
    c["X9'"] = spread(o["X9"] + T1_BASE)
    c["ROL(X15,8)"], c["X15"] = spread(rol(X15, 8)), spread(X15)
    a = (-w["K'"]) & MASK
    c["Hbad"] = hbad(o["C0.b1"], o["C0.c1"], o["C0.d1"], a)
    c["A8"] = a >> 8 & 255
    c["BG6"] = spread(GATE_BASE + (c["Hbad"] << 16) + (c["A8"] << 22))
    return o, w, c, v110_descriptors(w)
def window(w, ix, j):
    'o(IX, j) of Lemma XF: bits 9 to 13 of the omega of member j of a cluster with carries IX (all modulo 32).'
    c17, c25, c9a, c9b = ix & 1, ix >> 1 & 1, ix >> 2 & 1, ix >> 3 & 1
    v = ((16 + j) ^ (w["C0.b1"] >> 17)) + (w["-C0.c1"] >> 17) + c17
    v = (v ^ (w["C0.d1"] >> 25)) + (w["K'"] >> 25) + c25
    v = (v ^ (w["S15'"] >> 9)) + (w["-S0-S5"] >> 9) + c9a
    return (v + 1 + 2 * (j % 16) + c9b) & 31
def v110_descriptors(w):
    """The descriptor table of a context (9.9): for each IX and b8 (with omega mod 128 in S7) the survivors of Lemma XF (c)
    in two chunks as in (d), the chunk that holds the least survivor first, and the case word k of (n0, n1):
    {index: ((n0, JU0, JE0, js0), (n1, JU1, JE1, js1), k)}; the other 96 indices hold the case word of (0, 0)."""
    table = {}
    for ix in range(16):
        for b8 in (0, 1):
            surv = [j for j in range(1, 32) if LW[b8] >> window(w, ix, j) & 1]
            olds = [[j for j in surv if lo <= j < hi] for lo, hi in OLD_BATCHES]
            a = max(range(5), key=lambda k: (len(olds[k]), -k))
            chunks = [olds[a], [j for j in surv if j not in olds[a]]]
            chunks.sort(key=lambda ch: ch[0] if ch else 99)
            d = tuple((len(ch), sum(j << LANE_BITS * t + 17 for t, j in enumerate(ch)),
                       sum(j << LANE_BITS * t + 10 for t, j in enumerate(ch)), tuple(ch)) for ch in chunks)
            table[2 * ix + 32 * b8 + 64] = d + (CASE[d[0][0], d[1][0]],)
    return table
def px(w9):
    'The table PX of 9.9 at w = omega mod 512: 32 (bit 8 of w) + 64 [w mod 128 in S7].'
    return 32 * (w9 >> 8 & 1) + 64 * ((w9 & 127) in S7)
U_CONTEXT_WALK, U_FLAGS, U_DESCRIPTORS, U_CARRY, U_CTX_SETUP = 547, 160, 50000, 20, 16
U_REP, U_REP_TAIL, U_E, U_FILL, U_PASS = 59, 45, 7, 56, 53
U_REP_T2, U_W, U_GUARD, U_SEL, U_BCAST, U_JUJE, U_END, U_BOOK_OLD = 5, 1, 4, 11, 16, 6, 1, 21
def chunk_units(n):
    'A batch of n lanes (9.8): the omega side, 17, and its lane tests, 4 + 5 (n - 1) for n < 7 and 33 for 7.'
    return 0 if n == 0 else 17 + (33 if n == 7 else 4 + 5 * (n - 1))
# The cases (n0, n1) of a descriptor: no survivor, or 1 <= n0 <= 7, 0 <= n1 <= 7, n0 + n1 <= 9 (Lemma XF (c), (d)).
CASES = [(0, 0)] + [(a, b) for a in range(1, 8) for b in range(8) if a + b <= 9]
def case_base(a, b):
    """The units of an opened cluster (not a fallback) in case (a, b), without its dispatch: the addition to W, the
    representative's lane test, the byte guard, the selection up to the load of the case word, and, when a partner
    survives, the broadcasts and, for each used chunk, JU and JE, its omega side and lane tests and the jump at its end;
    with no survivor, the jump to the next gate test."""
    u = U_W + U_REP_T2 + U_GUARD + U_SEL
    if not a:
        return u + U_END
    return u + U_BCAST + sum(U_JUJE + chunk_units(n) + U_END for n in (a, b) if n)
U_OPEN, CASE_LMAX = 134, 10
CASE_LEN = {ab: min((U_OPEN - case_base(*ab)) // 2, CASE_LMAX) for ab in CASES}
def canonical(lengths, lmax):
    'Canonical prefix code for the given lengths, each code word left-aligned to lmax bits: {key: k}.'
    code, prev, out = 0, None, {}
    for key in sorted(lengths, key=lambda x: (lengths[x], x)):
        l = lengths[key]
        code = 0 if prev is None else (code + 1) << (l - prev)
        prev = l
        out[key] = code << (lmax - l)
    return out
CASE = canonical(CASE_LEN, CASE_LMAX)
def case_tree(lo, hi, keys):
    'The comparison tree on the case word over [lo, hi): a leaf (a, b), or (mid, below, at or above).'
    if len(keys) == 1:
        return keys[0]
    mid = (lo + hi) // 2
    below, above = [x for x in keys if CASE[x] < mid], [x for x in keys if CASE[x] >= mid]
    if not below:
        return case_tree(mid, hi, above)
    if not above:
        return case_tree(lo, mid, below)
    return (mid, case_tree(lo, mid, below), case_tree(mid, hi, above))
CASE_TREE = case_tree(0, 1 << CASE_LMAX, sorted(CASES, key=CASE.get))
def case_depths(node=CASE_TREE, d=0, out=None):
    out = {} if out is None else out
    if len(node) == 3:
        case_depths(node[1], d + 1, out)
        case_depths(node[2], d + 1, out)
    else:
        out[node] = d
    return out
CASE_DEPTH = case_depths()
U_FALLBACK = U_REP_T2 + U_BOOK_OLD + 4 * 50 + 31 + U_GUARD
U_CONTEXT = (U_CONTEXT_WALK + U_FLAGS + U_DESCRIPTORS + U_CARRY * REP_BATCHES + U_CTX_SETUP
             + 128 * (U_FALLBACK - U_OPEN))
class Walk:
    'One context walked on the counted machine: counts, work register W and the events of each cluster.'
    def __init__(s, seven):
        s.seven = list(seven)
        s.o, s.w, s.c, s.desc = v110_context(seven)
        s.m = Word.m = Run()
        s.m.at("context")
        s.W = Word(0)
        s.ev = {"clusters": 0, "opened": 0, "fallbacks": 0, "walked": 0, "e_lanes": 0, "fills": 0, "passes": 0}
        s.fired = set()
        s.lanes = []          # (member y, cluster, j, lane omega, mask of (2), Y9 lane or None, X or None)
        s.units = {"rep": set(), "open": [], "fallback": [], "E lane": set(), "fill": set()}
    def batch(s, u, e, n, g_of, js, cache):
        """The omega side of a batch from its U and E (17), then its lane tests (n lanes), with the E handler, the fill
        and the passing lane of each E lane (9.8). Returns (Y0, X0, Y12, Y8, D0a1, cg, om)."""
        m, c = s.m, s.c
        y8 = u ^ c["C0.b1"]
        y12 = y8 + c["-C0.c1"]
        y0 = pror(y12, 24) ^ c["C0.d1"]
        x0 = y0 + c["K'"]
        d0a1 = pror(x0, 16) ^ c["S15'"]
        cg = e + c["-S0-S5"]
        om = d0a1 + cg
        for i in range(n):
            s.lane_test(om, i, y0, x0, cache, g_of(i), js[i])
        return y0, x0, y12, y8, d0a1, cg, om
    def lane_test(s, om, i, y0, x0, cache, g, j):
        m = s.m
        part = m.part
        x = om if i == 0 else om >> LANE_BITS * i
        if i < 6:
            x = x & LANE
        if not int(x) < 3 << 32:
            raise ValueError("T2' address out of its table")
        m2 = m.load(t2(int(x) & MASK))
        m.branch(m2)
        s.ev["walked"] += 1
        rec = [g, j, int(x), int(m2), None, None]
        if m2:
            s.e_lane(i, int(m2), y0, x0, cache, rec)
            m.at(part)
        s.lanes.append(rec)
    def e_lane(s, i, m2, y0, x0, cache, rec):
        m, c = s.m, s.c
        s.ev["e_lanes"] += 1
        if "y9" not in cache:
            m.at("fill")
            f0 = m.units["fill"]
            s.W = s.W + (U_E + U_FILL)
            s.ev["fills"] += 1
            c0a1 = y0 + c["-C0.b1-w6"]
            d0d1 = x0 ^ c["ROL(X15,8)"]
            x12 = c0a1 ^ c["ROL(C0.d1,16)"]
            d1d1 = (x12 ^ M_ALL) + c["K"]
            x1 = pror(x12, 24) ^ d1d1
            w10 = (pror(d1d1, 16) ^ c["S12"]) + c["-S1-S6"]
            d0c1 = d0d1 + c["S10"]
            x5 = pror(pror(c["S5"] ^ d0c1, 12) ^ (d0c1 + c["X15"]), 7)
            c1a1 = x1 + x5 + c["w3"]
            c1d1 = pror(c["X13"] ^ c1a1, 16)
            c1c1 = c["X9'"] + c1d1
            y1 = c1a1 + pror(x5 ^ c1c1, 12) + w10
            cache["y9"] = c1c1 + pror(c1d1 ^ y1, 8)
            s.units["fill"].add(m.units["fill"] - f0 - 1)
            m.at("E lane")
            e0 = m.units["E lane"] - 1
        else:
            m.at("E lane")
            e0 = m.units["E lane"]
            s.W = s.W + U_E
        y = cache["y9"] if i == 0 else cache["y9"] >> LANE_BITS * i
        y = y & (T1_BASE + MASK)
        if not T1_BASE <= int(y) < T1_BASE + (1 << 32):
            raise ValueError("T1 address out of its table")
        mk = m.load(t1(int(y) - T1_BASE)) & m2
        m.branch(mk)
        s.units["E lane"].add(m.units["E lane"] - e0)
        rec[4], rec[5] = int(y) - T1_BASE, int(mk)
        if mk:
            s.ev["passes"] += 1
    def rep_batch(s, b):
        """Representative batch b (9.9): the pair, the omega side, the key, the carry word (paid by the context) and the gate
        test of each used lane, each opened cluster walked before the next gate test."""
        m, c = s.m, s.c
        n = 7 if b < REP_BATCHES - 1 else 16384 - 7 * (REP_BATCHES - 1)
        gs = [7 * b + min(i, n - 1) for i in range(7)]
        ys = [cluster_member(g, 0) for g in gs]
        m.at("rep")
        r0 = m.units["rep"]
        u = m.load(sum(rol(y, 7) << LANE_BITS * i for i, y in enumerate(ys)))
        m.tick()
        e = m.load(sum(((Y3 + y) & MASK) << LANE_BITS * i for i, y in enumerate(ys)))
        y8 = u ^ c["C0.b1"]
        y12 = y8 + c["-C0.c1"]
        y0 = pror(y12, 24) ^ c["C0.d1"]
        x0 = y0 + c["K'"]
        d0a1 = pror(x0, 16) ^ c["S15'"]
        cg = e + c["-S0-S5"]
        om = d0a1 + cg
        key = (om & R7) | (y0 & YM) | (e & EM) | c["BG6"]
        m.at("context")
        w8 = d0a1 + c["-S0-S5"]
        ix = ((((y12 ^ y8 ^ c["-C0.c1"]) >> 17) & N1) | (((x0 ^ y0 ^ c["K'"]) >> 24) & N2)
              | (((w8 ^ d0a1 ^ c["-S0-S5"]) >> 7) & N4) | (((om ^ e ^ w8) >> 6) & N8))
        cache = {}
        rep_units = m.units["rep"] - r0
        for i in range(n):
            m.at("rep")
            r1 = m.units["rep"]
            k = key if i == 0 else key >> LANE_BITS * i
            if i < 6:
                k = k & LANE
            entry = m.load(gate_entry(int(k)))
            m.branch(entry)
            rep_units += m.units["rep"] - r1
            s.ev["clusters"] += 1
            if entry:
                s.open_cluster(gs[i], i, u, e, y0, x0, om, ix, cache)
            else:
                s.lanes.append([gs[i], None, None, 0, None, None])
        s.units["rep"].add((n, rep_units))
    def open_cluster(s, g, i, u, e, y0, x0, om, ix, cache):
        m, c = s.m, s.c
        s.ev["opened"] += 1
        m.at("open")
        o0 = m.units["open"]
        s.W = s.W + U_OPEN
        s.lane_test(om, i, y0, x0, cache, g, 0)
        fire = (y0 >> LANE_BITS * i + 8) & 255
        m.branch(fire)
        if int(fire) == c["A8"]:
            s.ev["fallbacks"] += 1
            s.fired.add(g)
            m.at("fallback")
            f0 = m.units["fallback"]
            m.tick(U_BOOK_OLD - 1)                  # the address, ten loads and nine increments of the old pairs
            for lo, hi in OLD_BATCHES:
                ys = [cluster_member(g, j) for j in range(lo, hi)] + [cluster_member(g, hi - 1)] * (7 - hi + lo)
                uu = Word(sum(rol(y, 7) << LANE_BITS * t for t, y in enumerate(ys)))
                ee = Word(sum(((Y3 + y) & MASK) << LANE_BITS * t for t, y in enumerate(ys)))
                s.batch(uu, ee, hi - lo, lambda t: g, list(range(lo, hi)), {})
            s.units["fallback"].append(m.units["open"] - o0 + m.units["fallback"] - f0)
            return
        ixl = ix if i == 0 else ix >> LANE_BITS * i
        ixl = ixl & 15
        w9 = om if i == 0 else om >> LANE_BITS * i
        w9 = w9 & 511
        m.tick()                                      # the address of PX[w9]
        p = m.load(px(int(w9)))
        idx = (ixl << 1) | p
        m.tick(2)                                     # the descriptor address DB + 8 idx: a shift and an addition
        d = s.desc.get(int(idx), ((0, 0, 0, ()), (0, 0, 0, ()), CASE[0, 0]))
        k = m.load(d[2])                              # the case word
        node = CASE_TREE
        while len(node) == 3:                         # the comparison tree: k < mid and the branch, two units a node
            m.branch(k)
            node = node[1] if int(k) < node[0] else node[2]
        if node != (d[0][0], d[1][0]):
            raise ValueError("case word and descriptor disagree")
        chunks = []
        if node[0]:
            ub = u if i == 0 else u >> LANE_BITS * i
            ub = ub & MASK
            eb = e if i == 0 else e >> LANE_BITS * i
            eb = eb & MASK
            for _ in range(2):
                ub = ub | (ub << LANE_BITS * (1 if _ == 0 else 2))
                eb = eb | (eb << LANE_BITS * (1 if _ == 0 else 2))
            ub = ub | (ub << LANE_BITS * 3)
            eb = eb | (eb << LANE_BITS * 3)
            for n, ju, je, js in d[:2]:               # the leaf: chunk 1, then chunk 2 written out after it
                if not n:
                    break
                m.at("open")
                m.tick()
                uu = ub + m.load(ju)
                m.tick()
                ee = eb + m.load(je)
                s.batch(uu, ee, n, lambda t: g, list(js), {})
                m.at("open")
                m.tick()                              # the jump at the end of the chunk
                chunks.append(n)
        else:
            m.tick()                                  # no survivor: the jump to the next gate test
        units = m.units["open"] - o0
        s.units["open"].append((tuple(chunks), units))
def v110_walk(seven, batches):
    """Walk the given representative batches of the context of seven outer words and check every member of every
    cluster they hold against step CO, test (2) and the filter bit by bit. Returns (Walk, checks, mismatches,
    skipped passes)."""
    s = Walk(seven)
    for b in batches:
        s.rep_batch(b)
    seen = {}
    for g, j, x, m2, y9, mk in s.lanes:
        if j is not None:
            seen[g, j] = (x, m2, y9, mk)
    checks = bad = skipped = 0
    w, d = s.w, s.desc
    for g in sorted({r[0] for r in s.lanes}):
        rep = None
        for j in range(32):
            y = cluster_member(g, j)
            v = ctr_outer(s.seven + [0], y)
            omega = (Y3 + y + v["w8"]) & MASK
            m2 = t2(omega)
            mk = ctr_filter(v["Y9"], y, v["w8"])
            if j == 0:
                rep = (v, omega)
                x0 = v["X0"]
                l_word = rol(X15, 24) ^ v["S15"]
                cc = (Y3 + y - v["S0"] - v["S5"]) & MASK
                p0 = v["Y0"]
                uu = ((p0 >> 16 & 511) - (((-w["K'"]) & MASK) >> 16 & 511)) % 512
                prefixes = {(cc + (((uu - l) % 512) ^ (l_word & 511))) % 512 for l in (0, 1)}
                e1 = (Y3 + y) & MASK
                key = (GATE_BASE + (omega & 127) + (p0 & 0xFF00) + (s.c["Hbad"] << 16) + (e1 & 3 << 20)
                       + (s.c["A8"] << 22))
                fire = (p0 >> 8 & 255) == s.c["A8"]
                straddle = fire and s.c["Hbad"] >> (e1 >> 20 & 3) & 1 == 1
                ix = (((((v["Y8"] - v["C0.c1"]) & MASK) ^ v["Y8"] ^ (-v["C0.c1"] & MASK)) >> 17 & 1)
                      | (((((v["Y0"] + w["K'"]) & MASK) ^ v["Y0"] ^ w["K'"]) >> 25 & 1) << 1)
                      | (((v["w8"] ^ v["D0.a1"] ^ w["-S0-S5"]) >> 9 & 1) << 2)
                      | (((omega ^ ((Y3 + y) & MASK) ^ v["w8"]) >> 9 & 1) << 3))
                surv = None
                if not fire and (omega & 127) in S7:
                    ch = d[2 * ix + 32 * (omega >> 8 & 1) + 64]
                    surv = set(ch[0][3]) | set(ch[1][3])
                opened = (g, 0) in seen
                checks += 2
                bad += opened != bool(gate_entry(key)) or gate_entry(key) != int((omega & 127) in S7 or straddle)
                bad += opened and fire != (g in s.fired)
            checks += 1
            bad += (omega & 511) not in prefixes or (not straddle and (omega & 511) != (rep[1] & 511))
            if not fire and j:
                checks += 1
                bad += (omega >> 9 & 31) != window(w, ix, j)
            if (g, j) in seen:
                x, n2, y9, k = seen[g, j]
                checks += 1
                bad += (x & MASK, n2, k if n2 else None) != (omega, m2, mk if m2 else None) or (n2 and y9 != v["Y9"])
            elif m2:
                skipped += 1
            if (g, j) not in seen and opened and not fire and j and surv is not None and j in surv:
                bad += 1
    return s, checks, bad, skipped
# == the charge of proof.md Section 11 ==
ONCE_070 = ((1 << 38) + (1 << 26) + (1 << 20) + (1 << 20) + 4 * (1 << 26) + (1 << 50) + 40 + 12 * (1 << 20) + (1 << 27)
        + (1 << 34) + 3 * (1 << 20) + 14 * (1 << 20) + (1 << 36) + 2 * (1 << 22) + (1 << 38) + (1 << 41) + (1 << 34)
        + (1 << 28) + (1 << 20))
# v110: one more allowance of 2^40 for writing out the larger code of the joint dispatch (proof.md 12)
ONCE = ONCE_070 + (1 << 40)
S_OLD = 116 * 5 * (1 << 53) + 116 * ((1 << 51) + (1 << 10)) + (1 << 50)
FINAL = 1 << 38
def ledger(u_open=None, u_context=None, once=None):
    """430 T = the rows of Section 11 + S_old + 430 * 2^38, with u_O and the context's units (v110 by default; 144 and
    112,519 give the row of entry 070a02b2). Returns a dict with the exact integers and the claim, rounded up at the
    fifth decimal and checked in integers: 2^(claim - 1e-5) < T < 2^claim, as (430 T)^100000 against 430^100000."""
    u_open = U_OPEN if u_open is None else u_open
    u_context = U_CONTEXT if u_context is None else u_context
    once = ONCE if once is None else once
    wb = u_open * A_BUDGET + U_E * E_BUDGET + U_FILL * G_BUDGET + U_PASS * PASS_BUDGET
    w_ctx = 16384 * u_open + (U_E << 19) + 84261 * U_FILL + (U_PASS << 19)
    rep = (U_REP * REP_BATCHES - (U_REP - U_REP_TAIL)) * RUN_CONTEXTS
    rows = u_context * (RUN_CONTEXTS + 1) + rep + wb + w_ctx + CREDIT + once
    n = rows + S_OLD + 430 * FINAL
    lg = math.log2(n) - math.log2(430)
    claim = math.ceil(lg * 1e5)
    p, q = n ** 100000, 430 ** 100000
    return {"u_open": u_open, "u_context": u_context, "WB": wb, "W_CTX": w_ctx, "rows": rows, "N_430T": n,
            "time_log2": round(lg, 11), "claim": claim / 1e5, "claim_exact": q << claim - 1 < p < q << claim,
            "search_only_log2": round(math.log2(rows + 430 * FINAL) - math.log2(430), 8)}
CONSTANTS_070 = {"FACTOR": 125920632087, "RUN_STEPS_MIN": 639060516044734036987, "RUN_CONTEXTS": 1218911201562375,
                 "RESERVE_S": 110404312, "A_BUDGET": 8114703155646753044, "E_BUDGET": 34776155800492855966,
                 "G_BUDGET": 15194956341454300182, "PASS_BUDGET": 633770615067648623, "M_0": 844906655693766489106,
                 "M_C": 829292364315442262408, "CREDIT": 829308674569081960042, "ONCE_070": 1128752545267752,
                 "S_OLD": 5486510246044225536}
# == the organizer experiment ==
def walk_seed(seed):
    'The context and the representative batches of one organizer trial: four consecutive batches and the last.'
    z = int.from_bytes(hashlib.shake_256(b"v110 cluster-walk " + seed).digest(36), "little")
    b0 = (z >> 224) % (REP_BATCHES - 4)
    return [z >> 32 * i & MASK for i in range(7)], [b0, b0 + 1, b0 + 2, b0 + 3, REP_BATCHES - 1]
def walk_report(s, checks, bad, skipped):
    'The observations of a walk and the unit checks against the charges of Section 11.'
    u = s.units
    over = sum(x > U_OPEN for _, x in u["open"]) + sum(x > U_FALLBACK for x in u["fallback"])
    over += sum(x != {7: U_REP, 4: U_REP_TAIL}.get(n) for n, x in u["rep"])
    over += sum(x > U_E for x in u["E lane"]) + sum(x != U_FILL for x in u["fill"])
    lanes = [sum(ch) for ch, _ in u["open"]]
    return dict(s.ev, checks=checks, mismatches=bad + over, skipped_pass=skipped,
                open_units_max=max([x for _, x in u["open"]], default=0),
                chunk_lanes_max=max(lanes, default=0), work=int(s.W))
def cluster_walk(seed):
    seven, batches = walk_seed(seed)
    s, checks, bad, skipped = v110_walk(seven, batches)
    first, second, _ = half_collision(seed)
    return first, second, walk_report(s, checks, bad, skipped)
# == the self-test (proof.md 9.3) ==
def v110_selftest(cases, seed):
    rep, good = {}, True
    # (1) counter trials against the compressions of their last chunks (and the organizer's _compress if present)
    try:
        sys.path.insert(0, "verifier")
        import blake3 as organizer
    except ImportError:
        organizer = None
    right = same_c1 = org = 0
    for case in range(cases):
        r = ctr_r("halfsearch v110 trial %s %d" % (seed, case))
        e = ctr_eight(r)
        if case % 5 == 4:
            e[:7] = [(0, MASK, x, x)[r >> 2 * i & 3] for i, x in enumerate(e[:7])]
        o = ctr_outer(e)
        c1 = ctr_c1(r >> 240 & CTR_MEMBERS - 1)
        ok, h1 = ctr_lane(o, c1)
        if h1 is None:
            continue
        right += ok
        same_c1 += ctr_inverse(o, h1) == c1
        if organizer and case % 25 == 0:
            a, b, t, v = ctr_trial(o, c1)
            wa, da, ya = compress2(a[:LEN_A], t, CTR_FLAGS)
            org += list(organizer._compress(IV, wa, t, LEN_A, CTR_FLAGS, 2)[:8]) == da
    rep["trials"] = {"cases": cases, "right": right, "inverse_right": same_c1,
                     "organizer_compress": org if organizer else "verifier not found"}
    good &= right == same_c1 and right > 0.99 * cases and (not organizer or org == -(-cases // 25))
    # (2) the filter: brute force at width 10, SHARE and E_COUNT recounted from the tables (Section 8)
    fq, fe = ctr_tables()
    gs, ok = [ctr_g(t) for t in CTR_TAUS], 0
    small = [(dy, t, ctr_automaton(t, dy, 10)) for dy, t in ((0, [(ETA, y) for y in gs]),
                                                             (DY3, [(ror(y, 12), CTR_EPS) for y in gs]))]
    for case in range(64):
        rr = iter(struct.unpack("<40I", hashlib.shake_256(("halfsearch filter %s %d" % (seed, case)).encode()).digest(160)))
        for kind, (dy, targets, tables) in enumerate(small):
            x = next(rr) & 1023
            if case % 2:
                dy, dz = next(rr) * kind, next(rr)
                targets = [(next(rr) if kind else dz, next(rr)) for _ in range(7)]
            sol = lambda dz, w: ((x + w) ^ (x + dy + (w ^ dz))) & 1023
            if case % 2:
                targets[:3] = [(dz, sol(dz, next(rr))) for dz, _ in targets[:3]]
                tables = ctr_automaton(targets, dy, 10)
            ok += ctr_look(tables, x) == sum(1 << i for i, (dz, w) in enumerate(targets)
                                             if w & 1023 in {sol(dz, v) for v in range(1024)})
    words = []
    for tables in (fq, fe):
        n = {0: 1}
        for t in tables:
            new = {}
            for s, c in n.items():
                for b in range(256):
                    new[t[s + b]] = new.get(t[s + b], 0) + c
            n = new
        words.append(n)
    share = sum(a * b for x, a in words[0].items() for y, b in words[1].items() if x & y)
    e_count = sum(b for y, b in words[1].items() if y)
    rep["filter"] = {"brute_force_right": ok, "share_right": share == SHARE, "e_count_right": e_count == E_COUNT}
    good &= ok == 128 and share == SHARE and e_count == E_COUNT
    # (3) Lemma A9 (the 208 residues modulo 2^9, four copies of S7) and the 7,072 words of alive16 (Lemma XF (b)),
    # recounted by the automaton of (2) on 16 bits for the outcomes of S
    sig = {ror(ctr_g(t), 12) & 511 for j, t in enumerate(CTR_TAUS) if S_MASK >> j & 1}
    a9 = [r for r in range(512) if any((((r + f) ^ (r + 0xFD + (f ^ 0xF0))) & 511) == 0x55 for f in range(512))]
    t16 = ctr_automaton([(ror(x, 12), CTR_EPS) for x in gs], DY3, 16)
    t16[-1] = [x & S_MASK for x in t16[-1]]
    alive = [w for w in range(1 << 16) if ctr_look(t16, w)]
    alive16 = [w for w in range(1 << 16) if (w & 127) in S7 and LW[w >> 8 & 1] >> (w >> 9 & 31) & 1]
    rep["lemmas"] = {"a9_residues": len(a9), "a9_right": a9 == [r for r in range(512) if r % 128 in S7]
                     and sig == {0xF0} and DY3 & 511 == 0xFD and CTR_EPS & 511 == 0x55,
                     "alive16": len(alive), "alive16_right": alive == alive16,
                     "lw_bits": [bin(x).count("1") for x in LW], "y3_low": hex(Y3 & 0xFFFF)}
    good &= rep["lemmas"]["a9_right"] and len(a9) == 208 and alive == alive16 and len(alive) == 7072
    good &= Y3 & 0xFFFF == 0xC181 and Y3 & 1023 == 0x181
    # (4) Lemma CL on random contexts and clusters: y[17..24] = T_i and the borrow into bit 17 for every member; the
    # straddle flag against the two low bytes of p (half of the cases with A[8..15] = p[8..15]); the gate rule
    sd = st = nc = 0
    for case in range(max(64, cases)):
        b, c, dd, a0 = struct.unpack("<4I", hashlib.shake_256(("halfsearch v110 straddle %s %d" % (seed, case)).encode())
                                      .digest(16))
        g = ctr_r("cl %s %d" % (seed, case)) % 16384
        lows = set()
        for j in range(32):
            y = cluster_member(g, j)
            e1 = (Y3 + y) & MASK
            sd += (y >> 10 & 63) != 16 + j or (y >> 16 & 1) or (y >> 17 & 255) != (0xF2, 0xFA, 0x02, 0x0A)[e1 >> 20 & 3]
            lows.add(rol(((rol(y, 7) ^ b) - c) & MASK, 8) ^ dd)
        p0 = rol(((rol(cluster_member(g, 0), 7) ^ b) - c) & MASK, 8) ^ dd
        sd += len({p >> 8 & 0x1FFFF for p in lows}) != 1
        i = ((Y3 + cluster_member(g, 0)) & MASK) >> 20 & 3
        a = (a0 & 0xFFFF0000) | (p0 & 0xFF00) | (a0 & 255) if case % 2 else a0
        borrows = {(p & 0xFFFF) < (a & 0xFFFF) for p in lows}
        rule = (p0 >> 8 & 255) == (a >> 8 & 255) and hbad(b, c, dd, a) >> i & 1 == 1
        sd += (len(borrows) > 1) and not rule
        st += rule
        nc += 1
    gt = 0
    for case in range(4096):
        r = ctr_r("gate %s %d" % (seed, case))
        k = r & ((1 << 30) - 1)
        if case % 2:
            k = k & ~(255 << 22) | (k >> 8 & 255) << 22
        w, mm, h, i, a = k & 127, k >> 8 & 255, k >> 16 & 15, k >> 20 & 3, k >> 22
        gt += gate_entry(GATE_BASE + k) == gate_entry(GATE_BASE + (k ^ 128)) == int(
            (w - 0x25) & 0x5F <= 0x19 or (mm == a and h >> i & 1 == 1))
    rep["lemmas"]["straddle"] = {"clusters": nc, "mismatches": sd, "straddling": st, "gate_rule_right": gt}
    good &= sd == 0 and gt == 4096
    # (5) the walk of 9.8 and 9.9 against step CO, (2) and the filter; the descriptors and windows (Lemma XF)
    agg, units, surv_max, bij = {}, {"rep": set(), "E lane": set(), "fill": set()}, 0, 0
    open_max, fb_max, open_shapes = 0, 0, {}
    for n in range(max(3, cases // 50)):
        z = ctr_r("halfsearch v110 context %s %d" % (seed, n))
        seven = [z >> 32 * i & MASK for i in range(7)]
        batches = sorted({(z >> 224 + 6 * t) % (REP_BATCHES - 1) for t in range(5)}) + [REP_BATCHES - 1]
        s, checks, bad, skipped = v110_walk(seven, batches)
        r = walk_report(s, checks, bad, skipped)
        for k, v in r.items():
            if k in ("open_units_max", "chunk_lanes_max"):
                agg[k] = max(agg.get(k, 0), v)
            elif k != "work":
                agg[k] = agg.get(k, 0) + v
        for k in units:
            units[k] |= s.units[k]
        for ch, x in s.units["open"]:
            open_shapes[len(ch), sum(ch)] = max(open_shapes.get((len(ch), sum(ch)), 0), x)
        fb_max = max([fb_max] + s.units["fallback"])
        for d in s.desc.values():
            surv_max = max(surv_max, d[0][0] + d[1][0])
            good &= d[0][0] <= 7 and d[1][0] <= 7 and (d[1][0] == 0 or d[0][0] > 0) and (d[0][0], d[1][0]) in CASE
        bij += all(sorted(window(s.w, ix, j) for j in range(32)) == list(range(32)) for ix in range(16))
    rep["walk"] = dict(agg, units={k: sorted(v) for k, v in units.items()}, fallback_units_max=fb_max,
                       open_units_by_chunks={"%d chunks, %d lanes" % k: v for k, v in sorted(open_shapes.items())},
                       survivors_max=surv_max, window_bijections=bij)
    good &= (agg["mismatches"] == 0 and agg["skipped_pass"] == 0 and agg["e_lanes"] > 0 and surv_max <= 9
             and bij == max(3, cases // 50) and agg["open_units_max"] <= U_OPEN and fb_max <= U_FALLBACK)
    # (6) the lane bound of Lemma MB on the batch, the key and the fill, through the lines on upper bounds
    Bound.seen = []
    bc = {k: Bound(1 << 32) for k in ("C0.b1", "-C0.c1", "C0.d1", "K'", "S15'", "-S0-S5", "-C0.b1-w6", "ROL(C0.d1,16)",
                                      "K", "S12", "-S1-S6", "S10", "S5", "w3", "X13", "ROL(X15,8)", "X15")}
    bc["X9'"] = Bound((1 << 34) + (1 << 32))
    y0 = pror(Bound(1 << 32) + bc["-C0.c1"], 24) ^ bc["C0.d1"]
    x0 = y0 + bc["K'"]
    om = (pror(x0, 16) ^ bc["S15'"]) + (Bound(1 << 32) + bc["-S0-S5"])
    x12 = (y0 + bc["-C0.b1-w6"]) ^ bc["ROL(C0.d1,16)"]
    d1d1 = (x12 ^ MASK) + bc["K"]
    w10 = (pror(d1d1, 16) ^ bc["S12"]) + bc["-S1-S6"]
    d0c1 = (x0 ^ bc["ROL(X15,8)"]) + bc["S10"]
    x5 = pror(pror(d0c1 ^ bc["S5"], 12) ^ (d0c1 + bc["X15"]), 7)
    c1a1 = (pror(x12, 24) ^ d1d1) + x5 + bc["w3"]
    c1d1 = pror(c1a1 ^ bc["X13"], 16)
    c1c1 = bc["X9'"] + c1d1
    y9 = c1c1 + pror(c1d1 ^ (c1a1 + pror(x5 ^ c1c1, 12) + w10), 8)
    rep["walk"]["lane_bound_log2"] = round(math.log2(max(Bound.seen)), 4)
    rep["walk"]["omega_bound"] = om.b <= 3 << 32
    rep["walk"]["y9_bound"] = y9.b <= (1 << 35)
    good &= max(Bound.seen) <= 1 << LANE_BITS and om.b <= 3 << 32 and y9.b <= 1 << 35
    # (7) the constants of 9.1 and the ledger of Section 11: entry 070a02b2 reproduced, then this row; the case code
    from fractions import Fraction
    got = {k: globals()[k] for k in CONSTANTS_070}
    rep["constants_right"] = got == CONSTANTS_070
    base = ledger(144, 112519, ONCE_070)
    rep["ledger_070a02b2"] = {"N_430T": base["N_430T"], "time_log2": base["time_log2"],
                              "right": base["N_430T"] == 3436742575482187376270}
    worst = {ab: case_base(*ab) + 2 * CASE_DEPTH[ab] for ab in CASES}
    kraft = sum(Fraction(1, 1 << CASE_LEN[ab]) for ab in CASES)
    rep["dispatch"] = {"cases": len(CASES), "comparisons": sum(1 for _ in CASES) - 1, "kraft": str(kraft),
                       "worst_case": max(worst.values()), "worst_cases": sorted(str(ab) for ab in CASES
                                                                              if worst[ab] == max(worst.values())),
                       "depth_of_worst": sorted({CASE_DEPTH[ab] for ab in CASES if case_base(*ab) == 128}),
                       "prefix_free": len(set(CASE.values())) == len(CASES)
                       and all(CASE_DEPTH[ab] <= CASE_LEN[ab] for ab in CASES)}
    rep["ledger"] = ledger()
    rep["ledger"].update(u_open_items={"W": U_W, "rep T2'": U_REP_T2, "byte guard": U_GUARD, "selection": U_SEL,
                                       "dispatch and leaf, worst": U_OPEN - U_W - U_REP_T2 - U_GUARD - U_SEL},
                         u_context=U_CONTEXT, u_fallback=U_FALLBACK)
    good &= (rep["constants_right"] and rep["ledger_070a02b2"]["right"] and rep["ledger"]["claim_exact"]
             and kraft <= 1 and max(worst.values()) == U_OPEN == 134 and rep["dispatch"]["prefix_free"]
             and U_FALLBACK == 261 and U_CONTEXT == 113799 and agg["open_units_max"] <= U_OPEN)
    return rep, good
def selftest(cases, seed):
    rep, good = v110_selftest(cases, seed)
    json.dump(dict(rep, seed=seed, good=bool(good)), sys.stdout, separators=(",", ":"))
    sys.stdout.write("\n")
    return 0 if good else 1
def main():
    if len(sys.argv) > 1:
        if sys.argv[1] != "--selftest" or len(sys.argv) not in (3, 4) or not sys.argv[2].isdecimal() or int(sys.argv[2]) < 1:
            raise SystemExit("usage: halfsearch.py --selftest N [seed]   (no arguments: organizer request on stdin)")
        raise SystemExit(selftest(int(sys.argv[2]), sys.argv[3] if len(sys.argv) == 4 else "1"))
    request = json.load(sys.stdin)
    if request["schema_version"] != 1 or request["target_profile"] != "blake3-r2-prefix-v1":
        raise ValueError("unexpected organizer target")
    if request["event"].get("kind") != "digest-xor-mask":
        raise ValueError("unexpected organizer event")
    run = {"cluster-walk": cluster_walk}[request["experiment_id"]]
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
