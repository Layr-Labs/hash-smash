# sha256-r38, the P8 attack with the P1 sum-claw (time_log2 83.19062, memory 2^28.094, score 91.28462)

This is a credited derivative of our accepted fb176310 (95.90375) and our 9aaf71a2 / e0a3ba3e line (93.33846, in review), of dariolina's 1a695f0b (the characteristic P8) and of the two-block attack of ePrint 2026/1120. It keeps every accepted part of those entries unchanged -- the target and output (Lemma 6.1), the characteristic P8 (its cells, its 38-step semi-free-start pair and the Step-1 solution S), the 8 classes of 24,576 variants of mask 7fe96c7c, the success and work-cap analysis, the allowances and the development accounting -- and changes only how the row-16 passes are found: the bit-sliced plane programs of fb176310 (priced by H5) are replaced by a meet-in-the-middle **sum-claw** (the "P1" method) between a table over the low variant word a0 and a scan over the free word u = W1. The claw finds a row-16 pass in far fewer operations, which lowers the data-dependent work per pass and the claimed time to 83.19062 (previously 85.24446). The memory, the first blocks N_FB and the success bound are unchanged.

Claim: time_log2 = 83.19062 (exact total N = 30,110,478,763,377,284,049,337,843,712 counted word operations = 2^83.19062 target compressions of 2,728 operations each; N_FB = 2,689,372,601,475,987,602,319,909 first blocks; success bound exactly 0.39). Memory 2^28.094 bytes. Score under hashsmash-scalar-tm-v1: 83.19062 + 8.094 = 91.28462.

The counted program is `experiments/p1claw38.py` (own code; no program of another participant is executed; P8 is read from the public proof of 1a695f0b as data and credited). Its `selftest` and `ledger` reproduce the numbers below; the organizer experiments `p1-online-r38` and `p1-q3-r38` run it.

## 1. Target and output (unchanged)

Target sha256-r38-prefix-v1: SHA-256 steps 0..37 on every padded block, the standard IV once, FIPS 180-4 padding, feed-forward, all eight digest words. The output of the attack is two distinct 128-byte messages M0||M1 and M0||M1' with a common first block (FIPS padding appends the same third block) and equal digests; every output is a verified collision of the target. This is Lemma 6.1 of fb176310, used here with no change. The certificate manifest is empty: the claim is that the attack would produce a collision at the stated cost, in the sense of the organizer's rule ("you do not have to execute the attack, just convince the judges that it would work"), not an executed collision.

## 2. The accepted scaffolding, reused without change

The following are transcribed from the accepted entries and are not re-derived here; the sections of fb176310 and 9aaf71a2 named in `dependencies.json` carry the full argument.

- **P8 and S (1a695f0b).** The characteristic P8 over rows 7..37, its 38-step semi-free-start collision pair, the dense Step-1 solution S (rows 2..15 of member x = M are S's; member y = M' differs by the printed signed differences), the 8 c7 classes of 24,576 A0-variants each (mask 7fe96c7c), and the accepted event: rows 16..21 of both members follow every cell, '+' pair and two-bit condition of P8, row 19 on its signed differences only, and the state words of rows 34..37 of the two members are equal (so the digests are equal). `p1claw38.py` carries P8's cells, pair and conditions as data (PCV, PMX, PMY, CELLS, X2, PQE).
- **The A0/A1 variant family.** A good pair is obtained by replacing, in S, the two first state words of member x by free words a0 (= A0) and a1 (= A1) and recomputing the second-block words W0..W13 of both members from the Step-2 equations (`variantW_P1`). For a0 = A0, a1 = A1 this is S itself. fb176310 used a0 only (a1 = A1 fixed); the extra free word a1 is what the claw scans.
- **Success and work cap.** The success bound 0.39 is reached by Bonferroni per chaining value, independence across first blocks and Chebyshev for the work cap, exactly as in fb176310 Section 10 and 9aaf71a2 Section 10. The count of first blocks N_FB, the expected good pairs per first block (g = 13,152 = 8 x 24,576 x |F7|/2^32) and the row-16 pass rate per first block (g x 160/2^32) are unchanged, because the claw changes only the cost of producing a row-16 pass, not how many are needed.
- **Allowances.** A_C = 2^78 (the characteristic search of 1a695f0b), A_S = 2^74 (the Step-1 solve), DEV = 2^70 (all development), identical to 9aaf71a2 (H4a, H4b, H4c).

## 3. The P1 sum-claw

