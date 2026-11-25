# Omer Goldzweig's collision attack on 38-step SHA-256 (ePrint 2026/2913) under cost model v5: time 2^57.56, memory 2^32.5 bytes

**Track** sha256-r38-exploratory, target sha256-r38-prefix-v1, cost model collision-frontier-v5 (C = 2728), scalar policy hashsmash-scalar-tm-v1 (score = time_log2 + max(0, memory_log2_bytes - 20)).
**Claim** time_log2 = 57.56 (ledger total 2^57.5584 target compressions, Section 7), algorithmic success probability at least 0.39 (0.4231 under premise H4, Section 6), memory 2^32.5 bytes (Section 8), preprocessing 2^56.9479, non-uniform advice below 2^12 bytes. Scalar score 70.06.

## 0. Credit and scope of this filing

The attack, its characteristic, its core and the published collision are the work of Omer Goldzweig: O. Goldzweig, "A Collision for 38-Step SHA-256", Cryptology ePrint Archive, Paper 2026/2913, dated 15 November 2026 (cited below as [G]). Every rate of Table 4 of [G], the core search, the table construction and the GPU run that found the collision are his. This package files that attack on HashSmash with credit to him. He was asked to file it himself and has not; a filing by him takes precedence over this one. He is not a co-author of this submission and has not reviewed it.

Our contributions are limited to the following.
1. **Reconstruction of the core from the published pair.** A3..A13 of both executions, the variant, the lower part, the upper pair, the key and every value that [G] prints for the pair are recomputed from the 128-byte messages of [G, Table 5] (Section 4; check-2913 trial 0).
2. **Independent exact recounts.** The counts of [G, Table 2] on which the attack relies (|V7| = 2^14 in 512 aligned blocks, 4 values of W8, rows 17, 25, 26 and 30) are recomputed exactly, both by a 2^32 brute force in C and by the GF(2) method of the organizer experiment (Section 10).
3. **The variant count.** The core admits 1,572,864 variants (values of E6 with dW9 = 0 and a solvable dW8 = -4), each with exactly one pattern of E5 on F7; [G]'s three-stage search kept 56 (Section 4.3). This filing does not use the additional variants.
4. **Accounting under collision-frontier-v5** for a fully specified configuration of [G]'s attack that uses only the published variant (Sections 5 to 8).

| Term | Value | Section |
|---|---|---|
| per-lower-solution success, published variant | p1 = 2^-57.0587 | 6 |
| lower solutions processed (mu = 0.55) | L = 2^56.1962 | 6 |
| first blocks | 2^53.1962, each <= 4.38 compressions | 7 |
| matches | 2^53.8658, each <= 1 compression | 7 |
| online total | 2^56.0231 | 7 |
| core search, table, lower table, allowance | 2^56.9479 | 7 |
| **total time** | **2^57.5584** | 7 |
| memory | 5,551,035,016 bytes = 2^32.3701 <= 2^32.5 | 8 |

## 1. The output is an ordinary collision of the selected target

