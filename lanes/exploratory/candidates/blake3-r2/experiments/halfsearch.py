"""Half-collisions of 2-round BLAKE3 inside one difference class, and a small residual search.

Implements the constructions of proof.md for blake3-r2-prefix-v1. The
organizer request is read from stdin and one message pair is returned per
trial: a 55-byte message A and a 63-byte message B that ends in eight zero
bytes. Only the standard library is used; there is no OS randomness, wall
time or ambient state. No BLAKE3 library is imported. The pairs the program
returns are built with the quarter-round G alone, and the organizer runner
recomputes both complete digests. The file contains its own 2-round
compression (compress2, written out from proof.md Section 1). It is called
only to check the counted batch, in the experiment "residual-search" and in
the self-test, on the batch's own messages, and never for a returned pair.
SHAKE-256 from the standard library is used only to expand the organizer's
seed into the trial's parameters.

Both experiments use the trial of proof.md Section 6.1: a context (step S1 of
Section 4 for seven words: the second and third value of the round-1 call C0,
the state words S11, S4, X13 and X14, and the message word w0) and one member
of the class of Lemma Q, that is one of the CLASS_SIZE values of Y4 for which
the first-half d difference of round-1 call E3 is the word ETA below. In
every trial w14 = 0, w15 = 0 and the top byte of w13 is zero, so that the 63
bytes of B end in eight zero bytes.

Experiment "half-collision": one trial per seed. The proof predicts that
digest words 0, 2, 5, 7 of A and B are equal for every seed.

Experiment "residual-search": the search of proof.md Section 6 at toy scale.
For one context taken from the seed it tries the class members k0, k0+1, ...
(all members of the class at most) and returns the first pair whose residual
has a zero low byte in digest word 1, so that 136 digest bits agree. The
number of members tried is reported as an untrusted observation. For the
same context one packed two-stage batch of proof.md Section 6.5, the batch
that holds member k0, is also evaluated on a machine that counts operations
and loads. Both stages are evaluated, whether or not stage A passes. The
operations and loads of each stage, whether a lane passes stage A, and the
number of lanes that are right are reported as untrusted observations. A
lane is right when the words of its message A are those of the trial, its
stage-A flag says whether the trial satisfies rule A, with h1 taken from the
compression of the lane's own message A, and its stage-2 word and flag equal
the test word of Lemma N, computed from the compressions of the lane's two
messages and again from their two complete digests. That batch is not part
of the search and has no influence on the returned pair.

Self-test of the operation count (not an organizer mode):

    python3 experiments/halfsearch.py --selftest N [seed]

runs N packed batches on contexts and list positions derived from the seed
text (default 1). Every fourth case is the last batch of the class, and in
every fifth each context word is 0, 2^32 - 1 or as drawn. It prints one JSON
line: cases, lanes checked and lanes right (as above, each lane against the
complete digests of its two messages), the lanes that pass rule A and the
batches in which one does, operations and loads per part and per stage, the
largest lane of a sum per part and overall, the largest number of registers
in use at one time, the number of constants per context and per value of
X14, the number of class members in the list, for how many of the 128
patterns of zero and nonzero lanes the flags are right, and for how many
packed words, in which every pattern of the bits of z that rule A reads
occurs once in every lane, the stage-A flags are right (a random case hardly
ever has a zero stage-2 word). The exit status is 0 when every lane is
right, the counts are those of TABLE below in every case, every sum is below
the bound of its part, the registers are at most 16, the list holds all
members of the class and all patterns are right.
"""

import hashlib
import json
import struct
import sys

MASK = 0xFFFFFFFF
IV = (0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A,
      0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19)
