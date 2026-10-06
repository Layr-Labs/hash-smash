"""Half-collisions of 2-round BLAKE3 inside one difference class, and a small residual search.

Implements the constructions of proof.md for blake3-r2-prefix-v1. The
organizer request is read from stdin and one message pair is returned per
trial: a 60-byte message A and a 62-byte message B. Only the standard library
is used; there is no OS randomness, wall time or ambient state. No BLAKE3
library is imported. The pairs the program returns are built with the
quarter-round G alone, and the organizer runner recomputes both complete
digests. The file contains its own 2-round compression (compress2, written
out from proof.md Section 1). It is called only to check the counted batch,
in the experiment "residual-search" and in the self-test, on the batch's own
messages, and never for a returned pair. SHAKE-256 from the standard library
is used only to expand the organizer's seed into the trial's parameters.

Both experiments use the trial of proof.md Section 6.1: a context (step S1 of
Section 4 for nine state words), a value alpha of the D0 family and one member
of the class of Lemma Q, that is one of the CLASS_SIZE values of Y4 for which
the first-half d difference of round-1 call E3 is the word ETA below.

Experiment "half-collision": one trial per seed. The proof predicts that
digest words 0, 2, 5, 7 of A and B are equal for every seed.

Experiment "residual-search": the search of proof.md Section 6 at toy scale.
For one context and one alpha taken from the seed it tries the class members
k0, k0+1, ... (all members of the class at most) and returns the first pair whose
residual has a zero low byte in digest word 1, so that 136 digest bits agree.
The number of members tried is reported as an untrusted observation. For the
same context and alpha one packed two-stage batch of proof.md Section 6.5,
the batch that holds member k0, is also evaluated on a machine that counts
operations and loads. Both stages are evaluated, whether or not stage A
passes. The operations and loads of each stage, whether a lane passes stage
A, and the number of lanes that are right are reported as untrusted
observations. A lane is right when its stage-A flag says whether the trial
satisfies rule A, with h1 taken from the compression of the lane's own
message A, and its stage-2 word and flag equal the test word of Lemma N,
computed from the compressions of the lane's two messages and again from
their two complete digests. That batch is not part of the search and has no
influence on the returned pair.

Self-test of the operation count (not an organizer mode):

    python3 experiments/halfsearch.py --selftest N [seed]

runs N packed batches on contexts, values of alpha and list positions derived
from the seed text (default 1). Every fourth case is the last batch of the
class, and in every fifth each context word and alpha is 0, 2^32 - 1 or as
drawn. It prints one JSON line: cases, lanes checked and lanes right (as
above, each lane against the complete digests of its two messages), the
lanes that pass rule A and the batches in which one does, operations and
loads per part and per stage, the largest lane of a sum per part and
overall, the largest number of registers in use at one time, the number of
constants per context and per alpha, the number of class members in the
list, for how many of the 128 patterns of zero and nonzero lanes the flags
are right, and for how many of 256 packed words, in which every pattern of
the eight bits of z that rule A reads occurs once in every lane, the stage-A
flags are right (a random case hardly ever has a zero stage-2 word, and one
lane in 64 passes rule A). The exit status is 0 when
every lane is right, the counts are those of the table in Section 6.5 in
every case, every sum is below the bound quoted there, the registers are at
most 16, the list holds all members of the class and all patterns are right.
"""

import hashlib
import json
import struct
import sys

MASK = 0xFFFFFFFF
IV = (0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A,
      0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19)
K = (IV[2] + IV[6]) & MASK
LEN_A, LEN_B = 60, 62
# The pinned round-1 column call C3 = G(3,7,11,15; w4, w13) of proof.md Section 3.
X3, X7, X11, X15 = 0xD5D881CA, 0xAA277E35, 0x1F208000, 0x123F2142
W4, W13 = 0x7FFFFFFF, 0xFFFD6E01
W4B = (((W4 + K) & MASK) ^ LEN_A ^ LEN_B) - K & MASK
DELTA5 = (W4 - W4B) & MASK
# The class of proof.md Section 6.1.
ETA = 0xE7C1815F
# Rule A of proof.md Section 6.3 for this class: for every pair (mask, value), the XOR of the bits of h1 in mask is value.
RULE_A = ((0x00010000, 1), (0x00000003, 0), (0x00000006, 0), (0x0000000C, 0), (0x00000018, 1), (0x01800000, 1))
FREE = (1, 2, 5, 6, 9, 10, 12, 13, 14)


def ror(v, n):
    return ((v >> n) | (v << (32 - n))) & MASK


def rol(v, n):
    return ((v << n) | (v >> (32 - n))) & MASK


def g(a, b, c, d, x, y):
    a = (a + b + x) & MASK; d = ror(d ^ a, 16); c = (c + d) & MASK; b = ror(b ^ c, 12)
    a = (a + b + y) & MASK; d = ror(d ^ a, 8); c = (c + d) & MASK; b = ror(b ^ c, 7)
    return a, b, c, d


# a and c outputs of C3 for message A (w4 = W4) and for message B (w4 = W4B)
Y3, _, Y11, _ = g(X3, X7, X11, X15, W4, W13)
Y3B, _, Y11B, _ = g(X3, X7, X11, X15, W4B, W13)


def class_pattern():
    """Lemma Q: the bits of e1 = Y3 + Y4 that eta fixes (mask, value) and the free bit positions."""
    x = rol(ETA, 16)
    v = (Y3B - Y3 + x) & MASK
    if v & 1 or (v >> 1) & ~x & MASK:
        raise ValueError("no Y4 gives this eta")
    mask = x & 0x7FFFFFFF
    return mask, ~(v >> 1) & mask, tuple(i for i in range(32) if not mask >> i & 1)


CLASS_MASK, CLASS_VALUE, CLASS_FREE = class_pattern()
CLASS_SIZE = 1 << len(CLASS_FREE)
# The packed word of proof.md Section 6.5: seven lanes of 36 bits in one 256-bit word, on a 16-register machine.
LANES, LANE_BITS, REGISTERS = 7, 36, 16
LANE = (1 << LANE_BITS) - 1
WORD = (1 << 256) - 1
ONES = sum(1 << (LANE_BITS * i) for i in range(LANES))
BATCHES = (CLASS_SIZE + LANES - 1) // LANES
# (part, operations, loads, bound) of one batch of seven trials: the table of proof.md Section 6.5 and, in units of
# 2^32, the bound that Section 6.5 gives for the sums of the part. The first STAGE_A_PARTS parts are stage A, which
# every batch runs; the others are stage 2, which a batch runs only when one of its lanes passes rule A.
TABLE = (("loop", 3, 1, None), ("C0 backwards", 9, 7, 2), ("K3", 25, 12, 6), ("C2 to z", 16, 8, 8), ("rule A", 9, 6, 2),
         ("entry count", 3, 1, None), ("C2, rest", 12, 4, 3), ("D1", 8, 5, 2), ("C1 to Y1", 17, 9, 6),
         ("E1, A and B", 40, 14, 10), ("E1 test", 13, 6, 2))
