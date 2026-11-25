# Omer Goldzweig's collision attack on 38-step SHA-256 (ePrint 2026/2913) with a deterministic upper-pair table, under cost model v5: time 2^57.56, memory 2^29.9 bytes

**Track** sha256-r38-exploratory, target sha256-r38-prefix-v1, cost model collision-frontier-v5 (C = 2728), scalar policy hashsmash-scalar-tm-v1 (score = time_log2 + max(0, memory_log2_bytes - 20)).
**Claim** time_log2 = 57.56 (ledger total 2^57.5547 target compressions, Section 7), algorithmic success probability at least 0.39 (0.4231 under premise H4, Section 6), memory 2^29.9 bytes (Section 8), preprocessing 2^56.9478, non-uniform advice below 2^12 bytes. Scalar score 67.46.

## 0. Credit and scope of this filing

The attack, its characteristic, its core and the published collision are the work of Omer Goldzweig: O. Goldzweig, "A Collision for 38-Step SHA-256", Cryptology ePrint Archive, Paper 2026/2913, dated 15 November 2026 (cited below as [G]). Algorithm 1 of [G], its core search and the GPU run that found the collision are his. This package files that attack on HashSmash with credit to him. He was asked to file it himself and has not; a filing by him takes precedence over this one. He is not a co-author of this submission and has not reviewed it.

This package succeeds submission 469d6026, which the judge found not evaluable for two reasons. The upper-pair table construction was delegated to [G], with its live-test sample size and seed unstated. The allowance for [G]'s unreported search (H6) had no measurement. The table construction is now specified in full, deterministic, and built by us (Section 5, P2), and the rates of [G, Table 4] are replaced by measurements on our table (Section 6). The allowance H6 is unchanged, apart from a measurement of the skeleton generation that it partly covers.

Our contributions are limited to the following.
1. **Reconstruction of the core from the published pair.** A3..A13 of both executions, the variant, the lower part, the upper pair, the key and every value that [G] prints for the pair are recomputed from the 128-byte messages of [G, Table 5] (Section 4; check-2913 trial 0).
2. **Independent exact recounts** of the counts of [G, Table 2] (|V7| = 2^14 in 512 aligned blocks, 4 values of W8, rows 17, 25, 26 and 30), by a 2^32 brute force in C and by the GF(2) method of check-2913 (Section 10.2).
3. **The variant count.** The core admits 1,572,864 variants, of which 1,312 can satisfy row 25 and 32 have one of the two best values of tau (Section 4.3). This filing uses one.
4. **A deterministic upper-pair table** (P2): stated by the C program of Appendix A, which is normative and built the table in full; checked against an independent Python port (`experiments/p2slice.py`); its step-18 and step-19 rates measured (Sections 5, 6.1, 10.3). It is the subset of [G]'s table with minimal carries in E16 and A16, with N 8.6% smaller.
5. **The tail after step 19, measured** for the published variant (Section 6.2).
6. **Accounting under collision-frontier-v5** for the published variant alone (Sections 7, 8).

| Term | Value | Section |
|---|---|---|
| per-lower-solution success, published variant, our table | p1 = 2^-57.0764 | 6 |
| lower solutions processed (mu = 0.55) | L = 2^56.2139 | 6 |
| first blocks | 2^53.2139, each <= 4.38 compressions | 7 |
| matches | 2^53.7538, each <= 1 compression | 7 |
| online total | 2^56.0127 | 7 |
| core search, table build, lower table, allowance | 2^56.9478 | 7 |
| **total time** | **2^57.5547** | 7 |
| memory | 955,244,768 bytes = 2^29.8313 <= 2^29.9 | 8 |

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


### 4.3 The core admits 1,572,864 variants, 1,312 of them usable; this filing uses one

A variant is a value of E6 (equivalently A2, by (4)) with dW9 = 0 and some E5 with dW8 = -4. dW9 depends on E6 only on F8, and dW8 depends on E6 and E5 only on F7. Exactly one of the 2^10 patterns on F8 gives dW9 = 0 (so 2^22 values of E6), and counting the joint patterns on F7 union F8 gives 1,572,864 variants, each with exactly one E5 pattern on F7. The published E6 = 99ccff09 is one of them. A 2^32 brute force in C and trial 7 of check-2913 give the same count; trial 7 also builds 16 random variants end to end and checks that they follow the published pair's differences through step 17 with the published key and upper pair.

Row 25 needs D(s1; W23, -a) = tau with tau = -D(s0; W10, d) fixed by the variant. Only 114,398 of the 2^32 words arise as D(s1; x, -a), so most variants can never meet row 25. Enumerating W10 over 2^32 gives 716,800 values with an achievable tau, and 1,312 of them belong to a variant, with 102 distinct values of tau. The two best are tau = 6001fb3f (3,309,568 values of W23) and tau = 6002033f (3,276,800, the published variant); exactly 32 of the 1,312 variants have one of these two. This matches [G, Section 6.1], which uses 32 variants with these two counts. Their values are not published, so this filing uses only the published variant v*.

### 4.4 Upper pairs, keys and live entries

By (1) of [G], W16 = s1(W14) + C16 with the key C16 = W9 + s0(W1) + W0. W14 and W15 depend on the core and the upper pair pi = (A14, A15) only, and the key depends on the lower solution and on H. Both executions have the same key, and by (2), (3) the differences of steps 14..17 depend on the lower solution and H only through the key [G, Section 4.3]. An upper pair is valid if steps 14..16 follow the characteristic with the XOR digits E14 0x21000, A15 0x08010000, E15 0x200 and W15 4, and rows 17 and 30 hold. Its key set K(pi) consists of the keys for which step 17 follows the characteristic. In this filing it is restricted to minimal carries (E16 XOR E16' = 0x00200224, A16 XOR A16' = 4) and to the bit-27 rule E16[27] = E15[27] of [G, Section 4.3]. An entry (c, pi) with c in K(pi) is live if some value of the free word W17 lets step 18 hold. A **match** is a lower solution together with a live entry whose key equals the lower solution's key. Section 5 (P2) states the construction exactly.

## 5. The procedure

Precomputation, executed one process at a time:

- **P1 (advice).** The core of Section 4.1, the variant v* with E5 & F7, the constants w, d, a, the round constants, the 512 block indices of V7 and the 4 values of W8: below 2^12 bytes. The core and the variant v* are outputs of [G]'s core search (52,300 vCPU-hours, charged in Section 7); v* is one of the 32 variants [G] uses (the 20th, [G, Section 9]). [G] does not print their values; we read them from [G]'s published pair, which only publishes them. The GPU run that found that pair produces nothing the procedure needs and is not part of the procedure.
- **P2 (upper-pair table).** Deterministic given the core. The normative statement of steps 1 to 4 is the C program of Appendix A, which built the table: `upper a` for step 1, and in `ksolve.c` the functions `pairs_for`, `kpi` and `q18` with stop_first, the probe cap 1024 and the mix3/splitmix64 seed for steps 2 to 4. `experiments/p2slice.py` is an independent Python port of the same functions under the same names. It is checked equal to the C program on two full A14 values outside the organizer and on a walk prefix inside it (Sections 10.3, 10.6).
  1. *A14 survivors.* Every A14 with a14ok(A14): dE14 = -0x21000 with E14 XOR E14' = 0x21000, dE15 = 0x200 and dW15 = 4, all of which depend on A14 alone. A scan of all 2^32 values (`upper a`, 3.74 CPU-seconds, 2 MB) gives 262,144 = 2^18 survivors, processed in ascending order.
  2. *Valid pairs*, pairs_for(A14). The base variable is x = E15 of the first execution, with E15 XOR E15' = 0x200 (bit 9 of x is 0). For each sign pattern of the Sigma1 and Ch terms of step 16, the difference dE16 is a constant plus a sum selected by GF(2)-linear features of x. For each of the 8 allowed values of dE16 the solutions form affine subspaces of GF(2)^32, and every point of them is walked. Each point gives A15 = x - (A11 - Sigma0(A14) - Maj(A14, A13, A12)) and is tested by piok: A15 XOR A15' = 0x08010000; E15 XOR = 0x200 and W15 XOR = 4 with dW15 = 4; rows 17 and 30; dA16 = 4; dE16 in its set. piok returns the dE16 class 1..8.
  3. *Keys*, kpi(pi, class). The base variable is x = E16 of the first execution, with the digits of the class fixed at bits 21, 9, 5 and 2 (E16 XOR = 0x00200224) and E16[27] = E15[27]. The step-17 E difference must take one of its 4 allowed values: for each sign pattern this is an affine condition on x. dA17 = 0 is a condition on y = A16 = x + kappa, with A16 bit 2 = 0 (A16 XOR = 4) and the Sigma0 and Maj features of y. Every point of each affine solution space is walked, and the key is c = x - P16(pi). At most 2^16 keys are kept per pair, in walk order.
  4. *Liveness*, live(pi, c). With W17 = 0, steps 16 and 17 of both executions are computed. The base variable is x = E17, with the dE17 digits fixed at bits 27, 23 and 9 (E17 XOR = 0x08800200, minimal carries). dE18 = 0 is an affine condition on x per sign pattern, and dA18 = 0 is a condition on y = A17 = x + kappa read through Maj features. For each sign pattern with solutions, the affine space is walked completely if it has at most 1024 points. Otherwise 1024 points are drawn from it with a splitmix64 stream seeded by mix3(A14, A15, c). The entry is live at the first passing point.
  5. *Layout.* Each live entry (c, pi) gives a reduced key r = c mod 2^30 and the top bits c >> 30. Entries of one pair with the same r merge into one **item** with a 4-bit mask of the top-bit values present. Pair ids 0, 1, 2, ... go to the pairs with at least one live entry, in processing order (ascending A14, then pairs_for order). An item is one 32-bit word: the 6 low bits of r, the 21-bit pair id and the mask. Items are grouped by bucket b = r >> 6 (24 bits), with 2^24 bucket offsets of 4 bytes, and sorted within each bucket. A pair record holds (A14, A15), 8 bytes.
  6. *Two passes.* Pass 1 runs steps 1..4 and counts items per bucket (2^24 counters) and pairs; prefix sums turn the counts into offsets. Pass 2 repeats steps 1..4 and writes each item at its bucket's cursor (2^24 cursors) and each pair record. Each bucket is then sorted.
  
  P2 yields 16,780,994 valid pairs, 2,170,027,812 entries, N = 780,584,493 live entries in 1,755,653 pairs, 195,453,998 items and a layout of 862,970,080 bytes. One pass costs 42,924 CPU-seconds (Section 10.3).
- **P3 (lower table of v*).** For each of the 2^21 lower candidates store (theta, A0, A1) (12 bytes), sorted by theta >> 5; a bitmap over the 2^27 values of theta >> 5 marks the non-empty buckets; a directory (2^22 slots of 8 bytes) maps a non-empty bucket to its range.
- **P4 (allowance).** The characteristic search, the skeleton search and screening, earlier cores and development, which [G] does not report, are charged as an allowance (premise H6).

Online, for i = 1, ..., N_FB with N_FB = 2^53.2139 (Section 6), stopping at the first collision:

