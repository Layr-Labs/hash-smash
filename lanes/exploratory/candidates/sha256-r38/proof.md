# Collision attack on 38-step SHA-256 with dense-part variants and a row-16 table: 2^78.12

**Track** sha256-r38-exploratory, target sha256-r38-prefix-v1, cost model collision-frontier-v5 (C = 2728).
**Claim** time_log2 = 78.12 (the exact total is 2^78.109596 target compressions; the claim leaves 0.0104 bit, 2^71.00
units, for stricter conventions of instruction pricing), success probability at least 0.39 (the bound is 0.3960005,
chosen with 2% slack in the expected number of successes), memory 2^80 bytes, preprocessing 2^78.09 (exact
2^78.088314, included in time), nonuniform advice below 2^14 bytes.
The total is dominated (98.5%) by the allowances for the advice (the values also used by the earlier r38 packages):
A_C = 2^78 for the characteristic search, A_S = 2^74 for the Step-1 solve, DEV = 2^64 for all development (H4).
The attack itself costs 2^72.07 units: 2^72.02 online, with deliberate margins (q3 one bit below its measured bounds,
and a pair budget delta = 1 against a measured 0.0018), and 2^67.21 of counted table construction.

**Revision.** The first version of this package (submission 8bc7d6c5, claim 70.23909, allowance A_C = 2^64) was
reviewed as not evaluable: two judges rated that allowance for the unpublished characteristic search unsupported.
This version charges allowances large enough to bound any realistic search (H4; the earlier r38 packages use the
same values), measures the pair term H5 directly
(Section 6.5), estimates q3 over the whole variant population (6.2), makes the variant enumeration counted code
(5.1), and uses q3_model = 2^-102, one bit below the measured bounds, so that the organizer replica checks the
modelled value with margin (10.1). All Monte-Carlo evidence was rerun under a new preregistration after an advisory
review found that the earlier runs' seeding made consecutive seeds overlapping streams (6.2). The second version
(submission 3b532546, claim 78.11) was reviewed as not evaluable because the evaluability judge rated H5 unsupported:
its numerical pair bound (0.0079) rested on experiments the organizer did not execute. This version budgets the pair
term at delta = 1 (a success brings at most one further success in its group on average), which the measurements
exceed by a factor of about 500, and claims 78.12. The construction and
the counted online program are unchanged.

**What is new.** Every earlier r38 package runs the two-block attack of ePrint 2026/1120 with the one dense-part
solution S that the paper prints (its Step 1): one success per 2^104.9 first blocks, 2^103.9 first blocks for
success 0.39. The characteristic does not pin
the first three internal words A0, A1, A2 of the second block's dense part. With the published A3..A13 kept, about
2^29.48 pairs (A1, A2) are still valid for each of 256 selected values of A0 ("variants", Section 4): each one
reproduces every A/E cell of rows 0..15 and every modular and sigma difference that reaches rows >= 16, so each is
a further copy of the attack for the same chaining value (copies on one chaining value are not assumed independent;
Section 6.4). For a chaining value CV1 and a fixed A0, the Step-2
words satisfy W1 = Y + A1 and W9 = c9(A2) - A1 where Y and W0 depend only on (CV1, A0). W16, which alone decides
row 16 (probability 2^-27), is therefore s0(Y + A1) - A1 + Z0 + c9(A2) with Z0 = W0 + s1(W14). A table indexed by
(Y, Z0), built once per A0, lists exactly the variants whose row 16 holds. One table load per (CV1, A0) tests about
2^29.48 variants. A chaining value meets 256 x 2^29.48 = 2^37.48 variants for about 117 operations per A0, so
2^68.43 first blocks (2^66.45 without the margins on q3 and on the pair term) replace the 2^103.9 of the published-S
attack. Apart from figures quoted from the paper and
the counts of the unprinted exploration programs listed in Section 11, every number in this file is computed by the
programs of Appendix B or by `experiments/vt38.py`; the claim rests on five declared premises (Section 9).

**Credit.** The 38-step differential characteristic, its two-bit conditions and the semi-free-start pair are those
of Yingxin Li, Zhuolong Zhang, Muzhou Li, Fukang Liu, Haifeng Qian and Jinwei Zhu, *Pushing Collision Attacks on
SHA-2 to 39 Steps*, IACR ePrint 2026/1120 (CC BY), Tables 3, 4 and 5, in the memory-efficient two-block framework of
[LLWS26] (Yingxin Li, Fukang Liu, Gaoli Wang and Jiali Shi, ePrint 2026/1080, CRYPTO 2026); the characteristic was
found with the tool of [LLW24a] (Li, Liu, Wang, EUROCRYPT 2024). From earlier public HashSmash packages
(submissions 20a43626 and 3d819a4b by winglock and co-workers, b99301f4 by leech1996, d5a10596 by 0xshikhar) this
package reuses the transcription of Tables 3-5, the exact Step-2 filter F7 (instead of the paper's cell conditions
on W7), the reading of `+` and of the misprinted condition on W25, the design of the sequential Monte-Carlo estimator
of the Step-3 probability, the pattern of fixed caps with a pair bound and Hoeffding over independent groups, and the
values of the three advice allowances.
The dense-part variants, the row-16 table, the counted program, the estimates and all evidence below are new and
were computed for this package. None of the credited authors has reviewed it; mistakes are ours.

## 0. Summary

- **Construction (Sections 3-4).** Two-block messages M0 || M1 and M0 || M1' (128 bytes; padding appends the same
  third block). A variant v = (A0, A1, A2) replaces the first three A-words of the published dense part (both
  members; rows 0..6 carry no difference) and recomputes E4..E6 and W8..W10. It is valid if the E cells of rows 4..8
  hold and the differences W'_i - W_i and s0(W'_i) - s0(W_i), i = 8..11, are the published ones (exact test).
  Lemma 3: for a valid v and any CV1 the Step-2 words give a pair that follows every A/E cell of rows -4..15 and has
  the published differences in every message-expansion term of rows >= 16 (W16..W37).
- **Row 16 as a lookup (Section 4.4).** Row 16 holds iff W16 is in G, a set of exactly 32 words (exhaustive).
  W16 = s0(Y + A1) - A1 + Z0 + c9(A2) (Lemma 5), with (Y, Z0) a function of (CV1, A0). Table T_j lists, for every
  (Y, Z0), the valid (A1, A2) of A0_j whose W16 is in G; a bucket holds at most 344,064 entries (Lemma 6).
- **Algorithm (Section 5).** N_G = 398,563,284,869,814,990,705 groups (2^68.43337). A group draws two random words,
  computes the first block (1 unit) and runs 256 A0 blocks: compute (Y, Z0) (29 operations), load the bucket, test
  each entry's W7 against F7 (10 operations), and for the W7 passes check row 17 (66 operations); the rare entries
  that pass the first row-17 test run rows 17..37 of both members (at most 3,158 operations). Three work counters
  are capped (Hoeffding over the independent groups). Every count is from the counted program of
  `experiments/vt38.py` (an op-counting interpreter running the exact code, including the group epilogue and the
  table-construction passes; Section 5.3).
- **Probability (Section 6).** For one variant on one chaining value the success probability is p2 q3(v) with
  p2 = |F7|/2^32 = 2^-3.90197 (exact under H1) and q3(v) the probability of rows 16..37 (cells and two-bit
  conditions). Rows 16..22 have the same probability for every valid variant (Lemma 4); the tail depends on
  (W8, W9, W10) of the variant. Preregistered SMC estimates (6.2): over a uniform 2^20-variant sample, mean
  2^-101.0001 and one-sided 99% bound 2^-101.0101 (64 runs); over 256 fresh uniform variants, one per run, mean
  2^-100.9983 and bound 2^-101.0051 for the population mean. The ledger uses q3_model = 2^-102, one bit lower (H2).
  All 1,883,203 tail successes of these runs and of 6.5 were rebuilt and verified as 38-step semi-free-start
  collisions of the variant they used; on 4,000 of them the counted program itself finds and verifies the pair.
- **Real first blocks (Section 6.3).** On 5.2 x 10^7 chaining values from uniform first blocks through real 38-step
  compressions, the measured bucket sizes and W7 rates match the predictions; the row-17 rate is at or above the
  SMC value; the counted program agrees with the reference on 400 chaining values with their true buckets.
- **Pair term (Section 6.5).** On the chaining values of 513,481 verified successes of variants of 8 A0 values
  spread over the set (pairwise Hamming distances 1 to 9), every other variant of the 8 A0 was tested exactly
  through row 17. Rows 16 and 17 pass at rates consistent with the unconditional ones; the expected number of further
  successes per
  success, extrapolated to the 256 A0 values, is at most 0.0018 (99%, seed-clustered); the ledger budgets 1.
  Variants sharing (A0, A1) gave 0 further successes on 1,883,203 successes.
- **Ledger (Section 7).** T = 2^78.109596 units: allowances 2^78.08755; online 2^72.01600 (first blocks, A0 blocks,
  entries, row-17 and deep paths at their caps); table preprocessing 2^67.21233 (counted build code, zero
  initialisation included). Success >= 0.3960005 under H1, H2 and H5; with the measured pair term the bound stays
  >= 0.39 down to q3 = 2^-103.02, about two bits below the measured q3 bounds.
- **Premises (Section 9).** H1 chaining value of one trial behaves as uniform; H2 the q3 bound; H3 table pricing
  (one load = one operation in the word RAM; memory is reported, 2^80 bytes); H4 advice allowances (they set the
  score); H5 the expected number of further successes in a group, seen from a success. No expected-work bound, independence-of-conditions model or independence inside a group is used.
- **Organizer experiments (Section 10).** `vt-q3-smc-r38` runs a reduced replica of the SMC on organizer seeds and
  returns verified semi-free-start collisions of random variants with a preregistered pass rule (about 0.4-bit
  resolution; its threshold 2^-101.45 lies 0.55 bit above q3_model); `vt-ram-r38` runs the counted program on organizer-seeded
  real first blocks against the reference construction and returns a pair only if every check passed.

## 1. Target, cost model and notation

- **Target** sha256-r38-prefix-v1: SHA-256 steps 0..37 on every padded block, standard IV once, FIPS 180-4 padding,
  feed-forward, all eight digest words (repository `verifier/hash_functions.digest(m, "sha256", 38)`).
- **Cost model** collision-frontier-v5: one 38-step compression = 1 unit; every other 256-bit word primitive (load,
  store, add, sub, and, or, xor, shift, comparison, conditional branch, random word) = 1/C unit, C = 2728.
  Immediates and shift amounts are instruction fields. Memory is reported, not scored. Success >= 0.39.
- **Step i** (i = 0..37): E_i = A_{i-4} + E_{i-4} + S1(E_{i-1}) + CH(E_{i-1}, E_{i-2}, E_{i-3}) + K_i + W_i and
  A_i = E_i - A_{i-4} + S0(A_{i-1}) + MAJ(A_{i-1}, A_{i-2}, A_{i-3}) (mod 2^32), with
  (A_{-1}, A_{-2}, A_{-3}, A_{-4}, E_{-1}, E_{-2}, E_{-3}, E_{-4}) = (a, b, c, d, e, f, g, h) of the incoming chaining
  value. The output is cv + (A_37, A_36, A_35, A_34, E_37, E_36, E_35, E_34). Message expansion
  W_i = s1(W_{i-2}) + W_{i-7} + s0(W_{i-15}) + W_{i-16} (i >= 16). M = 2^32 - 1.