K = (IV[2] + IV[6]) & MASK
LEN_A, LEN_B = 55, 63
# The pinned round-1 column call C3 = G(3,7,11,15; w4, w13) of proof.md Section 3.
X3, X7, X11, X15 = 0x29D4FA98, 0xBEE3AF28, 0x44036000, 0x40C58500
W4, W13 = 0x97475638, 0x0007C006
W4B = (((W4 + K) & MASK) ^ LEN_A ^ LEN_B) - K & MASK
DELTA5 = (W4 - W4B) & MASK
# The class of proof.md Section 6.1.
ETA = 0x830303CF
# Rule A of proof.md Section 6.3 for this class: for every pair (mask, value), the XOR of the bits of h1 in mask is
# value. Three rules are written out, with four, five and six conditions; each contains the one before it.
# RULE_CONDITIONS is the one place that says which of them the batch uses.
RULES = {4: ((0x00000001, 0), (0x00000002, 1), (0x00010000, 0), (0x00020000, 0))}
RULES[5] = RULES[4] + ((0x0000000C, 1),)
RULES[6] = RULES[5] + ((0x00000180, 1),)
RULE_CONDITIONS = 5
RULE_A = RULES[RULE_CONDITIONS]
# The seven words of a context, in the order in which context() takes them.
CONTEXT_WORDS = ("C0.c1", "C0.d1", "S11", "S4", "X13", "X14", "w0")


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


def rule_a(h1):
    """Rule A on the word h1, the first-half d value of E3 on message A."""
    return all(bin(h1 & mask).count("1") & 1 == value for mask, value in RULE_A)


def rule_a_constants():
    """Lemma A: rule A as a condition on z, the XOR of the fifth and the second value of C2, for this class.

    Bit i of h1 is bit (i + 24) mod 32 of z XOR bit (i + 16) mod 32 of e1, and every bit of e1 that the rule meets
    is fixed by the class. A condition on one bit of h1 is a condition on one bit of z; a condition on the XOR of
    two bits of h1 is a condition on the XOR of two bits p < q of z and is kept at position p with the distance
    q - p. Returns (SHIFTS, ALL, V), SHIFTS a tuple of pairs (distance, mask of the positions p with that
    distance): a trial satisfies rule A exactly when ((z XOR y) AND ALL) == V, where y is the XOR over SHIFTS of
    ((z >> distance) AND mask).
    """
    shifts, everything, wanted = {}, 0, 0
    for mask, value in RULE_A:
        bits = [i for i in range(32) if mask >> i & 1]
        for i in bits:
            if not CLASS_MASK >> ((i + 16) % 32) & 1:
                raise ValueError("rule A meets a free bit of e1")
            value ^= CLASS_VALUE >> ((i + 16) % 32) & 1
        low = sorted((i + 24) % 32 for i in bits)
        if len(low) == 2:
            shifts[low[1] - low[0]] = shifts.get(low[1] - low[0], 0) | 1 << low[0]
        elif len(low) != 1:
            raise ValueError("rule A: a condition is neither one bit nor the XOR of two bits of z")
        if everything >> low[0] & 1:
            raise ValueError("rule A: two conditions at one position")
        everything |= 1 << low[0]
        wanted |= value << low[0]
    return tuple(sorted(shifts.items())), everything, wanted


A_SHIFTS, A_ALL, A_VALUE = rule_a_constants()
# (part, operations, loads, bound) of one batch of seven trials: the table of proof.md Section 6.5 and, in units of
# 2^32, the bound that Section 6.5 gives for the sums of the part. The first STAGE_A_PARTS parts are stage A, which
# every batch runs; the others are stage 2, which a batch runs only when one of its lanes passes rule A. The part
# "rule A" has three operations and one load for every distance of A_SHIFTS, and six operations and five loads more.
TABLE = (("loop", 3, 1, None), ("C0 backwards", 10, 8, 2), ("D0 and D1", 16, 10, 4), ("C2 to z", 17, 7, 5),
         ("rule A", 6 + 3 * len(A_SHIFTS), 5 + len(A_SHIFTS), 2),
         ("entry count", 3, 1, None), ("C2, rest", 12, 4, 6), ("D0 and D1, rest", 27, 13, 5), ("C1 to Y1", 18, 8, 9),
         ("E1, A and B", 40, 15, 13), ("E1 test", 15, 7, 2))
STAGE_A_PARTS = 5
# The budget of proof.md 6.4 step 4 on the batches that enter stage 2: a share 2^-STAGE_2_LOG2_SHARE of the batches
# of a run, one half, one quarter or one eighth for the rule with four, five or six conditions. A run has
# 2^TRIALS_LOG2 trials, that is 2^(TRIALS_LOG2 - 19) pairs of a context and a value of X14 with BATCHES batches each.
TRIALS_LOG2 = 102
STAGE_2_LOG2_SHARE = len(RULE_A) - 3
STAGE_2_BUDGET = BATCHES << (TRIALS_LOG2 - len(CLASS_FREE) - STAGE_2_LOG2_SHARE)