1. Draw M0 (two uniform 256-bit words) and compute H = F38(IV, M0). Write H0 = 32h + l with 0 <= l < 32, and compute the per-H constants of W0 and W1.
2. **Lower solutions.** For each g in (h + B) union (h + B + 1) mod 2^27, where B is the set of 512 block indices of V7, test the bitmap at g. For a non-empty bucket g read its records; a record is a lower solution if (g - h in B and theta_l >= l) or (g - h - 1 in B and theta_l < l), where theta_l = theta mod 32. This is the condition theta - H0 in V7, because V7 is a union of complete aligned blocks of 32 (check-2913 trial 1).
3. **Key.** For a lower solution compute W0 = A0 + k_H(H), W1 from E0, E1 (eq. (4), (5)), W9 = E9 - A5 - E5 - Sigma1(E8) - Ch(E8, E7, E6) - K9, and c = W9 + s0(W1) + W0.
4. **Matches.** With r = c mod 2^30 read the offsets of bucket r >> 6 and scan its items (11.65 on average). An item matches if its 6 key bits equal r mod 64 and its mask contains c >> 30; its pair id gives (A14, A15). For a match compute steps 16..18 of both executions (W16 = s1(W14) + c; W17, W18 from W1, W2, W3, W10, W11, W15, W16).
5. **Completion.** If dA18 = dE18 = 0, build M1 and M1' by (5), compute F38(H, M1) and F38(H, M1') and compare. On equality output M0 || M1 and M0 || M1'.

This is Algorithm 1 of [G] with one variant instead of 32, our table in place of [G]'s, and a bitmap scan over V7's blocks in place of [G]'s grouped bucket table. [G]'s grouping depends on the concentration of theta over its 32 variants, which is not published. The step-18 test and the completion are those of [G].

## 6. Success probability

### 6.1 The rates up to step 19 are measured on our table

**Lemma 6.1.** Under premise H1, for every lower solution, whatever its variant: the expected number of matches is N / 2^32; the expected number of step-18 passes is the sum over live entries of q18(c, pi) divided by 2^32, where q18 is the fraction of W17 values that pass step 18 for that entry; and the probability of step 19 given step 18 depends only on the step-18 state.

*Argument.*
1. Under H1, W0..W7 are independent and uniform (Section 2). A lower solution is selected by W7 in V7 alone.
2. Its key c = W9 + s0(W1) + W0 is uniform, because W0 is uniform and independent of W1 and W7. So each live entry is matched with probability 2^-32.
3. Given a match (c, pi), W1 is uniform, and W2 is uniform and independent of (W0, W1, W7). So W17 = s1(W15) + W10 + s0(W2) + W1 is uniform and independent of the entry.
4. Step 18 depends only on (c, pi), the core and E17, which is a function of (c, pi, core) plus W17. So its probability per match is q18(c, pi).
5. W18 = s1(W16) + W11 + s0(W3) + W2 contains the free uniform word W3. So E18 is uniform and independent of the step-18 state. []

Measured on the table of P2 (Section 10.3):
- **Matches** per lower solution: N / 2^32 = 780,584,493 / 2^32 = 0.181744, exact given Lemma 6.1.
- **Step 18 per live entry.** The sample is the 190,447 live entries with ((mix3(A14, A15, c) >> 40) & 4095) = 0, a hash-selected 1/4096 sample. For each, the number of E17 values with minimal carries that pass step 18 was counted exactly, by walking every affine solution space (`q18_res`, Appendix A).
  - Mean q18 = 8.4705e-5, standard deviation over entries 5.65e-5, standard error 1.30e-7 (0.15%).
  - Every sampled entry has at least 256 passing values, and the largest rate is 2.44e-4.
  - E17 values with non-minimal carries add nothing measurable. On 5,216 entries, the exact minimal-carry count matches a modular Monte Carlo of step 18 over all W17, with mean ratio 0.9995 and mean squared z 0.98 (`ksolve qcheck`).
- **Step 18 per lower solution**: 0.181744 x 8.4705e-5 = 1.5395e-5 +- 2.4e-8.
- **Step 19 given step 18.** For each sampled entry, 32 passing E17 values were drawn by reservoir sampling, with 32 uniform W18 values each.
  - Weighted by step-18 passes the rate is 0.015631 +- 0.000012, and weighted by entry it is 0.015624.
  - The rate is flat across the deciles of q18 (0.01556 to 0.01566).

[G, Table 4] gives 0.198823 matches, 1.5925e-5 and 0.015367 for its larger table. Ours has 8.6% fewer entries and 3.3% fewer step-18 passes per lower solution; its step-19 rate is 1.7% higher. These are no longer used.

### 6.2 The tail after step 19 is measured for the published variant

A pair of depth at least 20 collides exactly when steps 20..24 and rows 25 and 26 hold. The free words after step 19 enter in four layers:

| Layer | Free word | Conditions it pays | Rate on the published state |
|---|---|---|---|
| 1 | W19 | step 20 | 2^-9.902 |
| 2 | W20 | step 21 | 2^-6.994 |
| 3 | W21 | step 22 and row 25 | 2^-13.335 |
| 4 | W22 | step 23 and row 26 | 2^-3.754 |

The difference test of step t does not involve W_t, which cancels, so each layer's free word pays the conditions listed. Step 24 held for all 4,001,764 pairs that reached step 23. Within layers 3 and 4, the joint rates of the state condition and the message-expansion row agree with the products of the marginals to 0.015 bit (2^-13.3354 against 2^-13.3504, and 2^-3.7539 against 2^-3.7517). So the constants through which the variant and the lower part enter W23 and W24 do not shift the rate, and the variant enters the tail only through its row-25 count.

**The estimate.** The estimator samples 13,949 states the way the attack reaches step 19:
- an entry drawn in proportion to its measured step-18 rate;
- W7 from V7, W8 from the four row-23 values, W9 from the variant and E5;
- W17 drawn until step 18 passes, and W18 until step 19 passes.

Each state's tail is a nested mean over the four layers (8, 4 and 8 branches kept per layer, each weighted by its layer's measured pass fraction). For tau = 6002033f this gives **2^-35.0897 +- 0.0139 bit**. Two cross-checks:
- [G]'s own estimator, which draws W4, W5, W6 and derives W19..W22, gives 2^-35.0889 +- 0.0371 over the two best tau.
- The model with W19..W22 independent and uniform gives 2^-35.0915 +- 0.0260.

[G] states 2^-35.082. Half of the states that pass step 19 admit no step 20 at all and contribute zero; the average includes them.

With these measurements, p1 = 1.5395e-5 x 0.015631 x 2^-35.0897 = **2^-57.0764** per lower solution.

### 6.3 Fifty-five percent of the expected work gives success probability 0.42

The procedure processes N_FB = 2^53.2139 first blocks, so the expected number of lower solutions is L = 8 N_FB = 2^56.2139, and the expected number of collisions is mu = L p1 = 0.55.
- **Independence.** First blocks are drawn independently and the advice and tables are fixed, so successes in different first blocks are independent; only successes within one first block can cluster.
- **Bound.** Under premise H4 (Poisson approximation within a first block), Pr[at least one collision] >= 1 - e^-0.55 = 0.4231 >= 0.39.
- **Margin.** The threshold needs mu >= 0.4943, so the true p1 may be 10% below the stated value (0.15 bit) before the success probability falls below 0.39.
- **Probability space.** The procedure's coins: the first blocks M0 are drawn uniformly and independently. The advice of P1 is fixed, and P2 and P3 are deterministic given it.
- **Second-moment alternative.** If only Pr[X >= 1] >= E[X]^2 / E[X^2] is admitted, with pairwise non-positive correlation of distinct successes, mu = 0.64 is needed: time +0.0789 bit (Section 7.3).

## 7. Time

### 7.1 Unit costs

One 38-step compression costs 1; any other 256-bit word operation costs 1/2728 (cost model v5). 32-bit arithmetic is charged with its masks; a 32-bit rotation costs 4 operations (two shifts, an OR, a mask). Each table read is one 256-bit load.

| Unit | Bound | Itemization |
|---|---|---|
| first block | 1 + 9216/2728 = 4.378 | the compression of M0 (1); M0 from two random words (2 ops); the per-H constants of W0 and W1 (< 80 ops); 1024 bitmap probes of 8 ops each (8,192 ops); on average at most 1024 x 2^21 / 2^27 = 16 non-empty buckets, each a directory probe (< 40 ops). Total < 9,216 ops |
| lower solution | 384/2728 = 0.1408 | records examined: E[examined] <= 2 E[lower solutions], because a candidate's bucket is reached for at most 2 x 512 of the 2^27 values of h while it is a solution for 512 of them on average (2 records x 12 ops); W9 (3); W0 (2); E1 (25); W1 (29); s0(W1) (11); key (4); table probe: bucket index (3), two offsets (2 loads, 4 ops), 11.65 items on average at 6 ops each (load share, key-bit extraction, compare, mask test, branch: 70). About 175 ops, bound 384 |
| match | 1 | pair id and record (A14, A15) (5); recompute E14, E15, W14, W15 of both executions (< 320 ops); W2, W3 (< 120); steps 16, 17, 18 of both executions with W16, W17, W18 (< 900); compare (4). About 1,350 ops, bound 2,728 |
| step-18 pass | 3 | M1, M1' by (5) (< 1 compression), two compressions, compare |

### 7.2 Ledger

With L = 2^56.2139 expected lower solutions (Section 6.3), N_FB = L / 8, matches 0.181744 L and step-18 passes 1.5395 x 10^-5 L:

| Term | Count | Unit | log2 of the cost |
|---|---|---|---|
| first blocks | 2^53.2139 | 4.378 | 55.3442 |
| lower solutions | 2^56.2139 | 0.1408 | 53.3852 |
| matches | 2^53.7538 | 1 | 53.7538 |
| step-18 passes | 2^40.2266 | 3 | 41.8116 |
| **online** | | | **56.0127** |
| core search (P1): 52,300 vCPU-hours at R = 2^26 per vCPU-second | 2^27.4883 vCPU-s | 2^26 | 53.4883 |
| table (P2): two passes of 42,924 CPU-seconds | 2^16.3895 CPU-s | 2^26 | 42.3895 |
| A14 scan (P2 step 1): 2^32 evaluations of a14ok, each two E14 values and the dE15 and dW15 terms (< 160 ops, charged 256; measured 3.74 CPU-seconds) | 2^32 | 256/2728 | 28.5866 |
| lower table (P3): 2^21 candidates, 1024 ops each incl. sorting | | | 19.5864 |
| allowance (P4, premise H6): 10 x the core search | | | 56.8102 |
| **preprocessing** | | | **56.9478** |
| **total** | | | **57.5547** |

The time is the expected work of the full budget of N_FB first blocks, which bounds the expected work of the procedure that stops at the first collision. The time claim is 57.56.

**Rate envelope R.** The core search ran on CPUs ([G]: Arm machines), and our table build on an Apple M1 Pro. The word-RAM work of one vCPU-second is bounded by its instruction throughput.
- A server vCPU issues at most 8 instructions per cycle at most 4 GHz, each on at most 512 bits (two 256-bit words). That is at most 2^35.9 primitive operations per second, or 2^24.5 compressions.
- For an Arm Neoverse core (at most 2.8 GHz, 8-wide, vectors of at most 256 bits) the bound is 2^34.4 operations, or 2^23.0 compressions. An M1 Pro performance core (3.2 GHz, 8-wide, 128-bit vectors) is inside the first envelope.
- R = 2^26 leaves a factor of 2.8 and 8 respectively for instructions that combine several primitive operations (premise H5). A CDCL solver is bound by memory latency in unit propagation and runs well below the issue width.

