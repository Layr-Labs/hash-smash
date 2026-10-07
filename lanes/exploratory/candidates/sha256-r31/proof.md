# sha256-r31: replaying the published 31-step collision with its whole construction charged

## 1. Claim

Track `sha256-r31-exploratory`, target `sha256-r31-prefix-v1` (ordinary collision, SHA-256 steps
0..30 on every padded block, standard IV, FIPS padding, all eight digest words), cost model
`collision-frontier-v5` with C = 2140 (one 31-step compression = 1 unit, any other 256-bit word
operation = 1/2140 unit), review policy `paired-lanes-v1`, exploratory lane.

The scored program is a deterministic replay (Section 3): it outputs one stored pair of distinct
128-byte messages that collide under sha256-r31 (Section 4). It draws no random coins, so its success
probability is exactly 1. The stored pair is nonuniform advice, so the whole work needed to build it
is charged once as preprocessing and is part of total time (Sections 7 and 8).

| field | value | where |
|---|---|---|
| time_log2 | 40.76 | ledger total 2^40.7532 plus slack, Section 8 |
| preprocessing_log2 | 40.76 | construction terms L1-L5, Section 8 |
| success_probability | 1 | no coins, Section 3 |
| nonuniform_advice_log2_bytes | 9 | 256-byte pair plus 32-byte digest, Section 10 |
| memory_log2_bytes | 32 | reported only, Section 10 |

One score-critical heuristic is declared, H1 (Section 9). Two supporting heuristics, H2 (memory) and H3 (C3 acceptance cross-check), are declared in Section 9b. Neither affects the score.

This package replaces our earlier package for this track, which was refuted for two reasons: the
generation algorithm was not specified, and the cost and success premises were not named as
heuristics. Section 7 now specifies every construction step with exact predicates, Section 8 prices
every term, and Section 9 names the only premise the score rests on.

## 2. Target, written out

All words are 32-bit; `+` and `-` are modulo 2^32; ROTR is right rotation.

    S0(x) = ROTR(x,2) ^ ROTR(x,13) ^ ROTR(x,22)      s0(x) = ROTR(x,7) ^ ROTR(x,18) ^ (x >> 3)
    S1(x) = ROTR(x,6) ^ ROTR(x,11) ^ ROTR(x,25)      s1(x) = ROTR(x,17) ^ ROTR(x,19) ^ (x >> 10)
    IF(x,y,z) = (x & y) ^ (~x & z)                   MAJ(x,y,z) = (x & y) ^ (x & z) ^ (y & z)

Schedule: W[0..15] are the block words (big-endian); W[t] = s1(W[t-2]) + W[t-7] + s0(W[t-15]) + W[t-16]
for t = 16..30. Constants K[0..30] are the first 31 FIPS 180-4 constants.

We write the compression in the one-register form used by the source papers. The incoming chaining
value (a,b,c,d,e,f,g,h) is renamed (A[-1],A[-2],A[-3],A[-4],E[-1],E[-2],E[-3],E[-4]). For i = 0..30:

    E[i] = A[i-4] + E[i-4] + S1(E[i-1]) + IF(E[i-1],E[i-2],E[i-3]) + K[i] + W[i]
    A[i] = E[i] - A[i-4] + S0(A[i-1]) + MAJ(A[i-1],A[i-2],A[i-3])

This is the standard step: E[i] = d + T1 and A[i] = T1 + T2. The output chaining value is
(a+A[30], b+A[29], c+A[28], d+A[27], e+E[30], f+E[29], g+E[28], h+E[27]). The IV is the standard
one, used once. A 128-byte message is followed by one FIPS padding block (0x80, zeros, bit length
1024), so it is hashed as three compressions. The digest is the final chaining value, big-endian.
This matches `verifier/hash_functions.py:digest` with ("sha256", 31).

## 3. The scored program (online replay)