The procedure outputs two 128-byte messages M0 || M1 and M0 || M1' with M1 != M1'. M0 is a first block drawn from the procedure's coins, and (M1, M1') is a pair of second blocks with F38(H, M1) = F38(H, M1') for H = F38(IV, M0), where F38 is the 38-step compression of the target (steps 0..37, feed-forward). Both messages have the same length, so their padding blocks are equal and their 38-step digests are equal. Before output, the procedure computes both compressions from H and compares the outputs, so an output is a collision by direct verification, independent of every premise below. [G, Table 5] gives such a pair; its padded 38-step digest is 5b61bad3 7673bb33 23d64bc4 fad45b44 a7e6bf04 8d787d61 27ec259b 12d0d63f for both messages. Trial 0 of the experiment check-2913 returns it, and the organizer's harness recomputes the digests of every returned pair.

## 2. The chaining value enters the second block through W0..W7 only

We use the notation of [G, Section 2]. All words have 32 bits and additions are modulo 2^32. The state is described by sequences A_t, E_t with (A_-1, A_-2, A_-3, A_-4, E_-1, E_-2, E_-3, E_-4) = (H0, ..., H7), and

- (2) E_t = A_{t-4} + E_{t-4} + Sigma1(E_{t-1}) + Ch(E_{t-1}, E_{t-2}, E_{t-3}) + K_t + W_t,
- (3) A_t = E_t - A_{t-4} + Sigma0(A_{t-1}) + Maj(A_{t-1}, A_{t-2}, A_{t-3}),
- (4) E_t = A_t + A_{t-4} - Sigma0(A_{t-1}) - Maj(A_{t-1}, A_{t-2}, A_{t-3}),
- (5) W_t = E_t - A_{t-4} - E_{t-4} - Sigma1(E_{t-1}) - Ch(E_{t-1}, E_{t-2}, E_{t-3}) - K_t.

F38(H, M) = (A_37 + H0, ..., A_34 + H3, E_37 + H4, ..., E_34 + H7). By (4) and (5), H and A_0..A_15 determine W_0..W_15, and W_8..W_15 do not depend on H. For fixed A_0..A_7, W_{7-i} = kappa_i(H_0, ..., H_{i-1}) - H_i for i = 0..7, so H -> (W_0, ..., W_7) is a bijection: for a uniform H the words W_0..W_7 are independent and uniform. In particular W_7 = theta - H_0 with theta a function of A_0..A_7 alone. Trial 8 of check-2913 inverts this bijection 64 times (it solves H from chosen W_0..W_7) and checks W_7 = theta - H_0.

## 3. The characteristic has message differences in W7, W8, W10, W15

The two blocks differ by dW7 = w = 31de0240, dW8 = -4, dW10 = d = 00028000, dW15 = 4 (modular differences, second minus first). Among the expanded words only W23 and W24 differ, dW23 = -a = 07ff0000 and dW24 = -4, with a = f8010000 = dA15. With D(f; x, e) = f(x + e) - f(x), the message expansion imposes the conditions of [G, Table 2]:

| Row | Condition | Met by | Exact count over 2^32 (ours) |
|---|---|---|---|
| 17 | D(s1; W15, 4) = -d | the upper pair (validity) | 637,534,208 = 2^-2.752 |
| 22 | D(s0; W7, w) = -4, i.e. W7 in V7 | the chaining value: W7 = theta - H0 | 16,384 = 2^14 (512 aligned blocks of 32) |
| 23 | D(s0; W8, -4) = -a - w | the lower part: W8 in {16185001, 161a5001, 161c5001, 161e5001} | 4 |
| 24 | dW24 = dW8 = -4 | automatic | |
| 25 | D(s1; W23, -a) = tau, tau = -D(s0; W10, d) | chance | 3,276,800 for tau = 6002033f (2^-10.36) |
| 26 | D(s1; W24, -4) + d = 0 | chance | 637,534,208 (2^-2.752) |
| 30 | D(s0; W15, 4) = a | the upper pair (validity) | 536,870,912 = 2^-3 |
| 31 | dW31 = dW24 + dW15 = 0 | automatic | |

The state differences follow [G, Tables 3 and 6]. Steps 0..6 have no difference; steps 7..13 have the differences of the core; from step 14 on, dA_14 = 0, dE_14 = -0x21000, dA_15 = a, dE_15 = -s 2^9, dA_16 = 4, dE_16 and dE_17 in sets of 8 and 4 values, dA_t = 0 for t >= 17, dE_18 = 0, dE_19 = a, dE_20 = 4, and no difference from step 21 on (dE_23 = dE_19 + dW23 = 0 and dE_24 = dE_20 + dW24 = 0). A pair that follows the characteristic through step 24 and meets rows 25 and 26 has no difference in any expanded word after W24 and no state difference after step 20, so it collides. The published pair has s = -1 and the modular differences of [G, Table 6]; trial 0 of check-2913 recomputes all of them, every row of the table above on the pair's words, and checks that no other step or word has a difference. The characteristic does not extend to 39 steps (W38 contains s0(W23)), which does not matter for this target.

## 4. The second block: core, variant, lower part, upper pair, key

### 4.1 The core is recovered from the published pair

The core is A3..A13 of both executions; A3..A6 agree. Recomputed from [G, Table 5]:

| | A3 | A4 | A5 | A6 | A7 | A8 | A9 | A10 | A11 | A12 | A13 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| first | 3baa4a73 | ef43ece6 | ac72c958 | b1b7ffd2 | 3d429e3b | 93dbdd23 | 88f2acf8 | 959ea855 | 9871db5e | 6a30e20f | dad82f20 |
| second | 3baa4a73 | ef43ece6 | ac72c958 | b1b7ffd2 | 6f20a07b | e33142fb | 2aa7318e | d935a3b4 | 9991eb9f | 63b1f047 | d2793d21 |

The pair's chaining value is H = d00b8f69 1466ed03 49c1a713 7c64bf45 bd8254a1 c00b0cc6 a1382798 5f21292d. Its variant is A2 = 42747b1a (E6 = 99ccff09), its lower part A0 = 248e4477, A1 = 166a78d5 (E4 = cd0d33ea, E5 = 8426bd20), its upper pair A14 = 5bde5962, A15 = 9b3a6d8a (A15' = A15 + a), and its key C16 = W9 + s0(W1) + W0 = W16 - s1(W14) = 00b50618. All of these equal the values printed in [G, Section 9]. The set F7 of positions where E7 and E7' differ is 4e3e06c0 (|F7| = 13); the set F8 for E8 is 5a14c0a0 (|F8| = 10); they share 6 positions.