### 7.3 Sensitivity

| Change | time_log2 | score |
|---|---|---|
| this claim | 57.5547 | 67.4547 |
| R = 2^25 | 56.9806 | 66.8806 |
| R = 2^30 | 60.9942 | 70.8942 |
| allowance 0 | 56.2440 | 66.1440 |
| allowance 1 x core search | 56.4432 | 66.3432 |
| allowance 100 x core search | 60.2264 | 70.1264 |
| R = 2^30 and allowance 100 x | 64.1516 | 74.0516 |
| second-moment bound (mu = 0.64) | 57.6336 | 67.5336 |
| mu = 0.5 (success 0.3935) | 57.5090 | 67.4090 |

## 8. Memory

The procedure's peak memory is that of the online tables:

| Item | Bytes |
|---|---|
| table bucket offsets: 2^24 x 4 | 67,108,864 |
| table items: 195,453,998 x 4 | 781,815,992 |
| pair records (A14, A15): 1,755,653 x 8 | 14,045,224 |
| lower table of v*: 2^21 x 12 + bitmap 2^24 + directory 2^22 x 8 | 75,497,472 |
| code, advice, constants and working state | <= 16,777,216 |
| **total** | **955,244,768 = 2^29.8313** |

The claim is 2^29.9 = 1,001,836,546 bytes. [G]'s 7.35 GB of tables and 18 GB of GPU batching buffers belong to its implementation; the procedure here processes one first block at a time and needs a few kilobytes of working state.

**Scope of the peak.** The peak covers the online procedure and every computation whose output the procedure reads, executed one process at a time:
- **Searches.** The unreported searches (P4) and the core search produce the characteristic and the advice of P1. Their processes (SAT solving, CaDiCaL with an external propagator in [G], and bit-serial depth-first search) are bounded by premise H7 at 2^29.9 bytes each.
- **Table construction (P2).** The A14 scan holds 2 MB. Pass 1 holds 2^24 counters (67 MB) and the state of one A14. Pass 2 holds the final layout (862,970,080 bytes), 2^24 cursors (67,108,864 bytes) and the working state, 946,856,160 bytes in all, below the online peak.
- **Lower table (P3).** It needs below 10^8 bytes.
- **Online phase.** The peak above.

Total time is unchanged by sequential execution, since v5 charges work summed over processors. [G]'s GPU run is not part of the procedure: it produces nothing the procedure reads.

The studies that support the premises are evidence, not part of the procedure, and their memory is not charged:
- our build of the table, which ran as 8 chunk processes one after another, each multi-threaded at 556 MB, including a 512 MB key bitmap kept only for statistics;
- the rate measurements, the tail estimate and the skeleton study;
- [G]'s counts and run;
- our brute-force counts.

## 9. Heuristic premises

- **H1 (uniform chaining value).** For M0 drawn uniformly by the procedure, H = F38(IV, M0) behaves as a uniform 256-bit value for the events of the attack: the selection W7 in V7, the key, and the free words W2..W6. Evidence: [G]'s run processed 2^47.0 first blocks and 1.52 x 10^16 lower solutions, 108.0 per first block (rounded inputs) against 108.39 predicted for its configuration; its step-18 rate over the run (real chaining values) is 1.5929 x 10^-5 against 1.5925 x 10^-5 counted. Trial 8 of check-2913 checks the bijection H <-> W0..W7 used in Section 2.
- **H2 (rates of our table).** The table of P2 has N = 780,584,493 live entries. Its mean step-18 rate per live entry is 8.4705 x 10^-5 +- 1.30 x 10^-7, and step 19 given step 18 is 0.015631 +- 0.000012. With Lemma 6.1 they give 0.181744 matches and 1.5395 x 10^-5 step-18 passes per lower solution.
  - Evidence: the build and the exact counts on the hash-selected 1/4096 sample (Sections 6.1 and 10.3).
  - The minimal-carry restriction of E17 loses nothing measurable (`qcheck`, ratio 0.9995).
  - The organizer experiment p2slice runs the Python port of the construction on two A14 values against the stored C build.
  - Limitations: sample estimates with the stated standard errors; step 19 is a Monte Carlo estimate.
- **H3 (tail).** For the published variant (tau = 6002033f), a pair passing step 19 collides with probability 2^-35.0897 +- 0.0139 bit.
  - Evidence: the nested four-layer estimate on 13,949 states drawn as the attack reaches step 19 (Section 6.2).
  - The constants through which the variant enters W23 and W24 are measured not to shift the rate (0.015 bit).
  - [G]'s own estimator on our states gives 2^-35.0889, and [G] states 2^-35.082.
  - Rows 25 and 26 are exact counts (check-2913 trials 3, 4).
  - Limitations: an estimate rather than a count. The entries were drawn from a pool of 5 upper pairs, weighted by step-18 rates measured on that pool, so the state sample represents that pool, not provably the whole table.
- **H4 (Poisson).** With mu = 0.55 expected collisions, Pr[at least one] >= 1 - e^-0.55 = 0.4231.
  - Evidence: p1 = 2^-57.08 per lower solution. Successes in different first blocks are independent (independent first blocks, fixed tables), so only clustering within one first block is assumed small. Distinct lower solutions of one first block differ in A0, A1 and hence in W0..W3, and the tail depends on the free words W4..W6.
  - The threshold needs mu >= 0.4943, which leaves a 10% margin on p1.
  - Sensitivity: the second-moment bound costs +0.0789 bit.
- **H5 (precomputation and rate envelope).** The computation that produced the core took 52,300 vCPU-hours, as [G, Sections 6.1 and 7.2] reports. One pass of P2 took 42,924 CPU-seconds by our measurement (user and system time, summed over the 8 chunk processes), and the A14 scan 3.74 CPU-seconds (charged by its operation count). A vCPU-second performs at most R = 2^26 compressions' worth of word-RAM work.
  - Evidence: [G]'s statement (also US$290 for the core search); the per-chunk CPU records (Section 10.3); the instruction-throughput bound of Section 7.2.
  - Limitation: the core search's cost is one realized run, and the expected cost of a fresh core search is not established. The procedure uses the produced core as advice and charges the realized cost of the search that produced it.
- **H6 (allowance for unreported search).** The characteristic search, the skeleton search and screening, earlier cores and development cost at most 10 times the core search, 523,000 vCPU-hours.
  - Basis: [G, Section 6.1] describes skeletons generated by a SAT model of both executions and screened by the number of step-17 entries of the cores obtained from them. [G, Section 7.2] reports only the final core search.
  - Measured part: generating a skeleton costs at most 0.75 CPU-s and 14.6 MB per skeleton (Kissat on the two-execution model of steps 11..20, CNF build included, worst of 20 seeds), and one CaDiCaL instance enumerates 25,278 distinct skeletons in 587 CPU-s (Section 10.5). Skeleton generation is therefore negligible against the allowance.
  - What the allowance covers is the screening: obtaining cores from skeletons that were then discarded. It is unreported and unmeasured, and the allowance admits ten core searches of the reported size.
  - Sensitivity: Section 7.3.
- **H7 (memory of the SAT searches).** Each process of [G]'s core search and of the unreported searches of P4 used at most 2^29.9 bytes.
  - Evidence: in our skeleton study, every process peaked at or below 568 MB = 2^29.1 bytes. The largest was an enumeration holding 120,000 blocking clauses. Stage-2 completion of [G]'s published skeleton peaked at 11 to 36 MB, and a SAT stand-in for stage 3 at 38 to 139 MB.
  - An earlier Kissat solve on a 38-step characteristic peaked at 2^26.08 bytes. The depth-first stage 3 of [G] uses negligible memory.
  - Limitation: [G]'s CaDiCaL with an external propagator was not reproduced, and [G] does not report the memory of its SAT runs.

## 10. Evidence

### 10.1 [G]'s run and collision

The GPU run of [G, Section 8.2] processed 2^47.0 first blocks and 1.52 x 10^16 lower solutions in 53.3 GPU-hours and found the collision after about 10% of the expected work. A single success does not establish the expected cost; it shows that the procedure produces collisions. [G] reports that the GPU program's matches and depths are identical to those of a CPU implementation on four ranges of 2^28 first blocks, and that the collision was checked with five independent implementations. Trial 0 of check-2913 returns it, and the organizer's harness recomputes its digests.

### 10.2 Our reconstruction and exact counts

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

### 10.3 The table: build, totals and checks

The C program of Appendix A (`ksolve table`) ran P2 over all 2^18 A14 survivors in 8 chunks of 32,768. `merge` combined the chunks and `layout` sized the layout.

| Quantity | Ours | [G] |
| --- | --- | --- |
| A14 survivors | 262,144 | n/a |
| valid upper pairs | 16,780,994 | 1.68e7 |
| entries after the bit-27 rule | 2,170,027,812 (minimal carries) | 2.32e9 (all carries) |
| live entries N | 780,584,493 (36.0%) | 853,938,951 (37%) |
| upper pairs with live entries | 1,755,653 | 2,345,041 |
| distinct live keys / reduced keys | 713,617,711 / 178,660,864 | n/a / 193,853,061 |
| items (reduced key, pair) | 195,453,998 = N / 3.994 | n/a |
| layout | 862,970,080 bytes | 5.44 GB hash table |
| CPU per pass | 42,924 s | 42 vCPU-hours |

**Checks.**
- **Brute-force keys.** For 64 random valid pairs, K(pi) was enumerated over all 2^32 keys (`upper c`). kpi finds every key with minimal A16 carry (0 misses); the only keys it omits, 128 of one pair, have a non-minimal A16 carry and are all dead (`ksolve kcheck`).
- **Liveness.** The step-18 count with minimal E17 carries agrees with a modular Monte Carlo over all W17 (ratio 0.9995 on 5,216 entries).
- **Determinism.** The stored chunk records for A14 = 5bde5962 equal a fresh single-A14 run: 192 valid pairs, 81,552 entries, 29,655 live entries in 64 pairs. They include the published pair (class 7) and the published key 00b50618 among its 789 live keys.
- **Python port.** The independent port `experiments/p2slice.py`, run outside the organizer, rebuilds A14 = 5bde5962 and A14 = 4f9d3ed0 (256 valid pairs, 1,024 entries, 304 live entries in 2 pairs) completely. Its live keys are identical, pair by pair, to the stored C records.
- **Rates.** The sampled entries reproduce the step-18 and step-19 figures of Section 6.1 in a second run with the same seeds (`ksolve rates`). The chunk means of the step-18 rate lie in 8.44e-5 to 8.50e-5.

### 10.4 The tail estimate

`tail38` (our program; it rebuilds the published pair from its messages and confirms the condition list of Section 6.2 on it) produced the estimates of Section 6.2. On the published state, row 25 came out at 2^-10.347 and row 26 at 2^-2.752, against the exact 2^-10.3561 and 2^-2.7521.

