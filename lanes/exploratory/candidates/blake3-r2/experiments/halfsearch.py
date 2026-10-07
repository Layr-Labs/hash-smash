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

Both experiments use the trial of proof.md Section 6.1. It has three parts,
one for each loop of the search. The outer step takes six words: the second
and third value of the round-1 call C0, the second value of the round-0 call
D3, the state words S15 and S9 and the message word w5. The middle step
takes the state word X2. The seven words together are a context. The inner
loop takes one member of the sub-class of proof.md Section 6.1: the values
of Y4 for which the first-half d difference of round-1 call E3 is the word
ETA below (the class of Lemma Q) and for which the bits of e1 = Y3 + Y4
named in CUBE have the values given there; CLASS_SIZE values in all. In
every trial w14 = 0, w15 = 0 and the top byte of w13 is zero, so that the 63
bytes of B end in eight zero bytes.

Experiment "half-collision": one trial per seed. The proof predicts that
digest words 0, 2, 5, 7 of A and B are equal for every seed.

Experiment "residual-search": the search of proof.md Section 6 at toy scale.
For one context taken from the seed it tries the class members k0, k0+1, ...
(all members of the class at most) and returns the first pair whose residual
has a zero low byte in digest word 1, so that 136 digest bits agree. The
number of members tried is reported as an untrusted observation. For the
same context the work of the three loops is also evaluated on a machine that
counts operations, loads and stores: the outer step, the words of the table
of the outer step for the seven members of one batch (the batch that holds
member k0), the middle step, and the packed two-stage batch of proof.md
Section 6.5 for these seven members. Both stages of the batch are evaluated,
whether or not stage A passes. The operations and loads of each stage,
whether a lane passes stage A, and the number of lanes that are right are
reported as untrusted observations. A lane is right when the words of its
message A are those of the trial, its stage-A flag says whether the trial
satisfies rule A, with h1 taken from the compression of the lane's own
message A, and its stage-2 word and flag equal the test word of Lemma N,
computed from the compressions of the lane's two messages and again from
their two complete digests. No lane counts as right unless every word that
the counted outer step, table and middle step have stored is the word of
the context. That batch is not part of the search and has no influence on
the returned pair.

Self-test of the operation count (not an organizer mode):

    python3 experiments/halfsearch.py --selftest N [seed]

runs N cases on contexts and list positions derived from the seed text
(default 1); a case is one outer step, one word of each list of the table,
one middle step and one packed batch. Every fourth case is the last batch of
the class, and in every fifth each context word is 0, 2^32 - 1 or as drawn.
It prints one JSON line: cases, lanes checked and lanes right (as above,
each lane against the complete digests of its two messages), the cases in
which all stored words are right, the lanes that pass rule A and the batches
in which one does, operations and loads per part and per stage of the batch,
operations, loads and stores per part of the three other pieces, the largest
lane of a sum per part and overall, the largest number of registers in use
at one time per piece, the number of words that the outer step and the
middle step store, the number of class members in the list, for how many of
the 128 patterns of zero and nonzero lanes the flags are right, and for how
many packed words the stage-A flags are right when every pattern of the bits
of z that rule A reads, together with every pattern of the free bits of e1
that it reads, occurs once in every lane (a random case hardly ever has a
zero stage-2 word). The exit status is 0 when every lane is
right, the counts are those of TABLES below in every case, every sum is
below the bound of its part, the registers in use are at most REGISTERS in
each of the four pieces, the words that a batch finds in registers are
there again at its end, the list holds all members of the class and all
patterns are right. The JSON line also has the number of words kept in
registers during a class loop, the number of them that stage 2 loads again,
and per part the reads of a kept word, which are not loads.
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
# The class of proof.md Section 6.1, and the sub-class that the search uses: the members of the class whose
# e1 = Y3 + Y4 has, at the bits of the first word of CUBE, the bits of the second word.
ETA = 0x830303CF
CUBE = (0x04200000, 0x00000000)
# Rule A of proof.md Section 6.3 for this sub-class: for every pair (mask, value), the XOR of the bits of h1 in mask
# is value. Three rules are written out, with four, six and eight conditions; each contains the one before it.
# RULE_CONDITIONS is the one place that says which of them the batch uses.
RULES = {4: ((0x00000001, 0), (0x00000002, 1), (0x00010000, 0), (0x00020000, 0))}
RULES[6] = RULES[4] + ((0x00000404, 1), (0x00000808, 1))
RULES[8] = RULES[6] + ((0x01001008, 0), (0x02002040, 0))
RULE_CONDITIONS = 8
RULE_A = RULES[RULE_CONDITIONS]
# How stage A forms its test word y from z (Lemma A), per rule: the steps, and ALL, the positions of y that it
# reads. A step (d, mask) is s = (y shifted by d) AND mask, y = y XOR s; a step d alone is s = s shifted by d,
# y = y XOR s. A shift is to the left for d > 0 and to the right for d < 0. rule_a_constants() derives from these
# steps what every read position holds and stops unless the test is the rule.
A_PLANS = {4: ((), 0x03000300), 6: (((24, 0x0C000000),), 0x0F000300),
           8: (((12, 0x0003C000), 12, (13, 0x40010000)), 0x4F010300)}
A_STEPS, A_ALL = A_PLANS[RULE_CONDITIONS]
# The seven words of a context, in the order in which context() takes them: the six words of an outer step, then
# the word of the middle loop.
CONTEXT_WORDS = ("C0.c1", "C0.d1", "D3.d1", "S15", "S9", "w5", "X2")


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
# The first four values of the round-0 call K2 = G(2,6,10,14; w4, w5) with input (IV2, IV6, IV2, 55): constants.
K2A = (K + W4) & MASK
K2D = ror(K2A ^ LEN_A, 16)
K2C = (IV[2] + K2D) & MASK
K2B = ror(IV[6] ^ K2C, 12)


