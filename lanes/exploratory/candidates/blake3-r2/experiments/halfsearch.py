'Half-collisions of 2-round BLAKE3 inside one difference class, and a small residual search.'
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
RULES = {4: ((0x00000001, 0), (0x00000002, 1), (0x00010000, 0), (0x00020000, 0))}
RULES[6] = RULES[4] + ((0x00000404, 1), (0x00000808, 1))
RULES[8] = RULES[6] + ((0x01001008, 0), (0x02002040, 0))
RULE_CONDITIONS = 8
RULE_A = RULES[RULE_CONDITIONS]
A_PLANS = {4: ((), 0x03000300), 6: (((24, 0x0C000000),), 0x0F000300),
           8: (((12, 0x0003C000), 12, (13, 0x40010000)), 0x4F010300)}
A_STEPS, A_ALL = A_PLANS[RULE_CONDITIONS]
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
LANES, LANE_BITS = 7, 36
REGISTERS = 16
KEPT = 9
LANE = (1 << LANE_BITS) - 1
WORD = (1 << 256) - 1
ONES = sum(1 << (LANE_BITS * i) for i in range(LANES))
BATCHES = (CLASS_SIZE + LANES - 1) // LANES
def rule_a(h1):
    'Rule A on the word h1, the first-half d value of E3 on message A.'
    return all(bin(h1 & mask).count("1") & 1 == value for mask, value in RULE_A)
def rule_a_constants():
    'Lemma A: rule A as a test on z, the XOR of the fifth and the second value of C2, for this sub-class.'
    rule = [(rol(mask, 24), rol(mask, 16), value) for mask, value in RULE_A]
    width, mid = 5 * LANE_BITS, 2 * LANE_BITS
    y, s, reach = [1 << p for p in range(width)], None, 0
    def shifted(x, d):
        return [x[p - d] if 0 <= p - d < width else 0 for p in range(width)]
    for step in A_STEPS:
        if isinstance(step, tuple):
            s = [v if step[1] >> p % LANE_BITS & 1 else 0 for p, v in enumerate(shifted(y, step[0]))]
        else:
            s = shifted(s, step)
        reach += abs(step[0] if isinstance(step, tuple) else step)
        y = [a ^ b for a, b in zip(y, s)]
    def reduced(bits, combination, basis):
        for b, c in basis:
            if bits ^ b < bits:
                bits, combination = bits ^ b, combination ^ c
        return bits, combination
    basis, independent, flip = [], [], []
    for i, (bits, _, _) in enumerate(rule):
        basis.append(reduced(bits, 1 << i, basis))
        if not basis[-1][0]:
            raise ValueError("rule A: a condition follows from the others")
    for t in range(LANE_BITS):
        if A_ALL >> t & 1:
            if reach > mid or y[mid + t] & (1 << mid) - 1 or y[mid + t] >> mid + 32:
                raise ValueError("rule A: a read position holds a bit of another lane or a bit above 31")
            bits, combination = reduced(y[mid + t] >> mid, 0, basis)
            independent.append(reduced(combination, 0, independent))
            if bits or not independent[-1][0]:
                raise ValueError("rule A: a read position does not hold a new combination of the conditions")
            chosen = [r for i, r in enumerate(rule) if combination >> i & 1]
            flip.append((t, sum(r[2] for r in chosen) & 1, sum(1 << i for i in range(32)
                                                              if sum(r[1] >> i & 1 for r in chosen) & 1)))
    if A_ALL >> 32 or len(flip) != len(rule):
        raise ValueError("rule A: the read positions are not the rule")
    return tuple(step[1] for step in A_STEPS if isinstance(step, tuple)), tuple(flip)
A_MASKS, A_FLIP = rule_a_constants()
A_FREE = tuple(i for i in CLASS_FREE if any(m >> i & 1 for _, _, m in A_FLIP))
def rule_word(y4):
    'The lane of the list V for class member y4 (Lemma A): a 1 at every read position whose wanted bit is 0.'
    e1 = (Y3 + y4) & MASK
    return sum((1 ^ c ^ bin(e1 & m).count("1") & 1) << t for t, c, m in A_FLIP)
BATCH_WORDS = (["A16", "B16", "A12", "B12"] + ["A mask %d" % (n + 1) for n in range(len(A_MASKS))]
               + ["A all", "A carry", "not bit 32", "X2+w7", "w0",
                  "end of list", "-w2", "ROL(X15,8)", "S10+X15", "X14", "stage-2 budget", "A8", "B8", "A7", "B7",
                  "-X15", "S5", "w3", "X13", "X9", "S12", "w12-S1-S6", "Y11", "Y11'", "w5", "w5+delta", "A31",
                  "eta", "M", "bit 32"])