STAGE_A_PARTS = 5
# The budget of proof.md 6.4 step 4 on the batches that enter stage 2: one eighth of the batches of a run.
STAGE_2_BUDGET = BATCHES << 85


def rule_a(h1):
    """Rule A on the word h1, the first-half d value of E3 on message A."""
    return all(bin(h1 & mask).count("1") & 1 == value for mask, value in RULE_A)


def rule_a_constants():
    """Lemma A: rule A as a condition on z, the XOR of the fifth and the second value of C2, for this class.

    Bit i of h1 is bit (i + 24) mod 32 of z XOR bit (i + 16) mod 32 of e1, and every bit of e1 that the rule meets
    is fixed by the class. Returns (S, ALL, V): a trial satisfies rule A exactly when
    ((z XOR ((z >> 1) AND S)) AND ALL) == V.
    """
    shift = everything = wanted = 0
    for mask, value in RULE_A:
        bits = [i for i in range(32) if mask >> i & 1]
        for i in bits:
            if not CLASS_MASK >> ((i + 16) % 32) & 1:
                raise ValueError("rule A meets a free bit of e1")
            value ^= CLASS_VALUE >> ((i + 16) % 32) & 1
        low = sorted((i + 24) % 32 for i in bits)
        if len(low) == 2 and low[1] == low[0] + 1:
            shift |= 1 << low[0]
        elif len(low) != 1:
            raise ValueError("rule A: a condition is neither one bit nor two neighbouring bits of z")
        if everything >> low[0] & 1:
            raise ValueError("rule A: two conditions at one position")
        everything |= 1 << low[0]
        wanted |= value << low[0]
    return shift, everything, wanted


A_SHIFT, A_ALL, A_VALUE = rule_a_constants()


def class_member(k):
    """Y4 of class member number k: the bits of k fill the free positions of e1 in increasing order."""
    e1 = CLASS_VALUE
    for j, i in enumerate(CLASS_FREE):
        e1 |= (k >> j & 1) << i
    return (e1 - Y3) & MASK


def column_inverse(j, sb, sc, d0):
    """Round-0 column call j from its b and c outputs: returns (a out, d out, x, y)."""
    a0, b0, c0 = IV[j], IV[4 + j], IV[j]
    b1 = rol(sb, 7) ^ sc
    c1 = rol(b1, 12) ^ b0
    sd = (sc - c1) & MASK
    d1 = (c1 - c0) & MASK
    a1 = rol(d1, 16) ^ d0
    return rol(sd, 8) ^ d1, sd, (a1 - a0 - b0) & MASK, (rol(sd, 8) ^ d1) - a1 - b1 & MASK


def context(free):
    """Step S1: message words w, state X after round 0, state S after its column step."""
    X, S, w = [0] * 16, [0] * 16, [0] * 16
    for i, v in zip(FREE, free):
        X[i] = v
    X[3], X[7], X[11], X[15] = X3, X7, X11, X15
    w[4], w[13], w[15] = W4, W13, 0
    a1_c2 = (W4 + K) & MASK
    d1_c2 = ror(a1_c2 ^ LEN_A, 16)
    c1_c2 = (d1_c2 + IV[2]) & MASK
    b1_c2 = ror(c1_c2 ^ IV[6], 12)
    # D1 = G(1,6,11,12; w10, w11)
    b1_d1 = rol(X[6], 7) ^ X[11]
    c1_d1 = (X[11] - X[12]) & MASK
    d1_d1 = rol(X[12], 8) ^ X[1]
    S[6] = rol(b1_d1, 12) ^ c1_d1
    S[11] = (c1_d1 - d1_d1) & MASK
    S[10] = b1_c2 ^ rol(S[6], 7)
    # D0 = G(0,5,10,15; w8, w9); X0 is derived
    b1_d0 = rol(X[5], 7) ^ X[10]
    c1_d0 = (X[10] - X[15]) & MASK
    S[5] = rol(b1_d0, 12) ^ c1_d0
    d1_d0 = (c1_d0 - S[10]) & MASK
    X[0] = d1_d0 ^ rol(X[15], 8)
    # round-0 column call 2
    S[14] = (S[10] - c1_c2) & MASK
    S[2] = rol(S[14], 8) ^ d1_c2
    w[5] = (S[2] - a1_c2 - b1_c2) & MASK
    # D3 = G(3,4,9,14; w14, w15); X4 is derived
    d1_d3 = rol(X[14], 8) ^ X[3]
    a1_d3 = rol(d1_d3, 16) ^ S[14]
    b1_d3 = (X[3] - a1_d3 - w[15]) & MASK
    X[4] = ror(b1_d3 ^ X[9], 7)
    c1_d3 = (X[9] - X[14]) & MASK
    S[4] = rol(b1_d3, 12) ^ c1_d3
    S[9] = (c1_d3 - d1_d3) & MASK
    S[1], S[13], w[2], w[3] = column_inverse(1, S[5], S[9], 0)
    # D2 = G(2,7,8,13; w12, w13); X8 is derived
    d1_d2 = rol(X[13], 8) ^ X[2]
    a1_d2 = rol(d1_d2, 16) ^ S[13]
    b1_d2 = (X[2] - a1_d2 - w[13]) & MASK
    X[8] = b1_d2 ^ rol(X[7], 7)
    c1_d2 = (X[8] - X[13]) & MASK
    S[7] = rol(b1_d2, 12) ^ c1_d2
    S[8] = (c1_d2 - d1_d2) & MASK
    w[12] = (a1_d2 - S[2] - S[7]) & MASK
    S[0], S[12], w[0], w[1] = column_inverse(0, S[4], S[8], 0)
    S[3], S[15], w[6], w[7] = column_inverse(3, S[7], S[11], 11)
    a1_d0 = rol(d1_d0, 16) ^ S[15]
    w[8] = (a1_d0 - S[0] - S[5]) & MASK
    w[9] = (X[0] - a1_d0 - b1_d0) & MASK
    a1_d1 = rol(d1_d1, 16) ^ S[12]
    w[10] = (a1_d1 - S[1] - S[6]) & MASK
    w[11] = (X[1] - a1_d1 - b1_d1) & MASK
    w[14] = (a1_d3 - S[3] - S[4]) & MASK
    return X, S, w