def class_member(k):
    """Y4 of class member number k: the bits of k fill the free positions of e1 in increasing order."""
    e1 = CLASS_VALUE
    for j, i in enumerate(CLASS_FREE):
        e1 |= (k >> j & 1) << i
    return (e1 - Y3) & MASK


def context(free):
    """Step S1: message words w, state X after round 0, state S after its column step, first half of C0.

    free holds the seven words of CONTEXT_WORDS. The words w8..w11 and the state words X0, X1, X5, X6, X10, X12
    belong to the trial and are left zero here; w14 = w15 = 0. Returns (X, S, w, (C0.b1, C0.c1, C0.d1)), the last
    being the fourth, third and second value of the round-1 call C0 = G(0,4,8,12; w2, w6). The first block of
    lines does not read X14; the second block is everything that does.
    """
    c0c, c0d, s11, s4, x13, x14, w0 = free
    X, S, w = [0] * 16, [0] * 16, [0] * 16
    X[3], X[7], X[11], X[15], X[13], X[14] = X3, X7, X11, X15, x13, x14
    S[4], S[11] = s4, s11
    w[0], w[4], w[13] = w0, W4, W13
    # K0 = G(0,4,8,12; w0, w1) with input (IV0, IV4, IV0, 0): forwards to its fourth value, then from S4
    a1_k0 = (IV[0] + IV[4] + w0) & MASK
    d1_k0 = ror(a1_k0, 16)
    c1_k0 = (IV[0] + d1_k0) & MASK
    b1_k0 = ror(IV[4] ^ c1_k0, 12)
    S[8] = rol(s4, 7) ^ b1_k0
    S[12] = (S[8] - c1_k0) & MASK
    S[0] = rol(S[12], 8) ^ d1_k0
    w[1] = (S[0] - a1_k0 - b1_k0) & MASK
    # D2 = G(2,7,8,13; w12, w13) backwards from its outputs X7, X8, X13; X8 from the third value of C0
    X[8] = (c0c - c0d) & MASK
    c1_d2 = (X[8] - x13) & MASK
    d1_d2 = (c1_d2 - S[8]) & MASK
    b1_d2 = rol(X7, 7) ^ X[8]
    S[7] = rol(b1_d2, 12) ^ c1_d2
    X[2] = rol(x13, 8) ^ d1_d2
    a1_d2 = (X[2] - b1_d2 - W13) & MASK
    S[13] = rol(d1_d2, 16) ^ a1_d2
    # K3 = G(3,7,11,15; w6, w7) with input (IV3, IV7, IV3, 11) backwards from its outputs S7, S11
    b1_k3 = rol(S[7], 7) ^ s11
    c1_k3 = rol(b1_k3, 12) ^ IV[7]
    d1_k3 = (c1_k3 - IV[3]) & MASK
    S[15] = (s11 - c1_k3) & MASK
    S[3] = rol(S[15], 8) ^ d1_k3
    a1_k3 = rol(d1_k3, 16) ^ 11
    w[6] = (a1_k3 - IV[3] - IV[7]) & MASK
    w[7] = (S[3] - a1_k3 - b1_k3) & MASK
    # K2 = G(2,6,10,14; w4, w5) with input (IV2, IV6, IV2, 55): its first four values
    a1_k2 = (K + W4) & MASK
    d1_k2 = ror(a1_k2 ^ LEN_A, 16)
    c1_k2 = (IV[2] + d1_k2) & MASK
    b1_k2 = ror(IV[6] ^ c1_k2, 12)
    # D3 = G(3,4,9,14; w14, w15) with w14 = w15 = 0: its first value from S3, S4, its fourth from the output X3
    a1_d3 = (S[3] + s4) & MASK
    b1_d3 = (X3 - a1_d3) & MASK
    c1_d3 = rol(b1_d3, 12) ^ s4
    # ---- the lines that read X14
    d1_d3 = rol(x14, 8) ^ X3
    S[9] = (c1_d3 - d1_d3) & MASK
    S[14] = rol(d1_d3, 16) ^ a1_d3
    X[9] = (c1_d3 + x14) & MASK
    X[4] = ror(b1_d3 ^ X[9], 7)
    # K2, rest
    S[10] = (c1_k2 + S[14]) & MASK
    S[6] = ror(b1_k2 ^ S[10], 7)
    S[2] = rol(S[14], 8) ^ d1_k2
    w[5] = (S[2] - a1_k2 - b1_k2) & MASK
    w[12] = (a1_d2 - S[2] - S[7]) & MASK
    # K1 = G(1,5,9,13; w2, w3) with input (IV1, IV5, IV1, 0) backwards from its outputs S9, S13
    c1_k1 = (S[9] - S[13]) & MASK
    d1_k1 = (c1_k1 - IV[1]) & MASK
    a1_k1 = rol(d1_k1, 16)
    b1_k1 = ror(IV[5] ^ c1_k1, 12)
    S[1] = rol(S[13], 8) ^ d1_k1
    S[5] = ror(b1_k1 ^ S[9], 7)
    w[2] = (a1_k1 - IV[1] - IV[5]) & MASK
    w[3] = (S[1] - a1_k1 - b1_k1) & MASK
    return X, S, w, (ror(X[4] ^ c0c, 12), c0c, c0d)


