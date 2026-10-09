"""Half-collisions of 2-round BLAKE3 inside one difference class, a small residual search (the two organizer
experiments, root instance), and the v108 counter search: Jbenisek's chunk-counter construction and outer filter with Y4
in the whole class, the fourteen outcomes of beta*, winglock's exact E3 solver, and the walk in seven 36-bit lanes."""
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
    return v.rot(32 - n) if hasattr(v, "rot") else ((v >> n) | (v << (32 - n))) & MASK
def rol(v, n):
    return v.rot(n) if hasattr(v, "rot") else ((v << n) | (v >> (32 - n))) & MASK
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
# v107: Y4 runs over the whole class of eta (Lemma Q: 2^19 members), not the sub-class; no rule A.
CTR_CLASS = rol(ETA, 16) & 0x7FFFFFFF
CTR_CFREE = tuple(i for i in range(32) if not CTR_CLASS >> i & 1)
CTR_CSIZE = 1 << len(CTR_CFREE)
# The fourteen outcomes (tau, eps) of beta* with a nonzero part in the class, their parts (L * N3 / 2^83; sum 71,698,432,
# the count of proof.md Section 17 run on the class), the factor of H1' at margin 1.400 (GordoAR), the exact share of
# word pairs that pass the filter for the fourteen (Section 8), lambda and the run length.
CTR_TAUS = (0x175020A0, 0x175060A0, 0x185020A0, 0x185060A0, 0x275020A0, 0x275060A0, 0x285020A0, 0x285060A0,
            0x385020A0, 0x385060A0, 0x675020A0, 0x675060A0, 0x685020A0, 0x685060A0)
CTR_EPS = 0x6E21BE55
CTR_PARTS = (6291456, 196608, 16777216, 1048576, 1048576, 32768, 25165824, 1572864, 16777216, 1048576, 65536, 2048,
             1572864, 98304)
