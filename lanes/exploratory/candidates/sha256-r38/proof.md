# Collision attack on 38-step SHA-256: the ePrint 2026/1120 two-block attack with A0-variants of the Step-1 solution, 2^93.86313

Track `sha256-r38-exploratory`, target `sha256-r38-prefix-v1`, cost model `collision-frontier-v5` (C = 2728).
Claim: `time_log2 = 93.86313` target compressions on every run, success probability at least 0.39 (0.3934 under the
stated premises), memory 2^30.1 bytes (reported only), nonuniform advice below 2^13 bytes. No packed or bit-sliced
pricing is used anywhere: every target compression costs one unit and every other operation is a scalar 32-bit
operation on the word RAM.

The attack is the 38-step collision attack of Li, Zhang, Li, Liu, Qian and Zhu, "Pushing Collision Attacks on SHA-2
to 39 Steps" (IACR ePrint 2026/1120, CC BY), in the two-block memory-efficient framework of [LLWS26] (ePrint 2026/1080).
We reuse its 38-step characteristic and its published semi-free-start pair as transcribed and verified in the earlier
r38 filings of this attack (b99301f4 and its successors such as 349e3a6a and 20dbd783), and the exact Step-2 filter set F7.
**The new step (Section 4.3) is the one of our sha256-r37 filing 1c368173:** the second-block word A0 carries no
condition of the characteristic, so the Step-1 solution S has 2^26 *variants* that differ from S only in A0, E4, W8 (and
in the first-block-dependent words W0..W7). Variants sharing their W7 constant c7 form classes, and one W7 test decides
the Step-2 filter of a whole class (Section 5.3). Because the 38-step characteristic has no W6 filter, **every variant
of a passing class is usable**: a first block yields on average 16,440 usable (chaining value, variant) pairs instead of
2^-3.90.

## 0. Summary

- **Algorithm (Sections 4-8).** Messages M0 || M1 and M0 || M1' (128 bytes; padding adds the same third block). A
  first block M0 is two fresh uniform 256-bit words; CV1 = F_38(IV, M0) costs one unit. For each of 64 fixed classes
  of variants (3840 variants each, 245,760 in total) one test W7x = c7 - A_{-1} in F7 decides whether all variants of
  the class pass Step 2. For each variant of a passing class (a *good pair*) the program computes
  E16x = C16 + W0 + s0(W1) (37 counted operations including the stage-3a test of the ten fixed bits of E16x); a
  stage-3a pass (2^-10) is tested against the exact row-16 set (32 words), and a row-16 pass (2^-27 per good pair) is
  checked through row 37. A pair that follows every cell of rows 16..37 collides; it is verified with the target.
- **Rates (exact under H1).** Per first block: 64 p7 = 4.28125 passing classes and g = 64 x 3840 x p7 = 16,440 good
  pairs (p7 = |F7|/2^32 = 2^-3.90197). Measured on 2^23 real first blocks: 1.0005 x g.
- **Probability (Section 7, H2).** For a good pair, q3 = Pr[rows 16..37 follow every cell and printed two-bit
  condition] (|L* | = 1). Rows 16..22 have exactly the same probability for every variant (Lemma 7.1); a variant enters
  rows >= 23 only through W8 in W23 = s1(W21) + W16 + s0(W8) + W7 and W24 = s1(W22) + W17 + s0(W9) + W8. A preregistered
  sequential Monte-Carlo estimate (32 replicates, W8 drawn from the 245,760 variants) gives mean 2^-101.015 and a
  one-sided 99% lower bound 2^-101.045: q3_model = 2^-101.05. On the same 1,073,754,023 row-22 samples rows 23..37
  pass 32,542 times with the variants' W8 and 32,538 times with the published W8. The published-S estimate of the
  earlier r38 filings is 2^-101.02.
- **Cost (Sections 9, 11).** N_FB = 79,982,809,848,158,989,131,448,320 = 2^86.04789 first blocks; per first block 1
  unit plus 686 counted operations, plus on average 608,614.4 counted data-dependent operations (16,440 good pairs at 37
  each, per-class control, stage-3a and row-16 work), all capped by V_MAX. T = 2^93.863122, claimed 93.86313.
  Generous advice allowances (A_C = 2^78, A_S = 2^74, DEV = 2^64) do not change the claim at its rounding.
- **Premises (Section 12).** H1 uniform independent chaining values; H2 q3 >= 2^-101.05 for the variants; H3 the
  expected number of further successes of one first block given a success is small; H4 advice allowances.
- **Checks.** Exhaustive: |G| = 67,108,864; 102,696 distinct c7 values, the 64 classes (3840 each); F7 and its affine
  decomposition; the 32-word row-16 set. End to end on 2^16 + 2^23 real first blocks: every rate as predicted, 1,004
  row-16 passes all checked exactly. Semi-free-start collisions with variant dense parts verified with the repository's
  `verifier/hash_functions._compress` at 38 steps. Two organizer experiments repeat the semi-free-start construction and
  the counted online program on organizer seeds.

## 1. Target, cost model and output

- **Target** sha256-r38-prefix-v1: SHA-256 steps 0..37 on every padded block, the standard IV once, FIPS 180-4
  padding, feed-forward, all eight digest words (repository `verifier/hash_functions.digest(m, "sha256", 38)`).
  The output is two distinct complete messages with equal digests, verified with the target before output.
- **Cost model** collision-frontier-v5: one 38-step target compression = 1 unit; every other executed 256-bit word-RAM
  primitive (load, store, add/sub, and/or/xor/not, shift/rotation, compare, branch, uniform random word) = 1/C unit
  with C = 2728; 64 registers; memory reported only; success at least 0.39 over fresh coins.
- **Notation.** E_i = A_{i-4} + E_{i-4} + S1(E_{i-1}) + CH(E_{i-1}, E_{i-2}, E_{i-3}) + K_i + W_i and A_i = E_i -
  A_{i-4} + S0(A_{i-1}) + MAJ(A_{i-1}, A_{i-2}, A_{i-3}) (mod 2^32); (A_{-1..-4}, E_{-1..-4}) = (a, ..., h) of the
  incoming chaining value; F_R(cv, B) is the R-step compression with feed-forward.

## 2. Sources, credit, and what is new

- [LZLLQZ26] ePrint 2026/1120: the 38-step characteristic (Table 3), two-bit conditions (Table 4), SFS pair (Table 5),
  the three-step attack (Step 1: SAT solve of the dense part, reported 2^38.3; Step 2: random first blocks filtered on
  W7, 2^-4; Step 3: the (W14, W15) freedom, stated 2^2), total 2^104.3 (expected work). [LLWS26] ePrint 2026/1080: the
  framework; [LLW24] EUROCRYPT 2024: the tool.
- The earlier r38 filings of this attack (b99301f4, 349e3a6a, 20dbd783 and others, 100.07 to 100.33): the
  transcription of Tables 3-5, the orientation (x = the message printed second), the `+` reading, the corrected
  two-bit condition W25[4] = W25[6] (printed W25[4] = W25[9], which fails on the pair; bit 19 of s1(W25) is
  W25[4]^W25[6]^W25[29]), the exact filter F7, the exact L* (|L| = 8, |L* | = 1 for the published S), and the q3 SMC
  design. We re-derived and re-checked everything with our own code; we did not execute theirs.
- Our sha256-r37 filing 1c368173 (63.47455, passed AI screening): the A0-variant method, the c7 classes, the success
  analysis. New for 38 steps: the variant family is larger (E4 carries no cell), and there is no W6 filter, so a whole
  class is usable once its W7 test passes; no bit-sliced pricing is needed.

## 3. The characteristic (from the paper, as transcribed in the earlier r38 filings; verified here)

