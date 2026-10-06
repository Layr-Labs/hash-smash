# SHA-256 reduced to 31 steps: a two-block collision generator with self-generated starting points

Track `sha256-r31-exploratory`, target `sha256-r31-prefix-v1`, cost model `collision-frontier-v5`
(C = 2140), policy `paired-lanes-v1`, exploratory lane.

## 1. Claim and summary

Claim: a randomized algorithm that outputs two distinct 128-byte messages with equal 31-step
SHA-256 digests with probability at least 0.39 over its own coins, with total charged time below
2^39.65 target-compression units in every run. Memory is below 2^35 bytes.

The collision structure is the published two-block attack on 31-step SHA-256 (Mendel, Nad and
Schlaeffer, EUROCRYPT 2013; Li, Liu and Wang, EUROCRYPT 2024; Li, Liu, Wang, Dong and Sun,
ASIACRYPT 2024): a local collision in message words W5..W9, W16, W18 of the second block, a
precomputed table of "starting points" for steps 5..12, and a matching phase over random first
blocks. We use the published signed differential characteristic as advice. We do not use the
published colliding pair, its starting point, or any output of the published collision run.

What is new here, and what moves the cost:

1. **Own starting points at measured cost.** A complete bit-vector model of the starting-point
   conditions (Section 5) is solved with the STP solver. Adding the published characteristic's
   signed XOR patterns for both messages makes each solve take 1-3 CPU-minutes. Five
   independent base starting points were produced with 715 CPU-seconds in total, counting the
   unsatisfiable runs.
2. **Cheap neighbours.** From each base, a deterministic local search over 1- and 2-bit changes
   with an exhaustive "repair" of the later state words (Section 6) finds 4291 distinct
   starting points in total, with 59,279,520 table tuples. Every condition is an exact modular
   equation and is re-checked on every candidate.
3. **Several completions per match.** Each starting point carries up to 64 alternative
   completions of steps 9..12 with distinct W11. A matched first block can try each, so the
   final filter on `c18` passes with probability 0.256 instead of 0.136.

Per trial, under a uniform chaining value, the algorithm succeeds with probability at least
2^-35.16 (Section 9). Total time is dominated by the one-time cost of the published
characteristic, charged at 2^39.5 under declared premise H-CHAR. The online phase costs 2^35.35.

Evidence that the generator works: on one 12-thread machine, the full algorithm found
14 distinct new collisions from random first blocks in two one-hour runs (Section 12). All 14
are included as organizer-verified certificates. An organizer-run experiment re-completes the found prefixes
from fresh seeds.

`baseline_improved` names the organizer's nominal reference `sha256-r31-nominal-v2`, as the
schema requires. Comparison with the Yukon incumbent is left to Yukon.

## 2. Target and notation

All words are 32 bits, `+`/`-` are modulo 2^32, `>>>` is rotation right, `>>` is shift right.

    S0(x) = (x>>>2) ^ (x>>>13) ^ (x>>>22)      S1(x) = (x>>>6) ^ (x>>>11) ^ (x>>>25)
    s0(x) = (x>>>7) ^ (x>>>18) ^ (x>>3)        s1(x) = (x>>>17) ^ (x>>>19) ^ (x>>10)
    Ch(e,f,g) = (e & f) ^ (~e & g)             Maj(a,b,c) = (a & b) ^ (a & c) ^ (b & c)

The reduced compression C(H, M) expands W16..W30 by W[t] = s1(W[t-2]) + W[t-7] + s0(W[t-15]) +
W[t-16], runs steps t = 0..30 with the first 31 standard constants K[t] at their original
indices, and adds the working state to H. The hash pads with FIPS 180-4 padding, starts from the
standard IV, and outputs all eight words. This is the organizer profile: standard IV, padding,
step indices 0..30 on every block, full feed-forward, all 256 bits.

Write A_t, E_t for the new a and e after step t. Then

    E_t = A_{t-4} + E_{t-4} + S1(E_{t-1}) + Ch(E_{t-1},E_{t-2},E_{t-3}) + K[t] + W[t]        (1)
    A_t = E_t - A_{t-4} + S0(A_{t-1}) + Maj(A_{t-1},A_{t-2},A_{t-3})                          (2)

The chaining value entering a block is (A_-1, A_-2, A_-3, A_-4, E_-1, E_-2, E_-3, E_-4).