### 4.2 Lower candidates and lower solutions of the published variant

Fix the published variant v* (A2 = 42747b1a). By [G, Section 4.2], dW8 = -4 prescribes E5 on F7 (here E5 & F7 = 04260400) and leaves its 19 other bits free, and row 23 lets W8 take one of the 4 values above. A lower candidate is (E5, j) with E5 & F7 = 04260400 and j in {1, 2, 3, 4}; it fixes A1 = E5 - A5 + Sigma0(A4) + Maj(A4, A3, A2), E4 = E8 - A4 - Sigma1(E7) - Ch(E7, E6, E5) - K8 - W8^(j) and A0 = E4 - A4 + Sigma0(A3) + Maj(A3, A2, A1). The variant has 4 x 2^19 = 2^21 lower candidates. dW9 = 0 holds for the variant, and dW10 = d and dW11..dW13 = 0 hold for the core. The only remaining condition on a lower candidate is row 22, W7 = theta - H0 in V7. A lower candidate is a **lower solution** for the chaining value H if theta - H0 is in V7; for a uniform H0 this has probability |V7| / 2^32 = 2^-18 exactly, so a first block has 2^21 x 2^-18 = 8 lower solutions in expectation (premise H1). Trial 8 of check-2913 draws 64 lower candidates of v* with random free bits and random j, random W1..W6, a random W7 in V7 and W0 fixed by the key 00b50618, solves H, and checks that the pair of blocks has the message-difference pattern (w, -4, d, 4) and that both 38-step executions have exactly the published pair's differences dA_t, dE_t for t = 0..17.

### 4.3 The core admits 1,572,864 variants; this filing uses one

A variant is a value of E6 (equivalently A2, by (4)) with dW9 = 0 and some E5 with dW8 = -4. dW9 depends on E6 only on F8, and dW8 depends on E6 and E5 only on F7. Exactly one of the 2^10 patterns on F8 gives dW9 = 0 (so 2^22 values of E6), and counting the joint patterns on F7 union F8 gives 1,572,864 variants, each with exactly one E5 pattern on F7. The published E6 = 99ccff09 is one of them. A 2^32 brute force in C and trial 7 of check-2913 give the same count; trial 7 also builds 16 random variants end to end and checks that they follow the published pair's differences through step 17 with the published key and upper pair. [G, Section 6.1] reports 56 variants from its search and uses 32 of them. The values of those 32 variants are not published, so this filing uses only v*. The rates of Section 6 apply to v* by Lemma 6.1.

### 4.4 Upper pairs, keys and the table

By (1) of [G], W16 = s1(W14) + C16 with the key C16 = W9 + s0(W1) + W0. W14 and W15 depend on the core and the upper pair pi = (A14, A15) only, and the key depends on the lower solution and on H. Both executions have the same key, and by (2), (3) the differences of steps 14..17 depend on the lower solution and H only through the key [G, Section 4.3]. For each pi the set K(pi) of keys for which step 17 follows the characteristic is a function of pi and the core. An upper pair is valid if steps 14..16 follow the characteristic with the digit XOR patterns of [G] and rows 17 and 30 hold. An entry (c, pi) with c in K(pi) is kept if E16[27] = E15[27] and if step 18 can hold for some value of the free word W17 (the live test of [G, Section 4.3], a Monte Carlo search over W17 per entry). The table of [G] has N = 853,938,951 live entries in 2,345,041 upper pairs. A **match** is a lower solution together with a live entry whose key equals the lower solution's key. Step P2 of Section 5 builds this table by [G]'s construction with a fixed seed for the live test; we have not run that construction (premise H2 covers the rebuilt table).

## 5. The procedure

Precomputation, executed one process at a time:

