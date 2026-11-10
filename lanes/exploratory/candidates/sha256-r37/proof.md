# Collision attack on 37-step SHA-256 (ePrint 2026/1120, counted, fixed caps): 2^74.22669

**Track** sha256-r37-exploratory, target sha256-r37-prefix-v1, cost model collision-frontier-v5 (C = 2644).
**Claim** time_log2 = 74.22669 (the exact total is 2^74.226687 target compressions, rounded up at the 5th
decimal), success probability at least 0.39 (the bound is 0.393469), memory 2^20 bytes, preprocessing
2^60.00141, nonuniform advice 2^13 bytes.

**Credit.** The attack, its 37-step differential characteristic and the semi-free-start (SFS) pair are those of
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
of earlier SHA-256 filings (jaazinn and others) and the fixed-cap pattern of the r32 filing 6eeefb64 (jungjipdo); the
measured re-run of a characteristic search with the same tool by mitchuski, credited in 6eeefb64, sets the scale of
our search allowance (H4).

## 0. Summary

- **Algorithm (Section 4).** Two-block messages M0 || M1 and M0 || M1' (128 bytes each; FIPS padding appends the
  same third block).  Step 1 is the paper's dense-part solution S (rows 0..13 of both members and W8..W13), read off
  the published SFS pair.  Step 2 searches first blocks M0 until the chaining value CV1 passes the filter
  W7 in F7 and W6 in F6; this happens with probability exactly p2 = |F7| |F6| / 2^64 = 68,157,440 x 287,309,824 / 2^64 = 2^-9.87960 for a uniform CV1.  Step 3 tries every
  (W14, W15) of the exact freedom set L* (|L*| = 32) and checks every cell of rows 16..36, aborting at the first
  failing row.  A pair that passes every cell collides; it is verified with the target and output.
- **Program (Section 5).** The first block is evaluated 7 trials per 256-bit word (7 x 36-bit SWAR); a group fixes
  W0..W14 and lane l of batch k uses W15 = 2^29 l + k.  One batch (7 trials: rounds 15..36, the varying schedule
  words and the Step-2 test) costs exactly 1442 operations, 0.07791 units per trial.  The rare path and Step 3
  run on a counted scalar machine.  Every count is produced by the shipped program (Appendix A) and is
  data-independent.
- **Probability (Section 6).** p = p2 |L*| q3 kappa per first block.  p2 is exact under H1 (Lemma 2).  q3 is the
  average over L* of the probability that a valid first block's pair follows every cell of rows >= 16 and the
  paper's two-bit conditions (which only lowers it).  A sequential Monte-Carlo (SMC) estimator, unbiased for q3
  under H1, was run on 32 preregistered seeds: mean 2^-73.9916, one-sided 99% lower bound 2^-74.0074, so
  q3_model = 2^-74.01 by the preregistered rule.  kappa = 255/256 (H2 (b), Section 6.5).
  A standard-library replica of the estimator is the second organizer experiment (Section 10.2): it counts row 16
  exactly, draws W7 exactly from F7, runs 20 reduced replicates on organizer seeds with a preregistered pass rule,
  and rebuilds every success as a verified 37-step semi-free-start collision.
- **Caps and success (Section 7).** N_G = 74,789,021,673,342 groups of 2^29 batches, N = 2^77.89525 trials with
  N p_model >= 1/2 (N p_model = 0.5000000000), so Pr[success] >= 1 - e^(-1/2) - 2^-60 = 0.393469 under H1 and H2.
  All data-dependent work is capped by a global counter V <= V_MAX = 539,115,595,672,795,643,393,542 operations (halt on overflow);
  Hoeffding bounds the overflow probability by exp(-2^25.21).
- **Ledger (Section 8).** T = A_C + A_S + DEV + (pre + init + online + rare + fin_ops) / C + 6 = 29,220,711,737,171,902,226,065,981 / 1,322
  units = 2^74.226687, claimed as 74.22669.  The Step-1 SAT solve (paper: 2^41.3 compressions) is charged at
  A_S = 2^50, the authors' characteristic search and SFS-pair search (costs unpublished) at A_C = 2^60, and all our
  own development at DEV = 2^40.  The rare-path cap includes the program's own counter updates and register spills.
- **Heuristics (Section 9).** H1 uniform chaining values (score-critical), H2 the Step-3 probability and
  disjointness (score-critical), H3 packed-word pricing (score-critical, precedent), H4 the advice allowances
  (supporting).  Nothing else: no expected-work bound, no independence-of-conditions model.
- **Checks.** The selftest (Appendix A) reproduces the published pair's collision under our code and the
  repository verifier, every cell of the characteristic, the corrections, the per-row condition counts, S, L and L*,
  the exact counts, the register budgets of the batch and of the rare path, 2,100 lanes of the counted batch against the verifier, Step 3
  recovering the published pair from its chaining value, the code of the q3 replica (the row-16 count, the F7 and F6
  splits, one replicate, its semi-free-start collisions under the verifier) and the ledger.  Two organizer
  experiments (Section 10) run the shipped program on organizer seeds: the first-block check (H1, H3) and the q3
  replica (H2).

## 1. Target, cost model and output

- **Target** sha256-r37-prefix-v1: SHA-256 steps 0..36 on every padded block, the standard IV once, FIPS 180-4
  padding, feed-forward, all eight digest words (verifier `digest(m, "sha256", 37)`).  The output is two distinct
  complete messages with equal digests.
- **Cost model** collision-frontier-v5: one target compression (one R-step compression call) = 1 unit; every other
  executed 256-bit word primitive (load, store, add/sub, and/or/xor, shift, compare, branch, uniform random word)
  = 1/C unit, C = 2644.  Immediates and shift amounts are instruction fields.  We use 64 registers.  Memory is
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
- The earlier filing aa527ec0 (sha256-r32), which reused this paper, failed review.  Its public note shows two weak
  points that we avoid: (a) it priced expected work ("run to expected work") instead of a worst-case bound, and (b) it
  cited the paper's tables instead of restating the algorithm.  Here (a) every run's cost is at most T by fixed caps
  (Section 7), and (b) the tables, S, L*, every constant, the procedure and the counted program are in this file.

## 3. The characteristic

### 3.1 Notation and member orientation