def messages(w):
    """Steps S2 and S3."""
    other = list(w)
    other[4] = W4B
    other[5] = (w[5] + DELTA5) & MASK
    return struct.pack("<16I", *w)[:LEN_A], struct.pack("<16I", *other)[:LEN_B]


def trial(X, S, w, c0, y4):
    """The trial of proof.md 6.1 for class member y4: returns (words, (X0, X1, X5, X6, X10, X12, Y12)).

    The words are those of the context with w8..w11 replaced. Round 0 maps them to the context's state with
    X0, X1, X5, X6, X10, X12 as returned; C0 then has b output y4 and d output Y12.
    """
    c0b, c0c, c0d = c0
    # C0 = G(0,4,8,12; w2, w6) backwards from its b output, with its second, third and fourth value kept
    y8 = rol(y4, 7) ^ c0b
    y12 = (y8 - c0c) & MASK
    y0 = rol(y12, 8) ^ c0d
    a1 = (y0 - c0b - w[6]) & MASK
    x0 = (a1 - X[4] - w[2]) & MASK
    x12 = rol(c0d, 16) ^ a1
    # D0 = G(0,5,10,15; w8, w9) backwards from its outputs X0, X15, with its input S kept
    d_d0 = rol(X15, 8) ^ x0
    c_d0 = (S[10] + d_d0) & MASK
    x10 = (c_d0 + X15) & MASK
    b_d0 = ror(S[5] ^ c_d0, 12)
    x5 = ror(b_d0 ^ x10, 7)
    a_d0 = rol(d_d0, 16) ^ S[15]
    # D1 = G(1,6,11,12; w10, w11) backwards from its outputs X11, X12, with its input S kept
    c_d1 = (X11 - x12) & MASK
    b_d1 = ror(S[6] ^ c_d1, 12)
    x6 = ror(b_d1 ^ X11, 7)
    d_d1 = (c_d1 - S[11]) & MASK
    x1 = rol(x12, 8) ^ d_d1
    a_d1 = rol(d_d1, 16) ^ S[12]
    words = list(w)
    words[8], words[9] = (a_d0 - S[0] - S[5]) & MASK, (x0 - a_d0 - b_d0) & MASK
    words[10], words[11] = (a_d1 - S[1] - S[6]) & MASK, (x1 - a_d1 - b_d1) & MASK
    return words, (x0, x1, x5, x6, x10, x12, y12)


def residual_word1(X, words, state, y4):
    """Digest word 1 of A xor digest word 1 of B for one trial (round 1, partial; proof.md 6.2)."""
    _, x1, x5, x6, x10, _, y12 = state
    c1 = g(x1, x5, X[9], X[13], words[3], words[10])
    c2 = g(X[2], x6, x10, X[14], words[7], words[0])
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
        low = self.band(self.shr(z, r), self.load(rep((1 << (32 - r)) - 1)))
        high = self.band(self.shl(z, 32 - r), self.load(rep(((1 << r) - 1) << (32 - r))))
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