def messages(w):
    """Steps S2 and S3."""
    other = list(w)
    other[4] = W4B
    other[5] = (w[5] + DELTA5) & MASK
    return struct.pack("<16I", *w)[:LEN_A], struct.pack("<16I", *other)[:LEN_B]


def per_alpha(X, S, w, alpha):
    """What a trial needs that depends on alpha only: the D0 family and the first half of C0."""
    c = (alpha - X15) & MASK
    d_d0 = (c - S[10]) & MASK
    x0 = rol(X15, 8) ^ d_d0
    b_d0 = ror(S[5] ^ c, 12)
    x5 = ror(b_d0 ^ alpha, 7)
    a1 = (x0 + X[4] + w[2]) & MASK
    d1 = ror(X[12] ^ a1, 16)
    c1 = (X[8] + d1) & MASK
    b1 = ror(X[4] ^ c1, 12)
    return x0, x5, d_d0, b_d0, a1, d1, c1, b1


def trial(X, S, w, alpha, y4, pre=None):
    """The trial of proof.md 6.1 for class member y4: returns (words, X1, X5, Y12).

    The words are those of the context with w6..w11 and w14 replaced. Round 0 maps them to the
    context's state with X0, X5, X10 moved by the D0 family and X1 replaced; C0 then has b output y4.
    """
    x0, x5, d_d0, b_d0, a1, d1, c1, b1 = pre or per_alpha(X, S, w, alpha)
    # C0 = G(0,4,8,12; w2, w6) backwards from its b output
    c2 = rol(y4, 7) ^ b1
    y12 = (c2 - c1) & MASK
    a2 = rol(y12, 8) ^ d1
    w6 = (a2 - a1 - b1) & MASK
    # K3 = G(3,7,11,15; w6, w7) with its b output S7 kept
    ka = (IV[3] + IV[7] + w6) & MASK
    kd = ror(11 ^ ka, 16)
    kc = (IV[3] + kd) & MASK
    kb = ror(IV[7] ^ kc, 12)
    s11 = rol(S[7], 7) ^ kb
    s15 = (s11 - kc) & MASK
    s3 = rol(s15, 8) ^ kd
    w7 = (s3 - ka - kb) & MASK
    # D1 with the new S11
    d_d1 = (X11 - X[12] - s11) & MASK
    x1 = rol(X[12], 8) ^ d_d1
    a_d1 = rol(d_d1, 16) ^ S[12]
    b_d1 = rol(X[6], 7) ^ X11
    # D0 with the new S15, D3 with the new S3
    a_d0 = rol(d_d0, 16) ^ s15
    a_d3 = rol(rol(X[14], 8) ^ X3, 16) ^ S[14]
    words = list(w)
    words[6], words[7] = w6, w7
    words[8], words[9] = (a_d0 - S[0] - S[5]) & MASK, (x0 - a_d0 - b_d0) & MASK
    words[10], words[11] = (a_d1 - S[1] - S[6]) & MASK, (x1 - a_d1 - b_d1) & MASK
    words[14] = (a_d3 - s3 - S[4]) & MASK
    return words, x1, x5, y12


def residual_word1(X, words, alpha, x1, x5, y4, y12):
    """Digest word 1 of A xor digest word 1 of B for one trial (round 1, partial; proof.md 6.2)."""
    c1 = g(x1, x5, X[9], X[13], words[3], words[10])
    c2 = g(X[2], X[6], alpha, X[14], words[7], words[0])
    y1, y9, y6, y14 = c1[0], c1[2], c2[1], c2[3]
    w5b = (words[5] + DELTA5) & MASK
    pa = g(y1, y6, Y11, y12, words[12], words[5])
    pb = g(y1, y6, Y11B, y12, words[12], w5b)
    qa = g(Y3, y4, y9, y14, words[15], words[8])
    qb = g(Y3B, y4, y9, y14, words[15], words[8])
    return pa[0] ^ qa[2] ^ pb[0] ^ qb[2]


def rep(v):
    """The 32-bit value v in every lane of a packed word."""
    return (v & MASK) * ONES


def lanes(z):
    """The seven lanes of a packed word."""
    return [(z >> (LANE_BITS * i)) & LANE for i in range(LANES)]


class Packed:
    """A 256-bit word in a register: its value, the step that made it and the step of its last use."""

    __slots__ = ("z", "born", "last")

    def __init__(self, z, born):
        self.z, self.born, self.last = z, born, born


class Machine:
    """The counting machine of proof.md Section 6.5.

    Every addition, XOR, AND, OR and shift of 256-bit words is one operation,
    a comparison and a branch are one each, and every constant operand and
    list entry is fetched with load() and is one load. Both counts are kept
    per part of the batch. sums holds, per part, the largest lane of any sum
    of packed words; it is taken lane by lane from the two operands, so a
    carry out of a lane cannot hide. Every value records the step that made
    it and the step of its last use; registers() counts from these how many
    values are held at one time.
    """

    def __init__(self):
        self.ops, self.loads, self.sums = {}, {}, {}
        self.part, self.step, self.values = None, 0, []

    def at(self, part):
        self.part = part
        self.ops[part] = self.loads[part] = self.sums[part] = 0

    def value(self, z, *used):
        self.step += 1
        for operand in used:
            operand.last = self.step
        self.values.append(Packed(z, self.step))
        return self.values[-1]

    def load(self, constant):
        self.loads[self.part] += 1
        return self.value(constant)

    def constant(self, name, value):
        return self.load(value)

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
        """Rotate every lane right by r: ((z >> r) AND A_r) OR ((z << (32-r)) AND B_r)."""
        low = self.band(self.shr(z, r), self.constant("L" + str(r), rep((1 << (32 - r)) - 1)))
        high = self.band(self.shl(z, 32 - r), self.constant("H" + str(r), rep(((1 << r) - 1) << (32 - r))))
        return self.bor(low, high)

    def prol(self, z, r):
        return self.pror(z, 32 - r)

    def advance(self, position):
        """The next value of a counter kept in a register (the list position, the stage-2 entries): one addition."""
        return self.op(position + 1)

    def compare_and_branch(self, x, y):
        """The comparison of two registers and the branch on its result: two operations. True when they differ."""
        self.ops[self.part] += 2
        self.step += 1
        x.last = y.last = self.step
        return x.z != y.z

    def registers(self):
        """The largest number of registers in use at one time, for the operations in the order they were made.

        A value occupies a register from the step that makes it up to the
        step of its last use, whose result may take its place. Two more
        registers hold, from batch to batch, the list position and the
        number of batches that have entered stage 2.
        """
        change = [0] * (self.step + 1)
        for value in self.values:
            change[value.born] += 1
            change[value.last] -= 1
        held = peak = 0
        for delta in change:
            held += delta
            peak = max(peak, held)
        return peak + 2