- **P1 (advice).** The core of Section 4.1, the variant v* with E5 & F7, the constants w, d, a, the 64 round constants, the 512 block indices of V7 and the 4 values of W8: below 2^12 bytes. The core and the variant v* are outputs of [G]'s core search (52,300 vCPU-hours, charged in Section 7): v* is one of the 32 variants [G] uses (the 20th, [G, Section 9]). [G] does not print their values; we read them from [G]'s published pair, which only publishes them. The GPU run that found that pair produces nothing the procedure needs and is not part of the procedure; charging it would add 0.036 bit (Section 7.3).
- **P2 (upper-pair table).** As in [G, Sections 4.3 and 6.2]: enumerate the valid upper pairs (bit-serial search over A14, A15), compute K(pi) under the bit-27 rule, apply the live test, and insert every live entry directly into a hash table keyed by c mod 2^30 with a 4-bit mask of the top key bits (the layout of [G], 5.44 GB over 193,853,061 distinct reduced keys, one 32-byte bucket per probe). The live test uses a fixed public seed, so P2 is deterministic given the core. A first pass marks the reduced keys in a 2^30-bit set (134 MB) and counts them; the set is freed before the second pass allocates and fills the table. The 3.44 GB file of [G] is not needed. A record array holds (A14, A15) per upper-pair id (2,345,041 x 8 bytes).
- **P3 (lower table of v*).** For each of the 2^21 lower candidates store (theta, A0, A1) (12 bytes), sorted by theta >> 5; a bitmap over the 2^27 values of theta >> 5 marks the non-empty buckets; a directory (2^22 slots of 8 bytes) maps a non-empty bucket to its range.
- **P4 (allowance).** The characteristic search, the skeleton search and screening, earlier cores and development, which [G] does not report, are charged as an allowance (premise H6).

Online, for i = 1, ..., N_FB with N_FB = 2^53.1962 (Section 6), stopping at the first collision:

1. Draw M0 (two uniform 256-bit words) and compute H = F38(IV, M0). Write H0 = 32h + l with 0 <= l < 32, and compute the per-H constants of W0 and W1.
2. **Lower solutions.** For each g in (h + B) union (h + B + 1) mod 2^27, where B is the set of 512 block indices of V7, test the bitmap at g. For a non-empty bucket g read its records; a record is a lower solution if (g - h in B and theta_l >= l) or (g - h - 1 in B and theta_l < l), where theta_l = theta mod 32. This is the condition theta - H0 in V7, because V7 is a union of complete aligned blocks of 32 (check-2913 trial 1).
3. **Key.** For a lower solution compute W0 = A0 + k_H(H), W1 from E0, E1 (eq. (4), (5)), W9 = E9 - A5 - E5 - Sigma1(E8) - Ch(E8, E7, E6) - K9, and c = W9 + s0(W1) + W0.
4. **Matches.** Probe the hash table with c mod 2^30; every entry whose mask admits c >> 30 is a match. For a match read (A14, A15) and compute steps 16..18 of both executions (W16 = s1(W14) + c; W17, W18 from W1, W2, W3, W10, W11, W15, W16).
5. **Completion.** If dA18 = dE18 = 0, build M1 and M1' by (5), compute F38(H, M1) and F38(H, M1') and compare. On equality output M0 || M1 and M0 || M1'.

This is Algorithm 1 of [G] with one variant instead of 32 and with a bitmap scan over V7's blocks in place of [G]'s grouped bucket table; [G]'s grouping depends on the concentration of theta over its 32 variants, which is not published. The step-18 test and the completion are those of [G].

## 6. Success probability

### 6.1 The counted rates of Table 4 are constants of the table

[G, Table 4] gives, per lower solution of its 32 variants: expected matches N / 2^32 = 0.198823; step-18 passes 1.5925 x 10^-5 (counted on 2.1 x 10^15 lower solutions; 1.5929 x 10^-5 over the whole run); step 19 given step 18, 0.015367 (counted; 0.015368 over the run); collision given step 19, 2^-35.082 (+-0.5%, sequential Monte Carlo from 43,371 depth-20 states). Their product is p32 = 2^-57.0444.

**Lemma 6.1.** Under premise H1, for every variant of the core, the expected number of matches per lower solution, the expected number of step-18 passes per lower solution and the probability of step 19 given step 18 are the same constants of the table.

*Argument.* Under H1, W0..W7 are independent and uniform (Section 2). A lower solution is selected by W7 in V7 alone. Its key c = W9 + s0(W1) + W0 is uniform because W0 is uniform and independent of W1 and W7; so the expected number of matches is N / 2^32 for every lower solution. Given a match (c, pi), W1 is uniform and W2 is uniform and independent of (W0, W1, W7), so W17 = s1(W15) + W10 + s0(W2) + W1 is uniform and independent of the entry. The variant enters W17 only through the constant W10. Step 18 depends on (c, pi), the core and E17 = (a function of c, pi and the core) + W17, so its probability per match is q18(c, pi), the fraction of W17 values that pass, and the step-18 rate per lower solution is the sum of q18 over the table divided by 2^32, a constant of the table. W18 = s1(W16) + W11 + s0(W3) + W2 contains the free uniform word W3, so E18 is uniform and independent of the step-18 state, and step 19 given step 18 depends only on that state, whose law does not involve the variant. []