def list_words(j):
    """The packed word U[j] of proof.md Section 6.5 and the seven class members it holds.

    Lane i holds member number 7 j + i; the spare lanes of the last word repeat the last member.
    """
    members = [class_member(min(LANES * j + i, CLASS_SIZE - 1)) for i in range(LANES)]
    u = sum(rol(y, 7) << (LANE_BITS * i) for i, y in enumerate(members))
    return u, members


def batch_constants(X, S, w, c0):
    """Every constant a batch loads, by name and in all seven lanes; and how many are per context and per X14.

    The algorithm computes and stores them before the batches (proof.md Section 8). Nothing here is counted in a
    batch. A constant is per X14 when it changes with X14, and per context when it changes only with the other
    six words of the context.
    """
    c0b, c0c, c0d = c0
    fixed = {"M": MASK, "ROL(X15,8)": rol(X15, 8), "X11+1": X11 + 1, "X11": X11, "-X15": -X15,
             "Y11": Y11, "Y11'": Y11B, "eta": ETA, "A all": A_ALL, "A value": A_VALUE}
    fixed.update(("A shift %d" % distance, mask) for distance, mask in A_SHIFTS)
    per_context = {"-C0.c1": -c0c, "C0.d1": c0d, "NOT ROL(C0.d1,16)": ~rol(c0d, 16), "X2+w7": X[2] + w[7],
                   "w0": w[0], "-S11": -S[11], "S12": S[12], "X13": X[13]}
    for_x14 = {"C0.b1": c0b, "-C0.b1-w6": -c0b - w[6], "-X4-w2": -X[4] - w[2], "S10+X15": S[10] + X15,
               "S6": S[6], "X14": X[14], "S5": S[5], "w3": w[3], "X9": X[9], "-S1-S6": -S[1] - S[6],
               "w12": w[12], "w5": w[5], "w5+delta": w[5] + DELTA5}
    c = {name: rep(value) for group in (fixed, per_context, for_x14) for name, value in group.items()}
    c["bit 32"] = ONES << 32
    return c, len(per_context), len(for_x14)


def lane_flags(m, c, word):
    """The end of a stage: bit 32 of every lane of word + M, set where the reduced word is nonzero, and the branch.

    Returns the seven flags and whether the branch is taken, that is whether some lane has a zero word.
    """
    flags = m.band(m.add(word, m.load(c["M"])), m.load(c["bit 32"]))
    taken = m.compare_and_branch(flags, m.load(c["bit 32"]))
    return [(flags.z >> (LANE_BITS * i + 32)) & 1 for i in range(LANES)], taken


def rule_a_word(m, c, z):
    """The stage-A word of Lemma A for seven lanes z: zero exactly in the lanes whose trial satisfies rule A."""
    y = z
    for distance, _ in A_SHIFTS:
        y = m.xor(y, m.band(m.shr(z, distance), m.load(c["A shift %d" % distance])))
    return m.xor(m.band(y, m.load(c["A all"])), m.load(c["A value"]))