def class_pattern():
    """Lemma Q and the sub-class: the bits of e1 = Y3 + Y4 that eta or CUBE fixes (mask, value), the free positions."""
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
# The packed word of proof.md Section 6.5: seven lanes of 36 bits in one 256-bit word.
LANES, LANE_BITS = 7, 36
# The machine of proof.md Section 6.5: its number of registers, and how many of the memory words that a batch reads
# are kept in registers during a class loop (a number; 0: every memory word that an operation reads is fetched
# where it is read; None: all of them). These two lines are the machine convention of this file.
REGISTERS = 16
KEPT = 9
LANE = (1 << LANE_BITS) - 1
WORD = (1 << 256) - 1
ONES = sum(1 << (LANE_BITS * i) for i in range(LANES))
BATCHES = (CLASS_SIZE + LANES - 1) // LANES


def rule_a(h1):
    """Rule A on the word h1, the first-half d value of E3 on message A."""
    return all(bin(h1 & mask).count("1") & 1 == value for mask, value in RULE_A)


def rule_a_constants():
    """Lemma A: rule A as a test on z, the XOR of the fifth and the second value of C2, for this sub-class.

    Bit i of h1 is bit (i + 24) mod 32 of z XOR bit (i + 16) mod 32 of e1. So a condition of the rule, "the XOR of
    the bits of h1 in mask is value", reads: the XOR of the bits of z in ROL(mask, 24) is value XOR the XOR of the
    bits of e1 in ROL(mask, 16). The right side is known for every member: e1 = Y3 + Y4. The steps A_STEPS make a
    word y from z by shifts, ANDs with fixed masks and XORs alone, so every bit of y is the XOR of a set of bits of
    z of the same lane or of a neighbouring lane. This function follows the steps on five lanes of names of bits
    and stops unless, for every position t of A_ALL, the set at t has only bits 0 to 31 of the lane itself and is
    the XOR of the sets of some of the conditions (the conditions of t), and unless there are as many positions as
    conditions and the positions are independent as combinations of the conditions. Then "for every t, bit t of y
    is the XOR, over the conditions of t, of their right sides" holds exactly when every condition holds. Returns
    the masks of the steps and, for every t, (t, c, m): the wanted bit at t is c XOR the XOR of the bits of e1 in
    m. rule_word() puts a 1 at t where the wanted bit is 0; with that word v, a trial satisfies rule A exactly
    when ((y XOR v) AND ALL) == ALL.
    """
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
# The bits of e1 that the wanted bits depend on and that the sub-class leaves free.
A_FREE = tuple(i for i in CLASS_FREE if any(m >> i & 1 for _, _, m in A_FLIP))


def rule_word(y4):
    """The lane of the list V for class member y4 (Lemma A): a 1 at every read position whose wanted bit is 0."""
    e1 = (Y3 + y4) & MASK
    return sum((1 ^ c ^ bin(e1 & m).count("1") & 1) << t for t, c, m in A_FLIP)


# The memory words that a batch reads, the table words and the word of the list V apart: masks, fixed words, the
# two bounds of the loop, and the words that the outer step and the middle step have stored. With KEPT a number,
# the first KEPT of them are RESIDENT: the class loop entry loads each into a register, and it stays there for all
# batches of the value of X2. They are the masks of the rotations by 16 and by 12, the masks of the steps of rule
# A and the words that stage A must find in a register so that five registers are enough for its values. Stage 2
# gives up the registers of the words EVICT and loads these words again at its end. With RC_AGAIN stage A does not
# keep the third value of C2 and stage 2 forms it again; with Z_AGAIN the first step of rule A takes the register
# of z, and stage 2 forms z again.
BATCH_WORDS = (["A16", "B16", "A12", "B12"] + ["A mask %d" % (n + 1) for n in range(len(A_MASKS))]
               + ["A all", "A carry", "not bit 32", "X2+w7", "w0",
                  "end of list", "-w2", "ROL(X15,8)", "S10+X15", "X14", "stage-2 budget", "A8", "B8", "A7", "B7",
                  "-X15", "S5", "w3", "X13", "X9", "S12", "w12-S1-S6", "Y11", "Y11'", "w5", "w5+delta", "A31",
                  "eta", "M", "bit 32"])