The tail after step 19 depends on the words W19..W24, which contain the free words W4, W5, W6. The variant enters it through tau = -D(s0; W10, d) in row 25 and through W9, which shifts W24 by s0(W9) next to the term s1(W22) and which also varies with E5 inside every variant. Premise H3 states the tail of v* accordingly.

[G, Section 6.1]: for 32 of its 56 variants, the row-25 count is 3,309,568 or 3,276,800. The published variant has tau = 6002033f and the count 3,276,800, the smaller of the two. [G]'s Monte Carlo evaluates row 25 with each pair's own tau. With the row-25 factor treated as multiplicative (premise H3), the per-lower-solution success probability of v* is

p1 >= p32 x 3,276,800 / 3,309,568 = 2^-57.0444 x 2^-0.0144 = 2^-57.0587.

### 6.2 Fifty-five percent of the expected work gives success probability 0.42

The procedure processes N_FB = 2^53.1962 first blocks, so the expected number of lower solutions is L = 8 N_FB = 2^56.1962, and the expected number of collisions is mu = L p1 = 0.55. The successes are rare events (p1 = 2^-57.06 per lower solution) that depend on one another only through shared first blocks and shared table entries. Under premise H4 (Poisson approximation), Pr[at least one collision] >= 1 - e^-0.55 = 0.4231 >= 0.39. The threshold 0.39 needs mu >= 0.4943, so the true p1 may be 10% below the stated value (0.15 bit, against the 0.5% standard error of the tail estimate) before the success probability falls below 0.39. The probability space is the procedure's coins: the first blocks M0 are drawn uniformly and independently. The advice of P1 is fixed, and P2 and P3 are deterministic given it. If only the second-moment bound Pr[X >= 1] >= E[X]^2 / E[X^2] is admitted, with pairwise non-positive correlation of distinct successes, mu = 0.64 is needed: time +0.0792 bit (Section 7.3).

## 7. Time

### 7.1 Unit costs

One 38-step compression costs 1; any other 256-bit word operation costs 1/2728 (cost model v5). 32-bit arithmetic is charged with its masks; a 32-bit rotation costs 4 operations (two shifts, an OR, a mask). Each table probe is one 256-bit load.

| Unit | Bound | Itemization |
|---|---|---|
| first block | 1 + 9216/2728 = 4.378 | the compression of M0 (1); M0 from two random words (2 ops); the per-H constants of W0 and W1 (Sigma0(H0), Maj(H0, H1, H2), Sigma1(H4), Ch(H4, H5, H6) and sums, < 80 ops); 1024 bitmap probes of 8 ops each (index add and mask, word index, load, bit index, shift, AND, branch; 8,192 ops); on average at most 1024 x 2^21 / 2^27 = 16 non-empty buckets, each a directory probe (< 40 ops). Total < 9,216 ops |
| lower solution | 384/2728 = 0.1408 | records examined: E[examined] <= 2 E[lower solutions], because a candidate's bucket is reached for at most 2 x 512 of the 2^27 values of h while it is a solution for 512 of them on average (2 records x 12 ops); W9 (3); W0 (2); E1 (Sigma0, Maj, sums: 25); W1 (Sigma1, Ch, sums: 29); s0(W1) (11); key (4); hash-table probe with a second probe on overflow (2 x 45). About 190 ops, bound 384 |
| match | 1 | read (A14, A15); recompute E14, E15, W14, W15 of both executions (< 320 ops); W2, W3 (< 120); steps 16, 17, 18 of both executions with W16, W17, W18 (< 900); compare (4). About 1,350 ops, bound 2,728 |
| step-18 pass | 3 | M1, M1' by (5) (< 1 compression), two compressions, compare |

### 7.2 Ledger

With L = 2^56.1962 expected lower solutions (Section 6.2), N_FB = L / 8, matches 0.198823 L and step-18 passes 1.5925 x 10^-5 L:

| Term | Count | Unit | log2 of the cost |
|---|---|---|---|
| first blocks | 2^53.1962 | 4.378 | 55.3266 |
| lower solutions | 2^56.1962 | 0.1408 | 53.3676 |
| matches | 2^53.8658 | 1 | 53.8658 |
| step-18 passes | 2^40.2579 | 3 | 41.8428 |
| **online** | | | **56.0231** |
| core search (P1): 52,300 vCPU-hours at R = 2^26 per vCPU-second | 2^27.4883 vCPU-s | 2^26 | 53.4883 |
| table (P2): 42 vCPU-hours, two passes | 2^18.2061 vCPU-s | 2^26 | 44.2061 |
| lower table (P3): 2^21 candidates, 1024 ops each incl. sorting | | | 19.5864 |
| allowance (P4, premise H6): 10 x the core search | | | 56.8102 |
| **preprocessing** | | | **56.9479** |
| **total** | | | **57.5584** |