R1. Read the stored advice: two 128-byte strings P and P' (Section 4).
R2. Compute sha256-r31(P) and sha256-r31(P'): three compressions each.
R3. If P != P' and the digests are equal, output (P, P'). Otherwise output nothing.

R3 always outputs the pair, because the organizer verifier confirms the relation for these exact bytes
(certificate `published-31step-pair`). The program uses no randomness. Its probability space is a
single point, so success probability is 1 for the fixed target. It is not a generator of new pairs,
and no amortisation over several targets or runs is claimed.

## 4. The stored pair

Both messages share the first block M0 and differ only in words 5..9 of the second block.

    M0  : 8ce3f805 5c401aed 579e5f7f bc3116cb ca189b3c eb75f04c 958f0a0e 7760b082
          dcd5027d 32260ad6 7b12b659 eee66518 ad7f88dd f8ad20bb 7ae40ffd 21609249
    M1  : 9abdeb1b 1f195f41 5a7210c1 55614f13 a2269dd1 be888a61 359257d4 adf3737b
          9f0484a6 eb830a58 66add94a 9669232d 45271fa5 b8f69585 428bbce3 0703b904
    M1' : 9abdeb1b 1f195f41 5a7210c1 55614f13 a2269dd1 be887a67 35b2dfc5 fde32975
          c70595a6 eb838a5c 66add94a 9669232d 45271fa5 b8f69585 428bbce3 0703b904

