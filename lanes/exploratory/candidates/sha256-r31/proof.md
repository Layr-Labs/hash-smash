# SHA-256 reduced to 31 steps: a two-block collision generator whose characteristic, starting points and tables are all produced and measured by the algorithm itself

Track `sha256-r31-exploratory`, target `sha256-r31-prefix-v1`, cost model `collision-frontier-v5`
(C = 2140), policy `paired-lanes-v1`, exploratory lane.

## 1. Claim and summary

Claim: a randomized algorithm that outputs two distinct 128-byte messages with equal 31-step
SHA-256 digests with probability at least 0.39 over its own coins, with total charged time below
2^39.339 target-compression units in every run (`time_log2` = 39.34). Memory is below
2^35 bytes.

The attack structure is the published two-block 31-step attack: a local collision in W5..W9, W16
and W18 (Mendel, Nad and Schlaeffer, EUROCRYPT 2013; Li, Liu and Wang, EUROCRYPT 2024; Li, Liu,
Wang, Dong and Sun, ASIACRYPT 2024). **No published characteristic, starting point or colliding
pair is used.** Every input is produced by the algorithm's preprocessing, and its cost is
measured and charged:

1. **Characteristic and base point (Section 3).** These form the algorithm's only stored advice
   (under 256 bytes). They were produced once, by a recorded and measured computation: the
   authors' public value-consistent characteristic model (`correct_dc_model_31_256.py`) solved
   with STP over nine calls, three weight-constrained variants, and an evaluation of every
   candidate with our starting-point model. Candidate "257" was selected, and its base starting
   point solved. The whole one-time computation is charged as advice construction: 6829.6
   CPU-seconds of solver work at a hardware bound (premise H-CONV), plus our counted evaluation
   programs. Because the advice is stored, the solver's nondeterminism does not affect any run of
   the algorithm.
2. **Starting points (Sections 5-6).** A bit-vector model of all starting-point conditions is
   solved once (46 s), and a deterministic local search grows the result to 160,000 starting
   points with 1,161,880 table tuples. Every operation is counted.
3. **A better free constant.** The constant c5 (the s0-difference of W5) is not fixed by the
   characteristic. Choosing c5 = 10027e21 makes W5 lie in a set of 9,211,952 words instead of
   about 2^14, so each table tuple accepts 2^9 times more chaining values. The cost is a sparser
   final filter, which up to 64 completions per starting point partly compensate.

Per trial, under a uniform chaining value, the success probability is at least 2^-36.44
(Section 9; an exact, overlap-correct estimate with a Clopper-Pearson bound). The online phase
is N = 96 * 2^30 = 2^36.585 trials.

Evidence: the full algorithm, run on one 12-thread laptop CPU, found 3 new collisions from random first blocks in 2^37.56 trials (228 prefix-valid trials against 229.4 predicted). Every found pair is an
organizer-verified certificate. An organizer-run experiment re-completes found prefixes from
fresh seeds at the claimed caps.

`baseline_improved` names the organizer's nominal reference `sha256-r31-nominal-v2`, as the
schema requires. Comparison with the Yukon incumbent is left to Yukon.

## 2. Target and notation

All words are 32 bits, `+`/`-` are modulo 2^32, `>>>` is rotation right, `>>` is shift right.

    S0(x) = (x>>>2) ^ (x>>>13) ^ (x>>>22)      S1(x) = (x>>>6) ^ (x>>>11) ^ (x>>>25)
    s0(x) = (x>>>7) ^ (x>>>18) ^ (x>>3)        s1(x) = (x>>>17) ^ (x>>>19) ^ (x>>10)
    Ch(e,f,g) = (e & f) ^ (~e & g)             Maj(a,b,c) = (a & b) ^ (a & c) ^ (b & c)