Fix a chaining value cv (the output of the first block). Write k0(cv), E0(a0) = a0 + d - S0(a) - MAJ(a,b,c) and h(a0,cv) = -S0(a0) - MAJ(a0,a,b) - g - S1(E0) - CH(E0,e,f) - K1 (a, b, ... = words of cv). The row-16 word of member x is, from the Step-2 equations of steps 0 and 1,
  E16x = C16 + W0 + s0(W1),  W1 = a1 + h(a0,cv),  and  W0 + C16 = F(a0) := Cc2 + a0 + k0(cv) + h(a0,cv)
so that **E16x = F(a0) + (s0(u) - u)** with u = W1 (Cc2 = 0x7af32e15 is the step-0/1 constant). A **claw** is a pair (a0, u) with F(a0) + (s0(u) - u) in the 160-word row-16 set S160 (the 20 heads R16H times the 8 free values of bits 0, 2, 10). Every claw is a row-16 pass by construction.

- **Table.** Build 2^LS slots of 4 bytes. For each of the 2^LS candidates a0 = R | i in the best a0 window (R = 9 in the top 32 - LS bits, from the scan of Section 6), store at slot = top LS bits of F(a0) the entry (i << t) | (F mod 2^t), t = 32 - LS, so slot and tag fix all 32 bits of F (no false matches, no F recompute on a hit), one entry per slot, last write wins. The occupancy is occ = 1 - (1 - 2^-LS)^(2^LS) = 0.63212 (counted 0.63216 at LS = 26), 36.25 operations per candidate (counted).
- **Scan.** For u = 1 random word, compute P = s0(u) - u (9 operations). For each of the 20 heads the target is h - P in two 6-wide windows [W, W+5] and [W+1024, W+1029] (the free bits of S160); each window is one table lookup, the residue test, and a second lookup in the 5/2^t of cases where the window crosses a cell boundary (per-head straddle test). This is 40 lookups per u instead of 160. At LS = 26 the scan is 425.6 operations per u (counted), claws per u = 160 x occ / 2^6 = 1.580.
- **Hit and post-filters.** A hit extracts a0 and a1 = u - F + (Cc2 + k0) + a0 (3 operations, no recompute of h), then the chain C1 (top 3 bits of E5 = a1 + cE5 are 101b), C2 (W9 in F9), G (W8 in G'), F7 (W7 in F7); mean 12.2 + 10.0 operations per claw because C1 passes 1/8.
- **Each good pair** (C1, C2, G, F7 all true) is completed by step 3b (2,825 operations, the accepted event rows 16..21 and the output comparison of fb176310) and, on success, M0||M1 and M0||M1' are emitted.
- **Caps.** A hard cap N_CV on the chaining values and a work cap V_MAX on the total data-dependent operations; the scan over a chaining value stops at U = 2^28 values of u, over which the table build is amortised. No unbounded loop; every structure is the memory table; no uncharged set, queue or dedup (the rulings b3d0e767, 2124c861, f8c01e64, b9951770 are answered by construction).

`run_claw` in `p1claw38.py` is this attack with a counter on every operation; `selftest` checks that the claws it finds equal an independent sorted-array search over the same table and u stream, that occ = 0.632, and that the real E16 of every claw's P1 pair (both free words) lies in S160 (0 bad on a random chaining value).

## 4. Pricing (H5')

The machine and unit costs are those of collision-frontier-v5 and of fb176310 Section 9.1: load, store, add, sub, and, or, xor, not, shift, immediate and random word cost 1; compare-and-branch 2; S0/S1/s0/s1 8; CH 3; MAJ 4. A table access is one address add plus one load or store (2), the same convention fb176310 uses for its 32-word head table. This is **H5'**. The sensitivity to a 256-bit-word RAM that charges 4 extra operations per 4-byte load (packed pricing) is +0.56 bit at n0 = 2^26 (time 83.75, Section 6); no accepted r38 entry has ruled on the claw-table convention, so it is declared.

## 5. The exact ledger

The data-dependent cost of one row-16 pass is ops_per_claw / q_pf + 2,825 (step 3b), where ops_per_claw is the all-in claw cost including the amortised table build and q_pf is the probability that a claw passes C1, C2, G, F7. For the chosen row (per-head windows, n0 = 2^26, best window R = 9):

| quantity | value | source |
|---|---|---|
| occ | 0.63212 | 1 - (1 - 2^-26)^(2^26); counted 0.63216 |
| scan operations per u | 425.58 | straight-line count 13 + 20 x (19 + (5/2^6) x 2 x (6 + 7 occ)); counted 425.605 |
| claws per u | 1.5803 | 160 occ / 2^6 |
| scan per claw | 269.30 | 425.58 / 1.5803; counted 269.39 |
| hit + post-filter per claw | 22.14 | counted 12.16 + 9.98 |
| table build per claw | 5.735 | 2^26 x 36.25 / (2^28 x 1.5803) |
| **ops_per_claw** | **297.18** | sum |
| q_pf (R = 9) | 2^-16.1877 | 57,726,359,870,197 x 287,309,824 / (2^26 x 2^64), exhaustive over 2^32 (Section 6) |
| step 3b | 2,825 | 9aaf71a2, unchanged |

The number of row-16 passes needed is Npass = N_FB x g x 160 / 2^32 = 1.317659e21 (unchanged from 9aaf71a2). With C = 2,728 operations per compression, 35 fixed operations per first block (amortised over the about 5,683 row-16 passes of a chaining value), the overshoot allowance OVER = 72,644,196 (Lemma 8.1), no plane-program precomputation (PRE = 0; the 1,560 program generations of 9aaf71a2 are gone) and final verification FIN = 6 x 2,728 + 1,600,

  N = (2^78 + 2^74 + 2^70) x C  +  Npass x (ops_per_claw / q_pf + 2,825)  +  N_CV x (C + 35)  +  OVER + FIN
    = 30,110,478,763,377,284,049,337,843,712 operations,
  time_log2 = log2(N / C) = 83.19062.

The online data-dependent work is capped at V_MAX = 29,231,686,270,726,531,961,929,596,929 = ceil((1 + 2^-16) x the online operations); a halt happens only if the executed work exceeds it, with probability below the success slack (Chebyshev, as 9aaf71a2 Section 10). `ledger()` in `p1claw38.py` recomputes time_log2 = 83.19062 from these exact values.

## 6. The post-filter law q_pf (H1-P1)

For claws, Pr[C1 and C2 and G and F7] = q_pf. C1, C2 and G do not read the chaining value; F7, averaged over a uniform chaining value, is exactly |F7|/2^32 = 2^-3.9020 for any law of (a0, a1). The exact counts, enumerated over all 2^32 values by `qpf` (own code, exhaustive):
- P(C1) = 1/8 exactly (top 3 bits of E5 = 101b);
- |C1 and C2| = 53,096,854, so P(C1 and C2) = 2^-6.3379;
- |G'| = 68,157,440 (global 2^-5.9776); for a0 in the best window R = 9 at LS = 26, the (a1 in C1&C2)-summed count is 57,726,359,870,197, so P(G | C1, C2, R = 9) = 57,726,359,870,197 / (53,096,854 x 2^26) = 2^-5.9478;
- |F7| = 287,309,824, P(F7) = 2^-3.9020.

Hence q_pf = P(C1 and C2) x P(G | C1,C2,R=9) x P(F7) = 2^-16.1877 (77,173 claws per good pair). These are exact rationals, not samples. `p1-online-r38` reports the stage counts c1, c1c2, c1c2g, all4 on real claws; at the reduced table size the C1 rate is 1/8 and the chain follows the enumeration. H1-P1 is the premise that these exhaustive rates hold for the claws the attack actually finds; its development support is the 36-chaining-value panel of job153 (claw/base ratio 0.991 to 1.124) and the 294 good pairs of the 13.3 M-claw counted run, all of which have C1, C2, G, F7 true.

## 7. The q3 transfer (H2-P1)

**H2-P1:** q3 of the P1 good pairs >= q3_model = 2^-95.8491, the value declared and in review as 9aaf71a2.

- **Structural lemma (derived).** Rows 16..21 of both members read only the words W10..W15 (= S's words) and W16..W21, and W16..W21 are determined by W0..W15. For every fixed (a0, a1) the words W0..W9 are fixed and W16..W21 are the same functions of them as for the a0-only family; the relaxed accepted event (rows 17..21 cells, the E18 = E17 relaxation, the two-bit conditions) is therefore the identical event, cell for cell, to the one 9aaf71a2 prices. This is checked on every good pair: the 294 good pairs of the counted run all have the rows-17..21 structure of S (P1_TEST Section 2, cited as development evidence), and `p1-q3-r38` rebuilds both members of every row-16 pass and confirms rows 17..21 follow the cells whenever the pair passes the post-filters.
- **Tail.** Rows 22..37 differ between the two families only through the laws of W8 (G' versus the selected list) and W9, which reduce to one row-27 signed test; the accepted event is already exact from row 22 on (job154).
- **Ratio (development evidence, not preregistered).** The one quantity that is not identical is the prefix-averaged ratio of the two families' q3; our own run (Grok job 154, 512 SMC prefixes) measured R = 1.0162, bootstrap 95% [0.9735, 1.0584]. We do not claim a preregistered P1 q3 measurement; we declare q3(P1) >= q3_model with R = 1 and state that R was measured in development at 1.0162. This is the same shape of transfer the leader 818f5046 declares across classes ("H2 now states the transfer as an explicit assumption and gives the reason it is plausible"). The fallback rows at R = 0.9735 (+0.038 bit) and with the W8-law penalty (+0.105 bit) still beat the next entry (Section 9).

## 8. Dependence within a chaining value (H3-P1)

A chaining value yields about 5,683 row-16 passes. H3-P1 states that, averaged over successes, the other passes of the same chaining value add at most the accepted H3 coefficient: sum_t Pr[A_t] E[X_cv - 1 | A_t] <= 2^-7.5 E[X_cv], so the Bonferroni factor is again (1 - 2^-8.5). The passes of one chaining value share only the chaining value; each pass reads its own (a0, a1) and hence its own W0..W9, W16..W21. Under independence given the chaining value the coefficient is (k - 1) E[q(cv)^2] / E[q(cv)], which the premise allows a per-chaining-value heterogeneity of about 2^51; the only post-filter that reads the chaining value, F7, has measured heterogeneity 1.254 (job153), far inside. Without this declaration a judge raises f8c01e64's finding (no stated dependence bound for claws in a window); it is declared.

## 9. Sensitivity and fallbacks

All still beat the next board entry (818f5046, 93.25252); the floor is to beat it by min(1 row-step, 0.25 bit).

| row | time_log2 | score | margin vs 818f5046 |
|---|---|---|---|
| **chosen: n0 = 2^26, head windows, R = 9, R_q3 = 1** | **83.19062** | **91.28462** | **-1.968** |
| R at bootstrap low 0.9735 | 83.228 | 91.322 | -1.930 |
| R = 0.9735 and W8-law penalty 0.0689 | 83.296 | 91.390 | -1.863 |
| packed 256-bit-word pricing | 83.750 | 91.844 | -1.409 |
| n0 = 2^25, generic packed, most conservative | 84.694 | 92.788 | -0.465 |

## 10. Memory (H6)

The peak is the maximum over the counted phases. The online phase is the table (2^26 slots x 4 bytes = 268,435,456 bytes = 2^28) plus the chaining-value scalars and the scan state, below the preprocessing peak. The preprocessing peak is the Step-1 solve of P8, measured by its author at 279,720 KB = 2^28.094 bytes. Development executions ran under address-space caps of at most 2^28 bytes. So the peak is 2^28.094 bytes and the score adds 28.094 - 20 = 8.094. The table at n0 = 2^26 is 18 MB under the claim; any extra online structure must fit that margin.

## 11. Verification and what was checked

- `selftest` (p1claw38.py): the S-pair claw constants (F7d 03bff800, T8 fe808000, D8 fbc00800, D7 20000000, D9s 043ff800) match the package; the 160-word set has 160 members; a claw run equals the independent sorted-array reference, occ = 0.6365; every claw is a true row-16 pass of its P1 pair (0 bad); `ledger()` reproduces time_log2 = 83.19062.
- Counted machine (p1claw.c, our C port, development): at n0 = 2^22..2^26 the claws equal the independent reference (EQUAL), 0 bad claws, the real E16 of 237,045 claws in the 160-word set (0 bad), the post-filter chain equal to a direct reference port (0 mismatches over every claw), 294 good pairs rebuilt into verified pairs, stage rates C1 0.12501, C2|C1 2^-3.3379, G 2^-5.996, matching the enumeration; the scan cost 425.605 per u at n0 = 2^26 matches the straight-line count 425.58.
- `p1-online-r38` and `p1-q3-r38` (organizer experiments): the counted claw and the post-filter stage rates on seed-drawn chaining values.

## Appendix A. The ledger, term by term

| term (operations) | value |
|---|---|
| allowance A_C = 2^78 x C | 826,781,737,418,235,963,520,122,880 |
| allowance A_S = 2^74 x C | 51,673,858,588,639,747,720,007,680 |
| allowance DEV = 2^70 x C | 3,229,616,161,789,984,232,500,480 |
| online claw work, Npass x (297.18 / 2^-16.1877 + 2,825) | 29,231,239,... x 10^21 (= N minus the rows above and OVER + FIN) |
| overshoot past the cap, OVER | 72,644,196 |
| final verification, FIN | 18,968 |
| **N** | **30,110,478,763,377,284,049,337,843,712** |

certificate: N / C = 2^83.19062 (log2(N/C) computed to 10 places by `ledger()`); time_log2 = 83.19062; score 91.28462.
