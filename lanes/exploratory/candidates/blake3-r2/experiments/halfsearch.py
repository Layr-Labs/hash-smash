"""Half-collisions of 2-round BLAKE3 inside one difference class and a small residual search (the two organizer
experiments, root instance), and the counted pieces of the v108 counter search (proof.md Sections 8, 9 and 11): the
chunk-counter construction and its trials, the outer filter for the outcomes of S, and the walk of 9.8 by contexts and
member batches with the Y9 closure in the Q path, counted on the packed machine; with the ledger of Section 11."""
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
# (L * N3 / 2^83, Section 17), the listed set S = 5f (all but 675020a0; count 67,633,152), the factor of H1' at ten
# elevenths (margin 1.100, v109), the exact counts of Section 8 for S, and the constants of proof.md 9.1.
CTR_TAUS = (0x175020A0, 0x185020A0, 0x275020A0, 0x285020A0, 0x385020A0, 0x675020A0, 0x685020A0)
CTR_EPS = 0x6E21BE55
CTR_PARTS = (6291456, 16777216, 1048576, 25165824, 16777216, 65536, 1572864)
S_MASK = 0x5F
S_COUNT = sum(p for j, p in enumerate(CTR_PARTS) if S_MASK >> j & 1)
FACTOR = 10 * (S_COUNT << 11) // 11
RUN_STEPS_MIN = -(-(12419 << 128) // (25000 * FACTOR * (CTR_MEMBERS - 1)))
RUN_CONTEXTS = -(-RUN_STEPS_MIN >> 19)
RUN_STEPS = RUN_CONTEXTS << 19
SHARE, E_COUNT = 18289159183466496, 233715456
E_BUDGET = -(-17 * RUN_STEPS * E_COUNT >> 36)
PASS_BUDGET = -(-17 * RUN_STEPS * SHARE >> 68)
CBAR = 611713706062329
CREDIT_LC = (1 << 19) * 37032                                  # v110: the largest sum of C(T) over one context
CREDIT_MEAN = -(-106 * RUN_STEPS * CBAR // (100 << 47))        # ceil(1.06 * RUN_STEPS * cbar), the mean bound of H5'
CREDIT = CREDIT_MEAN + math.isqrt(40 * CREDIT_LC * CREDIT_MEAN - 1) + 1 + 14 * CREDIT_LC   # Bernstein reserve, tail exp(-20)
BATCHES = -(-CTR_CSIZE // 7)
RUN_BATCHES = BATCHES * RUN_CONTEXTS
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
def residual_word1(v, words, t, y4):
    'Digest word 1 of A xor digest word 1 of B for one trial (round 1, partial; proof.md 6.2).'
    c1 = g(t["X1"], t["X5"], v["X9"], v["X13"], words[3], words[10])
    c2 = g(v["X2"], t["X6"], t["X10"], v["X14"], words[7], words[0])
    y1, y9, y6, y14 = c1[0], c1[2], c2[1], c2[3]
    w5b = (words[5] + DELTA5) & MASK
    pa = g(y1, y6, Y11, t["Y12"], words[12], words[5])
    pb = g(y1, y6, Y11B, t["Y12"], words[12], w5b)
    qa = g(Y3, y4, y9, y14, words[15], words[8])
    qb = g(Y3B, y4, y9, y14, words[15], words[8])
    return pa[0] ^ qa[2] ^ pb[0] ^ qb[2]
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
def residual_search(seed):
    free, k0 = seeded(seed)
    v = context(free)
    for step in range(CLASS_SIZE):
        y4 = class_member((k0 + step) % CLASS_SIZE)
        words, values = trial(v, y4)
        if residual_word1(v, words, values, y4) & 0xFF == 0:
            return messages(words) + ({"tries": step + 1},)
    return None, None, {"tries": CLASS_SIZE}
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
# == v108: the walk of proof.md 9.8, contexts and member batches with direct tables, the Y9 closure in the Q path ==
DY3 = (Y3B - Y3) & MASK
LANE_BITS = 36
T1_BASE, T2_BASE = 1 << 40, 1 << 36
def spread(x):
    'The 32-bit value x in all seven 36-bit lanes of a packed word.'
    return sum(x << LANE_BITS * i for i in range(7))
M_ALL = spread(MASK)
def lane(z, i):
    return int(z) >> LANE_BITS * i & MASK
class Bound:
    'An exclusive upper bound on every lane of a packed value, carried through the lines (Lemma MB).'
    seen = []
    def __init__(s, b):
        s.b = b
        Bound.seen.append(b)
    def __add__(s, o):
        return Bound(s.b + (o.b if type(o) is Bound else (o & MASK) + 1) - 1)
    def __xor__(s, o):
        return Bound(1 << (max(s.b, o.b if type(o) is Bound else (o & MASK) + 1) - 1).bit_length())
    __radd__, __rxor__ = __add__, __xor__
def pror(z, r):
    'PROR of proof.md 6.5: every lane rotated right by r, five operations; its result is below 2^32 in every lane.'
    if type(z) is Bound:
        return Bound(1 << 32)
    return ((z >> r) & spread((1 << 32 - r) - 1)) | ((z << 32 - r) & spread(((1 << r) - 1) << 32 - r))
def v108_context(seven):
    """A context (proof.md 9.8): step CO for its seven outer words (the 39 lines of Lemma Y read no member; y = 0 here)
    and the sixteen context words of a batch, each in all seven lanes, with the immediates X15 and ROL(X15, 8)."""
    o = ctr_outer(list(seven) + [0], 0)
    w = {"C0.b1": o["C0.b1"], "-C0.c1": -o["C0.c1"], "C0.d1": o["C0.d1"],
         "-C0.b1-w6-X4-w2": -o["C0.b1"] - o["w6"] - o["X4"] - o["w2"], "ROL(X15,24)^S15": rol(X15, 24) ^ o["S15"],
         "-S0-S5": -o["S0"] - o["S5"], "-C0.b1-w6": -o["C0.b1"] - o["w6"], "ROL(C0.d1,16)": rol(o["C0.d1"], 16),
         "X11+1-S11": X11 + 1 - o["S11"], "S12": o["S12"], "-S1-S6": -o["S1"] - o["S6"], "S10": o["S10"],
         "S5": o["S5"], "w3": o["w3"], "X13": o["X13"], "X9": o["X9"]}
    return o, {k: spread(v & MASK) for k, v in w.items()}
V108_IMMEDIATE = {"ROL(X15,8)": spread(rol(X15, 8)), "X15": spread(X15)}
def v108_lists(b):
    'List words U[b] and E[b] (interleaved, E at the cursor plus one): ROL(y, 7) and e1 = Y3 + y of members 7b to 7b + 6.'
    ks = [min(7 * b + i, CTR_CSIZE - 1) for i in range(7)]
    ys = [ctr_member(k) for k in ks]
    return (sum(rol(y, 7) << LANE_BITS * i for i, y in enumerate(ys)),
            sum(((Y3 + y) & MASK) << LANE_BITS * i for i, y in enumerate(ys)), ks, ys)
def v108_omega(c, u, e):
    'The 17 packed operations of a batch after its list loads: Y0, X0 and omega = Y3 + y + w8 in every lane.'
    y0 = pror((u ^ c["C0.b1"]) + c["-C0.c1"], 24) ^ c["C0.d1"]
    x0 = y0 + c["-C0.b1-w6-X4-w2"]
    return y0, x0, (e + c["-S0-S5"]) + (pror(x0, 16) ^ c["ROL(X15,24)^S15"])
def v108_closure(c, y0, x0):
    'The 56 packed operations of the Y9 closure, run in every lane at the first Q path of a batch (proof.md 9.8).'
    x12 = (y0 + c["-C0.b1-w6"]) ^ c["ROL(C0.d1,16)"]
    d1d1 = (x12 ^ M_ALL) + c["X11+1-S11"]
    x1 = pror(x12, 24) ^ d1d1
    w10 = (pror(d1d1, 16) ^ c["S12"]) + c["-S1-S6"]
    d0c1 = (x0 ^ c["ROL(X15,8)"]) + c["S10"]
    x5 = pror(pror(d0c1 ^ c["S5"], 12) ^ (d0c1 + c["X15"]), 7)
    c1a1 = x1 + x5 + c["w3"]
    c1d1 = pror(c1a1 ^ c["X13"], 16)
    c1c1 = c1d1 + c["X9"]
    y1 = c1a1 + pror(x5 ^ c1c1, 12) + w10
    return c1c1 + pror(c1d1 ^ y1, 8)
def v108_batch(m, c, b, ec, p):
    """Batch b of a context on the counted machine m (proof.md 9.8): the two list loads, omega, and per used lane the
    test of (2) by one load of T2 at its omega; for a lane whose mask of (2) is not zero the Q path: the E count in its
    register, at the first such lane of the batch the Y9 closure, Y9 of the lane, one load of T1, the mask X and the
    jump back; then the cursor. Returns (E count, cursor, omega, Y9 or None, [(lane, mask of (2), X, Q-path units)])."""
    fq, fe = ctr_tables()
    U, E, ks, ys = v108_lists(b)
    m.at("batch")
    u = m.load(U)
    a = p + 1
    e = m.load(E)
    y0, x0, om = v108_omega(c, u, e)
    y9, out = None, []
    for i in range(7 if b < BATCHES - 1 else CTR_CSIZE - 7 * (BATCHES - 1)):
        m.at("batch")
        x = (om if i == 0 else om >> LANE_BITS * i) & MASK
        m2 = m.load(ctr_look(fe, lane(x + T2_BASE, 0)))
        m.branch(m2)
        if not m2:
            continue
        m.at("Q path")
        q0 = m.units["Q path"]
        ec = ec + 1
        m.branch(ec)
        if y9 is None:
            y9 = v108_closure(c, y0, x0)
        q = (y9 if i == 0 else y9 >> LANE_BITS * i) & MASK
        mx = m.load(ctr_look(fq, lane(q + T1_BASE, 0))) & m2
        m.branch(mx)
        m.tick()
        out.append((i, int(m2), int(mx), m.units["Q path"] - q0))
    m.at("batch")
    p = p + 2
    m.branch(p)
    return ec, p, int(om), None if y9 is None else int(y9), out
def v108_check(contexts, seed):
    """The walk of proof.md 9.8 against the scalar step CO and the filter: per context the full batches drawn from the
    seed and the last batch, every lane's omega, mask of (2) and, on a Q path, Y9 and X; the units of every batch and Q
    path; the registers; and the lane bounds of Lemma MB."""
    fq, fe = ctr_tables()
    r = {"contexts": contexts, "batches": 0, "lanes": 0, "lanes_right": 0, "q_paths": 0, "q_right": 0, "passing": 0,
         "batch_units": set(), "last_batch_units": set(), "q_units_first": set(), "q_units_later": set(),
         "context_lines_same": 0, "registers": 0}
    for n in range(contexts):
        z = ctr_r("halfsearch v108 context %s %d" % (seed, n))
        seven = [z >> 32 * i & MASK for i in range(7)]
        o, cw = v108_context(seven)
        m = Word.m = Cnt()
        m.at("context")
        c = dict({k: m.new(v) for k, v in cw.items()}, **V108_IMMEDIATE)
        ec, p = m.new(0), m.new(0)
        for t in range(26):
            b = BATCHES - 1 if t == 25 else (z >> 7 * t) % (BATCHES - 1)
            before = dict(m.units)
            ec, p, om, y9, out = v108_batch(m, c, b, ec, p)
            r["last_batch_units" if t == 25 else "batch_units"].add(m.units["batch"] - before.get("batch", 0))
            for n_q, (i, m2, mx, uq) in enumerate(out):
                r["q_units_later" if n_q else "q_units_first"].add(uq)
            U, E, ks, ys = v108_lists(b)
            got = {i: (m2, mx) for i, m2, mx, uq in out}
            r["batches"] += 1
            for i in range(7 if t < 25 else CTR_CSIZE - 7 * (BATCHES - 1)):
                v = ctr_outer(seven + [0], ys[i])
                r["context_lines_same"] += all(v[k] == o[k] for k in ("C0.b1", "C0.c1", "C0.d1", "w6", "X4", "w2", "S15",
                                               "S0", "S5", "S11", "S12", "S1", "S6", "S10", "w3", "X13", "X9"))
                omega = (Y3 + ys[i] + v["w8"]) & MASK
                m2 = ctr_look(fe, omega)
                ok = lane(om, i) == omega and (m2 != 0) == (i in got)
                if m2:
                    r["q_paths"] += 1
                    mx = ctr_filter(v["Y9"], ys[i], v["w8"])
                    qok = lane(y9, i) == v["Y9"] and got[i] == (m2, mx)
                    r["q_right"] += qok
                    r["passing"] += mx != 0
                    ok &= qok
                r["lanes"] += 1
                r["lanes_right"] += ok
        r["registers"] = max(r["registers"], m.registers())
    Bound.seen = []
    bc = {k: Bound(1 << 32) for k in cw}
    bc.update(V108_IMMEDIATE)
    y0, x0, om = v108_omega(bc, Bound(1 << 32), Bound(1 << 32))
    v108_closure(bc, y0, x0)
    r["lane_bound_log2"] = round(math.log2(max(Bound.seen)), 4)
    for k in ("batch_units", "last_batch_units", "q_units_first", "q_units_later"):
        r[k] = sorted(r[k])
    r["good"] = (r["lanes"] == r["lanes_right"] == r["context_lines_same"] and r["q_paths"] == r["q_right"] > 0
                 and r["batch_units"] == [V108_UNITS["batch"]] and max(r["last_batch_units"]) <= V108_UNITS["batch"]
                 and max(r["q_units_first"]) == V108_UNITS["Q path"] and max(r["q_units_later"]) <= 11
                 and r["registers"] <= 64 and max(Bound.seen) <= 1 << LANE_BITS)
    return r
# == the charge of proof.md Section 11 ==
V108_UNITS = {"batch": 64, "Q path": 67, "passing lane": 512, "context": 2048}
ONCE = (1 << 39) + (1 << 27) + (1 << 20) + 4 * (1 << 26) + (1 << 50) + 40 + 16
SEL_OPS = 116 * (1 << 56) + 116 * ((1 << 52) + (1 << 10)) + (1 << 50)
DEV_OPS = 1 << 54
FINAL = 1 << 38
def v108_time(u):
    """T = (rows + SEL_OPS + DEV_OPS) / 430 + FINAL, as a fraction; rows: batches, contexts, Q paths and passing lanes
    (each budget plus one), the credit, and the once-only items."""
    from fractions import Fraction
    rows = (u["batch"] * RUN_BATCHES + u["context"] * (RUN_CONTEXTS + 1) + u["Q path"] * (E_BUDGET + 1)
            + u["passing lane"] * (PASS_BUDGET + 1) + CREDIT + ONCE)
    return Fraction(rows + SEL_OPS + DEV_OPS, 430) + FINAL, rows
def v108_ledger(u):
    T, rows = v108_time(u)
    lg = math.log2(T.numerator) - math.log2(T.denominator)
    claim = math.ceil(lg * 1e5)
    p, q = T.numerator ** 100000, T.denominator ** 100000     # 2^(claim - 1) < T^100000 < 2^claim, in integers
    return {"claim_exact": q << claim - 1 < p < q << claim, "units": u, "factor": FACTOR, "run_contexts": RUN_CONTEXTS,
            "run_steps": RUN_STEPS, "run_batches": RUN_BATCHES, "e_budget": E_BUDGET, "pass_budget": PASS_BUDGET,
            "credit": CREDIT, "numerator": rows + SEL_OPS + DEV_OPS, "time_log2": round(lg, 8), "claim": claim / 1e5}
def ctr_selftest(cases, seed):
    """The v108 self-test (proof.md 9.3). Returns (report, good)."""
    rep, good = {}, True
    # (1) counter trials against the compressions of their last chunks (and the organizer's _compress if present)
    try:
        sys.path.insert(0, "verifier")
        import blake3 as organizer
    except ImportError:
        organizer = None
    right = same_c1 = e1_right = org = 0
    for case in range(cases):
        r = ctr_r("halfsearch v108 trial %s %d" % (seed, case))
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
        a, b, t, v = ctr_trial(o, c1)
        (wa, da, ya), (wb, db, yb) = compress2(a[:LEN_A], t, CTR_FLAGS), compress2(b[:LEN_B], t, CTR_FLAGS)
        ea, eb = g(ya[1], ya[6], ya[11], ya[12], wa[12], wa[5]), g(yb[1], yb[6], yb[11], yb[12], wb[12], wb[5])
        ga = g(v["Y1"], v["Y6"], Y11, v["Y12"], v["w12"], v["w5"])
        gb = g(v["Y1"], v["Y6"], Y11B, v["Y12"], v["w12"], (v["w5"] + DELTA5) & MASK)
        e1_right += (ea[0] ^ eb[0], ea[2] ^ eb[2]) == (ga[0] ^ gb[0], ga[2] ^ gb[2])
        if organizer and case % 25 == 0:
            org += list(organizer._compress(IV, wa, t, LEN_A, CTR_FLAGS, 2)[:8]) == da
    rep["trials"] = {"cases": cases, "right": right, "inverse_right": same_c1, "e1_right": e1_right,
                     "organizer_compress": org if organizer else "verifier not found"}
    good &= right == same_c1 == e1_right and right > 0.99 * cases and (not organizer or org == -(-cases // 25))
    # (2) the filter: brute force at width 10, the exact counts for S (Section 8), the counted scalar outer step
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
    counted, shape, regs = 0, None, 0
    for i in range(8):
        r = ctr_r("halfsearch v108 steps %s %d" % (seed, i))
        m, o, z = ctr_count(r)
        p = ctr_outer(ctr_eight(r))
        counted += all(o[k] == p[k] for k in p) and z == ctr_filter(p["Y9"], p["Y4"], p["w8"])
        shape = shape or dict(m.units)
        counted -= m.units != shape
        regs = max(regs, m.registers())
    rep["filter"] = {"brute_force_right": ok, "share_s": share, "share_right": share == SHARE, "e_count": e_count,
                     "e_count_right": e_count == E_COUNT, "share_log2": round(math.log2(share) - 64, 6),
                     "states": [[len(t) >> 8 for t in fq], [len(t) >> 8 for t in fe]],
                     "scalar_steps_right": counted, "scalar_units": shape, "registers": regs}
    good &= ok == 128 and share == SHARE and e_count == E_COUNT and counted == 8 and regs <= 64
    # (3) the walk of 9.8, the class numbering and the coverage of a context (Lemma CX (b))
    rep["walk"] = v108_check(max(4, cases // 50), seed)
    members = [7 * b + i for b in range(BATCHES) for i in range(7 if b < BATCHES - 1 else CTR_CSIZE - 7 * b)]
    e1 = [(Y3 + ctr_member(k)) & MASK for k in (0, 1, 2, CTR_CSIZE - 1)]
    rep["walk"]["coverage_right"] = members == list(range(CTR_CSIZE)) and BATCHES == 74899
    rep["walk"]["numbering_right"] = e1[0] == 0x030C0303 and all(x & CTR_CLASS == 0x030C0303 for x in e1)
    good &= rep["walk"]["good"] and rep["walk"]["coverage_right"] and rep["walk"]["numbering_right"]
    # (4) the charge
    rep["ledger"] = v108_ledger(V108_UNITS)
    good &= rep["ledger"]["claim_exact"] and FACTOR == 125920632087 and RUN_STEPS == 640117155200996737024 and CREDIT == 2949244610503938020175
    return rep, good
def selftest(cases, seed):
    rep, good = ctr_selftest(cases, seed)
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
