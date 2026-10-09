# Collision attack on 38-step SHA-256 (ePrint 2026/1120, counted, fixed caps, bit-sliced first blocks, solved first-block family): 2^99.91651

**Track** sha256-r38-exploratory, target sha256-r38-prefix-v1, cost model collision-frontier-v5 (C = 2728).
**Claim** time_log2 = 99.91651 (the exact total is 2^99.9165035 target compressions; the claim is the smallest
k / 10^5 not below log2 T, computed with an 80-digit logarithm), success probability at least 0.39 (the bound is
0.3900000050), memory 2^95 bytes (a word-RAM bound covering every charged computation, conditional on the advice
allowances H4; Section 13), preprocessing 2^78.08755, nonuniform advice 2^13 bytes.

**Credit.**  The attack, its 38-step differential characteristic and the semi-free-start (SFS) pair are those of
Yingxin Li, Zhuolong Zhang, Muzhou Li, Fukang Liu, Haifeng Qian and Jinwei Zhu, *Pushing Collision Attacks on
SHA-2 to 39 Steps*, IACR ePrint 2026/1120 (CC BY).  Its two-block, memory-efficient meet-in-the-middle framework is
[LLWS26]: Yingxin Li, Fukang Liu, Gaoli Wang and Jiali Shi, *Pushing the limit of memory-efficient collision attack
framework for SHA-2*, ePrint 2026/1080 (CRYPTO 2026).  The characteristic was found with the SAT/SMT tool of
[LLW24a]: Yingxin Li, Fukang Liu and Gaoli Wang, *New records in collision attacks on SHA-2*, EUROCRYPT 2024.
This package (q38c; its source files call it r38fam) is winglock's and continues our packages d1 (submission
20a43626) and d2 (3d819a4b), whose transcription and checks of the characteristic, Step-1 solution S, exact Step-2 sets and freedom set L*, counted
scalar Step 3, preregistered Monte-Carlo estimate of the Step-3 probability and q3 organizer experiment it keeps
unchanged, and our unsubmitted bit-sliced build q38 (the 38-step circuit with stage 3a inside it).  It is built on
the work of other solvers, each declared as a dependency:

- **leech1996, b99301f4** (this track): the corrected success and work-cap argument for d2 after its review (H1 for
  one trial at a time, the exact independence of groups, the within-group pair premise H5 with a Bonferroni bound,
  Hoeffding over groups, the cap test charged where it runs).  Sections 7 and 9 and `cert.py` follow it.
- **Th0rgal, dd6656d4** (sha256-r37): the bit-sliced circuit code reused here (signed-literal gate network with
  5-gate full adders, column-compression adders, group-constant gates hoisted into the group setup, furthest-next-use
  register allocation over 64 registers with every load and store counted, the gate-by-gate evaluator, the inlining
  of schedule words without later use, and the test of the Step-2 set as factored parity checks).  It extends
  **0xshikhar, ad9745bf** (sha256-r37), the first bit-sliced first-block batch for this attack, which credits
  **Th0rgal 64bca7e2**, **jaazinn 817d444c**, **mitchuski fca38c6d** and **0xshikhar 6de1b685** for the bit-sliced
  techniques; 64bca7e2 in turn credits **mitchuski 875a5083 and f153f574**.
- **Th0rgal, 882f372f and 349e3a6a** (this track; the "PR #674" line cited in the source comments): the tail of the circuit after step 37 - the factored 22-gate W7
  filter for (d7, t7) = (2^29, 03bff800) (we check it against the definition on all 2^32 words, `f7check.c`), W0
  folded into one 31-bit E16 column, ~E35 in W1 with IV6 in the constant, and the T1 reuse for e1/a1.
- **0xshikhar, d5a10596** (this track): the shared S0(a1) + MAJ(a1, a2, a3) adder used by the E0 and E16 columns
  (credited by 349e3a6a).
- **leech1996, efd8aa9d** (sha256-r37): the cap test executed only on batches that enter the rare path, where its
  charge sits, and a charge for building the circuit (PRE_BUILD).
- **GordoAR, 20dbd783** (this track): another bit-sliced r38 filing on the same basis; cited as a precedent for the
  pricing (H3).  No code or constant is taken from it.
- Earlier SHA-256 filings: fixed caps with a halting counter (6eeefb64) and the grouped first-block family
  (6b88bdb7), as credited by d1/d2.

What is new in this package against q38 (the family and variant technique come from our own unsubmitted sha256-r37
build q37, re-searched for 38 steps): a **solved first-block family** (per group 8 random words of W0..W14 and 7
words solved so that W20 = -K20 and the group-constant parts of W17, W19, W21, W22, W23 and W24 vanish; 20 instead
of 29 group-constant words reach the circuit; Section 4.6); **32 straight-line variant programs** per group (the top
5 bits of W15 folded into each as literals, everything that does not depend on the lane hoisted into the group
setup); the ported tail; the accounting fixes of our internal review of q38 (V and the counters in memory, average
form of H5, a 9/8 work-cap margin, exact rounding); the measurement `grp38fam.c` of H1 and H5 on the new family
(2^32 full 38-step compressions; Section 9); and a first-block organizer experiment for the new program, its design
frozen in `PREREG_fb.txt` (Section 10.1).  None of the credited solvers has reviewed this package; mistakes are ours.

## 0. Summary

- **Algorithm (Section 4, unchanged from d2).**  Two-block messages M0 || M1 and M0 || M1' (128 bytes each; FIPS
  padding appends the same third block).  Step 1 is the paper's dense-part solution S, read off the published SFS
  pair.  Step 2 searches first blocks M0 until the chaining value CV1 passes the exact filter W7 in F7 (probability
  p2 = 287,309,824 / 2^32 = 2^-3.90197 for a uniform CV1).  Step 3 tries the single element of the exact freedom set
  L* and checks every cell of rows 16..37 (stage 3a: the ten x-value cells of E16; stage 3b: rows 16..37 with early
  abort).  A pair that passes every cell collides; it is verified with the target and output.
- **Program (Section 5).**  First blocks are evaluated 256 at a time as bit planes (bit L of a 256-bit word belongs
  to first block L).  A group draws two random words: the 8 free words of the family, the lane offset rL and the
  start variant rb; lane L of batch k uses W15 = ((L ^ rL) << 9) | (v << 27) with v = (rb + k) mod 32; a group has
  32 batches (m = 8,192 first blocks), and batch k runs the straight-line **variant program** v.  The 32 variant
  programs (rounds 15..37, CV1, the W7 test and stage 3a for 256 lanes, the fail-plane test) cost exactly
  **1,398,573 operations** together (43,617..43,742 each, 43,705.41 on average), and the group setup 6,378 plus 10
  for group control: **171.504 operations per first block** (q38: 191.44; b99301f4: 218.14).  A lane leaves the
  circuit (is *flagged*) only if it passes W7 and stage 3a; the scalar rare path (CV1 recomputation and Step 3) runs
  on 0.0167 lanes per batch on average.  Every count is produced by the shipped program (Appendix A) and is
  data-independent.
- **Probability (Section 6, unchanged).**  p_model = p2 |L*| q3_model kappa = 2^-104.92197 per first block, with
  q3_model = 2^-101.02 from d2's preregistered sequential Monte-Carlo estimate (H2) and its organizer replica.
- **Caps and success (Section 7).**  Groups are independent (fresh coins); inside a group only the average pair
  bound H5 (2^-30) is used, through Bonferroni: Pr[a group succeeds] >= q_lb = 2^-91.92197.
  N_G = 2,318,775,195,457,330,464,467,753,076 groups (N = 2^103.90542 first blocks) with N_G q_lb >= 0.49429633, and
  all data-dependent work is capped by V <= V_MAX = 5,900,978,306,751,612,076,067,042,015,150 operations (halt on
  overflow; margin 9/8 over the per-lane expectation; Hoeffding over the groups), so
  Pr[success] >= 1 - e^-0.49429633 - exp(-2^58.11) - 2^-60 = 0.3900000050 under H1, H2 and H5.
- **Ledger (Section 8).**  T = A_C + A_S + DEV + (pre + init + online + rare + fin_ops) / C + 6 =
  3,263,690,571,759,872,834,848,962,656,197,285 / 2,728 units = 2^99.9165035, claimed as **99.91651**.  Online
  2^99.91389, rare 2^90.80517, the allowances together 2^78.09 (unchanged from d2: A_S = 2^74, A_C = 2^78, DEV = 2^64).
- **Heuristics (Section 9).**  H1 the chaining value of each single trial behaves as uniform (score-critical; also
  gives the stage-3a rate used for the work cap), H2 the Step-3 probability (score-critical, unchanged), H3
  bit-sliced word pricing (score-critical, precedent), H4 the advice allowances (supporting, unchanged), H5 an
  average pair bound for the trials of one group (score-critical).  Nothing else: no expected-work bound, no
  independence inside a group, no independence-of-conditions model.
- **Checks.**  The self-test (Appendix A) reproduces the published pair's collision under our code and the repository
  verifier, every cell, S, L and L*, the preregistered `tables_digest`, the family constraints, the exact counts,
  76,800 lanes of the circuit's evaluator against the verifier (every lane's W7 and flag decisions), 2,048 further
  batches on the flag path, all 32 counted variant programs (`run_vm`) on 2 groups (16,384 lanes) against the
  verifier, Step 3 recovering the published pair, the q3 replica and the ledger.  `grp38fam.c` measured H1's rates and
  H5's within-group dispersion on 2^32 first blocks of the new family (524,288 complete groups); `f7check.c` checks
  the factored W7 test on all 2^32 words.  Two organizer experiments run the shipped program on organizer seeds: the
  first-block check (H1, H3, H5) and the q3 replica (H2).

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
*Proof.* Substitute the equations; each step is inverted for its new coordinate.  The self-test checks the
reproduction on every W7 lane of its 76,800 lanes (5,239 chaining values).

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