CTR_FACTOR = (sum(CTR_PARTS) << 11) * 5 // 7
CTR_SHARE = 99669577442459648
LAMBDA = (495910, 10 ** 6)
RUN_OUTER_STEPS = -(-(LAMBDA[0] << 128) // (LAMBDA[1] * CTR_FACTOR * (CTR_MEMBERS - 1)))
# Premise of H2'' (mean pass units per walked outer step, from the preregistered sample of proof.md 13.5) and its budget.
PASS_PREMISE = (1369, 16)
PASS_BUDGET = -(-RUN_OUTER_STEPS * PASS_PREMISE[0] * 6001 // (PASS_PREMISE[1] * 6000))
# Charged besides (proof.md 9.2 and 11): the walk's loop control per walked outer step; the machine's bookkeeping in a
# passing step, at most X / 15 (Lemma U), so its units are at most PASS_SCALE * X; the last step may pass the budget by
# X_MAX, the largest X of one step.
LOOP_UNITS = 3
PASS_SCALE = (16, 15)
X_MAX = 56 + (1 << 23) + 14 * 1600 + (1 << 21) * 192 + 128 * 286720
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
    "The filter's two automata, built once per run on first use: (1) on Q for the fourteen G, (2) on E with E' = E + DY3."
    if not CTR_FILTER:
        g = [ctr_g(t) for t in CTR_TAUS]
        CTR_FILTER.extend((ctr_automaton([(ETA, x) for x in g], 0),
                           ctr_automaton([(ror(x, 12), CTR_EPS) for x in g], (Y3B - Y3) & MASK)))
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
    'The filter of one outer step: the outcomes (bits 0-13) with (1) solvable for Q = Y9 and (2) for E = Y3 + Y4 + w8.'
    fq, fe = ctr_tables()
    return ctr_look(fq, q) & ctr_look(fe, (Y3 + y4 + w8) & MASK)
class Cnt:
    """The machine of proof.md 9.2: one unit for every executed primitive (operation, load, store, comparison, branch,
    random word); constant operands, shift distances and table base addresses are instruction fields; 64 registers.
    Parts are counted separately; Word values record when they are made and last read, for the register count."""
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
# == v108: seven outer steps per 256-bit word, one in each 36-bit lane (proof.md 9.2, Lemma L7) ==
LANES = 7
def lrep(c):
    return sum(c << 36 * i for i in range(LANES))
LANE_M = lrep(MASK)
class LW:
    """Seven lanes of 36 bits: each lane lies in [lo, hi], below 2^36, and is congruent to its step's value modulo 2^32.
    Each operation keeps this (Lemma L7) and counts its primitives on Word.m; an int operand is a 32-bit immediate."""
    def __init__(s, v, lo, hi, n=0, used=()):
        if hi >> 36 or lo < 0:
            raise ValueError("lane bound")
        s.v, s.lo, s.hi, m = v, lo, hi, Word.m
        if m:
            m.tick(n)
            s.w = m.new(v)
            for u in used:
                u.w.l = s.w.b
    def lane(s, i):
        return s.v >> 36 * i & MASK
    def clean(s):
        return LW(s.v & LANE_M, 0, MASK, 1, (s,)) if s.hi > MASK else s
    def __and__(s, o):
        if o != MASK:
            raise ValueError("lane AND")
        return s
    def __add__(s, o):
        if type(o) is int:
            o &= MASK
            a = s if s.hi + o >> 36 == 0 else s.clean()
            return LW(a.v + lrep(o), a.lo + o, a.hi + o, 1, (a,)) if o else s
        a, b = (s, o) if s.hi + o.hi >> 36 == 0 else (s.clean(), o.clean())
        return LW(a.v + b.v, a.lo + b.lo, a.hi + b.hi, 1, (a, b))
    __radd__ = __add__
    def __sub__(s, o):
        if type(o) is int:
            o &= MASK
            return LW(s.v - lrep(o), s.lo - o, s.hi - o, 1, (s,)) if s.lo >= o else s + ((1 << 32) - o)
        if s.lo >= o.hi:
            return LW(s.v - o.v, s.lo - o.hi, s.hi - o.lo, 1, (s, o))
        b = o if o.hi >> 34 == 0 else o.clean()
        k = max(33, b.hi.bit_length())
        a = s if s.hi + (1 << k) >> 36 == 0 else s.clean()
        return LW((a.v | lrep(1 << k)) - b.v, (1 << k) - b.hi, a.hi + (1 << k) - b.lo, 2, (a, b))
    def __rsub__(s, o):
        b = s if s.hi >> 34 == 0 else s.clean()
        c = (o & MASK) + (1 << max(33, b.hi.bit_length()))
        return LW(lrep(c) - b.v, c - b.hi, c - b.lo, 1, (b,))
    def __xor__(s, o):
        if type(o) is int:
            return LW(s.v ^ lrep(o), 0, (1 << max(s.hi, MASK).bit_length()) - 1, 1, (s,))
        return LW(s.v ^ o.v, 0, (1 << max(s.hi, o.hi).bit_length()) - 1, 1, (s, o))
    __rxor__ = __xor__
    def rot(s, r):
        return LW((s.v & lrep((1 << 32 - r) - 1)) << r | s.v >> 32 - r & lrep((1 << r) - 1), 0, MASK, 5, (s,))
CTR_FREEM, CTR_E1 = ~CTR_CLASS & MASK, CLASS_VALUE & CTR_CLASS
CTR_T = ({}, {})
def ctr_table(k, x):
    'Entry x of the mask tables T1 (k = 0, condition (1)) and T2 (k = 1, condition (2)): the automaton of 8.3 on x.'
    t = CTR_T[k]
    if x not in t:
        t[x] = ctr_look(ctr_tables()[k], x)
    return t[x]
def ctr_batch(rs):
    """Seven outer steps from eight random words: lane i of words 0-6 gives the outer words of step i and lane i of word 7
    the free bits of its e1 = Y3 + Y4. Step CO on the lanes, omega = e1 + w8, and the filter by the tables T1 and T2.
    Returns (lanes, masks): the values of step CO of each step and its mask."""
    m = Word.m
    if m:
        m.tick(8)
    e1 = LW(rs[7] & lrep(CTR_FREEM) | lrep(CTR_E1), CTR_E1, MASK, 2)
    o = ctr_outer([LW(r & LANE_M, 0, MASK, 1) for r in rs[:7]] + [0], e1 - Y3)
    if m:
        m.at("filter")
    om = o["w8"] + e1
    z, zs = 0, []
    for i in range(LANES):
        q, e = [(x.w if m else x.v) >> 36 * i & MASK if i else (x.w if m else x.v) & MASK for x in (o["Y9"], om)]
        a, b = ctr_table(0, int(q)), ctr_table(1, int(e))
        zi = m.load(a) & m.load(b) if m else a & b
        z, zs = z | zi if i else zi, zs + [int(zi)]
    if m:
        m.branch(z)
    return [{k: x.lane(i) if type(x) is LW else x for k, x in o.items()} for i in range(LANES)], zs
def ctr_count(rs):
    'One counted batch: returns (machine, lanes, masks).'
    m = Word.m = Cnt()
    m.at("batch")
    lanes, zs = ctr_batch(rs)
    Word.m = None
    return m, lanes, zs
# == the exact E3 solver of proof.md 8.4 (Lemma E3) ==
DY3 = (Y3B - Y3) & MASK
DEAD = 4
def _tb(i):
    'B on bit k of f: carries of omega + f and of (omega + DY3) + (f ^ psi); key bits omega_k, omega2_k, psi_k, eps_k.'
    key, s, x = i >> 3, i >> 1 & 3, i & 1
    s1, s2 = (key & 1) + x + (s & 1), (key >> 1 & 1) + (x ^ key >> 2 & 1) + (s >> 1)
    return DEAD if (s1 ^ s2) & 1 != key >> 3 & 1 else s1 >> 1 | (s2 >> 1) << 1
def _ta(i):
    'A on bit i of g1: borrow of g1 - Y9 and carry of Y9 + (h ^ eta); key bits y_i, Y9_i, eta_i, theta_i; g1_i = x ^ y_i.'
    key, s, x = i >> 3, i >> 1 & 3, i & 1
    gb = x ^ key & 1
    d = gb - (key >> 1 & 1) - (s & 1)
    sm = (key >> 1 & 1) + ((d & 1) ^ key >> 2 & 1) + (s >> 1)
    return DEAD if sm & 1 != gb ^ key >> 3 & 1 else int(d < 0) | (sm >> 1) << 1
CTR_TB, CTR_TA = [_tb(i) for i in range(128)], [_ta(i) for i in range(128)]
# Units of the solver per event (proof.md 9.2): a call (the 32 level keys), a guess (its 32 joint alive sets, one table
# load each, and the root test), a root, a pop, an internal node, a child (two transitions and the joint test), a push,
# a leaf (E3 of both messages), a good h1 (ctr_good: c1 by Lemma IP, the cube test, t and E1 of both messages against
# the outcome, bounded in words).
SOLVER_UNITS = {"calls": 546, "guesses": 199, "roots": 5, "pops": 13, "internal": 14, "children": 11, "pushes": 11,
                "leaves": 49, "goods": 128}
CTR_JT = {}
def ctr_jt(key, j16, reset):
    """Entry (key, j16) of the joint alive tables (built once per run; JT19 when reset): the set, as 16 bits b * 4 + a
    and as 64 bits b * 8 + a, of joint states (b of automaton B, a of automaton A) before a bit from which some x leads
    into j16 after it; at reset (the bit k = 19, g1 bit 31) the A state after the bit is 0, the start of the low run."""
    e = (key, j16, reset)
    if e not in CTR_JT:
        s16 = s64 = 0
        for b in range(4):
            for a in range(4):
                for x in (0, 1):
                    nb, na = CTR_TB[(key >> 4) * 8 + b * 2 + x], CTR_TA[(key & 15) * 8 + a * 2 + x]
                    na = na & 4 if reset else na
                    if nb != DEAD and na != DEAD and j16 >> nb * 4 + na & 1:
                        s16, s64 = s16 | 1 << b * 4 + a, s64 | 1 << b * 8 + a
                        break
        CTR_JT[e] = s16, s64
    return CTR_JT[e]
def ctr_theta(tau):
    return rol(tau ^ ror(tau, 1), 12)
def ctr_e3(y4, y9, om, h1, j):
    'E3 of A and B for E3.h1 = h1 and omega = om: True when the differences are (theta_j, eps, tau_j) of outcome j.'
    t = CTR_TAUS[j]
    g1 = (y9 + h1) & MASK; e2 = (om + ror(y4 ^ g1, 12)) & MASK; g2 = (g1 + ror(h1 ^ e2, 8)) & MASK
    hb = h1 ^ ETA; gb = (y9 + hb) & MASK; eb = (om + DY3 + ror(y4 ^ gb, 12)) & MASK; g2b = (gb + ror(hb ^ eb, 8)) & MASK
    return g1 ^ gb == ctr_theta(t) and e2 ^ eb == CTR_EPS and g2 ^ g2b == t
def ctr_solve(y4, y9, om, j, ev, limit=None):
    """Every word h1 with ctr_e3(y4, y9, om, h1, j) (Lemma E3): a depth-first walk over the bits k = 0..31 of f1 =
    E3.f1 with automaton B on bit k of f1 and automaton A on bit i = k + 12 mod 32 of g1 = ROL(f1, 12) ^ y4 (the top
    run i = 12..31 from a guessed state, then the low run i = 0..11 from state 0, which must end in the guess), pruned
    by the joint alive sets of the pair of automata. ev counts the events of SOLVER_UNITS; with a limit, the call stops
    and returns None as soon as its units exceed it (the units spent stay counted)."""
    start = ctr_units(ev)
    ev["calls"] += 1
    om2, t = (om + DY3) & MASK, CTR_TAUS[j]
    ps, th = t ^ ror(t, 1), ctr_theta(t)
    key = [((om >> k & 1) | (om2 >> k & 1) << 1 | (ps >> k & 1) << 2 | (CTR_EPS >> k & 1) << 3) << 4
           | (y4 >> (k + 12) % 32 & 1) | (y9 >> (k + 12) % 32 & 1) << 1 | (ETA >> (k + 12) % 32 & 1) << 2
           | (th >> (k + 12) % 32 & 1) << 3 for k in range(32)]
    out = []
    for guess in range(4):
        ev["guesses"] += 1
        j16, j64 = [0] * 32 + [sum(1 << b * 4 + guess for b in range(4))], [0] * 32 + [0]
        for k in range(31, -1, -1):
            j16[k], j64[k] = ctr_jt(key[k], j16[k + 1], k == 19)
        if not j64[0] >> guess & 1:
            continue
        ev["roots"] += 1
        j64[32] = sum(1 << b * 8 + guess for b in range(4))
        stack = [(0, 0, 0, guess)]
        while stack:
            if limit is not None and ctr_units(ev) - start > limit:
                return None
            k, f, sb, sa = stack.pop()
            ev["pops"] += 1
            if k == 32:
                ev["leaves"] += 1
                h1 = ((rol(f, 12) ^ y4) - y9) & MASK
                if ctr_e3(y4, y9, om, h1, j):
                    ev["goods"] += 1
                    out.append(h1)
                continue
            ev["internal"] += 1
            for x in (1, 0):
                ev["children"] += 1
                nb, na = CTR_TB[(key[k] >> 4) * 8 + sb * 2 + x], CTR_TA[(key[k] & 15) * 8 + sa * 2 + x]
                na = na & 4 if k == 19 else na
                if j64[k + 1] >> nb * 8 + na & 1:
                    ev["pushes"] += 1
                    stack.append((k + 1, f | x << k, nb, na))
    return out
def ctr_events():
    return dict.fromkeys(SOLVER_UNITS, 0)
def ctr_units(ev):
    return sum(SOLVER_UNITS[k] * ev[k] for k in SOLVER_UNITS)
def ctr_dispatch(mask):
    'Units of a passing outer step outside the solver calls: the fourteen tests of the mask bits (shift, AND, branch).'
    return 4 * len(CTR_TAUS)
def ctr_inverse(o, h1):
    'Lemma IP read backwards: the c1 of the outer step o whose trial has E3.h1 = h1.'
    y14 = rol(h1, 16) ^ ((Y3 + o["Y4"]) & MASK)
    y6 = ror(((y14 + o["C2.c1"]) & MASK) ^ o["C2.b1"], 7)
    return (ror(((y6 + o["Y1"] + o["w12"]) & MASK) ^ o["Y12"], 16) + Y11) & MASK
def ctr_good(o, h1, j):
    """A word h1 found for outcome j (Section 9 step 3): c1 by Lemma IP; the trial only if c1 is in Q* and t != 0; then
    E1 of both messages: R = 0 exactly when its differences (beta, a output, c output) are (beta*, tau_j, eps) (Lemma
    D and Lemma E3). Returns (c1, in Q*, t, R = 0)."""
    c1 = ctr_inverse(o, h1)
    if c1 & CTR_MASK != CTR_VALUE:
        return c1, False, None, False
    r = ctr_trial(o, c1)
    if r is None:
        return c1, True, 0, False
    v, d1 = r[3], (c1 - Y11) & MASK
    e = [g(v["Y1"], v["Y6"], y11, v["Y12"], v["w12"], w5) for y11, w5 in ((Y11, v["w5"]), (Y11B, (v["w5"] + DELTA5) & MASK))]
    b1b = ror(v["Y6"] ^ ((Y11B + d1) & MASK), 12)
    return c1, True, r[2], (v["E1.b1"] ^ b1b, e[0][0] ^ e[1][0], e[0][2] ^ e[1][2]) == (CTR_BETA, CTR_TAUS[j], CTR_EPS)
CTR_STEP_CAP = 1 << 23
def ctr_goods_max():
    """Lemma S5 (GPT Sol 6.1 for e7b17fd1): for outcome j at most 2^(32 - n_j) words h1 pass E3, n_j the bits of
    ((sigma ^ eps) & 7fffffff) | (((eta ^ theta) & fff) << 20), each fixed by lower bits of f1. Returns the sum."""
    return sum(1 << 32 - bin(((t ^ ror(t, 1) ^ CTR_EPS) & 0x7FFFFFFF) | ((ETA ^ ctr_theta(t)) & 0xFFF) << 20).count("1")
               for t in CTR_TAUS)
SCAN_UNITS = CTR_MEMBERS * 192
def ctr_scan(o, mask, members=CTR_MEMBERS):
    """The fallback of a passing outer step whose solver units exceed CTR_STEP_CAP: every member c1 of Q* (step CT to
    E3.h1, E3 of both messages, the outcomes of the mask), SCAN_UNITS bounded in words. Returns [(h1, j)]."""
    e1, out = (Y3 + o["Y4"]) & MASK, []
    for n in range(members):
        y6 = ((rol((ctr_c1(n) - Y11) & MASK, 16) ^ o["Y12"]) - o["Y1"] - o["w12"]) & MASK
        h1 = ror((((rol(y6, 7) ^ o["C2.b1"]) - o["C2.c1"]) & MASK) ^ e1, 16)
        out += [(h1, j) for j in range(len(CTR_TAUS)) if mask >> j & 1
                and ctr_e3(o["Y4"], o["Y9"], (e1 + o["w8"]) & MASK, h1, j)]
    return out
def ctr_step(o, mask, cap=CTR_STEP_CAP, members=CTR_MEMBERS):
    """A passing outer step: the solver for each outcome of the mask, in order, while the step's solver units stay at
    most cap; past it the fallback scan does the outcomes not yet done. Returns (pass units, [(h1, j)], scanned)."""
    ev, hs, om = ctr_events(), [], (Y3 + o["Y4"] + o["w8"]) & MASK
    for j in range(len(CTR_TAUS)):
        if mask >> j & 1:
            r = ctr_solve(o["Y4"], o["Y9"], om, j, ev, cap - ctr_units(ev))
            if r is None:
                found = ctr_scan(o, mask >> j << j, members)
                units = ctr_dispatch(mask) + ctr_units(ev) + SCAN_UNITS + SOLVER_UNITS["goods"] * len(found)
                return units, hs + found, True
            hs += [(h, j) for h in r]
    return ctr_dispatch(mask) + ctr_units(ev), hs, False
def ctr_run(rs, budget=None, cap=CTR_STEP_CAP, members=CTR_MEMBERS):
    """The walk of proof.md 9.1 over batches of seven outer steps, each from eight random 256-bit words (ctr_batch); a
    passing step runs ctr_step; its pass units and the units of its goods are counted against the pass budget (the run
    halts, failed, when they would exceed it), and every h1 found goes to ctr_good. Returns (walked, passing, pass
    units, halted, found)."""
    walked = passing = units = 0
    found = []
    for r8 in rs:
        lanes, zs = ctr_batch(r8)
        walked += LANES
        for o, z in zip(lanes, zs):
            if not z:
                continue
            passing += 1
            u, hs, scanned = ctr_step(o, z, cap, members)
            units += u
            if budget is not None and units > budget:
                return walked, passing, units, True, found
            found += [(o, j, h, ctr_good(o, h, j)) for h, j in hs]
    return walked, passing, units, False, found
# 28 planted E3 solutions (y4 in the class, Y9, omega, outcome j, h1), made by the participant's development tool with
# B and C planted and A by rejection (proof.md 9.3); the self-test checks each of them and that the solver finds it.
CTR_FIXTURES = ((0x0DE48DEE,0x7AE638AC,0x13B5CDD5,3,0x6340656A),(0x1E146982,0xBFF927D0,0x94B1FE58,4,0x2EBCFA46),(0x25F46A6A,0x1BCE2014,0x9B7DC445,6,0xE1E878D6),(0x2E1459DA,0xF3B2B12C,0x0B427E53,2,0xB2F43976),(0x3204A652,0x2459F414,0x1ACB3CD3,6,0x897C4B46),(0x39E469C2,0xDFFDF860,0x1D3706B1,4,0xBDC8DA86),(0x3DF48E1E,0x19BDF4C4,0x6FCD364F,3,0xE318869A),(0x4A1445DA,0xE77DBFFC,0x574D073D,6,0xC6B89926),(0x55E44256,0x7F16ECC4,0x2F4697B3,3,0x1FB0059A),(0x560445E2,0x0075B3E0,0x26D5BCB7,4,0xCF508886),(0x5E049A6A,0x5C6D8840,0x26BD3EC6,4,0x8338F26E),(0x5E14B5F6,0x202A2310,0x77C17CBB,0,0x609C5D42),(0x6DE47A7A,0xD43E5830,0xA43483CB,4,0xB278906E),(0x6DE4B9A6,0x9EC97754,0xEEBFD44C,3,0x1FDCA65A),(0x85E47672,0x3F0DDB2C,0x35BBD45E,9,0x17A89B26),(0x91F4B1FA,0xFFE1B030,0xACB143A6,4,0x6FC4A2AE),(0x95E4562A,0xB71AB8A4,0x7BCA17AB,3,0x4CAC0976),(0x95F4B1CA,0xD89A8814,0x9A43845B,6,0x950C1906),(0x9DE44E32,0xA7367B3C,0x155596AC,3,0x5CA04966),(0xA5E4B196,0x42DE103C,0x6F948FD8,9,0xEB68C71A),(0xA9F4B1A6,0x4C520CB4,0x92920527,2,0x326435AA),(0xB9F4A27A,0xDF912344,0x55C5BBC9,2,0x6194FA56),(0xCA14BA5E,0x49B64D04,0xEBBD8FB1,13,0xEB00175A),(0xCE146A42,0x1092C420,0xD4D6FE4D,4,0x3C1439B6),(0xD6048A0E,0x73B27FA0,0xDE08FF5D,4,0xDDF4177A),(0xD604A606,0xB7A257FC,0x995044DD,6,0xAEB4655A),(0xE5F4999E,0xA329DBE4,0x2B75D7BB,7,0x93ACC53A),(0xFDF44592,0x74697354,0x2EFDACDC,3,0x8FCCFA46))
def ctr_reference(y4, y9, om, j):
    'A second enumeration for the self-test: every f1 of automaton B alone (a plain walk), then E3 in full.'
    t, om2, out, stack = CTR_TAUS[j], (om + DY3) & MASK, [], [(0, 0, 0)]
    ps = t ^ ror(t, 1)
    while stack:
        k, f, s = stack.pop()
        if k == 32:
            h1 = ((rol(f, 12) ^ y4) - y9) & MASK
            out += [h1] if ctr_e3(y4, y9, om, h1, j) else []
            continue
        for x in (0, 1):
            nb = CTR_TB[((om >> k & 1) | (om2 >> k & 1) << 1 | (ps >> k & 1) << 2 | (CTR_EPS >> k & 1) << 3) * 8 + s * 2 + x]
            if nb != DEAD:
                stack.append((k + 1, f | x << k, nb))
    return sorted(out)
def ctr_solve_counted(y4, y9, om, j, u0=0, cap=None):
    """ctr_solve executed on the counting machine (Word, Cnt), primitive by primitive as proof.md 9.2 itemizes it:
    keys, joint alive sets read from the tables, the stack walk, and the machine's own bookkeeping (9.2): the register
    u of the step's solver units (u0 before the call; +546 per call, +199 per guess, +5 per root, +11 per push, +49 per
    internal pop, +62 per leaf, +128 per good word) and, at every loop top, the test u > cap. Returns (machine, words,
    u), words None when the cap stops the call. The self-test checks that the units are those of SOLVER_UNITS for
    the events of ctr_solve plus 3 per pop and 1 per call, guess, root, push and good word, and that u and the stop
    are those of ctr_solve."""
    m = Word.m = Cnt()
    m.at("solver")
    y4, y9, om = m.new(y4), m.new(y9), m.new(om)
    u, top = m.new(u0), m.new(MASK << 40 if cap is None else cap)
    t = CTR_TAUS[j]
    ps, th = t ^ ror(t, 1), ctr_theta(t)
    u = u + 546
    om2 = (om + DY3) & MASK
    keys = []
    for k in range(32):
        i = (k + 12) & 31
        kb = ((om >> k) & 1 | ((om2 >> k) & 1) << 1) | ((ps >> k & 1) << 2 | (CTR_EPS >> k & 1) << 3)
        ka = ((y4 >> i) & 1 | ((y9 >> i) & 1) << 1) | ((ETA >> i & 1) << 2 | (th >> i & 1) << 3)
        keys.append(kb << 4 | ka)
        m.tick()                                       # store the key
    out, stack = [], []
    for guess in range(4):
        u = u + 199
        j16, jw = m.new(sum(1 << b * 4 + guess for b in range(4))), [None] * 33
        m.tick(2)                                      # the two start sets are immediates moved into registers
        for k in range(31, -1, -1):
            m.tick()                                   # load key k
            idx = Word(keys[k]) << 16
            m.vals.append(idx); idx.b = idx.l = m.t
            idx = idx | j16
            e = ctr_jt(int(keys[k]), int(j16), k == 19)
            w = m.load(e[0] | e[1] << 16)              # load from the joint alive table
            m.tick()                                   # store the word
            jw[k] = int(w)
            j16 = w & 0xFFFF
        j64 = w >> 16                                  # J_0, still in its register
        root = (j64 >> guess) & 1
        m.branch(root)
        if not root:
            continue
        u = u + 5
        jw[32] = sum(1 << b * 8 + guess for b in range(4)) << 16
        m.tick(3)                                      # root word, its store, the stack count
        stack.append(guess << 42)
        while True:
            m.branch()                                 # loop test (stack count against 0)
            if not stack:
                break
            m.branch(u, top)                           # the cap: u > cap
            if u > top:
                return m, None, int(u)
            m.tick(2)                                  # stack count, load of the entry
            w = m.new(stack.pop())
            k, sb, sa, f = (w >> 32) & 63, (w >> 40) & 3, (w >> 42) & 3, w & MASK
            m.branch(k)                                # leaf test
            if k == 32:
                u = u + 62
                h1 = (rol(f, 12) ^ y4) - y9 & MASK
                g1 = (y9 + h1) & MASK; e2 = (om + ror(y4 ^ g1, 12)) & MASK; g2 = (g1 + ror(h1 ^ e2, 8)) & MASK
                hb = h1 ^ ETA; gb = (y9 + hb) & MASK; eb = (om2 + ror(y4 ^ gb, 12)) & MASK; g2b = (gb + ror(hb ^ eb, 8)) & MASK
                ok = [g1 ^ gb, e2 ^ eb, g2 ^ g2b]
                for d in ok:
                    m.branch(d)
                if [int(d) for d in ok] == [th, CTR_EPS, t]:
                    u = u + 128                        # the good word's charge (its step 3 is ctr_good_counted)
                    out.append(int(h1))
                continue
            u = u + 49
            kk = int(k)
            i = (k + 12) & 31
            m.tick()                                   # load key k
            key = Word(keys[kk]); m.vals.append(key); key.b = key.l = m.t
            kb, ka = key >> 4, key & 15
            m.tick()                                   # load the joint word of k + 1
            jn = Word(jw[kk + 1]); m.vals.append(jn); jn.b = jn.l = m.t
            j64 = jn >> 16
            r = m.load(4 if kk == 19 else 7)           # the reset mask of k
            bb, ba = kb << 3 | sb << 1, ka << 3 | sa << 1
            for x in (1, 0):
                nb = m.load(CTR_TB[int(bb | x)])
                na = m.load(CTR_TA[int(ba | x)]) & r
                hit = (j64 >> (nb << 3 | na)) & 1
                m.branch(hit)
                if hit:
                    nw = (f | Word(x) << k) | (k + 1) << 32 | (nb << 40 | na << 42)
                    m.tick(2)                          # store, stack count
                    u = u + 11
                    stack.append(int(nw))
    return m, out, int(u)
def ctr_good_counted(o, h1, j):
    """ctr_good (step 3) on the counting machine: the outer step's words are loaded, h1 is in a register. Lemma IP back
    to c1 shares the first half of E1 (a1, d1, c1); the test of Q*; t (step CT) and its test; E1 of both messages from
    there, and the three differences, all compared. Returns (machine, ctr_good's tuple)."""
    m = Word.m = Cnt()
    m.at("good")
    h1 = m.new(h1)
    ld = lambda k: m.load(o[k])
    y14 = rol(h1, 16) ^ ((ld("Y4") + Y3) & MASK)
    c2b = ld("C2.b1")
    y6 = ror(((y14 + ld("C2.c1")) & MASK) ^ c2b, 7)
    a1 = (y6 + ld("Y1") + ld("w12")) & MASK
    d1 = ror(a1 ^ ld("Y12"), 16)
    c1 = (d1 + Y11) & MASK
    q = c1 & CTR_MASK
    m.branch(q)
    if q != CTR_VALUE:
        return m, (int(c1), False, None, False)
    k0a = ((((rol(y14, 8) ^ ld("C2.d1")) - ld("C2.a1") - c2b) & MASK) + (IV[0] + IV[4])) & MASK
    t = rol(ld("K0.d1"), 16) ^ k0a
    m.branch(t)
    if t == 0:
        return m, (int(c1), True, 0, False)
    w5 = ld("w5")
    b1 = ror(y6 ^ c1, 12)
    cb = (d1 + Y11B) & MASK
    b1b = ror(y6 ^ cb, 12)
    a2, a2b = (a1 + b1 + w5) & MASK, (a1 + b1b + w5 + DELTA5) & MASK
    c2, c2b = (c1 + ror(d1 ^ a2, 8)) & MASK, (cb + ror(d1 ^ a2b, 8)) & MASK
    ds = b1 ^ b1b, a2 ^ a2b, c2 ^ c2b
    for d in ds:
        m.branch(d)
    return m, (int(c1), True, int(t), tuple(map(int, ds)) == (CTR_BETA, CTR_TAUS[j], CTR_EPS))
def ctr_scan_counted(o, mask, n):
    """Member n of the scan on the counting machine: the outer words and the outcomes' constants are in registers or
    immediates; c1 from the table of Q*, step CT to E3.h1, E3 of both messages, eps first (common to the outcomes),
    then tau_j for each outcome and, for a match, the mask bit and theta_j; the loop. Returns (machine, [(h1, j)])."""
    m = Word.m = Cnt()
    m.at("scan")
    e1, om = m.new((Y3 + o["Y4"]) & MASK), m.new((Y3 + o["Y4"] + o["w8"]) & MASK)
    y4, y9, y12, y1, w12, c2b, c2c = (m.new(o[k]) for k in ("Y4", "Y9", "Y12", "Y1", "w12", "C2.b1", "C2.c1"))
    c1 = m.load(ctr_c1(n))
    y6 = ((rol((c1 - Y11) & MASK, 16) ^ y12) - y1 - w12) & MASK
    h1 = ror((((rol(y6, 7) ^ c2b) - c2c) & MASK) ^ e1, 16)
    g1 = (y9 + h1) & MASK; e2 = (om + ror(y4 ^ g1, 12)) & MASK; g2 = (g1 + ror(h1 ^ e2, 8)) & MASK
    hb = h1 ^ ETA; gb = (y9 + hb) & MASK; eb = (om + DY3 + ror(y4 ^ gb, 12)) & MASK; g2b = (gb + ror(hb ^ eb, 8)) & MASK
    dt, de, dg = g1 ^ gb, e2 ^ eb, g2 ^ g2b
    out = []
    m.branch(de)
    if de == CTR_EPS:
        for j, t in enumerate(CTR_TAUS):
            m.branch(dg)
            if dg == t:
                bit = (Word(mask) >> j) & 1
                m.branch(bit)
                m.branch(dt)
                if bit and dt == ctr_theta(t):
                    m.tick()
                    out.append((int(h1), j))
    m.tick(3)
    return m, out
def ctr_planted(y4, y9, om, h1, n, words):
    """For the self-test: the words of an outer step that the solver, the scan and step CT read, with (y4, Y9, omega)
    given, Y12, Y1, w12 and C2.b1 from words, and C2.c1 solved so that member n of Q* has E3.h1 = h1."""
    o = {"Y4": y4, "Y9": y9, "w8": (om - Y3 - y4) & MASK, "Y12": words[0], "Y1": words[1], "w12": words[2],
         "C2.b1": words[3]}
    y6 = ((rol((ctr_c1(n) - Y11) & MASK, 16) ^ o["Y12"]) - o["Y1"] - o["w12"]) & MASK
    o["C2.c1"] = ((rol(y6, 7) ^ o["C2.b1"]) - (rol(h1, 16) ^ ((Y3 + y4) & MASK))) & MASK
    return o
def ctr_r(text):
    return int.from_bytes(hashlib.shake_256(text.encode()).digest(32), "little")
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
        r = ctr_r("halfsearch v107 trial %s %d" % (seed, case))
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
    # (2) the filter: brute force at width 10, the exact share, real outer steps, the counted step
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
    steps = [[ctr_r("halfsearch v108 batch %s %d %d" % (seed, i, k)) for k in range(8)] for i in range(2340)]
    walked, passing, units, halted, found = ctr_run(steps)
    stop = ctr_run(steps, budget=units // 2)[3]
    counted, shape, regs = 0, None, 0
    for case in range(16):
        r8 = list(steps[case])
        if case >= 8:
            r8[:7] = [sum((0, MASK, x >> 36 * i & MASK)[(x >> 3 * i) % 3] << 36 * i for i in range(LANES)) for x in r8[:7]]
        m, lanes, zs = ctr_count(r8)
        lok = True
        for i, (o, z) in enumerate(zip(lanes, zs)):
            p = ctr_outer([r8[k] >> 36 * i & MASK for k in range(7)] + [0], ((r8[7] >> 36 * i & CTR_FREEM | CTR_E1) - Y3) & MASK)
            lok &= all(o[k] == p[k] for k in p) and z == ctr_filter(p["Y9"], p["Y4"], p["w8"])
        shape = shape or dict(m.units)
        counted += lok and m.units == shape
        regs = max(regs, m.registers() + 2)
    rep["filter"] = {"brute_force_right": ok, "exact_share": share, "share_right": share == CTR_SHARE,
                     "share_log2": round(math.log2(share) - 64, 6), "states": [[len(t) >> 8 for t in fq], [len(t) >> 8 for t in fe]],
                     "steps": walked, "passing": passing, "pass_units": units, "budget_halt_right": stop,
                     "counted_steps_right": counted, "units": shape, "registers": regs}
    good &= ok == 128 and share == CTR_SHARE and not halted and stop and counted == 16 and regs <= 64
    # (3) the solver: the planted solutions, a second enumeration, the cap and the scan
    fixed = sum(ctr_e3(y4, y9, om, h1, j) and ((Y3 + y4) & MASK) & CTR_CLASS == CLASS_VALUE & CTR_CLASS
                and (ctr_look(fq, y9) & ctr_look(fe, om)) >> j & 1 and h1 in ctr_solve(y4, y9, om, j, ctr_events())
                for y4, y9, om, j, h1 in CTR_FIXTURES)
    calls = [(y4, y9, om, j) for y4, y9, om, j, h1 in CTR_FIXTURES[:6]]
    for r8 in steps:
        for o, z in zip(*ctr_batch(r8)):
            om = (Y3 + o["Y4"] + o["w8"]) & MASK
            calls += [(o["Y4"], o["Y9"], om, j) for j in range(len(CTR_TAUS)) if z >> j & 1][:2]
    calls = calls[:30]
    agree = sum(sorted(ctr_solve(*c, ctr_events())) == ctr_reference(*c) for c in calls)
    y4, y9, om, j, h1 = CTR_FIXTURES[0]
    o = ctr_planted(y4, y9, om, h1, 777, (1, 2, 3, 4))
    u, hs, scanned = ctr_step(o, 1 << j, cap=0, members=1 << 10)
    scanned = scanned and (h1, j) in hs
    rep["solver"] = {"fixtures": len(CTR_FIXTURES), "fixtures_found": fixed, "second_enumeration_agree": agree,
                     "second_enumeration_calls": len(calls), "cap_path": scanned and u > SCAN_UNITS,
                     "goods_max": ctr_goods_max(), "units": SOLVER_UNITS}
    rep["solver"]["eps_n_0"] = ETA ^ CTR_EPS ^ rol(CTR_BETA ^ CTR_EPS, 1) == 0
    good &= fixed == len(CTR_FIXTURES) and agree == len(calls) and rep["solver"]["cap_path"] and rep["solver"]["eps_n_0"]
    # (4) the solver, step 3 and the scan counted primitive by primitive against their charges (9.2)
    same = stops = regs = 0
    for c in calls:
        ev = ctr_events()
        hs = ctr_solve(*c, ev)
        m, ws, u = ctr_solve_counted(*c)
        bk = 3 * ev["pops"] + ev["calls"] + ev["guesses"] + ev["roots"] + ev["pushes"] + ev["goods"]
        same += (m.units["solver"] == ctr_units(ev) - SOLVER_UNITS["goods"] * ev["goods"] + bk and u == ctr_units(ev)
                 and sorted(ws) == sorted(hs))
        regs = max(regs, m.registers())
        ev = ctr_events()
        stopped = ctr_solve(*c, ev, 1500) is None
        m, ws, u = ctr_solve_counted(*c, 0, 1500)
        bk = 3 * ev["pops"] + ev["calls"] + ev["guesses"] + ev["roots"] + ev["pushes"] + ev["goods"] + 2 * stopped
        stops += (ws is None) == stopped and u == ctr_units(ev) and m.units["solver"] == (
            ctr_units(ev) - SOLVER_UNITS["goods"] * ev["goods"] + bk)
    words = [(o, h, j) for o, j, h, res in found]
    for case in range(64):
        r = ctr_r("halfsearch v107 good %s %d" % (seed, case))
        o = ctr_outer(ctr_eight(r))
        tr = ctr_trial(o, ctr_c1(r >> 240 & CTR_MEMBERS - 1))
        words.append((o, tr[3]["E3.h1"] if tr and case % 2 else r >> 200 & MASK, case % len(CTR_TAUS)))
    gu, gs = 0, 0
    for o, h, j in words:
        m, res = ctr_good_counted(o, h, j)
        gs += res == ctr_good(o, h, j)
        gu, regs = max(gu, m.units["good"]), max(regs, m.registers())
    su, ss, sn = 0, 0, 0
    for case, (y4, y9, om, j, h1) in enumerate(CTR_FIXTURES):
        rr = struct.unpack("<5I", hashlib.shake_256(("halfsearch scan %s %d" % (seed, case)).encode()).digest(20))
        n = rr[0] & CTR_MEMBERS - 1
        o = ctr_planted(y4, y9, om, h1, n, rr[1:])
        for mask in ((1 << len(CTR_TAUS)) - 1, ((1 << len(CTR_TAUS)) - 1) ^ 1 << j):
            m, out = ctr_scan_counted(o, mask, n)
            want = [(h1, j)] if mask >> j & 1 else []
            want += [(h1, i) for i in range(len(CTR_TAUS)) if i != j and mask >> i & 1 and ctr_e3(y4, y9, om, h1, i)]
            ss, su, sn = ss + (sorted(out) == sorted(want)), max(su, m.units["scan"]), sn + 1
    rep["counted"] = {"solver_calls": len(calls), "solver_same": same, "cap_stops_same": stops,
                      "good_words": len(words), "good_same": gs,
                      "good_max_units": gu, "scan_members": sn, "scan_same": ss, "scan_max_units": su,
                      "registers": regs}
    good &= same == stops == len(calls) and gs == len(words) and gu + 1 <= SOLVER_UNITS["goods"] and ss == sn
    good &= su <= SCAN_UNITS // CTR_MEMBERS and regs <= 64
    rep["ledger"] = ctr_ledger(shape)
    good &= rep["ledger"]["claim_exact"] and X_MAX == 56 + CTR_STEP_CAP + 14 * 1600 + SCAN_UNITS + SOLVER_UNITS["goods"] * ctr_goods_max()
    return rep, good
SEL_OPS = 116 * (1 << 56) + 116 * ((1 << 52) + (1 << 10)) + (1 << 50)
ONE_TIME = 1 << 38
FINAL = 1 << 38
def ctr_time(shape):
    """proof.md Section 11, as a fraction: T = (RUN_OUTER_STEPS / 7 * (batch + filter + loop) + PASS_SCALE *
    (PASS_BUDGET + X_MAX) + ONE_TIME) / 430 + FINAL + SEL_OPS / 430 (steps 1 and 2 of 47804be2's selection, Section 12)."""
    from fractions import Fraction
    walk = shape["batch"] + shape["filter"] + LOOP_UNITS
    return (Fraction(RUN_OUTER_STEPS // LANES * walk + ONE_TIME, 430) + FINAL + Fraction(SEL_OPS, 430)
            + Fraction(PASS_SCALE[0] * (PASS_BUDGET + X_MAX), PASS_SCALE[1] * 430))
def ctr_ledger(shape):
    T = ctr_time(shape)
    lg = math.log2(T.numerator) - math.log2(T.denominator)
    claim = math.ceil(lg * 1e5)
    p, q = T.numerator ** 100000, T.denominator ** 100000     # 2^(claim - 1) < T^100000 < 2^claim, in integers
    return {"claim_exact": q << claim - 1 < p < q << claim and RUN_OUTER_STEPS % LANES == 0, "batch": shape["batch"],
            "filter": shape["filter"], "loop": LOOP_UNITS,
            "run_outer_steps": RUN_OUTER_STEPS, "pass_premise": "%d/%d" % PASS_PREMISE, "pass_budget": PASS_BUDGET,
            "pass_scale": "%d/%d" % PASS_SCALE, "x_max": X_MAX, "lambda": "%d/%d" % LAMBDA, "factor": CTR_FACTOR,
            "time_log2": round(lg, 7), "claim": claim / 1e5}
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