RESIDENT = tuple(BATCH_WORDS if KEPT is None else BATCH_WORDS[:KEPT])
EVICT = () if KEPT is None else RESIDENT[5:]
RC_AGAIN = bool(KEPT)
Z_AGAIN = bool(KEPT and A_STEPS)
# (part, operations, loads, stores, bound) of the four counted pieces: the tables of proof.md Section 6.5 and, in
# units of 2^32, the bound that Section 6.5 gives for the sums of the part. The outer step is run once for the six
# words of an outer step. The table build is run once per outer step for every word of the list, and stores one
# word of each of the five lists of the table. The middle step is run once per value of X2; its last part loads
# the words RESIDENT into registers. The batch is run once per value of X2 for every word of the list, that is for
# seven trials. Its first STAGE_A_PARTS parts are stage A, which every batch runs; the others are stage 2, which a
# batch runs only when one of its lanes passes rule A. The part "rule A" has three operations for every step of
# A_STEPS with a mask, two for every other step and six more, and one load, the word of the list V. The masks of
# the steps take the places of X2 + w7 and w0 among the nine words RESIDENT; stage A then loads these where it
# reads them. Forming z again costs stage 2 four operations and three loads.
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
# The budget of proof.md 6.4 step 4 on the batches that enter stage 2: a share 2^-STAGE_2_LOG2_SHARE of the batches
# of a run, one half, one eighth or one part in 32 for the rule with four, six or eight conditions. A run has
# 2^127 / FACTOR trials, FACTOR being the factor that proof.md Section 7 assumes for the rate: that is RUN_PAIRS
# pairs of an outer step and a value of X2, with BATCHES batches each. With the clusters of proof.md 6.7 the
# algorithm runs stage A on a representative always and on the 63 neighbours of a cluster only when the
# representative passes the gate, so it FINDS only part of the trials of a run that satisfy rule A: EQUIVALENTS of
# the 64 trials of a cluster, per representative, as proof.md 6.7 and Section 7 state. A run is lengthened by
# 64 / EQUIVALENTS so that the trials it finds are the 2^127 / FACTOR that Section 7 needs.
FACTOR = 92675904
EQUIVALENTS = 4102                 # 41.02 per representative, in hundredths; measured, proof.md Section 10
RUN_PAIRS_EQUIVALENT = -(-(1 << 127) // (FACTOR * CLASS_SIZE))   # the pairs whose equivalents the charge is per
RUN_PAIRS = -(-RUN_PAIRS_EQUIVALENT * 6400 // EQUIVALENTS)       # the pairs the run walks to find them
STAGE_2_LOG2_SHARE = len(RULE_A) - 3
STAGE_2_BUDGET = BATCHES * RUN_PAIRS >> STAGE_2_LOG2_SHARE


def class_member(k):
    """Y4 of class member number k: the bits of k fill the free positions of e1 in increasing order."""
    e1 = CLASS_VALUE
    for j, i in enumerate(CLASS_FREE):
        e1 |= (k >> j & 1) << i
    return (e1 - Y3) & MASK


def outer(six):
    """Step S1, first part: the lines that read neither X2 nor the member, for the six words of an outer step.

    Returns every value by its name: S for the state after the column step of round 0, X for the state after
    round 0, K0..K3 and D0..D3 for the calls of round 0 and C0 for the round-1 call G(0,4,8,12; w2, w6), with a1,
    d1, c1, b1 for the first four values of a call.
    """
    c0c, c0d, d3d, s15, s9, w5 = six
    v = {"C0.c1": c0c, "C0.d1": c0d, "D3.d1": d3d, "S15": s15, "S9": s9, "w5": w5}
    # K2 = G(2,6,10,14; w4, w5) with input (IV2, IV6, IV2, 55), forwards
    v["S2"] = (K2A + K2B + w5) & MASK
    v["S14"] = ror(K2D ^ v["S2"], 8)
    v["S10"] = (K2C + v["S14"]) & MASK
    v["S6"] = ror(K2B ^ v["S10"], 7)
    # D3 = G(3,4,9,14; w14, w15) with w14 = w15 = 0: from its second value, its inputs S9, S14 and its output X3
    v["D3.a1"] = rol(d3d, 16) ^ v["S14"]
    v["D3.c1"] = (s9 + d3d) & MASK
    v["D3.b1"] = (X3 - v["D3.a1"]) & MASK
    v["S4"] = rol(v["D3.b1"], 12) ^ v["D3.c1"]
    v["S3"] = (v["D3.a1"] - v["S4"]) & MASK
    v["X14"] = ror(d3d ^ X3, 8)
    v["X9"] = (v["D3.c1"] + v["X14"]) & MASK
    v["X4"] = ror(v["D3.b1"] ^ v["X9"], 7)
    # K3 = G(3,7,11,15; w6, w7) with input (IV3, IV7, IV3, 11) backwards from its outputs S3, S15
    v["K3.d1"] = rol(s15, 8) ^ v["S3"]
    v["K3.c1"] = (IV[3] + v["K3.d1"]) & MASK
    v["K3.b1"] = ror(IV[7] ^ v["K3.c1"], 12)
    v["S11"] = (v["K3.c1"] + s15) & MASK
    v["S7"] = ror(v["K3.b1"] ^ v["S11"], 7)
    v["K3.a1"] = rol(v["K3.d1"], 16) ^ 11
    v["w6"] = (v["K3.a1"] - IV[3] - IV[7]) & MASK
    v["w7"] = (v["S3"] - v["K3.a1"] - v["K3.b1"]) & MASK
    # C0: its fourth value; D2 = G(2,7,8,13; w12, w13) backwards from its outputs X7, X8 and its input S7
    v["C0.b1"] = ror(v["X4"] ^ c0c, 12)
    v["X8"] = (c0c - c0d) & MASK
    v["D2.b1"] = rol(X7, 7) ^ v["X8"]
    v["D2.c1"] = rol(v["D2.b1"], 12) ^ v["S7"]
    v["X13"] = (v["X8"] - v["D2.c1"]) & MASK
    return v


def middle(o, x2):
    """Step S1, second part: the lines that read X2, for the values o of an outer step. Returns o with them."""
    v = dict(o, X2=x2)
    # D2, rest
    v["D2.a1"] = (x2 - v["D2.b1"] - W13) & MASK
    v["D2.d1"] = rol(v["X13"], 8) ^ x2
    v["S13"] = rol(v["D2.d1"], 16) ^ v["D2.a1"]
    v["S8"] = (v["D2.c1"] - v["D2.d1"]) & MASK
    v["w12"] = (v["D2.a1"] - v["S2"] - v["S7"]) & MASK
    # K1 = G(1,5,9,13; w2, w3) with input (IV1, IV5, IV1, 0) backwards from its outputs S9, S13
    v["K1.c1"] = (v["S9"] - v["S13"]) & MASK
    v["K1.d1"] = (v["K1.c1"] - IV[1]) & MASK
    v["K1.a1"] = rol(v["K1.d1"], 16)
    v["K1.b1"] = ror(IV[5] ^ v["K1.c1"], 12)
    v["S1"] = rol(v["S13"], 8) ^ v["K1.d1"]
    v["S5"] = ror(v["K1.b1"] ^ v["S9"], 7)
    v["w2"] = (v["K1.a1"] - IV[1] - IV[5]) & MASK
    v["w3"] = (v["S1"] - v["K1.a1"] - v["K1.b1"]) & MASK
    # K0 = G(0,4,8,12; w0, w1) with input (IV0, IV4, IV0, 0) backwards from its outputs S4, S8
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
    """Step S1 for the seven words of CONTEXT_WORDS: every value of the two parts by its name."""
    return middle(outer(free[:6]), free[6])


def member(o, y4):
    """The lines that read the member and no word of the middle step: one row of the table of an outer step.

    C0 backwards from its b output y4, with its second, third and fourth value kept, then D1 = G(1,6,11,12; w10,
    w11) backwards from its outputs X11, X12 and its inputs S6, S11.
    """
    y12 = ((rol(y4, 7) ^ o["C0.b1"]) - o["C0.c1"]) & MASK
    a1 = ((rol(y12, 8) ^ o["C0.d1"]) - o["C0.b1"] - o["w6"]) & MASK
    x12 = rol(o["C0.d1"], 16) ^ a1
    c_d1 = (X11 - x12) & MASK
    b_d1 = ror(o["S6"] ^ c_d1, 12)
    d_d1 = (c_d1 - o["S11"]) & MASK
    return {"Y12": y12, "C0.a1": a1, "X12": x12, "D1.b1": b_d1, "X6": ror(b_d1 ^ X11, 7), "D1.d1": d_d1,
            "X1": rol(x12, 8) ^ d_d1}


def table_row(o, y4):
    """The five words that the table of an outer step holds for one member."""
    r = member(o, y4)
    return {"XA": (r["C0.a1"] - o["X4"]) & MASK, "X6": r["X6"], "X1": r["X1"], "R": rol(r["D1.d1"], 16), "Y12": r["Y12"]}


def messages(w):
    """Steps S2 and S3."""
    other = list(w)
    other[4] = W4B
    other[5] = (w[5] + DELTA5) & MASK
    return struct.pack("<16I", *w)[:LEN_A], struct.pack("<16I", *other)[:LEN_B]


def trial(v, y4):
    """The trial of proof.md 6.1 for the context v and class member y4: returns (words, values of the trial).

    The words are those of the context with w8..w11 added. Round 0 maps them to the context's state with
    X0, X1, X5, X6, X10, X12 as returned; C0 then has b output y4 and d output Y12.
    """
    r = member(v, y4)
    # D0 = G(0,5,10,15; w8, w9) backwards from its outputs X0, X15, with its input S kept
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
    """Digest word 1 of A xor digest word 1 of B for one trial (round 1, partial; proof.md 6.2)."""
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
    """The 32-bit value v in every lane of a packed word."""
    return (v & MASK) * ONES


def pack(values):
    """A packed word with the given 32-bit values in its lanes."""
    return sum((v & MASK) << (LANE_BITS * i) for i, v in enumerate(values))


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
    a comparison and a branch are one each, every word fetched from memory
    or from a list is one load, and every word written to memory or to a
    list is one store. The three counts are kept per part. A memory word
    that an operation reads is named with k(): it is fetched there, one
    load, unless it is kept in a register, and then the read is a use and
    no load. A word is kept from get(), which fetches it with one load, or
    from the class loop entry (resident()), up to drop(). sums holds, per
    part, the largest lane of any sum of packed words; it is taken lane by
    lane from the two operands, so a carry out of a lane cannot hide. Every
    value, a kept word too, records the step that made it and the step of
    its last use; registers() counts from these how many are held at one
    time.
    """

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
        """The memory word of that name as an operand: its register if it is kept in one, a load otherwise."""
        if name in self.kept:
            self.uses[self.part] += 1
            return self.kept[name]
        return self.load(self.memory[name])

    def get(self, *names):
        """Fetch memory words, one load each, and keep them in registers. Nothing is kept when KEPT is 0."""
        for name in names if KEPT != 0 else ():
            if name not in self.kept:
                self.kept[name] = self.load(self.memory[name])

    def drop(self, names):
        """The registers of these kept words are free from here on."""
        self.step += 1
        for name in names:
            if name in self.kept:
                self.kept.pop(name).last = self.step

    def resident(self, names):
        """The words that the class loop entry left in registers; their loads are counted there."""
        for name in names:
            self.kept[name] = self.value(self.memory[name])

    def finish(self, names=()):
        """The end of a piece. The kept words must be the words named, unchanged; they are held to the last step."""
        if set(self.kept) != set(names) or any(self.kept[name].z != self.memory[name] for name in names):
            raise ValueError("the words in registers at the end of a piece are not its kept words")
        self.step += 1
        for word in self.kept.values():
            word.last = self.step

    def store(self, x):
        """Write a register to memory: one store. Returns the stored word."""
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
        """Rotate every lane right by r: ((z >> r) AND A_r) OR ((z << (32-r)) AND B_r), the masks named Ar and Br."""
        low = self.band(self.shr(z, r), self.k("A%d" % r))
        high = self.band(self.shl(z, 32 - r), self.k("B%d" % r))
        return self.bor(low, high)

    def prol(self, z, r):
        return self.pror(z, 32 - r)

    def advance(self, position):
        """The next value of a counter (the list position, the stage-2 entries), in the counter's own register: one
        addition. The two counters have their registers for the whole search; registers() adds them."""
        self.ops[self.part] += 1
        self.step += 1
        return Packed(position + 1, self.step)

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
    """The packed words U[j] and V[j] of proof.md Section 6.5 and the seven class members they hold.

    Lane i holds member number 7 j + i; the spare lanes of the last word repeat the last member. The two lists are
    the same for the whole search. Only the table build reads U; stage A of a batch reads V (rule_word()).
    """
    members = [class_member(min(LANES * j + i, CLASS_SIZE - 1)) for i in range(LANES)]
    return pack(rol(y, 7) for y in members), members, pack(rule_word(y) for y in members)


# The memory cells that are the same for the whole search, by name; each holds its value in all seven lanes.
FIXED = {"M": MASK, "1": 1, "2": 2, "11": 11, "delta": DELTA5, "X3": X3, "X3+1": X3 + 1, "X15": X15, "-X15": -X15,
         "ROL(X15,8)": rol(X15, 8), "ROL(X7,7)": rol(X7, 7), "1-W13": 1 - W13, "X11": X11, "X11+1": X11 + 1,
         "K2.a1+K2.b1": K2A + K2B, "K2.d1": K2D, "K2.c1": K2C, "K2.b1": K2B, "IV3": IV[3], "IV7": IV[7],
         "-IV3-IV7": -IV[3] - IV[7], "-IV1": -IV[1], "IV1+IV5+1": IV[1] + IV[5] + 1, "IV5": IV[5], "IV4": IV[4],
         "-IV0": -IV[0], "-IV0-IV4": -IV[0] - IV[4], "Y11": Y11, "Y11'": Y11B, "eta": ETA,
         "A all": A_ALL, "A carry": -A_ALL, "w5 end": 0, "X2 end": 0}
FIXED.update(("A mask %d" % (n + 1), mask) for n, mask in enumerate(A_MASKS))
# The two masks of a rotation of every lane to the right by r: Ar selects the low 32 - r bits of a lane, Br the
# next r bits. The rotation to the left by one bit needs only A31.
for r in (7, 8, 12, 16, 20, 24, 25, 31):
    FIXED["A%d" % r], FIXED["B%d" % r] = (1 << (32 - r)) - 1, ((1 << r) - 1) << (32 - r)
del FIXED["B31"]


def memory(free):
    """The memory before the outer step of the context free.

    It holds the fixed cells and the seven words of the context, with w5 and X2 one below their values: the outer
    step and the middle step begin by adding one to their word. The cells "w5 end" and "X2 end" are compared with
    the two words by the end tests; no count depends on what they hold. "bit 32" has bit 32 of every lane and
    "not bit 32" every other bit of the seven lanes; the two bounds of the batch loop are plain numbers.
    """
    c = {name: rep(value) for name, value in FIXED.items()}
    c["bit 32"], c["not bit 32"] = ONES << 32, ONES * (LANE ^ 1 << 32)
    c["end of list"], c["stage-2 budget"] = BATCHES, STAGE_2_BUDGET
    c.update((name, rep(value)) for name, value in zip(CONTEXT_WORDS, free))
    c["w5"], c["X2"] = rep(free[5] - 1), rep(free[6] - 1)
    return c


def stored(v):
    """What the outer step and the middle step must leave in memory for the context v: two dicts, name -> value."""
    by_outer = {"w5": v["w5"], "w5+delta": v["w5"] + DELTA5, "S10+X15": v["S10"] + X15, "S6": v["S6"], "1-S6": 1 - v["S6"],
                "X14": v["X14"], "S9+1": v["S9"] + 1, "X9": v["X9"], "-X4": -v["X4"], "C0.b1": v["C0.b1"],
                "ROL(S4,7)": rol(v["S4"], 7), "-S11": -v["S11"], "-S2-S7": -v["S2"] - v["S7"], "w7": v["w7"],
                "-C0.b1-w6": -v["C0.b1"] - v["w6"], "-C0.c1": -v["C0.c1"], "ROL(C0.d1,16)": rol(v["C0.d1"], 16),
                "-D2.b1-W13": -v["D2.b1"] - W13, "D2.c1+1": v["D2.c1"] + 1, "X13": v["X13"], "ROL(X13,8)": rol(v["X13"], 8)}
    by_middle = {"X2": v["X2"], "X2+w7": v["X2"] + v["w7"], "w12-S1-S6": v["w12"] - v["S1"] - v["S6"], "-w2": -v["w2"],
                 "w3": v["w3"], "S5": v["S5"], "S12": v["S12"], "w0": v["w0"], "w1": v["w1"]}
    return by_outer, by_middle


def tools(m, c):
    """Four short forms used by the counted pieces, for the machine m with the memory c: name a memory word as an
    operand, store a register in a cell, reduce every lane to 32 bits, and plus - 1 - x in every lane (x - y is
    x + (y XOR M) + 1; a lane may hold more than 32 bits)."""
    m.memory = c

    def put(name, x):
        c[name] = m.store(x)

    def low(x):
        return m.band(x, m.k("M"))

    def neg(x, plus="1"):
        return m.add(m.xor(x, m.k("M")), m.k(plus))

    return m.k, put, low, neg


def outer_step(m, c):
    """The outer step on the machine m: the next value of w5, the lines of outer(), and the 21 words they leave.

    c is the memory. Every value is computed in all seven lanes, so that every word comes out in the form in which
    the table build, the middle step and the batch load it; a stored word is below 2^32 in every lane. The five
    other words of the outer step are read from memory where they are used.
    """
    k, put, low, neg = tools(m, c)
    m.at("next w5")                                                   # next value, end test, branch, store
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
    d3b = neg(d3a, "X3+1")                                            # D3.b1 = X3 - D3.a1
    x4 = m.pror(m.xor(d3b, x9), 7)
    put("-X4", low(neg(x4)))
    cc = k("C0.c1")
    cb = m.pror(m.xor(x4, cc), 12)
    put("C0.b1", cb)
    s4 = m.xor(m.prol(d3b, 12), d3c)
    put("ROL(S4,7)", m.prol(s4, 7))
    s3 = m.add(d3a, neg(s4))                                          # S3 = D3.a1 - S4
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
    put("w7", low(m.add(s3, neg(m.add(k3a, k3b)))))                   # w7 = S3 - K3.a1 - K3.b1
    put("-C0.b1-w6", low(neg(m.add(cb, m.add(k3a, k("-IV3-IV7"))))))   # w6 = K3.a1 - IV3 - IV7
    m.at("C0 and D2")
    put("-C0.c1", low(neg(cc)))
    cd = k("C0.d1")
    put("ROL(C0.d1,16)", m.prol(cd, 16))
    x8 = m.add(cc, neg(cd))                                           # X8 = C0.c1 - C0.d1
    d2b = m.xor(x8, k("ROL(X7,7)"))
    put("-D2.b1-W13", low(neg(d2b, "1-W13")))
    d2c = m.xor(m.prol(d2b, 12), s7)
    put("D2.c1+1", low(m.add(d2c, k("1"))))
    x13 = low(m.add(x8, neg(d2c)))                                    # X13 = X8 - D2.c1
    put("X13", x13)
    put("ROL(X13,8)", m.prol(x13, 8))


def table_build(m, c, j):
    """The table of an outer step for the seven members of list word U[j], on the machine m: one word of each list.

    The lines of member() from the list word ROL(Y4, 7). XA is the first value of C0 minus X4, R is the second
    value of D1 rotated left by 16. Every stored word is below 2^32 in every lane. Returns the five words by name.
    """
    k = tools(m, c)[0]
    m.at("build loop")                                                # next list position, end test, branch
    m.compare_and_branch(m.advance(j), k("end of list"))
    m.at("build C0")
    y12 = m.band(m.add(m.xor(m.load(list_words(j)[0]), k("C0.b1")), k("-C0.c1")), k("M"))
    row = {"Y12": m.store(y12)}
    ca = m.add(m.xor(m.prol(y12, 8), k("C0.d1")), k("-C0.b1-w6"))     # first value of C0
    row["XA"] = m.store(m.band(m.add(ca, k("-X4")), k("M")))
    x12 = m.xor(ca, k("ROL(C0.d1,16)"))
    m.at("build D1")
    cd1 = m.add(m.xor(x12, k("M")), k("X11+1"))                       # X11 - X12, the third value of D1
    bd1 = m.pror(m.xor(cd1, k("S6")), 12)
    row["X6"] = m.store(m.pror(m.xor(bd1, k("X11")), 7))
    dd1 = m.add(cd1, k("-S11"))
    row["X1"] = m.store(m.band(m.xor(m.prol(x12, 8), dd1), k("M")))
    row["R"] = m.store(m.prol(dd1, 16))
    return row


def middle_step(m, c):
    """The middle step on the machine m: the next value of X2, the lines of middle(), and the nine words they leave.

    Seven of the nine are read by a batch; the other two are X2 itself and w1. The words M and 1 and the masks of
    the rotation by 16 are fetched once and kept in registers for the step. Its last part is the entry of the class
    loop: the words RESIDENT are loaded into the registers in which the batches find them.
    """
    k, put, low, neg = tools(m, c)
    m.at("next X2")                                                   # next value, end test, branch, store
    m.get("M", "1", "A16", "B16")
    x2 = low(m.add(k("X2"), k("1")))
    m.compare_and_branch(x2, k("X2 end"))
    put("X2", x2)
    put("X2+w7", low(m.add(x2, k("w7"))))
    m.at("D2 and K1")
    d2a = m.add(x2, k("-D2.b1-W13"))
    d2d = m.xor(x2, k("ROL(X13,8)"))
    s13 = m.xor(m.prol(d2d, 16), d2a)
    k1c = neg(s13, "S9+1")                                            # K1.c1 = S9 - S13
    k1d = m.add(k1c, k("-IV1"))
    s1 = m.xor(m.prol(s13, 8), k1d)
    put("w12-S1-S6", low(m.add(m.add(d2a, k("-S2-S7")), neg(s1, "1-S6"))))   # w12 = D2.a1 - S2 - S7
    k1a = m.prol(k1d, 16)
    put("-w2", low(neg(k1a, "IV1+IV5+1")))                            # w2 = K1.a1 - IV1 - IV5
    k1b = m.pror(m.xor(k1c, k("IV5")), 12)
    put("w3", low(m.add(s1, neg(m.add(k1a, k1b)))))                   # w3 = S1 - K1.a1 - K1.b1
    put("S5", m.pror(m.xor(k1b, k("S9")), 7))
    m.at("K0")
    s8 = neg(d2d, "D2.c1+1")                                          # S8 = D2.c1 - D2.d1
    k0b = m.xor(s8, k("ROL(S4,7)"))
    k0c = m.xor(m.prol(k0b, 12), k("IV4"))
    s12 = low(m.add(s8, neg(k0c)))                                    # S12 = S8 - K0.c1
    put("S12", s12)
    k0d = m.add(k0c, k("-IV0"))
    k0a = m.prol(k0d, 16)
    put("w0", low(m.add(k0a, k("-IV0-IV4"))))
    s0 = m.xor(m.prol(s12, 8), k0d)
    put("w1", low(m.add(s0, neg(m.add(k0a, k0b)))))                   # w1 = S0 - K0.a1 - K0.b1
    m.at("class loop entry")
    m.drop(list(m.kept))
    m.get(*RESIDENT)
    m.finish(RESIDENT)


def lane_flags(m, c, word):
    """The end of stage 2: bit 32 of every lane of word + M, set where the reduced word is nonzero, and the branch.

    Returns the seven flags and whether the branch is taken, that is whether some lane has a zero word.
    """
    k = tools(m, c)[0]
    flags = m.band(m.add(word, k("M")), k("bit 32"))
    taken = m.compare_and_branch(flags, k("bit 32"))
    return [(flags.z >> (LANE_BITS * i + 32)) & 1 for i in range(LANES)], taken


def rule_a_flags(m, c, z, v):
    """The end of stage A (Lemma A) for seven lanes z and the word v of the list V: the flags of rule A, the branch.

    With y made from z by the steps A_STEPS, u = (y XOR v) AND ALL is ALL exactly in the lanes whose trial
    satisfies rule A, and below ALL in the others (rule_a_constants()). So bit 32 of u + (2^32 - ALL) is set
    exactly in those lanes. The sum is ORed with the word that has every other bit, and compared with that word:
    they differ when some lane satisfies rule A. A lane of z may hold more than 32 bits: a bit above 31, and a bit
    that a shift moves in from the next lane, never reaches a read position (rule_a_constants() stops otherwise)
    and is removed by the AND. Returns the seven flags (1 where the trial fails rule A) and whether the branch is
    taken.
    """
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
    """The two-stage batch of proof.md Section 6.5 for the seven trials of batch j, counted on the machine m.

    c is the memory after the outer step and the middle step, row the five words of the table for batch j. The
    words RESIDENT are in registers when the batch begins, and again when it ends. When only some of the words
    are kept (KEPT a number above 0), stage 2 takes the registers of the words EVICT for its values and loads these
    words again in its last part, and it fetches the masks of the rotations by 8 and by 7, M and the mask of bit
    32 once each and keeps them while it reads them. Every line below is made of calls of m only, so every
    operation and every load is counted. The names are those of
    proof.md 6.1 to 6.5; the parts and their order are those of TABLES. The algorithm runs the parts of stage 2
    only when the branch of stage A is taken; this function always evaluates them, so that their count and their
    lanes can be checked for every batch. entered is the number of batches that have entered stage 2 before this
    one; stage 2 begins by counting its own entry and comparing the count with STAGE_2_BUDGET (step 4 of proof.md
    6.4). Returns the seven reduced stage-2 test words, their seven flags (1 where the word is nonzero), whether
    the final branch is taken, the seven stage-A flags (1 where the trial fails rule A) and whether the stage-A
    branch is taken.
    """
    k = tools(m, c)[0]

    def drop(*names):
        m.drop([name for name in names if name not in RESIDENT])

    m.resident(RESIDENT)
    m.at("loop")                                                      # next list position, end test, branch
    m.compare_and_branch(m.advance(j), k("end of list"))
    m.at("X0 to X10")
    dd0 = m.xor(m.add(m.load(row["XA"]), k("-w2")), k("ROL(X15,8)"))  # X0, then the second value of D0
    x10 = m.add(dd0, k("S10+X15"))                                    # X10 = (S10 + dd0) + X15
    m.at("C2 to z")
    x6 = m.load(row["X6"])
    ra = m.add(x6, k("X2+w7"))                                        # X2 + X6 + w7
    rd = m.pror(m.xor(ra, k("X14")), 16)
    rc = m.add(x10, rd)
    rb = m.pror(m.xor(x6, rc), 12)
    z = m.xor(rd, m.add(m.add(ra, rb), k("w0")))                      # Y14 = ROR(z, 8)
    m.at("rule A")
    flags_a, taken_a = rule_a_flags(m, c, z, list_words(j)[2])
    # ---- stage 2
    m.at("entry count")                                               # one more entry, budget test, branch
    m.drop(EVICT)
    m.compare_and_branch(m.advance(entered), k("stage-2 budget"))
    m.at("C2, rest")
    if Z_AGAIN:                                                       # z, whose register rule A has taken
        z = m.xor(rd, m.add(m.add(m.add(m.load(row["X6"]), k("X2+w7")), rb), k("w0")))
    if RC_AGAIN:
        rc = m.add(x10, rd)                                           # the third value of C2, not kept by stage A
    m.get("A8", "B8")
    y14 = m.pror(z, 8)
    m.get("A7", "B7")
    y6 = m.pror(m.xor(m.add(rc, y14), rb), 7)
    m.at("C1 to Y1")
    bd0 = m.pror(m.xor(m.add(x10, k("-X15")), k("S5")), 12)           # the third value of D0 is X10 - X15
    x5 = m.pror(m.xor(bd0, x10), 7)
    drop("A7", "B7")
    qa = m.add(m.add(x5, m.load(row["X1"])), k("w3"))
    qd = m.pror(m.xor(qa, k("X13")), 16)
    qc = m.add(qd, k("X9"))
    qb = m.pror(m.xor(x5, qc), 12)
    y1 = m.add(m.add(qa, qb), m.xor(m.load(row["R"]), k("S12")))      # Y1 + S1 + S6: w10 is the first value of D1 - S1 - S6
    m.at("E1, A and B")
    a1 = m.add(m.add(y1, y6), k("w12-S1-S6"))                         # Y1 + Y6 + w12
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
    x = m.xor(beta, eps)                                              # below 2^34 in every lane
    rot = m.bor(m.band(m.shr(x, 31), k("A31")), m.shl(x, 1))          # ROL(x, 1) in the low 32 bits, bits 32..34 open
    m.get("M", "bit 32")
    word = m.band(m.xor(m.xor(rot, eps), k("eta")), k("M"))           # the reduced test word of Lemma N
    flags, taken = lane_flags(m, c, word)
    drop("M", "bit 32")
    if EVICT:
        m.at("restore")                                               # the words that stage 2 took the registers of
        m.get(*EVICT)
    m.finish(RESIDENT)
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


def reference(v, y4):
    """What the batch must show for one trial, taken from the compressions of the trial's two real messages.

    The messages A (55 bytes) and B (63 bytes) of the trial are built by steps S2 and S3 and each is compressed in
    full by compress2. Returned: Y4 of A; h1, the second value of E3 on A, from the state Y of A; the test word of
    Lemma N from E1 evaluated for A and for B with g on their own states and words; the same word from the two
    complete digests, digest word 3 XOR ROL(digest word 6, 8) of the XOR of the digests; whether the digests
    agree on digest words 0, 2, 5, 7 with the same Y4 in A and B; and whether the sixteen words of the 55 bytes of
    A are the words of the trial, which needs w14 = w15 = 0 and a zero top byte of w13.
    """
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
    """The four counted pieces for the context free and batch j of the class, each on a new machine.

    Returns a dict and the four machines by the names of TABLES. The dict has the operations and loads of stage A
    and of stage 2, the number of lanes that are right, the number of lanes that pass rule A, whether the batch
    enters stage 2, the number of zero stage-2 test words, and whether the stored words are right: every word
    that the outer step and the middle step left in memory is the word of stored() for the context, and the five
    table words are those of table_row() for the seven members. A lane is right when all of this holds for its
    trial and the reference of its two real messages: the words of message A are the words of the trial; Y4 of
    message A is the member of the lane; the digests agree on digest words 0, 2, 5, 7; the stage-A flag is 0
    exactly when h1 satisfies rule A; the reduced stage-2 word equals the word of Lemma N, which in turn equals
    the word from the two complete digests; and the stage-2 flag tells whether that word is nonzero. No lane
    counts as right when a stored word is not right, or when one of the two branches is not taken exactly if one
    of the seven words in front of it is zero.
    """
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
    """The seven words of a context and a class member number from the organizer seed."""
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
    """lane_flags on all 128 patterns of zero and nonzero lanes; random cases hardly ever have a zero lane."""
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
    """The stage-A test on all patterns of the bits that rule A reads: a complete enumeration for Lemma A.

    A pattern is a value of the bits of z that the conditions of the rule read (the bits of ROL(mask, 24)) together
    with a value of the bits A_FREE of e1. One packed word per pattern: lane i holds the pattern number
    (p + 37 i) modulo the number of patterns, so every pattern occurs once in every lane and the lanes of a word
    differ. The other bits of z and the other free bits of e1 are different in every lane, and the bits 32 and 33
    of the lanes are filled (a lane of z in the batch is below 2^34). A word is right when in every lane the flag
    is 0 exactly if h1 = ROR(ROR(z, 8) XOR e1, 16), with e1 = Y3 + Y4 of the lane's member, satisfies rule A as
    written on h1, the branch is taken exactly if some lane does, and no sum leaves its lane. Returns (words, words
    right, words in which some lane satisfies the rule).
    """
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


def selftest(cases, seed):
    """Run the four counted pieces on contexts derived from the seed text, print one JSON line, return the exit status."""
    shape, uses, same, last, extreme = None, None, True, 0, 0
    sums, registers = {name: {} for name in TABLES}, {name: 0 for name in TABLES}
    total = {"lanes_right": 0, "lanes_passing_rule_a": 0, "stage_2_entered": 0, "zero_test_words": 0, "stored_right": 0}
    for case in range(cases):
        text = "halfsearch selftest %s %d" % (seed, case)
        stream = struct.unpack("<9I", hashlib.shake_256(text.encode("utf-8")).digest(36))
        seven, j = list(stream[:7]), stream[7] % BATCHES
        if case % 4 == 0:                       # the last batch of the class, whose spare lanes repeat the last member
            j, last = BATCHES - 1, last + 1
        if case % 5 == 4:                       # extreme words: each context word is 0, 2^32 - 1 or as drawn
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
            if bounds.get(part) is not None:            # largest sum in units of 2^32, rounded down
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
    report = {
        "selftest": "outer step, table build, middle step and two-stage packed batch of proof.md Section 6.5",
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
    }
    json.dump(report, sys.stdout, separators=(",", ":"))
    sys.stdout.write("\n")
    good = (total["lanes_right"] == cases * LANES and total["stored_right"] == cases and same
            and report["counts_equal_table"] and below and max(registers.values()) <= REGISTERS
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