### 10.5 Skeleton generation is measured; screening is not

Stage 1 of [G]'s core search was modeled as the exact two-execution CNF of steps 11..20 with Table 3 fixed.
- **Skeleton generation.** One skeleton costs 0.13 to 0.75 CPU-s with Kissat 4.0.1 at 14.6 MB, and one incremental CaDiCaL instance enumerated 25,278 distinct skeletons in 587 CPU-s.
- **[G]'s skeleton.** It satisfies the model (forced: SAT in 1.1 to 1.7 CPU-s) but appeared in none of 25 fresh runs and none of the 25,278 enumerated skeletons. Completing its late states from the published A14 and E14 takes about 1 CPU-s at 11 to 36 MB.
- **Screening.** It is not reproduced. By our SAT route, a core from [G]'s skeleton costs at least 204 CPU-s (95% bound): 188,300 random completions gave no backward extension.

### 10.6 The organizer experiments

**check-2913** (`experiments/check2913.py`, under 2 seconds) runs nine checks, one per trial, and returns a pair only when its check passes:

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

The exact counts enumerate the carry paths of x + e. On each path the XOR difference D = (x + e) XOR x and some bits of x are fixed. With Y = sigma(D), sigma(x + e) - sigma(x) = Y - 2(sigma(x) AND Y), so the condition is affine in x over GF(2), and its solutions are counted by elimination. The counts equal the C brute force of Section 10.2.

**p2slice** (`experiments/p2slice.py`, an independent Python port of steps 1 to 4 of P2, about 4 seconds) runs the port on two A14 values against the stored C build and returns a non-colliding marker pair per trial only if every comparison holds:
- **Trial 0, A14 = 5bde5962.**
  - a14ok holds.
  - The solver on the first 2^16 points of each affine space of x = E15 finds the expected pairs.
  - All 192 valid pairs of the C build pass piok with their classes.
  - For the published pair, K(pi) has 2,496 keys, including 00b50618. Testing every one of them, its live keys are exactly the 789 stored by the C build, and the published key is live.
- **Trial 1, A14 = 4f9d3ed0.**
  - The same walk-prefix and validity checks hold.
  - K(pi) of all 256 valid pairs has 1,024 keys, as in the C build.
  - Testing every entry, the live keys are exactly the 304 stored by the C build, in the same 2 pairs.

A full walk of one A14 takes about 10 s in Python, so the organizer trials walk a prefix of each space. The full walks were compared outside the organizer (Section 10.3). In our runs in the pinned image (two runs each, byte-identical output) both experiments return a pair on every check trial, and check-2913 trial 0 is a full collision.

## 11. Limitations

- **Rates.** The step-18 and step-19 rates of our table are sample estimates (1/4096 of the live entries) with the stated standard errors. The tail is an estimate on states from a pool of 5 upper pairs.
- **Organizer coverage.** The organizer runs the Python port on two A14 values, with a walk prefix; the full table was built only by the C program, which is the normative statement of P2.
- **Precomputation cost.** The core search's cost is one realized run as [G] reports it. The screening of skeletons is covered by an allowance without a measurement (H5, H6).
- **First blocks.** The procedure uses one variant; its first-block cost (4.378 compressions) is an itemized bound, not a measurement.

## Appendix A. The C programs that built and measured the table

These programs are the normative statement of steps 1 to 4 of P2. `upper.h` holds the core words of both executions needed for steps 14..19 and the published upper pair. `upper.c` holds the step functions, a14ok (`upper a` scans all 2^32 A14 values) and the brute-force K(pi) of `upper c`. `ksolve.c` holds the solvers; `ksolve table a14.bin lo hi out` builds the chunk of A14 indices lo..hi, and the modes `rates`, `kcheck`, `qcheck`, `live` and `pcheck` produce the checks of Section 10.3. `merge.c` and `layout.c` give the totals and the layout size. Compiled with `gcc -O2 -fopenmp -lm` in Docker image `sha2sat:2`.

### A.1 `upper.h`

```c
#define A9_0 0x88f2acf8u
#define A9_1 0x2aa7318eu
#define A10_0 0x959ea855u
#define A10_1 0xd935a3b4u
#define A11_0 0x9871db5eu
#define A11_1 0x9991eb9fu
#define A12_0 0x6a30e20fu
#define A12_1 0x63b1f047u
#define A13_0 0xdad82f20u
#define A13_1 0xd2793d21u
#define E10_0 0x1e38fd64u
#define E10_1 0x85ade09bu
#define E11_0 0xe66f7c72u
#define E11_1 0x2017f638u
#define E12_0 0xa994479eu
#define E12_1 0xaff6c796u
#define E13_0 0xc21a9d0du
#define E13_1 0x86580f08u
#define PUB_A14 0x5bde5962u
#define PUB_A15 0x9b3a6d8au
#define PUB_KEY 0x00b50618u
#define PUB_W17 0x0c4ae1b7u
#define PUB_W18 0x4f9111edu
#define CA 0xf8010000u
```

### A.2 `upper.c`