P = M0||M1 and P' = M0||M1'. Recomputed values:

    CV1 = compress31(IV, M0)   = c0a93f38 23b02f67 2f718088 03dfb329 7eaa51b9 0e2dd226 107e021b 70b1ac59
    compress31(CV1, M1) = compress31(CV1, M1')
                               = ff558659 2977dd01 54638843 35f8de84 a3336841 f4f476f2 7c571548 f7025605
    sha256-r31(P) = sha256-r31(P') = 55fdfb37efcbd086e19c3de0f72596300a3acdf48da5b1d0450a592bb2869fcd

The pair does not collide at 32 or 64 steps. It is the colliding pair printed by Li, Liu, Wang, Dong
and Sun (ASIACRYPT 2024, presentation slide 15).

## 5. The differential characteristic

Each cell describes one bit (bit 31 on the left) of a word in copy P and copy P':
`=` the bits are equal; `0` / `1` both bits equal that value; `u` the bit is 0 in P and 1 in P';
`n` the bit is 1 in P and 0 in P'. Rows are the step index i. Rows -4..2, 17 and 19..30 are all `=`
in every column and are not listed.

    i  | A[i]                             | E[i]                             | W[i]
    3  | ================================ | ==========================10==== | ================================
    4  | ================================ | ============0===0=========01===0 | ================================
    5  | ===================n=unnnnnnn=n= | 000111010001111110nu=11111unnnu1 | ================nuuu=======0=uu=
    6  | ========n======================u | 101011=11==0n0==u11110==1110011n | ==========u=====u===u======n===u
    7  | ===u===n==n========n=========n=u | un0u1100n=01u11111001u1=n110u10n | =u=u=======n=====n=nu=n=====nun=
    8  | =============================n== | 1u01un0u0=1=1=11n=0=u0=001001u0= | =u=nn==========u===u===u==1=====
    9  | ================================ | 01100001110=0=010===00=11101u0=1 | ================u==========1=u==
    10 | ================u============u== | =1n1uuuuu0100=1un0=10unnnnnnn010 | ================================
    11 | ================================ | =01u1010uu1==11100===1000001n=0= | ================================
    12 | ================================ | ==110001=11====1n====0011110n=0= | ================================
    13 | ================================ | ===0====01======1=============== | ================================
    14 | ================================ | ================u===========0u== | ================================
    15 | ================================ | ================0============1== | ================================
    16 | ================================ | ================1============1== | =============unnnunnnnnnnnnnnn==
    18 | ================================ | ================================ | ==============1=n=0==========n==

The table has 300 non-`=` cells: 180 value cells (`0`/`1`) and 120 signed-difference cells
(`u`/`n`). Per row, (A, E, W) cells are: 3:(0,2,0) 4:(0,5,0) 5:(10,31,7) 6:(2,25,5) 7:(6,30,10)
8:(1,25,7) 9:(0,25,3) 10:(2,29,0) 11:(0,24,0) 12:(0,19,0) 13:(0,4,0) 14:(0,3,0) 15:(0,2,0)
16:(0,2,17) 18:(0,0,4). Evaluating every one of the 300 cells on the pair of Section 4 (second block,
chaining value CV1) gives zero violations.

Modular differences X' - X implied by the table and observed on the pair:

    W:  d5 = fffff006  d6 = 002087f1  d7 = 4fefb5fa  d8 = 28011100  d9 = 00008004
        d16 = 00008004 d18 = ffff7ffc  (every other W[t], t <= 30, has difference 0)
    A:  A5 fffff006  A6 ff800001  A7 0edfeffd  A8 fffffffc  A10 00008004
    E:  E5 fffff006  E6 fff87fff  E7 4f880387  E8 44ff8804  E9 00000008
        E10 ef808008 E11 10bffff8 E12 ffff7ff8 E14 00008004

The table is the published 31-step trail (ASIACRYPT 2024 presentation, slide 14), transcribed
cell by cell; rows 3 and 4 carry value conditions on E[3] and E[4] and are kept.

## 6. Why a pair that follows the table collides

6.1 Message expansion. Only W5..W9 differ in the block, by d5..d9. For t = 16..30 the difference of
W[t] follows from the recurrence. Every term not shown below has difference 0.

    t=16: W9 enters directly: dW16 = d9.                          No condition.
    t=18: s1(W16) term: dW18 = s1(W16+d9) - s1(W16).              Needs W16 in G16.
    t=20: s1(W18) and s0(W5) terms. This trail takes
          s0(W5+d5) - s0(W5) = d0018020 (W5 in V5) and
          s1(W18+d18) - s1(W18) = 2ffe7fe0 (W18 in G18); they cancel, so dW20 = 0.
    t=21: s0(W6) and W5 terms: needs s0(W6+d6) - s0(W6) = -d5 = 00000ffa      (W6 in V6).
    t=22: s0(W7) and W6 terms: needs s0(W7+d7) - s0(W7) = -d6 = ffdf780f      (W7 in V7).
    t=23: s0(W8), W16 and W7 terms: needs s0(W8+d8) - s0(W8) = -(d9+d7) = b00fca02 (W8 in V8).
    t=24: s0(W9) and W8 terms: needs s0(W9+d9) - s0(W9) = -d8 = d7feef00      (W9 in V9).
    t=25: W18 and W9 terms: d18 + d9 = 0.                          No condition.
    t=17, 19, 26..30: no term has a difference.

Here G16 = {w : s1(w+d9) - s1(w) = d18}. We enumerated all 2^32 words for each set:

    |V5| = 16384 = 2^14        |V6| = 8388608 = 2^23      |V7| = 512 = 2^9
    |V8| = 49408 (2^15.59)     |V9| = 35921920 (2^25.10)
    |G16| = 64                 |G18| = 42467328 (2^25.34)

Every element of V5, V6, V7 and G16 also matches the signed W-row of the table. For V8, V9 and G18
the words that also match the signed row number 8192, 33554432 and 33554432. Only the modular
difference of a W word enters the state update, so the modular sets are the exact requirements.
G16 consists of the 64 words (h << 28) | lo with h = 0..15 and lo in {031bbffc, 064bbffe, 09b3bffd,
0ce3bfff}. s0 and s1 are invertible GF(2)-linear maps (rank 32), which step C4 below uses.

6.2 State. With the expansion requirements met, W differs only at steps 5..9, 16 and 18. The table
has all-`=` rows for A[i], i >= 11, and for E[i], i >= 17. Step 18 cancels the E14 difference
+00008004 against dW18 = -00008004. Steps 19..30 have no difference in inputs, so A[27..30] and
E[27..30] are equal in both copies. Both copies start the second block from the same CV1, so their
second-block outputs are equal. The third (padding) block is identical, so the digests are equal.
This argument needs the table to hold. For the stored pair it does (Section 5), and the organizer
checks the collision itself directly.

## 7. The one-time construction that produced the stored pair

This is the two-phase framework of Li, Liu, Wang, Dong and Sun (ASIACRYPT 2024). The same authors
restate it as Steps 1-3 in ePrint 2026/1080, Section 3. We give each step with the exact predicates it
tests. The output of C5 is a pair like the one in Section 4, and the stored pair passes every
predicate below.

C0 (characteristic). Run the authors' SAT/SMT trail search with the message-difference positions
{5,6,7,8,9,16,18} fixed. It works in four stages: (1) minimise the weight of the W differences;
(2) minimise the E-difference weight in the tail; (3) minimise the A-difference weight; (4) fix the
signed trail and its value conditions. The output is the table of Section 5 and the constants d5..d18
and the sets of Section 6.

C1 (starting solutions). Use a SAT/SMT solver to find assignments to (A1..A12, E5..E12, W9..W12)
with P'-values given by the signed table, such that:
  (a) every cell of the table on these words holds;
  (b) the A-equation for i = 5..12 and the E-equation for i = 9..12 hold in both copies;
  (c) the step-8 and step-13 difference relations that involve only these words hold. For step 8,
      (E8'-E8) = (S1(E7')-S1(E7)) + (IF(E7',E6',E5')-IF(E7,E6,E5)) + d8, because A4 and E4 carry no
      difference. For step 13, E13 and A13 get difference 0;
  (d) W9 is in V9.
The tuple (A1..A4, E5..E8) of a solution is its starting point. Keep N_start solutions with distinct
starting points.

C2 (table). For each kept solution, run two loops.
  Loop 1: for W8 in V8, set E4 = E8 - A4 - S1(E7) - IF(E7,E6,E5) - K[8] - W8. Keep W8 if the row-4
  cells hold on E4 and if F7 holds:
  (E7'-E7) = (S1(E6')-S1(E6)) + (IF(E6',E5',E4) - IF(E6,E5,E4)) + d7.
  Then set A0 = E4 - A4 + S0(A3) + MAJ(A3,A2,A1).
  Loop 2: for each kept W8 and each W7 in V7, set E3 = E7 - A3 - S1(E6) - IF(E6,E5,E4) - K[7] - W7.
  Keep W7 if the row-3 cells hold on E3 and if F6 holds:
  (E6'-E6) = (S1(E5')-S1(E5)) + (IF(E5',E4,E3) - IF(E5,E4,E3)) + d6.
  Then set A[-1] = E3 - A3 + S0(A2) + MAJ(A2,A1,A0).
  Store the record (A[-1]; A0..A4, E3..E8, W7, W8, solution id), keyed by A[-1].
  We ran C2 exhaustively on the starting solution read off the stored pair. Of the 49408 values in V8,
  1632 survive loop 1, and loop 2 yields 16896 = 2^14.04 records. One of them is the stored pair's
  record: A[-1] = c0a93f38, A0 = 7535928e, E3 = 9f3c306a, E4 = 60e73dda, W7 = adf3737b,
  W8 = 9f0484a6. The published table of 2^19.8 records therefore corresponds to about
  2^19.8 / 16896 = 54 starting points of this yield.

C3 (matching). Repeat with a new first block M0: a fixed random block with a counter in one word, so
every trial uses a distinct block. Compute CV1 = compress31(IV, M0), which gives
A[-4..-1] and E[-4..-1]. For every record whose key equals A[-1]:
  E0 = A0 + A[-4] - S0(A[-1]) - MAJ(A[-1],A[-2],A[-3])
  E1 = A1 + A[-3] - S0(A0) - MAJ(A0,A[-1],A[-2])
  E2 = A2 + A[-2] - S0(A1) - MAJ(A1,A0,A[-1])
  W[i] = E[i] - A[i-4] - E[i-4] - S1(E[i-1]) - IF(E[i-1],E[i-2],E[i-3]) - K[i]   for i = 0..6
  Accept if W5 is in V5 and W6 is in V6.
  The table has no cells on E0..E2 or W0..W4, so these two tests are the whole check. For uniform words
  they pass with probability 2^-18 * 2^-9 = 2^-27 (under H3, Section 9b). W7 and W8 come from the record and W9..W12 from
  the solution, so W0..W12 are now fixed.

C4 (completion). Fill W13, W14, W15.
  For each g in G16, set W14 = s1^-1(g - W9 - s0(W1) - W0), so that W16 = g. Then set
  W18 = s1(g) + W11 + s0(W3) + W2 and require W18 in G18.
  Choose E13 among the words that meet the row-13 cells, and set
  W13 = E13 - A9 - E9 - S1(E12) - IF(E12,E11,E10) - K[13]. Require the row-14 cells and
  dE14 = 00008004 for the resulting E14.
  Choose E15 among the words that meet the row-15 cells, set W15 from the step-15 equation, and require
  the row-16 cells on E16.
  Finally, recompute both copies through step 30 and require equal second-block outputs. If no choice
  succeeds, return to C3.
  For the stored pair, W16 = 064bbffe (in G16) and W18 = 189ec315 (in G18).

C5 (store). Hash P = M0||M1 and P' = M0||M1' under sha256-r31, confirm equality and distinctness, and
store the 256 bytes.

The authors report the cost of C1-C4 as time 2^40.5 and memory 2^19.8 (table records), and a practical
run of 1.2 hours on 64 threads. Their framework writes the total as T_pre + T_match. Here
T_pre = N_start * (T_sat + table enumeration) contains the solver time T_sat per starting solution,
and T_match counts first-block trials at one compression each, plus completion work (ePrint 2026/1080,
Section 3). So the 2^40.5 already contains C1, C2 and C4 as well as C3. The search in C0 is not part
of that total and is charged separately in Section 8.

## 8. Cost ledger (collision-frontier-v5, C = 2140)

Time is summed over all processors, and nothing is discounted for parallel wall-clock time.

    L1  C1-C4, published two-phase total (H1a)                 2^40.5    = 1,554,944,255,988 units
    L2  C3 per-trial word operations not inside the compression:
        at most 32 per trial (advance the M0 counter, index the bucket array with the top bits of
        A[-1], load and compare the bucket bounds and keys, loop control), for at most 2^40.5
        trials: 2^40.5 * 32 / 2140                               2^34.437  =    23,251,502,894 units
    L3  C0 characteristic search, allowance (H1b)               2^38      =   274,877,906,944 units
    L4  one-time exhaustive set computations of Section 6 (V7, V8, G16; 2^32 words each,
        at most 24 operations per word): 3 * 2^32 * 24 / 2140    2^27.107  =       144,503,573 units
    L5  C5 check: 6 compressions + 64 word operations            6.03 units
    ---------------------------------------------------------------------------------------------
    preprocessing L1+...+L5                                      1,853,218,169,404 units = 2^40.75317
    R   online replay: 6 compressions + at most 768 word operations
        (read 256 bytes, padding, compare, output) = 6 + 768/2140 = 6.36 units
    ---------------------------------------------------------------------------------------------
    total time                                                   1,853,218,169,410 units = 2^40.75317

Claimed time_log2 = 40.76: 2^40.76 = 1,862,012,633,415 units, which exceeds the total by 8.8e9 units
(about 2^33.0). Claimed preprocessing_log2 = 40.76 covers L1-L5 with the same slack. The slack absorbs
rounding and any further per-trial overhead up to 12 more word operations per trial.

L2 counts word operations that the published figure, quoted in compressions, may omit. Per-hit work
in C3 is at most about 100 operations per table hit. There are about 2^40.5 * 2^19.8 / 2^32 = 2^28.3
hits, which comes to 2^28.3 * 100 / 2140 = 2^23.9 units, inside the slack. Table construction in C2 is
negligible: 49408 + 1632 * 512 = 884,992 candidate evaluations per starting point, at most 64
operations each, for about 54 starting points, which is 2^31.52 operations or 2^20.45 units. It is in
any case part of L1.

## 9. The one heuristic: H1 (score-critical)

H1. The one-time construction of Section 7 costs at most L1 + L2 + L3 + L4 + L5. In detail:
  (a) C1-C4 cost at most 2^40.5 target-compression units, as Li, Liu, Wang, Dong and Sun report for
      this exact trail, start (standard IV) and step count. The ledger adds the word-operation overhead
      L2 on top.
  (b) C0 costs at most 2^38 units.

Evidence for (a):
- The source states time 2^40.5 and memory 2^19.8 for the full 31-step SHA-256 collision attack. It
  also reports producing the stored pair in 1.2 hours on 64 threads, which is 276,480 thread-seconds.
  2^40.5 compressions in that time is 2^22.42 compressions per thread-second, an ordinary rate for
  31-step SHA-256 on one CPU thread.
- By the source framework's own definition, the total includes the starting-solution solver time.
  A public re-run of one comparable starting-solution solve took 178.4 CPU-seconds (reported by
  solver Th0rgal, submission 25088ab7). That is 2^30.1 units at 2^22.58 units per CPU-second, and
  about 2^35.9 for 54 starting points, well below 2^40.5.
- Section 7 independently reproduces the parts of the search that we could check exactly. C2 rebuilds
  the stored pair's own table record. Under H3, the C3 acceptance probability is 2^-27, the product of the
  exactly enumerated set fractions. The stored pair meets every predicate of C1-C5.
- The stored pair exists, and the organizer verifies it.

Evidence for (b):
- The same public report runs the authors' open-source four-stage trail search (STP with
  CryptoMiniSat) for this trail: 29 solver calls, 16,580.78 CPU-seconds in total, with stages 1-3
  reproducing the published optima.
- At that report's own conservative conversion of 2^22.58 units per CPU-second (2^33.64 word
  operations per CPU-second), the run costs 2^36.60 units. At the source's rate from (a), it costs
  2^36.44 units.
- 2^38 is 2.6x and 2.9x those values. It also exceeds a hardware ceiling: 6 instructions per cycle
  at 5.5 GHz is 2^34.94 operations per CPU-second, or 2^37.90 units for the measured run.

Scope: this one trail, the standard IV, steps 0..30, and the one-time construction of one pair. H1
says nothing about other step counts, other trails or other prefixes.

Sensitivity: time_log2 = 40.76 holds while L1 + L3 stays at or below 2^40.5 + 2^38 + 8.8e9 units.
If C0 cost 2^39 instead (twice the allowance), the total would be 2^40.95. If the true C1-C4 cost were
2^41, the total would be 2^41.19.

Limitations:
- The 2^40.5 is the authors' complexity analysis plus one practical run, not an organizer-model
  operation trace.
- 2^40.5 is the expected cost of a randomised search. What is charged is the one run that produced
  the stored pair. H1 asserts that this run stayed within the ledger; the reported 1.2 hours on 64
  threads is consistent with that but does not bound it.
- The per-trial completion success rate inside it is the authors' figure; we did not reproduce it
  separately.
- The C0 bound relies on a re-run of the public tool, not on the authors' original logs. If the
  authors explored more trails than the re-run did, that extra effort is not covered beyond the
  allowance.

Not heuristic: correctness and distinctness of the stored pair (organizer-verified), success
probability 1 (no coins), and the arithmetic of Section 8.

## 9b. Supporting heuristics H2 and H3 (not score-critical)

**H2-memory-bound.** The peak memory of the one-time construction is at most 2^32 bytes, as computed in Section 10. This assumes the C0/C1 solver calls run one at a time, as Section 7 specifies, and that each needs no more than the 2.13 GiB peak measured in a public re-run of the authors' open-source tool on this trail (credited in Section 12). We did not repeat that measurement. Running k calls in parallel would multiply the solver term by k. H2 affects only the reported memory metric; it does not affect time_log2, success or correctness.

**H3-C3-acceptance.** Section 6 enumerates the admissible sets V5 and V6 exactly over all 2^32 words. Their product of fractions, 2^-27, equals the C3 acceptance probability only if W5 and W6, after key matching, behave as jointly uniform and independent words. We assume this and do not prove it. H3 is used only as a cross-check that the published two-phase total in L1 is consistent. The ledger charges L1 as published, under H1, and does not recompute L1 from 2^-27. Collision correctness and replay success do not depend on H3.

## 10. Memory and advice

Nonuniform advice is the stored pair: 256 bytes, plus the 32-byte digest used in R3, which is less
than 2^9 bytes. The construction behind it is fully charged as preprocessing (Section 8), so the
advice is not free.

Memory is reported only and does not change the score. The peak is during the construction:
- the C0/C1 solver: 2.13 GiB peak resident size in the public re-run, which is 2^31.09 bytes;
- the C2 table: 2^19.8 records * 64 bytes (14 words plus solution id, padded) = 2^25.8 bytes;
- a 2^20-entry bucket index of 4-byte offsets: 2^22 bytes.
The solver is not resident during C3, but even counting all three together gives 2^31.13 bytes, below
the claimed 2^32. The online replay keeps fewer than 2^10 bytes.

## 11. Checks a reviewer can repeat

1. Hash P and P' of Section 4 with sha256-r31. Both give 55fdfb37...869fcd, and P != P'.
2. Run the second block from CV1 for both messages and compare every cell of Section 5. There are no
   violations.
3. Enumerate V5..V9, G16 and G18 over all 2^32 words to get the sizes of Section 6.1 (about 20 seconds
   in C).
4. Run C2 on the stored pair's starting solution: (A1..A4) = (f36e6fcf, b741c202, 90c67413,
   fc7566c3) and (E5..E8) = (1d1fa7dd, afe878e7, 4c97cbe5, 946f8048), with differences from Section 5.
   This gives 1632 and then 16896 records, including the pair's own record.