class ResidentMachine16(Machine):
    """Six resident masks (M, bit 32, L12, H12, L16, H16) on a 16-register machine (proof.md Section 11)."""

    def __init__(self, constants):
        super().__init__()
        names = ("M", "bit 32", "L12", "H12", "L16", "H16")
        self.resident = {name: Packed(constants[name], 0) for name in names}
        self.preload_operations = len(self.resident)

    def constant(self, name, value):
        if name in self.resident:
            result = self.resident[name]
            if result.z != value:
                raise AssertionError("resident constant mismatch")
            return result
        return self.load(value)

    def registers(self):
        return super().registers() + len(self.resident)


class ResidentMachine32(Machine):
    """Twenty-two resident constants on a 32-register machine (proof.md Section 11)."""

    def __init__(self, constants):
        super().__init__()
        names = ("M", "bit 32", "1", "L8", "H8", "L12", "H12", "L16", "H16", "L24", "H24",
                 "BATCHES", "pb", "-pc", "pd", "IV3+IV7-pa-pb", "11", "IV3", "IV7", "~ROL(S7,7)", "X2+X6", "X14")
        self.resident = {name: Packed(constants[name], 0) for name in names}
        self.preload_operations = len(self.resident)

    def constant(self, name, value):
        if name in self.resident:
            result = self.resident[name]
            if result.z != value:
                raise AssertionError("resident constant mismatch")
            return result
        return self.load(value)

    def registers(self):
        return super().registers() + len(self.resident) + 1


class FullResidentMachine64(Machine):
    """Forty-four immutable registers persist across the 9,363 batches of an alpha on a 64-register machine."""

    def __init__(self, constants):
        super().__init__()
        self.resident = {name: Packed(value, 0) for name, value in constants.items()}
        assert len(self.resident) == 44, f"expected 44 resident constants, got {len(self.resident)}"
        self.preload_operations = len(self.resident)

    def constant(self, name, value):
        result = self.resident[name]
        if result.z != value:
            raise AssertionError("resident constant mismatch")
        return result

    def registers(self):
        return super().registers() + len(self.resident) + 1


def list_words(j):
    """The packed word U[j] of proof.md Section 6.5 and the seven class members it holds.

    Lane i holds member number 7 j + i; the spare lanes of the last word repeat the last member.
    """
    members = [class_member(min(LANES * j + i, CLASS_SIZE - 1)) for i in range(LANES)]
    u = sum(rol(y, 7) << (LANE_BITS * i) for i, y in enumerate(members))
    return u, members


def batch_constants(X, S, w, alpha):
    """Every constant a batch loads, by name and in all seven lanes; and how many are per context and per alpha.

    The algorithm computes and stores them before the batches (proof.md Section 8). Nothing here is counted in a batch.
    """
    _, x5, _, _, pa, pd, pc, pb = per_alpha(X, S, w, alpha)
    fixed = {"M": MASK, "1": 1, "11": 11, "IV3": IV[3], "IV7": IV[7], "Y11": Y11, "Y11'": Y11B, "eta": ETA,
             "A shift": A_SHIFT, "A all": A_ALL, "A value": A_VALUE}
    for r in (7, 8, 12, 16, 24):
        fixed["L" + str(r)] = (1 << (32 - r)) - 1
        fixed["H" + str(r)] = ((1 << r) - 1) << (32 - r)
    per_context = {"~ROL(S7,7)": (~rol(S[7], 7)) & MASK, "X2+X6": (X[2] + X[6]) & MASK,
                   "X11-X12+1": (X11 - X[12] + 1) & MASK, "ROL(X12,8)": rol(X[12], 8), "S12": S[12],
                   "X13": X[13], "X9": X[9], "w12-S1-S6": (w[12] - S[1] - S[6]) & MASK,
                   "X14": X[14], "X6": X[6], "w0": w[0], "w5": w[5], "w5+delta": (w[5] + DELTA5) & MASK}
    for_alpha = {"pb": pb, "-pc": (-pc) & MASK, "pd": pd, "IV3+IV7-pa-pb": (IV[3] + IV[7] - pa - pb) & MASK,
                 "X5": x5, "X5+w3": (x5 + w[3]) & MASK, "alpha": alpha}
    c = {name: rep(value) for group in (fixed, per_context, for_alpha) for name, value in group.items()}
    c["bit 32"] = ONES << 32
    c["BATCHES"] = BATCHES
    c["STAGE_2_BUDGET"] = STAGE_2_BUDGET
    return c, len(per_context), len(for_alpha)


def lane_flags(m, c, word):
    """The end of a stage: bit 32 of every lane of word + M, set where the reduced word is nonzero, and the branch.

    Returns the seven flags and whether the branch is taken, that is whether some lane has a zero word.
    """
    flags = m.band(m.add(word, m.constant("M", c["M"])), m.constant("bit 32", c["bit 32"]))
    taken = m.compare_and_branch(flags, m.constant("bit 32", c["bit 32"]))
    return [(flags.z >> (LANE_BITS * i + 32)) & 1 for i in range(LANES)], taken


def rule_a_word(m, c, z):
    """The stage-A word of Lemma A for seven lanes z: zero exactly in the lanes whose trial satisfies rule A."""
    y = m.xor(z, m.band(m.shr(z, 1), m.constant("A shift", c["A shift"])))
    return m.xor(m.band(y, m.constant("A all", c["A all"])), m.constant("A value", c["A value"]))