```c
// Upper side of ePrint 2026/2913 (Goldzweig) on the core recovered from the published pair (upper.h).
//   ./upper check            published upper pair, key, W17, W18 pass steps 14..19
//   ./upper a out.bin        all A14 meeting the A14-only conditions (dE14, dE15, dW15)
//   ./upper b a14.bin n seed out.txt   valid upper pairs for n sampled A14 (2^30 loop over A15 each)
//   ./upper c pi.txt S seed out.txt    for each upper pair: K(pi) over 2^32 keys (bit-27 rule applied),
//                                     then per entry two independent sets of S W17 samples (step-18 rate)
//                                     and W18 samples for every step-18 pass (step-19 rate)
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include "upper.h"
typedef uint32_t u32; typedef uint64_t u64;
static inline u32 rr(u32 x,int n){return (x>>n)|(x<<(32-n));}
static inline u32 s0(u32 x){return rr(x,7)^rr(x,18)^(x>>3);}
static inline u32 s1(u32 x){return rr(x,17)^rr(x,19)^(x>>10);}
static inline u32 S0(u32 x){return rr(x,2)^rr(x,13)^rr(x,22);}
static inline u32 S1(u32 x){return rr(x,6)^rr(x,11)^rr(x,25);}
static inline u32 ch(u32 x,u32 y,u32 z){return (x&y)^(~x&z);}
static inline u32 mj(u32 x,u32 y,u32 z){return (x&y)^(x&z)^(y&z);}
static const u32 K14=0x9bdc06a7u,K15=0xc19bf174u,K16=0xe49b69c1u,K17=0xefbe4786u,K18=0x0fc19dc6u,K19=0x240ca1ccu;
static const u32 A10[2]={A10_0,A10_1},A11[2]={A11_0,A11_1},A12[2]={A12_0,A12_1},A13[2]={A13_0,A13_1};
static const u32 E10[2]={E10_0,E10_1},E11[2]={E11_0,E11_1},E12[2]={E12_0,E12_1},E13[2]={E13_0,E13_1};
static u64 sm(u64 *s){u64 z=(*s+=0x9e3779b97f4a7c15ull);z=(z^(z>>30))*0xbf58476d1ce4e5b9ull;z=(z^(z>>27))*0x94d049bb133111ebull;return z^(z>>31);}
typedef struct {u32 A14,A15[2],E14[2],E15[2],W14,W15[2];} up_t;
static void upset(up_t*u,u32 A14,u32 A15){
  u->A14=A14; u->A15[0]=A15; u->A15[1]=A15+CA;
  for(int k=0;k<2;k++){
    u->E14[k]=A14+A10[k]-S0(A13[k])-mj(A13[k],A12[k],A11[k]);
    u->E15[k]=u->A15[k]+A11[k]-S0(A14)-mj(A14,A13[k],A12[k]);
    u->W15[k]=u->E15[k]-A11[k]-E11[k]-S1(u->E14[k])-ch(u->E14[k],E13[k],E12[k])-K15;
  }
  u->W14=u->E14[0]-A10[0]-E10[0]-S1(E13[0])-ch(E13[0],E12[0],E11[0])-K14;
}
// dE16 in {e1 2^21 - 2^9 + e2 2^5 + e3 2^2}, dE17 in {e4 2^27 + e5 2^23 - 2^9}  (s = -1 for this core)
static int inset16(u32 d){for(int m=0;m<8;m++){u32 v=((m&1)?0x200000u:-0x200000u)-0x200u+((m&2)?0x20u:-0x20u)+((m&4)?4u:-4u); if(d==v) return m+1;} return 0;}
static int inset17(u32 d){for(int m=0;m<4;m++){u32 v=((m&1)?0x8000000u:-0x8000000u)+((m&2)?0x800000u:-0x800000u)-0x200u; if(d==v) return m+1;} return 0;}
static inline int a14ok(u32 A14){
  u32 E0=A14+A10[0]-S0(A13[0])-mj(A13[0],A12[0],A11[0]), E1=A14+A10[1]-S0(A13[1])-mj(A13[1],A12[1],A11[1]);
  if(E1-E0!=(u32)-0x21000 || (E0^E1)!=0x21000u) return 0;
  u32 dE15=CA+(A11[1]-A11[0])-(mj(A14,A13[1],A12[1])-mj(A14,A13[0],A12[0]));
  if(dE15!=0x200u) return 0;
  u32 g0=-S0(A14)-mj(A14,A13[0],A12[0])-E11[0]-S1(E0)-ch(E0,E13[0],E12[0]);
  u32 g1=-S0(A14)-mj(A14,A13[1],A12[1])-E11[1]-S1(E1)-ch(E1,E13[1],E12[1]);
  return CA+g1-g0==4u;
}
// full validity of an upper pair (steps 14..16, XOR exactness, rows 17 and 30); returns dE16 class or 0
static int piok(const up_t*u){
  if((u->A15[0]^u->A15[1])!=0x08010000u) return 0;
  if(u->E15[1]-u->E15[0]!=0x200u || (u->E15[0]^u->E15[1])!=0x200u) return 0;
  if(u->W15[1]-u->W15[0]!=4u || (u->W15[0]^u->W15[1])!=4u) return 0;
  if(s1(u->W15[1])-s1(u->W15[0])!=(u32)-0x28000) return 0;       // row 17: dsigma1(W15;4) = -d
  if(s0(u->W15[1])-s0(u->W15[0])!=CA) return 0;                  // row 30: dsigma0(W15;4) = a
  u32 E16[2],A16[2];
  for(int k=0;k<2;k++){E16[k]=A12[k]+E12[k]+S1(u->E15[k])+ch(u->E15[k],u->E14[k],E13[k])+K16;  // + W16 (same in both)
    A16[k]=E16[k]-A12[k]+S0(u->A15[k])+mj(u->A15[k],u->A14,A13[k]);}
  if(A16[1]-A16[0]!=4u) return 0;
  return inset16(E16[1]-E16[0]);
}
typedef struct {u32 E16[2],A16[2],E17[2],A17[2];} st_t;
static inline void step16(const up_t*u,u32 c,st_t*s){
  u32 W16=s1(u->W14)+c;
  for(int k=0;k<2;k++){s->E16[k]=A12[k]+E12[k]+S1(u->E15[k])+ch(u->E15[k],u->E14[k],E13[k])+K16+W16;
    s->A16[k]=s->E16[k]-A12[k]+S0(u->A15[k])+mj(u->A15[k],u->A14,A13[k]);}
}
static inline void step17(const up_t*u,st_t*s,u32 W17){
  for(int k=0;k<2;k++){s->E17[k]=A13[k]+E13[k]+S1(s->E16[k])+ch(s->E16[k],u->E15[k],u->E14[k])+K17+W17;
    s->A17[k]=s->E17[k]-A13[k]+S0(s->A16[k])+mj(s->A16[k],u->A15[k],u->A14);}
}
static inline int step18(const up_t*u,const st_t*s,u32 W18,u32*E18,u32*A18){
  for(int k=0;k<2;k++){E18[k]=u->A14+u->E14[k]+S1(s->E17[k])+ch(s->E17[k],s->E16[k],u->E15[k])+K18+W18;
    A18[k]=E18[k]-u->A14+S0(s->A17[k])+mj(s->A17[k],s->A16[k],u->A15[k]);}
  return E18[0]==E18[1] && A18[0]==A18[1];
}
static inline int step19(const up_t*u,const st_t*s,const u32*E18,const u32*A18){
  u32 E19[2],A19[2];
  for(int k=0;k<2;k++){E19[k]=u->A15[k]+u->E15[k]+S1(E18[k])+ch(E18[k],s->E17[k],s->E16[k])+K19;
    A19[k]=E19[k]-u->A15[k]+S0(A18[k])+mj(A18[k],s->A17[k],s->A16[k]);}
  return E19[1]-E19[0]==CA && A19[0]==A19[1];
}
int main(int argc,char**argv){
  if(argc<2) return 1;
  if(!strcmp(argv[1],"check")){
    up_t u; upset(&u,PUB_A14,PUB_A15); st_t s; u32 E18[2],A18[2];
    printf("a14ok %d piok(dE16 class) %d dW14 %08x\n",a14ok(PUB_A14),piok(&u),
      (u.E14[1]-A10[1]-E10[1]-S1(E13[1])-ch(E13[1],E12[1],E11[1])-K14)-u.W14);
    step16(&u,PUB_KEY,&s); step17(&u,&s,PUB_W17);
    printf("dE17 class %d dA17 %08x bit27 rule %d\n",inset17(s.E17[1]-s.E17[0]),s.A17[1]-s.A17[0],
      ((s.E16[0]>>27)&1)==((u.E15[0]>>27)&1));
    int p18=step18(&u,&s,PUB_W18,E18,A18); printf("step18 %d step19 %d\n",p18,p18&&step19(&u,&s,E18,A18));
    return 0;
  }
  if(!strcmp(argv[1],"a")){
    FILE*f=fopen(argv[2],"wb"); long n=0;
    #pragma omp parallel
    { u32 buf[4096]; int nb=0;
      #pragma omp for schedule(static) reduction(+:n)
      for(long x=0;x<(1L<<32);x++){ if(a14ok((u32)x)){ n++; buf[nb++]=(u32)x; if(nb==4096){
        #pragma omp critical
        fwrite(buf,4,nb,f); nb=0; } } }
      #pragma omp critical
      fwrite(buf,4,nb,f);
    }
    fclose(f); printf("A14 survivors: %ld = 2^%.3f\n",n,__builtin_log2((double)n)); return 0;
  }
  if(!strcmp(argv[1],"b")){
    FILE*f=fopen(argv[2],"rb"); fseek(f,0,SEEK_END); long na=ftell(f)/4; rewind(f);
    u32*a=malloc(na*4); fread(a,4,na,f); fclose(f);
    int n=atoi(argv[3]); u64 seed=strtoull(argv[4],0,10); FILE*o=fopen(argv[5],"w");
    long tot=0;
    for(int i=0;i<n;i++){
      u32 A14= i==0 ? PUB_A14 : a[sm(&seed)%na];
      long cnt=0;
      #pragma omp parallel for schedule(static) reduction(+:cnt)
      for(long y=0;y<(1L<<30);y++){
        u32 A15=(u32)(((y>>16)<<17)|(y&0xffff)); A15=((A15>>27)<<28)|(1u<<27)|(A15&0x7ffffff); // bit16=0, bit27=1
        up_t u; upset(&u,A14,A15); int cl=piok(&u);
        if(cl){ cnt++;
          #pragma omp critical
          fprintf(o,"%08x %08x %d\n",A14,A15,cl); }
      }
      tot+=cnt; fprintf(stderr,"A14 %08x: %ld valid upper pairs\n",A14,cnt);
    }
    fclose(o); printf("valid upper pairs over %d A14: %ld (mean %.2f)\n",n,tot,(double)tot/n); return 0;
  }
  if(!strcmp(argv[1],"c")){
    FILE*f=fopen(argv[2],"r"); u32 pa[100000],pb[100000]; int cl[100000],np=0;
    while(np<100000 && fscanf(f,"%x %x %d",&pa[np],&pb[np],&cl[np])==3) np++; fclose(f);
    long S=atol(argv[3]); u64 seed0=strtoull(argv[4],0,10); FILE*o=fopen(argv[5],"w");
    fprintf(o,"# pi A14 A15 dE16class key dE17class n18a n18b S n19trials n19\n");
    for(int p=0;p<np;p++){
      up_t u; upset(&u,pa[p],pb[p]);
      static u32 keys[1<<20]; static int kcl[1<<20]; int nk=0; long nraw=0;
      #pragma omp parallel for schedule(static) reduction(+:nraw)
      for(long x=0;x<(1L<<32);x++){
        st_t s; step16(&u,(u32)x,&s); step17(&u,&s,0);
        int c17=inset17(s.E17[1]-s.E17[0]); if(!c17 || s.A17[0]!=s.A17[1]) continue;
        nraw++;
        if(((s.E16[0]>>27)&1)!=((u.E15[0]>>27)&1)) continue;
        #pragma omp critical
        { if(nk<(1<<20)){keys[nk]=(u32)x; kcl[nk]=c17; nk++;} }
      }
      #pragma omp parallel for schedule(dynamic,1)
      for(int i=0;i<nk;i++){
        u64 sd=seed0^((u64)p<<32)^(u64)keys[i]; st_t s0_; step16(&u,keys[i],&s0_);
        long n18[2]={0,0},t19=0,n19=0; u32 E18[2],A18[2];
        for(int h=0;h<2;h++) for(long j=0;j<S;j++){
          st_t s=s0_; step17(&u,&s,(u32)sm(&sd));
          if(step18(&u,&s,0,E18,A18)){ n18[h]++;
            for(int r=0;r<64;r++){ u32 W18=(u32)sm(&sd); step18(&u,&s,W18,E18,A18); t19++; n19+=step19(&u,&s,E18,A18); } }
        }
        #pragma omp critical
        fprintf(o,"%d %08x %08x %d %08x %d %ld %ld %ld %ld %ld\n",p,pa[p],pb[p],cl[p],keys[i],kcl[i],n18[0],n18[1],S,t19,n19);
      }
      fflush(o); fprintf(stderr,"pi %d: |K| %ld, bit-27 kept %d\n",p,nraw,nk);
    }
    fclose(o); return 0;
  }
  return 1;
}
```

### A.3 `ksolve.c`