def packed_batch(m, c, j, entered=0):
    """The two-stage batch of proof.md Section 6.5 for the seven trials of batch j, counted on the machine m.

    c holds the constants of batch_constants. Every line below is made of calls of m only, so every operation
    and every load is counted. The names are those of proof.md 6.1 to 6.5; the parts and their order are those of
    TABLE. The algorithm runs the parts of stage 2 only when the branch of stage A is taken; this function always
    evaluates them, so that their count and their lanes can be checked for every batch. entered is the number of
    batches that have entered stage 2 before this one; stage 2 begins by counting its own entry and comparing the
    count with STAGE_2_BUDGET (step 4 of proof.md 6.4). Returns the seven reduced
    stage-2 test words, their seven flags (1 where the word is nonzero), whether the final branch is taken, the
    seven stage-A flags (1 where the trial fails rule A) and whether the stage-A branch is taken.
    """
    def k(name):
        return m.load(c[name])

    u, _ = list_words(j)
    m.at("loop")                                                      # next list position, end test, branch
    m.compare_and_branch(m.advance(j), m.load(BATCHES))
    m.at("C0 backwards")
    y8 = m.xor(m.load(u), k("C0.b1"))
    y12 = m.add(y8, k("-C0.c1"))
    y0 = m.xor(m.prol(y12, 8), k("C0.d1"))
    ca = m.add(y0, k("-C0.b1-w6"))                                    # first value of C0
    nx12 = m.xor(ca, k("NOT ROL(C0.d1,16)"))                          # NOT X12
    m.at("D0 and D1")
    dd0 = m.xor(m.add(ca, k("-X4-w2")), k("ROL(X15,8)"))              # X0, then the second value of D0
    x10 = m.add(dd0, k("S10+X15"))                                    # X10 = (S10 + dd0) + X15
    cd1 = m.add(nx12, k("X11+1"))                                     # X11 - X12, the third value of D1
    bd1 = m.pror(m.xor(cd1, k("S6")), 12)
    x6 = m.pror(m.xor(bd1, k("X11")), 7)
    m.at("C2 to z")
    ra = m.add(x6, k("X2+w7"))                                        # X2 + X6 + w7
    rd = m.pror(m.xor(ra, k("X14")), 16)
    rc = m.add(x10, rd)
    rb = m.pror(m.xor(rc, x6), 12)
    z = m.xor(m.add(m.add(ra, rb), k("w0")), rd)                      # Y14 = ROR(z, 8)
    m.at("rule A")
    flags_a, taken_a = lane_flags(m, c, rule_a_word(m, c, z))
    # ---- stage 2
    m.at("entry count")                                               # one more entry, budget test, branch
    m.compare_and_branch(m.advance(entered), m.load(STAGE_2_BUDGET))
    m.at("C2, rest")
    y14 = m.pror(z, 8)
    y6 = m.pror(m.xor(m.add(rc, y14), rb), 7)
    m.at("D0 and D1, rest")
    bd0 = m.pror(m.xor(m.add(x10, k("-X15")), k("S5")), 12)           # the third value of D0 is X10 - X15
    x5 = m.pror(m.xor(bd0, x10), 7)
    dd1 = m.add(cd1, k("-S11"))
    x1 = m.xor(m.xor(m.prol(nx12, 8), dd1), k("M"))                   # ROL(X12,8) XOR dd1
    ad1 = m.xor(m.prol(dd1, 16), k("S12"))
    m.at("C1 to Y1")
    qa = m.add(m.add(x1, x5), k("w3"))
    qd = m.pror(m.xor(qa, k("X13")), 16)
    qc = m.add(qd, k("X9"))
    qb = m.pror(m.xor(qc, x5), 12)
    y1 = m.add(m.add(m.add(qa, qb), ad1), k("-S1-S6"))                # fifth assignment, with w10 = ad1 - S1 - S6
    m.at("E1, A and B")
    a1 = m.add(m.add(y1, y6), k("w12"))
    d1 = m.pror(m.xor(a1, y12), 16)
    c1 = m.add(d1, k("Y11"))
    c1b = m.add(d1, k("Y11'"))
    b1 = m.pror(m.xor(c1, y6), 12)
    b1b = m.pror(m.xor(c1b, y6), 12)
    a2 = m.add(m.add(a1, b1), k("w5"))
    a2b = m.add(m.add(a1, b1b), k("w5+delta"))
    c2 = m.add(c1, m.pror(m.xor(a2, d1), 8))
    c2b = m.add(c1b, m.pror(m.xor(a2b, d1), 8))
    m.at("E1 test")
    eps = m.xor(c2, c2b)
    x = m.xor(m.xor(b1, b1b), eps)                                    # beta XOR eps
    word = m.band(m.xor(m.xor(m.prol(x, 1), eps), k("eta")), k("M"))  # the reduced test word of Lemma N
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


def reference(X, S, w, c0, y4):
    """What the batch must show for one trial, taken from the compressions of the trial's two real messages.

    The messages A (55 bytes) and B (63 bytes) of the trial are built by steps S2 and S3 and each is compressed in
    full by compress2. Returned: Y4 of A; h1, the second value of E3 on A, from the state Y of A; the test word of
    Lemma N from E1 evaluated for A and for B with g on their own states and words; the same word from the two
    complete digests, digest word 3 XOR ROL(digest word 6, 8) of the XOR of the digests; whether the digests
    agree on digest words 0, 2, 5, 7 with the same Y4 in A and B; and whether the sixteen words of the 55 bytes of
    A are the words of the trial, which needs w14 = w15 = 0 and a zero top byte of w13.
    """
    words = trial(X, S, w, c0, y4)[0]
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


