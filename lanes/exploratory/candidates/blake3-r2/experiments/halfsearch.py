"""Half-collisions of 2-round BLAKE3 inside one difference class, and a small residual search.

Implements the constructions of proof.md for blake3-r2-prefix-v1. The
organizer request is read from stdin and one message pair is returned per
trial: a 60-byte message A and a 62-byte message B. Only the standard library
is used; there is no OS randomness, wall time or ambient state. The program
never calls BLAKE3 or any implementation of the target: it evaluates the
quarter-round G directly, and the organizer runner recomputes both complete
digests. SHAKE-256 from the standard library is used only to expand the
organizer's seed into the trial's parameters.

Both experiments use the trial of proof.md Section 6.1: a context (step S1 of
Section 4 for nine state words), a value alpha of the D0 family and one member
of the class of Lemma Q, that is one of the 4096 values of Y4 for which the
first-half d difference of round-1 call E3 is eta = e96d6d6b.

Experiment "half-collision": one trial per seed. The proof predicts that
digest words 0, 2, 5, 7 of A and B are equal for every seed.

Experiment "residual-search": the search of proof.md Section 6 at toy scale.
For one context and one alpha taken from the seed it tries the class members
k0, k0+1, ... (all 4096 members at most) and returns the first pair whose
residual has a zero low byte in digest word 1, so that 136 digest bits agree.
The number of members tried is reported as an untrusted observation. For the
same context and alpha one packed batch of proof.md Section 6.5, the batch
that holds member k0, is also evaluated on a machine that counts operations
and loads. Its two counts and the number of its lanes that equal the scalar
early-test word of Lemma E are reported as untrusted observations. That
batch is not part of the search and has no influence on the returned pair.

Self-test of the operation count (not an organizer mode):

    python3 experiments/halfsearch.py --selftest N [seed]

runs N packed batches on contexts, values of alpha and list positions derived
from the seed text (default 1). Every fourth case is the last batch of the
class, and in every fifth each context word and alpha is 0, 2^32 - 1 or as
drawn. It prints one JSON line: cases, lanes checked, lanes equal to the
scalar word, scalar words that are zero, operations and loads per part and in
total, the largest lane of a sum per part and overall, the largest number of
registers in use at one time, the number of constants per context and per
alpha, the number of class members in the two lists, and for how many of the
128 patterns of zero and nonzero lanes the final flags are right (a random
case hardly ever has a zero word). The exit status is 0 when every lane
is equal, the counts are those of the table in Section 6.5 in every case,
every sum is below the bound quoted there, the registers are at most 16, the
lists hold all 4096 members and all 128 patterns are right.
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
X3, X7, X11, X15 = 0xA6C3B8C5, 0x793C473A, 0x5C32535C, 0x8367C7BB
W4, W13 = 0x60000001, 0x29BD3F58
W4B = (((W4 + K) & MASK) ^ LEN_A ^ LEN_B) - K & MASK
DELTA5 = (W4 - W4B) & MASK
# The class of proof.md Section 6.1.
ETA = 0xE96D6D6B
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
# 2^32, the bound that Section 6.5 gives for the sums of the part (the general bound 10 where it names no other).
TABLE = (("loop", 3, 1, None), ("C0 backwards", 9, 7, 2), ("K3", 27, 14, 6), ("D1", 9, 6, 2), ("C1", 24, 11, 6),
         ("C2", 28, 12, 8), ("E1, A and B", 26, 11, 10), ("E3, A and B", 15, 6, 4), ("early test", 13, 6, 10))


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
        """The next list position: one addition to the register that holds the position."""
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
        step of its last use, whose result may take its place. One more
        register holds the list position from batch to batch.
        """
        change = [0] * (self.step + 1)
        for value in self.values:
            change[value.born] += 1
            change[value.last] -= 1
        held = peak = 0
        for delta in change:
            held += delta
            peak = max(peak, held)
        return peak + 1