```c
// Fast solvers for the upper side of ePrint 2026/2913 (Goldzweig), core recovered from the published pair.
// Steps 17 and 18 are linear over GF(2) once the signs of the Sigma/Ch/Maj terms are chosen; the only
// non-linear part is a few bits of y = x + kappa, checked while walking the affine solution space.
//
//   ./ksolve kcheck pi.txt ent.txt   K(pi) by the solver vs the brute-force entries of `upper c`
//   ./ksolve qcheck ent.txt          exact step-18 rate (minimal E17 carries) vs the Monte Carlo of `upper c`
#include <time.h>
#include <sys/resource.h>
#define main upper_main
#include "upper.c"
#undef main

static inline int par(u32 x){return __builtin_parity(x);}
// ---------- a modular equation  cst + sum_i (feature_i ? v1_i : v0_i) == target, features = parity(word & mask)
typedef struct { int n; u32 mask[48], v0[48], v1[48]; u32 cst; } eq_t;
static void eq_init(eq_t*e){e->n=0;e->cst=0;}
static void eq_add(eq_t*e,u32 mask,u32 v0,u32 v1,u32 fixm,u32 fixv){
  if(v0==v1){e->cst+=v0;return;}
  if(!(mask&~fixm)){e->cst+=par(fixv&mask)?v1:v0;return;}
  for(int i=0;i<e->n;i++) if(e->mask[i]==mask){e->v0[i]+=v0;e->v1[i]+=v1;return;}
  e->mask[e->n]=mask;e->v0[e->n]=v0;e->v1[e->n]=v1;e->n++;
}
// Sigma-type term: F(w ^ D) - F(w) = Y - 2 (F(w) & Y), Y = F(D); F linear with rotation set r[] (and shift sh, 0 = none)
static void eq_sigma(eq_t*e,u32 D,const int*r,int nr,int sh,u32 fixm,u32 fixv){
  u32 Y=0; for(int k=0;k<nr;k++) Y^=rr(D,r[k]); if(sh) Y^=D>>sh;
  for(int j=0;j<32;j++) if(Y>>j&1){
    u32 m=0; for(int k=0;k<nr;k++) m^=1u<<((j+r[k])&31); if(sh && j+sh<32) m^=1u<<(j+sh);
    eq_add(e,m,1u<<j,(u32)-(1u<<j),fixm,fixv);
  }
}
// bitwise term f(w^D, b1, c1) - f(w, b0, c0), f = ch or maj, one feature per bit of w
static void eq_bitwise(eq_t*e,int isch,u32 D,u32 b0,u32 c0,u32 b1,u32 c1,u32 fixm,u32 fixv){
  for(int i=0;i<32;i++){
    u32 bi0=b0>>i&1,ci0=c0>>i&1,bi1=b1>>i&1,ci1=c1>>i&1,d=D>>i&1; u32 val[2];
    for(u32 v=0;v<2;v++){
      u32 o1= isch ? (((v^d)&bi1)|((~(v^d)&1)&ci1)) : (((v^d)&bi1)|((v^d)&ci1)|(bi1&ci1));
      u32 o0= isch ? ((v&bi0)|((~v&1)&ci0)) : ((v&bi0)|(v&ci0)|(bi0&ci0));
      val[v]=(o1-o0)<<i;   // in {-2^i, 0, 2^i} mod 2^32
    }
    eq_add(e,1u<<i,val[0],val[1],fixm,fixv);
  }
}
// ---------- GF(2) system on 32 unknown bits
typedef struct { int r; u32 row[40]; int rhs[40]; } gs_t;
static int gs_add(gs_t*g,u32 m,int b){
  for(int i=0;i<g->r;i++){int p=31-__builtin_clz(g->row[i]); if(m>>p&1){m^=g->row[i];b^=g->rhs[i];}}
  if(!m) return b==0;
  int p=31-__builtin_clz(m);
  for(int i=0;i<g->r;i++) if(g->row[i]>>p&1){g->row[i]^=m;g->rhs[i]^=b;}
  g->row[g->r]=m;g->rhs[g->r]=b;g->r++; return 1;
}
// affine space of solutions: x0 plus span of basis (Gray-code walk), returns dimension
static int gs_space(const gs_t*g,u32*x0,u32*basis){
  u32 piv=0; for(int i=0;i<g->r;i++) piv|=1u<<(31-__builtin_clz(g->row[i]));
  u32 x=0; for(int i=0;i<g->r;i++) if(g->rhs[i]) x|=1u<<(31-__builtin_clz(g->row[i]));
  *x0=x; int k=0;
  for(int f=0;f<32;f++) if(!(piv>>f&1)){
    u32 v=1u<<f; for(int i=0;i<g->r;i++) if(g->row[i]>>f&1) v|=1u<<(31-__builtin_clz(g->row[i]));
    basis[k++]=v;
  }
  return k;
}
// ---------- generic solve: x with fixed bits, eqx over x-features (target set), eqy over features of y = x + kappa,
// eqy target depends on the eqx target index; fixed bits on y.  cb(x) for every solution; returns count.
typedef void (*cb_t)(u32 x,void*ctx);
// walkmax: with stop_first, a space larger than walkmax is probed at walkmax random points (seeded) instead of walked
static u64 g_walkmax=~0ull; static __thread u64 g_seed=1;
static long solve(u32 fxm,u32 fxv,const eq_t*ex,const u32*tx,int ntx,
                  u32 kappa,u32 fym,u32 fyv,const eq_t*ey,const u32*ty,int stop_first,cb_t cb,void*ctx){
  long cnt=0; int nx=ex->n, ny=ey->n;
  for(u32 ax=0;ax<(1u<<nx);ax++){
    u32 s=ex->cst; for(int i=0;i<nx;i++) s+=(ax>>i&1)?ex->v1[i]:ex->v0[i];
    int ti=-1; for(int t=0;t<ntx;t++) if(s==tx[t]) ti=t;
    if(ti<0) continue;
    gs_t g; g.r=0; int ok=1;
    for(int b=0;b<32&&ok;b++) if(fxm>>b&1) ok=gs_add(&g,1u<<b,fxv>>b&1);
    for(int i=0;i<nx&&ok;i++) ok=gs_add(&g,ex->mask[i],ax>>i&1);
    if(!ok) continue;
    // allowed y-feature vectors for this target
    static __thread unsigned char yok[1<<12]; int anyy=0;
    for(u32 ay=0;ay<(1u<<ny);ay++){u32 t=ey->cst; for(int i=0;i<ny;i++) t+=(ay>>i&1)?ey->v1[i]:ey->v0[i]; yok[ay]=(t==ty[ti]); anyy|=yok[ay];}
    if(!anyy) continue;
    u32 x0,B[32]; int k=gs_space(&g,&x0,B);
    u32 x=x0; int rnd = stop_first && (1ull<<k) > g_walkmax;
    u64 iters = rnd ? g_walkmax : (1ull<<k);
    for(u64 it=0;it<iters;it++){
      if(rnd){ u64 r=sm(&g_seed); x=x0; for(int b=0;b<k;b++) if(r>>b&1) x^=B[b]; }
      else if(it) x^=B[__builtin_ctzll(it)];
      u32 y=x+kappa; if((y&fym)!=fyv) continue;
      u32 ay=0; for(int i=0;i<ny;i++) ay|=(u32)par(y&ey->mask[i])<<i;
      if(yok[ay]){cnt++; if(cb) cb(x,ctx); if(stop_first) return cnt;}
    }
  }
  return cnt;
}
// walk every x meeting the fixed bits and eqx (any target), handing (x, target index) to a direct check
typedef int (*wcb_t)(u32 x,int ti,void*ctx);
static long walk(u32 fxm,u32 fxv,const eq_t*ex,const u32*tx,int ntx,wcb_t cb,void*ctx){
  long cnt=0; int nx=ex->n;
  for(u32 ax=0;ax<(1u<<nx);ax++){
    u32 s=ex->cst; for(int i=0;i<nx;i++) s+=(ax>>i&1)?ex->v1[i]:ex->v0[i];
    int ti=-1; for(int t=0;t<ntx;t++) if(s==tx[t]) ti=t;
    if(ti<0) continue;
    gs_t g; g.r=0; int ok=1;
    for(int b=0;b<32&&ok;b++) if(fxm>>b&1) ok=gs_add(&g,1u<<b,fxv>>b&1);
    for(int i=0;i<nx&&ok;i++) ok=gs_add(&g,ex->mask[i],ax>>i&1);
    if(!ok) continue;
    u32 x0,B[32]; int k=gs_space(&g,&x0,B); u32 x=x0;
    for(u64 it=0;it<(1ull<<k);it++){ if(it) x^=B[__builtin_ctzll(it)]; cnt+=cb(x,ti,ctx); }
  }
  return cnt;
}
static const int R_S1[3]={6,11,25}, R_S0[3]={2,13,22};
// ---------- step 16: valid upper pairs for one A14 (base variable x = E15, minimal carry: E15 XOR = bit 9)
typedef struct { u32 A14,h0; u32 *z; int *cl; int n,cap; } pctx_t;
static int pcb(u32 x,int ti,void*c){ (void)ti; pctx_t*p=c; up_t u; upset(&u,p->A14,x-p->h0); int cl=piok(&u);
  if(cl && p->n<p->cap){p->z[p->n]=x-p->h0; p->cl[p->n]=cl; p->n++;} return cl!=0; }
static int pairs_for(u32 A14,pctx_t*P){
  u32 E14[2]; for(int k=0;k<2;k++) E14[k]=A14+A10[k]-S0(A13[k])-mj(A13[k],A12[k],A11[k]);
  u32 fxm=1u<<9, fxv=0;                // dE15 = +2^9 with XOR exactly bit 9
  eq_t ex; eq_init(&ex); ex.cst=(A12[1]-A12[0])+(E12[1]-E12[0]);
  eq_sigma(&ex,0x200u,R_S1,3,0,fxm,fxv);
  eq_bitwise(&ex,1,0x200u,E14[0],E13[0],E14[1],E13[1],fxm,fxv);
  u32 tx[8]; for(int m=0;m<8;m++) tx[m]=((m&1)?0x200000u:-0x200000u)-0x200u+((m&2)?0x20u:-0x20u)+((m&4)?4u:-4u);
  P->A14=A14; P->h0=A11[0]-S0(A14)-mj(A14,A13[0],A12[0]); P->n=0;
  return (int)walk(fxm,fxv,&ex,tx,8,pcb,P);
}
// ---------- step 17: K(pi) under the bit-27 rule, minimal carries in E16 (digits) and A16 (bit 2)
typedef struct { u32 keys[1<<16]; int n; u32 P16; } kctx_t;
static void kcb(u32 x,void*c){kctx_t*k=c; if(k->n<(1<<16)) k->keys[k->n++]=x-k->P16;}
static int kpi(const up_t*u,int cls16,kctx_t*K){
  // dE16 digits for class cls16 (1..8): m = cls16-1
  int m=cls16-1; u32 D=0x00200224u, fxm=D|(1u<<27), fxv=0;
  if(!(m&1)) fxv|=1u<<21;            // -2^21: bit set in E16
  fxv|=1u<<9;                         // -2^9
  if(!(m&2)) fxv|=1u<<5;
  if(!(m&4)) fxv|=1u<<2;
  fxv|=u->E15[0]&(1u<<27);            // bit-27 rule: E16[27] = E15[27]
  eq_t ex; eq_init(&ex); ex.cst=(A13[1]-A13[0])+(E13[1]-E13[0]);
  eq_sigma(&ex,D,R_S1,3,0,fxm,fxv);
  eq_bitwise(&ex,1,D,u->E15[0],u->E14[0],u->E15[1],u->E14[1],fxm,fxv);
  u32 tx[4],ty[4]; for(int q=0;q<4;q++){tx[q]=((q&1)?0x8000000u:-0x8000000u)+((q&2)?0x800000u:-0x800000u)-0x200u; ty[q]=(A13[1]-A13[0])-tx[q];}
  eq_t ey; eq_init(&ey); u32 fym=4u, fyv=0;   // A16 bit 2 = 0, so A16' = A16 ^ 4
  eq_sigma(&ey,4u,R_S0,3,0,fym,fyv);
  eq_bitwise(&ey,0,4u,u->A15[0],u->A14,u->A15[1],u->A14,fym,fyv);
  u32 kappa=-A12[0]+S0(u->A15[0])+mj(u->A15[0],u->A14,A13[0]);
  K->P16=A12[0]+E12[0]+S1(u->E15[0])+ch(u->E15[0],u->E14[0],E13[0])+K16+s1(u->W14);
  K->n=0;
  return (int)solve(fxm,fxv,&ex,tx,4,kappa,fym,fyv,&ey,ty,0,kcb,K);
}
// ---------- step 18 for an entry: number of E17 values (minimal E17 carries) passing; stop_first = liveness only
static long q18(const up_t*u,u32 c,int stop_first){
  st_t s; step16(u,c,&s); step17(u,&s,0);
  int c17=inset17(s.E17[1]-s.E17[0]); if(!c17||s.A17[0]!=s.A17[1]) return -1;
  int m=c17-1; u32 D=0x08800200u, fxm=D, fxv=1u<<9;   // digits 27, 23 (signs by class), -2^9
  if(!(m&1)) fxv|=1u<<27;
  if(!(m&2)) fxv|=1u<<23;
  eq_t ex; eq_init(&ex); ex.cst=u->E14[1]-u->E14[0];
  eq_sigma(&ex,D,R_S1,3,0,fxm,fxv);
  eq_bitwise(&ex,1,D,s.E16[0],u->E15[0],s.E16[1],u->E15[1],fxm,fxv);
  u32 tx[1]={0}, ty[1]={0};
  eq_t ey; eq_init(&ey);
  // A17 has no difference: Maj(A17, A16, A15) difference only through A16 and A15
  for(int i=0;i<32;i++){
    u32 a0=s.A16[0]>>i&1,a1=s.A16[1]>>i&1,b0=u->A15[0]>>i&1,b1=u->A15[1]>>i&1; u32 val[2];
    for(u32 v=0;v<2;v++) val[v]=((((v&a1)|(v&b1)|(a1&b1))-((v&a0)|(v&b0)|(a0&b0))))<<i;
    eq_add(&ey,1u<<i,val[0],val[1],0,0);
  }
  // x = E17 (with W17 = 0 the stored E17 is the offset), y = A17 = x + (A17 - E17)
  u32 kappa=s.A17[0]-s.E17[0];
  return solve(fxm,fxv,&ex,tx,1,kappa,0,0,&ey,ty,stop_first,0,0);
}
// ---------- step-18 passing E17 values (reservoir) for the step-19 estimate
typedef struct { u32 res[32]; int n; u64 seen; u64 rs; } rctx_t;
static void rcb(u32 x,void*c){ rctx_t*r=c; r->seen++; if(r->n<32) r->res[r->n++]=x; else { u64 j=sm(&r->rs)%r->seen; if(j<32) r->res[j]=x; } }
static long q18_res(const up_t*u,u32 c,rctx_t*R,st_t*S0){
  st_t s; step16(u,c,&s); step17(u,&s,0); *S0=s;
  int c17=inset17(s.E17[1]-s.E17[0]); if(!c17||s.A17[0]!=s.A17[1]) return -1;
  int m=c17-1; u32 D=0x08800200u, fxm=D, fxv=1u<<9; if(!(m&1)) fxv|=1u<<27; if(!(m&2)) fxv|=1u<<23;
  eq_t ex; eq_init(&ex); ex.cst=u->E14[1]-u->E14[0];
  eq_sigma(&ex,D,R_S1,3,0,fxm,fxv); eq_bitwise(&ex,1,D,s.E16[0],u->E15[0],s.E16[1],u->E15[1],fxm,fxv);
  u32 tx[1]={0}, ty[1]={0}; eq_t ey; eq_init(&ey);
  for(int i=0;i<32;i++){ u32 a0=s.A16[0]>>i&1,a1=s.A16[1]>>i&1,b0=u->A15[0]>>i&1,b1=u->A15[1]>>i&1; u32 val[2];
    for(u32 v=0;v<2;v++) val[v]=((((v&a1)|(v&b1)|(a1&b1))-((v&a0)|(v&b0)|(a0&b0))))<<i; eq_add(&ey,1u<<i,val[0],val[1],0,0); }
  return solve(fxm,fxv,&ex,tx,1,s.A17[0]-s.E17[0],0,0,&ey,ty,0,rcb,R);
}
static inline u64 mix3(u32 a,u32 b,u32 c){ u64 s=((u64)a<<32|b)^((u64)c*0x9e3779b97f4a7c15ull); return sm(&s); }
#ifndef KSOLVE_NO_MAIN
int main(int argc,char**argv){
  if(argc>=4 && !strcmp(argv[1],"rates")){
    // ./ksolve rates out.txt table/chunk*.bin : per-entry exact step-18 count and step-19 Monte Carlo on the same fixed
    // 1/4096 sample of live entries as `table` (same hash, same reservoir and W18 seeds), for standard errors and pass weighting
    FILE*o=fopen(argv[2],"w"); fprintf(o,"# A14 A15 cls16 key n18 s19trials s19passes\n"); long tot=0;
    for(int a=3;a<argc;a++){
      FILE*f=fopen(argv[a],"rb"); if(!f) return 2; fseek(f,0,SEEK_END); long sz=ftell(f); rewind(f);
      u32*d=malloc(sz); if(fread(d,1,sz,f)!=(size_t)sz) return 2; fclose(f); long nw=sz/4, nrec=0;
      for(long p=0;p<nw;p+=4+d[p+3]) nrec++;
      long*off=malloc(nrec*sizeof(long)); nrec=0; for(long p=0;p<nw;p+=4+d[p+3]) off[nrec++]=p;
      #pragma omp parallel for schedule(dynamic,16) reduction(+:tot)
      for(long r=0;r<nrec;r++){
        u32*rec=d+off[r]; up_t u; upset(&u,rec[0],rec[1]);
        for(u32 t=0;t<rec[3];t++){ u32 kk=rec[4+t]; u64 h=mix3(rec[0],rec[1],kk); if((h>>40)&4095) continue;
          rctx_t R; R.n=0; R.seen=0; R.rs=h^0x1919; st_t s0; long c=q18_res(&u,kk,&R,&s0);
          u64 rs=h^0x2020; long t19=0,p19=0;
          for(int q=0;q<R.n;q++){ st_t s=s0; u32 W17=R.res[q]-s0.E17[0]; step17(&u,&s,W17);
            for(int w=0;w<32;w++){ u32 E18[2],A18[2]; if(!step18(&u,&s,(u32)sm(&rs),E18,A18)) continue; t19++; p19+=step19(&u,&s,E18,A18); } }
          #pragma omp critical
          fprintf(o,"%08x %08x %u %08x %ld %ld %ld\n",rec[0],rec[1],rec[2],kk,c,t19,p19);
          tot++; }
      }
      free(off); free(d);
    }
    fclose(o); printf("%ld sampled entries\n",tot); return 0;
  }
  if(argc>=6 && !strcmp(argv[1],"table")){
    // ./ksolve table a14.bin lo hi out : valid pairs, K(pi) (bit-27, minimal carries), liveness (probe cap 1024),
    // records "u32 A14, u32 A15, u32 cls16, u32 nlive, u32 key[nlive]" for pairs with live keys; stats to out.stats
    FILE*f=fopen(argv[2],"rb"); fseek(f,0,SEEK_END); long na=ftell(f)/4; rewind(f); u32*a=malloc(na*4); if(fread(a,4,na,f)!=(size_t)na) return 2; fclose(f);
    long lo=atol(argv[3]), hi=atol(argv[4]); if(hi>na) hi=na;
    char fn[512]; snprintf(fn,sizeof fn,"%s.bin",argv[5]); FILE*o=fopen(fn,"wb");
    static u64 *bm=0; bm=calloc(1ull<<26,8);
    g_walkmax=1024;
    long npairs=0,npne=0,nent=0,nlive=0,nsamp=0,s19t=0,s19p=0; double sq18=0;
    long hist[16]={0};
    #pragma omp parallel reduction(+:npairs,npne,nent,nlive,nsamp,s19t,s19p,sq18)
    {
      pctx_t P; P.z=malloc(4<<16); P.cl=malloc(4<<16); P.cap=1<<16;
      kctx_t*K=malloc(sizeof(kctx_t)); u32*buf=malloc(4u<<20); size_t nb=0; u32*live=malloc(4<<16);
      #pragma omp for schedule(dynamic,8)
      for(long i=lo;i<hi;i++){
        pairs_for(a[i],&P); npairs+=P.n;
        for(int j=0;j<P.n;j++){
          up_t u; upset(&u,a[i],P.z[j]); kpi(&u,P.cl[j],K); nent+=K->n; int nl=0;
          for(int t=0;t<K->n;t++){
            u64 h=mix3(a[i],P.z[j],K->keys[t]); g_seed=h;
            if(q18(&u,K->keys[t],1)>0){ live[nl++]=K->keys[t];
              u32 kk=K->keys[t]; __atomic_fetch_or(&bm[kk>>6],1ull<<(kk&63),__ATOMIC_RELAXED);
              if(((h>>40)&4095)==0){   // fixed 1/4096 sample of live entries: exact step-18 count, step-19 Monte Carlo
                rctx_t R; R.n=0; R.seen=0; R.rs=h^0x1919; st_t s0; long c=q18_res(&u,kk,&R,&s0); nsamp++; sq18+=c/4294967296.0;
                u64 rs=h^0x2020;
                for(int r=0;r<R.n;r++){ st_t s=s0; u32 W17=R.res[r]-s0.E17[0]; step17(&u,&s,W17);
                  for(int w=0;w<32;w++){ u32 E18[2],A18[2]; if(!step18(&u,&s,(u32)sm(&rs),E18,A18)) continue; s19t++; s19p+=step19(&u,&s,E18,A18); } }
              }
            }
          }
          if(nl){ npne++; nlive+=nl;
            int hb=0; while((1<<hb)<nl && hb<15) hb++;
            #pragma omp atomic
            hist[hb]++;
            if(nb+4+nl>(1u<<20)){
              #pragma omp critical
              fwrite(buf,4,nb,o);
              nb=0; }
            buf[nb++]=a[i]; buf[nb++]=P.z[j]; buf[nb++]=P.cl[j]; buf[nb++]=nl; memcpy(buf+nb,live,4*nl); nb+=nl;
          }
        }
      }
      #pragma omp critical
      fwrite(buf,4,nb,o);
      free(buf); free(live); free(K); free(P.z); free(P.cl);
    }
    fclose(o);
    long distinct=0; for(long w=0;w<(1L<<26);w++) distinct+=__builtin_popcountll(bm[w]);
    struct rusage ru; getrusage(RUSAGE_SELF,&ru);
    snprintf(fn,sizeof fn,"%s.stats",argv[5]); FILE*st=fopen(fn,"w");
    fprintf(st,"A14 range %ld..%ld of %ld\nvalid upper pairs %ld\npairs with live keys %ld\nentries (bit-27 rule, minimal carries) %ld\nlive entries %ld\ndistinct live keys %ld\n"
               "sampled live entries %ld, mean exact step-18 rate %.6g\nstep-19 trials %ld passes %ld rate %.6g\ncpu user %.1f s sys %.1f s, peak RSS %ld KB\nlive keys per pair, log2 bins:",
      lo,hi,na,npairs,npne,nent,nlive,distinct,nsamp,nsamp?sq18/nsamp:0,s19t,s19p,s19t?(double)s19p/s19t:0,
      ru.ru_utime.tv_sec+ru.ru_utime.tv_usec/1e6,ru.ru_stime.tv_sec+ru.ru_stime.tv_usec/1e6,ru.ru_maxrss);
    for(int b=0;b<16;b++) fprintf(st," %ld",hist[b]); fprintf(st,"\n"); fclose(st);
    snprintf(fn,sizeof fn,"cat %s.stats",argv[5]); if(system(fn)) return 3;
    return 0;
  }
  if(argc>=3 && !strcmp(argv[1],"pcheck")){   // valid pairs by the solver vs brute-force pi40.txt (A14 list order)
    FILE*f=fopen(argv[2],"r"); u32 a,b; int c; static u32 A[100000],Bz[100000]; static int C[100000]; int n=0;
    while(n<100000 && fscanf(f,"%x %x %d",&A[n],&Bz[n],&C[n])==3) n++; fclose(f);
    u32 seen[64]; int ns=0; for(int i=0;i<n;i++){int k=0; for(int j=0;j<ns;j++) if(seen[j]==A[i]) k=1; if(!k) seen[ns++]=A[i];}
    static u32 z[1<<16]; static int cl[1<<16]; pctx_t P={0,0,z,cl,0,1<<16}; int bad=0;
    for(int s=0;s<ns;s++){
      struct timespec t0,t1; clock_gettime(CLOCK_MONOTONIC,&t0); int m=pairs_for(seen[s],&P); clock_gettime(CLOCK_MONOTONIC,&t1);
      int nb=0,hit=0; for(int i=0;i<n;i++) if(A[i]==seen[s]){ nb++; for(int j=0;j<P.n;j++) if(z[j]==Bz[i]&&cl[j]==C[i]) {hit++;break;} }
      if(m!=nb||hit!=nb) bad++;
      printf("A14 %08x: solver %d, brute force %d, matched %d (%.2f ms)\n",seen[s],m,nb,hit,(t1.tv_sec-t0.tv_sec)*1e3+(t1.tv_nsec-t0.tv_nsec)/1e6);
    }
    (void)a;(void)b;(void)c; printf("A14 values with a mismatch: %d\n",bad); return 0;
  }
  if(argc>=3 && !strcmp(argv[1],"live")){   // liveness only (stop at the first E17), timing
    FILE*g=fopen(argv[2],"r"); char line[512]; static u32 eA[1<<16],eB[1<<16],eK[1<<16]; static long eN[1<<16]; int ne=0;
    while(fgets(line,sizeof line,g)){ if(line[0]=='#') continue; unsigned P,A,B,C,Kk,C17; long na,nb,S;
      if(sscanf(line,"%u %x %x %u %x %u %ld %ld %ld",&P,&A,&B,&C,&Kk,&C17,&na,&nb,&S)!=9) continue;
      eA[ne]=A;eB[ne]=B;eK[ne]=Kk;eN[ne]=na+nb;ne++; }
    static char ex_live[1<<16];
    #pragma omp parallel for schedule(dynamic,8)
    for(int i=0;i<ne;i++){ up_t u; upset(&u,eA[i],eB[i]); ex_live[i]=q18(&u,eK[i],1)>0; }   // exact (full walk)
    long caps[4]={64,256,1024,4096};
    for(int c=0;c<4;c++){ g_walkmax=caps[c];
      struct timespec t0,t1; clock_gettime(CLOCK_MONOTONIC,&t0); int live=0,miss=0,dis=0;
      for(int i=0;i<ne;i++){ g_seed=0x2913ull^eK[i]; up_t u; upset(&u,eA[i],eB[i]); int q=q18(&u,eK[i],1)>0; live+=q; miss+=(ex_live[i]&&!q); dis+=(q!=(eN[i]>0)); }
      clock_gettime(CLOCK_MONOTONIC,&t1); double ms=(t1.tv_sec-t0.tv_sec)*1e3+(t1.tv_nsec-t0.tv_nsec)/1e6;
      printf("probe cap %5ld: %d entries, live %d, exact-live missed %d, disagreements with MC %d, %.2f us per entry (one thread)\n",
        caps[c],ne,live,miss,dis,1e3*ms/ne); }
    return 0;
  }
  if(argc>=4 && !strcmp(argv[1],"kcheck")){
    FILE*f=fopen(argv[2],"r"); u32 a14,a15; int cl; int p=0, bad=0;
    // brute-force entries: lines "p A14 A15 cls16 key cls17 ..."
    static u32 bk[1<<20][3]; int nb=0; FILE*g=fopen(argv[3],"r"); char line[512];
    while(fgets(line,sizeof line,g)){ if(line[0]=='#') continue; unsigned P,A,B,C,Kk; if(sscanf(line,"%u %x %x %u %x",&P,&A,&B,&C,&Kk)==5){bk[nb][0]=A;bk[nb][1]=B;bk[nb][2]=Kk;nb++;} }
    fclose(g);
    static kctx_t K;
    while(fscanf(f,"%x %x %d",&a14,&a15,&cl)==3){
      up_t u; upset(&u,a14,a15);
      struct timespec t0,t1; clock_gettime(CLOCK_MONOTONIC,&t0);
      int n=kpi(&u,cl,&K);
      clock_gettime(CLOCK_MONOTONIC,&t1);
      int nbf=0, found=0, a16min=0;
      for(int i=0;i<nb;i++) if(bk[i][0]==a14&&bk[i][1]==a15){ nbf++;
        st_t s; step16(&u,bk[i][2],&s); int min=((s.A16[0]^s.A16[1])==4u); a16min+=min;
        int hit=0; for(int j=0;j<K.n;j++) if(K.keys[j]==bk[i][2]) hit=1;
        found+=hit; if(min&&!hit) bad++; }
      int extra=0; for(int j=0;j<K.n;j++){ st_t s; step16(&u,K.keys[j],&s); step17(&u,&s,0);
        if(!inset17(s.E17[1]-s.E17[0])||s.A17[0]!=s.A17[1]||(((s.E16[0]>>27)&1)!=((u.E15[0]>>27)&1))) extra++; }
      if(nbf||n) printf("pi %d %08x %08x: solver %d keys (%.2f ms), brute force %d (A16-minimal %d), found %d, invalid %d\n",
        p,a14,a15,n,(t1.tv_sec-t0.tv_sec)*1e3+(t1.tv_nsec-t0.tv_nsec)/1e6,nbf,a16min,found,extra);
      p++;
    }
    printf("pairs %d, minimal brute-force entries missed by the solver: %d\n",p,bad); return 0;
  }
  if(argc>=3 && !strcmp(argv[1],"qcheck")){
    FILE*g=fopen(argv[2],"r"); char line[512]; int maxn=argc>=4?atoi(argv[3]):1000000;
    static u32 eA[1<<16],eB[1<<16],eK[1<<16]; static long eS[1<<16],eN[1<<16]; int ne=0;
    while(ne<maxn && fgets(line,sizeof line,g)){ if(line[0]=='#') continue; unsigned P,A,B,C,Kk,C17; long na,nb,S;
      if(sscanf(line,"%u %x %x %u %x %u %ld %ld %ld",&P,&A,&B,&C,&Kk,&C17,&na,&nb,&S)!=9) continue;
      eA[ne]=A;eB[ne]=B;eK[ne]=Kk;eS[ne]=2*S;eN[ne]=na+nb;ne++; }
    double se=0,sm=0; int live_mc=0, live_ex=0, mc_not_ex=0, ex_not_mc=0; double z2=0;
    #pragma omp parallel for schedule(dynamic,4) reduction(+:se,sm,live_mc,live_ex,mc_not_ex,ex_not_mc,z2)
    for(int i=0;i<ne;i++){
      up_t u; upset(&u,eA[i],eB[i]); long q=q18(&u,eK[i],0); double qe=q/4294967296.0, qm=(double)eN[i]/eS[i];
      se+=qe; sm+=qm; live_mc+=eN[i]>0; live_ex+=q>0; mc_not_ex+=(eN[i]>0&&q<=0); ex_not_mc+=(eN[i]==0&&q>0);
      if(qe>0) z2+=(qm-qe)*(qm-qe)/(qe/eS[i]);   // chi-square-like: MC counts vs exact rate
    }
    printf("%d entries: mean exact (minimal E17 carries) %.5g, mean MC %.5g, ratio %.4f\n",ne,se/ne,sm/ne,sm/se);
    printf("live exact %d, live MC %d; MC-live but exact 0: %d; exact-live but MC 0: %d; mean squared z %.3f\n",
      live_ex,live_mc,mc_not_ex,ex_not_mc,z2/live_ex);
    return 0;
  }
  return 1;
}
#endif
```