def packed_batch(m, c, j, entered=0):
    """The two-stage batch of proof.md Sections 6.5 and 11 for the seven trials of batch j, counted on the machine m.

    c holds the constants of batch_constants. Every line below is made of calls of m only, so every operation
    and every load is counted. The names are those of proof.md 6.1 to 6.5 and 11; the parts and their order are those
    of TABLE. The algorithm runs the parts of stage 2 only when the branch of stage A is taken; this function always
    evaluates them, so that their count and their lanes can be checked for every batch. entered is the number of
    batches that have entered stage 2 before this one; stage 2 begins by counting its own entry and comparing the
    count with STAGE_2_BUDGET (step 4 of proof.md 6.4). Returns the seven reduced
    stage-2 test words, their seven flags (1 where the word is nonzero), whether the final branch is taken, the
    seven stage-A flags (1 where the trial fails rule A) and whether the stage-A branch is taken.
    """
    def k(name):
        return m.constant(name, c[name])

    u, _ = list_words(j)
    m.at("loop")                                                      # next list position, end test, branch
    m.compare_and_branch(m.advance(j), k("BATCHES"))
    m.at("C0 backwards")
    y8 = m.xor(m.load(u), k("pb"))
    y12 = m.add(y8, k("-pc"))
    y0 = m.xor(m.prol(y12, 8), k("pd"))
    ka = m.add(y0, k("IV3+IV7-pa-pb"))                                # IV[3] + IV[7] + w6
    m.at("K3")
    kd = m.pror(m.xor(ka, k("11")), 16)
    kc = m.add(kd, k("IV3"))
    kb = m.pror(m.xor(kc, k("IV7")), 12)
    kab = m.add(ka, kb)
    ns11 = m.xor(kb, k("~ROL(S7,7)"))                                 # ~S11 = kb XOR ~ROL(S7,7)
    ns15 = m.add(ns11, kc)                                            # ~S15 = ~S11 + kc
    ns3 = m.xor(m.prol(ns15, 8), kd)                                  # ~S3 = ROL(~S15,8) XOR kd
    first = m.add(m.xor(m.add(ns3, kab), k("M")), k("X2+X6"))         # v = X2 + X6 + w7, w7 = (~(ns3 + ka + kb)) + 1
    m.at("C2 to z")
    rd = m.pror(m.xor(first, k("X14")), 16)
    rc = m.add(rd, k("alpha"))
    rb = m.pror(m.xor(rc, k("X6")), 12)
    ra = m.add(m.add(first, rb), k("w0"))
    z = m.xor(ra, rd)                                                 # Y14 = ROR(z, 8)
    m.at("rule A")
    flags_a, taken_a = lane_flags(m, c, rule_a_word(m, c, z))
    # ---- stage 2
    m.at("entry count")                                               # one more entry, budget test, branch
    m.compare_and_branch(m.advance(entered), k("STAGE_2_BUDGET"))
    m.at("C2, rest")
    y14 = m.pror(z, 8)
    y6 = m.pror(m.xor(m.add(rc, y14), rb), 7)
    m.at("D1")
    d = m.add(ns11, k("X11-X12+1"))                                   # (X11 - X12) - S11 = ~S11 + X11 - X12 + 1
    a = m.xor(m.prol(d, 16), k("S12"))
    x1 = m.xor(d, k("ROL(X12,8)"))
    m.at("C1 to Y1")
    qa = m.add(x1, k("X5+w3"))
    qd = m.pror(m.xor(qa, k("X13")), 16)
    y1_part = m.add(m.add(qa, a), k("w12-S1-S6"))
    qc = m.add(qd, k("X9"))
    qb = m.pror(m.xor(qc, k("X5")), 12)
    y1w12 = m.add(y1_part, qb)                                        # Y1 + w12, with w10 = a - S1 - S6
    m.at("E1, A and B")
    a1 = m.add(y1w12, y6)
    d1 = m.pror(m.xor(a1, y12), 16)
    c1 = m.add(d1, k("Y11"))
    b1 = m.pror(m.xor(c1, y6), 12)
    a2_d1 = m.xor(m.add(m.add(a1, b1), k("w5")), d1)
    c2 = m.add(c1, m.pror(a2_d1, 8))
    c1b = m.add(d1, k("Y11'"))
    b1b = m.pror(m.xor(c1b, y6), 12)
    a2b_d1 = m.xor(m.add(m.add(a1, b1b), k("w5+delta")), d1)
    beta = m.xor(b1, b1b)
    c2b = m.add(c1b, m.pror(a2b_d1, 8))
    m.at("E1 test")
    eps = m.xor(c2, c2b)
    x = m.xor(beta, eps)                                              # beta XOR eps (< 2^34 in every lane)
    prol1_x = m.bor(m.band(m.shr(x, 31), k("1")), m.shl(x, 1))
    word = m.band(m.xor(m.xor(prol1_x, eps), k("eta")), k("M"))       # the reduced test word of Lemma N
    flags, taken = lane_flags(m, c, word)
    return lanes(word.z), flags, taken, flags_a, taken_a


PERMUTATION = (2, 6, 3, 10, 7, 0, 4, 13, 1, 11, 12, 5, 9, 14, 15, 8)
G_CALLS = ((0, 4, 8, 12), (1, 5, 9, 13), (2, 6, 10, 14), (3, 7, 11, 15),
           (0, 5, 10, 15), (1, 6, 11, 12), (2, 7, 8, 13), (3, 4, 9, 14))


def compress2(message):
    """The complete 2-round compression of proof.md Section 1 for one message of at most 64 bytes.

    Returns its sixteen words, its eight digest words and the state Y after the four column calls of round 1.
    Used only to check the counted batch; no returned pair depends on it.
    """
    n = len(message)
    w = list(struct.unpack("<16I", message + bytes(64 - n)))
    v = list(IV) + list(IV[:4]) + [0, 0, n, 11]
    s, y = list(w), None
    for r in range(2):
        for i, (a, b, c, d) in enumerate(G_CALLS):
            if r == 1 and i == 4:
                y = list(v)
            v[a], v[b], v[c], v[d] = g(v[a], v[b], v[c], v[d], s[2 * i], s[2 * i + 1])
        s = [s[p] for p in PERMUTATION]
    return w, [v[i] ^ v[i + 8] for i in range(8)], y


