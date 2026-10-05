# SHA-256, 31 prefix rounds: two-block differential collision attack

This **exploratory** package selects track `sha256-r31-exploratory`, target
`sha256-r31-prefix-v1`, cost model `collision-frontier-v5`, and policy
`paired-lanes-v1`. It submits a concrete two-block differential collision
algorithm with declared heuristics, plus one mechanically checkable collision
witness for the exact target. Readiness requests review; it does not assert
an AI outcome, human acceptance, or a mathematical proof.

Attribution: the cryptanalysis is NOT original to this submission. The
algorithm is the published 31-step SHA-256 collision attack of Yingxin Li,
Fukang Liu and Gaoli Wang, "New Records in Collision Attacks on SHA-2",
EUROCRYPT 2024 (IACR ePrint 2024/349, Section 4.2), which improves the
two-block framework of Mendel, Nad and Schlaffer (EUROCRYPT 2013). The
witness pair is the published practical pair of Li, Liu, Wang, Dong and Sun,
"The First Practical Collision for 31-Step SHA-256", ASIACRYPT 2024, as
distributed in the authors' public verifier repository. This package's own
contribution is to (i) instantiate that attack inside the organizer's v5
total-computation RAM model, (ii) charge every phase including word
operations, table handling, failures and success amplification, and (iii)
bind the result to the exact padded target with a verified witness.

The required `baseline_improved` value `sha256-r31-nominal-v2` only identifies
the organizer's nominal display reference (128); it is not an established
attack. The declared scalar is `time_log2: 52`.

## 1. Target binding

The target is the complete SHA-256 hash with the standard FIPS 180-4 IV,
standard padding (0x80, zeros to 56 mod 64, 64-bit big-endian bit length),
standard message expansion and constants at original indices, rounds 0..30
inclusive in every compression, full feed-forward, and the full 256-bit
big-endian digest. Notation: for one compression, W[0..15] are the block
words, W[16..30] the expanded words, and A_i, E_i the new values of working
registers a and e produced by round i (i = 0..30). Following the standard
Davies-Meyer view, the incoming chaining value is the eight registers
(A_-1, A_-2, A_-3, A_-4, E_-1, E_-2, E_-3, E_-4) = (a, b, c, d, e, f, g, h).
The two round recurrences used below are, with all arithmetic mod 2^32,

    E_i = A_{i-4} + E_{i-4} + S1(E_{i-1}) + Ch(E_{i-1},E_{i-2},E_{i-3}) + K_i + W_i
    A_i = E_i - A_{i-4} + S0(A_{i-1}) + Maj(A_{i-1},A_{i-2},A_{i-3})

where S0, S1, Ch, Maj are the FIPS functions. Both are invertible in each
single unknown, which is what lets the attack compute backwards from an
internal state to the chaining value and the free words W[0..4].

Messages are exactly two 64-byte blocks M0 || M1 and M0 || M1'. Since both
have 128 bytes, padding appends the same third block. If the chaining values
after block 2 are equal, the third compressions are identical and the full
digests are equal. All three compressions of each message use the 31-round
target compression.

## 2. Witness certificate (mechanical evidence, not the cost argument)

`certificates/manifest.json` declares one `hash-collision-witness-v2`
certificate. `llwds24-a.bin` and `llwds24-b.bin` are 128-byte messages that
share block 1:

    M0  = 8ce3f805 5c401aed 579e5f7f bc3116cb ca189b3c eb75f04c 958f0a0e 7760b082
          dcd5027d 32260ad6 7b12b659 eee66518 ad7f88dd f8ad20bb 7ae40ffd 21609249
    M1  = 9abdeb1b 1f195f41 5a7210c1 55614f13 a2269dd1 be888a61 359257d4 adf3737b
          9f0484a6 eb830a58 66add94a 9669232d 45271fa5 b8f69585 428bbce3 0703b904
    M1' = 9abdeb1b 1f195f41 5a7210c1 55614f13 a2269dd1 be887a67 35b2dfc5 fde32975
          c70595a6 eb838a5c 66add94a 9669232d 45271fa5 b8f69585 428bbce3 0703b904

The chaining value after M0 is
`c0a93f38 23b02f67 2f718088 03dfb329 7eaa51b9 0e2dd226 107e021b 70b1ac59`.
The state after block 2 is identical for both messages
(`ff558659 2977dd01 ... f7025605`), and the complete padded digest under the
organizer checker is
`55fdfb37efcbd086e19c3de0f72596300a3acdf48da5b1d0450a592bb2869fcd`.
The organizer's checker recomputes this; it is not trusted from this file.