Symbols MSB first: `n` = (x, y) = (0, 1), `u` = (1, 0), `0`/`1` fixed and equal, `=` equal, `+` equal to the same bit
of the vertically adjacent `+` (no difference). Member x is the message printed second (M').

```text
  5  ================================  +++=============================  ================================
  6  ================================  +++=1====0==+1=====0+===1==1====  ================================
  7  =nu=============================  uuu=0+1=11=0+00====1+===0==00=01  ==n=============================
  8  =========n=====n====n======u====  100=u+010n=1nu01=01nu=00n11u1=01  =====u===u==========n===========
  9  ================================  11000u1=n11u0000101101110=01u0uu  ==u=============================
 10  ================================  ==1010=01u00001u=010u=101==10111  =====n=u=======n===n==n=n=n=u=u=
 11  ====================u=======un==  1=n000=0111100101unn00011+111u10  ============u======u=u==========
 12  =u===n====n======u===nu=======n=  01nuuu=110n111nu000100100+010u1n  ================================
 13  ==n============n================  00110101110=000u00111nuu+nnnu1n1  ================================
 14  ====u=========nn========u==u====  =010n0===00===1n=11+0100+1110001  ================================
 15  ======n=u=======n===============  =1==1=1==0=1==11===+u011n1011=1=  =====u===n==========n===========
 16  ================================  =u==10===n===+u1===n0=u=1==+====  ==u=============================
 17  ==u=============================  =0=====+00===+0=+==01=0=0==+====  ================================
 18  ================================  =0=====+01===n1=+==1==1===0u====  ================================
 19  ================================  ==11===nn====1==n===010===11==0=  ================================
 20  ================================  ==1====00====1==0==========1====  ================================
 21  ================================  ==u====10=======1===10==========  ================================
 22  ================================  ==0=============================  ================================
 23  ================================  ==1=============================  =====1=uu=====1=u=1=============
 25  ================================  ================================  ==n=============================
```

Rows -4..4 are entirely `=`: **A0..A4 and E0..E4 carry no condition** (no difference: the chaining value is common and
rows 0..6 of A and E have no u/n).

Two-bit conditions (Table 4) with the corrected reading:

```text
A14[15] = A16[15], A14[23] = A16[23], A14[25] = A16[25], A15[4] = A16[4], A15[7] = A16[7], A15[16] != A16[16]
A15[17] = A16[17], A15[27] = A16[27], A15[29] = A16[29], A16[15] = A17[15], A16[23] = A17[23], A16[25] = A17[25]
A17[9] = A17[20], A17[6] = A17[18], A17[8] = A17[17], A16[29] = A18[29], A18[29] = A19[29], E16[4] != E16[23]
E16[3] != E16[8], E16[14] = E16[28], E16[4] = E17[4], E16[18] = E17[18], E18[0] != E18[13], E17[15] = E18[15]
E17[24] = E18[24], E19[6] != E19[19], E19[20] = E19[2], E21[2] = E21[16], W7[8] != W7[25], W7[14] != W7[18]
W7[1] = W7[12], W8[0] != W8[28], W8[30] != W8[9], W8[1] = W8[18], W16[1] != W16[12], W16[20] != W16[27]
W16[8] = W16[25], W16[14] = W16[18], W16[4] != W16[6], W16[22] != W16[31], W23[0] != W23[30], W23[1] != W23[31]
W23[14] = W23[21], W23[16] = W23[25], W25[4] = W25[6] (printed W25[9]), W25[22] = W25[31], W25[20] = W25[27]
```

The SFS pair (Table 5):

```text
CV  cd278980 1b12a052 b87cc8a6 a9e059c5 c9c3db85 6ca4b5b5 63d13ac1 c0329f1e
M   48fc271b 9fca20cd cc89f96f fc40396f 8b328cb4 6b91ef78 97f9b767 e2450045
    3b016f58 de9804cb 66a99ea5 0ce30b8d a28cd15a 77a1e994 d28e48a0 9b5f6dbb
M'  48fc271b 9fca20cd cc89f96f fc40396f 8b328cb4 6b91ef78 97f9b767 c2450045
    3f416758 fe9804cb 63a88c0f 0ceb1f8d a28cd15a 77a1e994 d28e48a0 9f1f65bb
hash 5d9ca5f4 59ace3a3 26c9c26c 4252c585 4c0803b7 1b4d5ccd 25c3ccc0 90645c4d
```

F_38(CV, M) = F_38(CV, M') = the printed hash under our code and the repository's `_compress`; every cell of rows
-4..37 and every two-bit condition (corrected reading) holds with x = M', y = M (`a0core38.setup`, `sfs38.c`).

## 4. Step 1: the solution S and its A0-variants

### 4.1 S

S is the inner part of the published pair (x | y):

```text
A0  b75dae71 | b75dae71  A5  1ee5f173 | 1ee5f173  A10 bcc85d8c | bcc85d8c  E4  627cb061 | 627cb061  E9  c670b71b | c2e0b710
A1  da6c35e0 | da6c35e0  A6  7fd9cecb | 7fd9cecb  A11 25d3cc99 | 25d3c495  E5  1e847683 | 1e847683  E10 68c3aa97 | 6882a297
A2  479b4dc8 | 479b4dc8  A7  3e016e83 | 5e016e83  A12 4846f2d8 | 0c66b4da  E6  0c1c24b9 | 0c1c24b9  E11 c2f2c1be | e2f2b1ba
A3  d374b0d8 | d374b0d8  A8  b6a6b5f9 | b6e7bde9  A13 c2dc0441 | e2dd0441  E7  e2e9b205 | 02e9b205  E12 5f9d1216 | 63be1213
A4  df740c96 | df740c96  A9  3ec0b304 | 3ec0b304  W8  3f416758 | 3b016f58  E8  99352c79 | 917934e9  E13 35c13b0d | 35c03c77
W9  fe9804cb | de9804cb  W10 63a88c0f | 66a99ea5  W11 0ceb1f8d | 0ce30b8d  W12 a28cd15a | a28cd15a  W13 77a1e994 | 77a1e994
```

### 4.2 The Step-2 equations (Lemma 4.1)

For fixed state rows A0..A13 (both members) and a chaining value CV1, for each member
E_i = A_i + A_{i-4} - S0(A_{i-1}) - MAJ(A_{i-1}, A_{i-2}, A_{i-3}) and W_i = E_i - A_{i-4} - E_{i-4} - S1(E_{i-1}) -
CH(E_{i-1}, E_{i-2}, E_{i-3}) - K_i (i = 0..13). **Lemma 4.1.** Steps 0..13 of F_38 from CV1 with these words reproduce
the state rows; for fixed A0..A13 the map CV1 -> (W0, ..., W7) is a bijection (W7 depends only on A_{-1}, W6 is -A_{-2}
plus a function of A_{-1}, ..., W0 is -E_{-4} plus a function of the earlier coordinates); W8..W13 do not depend on
CV1. (Checked on every constructed pair, Section 13.)

### 4.3 The A0-variants

**Lemma 4.2.** Replace A0 of S by any a0 (both members) and keep A1..A13. For every chaining value:
(a) E5..E13 and W9..W13 are unchanged; (b) E4 = a0 + C4 with C4 = A4 - S0(A3) - MAJ(A3, A2, A1), and
W8x = W8C - E4 with W8C = E8 - A4 - S1(E7) - CH(E7, E6, E5) - K8 (both members shift by the same E4, so W8y - W8x =
D8 = fbc00800 is unchanged); (c) W0..W7 absorb E0..E4; their member differences are 0 for i <= 6 and d7 = 20000000 for
i = 7, because E4, E5, E6 carry no difference (so CH(E6, E5, E4) in step 7 and E4 as E_{i-4} in step 8 cancel between the
members); (d) the only cells involving E4 or W8 are W8's cell (u at bits 26, 22, n at bit 11, the x-values fixed there)
and the printed W8 two-bit conditions W8[0] != W8[28], W8[30] != W8[9], W8[1] = W8[18]; these fix the signed XOR
difference of s0(W8) and hence s0(W8y) - s0(W8x) = fe7f8000, the value of the published pair.

Define **G = {a0 : W8x = W8C - (a0 + C4) and W8y = W8x + D8 follow W8's cell, and the three W8 two-bit conditions
hold}**. Exhaustively |G| = 67,108,864 = 2^26; the published A0 (b75dae71) is in G.

**Lemma 4.3 (validity).** For a0 in G, every chaining value whose words satisfy W7x in F7 (Section 5.1), and the single
l in L*, the pair follows every cell of rows -4..15 (W7's XOR cell excepted) and every printed two-bit condition closing
at a row <= 15 except those on W7, and every modular difference entering the expansion equals the published pair's.
*Checks:* 1,004 row-16 passes of real first blocks (rows -4..16 exactly), sampled good pairs of the organizer experiment
`a0-online-r38` (rows -4..15), and every constructed semi-free-start pair (rows -4..37).

## 5. Step 2 with variants

### 5.1 The exact filter

With d7 = 20000000, the cells of rows 22/23 require s0(W7y) - s0(W7x) = t7 = 03bff800 (the earlier filings' Lemma 3;
W6 carries no difference in the 38-step characteristic, so there is no W6 filter):
F7 = {w : s0(w + d7) - s0(w) = t7}, |F7| = 287,309,824 (exhaustive), p7 = 2^-3.90197. By the carry pattern of w + d7:

```text
[w29=0, 14^18=1, 8^25=1, 1^12=0]                                                          2^28 words
[w29=1, w30=0, 14^18=1, 15^19=1, 8^25=1, 9^26=1, 1^12=0, 2^13=0]                            2^24 words
[w29=1, w30=1, 14^18=1, 15^19=1, 16^20^31=1, 8^25=1, 9^26=1, 10^27^31=1, 1^12=0, 2^13=0, 3^14^31=0]  2^21 words
```

For a variant a0 and CV1: **W7x = c7(a0) - A_{-1}** with c7(a0) = E7 - 2 A3 + S0(A2) + MAJ(A2, A1, a0) - S1(E6) -
CH(E6, E5, a0 + C4) - K7 (c7(b75dae71) = 8f6c89c5, the published constant).

### 5.2 Lemma 5.1 (distribution, per variant)

Under H1, for every fixed a0: Pr[W7x in F7] = p7 exactly; conditioned on it, (W0..W6) is uniform on (2^32)^7 and
independent of W7, which is uniform on F7; for the l of L*, (W16..W21) is a bijective image of (W0..W5) for fixed
(W6, W9..W15) (inverse expansion), hence iid uniform and independent of (W6, W7).

### 5.3 The c7 classes and the selection

c7 takes 102,696 distinct values on G (exhaustive); the largest classes have 3840 variants. A class is G intersected
with one value of c7; for all its variants and a given CV1, W7x is the same word, so one membership test decides the
whole class, and (38 steps having no other Step-2 filter) **every variant of a passing class is a good pair**. The 64
classes used (the 64 largest, ties by smaller c7; 128 classes have 3840) each equal {base XOR s : s subset of mask,
s in G, c7 = the class value} for the descriptors (c7, base, mask) listed in `experiments/a0core38.py` (`CLASSES`;
masks of 15 to 17 bits; checked exhaustively: 3840 members each). Per first block E[passing classes] = 64 p7 = 4.28125
and E[good pairs] = g = 64 x 3840 x p7 = 16,440 (exact under H1).

## 6. Step 3

L* (from the earlier filings, re-checked): for the published S, |L| = 8 and |L* | = 1, the published (W14, W15) =
(d28e48a0, 9f1f65bb) on the x side ((d28e48a0, 9b5f6dbb) on the y side). Rows 12..15 of both members depend only on
S and l, not on CV1 or the variant.

**Row 16.** E16x = C16 + u with u = W0 + s0(W1) (W16 = s1(W14) + W9 + s0(W1) + W0), and every cell of row 16 (both
members) and every two-bit condition closing at row 16 is a function of E16x. Exhaustive enumeration of the 2^22 values
with the row's ten fixed bits (mask 4c431a80) gives exactly 32 passing words:

```text
481b02f9 481b02fa 481b02fd 481b02fe 481b06f9 481b06fa 481b06fd 481b06fe 481b22f9 481b22fa 481b22fd 481b22fe
481b26f9 481b26fa 481b26fd 481b26fe 482302f9 482302fa 482302fd 482302fe 482306f9 482306fa 482306fd 482306fe
482322f9 482322fa 482322fd 482322fe 482326f9 482326fa 482326fd 482326fe
```

By Lemma 5.1 u is uniform for a good pair: Pr[stage 3a] = 2^-10 and Pr[row 16] = 32/2^32 = 2^-27 exactly. For a
row-16 pass the program computes W0..W8 of both members (Lemma 4.1), the y-words, and rows 16..37 with early abort.

**Lemma 6.1.** If rows 16..37 follow every cell, the two second-block outputs are equal (rows 34..37 of A and E have no
difference), so m = M0 || M1 and m' = M0 || M1' collide under the complete target (the third block is the common FIPS
padding block; M1 is a full data block). m != m' because M1 and M1' differ in W7, W8..W11, W15.

## 7. The Step-3 probability for the variants (H2)

### 7.1 Quantity and Lemma 7.1

q3 = the average over the 245,760 selected variants of Pr[rows 16..37 follow every cell and printed two-bit condition |
good], the probability over CV1 (Lemma 5.1). **Lemma 7.1.** Rows 16..22 are functions of S's rows 12..15, l and
W16..W22 (W22 = s1(W20) + W15 + s0(W7) + W6), whose law given goodness is the same for every variant: the probability
of rows 16..22 is identical for all variants. W8 enters rows >= 23 only through W23 = s1(W21) + W16 + s0(W8) + W7 and
W24 = s1(W22) + W17 + s0(W9) + W8 (and later words through them), with fixed modular differences (Lemma 4.2 (d)); only
the values of W23, W24 move, each by a constant added to a word that is near-uniform given rows 16..22.

### 7.2 The estimator (`smc38.c`, Appendix A)

Row 16 exact (stage mean 32/2^32 = 2^-27; initial particles uniform on the 32 words); rows 17..21: E_t^x proposed
uniformly with the row's fixed x-bits imposed (exact weight 2^-f), W_t^x = E_t^x - (the rest of step t), W_t^y =
W_t^x + its exact difference, the whole row checked; row 22: W7 uniform on F7, W6 uniform; rows 23..37 with the W8 of a
variant drawn uniformly from the 245,760 selected variants (and, paired, with the published W8). Multinomial
resampling after every stage; the product of the stage means is unbiased for q3.

### 7.3 Preregistration and results

Frozen before any listed seed ran (`PREREG_q3_r38.txt`, SHA-256 76e76864...; `smc38.c` and `lab38.h` hashes in it):
NP = 2048, M = 512, MT = 32768; seeds 80000..80007, 81000..81007, 82000..82007, 83000..83007; rule: one-sided 99%
Student lower bound of the mean of the 32 linear estimates, q3_model = 2^(floor(100 log2 LB)/100).

| quantity | value |
|---|---|
| per-replicate log2 estimates (seeds in order) | -101.019 -101.051 -101.061 -101.016 -100.978 -100.989 -100.938 -101.022 -101.044 -101.054 -100.958 -100.983 -101.097 -101.086 -101.084 -100.928 -101.014 -100.962 -101.126 -101.054 -100.969 -101.047 -100.962 -100.900 -100.931 -101.048 -101.190 -101.041 -101.127 -100.978 -100.931 -100.953 |
| mean | 2^-101.0154 |
| relative standard deviation; skewness | 0.0465; -0.31 |
| 99% lower bound (Student); percentile bootstrap 1% quantile of the mean | 2^-101.0448; 2^-101.0435 |
| **q3_model** | **2^-101.05** |
| stage means (log2) | 16: -27.000, 17: -16.996, 18: -12.999, 19: -15.011, 20: -6.000, 21: -7.000, 22: -1.000, 23..37: -15.011 |
| rows 23..37, paired, over 1,073,754,023 row-22 survivors | variant W8: 32,542 passes (2^-15.010); published W8: 32,538 (2^-15.010) |
| same replicates with the published W8 | mean 2^-101.0156 |

Consistency: the stage factors equal the per-row condition counts of the tables (27, 17, 13, 15, 6, 7, 1, 15); the
earlier filings' published-S estimate is 2^-101.02 (mean 2^-100.9941); real good pairs pass stage 3a and row 16 at the
exact rates (Section 13.1).

## 8. The algorithm (fixed caps)

```text
input: N_FB, V_MAX; precomputed: S, L*, the 64 class descriptors and their variant data (a0, S0(a0)), the bitmap of
       F7 (2^32 bits) and the bitmap of the row-16 set (2^32 bits)
V = 0
for f = 1 .. N_FB:
    draw two uniform 256-bit words; M0 := their sixteen 32-bit fields; CV1 := F_38(IV, M0)          [1 unit]
    hits := [c : c7_c - A_{-1} in F7]  (64 tests)
    if hits: per-first-block constants of W0, E0, W1 (36 operations); V += 1
        for c in hits:  V += 1
            for each variant a0 of c:  E16x := C16 + W0 + s0(W1); if its ten fixed bits match (stage 3a):
                V += 1; if E16x in the row-16 set: V += 1; W0..W8 of both members; rows 16..37 with early abort
                    if all rows pass: build m, m'; if digest(m) = digest(m') and m != m': output, halt
            V += the class's counted work; if V > V_MAX: halt (failure)
halt (failure)
```

The run executes at most N_FB compressions, N_FB x 686 fixed operations, V_MAX + one class's maximum work of
data-dependent operations, the precomputation and one final verification, whatever the coins.

## 9. The counted program (`experiments/a0core38.py`, `calibrate`)

256-bit word RAM, 64 registers, every executed primitive counted; 32-bit values in the low bits; reduction mod 2^32 is
one AND; S0, S1, s0, s1 cost 8 each (d = x | (x << 32), shifts, XORs, one mask); a bitmap lookup costs 6 (shr 8, add
base, load, and 255, shr, and 1). All counts are produced by running the routines and asserted constant over 20 random
inputs:

| routine | operations |
|---|---|
| first-block words (2 random words, 16 fields) | 30 |
| W7 tests: per class load c7, sub, and, bitmap (6), branch; 64 classes | 640 |
| control allowance per first block (loop counter, hit list, `if hits`, 12 more) | 16 |
| per passing class: control 8, V update 1, cap test 2 | 11 |
| per first block with a passing class: constants (36), V update (1), charged per passing class | 37 |
| per variant (good pair): 2 loads, E0 (add, and), W0 + C16 (add), MAJ (and, or), CH (and, xor), S1 (8), W1 (4 subs, and), s0 (8), E16x (add, and), stage 3a (and, xor, branch), loop (2) | 37 |
| per stage-3a pass: V update, row-16 bitmap (6), branch | 8 |
| per row-16 pass: V update, then at most the full path: E0..E7, W0..W7 (Lemma 4.1), W8, y-words, rows 16..37 (106 per row for both members; row check 53 + branch) | <= 3791 |

The full path (3790, every row passing) is asserted on the published pair by `calibrate`. Correctness of the counted
values: every good pair of the organizer experiment `a0-online-r38` is compared with the Step-2 equations (W7 = c7 -
A_{-1} in F7 and E16x = C16 + W0 + s0(W1) from Lemma 4.1).

## 10. Success probability, independence and caps

A *trial* is (first block f, selected variant a0) (|L* | = 1); A_t: a0 is good for f and rows 16..37 follow every cell
and printed two-bit condition. The program examines every good pair of every processed first block and every row-16
pass, so it finds a success iff some A_t occurs before the caps; every output is verified (Lemma 6.1).

- **Expectation.** E[X_f] = g q3 and E[X] = N_FB g q3 >= (1 + 2^-9)/2 for N_FB = ceil((1 + 2^-9)/2 / (g 2^-101.05)) =
  79,982,809,848,158,989,131,448,320 = 2^86.04789.
- **One first block (H3).** Bonferroni: Pr[X_f >= 1] >= E[X_f] - (1/2) sum_t Pr[A_t] E[X_f - 1 | A_t]. H3 states
  E[X_f - 1 | A_t] <= 2^-9.4, so Pr[X_f >= 1] >= (1 - 2^-10.4) E[X_f].
- **Many first blocks (H1).** Independent chaining values give Pr[X >= 1] >= 1 - exp(-(1 + 2^-9)(1 - 2^-10.4)/2) >=
  1 - exp(-1/2) = 0.393469.
- **Work cap.** The data-dependent work v_f has mean at most vbar = 608,614.40 and is at most 64 x 14,730,251 + 100 <
  2^29.82; by Chebyshev over the independent first blocks, Pr[sum v_f > (1 + 2^-8) N_FB vbar] <=
  2^29.82 / (2^-16 2^86.05 vbar) < 2^-59. V_MAX = ceil((1 + 2^-8) N_FB vbar).
- **Success.** Pr[output a collision] >= 0.393469 - 2^-59 - 2^-60 > 0.3934 > 0.39.

## 11. Ledger (exact; `python3 experiments/a0core38.py ledger`)

```text
T = A_C + A_S + DEV + N_FB + (N_FB x 686 + V_MAX + vmax_class + PRE + FIN) / C + 6
  A_C = 2^78, A_S = 2^74, DEV = 2^64   (allowances, H4; together below 2^-15.8 of T)
  N_FB = 79,982,809,848,158,989,131,448,320 first-block compressions (2^86.04789)
  686 fixed operations per first block
  V_MAX = 48,868,841,106,753,321,718,115,897,062,320 = ceil((1 + 2^-8) N_FB vbar), vbar = 608,614.40:
      per passing class (4.28125 per first block): 11 + 37 -> 205.5
      good pairs: g x 37 = 16,440 x 37 -> 608,280
      stage-3a passes: g x 2^-10 x 8 -> 128.4
      row-16 passes: g x 2^-27 x 3791 -> 0.46
  vmax_class = 14,730,251 (one class's maximum work; the overshoot after the last cap test)
  PRE = 2^40 operations (all precomputation: G and c7 over 2^32 words, the F7 and row-16 bitmaps, the 2^22 row-16
        enumeration, the class data); FIN = 1600 operations and 6 compressions
T x 2728 = 49,142,778,487,769,692,591,855,566,274,027   ->   T = 2^93.863122   ->   time_log2 = 93.86313
preprocessing = A_C + A_S + DEV + PRE/C = 2^78.08755
```

| change | log2 T |
|---|---|
| as claimed | 93.86312 |
| q3 lower by 0.25 / 0.5 / 1 bit | 94.11312 / 94.36311 / 94.86311 |
| q3 = 2^-102 (the paper's text count of 102 conditions) | 94.81311 |
| A_C = 2^84 | 93.86465 |
| the published S alone with bit-sliced first blocks (the earlier filings, for comparison) | 100.06593 (20dbd783) |

## 12. Premises

**H1 - uniform independent chaining values (score-critical).** First blocks are fresh uniform 512-bit strings; their
chaining values behave as independent uniform 256-bit values. Used for Lemma 5.1 (exact p7 and the law of the
second-block words, per variant), the expected counts and the independence across first blocks. Evidence: 2^16 + 2^23
real first blocks through the attack's own filters (Section 13.1): passing classes 35,932,046 against 35,913,728
expected, good pairs 1.0005 x expected, stage-3a passes z = +0.05, row-16 passes 994 against 1028.0 (z = -1.06);
the organizer experiment `a0-online-r38`. Limitations: tested on 2^23 first blocks, not 2^86.

**H2 - Step-3 probability of the variants (score-critical).** 2^-101.05 = q3_model <= q3 <= 2^-97. Evidence: Lemma 7.1,
the preregistered SMC (Section 7.3; Student and bootstrap bounds agree; all 32 replicates at least 2^-101.19), the
paired comparison of rows 23..37, agreement with the earlier filings' published-S estimate 2^-101.02, the exact
row-16 and stage-3a rates of real good pairs, and 38-step semi-free-start collisions built with variant dense parts
(Section 13.2; organizer experiment `a0-sfs-r38`). Limitations: a Monte-Carlo bound whose coverage rests on the
approximate normality of the mean of 32 replicates; the `+` reading and the W25 correction.

**H3 - few further successes per first block (score-critical, weak).** For every trial t, E[X_f - 1 | A_t] <= 2^-9.4.
With |L* | = 1 the only other trials of a first block are other variants. With q3 <= 2^-97 (H2), the expected number of
further successes is at most rho x 245,760 x q3 <= rho x 2^-79.09, where rho bounds Pr[t' succeeds | t succeeds, t'
good] / Pr[t' succeeds | t' good]; the premise is rho <= 2^69, i.e. at most 2^-10.1. Measured: among 2^23 real first
blocks, no first block had two row-16 passes (0.52 expected under independence); in our r37 filing the same
measurement over 2^23 first blocks gave a row-16 correlation factor of 1.001. Limitations: rows >= 17 of distinct good
pairs cannot be observed jointly within a first block; the premise allows 2^69.

**H4 - advice allowances (supporting).** The published characteristic, its two-bit conditions, S and L* are advice,
charged A_S = 2^74 (2^35.7 times the paper's reported Step-1 cost of 2^38.3; the completion of a Step-1 solution to a
38-step SFS pair is reproduced here in about a second per pair) and A_C = 2^78 for the unpublished characteristic
search: at the solver CPU-second price calibrated in the promoted filing 6eeefb64 (2^32.796 operations, 2^21.38 units
at C = 2728), 2^78 units are 2^56.6 CPU-seconds, about 3 x 10^9 CPU-years, 2^37 times the 593,858 CPU-seconds that
filing measured for a complete re-run of the predecessor [LLWS26] characteristic search. DEV = 2^64 covers all our
development (below 10^5 CPU-seconds). These allowances are below 2^-15.8 of T: A_C = 2^84 gives 93.86465.

Not used: expected work, an independence-of-conditions model for q3, packed or bit-sliced pricing.

## 13. Evidence and runs

### 13.1 End to end on real first blocks (`e2e38.c`, Appendix A)

Random M0, CV1 = F_38(IV, M0), the 64 W7 tests, E16x for every variant of every passing class, stage 3a and the exact
row-16 set; every row-16 pass checked exactly (Lemma 4.1 words, the W7 filter, E16x, every cell of rows -4..16 and the
two-bit conditions closing at rows 8..16).

| run | first blocks | passing classes (expected) | good pairs (ratio) | stage-3a passes (z) | row-16 passes (expected; z) | exact checks |
|---|---|---|---|---|---|---|
| seed 7 | 2^16 | 281,412 (280,576) | 1,080,622,080 (1.0030) | 1,055,591 (+0.29) | 10 (8.05; +0.69) | 10, 0 failures |
| seed 3 | 2^23 | 35,932,046 (35,913,728) | 137,979,056,640 (1.0005) | 134,745,727 (+0.05) | 994 (1028.02; -1.06) | 994, 0 failures |

### 13.2 Semi-free-start collisions with variant dense parts (`sfs38.c`, organizer experiment `a0-sfs-r38`)

For a random variant of G (or of a selected class) and the l of L*: row 16 from the 32-word set, rows 17..21 sampled,
then (W6, W7) and rows 22..37 with the variant's W8; W0..W5 by the inverse expansion and CV1 by inverting steps 7..0.
Every pair is checked: Lemma 4.1 maps (CV1, a0) back to W0..W13, the two 38-step outputs are equal, the blocks differ,
every cell of rows -4..37 (W7's XOR cell excepted) and every two-bit condition of rows >= 8 holds. Development: 7 pairs
(seeds 2, 5) verified with the repository's `_compress` at 38 steps (W8x 24ea4609, 5df2a5c0, 3c726650, d5568056,
b678732c, ff7b7184, cfe64457, none equal to the published 3f416758). Organizer-seed emulation of `a0-sfs-r38` (public seed, no holdout nonce): 12 of 12 trials
returned a pair, all verified with the repository verifier; 2.1 s; stdout SHA-256 0f92c0a3..., byte-identical on rerun.

### 13.3 Organizer experiments (`experiments/a0core38.py`)

- `a0-sfs-r38` (H2): trials 0..11 build 38-step semi-free-start collisions as in 13.2 with seed-chosen class and
  variant (rows 17..21 by proposals with the row's fixed x-bits imposed, restarting after 2^12 proposals; W23
  proposals with its x-cells and two-bit conditions imposed, W7 = W23 - s1(W21) - W16 - s0(W8) accepted iff in F7). It
  returns CV1 || M1, CV1 || M1' (96 bytes each) iff every check passes. They are semi-free-start collisions, not
  collisions from the IV.
- `a0-online-r38` (H1, H3): trials 0..5 run the counted online program on seed-drawn first blocks until a passing class
  (at most 16 first blocks), process one passing class (3840 good pairs), check every good pair against the Step-2
  equations and 8 of them against every cell of rows -4..15, and return the complete 128-byte messages M0 || M1,
  M0 || M1' of the first good pair. Public-seed emulation: 0 mismatches in all 6 trials, 6 pairs returned (not expected
  to collide); 3.1 s; stdout SHA-256 e2d870de..., byte-identical on rerun.

### 13.4 Development computation

Below 10^5 CPU-seconds in total (the preregistered SMC, the end-to-end runs, enumerations and checks), far inside
DEV = 2^64.

## 14. Memory and advice

The F7 bitmap and the row-16 bitmap (2^29 bytes each), the variant data (245,760 x (a0, S0(a0)), one 32-byte word each:
15.7 MB), the 2^16-entry tables and the program: below 1.09 x 10^9 bytes = 2^30.03; claimed 2^30.1. Nonuniform advice:
the characteristic, S, L*, the row-16 set and the 64 class descriptors (below 2^13 bytes), charged through A_C and A_S.

## 15. Limitations

- H1, H2, H3 are premises; q3 is estimated (Monte Carlo); no collision has been found and none is expected at our scale.
- The published characteristic and SFS pair are advice under allowances; we did not rerun the paper's searches.
- The single element of L* is the published one; the paper's stated 2^2 freedom is not reproduced for S (as in the
  earlier filings). With q3 = 2^-102 (the paper's text count), log2 T would be 94.81311.


## Appendix A. Local evidence programs and records

The C programs (C99 + pthreads, `cc -O3`) that produced the local evidence of Sections 4, 7 and 13, and the records of
the preregistered estimate and of the end-to-end runs. They are evidence for the reader, not part of the attack. The
attack's counted program, the class data and the organizer experiments are `experiments/a0core38.py`
(standard-library Python; `python3 a0core38.py ledger` prints Section 11's numbers). SHA-256 of each block in its header.

### A.1 `lab38.h` (13008 bytes, SHA-256 0d18ec729541e131d0842e3d23cdc87dd74fde7411f8eb7369d78e090e474eee)

```c
/* lab38.h - 38-step SHA-256, the ePrint 2026/1120 38-step characteristic (Tables 3-5), S, L*, and the A0 variant family. */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
typedef uint32_t u32; typedef uint64_t u64;
#define NR 38
static const u32 K[64] = {0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,
 0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,
 0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,
 0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,
 0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,
 0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,
 0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,
 0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2};
static const u32 IV0[8] = {0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19};
static inline u32 ror(u32 x, int n) { return (x >> n) | (x << (32 - n)); }
static inline u32 S0(u32 x) { return ror(x,2) ^ ror(x,13) ^ ror(x,22); }
static inline u32 S1(u32 x) { return ror(x,6) ^ ror(x,11) ^ ror(x,25); }
static inline u32 s0(u32 x) { return ror(x,7) ^ ror(x,18) ^ (x >> 3); }
static inline u32 s1(u32 x) { return ror(x,17) ^ ror(x,19) ^ (x >> 10); }
static inline u32 CH(u32 x, u32 y, u32 z) { return (x & y) ^ (~x & z); }
static inline u32 MAJ(u32 x, u32 y, u32 z) { return (x & y) ^ (x & z) ^ (y & z); }

/* state arrays indexed i+4 for i = -4..36 */
#define O 4
typedef struct { u32 A[NR+O], E[NR+O], W[NR]; } Tr;
static void expand(u32 *W, int n) { for (int i = 16; i < n; i++) W[i] = s1(W[i-2]) + W[i-7] + s0(W[i-15]) + W[i-16]; }
static void trace(const u32 cv[8], const u32 w16[16], Tr *t) {
  for (int j = 0; j < 4; j++) { t->A[O-1-j] = cv[j]; t->E[O-1-j] = cv[4+j]; }
  memcpy(t->W, w16, 64); expand(t->W, NR);
  for (int i = 0; i < NR; i++) {
    u32 *A = t->A + O, *E = t->E + O;
    E[i] = A[i-4] + E[i-4] + S1(E[i-1]) + CH(E[i-1], E[i-2], E[i-3]) + K[i] + t->W[i];
    A[i] = E[i] - A[i-4] + S0(A[i-1]) + MAJ(A[i-1], A[i-2], A[i-3]);
  }
}
static void compress(const u32 cv[8], const u32 w16[16], u32 out[8]) {
  Tr t; trace(cv, w16, &t); u32 *A = t.A + O, *E = t.E + O;
  u32 o[8] = {A[NR-1], A[NR-2], A[NR-3], A[NR-4], E[NR-1], E[NR-2], E[NR-3], E[NR-4]};
  for (int j = 0; j < 8; j++) out[j] = cv[j] + o[j];
}

/* ---- characteristic: x = the message printed second ---- */
typedef struct { u32 m, v, d, p; } Cell;
static Cell CA[NR+O], CE[NR+O], CW[NR];
static void mkcell(Cell *c, const char *s) {
  c->m = c->v = c->d = c->p = 0;
  for (int k = 0; k < 32; k++) { int b = 31 - k; char y = s[k];
    if (y=='0'||y=='1'||y=='u'||y=='n') c->m |= 1u << b;
    if (y=='1'||y=='u') c->v |= 1u << b;
    if (y=='u'||y=='n') c->d |= 1u << b;
    if (y=='+') c->p |= 1u << b; }
}
typedef struct { char k1; int i1, b1; char op; char k2; int i2, b2; } X2c;
static const X2c X2[] = {{'A',14,15,'=','A',16,15},{'A',14,23,'=','A',16,23},{'A',14,25,'=','A',16,25},{'A',15,4,'=','A',16,4},
 {'A',15,7,'=','A',16,7},{'A',15,16,'!','A',16,16},{'A',15,17,'=','A',16,17},{'A',15,27,'=','A',16,27},{'A',15,29,'=','A',16,29},
 {'A',16,15,'=','A',17,15},{'A',16,23,'=','A',17,23},{'A',16,25,'=','A',17,25},{'A',17,9,'=','A',17,20},
 {'A',17,6,'=','A',17,18},{'A',17,8,'=','A',17,17},{'A',16,29,'=','A',18,29},{'A',18,29,'=','A',19,29},
 {'E',16,4,'!','E',16,23},{'E',16,3,'!','E',16,8},{'E',16,14,'=','E',16,28},{'E',16,4,'=','E',17,4},{'E',16,18,'=','E',17,18},
 {'E',18,0,'!','E',18,13},{'E',17,15,'=','E',18,15},{'E',17,24,'=','E',18,24},{'E',19,6,'!','E',19,19},{'E',19,20,'=','E',19,2},
 {'E',21,2,'=','E',21,16},
 {'W',7,8,'!','W',7,25},{'W',7,14,'!','W',7,18},{'W',7,1,'=','W',7,12},
 {'W',8,0,'!','W',8,28},{'W',8,30,'!','W',8,9},{'W',8,1,'=','W',8,18},
 {'W',16,1,'!','W',16,12},{'W',16,20,'!','W',16,27},{'W',16,8,'=','W',16,25},{'W',16,14,'=','W',16,18},{'W',16,4,'!','W',16,6},{'W',16,22,'!','W',16,31},
 {'W',23,0,'!','W',23,30},{'W',23,1,'!','W',23,31},{'W',23,14,'=','W',23,21},{'W',23,16,'=','W',23,25},
 {'W',25,4,'=','W',25,6},{'W',25,22,'=','W',25,31},{'W',25,20,'=','W',25,27}};   /* W25[4] = W25[6]: printed W25[9] (misprint) */
#define NX2 ((int)(sizeof(X2)/sizeof(X2[0])))
static void init_char(void) {
  const char *EQ = "================================";
  for (int i = -4; i < NR; i++) { mkcell(&CA[i+O], EQ); mkcell(&CE[i+O], EQ); }
  for (int i = 0; i < NR; i++) mkcell(&CW[i], EQ);
  struct { int i; const char *s; } a[] = {{7,"=nu============================="},{8,"=========n=====n====n======u===="},
   {11,"====================u=======un=="},{12,"=u===n====n======u===nu=======n="},{13,"==n============n================"},
   {14,"====u=========nn========u==u===="},{15,"======n=u=======n==============="},{17,"==u============================="}};
  struct { int i; const char *s; } e[] = {{5,"+++============================="},{6,"+++=1====0==+1=====0+===1==1===="},
   {7,"uuu=0+1=11=0+00====1+===0==00=01"},{8,"100=u+010n=1nu01=01nu=00n11u1=01"},{9,"11000u1=n11u0000101101110=01u0uu"},
   {10,"==1010=01u00001u=010u=101==10111"},{11,"1=n000=0111100101unn00011+111u10"},{12,"01nuuu=110n111nu000100100+010u1n"},
   {13,"00110101110=000u00111nuu+nnnu1n1"},{14,"=010n0===00===1n=11+0100+1110001"},{15,"=1==1=1==0=1==11===+u011n1011=1="},
   {16,"=u==10===n===+u1===n0=u=1==+===="},{17,"=0=====+00===+0=+==01=0=0==+===="},{18,"=0=====+01===n1=+==1==1===0u===="},
   {19,"==11===nn====1==n===010===11==0="},{20,"==1====00====1==0==========1===="},{21,"==u====10=======1===10=========="},
   {22,"==0============================="},{23,"==1============================="}};
  struct { int i; const char *s; } w[] = {{7,"==n============================="},{8,"=====u===u==========n==========="},
   {9,"==u============================="},{10,"=====n=u=======n===n==n=n=n=u=u="},{11,"============u======u=u=========="},
   {15,"=====u===n==========n==========="},{16,"==u============================="},{23,"=====1=uu=====1=u=1============="},
   {25,"==n============================="}};
  for (unsigned k = 0; k < sizeof a/sizeof a[0]; k++) mkcell(&CA[a[k].i+O], a[k].s);
  for (unsigned k = 0; k < sizeof e/sizeof e[0]; k++) mkcell(&CE[e[k].i+O], e[k].s);
  for (unsigned k = 0; k < sizeof w/sizeof w[0]; k++) mkcell(&CW[w[k].i], w[k].s);
}
/* row i of both members: cells of A, E ('+' with row i-1), W (unless skipW) */
static inline int row_ok(const Tr *x, const Tr *y, int i, int checkW) {
  const Cell *c = &CA[i+O]; u32 ax = x->A[i+O], ay = y->A[i+O];
  if ((ax & c->m) != c->v || (ax ^ ay) != c->d) return 0;
  c = &CE[i+O]; u32 ex = x->E[i+O], ey = y->E[i+O];
  if ((ex & c->m) != c->v || (ex ^ ey) != c->d) return 0;
  if (i > -4) { u32 q = c->p & CE[i-1+O].p; if (q && ((ex ^ x->E[i-1+O]) & q)) return 0; }
  if (checkW && i >= 0) { c = &CW[i]; u32 wx = x->W[i], wy = y->W[i];
    if ((wx & c->m) != c->v || (wx ^ wy) != c->d) return 0; }
  return 1;
}
static inline u32 wordof(const Tr *x, char k, int i) { return k=='A' ? x->A[i+O] : k=='E' ? x->E[i+O] : x->W[i]; }
/* two-bit conditions whose later row is exactly r (member x) */
static inline int x2_row_ok(const Tr *x, int r) {
  for (int j = 0; j < NX2; j++) { const X2c *c = &X2[j]; int lr = c->i1 > c->i2 ? c->i1 : c->i2; if (lr != r) continue;
    int a = (wordof(x, c->k1, c->i1) >> c->b1) & 1, b = (wordof(x, c->k2, c->i2) >> c->b2) & 1;
    if ((c->op == '=') != (a == b)) return 0; }
  return 1;
}

/* ---- the published SFS pair and S ---- */
static const u32 CV0[8] = {0xcd278980,0x1b12a052,0xb87cc8a6,0xa9e059c5,0xc9c3db85,0x6ca4b5b5,0x63d13ac1,0xc0329f1e};
static const u32 MY[16] = {0x48fc271b,0x9fca20cd,0xcc89f96f,0xfc40396f,0x8b328cb4,0x6b91ef78,0x97f9b767,0xe2450045,
 0x3b016f58,0xde9804cb,0x66a99ea5,0x0ce30b8d,0xa28cd15a,0x77a1e994,0xd28e48a0,0x9b5f6dbb};
static const u32 MX[16] = {0x48fc271b,0x9fca20cd,0xcc89f96f,0xfc40396f,0x8b328cb4,0x6b91ef78,0x97f9b767,0xc2450045,
 0x3f416758,0xfe9804cb,0x63a88c0f,0x0ceb1f8d,0xa28cd15a,0x77a1e994,0xd28e48a0,0x9f1f65bb};
static const u32 HASH0[8] = {0x5d9ca5f4,0x59ace3a3,0x26c9c26c,0x4252c585,0x4c0803b7,0x1b4d5ccd,0x25c3ccc0,0x90645c4d};
#define NL 1
static const u32 LW14X[NL] = {0xd28e48a0}, LW15X[NL] = {0x9f1f65bb}, LW14Y[NL] = {0xd28e48a0}, LW15Y[NL] = {0x9b5f6dbb};
static Tr PX, PY;                     /* traces of the published pair (x, y) */
static u32 SAx[14], SAy[14];          /* A0..A13 of S */
#define D6 0x00000000u
#define T6 0x00000000u
#define D7 0x20000000u
#define T7 0x03bff800u
static u32 D8, T8;                    /* from S */
static inline int inF(u32 w, u32 d, u32 t) { return (u32)(s0(w + d) - s0(w)) == t; }
static u32 C4, W8C;                   /* E4 = a0 + C4; W8x = W8C - E4 */
static void init_S(void) {
  init_char(); trace(CV0, MX, &PX); trace(CV0, MY, &PY);
  for (int i = 0; i < 14; i++) { SAx[i] = PX.A[i+O]; SAy[i] = PY.A[i+O]; }
  C4 = SAx[4] - S0(SAx[3]) - MAJ(SAx[3], SAx[2], SAx[1]);
  const u32 *E = PX.E + O;
  W8C = E[8] - SAx[4] - S1(E[7]) - CH(E[7], E[6], E[5]) - K[8];
  D8 = PY.W[8] - PX.W[8]; T8 = s0(PY.W[8]) - s0(PX.W[8]);
}
/* variant family G (38 steps; E4 has no cell): W8x = W8C - E4 with W8y = W8x + D8 must follow the W8 cell (x-values at
   its u/n bits, XOR difference exactly there) and the printed W8 two-bit conditions W8[0] != W8[28], W8[30] != W8[9],
   W8[1] = W8[18] (they fix the signed difference of s0(W8), hence s0(W8y) - s0(W8x) = T8). */
static inline int inG(u32 a0) {
  u32 e4 = a0 + C4, w = W8C - e4, y = w + D8;
  const Cell *c = &CW[8];
  if ((w & c->m) != c->v || (w ^ y) != c->d) return 0;
  if (!(((w >> 0) ^ (w >> 28)) & 1)) return 0;
  if (!(((w >> 30) ^ (w >> 9)) & 1)) return 0;
  if (((w >> 1) ^ (w >> 18)) & 1) return 0;
  return 1;
}
/* second-block words W0..W13 of both members for chaining value cv and variant a0 (Lemma-1 equations) */
static void words_from_cv(const u32 cv[8], u32 a0, u32 wx[16], u32 wy[16]) {
  for (int mem = 0; mem < 2; mem++) {
    const u32 *SA = mem ? SAy : SAx; u32 *w = mem ? wy : wx;
    u32 Ab[18], Eb[18], *A = Ab + 4, *E = Eb + 4;
    for (int j = 0; j < 4; j++) { A[-1-j] = cv[j]; E[-1-j] = cv[4+j]; }
    for (int i = 0; i < 14; i++) A[i] = SA[i];
    A[0] = a0;
    for (int i = 0; i < 14; i++) E[i] = A[i] + A[i-4] - S0(A[i-1]) - MAJ(A[i-1], A[i-2], A[i-3]);
    for (int i = 0; i < 14; i++) w[i] = E[i] - A[i-4] - E[i-4] - S1(E[i-1]) - CH(E[i-1], E[i-2], E[i-3]) - K[i];
  }
}
/* xorshift-based PRNG (lab use only) */
typedef struct { u64 s[4]; } Rng;
static inline u64 rotl64(u64 x, int k) { return (x << k) | (x >> (64 - k)); }
static inline u64 rnext(Rng *r) { u64 *s = r->s, res = rotl64(s[1] * 5, 7) * 9, t = s[1] << 17;
  s[2] ^= s[0]; s[3] ^= s[1]; s[1] ^= s[2]; s[0] ^= s[3]; s[2] ^= t; s[3] = rotl64(s[3], 45); return res; }
static void rseed(Rng *r, u64 seed) { for (int i = 0; i < 4; i++) { seed += 0x9e3779b97f4a7c15ULL; u64 z = seed;
  z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9ULL; z = (z ^ (z >> 27)) * 0x94d049bb133111ebULL; r->s[i] = z ^ (z >> 31); } }
static inline u32 r32(Rng *r) { return (u32)(rnext(r) >> 32); }
static inline double runif(Rng *r) { return (rnext(r) >> 11) * (1.0 / 9007199254740992.0); }

/* ---- the 64 selected classes: G grouped by c7 (W7x = c7 - A_{-1}); the 64 largest, ties by smaller c7 ---- */
static inline u32 c7of(u32 a0) { const u32 *A = SAx; const u32 *E = PX.E + O; u32 e4 = a0 + C4;
  u32 E3k = A[3] - S0(A[2]) - MAJ(A[2], A[1], a0); return E[7] - A[3] - E3k - S1(E[6]) - CH(E[6], E[5], e4) - K[7]; }
typedef struct { u32 c7, a0; } CP;
typedef struct { u32 c7, start, n; } CL;
static int cmpCP(const void *a, const void *b) { const CP *x = a, *y = b; return x->c7 != y->c7 ? (x->c7 < y->c7 ? -1 : 1) : (x->a0 < y->a0 ? -1 : x->a0 > y->a0); }
static int cmpCL(const void *a, const void *b) { const CL *x = a, *y = b; return x->n != y->n ? (x->n > y->n ? -1 : 1) : (x->c7 < y->c7 ? -1 : 1); }
/* fills sel[] (class-major a0 list) and cls[0..k-1]; returns total */
static u32 select_classes(int k, CL *outc, u32 **sel) {
  u32 cap = 0; for (u64 a = 0; a < (1ull << 32); a++) cap += inG((u32)a);
  CP *v = malloc(sizeof(CP) * (size_t)cap); u32 n = 0;
  for (u64 a = 0; a < (1ull << 32); a++) if (inG((u32)a)) { v[n].a0 = (u32)a; v[n].c7 = c7of((u32)a); n++; }
  qsort(v, n, sizeof(CP), cmpCP);
  CL *cl = malloc(sizeof(CL) * (size_t)(n + 1)); u32 nc = 0;
  for (u32 i = 0; i < n; ) { u32 j = i; while (j < n && v[j].c7 == v[i].c7) j++; cl[nc].c7 = v[i].c7; cl[nc].start = i; cl[nc].n = j - i; nc++; i = j; }
  qsort(cl, nc, sizeof(CL), cmpCL);
  u32 tot = 0; for (int c = 0; c < k; c++) tot += cl[c].n;
  *sel = malloc(4 * tot); u32 q = 0;
  for (int c = 0; c < k; c++) { outc[c] = cl[c]; outc[c].start = q; for (u32 i = 0; i < cl[c].n; i++) (*sel)[q++] = v[cl[c].start + i].a0; }
  free(v); free(cl); return tot;
}
```

### A.2 `smc38.c` (7542 bytes, SHA-256 091287912229d9fd6f314deb5052f128f43795a0abd9f13feea661cc6c0b94af)

```c
/* smc38.c (38 steps) - sequential Monte-Carlo estimate of q3 = avg over l in L* of Pr[rows 16..36 follow every cell and the
   printed two-bit conditions], for the A0 variant family: W16..W21 iid uniform, (W6, W7) uniform on F6 x F7, and
   W8 = W8C - E4(a0) with a0 uniform on G.  Stages: row 16 (exact enumeration), rows 17..21 (proposal: E_t^x uniform
   with its fixed x-bits, exact weight 2^-f), row 22 (proposal (W6, W7) from F6 x F7), rows 23..36 (W8 from a uniform
   variant).  The stage-23 children are also evaluated with the published W8 (paired comparison).
   usage: smc <seed> <NP> <M> <MT>   (one replicate; prints the stage means and the estimate) */
#include "lab38.h"
#include <pthread.h>

static Tr T0x[NL], T0y[NL];          /* rows <= 15 for each l */
static u32 dW16[NL];
static u32 *P16[NL]; static u32 C16[NL];
static u32 *Glist; static u32 Gn;

static void step_rows(Tr *x, Tr *y, int t) {
  for (int m = 0; m < 2; m++) { Tr *s = m ? y : x; u32 *A = s->A + O, *E = s->E + O;
    E[t] = A[t-4] + E[t-4] + S1(E[t-1]) + CH(E[t-1], E[t-2], E[t-3]) + K[t] + s->W[t];
    A[t] = E[t] - A[t-4] + S0(A[t-1]) + MAJ(A[t-1], A[t-2], A[t-3]); }
}
static void setup(void) {
  init_S();
  for (int l = 0; l < NL; l++) {
    u32 wx[16], wy[16]; memcpy(wx, MX, 64); memcpy(wy, MY, 64);
    wx[14] = LW14X[l]; wx[15] = LW15X[l]; wy[14] = LW14Y[l]; wy[15] = LW15Y[l];
    trace(CV0, wx, &T0x[l]); trace(CV0, wy, &T0y[l]);
    for (int i = -4; i < 16; i++) if (!row_ok(&T0x[l], &T0y[l], i, i != 6 && i != 7)) { fprintf(stderr, "l %d row %d\n", l, i); exit(1); }
    Tr *x = &T0x[l], *y = &T0y[l];
    dW16[l] = (s1(y->W[14]) - s1(x->W[14])) + (y->W[9] - x->W[9]);
    /* row 16 exact: E16x over all words with the fixed x-bits of E16 */
    Cell *c = &CE[16+O]; u32 fr = ~c->m, e = 0, cnt = 0; u32 cap = 1u << 22; P16[l] = malloc(4u * cap);
    u32 base = x->A[12+O] + x->E[12+O] + S1(x->E[15+O]) + CH(x->E[15+O], x->E[14+O], x->E[13+O]) + K[16];
    do {
      u32 E16 = e | c->v; Tr X = *x, Y = *y;
      X.W[16] = E16 - base; Y.W[16] = X.W[16] + dW16[l]; step_rows(&X, &Y, 16);
      if (row_ok(&X, &Y, 16, 1) && x2_row_ok(&X, 16)) P16[l][cnt++] = X.W[16];
      e = (e - fr) & fr;
    } while (e);
    C16[l] = cnt;
  }
  if (getenv("SMC_ALLG")) { Glist = malloc(4u * 12200000u); Gn = 0;
    for (u64 a = 0; a < (1ull << 32); a++) if (inG((u32)a)) Glist[Gn++] = (u32)a; }
  else { static CL cc[64]; Gn = select_classes(64, cc, &Glist); }
}

typedef struct { Tr x, y; } Part;
static int NP, M, MT;

static void one(u64 seed, double out[16]) {
  Rng rg; rseed(&rg, seed);
  Part *P = malloc(sizeof(Part) * NP), *Q = malloc(sizeof(Part) * NP);
  int *L = malloc(sizeof(int) * NP), *L2 = malloc(sizeof(int) * NP);
  /* stage 16 */
  u64 tot = 0; for (int l = 0; l < NL; l++) tot += C16[l];
  double z16 = (double)tot / NL / 4294967296.0; out[0] = z16;
  for (int p = 0; p < NP; p++) {
    u64 r = rnext(&rg) % tot; int l = 0; while (r >= C16[l]) r -= C16[l++];
    P[p].x = T0x[l]; P[p].y = T0y[l]; L[p] = l;
    P[p].x.W[16] = P16[l][r]; P[p].y.W[16] = P16[l][r] + dW16[l]; step_rows(&P[p].x, &P[p].y, 16);
  }
  /* stages 17..21 */
  Part *ch = malloc(sizeof(Part) * (size_t)NP * 8); int *chl = malloc(sizeof(int) * (size_t)NP * 8); size_t chcap = (size_t)NP * 8;
  for (int t = 17; t < 22; t++) {
    Cell *c = &CE[t+O]; int f = __builtin_popcount(c->m); double w = ldexp(1.0, -f);
    u64 pass = 0; size_t nch = 0;
    for (int p = 0; p < NP; p++) {
      Tr *x = &P[p].x, *y = &P[p].y; int l = L[p];
      u32 dW = (u32)(s1(y->W[t-2]) - s1(x->W[t-2])) + (u32)(y->W[t-7] - x->W[t-7]) + (t == 21 ? T6 : 0);
      u32 base = x->A[t-4+O] + x->E[t-4+O] + S1(x->E[t-1+O]) + CH(x->E[t-1+O], x->E[t-2+O], x->E[t-3+O]) + K[t];
      for (int k = 0; k < M; k++) {
        u32 E = (r32(&rg) & ~c->m) | c->v;
        Part C = P[p]; C.x.W[t] = E - base; C.y.W[t] = C.x.W[t] + dW; step_rows(&C.x, &C.y, t);
        if (row_ok(&C.x, &C.y, t, 1) && x2_row_ok(&C.x, t)) {
          pass++;
          if (nch == chcap) { chcap *= 2; ch = realloc(ch, sizeof(Part) * chcap); chl = realloc(chl, sizeof(int) * chcap); }
          ch[nch] = C; chl[nch] = l; nch++;
        }
      }
    }
    out[t-16] = w * (double)pass / ((double)NP * M);
    if (!nch) { for (int j = t-15; j < 9; j++) out[j] = 0; free(P); free(Q); free(L); free(L2); free(ch); free(chl); return; }
    for (int p = 0; p < NP; p++) { size_t j = rnext(&rg) % nch; Q[p] = ch[j]; L2[p] = chl[j]; }
    Part *tp = P; P = Q; Q = tp; int *tl = L; L = L2; L2 = tl;
  }
  /* stage 22: (W6, W7) uniform on F6 x F7; stage 23: rows 23..36 with a uniform variant's W8 (and, paired, the
     published W8) */
  u64 p22 = 0, p23v = 0, p23p = 0, both = 0;
  for (int p = 0; p < NP; p++) {
    for (int k = 0; k < MT; k++) {
      Part C = P[p]; u32 w7, w6;
      do w7 = r32(&rg); while (!inF(w7, D7, T7)); w6 = r32(&rg);      /* 38 steps: W6 has no difference, F6 = all words */
      C.x.W[6] = w6; C.y.W[6] = w6 + D6; C.x.W[7] = w7; C.y.W[7] = w7 + D7;
      for (int m = 0; m < 2; m++) { Tr *s = m ? &C.y : &C.x; s->W[22] = s1(s->W[20]) + s->W[15] + s0(s->W[7]) + s->W[6]; }
      step_rows(&C.x, &C.y, 22);
      if (!(row_ok(&C.x, &C.y, 22, 1) && x2_row_ok(&C.x, 22))) continue;
      p22++;
      int okv[2];
      for (int which = 0; which < 2; which++) {
        Part D = C;
        u32 w8x = which ? PX.W[8] : (W8C - (Glist[rnext(&rg) % Gn] + C4));   /* W8y = W8x + D8 */
        D.x.W[8] = w8x; D.y.W[8] = w8x + D8;
        int ok = 1;
        for (int t = 23; t < NR && ok; t++) {
          for (int m = 0; m < 2; m++) { Tr *s = m ? &D.y : &D.x; s->W[t] = s1(s->W[t-2]) + s->W[t-7] + s0(s->W[t-15]) + s->W[t-16]; }
          step_rows(&D.x, &D.y, t);
          ok = row_ok(&D.x, &D.y, t, 1) && x2_row_ok(&D.x, t);
        }
        okv[which] = ok;
      }
      p23v += okv[0]; p23p += okv[1]; both += okv[0] & okv[1];
    }
  }
  out[6] = (double)p22 / ((double)NP * MT);
  out[7] = p22 ? (double)p23v / p22 : 0;    /* variant W8 */
  out[8] = p22 ? (double)p23p / p22 : 0;    /* published W8 (paired) */
  out[9] = (double)p22; out[10] = (double)p23v; out[11] = (double)p23p; out[12] = (double)both;
  free(P); free(Q); free(L); free(L2); free(ch); free(chl);
}

typedef struct { u64 seed; double out[16]; } Job;
static void *run(void *a) { Job *j = a; one(j->seed, j->out); return 0; }

int main(int argc, char **argv) {
  u64 seed = argc > 1 ? strtoull(argv[1], 0, 10) : 1; NP = argc > 2 ? atoi(argv[2]) : 1024;
  M = argc > 3 ? atoi(argv[3]) : 256; MT = argc > 4 ? atoi(argv[4]) : 4096; int nt = argc > 5 ? atoi(argv[5]) : 8;
  setup();
  u64 tot = 0; for (int l = 0; l < NL; l++) tot += C16[l];
  printf("row16 words per l:"); for (int l = 0; l < NL; l++) printf(" %u", C16[l]); printf("  total %llu  |G| %u\n", (unsigned long long)tot, Gn);
  pthread_t th[64]; Job jb[64];
  for (int i = 0; i < nt; i++) { jb[i].seed = seed * 1000 + i; pthread_create(&th[i], 0, run, &jb[i]); }
  for (int i = 0; i < nt; i++) pthread_join(th[i], 0);
  for (int i = 0; i < nt; i++) { double *o = jb[i].out, zv = 1, zp;
    for (int s = 0; s < 7; s++) zv *= o[s]; zp = zv * o[8]; zv *= o[7];
    printf("seed %llu stages(log2) 16:%.3f 17:%.3f 18:%.3f 19:%.3f 20:%.3f 21:%.3f 22:%.3f 23v:%.3f 23p:%.3f | q3 variant 2^%.4f published-W8 2^%.4f | n22 %.0f v %.0f p %.0f both %.0f\n",
      (unsigned long long)jb[i].seed, log2(o[0]), log2(o[1]), log2(o[2]), log2(o[3]), log2(o[4]), log2(o[5]), log2(o[6]), log2(o[7]), log2(o[8]),
      log2(zv), log2(zp), o[9], o[10], o[11], o[12]); }
  return 0;
}
```

### A.3 `e2e38.c` (5695 bytes, SHA-256 eb579e81c435ec50edc18565d9020c47a3d23bfb547bf955d2531ab67d0d2f37)

```c
/* e2e38.c - the online phase of the A0-variant attack on 38-step SHA-256, on real first blocks (scaled down):
   random M0, CV = F38(IV, M0), one W7 test per class (64 largest c7 classes of G38); every variant of a passing class
   is a good pair (38 steps have no W6 filter); u = W0 + s0(W1), E16x = C16 + u, the ten fixed x-bits of E16 (stage 3a)
   and the exact row-16 set (32 words).  Reports rates against the model, checks every row-16 pass exactly, and
   measures the within-first-block correlation of row-16 passes.
   usage: e2e38 <seed> <log2 first blocks per thread> <threads> */
#include "lab38.h"
#include <pthread.h>

static int KC = 64; static CL cls[64]; static u32 *sel, *vS0, NV;
static u64 *F7bm; static u32 R16v[64], R16n, C16, M16, V16, BASE16, DW16;
static inline int bm(const u64 *b, u32 w) { return (b[w >> 6] >> (w & 63)) & 1; }
static void step_rows(Tr *x, Tr *y, int t) {
  for (int m = 0; m < 2; m++) { Tr *s = m ? y : x; u32 *A = s->A + O, *E = s->E + O;
    E[t] = A[t-4] + E[t-4] + S1(E[t-1]) + CH(E[t-1], E[t-2], E[t-3]) + K[t] + s->W[t];
    A[t] = E[t] - A[t-4] + S0(A[t-1]) + MAJ(A[t-1], A[t-2], A[t-3]); }
}
static void setup(void) {
  init_S(); NV = select_classes(KC, cls, &sel);
  vS0 = malloc(4 * NV); for (u32 i = 0; i < NV; i++) vS0[i] = S0(sel[i]);
  F7bm = calloc(1u << 26, 8);
  for (u64 w = 0; w < (1ull << 32); w++) if (inF((u32)w, D7, T7)) F7bm[w >> 6] |= 1ull << (w & 63);
  u32 wx[16], wy[16]; memcpy(wx, MX, 64); memcpy(wy, MY, 64);
  Tr x, y; trace(CV0, wx, &x); trace(CV0, wy, &y);
  DW16 = (s1(y.W[14]) - s1(x.W[14])) + (y.W[9] - x.W[9]);
  BASE16 = x.A[12+O] + x.E[12+O] + S1(x.E[15+O]) + CH(x.E[15+O], x.E[14+O], x.E[13+O]) + K[16];
  C16 = BASE16 + s1(x.W[14]) + x.W[9];
  Cell *c = &CE[16+O]; M16 = c->m; V16 = c->v; u32 fr = ~c->m, e = 0; R16n = 0;
  do { u32 E16 = e | c->v; Tr X = x, Y = y; X.W[16] = E16 - BASE16; Y.W[16] = X.W[16] + DW16; step_rows(&X, &Y, 16);
    if (row_ok(&X, &Y, 16, 1) && x2_row_ok(&X, 16)) R16v[R16n++] = E16; e = (e - fr) & fr; } while (e);
  fprintf(stderr, "setup: %u selected variants, row-16 set %u words, 3a mask %08x\n", NV, R16n, M16);
}
typedef struct { u64 seed; int lg; u64 fb, hits, good, s3a, r16, chk, chkbad; double gg1, rr1; } Job;
static void *run(void *arg) {
  Job *J = arg; Rng rg; rseed(&rg, J->seed);
  for (u64 f = 0; f < (1ull << J->lg); f++) {
    u32 m0[16], cv[8]; for (int j = 0; j < 16; j++) m0[j] = r32(&rg);
    compress(IV0, m0, cv); J->fb++;
    u32 a = cv[0], Am1 = cv[0], Am2 = cv[1], Am3 = cv[2], Am4 = cv[3], Em1 = cv[4], Em2 = cv[5], Em3 = cv[6], Em4 = cv[7];
    u32 e0b = Am4 - S0(Am1) - MAJ(Am1, Am2, Am3);
    u32 kap0 = e0b - Am4 - Em4 - S1(Em1) - CH(Em1, Em2, Em3) - K[0];
    u32 o12 = Am1 | Am2, n12 = Am1 & Am2, X = Em1 ^ Em2, kap1 = SAx[1] - K[1] - Em3;
    u64 g = 0, r = 0;
    for (int c = 0; c < KC; c++) {
      if (!bm(F7bm, cls[c].c7 - a)) continue;
      J->hits++;
      for (u32 i = cls[c].start; i < cls[c].start + cls[c].n; i++) {
        u32 a0 = sel[i], E0 = a0 + e0b, W0 = a0 + kap0;
        u32 W1 = kap1 - vS0[i] - (n12 | (a0 & o12)) - S1(E0) - ((E0 & X) ^ Em2);
        u32 e16 = C16 + W0 + s0(W1);
        g++;
        if ((e16 & M16) != V16) continue;
        J->s3a++;
        int in = 0; for (u32 k = 0; k < R16n; k++) in |= R16v[k] == e16;
        if (!in) continue;
        J->r16++; r++;
        { u32 wx[16], wy[16]; words_from_cv(cv, a0, wx, wy);
          wx[14] = LW14X[0]; wx[15] = LW15X[0]; wy[14] = LW14Y[0]; wy[15] = LW15Y[0];
          Tr tx, ty; trace(cv, wx, &tx); trace(cv, wy, &ty);
          int ok = inF(wx[7], D7, T7) && wx[7] == (u32)(cls[c].c7 - a) && wx[0] == W0 && wx[1] == W1 && tx.E[16+O] == e16;
          for (int q = -4; q <= 16; q++) ok &= row_ok(&tx, &ty, q, q != 7);
          for (int q = 8; q <= 16; q++) ok &= x2_row_ok(&tx, q);
          J->chk++; J->chkbad += !ok; }
      }
    }
    J->good += g; J->gg1 += (double)g * (g ? g - 1 : 0); J->rr1 += (double)r * (r ? r - 1 : 0);
  }
  return 0;
}
int main(int argc, char **argv) {
  u64 seed = argc > 1 ? strtoull(argv[1], 0, 10) : 1; int lg = argc > 2 ? atoi(argv[2]) : 14, nt = argc > 3 ? atoi(argv[3]) : 8;
  setup();
  Job J[64]; pthread_t th[64]; memset(J, 0, sizeof J);
  for (int i = 0; i < nt; i++) { J[i].seed = seed * 100 + i; J[i].lg = lg; pthread_create(&th[i], 0, run, &J[i]); }
  Job T; memset(&T, 0, sizeof T);
  for (int i = 0; i < nt; i++) { pthread_join(th[i], 0); T.fb += J[i].fb; T.hits += J[i].hits; T.good += J[i].good; T.s3a += J[i].s3a;
    T.r16 += J[i].r16; T.chk += J[i].chk; T.chkbad += J[i].chkbad; T.gg1 += J[i].gg1; T.rr1 += J[i].rr1; }
  double p7 = 287309824.0 / 4294967296.0, eh = T.fb * KC * p7;
  printf("first blocks %llu (2^%.2f), %d classes, %u variants\n", (unsigned long long)T.fb, log2((double)T.fb), KC, NV);
  printf("passing classes %llu, expected %.1f (ratio %.4f)\n", (unsigned long long)T.hits, eh, T.hits / eh);
  printf("good pairs %llu, expected %.1f (ratio %.4f)\n", (unsigned long long)T.good, T.fb * (double)NV * p7, T.good / (T.fb * (double)NV * p7));
  printf("stage-3a passes %llu, expected %.1f (z %+.2f)\n", (unsigned long long)T.s3a, T.good / 1024.0, (T.s3a - T.good / 1024.0) / sqrt(T.good / 1024.0));
  double er = T.good * (double)R16n / 4294967296.0;
  printf("row-16 passes %llu, expected %.2f (z %+.2f); exact checks %llu, failures %llu\n", (unsigned long long)T.r16, er, (T.r16 - er) / sqrt(er),
         (unsigned long long)T.chk, (unsigned long long)T.chkbad);
  double p = (double)T.r16 / T.good;
  printf("within-first-block pairwise correlation of row-16 passes: rho = %.3f (sum R(R-1) %.0f, p^2 sum G(G-1) %.2f)\n", T.rr1 / (p * p * T.gg1), T.rr1, p * p * T.gg1);
  return 0;
}
```

### A.4 `sfs38.c` (5931 bytes, SHA-256 d61e1f9c5421ee340fba3ec41207b3f116af6b5d7dc1ead7e292e3c3d2da7f79)

```c
/* sfs38.c (38 steps) - checks of S and the A0 variant family, and construction of 37-step semi-free-start collisions whose
   second-block state uses a random variant a0 in G (so E4, W8 differ from the published pair).
   usage: sfs <seed> <count>   prints each pair as: SFS a0 cv[8] mx[16] my[16] */
#include "lab38.h"

static void step_rows(Tr *x, Tr *y, int t) {
  for (int m = 0; m < 2; m++) { Tr *s = m ? y : x; u32 *A = s->A + O, *E = s->E + O;
    E[t] = A[t-4] + E[t-4] + S1(E[t-1]) + CH(E[t-1], E[t-2], E[t-3]) + K[t] + s->W[t];
    A[t] = E[t] - A[t-4] + S0(A[t-1]) + MAJ(A[t-1], A[t-2], A[t-3]); }
}
/* invert steps 7..0 of member x from its state rows 4..7 and W0..W7: returns the chaining value */
static void invert_cv(const u32 *A /*A[-4..7] base+4*/, const u32 *E, const u32 *W, u32 cv[8]) {
  u32 Ab[12], Eb[12], *a = Ab + 4, *e = Eb + 4;
  for (int i = 4; i < 8; i++) { a[i] = A[i]; e[i] = E[i]; }
  for (int i = 7; i >= 0; i--) {
    u32 T2 = S0(a[i-1]) + MAJ(a[i-1], a[i-2], a[i-3]);
    u32 T1 = a[i] - T2;
    a[i-4] = e[i] - T1;
    e[i-4] = T1 - S1(e[i-1]) - CH(e[i-1], e[i-2], e[i-3]) - K[i] - W[i];
  }
  for (int j = 0; j < 4; j++) { cv[j] = a[-1-j]; cv[4+j] = e[-1-j]; }
}

int main(int argc, char **argv) {
  u64 seed = argc > 1 ? strtoull(argv[1], 0, 10) : 1; int count = argc > 2 ? atoi(argv[2]) : 1;
  init_S(); Rng rg; rseed(&rg, seed);
  /* 1. the published pair */
  u32 hx[8], hy[8]; compress(CV0, MX, hx); compress(CV0, MY, hy);
  int ok = !memcmp(hx, hy, 32) && !memcmp(hx, HASH0, 32);
  for (int i = -4; i < NR; i++) ok &= row_ok(&PX, &PY, i, 1);
  for (int r = 0; r < NR; r++) ok &= x2_row_ok(&PX, r);
  u32 wx[16], wy[16]; words_from_cv(CV0, SAx[0], wx, wy);
  for (int i = 0; i < 14; i++) ok &= wx[i] == MX[i] && wy[i] == MY[i];
  ok &= inG(SAx[0]) && (u32)(PY.W[8] - PX.W[8]) == D8 && (u32)(s0(PY.W[8]) - s0(PX.W[8])) == T8;
  fprintf(stderr, "published pair, cells, x2, Lemma-1 words, a0 in G: %s\n", ok ? "ok" : "FAIL"); if (!ok) return 1;
  /* 2. exact size of G */
  if (seed == 1) { CL cl[4096]; u32 *sel; u32 tot = select_classes(4096, cl, &sel);
    u64 g = 0; for (u64 a = 0; a < (1ull << 32); a++) g += inG((u32)a);
    fprintf(stderr, "|G| = %llu = 2^%.4f; top-4096 classes hold %u variants\n", (unsigned long long)g, log2((double)g), tot);
    u32 cum = 0; for (int k = 0; k < 4096; k++) { cum += cl[k].n;
      if (k < 4 || k == 15 || k == 63 || k == 127 || k == 255 || k == 1023 || k == 4095) fprintf(stderr, "  top %4d: size %u cumulative %u (2^%.3f)\n", k + 1, cl[k].n, cum, log2((double)cum)); } }
  /* 3. semi-free-start collisions with random variants */
  for (int c = 0; c < count; c++) {
    u32 a0; do a0 = r32(&rg); while (!inG(a0) || a0 == SAx[0]);
    int l = (int)(r32(&rg) % NL);
    words_from_cv(CV0, a0, wx, wy);
    wx[14] = LW14X[l]; wx[15] = LW15X[l]; wy[14] = LW14Y[l]; wy[15] = LW15Y[l];
    Tr x, y; trace(CV0, wx, &x); trace(CV0, wy, &y);      /* rows -4..15 hold for every chaining value (checked below) */
    int bad = 0; for (int i = -4; i < 16; i++) bad |= !row_ok(&x, &y, i, i != 6 && i != 7);
    if (bad) { fprintf(stderr, "rows -4..15 fail for a0 %08x l %d\n", a0, l); return 1; }
    u64 tries[7] = {0}; int t, fail = 0;
    for (t = 16; t < 22 && !fail; t++) {
      u32 dW = (u32)(s1(y.W[t-2]) - s1(x.W[t-2])) + (u32)(y.W[t-7] - x.W[t-7]) + (t == 21 ? T6 : 0);
      for (;;) {
        if (++tries[t-16] > (1ull << 26)) { fail = 1; break; }
        x.W[t] = r32(&rg); y.W[t] = x.W[t] + dW; step_rows(&x, &y, t);
        if (row_ok(&x, &y, t, 1) && x2_row_ok(&x, t)) break;
      }
    }
    if (fail) { c--; continue; }   /* l with an infeasible row 16 (4 of 32): redraw */
    u32 w8x = W8C - (a0 + C4);
    for (;;) {
      tries[6]++;
      u32 w7, w6; do w7 = r32(&rg); while (!inF(w7, D7, T7)); do w6 = r32(&rg); while (!inF(w6, D6, T6));
      x.W[6] = w6; y.W[6] = w6 + D6; x.W[7] = w7; y.W[7] = w7 + D7; x.W[8] = w8x; y.W[8] = w8x + D8;
      int okt = 1;
      for (t = 22; t < NR && okt; t++) {
        for (int m = 0; m < 2; m++) { Tr *s = m ? &y : &x; s->W[t] = s1(s->W[t-2]) + s->W[t-7] + s0(s->W[t-15]) + s->W[t-16]; }
        step_rows(&x, &y, t);
        okt = row_ok(&x, &y, t, 1) && x2_row_ok(&x, t);
      }
      if (okt) break;
    }
    /* rebuild W0..W5 (no member difference) by the inverse expansion, then the chaining value */
    u32 W[16];
    for (int i = 6; i < 16; i++) W[i] = x.W[i];
    W[5] = x.W[21] - s1(x.W[19]) - x.W[14] - s0(W[6]);
    W[4] = x.W[20] - s1(x.W[18]) - x.W[13] - s0(W[5]);
    W[3] = x.W[19] - s1(x.W[17]) - x.W[12] - s0(W[4]);
    W[2] = x.W[18] - s1(x.W[16]) - x.W[11] - s0(W[3]);
    W[1] = x.W[17] - s1(x.W[15]) - x.W[10] - s0(W[2]);
    W[0] = x.W[16] - s1(x.W[14]) - x.W[9] - s0(W[1]);
    u32 cv[8]; invert_cv(x.A + O, x.E + O, W, cv);
    u32 mx[16], my[16]; memcpy(mx, W, 64); memcpy(my, W, 64);
    for (int i = 6; i < 16; i++) my[i] = y.W[i];
    /* checks: Lemma-1 words from cv and a0 are exactly W0..W13; equal outputs; every cell (W6/W7 XOR cells excepted) */
    u32 vx[16], vy[16]; words_from_cv(cv, a0, vx, vy);
    int okc = 1; for (int i = 0; i < 14; i++) okc &= vx[i] == mx[i] && vy[i] == my[i];
    compress(cv, mx, hx); compress(cv, my, hy); okc &= !memcmp(hx, hy, 32) && memcmp(mx, my, 64);
    Tr X, Y; trace(cv, mx, &X); trace(cv, my, &Y);
    for (int i = -4; i < NR; i++) okc &= row_ok(&X, &Y, i, i != 6 && i != 7);
    for (int r = 8; r < NR; r++) okc &= x2_row_ok(&X, r);
    okc &= inF(mx[6], D6, T6) && inF(mx[7], D7, T7) && inG(a0) && mx[8] != MX[8];
    printf("SFS %08x", a0); for (int j = 0; j < 8; j++) printf(" %08x", cv[j]);
    for (int j = 0; j < 16; j++) printf(" %08x", mx[j]); for (int j = 0; j < 16; j++) printf(" %08x", my[j]);
    printf(" l=%d checks=%s tries16..21,tail=", l, okc ? "ok" : "FAIL");
    for (int j = 0; j < 7; j++) printf("%llu%s", (unsigned long long)tries[j], j < 6 ? "," : "\n");
    fflush(stdout);
  }
  return 0;
}
```

### A.5 `PREREG_q3_r38.txt` (1027 bytes, SHA-256 76e76864b5f640830fcf3621a6fca7148d0a9bf986806d3153f82098182c63cf)

```text
q3 SMC preregistration (A0-variant attack, sha256-r38), frozen 2026-10-09T15:55:03Z before any listed seed ran.
program: smc38.c sha256 091287912229d9fd6f314deb5052f128f43795a0abd9f13feea661cc6c0b94af  lab38.h sha256 0d18ec729541e131d0842e3d23cdc87dd74fde7411f8eb7369d78e090e474eee
build: cc -O3 -march=native -o smc38 smc38.c -lm -lpthread
W8 drawn uniformly from the 245,760 variants of the 64 selected classes (64 largest c7-classes of G38, 3840 each; ties by smaller c7).
parameters: NP=2048 M=512 MT=32768, 8 replicates per invocation.
invocations: ./smc38 80 2048 512 32768 8 ; ./smc38 81 ... ; ./smc38 82 ... ; ./smc38 83 ...  -> replicate seeds 80000..80007, 81000..81007, 82000..82007, 83000..83007 (32 replicates).
estimate per replicate: product of stage means (16 exact, 17..21, 22, 23..37 with the variant W8) = 'q3 variant'.
rule: Z_s linear estimates (32); LB = mean - t*sd/sqrt(32), t = 2.4528 (one-sided 99%, 31 df); q3_model = 2^(floor(100*log2(LB))/100).
All 32 replicates are reported; none may be dropped.
```

### A.6 `smc38_80.txt` (1706 bytes, SHA-256 a8ed184811d3fc524233ccdb8d5deb69d0482aaf4241548c7df33ce377e8a510)

```text
row16 words per l: 32  total 32  |G| 245760
seed 80000 stages(log2) 16:-27.000 17:-16.945 18:-12.995 19:-15.000 20:-6.000 21:-7.002 22:-1.000 23v:-15.076 23p:-14.997 | q3 variant 2^-101.0191 published-W8 2^-100.9396 | n22 33550380 v 971 p 1026 both 0
seed 80001 stages(log2) 16:-27.000 17:-17.023 18:-12.993 19:-15.015 20:-6.000 21:-7.000 22:-1.000 23v:-15.020 23p:-14.945 | q3 variant 2^-101.0511 published-W8 2^-100.9759 | n22 33558199 v 1010 p 1064 both 0
seed 80002 stages(log2) 16:-27.000 17:-17.110 18:-13.000 19:-14.960 20:-6.000 21:-6.998 22:-1.000 23v:-14.992 23p:-15.084 | q3 variant 2^-101.0607 published-W8 2^-101.1532 | n22 33555353 v 1030 p 966 both 0
seed 80003 stages(log2) 16:-27.000 17:-17.072 18:-12.992 19:-15.009 20:-6.000 21:-6.998 22:-1.000 23v:-14.945 23p:-14.942 | q3 variant 2^-101.0165 published-W8 2^-101.0138 | n22 33555805 v 1064 p 1066 both 0
seed 80004 stages(log2) 16:-27.000 17:-17.004 18:-12.994 19:-15.029 20:-6.000 21:-6.999 22:-1.000 23v:-14.952 23p:-14.983 | q3 variant 2^-100.9783 published-W8 2^-101.0100 | n22 33554746 v 1059 p 1036 both 0
seed 80005 stages(log2) 16:-27.000 17:-16.970 18:-12.999 19:-15.039 20:-6.000 21:-7.000 22:-1.000 23v:-14.982 23p:-15.023 | q3 variant 2^-100.9893 published-W8 2^-101.0302 | n22 33556958 v 1037 p 1008 both 0
seed 80006 stages(log2) 16:-27.000 17:-16.930 18:-12.996 19:-15.004 20:-6.000 21:-7.000 22:-1.000 23v:-15.007 23p:-15.009 | q3 variant 2^-100.9378 published-W8 2^-100.9392 | n22 33556258 v 1019 p 1018 both 0
seed 80007 stages(log2) 16:-27.000 17:-17.008 18:-12.991 19:-15.008 20:-6.000 21:-7.000 22:-1.000 23v:-15.016 23p:-14.994 | q3 variant 2^-101.0224 published-W8 2^-101.0012 | n22 33553979 v 1013 p 1028 both 0
```

### A.7 `smc38_81.txt` (1700 bytes, SHA-256 ad22cebeaac5b3cf044aff81bf7a2079bb9fde2ee0957f2226fad08c1d73f5d3)

```text
row16 words per l: 32  total 32  |G| 245760
seed 81000 stages(log2) 16:-27.000 17:-16.978 18:-13.002 19:-15.021 20:-6.000 21:-7.001 22:-1.000 23v:-15.041 23p:-15.026 | q3 variant 2^-101.0439 published-W8 2^-101.0280 | n22 33553735 v 995 p 1006 both 0
seed 81001 stages(log2) 16:-27.000 17:-16.980 18:-13.004 19:-14.995 20:-6.000 21:-6.998 22:-1.000 23v:-15.077 23p:-15.027 | q3 variant 2^-101.0538 published-W8 2^-101.0042 | n22 33551760 v 971 p 1005 both 0
seed 81002 stages(log2) 16:-27.000 17:-16.970 18:-13.000 19:-15.010 20:-6.000 21:-6.999 22:-1.000 23v:-14.979 23p:-15.006 | q3 variant 2^-100.9582 published-W8 2^-100.9848 | n22 33560444 v 1039 p 1020 both 0
seed 81003 stages(log2) 16:-27.000 17:-16.968 18:-12.998 19:-15.044 20:-6.000 21:-7.000 22:-1.000 23v:-14.974 23p:-14.956 | q3 variant 2^-100.9831 published-W8 2^-100.9653 | n22 33556224 v 1043 p 1056 both 0
seed 81004 stages(log2) 16:-27.000 17:-16.987 18:-12.992 19:-15.035 20:-6.000 21:-7.002 22:-1.000 23v:-15.080 23p:-15.174 | q3 variant 2^-101.0967 published-W8 2^-101.1905 | n22 33555825 v 969 p 908 both 0
seed 81005 stages(log2) 16:-27.000 17:-17.004 18:-12.997 19:-15.046 20:-6.000 21:-7.003 22:-1.000 23v:-15.037 23p:-15.047 | q3 variant 2^-101.0862 published-W8 2^-101.0963 | n22 33555288 v 998 p 991 both 1
seed 81006 stages(log2) 16:-27.000 17:-17.026 18:-13.000 19:-15.006 20:-6.000 21:-7.001 22:-1.000 23v:-15.050 23p:-15.028 | q3 variant 2^-101.0842 published-W8 2^-101.0624 | n22 33552618 v 989 p 1004 both 0
seed 81007 stages(log2) 16:-27.000 17:-16.953 18:-13.002 19:-14.996 20:-6.000 21:-7.000 22:-1.000 23v:-14.978 23p:-15.087 | q3 variant 2^-100.9281 published-W8 2^-101.0376 | n22 33555953 v 1040 p 964 both 0
```

### A.8 `smc38_82.txt` (1704 bytes, SHA-256 c82d8f5460dbf41cbc63bb8b772b934aed7f31aa2d7c8a257bc22bf838494a74)

```text
row16 words per l: 32  total 32  |G| 245760
seed 82000 stages(log2) 16:-27.000 17:-17.021 18:-12.996 19:-15.028 20:-6.000 21:-6.999 22:-1.000 23v:-14.969 23p:-14.901 | q3 variant 2^-101.0137 published-W8 2^-100.9451 | n22 33555055 v 1046 p 1097 both 0
seed 82001 stages(log2) 16:-27.000 17:-17.033 18:-13.002 19:-14.989 20:-6.000 21:-7.003 22:-1.000 23v:-14.935 23p:-14.884 | q3 variant 2^-100.9622 published-W8 2^-100.9106 | n22 33556835 v 1071 p 1110 both 0
seed 82002 stages(log2) 16:-27.000 17:-17.018 18:-12.997 19:-15.013 20:-6.000 21:-7.003 22:-1.000 23v:-15.096 23p:-15.031 | q3 variant 2^-101.1262 published-W8 2^-101.0614 | n22 33547024 v 958 p 1002 both 0
seed 82003 stages(log2) 16:-27.000 17:-17.031 18:-12.992 19:-15.039 20:-6.000 21:-7.001 22:-1.000 23v:-14.992 23p:-15.075 | q3 variant 2^-101.0544 published-W8 2^-101.1380 | n22 33557228 v 1030 p 972 both 0
seed 82004 stages(log2) 16:-27.000 17:-16.938 18:-13.003 19:-14.983 20:-6.000 21:-6.998 22:-1.000 23v:-15.047 23p:-14.943 | q3 variant 2^-100.9693 published-W8 2^-100.8654 | n22 33556901 v 991 p 1065 both 0
seed 82005 stages(log2) 16:-27.000 17:-16.967 18:-13.011 19:-15.023 20:-6.000 21:-7.001 22:-1.000 23v:-15.045 23p:-14.974 | q3 variant 2^-101.0468 published-W8 2^-100.9759 | n22 33558013 v 993 p 1043 both 0
seed 82006 stages(log2) 16:-27.000 17:-16.999 18:-12.996 19:-15.000 20:-6.000 21:-7.002 22:-1.000 23v:-14.966 23p:-14.891 | q3 variant 2^-100.9624 published-W8 2^-100.8873 | n22 33551843 v 1048 p 1104 both 0
seed 82007 stages(log2) 16:-27.000 17:-16.986 18:-12.999 19:-15.012 20:-6.000 21:-7.001 22:-1.000 23v:-14.902 23p:-15.018 | q3 variant 2^-100.9000 published-W8 2^-101.0165 | n22 33552766 v 1096 p 1011 both 0
```

### A.9 `smc38_83.txt` (1702 bytes, SHA-256 92e30dde6eb0bf76e1197209aba3a88c64b5f2e89ed1f18c3bd3a764dad01918)

```text
row16 words per l: 32  total 32  |G| 245760
seed 83000 stages(log2) 16:-27.000 17:-16.966 18:-12.995 19:-15.001 20:-6.000 21:-6.999 22:-1.000 23v:-14.970 23p:-14.975 | q3 variant 2^-100.9309 published-W8 2^-100.9364 | n22 33562166 v 1046 p 1042 both 0
seed 83001 stages(log2) 16:-27.000 17:-17.027 18:-13.004 19:-15.008 20:-6.000 21:-7.000 22:-1.000 23v:-15.009 23p:-15.039 | q3 variant 2^-101.0481 published-W8 2^-101.0781 | n22 33556055 v 1018 p 997 both 0
seed 83002 stages(log2) 16:-27.000 17:-17.038 18:-13.002 19:-15.022 20:-6.000 21:-6.999 22:-1.000 23v:-15.128 23p:-15.065 | q3 variant 2^-101.1896 published-W8 2^-101.1264 | n22 33549970 v 937 p 979 both 0
seed 83003 stages(log2) 16:-27.000 17:-17.010 18:-13.009 19:-15.035 20:-6.000 21:-7.000 22:-1.000 23v:-14.987 23p:-15.017 | q3 variant 2^-101.0413 published-W8 2^-101.0710 | n22 33555517 v 1033 p 1012 both 0
seed 83004 stages(log2) 16:-27.000 17:-17.002 18:-13.002 19:-14.997 20:-6.000 21:-7.000 22:-1.000 23v:-15.125 23p:-15.014 | q3 variant 2^-101.1266 published-W8 2^-101.0157 | n22 33552058 v 939 p 1014 both 0
seed 83005 stages(log2) 16:-27.000 17:-16.967 18:-12.994 19:-15.027 20:-6.000 21:-6.997 22:-1.000 23v:-14.993 23p:-14.988 | q3 variant 2^-100.9778 published-W8 2^-100.9736 | n22 33547074 v 1029 p 1032 both 0
seed 83006 stages(log2) 16:-27.000 17:-17.007 18:-12.998 19:-14.951 20:-6.000 21:-7.001 22:-1.000 23v:-14.974 23p:-15.104 | q3 variant 2^-100.9306 published-W8 2^-101.0608 | n22 33560136 v 1043 p 953 both 0
seed 83007 stages(log2) 16:-27.000 17:-16.936 18:-13.003 19:-15.004 20:-6.000 21:-7.000 22:-1.000 23v:-15.010 23p:-15.125 | q3 variant 2^-100.9527 published-W8 2^-101.0678 | n22 33551857 v 1017 p 939 both 0
```

### A.10 `e2e38_seed3.txt` (496 bytes, SHA-256 ae39f79a38cf23cafe92baf2a026f234cf3b2e245c3bc45fe34ff723c1b26e05)

```text
setup: 245760 selected variants, row-16 set 32 words, 3a mask 4c431a80
first blocks 8388608 (2^23.00), 64 classes, 245760 variants
passing classes 35932046, expected 35913728.0 (ratio 1.0005)
good pairs 137979056640, expected 137908715520.0 (ratio 1.0005)
stage-3a passes 134745727, expected 134745172.5 (z +0.05)
row-16 passes 994, expected 1028.02 (z -1.06); exact checks 994, failures 0
within-first-block pairwise correlation of row-16 passes: rho = 0.000 (sum R(R-1) 0, p^2 sum G(G-1) 0.52)
```