def reference(X, S, w, alpha, y4):
    """What the batch must show for one trial, taken from the compressions of the trial's two real messages.

    The messages A and B of the trial are built by steps S2 and S3 and each is compressed in full by compress2.
    Returned: Y4 of A; h1, the second value of E3 on A, from the state Y of A; the test word of Lemma N from E1
    evaluated for A and for B with g on their own states and words; the same word from the two complete digests,
    digest word 3 XOR ROL(digest word 6, 8) of the XOR of the digests; and whether the digests agree on digest
    words 0, 2, 5, 7 with the same Y4 in A and B.
    """
    first, second = messages(trial(X, S, w, alpha, y4)[0])
    (wa, da, ya), (wb, db, yb) = compress2(first), compress2(second)
    r = [p ^ q for p, q in zip(da, db)]
    h1 = ror(ya[14] ^ ((ya[3] + ya[4] + wa[15]) & MASK), 16)
    outs = []
    for words, y in ((wa, ya), (wb, yb)):
        a1 = (y[1] + y[6] + words[12]) & MASK
        b1 = ror(y[6] ^ ((y[11] + ror(y[12] ^ a1, 16)) & MASK), 12)
        outs.append((b1, g(y[1], y[6], y[11], y[12], words[12], words[5])[2]))
    beta, eps = outs[0][0] ^ outs[1][0], outs[0][1] ^ outs[1][1]
    return {"y4": ya[4], "h1": h1, "word": ETA ^ eps ^ rol(beta ^ eps, 1), "word_from_digests": r[3] ^ rol(r[6], 8),
            "half": int(r[0] == 0 and r[2] == 0 and r[5] == 0 and r[7] == 0 and ya[4] == yb[4])}


def batch_check(X, S, w, alpha, j, machine=None):
    """Batch j of the class for a context and an alpha, on a new machine unless one is given.

    Returns a dict: operations and loads of stage A and of stage 2, the number of lanes that are right, the number
    of lanes that pass rule A, whether the batch enters stage 2, and the number of zero stage-2 test words. A lane
    is right when all of this holds for its trial and the reference of its two real messages: Y4 of message A is
    the member of the lane; the digests agree on digest words 0, 2, 5, 7; the stage-A flag is 0 exactly when h1
    satisfies rule A; the reduced stage-2 word equals the word of Lemma N, which in turn equals the word from the
    two complete digests; and the stage-2 flag tells whether that word is nonzero. No lane counts as right when
    one of the two branches is not taken exactly if one of the seven words in front of it is zero.
    """
    m = machine or Machine()
    constants = batch_constants(X, S, w, alpha)[0]
    words, flags, taken, flags_a, taken_a = packed_batch(m, constants, j)
    m64 = FullResidentMachine64(constants)
    m32 = ResidentMachine32(constants)
    m16 = ResidentMachine16(constants)
    out64 = packed_batch(m64, constants, j)
    out32 = packed_batch(m32, constants, j)
    out16 = packed_batch(m16, constants, j)
    members = list_words(j)[1]
    refs = [reference(X, S, w, alpha, y4) for y4 in members]
    passing = [int(rule_a(r["h1"])) for r in refs]
    right = sum(int(r["y4"] == members[i] and r["half"] == 1 and flags_a[i] == 1 - passing[i] and words[i] == r["word"]
                    and r["word"] == r["word_from_digests"] and flags[i] == int(r["word"] != 0))
                for i, r in enumerate(refs))
    zero = sum(int(r["word"] == 0) for r in refs)
    if taken_a != (1 in passing) or taken != (zero > 0) or out64 != (words, flags, taken, flags_a, taken_a) or out32 != out64 or out16 != out64:
        right = 0
    parts = list(m.ops)
    stage_a, stage_2 = parts[:STAGE_A_PARTS], parts[STAGE_A_PARTS:]
    return {"stage_a_operations": sum(m.ops[p] for p in stage_a), "stage_a_loads": sum(m.loads[p] for p in stage_a),
            "stage_2_operations": sum(m.ops[p] for p in stage_2), "stage_2_loads": sum(m.loads[p] for p in stage_2),
            "full_resident64_stage_a_loads": sum(m64.loads[p] for p in stage_a),
            "full_resident64_stage_2_loads": sum(m64.loads[p] for p in stage_2),
            "full_resident64_registers": m64.registers(),
            "resident32_stage_a_loads": sum(m32.loads[p] for p in stage_a),
            "resident32_stage_2_loads": sum(m32.loads[p] for p in stage_2),
            "resident32_registers": m32.registers(),
            "resident16_stage_a_loads": sum(m16.loads[p] for p in stage_a),
            "resident16_stage_2_loads": sum(m16.loads[p] for p in stage_2),
            "resident16_registers": m16.registers(),
            "lanes_right": right, "lanes_passing_rule_a": sum(passing), "stage_2_entered": int(taken_a),
            "zero_test_words": zero}


def seeded(seed):
    """Nine state words, alpha and a class member number from the organizer seed."""
    stream = struct.unpack("<11I", hashlib.shake_256(seed).digest(44))
    return context(stream[:9]), stream[9], stream[10] % CLASS_SIZE


def half_collision(seed):
    (X, S, w), alpha, k = seeded(seed)
    words, _, _, _ = trial(X, S, w, alpha, class_member(k))
    return messages(words) + ({},)