Output. m = M0 || M1 and m' = M0 || M1', 128 bytes each. Both are hashed as three blocks: M0,
then M1 or M1', then the same padding block (0x80, zeros, bit length 1024). If
C(CV, M1) = C(CV, M1') for CV = C(IV, M0), the digests are equal. M1' = M1 + (d5..d9) in words
5..9, so the messages differ. Primed quantities belong to M1'. For a word X, dX = X' - X.

## 3. Advice: the published signed characteristic

The algorithm stores, as nonuniform advice, the published characteristic of the second block
(Li, Liu, Wang, EUROCRYPT 2024, 31-step SHA-256), in the following form. It is under 256 bytes.

Message differences: d5 = fffff006, d6 = 002087f1, d7 = 4fefb5fa, d8 = 28011100, d9 = 00008004,
and d_t = 0 for the other t < 16.
State differences used as constants: dE6 = fff87fff, dE7 = 4f880387, dE8 = 44ff8804.

Signed XOR patterns. For each word, `xor` is X ^ X' and `n` is the set of bits where X = 1 and
X' = 0. So the bits of X at positions in `xor` are fixed: equal to `n` there.

     t   A xor     A n       E xor     E n
     5   000017fa  000013fa  0000303e  0000201c
     6   00800001  00800000  00088001  00080001
     7   11201005  01201004  d0880489  40800081
     8   00000004  00000004  4d008804  04008000
     9   00000000  00000000  00000008  00000000
    10   00008004  00000000  2f8187f8  200083f8
    11   00000000  00000000  10c00008  00000008
    12   00000000  00000000  00008008  00008008
    W7   50105a0e  0010520a      W8   58011100  18000000

Derived constants (computed, not stored): c5 = d0018020, c6 = 00000ffa, c7 = ffdf780f,
c8 = b00fca02, x18 = 2ffe7fe0, d16 = 00008004, d18 = ffff7ffc.

The cost of finding this characteristic is charged as T_char under premise H-CHAR (Section 11).
The published colliding messages are not used by the algorithm, and their construction is not
part of its cost.

## 4. Word sets (exact, by enumeration over all 2^32 words)

    V_i = { w : s0(w + d_i) - s0(w) = c_i }    i = 5,6,7,8
    V9  = { w : s0(w + d9) - s0(w) = -d8 }
    G16 = { w : s1(w + d16) - s1(w) = d18 },    G18 = { w : s1(w + d18) - s1(w) = x18 }
    S   = { c : some g in G16 has s1(g) + c in G18 }

Sizes: |V5| = 16384, |V6| = 8388608 = 2^23, |V7| = 512, |V8| = 49408, |V9| = 35921920,
|G16| = 64, |G18| = 42467328, |S| = 584683520 (density 0.1361322).

These sets make the message expansion carry exactly d16 = d9, d18 = -d9 and no other difference:

    W16: d16 = d9.                      W18: needs W16 in G16.
    W20: needs W18 in G18 and W5 in V5 (x18 + c5 = 0).
    W21: W6 in V6.   W22: W7 in V7.   W23: W8 in V8 (d16 + c8 + d7 = 0).
    W24: W9 in V9.   W25: d18 + d9 = 0.   W17, W19, W26..W30: no difference.

## 5. Starting points and how the base points are generated

A starting point (SP) is the 12 words F = (A5, A6, A7, A8, E5, ..., E12) of message 1. The
following are derived from it:

- A1..A4 by (2) at steps 8, 7, 6, 5, and A9..A12 by (2);
- W9..W12 by (1), solved for W;
- message 2: A'_t = A_t for t <= 4, E'_5 = E5 + d5, E'_6 = E6 + dE6, E'_7 = E7 + dE7,
  E'_8 = E8 + dE8, A'_5..A'_8 by (2), then E'_9..E'_12 by (1) with W'_9 = W9 + d9 and
  W'_10..12 = W10..12, and A'_9..A'_12 by (2).

**SP conditions** (all exact 32-bit equations):

    (P3)   E'_8 - E_8 = [S1(E'_7) - S1(E_7)] + [Ch(E'_7,E'_6,E'_5) - Ch(E_7,E_6,E_5)] + d8
    (A9..12) A'_9 = A_9,  A'_10 - A_10 = 00008004,  A'_11 = A_11,  A'_12 = A_12
    (W9)   W9 in V9
    (E13)  A_9 + E_9 + S1(E_12) + Ch(E_12,E_11,E_10) = (same with primes)
    (A13)  S0(A_12) + Maj(A_12,A_11,A_10) = (same with primes)

(P3) makes step 8 consistent for both messages for every E_4 and W8. (E13) and (A13) give no
state difference after step 13 for every W13.

A **tuple** of an SP is (W7, W8) with W7 in V7, W8 in V8, and the two exact step-6/7 conditions

    E_4 = E_8 - A_4 - S1(E_7) - Ch(E_7,E_6,E_5) - K[8] - W8
    (F7)  Ch(E'_6,E'_5,E_4) - Ch(E_6,E_5,E_4) = (E'_7 - E_7) - [S1(E'_6) - S1(E_6)] - d7
    E_3 = E_7 - A_3 - S1(E_6) - Ch(E_6,E_5,E_4) - K[7] - W7
    (F6)  Ch(E'_5,E_4,E_3) - Ch(E_5,E_4,E_3) = (E'_6 - E_6) - [S1(E'_5) - S1(E_5)] - d6

Its key is A_-1 = E_3 - A_3 + S0(A_2) + Maj(A_2,A_1,A_0), with A_0 = E_4 - A_4 + S0(A_3) +
Maj(A_3,A_2,A_1). Tuples are enumerated by testing (F7) for all 49408 W8 and then (F6) for all
512 W7 for each W8 that passes.

**Base generation (model M).** M is a bit-vector formula over the 32-bit unknowns A5..A8,
E5..E12, W7, W8, which states:

- all derivations and SP conditions above, verbatim;
- one tuple: W7 in V7, W8 in V8 (as the s0 equations), (F7) and (F6);
- the advice's signed patterns: (X & xor) = n for X in {A5..A8, E5..E12, W7, W8}, and
  (X ^ X') = xor for X in {A5..A12, E5..E12} with X' computed as above.

M is written in STP's CVC language (215 assertions) and solved with STP 2.4.1, the official
release binary `stp-2.4.1-linux-amd64`, SHA-256
a9c0eb7834c6b4d24a0d3c5ee62509cd8f1ef0f6b11dfef78f3841ae2097d57e, default MiniSat backend, one
thread. The algorithm solves M once, and then M with each of 12 "cubes". Cube i adds four unit
constraints `X[b:b] = v`; the word X, bit b and value v are drawn from
`random.Random(sha256("base-cube-<i>"))` in Python 3.12, choosing X from the 12 SP words. The
satisfiable runs give the base SPs. Measured CPU time on this machine (user + sys): 179.1 s for
M, and 535.9 s for all 12 cubes (8 unsatisfiable, 4 satisfiable). Every output is re-checked
with the exact conditions above. Every base has at least one tuple by construction of M (the
base from M itself has 1280).

## 6. The starting-point family (deterministic local search)

For each base, a breadth-first search over SPs. Two SPs are the same node if their first eight
words (A5..A8, E5..E8) agree. For each node, in order:

1. Candidates: flip one or two bits (b1 <= b2) in one of the first eight words, for every word
   and bit pair in increasing order. Then flip one bit in each of two different first-eight
   words, for every word pair and bit pair.
2. Skip if already seen. Skip if (P3) or (A9) fails. These depend only on the first eight words.
3. Repair. If the SP conditions fail, try in order every 1- or 2-bit flip of one of E9..E12,
   then every single-bit flip in each of two of E9..E12. Take the first that satisfies all SP
   conditions, or drop the candidate.
4. Keep the candidate as a new node if it has at least one tuple.

The search ends when the queue is exhausted. Results for the five bases: 129, 910, 2164, 880 and
208 nodes, together 4291 distinct SPs with 59,279,520 tuples under 16,543,438 distinct keys.
The largest group of tuples sharing a key has 168 entries.

**Completions.** For each SP, a second search over 1- and 2-bit flips of E9..E12, starting from
the SP itself, collects up to 64 full SPs that satisfy all SP conditions and have pairwise
distinct W11. They share the first eight words, so they share the tuples. There are 90,215 in
total, between 4 and 64 per SP.

## 7. Online phase: one trial and the prefix

**Table.** All tuples of all SPs, sorted by key, with the SP index and the per-tuple constants.
A bitmap over the 2^32 keys marks which keys occur.

**Trial.** Draw two fresh uniform 256-bit RAM words and use them as the 512-bit block M0.
Compute CV = C(IV, M0). If the bitmap bit of A_-1 is 0, the trial ends. Otherwise, for each
tuple with key A_-1 (found by binary search):

    E_2 = A_2 + A_-2 - S0(A_1) - Maj(A_1,A_0,A_-1)
    W6  = E_6 - A_2 - E_2 - S1(E_5) - Ch(E_5,E_4,E_3) - K[6];       if W6 not in V6: next tuple
    E_1 = A_1 + A_-3 - S0(A_0) - Maj(A_0,A_-1,A_-2)
    W5  = E_5 - A_1 - E_1 - S1(E_4) - Ch(E_4,E_3,E_2) - K[5];       if W5 not in V5: next tuple
    E_0 = A_0 + A_-4 - S0(A_-1) - Maj(A_-1,A_-2,A_-3)
    W0..W4 by (1) solved for W at steps 0..4 (from CV and A_0, E_0..E_4)

The trial is then **prefix-valid**, with W0..W8 fixed. Both messages reach the SP states after
step 12 with any completion of that SP: steps 0..4 are identical; step 5 gives E'_5 = E_5 + d5;
(F6) and (F7) are steps 6 and 7 for message 2; (P3) is step 8; steps 9..12 hold by construction
of the SP. Equations (2) at steps 0..4 hold because E_0, E_1, E_2 were defined from them.

Lemma 1 (uniform chaining value). Fix a tuple. Its key matches with probability 2^-32. Given
the key, W6 = const - A_-2 is a bijection of A_-2, so W6 in V6 has probability exactly 2^-9.
Given A_-1 and A_-2, W5 = const - A_-3 is a bijection, so W5 in V5 has probability exactly
2^-18. Each tuple therefore accepts a set of chaining values of measure exactly 2^-59.

Lemma 2. Under a uniform CV, conditioned on (A_-1..A_-4) and on acceptance, (W0, W1, W2, W3) is
uniform on 2^128. The map (E_-4, E_-3, E_-2, E_-1) -> (W0..W3) is a triangular bijection, and
the E-words are uniform and independent of the A-words.

## 8. Completion of a prefix-valid trial

For each completion of the matched SP in order (at most 64), set W9..W12 from it and compute

    c16 = W9 + s0(W1) + W0,   c18 = W11 + s0(W3) + W2.

If c18 is not in S, go to the next completion. Otherwise, for each g in G16 with
s1(g) + c18 in G18: W16 = g, W18 = s1(g) + c18, W14 = s1^-1(g - c16) (s1 is an invertible
GF(2)-linear map). Search x = E_13 and then z = E_15 with fresh random starting offsets and step
9e3779b9, under these exact conditions:

    (C14)  dE_10 + Ch(x,E'_12,E'_11) - Ch(x,E_12,E_11) = 0              [so dE_14 = dA_10]
           y = A_10 + E_10 + S1(x) + Ch(x,E_12,E_11) + K[14] + W14,  y' = y + 00008004
    (C15)  E_11 + S1(y) + Ch(y,x,E_12) = E'_11 + S1(y') + Ch(y',x,E'_12)  [E'_15 = E_15]
    (C16)  E_12 + Ch(z,y,x) = E'_12 + Ch(z,y',x) + d9                      [E'_16 = E_16]
           u = A_12 + E_12 + S1(z) + Ch(z,y,x) + K[16] + g
    (C17)  Ch(u,z,y) = Ch(u,z,y')                                          [E'_17 = E_17]

On success, W13 = x - [A_9 + E_9 + S1(E_12) + Ch(E_12,E_11,E_10) + K[13]] and
W15 = z - [A_11 + E_11 + S1(y) + Ch(y,x,E_12) + K[15]]. After step 18 the states are equal:
dE_18 = dE_14 + d18 = 0, and all A-differences vanish by (2). With the expansion of Section 4,
the remaining steps and the feed-forward are equal. Caps per completion call: at most 2^18
candidates x and at most 2^14 candidates z in total, at most 64 z per accepted x.

Output check. Build m and m', hash both with three compressions each, compare, and require
m != m'. The algorithm outputs only a checked pair.

## 9. The complete algorithm and its success probability

    Parameters: N = 40 * 2^30 trials, H = 2^28 key hits, Q = 2^12 prefix-valid trials.
    Preprocessing: word sets (Section 4), base SPs (Section 5), family and completions
      (Section 6), table.
    For i = 1..N: one trial. If more than H key hits or more than Q prefix-valid trials have
      occurred: FAIL. On a prefix-valid trial run Section 8; on a checked pair, output and stop.
    After N trials: FAIL.

All randomness is fresh uniform 256-bit words: two per trial, and one per offset in Section 8.
Trials are therefore independent and identically distributed. The tables are fixed.

**Per-trial success under a uniform CV (q_U).** Write P for the union of the tuples' accepted
sets. By Lemma 1, each tuple has measure exactly 2^-59, and sets with different keys are
disjoint, so Pr_U[CV in P] <= 59,279,520 * 2^-59 = 2^-33.179 exactly. Tuples sharing a key can
overlap. For every CV in P, the algorithm tries the tuples of its key in table order, so there
is a unique **first** accepting tuple t*(CV). It succeeds at least when t*'s starting point
completes. Hence, exactly,

    q_U >= sum_t 2^-59 * Pr[ t = t*(CV) and the completion of t succeeds | CV uniform in t's set ]
        =  59,279,520 * 2^-59 * E[I],

where the expectation is over a uniform tuple t and a uniform CV in t's accepted set, and I is
the indicator that t is the first accepting tuple and the Section-8 completion (all completions
of t's SP, at the claimed caps) produces a pair that agrees through step 30. This is a
Karp-Luby estimator with the success event inside, so overlaps are handled exactly.

We sampled it exactly: a uniform table index, then A_-2 = kappa - v6 and A_-3 = lambda - v5 for
uniform v6 in V6 and v5 in V5 (by Lemma 1 this is uniform on the tuple's accepted set), and
uniform A_-4 and E_-1..E_-4. Then we scanned the key group for the first accepting tuple, ran
Section 8 with the claimed caps (2^18 x, 2^14 z), and checked both messages' compressions. From
1,000,000 samples: t was always the first accepting tuple (one sample had a second accepting
tuple), E[I] = 0.25687, and no completion failed its compression check. With a Hoeffding bound
at failure probability 10^-9, E[I] >= 0.25360. So

    q_U >= 59,279,520 * 0.25360 * 2^-59 >= 2^-35.1583.

This is a property of the fixed tables, measured by our sampling program (not
organizer-executed), under premise H-SAMPLING. Its random words are a ChaCha20 keystream (RFC
8439 block function, checked against the RFC test vector) keyed from a recorded seed.

**From q_U to the real algorithm.** The real CV = C(IV, M0) for uniform M0 is not uniform.
Premise H1 (Section 11): (a) q_D >= q_U / 2 and (b) Pr_D[prefix-valid] <= 2^4 * Pr_U[...].
Premise H-KEYHIT: the real key-hit probability is at most 1.2 times its uniform value.

- No success in N trials: probability <= exp(-N q_U / 2) = exp(-0.5600) < 0.5712.
- Key-hit cap: under U the hit probability is exactly 16,543,438 * 2^-32 = 2^-8.020, so
  E[hits] = 2^27.302. Under H-KEYHIT the mean is at most 1.2 * 2^27.302 < 2^27.57, and the cap
  2^28 is more than 1.34 times that. By a Chernoff bound the overflow probability is < 10^-6.
- Q cap: E[prefix-valid] <= N * 2^-33.179 * 2^4 < 70.8 under H1(b). By Markov, P(> 2^12) < 0.0173.

Success >= 1 - 0.5712 - 10^-6 - 0.0173 > 0.411 >= 0.39. The claim declares 0.39.

## 10. Cost (collision-frontier-v5 units; one 31-step compression = 1, other ops 1/2140)

Charged operations are on 256-bit RAM words. A 32-bit rotation costs 4 operations, and a
32-bit addition costs 2 (add, mask). Every bound below holds for every run.

**Online trials.** Per trial: one compression, two random words, block and result moves,
bitmap index, load, bit test, branch, loop control: <= 32 operations.
N * (1 + 32/2140) = 2^35.322 * 1.01495 < 2^35.344.

**Key hits.** Per hit: binary search over 2^25.82 entries (<= 26 * 12 operations) plus <= 168
tuples * <= 70 operations (W6 and W5 tests with precomputed per-tuple constants, W0..W4) <=
12,072 operations. H * 12,072 / 2140 < 2^30.50.

**Completions.** Per prefix-valid trial: <= 64 completions. Per completion, the c18 test (<= 30)
and, if it passes, <= 64 g tests (<= 12 each), <= 2^18 x steps (<= 70 each) and <= 2^14 z steps
(<= 60 each): <= 19,333,918 operations. Q * 64 * 19,333,918 / 2140 < 2^31.15.

**Final check.** 6 compressions.

**Preprocessing, exact counts from the run that built the tables:**

- Word sets: 2^32 words * <= 256 operations, plus S (2^32 bitmap words, and 42,467,328 * 64 *
  <= 12): < 2^40.1 operations.
- SP evaluations (search candidates, repairs, completions): 26,813,914,016 evaluations of the
  Section-5 derivation and checks, each <= 1,200 operations including candidate construction
  and the seen-hash: < 2^44.87 operations.
- Tuple enumerations: 728,809 calls, each <= 49,408 * 20 + 200 operations, plus 1,419,408,144
  W8 values passing (F7), each <= 512 * 20 + 80: < 2^43.80 operations.
- Table: sort and bitmap: < 2^34 operations.

Total < 4.874 * 10^13 operations, that is < 2.2776 * 10^10 units < 2^34.41.

**Base SPs (STP).** 715.1 CPU-seconds measured (user + sys of all 13 runs), charged at <= 2^24
units per CPU-second (premise H-CONV): 715.1 * 2^24 < 1.1998 * 10^10 units < 2^33.49.

**Advice (characteristic).** T_char <= 2^39.5 units (premise H-CHAR).

**Total.**

    term                         units (upper bound)
    T_char (H-CHAR)              7.7748 * 10^11   (2^39.5)
    base SPs (STP, H-CONV)       1.1998 * 10^10
    preprocessing (counted)      2.2776 * 10^10
    online trials                4.3592 * 10^10   (2^35.343)
    key hits                     1.5143 * 10^9
    completions                  2.3684 * 10^9
    final check                  6
    total                        8.5973 * 10^11  <  2^39.6452

`time_log2` = 39.65. `preprocessing_log2` = 39.57 bounds T_char + base SPs + counted
preprocessing = 8.1226 * 10^11 < 2^39.5632.

**Memory.** Table: 59,279,520 records of <= 12 words (32 bytes each) < 2^34.5 bytes. Bitmaps
(keys, V5, V6, G18, S): 5 * 2^29 bytes. SPs and completions < 2^28 bytes. The search's
seen-set: 2^29 bytes. STP peak resident memory, measured with getrusage(RUSAGE_CHILDREN) on
re-runs of M and of a cube: 120,536 kB and 101,204 kB. A re-run of M returned the identical
solution. Total < 2.64 * 10^10 bytes < 2^34.62; `memory_log2_bytes` = 35.

**Advice size.** The characteristic of Section 3: under 256 bytes;
`nonuniform_advice_log2_bytes` = 8.

## 11. Declared premises

**H1 (near-uniform chaining values; score-critical).** For CV = C(IV, M0) with uniform 512-bit
M0: (a) the per-trial success probability is at least half its value under uniform CV;
(b) the probability of a prefix-valid trial is at most 2^4 times its value under uniform CV.

- Evidence (Section 12): all full runs of the real algorithm on real 31-step chaining values. The
  32-bit key condition and the 41-bit key-plus-W6 condition match the uniform prediction to
  within sampling error. The 59-bit prefix-valid event and complete successes occur at rates
  consistent with the uniform prediction within the factor allowed.
- Runs 3-4 observed 54 prefix-valid events (59-bit condition) against 49.0 expected, and 14
  successes against 12.6 expected. Runs 1-2 observed 5 against about 10 expected. A deviation
  of a small factor at 59 bits cannot be excluded from these counts. That is why the factor 2
  is used, and it is consistent with all four runs.
- Sensitivity: with ratio rho in place of 1/2 the bound becomes 1 - exp(-1.1201 rho) - 0.0173.
  rho = 0.45 gives 0.379 (below 0.39); rho = 1 gives 0.656.

**H-CHAR (cost of the advice; score-critical).** All computation that produced the published
signed characteristic of Section 3 cost at most 2^39.5 units.

- Evidence: we re-ran the authors' public search script for 31-step SHA-256
  (`find_dc/find_dc_model_31_256.py`, repository github.com/Peace9911/sha_2_attack at commit
  6a9f35f, unmodified, STP 2.4.1 as above with CryptoMiniSat, 26 threads requested on 12
  hardware threads). It lowers a Hamming-weight bound by one per solver call, starting at 60.
  The calls for HW 60 down to 51 (the published characteristic's weight) all returned
  characteristics and took 32,357 CPU-seconds in total. At 2^24 units per CPU-second that is
  2^38.98 units; 2^39.5 is 1.43 times that.
- Limitation: the re-run outputs characteristics of the same shape (identical W16 and W18
  patterns, total message weight 48) but not the published one, which the authors obtained
  with their own (possibly longer) process, including a value-consistency model
  (`correct_dc_model_31_256.py`). Their actual effort is not published.
- Sensitivity: T_char = 2^40 gives a total of 2^40.11; 2^41 gives 2^41.06.

**H-CONV (CPU time to units; supporting).** One CPU-second of the solver runs used here costs at
most 2^24 units, that is 2^35.06 word operations per second. For comparison, our scalar 31-step
compression, a dense ALU workload, runs at 2^22.3-2^22.4 compressions per CPU-second per thread
on this machine (an Intel Core i5-12450H). So 2^24 allows 3 times more work per second than the
densest code we measured. It only affects the STP terms: the base solves (2^33.49) and, through
H-CHAR's evidence, the characteristic. If one CPU-second were worth 2^25 units, the base term
would double and the total would be 2^39.67.

**H-KEYHIT (real key-hit rate; supporting).** For the real CV distribution, the probability that
A_-1 is a table key is at most 1.2 times its uniform value 2^-8.020. It is used only for the
key-hit cap term (< 10^-6).

- Evidence: run 3 observed 1,314,841,618 key hits against 1,314,755,000 expected (ratio
  1.00007), and run 4 observed 520,944,271 against 520,960,206 (ratio 0.99997). A 32-bit condition on one output word is sampled
  directly at very high counts.
- Sensitivity: the cap fails with probability above 10^-6 only if the ratio exceeds about 1.45.

**H-SAMPLING (pseudorandom sampling; score-critical through q_U).** The ChaCha20 keystream
words used by our estimator of E[I] (Section 9) behave as independent uniform samples, so the
Hoeffding bound applies.

- Evidence: ChaCha20 is a standard stream cipher, and no distinguisher is known. Our
  implementation matches the RFC 8439 test vector. Independent seeds gave consistent results:
  E[I] = 0.25677 and 0.25687 over two 10^6-sample runs, one of them with a splitmix generator.
- Sensitivity: the success bound falls below 0.39 only if E[I] < 0.2369, that is 7.8% below the
  estimate and about 45 standard errors (4.4 * 10^-4 each) away.

## 12. Evidence

**Full runs of the algorithm** (our runs, 12 threads, AVX2 8-lane compression, first blocks from
per-thread streams seeded from the OS: splitmix in runs 1-3, ChaCha20 in run 4; identical prefix
and completion code):

| Run | Table | Trials | Key hits (expected) | Prefix-valid | Successes |
| --- | --- | --- | --- | --- | --- |
| 1 | family from the published SP, 7.8M tuples | 1.258e10 | 5,691,398 (5.69e6) | 1 | 1 |
| 2 | same | 7.211e11 | 326,091,014 (3.2609e8) | 4 | 2 |
| 3 | this package's tables (Section 6) | 3.413e11 (2^38.31) | 1,314,841,618 (1.31476e9) | 34 (exp. 34.3) | 9 (exp. 8.8) |
| 4 | same, claimed caps, ChaCha20 blocks | 1.353e11 (2^36.98) | 520,944,271 (5.20960e8) | 20 (exp. 13.9) | 5 (exp. 3.6) |

Runs 1-2 used an earlier table built from the published starting point, which is not part of
this algorithm. They are evidence for H1 because the matching and completion code is the same.
Runs 3 and 4 are the algorithm of this package. Each ran for one hour, past its first success,
to collect statistics. Run 3 used completion caps of 2^20/2^20 and splitmix-seeded blocks. Run
4 used exactly the claimed caps 2^18/2^14 and ChaCha20 blocks. Together they observed 54
prefix-valid trials against 49.0 expected, and 14 collisions against 12.6 expected. In run 3, the 41-bit event (key hit and W6 in V6) was
counted for every tested tuple: 9,208,177 passes in 4,711,490,502 tests, expected 1/512 of them under
uniform A_-2 (9,202,130; ratio 1.0007). Run 4: 3,644,467 passes against 3,645,968 expected.

**Certificates** (`certificates/`). Collisions produced by the full algorithm from random
first blocks, each verified with the organizer's `verifier.hash_functions.digest(m, "sha256",
31)`. In each pair the two messages differ, have equal 31-step digests, and do not collide at
32 steps.

- `found-1`: 31-step digest `429b81bff75c0eedf88ba58dca620c7055376189815bd4dfc5df36dde99c5137` (run 3)
- `found-2`: 31-step digest `c5f0bbfff7ce66cdfd3816a1100bfaa56f7c1352152d813e03e09ff6f35cde5f` (run 3)
- `found-3`: 31-step digest `33258f6423132b974c204b5d9a4a37253a994199335d976c390d097c90c4a572` (run 3)
- `found-4`: 31-step digest `21b967a1e4d29dbbd79249f077c43cbf7e0fd5317a54249a65e1a91b62aeac72` (run 3)
- `found-5`: 31-step digest `52543cae1517174ab9fcf4de209fa61b975c07d05711884bd6351ffe8c19d5d6` (run 3)
- `found-6`: 31-step digest `0d44cba8c6e08c2c7c85d739b284961b6dff4690e768d42f9526b2288f6d46cf` (run 3)
- `found-7`: 31-step digest `da61e84c04c883524dac0aee3326d0fb5f361fc94ebb61f9fccc4f2574ccfd9e` (run 3)
- `found-8`: 31-step digest `48906e53f331dccf3c39be6ce7ff7d73e520b84e3af5a3eeef54203d8012f7e1` (run 3)
- `found-9`: 31-step digest `cd239c46a74c34074fe5aac65adba479a547406c1847ac0e3350559ca1e94ebc` (run 3)
- `found-10`: 31-step digest `369ef5e307ec6675a3aa365b1346284f00a3ca07922a54fdb6f32735789b3b9e` (run 4)
- `found-11`: 31-step digest `f2d0b06e229c8f92aeb952a65e758d9c956298418d64042fd5f183d3d42cd700` (run 4)
- `found-12`: 31-step digest `7a83382d08e2eda32494a52202968dcb9556677c5c162265d35cef9630b66ed3` (run 4)
- `found-13`: 31-step digest `075ba19e5f20c9b24587f28110adc6313db95456fc4d9e2b3b95d1360f005212` (run 4)
- `found-14`: 31-step digest `550da68f4b62633e251a0e01158ec45d8b63f9d3c635c9c4b91f9579c0045776` (run 4)

**Organizer experiment `completion`** (`experiments/completion.py`, `python-message-pairs-v1`,
event `full-collision`). For each organizer seed, the program takes one of three found prefixes
(trial mod 3), recomputes both step-12 states from M0 and W0..W12, and runs Section 8 with
offsets derived from the seed by SHAKE-256. It returns the two messages, which the organizer
re-hashes. It uses exactly the claimed caps (2^18 x, 2^14 z). Locally, 256 seeds gave 256 full
collisions in 0.5 s. It does not run the first-block search.

## 13. Scope and limitations

- The characteristic and the attack structure are published cryptanalysis. This package
  contributes an accounting in which starting points are generated by a stated, measured
  procedure, plus the local-search family and the multi-completion step that lower the online
  cost.
- The score rests on H-CHAR, a bound on work done by others. Without it, the measured part of
  the algorithm (Sections 5-10) costs under 2^36.3 units.
- The success probability rests on H1, H-KEYHIT, and one jointly sampled table statistic E[I]
  with stated confidence (H-SAMPLING). The time bound holds for every run.
- Development cost is not charged: the solver formulations we tried before model M (about
  99,000 CPU-seconds of exploratory solver runs) and the earlier table built from the published
  starting point are not part of the algorithm. They are reported here for transparency.
- A passing exploratory review is an AI screening result, not a proof and not human acceptance.
