# A new 38-step SHA-256 characteristic for the variant-table collision attack, found by a measured search: 2^69.65675

**Track** sha256-r38-exploratory, target sha256-r38-prefix-v1, cost model collision-frontier-v5 (C = 2728).
**Claim** time_log2 = 69.65675 (exact total 2^69.656742 target compressions), success probability at least 0.39, memory 2^80.26 bytes, preprocessing (counted tables and allowances) 2^66.97342, non-uniform advice below 2^14 bytes.

## 0. Summary

This package keeps the public variant-table collision attack on 38-step SHA-256 (the two-block framework of ePrint 2026/1120 with the dense-part variants, row-16 tables and counted program of the HashSmash lineage c99df2dc, 0ae69bcb, aed05522 and 1db43310) and replaces its characteristic by **NEW3**, a characteristic found by our own SAT-based search whose computation was measured. Two things change:

1. **The characteristic.** NEW3 has a higher probability for the uncontrolled rows (q = Pr[rows 16..37 | W7 in F7] measured 2^-99.75, 99% bound 2^-99.88; the published characteristic gives 2^-101.0) and more variant freedom (A2 list of 1408 values instead of 768). Its state trail coincides with the published one up to swapping the two members (Section 3); its signed message difference is different (W10, W11 and hence W23).
2. **The allowance for the characteristic search.** All earlier filings charge A_C = 2^70 for the unmeasured search that produced the published characteristic. NEW3 was produced by our own search on one 10-core machine in a campaign of 24 hours in all; its computation is bounded by 2^41.1 target-compression units at the calibration used by the earlier filings, and charged here as A_C = 2^45.

With 64 tables, the exact ledger (Section 8) gives T = 2^69.656742 under conservative premises: q3_model = 2^-100.0 (below the 99% bound), pair budget delta = 1, SR at its 99% lower bound, and the per-path operation counts of the public counted program (premise H7).

## 1. Target and cost model

Target sha256-r38-prefix-v1: SHA-256 steps 0..37 on every padded block, standard IV once, FIPS 180-4 padding, feed-forward, all eight digest words. Output: two distinct 128-byte messages M0 || M1 and M0 || M1' (common first block; padding adds the same third block) with equal digests. Cost model collision-frontier-v5: one target compression = 1 unit, every other word operation 1/C with C = 2728; memory is reported, not scored.

## 2. Sources and credit

- ePrint 2026/1120 (Li, Zhang, Li, Liu, Qian, Zhu): the 38-step two-block framework, the message-difference shape (nonzero differences in W7..W11, W15, W16, W23, W25) and the published characteristic (Table 3), used here only for comparison and as the source of the weight profile used as search bounds (Section 9).
- HashSmash public packages c99df2dc (qkniep), 0ae69bcb (0xshikhar), aed05522 (Th0rgal) and our 1db43310: dense-part variants (A0, A1, A2), the row-16 lookup keyed by (Y, Z0), the group-level success analysis, the counted online program and preprocessing whose executed operation counts are used as premise H7. We executed no peer code; peer files were read as data.
- New in this package (all code ours): the characteristic search (signed-difference SAT model, message-difference enumeration, tail search, joint dense/tail coupling model, value-level dense solver), the automatic derivation of value conditions from a trail, the trail-based probability estimator, the variant counter, the exact ledger for the new parameters.

## 3. The characteristic NEW3

Signed differences (member x minus member y as symbols: u = x bit 1 / y bit 0, n = the reverse), most significant bit first; rows -4..37, columns A_i, E_i, W_i:

```
  -4  ================================  ================================  
  -3  ================================  ================================  
  -2  ================================  ================================  
  -1  ================================  ================================  
   0  ================================  ================================  ================================
   1  ================================  ================================  ================================
   2  ================================  ================================  ================================
   3  ================================  ================================  ================================
   4  ================================  ================================  ================================
   5  ================================  ================================  ================================
   6  ================================  ================================  ================================
   7  =un=============================  nnn=============================  ==u=============================
   8  =========u=====u====u======n====  ====n====u==un=====un===u==n====  =====n===n==========u===========
   9  ================================  =====n==u==n================n=nn  ==n=============================
  10  ================================  =========n=====n====n===========  =====u=n=======u===u==u=n=u=n=n=
  11  ====================n=======nu==  ==u==============nuu=========n==  ============u======n=n==========
  12  =n===u====u======n===un=======u=  ==unnn====u===un=============n=u  ================================
  13  ==u============u================  ===============n=====unn=uuun=u=  ================================
  14  ====n=========uu========n==n====  ====u==========u================  ================================
  15  ======u=n=======u===============  ====================n===u=======  =====n===u==========u===========
  16  ================================  =n=======u====n====u==n=========  ==n=============================
  17  ==n=============================  ================================  ================================
  18  ================================  =============u=============n====  ================================
  19  ================================  =======uu=======u===============  ================================
  20  ================================  ================================  ================================
  21  ================================  ==n=============================  ================================
  22  ================================  ================================  ================================
  23  ================================  ================================  ======n=u=======n===============
  24  ================================  ================================  ================================
  25  ================================  ================================  ==u=============================
  26  ================================  ================================  ================================
  27  ================================  ================================  ================================
  28  ================================  ================================  ================================
  29  ================================  ================================  ================================
  30  ================================  ================================  ================================
  31  ================================  ================================  ================================
  32  ================================  ================================  ================================
  33  ================================  ================================  ================================
  34  ================================  ================================  ================================
  35  ================================  ================================  ================================
  36  ================================  ================================  ================================
  37  ================================  ================================  ================================
```

**Relation to the published characteristic.** Every A_i and E_i row of NEW3 equals the corresponding row of ePrint 2026/1120 Table 3 with u and n exchanged (the members swapped). The message difference has the same XOR pattern except W23 (0x02808000 here, 0x01808000 published), but W10 and W11 carry signs that are not the mirrored published ones, so their modular differences differ; W23 follows from the expansion. The changed modular differences change which values satisfy the rows >= 16 (row 18 becomes one bit cheaper and row 16 looser, Section 7) and which variants are valid (Section 5).

**Dense part S\* and an explicit semi-free-start pair.** The dense part used by the attack is the following pair (rows -4..15 follow the trail; CV1 is arbitrary, chosen with a fixed seed):

```
CV  = 4e711b6c 2265b1f5 91b7584a d8f16adf cd613e30 c386bbc4 1027c4d1 414c343c
Wx  = 621956cc a8092e3a 7456d02f c79695d1 caac322d 8c82485e 84f8bead 3d7da000 d32b8c00 50b037fc 6e995630 e0784026 4ea34a38 dbb63b0b e8bb8779 8057fd5a
Wy  = 621956cc a8092e3a 7456d02f c79695d1 caac322d 8c82485e 84f8bead 1d7da000 d76b8400 70b037fc 6b98449a e0705426 4ea34a38 dbb63b0b e8bb8779 8417f55a
```

A complete 38-step semi-free-start collision following all of rows -4..37 (rebuilt from the first tail success of one estimator run, Section 7; W0..W6 by the inverse expansion, CV1 by inverting steps 7..0 of S*): the 38-step compressions of M and M' from CV1 are equal, checked with our SHA-256 and with the organizer reference verifier/hash_functions.py:

```
CV1 = 15cd4cd4 18d560b3 b8688c9d c67a8216 23ef659f 769960d0 5c6d35f1 491f99c9
M   = c8f84017 6e17820b 09fac5bb cc9e96c2 6243bb1e 5cc11591 851131e7 76216e98 d32b8c00 50b037fc 6e995630 e0784026 4ea34a38 dbb63b0b e8bb8779 8057fd5a
M'  = c8f84017 6e17820b 09fac5bb cc9e96c2 6243bb1e 5cc11591 851131e7 56216e98 d76b8400 70b037fc 6b98449a e0705426 4ea34a38 dbb63b0b e8bb8779 8417f55a
out = caceaa23 f2e5026a 504b7cb6 c3525ed7 017de1bf a522791e 0a585616 3e886ba3
```

## 4. Success event, conditions, G and F7

*Success event.* A(CV1, v): rows 16..37 of both members follow the signed trail of Section 3 (for A_i, E_i, W_i: the XOR difference equals the trail's, and member x has the trail's value on every difference bit) and the derived value conditions keyed at rows >= 16 hold. Rows 30..37 then carry no difference, so the two compressions from CV1 are equal and M0 || M1, M0 || M1' collide (M1 != M1' since W7 differs). Every success counted in Section 7 is also checked directly to give equal outputs.