class ResidentMachine(Machine):
    """Fourteen immutable registers persist across the 586 batches of an alpha.

    Loading these registers is setup, charged separately (14 loads per alpha,
    conservatively repeated even though these values are global). No value is
    cached by numerical equality: only the fourteen named constants are resident.
    Other constants and both class-list words remain charged memory loads.
    Python bookkeeping is an emulator, not the claimed RAM implementation.
    """
    def __init__(self):
        super().__init__()
        values = {"M": rep(MASK), "bit 32": ONES << 32}
        for r in (1, 7, 8, 12, 16, 24):
            values["L" + str(r)] = rep((1 << (32 - r)) - 1)
            values["H" + str(r)] = rep(((1 << r) - 1) << (32 - r))
        self.resident = {name: Packed(value, 0) for name, value in values.items()}
        self.preload_operations = len(values)

    def constant(self, name, value):
        if name in self.resident:
            result = self.resident[name]
            if result.z != value:
                raise AssertionError("resident constant mismatch")
            return result
        return self.load(value)

    def registers(self):
        # Keep every resident register throughout. Add three slots beyond the
        # base machine's list-index reservation: destination + two list bases.
        return super().registers() + len(self.resident) + 3


def list_words(j):
    """The packed words U[j] and V[j] of proof.md Section 6.5 and the seven class members they hold.

    Lane i holds member number 7 j + i; the six spare lanes of the last word repeat the last member.
    """
    members = [class_member(min(LANES * j + i, CLASS_SIZE - 1)) for i in range(LANES)]
    u = sum(rol(y, 7) << (LANE_BITS * i) for i, y in enumerate(members))
    v = sum(((Y3 + y) & MASK) << (LANE_BITS * i) for i, y in enumerate(members))
    return u, v, members


def batch_constants(X, S, w, alpha):
    """Every constant a batch loads, by name and in all seven lanes; and how many are per context and per alpha.

    The algorithm computes and stores them before the batches (proof.md Section 8). Nothing here is counted in a batch.
    """
    _, x5, _, _, pa, pd, pc, pb = per_alpha(X, S, w, alpha)
    fixed = {"M": MASK, "1": 1, "11": 11, "IV3": IV[3], "IV7": IV[7], "Y11": Y11, "Y11'": Y11B, "eta": ETA}
    per_context = {"ROL(S7,7)": rol(S[7], 7), "X2+X6+1": X[2] + X[6] + 1, "X11-X12+1": X11 - X[12] + 1,
                   "ROL(X12,8)": rol(X[12], 8), "S12": S[12], "X13": X[13], "X9": X[9], "-S1-S6": -S[1] - S[6],
                   "X14": X[14], "X6": X[6], "w0": w[0], "w12": w[12], "w5": w[5], "w5+delta": w[5] + DELTA5}
    for_alpha = {"pb": pb, "-pc": -pc, "pd": pd, "IV3+IV7-pa-pb": IV[3] + IV[7] - pa - pb,
                 "X5": x5, "X5+w3": x5 + w[3], "alpha": alpha}
    c = {name: rep(value) for group in (fixed, per_context, for_alpha) for name, value in group.items()}
    c["bit 32"] = ONES << 32
    return c, len(per_context), len(for_alpha)


def lane_flags(m, c, word):
    """The end of a batch: bit 32 of every lane of word + M, set where the reduced word is nonzero, and the branch.

    Returns the seven flags and whether the branch is taken, that is whether some lane has a zero word.
    """
    flags = m.band(m.add(word, m.constant("M", c["M"])), m.constant("bit 32", c["bit 32"]))
    taken = m.compare_and_branch(flags, m.constant("bit 32", c["bit 32"]))
    return [(flags.z >> (LANE_BITS * i + 32)) & 1 for i in range(LANES)], taken


