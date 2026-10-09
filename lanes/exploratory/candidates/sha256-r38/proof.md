# Collision attack on 38-step SHA-256 (ePrint 2026/1120, counted, fixed caps): 2^100.07954

**Track** sha256-r38-exploratory, target sha256-r38-prefix-v1, cost model collision-frontier-v5 (C = 2728).
**Claim** time_log2 = 100.07954 (the exact total is 2^100.079536 target compressions, rounded up at the 5th
decimal), success probability at least 0.39 (the bound is 0.3900022), memory 2^95 bytes (an unconditional bound on every charged computation, Section 13), preprocessing
2^78.08755, nonuniform advice 2^13 bytes.

**This package and its sources.**  This package builds on submission b99301f4 (validation PR pending), itself a
corrected version of winglock's public package d2 (submission 3d819a4b, PR #648; its predecessor d1 is submission
20a43626, PR #647).  b99301f4 fixed d2's two refuting findings: the independence premise for the trials of one
group (F1) and a cap test charged only on batches with a W7 pass (F2).  The cryptanalytic work, the transcription
and checks of the characteristic, the Step-3 estimate, the q3 organizer experiment and most of this text are
winglock's and their co-workers' (in Sections 2-6, 10, 11, 13 and Appendix A "we" means the d2 authors), and the
F1/F2 corrections are leech1996's.  This package replaces the first-block evaluator: the 7 x 36-bit SWAR batch
(1,525 + 2 operations per 7 trials) becomes a 256-lane bit-sliced program (49,181 + 2 operations per 256 trials),
with Step 3's stage-3a gate moved into the circuit because 38 steps have no W6 filter.  The group geometry, the
caps and the ledger are recomputed (Sections 4.6, 5, 7, 8), the heuristics and their evidence are restated for the
new first-block family (Section 9), and the first-block organizer experiment, `cert.py`, `selftest.py`, `disp.c`,
`disp_stats.py`, `grouprate.c` and `recount_fb.py` are adapted accordingly.  Everything else - the characteristic,
the Step-1 solution S, L*, Step 3, the Step-3 estimate and its replica (byte-identical output), the Step-2 sets,
the advice allowances and the second organizer experiment - is unchanged.  The bit-sliced evaluator was developed
for our sha256-r37 package (submission ad9745bf, in review).  Section 14 lists every change.

**Credit.** The attack, its 38-step differential characteristic and the semi-free-start (SFS) pair are those of
Yingxin Li, Zhuolong Zhang, Muzhou Li, Fukang Liu, Haifeng Qian and Jinwei Zhu, *Pushing Collision Attacks on
SHA-2 to 39 Steps*, IACR ePrint 2026/1120 (CC BY).  Its two-block, memory-efficient meet-in-the-middle framework is
[LLWS26]: Yingxin Li, Fukang Liu, Gaoli Wang and Jiali Shi, *Pushing the limit of memory-efficient collision attack
framework for SHA-2*, ePrint 2026/1080 (CRYPTO 2026).  The characteristic was found with the SAT/SMT tool of
[LLW24a]: Yingxin Li, Fukang Liu and Gaoli Wang, *New records in collision attacks on SHA-2*, EUROCRYPT 2024.  The
organizer's baseline for this track (time_log2 132, a distribution-free birthday search) defines the reference.
What this package adds is an exact cost account of that attack under collision-frontier-v5: a counted program for
every step, fixed trial and work caps with a success bound, an exact computation of the factors the paper states
(and corrections where its numbers do not reproduce), and a preregistered Monte-Carlo estimate of the Step-3
probability.  We also use the 7 x 36-bit SWAR word packing of tekkac and Th0rgal, the grouped first-block family
of earlier SHA-256 filings (jaazinn and others), the fixed-cap pattern of the r32 filing 6eeefb64, and the
256-lane bit-sliced first-block evaluator of our sha256-r37 package ad9745bf (in review).

## 0. Summary

- **Algorithm (Section 4).** Two-block messages M0 || M1 and M0 || M1' (128 bytes each; FIPS padding appends the
  same third block).  Step 1 is the paper's dense-part solution S (rows 0..13 of both members and W8..W13), read off
  the published SFS pair.  Step 2 searches first blocks M0 until the chaining value CV1 passes the filter
  W7 in F7; this happens with probability exactly p2 = |F7| / 2^32 = 287,309,824 / 2^32 = 2^-3.90197 for a uniform CV1.  Step 3 tries every
  (W14, W15) of the exact freedom set L* (|L*| = 1) and checks every cell of rows 16..37, aborting at the first
  failing row.  A pair that passes every cell collides; it is verified with the target and output.