Symbols are MSB first: `n` = bits (x, y) = (0, 1), `u` = (1, 0), `0`/`1` fixed and equal, `=` equal.  The paper does not
define `+`.  Every `+` sits in a vertical pair E_i[b], E_{i+1}[b], and the SFS pair satisfies E_i[b] = E_{i+1}[b] in
all of them, so we read `+` as that equality (with no member difference).  This reading only adds conditions.
In rows >= 15 the three `+` pairs are exactly three conditions that Table 16 prints (E15[4] = E16[4],
E16[24] = E17[24], E16[15] = E17[15]), which supports this reading; the counts of Section 6.4 count each once.
With member x = the message the paper prints first (M), every u/n of the table is reversed on the pair (the
selftest counts the reversed bits); with **x = the message printed second (M')** every cell holds.  We use x = M'.

### 3.2 The table (rows with a non-`=` cell; i, A_i, E_i, W_i)

```text
  4  ================================  000=============================  ================================
  5  ================================  111=0=====1==0=====01===++01====  ================================
  6  =nu=============================  uuu=1011=00=10111=0111=0++1011==  ==n=============================
  7  ==========n====n====n======n====  10n=u01001n00n00010nu110unuu0001  =====u===u==========n===========
  8  ================================  011=1n+1=n11u1101=001u1u1010=u=1  ==u=============================
  9  ================================  1=0110+=001=1100=+110100111u=0=+  =====u=u=======n===u==n=u=n=u=n=
 10  ======u===========u=============  10n001u110101==01+u1101011=1110+  ============n======u=n==========
 11  ====u=====u=========u=n====u==n=  =01un000011101=n0n0u1uu101011u1u  ================================
 12  =nu=============================  01101uuuuunu010110110n1u0u0uu0n0  ================================
 13  ====u=========u=u=======n==u====  0+10n110111unn+0n101110110001001  ================================
 14  ======u=n=======n===============  =+0=1000000111+=1==1n010u0=0101=  =0===u===n=1=1====1=u=1=====1=1=
 15  ================================  =u==01===n=011n01==u0=u=1==+====  ==u=============================
 16  ==u=============================  =0=====+00===11=+==01=0=0==+====  ================================
 17  ================================  =0=====+01===u1=+==0==1===1u====  ================================
 18  ================================  ==10===uu====0==n===111===01==1=  ================================
 19  ================================  ==1====00====1==0==========1====  ================================
 20  ================================  ==u====10=======1===00==========  ================================
 21  ================================  ==0=============================  ================================
 22  ================================  ==1=============================  =====0=nn=====1=u=1=============
 24  ================================  ================================  ==n=============================
```

### 3.3 Two-bit conditions as printed (Table 16)

```text
A15[15] != A16[15], A15[23] = A16[23], A15[25] = A16[25], A16[9] != A16[20], A16[18] != A16[6]
A16[8] = A16[17], A16[29] = A17[29], A17[29] = A18[29], E15[4] = E16[4], E17[0] != E17[13]
E16[24] = E17[24], E16[15] = E17[15], E18[6] != E18[19], E18[2] = E18[20], E20[2] != E20[16]
W6[1] = W6[12], W6[8] != W6[25], W6[14] = W6[18], W7[0] = W7[28], W7[9] = W7[30], W7[1] = W7[18]
W8[1] != W8[12], W8[8] != W8[25], W8[14] = W8[18], W22[31] != W22[1], W22[30] != W22[0]
W22[16] != W22[25], W22[14] != W22[21], W24[4] != W24[6], W24[22] = W24[31], W24[20] != W24[27]
```

On the published pair, every printed condition holds on both members except `A16[29] = A17[29]`: A16[29] carries the difference, so it holds on one member only.  The condition the characteristic needs (MAJ at step 18 must absorb the bit-29 difference) is A15[29] = A17[29], which holds on the pair and is equivalent on all of L* (A15[29] = 0 there).  Unlisted but necessary: A14[29] = A15[29] (MAJ at step 17); it depends only on (W14, W15) and holds on every element of L*.  The algorithm never uses the printed two-bit conditions: it checks the cells.  The SMC of Section 6
adds them (with the corrected readings) as extra conditions, which can only lower its estimate.

### 3.4 The SFS pair (Table 17) and its verification

```text
CV  63b4986c 35d83dc0 c98894e4 784e08fc 78a7f752 5ed877a8 315a2db3 d5614eb4
M   4d7f86ff 32ece589 d8accfc4 2cc2e433 068b5b34 eba68a28 2fe12cad 6aa26b0c
    9f0d78e1 681b8277 faa9c7e0 56aed439 cc2dbbc2 dd2ba0fc b95d377b 5dd43a81
M'  4d7f86ff 32ece589 d8accfc4 2cc2e433 068b5b34 eba68a28 0fe12cad 6ee2630c
    bf0d78e1 6d1a90dd faa1d3e0 56aed439 cc2dbbc2 dd2ba0fc bd1d3f7b 7dd43a81
hash a856d46e 4b46eb28 4935248c 92a2fc98 e0fb2610 10a9951f 54264f5b 80954580
```

F_37(CV, M) = F_37(CV, M') = the printed hash, under our code and under the repository's
`verifier/hash_functions._compress` (selftest).  Every cell of rows -4..36 holds with x = M', y = M.

## 4. The attack

### 4.1 Messages

m = M0 || M1 and m' = M0 || M1', 128 bytes each (two full blocks).  FIPS padding adds the same third block
P = 80 00 .. 00 || 00000000 00000400 to both, so the digests are F(F(F(IV, M0), M1), P) and F(F(F(IV, M0), M1'), P):
if F(CV1, M1) = F(CV1, M1') they are equal.  m != m' because M1 and M1' differ (in W6, W7 (from S), W8, W9, W10 (from S), W14, W15 (from l)).
M1 must be a full data block: in a final padded block W14 and W15 hold the length, which would remove the
(W14, W15) freedom and its differences.

### 4.2 Step 1: the solution S (published values, charged by allowance)

S is the inner part of the published pair: run F_37 from the pair's CV on x = M' and y = M and keep A0..A13,
E4..E13 and W8..W13 of both members.  These values do not depend on the CV.  (Columns: member x, member y.)

```text
A0   1b21ce20  1b21ce20
A1   62827866  62827866
A2   987f24c4  987f24c4
A3   44294b96  44294b96
A4   a8ccc9b3  a8ccc9b3
A5   a26653f8  a26653f8
A6   210c2860  410c2860
A7   7246d008  7267d818
A8   7c4a1e59  7c4a1e59
A9   edc43977  edc43977
A10  030eaaa0  010e8aa0
A11  1ae4bc99  12c4b68b
A12  2fd3ea18  4fd3ea18
A13  9992b350  919033c0
E4   1b2d044e  1b2d044e
E5   e7f2c81f  e7f2c81f
E6   eb0b9c2d  0b0b9c2d
E7   9a404eb1  b2645641
E8   7b3e8fa7  7f768aa3
E9   9a3c74f0  9a3c74e0
E10  87a8fadc  a5a8dadc
E11  b0741f5f  a875495a
E12  6fd5b358  6825b602
E13  66f25d89  6eeedd89
W8   bf0d78e1  9f0d78e1
W9   6d1a90dd  681b8277
W10  faa1d3e0  faa9c7e0
W11  56aed439  56aed439
W12  cc2dbbc2  cc2dbbc2
W13  dd2ba0fc  dd2ba0fc
```

S satisfies every cell of rows 0..13 for both members (selftest).  S is part of the published SFS pair, and we charge
its construction twice over (Section 8, H4): A_S for a Step-1 SAT solve (the paper's procedure for S), and the authors'
search for the whole SFS pair inside A_C, together with their characteristic search.

### 4.3 Step 2: the first block and the filter

For a chaining value CV1 = (A_{-1}, A_{-2}, A_{-3}, A_{-4}, E_{-1}, E_{-2}, E_{-3}, E_{-4}) the paper's Step-2
equations give the second-block words of member x that connect CV1 to S:

```text
E_i = A_i + A_{i-4} - S0(A_{i-1}) - MAJ(A_{i-1}, A_{i-2}, A_{i-3})                (i = 3, 2, 1, 0)
W_i = E_i - A_{i-4} - E_{i-4} - S1(E_{i-1}) - IF(E_{i-1}, E_{i-2}, E_{i-3}) - K_i   (i = 0..7)
```

In particular W7 = c7 - A_{-1} with c7 = d296fb78, and W6 = c6 - A_{-2} + MAJ(A1, A0, A_{-1}) - IF(E5, E4, E3),
E3 = k3 + A_{-1}, with c6 = f538a8f7, k3 = 2d5dc689.  Member y uses the same CV1 and S's y-values; rows <= 5 of S
carry no difference in either characteristic, so W'_i = W_i for i <= 5, W'_6 = W_6 + d6 and W'_7 = W_7 + d7 with
constants d6 = 20000000, d7 = fbc00800 fixed by S.  W6 and W7 carry differences (d6 = 20000000, d7 = fbc00800), so the filter has two parts: W7 in F7 and W6 in F6.

**Lemma 1 (triangular bijection).**  For fixed S the map CV1 -> (W0, ..., W7) is a bijection of (2^32)^8: W7 depends
only on A_{-1}; W6 is -A_{-2} plus a function of A_{-1}; W5 is -A_{-3} plus a function of (A_{-1}, A_{-2}); W4 is
-A_{-4} plus a function of A_{-1..-3}; W3, W2, W1, W0 are -E_{-1}, -E_{-2}, -E_{-3}, -E_{-4} plus functions of the
earlier coordinates.  With these words and S's W8..W13, F_R's steps 0..13 from CV1 reproduce S exactly (both members).
*Proof.* Substitute the equations; each step is inverted for its new coordinate.  The selftest checks the
reproduction on 2,100 chaining values.

**Lemma 2 (the second-block randomness).**  Let CV1 be uniform and condition on validity (W7 in F7 and W6 in F6, where
F_k = {w : s0(w + d_k) - s0(w) = t_k mod 2^32} with t7 = 017f8000, t6 = 03c00800).  Then (W0..W5) is uniform on
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

- |F7| = 68,157,440 and |F6| = 287,309,824 (exhaustive counts over all 2^32 words, `fcount.c`; sampled again by the
  selftest), hence p2 = |F7| |F6| / 2^64 = 68,157,440 x 287,309,824 / 2^64 = 2^-9.87960 for a uniform CV1.

### 4.4 The freedom set L* (exact)

L is the set of (W14, W15) for which, with S, rows 14 and 15 of A and E follow the cells for both members
(including the `+` pairs with rows 13/14) and the four expansion differences that depend only on (W14, W15),
s1(W'14) - s1(W14), s0(W'14) - s0(W14), s1(W'15) - s1(W15), s0(W'15) - s0(W15), equal those of the published pair.
It is enumerated exactly: E14 over its cell-consistent values (128 candidates), then E15 (524,288 candidates);
|L| = 4096.  L* keeps the elements of L whose row-16 modular differences dE16 and dA16 (functions of rows 12..15
and the W16 difference only, hence independent of M0) equal the characteristic's; no other element can ever
satisfy row 16.  |L* | = 32 (x-side W14/W15; the published one is element 13):

```text
 0:bd1d3f7b/7dd41680  1:bd1d3f7b/7dd41681  2:bd1d3f7b/7dd416a0  3:bd1d3f7b/7dd416a1
 4:bd1d3f7b/7dd41a80  5:bd1d3f7b/7dd41a81  6:bd1d3f7b/7dd41aa0  7:bd1d3f7b/7dd41aa1
 8:bd1d3f7b/7dd43680  9:bd1d3f7b/7dd43681 10:bd1d3f7b/7dd436a0 11:bd1d3f7b/7dd436a1
12:bd1d3f7b/7dd43a80 13:bd1d3f7b/7dd43a81 14:bd1d3f7b/7dd43aa0 15:bd1d3f7b/7dd43aa1
16:bd1d3f7b/fdb41680 17:bd1d3f7b/fdb41681 18:bd1d3f7b/fdb416a0 19:bd1d3f7b/fdb416a1
20:bd1d3f7b/fdb41a80 21:bd1d3f7b/fdb41a81 22:bd1d3f7b/fdb41aa0 23:bd1d3f7b/fdb41aa1
24:bd1d3f7b/fdb43680 25:bd1d3f7b/fdb43681 26:bd1d3f7b/fdb436a0 27:bd1d3f7b/fdb436a1
28:bd1d3f7b/fdb43a80 29:bd1d3f7b/fdb43a81 30:bd1d3f7b/fdb43aa0 31:bd1d3f7b/fdb43aa1
```

y side (W'14/W'15):

```text
 0:b95d377b/5dd41680  1:b95d377b/5dd41681  2:b95d377b/5dd416a0  3:b95d377b/5dd416a1
 4:b95d377b/5dd41a80  5:b95d377b/5dd41a81  6:b95d377b/5dd41aa0  7:b95d377b/5dd41aa1
 8:b95d377b/5dd43680  9:b95d377b/5dd43681 10:b95d377b/5dd436a0 11:b95d377b/5dd436a1
12:b95d377b/5dd43a80 13:b95d377b/5dd43a81 14:b95d377b/5dd43aa0 15:b95d377b/5dd43aa1
16:b95d377b/ddb41680 17:b95d377b/ddb41681 18:b95d377b/ddb416a0 19:b95d377b/ddb416a1
20:b95d377b/ddb41a80 21:b95d377b/ddb41a81 22:b95d377b/ddb41aa0 23:b95d377b/ddb41aa1
24:b95d377b/ddb43680 25:b95d377b/ddb43681 26:b95d377b/ddb436a0 27:b95d377b/ddb436a1
28:b95d377b/ddb43a80 29:b95d377b/ddb43a81 30:b95d377b/ddb43aa0 31:b95d377b/ddb43aa1
```

All 32 elements share W14 = bd1d3f7b; only W15 varies.  Exact enumeration of row 16 (Section 6.3) shows that elements 0, 2, 16 and 18 can never satisfy row 16 (they keep their place in the list; they only cost their stage-3a tests).  Every element also satisfies the W14/W15 cells (asserted).

### 4.5 Step 3 and the success event

For a valid CV1 and each l in L*, the pair (M1, M1') is (W0..W7, S's W8..W13, l) and (W'0..W'7, S's W'8..W'13, l').
**F_l** is the event that every cell of rows 16..36 (A, E, W; values, signed differences, `+` pairs) holds.

**Lemma 4.**  F_l implies F_37(CV1, M1) = F_37(CV1, M1'), hence a collision of m, m'.  *Proof.* Rows
33..36 of A and E have no u/n cell, so F_l gives equal A_i, E_i there, which with the common CV1 are the two
outputs (asserted in the program's setup).

Step 3 tests, in the order of L*: **stage 3a** - E16 = c16_l + k16_l + s0(W1) + W0 against the x-value cells and the
E15/E16 `+` pair of row 16 (10 bits, mask 40c61a90); **stage 3b** - both members' rows 16..36, one row at a time,
every cell of the row, abort at the first failing row.  Stage 3a only tests cells that F_l requires, so the early
abort never discards an element of F_l.  The first l that passes every row is verified with the target (Section 4.6).

### 4.6 The algorithm (fixed caps)

```text
input: N_G (groups), V_MAX (operations); coins: uniform 256-bit words
V = 0
for g = 0 .. N_G - 1:
    draw two random words; W0..W14 of M0 := their 15 low 32-bit fields; compute rounds 0..14 and the group
    constants (Section 5.3)
    for k = 0 .. 2^29 - 1:                                   # one batch: lanes l = 0..6, W15 = 2^29 l + k
        run the counted batch: A_{R-1}, A_{R-2} of the 7 first blocks and the W7 test
        if some lane passes W7:
            rare path (every operation counted into V, including V's updates and stage-3b spills): SWAR W6 test and lane scan
            for each passing lane: CV1 from the registers; Step 3 (stages 3a, 3b) over L*
                if some l passes every row: compute both 128-byte messages and their digests with the target
                    (6 compressions); if they are distinct and equal: output (m, m') and halt
            if V > V_MAX: halt (failure)
halt (failure)
```

Every run executes at most N_G group setups, N_G 2^29 batches, V_MAX + vmax rare-path operations and one
verification, whatever the coins (Section 8).

## 5. The counted program

### 5.1 Machine and pricing

A 256-bit word holds 7 lanes of 36 bits (bits 36 l .. 36 l + 35); the low 32 bits of a lane hold a SHA-256 word and the
top 4 bits are guard bits.  Primitives: ADD (mod 2^256), AND, OR, XOR, SHR, SHL, LOAD, STORE, compare + branch, RAND;
each executed instance costs one operation.  ROTR(x, r) = ((x >> r) AND lo_r) OR ((x << (32 - r)) AND hi_r): 5
operations with resident masks; S0, S1 = 17, s0, s1 = 14.  27 registers are resident (the lane mask M, the lane-flag
mask G, the lane increment, 20 rotation masks, 2 shift masks, the W15 lane word and the batch counter).  Every other
constant (round constants, group constants, filter constants) is LOADed at each use.  The scalar machine of the rare
path holds one 32-bit word per 256-bit word; additions are mod 2^256 and masked when needed; a rotation uses the
doubled word x | x << 32 (2 operations), so S0, S1, s0, s1 cost 8 each.  Group setup and Step 3 run on it.

### 5.2 The batch: 1442 operations per 7 trials

Rounds 15..36 of the 7 lanes, the schedule words that depend on W15 (W17, W19, W21, ..., W36; their constant
parts are folded into one LOADed group constant each, K_i included for the last words with no later use), the
specialised rounds 15..18 (their constant inputs are LOADed group constants), and the Step-2 W7 test:

```text
xm = A_{R-1} AND M;  W7 = ((xm XOR M) + c7m) AND M      (c7m = c7 - IV0 + 1, LOADed)
W7' = (W7 + d7) AND M;  z = ((s0(W7) + t7) AND M) XOR s0(W7')
y = (z + M) AND G   (bit 32 of a lane is set iff the lane fails);  branch if y != G
```

Count (from `d1core.calibrate`, identical over three groups): body and filter 1438, batch control 4 (lane-word
increment, counter increment, compare, branch), total **c_B = 1442** = load 51, add 180, and 451, or 173, xor 214, shift 367, cmp 1, branch 1.  Per trial
1442 / (7 C) = 0.07791 units = 2^-3.6820.

### 5.3 Group setup and start-up

Per group (counted on the scalar machine): two RAND, 15 words unpacked (shift + mask), rounds 0..14, W16, W18, W20,
the 32 group constants, each masked, broadcast to 7 lanes (3 SHL + 3 OR + 1 AND) and STOREd, the W15 lane word LOADed:
**c_G = 1069**, plus 4 for the group loop (zero the batch counter; add, compare and branch on the group counter).
Start-up: 51 program constants stored, plus an allowance of
256 operations for loading the 27 resident registers.

### 5.4 Rare path and Step 3 (counted on the scalar machine)

On a batch with a W7 pass the rare path runs the SWAR W6 test (62 operations, straight-line) and the lane scan (28), then Step 3 for every lane that passes both tests.  Per passing lane: c_cv = 34 (the lane's CV1 from the batch registers: 9 shifts, 8 LOADed IV words,
9 additions, 8 masks; E_{-1} = d + T1 + IV4), c01 = 71 (E0, W0, E1, W1 and q = s0(W1) + W0), per l in L* c3a =
9 (stage 3a), once per lane at the first stage-3a pass crest = 88 (E2, E3, W2..W7 and the y words), and per
stage-3b entry at most c3b = 2492 (a full pass of rows 16..36 for both members with every cell check; an
early abort costs less) plus FLAG3B = 2 for testing whether W2..W7 are computed yet.  The program maintains V itself:
each batch with a W7 pass spends VCTRL = 3 operations (V += the batch's fixed cost, compare with V_MAX, branch), each
passing lane VLANE = 1 (V += the lane's fixed cost) and each stage-3b entry VENT = 1 at its exit (V += the cost of the
executed path, a constant of that exit; the code is unrolled).  Each stage-3b entry also pays SPILL3B = 148 spill
operations: the 64 registers are STOREd at entry and LOADed back at exit (128), and W0..W7, W'6, W'7 are STOREd once
computed and LOADed again at a later entry (20).  The c-values are measured by the program on the published pair's
chaining value (which passes every row) and are data-independent except for the early abort; every operation of
this paragraph is counted into V.

### 5.5 Correctness of the counted program

- **Lane overflow.**  The counting machine carries, for every value, an upper bound on any lane (AND: min; OR/XOR:
  2^max(bit length) - 1; ADD: sum; shifts: 2^36 - 1, always followed by masks) and asserts that every ADD stays
  below 2^36, so no carry ever crosses a lane.  The bounds are structural (data-independent).  Masks whose removal
  keeps every bound were dropped (the list `SKIP` in `d1core.py`, found by `nomask_search`).  Rotations and shifts
  read only bits 0..31 of a lane, so guard-bit contents never change a result.
- **Registers.**  The counting machine records each value's definition and last use: at most 23 values are live
  at once in the batch (including the rare path's live-out registers), plus 27 resident registers = 50 <= 64.
  The rare path is traced the same way (`rare_liveness`, on the published pair's chaining value): the lane path holds
  at most 15 values (the chaining value, E0, W0, E1, W1 and q kept to the end), so with the batch's 10 live-out
  values, the 27 resident registers and V it needs 53 <= 64; stage 3b runs after the register-file save and holds
  at most 52 values, 53 <= 64 with V.  A rotation function is traced with two temporaries besides its result.
- **Bit-exactness.**  The selftest runs 300 batches (2,100 lanes) against the repository verifier: every lane's
  full CV1 (A_{R-1}, A_{R-2} directly and all eight words through the rare-path extraction), the W7 decision, for
  37 steps the W6 decision, and Lemma 1's reproduction of S.  0 mismatches.  Earlier development runs compared
  21,000 lanes per track with 0 mismatches.  The organizer experiment repeats the lane check on its own seeds.
- **Step 3 end to end.**  From the published pair's CV, the counted Step 3 derives W0..W7, finds the published
  (W14, W15) in L*, passes every row and returns exactly (M', M) (selftest).

## 6. The Step-3 probability (H2)

### 6.1 The quantity

For a valid CV1 (Lemma 2) and l in L*, let X'_l be the printed two-bit conditions on rows >= 16 (Section 3.3, with
the corrected reading A15[29] = A17[29]; the comment of `smc.py`, shared by both tracks, says "two corrected
readings": one per track).  Define q3 = (1/|L*|) sum_l Pr[F_l and X'_l | valid].  Then q3 <= (1/|L*|) sum_l
Pr[F_l | valid], and the expected number of l in L* that succeed is at least |L*| q3.  Under H1 q3 is a fixed number
determined by S, L* and the tables (Lemma 2 gives the full distribution of the second-block words).

### 6.2 The estimator (`smc.py`)

- Row 16 is computed **exactly**: for each l, E16 = c_l + W16 is uniform (W16 is fresh), so all 2^22 values of E16
  with its 10 fixed bits are enumerated and row 16 (all cells and X') is checked.  Valid E16 values per l: 0: 0, 1: 16384, 2: 0, 3: 16384, 4: 32768, 5: 8192, 6: 32768, 7: 4096, 8: 65536, 9: 49152, 10: 65536, 11: 49152, 12: 32768, 13: 57344, 14: 32768, 15: 59392, 16: 0, 17: 16384, 18: 0, 19: 16384, 20: 32768, 21: 16384, 22: 24576, 23: 12288, 24: 65536, 25: 49152, 26: 65536, 27: 49152, 28: 32768, 29: 49152, 30: 45056, 31: 55296;
  total 1,052,672, i.e. a stage factor of exactly 2^-16.9944.
- The fresh rows (rows 17..21) are sampled: E_i^x is drawn uniformly with its x-value cells, its `+` pairs
  and the E-to-E two-bit conditions imposed (an exact importance weight 2^-f), W_i^x = E_i^x - (the rest of step i),
  W_i^y = W_i^x + its exact difference (the s1/s0 differences of the previous words and the fixed differences), and
  the whole row is checked.  Lemma 2 makes these words iid uniform, so the proposal is exact.
- The tail: propose W22 with its x-value cells and the W22 two-bit conditions imposed (f bits), draw W7 uniformly from F7 and set W6 = W22 - s1(W20) - W15 - s0(W7); weight 1{W6 in F6} 2^(32-f) / |F6|; rows 22..36 are then deterministic.
- NP particles, M children per particle per stage, multinomial resampling of the survivors after every stage but
  the tail; the estimate is the product of the stage means, which is unbiased for q3: given the particles before a
  stage, the stage mean is an unbiased estimate of the particle average of that stage's conditional probability, and
  multinomial resampling keeps particle averages unbiased, so the expected product telescopes to q3 (the standard
  unbiasedness of the SMC normalising-constant estimator; Del Moral, *Feynman-Kac Formulae*, Springer 2004).
  The clumping replay (r37) rebuilds W0..W7 of every successful tail sample (inverse map of
  Lemma 2) and counts the elements of L* whose pair follows every cell for the same first block.

### 6.3 Preregistration and results

The rule (`smc_summary.py`): from the 32 per-seed estimates Z_s (linear scale), LB = mean - t sd / sqrt(32) with the
one-sided 99% Student quantile t = 2.4529 (31 degrees of freedom); q3_model = 2^(floor(100 log2 LB) / 100).  The
program hashes, parameters (NP = 4000, M = 2048, MT = 4096), seeds and rule were frozen before any listed seed was
run (`PREREG_v2.txt`, Section 12).  A first freeze (v1) was aborted after 8 seeds because 8 parallel processes used
31 GB of memory; v2 changed only memory handling and used new seeds; the 8 complete v1 values are reported in
Section 12 and agree with v2.

| quantity | value |
|---|---|
| per-seed log2 estimates (32) | -73.977 -73.926 -73.992 -74.001 -73.911 -74.037 -74.005 -73.973 -74.028 -73.978 -74.048 -73.958 -73.957 -73.951 -73.995 -73.990 -73.985 -74.040 -73.957 -74.023 -74.022 -73.929 -74.026 -74.052 -74.036 -73.995 -73.989 -74.028 -73.971 -73.987 -74.000 -73.976 |
| mean of Z_s | 2^-73.9916 |
| relative standard deviation of Z_s | 0.0252 |
| min / max | 2^-74.0520 / 2^-73.9113 |
| 99% lower bound LB | 2^-74.0074 |
| **q3_model** | **2^-74.01** |
| stage means (log2) | 16: -16.994, 17: -13.000, 18: -14.996, 19: -6.000, 20: -7.000, 21: -1.000, tail: -15.002 |
| tail hits (all seeds) | 1,094,997 |
| clumping replay | 1 l: 103,774 samples |

### 6.4 Consistency with independent counts and measurements

- The stage factors are integers within 0.01: rows fresh in one word behave like independent bit conditions.
  Their sum, 2^-73.99, compares with the paper's 75 conditions and our count of 52 + 22 = 74 one-bit plus
  two-bit conditions on rows >= 16 (Section 11).  Per row, from the printed tables (Sections 3.2 and 3.3; a reader can recount them, and the selftest does), one-bit cells (`0`, `1`, `u`, `n`) plus printed two-bit conditions, each `+` pair counted once as the two-bit condition it coincides with, are: row 16: 10 + 7 = 17, row 17: 9 + 4 = 13, row 18: 12 + 3 = 15, row 19: 6, row 20: 6 + 1 = 7, row 21: 1, rows 22..36: 8 + 7 = 15 (E22 1, W22 6 + 4, W24 1 + 3); total 74.  The SMC stage factors (Section 6.3) are 16.994, 13.000, 14.996, 6.000, 7.000, 1.000 and 15.002 bits, equal to these counts within 0.01 bit in every stage, so the estimate agrees with the standard condition-counting model applied to the paper's own tables.  The paper's probability column of Table 16 also gives 22 two-bit conditions on rows >= 16 (A16..A18: 6 + 1 + 1, E16..E20: 1 + 3 + 2 + 1, W22, W24: 4 + 3), so its tables give 74 as well; its text states 75 and we could not identify a 75th condition.  If the paper's 75 were right, q3 would be about 2^-75 and log2 T = 75.21665 (Section 8).
- The extraction harness (`hsm.c`, Section 12) measured row 16 directly on 2^36 uniform chaining values:
  all 17 row-16 conditions together pass at 2^-16.985 (95% CI [-17.01, -16.96]), against the exact 2^-16.994 of the enumeration.
- The early Step-3 conditions on real first blocks (2^30 random M0 through real 37-step compressions) pass at
  rate 1/2 each within noise (Section 12, `meas_step3_r37_M0_2e30.json`).
- **A second implementation.**  The q3 replica in `d1core.py` (standard library only, written for fix 2; the
  organizer experiment of Section 10.2) uses the same proposals and checks as `smc.py` but its own code.  Row 16:
  every row-16 word of l is E16^x plus a constant, so a bit-serial count over the 32 bits of E16^x (state: the six
  carries and the open two-bit conditions) gives, for every l, the number of E16^x that pass the whole row 16, and
  draws uniform among them (by unranking).  The counts equal `smc.py`'s enumeration for all 32 elements of L*
  (1,052,672 in total); for l = 1, 5, 15 and 31 the unranked words are exactly the enumerated sets (development) and
  for l = 7 all 4,096 draws are distinct and pass row 16 (selftest).  W7 is drawn from F7 exactly rather than by
  rejection: for a carry pattern c of w + d7, w + d7 = w ^ (d7 ^ c), which fixes the bits of w where d7 and c differ,
  and s0 is linear, so s0(w + d7) - s0(w) is the sum over j in s0(d7 ^ c) of +2^j if s0(w)_j = 0 and -2^j if it is 1;
  equality with t7 fixes s0(w)_j for j < 31 (the sign of 2^31 is irrelevant mod 2^32).  So F7 is a disjoint union of
  affine spaces, one per carry pattern: two, of 2^26 and 2^20 words, together exactly |F7| = 68,157,440 (F6 splits
  into 2^28 + 2^24 + 2^21 = 287,309,824 = |F6|), the exhaustive counts of `fcount.c`.
  Rows 17..36: 259 development replicates (NP = 64) gave a mean of 2^-73.9889; 1,020 validation replicates
  (design frozen first, own seeds, Section 10.2) gave 2^-74.0040 with a standard error of 0.0112 bit, 0.96 combined
  standard errors from the preregistered mean.  The validation sample's own one-sided 99% bound is 2^-74.0304;
  pooled with the preregistered sample by inverse-variance weights (the rule fixed in `PREREG_q3x.txt`) the
  mean is 2^-73.9947 and the 99% bound 2^-74.0077, so q3_model = 2^-74.01 stands (Section 8 lists q3 = 2^-74.04 as a
  sensitivity).  All 69,648 tail successes of the validation and 17,946 of development were rebuilt as 37-step
  semi-free-start collisions (CV1 by inverting steps 7..0 from S, then the reference compression of both
  blocks): none failed.

### 6.5 Disjointness across L*

For every successful tail sample of the three replay seeds (1 l: 103,774 samples; the samples of one seed share ancestors), rebuilding W0..W7 and checking all 32 elements of L* gave exactly one element following every cell.  So distinct l succeed disjointly in every observed case.  H2 (b) takes Pr[some l succeeds] >= (255/256) E[number of successful l]; the factor 255/256 costs 0.0056 bit and covers an overlap rate up to 2^-8, which the replay (0 overlaps) makes implausible.  The early-row correlation between elements of L* (they share W16) is irrelevant to this: it is part of q3 through the exact joint distribution.

## 7. Success probability and caps

- Per trial, under H1 and H2: Pr[success] >= p_model = p2 |L*| q3_model kappa = 2^-78.89525 (p2 = 2^-9.87960, |L*| =
  32, q3_model = 2^-74.01, kappa = 255/256 (H2 (b), Section 6.5)).  The algorithm finds every success of a trial (stage 3a never discards an
  element of F_l; stage 3b checks exactly F_l; F_l implies a collision, Lemma 4).
- **Trial cap.**  N_G = ceil(1/2 / (7 2^29 p_model)) = 74,789,021,673,342, N_B = 2^29 N_G = 40,152,050,273,354,885,627,904 batches, N = 7 N_B = 2^77.89525
  trials, N p_model = 0.5000000000 >= 1/2.  Under H1 the trials are independent, so Pr[some trial succeeds] >=
  1 - (1 - p_model)^N >= 1 - e^(-1/2) = 0.393469.
- **Work cap.**  The rare-path operations of a batch, v_b, are at most vmax = 595,499 (vmax = w6 + scan + 3 + 7 (c_cv + c01 + 1 + crest + 32 (c3a + c3b + 2 + 149))) and have
  expectation at most vbar = 13.4138 under H1 (vbar = P7any (w6 + scan + 3) + 7 p2 (c_cv + c01 + 1 + 32 c3a + min(1, 32 2^-10) crest + 32 2^-10 (c3b + 2 + 149)), P7any = 1 - (1 - |F7| 2^-32)^7; stage 3a passes with probability exactly 2^-10 because
  E16 is uniform; the stage-3b cost is bounded by its full pass).  V_MAX = ceil((1 + 2^-10) N_B vbar) = 539,115,595,672,795,643,393,542.
  The v_b of distinct batches are independent under H1, so Hoeffding gives Pr[sum v_b > V_MAX] <=
  exp(-2 (2^-10 N_B vbar)^2 / (N_B vmax^2)) = exp(-2^25.21).
- **Success.**  If the full run would not exceed V_MAX, all N trials are tested.  Hence Pr[output a collision] >=
  0.393469 - exp(-2^25.21) - 2^-60 > 0.39 (the 2^-60 also covers a repeated first block, which needs a 480-bit
  repeat of two random words).  Any output is a verified collision (Section 4.6), independently of the heuristics.

## 8. Ledger (exact; `cert.py`)

```text
T = A_C + A_S + DEV + (pre + init + online + rare + fin_ops) / C + fin_units
  A_C = 2^60 (characteristic and SFS-pair search), A_S = 2^50 (Step-1 solve), DEV = 2^40 (our computation)  [units]
  pre    = (E14 + E15 candidates) x 1024 + 2^20 = 538,050,560              (L, L* enumeration and tables)
  init   = c_init + 256 = 307
  online = N_G (c_G + 4) + N_B c_B = 57,899,256,574,426,365,330,933,534
  rare   = V_MAX + vmax = 539,115,595,672,795,643,989,041
  fin    = 6 units + 512 operations (two complete messages, their digests, once)
T = 29,220,711,737,171,902,226,065,981 / 1,322 units = 2^74.226687  ->  time_log2 = 74.22669 (rounded up at the 5th decimal)
preprocessing = A_C + A_S + DEV + pre / C = 2^60.00141
```

The online term is 2^74.2132 units, the rare term 2^67.4664; everything else is below 2^60.01.  The total
holds on every run: the program cannot execute more groups, batches, rare-path operations or verifications.

**Sensitivity** (`cert.ledger` with one input changed; log2 T):

| change | log2 T |
|---|---|
| q3 lower by 0.25 bit | 74.47668 |
| q3 lower by 0.50 bit | 74.72667 |
| q3 lower by 1.00 bit | 75.22665 |
| q3 = 2^-74.04 (the replica validation's 99% bound, rounded down) | 74.25669 |
| q3 = 2^-74.35 (the pooled threshold of the organizer replica) | 74.56667 |
| A_C = 2^56 | 74.22662 |
| A_C = 2^64 | 74.22782 |
| A_C = 2^68 | 74.24575 |
| q3 = 2^-75 (the paper's condition count) | 75.21665 |
| no packed pricing (each first block = 1 unit, filter at its SWAR share) | about 77.90 |

## 9. Heuristics

**H1 - uniform chaining values (score-critical).**  For the attack's first blocks (W0..W14 from uniform random words
per group, W15 = 2^29 l + k per lane), the chaining values CV1 = F_37(IV, M0) of distinct trials behave as
independent uniform 256-bit values.  Used for: p2 (exact under H1), the distribution of the second-block words
(Lemma 2), the independence of trials (success bound) and of batches (Hoeffding).  Run selection is part of this
premise: no program, parameter or seed was chosen after seeing an organizer-seed outcome.  The first-block
experiment's design and prediction were fixed by the d1 build, which ran it on 256 seeds of its own and on 256
review seeds; its only run on organizer seeds, a local emulation of the public-seed request (Section 10.1), came after
the fix-2 design freeze and returned 21 pairs, inside the expected range.  Evidence: (i) local, the
attack's own grouped family (`grouprate.c`, 939,524,096 = 2^29.81 trials, every one a full 37-step compression):
W7 passes 14,910,541 (expected 14,909,440, z = +0.29); valid lanes 997,084 (expected 997,360, z = -0.28; rate 2^-9.88000 against the exact 2^-9.87960); batches with >= 1 valid lane 993,991 (expected 994,189, z = -0.20); batches with >= 2 valid lanes
3,092 (expected 3,165, z = -1.30); (ii) the extraction harness's 2^30 random first blocks and 2^35..2^36 uniform CVs (cell semantics, Section 12);
(iii) the organizer experiment (Section 10.1).  Limitations: a premise, not a theorem; tested on about 2^30 trials,
not on 2^77.9; W15 is the only varying word (22..23 rounds follow it).

**H2 - Step-3 probability and disjointness (score-critical).**  (a) q3 >= q3_model = 2^-74.01; (b) for a valid first block, Pr[some l in L* succeeds] >= (255/256) x the expected number of successful l.
(c) No run selection: every run of the preregistered estimator and of the replica is reported (Section 12).
Evidence: Section 6 (unbiased estimator under H1, preregistered 32-seed sample with a one-sided 99% bound, exact row
16; every stage factor equals, within 0.01 bit, the condition count of its rows read off the printed tables, so the
estimate also agrees with the standard condition-counting model applied to the paper's own tables; a direct
measurement of row 16; the replay) and a second, standard-library implementation that the organizer runs on its own
seeds with a preregistered pass rule (Section 10.2; validated on 1,020 replicates of our own; every success it finds
is a verified semi-free-start collision).  The organizer run can confirm q3 only to within its pooled threshold
2^-74.35; the step from there to q3_model rests on our preregistered sample (sensitivity: q3 = 2^-74.35 gives
log2 T = 74.56667).  Limitations: a
Monte-Carlo bound (heavy tails would make the sample mean low rather than high, which errs on the conservative
side, but this is not proven); depends on H1; the `+` reading.

**H3 - packed-word pricing (score-critical; precedent).**  A word-RAM program that evaluates 7 first blocks in 7 x 36-bit
lanes of 256-bit words is charged by its counted primitives (1442 per 7 trials).  Precedent: the same packing was
rated plausible in sha256-r31 (H7) and blake3-r2 filings.  Without it each first block costs one unit: about 77.90.

**H4 - advice allowances (supporting).**  The published characteristic and the SFS pair's inner values S are used as
advice.  Their construction is charged at fixed allowances: A_S = 2^50 for a Step-1 SAT solve (the paper reports
2^41.3 compression-equivalents), and A_C = 2^60 for the authors' characteristic search together with their search for
the SFS pair (costs not published).  At 2^21.7 units per CPU-second (a core retiring about 10^10 primitive operations
per second at C of about 2,700; the dynamic CryptoMiniSat profile credited in the accepted sha256-r32 filing 6eeefb64
gives 2^21.68 at C = 2224, hence fewer units at our larger C), 2^60 units is 2^38.3 CPU-seconds, about 11,000
CPU-years.  For comparison, a complete re-run of the same tool's characteristic search for the 35-step [LLWS26]
characteristic was measured at 593,858 CPU-seconds (mitchuski, credited in 6eeefb64); A_C is more than 500,000 times
that.  DEV = 2^40 covers about 330,000 CPU-seconds; all our development, including the other workers' extraction and
design runs, the review runs and fix 2 (Section 12), is about 5,900 CPU-seconds.  If a reviewer charges more:
A_C = 2^64 gives 74.22782, 2^68 gives 74.24575 (log2 T); with the earlier allowance A_C = 2^56 it would be 74.22662.

Not used: expected work, an independence-of-conditions model (replaced by the SMC), a random-oracle model, any
premise on the published pair beyond its verified values.

## 10. Organizer experiments

`experiments/d1core.py` is byte-identical to Appendix A's `d1core.py` (SHA-256 68350927da786f13a7b767140dd2d7d4aa57ace82a59b3846d545232a3fd35d9).  Both experiments
run it; it dispatches on the request's experiment id.

### 10.1 d1-first-block-r37 (H1, H3)

Per organizer seed it runs one group of the attack driver (`attack`, the same code) with W0..W14 from SHAKE-256(seed), 16
batches = 112 trials.  A hook checks every lane against the scalar compression (all 8 CV1 words, the W7 decision,
for 37 steps the W6 decision), that the valid lanes are exactly those the driver sends to Step 3, and that for every
valid lane and every l in L* the pair follows every A/E cell of rows -4..15 and every W cell except W6/W7's XOR
cells (Lemma 3).  It returns the 128-byte pair (M0 || M1, M0 || M1') of the first valid lane with the published l if
every check passed, else two nulls.  Event: full collision (none is expected; Pr < 2^-60).

Prediction under H1: a trial returns a pair with probability 1 - (1 - p2)^112 = 0.1122, so about 28.7 of 256
are expected; the count is a witness observation, not a statistical test; mismatches 0 in every trial (observations).
A local run on our own 256 seeds returned 33 pairs, 0 mismatches, in 3.92 s (stdout db276eec).  A second
local run, on the 256 seeds of this version's review (SHA-256 of `review-<i>`), returned 29 pairs, 0 mismatches
(stdout c209c2ab).  Both outputs were reproduced byte for byte by a second execution, and under Python 3.9 and
3.12, and are unchanged under the fix-2 program.  A local emulation of the organizer's public-seed request (seed
protocol of `experiments/runner.py`, seed `hashsmash-public-seed-v1`, no holdout nonce; `run_exp_org.py`, run after
the fix-2 design freeze) returned 21 pairs, 0 mismatches, 21 valid lanes, byte-identical on two runs
and under Python 3.9 and 3.12 (stdout 43755366), 3.8 s (2.9 s under 3.12), peak RSS below 31 MB.
These three are the only runs of the experiment.  A holdout nonce changes the seeds and the count.

### 10.2 d1-q3-smc-r37 (H2)

The organizer runs the replica of Section 6.4 (`q3_experiment` in `d1core.py`) on its own seeds.  Row 16 is counted
exactly in every run (1,052,672 words over the 32 elements of L*, reported as row16_words), and F7 is split into its
affine spaces (their sizes are asserted to sum to |F7|).  Trials 0..19 each run one replicate of the estimator of
Section 6.2 (NP = 64 particles drawn uniformly from the row-16 words, 4 children per particle at rows 17 and 18, 1 at
rows 19..21, 512 tail proposals per particle with W7 drawn exactly from F7; randomness from SHAKE-256 of the trial's
seed).  Every tail success is rebuilt: W0..W7 by the inverse expansion (Lemma 2), CV1 by inverting steps 7..0 from S,
and the pair is accepted only if F_37(CV1, M1) = F_37(CV1, M1') under the reference compression, M1 != M1', the
paper's Step-2 equations map CV1 back to W0..W7, W7 is in F7, W6 is in F6 and every cell of rows -4..36 holds
except the XOR cells of W6 and W7.  Trial t < 20 returns its first rebuilt pair as the 96-byte strings CV1 || M1 and
CV1 || M1' iff it has a tail success and every success was accepted.  Trial 20 returns a pair iff all 20 trials did
and the mean of their 20 estimates is at least 2^-74.35.  Trials 21..255 return no pair by design.  The organizer's
target digest of these strings is not expected to collide (they are semi-free-start collisions from CV1, not
collisions from the IV), so the checked event has 0 successes; the organizer-visible statistic is the number of
returned pairs, predicted 21, and anyone can verify the semi-free-start collisions in the raw report.

The design was frozen (`PREREG_q3x.txt`, program 68350927) before any validation run and before the public-seed
request was computed.  The parameters mirror d1-q3-smc-r38 (rows 17..21 of r37 have the stage factors of rows 18..22
of r38; r37's 2^-17 row is row 16, which is exact here).  The threshold came from 259 development replicates
(relative sd 0.246): a bootstrap of the mean of 20 put its 0.0001 quantile 0.314 bit below the mean, at
2^-74.306 after shifting to the preregistered mean 2^-73.9916, and the threshold is that value rounded down to a
multiple of 0.05 bit.  Validation (`run_q3x_val.py`, 51 requests of 256 trials on our own seeds, 1,020 replicates):
every request returned exactly 21 pairs; the 51 pooled means lay in [2^-74.222, 2^-73.833]; 69,648 tail
successes, all accepted.  The public-seed emulation (`run_exp_org.py`) returned 21 pairs, pooled mean
2^-73.902, 1,386 tail successes all accepted, the 21 returned strings are semi-free-start collisions under
the repository's `_compress` as well, byte-identical on two runs and under Python 3.9 and 3.12 (stdout
0ecd1cbc), 3.5 s (2.5 s under 3.12; run time limit 20 s), peak RSS below 31 MB (limit 128 MB).  The
program is 65,424 bytes (source limit 65,536).

What this tests: an organizer-executed, unbiased estimate of q3 under the exact distribution of Lemma 2, with a
pass rule that a true q3 of 2^-74.35 would fail about half the time, of 2^-74.50 97% of the time and of
2^-74.60 more than 99.9% of the time, while q3 = q3_model = 2^-74.01 fails it with probability
about 2 x 10^-5 (bootstrap of the validation replicates, rescaled); and that the success event the estimator counts
produces genuine semi-free-start collisions.
What it does not test: H1 itself (it samples the second-block words from Lemma 2's distribution), and q3 more
finely than its threshold.

## 11. Differences from the paper

1. Member orientation: the tables hold with x = M' (Section 3.1).  `+` is undefined; read as E_i[b] = E_{i+1}[b].
2. Step 2: the paper counts W6 as 3 conditions and reports 2^-9; its own cells give W6 four (W6[29] = 0 is necessary) and the cell semantics gives exactly 2^-10 (2^-10.0007 measured on 2^30 real first blocks).  The exact requirement (Lemma 3) gives 2^-9.8796, which we use.
3. Table 16: `A16[29] = A17[29]` holds on one member only; the needed condition is A15[29] = A17[29].  Unlisted but necessary: A14[29] = A15[29] (inside L*).
4. (W14, W15) freedom 2^5 as in the paper (|L| = 4,096, |L*| = 32); four of the 32 can never pass row 16.
5. Condition counts on rows >= 16: ours 52 + 22 = 74 (one-bit + listed two-bit), paper 75.  We do not use counts:
   the SMC gives 2^-73.99.  The paper's own Table 16 probability column also gives 22 two-bit conditions on these rows (Section 6.4).
6. The paper's totals are expected work with independence-of-conditions; ours is a worst-case bound with caps.

## 12. Runs and hashes

All runs on one Apple-silicon Mac; CPU = user seconds.  Heavy runs held the shared lock and ran under `nice -n 10`.

| run | what | CPU | hashes / outputs |
|---|---|---:|---|
| extraction (other worker, 2026-10-08) | table OCR, `verify_sfs.py`, `hsm37/38 S`, `enum_S_py.py`, `validate.py`, `step2_equiv.py` (light) | about 70 | EXTRACT.md Section 11; summary.json ed648926 |
| extraction heavy (lock) | `hsm37 step3 30` (2^30 random M0), `hsm38 step3 30`, `hsm37 step3 36 direct` (2^36 CVs), `hsm38 step3 35 direct` | 2,121 | outputs 9ae6a612, 0dde492c, 79376572, 84bf58e1 (meas_step3_*.json) |
| design (other worker) | `p2exact.py` (exhaustive F counts, numpy, 72 s, no lock: disclosed), `enumL.py`, `lstar.py`, `fwdsim.py`, `smc.py`/`smc2.py`/`smc3.py` (earlier SMC versions), `clump.py`, `a0family.py`, `proto_v1.py`, `proj.py` | about 350 | DESIGN.md Section 13 (p2exact fce3f4d1, smc3 4bc9f2fe, clump 1fa7ea3a) |
| this build: program development | `d1core.py` lane tests (2 x 21,000 lanes, 0 mismatches), calibration, mask search, Step-3 end-to-end, L enumeration | about 60 | dev/t_batch.py |
| this build: `fcount.c` | exhaustive sizes of F7, F6 (3 sets, 2^32 words each) | 7 | runs/fcount.out 539a4288 |
| this build: SMC development | seeds 101, 102, 103r, 9, 77, 78r and small tests (not in the sample) | about 150 | - |
| this build: SMC v1 (lock; aborted) | frozen 20:22:03Z (PREREG.txt 9a2c39ef); 16 started, 8 complete: r37 seeds 1001..1008 = -73.954, -73.971, -74.033, -74.016, -74.040, -74.041, -73.982, -74.064 (replay 103,412 samples, all exactly 1 l); stopped at 31 GB RSS | about 470 | v1_aborted/LOG.txt bcf772c3, smc_v1.py b932a271 |
| this build: SMC v2 (lock) | frozen 20:25:28Z (PREREG_v2.txt 7613bbfe); 32 + 32 seeds, every one used | 1,401 | LOG.txt 7394640a; summary_r37 6acea59a, summary_r38 df211d69 |
| this build: `grouprate.c` (lock) | H1 evidence, 2^29.81 grouped trials per track | 175 | grouprate.log 04609f26; r37 fb2e15fb, r38 037a1b11 |
| this build: selftest, cert, collection, local experiment | selftest r37/r38 (full), cert, collect.py, run_exp_local.py (256 own seeds; r37 stdout db276eec, r38 1631cbcb) | about 200 | runs/exp_local_r*.json |
| review of this version (r37) | extraction + selftest r37 full (several), experiment profile (Python 3.9 / 3.12, 3.0 to 4.0 s, peak RSS below 30 MB), run_exp_review.py (256 review seeds: 29 pairs, stdout c209c2ab), run_exp_local.py re-run with the final program (stdout db276eec again), `rare_liveness`, cert, collect.py, local_tracks check | about 120 | runs/exp_review_r37.json, runs/exp_local_r37.json |
| fix 2: q3 replica development | `dev/q3sec37.py` and `dev/build_d1core.py` (the replica section and its insertion into 0126e311); the row-16 count against `smc.py`'s enumeration (all 32 l; unranking equal to the enumerated sets for l = 1, 5, 15, 31), the F7 and F6 splits and 20,000 F7 draws, seeds 1..3, timing; `dev/q3dev.py` on seeds 1..3 and 10001..10256 (259 replicates, NP 64, 8 processes, lock, 22:02:31Z-22:02:38Z); one request on development seeds (`dev/e2e_dev.py`, Python 3.9 and 3.12: identical output, 21 pairs) and the first-block experiment on the d1 build's 256 seeds (stdout db276eec, unchanged) | about 110 | dev/q3dev.py 8181953f, runs/q3dev/dev_all.jsonl f223d698 (program f3309922: the frozen program with POOL_LOG2 = -74.40) |
| fix 2: freeze | `PREREG_q3x.txt` e8e6825b (program 68350927, `run_q3x_val.py` fb90caa8, `run_exp_org.py` 2b58b113), 22:05:55Z | - | - |
| fix 2: validation (lock) | `run_q3x_val.py` 0..50 in 8 processes, 22:06:04Z-22:06:32Z: 51 x 21 returned pairs, 1,020 replicates, 69,648 tail successes all accepted; `val_summary.py` (the pooling rule of the freeze) | 203 | q3x/val_all.jsonl 4a4748db, val_summary.json 30c08db3, LOG.txt a7e5e710 |
| fix 2: organizer public-seed emulation | `run_exp_org.py` (both experiments, each run twice) under Python 3.9.6 and 3.12.14, and `/usr/bin/time` on each request: 21 and 21 returned pairs; stdout 43755366 and 0ecd1cbc under both versions; at most 3.8 s and 31 MB | about 45 | q3x/org_emulation.json 26cb44a5, q3x/org_emulation_py312.json 1a7ce9c1 |
| fix 2: checks | reproduction of the previous package by its pipeline, selftest 37 (also full, on the extracted Appendix A), collect.py (ledger unchanged), cert, assembly, local_tracks check | about 120 | gen/data_r37.json 525bb6b7 |
| sha256-r38 package, its fix 1 | the r38 q3 replica: development, validation, emulation, checks (listed in that package's Section 12) | about 400 | - |

Development total: about 5,900 CPU-seconds, far inside DEV = 2^40 units.  No run was discarded; the aborted
SMC v1 is reported above.

After the SMC freeze, `d1core.py` changed twice, in accounting code only.  (1) First build: the attack driver adds
VCTRL = 3 operations per batch with a W7 pass to V (the update of V and its cap test), GCTRL = 4 per group is defined
for `cert.py`, and Step 3 counts FLAG3B = 2 at each stage-3b entry (SHA-256 of that version
e1b12f5440c65231c3ff3043568206a3a3fadca664a42ac8c7b52966fe61b5de).  (2) This version: VLANE = 1 per passing lane and
V3B = VENT + SPILL3B = 1 + 148 per stage-3b entry are counted into V (Section 5.4), the liveness trace `ScLive` /
`rare_liveness` is added and reported by `calibrate`, and Step 3 keeps references to E0, W0, E1, W1, q and W0..W7 on
its machine object for that trace (no operation, no change to any computed value).  The frozen version had SHA-256
33c84afc151862c8dbb2f519af7bf900ba7c72d31b9b4182372da25e3fb9f641 (the hash in `PREREG_v2.txt`); the data the SMC
reads is unchanged (`tables_digest` a85c62555c8e3c5712fc82c1e1525272bbdb2fe16635e73058a60b03beeb0da9, printed by the selftest and equal to the value recorded in
`PREREG_v2.txt`), and `smc.py` uses none of the changed functions.  The SMC itself (`smc.py`) is byte-identical to the
frozen file.

Fix 2 (after an internal review of this package, which found that H2 had no organizer-run evidence) changed
`d1core.py` again (0126e311 -> 68350927) by adding only the q3 replica (Section 10.2), the dispatch of `__main__`
on the experiment id, the imports it needs and two lines of the header comment; the attack, the counted program and
every count are unchanged (`calibrate` gives the same counts, `tables_digest` is unchanged, `cert.py` gives the same
ledger, and the first-block experiment's output on the d1 build's 256 local seeds is byte-identical, stdout
db276eec).  `selftest.py` gained check 8 (the q3 replica); `cert.py` is unchanged.

## 13. Memory and advice

The attack holds the program constants (< 100 words), the group table (32 words), S, L* and the row masks (< 400
words) and its registers: below 2^16 bytes even at 32 bytes per word.  The preprocessing enumeration streams its
candidates and keeps L (4096 entries).  We claim memory 2^20 bytes.  The nonuniform advice is the characteristic and
S (the `CH`, `PAIRS`, `LSTAR` tables of `d1core.py`, below 2^13 bytes), charged as A_C + A_S.

## Appendix A. Program files

These files are the program and the evidence scripts of this package exactly as run (Python 3.9+ standard library
except `smc.py`, which needs numpy; `fcount.c` and `grouprate.c` are C99).  Each block below is one file; its
SHA-256 is in the marker line.

- `d1core.py` (65424 bytes): the counted program: reduced SHA-256, characteristic, SFS pair, S, L/L*, machines, batch, group setup, rare path, Step 3, verification, the attack driver with caps, calibration, the q3 replica, and the entry point of both organizer experiments (byte-identical to experiments/d1core.py).
- `cert.py` (4675 bytes): the exact ledger (Section 8).
- `selftest.py` (9912 bytes): the self-test (A.0, A.1).
- `smc.py` (13742 bytes): the SMC estimator of q3 (Section 6; needs numpy; local evidence).
- `smc_summary.py` (1653 bytes): the preregistered decision rule (Section 6.3).
- `run_smc.sh` (1211 bytes): the preregistered runner (lock, nice, logs).
- `SEEDS_37.txt` (163 bytes): the preregistered seeds of this track.
- `PREREG_v2.txt` (1907 bytes): the preregistration record (hashes frozen before the runs).
- `fcount.c` (762 bytes): exhaustive sizes of the Step-2 sets (Section 4.3).
- `grouprate.c` (4638 bytes): the H1 measurement on the grouped first blocks (Section 9).
- `PREREG_q3x.txt` (4716 bytes): the design freeze of the q3 organizer experiment (Section 10.2).
- `run_q3x_val.py` (1723 bytes): the validation of the q3 organizer experiment (Section 10.2).
- `run_exp_org.py` (4044 bytes): the local emulation of the organizer public-seed requests (Section 10).

Together 114570 bytes.

### A.0 Extraction and self-test

From the repository root (about 20 s; `full` re-enumerates L and L*; the self-test reads
`verifier/hash_functions.py` under REPO_ROOT):

```sh
mkdir -p /tmp/d1 && python3 - <<'EOF'
import hashlib, re
C = "lanes/exploratory/candidates/sha256-r37/"
t = open(C + "proof.md").read()
n = 0
for name, sha, body in re.findall(r"<!-- file: (\S+) sha256=(\w+) -->\n```\w*\n(.*?)```\n", t, re.S):
    assert hashlib.sha256(body.encode()).hexdigest() == sha, name
    open("/tmp/d1/" + name, "w").write(body)
    n += 1
assert n == 13
assert open(C + "experiments/d1core.py").read() == open("/tmp/d1/d1core.py").read()
EOF
cd /tmp/d1 && REPO_ROOT="$OLDPWD" python3 selftest.py 37 full
```

### A.1 Self-test output of our run

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
 "un_bits_reversed_if_x_is_M": 113,
 "plus_all_paired": 20,
 "plus_pairs_equal": 10,
 "printed_two_bit_failing_(x,y)": [
  [
   "A16[29]=A17[29]",
   [
    false,
    true
   ]
  ]
 ],
 "printed_two_bit_failures_as_stated": true,
 "plus_pairs_are_printed_conditions": 3,
 "condition_counts_rows_ge16": {
  "16": 17,
  "17": 13,
  "18": 15,
  "19": 6,
  "20": 7,
  "21": 1,
  "tail": 15,
  "total": 74
 },
 "condition_counts_as_stated": true,
 "S_W8_13_x": "bf0d78e1 6d1a90dd faa1d3e0 56aed439 cc2dbbc2 dd2ba0fc",
 "Lstar_size": 32,
 "constants": {
  "c7": "d296fb78",
  "d7": "fbc00800",
  "t7": "017f8000",
  "c6": "f538a8f7",
  "d6": "20000000",
  "t6": "03c00800",
  "k3": "2d5dc689"
 },
 "L_and_Lstar_sizes": [
  4096,
  32,
  128,
  524288
 ],
 "tables_digest": "a85c62555c8e3c5712fc82c1e1525272bbdb2fe16635e73058a60b03beeb0da9",
 "F7_sampled": [
  16721,
  16640.0
 ],
 "F6_sampled": [
  70005,
  70144.0
 ],
 "counts": {
  "c_init": 51,
  "c_G": 1069,
  "groupconsts": 32,
  "c_B": 1442,
  "body_filter": 1438,
  "cats": {
   "rand": 0,
   "load": 51,
   "store": 0,
   "add": 180,
   "and": 451,
   "or": 173,
   "xor": 214,
   "shift": 367,
   "cmp": 1,
   "branch": 1
  },
  "w6": 62,
  "scan": 28,
  "maxlive": 23,
  "resident": 27,
  "c_cv": 34,
  "c01": 71,
  "c3a": 9,
  "crest": 88,
  "c3b": 2492,
  "live_lane": 15,
  "live_3b": 52
 },
 "register_budget": 50,
 "rare_register_budget": [
  53,
  53
 ],
 "batch_bit_exact": {
  "lanes": 2100,
  "mismatches": 0,
  "w7_pass": 32
 },
 "step3_reproduces_published_pair": [
  13,
  1
 ],
 "q3x_row16_counts": 1052672,
 "q3x_row16_l7_draws": [
  4096,
  0
 ],
 "q3x_F7_affine_parts": [
  [
   26,
   20
  ],
  68157440
 ],
 "q3x_F6_affine_parts": [
  [
   28,
   24,
   21
  ],
  287309824
 ],
 "q3x_replicate_seed1": [
  -74.330856,
  56,
  0
 ],
 "q3x_pairs_sfs_repo_verifier": 56,
 "ledger": {
  "log2_p_model": -78.89524666715229,
  "NG": 74789021673342,
  "log2_N": 77.89524666715232,
  "N_times_p": 0.5000000000000058,
  "vbar": 13.413751615951822,
  "VMAX": 539115595672795643393542,
  "log2_T": 74.22668722937846,
  "time_log2": 74.22669,
  "preprocessing_log2": 60.00141,
  "success_lower_bound": 0.39346934028737013,
  "log2_hoeffding_exponent": 25.211694400855443
 },
 "success_at_least_0.39": true
}
selftest r37: all checks passed
```

The output is deterministic (no timings).  `cert.py 37` prints the full ledger (Section 8).

### A.2 Source files

<!-- file: d1core.py sha256=68350927da786f13a7b767140dd2d7d4aa57ace82a59b3846d545232a3fd35d9 -->
```python
#!/usr/bin/env python3
# d1core.py - counted program of the d1 packages (sha256-r37-prefix-v1 / sha256-r38-prefix-v1).
# The two-block collision attack of Li, Zhang, Li, Liu, Qian and Zhu, "Pushing Collision Attacks on SHA-2 to
# 39 Steps", IACR ePrint 2026/1120 (CC BY), in the memory-efficient framework of [LLWS26] (Li, Liu, Wang, Shi,
# CRYPTO 2026), with their characteristics (Tables 15 / 3) and SFS pairs (Tables 17 / 5).  This file holds:
# the reduced SHA-256 (scalar reference), the characteristic cells, the SFS pairs, the Step-1 solution S read
# off the SFS pair, the exact freedom set L*, the counted 7x36 SWAR first-block batch with its Step-2 filter,
# the counted rare path, the counted scalar Step 3 (early abort), the target verification, the attack driver
# with fixed caps, and the entry point of the two organizer experiments (stdin JSON -> stdout JSON): the
# first-block check and, for 37 steps, a reduced standard-library replica of smc.py.  Python 3.9+, stdlib.
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

# ---------------------------------------------------------------------------------------------------------
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

# ---------------------------------------------------------------------------------------------------------
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

# ---------------------------------------------------------------------------------------------------------
# Machines.  A program is a sequence of calls on a machine m.  FastM executes it; CountM executes it and also
# counts every primitive by category, tracks a per-lane upper bound of every value (asserting that no ADD can
# carry across a 36-bit lane), and records definitions and uses for the register-liveness check.
L7, LW = 7, 36
CATS = ('rand', 'load', 'store', 'add', 'and', 'or', 'xor', 'shift', 'cmp', 'branch')
def pk(v): return sum((v & M32) << (LW * l) for l in range(L7))
def pkl(vals): return sum((vals[l] & M32) << (LW * l) for l in range(L7))
def unpk(x): return [(x >> (LW * l)) & M32 for l in range(L7)]
ROTS = (2, 6, 7, 11, 13, 17, 18, 19, 22, 25)
LANEMAX = (1 << LW) - 1

class FastM:
    """Uncounted execution (same program, same results)."""
    def __init__(self, mem=None):
        self.mem = {} if mem is None else mem
        self.M = pk(M32); self.G = sum(1 << (LW * l + 32) for l in range(L7)); self.ONE = pk(1)
        self.rlo = {r: pk(M32 >> r) for r in ROTS}; self.rhi = {r: pk((M32 << (32 - r)) & M32) for r in ROTS}
        self.sm = {3: pk(M32 >> 3), 10: pk(M32 >> 10)}
        self.coins = None
    def val(self, x): return x
    def LD(self, key): return self.mem[key]
    def ST(self, key, x): self.mem[key] = x
    def RAND(self): return self.coins()
    def ADD(self, a, b): return (a + b) & WORD
    def AND(self, a, b): return a & b
    def OR(self, a, b): return a | b
    def XOR(self, a, b): return a ^ b
    def SHR(self, a, k): return a >> k
    def SHL(self, a, k): return (a << k) & WORD
    def EQ(self, a, b): return a == b                       # compare + branch
    def IMM(self, v): return v                                # immediate operand (instruction field)
    # composites (each counts its parts)
    def mask(self, x): return self.AND(x, self.M)
    def ROTR(self, x, r): return self.OR(self.AND(self.SHR(x, r), self.rlo[r]), self.AND(self.SHL(x, 32 - r), self.rhi[r]))
    def SHR32(self, x, k): return self.AND(self.SHR(x, k), self.sm[k])
    def sig0(self, x): return self.XOR(self.XOR(self.ROTR(x, 7), self.ROTR(x, 18)), self.SHR32(x, 3))
    def sig1(self, x): return self.XOR(self.XOR(self.ROTR(x, 17), self.ROTR(x, 19)), self.SHR32(x, 10))
    def BS0(self, x): return self.XOR(self.XOR(self.ROTR(x, 2), self.ROTR(x, 13)), self.ROTR(x, 22))
    def BS1(self, x): return self.XOR(self.XOR(self.ROTR(x, 6), self.ROTR(x, 11)), self.ROTR(x, 25))

class Val:
    __slots__ = ('v', 'b', 'id')
    def __init__(self, v, b, i): self.v = v; self.b = b; self.id = i

class CountM(FastM):
    """Counted execution: tick per primitive; per-lane bound; liveness trace (resident registers excluded)."""
    def __init__(self, mem=None):
        FastM.__init__(self, mem)
        self.ct = dict((c, 0) for c in CATS); self.t = 0; self.uses = {}; self.defs = {}; self.nid = 0
        self.resident = 3 + 2 * len(ROTS) + len(self.sm) + 2      # M, G, ONE, rotation and shift masks, w15, k
        R_ = lambda x, b: Val(x, b, None)
        self.M = R_(self.M, M32); self.G = R_(self.G, 1 << 32); self.ONE = R_(self.ONE, 1)
        self.rlo = dict((r, R_(v, M32 >> r)) for r, v in self.rlo.items())
        self.rhi = dict((r, R_(v, (M32 << (32 - r)) & M32)) for r, v in self.rhi.items())
        self.sm = dict((k, R_(v, M32 >> k)) for k, v in self.sm.items())
    def total(self): return sum(self.ct.values())
    def _new(self, v, b, cat):
        self.ct[cat] += 1; self.t += 1; self.nid += 1
        x = Val(v, b, self.nid); self.defs[self.nid] = self.t; return x
    def _use(self, *xs):
        for x in xs:
            if isinstance(x, Val) and x.id is not None: self.uses[x.id] = self.t + 1
    def val(self, x): return x.v if isinstance(x, Val) else x
    def LD(self, key):
        v, b = self.mem[key]; return self._new(v, b, 'load')
    def ST(self, key, x):
        self._use(x); self.ct['store'] += 1; self.t += 1; self.mem[key] = (x.v, x.b)
    def RAND(self): return self._new(self.coins(), WORD, 'rand')
    def ADD(self, a, b):
        self._use(a, b); bb = a.b + b.b
        assert bb <= LANEMAX, 'lane overflow possible'
        return self._new((a.v + b.v) & WORD, bb, 'add')
    def AND(self, a, b): self._use(a, b); return self._new(a.v & b.v, min(a.b, b.b), 'and')
    def OR(self, a, b): self._use(a, b); return self._new(a.v | b.v, (1 << max(a.b.bit_length(), b.b.bit_length())) - 1, 'or')
    def XOR(self, a, b): self._use(a, b); return self._new(a.v ^ b.v, (1 << max(a.b.bit_length(), b.b.bit_length())) - 1, 'xor')
    def SHR(self, a, k): self._use(a); return self._new(a.v >> k, LANEMAX, 'shift')
    def SHL(self, a, k): self._use(a); return self._new((a.v << k) & WORD, LANEMAX, 'shift')
    def EQ(self, a, b):
        self._use(a, b); self.ct['cmp'] += 1; self.ct['branch'] += 1; self.t += 2
        return self.val(a) == self.val(b)
    def IMM(self, v): return Val(v, v, None)
    def liveout(self, *xs): self._use(*xs)
    def maxlive(self):
        """Maximum number of simultaneously live values (defined, with a later use) over the program."""
        ev = []
        for i, d in self.defs.items():
            u = self.uses.get(i)
            if u is not None: ev.append((d, 1)); ev.append((u, -1))
        ev.sort(key=lambda z: (z[0], z[1])); live = best = 0
        for _, s in ev: live += s; best = max(best, live)
        return best

class Sc:
    """Counted scalar machine (group setup, rare path, Step 3): one 32-bit value per 256-bit word.  Every
    primitive counts 1: ld (load), add, sub, and, or, xor, shr, shl, compare, branch.  Arithmetic is mod 2^256
    (lazy) and m() masks to 32 bits.  A rotation uses the doubled word x | x << 32 (2 ops), so S0, S1, s0 and
    s1 cost 8 each; every input of a doubling or a compare is asserted to be masked."""
    def __init__(self): self.n = 0
    def ld(self, v): self.n += 1; return v
    def add(self, a, b): self.n += 1; return (a + b) & WORD
    def sub(self, a, b): self.n += 1; return (a - b) & WORD
    def m(self, a): self.n += 1; return a & M32
    def xor(self, a, b): self.n += 1; return a ^ b
    def and_(self, a, b): self.n += 1; return a & b
    def or_(self, a, b): self.n += 1; return a | b
    def shr(self, a, k): self.n += 1; return a >> k
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

# ---------------------------------------------------------------------------------------------------------
# Program constants (written once at start: c_init stores), group setup, batch, rare path.
def varying(R):
    """Schedule words that depend on W15 (structural)."""
    v = {15}
    for i in range(16, R):
        if any(j in v for j in (i - 2, i - 7, i - 15, i - 16)): v.add(i)
    return v

def foldK(R, i):
    """K_i is folded into W_i's group constant when W_i has a constant part and no later schedule use."""
    return i in varying(R) and i >= 21 and all(j >= R for j in (i + 2, i + 7, i + 15, i + 16)) and \
        any(j not in varying(R) for j in (i - 2, i - 7, i - 15, i - 16))

# Mask sites the structural lane-bound check of CountM proved unnecessary (found by nomask_search(); every
# ADD of the batch still satisfies bound <= 2^36 - 1, asserted on every counted run).
SKIP = {37: {('A', 20), ('A', 21), ('A', 25), ('A', 35), ('E', 35)} | set(('W', i) for i in range(17, 37) if i not in (18, 20)),
        38: {('A', 20), ('A', 21), ('A', 25), ('A', 36), ('E', 36)} | set(('W', i) for i in range(17, 38) if i not in (18, 20))}

def program_constants(R, P):
    c = {}
    for i in range(R): c[('K', i)] = pk(K[i])
    c['c7m'] = pk((P['c7'] - IV[0] + 1) & M32); c['d7'] = pk(P['d7']); c['t7'] = pk(P['t7'])
    c['IV0'] = pk(IV[0]); c['IV1'] = pk(IV[1]); c['base15'] = pkl([l << 29 for l in range(L7)])
    if R == 37:
        A, E = P['Sx']
        c['k3'] = pk(P['k3']); c['A1|A0'] = pk(A[1] | A[0]); c['A1&A0'] = pk(A[1] & A[0])
        c['E5&E4'] = pk(E[5] & E[4]); c['~E5'] = pk(E[5] ^ M32); c['k6'] = pk((P['c6'] + 2) & M32)
        c['d6'] = pk(P['d6']); c['t6'] = pk(P['t6'])
    return c

def install(m, R, P):
    """Write the packed program constants to memory; returns c_init (one store each)."""
    c = program_constants(R, P)
    for k, v in c.items(): m.mem[k] = (v, M32) if isinstance(m, CountM) else v
    return len(c)

BCAST = 7     # broadcast of a 32-bit value to 7 lanes: 3 shl + 3 or + 1 and

def group_setup(m, sc, R, words):
    """Per group: W0..W14 of M0 from two RAND words (shift + mask each), rounds 0..14 and the group constants
    on the scalar machine; each constant is masked, broadcast to the 7 lanes and stored."""
    w = [sc.m(sc.shr(words[j // 8], 32 * (j % 8))) for j in range(15)]
    a, b, c, d, e, f, g, h = [sc.ld(x) for x in IV]
    for i in range(15):
        t1 = sc.add(sc.add(sc.add(sc.add(h, sc.S1(e)), sc.IF(e, f, g)), sc.ld(K[i])), w[i])
        t2 = sc.add(sc.S0(a), sc.MAJ(a, b, c))
        a, b, c, d, e, f, g, h = sc.m(sc.add(t1, t2)), a, b, c, sc.m(sc.add(d, t1)), e, f, g
    A14, A13, A12, A11, E14, E13, E12 = a, b, c, d, e, f, g
    t1c = sc.add(sc.add(sc.add(h, sc.S1(e)), sc.IF(e, f, g)), sc.ld(K[15]))
    t2c = sc.add(sc.S0(a), sc.MAJ(a, b, c))
    Wc = dict(enumerate(w))
    for i in (16, 18, 20):
        Wc[i] = sc.m(sc.add(sc.add(sc.s1(Wc[i-2]), Wc[i-7]), sc.add(sc.s0(Wc[i-15]), Wc[i-16])))
    G = {}
    G['ke15'] = sc.add(A11, t1c); G['ka15'] = sc.add(t1c, t2c)
    G['E14^E13'] = sc.xor(E14, E13); G['E13'] = E13; G['k16'] = sc.add(sc.add(E12, sc.ld(K[16])), Wc[16])
    G['A14|A13'] = sc.or_(A14, A13); G['A14&A13'] = sc.and_(A14, A13); G['A12'] = A12
    G['E14'] = E14; G['k17'] = sc.add(E13, sc.ld(K[17])); G['A14'] = A14; G['A13'] = A13
    G['k18'] = sc.add(sc.add(E14, sc.ld(K[18])), Wc[18]); G['k20'] = sc.add(sc.ld(K[20]), Wc[20])
    var = varying(R)
    for i in sorted(var - {15}):
        cst = None
        for (j, fn) in ((i - 2, 's1'), (i - 7, None), (i - 15, 's0'), (i - 16, None)):
            if j in var: continue
            t = sc.s1(Wc[j]) if fn == 's1' else sc.s0(Wc[j]) if fn == 's0' else Wc[j]
            cst = t if cst is None else sc.add(cst, t)
        if cst is not None and foldK(R, i): cst = sc.add(cst, sc.ld(K[i]))
        if cst is not None: G[('W', i)] = cst
    cm = isinstance(m, CountM)
    for k, v in G.items():
        v = sc.m(v); sc.n += BCAST
        m.ST(('g', k), Val(pk(v), M32, None) if cm else pk(v))
    return len(G)

def batch(m, R):
    """The counted batch: rounds 15..R-1 of the 7 first blocks of the group whose W15 lanes are in m.w15, and
    the Step-2 W7 filter.  Returns (some lane passes W7, live-out registers for the rare path)."""
    LD = m.LD; var = varying(R); Wv = {15: m.w15}; sk = SKIP[R]
    def mk(name, x): return x if name in sk else m.mask(x)
    def sched(i):
        terms = []
        for (j, fn) in ((i - 2, 's1'), (i - 7, None), (i - 15, 's0'), (i - 16, None)):
            if j in var:
                x = Wv[j]; terms.append(m.sig1(x) if fn == 's1' else m.sig0(x) if fn == 's0' else x)
        x = terms[0]
        for t in terms[1:]: x = m.ADD(x, t)
        if ('g', ('W', i)) in m.mem: x = m.ADD(x, LD(('g', ('W', i))))
        Wv[i] = mk(('W', i), x)
    w15 = m.w15
    E15 = m.mask(m.ADD(LD(('g', 'ke15')), w15)); A15 = m.mask(m.ADD(LD(('g', 'ka15')), w15))
    # round 16: f, g, h, b, c, d are group constants
    ch = m.XOR(m.AND(E15, LD(('g', 'E14^E13'))), LD(('g', 'E13')))
    T1 = m.ADD(m.ADD(m.BS1(E15), ch), LD(('g', 'k16')))
    mj = m.OR(m.AND(A15, LD(('g', 'A14|A13'))), LD(('g', 'A14&A13')))
    T2 = m.ADD(m.BS0(A15), mj)
    E16 = m.mask(m.ADD(LD(('g', 'A12')), T1)); A16 = m.mask(m.ADD(T1, T2))
    # round 17: g, h, c, d constant; W17 varying
    sched(17)
    g_ = LD(('g', 'E14')); ch = m.XOR(m.AND(E16, m.XOR(E15, g_)), g_)
    T1 = m.ADD(m.ADD(m.ADD(m.BS1(E16), ch), Wv[17]), LD(('g', 'k17')))
    bc = m.XOR(A15, LD(('g', 'A14'))); ab = m.XOR(A16, A15); mj = m.XOR(m.AND(ab, bc), A15)
    T2 = m.ADD(m.BS0(A16), mj)
    E17 = m.mask(m.ADD(LD(('g', 'A13')), T1)); A17 = m.mask(m.ADD(T1, T2))
    # round 18: h, d constant; W18 constant
    ch = m.XOR(m.AND(E17, m.XOR(E16, E15)), E15)
    T1 = m.ADD(m.ADD(m.BS1(E17), ch), LD(('g', 'k18')))
    ab2 = m.XOR(A17, A16); mj = m.XOR(m.AND(ab2, ab), A16)
    T2 = m.ADD(m.BS0(A17), mj)
    E18 = m.mask(m.ADD(LD(('g', 'A14')), T1)); A18 = m.mask(m.ADD(T1, T2))
    a, b, c, d, e, f, g, h = A18, A17, A16, A15, E18, E17, E16, E15; prev = ab2
    for i in range(19, R):
        if i in var: sched(i)
        ch = m.XOR(m.AND(e, m.XOR(f, g)), g)
        if i == 20: T1 = m.ADD(m.ADD(m.ADD(h, m.BS1(e)), ch), LD(('g', 'k20')))
        elif foldK(R, i): T1 = m.ADD(m.ADD(m.ADD(h, m.BS1(e)), ch), Wv[i])
        else: T1 = m.ADD(m.ADD(m.ADD(m.ADD(h, m.BS1(e)), ch), Wv[i]), LD(('K', i)))
        xab = m.XOR(a, b); mj = m.XOR(m.AND(xab, prev), b); T2 = m.ADD(m.BS0(a), mj); prev = xab
        if i < R - 1:
            a, b, c, d, e, f, g, h = mk(('A', i), m.ADD(T1, T2)), a, b, c, mk(('E', i), m.ADD(d, T1)), e, f, g
        else:
            Alast = m.ADD(T1, T2)
    # Step-2 filter: W7 = c7 - IV0 - A[R-1]; a lane passes iff s0(W7 + d7) - s0(W7) = t7 (mod 2^32)
    xm = m.mask(Alast)
    W7 = m.mask(m.ADD(m.XOR(xm, m.M), LD('c7m')))
    W7p = m.mask(m.ADD(W7, LD('d7')))
    z = m.XOR(m.mask(m.ADD(m.sig0(W7), LD('t7'))), m.sig0(W7p))
    y = m.AND(m.ADD(z, m.M), m.G)                  # bit 32 of a lane is set iff the lane fails
    hit = not m.EQ(y, m.G)
    live = dict(xm=xm, a=a, b=b, c=c, d=d, T1=T1, e=e, f=f, g=g, y=y)
    if isinstance(m, CountM): m.liveout(*live.values())
    return hit, live

def batch_control(m):
    """Advance the 7 lane words (W15 += 1 in every lane) and the batch counter: add, add, compare, branch."""
    m.w15 = m.ADD(m.w15, m.ONE); m.k = m.ADD(m.k, m.IMM(1)); return m.EQ(m.k, m.IMM(1 << 29))

def w6_filter(m, live):
    """r37 rare path (once per batch with a W7 pass): SWAR W6 test, combined lane flags (bit 32 = fail)."""
    LD = m.LD
    A1 = m.mask(m.ADD(live['xm'], LD('IV0'))); A2 = m.mask(m.ADD(live['a'], LD('IV1')))
    E3 = m.mask(m.ADD(A1, LD('k3')))
    mj = m.OR(m.AND(A1, LD('A1|A0')), LD('A1&A0'))
    iv = m.XOR(LD('E5&E4'), m.AND(E3, LD('~E5')))
    W6 = m.mask(m.ADD(m.ADD(m.ADD(m.XOR(A2, m.M), mj), m.XOR(iv, m.M)), LD('k6')))
    W6p = m.mask(m.ADD(W6, LD('d6')))
    z = m.XOR(m.mask(m.ADD(m.sig0(W6), LD('t6'))), m.sig0(W6p))
    return m.OR(live['y'], m.AND(m.ADD(z, m.M), m.G))

def lanes_passing(m, y):
    """Scan the 7 lane flags (shift, and, compare, branch per lane)."""
    out = []
    for j in range(L7):
        if m.EQ(m.AND(m.SHR(y, LW * j + 32), m.IMM(1)), m.IMM(0)): out.append(j)
    return out

# ---------------------------------------------------------------------------------------------------------
# Step 3 (counted on Sc).
def lane_cv(sc, m, live, j):
    """CV1 of lane j: A[-1..-4] = (A_{R-1}, A_{R-2}, A_{R-3}, A_{R-4}) + IV0..3, E[-1] = d + T1 + IV4,
    E[-2..-4] = (E_{R-2}, E_{R-3}, E_{R-4}) + IV5..7 (shift the lane down, add, mask)."""
    g = lambda x: sc.shr(m.val(live[x]), LW * j)
    cv = [sc.m(sc.add(g(k), sc.ld(IV[i]))) for i, k in enumerate(('xm', 'a', 'b', 'c'))]
    cv.append(sc.m(sc.add(sc.add(g('d'), g('T1')), sc.ld(IV[4]))))
    cv += [sc.m(sc.add(g(k), sc.ld(IV[5 + i]))) for i, k in enumerate(('e', 'f', 'g'))]
    return cv

def stage3_constants(P):
    A, E = P['Sx']; c = {}
    c['kE1'] = (A[1] - S0(A[0])) & M32; c['kE2'] = (A[2] - S0(A[1])) & M32
    c['A1&A0'] = A[1] & A[0]; c['A1|A0'] = A[1] | A[0]
    c['kW4'] = (E[4] - A[0] - K[4]) & M32; c['kW5'] = (E[5] - A[1] - S1(E[4]) - K[5]) & M32
    c['kW6'] = (E[6] - A[2] - S1(E[5]) - K[6]) & M32; c['E5&E4'] = E[5] & E[4]; c['~E5'] = E[5] ^ M32
    return c

def step3(sc, P, cv, cost=None):
    """Counted Step 3 for one valid lane, cv = (A[-1], A[-2], A[-3], A[-4], E[-1], E[-2], E[-3], E[-4]).
    Stage 3a, for every l in L* in order: E16 = (c16 + k16) + s0(W1) + W0 must match the x-value cells of E16
    and the E15/E16 '+' pairs.  At the first pass W2..W7 are completed; stage 3b runs rows 16..R-1 of both
    members, checking every cell of the row and aborting at the first failing row.  Returns
    (index in L*, X words, Y words, stage-3b entries) for the first l passing every row, else (None, ...)."""
    R = P['R']; ld = sc.ld; A, E = P['Sx']; c = P['s3c']; n0 = sc.n
    a1, a2, a3, a4, e1, e2, e3, e4 = cv
    E0 = sc.m(sc.sub(sc.sub(sc.add(ld(A[0]), a4), sc.S0(a1)), sc.MAJ(a1, a2, a3)))
    W0 = sc.m(sc.sub(sc.sub(sc.sub(sc.sub(sc.sub(E0, a4), e4), sc.S1(e1)), sc.IF(e1, e2, e3)), ld(K[0])))
    E1 = sc.m(sc.sub(sc.add(ld(c['kE1']), a3), sc.MAJ(ld(A[0]), a1, a2)))
    W1 = sc.m(sc.sub(sc.sub(sc.sub(sc.sub(sc.sub(E1, a3), e3), sc.S1(E0)), sc.IF(E0, e1, e2)), ld(K[1])))
    q = sc.add(sc.s0(W1), W0)
    sc.keep = [E0, W0, E1, W1, q]                 # (bookkeeping for rare_liveness only; no operation)
    if cost is not None: cost['c01'] = sc.n - n0
    rest = None; n3b = 0
    for li, d in enumerate(P['Lstar']):
        n1 = sc.n
        e16 = sc.m(sc.add(ld(d['ck16']), q))
        p3a = sc.eq(sc.xor(sc.and_(e16, ld(P['m16'])), ld(d['v16'])), 0)
        if cost is not None: cost['c3a'] = sc.n - n1
        if not p3a: continue
        n3b += 1; sc.n += FLAG3B + V3B; n2 = sc.n    # flag test (are W2..W7 computed yet?), V update, register spill
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
        X = rest + [ld(P['Wx'][i]) for i in range(8, 14)] + [ld(d['w'][0]), ld(d['w'][1])]
        Y = rest_y + [ld(P['Wy'][i]) for i in range(8, 14)] + [ld(d['w'][2]), ld(d['w'][3])]
        Ax = dict((i, ld(d['Ax'][i])) for i in range(12, 16)); Ex = dict((i, ld(d['Ex'][i])) for i in range(12, 16))
        Ay = dict((i, ld(d['Ay'][i])) for i in range(12, 16)); Ey = dict((i, ld(d['Ey'][i])) for i in range(12, 16))
        ok = True
        for i in range(16, R):
            for Z in (X, Y):
                Z.append(sc.m(sc.add(sc.add(sc.add(sc.s1(Z[i-2]), Z[i-7]), sc.s0(Z[i-15])), Z[i-16])))
            k = ld(K[i])
            for (Aa, Ee, Z) in ((Ax, Ex, X), (Ay, Ey, Y)):
                t = sc.add(sc.add(sc.add(sc.add(sc.add(Aa[i-4], Ee[i-4]), sc.S1(Ee[i-1])),
                                         sc.IF(Ee[i-1], Ee[i-2], Ee[i-3])), k), Z[i])
                Ee[i] = sc.m(t)
                Aa[i] = sc.m(sc.add(sc.add(sc.sub(Ee[i], Aa[i-4]), sc.S0(Aa[i-1])), sc.MAJ(Aa[i-1], Aa[i-2], Aa[i-3])))
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
    """Sc with a register-liveness trace: every value is live from the operation that defines it to the last
    operation that reads it (a result may reuse a dying input's register); a rotation function holds two extra
    temporaries (the doubled word and a partial result).  Used only by rare_liveness()."""
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
    def shr(self, a, k): self.n += 1; return self._op((a,), self.u(a) >> k)
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
    """Register demand of the scalar rare path for one lane, from the published pair's chaining value.  Lane path
    (lane_cv words, c01 and the 32 stage-3a tests, no stage-3b entry): the chaining value, E0, W0, E1, W1 and q stay
    live to the end (a later element of L* may enter stage 3b); the batch's 10 live-out values, the 27 resident
    registers and the counter V are live as well.  Stage 3b (the published element passes every row) runs after the
    register file is saved (SPILL3B), so only its own values and V occupy registers; W0..W7, W'6, W'7 are stored
    once computed and q is restored with the file.  Returns (lane peak, stage-3b peak) of the traced values."""
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
# Bookkeeping of the rare path, counted into V like every other rare-path operation: VLANE = 1 per passing lane
# (V += the lane's fixed cost, one ADD with an immediate); per stage-3b entry V3B = VENT + SPILL3B with VENT = 1
# (V += the cost of the executed stage-3b path, one ADD with an immediate at its exit) and SPILL3B = 148: STORE all
# 64 registers at entry and LOAD them back at exit (128), so stage 3b has the whole register file, plus STORE of
# W0..W7, W'6, W'7 after they are first computed and their LOAD at a later entry (20); see rare_liveness().
VLANE, VENT, SPILL3B = 1, 1, 148
V3B = VENT + SPILL3B

def verify(R, M0, X, Y):
    """Target verification (charged VFIN_UNITS target compressions + VFIN_OPS operations, at most once):
    the complete 128-byte messages M0||M1 and M0||M1' are distinct and have equal R-step digests."""
    mx = struct.pack('>16I', *M0) + struct.pack('>16I', *X); my = struct.pack('>16I', *M0) + struct.pack('>16I', *Y)
    if mx != my and digest(mx, R) == digest(my, R): return mx, my
    return None

# ---------------------------------------------------------------------------------------------------------
# The attack with fixed caps.  NG groups of NB = 2^29 batches (7 trials each).  V counts every operation of the
# rare path (the SWAR W6 test and the lane scan at their exact straight-line counts OPS[R], every Sc operation,
# VCTRL = 3 for the batch's update of V and its cap test, VLANE per passing lane and V3B per stage-3b entry);
# the run halts with failure as soon as V exceeds VMAX.  The
# group loop costs GCTRL = 4 per group (zero the batch counter; add, compare, branch on the group counter),
# charged by cert.py with c_G.  coins() returns a uniform 256-bit word.
OPS = {}
VCTRL, GCTRL = 3, 4

def attack(R, P, NG, VMAX, coins, nbatch=1 << 29, hook=None):
    if R not in OPS: calibrate(R, P)
    m = FastM(); install(m, R, P); m.coins = coins; V = 0
    for gi in range(NG):
        sc = Sc(); r0, r1 = m.RAND(), m.RAND(); group_setup(m, sc, R, (r0, r1))
        M0 = [(r0 >> (32 * j)) & M32 for j in range(8)] + [(r1 >> (32 * j)) & M32 for j in range(7)]
        m.w15 = m.LD('base15'); m.k = m.IMM(0)
        for kb in range(nbatch):
            hit, live = batch(m, R); found = []
            if hit:
                v = Sc(); y = live['y']
                if R == 37: y = w6_filter(m, live); v.n += OPS[R]['w6']
                v.n += OPS[R]['scan'] + VCTRL
                for j in lanes_passing(m, y):
                    v.n += VLANE
                    cv = lane_cv(v, m, live, j)
                    li, X, Y, n3b = step3(v, P, cv)
                    found.append((j, cv, li, n3b))
                    if li is not None:
                        res = verify(R, M0 + [(j << 29) + kb], X, Y)
                        if res:
                            if hook: hook(M0, kb, live, hit, found)
                            return dict(pair=res, V=V + v.n, group=gi, batch=kb)
                V += v.n
            if hook: hook(M0, kb, live, hit, found)
            if V > VMAX: return dict(pair=None, V=V, group=gi, batch=kb, halted=True)
            batch_control(m)
    return dict(pair=None, V=V, group=NG, batch=0)

def calibrate(R, P):
    """Exact operation counts, each asserted equal over three groups: c_init, c_G, c_B (batch + control) with
    categories, the r37 SWAR W6 test, the lane scan, the register high-water mark of the batch; and the Step-3
    parts on the published pair's chaining value: c_cv (lane_cv), c01, c3a (per l), crest, c3b (full pass)."""
    res = None
    for seed in (1, 2, 3):
        def coins(s=[seed]):
            s[0] += 1; return int.from_bytes(hashlib.sha256(b'cal%d' % s[0]).digest(), 'big')
        m = CountM(); ci = install(m, R, P); m.coins = coins; sc = Sc()
        r = (m.RAND(), m.RAND()); ng = group_setup(m, sc, R, (r[0].v, r[1].v))
        m.w15 = m.LD('base15'); m.w15.id = None; m.k = m.IMM(0)
        cG = m.total() + sc.n
        m.ct = dict((c, 0) for c in CATS); m.defs = {}; m.uses = {}; m.t = 0
        hit, live = batch(m, R); body = m.total(); cats = dict(m.ct); mx = m.maxlive()
        batch_control(m); cB = m.total()
        m2 = CountM(m.mem); w6 = 0
        if R == 37: w6_filter(m2, dict((k, Val(v.v, v.b, None)) for k, v in live.items())); w6 = m2.total()
        m3 = CountM(); lanes_passing(m3, Val(0, WORD, None)); scan = m3.total()
        sc2 = Sc(); lane_cv(sc2, m, live, 3); ccv = sc2.n
        cost = {}; sc3 = Sc(); out = step3(sc3, P, PAIRS[R]['cv'], cost)
        lv = rare_liveness(R, P)
        assert out[0] is not None and out[1] == PAIRS[R]['mp'] and out[2] == PAIRS[R]['m']
        cur = dict(c_init=ci, c_G=cG, groupconsts=ng, c_B=cB, body_filter=body, cats=cats, w6=w6, scan=scan,
                   maxlive=mx, resident=m.resident, c_cv=ccv, c01=cost['c01'], c3a=cost['c3a'],
                   crest=cost['crest'], c3b=cost['c3b'], live_lane=lv[0], live_3b=lv[1])
        assert res is None or res == cur, (res, cur)
        res = cur
    OPS[R] = res
    return res

def nomask_search(R, P):
    """Greedy: drop each mask site (schedule words, then state words from the last round down) when the
    structural per-lane bound check still passes for the whole batch and the W6 test."""
    sites = [('W', i) for i in sorted(varying(R) - {15})] + [(k, i) for i in range(R - 2, 18, -1) for k in ('E', 'A')]
    SKIP[R] = set()
    for s_ in sites:
        SKIP[R].add(s_)
        try:
            OPS.pop(R, None); calibrate(R, P)
        except AssertionError:
            SKIP[R].discard(s_)
    OPS.pop(R, None); calibrate(R, P)
    return sorted(SKIP[R])

# ---------------------------------------------------------------------------------------------------------
# Organizer experiment (python-message-pairs-v1).  Per organizer seed: one group of the attack with W0..W14 of
# M0 from SHAKE-256(seed), NB_EXP[R] batches of the driver above (same program; caps irrelevant here).  A hook
# checks every lane against the scalar compression (all 8 chaining-value words via lane_cv, the W7 decision, and
# for r37 the W6 decision), checks that every valid lane is exactly the set the driver sends to Step 3, and that
# for every valid lane and every l in L* the pair (M1, M1') follows every cell of rows -4..15.  The pair
# M0||M1, M0||M1' of the first valid lane (published W14, W15) is returned if every check passed, else nulls.
NB_EXP = {37: 16, 38: 3}

def experiment(req):
    R = {'sha256-r37-prefix-v1': 37, 'sha256-r38-prefix-v1': 38}[req['target_profile']]
    P = setup(R); cal = calibrate(R, P); lsfs = [d['w'][:2] for d in P['Lstar']].index(tuple(P['Wx'][14:16]))
    rows = []
    for tr in req['trials']:
        seed = bytes.fromhex(tr['seed']); ctr = [0]
        def coins():
            ctr[0] += 1; return int.from_bytes(hashlib.shake_256(seed + bytes([ctr[0]])).digest(32), 'big')
        obs = dict(lanes=0, mismatches=0, w7_pass=0, valid=0, stage3b=0, deepest_row=15, batch_ops=cal['c_B'])
        first = []
        def hook(M0, kb, live, hit, found):
            fl = dict((f[0], f) for f in found)
            for j in range(L7):
                blk = M0 + [(j << 29) + kb]; cv = compress(IV, blk, R); obs['lanes'] += 1
                bad = lane_cv(Sc(), FastM(), live, j) != cv
                p7 = inF((P['c7'] - cv[0]) & M32, P['d7'], P['t7'])
                bad |= p7 != ((live['y'] >> (LW * j + 32)) & 1 == 0)
                W = ref_words(P, cv); valid = p7 and inF(W[6], P['d6'], P['t6'])
                bad |= valid != (j in fl)
                obs['w7_pass'] += p7
                if valid:
                    obs['valid'] += 1; obs['stage3b'] += fl[j][3]
                    Wy = W[:6] + [(W[6] + P['d6']) & M32, (W[7] + P['d7']) & M32]
                    for li, d in enumerate(P['Lstar']):
                        X = W + P['Wx'][8:14] + list(d['w'][:2]); Y = Wy + P['Wy'][8:14] + list(d['w'][2:])
                        b = cellcheck(R, cv, X, Y)[0]
                        bad |= any(i < 16 and (k, i) not in (('W', 6), ('W', 7)) for k, i in b)
                        obs['deepest_row'] = max(obs['deepest_row'], min([i for _, i in b] + [R]) - 1)
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

# ---------------------------------------------------------------------------------------------------------
# Organizer experiment d1-q3-smc-r37 (H2; proof.md Section 10.2): smc.py's estimator of q3 at reduced size, with
# exact row 16 and exact draws from F7; every tail success is rebuilt and checked as a 37-step SFS collision.
FIX = {('A', 16, 29, '=', 'A', 17, 29): ('A', 15, 29, '=', 'A', 17, 29)}   # Section 3.3
KI = {'A': 0, 'E': 1, 'W': 4}
Q3X = dict(K=20, NP=64, MS={17: 4, 18: 4, 19: 1, 20: 1, 21: 1}, MT=512, POOL_LOG2=-74.35)

def xlist(R):
    out = {}
    for x in CH[R]['X']:
        x = FIX.get(x, x)
        if max(x[1], x[5]) >= 16: out.setdefault(max(x[1], x[5]), []).append(x)
    return out

def recipe(P, XL, kind, i):
    """As smc.propose: x-value cells, '+' bits, same-kind two-bit conditions of row i fixed; weight 2^-f."""
    m0, v, _, _ = row(CH[P['R']], kind, i); pq = P['rows'][i][3] if kind == 'E' else 0; m = det = m0 | pq; steps = []
    for w1, i1, b1, op, w2, i2, b2 in XL.get(i, ()):
        if w1 != kind or w2 != kind: continue
        for ia, ba, ib, bb in ((i2, b2, i1, b1), (i1, b1, i2, b2)):
            if ia == i and not det >> ba & 1 and (ib < i or det >> bb & 1 or ib == i and not m >> bb & 1):
                steps.append((ba, ib, bb, op == '!')); m |= 1 << ba; det |= 1 << ba | 1 << bb; break
    return i, m0, v & m0, pq, steps, bin(m).count('1')

def propose(rc, Wd, rnd):
    i, m0, v, pq, steps, f = rc; e = v | rnd & ~m0 & M32
    if pq: e = e & ~pq | Wd[i - 1] & pq
    for ba, ib, bb, fl in steps: e = e & ~(1 << ba) | ((Wd[ib] if ib < i else e) >> bb & 1 ^ fl) << ba
    return e

def rowok(P, XL, p, i):
    (mA, vA, dA, _), (mE, vE, dE, _), (mW, vW, dW, _), pq = P['rows'][i]; a, e, x = p[0][i], p[1][i], p[4][i]
    if a ^ p[2][i] != dA or a & mA != vA or e ^ p[3][i] != dE or e & mE != vE or x ^ p[5][i] != dW or x & mW != vW \
            or (e ^ p[1][i - 1]) & pq: return False
    return all((p[KI[w1]][i1] >> b1 ^ p[KI[w2]][i2] >> b2) & 1 == (op == '!') for w1, i1, b1, op, w2, i2, b2 in XL.get(i, ()))

def stp(A, E, Z, i): E[i] = stepE(A, E, i, Z[i]); A[i] = stepA(A, E, i)
def sch(Z, i): return (s1(Z[i-2]) + Z[i-7] + s0(Z[i-15]) + Z[i-16]) & M32

def particle(P, d):
    p = [[0] * P['R'] for _ in range(6)]
    for i in range(12, 16): p[0][i], p[1][i], p[2][i], p[3][i] = d['Ax'][i], d['Ex'][i], d['Ay'][i], d['Ey'][i]
    p[4][8:16] = P['Wx'][8:14] + list(d['w'][:2]); p[5][8:16] = P['Wy'][8:14] + list(d['w'][2:])
    return p

def r16(P, XL, d):
    """Row 16 of l: word k of p is e + c[k] (e = E16^x); every condition as parities by bit (see nx)."""
    p = particle(P, d); AX, EX, AY, EY, X, Y = p; rw = P['rows'][16]; cs = []
    X[16] = -stepE(AX, EX, 16, 0) & M32; Y[16] = (X[16] + s1(Y[14]) - s1(X[14]) + Y[9] - X[9]) & M32
    stp(AX, EX, X, 16); stp(AY, EY, Y, 16)
    for b in range(32):
        for (m, v, dd, _), x, y in ((rw[0], 0, 2), (rw[1], 1, 3), (rw[2], 4, 5)):
            cs += [([(x, b), (y, b)], dd >> b & 1)] + [([(x, b)], v >> b & 1)] * (m >> b & 1)
        cs += [([(1, b)], EX[15] >> b & 1)] * (rw[3] >> b & 1)
    for w1, i1, b1, op, w2, i2, b2 in XL[16]:
        t = ((w1, i1, b1), (w2, i2, b2))
        cs.append(([(KI[w], b) for w, i, b in t if i == 16], (op == '!') ^ sum(p[KI[w]][i] >> b for w, i, b in t if i < 16) & 1))
    by = [[] for _ in range(32)]; ns = 0
    for rf, v in cs:
        bs = sorted(set(b for _, b in rf)); j = ns if len(bs) > 1 else -1; ns += len(bs) > 1
        for b in bs: by[b].append((sum(1 << w for w, b_ in rf if b_ == b), j, b == bs[-1], int(v)))
    return [w[16] for w in p], by

def nx(c, by, b, s, e):
    """State after bit b = e (bits 0..5 carries, 6 + j open parity j), None if a condition fails."""
    w = 0; s2 = s >> 6 << 6
    for i in range(6):
        t = e + (c[i] >> b & 1) + (s >> i & 1); w |= (t & 1) << i; s2 |= (t >> 1) << i
    for m, j, last, v in by[b]:
        x = bin(w & m).count('1') & 1
        if j >= 0: x ^= s2 >> 6 + j & 1; s2 &= ~(1 << 6 + j)
        if not last: s2 |= x << 6 + j
        elif x != v: return None
    return s2

def cnt(c, by, memo, b, s):
    if b == 32: return 1
    if (b, s) not in memo:
        memo[b, s] = sum(cnt(c, by, memo, b + 1, t) for t in (nx(c, by, b, s, 0), nx(c, by, b, s, 1)) if t is not None)
    return memo[b, s]

def unrank(c, by, memo, r):
    s = e = 0
    for b in range(32):
        for x in (0, 1):
            t = nx(c, by, b, s, x); n = 0 if t is None else cnt(c, by, memo, b + 1, t)
            if r < n: e |= x << b; s = t; break
            r -= n
    return e

def row16(P, XL):
    out = []
    for d in P['Lstar']: c, by = r16(P, XL, d); memo = {}; out.append((c, by, memo, cnt(c, by, memo, 0, 0)))
    return out

def gauss(eqs):
    pv = {}
    for r, v in eqs:
        for b, (q, u) in pv.items():
            if r >> b & 1: r ^= q; v ^= u
        if not r:
            if v: return None
            continue
        b = r.bit_length() - 1
        for b2, (q, u) in list(pv.items()):
            if q >> b & 1: pv[b2] = (q ^ r, u ^ v)
        pv[b] = (r, v)
    x0 = sum(u << b for b, (q, u) in pv.items())
    return x0, [1 << f | sum(1 << b for b, (q, u) in pv.items() if q >> f & 1) for f in range(32) if f not in pv]

def fparts(d, t):
    """{w : s0(w + d) - s0(w) = t}: disjoint affine spaces, one per carry pattern c of w + d (proof.md 10.2)."""
    sr = [sum((s0(1 << i) >> j & 1) << i for i in range(32)) for j in range(32)]; out = []; n = [0]
    def walk(j, c, eqs):
        if j < 31:
            if (c ^ d) >> j & 1:
                for x in (0, 1): walk(j + 1, c | x << j + 1, eqs + [(1 << j, x)])
            else: walk(j + 1, c | (d & 1 << j) << 1, eqs)
            return
        M = s0(d ^ c); u = (M - t) & M32
        if u & 1 or u >> 1 & ~M & 0x7fffffff: return
        a = gauss(eqs + [(sr[i], u >> i + 1 & 1) for i in range(31) if M >> i & 1])
        if a: out.append((n[0],) + a); n[0] += 1 << len(a[1])
    walk(0, 0, [])
    return out, n[0]

def fdraw(F, r):
    i = len(F[0]) - 1
    while F[0][i][0] > r: i -= 1
    s, x, bs = F[0][i]; r -= s
    for v in bs:
        if r & 1: x ^= v
        r >>= 1
    return x

def sfs(P, p, W7):
    X, Y = p[4], p[5]; W = [0] * 6 + [(X[22] - s1(X[20]) - X[15] - s0(W7)) & M32, W7]
    for i in range(5, -1, -1): W[i] = (X[i+16] - s1(X[i+14]) - X[i+9] - s0(W[i+1])) & M32
    wx = W + X[8:16]; wy = W[:6] + [(W[6] + P['d6']) & M32, (W7 + P['d7']) & M32] + Y[8:16]
    A = dict(P['Sx'][0]); E = dict(P['Sx'][1])
    for i in range(7, -1, -1):
        a = (E[i] - A[i] + S0(A[i-1]) + MAJ(A[i-1], A[i-2], A[i-3])) & M32
        if i >= 4 and a != A[i-4]: return None
        A[i-4] = a; E[i-4] = (E[i] - a - S1(E[i-1]) - IF(E[i-1], E[i-2], E[i-3]) - K[i] - wx[i]) & M32
    cv = [A[-1], A[-2], A[-3], A[-4], E[-1], E[-2], E[-3], E[-4]]; R = P['R']
    ok = wx != wy and compress(cv, wx, R) == compress(cv, wy, R) and ref_words(P, cv) == wx[:8] and inF(W7, P['d7'], P['t7']) \
        and inF(W[6], P['d6'], P['t6']) and set(cellcheck(R, cv, wx, wy)[0]) <= {('W', 6), ('W', 7)}
    return (cv, wx, wy) if ok else None

def mini_smc(P, XL, V, rng, NP, MS, MT):
    V16, F7 = V; R = P['R']; n16 = sum(v[3] for v in V16); est = n16 / (len(V16) * 2.0 ** 32); st = [(16, n16)]; ps = []
    for _ in range(NP):
        r = rng.randrange(n16); li = 0
        while r >= V16[li][3]: r -= V16[li][3]; li += 1
        p = particle(P, P['Lstar'][li]); e = unrank(*V16[li][:3], r)
        for w, c in zip(p, V16[li][0]): w[16] = (e + c) & M32
        assert rowok(P, XL, p, 16); ps.append(p)
    for i in range(17, 22):
        rc = recipe(P, XL, 'E', i); sv = []
        for p in ps:
            AX, EX, AY, EY, X, Y = p; c = stepE(AX, EX, i, 0)
            dy = s1(Y[i-2]) - s1(X[i-2]) + Y[i-7] - X[i-7] + (P['t6'] if i == 21 else 0)
            for _ in range(MS[i]):
                X[i] = (propose(rc, EX, rng.getrandbits(32)) - c) & M32; Y[i] = (X[i] + dy) & M32
                stp(AX, EX, X, i); stp(AY, EY, Y, i)
                if rowok(P, XL, p, i): sv.append([z[:] for z in p])
        st.append((i, len(sv))); est *= len(sv) * 2.0 ** -rc[5] / (NP * MS[i])
        if not sv: return 0.0, st, 0, [], 0
        ps = [sv[rng.randrange(len(sv))] for _ in range(NP)]
    rc = recipe(P, XL, 'W', 22); hits = bad = 0; pairs = []; d6, t6, d7 = P['d6'], P['t6'], P['d7']
    for p in ps:
        AX, EX, AY, EY, X, Y = p; b6 = (s1(X[20]) + X[15]) & M32; y6 = s1(Y[20]) + Y[15] + d6
        b7 = s1(X[21]) + X[16] + s0(X[8]); y7 = s1(Y[21]) + Y[16] + s0(Y[8]) + d7
        for _ in range(MT):
            w22 = propose(rc, X, rng.getrandbits(32)); W7 = fdraw(F7, rng.randrange(F7[1])); W6 = (w22 - b6 - s0(W7)) & M32
            if not inF(W6, d6, t6): continue
            X[22] = w22; Y[22] = (y6 + s0((W7 + d7) & M32) + W6) & M32; X[23] = (b7 + W7) & M32; Y[23] = (y7 + W7) & M32
            for i in range(22, R):
                if i > 23: X[i] = sch(X, i); Y[i] = sch(Y, i)
                stp(AX, EX, X, i); stp(AY, EY, Y, i)
                if not rowok(P, XL, p, i): break
            else:
                hits += 1; r = sfs(P, p, W7)
                if r is None: bad += 1
                else: pairs.append(r)
    st.append(('tail', hits))
    return est * hits * 2.0 ** (32 - rc[5]) / P['F6'] / (NP * MT), st, hits, pairs, bad

def q3_experiment(req):
    """Trial t < K: a replicate, its first pair iff all verify; K: the last pair iff all did and mean >= 2^POOL_LOG2."""
    R = {'sha256-r37-prefix-v1': 37}[req['target_profile']]; P = setup(R); XL = xlist(R); K_ = Q3X['K']
    F7 = fparts(P['d7'], P['t7']); assert F7[1] == P['F7']; V = (row16(P, XL), F7); rows, zs, last = [], [], []
    def put(o, pr): o['message_a_hex'], o['message_b_hex'] = (struct.pack('>24I', *pr[0], *w).hex() for w in pr[1:])
    for tr in req['trials']:
        t = tr['trial']; o = dict(trial=t, message_a_hex=None, message_b_hex=None)
        if t < K_:
            rng = random.Random(int.from_bytes(hashlib.shake_256(b'd1-q3' + bytes.fromhex(tr['seed'])).digest(32), 'big'))
            z, st, hits, pairs, bad = mini_smc(P, XL, V, rng, Q3X['NP'], Q3X['MS'], Q3X['MT']); zs.append(z)
            o['observations'] = dict(log2_estimate=math.log2(z) if z else -1000.0, row16_words=st[0][1], tail_successes=hits,
                                     verified_pairs=len(pairs), failed_rebuilds=bad, **{'survivors_%s' % s: n for s, n in st[1:6]})
            if hits and not bad: put(o, pairs[0]); last.append(pairs[-1])
        elif t == K_:
            zb = sum(zs) / len(zs); o['observations'] = dict(log2_pooled_mean=math.log2(zb) if zb else -1000.0, replicates=len(zs))
            if len(last) == K_ and zb >= 2.0 ** Q3X['POOL_LOG2']: put(o, last[-1])
        rows.append(o)
    return dict(schema_version=1, trials=rows)

if __name__ == '__main__':
    req = json.loads(sys.stdin.read())
    out = q3_experiment(req) if req['experiment_id'].startswith('d1-q3-smc') else experiment(req)
    sys.stdout.write(json.dumps(out, sort_keys=True, separators=(',', ':')))
```

<!-- file: cert.py sha256=b339aeb2db91dde4c7c003f4b90872b2c41d3db51e89a3e09a1cdcf9c0474cfb -->
```python
#!/usr/bin/env python3
# cert.py - the exact ledger of the d1 packages (proof.md Section 8).  Every count comes from d1core.calibrate()
# (the counted program) and d1core.setup(R, full=True) (the preprocessing enumeration); every probability is an
# exact rational except q3_model, the preregistered SMC value (H2).  The total is an exact rational; time_log2 is
# rounded up at the 5th decimal.  usage: cert.py 37|38  (prints JSON; exits non-zero if a check fails)
import sys, json, math
from fractions import Fraction as Fr
import d1core as D

Q3_LOG2 = {37: -74.01, 38: -101.02}          # preregistered q3_model (proof.md Section 6.3), filled from smc_summary.py
KAPPA = {37: Fr(255, 256), 38: Fr(1)}   # r37: disjointness factor for the 32 elements of L* (H2 (b))
A_C, A_S, DEV = 2 ** 60, 2 ** 50, 2 ** 40   # allowances (units): characteristic + SFS-pair search, Step-1 solve, our development
CTRL_INIT = D.GCTRL                     # per group: zero the batch counter; add, compare, branch on the group counter
INIT_ALLOW = 256                        # resident registers (27 masks/constants) loaded once + program start
PRE_PER_CAND = 1024                     # operation bound per candidate of the L enumeration (each < 300)
MARGIN = Fr(1025, 1024)                 # V_max = ceil(MARGIN * N_B * vbar)

def log2f(x):
    """log2 of a positive Fraction to ~1e-15 absolute."""
    n, d = x.numerator, x.denominator; k = n.bit_length() - d.bit_length() - 60
    q = (n << -k) // d if k < 0 else n // (d << k)
    return k + math.log2(q)

def ceil5(x): return math.ceil(x * 100000 - 1e-9) / 100000

def ledger(R, q3_log2=None):
    P = D.setup(R, full=True); cal = D.calibrate(R, P); C = D.C_REF[R]
    q3_log2 = Q3_LOG2[R] if q3_log2 is None else q3_log2
    nL = len(P['Lstar']); F7, F6 = P['F7'], P['F6']
    p7 = Fr(F7, 2 ** 32); p6 = Fr(F6, 2 ** 32); p2 = p7 * p6
    fl = math.floor(q3_log2)       # q3 = a rational not above 2^q3_log2
    q3 = Fr(2) ** fl * Fr(math.floor(2 ** (q3_log2 - fl) * 2 ** 40), 2 ** 40)
    pm = p2 * nL * q3 * KAPPA[R]
    per_group = 7 * 2 ** 29
    NG = -(-Fr(1, 2) // (per_group * pm)); NG = int(NG)
    NB = NG * 2 ** 29; N = 7 * NB
    assert N * pm >= Fr(1, 2)
    # data-dependent work per batch (exact expectation bound under H1) and its worst case
    P7any = 1 - (1 - p7) ** 7
    p3a = Fr(1, 2 ** P['f16'])
    sw = cal['w6'] + cal['scan'] + D.VCTRL       # per batch with a W7 pass: W6 test, lane scan, V update and cap test
    c3b = cal['c3b'] + D.FLAG3B + D.V3B           # per stage-3b entry: full pass, flag test, V update, register spill
    lane = cal['c_cv'] + cal['c01'] + D.VLANE + nL * cal['c3a'] + min(Fr(1), nL * p3a) * cal['crest'] + nL * p3a * c3b
    vbar = P7any * sw + 7 * p2 * lane
    vmax = sw + 7 * (cal['c_cv'] + cal['c01'] + D.VLANE + cal['crest'] + nL * (cal['c3a'] + c3b))
    VMAX = -(-(MARGIN * NB * vbar) // 1); VMAX = int(VMAX)
    pre_ops = (P['nE14'] + P['nE15']) * PRE_PER_CAND + 2 ** 20
    init_ops = cal['c_init'] + INIT_ALLOW
    online_ops = NG * (cal['c_G'] + CTRL_INIT) + NB * cal['c_B']
    rare_ops = VMAX + vmax
    fin = D.VFIN_UNITS + Fr(D.VFIN_OPS, C)
    T = A_C + A_S + DEV + Fr(pre_ops + init_ops + online_ops + rare_ops, C) + fin
    pre = A_C + A_S + DEV + Fr(pre_ops, C)
    # Hoeffding: Pr[V > VMAX] <= exp(-2 (VMAX - E V)^2 / (NB vmax^2)), VMAX - E V >= (MARGIN - 1) NB vbar
    hexp = 2 * ((MARGIN - 1) * vbar) ** 2 * NB / vmax ** 2
    succ_lb = 1 - math.exp(-float(N * pm)) - 2.0 ** -60 if log2f(hexp) > 6 else None
    out = dict(R=R, C=C, counts=cal, nLstar=nL, F7=F7, F6=F6, f16=P['f16'], nE14=P['nE14'], nE15=P['nE15'],
               log2_p2=log2f(p2), q3_model_log2=q3_log2, kappa=str(KAPPA[R]), log2_p_model=log2f(pm),
               NG=NG, NB=NB, log2_N=log2f(Fr(N)), N_times_p=float(N * pm),
               vbar=float(vbar), vmax=int(vmax), VMAX=VMAX, log2_hoeffding_exponent=log2f(hexp),
               ops=dict(pre=pre_ops, init=init_ops, online=online_ops, rare=rare_ops, fin_ops=D.VFIN_OPS),
               units=dict(A_C=A_C, A_S=A_S, DEV=DEV, pre=float(Fr(pre_ops, C)), online=float(Fr(online_ops, C)),
                          rare=float(Fr(rare_ops, C)), fin=float(fin)),
               T_num=T.numerator, T_den=T.denominator, log2_T=log2f(T), time_log2=ceil5(log2f(T)),
               preprocessing_log2=ceil5(log2f(pre)), success_lower_bound=succ_lb,
               log2_units_per_trial=log2f(Fr(cal['c_B'], 7 * C)))
    return out

if __name__ == '__main__':
    R = int(sys.argv[1]); out = ledger(R, float(sys.argv[2]) if len(sys.argv) > 2 else None)
    print(json.dumps(out, indent=1, default=str))
    assert out['success_lower_bound'] >= 0.39
```

<!-- file: selftest.py sha256=a1f5621b23bab9d00a62c8c5de7b742709d96055078f3d4259b4277bacb1893d -->
```python
#!/usr/bin/env python3
# selftest.py - checks of the d1 packages (proof.md Appendix A).  Extract the Appendix A files into one
# directory (snippet in Appendix A), then:  REPO_ROOT=/path/to/hash-smash python3 selftest.py 37 [full]
# (or 38).  Without REPO_ROOT the verifier comparisons are skipped and reported as such.  'full' re-enumerates L
# and L* (about 3 s for 37 steps, 14 s for 38 steps).  Exits non-zero on the first failed check.
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
# condition counts on rows >= 16 read off the tables (Section 6.4): one-bit cells (0, 1, u, n) plus printed two-bit
# conditions, grouped by their later row; every '+' pair with its later row >= 16 is a printed two-bit equality and is
# not counted again.  Stages as in smc.py: one per fresh row, then the deterministic tail.
fresh = range(16, 22 if R == 37 else 23)
pp = [(i, b) for (i, b) in pairs_ if i + 1 >= 16]
ok('plus_pairs_are_printed_conditions', all(('E', i, b, '=', 'E', i + 1, b) in ch['X'] for i, b in pp), len(pp))
cnt = {}
for i in range(16, R):
    k_ = str(i) if i in fresh else 'tail'
    cnt[k_] = cnt.get(k_, 0) + sum(sum(c in '01un' for c in ch[w].get(i, '=' * 32)) for w in 'AEW') + \
        sum(1 for x in ch['X'] if max(x[1], x[5]) == i)
res['condition_counts_rows_ge16'] = dict(cnt, total=sum(cnt.values()))
if R == 37: ok('condition_counts_as_stated', [cnt[k_] for k_ in ('16', '17', '18', '19', '20', '21', 'tail')] == [17, 13, 15, 6, 7, 1, 15])
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
ok('register_budget', cal['maxlive'] + cal['resident'] <= 64, cal['maxlive'] + cal['resident'])
# rare path: lane path with the batch's 10 live-out values, the resident registers and V; stage 3b after the
# register-file save (SPILL3B) with V
ok('rare_register_budget', cal['resident'] + 10 + 1 + cal['live_lane'] <= 64 and cal['live_3b'] + 1 <= 64,
   [cal['resident'] + 10 + 1 + cal['live_lane'], cal['live_3b'] + 1])
# 6. bit-exact: 300 batches (2100 lanes) of the counted program against the repository verifier (or d1core)
comp = (lambda cv, w: list(hf._compress('sha256', tuple(cv), struct.pack('>16I', *w), R))) if hf else D.compress
mis = 0; nl = 0; nv = 0; rnd = random.Random(1000 + R)
for g in range(100):
    m = D.FastM(); D.install(m, R, P); sc = D.Sc(); r0, r1 = rnd.getrandbits(256), rnd.getrandbits(256)
    D.group_setup(m, sc, R, (r0, r1)); M0 = [(r0 >> (32 * j)) & D.M32 for j in range(8)] + [(r1 >> (32 * j)) & D.M32 for j in range(7)]
    m.w15 = m.LD('base15'); m.k = 0
    for kb in range(3):
        hit, live = D.batch(m, R); y = D.w6_filter(m, live) if (R == 37 and hit) else live['y']
        for j in range(7):
            cv = comp(D.IV, M0 + [(j << 29) + kb]); nl += 1
            mis += D.lane_cv(D.Sc(), m, live, j) != cv
            W = D.ref_words(P, cv); p7 = D.inF((P['c7'] - cv[0]) & D.M32, P['d7'], P['t7'])
            mis += p7 != (((live['y'] >> (36 * j + 32)) & 1) == 0)
            if hit: mis += (p7 and D.inF(W[6], P['d6'], P['t6'])) != (((y >> (36 * j + 32)) & 1) == 0)
            Xm = W + P['Wx'][8:16]; A_, E_, _ = D.trace(cv, Xm, 14)       # W0..W7 reproduce S on rows 0..13
            mis += any(A_[i] != P['Sx'][0][i] or (i >= 4 and E_[i] != P['Sx'][1][i]) for i in range(14))
            nv += p7
        D.batch_control(m)
ok('batch_bit_exact', mis == 0, dict(lanes=nl, mismatches=mis, w7_pass=nv))
# 7. Step 3 end to end on the published pair's chaining value: the counted code derives W0..W7, finds the
#    published (W14, W15) in L*, passes every row 16..R-1 and returns exactly the published pair (x = M', y = M)
li, Xw, Yw, n3b = D.step3(D.Sc(), P, pr['cv'])
ok('step3_reproduces_published_pair', li is not None and Xw == pr['mp'] and Yw == pr['m'], [li, n3b])
# 8. (37 steps) the code of the organizer experiment d1-q3-smc: the bit-serial row-16 count gives smc.py's per-l counts
#    (Section 6.2) and, for l = 7, 4,096 distinct draws that all pass row 16; F7 and F6 split into affine spaces of
#    exactly |F7| and |F6| words and 4,096 draws from each lie in the set; one replicate on a fixed seed reproduces its
#    recorded estimate, and every rebuilt pair is a 37-step semi-free-start collision under the repository verifier
if R == 37:
    XL = D.xlist(R); V16 = D.row16(P, XL)
    ok('q3x_row16_counts', [x[3] for x in V16] == [0, 16384, 0, 16384, 32768, 8192, 32768, 4096, 65536, 49152, 65536, 49152,
       32768, 57344, 32768, 59392, 0, 16384, 0, 16384, 32768, 16384, 24576, 12288, 65536, 49152, 65536, 49152, 32768, 49152,
       45056, 55296], sum(x[3] for x in V16))
    c_, by_, memo_, n_ = V16[7]; es = set(); b16 = 0
    for r_ in range(n_):
        e_ = D.unrank(c_, by_, memo_, r_); p_ = D.particle(P, P['Lstar'][7]); es.add(e_)
        for w_, k_ in zip(p_, c_): w_[16] = (e_ + k_) & D.M32
        b16 += not D.rowok(P, XL, p_, 16)
    ok('q3x_row16_l7_draws', len(es) == n_ == 4096 and b16 == 0, [len(es), b16])
    for k, d_, t_, F in ((7, P['d7'], P['t7'], P['F7']), (6, P['d6'], P['t6'], P['F6'])):
        Fp = D.fparts(d_, t_); rnd = random.Random(k)
        ok('q3x_F%d_affine_parts' % k, Fp[1] == F and all(D.inF(D.fdraw(Fp, rnd.randrange(Fp[1])), d_, t_) for _ in range(4096)),
           [[len(x[2]) for x in Fp[0]], Fp[1]])
    z, st, hits, prs, bad = D.mini_smc(P, XL, (V16, D.fparts(P['d7'], P['t7'])), random.Random(1), D.Q3X['NP'], D.Q3X['MS'], D.Q3X['MT'])
    ok('q3x_replicate_seed1', abs(math.log2(z) + 74.33085630132217) < 1e-9 and hits == len(prs) == 56 and bad == 0,
       [round(math.log2(z), 6), hits, bad])
    if hf: ok('q3x_pairs_sfs_repo_verifier', all(v(cv, wx) == v(cv, wy) and wx != wy for cv, wx, wy in prs), len(prs))
# 9. the ledger
led = cert.ledger(R)
res['ledger'] = dict((k, led[k]) for k in ('log2_p_model', 'NG', 'log2_N', 'N_times_p', 'vbar', 'VMAX', 'log2_T', 'time_log2',
                                           'preprocessing_log2', 'success_lower_bound', 'log2_hoeffding_exponent'))
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

<!-- file: SEEDS_37.txt sha256=7dff39b082f8759e6973e07dec7cdaeaac9183286bd28b225b50c4b56fae3d52 -->
```text
3001r
3002r
3003r
3004
3005
3006
3007
3008
3009
3010
3011
3012
3013
3014
3015
3016
3017
3018
3019
3020
3021
3022
3023
3024
3025
3026
3027
3028
3029
3030
3031
3032
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

<!-- file: grouprate.c sha256=c73906bbf0aa4bdbe4c97ba5f22ee8c8a9fa9f137fbb7f324568f99634d12ce4 -->
```c
/* grouprate.c - local H1 evidence (proof.md Section 9.1): Step-2 rates on the attack's own grouped first blocks.
   Each group draws W0..W14 (xoshiro256**, seeded), lane l of batch k has W15 = (l << 29) + k (k < K); every trial
   is the full R-step compression from the IV with feed-forward (no shortcut).  Counts W7 passes, valid lanes
   (W7 and, for 37 steps, W6 in their exact sets) and batches with >= 1 and >= 2 valid lanes.
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
0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2};
static const uint32_t IV[8] = {0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19};
#define ROR(x,n) (((x) >> (n)) | ((x) << (32 - (n))))
#define S0(x) (ROR(x,2) ^ ROR(x,13) ^ ROR(x,22))
#define S1(x) (ROR(x,6) ^ ROR(x,11) ^ ROR(x,25))
#define s0(x) (ROR(x,7) ^ ROR(x,18) ^ ((x) >> 3))
#define s1(x) (ROR(x,17) ^ ROR(x,19) ^ ((x) >> 10))
static int R; static long G, KB; static uint64_t SEED; static int NT;
static uint32_t c7, d7, t7, c6, d6, t6, k3, A1, A0, E5, E4;
static uint64_t rotl(uint64_t x, int k) { return (x << k) | (x >> (64 - k)); }
static uint64_t nxt(uint64_t *s) { uint64_t r = rotl(s[1] * 5, 7) * 9, t = s[1] << 17; s[2] ^= s[0]; s[3] ^= s[1]; s[1] ^= s[2];
  s[0] ^= s[3]; s[2] ^= t; s[3] = rotl(s[3], 45); return r; }
typedef struct { int id; uint64_t trials, w7, valid, b1, b2; } job;
static void *work(void *arg) {
  job *j = arg; uint64_t s[4] = {SEED ^ 0x9e3779b97f4a7c15ull * (j->id + 1), SEED + j->id, 0x1234567ull * (j->id + 3), 0xabcdefull + j->id};
  for (int i = 0; i < 20; i++) nxt(s);
  for (long g = j->id; g < G; g += NT) {
    uint32_t w0[16]; for (int i = 0; i < 15; i++) w0[i] = (uint32_t)nxt(s);
    for (long k = 0; k < KB; k++) { int nv = 0;
      for (int l = 0; l < 7; l++) {
        uint32_t w[64]; for (int i = 0; i < 15; i++) w[i] = w0[i]; w[15] = ((uint32_t)l << 29) + (uint32_t)k;
        for (int i = 16; i < R; i++) w[i] = s1(w[i-2]) + w[i-7] + s0(w[i-15]) + w[i-16];
        uint32_t a=IV[0],b=IV[1],c=IV[2],d=IV[3],e=IV[4],f=IV[5],gg=IV[6],h=IV[7];
        for (int i = 0; i < R; i++) { uint32_t t1 = h + S1(e) + ((e & f) ^ (~e & gg)) + K[i] + w[i], t2 = S0(a) + ((a & b) ^ (a & c) ^ (b & c));
          h = gg; gg = f; f = e; e = d + t1; d = c; c = b; b = a; a = t1 + t2; }
        uint32_t am1 = a + IV[0], am2 = b + IV[1];
        uint32_t W7 = c7 - am1; int p7 = (uint32_t)(s0(W7 + d7) - s0(W7)) == t7; j->trials++; j->w7 += p7;
        int ok = p7;
        if (ok && d6) { uint32_t E3 = k3 + am1, mj = (A1 & A0) | (am1 & (A1 | A0)), iv = (E5 & E4) ^ (~E5 & E3);
          uint32_t W6 = c6 - am2 + mj - iv; ok = (uint32_t)(s0(W6 + d6) - s0(W6)) == t6; }
        j->valid += ok; nv += ok; }
      j->b1 += nv >= 1; j->b2 += nv >= 2; } }
  return 0; }
int main(int argc, char **argv) {
  R = atoi(argv[1]); G = atol(argv[2]); KB = atol(argv[3]); SEED = strtoull(argv[4], 0, 10); NT = atoi(argv[5]);
  if (R == 37) { c7=0xd296fb78; d7=0xfbc00800; t7=0x017f8000; c6=0xf538a8f7; d6=0x20000000; t6=0x03c00800; k3=0x2d5dc689;
    A1=0x62827866; A0=0x1b21ce20; E5=0xe7f2c81f; E4=0x1b2d044e; }
  else { c7=0x8f6c89c5; d7=0x20000000; t7=0x03bff800; d6=0; }
  pthread_t th[64]; job jb[64];
  for (int i = 0; i < NT; i++) { jb[i] = (job){i, 0, 0, 0, 0, 0}; pthread_create(&th[i], 0, work, &jb[i]); }
  uint64_t T = 0, w7 = 0, v = 0, b1 = 0, b2 = 0;
  for (int i = 0; i < NT; i++) { pthread_join(th[i], 0); T += jb[i].trials; w7 += jb[i].w7; v += jb[i].valid; b1 += jb[i].b1; b2 += jb[i].b2; }
  printf("{\"R\":%d,\"groups\":%ld,\"batches_per_group\":%ld,\"seed\":%llu,\"trials\":%llu,\"w7_pass\":%llu,\"valid\":%llu,\"batches_ge1\":%llu,\"batches_ge2\":%llu}\n",
    R, G, KB, (unsigned long long)SEED, (unsigned long long)T, (unsigned long long)w7, (unsigned long long)v, (unsigned long long)b1, (unsigned long long)b2);
  return 0; }
```

<!-- file: PREREG_q3x.txt sha256=e8e6825bb4e23f5e298f17a809f119469dbea16c50621748dc1cf4b9b48f2c36 -->
```text
Organizer experiment d1-q3-smc-r37 (sha256-r37 d1 package, fix 2): design frozen 2026-10-08T22:05:55Z before any validation run and
before the organizer's public-seed request was computed or run.
Program: d1core.py sha256 68350927da786f13a7b767140dd2d7d4aa57ace82a59b3846d545232a3fd35d9 (65424 bytes; the attack, the counted
program, cert inputs, tables_digest and the first-block experiment are unchanged from 0126e311...; this version adds
only the q3 experiment section, the dispatch of __main__ on the experiment id, the imports and two header lines).
Estimator (d1core.mini_smc; the proposals and checks of smc.py): row 16 exact, by a bit-serial count over E16^x for
each of the 32 elements of L* (1,052,672 passing words, the per-l counts of smc.py's enumeration) and uniform draws
among them; rows 17..21 sampled with smc.py's proposals and exact weights 2^-f, multinomial resampling of NP survivors;
tail: W22 proposed (cells and W22 two-bit conditions), W7 drawn exactly uniformly from F7 (F7 split into 2 disjoint
affine spaces, one per carry pattern of w + d7, total 68,157,440 = |F7|), W6 implied, weight 1{W6 in F6} 2^(32-f)/|F6|,
rows 22..36 deterministic.  Every tail success is rebuilt (W0..W7 by the inverse expansion, CV1 by inverting steps 7..0
from S) and accepted only if the reference 37-step compression collides from CV1, M1 != M1', ref_words(CV1) = W0..W7,
W7 in F7, W6 in F6 and every cell of rows -4..36 holds except the XOR cells of W6/W7.
Parameters (d1core.Q3X): K = 20 replicates (trials 0..19), NP = 64, children per particle 4 (rows 17, 18) and 1 (rows
19..21), MT = 512 tail proposals per particle, POOL_LOG2 = -74.35.  Seeds: trial t < 20 uses
random.Random(SHAKE-256('d1-q3' || bytes of the organizer's trial seed)); trials 20..255 use no randomness.
Rule: trial t < 20 returns its first rebuilt pair (CV1 || M1, CV1 || M1', 96 bytes each) iff it has >= 1 tail success
and every success is a verified 37-step semi-free-start collision; trial 20 returns the last pair of trial 19 iff all 20
replicates passed and the mean of the 20 estimates is >= 2^-74.35; trials 21..255 return no pair.
Predicted: 21 returned pairs, 0 full collisions (the strings are semi-free-start collisions from CV1, not collisions
from the IV), failed_rebuilds 0 in every trial, row16_words 1052672 in every replicate trial.
How the parameters were chosen: K, NP, MT and the children per particle mirror d1-q3-smc-r38 (r37's rows 17..21 have
the stage factors of r38's rows 18..22; r37's 2^-17 row is row 16, which is exact here).  Development runs of the
identical estimator (d1core.py f33099229ee71e11066dfaed9c8b4c717c8851b5b37bcbc39e9b9049b02eb45a, which differs from the
frozen program only in POOL_LOG2; dev/q3dev.py 8181953f0175b4dfdc1511a9d06352637713b9cce8501061ca73fa3f56e5f856,
random.Random(seed), seeds 1..3 and 10001..10256; runs/q3dev/dev_all.jsonl
f223d698e1314b0965038c334b7882a345bbff3bbc058f1e5a611418deb96caa) gave a mean of 2^-73.9889, a per-replicate relative sd
of 0.246 and 17,946 tail successes, all verified.  A bootstrap of the mean of 20 (2,000,000 resamples, numpy
default_rng(20261009)) put its 0.0001 quantile at 0.804 times the mean (-0.314 bit), i.e. 2^-74.306 after shifting to
the preregistered SMC mean 2^-73.9916 (PREREG_v2.txt); the threshold is that value rounded down to a multiple of 0.05
bit: -74.35.  Under the same bootstrap the pooled rule fails with probability 1.3e-5 if q3 = 2^-73.9916, 2.9e-5 if
q3 = q3_model = 2^-74.01, 0.033 if q3 = 2^-74.20, 0.51 if q3 = 2^-74.35, 0.974 if q3 = 2^-74.50, 0.9994 if q3 = 2^-74.60.
Planned runs, all reported: (1) validation: run_q3x_val.py (sha256
fb90caa8e3d9c97a7adc0bd24e22514b2166e03e84a3471ff47ccce27527faf6) on requests 0..50 (51 x 20 replicates, own seeds
sha256('d1-q3x37-val-<r>-<t>')), 8 processes under the heavy-job lock with nice -n 10; (2) local runs of the organizer
public-seed requests of both experiments (run_exp_org.py sha256
2b58b11313e9606de7c165cf9a005e7ea956f1b4e26138904335198d340650c5; seed protocol of experiments/runner.py, public seed
'hashsmash-public-seed-v1', no holdout nonce) under Python 3.9 and 3.12, plus /usr/bin/time on the q3 request, to check
the deterministic gate, the run time (limit 20 s) and the memory (limit 128 MB).
Use of the validation (decided now): it is reported in full.  Its 1,020 estimates are pooled with the 32 preregistered
SMC estimates by inverse-variance weights (each sample: mean and standard error of its estimates, linear scale); if the
one-sided 99% normal bound of the pooled mean is >= 2^-74.01, q3_model = 2^-74.01 and the claim stay; otherwise
q3_model becomes that bound rounded down to 0.01 bit and the ledger is recomputed exactly with cert.py.
```

<!-- file: run_q3x_val.py sha256=fb90caa8e3d9c97a7adc0bd24e22514b2166e03e84a3471ff47ccce27527faf6 -->
```python
#!/usr/bin/env python3
# run_q3x_val.py - validation of the organizer experiment d1-q3-smc-r37 on our own seeds (proof.md Section 10.2).
# Runs d1core.q3_experiment on synthetic 256-trial requests whose trial seeds are sha256('d1-q3x37-val-<r>-<t>'),
# r in [R0, R1), exactly as the organizer runner passes a request; one JSON line per request.
# usage: run_q3x_val.py R0 R1 > out.jsonl
import sys, json, hashlib, time
import d1core as D
R0, R1 = int(sys.argv[1]), int(sys.argv[2])
for r in range(R0, R1):
    req = dict(schema_version=1, experiment_id='d1-q3-smc-r37', target_profile='sha256-r37-prefix-v1',
               event={'kind': 'full-collision'}, max_message_bytes=4096,
               trials=[dict(trial=t, seed=hashlib.sha256(b'd1-q3x37-val-%d-%d' % (r, t)).hexdigest()) for t in range(256)])
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

<!-- file: run_exp_org.py sha256=2b58b11313e9606de7c165cf9a005e7ea956f1b4e26138904335198d340650c5 -->
```python
#!/usr/bin/env python3
# run_exp_org.py - local emulation of the organizer requests of the d1 r37 package's experiments with the public
# seed protocol of experiments/runner.py (seed 'hashsmash-public-seed-v1', no holdout nonce, 256 trials): builds
# the request exactly as _python_result does, runs d1core.py twice (python3 -B -s), compares stdout bytes,
# recomputes the target digest of every returned pair with the repository verifier, and summarizes.
# usage: REPO_ROOT=... run_exp_org.py OUT.json
import os, sys, json, hashlib, subprocess, time
REPO = os.environ['REPO_ROOT']; sys.path.insert(0, REPO)
from verifier.frontier_tracks import get_frontier_track
from verifier.hash_functions import digest
from verifier import hash_functions as hf
tr = get_frontier_track('sha256-r37-exploratory'); R = 37
def canon(v): return json.dumps(v, sort_keys=True, separators=(',', ':'), ensure_ascii=True, allow_nan=False).encode()
cfg = tr.config_sha256()
sm = canon({"domain": "hashsmash-experiments-v1", "seed": "hashsmash-public-seed-v1", "holdout_nonce": None, "target_config_sha256": cfg})
res = dict(track=tr.id, profile=tr.profile_id, target_config_sha256=cfg, python=sys.version.split()[0],
           program_sha256=hashlib.sha256(open('d1core.py', 'rb').read()).hexdigest())
for eid in ('d1-first-block-r37', 'd1-q3-smc-r37'):
    req = {"schema_version": 1, "experiment_id": eid, "target_profile": tr.profile_id, "event": {"kind": "full-collision"},
           "max_message_bytes": 4096, "trials": [{"trial": i, "seed": hashlib.sha256(sm + canon([eid, i])).hexdigest()} for i in range(256)]}
    rq = canon(req) + b"\n"; t0 = time.time()
    o1 = subprocess.run([sys.executable, '-B', '-s', 'd1core.py'], input=rq, capture_output=True, check=True).stdout; dt = time.time() - t0
    o2 = subprocess.run([sys.executable, '-B', '-s', 'd1core.py'], input=rq, capture_output=True, check=True).stdout
    out = json.loads(o1); rows = out['trials']; ret = [r for r in rows if r['message_a_hex'] is not None]
    full = sum(1 for r in ret if r['message_a_hex'] != r['message_b_hex'] and
               digest(bytes.fromhex(r['message_a_hex']), 'sha256', R) == digest(bytes.fromhex(r['message_b_hex']), 'sha256', R))
    pairs = [hashlib.sha256(canon(sorted([r['message_a_hex'], r['message_b_hex']]))).hexdigest() for r in ret]
    s = dict(sec=round(dt, 2), byte_identical=o1 == o2, request_sha256=hashlib.sha256(rq).hexdigest(),
             stdout_sha256=hashlib.sha256(o1).hexdigest(), stdout_bytes=len(o1), returned=len(ret), full_collisions=full,
             repeated=len(pairs) - len(set(pairs)), max_obs=max(len(r.get('observations', {})) for r in rows))
    if eid == 'd1-first-block-r37':
        s.update(mismatches=sum(r['observations']['mismatches'] for r in rows), valid=sum(r['observations']['valid'] for r in rows),
                 lanes=sum(r['observations']['lanes'] for r in rows))
    else:
        K = 20; s.update(witness=sum(1 for r in rows[:K] if r['message_a_hex']), pooled_pass=rows[K]['message_a_hex'] is not None,
                         pooled_log2=rows[K]['observations']['log2_pooled_mean'], log2=[r['observations']['log2_estimate'] for r in rows[:K]],
                         tail=sum(r['observations']['tail_successes'] for r in rows[:K]), verified=sum(r['observations']['verified_pairs'] for r in rows[:K]),
                         failed=sum(r['observations']['failed_rebuilds'] for r in rows[:K]))
        # independent check of the returned semi-free-start collisions with the repository compression
        sfs = 0
        for r in ret:
            a, b = bytes.fromhex(r['message_a_hex']), bytes.fromhex(r['message_b_hex'])
            cv = tuple(int.from_bytes(a[4*i:4*i+4], 'big') for i in range(8))
            if a[:32] == b[:32] and a[32:] != b[32:] and hf._compress('sha256', cv, a[32:], R) == hf._compress('sha256', cv, b[32:], R): sfs += 1
        s['sfs_collisions_repo_verifier'] = sfs
    res[eid] = s
open(sys.argv[1], 'w').write(json.dumps(res, indent=1)); print(json.dumps(res, indent=1))
```