Step 3 tests, in the order of L*: **stage 3a** - E16 = c16_l + k16_l + s0(W1) + W0 against the ten x-value cells of
row 16 (bits 30, 27, 26, 22, 17, 16, 12, 11, 9, 7: mask 4c431a80; the `+` cells of row 16 pair with row 17 and are
checked in stage 3b); **stage 3b** - both members' rows 16..37, one row at a time,
every cell of the row, abort at the first failing row.  Stage 3a only tests cells that F_l requires, so the early
abort never discards an element of F_l.  The first l that passes every row is verified with the target (Section 4.6).
In this package stage 3a is evaluated twice: for all 256 lanes of a batch inside the counted variant program (Section
5.2, from the batch's own chaining values), and again by the counted scalar Step 3 for every lane the circuit flags.

### 4.6 The first-block family and the algorithm (fixed caps)

**Family (`d1core.FAM`, `family`).**  A group draws two uniform 256-bit words r0, r1.  The eight 32-bit fields of
r0 are W0, W1, W2, W3, W4, W9, W11, W14; rL = bits 0..7 of r1 and rb = bits 8..12 of r1.  The other seven words of
W0..W14 are solved, in this order, from the words already known (each a counted subtraction chain on the scalar
machine):

| solved word | constraint (inside every group) |
|---|---|
| W10 | the group-constant part of W17 is 0, so W17 = s1(W15) |
| W12 | the group-constant part of W19 is 0, so W19 = s1(W17) |
| W8 | the group-constant part of W24 is 0, so W24 = s1(W22) + W17 |
| W7 | the group-constant part of W23 is 0 (W16 + s0(W8) + W7 = 0) |
| W6 | the group-constant part of W22 is 0, so W22 = W15 |
| W5 | the group-constant part of W21 is 0, so W21 = s1(W19) |
| W13 | W20 = -K20 (so W20 + K20 = 0 in step 20; s0(W20) and W20 + K36 are literals) |

So 20 group-constant words remain for the circuit (q38: 29), and several schedule words are literals or cheaper
functions of W15.  The family was chosen among 17 candidate constraints (W16 or W18 = 0, W20 in {0, -K20, -K36,
-K20 - K36}, the zero constant parts of W17, W19, W21..W30) by a greedy and swap search scored with the emitted
operation count, jointly with the lane offset (bits 9..16) and the number of batch bits (5); this development is
charged under DEV (Section 9, H4).  For a fixed lane L and batch position k, one trial's first block is uniform
over a set of 2^(256 + 8 + 5) = 2^269 distinct blocks (the 8 free words, rL and rb), and since rL and rb are
uniform, every trial position (L, k) has exactly the same distribution; H1 is a statement about this distribution.
The family holds by construction (each solved word is computed exactly from its constraint).  The Python `assert`
in `group_setup` is a reference self-check of the implementation, not part of the counted program; the constraints
are also checked on the scalar schedule of every checked lane of the organizer experiment and on every trial of
`grp38fam.c`.

```text
input: N_G (groups), V_MAX (operations); coins: uniform 256-bit words
V = 0
for g = 0 .. N_G - 1:                                   # group control GCTRL = 10
    draw r0, r1; solve the family; rL, rb; rounds 0..14, the 20 group-constant words and their planes, the lane
    planes of L ^ rL, the 721 hoisted gates (Section 5.3)
    for k = 0 .. 31:                                    # straight line: rotated sequence rb (no batch loop)
        v = (rb + k) mod 32; lanes L = 0..255 use W15 = ((L ^ rL) << 9) | (v << 27)
        run variant program v: rounds 15..37, CV1, the W7 test and stage 3a of the 256 lanes -> fail plane
        if some lane is flagged (fail plane != all ones):     # compare + branch: part of the variant's count
            rare path (counted into V): load V, scan, for each flagged lane: CV1 recomputed on the scalar machine;
            Step 3 (stages 3a, 3b) over L*
                if l passes every row: compute both 128-byte messages and their digests with the target
                    (6 compressions); if they are distinct and equal: output (m, m') and halt
            V += (this batch's rare-path operations); if V > V_MAX: halt (failure); store V; return
halt (failure)
```

This is the driver `attack` of `d1core.py`.  **The cap test is inside the rare branch** (as in efd8aa9d): V changes
only there, so V can first exceed V_MAX only right after an update, and the test runs exactly once per batch that
enters the rare path.  Every register can be live inside a variant program (Section 5.5), so V and the group counter
g are kept in memory: VCTRL = 6 per rare batch (load V, add, compare with V_MAX, branch, store V, return jump into
the variant sequence) and GCTRL = 10 per group (load g, add, store g, compare, branch; dispatch to rotated
sequence rb: shift, add, load, branch; the return jump at the end of that sequence).  The program holds 32 rotated
straight-line sequences: sequence s is the variant programs v = s, s + 1, ..., s + 31 (mod 32) followed by a direct
return jump to the group loop, so a group runs its 32 batches without a batch loop and without any data-dependent
test at the group end.  Each of the 1,024 variant copies branches to its own copy of the scalar rare-path code, in
which v, the return address (the next copy, or the group-loop return after the 32nd) and the position are
immediates (the rare path nevertheless charges a load of the batch index and of the mask in `lane_cv`).  The code
size is accounted in Section 13.  A batch
without a flagged lane executes only its variant program, including the fail-plane test (compare + branch).
Every run executes at most N_G group setups, 32 N_G variant programs, V_MAX + vmax rare-path operations and one
verification, whatever the coins (Section 8).  There is at most one verification because the first one always
succeeds: a pair that passes stage 3b has equal second-block outputs (Lemma 4), and M1 != M1' because W7 differs by
d7 != 0, so the run outputs and halts.

## 5. The counted program

### 5.1 Machine and pricing

A 256-bit word RAM with 64 registers.  Primitives: AND, OR, XOR, ADD/SUB (mod 2^256), SHR, SHL, LOAD, STORE,
compare, branch, RAND; each executed instance costs one operation; immediates and shift amounts are instruction
fields.  In a variant program a 256-bit word is a *plane*: bit L belongs to first block L, and a 32-bit SHA-256 word
of the 256 first blocks is 32 planes.  Every intermediate is a signed literal (a stored plane and a compile-time
polarity), so NOT, rotations and constant shifts are free renamings; only AND, OR and XOR gates, loads, stores and
the fail-plane test are executed.  The scalar machine of the group setup, the rare path and Step 3 is d2's: one
32-bit value per word, rotations via the doubled word x | x << 32, S0, S1, s0, s1 at 8 operations each.

### 5.2 The variant programs: 1,398,573 operations per group of 32 x 256 first blocks

`build(R, v)` in `d1core.py` generates the circuit of variant v (the 5 batch bits of W15 are the literal bits of v);
`emit` allocates it onto the 64 registers; `run_vm` executes the resulting straight-line program and counts every
instruction.

- **Inputs** (in memory, written by the group setup).  Group-constant planes (each all-zeros or all-ones): the 20
  words that depend only on the group (the state after round 14, the non-zero group-constant schedule parts and the
  sums, S0/S1/s0/s1, Ch or Maj of such words that the circuit needs, with K_t folded in); the 8 lane planes (bit L of
  plane i is bit i of L ^ rL: W15 bits 9..16); the 721 hoisted gates (every gate whose inputs are group constants or
  lane planes only, which is therefore the same in all 32 variants of a group); the all-ones plane.  W15 bits 0..8
  and 17..26 are 0; bits 27..31 are the literal bits of v.
- **Gates** (dd6656d4's network).  X & Y, ~X & ~Y = ~(X | Y), X & ~Y = (X ^ Y) & X with the XOR shared; Ch and Maj in
  every polarity (Maj shares an XOR with the previous round); a full adder in 5 gates, 2 with a constant 1;
  column-compression adders mod 2^32 (operands in reversed order, from q37).  Literal inputs (family constants,
  the batch bits) are folded at build time.
- **Rounds 15..37.**  Every round computes A_t and E_t (T1 materialised when it has at least two varying summands).
  The schedule words that depend on W15 and are used again are computed in the round that uses them, in the cheaper
  forms the family gives (W17 = s1(W15), W19 = s1(W17), W21 = s1(W19), W22 = W15, W24 = s1(W22) + W17, W20 + K20 =
  0); W36 and W37, which no later word uses, are added into the round-36 and round-37 adders directly (dd6656d4's
  cut).  Emission is in lock step: for round t and bit j the circuit computes bit j of W_t, T1, E_t and A_t, keeping
  the carry chains open.
- **Chaining value.**  CV1 = (a1, a2, a3, a4, e1, e2, e3, e4) = (A37, A36, A35, A34, E37, E36, E35, E34) + IV.  IV0
  and IV4 are added inside the round-37 adders (with the T1 reuse of 882f372f), which output a1 and e1 directly;
  four constant adders in lock step with round 37 give a2 = A36 + IV1, a3 = A35 + IV2, e2 = E36 + IV5 and
  e3 = E35 + IV6 (e3 is needed inside IF(e1, e2, e3)).  a4 and e4 enter the formulas below only linearly, so A34 and
  E34 are used with IV3 and IV7 folded into constants; in W1, -e3 is taken as ~E35 with IV6 in the constant (882f372f).
- **Step-2 test.**  W7 = c7 - a1 = ~a1 + (c7 + 1).  F7 = {w : s0(w + d7) - s0(w) = t7} is the disjoint union of
  three affine subspaces of GF(2)^32 of dimensions 28, 24 and 21 (`fparts` in `d1aux.py`; 2^28 + 2^24 + 2^21 =
  287,309,824 = |F7|, the exhaustive count of `fcount.c`).  The circuit uses Th0rgal's factored 22-gate form over the
  carry of bit 29 (`fails7`, from 882f372f), which `f7check.c` compares with the definition on all 2^32 words
  (287,309,824 members, 0 disagreements); this gives the plane fail7.
- **Stage 3a.**  With -x = ~x + 1 (NOT is free) the Step-2 equations of Section 4.3 and stage 3a of Section 4.5
  become multi-operand additions and one 10-bit comparison:

  ```text
  Smj = S0(a1) + MAJ(a1, a2, a3)                                     (one adder, used in E0 and in E16; d5a10596)
  E0  = A34 + ~Smj + (A0 + IV3 + 1)                                   = A0 + a4 - S0(a1) - MAJ(a1, a2, a3)
  W1  = ~S1(E0) + ~IF(E0, e1, e2) + ~MAJ(A0, a1, a2) + ~E35 + (A1 - S0(A0) - K1 - IV6 + 4)
                                                                      = E1 - a3 - e3 - S1(E0) - IF(E0, e1, e2) - K1
  W0  = ~IF(e1, e2, e3) + ~E34 + ~S1(e1) + ~Smj + (A0 - K0 - IV7 + 4) = E0 - a4 - e4 - S1(e1) - IF(e1, e2, e3) - K0
  E16 = ck16 + s0(W1) + W0,   fail16 = OR over the bits b of m16 of (E16[b] XOR v16[b])
  ```

  (E1 = A1 + a3 - S0(A0) - MAJ(A0, a1, a2), so a3 cancels in W1; ck16 = fe314838, m16 = 4c431a80 (10 bits), v16 =
  48030280, the constants of the scalar stage 3a.)  W0 is not materialised: its summands enter the E16 column
  directly, which stops at bit 30, the highest bit of m16 (882f372f's fold).  MAJ(A0, a1, a2) has the constant A0
  of S and costs one gate per bit.  The fail plane is fail = fail7 OR fail16: bit L is 0 iff lane L passes W7 and
  stage 3a.  Without stage 3a in the circuit, 256 p2 = 17.1 lanes per batch would go to the scalar path (at least
  1,371 operations each).
- **Test.**  "Some lane flagged" is one compare (the fail plane with the all-ones plane, or with 0 when its literal
  is negated) and a branch to the copy's rare path: 2 operations per variant.

Count (from `d1core.calibrate`: each of the 32 variant programs is run by `run_vm` on the memory images of three
groups, gives the same count each time and the evaluator's fail plane): load 231,494, store 83,090, XOR 851,467,
AND 122,559, OR 109,899, test 32 x 2; total **c_B = 1,398,573** per group (per variant 43,617 .. 43,742, on average
43,705.41 per 256 first blocks = 170.724 per first block).  With the group setup and control (6,388 per 8,192 first
blocks = 0.780) a first block costs 171.504 operations = 2^-3.99153 units.  Spill traffic (loads and stores) is
about 22 % of the count.

### 5.3 Group setup and start-up

Per group (counted on the scalar machine, `group_setup`): two RAND, rL and rb (3), the family (the 8 fields of r0
unpacked by shift and mask, 7 words solved), rounds 0..14 and the group-constant words (shared subexpressions
evaluated once; the family's fixed words and zero sums hold by construction, the `assert` is an uncounted reference
check), their 640 planes (shift, AND 1, subtract from 0,
STORE: 4 operations per plane), the 8 lane planes of L ^ rL (6 each), the 721 hoisted gates (2 loads, 1 gate,
1 store each), the all-ones plane (2) and the stores of M0, rL, rb, A11..A14 and E11..E14 for the rare path:
**c_G = 6,378**, identical over three groups; plus GCTRL = 10 for group control (Section 4.6).  The scalar phase of
the group setup keeps at most 39 values live, so it needs no spill.  Start-up: c_init = 9 plus an allowance of 256.
Building the circuit, the 32 variant programs and their register allocation is preprocessing, charged at
PRE_BUILD = 2^40 operations (Section 8): it takes 6.4 CPU-seconds in CPython on our machine, and the
enumeration of L in `setup` 15.2 CPU-seconds; at the 10^10 primitive operations per CPU-second of H4 both together
are below 2^37.7 operations.

### 5.4 Rare path and Step 3 (counted on the scalar machine)

A batch with a flagged lane executes VCTRL = 6 (Section 4.6), then scans the fail plane: x = fail XOR ones and the
loop test (SCANB = 4), and per flagged lane at most SCANL = 45 (low = x AND (0 - x), x XOR= low, the lane index by
an 8-step binary search, the loop test).  Per flagged lane: VLANE = 1 (the per-lane addition to the rare-path
counter that `attack` keeps), then c_cv = 1,235 (CV1 recomputed from the stored group state: W15, the schedule
words W16..W37 with the family's fixed words as immediates, rounds 15..37 and the feed-forward; the batch index and
mask loads are charged although the copy index is an immediate), then d2's Step 3: c01 = 71 (E0, W0, E1, W1 and
q = s0(W1) + W0), c3a = 9 (stage 3a; it passes, since the circuit computed the same test), FLAG3B = 2 and
V3B = VENT + SPILL3B = 1 + 148 at the stage-3b entry (the V update at its exit; all 64 registers and the
second-block words stored and reloaded), crest = 85 (E2, E3, W2..W7, the y words) and at most c3b = 2,620 (a full
pass of rows 16..37 for both members with every cell check; an early abort costs less).  Per flagged lane at most
45 + 1 + 1,235 + 71 + 9 + 2 + 149 + 85 + 2,620 = 4,217 operations; per rare batch at most
vmax = 6 + 4 + 256 x 4,217 = 1,079,562.  Every operation of this paragraph is counted into V.

### 5.5 Correctness of the counted program

- **Registers.**  `emit` allocates onto registers 0..63 by furthest-next-use eviction and the machine has only those
  64 registers (`calibrate` reports register 63 as the highest used); every load reads a stored value or an input.
  All 64 registers can be live inside a variant program, so nothing is kept in a register across a batch: V, g and
  the scan state are in memory or in registers the finished variant no longer uses.  In the rare path the lane path
  of Step 3 needs at most 15 values besides the scan word, the lane index and V (`rare_liveness` in `d1aux.py`):
  19 <= 64; stage 3b runs after the register-file save and holds at most 52 values, 53 <= 64 with V.
- **Evaluator and counted programs.**  The driver `attack` evaluates a batch with the gate-by-gate evaluator
  `Prog.f`; the counted variant programs are the charged implementation.  Their equality is checked (i) in every
  `calibrate` call: all 32 variant programs (`run_vm`) against the evaluator on three groups' memory images; (ii) in
  the self-test: every lane of all 32 counted variant programs on 2 groups (16,384 lanes) against the repository
  verifier.
- **Bit-exactness against the verifier.**  The self-test checks 300 batches (76,800 lanes) of the evaluator against
  the repository verifier: every lane's W7 decision and flag (W7 and stage 3a), the CV1 of every flagged lane and of
  every 16th lane through the rare path's recomputation, and Lemma 1's reproduction of S from every W7 lane's
  W0..W7 (5,239 W7 lanes, 59 lanes whose E16 misses the ten cells in exactly one bit, 6 flagged lanes,
  0 mismatches); and 2,048 further batches (524,288 lanes) in which every lane the circuit marks as passing W7 or as
  flagged is recomputed with the verifier (35,222 W7 lanes, 356 one-bit misses, 34 flagged lanes, 0 mismatches).
  The organizer experiment repeats the lane checks on its seeds.
- **Step 3 end to end.**  From the published pair's CV, the counted Step 3 derives W0..W7, finds the published
  (W14, W15) in L*, passes every row and returns exactly (M', M) (self-test).

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
31 GB of memory; v2 changed only memory handling and used new seeds; the 8 complete v1 values (Section 12) are r37 values and
agree with v2's r37 sample; no r38 v1 estimate had completed, so no r38 value was discarded from H2's sample.

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
- **A second implementation.**  The q3 replica in `d1core.py` (standard library only, written for d2's fix 1; the
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

The argument is b99301f4's (which replaced d2's): one trial at a time (H1, H2), the exact independence of distinct
groups, and a pair bound inside a group (H5, here in its average form).

- **Events.**  For a trial i (one first block), A_i is the event that its chaining value is valid and the pair of
  the element of L* follows every cell of rows 16..37 (F_l).  The algorithm finds every A_i among the trials it
  tests: the circuit's stage 3a and the scalar stage 3a test only cells that F_l requires, stage 3b checks exactly
  F_l, and F_l implies a collision (Lemma 4).
- **One trial (H1, H2).**  Pr[A_i] >= p_model = p2 |L*| q3_model kappa = 2^-104.92197 (p2 = 2^-3.90197, |L*| = 1,
  q3_model = 2^-101.02, kappa = 1).  This uses the distribution of one trial's chaining value only.
- **Groups are independent (exact).**  Each group draws its own two uniform 256-bit words.  Its trials, their
  outcomes and its rare-path work are functions of those words, so the N_G groups are independent and identically
  distributed.  Inside a group nothing is assumed independent: its 8,192 trials are deterministic functions of 269
  bits.
- **One group (H5, Bonferroni).**  With m = 256 x 32 = 8,192 trials per group, q_g = Pr[some A_i of the group] >=
  sum_i Pr[A_i] - sum_{i<j} Pr[A_i and A_j].  H5 states sum_{j != i} Pr[A_i and A_j] <= (m - 1) 2^-30 sum_i Pr[A_i]
  (an average over ordered pairs, which is exactly what Bonferroni needs), so
  sum_{i<j} Pr[A_i and A_j] <= (m - 1) 2^-31 sum_i Pr[A_i], and q_g >= (1 - (m - 1) 2^-31) m p_model = q_lb =
  2^-91.92197 ((m - 1) 2^-31 = 2^-18.0).
- **Trial cap.**  N_G = ceil(0.49429633 / q_lb) = 2,318,775,195,457,330,464,467,753,076 groups,
  N_B = 32 N_G = 74,200,806,254,634,574,862,968,098,432 batches, N = 256 N_B = 2^103.90542 first blocks
  (N p_model = 0.4942982).  Pr[no group succeeds] = (1 - q_g)^N_G <= exp(-N_G q_lb) <= exp(-0.49429633).
- **Work cap.**  The rare-path operations of a batch, v_b, are at most vmax = 1,079,562 = 10 + 256 x 4,217
  (Section 5.4).  Their expectation is at most vbar = 70.6907958984375, computed from one lane at a time: a lane is
  flagged iff it passes W7 (probability p2) and, given that, stage 3a, whose ten cells of E16 = ck16 + s0(W1) + W0
  match with probability exactly 2^-10 because W0 and W1 are uniform and independent given validity (H1, Lemma 2);
  the expected number of flagged lanes of a batch is 256 p2 2^-10 = 0.0167236 and the union bound gives
  Pr[a batch has a flagged lane] <= 256 p2 2^-10, so no joint distribution of the 256 lanes is needed:
  vbar = 256 p2 2^-10 (10 + 4,217).  V_MAX = ceil((9/8) N_B vbar) = 5,900,978,306,751,612,076,067,042,015,150.  The
  rare-path work of a group lies in [0, 32 vmax] and the groups are independent, so Hoeffding over the N_G groups
  gives Pr[sum v_b > V_MAX] <= exp(-2 ((1/8) N_B vbar)^2 / (N_G (32 vmax)^2)) = exp(-2^58.108).  The margin 9/8
  tolerates a mean flagged rate up to 12.5 % above p2 2^-10 (at an excess of 12.49 % the Hoeffding exponent is still
  2^37.5); `grp38fam.c` observed an excess of +0.28 % (flagged 281,357 against 280,576 expected; the binomial standard
  error is 0.19 %, and the per-group dispersion of the flagged counts about the observed rate is 1.0008, so
  correlation inside groups does not widen it materially; Section 9), far below 12.5 %.
- **Success.**  If the full run would not exceed V_MAX, all N trials are tested.  Hence Pr[output a collision] >=
  1 - exp(-0.49429633) - exp(-2^58.108) - 2^-60 = 0.3900000050 > 0.39 under H1, H2 and H5 (the 2^-60 is kept as
  slack).  Any output is a verified collision (Section 4.6), independently of the heuristics.

## 8. Ledger (exact; `cert.py`)

```text
T = A_C + A_S + DEV + (pre + init + online + rare + fin_ops) / C + fin_units
  A_C = 2^78 (characteristic search), A_S = 2^74 (Step-1 solve), DEV = 2^64 (all development)        [units]
  pre    = (E14 + E15 candidates) x 1024 + 2^20 + PRE_BUILD = 1,102,197,555,200   (L, L*, tables; PRE_BUILD = 2^40)
  init   = c_init + 256 = 265
  online = N_G (c_G + GCTRL + c_B) = N_G (6,378 + 10 + 1,398,573) = 3,257,788,717,384,926,466,689,078,829,410,036
  rare   = V_MAX + vmax = 5,900,978,306,751,612,076,067,043,094,712
  fin    = 6 units + 512 operations (two complete messages, their digests, once)
T = 3,263,690,571,759,872,834,849,993,448,348,325 / 2,728 units = 2^99.91650348513534649...
  -> time_log2 = 99.91651 (the smallest k / 10^5 with 2^(k / 10^5) >= T; 80-digit logarithm, cert.claim5)
preprocessing = A_C + A_S + DEV + pre / C = 2^78.08755
```

The online term is 2^99.91389 units, the rare term 2^90.80517, the three allowances together 2^78.09; everything
else is below 2^29.  The online count includes every variant program's fail-plane test; the cap test and the loads
and stores of V are part of VCTRL in the rare term, and the group counter's in GCTRL (Section 4.6).  The total holds
on every run: the program cannot execute more groups, variant programs, cap tests, rare-path operations or
verifications.  The slack between log2 T and the claim is 6.5 x 10^-6 bit (about 2^82.1 units, or 0.20 operations
per batch); any later accounting change must be re-checked against it.

**Sensitivity** (`cert.ledger` with one input changed and N_G, V_MAX re-derived; the exact log2 T, which a claim
rounds up at the 5th decimal):

| change | log2 T |
|---|---|
| none (the claim) | 99.9165035 |
| q3 = 2^-101.10 | 99.9965035 |
| q3 = 2^-101.40 (the pooled threshold of the organizer replica) | 100.2965034 |
| H5 with 2^-40 instead of 2^-30 | 99.9164980 |
| H5 with 2^-25 | 99.9166741 |
| H5 with 2^-20 | 99.9221439 |
| work-cap margin 5/4 instead of 9/8 | 99.9167933 |
| A_C = 2^80 | 99.9165046 |
| no word-parallel pricing (each first block = 1 unit) | about 103.91 |

With the claimed N_G (no re-derivation) the success bound stays at or above 0.39 for an average pair bound up to
2^-29.994 only: N_G is the smallest integer that meets 0.39 under 2^-30, so the premise is stated with no slack of
its own; its distance from the evidence is in Section 9 (H5).

## 9. Heuristics

**H1 - the chaining value of one trial (score-critical).**  For every single trial of the attack (lane value
W15 = ((L ^ rL) << 9) | (v << 27) for a fixed lane L and batch position; the 8 free words W0, W1, W2, W3, W4, W9,
W11, W14 uniform from the group's first random word, the other seven words of W0..W14 solved from them as in
`d1core.family`, rL and rb from the second word), the chaining value CV1 = F_38(IV, M0) behaves as a uniform 256-bit
value as far as Steps 2 and 3 are concerned: the trial is valid with probability p2, and given validity the
second-block words have the distribution of Lemma 2 (in particular W0 and W1 are uniform and independent, so stage
3a passes with probability exactly 2^-10).  It is a statement about one trial at a time (a 256-bit value computed
from 269 uniform bits); it says nothing about two trials of one group, which H5 covers.  Used for: p2, the
distribution of the second-block words (Lemma 2, hence q3), and the per-lane expectations of the work cap.
Evidence: (i) local, on this package's family (`grp38fam.c`, Appendix A, generated from `FAM`, the lane offset and
the batch bits of `d1core.py`; 524,288 groups with xoshiro256** coins, seed 20261010, each group complete: its
32 batches of 256 lanes, 2^32 trials, each a complete 38-step compression from the IV with feed-forward; the
family words solved as in the program and checked on every trial's expanded schedule, 0 violations; W0, W1 by the
Step-2 equations; statistics by `grp38fam_stats.py`):

```text
valid (W7 in F7):  287,312,335 of 2^32 (expected 287,309,824.0, z +0.15, rate 2^-3.90196); per-group dispersion 1.0036 (z +1.84);
                   avg Pr[j|i] / rate = 1.000006 (+3 se 1.000016)
flagged (W7 and stage 3a): 281,357 (expected 280,576.0, z +1.47, rate 2^-13.89796); dispersion 1.0036 (z +1.84);
                   avg Pr[j|i] / rate = 1.0015 (+3 se 1.012)
stage 3a given valid: 2^-9.99600 (exact under H1: 2^-10; z +1.47)
batches with >= 1 valid lane:   16,777,216 of 16,777,216 (independent lanes: 16,777,215.7, z +0.58)
batches with >= 2 valid lanes:  16,777,210 (independent lanes: 16,777,209.5, z +0.20)
batches with >= 1 flagged lane: 279,047 (independent lanes: 278,251.9, z +1.52)
valid trials per variant v (32 cells): chi-square 32.3 on 31 df
byte chi-squares (255 df): CV1, 32 positions, all trials: 200.5 .. 329.0; W0..W5, 24 positions, valid trials: 220.1 .. 301.6
                   (none above the 99.9% point 330.5)
```

(ii) d2's `grouprate.c` on the SWAR family (2^29.81 trials: W7 rate 2^-3.90189) and the extraction harness's 2^30
random first blocks and 2^35..2^36 uniform CVs (Section 12); (iii) the organizer experiment (Section 10.1), which
exhibits the flag path lane by lane but is not a rate test.  Limitations: a premise, not a theorem; tested on 2^32
trials, not on 2^103.9; seven of the fifteen group words are solved, so the first block is structured (W17 = s1(W15),
W19 = s1(W17), W21 = s1(W19), W22 = W15, W24 = s1(W22) + W17 inside every group), and W15 is the only word that
varies inside a group (23 steps follow it); W17, W19 and W21..W24 are the same functions of W15 in every group, so
the randomness entering steps 15..24 comes only from the state after step 14, W16 and W18.  (Sanity remark, not
evidence: the 2^269 first blocks per trial position exceed the 2^256 chaining values, a necessary condition for
literal uniformity.)

**H2 - Step-3 probability and disjointness (score-critical; unchanged from d2).**  (a) q3 >= q3_model =
2^-101.02; (b) kappa = 1 (|L*| = 1; nothing to assume).  (c) No run selection: every run of the preregistered
estimator and of the replica is reported (Section 12).  Evidence: Section 6 (unbiased estimator under H1,
preregistered 32-seed sample with a one-sided 99% bound, exact row 16, integer stage factors, agreement with
independent counts and measurements) and a second, standard-library implementation that the organizer runs on its
own seeds with a preregistered pass rule (Section 10.2; validated on 1,020 replicates; every success it finds is a
verified semi-free-start collision).  The organizer run can confirm q3 only to within its pooled threshold
2^-101.40; the step from there to q3_model rests on the preregistered sample (sensitivity: q3 = 2^-101.40 gives
log2 T = 100.2965034).  Limitations: a Monte-Carlo bound whose 99% level relies on the central limit theorem for 32
independent estimates (heavy tails would make the sample mean low rather than high, which errs on the conservative
side, but this is not proven); depends on H1; the `+` reading.

**H3 - bit-sliced word pricing (score-critical; precedent).**  Under collision-frontier-v5 a word-RAM program that
evaluates 256 first blocks as bit planes over 64 256-bit registers is charged by its counted primitives: per group
the 32 straight-line variant programs execute 1,398,573 operations (loads, stores and gates of the emitted programs,
32 fail-plane tests of 2), 43,705.41 per batch, and the group setup 6,378 plus 10 group control: 171.504 operations =
2^-3.99153 units per first block.  The counts are produced by the shipped program (`calibrate`: all 32 variant
programs run by `run_vm` on three groups, identical counts, fail plane equal to the evaluator's), the programs use
registers 0..63 only, and the circuit is checked against the repository verifier (Section 5.5).  The specialisation
into 32 programs is charged by their summed counts (each runs once per group); their code is held in memory (Section
13).  Precedent: the bit-sliced sha256-r37 filings of this attack (ad9745bf, efd8aa9d, dd6656d4) and the sha256-r38
filings 882f372f, 349e3a6a, d5a10596 and 20dbd783 use the same pricing; no organizer ruling is cited.  Without
word-parallel pricing each first block costs one unit: about 103.91.

**H4 - advice allowances (supporting; unchanged from d2).**  The published characteristic and the SFS pair's inner
values S are used as advice; their construction is charged at A_S = 2^74 (the paper reports 2^38.3
compression-equivalents for Step 1, so the allowance is 2^35.7 times larger) and A_C = 2^78 (the characteristic
search; cost not published).  Both were run by the paper's authors with the open-source SAT/SMT tool [LLW24a] and
published together with the SFS pair, so they are computations an academic group completed.  At 2^21.8 units per
CPU-second (a core retiring about 10^10 primitive operations per second at C of about 2,700), 2^78 units is about
2.6 x 10^9 CPU-years, about 130 times the output of a 10^7-core machine (the scale of the largest supercomputers)
running for two years; it bounds any search an academic group completed and published.  DEV = 2^64 covers about
2^42.2 CPU-seconds (about 1.6 x 10^5 CPU-years).  All of our development for this track (d1, d2, q38 and this
package, including the family search that selected `FAM`, the lane offset and the batch-bit count) ran on one
15-core machine within three days, at most 15 x 3 x 86,400 = 2^21.9 CPU-seconds; b99301f4's runs were below 3,000
CPU-seconds, and the development of the reused circuit code by its authors is of the same kind (single machines,
days).  The preprocessing operation charges (PRE_BUILD = 2^40, the L enumeration at 1,024 per candidate) are bounds
by the same scale (Section 5.3).  The memory and preprocessing bounds (Section 13) are conditional on this premise.
Sensitivity: A_C = 2^80 gives log2 T = 99.9165046.

**H5 - pairs inside a group (score-critical).**  For the trials of one group (the same family words, rL and rb;
different W15), the average over ordered pairs (i, j), i != j, of Pr[A_j | A_i] is at most 2^-30:
sum_{j != i} Pr[A_i and A_j] <= (m - 1) 2^-30 sum_i Pr[A_i], m = 8,192.  (The trials of a group are exactly
identically distributed, because rL and rb are uniform, so all Pr[A_i] are equal and the plain average over
ordered pairs and the weighted form coincide.)  Under the independent-uniform model the
average is p_model = 2^-104.9, so H5 allows a dependence 2^74.9 times stronger than that model; it constrains pairs
only and is compatible with the group's 269 bits of randomness.  Used for: the group success bound (Section 7)
through the Bonferroni inequality, which needs exactly this average.  Evidence: (i) structure: two trials of a group
share steps 0..14 and differ in W15, which enters step 15 directly, the schedule words W17, W22, W30, W31 by the
expansion, and through the family W19, W21, W24 and later words;
23 steps then separate their chaining values, and A_j would have to follow from A_i with average probability above
2^-30 although each needs about 105 bits of conditions on its own chaining value; (ii) measured inside groups on
this package's family (`grp38fam.c`, the output above): the average Pr[A_j | A_i] over the ordered pairs of a group,
estimated from the per-group counts, equals the unconditional rate to within a factor 1.000006 (valid trials, rate
2^-3.9; three standard errors 1.000016) and 1.0015 (W7 and stage 3a, rate 2^-13.9; three standard errors 1.012);
batches with a flagged lane occur at the independent-lane rate (z +1.52); (iii) b99301f4's `disp.c` on the SWAR
family (2^31.81 trials, the same conclusion).  With m = 8,192 trials per group the Bonferroni factor is
1 - 2^-18.0, so the weaker constant costs 5.5 x 10^-6 bit against 2^-40 (Section 8).  Limitations: a premise; the
measured events have probability about 2^-4 and 2^-14, not 2^-105, so the measurement cannot tell 2^-30 from
2^-29.9 for the success event; the success bound uses the stated constant with no slack (Section 8); the measurement
is participant-produced (source in the package).

Not used: expected work, an independence-of-conditions model (replaced by the SMC), a random-oracle model, any
premise on the published pair beyond its verified values, any independence of the trials of one group, any
inference from organizer counts.

## 10. Organizer experiments

`experiments/d1core.py` is byte-identical to Appendix A's `d1core.py` (SHA-256 1b3e62de7e4377a4796459ea49c7e428059c1896ff1fa76247d04b998d20badc).
Both experiments run it; it dispatches on the request's experiment id.  `d1aux.py` (liveness trace, affine parts of
F7) is used only by the self-test and is not needed by the experiments.

### 10.1 d1-first-block-r38 (H1, H3, H5)

Per organizer seed the experiment runs one group of the attack driver (`attack`, the same code) with r0, r1 from
SHAKE-256(seed) and 4 batches (variants rb .. rb + 3 mod 32; 1,024 first blocks).  Each request first runs
`calibrate` on variants 0 and 31 (the counted 64-register programs against the evaluator on three groups) and reports
their summed count as the observation `variant_ops` (87,359 = 43,617 + 43,742).  A hook recomputes with the scalar
38-step compression 8 seed-chosen lanes per batch, every lane the circuit marks as passing W7 and every flagged lane,
and checks: the family's fixed words and zero sums on the lane's scalar schedule; the circuit's W7 decision and
flag; that the flagged lanes are exactly the lanes the driver sends to Step 3, with their full CV1; and, for every
flagged lane and the first W7 lane of each batch, that the second-block pair (published W14, W15) follows every A/E
cell of rows -4..15 and every W cell except W7's XOR cell (Lemma 3).  It returns the 128-byte pair
(M0 || M1, M0 || M1') of the first flagged lane if every check passed, else two nulls.  Event: full collision (none is
expected; Pr < 2^-60).  Every returned pair can be checked offline: its common first block M0 gives a CV1 that
passes W7 and the ten E16 cells, and M1 is the Step-2 image of that CV1.

The design and the expectation were frozen before any run of the frozen program on the public seed or on our own
seed set: the freeze record hashed the Appendix A files and `PREREG_fb.txt` at 2026-10-09T15:15:45Z (program
5a0903c0...); the text of `PREREG_fb.txt` carries its own time stamp 15:15:56Z.  `grp38fam.c` ran from 15:13:18Z to
15:16:56Z and its statistics at 15:18:10Z, around the freeze; the witness range is derived from the model (p2 2^-10),
not from that run, and the family was fixed before `grp38fam.c` started.  Expectation, stated as a range (not a
test; no independence of the organizer's trials is assumed and no inference is drawn from the count): mismatches 0
in every trial; under the independent-uniform model a trial returns a pair with probability
1 - (1 - p2 2^-10)^1024 = 0.06471, about 16.6 of 256, witness range 6..30; full collisions 0.  The design (4 batches,
8 random lanes per batch) was fixed for run time.  **Amendment** (15:18:41Z, recorded in `PREREG_fb.txt`): the
organizer runner accepts only numeric observations and the frozen program reported `variant_ops` as a list; it now
reports the sum (program 1b3e62de..., nothing else changed).  Before the amendment the frozen program had been run
with `run_exp_org.py` on our own seed set (12 pairs) and on the public seed (17 pairs, 0 mismatches) and once through
the local organizer-runner replay, which rejected the list observation; all runs were repeated with the amended
program.  A development build (a different family, lane offset 8, not kept) had been run once through the local
organizer-runner replay on the public seed before the freeze; its numbers are not used.

Local emulations with the amended program (`run_exp_org.py`, seed protocol of `experiments/runner.py`, Python
3.12.14): the public-seed request (no holdout nonce): 17 returned pairs, 25,042 lanes checked, 17,546 W7 lanes,
17 flagged lanes, 0 mismatches, stdout 11d8e6f7, byte-identical on two runs and under Python 3.9.6, 6.1 s; our own
seed set ('r38fam-own-seeds'): 12 pairs (14 flagged lanes in 12 trials), 25,182 lanes
checked, 0 mismatches, stdout 361750d9.  The organizer-runner replay (`experiments.runner.run_experiments` with a
subprocess executor, Python 3.12, with the package's final manifest): both experiments `completed`, first block
4.2 s and 4.0 s, q3 2.7 s and 2.7 s (6.1 s and 6.0 s in an earlier replay at load about 10), peak RSS below 75 MB
(limits 20 s and 128 MiB).  These times are from Apple silicon with the subprocess executor, not from the organizer's
linux/amd64 image with one CPU, so the margin against 20 s (3.3x at the slower replay) is an estimate.  A holdout nonce changes the seeds and
the count.

### 10.2 d1-q3-smc-r38 (H2)

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
organizer-visible statistic is the number of returned pairs, expected 21 and stated as the range 0..21 (each
replicate without an accepted success removes its own pair and trial 20's), and anyone can verify the semi-free-start
collisions in the raw report.

The design was frozen (`PREREG_q3x.txt`, program ba1dd804) before any validation run and before the public-seed
request was computed.  The threshold came from development replicates: a bootstrap of the mean of 20 put its
0.0001 quantile at 2^-101.37 after shifting to the preregistered mean.  Validation (`run_q3x_val.py`, 51 requests of
256 trials on our own seeds, 1,020 replicates): every request returned exactly 21 pairs; the 51 pooled means lay in
[2^-101.315, 2^-100.757]; 69,190 tail successes, all accepted.  d2's public-seed emulation (its own `run_exp_org.py`) returned
21 pairs, pooled mean 2^-100.843, 1,445 tail successes all accepted, the 21 returned strings are semi-free-start
collisions under the repository's `_compress` as well, byte-identical on two runs, 3.4 s (run time limit 20 s).
Under Python 3.12.14 (the organizer image runs 3.12) both requests give byte-identical stdout to Python 3.9, and the
q3 request takes 2.4 s.

What this tests: an organizer-executed, unbiased estimate of q3 under the exact distribution of Lemma 2, with a
pass rule that a true q3 of 2^-101.40 would fail about half the time, of 2^-101.55 more than 93% of the time and of
2^-101.7 more than 99.8% of the time (bootstrap of the validation replicates, rescaled); and that the success event
the estimator counts produces genuine semi-free-start collisions.  What it does not test:
H1 itself (it samples the second-block words from Lemma 2's distribution), and q3 more finely than its threshold.

**In this package.**  The q3 code of `d1core.py` (from the comment block of `q3_experiment`'s section to the end of
the file: 11,128 bytes, SHA-256 77f746cba884f10d6e4dfc883045d69e19843c4f81ccc3e35795225fa6cd45bf, identical in d2's
program ba1dd804, in q38's and in this one) is byte-identical to d2's; `setup` is identical up to its docstring and the
tables it reads are unchanged (`tables_digest` as preregistered, asserted by the self-test).  The public-seed request
with this package's program gives stdout 97394afe, the same as d2's emulation: 21 pairs, pooled mean 2^-100.843, 1,445
tail successes, all accepted, 3.5 s (Python 3.12); our own seed set gives 21 pairs (stdout aa976143).

## 11. Differences from the paper

1. Member orientation: the tables hold with x = M' (Section 3.1).  `+` is undefined; read as E_i[b] = E_{i+1}[b].
2. Step 2: 4 conditions and 2^-4, as in the paper, for the cell semantics; the exact requirement (Lemma 3) gives 2^-3.9020, which we use.
3. Table 4: `W25[4] = W25[9]` fails on the pair; it should read W25[4] = W25[6] (count unchanged).
4. (W14, W15) freedom: the paper says 2^2; for the published Step-1 solution exactly one value survives (|L| = 8, |L*| = 1).  This costs 2 bits against the paper's arithmetic; its attack may use another Step-1 solution.
5. Condition counts on rows >= 16: ours 62 + 41 = 103 (one-bit + listed two-bit), paper 102.  We do not use counts:
   the SMC gives 2^-100.99.
6. The paper's totals are expected work with independence-of-conditions; ours is a worst-case bound with caps.

## 12. Runs and hashes

Runs of d2 (and d1), on which this package rests (H2's preregistered sample, the q3 replica and its validation, the
extraction checks); all on one Apple-silicon Mac, CPU = user seconds:

| run | what | CPU | hashes / outputs |
|---|---|---:|---|
| extraction (a second agent on the same machine, 2026-10-08) | table OCR, `verify_sfs.py`, `hsm37/38 S`, `enum_S_py.py`, `validate.py`, `step2_equiv.py` (light) | about 70 | EXTRACT.md Section 11; summary.json ed648926 |
| extraction heavy (lock) | `hsm37 step3 30` (2^30 random M0), `hsm38 step3 30`, `hsm37 step3 36 direct` (2^36 CVs), `hsm38 step3 35 direct` | 2,121 | outputs 9ae6a612, 0dde492c, 79376572, 84bf58e1 (meas_step3_*.json) |
| design (the second agent) | `p2exact.py` (exhaustive F counts, numpy, 72 s, no lock: disclosed), `enumL.py`, `lstar.py`, `fwdsim.py`, `smc.py`/`smc2.py`/`smc3.py` (earlier SMC versions), `clump.py`, `a0family.py`, `proto_v1.py`, `proj.py` | about 350 | DESIGN.md Section 13 (p2exact fce3f4d1, smc3 4bc9f2fe, clump 1fa7ea3a) |
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

Runs of b99301f4 (the corrected accounting; a different machine, inside the pinned image under emulation; as reported
in its package, where A.1 and Section 8 refer to its own proof):

| run | what | CPU | hashes / outputs |
|---|---|---:|---|
| `disp.c` | H5 evidence: 2,048 groups x 1,835,008 grouped trials, seed 20261009 (`disp 2048 18 20261009 6`) | about 330 | output sha256 3224cf649c29e06bc49776c516488f225523801830e95138327dab144876927a |
| `selftest.py 38 full`, `cert.py 38` | the self-test (A.1) and the ledger with the new `cert.py` | about 950 | A.1; the ledger of Section 8 |
| ledger cross-check | an independent re-implementation of the ledger (exact rationals) reproduces d2's and this total | 1 | - |
| `recount_fb.py` | recount of the first-block experiment from the organizer's seeds (d2's official report) | 2 | 198 groups, 380 valid trials, 256/256 recorded pairs matched |

Runs of q38 (our unsubmitted predecessor build: the 38-step circuit with stage 3a, `grp38.c` on its family) and of
this package (Apple silicon, 15 cores; heavy runs through the shared machine-wide slot lock under `nice -n 10`;
Python 3.9.6 and 3.12.14):

| run | what | CPU | hashes / outputs |
|---|---|---:|---|
| q38 development | the 38-step circuit, orderings of the post-round part, lane checks of development builds (0 mismatches), timing | about 300 | - |
| q38 `grp38.c` (lock) | H1 / H5 on q38's family, 2^32 trials (superseded by `grp38fam.c`; not used as evidence here) | 264 | grp38.out aaadd45b |
| q38 checks | self-test, ledger, sensitivities, local emulations, organizer-runner replay of the q38 program | about 400 | - |
| family search | greedy + swap search over 17 candidate constraints scored only with the deterministic emitted operation count (no probabilistic evidence), jointly with the lane offset and 3..6 batch bits (`famsearch.py`, `famsearch2.py`, `refine.py`); tail port and its tests; spill-order experiments (no gain); the family was fixed before `grp38fam.c` ran | not timed individually; its logs were written 2026-10-09 14:50Z-15:12Z, and it is bounded with everything else by 2^21.9 CPU-seconds (H4) | logs kept locally |
| development replay | one development build (lane offset 8, a different family) through the local organizer-runner replay, public seed, before the freeze | 23 | not used |
| `f7check.c` | the factored W7 test against the definition of F7 on all 2^32 words | about 20 | 287,309,824 members, 0 disagreements |
| `grp38fam.c` (lock, 3 threads) | H1 / H5 on this family: 524,288 groups x 32 batches x 256 lanes = 2^32 complete 38-step trials, seed 20261010, 217 s wall, peak RSS 2 MB | 632 | output f0fabbf1, `grp38fam_stats.py` output in Section 9 |
| freeze | freeze record of the Appendix A files and `PREREG_fb.txt` 2026-10-09T15:15:45Z (program 5a0903c0; the PREREG text is stamped 15:15:56Z); amended 15:18:41Z (program 1b3e62de, observation as a scalar) | - | - |
| pre-amendment runs | `run_exp_org.py` own seeds (12 pairs) and public seed (17 pairs); one organizer-runner replay (rejected the list observation) | about 25 | repeated after the amendment |
| self-test | `selftest.py 38 full` under Python 3.9.6 (118 s) and 3.12.14 (82 s), identical output (A.1), peak 78 MB | 200 | A.1 |
| ledger | `cert.py 38`; sensitivities (Section 8); the PRE_BUILD change of Section 14 re-run | about 150 | the ledger of Section 8 |
| local emulations | `run_exp_org.py` (own seeds; public seed under 3.12 and 3.9; each request run twice) | about 45 | first block: own 361750d9, public 11d8e6f7; q3: own aa976143, public 97394afe |
| organizer runner replay | `experiments.runner.run_experiments` with a subprocess executor (Python 3.12), public seed; repeated with the final manifest after the text fixes of Section 14 | about 35 | completed; 17 and 21 returned pairs, 0 full collisions |
| build timing | the circuit, the 32 variant programs and their allocation (6.4 CPU-s); `setup(38, full=True)` (15.2 CPU-s) | 22 | Section 5.3 |

No run was discarded.  All development of d1, d2, q38 and this package ran on one 15-core machine within three days
(at most 2^21.9 CPU-seconds), far inside DEV = 2^64 units (about 2^42 CPU-seconds).

History of `d1core.py`.  q38 replaced d2's first-block code by the bit-sliced circuit (program ae0c713b, frozen
2026-10-09T07:40:21Z, not submitted); this package replaced q38's family, circuit tail and driver (programs 5a0903c0
and, after the amendment of Section 10.1, 1b3e62de); the q3 section is byte-identical throughout (Section 10.2).

Notes of d2 on the history of its `d1core.py` (the program whose `setup` and q3 code this package keeps; quoted
from d2, where "this package" means d2):

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

## 13. Memory and advice

The online attack holds the program (32 rotated sequences of the 32 variant programs, 32 x 1,398,573 instructions,
each of the 1,024 variant copies with its own copy of the scalar rare-path code of at most about 4,300 instructions;
at 32 bytes per instruction below 2^30.6 bytes), the group-constant and lane planes and the hoisted gates (640 + 8 + 721 + 1 planes), the spill slots
of a variant (at most one per stored value, below 3,000), S, L* and the row masks of Step 3, the counters and the
register save of stage 3b: below 2^31 bytes at 32 bytes per word.  The claimed memory covers every charged
computation, not only the online attack: a word-RAM computation of K primitives stores at most K words, and the
preprocessing is at most 2^78.08755 units = 2^89.50 primitives (Section 8), so its memory is at most 2^94.50 bytes
at 32 bytes per word; we claim 2^95 bytes.  This bound is conditional on H4: it converts the allowances A_C, A_S and
DEV into primitives, and the characteristic search has no published cost.  For information, the largest process run
for d2 used 31 GB RSS (the aborted SMC v1, Section 6.3); the runs of this package used at most 110 MB.  The nonuniform
advice is the characteristic and S (the `CH`, `PAIRS`, `LSTAR` tables of `d1core.py`, below 2^13 bytes), charged as
A_C + A_S.

## 14. Changes from q38, b99301f4 and d2

1. **The first-block family** (Section 4.6): 8 random words and 7 solved words per group (W20 = -K20 and the
   group-constant parts of W17, W19, W21, W22, W23, W24 equal to 0); 20 group-constant words reach the circuit
   (q38: 29).  W15 = ((L ^ rL) << 9) | (v << 27), 32 batches per group (m = 8,192; q38: W15 = L << 24 | b << 8 | gb,
   2^16 batches, m = 2^24).
2. **The batch** (Sections 5.2-5.3): 32 straight-line variant programs per group with the batch bits as literals
   and everything lane-independent hoisted into the group setup (721 gates); the tail of 882f372f / 349e3a6a /
   d5a10596; 1,398,573 operations per 32 x 256 first blocks plus 6,388 per group: 171.504 per first block (q38:
   191.44; b99301f4: 218.14).
3. **Control and counters** (Section 4.6): V and the group counter in memory (VCTRL = 6, GCTRL = 10; q38: 3 and 4,
   which left their loads and stores uncharged); the cap test inside the rare branch, where V changes.
4. **The accounting** (Sections 7, 8): b99301f4's argument with the new counts; H5 in its average form with 2^-30
   (Bonferroni factor 1 - 2^-18); a work-cap margin 9/8 (q38: 1025/1024, smaller than its evidence could
   resolve); the claim computed exactly as the smallest k / 10^5 not below log2 T (80-digit logarithm).  After the
   freeze, `cert.py` changed in one constant: PRE_BUILD = 2^36 -> 2^40, so that the preprocessing charge covers the
   measured build and enumeration time by scale with a margin (Section 5.3); log2 T moved by about 10^-21 bit, the
   claim and the preprocessing exponent are unchanged.  `d1core.py` is unchanged.  After an internal committee
simulation of this package the text was corrected (code layout as 32 rotated sequences with the code size in
Section 13, the family `assert` described as an uncounted reference check, the H4 rate 2^21.8 units per
CPU-second, the H5 wording, the experiment wording in `experiments/manifest.json` (expectations as ranges)); no
count, constant or program changed.
5. **Evidence** (Section 9): `grp38fam.c` measures H1's rates (including the stage-3a rate) and H5's within-group
   dispersion on the new family with complete groups; `f7check.c` checks the factored W7 test exhaustively.
   `grp38.c` (q38), `disp.c`, `grouprate.c` and `recount_fb.py` (b99301f4, d2) concerned other families and are
   cited, not shipped.
6. **Experiments** (Section 10): the first-block experiment for the new program, its design frozen in
   `PREREG_fb.txt` before any run of the frozen program on the public seed; the q3 experiment is unchanged
   (byte-identical code and output).
7. **Result.**  log2 T = 99.9165035 (q38 as built: 100.0746597; b99301f4: 100.3273406; d2: 100.3372398), claimed as
   99.91651.

## Appendix A. Program files

These files are the program and the evidence scripts of this package exactly as run (Python 3.9+ standard library
except `smc.py`, which needs numpy; the C files are C99, `grp38fam.c` with pthreads).  Each block below is one
file; its SHA-256 is in the marker line.  Files marked (d2) are byte-identical to those of submission 3d819a4b.

- `d1core.py` (64824 bytes): the counted program: reduced SHA-256, characteristic, SFS pair, S, L/L*, the family, the bit-sliced circuit and its 32 variant programs (build, emit, run_vm, evaluator), group setup, rare path, Step 3, verification, the attack driver with caps, calibration, the first-block experiment and the q3 replica (byte-identical to experiments/d1core.py).
- `d1aux.py` (4755 bytes): auxiliary code used by the self-test only: the liveness trace of the rare path and the affine parts of F7.
- `cert.py` (6911 bytes): the exact ledger (Sections 7, 8).
- `selftest.py` (11439 bytes): the self-test (A.0, A.1).
- `grp38fam.c` (9937 bytes): the H1 / H5 measurement on this package's family (Section 9).
- `grp38fam_stats.py` (2452 bytes): its statistics (Section 9).
- `f7check.c` (1158 bytes): the exhaustive check of the factored W7 test (Section 5.2).
- `run_exp_org.py` (4353 bytes): the local emulation of the organizer requests (Section 10).
- `PREREG_fb.txt` (1963 bytes): the design freeze of the first-block organizer experiment and its amendment (Section 10.1).
- `smc.py` (13742 bytes): the SMC estimator of q3 (d2; Section 6; needs numpy; local evidence).
- `smc_summary.py` (1653 bytes): the preregistered decision rule (d2; Section 6.3).
- `run_smc.sh` (1211 bytes): the preregistered runner (d2).
- `SEEDS_38.txt` (160 bytes): the preregistered seeds (d2).
- `PREREG_v2.txt` (1907 bytes): the preregistration record (d2).
- `fcount.c` (762 bytes): exhaustive sizes of the Step-2 sets (d2; Section 4.3).
- `PREREG_q3x.txt` (1949 bytes): the design freeze of the q3 organizer experiment (d2; Section 10.2).
- `run_q3x_val.py` (1730 bytes): the validation of the q3 organizer experiment (d2; Section 10.2).

Together 130906 bytes.

### A.0 Extraction and self-test

From the repository root (about 90 s; `full` re-enumerates L and L*; the self-test reads `verifier/hash_functions.py`
under REPO_ROOT):

```sh
mkdir -p /tmp/q38c && python3 - <<'EOF'
import hashlib, re
C = "lanes/exploratory/candidates/sha256-r38/"
t = open(C + "proof.md").read()
n = 0
for name, sha, body in re.findall(r"<!-- file: (\S+) sha256=(\w+) -->\n```\w*\n(.*?)```\n", t, re.S):
    assert hashlib.sha256(body.encode()).hexdigest() == sha, name
    open("/tmp/q38c/" + name, "w").write(body)
    n += 1
assert n == 17
assert open(C + "experiments/d1core.py").read() == open("/tmp/q38c/d1core.py").read()
EOF
cd /tmp/q38c && REPO_ROOT="$OLDPWD" python3 selftest.py 38 full
```

### A.1 Self-test output (this package; Python 3.12.14, identical under Python 3.9.6)

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
 "tables_digest_as_preregistered": "bf3bcc643e37895acd208384cebfd8c3f4ff012bbbc123a26a801b88698a4544",
 "stage3a": {
  "ck16": "fe314838",
  "m16": "4c431a80",
  "v16": "48030280",
  "f16": 10
 },
 "F7_affine_parts_and_factored_test": [
  [
   28,
   24,
   21
  ],
  287309824,
  1048576,
  65536
 ],
 "F7_sampled": [
  69817,
  70144.0
 ],
 "counts": {
  "c_init": 9,
  "c_G": 6378,
  "groupconsts": 20,
  "hoisted": 721,
  "scanb": 4,
  "scanl": 45,
  "c_cv": 1235,
  "live_lane": 15,
  "live_3b": 52,
  "c01": 71,
  "c3a": 9,
  "crest": 85,
  "c3b": 2620,
  "c_B": 1398573,
  "c_Bv": [
   43617,
   43714,
   43678,
   43703,
   43708,
   43703,
   43705,
   43719,
   43667,
   43691,
   43704,
   43728,
   43709,
   43710,
   43723,
   43721,
   43703,
   43697,
   43712,
   43713,
   43698,
   43709,
   43702,
   43717,
   43685,
   43705,
   43733,
   43726,
   43704,
   43708,
   43719,
   43742
  ],
  "cats": {
   "ld": 231494,
   "st": 83090,
   "xor": 851467,
   "and": 122559,
   "or": 109899
  },
  "maxreg": 63
 },
 "register_budget": 64,
 "variant_count": 32,
 "rare_register_budget": [
  19,
  53
 ],
 "family": {
  "FAM": [
   [
    "Z",
    17,
    0,
    10
   ],
   [
    "Z",
    19,
    0,
    12
   ],
   [
    "Z",
    24,
    0,
    8
   ],
   [
    "Z",
    23,
    0,
    7
   ],
   [
    "Z",
    22,
    0,
    6
   ],
   [
    "Z",
    21,
    0,
    5
   ],
   [
    "W",
    20,
    3524711313,
    13
   ]
  ],
  "UB": 5,
  "LO": 9,
  "NBATCH": 32
 },
 "family_constraints": 0,
 "batch_bit_exact": {
  "lanes": 76800,
  "mismatches": 0,
  "w7_pass": 5239,
  "stage3a_one_bit_off": 59,
  "flagged": 6
 },
 "flag_path_bit_exact": {
  "batches": 2048,
  "w7_pass": 35222,
  "stage3a_one_bit_off": 356,
  "flagged": 34,
  "mismatches": 0
 },
 "variant_programs_bit_exact": {
  "lanes": 16384,
  "mismatches": 0
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
  "trials_per_group": 8192,
  "log2_q_group_lb": -91.92197341982354,
  "NG": 2318775195457330464467753076,
  "NG_times_q_lb": 0.49429633,
  "log2_N": 103.90542151988149,
  "N_times_p": 0.49429821536787505,
  "vbar": 70.6907958984375,
  "vmax": 1079562,
  "VMAX": 5900978306751612076067042015150,
  "log2_online_units": 99.91389224373268,
  "log2_rare_units": 90.80516907229095,
  "log2_T": 99.91650348513534,
  "time_log2": 99.91651,
  "preprocessing_log2": 78.08755,
  "success_lower_bound": 0.3900000049923741,
  "log2_hoeffding_exponent": 58.10829313976779,
  "ops_per_batch_avg": 43705.40625,
  "ops_per_trial": 171.5040283203125
 },
 "success_at_least_0.39": true
}
selftest r38: all checks passed
```

The output is deterministic (no timings).  `cert.py 38` prints the full ledger (Section 8).

### A.2 Source files

<!-- file: d1core.py sha256=1b3e62de7e4377a4796459ea49c7e428059c1896ff1fa76247d04b998d20badc -->
```python
#!/usr/bin/env python3
# d1core.py - counted program of the r38fam package (sha256-r38-prefix-v1).  Two-block collision attack of ePrint
# 2026/1120 (CC BY) in [LLWS26] (CRYPTO 2026): reduced SHA-256, cells, SFS pair, S, L*, the r38fam first-block family,
# the NBATCH counted bit-sliced variant programs (256 lanes each; W7 test and stage 3a in the circuit), rare path,
# Step 3, both experiments.  Built on winglock's q38/d2, Th0rgal's dd6656d4 compiler and PR #674 tail, and the q37
# family/variant technique.
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
C_REF = {38: 2728}

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
# ePrint 2026/1120 Table 3 (38 steps): rows not listed are all '='.  MSB first.
# Member x is the message the paper prints second (M'); 'n' = (x, y) bits (0, 1), 'u' = (1, 0), '0'/'1' fixed
# and equal, '=' equal, '+' (undefined in the paper) read as E_i[b] = E_{i-1}[b] for vertical '+' pairs.
# X: Table 4 two-bit conditions as printed (word, step, bit, op, word, step, bit); not used by the attack.
CH = {38: dict(
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
# Table 5: chaining value, M (printed first), M' (printed second = member x), printed hash.
PAIRS = {
 38: dict(cv=_h('cd278980 1b12a052 b87cc8a6 a9e059c5 c9c3db85 6ca4b5b5 63d13ac1 c0329f1e'),
  m=_h('48fc271b 9fca20cd cc89f96f fc40396f 8b328cb4 6b91ef78 97f9b767 e2450045 3b016f58 de9804cb 66a99ea5 0ce30b8d a28cd15a 77a1e994 d28e48a0 9b5f6dbb'),
  mp=_h('48fc271b 9fca20cd cc89f96f fc40396f 8b328cb4 6b91ef78 97f9b767 c2450045 3f416758 fe9804cb 63a88c0f 0ceb1f8d a28cd15a 77a1e994 d28e48a0 9f1f65bb'),
  hash=_h('5d9ca5f4 59ace3a3 26c9c26c 4252c585 4c0803b7 1b4d5ccd 25c3ccc0 90645c4d'))}

# Exact sizes of the Step-2 sets F = {w : s0(w + d) - s0(w) = t mod 2^32} (exhaustive counts over 2^32 words,
# proof.md Section 4.3; reproduced by fcount.c and sampled by selftest.py).
FSIZE = {(38, 7): 287309824}

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

LSTAR = {38: [(0xd28e48a0, 0x9f1f65bb)]}

def setup(R, full=False):
    """All constants for R steps; full=True re-enumerates L and L*, else the recorded L* is re-checked exactly."""
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
    def shr(self, a, k): self.n += 1; return a >> k
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

# ---------------------------------------------------------------------------------------------------------
# Structural sets.
def varying(R):
    """Schedule words that depend on W15 (structural)."""
    v = {15}
    for i in range(16, R):
        if any(j in v for j in (i - 2, i - 7, i - 15, i - 16)): v.add(i)
    return v


# ---------------------------------------------------------------------------------------------------------
# Step 3 (counted on Sc).
def stage3_constants(P):
    A, E = P['Sx']; c = {}
    c['kE1'] = (A[1] - S0(A[0])) & M32; c['kE2'] = (A[2] - S0(A[1])) & M32
    c['A1&A0'] = A[1] & A[0]; c['A1|A0'] = A[1] | A[0]
    c['kW4'] = (E[4] - A[0] - K[4]) & M32; c['kW5'] = (E[5] - A[1] - S1(E[4]) - K[5]) & M32
    c['kW6'] = (E[6] - A[2] - S1(E[5]) - K[6]) & M32; c['E5&E4'] = E[5] & E[4]; c['~E5'] = E[5] ^ M32
    return c

def step3(sc, P, cv, cost=None):
    """Counted Step 3 for one valid lane (cv = CV1).  Stage 3a per l in L*: E16 = (c16 + k16) + s0(W1) + W0 against
    E16's x-value cells and '+' pairs; at the first pass W2..W7; stage 3b: rows 16..R-1 of both members, every cell,
    abort at the first failing row.  Returns (index in L*, X, Y, stage-3b entries) or (None, ...)."""
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

def ref_words(P, cv):
    """Reference (uncounted) W0..W7 of member x from CV1 by the paper's Step-2 equations."""
    A = dict(P['Sx'][0]); E = dict(P['Sx'][1])
    A[-1], A[-2], A[-3], A[-4], E[-1], E[-2], E[-3], E[-4] = cv
    for i in range(4): E[i] = (A[i] + A[i-4] - S0(A[i-1]) - MAJ(A[i-1], A[i-2], A[i-3])) & M32
    return [(E[i] - A[i-4] - E[i-4] - S1(E[i-1]) - IF(E[i-1], E[i-2], E[i-3]) - K[i]) & M32 for i in range(8)]

def inF(w, d, t): return d == 0 or ((s0((w + d) & M32) - s0(w)) & M32) == t

VFIN_UNITS, VFIN_OPS, FLAG3B, VLANE, VENT, SPILL3B = 6, 512, 2, 1, 1, 148
V3B = VENT + SPILL3B

def verify(R, M0, X, Y):
    """Target verification (VFIN_UNITS compressions + VFIN_OPS operations, once): distinct, equal R-step digests."""
    mx = struct.pack('>16I', *M0) + struct.pack('>16I', *X); my = struct.pack('>16I', *M0) + struct.pack('>16I', *Y)
    if mx != my and digest(mx, R) == digest(my, R): return mx, my
    return None

# ---------------------------------------------------------------------------------------------------------
# Bit-sliced batch: bit L of a plane is lane L; W15 = ((L ^ rL) << LO) | v << (32 - UB) (variant v = batch position).
# AND/OR/XOR gates on signed literals (NOT, rotations, constant shifts free).
CONE, CZERO = ('C', 1), ('C', 0)

class Net:
    def __init__(self): self.nodes, self.cse, self.inputs, self.grp, self.hdef, self.nh = [], {}, {}, set(), {}, False
    def inp(self, name, grp=True):
        if name not in self.inputs:
            self.nodes.append(('in', name)); n = len(self.nodes) - 1; self.inputs[name] = n
            if grp: self.grp.add(n)
        return (self.inputs[name], 0)
    def gate(self, op, a, b):
        if a > b: a, b = b, a
        key = (op, a, b)
        if key in self.cse: return self.cse[key]
        if a in self.grp and b in self.grp and not self.nh:   # group-level inputs only: computed in group setup
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
        if x[1] and y[1]: return (self.gate('or', x[0], y[0]), 1)              # ~X & ~Y = ~(X | Y)
        if x[1]: x, y = y, x
        return (self.gate('and', self.gate('xor', x[0], y[0]), x[0]), 0)       # X & ~Y = (X ^ Y) & X
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
        n = self.n; col = list(bits)[::-1] + self.carry; self.carry = []; last = self.j == self.nb - 1
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
    __slots__ = ('e',)                   # group-constant word: expression over the group's scalar values
    def __init__(self, e): self.e = e

def lits(v): return [CONE if (v >> j) & 1 else CZERO for j in range(32)]
SIG = {'S0': (2, 13, 22, None), 'S1': (6, 11, 25, None), 's0': (7, 18, None, 3), 's1': (17, 19, None, 10)}
# The r38fam family (proof.md Section 4.6): FAM fixes the listed schedule words (kind 'W') and sets the group-constant
# part of the listed expansions to 0 (kind 'Z'); those words and sums are literals of the circuit (no planes, constant
# folding).  Solved in order for the last field; the other 8 words of W0..W14 are random.  UB batch-counter bits of
# W15 (bits 32-UB..31); the lanes in bits LO..LO+7 (XOR the group's rL); the other bits 0.
FAM = [('Z', 17, 0, 10), ('Z', 19, 0, 12), ('Z', 24, 0, 8), ('Z', 23, 0, 7), ('Z', 22, 0, 6), ('Z', 21, 0, 5),
       ('W', 20, -K[20] & M32, 13)]
UB, LO = 5, 9

def zterms(t):
    """The group-constant terms of W_t's expansion (the words W_u, u <= 20, u not varying)."""
    var = varying(38)
    return tuple(((fn, ('W', u)) if fn else ('W', u)) for u, fn in ((t - 2, 's1'), (t - 7, None), (t - 15, 's0'),
                 (t - 16, None)) if u not in var)

def wterms(t): return (('s1', ('W', t - 2)), ('W', t - 7), ('s0', ('W', t - 15)), ('W', t - 16))
FW = dict((('W', t), v) for k, t, v, x in FAM if k == 'W'); ZS = set(frozenset(zterms(t)) for k, t, v, x in FAM if k == 'Z')

def wv(e, Z): return Z[e[1]] if e[0] == 'W' else globals()[e[0]](wv(e[1], Z))

def fixv(e):
    """Value of a group-word expression that is the same in every group of the family, else None."""
    o = e[0]
    if o in ('K', 'IV', 'IMM'): return K[e[1]] if o == 'K' else IV[e[1]] if o == 'IV' else e[1]
    if o in ('W', 'A', 'E'): return FW.get(e)
    t = list(e[1:])
    if o == 'ADD':
        for z in ZS:
            if all(x in t for x in z):
                for x in z: t.remove(x)
    a = [fixv(x) for x in t]
    if None in a: return None
    if o == 'ADD': return sum(a) & M32
    return globals()[o](a[0]) if o in SIG else (IF if o == 'CH' else MAJ)(*a)

class Bld:
    def __init__(self, R): self.R = R; self.net = Net(); self.reg = {}
    def planes(self, w):
        if isinstance(w, list): return w
        v = fixv(w.e)
        if v is not None: return lits(v)
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

def build(R, v=None, b=None):
    """Lock-step emission (W_t, T1, E_t, A_t at bit j) of rounds 15..37, then CV1 (feed-forward), the Step-2 test
    W7 in F7 and stage 3a (E16 = ck16 + s0(W1) + W0 on the 10 cells of m16).  Returns (builder, fail, fail7): bit L
    of fail is 0 iff lane L passes both tests, bit L of fail7 is 0 iff lane L passes W7.  v None: the batch bits are
    inputs uhi[i] (evaluator; defines the hoisted gates); else the literal bits of v on b's net, no new hoisting."""
    b = b or Bld(R); n = b.net; n.nh = v is not None; var = varying(R); inl = {R - 2, R - 1}   # W36, W37 inlined
    W = {i: Cw(('W', i)) for i in list(range(15)) + [i for i in range(16, R) if i not in var]}
    W[15] = [CZERO] * LO + [n.inp('lane[%d]' % i) for i in range(8)] + [CZERO] * (24 - UB - LO) + \
        ([n.inp('uhi[%d]' % i, False) for i in range(UB)] if v is None else lits(v)[:UB])
    A = {i: Cw(('A', i)) for i in range(11, 15)}; E = {i: Cw(('E', i)) for i in range(11, 15)}
    P = setup(R); A0, A1 = P['Sx'][0][0], P['Sx'][0][1]; d0 = P['Lstar'][0]; L = lambda v: lits(v & M32)
    def wi(t):
        return [b.fn(fn, [W[u]]) if fn else W[u] for u, fn in ((t-2, 's1'), (t-7, None), (t-15, 's0'), (t-16, None))]
    for t in range(15, R):
        a, bb, c, d, e, f, g, h = A[t-1], A[t-2], A[t-3], A[t-4], E[t-1], E[t-2], E[t-3], E[t-4]
        dep = t in var and t > 15 and t not in inl; last = t == R - 1
        if dep: wf = b.prep(wi(t)); wc = Col(n); W[t] = []
        t1 = [h, b.fn('S1', [e]), b.fn('CH', [e, f, g])] + (wi(t) if t in inl else ([] if dep else [W[t]]))
        s0a, mj = b.fn('S0', [a]), b.fn('MAJ', [a, bb, c])
        nv = sum(not isinstance(x, Cw) for x in t1) + dep
        if last:      # a1 = A37 + IV0, e1 = E37 + IV4; a2, a3, e2, e3 = A36, A35, E36, E35 + IV; W7 = c7 - a1
            tf = b.prep(t1, t); tc = Col(n); ef = b.prep([d, Cw(('IMM', IV[4]))]); ec = Col(n)
            af = b.prep([s0a, mj, Cw(('IMM', IV[0]))]); ac = Col(n); E[t], A[t] = [], []
            cv = [(Col(n), x, L(k)) for x, k in ((a, IV[1]), (bb, IV[2]), (e, IV[5]), (f, IV[6]))]; cw = [[], [], [], []]
            w7c, w7k = Col(n), L(P['c7'] + 1)
        elif nv >= 2:
            tf = b.prep(t1, t); tc = Col(n); ef = b.prep([d]); ec = Col(n); af = b.prep([s0a, mj]); ac = Col(n); E[t], A[t] = [], []
        else:
            ef = b.prep(t1 + [d], t); ec = Col(n); af = b.prep(t1 + [s0a, mj], t); ac = Col(n); E[t], A[t] = [], []
        for j in range(32):
            wj = []
            if dep: W[t].append(wc.step([q(j) for q in wf])); wj = [W[t][j]]
            if nv >= 2 or last:
                tj = tc.step([q(j) for q in tf] + wj)
                E[t].append(ec.step([tj] + [q(j) for q in ef])); A[t].append(ac.step([tj] + [q(j) for q in af]))
            else:
                E[t].append(ec.step([q(j) for q in ef] + wj)); A[t].append(ac.step([q(j) for q in af] + wj))
            if last:
                for (cc, x, k), o in zip(cv, cw): o.append(cc.step([x[j], k[j]]))
    # W7 = c7 - a1 (a1 = A37 + IV0); E0 = A0 + a4 - Smj, Smj = S0(a1) + MAJ(a1, a2, a3); W1 = A1 - S0(A0) - K1 - MAJ(A0, a1,
    # a2) - e3 - S1(E0) - IF(E0, e1, e2); E16 = ck16 + s0(W1) + W0 with W0 = A0 - K0 - Smj - e4 - S1(e1) - IF(e1, e2, e3)
    # folded into one column (bits 0..30; -x = ~x + 1; a4 = A34 + IV3, e3 = E35 + IV6, e4 = E34 + IV7 enter linearly in
    # E0, W1 and E16, so their IV words fold into the constants) - the tail of Th0rgal's PR #674.
    a1, e1, a4, e4 = A[R-1], E[R-1], A[R-4], E[R-4]; a2, a3, e2, e3 = cw
    f7 = fails7(n, [w7c.step([n.NOT(a1[j]), w7k[j]]) for j in range(32)])
    neg = lambda p: [n.NOT(x) for x in p]; ng = lambda f: (lambda j, f=f: n.NOT(f(j))); c = P['s3c']
    Smj = b.add([b.fn('S0', [a1]), b.fn('MAJ', [a1, a2, a3])])
    E0 = b.add([a4, neg(Smj), L(A0 + IV[3] + 1)])
    mjB = [(n.OR if (A0 >> j) & 1 else n.AND)(a1[j], a2[j]) for j in range(32)]
    W1 = b.add([ng(b.fn('S1', [E0])), ng(b.fn('CH', [E0, e1, e2])), neg(mjB), neg(E[R-3]), L(c['kE1'] - K[1] - IV[6] + 4)])
    fs = b.prep([b.fn('s0', [W1]), ng(b.fn('CH', [e1, e2, e3])), neg(e4), ng(b.fn('S1', [e1])), neg(Smj),
                 L(A0 - K[0] - IV[7] + 4 + d0['ck16'])])
    col = Col(n, 31); f16 = None
    for j in range(31):
        x = n.XOR(col.step([q(j) for q in fs]), CONE if (d0['v16'] >> j) & 1 else CZERO)
        if (P['m16'] >> j) & 1: f16 = x if f16 is None else n.OR(f16, x)
    return b, n.OR(f7, f16), f7

def fails7(n, w):
    """W7 not in F7 for (d7, t7) = (2^29, 0x03bff800), factored over the carry of bit 29 (Th0rgal, PR #674)."""
    f0 = n.OR(n.OR(n.XOR(w[1], w[12]), n.NOT(n.XOR(w[8], w[25]))), n.NOT(n.XOR(w[14], w[18])))
    f1 = n.OR(n.OR(n.XOR(w[2], w[13]), n.NOT(n.XOR(w[9], w[26]))), n.NOT(n.XOR(w[15], w[19])))
    w3 = n.XOR(w[3], w[14])
    f2 = n.OR(n.OR(n.XOR(w3, w[31]), n.NOT(n.XOR(w3, n.XOR(w[10], w[27])))), n.NOT(n.XOR(w3, n.XOR(w[16], w[20]))))
    return n.OR(f0, n.AND(w[29], n.OR(f1, n.AND(w[30], f2))))

NREG, TEST = 64, 2       # registers; fail-plane test (compare, branch)

def emit(net, fail, nreg=NREG):
    """Furthest-next-use allocation, every load and store explicit; inputs (group, lane, hoisted, ones planes) are
    in memory; 'test' reads the fail plane (and ones if unnegated)."""
    need, st = set(), [fail[0]]
    while st:
        x = st.pop()
        if x not in need: need.add(x); st.extend(operands(net.nodes[x]))
    ones = net.inp('ones')[0]; need.add(ones)
    order = [i for i in range(len(net.nodes)) if i in need and net.nodes[i][0] != 'in'] + ['test']
    def opd(x): return ((fail[0],) if fail[1] else (fail[0], ones)) if x == 'test' else operands(net.nodes[x])
    uses = {}
    for pos, x in enumerate(order):
        for o in opd(x): uses.setdefault(o, []).append(pos)
    INF = 1 << 60; ptr = {}
    def nxt(v, pos):
        u = uses.get(v, ()); i = ptr.get(v, 0)
        while i < len(u) and u[i] < pos: i += 1
        ptr[v] = i; return u[i] if i < len(u) else INF
    reg = {}; free = list(range(nreg))[::-1]; inmem = set(i for i in need if net.nodes[i][0] == 'in'); prog = []
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
        if x == 'test': prog.append((x,) + tuple(src)); continue
        rd = take(pos + 1, set()); reg[x] = rd; prog.append((net.nodes[x][0], rd, src[0], src[1]))
    return prog

def run_vm(prog, mem, fpol, nreg=NREG):
    """Runs a variant program; returns (operations, fail plane, hit)."""
    r = [0] * nreg; ops = 0; hit = fl = None
    for ins in prog:
        o = ins[0]
        if o == 'ld': r[ins[1]] = mem[ins[2]]; ops += 1
        elif o == 'st': mem[ins[1]] = r[ins[2]]; ops += 1
        elif o == 'xor': r[ins[1]] = r[ins[2]] ^ r[ins[3]]; ops += 1
        elif o == 'and': r[ins[1]] = r[ins[2]] & r[ins[3]]; ops += 1
        elif o == 'or': r[ins[1]] = r[ins[2]] | r[ins[3]]; ops += 1
        else: fl = r[ins[1]] ^ (WORD if fpol else 0); hit = (r[ins[1]] != 0) if fpol else (r[ins[1]] != r[ins[2]]); ops += TEST
    return ops, fl, hit

class Prog:
    def __init__(self, R):
        self.R = R; self.b, self.fail, self.f7 = build(R); net = self.b.net
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
        return tuple(v[x[0]] ^ (WORD if x[1] else 0) for x in (s.fail, s.f7))
    def inputs(self, base, rL, c):
        I = {}; reg = self.b.reg; sc = Sc(); memo = {}
        for e, i in reg.items():
            v = cval_sc(sc, e, base, memo)
            for j in range(32): I['G%d[%d]' % (i, j)] = WORD if (v >> j) & 1 else 0
        for i in range(UB): I['uhi[%d]' % i] = WORD if (c >> i) & 1 else 0
        for i in range(8): I['lane[%d]' % i] = sum(1 << L for L in range(256) if ((L ^ rL) >> i) & 1)
        I['ones'] = WORD; return I
    def planes(s, base, rL, c): return s.f(s.inputs(base, rL, c))
    def variant(s, v):
        b, _, _ = build(s.R); _, f, _ = build(s.R, v, b); return b.net, f
    def mem(s, I):
        """Memory image of a group: input planes and the hoisted gates (as group_setup computes them)."""
        net = s.b.net; m = {}
        for x, nd in enumerate(net.nodes):
            if nd[0] == 'in':
                if x in net.hdef: op, p, q = net.hdef[x]; m[x] = m[p] ^ m[q] if op == 'xor' else m[p] & m[q] if op == 'and' else m[p] | m[q]
                else: m[x] = I.get(nd[1], 0)
        return m


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

GPLANE = 4         # plane of a group-constant bit: shift, and 1, subtract from 0, store

def tval(sc, e, w):
    """Counted value of a family term from the words w (W16/W18/W20 recomputed unless fixed)."""
    if e[0] == 'W':
        i = e[1]
        if i <= 14: return w[i]
        if ('W', i) in FW: return sc.ld(FW[('W', i)])
        return sc.m(sc.add(sc.add(tval(sc, ('s1', ('W', i - 2)), w), w[i - 7]), sc.add(tval(sc, ('s0', ('W', i - 15)), w), w[i - 16])))
    return getattr(sc, e[0])(tval(sc, e[1], w))

def family(sc, r0, r1):
    """W0..W14 of a group (counted): the 8 words not solved are the 32-bit fields of r0 (shift, mask); then each FAM
    constraint is solved for its word in order."""
    sol = [x for k, t, v, x in FAM]; rnd = [i for i in range(15) if i not in sol]; w = [None] * 15
    for j, i in enumerate(rnd): w[i] = (r0 >> (32 * j)) & M32; sc.n += 2
    for k, t, v, x in FAM:
        terms = list(wterms(t) if k == 'W' else zterms(t)); terms.remove(('W', x))
        acc = sc.ld(v if k == 'W' else 0)
        for e in terms: acc = sc.sub(acc, tval(sc, e, w))
        w[x] = sc.m(acc)
    return w

def w15(L, rL, c): return ((L ^ rL) << LO) | ((c % NBATCH) << (32 - UB))

def group_setup(sc, pg, R, r0, r1):
    """Counted: 2 RAND, family(), rL, rb (3), rounds 0..14 and the non-varying words (asserted), constant words and
    planes, lane planes of L ^ rL (6 each), hoisted gates (2 loads, gate, store), the ones plane (2), stores of M0,
    rL, rb, A11..14, E11..14 for the rare path."""
    sc.n += 2 + 3; w = family(sc, r0, r1); rL, rb = r1 & 255, (r1 >> 8) % NBATCH
    base = group_base(sc, R, w); memo = {}; Zd = dict((i, base[('W', i)]) for i in range(21) if ('W', i) in base)
    assert all(base[e] == v for e, v in FW.items()) and all(sum(wv(x, Zd) for x in z) & M32 == 0 for z in ZS)
    for e in pg.b.reg: cval_sc(sc, e, base, memo)
    sc.n += GPLANE * 32 * len(pg.b.reg) + 6 * 8 + 4 * len(pg.b.net.hdef) + 2 + 15 + 2 + 8
    return base, w, rL, rb

def lane_cv(sc, R, base, rL, c, L):
    """CV1 of lane L at batch counter c recomputed from the stored group state (rounds 15..R-1, feed-forward);
    the family's fixed words are immediates."""
    ld = sc.ld; W = dict((i, ld(base[('W', i)])) for i in range(15))
    W[15] = sc.or_(sc.shl(sc.xor(L, ld(rL)), LO), sc.shl(sc.and_(ld(c), ld(NBATCH - 1)), 32 - UB))
    for i in range(16, R):
        W[i] = ld(FW[('W', i)]) if ('W', i) in FW else \
            sc.m(sc.add(sc.add(sc.s1(W[i-2]), W[i-7]), sc.add(sc.s0(W[i-15]), W[i-16])))
    a, b_, c_, d = [ld(base[('A', i)]) for i in (14, 13, 12, 11)]; e, f, g, h = [ld(base[('E', i)]) for i in (14, 13, 12, 11)]
    for i in range(15, R):
        t1 = sc.add(sc.add(sc.add(sc.add(h, sc.S1(e)), sc.IF(e, f, g)), ld(K[i])), W[i])
        t2 = sc.add(sc.S0(a), sc.MAJ(a, b_, c_))
        a, b_, c_, d, e, f, g, h = sc.m(sc.add(t1, t2)), a, b_, c_, sc.m(sc.add(d, t1)), e, f, g
    return [sc.m(sc.add(x, ld(v))) for x, v in zip((a, b_, c_, d, e, f, g, h), IV)]

# Lane scan: x = fail ^ ones, loop test: SCANB = 4; per flagged lane (worst case) SCANL = 45: low = x & -x (2),
# x ^= low (1), index by an 8-step binary search (<= 5 each), loop test (2).
SCANB, SCANL = 4, 45

def lanes_passing(sc, fl):
    x = fl ^ WORD; sc.n += SCANB; out = []
    while x:
        low = x & -x; out.append(low.bit_length() - 1); x ^= low; sc.n += SCANL
    return out

# ---------------------------------------------------------------------------------------------------------
# The attack with fixed caps: NG groups of NBATCH batches of 256 trials; batch k of a group runs the variant program
# v = (rb + k) mod NBATCH.  A batch enters the rare path iff some lane passes W7 and stage 3a.  V counts every
# rare-path operation (SCANB, VCTRL, per lane SCANL, VLANE, lane_cv, Step 3, V3B per stage-3b entry); V changes only
# there and is compared with VMAX there; halt when V > VMAX.  All 64 registers can be live inside a variant program,
# so V and the group counter g live in memory: VCTRL = 6 (load V, add, compare, branch, store V, return jump into the
# variant sequence); GCTRL = 10 per group (load g, add, store g, compare, branch; dispatch into the doubled variant
# sequence at rb: shift, add, load, branch; return jump).
OPS = {}; PROG = {}
VCTRL, GCTRL = 6, 10
NBATCH = 1 << UB

def prog(R):
    if R not in PROG: PROG[R] = Prog(R)
    return PROG[R]

def attack(R, P, NG, VMAX, coins, nbatch=None, hook=None):
    pg = prog(R); V = 0; nbatch = NBATCH if nbatch is None else nbatch
    for gi in range(NG):
        r0, r1 = coins(), coins(); base, M0, rL, rb = group_setup(Sc(), pg, R, r0, r1); I = pg.inputs(base, rL, 0)
        for kb in range(nbatch):
            c = rb + kb
            for i in range(UB): I['uhi[%d]' % i] = WORD if (c >> i) & 1 else 0
            fl, f7 = pg.f(I); found = []
            if fl != WORD:
                v = Sc(); v.n += VCTRL
                for L in lanes_passing(v, fl):
                    v.n += VLANE; cv = lane_cv(v, R, base, rL, c, L)
                    li, X, Y, n3b = step3(v, P, cv); found.append((L, cv, li, n3b))
                    if li is not None:
                        res = verify(R, M0 + [w15(L, rL, c)], X, Y)
                        if res:
                            if hook: hook(M0, rL, c, fl, f7, found)
                            return dict(pair=res, V=V + v.n, group=gi, batch=kb)
                V += v.n
                if V > VMAX:
                    if hook: hook(M0, rL, c, fl, f7, found)
                    return dict(pair=None, V=V, group=gi, batch=kb, halted=True)
            if hook: hook(M0, rL, c, fl, f7, found)
    return dict(pair=None, V=V, group=NG, batch=0)

def calibrate(R, P, live=True, vs=None):
    """Exact counts: c_G, c_cv, Step-3 parts equal over three groups; each variant program (vs: all, or the listed
    ones) run on the three groups gives the evaluator's fail plane; c_B = sum of the variant costs (one group)."""
    pg = prog(R); res = None; G = []
    for seed in (1, 2, 3):
        h = lambda i: int.from_bytes(hashlib.sha256(b'cal%d-%d' % (seed, i)).digest(), 'big')
        sc = Sc(); base, M0, rL, rb = group_setup(sc, pg, R, h(0), h(1)); cG = sc.n
        I = pg.inputs(base, rL, 0); G.append((I, pg.mem(I)))
        s2 = Sc(); lane_cv(s2, R, base, rL, rb + 5, 7); ccv = s2.n
        cost = {}; out = step3(Sc(), P, PAIRS[R]['cv'], cost); lv = __import__('d1aux').rare_liveness(R, P) if live else (0, 0)
        assert out[0] is not None and out[1] == PAIRS[R]['mp'] and out[2] == PAIRS[R]['m']
        cur = dict(c_init=9, c_G=cG, groupconsts=len(pg.b.reg), hoisted=len(pg.b.net.hdef), scanb=SCANB, scanl=SCANL,
                   c_cv=ccv, live_lane=lv[0], live_3b=lv[1], **cost)
        assert res is None or res == cur, (res, cur)
        res = cur
    cv, cats, mx = [], dict.fromkeys(('ld', 'st', 'xor', 'and', 'or'), 0), 0
    for v in (range(NBATCH) if vs is None else vs):
        vn, vf = pg.variant(v); pr = emit(vn, vf); ones = vn.inputs['ones']; n = None
        for I, m in G:
            for i in range(UB): I['uhi[%d]' % i] = WORD if (v >> i) & 1 else 0
            m = dict(m); m[ones] = WORD; ops, fl, hit = run_vm(pr, m, vf[1])
            assert fl == pg.f(I)[0] and hit == (fl != WORD) and n in (None, ops); n = ops
        cv.append(n); mx = max([mx] + [max(i[1:]) for i in pr if i[0] in ('xor', 'and', 'or')])
        for k in cats: cats[k] += sum(1 for i in pr if i[0] == k)
    res.update(c_B=sum(cv), c_Bv=cv, cats=cats, maxreg=mx)
    OPS[R] = res
    return res

# ---------------------------------------------------------------------------------------------------------
# Organizer experiment d1-first-block-r38: per seed one group (coins from SHAKE-256(seed)), NB_EXP batches of the
# driver.  The family's fixed words and zero sums are checked on the scalar schedule of every lane checked.  For CHK
# seed-chosen lanes per batch, every lane the circuit marks as passing W7 and every flagged lane: the W7 and W7 +
# stage-3a decisions against the scalar compression, flagged lanes = lanes sent to Step 3 with the scalar CV1; every
# cell of rows -4..15 (but the W7 XOR cell) for every flagged lane and the first W7 lane of each batch.  Returns the
# pair (published l) of the first flagged lane if every check passed.
NB_EXP, CHK, VEXP = 4, 8, (0, 31)

def experiment(req):
    R = {'sha256-r38-prefix-v1': 38}[req['target_profile']]
    P = setup(R); d0 = P['Lstar'][0]; rows = []; cal = None
    for tr in req['trials']:
        seed = bytes.fromhex(tr['seed']); ctr = [0]
        if cal is None: cal = calibrate(R, P, False, VEXP)
        def coins():
            ctr[0] += 1; return int.from_bytes(hashlib.shake_256(seed + bytes([ctr[0]])).digest(32), 'big')
        obs = dict(lanes_checked=0, mismatches=0, w7_pass=0, hits=0, stage3b=0, cells_checked=0, variant_ops=cal['c_B'])
        first = []
        def hook(M0, rL, c, fl, f7, found):
            fd = dict((f[0], f) for f in found); c1 = True
            pick = set(hashlib.shake_256(seed + b'chk' + bytes([c & 255])).digest(CHK)) | set(fd) | \
                set(L for L in range(256) if not (f7 >> L) & 1 or not (fl >> L) & 1)
            for L in sorted(pick):
                blk = M0 + [w15(L, rL, c)]; cv = compress(IV, blk, R); obs['lanes_checked'] += 1
                Z = list(blk)
                for i in range(16, 21): Z.append(sch(Z, i))
                bad = any(Z[e[1]] != v for e, v in FW.items()) or any(sum(wv(x, Z) for x in z) & M32 for z in ZS)
                W = ref_words(P, cv); p7 = inF(W[7], P['d7'], P['t7'])
                hit = p7 and ((d0['ck16'] + s0(W[1]) + W[0]) & P['m16']) == d0['v16']
                bad |= p7 != (not (f7 >> L) & 1) or hit != (not (fl >> L) & 1) or hit != (L in fd) or (L in fd and fd[L][1] != cv)
                obs['w7_pass'] += p7
                if p7 and (hit or c1):
                    X = W + P['Wx'][8:14] + list(d0['w'][:2]); Y = W[:7] + [(W[7] + P['d7']) & M32] + P['Wy'][8:14] + list(d0['w'][2:])
                    bad |= any(i < 16 and (k, i) != ('W', 7) for k, i in cellcheck(R, cv, X, Y)[0]); c1 = False; obs['cells_checked'] += 1
                    if hit:
                        obs['hits'] += 1; obs['stage3b'] += fd[L][3]
                        if not first: first.append((blk, X, Y))
                obs['mismatches'] += bad
        attack(R, P, 1, 1 << 60, coins, nbatch=NB_EXP, hook=hook)
        row = dict(trial=tr['trial'], message_a_hex=None, message_b_hex=None, observations=obs)
        if first and obs['mismatches'] == 0:
            blk, X, Y = first[0]
            row['message_a_hex'] = (struct.pack('>16I', *blk) + struct.pack('>16I', *X)).hex()
            row['message_b_hex'] = (struct.pack('>16I', *blk) + struct.pack('>16I', *Y)).hex()
        rows.append(row)
    return dict(schema_version=1, trials=rows)
# ---------------------------------------------------------------------------------------------------------
# Organizer experiment d1-q3-smc-r38 (H2; proof.md Section 10.2): smc.py's estimator of q3 for 38 steps,
# re-implemented with the standard library at reduced size.  Row 16 exactly: every E16 word with the proposal's
# constraints (x-value cells, '+' bits, E16-to-E16 two-bit conditions; 2^19 words) is checked against the whole
# row 16.  Rows 17..22: propose E_i^x (weight 2^-f, exact), W_i^x = E_i^x - (rest of step i), W_i^y = W_i^x + its
# exact difference, check the row, resample NP survivors uniformly.  Tail: propose W23 (cells and W23 conditions
# imposed), imply W7 (weight 1{W7 in F7} 2^(32-f) / |F7|), rows 23..37 deterministic.  Every tail success is
# rebuilt (W0..W7 by the inverse expansion, CV1 by inverting steps 7..0 from S) and checked with the reference
# compression as a 38-step semi-free-start collision whose CV1 passes Step 2 and whose cells hold on rows 16..37.
FIX = {38: {('W', 25, 4, '=', 'W', 25, 9): ('W', 25, 4, '=', 'W', 25, 6)}}   # the corrected reading (Section 3.3)
KI = {'A': 0, 'E': 1, 'W': 4}
Q3X = dict(K=20, NP=64, MS={17: 128, 18: 4, 19: 4, 20: 1, 21: 1, 22: 1}, MT=512, POOL_LOG2=-101.40)

def xlist(R):
    """X': the printed two-bit conditions with a word in rows >= 16 (one corrected), keyed by the later row."""
    out = {}
    for x in CH[R]['X']:
        x = FIX[R].get(x, x)
        if max(x[1], x[5]) >= 16: out.setdefault(max(x[1], x[5]), []).append(x)
    return out

def recipe(P, XL, kind, i):
    """Proposal of the x-side word of row i (as smc.propose): its x-value cells, '+' bits (E) and the same-kind
    two-bit conditions imposed; a step (ba, ib, bb, flip) sets bit ba to bit bb of row ib's word (of the word
    itself if ib == i), flipped for '!'.  2^-f is the exact probability of the constraints for a uniform word."""
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
    """Row i of particle p = [AX, EX, AY, EY, X, Y]: every cell (A, E, W), the '+' pairs and X' of row i."""
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
    """Exact row 16 for every l in L*: [(l index, E16^x)] over all 2^(32-f) proposal words, and f."""
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
    """One replicate: an unbiased estimate of q3 (smc.py's estimator at reduced size).  Returns (estimate,
    [(stage, survivors)], tail successes, rebuilt pairs, failed rebuilds)."""
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
    """Trials 0..K-1: one replicate each (randomness from SHAKE-256 of the organizer seed); trial t returns its
    first rebuilt pair (CV1 || M1, CV1 || M1', 96 bytes each) iff it has a tail success and every success was
    verified.  Trial K returns the last rebuilt pair iff every replicate passed and the mean of the K estimates
    is at least 2^POOL_LOG2.  Later trials return no pair by design."""
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

<!-- file: d1aux.py sha256=56df20b2ed6f2ee52fa0ad25744e1243bb68a85f638871644870d13c9f143f61 -->
```python
# d1aux.py - auxiliary code of the r38fam package (proof.md Appendix A), not part of the experiment program:
# the liveness trace of the rare path (ScLive, rare_liveness; used by d1core.calibrate when live=True) and the affine
# parts of the Step-2 set F7 (gauss, fparts; used by selftest.py).
from d1core import *

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
    """Register demand of Step 3 for one lane on the published pair's CV: lane path (CV, E0, W0, E1, W1, q pinned;
    no stage-3b entry) and stage 3b (after the register-file save).  Returns (lane peak, stage-3b peak)."""
    cv0 = PAIRS[R]['cv']; li0 = [d['w'][:2] for d in P['Lstar']].index(tuple(P['Wx'][14:16]))
    sc = ScLive(); cv = [sc.ld(c) for c in cv0]
    P2 = dict(P); P2['Lstar'] = [d for i, d in enumerate(P['Lstar']) if i != li0]
    out = step3(sc, P2, cv); assert out[0] is None and out[3] == 0
    lane = sc.peak(pinned=cv + sc.keep)
    sc = ScLive(); cv = [sc.ld(c) for c in cv0]
    li, X, Y, n3b = step3(sc, P, cv); assert li == li0 and n3b == 1
    return lane, sc.peak()

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
```

<!-- file: cert.py sha256=9bcfde4b99550743ed4ac6188601eeb27bb0bc66f89bab285f26e59651964539 -->
```python
#!/usr/bin/env python3
# cert.py - the exact ledger of the r38fam package (proof.md Sections 7 and 8).  Every count comes from
# d1core.calibrate() (the counted variant programs, group setup, rare path) and d1core.setup(38, full=True) (the
# preprocessing enumeration); every probability is an exact rational except q3_model, the preregistered SMC value
# (H2), and the three exponentials of the success bound (floating point with a margin).  The total is an exact
# rational; time_log2 is the smallest k / 10^5 with 2^(k / 10^5) >= T (exact integer test).
# usage: cert.py 38 [q3_log2] [pair_log2]   (prints JSON; exits non-zero if a check fails)
# Success: H1 per single trial, exact independence of groups (fresh coins), H5 (average pair bound) + Bonferroni
# inside a group.  Work cap: per-lane expectations (H1) with a union bound per batch, Hoeffding over the groups.
import sys, json, math
from fractions import Fraction as Fr
import d1core as D

Q3_LOG2 = -101.02                       # preregistered q3_model (proof.md Section 6.3), from smc_summary.py
KAPPA = Fr(1)                           # |L*| = 1: no disjointness factor (H2 (b))
A_C, A_S, DEV = 2 ** 78, 2 ** 74, 2 ** 64   # allowances (units): characteristic search, Step-1 solve, all development (H4)
INIT_ALLOW = 256                        # constant planes (8 lane patterns, all-ones) written once + program start
PRE_BUILD = 2 ** 40                     # operation bound by scale: building the circuit, the NBATCH variant programs and
                                        # their allocation (6.4 CPU-s) and the L enumeration (15.2 CPU-s) at 10^10 ops/CPU-s
PRE_PER_CAND = 1024                     # operation bound per candidate of the L enumeration (each < 300)
MARGIN = Fr(9, 8)                       # V_MAX = ceil(MARGIN * N_B * vbar): tolerates a 12.5% excess of the flagged rate
PAIR_LOG2 = -30                         # H5: average over ordered pairs i != j of one group of Pr[A_j | A_i] <= 2^PAIR_LOG2
XREQ = Fr(49429633, 10 ** 8)            # N_G q_lb >= XREQ; 1 - exp(-XREQ) = 0.3900000050...

def log2f(x):
    """log2 of a positive Fraction to ~1e-15 absolute."""
    n, d = x.numerator, x.denominator; k = n.bit_length() - d.bit_length() - 60
    q = (n << -k) // d if k < 0 else n // (d << k)
    return k + math.log2(q)

def claim5(T):
    """Smallest k with 2^(k / 10^5) >= T, as k / 10^5: (k / 10^5) >= log2 T  <=>  2^k >= T^(10^5); exact via
    integer comparison of 2^k * den^(10^5) >= num^(10^5) is too large, so bracket with log2f and check both
    neighbours with 200-bit fixed point."""
    x = log2f(T); k = math.ceil(x * 100000) - 2
    from decimal import Decimal, getcontext
    getcontext().prec = 80
    lt = (Decimal(T.numerator).ln() - Decimal(T.denominator).ln()) / Decimal(2).ln()
    while Decimal(k) / Decimal(100000) < lt: k += 1
    return k / 100000, str(lt)

def ledger(R=38, q3_log2=None, pair_log2=None):
    P = D.setup(R, full=True); cal = D.calibrate(R, P); C = D.C_REF[R]
    q3_log2 = Q3_LOG2 if q3_log2 is None else q3_log2; PAIR = Fr(2) ** (PAIR_LOG2 if pair_log2 is None else pair_log2)
    nL = len(P['Lstar']); p2 = Fr(P['F7'], 2 ** 32)
    fl = math.floor(q3_log2)            # q3 = a rational not above 2^q3_log2
    q3 = Fr(2) ** fl * Fr(math.floor(2 ** (q3_log2 - fl) * 2 ** 40), 2 ** 40)
    pm = p2 * nL * q3 * KAPPA
    LANES, NBG = 256, D.NBATCH          # trials per batch, batches (variants) per group
    m = LANES * NBG                     # trials per group
    # group success: Pr[some A_i] >= sum_i Pr[A_i] - sum_{i<j} Pr[A_i and A_j] >= m pm (1 - (m - 1) PAIR / 2)
    q_lb = m * pm * (1 - (m - 1) * PAIR / 2)
    NG = int(-(-XREQ // q_lb)); NB = NG * NBG; N = LANES * NB
    assert NG * q_lb >= XREQ
    # rare path: a lane is flagged iff it passes W7 (p2, H1) and stage 3a (E16 uniform given validity: 2^-f16, H1);
    # a batch enters the rare path iff some lane is flagged (union bound: probability <= LANES p2 2^-f16)
    pf = p2 * Fr(1, 2 ** P['f16'])
    sw = D.VCTRL + cal['scanb']                   # per batch with a flagged lane: V update, cap test, scan start
    lane = cal['scanl'] + D.VLANE + cal['c_cv'] + cal['c01'] + nL * cal['c3a'] + cal['crest'] + \
        nL * (cal['c3b'] + D.FLAG3B + D.V3B)      # per flagged lane: the full stage-3b pass bounds the early abort
    vbar = LANES * pf * (sw + lane)
    vmax = sw + LANES * lane
    VMAX = int(-(-(MARGIN * NB * vbar) // 1))
    pre_ops = (P['nE14'] + P['nE15']) * PRE_PER_CAND + 2 ** 20 + PRE_BUILD
    init_ops = cal['c_init'] + INIT_ALLOW
    online_ops = NG * (cal['c_G'] + D.GCTRL + cal['c_B'])
    rare_ops = VMAX + vmax
    fin = D.VFIN_UNITS + Fr(D.VFIN_OPS, C)
    T = A_C + A_S + DEV + Fr(pre_ops + init_ops + online_ops + rare_ops, C) + fin
    pre = A_C + A_S + DEV + Fr(pre_ops, C)
    # Hoeffding over the N_G independent groups: a group's rare-path work lies in [0, NBG vmax] and its mean is at
    # most NBG vbar, so Pr[V > VMAX] <= exp(-2 ((MARGIN - 1) NB vbar)^2 / (NG (NBG vmax)^2))
    hexp = 2 * ((MARGIN - 1) * NB * vbar) ** 2 / (NG * (NBG * vmax) ** 2)
    eps = math.exp(-float(NG * q_lb)) * (1 + 1e-12)
    succ = 1 - eps - math.exp(-float(hexp)) - 2.0 ** -60 if log2f(hexp) > 6 else None
    tl, lt = claim5(T)
    return dict(R=R, C=C, counts=cal, nLstar=nL, F7=P['F7'], f16=P['f16'], nE14=P['nE14'], nE15=P['nE15'],
                log2_p2=log2f(p2), q3_model_log2=q3_log2, kappa=str(KAPPA), log2_p_model=log2f(pm),
                pair_log2=log2f(PAIR), trials_per_group=m, log2_q_group_lb=log2f(q_lb), NG=NG, NB=NB,
                NG_times_q_lb=float(NG * q_lb), log2_N=log2f(Fr(N)), N_times_p=float(N * pm),
                vbar=float(vbar), vmax=int(vmax), VMAX=VMAX, log2_hoeffding_exponent=log2f(hexp),
                ops=dict(pre=pre_ops, init=init_ops, online=online_ops, rare=rare_ops, fin_ops=D.VFIN_OPS),
                units=dict(A_C=A_C, A_S=A_S, DEV=DEV, pre=float(Fr(pre_ops, C)), online=float(Fr(online_ops, C)),
                           rare=float(Fr(rare_ops, C)), fin=float(fin)),
                log2_online_units=log2f(Fr(online_ops, C)), log2_rare_units=log2f(Fr(rare_ops, C)),
                T_num=T.numerator, T_den=T.denominator, log2_T=log2f(T), log2_T_80digits=lt, time_log2=tl,
                preprocessing_log2=claim5(pre)[0], success_lower_bound=succ,
                ops_per_batch_avg=float(Fr(cal['c_B'], NBG)), ops_per_trial_variants=float(Fr(cal['c_B'], m)),
                ops_per_trial=float(Fr(cal['c_B'] + cal['c_G'] + D.GCTRL, m)),
                log2_units_per_trial=log2f(Fr(cal['c_B'] + cal['c_G'] + D.GCTRL, m * C)))

if __name__ == '__main__':
    a = sys.argv[1:] + [None, None, None]
    out = ledger(int(a[0]), float(a[1]) if a[1] else None, float(a[2]) if a[2] else None)
    print(json.dumps(out, indent=1, default=str))
    assert out['success_lower_bound'] >= 0.39 and out['log2_hoeffding_exponent'] >= 6
```

<!-- file: selftest.py sha256=c63ccc7f9293b505ba14919c6124419a4e036eb647be6bfd6259ca1a7fd9067f -->
```python
#!/usr/bin/env python3
# selftest.py - checks of the r38fam package (proof.md Appendix A).  Extract the Appendix A files into one directory
# (snippet in A.0), then:  REPO_ROOT=/path/to/hash-smash python3 selftest.py 38 [full]
# Without REPO_ROOT the verifier comparisons are skipped and reported as such.  'full' re-enumerates L and L*
# (about 15 s).  Exits non-zero on the first failed check.
import os, sys, json, random, struct, math
import d1core as D, d1aux as X
import cert

R = int(sys.argv[1]); assert R == 38; full = 'full' in sys.argv[2:]; REPO = os.environ.get('REPO_ROOT'); res = {}
def ok(name, cond, val=None):
    res[name] = val if val is not None else bool(cond)
    if not cond: print(json.dumps(res, indent=1, default=str)); sys.exit('FAILED: ' + name)
hf = None
if REPO:
    sys.path.insert(0, REPO); from verifier import hash_functions as hf
pr = D.PAIRS[R]; ch = D.CH[R]
# 1. the published SFS pair (Table 5) collides after 38 steps from its chaining value, with the printed hash
o1, o2 = D.compress(pr['cv'], pr['m'], R), D.compress(pr['cv'], pr['mp'], R)
ok('sfs_pair_collides', o1 == o2 == pr['hash'])
if hf:
    v = lambda cv, w: list(hf._compress('sha256', tuple(cv), struct.pack('>16I', *w), R))
    ok('sfs_pair_collides_repo_verifier', v(pr['cv'], pr['m']) == v(pr['cv'], pr['mp']) == o1)
    for n in (0, 1, 55, 56, 64, 119, 128, 200):
        msg = bytes(random.Random(n).getrandbits(8) for _ in range(n))
        ok('digest_equals_repo_verifier_len%d' % n, D.digest(msg, R) == hf.digest(msg, 'sha256', R))
else: res['repo_verifier'] = 'skipped (REPO_ROOT not set)'
# 2. cells: with member x = the message printed second (M'), every cell of rows -4..37 holds
bad, Xc, Yc = D.cellcheck(R, pr['cv'], pr['mp'], pr['m']); ok('cells_hold_x_is_Mprime', not bad, 0)
Ax, Ex, Wx = D.trace(pr['cv'], pr['m'], R); Ay, Ey, Wy = D.trace(pr['cv'], pr['mp'], R)
rev = 0
for k, (u, w) in (('A', (Ax, Ay)), ('E', (Ex, Ey)), ('W', (dict(enumerate(Wx)), dict(enumerate(Wy))))):
    for i, s in ch[k].items():
        for c, sym in enumerate(s):
            b = 31 - c
            if sym in 'un' and ((u[i] >> b) & 1) != (1 if sym == 'u' else 0): rev += 1
res['un_bits_reversed_if_x_is_M'] = rev
X0 = Xc[1]; plus = [(i, 31 - c) for i, s in ch['E'].items() for c, sym in enumerate(s) if sym == '+']
pairs_ = [(i, b) for (i, b) in plus if (i + 1, b) in plus]
ok('plus_all_paired', all((i + 1, b) in plus or (i - 1, b) in plus for i, b in plus), len(plus))
ok('plus_pairs_equal', all(((X0[i] ^ X0[i + 1]) >> b) & 1 == 0 for i, b in pairs_), len(pairs_))
V = {'A': (Xc[0], Yc[0]), 'E': (Xc[1], Yc[1]), 'W': (dict(enumerate(Xc[2])), dict(enumerate(Yc[2])))}
fail = []
for (w1, i1, b1, op, w2, i2, b2) in ch['X']:
    r_ = [(((V[w1][s][i1] >> b1) ^ (V[w2][s][i2] >> b2)) & 1 == 0) == (op == '=') for s in (0, 1)]
    if not all(r_): fail.append(['%s%d[%d]%s%s%d[%d]' % (w1, i1, b1, '=' if op == '=' else '!=', w2, i2, b2), r_])
res['printed_two_bit_failing_(x,y)'] = fail
ok('printed_two_bit_failures_as_stated', [f[0] for f in fail] == ['W25[4]=W25[9]'])
# 3. Step-1 solution S, Step-2 constants, the freedom sets (exact), and the data the preregistered SMC read
P = D.setup(R, full=full)
res['S_W8_13_x'] = ' '.join('%08x' % w for w in P['Wx'][8:14]); res['Lstar_size'] = len(P['Lstar'])
res['constants'] = dict((k, '%08x' % P[k]) for k in ('c7', 'd7', 't7', 'c6', 'd6', 't6', 'k3'))
if full: ok('L_and_Lstar_sizes', (len(P['L']), len(P['Lstar'])) == (8, 1), [len(P['L']), len(P['Lstar']), P['nE14'], P['nE15']])
ok('tables_digest_as_preregistered', D.tables_digest(R) == 'bf3bcc643e37895acd208384cebfd8c3f4ff012bbbc123a26a801b88698a4544',
   D.tables_digest(R))
d0 = P['Lstar'][0]
res['stage3a'] = dict(ck16='%08x' % d0['ck16'], m16='%08x' % P['m16'], v16='%08x' % d0['v16'], f16=P['f16'])
# 4. F7: the affine parts (fparts) have exactly |F7| words (fcount.c's exhaustive count); the circuit's factored W7
#    test (fails7, evaluated here on integers) equals 'not in F7' on 2^20 random words and on 2^16 words drawn from
#    the affine parts (the exhaustive 2^32 comparison is f7check.c); sampled rate against the exact size (5 sigma)
Fp = X.fparts(P['d7'], P['t7']); rnd = random.Random(R)
class IntNet:
    def XOR(self, a, b): return a ^ b
    def OR(self, a, b): return a | b
    def AND(self, a, b): return a & b
    def NOT(self, a): return a ^ 1
def f7int(w): return D.fails7(IntNet(), [(w >> j) & 1 for j in range(32)])
def inparts(w):
    for _, x0, bs in Fp[0]:
        y = w ^ x0
        for v_ in bs:
            if (y >> ((v_ & -v_).bit_length() - 1)) & 1: y ^= v_
        if y == 0: return True
    return False
n = 1 << 20; h = agree = 0
for _ in range(n):
    w = rnd.getrandbits(32); a_ = D.inF(w, P['d7'], P['t7']); h += a_; agree += a_ == inparts(w) == (not f7int(w))
acc = 0
for _ in range(1 << 16):
    _, x0, bs = Fp[0][rnd.randrange(len(Fp[0]))]; w = x0
    for v_ in bs:
        if rnd.getrandbits(1): w ^= v_
    acc += D.inF(w, P['d7'], P['t7']) and not f7int(w)
p = P['F7'] / 2 ** 32
ok('F7_affine_parts_and_factored_test', Fp[1] == P['F7'] and agree == n and acc == 1 << 16, [[len(x[2]) for x in Fp[0]], Fp[1], agree, acc])
ok('F7_sampled', abs(h - n * p) < 5 * math.sqrt(n * p * (1 - p)), [h, round(n * p, 1)])
# 5. operation counts (data-independent; calibrate asserts c_G and the rare-path parts equal over three groups and
#    runs every variant program on the three groups' memory images against the evaluator's fail plane)
cal = D.calibrate(R, P); res['counts'] = cal
ok('register_budget', cal['maxreg'] < 64, cal['maxreg'] + 1)
ok('variant_count', len(cal['c_Bv']) == D.NBATCH == 1 << D.UB and sum(cal['c_Bv']) == cal['c_B'], len(cal['c_Bv']))
ok('rare_register_budget', 4 + cal['live_lane'] <= 64 and cal['live_3b'] + 1 <= 64, [4 + cal['live_lane'], cal['live_3b'] + 1])
res['family'] = dict(FAM=[list(f) for f in D.FAM], UB=D.UB, LO=D.LO, NBATCH=D.NBATCH)
# 6. the family and the batches against the repository verifier (or d1core).  (a) 100 groups: the solved words give
#    the fixed words and zero sums on the expanded schedule of every lane checked; for 3 batches of each group
#    (positions 0, random, NBATCH-1) every lane's W7 decision and W7 + stage-3a decision (flag) equal the evaluator's
#    planes, the CV1 of every flagged lane and of every 16th lane through lane_cv, and Lemma 1's reproduction of S on
#    rows 0..13 from every W7 lane's W0..W7.  (b) the flag path: 2,048 more batches; every lane the evaluator marks as
#    passing W7 or as flagged is recomputed.  (c) the counted programs: every variant program, run by run_vm on the
#    memory image of 2 groups, gives every lane's flag decision (verifier) and the calibrated count.
comp = (lambda cv, w: list(hf._compress('sha256', tuple(cv), struct.pack('>16I', *w), R))) if hf else (lambda cv, w: D.compress(cv, w, R))
def dec(cv):
    W = D.ref_words(P, cv); p7 = D.inF(W[7], P['d7'], P['t7'])
    e16 = (d0['ck16'] + D.s0(W[1]) + W[0]) & D.M32; nb_ = bin((e16 ^ d0['v16']) & P['m16']).count('1')
    return W, p7, p7 and nb_ == 0, p7 and nb_ == 1
def famok(blk):
    Z = D.trace(D.IV, blk, R)[2]
    return not (any(Z[e[1]] != v for e, v in D.FW.items()) or any(sum(D.wv(x, Z) for x in z) & D.M32 for z in D.ZS))
mis = nl = n7 = nf = near = fam = 0; rnd = random.Random(1000 + R); pg = D.prog(R); grp = []
for g in range(100):
    base, M0, rL, rb = D.group_setup(D.Sc(), pg, R, rnd.getrandbits(256), rnd.getrandbits(256))
    if g < 2: grp.append((base, M0, rL, rb))
    for k in (0, rnd.randrange(D.NBATCH), D.NBATCH - 1):
        c = rb + k; fl, f7 = pg.planes(base, rL, c)
        for L in range(256):
            blk = M0 + [D.w15(L, rL, c)]; cv = comp(D.IV, blk); nl += 1
            if L % 32 == 0: fam += not famok(blk)
            W, p7, flag, nr = dec(cv); near += nr
            mis += (p7 != (not (f7 >> L) & 1)) + (flag != (not (fl >> L) & 1)); n7 += p7; nf += flag
            if flag or L % 16 == 0: mis += D.lane_cv(D.Sc(), R, base, rL, c, L) != cv
            if p7:
                A_, E_, _ = D.trace(cv, W + P['Wx'][8:16], 14)
                mis += any(A_[i] != P['Sx'][0][i] or (i >= 4 and E_[i] != P['Sx'][1][i]) for i in range(14))
ok('family_constraints', fam == 0, fam)
ok('batch_bit_exact', mis == 0, dict(lanes=nl, mismatches=mis, w7_pass=n7, stage3a_one_bit_off=near, flagged=nf))
mis = n7 = nf = near = 0; rnd = random.Random(2000 + R)
for g in range(64):
    base, M0, rL, rb = D.group_setup(D.Sc(), pg, R, rnd.getrandbits(256), rnd.getrandbits(256)); I = pg.inputs(base, rL, 0)
    for k in range(D.NBATCH):
        c = rb + k
        for i in range(D.UB): I['uhi[%d]' % i] = D.WORD if (c >> i) & 1 else 0
        fl, f7 = pg.f(I)
        for L in range(256):
            if (f7 >> L) & 1 and (fl >> L) & 1: continue
            cv = comp(D.IV, M0 + [D.w15(L, rL, c)]); W, p7, flag, nr = dec(cv); near += nr; n7 += p7; nf += flag
            mis += (not p7) + (flag != (not (fl >> L) & 1))
            if flag: mis += D.lane_cv(D.Sc(), R, base, rL, c, L) != cv
ok('flag_path_bit_exact', mis == 0, dict(batches=64 * D.NBATCH, w7_pass=n7, stage3a_one_bit_off=near, flagged=nf, mismatches=mis))
mis = nl = 0
for u in range(D.NBATCH):
    vn, vf = pg.variant(u); vp = D.emit(vn, vf)
    for base, M0, rL, rb in grp:
        I = pg.inputs(base, rL, u); m = pg.mem(I); m[vn.inputs['ones']] = D.WORD; ops, fl, hit = D.run_vm(vp, m, vf[1])
        mis += ops != cal['c_Bv'][u]
        for L in range(256): mis += dec(comp(D.IV, M0 + [D.w15(L, rL, u)]))[2] != (not (fl >> L) & 1); nl += 1
ok('variant_programs_bit_exact', mis == 0, dict(lanes=nl, mismatches=mis))
# 7. Step 3 end to end on the published pair's chaining value: the counted code derives W0..W7, finds the published
#    (W14, W15) in L*, passes every row 16..37 and returns exactly the published pair (x = M', y = M)
li, Xw, Yw, n3b = D.step3(D.Sc(), P, pr['cv'])
ok('step3_reproduces_published_pair', li is not None and Xw == pr['mp'] and Yw == pr['m'], [li, n3b])
# 8. the code of the organizer experiment d1-q3-smc (byte-identical to d2's): exact row 16 (the same 32 words as
#    smc.py's enumeration), one replicate on a fixed seed reproduces its recorded estimate, and every rebuilt pair is a
#    38-step semi-free-start collision under the repository verifier
XL = D.xlist(R); V16 = D.row16(P, XL)
ok('q3x_row16_words', len(V16[0]) == 32 and V16[1] == 13, [len(V16[0]), V16[1]])
z, st, hits, prs, bad = D.mini_smc(P, XL, V16, random.Random(1), D.Q3X['NP'], D.Q3X['MS'], D.Q3X['MT'])
ok('q3x_replicate_seed1', abs(math.log2(z) + 101.01960542679035) < 1e-9 and hits == len(prs) == 69 and bad == 0,
   [round(math.log2(z), 6), hits, bad])
if hf: ok('q3x_pairs_sfs_repo_verifier', all(v(cv, wx) == v(cv, wy) and wx != wy for cv, wx, wy in prs), len(prs))
# 9. the ledger
led = cert.ledger(R)
res['ledger'] = dict((k, led[k]) for k in ('log2_p_model', 'trials_per_group', 'log2_q_group_lb', 'NG', 'NG_times_q_lb', 'log2_N',
                                           'N_times_p', 'vbar', 'vmax', 'VMAX', 'log2_online_units', 'log2_rare_units', 'log2_T',
                                           'time_log2', 'preprocessing_log2', 'success_lower_bound', 'log2_hoeffding_exponent',
                                           'ops_per_batch_avg', 'ops_per_trial'))
ok('success_at_least_0.39', led['success_lower_bound'] >= 0.39)
print(json.dumps(res, indent=1, default=str)); print('selftest r%d: all checks passed' % R)
```

<!-- file: grp38fam.c sha256=d9e2023abf94f6b5c8214fcf6ed14d4016c241b1bb4569656713adc76a8f13cd -->
```c
/* grp38fam.c - local H1/H5 evidence (proof.md Section 9) on the r38fam first-block family, 38 steps.
   Each group draws 8 words (W0, W1, W2, W3, W4, W9, W11, W14), rL (8 bits) and rb (5 bits) from xoshiro256** (seeded per thread), solves
   the family words W10, W12, W8, W7, W6, W5, W13 as d1core.family() does (checked on the expanded schedule of every trial), and runs its
   32 batches x 256 lanes: trial (k, L) has W15 = ((L ^ rL) << 9) | (((rb + k) mod 32) << 27).  Every trial
   is the full 38-step compression from the IV with feed-forward (no shortcut).  Per trial: valid = W7 in F7 (W7 = c7 -
   CV1[0]); flagged = valid and stage 3a (E16 = ck16 + s0(W1) + W0 on m16 = v16, W0, W1 by the Step-2 equations).
   Prints JSON: totals; per-group sums of squares of the valid and flagged counts (within-group dispersion, H5);
   batches with >= 1 / >= 2 valid lanes and >= 1 flagged lane; valid and flagged pairs inside groups; valid trials per
   variant; family violations; chi-square (255 df) of every byte of CV1 over all trials and of every byte of the Step-2
   words W0..W5 over the valid trials (H1).  usage: grp38fam groups seed threads   (cc -O3 -pthread) */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
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
#define IF(x,y,z) (((x) & (y)) ^ (~(x) & (z)))
#define MAJ(x,y,z) (((x) & (y)) ^ ((x) & (z)) ^ ((y) & (z)))
#define R 38
#define NB 32
static long G; static uint64_t SEED; static int NT;
static const uint32_t C7 = 0x8f6c89c5u, D7 = 0x20000000u, T7 = 0x03bff800u, A0 = 0xb75dae71u, A1 = 0xda6c35e0u,
  CK16 = 0xfe314838u, M16 = 0x4c431a80u, V16 = 0x48030280u;
static uint64_t rotl(uint64_t x, int k) { return (x << k) | (x >> (64 - k)); }
static uint64_t nxt(uint64_t *s) { uint64_t r = rotl(s[1] * 5, 7) * 9, t = s[1] << 17; s[2] ^= s[0]; s[3] ^= s[1]; s[1] ^= s[2];
  s[0] ^= s[3]; s[2] ^= t; s[3] = rotl(s[3], 45); return r; }
typedef struct { int id; uint64_t trials, w7, valid, flag, b1, b2, bf, vpairs, fpairs, bad, vsq, fsq, nbv[NB], cvh[32][256], wh[24][256]; } job;
static void *work(void *arg) {
  job *j = arg; uint64_t s[4] = {SEED ^ 0x9e3779b97f4a7c15ull * (j->id + 1), SEED + j->id, 0x1234567ull * (j->id + 3), 0xabcdefull + j->id};
  for (int i = 0; i < 20; i++) nxt(s);
  for (long g = j->id; g < G; g += NT) {
    uint32_t w0[16]; uint64_t r[5]; for (int i = 0; i < 5; i++) r[i] = nxt(s);
    w0[0] = (uint32_t)(r[0] >> 0);
    w0[1] = (uint32_t)(r[0] >> 32);
    w0[2] = (uint32_t)(r[1] >> 0);
    w0[3] = (uint32_t)(r[1] >> 32);
    w0[4] = (uint32_t)(r[2] >> 0);
    w0[9] = (uint32_t)(r[2] >> 32);
    w0[11] = (uint32_t)(r[3] >> 0);
    w0[14] = (uint32_t)(r[3] >> 32);
    uint32_t rL = (uint32_t)r[4] & 255, rb = (uint32_t)(r[4] >> 8) & (NB - 1);
    w0[10] = 0x00000000u - s0(w0[2]) - w0[1];
    w0[12] = 0x00000000u - s0(w0[4]) - w0[3];
    w0[8] = 0x00000000u - s0(w0[9]);
    w0[7] = 0x00000000u - (s1(w0[14]) + w0[9] + s0(w0[1]) + w0[0]) - s0(w0[8]);
    w0[6] = 0x00000000u - s1(0xd216d391u) - s0(w0[7]);
    w0[5] = 0x00000000u - w0[14] - s0(w0[6]);
    w0[13] = 0xd216d391u - s1((s1((s1(w0[14]) + w0[9] + s0(w0[1]) + w0[0])) + w0[11] + s0(w0[3]) + w0[2])) - s0(w0[5]) - w0[4];
    uint64_t gv = 0, gf = 0;
    for (int k = 0; k < NB; k++) { int nv = 0, nf = 0; uint32_t c = (rb + k) & (NB - 1);
      for (int L = 0; L < 256; L++) {
        uint32_t w[64]; for (int i = 0; i < 15; i++) w[i] = w0[i]; w[15] = (((uint32_t)L ^ rL) << 9) | (c << 27);
        for (int i = 16; i < R; i++) w[i] = s1(w[i-2]) + w[i-7] + s0(w[i-15]) + w[i-16];
        if (w[20] != 0xd216d391u || (uint32_t)(w[12] + s0(w[4]) + w[3]) || (uint32_t)(w[8] + s0(w[9])) || (uint32_t)(w[6] + s1(0xd216d391u) + s0(w[7])) || (uint32_t)(s0(w[2]) + w[1] + w[10]) || (uint32_t)((s1(w[14]) + w[9] + s0(w[1]) + w[0]) + w[7] + s0(w[8])) || (uint32_t)(w[5] + w[14] + s0(w[6]))) j->bad++;
        uint32_t a=IV[0],b=IV[1],cc=IV[2],d=IV[3],e=IV[4],f=IV[5],gg=IV[6],h=IV[7];
        for (int i = 0; i < R; i++) { uint32_t t1 = h + S1(e) + IF(e, f, gg) + K[i] + w[i], t2 = S0(a) + MAJ(a, b, cc);
          h = gg; gg = f; f = e; e = d + t1; d = cc; cc = b; b = a; a = t1 + t2; }
        uint32_t v[8] = {a + IV[0], b + IV[1], cc + IV[2], d + IV[3], e + IV[4], f + IV[5], gg + IV[6], h + IV[7]};
        j->trials++;
        for (int q = 0; q < 8; q++) for (int y8 = 0; y8 < 4; y8++) j->cvh[4 * q + y8][(v[q] >> (8 * y8)) & 255]++;
        uint32_t W7 = C7 - v[0]; if ((uint32_t)(s0(W7 + D7) - s0(W7)) != T7) continue;
        j->w7++; j->valid++; nv++; j->nbv[c]++;
        /* the paper's Step-2 equations: A[-1..-4] = CV1[0..3], E[-1..-4] = CV1[4..7], A0..A3, E4, E5 from S */
        uint32_t a1=v[0],a2=v[1],a3=v[2],a4=v[3],e1=v[4],e2=v[5],e3=v[6],e4=v[7];
        uint32_t E0 = A0 + a4 - S0(a1) - MAJ(a1,a2,a3), W0 = E0 - a4 - e4 - S1(e1) - IF(e1,e2,e3) - K[0];
        uint32_t E1 = A1 + a3 - S0(A0) - MAJ(A0,a1,a2), W1 = E1 - a3 - e3 - S1(E0) - IF(E0,e1,e2) - K[1];
        uint32_t SA2 = 0x479b4dc8u, SA3 = 0xd374b0d8u, SE4 = 0x627cb061u, SE5 = 0x1e847683u;
        uint32_t E2 = SA2 + a2 - S0(A1) - MAJ(A1,A0,a1), W2 = E2 - a2 - e2 - S1(E1) - IF(E1,E0,e1) - K[2];
        uint32_t E3 = SA3 + a1 - S0(SA2) - MAJ(SA2,A1,A0), W3 = E3 - a1 - e1 - S1(E2) - IF(E2,E1,E0) - K[3];
        uint32_t W4 = SE4 - A0 - E0 - S1(E3) - IF(E3,E2,E1) - K[4], W5 = SE5 - A1 - E1 - S1(SE4) - IF(SE4,E3,E2) - K[5];
        uint32_t W2s[6] = {W0, W1, W2, W3, W4, W5};
        for (int q = 0; q < 6; q++) for (int y8 = 0; y8 < 4; y8++) j->wh[4 * q + y8][(W2s[q] >> (8 * y8)) & 255]++;
        if (((CK16 + s0(W1) + W0) & M16) == V16) { j->flag++; nf++; } }
      j->b1 += nv >= 1; j->b2 += nv >= 2; j->bf += nf >= 1; gv += nv; gf += nf; }
    j->vpairs += gv * (gv - 1) / 2; j->fpairs += gf * (gf - 1) / 2; j->vsq += gv * gv; j->fsq += gf * gf; }
  return 0; }
static job jb[64];
int main(int argc, char **argv) {
  if (argc < 4) { fprintf(stderr, "usage: grp38fam groups seed threads\n"); return 2; }
  G = atol(argv[1]); SEED = strtoull(argv[2], 0, 10); NT = atoi(argv[3]);
  { /* the published pair's chaining value: Step 2 and stage 3a pass and W0, W1 are the published M' words */
    uint32_t v[8] = {0xcd278980,0x1b12a052,0xb87cc8a6,0xa9e059c5,0xc9c3db85,0x6ca4b5b5,0x63d13ac1,0xc0329f1e};
    uint32_t a1=v[0],a2=v[1],a3=v[2],a4=v[3],e1=v[4],e2=v[5],e3=v[6],e4=v[7], W7 = C7 - a1;
    uint32_t E0 = A0 + a4 - S0(a1) - MAJ(a1,a2,a3), W0 = E0 - a4 - e4 - S1(e1) - IF(e1,e2,e3) - K[0];
    uint32_t E1 = A1 + a3 - S0(A0) - MAJ(A0,a1,a2), W1 = E1 - a3 - e3 - S1(E0) - IF(E0,e1,e2) - K[1];
    int ok = (uint32_t)(s0(W7 + D7) - s0(W7)) == T7 && ((CK16 + s0(W1) + W0) & M16) == V16 && W0 == 0x48fc271bu && W1 == 0x9fca20cdu;
    if (!ok) { fprintf(stderr, "published CV check FAILED\n"); return 1; } }
  pthread_t th[64];
  for (int i = 0; i < NT; i++) { memset(&jb[i], 0, sizeof(job)); jb[i].id = i; pthread_create(&th[i], 0, work, &jb[i]); }
  static job S; memset(&S, 0, sizeof S);
  for (int i = 0; i < NT; i++) { pthread_join(th[i], 0);
    S.trials += jb[i].trials; S.w7 += jb[i].w7; S.valid += jb[i].valid; S.flag += jb[i].flag; S.b1 += jb[i].b1; S.b2 += jb[i].b2;
    S.bf += jb[i].bf; S.vpairs += jb[i].vpairs; S.fpairs += jb[i].fpairs; S.bad += jb[i].bad; S.vsq += jb[i].vsq; S.fsq += jb[i].fsq;
    for (int n = 0; n < NB; n++) S.nbv[n] += jb[i].nbv[n];
    for (int p = 0; p < 32; p++) for (int b = 0; b < 256; b++) S.cvh[p][b] += jb[i].cvh[p][b];
    for (int p = 0; p < 24; p++) for (int b = 0; b < 256; b++) S.wh[p][b] += jb[i].wh[p][b]; }
  printf("{\"groups\":%ld,\"seed\":%llu,\"threads\":%d,\"batches_per_group\":%d,\"trials\":%llu,\"valid\":%llu,\"flagged\":%llu,"
    "\"valid_sumsq\":%llu,\"flagged_sumsq\":%llu,\"batches_ge1_valid\":%llu,\"batches_ge2_valid\":%llu,\"batches_ge1_flagged\":%llu,"
    "\"valid_pairs_in_groups\":%llu,\"flagged_pairs_in_groups\":%llu,\"family_violations\":%llu,\"valid_by_variant\":[",
    G, (unsigned long long)SEED, NT, NB, (unsigned long long)S.trials, (unsigned long long)S.valid, (unsigned long long)S.flag,
    (unsigned long long)S.vsq, (unsigned long long)S.fsq, (unsigned long long)S.b1, (unsigned long long)S.b2, (unsigned long long)S.bf,
    (unsigned long long)S.vpairs, (unsigned long long)S.fpairs, (unsigned long long)S.bad);
  for (int n = 0; n < NB; n++) printf("%s%llu", n ? "," : "", (unsigned long long)S.nbv[n]);
  printf("],\"cv1_byte_chi2\":[");
  for (int p = 0; p < 32; p++) { double e = S.trials / 256.0, c = 0; for (int b = 0; b < 256; b++) c += (S.cvh[p][b] - e) * (S.cvh[p][b] - e) / e;
    printf("%s%.1f", p ? "," : "", c); }
  printf("],\"w0_5_byte_chi2_valid\":[");
  for (int p = 0; p < 24; p++) { double e = S.valid / 256.0, c = 0; for (int b = 0; b < 256; b++) c += (S.wh[p][b] - e) * (S.wh[p][b] - e) / e;
    printf("%s%.1f", p ? "," : "", c); }
  printf("]}\n");
  return 0; }
```

<!-- file: grp38fam_stats.py sha256=e4b69faab662e2feea2c459ba65ec9aea869c4dfeb3c9b1175fdee2bda85ddfc -->
```python
#!/usr/bin/env python3
# grp38fam_stats.py - statistics of grp38fam.c output (proof.md Section 9, H1 and H5).  usage: grp38fam_stats.py out.json
# Rates against the exact single-trial values under H1 (p2 = |F7| / 2^32; flagged: p2 2^-10); per-group dispersion of
# the valid and flagged counts and the implied average Pr[A_j | A_i] over ordered pairs i != j of one group (H5);
# batch-level counts against independent lanes; valid trials per variant (chi-square, 31 df); byte chi-squares (255 df).
import sys, json, math
d = json.loads(open(sys.argv[1]).read()); G = d['groups']; NB = d['batches_per_group']; m = 256 * NB; N = d['trials']
assert N == G * m and d['family_violations'] == 0
p = 287309824 / 2 ** 32; pf = p / 1024; out = {}
for name, r, tot, sq in (('valid', p, d['valid'], d['valid_sumsq']), ('flagged', pf, d['flagged'], d['flagged_sumsq'])):
    mu = tot / G; s2 = (sq - G * mu * mu) / (G - 1); e = m * r; var = m * r * (1 - r)
    z = (tot - G * e) / math.sqrt(G * var); D = s2 / var; zD = (D - 1) / math.sqrt(2 / (G - 1))
    # E[n(n-1)] = sum_{i != j} Pr[A_i A_j]; avg Pr[A_j | A_i] = E[n(n-1)] / ((m - 1) E[n])
    pairs = (sq - tot) / G; cond = pairs / ((m - 1) * mu)
    se = math.sqrt(2 / (G - 1)) * var / ((m - 1) * mu)          # standard error of the conditional rate (Gaussian approx.)
    out[name] = dict(total=tot, expected=G * e, z=z, log2_rate=math.log2(tot / N), dispersion=D, z_dispersion=zD,
                     avg_cond=cond, rate=tot / N, cond_over_rate=cond / (tot / N), cond_over_rate_plus3se=(cond + 3 * se) / (tot / N))
na, nf = d['valid'], d['flagged']
out['stage3a_given_valid'] = dict(rate_log2=math.log2(nf / na), z=(nf - na / 1024) / math.sqrt(na / 1024 * (1 - 1 / 1024)))
nb = G * NB
for name, x, q in (('batches_ge1_valid', d['batches_ge1_valid'], 1 - (1 - p) ** 256),
                   ('batches_ge2_valid', d['batches_ge2_valid'], 1 - (1 - p) ** 256 - 256 * p * (1 - p) ** 255),
                   ('batches_ge1_flagged', d['batches_ge1_flagged'], 1 - (1 - pf) ** 256)):
    out[name] = dict(count=x, of=nb, independent_lanes=nb * q, z=(x - nb * q) / math.sqrt(nb * q * (1 - q)))
v = d['valid_by_variant']; ev = na / NB
out['valid_by_variant_chi2_31df'] = sum((x - ev) ** 2 / ev for x in v)
for k in ('cv1_byte_chi2', 'w0_5_byte_chi2_valid'):
    c = d[k]; out[k] = dict(n=len(c), mean=sum(c) / len(c), min=min(c), max=max(c), above_330_5=sum(x > 330.5 for x in c))
print(json.dumps(out, indent=1))
```

<!-- file: f7check.c sha256=8492142b05cc461165834e8720a299ad893027be6c46ad224e32d8b52321f4e4 -->
```c
/* f7check.c - exhaustive check of the circuit's factored W7 test (d1core.fails7, Th0rgal's PR #674 form) against the
   definition of F7 = {w : s0(w + 2^29) - s0(w) = 0x03bff800 mod 2^32} over all 2^32 words; prints |F7| and the number
   of disagreements (must be 287309824 and 0).  usage: f7check   (cc -O3) */
#include <stdio.h>
#include <stdint.h>
#define ROR(x,n) (((x) >> (n)) | ((x) << (32 - (n))))
#define s0(x) (ROR(x,7) ^ ROR(x,18) ^ ((x) >> 3))
#define B(j) ((w >> (j)) & 1u)
int main(void) {
  uint64_t inF = 0, bad = 0; uint32_t w = 0;
  do {
    int in = (uint32_t)(s0(w + 0x20000000u) - s0(w)) == 0x03bff800u; inF += in;
    uint32_t f0 = (B(1) ^ B(12)) | (1 ^ B(8) ^ B(25)) | (1 ^ B(14) ^ B(18));
    uint32_t f1 = (B(2) ^ B(13)) | (1 ^ B(9) ^ B(26)) | (1 ^ B(15) ^ B(19));
    uint32_t w3 = B(3) ^ B(14);
    uint32_t f2 = (w3 ^ B(31)) | (1 ^ w3 ^ B(10) ^ B(27)) | (1 ^ w3 ^ B(16) ^ B(20));
    uint32_t fail = f0 | (B(29) & (f1 | (B(30) & f2)));
    bad += (fail == 0) != in;
  } while (++w);
  printf("{\"F7\":%llu,\"disagreements\":%llu}\n", (unsigned long long)inF, (unsigned long long)bad);
  return bad != 0 || inF != 287309824ull; }
```

<!-- file: run_exp_org.py sha256=fcd9266d46b659c3e69273fc63e9b22a9dcdc8a7240fb51e9f1d52fc8b0ee5e3 -->
```python
#!/usr/bin/env python3
# run_exp_org.py - local emulation of the organizer requests of the r38fam package's experiments with the public seed
# protocol of experiments/runner.py (seed 'hashsmash-public-seed-v1', no holdout nonce, 256 trials): builds the
# request exactly as _python_result does, runs d1core.py twice (python -B -s), compares stdout bytes, recomputes the
# target digest of every returned pair with the repository verifier, and summarizes.
# usage: REPO_ROOT=... run_exp_org.py OUT.json [own]   ('own': seed 'r38fam-own-seeds' instead of the public seed)
import os, sys, json, hashlib, subprocess, time
REPO = os.environ['REPO_ROOT']; sys.path.insert(0, REPO)
from verifier.frontier_tracks import get_frontier_track
from verifier.hash_functions import digest
from verifier import hash_functions as hf
tr = get_frontier_track('sha256-r38-exploratory')
def canon(v): return json.dumps(v, sort_keys=True, separators=(',', ':'), ensure_ascii=True, allow_nan=False).encode()
cfg = tr.config_sha256(); seed = 'r38fam-own-seeds' if 'own' in sys.argv[2:] else 'hashsmash-public-seed-v1'
sm = canon({"domain": "hashsmash-experiments-v1", "seed": seed, "holdout_nonce": None, "target_config_sha256": cfg})
res = dict(track=tr.id, profile=tr.profile_id, seed=seed, target_config_sha256=cfg, python=sys.version.split()[0],
           program_sha256=hashlib.sha256(open('d1core.py', 'rb').read()).hexdigest())
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
             repeated=len(pairs) - len(set(pairs)))
    if eid == 'd1-first-block-r38':
        for k in ('lanes_checked', 'mismatches', 'w7_pass', 'hits', 'stage3b'): s[k] = sum(r['observations'][k] for r in rows)
        # every returned pair: common first block, distinct second blocks, the second-block compressions from CV1
        # (repository compression) and the first-block chaining value
        ok = 0
        for r in ret:
            a, b = bytes.fromhex(r['message_a_hex']), bytes.fromhex(r['message_b_hex'])
            ok += a[:64] == b[:64] and a[64:] != b[64:]
        s['returned_common_first_block'] = ok
    else:
        K = 20; s.update(witness=sum(1 for r in rows[:K] if r['message_a_hex']), pooled_pass=rows[K]['message_a_hex'] is not None,
                         pooled_log2=rows[K]['observations']['log2_pooled_mean'], log2=[r['observations']['log2_estimate'] for r in rows[:K]],
                         tail=sum(r['observations']['tail_successes'] for r in rows[:K]), verified=sum(r['observations']['verified_pairs'] for r in rows[:K]),
                         failed=sum(r['observations']['failed_rebuilds'] for r in rows[:K]))
        sfs = 0
        for r in ret:
            a, b = bytes.fromhex(r['message_a_hex']), bytes.fromhex(r['message_b_hex'])
            cv = tuple(int.from_bytes(a[4*i:4*i+4], 'big') for i in range(8))
            if a[:32] == b[:32] and a[32:] != b[32:] and hf._compress('sha256', cv, a[32:], 38) == hf._compress('sha256', cv, b[32:], 38): sfs += 1
        s['sfs_collisions_repo_verifier'] = sfs
    res[eid] = s
open(sys.argv[1], 'w').write(json.dumps(res, indent=1)); print(json.dumps(res, indent=1))
```

<!-- file: PREREG_fb.txt sha256=48e3940abc772110d38520f3ba67c2ba26313f0e4bf7b7d078a220f3424d632d -->
```text
r38fam first-block organizer experiment (d1-first-block-r38): design record, frozen 2026-10-09T15:15:56Z before any run of
the frozen program below on the public seed or on our own seed set 'r38fam-own-seeds'.
Program: experiments/d1core.py sha256 5a0903c07a6138be9dcade7950090ded195d8535361f9bef3cbed3b456f3f88b (d1core.experiment).
Design: per organizer trial one group of the r38fam family (coins from SHAKE-256(seed)), NB_EXP = 4 batches of 256 lanes
(variants rb .. rb+3 mod 32), CHK = 8 seed-chosen lanes per batch plus every lane the circuit marks as passing W7 and every
flagged lane, checked against the scalar 38-step compression; calibrate runs the counted variant programs 0 and 31 against
the gate evaluator on three groups.  A trial returns the pair of its first flagged lane iff every check passed.
Expectation (not a test; no statistical inference is drawn from organizer counts): mismatches 0 in every trial; returned
pairs: a trial returns a pair with probability 1 - (1 - p2 2^-10)^1024 = 0.06471 under the independent-uniform model
(p2 = 2^-3.90197), i.e. about 16.6 of 256; we state the witness range 6..30; full collisions 0.
Disclosure: a development build (lane offset 8, a different family) was run once through the local organizer-runner replay
(public seed, no holdout nonce) before this freeze; its numbers are not used.
Amendment 2026-10-09T15:18:41Z: the organizer runner accepts only numeric observations, and the frozen program reported
variant_ops as a list; the observation is now the sum of the two calibrated variant counts (87,359).  No other change (design,
checks, coins and returned pairs are unchanged).  Amended program sha256 1b3e62de7e4377a4796459ea49c7e428059c1896ff1fa76247d04b998d20badc.
Before the amendment the frozen program had been run on our own seed set (12 pairs) and on the public seed (17 pairs, 0
mismatches) with the participant emulation run_exp_org.py; the runs were repeated with the amended program.
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