def batch_check(X, S, w, c0, j, machine=None):
    """Batch j of the class for a context, on a new machine unless one is given.

    Returns a dict: operations and loads of stage A and of stage 2, the number of lanes that are right, the number
    of lanes that pass rule A, whether the batch enters stage 2, and the number of zero stage-2 test words. A lane
    is right when all of this holds for its trial and the reference of its two real messages: the words of
    message A are the words of the trial; Y4 of message A is the member of the lane; the digests agree on digest
    words 0, 2, 5, 7; the stage-A flag is 0 exactly when h1 satisfies rule A; the reduced stage-2 word equals the
    word of Lemma N, which in turn equals the word from the two complete digests; and the stage-2 flag tells
    whether that word is nonzero. No lane counts as right when one of the two branches is not taken exactly if
    one of the seven words in front of it is zero.
    """
    m = machine or Machine()
    words, flags, taken, flags_a, taken_a = packed_batch(m, batch_constants(X, S, w, c0)[0], j)
    members = list_words(j)[1]
    refs = [reference(X, S, w, c0, y4) for y4 in members]
    passing = [int(rule_a(r["h1"])) for r in refs]
    right = sum(int(r["words"] == 1 and r["y4"] == members[i] and r["half"] == 1 and flags_a[i] == 1 - passing[i]
                    and words[i] == r["word"] and r["word"] == r["word_from_digests"] and flags[i] == int(r["word"] != 0))
                for i, r in enumerate(refs))
    zero = sum(int(r["word"] == 0) for r in refs)
    if taken_a != (1 in passing) or taken != (zero > 0):
        right = 0
    parts = list(m.ops)
    stage_a, stage_2 = parts[:STAGE_A_PARTS], parts[STAGE_A_PARTS:]
    return {"stage_a_operations": sum(m.ops[p] for p in stage_a), "stage_a_loads": sum(m.loads[p] for p in stage_a),
            "stage_2_operations": sum(m.ops[p] for p in stage_2), "stage_2_loads": sum(m.loads[p] for p in stage_2),
            "lanes_right": right, "lanes_passing_rule_a": sum(passing), "stage_2_entered": int(taken_a),
            "zero_test_words": zero}


def seeded(seed):
    """The seven words of a context and a class member number from the organizer seed."""
    stream = struct.unpack("<8I", hashlib.shake_256(seed).digest(32))
    return context(stream[:7]), stream[7] % CLASS_SIZE


def half_collision(seed):
    (X, S, w, c0), k = seeded(seed)
    return messages(trial(X, S, w, c0, class_member(k))[0]) + ({},)