The time is the expected work of the full budget of N_FB first blocks, which bounds the expected work of the procedure that stops at the first collision. The work of 2^53 independent first blocks concentrates: its relative standard deviation is below 2^-20. The time claim is 57.56.

**Rate envelope R.** The core search and the table ran on CPUs ([G]: Arm machines for the core search). The word-RAM work of one vCPU-second is bounded by its instruction throughput. A server vCPU issues at most 8 instructions per cycle at most 4 GHz, each on at most 512 bits (two 256-bit words), so at most 2^35.9 primitive operations per second = 2^24.5 compressions. For an Arm Neoverse core (at most 2.8 GHz, 8-wide, vectors of at most 256 bits) the bound is 2^34.4 operations = 2^23.0 compressions. R = 2^26 leaves a factor of 2.8 and 8 respectively for instructions that combine several primitive operations (premise H5). A CDCL solver such as CaDiCaL is bound by memory latency in unit propagation and executes far fewer instructions per cycle than the issue width, which adds to this margin. Our earlier filings used 2^30; Section 7.3 gives the result under it.

### 7.3 Sensitivity

| Change | time_log2 | score |
|---|---|---|
| this claim | 57.5584 | 70.0584 |
| R = 2^25 | 56.9860 | 69.4860 |
| R = 2^30 | 60.9947 | 73.4947 |
| allowance 0 | 56.2531 | 68.7531 |
| allowance 1 x core search | 56.4511 | 68.9511 |
| allowance 100 x core search | 60.2270 | 72.7270 |
| R = 2^30 and allowance 100 x | 64.1517 | 76.6517 |
| second-moment bound (mu = 0.64) | 57.6376 | 70.1376 |
| mu = 0.5 (success 0.3935) | 57.5124 | 70.0124 |
| matches 10% more (a rebuilt table with N 10% larger) | 57.5695 | 70.0695 |
| also charging [G]'s GPU run that found the published pair (2^52.24) | 57.5941 | 70.0941 |
| [G]'s 32 variants (not published) | 57.2178 | 69.7178 |
| [G]'s convention (1 call per first block and per match, expected cost, no preprocessing) | 54.7794 | n/a |

## 8. Memory

The procedure's peak memory is that of the online tables:

| Item | Bytes |
|---|---|
| live-entry hash table ([G, Section 6.2]) | 5,440,000,000 |
| upper-pair records (A14, A15): 2,345,041 x 8 | 18,760,328 |
| lower table of v*: 2^21 x 12 + bitmap 2^24 + directory 2^22 x 8 | 75,497,472 |
| code, advice, constants and working state | <= 16,777,216 |
| **total** | **5,551,035,016 = 2^32.3701** |

The claim is 2^32.5 = 6,074,000,999 bytes. [G] states sizes in decimal units: its bucket offsets of 2^27 x 4 = 536,870,912 bytes are "537 MB", and its 7.35 GB of tables are "6.8 GiB" [G, Table 1]. The claim leaves room for a rebuilt table (P2) up to 9.5% larger than [G]'s 5.44 GB, and also covers 5.44 GiB. [G] reports 7.35 GB of tables for its GPU program: it also holds the lower-solution table of 32 variants (1.09 GB), a key filter (89 MB) and per-upper-pair records with precomputed words (part of 0.74 GB). The procedure here uses one variant, no filter, and recomputes the upper-pair words from (A14, A15) inside the match cost. The 18 GB of GPU batching buffers of [G] belong to that implementation; the procedure here processes one first block at a time and needs a few kilobytes of working state.

**Scope of the peak.** The peak covers the online procedure and every computation whose output the procedure reads, executed one process at a time: the unreported searches (P4) and the core search, whose outputs are the characteristic and the advice of P1; the table construction (P2); the lower table (P3); and the online phase. Total time is unchanged by sequential execution, since v5 charges work summed over processors. P2's first pass holds a 2^30-bit set (134 MB); its second pass inserts live entries directly into the final hash table and appends records, so its peak is the final table plus the state of one upper pair. P3 needs below 10^8 bytes. The processes of the core search and of P4 (SAT solving, CaDiCaL with an external propagator in [G], and bit-serial depth-first search) are bounded by premise H7 at 2^32 bytes each, below the online peak. [G]'s GPU run is not part of the procedure: it produces nothing the procedure reads, since the advice values are outputs of the core search that the published pair merely displays. The studies that support the premises are evidence, not part of the procedure, and their memory is not charged: [G]'s rate counts over 2.1 x 10^15 lower solutions, its Monte Carlo tail estimate, its GPU run, and our brute-force counts and reconstruction. The procedure reads only the declared constants, the advice of P1 and the tables it builds.