I recomputed the per-round XOR differences of this pair with an independent
31-round implementation. They exhibit exactly the local-collision shape the
attack relies on:

| Round i | XOR dW_i | XOR dA_i | XOR dE_i |
| --- | --- | --- | --- |
| 0-4 | 0 | 0 | 0 |
| 5 | 0000f006 | 000017fa | 0000303e |
| 6 | 00208811 | 00800001 | 00088001 |
| 7 | 50105a0e | 11201005 | d0880489 |
| 8 | 58011100 | 00000004 | 4d008804 |
| 9 | 00008004 | 0 | 00000008 |
| 10 | 0 | 00008004 | 2f8187f8 |
| 11 | 0 | 0 | 10c00008 |
| 12 | 0 | 0 | 00008008 |
| 13 | 0 | 0 | 0 |
| 14 | 0 | 0 | 00008004 |
| 15 | 0 | 0 | 0 |
| 16 | 0007fffc | 0 | 0 |
| 17 | 0 | 0 | 0 |
| 18 | 00008004 | 0 | 0 |
| 19-30 | 0 | 0 | 0 |

Message differences occur only in W5..W9 and in the expanded words W16 and
W18; block words W0..W4 and W10..W15 are equal; the state difference is
cancelled from round 15 onward, so the feed-forward outputs agree. This is
the 7-word message-difference pattern (W5,W6,W7,W8,W9,W16,W18) of the
published characteristic.

Scope of this evidence: the certificate establishes that a characteristic of
this shape is valid for the exact target (no hidden contradiction), that
first-block matching with free W0..W4 really reaches the standard IV, and
that the padded construction collides. One successful run does NOT establish
the expected cost; Sections 3-6 give the cost argument and its heuristics.
The algorithm below does not read the certificate; it is not advice.

## 3. The algorithm (EUROCRYPT 2024, one starting point)

The second-block characteristic has no conditions on W0..W4, on E_1, E_2, or
on the chaining registers. All differential conditions in rounds 5..12 are
packed into a precomputed table; the free words W0..W4 then connect any
matching chaining value to a table entry.

Phase 0 (starting point). Using a SAT/SMT model of the signed differential
and value transitions, find one starting point: values of A_1..A_12,
E_5..E_12 and W9..W12 satisfying all differential conditions on rounds 5..12.
The paper reports T_model ~ 2^31.7 for this step and calls it negligible.

Phase 1 (table TAB1). Under the characteristic, W5, W6, W7, W8 have
respectively 2^14, 2^23, 2^27, 2^25 admissible values (the bit conditions
enforcing the local collision in the message expansion). For the fixed
starting point, E_4 is determined by W8 and E_3 by W7 via the E recurrence
(read backwards), and the conditions on (E_3,E_4) leave, by the paper's
experiment, about 2^11 valid (W7,W8) pairs. E_1, E_2 then follow from W5, W6,
and A_0, A_-1, A_-2, A_-3 follow from the A recurrence read backwards. There
are no conditions on E_1, E_2 or on A_-3..A_0. So one starting point yields
2^(14+23+11) = 2^48 complete solutions of (A_i)_{-3..12}, (E_i)_{1..12},
(W_i)_{5..12}. Each solution is inserted in TAB1 keyed by its 96-bit value
(A_-3, A_-2, A_-1).

Phase 2 (matching). Repeat N = 2^50.3 times: draw a fresh uniform 512-bit
first block M0 (two random 256-bit words), compute the 31-round compression
from the IV, and look up the resulting (a, b, c) = (A_-1, A_-2, A_-3) in
TAB1. On a match, the chaining value fixes A_-4 and E_-4..E_-1; with the
entry's A_-3..A_12, E_1..E_12, W5..W12, the five words W0..W4 and E_0 are
uniquely determined by the recurrences (rounds 0..4 each have exactly one
unknown message word). Pass the match to Phase 3. Process at most 64
matches; ignore further matches.