def packed_batch(m, c, j):
    """The early test of Lemma E for the seven trials of batch j in one packed word, counted on the machine m.

    c holds the constants of batch_constants. Every line below is made of calls of m only, so every operation
    and every load is counted. The names are those of proof.md 6.1 to 6.5; the parts and their order are those of
    TABLE. Returns the seven reduced test words, the seven flags (1 where the word is nonzero) and whether the
    final branch is taken.
    """
    def k(name):
        return m.constant(name, c[name])

    u, v, _ = list_words(j)
    m.at("loop")                                                      # next list position, end test, branch
    m.compare_and_branch(m.advance(j), m.load(BATCHES))
    m.at("C0 backwards")
    y8 = m.xor(m.load(u), k("pb"))
    y12 = m.add(y8, k("-pc"))
    y0 = m.xor(m.prol(y12, 8), k("pd"))
    ka = m.add(y0, k("IV3+IV7-pa-pb"))                                # IV[3] + IV[7] + w6
    m.at("K3")
    kd = m.pror(m.xor(ka, k("11")), 16)
    kc = m.add(kd, k("IV3"))
    kb = m.pror(m.xor(kc, k("IV7")), 12)
    s11 = m.xor(kb, k("ROL(S7,7)"))
    s15 = m.add(m.add(s11, m.xor(kc, k("M"))), k("1"))                # S11 - kc
    s3 = m.xor(m.prol(s15, 8), kd)
    first = m.add(m.add(s3, m.xor(m.add(ka, kb), k("M"))), k("X2+X6+1"))  # v = X2 + X6 + w7, w7 = S3 - ka - kb
    m.at("D1")
    d = m.add(m.xor(s11, k("M")), k("X11-X12+1"))                     # (X11 - X12) - S11
    x1 = m.xor(d, k("ROL(X12,8)"))
    a = m.xor(m.prol(d, 16), k("S12"))
    m.at("C1")
    qa = m.add(x1, k("X5+w3"))
    qd = m.pror(m.xor(qa, k("X13")), 16)
    qc = m.add(qd, k("X9"))
    qb = m.pror(m.xor(qc, k("X5")), 12)
    y1 = m.add(m.add(m.add(qa, qb), a), k("-S1-S6"))                  # fifth assignment, with w10 = a - S1 - S6
    y9 = m.add(qc, m.pror(m.xor(y1, qd), 8))
    m.at("C2")
    rd = m.pror(m.xor(first, k("X14")), 16)
    rc = m.add(rd, k("alpha"))
    rb = m.pror(m.xor(rc, k("X6")), 12)
    ra = m.add(m.add(first, rb), k("w0"))
    y14 = m.pror(m.xor(ra, rd), 8)
    y6 = m.pror(m.xor(m.add(rc, y14), rb), 7)
    m.at("E1, A and B")
    a1 = m.add(m.add(y1, y6), k("w12"))
    d1 = m.pror(m.xor(a1, y12), 16)
    c1 = m.add(d1, k("Y11"))
    c1b = m.add(d1, k("Y11'"))
    b1 = m.pror(m.xor(c1, y6), 12)
    b1b = m.pror(m.xor(c1b, y6), 12)
    a2 = m.add(m.add(a1, b1), k("w5"))
    a2b = m.add(m.add(a1, b1b), k("w5+delta"))
    m.at("E3, A and B")
    h1 = m.pror(m.xor(y14, m.load(v)), 16)
    h1b = m.xor(h1, k("eta"))
    g1 = m.add(y9, h1)
    g1b = m.add(y9, h1b)
    fx = m.pror(m.xor(g1, g1b), 12)                                   # f1 XOR f1'
    m.at("early test")
    t = m.xor(a2, a2b)
    word = m.band(m.xor(m.xor(fx, t), m.pror(t, 1)), k("M"))          # the reduced test word
    flags, taken = lane_flags(m, c, word)
    return lanes(word.z), flags, taken