### A.4 `merge.c`

```c
// Merge the table chunks written by `ksolve table`: totals, distinct keys (mod 2^32 and mod 2^30),
// largest key multiplicity class, and record integrity.  ./merge table/chunk*.bin
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef uint32_t u32; typedef uint64_t u64;
int main(int argc,char**argv){
  u64 *b32=calloc(1ull<<26,8), *b30=calloc(1ull<<24,8);
  u64 pairs=0, entries=0, bad=0; u32 hdr[4];
  for(int a=1;a<argc;a++){
    FILE*f=fopen(argv[a],"rb"); if(!f){fprintf(stderr,"missing %s\n",argv[a]); return 1;}
    static u32 keys[1<<16];
    while(fread(hdr,4,4,f)==4){
      u32 n=hdr[3]; if(n==0||n>(1u<<16)||hdr[2]<1||hdr[2]>8){bad++; break;}
      if(fread(keys,4,n,f)!=n){bad++; break;}
      pairs++; entries+=n;
      for(u32 i=0;i<n;i++){ u32 k=keys[i]; b32[k>>6]|=1ull<<(k&63); u32 r=k&0x3fffffffu; b30[r>>6]|=1ull<<(r&63); }
    }
    fclose(f);
  }
  u64 d32=0,d30=0; for(u64 w=0;w<(1ull<<26);w++) d32+=__builtin_popcountll(b32[w]); for(u64 w=0;w<(1ull<<24);w++) d30+=__builtin_popcountll(b30[w]);
  printf("pairs with live keys %llu\nlive entries N %llu = 2^%.4f\ndistinct keys %llu\ndistinct keys mod 2^30 %llu\nmatches per lower solution N/2^32 %.6f\nbad records %llu\n",
    (unsigned long long)pairs,(unsigned long long)entries,__builtin_log2((double)entries),(unsigned long long)d32,(unsigned long long)d30,entries/4294967296.0,(unsigned long long)bad);
  return 0;
}
```