def residual_search(seed):
    (X, S, w), alpha, k0 = seeded(seed)
    checked = batch_check(X, S, w, alpha, k0 // LANES)
    counted = {"batch_" + key: checked[key] for key in ("stage_a_operations", "stage_a_loads", "stage_2_operations",
                                                        "stage_2_loads", "full_resident64_stage_a_loads",
                                                        "full_resident64_stage_2_loads", "full_resident64_registers",
                                                        "resident32_stage_a_loads", "resident32_stage_2_loads",
                                                        "resident32_registers", "resident16_stage_a_loads",
                                                        "resident16_stage_2_loads", "resident16_registers",
                                                        "lanes_right", "stage_2_entered")}
    pre = per_alpha(X, S, w, alpha)
    for step in range(CLASS_SIZE):
        y4 = class_member((k0 + step) % CLASS_SIZE)
        words, x1, x5, y12 = trial(X, S, w, alpha, y4, pre)
        if residual_word1(X, words, alpha, x1, x5, y4, y12) & 0xFF == 0:
            return messages(words) + (dict(counted, tries=step + 1),)
    return None, None, dict(counted, tries=CLASS_SIZE)


def resident_audit(seed):
    """Exact run layout of proof.md Section 6.4 (shared X2,X5,X6,X9 with X1=X10=0 so S5 is fixed across contexts).

    Four contexts per organizer seed share X2,X5,X6,X9 with X1=X10=0, X12 < 2^8 and X13 < 2^16. Both the first and
    padded final list batches are checked across all four machine tiers (Machine, ResidentMachine16, ResidentMachine32,
    FullResidentMachine64) against the full two-round reference compressions of each lane's messages, recording
    rule-A passes (H3), stage-2 entries (H3), E1-test passes (H2), and low-nibble residual hits (H1).
    """
    stream = struct.unpack("<16I", hashlib.shake_256(seed).digest(64))
    fixed = stream[:4]
    checked = rule_a_passes = stage2_entries = e1_passes = low4_hits = 0
    s5_values = set()
    peak16 = peak16_res = peak32 = peak64 = 0
    last_pair = None
    for index in range(4):
        x12 = (stream[4] >> (8 * index)) & 0xFF
        x13 = (stream[5 + (index >> 1)] >> (16 * (index & 1))) & 0xFFFF
        x14 = stream[7 + index]
        free = [0, fixed[0], fixed[1], fixed[2], fixed[3], 0, x12, x13, x14]
        X, S, w = context(free)
        s5_values.add(S[5])
        alpha = stream[11 + index]
        pre = per_alpha(X, S, w, alpha)
        constants = batch_constants(X, S, w, alpha)[0]
        for j in (0, BATCHES - 1):
            m0 = Machine()
            m16 = ResidentMachine16(constants)
            m32 = ResidentMachine32(constants)
            m64 = FullResidentMachine64(constants)
            out0 = packed_batch(m0, constants, j)
            out16 = packed_batch(m16, constants, j)
            out32 = packed_batch(m32, constants, j)
            out64 = packed_batch(m64, constants, j)
            if out0 != out16 or out0 != out32 or out0 != out64:
                raise AssertionError("resident/reference schedule mismatch")
            words, flags, taken, flags_a, taken_a = out64
            members = list_words(j)[1]
            refs = [reference(X, S, w, alpha, y4) for y4 in members]
            passing = [int(rule_a(r["h1"])) for r in refs]
            for i, r in enumerate(refs):
                if not (r["y4"] == members[i] and r["half"] == 1 and flags_a[i] == 1 - passing[i]
                        and words[i] == r["word"] and r["word"] == r["word_from_digests"]
                        and flags[i] == int(r["word"] != 0)):
                    raise AssertionError("lane reference mismatch")
            if taken_a != (1 in passing) or taken != any(r["word"] == 0 for r in refs):
                raise AssertionError("branch flag mismatch")
            parts = list(m0.ops)
            sa, s2 = parts[:STAGE_A_PARTS], parts[STAGE_A_PARTS:]
            if (sum(m64.ops[p] for p in sa) != 62 or sum(m64.loads[p] for p in sa) != 1
                    or sum(m64.ops[p] for p in s2) != 93 or sum(m64.loads[p] for p in s2) != 0):
                raise AssertionError("full-resident-64 count mismatch")
            if (sum(m32.ops[p] for p in sa) != 62 or sum(m32.loads[p] for p in sa) != 7
                    or sum(m32.ops[p] for p in s2) != 93 or sum(m32.loads[p] for p in s2) != 16):
                raise AssertionError("resident-32 count mismatch")
            if (sum(m16.ops[p] for p in sa) != 62 or sum(m16.loads[p] for p in sa) != 22
                    or sum(m16.ops[p] for p in s2) != 93 or sum(m16.loads[p] for p in s2) != 23):
                raise AssertionError("resident-16 count mismatch")
            peak16 = max(peak16, m0.registers())
            peak16_res = max(peak16_res, m16.registers())
            peak32 = max(peak32, m32.registers())
            peak64 = max(peak64, m64.registers())
            if peak16 > 16 or peak16_res > 16 or peak32 > 32 or peak64 > 64:
                raise AssertionError("register budget exceeded")
            checked += LANES
            rule_a_passes += sum(passing)
            stage2_entries += int(taken_a)
            e1_passes += sum(int(r["word"] == 0) for r in refs)
            for y4 in members:
                words_t, x1_t, x5_t, y12_t = trial(X, S, w, alpha, y4, pre)
                if (residual_word1(X, words_t, alpha, x1_t, x5_t, y4, y12_t) & 0xF) == 0:
                    low4_hits += 1
        words_last, _, _, _ = trial(X, S, w, alpha, class_member((stream[15] + index) % CLASS_SIZE), pre)
        last_pair = messages(words_last)
    if len(s5_values) != 1:
        raise AssertionError("S5 must remain fixed across shared-seed contexts")
    return last_pair + ({"audited_lanes": checked, "rule_a_passes": rule_a_passes, "stage2_entries": stage2_entries,
                         "e1_test_passes": e1_passes, "residual_low4_hits": low4_hits, "s5_shared_fixed": 1,
                         "full_resident64_stage_a_ops": 62, "full_resident64_stage_a_loads": 1,
                         "full_resident64_stage_2_ops": 93, "full_resident64_stage_2_loads": 0,
                         "full_resident64_registers": peak64, "resident32_registers": peak32,
                         "resident16_registers": peak16_res, "base16_registers": peak16},)


def flags_right():
    """lane_flags on all 128 patterns of zero and nonzero lanes; random cases hardly ever have a zero lane."""
    c = {"M": rep(MASK), "bit 32": ONES << 32}
    right = 0
    for pattern in range(1 << LANES):
        words = [0 if pattern >> i & 1 else (MASK, 1, 0x80000000)[i % 3] for i in range(LANES)]
        m = Machine()
        m.at("E1 test")
        flags, taken = lane_flags(m, c, m.load(sum(v << (LANE_BITS * i) for i, v in enumerate(words))))
        right += int(flags == [int(v != 0) for v in words] and taken == (pattern != 0))
    return right


def rule_a_right():
    """The stage-A word on all patterns of the bits of z that rule A reads; one random lane in 64 passes the rule.

    One packed word per pattern: lane i holds the pattern number (p + 37 i) modulo the number of patterns, so every
    pattern occurs once in every lane and the lanes of a word differ. The bits of z outside the rule are different
    in every lane, the guard bits 32..35 of the lanes are filled, and every lane belongs to another member of the
    class. A word is right when in every lane the flag is 0 exactly if h1 = ROR(ROR(z, 8) XOR e1, 16), with
    e1 = Y3 + Y4 of the lane's member, satisfies rule A as written on h1, and the branch is taken exactly if some
    lane does. Returns (words, words right, words in which some lane satisfies the rule).
    """
    read = [i for i in range(32) if (A_ALL | A_SHIFT << 1) >> i & 1]
    c = {"M": rep(MASK), "bit 32": ONES << 32, "A shift": rep(A_SHIFT), "A all": rep(A_ALL), "A value": rep(A_VALUE)}
    right = satisfied = 0
    for pattern in range(1 << len(read)):
        zs, passing = [], []
        for lane in range(LANES):
            number = (pattern + 37 * lane) % (1 << len(read))
            base = sum((number >> n & 1) << i for n, i in enumerate(read))
            other = struct.unpack("<I", hashlib.shake_256(b"rule A %d %d" % (pattern, lane)).digest(4))[0]
            z = base | (other & ~sum(1 << i for i in read) & MASK)
            e1 = (Y3 + class_member((pattern * LANES + lane) * 37 % CLASS_SIZE)) & MASK
            zs.append(z | (other & 0xF) << 32)
            passing.append(int(rule_a(ror(ror(z, 8) ^ e1, 16))))
        m = Machine()
        m.at("rule A")
        flags, taken = lane_flags(m, c, rule_a_word(m, c, m.load(sum(v << (LANE_BITS * i) for i, v in enumerate(zs)))))
        right += int(flags == [1 - p for p in passing] and taken == (1 in passing))
        satisfied += int(1 in passing)
    return 1 << len(read), right, satisfied


def selftest(cases, seed):
    """Run packed batches on contexts derived from the seed text, print one JSON line, return the exit status."""
    shape, same, last, extreme, sums = None, True, 0, 0, {}
    total = {"lanes_right": 0, "lanes_passing_rule_a": 0, "stage_2_entered": 0, "zero_test_words": 0}
    for case in range(cases):
        text = "halfsearch selftest %s %d" % (seed, case)
        stream = struct.unpack("<12I", hashlib.shake_256(text.encode("utf-8")).digest(48))
        nine, alpha, j = list(stream[:9]), stream[9], stream[10] % BATCHES
        if case % 4 == 0:                       # the last batch of the class, whose spare lanes repeat the last member
            j, last = BATCHES - 1, last + 1
        if case % 5 == 4:                       # extreme words: each context word and alpha is 0, 2^32 - 1 or as drawn
            nine = [(0, MASK, v, v)[stream[11] >> 2 * i & 3] for i, v in enumerate(nine)]
            alpha, extreme = (0, MASK, alpha, alpha)[stream[11] >> 18 & 3], extreme + 1
        X, S, w = context(nine)
        machine = Machine()
        checked = batch_check(X, S, w, alpha, j, machine)
        for key in total:
            total[key] += checked[key]
        found = (tuple((part, machine.ops[part], machine.loads[part]) for part in machine.ops), machine.registers(),
                 batch_constants(X, S, w, alpha)[1:], checked["full_resident64_registers"],
                 checked["resident32_registers"], checked["resident16_registers"])
        shape = shape or found
        same = same and found == shape
        for part, top in machine.sums.items():
            sums[part] = max(sums.get(part, 0), top)
    table, registers, (per_context, for_alpha), reg64, reg32, reg16 = shape
    bounds = {row[0]: row[3] for row in TABLE}
    parts, below = {}, True
    for part, operations, loads in table:
        parts[part] = {"operations": operations, "loads": loads}
        if bounds.get(part) is not None:                # largest sum in units of 2^32, rounded down
            parts[part].update(largest_sum=(sums[part] * 1000 >> 32) / 1000, bound=bounds[part])
            below = below and sums[part] < bounds[part] << 32
    largest = max(sums.values())
    members = {y for j in range(BATCHES) for y in list_words(j)[1]}
    flags = flags_right()
    patterns, patterns_right, patterns_satisfied = rule_a_right()
    stage_a, stage_2 = table[:STAGE_A_PARTS], table[STAGE_A_PARTS:]
    report = {
        "selftest": "two-stage packed batch of proof.md Sections 6.5 and 11",
        "seed": seed, "cases": cases, "last_batches": last, "extreme_cases": extreme,
        "lanes_checked": cases * LANES, "lanes_right": total["lanes_right"],
        "lanes_passing_rule_a": total["lanes_passing_rule_a"], "batches_entering_stage_2": total["stage_2_entered"],
        "zero_test_words": total["zero_test_words"],
        "parts": parts,
        "stage_a": {"operations": sum(row[1] for row in stage_a), "loads": sum(row[2] for row in stage_a)},
        "stage_2": {"operations": sum(row[1] for row in stage_2), "loads": sum(row[2] for row in stage_2)},
        "full_resident64": {"stage_a_ops": 62, "stage_a_loads": 1, "stage_2_ops": 93, "stage_2_loads": 0, "registers": reg64},
        "resident32": {"stage_a_ops": 62, "stage_a_loads": 7, "stage_2_ops": 93, "stage_2_loads": 16, "registers": reg32},
        "resident16": {"stage_a_ops": 62, "stage_a_loads": 22, "stage_2_ops": 93, "stage_2_loads": 23, "registers": reg16},
        "same_counts_in_every_case": same, "counts_equal_table": table == tuple(row[:3] for row in TABLE),
        "largest_lane": largest, "largest_lane_bits": largest.bit_length(), "lane_bits": LANE_BITS,
        "sums_below_bounds": below,
        "registers": registers, "register_limit": REGISTERS,
        "per_context_constants": per_context, "per_alpha_constants": for_alpha,
        "list_words": BATCHES, "members_in_list": len(members),
        "zero_lane_patterns": 1 << LANES, "zero_lane_patterns_right": flags,
        "rule_a_patterns": patterns, "rule_a_patterns_right": patterns_right, "rule_a_patterns_satisfied": patterns_satisfied,
        "rule_a_on_z": {"shift_mask": "%08x" % A_SHIFT, "all": "%08x" % A_ALL, "value": "%08x" % A_VALUE},
    }
    json.dump(report, sys.stdout, separators=(",", ":"))
    sys.stdout.write("\n")
    good = (total["lanes_right"] == cases * LANES and same and report["counts_equal_table"] and below
            and registers <= REGISTERS and reg16 <= 16 and reg32 <= 32 and reg64 <= 64
            and len(members) == CLASS_SIZE and flags == 1 << LANES and patterns_right == patterns)
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
    run = {"half-collision": half_collision, "residual-search": residual_search, "resident-audit": resident_audit}[request["experiment_id"]]
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