*Derived value conditions.* For every bit of every boolean-function instance of rows >= 16 (Sigma1, IF, Sigma0, MAJ of the state; sigma0, sigma1 of the expansion) the trail fixes the input differences and the output difference (intermediate words of the characteristic search). Enumerating the values of the inputs without difference gives the allowed set; a condition is keyed at its latest input row. `cond.py` (Appendix B) derives them; for the published characteristic this reproduces |G| = 32 and q = 2^-101.05 (the paper's hand-derived conditions give 2^-101.0), which validates the derivation. NEW3 has 172 conditions; per key row: 7: 3, 8: 3, 9: 3, 10: 6, 11: 9, 14: 5, 15: 47, 16: 24, 17: 15, 18: 13, 19: 12, 20: 6, 21: 6, 22: 1, 23: 8, 25: 3. Those keyed <= 15 hold on S* except the s0 conditions on W7, which the attack replaces by the modular condition W7 in F7.

*W7.* W7 enters rows >= 16 only through s0(W7) in W22 and W7 in W23, so the trail needs s0(W7 + D7) - s0(W7) = T7 with D7 = 0xe0000000, T7 = 0xfc400800: F7 = {w : s0(w + D7) - s0(w) = T7}, |F7| = 287,309,824 (exhaustive), p2 = 2^-3.90197.

*G.* Row 16 (with all conditions keyed 16) depends on W16 alone given S*; an exhaustive pass over the 2^32 values gives G of 40 words, and for all 40 the row-17 test can pass (sampled: 250..270 passes per 2^24 W17 values each). G = 484e6072 484e60d2 484e6472 484e64d2 48c6607b 48c6607e 48c6607f 48c660db 48c660de 48c660df 48c6647b 48c6647e 48c6647f 48c664db 48c664de 48c664df c8a6607b c8a6607e c8a6607f c8a660db c8a660de c8a660df c8a6647b c8a6647e c8a6647f c8a664db c8a664de c8a664df c8ae607b c8ae607e c8ae607f c8ae60db c8ae60de c8ae60df c8ae647b c8ae647e c8ae647f c8ae64db c8ae64de c8ae64df.

## 5. Variants, the A2 list and the A0 set

A variant v = (A0, A1, A2) replaces A0, A1, A2 of S* in both members (rows 0..6 carry no difference) and recomputes E4, E5, E6 and W8, W9, W10 of each member; it is valid iff every derived condition that reads E4..E6 or A0..A2 holds and (dW_i, ds0(W_i)) for i = 8, 9, 10 equal those of S* (W8..W10 reach rows >= 16 only through these modular quantities). The A2 list (conditions on E6 alone and the W10 differences) has 1408 values (exhaustive over 2^32). The structure of the attack is unchanged: W16 = s0(Y + A1) - A1 + Z0 + c9(A2) with (Y, Z0) a function of (CV1, A0) only (Lemma 5 of the lineage depends only on the message-difference shape), so the table T_j lists, for each (Y, Z0), the variants of A0_j whose W16 is in G.

*A0 set (advice, 64 values).* 2048 random A0 values were screened (1M variant samples each); the 64 best by the screening were kept and |R_j| re-estimated on fresh samples (4M each), so the estimate carries no selection bias: 85,421 valid of 256,000,000 samples in all; with the A2 list of 1408 and A1 uniform over 2^32, SR = sum_j |R_j| = 2^36.9102 (estimate) with one-sided 99% lower bound **SR >= 128,114,134,546 = 2^36.8986**, which the ledger uses (H6). A0 values: cd558204 0ec4af60 08c99fc2 0f4560f8 a8bc51e4 a2556d8c 7e54bfe4 1fcc40a3 a6d56d10 67d2813e 86c650d0 2f3da268 0255cc98 01c58fa4 74d0bf32 b1c90c8a 58b97d12 a1d63da8 e849133a 26d4f2dc cf3c5f70 2146a1db 0cc94e9e 76c0808d 1fd51cac d3421006 da44decf d7c46d3f 8e54f8ec 234e0ccc 77cd5dbc ec450ebc 19d50b4c 20c80e16 cbcae1ba 0ad27d8e 6f3c21ec 39bef20f 9255b1c4 2dd55067 18c88e3d 5c4960cd 2f39cfc6 edd00732 30476df2 f6ccce6b edd4cd1f 13516ebd c451bc62 1fd30f8b e0cadcb9 88bcfe68 d1d53db3 5550e275 f53d9164 bcc64ecf bdbd1107 9646dd54 fe3840f2 3d54abf3 b5564a9b 91547f7b 68bc8b68 9bc6cfb0.

## 6. Algorithm

The algorithm is the variant-table attack of the lineage (aed05522 Sections 4.4-5.4) with the constants of NEW3: preprocessing builds, for the 64 A0 values, the variant lists R_j and the tables T_j over (Y, Z0) in (2^32)^2 (zeroed headers, counting, prefix and fill passes); online, each group draws a first block M0, computes CV1 = F_38(IV, M0), and for each A0_j looks up the bucket T_j[Y, Z0], scans its entries, tests W7 in F7 (one table load), then row 17 and rows 18..37 with early abort, and outputs M0 || M1, M0 || M1' on success. Groups use fresh coins; four work counters (entries, W7 passes, first row-17 test passes, deep entries) are capped (Chebyshev margins 2^-16, 2^-14, 2^-7, 2^-5) and tested after every group.

## 7. The success probability

*Estimator* (`q3t.c`, Appendix B): fixed-effort multilevel splitting with S* fixed. Row 16 exact (W16 uniform in G: factor |G|/2^32); rows 17..22: W_i^x uniform (W16..W21 iid uniform and independent of (W6, W7) by the Step-2 bijection; W22 uniform through W6), W_i^y from the schedule differences, both members stepped, all trail and condition checks of the row; factor (N - 1)/(trials - 1); tail: W7 uniform in F7, rows 23..37 deterministic, factor successes/proposals. Every tail success is checked to give equal outputs.

| run | stage factors log2 (rows 16..22, tail) | tail successes (all collisions) | log2 q |
|---|---|---|---|
| seed 11 | -26.678 -16.032 -13.113 -14.916 -5.947 -6.935 -0.955 -15.014 | 990 | -99.5901 |
| seed 12 | -26.678 -15.978 -13.063 -15.026 -6.023 -7.000 -0.964 -14.986 | 1010 | -99.7185 |
| seed 13 | -26.678 -15.968 -13.132 -15.037 -5.995 -6.908 -0.984 -15.010 | 993 | -99.7115 |
| seed 14 | -26.678 -16.039 -13.107 -15.025 -5.954 -7.002 -1.008 -15.039 | 973 | -99.8545 |
| seed 15 | -26.678 -15.993 -13.060 -14.930 -6.038 -7.008 -0.993 -15.068 | 954 | -99.7676 |
| seed 16 | -26.678 -16.005 -13.117 -15.055 -6.012 -6.994 -0.969 -15.028 | 981 | -99.8579 |

Each run uses N = 2000 particles and 16,384 tail proposals per particle. Mean of 6 runs: 2^-99.7471, relative sd 0.071, one-sided 99% Student bound (t = 3.365, 5 degrees of freedom: mean - t sd / sqrt(6)) 2^-99.8946; 5,901 tail successes, all collisions. **q3_model = 2^-100.0** (H2). The published characteristic measured by the same estimator gives 2^-101.05.

*Groups.* Per group, E[N] = S = SR p2 q3 >= S_model = 2^-67.00333. With pair budget delta = 1 (H5; no measurement for NEW3 is claimed), Bonferroni gives Pr[N >= 1] >= S_model (1 - delta/2) = 2^-68.00333 per group; groups are independent; N_G is the smallest integer with 1 - exp(-N_G q_lb) - P_cap >= 0.39.

## 8. Ledger (exact; `ledger_n3.py`, Appendix B)

| term | value |
|---|---|
| N_G | 146,227,926,952,758,750,725 = 2^66.98678 |
| caps NE / NW / N1 / N2 | 367,668,199,532,479,611,218,413 / 11,671,982,335,115,322,691,505 / 183,788,308,969,164,068,014 / 734,618,967,536,629,633 |
| P_cap | 7.2501e-07 |
| online operations (N_G x (89 + 13 + 16 x 51) + 3 (NE+B) + 43 (NW+B) + 17 (N1+B) + 3142 (N2+B)) | 1,744,569,649,998,554,687,340,740 = 2^80.5291 |
| preprocessing operations (base passes scaled: zero/prefix by 64/256, count/fill by SR x 40 / (SR_base x 22)) | 395,225,042,671,389,909,954,014 = 2^66.9734 units |
| first-block compressions | N_G |
| allowances A_C + A_S + DEV = 2^45 + 2^50 + 2^50 (Section 9) | 2^51.0224 |
| attack and preprocessing | 2^69.65674 |
| **T x 2728 (exact integer)** | **2,538,710,716,289,933,555,947,482** |
| **T** | **2^69.656742, claimed 69.65675** |
| memory (64 x 2^64 headers of 32 bytes + SR x 40 x 2^32 entries of 64 bytes) | 2^80.26 bytes |

First-row-17-test and deep-path fractions are charged at 2^-6 and 2^-14 of the W7 passes (measured: all of row 17 passes about 2^-16 of entries per G word); the base filings used 2^-10 and the exact row-17 count. The first-test fraction for NEW3 was not measured separately: 2^-6 is charged because the E17 part of NEW3's row-17 conditions alone has more than 6 bits; at 2^-4 the claim is 69.742. The per-group fixed count 89 + 13 + 16 x 51 assumes the four-lane block of the base program (51 operations per four A0 blocks) repeated for 64 instead of 256 tables. "Preprocessing" in claim.json is the counted table construction plus the three allowances. Sensitivity (same exact ledger, one input changed):

```
claimed (q3_model 2^-100.0, delta 1, k 64, A_C 2^45, A_S = DEV = 2^50)   69.65675   (attack 69.6567, N_G 2^66.9868)
q3_model 2^-99.75                                                        69.44863   (attack 69.4486, N_G 2^66.7368)
q3_model 2^-100.25                                                       69.87056   (attack 69.8706, N_G 2^67.2368)
q3_model 2^-100.5                                                        70.08942   (attack 70.0894, N_G 2^67.4868)
delta 0.564                                                              69.22944   (attack 69.2294, N_G 2^66.4647)
delta 3/2                                                                70.53983   (attack 70.5398, N_G 2^67.9868)
deep/first-test fractions 2^-8, 2^-4                                     69.74213   (attack 69.7421, N_G 2^66.9868)
A_C 2^60                                                                 69.65853   (attack 69.6567, N_G 2^66.9868)
A_C 2^66                                                                 69.76683   (attack 69.6567, N_G 2^66.9868)
A_C = A_S = DEV = 2^60                                                   69.66210   (attack 69.6567, N_G 2^66.9868)
A_C = 2^70 (if the published search allowance is charged)                70.83856   (attack 69.6567, N_G 2^66.9868)
SR / 2                                                                   69.86843   (attack 69.8684, N_G 2^67.9868)
```

## 9. The characteristic search and its measured cost

All searches ran in one OrbStack Linux container (Ubuntu 22.04; Kissat 4.0.1, CaDiCaL 1.9.5 via python-sat, CryptoMiniSat 5.8, STP 2.3.3) on one 10-core machine. Sequence: (1) message-difference shape search: minimum HW(dW) = 25 on the shape W7..W11, W15, W16, W23, W25 (284 s, 10 parallel bounds); enumeration of the 24 XOR patterns of HW 25 (76 s); (2) full signed characteristics with the XOR pattern fixed and signs free, the tail bounded by an attack-aware weight (P <= 43), the dense part bounded by HW(dA7..15) <= 26, HW(dE7..15) <= 47, HW(dE14..15) <= 4, HW(dA13..15) <= 10 (the weights of the published characteristic; earlier runs with looser bounds produced characteristics that did not couple): NEW3's run took 2,586 s; (3) joint coupling check, value-exact dense part with a value-exact tail (steps 16..19), P <= 43: 1,262 s; (4) dense values and the estimator: minutes.

The whole campaign, including every failed attempt, development, estimator and variant runs, used the machine for 24.0 hours: at most 10 x 86,330 = 863,260 core-seconds = 2^19.72 s. At the calibration of 2^21.383 target-compression units per solver core-second used by aed05522 (from the promoted filing 6eeefb64) this is 2^41.1 units. The ledger charges A_C = 2^45 (characteristic search), A_S = 2^50 (dense part S* and its variants' constants; the dense solve took minutes) and DEV = 2^50 (everything else). Literature inputs: the message-difference shape (also re-derived by step (1)), and the published weight profile used as bounds in step (2).

*Is the published search reused?* The state trail of NEW3 equals the published one with the members swapped, and our searches only produced coupled characteristics once the dense part was bounded by the published weights (HW(dA7..15) <= 26, HW(dE7..15) <= 47; searches with HW <= 30 / 55 produced value-feasible but non-coupling characteristics). Our argument that A_C = 2^45 suffices: the information taken from the paper is four integers, not the trail; a sweep over such bounds (a few hundred values) multiplies the search cost by at most 2^9 and stays far below 2^60; the solver never had the published characteristic, and it returned a different signed message difference with a measurably different (higher) probability. A judge who instead holds that NEW3 reuses the costly part of the published search should charge the published allowance A_C = 2^70: the ledger then gives 70.84 (sensitivity table), and this package would not improve the published frontier.

## 10. Heuristics

- H1 single-trial chaining value: CV1 = F_38(IV, M0) behaves as uniform for the events of one variant (as in the lineage).
- H2 q3: the variant-averaged q3 is at least 2^-100.0 (Section 7: single dense part S*; the variants change W8..W10 values, which the lineage's studies found not to move q3 measurably).
- H3 table pricing: unit-cost table access in the word RAM (memory reported, not scored), as in the lineage.
- H4 allowances: A_C, A_S, DEV bounded by the measured campaign (Section 9).
- H5 pair budget delta = 1.
- H6 SR: sum of |R_j| over the 64 A0 values is at least the 99% lower bound of Section 5.
- H7 counted program: the per-path executed operation counts of the public counted program (aed05522/1db43310: 89, 13, 51 per four blocks, 6 per entry, 43 per W7 pass, 17 per first-test pass, 3,142 per deep entry) apply with NEW3's constants; the preprocessing passes scale with their drivers (tables, entries).

## 11. Limitations

- NEW3's state trail is the published one with the members swapped; the novelty is the signed message difference (W10, W11, W23) and that it was found and measured by our own search.
- q3 is estimated (participant-run, one dense part, 6 runs); delta is not measured (delta = 1 is charged); no organizer experiment is declared.
- Operation counts are those of the public counted program, not re-counted for NEW3 (H7); the deep-path and first-test fractions are charged above the measured rates.
- The tables need 2^80.26 bytes; the claim is in the word-RAM model of the track.

## Appendix A. Data

Per-row signed differences of the published characteristic for comparison (A, E, W):

```
  -4  ================================  ================================  
  -3  ================================  ================================  
  -2  ================================  ================================  
  -1  ================================  ================================  
   0  ================================  ================================  ================================
   1  ================================  ================================  ================================
   2  ================================  ================================  ================================
   3  ================================  ================================  ================================
   4  ================================  ================================  ================================
   5  ================================  ================================  ================================
   6  ================================  ================================  ================================
   7  =nu=============================  uuu=============================  ==n=============================
   8  =========n=====n====n======u====  ====u====n==nu=====nu===n==u====  =====u===u==========n===========
   9  ================================  =====u==n==u================u=uu  ==u=============================
  10  ================================  =========u=====u====u===========  =====n=u=======n===n==n=n=n=u=u=
  11  ====================u=======un==  ==n==============unn=========u==  ============u======u=u==========
  12  =u===n====n======u===nu=======n=  ==nuuu====n===nu=============u=n  ================================
  13  ==n============n================  ===============u=====nuu=nnnu=n=  ================================
  14  ====u=========nn========u==u====  ====n==========n================  ================================
  15  ======n=u=======n===============  ====================u===n=======  =====u===n==========n===========
  16  ================================  =u=======n====u====n==u=========  ==u=============================
  17  ==u=============================  ================================  ================================
  18  ================================  =============n=============u====  ================================
  19  ================================  =======nn=======n===============  ================================
  20  ================================  ================================  ================================
  21  ================================  ==u=============================  ================================
  22  ================================  ================================  ================================
  23  ================================  ================================  =======uu=======u===============
  24  ================================  ================================  ================================
  25  ================================  ================================  ==n=============================
  26  ================================  ================================  ================================
  27  ================================  ================================  ================================
  28  ================================  ================================  ================================
  29  ================================  ================================  ================================
  30  ================================  ================================  ================================
  31  ================================  ================================  ================================
  32  ================================  ================================  ================================
  33  ================================  ================================  ================================
  34  ================================  ================================  ================================
  35  ================================  ================================  ================================
  36  ================================  ================================  ================================
  37  ================================  ================================  ================================
```

## Appendix B. Programs (SHA-256 and full listings of every file behind the numbers of this package; the claim: `python3 ledger_n3.py --SR 128114134546 --k 64`)

- `ledger_n3.py`: 8f2d2cb1b069e09d78f6721aac85c1a38a4f93648b02002589edfa2c8308940f
- `cond.py`: 2220ff08693b795d999eabb5c31dac06fcf9905eb57f403bdd2dbe05901426a8
- `q3t.c`: c2ead6d71290dc184e22f4ca533961e7521480ddc8039c4a822b702ebd46d8e6
- `prep.py`: 7550447964f6b5444638db1b60142475ea839cb066e262b6bfeb6d713b957299
- `var.c`: feafffa51f58f3aae6a48b0c34fc3f9e70421c71ac66c20c487991bea6de7f16
- `prepvar.py`: e9fff31bfae4a1d07fcc75a18a9ba0baff67a5c7aeccd7a8e2df14107f27a4e0
- `sdmodel.py`: fac660e9f5de63bf4e071ec7538598ceff1362466b26e37be28f9f8f3cfae416
- `vmodel.py`: 86bafa88614a1b85b1d3601f3b27479c381442769b0fda054ff7651dbd84244d
- `joint.py`: 7e641e68540e79d3be7902d52bccb372febe17dc16ca5364f9390c3ecf37cb95
- `stepk.py`: 26e26b8bf40d6c00d95a59d2dc463d6aade21df557b886277f20db5a127a3d4b
- `rebuild.py`: 88d40cc76b5432621964c84f548be807ab8c7025ff44b772240e67fe0c46de94
- `sha38.py`: 7aa83ceebd6baede02877736640e066e09d640656a08929e792ae1c5c1b0fe67

### ledger_n3.py

```python
#!/usr/bin/env python3
"""ledger_n3.py - exact ledger of the variant-table attack instantiated with the NEW3 characteristic.
Algorithm and counted-program structure: the public variant-table attack (c99df2dc / 0ae69bcb lineage, as filed in
aed05522 and 1db43310); its executed per-path operation counts are used as a premise (H7n). Inputs that differ from
the base: SR (sum of |R_j| over the selected A0 values, statistical lower bound; k = 64 tables), |G'| = 40 table words,
|F7| = 287,309,824 (exhaustive), q3_model, delta, deep-path / first-test fractions (charged above the measured ones),
preprocessing (the base total split into its passes: zero/prefix scaled by k/256, count/fill by SR * |G'| / (SR_base * 22)), and
allowances (A_C = measured characteristic search, A_S = measured dense solve, DEV = all development, generously).
Integers and Fractions throughout; exp/log through Decimal at 80 digits with explicit margins."""
from fractions import Fraction as Fr
from decimal import Decimal as D, getcontext
import argparse, math
getcontext().prec = 80
C = 2728
F7 = 287_309_824
p2 = Fr(F7, 2 ** 32)
BASE_SR, BASE_G, BASE_PRE_OPS = 191_773_672_732, 22, 385_844_947_274_217_344_088_044
FIXED = 3366
COST = dict(NE=3, NW=43, N1=17, N2=3142)
EPS = dict(NE=Fr(1, 2 ** 16), NW=Fr(1, 2 ** 14), N1=Fr(1, 2 ** 7), N2=Fr(1, 2 ** 5))
GEN_OPS, GEN_UNITS = 2 ** 32 + 1024, 6

def dlog2(x):
    x = Fr(x); return (D(x.numerator).ln() - D(x.denominator).ln()) / D(2).ln()

def qmodel(q):
    num = Fr(round(q * 100)) / 100
    return Fr(int((D(2) ** (D(num.numerator) / D(num.denominator))) * D(10) ** 75), 10 ** 75)

def ledger(SR, Gp=40, k=64, q3=-100.0, delta=Fr(1), f1=Fr(1, 2 ** 6), f2=Fr(1, 2 ** 14), AC=45, AS=50, DEV=50, succ=Fr(39, 100), NG=None):
    q = qmodel(q3); S = SR * p2 * q; qlb = S * (1 - delta / 2)
    ent = Fr(SR * Gp, 2 ** 32)
    E = dict(NE=2 * (ent + k), NW=ent * p2)
    E['N1'] = E['NW'] * f1; E['N2'] = E['NW'] * f2
    B = dict(NE=2 * (k * 236544 + k), NW=k * 236544, N1=k * 236544, N2=k * 236544)
    def pcap(ng): return sum(Fr(B[c]) / (EPS[c] ** 2 * ng * E[c]) for c in B)
    def ok(ng):
        return D(1) - (-(D(ng) * D(qlb.numerator) / D(qlb.denominator))).exp() - D(pcap(ng).numerator) / D(pcap(ng).denominator) - D(succ.numerator) / D(succ.denominator) > D('1e-40')
    if NG is None:
        lo, hi = 1, 2 ** 90
        while lo < hi:
            mid = (lo + hi) // 2
            if ok(mid): hi = mid
            else: lo = mid + 1
        NG = lo
    caps = {c: math.ceil((1 + EPS[c]) * NG * E[c]) for c in B}
    fixed = 89 + 13 + math.ceil(k / 4) * (75 - 24)   # prologue + epilogue + four-lane blocks (base: 3366 for 256)
    online = NG * fixed + sum(COST[c] * (caps[c] + B[c]) for c in B)
    # base pass split (aed05522 Section 5.1): zero 2^73.1, prefix 2^75.8 (per table: 2^64 headers), count 2^76.7, fill 2^77.3
    # (per entry), rest < 2^53; the base total is distributed in these proportions, then each part is scaled by its driver.
    parts = {'zero': 2 ** 73.1, 'prefix': 2 ** 75.8, 'count': 2 ** 76.7, 'fill': 2 ** 77.3}
    tot = sum(parts.values())
    perT = Fr(BASE_PRE_OPS) * Fr(parts['zero'] + parts['prefix']) / Fr(tot)
    perE = Fr(BASE_PRE_OPS) * Fr(parts['count'] + parts['fill']) / Fr(tot)
    pre = math.ceil(perT * Fr(k, 256) + perE * Fr(SR * Gp, BASE_SR * BASE_G)) + 2 ** 53
    alw = 2 ** AC + 2 ** AS + 2 ** DEV
    Tnum = online + pre + GEN_OPS + C * (NG + GEN_UNITS + alw)
    T = Fr(Tnum, C)
    claim = math.ceil(float(dlog2(T)) * 1e5) / 1e5
    assert D(Tnum).ln() - D(C).ln() <= D(round(claim * 1e5)) / D(100000) * D(2).ln()
    mem = k * 2 ** 64 * 32 + SR * Gp * 2 ** 32 * 64   # headers + 2-word (64-byte) entries: each variant appears once per (Y, g)
    return dict(NG=NG, log2NG=float(dlog2(NG)), S=float(dlog2(S)), qlb=float(dlog2(qlb)), Pcap=float(pcap(NG)), online=online, log2online=float(dlog2(online)),
                pre=pre, log2pre_units=float(dlog2(Fr(pre, C))), log2attack=float(dlog2(Fr(Tnum - C * alw, C))), Tnum=Tnum, log2T=float(dlog2(T)), claim=claim,
                caps=caps, log2mem=math.log2(mem), alw=float(dlog2(alw)))

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--SR', type=int, default=128114134546);   # claim: python3 ledger_n3.py --SR 128114134546 --k 64
    ap.add_argument('--q3', type=float, default=-100.0)
    ap.add_argument('--delta', default='1'); ap.add_argument('--sens', action='store_true'); ap.add_argument('--k', type=int, default=64)
    a = ap.parse_args()
    r = ledger(a.SR, k=a.k, q3=a.q3, delta=Fr(a.delta))
    for k in ('NG', 'log2NG', 'S', 'qlb', 'Pcap', 'online', 'log2online', 'pre', 'log2pre_units', 'log2attack', 'alw', 'Tnum', 'log2T', 'claim', 'log2mem'): print(k, r[k])
    print('caps', r['caps'])
    if a.sens:
        for name, kw in [('q3 -99.75', dict(q3=-99.75)), ('q3 -100.25', dict(q3=-100.25)), ('q3 -100.5', dict(q3=-100.5)), ('delta 0.564', dict(delta=Fr(141, 250))),
                         ('delta 3/2', dict(delta=Fr(3, 2))), ('f1 1/16, f2 1/256', dict(f1=Fr(1, 16), f2=Fr(1, 256))),
                         ('A_C 2^60', dict(AC=60)), ('A_C 2^66', dict(AC=66)), ('A_C = A_S = DEV = 2^60', dict(AC=60, AS=60, DEV=60)), ('A_C 2^70 (published-search allowance)', dict(AC=70)), ('SR / 2', dict(SR=a.SR // 2))]:
            kk = dict(SR=a.SR, k=a.k, q3=a.q3, delta=Fr(a.delta)); kk.update(kw)
            x = ledger(**kk); print('%-28s %.5f   (attack %.4f, N_G 2^%.4f)' % (name, x['claim'], x['log2attack'], x['log2NG']))
```

### cond.py

```python
"""Derive value conditions of a signed trail from its boolean-function instances (own code).
For each step r and bit j, the instances Sigma1(E_{r-1}), IF(E_{r-1}, E_{r-2}, E_{r-3}),
Sigma0(A_{r-1}), MAJ(A_{r-1}, A_{r-2}, A_{r-3}) must produce the trail's output signed difference
(intermediate words S1_r, IF_r, S0_r, MJ_r). Inputs with a difference have their x value fixed by
the sign; for the inputs without a difference, enumerate their values and keep the allowed set.
A condition is (refs, allowed): refs = [(kind, row, bit)] of the non-difference inputs, allowed =
set of value tuples. Keyed at the largest input row."""
import itertools

def sym_xy(s, v):
    """symbol and a value for non-diff bits -> (x, y)"""
    if s == 'u': return 1, 0
    if s == 'n': return 0, 1
    return v, v

FN = {'XOR': lambda a, b, c: a ^ b ^ c, 'IF': lambda a, b, c: (a & b) ^ ((1 - a) & c), 'MAJ': lambda a, b, c: (a & b) ^ (a & c) ^ (b & c)}

def bit(row, j):    # row string MSB first
    return row[31 - j]

def derive(rows, inter, steps):
    """rows[(kind, i)] -> 32-symbol string ('=', 'u', 'n'; others mean '='), kinds 'A', 'E';
    inter[(name, r)] -> 32-symbol output string for name in S1, IF, S0, MJ. Returns list of
    dicts {key, refs, allowed, src} and a list of impossible instances."""
    conds, bad = [], []
    def g(kind, i, j):
        if kind == 'Z': return '0'
        s = rows.get((kind, i), '=' * 32)[31 - j]
        return s if s in 'un' else '='
    for r in steps:
        specs = []
        for j in range(32):
            specs.append(('S1', 'XOR', [('E', r - 1, (j + 6) % 32), ('E', r - 1, (j + 11) % 32), ('E', r - 1, (j + 25) % 32)], j))
            specs.append(('IF', 'IF', [('E', r - 1, j), ('E', r - 2, j), ('E', r - 3, j)], j))
            specs.append(('S0', 'XOR', [('A', r - 1, (j + 2) % 32), ('A', r - 1, (j + 13) % 32), ('A', r - 1, (j + 22) % 32)], j))
            specs.append(('MJ', 'MAJ', [('A', r - 1, j), ('A', r - 2, j), ('A', r - 3, j)], j))
            if r >= 16:   # W_r = s1(W_{r-2}) + W_{r-7} + s0(W_{r-15}) + W_{r-16}
                specs.append(('s1', 'XOR', [('W', r - 2, (j + 17) % 32), ('W', r - 2, (j + 19) % 32)] + ([('W', r - 2, j + 10)] if j + 10 < 32 else [('Z', 0, 0)]), j))
                specs.append(('s0', 'XOR', [('W', r - 15, (j + 7) % 32), ('W', r - 15, (j + 18) % 32)] + ([('W', r - 15, j + 3)] if j + 3 < 32 else [('Z', 0, 0)]), j))
        for name, fn, ins, j in specs:
            out = inter.get((name, r), '=' * 32)[31 - j]
            out = out if out in 'un' else '='
            syms = [g(*t) for t in ins]
            free = [k for k, s in enumerate(syms) if s == '=']
            syms = [('=' if s == '0' else s) for s in syms]
            # deduplicate repeated references (rotations never repeat a bit, MAJ/IF use distinct rows)
            allowed = set()
            for vals in itertools.product((0, 1), repeat=len(free)):
                vv = dict(zip(free, vals))
                xs, ys = zip(*[sym_xy(syms[k], vv.get(k, 0)) for k in range(3)])
                ox, oy = FN[fn](*xs), FN[fn](*ys)
                o = '=' if ox == oy else ('u' if ox == 1 else 'n')
                if o == out: allowed.add(vals)
            if not allowed:
                bad.append((name, r, j)); continue
            if len(allowed) < 2 ** len(free):
                refs = [ins[k] for k in free]
                conds.append(dict(key=max(t[1] for t in refs), refs=refs, allowed=sorted(allowed), src='%s_%d[%d]' % (name, r, j)))
    return conds, bad

def check(conds, val):
    """val(kind, row) -> 32-bit word of member x. Returns failing conditions."""
    fails = []
    for c in conds:
        t = tuple((val(k, i) >> b) & 1 for k, i, b in c['refs'])
        if t not in set(map(tuple, c['allowed'])): fails.append(c)
    return fails

def intermediates_from_pair(trace_x, trace_y, steps, Wx=None, Wy=None):
    """exact intermediate output differences from a conforming pair (A, E dicts of both members; W lists)."""
    from sha38 import S0, S1, CH, MAJ, s0, s1
    (Ax, Ex), (Ay, Ey) = trace_x, trace_y
    def sym(x, y):
        return ''.join('=' if ((x >> j) & 1) == ((y >> j) & 1) else ('u' if (x >> j) & 1 else 'n') for j in range(31, -1, -1))
    inter = {}
    for r in steps:
        inter[('S1', r)] = sym(S1(Ex[r - 1]), S1(Ey[r - 1]))
        inter[('IF', r)] = sym(CH(Ex[r - 1], Ex[r - 2], Ex[r - 3]), CH(Ey[r - 1], Ey[r - 2], Ey[r - 3]))
        inter[('S0', r)] = sym(S0(Ax[r - 1]), S0(Ay[r - 1]))
        inter[('MJ', r)] = sym(MAJ(Ax[r - 1], Ax[r - 2], Ax[r - 3]), MAJ(Ay[r - 1], Ay[r - 2], Ay[r - 3]))
        if Wx is not None and r >= 16:
            inter[('s1', r)] = sym(s1(Wx[r - 2]), s1(Wy[r - 2])); inter[('s0', r)] = sym(s0(Wx[r - 15]), s0(Wy[r - 15]))
    return inter
```

### q3t.c

```c
// Trail-based estimator of the uncontrolled probability of a 38-step SHA-256 characteristic (own code).
// q = Pr[rows 16..37 follow the signed trail | dense part, W7 in F7], W0..W6 uniform (Lemma 4 structure).
// Input file (text, hex words): see prep.py. Usage: q3t <datafile> <seed> <N> <T> [g-cache]
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdint.h>
typedef uint32_t u32;
static const u32 K[64] = {
 0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,
 0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,
 0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070};
static inline u32 ror(u32 x, int n) { return (x >> n) | (x << (32 - n)); }
static inline u32 S0(u32 x) { return ror(x, 2) ^ ror(x, 13) ^ ror(x, 22); }
static inline u32 S1(u32 x) { return ror(x, 6) ^ ror(x, 11) ^ ror(x, 25); }
static inline u32 s0(u32 x) { return ror(x, 7) ^ ror(x, 18) ^ (x >> 3); }
static inline u32 s1(u32 x) { return ror(x, 17) ^ ror(x, 19) ^ (x >> 10); }
static inline u32 CH(u32 x, u32 y, u32 z) { return (x & y) ^ (~x & z); }
static inline u32 MAJ(u32 x, u32 y, u32 z) { return (x & y) ^ (x & z) ^ (y & z); }
static uint64_t rs[4];
static inline uint64_t rotl(uint64_t x, int k) { return (x << k) | (x >> (64 - k)); }
static uint64_t nxt(void) { uint64_t r = rotl(rs[1] * 5, 7) * 9, t = rs[1] << 17; rs[2] ^= rs[0]; rs[3] ^= rs[1]; rs[1] ^= rs[2]; rs[0] ^= rs[3]; rs[2] ^= t; rs[3] = rotl(rs[3], 45); return r; }
static void seed(uint64_t s) { for (int i = 0; i < 4; i++) { s += 0x9e3779b97f4a7c15ULL; uint64_t z = s; z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9ULL; z = (z ^ (z >> 27)) * 0x94d049bb133111ebULL; rs[i] = z ^ (z >> 31); } }
static inline u32 r32(void) { return (u32)(nxt() >> 32); }

typedef struct { u32 A[2][42], E[2][42], W[2][38]; } St;     // A/E index +4
#define AA(s, m, i) (s)->A[m][(i) + 4]
#define EE(s, m, i) (s)->E[m][(i) + 4]
static u32 MA[38], SA[38], ME[38], SE[38], MW[38], SW[38];   // trail: xor mask and x-value on the mask, rows 0..37
static St base; static u32 D7, T7;
typedef struct { int key, n, kind[3], row[3], bit[3]; u32 allowed; } Cond;
static Cond CO[8192]; static int nCO;

static inline void step(St *s, int i) {
    for (int m = 0; m < 2; m++) {
        u32 a = AA(s, m, i - 1), b = AA(s, m, i - 2), c = AA(s, m, i - 3), d = AA(s, m, i - 4);
        u32 e = EE(s, m, i - 1), f = EE(s, m, i - 2), g = EE(s, m, i - 3), h = EE(s, m, i - 4);
        u32 T1 = h + S1(e) + CH(e, f, g) + K[i] + s->W[m][i];
        EE(s, m, i) = d + T1; AA(s, m, i) = T1 + S0(a) + MAJ(a, b, c);
    }
}
static inline int condok(const St *s, int r) {
    for (int c = 0; c < nCO; c++) {
        if (CO[c].key != r) continue;
        int idx = 0;
        for (int q = 0; q < CO[c].n; q++) { u32 w = CO[c].kind[q] == 2 ? s->W[0][CO[c].row[q]] : CO[c].kind[q] ? EE(s, 0, CO[c].row[q]) : AA(s, 0, CO[c].row[q]); idx |= ((w >> CO[c].bit[q]) & 1) << q; }
        if (!((CO[c].allowed >> idx) & 1)) return 0;
    }
    return 1;
}
static inline int rowok(const St *s, int r) {
    u32 ax = AA(s, 0, r), ex = EE(s, 0, r), wx = s->W[0][r];
    if (!condok(s, r)) return 0;
    return ((ax ^ AA(s, 1, r)) == MA[r]) && ((ax & MA[r]) == SA[r]) && ((ex ^ EE(s, 1, r)) == ME[r]) && ((ex & ME[r]) == SE[r])
        && ((wx ^ s->W[1][r]) == MW[r]) && ((wx & MW[r]) == SW[r]);
}
static inline void sched(St *s, int i) { for (int m = 0; m < 2; m++) s->W[m][i] = s1(s->W[m][i - 2]) + s->W[m][i - 7] + s0(s->W[m][i - 15]) + s->W[m][i - 16]; }
static inline int inF7(u32 w) { return s0(w + D7) - s0(w) == T7; }

static void load(const char *fn) {
    FILE *f = fopen(fn, "r"); if (!f) { perror(fn); exit(1); }
    char key[32];
    while (fscanf(f, "%31s", key) == 1) {
        if (!strcmp(key, "D7")) fscanf(f, "%x", &D7);
        else if (!strcmp(key, "T7")) fscanf(f, "%x", &T7);
        else if (!strcmp(key, "ROW")) { int r; u32 a, b, c, d, e, g; fscanf(f, "%d %x %x %x %x %x %x", &r, &a, &b, &c, &d, &e, &g); MA[r] = a; SA[r] = b; ME[r] = c; SE[r] = d; MW[r] = e; SW[r] = g; }
        else if (!strcmp(key, "ST")) { int m, i; u32 a, e; fscanf(f, "%d %d %x %x", &m, &i, &a, &e); AA(&base, m, i) = a; EE(&base, m, i) = e; }
        else if (!strcmp(key, "COND")) { Cond *c = &CO[nCO++]; fscanf(f, "%d %d", &c->key, &c->n); for (int q = 0; q < c->n; q++) fscanf(f, "%d %d %d", &c->kind[q], &c->row[q], &c->bit[q]); fscanf(f, "%x", &c->allowed); }
        else if (!strcmp(key, "W")) { int m, i; u32 w; fscanf(f, "%d %d %x", &m, &i, &w); base.W[m][i] = w; }
    }
    fclose(f);
}

int main(int argc, char **argv) {
    load(argv[1]); uint64_t sd = strtoull(argv[2], 0, 10); int N = atoi(argv[3]), T = atoi(argv[4]);
    seed(sd);
    u32 dW16 = (s1(base.W[1][14]) + base.W[1][9]) - (s1(base.W[0][14]) + base.W[0][9]);   // W0, W1 carry no difference
    // row 16 exhaustive (cached)
    static u32 G[1 << 20]; long nG = 0;
    char cache[512]; snprintf(cache, sizeof cache, "%s.g16", argv[1]);
    FILE *fc = fopen(cache, "rb");
    if (fc) { nG = fread(G, 4, 1 << 20, fc); fclose(fc); }
    else {
        for (uint64_t w = 0; w < (1ULL << 32); w++) {
            St s; memcpy(s.A, base.A, sizeof s.A); memcpy(s.E, base.E, sizeof s.E);
            s.W[0][16] = (u32)w; s.W[1][16] = (u32)w + dW16; step(&s, 16);
            if (rowok(&s, 16)) { if (nG < (1 << 20)) G[nG] = (u32)w; nG++; }
        }
        if (nG > (1 << 20)) { fprintf(stderr, "G too large %ld\n", nG); nG = 1 << 20; }
        fc = fopen(cache, "wb"); fwrite(G, 4, nG, fc); fclose(fc);
    }
    if (argc > 5 && !strcmp(argv[5], "live")) {   // row-17 pass counts per G word (sampled W17)
        int live = 0; uint64_t S = 1ULL << 24;
        for (long gi = 0; gi < nG; gi++) {
            St s = base; s.W[0][16] = G[gi]; s.W[1][16] = G[gi] + dW16; step(&s, 16);
            uint64_t pass = 0;
            for (uint64_t k = 0; k < S; k++) {
                St t = s; u32 wx = r32();
                u32 dsch = (s1(t.W[1][15]) + t.W[1][10]) - (s1(t.W[0][15]) + t.W[0][10]) + s0(t.W[1][2]) - s0(t.W[0][2]);
                t.W[0][17] = wx; t.W[1][17] = wx + dsch; step(&t, 17); pass += rowok(&t, 17);
            }
            live += pass > 0;
            printf("G %08x row17 passes %llu / 2^24\n", G[gi], (unsigned long long)pass);
        }
        printf("live G words: %d of %ld\n", live, nG); return 0;
    }
    uint64_t f7 = 0; for (int k = 0; k < 1 << 20; k++) f7 += inF7(r32());
    double lv[8]; lv[0] = nG ? log2((double)nG) - 32 : -INFINITY;
    if (!nG) { printf("seed %llu row16 impossible\n", (unsigned long long)sd); return 0; }
    St *cur = malloc(sizeof(St) * N), *nx = malloc(sizeof(St) * N); int ncur = N;
    for (int k = 0; k < N; k++) { St s = base; u32 w = G[nxt() % nG]; s.W[0][16] = w; s.W[1][16] = w + dW16; step(&s, 16); cur[k] = s; }
    for (int r = 17; r <= 22; r++) {
        uint64_t tries = 0; int got = 0;
        while (got < N) {
            if (tries > (1ULL << 34)) { printf("seed %llu stalled at row %d\n", (unsigned long long)sd, r); return 0; }
            const St *p = &cur[nxt() % ncur]; tries++;
            u32 wx = r32();
            u32 dsch = (s1(p->W[1][r - 2]) + p->W[1][r - 7]) - (s1(p->W[0][r - 2]) + p->W[0][r - 7]);
            if (r == 22) dsch += T7; else dsch += s0(p->W[1][r - 15]) - s0(p->W[0][r - 15]);
            St s = *p; s.W[0][r] = wx; s.W[1][r] = wx + dsch; step(&s, r);
            if (rowok(&s, r)) nx[got++] = s;
        }
        lv[r - 16] = log2((double)(N - 1) / (double)(tries - 1));
        St *t = cur; cur = nx; nx = t;
    }
    uint64_t prop = (uint64_t)N * T, succ = 0, coll = 0;
    for (uint64_t k = 0; k < prop; k++) {
        St s = cur[k % N]; u32 w7; do w7 = r32(); while (!inF7(w7));
        s.W[0][7] = w7; s.W[1][7] = w7 + D7;
        int ok = 1;
        for (int r = 23; r < 38 && ok; r++) { sched(&s, r); step(&s, r); ok = rowok(&s, r); }
        if (ok) {
            succ++;
            if (succ == 1 && getenv("DUMP")) {
                FILE *fd = fopen(getenv("DUMP"), "w");
                for (int m = 0; m < 2; m++) for (int i = 0; i < 38; i++) fprintf(fd, "W %d %d %08x\n", m, i, s.W[m][i]);
                fclose(fd);
            }
            int eq = 1; for (int i = 34; i < 38; i++) if (AA(&s, 0, i) != AA(&s, 1, i) || EE(&s, 0, i) != EE(&s, 1, i)) eq = 0;
            coll += eq;
        }
    }
    lv[7] = succ ? log2((double)succ / prop) : -INFINITY;
    double tot = 0; for (int i = 0; i < 8; i++) tot += lv[i];
    printf("seed %llu |G| %ld p2 %.4f stages", (unsigned long long)sd, nG, log2((double)f7 / (1 << 20)));
    for (int i = 0; i < 8; i++) printf(" %.3f", lv[i]);
    printf(" | succ %llu coll %llu | log2q %.4f\n", (unsigned long long)succ, (unsigned long long)coll, tot);
    return 0;
}
```

### prep.py

```python
"""prep.py <char.json> <pair.json> <out.dat> [inter.json]: data file for q3t.c (own code).
pair.json: {"cv": [8 words], "Wx": [16], "Wy": [16]} (dense pair; if it is a full 38-step
conforming pair and no inter.json is given, intermediates of rows >= 16 are taken from it).
inter.json: {"S1_16": row, ...} intermediate signed outputs from the SAT solution."""
import sys, json
sys.path.insert(0, '/work/m38'); sys.path.insert(0, sys.argv[0].rsplit('/', 1)[0])
from sha38 import trace, s1, M32
from cond import derive, check, intermediates_from_pair
C = {int(k): v for k, v in json.load(open(sys.argv[1])).items()}
P = json.load(open(sys.argv[2]))
cv, Wx, Wy = P['cv'], P['Wx'], P['Wy']
ax, ex, _, _ = trace(cv, Wx, 16); ay, ey, _, _ = trace(cv, Wy, 16)
def ms(row):
    m = sum(1 << (31 - k) for k, c in enumerate(row) if c in 'un'); s = sum(1 << (31 - k) for k, c in enumerate(row) if c == 'u')
    return m, s
def sval(row):   # y - x for the signed row ('u': x = 1, y = 0)
    return sum((-(1 << (31 - k)) if c == 'u' else (1 << (31 - k))) for k, c in enumerate(row) if c in 'un') & M32
out = []
for r in range(16, 38):
    row = C.get(r, {'A': '=' * 32, 'E': '=' * 32, 'W': '=' * 32})
    out.append('ROW %d %08x %08x %08x %08x %08x %08x' % ((r,) + ms(row['A']) + ms(row['E']) + ms(row['W'])))
for m, (A, E) in enumerate(((ax, ex), (ay, ey))):
    for i in range(-4, 16): out.append('ST %d %d %08x %08x' % (m, i, A[i], E[i]))
for m, W in enumerate((Wx, Wy)):
    for i in range(16): out.append('W %d %d %08x' % (m, i, W[i]))
assert all(c not in 'un' for c in C.get(20, {'W': '='})['W']), 'W20 difference not supported'
d7 = (Wy[7] - Wx[7]) & M32
t7 = (sval(C.get(22, {'W': '=' * 32})['W']) - ((Wy[15] - Wx[15]) & M32)) & M32
out = ['D7 %08x' % d7, 'T7 %08x' % t7] + out
# value conditions of the boolean functions of steps 16..37
rows = {}
for i, r in C.items():
    rows[('A', i)] = r['A']; rows[('E', i)] = r['E']; rows[('W', i)] = r['W']
if len(sys.argv) > 4:
    I = json.load(open(sys.argv[4])); inter = {(k.split('_')[0], int(k.split('_')[1])): v for k, v in I.items()}
else:
    fx, fy = trace(cv, Wx, 38), trace(cv, Wy, 38)
    inter = intermediates_from_pair((fx[0], fx[1]), (fy[0], fy[1]), range(16, 38), fx[2], fy[2])
conds, bad = derive(rows, inter, range(16, 38))
assert not bad, ('impossible boolean instances', bad[:5])
Ax, Ex = ax, ex
early = [c for c in conds if c['key'] <= 15]
fails = check(early, lambda k, i: {'A': Ax, 'E': Ex, 'W': dict(enumerate(Wx))}[k][i])
print('conditions: %d (keyed <= 15: %d, violated by the dense pair: %d)' % (len(conds), len(early), len(fails)))
for c in fails[:10]: print('  violated', c['src'], c['refs'], c['allowed'])
for c in conds:
    if c['key'] <= 15: continue
    am = sum(1 << sum(b << q for q, b in enumerate(t)) for t in c['allowed'])
    out.append('COND %d %d %s %x' % (c['key'], len(c['refs']), ' '.join('%d %d %d' % ({'A': 0, 'E': 1, 'W': 2}[k], i, b) for k, i, b in c['refs']), am))
open(sys.argv[3], 'w').write('\n'.join(out) + '\n')
from collections import Counter
print('conditions per key row:', sorted(Counter(c['key'] for c in conds).items()))
print('D7 %08x T7 %08x' % (d7, t7))
```

### var.c

```c
// Variant freedom of a 38-step characteristic (own code). var <prefix.var.dat> <seed> <nA0> <samples-per-A0>
// 1) exhaustive A2 list: conditions that read E6 only (with fixed rows), W10 modular/s0 differences;
// 2) per random A0: validity rate of (A1 uniform, A2 uniform in list) -> |R(A0)| estimate = rate * |list| * 2^32;
// SR estimate for 256 random A0 = 256 * mean |R(A0)| (no A0 selection).
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdint.h>
typedef uint32_t u32;
static const u32 K[16] = {0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174};
static inline u32 ror(u32 x, int n) { return (x >> n) | (x << (32 - n)); }
static inline u32 S0(u32 x) { return ror(x, 2) ^ ror(x, 13) ^ ror(x, 22); }
static inline u32 S1(u32 x) { return ror(x, 6) ^ ror(x, 11) ^ ror(x, 25); }
static inline u32 s0(u32 x) { return ror(x, 7) ^ ror(x, 18) ^ (x >> 3); }
static inline u32 CH(u32 x, u32 y, u32 z) { return (x & y) ^ (~x & z); }
static inline u32 MAJ(u32 x, u32 y, u32 z) { return (x & y) ^ (x & z) ^ (y & z); }
static uint64_t rs[4];
static inline uint64_t rotl(uint64_t x, int k) { return (x << k) | (x >> (64 - k)); }
static uint64_t nxt(void) { uint64_t r = rotl(rs[1] * 5, 7) * 9, t = rs[1] << 17; rs[2] ^= rs[0]; rs[3] ^= rs[1]; rs[1] ^= rs[2]; rs[0] ^= rs[3]; rs[2] ^= t; rs[3] = rotl(rs[3], 45); return r; }
static void seed(uint64_t s) { for (int i = 0; i < 4; i++) { s += 0x9e3779b97f4a7c15ULL; uint64_t z = s; z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9ULL; z = (z ^ (z >> 27)) * 0x94d049bb133111ebULL; rs[i] = z ^ (z >> 31); } }
static inline u32 r32(void) { return (u32)(nxt() >> 32); }
static u32 BA[2][20], BE[2][20];   // index +4
#define A_(m, i) BA[m][(i) + 4]
#define E_(m, i) BE[m][(i) + 4]
static u32 DW[11], DS[11];
typedef struct { int n, kind[3], row[3], bit[3]; u32 allowed; int dep; } Cond;   // dep bits: 1 A0, 2 A1, 4 A2
static Cond CO[4096]; static int nCO;
static int depof(int kind, int row) {   // which of A0, A1, A2 a word depends on
    if (kind == 0) return row == 0 ? 1 : row == 1 ? 2 : row == 2 ? 4 : 0;
    if (row == 4) return 7; if (row == 5) return 6; if (row == 6) return 4; return 0;
}
typedef struct { u32 a0, a1, a2, e4, e5, e6; } Var;
static inline u32 wordv(const Var *v, int kind, int row) {
    if (kind == 0) return row == 0 ? v->a0 : row == 1 ? v->a1 : row == 2 ? v->a2 : A_(0, row);
    return row == 4 ? v->e4 : row == 5 ? v->e5 : row == 6 ? v->e6 : E_(0, row);
}
static inline int conds_ok(const Var *v, int need) {   // check conditions whose dependency is within 'need'
    for (int c = 0; c < nCO; c++) {
        if (CO[c].dep & ~need) continue;
        int idx = 0;
        for (int q = 0; q < CO[c].n; q++) idx |= ((wordv(v, CO[c].kind[q], CO[c].row[q]) >> CO[c].bit[q]) & 1) << q;
        if (!((CO[c].allowed >> idx) & 1)) return 0;
    }
    return 1;
}
static inline u32 Wi(int m, int i, u32 e4, u32 e5, u32 e6) {   // W_i, i = 8, 9, 10 with E4..E6 replaced
    u32 E[12]; for (int k = 4; k < 12; k++) E[k] = E_(m, k);
    E[4] = e4; E[5] = e5; E[6] = e6;
    return E[i] - A_(m, i - 4) - E[i - 4] - S1(E[i - 1]) - CH(E[i - 1], E[i - 2], E[i - 3]) - K[i];
}
static inline int wok(int i, u32 e4, u32 e5, u32 e6) { u32 x = Wi(0, i, e4, e5, e6), y = Wi(1, i, e4, e5, e6); return y - x == DW[i] && s0(y) - s0(x) == DS[i]; }
int main(int argc, char **argv) {
    FILE *f = fopen(argv[1], "r"); char key[16];
    while (fscanf(f, "%15s", key) == 1) {
        if (!strcmp(key, "ST")) { int m, i; u32 a, e; fscanf(f, "%d %d %x %x", &m, &i, &a, &e); A_(m, i) = a; E_(m, i) = e; }
        else if (!strcmp(key, "DW")) { int i; fscanf(f, "%d", &i); fscanf(f, "%x %x", &DW[i], &DS[i]); }
        else if (!strcmp(key, "COND")) { Cond *c = &CO[nCO++]; fscanf(f, "%d", &c->n); c->dep = 0; for (int q = 0; q < c->n; q++) { fscanf(f, "%d %d %d", &c->kind[q], &c->row[q], &c->bit[q]); c->dep |= depof(c->kind[q], c->row[q]); } fscanf(f, "%x", &c->allowed); }
    }
    fclose(f);
    seed(strtoull(argv[2], 0, 10)); int nA0 = atoi(argv[3]); long S = atol(argv[4]);
    // 1) A2 list
    static u32 L[1 << 22]; long nL = 0;
    for (uint64_t a2 = 0; a2 < (1ULL << 32); a2++) {
        Var v = {0}; v.a2 = (u32)a2; v.e6 = A_(0, 6) + v.a2 - S0(A_(0, 5)) - MAJ(A_(0, 5), A_(0, 4), A_(0, 3));
        if (!conds_ok(&v, 4)) continue;
        if (!wok(10, 0, 0, v.e6)) continue;
        if (nL < (1 << 22)) L[nL] = v.a2; nL++;
    }
    printf("A2 list %ld (2^%.3f)\n", nL, log2((double)nL)); fflush(stdout);
    if (!nL) return 0;
    // 2) per A0 validity rate
    double sum = 0, sumsq = 0;
    static u32 A0L[65536]; int nL0 = 0;
    FILE *fa = fopen(argv[3], "r");
    if (fa) { while (nL0 < 65536 && fscanf(fa, "%x", &A0L[nL0]) == 1) nL0++; fclose(fa); nA0 = nL0; }
    for (int t = 0; t < nA0; t++) {
        u32 a0 = nL0 ? A0L[t] : r32(); long ok = 0;
        for (long k = 0; k < S; k++) {
            Var v; v.a0 = a0; v.a1 = r32(); v.a2 = L[nxt() % (nL < (1 << 22) ? nL : (1 << 22))];
            v.e6 = A_(0, 6) + v.a2 - S0(A_(0, 5)) - MAJ(A_(0, 5), A_(0, 4), A_(0, 3));
            v.e5 = A_(0, 5) + v.a1 - S0(A_(0, 4)) - MAJ(A_(0, 4), A_(0, 3), v.a2);
            v.e4 = A_(0, 4) + v.a0 - S0(A_(0, 3)) - MAJ(A_(0, 3), v.a2, v.a1);
            if (!conds_ok(&v, 7)) continue;
            if (!wok(9, v.e4, v.e5, v.e6) || !wok(8, v.e4, v.e5, v.e6)) continue;
            ok++;
        }
        double R = (double)ok / S * nL * 4294967296.0;
        sum += R; sumsq += R * R;
        printf("A0 %08x valid %ld/%ld |R| ~ 2^%.3f\n", a0, ok, S, ok ? log2(R) : -1.0);
    }
    double mean = sum / nA0;
    printf("mean |R(A0)| 2^%.3f ; SR(256 random A0) ~ 2^%.3f\n", log2(mean), log2(256 * mean));
    return 0;
}
```

### prepvar.py

```python
"""prepvar.py <prefix>: data for var.c from <prefix>.char.json, .inter.json, .pair.json (own code).
A variant replaces A0, A1, A2 of the dense pair (rows 0..6 carry no difference, so both members share
them); E4, E5, E6 and W8, W9, W10 of each member are recomputed. Validity: every derived condition that
reads E4..E6 or A0..A2 holds (member x), and (dW_i, ds0(W_i)) for i = 8, 9, 10 equal the dense pair's."""
import sys, json
sys.path.insert(0, '/work/m38')
from cond import derive, intermediates_from_pair
from sha38 import trace, s0, M32
pre = sys.argv[1]
C = {int(k): v for k, v in json.load(open(pre + '.char.json')).items()}
I = json.load(open(pre + '.inter.json')); inter = {(k.split('_')[0], int(k.split('_')[1])): v for k, v in I.items()}
P = json.load(open(pre + '.pair.json'))
rows = {}
for i, r in C.items(): rows[('A', i)] = r['A']; rows[('E', i)] = r['E']; rows[('W', i)] = r['W']
fx, fy = trace(P['cv'], P['Wx'], 16), trace(P['cv'], P['Wy'], 16)
dense_inter = intermediates_from_pair((fx[0], fx[1]), (fy[0], fy[1]), range(7, 16))   # exact dense-step outputs from the pair
for k, v in dense_inter.items(): inter.setdefault(k, v)
conds, bad = derive(rows, inter, range(7, 38))
assert not bad, bad[:5]
ax, ex, wx, _ = trace(P['cv'], P['Wx'], 16); ay, ey, wy, _ = trace(P['cv'], P['Wy'], 16)
out = []
for m, (A, E) in enumerate(((ax, ex), (ay, ey))):
    for i in range(-4, 16): out.append('ST %d %d %08x %08x' % (m, i, A[i], E[i]))
for i in (8, 9, 10):
    out.append('DW %d %08x %08x' % (i, (wy[i] - wx[i]) & M32, (s0(wy[i]) - s0(wx[i])) & M32))
dep = lambda k, i: (k == 'E' and 4 <= i <= 6) or (k == 'A' and 0 <= i <= 2)
nc = 0
for c in conds:
    if any(k == 'W' for k, i, b in c['refs']): continue
    if not any(dep(k, i) for k, i, b in c['refs']): continue
    am = sum(1 << sum(b << q for q, b in enumerate(t)) for t in c['allowed'])
    out.append('COND %d %s %x' % (len(c['refs']), ' '.join('%d %d %d' % ({'A': 0, 'E': 1}[k], i, b) for k, i, b in c['refs']), am))
    nc += 1
open(pre + '.var.dat', 'w').write('\n'.join(out) + '\n')
print('variant conditions:', nc)
```

### sdmodel.py

```python
"""Own signed-difference CNF model of reduced SHA-256 (written from scratch for this search).

Each bit of every word is a pair (v, d): v = value in member x, d = 1 iff member y differs
(member y's bit is v XOR d). Symbols: d = 0 '=' (value v), (v, d) = (1, 1) 'u', (0, 1) 'n'.
- Boolean functions (XOR3 for Sigma/sigma, IF, MAJ): exact two-member relations.
- Modular addition: signed-carry relation s_a + s_b + s_c = s_z + 2 s_c' with s = d (2v - 1),
  values ignored (the standard signed-difference relaxation; value consistency is checked later
  by solving for a conforming pair).
Rows of the state are indexed as in FIPS / the paper: A_i, E_i for i = -4..; step i uses W_i."""
import itertools
from functools import lru_cache
from pysat.formula import CNF, IDPool
from pysat.card import CardEnc, EncType

B = 32
K = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5, 0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174, 0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da, 0x983e5152, 0xa831c66d]
ROT = lambda w, n: w[n:] + w[:n]          # w[j] = bit j; ROTR by n: new[j] = old[j + n]


def qm_cnf(nvars, allowed, dontcare=()):
    """Minimal-ish CNF (prime implicates covering the forbidden set) of a boolean relation
    over nvars variables; allowed and dontcare are sets of assignments (tuples of 0/1)."""
    allowed, dontcare = set(allowed), set(dontcare)
    forbidden = [a for a in itertools.product((0, 1), repeat=nvars) if a not in allowed and a not in dontcare]
    if not forbidden:
        return []
    # implicants of the forbidden function (as cubes with None = free), merging with don't-cares
    on = set(forbidden) | dontcare
    cubes = {tuple(a) for a in on}
    primes = set()
    while cubes:
        nxt, used = set(), set()
        cl = list(cubes)
        idx = {}
        for c in cl:
            for k in range(nvars):
                if c[k] is None: continue
                key = c[:k] + (None,) + c[k + 1:]
                idx.setdefault((k, key), []).append(c)
        for (k, key), group in idx.items():
            vals = {g[k] for g in group}
            if vals == {0, 1}:
                nxt.add(key); used.update(group)
        primes |= cubes - used
        cubes = nxt
    primes = list(primes)
    # greedy cover of the forbidden minterms (don't-cares need not be covered)
    def covers(p, m): return all(p[k] is None or p[k] == m[k] for k in range(nvars))
    todo = set(forbidden); chosen = []
    while todo:
        best = max(primes, key=lambda p: (sum(covers(p, m) for m in todo), -sum(x is not None for x in p)))
        chosen.append(best); todo = {m for m in todo if not covers(best, m)}
    # a cube of the forbidden set -> clause forbidding it
    return [[(k + 1) * (-1 if p[k] == 1 else 1) for k in range(nvars) if p[k] is not None] for p in chosen]


@lru_cache(None)
def rel_bool(fn):
    """inputs (v0,d0,v1,d1,v2,d2) -> output (vo,do); exact for both members."""
    f = {'XOR': lambda a, b, c: a ^ b ^ c, 'IF': lambda a, b, c: (a & b) ^ ((1 - a) & c), 'MAJ': lambda a, b, c: (a & b) ^ (a & c) ^ (b & c)}[fn]
    allowed = set()
    for v0, d0, v1, d1, v2, d2 in itertools.product((0, 1), repeat=6):
        x = f(v0, v1, v2); y = f(v0 ^ d0, v1 ^ d1, v2 ^ d2)
        allowed.add((v0, d0, v1, d1, v2, d2, x, x ^ y))
    return qm_cnf(8, allowed)


@lru_cache(None)
def rel_add():
    """signed-carry addition bit: (va,da,vb,db,vc,dc,vz,dz,vn,dn) with s_a+s_b+s_c = s_z + 2 s_n.
    For d = 0 the value bit is free (don't care)."""
    allowed = set()
    sg = lambda v, d: (2 * v - 1) if d else 0
    for t in itertools.product((0, 1), repeat=10):
        va, da, vb, db, vc, dc, vz, dz, vn, dn = t
        if sg(va, da) + sg(vb, db) + sg(vc, dc) == sg(vz, dz) + 2 * sg(vn, dn):
            allowed.add(t)
    return qm_cnf(10, allowed)


class SD:
    def __init__(self):
        self.pool = IDPool(); self.cnf = CNF(); self.words = {}

    def word(self, name):
        if name not in self.words:
            self.words[name] = [(self.pool.id((name, j, 'v')), self.pool.id((name, j, 'd'))) for j in range(B)]
        return self.words[name]

    def const_word(self, c):
        name = 'K_%08x' % c
        if name not in self.words:
            w = self.word(name)
            for j, (v, d) in enumerate(w):
                self.cnf.append([-d]); self.cnf.append([v] if (c >> j) & 1 else [-v])
        return self.words[name]

    def const0(self):
        if 'ZERO' not in self.words:
            w = self.word('ZERO')
            for v, d in w: self.cnf.append([-v]); self.cnf.append([-d])
        return self.words['ZERO'][0]

    def apply(self, clauses, lits):
        for c in clauses:
            self.cnf.append([lits[abs(l) - 1] * (1 if l > 0 else -1) for l in c])

    def relaxed_copy(self, w):
        """per-instance value bits: shared sign (v when d = 1), free value when d = 0"""
        out = []
        for v, d in w:
            v2 = self.pool.id()
            self.cnf.append([-d, -v, v2]); self.cnf.append([-d, v, -v2])
            out.append((v2, d))
        return out

    def boolfn(self, fn, a, b, c, out, relax=False):
        cl = rel_bool(fn)
        if relax: a, b, c = self.relaxed_copy(a), self.relaxed_copy(b), self.relaxed_copy(c)
        for j in range(B):
            self.apply(cl, [a[j][0], a[j][1], b[j][0], b[j][1], c[j][0], c[j][1], out[j][0], out[j][1]])

    def add(self, a, b, out, tag):
        """out = a + b with signed carries."""
        cl = rel_add()
        carry = [(self.pool.id((tag, j, 'cv')), self.pool.id((tag, j, 'cd'))) for j in range(B + 1)]
        self.cnf.append([-carry[0][1]])          # no carry difference into bit 0
        for j in range(B):
            self.apply(cl, [a[j][0], a[j][1], b[j][0], b[j][1], carry[j][0], carry[j][1], out[j][0], out[j][1], carry[j + 1][0], carry[j + 1][1]])
        # carry out of bit 31 is discarded (mod 2^32): no constraint

    def yval(self, v, d):
        y = self.pool.id(); self.cnf.extend([[-v, -d, -y], [v, d, -y], [v, -d, y], [-v, d, y]]); return y

    def exact_add(self, a, b, out):
        """value-exact z = a + b for member x (bits v) and member y (bits v XOR d)."""
        for m in (0, 1):
            av = [x[0] if m == 0 else self.yval(*x) for x in a]
            bv = [x[0] if m == 0 else self.yval(*x) for x in b]
            zv = [x[0] if m == 0 else self.yval(*x) for x in out]
            c = None
            for j in range(B):
                if c is None:
                    self.xor_eq(av[j], bv[j], None, zv[j]); c = self.pool.id()
                    self.cnf.extend([[-av[j], -bv[j], c], [av[j], -c], [bv[j], -c]])
                else:
                    self.xor_eq(av[j], bv[j], c, zv[j])
                    if j < B - 1:
                        c2 = self.pool.id()
                        self.cnf.extend([[-av[j], -bv[j], c2], [-av[j], -c, c2], [-bv[j], -c, c2], [av[j], bv[j], -c2], [av[j], c, -c2], [bv[j], c, -c2]])
                        c = c2

    def xor_eq(self, a, b, c, z):
        lits = [a, b] + ([c] if c is not None else [])
        import itertools
        for vals in itertools.product((0, 1), repeat=len(lits)):
            r = sum(vals) & 1
            self.cnf.append([(-l if v else l) for l, v in zip(lits, vals)] + [z if r else -z])

    def addn(self, terms, out, tag, exact=False):
        acc = terms[0]
        for k, t in enumerate(terms[1:]):
            dst = out if k == len(terms) - 2 else self.word('%s_t%d' % (tag, k))
            self.add(acc, t, dst, '%s_c%d' % (tag, k))
            if exact: self.exact_add(acc, t, dst)
            acc = dst

    def sigma(self, w, r1, r2, r3, shift, out, relax=False):
        z = self.const0()
        if relax: w = self.relaxed_copy(w)
        third = ROT(w, r3) if not shift else (w[r3:] + [z] * r3)
        self.boolfn('XOR', ROT(w, r1), ROT(w, r2), third, out)

    def zero_diff(self, w):
        for v, d in w: self.cnf.append([-d])

    def hw_lits(self, ws):
        return [d for w in ws for v, d in w]

    def fix(self, w, row):
        """row: 32 symbols MSB first; '=' no diff (value free), 'u'/'n' diff, '0'/'1' value condition, '-' free."""
        for k, s in enumerate(row):
            v, d = w[B - 1 - k]
            if s in '=0123456789+-' and s not in 'un':
                self.cnf.append([-d])
                if s == '0': self.cnf.append([-v])
                if s == '1': self.cnf.append([v])
            elif s == 'u': self.cnf.append([d]); self.cnf.append([v])
            elif s == 'n': self.cnf.append([d]); self.cnf.append([-v])

    def card(self, lits, op, k, enc=EncType.totalizer):
        f = {'<=': CardEnc.atmost, '>=': CardEnc.atleast, '=': CardEnc.equals}[op](lits=lits, bound=k, vpool=self.pool, encoding=enc)
        self.cnf.extend(f.clauses)


def sha256_model(n_msg=38, diff_words=(7, 8, 9, 10, 11, 15, 16, 23, 25), state=(7, 26), with_state=True, zero_start=True, relax_steps=(), relax_kinds=('S', 'B'), exact_steps=()):
    m = SD()
    W = [m.word('W%d' % i) for i in range(n_msg)]
    for i in range(16, n_msg):
        s1, s0 = m.word('s1_%d' % i), m.word('s0_%d' % i)
        m.sigma(W[i - 2], 17, 19, 10, True, s1)
        m.sigma(W[i - 15], 7, 18, 3, True, s0)
        m.addn([s1, W[i - 7], s0, W[i - 16]], W[i], 'mx%d' % i)
    for i in range(n_msg):
        if i not in diff_words: m.zero_diff(W[i])
    A = {i: m.word('A%d' % i) for i in range(state[0] - 4, state[1])}
    E = {i: m.word('E%d' % i) for i in range(state[0] - 4, state[1])}
    if with_state:
        for i in range(state[0], state[1]):
            S1, IF, S0, MJ, T1 = (m.word('%s_%d' % (n, i)) for n in ('S1', 'IF', 'S0', 'MJ', 'T1'))
            rs = i in relax_steps and 'S' in relax_kinds; rb = i in relax_steps and 'B' in relax_kinds
            m.sigma(E[i - 1], 6, 11, 25, False, S1, relax=rs)
            m.boolfn('IF', E[i - 1], E[i - 2], E[i - 3], IF, relax=rb)
            ex = i in exact_steps
            m.addn([E[i - 4], S1, IF, W[i], m.const_word(K[i]) if ex else None][:5 if ex else 4], T1, 't1_%d' % i, exact=ex)
            m.add(A[i - 4], T1, E[i], 'e_%d' % i)
            if ex: m.exact_add(A[i - 4], T1, E[i])
            m.sigma(A[i - 1], 2, 13, 22, False, S0, relax=rs)
            m.boolfn('MAJ', A[i - 1], A[i - 2], A[i - 3], MJ, relax=rb)
            m.addn([T1, S0, MJ], A[i], 'a_%d' % i, exact=ex)
        for i in range(state[0] - 4, state[0]):
            if zero_start: m.zero_diff(A[i]); m.zero_diff(E[i])
        for i in range(state[1] - 8, state[1]): m.zero_diff(A[i])
        for i in range(state[1] - 4, state[1]): m.zero_diff(E[i])
    m.W, m.A, m.E = W, A, E
    return m


def decode(m, model_set, words):
    rows = {}
    for name in words:
        w = m.words[name]; s = ''
        for j in range(B - 1, -1, -1):
            v, d = w[j]
            s += ('u' if v in model_set else 'n') if d in model_set else '='
        rows[name] = s
    return rows
```

### vmodel.py

```python
"""Exact value-level two-member model of SHA-256 rows 0..15 for a given signed characteristic
(own code). Member x is computed exactly; member y's words are x XOR (difference mask) with the
sign bits fixed ('u': x bit 1, 'n': x bit 0), and y's rows are also computed exactly, so every
difference of the characteristic holds with real carries. Free: A0..A6 (with A_-4..A_-1, E_-4..E_-1
implied by the Step-2 bijection, they need not be modeled), W7..W15. Rows 4..6 E words are derived
from A0..A6 (E_i = A_i + A_{i-4} - S0(A_{i-1}) - MAJ(A_{i-1}, A_{i-2}, A_{i-3}), i >= 4)."""
from pysat.formula import IDPool
K = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
     0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
     0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
     0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
     0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85]
B = 32


class V:
    XOR_NATIVE = False
    def __init__(self):
        self.pool = IDPool(); self.cl = []; self.xors = []
        self.T = self.pool.id('TRUE'); self.cl.append([self.T])

    def new(self, n=B, tag=None):
        return [self.pool.id() for _ in range(n)]

    def const(self, c):
        return [self.T if (c >> j) & 1 else -self.T for j in range(B)]

    def xor2(self, a, b):
        o = self.pool.id()
        if V.XOR_NATIVE: self.xors.append([a, b, -o]); return o      # a ^ b ^ ~o = 1  <=>  o = a ^ b
        self.cl += [[-a, -b, -o], [a, b, -o], [a, -b, o], [-a, b, o]]
        return o

    def xor3(self, a, b, c):
        o = self.pool.id()
        if V.XOR_NATIVE: self.xors.append([a, b, c, -o]); return o
        for s in range(8):
            x, y, z = s & 1, s >> 1 & 1, s >> 2 & 1
            r = x ^ y ^ z
            self.cl.append([(-a if x else a), (-b if y else b), (-c if z else c), (o if r else -o)])
        return o

    def maj(self, a, b, c):
        o = self.pool.id()
        self.cl += [[-a, -b, o], [-a, -c, o], [-b, -c, o], [a, b, -o], [a, c, -o], [b, c, -o]]
        return o

    def ifn(self, e, f, g):
        o = self.pool.id()
        self.cl += [[-e, -f, o], [-e, f, -o], [e, -g, o], [e, g, -o]]
        return o

    def add(self, a, b):
        out, c = [], None
        for j in range(B):
            if c is None:
                out.append(self.xor2(a[j], b[j])); c = self.and2(a[j], b[j])
            else:
                out.append(self.xor3(a[j], b[j], c))
                if j < B - 1: c = self.maj(a[j], b[j], c)
        return out

    def and2(self, a, b):
        o = self.pool.id()
        self.cl += [[-a, -b, o], [a, -o], [b, -o]]
        return o

    def addn(self, ws):
        acc = ws[0]
        for w in ws[1:]: acc = self.add(acc, w)
        return acc

    def neg(self, w):  # two's complement: ~w + 1
        return self.add([-x for x in w], self.const(1))

    def rot(self, w, n): return w[n:] + w[:n]

    def S0(self, w): return [self.xor3(*t) for t in zip(self.rot(w, 2), self.rot(w, 13), self.rot(w, 22))]
    def S1(self, w): return [self.xor3(*t) for t in zip(self.rot(w, 6), self.rot(w, 11), self.rot(w, 25))]
    def s0(self, w): return [self.xor3(*t) for t in zip(self.rot(w, 7), self.rot(w, 18), w[3:] + [-self.T] * 3)]
    def s1(self, w): return [self.xor3(*t) for t in zip(self.rot(w, 17), self.rot(w, 19), w[10:] + [-self.T] * 10)]
    def IF(self, e, f, g): return [self.ifn(*t) for t in zip(e, f, g)]
    def MAJ(self, a, b, c): return [self.maj(*t) for t in zip(a, b, c)]

    def eq(self, a, b):
        for x, y in zip(a, b): self.cl += [[-x, y], [x, -y]]


def masks(row):
    """row MSB first -> (xor mask, sign fixes {bit: x value})"""
    m, fx = 0, {}
    for k, s in enumerate(row):
        j = B - 1 - k
        if s in 'un': m |= 1 << j; fx[j] = 1 if s == 'u' else 0
    return m, fx


def add_conditions(v, conds, Ax, Ex, W):
    """value conditions on member-x bits (rows <= 15, W7 excluded) as clauses forbidding disallowed tuples."""
    import itertools
    n = 0
    for c in conds:
        if c['key'] > 15 or any(k == 'W' and i == 7 for k, i, b in c['refs']): continue
        lits = []
        for k, i, b in c['refs']:
            src = {'A': Ax, 'E': Ex, 'W': W}[k]
            if i not in src: lits = None; break
            lits.append(src[i][b])
        if lits is None: continue
        allowed = set(map(tuple, c['allowed']))
        for t in itertools.product((0, 1), repeat=len(lits)):
            if t not in allowed:
                v.cl.append([(-l if bit else l) for l, bit in zip(lits, t)])
        n += 1
    return n


def dense_model(char, last=15, extra_rows=(), free_rows=(), skip=(), free_signs=False, expansion=False):
    """char: {row: {'A': str, 'E': str, 'W': str}} for rows 0..last (signed differences only are used)."""
    v = V()
    A = {i: v.new() for i in range(0, 7)}          # member x A0..A6 (equal in y: rows < 7 carry no difference)
    W = {i: v.new() for i in range(7, last + 1)}   # member x W7..W15
    # E4..E6 from A0..A6
    E = {3: v.new()}                              # E3 is free (it fixes A_-1 of the chaining value)
    for i in (4, 5, 6):
        E[i] = v.addn([A[i], A[i - 4], v.neg(v.S0(A[i - 1])), v.neg(v.MAJ(A[i - 1], A[i - 2], A[i - 3]))])
    def ymask(w, row):
        m, fx = masks(row)
        if not free_signs:
            for j, val in fx.items(): v.cl.append([w[j] if val else -w[j]])
        return [(-x if (m >> j) & 1 else x) for j, x in enumerate(w)]
    Wy = {i: ymask(W[i], char[i]['W']) for i in W}
    # rows 4..6: no differences allowed
    for i in (4, 5, 6):
        assert set(char[i]['E']) <= set('=01+-') and set(char[i]['A']) <= set('=01+-'), i
    Ax = dict(A); Ex = dict(E); Ay = dict(A); Ey = dict(E)
    for i in range(7, last + 1):
        for (AA, EE, WW) in ((Ax, Ex, W), (Ay, Ey, Wy)):
            T1 = v.addn([EE[i - 4], v.S1(EE[i - 1]), v.IF(EE[i - 1], EE[i - 2], EE[i - 3]), v.const(K[i]), WW[i]])
            EE[i] = v.add(AA[i - 4], T1)
            AA[i] = v.addn([T1, v.S0(AA[i - 1]), v.MAJ(AA[i - 1], AA[i - 2], AA[i - 3])])
        # link: y = x XOR mask with signs fixed (rows in free_rows: no link, the trail is whatever the values give)
        if i in free_rows: continue
        for nm, X, Y in (('A', Ax, Ay), ('E', Ex, Ey)):
            if (nm, i) in skip: continue
            m, fx = masks(char[i][nm])
            for j, val in fx.items(): v.cl.append([X[i][j] if val else -X[i][j]])
            v.eq(Y[i], [(-x if (m >> j) & 1 else x) for j, x in enumerate(X[i])])
    if expansion:   # modular conditions of the expansion on the dense words (dW17 = dW24 = dW26 = dW30 = 0)
        def diff(fx, fy): return v.add(fy, v.neg(fx))
        zero = v.const(0)
        v.eq(v.add(diff(v.s1(W[15]), v.s1(Wy[15])), diff(W[10], Wy[10])), zero)
        v.eq(v.add(diff(v.s0(W[9]), v.s0(Wy[9])), diff(W[8], Wy[8])), zero)
        v.eq(v.add(diff(v.s0(W[11]), v.s0(Wy[11])), diff(W[10], Wy[10])), zero)
        v.eq(v.addn([diff(v.s0(W[15]), v.s0(Wy[15])), diff(W[9], Wy[9]), diff(v.s0(W[8]), v.s0(Wy[8])), diff(W[7], Wy[7])]), zero)
    v.A, v.E, v.W, v.Ay, v.Ey, v.Wy = Ax, Ex, W, Ay, Ey, Wy
    return v


def value(model_set, w):
    """model_set: set of true positive literals"""
    return sum(1 << j for j, x in enumerate(w) if (x > 0 and x in model_set) or (x < 0 and (-x) not in model_set))


def write_dimacs(v, fn):
    """CNF plus CryptoMiniSat native XOR lines ('x' prefix: XOR of literals = true)."""
    with open(fn, 'w') as f:
        f.write('p cnf %d %d\n' % (v.pool.top, len(v.cl) + len(v.xors)))
        for c in v.cl: f.write(' '.join(map(str, c)) + ' 0\n')
        for x in v.xors: f.write('x' + ' '.join(map(str, x)) + ' 0\n')
```

### joint.py

```python
"""joint.py <char prefix> <P> <seed> <out prefix>: one CNF = value-exact dense part (rows <= 15, signed dense trail
of <prefix>.char.json, expansion constraints) + signed tail model (steps 16..25, weighted bound P), linked at rows
12..15 (tail (v, d) = dense (x, x XOR y)) and on the message words. Solved with Kissat (own code)."""
import sys, json, time, subprocess, os, math
sys.path.insert(0, '/work/m38')
from sdmodel import sha256_model, decode
from vmodel import dense_model, value
from cond import derive
from collections import Counter
from pysat.card import EncType
pre, P, seed, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
C = {int(k): v for k, v in json.load(open(pre + '.char.json')).items()}
free15 = len(sys.argv) > 5 and sys.argv[5] == 'free1215'   # let the dense rows 12..15 trail be free (only the tail fixes them)
freerows = [int(x) for x in sys.argv[5].split(',')] if len(sys.argv) > 5 and sys.argv[5] != 'free1215' else (range(12, 16) if free15 else ())
import os as _os
m = sha256_model(state=(16, 26), zero_start=False, exact_steps=set(int(x) for x in _os.environ.get('EXACT_TAIL', '').split(',') if x))
for i in range(38): m.fix(m.words['W%d' % i], ''.join(c if c in 'un' else '=' for c in C[i]['W']))
lits = []
for kind, rows, wt in (('E', [16], 2), ('E', [15], 1), ('E', range(17, 26), 3), ('A', range(16, 26), 3), ('W', range(16, 38), 2)):
    lits += m.hw_lits([m.words['%s%d' % (kind, i)] for i in rows if '%s%d' % (kind, i) in m.words]) * wt
m.card(lits, '<=', P, enc=EncType.kmtotalizer)
N1 = m.pool.top
v = dense_model(C, expansion=True, free_rows=freerows)
sh = lambda l: (abs(l) + N1) * (1 if l > 0 else -1)
cl = [list(c) for c in m.cnf.clauses] + [[sh(l) for l in c] for c in v.cl]
nv = N1 + v.pool.top
def xorvar(a, b):
    global nv
    nv += 1; d = nv
    cl.extend([[-a, -b, -d], [a, b, -d], [a, -b, d], [-a, b, d]]); return d
def eqlit(a, b): cl.extend([[-a, b], [a, -b]])
for i in range(12, 16):
    for nm, X, Y in (('A', v.A, v.Ay), ('E', v.E, v.Ey)):
        for j in range(32):
            sv, sd = m.words['%s%d' % (nm, i)][j]
            x, y = sh(X[i][j]), sh(Y[i][j])
            eqlit(sv, x); eqlit(sd, xorvar(x, y))
for i in range(8, 16):     # message words: tail model value bits = dense member-x values
    for j in range(32):
        sv, sd = m.words['W%d' % i][j]; eqlit(sv, sh(v.W[i][j]))
fn = out + '.cnf'
with open(fn, 'w') as f:
    f.write('p cnf %d %d\n' % (nv, len(cl)))
    for c in cl: f.write(' '.join(map(str, c)) + ' 0\n')
t = time.time(); r = subprocess.run(['kissat', '-q', '--seed=%d' % seed, fn], capture_output=True, text=True); os.unlink(fn)
ok = 's SATISFIABLE' in r.stdout; print('joint SAT:', ok, '%.1fs' % (time.time() - t), 'vars', nv, 'clauses', len(cl), flush=True)
if not ok: sys.exit(1)
model = set(int(x) for l in r.stdout.splitlines() if l.startswith('v') for x in l[1:].split() if x != '0' and int(x) > 0)
ms_sd = {l for l in model if l <= N1}
ms_v = {l - N1 for l in model if N1 < l <= N1 + v.pool.top}
names = ['A%d' % i for i in range(12, 26)] + ['E%d' % i for i in range(12, 26)] + ['W%d' % i for i in range(38)]
names += [x for x in m.words if x.split('_')[0] in ('S1', 'IF', 'S0', 'MJ', 's1', 's0') and x.count('_') == 1]
R = decode(m, ms_sd, names)
rows = {(k, i): R.get('%s%d' % (k, i), '=' * 32) for k in 'AEW' for i in range(-4, 38)}
inter = {(x.split('_')[0], int(x.split('_')[1])): rr for x, rr in R.items() if '_' in x}
conds, bad = derive(rows, inter, range(17, 38))
cost = Counter()
for c in conds: cost[c['key']] += len(c['refs']) - math.log2(len(c['allowed']))
print('tail ge17 %.1f k16 %.1f bad %d' % (sum(vv for kk, vv in cost.items() if kk >= 17), cost.get(16, 0), len(bad)), flush=True)
Ws = {str(i): C[i]['W'] for i in range(38) if any(c in 'un' for c in C[i]['W'])}
json.dump(dict(A={i: value(ms_v, v.A[i]) for i in range(0, 16)}, E={i: value(ms_v, v.E[i]) for i in range(3, 16)},
               W={i: value(ms_v, v.W[i]) for i in range(7, 16)}, Ay={i: value(ms_v, v.Ay[i]) for i in range(7, 16)},
               Ey={i: value(ms_v, v.Ey[i]) for i in range(7, 16)}, Wy={i: value(ms_v, v.Wy[i]) for i in range(7, 16)}, Wsigned=Ws),
          open(out + '.dense.json', 'w'))
json.dump(dict(rows=R, ge17=sum(vv for kk, vv in cost.items() if kk >= 17)), open(out + '.tail.json', 'w'))
```

### stepk.py

```python
"""Generic bounded query: python3 stepk.py <name> <json spec>; spec: {"hw_w": 25, "bounds": [[kind, rows, op, k], ...], "fix": {...}}"""
import sys, time, json, os
sys.path.insert(0, '/work/m38')
from sdmodel import sha256_model, decode
from pysat.solvers import Solver
name, spec = sys.argv[1], json.loads(sys.argv[2])
t0 = time.time()
m = sha256_model(diff_words=tuple(spec.get('diff_words', (7, 8, 9, 10, 11, 15, 16, 23, 25))), with_state=spec.get('with_state', True), state=tuple(spec.get('state', (7, 26))), zero_start=spec.get('zero_start', True), relax_steps=set(spec.get('relax_steps', ())), relax_kinds=tuple(spec.get('relax_kinds', ('S', 'B'))), exact_steps=set(spec.get('exact_steps', ())))
if 'hw_w' in spec: m.card(m.hw_lits(m.W), spec.get('hw_w_op', '='), spec['hw_w'])
for kind, rows, op, k in spec.get('bounds', []):
    ws = [m.words['%s%d' % (kind, i)] for i in rows if '%s%d' % (kind, i) in m.words]
    m.card(m.hw_lits(ws), op, k)
for terms, op, k in spec.get('wbounds', []):   # weighted: terms = [[kind, rows, weight], ...] (literals repeated by weight)
    lits = []
    for kind, rows, wt in terms:
        lits += m.hw_lits([m.words['%s%d' % (kind, i)] for i in rows]) * wt
    from pysat.card import EncType
    m.card(lits, op, k, enc=EncType.kmtotalizer if op == '<=' else EncType.totalizer)
for wname, row in spec.get('fix_xor', {}).items():     # difference positions only, signs free
    for q, ch in enumerate(row):
        v_, d_ = m.words[wname][31 - q]; m.cnf.append([d_] if ch in 'un' else [-d_])
for wname, row in spec.get('fix', {}).items():
    m.fix(m.words[wname], row)
t1 = time.time()
class _K:
    def __init__(self, clauses, nv): self.clauses, self.nv = clauses, nv
    def __enter__(self): return self
    def __exit__(self, *a): pass
    def solve(self):
        import subprocess, tempfile
        fn = tempfile.mktemp(suffix='.cnf', dir='/tmp')
        with open(fn, 'w') as f:
            f.write('p cnf %d %d\n' % (self.nv, len(self.clauses)))
            for c in self.clauses: f.write(' '.join(map(str, c)) + ' 0\n')
        r = subprocess.run(['kissat', '-q', '--seed=%d' % spec.get('seed', 0), fn], capture_output=True, text=True)
        os.unlink(fn)
        self.model = [int(x) for l in r.stdout.splitlines() if l.startswith('v') for x in l[1:].split() if x != '0']
        return 's SATISFIABLE' in r.stdout
    def get_model(self): return self.model
_solver = (lambda: _K(m.cnf.clauses, m.pool.top)) if spec.get('solver') == 'kissat' else (lambda: Solver(name=spec.get('solver', 'cadical195'), bootstrap_with=m.cnf.clauses))
with _solver() as s:
    ok = s.solve()
    dt = time.time() - t1
    out = dict(name=name, spec=spec, sat=ok, solve_s=round(dt, 1), build_s=round(t1 - t0, 1))
    if ok:
        ms = set(l for l in s.get_model() if l > 0)
        names = [n for n in ['A%d' % i for i in range(-4, 26)] + ['E%d' % i for i in range(-4, 26)] if n in m.words] + ['W%d' % i for i in range(38)]
        names += [n for n in m.words if n.split('_')[0] in ('S1', 'IF', 'S0', 'MJ', 's1', 's0') and n.count('_') == 1]
        out['rows'] = decode(m, ms, names)
os.makedirs('/work/runs/q', exist_ok=True)
json.dump(out, open('/work/runs/q/%s.json' % name, 'w'))
print(name, 'SAT' if ok else 'UNSAT', '%.1fs' % dt)
```

### rebuild.py

```python
"""rebuild.py <prefix> <dump>: turn an estimator success (member-x/y words W7..W37 with the dense pair) into an explicit
semi-free-start pair (CV1, M, M'), and verify the 38-step compressions with own SHA-256 and the organizer reference."""
import sys, json, struct
sys.path.insert(0, '/work/m38'); sys.path.insert(0, sys.argv[3] if len(sys.argv) > 3 else '/work/verifier')
from sha38 import trace, compress, s0, s1, S0, S1, CH, MAJ, M32
from vmodel import K
pre, dump = sys.argv[1], sys.argv[2]
P = json.load(open(pre + '.pair.json'))
W = {0: {}, 1: {}}
for l in open(dump):
    _, m, i, w = l.split(); W[int(m)][int(i)] = int(w, 16)
# dense part of the pair (rows -4..15) -> A0..A7, E4..E7 values of member x (state rows 0..6 equal in both members)
ax, ex, _, _ = trace(P['cv'], P['Wx'], 16)
msgs = []
for m in (0, 1):
    w = dict(W[m])
    for i in range(6, -1, -1):  # W_i = W_{i+16} - s1(W_{i+14}) - W_{i+9} - s0(W_{i+1})
        w[i] = (w[i + 16] - s1(w[i + 14]) - w[i + 9] - s0(w[i + 1])) & M32
    msgs.append([w[i] for i in range(16)])
assert msgs[0][:7] == msgs[1][:7], 'W0..W6 must coincide'
# CV1: invert steps 7..0 of member x from its dense rows (A0..A7 and E4..E7 of the pair) with the new W0..W7
A = {i: ax[i] for i in range(0, 8)}; E = {i: ex[i] for i in range(4, 8)}
Wx = msgs[0]
for i in range(7, -1, -1):
    a, b, c = A[i - 1], A[i - 2], A[i - 3]; e, f, g = E[i - 1], E[i - 2], E[i - 3]
    T1 = (A[i] - S0(a) - MAJ(a, b, c)) & M32
    A[i - 4] = (E[i] - T1) & M32
    E[i - 4] = (T1 - S1(e) - CH(e, f, g) - K[i] - Wx[i]) & M32
cv = (A[-1], A[-2], A[-3], A[-4], E[-1], E[-2], E[-3], E[-4])
ox, oy = compress(cv, msgs[0], 38), compress(cv, msgs[1], 38)
print('CV1 =', ' '.join('%08x' % x for x in cv))
print('M   =', ' '.join('%08x' % x for x in msgs[0])); print("M'  =", ' '.join('%08x' % x for x in msgs[1]))
print('38-step outputs equal (own SHA-256):', ox == oy, ' messages differ:', msgs[0] != msgs[1])
import hash_functions as hf
bx = b''.join(struct.pack('>I', x) for x in msgs[0]); by = b''.join(struct.pack('>I', x) for x in msgs[1])
print('organizer reference equal:', hf._compress('sha256', cv, bx, 38) == hf._compress('sha256', cv, by, 38))
print('output:', ' '.join('%08x' % x for x in ox))
json.dump(dict(cv=list(cv), M=msgs[0], M2=msgs[1], out=list(ox)), open(pre + '.sfs_pair.json', 'w'))
```

### sha38.py

```python
"""Independent reduced-round SHA-256 (FIPS 180-4) with full trace, written from the spec."""
M32 = 0xFFFFFFFF
K = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2,
]
IV = (0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19)


def ror(x, n):
    return ((x >> n) | (x << (32 - n))) & M32


def S0(x): return ror(x, 2) ^ ror(x, 13) ^ ror(x, 22)
def S1(x): return ror(x, 6) ^ ror(x, 11) ^ ror(x, 25)
def s0(x): return ror(x, 7) ^ ror(x, 18) ^ (x >> 3)
def s1(x): return ror(x, 17) ^ ror(x, 19) ^ (x >> 10)
def CH(x, y, z): return (x & y) ^ (~x & z & M32)
def MAJ(x, y, z): return (x & y) ^ (x & z) ^ (y & z)


def expand(W16, n):
    W = list(W16)
    for i in range(16, n):
        W.append((s1(W[i - 2]) + W[i - 7] + s0(W[i - 15]) + W[i - 16]) & M32)
    return W


def trace(cv, W16, rounds=38):
    """Return (A, E, W, out) with A[i], E[i] indexed i = -4..rounds-1 via dict."""
    a, b, c, d, e, f, g, h = cv
    A = {-1: a, -2: b, -3: c, -4: d}
    E = {-1: e, -2: f, -3: g, -4: h}
    W = expand(W16, rounds)
    for i in range(rounds):
        T1 = (h + S1(e) + CH(e, f, g) + K[i] + W[i]) & M32
        T2 = (S0(a) + MAJ(a, b, c)) & M32
        h, g, f = g, f, e
        e = (d + T1) & M32
        d, c, b = c, b, a
        a = (T1 + T2) & M32
        A[i], E[i] = a, e
    out = tuple((x + y) & M32 for x, y in zip(cv, (a, b, c, d, e, f, g, h)))
    return A, E, W, out


def compress(cv, W16, rounds=38):
    return trace(cv, W16, rounds)[3]
```