### A.5 `layout.c`

```c
// Size of a compact static layout for the live table written by `ksolve table`.
//   ./layout table/chunk*.bin
// Item = (reduced key c mod 2^30, upper pair) with a 4-bit mask of the top two key bits present (the reduction of
// [G, Section 6.2], which neither loses nor adds entries). Reports the item count, the mask histogram, the largest
// pair id, and the bytes of a sorted layout: 2^b bucket offsets (4 bytes each) indexed by the top b bits of the
// reduced key, and per item the remaining 30-b key bits, the pair id and the mask, packed to whole bytes.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
typedef uint32_t u32; typedef uint64_t u64;
static int cmpu(const void*a,const void*b){u32 x=*(const u32*)a,y=*(const u32*)b; return x<y?-1:x>y;}
int main(int argc,char**argv){
  u64 recs=0, ent=0, items=0, mh[16]={0}, maxn=0; u32 hdr[4]; static u32 keys[1<<16], low[1<<16];
  u64 *seen=calloc(1ull<<24,8); u64 dred=0;
  for(int a=1;a<argc;a++){
    FILE*f=fopen(argv[a],"rb"); if(!f){fprintf(stderr,"missing %s\n",argv[a]); return 1;}
    while(fread(hdr,4,4,f)==4){
      u32 n=hdr[3]; if(n==0||n>(1u<<16)){fprintf(stderr,"bad record\n"); return 1;}
      if(fread(keys,4,n,f)!=n){fprintf(stderr,"short record\n"); return 1;}
      recs++; ent+=n; if(n>maxn) maxn=n;
      for(u32 i=0;i<n;i++) low[i]=(keys[i]&0x3fffffffu)<<2|keys[i]>>30;
      qsort(low,n,4,cmpu);
      for(u32 i=0;i<n;){ u32 r=low[i]>>2, m=0; while(i<n && (low[i]>>2)==r){ m|=1u<<(low[i]&3); i++; }
        items++; mh[m]++; if(!(seen[r>>6]>>(r&63)&1)){ seen[r>>6]|=1ull<<(r&63); dred++; } }
    }
    fclose(f);
  }
  int pid_bits=0; while((1ull<<pid_bits)<recs) pid_bits++;
  printf("records (upper pairs) %llu, pair-id bits %d\nentries %llu\nitems (reduced key, pair) %llu = entries/%.4f\ndistinct reduced keys %llu\nlargest record %llu keys\n",
    (unsigned long long)recs,pid_bits,(unsigned long long)ent,(unsigned long long)items,(double)ent/items,(unsigned long long)dred,(unsigned long long)maxn);
  printf("mask histogram (bit j = top bits j present):");
  for(int m=1;m<16;m++) printf(" %x:%llu",m,(unsigned long long)mh[m]); printf("\n");
  for(int b=24;b<=30;b++){
    int ib=(30-b)+pid_bits+4; int bytes=(ib+7)/8;
    double tot=(double)(1ull<<b)*4+(double)items*bytes+(double)recs*8;
    printf("b=%d: offsets %.0f B, item %d bits -> %d B, items %.0f B, pair records %.0f B, total %.0f B = 2^%.4f\n",
      b,(double)(1ull<<b)*4,ib,bytes,(double)items*bytes,(double)recs*8,tot,log2(tot));
  }
  return 0;
}
```