- **Program (Section 5).** The first block is evaluated 256 trials per batch as bit-planes over 256-bit
  registers (bit L of a register is lane L); a group fixes W0..W14 and the byte gb, and lane l of batch b uses
  W15 = (l << 24) | (b << 8) | gb.  One batch (256 trials: rounds 15..37, the varying schedule words, the Step-2
  W7 test and - 38 steps only, which has no W6 filter - Step 3's stage-3a gate) costs exactly 49,181 operations;
  with the cap test that follows every batch the ledger charges 49,183 operations, 0.07043 units per trial
  (192.12 operations).  The rare path - entered exactly for the lanes that reach stage 3b - and Step 3 run on a
  counted scalar machine.  Every count is produced by the shipped program (Appendix A) and is data-independent.
- **Probability (Section 6).** p = p2 |L*| q3 kappa per first block.  p2 is exact under H1 (Lemma 2).  q3 is the
  average over L* of the probability that a valid first block's pair follows every cell of rows >= 16 and the
  paper's two-bit conditions (which only lowers it).  A sequential Monte-Carlo (SMC) estimator, unbiased for q3
  under H1, was run on 32 preregistered seeds: mean 2^-100.9941, one-sided 99% lower bound 2^-101.0121, so
  q3_model = 2^-101.02 by the preregistered rule.  kappa = 1 (|L*| = 1).
  A standard-library replica of the estimator is the second organizer experiment (Section 10.2): it recomputes row
  16 exactly, runs 20 reduced replicates on organizer seeds with a preregistered pass rule, and rebuilds every success
  as a verified 38-step semi-free-start collision.
- **Caps and success (Section 7).** Each group draws fresh coins, so the groups are independent; inside a group
  no independence is assumed.  A pair bound (H5: Pr[trial j succeeds | trial i succeeds] <= 2^-40 for two trials of
  one group) and the Bonferroni inequality give Pr[a group succeeds] >= q_lb = 2^-80.92198.  N_G = 1,132,227,176,902,152,117,833,655
  groups of 2^16 batches (N = 2^103.90544 trials) with N_G q_lb >= 0.4943, so Pr[success] >= 1 - e^(-0.4943) -
  exp(-2^33.11) - 2^-60 = 0.3900022 under H1, H2 and H5.  All data-dependent work is capped by a global counter V <= V_MAX =
  4,685,325,007,545,158,831,606,997,380,708 operations (halt on overflow); Hoeffding over the independent groups bounds the overflow
  probability by exp(-2^33.11).
- **Ledger (Section 8).** T = A_C + A_S + DEV + (pre + init + online + rare + fin_ops) / C + 6 = 332,195,629,298,691,278,993,927,800,811,111 / 248
  units = 2^100.079536, claimed as 100.07954.  The online term charges 49,183 operations per batch: the counted batch
  (49,181) and the cap test that follows every batch (2).  The Step-1 SAT solve (paper: 2^38.3 compressions) is charged at
  A_S = 2^74, the characteristic search (cost unpublished) at A_C = 2^78, and all our own development at DEV = 2^64:
  deliberately generous allowances, upper bounds by scale (H4, Section 9); the rounded claim is unchanged by them.
- **Heuristics (Section 9).** H1 the chaining value of each single trial behaves as a uniform value
  (score-critical; a statement about one trial at a time), H2 the Step-3 probability and disjointness
  (score-critical), H3 bit-sliced pricing (score-critical, precedent), H4 the advice allowances (supporting), H5 a
  pair bound for two trials of one group (score-critical; 2^64.9 times weaker than independence).  Nothing else: no
  expected-work bound, no independence-of-conditions model, no independence inside a group.
- **Checks.** The selftest (Appendix A) reproduces the published pair's collision under our code and the
  repository verifier, every cell of the characteristic, the corrections, S, L and L*, the exact counts, 65,536
  lanes of the batch evaluator against the verifier (the Step-2 and stage-3a decisions of every lane, the
  recomputed CV of every valid lane), Step 3 recovering the published pair from its chaining value, the
  code of the q3 replica (exact row 16, one replicate, its semi-free-start collisions under the verifier) and the
  ledger.  Two organizer experiments (Section 10) run the shipped program on organizer seeds: the first-block check
  (H1, H3, H5) and the q3 replica (H2; byte-identical output to b99301f4's program).  A within-group dispersion
  measurement (`disp.c`, 2^32 grouped trials) and a recount of the first-block runs from the organizer's seed
  protocol (`recount_fb.py`) support H5.

## 1. Target, cost model and output

- **Target** sha256-r38-prefix-v1: SHA-256 steps 0..37 on every padded block, the standard IV once, FIPS 180-4
  padding, feed-forward, all eight digest words (verifier `digest(m, "sha256", 38)`).  The output is two distinct
  complete messages with equal digests.
- **Cost model** collision-frontier-v5: one target compression (one R-step compression call) = 1 unit; every other
  executed 256-bit word primitive (load, store, add/sub, and/or/xor, shift, compare, branch, uniform random word)
  = 1/C unit, C = 2728.  Immediates and shift amounts are instruction fields.  We use 64 registers.  Memory is
  reported only.  Success must be at least 0.39 over fresh coins.
- **Notation.** F_R(cv, B) is the target compression with feed-forward.  In step i, E_i = A_{i-4} + E_{i-4} +
  S1(E_{i-1}) + IF(E_{i-1}, E_{i-2}, E_{i-3}) + K_i + W_i and A_i = E_i - A_{i-4} + S0(A_{i-1}) + MAJ(A_{i-1},
  A_{i-2}, A_{i-3}) (mod 2^32), with (A_{-1..-4}, E_{-1..-4}) = (a, b, c, d, e, f, g, h) of the incoming chaining value.
  The output is cv + (A_{R-1}, A_{R-2}, A_{R-3}, A_{R-4}, E_{R-1}, E_{R-2}, E_{R-3}, E_{R-4}).

## 2. Sources, the paper's claims, and what we checked

- The paper's attack (its Section 4.2 / 3.1): Step 1 finds W8..W13, A0..A13, E4..E13 with a SAT solver; Step 2
  tries random M0 and checks conditions on W6/W7 (37 steps: "3 and 6 conditions", measured 2^-9; 38 steps: 4
  conditions, 2^-4); Step 3 uses the freedom in (W14, W15) (2^5 / 2^2 values) to satisfy the remaining conditions
  on rows >= 16 (75 / 102).  Totals 2^79.1 / 2^104.3, expected work.
- We transcribed the characteristic tables (37 steps: Table 15, conditions Table 16, pair Table 17; 38 steps:
  Tables 3, 4, 5) twice independently (template OCR of the rendered PDF and a hand transcription; they agree symbol
  for symbol) and verified them against the SFS pair (Section 3).  Section 11 lists every place where our numbers
  differ from the paper's.  We always use the exactly computed value, never the paper's where they differ.
- The earlier filing aa527ec0 (sha256-r32) that reused this paper failed review for (a) expected work instead of a
  worst-case bound and (b) an algorithm that could not be rebuilt from the text.  Here (a) every run's cost is at
  most T by fixed caps (Section 7), and (b) the tables, S, L*, every constant, the procedure and the counted program
  are in this file.

## 3. The characteristic

### 3.1 Notation and member orientation

Symbols are MSB first: `n` = bits (x, y) = (0, 1), `u` = (1, 0), `0`/`1` fixed and equal, `=` equal.  The paper does not
define `+`.  Every `+` sits in a vertical pair E_i[b], E_{i+1}[b], and the SFS pair satisfies E_i[b] = E_{i+1}[b] in
all of them, so we read `+` as that equality (with no member difference).  This reading only adds conditions.
With member x = the message the paper prints first (M), every u/n of the table is reversed on the pair (the
selftest counts the reversed bits); with **x = the message printed second (M')** every cell holds.  We use x = M'.

### 3.2 The table (rows with a non-`=` cell; i, A_i, E_i, W_i)

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

### 3.3 Two-bit conditions as printed (Table 4)

```text
A14[15] = A16[15], A14[23] = A16[23], A14[25] = A16[25], A15[4] = A16[4], A15[7] = A16[7]
A15[16] != A16[16], A15[17] = A16[17], A15[27] = A16[27], A15[29] = A16[29], A16[15] = A17[15]
A16[23] = A17[23], A16[25] = A17[25], A17[9] = A17[20], A17[6] = A17[18], A17[8] = A17[17]
A16[29] = A18[29], A18[29] = A19[29], E16[4] != E16[23], E16[3] != E16[8], E16[14] = E16[28]
E16[4] = E17[4], E16[18] = E17[18], E18[0] != E18[13], E17[15] = E18[15], E17[24] = E18[24]
E19[6] != E19[19], E19[20] = E19[2], E21[2] = E21[16], W7[8] != W7[25], W7[14] != W7[18]
W7[1] = W7[12], W8[0] != W8[28], W8[30] != W8[9], W8[1] = W8[18], W16[1] != W16[12]
W16[20] != W16[27], W16[8] = W16[25], W16[14] = W16[18], W16[4] != W16[6], W16[22] != W16[31]
W23[0] != W23[30], W23[1] != W23[31], W23[14] = W23[21], W23[16] = W23[25], W25[4] = W25[9]
W25[22] = W25[31], W25[20] = W25[27]
```

On the published pair, every printed condition holds on both members except `W25[4] = W25[9]`, which fails on both.  Bit 19 of s1(W25) is W25[4] ^ W25[6] ^ W25[29]; the pair satisfies W25[4] = W25[6], so we read the printed condition as that (a 9/6 misprint; the 37-step analogue is W24[4] != W24[6]).  The algorithm never uses the printed two-bit conditions: it checks the cells.  The SMC of Section 6
adds them (with the corrected readings) as extra conditions, which can only lower its estimate.

### 3.4 The SFS pair (Table 5) and its verification

```text
CV  cd278980 1b12a052 b87cc8a6 a9e059c5 c9c3db85 6ca4b5b5 63d13ac1 c0329f1e
M   48fc271b 9fca20cd cc89f96f fc40396f 8b328cb4 6b91ef78 97f9b767 e2450045
    3b016f58 de9804cb 66a99ea5 0ce30b8d a28cd15a 77a1e994 d28e48a0 9b5f6dbb
M'  48fc271b 9fca20cd cc89f96f fc40396f 8b328cb4 6b91ef78 97f9b767 c2450045
    3f416758 fe9804cb 63a88c0f 0ceb1f8d a28cd15a 77a1e994 d28e48a0 9f1f65bb
hash 5d9ca5f4 59ace3a3 26c9c26c 4252c585 4c0803b7 1b4d5ccd 25c3ccc0 90645c4d
```

F_38(CV, M) = F_38(CV, M') = the printed hash, under our code and under the repository's
`verifier/hash_functions._compress` (selftest).  Every cell of rows -4..37 holds with x = M', y = M.

## 4. The attack

### 4.1 Messages

m = M0 || M1 and m' = M0 || M1', 128 bytes each (two full blocks).  FIPS padding adds the same third block
P = 80 00 .. 00 || 00000000 00000400 to both, so the digests are F(F(F(IV, M0), M1), P) and F(F(F(IV, M0), M1'), P):
if F(CV1, M1) = F(CV1, M1') they are equal.  m != m' because M1 and M1' differ (in W7 (from S), W8..W11 (from S), W15 (from l)).
M1 must be a full data block: in a final padded block W14 and W15 hold the length, which would remove the
(W14, W15) freedom and its differences.

### 4.2 Step 1: the solution S (published values, charged by allowance)

S is the inner part of the published pair: run F_38 from the pair's CV on x = M' and y = M and keep A0..A13,
E4..E13 and W8..W13 of both members.  These values do not depend on the CV.  (Columns: member x, member y.)

```text
A0   b75dae71  b75dae71
A1   da6c35e0  da6c35e0
A2   479b4dc8  479b4dc8
A3   d374b0d8  d374b0d8
A4   df740c96  df740c96
A5   1ee5f173  1ee5f173
A6   7fd9cecb  7fd9cecb
A7   3e016e83  5e016e83
A8   b6a6b5f9  b6e7bde9
A9   3ec0b304  3ec0b304
A10  bcc85d8c  bcc85d8c
A11  25d3cc99  25d3c495
A12  4846f2d8  0c66b4da
A13  c2dc0441  e2dd0441
E4   627cb061  627cb061
E5   1e847683  1e847683
E6   0c1c24b9  0c1c24b9
E7   e2e9b205  02e9b205
E8   99352c79  917934e9
E9   c670b71b  c2e0b710
E10  68c3aa97  6882a297
E11  c2f2c1be  e2f2b1ba
E12  5f9d1216  63be1213
E13  35c13b0d  35c03c77
W8   3f416758  3b016f58
W9   fe9804cb  de9804cb
W10  63a88c0f  66a99ea5
W11  0ceb1f8d  0ce30b8d
W12  a28cd15a  a28cd15a
W13  77a1e994  77a1e994
```

S satisfies every cell of rows 0..13 for both members (selftest).  Its construction is the paper's Step-1 SAT
solve; we charge it as A_S (Section 8, H4).

### 4.3 Step 2: the first block and the filter

For a chaining value CV1 = (A_{-1}, A_{-2}, A_{-3}, A_{-4}, E_{-1}, E_{-2}, E_{-3}, E_{-4}) the paper's Step-2
equations give the second-block words of member x that connect CV1 to S:

```text
E_i = A_i + A_{i-4} - S0(A_{i-1}) - MAJ(A_{i-1}, A_{i-2}, A_{i-3})                (i = 3, 2, 1, 0)
W_i = E_i - A_{i-4} - E_{i-4} - S1(E_{i-1}) - IF(E_{i-1}, E_{i-2}, E_{i-3}) - K_i   (i = 0..7)
```

In particular W7 = c7 - A_{-1} with c7 = 8f6c89c5, and W6 = c6 - A_{-2} + MAJ(A1, A0, A_{-1}) - IF(E5, E4, E3),
E3 = k3 + A_{-1}, with c6 = 75cde31a, k3 = e983b442.  Member y uses the same CV1 and S's y-values; rows <= 5 of S
carry no difference in either characteristic, so W'_i = W_i for i <= 5, W'_6 = W_6 + d6 and W'_7 = W_7 + d7 with
constants d6 = 00000000, d7 = 20000000 fixed by S.  W6 carries no difference in the 38-step characteristic, so the filter is W7 in F7 only (d7 = 20000000).

**Lemma 1 (triangular bijection).**  For fixed S the map CV1 -> (W0, ..., W7) is a bijection of (2^32)^8: W7 depends
only on A_{-1}; W6 is -A_{-2} plus a function of A_{-1}; W5 is -A_{-3} plus a function of (A_{-1}, A_{-2}); W4 is
-A_{-4} plus a function of A_{-1..-3}; W3, W2, W1, W0 are -E_{-1}, -E_{-2}, -E_{-3}, -E_{-4} plus functions of the
earlier coordinates.  With these words and S's W8..W13, F_R's steps 0..13 from CV1 reproduce S exactly (both members).
*Proof.* Substitute the equations; each step is inverted for its new coordinate.  The selftest checks the
reproduction on 65,536 chaining values.

**Lemma 2 (the second-block randomness).**  Let CV1 be uniform and condition on validity (W7 in F7, where
F_k = {w : s0(w + d_k) - s0(w) = t_k mod 2^32} with t7 = 03bff800).  Then (W0..W5) is uniform on
(2^32)^6, (W6, W7) is uniform on F6 x F7 (F6 = all words when d6 = 0), and the three are independent.  For any
l = (W14, W15), the expanded words (W16, ..., W21) are a bijective image of (W0, ..., W5) for fixed (W6, W14, W15)
(W5 = W21 - s1(W19) - W14 - s0(W6), W4 = W20 - s1(W18) - W13 - s0(W5), ..., W0 = W16 - s1(W14) - W9 - s0(W1)),
so they are iid uniform and independent of (W6, W7).  *Proof.* Lemma 1, and the displayed inverse.

**Lemma 3 (the filter is exactly the requirement).**  W6 and W7 enter the expansion only as s0(W6) in W21, W6 in
W22, s0(W7) in W22 and W7 in W23 (W8, W9 are message words).  The characteristic fixes the modular differences of
W21 and W22, and all other terms of those words have differences fixed by S and l, so the cells of rows 21/22 can
hold only if s0(W'_k) - s0(W_k) = t_k, the value on the published pair: validity is necessary for success.
Conversely, for a valid CV1 and l in L* (Section 4.4) every cell of rows -4..15 of A and E holds for both members.
The XOR cells of W6/W7 themselves need not hold: the state rows are fixed by S, and only the modular differences
above reach rows >= 16.  The paper's cell semantics (one-bit plus two-bit conditions on W6, W7) is a sufficient
subset with probability 2^-10 / 2^-4; the exact requirement has

- |F7| = 287,309,824 and |F6| = 4,294,967,296 (exhaustive counts over all 2^32 words, `fcount.c`; sampled again by the
  selftest), hence p2 = |F7| / 2^32 = 287,309,824 / 2^32 = 2^-3.90197 for a uniform CV1.

### 4.4 The freedom set L* (exact)

L is the set of (W14, W15) for which, with S, rows 14 and 15 of A and E follow the cells for both members
(including the `+` pairs with rows 13/14) and the four expansion differences that depend only on (W14, W15),
s1(W'14) - s1(W14), s0(W'14) - s0(W14), s1(W'15) - s1(W15), s0(W'15) - s0(W15), equal those of the published pair.
It is enumerated exactly: E14 over its cell-consistent values (512 candidates), then E15 (2,621,440 candidates);
|L| = 8.  L* keeps the elements of L whose row-16 modular differences dE16 and dA16 (functions of rows 12..15
and the W16 difference only, hence independent of M0) equal the characteristic's; no other element can ever
satisfy row 16.  |L* | = 1 (x-side W14/W15; the published one is element 0):

```text
 0:d28e48a0/9f1f65bb
```

y side (W'14/W'15):

```text
 0:d28e48a0/9b5f6dbb
```

Only the published (W14, W15) survives the row-16 differences; the paper's 2^2 is not reproduced for the published Step-1 solution (Section 11).  Every element also satisfies the W14/W15 cells (asserted).

### 4.5 Step 3 and the success event

For a valid CV1 and each l in L*, the pair (M1, M1') is (W0..W7, S's W8..W13, l) and (W'0..W'7, S's W'8..W'13, l').
**F_l** is the event that every cell of rows 16..37 (A, E, W; values, signed differences, `+` pairs) holds.

**Lemma 4.**  F_l implies F_38(CV1, M1) = F_38(CV1, M1'), hence a collision of m, m'.  *Proof.* Rows
34..37 of A and E have no u/n cell, so F_l gives equal A_i, E_i there, which with the common CV1 are the two
outputs (asserted in the program's setup).

Step 3 tests, in the order of L*: **stage 3a** - E16 = c16_l + k16_l + s0(W1) + W0 against the x-value cells and the
E15/E16 `+` pair of row 16 (10 bits, mask 4c431a80); **stage 3b** - both members' rows 16..37, one row at a time,
every cell of the row, abort at the first failing row.  Stage 3a only tests cells that F_l requires, so the early
abort never discards an element of F_l.  The first l that passes every row is verified with the target (Section 4.6).

### 4.6 The algorithm (fixed caps)

```text
input: N_G (groups), V_MAX (operations); coins: uniform 256-bit words
V = 0
for g = 0 .. N_G - 1:
    draw two random words; W0..W14 of M0 := their 15 low 32-bit fields; gb := the next byte of the second word;
    compute rounds 0..14 and the group constants (Section 5.3)
    for b = 0 .. 2^16 - 1:                                 # one batch: 256 lanes l, W15 = (l << 24) | (b << 8) | gb
        run the counted bit-sliced batch: rounds 15..37, the W7 test and the stage-3a gate on all 256 lanes
        if some lane is valid (passes W7 and stage 3a, i.e. reaches stage 3b):
            rare path (counted into V): lane scan
            for each valid lane: CV1 recomputed from the group state; Step 3 (stages 3a, 3b) over L*
                if some l passes every row: compute both 128-byte messages and their digests with the target
                    (6 compressions); if they are distinct and equal: output (m, m') and halt
        if V > V_MAX: halt (failure)                         # after every batch: compare + branch, 2 operations
halt (failure)
```

Every run executes at most N_G group setups, N_G 2^16 batches with their cap tests, V_MAX + vmax rare-path
operations and one verification, whatever the coins (Section 8).  The cap test is placed after every batch, as in
the driver `attack` of `d1core.py`, and is charged on every batch.  The batch decides stage 3a in circuit:
because Step 3 begins by testing stage 3a for every l and a lane that fails it for every l of L* cannot succeed,
the per-trial success events of Section 7 are unchanged - the counted path simply does not spend scalar work on
W7-pass lanes that Step 3 would reject at its first test (at 38 steps a batch sees about 17 W7 passes but a
stage-3a pass only about once in 60 batches).  There is at most one verification because the first one always
succeeds: a pair that passes stage 3b has equal second-block outputs (Lemma 4), and M1 != M1' because W7 differs by
d7 != 0, so the run outputs and halts.

## 5. The counted program

### 5.1 Machine and pricing

The batch machine holds 64 registers of 256 bits; bit L of a register is the value of lane L (l = 0..255).
Primitives: AND, OR, XOR on registers, LOAD, STORE, compare + branch, RAND, each costing one operation.
NOT is free (every value is a signed literal: each gate output carries its own polarity, folded at compile time);
rotations and shifts are free (they rename bit positions, resolved when the program is compiled); constants are
free (a constant gate folds into the polarity of its consumers, so CONE/CZERO inputs vanish in `emit`).  The batch
derives the 16 batch-counter planes (bit i of the counter broadcast to a plane: 3 operations each, 48 per batch),
tests the fail plane (compare + branch: 2 operations) and runs the batch loop (counter += 1, compare, branch: 3
operations).  The scalar machine of the group setup and the rare path holds one 32-bit word per 256-bit word;
additions are mod 2^256 and masked when needed; a rotation uses the doubled word x | x << 32 (2 operations), so
S0, S1, s0, s1 cost 8 each.

### 5.2 The batch: 49,181 operations per 256 trials

The circuit is compiled once per target (`build(R)`, `emit` in `d1core.py`): a Boolean network of signed-literal
gates (xor/and/or with common-subexpression elimination) evaluating, on planes, the state rounds 15..37, the
schedule words that depend on W15 (W17, W19, W21, ..., W37), the Step-2 W7 test (the fail bit of a lane is
z != 0 where z = s0(W7 + d7) XOR s0(W7) XOR t7, evaluated as a masked equality) and - 38 steps only, which has no
W6 filter - Step 3's stage-3a gate: e16 = ck16 + s0(W1) + W0, the masked equality (e16 AND m16) == v16
OR-accumulated into the fail plane, so bit L of the fail word is clear exactly for the lanes that reach stage 3b.
(For 37 steps the second Step-2 test, W6, takes the place of the stage-3a gate.)  Additions are evaluated per bit
position; X AND NOT Y shares the XOR the adder already computes.  The network is scheduled by next-use distance
onto 64 registers (register 63 is the batch counter); spilled values are stored to memory and loaded back, every
load and store counted.  Count (from `d1core.calibrate`, identical over three groups): **c_B = 49,181** = 8,342
loads + 2,850 stores + 30,106 xor + 4,989 and + 2,841 or + 48 counter planes + 2 fail test + 3 loop; the deepest
spill point uses register 63 (`cal['maxreg']`).  The driver then tests the work cap after every batch (compare V
with V_MAX, branch: 2 operations, not part of `calibrate`'s c_B); the ledger charges c_B + 2 = **49,183**
operations per batch.  Per trial 49,183 / (256 C) = 0.07043 units = 2^-3.82781.

### 5.3 Group setup and start-up

Per group (counted on the scalar machine): two RAND, 15 words unpacked (shift + mask each), gb extracted (2),
rounds 0..14 and W16, W18, W20, ... (the parts of the schedule independent of W15), the 29 group constants, each
masked, stored for scalar reuse in the rare path and broadcast to 32 planes (shift + and + subtract + store per plane), the 8 gb planes, the 274 hoisted
shared subexpressions of the circuit (2 loads + gate + store each, once per group), and the stores of M0, gb and
the A11..A14 / E11..E14 state that the rare path needs: **c_G = 5,691**, plus 4 for the group loop (zero the batch
counter; add, compare and branch on the group counter).  Start-up: 9 program constants stored, plus an allowance
of 256 operations for loading the circuit's constant planes.

### 5.4 Rare path and Step 3 (counted on the scalar machine)

On a batch with a valid lane the rare path runs the lane scan (4 operations to extract the first set bit of the
fail word's complement, repeated per valid lane at 45), then recomputes the lane's CV1 from the stored group state
and precomputed group-constant words (`lane_cv`, rounds 15..37 on the scalar machine plus feed-forward: c_cv = 1021), then Step 3 over L*.  Per lane:
c01 = 71 (E0, W0, E1, W1 and q = s0(W1) + W0), per l in L* c3a = 8 (stage 3a; it passes, since only lanes that
reached stage 3b enter the rare path), once per lane at the first stage-3a pass crest = 85 (E2, E3, W2..W7 and the
y words), and per stage-3b entry at most c3b = 2383 (a full pass of rows 16..37 for both members with every cell
check, reusing e16 and pre-folded per-element constants; an early abort costs less), plus FLAG3B + V3B = 2 + 149 (test of the live registers, spill and reload of
the 64 batch registers, and the stores of W0..W7, W'6, W'7 the later stages need).  Each batch with a valid lane
also spends VCTRL = 3 operations adding its rare-path count to V (counted into V; it includes a second,
conservative charge of the cap test, which Section 8 charges on every batch).  All are measured by the program on
the published pair's chaining value (which passes every row) and are data-independent except for the early abort;
every one of them is counted into V.

### 5.5 Correctness of the counted program

- **Bit-exactness.**  The selftest runs 256 batches (65,536 lanes) against the repository verifier: every lane's
  W7 decision and - 38 steps - stage-3a decision equals the fail bit, the recomputed CV1 of every valid lane and
  of the first 8 lanes of each batch equals the verifier's compression, and Lemma 1's reproduction of S on rows
  0..13 holds for every lane.  0 mismatches.  `calibrate` additionally asserts the counted `run_vm` program's fail
  plane equals the fast evaluator's on every group, and a development run over 360 batches flagged exactly the
  stage-3b-reaching lanes (0 mismatches, 24,576 lanes).  The organizer experiment repeats the lane check on its
  own seeds.
- **Gate soundness.**  Signed literals: NOT is folded into each gate's output polarity; common subexpressions
  are shared by structural key; constant inputs fold at compile time.  `emit` is a scheduling pass over the same
  gate list (no semantic change).  The plane value of bit L is exactly the lane-L value the scalar machine would
  compute, so a scalar lane check (previous bullet) verifies every lane.
- **Registers.**  `emit` schedules onto 64 registers with spills charged; the largest operand index the counted
  program uses is 63 (`cal['maxreg']`).
- **Step 3 end to end.**  From the published pair's CV, the counted Step 3 derives W0..W7, finds the published
  (W14, W15) in L*, passes every row and returns exactly (M', M) (selftest).

## 6. The Step-3 probability (H2)

### 6.1 The quantity

For a valid CV1 (Lemma 2) and l in L*, let X'_l be the printed two-bit conditions on rows >= 16 (Section 3.3, with
the corrected reading W25[4] = W25[6]; the comment of `smc.py`, shared by both tracks, says "two corrected readings": one
per track).  Define q3 = (1/|L*|) sum_l Pr[F_l and X'_l | valid].  Then q3 <= (1/|L*|) sum_l
Pr[F_l | valid], and the expected number of l in L* that succeed is at least |L*| q3.  Under H1 q3 is a fixed number
determined by S, L* and the tables (Lemma 2 gives the full distribution of the second-block words).

### 6.2 The estimator (`smc.py`)

- Row 16 is computed **exactly**: for each l, E16 = c_l + W16 is uniform (W16 is fresh), so all 2^22 values of E16
  with its 10 fixed bits are enumerated and row 16 (all cells and X') is checked.  Valid E16 values per l: 0: 32;
  total 32, i.e. a stage factor of exactly 2^-27.0000.
- The fresh rows (rows 17..22) are sampled: E_i^x is drawn uniformly with its x-value cells, its `+` pairs
  and the E-to-E two-bit conditions imposed (an exact importance weight 2^-f), W_i^x = E_i^x - (the rest of step i),
  W_i^y = W_i^x + its exact difference (the s1/s0 differences of the previous words and the fixed differences), and
  the whole row is checked.  Lemma 2 makes these words iid uniform, so the proposal is exact.
- The tail (row 22 is fresh because W6 is uniform and unconstrained): propose W23 with its x-value cells and the W23 two-bit conditions imposed (f bits) and set W7 = W23 - s1(W21) - W16 - s0(W8); weight 1{W7 in F7} 2^(32-f) / |F7|; rows 23..37 are then deterministic.
- NP particles, M children per particle per stage, multinomial resampling of the survivors after every stage but
  the tail; the estimate is the product of the stage means, which is unbiased for q3: given the particles before a
  stage, the stage mean is an unbiased estimate of the particle average of that stage's conditional probability, and
  multinomial resampling keeps particle averages unbiased, so the expected product telescopes to q3 (the standard
  unbiasedness of the SMC normalising-constant estimator; Del Moral, *Feynman-Kac Formulae*, Springer 2004).
  The clumping replay (r37) rebuilds W0..W7 of every successful tail sample (inverse map of Lemma 2) and counts
  the elements of L* whose pair follows every cell for the same first block.

### 6.3 Preregistration and results

The rule (`smc_summary.py`): from the 32 per-seed estimates Z_s (linear scale), LB = mean - t sd / sqrt(32) with the
one-sided 99% Student quantile t = 2.4529 (31 degrees of freedom); q3_model = 2^(floor(100 log2 LB) / 100).  The
program hashes, parameters (NP = 4000, M = 2048, MT = 8192), seeds and rule were frozen before any listed seed was
run (`PREREG_v2.txt`, Section 12).  A first freeze (v1) was aborted after 8 seeds because 8 parallel processes used
31 GB of memory; v2 changed only memory handling and used new seeds; the 8 complete v1 values are reported in
Section 12 and agree with v2.

| quantity | value |
|---|---|
| per-seed log2 estimates (32) | -101.043 -101.075 -100.982 -101.043 -100.967 -100.980 -101.044 -100.921 -100.984 -101.002 -101.004 -101.033 -100.962 -101.006 -100.995 -100.986 -101.050 -100.910 -101.010 -100.996 -100.991 -101.032 -100.923 -100.950 -100.955 -101.044 -101.017 -100.988 -100.985 -101.027 -100.997 -100.928 |
| mean of Z_s | 2^-100.9941 |
| relative standard deviation of Z_s | 0.0285 |
| min / max | 2^-101.0745 / 2^-100.9098 |
| 99% lower bound LB | 2^-101.0121 |
| **q3_model** | **2^-101.02** |
| stage means (log2) | 16: -27.000, 17: -16.997, 18: -13.000, 19: -15.002, 20: -6.000, 21: -7.000, 22: -1.000, tail: -14.995 |
| tail hits (all seeds) | 2,199,373 |
| clumping replay | not run (|L*| = 1) |

### 6.4 Consistency with independent counts and measurements

- The stage factors are integers within 0.01: rows fresh in one word behave like independent bit conditions.
  Their sum, 2^-100.99, compares with the paper's 102 conditions and our count of 62 + 41 = 103 one-bit plus
  two-bit conditions on rows >= 16 (Section 11).  The SMC is about 2 bits above the condition count: the A16 two-bit conditions are strongly dependent (A16 = E16 + a constant for the single l), and the exact row-16 enumeration gives 2^-27.000 for the 29 conditions of row 16 that the count prices at 2^-29.
- The extraction harness (`hsm.c`, Section 12) measured row 16 directly on 2^35 uniform chaining values:
  all 29 row-16 conditions together pass at 2^-26.913 (CI [-27.59, -26.23]), against the exact 2^-27.000 of the enumeration.
- The early Step-3 conditions on real first blocks (2^30 random M0 through real 38-step compressions) pass at
  rate 1/2 each within noise (Section 12, `meas_step3_r38_M0_2e30.json`).
- **A second implementation.**  The q3 replica in `d1core.py` (standard library only, written for this fix; the
  organizer experiment of Section 10.2) uses the same proposals and checks as `smc.py` but its own code.  Row 16:
  it enumerates the 2^19 words that satisfy the proposal's constraints (x-value cells and the three E16-to-E16
  conditions; every word passing row 16 satisfies them) and finds the same 32 words as `smc.py`'s 2^22 enumeration.
  Rows 17..37: 256 development replicates (NP = 64) gave a mean of 2^-100.9621; 1,020 validation replicates
  (design frozen first, own seeds, Section 10.2) gave 2^-101.0186 with a standard error of 0.0146 bit, 1.5 standard
  errors from the preregistered mean.  The validation sample's own one-sided 99% bound is 2^-101.0529; pooled with
  the preregistered sample by inverse-variance weights the mean is 2^-100.9991 and the 99% bound 2^-101.0143, so
  q3_model = 2^-101.02 stands (Section 8 lists q3 = 2^-101.06 as a sensitivity).  All 69,190 tail successes of the
  validation and 18,053 of development were rebuilt as 38-step semi-free-start collisions (CV1 by inverting
  steps 7..0 from S, then the reference compression of both blocks): none failed.

### 6.5 Disjointness across L*

|L*| = 1, so the success event of a valid first block is F_l for the single l; kappa = 1.

## 7. Success probability and caps

Only three facts are used: one trial at a time (H1, H2), the exact independence of distinct groups, and a pair
bound inside a group (H5).

- **Events.**  For a trial i (one first block), A_i is the event that its chaining value is valid and the pair of
  the element of L* follows every cell of rows 16..37 (F_l).  The algorithm finds every A_i among the trials it
  tests: the batch's stage-3a gate is exactly Step 3's first test, so it never discards an element of F_l; stage
  3b checks exactly F_l, and F_l implies a collision (Lemma 4).
- **One trial (H1, H2).**  Pr[A_i] >= p_model = p2 |L*| q3_model kappa = 2^-104.92197 (p2 = 2^-3.90197, |L*| = 1,
  q3_model = 2^-101.02, kappa = 1).  This uses the distribution of one trial's chaining value only.
- **Groups are independent (exact).**  Each group draws its own two uniform 256-bit words.  Its trials, their
  outcomes and its rare-path work are functions of those words, so the N_G groups are independent and identically
  distributed.  Inside a group nothing is independent: its 16,777,216 trials are deterministic functions of 488 bits.
- **One group (H5, Bonferroni).**  With m = 256 2^16 = 2^24 = 16,777,216 trials per group,
  q_g = Pr[some A_i of the group] >= sum_i Pr[A_i] - sum_{i<j} Pr[A_i and A_j].  H5 bounds Pr[A_j | A_i] <= 2^-40
  for i != j in one group, so sum_{i<j} Pr[A_i and A_j] <= (m - 1) 2^-41 sum_i Pr[A_i], and
  q_g >= (1 - (m - 1) 2^-41) m p_model = q_lb = 2^-80.92198 ((m - 1) 2^-41 = 2^-17.00 = 0.0000076).
- **Trial cap.**  N_G = ceil(0.4943 / q_lb) = 1,132,227,176,902,152,117,833,655, N_B = 2^16 N_G = 74,201,640,265,459,441,194,346,414,080 batches,
  N = 256 N_B = 2^103.90544 trials (N p_model = 0.4943037712).  Pr[no group succeeds] = (1 - q_g)^N_G <= exp(-N_G q_lb)
  <= exp(-0.4943) = 0.6099978.
- **Work cap.**  The rare-path operations of a batch, v_b, are at most vmax = 963,847 (vmax = SCANB + VCTRL +
  256 (SCANL + VLANE + c_cv + c01 + crest + c3a + c3b + FLAG3B + V3B) = 7 + 256 3,765).  Their expectation is at
  most vbar = 63.0815, computed from one lane at a time: vbar = P_hit (SCANB + VCTRL) + 256 p2 |L*| p3a lane,
  where P_hit <= 256 p2 |L*| p3a = 0.0167 by the union bound (no joint distribution of the 256 lanes is needed),
  lane = SCANL + VLANE + c_cv + c01 + |L*| (c3a + c3b + FLAG3B + V3B) + crest = 3,765, and a lane reaches stage 3b
  with probability p2 p3a = p2 |L*| 2^-10 because it must pass W7 and then stage 3a, and E16 is uniform given a
  valid CV1 (H1, Lemma 2); the stage-3b cost is bounded by its full pass.  V_MAX = ceil((1 + 2^-10) N_B vbar) =
  4,685,325,007,545,158,831,606,997,380,708.  The rare-path work of a group lies in [0, 2^16 vmax] and the groups
  are independent, so Hoeffding over the N_G groups gives Pr[sum v_b > V_MAX] <= exp(-2 (2^-10 N_B vbar)^2 /
  (N_G (2^16 vmax)^2)) = exp(-2^33.11).
- **Success.**  If the full run would not exceed V_MAX, all N trials are tested.  Hence Pr[output a collision] >=
  1 - exp(-0.4943) - exp(-2^33.11) - 2^-60 = 0.3900022 > 0.39 under H1, H2 and H5 (the 2^-60 is kept as slack).
  Any output is a verified collision (Section 4.6), independently of the heuristics.

## 8. Ledger (exact; `cert.py`)

```text
T = A_C + A_S + DEV + (pre + init + online + rare + fin_ops) / C + fin_units
  A_C = 2^78 (characteristic search), A_S = 2^74 (Step-1 solve), DEV = 2^64 (all development)        [units]
  pre    = (E14 + E15 candidates) x 1024 + 2^20 = 2,685,927,424              (L, L* enumeration and tables)
  init   = c_init + 256 = 265
  online = N_G (c_G + 4) + N_B (c_B + 2) = 3,649,465,721,209,864,154,017,850,746,361,865
  rare   = V_MAX + vmax = 4,685,325,007,545,158,831,606,998,344,555
  fin    = 6 units + 512 operations (two complete messages, their digests, once)
T = 332,195,629,298,691,278,993,927,800,811,111 / 248 units = 2^100.079536  ->  time_log2 = 100.07954 (rounded up at the 5th decimal)
preprocessing = A_C + A_S + DEV + pre / C = 2^78.08755
```

The online term is 2^100.0777 units, the rare term 2^90.4723, the three allowances together 2^78.09; everything
else is below 2^21.  The cap test that follows every batch is in the online term (c_B + 2).  The total holds on
every run: the program cannot execute more groups, batches, cap tests, rare-path operations or verifications.

**Sensitivity** (`cert.ledger` with one input changed, or the same formulas with H5's bound changed; the exact log2 T
to 7 decimals, which a claim rounds up at the 5th decimal):

| change | log2 T |
|---|---|
| q3 lower by 0.25 bit | 100.3295358 |
| q3 lower by 0.50 bit | 100.5795357 |
| q3 lower by 1.00 bit | 101.0795356 |
| q3 = 2^-101.06 (the replica validation's 99% bound, rounded down) | 100.1195358 |
| q3 = 2^-101.40 (the pooled threshold of the organizer replica) | 100.4595357 |
| q3 = 2^-102 (the paper's condition count) | 101.0595356 |
| earlier allowances (A_C = 2^56, A_S = 2^50, DEV = 2^40) | 100.0795355 |
| A_C = 2^79 | 100.0795361 |
| H5 with 2^-38 instead of 2^-40 | 100.0795688 |
| H5 with 2^-36 instead of 2^-40 | 100.0797009 |
| no packed pricing (each first block = 1 unit) | about 103.91 |

## 9. Heuristics

**H1 - the chaining value of one trial (score-critical).**  For every single trial of the attack (lane value
W15 = (l << 24) | (b << 8) | gb fixed, W0..W14 and gb from the group's two uniform random words), the chaining
value CV1 = F_38(IV, M0)
behaves as a uniform 256-bit value as far as Steps 2 and 3 are concerned: the trial is valid with probability p2,
and given validity the second-block words have the distribution of Lemma 2.  It is a statement about one trial at a
time (a 256-bit value computed from 488 uniform bits); it says nothing about two trials of one group, which H5
covers.  Used for: p2, the distribution of the second-block words (Lemma 2, hence q3), and the per-lane
expectations of the work cap.  Evidence: (i) local, the
attack's own grouped family (`grouprate.c`, 2^31 = 2,147,483,648 trials, every one a full 38-step compression):
W7 passes 143,644,003 (expected 143,654,912, z = -0.94; rate 2^-3.9032 against the exact 2^-3.90197); valid lanes
(W7 pass and stage-3a pass) 140,524 (expected 140,288.0, z = +0.63); batches with >= 1 valid lane 139,356 (expected
139,125.7, z = +0.62); batches with >= 2 valid lanes 1,162 (expected 1,155.6, z = +0.19); (ii) the extraction harness's 2^30 random first blocks and 2^35..2^36 uniform CVs (cell semantics, Section 12);
(iii) the organizer experiment (Section 10.1).  No run selection: the first-block experiment's design and prediction
are fixed in this file; on 256 seeds of our own it returned 18 pairs and on the organizer's public-seed request
(Section 10.1) 23, both inside the expected range.  Limitations: a premise, not a theorem; tested on about 2^31 trials, not on 2^103.9; W15 is the only
varying word (22..23 rounds follow it).  (The text of this paragraph from "Evidence" on follows d2's, adapted to
the bit-sliced family; d2 stated H1 for all trials jointly, which this package does not use.)

**H2 - Step-3 probability and disjointness (score-critical).**  (a) q3 >= q3_model = 2^-101.02; (b) kappa = 1 (|L*| = 1; nothing to assume).
(c) No run selection: every run of the preregistered estimator and of the replica is reported (Section 12).
Evidence: Section 6 (unbiased estimator under H1, preregistered 32-seed sample with a one-sided 99% bound, exact row
16, integer stage factors, agreement with independent counts and measurements; the replay) and a second,
standard-library implementation that the organizer runs on its own seeds with a preregistered pass rule (Section
10.2; validated on 1,020 replicates of our own; every success it finds is a verified semi-free-start collision).
The organizer run can confirm q3 only to within its pooled threshold 2^-101.40; the step from there to q3_model rests
on our preregistered sample (sensitivity: q3 = 2^-101.40 gives log2 T = 100.45954).  Limitations: a
Monte-Carlo bound (heavy tails would make the sample mean low rather than high, which errs on the conservative
side, but this is not proven); depends on H1; the `+` reading.

**H3 - bit-sliced pricing (score-critical; precedent).**  A word-RAM program that evaluates 256 first blocks as
bit-planes over 256-bit registers is charged by its counted primitives (49,181 per batch of 256 trials, plus the
2-operation cap test per batch in the ledger: 49,183/256 = 192.12 operations per trial).  Precedent: the same
bit-sliced accounting is used in our sha256-r37 submission ad9745bf (in review), and packed-word pricing was
rated plausible in sha256-r31 (H7) and blake3-r2 filings.  Without it each first block costs one unit: about 103.91.

**H4 - advice allowances (supporting).**  The published characteristic and the SFS pair's inner values S are used as
advice; their construction is charged at A_S = 2^74 (the paper reports 2^38.3 compression-equivalents for
Step 1, so the allowance is 2^35 times larger) and A_C = 2^78 (the characteristic search; cost not published).
Organizer-executed experiments `d1-first-block-r38` and `d1-q3-smc-r38` directly load, validate, and replay the entire 8 KiB advice package (`CH[38]`, `PAIRS[38]`, `LSTAR[38]`, and derived `S`, `k3`, `c6`, `c7`, `s3c`, and row masks) on every run: `setup(38)` asserts every cell of the published SFS pair on rows -4..37, verifies `L*` against the row-14..16 conditions, checks that every valid first-block lane's Step-2 reconstruction reproduces `S` on rows 0..13 (`d1-first-block-r38`), and rebuilds 1,445 verified 38-step semi-free-start collisions from `S` and `L*` under the repository verifier (`d1-q3-smc-r38`).
Both searches were run by the paper's authors with the open-source SAT/SMT tool [LLW24a] and published together with the SFS
pair, so they are computations an academic group completed.  At 2^21.7 units per CPU-second (a core retiring about
10^10 primitive operations per second at C of about 2,700), 2^78 units is about 3 x 10^9 CPU-years (2^29 times the published Dobraunig-Eichlseder-Mendel-Schlaffer 35-step wall-clock search of < 2^49 compressions), and DEV = 2^64
covers about 2^42 CPU-seconds against about 5,400 CPU-seconds of recorded development (Section 12).  So A_C
is an upper bound by scale, not a measurement: 2^78 units is about 3 x 10^9 CPU-years at 2^21.7 units per CPU-second, about 140 times the output of a 10^7-core machine (the scale of the largest supercomputers) running for two years; it bounds any search an academic group completed
and published.  The rounded claim 100.07954 is unchanged for A_C up to 2^79 (A_C = 2^79 gives 100.0795361); with the earlier values (2^56, 2^50, 2^40) log2 T is 100.0795355.

**H5 - pairs inside a group (score-critical).**  For two distinct trials i != j of one group (the same W0..W14,
different W15), Pr[A_j | A_i] <= 2^-40.  Under the independent-uniform model the left side is p_model = 2^-104.9, so
H5 allows a dependence 2^64.9 times stronger than that model; it constrains pairs only and is compatible with the
group's 488 bits of randomness.  Used for: the group success bound (Section 7) through the Bonferroni inequality.
Evidence: (i) structure: two trials of a group share rounds 0..14 and differ in W15, which enters step 15 and the
schedule words W17, W22, W30 and W31; 23 rounds then separate their chaining values, and A_j would have to follow
from A_i with probability 2^-40 although each needs about 105 bits of conditions on its own chaining value;
(ii) measured inside groups (`disp.c`, `disp_stats.py`, Appendix A; 2,048 groups with fresh W0..W14 and 256 x 2^13
lane values each, 2^32 full 38-step trials): the per-group counts of valid trials, and of valid trials that reach
stage 3b (W7 pass and the stage-3a e16 condition, rate 2^-13.9), have binomial dispersion, so the average
Pr[A_j | A_i]
inside a group equals the unconditional rate to within a factor 1.000001 (Step 2) and 1.0006 (the 2^-13.9 event),
three standard errors included:

```text
a (W7 valid): groups 2048, trials/group 2097152, total 287341177 (expected 287309824.0, z +1.91); dispersion 1.0057 (z +0.18); avg Pr[j|i] = 6.689453e-02 vs rate 6.689453e-02 (ratio 1.000000, +3se ratio 1.000001)
b (reaches stage 3b): groups 2048, trials/group 2097152, total 280540 (expected 280576.0, z -0.07); dispersion 0.9807 (z -0.62); avg Pr[j|i] = 6.531747e-05 vs rate 6.532669e-05 (ratio 0.999859, +3se ratio 1.000543)
batches with >= 2 stage-3b lanes: 2356 (expected 2311.3, z +0.93)
```

(event b is the event the rare path actually runs - W7 pass and the stage-3a e16 condition - measured directly,
where b99301f4 measured a fixed-bit proxy at the same rate); (iii) organizer-executed: the first-block
experiment (Section 10.1) runs one group per organizer seed and returns a pair iff the group has a valid
trial.  In the public-seed emulation of this package's experiment 23 of 256 groups returned a pair, against
24.5 expected if the 1,536 trials of a group were independent; positive dependence inside groups would lower this
count.  `recount_fb.py` (Appendix A) recomputes the statistic from the organizer's seeds with the repository's
compression and seed protocol only, without the participant program: 23 groups with a valid trial, 25 valid
trials of 393,216 (24.5 expected), and the recorded pair of every one of the 256 trials is exactly the first
valid trial of its group.  Sensitivity:
with 2^-38 instead of 2^-40 log2 T is 100.0795688; with 2^-36, 100.0797009; the bound fails only beyond about
2^-23 (the groups hold 2^24 trials, so the correction term stays negligible far longer than in b99301f4).
Limitations: a premise; the measured events are about 2^-4 and 2^-14, not 2^-105.

Not used: expected work, an independence-of-conditions model (replaced by the SMC), a random-oracle model, any
premise on the published pair beyond its verified values, any independence of the trials of one group.

## 10. Organizer experiments

`experiments/d1core.py` is byte-identical to Appendix A's `d1core.py` (SHA-256 given in A.2).  Both experiments
run it; it dispatches on the request's experiment id.

### 10.1 d1-first-block-r38 (H1, H3, H4, H5)

Per organizer seed it runs `setup(38)` (verifying the advice `CH[38]`, `PAIRS[38]`, `LSTAR[38]`, and `S`) and one group of the attack driver (`attack`, the same code) with W0..W14 and gb from
SHAKE-256(seed), 6 batches = 1,536 trials.  A hook checks 24 seed-chosen lanes of every batch and every lane the
fail plane marks valid against the scalar compression (all 8 CV1 words, the W7 decision, the stage-3a decision),
that the valid lanes are exactly those the driver sends to Step 3 (with the recomputed CV1 equal), and that for every
valid lane and every l in L* the pair follows every A/E cell of rows -4..15 and every W cell except W6/W7's XOR
cells (Lemma 3).  It returns the 128-byte pair (M0 || M1, M0 || M1') of the first valid lane with the published l if
every check passed, else two nulls.  Event: full collision (none is expected; Pr < 2^-60).

Prediction under the independent-uniform model (it only states the expected count; H1 and H5 do not imply it): a
trial returns a pair with probability 1 - (1 - p2 |L*| 2^-10)^1536 = 0.0957, so about 24.5 of 256 are expected; the count is a witness observation, not a statistical test; mismatches 0 in every trial (observations).
A local run on our own 256 seeds returned 18 pairs, 0 mismatches, 21 valid lanes of 393,216 trials (25.7 valid
lanes expected).  A local emulation of the organizer's public-seed request (seed protocol of
`experiments/runner.py`, seed `hashsmash-public-seed-v1`, no holdout nonce; `run_exp_org.py`) returned 23 pairs,
0 mismatches, 25 valid lanes, 2,411 W7 passes, 35,281 lanes checked, byte-identical on two runs, 5.9 s
(run time limit 20 s).  A holdout nonce changes the seeds and the count.

### 10.2 d1-q3-smc-r38 (H2, H4)

The organizer runs the replica of Section 6.4 (`q3_experiment` in `d1core.py`) on its own seeds.  Row 16 is
enumerated exactly (2^19 words) in every run.  Trials 0..19 each run one replicate of the estimator of Section 6.2
(NP = 64 particles, 128 children per particle at row 17, 4 at rows 18 and 19, 1 at rows 20..22, 512 tail proposals
per particle; randomness from SHAKE-256 of the trial's seed).  Every tail success is rebuilt: W0..W7 by the inverse
expansion (Lemma 2), CV1 by inverting steps 7..0 from S, and the pair is accepted only if F_38(CV1, M1) =
F_38(CV1, M1') under the reference compression, M1 != M1', the paper's Step-2 equations map CV1 back to W0..W7,
W7 is in F7 and every cell of rows -4..37 holds except W7's XOR cell.  Trial t < 20 returns its first rebuilt
pair as the 96-byte strings CV1 || M1 and CV1 || M1' iff it has a tail success and every success was accepted.
Trial 20 returns a pair iff all 20 trials did and the mean of their 20 estimates is at least 2^-101.40.  Trials
21..255 return no pair by design.  The organizer's target digest of these strings is not expected to collide (they
are semi-free-start collisions from CV1, not collisions from the IV), so the checked event has 0 successes; the
organizer-visible statistic is the number of returned pairs, predicted 21, and anyone can verify the semi-free-start
collisions in the raw report.

The design was frozen (`PREREG_q3x.txt`, program ba1dd804) before any validation run and before the public-seed
request was computed.  The threshold came from development replicates: a bootstrap of the mean of 20 put its
0.0001 quantile at 2^-101.37 after shifting to the preregistered mean.  Validation (`run_q3x_val.py`, 51 requests of
256 trials on our own seeds, 1,020 replicates): every request returned exactly 21 pairs; the 51 pooled means lay in
[2^-101.315, 2^-100.757]; 69,190 tail successes, all accepted.  The public-seed emulation (`run_exp_org.py`) returned
21 pairs, pooled mean 2^-100.843, 1,445 tail successes all accepted, the 21 returned strings are semi-free-start
collisions under the repository's `_compress` as well, byte-identical on two runs, 3.4 s (run time limit 20 s).
This package's `d1core.py` differs from the frozen program only outside `q3_experiment`: the replica's output on
the public-seed request is byte-identical to b99301f4's program's (3.5 s), so every number of this section
carries over.

What this tests: an organizer-executed, unbiased estimate of q3 under the exact distribution of Lemma 2, with a
pass rule that a true q3 of 2^-101.40 would fail about half the time, of 2^-101.55 more than 93% of the time and of
2^-101.7 more than 99.8% of the time (bootstrap of the validation replicates, rescaled); and that the success event
the estimator counts produces genuine semi-free-start collisions.  What it does not test:
H1 itself (it samples the second-block words from Lemma 2's distribution), and q3 more finely than its threshold.

## 11. Differences from the paper

1. Member orientation: the tables hold with x = M' (Section 3.1).  `+` is undefined; read as E_i[b] = E_{i+1}[b].
2. Step 2: 4 conditions and 2^-4, as in the paper, for the cell semantics; the exact requirement (Lemma 3) gives 2^-3.9020, which we use.
3. Table 4: `W25[4] = W25[9]` fails on the pair; it should read W25[4] = W25[6] (count unchanged).
4. (W14, W15) freedom: the paper says 2^2; for the published Step-1 solution exactly one value survives (|L| = 8, |L*| = 1).  This costs 2 bits against the paper's arithmetic; its attack may use another Step-1 solution.
5. Condition counts on rows >= 16: ours 62 + 41 = 103 (one-bit + listed two-bit), paper 102.  We do not use counts:
   the SMC gives 2^-100.99.
6. The paper's totals are expected work with independence-of-conditions; ours is a worst-case bound with caps.

## 12. Runs and hashes

All runs on one Apple-silicon Mac; CPU = user seconds.  Heavy runs held the shared lock and ran under `nice -n 10`.

| run | what | CPU | hashes / outputs |
|---|---|---:|---|
| extraction (other worker, 2026-10-08) | table OCR, `verify_sfs.py`, `hsm37/38 S`, `enum_S_py.py`, `validate.py`, `step2_equiv.py` (light) | about 70 | EXTRACT.md Section 11; summary.json ed648926 |
| extraction heavy (lock) | `hsm37 step3 30` (2^30 random M0), `hsm38 step3 30`, `hsm37 step3 36 direct` (2^36 CVs), `hsm38 step3 35 direct` | 2,121 | outputs 9ae6a612, 0dde492c, 79376572, 84bf58e1 (meas_step3_*.json) |
| design (other worker) | `p2exact.py` (exhaustive F counts, numpy, 72 s, no lock: disclosed), `enumL.py`, `lstar.py`, `fwdsim.py`, `smc.py`/`smc2.py`/`smc3.py` (earlier SMC versions), `clump.py`, `a0family.py`, `proto_v1.py`, `proj.py` | about 350 | DESIGN.md Section 13 (p2exact fce3f4d1, smc3 4bc9f2fe, clump 1fa7ea3a) |
| this build: program development | `d1core.py` lane tests (2 x 21,000 lanes, 0 mismatches), calibration, mask search, Step-3 end-to-end, L enumeration | about 60 | dev/t_batch.py |
| this build: `fcount.c` | exhaustive |F7|, |F6| (3 sets, 2^32 each) | 7 | runs/fcount.out 539a4288 |
| this build: SMC development | seeds 101, 102, 103r, 9, 77, 78r and small tests (not in the sample) | about 150 | - |
| this build: SMC v1 (lock; aborted) | frozen 20:22:03Z (PREREG.txt 9a2c39ef); 16 started, 8 complete: r37 seeds 1001..1008 = -73.954, -73.971, -74.033, -74.016, -74.040, -74.041, -73.982, -74.064 (replay 103,412 samples, all exactly 1 l); stopped at 31 GB RSS | about 470 | v1_aborted/LOG.txt bcf772c3, smc_v1.py b932a271 |
| this build: SMC v2 (lock) | frozen 20:25:28Z (PREREG_v2.txt 7613bbfe); 32 + 32 seeds, every one used | 1,401 | LOG.txt 7394640a; summary_r37 6acea59a, summary_r38 df211d69 |
| this build: `grouprate.c` (lock) | H1 evidence, 2^29.81 grouped trials per track | 175 | grouprate.log 04609f26; r37 fb2e15fb, r38 037a1b11 |
| this build: selftest, cert, collection, local experiment | selftest r37/r38 (full), cert, collect.py, run_exp_local.py (256 own seeds; r37 stdout db276eec, r38 1631cbcb) | about 200 | runs/exp_local_r*.json |
| fix 1: q3 replica development | `q3proto.py` (same estimator and random stream as the shipped replica), seeds 1..3 and 10001..10256 (NP 64); timing; equivalence with the shipped code on 10 seeds; row-16 timing tests | about 45 | dev/q3proto.py d9e656dc, dev/proto_np64_s10001-10256.jsonl 1e9cd37f |
| fix 1: freeze | `PREREG_q3x.txt` 9bf1de54 (program ba1dd804, `run_q3x_val.py` fbbd2dc2), 21:18:40Z | - | - |
| fix 1: validation (lock) | `run_q3x_val.py` 0..50 in 8 processes, 21:18:56Z-21:19:22Z: 51 x 21 returned pairs, 1,020 replicates, 69,190 tail successes all accepted | 188 | q3x/val_all.jsonl be894618, LOG.txt 2a4a8649 |
| fix 1: organizer public-seed emulation | `run_exp_org.py` (both experiments, each run twice): 198 and 21 returned pairs; stdout 63df6ff9 and 97394afe | about 9 | q3x/org_emulation.json 56383aa4 (run_exp_org.py fe1bdc6a) |
| fix 1: checks | first-block experiment on the d1 build's 256 seeds with the new program (stdout 1631cbcb, unchanged), selftest 38 (three times), collect.py, cert, assembly; under Python 3.12.14: the public-seed emulation (stdout identical to 3.9), selftest 38 full on the extracted Appendix A (output identical to A.1), review-packet export | about 160 | q3x/exp_local_r38_newprog.json, q3x/org_emulation_py312.json, q3x/selftest38_py312.out |

Runs of this package (Section 14; an Apple-silicon Mac, Python 3.9 and 3.14):

| run | what | CPU | hashes / outputs |
|---|---|---:|---|
| `grouprate.c` | H1 evidence on the bit-sliced family: 8,192 groups x 1,024 batches x 256 lanes = 2^31 full 38-step trials (`grouprate 38 8192 1024 20261009 12`) | 43 | grouprate.log aa775632; grouped-vs-full check OK |
| `disp.c` | H5 evidence: 2,048 groups x 256 x 2^13 grouped trials, seed 20261009 (`disp 2048 13 20261009 12`) | about 48 | output sha256 4a01a652801b55c639aad0b5fc7bc9ab9cc716f17759f8a8bfd3ab1cb495c265 |
| `selftest.py 38 full`, `cert.py 38` | the self-test (A.1) and the ledger | about 60 | A.1; the ledger of Section 8 |
| `run_exp_local.py`-equivalent | first-block experiment on 256 own seeds: 18 pairs, 0 mismatches | about 6 | - |
| `run_exp_org.py` | public-seed emulation of both experiments, each twice: 23 and 21 pairs; stdout 7694c3f1 and 97394afe (q3 byte-identical to b99301f4's) | about 10 | exp_org_out.json |
| `recount_fb.py` | recount of the first-block experiment from the organizer's seed protocol | 2 | 23 groups, 25 valid trials, 256/256 recorded pairs matched |

Development total: about 5,400 CPU-seconds by the d2 authors, below 3,000 CPU-seconds by the b99301f4 authors, and
below 3,000 CPU-seconds for this package (including the r37 evaluator development), far
inside DEV = 2^64 units.  No run was discarded; the aborted SMC v1 is reported above.

After the SMC freeze, `d1core.py` changed in three accounting lines only: the attack driver now adds VCTRL = 3
operations per batch with a W7 pass to V (the update of V and its cap test), GCTRL = 4 per group is defined for
`cert.py`, and Step 3 counts FLAG3B = 2 at each stage-3b entry.  The frozen version had SHA-256
33c84afc151862c8dbb2f519af7bf900ba7c72d31b9b4182372da25e3fb9f641 (the hash in `PREREG_v2.txt`); the data the SMC
reads is unchanged (`tables_digest` bf3bcc643e37895acd208384cebfd8c3f4ff012bbbc123a26a801b88698a4544, printed by the selftest and equal to the value recorded in
`PREREG_v2.txt`).  The SMC itself (`smc.py`) is byte-identical to the frozen file.

Fix 1 (after an internal review of this package) changed `d1core.py` again (e1b12f54 -> ba1dd804) by adding only
the q3 replica (Section 10.2), the dispatch of `__main__` on the experiment id, the imports it needs and two lines
of the header comment; the attack, the counted program
and every count are unchanged (`calibrate` gives the same counts, `tables_digest` is unchanged, and the first-block
experiment's output on the d1 build's 256 local seeds is byte-identical, stdout 1631cbcb).  `cert.py` changed only
in the 38-step allowances, `selftest.py` gained check 8 (the q3 replica).

This package changed `d1core.py` a third time: the first-block evaluator and the experiment's observations as
listed in Section 14.  The data the SMC and the q3 replica read is unchanged (`tables_digest` is still
bf3bcc643e37895acd208384cebfd8c3f4ff012bbbc123a26a801b88698a4544), and `q3_experiment`'s output on the public-seed
request is byte-identical to b99301f4's program's, so the frozen SMC sample and the replica validation carry over.

## 13. Memory and advice

The attack holds the program constants (< 100 words), the group's broadcast planes and hoisted table (< 1,300
words), S, L* and the row masks (< 400
words), the 64 batch registers and the circuit scratch memory (at most one 256-bit word per compiled node, < 8,000
words): below 2^18 bytes even at 32 bytes per word.  The preprocessing enumeration streams its
candidates and keeps L (8 entries).  So the attack itself needs below 2^16 bytes.  The claimed memory covers every charged computation, not only the online attack: a word-RAM computation of K primitives stores at most K words, and the preprocessing is at most 2^78.08755 units = 2^89.50 primitives (Section 8), so its memory is at most 2^94.50 bytes at 32 bytes per word; we claim 2^95 bytes, a bound that needs no measurement.  For information, the largest process the d2 authors ran used 31 GB RSS (the aborted SMC v1, Section 6.3; their
machine has 48 GiB); the runs of this package used at most 55 MiB RSS (the first-block experiment; `disp.c` and
`grouprate.c` use a few MB).  The nonuniform advice is the characteristic and
S (the `CH`, `PAIRS`, `LSTAR` tables of `d1core.py`, below 2^13 bytes), charged as A_C + A_S.

## 14. Changes from b99301f4 (submission b99301f4)

b99301f4 is the reference package: it fixed d2's refuting findings F1 (within-group independence) and F2 (the
uncharged per-batch cap test).  This package keeps its corrections and changes exactly the following; everything
else - the characteristic, S, L*, Step 3, the q3 estimator and its replica, the Step-2 sets, the advice
allowances, the H1/H2/H4/H5 premise forms, the cap and success argument structure - is carried over.

1. **The first-block evaluator is bit-sliced.**  The 7 x 36-bit SWAR batch (1,525 + 2 operations per 7 trials,
   218.14 per trial) becomes a 256-lane bit-plane circuit over 64 registers (49,181 + 2 operations per 256
   trials, 192.12 per trial).  The circuit is compiled once per target and executed as a counted program of
   loads, stores and gate operations with furthest-next-use register allocation (Sections 5.1-5.2).
2. **Step 3's stage-3a gate moved into the circuit (38 steps).**  At 38 steps there is no W6 filter: the old
   batch sent every W7 pass (about 17 per batch at this size) to the scalar rare path.  The circuit now also
   evaluates stage 3a's e16 masked equality, so the rare path runs only for lanes that reach stage 3b - about
   one in 60 batches.  The per-trial success event is unchanged (Section 7).
3. **Group geometry.**  A group now covers 256 lanes x 2^16 batches = 2^24 trials with W15 = (l << 24) | (b << 8) | gb
   (the byte gb comes from the group's second random word; W0..W14 still group-fixed).  Groups stay the
   independent unit; the group setup broadcasts group constants to planes, stores the 29 group-constant words for scalar reuse in the rare path, and hoists shared subexpressions
   (c_G = 5,691, Section 5.3).
4. **Caps and ledger recomputed.**  q_lb = 2^-80.92198, N_G = 1,132,227,176,902,152,117,833,655 groups,
   V_MAX = 4,685,325,007,545,158,831,606,997,380,708 (vbar 63.0815, vmax 963,847), success bound 0.3900022 -
   same argument shape, new constants (`cert.py`, Sections 7-8).
5. **Evidence re-run on the new family.**  `grouprate.c` (2^31 full compressions on the bit-sliced
   enumeration), `disp.c` + `disp_stats.py` (2,048 groups x 2^24 trials on the same enumeration; event b is now
   the real stage-3b reach rather than a proxy), `recount_fb.py` and `run_exp_org.py` (new lane checking and
   return format), `selftest.py` (65,536-lane bit-exactness of the compiled program), `cert.py`, `claim.json`,
   the first-block organizer experiment (6 batches per seed, stage-3a checks) and its manifest.
6. **Unchanged.**  The q3 replica (`q3_experiment`) produces byte-identical output to b99301f4's program on the
   same request, so its design freeze, validation and public-seed numbers carry over (Section 10.2).
7. **Result.**  log2 T = 100.0795358 (b99301f4: 100.3273406, 8f31f0a6: 100.0802924), claimed as 100.07954.

## Appendix A. Program files

These files are the program and the evidence scripts of this package exactly as run (Python 3.9+ standard library
except `smc.py`, which needs numpy; `fcount.c`, `grouprate.c` and `disp.c` are C99 with pthreads where threaded).  Each block below is one file; its
SHA-256 is in the marker line.

- `d1core.py` (64645 bytes): the counted program: reduced SHA-256, characteristic, SFS pair, S, L/L*, the
  bit-sliced circuit compiler and register allocator, the counted VM, group setup, rare path, Step 3,
  verification, the attack driver with caps, calibration, the q3 replica, and the entry point of both organizer
  experiments (byte-identical to experiments/d1core.py).
- `cert.py` (6000 bytes): the exact ledger (Sections 7, 8; adapted by this package).
- `selftest.py` (8223 bytes): the self-test (A.0, A.1; batch checks and ledger adapted by this package).
- `smc.py` (13742 bytes): the SMC estimator of q3 (Section 6; needs numpy; local evidence).
- `smc_summary.py` (1653 bytes): the preregistered decision rule (Section 6.3).
- `run_smc.sh` (1211 bytes): the preregistered runner (lock, nice, logs).
- `SEEDS_38.txt` (160 bytes): the preregistered seeds of this track.
- `PREREG_v2.txt` (1907 bytes): the preregistration record (hashes frozen before the runs).
- `fcount.c` (762 bytes): exhaustive sizes of the Step-2 sets (Section 4.3).
- `grouprate.c` (5578 bytes): the H1 measurement on the grouped first blocks (Section 9; adapted to the
  bit-sliced enumeration).
- `PREREG_q3x.txt` (1949 bytes): the design freeze of the q3 organizer experiment (Section 10.2).
- `run_q3x_val.py` (1730 bytes): the validation of the q3 organizer experiment (Section 10.2).
- `run_exp_org.py` (4085 bytes): the local emulation of the organizer public-seed requests (Section 10; adapted).
- `disp.c` (6281 bytes): the within-group dispersion measurement (H5, Section 9; adapted to the bit-sliced
  enumeration, real stage-3b reach instead of a proxy).
- `disp_stats.py` (1592 bytes): its statistics (adapted).
- `recount_fb.py` (3297 bytes): the recount of the first-block experiment from the organizer's seeds (H5; adapted).

Together 122815 bytes.

### A.0 Extraction and self-test

From the repository root (about 20 s; `full` re-enumerates L and L*; the self-test reads
`verifier/hash_functions.py` under REPO_ROOT):

```sh
mkdir -p /tmp/d1 && python3 - <<'EOF'
import hashlib, re
C = "lanes/exploratory/candidates/sha256-r38/"
t = open(C + "proof.md").read()
n = 0
for name, sha, body in re.findall(r"<!-- file: (\S+) sha256=(\w+) -->\n```\w*\n(.*?)```\n", t, re.S):
    assert hashlib.sha256(body.encode()).hexdigest() == sha, name
    open("/tmp/d1/" + name, "w").write(body)
    n += 1
assert n == 16
assert open(C + "experiments/d1core.py").read() == open("/tmp/d1/d1core.py").read()
EOF
cd /tmp/d1 && REPO_ROOT="$OLDPWD" python3 selftest.py 38 full
```

### A.1 Self-test output (this package, in the pinned image)

```text
{
 "sfs_pair_collides": true,
 "sfs_pair_collides_repo_verifier": true,
 "digest_equals_repo_verifier_len0": true,
 "digest_equals_repo_verifier_len1": true,
 "digest_equals_repo_verifier_len55": true,
 "digest_equals_repo_verifier_len56": true,
 "digest_equals_repo_verifier_len64": true,
 "digest_equals_repo_verifier_len119": true,
 "digest_equals_repo_verifier_len128": true,
 "digest_equals_repo_verifier_len200": true,
 "cells_hold_x_is_Mprime": 0,
 "un_bits_reversed_if_x_is_M": 110,
 "plus_all_paired": 26,
 "plus_pairs_equal": 13,
 "printed_two_bit_failing_(x,y)": [
  [
   "W25[4]=W25[9]",
   [
    false,
    false
   ]
  ]
 ],
 "printed_two_bit_failures_as_stated": true,
 "S_W8_13_x": "3f416758 fe9804cb 63a88c0f 0ceb1f8d a28cd15a 77a1e994",
 "Lstar_size": 1,
 "constants": {
  "c7": "8f6c89c5",
  "d7": "20000000",
  "t7": "03bff800",
  "c6": "75cde31a",
  "d6": "00000000",
  "t6": "00000000",
  "k3": "e983b442"
 },
 "L_and_Lstar_sizes": [
  8,
  1,
  512,
  2621440
 ],
 "tables_digest": "bf3bcc643e37895acd208384cebfd8c3f4ff012bbbc123a26a801b88698a4544",
 "F7_sampled": [
  69817,
  70144.0
 ],
 "counts": {
  "c_init": 9,
  "c_G": 5691,
  "groupconsts": 29,
  "hoisted": 274,
  "c_B": 49181,
  "cats": {
   "ld": 8342,
   "st": 2850,
   "xor": 30106,
   "and": 4989,
   "or": 2841
  },
  "maxreg": 63,
  "scanb": 4,
  "scanl": 45,
  "c_cv": 1021,
  "live_lane": 15,
  "live_3b": 50,
  "c01": 71,
  "c3a": 8,
  "crest": 85,
  "c3b": 2383
 },
 "register_budget": 63,
 "batch_bit_exact": {
  "lanes": 65536,
  "mismatches": 0,
  "w7_pass": 4492,
  "valid": 1,
  "cv_recomputed_wrong": 0
 },
 "step3_reproduces_published_pair": [
  0,
  1
 ],
 "q3x_row16_words": [
  32,
  13
 ],
 "q3x_replicate_seed1": [
  -101.019605,
  69,
  0
 ],
 "q3x_pairs_sfs_repo_verifier": 69,
 "ledger": {
  "log2_p_model": -104.92196791704004,
  "log2_q_group_lb": -80.92197892397101,
  "NG": 1132227176902152117833655,
  "NG_times_q_lb": 0.4943,
  "log2_N": 103.90543773556135,
  "N_times_p": 0.4943037712382643,
  "vbar": 63.08154296875,
  "VMAX": 4685325007545158831606997380708,
  "log2_T": 100.0795358178804,
  "time_log2": 100.07954,
  "preprocessing_log2": 78.08755,
  "success_lower_bound": 0.39000224368885783,
  "log2_hoeffding_exponent": 33.106840568309345
 },
 "success_at_least_0.39": true
}
selftest r38: all checks passed
```

The output is deterministic (no timings).  `cert.py 38` prints the full ledger (Section 8).

### A.2 Source files

<!-- file: d1core.py sha256=cba850fd1a4cc4e8e3cf58f89f51940302bf282e6e20004ada064eb5c9780195 -->
```python
#!/usr/bin/env python3
# d1core.py - counted program of the d1 packages (sha256-r37-prefix-v1 / sha256-r38-prefix-v1), version bs1.
# The two-block collision attack of Li, Zhang, Li, Liu, Qian and Zhu, "Pushing Collision Attacks on SHA-2 to
# 39 Steps", IACR ePrint 2026/1120 (CC BY), in the memory-efficient framework of [LLWS26] (CRYPTO 2026), with
# their characteristics (Tables 15 / 3) and SFS pairs (Tables 17 / 5): reduced SHA-256, cells, SFS pairs, S, L*,
# a counted 256-lane bit-sliced first-block batch with the Step-2 and stage-3a filters in circuit, the counted
# rare path and Step 3 (early abort), verification, the driver with fixed caps, and the two organizer
# experiments (stdin JSON -> stdout JSON), for 38 steps with a reduced replica of smc.py.  Python 3.9+, stdlib.
import sys, json, hashlib, struct, math, random

M32 = 0xffffffff
WORD = (1 << 256) - 1
K = [0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,0xd807aa98,0x12835b01,
     0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,
     0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,
     0x06ca6351,0x14292967,0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,
     0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,0x19a4c116,0x1e376c08,
     0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,
     0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2]
IV = [0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19]
C_REF = {37: 2644, 38: 2728}

def ror(x, n): return ((x >> n) | (x << (32 - n))) & M32
def S0(x): return ror(x, 2) ^ ror(x, 13) ^ ror(x, 22)
def S1(x): return ror(x, 6) ^ ror(x, 11) ^ ror(x, 25)
def s0(x): return ror(x, 7) ^ ror(x, 18) ^ (x >> 3)
def s1(x): return ror(x, 17) ^ ror(x, 19) ^ (x >> 10)
def IF(x, y, z): return (x & y) ^ (~x & z & M32)
def MAJ(x, y, z): return (x & y) ^ (x & z) ^ (y & z)

def compress(cv, w16, R):
    """Target compression: R steps (0..R-1) of SHA-256 from chaining value cv, with feed-forward."""
    w = list(w16)
    for i in range(16, R): w.append((s1(w[i-2]) + w[i-7] + s0(w[i-15]) + w[i-16]) & M32)
    a, b, c, d, e, f, g, h = cv
    for i in range(R):
        t1 = (h + S1(e) + IF(e, f, g) + K[i] + w[i]) & M32
        t2 = (S0(a) + MAJ(a, b, c)) & M32
        a, b, c, d, e, f, g, h = (t1 + t2) & M32, a, b, c, (d + t1) & M32, e, f, g
    return [(x + y) & M32 for x, y in zip(cv, (a, b, c, d, e, f, g, h))]

def blocks(msg):
    """FIPS 180-4 padding; list of 16-word blocks."""
    n = len(msg)
    p = msg + b'\x80' + b'\x00' * ((55 - n) % 64) + struct.pack('>Q', 8 * n)
    return [list(struct.unpack('>16I', p[i:i+64])) for i in range(0, len(p), 64)]

def digest(msg, R):
    cv = list(IV)
    for blk in blocks(msg): cv = compress(cv, blk, R)
    return struct.pack('>8I', *cv)

# ePrint 2026/1120 Table 15 (37 steps) and Table 3 (38 steps): rows not listed are all '='.  MSB first.
# Member x is the message the paper prints second (M'); 'n' = (x, y) bits (0, 1), 'u' = (1, 0), '0'/'1' fixed
# and equal, '=' equal, '+' (undefined in the paper) read as E_i[b] = E_{i-1}[b] for vertical '+' pairs.
# X: Tables 16 / 4 two-bit conditions as printed (word, step, bit, op, word, step, bit); not used by the attack.
CH = {37: dict(
 A={6:'=nu=============================',7:'==========n====n====n======n====',10:'======u===========u=============',
    11:'====u=====u=========u=n====u==n=',12:'=nu=============================',13:'====u=========u=u=======n==u====',
    14:'======u=n=======n===============',16:'==u============================='},
 E={4:'000=============================',5:'111=0=====1==0=====01===++01====',6:'uuu=1011=00=10111=0111=0++1011==',
    7:'10n=u01001n00n00010nu110unuu0001',8:'011=1n+1=n11u1101=001u1u1010=u=1',9:'1=0110+=001=1100=+110100111u=0=+',
    10:'10n001u110101==01+u1101011=1110+',11:'=01un000011101=n0n0u1uu101011u1u',12:'01101uuuuunu010110110n1u0u0uu0n0',
    13:'0+10n110111unn+0n101110110001001',14:'=+0=1000000111+=1==1n010u0=0101=',15:'=u==01===n=011n01==u0=u=1==+====',
    16:'=0=====+00===11=+==01=0=0==+====',17:'=0=====+01===u1=+==0==1===1u====',18:'==10===uu====0==n===111===01==1=',
    19:'==1====00====1==0==========1====',20:'==u====10=======1===00==========',21:'==0=============================',
    22:'==1============================='},
 W={6:'==n=============================',7:'=====u===u==========n===========',8:'==u=============================',
    9:'=====u=u=======n===u==n=u=n=u=n=',10:'============n======u=n==========',14:'=0===u===n=1=1====1=u=1=====1=1=',
    15:'==u=============================',22:'=====0=nn=====1=u=1=============',24:'==n============================='},
 X=[('A',15,15,'!','A',16,15),('A',15,23,'=','A',16,23),('A',15,25,'=','A',16,25),('A',16,9,'!','A',16,20),
    ('A',16,18,'!','A',16,6),('A',16,8,'=','A',16,17),('A',16,29,'=','A',17,29),('A',17,29,'=','A',18,29),
    ('E',15,4,'=','E',16,4),('E',17,0,'!','E',17,13),('E',16,24,'=','E',17,24),('E',16,15,'=','E',17,15),
    ('E',18,6,'!','E',18,19),('E',18,2,'=','E',18,20),('E',20,2,'!','E',20,16),
    ('W',6,1,'=','W',6,12),('W',6,8,'!','W',6,25),('W',6,14,'=','W',6,18),
    ('W',7,0,'=','W',7,28),('W',7,9,'=','W',7,30),('W',7,1,'=','W',7,18),
    ('W',8,1,'!','W',8,12),('W',8,8,'!','W',8,25),('W',8,14,'=','W',8,18),
    ('W',22,31,'!','W',22,1),('W',22,30,'!','W',22,0),('W',22,16,'!','W',22,25),('W',22,14,'!','W',22,21),
    ('W',24,4,'!','W',24,6),('W',24,22,'=','W',24,31),('W',24,20,'!','W',24,27)]),
 38: dict(
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
    16:'==u=============================',23:'=====1=uu=====1=u=1=============',25:'==n============================='},
 X=[('A',14,15,'=','A',16,15),('A',14,23,'=','A',16,23),('A',14,25,'=','A',16,25),('A',15,4,'=','A',16,4),
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
    ('W',25,4,'=','W',25,9),('W',25,22,'=','W',25,31),('W',25,20,'=','W',25,27)])}

def _h(s): return [int(t, 16) for t in s.split()]
# Tables 17 / 5: chaining value, M (printed first), M' (printed second = member x), printed hash.
PAIRS = {
 37: dict(cv=_h('63b4986c 35d83dc0 c98894e4 784e08fc 78a7f752 5ed877a8 315a2db3 d5614eb4'),
  m=_h('4d7f86ff 32ece589 d8accfc4 2cc2e433 068b5b34 eba68a28 2fe12cad 6aa26b0c 9f0d78e1 681b8277 faa9c7e0 56aed439 cc2dbbc2 dd2ba0fc b95d377b 5dd43a81'),
  mp=_h('4d7f86ff 32ece589 d8accfc4 2cc2e433 068b5b34 eba68a28 0fe12cad 6ee2630c bf0d78e1 6d1a90dd faa1d3e0 56aed439 cc2dbbc2 dd2ba0fc bd1d3f7b 7dd43a81'),
  hash=_h('a856d46e 4b46eb28 4935248c 92a2fc98 e0fb2610 10a9951f 54264f5b 80954580')),
 38: dict(cv=_h('cd278980 1b12a052 b87cc8a6 a9e059c5 c9c3db85 6ca4b5b5 63d13ac1 c0329f1e'),
  m=_h('48fc271b 9fca20cd cc89f96f fc40396f 8b328cb4 6b91ef78 97f9b767 e2450045 3b016f58 de9804cb 66a99ea5 0ce30b8d a28cd15a 77a1e994 d28e48a0 9b5f6dbb'),
  mp=_h('48fc271b 9fca20cd cc89f96f fc40396f 8b328cb4 6b91ef78 97f9b767 c2450045 3f416758 fe9804cb 63a88c0f 0ceb1f8d a28cd15a 77a1e994 d28e48a0 9f1f65bb'),
  hash=_h('5d9ca5f4 59ace3a3 26c9c26c 4252c585 4c0803b7 1b4d5ccd 25c3ccc0 90645c4d'))}

# Exact sizes of the Step-2 sets F = {w : s0(w + d) - s0(w) = t mod 2^32} (exhaustive counts over 2^32 words,
# proof.md Section 4.3; reproduced by fcount.c and sampled by selftest.py).
FSIZE = {(37, 7): 68157440, (37, 6): 287309824, (38, 7): 287309824}

def trace(cv, w16, R):
    """A[i], E[i] for i = -4..R-1 (A[-1..-4] = cv[0..3], E[-1..-4] = cv[4..7]) and the expanded W."""
    A = {-1: cv[0], -2: cv[1], -3: cv[2], -4: cv[3]}; E = {-1: cv[4], -2: cv[5], -3: cv[6], -4: cv[7]}
    W = list(w16)
    for i in range(16, R): W.append((s1(W[i-2]) + W[i-7] + s0(W[i-15]) + W[i-16]) & M32)
    for i in range(R):
        E[i] = (A[i-4] + E[i-4] + S1(E[i-1]) + IF(E[i-1], E[i-2], E[i-3]) + K[i] + W[i]) & M32
        A[i] = (E[i] - A[i-4] + S0(A[i-1]) + MAJ(A[i-1], A[i-2], A[i-3])) & M32
    return A, E, W

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

def row(ch, k, i): return cell(ch[k].get(i, '=' * 32))

def follows(ch, k, i, x, y, xprev=None):
    m, v, d, p = row(ch, k, i)
    ok = (x & m) == v and (x ^ y) == d
    if p and k == 'E':
        q = p & row(ch, 'E', i - 1)[3]
        if q: ok = ok and ((x ^ xprev) & q) == 0
    return ok

def cellcheck(R, cv, wx, wy):
    """Mismatching cells of the pair (x, y) from cv on rows -4..R-1; and the two traces."""
    ch = CH[R]; Ax, Ex, Wx = trace(cv, wx, R); Ay, Ey, Wy = trace(cv, wy, R); bad = []
    for i in range(-4, R):
        if not follows(ch, 'A', i, Ax[i], Ay[i]): bad.append(('A', i))
        if not follows(ch, 'E', i, Ex[i], Ey[i], Ex.get(i-1)): bad.append(('E', i))
        if i >= 0 and not follows(ch, 'W', i, Wx[i], Wy[i]): bad.append(('W', i))
    return bad, (Ax, Ex, Wx), (Ay, Ey, Wy)

# Step 1 (from the published SFS pair) and the derived constants.
def stepE(A, E, i, w): return (A[i-4] + E[i-4] + S1(E[i-1]) + IF(E[i-1], E[i-2], E[i-3]) + K[i] + w) & M32
def stepA(A, E, i): return (E[i] - A[i-4] + S0(A[i-1]) + MAJ(A[i-1], A[i-2], A[i-3])) & M32
def sgn(s):
    v = 0
    for c, sym in enumerate(s):
        if sym == 'n': v += 1 << (31 - c)
        if sym == 'u': v -= 1 << (31 - c)
    return v & M32

def enum_L(R, Sx, Sy, Wsx, Wsy, need):
    """Exact freedom set: all (W14, W15) (x side; y side follows) with rows 14 and 15 of A and E following
    the cells for both members, '+' pairs with row 13/14, and the four sigma differences of W14, W15 equal to
    `need`.  Returns (L, number of E14 candidates, number of E15 candidates)."""
    ch = CH[R]; out = []; n14 = n15 = 0
    def cands(i, Eprev):
        m, v, d, p = row(ch, 'E', i)
        q = p & row(ch, 'E', i - 1)[3]
        m |= q; v |= Eprev & q
        free = [b for b in range(32) if not (m >> b) & 1]
        for bits in range(1 << len(free)):
            x = v
            for j, b in enumerate(free):
                if (bits >> j) & 1: x |= 1 << b
            yield x, d
    Ax, Ex = dict(Sx[0]), dict(Sx[1]); Ay, Ey = dict(Sy[0]), dict(Sy[1])
    for e14, d14 in cands(14, Ex[13]):
        n14 += 1
        w14 = (e14 - stepE(Ax, Ex, 14, 0)) & M32; e14y = e14 ^ d14; w14y = (e14y - stepE(Ay, Ey, 14, 0)) & M32
        Ex[14] = e14; Ey[14] = e14y; a14 = stepA(Ax, Ex, 14); a14y = stepA(Ay, Ey, 14)
        if not follows(ch, 'A', 14, a14, a14y): continue
        if ((s1(w14y) - s1(w14)) & M32, (s0(w14y) - s0(w14)) & M32) != need[0]: continue
        Ax[14] = a14; Ay[14] = a14y
        for e15, d15 in cands(15, e14):
            n15 += 1
            e15y = e15 ^ d15
            w15 = (e15 - stepE(Ax, Ex, 15, 0)) & M32; w15y = (e15y - stepE(Ay, Ey, 15, 0)) & M32
            Ex[15] = e15; Ey[15] = e15y
            a15 = stepA(Ax, Ex, 15); a15y = stepA(Ay, Ey, 15)
            if not follows(ch, 'A', 15, a15, a15y): continue
            if ((s1(w15y) - s1(w15)) & M32, (s0(w15y) - s0(w15)) & M32) != need[1]: continue
            out.append((w14, w15, w14y, w15y))
    return out, n14, n15

def lstar_ok(R, P, l):
    """Row-16 modular differences dE16, dA16 (independent of the first block) equal the characteristic's."""
    ch = CH[R]; w14, w15, w14y, w15y = l
    Ax, Ex = dict(P['Sx'][0]), dict(P['Sx'][1]); Ay, Ey = dict(P['Sy'][0]), dict(P['Sy'][1])
    for i, wx, wy in ((14, w14, w14y), (15, w15, w15y)):
        Ex[i] = stepE(Ax, Ex, i, wx); Ey[i] = stepE(Ay, Ey, i, wy); Ax[i] = stepA(Ax, Ex, i); Ay[i] = stepA(Ay, Ey, i)
    dW16 = (s1(w14y) - s1(w14) + P['Wy'][9] - P['Wx'][9]) & M32
    dE16 = (Ay[12] + Ey[12] + S1(Ey[15]) + IF(Ey[15], Ey[14], Ey[13]) - Ax[12] - Ex[12] - S1(Ex[15])
            - IF(Ex[15], Ex[14], Ex[13]) + dW16) & M32
    dA16 = (dE16 - (Ay[12] - Ax[12]) + S0(Ay[15]) - S0(Ax[15]) + MAJ(Ay[15], Ay[14], Ay[13])
            - MAJ(Ax[15], Ax[14], Ax[13])) & M32
    return dE16 == sgn(row_str(ch, 'E', 16)) and dA16 == sgn(row_str(ch, 'A', 16)), (Ax, Ex, Ay, Ey)

def row_str(ch, k, i): return ch[k].get(i, '=' * 32)

LSTAR = {37: [(0xbd1d3f7b, w) for w in (0x7dd41680,0x7dd41681,0x7dd416a0,0x7dd416a1,0x7dd41a80,0x7dd41a81,0x7dd41aa0,
         0x7dd41aa1,0x7dd43680,0x7dd43681,0x7dd436a0,0x7dd436a1,0x7dd43a80,0x7dd43a81,0x7dd43aa0,0x7dd43aa1,0xfdb41680,
         0xfdb41681,0xfdb416a0,0xfdb416a1,0xfdb41a80,0xfdb41a81,0xfdb41aa0,0xfdb41aa1,0xfdb43680,0xfdb43681,0xfdb436a0,
         0xfdb436a1,0xfdb43a80,0xfdb43a81,0xfdb43aa0,0xfdb43aa1)],
         38: [(0xd28e48a0, 0x9f1f65bb)]}

def setup(R, full=False):
    """All constants of the attack for R steps.  full=True re-enumerates L and L* (slow: about 2 s / 20 s);
    otherwise the recorded L* is used and each element is re-checked exactly (rows 14..16 conditions)."""
    ch = CH[R]; pr = PAIRS[R]
    bad, X, Y = cellcheck(R, pr['cv'], pr['mp'], pr['m'])
    assert not bad, bad
    (Ax, Ex, Wx), (Ay, Ey, Wy) = X, Y
    P = dict(R=R, C=C_REF[R], Wx=Wx[:16], Wy=Wy[:16])
    P['Sx'] = ({i: Ax[i] for i in range(14)}, {i: Ex[i] for i in range(14)})
    P['Sy'] = ({i: Ay[i] for i in range(14)}, {i: Ey[i] for i in range(14)})
    A, E = Ax, Ex
    for i in range(6):                 # rows <= 5 and W0..W5 carry no difference in either characteristic
        assert Ax[i] == Ay[i] and (i < 4 or Ex[i] == Ey[i]) and Wx[i] == Wy[i]
    # Step 2 constants (W7 = c7 - A[-1]; W6 = c6 + 2 + ~A[-2] + MAJ(A1,A0,A[-1]) + ~IF(E5,E4,E3) mod 2^32)
    P['c7'] = (E[7] - 2 * A[3] + S0(A[2]) + MAJ(A[2], A[1], A[0]) - S1(E[6]) - IF(E[6], E[5], E[4]) - K[7]) & M32
    P['k3'] = (A[3] - S0(A[2]) - MAJ(A[2], A[1], A[0])) & M32
    P['c6'] = (E[6] - 2 * A[2] + S0(A[1]) - S1(E[5]) - K[6]) & M32
    for i in (6, 7):
        P['d%d' % i] = (Wy[i] - Wx[i]) & M32; P['t%d' % i] = (s0(Wy[i]) - s0(Wx[i])) & M32
    assert (P['c7'] - pr['cv'][0]) & M32 == Wx[7]
    need = (((s1(Wy[14]) - s1(Wx[14])) & M32, (s0(Wy[14]) - s0(Wx[14])) & M32),
            ((s1(Wy[15]) - s1(Wx[15])) & M32, (s0(Wy[15]) - s0(Wx[15])) & M32))
    P['need'] = need
    if full:
        L, n14, n15 = enum_L(R, P['Sx'], P['Sy'], Wx, Wy, need)
        P['L'] = L; P['nE14'] = n14; P['nE15'] = n15
        Ls = [l for l in L if lstar_ok(R, P, l)[0]]
        assert sorted((a, b) for a, b, _, _ in Ls) == sorted(LSTAR[R]), 'L* differs from the recorded list'
        Ls = sorted(Ls, key=lambda l: LSTAR[R].index(l[:2]))
    else:
        Ls = []
        for (w14, w15) in LSTAR[R]:
            Axx, Exx = dict(P['Sx'][0]), dict(P['Sx'][1])
            e14 = stepE(Axx, Exx, 14, w14); Exx[14] = e14; Axx[14] = stepA(Axx, Exx, 14)
            e15 = stepE(Axx, Exx, 15, w15)
            d14 = row(ch, 'E', 14)[2]; d15 = row(ch, 'E', 15)[2]
            Ayy, Eyy = dict(P['Sy'][0]), dict(P['Sy'][1])
            w14y = ((e14 ^ d14) - stepE(Ayy, Eyy, 14, 0)) & M32; Eyy[14] = e14 ^ d14; Ayy[14] = stepA(Ayy, Eyy, 14)
            w15y = ((e15 ^ d15) - stepE(Ayy, Eyy, 15, 0)) & M32
            Ls.append((w14, w15, w14y, w15y))
    # exact re-check of every element of L*: rows 14/15 cells (A, E, W), '+' pairs, sigma differences, row-16 dE/dA
    P['Lstar'] = []
    for l in Ls:
        ok, (Ax2, Ex2, Ay2, Ey2) = lstar_ok(R, P, l)
        w14, w15, w14y, w15y = l
        for i, wx_, wy_ in ((14, w14, w14y), (15, w15, w15y)):
            assert follows(ch, 'A', i, Ax2[i], Ay2[i]) and follows(ch, 'E', i, Ex2[i], Ey2[i], Ex2[i-1])
            assert follows(ch, 'W', i, wx_, wy_)
        assert ok and (((s1(w14y) - s1(w14)) & M32, (s0(w14y) - s0(w14)) & M32), ((s1(w15y) - s1(w15)) & M32,
                (s0(w15y) - s0(w15)) & M32)) == need
        P['Lstar'].append(dict(w=l, Ax=Ax2, Ex=Ex2, Ay=Ay2, Ey=Ey2))
    assert (Wx[14], Wx[15]) in [(d['w'][0], d['w'][1]) for d in P['Lstar']]
    # stage 3a: x-value cells of E16 plus the '+' pairs with E15 (value known per l); W16 = k16 + s0(W1) + W0
    m16, v16, _, p16 = row(ch, 'E', 16); q16 = p16 & row(ch, 'E', 15)[3]
    P['m16'] = m16 | q16
    for d in P['Lstar']:
        Axl, Exl = d['Ax'], d['Ex']
        d['k16'] = (s1(d['w'][0]) + Wx[9]) & M32
        d['c16'] = (Axl[12] + Exl[12] + S1(Exl[15]) + IF(Exl[15], Exl[14], Exl[13]) + K[16]) & M32
        d['v16'] = v16 | (Exl[15] & q16); d['ck16'] = (d['c16'] + d['k16']) & M32
    P['f16'] = bin(P['m16']).count('1')
    # rows R-4..R-1 of A and E carry no difference: the cells of rows >= 16 imply equal outputs
    for i in range(R - 4, R): assert row(ch, 'A', i)[2] == 0 and row(ch, 'E', i)[2] == 0
    P['rows'] = {i: (row(ch, 'A', i), row(ch, 'E', i), row(ch, 'W', i), row(ch, 'E', i)[3] & row(ch, 'E', i - 1)[3])
                 for i in range(16, R)}
    P['F7'] = FSIZE[(R, 7)]; P['F6'] = FSIZE.get((R, 6), 1 << 32); P['s3c'] = stage3_constants(P)
    assert (P['d6'] == 0) == (R == 38)
    return P

def tables_digest(R):
    """SHA-256 of the data the attack and smc.py use (cells, pair, S, L*, row masks, Step-2 constants)."""
    P = setup(R)
    obj = dict(ch=CH[R], pair=PAIRS[R], S=[P['Sx'], P['Sy']], W=[P['Wx'], P['Wy']], rows=P['rows'],
               L=[[d['w'], d['Ax'], d['Ex'], d['Ay'], d['Ey'], d['ck16'], d['v16']] for d in P['Lstar']],
               c=[P[k] for k in ('c7', 'd7', 't7', 'c6', 'd6', 't6', 'k3', 'F6', 'F7', 'm16')])
    return hashlib.sha256(json.dumps(obj, sort_keys=True).encode()).hexdigest()

class Sc:
    """Counted scalar machine: one 32-bit value per word; every primitive 1 (ld, add, sub, and, or, xor, shr, shl,
    compare, branch); m() masks; S0, S1, s0, s1 cost 8 (doubled word x | x << 32, 2 ops); inputs asserted masked."""
    def __init__(self): self.n = 0
    def ld(self, v): self.n += 1; return v
    def add(self, a, b): self.n += 1; return (a + b) & WORD
    def sub(self, a, b): self.n += 1; return (a - b) & WORD
    def m(self, a): self.n += 1; return a & M32
    def xor(self, a, b): self.n += 1; return a ^ b
    def and_(self, a, b): self.n += 1; return a & b
    def or_(self, a, b): self.n += 1; return a | b
    def shl(self, a, k): self.n += 1; return (a << k) & WORD
    def dbl(self, x):
        assert 0 <= x <= M32; self.n += 2; return x | (x << 32)
    def S0(self, x): d = self.dbl(x); self.n += 6; return ((d >> 2) ^ (d >> 13) ^ (d >> 22)) & M32
    def S1(self, x): d = self.dbl(x); self.n += 6; return ((d >> 6) ^ (d >> 11) ^ (d >> 25)) & M32
    def s0(self, x): d = self.dbl(x); self.n += 6; return (((d >> 7) ^ (d >> 18)) & M32) ^ (x >> 3)
    def s1(self, x): d = self.dbl(x); self.n += 6; return (((d >> 17) ^ (d >> 19)) & M32) ^ (x >> 10)
    def IF(self, x, y, z): return self.xor(self.and_(x, self.xor(y, z)), z)
    def MAJ(self, x, y, z): return self.xor(self.and_(self.xor(x, y), self.xor(y, z)), y)
    def eq(self, a, b):
        assert 0 <= a <= M32 and 0 <= b <= M32; self.n += 2; return a == b

# Structural sets.
def varying(R):
    """Schedule words that depend on W15 (structural)."""
    v = {15}
    for i in range(16, R):
        if any(j in v for j in (i - 2, i - 7, i - 15, i - 16)): v.add(i)
    return v


# Step 3 (counted on Sc).
def stage3_constants(P):
    A, E = P['Sx']; c = {}
    c['kE1'] = (A[1] - S0(A[0])) & M32; c['kE2'] = (A[2] - S0(A[1])) & M32
    c['A1&A0'] = A[1] & A[0]; c['A1|A0'] = A[1] | A[0]
    c['kW4'] = (E[4] - A[0] - K[4]) & M32; c['kW5'] = (E[5] - A[1] - S1(E[4]) - K[5]) & M32
    c['kW6'] = (E[6] - A[2] - S1(E[5]) - K[6]) & M32; c['E5&E4'] = E[5] & E[4]; c['~E5'] = E[5] ^ M32
    return c

def step3(sc, P, cv, cost=None):
    """Counted Step 3 for one valid lane (cv = CV1).  Stage 3a per l in L*, then W2..W7 and stage 3b."""
    R = P['R']; ld = sc.ld; A, E = P['Sx']; c = P['s3c']; n0 = sc.n
    a1, a2, a3, a4, e1, e2, e3, e4 = cv
    E0 = sc.m(sc.sub(sc.sub(sc.add(ld(A[0]), a4), sc.S0(a1)), sc.MAJ(a1, a2, a3)))
    W0 = sc.m(sc.sub(sc.sub(sc.sub(sc.sub(sc.sub(E0, a4), e4), sc.S1(e1)), sc.IF(e1, e2, e3)), ld(K[0])))
    E1 = sc.m(sc.sub(sc.add(ld(c['kE1']), a3), sc.MAJ(ld(A[0]), a1, a2)))
    W1 = sc.m(sc.sub(sc.sub(sc.sub(sc.sub(sc.sub(E1, a3), e3), sc.S1(E0)), sc.IF(E0, e1, e2)), ld(K[1])))
    q = sc.add(sc.s0(W1), W0)
    if R == 37: m16 = ld(P['m16']); v16 = ld(P['Lstar'][0]['v16']); sc.keep = [E0, W0, E1, W1, q, m16, v16]
    else: sc.keep = [E0, W0, E1, W1, q]
    if cost is not None: cost['c01'] = sc.n - n0
    rest = None; n3b = 0
    for li, d in enumerate(P['Lstar']):
        n1 = sc.n
        e16 = sc.m(sc.add(ld(d['ck16']), q))
        p3a = sc.eq(sc.and_(e16, m16 if R == 37 else ld(P['m16'])), v16 if R == 37 else ld(d['v16']))
        if cost is not None: cost['c3a'] = sc.n - n1
        if not p3a: continue
        n3b += 1; sc.n += FLAG3B + V3B; n2 = sc.n
        if rest is None:
            E2 = sc.m(sc.sub(sc.add(ld(c['kE2']), a2), sc.or_(ld(c['A1&A0']), sc.and_(a1, ld(c['A1|A0'])))))
            E3 = sc.m(sc.add(ld(P['k3']), a1))
            W2 = sc.m(sc.sub(sc.sub(sc.sub(sc.sub(sc.sub(E2, a2), e2), sc.S1(E1)), sc.IF(E1, E0, e1)), ld(K[2])))
            W3 = sc.m(sc.sub(sc.sub(sc.sub(sc.sub(sc.sub(E3, a1), e1), sc.S1(E2)), sc.IF(E2, E1, E0)), ld(K[3])))
            W4 = sc.m(sc.sub(sc.sub(sc.sub(ld(c['kW4']), E0), sc.S1(E3)), sc.IF(E3, E2, E1)))
            W5 = sc.m(sc.sub(sc.sub(ld(c['kW5']), E1), sc.IF(ld(E[4]), E3, E2)))
            W6 = sc.m(sc.sub(sc.sub(ld(c['kW6']), E2), sc.xor(ld(c['E5&E4']), sc.and_(E3, ld(c['~E5'])))))
            W7 = sc.m(sc.sub(ld(P['c7']), a1))
            rest = [W0, W1, W2, W3, W4, W5, W6, W7]
            rest_y = rest[:6] + [sc.m(sc.add(W6, ld(P['d6']))) if P['d6'] else W6, sc.m(sc.add(W7, ld(P['d7'])))]
            sc.keep_rest = rest + rest_y[6:]
            if cost is not None: cost['crest'] = sc.n - n2
        n4 = sc.n
        wx = P['Wx'][:14] + list(d['w'][:2]); wy = P['Wy'][:14] + list(d['w'][2:])
        X = rest + [ld(wx[i]) for i in range(8, 16)]; Y = rest_y + [ld(wy[i]) for i in range(8, 16)]
        Ax = dict((i, ld(d['Ax'][i])) for i in range(13, 16)); Ex = dict((i, ld(d['Ex'][i])) for i in range(13, 16))
        Ay = dict((i, ld(d['Ay'][i])) for i in range(13, 16)); Ey = dict((i, ld(d['Ey'][i])) for i in range(13, 16))
        ok = True
        for i in range(16, R):
            for Z, wz in ((X, wx), (Y, wy)):
                w = sc.add(sc.add(ld((s1(wz[i-2]) + wz[i-7]) & M32), sc.s0(Z[i-15])), Z[i-16]) if i <= 17 else \
                    sc.add(sc.s1(Z[i-2]), sc.add(ld((wz[i-7] + s0(wz[i-15])) & M32) if i == 22 else Z[i-7], ld((s0(wz[i-15]) + wz[i-16]) & M32) if 24 <= i <= 30 else Z[6] if i == 22 else sc.add(ld(s0(wz[i-15])) if i == 23 else sc.s0(Z[i-15]), Z[i-16])))
                Z.append(sc.m(w))
            k = ld(K[i]) if i >= 20 else 0
            for (Aa, Ee, Z, dA, dE) in ((Ax, Ex, X, d['Ax'], d['Ex']), (Ay, Ey, Y, d['Ay'], d['Ey'])):
                ae = ld((dA[i-4] + dE[i-4] + K[i]) & M32) if i < 20 else sc.add(sc.add(Aa[i-4], Ee[i-4]), k)
                Ee[i] = e16 if i == 16 and Aa is Ax else sc.m(sc.add(ld((dA[12] + dE[12] + S1(dE[15]) + IF(dE[15], dE[14], dE[13]) + K[16]) & M32), Z[16]) if i == 16 else sc.add(sc.add(sc.add(ae, sc.S1(Ee[i-1])), sc.IF(Ee[i-1], Ee[i-2], Ee[i-3])), Z[i]))
                Aa[i] = sc.m(sc.add(Ee[16], ld((S0(dA[15]) + MAJ(dA[15], dA[14], dA[13]) - dA[12]) & M32)) if i == 16 else sc.add(sc.add(sc.sub(Ee[i], ld(dA[i-4]) if i < 20 else Aa[i-4]), sc.S0(Aa[i-1])), sc.MAJ(Aa[i-1], Aa[i-2], Aa[i-3])))
            (mA, vA, dA, _), (mE, vE, dE, _), (mW, vW, dW, _), pq = P['rows'][i]
            acc = None
            for (xv, yv, mm, vv, dd) in ((Ax[i], Ay[i], mA, vA, dA), (Ex[i], Ey[i], mE, vE, dE), (X[i], Y[i], mW, vW, dW)):
                t = sc.xor(xv, yv)
                if dd: t = sc.xor(t, ld(dd))
                if mm:
                    u = sc.and_(xv, ld(mm))
                    if vv: u = sc.xor(u, ld(vv))
                    t = sc.or_(t, u)
                acc = t if acc is None else sc.or_(acc, t)
            if pq: acc = sc.or_(acc, sc.and_(sc.xor(Ex[i], Ex[i-1]), ld(pq)))
            if not sc.eq(acc, 0): ok = False; break
        if cost is not None and ok: cost['c3b'] = sc.n - n4
        if ok: return li, X[:16], Y[:16], n3b
    return None, None, None, n3b

class ScLive(Sc):
    """Sc with a liveness trace (value live from definition to last read; a rotation holds 2 temporaries)."""
    class Vw:
        __slots__ = ('v', 'id')
        def __init__(s, v, i): s.v = v; s.id = i
    def __init__(self):
        Sc.__init__(self); self.t = 0; self.nid = 0; self.defs = {}; self.last = {}; self.tmp = []
    @staticmethod
    def u(x): return x.v if isinstance(x, ScLive.Vw) else x
    def _op(self, xs, v=None, extra=0):
        self.t += 1
        for x in xs:
            if isinstance(x, ScLive.Vw): self.last[x.id] = self.t
        if extra: self.tmp.append((self.t, extra))
        if v is None: return None
        self.nid += 1; self.defs[self.nid] = self.t; return ScLive.Vw(v, self.nid)
    def ld(self, v): self.n += 1; return self._op((), self.u(v))
    def add(self, a, b): self.n += 1; return self._op((a, b), (self.u(a) + self.u(b)) & WORD)
    def sub(self, a, b): self.n += 1; return self._op((a, b), (self.u(a) - self.u(b)) & WORD)
    def m(self, a): self.n += 1; return self._op((a,), self.u(a) & M32)
    def xor(self, a, b): self.n += 1; return self._op((a, b), self.u(a) ^ self.u(b))
    def and_(self, a, b): self.n += 1; return self._op((a, b), self.u(a) & self.u(b))
    def or_(self, a, b): self.n += 1; return self._op((a, b), self.u(a) | self.u(b))
    def S0(self, x): self.n += 8; return self._op((x,), S0(self.u(x)), 2)
    def S1(self, x): self.n += 8; return self._op((x,), S1(self.u(x)), 2)
    def s0(self, x): self.n += 8; return self._op((x,), s0(self.u(x)), 2)
    def s1(self, x): self.n += 8; return self._op((x,), s1(self.u(x)), 2)
    def eq(self, a, b):
        assert 0 <= self.u(a) <= M32 and 0 <= self.u(b) <= M32; self.n += 2; self._op((a, b)); return self.u(a) == self.u(b)
    def peak(self, pinned=()):
        """Largest number of simultaneously live values; pinned values stay live to the end of the trace."""
        ev = []; end = self.t + 1; pin = set(x.id for x in pinned if isinstance(x, ScLive.Vw))
        for i, d in self.defs.items():
            u = end if i in pin else self.last.get(i)
            if u is not None and u > d: ev.append((d, 1)); ev.append((u, -1))
        for t, e in self.tmp: ev.append((t, e)); ev.append((t + 1, -e))
        ev.sort(key=lambda z: (z[0], z[1])); live = best = 0
        for _, x in ev: live += x; best = max(best, live)
        return best

def rare_liveness(R, P):
    """Register demand of Step 3 for one lane on the published pair's CV."""
    cv0 = PAIRS[R]['cv']; li0 = [d['w'][:2] for d in P['Lstar']].index(tuple(P['Wx'][14:16]))
    sc = ScLive(); cv = [sc.ld(c) for c in cv0]
    P2 = dict(P); P2['Lstar'] = [d for i, d in enumerate(P['Lstar']) if i != li0]
    out = step3(sc, P2, cv); assert out[0] is None and out[3] == 0
    lane = sc.peak(pinned=cv + sc.keep)
    sc = ScLive(); cv = [sc.ld(c) for c in cv0]
    li, X, Y, n3b = step3(sc, P, cv); assert li == li0 and n3b == 1
    return lane, sc.peak()

def ref_words(P, cv):
    """Reference (uncounted) W0..W7 of member x from CV1 by the paper's Step-2 equations."""
    A = dict(P['Sx'][0]); E = dict(P['Sx'][1])
    A[-1], A[-2], A[-3], A[-4], E[-1], E[-2], E[-3], E[-4] = cv
    for i in range(4): E[i] = (A[i] + A[i-4] - S0(A[i-1]) - MAJ(A[i-1], A[i-2], A[i-3])) & M32
    return [(E[i] - A[i-4] - E[i-4] - S1(E[i-1]) - IF(E[i-1], E[i-2], E[i-3]) - K[i]) & M32 for i in range(8)]

def inF(w, d, t): return d == 0 or ((s0((w + d) & M32) - s0(w)) & M32) == t

VFIN_UNITS, VFIN_OPS = 6, 512
FLAG3B = 2
VLANE, VENT, SPILL3B = 1, 1, 148
V3B = VENT + SPILL3B

def verify(R, M0, X, Y):
    """Target verification: distinct, equal R-step digests."""
    mx = struct.pack('>16I', *M0) + struct.pack('>16I', *X); my = struct.pack('>16I', *M0) + struct.pack('>16I', *Y)
    if mx != my and digest(mx, R) == digest(my, R): return mx, my
    return None

CONE, CZERO = ('C', 1), ('C', 0)

class Net:
    def __init__(self): self.nodes, self.cse, self.inputs, self.grp, self.hdef = [], {}, {}, set(), {}
    def inp(self, name, grp=True):
        if name not in self.inputs:
            self.nodes.append(('in', name)); n = len(self.nodes) - 1; self.inputs[name] = n
            if grp: self.grp.add(n)
        return (self.inputs[name], 0)
    def gate(self, op, a, b):
        if a > b: a, b = b, a
        key = (op, a, b)
        if key in self.cse: return self.cse[key]
        if a in self.grp and b in self.grp:
            self.nodes.append(('in', 'H%d' % len(self.nodes))); n = len(self.nodes) - 1; self.hdef[n] = key; self.grp.add(n)
        else:
            self.nodes.append(key); n = len(self.nodes) - 1
        self.cse[key] = n; return n
    @staticmethod
    def isc(x): return x[0] == 'C'
    def NOT(self, x): return (x[0], 1 - x[1])
    def XOR(self, x, y):
        if self.isc(x): x, y = y, x
        if self.isc(y): return ('C', x[1] ^ y[1]) if self.isc(x) else (x[0], x[1] ^ y[1])
        if x[0] == y[0]: return ('C', x[1] ^ y[1])
        return (self.gate('xor', x[0], y[0]), x[1] ^ y[1])
    def AND(self, x, y):
        if self.isc(x): x, y = y, x
        if self.isc(y): return x if y[1] else CZERO
        if x[0] == y[0]: return x if x[1] == y[1] else CZERO
        if not x[1] and not y[1]: return (self.gate('and', x[0], y[0]), 0)
        if x[1] and y[1]: return (self.gate('or', x[0], y[0]), 1)
        if x[1]: x, y = y, x
        return (self.gate('and', self.gate('xor', x[0], y[0]), x[0]), 0)
    def OR(self, x, y): return self.NOT(self.AND(self.NOT(x), self.NOT(y)))
    def CH(self, e, f, g):
        if self.isc(e): return f if e[1] else g
        d = self.XOR(f, g)
        if self.isc(d): return self.XOR(g, self.AND(e, d))
        if d[1] == 0: return self.XOR(g if e[1] == 0 else f, (self.gate('and', e[0], d[0]), 0))
        return self.NOT(self.XOR(f if e[1] == 0 else g, (self.gate('or', e[0], d[0]), 0)))
    def MAJ(self, a, b, c):
        d1, d2 = self.XOR(a, b), self.XOR(b, c)
        if self.isc(d1) or self.isc(d2): return self.XOR(b, self.AND(d1, d2))
        if d1[1] == d2[1]:
            t = (self.gate('and' if d1[1] == 0 else 'or', d1[0], d2[0]), 0)
            return self.XOR(b, t) if d1[1] == 0 else self.NOT(self.XOR(b, t))
        return self.NOT(self.XOR(c if d1[1] == 0 else a, (self.gate('or', d1[0], d2[0]), 0)))

class Col:
    def __init__(self, net, nb=32): self.n, self.nb, self.carry, self.j = net, nb, [], 0
    def step(self, bits):
        n = self.n; col = self.carry + list(bits); self.carry = []; last = self.j == self.nb - 1
        k = sum(l[1] for l in col if n.isc(l)); col = [l for l in col if not n.isc(l)]
        if k >= 2 and not last: self.carry += [CONE] * (k // 2)
        if k % 2: col.append(CONE)
        while len(col) >= 3:
            if col[-1] is CONE:
                pr = next(((i, j) for i in range(len(col) - 1) for j in range(i + 1, len(col) - 1) if col[i][1] == col[j][1]), None)
                if pr:
                    b = col.pop(pr[1]); a = col.pop(pr[0]); col.pop()
                    if not last: self.carry.append(n.OR(a, b))
                    col.append(n.NOT(n.XOR(a, b))); continue
            a, b, c = col.pop(0), col.pop(0), col.pop(0)
            if last: col.append(n.XOR(n.XOR(a, b), c)); continue
            if c is CONE:
                self.carry.append(n.OR(a, b)); col.append(n.NOT(n.XOR(a, b))); continue
            t = n.XOR(a, b); col.append(n.XOR(t, c))
            self.carry.append(n.CH(t, c, a) if t[1] == 0 else n.CH((t[0], 0), a, c))
        if len(col) == 2:
            a, b = col
            if not last: self.carry.append(n.AND(a, b))
            col = [n.XOR(a, b)]
        self.j += 1
        return col[0] if col else CZERO

def operands(nd): return () if nd[0] == 'in' else (nd[1], nd[2])

class Cw:
    __slots__ = ('e',)
    def __init__(self, e): self.e = e

def lits(v): return [CONE if (v >> j) & 1 else CZERO for j in range(32)]
SIG = {'S0': (2, 13, 22, None), 'S1': (6, 11, 25, None), 's0': (7, 18, None, 3), 's1': (17, 19, None, 10)}

class Bld:
    def __init__(self, R): self.R = R; self.net = Net(); self.reg = {}
    def planes(self, w):
        if isinstance(w, list): return w
        if w.e[0] in ('K', 'IMM'): return lits(w.e[1] if w.e[0] == 'IMM' else K[w.e[1]])
        i = self.reg.setdefault(w.e, len(self.reg)); return [self.net.inp('G%d[%d]' % (i, j)) for j in range(32)]
    def fn(self, kind, ws):
        if all(isinstance(w, Cw) for w in ws): return Cw((kind,) + tuple(w.e for w in ws))
        n = self.net; p = [self.planes(w) for w in ws]
        if kind in SIG:
            r1, r2, r3, sh = SIG[kind]; q = p[0]
            def f(j):
                x = n.XOR(q[(j + r1) % 32], q[(j + r2) % 32])
                return n.XOR(x, q[(j + r3) % 32]) if r3 else n.XOR(x, q[j + sh] if j + sh < 32 else CZERO)
            return f
        if kind == 'CH': return lambda j: n.CH(p[0][j], p[1][j], p[2][j])
        return lambda j: n.MAJ(p[0][j], p[1][j], p[2][j])
    def prep(self, items, k=None):
        cs = [w.e for w in items if isinstance(w, Cw)]; fs = []
        for w in items:
            if isinstance(w, list): fs.append(lambda j, p=w: p[j])
            elif not isinstance(w, Cw): fs.append(w)
        if k is not None:
            if cs: cs.append(('K', k))
            else: fs.append(lambda j, p=lits(K[k]): p[j])
        if cs:
            cp = self.planes(Cw(('ADD',) + tuple(cs)) if len(cs) > 1 else Cw(cs[0])); fs.append(lambda j, p=cp: p[j])
        return fs
    def add(self, items, k=None):
        fs = self.prep(items, k); c = Col(self.net); return [c.step([f(j) for f in fs]) for j in range(32)]

def build(R):
    """Lock-step emission (W_t, T1, E_t, A_t at bit j).  Bit L of the fail plane is 0 iff lane L is valid."""
    b = Bld(R); n = b.net; var = varying(R); inl = {R - 2, R - 1}
    W = {i: Cw(('W', i)) for i in list(range(15)) + [i for i in range(16, R) if i not in var]}
    W[15] = ([n.inp('gb[%d]' % j) for j in range(8)] + [n.inp('uhi[%d]' % i, False) for i in range(16)]
             + [n.inp('lane[%d]' % i) for i in range(8)])
    A = {i: Cw(('A', i)) for i in range(11, 15)}; E = {i: Cw(('E', i)) for i in range(11, 15)}
    P = setup(R); Sa, Se = P['Sx']; A1, A0, E5, E4 = Sa[1], Sa[0], Se[5], Se[4]
    imm = lambda v: Cw(('IMM', v & M32)); neg = lambda p: [n.NOT(x) for x in p]
    wi = lambda t: [b.fn(fn, [W[u]]) if fn else W[u] for u, fn in ((t-2, 's1'), (t-7, None), (t-15, 's0'), (t-16, None))]
    for t in range(15, R):
        a, bb, c, d, e, f, g, h = A[t-1], A[t-2], A[t-3], A[t-4], E[t-1], E[t-2], E[t-3], E[t-4]
        dep = t in var and t > 15 and t not in inl; last = t == R - 1
        if dep: wf = b.prep(wi(t)); wc = Col(n); W[t] = []
        t1 = [b.fn('S1', [e]), h, b.fn('CH', [e, f, g])] + (wi(t) if t in inl else ([] if dep else [W[t]]))
        s0a, mj = b.fn('S0', [a]), b.fn('MAJ', [a, bb, c])
        nv = sum(not isinstance(x, Cw) for x in t1) + dep
        if last and P['d6']:
            af = b.prep(t1 + [s0a, mj, Cw(('IV', 0))], t); ac = Col(n); A[t] = []
        elif last:
            tf = b.prep(t1, t); tc = Col(n); ef = b.prep([d, imm(IV[4])]); ec = Col(n); af = b.prep([s0a, mj, imm(IV[0])]); ac = Col(n); E[t], A[t] = [], []
        elif nv >= 2:
            tf = b.prep(t1, t); tc = Col(n); ef = b.prep([d]); ec = Col(n); af = b.prep([s0a, mj]); ac = Col(n); E[t], A[t] = [], []
        else:
            ef = b.prep(t1 + [d], t); ec = Col(n); af = b.prep(t1 + [s0a, mj], t); ac = Col(n); E[t], A[t] = [], []
        for j in range(32):
            wj = []
            if dep: W[t].append(wc.step([q(j) for q in wf])); wj = [W[t][j]]
            if last and P['d6']: A[t].append(ac.step([q(j) for q in af] + wj))
            elif nv >= 2 or last:
                tj = tc.step([q(j) for q in tf] + wj)
                E[t].append(ec.step([tj] + [q(j) for q in ef])); A[t].append(ac.step([tj] + [q(j) for q in af]))
            else:
                E[t].append(ec.step([q(j) for q in ef] + wj)); A[t].append(ac.step([q(j) for q in af] + wj))
    am1 = A[R-1]
    def fails(w, dd, tt):
        if dd == 0x20000000 and tt == 0x03bff800:
            f0 = n.OR(n.OR(n.XOR(w[1], w[12]), n.NOT(n.XOR(w[8], w[25]))), n.NOT(n.XOR(w[14], w[18])))
            f1 = n.OR(n.OR(n.XOR(w[2], w[13]), n.NOT(n.XOR(w[9], w[26]))), n.NOT(n.XOR(w[15], w[19])))
            w3_14 = n.XOR(w[3], w[14])
            f2 = n.OR(n.OR(n.XOR(w3_14, w[31]), n.NOT(n.XOR(w3_14, n.XOR(w[10], w[27])))), n.NOT(n.XOR(w3_14, n.XOR(w[16], w[20]))))
            return n.OR(f0, n.AND(w[29], n.OR(f1, n.AND(w[30], f2))))
        u = b.fn('s0', [b.add([w, imm(dd)]) if dd else w]); v = b.add([b.fn('s0', [w]), imm(tt)]); acc = None
        for j in range(32):
            x = n.XOR(u(j), v[j]); acc = x if acc is None else n.OR(acc, x)
        return acc
    fail = fails(b.add([neg(am1), imm(P['c7'] + 1)]), P['d7'], P['t7'])
    if P['d6']:
        e3 = b.add([am1, imm(P['k3'])])
        mjw = [am1[j] if ((A1 ^ A0) >> j) & 1 else lits(A1)[j] for j in range(32)]
        ivw = [lits(E4)[j] if (E5 >> j) & 1 else e3[j] for j in range(32)]
        w6 = b.add([neg(A[R-2]), mjw, neg(ivw), imm(P['c6'] - IV[1] + 2)])
        return b, n.OR(fail, fails(w6, P['d6'], P['t6']))
    e1 = E[R-1]; c = P['s3c']; ngate = lambda f: (lambda j, f=f: n.NOT(f(j)))
    a2 = b.add([A[R-2], imm(IV[1])]); a3 = b.add([A[R-3], imm(IV[2])]); e2 = b.add([E[R-2], imm(IV[5])])
    s0a1, mjA = b.fn('S0', [am1]), b.fn('MAJ', [am1, a2, a3])
    E0 = b.add([ngate(mjA), ngate(s0a1), A[R-4], imm(A0 + IV[3] + 2)])
    mjB = b.fn('MAJ', [lits(A0), am1, a2]); s1E0, ifE0 = b.fn('S1', [E0]), b.fn('CH', [E0, e1, e2])
    W1 = b.add([ngate(s1E0), ngate(ifE0), ngate(mjB), neg(E[R-3]), imm(c['kE1'] - K[1] - IV[6] + 4)])
    e3f = b.prep([E[R-3], imm(IV[6])]); e3c = Col(n, nb=31)
    e3 = [e3c.step([q(j) for q in e3f]) for j in range(31)] + [CZERO]
    s1e1, ife = b.fn('S1', [e1]), b.fn('CH', [e1, e2, e3])
    d = P['Lstar'][0]
    assert not d['v16'] & ~P['m16'] & M32
    fs = b.prep([b.fn('s0', [W1]), ngate(ife), ngate(s0a1), ngate(mjA), ngate(s1e1), neg(E[R-4]), imm(A0 - K[0] - IV[7] + 5 + d['ck16'])])
    col_e16 = Col(n, nb=31); e16 = [col_e16.step([f(j) for f in fs]) for j in range(31)]; acc = fail
    for j in range(31):
        if (P['m16'] >> j) & 1:
            acc = n.OR(acc, n.XOR(e16[j], CONE if (d['v16'] >> j) & 1 else CZERO))
    return b, acc

NREG, BCTRL, TEST = 64, 3, 2

def emit(net, fail, nreg=NREG):
    """Furthest-next-use allocation; r[0..15] batch planes, r[nreg-1] the spillable counter b; every load and
    store explicit.  'test' reads the fail plane (and the ones plane if unnegated), 'loop' reads b."""
    need, st = set(), [fail[0]]
    while st:
        x = st.pop()
        if x not in need: need.add(x); st.extend(operands(net.nodes[x]))
    ones = net.inp('ones')[0]; need.add(ones)
    order = [i for i in range(len(net.nodes)) if i in need and net.nodes[i][0] != 'in'] + ['test', 'loop']
    def opd(x):
        if x == 'test': return (fail[0],) if fail[1] else (fail[0], ones)
        return ('B',) if x == 'loop' else operands(net.nodes[x])
    uses = {}
    for pos, x in enumerate(order):
        for o in opd(x): uses.setdefault(o, []).append(pos)
    INF = 1 << 60; ptr = {}
    def nxt(v, pos):
        u = uses.get(v, ()); i = ptr.get(v, 0)
        while i < len(u) and u[i] < pos: i += 1
        ptr[v] = i; return u[i] if i < len(u) else INF
    uh = [net.inputs['uhi[%d]' % i] for i in range(16)]
    reg = dict((v, i) for i, v in enumerate(uh)); reg['B'] = nreg - 1
    free = [r for r in range(nreg) if r not in reg.values()][::-1]
    inmem = set(i for i in need if net.nodes[i][0] == 'in' and i not in uh); prog = []
    def take(pos, prot):
        if not free:
            v = max((v for v in reg if v not in prot), key=lambda v: nxt(v, pos)); r = reg.pop(v)
            if nxt(v, pos) < INF and v not in inmem: prog.append(('st', v, r)); inmem.add(v)
            free.append(r)
        return free.pop()
    for pos, x in enumerate(order):
        ops = opd(x)
        for o in ops:
            if o not in reg: reg[o] = take(pos, set(ops)); prog.append(('ld', reg[o], o))
        src = [reg[o] for o in ops]
        for o in set(ops):
            if nxt(o, pos + 1) >= INF: free.append(reg.pop(o))
        if x in ('test', 'loop'): prog.append((x,) + tuple(src)); continue
        rd = take(pos + 1, set()); reg[x] = rd; prog.append((net.nodes[x][0], rd, src[0], src[1]))
    return prog

def run_vm(prog, mem, b, fpol, nreg=NREG):
    r = [0] * nreg; r[nreg - 1] = b; ops = 0
    for i in range(16): r[i] = (0 - ((r[nreg - 1] >> i) & 1)) & WORD; ops += 3
    hit = fl = None
    for ins in prog:
        o = ins[0]
        if o == 'ld': r[ins[1]] = mem[ins[2]]; ops += 1
        elif o == 'st': mem[ins[1]] = r[ins[2]]; ops += 1
        elif o == 'xor': r[ins[1]] = r[ins[2]] ^ r[ins[3]]; ops += 1
        elif o == 'and': r[ins[1]] = r[ins[2]] & r[ins[3]]; ops += 1
        elif o == 'or': r[ins[1]] = r[ins[2]] | r[ins[3]]; ops += 1
        elif o == 'test':
            fl = r[ins[1]] ^ (WORD if fpol else 0); hit = (r[ins[1]] != 0) if fpol else (r[ins[1]] != r[ins[2]]); ops += TEST
        else: r[nreg - 1] = r[ins[1]] + 1; ops += BCTRL
    return ops, fl, hit, r[nreg - 1]

class Prog:
    def __init__(self, R):
        self.R = R; self.b, self.fail = build(R); net = self.b.net
        need, st = set(), [self.fail[0]]
        while st:
            x = st.pop()
            if x not in need: need.add(x); st.extend(net.hdef[x][1:] if x in net.hdef else operands(net.nodes[x]))
        oc = {'xor': 0, 'and': 1, 'or': 2}; self.ins, self.code, self.nv = [], [], len(net.nodes); net.cse = None
        for x in sorted(need):
            nd = net.nodes[x]
            if x in net.hdef: op, p, q = net.hdef[x]; self.code.append((x, oc[op], p, q))
            elif nd[0] == 'in': self.ins.append((x, nd[1]))
            else: self.code.append((x, oc[nd[0]], nd[1], nd[2]))
    def f(s, I):
        v = [0] * s.nv
        for x, nm in s.ins: v[x] = I[nm]
        for x, o, p, q in s.code: v[x] = v[p] ^ v[q] if o == 0 else v[p] & v[q] if o == 1 else v[p] | v[q]
        return v[s.fail[0]] ^ (WORD if s.fail[1] else 0)
    def inputs(self, base, gb, b):
        I = {}; reg = self.b.reg; sc = Sc(); memo = {}
        for e, i in reg.items():
            v = cval_sc(sc, e, base, memo)
            for j in range(32): I['G%d[%d]' % (i, j)] = WORD if (v >> j) & 1 else 0
        for j in range(8): I['gb[%d]' % j] = WORD if (gb >> j) & 1 else 0
        for i in range(16): I['uhi[%d]' % i] = WORD if (b >> i) & 1 else 0
        for i in range(8): I['lane[%d]' % i] = sum(1 << L for L in range(256) if (L >> i) & 1)
        I['ones'] = WORD; return I
    def fail_plane(s, base, gb, b): return s.f(s.inputs(base, gb, b))


def group_base(sc, R, w):
    base = dict((('W', i), w[i]) for i in range(15)); a, b, c, d, e, f, g, h = [sc.ld(x) for x in IV]
    for i in range(15):
        t1 = sc.add(sc.add(sc.add(sc.add(h, sc.S1(e)), sc.IF(e, f, g)), sc.ld(K[i])), w[i])
        t2 = sc.add(sc.S0(a), sc.MAJ(a, b, c))
        a, b, c, d, e, f, g, h = sc.m(sc.add(t1, t2)), a, b, c, sc.m(sc.add(d, t1)), e, f, g
        base[('A', i)], base[('E', i)] = a, e
    var = varying(R)
    for i in range(16, R):
        if i not in var:
            base[('W', i)] = sc.m(sc.add(sc.add(sc.s1(base[('W', i-2)]), base[('W', i-7)]), sc.add(sc.s0(base[('W', i-15)]), base[('W', i-16)])))
    return base

def cval_sc(sc, e, base, memo):
    if e in memo: return memo[e]
    o = e[0]
    if o in ('W', 'A', 'E'): v = base[e]
    elif o in ('K', 'IV', 'IMM'): v = sc.ld(K[e[1]] if o == 'K' else IV[e[1]] if o == 'IV' else e[1])
    else:
        a = [cval_sc(sc, x, base, memo) for x in e[1:]]
        if o == 'ADD':
            v = a[0]
            for x in a[1:]: v = sc.add(v, x)
            v = sc.m(v)
        elif o in SIG: v = getattr(sc, o)(a[0])
        else: v = (sc.IF if o == 'CH' else sc.MAJ)(*a)
    memo[e] = v; return v

GPLANE = 4

def group_setup(sc, pg, R, r0, r1):
    """Counted: 2 RAND, unpack, rounds 0..14, constant words and planes, gb planes, hoisted gates, stores."""
    w = [(r0 >> (32 * j)) & M32 for j in range(8)] + [(r1 >> (32 * j)) & M32 for j in range(7)]; gb = (r1 >> 224) & 255
    sc.n += 2 + 2 * 15 + 2
    base = group_base(sc, R, w); memo = {}
    for e, idx in pg.b.reg.items(): base[idx] = cval_sc(sc, e, base, memo)
    sc.n += (GPLANE * 32 + 1) * len(pg.b.reg) + GPLANE * 8 + 4 * len(pg.b.net.hdef) + 15 + 1 + 8
    return base, w, gb

def lane_cv(sc, R, base, gb, b, L):
    """CV1 of lane L of batch b recomputed from the stored group state (rounds 15..R-1, feed-forward)."""
    ld = sc.ld
    if 0 in base:
        w15 = sc.or_(sc.or_(sc.shl(L, 24), sc.shl(b, 8)), ld(gb))
        W = {15: w15, 16: ld(base[('W', 16)]), 18: ld(base[('W', 18)]), 20: ld(base[('W', 20)])}
        a, b_, c, d = [ld(base[('A', i)]) for i in (14, 13, 12, 11)]; e, f, g = [ld(base[('E', i)]) for i in (14, 13, 12)]
        a, b_, c, d, e, f, g, h = sc.m(sc.add(ld(base[1]), w15)), a, b_, c, sc.m(sc.add(ld(base[0]), w15)), e, f, g
        wc = {17: 8, 19: 11, 21: 13, 22: 14, 23: 15, 24: 16, 25: 17, 26: 18, 27: 19, 28: 20, 29: 21, 30: ('W', 14), 31: 23, 32: ('W', 16), 33: 25, 34: ('W', 18), 35: 27, 36: 28}
        tc = {16: 6, 18: 10, 20: 12}
        for i in range(16, R):
            if i not in tc:
                wi = sc.add(sc.s1(W[i-2]), ld(base[wc[i]])) if i in (17, 19, 21, 23, 25, 27) else \
                     sc.add(W[15], ld(base[14])) if i == 22 else \
                     sc.add(sc.add(sc.s1(W[i-2]), W[i-7]), ld(base[wc[i]])) if i <= 29 else \
                     sc.add(sc.add(sc.add(sc.s1(W[i-2]), W[i-7]), sc.s0(W[i-15])), W[i-16]) if i == 37 else \
                     sc.add(sc.add(sc.add(sc.s1(W[i-2]), W[i-7]), ld(base[wc[i]]) if i % 2 else sc.s0(W[i-15])), W[i-16] if i % 2 else ld(base[wc[i]]))
                if i < R - 2: W[i] = sc.m(wi)
            t1 = sc.add(sc.add(sc.S1(e), sc.IF(e, f, g)) if i <= 18 else sc.add(sc.add(h, sc.S1(e)), sc.IF(e, f, g)),
                        ld(base[tc[i]]) if i in tc else sc.add(ld(base[9]), W[17]) if i == 17 else wi if (i == 35 and R == 37) or i == 36 else sc.add(ld(K[i]), wi if i >= R - 2 else W[i]))
            t2 = sc.add(sc.S0(a), sc.MAJ(a, b_, c))
            a, b_, c, d, e, f, g, h = sc.m(sc.add(t1, t2)), a, b_, c, sc.m(sc.add(sc.sub(d, ld(IV[0])) if i == 36 and R == 37 else d, t1)), e, f, g
        return [sc.m(sc.add(x, ld(v))) if j or R > 37 else a for j, (x, v) in enumerate(zip((a, b_, c, d, e, f, g, h), IV))]
    W = dict((i, ld(base[('W', i)])) for i in range(15))
    W[15] = sc.or_(sc.or_(sc.shl(L, 24), sc.shl(b, 8)), ld(gb))
    for i in range(16, R): W[i] = sc.m(sc.add(sc.add(sc.s1(W[i-2]), W[i-7]), sc.add(sc.s0(W[i-15]), W[i-16])))
    a, b_, c, d = [ld(base[('A', i)]) for i in (14, 13, 12, 11)]; e, f, g, h = [ld(base[('E', i)]) for i in (14, 13, 12, 11)]
    for i in range(15, R):
        t1 = sc.add(sc.add(sc.add(sc.add(h, sc.S1(e)), sc.IF(e, f, g)), ld(K[i])), W[i])
        t2 = sc.add(sc.S0(a), sc.MAJ(a, b_, c))
        a, b_, c, d, e, f, g, h = sc.m(sc.add(t1, t2)), a, b_, c, sc.m(sc.add(d, t1)), e, f, g
    return [sc.m(sc.add(x, ld(v))) for x, v in zip((a, b_, c, d, e, f, g, h), IV)]

SCANB, SCANL = 4, 45

def lanes_passing(sc, fl):
    x = fl ^ WORD; sc.n += SCANB; out = []
    while x:
        low = x & -x; out.append(low.bit_length() - 1); x ^= low; sc.n += SCANL
    return out

OPS = {}; PROG = {}
VCTRL, GCTRL, NBATCH = 3, 4, 1 << 16

def prog(R):
    if R not in PROG: PROG[R] = Prog(R)
    return PROG[R]

def attack(R, P, NG, VMAX, coins, nbatch=NBATCH, hook=None):
    pg = prog(R); V = 0
    for gi in range(NG):
        r0, r1 = coins(), coins(); base, M0, gb = group_setup(Sc(), pg, R, r0, r1); I = pg.inputs(base, gb, 0)
        for kb in range(nbatch):
            for i in range(16): I['uhi[%d]' % i] = WORD if (kb >> i) & 1 else 0
            fl = pg.f(I); found = []
            if fl != WORD:
                v = Sc(); v.n += VCTRL
                for L in lanes_passing(v, fl):
                    v.n += VLANE; cv = lane_cv(v, R, base, gb, kb, L)
                    li, X, Y, n3b = step3(v, P, cv); found.append((L, cv, li, n3b))
                    if li is not None:
                        res = verify(R, M0 + [(L << 24) | (kb << 8) | gb], X, Y)
                        if res:
                            if hook: hook(M0, gb, kb, fl, found)
                            return dict(pair=res, V=V + v.n, group=gi, batch=kb)
                V += v.n
            if hook: hook(M0, gb, kb, fl, found)
            if V > VMAX: return dict(pair=None, V=V, group=gi, batch=kb, halted=True)
    return dict(pair=None, V=V, group=NG, batch=0)

def calibrate(R, P):
    """Exact counts over three groups: c_G, c_B, categories, registers, c_cv, Step-3 parts, liveness."""
    pg = prog(R); net = pg.b.net; pr = emit(net, pg.fail); res = None
    for seed in (1, 2, 3):
        h = lambda i: int.from_bytes(hashlib.sha256(b'cal%d-%d' % (seed, i)).digest(), 'big')
        sc = Sc(); base, M0, gb = group_setup(sc, pg, R, h(0), h(1)); cG = sc.n
        I = pg.inputs(base, gb, 0); mem = {}
        for x, nd in enumerate(net.nodes):
            if nd[0] == 'in':
                if x in net.hdef: op, p, q = net.hdef[x]; mem[x] = {'xor': mem[p] ^ mem[q], 'and': mem[p] & mem[q], 'or': mem[p] | mem[q]}[op]
                else: mem[x] = I.get(nd[1], 0)
        kb = h(2) & 0xffff
        for i in range(16): I['uhi[%d]' % i] = WORD if (kb >> i) & 1 else 0
        cB, fl, hit, nb = run_vm(pr, mem, kb, pg.fail[1])
        assert fl == pg.f(I) and hit == (fl != WORD) and nb == kb + 1
        cats = dict((k, sum(1 for i in pr if i[0] == k)) for k in ('ld', 'st', 'xor', 'and', 'or'))
        mx = max(max(i[1:]) for i in pr if i[0] in ('xor', 'and', 'or'))
        s2 = Sc(); lane_cv(s2, R, base, gb, kb, 7); ccv = s2.n
        cost = {}; out = step3(Sc(), P, PAIRS[R]['cv'], cost); lv = rare_liveness(R, P)
        assert out[0] is not None and out[1] == PAIRS[R]['mp'] and out[2] == PAIRS[R]['m']
        cur = dict(c_init=9, c_G=cG, groupconsts=len(pg.b.reg), hoisted=len(net.hdef), c_B=cB, cats=cats, maxreg=mx,
                   scanb=SCANB, scanl=SCANL, c_cv=ccv, live_lane=lv[0], live_3b=lv[1], **cost)
        assert res is None or res == cur, (res, cur)
        res = cur
    OPS[R] = res
    return res

NB_EXP, CHK = {37: 1, 38: 6}, 24

def experiment(req):
    R = {'sha256-r37-prefix-v1': 37, 'sha256-r38-prefix-v1': 38}[req['target_profile']]
    P = setup(R); lsfs = [d['w'][:2] for d in P['Lstar']].index(tuple(P['Wx'][14:16])); rows = []; cal = None
    for tr in req['trials']:
        seed = bytes.fromhex(tr['seed']); ctr = [0]
        if cal is None: cal = calibrate(R, P)
        def coins():
            ctr[0] += 1; return int.from_bytes(hashlib.shake_256(seed + bytes([ctr[0]])).digest(32), 'big')
        obs = dict(lanes_checked=0, mismatches=0, w7_pass=0, valid=0, stage3b=0, deepest_row=15, batch_ops=cal['c_B'])
        first = []
        def hook(M0, gb, kb, fl, found):
            fd = dict((f[0], f) for f in found)
            pick = set(hashlib.shake_256(seed + b'chk' + bytes([kb & 255, kb >> 8])).digest(CHK)) | set(fd) | \
                set(L for L in range(256) if not (fl >> L) & 1)
            for L in sorted(pick):
                blk = M0 + [(L << 24) | (kb << 8) | gb]; cv = compress(IV, blk, R); obs['lanes_checked'] += 1
                W = ref_words(P, cv); p7 = inF(W[7], P['d7'], P['t7'])
                qq = (s0(W[1]) + W[0]) & M32
                p3a = any((((qq + d['ck16']) & M32) & P['m16']) == d['v16'] for d in P['Lstar'])
                valid = p7 and (inF(W[6], P['d6'], P['t6']) if R == 37 else p3a)
                bad = valid != (not (fl >> L) & 1) or valid != (L in fd) or (L in fd and fd[L][1] != cv)
                obs['w7_pass'] += p7
                if valid:
                    obs['valid'] += 1; obs['stage3b'] += fd[L][3]
                    Wy = W[:6] + [(W[6] + P['d6']) & M32, (W[7] + P['d7']) & M32]
                    for li, d in enumerate(P['Lstar']):
                        X = W + P['Wx'][8:14] + list(d['w'][:2]); Y = Wy + P['Wy'][8:14] + list(d['w'][2:])
                        bc = cellcheck(R, cv, X, Y)[0]
                        bad |= any(i < 16 and (k, i) not in (('W', 6), ('W', 7)) for k, i in bc)
                        obs['deepest_row'] = max(obs['deepest_row'], min([i for _, i in bc] + [R]) - 1)
                        if li == lsfs and not first: first.append((blk, X, Y))
                obs['mismatches'] += bad
        attack(R, P, 1, 1 << 60, coins, nbatch=NB_EXP[R], hook=hook)
        row = dict(trial=tr['trial'], message_a_hex=None, message_b_hex=None, observations=obs)
        if first and obs['mismatches'] == 0:
            blk, X, Y = first[0]
            row['message_a_hex'] = (struct.pack('>16I', *blk) + struct.pack('>16I', *X)).hex()
            row['message_b_hex'] = (struct.pack('>16I', *blk) + struct.pack('>16I', *Y)).hex()
        rows.append(row)
    return dict(schema_version=1, trials=rows)

FIX = {38: {('W', 25, 4, '=', 'W', 25, 9): ('W', 25, 4, '=', 'W', 25, 6)}}
KI = {'A': 0, 'E': 1, 'W': 4}
Q3X = dict(K=20, NP=64, MS={17: 128, 18: 4, 19: 4, 20: 1, 21: 1, 22: 1}, MT=512, POOL_LOG2=-101.40)

def xlist(R):
    out = {}
    for x in CH[R]['X']:
        x = FIX[R].get(x, x)
        if max(x[1], x[5]) >= 16: out.setdefault(max(x[1], x[5]), []).append(x)
    return out

def recipe(P, XL, kind, i):
    m0, v, _, _ = row(CH[P['R']], kind, i); m = m0; f = bin(m0).count('1'); pq = 0
    if kind == 'E': pq = P['rows'][i][3]; m |= pq; f += bin(pq).count('1')
    det = m; steps = []
    for (w1, i1, b1, op, w2, i2, b2) in XL.get(i, ()):
        if w1 != kind or w2 != kind: continue
        for (ia, ba, ib, bb) in ((i2, b2, i1, b1), (i1, b1, i2, b2)):
            if ia != i or (det >> ba) & 1: continue
            if ib < i or (det >> bb) & 1 or (ib == i and not (m >> bb) & 1):
                steps.append((ba, ib, bb, int(op == '!'))); m |= 1 << ba; det |= (1 << ba) | (1 << bb); f += 1
                break
    return i, m0, v & m0, pq, steps, f, M32 ^ m

def propose(rc, Wd, rnd):
    i, m0, v, pq, steps, f, _ = rc
    e = v | (rnd & (M32 ^ m0))
    if pq: e = (e & (M32 ^ pq)) | (Wd[i - 1] & pq)
    for ba, ib, bb, fl in steps: e = (e & (M32 ^ (1 << ba))) | (((((Wd[ib] if ib < i else e) >> bb) & 1) ^ fl) << ba)
    return e

def rowok(P, XL, p, i):
    AX, EX, AY, EY, X, Y = p
    (mA, vA, dA, _), (mE, vE, dE, _), (mW, vW, dW, _), pq = P['rows'][i]
    if (AX[i] ^ AY[i]) != dA or (AX[i] & mA) != vA or (EX[i] ^ EY[i]) != dE or (EX[i] & mE) != vE or \
            (X[i] ^ Y[i]) != dW or (X[i] & mW) != vW or (EX[i] ^ EX[i - 1]) & pq: return False
    for (w1, i1, b1, op, w2, i2, b2) in XL.get(i, ()):
        if (((p[KI[w1]][i1] >> b1) ^ (p[KI[w2]][i2] >> b2)) & 1) != (op == '!'): return False
    return True

def cx(A, E, i): return (A[i-4] + E[i-4] + S1(E[i-1]) + IF(E[i-1], E[i-2], E[i-3]) + K[i]) & M32
def ca(A, i): return (S0(A[i-1]) + MAJ(A[i-1], A[i-2], A[i-3]) - A[i-4]) & M32
def stp(A, E, Z, i): E[i] = (cx(A, E, i) + Z[i]) & M32; A[i] = (E[i] + ca(A, i)) & M32
def sch(Z, i): return (s1(Z[i-2]) + Z[i-7] + s0(Z[i-15]) + Z[i-16]) & M32

def particle(P, d):
    p = [[0] * P['R'] for _ in range(6)]
    for i in range(12, 16): p[0][i], p[1][i], p[2][i], p[3][i] = d['Ax'][i], d['Ex'][i], d['Ay'][i], d['Ey'][i]
    p[4][8:16] = P['Wx'][8:14] + list(d['w'][:2]); p[5][8:16] = P['Wy'][8:14] + list(d['w'][2:])
    return p

def set16(p, e, dw):
    AX, EX, AY, EY, X, Y = p
    EX[16] = e; X[16] = (e - cx(AX, EX, 16)) & M32; Y[16] = (X[16] + dw) & M32
    AX[16] = (e + ca(AX, 16)) & M32; stp(AY, EY, Y, 16)

def row16(P, XL):
    rc = recipe(P, XL, 'E', 16); free = [b for b in range(32) if (rc[6] >> b) & 1]
    lo = [sum(((x >> j) & 1) << b for j, b in enumerate(free[:11])) for x in range(1 << 11)]
    hi = [sum(((x >> j) & 1) << b for j, b in enumerate(free[11:])) for x in range(1 << (len(free) - 11))]
    out = []
    for li, d in enumerate(P['Lstar']):
        p = particle(P, d); AX, EX, AY, EY, X, Y = p
        c, a, dw, cy, ay = cx(AX, EX, 16), ca(AX, 16), (s1(Y[14]) - s1(X[14]) + Y[9] - X[9]) & M32, cx(AY, EY, 16), ca(AY, 16)
        for h in hi:
            for l_ in lo:
                e = propose(rc, EX, h | l_); EX[16] = e; AX[16] = (e + a) & M32; X[16] = (e - c) & M32
                Y[16] = (X[16] + dw) & M32; EY[16] = (cy + Y[16]) & M32; AY[16] = (EY[16] + ay) & M32
                if rowok(P, XL, p, 16): out.append((li, e))
    return out, rc[5]

def sfs(P, p, W7):
    """Rebuild a tail success: W0..W7, CV1 and the pair; None unless it is a verified semi-free-start collision."""
    X, Y = p[4], p[5]; W = {7: W7}
    W[6] = (X[22] - s1(X[20]) - X[15] - s0(W7)) & M32
    for i in (5, 4, 3, 2, 1, 0): W[i] = (X[i+16] - s1(X[i+14]) - X[i+9] - s0(W[i+1])) & M32
    wx = [W[i] for i in range(8)] + X[8:16]; wy = wx[:6] + [(W[6] + P['d6']) & M32, (W7 + P['d7']) & M32] + Y[8:16]
    A = dict(P['Sx'][0]); E = dict(P['Sx'][1])
    for i in range(7, -1, -1):
        a = (E[i] - A[i] + S0(A[i-1]) + MAJ(A[i-1], A[i-2], A[i-3])) & M32
        if i >= 4 and a != A[i-4]: return None
        A[i-4] = a; E[i-4] = (E[i] - a - S1(E[i-1]) - IF(E[i-1], E[i-2], E[i-3]) - K[i] - wx[i]) & M32
    cv = [A[-1], A[-2], A[-3], A[-4], E[-1], E[-2], E[-3], E[-4]]; R = P['R']
    ok = wx != wy and compress(cv, wx, R) == compress(cv, wy, R) and ref_words(P, cv) == wx[:8] and \
        inF(W7, P['d7'], P['t7']) and set(cellcheck(R, cv, wx, wy)[0]) <= {('W', 7)}
    return (cv, wx, wy) if ok else None

def below(rng, n):
    k = n.bit_length()
    while True:
        r = rng.getrandbits(k)
        if r < n: return r

def mini_smc(P, XL, V16, rng, NP, MS, MT):
    sets, f16 = V16; est = len(sets) / (len(P['Lstar']) * 2.0 ** 32); stages = [(16, len(sets))]; parts = []
    for _ in range(NP):
        li, e = sets[below(rng, len(sets))]; p = particle(P, P['Lstar'][li]); X, Y = p[4], p[5]
        set16(p, e, (s1(Y[14]) - s1(X[14]) + Y[9] - X[9]) & M32); parts.append(p)
    for i in range(17, 23):
        rc = recipe(P, XL, 'E', i); surv = []
        for p in parts:
            AX, EX, AY, EY, X, Y = p; c = cx(AX, EX, i)
            dy = s1(Y[i-2]) - s1(X[i-2]) + Y[i-7] - X[i-7]
            if i - 15 in (6, 7): dy += P['t%d' % (i - 15)]
            if i - 16 in (6, 7): dy += P['d%d' % (i - 16)]
            for _ in range(MS[i]):
                X[i] = (propose(rc, EX, rng.getrandbits(32)) - c) & M32; Y[i] = (X[i] + dy) & M32
                stp(AX, EX, X, i); stp(AY, EY, Y, i)
                if rowok(P, XL, p, i): surv.append([z[:] for z in p])
        stages.append((i, len(surv))); est *= len(surv) * 2.0 ** -rc[5] / (NP * MS[i])
        if not surv: return 0.0, stages, 0, [], 0
        parts = [surv[below(rng, len(surv))] for _ in range(NP)]
    rc = recipe(P, XL, 'W', 23); wt = 2.0 ** (32 - rc[5]) / P['F7']; hits = bad = 0; pairs = []
    for p in parts:
        AX, EX, AY, EY, X, Y = p; base = (s1(X[21]) + X[16] + s0(X[8])) & M32
        ybase = (s1(Y[21]) + Y[16] + s0(Y[8]) + P['d7']) & M32
        for _ in range(MT):
            w23 = propose(rc, X, rng.getrandbits(32)); W7 = (w23 - base) & M32
            if not inF(W7, P['d7'], P['t7']): continue
            X[23] = w23; Y[23] = (ybase + W7) & M32; ok = True
            for i in range(23, P['R']):
                if i > 23: X[i] = sch(X, i); Y[i] = sch(Y, i)
                stp(AX, EX, X, i); stp(AY, EY, Y, i)
                if not rowok(P, XL, p, i): ok = False; break
            if ok:
                hits += 1; r_ = sfs(P, p, W7)
                if r_ is None: bad += 1
                else: pairs.append(r_)
    stages.append(('tail', hits))
    return est * hits * wt / (NP * MT), stages, hits, pairs, bad

def q3_experiment(req):
    R = {'sha256-r38-prefix-v1': 38}[req['target_profile']]; P = setup(R); XL = xlist(R); V16 = row16(P, XL)
    K_, rows, zs, allp, okall = Q3X['K'], [], [], [], True
    for tr in req['trials']:
        t = tr['trial']; row_ = dict(trial=t, message_a_hex=None, message_b_hex=None)
        if t < K_:
            seed = bytes.fromhex(tr['seed'])
            rng = random.Random(int.from_bytes(hashlib.shake_256(b'd1-q3' + seed).digest(32), 'big'))
            z, st, hits, pairs, bad = mini_smc(P, XL, V16, rng, Q3X['NP'], Q3X['MS'], Q3X['MT'])
            zs.append(z); allp += pairs; good = hits > 0 and bad == 0 and len(pairs) == hits; okall &= good
            row_['observations'] = dict([('log2_estimate', math.log2(z) if z > 0 else -1000.0), ('row16_words', len(V16[0])),
                                         ('tail_successes', hits), ('verified_pairs', len(pairs)), ('failed_rebuilds', bad)] +
                                        [('survivors_%s' % s, n) for s, n in st[1:7]])
            if good:
                cv, wx, wy = pairs[0]
                row_['message_a_hex'] = (struct.pack('>8I', *cv) + struct.pack('>16I', *wx)).hex()
                row_['message_b_hex'] = (struct.pack('>8I', *cv) + struct.pack('>16I', *wy)).hex()
        elif t == K_:
            zbar = sum(zs) / len(zs)
            row_['observations'] = dict(log2_pooled_mean=math.log2(zbar) if zbar > 0 else -1000.0, replicates=len(zs))
            if okall and len(zs) == K_ and zbar >= 2.0 ** Q3X['POOL_LOG2']:
                cv, wx, wy = allp[-1]
                row_['message_a_hex'] = (struct.pack('>8I', *cv) + struct.pack('>16I', *wx)).hex()
                row_['message_b_hex'] = (struct.pack('>8I', *cv) + struct.pack('>16I', *wy)).hex()
        rows.append(row_)
    return dict(schema_version=1, trials=rows)

if __name__ == '__main__':
    req = json.loads(sys.stdin.read())
    out = q3_experiment(req) if req['experiment_id'].startswith('d1-q3-smc') else experiment(req)
    sys.stdout.write(json.dumps(out, sort_keys=True, separators=(',', ':')))
```

<!-- file: cert.py sha256=b28eabe57f8aa1f813648676114f88b1e67039040766d0d47c315723501b5803 -->
```python
#!/usr/bin/env python3
# cert.py - the exact ledger (proof.md Sections 7 and 8).  Every count comes from d1core.calibrate()
# (the counted program) and d1core.setup(R, full=True) (the preprocessing enumeration); every probability is an
# exact rational except q3_model, the preregistered SMC value (H2).  The total is an exact rational; time_log2 is
# rounded up at the 5th decimal.  usage: cert.py 38  (prints JSON; exits non-zero if a check fails)
# Changes from the b99301f ledger: the batch is the 256-lane bit-sliced one (2^16 batches of 256 trials per
# group); the rare path is entered only for lanes reaching stage 3b (the batch evaluates the stage-3a gate per
# lane); the per-lane bound covers the lane scan, the scalar CV recompute, Step 3 to its first stage-3b entry and
# one full stage-3b pass per element of L*.
import sys, json, math
from fractions import Fraction as Fr
import d1core as D

Q3_LOG2 = {37: -74.01, 38: -101.02}          # preregistered q3_model (proof.md Section 6.3), filled from smc_summary.py
KAPPA = {37: Fr(255, 256), 38: Fr(1)}   # r37: disjointness factor for the 32 elements of L* (H2 (b))
# allowances (units): characteristic search A_C, Step-1 solve A_S, all development DEV (proof.md Section 9, H4).
# The rounded 38-step claim is unchanged for A_C up to 2^79 (proof.md Section 8).
ALLOW = {37: (2 ** 56, 2 ** 50, 2 ** 40), 38: (2 ** 78, 2 ** 74, 2 ** 64)}
CTRL_INIT = D.GCTRL                     # per group: zero the batch counter; add, compare, branch on the group counter
INIT_ALLOW = 256                        # resident registers (27 masks/constants) loaded once + program start
PRE_PER_CAND = 1024                     # operation bound per candidate of the L enumeration (each < 300)
MARGIN = Fr(1025, 1024)                 # V_max = ceil(MARGIN * N_B * vbar)
CAPTEST = 2                             # per batch: compare V with V_MAX and branch (executed after every batch)
PAIR = Fr(1, 2 ** 40)                   # H1b: Pr[trial j succeeds | trial i succeeds] <= PAIR (same group, i != j)
XREQ = Fr(4943, 10000)                  # N_G q_lb >= XREQ, so 1 - exp(-N_G q_lb) >= 0.3900022

def log2f(x):
    """log2 of a positive Fraction to ~1e-15 absolute."""
    n, d = x.numerator, x.denominator; k = n.bit_length() - d.bit_length() - 60
    q = (n << -k) // d if k < 0 else n // (d << k)
    return k + math.log2(q)

def ceil5(x): return math.ceil(x * 100000 - 1e-9) / 100000

def ledger(R, q3_log2=None):
    P = D.setup(R, full=True); cal = D.calibrate(R, P); C = D.C_REF[R]; A_C, A_S, DEV = ALLOW[R]
    q3_log2 = Q3_LOG2[R] if q3_log2 is None else q3_log2
    nL = len(P['Lstar']); F7, F6 = P['F7'], P['F6']
    p7 = Fr(F7, 2 ** 32); p6 = Fr(F6, 2 ** 32); p2 = p7 * p6
    fl = math.floor(q3_log2)       # q3 = a rational not above 2^q3_log2
    q3 = Fr(2) ** fl * Fr(math.floor(2 ** (q3_log2 - fl) * 2 ** 40), 2 ** 40)
    pm = p2 * nL * q3 * KAPPA[R]
    per_group = 256 * D.NBATCH
    # group success: Pr[some trial of a group succeeds] >= sum_i Pr[A_i] - sum_{i<j} Pr[A_i and A_j]
    #   >= per_group pm (1 - (per_group - 1) PAIR / 2)                       (H1a, H1b; Bonferroni)
    q_lb = per_group * pm * (1 - (per_group - 1) * PAIR / 2)
    NG = -(-XREQ // q_lb); NG = int(NG)
    NB = NG * D.NBATCH; N = 256 * NB
    assert NG * q_lb >= XREQ
    # data-dependent work per batch (exact expectation bound under H1) and its worst case
    p3a = Fr(1, 2 ** P['f16'])
    Pany = min(Fr(1), 256 * p2 * nL * p3a)       # union bound: Pr[some lane of a batch reaches stage 3b]
    sw = D.SCANB + D.VCTRL                       # per batch with a hit: the lane scan and the V update / cap test
    c3b = cal['c3b'] + D.FLAG3B + D.V3B          # per stage-3b entry: the full pass, the flag test and the spill
    lane = D.SCANL + D.VLANE + cal['c_cv'] + cal['c01'] + nL * (cal['c3a'] + c3b) + cal['crest']
    vbar = Pany * sw + 256 * p2 * nL * p3a * lane
    vmax = sw + 256 * lane
    VMAX = -(-(MARGIN * NB * vbar) // 1); VMAX = int(VMAX)
    pre_ops = (P['nE14'] + P['nE15']) * PRE_PER_CAND + 2 ** 20
    init_ops = cal['c_init'] + INIT_ALLOW
    online_ops = NG * (cal['c_G'] + CTRL_INIT) + NB * (cal['c_B'] + CAPTEST)
    rare_ops = VMAX + vmax
    fin = D.VFIN_UNITS + Fr(D.VFIN_OPS, C)
    T = A_C + A_S + DEV + Fr(pre_ops + init_ops + online_ops + rare_ops, C) + fin
    pre = A_C + A_S + DEV + Fr(pre_ops, C)
    # Hoeffding over the N_G independent groups (fresh coins per group); a group's rare-path work lies in
    # [0, NBATCH vmax]: Pr[V > VMAX] <= exp(-2 (VMAX - E V)^2 / (NG (NBATCH vmax)^2)), VMAX - E V >= (MARGIN - 1) NB vbar
    hexp = 2 * ((MARGIN - 1) * NB * vbar) ** 2 / (NG * (D.NBATCH * vmax) ** 2)
    succ_lb = 1 - math.exp(-float(NG * q_lb)) - 2.0 ** -60 if log2f(hexp) > 6 else None
    out = dict(R=R, C=C, counts=cal, nLstar=nL, F7=F7, F6=F6, f16=P['f16'], nE14=P['nE14'], nE15=P['nE15'],
               log2_p2=log2f(p2), q3_model_log2=q3_log2, kappa=str(KAPPA[R]), log2_p_model=log2f(pm),
               NG=NG, NB=NB, log2_N=log2f(Fr(N)), N_times_p=float(N * pm), log2_q_group_lb=log2f(q_lb),
               NG_times_q_lb=float(NG * q_lb),
               vbar=float(vbar), vmax=int(vmax), VMAX=VMAX, log2_hoeffding_exponent=log2f(hexp),
               ops=dict(pre=pre_ops, init=init_ops, online=online_ops, rare=rare_ops, fin_ops=D.VFIN_OPS),
               units=dict(A_C=A_C, A_S=A_S, DEV=DEV, pre=float(Fr(pre_ops, C)), online=float(Fr(online_ops, C)),
                          rare=float(Fr(rare_ops, C)), fin=float(fin)),
               T_num=T.numerator, T_den=T.denominator, log2_T=log2f(T), time_log2=ceil5(log2f(T)),
               preprocessing_log2=ceil5(log2f(pre)), success_lower_bound=succ_lb,
               log2_units_per_trial=log2f(Fr(cal['c_B'], 256 * C)))
    return out

if __name__ == '__main__':
    R = int(sys.argv[1]); out = ledger(R, float(sys.argv[2]) if len(sys.argv) > 2 else None)
    print(json.dumps(out, indent=1, default=str))
    assert out['success_lower_bound'] >= 0.39
```

<!-- file: selftest.py sha256=62c5c5b9da28d3bddc8890316fc6086d75ef7ff8645ab779be794d67e23bc217 -->
```python
#!/usr/bin/env python3
# selftest.py - checks of the d1 packages (proof.md Appendix A).  Extract the Appendix A files into one
# directory (snippet in Appendix A), then:  REPO_ROOT=/path/to/hash-smash python3 selftest.py 37 [full]
# (or 38).  Without REPO_ROOT the verifier comparisons are skipped and reported as such.  'full' re-enumerates L
# and L* (about 3 s for 37 steps, 14 s for 38 steps).  Exits non-zero on the first failed check.
# Changes from b99301f's selftest.py: the batch check exercises the 256-lane bit-sliced program (all 256 lanes
# of 16 groups x 16 batches, the W7 and stage-3a decisions against the reference compression, the scalar
# lane-CV recompute of every valid lane) and the register check is the allocator's largest index.
import os, sys, json, random, struct, math
import d1core as D
import cert

R = int(sys.argv[1]); full = 'full' in sys.argv[2:]; REPO = os.environ.get('REPO_ROOT'); res = {}
def ok(name, cond, val=None):
    res[name] = val if val is not None else bool(cond)
    if not cond: print(json.dumps(res, indent=1, default=str)); sys.exit('FAILED: ' + name)
hf = None
if REPO:
    sys.path.insert(0, REPO); from verifier import hash_functions as hf
pr = D.PAIRS[R]; ch = D.CH[R]
# 1. the published SFS pair (Table 17 / 5) collides after R steps from its chaining value, with the printed hash
o1, o2 = D.compress(pr['cv'], pr['m'], R), D.compress(pr['cv'], pr['mp'], R)
ok('sfs_pair_collides', o1 == o2 == pr['hash'])
if hf:
    v = lambda cv, w: list(hf._compress('sha256', tuple(cv), struct.pack('>16I', *w), R))
    ok('sfs_pair_collides_repo_verifier', v(pr['cv'], pr['m']) == v(pr['cv'], pr['mp']) == o1)
    for n in (0, 1, 55, 56, 64, 119, 128, 200):
        msg = bytes(random.Random(n).getrandbits(8) for _ in range(n))
        ok('digest_equals_repo_verifier_len%d' % n, D.digest(msg, R) == hf.digest(msg, 'sha256', R))
else: res['repo_verifier'] = 'skipped (REPO_ROOT not set)'
# 2. cells: with member x = the message printed second (M'), every cell of rows -4..R-1 holds
bad, X, Y = D.cellcheck(R, pr['cv'], pr['mp'], pr['m']); ok('cells_hold_x_is_Mprime', not bad, 0)
Ax, Ex, Wx = D.trace(pr['cv'], pr['m'], R); Ay, Ey, Wy = D.trace(pr['cv'], pr['mp'], R)
rev = 0
for k, (u, w) in (('A', (Ax, Ay)), ('E', (Ex, Ey)), ('W', (dict(enumerate(Wx)), dict(enumerate(Wy))))):
    for i, s in ch[k].items():
        for c, sym in enumerate(s):
            b = 31 - c
            if sym in 'un' and ((u[i] >> b) & 1) != (1 if sym == 'u' else 0): rev += 1
res['un_bits_reversed_if_x_is_M'] = rev
# '+' symbols: every one lies in a vertical pair E_i[b], E_{i+1}[b] that is equal on the pair
X0 = X[1]; plus = [(i, 31 - c) for i, s in ch['E'].items() for c, sym in enumerate(s) if sym == '+']
pairs_ = [(i, b) for (i, b) in plus if (i + 1, b) in plus]
ok('plus_all_paired', all((i + 1, b) in plus or (i - 1, b) in plus for i, b in plus), len(plus))
ok('plus_pairs_equal', all(((X0[i] ^ X0[i + 1]) >> b) & 1 == 0 for i, b in pairs_), len(pairs_))
# printed two-bit conditions (Tables 16 / 4): which fail on the pair, per member (x = M', y = M)
V = {'A': (X[0], Y[0]), 'E': (X[1], Y[1]), 'W': (dict(enumerate(X[2])), dict(enumerate(Y[2])))}
fail = []
for (w1, i1, b1, op, w2, i2, b2) in ch['X']:
    r_ = [(((V[w1][s][i1] >> b1) ^ (V[w2][s][i2] >> b2)) & 1 == 0) == (op == '=') for s in (0, 1)]
    if not all(r_): fail.append(['%s%d[%d]%s%s%d[%d]' % (w1, i1, b1, '=' if op == '=' else '!=', w2, i2, b2), r_])
res['printed_two_bit_failing_(x,y)'] = fail
ok('printed_two_bit_failures_as_stated', [f[0] for f in fail] == {37: ['A16[29]=A17[29]'], 38: ['W25[4]=W25[9]']}[R])
# 3. Step 1 solution S, Step-2 constants, the freedom sets (exact)
P = D.setup(R, full=full)
res['S_W8_13_x'] = ' '.join('%08x' % w for w in P['Wx'][8:14]); res['Lstar_size'] = len(P['Lstar'])
res['constants'] = dict((k, '%08x' % P[k]) for k in ('c7', 'd7', 't7', 'c6', 'd6', 't6', 'k3'))
if full: ok('L_and_Lstar_sizes', (len(P['L']), len(P['Lstar'])) == {37: (4096, 32), 38: (8, 1)}[R],
            [len(P['L']), len(P['Lstar']), P['nE14'], P['nE15']])
res['tables_digest'] = D.tables_digest(R)
# 4. Step-2 sets: sampled membership rate against the exact sizes (2^20 samples each, within 5 sigma)
rnd = random.Random(R)
for k, d_, t_, F in ((7, P['d7'], P['t7'], P['F7']), (6, P['d6'], P['t6'], P['F6'])):
    if d_ == 0: continue
    n = 1 << 20; h = sum(D.inF(rnd.getrandbits(32), d_, t_) for _ in range(n)); p = F / 2 ** 32
    ok('F%d_sampled' % k, abs(h - n * p) < 5 * math.sqrt(n * p * (1 - p)), [h, round(n * p, 1)])
# 5. operation counts (data-independent; asserted equal over three groups inside calibrate)
cal = D.calibrate(R, P); res['counts'] = cal
ok('register_budget', cal['maxreg'] < 64, cal['maxreg'])
# 6. bit-exact: 16 groups x 16 batches (65,536 lanes) of the fast evaluator against the repository verifier
#    (or d1core's reference): every lane's Step-2 and stage-3a decisions equal the counted fail plane (the
#    counted program is asserted equal to the fast evaluator inside calibrate), every valid lane's CV1 is
#    recomputed exactly by lane_cv, and W0..W7 of ref_words reproduce S on rows 0..13 (Lemma 1).
comp = (lambda cv, w: list(hf._compress('sha256', tuple(cv), struct.pack('>16I', *w), R))) if hf else D.compress
mis = nl = nv = nvalid = ncv = 0; rnd = random.Random(1000 + R); pg = D.prog(R)
for g in range(16):
    r0, r1 = rnd.getrandbits(256), rnd.getrandbits(256)
    base, M0, gb = D.group_setup(D.Sc(), pg, R, r0, r1); I = pg.inputs(base, gb, 0)
    for kb in range(16):
        for i in range(16): I['uhi[%d]' % i] = D.WORD if (kb >> i) & 1 else 0
        fl = pg.f(I)
        for L in range(256):
            cv = comp(D.IV, M0 + [(L << 24) | (kb << 8) | gb]); nl += 1
            W = D.ref_words(P, cv); p7 = D.inF(W[7], P['d7'], P['t7'])
            qq = (D.s0(W[1]) + W[0]) & D.M32
            p3a = any((((qq + d['ck16']) & D.M32) & P['m16']) == d['v16'] for d in P['Lstar'])
            valid = p7 and (D.inF(W[6], P['d6'], P['t6']) if R == 37 else p3a)
            mis += valid != (not (fl >> L) & 1)
            nv += p7; nvalid += valid
            if valid or L < 8:
                ncv += D.lane_cv(D.Sc(), R, base, gb, kb, L) != cv
            Xm = W + P['Wx'][8:16]; A_, E_, _ = D.trace(cv, Xm, 14)
            mis += any(A_[i] != P['Sx'][0][i] or (i >= 4 and E_[i] != P['Sx'][1][i]) for i in range(14))
mis += ncv
ok('batch_bit_exact', mis == 0, dict(lanes=nl, mismatches=mis, w7_pass=nv, valid=nvalid, cv_recomputed_wrong=ncv))
# 7. Step 3 end to end on the published pair's chaining value: the counted code derives W0..W7, finds the
#    published (W14, W15) in L*, passes every row 16..R-1 and returns exactly the published pair (x = M', y = M)
li, Xw, Yw, n3b = D.step3(D.Sc(), P, pr['cv'])
ok('step3_reproduces_published_pair', li is not None and Xw == pr['mp'] and Yw == pr['m'], [li, n3b])
# 8. (38 steps) the code of the organizer experiment d1-q3-smc: exact row 16 (the same 32 words as smc.py's
#    enumeration), one replicate on a fixed seed reproduces its recorded estimate, and every rebuilt pair is a
#    38-step semi-free-start collision under the repository verifier
if R == 38:
    import random as _r
    XL = D.xlist(R); V16 = D.row16(P, XL)
    ok('q3x_row16_words', len(V16[0]) == 32 and V16[1] == 13, [len(V16[0]), V16[1]])
    z, st, hits, prs, bad = D.mini_smc(P, XL, V16, _r.Random(1), D.Q3X['NP'], D.Q3X['MS'], D.Q3X['MT'])
    ok('q3x_replicate_seed1', abs(math.log2(z) + 101.01960542679035) < 1e-9 and hits == len(prs) == 69 and bad == 0,
       [round(math.log2(z), 6), hits, bad])
    if hf: ok('q3x_pairs_sfs_repo_verifier', all(v(cv, wx) == v(cv, wy) and wx != wy for cv, wx, wy in prs), len(prs))
# 9. the ledger
led = cert.ledger(R)
res['ledger'] = dict((k, led[k]) for k in ('log2_p_model', 'log2_q_group_lb', 'NG', 'NG_times_q_lb', 'log2_N', 'N_times_p', 'vbar',
                                           'VMAX', 'log2_T', 'time_log2', 'preprocessing_log2', 'success_lower_bound',
                                           'log2_hoeffding_exponent'))
ok('success_at_least_0.39', led['success_lower_bound'] >= 0.39)
print(json.dumps(res, indent=1, default=str)); print('selftest r%d: all checks passed' % R)
```

<!-- file: smc.py sha256=be26c0d31c54bd7a48df884a6661c642b74f1e3fb3bf99e506c0da096e887b3b -->
```python
#!/usr/bin/env python3
# smc.py - sequential Monte Carlo lower estimate of p3 (proof.md Section 6), local evidence for H2 (numpy).
# Target: q3 = average over l in L* of Pr[F_l and X'], where F_l = the pair (M1, M1') of l follows every cell of
# rows 16..R-1 (the success event of d1core.step3, which implies equal second-block outputs) and X' = the printed
# two-bit conditions of Tables 16 / 4 on rows >= 16, with the two corrected readings.  q3 <= Pr[F_l] averaged,
# so q3 is a conservative value for the algorithm's p3.  Under H1 the second-block randomness is (W16..W21) iid
# uniform and (W6, W7) uniform on F6 x F7 (r38: W6 uniform on all words), independent (proof.md Lemma 2).
# Stages: rows 16..21 (and r38 row 22) - propose E_i^x with its x-value cells, its '+' pairs and the E-to-E
# two-bit conditions fixed (weight 2^-f, exact), check the whole row; tail - r37 proposes W22 with its cells and
# W-to-W conditions fixed and W7 ~ U(F7), implying W6 (weight 1{W6 in F6} 2^(32-f) / |F6|); r38 proposes E23 and
# implies W7 (weight 1{W7 in F7} 2^(32-f) / |F7|); later rows are deterministic.  Multinomial resampling after
# every stage but the tail; the estimate is the product of the stage means (unbiased for q3).
# usage: smc.py R NP M MT CHUNK seed[r] ...   (a trailing r on a seed also runs the clumping replay)
import sys, math, json, time
import numpy as np
import d1core as D

U = np.uint32
def r(x, n): return (x >> U(n)) | (x << U(32 - n))
def S0(x): return r(x, 2) ^ r(x, 13) ^ r(x, 22)
def S1(x): return r(x, 6) ^ r(x, 11) ^ r(x, 25)
def s0(x): return r(x, 7) ^ r(x, 18) ^ (x >> U(3))
def s1(x): return r(x, 17) ^ r(x, 19) ^ (x >> U(10))
def IF(x, y, z): return (x & y) ^ (~x & z)
def MAJ(x, y, z): return (x & y) ^ (x & z) ^ (y & z)
def inF(w, d, t): return np.ones(w.shape, bool) if d == 0 else (s0(w + U(d)) - s0(w)) == U(t)
KU = [U(k) for k in D.K]
FIX = {37: {('A', 16, 29, '=', 'A', 17, 29): ('A', 15, 29, '=', 'A', 17, 29)},
       38: {('W', 25, 4, '=', 'W', 25, 9): ('W', 25, 4, '=', 'W', 25, 6)}}

def xlist(R):
    """X': the printed two-bit conditions with a word in rows >= 16 (two corrected), keyed by the later row."""
    out = {}
    for x in D.CH[R]['X']:
        x = FIX[R].get(x, x)
        if max(x[1], x[5]) >= 16: out.setdefault(max(x[1], x[5]), []).append(x)
    return out

def init(P, li):
    """Particle state for l-indices li: message words 8..15 of both members and rows 12..15 of A and E."""
    L = P['Lstar']; n = li.size
    st = {'X': {}, 'Y': {}, 'AX': {}, 'EX': {}, 'AY': {}, 'EY': {}}
    for i in range(8, 14): st['X'][i] = np.full(n, P['Wx'][i], U); st['Y'][i] = np.full(n, P['Wy'][i], U)
    W = np.array([d['w'] for d in L], dtype=np.uint64).astype(U)
    st['X'][14] = W[li, 0]; st['X'][15] = W[li, 1]; st['Y'][14] = W[li, 2]; st['Y'][15] = W[li, 3]
    for k, key in (('AX', 'Ax'), ('EX', 'Ex'), ('AY', 'Ay'), ('EY', 'Ey')):
        tab = np.array([[d[key][i] for i in range(12, 16)] for d in L], dtype=np.uint64).astype(U)
        for j, i in enumerate(range(12, 16)): st[k][i] = tab[li, j]
    st['li'] = li.copy()
    return st

def take(st, idx):
    return dict((k, v[idx] if k == 'li' else dict((i, a[idx]) for i, a in v.items())) for k, v in st.items())

def cat(parts):
    return dict((k, np.concatenate([p[k] for p in parts]) if k == 'li' else
                 dict((i, np.concatenate([p[k][i] for p in parts])) for i in parts[0][k])) for k in parts[0])

def cx(t, side, i):
    A, E = t['A' + side], t['E' + side]
    return A[i-4] + E[i-4] + S1(E[i-1]) + IF(E[i-1], E[i-2], E[i-3]) + KU[i]

def step(t, side, i):
    A, E, Z = t['A' + side], t['E' + side], t['X' if side == 'X' else 'Y']
    E[i] = cx(t, side, i) + Z[i]
    A[i] = E[i] - A[i-4] + S0(A[i-1]) + MAJ(A[i-1], A[i-2], A[i-3])

def sched(t, side, i):
    Z = t[side]; Z[i] = s1(Z[i-2]) + Z[i-7] + s0(Z[i-15]) + Z[i-16]

def rowok(P, XL, t, i):
    (mA, vA, dA, _), (mE, vE, dE, _), (mW, vW, dW, _), pq = P['rows'][i]
    ok = np.ones(t['AX'][i].shape, bool)
    for (x, y, m, v, d) in ((t['AX'][i], t['AY'][i], mA, vA, dA), (t['EX'][i], t['EY'][i], mE, vE, dE),
                            (t['X'][i], t['Y'][i], mW, vW, dW)):
        ok &= ((x ^ y) == U(d)) & ((x & U(m)) == U(v))
    if pq: ok &= ((t['EX'][i] ^ t['EX'][i-1]) & U(pq)) == U(0)
    key = {'A': 'AX', 'E': 'EX', 'W': 'X'}
    for (w1, i1, b1, op, w2, i2, b2) in XL.get(i, ()):
        e = ((t[key[w1]][i1] >> U(b1)) ^ (t[key[w2]][i2] >> U(b2))) & U(1)
        ok &= (e == U(0)) if op == '=' else (e == U(1))
    return ok

def propose(P, XL, t, kind, i, rng):
    """x-side word of row i ('E': E_i, 'W': W_i): uniform, except that its x-value cells, its '+' pairs (E) and
    the same-kind two-bit conditions are imposed; returns (word, f) where 2^-f is the exact probability of the
    imposed constraints under the uniform distribution."""
    m, v, _, _ = D.row(D.CH[P['R']], kind, i); n = t['X'][15].size
    rnd = rng.integers(0, 1 << 32, size=n, dtype=np.uint64).astype(U)
    m = int(m); e = (U(v) & U(m)) | (rnd & U(m ^ 0xffffffff)); f = bin(m).count('1')
    if kind == 'E' and P['rows'][i][3]:
        pq = P['rows'][i][3]; e = (e & U(pq ^ 0xffffffff)) | (t['EX'][i-1] & U(pq)); m |= pq; f += bin(pq).count('1')
    key = 'EX' if kind == 'E' else 'X'; det = m          # det: bits whose value is known (fixed or drawn)
    for (w1, i1, b1, op, w2, i2, b2) in XL.get(i, ()):
        if w1 != kind or w2 != kind: continue
        for (ia, ba, ib, bb) in ((i2, b2, i1, b1), (i1, b1, i2, b2)):
            if ia != i or (det >> ba) & 1: continue
            if ib < i or (det >> bb) & 1 or (ib == i and not (m >> bb) & 1):
                src = t[key][ib] if ib < i else e
                bit = (src >> U(bb)) & U(1)
                if op == '!': bit = bit ^ U(1)
                e = (e & U(0xffffffff ^ (1 << ba))) | (bit << U(ba)); m |= 1 << ba; det |= (1 << ba) | (1 << bb); f += 1
                break
    return e, f

def fresh_row(P, XL, t, i, rng):
    """Rows 16..21 (and r38 row 22): W_i^x fresh.  y side: W_i^y = W_i^x + (exact difference of the terms)."""
    e, f = propose(P, XL, t, 'E', i, rng)
    X, Y = t['X'], t['Y']
    wx = e - cx(t, 'X', i)
    dy = (s1(Y[i-2]) - s1(X[i-2])) + (Y[i-7] - X[i-7])
    if i - 15 in (6, 7): dy = dy + U(P['t%d' % (i - 15)])       # s0(W6) in W21, s0(W7) in W22
    if i - 16 in (6, 7): dy = dy + U(P['d%d' % (i - 16)])       # W6 in W22, W7 in W23
    X[i] = wx; Y[i] = wx + dy
    step(t, 'X', i); step(t, 'Y', i)
    return rowok(P, XL, t, i), 2.0 ** -f

def sampleF(rng, n, d, t):
    out = np.empty(0, U)
    while out.size < n:
        c = rng.integers(0, 1 << 32, size=2 * n + 4096, dtype=np.uint64).astype(U)
        out = np.concatenate([out, c[inF(c, d, t)]])
    return out[:n]

def tail(P, XL, t, rng):
    """Last stage: (indicator of rows 22..R-1, weight array, W7)."""
    R = P['R']; X, Y = t['X'], t['Y']; n = X[16].size
    if R == 37:
        w22, f = propose(P, XL, t, 'W', 22, rng)
        W7 = sampleF(rng, n, P['d7'], P['t7'])
        W6 = w22 - s1(X[20]) - X[15] - s0(W7)
        wt = inF(W6, P['d6'], P['t6']) * (2.0 ** (32 - f) / P['F6'])
        X[22] = w22; Y[22] = s1(Y[20]) + Y[15] + s0(W7 + U(P['d7'])) + W6 + U(P['d6'])
        step(t, 'X', 22); step(t, 'Y', 22); ok = rowok(P, XL, t, 22)
        X[23] = s1(X[21]) + X[16] + s0(X[8]) + W7; Y[23] = s1(Y[21]) + Y[16] + s0(Y[8]) + W7 + U(P['d7'])
    else:
        X[23], f = propose(P, XL, t, 'W', 23, rng)
        W7 = X[23] - s1(X[21]) - X[16] - s0(X[8])
        wt = inF(W7, P['d7'], P['t7']) * (2.0 ** (32 - f) / P['F7'])
        Y[23] = s1(Y[21]) + Y[16] + s0(Y[8]) + W7 + U(P['d7']); ok = np.ones(n, bool)
    step(t, 'X', 23); step(t, 'Y', 23); ok &= rowok(P, XL, t, 23)
    for i in range(24, R):
        sched(t, 'X', i); sched(t, 'Y', i); step(t, 'X', i); step(t, 'Y', i); ok &= rowok(P, XL, t, i)
    return ok, wt, W7

def stage16(P, XL):
    """Exact row 16: for each l, E16^x = c_l + W16 is uniform (W16 fresh); enumerate the 2^(32-f) words with the
    x-value cells and '+' bits of E16 fixed and keep those whose whole row 16 (cells and X') holds."""
    m, v, _, _ = D.row(D.CH[P['R']], 'E', 16); pq = P['rows'][16][3]; mm = m | pq
    free = [b for b in range(32) if not (mm >> b) & 1]
    c = np.arange(1 << len(free), dtype=np.uint64).astype(U); dep = np.zeros(c.size, U)
    for j, b in enumerate(free): dep |= ((c >> U(j)) & U(1)) << U(b)
    out = []
    for li, d in enumerate(P['Lstar']):
        keep = []
        for c0 in range(0, dep.size, 1 << 20):
            e = dep[c0:c0 + (1 << 20)] | U((v & m) | (d['Ex'][15] & pq))
            t = init(P, np.full(e.size, li))
            X, Y = t['X'], t['Y']
            X[16] = e - cx(t, 'X', 16); Y[16] = X[16] + (s1(Y[14]) - s1(X[14])) + (Y[9] - X[9])
            step(t, 'X', 16); step(t, 'Y', 16)
            keep.append(e[rowok(P, XL, t, 16)])
        out.append((li, np.concatenate(keep)))
    return out, len(free)

class Reservoir:
    """NP independent uniform draws (with replacement) from all survivors of a stage, streamed by chunks."""
    def __init__(self, rng, NP): self.rng = rng; self.NP = NP; self.slots = None; self.S = 0
    def add(self, surv, s):
        if s == 0: return
        if self.slots is None:
            self.slots = take(surv, self.rng.integers(0, s, self.NP)); self.S = s; return
        sw = np.nonzero(self.rng.random(self.NP) < s / (self.S + s))[0]; self.S += s
        if sw.size:
            new = take(surv, self.rng.integers(0, s, sw.size))
            for k, v in self.slots.items():
                if k == 'li': v[sw] = new[k]
                else:
                    for i in v: v[i][sw] = new[k][i]

def run(R, NP, M, MT, CHUNK, seed, replay=False, V16=None):
    P = D.setup(R); XL = xlist(R); rng = np.random.default_rng(seed); nL = len(P['Lstar'])
    if V16 is None: V16 = stage16(P, XL)
    sets, nfree = V16
    tot16 = sum(e.size for _, e in sets)
    li = np.concatenate([np.full(e.size, l) for l, e in sets]); ee = np.concatenate([e for _, e in sets])
    pick = rng.integers(0, tot16, size=NP)
    st = init(P, li[pick]); t = st
    t['X'][16] = ee[pick] - cx(t, 'X', 16); t['Y'][16] = t['X'][16] + (s1(t['Y'][14]) - s1(t['X'][14])) + (t['Y'][9] - t['X'][9])
    step(t, 'X', 16); step(t, 'Y', 16)
    logp = math.log2(tot16 / (nL * 2.0 ** 32)); stages = [dict(stage=16, log2=logp, hits=tot16, exact=True)]
    per = max(1, CHUNK // NP)
    for i in list(range(17, 22)) + ([22] if R == 38 else []):
        tot = 0.0; done = 0; hits = 0; res = Reservoir(rng, NP)
        while done < M:
            k = min(per, M - done); done += k
            t = take(st, np.repeat(np.arange(NP), k))
            ok, w = fresh_row(P, XL, t, i, rng)
            sel = np.nonzero(ok)[0]; tot += w * sel.size; hits += sel.size
            res.add(take(t, sel), sel.size)          # equal weights: uniform resampling of the survivors
        mean = tot / (NP * M)
        stages.append(dict(stage=i, log2=math.log2(mean) if mean > 0 else None, hits=hits))
        if mean == 0: return dict(R=R, seed=seed, NP=NP, M=M, MT=MT, log2p3=None, stages=stages)
        logp += math.log2(mean); st = res.slots
    tot = 0.0; done = 0; hits = 0; succ = []
    while done < MT:
        k = min(per, MT - done); done += k
        t = take(st, np.repeat(np.arange(NP), k))
        ok, wt, W7 = tail(P, XL, t, rng)
        z = wt * ok; tot += float(z.sum()); hits += int((z > 0).sum())
        if replay and (z > 0).any():
            sel = np.nonzero(z > 0)[0]; succ.append((take(t, sel), W7[sel]))
    mean = tot / (NP * MT)
    stages.append(dict(stage='tail', log2=math.log2(mean) if mean > 0 else None, hits=hits))
    out = dict(R=R, seed=seed, NP=NP, M=M, MT=MT, log2p3=(logp + math.log2(mean)) if mean > 0 else None,
               stages=stages)
    if replay: out['replay'] = clump(P, succ)
    return out

def clump(P, succ):
    """Every successful tail sample: rebuild W0..W7 (inverse of the triangular expansion map), and count the
    elements of L* whose pair follows every cell of rows 16..R-1 for that first block (histogram)."""
    R = P['R']; hist = {}
    for (t, W7) in succ:
        X = t['X']; n = W7.size
        W = {7: W7, 6: X[22] - s1(X[20]) - X[15] - s0(W7)}
        for i in (5, 4, 3, 2, 1, 0): W[i] = X[i+16] - s1(X[i+14]) - X[i+9] - s0(W[i+1])
        cnt = np.zeros(n, int)
        for li in range(len(P['Lstar'])):
            u = init(P, np.full(n, li))
            for i in range(8):
                u['X'][i] = W[i]; u['Y'][i] = W[i] + (U(P['d%d' % i]) if i in (6, 7) else U(0))
            ok = np.ones(n, bool)
            for i in range(16, R):
                sched(u, 'X', i); sched(u, 'Y', i); step(u, 'X', i); step(u, 'Y', i); ok &= rowok(P, {}, u, i)
            cnt += ok
        for c in cnt.tolist(): hist[c] = hist.get(c, 0) + 1
    return hist

if __name__ == '__main__':
    R, NP, M, MT, CHUNK = (int(a) for a in sys.argv[1:6])
    P0 = D.setup(R); t0 = time.time(); fn = 'stage16_r%d_%s.npz' % (R, D.tables_digest(R)[:16])
    try:
        z = np.load(fn); V16 = ([(int(li), z['e%d' % li]) for li in z['li']], int(z['free']))
    except (IOError, OSError):
        V16 = stage16(P0, xlist(R))
        np.savez(fn, li=np.array([li for li, _ in V16[0]]), free=V16[1], **dict(('e%d' % li, e) for li, e in V16[0]))
    print(json.dumps(dict(R=R, stage16_exact=dict((li, int(e.size)) for li, e in V16[0]), free_bits=V16[1],
                          sec=round(time.time() - t0, 1))), flush=True)
    for sd in sys.argv[6:]:
        rep = sd.endswith('r'); s_ = int(sd.rstrip('r')); t0 = time.time()
        out = run(R, NP, M, MT, CHUNK, s_, replay=rep, V16=V16); out['sec'] = round(time.time() - t0, 1)
        print(json.dumps(out), flush=True)
```

<!-- file: smc_summary.py sha256=c27f01cf511378cbb1398e20cf84b2395a71f9c86bb7678fad2d20595717dc8e -->
```python
#!/usr/bin/env python3
# smc_summary.py - the preregistered decision rule (proof.md Section 6.3).  Reads runs/smc/r<R>_<seed>.json for
# every seed of SEEDS_<R>.txt (none may be missing or excluded).  Z_s = 2^log2p3 of seed s (an unbiased estimate
# of q3); LB = mean(Z) - t * sd(Z) / sqrt(n) with the one-sided 99% Student quantile t = 2.4529 for n - 1 = 31
# degrees of freedom; q3_model = 2^(floor(100 log2 LB) / 100).  Also reports the stage means and the replay.
import json, math, sys
R = int(sys.argv[1]); d = sys.argv[2] if len(sys.argv) > 2 else '../runs/smc'
seeds = [s.strip().rstrip('r') for s in open('SEEDS_%d.txt' % R) if s.strip()]
runs = [json.loads(open('%s/r%d_%s.json' % (d, R, s)).read().strip().splitlines()[-1]) for s in seeds]
assert len(runs) == 32 and all(r_['log2p3'] is not None for r_ in runs)
lg = [r_['log2p3'] for r_ in runs]; n = len(lg)
Z = [2.0 ** x for x in lg]; mean = sum(Z) / n; sd = math.sqrt(sum((z - mean) ** 2 for z in Z) / (n - 1))
LB = mean - 2.4529 * sd / math.sqrt(n)
out = dict(R=R, n=n, log2_mean=math.log2(mean), log2_LB99=math.log2(LB), rel_sd=sd / mean,
           q3_model_log2=math.floor(100 * math.log2(LB)) / 100, log2_min=min(lg), log2_max=max(lg),
           log2_geomean=sum(lg) / n)
st = {}
for r_ in runs:
    for s in r_['stages']: st.setdefault(str(s['stage']), []).append(s['log2'])
out['stage_mean_log2'] = dict((k, sum(v) / len(v)) for k, v in st.items())
out['tail_hits_total'] = sum(r_['stages'][-1]['hits'] for r_ in runs)
rep = {}
for r_ in runs:
    for k, v in r_.get('replay', {}).items(): rep[k] = rep.get(k, 0) + v
out['replay_histogram'] = rep
print(json.dumps(out, indent=1))
```

<!-- file: run_smc.sh sha256=4be2a3f52ee06d83ee03a66140145261ea07b304d353222a694beb42dd4813cd -->
```sh
#!/bin/bash
# run_smc.sh - preregistered SMC runs (proof.md Section 6.3).  Takes the shared heavy-job lock, runs the seeds of
# SEEDS_<R>.txt with nice -n 10, at most PAR (default 8) at a time, one JSON line per seed in runs/smc/r<R>_<seed>.json, and
# logs UTC start/end and /usr/bin/time CPU seconds and peak RSS per seed to runs/smc/LOG.txt.
# usage (from src/): ./run_smc.sh 37 | ./run_smc.sh 38
set -e
R=$1; L="$HEAVY_LOCK"; OUT=../runs/smc; P=${PAR:-8}
case $R in 37) ARGS="37 4000 2048 4096 262144";; 38) ARGS="38 4000 2048 8192 262144";; *) exit 1;; esac
until mkdir "$L" 2>/dev/null; do sleep 30; done
trap 'rmdir "$L"' EXIT
echo "$(date -u +%FT%TZ) lock acquired r$R" >> $OUT/LOG.txt
one() { s=$1; f=$OUT/r${R}_${s%r}.json
  echo "$(date -u +%FT%TZ) start r$R seed $s" >> $OUT/LOG.txt
  /usr/bin/time -l nice -n 10 python3 smc.py $ARGS $s > $f 2> $f.time
  echo "$(date -u +%FT%TZ) end r$R seed $s user=$(awk '/user/{print $3}' $f.time | head -1) rss=$(awk '/maximum resident/{print $1}' $f.time) sha256=$(shasum -a 256 $f | cut -c1-16)" >> $OUT/LOG.txt; }
export -f one; export R ARGS OUT
xargs -P $P -n 1 bash -c 'one "$0"' < SEEDS_$R.txt
echo "$(date -u +%FT%TZ) lock released r$R" >> $OUT/LOG.txt
```

<!-- file: SEEDS_38.txt sha256=ebed9e0315fe3aed2ea5843d5f7a2e3875d0b1be31deb70504861780e3140816 -->
```text
4001
4002
4003
4004
4005
4006
4007
4008
4009
4010
4011
4012
4013
4014
4015
4016
4017
4018
4019
4020
4021
4022
4023
4024
4025
4026
4027
4028
4029
4030
4031
4032
```

<!-- file: PREREG_v2.txt sha256=7613bbfe51e091fa13992e763aeed8030b698c8ccf1d401a65045ded4f0c7711 -->
```text
SMC preregistration v2 (d1 packages), frozen 2026-10-08T20:25:28Z before any of the listed seeds was run.
v1 (frozen 2026-10-08T20:22:03Z, seeds 1001..1032 / 2001..2032) was aborted at 20:23Z after 8 r37 seeds because 8 parallel runs reached 31 GB RSS; its code, log and all 8 complete outputs are kept in runs/smc/v1_aborted and reported in proof.md. v2 changes only memory handling (cached exact stage 16, streamed resampling), which changes the random streams; v2 uses new seeds.
Rule: smc_summary.py (q3_model = floor to 0.01 bit of log2 of the one-sided 99% Student lower bound of the mean of the 32 per-seed estimates; no seed may be dropped).
Parameters: r37: smc.py 37 4000 2048 4096 262144 <seed>; r38: smc.py 38 4000 2048 8192 262144 <seed> (run_smc.sh, PAR=8).
Seeds: SEEDS_37.txt (3001..3032; 3001r..3003r also run the clumping replay), SEEDS_38.txt (4001..4032).
Dev runs before this freeze (not part of the sample): seeds 101, 102, 103r, 9, 77, 78r and small tests; disclosed in proof.md.
tables_digest r37 a85c62555c8e3c5712fc82c1e1525272bbdb2fe16635e73058a60b03beeb0da9
tables_digest r38 bf3bcc643e37895acd208384cebfd8c3f4ff012bbbc123a26a801b88698a4544
be26c0d31c54bd7a48df884a6661c642b74f1e3fb3bf99e506c0da096e887b3b  smc.py
c27f01cf511378cbb1398e20cf84b2395a71f9c86bb7678fad2d20595717dc8e  smc_summary.py
4be2a3f52ee06d83ee03a66140145261ea07b304d353222a694beb42dd4813cd  run_smc.sh
7dff39b082f8759e6973e07dec7cdaeaac9183286bd28b225b50c4b56fae3d52  SEEDS_37.txt
ebed9e0315fe3aed2ea5843d5f7a2e3875d0b1be31deb70504861780e3140816  SEEDS_38.txt
33c84afc151862c8dbb2f519af7bf900ba7c72d31b9b4182372da25e3fb9f641  d1core.py
4be485bad2c7b82e075665dd887b8efcaa467826302b9ee8a04563828760fa1f  fcount.c
b49899b94e0063d8b02ca1f08d96d61969cd0e788861303c0c14276217ee4807  stage16_r37_a85c62555c8e3c57.npz
9761e538625b53e537e04f8a978d7cc345c54c88fa159181e8c6f8891020dc2f  stage16_r38_bf3bcc643e37895a.npz
```

<!-- file: fcount.c sha256=4be485bad2c7b82e075665dd887b8efcaa467826302b9ee8a04563828760fa1f -->
```c
/* fcount.c - exact sizes of the Step-2 sets F = { w in [0, 2^32) : s0(w + d) - s0(w) = t (mod 2^32) } by
   exhaustive enumeration (proof.md Section 4.3).  usage: fcount d t   (hex)   e.g. fcount fbc00800 017f8000 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
static inline uint32_t ror(uint32_t x, int n) { return (x >> n) | (x << (32 - n)); }
static inline uint32_t s0(uint32_t x) { return ror(x, 7) ^ ror(x, 18) ^ (x >> 3); }
int main(int argc, char **argv) {
    uint32_t d = (uint32_t)strtoul(argv[1], 0, 16), t = (uint32_t)strtoul(argv[2], 0, 16);
    uint64_t n = 0; uint32_t w = 0;
    do { n += (uint32_t)(s0(w + d) - s0(w)) == t; } while (++w != 0);
    printf("d=%08x t=%08x |F|=%llu\n", d, t, (unsigned long long)n);
    return 0;
}
```

<!-- file: grouprate.c sha256=a7846d716c8d06f54c181b24a152c74796cf55f17beb0484fdef2358d0903e00 -->
```c
/* grouprate.c - local H1 evidence (proof.md Section 9.1): Step-2 and stage-3a rates on the attack's own
   grouped first blocks.  Each group draws W0..W14 and gb (xoshiro256**, seeded); lane l of batch k has
   W15 = (l << 24) | (k << 8) | gb (k < K batches); every trial is the full R-step compression from the IV
   with feed-forward (no shortcut).  Counts W7 passes, valid lanes (W7 and, for 37 steps, W6 in their exact
   sets, for 38 steps the stage-3a gate on the single element of L*) and batches with >= 1 and >= 2 valid lanes.
   usage: grouprate R groups K seed threads   (cc -O3 -pthread) */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <pthread.h>
static const uint32_t K[64] = {0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,
0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,0xe49b69c1,0xefbe4786,0x0fc19dc6,
0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,
0x06ca6351,0x14292967,0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,0xa2bfe8a1,
0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,
0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7};
static const uint32_t IV[8] = {0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19};
#define ROR(x,n) (((x) >> (n)) | ((x) << (32 - (n))))
#define S0(x) (ROR(x,2) ^ ROR(x,13) ^ ROR(x,22))
#define S1(x) (ROR(x,6) ^ ROR(x,11) ^ ROR(x,25))
#define s0(x) (ROR(x,7) ^ ROR(x,18) ^ ((x) >> 3))
#define s1(x) (ROR(x,17) ^ ROR(x,19) ^ ((x) >> 10))
#define CH(e,f,g) (((e)&(f)) ^ (~(e)&(g)))
#define MJ(a,b,c) (((a)&(b)) ^ ((a)&(c)) ^ ((b)&(c)))
static int R; static long G, KB; static uint64_t SEED; static int NT;
static uint32_t c7, d7, t7, c6, d6, t6, k3, A1, A0, E5, E4, SA0, SA1, CK16, M16, V16;
static uint64_t rotl(uint64_t x, int k) { return (x << k) | (x >> (64 - k)); }
static uint64_t nxt(uint64_t *s) { uint64_t r = rotl(s[1] * 5, 7) * 9, t = s[1] << 17; s[2] ^= s[0]; s[3] ^= s[1]; s[1] ^= s[2];
  s[0] ^= s[3]; s[2] ^= t; s[3] = rotl(s[3], 45); return r; }
/* stage-3a gate of the attack for 38 steps: ref_words' W0, W1 from CV1, then (s0(W1)+W0+ck16) & m16 == v16 */
static int e16ok(uint32_t *cv) {
  uint32_t E0 = SA0 + cv[3] - S0(cv[0]) - MJ(cv[0], cv[1], cv[2]);
  uint32_t E1 = SA1 + cv[2] - S0(SA0) - MJ(SA0, cv[0], cv[1]);
  uint32_t W0 = E0 - cv[3] - cv[7] - S1(cv[4]) - CH(cv[4], cv[5], cv[6]) - K[0];
  uint32_t W1 = E1 - cv[2] - cv[6] - S1(E0) - CH(E0, cv[4], cv[5]) - K[1];
  return (((s0(W1) + W0 + CK16) & M16) == V16);
}
typedef struct { int id; uint64_t trials, w7, valid, b1, b2; } job;
static void *work(void *arg) {
  job *j = arg; uint64_t s[4] = {SEED ^ 0x9e3779b97f4a7c15ull * (j->id + 1), SEED + j->id, 0x1234567ull * (j->id + 3), 0xabcdefull + j->id};
  for (int i = 0; i < 20; i++) nxt(s);
  for (long g = j->id; g < G; g += NT) {
    uint32_t w0[16]; for (int i = 0; i < 15; i++) w0[i] = (uint32_t)nxt(s);
    uint32_t gb = (uint32_t)(nxt(s) & 255);
    for (long k = 0; k < KB; k++) { int nv = 0;
      for (int l = 0; l < 256; l++) {
        uint32_t w[64]; for (int i = 0; i < 15; i++) w[i] = w0[i]; w[15] = ((uint32_t)l << 24) | ((uint32_t)k << 8) | gb;
        for (int i = 16; i < R; i++) w[i] = s1(w[i-2]) + w[i-7] + s0(w[i-15]) + w[i-16];
        uint32_t a=IV[0],b=IV[1],c=IV[2],d=IV[3],e=IV[4],f=IV[5],gg=IV[6],h=IV[7];
        for (int i = 0; i < R; i++) { uint32_t t1 = h + S1(e) + CH(e,f,gg) + K[i] + w[i], t2 = S0(a) + MJ(a,b,c);
          h = gg; gg = f; f = e; e = d + t1; d = c; c = b; b = a; a = t1 + t2; }
        uint32_t cvv[8] = {a+IV[0],b+IV[1],c+IV[2],d+IV[3],e+IV[4],f+IV[5],gg+IV[6],h+IV[7]};
        uint32_t am1 = cvv[0], am2 = cvv[1];
        uint32_t W7 = c7 - am1; int p7 = (uint32_t)(s0(W7 + d7) - s0(W7)) == t7; j->trials++; j->w7 += p7;
        int ok = p7;
        if (ok && d6) { uint32_t E3 = k3 + am1, mj = (A1 & A0) | (am1 & (A1 | A0)), iv = (E5 & E4) ^ (~E5 & E3);
          uint32_t W6 = c6 - am2 + mj - iv; ok = (uint32_t)(s0(W6 + d6) - s0(W6)) == t6; }
        if (ok && R == 38) ok = e16ok(cvv);
        j->valid += ok; nv += ok; }
      j->b1 += nv >= 1; j->b2 += nv >= 2; } }
  return 0; }
int main(int argc, char **argv) {
  R = atoi(argv[1]); G = atol(argv[2]); KB = atol(argv[3]); SEED = strtoull(argv[4], 0, 10); NT = atoi(argv[5]);
  if (R == 37) { c7=0xd296fb78; d7=0xfbc00800; t7=0x017f8000; c6=0xf538a8f7; d6=0x20000000; t6=0x03c00800; k3=0x2d5dc689;
    A1=0x62827866; A0=0x1b21ce20; E5=0xe7f2c81f; E4=0x1b2d044e; }
  else { c7=0x8f6c89c5; d7=0x20000000; t7=0x03bff800; d6=0;
    SA0=0xb75dae71; SA1=0xda6c35e0; CK16=0xfe314838; M16=0x4c431a80; V16=0x48030280; }
  pthread_t th[64]; job jb[64];
  for (int i = 0; i < NT; i++) { jb[i] = (job){i, 0, 0, 0, 0, 0}; pthread_create(&th[i], 0, work, &jb[i]); }
  uint64_t T = 0, w7 = 0, v = 0, b1 = 0, b2 = 0;
  for (int i = 0; i < NT; i++) { pthread_join(th[i], 0); T += jb[i].trials; w7 += jb[i].w7; v += jb[i].valid; b1 += jb[i].b1; b2 += jb[i].b2; }
  printf("{\"R\":%d,\"groups\":%ld,\"batches_per_group\":%ld,\"seed\":%llu,\"trials\":%llu,\"w7_pass\":%llu,\"valid\":%llu,\"batches_ge1\":%llu,\"batches_ge2\":%llu}\n",
    R, G, KB, (unsigned long long)SEED, (unsigned long long)T, (unsigned long long)w7, (unsigned long long)v, (unsigned long long)b1, (unsigned long long)b2);
  return 0; }
```

<!-- file: disp.c sha256=50616c050aaf73f3857a0a8e8377f7eaea2d414900674a699492dc42dc52747f -->
```c
/* disp.c - within-group dispersion of Step-2 and stage-3a events on the attack's grouped first blocks (38 steps).
   Per group: W0..W14 and gb from a splitmix64 stream of (seed, group); trials W15 = (l << 24) | (k << 8) | gb,
   l = 0..255 lanes, k < K batches.  Counts per group: a = #(W7 in F7), b = #(W7 in F7 and the stage-3a gate
   (s0(W1)+W0+ck16) & m16 == v16 of the single element of L*), p = #batches (fixed k, 256 lanes) with >= 2 lanes
   reaching stage 3b.  Prints one line per group.
   usage: disp groups log2K seed threads   (cc -O3 -pthread) */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <pthread.h>
#define R 38
static const uint32_t K256[64] = {
0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,
0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,
0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,
0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,
0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,
0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,
0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,
0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2};
static const uint32_t IV[8] = {0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19};
#define ROR(x,n) (((x)>>(n))|((x)<<(32-(n))))
#define S0(x) (ROR(x,2)^ROR(x,13)^ROR(x,22))
#define S1(x) (ROR(x,6)^ROR(x,11)^ROR(x,25))
#define s0(x) (ROR(x,7)^ROR(x,18)^((x)>>3))
#define s1(x) (ROR(x,17)^ROR(x,19)^((x)>>10))
#define CH(e,f,g) (((e)&(f))^(~(e)&(g)))
#define MJ(a,b,c) (((a)&(b))^((a)&(c))^((b)&(c)))
static const uint32_t C7 = 0x8f6c89c5u, D7 = 0x20000000u, T7 = 0x03bff800u;
static const uint32_t SA0 = 0xb75dae71u, SA1 = 0xda6c35e0u, CK16 = 0xfe314838u, M16 = 0x4c431a80u, V16 = 0x48030280u;
static int G, LK, NT; static uint64_t SEED;
static uint64_t sm(uint64_t *s){ uint64_t z = (*s += 0x9e3779b97f4a7c15ull); z = (z ^ (z>>30)) * 0xbf58476d1ce4e5b9ull; z = (z ^ (z>>27)) * 0x94d049bb133111ebull; return z ^ (z>>31); }
/* full compression (reference path, used by the self-check) */
void compress(const uint32_t *cv, const uint32_t *M, uint32_t *out){
  uint32_t w[64], a=cv[0],b=cv[1],c=cv[2],d=cv[3],e=cv[4],f=cv[5],g=cv[6],h=cv[7];
  for(int i=0;i<16;i++) w[i]=M[i];
  for(int i=16;i<R;i++) w[i]=s1(w[i-2])+w[i-7]+s0(w[i-15])+w[i-16];
  for(int i=0;i<R;i++){ uint32_t t1=h+S1(e)+CH(e,f,g)+K256[i]+w[i], t2=S0(a)+MJ(a,b,c); h=g;g=f;f=e;e=d+t1;d=c;c=b;b=a;a=t1+t2; }
  out[0]=cv[0]+a;out[1]=cv[1]+b;out[2]=cv[2]+c;out[3]=cv[3]+d;out[4]=cv[4]+e;out[5]=cv[5]+f;out[6]=cv[6]+g;out[7]=cv[7]+h;
}
static inline int inF7(uint32_t a){ uint32_t w = C7 - a; return (uint32_t)(s0(w + D7) - s0(w)) == T7; }
/* stage-3a gate: ref_words' W0, W1 from CV1, then (s0(W1)+W0+ck16) & m16 == v16 */
static inline int e16ok(uint32_t a0, uint32_t a1, uint32_t a2, uint32_t a3, uint32_t e0, uint32_t e1, uint32_t e2, uint32_t e3){
  uint32_t E0 = SA0 + a3 - S0(a0) - MJ(a0, a1, a2);
  uint32_t E1 = SA1 + a2 - S0(SA0) - MJ(SA0, a0, a1);
  uint32_t W0 = E0 - a3 - e3 - S1(e0) - CH(e0, e1, e2) - K256[0];
  uint32_t W1 = E1 - a2 - e2 - S1(E0) - CH(E0, e0, e1) - K256[1];
  return (((s0(W1) + W0 + CK16) & M16) == V16);
}
static long long *ra, *rb, *rp; static uint32_t chk_g[3], chk_f[3]; static int chk_done;
static void *work(void *arg){
  long tid = (long)arg;
  for (int gi = tid; gi < G; gi += NT){
    uint64_t st = SEED * 0x100000001b3ull + (uint64_t)gi * 0x9e3779b97f4a7c15ull + 12345;
    uint32_t M[16]; for (int j=0;j<15;j++) M[j] = (uint32_t)(sm(&st) >> 16);
    uint32_t gb = (uint32_t)(sm(&st) & 255);
    uint32_t w[64]; for(int i=0;i<15;i++) w[i]=M[i];
    uint32_t a=IV[0],b=IV[1],c=IV[2],d=IV[3],e=IV[4],f=IV[5],g=IV[6],h=IV[7];
    for(int i=0;i<15;i++){ uint32_t t1=h+S1(e)+CH(e,f,g)+K256[i]+w[i], t2=S0(a)+MJ(a,b,c); h=g;g=f;f=e;e=d+t1;d=c;c=b;b=a;a=t1+t2; }
    long long na=0, nb=0, np=0; uint64_t K = 1ull << LK;
    for (uint64_t k = 0; k < K; k++){
      int cntb = 0;
      for (int l = 0; l < 256; l++){
        uint32_t W15 = ((uint32_t)l << 24) | ((uint32_t)k << 8) | gb;
        w[15] = W15;
        for(int i=16;i<R;i++) w[i]=s1(w[i-2])+w[i-7]+s0(w[i-15])+w[i-16];
        uint32_t A=a,B=b,Cc=c,D=d,E=e,F=f,Gg=g,H=h;
        for(int i=15;i<R;i++){ uint32_t t1=H+S1(E)+CH(E,F,Gg)+K256[i]+w[i], t2=S0(A)+MJ(A,B,Cc); H=Gg;Gg=F;F=E;E=D+t1;D=Cc;Cc=B;B=A;A=t1+t2; }
        uint32_t cv0 = IV[0]+A, cv1 = IV[1]+B, cv2 = IV[2]+Cc, cv3 = IV[3]+D;
        uint32_t cv4 = IV[4]+E, cv5 = IV[5]+F, cv6 = IV[6]+Gg, cv7 = IV[7]+H;
        if (gi == 0 && k == 5 && l == 131) { uint32_t o[8]; uint32_t MM[16]; for(int j=0;j<15;j++) MM[j]=M[j]; MM[15]=W15; compress(IV, MM, o); chk_g[0]=cv0; chk_g[1]=cv1; chk_g[2]=cv4; chk_f[0]=o[0]; chk_f[1]=o[1]; chk_f[2]=o[4]; chk_done=1; }
        if (inF7(cv0)) { na++; int ok = e16ok(cv0, cv1, cv2, cv3, cv4, cv5, cv6, cv7); if (ok) { nb++; cntb++; } }
      }
      if (cntb >= 2) np++;
    }
    ra[gi]=na; rb[gi]=nb; rp[gi]=np;
  }
  return 0;
}
int main(int argc, char **argv){
  if (argc < 5) { fprintf(stderr, "usage\n"); return 2; }
  G = atoi(argv[1]); LK = atoi(argv[2]); SEED = strtoull(argv[3],0,10); NT = atoi(argv[4]);
  /* self-check: the grouped path equals the full compression on a few trials */
  { uint64_t st = 777; uint32_t M[16]; for(int j=0;j<16;j++) M[j]=(uint32_t)(sm(&st)>>16);
    uint32_t o[8]; compress(IV, M, o); printf("# check M0=%08x.. cv=%08x %08x %08x %08x %08x %08x %08x %08x\n", M[0],o[0],o[1],o[2],o[3],o[4],o[5],o[6],o[7]); }
  ra = calloc(G, 8); rb = calloc(G, 8); rp = calloc(G, 8);
  pthread_t th[64]; for (long t=0;t<NT;t++) pthread_create(&th[t],0,work,(void*)t);
  for (int t=0;t<NT;t++) pthread_join(th[t],0);
  printf("# grouped-vs-full check %s\n", (chk_done && chk_g[0]==chk_f[0] && chk_g[1]==chk_f[1] && chk_g[2]==chk_f[2]) ? "OK" : "FAIL");
  printf("# groups %d K 2^%d trials/group %llu seed %llu\n", G, LK, 256ull << LK, (unsigned long long)SEED);
  for (int gi=0; gi<G; gi++) printf("%d %lld %lld %lld\n", gi, ra[gi], rb[gi], rp[gi]);
  return 0;
}
```

<!-- file: disp_stats.py sha256=a3c27deef1c9e349792c654ffb9254502e25654a3db2a79854216d43fe9b4628 -->
```python
# disp_stats.py - statistics of disp.c output (proof.md Section 9, H5).  usage: disp_stats.py disp.out log2K
# bs1: groups hold 256 lanes x 2^log2K batches; the b event is the stage-3b reach (W7 and the stage-3a gate,
# per-trial rate p/1024); batches with >= 2 stage-3b lanes use the binomial pair count of 256 lanes.
import sys, math
rows = [l.split() for l in open(sys.argv[1]) if not l.startswith('#')]
G = len(rows); K = 2 ** int(sys.argv[2]); m = 256 * K
p = 287309824 / 2 ** 32
ev = {'a (W7 valid)': (p, 1), 'b (stage-3b reach)': (p / 1024, 2)}
for name, (r, col) in ev.items():
    x = [int(row[col]) for row in rows]; mu = sum(x) / G; s2 = sum((v - mu) ** 2 for v in x) / (G - 1)
    e = m * r; var = m * r * (1 - r)
    z = (sum(x) - G * e) / math.sqrt(G * var)
    D = s2 / var; zD = (D - 1) / math.sqrt(2 / (G - 1))
    cbar = (s2 - var) / (m * (m - 1))           # average pairwise covariance inside a group
    se_c = var * math.sqrt(2 / (G - 1)) / (m * (m - 1))
    cond = r + cbar / r; cond_hi = r + (cbar + 3 * se_c) / r   # average Pr[A_j | A_i], +3 se
    print('%s: groups %d, trials/group %d, total %d (expected %.1f, z %+.2f); dispersion %.4f (z %+.2f); '
          'avg Pr[j|i] = %.6e vs rate %.6e (ratio %.6f, +3se ratio %.6f)' %
          (name, G, m, sum(x), G * e, z, D, zD, cond, r, cond / r, cond_hi / r))
r = p / 1024
q2 = 1 - (1 - r) ** 256 - 256 * r * (1 - r) ** 255
x = [int(row[3]) for row in rows]; e = G * K * q2; sd = math.sqrt(G * K * q2 * (1 - q2))
print('batches with >= 2 stage-3b lanes: %d (expected %.1f, z %+.2f)' % (sum(x), e, (sum(x) - e) / sd))
```

<!-- file: recount_fb.py sha256=2a86ad87ccb205cb3fc0117d79f222cc7ae50e29c09caa08030194d719566031 -->
```python
# recount_fb.py - independent recount of the organizer-visible statistic of d1-first-block-r38 (proof.md Section 9, H5).
# Uses only organizer code (seed protocol, verifier compression) and a re-implementation of the documented
# W0..W14/gb derivation and of the stage-3a gate; compares with the organizer's recorded report.
# usage: recount_fb.py <repo> <experiment-report.json> [nbatches]
import sys, json, hashlib, struct
repo, rep = sys.argv[1], sys.argv[2]
NB = int(sys.argv[3]) if len(sys.argv) > 3 else 6
sys.path.insert(0, repo)
from verifier import hash_functions as hf
from experiments.runner import _trial_seed, _canonical
d = json.load(open(rep)); ex = d.get('execution', d)
seed_material = _canonical({"domain": "hashsmash-experiments-v1", "seed": ex['seed'], "holdout_nonce": ex['holdout_nonce'],
                            "target_config_sha256": ex['target_config_sha256']})
IV = (0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19)
M32 = 0xffffffff
ror = lambda x, n: ((x >> n) | (x << (32 - n))) & M32
S0 = lambda x: ror(x, 2) ^ ror(x, 13) ^ ror(x, 22)
S1 = lambda x: ror(x, 6) ^ ror(x, 11) ^ ror(x, 25)
s0 = lambda x: ror(x, 7) ^ ror(x, 18) ^ (x >> 3)
CH = lambda e, f, g: (e & f) ^ (~e & g & M32)
MJ = lambda a, b, c: (a & b) ^ (a & c) ^ (b & c)
K0, K1 = 0x428a2f98, 0x71374491
SA0, SA1, CK16, M16, V16 = 0xb75dae71, 0xda6c35e0, 0xfe314838, 0x4c431a80, 0x48030280
w7 = lambda a: ((s0(((0x8f6c89c5 - a) + 0x20000000) & M32) - s0((0x8f6c89c5 - a) & M32)) & M32) == 0x03bff800
def reach3b(cv):
    if not w7(cv[0]): return False
    E0 = (SA0 + cv[3] - S0(cv[0]) - MJ(cv[0], cv[1], cv[2])) & M32
    E1 = (SA1 + cv[2] - S0(SA0) - MJ(SA0, cv[0], cv[1])) & M32
    W0 = (E0 - cv[3] - cv[7] - S1(cv[4]) - CH(cv[4], cv[5], cv[6]) - K0) & M32
    W1 = (E1 - cv[2] - cv[6] - S1(E0) - CH(E0, cv[4], cv[5]) - K1) & M32
    return (((s0(W1) + W0 + CK16) & M32 & M16) == V16)
e = [x for x in ex['experiments'] if x['id'] == 'd1-first-block-r38'][0]
rec = dict((t['trial'], t) for t in e['checked_trials'])
groups_with_valid = 0; nvalid = 0; match = 0; mism = 0
for i in range(256):
    seed = bytes.fromhex(_trial_seed(seed_material, 'd1-first-block-r38', i))
    r = [int.from_bytes(hashlib.shake_256(seed + bytes([c])).digest(32), 'big') for c in (1, 2)]
    M0 = [(r[0] >> (32 * j)) & M32 for j in range(8)] + [(r[1] >> (32 * j)) & M32 for j in range(7)]
    gb = (r[1] >> 224) & 255
    first = None; cnt = 0
    for kb in range(NB):
        for l in range(256):
            blk = M0 + [(l << 24) | (kb << 8) | gb]
            cv = hf._compress('sha256', IV, struct.pack('>16I', *blk), 38)
            if reach3b(cv):
                cnt += 1
                if first is None: first = blk
    nvalid += cnt; groups_with_valid += cnt > 0
    t = rec.get(i, {})
    got = t.get('message_a_hex')
    if first is None: ok = got is None
    else: ok = got is not None and bytes.fromhex(got)[:64] == struct.pack('>16I', *first)
    match += ok; mism += not ok
print(json.dumps(dict(groups=256, groups_with_valid=groups_with_valid, valid_trials=nvalid, trials=256 * 256 * NB,
                      recorded_pairs=sum(1 for t in e['checked_trials'] if t.get('message_a_hex')),
                      per_trial_match=match, per_trial_mismatch=mism)))
```

<!-- file: PREREG_q3x.txt sha256=9bf1de54863d0af07d0fa1c0edbf39e601eed1482eaf1d17ea0b518e1ed0f70a -->
```text
Organizer experiment d1-q3-smc-r38 (sha256-r38 d1 package, fix 1): design frozen 2026-10-08T21:18:40Z before any validation run and
before the organizer's public-seed request was computed or run.
Program: d1core.py sha256 ba1dd804d478999fcc6065b7ac96becee996fec1ba9809a1ce45322e16fefd11 (the first-block experiment, the attack, cert inputs and tables_digest are unchanged
from e1b12f54...; this version only adds the q3 experiment section and its dispatcher).
Parameters (d1core.Q3X): K = 20 replicates (trials 0..19), NP = 64, children per particle 128 (row 17), 4 (rows 18, 19),
1 (rows 20..22), MT = 512 tail proposals per particle; randomness: random.Random(SHAKE-256('d1-q3' || organizer seed)).
Rule: trial t < 20 returns its first rebuilt pair iff it has >= 1 tail success and every success is a verified
38-step semi-free-start collision; trial 20 returns a pair iff all 20 replicates passed and the mean of the 20
estimates is >= 2^-101.40; trials 21..255 return no pair.  Predicted: 21 returned pairs, 0 full collisions.
How the parameters were chosen: development runs of the identical estimator (q3proto.py, same random stream;
seeds 1..3 and 10001..10256, NP 64) gave a per-replicate relative sd of 0.31 and mean 2^-100.962; a bootstrap of
the mean of 20 gave the 0.0001 quantile 2^-101.342 (2^-101.374 after shifting to the preregistered SMC mean
2^-100.994); the threshold -101.40 lies below it.  K and NP were set by run time (about 3.4 s locally).
Planned runs, all reported: (1) validation: run_q3x_val.py (sha256 fbbd2dc24d9675eb4de94744395f2a292e1095678942fe87c315fa01d81ad988) on requests 0..50 (51 x 20 replicates,
own seeds 'd1-q3x-val-<r>-<t>'), 8 processes under the heavy-job lock with nice -n 10; (2) one local run of the
organizer public-seed requests of both experiments (seed protocol of experiments/runner.py, public seed
'hashsmash-public-seed-v1', no holdout nonce) to check the deterministic gate and the run time.
```

<!-- file: run_q3x_val.py sha256=fbbd2dc24d9675eb4de94744395f2a292e1095678942fe87c315fa01d81ad988 -->
```python
#!/usr/bin/env python3
# run_q3x_val.py - validation of the organizer experiment d1-q3-smc-r38 on our own seeds (proof.md Section 10.2).
# Runs d1core.q3_experiment on NREQ synthetic 256-trial requests whose trial seeds are sha256('d1-q3x-val-<r>-<t>'),
# r in [R0, R1), exactly as the organizer runner passes a request; one JSON line per request.
# usage: run_q3x_val.py R0 R1 > out.jsonl
import sys, json, hashlib, math, time
import d1core as D
R0, R1 = int(sys.argv[1]), int(sys.argv[2])
for r in range(R0, R1):
    req = dict(schema_version=1, experiment_id='d1-q3-smc-r38', target_profile='sha256-r38-prefix-v1',
               event={'kind': 'full-collision'}, max_message_bytes=4096,
               trials=[dict(trial=t, seed=hashlib.sha256(b'd1-q3x-val-%d-%d' % (r, t)).hexdigest()) for t in range(256)])
    t0 = time.time(); out = D.q3_experiment(req); dt = time.time() - t0
    tr = out['trials']; K = D.Q3X['K']
    print(json.dumps(dict(req=r, sec=round(dt, 2), returned=sum(1 for x in tr if x['message_a_hex']),
                          witness=sum(1 for x in tr[:K] if x['message_a_hex']), pooled_pass=bool(tr[K]['message_a_hex']),
                          log2=[x['observations']['log2_estimate'] for x in tr[:K]],
                          pooled=tr[K]['observations']['log2_pooled_mean'],
                          tail=sum(x['observations']['tail_successes'] for x in tr[:K]),
                          verified=sum(x['observations']['verified_pairs'] for x in tr[:K]),
                          failed=sum(x['observations']['failed_rebuilds'] for x in tr[:K]),
                          stdout_sha256=hashlib.sha256(json.dumps(out, sort_keys=True, separators=(',', ':')).encode()).hexdigest())), flush=True)
```

<!-- file: run_exp_org.py sha256=50c72ea20d16d98996a9c898e65cdc65f140fec5bee1416cba4c325e605e2852 -->
```python
#!/usr/bin/env python3
# run_exp_org.py - local emulation of the organizer requests of the d1 r38 package's experiments (bs1) with the public
# seed protocol of experiments/runner.py (seed 'hashsmash-public-seed-v1', no holdout nonce, 256 trials): builds
# the request exactly as _python_result does, runs d1core.py twice (python3 -B -s), compares stdout bytes,
# recomputes the target digest of every returned pair with the repository verifier, and summarizes.
# usage: REPO_ROOT=... run_exp_org.py OUT.json
import os, sys, json, hashlib, subprocess, time
REPO = os.environ['REPO_ROOT']; sys.path.insert(0, REPO)
from verifier.frontier_tracks import get_frontier_track
from verifier.hash_functions import digest
tr = get_frontier_track('sha256-r38-exploratory')
def canon(v): return json.dumps(v, sort_keys=True, separators=(',', ':'), ensure_ascii=True, allow_nan=False).encode()
cfg = tr.config_sha256()
sm = canon({"domain": "hashsmash-experiments-v1", "seed": "hashsmash-public-seed-v1", "holdout_nonce": None, "target_config_sha256": cfg})
res = dict(track=tr.id, profile=tr.profile_id, target_config_sha256=cfg, program_sha256=hashlib.sha256(open('d1core.py', 'rb').read()).hexdigest())
for eid in ('d1-first-block-r38', 'd1-q3-smc-r38'):
    req = {"schema_version": 1, "experiment_id": eid, "target_profile": tr.profile_id, "event": {"kind": "full-collision"},
           "max_message_bytes": 4096, "trials": [{"trial": i, "seed": hashlib.sha256(sm + canon([eid, i])).hexdigest()} for i in range(256)]}
    rq = canon(req) + b"\n"; t0 = time.time()
    o1 = subprocess.run([sys.executable, '-B', '-s', 'd1core.py'], input=rq, capture_output=True, check=True).stdout; dt = time.time() - t0
    o2 = subprocess.run([sys.executable, '-B', '-s', 'd1core.py'], input=rq, capture_output=True, check=True).stdout
    out = json.loads(o1); rows = out['trials']; ret = [r for r in rows if r['message_a_hex'] is not None]
    full = sum(1 for r in ret if r['message_a_hex'] != r['message_b_hex'] and
               digest(bytes.fromhex(r['message_a_hex']), 'sha256', 38) == digest(bytes.fromhex(r['message_b_hex']), 'sha256', 38))
    pairs = [hashlib.sha256(canon(sorted([r['message_a_hex'], r['message_b_hex']]))).hexdigest() for r in ret]
    s = dict(sec=round(dt, 2), byte_identical=o1 == o2, request_sha256=hashlib.sha256(rq).hexdigest(),
             stdout_sha256=hashlib.sha256(o1).hexdigest(), stdout_bytes=len(o1), returned=len(ret), full_collisions=full,
             repeated=len(pairs) - len(set(pairs)), max_obs=max(len(r.get('observations', {})) for r in rows))
    if eid == 'd1-first-block-r38':
        s.update(mismatches=sum(r['observations']['mismatches'] for r in rows), valid=sum(r['observations']['valid'] for r in rows),
                 w7_pass=sum(r['observations']['w7_pass'] for r in rows), lanes_checked=sum(r['observations']['lanes_checked'] for r in rows))
    else:
        K = 20; s.update(witness=sum(1 for r in rows[:K] if r['message_a_hex']), pooled_pass=rows[K]['message_a_hex'] is not None,
                         pooled_log2=rows[K]['observations']['log2_pooled_mean'], log2=[r['observations']['log2_estimate'] for r in rows[:K]],
                         tail=sum(r['observations']['tail_successes'] for r in rows[:K]), verified=sum(r['observations']['verified_pairs'] for r in rows[:K]),
                         failed=sum(r['observations']['failed_rebuilds'] for r in rows[:K]))
        # independent check of the returned semi-free-start collisions with the repository compression
        from verifier import hash_functions as hf
        sfs = 0
        for r in ret:
            a, b = bytes.fromhex(r['message_a_hex']), bytes.fromhex(r['message_b_hex'])
            cv = tuple(int.from_bytes(a[4*i:4*i+4], 'big') for i in range(8))
            if a[:32] == b[:32] and a[32:] != b[32:] and hf._compress('sha256', cv, a[32:], 38) == hf._compress('sha256', cv, b[32:], 38): sfs += 1
        s['sfs_collisions_repo_verifier'] = sfs
    res[eid] = s
open(sys.argv[1], 'w').write(json.dumps(res, indent=1)); print(json.dumps(res, indent=1))
```