C(H, M) expands W16..W30 by W[t] = s1(W[t-2]) + W[t-7] + s0(W[t-15]) + W[t-16], runs steps
t = 0..30 with the standard constants K[0..30] at their original indices, and adds the working
state to H. The hash uses FIPS 180-4 padding, the standard IV, and all eight output words. This
is the organizer profile.

Write A_t, E_t for the new a and e after step t:

    E_t = A_{t-4} + E_{t-4} + S1(E_{t-1}) + Ch(E_{t-1},E_{t-2},E_{t-3}) + K[t] + W[t]        (1)
    A_t = E_t - A_{t-4} + S0(A_{t-1}) + Maj(A_{t-1},A_{t-2},A_{t-3})                          (2)

The chaining value entering a block is (A_-1, A_-2, A_-3, A_-4, E_-1, E_-2, E_-3, E_-4).
Output: m = M0 || M1 and m' = M0 || M1' (128 bytes each), hashed as M0, M1 or M1', and the
common padding block. M1' = M1 + (d5..d9) in words 5..9. Primed quantities belong to M1', and
dX = X' - X.

## 3. Advice and its one-time construction P0 (measured)

**P0.1 (characteristic candidates).** Run the unmodified `correct_dc_model_31_256.py` from
github.com/Peace9911/sha_2_attack (commit 6a9f35f) with STP 2.4.1 (official binary
`stp-2.4.1-linux-amd64`, SHA-256 a9c0eb78...97d57e) and CryptoMiniSat, 26 threads. The script
issues the same query repeatedly. Each call returns a characteristic, and the multithreaded
solver returns different ones. We let it make 1 call, and later 8 more. We also ran a driver that
adds HW(dE5) + HW(dE6) <= L to the same model, for L = 10, 16 and 22; all three were
unsatisfiable. Measured CPU (user + sys): 581.8 s, 4331.2 s and 1291.8 s.

**P0.2 (evaluation and selection).** For each of the 9 candidates: choose c5 by sampling (Section
4), enumerate the word sets, solve the starting-point model of Section 5 (418.2 s of STP CPU for
the 8 later candidates, 74.8 s for the first, including 12 cube variants), and run the local
search of Section 6 capped at 400 starting points. Then select the candidate with the most
tuples per starting point. Candidate 257 was selected (2484 tuples in 400 starting points; the
others had 4-2572). We also tried 24 cube variants of 257's model (131.8 s). Our own C programs
in this phase executed 20,575,846,502 starting-point evaluations, 186,598 tuple enumerations
with 1,321,057 passing W8 values, and 9 exhaustive word-set passes, under 3.65 * 10^13
operations in total.

**Charge (once, as advice construction).** All STP work: 6829.6 CPU-seconds at <= 2^26
units per CPU-second (H-CONV), 4.5833e+11 units. Own programs: 1.7051e+10 units.
P0 was executed once, and its outputs are stored as advice: the characteristic below, c5, and
the base point B0 (Section 5), under 256 bytes in total. The online algorithm and P1 are
deterministic given the advice, so the time bound of Section 10 holds for every run. The cost of
P0 is the recorded cost of that one execution.

**The selected characteristic (257).** Message differences: d5 = 00000ffa, d6 = ffe077ef,
d7 = 4fefa9fa, d8 = d8011100, d9 = 00008004; d16 = d9, d18 = -d9, no other message-word
difference. State differences used as constants: dE6 = 000fc40a, dE7 = 0ddfdffb,
dE8 = 3e707950, dA9 = 0, dA10 = d9.

Signed patterns: `xor` is X ^ X', and `n` is the set of bits where X = 1 and X' = 0. Bits of X
at positions in `xor` are therefore fixed: equal to `n` there.

     t   A xor     A n       E xor     E n
     5   0000100a  00000008  000ff7fe  0007f402
     6   00000000  00000000  0070cc1e  0030840a
     7   12201003  02201003  0de0e007  00008006
     8   00000000  00000000  42b18ad0  022088c0
     9   00000000  00000000  00002004  00000004
    10   00008004  00000000  f01fbffc  000f9ffc
    11   00000000  00000000  1040000c  0040000c
    12   00000000  00000000  00008004  00008004
    W7   50105a0e  0010580a      W8   58011100  40000000