def scalar_early(X, S, w, alpha, y4):
    """The test word (f1 XOR f1') XOR t XOR ROR(t, 1) of Lemma E for one trial, in 32-bit arithmetic.

    It is computed forwards from the trial's message words: C0, C1 and C2 with g, then the first halves of E1 and
    of E3 for both messages as written in proof.md 6.2 and 6.3, without the shortcuts of the batch.
    """
    pre = per_alpha(X, S, w, alpha)
    words, x1, x5, _ = trial(X, S, w, alpha, y4, pre)
    c0 = g(pre[0], X[4], X[8], X[12], words[2], words[6])
    c1 = g(x1, x5, X[9], X[13], words[3], words[10])
    c2 = g(X[2], X[6], alpha, X[14], words[7], words[0])
    y4, y12, y1, y9, y6, y14 = c0[1], c0[3], c1[0], c1[2], c2[1], c2[3]
    a1 = (y1 + y6 + words[12]) & MASK
    d1 = ror(y12 ^ a1, 16)
    b1, b1b = ror(y6 ^ ((Y11 + d1) & MASK), 12), ror(y6 ^ ((Y11B + d1) & MASK), 12)
    t = ((a1 + b1 + words[5]) & MASK) ^ ((a1 + b1b + words[5] + DELTA5) & MASK)
    f1 = ror(y4 ^ ((y9 + ror(y14 ^ ((Y3 + y4 + words[15]) & MASK), 16)) & MASK), 12)
    f1b = ror(y4 ^ ((y9 + ror(y14 ^ ((Y3B + y4 + words[15]) & MASK), 16)) & MASK), 12)
    return f1 ^ f1b ^ t ^ ror(t, 1)


