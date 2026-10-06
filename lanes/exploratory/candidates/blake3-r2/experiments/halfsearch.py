"""Half-collisions of 2-round BLAKE3 and a small residual search.

Implements the constructions of proof.md for blake3-r2-prefix-v1. The
organizer request is read from stdin and one message pair is returned per
trial: a 60-byte message A and a 62-byte message B. Only the standard library
is used; there is no OS randomness, wall time or ambient state. The program
never calls BLAKE3 or any implementation of the target: it evaluates the
quarter-round G directly, and the organizer runner recomputes both complete
digests. SHAKE-256 from the standard library is used only to expand the
organizer's seed into the trial's parameters.

Experiment "half-collision": steps S1-S3 of proof.md Section 4 for nine state
words taken from the seed. The proof predicts that digest words 0, 2, 5, 7 of
A and B are equal for every seed.

Experiment "residual-search": the search of proof.md Section 6 at toy scale.
For one context and one alpha taken from the seed it tries gamma = g0, g0+1,
... (at most LIMIT values) and returns the first pair whose residual has a zero
low byte in digest word 1, so that 136 digest bits agree. The number of
values tried is reported as an untrusted observation. For the same context
and alpha one packed batch of proof.md Section 6.5 (the seven trials g0, ..,
g0+6) is also evaluated on a machine that counts operations and loads. Its
two counts and the number of lanes equal to the scalar early-test word of
Lemma E are reported as untrusted observations. That batch is not part of
the search and has no influence on the returned pair.

Self-test of the operation count (not an organizer mode):

    python3 experiments/halfsearch.py --selftest N [seed]

runs N packed batches on contexts derived from the seed text (default 1);
every fourth one is the final batch of a gamma loop. It prints one JSON line:
cases, lanes checked, lanes equal to the scalar word, operations and loads
per part and in total, and the largest lane value seen. The exit status is 0
when every lane is equal and the counts are those of the table in 6.5.
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
FREE = (1, 2, 5, 6, 9, 10, 12, 13, 14)
LIMIT = 8192
# The packed word of proof.md Section 6.5: seven lanes of 36 bits in one 256-bit word.
LANES, LANE_BITS = 7, 36
LANE = (1 << LANE_BITS) - 1
WORD = (1 << 256) - 1
ONES = sum(1 << (LANE_BITS * i) for i in range(LANES))
# First gamma of the final batch of a gamma loop (2^32 = 7 * 613566756 + 4).
LAST_GAMMA = (1 << 32) - 4
# (part, operations, loads) of one batch of seven trials: the table of proof.md Section 6.5.
TABLE = (("loop", 1, 1), ("D1 family", 28, 15), ("C0", 27, 12), ("C1", 25, 12), ("C2", 29, 12),
         ("E1, A and B", 26, 11), ("E3, A and B", 28, 10), ("early test", 14, 6))


def ror(v, n):
    return ((v >> n) | (v << (32 - n))) & MASK


def rol(v, n):
    return ((v << n) | (v >> (32 - n))) & MASK


def g(a, b, c, d, x, y):
    a = (a + b + x) & MASK; d = ror(d ^ a, 16); c = (c + d) & MASK; b = ror(b ^ c, 12)
    a = (a + b + y) & MASK; d = ror(d ^ a, 8); c = (c + d) & MASK; b = ror(b ^ c, 7)
    return a, b, c, d


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
    """Steps S1-S3: message words w, state X after round 0, state S after its column step."""
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
    other = list(w)
    other[4] = W4B
    other[5] = (w[5] + DELTA5) & MASK
    return struct.pack("<16I", *w)[:LEN_A], struct.pack("<16I", *other)[:LEN_B]


def d0_family(S, alpha):
    """Words (w8, w9) of D0 giving c output alpha and d output X15: returns X0, X5, w8, w9."""
    c1 = (alpha - X15) & MASK
    d1 = (c1 - S[10]) & MASK
    x0 = rol(X15, 8) ^ d1
    b1 = ror(S[5] ^ c1, 12)
    a1 = rol(d1, 16) ^ S[15]
    return x0, ror(b1 ^ alpha, 7), (a1 - S[0] - S[5]) & MASK, (x0 - a1 - b1) & MASK


def d1_family(S, gamma):
    """Words (w10, w11) of D1 with first-half c value gamma and c output X11: returns X1, X6, X12, w10, w11."""
    x12 = (X11 - gamma) & MASK
    d1 = (gamma - S[11]) & MASK
    x1 = rol(x12, 8) ^ d1
    b1 = ror(S[6] ^ gamma, 12)
    a1 = rol(d1, 16) ^ S[12]
    return x1, ror(b1 ^ X11, 7), x12, (a1 - S[1] - S[6]) & MASK, (x1 - a1 - b1) & MASK


def residual_word1(X, w, x0, x5, alpha, w8, x1, x6, x12, w10, pinned):
    """Digest word 1 of A xor digest word 1 of B for one trial (round 1, partial)."""
    y3, y3b, y11, y11b = pinned
    c0 = g(x0, X[4], X[8], x12, w[2], w[6])
    c1 = g(x1, x5, X[9], X[13], w[3], w10)
    c2 = g(X[2], x6, alpha, X[14], w[7], w[0])
    y4, y12, y1, y9, y6, y14 = c0[1], c0[3], c1[0], c1[2], c2[1], c2[3]
    w5b = (w[5] + DELTA5) & MASK
    pa = g(y1, y6, y11, y12, w[12], w[5])
    pb = g(y1, y6, y11b, y12, w[12], w5b)
    qa = g(y3, y4, y9, y14, w[15], w8)
    qb = g(y3b, y4, y9, y14, w[15], w8)
    return pa[0] ^ qa[2] ^ pb[0] ^ qb[2]


def rep(v):
    """The 32-bit value v in every lane of a packed word."""
    return (v & MASK) * ONES


class Machine:
    """The counting packed-word machine of proof.md Section 6.5.

    A packed word is one integer of seven 36-bit lanes. Every addition, XOR,
    AND, OR and shift of packed words is one operation, the final comparison
    and the branch are one each, and every constant operand is fetched with
    load() and is one load. Both counts are kept per part of the batch.
    largest is the largest lane value of any sum or XOR formed.
    """

    def __init__(self):
        self.ops, self.loads, self.part, self.largest = {}, {}, None, 0

    def at(self, part):
        self.part = part
        self.ops[part] = self.loads[part] = 0

    def load(self, constant):
        self.loads[self.part] += 1
        return constant

    def op(self, z, lanes=False):
        self.ops[self.part] += 1
        if lanes:
            self.largest = max(self.largest, max((z >> (LANE_BITS * i)) & LANE for i in range(LANES)))
        return z

    def add(self, x, y):
        return self.op(x + y, True)

    def xor(self, x, y):
        return self.op(x ^ y, True)

    def band(self, x, y):
        return self.op(x & y)

    def bor(self, x, y):
        return self.op(x | y)

    def shr(self, x, r):
        return self.op(x >> r)

    def shl(self, x, r):
        return self.op((x << r) & WORD)

    def pror(self, z, r):
        """Rotate every lane right by r: ((z >> r) AND A_r) OR ((z << (32-r)) AND B_r)."""
        low = self.band(self.shr(z, r), self.load(rep((1 << (32 - r)) - 1)))
        high = self.band(self.shl(z, 32 - r), self.load(rep(((1 << r) - 1) << (32 - r))))
        return self.bor(low, high)

    def prol(self, z, r):
        return self.pror(z, 32 - r)

    def compare_and_branch(self, x, y):
        """The final comparison of two packed words and the branch on it: two operations."""
        self.ops[self.part] += 2
        return x != y


def scalar_early(X, S, w, alpha, gamma, pinned):
    """The test word (f1 XOR f1') XOR t XOR ROR(t, 1) of Lemma E for one trial, in 32-bit arithmetic."""
    y3, y3b, y11, y11b = pinned
    x0, x5, _, _ = d0_family(S, alpha)
    x1, x6, x12, w10, _ = d1_family(S, gamma)
    c0 = g(x0, X[4], X[8], x12, w[2], w[6])
    c1 = g(x1, x5, X[9], X[13], w[3], w10)
    c2 = g(X[2], x6, alpha, X[14], w[7], w[0])
    y4, y12, y1, y9, y6, y14 = c0[1], c0[3], c1[0], c1[2], c2[1], c2[3]
    a1 = (y1 + y6 + w[12]) & MASK
    d1 = ror(y12 ^ a1, 16)
    b1, b1b = ror(y6 ^ ((y11 + d1) & MASK), 12), ror(y6 ^ ((y11b + d1) & MASK), 12)
    t = ((a1 + b1 + w[5]) & MASK) ^ ((a1 + b1b + w[5] + DELTA5) & MASK)
    e1, e1b = (y3 + y4) & MASK, (y3b + y4) & MASK
    f1 = ror(y4 ^ ((y9 + ror(y14 ^ e1, 16)) & MASK), 12)
    f1b = ror(y4 ^ ((y9 + ror(y14 ^ e1b, 16)) & MASK), 12)
    return f1 ^ f1b ^ t ^ ror(t, 1)


def packed_batch(m, X, S, w, alpha, gamma0, pinned):
    """The early test of Lemma E for the trials gamma0, .., gamma0+6 in one packed word, counted on m.

    Lane i holds gamma0 + i without reduction, as the gamma register of the
    algorithm does, and stands for the trial gamma = gamma0 + i mod 2^32.
    Returns the seven reduced test words and the seven flags (1 where the
    test word is nonzero). The parts and their order are those of TABLE.
    """
    y3, y3b, y11, y11b = pinned
    x0, x5, _, _ = d0_family(S, alpha)
    a1c0 = (x0 + X[4] + w[2]) & MASK                                  # a1 of C0, a per-alpha constant
    M = rep(MASK)
    gam = sum((gamma0 + i) << (LANE_BITS * i) for i in range(LANES))

    m.at("loop")                                                      # the gamma register of the next batch
    m.add(gam, m.load(rep(7)))
    m.at("D1 family")
    x12 = m.add(m.xor(gam, m.load(M)), m.load(rep(X11 + 1)))          # X11 - gamma
    d = m.add(gam, m.load(rep(-S[11])))
    x1 = m.xor(m.prol(x12, 8), d)
    b = m.pror(m.xor(gam, m.load(rep(S[6]))), 12)
    x6 = m.pror(m.xor(b, m.load(rep(X11))), 7)
    a = m.xor(m.prol(d, 16), m.load(rep(S[12])))
    w10 = m.add(a, m.load(rep(-S[1] - S[6])))
    m.at("C0")
    pd1 = m.pror(m.xor(x12, m.load(rep(a1c0))), 16)
    pc1 = m.add(pd1, m.load(rep(X[8])))
    pb1 = m.pror(m.xor(pc1, m.load(rep(X[4]))), 12)
    pa2 = m.add(pb1, m.load(rep(a1c0 + w[6])))
    y12 = m.pror(m.xor(pa2, pd1), 8)
    pc2 = m.add(pc1, y12)
    y4 = m.pror(m.xor(pc2, pb1), 7)
    m.at("C1")
    qa1 = m.add(x1, m.load(rep(x5 + w[3])))
    qd1 = m.pror(m.xor(qa1, m.load(rep(X[13]))), 16)
    qc1 = m.add(qd1, m.load(rep(X[9])))
    qb1 = m.pror(m.xor(qc1, m.load(rep(x5))), 12)
    qa2 = m.add(m.add(qa1, qb1), w10)
    qd2 = m.pror(m.xor(qa2, qd1), 8)
    qc2 = m.add(qc1, qd2)
    y1 = m.band(qa2, m.load(M))                                       # reduce Y1
    y9 = m.band(qc2, m.load(M))                                       # reduce Y9
    m.at("C2")
    ra1 = m.add(x6, m.load(rep(X[2] + w[7])))
    rd1 = m.pror(m.xor(ra1, m.load(rep(X[14]))), 16)
    rc1 = m.add(rd1, m.load(rep(alpha)))
    rb1 = m.pror(m.xor(rc1, x6), 12)
    ra2 = m.add(m.add(ra1, rb1), m.load(rep(w[0])))
    y14 = m.pror(m.xor(ra2, rd1), 8)
    rc2 = m.add(rc1, y14)
    y6 = m.pror(m.xor(rc2, rb1), 7)
    m.at("E1, A and B")
    ea1 = m.add(m.add(y1, y6), m.load(rep(w[12])))
    ed1 = m.pror(m.xor(ea1, y12), 16)
    ec1 = m.add(ed1, m.load(rep(y11)))
    ec1b = m.add(ed1, m.load(rep(y11b)))
    eb1 = m.pror(m.xor(ec1, y6), 12)
    eb1b = m.pror(m.xor(ec1b, y6), 12)
    ea2 = m.add(m.add(ea1, eb1), m.load(rep(w[5])))
    ea2b = m.add(m.add(ea1, eb1b), m.load(rep(w[5] + DELTA5)))
    m.at("E3, A and B")
    e1 = m.add(y4, m.load(rep(y3)))
    e1b = m.add(y4, m.load(rep(y3b)))
    h1 = m.pror(m.xor(y14, e1), 16)
    h1b = m.pror(m.xor(y14, e1b), 16)
    g1 = m.add(y9, h1)
    g1b = m.add(y9, h1b)
    f1 = m.pror(m.xor(y4, g1), 12)
    f1b = m.pror(m.xor(y4, g1b), 12)
    m.at("early test")
    t = m.xor(ea2, ea2b)
    word = m.xor(m.xor(m.xor(f1, f1b), t), m.pror(t, 1))
    word = m.band(word, m.load(M))                                    # reduce the test word
    flags = m.band(m.add(word, m.load(M)), m.load(ONES << 32))        # bit 32 of a lane: its word is nonzero
    m.compare_and_branch(flags, m.load(ONES << 32))                   # taken when a lane has a zero word
    return ([(word >> (LANE_BITS * i)) & LANE for i in range(LANES)],
            [(flags >> (LANE_BITS * i + 32)) & 1 for i in range(LANES)])


def batch_check(X, S, w, alpha, gamma0, pinned, machine=None):
    """One packed batch for a context, an alpha and the seven trials from gamma0, on a new machine unless one is given.

    Returns (operations, loads, lanes equal to the scalar early-test word, bit
    length of the largest lane value). A lane is equal when its reduced test
    word is the scalar word and its flag tells whether that word is nonzero.
    """
    m = Machine() if machine is None else machine
    words, flags = packed_batch(m, X, S, w, alpha, gamma0, pinned)
    equal = 0
    for i in range(LANES):
        early = scalar_early(X, S, w, alpha, (gamma0 + i) & MASK, pinned)
        equal += int(words[i] == early and flags[i] == int(early != 0))
    return sum(m.ops.values()), sum(m.loads.values()), equal, m.largest.bit_length()


def half_collision(seed):
    free = struct.unpack("<9I", hashlib.shake_256(seed).digest(36))
    _, _, w = context(free)
    return messages(w) + ({},)


def residual_search(seed):
    stream = struct.unpack("<11I", hashlib.shake_256(seed).digest(44))
    X, S, w = context(stream[:9])
    alpha, gamma0 = stream[9], stream[10]
    ca = g(X3, X7, X11, X15, W4, W13)
    cb = g(X3, X7, X11, X15, W4B, W13)
    pinned = (ca[0], cb[0], ca[2], cb[2])
    operations, loads, equal, _ = batch_check(X, S, w, alpha, gamma0, pinned)
    counted = {"batch_operations": operations, "batch_loads": loads, "batch_lanes_equal": equal}
    x0, x5, w8, w9 = d0_family(S, alpha)
    for step in range(LIMIT):
        x1, x6, x12, w10, w11 = d1_family(S, (gamma0 + step) & MASK)
        if residual_word1(X, w, x0, x5, alpha, w8, x1, x6, x12, w10, pinned) & 0xFF == 0:
            words = list(w)
            words[8], words[9], words[10], words[11] = w8, w9, w10, w11
            return messages(words) + (dict(counted, tries=step + 1),)
    return None, None, dict(counted, tries=LIMIT)


def selftest(cases, seed):
    """Run packed batches on contexts derived from the seed text, print one JSON line, return the exit status."""
    ca = g(X3, X7, X11, X15, W4, W13)
    cb = g(X3, X7, X11, X15, W4B, W13)
    pinned = (ca[0], cb[0], ca[2], cb[2])
    counts, same, equal, largest, final = None, True, 0, 0, 0
    for case in range(cases):
        text = "halfsearch selftest %s %d" % (seed, case)
        stream = struct.unpack("<11I", hashlib.shake_256(text.encode("utf-8")).digest(44))
        X, S, w = context(stream[:9])
        last = case % 4 == 0                    # the final batch of a gamma loop: the three top lanes reach 2^32
        final += int(last)
        machine = Machine()
        _, _, lanes_equal, bits = batch_check(X, S, w, stream[9], LAST_GAMMA if last else stream[10], pinned, machine)
        table = tuple((part, machine.ops[part], machine.loads[part]) for part in machine.ops)
        counts = counts or table
        same = same and table == counts
        equal += lanes_equal
        largest = max(largest, bits)
    report = {
        "selftest": "packed batch of proof.md Section 6.5",
        "seed": seed, "cases": cases, "final_batches": final,
        "lanes_checked": cases * LANES, "lanes_equal": equal,
        "parts": {part: {"operations": ops, "loads": loads} for part, ops, loads in counts},
        "operations": sum(row[1] for row in counts), "loads": sum(row[2] for row in counts),
        "same_counts_in_every_case": same, "counts_equal_table": counts == TABLE,
        "largest_lane_bits": largest, "lane_bits": LANE_BITS,
    }
    json.dump(report, sys.stdout, separators=(",", ":"))
    sys.stdout.write("\n")
    return 0 if equal == cases * LANES and same and counts == TABLE else 1


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
    for trial in request["trials"]:
        first, second, observations = run(bytes.fromhex(trial["seed"]))
        row = {"trial": trial["trial"],
               "message_a_hex": None if first is None else first.hex(),
               "message_b_hex": None if second is None else second.hex()}
        if observations:
            row["observations"] = observations
        trials.append(row)
    json.dump({"schema_version": 1, "trials": trials}, sys.stdout, separators=(",", ":"), sort_keys=True)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