def residual_search(seed):
    (X, S, w, c0), k0 = seeded(seed)
    checked = batch_check(X, S, w, c0, k0 // LANES)
    counted = {"batch_" + key: checked[key] for key in ("stage_a_operations", "stage_a_loads", "stage_2_operations",
                                                        "stage_2_loads", "lanes_right", "stage_2_entered")}
    for step in range(CLASS_SIZE):
        y4 = class_member((k0 + step) % CLASS_SIZE)
        words, state = trial(X, S, w, c0, y4)
        if residual_word1(X, words, state, y4) & 0xFF == 0:
            return messages(words) + (dict(counted, tries=step + 1),)
    return None, None, dict(counted, tries=CLASS_SIZE)


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
    """The stage-A word on all patterns of the bits of z that rule A reads.

    One packed word per pattern: lane i holds the pattern number (p + 37 i) modulo the number of patterns, so every
    pattern occurs once in every lane and the lanes of a word differ. The bits of z outside the rule are different
    in every lane, the guard bits 32..35 of the lanes are filled, and every lane belongs to another member of the
    class. A word is right when in every lane the flag is 0 exactly if h1 = ROR(ROR(z, 8) XOR e1, 16), with
    e1 = Y3 + Y4 of the lane's member, satisfies rule A as written on h1, and the branch is taken exactly if some
    lane does. Returns (words, words right, words in which some lane satisfies the rule).
    """
    everything = A_ALL
    for distance, mask in A_SHIFTS:
        everything |= mask << distance
    read = [i for i in range(32) if everything >> i & 1]
    c = {"M": rep(MASK), "bit 32": ONES << 32, "A all": rep(A_ALL), "A value": rep(A_VALUE)}
    c.update(("A shift %d" % distance, rep(mask)) for distance, mask in A_SHIFTS)
    right = satisfied = 0
    for pattern in range(1 << len(read)):
        zs, passing = [], []
        for lane in range(LANES):
            number = (pattern + 37 * lane) % (1 << len(read))
            base = sum((number >> n & 1) << i for n, i in enumerate(read))
            other = struct.unpack("<I", hashlib.shake_256(b"rule A %d %d" % (pattern, lane)).digest(4))[0]
            z = base | (other & ~everything & MASK)
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
        stream = struct.unpack("<9I", hashlib.shake_256(text.encode("utf-8")).digest(36))
        seven, j = list(stream[:7]), stream[7] % BATCHES
        if case % 4 == 0:                       # the last batch of the class, whose spare lanes repeat the last member
            j, last = BATCHES - 1, last + 1
        if case % 5 == 4:                       # extreme words: each context word is 0, 2^32 - 1 or as drawn
            seven = [(0, MASK, v, v)[stream[8] >> 2 * i & 3] for i, v in enumerate(seven)]
            extreme += 1
        X, S, w, c0 = context(seven)
        machine = Machine()
        checked = batch_check(X, S, w, c0, j, machine)
        for key in total:
            total[key] += checked[key]
        found = (tuple((part, machine.ops[part], machine.loads[part]) for part in machine.ops), machine.registers(),
                 batch_constants(X, S, w, c0)[1:])
        shape = shape or found
        same = same and found == shape
        for part, top in machine.sums.items():
            sums[part] = max(sums.get(part, 0), top)
    table, registers, (per_context, for_x14) = shape
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
        "selftest": "two-stage packed batch of proof.md Section 6.5",
        "seed": seed, "cases": cases, "last_batches": last, "extreme_cases": extreme,
        "message_bytes": [LEN_A, LEN_B], "rule_conditions": len(RULE_A), "stage_2_log2_share": STAGE_2_LOG2_SHARE,
        "lanes_checked": cases * LANES, "lanes_right": total["lanes_right"],
        "lanes_passing_rule_a": total["lanes_passing_rule_a"], "batches_entering_stage_2": total["stage_2_entered"],
        "zero_test_words": total["zero_test_words"],
        "parts": parts,
        "stage_a": {"operations": sum(row[1] for row in stage_a), "loads": sum(row[2] for row in stage_a)},
        "stage_2": {"operations": sum(row[1] for row in stage_2), "loads": sum(row[2] for row in stage_2)},
        "same_counts_in_every_case": same, "counts_equal_table": table == tuple(row[:3] for row in TABLE),
        "largest_lane": largest, "largest_lane_bits": largest.bit_length(), "lane_bits": LANE_BITS,
        "sums_below_bounds": below,
        "registers": registers, "register_limit": REGISTERS,
        "per_context_constants": per_context, "per_x14_constants": for_x14,
        "list_words": BATCHES, "members_in_list": len(members),
        "zero_lane_patterns": 1 << LANES, "zero_lane_patterns_right": flags,
        "rule_a_patterns": patterns, "rule_a_patterns_right": patterns_right, "rule_a_patterns_satisfied": patterns_satisfied,
        "rule_a_on_z": {"shifts": [[distance, "%08x" % mask] for distance, mask in A_SHIFTS],
                        "all": "%08x" % A_ALL, "value": "%08x" % A_VALUE},
    }
    json.dump(report, sys.stdout, separators=(",", ":"))
    sys.stdout.write("\n")
    good = (total["lanes_right"] == cases * LANES and same and report["counts_equal_table"] and below
            and registers <= REGISTERS and len(members) == CLASS_SIZE and flags == 1 << LANES
            and patterns_right == patterns)
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