- **Members.** x is the message the paper prints second (M'), y the one printed first (M). Characteristic symbols
  (MSB first): `u` = (x, y) bits (1, 0), `n` = (0, 1), `0`/`1` fixed and equal, `=` equal; `+` in rows i-1 and i at
  bit b means E_i[b] = E_{i-1}[b] (the paper does not define `+`; on the published pair this reading holds in every
  vertical pair, and it only adds conditions). A row "holds" if the x-values, the XOR differences between members,
  the `+` pairs and the two-bit conditions keyed at that row (on member x) hold.

## 2. Sources, and what is reused or new

| item | source | here |
|---|---|---|
| characteristic (Table 3), two-bit conditions (Table 4), SFS pair (Table 5) | ePrint 2026/1120 | transcribed as in 20a43626/3d819a4b/d5a10596; verified (Section 3.3) |
| W25[4] = W25[9] read as W25[4] = W25[6] | 3d819a4b | same (the printed condition fails on the published pair) |
| Step-2 equations, exact filter F7, |F7| | [LLWS26], 3d819a4b | same; |F7| recounted (fset.c) |
| SMC design for q3 (row 16 exact, importance-weighted rows 17..22, W23 tail) | 3d819a4b | reimplemented in C (smc2.c, now smc3.c), tail averaged over variants |
| fixed caps, Bonferroni with a pair bound, Hoeffding | b99301f4 | same pattern; three work counters |
| dense-part variants (A0, A1, A2), validity, the A2 list, the A0 set | new | Section 4 |
| row 16 as a function of (Y, Z0); the tables T_j; bucket bound | new | Sections 4.4-4.5 |
| counted online program and ledger | new | Sections 5, 7; `experiments/vt38.py`, cert.py |

The paper's own attack (its Section 3.1) uses one Step-1 solution and the freedom in (W14, W15); its count is
2^104.3 expected work. For the published solution only one (W14, W15) survives the row-16 differences (|L*| = 1,
established in 3d819a4b and rechecked here); this package keeps that (W14, W15) and gains its freedom elsewhere.

## 3. The characteristic and the published dense part

### 3.1 The table (rows with a non-`=` cell; i, A_i, E_i, W_i)

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

### 3.2 Two-bit conditions with a word in rows >= 16 (Table 4; member x; keyed at the later row)

```text
A14[15]=A16[15] A14[23]=A16[23] A14[25]=A16[25] A15[4]=A16[4] A15[7]=A16[7] A15[16]!=A16[16] A15[17]=A16[17]
A15[27]=A16[27] A15[29]=A16[29] A16[15]=A17[15] A16[23]=A17[23] A16[25]=A17[25] A17[9]=A17[20] A17[6]=A17[18]
A17[8]=A17[17] A16[29]=A18[29] A18[29]=A19[29] E16[4]!=E16[23] E16[3]!=E16[8] E16[14]=E16[28] E16[4]=E17[4]
E16[18]=E17[18] E18[0]!=E18[13] E17[15]=E18[15] E17[24]=E18[24] E19[6]!=E19[19] E19[20]=E19[2] E21[2]=E21[16]
W16[1]!=W16[12] W16[20]!=W16[27] W16[8]=W16[25] W16[14]=W16[18] W16[4]!=W16[6] W16[22]!=W16[31]
W23[0]!=W23[30] W23[1]!=W23[31] W23[14]=W23[21] W23[16]=W23[25] W25[4]=W25[6] W25[22]=W25[31] W25[20]=W25[27]
```

The printed W7 and W8 conditions are not used: W7 is tested by the exact filter F7 (3.5), and W8 enters only
through its differences, which variant validity fixes exactly (4.1). The success event of this package is: every
cell of rows 16..37 and every condition above holds, and W7 is in F7.

### 3.3 The semi-free-start pair (Table 5) and the published dense part S*

```text
CV  cd278980 1b12a052 b87cc8a6 a9e059c5 c9c3db85 6ca4b5b5 63d13ac1 c0329f1e
M   48fc271b 9fca20cd cc89f96f fc40396f 8b328cb4 6b91ef78 97f9b767 e2450045 3b016f58 de9804cb 66a99ea5 0ce30b8d a28cd15a 77a1e994 d28e48a0 9b5f6dbb
M'  48fc271b 9fca20cd cc89f96f fc40396f 8b328cb4 6b91ef78 97f9b767 c2450045 3f416758 fe9804cb 63a88c0f 0ceb1f8d a28cd15a 77a1e994 d28e48a0 9f1f65bb
```

F_38(CV, M) = F_38(CV, M') = 5d9ca5f4 59ace3a3 26c9c26c 4252c585 4c0803b7 1b4d5ccd 25c3ccc0 90645c4d under our code and
the repository verifier; every cell of rows -4..37 and every condition of 3.2 holds with x = M', y = M (selftest).
S* is the inner part of the pair (columns: member x, member y; values not listed are equal in both members):

```text
i   A_i (x, y)          E_i (x, y)          W_i (x, y)
0   b75dae71
1   da6c35e0
2   479b4dc8
3   d374b0d8
4   df740c96            627cb061
5   1ee5f173            1e847683
6   7fd9cecb            0c1c24b9
7   3e016e83 5e016e83   e2e9b205 02e9b205
8   b6a6b5f9 b6e7bde9   99352c79 917934e9   3f416758 3b016f58
9   3ec0b304            c670b71b c2e0b710   fe9804cb de9804cb
10  bcc85d8c            68c3aa97 6882a297   63a88c0f 66a99ea5
11  25d3cc99 25d3c495   c2f2c1be e2f2b1ba   0ceb1f8d 0ce30b8d
12  4846f2d8 0c66b4da   5f9d1216 63be1213   a28cd15a
13  c2dc0441 e2dd0441   35c13b0d 35c03c77   77a1e994
14  c84cdcb9 c04fdc29   21966471 29976471   d28e48a0
15  91c40603 93448603   4a9b6b5a 4a9b63da   9f1f65bb 9b5f6dbb
```

Rows 14, 15 and (W14, W15) are the published ones throughout this package (the exact freedom set L* of the
published solution has one element; 3d819a4b, Section 4.4).

### 3.4 Differences that reach rows >= 16

The published pair has W'_i - W_i (x minus y) and s0(W_i^x) - s0(W_i^y) equal to (043ff800, 01808000) for i = 8,
(20000000, fbc00800) for i = 9, (fcfeed6a, 10005f30) for i = 10 and (00081400, 03011296) for i = 11; W12, W13, W14
carry no difference; dW16 = W16^x - W16^y = 20000000 and dW17 = 0 for every chaining value (they are functions of
these constants, W9 and W15).

### 3.5 Step-2 equations and the exact W7 filter

For a dense part (A0..A7, E4..E7 of a member) and a chaining value CV1, the Step-2 equations
E_i = A_i + A_{i-4} - S0(A_{i-1}) - MAJ(A_{i-1}, A_{i-2}, A_{i-3}) (i = 3, 2, 1, 0) and
W_i = E_i - A_{i-4} - E_{i-4} - S1(E_{i-1}) - CH(E_{i-1}, E_{i-2}, E_{i-3}) - K_i (i = 0..7) give the unique
W0..W7 that connect CV1 to the dense part; CV1 -> (W0, ..., W7) is a bijection of (2^32)^8 for a fixed dense part
(triangular; [LLWS26], 3d819a4b Lemma 1). Both members use the same CV1; for every dense part of this package
W'_i = W_i (i <= 6) and W'_7 = W_7 + d7, d7 = 20000000, and W7 = c7 - a with c7 a constant of the dense part.
W7 enters rows >= 16 only through s0(W7) in W22 and W7 in W23; the characteristic fixes the difference of W22, so a
pair can follow row 22 only if s0(W7 + d7) - s0(W7) = t7 = 03bff800. F7 = {w : s0(w + d7) - s0(w) = t7} has
|F7| = 287,309,824 elements (exhaustive count, fset.c), p2 = |F7|/2^32 = 2^-3.90197.

## 4. Dense-part variants

### 4.1 Definition and validity

**Definition.** For words (A0, A1, A2) the variant v = (A0, A1, A2) is the dense part with A0, A1, A2 of both members
replaced (rows 0..6 carry no A or E difference, so both members get the same values), A3..A13, E7..E13 and
W11..W15 of S* unchanged, and E4, E5, E6 and W8, W9, W10 of each member recomputed by
E_i = A_i + A_{i-4} - S0(A_{i-1}) - MAJ(A_{i-1}, A_{i-2}, A_{i-3}) (i = 4, 5, 6) and
W_i = E_i - A_{i-4} - E_{i-4} - S1(E_{i-1}) - CH(E_{i-1}, E_{i-2}, E_{i-3}) - K_i (i = 8, 9, 10).
(E7 depends on A3..A7 only; W11 on E7..E11 and A7 only; both are unchanged.)

**Validity.** v is valid if (i) the E cells of rows 4..8 hold for both members, including the `+` pairs (rows 5/6:
E6[31..29] = E5[31..29]; rows 6/7: E7[19] = E6[19], E7[11] = E6[11]), and (ii) for i = 8, 9, 10, 11 the pair
(W_i^x - W_i^y, s0(W_i^x) - s0(W_i^y)) equals the published value of 3.4. The XOR cells of W8..W10 are not
required: these words reach rows >= 16 only through those modular quantities (W8 in W23 via s0 and in W24; W9 in
W16, W25 and via s0 in W24; W10 in W17, W26 and via s0 in W25).

**Lemma 3 (variants are sound).** Let v be valid, CV1 arbitrary, W0..W7 the Step-2 words of member x from CV1 and v,
W'_0..W'_7 those of member y, and M1 = (W0..W7, W8..W15 of x), M1' = (W'_0..W'_7, W8..W15 of y). Then F_38 from CV1
reproduces v's A0..A13, E4..E13 in both members, rows -4..15 follow every A/E cell, and every term of W16..W37 that
involves W0..W15 has the published difference, except the s0(W7) term (handled by F7). In particular
dW16 = 20000000 and dW17 = 0.
*Proof.* Steps 0..7 reproduce A0..A7, E0..E7 by construction of the Step-2 words; steps 8..10 reproduce E8..E10 and
A8..A10 because W8..W10 are solved from them; steps 11..15 are those of S* (they depend on rows 7..15 and W11..W15
only). Rows 0..3 have no cells; rows 4..8 hold by (i); rows 9..15 are those of S*. W0..W6 have no member difference
and W7 has difference d7 for every dense part of this kind (c7^y - c7^x = E7^y - E7^x). The expansion terms that
involve W8..W11 have the published differences by (ii); W12..W15 are published. Checked on 300 random chaining
values per run of the selftest (Appendix A.1, item 5) and on every pair rebuilt in Sections 6.2 and 10.

### 4.2 The A2 list

Conditions that involve A2 alone (A0, A1 do not enter): E6 = A6 + A2 - S0(A5) - MAJ(A5, A4, A3) must satisfy row 6's
x-value cells and E7[19] = E6[19], E7[11] = E6[11]; W10 (which depends on E6 only) must have the published
(dW10, ds0(W10)). An exhaustive pass over all 2^32 values of A2 (`load_a2` in lib.h) leaves exactly 768 values
(Appendix A.3), the A2 list. W9 = c9(A2) - A1 with
c9(A2) = E9 - 2 A5 + S0(A4) + MAJ(A4, A3, A2) - S1(E8) - CH(E8, E7, E6(A2)) - K9 (member x; member y: c9 - dW9);
the 768 values fall into 96 classes of equal c9 (sizes 4, 6 and 8).

### 4.3 The A0 set and the variant sets R_j

For A0 fixed, R(A0) is the set of (A1, A2) with A2 in the A2 list and (A0, A1, A2) valid. Condition (i) on E5
(E5[31..29] = E6[31..29]) confines A1 to one residue interval of length 2^29 per A2, so R(A0) is found by testing
768 x 2^29 candidates (`enum_v` in lib.h). The only condition that involves A0 is the s0 difference of
W8 = F(A1, A2) - A0, where F does not depend on A0. A0 was chosen to maximize |R(A0)| from the exact histogram of F
over all (A1, A2) that satisfy the A0-free conditions (2^33.211 pairs; v9all.c, a0exact.c): the A0 set is the 256
values with the largest exact |R(A0)| among 3,000 candidates found by local search (Appendix A.2 lists them with
their exact sizes). min |R_j| = 747,959,736 = 2^29.47839, max 750,798,738 = 2^29.48385, and

    SR = sum_j |R_j| = 191,773,672,732 = 2^37.48061.

The published A0 itself has |R| = 212,845,642 = 2^27.66523 and is not in the set; the published S* is not needed by the attack
except for A3..A13, E7..E13 and W11..W15. The fast test valid3 (lib.h) agrees with the generic test var_valid (core.h) on 2,000,000 random candidates and
on every sampled variant (varsample.c checks each one). The sample used by the SMC is `varsample a0set256.txt 256
1048576 20261010 vs256.bin` (2^20 variants; A0_j with probability |R_j|/SR, then (A1, A2) uniform in R_j by rejection
from the 768 x 2^29 candidates); the 512 variants embedded in vt38.py are its first 512 records.

### 4.4 Row 16 is a function of (Y, Z0)

**Lemma 4 (rows 16..22 do not depend on the variant).** Fix a valid v and let CV1 be uniform. Then (W0, ..., W7) is
uniform on (2^32)^8 (3.5); conditioned on W7 in F7, (W0..W6) is uniform and independent of W7. For any (W14, W15)
and W9..W13, the map (W0..W5) -> (W16..W21) is a bijection for fixed W6 (W5 = W21 - s1(W19) - W14 - s0(W6), ...,
W0 = W16 - s1(W14) - W9 - s0(W1)), so (W16..W21) is iid uniform and independent of (W6, W7), and
W22 = s1(W20) + W15 + s0(W7) + W6. Rows 12..15 of both members are those of S*, and the differences of W16..W22 are
the published ones (Lemma 3). Hence the joint distribution of rows 16..22 of both members, conditioned on W7 in F7,
is the same for every valid variant, and so is the probability that rows 16..22 hold. Rows 23..37 depend on the
variant only through W8, W9, W10 of both members (W23 = s1(W21) + W16 + s0(W8) + W7, W24 = s1(W22) + W17 +
s0(W9) + W8, W25 = s1(W23) + W18 + s0(W10) + W9, W26 = s1(W24) + W19 + s0(W11) + W10).

**G.** With rows 12..15 of S*, row 16 (cells, `+`, the conditions of 3.2 keyed at row 16) is a function of W16^x
alone (E16 = A12 + E12 + S1(E15) + CH(E15, E14, E13) + K16 + W16 and A16 = E16 - A12 + S0(A15) +
MAJ(A15, A14, A13) in each member, W16^y = W16^x - 20000000). An exhaustive pass over all 2^32 values (gset.c) finds
exactly 32 words, G = {35f29010 + any subset of bits 0, 2, 10, 13, 19} (= 2^-27 of all words).

**Lemma 5 (W16).** For a chaining value CV1 and A0 put hh = d - S0(a) - MAJ(a, b, c), E0 = A0 + hh,
Y = -S0(A0) - MAJ(A0, a, b) - g - S1(E0) - CH(E0, e, f) - K1, W0 = A0 + hh - d - h - S1(e) - CH(e, f, g) - K0 and
Z0 = W0 + s1(W14). For every valid (A0, A1, A2): W0 is the Step-2 word, W1 = Y + A1, W9^x = c9(A2) - A1 and
W16^x = s0(Y + A1) - A1 + Z0 + c9(A2) (mod 2^32).
*Proof.* E0 depends on A0 and CV1 only; E1 = A1 + c - S0(A0) - MAJ(A0, a, b), so W1 = E1 - c - g - S1(E0) -
CH(E0, e, f) - K1 = A1 + Y; W9 = E9 - A5 - E5 - S1(E8) - CH(E8, E7, E6) - K9 with E5 = A5 + A1 - S0(A4) -
MAJ(A4, A3, A2); W16 = s1(W14) + W9 + s0(W1) + W0. (Selftest item 5 checks all four identities.)

### 4.5 The tables T_j and the bucket bound

For j = 1..256 let T_j map every (Y, Z0) in (2^32)^2 to the list of entries for the (A1, A2) in R_j with
s0(Y + A1) - A1 + Z0 + c9(A2) in G. By Lemma 5 and the definition of G, the bucket T_j[Y, Z0] holds exactly the
variants of A0_j whose row 16 holds for a chaining value with these (Y, Z0). An entry is one 256-bit word: c7 of the
variant (bits 0..31; W7^x = c7 - a), A1 (32..63), the A2 index (64..73), the index of W16 in G (74..78) and S0(A1)
(80..111). A bucket header is one word: (offset << 20) | count.

**Lemma 6 (bucket bound).** |T_j[Y, Z0]| <= 344,064 for all j, Y, Z0.
*Proof.* With u = Y + A1 the condition reads phi(u) = g' - Y - Z0 - c9(A2) for some g' in G, phi(u) = s0(u) - u.
For each of the 96 values of c9 and the 32 values of g' this fixes phi(u), and every value has at most 14 preimages
(exhaustive over 2^32, phimax.c: 1 value with 14, 1 with 13, 3 with 12). Each A1 pairs with at most the class size
(<= 8) of A2 values, so a bucket has at most 14 x 32 x 768 = 344,064 entries. (Observed maximum over 3.2 x 10^7
random buckets: 104; the distribution is in Section 6.3.)

**Expected bucket size.** For a uniform CV1, (W0, W1) is uniform for every fixed variant (3.5), hence (Y, Z0) is
uniform, and E|T_j[Y, Z0]| = |R_j| x 32/2^32 = |R_j| 2^-27 exactly (5.593 for the largest R_j).

### 4.6 Row 17 of member y

For each of the 32 values of W16 in G the row-16 state of both members is fixed, and W17^y = W17^x (dW17 = 0).
For all 32 values E17^y = E17^x and A17^x - A17^y = 20000000 (checked for each value; `tables` in vt38.py builds the
per-value constants), so member y's row-17 cells follow from member x's (A17^x[29] = 1, the `u` cell). Row 17 is
tested on member x: E17^x against a mask of 10 bits (its x-value cells, the `+` pair with E16 and the two E16-E17
conditions, which coincide with the `+` bits), A17^x against 4 bits (its cell and the A16-A17 conditions with A16
known) and the three A17-internal conditions.

### 4.7 The success event

For a chaining value CV1 and a valid variant v, A(CV1, v) is the event that row 16 holds (W16 in G), W7 is in F7, and
rows 17..37 hold (cells, `+`, the conditions of 3.2). **Lemma 7.** A(CV1, v) implies
F_38(CV1, M1) = F_38(CV1, M1'), hence a collision of M0 || M1 and M0 || M1' when CV1 = F_38(IV, M0); M1 != M1'
because W7 differs by d7. *Proof.* Rows 34..37 have no u/n cell, so A_i and E_i (i = 34..37) are equal in both
members; with the common CV1 these are the outputs. (Every success of Sections 6.2 and 10 is also checked directly.)

## 5. The algorithm

### 5.1 Preprocessing (deterministic; costs in operations)

| step | work | operations |
|---|---|---|
| P1 G | all 2^32 values of W16, row 16 of both members (Section 4.4) | 2^32 x 64 |
| P2 F7 word table | F7T[w] = 1 iff w in F7, all 2^32 w | 2^32 x 24 |
| P3 A2 list | all 2^32 values of A2 (4.2) | 2^32 x 64 |
| P4 records | 768 A2 records (4 words: A2, W10x + s1(W15x), S0(A2), E6, E5 - A1, c9x, c9y, W10x, W10y), 32 G records | 768 x 64 + 32 x 128 |
| P5 R_j | per (A0, A2): setup 42 and outer loop 8; 2^29 candidates (valid3, at most 67 operations each); for each valid variant 25 more (entry base word and c9x appended to R_j) | 256 x 768 x (2^29 x 67 + 50) + SR x 25 |
| P6 T_j | zero the 2^64 header words (4 each); count pass over every (Y, (A1, A2)): u = Y + A1, X = s0(u) - A1 + c9, then for each of the 32 g in G: Z0 = (g - X) and M, header address, count (211 per (Y, variant)); prefix sums: header = offset << 20 or count, cursor = offset (10 per header); fill pass: entry stored at the cursor of each of the 32 targets (275 per (Y, variant)); setup per Y and pass (10) | 2^32 x SR x (211 + 275) + 256 x 2^64 x (4 + 10) + 256 x 2^32 x 20 |

P5 and P6 are counted code in vt38.py. P6 (`gen_build_pass`, `gen_zero`, `gen_prefix`): the selftest runs the
passes on a toy instance (two values of Y and up to 34 variants, including a c9 class sharing W16, so buckets hold up
to 16 entries) and checks every bucket against the definition of 4.5 (0 mismatches) and the per-item counts 211,
275, 4, 10. P5 (`gen_enum_setup`, `gen_enum`, `gen_enum_outer`): the setup computes the constants of (A0, A2) and the
window start st of 4.3; the candidate loop tests the `+` pair of rows 5/6, ds0(W9) (dW9 holds for every A1), dW8 and
ds0(W8) with W8 = k8 - E4 - CH(E7, E6, E5) per member, and appends the entry base word and c9x of a valid variant.
The selftest (item 10) runs it for two A0 on two windows of 4,096 candidates each (one around a known valid A1, one
straddling st, so the `+` test both passes and fails) and compares every appended word with the reference test
valid() and the entry words of the table build: 0 mismatches, 604 valid variants; the executed operations stay
below 67 per candidate plus 25 per valid variant. Total preprocessing 466,412,701,031,896,270,852,028 operations =
2^67.21233 units; with the allowances of Section 7 the preprocessing is 2^78.088314, claimed as 2^78.09. The A0 set, the A2 list and the order of the tables are advice of this
package (Section 8); their search is covered by the development allowance.

### 5.2 Online

```text
input: N_G (groups), caps NE_MAX, NW_MAX, N1_MAX; coins: uniform 256-bit words
NE = NW = N1 = 0
for group = 1 .. N_G:
    r0, r1 = RAND, RAND; M0 = the sixteen 32-bit fields of (r0, r1); CV1 = F_38(IV, M0)          # 1 unit
    per-CV values: hh, y0', a^b, a&b, e^f, g + K1                                                # prologue
    for j = 1 .. 256:                                                                            # A0 block j
        compute Y, Z0 (Lemma 5); H = T_j header at (Y, Z0); NE += count
        for each entry of the bucket:
            W7 = (c7 - a) mod 2^32; if F7T[W7]:                                                  # p2
                NW += 1; compute W1, E1, W2, W17, E17 (member x); test the 10-bit E17 mask       # 2^-10
                if it holds: N1 += 1; test A17; compute W3..W7, W8..W10 of both members, expand
                    W18..W37, run steps 18..37 of both members testing every row; if every row holds:
                    output M0 || M1 and M0 || M1' after checking both digests (6 units); halt
    if NE > NE_MAX or NW > NW_MAX or N1 > N1_MAX: halt (failure)
halt (failure)
```

The caps are tested after every group, so the program executes at most N_G groups, NE_MAX entries, NW_MAX row-17
paths and N1_MAX first-test passes plus at most one group's worth of each (256 x 344,064 items, charged in the
ledger), and one output check, whatever its coins. Any output is a collision (Lemma 7 and the digest check).

### 5.3 The counted program

`experiments/vt38.py` contains the online program as 256-bit word-RAM code (generators `gen_prologue`, `gen_block`,
`gen_row17`, `gen_deep`, `gen_epilogue`), a register allocator (liveness on the control-flow graph, greedy colouring;
41 registers are used, at most 64 allowed) and an interpreter `Machine` that counts every executed operation: add,
sub, and, or, xor, shl, shr, load and store (register or direct address), random word and unconditional jump cost 1,
a conditional branch costs 2 (comparison and branch), the compression costs 1 unit. Values are 32-bit words held in
256-bit registers; arithmetic is mod 2^256 and masked with M before any rotation, comparison or address use
(additions and subtractions carry upward only, so bits above 31 never reach a used low bit). A 32-bit rotation uses
the doubled word x | x << 32 (2 operations), so S0, S1, s0, s1 cost 7 when the final mask is shared. Static path
costs (every instruction counted along each path; `static_costs.py`):

| part | operations |
|---|---|
| group prologue: 2 RAND, unpack 16 words, CV1 (+1 unit), per-CV values | 64 |
| A0 block: E0, S1(E0), CH, MAJ, Y, Z0, table index, header load, count/offset, NE update, empty test | 29 (+1 if the bucket is not empty) |
| one entry: load, W7, F7T load, branch, next | 10 |
| row-17 path of a W7 pass, to the first test (E17 mask) and back | 66 |
| after the first test: A17 tests (12 / 13 more) and the deep path to its last test or success | at most 26 + 3,132 |
| group epilogue: three cap tests, group counter, group loop branch | 15 |

The interpreter reproduces these counts (selftest item 7: prologue with epilogue and loop 79 = 64 + 15, empty block
29, a block with three entries that fail W7 60 = 29 + 1 + 30). The table-construction passes are counted the same way
(selftest items 9 and 10; Section 5.1). The selftest also runs the program on four semi-free-start successes of the SMC
(Section 6.2) as forced chaining values, with buckets holding decoys and the true entry: it reaches the success and
the pair collides (item 6). The organizer experiment `vt-ram-r38` runs it on organizer-seeded real first blocks
(Section 10.2). The tables are served to the interpreter by an oracle (a test can only supply buckets it knows);
the op counts do not depend on the table contents beyond the bucket size. On true buckets (all row-16 variants of
A0 = 3662dd58 for 400 real chaining values, dumped by pipe.c: 2,326 entries) the program's counters NE, NW, N1 agree
with the reference construction on every chaining value (truebucket.py; 172 W7 passes, 0 first-test passes).

## 6. The success probability

### 6.1 One variant on one chaining value (H1)

For a fixed valid v and a uniform CV1, Pr[A(CV1, v)] = p2 q3(v), where q3(v) = Pr[rows 16..37 hold | W7 in F7].
This uses the distribution of 3.5 and Lemma 4 only. H1 (Section 9) states that the chaining value of one first
block, CV1 = F_38(IV, M0) with M0 uniform, behaves as uniform for these events.

### 6.2 q3 for the variants (H2): the SMC estimate

**Estimator** (smc3.c, Appendix B.4). Row 16 exactly: the 32 words of G out of 2^32 (stage factor 2^-27 exactly);
particles start from uniform elements of G. Rows 17..22: E_i^x is proposed uniformly with its x-value cells and its
`+` bits imposed (exact weight 2^-f, f = number of imposed bits), W_i^x = E_i^x - (rest of step i), W_i^y = W_i^x -
(its exact difference: ds1(W_{i-2}) + dW_{i-7}, and -t7 for i = 22), both members are stepped and the whole row is
tested; W16..W21 are iid uniform and W22 is uniform given W20 because W6 is (Lemma 4), so the proposals are exact.
Tail: each proposal draws a variant uniformly from a sample of 2^20 variants drawn uniformly from the union of the
R_j (vs256.bin, varsample.c) and sets W8, W9, W10 of both members to the variant's, proposes W23^x with its x-value
cells imposed (f = 6) and sets W7 = W23 - s1(W21) - W16 - s0(W8); weight 1{W7 in F7} 2^(32-f)/|F7|; rows 23..37 are
then deterministic (both members, every row tested). NP particles, M_i children per particle, multinomial
resampling after every stage but the tail; the estimate is the product of the stage means, unbiased for the
variant-averaged q3 (the standard unbiasedness of the SMC normalising-constant estimator; resampling keeps particle
averages unbiased, and the variant sample is itself uniform). Every tail success is rebuilt: W0..W6 by the inverse
expansion, CV1 by inverting steps 7..0 of the variant; it is accepted only if F_38(CV1, M1) = F_38(CV1, M1') with
M1 != M1', the variant's Step-2 words map CV1 back to W0..W7, W7 is in F7 and every A/E cell of rows -4..37 and W
cell of rows 16..37 holds (the conditions of 3.2 are rechecked by the success test). Clumping replay: for every
success, every other A2 of the list valid with the same (A0, A1) is tried on the same CV1.

**Seeding of the earlier runs.** The runs of the first version (smc2.c) and the third version's added runs seeded the
splitmix64 generator with seed0 x phi + 1, while each draw adds phi: the stream of seed s + 1 is the stream of seed s
shifted by one draw, so consecutive seeds were not independent (all 64 runs of the first preregistration printed the
same row-21 factor, -7.003). smc3.c starts from the splitmix64 output of seed0 instead (unrelated points of the 2^64
cycle) and is otherwise unchanged, with smc_het's optional fixed-variant argument. All runs below use it; the earlier
runs are superseded (their means agree with the new ones within 0.004 bit; Appendix A.4 lists them).

**Preregistration** (PREREG_v3.txt, sha256 6ba6bc72570e76e5..., frozen 2026-10-09T17:28:36Z, Appendix A.4): program smc3.c
sha256 389af9738dacd0f6..., data vs256.bin, a0set256.txt, G, F7 as before; NP 4000, children 2048, 64, 64, 8, 8, 4 at rows
17..22, 8192 tail proposals per particle; every seed reported (Appendix A.5); rules: one-sided 99% Student bounds,
q3_model = 2^-102 kept if both are at least 2^-102.

| quantity | R1: fixed uniform 2^20-variant sample | R2: population, one fresh uniform variant per run |
|---|---|---|
| seeds | 21001..21064 | 22000..22255 (run i: variant i of vsP.bin, `varsample a0set256.txt 256 256 20261011`) |
| mean of Z / relative sd | 2^-101.0001 / 0.0230 | 2^-100.9983 / 0.0321 |
| min / max | 2^-101.0982 / 2^-100.9476 | 2^-101.1694 / 2^-100.8690 |
| one-sided 99% bound | 2^-101.0101 (63 df, t = 2.3870) | 2^-101.0051 (255 df, t = 2.3411) |
| stage means (log2): rows 16..22, tail | -27.000 -17.000 -13.000 -14.999 -6.000 -7.000 -1.000 -15.002 | -27.000 -16.999 -13.000 -15.000 -6.000 -6.999 -1.000 -15.000 |
| tail successes, rebuilt and verified | 273,712, failed rebuilds 0 | 1,096,010, failed rebuilds 0 |
| clumping replay | 0 further successes in 3,341,913 trials | 0 further successes in 12,547,972 trials |

R1 bounds the average over the fixed sample (particle noise only). R2 bounds the population average directly: its
variants are independent uniform draws from the union of the R_j, each run's estimate is unbiased for its variant's
q3, and the spread of the 256 estimates contains the variant dispersion (relative sd 0.032 against 0.023
for R1), so no extrapolation from the sample to the population is needed.

**q3_model.** Both bounds exceed 2^-102 (the smaller is 2^-101.0101), so by the preregistered rule the ledger uses
q3_model = 2^-102, one bit below them; because the allowances dominate T, the margin costs about 0.01 in the claim
(Section 7). The integer stage factors (row 17: 2^-17.000) are also the rates used for the predictions of 6.3.

**The counted program on SMC successes** (R4, ram_check.py, Appendix B.20). For 4,000 successes of R2 drawn with a
preregistered seed (166 distinct A0), the success's chaining value is forced and its A0 block's bucket holds a
decoy, the true entry and the decoy: the counted program finds and verifies the pair in all 4,000 cases (failures: 0), so the program's own tests (row-17 masks, deep path) accept exactly the SMC's success event on these samples.

### 6.3 Consistency and measurements on real first blocks

- **Published dense part.** The same estimator with the published W8, W9, W10 (smc.c, 8 development seeds) gives
  log2 q3 between -101.07 and -100.93, stage factors as above; the tail factor of variants (-15.005) equals the
  published one (-14.99). The integer stage factors agree with the earlier packages' independent estimate for the
  published S (3d819a4b: mean 2^-100.9941; stages -27.000, -16.997, -13.000, -15.002, -6.000, -7.000, -1.000,
  -14.995).
- **Real first blocks** (pipe.c, Appendix B.5). M0 uniform (64-bit PRNG), CV1 = F_38(IV, M0) by a real compression;
  for one A0 the program finds every (A1, A2) of R(A0) whose row 16 holds through phi^-1 (an exact inverse table of
  phi), builds the pair with the generic code, checks rows -4..16 of both members, W7 and every later row:

| run | A0 | chaining values | entries per CV (predicted) | W7 rate (2^-3.90197) | row 17 passed (predicted) | cell mismatches |
|---|---|---:|---|---|---|---:|
| long | 36613d50 | 20,000,000 | 5.5920 (5.5939) | 2^-3.9016 | 74 (57.1) | 0 |
| a | 3662dd58 | 6,000,000 | 5.5903 (5.5939) | 2^-3.9042 | 15 (17.1) | 0 |
| b | 366afd58 | 6,000,000 | 5.5733 (5.5727) | 2^-3.9017 | 20 (17.1) | 0 |
| long2 | 36613d50 | 20,000,000 | 5.5945 (5.5939) | 2^-3.9021 | 47 (57.1) | 0 |

  All four A0 values are in the A0 set. Run "long" used the first version of pipe.c, which printed no
  chaining-value index (the computation is the same; the listed pipe.c adds the per-CV histograms and the index);
  "long2" repeats it with the listed program and new seeds. Over all runs the row-17 passes total 156 against
  148.4 predicted from the SMC's row-17 factor 2^-17.000 (6.2; ratio 1.05); in runs a, b and long2 (82 passes) no chaining value had
  two row-17 passes. Bucket sizes (runs a, b, long2: 3.2 x 10^7 buckets): largest 104; the distribution is
  concentrated on multiples of 4 because the A2 values of one c9 class share row 16 for the same A1.
- **The counted program on true buckets.** For A0 = 3662dd58 and 400 real chaining values, pipe.c (with a dump
  option) lists every row-16 variant (2,326 entries); the counted program run on exactly these buckets gives the
  same entry, W7-pass and first-row-17-test counts as the reference construction on every chaining value.

### 6.4 Groups, the pair term and the caps

- **Events.** In a group the program examines every variant v = (A0_j, A1, A2) with (A1, A2) in R_j, j = 1..256,
  on the group's CV1: it finds every v whose row 16 holds (Lemma 5, 4.5) and tests W7 and rows 17..37 exactly.
  n = SR = 2^37.48061 variants per group.
- **One group.** S = sum_v Pr[A(CV1, v)] >= SR p2 q3_model = 2^-68.42135 (H1, H2). Groups use fresh coins, so they
  are independent and identically distributed. Inside a group the events are not assumed independent. Let N be the
  number of variants v of the group with A_v. By the Bonferroni inequality Pr[N >= 1] >= E[N] - E[N(N - 1)]/2, and
  E[N(N - 1)] = sum_v Pr[A_v] E[N - 1 | A_v]. H5 bounds the average of E[N - 1 | A_v] under the weights Pr[A_v], the
  expected number of further successes in the group seen from a success, by delta = 1. Hence Pr[N >= 1] >=
  E[N] (1 - delta/2) >= S/2 = q_lb. No bound for each pair separately is needed. The measured values (6.5) are at most
  0.0018 for variants not sharing (A0, A1) with v and 2.4 x 10^-6 for those sharing it, about 500 times below the
  budget.
- **Groups.** N_G = ceil(0.504182 / q_lb) = 398,563,284,869,814,990,705 (2^68.43337); 0.504182 is -ln(1 - 0.396)
  rounded up at the 6th decimal, about 2% more than the 0.494296 that 0.39 requires, so the success bound tolerates
  a 2.0% (0.0286-bit) shortfall of the expected number of successes per group. Pr[no group succeeds] <=
  exp(-N_G q_lb) <= exp(-0.504182).
- **Caps.** Per group the counters lie in [0, 256 x 344,064] (Lemma 6). Their expectations: E[NE] = SR 2^-27 =
  2^10.48061 (4.5, H1), E[NW] = E[NE] p2 (W7 is independent of (W0, W1) for a fixed variant), E[N1] = E[NW] 2^-10 (E17^x
  is uniform given rows 16 and W7, Lemma 4). NE_MAX = ceil(N_G E[NE] (1 + 2^-6)), NW_MAX = ceil(N_G E[NW] (1 + 2^-5)),
  N1_MAX = ceil(N_G E[N1] (1 + 3)). Hoeffding over the N_G independent groups bounds the overflow probabilities by
  exp(-51,211,458), exp(-916,660) and exp(-8,056). The margins 1.6% and 3.1% exceed the measured deviations of the
  bucket size (at most 0.07%) and the W7 rate (at most 0.2%) on real first blocks by a factor of more than 10.
- **Success.** Pr[output] >= 1 - exp(-0.504182) - exp(-51,211,458) - exp(-916,660) - exp(-8,056) = 0.3960005 > 0.39.
- **Sensitivity of the success bound.** With N_G fixed, the bound stays >= 0.39 if the true S (1 - delta/2) is at least
  98% of the modelled S/2. With the measured pair term (delta <= 0.0079) that holds down to q3 = 2^-103.02, two bits
  below the measured 99% bounds (2^-101.0101 and 2^-101.0051); at q3_model it holds for delta up to 1.02, and at the
  measured q3 bound for delta up to 1.51.

### 6.5 Measuring the pair term (H5)

**Far variants** (R3 of PREREG_v3: far2.c and far_bound2.py, Appendix B.18 and B.19; outputs in Appendix A.6).
Conditioning sample: 513,481 tail successes of smc3 (seeds 23001..23120) whose tail variants are drawn from a uniform
sample of 2^18 variants of 8 A0 of the set (`varsample a0set8.txt 8 262144 20261012`): the four of largest |R| and four
drawn by a preregistered rule, two of them starting b6.. (pairwise Hamming distances 1 to 9; in the whole set 99.2% of
the pairs are at distance 1 to 9 and 263 of 32,640 at 10 or 11). Each success was rebuilt and verified as a 38-step semi-free-start collision
of its variant v on its CV1 (0 failures; the run's mean q3 estimate 2^-100.9997 agrees with 6.2); the pairs
(v, CV1) are the SMC's sample of a success weighted by Pr[A_v], the weighting of H5. For each, far2.c finds every
other variant w of the 8 R(A0) whose row 16 holds on the same CV1 (through phi^-1, as pipe.c), excluding v and the
variants sharing (A0, A1) with v, builds w's pair with the generic code, checks the A/E cells of rows 0..16 and W16,
and records W7 in F7, the first row-17 test, all of row 17 (cells, `+`, two-bit conditions) and any deeper row. Let
B_w be the event that row 16, W7 and row 17 of w hold. A_w implies B_w, so the number of far w with B_w bounds the
number of far w with A_w whatever the dependence beyond row 17. The same probes on 500,000 uniform chaining values
give the unconditional baseline.

| conditioning | far class | row-16 variants per CV | W7 rate (p2 = 2^-3.90197) | first row-17 test | row 17 (expected) |
|---|---|---|---|---|---|
| success of v | same A0, other A1 | 5.5735 | 2^-3.8833 | 203 | 2 (1.49) |
| success of v | other A0 (7) | 39.1093 | 2^-3.8963 | 1267 | 11 (10.35) |
| uniform CV1 | all 8 A0 | 44.6964 | 2^-3.8994 | 1464 | 12 (11.50) |

By the Hamming distance between the A0 of v and of w (pairs of A0 values; the same-A0 class is distance 0):

| distance | A0 pairs | row-16 variants per (success, A0 of w) | W7 rate | first-test rate | row 17 (expected) |
|---|---|---|---|---|---|
| 0..0 | 8 | 5.5735 | 2^-3.8833 | 2^-9.900 | 2 (1.49) |
| 1..3 | 14 | 5.6026 | 2^-3.8921 | 2^-10.086 | 3 (2.60) |
| 4..6 | 24 | 5.5815 | 2^-3.8950 | 2^-10.036 | 4 (4.46) |
| 7..9 | 18 | 5.5824 | 2^-3.9012 | 2^-10.059 | 4 (3.30) |

Expected values use far2.c's built-in row-17 rate 2^-16.991; at the measured 2^-17.000 (6.2) they are 0.6% lower.
0 cell mismatches in 45.3 x 10^6 constructed pairs. Given a success, far variants pass row 16 and row 17 at
rates consistent with the unconditional ones in every distance band (2 to 4 row-17 events per band against 1.5 to 4.5
expected; with so few events a band can only exclude a large enhancement, while the pooled count is 13 against 11.8);
their W7 rate is slightly raised, most for variants of v's own A0
(W7 = c7(w) - a shares a = A_{-1} with v). The bound does not need unconditional behaviour, since B_w includes W7.
No far variant passed beyond row 17. Extrapolation to the attack (one same-A0 class and 255 other A0 per success):
D_far = E_same + (255/7) E_other7; point estimate 0.00078; 99% bound 0.0016 (Poisson, 0.5% per class);
0.0018 seed-clustered (13 of 120 seeds had events, at most 1 in one seed; all events scaled by 255/7). The
preregistered rule kept a far term of 1/200 in the ledger (the clustered bound is below it); this version budgets the
whole pair term at delta = 1 instead (6.4), so the measurement is a check of the premise with a margin of about 500.

**Close variants** (same (A0, A1), other A2: at most 767 per variant). The clumping replay tries all of them on the
CV1 of every success of R1, R2 and R3: 0 further successes on 1,883,203 successes (22,199,766 trials). The 99% bound for the
expected number of further close successes per success is 4.61/1,883,203 = 2.4 x 10^-6. (The close variants of one
success number at most 767, so even with no measurement at all their contribution cannot exceed 767; the budget of 1
needs the measurement only for its far part.)

**Premise for real chaining values.** These measurements condition on semi-free-start successes, whose CV1 follows
the uniform model; the attack's CV1 = F_38(IV, M0). H5 therefore includes the premise that joint events of two
variants on a real chaining value behave as on a uniform one (H1 states this for one variant). There is no direct
measurement of this transfer at depth; the only real-chaining-value observation (runs a, b and long2: no chaining
value with two row-17 passes among 82, one A0 per run) excludes only a very large enhancement. The premise is the
pairwise analogue of H1 and is declared as part of H5. The conditioning sample is the SMC's particle approximation
of the success distribution, a further premise of the measurement.

## 7. Ledger (exact; cert.py, Appendix B.1)

```text
T = A_C + A_S + DEV + (pre + init + online + fin_ops) / C + N_G + fin_units
  A_C = 2^78 (characteristic search), A_S = 2^74 (Step-1 solve), DEV = 2^64 (all development)        [units]
  pre    = 466,412,701,031,896,270,852,028                (Section 5.1; P5 and P6 are counted code)
  init   = 1,024                                          (counters, constants, code pointers)
  online = N_G (64 + 256 x 30 + 15) + NE_MAX x 10 + NW_MAX x 66 + N1_MAX x (26 + 3,132)
           + 256 x 344,064 x (10 + 66 + 3,158)            (one group's overshoot of the caps)
         = 11,938,977,653,196,641,712,347,327
           NE_MAX = 578,375,349,533,157,559,511,618   NW_MAX = 39,285,380,938,092,027,141,708
           N1_MAX = 148,808,261,129,136,466,446
  N_G    = 398,563,284,869,814,990,705 first-block compressions                                        [units]
  fin    = 6 units + 1,024 operations (two messages, their three-block digests, output)
T = 2^78.109596  ->  claimed time_log2 = 78.12 (0.0104 bit of slack, 2^71.00 units)
allowances 2^78.08755; online (first blocks and online operations) 2^72.01600; preprocessing operations 2^67.21233
```

The allowances are 98.5% of T; everything else, the attack proper, is 2^72.07 units. Per (CV1, A0) the online word
operations are 117.0 at the caps: 30 for the block, 56.69 for the entries (5.6 per block), 25.41 for the W7 passes,
4.61 for first-test passes and deep paths (their cap is 4 times the expectation), 0.31 for the prologue and
epilogue; the first-block compression adds 2728/256 = 10.66 operation-equivalents.

**Sensitivity** (cert.ledger with one input changed; exact log2 T; N_G recomputed for the same success bound):

| change | log2 T |
|---|---|
| q3 at the smaller preregistered 99% bound 2^-101.0101 instead of q3_model (no q3 margin) | 78.09907 |
| q3 lower than q3_model by 1 / 2 bits | 78.13057 / 78.17162 |
| pair budget delta = 0.0079259 (the measured terms with margin, as in the second version) | 78.09904 |
| A_C = 2^80 instead of 2^78 | 80.02819 |
| the first version's allowances (2^64, 2^56, 2^56) | 72.07216 |
| no allowances (the attack alone) | 72.06675 |
| success bound 0.39 instead of 0.396 (no slack) | 78.10918 |
| 128 instead of 256 tables (top half of the A0 set) | 78.11102 |
| no table (bucket found through phi^-1: 3,072 probes of about 14 operations per (CV1, A0)) | about 80.68 |

## 8. Memory and advice

Memory (a reported metric): per table 2 x 2^64 words of headers and fill cursors, 32 x 2^32 x |R_j| entry words;
the R_j lists, the F7 word table (2^32 words), the A2 and G records and the program (256 blocks of at most 3,300
instructions): at most 2^75.0 words = 2^79.92 bytes at 32 bytes per word; claimed 2^80 bytes. The online attack
itself reads the tables and keeps 41 registers and a scratch area of 600 words. The nonuniform advice is the
characteristic, S*, the A2 list, the A0 set and G, below 2^13 bytes in all: the cell masks and values of the
characteristic (3 x 3 x 38 words and 38 `+` masks, 1,520 bytes), the two-bit conditions (about 40 x 7 bytes), S*
(3 x 16 words of each member, 384 bytes), the A0 set (1,024 bytes), the A2 list (3,072 bytes; also recomputed by P3),
G and F7's two constants (136 bytes), about 6.4 KB; the per-A0 blocks of the program are generated from these values
by the uniform generator of vt38.py. The characteristic and S* are charged by the
allowances A_C = 2^78 and A_S = 2^74; the A2 list and G are recomputed by P3 and P1; the A0 set (256 words) is advice whose
search is covered by the development allowance DEV (Section 9, H4).

## 9. Heuristics

**H1 - the chaining value of one trial (score-critical).** For one group, CV1 = F_38(IV, M0) with M0 uniform
behaves as a uniform 256-bit value as far as the events of one fixed variant are concerned: (Y, Z0) is uniform for
each A0 (so E[bucket size] = |R_j| 2^-27), W7 is uniform and independent of (W0, W1) (so W7 passes with p2), and the
second-block words have the distribution of 3.5 and Lemma 4. It is a statement about one trial (one first block
and one variant) at a time; nothing is assumed about two variants of one group (H5 covers that). Evidence: the
real-first-block runs of 6.3 (5.2 x 10^7 chaining values for four A0: entries per CV within 0.07% of the
prediction, W7 rates within 0.003 bit, row 17 156 passes against 148.4 predicted); the counted program on true
buckets (6.3); the organizer experiment `vt-ram-r38`, which checks the counted program's table index and W7
decisions on organizer-seeded real first blocks (a consistency check of the code and a witness count of W7
passes, not a statistical test). Sensitivity: the caps tolerate deviations of the expected bucket size and W7 rate
of 1.6% and 3.1%; the success bound tolerates a 2.0% shortfall of the per-group success rate at q3_model, about one
bit more with the measured pair term (6.4).
Limitations: a premise; the measured events have probability 2^-27 to 2^-48 per variant, not 2^-105.

**H2 - q3 for the variants (score-critical).** The average over the variants the program examines (uniform over
the union of the R_j) of q3(v) is at least q3_model = 2^-102. Evidence: Lemma 4 (rows 16..22 are the same for every
variant, so only the tail is averaged); the preregistered runs of 6.2 on independent streams: R1 over a uniform
2^20-variant sample (99% bound 2^-101.0101) and R2 over 256 fresh uniform variants (99% bound 2^-101.0051 for the
population mean); the 1,883,203 tail successes of these runs and of 6.5, each rebuilt and verified as a
semi-free-start collision of a random variant, none failed; the counted program accepts 4000 of 4000 of them (R4);
the tail factor of variants equals the published one; the row-17 rates on real first blocks; the organizer replica
`vt-q3-smc-r38` (10.1), whose pass threshold 2^-101.45 lies 0.55 bit above q3_model. Sensitivity: q3_model is about
one bit below both measured bounds; with the measured pair term the success bound holds down to q3 = 2^-103.02 at
the declared N_G, and lowering q3_model by one bit would cost 0.021 in T (Section 7). Limitations: Monte-Carlo bounds relying on the central limit theorem (64
and 256 estimates); q3 itself cannot be observed; the runs that preceded the seeding fix are superseded.

**H3 - table pricing (score-critical).** Under collision-frontier-v5 the online program is charged by its counted
primitives. The model's text: computation model "Classical probabilistic 256-bit word RAM. ... every other primitive
word operation costs 1/C units"; primitive operations "256-bit load or store", "addition/subtraction modulo 2^256",
"bitwise AND/OR/XOR/NOT", "shift or rotation", "comparison", "conditional branch", "independent uniform random
256-bit word"; memory scoring "Required and reviewed as a metric only; no scalar contribution and no tie-break". A load from any address therefore costs one
operation whatever the memory size, and the memory used (2^80 bytes) is reported, not scored. Every table word is
written by the counted preprocessing of 5.1 (2^67.21 units, charged in time, zero initialisation included).
Limitations: the tables are far beyond physical memory; without unit-cost table access the claim does not hold,
and the variant idea alone (buckets found through phi^-1 instead of a table) gives about 80.68.

**H4 - advice allowances (score-critical: they set T).** The characteristic, its two-bit conditions and S* are
advice. The cost model requires that "all construction/preprocessing and advice must be accounted for, including any
search omitted from the submitted program"; we read this as the total computation spent to obtain the advice,
failed and repeated searches and tool development included. It is charged at fixed, deliberately generous
allowances: A_C = 2^78 units for the characteristic search (its cost is not published), A_S = 2^74 for the Step-1
solve (the paper reports the time of that SAT solve as about 2^38.3 calls of the compression function, so A_S is
2^35.7 times the published figure), and DEV = 2^64 for all development of this package (recorded below 4.1 x 10^5
CPU-seconds, Section 11). Bound chain for A_C, every factor chosen generously: 10^5 CPU cores for 10 years at 10^10
256-bit word operations per second each (more than a core sustains; a SAT/SMT solver is scalar code) is 3.2 x 10^23
operations = 2^66.6 units; 10^4 GPUs for 10 years at 10^13 operations per second each, counting every 32-bit lane
operation as a 256-bit word operation, is 2^73.3 units. A_C = 2^78 exceeds the sum by a factor of about 26. The
search used an open-source CPU SAT/SMT tool [LLW24a] (ePrint 2026/1120, Section 3.1: "We still use the open-source
SAT/SMT-based tool [LLW24a] to search for SHA-2 differential characteristics"), and the authors' previous paper
[LLWS26] reports that no high-probability 38-step characteristic had been found, so failed searches are part of
what A_C covers. The same values are used by the earlier r38 packages (context, not evidence). The allowances are
98.5% of T and only overcharge: the attack proper costs 2^72.07, and a smaller true construction cost would only
lower T. Limitations: an allowance by a scale argument, not a measurement or a published figure; we did not rerun
the search. A characteristic search above 2^78 units would raise the claim (A_C = 2^80 gives 80.02819).

**H5 - the pair term (score-critical).** Let N be the number of successful variants in a group, whose chaining value
is that of a real first block. The expected number of further successes seen from a success,
sum_v Pr[A_v] E[N - 1 | A_v] / sum_v Pr[A_v], is at most delta = 1: on average a success does not bring more than one
further success on the same chaining value. This includes the premise that joint events of two variants on a real
chaining value behave as on a uniform one (H1 covers one variant). Support: (i) structure: a further success needs a
second variant whose own row 16 (probability 2^-27), W7 (2^-3.9) and rows 17..37 (about 2^-74) hold; variants
sharing (A0, A1) with v (at most 767) share W0, W1, W16 and row 16 but have different W2..W7, W10 and c7, and all
others differ in W1 or W0 and need their own W16 in G; under independence delta would be about 2^-68. (ii)
Measurements (6.5, preregistered, participant-run): on the chaining values of 513,481 verified successes of variants
of 8 A0 spread over the set, every far variant of the 8 A0 was tested exactly through row 17; rows 16 and 17 pass at
rates consistent with the unconditional ones (13 row-17 events against 11.8 expected), and the extrapolation to all
256 A0 gives 0.0018 (99%, seed-clustered); close variants gave 0 further successes on 1,883,203 successes (99% bound
2.4 x 10^-6); on real first blocks no chaining value had two row-17 passes. The budget is about 500 times the
measured value. Sensitivity: at q3_model the success bound holds for delta up to 1.02, at the measured q3 for delta
up to 1.51; with the measured value instead of the budget the claim would be 78.09904 (Section 7). Limitations: a
premise; the measurements are not executed by the organizer, the far term is measured for 8 A0 values and
extrapolated, and the transfer to real chaining values is supported only indirectly; the budget leaves a margin of
about 500 for all of these.

Not used: expected work, an independence-of-conditions model, independence inside a group, any property of the
published pair beyond its verified values.

## 10. Organizer experiments

`experiments/vt38.py` (65,431 bytes, sha256 70876be2b82e5629..., standard library) serves both experiments and contains the reference
construction, the counted program (online code and table-construction code) and the selftest
(`python3 vt38.py selftest`, output in Appendix A.1). Both experiments declare the full-collision event and are not
expected to produce one: the organizer-visible statistic is the number of returned pairs, and a pair is returned
only when the program's own checks pass (verified semi-free-start collisions in 10.1, a mismatch-free trial in 10.2);
the semi-free-start strings of 10.1 can be checked offline by anyone with the 38-step compression. The design was
frozen twice before validation: PREREG_exp.txt (2026-10-09T15:11:17Z, program 1e2658287123091d...) and, after the
advisory review, PREREG_exp_v2.txt (2026-10-09T15:44:43Z, program 8c0c2fb8f59ce815..., the shipped file). Both texts
are in Appendix A.4. The second version changes the counted program (group epilogue, table-construction code) and
makes vt-ram-r38 return its pair only for a mismatch-free trial; q3_experiment and everything it calls are unchanged,
and its output is byte-identical to the first version's on the six requests compared. The shipped third version
(after the first official review) only adds the counted variant enumeration of 5.1 and selftest item 10;
q3_experiment, ram_experiment and everything they call are unchanged, and on the ten requests replayed (six of
vt-q3-smc-r38, four of vt-ram-r38, including the public seed) its stdout equals the second version's byte for byte
(VALIDATION_v3.jsonl, Appendix A.4).

**Pass signals and offline checks.** The organizer-visible signals are the returned pairs and the observations:
vt-q3-smc-r38 passes iff trial 20 returns a pair (21 returned pairs; the runner sends all 256 trials of an
experiment in one request, so trial 20 sees trials 0..19); vt-ram-r38 passes iff all 256 trials return a pair and
the reported W7 passes total lies between 457 and 639 (548 +- 4 binomial standard deviations). full_collisions = 0 is
expected for both: the declared event kind is the repository's only one, full-collision, which these experiments do
not produce. The 96-byte strings of vt-q3-smc-r38 are checkable offline: bytes 0..31 are CV1 as eight big-endian
words, bytes 32..95 one message block (16 big-endian words), and the 38-step compression function from CV1
(feed-forward included, no padding) gives equal outputs for the two strings. The 128-byte strings of vt-ram-r38 are
M0 || M1 and M0 || M1' of one variant (not a collision): their first blocks are equal and their second blocks
differ in W7 by 2^29.

### 10.1 vt-q3-smc-r38 (H2)

Trials 0..19 each run one reduced replicate of the estimator of 6.2 (NP 64; 128, 4, 4, 1, 1, 1 children at rows
17..22; 512 tail proposals per particle with the W23 x-value cells and its four two-bit conditions imposed; variants
drawn from the 512 embedded variants, the first 512 of the uniform sample of 6.2; randomness from Python's
random.Random seeded with SHAKE-256 of the trial seed). Trial 20 uses the estimates of trials 0..19, which the
runner supplies in the same request (all 256 trials of an experiment are one request). Every tail success is rebuilt and accepted only under the checks of 6.2. Trial t < 20 returns its first
accepted pair as the 96-byte strings CV1 || M1 and CV1 || M1'; trial 20 returns a pair iff all 20 trials had a
success, all were accepted, and the mean of the 20 estimates is at least 2^-101.45; trials 21..255 return none.
The threshold: on 1,120 development replicates (mean 2^-100.9827, relative sd 0.338, 76,695 tail successes, all
accepted) the 0.0001 bootstrap quantile of a mean of 20 is 2^-101.404; by that bootstrap a true q3 lower by 0.4 /
0.55 / 0.7 bit would fail the rule with probability 0.45 / 0.90 / 0.996 (a gamma model with relative sd 0.338 gives
0.28 / 0.79 / 0.987). It is therefore a sanity check of the estimator at about 0.4-bit
resolution on organizer seeds. With q3_model = 2^-102, 1.02 bit below the development mean, a true q3 as low as
q3_model would fail the rule with probability above 0.996: a pass on organizer seeds is trusted evidence that q3 is
above q3_model at the replica's resolution. The precise bounds rest on the samples of 6.2.
Validation: first version, own seeds `vt-validation-0..24`: every request returned exactly 21 pairs, pooled means
2^-101.219 .. 2^-100.805, 34,384 tail successes, all accepted; second version, `vt-validation2-0..9`: 21 pairs each,
pooled means 2^-101.261 .. 2^-100.910, all successes accepted; on `vt-validation-0..4` and the public seed its
stdout is byte-identical to the first version's. Public-seed emulation: 21 pairs, pooled mean 2^-100.846, 1,443
successes, all accepted. Byte-identical replays everywhere; at most 4.1 s alone, 9.9 s with 8 runs in parallel.

### 10.2 vt-ram-r38 (H1, counted program)

Per organizer seed: two 256-bit words from SHAKE-256 of the seed are the program's two RAND outputs; the counted
program's prologue unpacks M0 and computes CV1; then 32 A0 blocks (indices 32t .. 32t+31 mod 256) run with a table
oracle whose bucket holds one entry, the embedded valid variant of that A0 (in general not a row-16 hit), and the
group epilogue and loop run once. Checks: M0 is the unpack of the two words; CV1 equals the reference compression;
every block requests the index (Y, Z0) that the reference computes from (CV1, A0) (Lemma 5); the program enters its
row-17 path exactly for the entries whose reference W7 is in F7, and its W17 equals the reference pair's. Returns
(M0 || M1, M0 || M1') of the first block's variant (128 bytes each; never a collision) only if every check passed.
It tests the counted program's arithmetic on organizer inputs and gives a witness count of W7 passes; it does not
exercise the tables (Section 5.3 and 6.3 cover the table semantics and true buckets). Predicted: 256 returned pairs
(no mismatch), about 548 W7 passes. Validation, second version (4 own requests): 256 pairs each, mismatches 0, W7
passes 548, 568, 532, 528; public-seed emulation: 256 pairs, 573 W7 passes; byte-identical replays.

## 11. Runs and hashes

All runs on one Apple-silicon Mac (16 cores) on 2026-10-09; C programs compiled with `cc -O3` (the PREREG_v3 programs with
`-O3 -march=native`; their runs used 14 parallel processes or threads). Hashes are SHA-256
(first 16 hex digits); the printed programs are in Appendix B, the data files (a0set256.txt = Appendix A.2, G = 4.4)
and the preregistration texts and results in Appendix A.

| run | what | CPU-seconds | outputs |
|---|---|---:|---|
| variant counts | exploration programs (A0, A1, A2, A3 varied alone with the generic test of core.h; 64 random A0; all A2 at one A0), not printed; their results are reproduced by lib.h (enum_v) and a0exact.c | about 4,000 s | valid A1 at the published A0: 923,932 |
| A0 search | v9all.c (histograms of the A0-free part of W8 over all A2; 2^33.211 pairs), local search, a0exact.c (exact |R(A0)| for 3,000 candidates) | about 6,000 s | a0set256.txt 9c84fdfbc724c637 |
| G, F7, phi | gset.c (32), fset.c (287,309,824), phimax.c (max 14) | about 30 s | G.txt 789e71d06549216e |
| real first blocks | pipe.c: long (first version), a, b, long2; pipe_dump (dump option) and truebucket.py for the true-bucket check | about 60,000 s | Section 6.3 |
| SMC development | smc.c (published dense part), smc2.c, 30 seeds (not in the sample) | about 200 s | - |
| SMC preregistered, first version (superseded: overlapping streams) | smc2.c e1f653c3ab1345d1, 64 seeds | about 400 s | RESULTS.txt 77f890d691e0f0d2 |
| variant dispersion (superseded) | smc_het (smc2.c with a fixed-variant argument), 48 variants, seeds 5000..5047 | about 300 s | - |
| replica development | 1,120 replicates | about 200 s | threshold 2^-101.45 |
| experiment validation | emu.py: runner seed protocol of experiments/runner.py, program run twice, outputs validated as the runner does, pairs checked with the repository digest | about 500 s | VALIDATION.jsonl 991a348ed10c50bf, PUBLIC_SEED.jsonl ee34fa5df2170f69, VALIDATION_v2.jsonl (A.4) |
| superseded third-version runs (overlapping streams) | smc_het seeds 7000..7255; smc2.c seeds 3001..3120 (4 A0); far.c, far_bound.py | about 4,700 s | A.4 |
| PREREG_v3 R1..R4 | run_v3.sh: smc3.c (R1 64, R2 256, R3 120 runs), varsample, far2.c on 8 A0 with 500,000 uniform CV1, far_bound2.py, ram_check.py | about 9,000 s | 6.2, 6.5, A.5, A.6 |
| third version | selftest (item 10), emu.py replays of ten requests | about 100 s | VALIDATION_v3.jsonl (A.4) |
| advisory reviews | four fresh-context critics on the exported review packet (no execution), for the first and for the third version | - | addressed in this version |

The listed runs total about 8.6 x 10^4 CPU-seconds; the declared bound 4.1 x 10^5 CPU-seconds also covers unlisted
short runs (compilation, tests, the advisory critics' arithmetic). At 10^10 word operations per second (2^21.8 units
per CPU-second) it is 2^40.5 units, far inside DEV. No run was discarded. Docker was not available on the
development machine, so the experiments were run with the local Python 3.13 interpreter under `-I` (the organizer
runs Python 3.12 in its sandbox; both experiments use only `random.Random`, `hashlib`, `struct`, `zlib`, `base64` and
`json`, whose outputs do not differ between these versions for the calls used). smc3.c is the file frozen by PREREG_v3 and
is printed unchanged; its comment "Lemma V2" refers to Lemma 4 of this file.

## 12. Limitations and differences from the paper

1. The success probability rests on H1, H2, H5 and the cost on H3 and H4; Lemmas 3-7 and all counts are exact.
2. The claim is set by the advice allowances (H4): the attack proper costs 2^72.07 (about 2^70.2 without the margins
   on q3 and on the pair term). Measured or published costs that allowed A_C, A_S and DEV of 2^64, 2^56 and 2^56 would
   lower it to 72.07216.
3. The tables are enormous (2^80 bytes): the claim is a time bound in the word-RAM model of the track, not a
   practical memory budget. The variant idea is independent of the tables (see the sensitivity table).
4. The paper's attack uses one Step-1 solution and (W14, W15) freedom; this one keeps the published A3..A13 and
   (W14, W15) and uses (A0, A1, A2). We did not rerun the paper's SAT solve or characteristic search.
5. Earlier r38 packages' q3 estimate (for the published S) and ours (for the variants) agree; ours was computed
   independently with new code, but with the same estimator design.

## Appendix A. Data

### A.1 Selftest output (`python3 experiments/vt38.py selftest`)

```text
1 published pair collides, rows 16..37 hold: True
2 G: 32 values, 32 pass row 16
3 A2 list: 768 distinct values, 0 violate the A2-only conditions
4 invalid embedded variants: 0 of 256, 0 of 512
5 variant soundness, 300 random chaining values: 0 mismatches
6 counted program on the semi-free-start vectors: 4 of 4 found and verified
7 ops: group prologue + epilogue + loop 79 (+1 unit), empty block 29, block with 3 entries (W7 False) 60
8 physical registers: 41
9 table build, toy A0 index 0: 7 variants, 256 buckets (largest 4), 0 mismatches; ops per (Y, variant): count 211, fill 275; per header: zero 4, prefix 10
9 table build, toy A0 index 5: 34 variants, 320 buckets (largest 16), 0 mismatches; ops per (Y, variant): count 211, fill 275; per header: zero 4, prefix 10
10 variant enumeration, toy A0 index 0: 8192 candidates, 112 valid, 0 mismatches; ops: setup 42, outer 8, per candidate <= 67, per valid +25 (executed 228883 <= 551664)
10 variant enumeration, toy A0 index 5: 8192 candidates, 492 valid, 0 mismatches; ops: setup 42, outer 8, per candidate <= 67, per valid +25 (executed 263793 <= 561164)
SELFTEST OK
```

### A.2 The A0 set (j = 1..256: A0_j and |R_j|; the file a0set256.txt read by cert.py has these two columns)

```text
  1 3662dd58 750798738    2 3662dd50 750798738    3 3662bd50 750798738    4 36629d50 750798738
  5 36627d58 750798738    6 36627d50 750798738    7 36625d58 750798738    8 36625d50 750798738
  9 36623d58 750798738   10 36623d50 750798738   11 36621d58 750798738   12 36621d50 750798738
 13 3661fd58 750798738   14 3661fd50 750798738   15 3661dd58 750798738   16 3661dd50 750798738
 17 3661bd58 750798738   18 3661bd50 750798738   19 36619d58 750798738   20 36619d50 750798738
 21 36617d58 750798738   22 36617d50 750798738   23 36615d58 750798738   24 36615d50 750798738
 25 36613d58 750798738   26 36613d50 750798738   27 36611d58 750798738   28 36611d50 750798738
 29 3660fd58 750798738   30 3660fd50 750798738   31 b662dd50 750367881   32 b6629d50 750367881
 33 b6625d50 750367881   34 b6623d50 750367881   35 b6621d58 750367881   36 b6621d50 750367881
 37 b661fd50 750367881   38 b661dd50 750367881   39 b661bd50 750367881   40 b6619d50 750367881
 41 b6617d50 750367881   42 b6615d58 750367881   43 b6615d50 750367881   44 b6613d58 750367881
 45 b6613d50 750367881   46 b6611d58 750367881   47 b6611d50 750367881   48 b660fd58 750367881
 49 b660fd50 750367881   50 3660bd58 749907870   51 3660bd50 749907870   52 b660bd50 749607325
 53 3660dd58 749434566   54 3660dd50 749434566   55 366add58 749306678   56 366add50 749306678
 57 366abd58 749306678   58 366abd50 749306678   59 366a9d58 749306678   60 366a9d50 749306678
 61 366a7d50 749306678   62 366a5d58 749306678   63 366a5d50 749306678   64 366a3d50 749306678
 65 366a1d58 749306678   66 366a1d50 749306678   67 3669fd50 749306678   68 3669dd58 749306678
 69 3669dd50 749306678   70 3669bd50 749306678   71 36699d50 749306678   72 36697d50 749306678
 73 36695d58 749306678   74 36695d50 749306678   75 36693d58 749306678   76 36693d50 749306678
 77 36691d58 749306678   78 36691d50 749306678   79 3668fd58 749306678   80 3668fd50 749306678
 81 3662dd56 749304379   82 3662dd4e 749304379   83 3662bd56 749304379   84 3662bd4e 749304379
 85 36627d56 749304379   86 36627d4e 749304379   87 36625d4e 749304379   88 36623d56 749304379
 89 36623d4e 749304379   90 36621d56 749304379   91 36621d4e 749304379   92 3661fd56 749304379
 93 3661fd4e 749304379   94 3661dd56 749304379   95 3661dd4e 749304379   96 3661bd56 749304379
 97 3661bd4e 749304379   98 36619d56 749304379   99 36619d4e 749304379  100 36617d56 749304379
101 36617d4e 749304379  102 36615d56 749304379  103 36615d4e 749304379  104 36613d56 749304379
105 36613d4e 749304379  106 36611d56 749304379  107 36611d4e 749304379  108 3660fd56 749304379
109 3660fd4e 749304379  110 3668bd50 749092986  111 b66add58 748997270  112 b66add50 748997270
113 b66abd50 748997270  114 b66a9d58 748997270  115 b66a9d50 748997270  116 b66a7d50 748997270
117 b66a5d58 748997270  118 b66a5d50 748997270  119 b66a3d58 748997270  120 b66a3d50 748997270
121 b66a1d58 748997270  122 b66a1d50 748997270  123 b669fd58 748997270  124 b669fd50 748997270
125 b669dd58 748997270  126 b669dd50 748997270  127 b669bd50 748997270  128 b6699d58 748997270
129 b6699d50 748997270  130 b6697d50 748997270  131 b6695d50 748997270  132 b6693d50 748997270
133 b6691d58 748997270  134 b6691d50 748997270  135 b668fd50 748997270  136 3662fd58 748982994
137 3662fd50 748982994  138 b6623d4e 748863932  139 b6621d4e 748863932  140 b661fd56 748863932
141 b661bd4e 748863932  142 b6617d56 748863932  143 b6617d4e 748863932  144 b6615d4e 748863932
145 b6613d56 748863932  146 b6613d4e 748863932  147 b6611d56 748863932  148 b6611d4e 748863932
149 b660fd56 748863932  150 b660fd4e 748863932  151 3662dd52 748706771  152 3662bd52 748706771
153 36627d52 748706771  154 36625d52 748706771  155 36623d52 748706771  156 36621d52 748706771
157 3661fd52 748706771  158 3661dd52 748706771  159 3661bd52 748706771  160 36619d52 748706771
161 36617d52 748706771  162 36615d52 748706771  163 36613d52 748706771  164 36611d52 748706771
165 3660fd52 748706771  166 36623d5a 748706531  167 3661fd5a 748706531  168 3661bd5a 748706531
169 36617d5a 748706531  170 36615d5a 748706531  171 36613d5a 748706531  172 36611d5a 748706531
173 3660fd5a 748706531  174 3668dd58 748617938  175 3668dd50 748617938  176 3662fd56 748515751
177 3662fd4e 748515006  178 3660dd4e 748497055  179 3660dd56 748496687  180 b668dd50 748328226
181 b6613d5a 748272092  182 b660fd5a 748272092  183 b6623d52 748271884  184 b6621d52 748271884
185 b661bd52 748271884  186 b6617d52 748271884  187 b6615d52 748271884  188 b6613d52 748271884
189 b6611d52 748271884  190 b660fd52 748271884  191 3662dd54 748258600  192 3662bd54 748258600
193 36627d54 748258600  194 36625d54 748258600  195 36623d54 748258600  196 36621d54 748258600
197 3661fd54 748258600  198 3661dd54 748258600  199 3661bd54 748258600  200 36619d54 748258600
201 36617d54 748258600  202 36615d54 748258600  203 36613d54 748258600  204 36611d54 748258600
205 3660fd54 748258600  206 3662dd4c 748258590  207 3662bd4c 748258590  208 36627d4c 748258590
209 36625d4c 748258590  210 36623d4c 748258590  211 36621d4c 748258590  212 3661fd4c 748258590
213 3661dd4c 748258590  214 3661bd4c 748258590  215 36619d4c 748258590  216 36617d4c 748258590
217 36615d4c 748258590  218 36613d4c 748258590  219 36611d4c 748258590  220 3660fd4c 748258590
221 36623d5c 748257912  222 3661bd5c 748257912  223 36617d5c 748257912  224 36615d5c 748257912
225 36613d5c 748257912  226 36611d5c 748257912  227 3660fd5c 748257912  228 366add56 748249397
229 366add4e 748249397  230 366abd4e 748249397  231 366a9d4e 748249397  232 366a5d4e 748249397
233 366a3d4e 748249397  234 366a1d4e 748249397  235 3669fd56 748249397  236 3669dd4e 748249397
237 3669bd4e 748249397  238 36697d56 748249397  239 36697d4e 748249397  240 36695d4e 748249397
241 36693d56 748249397  242 36693d4e 748249397  243 36691d56 748249397  244 36691d4e 748249397
245 3668fd56 748249397  246 3668fd4e 748249397  247 b660dd56 748149584  248 36631d58 748119330
249 36631d50 748119330  250 3660dd5a 748106455  251 3660dd52 748104487  252 3660bd56 748016615
253 3660bd4e 748016615  254 3668dd4e 747975479  255 3668dd56 747975119  256 366afd58 747959736
```

### A.3 The A2 list (768 values, in increasing order)

```text
379b2dc8 379b2dc9 379b2dcc 379b2dcd 379b4dc8 379b4dc9 379b4dcc 379b4dcd 37bb2dc8 37bb2dc9 37bb2dcc 37bb2dcd
37bb4dc8 37bb4dc9 37bb4dcc 37bb4dcd 381b2cc8 381b2cc9 381b2ccc 381b2ccd 381b30c8 381b30c9 381b30cc 381b30cd
381b4cc8 381b4cc9 381b4ccc 381b4ccd 381b50c8 381b50c9 381b50cc 381b50cd 383b2cc8 383b2cc9 383b2ccc 383b2ccd
383b30c8 383b30c9 383b30cc 383b30cd 383b4cc8 383b4cc9 383b4ccc 383b4ccd 383b50c8 383b50c9 383b50cc 383b50cd
399b2dc8 399b2dc9 399b2dcc 399b2dcd 399b4dc8 399b4dc9 399b4dcc 399b4dcd 39bb2dc8 39bb2dc9 39bb2dcc 39bb2dcd
39bb4dc8 39bb4dc9 39bb4dcc 39bb4dcd 3a1b2cc8 3a1b2cc9 3a1b2ccc 3a1b2ccd 3a1b30c8 3a1b30c9 3a1b30cc 3a1b30cd
3a1b4cc8 3a1b4cc9 3a1b4ccc 3a1b4ccd 3a1b50c8 3a1b50c9 3a1b50cc 3a1b50cd 3a3b2cc8 3a3b2cc9 3a3b2ccc 3a3b2ccd
3a3b30c8 3a3b30c9 3a3b30cc 3a3b30cd 3a3b4cc8 3a3b4cc9 3a3b4ccc 3a3b4ccd 3a3b50c8 3a3b50c9 3a3b50cc 3a3b50cd
479b2dc8 479b2dc9 479b2dcc 479b2dcd 479b4dc8 479b4dc9 479b4dcc 479b4dcd 47bb2dc8 47bb2dc9 47bb2dcc 47bb2dcd
47bb4dc8 47bb4dc9 47bb4dcc 47bb4dcd 481b2cc8 481b2cc9 481b2ccc 481b2ccd 481b30c8 481b30c9 481b30cc 481b30cd
481b4cc8 481b4cc9 481b4ccc 481b4ccd 481b50c8 481b50c9 481b50cc 481b50cd 483b2cc8 483b2cc9 483b2ccc 483b2ccd
483b30c8 483b30c9 483b30cc 483b30cd 483b4cc8 483b4cc9 483b4ccc 483b4ccd 483b50c8 483b50c9 483b50cc 483b50cd
499b2dc8 499b2dc9 499b2dcc 499b2dcd 499b4dc8 499b4dc9 499b4dcc 499b4dcd 49bb2dc8 49bb2dc9 49bb2dcc 49bb2dcd
49bb4dc8 49bb4dc9 49bb4dcc 49bb4dcd 4a1b2cc8 4a1b2cc9 4a1b2ccc 4a1b2ccd 4a1b30c8 4a1b30c9 4a1b30cc 4a1b30cd
4a1b4cc8 4a1b4cc9 4a1b4ccc 4a1b4ccd 4a1b50c8 4a1b50c9 4a1b50cc 4a1b50cd 4a3b2cc8 4a3b2cc9 4a3b2ccc 4a3b2ccd
4a3b30c8 4a3b30c9 4a3b30cc 4a3b30cd 4a3b4cc8 4a3b4cc9 4a3b4ccc 4a3b4ccd 4a3b50c8 4a3b50c9 4a3b50cc 4a3b50cd
579b2dc8 579b2dc9 579b2dcc 579b2dcd 579b4dc8 579b4dc9 579b4dcc 579b4dcd 57bb2dc8 57bb2dc9 57bb2dcc 57bb2dcd
57bb4dc8 57bb4dc9 57bb4dcc 57bb4dcd 581b2cc8 581b2cc9 581b2ccc 581b2ccd 581b30c8 581b30c9 581b30cc 581b30cd
581b4cc8 581b4cc9 581b4ccc 581b4ccd 581b50c8 581b50c9 581b50cc 581b50cd 583b2cc8 583b2cc9 583b2ccc 583b2ccd
583b30c8 583b30c9 583b30cc 583b30cd 583b4cc8 583b4cc9 583b4ccc 583b4ccd 583b50c8 583b50c9 583b50cc 583b50cd
599b2dc8 599b2dc9 599b2dcc 599b2dcd 599b4dc8 599b4dc9 599b4dcc 599b4dcd 59bb2dc8 59bb2dc9 59bb2dcc 59bb2dcd
59bb4dc8 59bb4dc9 59bb4dcc 59bb4dcd 5a1b2cc8 5a1b2cc9 5a1b2ccc 5a1b2ccd 5a1b30c8 5a1b30c9 5a1b30cc 5a1b30cd
5a1b4cc8 5a1b4cc9 5a1b4ccc 5a1b4ccd 5a1b50c8 5a1b50c9 5a1b50cc 5a1b50cd 5a3b2cc8 5a3b2cc9 5a3b2ccc 5a3b2ccd
5a3b30c8 5a3b30c9 5a3b30cc 5a3b30cd 5a3b4cc8 5a3b4cc9 5a3b4ccc 5a3b4ccd 5a3b50c8 5a3b50c9 5a3b50cc 5a3b50cd
679b2dc8 679b2dc9 679b2dcc 679b2dcd 679b4dc8 679b4dc9 679b4dcc 679b4dcd 67bb2dc8 67bb2dc9 67bb2dcc 67bb2dcd
67bb4dc8 67bb4dc9 67bb4dcc 67bb4dcd 681b2cc8 681b2cc9 681b2ccc 681b2ccd 681b30c8 681b30c9 681b30cc 681b30cd
681b4cc8 681b4cc9 681b4ccc 681b4ccd 681b50c8 681b50c9 681b50cc 681b50cd 683b2cc8 683b2cc9 683b2ccc 683b2ccd
683b30c8 683b30c9 683b30cc 683b30cd 683b4cc8 683b4cc9 683b4ccc 683b4ccd 683b50c8 683b50c9 683b50cc 683b50cd
699b2dc8 699b2dc9 699b2dcc 699b2dcd 699b4dc8 699b4dc9 699b4dcc 699b4dcd 69bb2dc8 69bb2dc9 69bb2dcc 69bb2dcd
69bb4dc8 69bb4dc9 69bb4dcc 69bb4dcd 6a1b2cc8 6a1b2cc9 6a1b2ccc 6a1b2ccd 6a1b30c8 6a1b30c9 6a1b30cc 6a1b30cd
6a1b4cc8 6a1b4cc9 6a1b4ccc 6a1b4ccd 6a1b50c8 6a1b50c9 6a1b50cc 6a1b50cd 6a3b2cc8 6a3b2cc9 6a3b2ccc 6a3b2ccd
6a3b30c8 6a3b30c9 6a3b30cc 6a3b30cd 6a3b4cc8 6a3b4cc9 6a3b4ccc 6a3b4ccd 6a3b50c8 6a3b50c9 6a3b50cc 6a3b50cd
779b2dc8 779b2dc9 779b2dcc 779b2dcd 779b4dc8 779b4dc9 779b4dcc 779b4dcd 77bb2dc8 77bb2dc9 77bb2dcc 77bb2dcd
77bb4dc8 77bb4dc9 77bb4dcc 77bb4dcd 781b2cc8 781b2cc9 781b2ccc 781b2ccd 781b30c8 781b30c9 781b30cc 781b30cd
781b4cc8 781b4cc9 781b4ccc 781b4ccd 781b50c8 781b50c9 781b50cc 781b50cd 783b2cc8 783b2cc9 783b2ccc 783b2ccd
783b30c8 783b30c9 783b30cc 783b30cd 783b4cc8 783b4cc9 783b4ccc 783b4ccd 783b50c8 783b50c9 783b50cc 783b50cd
799b2dc8 799b2dc9 799b2dcc 799b2dcd 799b4dc8 799b4dc9 799b4dcc 799b4dcd 79bb2dc8 79bb2dc9 79bb2dcc 79bb2dcd
79bb4dc8 79bb4dc9 79bb4dcc 79bb4dcd 7a1b2cc8 7a1b2cc9 7a1b2ccc 7a1b2ccd 7a1b30c8 7a1b30c9 7a1b30cc 7a1b30cd
7a1b4cc8 7a1b4cc9 7a1b4ccc 7a1b4ccd 7a1b50c8 7a1b50c9 7a1b50cc 7a1b50cd 7a3b2cc8 7a3b2cc9 7a3b2ccc 7a3b2ccd
7a3b30c8 7a3b30c9 7a3b30cc 7a3b30cd 7a3b4cc8 7a3b4cc9 7a3b4ccc 7a3b4ccd 7a3b50c8 7a3b50c9 7a3b50cc 7a3b50cd
879b2dc8 879b2dc9 879b2dcc 879b2dcd 879b4dc8 879b4dc9 879b4dcc 879b4dcd 87bb2dc8 87bb2dc9 87bb2dcc 87bb2dcd
87bb4dc8 87bb4dc9 87bb4dcc 87bb4dcd 881b2cc8 881b2cc9 881b2ccc 881b2ccd 881b30c8 881b30c9 881b30cc 881b30cd
881b4cc8 881b4cc9 881b4ccc 881b4ccd 881b50c8 881b50c9 881b50cc 881b50cd 883b2cc8 883b2cc9 883b2ccc 883b2ccd
883b30c8 883b30c9 883b30cc 883b30cd 883b4cc8 883b4cc9 883b4ccc 883b4ccd 883b50c8 883b50c9 883b50cc 883b50cd
899b2dc8 899b2dc9 899b2dcc 899b2dcd 899b4dc8 899b4dc9 899b4dcc 899b4dcd 89bb2dc8 89bb2dc9 89bb2dcc 89bb2dcd
89bb4dc8 89bb4dc9 89bb4dcc 89bb4dcd 8a1b2cc8 8a1b2cc9 8a1b2ccc 8a1b2ccd 8a1b30c8 8a1b30c9 8a1b30cc 8a1b30cd
8a1b4cc8 8a1b4cc9 8a1b4ccc 8a1b4ccd 8a1b50c8 8a1b50c9 8a1b50cc 8a1b50cd 8a3b2cc8 8a3b2cc9 8a3b2ccc 8a3b2ccd
8a3b30c8 8a3b30c9 8a3b30cc 8a3b30cd 8a3b4cc8 8a3b4cc9 8a3b4ccc 8a3b4ccd 8a3b50c8 8a3b50c9 8a3b50cc 8a3b50cd
979b2dc8 979b2dc9 979b2dcc 979b2dcd 979b4dc8 979b4dc9 979b4dcc 979b4dcd 97bb2dc8 97bb2dc9 97bb2dcc 97bb2dcd
97bb4dc8 97bb4dc9 97bb4dcc 97bb4dcd 981b2cc8 981b2cc9 981b2ccc 981b2ccd 981b30c8 981b30c9 981b30cc 981b30cd
981b4cc8 981b4cc9 981b4ccc 981b4ccd 981b50c8 981b50c9 981b50cc 981b50cd 983b2cc8 983b2cc9 983b2ccc 983b2ccd
983b30c8 983b30c9 983b30cc 983b30cd 983b4cc8 983b4cc9 983b4ccc 983b4ccd 983b50c8 983b50c9 983b50cc 983b50cd
999b2dc8 999b2dc9 999b2dcc 999b2dcd 999b4dc8 999b4dc9 999b4dcc 999b4dcd 99bb2dc8 99bb2dc9 99bb2dcc 99bb2dcd
99bb4dc8 99bb4dc9 99bb4dcc 99bb4dcd 9a1b2cc8 9a1b2cc9 9a1b2ccc 9a1b2ccd 9a1b30c8 9a1b30c9 9a1b30cc 9a1b30cd
9a1b4cc8 9a1b4cc9 9a1b4ccc 9a1b4ccd 9a1b50c8 9a1b50c9 9a1b50cc 9a1b50cd 9a3b2cc8 9a3b2cc9 9a3b2ccc 9a3b2ccd
9a3b30c8 9a3b30c9 9a3b30cc 9a3b30cd 9a3b4cc8 9a3b4cc9 9a3b4ccc 9a3b4ccd 9a3b50c8 9a3b50c9 9a3b50cc 9a3b50cd
a79b2dc8 a79b2dc9 a79b2dcc a79b2dcd a79b4dc8 a79b4dc9 a79b4dcc a79b4dcd a7bb2dc8 a7bb2dc9 a7bb2dcc a7bb2dcd
a7bb4dc8 a7bb4dc9 a7bb4dcc a7bb4dcd a81b2cc8 a81b2cc9 a81b2ccc a81b2ccd a81b30c8 a81b30c9 a81b30cc a81b30cd
a81b4cc8 a81b4cc9 a81b4ccc a81b4ccd a81b50c8 a81b50c9 a81b50cc a81b50cd a83b2cc8 a83b2cc9 a83b2ccc a83b2ccd
a83b30c8 a83b30c9 a83b30cc a83b30cd a83b4cc8 a83b4cc9 a83b4ccc a83b4ccd a83b50c8 a83b50c9 a83b50cc a83b50cd
a99b2dc8 a99b2dc9 a99b2dcc a99b2dcd a99b4dc8 a99b4dc9 a99b4dcc a99b4dcd a9bb2dc8 a9bb2dc9 a9bb2dcc a9bb2dcd
a9bb4dc8 a9bb4dc9 a9bb4dcc a9bb4dcd aa1b2cc8 aa1b2cc9 aa1b2ccc aa1b2ccd aa1b30c8 aa1b30c9 aa1b30cc aa1b30cd
aa1b4cc8 aa1b4cc9 aa1b4ccc aa1b4ccd aa1b50c8 aa1b50c9 aa1b50cc aa1b50cd aa3b2cc8 aa3b2cc9 aa3b2ccc aa3b2ccd
aa3b30c8 aa3b30c9 aa3b30cc aa3b30cd aa3b4cc8 aa3b4cc9 aa3b4ccc aa3b4ccd aa3b50c8 aa3b50c9 aa3b50cc aa3b50cd
```

### A.4 Preregistrations, results and validation

PREREG_v3.txt (sha256 6ba6bc72570e76e572f713005ae96306ef5577ba5f282372d20f1bc297db1edb; the runs of Section 6.2 and 6.5):

```text
PREREG_v3.txt - frozen 2026-10-09T17:28:36Z, before any of the runs below.
Reason: the advisory review of the third version found that smc2.c (and smc_het) seed with seed0 * phi + 1 while the
splitmix64 step is phi, so consecutive seeds are one-draw shifts of one stream and the earlier SMC replicates (seeds
1001..1064, 5000..5047, 7000..7255, 3001..3120) are not independent.  smc3.c hashes seed0 through the splitmix64
finalizer; everything else is unchanged.  These runs replace the earlier ones as evidence for H2 and H5.
Programs (sha256): smc3.c 389af9738dacd0f6ebf36ebc96ae7dbcd8cd2d99b67eb41e0b845bb75122aeda; far2.c c3a7f1f6f7d85ccb1196d4abf669c8c213428693ffe90b7eea1431513e10cbfd; far_bound2.py 6297af48cd78ac7ddfc644c5ee83520db54203f896e8ad58c9072929ce4742f6; ram_check.py 7ef608537082cb50db878cc101f012c5b88efc624a414640b1631111f46225f6; varsample.c 3f4a151b94770857651b4a19a88a2b4728d6fe28edb2801b452495b6af9b4c50; lib.h 9b0103e54ebd8d9da0a12a20d156245690667e00073c17aa7d1348c639110ffb; core.h ad23214b4e8073fe72a2ea77ba18697f6cf8fa844e39bf4961054168bf223d52; consts.h d0ae82752982ce98020315037e5e5e12672344015e4a83fe41c975aef43b6d58; twobit.h 8ede00cf73dd69079d872b52520eca0997ecd081636c2ea809cc66c4147d277d; vt38.py 70876be2b82e5629fa0d594dbdff111e85071bfc11eb5fb91e7b14cb0f91225c
Data (sha256): vs256.bin b64cbc8952bc4b9a0b5ef61f61142de3747c895b036709c6e2b67fc41c2bc64b; a0set256.txt 9c84fdfbc724c637ac6caf3748b6b647aa6e1c1462714cdcad668d842adfc0b6; a0set8.txt 1a187ebd007da4f158225e500c17ec2698556ef16891bdf6f49a093ea767d2d4; G.txt 789e71d06549216e23d580aaa9af06f77ebff5b1932726caa7f2dcb6121e622f; F7.bm 65f2090b3e87be9c6ede2edf1eb07331d419f5648d5ca0ce1272758497221269
a0set8.txt rule: the four A0 of largest |R| (a0set4) plus random.Random(20261009).sample of 2 from the other 182 A0
starting 36.. and 2 from the 70 A0 starting b6...
Compiled with cc -O3 -march=native; all runs on the development Mac, 14 parallel processes or threads.
R1 (H2, fixed uniform 2^20 variant sample): ./smc3 s 4000 2048 64 64 8 8 4 8192 vs256.bin pre3/s, s = 21001..21064.
   Rule: LB1 = mean(Z) - 2.3870 sd(Z)/8 (one-sided 99%, Student 63 df).
R2 (H2, population): ./varsample a0set256.txt 256 256 20261011 vsP.bin (256 fresh uniform variants); then
   ./smc3 22000+i 4000 2048 64 64 8 8 4 8192 vsP.bin pop3/p i, i = 0..255 (run i uses only variant i).
   Rule: LB2 = mean(Z) - 2.3411 sd(Z)/16 (one-sided 99%, Student 255 df).
   Use: q3_model = 2^-102 stays if min(LB1, LB2) >= 2^-102; otherwise q3_model = 2^(floor(100 log2 min(LB1, LB2))/100 - 1).
R3 (H5): ./varsample a0set8.txt 8 262144 20261012 vs8.bin; ./smc3 s 4000 2048 64 64 8 8 4 8192 vs8.bin h53/s,
   s = 23001..23120; then BASE=500000 RECOUT=far3_rec.txt MATOUT=far3_mat.txt ./far2 a0set8.txt h53/*.sfs;
   python3 far_bound2.py far3_rec.txt far3_mat.txt.
   Use: the ledger's far term stays 1/200 if the seed-clustered bound is <= 1/200, else it becomes the smallest 1/2^k
   at least that bound.  Close term: the clumping replay of R1, R2 and R3 (0 further successes expected); the ledger
   keeps 767 x 2^-18 if the 99% bound 4.61/(successes) (or, with events, the Poisson 99% bound) is below it.
R4 (counted program vs the SMC success test): python3 ram_check.py 4000 20261013 pop3/*.sfs.
   Rule: every sampled success must be found by the counted program and verified; any failure is reported.
All seeds and all outputs are reported in full (proof.md Appendix A).
```

PREREG.txt (first version; superseded, its runs used overlapping streams, Section 6.2) (sha256 785c86d04b0b3dcc83682b5bdc90a9815c11c5d7082a5c2ab054805fb723c802):

```text
Preregistration of the q3 estimate (variant-averaged), written 2026-10-09T14:50:03Z before any listed seed is run.
Program: smc2.c (sha256 e1f653c3ab1345d14ebebb8434be51e5810b28c9d637c3393bec33599bc2a698), headers lib.h 9b0103e54ebd8d9d core.h ad23214b4e8073fe consts.h d0ae82752982ce98 twobit.h 8ede00cf73dd6907
Data: G.txt 789e71d06549216e, F7.bm 65f2090b3e87be9c, variant sample vs256.bin b64cbc8952bc4b9a (2^20 variants drawn uniformly from the union of R(A0) over a0set256.txt 9c84fdfbc724c637)
Parameters: NP 4000, children per particle rows 17..22 = 2048 64 64 8 8 4, MT 8192 tail proposals per particle.
Seeds: 1001 .. 1064 (64 seeds), every one reported.
Rule: Z_s = per-seed estimate (linear).  LB = mean(Z) - t sd(Z)/sqrt(64), t = 2.3870 (one-sided 99% Student, 63 df).
q3_model = 2^(floor(100 log2 LB)/100).  Also reported: every tail success rebuilt as a verified 38-step SFS collision
(rebuilt-bad must be 0), and the clumping replay counts (successes among other A2 valid with the same (A0, A1)).
```

RESULTS.txt (sha256 77f890d691e0f0d25..., one line per preregistered seed; Z is the linear estimate, stages are log2 stage factors for rows 16..22 and the tail, "clump" is successes/trials of the replay):

```text
seed 1002 NP 4000: log2 q3 = -101.0291  Z = 3.865439e-31  stages: -27.000 -16.975 -13.006 -15.025 -6.000 -7.003 -1.000 -15.020  tail 4223 rebuilt-bad 0 clump 0/51848
seed 1004 NP 4000: log2 q3 = -100.9979  Z = 3.950175e-31  stages: -27.000 -17.003 -13.010 -14.991 -6.000 -7.003 -1.000 -14.990  tail 4310 rebuilt-bad 0 clump 0/51587
seed 1003 NP 4000: log2 q3 = -101.0257  Z = 3.874592e-31  stages: -27.000 -16.985 -13.001 -15.017 -6.000 -7.003 -1.000 -15.018  tail 4227 rebuilt-bad 0 clump 0/51356
seed 1001 NP 4000: log2 q3 = -101.0006  Z = 3.942763e-31  stages: -27.000 -16.988 -13.009 -15.025 -6.000 -7.003 -1.000 -14.976  tail 4353 rebuilt-bad 0 clump 0/53528
seed 1007 NP 4000: log2 q3 = -100.9570  Z = 4.063580e-31  stages: -27.000 -16.984 -13.001 -14.984 -6.000 -7.003 -1.000 -14.986  tail 4323 rebuilt-bad 0 clump 0/52774
seed 1006 NP 4000: log2 q3 = -101.0445  Z = 3.824455e-31  stages: -27.000 -16.989 -13.008 -15.002 -6.000 -7.003 -1.000 -15.042  tail 4157 rebuilt-bad 0 clump 0/51359
seed 1008 NP 4000: log2 q3 = -101.0510  Z = 3.807193e-31  stages: -27.000 -16.993 -13.013 -15.027 -6.000 -7.003 -1.000 -15.015  tail 4237 rebuilt-bad 0 clump 0/52041
seed 1005 NP 4000: log2 q3 = -101.0156  Z = 3.901892e-31  stages: -27.000 -16.988 -13.011 -15.020 -6.000 -7.003 -1.000 -14.993  tail 4301 rebuilt-bad 0 clump 0/52407
seed 1009 NP 4000: log2 q3 = -101.0357  Z = 3.847864e-31  stages: -27.000 -16.979 -13.002 -15.030 -6.000 -7.003 -1.000 -15.022  tail 4217 rebuilt-bad 0 clump 0/51647
seed 1011 NP 4000: log2 q3 = -100.9951  Z = 3.957736e-31  stages: -27.000 -16.990 -12.999 -14.991 -6.000 -7.003 -1.000 -15.013  tail 4244 rebuilt-bad 0 clump 0/52456
seed 1010 NP 4000: log2 q3 = -100.9601  Z = 4.054880e-31  stages: -27.000 -16.982 -13.002 -14.982 -6.000 -7.003 -1.000 -14.991  tail 4308 rebuilt-bad 0 clump 0/53277
seed 1012 NP 4000: log2 q3 = -101.0234  Z = 3.880945e-31  stages: -27.000 -16.985 -13.003 -15.007 -6.000 -7.003 -1.000 -15.024  tail 4210 rebuilt-bad 0 clump 0/51929
seed 1013 NP 4000: log2 q3 = -100.9938  Z = 3.961255e-31  stages: -27.000 -16.979 -13.004 -14.993 -6.000 -7.003 -1.000 -15.015  tail 4238 rebuilt-bad 0 clump 0/51966
seed 1014 NP 4000: log2 q3 = -100.9805  Z = 3.998021e-31  stages: -27.000 -16.987 -13.002 -14.984 -6.000 -7.003 -1.000 -15.005  tail 4267 rebuilt-bad 0 clump 0/50722
seed 1015 NP 4000: log2 q3 = -100.9990  Z = 3.946997e-31  stages: -27.000 -16.992 -13.000 -15.016 -6.000 -7.003 -1.000 -14.988  tail 4318 rebuilt-bad 0 clump 0/52720
seed 1016 NP 4000: log2 q3 = -101.0483  Z = 3.814365e-31  stages: -27.000 -16.980 -13.000 -15.023 -6.000 -7.003 -1.000 -15.042  tail 4157 rebuilt-bad 0 clump 0/51599
seed 1017 NP 4000: log2 q3 = -101.0017  Z = 3.939593e-31  stages: -27.000 -16.996 -13.009 -14.984 -6.000 -7.003 -1.000 -15.010  tail 4251 rebuilt-bad 0 clump 0/51911
seed 1018 NP 4000: log2 q3 = -101.0129  Z = 3.909320e-31  stages: -27.000 -16.988 -13.005 -14.960 -6.000 -7.003 -1.000 -15.056  tail 4118 rebuilt-bad 0 clump 0/50143
seed 1019 NP 4000: log2 q3 = -101.0480  Z = 3.815221e-31  stages: -27.000 -16.988 -13.000 -15.009 -6.000 -7.003 -1.000 -15.048  tail 4140 rebuilt-bad 0 clump 0/50524
seed 1020 NP 4000: log2 q3 = -101.0247  Z = 3.877432e-31  stages: -27.000 -16.992 -13.005 -15.022 -6.000 -7.003 -1.000 -15.002  tail 4275 rebuilt-bad 0 clump 0/52620
seed 1021 NP 4000: log2 q3 = -100.9662  Z = 4.037864e-31  stages: -27.000 -16.988 -13.003 -14.977 -6.000 -7.003 -1.000 -14.995  tail 4296 rebuilt-bad 0 clump 0/52075
seed 1022 NP 4000: log2 q3 = -100.9985  Z = 3.948525e-31  stages: -27.000 -16.992 -13.009 -15.000 -6.000 -7.003 -1.000 -14.994  tail 4298 rebuilt-bad 0 clump 0/53488
seed 1023 NP 4000: log2 q3 = -100.9697  Z = 4.027954e-31  stages: -27.000 -16.985 -13.007 -14.978 -6.000 -7.003 -1.000 -14.996  tail 4292 rebuilt-bad 0 clump 0/51640
seed 1024 NP 4000: log2 q3 = -100.9704  Z = 4.026016e-31  stages: -27.000 -16.990 -13.003 -14.998 -6.000 -7.003 -1.000 -14.977  tail 4351 rebuilt-bad 0 clump 0/53529
seed 1025 NP 4000: log2 q3 = -101.0221  Z = 3.884473e-31  stages: -27.000 -16.989 -13.008 -14.997 -6.000 -7.003 -1.000 -15.025  tail 4209 rebuilt-bad 0 clump 0/51735
seed 1026 NP 4000: log2 q3 = -101.0409  Z = 3.834128e-31  stages: -27.000 -16.997 -13.012 -15.028 -6.000 -7.003 -1.000 -15.000  tail 4280 rebuilt-bad 0 clump 0/52188
seed 1027 NP 4000: log2 q3 = -101.0683  Z = 3.761902e-31  stages: -27.000 -16.996 -13.000 -14.992 -6.000 -7.003 -1.000 -15.077  tail 4060 rebuilt-bad 0 clump 0/50124
seed 1028 NP 4000: log2 q3 = -100.9988  Z = 3.947629e-31  stages: -27.000 -16.986 -13.000 -14.995 -6.000 -7.003 -1.000 -15.014  tail 4239 rebuilt-bad 0 clump 0/52149
seed 1029 NP 4000: log2 q3 = -100.9982  Z = 3.949172e-31  stages: -27.000 -16.989 -13.007 -14.981 -6.000 -7.003 -1.000 -15.018  tail 4229 rebuilt-bad 0 clump 0/52009
seed 1030 NP 4000: log2 q3 = -101.0288  Z = 3.866289e-31  stages: -27.000 -17.002 -13.003 -15.000 -6.000 -7.003 -1.000 -15.021  tail 4220 rebuilt-bad 0 clump 0/51354
seed 1031 NP 4000: log2 q3 = -100.9519  Z = 4.078012e-31  stages: -27.000 -16.992 -13.000 -14.976 -6.000 -7.003 -1.000 -14.981  tail 4339 rebuilt-bad 0 clump 0/54100
seed 1032 NP 4000: log2 q3 = -101.0514  Z = 3.806206e-31  stages: -27.000 -16.993 -13.001 -14.996 -6.000 -7.003 -1.000 -15.059  tail 4110 rebuilt-bad 0 clump 0/51168
seed 1033 NP 4000: log2 q3 = -100.9957  Z = 3.956118e-31  stages: -27.000 -16.988 -13.008 -14.985 -6.000 -7.003 -1.000 -15.011  tail 4249 rebuilt-bad 0 clump 0/51937
seed 1034 NP 4000: log2 q3 = -100.9423  Z = 4.105158e-31  stages: -27.000 -16.993 -12.997 -14.980 -6.000 -7.003 -1.000 -14.969  tail 4375 rebuilt-bad 0 clump 0/53947
seed 1035 NP 4000: log2 q3 = -100.9903  Z = 3.971048e-31  stages: -27.000 -16.987 -13.008 -14.992 -6.000 -7.003 -1.000 -15.001  tail 4279 rebuilt-bad 0 clump 0/53366
seed 1036 NP 4000: log2 q3 = -100.9816  Z = 3.995050e-31  stages: -27.000 -16.987 -13.009 -14.985 -6.000 -7.003 -1.000 -14.997  tail 4291 rebuilt-bad 0 clump 0/52598
seed 1037 NP 4000: log2 q3 = -100.9841  Z = 3.987880e-31  stages: -27.000 -16.989 -13.000 -14.968 -6.000 -7.003 -1.000 -15.023  tail 4213 rebuilt-bad 0 clump 0/51540
seed 1038 NP 4000: log2 q3 = -101.0086  Z = 3.920942e-31  stages: -27.000 -16.996 -13.010 -14.976 -6.000 -7.003 -1.000 -15.023  tail 4213 rebuilt-bad 0 clump 0/51098
seed 1039 NP 4000: log2 q3 = -100.9978  Z = 3.950437e-31  stages: -27.000 -16.987 -13.009 -15.016 -6.000 -7.003 -1.000 -14.982  tail 4334 rebuilt-bad 0 clump 0/53171
seed 1040 NP 4000: log2 q3 = -100.9885  Z = 3.975751e-31  stages: -27.000 -16.989 -13.003 -14.997 -6.000 -7.003 -1.000 -14.996  tail 4294 rebuilt-bad 0 clump 0/52698
seed 1041 NP 4000: log2 q3 = -100.9990  Z = 3.947020e-31  stages: -27.000 -16.986 -12.995 -15.014 -6.000 -7.003 -1.000 -15.001  tail 4277 rebuilt-bad 0 clump 0/52069
seed 1042 NP 4000: log2 q3 = -100.9852  Z = 3.985103e-31  stages: -27.000 -16.985 -12.999 -14.991 -6.000 -7.003 -1.000 -15.008  tail 4259 rebuilt-bad 0 clump 0/52840
seed 1043 NP 4000: log2 q3 = -100.9346  Z = 4.127100e-31  stages: -27.000 -16.990 -13.013 -14.992 -6.000 -7.003 -1.000 -14.936  tail 4474 rebuilt-bad 0 clump 0/55780
seed 1044 NP 4000: log2 q3 = -100.9885  Z = 3.975796e-31  stages: -27.000 -16.993 -13.007 -15.010 -6.000 -7.003 -1.000 -14.976  tail 4352 rebuilt-bad 0 clump 0/53230
seed 1045 NP 4000: log2 q3 = -101.0211  Z = 3.887021e-31  stages: -27.000 -17.000 -13.003 -14.991 -6.000 -7.003 -1.000 -15.025  tail 4207 rebuilt-bad 0 clump 0/51321
seed 1047 NP 4000: log2 q3 = -100.9649  Z = 4.041495e-31  stages: -27.000 -17.002 -13.006 -14.980 -6.000 -7.003 -1.000 -14.974  tail 4359 rebuilt-bad 0 clump 0/52647
seed 1046 NP 4000: log2 q3 = -100.9466  Z = 4.092930e-31  stages: -27.000 -17.003 -13.005 -14.965 -6.000 -7.003 -1.000 -14.971  tail 4368 rebuilt-bad 0 clump 0/52850
seed 1048 NP 4000: log2 q3 = -100.9568  Z = 4.064140e-31  stages: -27.000 -16.995 -12.998 -14.984 -6.000 -7.003 -1.000 -14.976  tail 4352 rebuilt-bad 0 clump 0/53562
seed 1049 NP 4000: log2 q3 = -100.9790  Z = 4.002066e-31  stages: -27.000 -16.998 -13.002 -14.979 -6.000 -7.003 -1.000 -14.997  tail 4291 rebuilt-bad 0 clump 0/52543
seed 1050 NP 4000: log2 q3 = -100.9974  Z = 3.951420e-31  stages: -27.000 -16.989 -13.002 -14.989 -6.000 -7.003 -1.000 -15.014  tail 4239 rebuilt-bad 0 clump 0/53054
seed 1052 NP 4000: log2 q3 = -101.0222  Z = 3.884048e-31  stages: -27.000 -16.999 -13.005 -15.009 -6.000 -7.003 -1.000 -15.005  tail 4265 rebuilt-bad 0 clump 0/52331
seed 1051 NP 4000: log2 q3 = -101.0006  Z = 3.942728e-31  stages: -27.000 -16.997 -13.010 -14.992 -6.000 -7.003 -1.000 -15.000  tail 4282 rebuilt-bad 0 clump 0/52346
seed 1053 NP 4000: log2 q3 = -100.9385  Z = 4.116029e-31  stages: -27.000 -16.987 -13.002 -14.973 -6.000 -7.003 -1.000 -14.974  tail 4360 rebuilt-bad 0 clump 0/53165
seed 1054 NP 4000: log2 q3 = -101.0099  Z = 3.917284e-31  stages: -27.000 -17.000 -13.007 -14.987 -6.000 -7.003 -1.000 -15.013  tail 4243 rebuilt-bad 0 clump 0/52785
seed 1056 NP 4000: log2 q3 = -101.0247  Z = 3.877306e-31  stages: -27.000 -16.990 -12.997 -15.013 -6.000 -7.003 -1.000 -15.022  tail 4215 rebuilt-bad 0 clump 0/50708
seed 1055 NP 4000: log2 q3 = -101.0253  Z = 3.875739e-31  stages: -27.000 -16.997 -13.006 -14.992 -6.000 -7.003 -1.000 -15.027  tail 4203 rebuilt-bad 0 clump 0/51175
seed 1057 NP 4000: log2 q3 = -101.0561  Z = 3.794002e-31  stages: -27.000 -17.001 -13.003 -15.014 -6.000 -7.003 -1.000 -15.035  tail 4179 rebuilt-bad 0 clump 0/51523
seed 1060 NP 4000: log2 q3 = -101.0050  Z = 3.930553e-31  stages: -27.000 -16.993 -12.999 -14.987 -6.000 -7.003 -1.000 -15.022  tail 4215 rebuilt-bad 0 clump 0/51183
seed 1058 NP 4000: log2 q3 = -100.9695  Z = 4.028493e-31  stages: -27.000 -16.990 -13.006 -14.978 -6.000 -7.003 -1.000 -14.992  tail 4305 rebuilt-bad 0 clump 0/52753
seed 1059 NP 4000: log2 q3 = -100.9439  Z = 4.100594e-31  stages: -27.000 -16.992 -13.003 -14.945 -6.000 -7.003 -1.000 -15.001  tail 4279 rebuilt-bad 0 clump 0/52873
seed 1061 NP 4000: log2 q3 = -101.0065  Z = 3.926641e-31  stages: -27.000 -16.992 -13.007 -14.999 -6.000 -7.003 -1.000 -15.005  tail 4267 rebuilt-bad 0 clump 0/52072
seed 1062 NP 4000: log2 q3 = -100.9839  Z = 3.988435e-31  stages: -27.000 -17.000 -12.996 -14.996 -6.000 -7.003 -1.000 -14.989  tail 4314 rebuilt-bad 0 clump 0/52852
seed 1063 NP 4000: log2 q3 = -100.9629  Z = 4.047123e-31  stages: -27.000 -16.993 -13.005 -14.988 -6.000 -7.003 -1.000 -14.974  tail 4360 rebuilt-bad 0 clump 0/52635
seed 1064 NP 4000: log2 q3 = -100.9917  Z = 3.967121e-31  stages: -27.000 -17.001 -12.998 -15.006 -6.000 -7.003 -1.000 -14.983  tail 4333 rebuilt-bad 0 clump 0/53539
```

PREREG_exp.txt (sha256 10e3682caebd614e31ac72e4aa4a35ac4277cb50cd136fc1ff0f7c518b1cb82e):

```text
Freeze of the organizer experiments, written 2026-10-09T15:11:17Z before any validation run.
Program experiments/vt38.py sha256 1e2658287123091dca986a04cba17a3c215bea5aff744e094c5f8a9a63bb26f8 (54957 bytes).
vt-q3-smc-r38: K 20 replicates, NP 64, children 128 4 4 1 1 1 (rows 17..22), 512 tail proposals per particle, W23
x-value cells and the four W23 two-bit conditions imposed in the tail proposal, 512 embedded variants.  Pass rule of
trial 20: all 20 replicates have >= 1 tail success, every success rebuilt and accepted, mean of the 20 estimates
>= 2^-101.45 (from 1,120 development replicates: their mean-of-20 0.0001 bootstrap quantile is 2^-101.404).
Prediction: 21 returned pairs, 0 full collisions, failed_rebuilds 0.
vt-ram-r38: 32 A0 blocks per trial; prediction: 256 returned pairs, 0 full collisions, mismatches 0 in every trial,
about 548 W7 passes in total.
Validation: own seeds "vt-validation-<k>" (k = 0..24 for vt-q3-smc-r38, k = 0..3 for vt-ram-r38); every run reported.
```

PREREG_exp_v2.txt (sha256 1ab13d696eb499ec9aecf068f7f9dce41c0fa19c02cf425ee72306d00427aa64):

```text
Second freeze of the organizer experiments, written 2026-10-09T15:44:43Z after advisory review and before any
validation run of this version.  Program experiments/vt38.py sha256 8c0c2fb8f59ce8158b790047e70aacf8e2a4e6497d2b80c1d56a2920f85616e4 (60793 bytes).
Changes from the first freeze (program 1e2658287123091d...): the executed group program now contains the cap epilogue
and the group loop; the table-construction passes are added as counted code with a toy check in the selftest; the
interpreter reads unset registers as zero in every instruction; vt-ram-r38 returns its pair only if the trial has
no mismatch; comments.  q3_experiment and everything it calls are unchanged, so vt-q3-smc-r38's output must be
byte-identical to the first version's for the same request.
Predictions: vt-q3-smc-r38 21 returned pairs; vt-ram-r38 256 returned pairs (no mismatch), about 548 W7 passes.
Validation: own seeds "vt-validation2-<k>" (k = 0..9 for vt-q3-smc-r38, 0..3 for vt-ram-r38); the public seed; and the
first version's validation seeds vt-validation-0..4 for the byte-identity check of vt-q3-smc-r38.
```

Validation (emu.py; one line per request: experiment, seed, returned pairs, full collisions, byte-identical replay, mismatches, W7 passes, failed rebuilds, tail successes, pooled mean of trial 20):

```text
# first version (program 1e2658287123091d)
vt-q3-smc-r38  vt-validation-10         pairs  21 coll 0 replay same mis 0 w7   0 failed 0 tail  1365 -101.053
vt-q3-smc-r38  vt-validation-5          pairs  21 coll 0 replay same mis 0 w7   0 failed 0 tail  1275 -101.218
vt-q3-smc-r38  vt-validation-7          pairs  21 coll 0 replay same mis 0 w7   0 failed 0 tail  1415 -100.924
vt-q3-smc-r38  vt-validation-4          pairs  21 coll 0 replay same mis 0 w7   0 failed 0 tail  1328 -101.108
vt-q3-smc-r38  vt-validation-13         pairs  21 coll 0 replay same mis 0 w7   0 failed 0 tail  1326 -100.986
vt-q3-smc-r38  vt-validation-2          pairs  21 coll 0 replay same mis 0 w7   0 failed 0 tail  1392 -100.960
vt-q3-smc-r38  vt-validation-6          pairs  21 coll 0 replay same mis 0 w7   0 failed 0 tail  1372 -100.931
vt-q3-smc-r38  vt-validation-12         pairs  21 coll 0 replay same mis 0 w7   0 failed 0 tail  1395 -101.005
vt-q3-smc-r38  vt-validation-8          pairs  21 coll 0 replay same mis 0 w7   0 failed 0 tail  1332 -101.111
vt-q3-smc-r38  vt-validation-11         pairs  21 coll 0 replay same mis 0 w7   0 failed 0 tail  1439 -100.923
vt-q3-smc-r38  vt-validation-1          pairs  21 coll 0 replay same mis 0 w7   0 failed 0 tail  1359 -100.933
vt-q3-smc-r38  vt-validation-9          pairs  21 coll 0 replay same mis 0 w7   0 failed 0 tail  1375 -101.149
vt-q3-smc-r38  vt-validation-0          pairs  21 coll 0 replay same mis 0 w7   0 failed 0 tail  1372 -101.219
vt-q3-smc-r38  vt-validation-3          pairs  21 coll 0 replay same mis 0 w7   0 failed 0 tail  1380 -100.999
vt-ram-r38     vt-validation-0          pairs 256 coll 0 replay same mis 0 w7 516 failed 0 tail     0 
vt-ram-r38     vt-validation-1          pairs 256 coll 0 replay same mis 0 w7 561 failed 0 tail     0 
vt-ram-r38     vt-validation-2          pairs 256 coll 0 replay same mis 0 w7 571 failed 0 tail     0 
vt-ram-r38     vt-validation-3          pairs 256 coll 0 replay same mis 0 w7 564 failed 0 tail     0 
vt-q3-smc-r38  vt-validation-16         pairs  21 coll 0 replay same mis 0 w7   0 failed 0 tail  1391 -101.146
vt-q3-smc-r38  vt-validation-14         pairs  21 coll 0 replay same mis 0 w7   0 failed 0 tail  1332 -100.805
vt-q3-smc-r38  vt-validation-22         pairs  21 coll 0 replay same mis 0 w7   0 failed 0 tail  1319 -100.817
vt-q3-smc-r38  vt-validation-15         pairs  21 coll 0 replay same mis 0 w7   0 failed 0 tail  1393 -101.117
vt-q3-smc-r38  vt-validation-23         pairs  21 coll 0 replay same mis 0 w7   0 failed 0 tail  1375 -101.071
vt-q3-smc-r38  vt-validation-17         pairs  21 coll 0 replay same mis 0 w7   0 failed 0 tail  1378 -100.952
vt-q3-smc-r38  vt-validation-18         pairs  21 coll 0 replay same mis 0 w7   0 failed 0 tail  1409 -100.927
vt-q3-smc-r38  vt-validation-21         pairs  21 coll 0 replay same mis 0 w7   0 failed 0 tail  1368 -101.064
vt-q3-smc-r38  vt-validation-19         pairs  21 coll 0 replay same mis 0 w7   0 failed 0 tail  1413 -101.031
vt-q3-smc-r38  vt-validation-20         pairs  21 coll 0 replay same mis 0 w7   0 failed 0 tail  1454 -100.865
vt-q3-smc-r38  vt-validation-24         pairs  21 coll 0 replay same mis 0 w7   0 failed 0 tail  1427 -101.004
vt-q3-smc-r38  hashsmash-public-seed-v1 pairs  21 coll 0 replay same mis 0 w7   0 failed 0 tail  1443 -100.846
vt-ram-r38     hashsmash-public-seed-v1 pairs 256 coll 0 replay same mis 0 w7 573 failed 0 tail     0 
# second version (program 8c0c2fb8f59ce815)
vt-q3-smc-r38  vt-validation2-4         pairs  21 coll 0 replay same mis 0 w7   0 failed 0 tail  1370 -101.261
vt-q3-smc-r38  vt-validation2-5         pairs  21 coll 0 replay same mis 0 w7   0 failed 0 tail  1401 -100.958
vt-q3-smc-r38  vt-validation2-6         pairs  21 coll 0 replay same mis 0 w7   0 failed 0 tail  1385 -100.954
vt-q3-smc-r38  vt-validation2-2         pairs  21 coll 0 replay same mis 0 w7   0 failed 0 tail  1368 -100.926
vt-q3-smc-r38  vt-validation2-1         pairs  21 coll 0 replay same mis 0 w7   0 failed 0 tail  1415 -100.999
vt-q3-smc-r38  vt-validation2-3         pairs  21 coll 0 replay same mis 0 w7   0 failed 0 tail  1330 -101.113
vt-q3-smc-r38  vt-validation2-0         pairs  21 coll 0 replay same mis 0 w7   0 failed 0 tail  1334 -101.085
vt-q3-smc-r38  vt-validation2-7         pairs  21 coll 0 replay same mis 0 w7   0 failed 0 tail  1306 -100.910
vt-ram-r38     vt-validation2-1         pairs 256 coll 0 replay same mis 0 w7 568 failed 0 tail     0 
vt-ram-r38     vt-validation2-0         pairs 256 coll 0 replay same mis 0 w7 548 failed 0 tail     0 
vt-ram-r38     vt-validation2-3         pairs 256 coll 0 replay same mis 0 w7 528 failed 0 tail     0 
vt-ram-r38     vt-validation2-2         pairs 256 coll 0 replay same mis 0 w7 532 failed 0 tail     0 
vt-q3-smc-r38  vt-validation2-8         pairs  21 coll 0 replay same mis 0 w7   0 failed 0 tail  1386 -100.935
vt-q3-smc-r38  vt-validation2-9         pairs  21 coll 0 replay same mis 0 w7   0 failed 0 tail  1326 -100.983
vt-q3-smc-r38  vt-validation-1          pairs  21 coll 0 replay same mis 0 w7   0 failed 0 tail  1359 -100.933
vt-q3-smc-r38  vt-validation-0          pairs  21 coll 0 replay same mis 0 w7   0 failed 0 tail  1372 -101.219
vt-ram-r38     hashsmash-public-seed-v1 pairs 256 coll 0 replay same mis 0 w7 573 failed 0 tail     0 
vt-q3-smc-r38  vt-validation-2          pairs  21 coll 0 replay same mis 0 w7   0 failed 0 tail  1392 -100.960
vt-q3-smc-r38  vt-validation-3          pairs  21 coll 0 replay same mis 0 w7   0 failed 0 tail  1380 -100.999
vt-q3-smc-r38  vt-validation-4          pairs  21 coll 0 replay same mis 0 w7   0 failed 0 tail  1328 -101.108
vt-q3-smc-r38  hashsmash-public-seed-v1 pairs  21 coll 0 replay same mis 0 w7   0 failed 0 tail  1443 -100.846
# third version (program 70876be2b82e5629, shipped): replays of second-version requests, stdout compared
vt-q3-smc-r38  vt-validation2-0         pairs  21 coll 0 replay same mis 0 w7   0 failed 0 tail  1334 -101.085 stdout 1abaf705e868a1ff
vt-q3-smc-r38  vt-validation2-1         pairs  21 coll 0 replay same mis 0 w7   0 failed 0 tail  1415 -100.999 stdout b8b9b9e374820d28
vt-q3-smc-r38  vt-validation2-2         pairs  21 coll 0 replay same mis 0 w7   0 failed 0 tail  1368 -100.926 stdout 22c8021286d45d9b
vt-q3-smc-r38  vt-validation2-3         pairs  21 coll 0 replay same mis 0 w7   0 failed 0 tail  1330 -101.113 stdout 062cab93090214a5
vt-q3-smc-r38  hashsmash-public-seed-v1 pairs  21 coll 0 replay same mis 0 w7   0 failed 0 tail  1443 -100.846 stdout 8dadb14dcc0eb0f9
vt-q3-smc-r38  vt-validation-0          pairs  21 coll 0 replay same mis 0 w7   0 failed 0 tail  1372 -101.219 stdout 6b5620da7e7e2111
vt-ram-r38     vt-validation2-0         pairs 256 coll 0 replay same mis 0 w7 548 failed 0 tail     0  stdout 113cbd74a61dd482
vt-ram-r38     vt-validation2-1         pairs 256 coll 0 replay same mis 0 w7 568 failed 0 tail     0  stdout 397236a50417ad18
vt-ram-r38     vt-validation2-2         pairs 256 coll 0 replay same mis 0 w7 532 failed 0 tail     0  stdout 737e7804366d8f85
vt-ram-r38     hashsmash-public-seed-v1 pairs 256 coll 0 replay same mis 0 w7 573 failed 0 tail     0  stdout 02d81965545792ce
```

Superseded runs of the third version (overlapping streams): population run (smc_het, seeds 7000..7255, seed 7000 + i
used variant 17 + 4093 i of vs256.bin), log2 of the estimate per seed; then the 4-A0 far-pair run (far.c, far_bound.py).

```text
7000:-101.031 7001:-101.076 7002:-100.970 7003:-101.031 7004:-101.052 7005:-101.010 7006:-100.998 7007:-100.942
7008:-100.977 7009:-101.018 7010:-100.995 7011:-101.058 7012:-101.104 7013:-101.027 7014:-101.075 7015:-100.925
7016:-101.025 7017:-101.037 7018:-100.991 7019:-100.986 7020:-101.055 7021:-101.019 7022:-100.978 7023:-101.053
7024:-101.024 7025:-101.028 7026:-101.042 7027:-101.010 7028:-101.011 7029:-100.966 7030:-101.041 7031:-100.938
7032:-101.015 7033:-101.001 7034:-101.014 7035:-101.083 7036:-100.964 7037:-100.994 7038:-101.030 7039:-101.026
7040:-100.936 7041:-100.949 7042:-100.988 7043:-101.026 7044:-100.963 7045:-101.072 7046:-100.999 7047:-101.005
7048:-100.956 7049:-101.025 7050:-101.005 7051:-101.001 7052:-101.121 7053:-100.987 7054:-101.019 7055:-100.973
7056:-100.996 7057:-100.959 7058:-101.015 7059:-101.074 7060:-101.003 7061:-101.067 7062:-101.070 7063:-100.980
7064:-101.042 7065:-100.972 7066:-100.989 7067:-101.052 7068:-100.969 7069:-100.970 7070:-100.978 7071:-101.025
7072:-101.038 7073:-101.048 7074:-100.946 7075:-101.010 7076:-100.993 7077:-101.028 7078:-101.017 7079:-101.005
7080:-100.982 7081:-100.974 7082:-100.959 7083:-101.024 7084:-101.045 7085:-101.063 7086:-100.971 7087:-101.003
7088:-100.985 7089:-100.980 7090:-100.926 7091:-100.988 7092:-101.053 7093:-101.059 7094:-100.979 7095:-101.007
7096:-101.033 7097:-100.951 7098:-100.999 7099:-101.032 7100:-101.110 7101:-101.018 7102:-100.977 7103:-101.009
7104:-100.991 7105:-101.052 7106:-101.020 7107:-100.980 7108:-100.971 7109:-101.041 7110:-101.072 7111:-100.972
7112:-100.965 7113:-101.000 7114:-101.018 7115:-101.003 7116:-101.001 7117:-100.967 7118:-101.012 7119:-100.965
7120:-100.983 7121:-101.056 7122:-101.000 7123:-100.996 7124:-100.996 7125:-101.000 7126:-100.975 7127:-100.953
7128:-100.995 7129:-101.014 7130:-101.011 7131:-101.046 7132:-100.997 7133:-101.058 7134:-101.039 7135:-101.017
7136:-100.963 7137:-100.962 7138:-100.986 7139:-101.072 7140:-101.085 7141:-100.999 7142:-100.931 7143:-100.998
7144:-100.956 7145:-101.047 7146:-100.956 7147:-101.101 7148:-100.921 7149:-101.009 7150:-100.999 7151:-101.038
7152:-101.025 7153:-100.921 7154:-100.930 7155:-101.062 7156:-100.955 7157:-101.008 7158:-100.998 7159:-101.034
7160:-100.961 7161:-100.997 7162:-100.951 7163:-101.004 7164:-100.941 7165:-100.938 7166:-101.032 7167:-101.030
7168:-100.980 7169:-101.040 7170:-100.974 7171:-100.986 7172:-101.021 7173:-101.004 7174:-101.004 7175:-100.996
7176:-100.981 7177:-100.978 7178:-101.023 7179:-101.000 7180:-101.019 7181:-100.968 7182:-100.935 7183:-100.993
7184:-100.980 7185:-101.020 7186:-100.946 7187:-100.962 7188:-101.015 7189:-101.111 7190:-100.944 7191:-100.970
7192:-101.005 7193:-100.981 7194:-101.059 7195:-100.943 7196:-100.970 7197:-100.913 7198:-100.973 7199:-101.054
7200:-100.995 7201:-100.920 7202:-101.047 7203:-101.006 7204:-101.006 7205:-101.003 7206:-100.996 7207:-100.967
7208:-101.069 7209:-100.908 7210:-101.038 7211:-101.034 7212:-100.957 7213:-100.970 7214:-100.977 7215:-101.001
7216:-101.026 7217:-101.039 7218:-101.001 7219:-101.025 7220:-100.944 7221:-100.979 7222:-101.065 7223:-101.030
7224:-100.974 7225:-100.925 7226:-100.887 7227:-100.941 7228:-100.968 7229:-100.985 7230:-101.016 7231:-100.941
7232:-101.029 7233:-101.019 7234:-100.994 7235:-100.957 7236:-101.073 7237:-100.960 7238:-101.031 7239:-100.969
7240:-100.999 7241:-101.019 7242:-100.992 7243:-101.046 7244:-100.928 7245:-101.074 7246:-101.005 7247:-101.032
7248:-101.020 7249:-101.059 7250:-100.955 7251:-101.016 7252:-101.006 7253:-100.991 7254:-100.997 7255:-100.984
514246 successes
A0 3662dd58: |R| = 750798738
A0 3662dd50: |R| = 750798738
A0 3662bd50: |R| = 750798738
A0 36629d50: |R| = 750798738
conditional on a success of v [same A0, other A1]: CVs 514246, row-16 variants 2880487 (5.6014 per CV), cell mismatches 0; W7 195642 (rate 2^-3.8800, p2 2^-3.9020); first row-17 test 168 (rate 2^-10.186 given W7, exact 2^-10; expected 191.1); row 17 0 (expected 1.50 at 2^-16.991 of W7 passes); deepest rows:; full successes 0
conditional on a success of v [other A0]: CVs 514246, row-16 variants 8614782 (16.7523 per CV), cell mismatches 0; W7 580409 (rate 2^-3.8917, p2 2^-3.9020); first row-17 test 548 (rate 2^-10.049 given W7, exact 2^-10; expected 566.8); row 17 5 (expected 4.46 at 2^-16.991 of W7 passes); deepest rows: row17:5; full successes 0
baseline, random CV [same A0, other A1]: CVs 514246, row-16 variants 0 (0.0000 per CV), cell mismatches 0; W7 0 (rate 2^nan, p2 2^-3.9020); first row-17 test 0 (rate 2^nan given W7, exact 2^-10; expected 0.0); row 17 0 (expected 0.00 at 2^-16.991 of W7 passes); deepest rows:; full successes 0
baseline, random CV [other A0]: CVs 514246, row-16 variants 11491498 (22.3463 per CV), cell mismatches 0; W7 770345 (rate 2^-3.8989, p2 2^-3.9020); first row-17 test 788 (rate 2^-9.933 given W7, exact 2^-10; expected 752.3); row 17 6 (expected 5.91 at 2^-16.991 of W7 passes); deepest rows: row17:6; full successes 0
conditioning successes 514246; far row-17 passes: same A0 0, other A0 5, in 4 records (files [5, 24, 76, 77]), largest per record 2
D_far: point 0.000826; 99% upper bound (Poisson, 0.5% per class) 0.002349; record-clustered bound 0.004174; ledger value 1/200
```

### A.5 The preregistered SMC runs of PREREG_v3 (Section 6.2): v3_stats.py summaries and log2 of the estimate per seed

```text
v3_R1.log: 64 runs, mean 2^-101.0001, relative sd 0.0230, min 2^-101.0982, max 2^-100.9476, 99% bound 2^-101.0101
  stage means -27.000 -17.000 -13.000 -14.999 -6.000 -7.000 -1.000 -15.002 | stage sds 0.0000 0.0184 0.0052 0.0185 0.0000 0.0072 0.0000 0.0236
  tail successes 273712, failed rebuilds 0, clumping replay 0 further successes in 3341913 trials
v3_R2.log: 256 runs, mean 2^-100.9983, relative sd 0.0321, min 2^-101.1694, max 2^-100.8690, 99% bound 2^-101.0051
  stage means -27.000 -16.999 -13.000 -15.000 -6.000 -6.999 -1.000 -15.000 | stage sds 0.0000 0.0193 0.0051 0.0199 0.0000 0.0084 0.0000 0.0367
  tail successes 1096010, failed rebuilds 0, clumping replay 0 further successes in 12547972 trials
v3_R3_smc.log: 120 runs, mean 2^-100.9997, relative sd 0.0248, min 2^-101.1154, max 2^-100.9188, 99% bound 2^-101.0075
  stage means -27.000 -17.001 -13.000 -14.999 -6.000 -7.000 -1.000 -15.001 | stage sds 0.0000 0.0191 0.0053 0.0209 0.0000 0.0076 0.0000 0.0217
  tail successes 513481, failed rebuilds 0, clumping replay 0 further successes in 6309881 trials
# R1 (vs256.bin)
21001:-101.014 21002:-101.010 21003:-100.962 21004:-101.036 21005:-100.987 21006:-100.988 21007:-100.959 21008:-101.023
21009:-100.978 21010:-100.993 21011:-100.969 21012:-100.964 21013:-100.970 21014:-100.987 21015:-101.008 21016:-101.025
21017:-101.014 21018:-100.993 21019:-100.983 21020:-101.007 21021:-100.975 21022:-100.988 21023:-101.006 21024:-100.984
21025:-100.976 21026:-100.970 21027:-101.082 21028:-101.003 21029:-101.022 21030:-101.057 21031:-101.018 21032:-100.992
21033:-100.986 21034:-101.090 21035:-101.052 21036:-101.002 21037:-100.971 21038:-101.062 21039:-101.006 21040:-101.046
21041:-100.980 21042:-100.965 21043:-101.048 21044:-100.960 21045:-100.973 21046:-100.965 21047:-100.948 21048:-101.014
21049:-100.982 21050:-100.983 21051:-101.021 21052:-100.995 21053:-100.987 21054:-101.098 21055:-100.956 21056:-100.996
21057:-101.037 21058:-100.968 21059:-101.021 21060:-101.013 21061:-100.999 21062:-100.955 21063:-100.991 21064:-101.019
# R2 (seed 22000 + i uses variant i of vsP.bin)
22000:-100.991 22001:-101.059 22002:-100.888 22003:-101.038 22004:-101.018 22005:-100.910 22006:-101.004 22007:-100.970
22008:-101.025 22009:-100.938 22010:-101.028 22011:-100.945 22012:-101.075 22013:-101.077 22014:-100.990 22015:-101.009
22016:-100.886 22017:-100.999 22018:-100.988 22019:-100.974 22020:-100.969 22021:-101.009 22022:-101.048 22023:-101.081
22024:-101.017 22025:-101.002 22026:-101.086 22027:-101.033 22028:-101.023 22029:-100.933 22030:-101.045 22031:-101.032
22032:-101.083 22033:-100.909 22034:-100.956 22035:-100.986 22036:-100.976 22037:-101.055 22038:-100.992 22039:-100.919
22040:-100.994 22041:-100.989 22042:-101.015 22043:-101.007 22044:-101.016 22045:-101.019 22046:-100.952 22047:-100.946
22048:-101.038 22049:-101.022 22050:-101.001 22051:-100.968 22052:-100.927 22053:-100.968 22054:-101.040 22055:-101.035
22056:-101.031 22057:-100.987 22058:-101.028 22059:-101.031 22060:-100.971 22061:-101.015 22062:-100.980 22063:-100.945
22064:-100.953 22065:-100.989 22066:-100.911 22067:-100.955 22068:-100.959 22069:-100.963 22070:-101.038 22071:-101.055
22072:-101.064 22073:-100.979 22074:-100.962 22075:-101.003 22076:-100.989 22077:-100.981 22078:-101.018 22079:-101.024
22080:-100.989 22081:-101.010 22082:-101.060 22083:-100.973 22084:-100.918 22085:-100.961 22086:-100.998 22087:-101.026
22088:-101.063 22089:-100.939 22090:-101.002 22091:-101.039 22092:-101.011 22093:-100.956 22094:-100.925 22095:-101.015
22096:-101.023 22097:-100.952 22098:-100.986 22099:-100.959 22100:-101.039 22101:-100.983 22102:-100.974 22103:-100.965
22104:-101.028 22105:-101.003 22106:-101.035 22107:-100.973 22108:-100.950 22109:-100.962 22110:-100.869 22111:-100.989
22112:-101.031 22113:-100.989 22114:-101.016 22115:-100.975 22116:-100.939 22117:-100.983 22118:-101.085 22119:-101.064
22120:-100.954 22121:-101.041 22122:-100.985 22123:-100.944 22124:-100.972 22125:-100.985 22126:-101.056 22127:-101.037
22128:-100.972 22129:-101.013 22130:-101.095 22131:-101.047 22132:-100.996 22133:-100.964 22134:-100.974 22135:-100.945
22136:-100.945 22137:-100.924 22138:-101.044 22139:-100.984 22140:-101.022 22141:-101.033 22142:-100.985 22143:-100.954
22144:-100.966 22145:-100.999 22146:-100.914 22147:-100.989 22148:-100.942 22149:-101.032 22150:-101.042 22151:-101.087
22152:-101.019 22153:-101.029 22154:-100.992 22155:-101.076 22156:-101.038 22157:-100.989 22158:-101.014 22159:-101.020
22160:-100.983 22161:-100.987 22162:-100.996 22163:-100.991 22164:-101.028 22165:-100.996 22166:-101.104 22167:-100.990
22168:-100.929 22169:-100.999 22170:-101.028 22171:-101.045 22172:-100.956 22173:-101.018 22174:-101.060 22175:-100.968
22176:-101.122 22177:-101.039 22178:-101.040 22179:-100.998 22180:-101.057 22181:-101.042 22182:-100.982 22183:-100.938
22184:-101.022 22185:-101.052 22186:-100.973 22187:-101.035 22188:-100.974 22189:-100.938 22190:-101.032 22191:-100.986
22192:-101.029 22193:-100.992 22194:-100.984 22195:-100.986 22196:-100.988 22197:-100.984 22198:-100.964 22199:-100.965
22200:-100.941 22201:-101.051 22202:-100.984 22203:-100.978 22204:-100.984 22205:-101.074 22206:-100.970 22207:-100.955
22208:-101.041 22209:-100.987 22210:-101.007 22211:-100.923 22212:-101.101 22213:-101.016 22214:-101.078 22215:-100.987
22216:-101.113 22217:-101.096 22218:-101.022 22219:-100.982 22220:-100.974 22221:-101.021 22222:-101.037 22223:-101.006
22224:-101.017 22225:-100.994 22226:-100.964 22227:-100.962 22228:-100.962 22229:-100.983 22230:-101.025 22231:-100.963
22232:-100.961 22233:-100.994 22234:-101.035 22235:-100.944 22236:-101.084 22237:-100.991 22238:-100.991 22239:-100.953
22240:-101.012 22241:-100.970 22242:-101.010 22243:-101.046 22244:-100.992 22245:-100.962 22246:-100.992 22247:-100.948
22248:-101.051 22249:-100.917 22250:-100.939 22251:-101.041 22252:-101.014 22253:-101.169 22254:-101.051 22255:-100.887
```

### A.6 R3 and R4 of PREREG_v3 (Section 6.5, 6.2): outputs of far2.c (stderr, report, per-pair matrix), far_bound2.py and ram_check.py

```text
513481 successes
A0 3662dd58: |R| = 750798738
A0 3662dd50: |R| = 750798738
A0 3662bd50: |R| = 750798738
A0 36629d50: |R| = 750798738
A0 36691d4e: |R| = 748249397
A0 36693d50: |R| = 749306678
A0 b6613d5a: |R| = 748272092
A0 b660fd58: |R| = 750367881
conditional on a success of v [same A0, other A1]: CVs 513481, row-16 variants 2861894 (5.5735 per CV), cell mismatches 0; W7 193943 (rate 2^-3.8833, p2 2^-3.9020); first row-17 test 203 (rate 2^-9.900 given W7, exact 2^-10; expected 189.4); row 17 2 (expected 1.49 at 2^-16.991 of W7 passes); deepest rows: row17:2; full successes 0
conditional on a success of v [other A0]: CVs 513481, row-16 variants 20081905 (39.1093 per CV), cell mismatches 0; W7 1348672 (rate 2^-3.8963, p2 2^-3.9020); first row-17 test 1267 (rate 2^-10.056 given W7, exact 2^-10; expected 1317.1); row 17 11 (expected 10.35 at 2^-16.991 of W7 passes); deepest rows: row17:11; full successes 0
baseline, random CV [same A0, other A1]: CVs 500000, row-16 variants 0 (0.0000 per CV), cell mismatches 0; W7 0 (rate 2^nan, p2 2^-3.9020); first row-17 test 0 (rate 2^nan given W7, exact 2^-10; expected 0.0); row 17 0 (expected 0.00 at 2^-16.991 of W7 passes); deepest rows:; full successes 0
baseline, random CV [other A0]: CVs 500000, row-16 variants 22348210 (44.6964 per CV), cell mismatches 0; W7 1497679 (rate 2^-3.8994, p2 2^-3.9020); first row-17 test 1464 (rate 2^-9.999 given W7, exact 2^-10; expected 1462.6); row 17 12 (expected 11.50 at 2^-16.991 of W7 passes); deepest rows: row17:12; full successes 0
pair v 3662dd58 w 3662dd58 successes 63334 entries 351657 w7 23689 t1 22 r17 0
pair v 3662dd58 w 3662dd50 successes 63334 entries 354630 w7 23955 t1 23 r17 1
pair v 3662dd58 w 3662bd50 successes 63334 entries 353047 w7 23833 t1 28 r17 0
pair v 3662dd58 w 36629d50 successes 63334 entries 356219 w7 24048 t1 27 r17 0
pair v 3662dd58 w 36691d4e successes 63334 entries 352582 w7 23410 t1 22 r17 0
pair v 3662dd58 w 36693d50 successes 63334 entries 353224 w7 23974 t1 32 r17 1
pair v 3662dd58 w b6613d5a successes 63334 entries 353954 w7 24051 t1 20 r17 0
pair v 3662dd58 w b660fd58 successes 63334 entries 356919 w7 24002 t1 18 r17 0
pair v 3662dd50 w 3662dd58 successes 64288 entries 360255 w7 24383 t1 23 r17 0
pair v 3662dd50 w 3662dd50 successes 64288 entries 359441 w7 24638 t1 25 r17 0
pair v 3662dd50 w 3662bd50 successes 64288 entries 358894 w7 24301 t1 17 r17 1
pair v 3662dd50 w 36629d50 successes 64288 entries 361885 w7 24153 t1 22 r17 0
pair v 3662dd50 w 36691d4e successes 64288 entries 360051 w7 24129 t1 26 r17 0
pair v 3662dd50 w 36693d50 successes 64288 entries 357000 w7 23861 t1 24 r17 0
pair v 3662dd50 w b6613d5a successes 64288 entries 360969 w7 24538 t1 26 r17 1
pair v 3662dd50 w b660fd58 successes 64288 entries 361093 w7 24127 t1 33 r17 0
pair v 3662bd50 w 3662dd58 successes 64139 entries 356886 w7 24149 t1 18 r17 0
pair v 3662bd50 w 3662dd50 successes 64139 entries 357645 w7 24035 t1 14 r17 0
pair v 3662bd50 w 3662bd50 successes 64139 entries 354322 w7 23938 t1 19 r17 2
pair v 3662bd50 w 36629d50 successes 64139 entries 358125 w7 23957 t1 20 r17 0
pair v 3662bd50 w 36691d4e successes 64139 entries 355334 w7 23865 t1 23 r17 0
pair v 3662bd50 w 36693d50 successes 64139 entries 358385 w7 24233 t1 31 r17 1
pair v 3662bd50 w b6613d5a successes 64139 entries 355599 w7 23617 t1 27 r17 0
pair v 3662bd50 w b660fd58 successes 64139 entries 356216 w7 23976 t1 26 r17 1
pair v 36629d50 w 3662dd58 successes 64372 entries 360072 w7 24367 t1 23 r17 1
pair v 36629d50 w 3662dd50 successes 64372 entries 359708 w7 24269 t1 24 r17 0
pair v 36629d50 w 3662bd50 successes 64372 entries 362799 w7 24378 t1 28 r17 0
pair v 36629d50 w 36629d50 successes 64372 entries 363115 w7 24670 t1 36 r17 0
pair v 36629d50 w 36691d4e successes 64372 entries 361312 w7 23971 t1 23 r17 0
pair v 36629d50 w 36693d50 successes 64372 entries 358687 w7 24396 t1 18 r17 0
pair v 36629d50 w b6613d5a successes 64372 entries 355658 w7 23771 t1 19 r17 0
pair v 36629d50 w b660fd58 successes 64372 entries 359518 w7 24207 t1 21 r17 0
pair v 36691d4e w 3662dd58 successes 63403 entries 355164 w7 23609 t1 13 r17 0
pair v 36691d4e w 3662dd50 successes 63403 entries 354833 w7 23635 t1 21 r17 1
pair v 36691d4e w 3662bd50 successes 63403 entries 356139 w7 23584 t1 30 r17 0
pair v 36691d4e w 36629d50 successes 63403 entries 353590 w7 23372 t1 19 r17 0
pair v 36691d4e w 36691d4e successes 63403 entries 353706 w7 24124 t1 21 r17 0
pair v 36691d4e w 36693d50 successes 63403 entries 354469 w7 23720 t1 20 r17 0
pair v 36691d4e w b6613d5a successes 63403 entries 354515 w7 24093 t1 23 r17 0
pair v 36691d4e w b660fd58 successes 63403 entries 355010 w7 23654 t1 23 r17 0
pair v 36693d50 w 3662dd58 successes 65466 entries 364513 w7 24353 t1 25 r17 1
pair v 36693d50 w 3662dd50 successes 65466 entries 367175 w7 25034 t1 34 r17 1
pair v 36693d50 w 3662bd50 successes 65466 entries 365101 w7 24523 t1 23 r17 0
pair v 36693d50 w 36629d50 successes 65466 entries 365011 w7 24603 t1 22 r17 0
pair v 36693d50 w 36691d4e successes 65466 entries 365380 w7 24469 t1 23 r17 0
pair v 36693d50 w 36693d50 successes 65466 entries 365919 w7 24672 t1 34 r17 0
pair v 36693d50 w b6613d5a successes 65466 entries 365692 w7 24192 t1 21 r17 0
pair v 36693d50 w b660fd58 successes 65466 entries 367850 w7 24650 t1 19 r17 0
pair v b6613d5a w 3662dd58 successes 64239 entries 360007 w7 24240 t1 19 r17 0
pair v b6613d5a w 3662dd50 successes 64239 entries 358386 w7 23930 t1 21 r17 0
pair v b6613d5a w 3662bd50 successes 64239 entries 357788 w7 23877 t1 15 r17 0
pair v b6613d5a w 36629d50 successes 64239 entries 357062 w7 23907 t1 19 r17 0
pair v b6613d5a w 36691d4e successes 64239 entries 357290 w7 24216 t1 24 r17 0
pair v b6613d5a w 36693d50 successes 64239 entries 358602 w7 24126 t1 17 r17 0
pair v b6613d5a w b6613d5a successes 64239 entries 355563 w7 23886 t1 16 r17 0
pair v b6613d5a w b660fd58 successes 64239 entries 362045 w7 24282 t1 22 r17 0
pair v b660fd58 w 3662dd58 successes 64240 entries 362655 w7 24268 t1 26 r17 0
pair v b660fd58 w 3662dd50 successes 64240 entries 359889 w7 24092 t1 15 r17 0
pair v b660fd58 w 3662bd50 successes 64240 entries 356478 w7 24051 t1 23 r17 0
pair v b660fd58 w 36629d50 successes 64240 entries 357867 w7 23988 t1 26 r17 0
pair v b660fd58 w 36691d4e successes 64240 entries 357014 w7 24009 t1 22 r17 0
pair v b660fd58 w 36693d50 successes 64240 entries 359765 w7 24294 t1 23 r17 0
pair v b660fd58 w b6613d5a successes 64240 entries 355949 w7 23945 t1 23 r17 1
pair v b660fd58 w b660fd58 successes 64240 entries 358171 w7 24326 t1 30 r17 0
base w 3662dd58 cvs 500000 entries 2799178 w7 187502 t1 196 r17 0
base w 3662dd50 cvs 500000 entries 2787679 w7 185517 t1 202 r17 2
base w 3662bd50 cvs 500000 entries 2796113 w7 188516 t1 187 r17 2
base w 36629d50 cvs 500000 entries 2792083 w7 187697 t1 180 r17 1
base w 36691d4e cvs 500000 entries 2788467 w7 186899 t1 167 r17 1
base w 36693d50 cvs 500000 entries 2794812 w7 187226 t1 168 r17 1
base w b6613d5a cvs 500000 entries 2790922 w7 186709 t1 191 r17 2
base w b660fd58 cvs 500000 entries 2798956 w7 187613 t1 173 r17 3
conditioning successes 513481 over 8 A0; far row-17 passes: same A0 2, other A0 11 (pairs over 7 other A0 per success)
  HD 0..0:  8 pairs, entries per (success, A0 of w) 5.5735, W7 rate 2^-3.8833, first-test rate 2^-9.900, row-17 passes 2 (expected 1.49 at 2^-16.991)
  HD 1..3: 14 pairs, entries per (success, A0 of w) 5.6026, W7 rate 2^-3.8921, first-test rate 2^-10.086, row-17 passes 3 (expected 2.60 at 2^-16.991)
  HD 4..6: 24 pairs, entries per (success, A0 of w) 5.5815, W7 rate 2^-3.8950, first-test rate 2^-10.036, row-17 passes 4 (expected 4.46 at 2^-16.991)
  HD 7..9: 18 pairs, entries per (success, A0 of w) 5.5824, W7 rate 2^-3.9012, first-test rate 2^-10.059, row-17 passes 4 (expected 3.30 at 2^-16.991)
seeds 120, seeds with events 13, largest per seed 1, records with two or more 0
D_far: point 0.000784; 99% bound (Poisson, 0.5% per class) 0.001634; seed-clustered bound 0.001809; ledger value 1/200 = 0.005
ram_check: 4000 successes (of 1096010), 166 distinct A0: 4000 found and verified by the counted program, 0 not
```

## Appendix B. Evidence programs

The files used for the runs of Section 11. consts.h (cell masks and the published trace) and twobit.h (the
conditions of 3.2) are generated from the tables of Section 3 by gen_consts.py and gen2.py, which use r38.py.
smc2.c (first version) is smc3.c with seed = seed0 * 0x9e3779b97f4a7c15 + 1 and without the optional fixed-variant
argument; smc_het was smc2.c with that argument. far.c (superseded run) is far2.c with four fixed A0 and no per-pair counts.
pipe_dump is pipe.c with one change: with DUMP set it prints every chaining value (index, M0) and every hit
(index, A1, A2 index, g index); truebucket.py reads that output.

### B.1 cert.py

```python
#!/usr/bin/env python3
# cert.py - the exact ledger of the variant-table attack (proof.md Sections 6.4, 7, 8).  Every count is a number of
# primitive operations of the counted program (experiments/vt38.py: online code and table-build code, counted by
# its interpreter) or of the preprocessing of proof.md 5.1; probabilities are exact rationals except q3_model
# (2^-102, one bit below the SMC lower bounds, H2) and the pair budget delta = 1 (H5; measured values are far smaller).
from fractions import Fraction as F
import math, sys

C = 2728                                   # reference operation cost of sha256-r38 (collision-frontier-v5)
LOG = lambda x: math.log2(x.numerator) - math.log2(x.denominator)

def ledger(R, q3_log2=-102, delta=F(1),
           A_C=F(2)**78, A_S=F(2)**74, DEV=F(2)**64, target=F(396, 1000), verbose=True):
    m = len(R); SR = sum(R)
    p2 = F(287309824, 2**32)                                  # |F7| / 2^32
    p16 = F(32, 2**32)                                        # |G| / 2^32
    q3 = F(math.floor(2.0 ** q3_log2 * 2**140), 2**140)        # rational lower bound of 2^q3_log2
    S = SR * p2 * q3                                          # expected successes per group (H1, H2)
    n = SR                                                    # variants examined per group
    # H5: the expected number of further successes in the group, seen from a success, is at most delta
    qlb = S * (1 - delta / 2)                                 # Bonferroni
    cexp = F(math.ceil(-math.log(1 - float(target)) * 10**6), 10**6)   # N_G q_lb >= -ln(1 - target)
    NG = -(-cexp // qlb)                                      # groups (ceil)
    # per-group work counters: entries NE, W7 passes NW, first-row-17-test passes N1 (proof.md 6.4)
    BMAX = 14 * 32 * 768                                      # bucket-size bound: max|phi^-1| * |G| * |A2 list|
    muE = SR * p16                                            # E[NE] per group (H1)
    muW = muE * p2                                            # E[NW]
    mE_bits = 10                                             # x-value bits of E17 tested first (2^-10 exactly, H1)
    mu1 = muW * F(1, 2**mE_bits)                              # E[N1]: W7 passes that pass the first row-17 test
    rng = m * BMAX                                            # range of each counter per group
    def cap(mu, t):                                           # Hoeffding over NG independent groups
        expo = 2 * (t * mu) ** 2 * NG / rng ** 2              # Pr[overflow] <= exp(-expo)
        return -(-(NG * mu * (1 + t)) // 1), float(expo)
    NE_MAX, eE = cap(muE, F(1, 2**6)); NW_MAX, eW = cap(muW, F(1, 2**5)); N1_MAX, e1 = cap(mu1, F(3))
    c_pro, c_blk, c_ep = 64, 30, 15                           # prologue (+1 unit), per A0 block (+END), epilogue+loop
    c_ent, c_17, c_17b = 10, 66, 26 + 3132                    # per entry, per W7 pass, per first-test pass (rest + deep)
    over = rng * (c_ent + c_17 + c_17b)                       # caps are tested after a group: one group's overshoot
    online_ops = NG * (c_pro + m * c_blk + c_ep) + NE_MAX * c_ent + NW_MAX * c_17 + N1_MAX * c_17b + over
    online_units = NG                                         # one first-block compression per group
    init_ops = 1024                                           # start-up: counters, constants, code pointers
    fin_units, fin_ops = 6, 1024                              # two messages, their three-block digests, output
    # preprocessing (proof.md Section 5.1), in operations
    P_G = 2**32 * 64; P_F7 = 2**32 * 24; P_A2 = 2**32 * 64; P_rec = 768 * 64 + 32 * 128
    P_R = m * 768 * (2**29 * 67 + 42 + 8) + SR * 25           # counted (selftest item 10): candidate, setup, outer, valid
    P_T = 2**32 * SR * (211 + 275) + m * 2**64 * (4 + 10) + m * 2**32 * 2 * 10   # count+fill, zero+prefix, per-Y setup
    pre_ops = P_G + P_F7 + P_A2 + P_rec + P_R + P_T
    T = A_C + A_S + DEV + F(pre_ops + init_ops + online_ops + fin_ops, C) + online_units + fin_units
    # memory in 256-bit words: per table headers and fill cursors (2 x 2^64), entries (32 per (Y, v)); R lists;
    # (two words per variant); F7 word table; A2 and G records; program code (blocks of <= 3,300 instructions)
    mem_words = m * 2 * 2**64 + 2**32 * SR * 32 + 2 * SR + 2**32 + 768 * 4 + 32 * 16 + m * 4000
    pre_units = A_C + A_S + DEV + F(pre_ops, C)
    succ = 1 - math.exp(-float(NG * qlb)) - math.exp(-eE) - math.exp(-eW) - math.exp(-e1)
    out = dict(m=m, SR_log2=LOG(F(SR)), q3_log2=LOG(q3), S_log2=LOG(S), delta=float(delta), NG=NG, NG_log2=LOG(F(NG)),
               NE_MAX=NE_MAX, NW_MAX=NW_MAX, N1_MAX=N1_MAX, hoeffding_exponents=(eE, eW, e1),
               online_units_log2=LOG(online_units + F(online_ops, C)), pre_units_log2=LOG(F(pre_ops, C)),
               allowances_log2=LOG(A_C + A_S + DEV), T_log2=LOG(T), success=succ,
               preprocessing_log2=LOG(pre_units), memory_log2_bytes=LOG(F(mem_words * 32)),
               T_exact=T, terms=dict(online_ops=online_ops, online_units=online_units, pre_ops=pre_ops,
               P_G=P_G, P_F7=P_F7, P_A2=P_A2, P_rec=P_rec, P_R=P_R, P_T=P_T, init_ops=init_ops, fin=(fin_units, fin_ops)),
               per_pair_ops=float(F(online_ops, NG * m)))
    if verbose:
        for k, v in out.items(): print('%-22s %s' % (k, v))
    return out, T

if __name__ == '__main__':
    R = [int(l.split()[1]) for l in open(sys.argv[1] if len(sys.argv) > 1 else 'a0set256.txt')]
    m = int(sys.argv[2]) if len(sys.argv) > 2 else len(R)
    out, T = ledger(R[:m])
    tl = math.ceil(out['T_log2'] * 1e5) / 1e5
    print('time_log2 (rounded up) = %.5f' % tl)
```

### B.2 core.h

```c
// Shared code: reduced SHA-256 steps, the 38-step characteristic checks, dense-part variants.
#include <stdint.h>
#include <string.h>
#include "consts.h"
#include "twobit.h"
#define ROR(x,n) (((x)>>(n))|((x)<<(32-(n))))
static inline uint32_t S0(uint32_t x){return ROR(x,2)^ROR(x,13)^ROR(x,22);}
static inline uint32_t S1(uint32_t x){return ROR(x,6)^ROR(x,11)^ROR(x,25);}
static inline uint32_t s0(uint32_t x){return ROR(x,7)^ROR(x,18)^(x>>3);}
static inline uint32_t s1(uint32_t x){return ROR(x,17)^ROR(x,19)^(x>>10);}
static inline uint32_t Ch(uint32_t x,uint32_t y,uint32_t z){return (x&y)^(~x&z);}
static inline uint32_t Mj(uint32_t x,uint32_t y,uint32_t z){return (x&y)^(x&z)^(y&z);}
#define NR 38
// state arrays: a[i+4], e[i+4] for i = -4..37; w[i] for i = 0..37
typedef struct { uint32_t a[NR+4], e[NR+4], w[NR]; } Tr;
#define AA(t,i) ((t)->a[(i)+4])
#define EE(t,i) ((t)->e[(i)+4])
static inline void step(Tr *t, int i) {
    EE(t,i) = AA(t,i-4) + EE(t,i-4) + S1(EE(t,i-1)) + Ch(EE(t,i-1), EE(t,i-2), EE(t,i-3)) + KK[i] + t->w[i];
    AA(t,i) = EE(t,i) - AA(t,i-4) + S0(AA(t,i-1)) + Mj(AA(t,i-1), AA(t,i-2), AA(t,i-3));
}
static inline uint32_t sched(const Tr *t, int i) { return s1(t->w[i-2]) + t->w[i-7] + s0(t->w[i-15]) + t->w[i-16]; }
static inline uint32_t getv(const Tr *t, int k, int i) { return k == 0 ? AA(t,i) : k == 1 ? EE(t,i) : t->w[i]; }
static inline uint32_t plusmask(int i) { return (i >= 1 && i < NR) ? (CP[i]) : 0; }
// cells of row i (A, E with '+', and W if wcell), plus two-bit conditions keyed at row i (member x)
static inline int rowok(const Tr *x, const Tr *y, int i, int wcell) {
    uint32_t ax = AA(x,i), ay = AA(y,i), ex = EE(x,i), ey = EE(y,i);
    if ((ax & CM[0][i]) != CV_[0][i] || (ax ^ ay) != CD[0][i]) return 0;
    if ((ex & CM[1][i]) != CV_[1][i] || (ex ^ ey) != CD[1][i]) return 0;
    if (CP[i] && ((ex ^ EE(x,i-1)) & CP[i])) return 0;
    if (wcell) { uint32_t wx = x->w[i], wy = y->w[i]; if ((wx & CM[2][i]) != CV_[2][i] || (wx ^ wy) != CD[2][i]) return 0; }
    for (int j = 0; j < NX; j++) if (XROW[j] == i) {
        uint32_t b1 = getv(x, XK1[j], XI1[j]) >> XB1[j] & 1, b2 = getv(x, XK2[j], XI2[j]) >> XB2[j] & 1;
        if ((b1 ^ b2) != (uint32_t)XNE[j]) return 0;
    }
    return 1;
}
// Dense-part variant: A0..A3 replaced (no difference rows 0..6), E4..E7, W8..W11 recomputed, both members.
typedef struct { uint32_t A[2][16], E[2][16], W[2][16]; uint32_t c7[2]; } Var;
static const uint32_t W1415[2][2] = {{0xd28e48a0, 0x9f1f65bb}, {0xd28e48a0, 0x9b5f6dbb}};
static void mkvar(Var *v, uint32_t a0, uint32_t a1, uint32_t a2, uint32_t a3) {
    for (int m = 0; m < 2; m++) {
        const uint32_t *A0 = m ? AY : AX, *E0 = m ? EY : EX, *W0 = m ? WY : WX;
        uint32_t *A = v->A[m], *E = v->E[m], *W = v->W[m];
        for (int i = 0; i < 16; i++) { A[i] = A0[i]; E[i] = E0[i]; W[i] = W0[i]; }
        A[0] = a0; A[1] = a1; A[2] = a2; A[3] = a3;
        for (int i = 4; i <= 7; i++) E[i] = A[i] + A[i-4] - S0(A[i-1]) - Mj(A[i-1], A[i-2], A[i-3]);
        for (int i = 8; i <= 11; i++) W[i] = E[i] - A[i-4] - E[i-4] - S1(E[i-1]) - Ch(E[i-1], E[i-2], E[i-3]) - KK[i];
        W[14] = W1415[m][0]; W[15] = W1415[m][1];
        // W7 = c7 - A_{-1}
        v->c7[m] = E[7] - 2*A[3] + S0(A[2]) + Mj(A[2], A[1], A[0]) - S1(E[6]) - Ch(E[6], E[5], E[4]) - KK[7];
    }
}
// Validity of a variant: E cells rows 4..8 ('+' pairs included) and unchanged modular differences that reach
// rows >= 16: dW8..dW11 and ds0(W8..W11).
static int var_valid(const Var *v) {
    for (int i = 4; i <= 8; i++) {
        uint32_t x = v->E[0][i], y = v->E[1][i];
        if ((x & CM[1][i]) != CV_[1][i] || (x ^ y) != CD[1][i]) return 0;
        if (CP[i] && ((x ^ v->E[0][i-1]) & CP[i])) return 0;
    }
    for (int i = 8; i <= 11; i++) {
        if (v->W[0][i] - v->W[1][i] != WX[i] - WY[i]) return 0;
        if (s0(v->W[0][i]) - s0(v->W[1][i]) != s0(WX[i]) - s0(WY[i])) return 0;
    }
    return 1;
}
// Second-block pair from chaining value cv for variant v: fills traces x, y with rows -4..15 and W0..W15.
static void mkpair(const Var *v, const uint32_t cv[8], Tr *x, Tr *y) {
    for (int m = 0; m < 2; m++) {
        Tr *t = m ? y : x; const uint32_t *A = v->A[m], *E = v->E[m];
        for (int j = 0; j < 4; j++) { AA(t,-1-j) = cv[j]; EE(t,-1-j) = cv[4+j]; }
        for (int i = 0; i < 16; i++) AA(t,i) = A[i];
        for (int i = 4; i < 16; i++) EE(t,i) = E[i];
        for (int i = 0; i < 4; i++) EE(t,i) = AA(t,i) + AA(t,i-4) - S0(AA(t,i-1)) - Mj(AA(t,i-1), AA(t,i-2), AA(t,i-3));
        for (int i = 0; i < 8; i++) t->w[i] = EE(t,i) - AA(t,i-4) - EE(t,i-4) - S1(EE(t,i-1)) - Ch(EE(t,i-1), EE(t,i-2), EE(t,i-3)) - KK[i];
        for (int i = 8; i < 16; i++) t->w[i] = v->W[m][i];
    }
}
// splitmix64 PRNG for experiments
static inline uint64_t smx(uint64_t *s) { uint64_t z = (*s += 0x9e3779b97f4a7c15ULL); z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9ULL; z = (z ^ (z >> 27)) * 0x94d049bb133111ebULL; return z ^ (z >> 31); }
// full 38-step compression with feed-forward
static void compress38(const uint32_t cv[8], const uint32_t m[16], uint32_t out[8]) {
    Tr t; for (int j = 0; j < 4; j++) { AA(&t,-1-j) = cv[j]; EE(&t,-1-j) = cv[4+j]; }
    for (int i = 0; i < 16; i++) t.w[i] = m[i];
    for (int i = 16; i < NR; i++) t.w[i] = sched(&t, i);
    for (int i = 0; i < NR; i++) step(&t, i);
    for (int j = 0; j < 4; j++) { out[j] = cv[j] + AA(&t, NR-1-j); out[4+j] = cv[4+j] + EE(&t, NR-1-j); }
}
static const uint32_t IV8[8] = {0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19};
```

### B.3 lib.h

```c
// Variant machinery on top of core.h: A2 candidates, fast V(A0, A2) enumeration, per-CV quantities.
#include <stdio.h>
#include <stdlib.h>
#include "core.h"

static uint32_t D8, T8, D9, T9, D10, T10;
static void lib_init(void) {
    D8 = WX[8] - WY[8]; T8 = s0(WX[8]) - s0(WY[8]);
    D9 = WX[9] - WY[9]; T9 = s0(WX[9]) - s0(WY[9]);
    D10 = WX[10] - WY[10]; T10 = s0(WX[10]) - s0(WY[10]);
}
static inline int good8(uint32_t w) { return s0(w) - s0(w - D8) == T8; }

// A2 candidates: E6 x-value cells, E7/E6 '+', dW10 and ds0(W10) unchanged (conditions on A2 alone).
typedef struct { uint32_t a2, e6, c9x, c9y; } A2c;   // W9x = c9x - A1, W9y = c9y - A1
static A2c *A2L; static int nA2;
static void load_a2(void) {
    A2L = malloc(sizeof(A2c) * 1024); nA2 = 0;
    for (uint64_t v = 0; v < (1ULL << 32); v++) {
        uint32_t a2 = (uint32_t)v;
        uint32_t e6 = AX[6] + a2 - S0(AX[5]) - Mj(AX[5], AX[4], AX[3]);
        if ((e6 & CM[1][6]) != CV_[1][6]) continue;
        if ((EX[7] ^ e6) & CP[7]) continue;
        uint32_t w10x = EX[10] - AX[6] - e6 - S1(EX[9]) - Ch(EX[9], EX[8], EX[7]) - KK[10];
        uint32_t w10y = EY[10] - AY[6] - e6 - S1(EY[9]) - Ch(EY[9], EY[8], EY[7]) - KK[10];
        if (w10x - w10y != D10 || s0(w10x) - s0(w10y) != T10) continue;
        A2c c; c.a2 = a2; c.e6 = e6;
        // W9 = E9 - A5 - E5 - S1(E8) - Ch(E8,E7,E6) - K9, E5 = A5 + A1 - S0(A4) - Mj(A4,A3,A2)
        c.c9x = EX[9] - AX[5] - (AX[5] - S0(AX[4]) - Mj(AX[4], AX[3], a2)) - S1(EX[8]) - Ch(EX[8], EX[7], e6) - KK[9];
        c.c9y = EY[9] - AY[5] - (AY[5] - S0(AY[4]) - Mj(AY[4], AY[3], a2)) - S1(EY[8]) - Ch(EY[8], EY[7], e6) - KK[9];
        A2L[nA2++] = c;
    }
}
// A0-independent part of W8 (member m) for (A1, A2): W8 = F - A0.
static inline uint32_t Fpart(int m, uint32_t a1, const A2c *c) {
    const uint32_t *A = m ? AY : AX, *E = m ? EY : EX;
    uint32_t e4 = A[4] - S0(A[3]) - Mj(A[3], c->a2, a1);           // + A0
    uint32_t e5 = A[5] + a1 - S0(A[4]) - Mj(A[4], A[3], c->a2);
    return E[8] - A[4] - e4 - S1(E[7]) - Ch(E[7], c->e6, e5) - KK[8];
}
// Validity of (A0, A1, A2) for an A2 candidate (fast path; equals var_valid, checked in selftests).
static inline int valid3(uint32_t a0, uint32_t a1, const A2c *c) {
    uint32_t e5 = AX[5] + a1 - S0(AX[4]) - Mj(AX[4], AX[3], c->a2);
    if ((c->e6 ^ e5) & CP[6]) return 0;
    uint32_t w9x = c->c9x - a1, w9y = c->c9y - a1;
    if (w9x - w9y != D9 || s0(w9x) - s0(w9y) != T9) return 0;
    uint32_t w8x = Fpart(0, a1, c) - a0, w8y = Fpart(1, a1, c) - a0;
    if (w8x - w8y != D8 || s0(w8x) - s0(w8y) != T8) return 0;
    return 1;
}
// E5's top three bits must equal E6's: A1 lies in one residue interval of length 2^29.
static inline uint32_t a1_start(const A2c *c) {
    uint32_t base = AX[5] - S0(AX[4]) - Mj(AX[4], AX[3], c->a2);   // E5 = base + A1
    uint32_t top = c->e6 & 0xe0000000u;
    return top - base;   // A1 = top - base + k, k in [0, 2^29): E5 = top + k
}
// Enumerate V(A0, A2): returns count, writes A1 values to out (if non-null).
static long enum_v(uint32_t a0, const A2c *c, uint32_t *out) {
    long n = 0; uint32_t st = a1_start(c);
    for (uint32_t k = 0; k < (1u << 29); k++) {
        uint32_t a1 = st + k;
        if (valid3(a0, a1, c)) { if (out) out[n] = a1; n++; }
    }
    return n;
}
// Per (CV, A0): W0 = A0 + y0, Y = W1 - A1 (A1-free), Z0 = W0 + s1(W14x).
typedef struct { uint32_t a, b, c, d, e, f, g, h; uint32_t hh, y0; } CVq;
static void cv_pre(const uint32_t cv[8], CVq *q) {
    q->a = cv[0]; q->b = cv[1]; q->c = cv[2]; q->d = cv[3]; q->e = cv[4]; q->f = cv[5]; q->g = cv[6]; q->h = cv[7];
    // E0 = A0 + hh, hh = A_{-4} - S0(A_{-1}) - Mj(A_{-1}, A_{-2}, A_{-3})
    q->hh = q->d - S0(q->a) - Mj(q->a, q->b, q->c);
    // W0 = E0 - A_{-4} - E_{-4} - S1(E_{-1}) - Ch(E_{-1},E_{-2},E_{-3}) - K0 = A0 + y0
    q->y0 = q->hh - q->d - q->h - S1(q->e) - Ch(q->e, q->f, q->g) - KK[0];
}
static inline void cv_a0(const CVq *q, uint32_t a0, uint32_t *Y, uint32_t *Z0, uint32_t *W0) {
    uint32_t e0 = a0 + q->hh;
    // W1 = A1 - S0(A0) - Mj(A0, A_{-1}, A_{-2}) - E_{-3} - S1(E0) - Ch(E0, E_{-1}, E_{-2}) - K1
    *Y = 0u - S0(a0) - Mj(a0, q->a, q->b) - q->g - S1(e0) - Ch(e0, q->e, q->f) - KK[1];
    *W0 = a0 + q->y0;
    *Z0 = *W0 + s1(0xd28e48a0u);
}
```

### B.4 smc3.c

```c
// Sequential Monte-Carlo estimate of the variant-averaged q3 = E_v Pr[rows 16..37 hold | W7 in F7] for the
// ePrint 2026/1120 38-step characteristic with dense-part variants v = (A0, A1, A2).
// Rows 16..22 do not depend on v (Lemma V2): row 16 exact (32 good W16 of 2^32); rows 17..22 propose E_i^x
// uniformly with its x-value cells and '+' bits imposed (exact weight 2^-f).  Tail: each proposal draws a
// variant uniformly from the supplied sample (W8, W9, W10 of both members), proposes W23^x with its x-value
// cells imposed and sets W7 = W23 - s1(W21) - W16 - s0(W8), weight 1{W7 in F7} 2^(32-f)/|F7|; rows 23..37
// deterministic.  Every tail success is rebuilt (W0..W7 by the inverse expansion, CV1 by inverting steps 7..0 of
// the variant) and accepted only if it is a 38-step semi-free-start collision from CV1 whose Step-2 words map
// back to W0..W7, with W7 in F7 and every A/E cell of rows -4..37 and W cell of rows 16..37 holding.
// Clumping replay: for every success, all other A2 valid with the same (A0, A1) are tried on the same CV1.
// usage: smc3 seed NP M17 M18 M19 M20 M21 M22 MT variants.bin outprefix [fixed variant index]
// (smc3.c = smc2.c with hashed seeding and the optional fixed-variant argument of smc_het.)
#include <math.h>
#include "lib.h"
typedef struct { Tr x, y; } P;
static uint8_t *F7bm; static const double F7n = 287309824.0;
static inline int inF7(uint32_t w) { return F7bm[w >> 3] >> (w & 7) & 1; }
static uint32_t G[32];
typedef struct { uint32_t a0, a1, a2, w8x, w8y, w9x, w9y, w10x, w10y, c7x; } VR;
static VR *VS; static long nV; static long FIXV = -1;
static inline uint64_t below(uint64_t *s, uint64_t n) { return smx(s) % n; }
static inline int aecells(const Tr *x, const Tr *y) {
    for (int i = 0; i < NR; i++) {
        uint32_t ax = AA(x,i), ay = AA(y,i), ex = EE(x,i), ey = EE(y,i);
        if ((ax & CM[0][i]) != CV_[0][i] || (ax ^ ay) != CD[0][i]) return 0;
        if ((ex & CM[1][i]) != CV_[1][i] || (ex ^ ey) != CD[1][i]) return 0;
        if (CP[i] && ((ex ^ EE(x,i-1)) & CP[i])) return 0;
        if (i >= 16) { uint32_t wx = x->w[i], wy = y->w[i]; if ((wx & CM[2][i]) != CV_[2][i] || (wx ^ wy) != CD[2][i]) return 0; }
    }
    return 1;
}
// full success test of variant (a0,a1,a2) on chaining value cv: rows 16..37 (cells + two-bit) and W7 in F7
static int success(const uint32_t cv[8], uint32_t a0, uint32_t a1, uint32_t a2, Tr *xo, Tr *yo) {
    Var v; mkvar(&v, a0, a1, a2, AX[3]); if (!var_valid(&v)) return 0;
    Tr x, y; mkpair(&v, cv, &x, &y);
    if (!inF7(x.w[7])) return 0;
    for (int i = 16; i < NR; i++) { x.w[i] = sched(&x, i); y.w[i] = sched(&y, i); }
    for (int i = 0; i < NR; i++) { step(&x, i); step(&y, i); if (i >= 16 && !rowok(&x, &y, i, 1)) return 0; }
    if (xo) { *xo = x; *yo = y; }
    return 1;
}
int main(int argc, char **argv) {
    if (argc < 12) { fprintf(stderr, "usage\n"); return 1; }
    // Seeding: the splitmix64 finalizer of seed0 (smc2.c used seed0 * phi + 1, which made the streams of consecutive
    // seeds one-draw shifts of each other); distinct seeds start at unrelated points of the 2^64 cycle.
    uint64_t seed0 = strtoull(argv[1], 0, 10), seed = seed0; seed = smx(&seed); int NP = atoi(argv[2]);
    int MS[23]; for (int i = 17; i <= 22; i++) MS[i] = atoi(argv[3 + i - 17]);
    int MT = atoi(argv[9]); const char *vf = argv[10], *outp = argv[11]; if (argc > 12) FIXV = atol(argv[12]);
    lib_init(); load_a2();
    FILE *f = fopen("F7.bm", "rb"); F7bm = malloc(1u << 29); fread(F7bm, 1, 1u << 29, f); fclose(f);
    f = fopen("G.txt", "r"); for (int i = 0; i < 32; i++) fscanf(f, "%x", &G[i]); fclose(f);
    f = fopen(vf, "rb"); fseek(f, 0, SEEK_END); nV = ftell(f) / sizeof(VR); fseek(f, 0, SEEK_SET); VS = malloc(nV * sizeof(VR)); fread(VS, sizeof(VR), nV, f); fclose(f);
    Var v0; mkvar(&v0, AX[0], AX[1], AX[2], AX[3]);
    P base; memset(&base, 0, sizeof base);
    for (int m = 0; m < 2; m++) {
        Tr *t = m ? &base.y : &base.x;
        for (int i = 8; i < 16; i++) { AA(t,i) = v0.A[m][i]; EE(t,i) = m ? EY[i] : EX[i]; t->w[i] = v0.W[m][i]; }
    }
    const uint32_t dW16 = 0x20000000u, d7 = 0x20000000u, t7 = 0x03bff800u;
    double logs[10]; int ns = 0; double est = 32.0 / 4294967296.0; logs[ns++] = log2(est);
    P *cur = malloc(sizeof(P) * (size_t)NP); P *surv = NULL; size_t cap = 0;
    for (int p = 0; p < NP; p++) {
        cur[p] = base; uint32_t w = G[below(&seed, 32)];
        cur[p].x.w[16] = w; cur[p].y.w[16] = w - dW16; step(&cur[p].x, 16); step(&cur[p].y, 16);
        if (!rowok(&cur[p].x, &cur[p].y, 16, 1)) { fprintf(stderr, "G mismatch\n"); return 1; }
    }
    for (int i = 17; i <= 22; i++) {
        uint32_t m = CM[1][i], vv = CV_[1][i], pq = CP[i]; int fb = __builtin_popcount(m) + __builtin_popcount(pq);
        size_t ns_ = 0;
        for (int p = 0; p < NP; p++) for (int c = 0; c < MS[i]; c++) {
            P q = cur[p];
            uint32_t e = ((uint32_t)smx(&seed) & ~m) | vv;
            if (pq) e = (e & ~pq) | (EE(&q.x, i-1) & pq);
            uint32_t cx = AA(&q.x,i-4) + EE(&q.x,i-4) + S1(EE(&q.x,i-1)) + Ch(EE(&q.x,i-1), EE(&q.x,i-2), EE(&q.x,i-3)) + KK[i];
            q.x.w[i] = e - cx;
            uint32_t dw = (s1(q.x.w[i-2]) - s1(q.y.w[i-2])) + (q.x.w[i-7] - q.y.w[i-7]);
            if (i == 22) dw += 0u - t7;                 // s0(W7x) - s0(W7y) = -t7
            q.y.w[i] = q.x.w[i] - dw;
            step(&q.x, i); step(&q.y, i);
            if (!rowok(&q.x, &q.y, i, 1)) continue;
            if (ns_ == cap) { cap = cap ? 2 * cap : 1 << 16; surv = realloc(surv, cap * sizeof(P)); }
            surv[ns_++] = q;
        }
        double fac = (double)ns_ / ((double)NP * MS[i]) * pow(2.0, -fb); est *= fac; logs[ns++] = log2(fac);
        if (!ns_) { printf("seed %llu: extinct at row %d\n", (unsigned long long)seed0, i); return 0; }
        for (int p = 0; p < NP; p++) cur[p] = surv[below(&seed, ns_)];
    }
    uint32_t m23 = CM[2][23], v23 = CV_[2][23]; int f23 = __builtin_popcount(m23);
    long nhit = 0, bad = 0, clump_tried = 0, clump_succ = 0;
    char fn[512]; sprintf(fn, "%s_%llu.sfs", outp, (unsigned long long)seed0); FILE *fs = fopen(fn, "w");
    for (int p = 0; p < NP; p++) for (int c = 0; c < MT; c++) {
        P q = cur[p]; const VR *vr = FIXV >= 0 ? &VS[FIXV] : &VS[below(&seed, nV)];
        q.x.w[8] = vr->w8x; q.y.w[8] = vr->w8y; q.x.w[9] = vr->w9x; q.y.w[9] = vr->w9y; q.x.w[10] = vr->w10x; q.y.w[10] = vr->w10y;
        uint32_t w23 = ((uint32_t)smx(&seed) & ~m23) | v23;
        uint32_t w7 = w23 - s1(q.x.w[21]) - q.x.w[16] - s0(q.x.w[8]);
        if (!inF7(w7)) continue;
        q.x.w[23] = w23; q.y.w[23] = s1(q.y.w[21]) + q.y.w[16] + s0(q.y.w[8]) + (w7 + d7);
        int ok = 1;
        for (int i = 23; i < NR && ok; i++) {
            if (i > 23) { q.x.w[i] = sched(&q.x, i); q.y.w[i] = sched(&q.y, i); }
            step(&q.x, i); step(&q.y, i); ok = rowok(&q.x, &q.y, i, 1);
        }
        if (!ok) continue;
        nhit++;
        // rebuild: W0..W7 by the inverse expansion, CV1 by inverting steps 7..0 of the variant
        uint32_t W[16]; W[7] = w7;
        for (int i = 8; i < 16; i++) W[i] = q.x.w[i];
        W[6] = q.x.w[22] - s1(q.x.w[20]) - W[15] - s0(W[7]);
        for (int i = 5; i >= 0; i--) W[i] = q.x.w[i+16] - s1(q.x.w[i+14]) - W[i+9] - s0(W[i+1]);
        Var v; mkvar(&v, vr->a0, vr->a1, vr->a2, AX[3]);
        uint32_t A[24], E[24];   // index i+8
        for (int i = 0; i < 8; i++) { A[i+8] = v.A[0][i]; if (i >= 4) E[i+8] = v.E[0][i]; }
        for (int i = 7; i >= 0; i--) {
            A[i-4+8] = E[i+8] - A[i+8] + S0(A[i-1+8]) + Mj(A[i-1+8], A[i-2+8], A[i-3+8]);
            E[i-4+8] = E[i+8] - A[i-4+8] - S1(E[i-1+8]) - Ch(E[i-1+8], E[i-2+8], E[i-3+8]) - KK[i] - W[i];
        }
        uint32_t cv[8] = {A[7], A[6], A[5], A[4], E[7], E[6], E[5], E[4]};
        Tr x, y; uint32_t h1[8], h2[8], wy[16];
        int good = success(cv, vr->a0, vr->a1, vr->a2, &x, &y);
        if (good) { for (int i = 0; i < 16; i++) { good &= x.w[i] == W[i] || i > 7; wy[i] = y.w[i]; }
            good &= aecells(&x, &y);
            compress38(cv, x.w, h1); compress38(cv, wy, h2); good &= !memcmp(h1, h2, 32) && memcmp(x.w, wy, 64); }
        if (!good) { bad++; continue; }
        fprintf(fs, "%08x %08x %08x", vr->a0, vr->a1, vr->a2);
        for (int j = 0; j < 8; j++) fprintf(fs, " %08x", cv[j]);
        for (int j = 0; j < 16; j++) fprintf(fs, " %08x", x.w[j]);
        for (int j = 0; j < 16; j++) fprintf(fs, " %08x", wy[j]);
        // clumping replay: other A2 valid with (A0, A1)
        int extra = 0;
        for (int k = 0; k < nA2; k++) {
            if (A2L[k].a2 == vr->a2 || !valid3(vr->a0, vr->a1, &A2L[k])) continue;
            clump_tried++; if (success(cv, vr->a0, vr->a1, A2L[k].a2, 0, 0)) { clump_succ++; extra++; }
        }
        fprintf(fs, " %d\n", extra);
    }
    fclose(fs);
    double tf = (double)nhit / ((double)NP * MT) * pow(2.0, 32 - f23) / F7n; est *= tf; logs[ns++] = log2(tf);
    printf("seed %llu NP %d: log2 q3 = %.4f  Z = %.6e  stages:", (unsigned long long)seed0, NP, log2(est), est);
    for (int k = 0; k < ns; k++) printf(" %.3f", logs[k]);
    printf("  tail %ld rebuilt-bad %ld clump %ld/%ld\n", nhit, bad, clump_succ, clump_tried);
    return 0;
}
```

### B.5 pipe.c

```c
// End-to-end check on real first blocks: M0 uniform, CV1 = F38(IV, M0); for one A0, find every (A1, A2) in R(A0)
// whose row 16 holds (via phi^{-1}, phi(u) = s0(u) - u), then build the second-block pair with the generic code
// and record: hits per CV, W7-filter passes, deepest row reached.  Compares with |R(A0)| 2^-27, p2, SMC stages.
// usage: pipe A0hex nCV seed threads
#include <pthread.h>
#include <math.h>
#include "lib.h"
static uint32_t *PHO;      // PHO[t] = start offset of phi^{-1}(t) in PHU (t < 2^32); end = PHO[t+1] or 2^32
static uint32_t *PHU;
static uint8_t *F7bm;
static inline int inF7(uint32_t w) { return F7bm[w >> 3] >> (w & 7) & 1; }
static uint32_t G[32];
// R(A0) grouped by c9x class: sorted (A1, A2 index) arrays
typedef struct { uint32_t c9x; uint64_t *e; long n; } Cls;   // e = (A1 << 32) | a2idx
static Cls CL[256]; static int nCL;
static uint64_t *BLOOM; // 2^35 bits keyed by (cls, A1)
static inline uint64_t bkey(int cl, uint32_t a1) { uint64_t k = ((uint64_t)cl << 32) | a1; k *= 0x9e3779b97f4a7c15ULL; return k >> 29; }
static uint32_t A0;
static uint64_t NCV, SEED; static int NT;
typedef struct { uint64_t cv, hits, w7, row[40], ymis, hist[257], w7hist[33]; } Stat;
static Stat ST[64];
static int cmpu64(const void *a, const void *b) { uint64_t x = *(uint64_t*)a, y = *(uint64_t*)b; return x < y ? -1 : x > y; }
static inline int aecells(const Tr *x, const Tr *y, int lo, int hi) {
    for (int i = lo; i <= hi; i++) {
        if (i < 0) continue;
        uint32_t ax = AA(x,i), ay = AA(y,i), ex = EE(x,i), ey = EE(y,i);
        if ((ax & CM[0][i]) != CV_[0][i] || (ax ^ ay) != CD[0][i]) return 0;
        if ((ex & CM[1][i]) != CV_[1][i] || (ex ^ ey) != CD[1][i]) return 0;
        if (CP[i] && ((ex ^ EE(x,i-1)) & CP[i])) return 0;
    }
    return 1;
}
static void *work(void *arg) {
    int id = (int)(long)arg; Stat *st = &ST[id]; uint64_t s = SEED * 1000003 + id;
    for (uint64_t it = id; it < NCV; it += NT) {
        uint32_t m0[16], cv[8]; for (int j = 0; j < 16; j++) m0[j] = (uint32_t)smx(&s);
        compress38(IV8, m0, cv); st->cv++;
        CVq q; cv_pre(cv, &q); uint32_t Y, Z0, W0; cv_a0(&q, A0, &Y, &Z0, &W0);
        uint64_t h0 = st->hits, w0 = st->w7;
        for (int cl = 0; cl < nCL; cl++) {
            uint32_t tb = Y + Z0 + CL[cl].c9x;
            for (int gi = 0; gi < 32; gi++) {
                uint32_t t = G[gi] - tb;
                uint64_t lo = PHO[t], hi = (t == 0xffffffffu) ? (1ULL << 32) : PHO[t + 1];
                for (uint64_t p = lo; p < hi; p++) {
                    uint32_t a1 = PHU[p] - Y;
                    uint64_t bk = bkey(cl, a1); if (!(BLOOM[bk >> 6] >> (bk & 63) & 1)) continue;
                    uint64_t key = (uint64_t)a1 << 32;
                    // binary search first entry with A1
                    long L = 0, H = CL[cl].n;
                    while (L < H) { long M = (L + H) / 2; if (CL[cl].e[M] < key) L = M + 1; else H = M; }
                    for (long k = L; k < CL[cl].n && (CL[cl].e[k] >> 32) == a1; k++) {
                        const A2c *c = &A2L[CL[cl].e[k] & 0xffffffffu];
                        st->hits++;
                        Var v; mkvar(&v, A0, a1, c->a2, AX[3]);
                        Tr x, y; mkpair(&v, cv, &x, &y);
                        for (int i = 16; i < NR; i++) { x.w[i] = sched(&x, i); y.w[i] = sched(&y, i); }
                        for (int i = 0; i < 16; i++) { step(&x, i); step(&y, i); }
                        // sanity: rows -4..15 follow the cells (W cells only where they matter: 10, 11, 15)
                        int ok = aecells(&x, &y, -4, 15);
                        if (!ok || x.w[16] != G[gi]) { st->ymis++; continue; }
                        if (!inF7(x.w[7])) continue;
                        st->w7++;
                        int deep = 15;
                        for (int i = 16; i < NR; i++) { step(&x, i); step(&y, i); if (!rowok(&x, &y, i, 1)) break; deep = i; }
                        st->row[deep]++;
                        if (deep >= 17) { printf("ROW17+ deep %d cvidx %llu A0 %08x A1 %08x A2 %08x\n", deep, (unsigned long long)it, A0, a1, c->a2); fflush(stdout); }
                    }
                }
            }
        }
        { uint64_t hc = st->hits - h0; st->hist[hc > 256 ? 256 : hc]++; uint64_t wc = st->w7 - w0; st->w7hist[wc > 32 ? 32 : wc]++; }
    }
    return 0;
}
static uint32_t *EL[1024]; static long ELEN[1024];
static void *enum_worker(void *arg) {
    int id = (int)(long)arg; uint32_t *buf = malloc(4u << 26);
    for (int i = id; i < nA2; i += NT) { long n = enum_v(A0, &A2L[i], buf); EL[i] = malloc(4 * (n ? n : 1)); memcpy(EL[i], buf, 4 * n); ELEN[i] = n; }
    free(buf); return 0;
}
static double T0;
int main(int argc, char **argv) {
    A0 = strtoul(argv[1], 0, 16); NCV = strtoull(argv[2], 0, 10); SEED = strtoull(argv[3], 0, 10); NT = atoi(argv[4]);
    lib_init(); load_a2();
    FILE *f = fopen("F7.bm", "rb"); F7bm = malloc(1u << 29); fread(F7bm, 1, 1u << 29, f); fclose(f);
    f = fopen("G.txt", "r"); for (int i = 0; i < 32; i++) fscanf(f, "%x", &G[i]); fclose(f);
    // phi^{-1}
    PHO = calloc(1ULL << 32, 4); PHU = malloc(4ULL << 32);
    for (uint64_t u = 0; u < (1ULL << 32); u++) PHO[(uint32_t)(s0((uint32_t)u) - (uint32_t)u)]++;
    uint64_t acc = 0; for (uint64_t t = 0; t < (1ULL << 32); t++) { uint32_t c = PHO[t]; PHO[t] = (uint32_t)acc; acc += c; }
    uint32_t *fill = malloc(4ULL << 32); memcpy(fill, PHO, 4ULL << 32);
    for (uint64_t u = 0; u < (1ULL << 32); u++) { uint32_t t = s0((uint32_t)u) - (uint32_t)u; PHU[fill[t]++] = (uint32_t)u; }
    free(fill);
    fprintf(stderr, "phi^-1 built\n");
    // R(A0) by c9x class (per-A2 enumeration in parallel)
    nCL = 0; long total = 0;
    static uint32_t *lists[1024]; static long lens[1024];
    { pthread_t th[64]; for (int i = 0; i < NT; i++) pthread_create(&th[i], 0, enum_worker, (void*)(long)i);
      for (int i = 0; i < NT; i++) pthread_join(th[i], 0); }
    for (int i = 0; i < nA2; i++) {
        int cl; for (cl = 0; cl < nCL; cl++) if (CL[cl].c9x == A2L[i].c9x) break;
        if (cl == nCL) { CL[nCL].c9x = A2L[i].c9x; CL[nCL].e = 0; CL[nCL].n = 0; nCL++; }
        long n = ELEN[i]; total += n;
        CL[cl].e = realloc(CL[cl].e, 8 * (CL[cl].n + n));
        for (long k = 0; k < n; k++) CL[cl].e[CL[cl].n + k] = ((uint64_t)EL[i][k] << 32) | (uint32_t)i;
        CL[cl].n += n; free(EL[i]);
    }
    (void)lists; (void)lens;
    BLOOM = calloc(1ULL << 29, 8);
    for (int cl = 0; cl < nCL; cl++) {
        qsort(CL[cl].e, CL[cl].n, 8, cmpu64);
        for (long k = 0; k < CL[cl].n; k++) { uint64_t bk = bkey(cl, CL[cl].e[k] >> 32); BLOOM[bk >> 6] |= 1ULL << (bk & 63); }
    }
    fprintf(stderr, "|R(A0)| = %ld (2^%.4f), classes %d\n", total, log2((double)total), nCL);
    pthread_t th[64]; for (int i = 0; i < NT; i++) pthread_create(&th[i], 0, work, (void*)(long)i);
    for (int i = 0; i < NT; i++) pthread_join(th[i], 0);
    Stat T = {0}; for (int i = 0; i < NT; i++) { T.cv += ST[i].cv; T.hits += ST[i].hits; T.w7 += ST[i].w7; T.ymis += ST[i].ymis; for (int r = 0; r < 40; r++) T.row[r] += ST[i].row[r]; }
    for (int i = 0; i < NT; i++) { for (int k = 0; k < 257; k++) T.hist[k] += ST[i].hist[k]; for (int k = 0; k < 33; k++) T.w7hist[k] += ST[i].w7hist[k]; }
    printf("hits-per-CV histogram:"); for (int k = 0; k < 257; k++) if (T.hist[k]) printf(" %d:%llu", k, (unsigned long long)T.hist[k]); printf("\n");
    printf("W7-passes-per-CV histogram:"); for (int k = 0; k < 33; k++) if (T.w7hist[k]) printf(" %d:%llu", k, (unsigned long long)T.w7hist[k]); printf("\n");
    double eh = total * pow(2, -27);
    printf("A0 %08x: CVs %llu  hits %llu (per CV %.4f, expected %.4f)  mismatches %llu\n", A0, (unsigned long long)T.cv,
        (unsigned long long)T.hits, (double)T.hits / T.cv, eh, (unsigned long long)T.ymis);
    printf("W7 passes %llu (rate 2^%.4f, expected 2^-3.9020)\n", (unsigned long long)T.w7, log2((double)T.w7 / T.hits));
    uint64_t cum = T.w7; for (int r = 15; r < 24; r++) { printf("  passed through row %d: %llu\n", r, (unsigned long long)cum); cum -= T.row[r]; }
    return 0;
}
```

### B.6 truebucket.py

```python
# The counted program on true buckets: every row-16 hit of A0 3662dd58 for 400 real chaining values (pipe_dump.c),
# compared with the reference construction: entries (NE), W7 passes (NW), first row-17 test passes (N1).
import vt38 as V
from vt38 import M
E = V.emb(); j = E['A0'].index(0x3662dd58); A2 = E['A2']
cvs, hits = {}, {}
for line in open('dump_a.txt'):
    t = line.split()
    if t[0] == 'CV': cvs[int(t[1])] = [int(x, 16) for x in t[2:]]
    elif t[0] == 'HIT': hits.setdefault(int(t[1]), []).append((int(t[2], 16), int(t[3]), int(t[4])))
prog = V.program([j]); agree = dis = ent = nw = n1 = 0
for it, m0 in sorted(cvs.items()):
    cv = V.compress(V.IV, m0); hs = hits.get(it, [])
    for a1, k, gi in hs:
        var, _ = V.variant(E['A0'][j], a1, A2[k]); wx, _ = V.pair(cv, var)
        assert V.valid(var) and (V.s1(wx[14]) + wx[9] + V.s0(wx[1]) + wx[0]) & M == V.G[gi]
    ents = [V.entry(cv, j, a1, k) for a1, k, gi in hs]
    mach = V.Machine([1, 2], lambda jj, Y, Z0: ents, cvforce=cv); mach.run(prog)
    rnw = rn1 = 0
    for a1, k, gi in hs:
        r16, w7, deep, (tx, ty, wx, wy) = V.outcome(cv, E['A0'][j], a1, A2[k])
        if w7:
            rnw += 1; mE = V.GREC[gi][1]; vE = V.GREC[gi][2]
            rn1 += (tx[1][17] & mE) == vE
    got = (mach.r.get(V.RMAP['NE'], 0), mach.r.get(V.RMAP['NW'], 0), mach.r.get(V.RMAP['N1'], 0))
    ent += len(hs); nw += rnw; n1 += rn1
    if got == (len(hs), rnw, rn1) and mach.succ is None: agree += 1
    else: dis += 1; print('DIS', it, got, (len(hs), rnw, rn1))
print('CVs %d entries %d W7 passes %d first-test passes %d; counted program agrees on %d, disagrees on %d' % (len(cvs), ent, nw, n1, agree, dis))
```

### B.7 gset.c

```c
// G: all W16 (member x) for which row 16 holds (cells + two-bit conditions keyed at row 16), with the fixed
// rows 12..15 of S and L*.  Also prints dW16 and checks the published pair end to end.
#include <stdio.h>
#include <stdlib.h>
#include "core.h"
int main(void) {
    Var v; mkvar(&v, AX[0], AX[1], AX[2], AX[3]);
    printf("orig valid %d\n", var_valid(&v));
    // published pair check: rows -4..37
    Tr x, y; mkpair(&v, (uint32_t[8]){0xcd278980,0x1b12a052,0xb87cc8a6,0xa9e059c5,0xc9c3db85,0x6ca4b5b5,0x63d13ac1,0xc0329f1e}, &x, &y);
    for (int i = 16; i < NR; i++) { x.w[i] = sched(&x, i); y.w[i] = sched(&y, i); }
    for (int i = 0; i < NR; i++) { step(&x, i); step(&y, i); }
    int bad = 0; for (int i = 0; i < NR; i++) if (!rowok(&x, &y, i, i >= 16 || i == 15 || i == 10 || i == 11)) { printf("row %d fails\n", i); bad++; }
    printf("published pair rows ok: %s\n", bad ? "NO" : "yes");
    uint32_t dW16 = x.w[16] - y.w[16];
    printf("dW16 = %08x  W16x(pub) = %08x\n", dW16, x.w[16]);
    // enumerate W16x
    uint64_t n = 0; FILE *fo = fopen("G.txt", "w");
    for (uint64_t w = 0; w < (1ULL << 32); w++) {
        x.w[16] = (uint32_t)w; y.w[16] = (uint32_t)w - dW16;
        step(&x, 16); step(&y, 16);
        if (rowok(&x, &y, 16, 1)) { n++; fprintf(fo, "%08x\n", (uint32_t)w); }
    }
    fclose(fo);
    printf("|G| = %llu\n", (unsigned long long)n);
    return 0;
}
```

### B.8 fset.c

```c
// F7 = {w : s0(w + d7) - s0(w) = t7}: write a 2^32-bit bitmap and print |F7|.
#include <stdio.h>
#include <stdlib.h>
#include "core.h"
int main(void) {
    uint32_t d7 = WY[7] - WX[7], t7 = s0(WY[7]) - s0(WX[7]);
    printf("d7 = %08x t7 = %08x\n", d7, t7);
    uint8_t *bm = calloc(1u << 29, 1); uint64_t n = 0;
    for (uint64_t w = 0; w < (1ULL << 32); w++) if (s0((uint32_t)w + d7) - s0((uint32_t)w) == t7) { bm[w >> 3] |= 1 << (w & 7); n++; }
    printf("|F7| = %llu (2^%.5f)\n", (unsigned long long)n, __builtin_log2((double)n) - 32);
    FILE *f = fopen("F7.bm", "wb"); fwrite(bm, 1, 1u << 29, f); fclose(f);
    return 0;
}
```

### B.9 phimax.c

```c
#include "lib.h"
int main(void) {
    uint8_t *cnt = calloc(1ULL << 32, 1);
    for (uint64_t u = 0; u < (1ULL << 32); u++) { uint32_t t = s0((uint32_t)u) - (uint32_t)u; if (cnt[t] < 255) cnt[t]++; }
    uint64_t h[256] = {0}; int mx = 0;
    for (uint64_t t = 0; t < (1ULL << 32); t++) { h[cnt[t]]++; if (cnt[t] > mx) mx = cnt[t]; }
    printf("max |phi^-1(t)| = %d; histogram:", mx); for (int k = 0; k <= mx; k++) printf(" %d:%llu", k, (unsigned long long)h[k]); printf("\n");
    return 0;
}
```

### B.10 v9all.c

```c
// For each A2 candidate (chunk): enumerate A1 passing all A0-independent validity conditions; histogram
// F = W8x + A0 (the A0-free part of W8x).  Output (F, count) pairs per A2 chunk to a binary file.
// A0-independent conditions: E5/E6 '+', dW8 (A0 cancels), dW9, ds0(W9), and (A2-only, prechecked) E6 cells,
// E7/E6 '+', dW10, ds0(W10).  The remaining A0-dependent condition is ds0(W8) (Good8).
#include <stdio.h>
#include <stdlib.h>
#include "core.h"
static int cmp(const void *a, const void *b) { uint32_t x = *(uint32_t*)a, y = *(uint32_t*)b; return x < y ? -1 : x > y; }
int main(int argc, char **argv) {
    int lo = atoi(argv[1]), hi = atoi(argv[2]); char fn[64]; sprintf(fn, "fh_%03d_%03d.bin", lo, hi);
    FILE *fi = fopen("a2cand.bin", "rb"), *fo = fopen(fn, "wb"); uint32_t r[3]; int k = 0;
    uint32_t D8 = WX[8] - WY[8], D9 = WX[9] - WY[9], T9 = s0(WX[9]) - s0(WY[9]);
    uint32_t *buf = malloc(4u << 26);
    while (fread(r, 4, 3, fi) == 3) {
        if (k >= lo && k < hi) {
            uint32_t a2 = r[0]; long n = 0;
            uint32_t e6 = AX[6] + a2 - S0(AX[5]) - Mj(AX[5], AX[4], AX[3]);
            for (uint64_t a1 = 0; a1 < (1ULL << 32); a1++) {
                uint32_t A1 = (uint32_t)a1, w8[2], w9[2], e5x = 0;
                for (int m = 0; m < 2; m++) {
                    const uint32_t *A = m ? AY : AX, *E = m ? EY : EX;
                    uint32_t e4 = A[4] + 0 - S0(A[3]) - Mj(A[3], a2, A1);        // A0 = 0
                    uint32_t e5 = A[5] + A1 - S0(A[4]) - Mj(A[4], A[3], a2);
                    if (!m) e5x = e5;
                    w8[m] = E[8] - A[4] - e4 - S1(E[7]) - Ch(E[7], e6, e5) - KK[8];
                    w9[m] = E[9] - A[5] - e5 - S1(E[8]) - Ch(E[8], E[7], e6) - KK[9];
                }
                if ((e6 ^ e5x) & CP[6]) continue;
                if (w8[0] - w8[1] != D8 || w9[0] - w9[1] != D9 || s0(w9[0]) - s0(w9[1]) != T9) continue;
                buf[n++] = w8[0];   // = F (W8x at A0 = 0); W8x(A0) = F - A0
            }
            qsort(buf, n, 4, cmp);
            long i = 0; uint32_t hdr[2] = {(uint32_t)k, 0}; long npos = ftell(fo); fwrite(hdr, 4, 2, fo); uint32_t nd = 0;
            while (i < n) { long j = i; while (j < n && buf[j] == buf[i]) j++; uint32_t rec[2] = {buf[i], (uint32_t)(j - i)}; fwrite(rec, 4, 2, fo); nd++; i = j; }
            long end = ftell(fo); fseek(fo, npos, SEEK_SET); hdr[1] = nd; fwrite(hdr, 4, 2, fo); fseek(fo, end, SEEK_SET);
            fprintf(stderr, "A2 #%d %08x: V9 %ld distinct F %u\n", k, a2, n, nd);
        }
        k++;
    }
    fclose(fo); return 0;
}
```

### B.11 a0exact.c

```c
// Exact |R(A0)| for a list of A0 (stdin), multi-threaded over the F histogram.
#include <pthread.h>
#include <glob.h>
#include "lib.h"
typedef struct { uint32_t f, n; } Rec;
static Rec *R; static size_t nR; static uint32_t *A0s; static uint64_t *SC; static int nA, NT;
static void *w(void *arg) { int id = (int)(long)arg;
    for (int i = id; i < nA; i += NT) { uint64_t s = 0; uint32_t a = A0s[i]; for (size_t k = 0; k < nR; k++) if (good8(R[k].f - a)) s += R[k].n; SC[i] = s; }
    return 0; }
int main(int argc, char **argv) {
    lib_init(); NT = atoi(argv[1]);
    glob_t g; glob("fh_*.bin", 0, 0, &g); size_t cap = 1 << 26; R = malloc(cap * sizeof(Rec)); nR = 0;
    for (size_t i = 0; i < g.gl_pathc; i++) { FILE *f = fopen(g.gl_pathv[i], "rb"); uint32_t hdr[2];
        while (fread(hdr, 4, 2, f) == 2) for (uint32_t j = 0; j < hdr[1]; j++) { if (nR == cap) { cap *= 2; R = realloc(R, cap * sizeof(Rec)); } fread(&R[nR++], 8, 1, f); }
        fclose(f); }
    A0s = malloc(4 * 100000); nA = 0; char line[256]; while (fgets(line, sizeof line, stdin)) A0s[nA++] = strtoul(line, 0, 16);
    SC = calloc(nA, 8);
    pthread_t th[64]; for (int i = 0; i < NT; i++) pthread_create(&th[i], 0, w, (void*)(long)i); for (int i = 0; i < NT; i++) pthread_join(th[i], 0);
    for (int i = 0; i < nA; i++) printf("%08x %llu %.5f\n", A0s[i], (unsigned long long)SC[i], __builtin_log2((double)SC[i]));
    return 0;
}
```

### B.12 varsample.c

```c
// Uniform sample of variants (A0, A1, A2) from the union of R(A0) over an A0 list (weights = exact |R(A0)|).
// Record: A0 A1 A2 W8x W8y W9x W9y W10x W10y c7x (10 words).  usage: varsample a0file nA0 nsamples seed out
#include "lib.h"
int main(int argc, char **argv) {
    lib_init(); load_a2();
    FILE *f = fopen(argv[1], "r"); int m = atoi(argv[2]); long ns = atol(argv[3]); uint64_t s = strtoull(argv[4], 0, 10);
    uint32_t a0[4096]; double w[4096], tot = 0; char line[256];
    for (int i = 0; i < m && fgets(line, sizeof line, f); i++) { unsigned long long sc; sscanf(line, "%x %llu", &a0[i], &sc); w[i] = (double)sc; tot += w[i]; }
    fclose(f);
    FILE *fo = fopen(argv[5], "wb"); long tries = 0;
    for (long k = 0; k < ns; ) {
        double r = (double)(smx(&s) >> 11) / 9007199254740992.0 * tot; int j = 0; while (j < m - 1 && r >= w[j]) { r -= w[j]; j++; }
        for (;;) {
            const A2c *c = &A2L[smx(&s) % nA2]; uint32_t a1 = a1_start(c) + (uint32_t)(smx(&s) & ((1u << 29) - 1)); tries++;
            if (!valid3(a0[j], a1, c)) continue;
            Var v; mkvar(&v, a0[j], a1, c->a2, AX[3]);
            if (!var_valid(&v)) { fprintf(stderr, "inconsistent\n"); return 1; }
            uint32_t rec[10] = {a0[j], a1, c->a2, v.W[0][8], v.W[1][8], v.W[0][9], v.W[1][9], v.W[0][10], v.W[1][10], v.c7[0]};
            fwrite(rec, 4, 10, fo); k++; break;
        }
    }
    fclose(fo); fprintf(stderr, "%ld samples, %ld tries\n", ns, tries);
    return 0;
}
```

### B.13 static_costs.py

```python
# Static path costs of the counted program (vt38.py): straight-line costs to every exit.
import vt38 as V
COST = lambda op: 2 if op in ('bz', 'bnz', 'bne') else (0 if op in ('succ', 'halt_ok', 'obs') else 1)   # obs: zero-cost observation hook
p = V.program([0], alloc=False); L = p.lab
lab = lambda pre: [k for k in L if k.startswith(pre)][0]
def walk(start, stop_ops=('bz', 'bnz', 'bne', 'jmp', 'succ', 'halt_ok'), end=None):
    acc, ex = 0, []
    for pc in range(start, end if end is not None else len(p.c)):
        ins = p.c[pc]; acc += COST(ins[0])
        if ins[0] in stop_ops: ex.append((ins[0], acc))
        if ins[0] in ('jmp', 'succ', 'halt_ok'): break
    return ex
bstart = max(pc for pc, ins in enumerate(p.c) if ins[0] == 'add' and ins[1] == 'gk') + 1
print('prologue ops (f38 = 1 unit not included):', sum(COST(i[0]) for i in p.c[:bstart]) - 1)
print('block head to bz:', walk(bstart)[0][1], '; END:', 1)
print('entry: loop..bnz FL:', walk(L[lab('loop')])[0][1], '; back..bne:', walk(L[lab('back')])[0][1])
r = walk(L[lab('r17')], end=L[lab('deep')])
print('row-17 path exits (cumulative):', [e[1] for e in r])
d = walk(L[lab('deep')], stop_ops=('bne', 'bnz', 'succ'))
d = []; acc = 0
for pc in range(L[lab('deep')], len(p.c)):
    ins = p.c[pc]; acc += COST(ins[0])
    if ins[0] in ('bne', 'bnz', 'succ'): d.append(acc)
    if ins[0] == 'succ': break
print('deep path: %d exits, first %d, success %d' % (len(d), d[0], d[-1]))
```

### B.14 emu.py

```python
#!/usr/bin/env python3
# Emulate the organizer's python-message-pairs-v1 run of experiments/vt38.py: request built with the repository's
# runner (seed protocol), program executed twice (byte-identity), output validated, returned pairs checked with
# the repository verifier's selected-target digest.  usage: emu.py <experiment-id> <seed-string> [holdout]
import sys, os, json, time, subprocess, hashlib
REPO = os.environ.get('HASHSMASH_REPO', '.')   # a hash-smash checkout
sys.path.insert(0, REPO)
from experiments import runner
from verifier.frontier_tracks import get_frontier_track
from verifier.hash_functions import digest
eid, seed = sys.argv[1], sys.argv[2]; nonce = sys.argv[3] if len(sys.argv) > 3 else None
prog = REPO + '/lanes/exploratory/candidates/sha256-r38/experiments/vt38.py'
cfg = get_frontier_track('sha256-r38-exploratory').config_sha256()
sm = runner._canonical({"domain": "hashsmash-experiments-v1", "seed": seed, "holdout_nonce": nonce, "target_config_sha256": cfg})
req = {"schema_version": 1, "experiment_id": eid, "target_profile": "sha256-r38-prefix-v1", "event": {"kind": "full-collision"},
       "max_message_bytes": 4096, "trials": [{"trial": i, "seed": runner._trial_seed(sm, eid, i)} for i in range(256)]}
outs = []; times = []
for _ in range(2):
    t0 = time.time(); p = subprocess.run([sys.executable, '-I', prog], input=json.dumps(req).encode(), capture_output=True, timeout=300)
    times.append(time.time() - t0); assert p.returncode == 0, p.stderr.decode()[-2000:]; outs.append(p.stdout)
res = runner._strict_json(outs[0]); assert len(res['trials']) == 256
ret = coll = 0; obs = []
for i, row in enumerate(res['trials']):
    assert row['trial'] == i and set(row) <= {'trial', 'message_a_hex', 'message_b_hex', 'observations'}
    o = row.get('observations', {}); assert len(o) <= 16 and all(type(v) in (int, float, bool) for v in o.values())
    obs.append(o)
    if row['message_a_hex'] is not None:
        ret += 1; a, b = bytes.fromhex(row['message_a_hex']), bytes.fromhex(row['message_b_hex'])
        coll += a != b and digest(a, 'sha256', 38) == digest(b, 'sha256', 38)
print(json.dumps(dict(experiment=eid, seed=seed, returned_pairs=ret, full_collisions=coll, identical=outs[0] == outs[1],
    seconds=[round(t, 2) for t in times], stdout_sha256=hashlib.sha256(outs[0]).hexdigest()[:16], obs20=obs[20] if len(obs) > 20 else None,
    sum_mismatches=sum(o.get('mismatches', 0) for o in obs), sum_w7=sum(o.get('w7_passes', 0) for o in obs),
    sum_failed=sum(o.get('failed_rebuilds', 0) for o in obs), sum_tail=sum(o.get('tail_successes', 0) for o in obs))))
```

### B.15 r38.py

```python
#!/usr/bin/env python3
"""Reduced SHA-256 (38 steps), the ePrint 2026/1120 38-step characteristic (Table 3) and SFS pair (Table 5).

Conventions: step i computes E_i, A_i from (A_{i-1..i-4}, E_{i-1..i-4}); (A_{-1..-4}, E_{-1..-4}) = cv words
(a,b,c,d,e,f,g,h).  Characteristic strings are MSB first; member x = the message the paper prints second (M'),
'u' = (x,y) bits (1,0), 'n' = (0,1), '0'/'1' fixed equal, '=' equal, '+' in rows i-1 and i at bit b means
E_i[b] = E_{i-1}[b].
"""
import struct

M32 = 0xffffffff
K = [0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,0xd807aa98,0x12835b01,
     0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,
     0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,
     0x06ca6351,0x14292967,0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,
     0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,0x19a4c116,0x1e376c08,
     0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,
     0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2]
IV = [0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19]
R = 38

def ror(x, n): return ((x >> n) | (x << (32 - n))) & M32
def S0(x): return ror(x, 2) ^ ror(x, 13) ^ ror(x, 22)
def S1(x): return ror(x, 6) ^ ror(x, 11) ^ ror(x, 25)
def s0(x): return ror(x, 7) ^ ror(x, 18) ^ (x >> 3)
def s1(x): return ror(x, 17) ^ ror(x, 19) ^ (x >> 10)
def CH(x, y, z): return (x & y) ^ (~x & z & M32)
def MAJ(x, y, z): return (x & y) ^ (x & z) ^ (y & z)

def expand(w16, r=R):
    w = list(w16)
    for i in range(16, r): w.append((s1(w[i-2]) + w[i-7] + s0(w[i-15]) + w[i-16]) & M32)
    return w

def compress(cv, w16, r=R):
    w = expand(w16, r)
    a, b, c, d, e, f, g, h = cv
    for i in range(r):
        t1 = (h + S1(e) + CH(e, f, g) + K[i] + w[i]) & M32
        t2 = (S0(a) + MAJ(a, b, c)) & M32
        a, b, c, d, e, f, g, h = (t1 + t2) & M32, a, b, c, (d + t1) & M32, e, f, g
    return [(x + y) & M32 for x, y in zip(cv, (a, b, c, d, e, f, g, h))]

def pad_blocks(msg):
    n = len(msg)
    p = msg + b'\x80' + b'\x00' * ((55 - n) % 64) + struct.pack('>Q', 8 * n)
    return [list(struct.unpack('>16I', p[i:i+64])) for i in range(0, len(p), 64)]

def digest(msg, r=R):
    cv = list(IV)
    for blk in pad_blocks(msg): cv = compress(cv, blk, r)
    return struct.pack('>8I', *cv)

def trace(cv, w16, r=R):
    A = {-1: cv[0], -2: cv[1], -3: cv[2], -4: cv[3]}; E = {-1: cv[4], -2: cv[5], -3: cv[6], -4: cv[7]}
    W = expand(w16, r)
    for i in range(r):
        E[i] = (A[i-4] + E[i-4] + S1(E[i-1]) + CH(E[i-1], E[i-2], E[i-3]) + K[i] + W[i]) & M32
        A[i] = (E[i] - A[i-4] + S0(A[i-1]) + MAJ(A[i-1], A[i-2], A[i-3])) & M32
    return A, E, W

# Table 3 of ePrint 2026/1120 (38 steps), transcribed MSB first; unlisted rows are all '='.
CHAR = dict(
 A={7:'=nu=============================',8:'=========n=====n====n======u====',11:'====================u=======un==',
    12:'=u===n====n======u===nu=======n=',13:'==n============n================',14:'====u=========nn========u==u====',
    15:'======n=u=======n===============',17:'==u============================='},
 E={5:'+++=============================',6:'+++=1====0==+1=====0+===1==1====',7:'uuu=0+1=11=0+00====1+===0==00=01',
    8:'100=u+010n=1nu01=01nu=00n11u1=01',9:'11000u1=n11u0000101101110=01u0uu',10:'==1010=01u00001u=010u=101==10111',
    11:'1=n000=0111100101unn00011+111u10',12:'01nuuu=110n111nu000100100+010u1n',13:'00110101110=000u00111nuu+nnnu1n1',
    14:'=010n0===00===1n=11+0100+1110001',15:'=1==1=1==0=1==11===+u011n1011=1=',16:'=u==10===n===+u1===n0=u=1==+====',
    17:'=0=====+00===+0=+==01=0=0==+====',18:'=0=====+01===n1=+==1==1===0u====',19:'==11===nn====1==n===010===11==0=',
    20:'==1====00====1==0==========1====',21:'==u====10=======1===10==========',22:'==0=============================',
    23:'==1============================='},
 W={7:'==n=============================',8:'=====u===u==========n===========',9:'==u=============================',
    10:'=====n=u=======n===n==n=n=n=u=u=',11:'============u======u=u==========',15:'=====u===n==========n===========',
    16:'==u=============================',23:'=====1=uu=====1=u=1=============',25:'==n============================='})
# Table 4 two-bit conditions as printed, with W25[4]=W25[9] read as W25[4]=W25[6] (fails on the pair as printed).
TWOBIT = [('A',14,15,'=','A',16,15),('A',14,23,'=','A',16,23),('A',14,25,'=','A',16,25),('A',15,4,'=','A',16,4),
    ('A',15,7,'=','A',16,7),('A',15,16,'!','A',16,16),('A',15,17,'=','A',16,17),('A',15,27,'=','A',16,27),('A',15,29,'=','A',16,29),
    ('A',16,15,'=','A',17,15),('A',16,23,'=','A',17,23),('A',16,25,'=','A',17,25),('A',17,9,'=','A',17,20),
    ('A',17,6,'=','A',17,18),('A',17,8,'=','A',17,17),('A',16,29,'=','A',18,29),('A',18,29,'=','A',19,29),
    ('E',16,4,'!','E',16,23),('E',16,3,'!','E',16,8),('E',16,14,'=','E',16,28),('E',16,4,'=','E',17,4),('E',16,18,'=','E',17,18),
    ('E',18,0,'!','E',18,13),('E',17,15,'=','E',18,15),('E',17,24,'=','E',18,24),('E',19,6,'!','E',19,19),('E',19,20,'=','E',19,2),
    ('E',21,2,'=','E',21,16),
    ('W',7,8,'!','W',7,25),('W',7,14,'!','W',7,18),('W',7,1,'=','W',7,12),
    ('W',8,0,'!','W',8,28),('W',8,30,'!','W',8,9),('W',8,1,'=','W',8,18),
    ('W',16,1,'!','W',16,12),('W',16,20,'!','W',16,27),('W',16,8,'=','W',16,25),('W',16,14,'=','W',16,18),('W',16,4,'!','W',16,6),('W',16,22,'!','W',16,31),
    ('W',23,0,'!','W',23,30),('W',23,1,'!','W',23,31),('W',23,14,'=','W',23,21),('W',23,16,'=','W',23,25),
    ('W',25,4,'=','W',25,6),('W',25,22,'=','W',25,31),('W',25,20,'=','W',25,27)]

def _h(s): return [int(t, 16) for t in s.split()]
# Table 5: chaining value, M (printed first), M' (printed second = member x), printed hash.
PAIR = dict(cv=_h('cd278980 1b12a052 b87cc8a6 a9e059c5 c9c3db85 6ca4b5b5 63d13ac1 c0329f1e'),
  m=_h('48fc271b 9fca20cd cc89f96f fc40396f 8b328cb4 6b91ef78 97f9b767 e2450045 3b016f58 de9804cb 66a99ea5 0ce30b8d a28cd15a 77a1e994 d28e48a0 9b5f6dbb'),
  mp=_h('48fc271b 9fca20cd cc89f96f fc40396f 8b328cb4 6b91ef78 97f9b767 c2450045 3f416758 fe9804cb 63a88c0f 0ceb1f8d a28cd15a 77a1e994 d28e48a0 9f1f65bb'),
  hash=_h('5d9ca5f4 59ace3a3 26c9c26c 4252c585 4c0803b7 1b4d5ccd 25c3ccc0 90645c4d'))

def cell(s):
    """(m, v, d, p): x-value mask, x-values, XOR-difference mask, '+' mask."""
    m = v = d = p = 0
    for c, sym in enumerate(s):
        b = 31 - c
        if sym in '01un': m |= 1 << b
        if sym in '1u': v |= 1 << b
        if sym in 'un': d |= 1 << b
        if sym == '+': p |= 1 << b
    return m, v, d, p

def row(k, i): return cell(CHAR[k].get(i, '=' * 32))

def plus_mask(i):
    """Bits b with E_i[b] = E_{i-1}[b] required."""
    return row('E', i)[3] & row('E', i - 1)[3]

def cell_ok(k, i, x, y, xprev=None):
    m, v, d, p = row(k, i)
    if (x & m) != v or (x ^ y) != d: return False
    if k == 'E':
        q = plus_mask(i)
        if q and ((x ^ xprev) & q): return False
    return True

def bad_cells(cv, wx, wy, rows=range(-4, R)):
    Ax, Ex, Wx = trace(cv, wx); Ay, Ey, Wy = trace(cv, wy)
    bad = []
    for i in rows:
        if not cell_ok('A', i, Ax[i], Ay[i]): bad.append(('A', i))
        if not cell_ok('E', i, Ex[i], Ey[i], Ex.get(i - 1)): bad.append(('E', i))
        if i >= 0 and not cell_ok('W', i, Wx[i], Wy[i]): bad.append(('W', i))
    return bad, (Ax, Ex, Wx), (Ay, Ey, Wy)

def twobit_ok(tx, cond):
    A, E, W = tx
    k1, i1, b1, op, k2, i2, b2 = cond
    v1 = ({'A': A, 'E': E, 'W': W}[k1][i1] >> b1) & 1
    v2 = ({'A': A, 'E': E, 'W': W}[k2][i2] >> b2) & 1
    return (v1 == v2) if op == '=' else (v1 != v2)

if __name__ == '__main__':
    cv, mx, my = PAIR['cv'], PAIR['mp'], PAIR['m']
    hx, hy = compress(cv, mx), compress(cv, my)
    print('collision:', hx == hy, 'matches printed:', hx == PAIR['hash'])
    bad, tx, ty = bad_cells(cv, mx, my)
    print('bad cells:', bad)
    print('two-bit failures (x):', [c for c in TWOBIT if not twobit_ok(tx, c)])
    print('two-bit failures (y):', [c for c in TWOBIT if not twobit_ok(ty, c)])
```

### B.16 gen_consts.py

```python
import r38
cv, mx, my = r38.PAIR['cv'], r38.PAIR['mp'], r38.PAIR['m']
Ax, Ex, Wx = r38.trace(cv, mx); Ay, Ey, Wy = r38.trace(cv, my)
out = []
def arr(name, d, lo, hi):
    out.append('static const uint32_t %s[%d] = {%s};' % (name, hi - lo + 1, ','.join('0x%08x' % d[i] for i in range(lo, hi + 1))))
arr('AX', Ax, 0, 15); arr('AY', Ay, 0, 15); arr('EX', Ex, 0, 15); arr('EY', Ey, 0, 15)
arr('WX', {i: Wx[i] for i in range(38)}, 0, 37); arr('WY', {i: Wy[i] for i in range(38)}, 0, 37)
for k in 'AEW':
    for i in range(-4, 38):
        m, v, d, p = r38.row(k, i)
        pass
cells = []
for k in 'AEW':
    for i in range(0, 38):
        m, v, d, p = r38.row(k, i)
        q = r38.plus_mask(i) if k == 'E' else 0
        cells.append((k, i, m, v, d, q))
out.append('static const uint32_t CM[3][38] = {%s};' % ','.join('{' + ','.join('0x%08x' % c[2] for c in cells if c[0] == k) + '}' for k in 'AEW'))
out.append('static const uint32_t CV_[3][38] = {%s};' % ','.join('{' + ','.join('0x%08x' % c[3] for c in cells if c[0] == k) + '}' for k in 'AEW'))
out.append('static const uint32_t CD[3][38] = {%s};' % ','.join('{' + ','.join('0x%08x' % c[4] for c in cells if c[0] == k) + '}' for k in 'AEW'))
out.append('static const uint32_t CP[38] = {%s};' % ','.join('0x%08x' % c[5] for c in cells if c[0] == 'E'))
out.append('static const uint32_t KK[64] = {%s};' % ','.join('0x%08x' % x for x in r38.K))
open('consts.h', 'w').write('\n'.join(out) + '\n')
print('\n'.join(out[:4]))
```

### B.17 gen2.py

```python
# Emit two-bit conditions (member x) keyed by their later row, as C arrays.
import r38
KI = {'A': 0, 'E': 1, 'W': 2}
conds = sorted(r38.TWOBIT, key=lambda c: max(c[1], c[5]))
lines = ['#define NX %d' % len(conds),
 'static const int XK1[NX] = {%s};' % ','.join(str(KI[c[0]]) for c in conds),
 'static const int XI1[NX] = {%s};' % ','.join(str(c[1]) for c in conds),
 'static const int XB1[NX] = {%s};' % ','.join(str(c[2]) for c in conds),
 'static const int XNE[NX] = {%s};' % ','.join('1' if c[3] == '!' else '0' for c in conds),
 'static const int XK2[NX] = {%s};' % ','.join(str(KI[c[4]]) for c in conds),
 'static const int XI2[NX] = {%s};' % ','.join(str(c[5]) for c in conds),
 'static const int XB2[NX] = {%s};' % ','.join(str(c[6]) for c in conds),
 'static const int XROW[NX] = {%s};' % ','.join(str(max(c[1], c[5])) for c in conds)]
open('twobit.h', 'w').write('\n'.join(lines) + '\n')
print(len(conds), 'two-bit conditions; rows:', sorted(set(max(c[1], c[5]) for c in conds)))
```

### B.18 far2.c

```c
// Far pairs (H5): on chaining values CV1 where one variant v = (A0, A1, A2) succeeds fully (semi-free-start
// successes of the SMC, sfs files), find every other variant w of a set of NA <= 8 A0 values whose row 16 holds on
// the same CV1 (phi^{-1} probing, exactly as pipe.c), excluding v and the variants sharing (A0, A1) with v, and
// record how far w gets: W7 in F7, the first row-17 test (E17 x-mask), all of row 17, rows 18.., full success.
// Counts are kept per pair (A0 of v, A0 of w) and per success record.  The same is done on uniformly random
// chaining values as the unconditional baseline.  (far2.c = far.c with NA read from the file and per-pair counts.)
// usage: far2 a0file sfsfiles... ; env BASE=n for n random baseline chaining values, RECOUT, MATOUT for outputs
#include <pthread.h>
#include <math.h>
#include "lib.h"
#define MA 8
static uint32_t *PHO, *PHU; static uint8_t *F7bm;
static inline int inF7(uint32_t w) { return F7bm[w >> 3] >> (w & 7) & 1; }
static uint32_t G[32];
typedef struct { uint32_t c9x; uint64_t *e; long n; } Cls;
static int NA; static Cls CL[MA][256]; static int nCL[MA]; static uint32_t A0S[MA];
static uint64_t *BLOOM;
static inline uint64_t bkey(int a, int cl, uint32_t a1) { uint64_t k = ((uint64_t)(a * 256 + cl) << 32) | a1; k *= 0x9e3779b97f4a7c15ULL; return k >> 29; }
static int cmpu64(const void *x, const void *y) { uint64_t a = *(uint64_t*)x, b = *(uint64_t*)y; return a < b ? -1 : a > b; }
typedef struct { uint64_t cvs, ent, w7, t1, r17, deep[40], succ, mis; } St;   // per class: [0] same A0 as v, [1] other A0
typedef struct { uint64_t ent, w7, t1, r17; } PC;
static PC PCc[64][MA][MA], PCb[64][MA];   // per thread: [A0 of v][A0 of w] (successes); [A0 of w] (baseline)
static uint32_t (*SV)[11]; static long nSV;   // success records: a0 a1 a2 cv[8]
static int NT = 14; static St STc[64][2], STb[64][2]; static long NBASE;
// per success record: far W7 passes, first-test passes, row-17 passes; source file index
static uint32_t *RW7, *RT1, *R17; static int *RFILE;
static inline int aecell(const Tr *x, const Tr *y, int i) {
    uint32_t ax = AA(x,i), ay = AA(y,i), ex = EE(x,i), ey = EE(y,i);
    if ((ax & CM[0][i]) != CV_[0][i] || (ax ^ ay) != CD[0][i]) return 0;
    if ((ex & CM[1][i]) != CV_[1][i] || (ex ^ ey) != CD[1][i]) return 0;
    return !(CP[i] && ((ex ^ EE(x,i-1)) & CP[i]));
}
// first row-17 test: E17x & mE == vE (incl. '+' and E16 two-bit), as the counted program
static void probe(const uint32_t cv[8], int skip_a0, uint32_t skip_a1, St *S, long rec, int tid) {
    CVq q; cv_pre(cv, &q);
    for (int a = 0; a < NA; a++) {
        uint32_t Y, Z0, W0; cv_a0(&q, A0S[a], &Y, &Z0, &W0);
        for (int cl = 0; cl < nCL[a]; cl++) {
            uint32_t tb = Y + Z0 + CL[a][cl].c9x;
            for (int gi = 0; gi < 32; gi++) {
                uint32_t t = G[gi] - tb; uint64_t lo = PHO[t], hi = (t == 0xffffffffu) ? (1ULL << 32) : PHO[t + 1];
                for (uint64_t p = lo; p < hi; p++) {
                    uint32_t a1 = PHU[p] - Y; uint64_t bk = bkey(a, cl, a1);
                    if (!(BLOOM[bk >> 6] >> (bk & 63) & 1)) continue;
                    if (a == skip_a0 && a1 == skip_a1) continue;          // v itself and its same-(A0, A1) mates
                    uint64_t key = (uint64_t)a1 << 32; long L = 0, H = CL[a][cl].n;
                    while (L < H) { long Mi = (L + H) / 2; if (CL[a][cl].e[Mi] < key) L = Mi + 1; else H = Mi; }
                    for (long k = L; k < CL[a][cl].n && (CL[a][cl].e[k] >> 32) == a1; k++) {
                        const A2c *c = &A2L[CL[a][cl].e[k] & 0xffffffffu]; St *st = &S[a != skip_a0]; st->ent++;
                        PC *pc = rec >= 0 ? &PCc[tid][skip_a0][a] : &PCb[tid][a]; pc->ent++;
                        Var v; mkvar(&v, A0S[a], a1, c->a2, AX[3]); Tr x, y; mkpair(&v, cv, &x, &y);
                        if (!inF7(x.w[7])) continue;
                        st->w7++; pc->w7++; if (rec >= 0) RW7[rec]++;
                        for (int i = 16; i < NR; i++) { x.w[i] = sched(&x, i); y.w[i] = sched(&y, i); }
                        int cells = 1; for (int i = 0; i <= 17; i++) { step(&x, i); step(&y, i); if (i <= 16 && !aecell(&x, &y, i)) cells = 0; }
                        if (!cells || x.w[16] != G[gi]) { st->mis++; continue; }
                        // first test: x-value cells of E17, '+' with E16, E16-E17 two-bit conditions (bits 4, 18)
                        uint32_t e = EE(&x, 17), m = CM[1][17] | CP[17], val = CV_[1][17] | (EE(&x, 16) & CP[17]);
                        if ((e & m) != val) continue;
                        st->t1++; pc->t1++; if (rec >= 0) RT1[rec]++;
                        if (!rowok(&x, &y, 17, 1)) continue;
                        st->r17++; pc->r17++; if (rec >= 0) R17[rec]++; int deep = 17, ok = 1;
                        for (int i = 18; i < NR && ok; i++) { step(&x, i); step(&y, i); ok = rowok(&x, &y, i, 1); if (ok) deep = i; }
                        st->deep[deep]++; if (deep == NR - 1) st->succ++;
                    }
                }
            }
        }
    }
}
static void *wc(void *arg) {
    int id = (int)(long)arg;
    for (long i = id; i < nSV; i += NT) {
        uint32_t *r = SV[i]; int sa = -1; for (int a = 0; a < NA; a++) if (A0S[a] == r[0]) sa = a;
        if (sa < 0) continue;
        STc[id][0].cvs++; probe(r + 3, sa, r[1], STc[id], i, id);
    }
    return 0;
}
static void *wb(void *arg) {
    int id = (int)(long)arg; uint64_t s = 777 + id;
    for (long i = id; i < NBASE; i += NT) { uint32_t cv[8]; for (int j = 0; j < 8; j++) cv[j] = (uint32_t)smx(&s); STb[id][0].cvs++; probe(cv, -1, 0, STb[id], -1, id); }
    return 0;
}
static uint32_t *EL[1024]; static long ELEN[1024]; static int CUR_A;
static void *enum_worker(void *arg) {
    int id = (int)(long)arg; uint32_t *buf = malloc(4u << 26);
    for (int i = id; i < nA2; i += NT) { long n = enum_v(A0S[CUR_A], &A2L[i], buf); EL[i] = malloc(4 * (n ? n : 1)); memcpy(EL[i], buf, 4 * n); ELEN[i] = n; }
    free(buf); return 0;
}
static void report(const char *nm, St (*S)[2]) {
    uint64_t cvs = 0; for (int i = 0; i < NT; i++) cvs += S[i][0].cvs;
    for (int c = 0; c < 2; c++) {
        St T = {0}; for (int i = 0; i < NT; i++) { St *u = &S[i][c]; T.ent += u->ent; T.w7 += u->w7; T.t1 += u->t1; T.r17 += u->r17; T.succ += u->succ; T.mis += u->mis; for (int k = 0; k < 40; k++) T.deep[k] += u->deep[k]; }
        printf("%s [%s]: CVs %llu, row-16 variants %llu (%.4f per CV), cell mismatches %llu; W7 %llu (rate 2^%.4f, p2 2^-3.9020); first row-17 test %llu (rate 2^%.3f given W7, exact 2^-10; expected %.1f); row 17 %llu (expected %.2f at 2^-16.991 of W7 passes); deepest rows:",
            nm, c ? "other A0" : "same A0, other A1", (unsigned long long)cvs, (unsigned long long)T.ent, (double)T.ent / cvs, (unsigned long long)T.mis,
            (unsigned long long)T.w7, log2((double)T.w7 / T.ent), (unsigned long long)T.t1, log2((double)T.t1 / T.w7), T.w7 / 1024.0,
            (unsigned long long)T.r17, T.w7 * pow(2, -16.991));
        for (int k = 17; k < 40; k++) if (T.deep[k]) printf(" row%d:%llu", k, (unsigned long long)T.deep[k]);
        printf("; full successes %llu\n", (unsigned long long)T.succ);
    }
}
int main(int argc, char **argv) {
    lib_init(); load_a2(); NBASE = getenv("BASE") ? atol(getenv("BASE")) : 0;
    FILE *f = fopen(argv[1], "r"); char line[512]; NA = 0; while (NA < MA && fgets(line, sizeof line, f)) A0S[NA++] = strtoul(line, 0, 16); fclose(f);
    f = fopen("F7.bm", "rb"); F7bm = malloc(1u << 29); fread(F7bm, 1, 1u << 29, f); fclose(f);
    f = fopen("G.txt", "r"); for (int i = 0; i < 32; i++) fscanf(f, "%x", &G[i]); fclose(f);
    long cap = 1 << 20; SV = malloc(cap * 44); nSV = 0;
    for (int k = 2; k < argc; k++) { f = fopen(argv[k], "r"); while (fgets(line, sizeof line, f)) { if (nSV == cap) { cap *= 2; SV = realloc(SV, cap * 44); }
        char *p = line; for (int j = 0; j < 11; j++) SV[nSV][j] = (uint32_t)strtoul(p, &p, 16); RFILE = realloc(RFILE, sizeof(int) * cap); RFILE[nSV] = k; nSV++; } fclose(f); }
    fprintf(stderr, "%ld successes\n", nSV); RW7 = calloc(nSV, 4); RT1 = calloc(nSV, 4); R17 = calloc(nSV, 4);
    PHO = calloc(1ULL << 32, 4); PHU = malloc(4ULL << 32);
    for (uint64_t u = 0; u < (1ULL << 32); u++) PHO[(uint32_t)(s0((uint32_t)u) - (uint32_t)u)]++;
    uint64_t acc = 0; for (uint64_t t = 0; t < (1ULL << 32); t++) { uint32_t c = PHO[t]; PHO[t] = (uint32_t)acc; acc += c; }
    uint32_t *fill = malloc(4ULL << 32); memcpy(fill, PHO, 4ULL << 32);
    for (uint64_t u = 0; u < (1ULL << 32); u++) { uint32_t t = s0((uint32_t)u) - (uint32_t)u; PHU[fill[t]++] = (uint32_t)u; }
    free(fill);
    BLOOM = calloc(1ULL << 29, 8);
    for (int a = 0; a < NA; a++) {
        CUR_A = a; pthread_t th[64]; for (int i = 0; i < NT; i++) pthread_create(&th[i], 0, enum_worker, (void*)(long)i); for (int i = 0; i < NT; i++) pthread_join(th[i], 0);
        nCL[a] = 0; long total = 0;
        for (int i = 0; i < nA2; i++) {
            int cl; for (cl = 0; cl < nCL[a]; cl++) if (CL[a][cl].c9x == A2L[i].c9x) break;
            if (cl == nCL[a]) { CL[a][cl].c9x = A2L[i].c9x; CL[a][cl].e = 0; CL[a][cl].n = 0; nCL[a]++; }
            long n = ELEN[i]; total += n; CL[a][cl].e = realloc(CL[a][cl].e, 8 * (CL[a][cl].n + n));
            for (long k = 0; k < n; k++) CL[a][cl].e[CL[a][cl].n + k] = ((uint64_t)EL[i][k] << 32) | (uint32_t)i;
            CL[a][cl].n += n; free(EL[i]);
        }
        for (int cl = 0; cl < nCL[a]; cl++) { qsort(CL[a][cl].e, CL[a][cl].n, 8, cmpu64);
            for (long k = 0; k < CL[a][cl].n; k++) { uint64_t bk = bkey(a, cl, CL[a][cl].e[k] >> 32); BLOOM[bk >> 6] |= 1ULL << (bk & 63); } }
        fprintf(stderr, "A0 %08x: |R| = %ld\n", A0S[a], total);
    }
    pthread_t th[64];
    for (int i = 0; i < NT; i++) pthread_create(&th[i], 0, wc, (void*)(long)i); for (int i = 0; i < NT; i++) pthread_join(th[i], 0);
    report("conditional on a success of v", STc);
    { FILE *o = fopen(getenv("MATOUT") ? getenv("MATOUT") : "far_mat.txt", "w");
      for (int x = 0; x < NA; x++) for (int y = 0; y < NA; y++) { PC t = {0}; for (int i = 0; i < NT; i++) { t.ent += PCc[i][x][y].ent; t.w7 += PCc[i][x][y].w7; t.t1 += PCc[i][x][y].t1; t.r17 += PCc[i][x][y].r17; }
          uint64_t nv = 0; for (long r = 0; r < nSV; r++) nv += SV[r][0] == A0S[x];
          fprintf(o, "pair v %08x w %08x successes %llu entries %llu w7 %llu t1 %llu r17 %llu\n", A0S[x], A0S[y], (unsigned long long)nv, (unsigned long long)t.ent, (unsigned long long)t.w7, (unsigned long long)t.t1, (unsigned long long)t.r17); }
      fclose(o); }
    { FILE *o = fopen(getenv("RECOUT") ? getenv("RECOUT") : "far_rec.txt", "w"); for (long i = 0; i < nSV; i++) fprintf(o, "%d %u %u %u\n", RFILE[i], RW7[i], RT1[i], R17[i]); fclose(o); }
    if (NBASE) { for (int i = 0; i < NT; i++) pthread_create(&th[i], 0, wb, (void*)(long)i); for (int i = 0; i < NT; i++) pthread_join(th[i], 0); report("baseline, random CV", STb);
      FILE *o = fopen(getenv("MATOUT") ? getenv("MATOUT") : "far_mat.txt", "a");
      for (int y = 0; y < NA; y++) { PC t = {0}; for (int i = 0; i < NT; i++) { t.ent += PCb[i][y].ent; t.w7 += PCb[i][y].w7; t.t1 += PCb[i][y].t1; t.r17 += PCb[i][y].r17; }
          fprintf(o, "base w %08x cvs %ld entries %llu w7 %llu t1 %llu r17 %llu\n", A0S[y], NBASE, (unsigned long long)t.ent, (unsigned long long)t.w7, (unsigned long long)t.t1, (unsigned long long)t.r17); }
      fclose(o); }
    return 0;
}
```

### B.19 far_bound2.py

```python
#!/usr/bin/env python3
# far_bound2.py - the H5 far term from far2.c over NA A0 values (proof.md 6.5).  Inputs: the per-record file (source
# file index = seed, far W7 passes, first-test passes, row-17 passes) and the per-pair matrix (A0 of v, A0 of w).
# D_far = E[number of far w passing rows 16, W7 and 17 | A_v] bounds E[number of far w succeeding | A_v].  Per
# success: E_same (w with v's A0, other A1) + 255 x E_other (per other A0, averaged over the NA - 1 measured ones).
# Bounds: Poisson at 99.5% per class (99% jointly); seed-clustered: the number of seeds with at least one event
# (Poisson 99.5%) times the largest number of events in one seed, all scaled by 255/(NA - 1) (conservative for
# the same-A0 class, whose factor is 1).
import math, sys

def poisson_ub(k, conf):
    cdf = lambda lam: sum(math.exp(-lam + i * math.log(lam) - math.lgamma(i + 1)) for i in range(k + 1))
    lo, hi = 0.0, 10.0 * (k + 5)
    for _ in range(200):
        mid = (lo + hi) / 2
        if cdf(mid) > 1 - conf: lo = mid
        else: hi = mid
    return hi

rec = [list(map(int, l.split())) for l in open(sys.argv[1])]
mat = [l.split() for l in open(sys.argv[2]) if l.startswith('pair')]
n = len(rec)
A = sorted({r[2] for r in mat}); NA = len(A)
hd = lambda a, b: bin(int(a, 16) ^ int(b, 16)).count('1')
# pair line: pair v A w B successes S entries E w7 W t1 T r17 R
same = sum(int(r[14]) for r in mat if r[2] == r[4]); other = sum(int(r[14]) for r in mat if r[2] != r[4])
assert same + other == sum(r[3] for r in rec), (same, other, sum(r[3] for r in rec))
print('conditioning successes %d over %d A0; far row-17 passes: same A0 %d, other A0 %d (pairs over %d other A0 per success)'
      % (n, NA, same, other, NA - 1))
# rates by Hamming-distance band of (A0 of v, A0 of w)
for lo_, hi_ in ((0, 0), (1, 3), (4, 6), (7, 9)):
    rows = [r for r in mat if lo_ <= hd(r[2], r[4]) <= hi_]
    if not rows: continue
    succ = sum(int(r[6]) for r in rows); ent = sum(int(r[8]) for r in rows); w7 = sum(int(r[10]) for r in rows)
    t1 = sum(int(r[12]) for r in rows); r17 = sum(int(r[14]) for r in rows)
    print('  HD %d..%d: %2d pairs, entries per (success, A0 of w) %.4f, W7 rate 2^%.4f, first-test rate 2^%.3f, row-17 passes %d (expected %.2f at 2^-16.991)'
          % (lo_, hi_, len(rows), ent / succ, math.log2(w7 / ent), math.log2(t1 / w7) if t1 else float('nan'),
             r17, w7 * 2 ** -16.991))
f = 255 / (NA - 1)
pt = (same + f * other) / n
ub = (poisson_ub(same, 0.995) + f * poisson_ub(other, 0.995)) / n
by_seed = {}
for r in rec: by_seed[r[0]] = by_seed.get(r[0], 0) + r[3]
ev = [v for v in by_seed.values() if v]
kmax = max(ev or [0]); ns = len(ev)
cl = (poisson_ub(ns, 0.995) * kmax) * f / n if ns else poisson_ub(0, 0.995) * f / n
print('seeds %d, seeds with events %d, largest per seed %d, records with two or more %d'
      % (len(by_seed), ns, kmax, sum(1 for r in rec if r[3] >= 2)))
print('D_far: point %.6f; 99%% bound (Poisson, 0.5%% per class) %.6f; seed-clustered bound %.6f; ledger value 1/200 = 0.005'
      % (pt, ub, cl))
```

### B.20 ram_check.py

```python
#!/usr/bin/env python3
# ram_check.py - the counted online program (experiments/vt38.py) on semi-free-start successes of the SMC
# (proof.md 6.2): for N successes drawn with a seeded RNG from the given .sfs files, the success's chaining value is
# forced, the bucket of its A0 block holds a decoy, the true entry and the decoy, and the program must halt with the
# true entry after its own row-17 and deep-path tests; the reference construction must agree (rows 16..37, W7 in F7)
# and the pair must collide under the 38-step compression.  usage: ram_check.py N seed sfsfiles...
import sys, os, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vt38 as V
N, seed, files = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3:]
recs = [l.split() for f in sorted(files) for l in open(f)]
pick = random.Random(seed).sample(range(len(recs)), min(N, len(recs)))
E = V.emb(); a0i = {a: j for j, a in enumerate(E['A0'])}; a2i = {a: k for k, a in enumerate(E['A2'])}
good = bad = 0; js = set()
for i in pick:
    t = [int(x, 16) for x in recs[i][:11]]
    a0, a1, a2 = t[:3]; cv = t[3:11]; j, k = a0i[a0], a2i[a2]; js.add(j)
    r16, w7, deep, (tx, ty, wx, wy) = V.outcome(cv, a0, a1, a2)
    true = V.entry(cv, j, a1, k); dec = V.entry(cv, j, *E['A0P'][j])
    m = V.Machine([1, 2], lambda jj, Y, Z0: [dec, true, dec], cvforce=cv); m.run(V.program([j]))
    ok = r16 and w7 and deep == V.R - 1 and m.succ == (j, true) and V.compress(cv, wx) == V.compress(cv, wy) and wx != wy
    good += ok; bad += not ok
print('ram_check: %d successes (of %d), %d distinct A0: %d found and verified by the counted program, %d not' % (len(pick), len(recs), len(js), good, bad))
```

### B.21 v3_stats.py

```python
#!/usr/bin/env python3
# v3_stats.py - summary of a set of smc3 runs (PREREG_v3 rules): mean, relative sd, one-sided 99% Student bound,
# stage means and their spread, tail successes, failed rebuilds, clumping replay.  usage: v3_stats.py log t
import re, sys, math, statistics
rows = [l for l in open(sys.argv[1]) if l.startswith('seed')]; t = float(sys.argv[2])
Z = [float(re.search(r'Z = (\S+)', l).group(1)) for l in rows]
st = [list(map(float, re.search(r'stages: (.*?)\s+tail', l).group(1).split())) for l in rows]
tail = sum(int(re.search(r'tail (\d+)', l).group(1)) for l in rows); bad = sum(int(re.search(r'rebuilt-bad (\d+)', l).group(1)) for l in rows)
cl = [tuple(map(int, re.search(r'clump (\d+)/(\d+)', l).group(1, 2))) for l in rows]
n = len(Z); m = statistics.mean(Z); sd = statistics.stdev(Z); lb = m - t * sd / math.sqrt(n)
print('%s: %d runs, mean 2^%.4f, relative sd %.4f, min 2^%.4f, max 2^%.4f, 99%% bound 2^%.4f' % (sys.argv[1], n, math.log2(m), sd / m, math.log2(min(Z)), math.log2(max(Z)), math.log2(lb)))
print('  stage means', ' '.join('%.3f' % statistics.mean(s[i] for s in st) for i in range(len(st[0]))),
      '| stage sds', ' '.join('%.4f' % statistics.pstdev(s[i] for s in st) for i in range(len(st[0]))))
print('  tail successes %d, failed rebuilds %d, clumping replay %d further successes in %d trials' % (tail, bad, sum(a for a, b in cl), sum(b for a, b in cl)))
```

### B.22 run_v3.sh

```sh
#!/bin/sh
# The runs of PREREG_v3.txt, in order; logs in v3_*.log.
set -e
date -u +%FT%TZ > v3_times.log
seq 21001 21064 | xargs -P 14 -I{} ./smc3 {} 4000 2048 64 64 8 8 4 8192 vs256.bin pre3/s > v3_R1.log 2>&1
date -u +%FT%TZ >> v3_times.log
./varsample a0set256.txt 256 256 20261011 vsP.bin > v3_R2_varsample.log 2>&1
seq 0 255 | xargs -P 14 -I{} sh -c './smc3 $((22000 + {})) 4000 2048 64 64 8 8 4 8192 vsP.bin pop3/p {}' > v3_R2.log 2>&1
date -u +%FT%TZ >> v3_times.log
./varsample a0set8.txt 8 262144 20261012 vs8.bin > v3_R3_varsample.log 2>&1
seq 23001 23120 | xargs -P 14 -I{} ./smc3 {} 4000 2048 64 64 8 8 4 8192 vs8.bin h53/s > v3_R3_smc.log 2>&1
date -u +%FT%TZ >> v3_times.log
BASE=500000 RECOUT=far3_rec.txt MATOUT=far3_mat.txt ./far2 a0set8.txt h53/*.sfs > v3_R3_far.log 2> v3_R3_far.err
python3 -I far_bound2.py far3_rec.txt far3_mat.txt > v3_R3_bound.log 2>&1
date -u +%FT%TZ >> v3_times.log
python3 -I ram_check.py 4000 20261013 pop3/*.sfs > v3_R4.log 2>&1
date -u +%FT%TZ >> v3_times.log
echo done >> v3_times.log
```