## 9. Heuristic premises

- **H1 (uniform chaining value).** For M0 drawn uniformly by the procedure, H = F38(IV, M0) behaves as a uniform 256-bit value for the events of the attack: the selection W7 in V7, the key, and the free words W2..W6. Evidence: [G]'s run processed 2^47.0 first blocks and 1.52 x 10^16 lower solutions, 108.0 per first block (rounded inputs) against 108.39 predicted for its configuration; the step-18 rate over the run (real chaining values) is 1.5929 x 10^-5 against 1.5925 x 10^-5. Trial 8 of check-2913 checks the bijection H <-> W0..W7 used in Section 2.
- **H2 (the counted rates of [G, Table 4], for the table of P2).** [G]'s live table has N = 853,938,951 entries; the step-18 rate per lower solution is 1.5925 x 10^-5 and step 19 given step 18 is 0.015367. A table built by P2 with a fixed seed for the live test has at most 1.095 N entries and the same step-18 and step-19 rates. Evidence: [G]'s counts over 2.1 x 10^15 lower solutions and over the whole run (1.5929 x 10^-5, 0.015368). Two builds can differ only in entries where the sampled search for a passing W17 succeeds in one build and not in the other. [G] reports that the attack with and without the live filter found the same 5,535 pairs of depth 20 or more in 5 x 10^7 first blocks, and that an exact search found a passing W17 for 1 of 6,659 rejected entries. Such marginal entries carry no measurable share of the step-18 passes. By Lemma 6.1 the rates are constants of the table and apply to v*. We have not rebuilt the table. Sensitivity: 10% more entries cost +0.0111 bit of time and stay within the memory claim.
- **H3 (tail).** Collision given step 19 is 2^-35.082 for [G]'s variant mix and at least 2^-35.096 for v*: the variant enters the tail through row 25, a factor taken at the smaller of [G]'s two counts (3,276,800 of 2^32 against 3,309,568), and through W9, which shifts W24 by s0(W9) beside the term s1(W22) and does not change the tail rate. Evidence: [G]'s sequential Monte Carlo (43,371 depth-20 states, 128 particles each, standard error 0.5%; reweighting for the sampling bias changes it by 0.05%); treating W19..W22 as independent uniform words gives 2^-35.079; the numbers of pairs of depth at least 21, 22, 23 and 25 in [G]'s run agree with the predictions of this estimate within 2% (by our arithmetic from [G]'s rates, about 900 pairs of depth at least 25 over the run); rows 25 and 26 are exact counts (Section 3; check-2913 trials 3, 4); the collision itself.
- **H4 (Poisson).** With mu = 0.55 expected collisions, Pr[at least one] >= 1 - e^-0.55 = 0.4231. Evidence: p1 = 2^-57.06 per lower solution. First blocks are drawn independently and the advice and tables are fixed, so successes in different first blocks are independent; only successes within one first block can cluster. Distinct lower solutions of one first block differ in A0, A1 and hence in W0..W3, and the tail conditions depend on the free words W4..W6. [G]'s depth counts agree with the rate model. The threshold needs mu >= 0.4943, which leaves a 10% margin on p1. Sensitivity: the second-moment bound costs +0.0792 bit.
- **H5 (precomputation and rate envelope).** The computation that produced the core took 52,300 vCPU-hours and the table 42 vCPU-hours, as [G, Sections 6.1 and 7.2] reports; a vCPU-second performs at most R = 2^26 compressions' worth of word-RAM work. Evidence: [G]'s statements (also US$290 for the core search); the instruction-throughput bound of Section 7.2. Limitation: the core search's cost is one realized run; the expected cost of a fresh core search is not established. The procedure uses the produced core as advice and charges its realized cost.
- **H6 (allowance for unreported search).** The characteristic search, the skeleton search and screening, earlier cores and development cost at most 10 times the core search (523,000 vCPU-hours, about US$2,900 at [G]'s price). Basis: [G, Section 6.1] presents these as searches of the same kind as the reported one (SAT models of both executions, screened by the step-17 entries of cores completed from them) and reports only the final core search; the allowance admits ten screenings of the reported size. Quantitative comparison, by our own accounting in earlier filings: our search for a 38-step SHA-256 characteristic (a signed-difference SAT model swept over 24 XOR patterns of the message difference), the SAT solve that conforms its first 16 steps, and all development of our earlier r38 filings took less than 2^22 core-seconds on one 10-core machine, 2^-8.8 of this allowance (2^30.8 vCPU-seconds). [G]'s skeleton screening completes cores from candidate skeletons, so it can cost a multiple of one core search; the allowance admits ten. No measurement of [G]'s own unreported computation exists. Sensitivity: Section 7.3.
- **H7 (memory of the SAT searches).** Each process of [G]'s core search and of the unreported searches of P4 used at most 2^32 bytes. Evidence: our measured peak for a comparable SAT solve on 38-step SHA-256 (Kissat 4.0.1 on a 459,368-clause formula whose solution fixes the first 16 message words of a pair following a 38-step characteristic) is 70,892 KB = 2^26.08 bytes; the depth-first stage 3 of [G] uses negligible memory. Limitation: [G] does not report the memory of its SAT runs.

## 10. Evidence

### 10.1 [G]'s run and collision

The GPU run of [G, Section 8.2] processed 2^47.0 first blocks and 1.52 x 10^16 lower solutions in 53.3 GPU-hours and found the collision after about 10% of the expected work. A single success does not establish the expected cost; it shows that the procedure produces collisions and that the rates of the first stages hold on real chaining values. [G] reports that the GPU program's matches and depths are identical to those of a CPU implementation on four ranges of 2^28 first blocks, and that the collision was checked with five independent implementations. Trial 0 of check-2913 returns it, and the organizer's harness recomputes its digests.

### 10.2 Our reconstruction

From the published 128-byte messages we recomputed H, both 38-step traces, the core, the variant, the lower part, the upper pair, the key, |F7| = 13, w, d, a, tau = 6002033f, every difference of [G, Table 6], and every condition of [G, Table 2] on the pair's words. All agree with [G]. A brute force over 2^32 in C (OpenMP, 10 threads) gave:

```
published variant E6=99ccff09 found, 1 E5|F7 solutions
E6 with dW9=0: 4194304; variants (dW8=-4 feasible): 1572864; E5|F7 solution-count histogram: 1:1572864
|V7| = 16384 (2^14 = 16384), full aligned 32-blocks: 512
row 23 W8 values: 4 (paper 4)
row 25 count for tau: 3276800 (paper 3,276,800)
row 26 count: 637534208 (paper 637,534,208)
row 17 W15 count: 637534208 = 2^-2.752 (paper ~2^-2.75)
row 30 W15 count: 536870912 = 2^-3.000 (paper ~2^-3)
```

### 10.3 The organizer experiment check-2913

`experiments/check2913.py` (standard library, deterministic, under 2 seconds) runs nine checks, one per trial, and returns a pair only when its check passes:

| Trial | Check | Pair returned on success |
|---|---|---|
| 0 | the published pair: H, outputs, digest, core, variant, lower part, upper pair, Table 6, Table 2 rows on the pair's words, key | the published collision (a full collision) |
| 1 | the size of V7 is 16,384 by exact count, 512 complete aligned blocks of 32, the pair's W7 in V7 | marker pair (not a collision) |
| 2 | exactly 4 values of W8 satisfy row 23, the pair's W8 among them | marker pair |
| 3 | row 25 count 3,276,800 for tau = 6002033f | marker pair |
| 4 | row 26 count 637,534,208 | marker pair |
| 5 | row 17 count 637,534,208 | marker pair |
| 6 | row 30 count 536,870,912 | marker pair |
| 7 | 1,572,864 variants, one E5 pattern each, the published one among them; 16 random variants follow the pair's differences through step 17 | marker pair |
| 8 | 64 random lower candidates of v* with random W1..W6, W7 in V7, W0 from the key: H solved, differences through step 17 equal the pair's | marker pair |

The exact counts enumerate the carry paths of x + e. On each path the XOR difference D = (x + e) XOR x and some bits of x are fixed; with Y = sigma(D), sigma(x + e) - sigma(x) = Y - 2(sigma(x) AND Y), so the condition is affine in x over GF(2), and its solutions are counted by elimination. The counts equal the C brute force of Section 10.2. In our runs in the pinned image (two runs, byte-identical output) trials 0..8 return pairs and trial 0 is a full collision.

## 11. Limitations

- We have not rebuilt [G]'s upper-pair table or measured the rates of [G, Table 4]; H2 and H3 rest on [G]'s counts, its Monte Carlo estimate and its run.
- The live test of [G] is a Monte Carlo test whose sample size [G] does not state; P2 follows it with a fixed seed, and premise H2 carries the rates of [G]'s table over to the rebuilt one.
- The core search's cost is one realized run, and the unreported searches are covered by an allowance without a measurement (H5, H6).
- The procedure uses one variant; its first-block cost (4.378 compressions) is an itemized bound, not a measurement.