Phase 3 (remaining conditions). Now W0..W12 are fixed. Use W13, W14, W15
(96 free bits) to satisfy the remaining uncontrolled conditions on
E_13, E_14, E_15, W16 and W18 (W16 and W18 depend on W14 and on W16 through
the sigma functions). The paper measured that this succeeds with probability
2^-gamma, gamma ~ 1.3, "by 100 tests". On success, output
(M0 || M1, M0 || M1'), where M1' = M1 plus the characteristic's differences
in W5..W9.

Phase 4 (verification). Recompute both complete padded 31-round digests
(three compressions each), check equality and message inequality, and
return the pair; otherwise continue Phase 2 until N trials are exhausted,
then return FAIL.

Correctness of any returned pair is unconditional: Phase 4 checks it with
the exact target function. Heuristics affect only cost and success
probability.

## 4. Success probability

Heuristic H-match: chaining values (A_-1, A_-2, A_-3) of independent uniform
first blocks behave as independent and close to uniform on 96 bits with
respect to the fixed 2^48-entry set, so each trial matches with probability
about 2^48 / 2^96 = 2^-48. Uniform M0 is drawn with fresh model coins; the
heuristic concerns only how the compression output hits a fixed set.

Expected matches: lambda_m = N * 2^-48 = 2^2.3 ~ 4.92. With the Poisson
approximation of a sum of 2^50.3 rare independent indicators, and
H-step3 (each match independently passes Phase 3 with probability
2^-gamma, gamma ~ 1.3), the number of successes is approximately Poisson
with mean 4.92 * 2^-1.3 ~ 2.0, so

    Pr(success) ~ 1 - exp(-2.0) ~ 0.865.

The 64-match cap only matters if more than 64 matches occur, which has
probability below 10^-30 for mean 4.92; the cap cannot reduce success
probability by more than that.

Robustness: the declared `success_probability: 0.6` needs a success mean of
at least ln(2.5) ~ 0.917, i.e. it still holds if gamma is as large as
about 2.42 (over one bit worse than measured), or if the effective table
size is about 2^47 rather than 2^48 at gamma = 1.3. This is a heuristic
lower bound, not a proof and not a confidence level.

## 5. Resource accounting under collision-frontier-v5

Units: one 31-round target compression (including its expansion and
feed-forward) costs 1. Every other 256-bit-word RAM primitive (load, store,
add, Boolean, shift/rotate, compare, branch, random word) costs 1/C with
C = 2140. Counts below are deliberately padded upper budgets, including
instruction-level overhead (operand loads/stores, address arithmetic,
loop control). 32-bit operations are performed in 256-bit words and masked;
masks are included in the budgets.

### 5.1 Phase costs

| Phase | Work | Units (v5) | log2 |
| --- | --- | --- | --- |
| 0 starting point | SAT/SMT search, budgeted at 2^40 units (paper: ~2^31.7) | 2^40 | 40.0 |
| 1a valid (W7,W8) | exhaustive pairs 2^25 x 2^27 = 2^52, each <= 128 ops | 2^52*128/2140 | 47.94 |
| 1b table entries | 2^48 entries, each <= 1024 ops (backward recurrences + insert) | 2^48*1024/2140 | 46.94 |
| 2 matching | 2^50.3 trials, each 1 compression + <= 2048 ops | 2^50.3*(1+2048/2140) | 51.27 |
| 3 conditions | <= 64 matches, each budgeted at 2^36 units | 2^42 | 42.0 |
| 4 verification | 6 compressions + <= 8192 ops per returned candidate | < 2^4 | ~3.6 |
| Total | sum of the above | < 2^51.48 | 51.48 |

Phase 1a is intentionally naive. The admissible W7 and W8 values are
defined by bit conditions and can be enumerated directly; for each W8 the
backward E recurrence gives E_4, for each W7 it gives E_3, and checking the
characteristic's conditions on (E_3, E_4) is a fixed number of masked
compares. A staged search (W8 first, then only W7 for surviving W8) is far
cheaper, but the full product is charged so that no staging assumption is
needed. It is the paper's experimental claim, not this bound, that about
2^11 pairs survive (heuristic H-table).

Phase 2 per-trial budget (<= 2048 ops): two random-word draws; unpacking
16 message words (shifts/masks, ~32 ops); dispatching the compression and
copying 8 state words (~32 ops); forming the bucket index from the chaining
words (~8 ops); scanning a bucket of at most 16 slots with a 96-bit key
compare each (<= 16 * 16 = 256 ops); loop control and counters. With the
8x instruction-overhead factor on the core ~200 operations this stays under
2048 ops = 0.957 units, so a trial costs < 1.957 units < 2^0.969.

Phase 3 budget: once W0..W12 are fixed, E_13, E_14, E_15 depend on W13,
W14, W15 one word at a time (each E_i is affine in W_i given earlier state),
so their bit conditions are set directly; the W16/W18 conditions are then
tested over the remaining freedom. The paper treats this step as negligible
and evaluated it 100 times. The 2^36-unit budget per match (about 2^47 word
operations) is a deliberately generous cap; heuristic H-step3 covers it.

Total time:

    T <= 2^40 + 2^47.94 + 2^46.94 + 2^51.27 + 2^42 + 16 < 2^51.48 < 2^52.

Hence `time_log2: 52`. Preprocessing (Phases 0 and 1) is below
2^40 + 2^47.94 + 2^46.94 < 2^48.6 units, declared as
`preprocessing_log2: 49`; it is included in T, not additional.

The paper's own estimate is 2^(96-48+1.3) + 2^48 ~ 2^49.8 (unit: SHA-256
computations, word-operation overhead not charged). The difference to 52
comes from success amplification to a mean of 2 successes (one extra bit of
trials), the 0.957-unit word-operation surcharge per trial, and the padded
table-construction budgets.