5. Recompute the ledger of Section 8.

## 12. Sources and credit

- Y. Li, F. Liu, G. Wang, X. Dong, S. Sun, "The First Practical Collision for 31-Step SHA-256",
  ASIACRYPT 2024 (LNCS), presentation slides 9-15: the
  framework, the trail, the colliding pair, and time 2^40.5 / memory 2^19.8 / 1.2 hours on 64 threads.
- Y. Li, F. Liu, G. Wang, J. Shi, "Pushing the Limit of Memory-efficient Collision Attack Framework
  for SHA-2", ePrint 2026/1080, Section 3: the framework steps and its time formula.
- Y. Li, F. Liu, G. Wang, "New Records in Collision Attacks on SHA-2", EUROCRYPT 2024 (ePrint
  2024/349): the SAT/SMT tool and the earlier 31-step attack.
- Public Yukon submissions: the replay-with-charged-construction accounting was first used on this
  track by Akashneelesh, Michae2xl, pepedesigner and newjordan. The solver re-run measurements cited
  in Sections 9-10 are from Th0rgal (submission 25088ab7). We credit all of them.
- Our own contributions: the cell-by-cell check of the pair against the trail; the exact set
  enumerations; the C2 re-run that rebuilds the pair's record; the step-by-step construction
  specification; and the ledger. We claim no new attack or lower complexity.