## 4. Word sets (exact enumeration over all 2^32 words)

    V5  = { w : s0(w + d5) - s0(w) = c5 }             c5 = 10027e21
    V6  = { w : s0(w + d6) - s0(w) = -d5 }            V7 = { w : s0(w + d7) - s0(w) = -d6 }
    V8  = { w : s0(w + d8) - s0(w) = -d16 - d7 }      V9 = { w : s0(w + d9) - s0(w) = -d8 }
    G16 = { w : s1(w + d16) - s1(w) = d18 }           G18 = { w : s1(w + d18) - s1(w) = -c5 }
    S   = { c : some g in G16 has s1(g) + c in G18 }

Sizes: |V5| = 9,211,952, |V6| = 8,388,608, |V7| = 512, |V8| = 49,152, |V9| = 35,921,920,
|G16| = 64, |G18| = 155,648, |S| = 7,297,024.

With W5..W9 in V5..V9, W16 in G16 and W18 in G18, the expansion has exactly d16 = d9 and
d18 = -d9, and no other difference in W17..W30 (W20: c5 - c5 = 0; W21: -d5 + d5; W22: -d6 + d6;
W23: d16 + (-d16 - d7) + d7; W24: -d8 + d8; W25: d18 + d9).

**Choice of c5.** c5 is free: any value works if V5 and G18 are nonempty. We chose it by sampling
2^24 words and maximizing |V5| * (coverage of S). This selection is part of P0.2.

## 5. Starting points and the base point

A starting point (SP) is F = (A5..A8, E5..E12) of message 1. A1..A4 come from (2) at steps
8..5. A9..A12 come from (2), and W9..W12 from (1) solved for W. For message 2: A'_t = A_t for
t <= 4, E'_5 = E5 + d5, E'_6 = E6 + dE6, E'_7 = E7 + dE7, E'_8 = E8 + dE8, A'_5..A'_8 from (2),
and E'_9..E'_12, A'_9..A'_12 from (1) and (2) with W'_9 = W9 + d9 and W'_10..12 = W10..12.