def batch_check(X, S, w, alpha, j, machine=None):
    """Batch j of the class for a context and an alpha, on a new machine unless one is given.

    Returns (operations, loads, lanes equal, scalar words that are zero). A lane is equal when its reduced test
    word is the scalar word of its trial and its flag tells whether that word is nonzero. No lane counts as equal
    when the final branch is not taken exactly if one of the seven scalar words is zero.
    """
    m = machine or Machine()
    words, flags, taken = packed_batch(m, batch_constants(X, S, w, alpha)[0], j)
    scalar = [scalar_early(X, S, w, alpha, y4) for y4 in list_words(j)[2]]
    equal = sum(int(words[i] == scalar[i] and flags[i] == int(scalar[i] != 0)) for i in range(LANES))
    return sum(m.ops.values()), sum(m.loads.values()), equal if taken == (0 in scalar) else 0, scalar.count(0)


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
    operations, loads, equal, _ = batch_check(X, S, w, alpha, k0 // LANES)
    counted = {"batch_operations": operations, "batch_loads": loads, "batch_lanes_equal": equal}
    pre = per_alpha(X, S, w, alpha)
    for step in range(CLASS_SIZE):
        y4 = class_member((k0 + step) % CLASS_SIZE)
        words, x1, x5, y12 = trial(X, S, w, alpha, y4, pre)
        if residual_word1(X, words, alpha, x1, x5, y4, y12) & 0xFF == 0:
            return messages(words) + (dict(counted, tries=step + 1),)
    return None, None, dict(counted, tries=CLASS_SIZE)


class FullResidentMachine(Machine):
    """Forty-two immutable registers persist across the 586 batches of an alpha (64-register machine).

    Pins the 14 mask constants, 7 fixed constants (including BATCHES; constant '1' is eliminated by
    complement propagation ~S15 = ~S11 + kc), 14 per-context constants (with ~ROL(S7,7) and X2+X6),
    and 7 per-alpha constants. Only the two class-list words U[j] and V[j] are loaded from memory per batch.
    """
    def __init__(self, constants):
        super().__init__()
        values = {"M": rep(MASK), "bit 32": ONES << 32, "BATCHES": BATCHES}
        for r in (1, 7, 8, 12, 16, 24):
            values["L" + str(r)] = rep((1 << (32 - r)) - 1)
            values["H" + str(r)] = rep(((1 << r) - 1) << (32 - r))
        for name, val in constants.items():
            if name not in ("1", "ROL(S7,7)", "X2+X6+1"):
                values[name] = val
        assert len(values) == 42, f"expected 42 resident constants, got {len(values)}"
        self.resident = {name: Packed(value, 0) for name, value in values.items()}
        self.preload_operations = len(values)

    def constant(self, name, value):
        if name in self.resident:
            result = self.resident[name]
            if result.z != value:
                raise AssertionError("resident constant mismatch")
            return result
        return self.load(value)

    def registers(self):
        return super().registers() + len(self.resident) + 3


def packed_batch_opt(m, c, j):
    """Complement-propagated batch (151 ALU/control ops + 2 list loads on FullResidentMachine).

    Uses ~S11 = kb ^ (~ROL(S7,7)), ~S15 = ~S11 + kc (1 ADD instead of 3 ops), ~S3 = ROL(~S15,8) ^ kd,
    first = ((~S3 + ka + kb) ^ M) + (X2 + X6), and d = ~S11 + (X11 - X12 + 1) (1 ADD instead of 2 ops).
    """
    def k(name):
        return m.constant(name, c[name])

    u, v, _ = list_words(j)
    m.at("loop")
    m.compare_and_branch(m.advance(j), m.constant("BATCHES", BATCHES))
    m.at("C0 backwards")
    y8 = m.xor(m.load(u), k("pb"))
    y12 = m.add(y8, k("-pc"))
    y0 = m.xor(m.prol(y12, 8), k("pd"))
    ka = m.add(y0, k("IV3+IV7-pa-pb"))
    m.at("K3")
    kd = m.pror(m.xor(ka, k("11")), 16)
    kc = m.add(kd, k("IV3"))
    kb = m.pror(m.xor(kc, k("IV7")), 12)
    ns11 = m.xor(kb, k("~ROL(S7,7)"))
    ns15 = m.add(ns11, kc)
    ns3 = m.xor(m.prol(ns15, 8), kd)
    first = m.add(m.xor(m.add(ns3, m.add(ka, kb)), k("M")), k("X2+X6"))
    m.at("D1")
    d = m.add(ns11, k("X11-X12+1"))
    x1 = m.xor(d, k("ROL(X12,8)"))
    a = m.xor(m.prol(d, 16), k("S12"))
    m.at("C1")
    qa = m.add(x1, k("X5+w3"))
    qd = m.pror(m.xor(qa, k("X13")), 16)
    qc = m.add(qd, k("X9"))
    qb = m.pror(m.xor(qc, k("X5")), 12)
    y1 = m.add(m.add(m.add(qa, qb), a), k("-S1-S6"))
    y9 = m.add(qc, m.pror(m.xor(y1, qd), 8))
    m.at("C2")
    rd = m.pror(m.xor(first, k("X14")), 16)
    rc = m.add(rd, k("alpha"))
    rb = m.pror(m.xor(rc, k("X6")), 12)
    ra = m.add(m.add(first, rb), k("w0"))
    y14 = m.pror(m.xor(ra, rd), 8)
    y6 = m.pror(m.xor(m.add(rc, y14), rb), 7)
    m.at("E1, A and B")
    a1 = m.add(m.add(y1, y6), k("w12"))
    d1 = m.pror(m.xor(a1, y12), 16)
    c1 = m.add(d1, k("Y11"))
    c1b = m.add(d1, k("Y11'"))
    b1 = m.pror(m.xor(c1, y6), 12)
    b1b = m.pror(m.xor(c1b, y6), 12)
    a2 = m.add(m.add(a1, b1), k("w5"))
    a2b = m.add(m.add(a1, b1b), k("w5+delta"))
    m.at("E3, A and B")
    h1 = m.pror(m.xor(y14, m.load(v)), 16)
    h1b = m.xor(h1, k("eta"))
    g1 = m.add(y9, h1)
    g1b = m.add(y9, h1b)
    fx = m.pror(m.xor(g1, g1b), 12)
    m.at("early test")
    t = m.xor(a2, a2b)
    word = m.band(m.xor(m.xor(fx, t), m.pror(t, 1)), k("M"))
    flags, taken = lane_flags(m, c, word)
    return lanes(word.z), flags, taken


def resident_audit(seed):
    """Exact attack seed layout (S5 shared across contexts), bounded packed/scalar and H1/H2 audit.

    Four contexts share X2,X5,X6,X9 and X10=0, so S5 is held fixed across all four
    contexts just as in proof.md Section 6.4. X12 is restricted to eight bits.
    Both the first and padded last list batch are included. Audits the 64-register
    full-resident complement-propagated schedule (151 ops, 2 list loads), the
    32-register resident-mask schedule, and counts early-test passes (H2) and
    low-nibble residual hits (H1) across the shared-seed S5-fixed trials.
    """
    stream = struct.unpack("<16I", hashlib.shake_256(seed).digest(64))
    fixed = stream[:4]
    checked = 0
    early_passes = 0
    low4_hits = 0
    s5_values = set()
    peak32 = 0
    peak64 = 0
    last_pair = None
    for index in range(4):
        x12 = (stream[4] + index) & 255
        x13 = (stream[5] + index) & MASK
        x14 = stream[6]
        free = [0, fixed[0], fixed[1], fixed[2], fixed[3], 0, x12, x13, x14]
        X, S, w = context(free)
        s5_values.add(S[5])
        alpha = stream[7 + index]
        pre = per_alpha(X, S, w, alpha)
        for j in (0, BATCHES - 1):
            baseline = Machine()
            resident = ResidentMachine()
            constants = batch_constants(X, S, w, alpha)[0]
            constants["~ROL(S7,7)"] = rep(~rol(S[7], 7) & MASK)
            constants["X2+X6"] = rep((X[2] + X[6]) & MASK)
            full_res = FullResidentMachine(constants)
            ordinary = packed_batch(baseline, constants, j)
            changed = packed_batch(resident, constants, j)
            opt_out = packed_batch_opt(full_res, constants, j)
            if ordinary != changed or ordinary != opt_out:
                raise AssertionError("resident/reference mismatch")
            members = list_words(j)[2]
            expected = [scalar_early(X, S, w, alpha, y) for y in members]
            if opt_out[0] != expected or opt_out[2] != (0 in expected):
                raise AssertionError("resident/scalar mismatch")
            if opt_out[1] != [int(v != 0) for v in expected]:
                raise AssertionError("lane flags mismatch")
            if sum(resident.ops.values()) != 154 or sum(resident.loads.values()) != 31:
                raise AssertionError("resident-32 schedule count mismatch")
            if sum(full_res.ops.values()) != 151 or sum(full_res.loads.values()) != 2:
                raise AssertionError("full-resident-64 schedule count mismatch")
            peak32 = max(peak32, resident.registers())
            peak64 = max(peak64, full_res.registers())
            if peak32 > 32 or peak64 > 56:
                raise AssertionError("register budget exceeded")
            checked += LANES
            early_passes += expected.count(0)
            for y4 in members:
                words_t, x1_t, x5_t, y12_t = trial(X, S, w, alpha, y4, pre)
                if (residual_word1(X, words_t, alpha, x1_t, x5_t, y4, y12_t) & 0xF) == 0:
                    low4_hits += 1
        words, _, _, _ = trial(X, S, w, alpha, class_member(stream[11 + index] % CLASS_SIZE), pre)
        last_pair = messages(words)
    if len(s5_values) != 1:
        raise AssertionError("S5 must remain fixed across shared-seed contexts")
    return last_pair + ({"audited_lanes": checked, "early_test_passes": early_passes,
                         "residual_low4_hits": low4_hits, "s5_shared_fixed": 1,
                         "full_resident_operations": 151, "full_resident_loads": 2,
                         "full_preload_operations": 42, "register_upper_bound_64": peak64,
                         "resident32_operations": 154, "resident32_loads": 31,
                         "register_upper_bound_32": peak32, "shared_contexts": 4},)


def flags_right():
    """lane_flags on all 128 patterns of zero and nonzero lanes; random cases hardly ever have a zero lane."""
    c = {"M": rep(MASK), "bit 32": ONES << 32}
    right = 0
    for pattern in range(1 << LANES):
        words = [0 if pattern >> i & 1 else (MASK, 1, 0x80000000)[i % 3] for i in range(LANES)]
        m = Machine()
        m.at("early test")
        flags, taken = lane_flags(m, c, m.load(sum(v << (LANE_BITS * i) for i, v in enumerate(words))))
        right += int(flags == [int(v != 0) for v in words] and taken == (pattern != 0))
    return right


def selftest(cases, seed):
    """Run packed batches on contexts derived from the seed text, print one JSON line, return the exit status."""
    shape, same, equal, zero, last, extreme, sums = None, True, 0, 0, 0, 0, {}
    for case in range(cases):
        text = "halfsearch selftest %s %d" % (seed, case)
        stream = struct.unpack("<12I", hashlib.shake_256(text.encode("utf-8")).digest(48))
        nine, alpha, j = list(stream[:9]), stream[9], stream[10] % BATCHES
        if case % 4 == 0:                       # the last batch of the class: its one member in all seven lanes
            j, last = BATCHES - 1, last + 1
        if case % 5 == 4:                       # extreme words: each context word and alpha is 0, 2^32 - 1 or as drawn
            nine = [(0, MASK, v, v)[stream[11] >> 2 * i & 3] for i, v in enumerate(nine)]
            alpha, extreme = (0, MASK, alpha, alpha)[stream[11] >> 18 & 3], extreme + 1
        X, S, w = context(nine)
        machine = Machine()
        checked = batch_check(X, S, w, alpha, j, machine)
        equal, zero = equal + checked[2], zero + checked[3]
        found = (tuple((part, machine.ops[part], machine.loads[part]) for part in machine.ops), machine.registers(),
                 batch_constants(X, S, w, alpha)[1:])
        shape = shape or found
        same = same and found == shape
        for part, top in machine.sums.items():
            sums[part] = max(sums.get(part, 0), top)
    table, registers, (per_context, for_alpha) = shape
    bounds = {row[0]: row[3] for row in TABLE}
    parts, below = {}, True
    for part, operations, loads in table:
        parts[part] = {"operations": operations, "loads": loads}
        if bounds.get(part) is not None:                # largest sum in units of 2^32, rounded down
            parts[part].update(largest_sum=(sums[part] * 1000 >> 32) / 1000, bound=bounds[part])
            below = below and sums[part] < bounds[part] << 32
    largest = max(sums.values())
    members = {y for j in range(BATCHES) for y in list_words(j)[2]}
    flags = flags_right()
    report = {
        "selftest": "packed batch of proof.md Section 6.5",
        "seed": seed, "cases": cases, "last_batches": last, "extreme_cases": extreme,
        "lanes_checked": cases * LANES, "lanes_equal": equal, "zero_test_words": zero,
        "parts": parts,
        "operations": sum(row[1] for row in table), "loads": sum(row[2] for row in table),
        "same_counts_in_every_case": same, "counts_equal_table": table == tuple(row[:3] for row in TABLE),
        "largest_lane": largest, "largest_lane_bits": largest.bit_length(), "lane_bits": LANE_BITS,
        "sums_below_bounds": below,
        "registers": registers, "register_limit": REGISTERS,
        "per_context_constants": per_context, "per_alpha_constants": for_alpha,
        "list_words": BATCHES, "members_in_lists": len(members),
        "zero_lane_patterns": 1 << LANES, "zero_lane_patterns_right": flags,
    }
    json.dump(report, sys.stdout, separators=(",", ":"))
    sys.stdout.write("\n")
    good = (equal == cases * LANES and same and report["counts_equal_table"] and below and registers <= REGISTERS
            and len(members) == CLASS_SIZE and flags == 1 << LANES)
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