RESIDENT = tuple(BATCH_WORDS if KEPT is None else BATCH_WORDS[:KEPT])
EVICT = () if KEPT is None else RESIDENT[5:]
RC_AGAIN = bool(KEPT)
Z_AGAIN = bool(KEPT and A_STEPS)
A_OPS = sum(3 if isinstance(step, tuple) else 2 for step in A_STEPS)
TABLES = {
    "outer step": (("next w5", 6, 6, 2, 2), ("K2 and D3", 67, 39, 9, 4), ("K3", 43, 25, 4, 7),
                   ("C0 and D2", 32, 21, 6, 5)),
    "table build": (("build loop", 3, 1, 0, None), ("build C0", 13, 11, 2, 3), ("build D1", 27, 14, 3, 4)),
    "middle step": (("next X2", 6, 7, 2, 2), ("D2 and K1", 47, 15, 4, 8), ("K0", 32, 9, 3, 6),
                    ("class loop entry", 0, len(RESIDENT), 0, None)),
    "batch": (("loop", 3, 1, 0, None), ("X0 to X10", 3, 4, 0, 3), ("C2 to z", 17, 2 + len(A_MASKS), 0, 4),
              ("rule A", 6 + A_OPS, 1, 0, 2), ("entry count", 3, 1, 0, None),
              ("C2, rest", 13 + 4 * Z_AGAIN, 4 + 3 * Z_AGAIN, 0, 5), ("C1 to Y1", 31, 8, 0, 5),
              ("E1, A and B", 41, 6, 0, 9), ("E1 test", 13, 4, 0, 2), ("restore", 0, len(EVICT), 0, None)),
}
STAGE_A_PARTS = 4
STAGE_2_LOG2_SHARE = len(RULE_A) - 3
CTR_FLAGS = 3
CTR_MASK, CTR_VALUE, CTR_BETA = 0x0E09818B, 0x02008000, 0x18B0E098
CTR_FREE = tuple(i for i in range(32) if not CTR_MASK >> i & 1)
CTR_BASIS = ("C0.d1", "D2.a1", "D2.b1", "S11", "S4", "X9", "w6")
CTR_MEMBERS = 1 << len(CTR_FREE)
CTR_WORDS = -(-CTR_MEMBERS // LANES)
CTR_FACTOR = (67698688 << 11) * 5 // 7
RUN_OUTER_STEPS = -(-(12419 << 128) // (25000 * CTR_FACTOR * (CTR_MEMBERS - 1)))
# The seven beta* outcomes (tau, eps) of E1 with n = 0 and their counts in units of 2^16 (pkg10 a15 count, sum as in
# CTR_FACTOR); CTR_SHARE / 2^64 = 2^-9.8132, the exact share of words (Q, E) that pass the filter (the self-test
# recounts it from this program's own tables); the pass budget is that share of RUN_OUTER_STEPS times the margin 17/16.
# Only passing steps run their cube enumeration, so STAGE_2_BUDGET (stage-2 entries) is one word in 32 of the words
# enumerated in at most CTR_PASS_BUDGET passing steps.
CTR_TAUS = (0x175020A0, 0x185020A0, 0x275020A0, 0x285020A0, 0x385020A0, 0x675020A0, 0x685020A0)
CTR_EPS, CTR_MASS = 0x6E21BE55, (96, 256, 16, 384, 256, 1, 24)
CTR_SHARE = 20504986129465344
CTR_PASS_BUDGET = RUN_OUTER_STEPS * CTR_SHARE * 17 >> 68
STAGE_2_BUDGET = (CTR_PASS_BUDGET * CTR_WORDS) >> STAGE_2_LOG2_SHARE
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
def table_row(o, y4):
    'The five words that the table of an outer step holds for one member.'
    r = member(o, y4)
    return {"XA": (r["C0.a1"] - o["X4"]) & MASK, "X6": r["X6"], "X1": r["X1"], "R": rol(r["D1.d1"], 16), "Y12": r["Y12"]}
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
def rep(v):
    'The 32-bit value v in every lane of a packed word.'
    return (v & MASK) * ONES
def pack(values):
    'A packed word with the given 32-bit values in its lanes.'
    return sum((v & MASK) << (LANE_BITS * i) for i, v in enumerate(values))
def lanes(z):
    'The seven lanes of a packed word.'
    return [(z >> (LANE_BITS * i)) & LANE for i in range(LANES)]
class Packed:
    'A 256-bit word in a register: its value, the step that made it and the step of its last use.'
    __slots__ = ("z", "born", "last")
    def __init__(self, z, born):
        self.z, self.born, self.last = z, born, born
class Machine:
    'The counting machine of proof.md Section 6.5.'
    def __init__(self):
        self.ops, self.loads, self.stores, self.uses, self.sums = {}, {}, {}, {}, {}
        self.part, self.step, self.values, self.memory, self.kept = None, 0, [], {}, {}
    def at(self, part):
        self.part = part
        self.ops[part] = self.loads[part] = self.stores[part] = self.uses[part] = self.sums[part] = 0
    def value(self, z, *used):
        self.step += 1
        for operand in used:
            operand.last = self.step
        self.values.append(Packed(z, self.step))
        return self.values[-1]
    def load(self, constant):
        self.loads[self.part] += 1
        return self.value(constant)
    def k(self, name):
        'The memory word of that name as an operand: its register if it is kept in one, a load otherwise.'
        if name in self.kept:
            self.uses[self.part] += 1
            return self.kept[name]
        return self.load(self.memory[name])
    def get(self, *names):
        'Fetch memory words, one load each, and keep them in registers. Nothing is kept when KEPT is 0.'
        for name in names if KEPT != 0 else ():
            if name not in self.kept:
                self.kept[name] = self.load(self.memory[name])
    def drop(self, names):
        'The registers of these kept words are free from here on.'
        self.step += 1
        for name in names:
            if name in self.kept:
                self.kept.pop(name).last = self.step
    def resident(self, names):
        'The words that the class loop entry left in registers; their loads are counted there.'
        for name in names:
            self.kept[name] = self.value(self.memory[name])
    def finish(self, names=()):
        'The end of a piece. The kept words must be the words named, unchanged; they are held to the last step.'
        if set(self.kept) != set(names) or any(self.kept[name].z != self.memory[name] for name in names):
            raise ValueError("the words in registers at the end of a piece are not its kept words")
        self.step += 1
        for word in self.kept.values():
            word.last = self.step
    def store(self, x):
        'Write a register to memory: one store. Returns the stored word.'
        self.stores[self.part] += 1
        self.step += 1
        x.last = self.step
        return x.z
    def op(self, z, *used):
        self.ops[self.part] += 1
        return self.value(z, *used)
    def add(self, x, y):
        self.sums[self.part] = max(self.sums[self.part], max(a + b for a, b in zip(lanes(x.z), lanes(y.z))))
        return self.op((x.z + y.z) & WORD, x, y)
    def xor(self, x, y):
        return self.op(x.z ^ y.z, x, y)
    def band(self, x, y):
        return self.op(x.z & y.z, x, y)
    def bor(self, x, y):
        return self.op(x.z | y.z, x, y)
    def shr(self, x, r):
        return self.op(x.z >> r, x)
    def shl(self, x, r):
        return self.op((x.z << r) & WORD, x)
    def pror(self, z, r):
        'Rotate every lane right by r: ((z >> r) AND A_r) OR ((z << (32-r)) AND B_r), the masks named Ar and Br.'
        low = self.band(self.shr(z, r), self.k("A%d" % r))
        high = self.band(self.shl(z, 32 - r), self.k("B%d" % r))
        return self.bor(low, high)
    def prol(self, z, r):
        return self.pror(z, 32 - r)
    def advance(self, position):
        "The next value of a counter (the list position, the stage-2 entries), in the counter's own register: one"
        self.ops[self.part] += 1
        self.step += 1
        return Packed(position + 1, self.step)
    def compare_and_branch(self, x, y):
        'The comparison of two registers and the branch on its result: two operations. True when they differ.'
        self.ops[self.part] += 2
        self.step += 1
        x.last = y.last = self.step
        return x.z != y.z
    def registers(self):
        'The largest number of registers in use at one time, for the operations in the order they were made.'
        change = [0] * (self.step + 1)
        for value in self.values:
            change[value.born] += 1
            change[value.last] -= 1
        held = peak = 0
        for delta in change:
            held += delta
            peak = max(peak, held)
        return peak + 2
def list_words(j):
    'The packed words U[j] and V[j] of proof.md Section 6.5 and the seven class members they hold.'
    members = [class_member(min(LANES * j + i, CLASS_SIZE - 1)) for i in range(LANES)]
    return pack(rol(y, 7) for y in members), members, pack(rule_word(y) for y in members)
FIXED = {"M": MASK, "1": 1, "2": 2, "11": 11, "delta": DELTA5, "X3": X3, "X3+1": X3 + 1, "X15": X15, "-X15": -X15,
         "ROL(X15,8)": rol(X15, 8), "ROL(X7,7)": rol(X7, 7), "1-W13": 1 - W13, "X11": X11, "X11+1": X11 + 1,
         "K2.a1+K2.b1": K2A + K2B, "K2.d1": K2D, "K2.c1": K2C, "K2.b1": K2B, "IV3": IV[3], "IV7": IV[7],
         "-IV3-IV7": -IV[3] - IV[7], "-IV1": -IV[1], "IV1+IV5+1": IV[1] + IV[5] + 1, "IV5": IV[5], "IV4": IV[4],
         "-IV0": -IV[0], "-IV0-IV4": -IV[0] - IV[4], "Y11": Y11, "Y11'": Y11B, "eta": ETA,
         "A all": A_ALL, "A carry": -A_ALL, "w5 end": 0, "X2 end": 0}
FIXED.update(("A mask %d" % (n + 1), mask) for n, mask in enumerate(A_MASKS))
for r in (7, 8, 12, 16, 20, 24, 25, 31):
    FIXED["A%d" % r], FIXED["B%d" % r] = (1 << (32 - r)) - 1, ((1 << r) - 1) << (32 - r)
del FIXED["B31"]
def memory(free):
    'The memory before the outer step of the context free.'
    c = {name: rep(value) for name, value in FIXED.items()}
    c["bit 32"], c["not bit 32"] = ONES << 32, ONES * (LANE ^ 1 << 32)
    c["end of list"], c["stage-2 budget"] = BATCHES, STAGE_2_BUDGET
    c.update((name, rep(value)) for name, value in zip(CONTEXT_WORDS, free))
    c["w5"], c["X2"] = rep(free[5] - 1), rep(free[6] - 1)
    return c
def stored(v):
    'What the outer step and the middle step must leave in memory for the context v: two dicts, name -> value.'
    by_outer = {"w5": v["w5"], "w5+delta": v["w5"] + DELTA5, "S10+X15": v["S10"] + X15, "S6": v["S6"], "1-S6": 1 - v["S6"],
                "X14": v["X14"], "S9+1": v["S9"] + 1, "X9": v["X9"], "-X4": -v["X4"], "C0.b1": v["C0.b1"],
                "ROL(S4,7)": rol(v["S4"], 7), "-S11": -v["S11"], "-S2-S7": -v["S2"] - v["S7"], "w7": v["w7"],
                "-C0.b1-w6": -v["C0.b1"] - v["w6"], "-C0.c1": -v["C0.c1"], "ROL(C0.d1,16)": rol(v["C0.d1"], 16),
                "-D2.b1-W13": -v["D2.b1"] - W13, "D2.c1+1": v["D2.c1"] + 1, "X13": v["X13"], "ROL(X13,8)": rol(v["X13"], 8)}
    by_middle = {"X2": v["X2"], "X2+w7": v["X2"] + v["w7"], "w12-S1-S6": v["w12"] - v["S1"] - v["S6"], "-w2": -v["w2"],
                 "w3": v["w3"], "S5": v["S5"], "S12": v["S12"], "w0": v["w0"], "w1": v["w1"]}
    return by_outer, by_middle
def tools(m, c):
    'Four short forms used by the counted pieces, for the machine m with the memory c: name a memory word as an'
    m.memory = c
    def put(name, x):
        c[name] = m.store(x)
    def low(x):
        return m.band(x, m.k("M"))
    def neg(x, plus="1"):
        return m.add(m.xor(x, m.k("M")), m.k(plus))
    return m.k, put, low, neg
def outer_step(m, c):
    'The outer step on the machine m: the next value of w5, the lines of outer(), and the 21 words they leave.'
    k, put, low, neg = tools(m, c)
    m.at("next w5")
    w5 = low(m.add(k("w5"), k("1")))
    m.compare_and_branch(w5, k("w5 end"))
    put("w5", w5)
    put("w5+delta", low(m.add(w5, k("delta"))))
    m.at("K2 and D3")
    s2 = m.add(w5, k("K2.a1+K2.b1"))
    s14 = m.pror(m.xor(s2, k("K2.d1")), 8)
    s10 = m.add(s14, k("K2.c1"))
    put("S10+X15", low(m.add(s10, k("X15"))))
    s6 = m.pror(m.xor(s10, k("K2.b1")), 7)
    put("S6", s6)
    put("1-S6", low(neg(s6, "2")))
    d3d = k("D3.d1")
    d3a = m.xor(m.prol(d3d, 16), s14)
    x14 = m.pror(m.xor(d3d, k("X3")), 8)
    put("X14", x14)
    s9 = k("S9")
    put("S9+1", low(m.add(s9, k("1"))))
    d3c = m.add(d3d, s9)
    x9 = m.add(d3c, x14)
    put("X9", low(x9))
    d3b = neg(d3a, "X3+1")
    x4 = m.pror(m.xor(d3b, x9), 7)
    put("-X4", low(neg(x4)))
    cc = k("C0.c1")
    cb = m.pror(m.xor(x4, cc), 12)
    put("C0.b1", cb)
    s4 = m.xor(m.prol(d3b, 12), d3c)
    put("ROL(S4,7)", m.prol(s4, 7))
    s3 = m.add(d3a, neg(s4))
    m.at("K3")
    s15 = k("S15")
    k3d = m.xor(m.prol(s15, 8), s3)
    k3c = m.add(k3d, k("IV3"))
    s11 = m.add(k3c, s15)
    put("-S11", low(neg(s11)))
    k3b = m.pror(m.xor(k3c, k("IV7")), 12)
    s7 = m.pror(m.xor(k3b, s11), 7)
    put("-S2-S7", low(neg(m.add(s2, s7))))
    k3a = m.xor(m.prol(k3d, 16), k("11"))
    put("w7", low(m.add(s3, neg(m.add(k3a, k3b)))))
    put("-C0.b1-w6", low(neg(m.add(cb, m.add(k3a, k("-IV3-IV7"))))))
    m.at("C0 and D2")
    put("-C0.c1", low(neg(cc)))
    cd = k("C0.d1")
    put("ROL(C0.d1,16)", m.prol(cd, 16))
    x8 = m.add(cc, neg(cd))
    d2b = m.xor(x8, k("ROL(X7,7)"))
    put("-D2.b1-W13", low(neg(d2b, "1-W13")))
    d2c = m.xor(m.prol(d2b, 12), s7)
    put("D2.c1+1", low(m.add(d2c, k("1"))))
    x13 = low(m.add(x8, neg(d2c)))
    put("X13", x13)
    put("ROL(X13,8)", m.prol(x13, 8))
def table_build(m, c, j):
    'The table of an outer step for the seven members of list word U[j], on the machine m: one word of each list.'
    k = tools(m, c)[0]
    m.at("build loop")
    m.compare_and_branch(m.advance(j), k("end of list"))
    m.at("build C0")
    y12 = m.band(m.add(m.xor(m.load(list_words(j)[0]), k("C0.b1")), k("-C0.c1")), k("M"))
    row = {"Y12": m.store(y12)}
    ca = m.add(m.xor(m.prol(y12, 8), k("C0.d1")), k("-C0.b1-w6"))
    row["XA"] = m.store(m.band(m.add(ca, k("-X4")), k("M")))
    x12 = m.xor(ca, k("ROL(C0.d1,16)"))
    m.at("build D1")
    cd1 = m.add(m.xor(x12, k("M")), k("X11+1"))
    bd1 = m.pror(m.xor(cd1, k("S6")), 12)
    row["X6"] = m.store(m.pror(m.xor(bd1, k("X11")), 7))
    dd1 = m.add(cd1, k("-S11"))
    row["X1"] = m.store(m.band(m.xor(m.prol(x12, 8), dd1), k("M")))
    row["R"] = m.store(m.prol(dd1, 16))
    return row
def middle_step(m, c):
    'The middle step on the machine m: the next value of X2, the lines of middle(), and the nine words they leave.'
    k, put, low, neg = tools(m, c)
    m.at("next X2")
    m.get("M", "1", "A16", "B16")
    x2 = low(m.add(k("X2"), k("1")))
    m.compare_and_branch(x2, k("X2 end"))
    put("X2", x2)
    put("X2+w7", low(m.add(x2, k("w7"))))
    m.at("D2 and K1")
    d2a = m.add(x2, k("-D2.b1-W13"))
    d2d = m.xor(x2, k("ROL(X13,8)"))
    s13 = m.xor(m.prol(d2d, 16), d2a)
    k1c = neg(s13, "S9+1")
    k1d = m.add(k1c, k("-IV1"))
    s1 = m.xor(m.prol(s13, 8), k1d)
    put("w12-S1-S6", low(m.add(m.add(d2a, k("-S2-S7")), neg(s1, "1-S6"))))
    k1a = m.prol(k1d, 16)
    put("-w2", low(neg(k1a, "IV1+IV5+1")))
    k1b = m.pror(m.xor(k1c, k("IV5")), 12)
    put("w3", low(m.add(s1, neg(m.add(k1a, k1b)))))
    put("S5", m.pror(m.xor(k1b, k("S9")), 7))
    m.at("K0")
    s8 = neg(d2d, "D2.c1+1")
    k0b = m.xor(s8, k("ROL(S4,7)"))
    k0c = m.xor(m.prol(k0b, 12), k("IV4"))
    s12 = low(m.add(s8, neg(k0c)))
    put("S12", s12)
    k0d = m.add(k0c, k("-IV0"))
    k0a = m.prol(k0d, 16)
    put("w0", low(m.add(k0a, k("-IV0-IV4"))))
    s0 = m.xor(m.prol(s12, 8), k0d)
    put("w1", low(m.add(s0, neg(m.add(k0a, k0b)))))
    m.drop(list(m.kept))
    m.at("class loop entry")
    m.get(*RESIDENT)
    m.finish(RESIDENT)
def lane_flags(m, c, word):
    'The end of stage 2: bit 32 of every lane of word + M, set where the reduced word is nonzero, and the branch.'
    k = tools(m, c)[0]
    flags = m.band(m.add(word, k("M")), k("bit 32"))
    taken = m.compare_and_branch(flags, k("bit 32"))
    return [(flags.z >> (LANE_BITS * i + 32)) & 1 for i in range(LANES)], taken
def rule_a_flags(m, c, z, v):
    'The end of stage A (Lemma A) for seven lanes z and the word v of the list V: the flags of rule A, the branch.'
    k = tools(m, c)[0]
    y, s, n = z, None, 0
    for step in A_STEPS:
        if isinstance(step, tuple):
            n, d = n + 1, step[0]
            s = m.band(m.shl(y, d) if d > 0 else m.shr(y, -d), k("A mask %d" % n))
        else:
            s = m.shl(s, step) if step > 0 else m.shr(s, -step)
        y = m.xor(y, s)
    s = m.add(m.band(m.xor(y, m.load(v)), k("A all")), k("A carry"))
    taken = m.compare_and_branch(m.bor(s, k("not bit 32")), k("not bit 32"))
    return [1 - (s.z >> (LANE_BITS * i + 32) & 1) for i in range(LANES)], taken
def packed_batch(m, c, row, j, entered=0):
    'The two-stage batch of proof.md Section 6.5 for the seven trials of batch j, counted on the machine m.'
    k = tools(m, c)[0]
    def drop(*names):
        m.drop([name for name in names if name not in RESIDENT])
    m.resident(RESIDENT)
    m.at("loop")
    m.compare_and_branch(m.advance(j), k("end of list"))
    m.at("X0 to X10")
    dd0 = m.xor(m.add(m.load(row["XA"]), k("-w2")), k("ROL(X15,8)"))
    x10 = m.add(dd0, k("S10+X15"))
    m.at("C2 to z")
    x6 = m.load(row["X6"])
    ra = m.add(x6, k("X2+w7"))
    rd = m.pror(m.xor(ra, k("X14")), 16)
    rc = m.add(x10, rd)
    rb = m.pror(m.xor(x6, rc), 12)
    z = m.xor(rd, m.add(m.add(ra, rb), k("w0")))
    m.at("rule A")
    flags_a, taken_a = rule_a_flags(m, c, z, list_words(j)[2])
    m.at("entry count")
    m.drop(EVICT)
    m.compare_and_branch(m.advance(entered), k("stage-2 budget"))
    m.at("C2, rest")
    if Z_AGAIN:
        z = m.xor(rd, m.add(m.add(m.add(m.load(row["X6"]), k("X2+w7")), rb), k("w0")))
    if RC_AGAIN:
        rc = m.add(x10, rd)
    m.get("A8", "B8")
    y14 = m.pror(z, 8)
    m.get("A7", "B7")
    y6 = m.pror(m.xor(m.add(rc, y14), rb), 7)
    m.at("C1 to Y1")
    bd0 = m.pror(m.xor(m.add(x10, k("-X15")), k("S5")), 12)
    x5 = m.pror(m.xor(bd0, x10), 7)
    drop("A7", "B7")
    qa = m.add(m.add(x5, m.load(row["X1"])), k("w3"))
    qd = m.pror(m.xor(qa, k("X13")), 16)
    qc = m.add(qd, k("X9"))
    qb = m.pror(m.xor(x5, qc), 12)
    y1 = m.add(m.add(qa, qb), m.xor(m.load(row["R"]), k("S12")))
    m.at("E1, A and B")
    a1 = m.add(m.add(y1, y6), k("w12-S1-S6"))
    d1 = m.pror(m.xor(a1, m.load(row["Y12"])), 16)
    c1 = m.add(d1, k("Y11"))
    b1 = m.pror(m.xor(c1, y6), 12)
    a2 = m.add(m.add(k("w5"), a1), b1)
    c2 = m.add(c1, m.pror(m.xor(a2, d1), 8))
    c1b = m.add(d1, k("Y11'"))
    b1b = m.pror(m.xor(c1b, y6), 12)
    a2b = m.add(m.add(k("w5+delta"), a1), b1b)
    beta = m.xor(b1, b1b)
    c2b = m.add(c1b, m.pror(m.xor(a2b, d1), 8))
    drop("A8", "B8")
    m.at("E1 test")
    eps = m.xor(c2, c2b)
    x = m.xor(beta, eps)
    rot = m.bor(m.band(m.shr(x, 31), k("A31")), m.shl(x, 1))
    m.get("M", "bit 32")
    word = m.band(m.xor(m.xor(rot, eps), k("eta")), k("M"))
    flags, taken = lane_flags(m, c, word)
    drop("M", "bit 32")
    if EVICT:
        m.at("restore")
        m.get(*EVICT)
    m.finish(RESIDENT)
    return lanes(word.z), flags, taken, flags_a, taken_a
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
def reference(v, y4):
    "What the batch must show for one trial, taken from the compressions of the trial's two real messages."
    words = trial(v, y4)[0]
    first, second = messages(words)
    (wa, da, ya), (wb, db, yb) = compress2(first), compress2(second)
    r = [p ^ q for p, q in zip(da, db)]
    h1 = ror(ya[14] ^ ((ya[3] + ya[4] + wa[15]) & MASK), 16)
    outs = []
    for mw, y in ((wa, ya), (wb, yb)):
        a1 = (y[1] + y[6] + mw[12]) & MASK
        b1 = ror(y[6] ^ ((y[11] + ror(y[12] ^ a1, 16)) & MASK), 12)
        outs.append((b1, g(y[1], y[6], y[11], y[12], mw[12], mw[5])[2]))
    beta, eps = outs[0][0] ^ outs[1][0], outs[0][1] ^ outs[1][1]
    return {"y4": ya[4], "h1": h1, "word": ETA ^ eps ^ rol(beta ^ eps, 1), "word_from_digests": r[3] ^ rol(r[6], 8),
            "half": int(r[0] == 0 and r[2] == 0 and r[5] == 0 and r[7] == 0 and ya[4] == yb[4]),
            "words": int(wa == words and len(first) == LEN_A and len(second) == LEN_B)}
def batch_check(free, j):
    'The four counted pieces for the context free and batch j of the class, each on a new machine.'
    v, c = context(free), memory(free)
    machines = {name: Machine() for name in TABLES}
    outer_step(machines["outer step"], c)
    row = table_build(machines["table build"], c, j)
    middle_step(machines["middle step"], c)
    m = machines["batch"]
    words, flags, taken, flags_a, taken_a = packed_batch(m, c, row, j)
    members = list_words(j)[1]
    by_outer, by_middle = stored(v)
    rows = [table_row(v, y4) for y4 in members]
    kept = int(all(c[name] == rep(value) for group in (by_outer, by_middle) for name, value in group.items())
               and row == {name: pack(r[name] for r in rows) for name in rows[0]})
    refs = [reference(v, y4) for y4 in members]
    passing = [int(rule_a(r["h1"])) for r in refs]
    right = sum(int(r["words"] == 1 and r["y4"] == members[i] and r["half"] == 1 and flags_a[i] == 1 - passing[i]
                    and words[i] == r["word"] and r["word"] == r["word_from_digests"] and flags[i] == int(r["word"] != 0))
                for i, r in enumerate(refs))
    zero = sum(int(r["word"] == 0) for r in refs)
    if not kept or taken_a != (1 in passing) or taken != (zero > 0):
        right = 0
    parts = list(m.ops)
    stage_a, stage_2 = parts[:STAGE_A_PARTS], parts[STAGE_A_PARTS:]
    return {"stage_a_operations": sum(m.ops[p] for p in stage_a), "stage_a_loads": sum(m.loads[p] for p in stage_a),
            "stage_2_operations": sum(m.ops[p] for p in stage_2), "stage_2_loads": sum(m.loads[p] for p in stage_2),
            "lanes_right": right, "lanes_passing_rule_a": sum(passing), "stage_2_entered": int(taken_a),
            "zero_test_words": zero, "stored_right": kept}, machines
def seeded(seed):
    'The seven words of a context and a class member number from the organizer seed.'
    stream = struct.unpack("<8I", hashlib.shake_256(seed).digest(32))
    return stream[:7], stream[7] % CLASS_SIZE
def half_collision(seed):
    free, k = seeded(seed)
    return messages(trial(context(free), class_member(k))[0]) + ({},)
def residual_search(seed):
    free, k0 = seeded(seed)
    checked = batch_check(free, k0 // LANES)[0]
    counted = {"batch_" + key: checked[key] for key in ("stage_a_operations", "stage_a_loads", "stage_2_operations",
                                                        "stage_2_loads", "lanes_right", "stage_2_entered")}
    v = context(free)
    for step in range(CLASS_SIZE):
        y4 = class_member((k0 + step) % CLASS_SIZE)
        words, values = trial(v, y4)
        if residual_word1(v, words, values, y4) & 0xFF == 0:
            return messages(words) + (dict(counted, tries=step + 1),)
    return None, None, dict(counted, tries=CLASS_SIZE)
def flags_right():
    'lane_flags on all 128 patterns of zero and nonzero lanes; random cases hardly ever have a zero lane.'
    c = {"M": rep(MASK), "bit 32": ONES << 32}
    right = 0
    for pattern in range(1 << LANES):
        words = [0 if pattern >> i & 1 else (MASK, 1, 0x80000000)[i % 3] for i in range(LANES)]
        m = Machine()
        m.at("E1 test")
        flags, taken = lane_flags(m, c, m.load(pack(words)))
        right += int(flags == [int(v != 0) for v in words] and taken == (pattern != 0))
    return right
def rule_a_right():
    'The stage-A test on all patterns of the bits that rule A reads: a complete enumeration for Lemma A.'
    read = [i for i in range(32) if any(rol(mask, 24) >> i & 1 for mask, _ in RULE_A)]
    spots = [CLASS_FREE.index(i) for i in A_FREE]
    c = {name: value for name, value in memory([0] * 7).items() if name.startswith(("A ", "not bit"))}
    total, right, satisfied = 1 << len(read) + len(spots), 0, 0
    for pattern in range(total):
        fill = struct.unpack("<14I", hashlib.shake_256(b"rule A %d" % pattern).digest(56))
        zs, vs, passing = [], [], []
        for lane in range(LANES):
            number, z, k = (pattern + 37 * lane) % total, fill[lane], fill[7 + lane] % CLASS_SIZE
            for n, i in enumerate(read):
                z = z & ~(1 << i) | (number >> n & 1) << i
            for n, i in enumerate(spots):
                k = k & ~(1 << i) | (number >> len(read) + n & 1) << i
            y4 = class_member(k)
            zs.append(z | (fill[7 + lane] >> 30) << 32)
            vs.append(rule_word(y4))
            passing.append(int(rule_a(ror(ror(z, 8) ^ (Y3 + y4) & MASK, 16))))
        m = Machine()
        m.at("rule A")
        flags, taken = rule_a_flags(m, c, m.load(sum(v << (LANE_BITS * i) for i, v in enumerate(zs))), pack(vs))
        right += int(flags == [1 - p for p in passing] and taken == (1 in passing) and m.sums["rule A"] <= LANE)
        satisfied += int(1 in passing)
    return total, right, satisfied
def ctr_c1(j):
    'E1.c1 of cube member j: the bits of j fill the free positions of (c1 AND CTR_MASK) = CTR_VALUE in increasing order.'
    c1 = CTR_VALUE
    for n, i in enumerate(CTR_FREE):
        c1 |= (j >> n & 1) << i
    return c1
def ctr_outer(eight):
    'The unstarred lines of the counter order, in its sequence, for the words of CTR_BASIS and member number eight[7].'
    v = dict(zip(CTR_BASIS, eight), Y4=class_member(eight[7] % CLASS_SIZE))
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
CTR_TABLE = (("loop", 3, 1, 0), ("cube word to Y14", 9, 1, 0), ("z", 5, 1, 0), ("rule A", 14, 7, 0),
             ("entry count", 3, 1, 0), ("E1, A and B", 34, 14, 0), ("E1 test", 13, 7, 0))
CTR_RESIDENT = ("Y12", "-Y1-w12", "A25", "B25", "C2.b1", "-C2.c1", "A24")
def ctr_table_word(j):
    'Word j of the run-wide table: ROL(E1.d1, 16) and E1.d1 = c1 - Y11 of cube members 7j to 7j + 6, and their c1.'
    c1s = [ctr_c1(min(LANES * j + i, CTR_MEMBERS - 1)) for i in range(LANES)]
    d1s = [(c1 - Y11) & MASK for c1 in c1s]
    return pack(rol(d, 16) for d in d1s), pack(d1s), c1s
def ctr_memory(o):
    'The memory of the counter batch for the outer step o: the fixed words, the end of the table, the budget, eight words.'
    c = {name: rep(value) for name, value in FIXED.items()}
    c["bit 32"], c["not bit 32"] = ONES << 32, ONES * (LANE ^ 1 << 32)
    c["end of list"], c["stage-2 budget"] = CTR_WORDS, STAGE_2_BUDGET
    c.update((name, rep(value)) for name, value in (
        ("Y12", o["Y12"]), ("-Y1-w12", -o["Y1"] - o["w12"]), ("C2.b1", o["C2.b1"]), ("-C2.c1", -o["C2.c1"]),
        ("w5", o["w5"]), ("w5+delta", o["w5"] + DELTA5), ("beta", CTR_BETA), ("V", rule_word(o["Y4"]))))
    return c
def ctr_batch(m, c, j, entered=0):
    'The two-stage batch of the counter trial for table word j, counted on the machine m; entered: stage-2 entries so far.'
    k = tools(m, c)[0]
    rt, d1, _ = ctr_table_word(j)
    m.resident(CTR_RESIDENT)
    m.at("loop")
    more = m.compare_and_branch(m.advance(j), k("end of list"))
    m.at("cube word to Y14")
    a1 = m.xor(m.load(rt), k("Y12"))
    y6 = m.add(a1, k("-Y1-w12"))
    y14 = m.add(m.xor(m.prol(y6, 7), k("C2.b1")), k("-C2.c1"))
    m.at("z")
    z = m.prol(y14, 8)
    m.at("rule A")
    flags_a, taken_a = rule_a_flags(m, c, z, c["V"])
    m.at("entry count")
    below = m.compare_and_branch(m.advance(entered), k("stage-2 budget"))
    m.at("E1, A and B")
    a1 = m.xor(m.load(rt), k("Y12"))
    y6 = m.add(a1, k("-Y1-w12"))
    d1 = m.load(d1)
    c1 = m.add(d1, k("Y11"))
    b1 = m.pror(m.xor(c1, y6), 12)
    a2 = m.add(m.add(k("w5"), a1), b1)
    c2 = m.add(c1, m.pror(m.xor(a2, d1), 8))
    c1b = m.add(d1, k("Y11'"))
    b1b = m.pror(m.xor(c1b, y6), 12)
    a2b = m.add(m.add(k("w5+delta"), a1), b1b)
    c2b = m.add(c1b, m.pror(m.xor(a2b, d1), 8))
    m.at("E1 test")
    eps = m.xor(c2, c2b)
    x = m.xor(k("beta"), eps)
    rot = m.bor(m.band(m.shr(x, 31), k("A31")), m.shl(x, 1))
    word = m.band(m.xor(m.xor(rot, eps), k("eta")), k("M"))
    flags, taken = lane_flags(m, c, word)
    m.finish(CTR_RESIDENT)
    return lanes(word.z), flags, taken, flags_a, taken_a, more, below
def ctr_lane(o, c1):
    'One counter trial against the 2-round compressions of its two last chunks (counter t, flags 3): its checks, h1, n.'
    r = ctr_trial(o, c1)
    if r is None:
        return False, 0, -1
    a, b, t, v = r
    (wa, da, ya), (wb, db, yb) = compress2(a[:LEN_A], t, CTR_FLAGS), compress2(b[:LEN_B], t, CTR_FLAGS)
    e = []
    for w, y in ((wa, ya), (wb, yb)):
        c = (y[11] + ror(y[12] ^ ((y[1] + y[6] + w[12]) & MASK), 16)) & MASK
        e.append((c, ror(y[6] ^ c, 12), g(y[1], y[6], y[11], y[12], w[12], w[5])[2], (y[3] + y[4] + w[15]) & MASK))
    h1, eps = ror(ya[14] ^ e[0][3], 16), e[0][2] ^ e[1][2]
    good = (all(ya[i] == v["Y%d" % i] for i in (0, 1, 2, 4, 5, 6, 8, 9, 10, 12, 13, 14))
            and (ya[3], ya[11], yb[3], yb[11], yb[4], e[0][1], h1) == (Y3, Y11, Y3B, Y11B, v["Y4"], v["E1.b1"], v["E3.h1"])
            and wa == list(struct.unpack("<16I", a)) and wb == list(struct.unpack("<16I", b)) and t >> 32 == 0
            and all(da[i] == db[i] for i in (0, 2, 5, 7)) and e[0][3] & CLASS_MASK == CLASS_VALUE
            and e[0][0] == c1 and c1 & CTR_MASK == CTR_VALUE and e[0][1] ^ e[1][1] == CTR_BETA
            and ror(e[0][3] ^ e[1][3], 16) == ETA)
    return good, int(rule_a(h1)), ETA ^ eps ^ rol(CTR_BETA ^ eps, 1)
def ctr_selftest(cases, seed):
    'The counter batch and its trials on cases from the seed text; every lane against ctr_lane. Returns (report, good).'
    shape, same, right, passing, ends, registers, largest = None, True, 0, 0, 0, 0, 0
    for case in range(cases):
        text = "halfsearch counter selftest %s %d" % (seed, case)
        s = struct.unpack("<10I", hashlib.shake_256(text.encode("utf-8")).digest(40))
        eight, j, entered = list(s[:8]), s[8] % CTR_WORDS, s[9]
        if case % 4 == 0:
            j = CTR_WORDS - 1
        if case % 4 == 1:
            entered = STAGE_2_BUDGET - 1
        if case % 5 == 4:
            eight[:7] = [(0, MASK, x, x)[s[9] >> 2 * i & 3] for i, x in enumerate(eight[:7])]
        o, m = ctr_outer(eight), Machine()
        words, flags, taken, flags_a, taken_a, more, below = ctr_batch(m, ctr_memory(o), j, entered)
        refs = [ctr_lane(o, c1) for c1 in ctr_table_word(j)[2]]
        right += sum(int(r[0] and flags_a[i] == 1 - r[1] and words[i] == r[2] and flags[i] == int(r[2] != 0))
                     for i, r in enumerate(refs))
        passing += sum(r[1] for r in refs)
        ends += int(taken_a == any(r[1] for r in refs) and taken == any(r[2] == 0 for r in refs)
                    and more == (j != CTR_WORDS - 1) and below == (entered != STAGE_2_BUDGET - 1))
        found = tuple((part, m.ops[part], m.loads[part], m.stores[part]) for part in m.ops)
        shape = shape or found
        same = same and found == shape
        registers, largest = max(registers, m.registers()), max([largest] + list(m.sums.values()))
    stage_a, stage_2 = sum(sum(p[1:]) for p in shape[:STAGE_A_PARTS]), sum(sum(p[1:]) for p in shape[STAGE_A_PARTS:])
    report = {"cases": cases, "lanes_checked": cases * LANES, "lanes_right": right, "lanes_passing_rule_a": passing,
              "end_tests_right": ends, "parts": {p[0]: list(p[1:]) for p in shape}, "same_counts_in_every_case": same,
              "counts_equal_table": shape == CTR_TABLE, "stage_a_units": stage_a, "stage_2_units": stage_2,
              "units_per_trial_at_budget": round((stage_a + stage_2 / (1 << STAGE_2_LOG2_SHARE)) / LANES, 4),
              "registers": registers, "largest_lane_bits": largest.bit_length(), "flags": CTR_FLAGS,
              "cube": ["%08x" % CTR_MASK, "%08x" % CTR_VALUE, CTR_MEMBERS], "beta": "%08x" % CTR_BETA,
              "table_words": CTR_WORDS, "run_outer_steps": RUN_OUTER_STEPS, "stage_2_budget": STAGE_2_BUDGET}
    report["filter"], filter_good = ctr_filter_selftest(seed)
    good = (right == cases * LANES and ends == cases and same and shape == CTR_TABLE and registers <= REGISTERS
            and largest <= LANE and filter_good)
    return report, good
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
    "The filter's two automata, built once per run on first use: (1) on Q for the seven G, (2) on E with E' = E + DY3."
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
        s = t[s + b if p else b]
        if type(x) is Word:
            Word.m.load(s)
            s = Word(s)
    return s
def ctr_filter(q, y4, w8):
    'The filter of one outer step: the outcomes (bits 0-6) with (1) solvable for Q = Y9 and (2) for E = Y3 + Y4 + w8.'
    fq, fe = ctr_tables()
    return ctr_look(fq, q) & ctr_look(fe, (Y3 + y4 + w8) & MASK)
def ctr_run(eights, cube, budget=CTR_PASS_BUDGET):
    """The walk of the run over outer steps (eight words each): ctr_outer, then the filter. A failing step skips its cube
    enumeration; a passing step is counted against the pass budget (the run halts, failed, when more than budget steps
    pass), then cube(o) runs its CTR_WORDS batches (ctr_batch). Returns (steps walked, steps passing, halted)."""
    walked = passed = 0
    for eight in eights:
        o, walked = ctr_outer(eight), walked + 1
        if ctr_filter(o["Y9"], o["Y4"], o["w8"]):
            passed += 1
            if passed > budget:
                return walked, passed, True
            cube(o)
    return walked, passed, False
class Word(int):
    'A scalar word whose operations are counted on the machine Word.m: one operation each, one load per constant operand.'
    m = None
    def c(s, o, z, load=True):
        if load and type(o) is not Word:
            Word.m.load(o)
        Word.m.op(z)
        return Word(z)
    __add__ = __radd__ = lambda s, o: s.c(o, int(s) + int(o))
    __sub__ = lambda s, o: s.c(o, int(s) - int(o))
    __rsub__ = lambda s, o: s.c(o, int(o) - int(s))
    __xor__ = __rxor__ = lambda s, o: s.c(o, int(s) ^ int(o))
    __or__ = __ror__ = lambda s, o: s.c(o, int(s) | int(o))
    __and__ = __rand__ = lambda s, o: s.c(o, int(s) & int(o))
    __mod__ = lambda s, o: s.c(o, int(s) % o)
    __rshift__ = lambda s, o: s.c(o, int(s) >> o, False)
    __lshift__ = lambda s, o: s.c(o, int(s) << o, False)
def ctr_count(eight, passed):
    """One walked outer step of ctr_run counted on a machine with scalar words. Parts: member (Y4 from its number, also
    inside the outer step), outer step (ctr_outer as written), filter (E, eight table loads, the AND, the branch),
    pass count (passing steps only: the count against the budget). Returns (machine, words, pattern, run goes on)."""
    m = Word.m = Machine()
    m.at("member")
    class_member(Word(eight[7]) % CLASS_SIZE)
    m.at("outer step")
    o = ctr_outer([Word(x) for x in eight])
    m.at("filter")
    z = ctr_filter(o["Y9"], o["Y4"], o["w8"])
    m.compare_and_branch(m.value(z), m.load(0))
    m.at("pass count")
    return m, o, int(z), m.compare_and_branch(m.advance(passed), m.load(CTR_PASS_BUDGET + 1))
def ctr_filter_selftest(seed):
    """The filter: its tables against brute force over all v at width 10 (the real constants, and random ones with three
    planted solutions), the exact share from its own tables, 2^16 real outer steps through ctr_run (share, skip, halt),
    and the counted step against the plain one. Returns (report, good)."""
    fq, fe = ctr_tables()
    g, right = [ctr_g(t) for t in CTR_TAUS], 0
    small = [(dy, t, ctr_automaton(t, dy, 10)) for dy, t in ((0, [(ETA, y) for y in g]),
                                                             ((Y3B - Y3) & MASK, [(ror(y, 12), CTR_EPS) for y in g]))]
    for case in range(64):
        r = iter(struct.unpack("<40I", hashlib.shake_256(("halfsearch filter %s %d" % (seed, case)).encode()).digest(160)))
        for kind, (dy, targets, tables) in enumerate(small):
            x = next(r) & 1023
            if case % 2:
                dy, dz = next(r) * kind, next(r)
                targets = [(next(r) if kind else dz, next(r)) for _ in range(7)]
            sol = lambda dz, v: ((x + v) ^ (x + dy + (v ^ dz))) & 1023
            if case % 2:
                targets[:3] = [(dz, sol(dz, next(r))) for dz, _ in targets[:3]]
                tables = ctr_automaton(targets, dy, 10)
            want = sum(1 << i for i, (dz, out) in enumerate(targets) if out & 1023 in {sol(dz, v) for v in range(1024)})
            right += ctr_look(tables, x) == want
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
    steps, taken, entered, again = 1 << 16, [], [], []
    eights = [struct.unpack("<8I", hashlib.shake_256(("halfsearch filter steps %s %d" % (seed, i)).encode()).digest(32))
              for i in range(steps)]
    walked, passed, halted = ctr_run((taken.append(e) or e for e in eights), lambda o: entered.append(len(taken)))
    halt = passed > 2 and ctr_run(eights, again.append, 2) == (entered[2], 3, True) and len(again) == 2
    counted, shape = 0, None
    for i in [0, 1, 2, 3] + [e - 1 for e in entered[:4]]:
        m, o, z, more = ctr_count(eights[i], 0)
        plain = ctr_outer(eights[i])
        counted += all(o[k] == plain[k] for k in plain) and z == ctr_filter(plain["Y9"], plain["Y4"], plain["w8"]) and more
        found = {p: [m.ops[p], m.loads[p], m.stores[p]] for p in m.ops}
        shape, counted = shape or found, counted - (found != (shape or found))
    stop = not ctr_count(eights[0], CTR_PASS_BUDGET)[3]
    p, exact = max(passed, 1) / steps, CTR_SHARE / 2 ** 64
    units = {k: sum(v) for k, v in shape.items()}
    stage_a, stage_2 = (sum(sum(r[1:]) for r in rows) for rows in (CTR_TABLE[:STAGE_A_PARTS], CTR_TABLE[STAGE_A_PARTS:]))
    per_pass = units["pass count"] + CTR_WORDS * (stage_a + stage_2 / (1 << STAGE_2_LOG2_SHARE))
    report = {"tau": ["%08x" % t for t in CTR_TAUS], "eps": "%08x" % CTR_EPS, "mass": sum(CTR_MASS) << 16,
              "eps_n_0": ETA ^ CTR_EPS ^ rol(CTR_BETA ^ CTR_EPS, 1) == 0,
              "states_per_byte": [[len(t) >> 8 for t in fq], [len(t) >> 8 for t in fe]],
              "exact_pass_words": share, "exact_share_log2": round(math.log2(share) - 64, 4), "share_as_set": share == CTR_SHARE,
              "brute_force": {"width": 10, "verdicts": 128, "right": right},
              "real_outer_steps": steps, "passing": passed, "share": round(p, 6), "share_log2": round(math.log2(p), 3),
              "standard_error": round((p * (1 - p) / steps) ** 0.5, 6),
              "z_against_exact": round((p - exact) / (exact * (1 - exact) / steps) ** 0.5, 2),
              "cube_enumerations": len(entered), "skipped": walked - len(entered), "halt_right": halt and stop,
              "counted_steps_right": counted, "parts": shape, "units_per_passing_step": round(per_pass),
              "units_per_walked_step": round(units["outer step"] + units["filter"] + exact * per_pass, 1),
              "units_per_walked_step_at_budget": round(units["outer step"] + units["filter"]
                                                       + CTR_PASS_BUDGET / RUN_OUTER_STEPS * per_pass, 1),
              "pass_budget": CTR_PASS_BUDGET, "pass_margin": "17/16", "expected_passing": RUN_OUTER_STEPS * share >> 64}
    good = (right == 128 and share == CTR_SHARE and ((sum(CTR_MASS) << 27) * 5) // 7 == CTR_FACTOR and report["eps_n_0"]
            and abs(report["z_against_exact"]) < 5 and walked == steps and not halted and len(entered) == passed
            and halt and stop and counted == 8)
    return report, good
def selftest(cases, seed):
    'Run the four counted pieces on contexts derived from the seed text, print one JSON line, return the exit status.'
    shape, uses, same, last, extreme = None, None, True, 0, 0
    sums, registers = {name: {} for name in TABLES}, {name: 0 for name in TABLES}
    total = {"lanes_right": 0, "lanes_passing_rule_a": 0, "stage_2_entered": 0, "zero_test_words": 0, "stored_right": 0}
    for case in range(cases):
        text = "halfsearch selftest %s %d" % (seed, case)
        stream = struct.unpack("<9I", hashlib.shake_256(text.encode("utf-8")).digest(36))
        seven, j = list(stream[:7]), stream[7] % BATCHES
        if case % 4 == 0:
            j, last = BATCHES - 1, last + 1
        if case % 5 == 4:
            seven = [(0, MASK, v, v)[stream[8] >> 2 * i & 3] for i, v in enumerate(seven)]
            extreme += 1
        checked, machines = batch_check(seven, j)
        for key in total:
            total[key] += checked[key]
        found = {name: tuple((part, m.ops[part], m.loads[part], m.stores[part]) for part in m.ops)
                 for name, m in machines.items()}
        shape, uses = shape or found, uses or dict(machines["batch"].uses)
        same = same and found == shape and machines["batch"].uses == uses
        for name, m in machines.items():
            registers[name] = max(registers[name], m.registers())
            for part, top in m.sums.items():
                sums[name][part] = max(sums[name].get(part, 0), top)
    pieces, below = {}, True
    for name, rows in TABLES.items():
        bounds, parts = {row[0]: row[4] for row in rows}, {}
        for part, operations, loads, stores in shape[name]:
            parts[part] = {"operations": operations, "loads": loads, "stores": stores}
            if bounds.get(part) is not None:
                parts[part].update(largest_sum=(sums[name][part] * 1000 >> 32) / 1000, bound=bounds[part])
                below = below and sums[name][part] < bounds[part] << 32
        largest = max(sums[name].values())
        pieces[name] = {"operations": sum(row[1] for row in shape[name]), "loads": sum(row[2] for row in shape[name]),
                        "stores": sum(row[3] for row in shape[name]), "registers": registers[name],
                        "largest_lane": largest, "largest_lane_bits": largest.bit_length(), "parts": parts}
    batch = pieces.pop("batch")
    for name, part in batch["parts"].items():
        del part["stores"]
        part["uses"] = uses[name]
    members = {y for j in range(BATCHES) for y in list_words(j)[1]}
    flags = flags_right()
    patterns, patterns_right, patterns_satisfied = rule_a_right()
    stage_a, stage_2 = shape["batch"][:STAGE_A_PARTS], shape["batch"][STAGE_A_PARTS:]
    by_outer, by_middle = stored(context([0] * 7))
    counter, counter_good = ctr_selftest(cases, seed)
    report = {
        "selftest": "outer step, table build, middle step and two-stage packed batch of proof.md Section 6.5; counter batch",
        "seed": seed, "cases": cases, "last_batches": last, "extreme_cases": extreme,
        "message_bytes": [LEN_A, LEN_B], "rule_conditions": len(RULE_A), "stage_2_log2_share": STAGE_2_LOG2_SHARE,
        "lanes_checked": cases * LANES, "lanes_right": total["lanes_right"], "cases_stored_right": total["stored_right"],
        "lanes_passing_rule_a": total["lanes_passing_rule_a"], "batches_entering_stage_2": total["stage_2_entered"],
        "zero_test_words": total["zero_test_words"],
        "parts": batch["parts"],
        "stage_a": {"operations": sum(row[1] for row in stage_a), "loads": sum(row[2] for row in stage_a),
                    "uses": sum(uses[row[0]] for row in stage_a)},
        "stage_2": {"operations": sum(row[1] for row in stage_2), "loads": sum(row[2] for row in stage_2),
                    "uses": sum(uses[row[0]] for row in stage_2)},
        "words_kept_in_registers": len(RESIDENT), "words_loaded_again_by_stage_2": len(EVICT),
        "outer_step": pieces["outer step"], "table_build": pieces["table build"], "middle_step": pieces["middle step"],
        "same_counts_in_every_case": same,
        "counts_equal_table": shape == {name: tuple(row[:4] for row in rows) for name, rows in TABLES.items()},
        "largest_lane": batch["largest_lane"], "largest_lane_bits": batch["largest_lane_bits"], "lane_bits": LANE_BITS,
        "sums_below_bounds": below,
        "registers": batch["registers"], "register_limit": REGISTERS,
        "words_stored_per_outer_step": len(by_outer), "words_stored_per_x2": len(by_middle), "table_lists": 5,
        "list_words": BATCHES, "members_in_list": len(members),
        "zero_lane_patterns": 1 << LANES, "zero_lane_patterns_right": flags,
        "rule_a_patterns": patterns, "rule_a_patterns_right": patterns_right, "rule_a_patterns_satisfied": patterns_satisfied,
        "rule_a_on_z": {"steps": [list(s[:1]) + ["%08x" % s[1]] if isinstance(s, tuple) else s for s in A_STEPS],
                        "all": "%08x" % A_ALL, "wanted": [[t, w, "%08x" % e] for t, w, e in A_FLIP],
                        "free_bits_of_e1": list(A_FREE)},
        "class": {"eta": "%08x" % ETA, "mask": "%08x" % CLASS_MASK, "value": "%08x" % CLASS_VALUE,
                  "members": CLASS_SIZE},
        "counter": counter,
    }
    json.dump(report, sys.stdout, separators=(",", ":"))
    sys.stdout.write("\n")
    good = (total["lanes_right"] == cases * LANES and total["stored_right"] == cases and same
            and report["counts_equal_table"] and below and max(registers.values()) <= REGISTERS
            and len(members) == CLASS_SIZE and flags == 1 << LANES and patterns_right == patterns and counter_good)
    return 0 if good else 1
def main():
    if len(sys.argv) > 1:
        modes = {"--selftest": selftest}
        if sys.argv[1] not in modes or len(sys.argv) not in (3, 4) or not sys.argv[2].isdecimal() or int(sys.argv[2]) < 1:
            raise SystemExit("usage: halfsearch.py --selftest N [seed]   (no arguments: organizer request on stdin)")
        raise SystemExit(modes[sys.argv[1]](int(sys.argv[2]), sys.argv[3] if len(sys.argv) == 4 else "1"))
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