### 5.2 Memory

TAB1 is a bucketed hash table with 2^47 buckets indexed by 47 bits of
(A_-1, A_-2, A_-3), each bucket a fixed array of 16 slots plus an 8-byte
fill counter. A slot is one 256-bit word (32 bytes) holding the 96-bit key
and the 48-bit index (14 + 23 + 11 bits) from which W5, W6 and the
(W7,W8) pair are recomputed in Phase 2 on a match. With 2^48 entries the
mean load is 2 per bucket; an entry is dropped only if its bucket already
holds 16, which for Poisson(2) loads affects a fraction below 10^-9 of
entries, negligible for lambda_m. Memory:

    2^47 * 16 * 32 + 2^47 * 8 + (starting-point model, list of 2^11 (W7,W8)
    pairs, code, constants and scratch, all budgeted at <= 2^40 bytes)
    < 2^56.03 bytes < 2^57.

Hence `memory_log2_bytes: 57`. Memory is reported only; it does not affect
the scalar.

`nonuniform_advice_log2_bytes: 0`: there is no advice. The characteristic
(conditions on rounds 5..18) is public specification of the algorithm and
is regenerated in Phase 0 from the model; its storage is inside the 2^40-byte
budget and its search inside the 2^40-unit Phase-0 budget. The certificate
pair is evidence only and is never consulted by the algorithm.

## 6. Declared heuristics

H-table (score-critical). One starting point yields about 2^48 valid table
entries: 2^14 W5 values, 2^23 W6 values, and about 2^11 (W7,W8) pairs
satisfying the (E_3,E_4) conditions. Evidence: the published experiment
(Li-Liu-Wang 2024, Section 4.2) and the certificate, whose second block is a
concrete member of such a solution family (Section 2 table). Score
sensitivity: N is fixed, so a table of 2^(48-d) entries does not change
the time bound; it lowers the success mean to 2^(1-d), and the declared
0.6 holds for d <= 1.1 (at gamma = 1.3). Restoring a success mean of 2
would cost d more bits of Phase 2.

H-match (score-critical). First-block chaining values hit the fixed 96-bit
key set at rate about 2^-48 per trial, independently across trials.
Evidence: the compression is evaluated on independent uniform inputs; this
is the standard random-function heuristic for one 31-round compression
restricted to three output words, and the certificate shows a match to the
standard IV is reachable. Limitation: not proved for the actual function.

H-step3 (score-critical). A match completes Phase 3 with probability about
2^-1.3, and each attempt costs well below 2^36 units. Evidence: the paper's
100 tests; the certificate, which satisfies all conditions on rounds 13..18
(zero state difference from round 15, Section 2 table). Limitation: 100
tests give gamma only to roughly +-0.3 bits; Section 4 shows the claim
survives gamma up to ~2.42.

H-start (supporting). One starting point can be found with the SAT/SMT
model in at most 2^40 units. Evidence: the paper's T_model ~ 2^31.7 and the
existence of the certificate's internal state. If this failed it would not
change the scalar (2^40 is far below 2^51.3).

## 7. Relation to other published results and limitations

- Mendel-Nad-Schlaffer (EUROCRYPT 2013): time 2^65.5, memory 2^34, same
  two-block framework with an older characteristic (l ~ 34, gamma ~ 3.5).
- Li-Liu-Wang (EUROCRYPT 2024): 2^49.8 time, 2^48 memory; this package's
  algorithm.
- Li-Liu-Wang-Dong-Sun (ASIACRYPT 2024): a memory-efficient variant that
  matches only A_-1 against a small table and checks A_-2, A_-3 on the fly;
  the authors report finding a pair in 1.2 hours with 64 threads and
  negligible memory. Its concrete parameters and stated time complexity are
  not reproduced here, so this package does not claim its cost; it uses only
  its published pair as a witness. A future submission could tighten the
  scalar with that variant.

Limitations: the score depends on the heuristics above, which are supported
by published experiments and by one exact-target witness, not by proof. The
paper's unit for 2^49.8 is not stated; this package does not rely on it and
re-derives every phase's cost in v5 units. No experiment manifest is
declared: no participant code is executed. This is an exploratory claim;
it does not qualify the rigorous lane.