**SP conditions** (exact 32-bit equations):

    (P3)   E'_8 - E_8 = [S1(E'_7) - S1(E_7)] + [Ch(E'_7,E'_6,E'_5) - Ch(E_7,E_6,E_5)] + d8
    (A9..12) A'_9 - A_9 = dA9,  A'_10 - A_10 = d9,  A'_11 = A_11,  A'_12 = A_12
    (W9)   W9 in V9
    (E13)  A_9 + E_9 + S1(E_12) + Ch(E_12,E_11,E_10) = (same with primes)
    (A13)  -A_9 + S0(A_12) + Maj(A_12,A_11,A_10) = (same with primes)

A **tuple** is (W7, W8) in V7 x V8 with

    E_4 = E_8 - A_4 - S1(E_7) - Ch(E_7,E_6,E_5) - K[8] - W8
    (F7)  Ch(E'_6,E'_5,E_4) - Ch(E_6,E_5,E_4) = (E'_7 - E_7) - [S1(E'_6) - S1(E_6)] - d7
    E_3 = E_7 - A_3 - S1(E_6) - Ch(E_6,E_5,E_4) - K[7] - W7
    (F6)  Ch(E'_5,E_4,E_3) - Ch(E_5,E_4,E_3) = (E'_6 - E_6) - [S1(E'_5) - S1(E_5)] - d6

Its key is A_-1 = E_3 - A_3 + S0(A_2) + Maj(A_2,A_1,A_0), with A_0 = E_4 - A_4 + S0(A_3) +
Maj(A_3,A_2,A_1). Implementation note: (F7) depends on E_4 only at the bits of m = E_6 ^ E'_6,
so the valid patterns are precomputed (2^HW(m) evaluations) and each W8 is tested with one
bit-extract and lookup. This gives output identical to direct testing; we checked it on 18,345
starting points.

**Model M.** A bit-vector formula over A5..A8, E5..E12, W7, W8 stating all derivations, all SP
conditions, one tuple, and the signed patterns of Section 3 for message 1 values and XOR
differences (190 assertions in STP's CVC language, generated by a script from the
characteristic). STP 2.4.1 (MiniSat backend, one thread) solves M in 46.0 CPU-seconds. The
solution is the base SP B0 = (3f2c2d98, 9c899694, 2a3191af, 1cdfada6, 15e7fc03, f8bb97cb,
a01183ae, b3289dc1, ade78a85, 072fdffc, aff2775f, 0e7fa01c). It is re-checked with the exact
conditions. This solve is part of P0.2's charged STP time.

## 6. Preprocessing P1: the starting-point family and completions

Breadth-first search from B0. Nodes are SPs identified by their first eight words. For each
node, in order:

1. Candidates: flip one or two bits (b1 <= b2) of one of the first eight words, for every word
   and bit pair in increasing order.
2. Skip if seen. Skip if (P3) or (A9) fails. Skip if the candidate has no tuple; tuples depend
   only on the first eight words.
3. Repair. If the SP conditions fail, try in order every 1- or 2-bit flip of one of E9..E12,
   then every single-bit flip in each of two of E9..E12. Take the first full SP, or drop.
4. Keep it as a new node. Stop when 160,000 nodes exist.

Result: 160,000 SPs, 1,161,880 tuples, 960,237 distinct keys, largest key group 24.

**Completions.** For each SP, a breadth-first search over 1- and 2-bit flips of E9..E12 collects
up to 64 full SPs with pairwise distinct W11. They share the first eight words and the tuples.
In total there are 1,067,608.

**Counted work in P1** (instrumented counters of the run that built the tables):
156,213,580,885 SP evaluations (<= 1,200 operations each); 167,823,508,480 (F7) pattern
evaluations (<= 30); 70,877,332 W8 scans (<= 49,152 * 8 + 64); 2,092,815,738 passing W8 values
(<= 512 * 20 + 80); 82,021,399 tuple-routine calls (<= 200 overhead); 2,254,788,096 completion
evaluations (<= 1,200); word sets (<= 2^32 * 300) and table (<= 2^34). Total
<= 2.4599e+14 operations = 1.1495e+11 units.

## 7. Online phase: trial and prefix

**Table.** Tuples sorted by key with their SP index and per-tuple constants, plus a bitmap of
the 2^32 keys.

**Trial.** Draw two fresh uniform 256-bit RAM words as the 512-bit block M0, and compute
CV = C(IV, M0). If the bitmap bit of A_-1 is 0, the trial ends. Otherwise, for each tuple with
key A_-1:

    E_2 = A_2 + A_-2 - S0(A_1) - Maj(A_1,A_0,A_-1)
    W6  = E_6 - A_2 - E_2 - S1(E_5) - Ch(E_5,E_4,E_3) - K[6];       if W6 not in V6: next
    E_1 = A_1 + A_-3 - S0(A_0) - Maj(A_0,A_-1,A_-2)
    W5  = E_5 - A_1 - E_1 - S1(E_4) - Ch(E_4,E_3,E_2) - K[5];       if W5 not in V5: next
    E_0 = A_0 + A_-4 - S0(A_-1) - Maj(A_-1,A_-2,A_-3);   W0..W4 from (1) at steps 0..4

The trial is then **prefix-valid**. Both messages reach the SP states after step 12, for any
completion of that SP: steps 0..4 are identical, E'_5 = E_5 + d5, (F6) and (F7) are steps 6 and
7 of message 2, (P3) is step 8, and steps 9..12 hold by construction.

Lemma 1. Under a uniform CV, a fixed tuple accepts with probability exactly
2^-32 * (|V6|/2^32) * (|V5|/2^32) = 2^-49.8649. The key matches with probability 2^-32;
W6 = const - A_-2 and W5 = const' - A_-3 are bijections. Different keys give disjoint sets.

Lemma 2. Under a uniform CV, conditioned on (A_-1..A_-4) and acceptance, (W0..W3) is uniform.
The map from (E_-4..E_-1) is a triangular bijection.

## 8. Completion of a prefix-valid trial

For each completion j of the matched SP (at most 64): c16 = W9 + s0(W1) + W0 and
c18 = W11 + s0(W3) + W2. If c18 is not in S, go to the next j. Otherwise this is a **completion
call**: for each g in G16 with s1(g) + c18 in G18, set W16 = g, W18 = s1(g) + c18 and
W14 = s1^-1(g - c16), then search x = E_13 and z = E_15 (fresh random offsets, step 9e3779b9):

    (C14)  dE_10 + Ch(x,E'_12,E'_11) - Ch(x,E_12,E_11) = 0
           y = A_10 + E_10 + S1(x) + Ch(x,E_12,E_11) + K[14] + W14,   y' = y + d9
    (C15)  E_11 + S1(y) + Ch(y,x,E_12) = E'_11 + S1(y') + Ch(y',x,E'_12)
    (C16)  E_12 + Ch(z,y,x) = E'_12 + Ch(z,y',x) + d9
           u = A_12 + E_12 + S1(z) + Ch(z,y,x) + K[16] + g
    (C17)  Ch(u,z,y) = Ch(u,z,y')

Then W13 = x - [A_9 + E_9 + S1(E_12) + Ch(E_12,E_11,E_10) + K[13]] and
W15 = z - [A_11 + E_11 + S1(y) + Ch(y,x,E_12) + K[15]]. After step 18 the states are equal
(dE_14 = dA_10 = d9, dE_18 = dE_14 + d18 = 0). With Section 4 the remaining steps and the
feed-forward are equal. Caps per call: 2^18 candidates x and 2^14 candidates z in total, and at
most 64 z per accepted x. The output is checked by hashing both full messages and requiring
m != m'.

## 9. Algorithm, caps and success probability

    N = N = 96 * 2^30 = 2^36.585 trials; caps: H = 2^25 key hits, Q = 2^19 prefix-valid trials,
    R = 2^15 completion calls. Exceeding a cap: FAIL. After N trials: FAIL.

All coins are fresh uniform 256-bit words. Trials are independent and identically distributed.

**q_U, exactly and overlap-correct.** For every CV accepted by some tuple, the algorithm tries
the tuples of its key in table order, so there is a unique first accepting tuple t*(CV). Hence

    q_U >= 1,161,880 * 2^-49.8649 * E[I],

where t is a uniform tuple, CV is uniform in t's accepted set, and I indicates that t is the
first accepting tuple and the Section-8 completion at the claimed caps succeeds (both messages'
compressions checked). We sampled exactly this: uniform table index, then A_-2 = kappa - v6 and
A_-3 = lambda - v5 for uniform v6 in V6 and v5 in V5, and uniform A_-4 and E_-1..E_-4. Two runs
of 10^6 and 4 * 10^6 samples gave 9,741 and 38,852 successes: 48,593 of 5,000,000, so
E[I] = 0.009719. No completion failed its check. The exact one-sided Clopper-Pearson bound at
alpha = 10^-9 is E[I] >= 0.009458 (premise H-SAMPLING). So q_U >= 2^-36.4411.

**Real distribution.** Premise H1: (a) q_D >= q_U / 2; (b) Pr_D[prefix-valid] <= 2^4 times its
uniform value; (c) the expected number of completion calls per trial is at most 2^4 times its
value under uniform CV. Premise H-KEYHIT: the real key-hit rate is <= 1.2 times uniform.

- No success: <= exp(-N q_U / 2) = exp(-0.5524) = 0.5756.
- Q cap: E[prefix-valid] <= N * 1,161,880 * 2^-49.8649 * 2^4 = 1869; by Markov,
  P(> 2^19) <= 0.0036.
- R cap: under uniform CV, given a prefix-valid trial, each completion's c18 is uniform
  (Lemma 2). So the uniform-CV expectation of completion calls is at most N * (prefix-valid
  probability) * 64 * |S|/2^32. Under H1(c), E[completion calls] <= 203.2, and
  P(> 2^15) <= 0.0062.
- H cap: E[key hits] <= 1.2 * N * 960,237/2^32 < 2^24.72. The cap 2^25 is 1.2 times
  that, and the Chernoff tail is < 10^-6.

Success >= 1 - 0.5756 - 0.0098 - 10^-6 = 0.4147 >= 0.39. The claim declares 0.39.

## 10. Cost (units; one 31-step compression = 1; other 256-bit word operations 1/2140)

Rotations cost 4 operations and 32-bit additions 2. All bounds hold for every run.

    term                                         units
    P0 solver work (6829.6 CPU-s * 2^26)        4.5833e+11
    P0 own evaluation programs                   1.7051e+10
    P1 family, completions, sets, table          1.1495e+11
    online trials N * (1 + 32/2140)              1.0462e+11
    key hits (H * 1992 operations)              3.1234e+07
    prefix-valid and completion caps             2.9654e+08
    final check (6 compressions, <= 2140 ops)    7
    total                                        6.9528e+11  <  2^39.3388

Per trial: one compression plus <= 32 operations (two random words, moves, bitmap test, loop).
Per key hit: binary search (<= 26 * 12) plus <= 24 tuples * 70. Per prefix-valid trial: <= 100
+ 64 * 30 (W0..W4 and the c18 tests). Per completion call: <= 64 * 12 + 2^18 * 70 + 2^14 * 60.

`time_log2` = 39.34. `preprocessing_log2` = 39.11 (P0 + P1 = 5.9033e+11 <
2^39.1027).

**Memory.** Table: 1,161,880 records of <= 12 RAM words of 32 bytes each (384 bytes); five 2^32-bit bitmaps; SPs and
completions (1,227,608 * 48 bytes); the search's seen-set (2^31 slots of 8 bytes); STP peak RSS
(measured, < 120 MB). Total < 2^34.25 bytes; `memory_log2_bytes` = 35.

**Advice.** The characteristic of Section 3 (message differences, three state-difference
constants, 18 signed pattern pairs), c5, and B0: under 256 bytes; `nonuniform_advice_log2_bytes`
= 8. Its construction cost is the P0 term.

## 11. Declared premises

**H-CONV (CPU time to units; score-critical).** One CPU-second of the STP runs costs at most 2^26
units (2^37.06 primitive 256-bit word operations).

- Basis: the runs used an Intel Core i5-12450H. Its maximum clock is 4.4 GHz, and its cores
  retire at most 8 instructions per cycle, so a CPU-second retires at most 3.52 * 10^10
  instructions. The premise is that a 256-bit word RAM simulates the average x86-64
  instruction executed by STP/CryptoMiniSat (scalar integer, load/store, branch) in at most 4
  word operations.
- For comparison, our scalar 31-step compression runs at 2^22.3-2^22.4 compressions per
  CPU-second, about 2^33.5 word operations per second. The premise allows 12 times more.
- Sensitivity: at 2^27 units per CPU-second the total would be 2^40.07.

**H1 (near-uniform chaining values; score-critical).** For CV = C(IV, M0) with uniform M0:
(a) the per-trial success probability is at least half of its value under uniform CV, and
(b) the prefix-valid probability is at most 2^4 times its uniform value, and (c) the expected
number of completion calls per trial is at most 2^4 times its uniform-CV value.

- Evidence (Section 12): real runs of this algorithm. one run of 2^37.56 trials. Observed against expected: 32-bit key hits 45,267,325 vs 45,263,296; the 41-bit event 107,435 vs 106,986; prefix-valid trials 228 vs 229.4; completion calls 3 vs 2.60; collisions 3 vs 2.23. These counts cannot exclude a small-factor deviation at the full success event, which is why the factor 2 (and 2^4 for (b) and (c)) is used.
- Sensitivity: with rho in place of 1/2, success >= 1 - exp(-1.1048 rho) - 0.0098;
  rho = 0.45 gives 0.382, rho = 1 gives 0.659.

**H-KEYHIT (supporting).** The real key-hit rate is at most 1.2 times its uniform value
960,237/2^32. Observed 45,267,325 key hits against 45,263,296 expected (ratio 1.00009). It is used only for the H cap.

**H-SAMPLING (score-critical through q_U and the H1 evidence).** The ChaCha20 keystream words
(RFC 8439 block function, checked against the RFC test vector) behave as independent uniform
samples. This applies to the E[I] sampler, so the Clopper-Pearson bound holds, and to the first
blocks of the evidence run, so its counts are samples of the real distribution of C(IV, M0). Sensitivity: the success bound falls
below 0.39 only if E[I] < 0.00874.

## 12. Evidence

**Full run of this algorithm** (our run: 10 threads, AVX2 8-lane compression, ChaCha20-generated
first blocks (H-SAMPLING), the claimed caps, the tables of Section 6):

| Quantity | Observed | Expected under uniform CV |
| --- | --- | --- |
| trials | 202,454,576,168 (2^37.56) | - |
| key hits (32-bit event) | 45,267,325 | 45,263,296 |
| key hit and W6 in V6 (41-bit event), over 54,776,717 tuple tests | 107,435 | 106,986 |
| prefix-valid trials (Lemma 1 measure) | 228 | 229.4 |
| completion calls (c18 in S) | 3 | 2.60 |
| collisions | 3 | 2.23 |

Every completion call completed, and each output was checked. The expected values are computed
from the table: N_run * 960,237/2^32, N_run * 1,161,880 * 2^-49.8649, the sum over the 228
observed prefix-valid trials of (completions of the matched SP) * |S|/2^32, and the prefix-valid
expectation times E[I].

**Certificates** (`certificates/`): collisions found by the full algorithm from random first
blocks, each verified with `verifier.hash_functions.digest(m, "sha256", 31)`. They are
distinct, have equal 31-step digests, and are not 32-step collisions.

- `found-1`: 31-step digest `96145d3645b1c7e23baf8d6bb39bc983ea757f2db1c3cffb2d61190efcc04351`
- `found-2`: 31-step digest `e1a16a1cdc926f0db27a7ef176cea2b64b90e53f51babf7d39655d319da46234`
- `found-3`: 31-step digest `8458e9ed3b6b7373ba40b21e53b9a67b621beff51106e58e93d3699c8163c924`

**Organizer experiment `completion`** (`python-message-pairs-v1`, event `full-collision`): for
each organizer seed, re-run Section 8 at the claimed caps on one of the found prefixes, with
offsets derived from the seed by SHAKE-256, and return the two messages for re-hashing. It does
not run the first-block search.

## 13. Scope and limitations

- The attack structure is published cryptanalysis. This package contributes an accounting in
  which the characteristic, starting points and tables are produced by stated, measured
  procedures, plus the c5 choice, the local-search family and multiple completions.
- The dominant term is solver CPU time converted under H-CONV, a hardware-derived bound and not
  an instruction count. No instruction counters were available.
- The success probability rests on H1, H-KEYHIT and H-SAMPLING. The time bound holds for every
  run.
- Not charged, but reported: an earlier, unused run of the authors' `find_dc_model_31_256.py`
  (32,357 CPU-s; its outputs admitted no starting point), earlier solver formulations, and
  re-runs of the same deterministic search that were aborted by our implementation bugs. None of
  these produced an input to the algorithm.
- A passing exploratory review is an AI screening result, not a proof and not human acceptance.
