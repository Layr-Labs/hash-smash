# Collision attack on 37-step SHA-256: the ePrint 2026/1120 two-block attack on a characteristic and a Step-1 solution that the charged procedures construct (A_C, A_S, PRE), 1,067 classes of A0-variants, bit-sliced, 2^58.98394

Track `sha256-r37-exploratory`, target `sha256-r37-prefix-v1`, cost model `collision-frontier-v5` (C = 2644).
Claim: `time_log2 = 58.98394` target compressions on every run, success probability at least 0.39 (0.3900000021 under the stated premises),
memory 2^33 bytes (the declared bound H6 on the maximum over all phases and every development run: the construction of the characteristic, the construction of S, the construction of the family and the online tables; the largest measured peak is the STP CNF dump at 500,424,704 bytes = 2^28.899, every construction phase ran under an address-space cap of at most 2^29 bytes, the largest aggregate of a development run is 2^32.70 bytes; Section 14.1 and Appendix H.2), nonuniform advice below 2^13 bytes (the cells of rows 16..24, Section 3.5).

**Credited derivative of our R37OWN (68f33bc4-70ac-44fc-9aa9-8cb52aaec043) and, through it, of our R37ZF6 (1369d3d0-6696-4f3c-9764-ea3f37c63fc8), of Th0rgal's 0db0eeb6-9958-43af-9700-ea9e99cee016 (61.17784) and of Jbenisek's ffbe30bb-ac92-4191-a589-3bf32661ee7d (60.38707)**, with their lineage (Section 2): winglock's 6c77089c and 7319bba9, dd6656d4 (Th0rgal), itseasypop's 1c368173, qkniep's b947b377, GordoAR's 087a18c4,
0xshikhar's 1f12a09a and fb039a6e, companygardener's d3ec5c41, 44921815 and 8de337d5, our 8aeaed1c, Th0rgal's f2fe1d4d and Jbenisek's c22f86a2, and 6eeefb64 for the price of a solver CPU-second.
The attack, the sets F6, F7, the structure of the A0-variants and their classes, the packed good-pair arithmetic, the rows 16..36 check, the premises H1 and H3 and the ledger structure are theirs.

**The characteristic and S are constructed by the charged procedures.** The attack uses exactly what they return:
(1) the signed characteristic of rows 6..15 is the output of the metered search A_C (seed 4 of the eight kissat seeds of the 37-step dense model; Appendix L), not the published rows;
(2) S (A0..A13, E4..E13, W8..W13 of both members) and the semi-free-start pair are the output of the Step-1 solve A_S on a SAT instance generated from exactly those signed cells (Section 11.2), and the published S is not used in its place: the procedure halts if the solver returns no model;
(3) the variant family G, its classes, the sets F6/F7, L* and the row-16 data are computed from that S by the preprocessing PRE (the programs `gscan.c`, `grp.c`, `lscan.c`, `stats.c` of Appendix G, run under an address-space cap of 2^29 bytes), and q3 is measured for this family with the exact end event (Section 7.4, Appendix F).
The price is 0.3060 bit: the published family has 222 classes with cube sharing and 32 elements of L*, this one 1,067 classes without cube sharing and 44 elements of L* (more good pairs per first block, more work per good pair), and q3 is 2^-70.34 against 2^-70.16.

## 0. Summary

- **Algorithm (Sections 4-8).** Messages M0 || M1 and M0 || M1' (128 bytes; padding adds the same third block). A first block M0 is two fresh uniform 256-bit words; CV1 = F_37(IV, M0) costs one unit.
  (1) One bit-sliced F7 test of c7 - x over the 1,067 classes (x = A_{-1}; five batches of 256 lanes) finds the passing classes (16.93 per first block on average). (2) For each passing class, in batches of 256 reps (the class is `base | s` for s in a list with 21 variable bits), the planes of
  W6x = CB3 + (s & q) - H are formed (Lemma 8.1) and the F6 test gives the plane of good reps. (3) The good pairs (4647.70 per first block on average) are read from packed entry words in groups of four and the row-16 address
  u = W0 + s0(W1) of the group is computed. (4) Two table reads per lane give the l in L* (44 elements) whose E16x = u + C_l satisfies eight fixed-bit conditions; each of the (on average 0.172 per lane) survivors gets an exact straight-line test (34 operations).
  (5) A row-16 pass is checked through row 36: the cells and printed two-bit conditions of rows 16..21, then rows 22..36 of both members replayed on the raw schedule words, accepted iff the eight registers agree after row 36 (Section 7.4). Such a pair collides; it is verified with the target and output.
- **Cost (Sections 9, 11).** N_FB = 3,720,517,587,736,805 first blocks (2^51.72442); per first block 1 unit, 2,223 counted fixed operations and on average 400160.05 counted data-dependent operations (153.19 units in all), capped by V_MAX.
  T = A_C + A_S + DEV + N_FB + (N_FB x 2223 + V_MAX + vmax_fb + PRE + FIN) / C + 6 = N / C with N = 1,507,285,642,753,610,495,235, 2^58.983936 target compressions, claimed 58.98394. The characteristic, S and the family are constructed by charged procedures: A_C = 91,298,997,556 units (32,381.45 solver CPU-seconds, 2^36.41), A_S = 12,339,615,049 units (4,376.55 CPU-seconds, 2^33.52), PRE = 90 CPU-seconds (Section 11.2, 14.2, Appendices G, L).
- **Probability (Section 7, H2).** q3 = at least 2^-70.34, the probability of the exact end event (rows 22..36 replayed, registers equal; Section 7.4), the lower of two preregistered sets of 64 seeds of a sequential Monte-Carlo estimator written for this family (Appendix F). No hedge is needed: every variant of every passing class is examined.
- **Memory (Section 14).** Online tables 12,676,416 bytes = 2^23.60 (Section 14.1); the construction phases are measured and run under an address-space cap of 2^29 bytes (largest peak 500,424,704 bytes, the STP dump); claimed 2^33 bytes, the declared bound over all phases and development runs (H6, Appendix H.2).
- **Premises (Section 12).** H1 uniform independent chaining values; H2 q3; H3 few further successes per first block; H4 the advice charges (measured CPU-seconds of A_C, A_S and PRE at the calibrated price, DEV = 2^42); H5 counted word-RAM pricing of the bit-sliced program, 64 registers; H6 the memory bound 2^33 over all phases and development runs; H7 exact success floor. Nothing else is heuristic (Appendix H.1).
  No table statistics are used: every count in the ledger is an exact expectation or a stated bound on one.
- **Checks (Section 13).** `lowm.py selftest` and `lowm.py family` (the 1,067 classes recomputed from their c7 values against the definitions: 4,378,186 variants; the plane programs against the scalar definitions on 198,624 lanes; the class test on 213,400 lanes; the row-16 stage against the row-16 definition; the packed address on 400 lanes);
  the organizer experiments, all 256 trials of each; 300 trials of the counted online program against every definition (0 mismatches) and 80 of 80 planted semi-free-start collisions found by it; a calibration of the counted operation count on 28,500 first blocks against the ledger.

## 1. Target, cost model and output

- **Target** sha256-r37-prefix-v1: SHA-256 steps 0..36 on every padded block, the standard IV once, FIPS 180-4 padding, feed-forward, all eight digest words (repository `verifier/hash_functions.digest(m, "sha256", 37)`).
  The output is two distinct complete messages with equal digests, verified with the target before output.
- **Cost model** collision-frontier-v5: one 37-step target compression = 1 unit; every other executed 256-bit word-RAM primitive (load, store, add/sub, and/or/xor/not, shift/rotation, compare, branch,
  uniform random word) = 1/C unit with C = 2644. Immediates and shift amounts are instruction fields; 64 registers. Success must be at least 0.39 over fresh coins.
  The model text on construction: "A stored precomputed collision is not a cheap construction. All construction/preprocessing and advice must be accounted for, including any search omitted from the submitted program."
- **Notation.** In step i, E_i = A_{i-4} + E_{i-4} + S1(E_{i-1}) + CH(E_{i-1}, E_{i-2}, E_{i-3}) + K_i + W_i and A_i = E_i - A_{i-4} + S0(A_{i-1}) + MAJ(A_{i-1}, A_{i-2}, A_{i-3}) (mod 2^32);
  (A_{-1..-4}, E_{-1..-4}) = (a, b, c, d, e, f, g, h) of the incoming chaining value. F_R(cv, B) is the R-step compression with feed-forward; its output is cv + (A_{R-1}, A_{R-2}, A_{R-3}, A_{R-4}, E_{R-1}, E_{R-2}, E_{R-3}, E_{R-4}).

## 2. Sources and credit

- [LZLLQZ26] Y. Li, Z. Zhang, M. Li, F. Liu, H. Qian, J. Zhu, "Pushing Collision Attacks on SHA-2 to 39 Steps", IACR ePrint 2026/1120 (CC BY): the three-step attack, the window of the disturbance (Section 4.1 of the paper), and, as the guide for rows 16..24 that this filing uses as advice, the late cells of Table 15 and the two-bit conditions of Table 16.
  [LLWS26] Y. Li, F. Liu, G. Wang, J. Shi, ePrint 2026/1080 (the framework and the dense SAT model, FunctionModel).
- 68f33bc4-70ac-44fc-9aa9-8cb52aaec043 (our R37OWN; the ruling on it is answered in Appendix M), 1369d3d0 and d0789558 (our R37ZF6, R37ZF5): the program, the ledger structure, the premises, the memory accounting and the measured A_C run (Appendix L).
- ffbe30bb-ac92-4191-a589-3bf32661ee7d (Jbenisek, 60.38707, a credited derivative of fb039a6e): the four feasible value patterns of E18[1,5,10,11,18,28,29] and E19[29] and the change of the cell strings, the solver enumeration and the three verified collisions behind them (Section 7.6).
- Filings on this track, declared as dependencies: 6c77089c (winglock): transcription of Tables 15-17, the exact sets F6, F7 and L*, the SMC design for q3. dd6656d4 (Th0rgal): affine decomposition of F6, F7. 1c368173 (itseasypop), b947b377 (qkniep): the A0 freedom of the Step-1 solution and the c7 classes.
  087a18c4 (GordoAR): the exact-rational ledger and the success analysis. 1f12a09a (0xshikhar): the class selection by size and the packed groups of four 64-bit lanes. 7319bba9 (winglock): the program structure, the row-16 enumeration, the preregistered q3 studies, the end-to-end rates.
  d3ec5c41, 44921815, 8de337d5 (companygardener): the counted-program framework and the ledger. 8aeaed1c (ours) and c22f86a2 (Jbenisek): the direct row-16 lane read and the cap slack squared in the Chebyshev bound.
  f2fe1d4d, 0db0eeb6 (Th0rgal): the MAJ identity, the single packed member word `Gw` and its 31-operation group. fb039a6e (0xshikhar): the bit-sliced additions with register-resident planes. 6eeefb64 (sha256-r32): the calibrated price of a solver CPU-second (Sections 11.2, 13.4).
- **New here.** The attack runs on the output of its own charged procedures: the seed-4 characteristic of A_C, S and the pair of A_S, and a family, classes, lists, L*, F6/F7 counts and row-16 data computed from that S by the programs of Appendix G (Sections 3-6, 11.2, 14.2); the derivation of every class of the family from its c7 value alone (Lemma 5.3, `fibre` in `lowm.py`); the class test and W6 test without cube sharing for lists with 21 variable bits (Sections 5.3, 8, 9); q3 measured for this family and the exact end event in one preregistered estimator (Section 7.4, Appendix F); the ledger for 1,067 classes and 44 elements of L* (Sections 9-11, Appendix B).

## 3. The characteristic (rows 6..15 constructed by A_C; rows 16..24 advice; checked by `experiments/lowm.py`)

### 3.1 Notation and orientation

Symbols are MSB first: `n` = bits (x, y) = (0, 1), `u` = (1, 0), `0`/`1` fixed and equal, `=` equal, `+` = equal on
both members and equal to the same bit of the vertically adjacent `+` (E_i[b] = E_{i+1}[b]). Member x is the
first message M of the pair of Section 3.4; y is the second, M'.

### 3.2 What the attack uses of the characteristic, and where each part comes from

The attack uses (a) the **signed cells** (`n`, `u`, `=`) of rows 6..15 of A, E and W, (b) the modular differences that follow from them (d6, d7, d8, t6, t7, t8 of Section 5.1), (c) the **cells and printed two-bit conditions of rows 16..21** (and the `+` link of E15 and E16, the conditions that close at rows 15..21) and (d) the exact end event of rows 22..36, which uses no cell.
(a) and (b) are the output of the charged search **A_C** (Section 11.2, Appendix L): kissat 4.0.4 seed 4 on the CNF of the 37-step dense model (`gen37.py ... --fix 16-24 --fixw 22,24 --W 25 --O2 7 --O3 25 --E 63`), its model decoded by `decode_model.py`; the file is `seed4.full.chi` (sha256 235556a2...b2b9). The value cells (`0`, `1`, `+`) and the two-bit conditions of rows <= 14 of Table 15 are **not used**: the dense model is a signed-difference model and its output has none.
The signed path was not assumed realizable by a pair; **A_S** (Section 11.2) is the solve that shows it: the SAT instance of the pair (signed cells, the message XOR masks of the window) returned a model, which is S and the pair of Section 3.4.
(c) are the cells of Tables 15 and 16 of the paper (advice, Section 3.5). (d) needs none.

The rows used (the program's strings: rows 6..15 are the signed cells of `seed4.full.chi` together with the `+` link of E15; rows 16..22, 24 are the cells of Table 15 as the program uses them, with the value bits of rows 18 and 19 and the cells E16[23], E16[24]/E17[24] relaxed as in Sections 7.4c and 7.6; rows 22 and 24 are those of the paper and are read by `row_ok` for the checks of Section 13 only):

```text
  i  A_i                               E_i                               W_i
  6  =nu=============================  nuu=============================  ==n=============================
  7  ==========n====n====n======n====  ==n=u=====n==n=====nu===unuu====  =====u===u==========n===========
  8  ================================  =====n===n==u========u=u=====u==  ==u=============================
  9  ================================  ===========================u====  =====u=u=======n===n==u=u=n=u=n=
 10  ======u===========u=============  ==n===u===========u=============  ============n======u=u==========
 11  ====u=====u=========u=n====u==n=  ===un==========n=n=u=uu======u=u  ================================
 12  =nu=============================  =====uuuuunu=========n=u=u=uu=n=  ================================
 13  ====u=========u=u=======n==u====  ====n======unn==n===============  ================================
 14  ======u=n=======n===============  ====================n===u=======  =====u===n==========u===========
 15  ================================  =u=======n====n====u==u====+====  ==u=============================
 16  ==u=============================  =0=====+=0===11=+==01=0=0==+====  ================================
 17  ================================  =0======01===u1=+==0==1===1u====  ================================
 18  ================================  =======uu=======n=====1====1====  ================================
 19  ================================  =======00====1==0==========1====  ================================
 20  ================================  ==u====10=======1===00==========  ================================
 21  ================================  ==0=============================  ================================
 22  ================================  ==1=============================  =====0=nn=====1=u=1=============
 24  ================================  ================================  ==n=============================
```

It differs from the published characteristic in four cells of rows 6..15, all of seed 4: E6[31] (`n` instead of `u`, the same modular value), two signs of W9 and one sign of W10; the modular differences of W6, W7, W8, W14, W15, W22, W24 and the XOR masks of the message words (W6 20000000, W7 04400800, W8 20000000, W9 050112aa, W10 00081400, W14 04400800, W15 20000000) are the published ones (`r37own/PLAN.md`, MEASURED by comparing `seed4.full.chi` with the published signed cells). Rows -4..3 are entirely `=`: **A0..A3 and E0..E3 carry no condition**, and rows 4 and 5 carry no signed cell.

### 3.3 Two-bit conditions

```text
A15[15] != A16[15], A15[23] = A16[23], A15[25] = A16[25], A16[9] != A16[20], A16[18] != A16[6]
A16[8] = A16[17], A15[29] = A17[29] (printed: A16[29] = A17[29]), A17[29] = A18[29], E15[4] = E16[4]
E17[0] != E17[13], E16[15] = E17[15], E18[6] != E18[19], E18[2] = E18[20], E20[2] != E20[16]
```

These are the conditions of Table 16 that close at rows 15..21, as read by the program (`X2` of `lowm.py` restricted to rows >= 15; E16[24] = E17[24] is dropped by R16x, Section 7.4c). The program checks every cell of rows -4..21 and, on rows >= 15, these conditions (they can only lower the success probability, and q3 is defined with them). The two-bit conditions of rows <= 14 and those on W22 and W24 are not used: the value cells they belong to are replaced by the signed path of A_C (rows <= 14) and by the exact end event (rows 22..36). The W6, W7 and W8 conditions are replaced by the exact filters of Section 5.1 and by the definition of G (Section 4.3).

### 3.4 The semi-free-start pair (output of A_S)

```text
CV  177b3054 86566196 6e70d910 63ccf669 8de0c06c 4e5afdb9 2589bbf6 7befabae
M   47148b8b 88e4d419 5c615dc9 71c227ff ab7a34f8 3160fa12 100b1577 56fe27fb
    a3d6f43d af36ae8c 0826d41f a3ad8526 df919938 82243979 849eef4a 3cc48222
M'  47148b8b 88e4d419 5c615dc9 71c227ff ab7a34f8 3160fa12 300b1577 52be2ffb
    83d6f43d aa37bc26 082ec01f a3ad8526 df919938 82243979 80dee74a 1cc48222
hash 35fdf833 b274e9e7 1e71a37d 3757fb3f b8a61086 8a724ec4 e7086f24 1671244b
```

F_37(CV, M) = F_37(CV, M') = the printed hash; every signed cell of rows -4..36 of A, E and W holds with x = M, y = M' (`s4_check.py`: the signed difference of A, E (rows -4..36) and W (rows 0..36), every bit, `=` cells included, equals the cells of `seed4.full.chi` with the published rows 16..24: 0 mismatches; `experiments/lowm.py` rebuilds both members from S and checks the cells of rows -4..21). This pair is not the paper's: it is the model of the instance of Section 11.2.

### 3.5 Advice

The cells of rows 16..21 (and the rows 22 and 24 cells that the search A_C holds fixed) are the published input of this filing: they are used as written in Tables 15 and 16 of [LZLLQZ26], they are not constructed by any procedure of this filing, and they are declared as nonuniform advice: the text above is below 2^13 bytes (claim `nonuniform_advice_log2_bytes` = 13), and it is part of the online tables and constants of Section 14.1 (`characteristic_and_Lstar`, 40,960 bytes). The attack's success does not depend on their being right in the sense of an output: every output is verified with the target (Section 1). The cells act as the guide that fixes which second-block pairs are examined (the probability q3 of Section 7 is the probability of the exact event for pairs that follow them).

## 4. Step 1: the solution S (output of A_S) and its A0-variants

### 4.1 S

S is the inner part of the pair of Section 3.4: A0..A13, E4..E13 and W8..W13 of both members (x | y):

```text
A0  f3d0048f | f3d0048f   A1  8f5a9ca1 | 8f5a9ca1   A2  6effba9c | 6effba9c   A3  3604bd1f | 3604bd1f   A4  f8ba7da3 | f8ba7da3
A5  60a20367 | 60a20367   A6  b7ce995c | d7ce995c   A7  325a9601 | 327b9e11   A8  3b8428e4 | 3b8428e4   A9  07cc18ce | 07cc18ce
A10 7b8a3ab1 | 798a1ab1   A11 dd2b5955 | d50b5347   A12 a45d0bc4 | c45d0bc4   A13 5f4ed318 | 574c5388   E4  869ee1db | 869ee1db
E5  76760d10 | 76760d10   E6  6b0dfe86 | 8b0dfe86   E7  9a41cebd | b265d64d   E8  6aacdfa5 | 6ee4daa1   E9  db3c3cfb | db3c3ceb
E10 87acbafd | a5ac9afd   E11 30761f5f | 2877495a   E12 6fd5b358 | 6825b602   E13 66f25d89 | 6eeedd89   W8  a3d6f43d | 83d6f43d
W9  af36ae8c | aa37bc26   W10 0826d41f | 082ec01f   W11 a3ad8526 | a3ad8526   W12 df919938 | df919938   W13 82243979 | 82243979
```

### 4.2 The Step-2 equations (Lemma 4.1, triangular bijection)

For fixed state rows A0..A13 (both members) and a chaining value CV1 = (A_{-1..-4}, E_{-1..-4}), define for each member

```text
E_i = A_i + A_{i-4} - S0(A_{i-1}) - MAJ(A_{i-1}, A_{i-2}, A_{i-3})                        (i = 0..13)
W_i = E_i - A_{i-4} - E_{i-4} - S1(E_{i-1}) - CH(E_{i-1}, E_{i-2}, E_{i-3}) - K_i            (i = 0..13)
```

**Lemma 4.1.** With these words, F_37's steps 0..13 from CV1 reproduce the state rows A0..A13 (and the E_i)
exactly, and for fixed A0..A13 the map CV1 -> (W0, ..., W7) is a bijection of (2^32)^8: W7 depends only on
A_{-1}, W6 is -A_{-2} plus a function of A_{-1}, ..., W0 is -E_{-4} plus a function of the earlier coordinates
(each step inverted for its new coordinate). W8..W13 do not depend on CV1. *Proof.* Substitution; `lowm.py`
(`words_from_cv`, `invert_cv`, `sfs_trial`) checks the reproduction and the inverse on every constructed pair.

### 4.3 The A0-variants (itseasypop 1c368173, qkniep b947b377; re-derived here for this S)

**Lemma 4.2 (variants).** Replace A0 of S by any a0 (both members: rows 0..5 of S carry no difference) and keep
A1..A13 of both members. Then, for every chaining value:
(a) E5..E13 and W9..W13 are unchanged (E_i for i >= 5 involves A_{i-4..i} with i-4 >= 1; W_i for i >= 9 involves
    E_{i-4..i}, A_{i-4} with i-4 >= 5);
(b) E4 = a0 + C4 with C4 = A4 - S0(A3) - MAJ(A3, A2, A1) = 92cedd4c, and W8x = W8C - E4 with
    W8C = E8 - A4 - S1(E7) - CH(E7, E6, E5) - K8 = 2a75d618; E4 enters W8 of both members with the same sign
    (as E_{i-4} of step 8, without a member difference), so the modular difference W8y - W8x = e0000000 is
    unchanged;
(c) W0..W7 change (they absorb E0..E4); the member differences W_i^y - W_i^x are 0 for i <= 5, d6 = 20000000 for
    i = 6 (E5, E4, E3 carry no difference) and d7 = fbc00800 for i = 7 **provided E4[31:29] = 100**: in step 7,
    CH(E6, E5, E4) selects E5 for the bits where E6 is 1 and E4 where E6 is 0; E6x = 6b0dfe86 and E6y = 8b0dfe86 differ in bits 31..29 (`011` against `100`; XOR e0000000), E5 = 76760d10 has `011` there, so d7 depends on E4[31:29] only and, over the eight values of E4[31:29], equals fbc00800 for exactly one, `100` (`s4_derive.py`, exhaustive; the published S needs `000`);
(d) the signed cells of rows -4..15 that involve W8: W8's cell (`u` at bit 29) and the signed XOR difference of s0(W8) that the cells of W23 need, i.e. the modular difference s0(W8y) - s0(W8x) = t8 = 043ff800 = -d7 that makes W23 = s1(W21) + W16 + s0(W8) + W7 difference-free.

Define **G = {a0 : E4 = a0 + C4 has E4[31:29] = 100, w = W8x = W8C - E4 has w[29] = 1 and s0(w + d8) - s0(w) = t8}**, d8 = e0000000, t8 = 043ff800. The last two conditions are equivalent to the printed cell and the three printed two-bit conditions of W8 (W8[29] = 1 as the cell `u`, W8[1] != W8[12], W8[8] != W8[25], W8[14] = W8[18]): over all 2^32 words w, `w[29] = 1 and s0(w + d8) - s0(w) = t8` and the four printed conditions hold for exactly the same 2^28 words (`f8.c` of Appendix G, exhaustive, 0 differences). Exhaustive count over the 2^29 values of E4 with E4[31:29] = 100 (a0 = E4 - C4 is a bijection; `gscan.c`, Appendix G): **|G| = 21,935,501 = 2^24.39**. The A0 of S (f3d0048f) is in G.

**Lemma 4.3 (validity).** For a0 in G, every chaining value CV1 whose words (Lemma 4.1 with A0 = a0) satisfy the
filters W7x in F7 and W6x in F6 (Section 5.1), and every l in L* (Section 6), the pair follows every signed cell of rows
-4..15 of A, E and W except the XOR cells of W6 and W7, and every modular difference that enters the message expansion (W6..W15 and
s0(W6..W15), s1(W14), s1(W15)) equals that of the pair of Section 3.4. *Proof.* Lemma 4.2 for E4, W8 and d6, d7; the
filters for s0(W6), s0(W7) (Section 5.1); everything else is S's or l's. *Checks:* every good pair of the
organizer experiment `a0-online-r37` and of the end-to-end runs (Section 13) against all 44 l.

So a variant changes A0, E0..E4 and W0..W8 only. W8 is the only changed word that enters the expansion beyond W8
itself (W23 via s0(W8), W24 directly); Section 7 shows this is all that can change q3.


## 5. Step 2 with variants

### 5.1 The exact filters

The characteristic fixes the modular differences of W21, W22, W23; with S (or any variant) fixed, the only remaining
requirements on W6, W7 (6c77089c, Lemma 3) are W6x in F6 and W7x in F7, where F_k = {w : s0(w + d_k) - s0(w) = t_k
mod 2^32}, d6 = 20000000, t6 = 03c00800, d7 = fbc00800, t7 = 017f8000. |F7| = 68,157,440 and |F6| = 287,309,824
(exhaustive over all 2^32 words by 0db0eeb6, Tungsten; the counts of 7319bba's `f6chk.c` agree). By the carry pattern of w + d (s0 is linear), each set is a disjoint union of
affine spaces. We use them in the following bitwise form, **checked against the definition on all 2^32 words**
(0db0eeb6, Tungsten: about 10 CPU-minutes, zero mismatches for both; here `selftest` and the organizer experiments compare the plane programs with the definitions):

```text
F6: w is NOT in F6  iff  common | (w29 & (bc | (w30 & X)))  with
      common = (w14^w18) | ~(w8^w25) | (w1^w12),   bc = (w15^w19) | ~(w9^w26) | (w2^w13),
      X = (w16^w20^w31) | ~(w10^w27^w31) | (w3^w14^w31)                                  (bits are w_i; | is OR)
F7: w is in F7  iff  w1 = w18, w0 = w28, w9 = w30 and
      [ w11 = 0, w22 = 1, w26 = 1 ]                                                       2^26 words
      or [ w11 = 1, w12 = 0, w22 = 0, w23 = 1, w26 = 0, w27 = 1, w2 = w19, w1 = w29, w10 = w31 ]   2^20 words
```

(F6 is the form published in 087a18c4/1c368173 with b_bad & c_bad simplified to bc | (w30 & X); 7319bba derived the F7 constraint
set from the affine hull of F7 and of its two halves (7319bba); here it is verified
exhaustively against the definition.)

For a variant a0 and CV1 the filter words are (member x, from Lemma 4.1):

```text
W7x = c7(a0) - A_{-1},           c7(a0) = 6534c91b + MAJ(A2, A1, a0) - CH(E6, E5, a0 + C4)
W6x = C6 - A_{-2} + MAJ(A1, a0, A_{-1}) - CH(E5, a0 + C4, E3),   E3 = K3C - MAJ(A2, A1, a0) + A_{-1}
C6 = E6 - 2 A2 + S0(A1) - S1(E5) - K6 = 0ea5c39d,   K3C = A3 - S0(A2) = 044dd43e,   6534c91b = E7 - A3 - S1(E6) - K7 - K3C
```

(A1 = 8f5a9ca1, A2 = 6effba9c, A3 = 3604bd1f, E5 = 76760d10, E6 = 6b0dfe86, E7 = 9a41cebd, C4 = 92cedd4c for this S.) The exact counts |F6| = 287,309,824 and |F7| = 68,157,440 do not depend on S (they depend on d6, t6, d7, t7, which are the published ones for this characteristic, Section 3.2); `stats.c` (Appendix G) recounts both over all 2^32 words (output in Appendix A).

### 5.2 Lemma 5.1 (distribution, per variant)

Under H1 (CV1 uniform), for every fixed variant a0: Pr[W7x in F7] = p7 = |F7|/2^32 = 2^-5.97763 and
Pr[W6x in F6 | W7x in F7] = p6 = |F6|/2^32 = 2^-3.90197 exactly; conditioned on both, (W0..W5) is uniform on
(2^32)^6, (W6, W7) is uniform on F6 x F7, and they are independent. For every l in L*, (W16, ..., W21) is then a
bijective image of (W0..W5) for fixed (W6, W9..W15), hence iid uniform and independent of (W6, W7).
*Proof.* Lemma 4.1 (bijection for fixed a0) and the inverse expansion W5 = W21 - s1(W19) - W14 - s0(W6),
W4 = W20 - s1(W18) - W13 - s0(W5), ..., W0 = W16 - s1(W14) - W9 - s0(W1). (6c77089c's Lemma 2, for each variant.)

### 5.3 The 1,067 classes, their lists, and Lemma 5.3 (a class from its c7)

c7(a0) takes 16,980 distinct values on G (`grp.c`, Appendix G). A *class* is G intersected with one value of c7; for all variants of a class and a given CV1, W7x is the same word, so one membership test decides the W7 filter of the whole class.
**This filing examines the 1,067 classes with at least 3456 variants** (4,378,186 variants, 19.96% of G; the size threshold is the one of the 222 classes of 1f12a09a's selection; the ledger moves by under 0.02 bit for thresholds between 3,000 and 5,000, `r37own/STAGE2.md` Section 4). The classes are written by `grp.c` in the preprocessing (Section 14.2): class c7 value, size and members. The sizes (size x number of classes):

```text
3456 x 73  3472 x 14  3516 x 10  3520 x 2  3548 x 9  3552 x 2
3584 x 192  3600 x 9  3760 x 4  3790 x 4  3808 x 3  3840 x 140
3900 x 4  3936 x 132  3940 x 4  3968 x 64  4000 x 4  4016 x 64
4032 x 49  4080 x 2  4180 x 2  4216 x 1  4266 x 1  4288 x 4
4320 x 18  4400 x 4  4416 x 2  4424 x 18  4464 x 9  4480 x 14
4512 x 4  4516 x 9  4548 x 4  4608 x 36  4728 x 12  4800 x 20
4920 x 8  4960 x 4  5020 x 4  5376 x 36  5760 x 24  5904 x 24
5952 x 12  6024 x 12
```

**Fact (computed; `lowm.py family` re-derives it for every class).** For all 1,067 classes base & mask = 0, where base is the AND and mask the OR minus the AND of the members, so a0 = base + s = base | s = base ^ s with s a subset of the mask, and the set of s depends only on one of **262 lists** (classes with equal mask and equal set of s share one list). The masks have 14 to 21 bits; the union of the masks is 1fbad9bb (21 bits: 0, 1, 3, 4, 5, 7, 8, 11, 12, 14, 15, 17, 19, 20, 21, 23..28) and the bits 0, 1, 3, 4, 5, 7, 11, 12, 15, 19, 21, 23, 27, 28 (18a898bb) are in every mask. A list is stored as the planes of its reps (the 21 bits of the union; the bits outside the mask of a class are static) and as packed entries (Section 9.6).
**There is no cube.** In the published family the free bits 0, 2, 3 of the lists let one W6 test decide up to eight reps (Lemma 8.2 there). Here the lists have free bits (3, 7, 15, 19, 21, 23 in various lists) but flipping any of them changes W6x (a test with 300 random x per bit, `r37own/STAGE2.md` Section 2), so every rep is tested once, and the ledger charges it.
S0(a0) is at most 0xffffff05 over the 4,378,186 variants (`family`), so ~S0(a0) & M32 >= 0xfa and no carry leaves a 64-bit lane of the packed words of Section 9 (the program asserts the lane bound at every group).

**Lemma 5.3 (a class from its c7).** For a value c, the set {a0 : c7(a0) = c} is computed by the recursion `fibre(c)` of `lowm.py`, and the class of c is {a0 in that set : a0 in G}. *Proof.* With ZC = 6534c91b, c7(a0) = ZC + MAJ(A2, A1, a0) - CH(E6, E5, e4) and e4 = a0 + C4. Write m_i = MAJ(A2, A1, a0)_i (it is A2_i where A1_i = A2_i and a0_i elsewhere) and v_i = CH(E6, E5, e4)_i (E5_i where E6_i = 1 and e4_i elsewhere). Bit i of m - v - (borrow from the lower bits) depends on a0_i, on the carry of a0 + C4 into bit i (for e4_i) and on the borrow into bit i; the recursion over i = 0..31 carries these two bits as its state, tries a0_i = 0 and 1, and keeps a branch iff bit i of the difference equals bit i of c - ZC. Its leaves are exactly the solutions of c7(a0) = c. QED.
So a class needs only its c7 value, S and the definition of G: the program derives the members, base, mask and list of each class it uses from c7 (`klass` of `lowm.py`: 0.11 to 0.17 s per class in Python, 43,008 to 57,344 leaves, of which 3,456 to 6,024 are in G); `family` recomputes all 1,067 classes this way and compares the sizes, the histogram above and the union and intersection of the masks with the output of `grp.c` (4,378,186 variants, 0 differences; Section 13.2).

Per first block over uniform x, every class passes the W7 test for exactly |F7| = 68,157,440 values of x, so the number of passing classes has mean 1,067 p7 = 16.93 and the number of variants in passing classes has mean 4,378,186 p7 = 69,478.
Passing classes are strongly correlated (their c7 values are close), so the counts are bursty; only expectations are used.


## 6. Step 3

### 6.1 L* (computed by `lscan.c` from the pair of Section 3.4)

L is the set of (W14, W15) for which rows 14, 15 of both members follow the signed cells (with the `+` pair of E15) and the four expansion differences depending only on (W14, W15) equal those of the pair of Section 3.4; `lscan.c` scans all 2^32 values of W14 and of W15 and forms the product: **|L| = 1,048,576** (the signed path has no value cells, so L is larger than the 4,096 of the published cells). L* keeps the elements
whose row-16 modular differences equal the characteristic's (dE16 = 0, dA16 = e0000000): **|L*| = 44** (66.66 CPU-seconds, 132,988 KB; Appendix G), all with W14x = 849eef4a and W15x in

```text
 0:2c64be0c   1:2c64be0d   2:2c64be2c   3:2c64be2d   4:2d64be0c   5:2d64be0d   6:2d64be2c   7:2d64be2d
 8:3c64820b   9:3c64820e  10:3c64820f  11:3c64822b  12:3c64822e  13:3c64822f  14:3c649e0c  15:3c649e0d
16:3c649e2c  17:3c649e2d  18:3c64a20b  19:3c64a20e  20:3c64a20f  21:3c64a22b  22:3c64a22e  23:3c64a22f
24:3cc48222  25:3cc4a222  26:3d64820b  27:3d64820e  28:3d64820f  29:3d64822b  30:3d64822e  31:3d64822f
32:3d649e0c  33:3d649e0d  34:3d649e2c  35:3d649e2d  36:3d64a20b  37:3d64a20e  38:3d64a20f  39:3d64a22b
40:3d64a22e  41:3d64a22f  42:3dc48222  43:3dc4a222
```

(y side: W14y = W14x ^ 04400800, W15y = W15x ^ 20000000; the pair of Section 3.4 has W15x = 3cc48222.) Rows 12..15 of both members
depend only on S and l, not on CV1 or the variant.

### 6.2 Row 16 without a mask table

For l in L*, E16x = C_l + u with u = W0 + s0(W1) (W16 = s1(W14) + W9 + s0(W1) + W0; C_l collects rows 12..15 of l, K16, s1(W14) and W9). The cell E16[23] = 0 of Table 15 is not imposed (R16x, Section 7.4c), so every one of the 44 elements of L* has row-16 values: **exactly 65,536 values of E16x for 41 of them, 69,632 for l = 25 and l = 42 and 67,584 for l = 29: 2,893,824 pairs (u, l)** (`stats.c`, exhaustive over the 2^24 values of E16x with the eight fixed bits for each l, Appendix G and A; the estimator `smc_s4.c`, which uses the generic cell machinery and not the test below, enumerates the same 2,893,824 pairs with the same per-l counts, Appendix F). By Lemma 5.1 u is uniform for a good pair, so Pr[row 16 holds for l] = (number for l) / 2^32 exactly and the expected number of row-16 hits per probed lane is 2,893,824 / 2^32 = 2^-10.54.

**Lemma 6.2 (the exact test).** For each of the 44 l let A16x = E16x + cxA_l with cxA_l = -A12x + S0(A15x) + MAJ(A15x, A14x, A13x) (rows 12..15 of member x for l). Then E16y = E16x and A16y = A16x - 2^29 (mod 2^32), computed for all 44 l.
Row 16 holds for (u, l) iff all of the following hold (cells of row 16 and the two-bit conditions closing at row 16):

```text
E16x & 40461a80 = 00060800         the eight fixed bits 30, 22, 18, 17, 12, 11, 9, 7 of the E cell (E16 has no difference: E16y = E16x; bit 23 is free under R16x)
E16x[4] = E15x[4]                  the '+' pair of the E cells of rows 15 and 16 (E15[4] = E16[4])
A16x[29] = 1                       the A cell 'u' at bit 29: with A16y = A16x - 2^29 the XOR difference is 2^29 iff A16x[29] = 1
A16x[15] != A15x[15], A16x[23] = A15x[23], A16x[25] = A15x[25]          (A15x of l is a constant)
A16x[9] != A16x[20], A16x[18] != A16x[6], A16x[8] = A16x[17]
```

*Proof.* The cells of row 16 are the A cell (u at bit 29), the E cell (eight fixed bits, no difference), the W cell (none); the printed conditions closing at row 16 are the seven of Section 3.3 (A15/A16 three, A16 three, E15/E16 one);
for all 44 l the difference of E16 is zero and cyA_l - cxA_l = e0000000 (the defining property of L*), which is the statement on A16y. *Checks:* the program counts the pairs the test accepts by the loop over all 2^24 values of E16x for each l (`stats.c`, 2,893,824) and the independent estimator's enumeration gives the same per-l counts;
the experiments and `selftest` compare the test with the generic row check (`row16_ok`) on random and near-miss values (members seen and missed: 0). QED.

**The table stage.** A necessary condition on all 44 l at once, from two tables of 4096 words (one 256-bit word each, two 44-bit masks in the 64-bit lanes 0 and 1): for the chunk lo = u mod 2^12 and mid = (u >> 12) mod 2^12,
LO[lo] = (pm, pm & cm) with pm the l for which E16x = u + C_l satisfies E16x[4] = E15x[4] and the fixed bits 7, 9, 11, and cm the l for which lo + (C_l mod 2^12) carries into bit 12;
MID[mid] = (P0, P0 ^ P1) with P_c the l for which E16x satisfies the fixed bits 12, 17, 18, 22 when the carry into bit 12 is c. The mask of the l that can still pass is

    filt(u) = pm & (P0 ^ ((P0 ^ P1) & cm)) = lane 0 xor lane 1 of T,   T = LO[lo] & MID[mid] (a single AND of two words),

a superset of {l : row 16 holds for (u, l)} (it uses seven of the eight fixed bits and E16x[4] = E15x[4]: eight conditions on the bits 4, 7, 9, 11, 12, 17, 18, 22; bit 30 and the A conditions are left to the exact test). For uniform u,
E16x = u + C_l is uniform, so each l is in filt(u) with probability exactly 2^-8 and E|filt(u)| = 44/256 = 0.171875; counted over all 2^24 values of u mod 2^24 (`stats.c`), the sum of |filt| is 2,883,584 = 44 x 2^16 and filt(u) != 0 for exactly 2,517,128 of them, so Pr[filt(u) != 0] = 2,517,128 / 2^24 = 0.15003 exactly. The tables are built in the preprocessing from the cells; `selftest` and the organizer experiments check filt(u) against the generic row check on random and near-miss values (members seen and missed: 0).


## 7. The Step-3 probability for the variants (H2)

### 7.1 The quantity

For a good pair (CV1, a0) and l in L*, let F_l be the event that rows 16..36 are followed as described below. q3 = average over the 4,378,186 variants of the 1,067 classes and over l in L* (44 elements) of
Pr[F_l | good], the probability over CV1 (Lemma 5.1 gives the exact joint law of all second-block words). The
expected number of successful (variant, l) per first block is g x 44 x q3.

The event F_l of this filing: the cells of rows 16..21 (Section 3.2) and the printed two-bit conditions closing at rows 16..21 hold for both members, with the eight value bits of rows 18 and 19 of Table 15 not imposed and E16[23] = 0 and E16[24] = E17[24] not imposed (R16x; Sections 7.4c and 7.6), and rows 22..36 are replayed on the raw schedule words of both members (W6, W7, W8 as drawn; W_t for t >= 22 from the schedule recurrence on each member's own words) and the event is that the eight registers (A33..A36, E33..E36) of the two members agree after step 36. No cell or printed condition is imposed at rows 22..36 (the published cells of W22 and W24 belong to the published signs of W9 and W10, not to this characteristic: the cell event of rows 22..36 is not defined for the pair of Section 3.4, cellevent = 0 in all 144 seeds of Appendix F).

### 7.2 Lemma 7.1 (what a variant can change)

Rows 16..22 (all their cells and two-bit conditions) are functions of S's rows 12..15, l, and W16..W22, where
W16..W21 are functions of (W0..W6, W9..W15) and W22 = s1(W20) + W15 + s0(W7) + W6. By Lemma 5.1 the law of
(W16..W22) given goodness is the same for every variant (W8 does not occur). **Hence the probability that rows
16..21 pass is identical for all variants.** The variant enters rows 23..36 only through W8, which occurs in W23 = s1(W21) + W16 + s0(W8) + W7 and W24 = s1(W22) + W17 + s0(W9) + W8 (and
in later words through them). Its modular differences are fixed (Lemma 4.2 (d)), so only the *values* of W23, W24
move. The probability of the exact end event given a pass of rows 16..21 is therefore an average over (W6, W7, W8) of an indicator, and the estimator of Section 7.3 draws W8 uniformly from the family, as the program meets it.

### 7.3 The estimator

Stages: row 16 exact (the enumeration of 6.2: the stage mean is (1/44) sum_l |R16_l| / 2^32 = 2^-15.995, and the initial particles are drawn exactly from the passing (l, E16) pairs);
rows 17..21: each child proposes E_t^x uniformly with the row's fixed x-bits imposed (exact importance weight 2^-f), sets W_t^x = E_t^x - (the rest of step t), W_t^y = W_t^x + its exact
difference, and checks the whole row; then, for each particle that has passed rows 16..21, MT tail proposals (E21, W6, W7, W8): W6 drawn uniformly from F6 (rejection), W7 uniformly from F7 (its affine decomposition), W8 uniformly from the 4,378,186 variants, with the exact end event evaluated on each proposal. NP particles, M children per particle per stage, multinomial resampling of the survivors after
every stage; the product of the stage means (est21: rows 16..21) times the fraction of tail proposals that are exact collisions is an unbiased estimator of q3 (the standard SMC normalising-constant estimator). The design is 6c77089c's and 087a18c4's; the program of this filing is `smc_s4.c` (Appendix F), the estimator of 7319bba's design as re-implemented for 96933f8e and 1369d3d0 (`smc_r16x.c`) with the l-values, the pair, L* and the variant list of this S (Section 7.4).

### 7.4 The study of this filing (preregistered; our own estimator)

**Program and inputs.** `smc_s4.c` (sha256 f09f4bed...edc) with the constants header `lab_s4.h` (sha256 2af1febe...ff2), written by `mk_lab.py` from the pair of Section 3.4, the cells of `lowm.py` and L* (Appendices F and G); the family file is the output of `grp.c` (`s4_3456.cls`, sha256 dd44ff81...a064). Built with `gcc -O2 -DFFBE_RELAX -DR16X`: the four value patterns of rows 18 and 19 and R16x are one carrier (Sections 7.4c, 7.6). The same source, compiled against the constants of the published pair (`smc_pub`), reproduces the filed output of seed 9201 of the study of 1369d3d0 bit for bit (known-answer check of the changes).
**Preregistration** (`PREREG_s4.md`, sha256 51c64a83...81300, written before any listed run; reproduced in Appendix F). Per seed: NP = 8192, M = 512, MT = 8192 (2^26 tail proposals), Q = 2^log2est21 x exact/n. Two independent sets of 64 seeds, S1 (40001..40064) and S2 (50001..50064), on the family of 1,067 classes; a descriptive set S3 (60001..60016) on the 223 classes of at least 4,480 variants (not used). Rule fixed in advance: **declared q3 = 2^x, x = floor(100 log2 min(LB_S1, LB_S2)) / 100**, LB the one-sided 99% Student lower bound of the mean of the 64 linear estimates (t = 2.3870, 63 df); if the sets disagree by more than 2 standard errors of the difference, both are reported and the lower is declared. Every listed seed was run and is reported (Appendix F); none was dropped or rerun.

**Results** (log2 of the linear means; 144 seeds, 4 processes at a time in one cgroup, 18 minutes on the cloud machine):

| set | seeds | family | mean | relative sd | 99% lower bound | exact events | tail proposals |
|---|---|---|---:|---:|---:|---:|---:|
| S1 | 40001..40064 | 1,067 classes | 2^-70.2581 | 0.0914 | 2^-70.2979 | 286,975 | 2^32 |
| S2 | 50001..50064 | 1,067 classes | 2^-70.2885 | 0.1160 | 2^-70.3394 | 287,460 | 2^32 |
| S3 (descriptive) | 60001..60016 | 223 classes | 2^-70.2735 | 0.1160 | 2^-70.3867 | 71,495 | 2^30 |

The sets agree (z = 1.15, pooled mean 2^-70.2732). Rule applied: the lower bound of S2 is the lower, **q3 = 2^-70.34** (floor to two decimals of -70.3394), against 2^-70.16 for the published family. est21 is about 2^-56.37 and the exact fraction of the tail about 2^-13.88 per seed (published pair, seed 9201 of the earlier study: 2^-56.33 and 2^-13.68). The cell event of rows 22..36 is not defined for this characteristic (cellevent = 0 in all 144 seeds of about 10^10 proposals): the published cells of W22 and W24 belong to the published signs of W9 and W10, and the characteristic of Section 3.2 differs from the published one in those signs. The exact event is what the program accepts and what the claim uses.

**Constructive check** (`smc_hit.c`, `verify_hits.py`; the same build, seed 777). 40 hits of the estimator (each a different (a0, l, CV1) with a0 a variant of S that is not the model's own A0), reconstructed to CV1 and W0..W15 by the inverse expansion, are all genuine 37-step semi-free-start collisions on the real compression (40 of 40; the state rows 0..13 equal S with A0 = a0; every signed cell of rows -4..21 holds). Twenty of the 40 differ from the characteristic only in the signed XOR pattern of W22 (one also of W24): other sign patterns of the same modular differences, still collisions, which is why the exact event and not the cells of rows 22..36 is the event.

### 7.4c Rows 16 and 17: the R16x relaxation, and rows 18 and 19: the value patterns

Table 15 imposes E16[23] = 0 (a `0` in the E cell of row 16) and E16[24] = E17[24] (a `+` pair of the E cells of rows 16 and 17, printed again as a two-bit condition). Neither can be dropped alone: a pair that breaks only one of them dies at row 19.
Dropped together they can: at step 19, CH(E18, E17, E16) emits terms at bits 24 and 23 whenever E17 and E16 differ there, and the signed sum of row 19 absorbs them with a different sign solution of S1(E18). In `lowm.py`: the character of bit 23 of `CHE[16]` is `=` instead of `0`, the character of bit 24 of `CHE[17]` is `=` instead of `+`, and the two-bit condition (E, 16, 24, =, E, 17, 24) is not in `X2`:

```text
 row 16   Table 15 =0=====+00===11=+==01=0=0==+====     program =0=====+=0===11=+==01=0=0==+====
 row 17   Table 15 =0=====+01===u1=+==0==1===1u====     program =0======01===u1=+==0==1===1u====
```

The parity is not tested by the program: every pair that follows the remaining cells of rows 16..36 has zero output difference and is verified with the target before output. The estimator counts exactly the pairs that the program accepts. `row_ok` reads the masks and values of the cells as constants, so `ROWCHECK` and `ROWCOMP` are unchanged. What the relaxation costs is at row 16 (Section 6.2): every l in L* has row-16 values, the table stage has eight conditions, E|filt(u)| = 44/256 = 0.172 per lane.
The relaxation was measured for the published characteristic (a ratio of 1.5055, +0.59 bit, over the four patterns alone; 6 seeds, 4.0e8 samples, 30,814 collisions rebuilt and hashed again independently, 0 false; a sweep of 30 further pairs of conditions of rows 16..21 found no further gain). For the characteristic of this filing it is part of the carrier of the study of Section 7.4: the estimator accepts exactly what the program accepts.

### 7.5 The examined family of this filing

The estimator draws W8 from exactly the 4,378,186 variants of the 1,067 classes that the program examines, and (W6, W7) uniformly from F6 x F7. This filing examines **exactly that family**: every variant of every passing class is examined, and given a good pair the variant, W6 and W7 have the laws of the study
(Lemma 5.1: for every variant a0, W7x is uniform on F7 and W6x uniform on F6 given that the pair is good, independent of each other and of the variant). So q3 = the mean over the 4,378,186 variants and the 44 elements of L* of the study's conditional probability, with no hedge for a different or weighted subset.
**q3_used = 2^-70.34** (the exact event, Section 7.4). That the dependence on the variant is the four W24 conditions, about 2^-4 for every W8 (Lemma 7.1), is unchanged by the relaxations, which act on rows 16..19 only.
The row-16 pass rate of the program's own good pairs is the exact 2,893,824 / 2^32 per probed lane (Section 13.3: 3,324 row-16 passes among 4,829,581 good pairs of 300 trials of the counted program, 3,254 expected, z = +1.2).

### 7.6 Rows 18 and 19: the accepted value patterns (credit: Jbenisek's ffbe30bb-ac92-4191-a589-3bf32661ee7d)

Table 15 fixes the value bits E18[1] = 1, E18[5] = 0, E18[10] = 1, E18[11] = 1, E18[18] = 0, E18[28] = 0, E18[29] = 1 and E19[29] = 1. They are not all required. With every other cell and printed two-bit condition kept, ffbe30bb showed by an all-solutions enumeration with a verified 37-step model (Bitwuzla and Z3) that exactly four patterns of these eight bits admit a 37-step semi-free-start collision for the published dense part, because the bits enter only through six parity conditions: E18[1] = E18[11], E18[1] != E18[28], E18[10] = E18[29], E18[10] = E19[29], E18[5] = E18[18] and E18[5] ^ E18[1] ^ E18[10] = 0.
The seven E18 bits enter only through the signs of the signed difference of S1(E18) at step 19 (each output bit of S1 is the XOR of three taps, and the sign of the difference at that bit depends on the XOR of the two taps that carry no difference), and E19[29] only through E18[29] ^ E19[29] = 0 in the signed difference of Ch(E19, E18, E17) at step 21.
That enumeration, the 74 single-flip tests and the exact stage enumeration are ffbe30bb's and are quoted, not redone. For the dense part of this filing the program does not rely on the count four: it does not impose the eight value bits, and the exact signed-difference checks of both members that `row_ok` always made, at rows 19 and 21, decide which patterns pass; the estimator of Section 7.4 and the organizer experiment `a0-sfs-r37` (below) use the same checks.

The strings of the E cells of rows 18 and 19 in `lowm.py` (`CHE[18]`, `CHE[19]`) are

```text
 row 18   Table 15 ==10===uu====0==n===111===01==1=     program =======uu=======n=====1====1====
 row 19   Table 15 ==1====00====1==0==========1====     program =======00====1==0==========1====
```

(the remaining `1` of row 18 are E18[9] and E18[4], which stay imposed; so do the differences `u`, `n` and every other character). `row_ok` tests the masks and values of the cells as constants of the straight-line text, so the operation counts of Section 9 (`ROWCHECK`, `ROWCOMP` per row) are unchanged by this relaxation. The patterns, as flips of Table 15's values (E18 bits 29,28,18,11,10,5,1 | E19 bit 29):

| pattern | flipped bits of Table 15's values | flip masks (E18, E19) |
|---|---|---|
| 0 Table 15 | none | 0x00000000, 0x00000000 |
| 1 | E18[5], E18[10], E18[18], E18[29], E19[29] | 0x20040420, 0x20000000 |
| 2 | E18[1], E18[5], E18[11], E18[18], E18[28] | 0x10040822, 0x00000000 |
| 3 | E18[1], E18[10], E18[11], E18[28], E18[29], E19[29] | 0x30000c02, 0x20000000 |

The organizer experiment `a0-sfs-r37` imposes the R16x pattern 4 + (t mod 4) on its construction of trial t (`IMP` and `PAT` in `experiments/lowm.py`: patterns 4..7 are the four patterns above with E16[23] = 1 and E17[24] != E16[24]); it checks every cell of rows -4..21 with the program's own `row_ok` and, for every pair it returns, feeds the constructed chaining value to the counted online program, which must find exactly the constructed pair (Section 13.2).

## 8. The algorithm

### 8.1 Lemma 8.1 (the class test and the W6 test)

Let x = A_{-1}, cb = C6 - A_{-2}, q = A1 ^ x, and for a class with base and mask put

```text
CB3 = cb + (A1 & x) + (base & q),   KZ = K3C + x - (A1 & A2) - (base & FA),   FA = A1 ^ A2 = e1a5263d,   C4 = 92cedd4c,   e4 = a0 + C4,   e3 = KZ - (s & FA).
```

**Lemma 8.1.** (a) The class passes the W7 filter at x iff F7(c7 - x). (b) For a0 = base | s of the class, W6x = cb + phi(a0, x) = CB3 + (s & q) - H, mod 2^32, where H_j = e4_j for the bits j with E5_j = 1 and H_j = e3_j for the bits with E5_j = 0 (E5 = 76760d10).
Hence a0 is good (W7x in F7 and W6x in F6) iff its class passes and F6(CB3 + (s & q) - H).
*Proof.* (a) Section 5.1. (b) W6x = C6 - A_{-2} + MAJ(A1, a0, x) - CH(E5, e4, e3) with e4 = a0 + C4 and e3 = K3C - MAJ(A2, A1, a0) + x (Section 5.1), and CH(E5, e4, e3) selects bit j of e4 where E5_j = 1 and of e3 where E5_j = 0.
MAJ(A1, a0, x) = (a0 & (A1 ^ x)) | (A1 & x) with disjoint bit sets, so MAJ = (a0 & q) + (A1 & x); likewise MAJ(A2, A1, a0) = (a0 & FA) + (A1 & A2). Since a0 = base + s with base & s = 0 (Section 5.3), a0 & m = (base & m) + (s & m) for every mask m.
Collecting the scalar terms gives CB3 and KZ. QED. (Checked on every lane of every pass plane of the experiments and of `selftest`, 0 mismatches.)

There is no cube sharing in this family (Section 5.3): every rep of a list is tested by one W6 program run. The scalars CB3 and KZ are computed once per passing class; the planes of the reps (the 21 bits of the union of the masks, of which the bits outside a class's mask are static) are the only lane-dependent data. Both tests are programs on *planes*: a plane is a 256-bit word holding one bit of each of 256 lanes (the lanes of a batch are 256 consecutive reps of a list; for the class test, 256 consecutive classes).

### 8.2 The online algorithm

```text
input: N_FB, V_MAX; precomputed (Section 14.2): S, L*, the lists as planes of reps and packed entries, the 1,067 class descriptors, the c7 planes (five batches), the chunk tables LO and MID, the lane-scan table, per-l constants
V = 0
for f = 1 .. N_FB:
    draw two uniform 256-bit words; M0 := their sixteen 32-bit fields; CV1 := F_37(IV, M0)                                     [1 unit]
    x := A_{-1}; cb, q, CB2 = cb + (A1 & x), KXA = K3C - (A1 & A2) + x; the 21 planes of q; cv_pre(CV1)                          (Section 9.2)
    planes P7 := F7(c7 - x) over the 1,067 class lanes (bit-sliced, five batches of 256 lanes)
    for each set lane c of P7:                                                                                                    (passing class)
        CB3, KZ; the planes of CB3 (32), KZ (bits 0..28) and base (18 bits) are formed and stored                                (Section 9.3)
        for each sweep of two batches of reps of the class's list:
            load the 100 scalar planes; for each batch: load the planes of the reps; sums W := W6 program; pass plane := F6(W)   (Sections 9.4, 9.5)
            gather(pass plane)
        where gather(plane): for each set lane (r, i) of the plane (11-bit chunk scan):
                    entry := (packed word i of the batch)[part r] xor BP(class); place it in the next slot of the group register
                        when the group register holds four entries: U := packed row-16 address of the group                           (Section 9.7)
                            for each of the four lanes: u := U lane; G := filt(u) (two table reads)
                                if G != 0: for each l in G: if exact(u, l): recompute W6, W7; rows 16..21 of both members by cells with early abort, rows 22..36 replayed, eight registers compared   (Sections 7.4, 9.8, 9.9)
                                    if all rows pass: build m, m'; if digest(m) = digest(m') and m != m': output, halt
    the last group of the first block is padded by repeating its last entry and processed
    V += the counted work of this first block; if V > V_MAX: halt (failure)
halt (failure)
```

The loop is the function `attack(nfb, vmax)` of `experiments/lowm.py` (`python3 lowm.py attack N V`): at most N first blocks, V the counted data-dependent operations of Section 9, halt when V exceeds the cap; an output is verified with the target digest before it is returned. If the construction phases of Section 11.2 return no model or no family, there is no attack: the procedure halts (published data is never used in its place).

### 8.3 What is not assumed

No property of x other than being a 32-bit word is used, and nothing about the correlation of the classes of one first block: the ledger uses only the exact marginal law of each class test (probability p7 = |F7| / 2^32) and of each variant's F6 test given its class passes (p6 = |F6| / 2^32, exactly,
because cb is uniform and independent of x) and linearity of expectation. Padding lanes (the repeated last entry of a first block's last group) are probed and charged; a duplicated member that hit would be processed twice, which changes the cost (charged) and not the set of pairs found.


## 9. The counted program

### 9.1 Machine and pricing

256-bit word RAM, 64 registers, every executed primitive counted (loads, stores, branches and address additions included). 32-bit values are kept in the low bits; a reduction mod 2^32 is one AND; a 32-bit rotation pattern (S0, S1, s0, s1) costs 8: d = x | (x << 32) (2), three shifts and two XORs and one mask.
A conditional branch tests a register for nonzero and is one primitive. Every address that is not a register value is formed by a counted add (one add per plane or word load; a table read is an index extraction, an add of the table base and a load). The program text is straight-line code.
The target compression of a first block is one unit and its internal operations are not counted again.

**Plane algebra.** The plane programs are executed by `lowm.py` on Python integers of 256 bits through a small algebra whose every call is a primitive of the straight-line text: a plane carries a *static constant tag* (all-zero, all-one: a constant of S such as C4, E5, A1 ^ A2) and an *inversion flag* (the stored word is the complement of the true plane).
These are compile-time facts of the text, not data: x ^ 0 = x, x ^ 1 = ~x (flag flips; no primitive), x & 0 = 0, x & 1 = x, x | 1 = 1, x | 0 = x cost nothing; an AND or OR of two planes with equal flags is one primitive (both flagged: De Morgan, the stored words are combined with the dual operation);
an AND or OR of unequal flags costs a NOT first (2 primitives); every other XOR, AND, OR on dynamic planes is one primitive. A full-adder bit is `xy = a ^ b; sum = xy ^ c; carry = a ^ (xy & (a ^ c))`: 5 primitives, 4 without the sum; with a static constant operand bit b: xy = a or ~a (free) and carry = a & c or a | c: 1 primitive.
The counter `CN.n` of the algebra is the count of the plane programs; `process_cv` asserts the counts of the plane programs (W6 by cube size, the subtraction runs, F7 = 166) at every execution (the counts do not depend on the data). The scalar and control steps are counted where they execute by the constants below.

### 9.2 Fixed per first block: FIXED = 2,223 operations

First block words: 2 random words and the 16 fields (field 0 of a word: and; fields 1..6: shr, and; field 7: shr): 30; control 16 (loop counter add and compare-branch, the cap test, address arithmetic not itemised below): 46. Then:

- **Class test, 1,985 = 5 x 397:** the 1,067 classes occupy five batches of 256 lanes (the last with 43 lanes); per batch: -x mod 2^32 (2); the planes of -x, z_j = 0 - ((s >> j) & 1), consumed bit by bit (3 per plane, 2 for plane 0: 95); the 32 planes of c7 (32 loads and 31 address adds: 63); the adder c7 + (-x) with sums for the 17 bits {0, 1, 2, 9, 10, 11, 12, 18, 19, 22, 23, 26, 27, 28, 29, 30, 31} (140) and the F7 test (26):
  F7 is in the bitwise form of Section 5.1; F7_OPS = 166; the mask of the valid lanes (1); the scan of the plane (SCAN_FIX = 70: for each of the four 64-bit parts the extraction of the part (1 or 2) and for each of its six chunks (five of 11 bits, one of 9) the extraction (1 or 2) and a zero branch). The planes of -x are formed again for every batch (not shared; charged as executed).
- **Scalars and planes, 192:** cb = C6 - A_{-2} (2), q = A1 ^ x (1), A1 & x (1), CB2 = cb + (A1 & x) (2), KXA = K3C - (A1 & A2) + x (2); the 21 planes of q (the bits of the union of the masks, 1fbad9bb; 62) and their stores (21 stores and 20 address adds: 41);
  `cv_pre` (81 as in 0db0eeb6 Section 9.2: e0b, kap0, C = RBASE + (kap0 - e0b), x12, n12, X, Em2, kap1 and the broadcasts of the constants to four lanes, and the unpacking of the chaining value from the compression output).

46 + 1,985 + 192 = 2,223 (`FIXED` of `lowm.py`, asserted by the plane programs and by the executed counts of Section 13).

### 9.3 Per passing class: 410 + 6 operations

Per set lane of the class plane: table address 1, table load 1, chunk offset add 1, c & (c - 1) 2, branch 1: CLS_LANE = 6. Then: five loads of the class descriptor (base, BP = base | ((~S0(base) & M32) << 32), list pointers, batch count, cost word) with their address adds (10);
CB3 = CB2 + (base & q) (3) and KZ = KXA - (base & FA) (3); the planes of CB3 (95), of KZ for the bits 0..28 (86; e3 is needed up to bit 28, the highest bit with E5 = 0) and of base for the 18 bits that are not in every mask (54), 3 per plane; their stores
(79 stores and 79 address adds: 158); one work-counter update (1): 10 + 6 + 235 + 158 + 1 = 410. The class control (list pointer, batch count and the loop tests; CF_CLASS = 6 as in the program this one derives from, kept although there is one run per class).

### 9.4 Sweeps of two batches

A list of n reps is processed in nb = ceil(n / 256) batches (14 for 3,456 reps, 24 for 6,024), two at a time. A sweep loads the 100 scalar planes it needs once for both batches: zq (21), zKZ (29), zCB3 (32), zb (18), each one load and one address add, plus 3 of control: SWEEP_OVH = 203.
Per batch: the stored planes of the reps (21, with their address adds) and the two pointers of the batch: 44 operations.

### 9.5 The W6 program of one batch

Straight-line on planes (Lemma 8.1), with sums produced only for the bits that are used:

| step | primitives |
|---|---|
| a_j for the 21 mask bits: a_j = s_j for the 14 bits in every mask; a_j = s_j or zb_j for the other 7; a_j = zb_j (loaded) for the 11 bits outside the union | 7 |
| e4 = a + C4 (C4 static: carry = a & c or a \| c), sums for the 14 bits with E5 = 1 | 41 |
| e3 = zKZ - (s & FA) (FA & union has 7 dynamic bits: 0, 3, 4, 5, 21, 23, 24), sums for the 18 bits with E5 = 0 | 75 |
| Sq = s & zq on the 21 mask bits | 21 |
| W6a = zCB3 + Sq | 124 |
| W = W6a - H, sums for the 20 bits {1, 2, 3, 8, 9, 10, 12, 13, 14, 15, 16, 18, 19, 20, 25, 26, 27, 29, 30, 31} that F6 reads | 151 |
| F6 in the bitwise form of Section 5.1: pass = (w8 ^ w25) & ~fail | 27 |
| **total** | **446** |

The pass plane carries no inversion flag in the shipped text; `measure_ops` adds one primitive if it did, and `process_cv` asserts the total. A partial batch (the last, with fewer than 256 live lanes) costs one more AND with the lane mask.
**Registers.** The two batches of a sweep are processed together bit by bit, j = 0..31; the loaded planes of bit j are dead after use. Each batch holds the four carries (e4, e3, W6a, W) and the F6 operands that are kept for later bits, folded as soon as both operands of a term exist:
the pairs (w1, w12), (w2, w13), (w3, w14), (w14, w18), (w15, w19), (w9, w26), (w10, w27), (w16, w20), (w8, w25) and the three single bits w29, w30, w31; at most ten values at any bit. With at most six temporaries that is at most 20 live planes per batch, 40 for the sweep, plus about eight addresses, counters and constants: below 64, with no spill.

### 9.6 Scan of the pass plane, the reps and their members

The pass plane (zero in the unused lanes) is scanned in four 64-bit parts of six chunks (SCAN_FIX = 70 per plane); per set lane (a passing rep): table address 1, table load of the bit index 1, add of the chunk offset 1, add of the batch word pointer 1, load of the packed word 1, c & (c - 1) 2, loop branch 1: SCAN_LANE = 8.
The packed word i of a batch holds in its 64-bit part r the entry s | (S0(s) << 32) of the rep of lane 64 r + i. The entry is extracted (EXTR = 1, 2, 2, 1 for r = 0..3) and XOR'ed with BP (the result is a0 | ((~S0(a0) & M32) << 32) for the member a0 = base | rep, because S0 is linear and base, rep have disjoint bits).
Every rep is one member (no cube): it is placed: shift into slot k of the group register 1, or 1, slot update (sh + 64) & 255 2, branch on the full group 1, work-counter update 1, and the xor 1: PLACE = 7. A group of four members is complete after four placements; the last group of a first block is padded (PAD_OPS = 7).

### 9.7 The packed group: GROUP_BODY = 31, probe 11 + 12 + 12 + 12

Gw holds in each 64-bit lane a0 in bits 0..31 and ~S0(a0) & M32 in bits 32..63. With LM = 2^32 - 1 in every lane (as in 0db0eeb6 Section 9.6): Sw = Gw >> 32 (1); E0 = (Gw + bc(e0b)) & LM (2); mj = Gw & bc(x12) (1); ch = (E0 & bc(X)) ^ bc(Em2) (2); S1(E0) with the 8-primitive pattern (8);
W1 = (bc(kap1 + 1 + 3 2^32) + Sw - mj - S1(E0) - ch) & LM (5); s0(W1) (8); U = E0 + s0(W1) + bc64(C) (2); clearing the group register (1) and the work-counter update (1): 31. Lane k of U holds u + {0, 2^32, 2 2^32}, u = W0 + s0(W1) mod 2^32 (verified on 400 lanes with extreme chaining-value words: 0 mismatches).
The probe of lane k: the lane to the low end (k > 0: 1); lo = v & 0xfff (1); mid = (v >> 12) & 0xfff (2); the address of LO (add of the table base: 1; the table MID is placed at address 0, so mid is its address) and the two loads (2); T = LOw & MIDw (1), T >> 64 (1), their xor (1), & (2^44 - 1) (1); the branch on nonzero (1): 11 for lane 0 and 12 for the others.
This is the stage of Section 6.2; for G = filt(u) the table words are LOw = (pm, pm & cm) and MIDw = (P0, P0 ^ P1) in the 64-bit lanes 0 and 1.

### 9.8 Survivors and the exact test

When G != 0 (probability exactly 2,517,128 / 2^24 per lane, Section 6.2): u = lane & M32 and the scan of the 44-bit mask G in four chunks of 11 bits (SURV_FIX = 11); for each set bit l: table address 1, load 1, chunk offset 1, c & (c - 1) 2, branch 1, work-counter update 1 and the l-to-constant-address add 1 (SURV_LANE = 7), then the exact test of Lemma 6.2, straight-line, EX_OPS = 34:
e = u + C_l (load C_l 2, add 1, and 1); (e & 40461a80) ^ 00060800 (2); (e ^ E15x[4] word) & 0x10 (load 2, 2); A = e + cxA_l (load 2, add 1, and 1); (A & 22808000) ^ VA_l (and 1, load 2, xor 1); the three pair conditions with shifts 11, 12, 9 (x1 = A ^ (A >> 11), x2, x3: 6; and with 0x200, 0x40, 0x100: 3; or 2; xor 0x240: 1);
the OR of the four results (3) and the branch (1): 34, with no early exit.

### 9.9 The rare path

A pair with a row-16 pass for some l (probability at most 2,893,824 / 2^32 = 2^-10.54 per probed lane): work-counter update and lookup of the member (1 + 2); recompute W6 and W7 (RECOMP = 35); W0..W5 and W8 (201); then for each such l the y-words (8) and rows 16..36, each row 106 + 53 + 1 (both members' W 20, CH 3, E 14, MAJ 4, A 12 per word; the cells and two-bit conditions closing at the row at most 53, executed for rows 16..21 only, with early abort; rows 22..36 are replayed without a cell test and the eight registers are compared after row 36, at most 16 operations, covered by the unused 53 of those rows; the work-counter update 1),
charged for rows 16 and 17 always and for rows 18..36 with probability at most 2^-9 each (the stage factor of row 17 is 2^-12, Section 7.4c). These are the counts of 0db0eeb6 Section 9.7 and 7319bba.

### 9.10 The work counter V and the cap

V counts every executed data-dependent primitive: each of the following updates it by a constant (one primitive each, counted in the item): a passing class (its fixed price, sweeps, W6 programs and scans), a member (its placement and, for a rep, its scan and extraction), a group (its body and four probes), a survivor lane, a survivor bit (its exact test) and every row of the rare path.
The data-independent part (FIXED) is charged per first block. The cap is tested after every first block (compare and branch, in the control of 9.2). The overshoot past V_MAX is at most the maximal data-dependent work of one first block, vmax_fb = 722,960,904,448 (every class passes, every rep good, every l surviving, every probe hitting), which the ledger charges.


## 10. Success probability, independence and caps

Let a *trial* t = (f, a0, l) be a first block f, a variant a0 of a passing class and l in L*, and A_t the event that a0 is good for f, the pair follows every cell and printed two-bit condition of rows 16..21 and the eight registers of its two members agree after the replay of rows 22..36 (Section 7.4). The program examines every good pair of every processed first block (Lemma 8.1) and every l whose row 16 holds
(Lemma 6.2, exact), so it finds a success iff some A_t occurs before the cap, and every output is verified. Let X_f = sum over the trials of f of 1[A_t] and X = sum_f X_f.

- **Expectation.** E[X_f] = g x 44 x q3 (Lemma 5.1 and Section 7) with g = p7 p6 x 4,378,186 = 4647.70 the expected number of good pairs per first block (exact: each of the 1,067 classes passes with probability p7 and each of its variants then passes F6 with probability p6), and E[X] = N_FB g 44 q3.
  With q3 >= q3_used = 2^-70.34 (H2): E[X] >= mu0 = 0.50914839 (H7) for N_FB = ceil(mu0 / (g 44 q3_used)) = 3,720,517,587,736,805 = 2^51.72442, where mu0 is the smallest 8-decimal number strictly above -ln(0.61 - Pcap - 2^-60) / (1 - 2^-8.5), with Pcap = 0.00814700 the assumed bound of the work-cap failure probability below (Appendix C).
- **One first block (H3).** By Bonferroni, Pr[X_f >= 1] >= E[X_f] - sum over pairs t < t' of f of Pr[A_t and A_t'] = E[X_f] - (1/2) sum_t Pr[A_t] E[X_f - 1 | A_t]. H3: the average of E[X_f - 1 | A_t] over the trials t with the weights Pr[A_t] (the only quantity this sum needs) is at most delta = 2^-7.5, and we assume the bound for every trial t, so Pr[X_f >= 1] >= (1 - 2^-8.5) E[X_f].
  H3 splits into (a) the same variant with another l: at most 2^-11 (7319bba measured 0 further successes among 19,620,436 distinct Step-3 successes of its SMC, rule-of-three bound 2^-22.65, for the published pair; the four accepted patterns multiply the chance of passing rows 18 and 19 by about 4 and R16x the chance of the path by about 1.6, which gives about 2^-19.8 there, far below 2^-11), and (b) other good pairs of the same first block (rho and q3 as stated below; the measurements of Appendix H.6 are program checks, not a proof): at most rho x N_good x 44 x q3 with rho <= 2^35 (the measured factor at row 16 is 0.98 and 1.00 for the published pair), q3 <= 2^-70.21 (the exact event; derived in Appendix H.4: the 99 percent upper Student bound of the larger of the two sets of Section 7.4) and
  N_good <= 4,378,186 (all variants of the family, 2^22.06), so (b) <= 2^35 x 2^22.06 x 2^5.46 x 2^-70.21 = 2^-7.69 and delta <= 2^-11 + 2^-7.69 = 2^-7.55 < 2^-7.5 (margin 0.05 bit; the break-even q3 is 2^-70.15). (N_good is the number of all variants of the family; no size-biased mean is needed.)
- **Many first blocks (H1).** Distinct first blocks have independent chaining values, so the events X_f >= 1 are independent and Pr[X >= 1] >= 1 - exp(-sum_f Pr[X_f >= 1]) >= 1 - exp(-(1 - 2^-8.5) mu0).
- **Work cap.** The data-dependent work v_f of a first block (everything except its compression and its FIXED operations) has mean vbar = 400160.05 (Section 11) and is at most vmax_fb = 722,960,904,448. The v_f are independent (H1), so by Chebyshev
  Pr[sum v_f > (1 + s) N_FB vbar] <= E[v_f^2] / (s^2 N_FB vbar^2) <= vmax_fb / (s^2 N_FB vbar) = Pcap with the slack s = 2^-12: Pcap = 2^-6.94 (<= 0.00814700). V_MAX = ceil((1 + s) N_FB vbar) = 1,489,165,979,804,742,916,402 is exceeded with probability below Pcap; the run then fails, which is accounted for here.
  No part of v_f depends on a conditional law of the scalars: the plane programs cost the same for every data, and the data-dependent items are linear in the numbers of passing classes, good pairs, groups, survivors and hits, whose exact means the ledger uses.
- **Success.** Pr[output a collision] >= 1 - exp(-(1 - 2^-8.5) mu0) - Pcap - 2^-60 = 0.3900000021 > 0.39 (the 2^-60 covers a repeated first block among N_FB draws of 512 bits). Any output is a verified collision, independent of the premises.

## 11. Ledger (exact; `python3 experiments/lowm.py ledger`; the program of Appendix B reproduces it from the stage prices)

```text
T = A_C + A_S + DEV + N_FB + (N_FB x 2223 + V_MAX + vmax_fb + PRE + FIN) / C + 6
  A_C = 91,298,997,556 = 32,381.45 CPU-seconds x 2^21.427 units (2^36.41)   the metered search of the 37-step dense model whose output is used (H4, Appendix L)
  A_S = 12,339,615,049 = 4,376.55 CPU-seconds x 2^21.427 units (2^33.52)    the Step-1 solve that returned S (H4, Section 11.2)
  DEV = 2^42   all development computation (Section 13.4)
  N_FB = 3,720,517,587,736,805 compressions (2^51.72442; mu0 = 0.50914839, q3 = 2^-70.34, g = 4647.70 good pairs per first block)
  2223  fixed operations per first block (Section 9.2: first block and control 46, class test 1,985, scalars and planes 192)
  V_MAX = 1,489,165,979,804,742,916,402 = ceil((1 + 2^-12) N_FB vbar), vbar = 400160.05 operations, of which (per first block, exact expectations or the stated bounds)
               class scans (6 per passing class, 1,067 p7 classes):                                  101.59
               passing classes (p7 x [preparation, sweeps, W6 programs, scans, reps, members]):   267119.24
               groups (E ceil(N/4) <= (g + 3)/4 groups of 31 + 47, plus the last-group padding):  90695.68
               survivors (per probed lane 0.1500 x 11 + 44/256 x (7 + 34); probed lanes <= g + 3): 40448.23
               row-16 hits (every probed lane may hit, 2,893,824 / 2^32 per lane):                1795.30
  vmax_fb = 722,960,904,448 (one first block's maximal work: every class passes, every variant is good, every l survives, every probe hits)
  PRE = 670,924,540,390 operations = 90 CPU-seconds x 2^21.427 x C (Sections 11.2, 14.2); FIN = 1600 operations and 6 compressions
N = C T = 1,507,285,642,753,610,495,235     ->   T = 2^58.983936   ->   time_log2 = 58.98394
preprocessing = A_C + A_S + DEV + PRE / C = 2^42.03368 (claimed 42.03369, rounded up)
```

Every count in this block is produced by `ledger()` of `experiments/lowm.py` from the executable routines (stage prices asserted by the plane programs; the scalar items as listed in Section 9), and Appendix B reproduces N from the stage prices alone with integers and Fractions; the integer tightness of the fifth decimal is asserted in both directions.
Per first block the program spends 153.19 units (1 + 2223/C + vbar/C); per good pair the data-dependent work is 86.1 operations. The one sensitivity a declared premise needs: with q3 one bit lower, 2^-71.34, the claim would be 59.96490 (the table of Appendix H.5 gives the others).

### 11.1 Exactness of the expectations

Each row is linear in a count whose expectation is exact: a class passes with probability p7 (Section 5.3), a rep of a passing class is good with probability p6 (Lemma 5.1), a probed lane has exactly 44/256 survivors on average and a nonzero filter with probability exactly 2,517,128/2^24 (Section 6.2), and 2,893,824/2^32 row-16 hits (Lemma 5.1: u uniform).
One row is a bound on an expectation that is not exact: the number of groups E ceil(N / 4) <= (E N + 3) / 4 (the padding of the last group of a first block is charged at its worst case; the exact value is E N / 4 + E[(4 - N mod 4) mod 4] / 4 <= E N / 4 + 3/4).
It is below 0.2% of vbar.

### 11.2 The construction charges A_C, A_S and PRE (H4)

The attack uses a characteristic, S and a family of variants. Collision-frontier-v5 requires that "All construction/preprocessing and advice must be accounted for, including any search omitted from the submitted program". Each of the three is the output of a procedure that is charged here at the CPU-seconds of its measured run (kissat is deterministic for a fixed binary, input and options, so a rerun repeats the search), converted at the price of 2^21.427 units per CPU-second at C = 2644 that the accepted filing 6eeefb64 calibrated on its measured complete re-run of the predecessor 35-step search (593,858 CPU-seconds there).

**P_C, the characteristic (A_C = 91,298,997,556 units = 2^36.41).** (1) `gen37.py dense_pub.cvc --chi chi37.txt --fix 16-24 --fixw 22,24 --W 25 --O2 7 --O3 25 --E 63` (the unmodified LLW24 FunctionModel of the 37-step dense model; `chi37.txt` supplies only the cells of rows 16..24 and of W22, W24, Section 3.5), (2) the translation to SMT2, (3) the STP CNF dump (`dense_pub.cnf`, sha256 445a880e...42f4, 200,534 variables, 954,732 clauses), (4) kissat 4.0.4 on the CNF, seeds 1..8, (5) the decoding of the model of seed 4 into the signed cells of rows 6..15 (`decode_model.py`, `stp_check.sh`; `seed4.full.chi`). The model of seed 4 is used because it is the lowest seed whose characteristic has the message XOR masks of the window that the generator of P_S encodes (W6 20000000, W7 04400800, W8 20000000, W9 050112aa, W10 00081400, W14 04400800, W15 20000000; seeds 4 and 7 have them, read from the decoded models). Measured (cloud, AMD EPYC Turin, 32 vCPU, shared): setup 29.45 s (7.63 + 3.34 + 18.48), seed 4 completed after 4,039.31 s user + 1.42 s system (wall 4,044 s, 81,652 KB); all eight seeds completed (Appendix L). The charge is the portfolio run to the finish of seed 4: 8 x 4,044 + 29.45 = 32,381.45 CPU-seconds (the eight seeds actually used 9,919.35 CPU-seconds; the difference covers the decoding of the eight models).

**P_S, S and the pair (A_S = 12,339,615,049 units = 2^33.52).** (1) The signed cells of `seed4.full.chi` for rows 6..15 and the signed cells of rows 4, 5 and 16..24 as in the paper (`mk_h3.py`; `chi37_H3_seed4.txt`, sha256 b5580e03...a2ae), (2) `dense_sat.py chi`, the generator of the SAT instance of a semi-free-start pair for the window of the paper's Section 4.1 (the one-bit message family at disturbance bit 29, expanded differences in rows 22 and 24, state differences inside the window): 0.34 s user, 70,828 KB, the CNF `dense_chi.cnf` (107,359 variables, 373,031 clauses, sha256 2ad3a254...7d57) and its variable map, (3) kissat 4.0.4 with default options and `--seed=1`, and a second process with `--seed=2 --sat --walkinitially=true`, both under `prlimit --as=379625062`, `--time=43200`; the first model stops both, (4) `s4_derive.py` decodes the model into CV, M, M' and S, and verifies the 37-step collision and every signed cell (Section 3.4). If no model is returned the procedure halts: published data is not used in its place. Measured: seed 1 returned SATISFIABLE after 2,187.92 s user + 0.17 s system (wall 36:28, 64,168 KB); the second process returned a model after 1:35:19. The charge is the two processes at the winner's time plus the generation: 2 x 2,188.09 + 0.37 = 4,376.55 CPU-seconds. (The step-1 re-solve of s37_all.cnf with A_S = 2^50 of earlier filings is not part of this filing.)

**P_F, the family and the tables (PRE = 90 CPU-seconds).** `gscan.c` (G for S: 0.46 s user + 0.03 s system, 1,912 KB), `grp.c` (the classes by c7 value, at least 3,456 variants: 1.32 s user + 0.15 s system, 344,284 KB), `lscan.c` (L and L*: 66.61 s user + 0.05 s system, 132,988 KB), `stats.c` (|F6|, |F7|, the row-16 pairs and the filter statistics: 6.86 s, 1,656 KB), then the lists, planes, packed entries and tables of Section 14.1 from the output (fewer than 2^29 word operations, Section 14.2). Measured total 75.48 CPU-seconds; charged 90 (the margin covers the tables). `gscan`, `grp`, `lscan` and `stats` ran under `prlimit --as=536870912`; `stats` has a peak of 1,656 KB.

Rows 16..24 of the characteristic, the cells that A_C holds fixed and that the program uses as its guide for rows 16..21, are the advice of Section 3.5: an input of P_C, not an output.

DEV is 2^42 units (Section 13.4).


## 12. Premises

**H1 (score-critical).** Our theory: the first blocks M0 are fresh uniform 512-bit strings; their chaining values CV1 = F_37(IV, M0) behave as independent uniform 256-bit values; in particular x = A_{-1} is uniform on 2^32 and independent of cb = C6 - A_{-2}, which is uniform on 2^32. Consequences used: each of the 1,067 classes passes the W7 test with probability p7 = |F7|/2^32 exactly, each variant of a passing class then passes F6 with probability p6 = |F6|/2^32 exactly, and given both, W0..W5 are uniform and independent of (W6, W7) (proof.md Lemma 5.1); hence the expected number of good pairs per first block is g = 4,378,186 p7 p6 = 4647.70, the expected counts of the ledger, and the independence of distinct first blocks.

*Scope.* The expected numbers of passing classes, good pairs, survivors and row-16 passes per first block; the expected operation count of the counted program; the law of the second-block words that defines q3; independence across first blocks (proof.md Section 10). Not the validity of any output: every output is verified with the target. *Evidence.* Measured by 7319bba with the attack's own filters on real first blocks in C (2^21 and 2^23 first blocks of the published family: passing classes 7,400,134 and 29,545,568 against 7,388,160 and 29,552,640 expected; good pairs ratio 1.0034 and 1.0011; the filters F6, F7 and the laws of Lemma 5.1 are those of this family) and by this filing's own run of the counted program on 28,500 real first blocks (6 runs, all 1,067 classes): passing classes per first block 17.07 against the exact 16.93, good pairs 4635.8 against the exact 4,647.7, mean counted operations 403,457 against the ledger's 402,383 (proof.md Section 13.3). The attack applies the same rates to its 2^51.7 first blocks; the organizer experiments a0-online-r37 and h1-cv1-filters-nonce run the program and the two filters on real chaining values. *Limitations.* Per-first-block counts are overdispersed (the class tests of one first block are correlated); only their expectations and the independence across first blocks are used.

**H2 (score-critical).** For a good pair, q3 = the average over the 4,378,186 variants of the 1,067 classes (each equally likely, as examined here) and the 44 elements of L* of Pr[rows 16..21 of both members follow every cell and every printed two-bit condition closing at rows 16..21 (corrected reading A15[29] = A17[29]), the eight value bits E18[1,5,10,11,18,28,29] and E19[29] of Table 15 not imposed, and (R16x) E16[23] = 0 and E16[24] = E17[24] not imposed, and rows 22..36 replayed on the raw schedule words end with the eight registers of the two members equal: exactly the checks of experiments/lowm.py step3b] satisfies q3_used = 2^-70.34 <= q3 <= 2^-70.21, where 2^-70.34 is the lower of the two 99 percent Student lower bounds (2^-70.2979 and 2^-70.3394), rounded down to two decimals of log2, of two preregistered sets of 64 seeds of a sequential Monte-Carlo estimator written for this family (proof.md Section 7.4, Appendix F), and 2^-70.21 is the larger of the two 99 percent upper Student bounds (Appendix H.4).

*Scope.* The expected number of successes E[X] = N_FB g 44 q3 and hence N_FB (proof.md Sections 7 and 10). The good pairs and the later rows are those of 7319bba; this filing changes how the good pairs are found, not which pairs are good, and which pairs count as a success: (from ffbe30bb) the value patterns of rows 18 and 19 and (R16x) rows 16 and 17. *Evidence.* Lemma 7.1: rows 16..21 have exactly the same probability for every variant; a variant enters rows >= 23 only through W8. The estimator (exact row 16, exact importance weights at rows 17..21, (W6, W7) uniform on F6 x F7, W8 drawn uniformly from the 4,378,186 variants, the exact event on every tail proposal; Appendix F) was preregistered (PREREG_s4.md, sha256 51c64a83...81300, before any listed seed ran): S1 (64 seeds) mean 2^-70.2581, relative sd 0.0914, bound 2^-70.2979; S2 (64 seeds) mean 2^-70.2885, relative sd 0.1160, bound 2^-70.3394; z = 1.15; declared 2^-70.34 (published pair: 2^-70.16). The same source compiled for the published pair reproduces the filed output of seed 9201 bit for bit. Forty hits of the estimator, each rebuilt to a chaining value and W0..W15, are all real 37-step semi-free-start collisions (40 of 40). The estimator source, the preregistration, the analysis program and the 144 per-seed estimates are printed in Appendix F, so the study replays from the proof; a0-sfs-r37 builds real 37-step semi-free-start collisions with the same end event. The R16x relaxation and the four value patterns of rows 18 and 19 are part of the carrier; the estimator accepts exactly what the program accepts. Here the examined law is the studied law (every variant of every passing class, no weighting). *Limitations.* Student coverage of the mean of 64 replicates (one per seed) per set: relative sd 0.09 and 0.12, skewness 0.31 and 0.15, and the percentile bootstrap agrees with Student to 0.002 bit (Appendix H.4). The tail draws (W6, W7) uniformly from F6 x F7 by Lemma 5.1; the row-16 stage equals the exact counts of stats.c. Premise (our theory): q3 is our computation, with the estimator, the preregistration and the 144 estimates printed in Appendix F. No organizer experiment executes its end event: rows 22..36 reach the digest only through a second-block chaining value that must be equal, which needs a reachable first block, that is the attack itself (a0-sfs-r37 returns semi-free-start pairs and no full collision of the target). The organizer-executed h3-ladder-r37 runs the row-16 stage of q3 on organizer seeds: 156 exact row-16 passes among 240,028 W6 passes (6.5e-4, three seed sets) against the 6.74e-4 of stats.c.

**H3 (score-critical).** For every trial t = (first block, variant, l), the expected number of other successful trials of the same first block given that t succeeds is at most 2^-7.5: E[X_f - 1 | A_t] <= 2^-7.5. Equivalently: (a) the expected number of other l in L* succeeding with the same variant is at most 2^-11, and (b) for other good pairs t' of the same first block, Pr[t' succeeds | t succeeds, t' good] <= 2^35 Pr[t' succeeds | t' good].

*Scope.* The per-first-block Bonferroni bound Pr[X_f >= 1] >= (1 - 2^-8.5) E[X_f] (proof.md Section 10). The good pairs of a first block and their dependence structure are those of 7319bba; this filing changes the order in which they are processed, not the set. *Evidence.* (a) 7319bba's replay of 19,620,436 distinct Step-3 successes of the SMC for the published pair: 0 further successes among the other 31 elements of L* (rule-of-three 95 percent bound 2^-22.65 per success); the accepted patterns raise the chance of passing rows 18 and 19 by about 4 and R16x the chance of the path by about 1.6, so about 2^-19.8 there, far below 2^-11. (b) With q3 <= 2^-70.21 (H2, the exact event; Appendix H.4), the expected number of further successes among other good pairs is at most rho x N_good x 44 x q3 with N_good <= 4,378,186 (all variants of the family): 2^35 x 2^22.06 x 2^5.46 x 2^-70.21 = 2^-7.69, so delta <= 2^-11 + 2^-7.69 = 2^-7.55 < 2^-7.5; the measured factor at the row-16 level over 2^21 and 2^23 real first blocks of the published family is 0.98 and 1.00. The organizer experiment h3-cowpass-nonce counts the first blocks in which several variants of one class pass F6 together. The sensitivity of the claim to delta is in Appendix H.5. The organizer experiment h3-ladder-r37 (proof.md Appendix H.7) counts, on organizer-seeded real first blocks, the pairs of distinct variants of one first block that both pass each level of the attack through the exact row-16 test, against the pairs expected if they passed independently: our replays (three seed sets, the third the organizer runner's own run) give the dependence factor 2.77, 2.55 and 2.44 at the W6 filter (variants of one class share bits), 0.99, 1.00, 1.00 and 0.99, 1.02, 1.00 at the two table levels, and 1.25, 1.13 and 0.71 at the exact row-16 test (35, 58 and 63 passes). *Limitations.* rho = 2^35 is the allowance over the measured row-16 factor (0.98 and 1.00) for rows >= 17 of distinct good pairs of one first block; delta <= 2^-7.55 against the declared 2^-7.5. Premise (our theory): rows 17..36 are not reachable by any organizer experiment of 20 s; for them rho = 2^35 over the measured factor (0.71 to 1.25 through row 16) is the stated allowance, 2^1.75 per later row, with the margin of 0.05 bit.

**H4 (supporting).** The characteristic, S and the family the attack uses are the outputs of three charged procedures, with the measured CPU-seconds of their runs at the price of 6eeefb64 (2^21.427 units per CPU-second): P_C, the metered search of the 37-step dense model (kissat seed 4 of eight; A_C = 91,298,997,556 units = 2^36.41, charged as eight seeds to the finish of seed 4 plus setup, 32,381.45 CPU-seconds), P_S, the Step-1 solve on the SAT instance generated from the signed cells of that characteristic (A_S = 12,339,615,049 units = 2^33.52, two processes at the winner's 2,188.09 s plus 0.37 s of generation), and P_F, the programs gscan.c, grp.c, lscan.c, stats.c and the tables (PRE = 90 CPU-seconds); all development computation at DEV = 2^42. The cells of rows 16..24 are advice, below 2^13 bytes, an input of P_C.

*Scope.* The preprocessing part of the ledger (2^42.03368) and the advice (below 2^13 bytes). *Evidence.* proof.md Section 11.2, Appendices G, H.3 and L. The runs are complete and their records are in the appendices: P_C seed 4 SATISFIABLE after 4,039.31 s user + 1.42 s system, all eight seeds completed, models verified against the CNF; P_S SATISFIABLE after 2,187.92 s + 0.17 s, model verified (all 373,031 clauses), decoded into a pair that collides on the real 37-step compression with every signed cell of rows -4..36 equal to the characteristic; P_F measured 75.48 CPU-seconds. The program uses nothing but these outputs and the advice: no published S, pair or family is used in their place. Kissat is deterministic for the fixed binary, input and options, so each run repeats; hashes, solver outputs and CPU-seconds are in Appendix L. Sensitivity (Appendix H.5): the claim moves by under 0.0001 bit if A_C (about 190 times larger) or A_S (about 1,400 times larger) is 2^44 units; DEV = 2^42 covers the 2^40.2 units of development 3.4 times (Section 13.4). *Limitations.* The CPU-seconds are those of our runs on the cloud machine, at the price of 6eeefb64 (2^21.427 units per CPU-second). The advice rows 16..24 are published input. Premise (our theory): A_C, A_S and PRE are the CPU-seconds of completed runs, converted at the price of 6eeefb64; runs of 4,044 s and 2,188 s do not fit 20 s and 128 MiB, so no organizer report validates them, and the claim moves by under 0.0001 bit if A_C or A_S is 2^44 units (Appendix H.5).

**H5 (score-critical).** Under collision-frontier-v5 a word-RAM program of 256-bit primitives in which every executed load, store, logic operation, shift, addition, comparison, branch and jump is one primitive is charged by the primitives it executes. The W7 class test (166 primitives for 256 classes, five batches for the 1,067 classes) and the W6 test of a batch of 256 reps (446 primitives) are straight-line plane programs whose counts do not depend on the data, produced by a plane algebra in which static constants fold and complemented planes carry an inversion flag at no cost, and in which a NOT is paid when an AND or OR meets unequal flags; two batches are processed together bit by bit with at most 20 live planes each (64 registers, no spill). The group of four members is 31 primitives, the probe of a lane 11 or 12, the survivor scan 11 plus 7 per set bit, the exact row-16 test 34, with the scalar and control items of proof.md Section 9. All tables, the code (bounded by 2^16 bytes) and the constants occupy 12,676,416 bytes = 2^23.60. The classes are base | s for s in 262 lists (derived from c7 by Lemma 5.3 and checked for all 4,378,186 variants); there is no cube sharing.

*Scope.* The class-test, W6, scan, gather, group, probe and survivor terms of the ledger (essentially all of the data-dependent operations per first block), the fixed terms, the memory figure and the preprocessing bound. *Evidence.* The program is experiments/lowm.py (the plane programs assert their counts at every execution; process_cv counts every scalar item where it executes). It is exact against the scalar definitions: every lane of every class-test plane and every pass plane equals the F7 or F6 test of its definition (213,400 and 198,624 lanes in selftest, and every lane of every processed class in a0-online-r37 and in the 300 trials of Section 13.2), the sets of good pairs equal the brute-force sets, the address u equals W0 + s0(W1) from the step equations, the exact row-16 test equals the generic row check on random and near-miss values, and the table stage never rejects a member. The counted operations per first block over 28,500 real first blocks are 1.003 times the ledger's expectation (proof.md Section 13.3). *Limitations.* The static constants and inversion flags of the plane algebra are compile-time facts of the text; the register argument counts live planes. The code size is bounded by 8192 primitives of at most 8 bytes. A branch on a register is one primitive, as in the earlier filings. The ceiling of the group count and the survivor scan are charged at their worst case (below 0.2 percent of the data-dependent work), and the class test recomputes the planes of -x for each of its five batches and is charged so.

**H6 (score-critical).** Declared bound: the peak memory of the whole procedure, the construction of the characteristic (the generation of the SAT instance of the 37-step dense model, its CNF dump and the solver search, charged as A_C), the construction of S (the generation of the pair instance and its solver search, charged as A_S), the preprocessing (gscan, grp, lscan, stats and the tables), the online program and development, is at most 2^33 = 8,589,934,592 bytes (the construction phases ran under address-space caps of at most 2^29 bytes; the aggregates of the development runs are in Appendix H.2), so memory_log2_bytes = 33 and the score is time_log2 + 13. The online tables, code and constants take 12,676,416 bytes = 2^23.60.

*Scope.* The memory term of the score. The time ledger is unchanged. *Evidence.* Measured peaks (resident set, one thread, cloud machine; Appendix H.2): gen37.py 97,816 KB, translation to SMT2 97,712 KB, STP 2.4.1 CNF dump 488,696 KB = 500,424,704 bytes (2^28.899), kissat 4.0.4 seed 4 on the characteristic instance 81,652 KB under prlimit --as=379625062 (2^28.5); the pair instance generator 70,828 KB and kissat 64,168 KB under prlimit --as=379625062; gscan 1,912 KB, grp 344,284 KB, lscan 132,988 KB under prlimit --as=536870912, stats 1,656 KB; online 12,676,416 bytes. The q3 study of Section 7.4 ran 4 processes at a time in one cgroup (MemoryMax 402,653,184 bytes, no swap): aggregate peak 338,391,040 bytes = 2^28.33, driver included (Appendix H.2). *Limitations.* The largest peak of one phase is the STP dump, 2^28.899 bytes; the largest aggregate of a development run is 2^32.70 bytes (the Python counted-program checks).

**H7 (supporting).** The cap target is mu0 = 0.50914839, the smallest 8-decimal number strictly above -ln(0.61 - Pcap - 2^-60) / (1 - 2^-8.5) with Pcap = 0.00814700 the assumed bound of the Chebyshev work-cap failure probability. With E[X] >= mu0 the success bound of proof.md Section 10, 1 - exp(-(1 - 2^-8.5) mu0) - Pcap - 2^-60, is >= 0.39000000 with no further padding.

*Scope.* N_FB (the cap) in the ledger. *Evidence.* Every allowance is an explicit term of the floor equation: the Chebyshev cap-failure bound Pcap (priced in proof.md Section 10 from the exact vmax_fb and vbar of the ledger; the computed bound is 2^-6.94), the repeated-first-block allowance 2^-60, and the H3 dependence discount as the divisor (1 - 2^-8.5). Appendix C computes mu0 and the bound with 60-digit decimals and asserts the bound > 0.39; lowm.py ledger() iterates Pcap and N_FB to a fixed point and asserts the same. *Limitations.* The 0.39 floor is the organizer's success requirement; the equation makes the success arithmetic exact.

## 13. Evidence and runs

The construction runs (A_C, A_S, PRE, the estimator of Section 7.4 and the long tests below) were made on the cloud machine (AMD EPYC Turin, 32 vCPU, shared, Ubuntu; every job `nice -n 10`, an address-space cap of at least the process's need, its own processes only); the organizer experiments were replayed in the organizer's Docker sandbox on a local WSL host; Python standard library (`experiments/lowm.py`). The programs and numbers that are used as premises (7319bba, fb039a6e, ffbe30bb) are labelled as such; the q3 study of Section 7.4 was run for this family with `smc_s4.c` (Appendix F).

### 13.1 Quoted from 7319bba (end to end on real first blocks; inherited evidence for H1, H3 for the published pair)

C statistics of 7319bba on the published family (random M0 from xoshiro256**, CV1 = F_37(IV, M0), the W7 tests of the 222-class family, the scalar W6 test of every variant of every passing class, u and the exact row-16 test for every l, exact checks of sampled pairs):

| run | first blocks | passing classes (expected) | good pairs (expected; ratio) | row-16 pairs (expected; z) | H3 factor: sum R(R-1) / p^2 sum G(G-1), p = 1052672/2^32 |
|---|---|---|---|---|---|
| seed 5eed0021 | 2^21 | 7,400,134 (7,388,160) | 1,748,648,111 (1,742,708,500; 1.00341) | 424,363 (422,895; +0.88) | 0.981 |
| seed 5eed0023 | 2^23 | 29,545,568 (29,552,640) | 6,978,649,557 (6,970,834,000; 1.00112) | 1,693,297 (1,691,580; +0.51) | 0.979 |

The counts are strongly overdispersed (variance-to-mean ratios 28.8 for passing classes, about 23,100 for good pairs, 6.6 for row-16 pairs) because classes are correlated; their means match. 7319bba's replay of 19,620,436 distinct Step-3 successes of the SMC found 0 co-successes across the other 31 elements of L*.
The filters F6, F7 and the laws of Lemma 5.1 are the same for the family of this filing; the classes and the lists are not. Section 13.3 is this filing's own run.

### 13.2 Exhaustive checks and equivalence with the definitions (this filing)

- **F6, F7 and G.** The definitions of F6 and F7 against their bitwise forms over all 2^32 words, |F6| = 287,309,824 and |F7| = 68,157,440, 0 mismatches (0db0eeb6, Tungsten; the bitwise forms are those used by the plane programs here, which `selftest` and the experiments compare with the definitions on the lanes below); `stats.c` recounts both from the definitions (Appendix G). |G| = 21,935,501 (`gscan.c`, exhaustive over the 2^29 values of E4); the equivalence of the W8 conditions of G with the printed cell and two-bit conditions over all 2^32 words (`f8.c`).
- **The classes and the lists (`lowm.py family`).** The 1,067 classes recomputed from their c7 values by `fibre`: 4,378,186 variants, the histogram of sizes of Section 5.3, the union 1fbad9bb and the intersection 18a898bb of the masks all equal the output of `grp.c` (0 differences); maximum S0(a0) over the variants 0xffffff05 (lane safety of the packed words). (1 min 52 s, 2.4 GB of Python memory on the cloud machine: a verification command, not a phase of the attack.)
- **The plane programs and the tables (`lowm.py selftest`).** Output in Appendix D: the sample of 8 classes against the definitions (membership, c7, size), the F7 sampler (20,000 draws), the W6 plane programs on 198,624 lanes (14,912 F6 passes), the class test on 213,400 lanes (200 values of x, half constructed to pass a class), the row-16 stage, the packed address on 400 lanes: 0 mismatches of every kind.
- **Row 16.** The exact test of Lemma 6.2 against the generic row check (`row16_ok`) on random and near-miss values of E16x for all 44 l, and filt(u) containing every l of every member: 0 mismatches (`selftest`); the exact counts of `stats.c` (2,893,824 pairs, 41 l with 65,536, l = 25 and 42 with 69,632, l = 29 with 67,584) are the counts of the independent enumeration of `smc_s4.c` (Section 7.4); the sums of |filt| over the 2^24 values of u mod 2^24 are the exact means of the ledger.
- **Packed address.** The 4-lane U against the definition u = W0 + s0(W1) of the chaining value and a0 (400 lanes, extreme chaining-value words): 0 mismatches.
- **Unrestricted run of the experiment checks (`run_online.py`, 300 trials, seeds `K|t`).** The checks of `a0-online-r37` (every lane of the class-test and pass planes, the good sets against brute force over all variants of the processed classes, the addresses, the table stage and the exact test against the row-16 definition, the cells of rows -4..15 for all 44 l) on 1,069 first blocks, **up to 100 passing classes** of each processed first block (18,178 classes, 4,869,640 good pairs, 1,217,446 groups, 835,700 survivors of the table stage, 3,270 row-16 passes): 0 mismatches of every kind.
- **Planted collisions (`run_sfs.py`, 128 trials).** The constructed semi-free-start collisions (a0 a variant of a chosen class, rows 16..21 by cells with the patterns 4..7, rows 22..36 by the exact end event; patterns 0..3 are not built): 80 of 128 trials built a pair (the others exhaust their proposal budget), every built pair is a real 37-step semi-free-start collision (the two compressions are equal), and the counted online program restricted to the class of a0 found exactly the constructed pair (a0, M, M') in 80 of 80.
- **Organizer experiments (replayed in the organizer's sandbox; inside 20 s and 128 MiB).** `a0-sfs-r37` (256 trials; trials 0..7 construct): 5 of the first 8 trials built a 37-step semi-free-start collision with a variant dense part (trials 2, 3, 5, 6, 7; patterns 6, 7, 5, 6, 7), each with checks_passed = 1 (every cell of rows -4..21 and every printed condition holds for the variant, a0 in G and in its class, W8 differs from S's), and for each the counted online program restricted to the class of a0 found exactly the constructed pair (detected_by_counted_program = 1 in 5 of 5); the other trials exhaust the shared proposal budget of 2^20 tail proposals and return no pair; about 6 s. `a0-online-r37` (trials 0..7): 31 first blocks drawn, 22 classes processed, 4,513 good pairs, 1,129 groups, 811 survivors of the table stage, 1 row-16 passes; class-lane, pass-lane, good-set, address, row-16 and cell mismatches: 0, 0, 0, 0, 0, 0 (pairs checked against every cell of rows -4..15 for all 44 elements of L*: 10); about 4 s. `h1-cv1-filters-nonce` and `h3-cowpass-nonce` (256 trials of 150 first blocks each, one program): 38,400 first blocks, 630 W7 passes (609 at the exact rate), 10008 W6 passes over the four variants (10275 at the exact rate), 3676 first blocks with two or more variants passing F6, 65 with both a W7 and a W6 pass; about 4 s.

### 13.3 The counted program run on real first blocks (premises H1, H5)

`experiments/lowm.py`'s `process_cv` was run on 28,500 real first blocks in 6 runs (first words from SHAKE-256 of the seeds `s4cal<tag>|<t>`, real 37-step compressions, all 1,067 classes, every operation counted), without any restriction of the family.
Realized counts: 17.07 passing classes per first block against the exact 16.93, 4635.8 good pairs per first block against the exact 4,647.7, and, over the 6 runs, a mean of 403,457 counted operations per first block (the 46 first-block operations included) against the ledger's expectation 402,383 (= FIXED + vbar): ratio 1.003 (the standard error of the pooled mean is 1.5%; the counts are bursty, standard deviation across first blocks about 2.5 times the mean). The ledger does not use this run; it uses the exact expectations, and the run is a check of them.
The realized operations of every category (class test, scalars, class preparation, sweeps, W6 programs, scans, members, groups, probes, survivors, rare path) are the executed counts of Section 9's prices.

### 13.4 Development computation

All computation of this line of work, with the runs still open counted at their caps: four kissat seeds on the 37-step dense instance with rows 16..24 free (86,400 s each, 345,600 s; not finished at the time of writing), the Step-1 diagnostics (the control on the published signed path 9,058 s, the second seed on the path of this filing 5,719 s, a third path at its cap of 43,200 s, the probes about 60 s), the G, grouping and L* scans and their repeats (below 600 s), the preregistered estimator runs of Section 7.4 (144 seeds, run twice, below 10,000 s), the counted-program checks and calibrations above (below 30,000 s) and local runs (below 10,000 s): below 4.5 x 10^5 CPU-seconds = 2^18.8 CPU-seconds, 2^40.2 units at 2^21.427 units per CPU-second. A_C and A_S are charged separately (Section 11.2). DEV = 2^42 units (2^20.6 CPU-seconds) covers it 3.4 times over.



## 14. Memory, preprocessing and advice

### 14.1 Memory

Everything resident during the online phase (`python3 experiments/lowm.py memory`; words of 32 bytes; the lists are the 262 distinct ones):

| item | bytes |
|---|---|
| planes of the reps: 4,442 batches of 256 reps (the 262 lists) x 21 planes | 2,985,024 |
| packed entries of the reps: 4,442 batches x 64 words | 9,097,216 |
| cube entries D[c]: 8 words (unused: no cube) | 256 |
| spill area of the sums of a class's batches: 7 x 32 words (unused: no subtraction runs) | 7,168 |
| c7 planes: 32 words x 5 batches | 5,120 |
| chunk table LO: 4096 words | 131,072 |
| chunk table MID: 4096 words | 131,072 |
| lane-scan table: 2048 words | 65,536 |
| class descriptors: 1,067 x 4 words (base, BP, list data, c7) | 136,576 |
| per-l constants: 44 x 4 words (C_l, cxA_l, E15x word, VA_l) | 5,632 |
| scalar planes in memory: 100 words | 3,200 |
| characteristic cells, L* rows, S: bound 1280 words | 40,960 |
| chaining-value constants (cv_pre) and the first-block buffer: 64 words | 2,048 |
| code (bound: at most 8192 primitives of at most 8 bytes) | 65,536 |
| **total** | **12,676,416 = 2^23.60** |

The claimed memory is 2^33 bytes, the declared bound H6 over all phases and development runs (Appendix H.2): the construction of the characteristic (generator, translation, STP dump, kissat) and of S (CNF generation, kissat), the scans of the preprocessing and the online phase. The phases ran under address-space caps of at most 2^29 bytes (`prlimit --as`), the largest measured peak being the STP CNF dump, 500,424,704 bytes (2^28.899); the online tables are 2^23.60 and the preprocessing peak is `grp.c` at 344,284 KB (2^28.4). peak = max(online, preprocessing phases, construction of S, construction of the characteristic) <= 2^29 (Appendix H.2). The messages (128 bytes), the registers (64 x 32 bytes) and the compression state are included in the last constants. Nonuniform advice: the cells of rows 16..24 (Section 3.5), below 2^13 bytes.
The tables are built in the preprocessing from the output of `grp.c` and `lscan.c` and are never held twice.

### 14.2 Preprocessing: PRE = 90 CPU-seconds

(i) The family and its tables are computed from S by the programs of Appendix G, measured on the cloud machine (`gscan`, `grp`, `lscan` under `prlimit --as=536870912`): `gscan.c` 0.46 s user + 0.03 s system (1,912 KB; G, 21,935,501 variants, written as a file of 87.7 MB); `grp.c` 1.32 s + 0.15 s (344,284 KB; the classes by c7 value and the file of the 1,067 classes of at least 3,456 variants); `lscan.c` 66.61 s + 0.05 s (132,988 KB; L and L*); `stats.c` 6.86 s (1,656 KB; |F6|, |F7|, the 2,893,824 pairs of row 16, the filter statistics). Together 75.48 CPU-seconds.
(ii) The lists: from the members of each class, base = AND, mask = OR minus AND, s = member xor base: 4,378,186 x about 30 operations < 2^27. (iii) The planes and packed entries: 4,442 batches x (21 x 256 bit insertions x 3 + 64 x 4 x 10) < 2^27. (iv) The tables LO and MID: 44 x (4096 x 10 + 2 x 4096 x 6) < 2^23, the per-l constants 44 x 200; the scan table 2048 x 6; the c7 planes 1,067 x 32 x 3. Together fewer than 2^29 word operations (0.2 CPU-seconds at the price of Section 11.2).
PRE = 90 CPU-seconds is charged (the measured 75.48 plus a margin for (ii)-(iv) and for the repeat of a scan). Nothing depends on cb or on any other word of the chaining value.

## 15. Scope of the evidence

- H1, H2 and H3 are our theory for the attack at its scale (2^51.7 first blocks). Their evidence is in Sections 12 and 13 and Appendices F and H.4; Appendix H.5 gives the effect of changing each.
- The counted program is a straight-line text whose plane programs are counted by an algebra with static constants and inversion flags; the scalar and control items are counted by the constants of Section 9. The register argument of Section 9.5 counts live planes.
- Section 13.3 runs about 3 x 10^4 first blocks; the ledger uses the exact expectations.
- The organizer experiments load the outputs of the construction as one data bundle (sha256 of every part in Appendix G) and `lowm.py` derives the classes it uses from them (Lemma 5.3); `a0-online-r37` processes at most the first three passing classes of a first block and `a0-sfs-r37` builds at most as many pairs as its shared proposal budget of 2^20 allows.
- H3 (b) is measured at the row-16 level (7319bba, published pair) with rho <= 2^35; delta <= 2^-7.55 against 2^-7.5 (Section 10, Appendix H.4).
- The cells of rows 16..24 are the advice of Section 3.5.

## Appendix A. Row 16: the exact counts

`stats.c` (Appendix G.5), compiled with `gcc -O2` and run on the constants of the exact test of Lemma 6.2 (`dump_r16cfg.py` writes `r16cfg.txt` from `experiments/lowm.py`: the per-l constants C_l, cxA_l, E15x, VA_l and the E16 mask and value), loops over the 2^24 values of E16x with the eight fixed bits for each l, counts those that pass the exact test, and then counts, over the 2^24 values of u mod 2^24, the l that satisfy the eight conditions of the table stage. Output (6.86 s, 1,656 KB):

```text
F6 287309824 F7 68157440
l 0 r16 65536
l 1 r16 65536
l 2 r16 65536
l 3 r16 65536
l 4 r16 65536
l 5 r16 65536
l 6 r16 65536
l 7 r16 65536
l 8 r16 65536
l 9 r16 65536
l 10 r16 65536
l 11 r16 65536
l 12 r16 65536
l 13 r16 65536
l 14 r16 65536
l 15 r16 65536
l 16 r16 65536
l 17 r16 65536
l 18 r16 65536
l 19 r16 65536
l 20 r16 65536
l 21 r16 65536
l 22 r16 65536
l 23 r16 65536
l 24 r16 65536
l 25 r16 69632
l 26 r16 65536
l 27 r16 65536
l 28 r16 65536
l 29 r16 67584
l 30 r16 65536
l 31 r16 65536
l 32 r16 65536
l 33 r16 65536
l 34 r16 65536
l 35 r16 65536
l 36 r16 65536
l 37 r16 65536
l 38 r16 65536
l 39 r16 65536
l 40 r16 65536
l 41 r16 65536
l 42 r16 69632
l 43 r16 65536
R16 2893824
PNZ 2517128 TOT 2883584 (mean 0.171875, NL/256 = 0.171875)
```
The estimator `smc_s4.c` (Appendix F) enumerates the same set with its own generic cell machinery (`rowx`, `rowy` of the cells of rows 16: the E and A cells, the `+` link and the printed conditions) and prints `NPAIR 2893824` and the per-l counts `65536 ... 69632 (l = 25) ... 67584 (l = 29) ... 69632 (l = 42)`, the counts above. The sum of |filt| over the 2^24 values of u mod 2^24 is 2,883,584 = 44 x 2^16 (mean 0.171875 = 44/256) and filt(u) != 0 for 2,517,128 of them: the ledger constants R16F = 2,893,824/2^32, MU = 44/256, PNZ = 2,517,128/2^24.

## Appendix B. The exact ledger

Self-contained (integers and Fractions); the stage prices are the constants of Section 9, asserted by `lowm.py`. It reproduces `python3 experiments/lowm.py ledger`.

```python
from fractions import Fraction as Fr
import math
# Exact ledger of the counted program (proof.md Sections 9-11). Integers and Fractions only.
C = 2644                                   # reference cost of one target compression, in word operations
# stage prices (primitives of the straight-line text, proof.md Section 9; the plane-program counts are measured by lowm.py and asserted at every execution)
W6_OPS = 446                               # W6 program of a batch of 256 reps (no cube: one run per class)
F7_OPS, SCAN_FIX, SCAN_LANE, CLS_LANE = 166, 70, 8, 6
EXTR, PLACE, GROUP_BODY, PAD_OPS, PROBE = (1, 2, 2, 1), 7, 31, 7, (11, 12, 12, 12)
SURV_FIX, SURV_LANE, EX_OPS, RARE_LOOKUP, RECOMP, ROWCHECK, ROWCOMP = 11, 7, 34, 2, 35, 53, 106
CPREP, CF_CLASS, SWEEP_OVH, FIXED = 410, 6, 203, 2223
SP_LOADS = 44                              # per batch: stored planes of the reps (21) with their address adds, two pointers
# the 1067 classes: (variants, classes) (proof.md Section 5.3)
CLASS_TYPES = [(3456, 73), (3472, 14), (3516, 10), (3520, 2), (3548, 9), (3552, 2), (3584, 192), (3600, 9), (3760, 4), (3790, 4), (3808, 3), (3840, 140), (3900, 4), (3936, 132),
               (3940, 4), (3968, 64), (4000, 4), (4016, 64), (4032, 49), (4080, 2), (4180, 2), (4216, 1), (4266, 1), (4288, 4), (4320, 18), (4400, 4), (4416, 2), (4424, 18),
               (4464, 9), (4480, 14), (4512, 4), (4516, 9), (4548, 4), (4608, 36), (4728, 12), (4800, 20), (4920, 8), (4960, 4), (5020, 4), (5376, 36), (5760, 24), (5904, 24),
               (5952, 12), (6024, 12)]
NCLS = sum(c for n, c in CLASS_TYPES); NVAR = sum(n * c for n, c in CLASS_TYPES); NFEAS = 44
P7 = Fr(68157440, 1 << 32); P6 = Fr(287309824, 1 << 32); R16F = Fr(2893824, 1 << 32); MU = Fr(NFEAS, 256); PNZ = Fr(2517128, 1 << 24)
# fixed charges (Sections 11.2, 13.4, 14.2) and the success-floor constants
PRICE = 2 ** 21.427                              # units per solver CPU-second (6eeefb64)
A_C = int((8 * 4044 + 29.45) * PRICE)            # 32,381.45 CPU-seconds (Appendix L)
A_S = int((2 * 2188.09 + 0.37) * PRICE)          # 4,376.55 CPU-seconds (Section 11.2)
DEV = 1 << 42; FIN = 1600
PRE = int(90.0 * PRICE * C)                      # 90 CPU-seconds of preprocessing, in word operations (Section 14.2)
Q3_LOG2 = -70.34
fl = math.floor(Q3_LOG2); Q3 = Fr(2) ** fl * Fr(math.floor(2 ** (Q3_LOG2 - fl) * 2 ** 40), 2 ** 40)      # q3 = 2^-70.34 rounded down to a 40-bit mantissa
DISC = Fr(17, 2)                                 # the H3 discount is 1 - 2^-DISC (delta = 2^-7.5)
SLACK = Fr(1, 4096)
def lane_costs(nls): return sum(SCAN_LANE + EXTR[L // 64] for nl in nls for L in range(nl))   # scan and extraction of every lane of the batches of reps
def class_det(n, k=0, Q0=0):
    # operations of a passing class that do not depend on which reps are good (one run)
    nb = (n + 255) // 256; nsw = (nb + 1) // 2; part = 1 if n % 256 else 0
    return CPREP + CF_CLASS + nsw * SWEEP_OVH + nb * (SP_LOADS + W6_OPS + SCAN_FIX) + part
def class_run_cost(n, k=0, Q0=0):
    # scan, extraction and placement of the members if all reps are good (times p6 for the expectation)
    nls = [min(256, n - 256 * b) for b in range((n + 255) // 256)]
    return lane_costs(nls) + n * PLACE
perclass = pairs = Fr(0); vmax = Fr(0)
c3b_row = ROWCOMP + ROWCHECK + 1; c3b_pair = 201 + RECOMP + 1 + RARE_LOOKUP; c3b_l = 2 + 6 + 2 * c3b_row
for n, cnt in CLASS_TYPES:
    perclass += cnt * P7 * (class_det(n) + P6 * class_run_cost(n)); pairs += cnt * P7 * P6 * n; vmax += cnt * (class_det(n) + class_run_cost(n))
ct_var = CLS_LANE * NCLS * P7
groups = (pairs + 3) / 4; lanes = 4 * groups
grp = groups * (GROUP_BODY + sum(PROBE)) + PAD_OPS
surv = lanes * (PNZ * SURV_FIX + MU * (SURV_LANE + EX_OPS))
rare = lanes * R16F * (c3b_pair + c3b_l + 19 * Fr(1, 512) * c3b_row)
vbar = ct_var + perclass + grp + surv + rare            # expected data-dependent operations per first block
g = pairs                                               # expected good pairs per first block
vlanes = NVAR + 3                                       # one first block's maximal data-dependent work: all classes pass, all variants good, every l survives, every probe hits
vmax_fb = vmax + Fr(vlanes, 4) * (GROUP_BODY + sum(PROBE)) + PAD_OPS + vlanes * (SURV_FIX + NFEAS * (SURV_LANE + EX_OPS)) \
          + vlanes * Fr(11, 10) * (c3b_pair + NFEAS * (c3b_l + 19 * c3b_row)) + 24 + CLS_LANE * NCLS
from decimal import Decimal, getcontext
getcontext().prec = 60
def mu_req(pcap):
    x = Decimal('0.61') - Decimal(pcap.numerator) / Decimal(pcap.denominator) - Decimal(2) ** -60
    return Fr(int(math.floor(-x.ln() / (Decimal(1) - (-(Decimal(17) / 2) * Decimal(2).ln()).exp()) * 10 ** 8)) + 1, 10 ** 8)
pa = Fr(1, 1 << 24)                                     # the assumed Chebyshev bound is iterated to a fixed point
for _ in range(8):
    MU0 = mu_req(pa); NFB = int(-(-MU0 // (g * NFEAS * Q3))); PCAP = vmax_fb / (SLACK * SLACK * NFB * vbar); pa2 = Fr(math.ceil(PCAP * 10 ** 8), 10 ** 8)
    if pa2 == pa: break
    pa = pa2
PCAP_ASSUMED = pa
assert PCAP <= PCAP_ASSUMED
V_MAX = int(-(-(1 + SLACK) * NFB * vbar // 1))          # cap on the counted data-dependent operations
ROWS = [("A_C: characteristic search (units x C)", A_C * C), ("A_S: Step-1 solve (units x C)", A_S * C), ("DEV: development (units x C)", DEV * C),
        ("N_FB first-block compressions (units x C)", NFB * C), ("fixed operations: N_FB x FIXED", NFB * FIXED), ("V_MAX: data-dependent operations", V_MAX),
        ("overshoot past the cap: vmax_fb", -(-vmax_fb // 1)), ("PRE: preprocessing", PRE), ("FIN: final verification", FIN), ("6 further compressions (units x C)", 6 * C)]
ROWS = [(a, int(b)) for a, b in ROWS]
N = sum(b for _, b in ROWS)
P = 100000
a = (N ** P // C ** P).bit_length() - 1
while (1 << (a + 1)) * C ** P <= N ** P: a += 1
while (1 << a) * C ** P > N ** P: a -= 1
claim = Fr(-(-(a + 1) * 10 ** 5 // P), 10 ** 5)
w = max(len(k) for k, _ in ROWS)
for k, v in ROWS: print(k.ljust(w), format(v, ","))
print("N_FB = %d, g = %s, vbar = %s, Pcap = %s <= %s" % (NFB, float(g), float(vbar), float(PCAP), float(PCAP_ASSUMED)))
print("N = %d" % N)
print("certificate: 2^%d * %d^%d <= N^%d < 2^%d * %d^%d" % (a, C, P, P, a + 1, C, P))
print("time_log2 = %.5f" % float(claim))
```

Output:

```text
A_C: characteristic search (units x C)    241,394,549,538,064
A_S: Step-1 solve (units x C)             32,625,942,189,556
DEV: development (units x C)              11,628,434,975,358,976
N_FB first-block compressions (units x C) 9,837,048,501,976,112,420
fixed operations: N_FB x FIXED            8,270,710,597,538,917,515
V_MAX: data-dependent operations          1,489,165,979,804,742,916,402
overshoot past the cap: vmax_fb           722,960,904,448
PRE: preprocessing                        670,924,540,390
FIN: final verification                   1,600
6 further compressions (units x C)        15,864
N_FB = 3720517587736805, g = 4647.701541185379, vbar = 400160.049649675, Pcap = 0.008146998162639175 <= 0.008147
N = 1507285642753610495235
certificate: 2^5898393 * 2644^100000 <= N^100000 < 2^5898394 * 2644^100000
time_log2 = 58.98394
```

## Appendix C. The success floor

```python
from decimal import Decimal, getcontext
getcontext().prec = 60
PCAP = Decimal(8147) / Decimal(1000000)           # the assumed bound of the Chebyshev work-cap failure probability (Appendix B asserts the computed bound is below it)
EPS = Decimal(2) ** -60                          # a repeated first block among N_FB draws
D = 1 - Decimal(2) ** Decimal('-8.5')            # the H3 discount 1 - 2^-8.5
req = -(Decimal('0.61') - PCAP - EPS).ln() / D   # mu0 must exceed this
MU0 = Decimal(50914839) / Decimal(10 ** 8)
assert req < MU0 <= req + Decimal(2) / Decimal(10 ** 8)
succ = 1 - (-D * MU0).exp() - PCAP - EPS
print('required %.12f, mu0 %.8f, success bound %.12f' % (req, MU0, succ))
assert succ > Decimal('0.39')
print('OK')
```

Output:

```text
required 0.509148386557, mu0 0.50914839, success bound 0.390000002067
OK
```

## Appendix D. `selftest` and `family` output

```text
sample classes 8, variants 33104, mismatches 0
W6_OPS (k, full): {(0, False): 446, (0, True): 457} SUBF_OPS: {} F7_OPS 166 FIXED 2223
F7 sampler violations 0
invariance of W6x under the flips of the bits of I: 3840 checks, 0 mismatches
w6 plane lanes 198624, F6 passes 14912, mismatches 0
class-test lanes 213400, mismatches 0
row-16 checks: members seen 26, mismatches 0
packed u lanes 400, mismatches 0
max S0 over the family variants 0xffff1068 True
classes 1067 variants 4378186 hist ok True masks 1fbad9bb 18a898bb True max S0 0xffffff05 True
```

## Appendix E. Credits

Authors of the work this filing builds on are named in Section 2 and in the dependency list. The paper: Y. Li, Z. Zhang, M. Li, F. Liu, H. Qian, J. Zhu. This filing: Jbenisek with Claude Sonnet 5.5 and Claude Opus 5.5 (Claude Code), which built, ran and checked the program, the construction programs of Appendix G and the q3 estimator `smc_s4.c` and wrote this text; Grok (xAI) wrote the generator `dense_sat.py` of the pair instance (Appendix G.8) and pointed to the memory-efficient mode of the paper as the lead; GPT Luna priced the memory trade of the table package that the predecessor replaced and, with Claude, built the verified 37-step solver model (Bitwuzla, Z3) behind ffbe30bb's enumeration of the four patterns. ffbe30bb-ac92-4191-a589-3bf32661ee7d (Jbenisek): the four-pattern acceptance of rows 18 and 19, its enumeration and the three collisions of Section 7.6. None of the AI tools reviewed this filing; mistakes are ours.

## Appendix F. The q3 study: preregistration, results, programs

Files (cloud `/root/r37own/step2/`, local `levers_1016/r37own/step2/`): the estimator `smc_s4.c` and its constants header `lab_s4.h` (generated from the pair of Section 3.4, the cells of `lowm.py` and L* by `mk_lab.py`, which edits the header of the estimator of the earlier filing), the family file `s4_3456.cls` (the output of `grp.c`: one line per class, c7 value, size, members), `run_smc.sh` (144 runs, 12 at a time), `analyze_s4.py` (the preregistered rule). Build: `gcc -O2 -DFFBE_RELAX -DR16X smc_s4.c -lm -o smc_s4`; run: `smc_s4 SEED 8192 512 8192 s4_3456.cls 0`. The constants of the estimator are the same numbers as `lowm.py` embeds: S, L* (44), D6..T8, the cells.

### F.1 Preregistration (`PREREG_s4.md`, sha256 51c64a8358b21b9579d474340a77fdc31f32bbc7ab31e183846aa00b67a81300, written before any listed seed ran)

```text
# PREREG q3 (exact end event), seed-4 family. Written 2026-10-16 20:35Z (14:35 MDT) before any counted run.
Smoke runs already done and disclosed (not counted): seeds 1 (NP 2048/256/2048 and NP 256/64/256), and pub-equivalence seed 9201 (smc_pub reproduces r37exact/raw/out_r16x_9201.txt bit for bit).
Program: smc_s4.c (= r37exact/smc_r16x.c with NL l-values, NPAIR/NL, and the seed-4 pair/L* in lab_s4.h), build gcc -O2 -DFFBE_RELAX -DR16X. sha256 smc_s4.c f09f4bed...edc, lab_s4.h 2af1febe...ff2 (hashes_smc.txt).
Data: S = pair of the H3_seed4 model (H3s4_seed1.out), L* = 44 elements (Ls4.Lstar f747c1c6...), family A = classes of G(S) with >= 3456 variants (s4_3456.cls: 1,067 classes, 4,378,186 variants, dd44ff81...), family B = classes with >= 4480 (s4_top223.cls: 223 classes, 1,154,692 variants).
Parameters per seed: NP 8192, M 512, MT 8192 (2^26 proposals), mode 0 (W6 in F6, W7 in F7 uniform, W8 from the family uniformly).
Sets: S1 = seeds 40001..40064 family A; S2 = seeds 50001..50064 family A; S3 (descriptive) = seeds 60001..60016 family B. At most 4 processes at a time, nice 10, one cgroup (MemoryMax 402,653,184 bytes, no swap), cloud box.
Per seed estimate Q = 2^log2est21 * exact/n (linear). The exact event = the eight registers of both members equal after step 36 (rows 22..36 replayed on raw schedule words); rows 16..21 impose the published cells with the four value patterns of rows 18/19 and R16x relaxed (as ZF6). The cell event of rows 22..36 is NOT defined for seed 4 (the published W22/W24 value cells and two-bit conditions belong to the published W9/W10 signs; diagnostic only).
Rule fixed now: per set LB = mean(Q) - t(0.99, 63) * sd(Q)/sqrt(64), t = 2.3870. Declared q3 = 2^x, x = floor(100 * log2(min(LB_S1, LB_S2)))/100. S3 is reported only. No seed dropped or rerun. Sets must agree within 2 standard errors of the difference, else report both and declare the lower.
Not claimed: that the transfer to the counted program holds beyond what pub did (family structure, cube sharing) - see STAGE2.md.
```

The smoke runs disclosed in the preregistration are part of the development computation of Section 13.4.

### F.2 Results

Per-seed estimates Q (log2, rounded to 0.001) of the 144 seeds, in seed order; none dropped, none rerun. `analyze_s4.py` output:

```text
S1 seeds 64 missing [] mean log2 -70.2581 rel sd 0.0914 se rel 0.0114 LB99 log2 -70.2979 exact total 286975 cell total 0
S2 seeds 64 missing [] mean log2 -70.2885 rel sd 0.1160 se rel 0.0145 LB99 log2 -70.3394 exact total 287460 cell total 0
S3 seeds 16 missing [] mean log2 -70.2735 rel sd 0.1160 se rel 0.0290 LB99 log2 -70.3867 exact total 71495 cell total 0
difference z 1.147  declared q3_log2 = -70.34  pooled mean log2 -70.2732
```

All 64 log2 estimates of S1:

```text
-70.245  -70.268  -70.122  -70.236  -70.131  -70.252  -70.232  -70.493  -70.437  -70.115  -70.074  -70.388  -70.081  -69.990  -70.394  -70.132
-70.273  -70.359  -70.221  -70.220  -70.289  -70.293  -69.973  -70.507  -70.287  -70.391  -70.250  -70.293  -70.379  -70.204  -70.354  -70.208
-70.403  -70.265  -70.218  -70.350  -70.308  -70.435  -70.418  -70.309  -70.365  -70.066  -70.361  -70.465  -70.183  -70.079  -70.216  -70.377
-70.072  -70.231  -70.458  -70.401  -70.464  -70.141  -70.287  -70.049  -70.087  -70.335  -70.148  -70.227  -70.194  -70.203  -70.461  -70.224
```

All 64 log2 estimates of S2:

```text
-70.311  -69.976  -70.192  -70.277  -70.398  -70.259  -70.334  -70.374  -70.035  -70.319  -70.167  -70.163  -70.248  -70.046  -70.317  -70.528
-70.236  -70.431  -70.168  -70.089  -70.348  -70.017  -70.214  -70.111  -70.692  -70.109  -70.248  -70.357  -70.251  -70.376  -70.339  -70.315
-70.562  -70.011  -70.580  -70.440  -70.219  -70.559  -70.425  -70.320  -70.201  -70.512  -70.239  -70.328  -70.389  -70.121  -70.619  -70.237
-70.059  -70.305  -70.498  -70.009  -70.205  -70.580  -70.047  -70.504  -70.244  -70.367  -70.376  -70.318  -70.439  -70.507  -70.246  -70.371
```

All 16 log2 estimates of S3:

```text
-70.245  -70.419  -70.190  -70.241  -70.241  -70.305  -70.401  -70.267  -70.543  -70.345  -70.315  -69.833  -70.316  -70.421  -70.135  -70.290
```

### F.3 `smc_s4.c`

```c
/* smc.c - sequential Monte-Carlo estimator of q3 (37-step SHA-256 second block, rows 16..36), variant-W8 tail.
   usage: smc seed NP M MT classes.txt      |      smc -t classes.txt   (self tests) */
#ifdef PUBLAB
#include "lab.h"
#define NL 32
#else
#include "lab_s4.h"
#endif
typedef struct { u32 Ax[NR+O],Ex[NR+O],Ay[NR+O],Ey[NR+O],Wx[NR],Wy[NR]; int l; } P;
#define AX(q,i) ((q)->Ax[(i)+O])
#define EX(q,i) ((q)->Ex[(i)+O])
#define AY(q,i) ((q)->Ay[(i)+O])
#define EY(q,i) ((q)->Ey[(i)+O])
static int x2row[NR][NX2], nx2row[NR];
static u32 xval(const P*q,int k,int i,int b){u32 v= k==0?AX(q,i):k==1?EX(q,i):q->Wx[i];return (v>>b)&1;}
static int x2ok(const P*q,int t){for(int c=0;c<nx2row[t];c++){const X2C*x=&X2[x2row[t][c]];
  if((int)(xval(q,x->k1,x->i1,x->b1)==xval(q,x->k2,x->i2,x->b2))!=x->op)return 0;}return 1;}
/* x member of row t. haveW: val is W_t^x, else val is E_t^x. returns 1 iff every x-side cell and printed two-bit condition of row t holds */
static inline int rowx(P*q,int t,int haveW,u32 val){
  u32 rest=AX(q,t-4)+EX(q,t-4)+S1(EX(q,t-1))+CH(EX(q,t-1),EX(q,t-2),EX(q,t-3))+KC[t];
  u32 e,W; if(haveW){W=val;e=rest+W;}else{e=val;W=e-rest;}
  u32 a=e-AX(q,t-4)+S0(AX(q,t-1))+MAJ(AX(q,t-1),AX(q,t-2),AX(q,t-3));
  EX(q,t)=e;AX(q,t)=a;q->Wx[t]=W;
  const Cell*ca=&CELL[0][t],*ce=&CELL[1][t],*cw=&CELL[2][t];
  if((e&ce->m)!=ce->v||(a&ca->m)!=ca->v||(W&cw->m)!=cw->v)return 0;
  u32 pq=ce->p&CELL[1][t-1].p; if((e^EX(q,t-1))&pq)return 0;
  return x2ok(q,t);}
/* y member; mode 0: W^y = W^x + exact difference (E-driven rows 16..21), 1: message schedule on y words, 2: stored W^y */
static inline int rowy(P*q,int t,int mode){
  u32 W;
  if(mode==0){ W=q->Wx[t]+(s1(q->Wy[t-2])-s1(q->Wx[t-2]))+(q->Wy[t-7]-q->Wx[t-7])+(t==21?T6:0u); q->Wy[t]=W; }
  else if(mode==1){ W=s1(q->Wy[t-2])+q->Wy[t-7]+s0(q->Wy[t-15])+q->Wy[t-16]; q->Wy[t]=W; }
  else W=q->Wy[t];
  u32 e=AY(q,t-4)+EY(q,t-4)+S1(EY(q,t-1))+CH(EY(q,t-1),EY(q,t-2),EY(q,t-3))+KC[t]+W;
  u32 a=e-AY(q,t-4)+S0(AY(q,t-1))+MAJ(AY(q,t-1),AY(q,t-2),AY(q,t-3));
  EY(q,t)=e;AY(q,t)=a;
  return ((EX(q,t)^e)==CELL[1][t].d)&&((AX(q,t)^a)==CELL[0][t].d)&&((q->Wx[t]^W)==CELL[2][t].d);}
static void setup_l(P*q,int l){
  memset(q,0,sizeof*q);q->l=l;
  AX(q,-1)=CV0[0];AX(q,-2)=CV0[1];AX(q,-3)=CV0[2];AX(q,-4)=CV0[3];EX(q,-1)=CV0[4];EX(q,-2)=CV0[5];EX(q,-3)=CV0[6];EX(q,-4)=CV0[7];
  AY(q,-1)=CV0[0];AY(q,-2)=CV0[1];AY(q,-3)=CV0[2];AY(q,-4)=CV0[3];EY(q,-1)=CV0[4];EY(q,-2)=CV0[5];EY(q,-3)=CV0[6];EY(q,-4)=CV0[7];
  for(int i=0;i<14;i++){q->Wx[i]=MX[i];q->Wy[i]=MY[i];}
  q->Wx[14]=W14X;q->Wx[15]=LW15[l];q->Wy[14]=W14X^W14DX;q->Wy[15]=LW15[l]^W15DX;
  for(int t=0;t<16;t++){
    u32 e=AX(q,t-4)+EX(q,t-4)+S1(EX(q,t-1))+CH(EX(q,t-1),EX(q,t-2),EX(q,t-3))+KC[t]+q->Wx[t];
    EX(q,t)=e;AX(q,t)=e-AX(q,t-4)+S0(AX(q,t-1))+MAJ(AX(q,t-1),AX(q,t-2),AX(q,t-3));
    e=AY(q,t-4)+EY(q,t-4)+S1(EY(q,t-1))+CH(EY(q,t-1),EY(q,t-2),EY(q,t-3))+KC[t]+q->Wy[t];
    EY(q,t)=e;AY(q,t)=e-AY(q,t-4)+S0(AY(q,t-1))+MAJ(AY(q,t-1),AY(q,t-2),AY(q,t-3));}}
/* F6/F7 samplers */
static u32 samp6(Rng*r){for(;;){u32 w=r32(r);if(inF6(w))return w;}}
#define BIT(w,b) (((w)>>(b))&1u)
#define SETB(w,b,v) ((w)=((w)&~(1u<<(b)))|((u32)(v)<<(b)))
static u32 samp7(Rng*r){
  u64 pick=rbelow(r,(1ull<<26)+(1ull<<20)); u32 w=r32(r);
  if(pick<(1ull<<26)){ SETB(w,11,0);SETB(w,22,1);SETB(w,26,1); SETB(w,18,BIT(w,1));SETB(w,28,BIT(w,0));SETB(w,30,BIT(w,9)); }
  else { SETB(w,11,1);SETB(w,12,0);SETB(w,22,0);SETB(w,23,1);SETB(w,26,0);SETB(w,27,1);
    SETB(w,18,BIT(w,1));SETB(w,19,BIT(w,2));SETB(w,28,BIT(w,0));SETB(w,29,BIT(w,1));SETB(w,30,BIT(w,9));SETB(w,31,BIT(w,10)); }
  return w;}
/* stage application (shared by proposal and reconstruction). t in 17..21: a=E_t^x. t==22: a=W6, b=W7. */
static inline int apply_stage(P*q,int t,u32 a,u32 b){
  if(t<=21){ if(!rowx(q,t,0,a))return 0; return rowy(q,t,0); }
  q->Wx[6]=a;q->Wy[6]=a+D6;q->Wx[7]=b;q->Wy[7]=b+D7;
  u32 W=s1(q->Wx[20])+q->Wx[15]+s0(q->Wx[7])+q->Wx[6];
  if(!rowx(q,22,1,W))return 0; return rowy(q,22,1);}
static int tail_eval(P*q){for(int t=23;t<NR;t++){
  u32 W=s1(q->Wx[t-2])+q->Wx[t-7]+s0(q->Wx[t-15])+q->Wx[t-16];
  if(!rowx(q,t,1,W))return 0; if(!rowy(q,t,1))return 0;}return 1;}
static u32 *VAR; static long NVAR; static u32 W8C,C4P;
static int load_variants(const char*path){
  FILE*f=fopen(path,"r");if(!f)return -1; long cap=1<<20;VAR=malloc(cap*4);NVAR=0;char*line=NULL;size_t lc=0;
  P q; setup_l(&q,13); /* rows 0..8 from the published pair */
  u32 A4=AX(&q,4),A3=AX(&q,3),A2=AX(&q,2),A1=AX(&q,1),E8=EX(&q,8),E7=EX(&q,7),E6=EX(&q,6),E5=EX(&q,5);
  C4P=A4-S0(A3)-MAJ(A3,A2,A1); W8C=E8-A4-S1(E7)-CH(E7,E6,E5)-KC[8];
  if((u32)(W8C-(AX(&q,0)+C4P))!=MX[8]){fprintf(stderr,"W8 constant self-check failed\n");return -2;}
  while(getline(&line,&lc,f)>0){char*tok=strtok(line," \n");if(!tok)continue;tok=strtok(NULL," \n");long n=atol(tok);
    for(long i=0;i<n;i++){tok=strtok(NULL," \n");u32 a0=(u32)strtoul(tok,NULL,16);if(NVAR==cap){cap*=2;VAR=realloc(VAR,cap*4);}VAR[NVAR++]=W8C-(a0+C4P);}}
  fclose(f);free(line);return 0;}
static P* P0; /* P0[l] */
static u32 *pairE; static unsigned char *pairL; static long NPAIR;
static void build_r16(void){
  P0=malloc(NL*sizeof(P)); long cap=1<<21; pairE=malloc(cap*4); pairL=malloc(cap); NPAIR=0;
  u32 M16=CELL[1][16].m,V16=CELL[1][16].v,fr=~M16;
  for(int l=0;l<NL;l++){ setup_l(&P0[l],l); P s=P0[l];
    u32 sub=0; do{ u32 e=sub|V16;
      if(rowx(&s,16,0,e)&&rowy(&s,16,0)){ if(NPAIR==cap){cap*=2;pairE=realloc(pairE,cap*4);pairL=realloc(pairL,cap);} pairE[NPAIR]=e;pairL[NPAIR]=l;NPAIR++; }
      sub=(sub-fr)&fr; }while(sub);}
}
static void init_all(void){
  init_cells();
#ifdef FFBE_RELAX
  /* ffbe30bb's only characteristic change: remove the eight E18/E19 value
     masks; retain every signed-difference and X2 test.  The bit positions are
     the published LSB indices, matching the ffbe proof and its four-pattern
     SMC.  This is a compile-time research variant; the ordinary control build
     is unchanged. */
  { const u32 e18 = (1u<<1)|(1u<<5)|(1u<<10)|(1u<<11)|(1u<<18)|(1u<<28)|(1u<<29);
    const u32 e19 = (1u<<29);
    CELL[1][18].m &= ~e18; CELL[1][18].v &= ~e18;
    CELL[1][19].m &= ~e19; CELL[1][19].v &= ~e19; }
#endif
#ifdef R16X
  /* R16x: no E16[23]=0 value, no '+' of E17 bit 24, no condition E16[24]=E17[24] (X2 entry {1,16,24,1,1,17,24}) */
  CELL[1][16].m &= ~(1u<<23); CELL[1][16].v &= ~(1u<<23);
  CELL[1][17].p &= ~(1u<<24);
#endif
  const char*all[]={0};(void)all;
  for(unsigned i=0;i<sizeof CHA/sizeof*CHA;i++)if(strlen(CHA[i].s)!=32)exit(90);
  for(unsigned i=0;i<sizeof CHE/sizeof*CHE;i++)if(strlen(CHE[i].s)!=32)exit(91);
  for(unsigned i=0;i<sizeof CHW/sizeof*CHW;i++)if(strlen(CHW[i].s)!=32)exit(92);
  memset(nx2row,0,sizeof nx2row);
  for(int c=0;c<NX2;c++){int r=X2[c].i1>X2[c].i2?X2[c].i1:X2[c].i2;
#ifdef R16X
    if(X2[c].k1==1&&X2[c].i1==16&&X2[c].b1==24&&X2[c].k2==1&&X2[c].i2==17&&X2[c].b2==24)continue;
#endif
    x2row[r][nx2row[r]++]=c;}
}
typedef struct { u32 pi,a,b; } Rec;
static int selftest(const char*cls){
  init_all(); int bad=0;
  /* published pair rows 4..15 for all l: cells and printed two-bit conditions (rows < 16 only) */
  for(int l=0;l<32;l++){P q;setup_l(&q,l);P c=q;
    for(int t=4;t<16;t++){ if(!rowx(&c,t,1,q.Wx[t])||!rowy(&c,t,2)){printf("row %d fails for l=%d\n",t,l);bad++;break;} } }
  printf("published/L* rows 4..15 check done, bad=%d\n",bad);
  build_r16(); printf("row16 pairs %ld (expected 1052672)\n",NPAIR); if(NPAIR!=1052672)bad++;
  long cnt[32]={0};for(long i=0;i<NPAIR;i++)cnt[pairL[i]]++; for(int l=0;l<32;l++)printf("%ld ",cnt[l]);printf("\n");
  Rng r;rseed(&r,12345); long b6=0,b7=0; for(int i=0;i<2000000;i++){if(!inF6(samp6(&r)))b6++; if(!inF7(samp7(&r)))b7++;}
  printf("F6/F7 sampler violations %ld %ld\n",b6,b7); bad+=b6+b7;
  /* F7 decomposition: scan random words; every member must be in the decomposition and density must match */
  { long inF=0,notdec=0,N=200000000; for(long i=0;i<N;i++){u32 w=r32(&r); if(inF7(w)){inF++;
      int d1=!BIT(w,11)&&BIT(w,22)&&BIT(w,26)&&BIT(w,1)==BIT(w,18)&&BIT(w,0)==BIT(w,28)&&BIT(w,9)==BIT(w,30);
      int d2=BIT(w,11)&&!BIT(w,12)&&!BIT(w,22)&&BIT(w,23)&&!BIT(w,26)&&BIT(w,27)&&BIT(w,1)==BIT(w,18)&&BIT(w,2)==BIT(w,19)&&BIT(w,0)==BIT(w,28)&&BIT(w,1)==BIT(w,29)&&BIT(w,9)==BIT(w,30)&&BIT(w,10)==BIT(w,31);
      if(!d1&&!d2)notdec++; }}
    printf("F7 random scan: %ld hits of %ld (expected %.0f), outside decomposition %ld\n",inF,N,N*(67108864.0+1048576.0)/4294967296.0,notdec); if(notdec)bad++; }
  if(load_variants(cls)){printf("variant load failed\n");return 1;}
  long v1=0,v2=0; for(long i=0;i<NVAR;i++){u32 w=VAR[i]; if((u32)(s0(w+D8)-s0(w))!=T8)v1++; const Cell*cw=&CELL[2][8]; if((w&cw->m)!=cw->v)v2++;
    if(BIT(w,1)==BIT(w,12)||BIT(w,8)==BIT(w,25)||BIT(w,14)!=BIT(w,18))v2++;}
  printf("variants %ld; T8 violations %ld; W8 cell/2-bit violations %ld\n",NVAR,v1,v2); bad+=v1+v2;
  printf("selftest %s\n",bad?"FAILED":"ok"); return bad!=0;}
static u32 samp7m(Rng*r,int mode){ if(!mode)return samp7(r); for(;;){u32 w=samp7(r); int br=((w>>11)&1); if(mode==1&&!br)return w; if(mode==2&&br)return w; if(mode==3&&(w&1))return w; if(mode==4&&!(w&1))return w;} }
static int MODE=0;
/* exact end event: rows 22..36 replayed on raw schedule words, no cells; collision <=> all 8 registers equal after step 36 (same cv, feed-forward cancels) */
static int exact_coll(P*q,u32 w6,u32 w7,u32 w8){
  u32 Wx[NR],Wy[NR]; for(int t=0;t<22;t++){Wx[t]=q->Wx[t];Wy[t]=q->Wy[t];}
  Wx[6]=w6;Wy[6]=w6+D6;Wx[7]=w7;Wy[7]=w7+D7;Wx[8]=w8;Wy[8]=w8+D8;
  for(int t=22;t<NR;t++){Wx[t]=s1(Wx[t-2])+Wx[t-7]+s0(Wx[t-15])+Wx[t-16];Wy[t]=s1(Wy[t-2])+Wy[t-7]+s0(Wy[t-15])+Wy[t-16];}
  u32 ax[NR+O],ex[NR+O],ay[NR+O],ey[NR+O];
  for(int i=-4;i<=21;i++){ax[i+O]=AX(q,i);ex[i+O]=EX(q,i);ay[i+O]=AY(q,i);ey[i+O]=EY(q,i);}
  for(int t=22;t<NR;t++){
    u32 e=ax[t-4+O]+ex[t-4+O]+S1(ex[t-1+O])+CH(ex[t-1+O],ex[t-2+O],ex[t-3+O])+KC[t]+Wx[t];
    ex[t+O]=e;ax[t+O]=e-ax[t-4+O]+S0(ax[t-1+O])+MAJ(ax[t-1+O],ax[t-2+O],ax[t-3+O]);
    e=ay[t-4+O]+ey[t-4+O]+S1(ey[t-1+O])+CH(ey[t-1+O],ey[t-2+O],ey[t-3+O])+KC[t]+Wy[t];
    ey[t+O]=e;ay[t+O]=e-ay[t-4+O]+S0(ay[t-1+O])+MAJ(ay[t-1+O],ay[t-2+O],ay[t-3+O]);}
  for(int t=33;t<NR;t++) if(ax[t+O]!=ay[t+O]||ex[t+O]!=ey[t+O]) return 0;
  return 1;}

/* row-21 exact: E21 arbitrary (no cell, no exact-diff filter on row 21); W21x derived from E21, W21y from the real schedule difference */
static int exact_coll21(P*q,u32 e21,u32 w6,u32 w7,u32 w8){
  u32 Wx[NR],Wy[NR]; for(int t=0;t<21;t++){Wx[t]=q->Wx[t];Wy[t]=q->Wy[t];}
  u32 ax[NR+O],ex[NR+O],ay[NR+O],ey[NR+O];
  for(int i=-4;i<=20;i++){ax[i+O]=AX(q,i);ex[i+O]=EX(q,i);ay[i+O]=AY(q,i);ey[i+O]=EY(q,i);}
  u32 rest=ax[17+O]+ex[17+O]+S1(ex[20+O])+CH(ex[20+O],ex[19+O],ex[18+O])+KC[21];
  Wx[21]=e21-rest; Wy[21]=Wx[21]+(s1(Wy[19])-s1(Wx[19]))+(Wy[14]-Wx[14])+(s0(w6+D6)-s0(w6));
  Wx[6]=w6;Wy[6]=w6+D6;Wx[7]=w7;Wy[7]=w7+D7;Wx[8]=w8;Wy[8]=w8+D8;
  for(int t=22;t<NR;t++){Wx[t]=s1(Wx[t-2])+Wx[t-7]+s0(Wx[t-15])+Wx[t-16];Wy[t]=s1(Wy[t-2])+Wy[t-7]+s0(Wy[t-15])+Wy[t-16];}
  for(int t=21;t<NR;t++){
    u32 e=ax[t-4+O]+ex[t-4+O]+S1(ex[t-1+O])+CH(ex[t-1+O],ex[t-2+O],ex[t-3+O])+KC[t]+Wx[t];
    ex[t+O]=e;ax[t+O]=e-ax[t-4+O]+S0(ax[t-1+O])+MAJ(ax[t-1+O],ax[t-2+O],ax[t-3+O]);
    e=ay[t-4+O]+ey[t-4+O]+S1(ey[t-1+O])+CH(ey[t-1+O],ey[t-2+O],ey[t-3+O])+KC[t]+Wy[t];
    ey[t+O]=e;ay[t+O]=e-ay[t-4+O]+S0(ay[t-1+O])+MAJ(ay[t-1+O],ay[t-2+O],ay[t-3+O]);}
  for(int t=33;t<NR;t++) if(ax[t+O]!=ay[t+O]||ex[t+O]!=ey[t+O]) return 0;
  return 1;}
int main(int argc,char**argv){
  if(argc<7){fprintf(stderr,"usage: smc_exact seed NP M MT2 classes.txt mode(0=w6w7 F6xF7)\n");return 2;}
  u64 seed=strtoull(argv[1],0,10); int NP=atoi(argv[2]),M=atoi(argv[3]),MT=atoi(argv[4]);
  MODE=atoi(argv[6]); init_all(); if(load_variants(argv[5])){fprintf(stderr,"variants\n");return 3;}
  build_r16(); Rng R;rseed(&R,seed);
  { long cnt[64]={0}; for(long i=0;i<NPAIR;i++)cnt[pairL[i]]++; printf("NL %d NVAR %ld NPAIR %ld PERL",NL,NVAR,NPAIR); for(int l=0;l<NL;l++)printf(" %ld",cnt[l]); printf("\n"); }
  P *pop=malloc((size_t)NP*sizeof(P)),*pop2=malloc((size_t)NP*sizeof(P)); Rec*rec=malloc((size_t)NP*M*sizeof(Rec));
  double est=(double)NPAIR/(double)NL/4294967296.0;
  printf("seed %llu NP %d M %d MT2 %d\n",(unsigned long long)seed,NP,M,MT);
  for(int i=0;i<NP;i++){long k=rbelow(&R,NPAIR);pop[i]=P0[pairL[k]];
    if(!(rowx(&pop[i],16,0,pairE[k])&&rowy(&pop[i],16,0))){fprintf(stderr,"init fail\n");return 4;}}
  int TEND=(MODE>=10)?20:21;
  for(int t=17;t<=TEND;t++){
    u32 fm=CELL[1][t].m,fv=CELL[1][t].v; double w=ldexp(1.0,-__builtin_popcount(fm)); long cnt=0;
    for(int i=0;i<NP;i++){P s=pop[i];
      for(int c=0;c<M;c++){ u32 a=(r32(&R)&~fm)|fv;
        if(apply_stage(&s,t,a,0)){rec[cnt].pi=i;rec[cnt].a=a;rec[cnt].b=0;cnt++;} } }
    est*=w*(double)cnt/((double)NP*M);
    if(!cnt){printf("dead\n");return 0;}
    for(int i=0;i<NP;i++){long k=rbelow(&R,cnt);pop2[i]=pop[rec[k].pi];
      if(!apply_stage(&pop2[i],t,rec[k].a,0)){fprintf(stderr,"resample fail\n");return 5;}}
    P*tmp=pop;pop=pop2;pop2=tmp; }
  /* joint 22+tail: proposals (W6,W7,W8); control = cell event (stage-22 cells + tail cells), test = exact collision */
  if(MODE>=10){ MODE-=10; long n=0,cell=0,ex=0,x=0;
    for(int i=0;i<NP;i++){ P s=pop[i];
      for(int j=0;j<MT;j++){ u32 e21=r32(&R),w6=samp6(&R),w7=samp7m(&R,MODE),w8=VAR[rbelow(&R,NVAR)];
        int e=exact_coll21(&s,e21,w6,w7,w8);
        s.Wx[8]=w8;s.Wy[8]=w8+D8; int c=0;
        if(apply_stage(&s,21,e21,0)&&apply_stage(&s,22,w6,w7)) c=tail_eval(&s);
        n++;cell+=c;ex+=e;x+=(c&&!e);} }
    printf("n %ld cellevent %ld exact %ld cell_not_exact %ld\n",n,cell,ex,x);
    printf("RESULT21 seed %llu log2est20 %.5f log2cell %.5f log2exact %.5f ratio %.4f\n",(unsigned long long)seed,log2(est),log2((double)cell/n),log2((double)ex/n),(double)ex/cell);
    return 0; }
  /* pair_0: tag every proposal by its particle's relaxed bits: E18x[1,5,10,11,18,28,29], E19x[29] (8-bit key k) */
  static long bn[512],bc[512],be[512],bb[512],bx[512],bpart[512];
  long n=0,cell=0,ex=0,both=0,cell_notex=0,s22=0;
  for(int i=0;i<NP;i++){ P s=pop[i];
    u32 e18=EX(&s,18),e19=EX(&s,19);
    int k=(int)(BIT(e18,1)|BIT(e18,5)<<1|BIT(e18,10)<<2|BIT(e18,11)<<3|BIT(e18,18)<<4|BIT(e18,28)<<5|BIT(e18,29)<<6|BIT(e19,29)<<7)|(int)(BIT(EX(&s,16),23)<<8);
    bpart[k]++;
    for(int j=0;j<MT;j++){ u32 w6=samp6(&R),w7=samp7m(&R,MODE),w8=VAR[rbelow(&R,NVAR)];
      int e=exact_coll(&s,w6,w7,w8);
      s.Wx[8]=w8;s.Wy[8]=w8+D8;
      int c=0; if(apply_stage(&s,22,w6,w7)){ s22++; c=tail_eval(&s); }
      n++;cell+=c;ex+=e;both+=(c&&e);cell_notex+=(c&&!e);
      bn[k]++;bc[k]+=c;be[k]+=e;bb[k]+=(c&&e);bx[k]+=(c&&!e);} }
  printf("n %ld stage22cells %ld cellevent %ld exact %ld both %ld cell_not_exact %ld\n",n,s22,cell,ex,both,cell_notex);
  printf("RESULT seed %llu log2est21 %.5f log2cell %.5f log2exact %.5f ratio %.4f\n",(unsigned long long)seed,log2(est),log2((double)cell/n),log2((double)ex/n),(double)ex/cell);
  printf("EST21 %.17g\n",est);
  for(int k=0;k<512;k++) if(bn[k]) printf("BIN %d particles %ld n %ld cell %ld exact %ld both %ld cell_not_exact %ld\n",k,bpart[k],bn[k],bc[k],be[k],bb[k],bx[k]);
  return 0;}
```

### F.4 `lab_s4.h`

```c
/* lab.h - data and SHA-256 helpers for the q3 SMC (own implementation; data from ePrint 2026/1120 tables as transcribed in 087a18c4 / own core.py) */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
typedef uint32_t u32; typedef uint64_t u64;
#define NR 37
#define O 4
static inline u32 ROR(u32 x,int n){return (x>>n)|(x<<(32-n));}
static inline u32 S0(u32 x){return ROR(x,2)^ROR(x,13)^ROR(x,22);}
static inline u32 S1(u32 x){return ROR(x,6)^ROR(x,11)^ROR(x,25);}
static inline u32 s0(u32 x){return ROR(x,7)^ROR(x,18)^(x>>3);}
static inline u32 s1(u32 x){return ROR(x,17)^ROR(x,19)^(x>>10);}
static inline u32 CH(u32 x,u32 y,u32 z){return (x&y)^(~x&z);}
static inline u32 MAJ(u32 x,u32 y,u32 z){return (x&y)^(x&z)^(y&z);}
static const u32 KC[NR]={0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,
0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,
0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,
0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,
0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354};
/* characteristic cells, MSB first; rows without entry are all '=' */
typedef struct {int row; const char*s;} CellRow;
static const CellRow CHA[]={{6,"=nu============================="},{7,"==========n====n====n======n===="},{10,"======u===========u============="},
{11,"====u=====u=========u=n====u==n="},{12,"=nu============================="},{13,"====u=========u=u=======n==u===="},
{14,"======u=n=======n==============="},{16,"==u=============================",}};
static const CellRow CHE[]={{4,"000============================="},{5,"111=0=====1==0=====01===++01===="},{6,"uuu=1011=00=10111=0111=0++1011=="},
{7,"10n=u01001n00n00010nu110unuu0001"},{8,"011=1n+1=n11u1101=001u1u1010=u=1"},{9,"1=0110+=001=1100=+110100111u=0=+"},
{10,"10n001u110101==01+u1101011=1110+"},{11,"=01un000011101=n0n0u1uu101011u1u"},{12,"01101uuuuunu010110110n1u0u0uu0n0"},
{13,"0+10n110111unn+0n101110110001001"},{14,"=+0=1000000111+=1==1n010u0=0101="},{15,"=u==01===n=011n01==u0=u=1==+===="},
{16,"=0=====+00===11=+==01=0=0==+===="},{17,"=0=====+01===u1=+==0==1===1u===="},{18,"==10===uu====0==n===111===01==1="},
{19,"==1====00====1==0==========1===="},{20,"==u====10=======1===00=========="},{21,"==0============================="},
{22,"==1=============================",}};
static const CellRow CHW[]={{6,"==n============================="},{7,"=====u===u==========n==========="},{8,"==u============================="},
{9,"=====u=u=======n===u==n=u=n=u=n="},{10,"============n======u=n=========="},{14,"=0===u===n=1=1====1=u=1=====1=1="},
{15,"==u============================="},{22,"=====0=nn=====1=u=1============="},{24,"==n=============================",}};
typedef struct {u32 m,v,d,p;} Cell;
/* two-bit conditions: kind 0=A 1=E 2=W ; op 1 means '=' , 0 means '!=' */
typedef struct {int k1,i1,b1,op,k2,i2,b2;} X2C;
static const X2C X2[]={{0,15,15,0,0,16,15},{0,15,23,1,0,16,23},{0,15,25,1,0,16,25},{0,16,9,0,0,16,20},{0,16,18,0,0,16,6},
{0,16,8,1,0,16,17},{0,15,29,1,0,17,29},{0,17,29,1,0,18,29},{1,15,4,1,1,16,4},{1,17,0,0,1,17,13},{1,16,24,1,1,17,24},
{1,16,15,1,1,17,15},{1,18,6,0,1,18,19},{1,18,2,1,1,18,20},{1,20,2,0,1,20,16},
{2,6,1,1,2,6,12},{2,6,8,0,2,6,25},{2,6,14,1,2,6,18},{2,7,0,1,2,7,28},{2,7,9,1,2,7,30},{2,7,1,1,2,7,18},
{2,8,1,0,2,8,12},{2,8,8,0,2,8,25},{2,8,14,1,2,8,18},{2,22,31,0,2,22,1},{2,22,30,0,2,22,0},{2,22,16,0,2,22,25},
{2,22,14,0,2,22,21},{2,24,4,0,2,24,6},{2,24,22,1,2,24,31},{2,24,20,0,2,24,27}};
#define NX2 ((int)(sizeof(X2)/sizeof(X2[0])))
static Cell CELL[3][NR];
static void parse_cell(Cell*c,const char*s){c->m=c->v=c->d=c->p=0;for(int i=0;i<32;i++){int b=31-i;char ch=s[i];
 if(ch=='0'||ch=='1'||ch=='u'||ch=='n')c->m|=1u<<b; if(ch=='1'||ch=='u')c->v|=1u<<b; if(ch=='u'||ch=='n')c->d|=1u<<b; if(ch=='+')c->p|=1u<<b;}}
static void init_cells(void){
 memset(CELL,0,sizeof CELL);
 for(unsigned i=0;i<sizeof CHA/sizeof*CHA;i++)parse_cell(&CELL[0][CHA[i].row],CHA[i].s);
 for(unsigned i=0;i<sizeof CHE/sizeof*CHE;i++)parse_cell(&CELL[1][CHE[i].row],CHE[i].s);
 for(unsigned i=0;i<sizeof CHW/sizeof*CHW;i++)parse_cell(&CELL[2][CHW[i].row],CHW[i].s);}
/* published data */
static const u32 CV0[8]={0x177b3054,0x86566196,0x6e70d910,0x63ccf669,0x8de0c06c,0x4e5afdb9,0x2589bbf6,0x7befabae};
static const u32 MX[16]={0x47148b8b,0x88e4d419,0x5c615dc9,0x71c227ff,0xab7a34f8,0x3160fa12,0x100b1577,0x56fe27fb,0xa3d6f43d,0xaf36ae8c,0x0826d41f,0xa3ad8526,0xdf919938,0x82243979,0x849eef4a,0x3cc48222};
static const u32 MY[16]={0x47148b8b,0x88e4d419,0x5c615dc9,0x71c227ff,0xab7a34f8,0x3160fa12,0x300b1577,0x52be2ffb,0x83d6f43d,0xaa37bc26,0x082ec01f,0xa3ad8526,0xdf919938,0x82243979,0x80dee74a,0x1cc48222};
static const u32 W14X=0x849eef4au;
#define NL 44
static const u32 LW15[NL]={0x2c64be0c,0x2c64be0d,0x2c64be2c,0x2c64be2d,0x2d64be0c,0x2d64be0d,0x2d64be2c,0x2d64be2d,0x3c64820b,0x3c64820e,0x3c64820f,0x3c64822b,0x3c64822e,0x3c64822f,0x3c649e0c,0x3c649e0d,0x3c649e2c,0x3c649e2d,0x3c64a20b,0x3c64a20e,0x3c64a20f,0x3c64a22b,0x3c64a22e,0x3c64a22f,0x3cc48222,0x3cc4a222,0x3d64820b,0x3d64820e,0x3d64820f,0x3d64822b,0x3d64822e,0x3d64822f,0x3d649e0c,0x3d649e0d,0x3d649e2c,0x3d649e2d,0x3d64a20b,0x3d64a20e,0x3d64a20f,0x3d64a22b,0x3d64a22e,0x3d64a22f,0x3dc48222,0x3dc4a222};
#define W14DX 0x04400800u
#define W15DX 0x20000000u
#define D6 0x20000000u
#define T6 0x03c00800u
#define D7 0xfbc00800u
#define T7 0x017f8000u
#define D8 0xe0000000u
#define T8 0x043ff800u
/* F6, F7 membership */
static inline int inF6(u32 w){return (u32)(s0(w+D6)-s0(w))==T6;}
static inline int inF7(u32 w){return (u32)(s0(w+D7)-s0(w))==T7;}
/* xoshiro256** */
typedef struct{u64 s[4];}Rng;
static inline u64 rotl64(u64 x,int k){return (x<<k)|(x>>(64-k));}
static inline u64 rnext(Rng*r){u64*s=r->s;u64 res=rotl64(s[1]*5,7)*9,t=s[1]<<17;s[2]^=s[0];s[3]^=s[1];s[1]^=s[2];s[0]^=s[3];s[2]^=t;s[3]=rotl64(s[3],45);return res;}
static void rseed(Rng*r,u64 seed){u64 z=seed;for(int i=0;i<4;i++){z+=0x9e3779b97f4a7c15ull;u64 x=z;x=(x^(x>>30))*0xbf58476d1ce4e5b9ull;x=(x^(x>>27))*0x94d049bb133111ebull;r->s[i]=x^(x>>31);}}
static inline u32 r32(Rng*r){return (u32)(rnext(r)>>32);}
static inline u64 rbelow(Rng*r,u64 n){return (u64)(((__uint128_t)rnext(r)*n)>>64);} /* bias < n/2^64 */
```

### F.5 `mk_lab.py`, `analyze_s4.py`, `run_smc.sh`

```python
# mk_lab.py: lab_s4.h from the r37exact lab.h with the seed-4 pair and the L* list (S from s4_S.json, L* from Ls4.Lstar)
import re, json, sys
S=json.load(open('s4_S.json'))
lst=[ln.split() for ln in open(sys.argv[1] if len(sys.argv)>1 else 'Ls4.Lstar')]
w14=int(lst[0][0],16); assert all(int(a,16)==w14 for a,b in lst)
w15=[int(b,16) for a,b in lst]
src=open('../../r37exact/lab.h').read()
hx=lambda v:'0x%08x'%v
def arr(name,vals): return 'static const u32 %s[%d]={%s};'%(name,len(vals),','.join(hx(v) for v in vals))
src=re.sub(r'static const u32 CV0\[8\]=\{[^}]*\};',arr('CV0',S['CV']),src)
src=re.sub(r'static const u32 MX\[16\]=\{[^}]*\};',arr('MX',S['MX']),src)
src=re.sub(r'static const u32 MY\[16\]=\{[^}]*\};',arr('MY',S['MY']),src)
src=re.sub(r'static const u32 W14X=0x[0-9a-fA-F]+u;','static const u32 W14X=%su;'%hx(w14),src)
src=re.sub(r'static const u32 LW15\[32\]=\{[^}]*\};','#define NL %d\nstatic const u32 LW15[NL]={%s};'%(len(w15),','.join(hx(v) for v in w15)),src)
c=json.load(open('s4_consts.json'))
for k in ('D6','T6','D7','T7','D8','T8'):
    src=re.sub(r'#define %s 0x[0-9a-fA-F]+u'%k,'#define %s %su'%(k,hx(c[k])),src)
open('lab_s4.h','w').write(src)
print('NL',len(w15),'W14X',hx(w14))
```

```python
# analyze_s4.py - applies PREREG_s4.md: Q = 2^log2est21 * exact/n per seed; per-set mean, sd, 99% one-sided Student lower bound (t=2.3870, 63 df)
import re, math, glob, sys
d=sys.argv[1] if len(sys.argv)>1 else 'smc_raw'
def load(lo,hi):
    Q=[];ex=[];cell=[];nn=0;miss=[]
    for s in range(lo,hi+1):
        try: t=open('%s/out_%d.txt'%(d,s)).read()
        except: miss.append(s); continue
        m=re.search(r'n (\d+) stage22cells (\d+) cellevent (\d+) exact (\d+) both (\d+) cell_not_exact (\d+)',t); r=re.search(r'RESULT seed \d+ log2est21 (\S+) ',t)
        if not m or not r: miss.append(s); continue
        n,s22,c,e,b,x=map(int,m.groups()); est=2**float(r.group(1)); Q.append(est*e/n); ex.append(e); cell.append(c)
    return Q,ex,cell,miss
res={}
for name,lo,hi in (('S1',40001,40064),('S2',50001,50064),('S3',60001,60016)):
    Q,ex,cell,miss=load(lo,hi)
    if not Q: continue
    n=len(Q); m=sum(Q)/n; sd=math.sqrt(sum((q-m)**2 for q in Q)/(n-1)); t={64:2.3870,16:2.602}.get(n,2.4)
    lb=m-t*sd/math.sqrt(n)
    res[name]=(m,sd,n,lb)
    print(name,'seeds',n,'missing',miss,'mean log2 %.4f'%math.log2(m),'rel sd %.4f'%(sd/m),'se rel %.4f'%(sd/m/math.sqrt(n)),'LB99 log2 %.4f'%math.log2(lb),'exact total',sum(ex),'cell total',sum(cell))
if 'S1' in res and 'S2' in res:
    (m1,s1,n1,l1),(m2,s2,n2,l2)=res['S1'],res['S2']
    z=(m1-m2)/math.sqrt(s1**2/n1+s2**2/n2)
    x=math.floor(100*math.log2(min(l1,l2)))/100
    print('difference z %.3f'%z,' declared q3_log2 = %.2f'%x, ' pooled mean log2 %.4f'%math.log2((m1+m2)/2))
```

```bash
#!/bin/bash
# cloud: run all prereg seeds, 4 at a time, nice 10, inside one cgroup:
#   systemd-run --scope --unit=r37q3p4 -p MemoryMax=402653184 -p MemorySwapMax=0 bash this_script
cd /root/r37own/step2
mkdir -p smc_raw
date -u +%FT%TZ > smc_raw/START
( for s in $(seq 40001 40064); do echo "$s s4_3456.cls"; done
  for s in $(seq 50001 50064); do echo "$s s4_3456.cls"; done
  for s in $(seq 60001 60016); do echo "$s s4_top223.cls"; done ) > smc_raw/jobs.txt
cat smc_raw/jobs.txt | xargs -P 4 -L 1 bash -c 'nice -n 10 ./smc_s4 $0 8192 512 8192 $1 0 > smc_raw/out_$0.txt 2>&1'
date -u +%FT%TZ > smc_raw/DONE
```

Hashes of the files as run (`pre_cloud/hashes_smc.txt`):

```text
f09f4bedb4d551a4c8795532b320911c17622a80e86f99882625609de0238edc  smc_s4.c
2af1febe7c4b2cbc174420d3b87284ae211ccd12b738f33bea1ff1f39a2f7ff2  lab_s4.h
dd44ff812ccd69eca382a5300f68c68077e00c15c6faf7fa00128bb6c7a0a064  s4_3456.cls
2579f992f5e040d54a01f26eb24351c48edff70d47c45b1c5a67109c3e31a144  s4_top223.cls
f747c1c6d3e5ac86c6929a5ab3a7814f9f952544c8008a0898f42f4275a0578d  Ls4.Lstar
5a350fdf3c96a4085154cace5096c89ca84108e8742f5bab5c16dccb5e78de71  G_s4.bin
```

## Appendix G. The construction programs and the data flow

The outputs of the charged procedures of Section 11.2 and the files that carry them. Every program below was run on the cloud machine as stated in Section 14.2; the sources are reproduced here. `lowm.py` embeds the outputs as one data bundle (zlib and base85 of: the pair, the lines of L*, the modular constants, the signed rows of `chi37_H3_seed4.txt`, the c7 values of the 1,067 classes in the order of `grp.c`, the histogram of their sizes, the union and the intersection of their masks, the four counts of `stats.c`, q3) and derives from it everything else; `python3 lowm.py family` checks the c7 list and the derived classes against the output of `grp.c` (Section 13.2).

| file | name | sha256 |
|---|---|---|
| P_C: characteristic, seed 4 (decoded model) | `seed4.full.chi` | 235556a2609f37e147d7252a08ed377a6515495b1e0c1d7440885207f510b2b9 |
| P_C: seed 4 solver output | `seed4.out` | 9b292d1e98509eacfbdb01abf424767ccb332d527b022720009fcf4bdf4d0554 |
| P_C: seed 4 solver time record | `seed4.time` | b8d3efd01e50572ef91b5b1e2a34cc9a798cc609dcf44596c3f40fc16f3fd905 |
| P_S: pair instance input (signed cells) | `chi37_H3_seed4.txt` | b5580e03f3bdb9cc9e5a81be6e085ee09f4d6dd125acb5ff407353bf6f65a2ae |
| P_S: generator dense_sat.py | `dense_sat.py` | bd85b06117000244bf9cac0904eaf32afad635e6cc41a49753b7ed1470e01598 |
| P_S: instance variable map | `dense_chi.cnf.map` | ec1f6bbedc0b1baef356f414e2004c9f23e679ab89711fdd3ead90af467fd397 |
| P_S: solver output (model) | `H3s4_seed1.out` | f10ccf9b9a657ec22ab4c9b9436014ac9e8e470e37dedf64fbaf1c28f1c43122 |
| P_S: derivation s4_derive.py | `s4_derive.py` | c34ecc434262459ff8d023c6aa008b7993d08b9537f4b58ef61f5e83eccd3573 |
| P_S: pair S (json) | `s4_S.json` | ed792ed30b48fee25a407d767b905c37ff6ce43d9eac0a09554145db55446901 |
| P_S: modular constants | `s4_consts.json` | 4b4ce87a3f873490afc95bf19c890aa9234d0a219f70223087c5ac44a3892d50 |
| P_F: family file (grp.c output) | `s4_3456.cls` | dd44ff812ccd69eca382a5300f68c68077e00c15c6faf7fa00128bb6c7a0a064 |
| P_F: L* (lscan.c output) | `Ls4.Lstar` | f747c1c6d3e5ac86c6929a5ab3a7814f9f952544c8008a0898f42f4275a0578d |
| P_F: stats | `stats.json` | 9fc284564ab70498ecf32804d2ab09adb1ba7d5b3a31ac94cd1453248c7e7c7c |

The instance of P_S (`dense_chi.cnf`, 107,359 variables, 373,031 clauses) has sha256 2ad3a254051cfe6be55cdb14032df13873773943b4ef93c72c0a413753b87d57; `G_s4.bin` (the output of `gscan.c`, 21,935,501 words) 5a350fdf3c96a4085154cace5096c89ca84108e8742f5bab5c16dccb5e78de71. Model checks: `verify_cnf.py` reads the `v` lines of `H3s4_seed1.out` and checks every clause of the CNF (all 373,031 satisfied, no unassigned variable); `s4_derive.py` recomputes the state rows with the step function and checks equality with the rows of the SAT map for rows 0..24, the equal digests of the two members and `words_from_cv`/`invert_cv`.

### G.1 Commands and measured runs

The four programs of P_F, compiled with `gcc -O2` from the sources below and run in this order on the cloud machine, each under `prlimit --as=536870912` and `/usr/bin/time -v` (`run_pre.sh`; the log is reproduced: the command, the user and system seconds, the wall time, the maximum resident set, the last lines of output):

```text
== gscan: ./gscan 92cedd4c 2a75d618 4 e0000000 043ff800 G.bin
rc=0
 User time (seconds): 0.46
 System time (seconds): 0.03
 Elapsed (wall clock) time (h:mm:ss or m:ss): 0:00.49
 Maximum resident set size (kbytes): 1912
G size 21935501
== grp: ./grp G.bin 8f5a9ca1 6effba9c 3604bd1f 76760d10 6b0dfe86 9a41cebd 92cedd4c 3456 s4_3456
rc=0
 User time (seconds): 1.32
 System time (seconds): 0.15
 Elapsed (wall clock) time (h:mm:ss or m:ss): 0:01.48
 Maximum resident set size (kbytes): 344284
classes 16980 variants 21935501 ; classes>=3456: 1067 variants 4378186
== lscan: ./lscan s4.cfg Ls4
rc=0
 User time (seconds): 66.61
 System time (seconds): 0.05
 Elapsed (wall clock) time (h:mm:ss or m:ss): 1:06.66
 Maximum resident set size (kbytes): 132988
Q14 4096
Q15 33554432
L 1048576 Lstar 44
== stats: ./stats r16cfg.txt
rc=0
 User time (seconds): 6.86
 System time (seconds): 0.00
 Elapsed (wall clock) time (h:mm:ss or m:ss): 0:06.86
 Maximum resident set size (kbytes): 1656
l 43 r16 65536
R16 2893824
PNZ 2517128 TOT 2883584 (mean 0.171875, NL/256 = 0.171875)
5a350fdf3c96a4085154cace5096c89ca84108e8742f5bab5c16dccb5e78de71  G.bin
dd44ff812ccd69eca382a5300f68c68077e00c15c6faf7fa00128bb6c7a0a064  s4_3456.cls
6df90c8b6de6f68962ee3b34417d5d79cc27c65ca2ee90bab3632225454466a7  s4_3456.hist
f747c1c6d3e5ac86c6929a5ab3a7814f9f952544c8008a0898f42f4275a0578d  Ls4.Lstar
7033899ee9218ff02b1bfd168828955755d5fc794cfcd10f67e55669a7bf2810  Ls4.L
Fri Oct 16 10:55:04 PM UTC 2026
```

The arguments are the constants of Sections 4.3 and 5.1 for this S (C4, W8C, the top bits of E4, d8, t8; A1, A2, A3, E5, E6, E7, C4 and the size threshold 3456); `s4.cfg` is written by `mkcfg.py s4 s4.cfg` and `r16cfg.txt` by `dump_r16cfg.py`. The outputs have the sha256 of the table above (G_s4.bin = G.bin, s4_3456.cls, Ls4.Lstar). `dense_sat.py chi` runs in the directory of `chi37.txt` (= `chi37_H3_seed4.txt`).

### G.2 `gscan.c`

```c
/* gscan.c - exhaustive scan of the A0-variant family G for a given S.
   usage: gscan C4 W8C E4top3 D8 T8 out.bin     (hex, E4top3 = value of E4[31:29] (0..7))
   G = { a0 : E4 = a0 + C4 has E4[31:29] = E4top3, w = W8C - E4 has w[29] = 1 and s0(w + D8) - s0(w) = T8 }  (exhaustive over the 2^29 values of E4) */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef uint32_t u32;
static inline u32 ror(u32 x,int n){return (x>>n)|(x<<(32-n));}
static inline u32 s0(u32 x){return ror(x,7)^ror(x,18)^(x>>3);}
int main(int argc,char**argv){
  if(argc<7){fprintf(stderr,"usage\n");return 2;}
  u32 C4=strtoul(argv[1],0,16),W8C=strtoul(argv[2],0,16),top=strtoul(argv[3],0,16),D8=strtoul(argv[4],0,16),T8=strtoul(argv[5],0,16);
  FILE*f=fopen(argv[6],"wb"); u32 cnt=0;
  for(u32 lo=0;lo<(1u<<29);lo++){ u32 e4=(top<<29)|lo; u32 w=W8C-e4;
    if(!((w>>29)&1))continue; if((u32)(s0(w+D8)-s0(w))!=T8)continue;
    u32 a0=e4-C4; fwrite(&a0,4,1,f); cnt++; }
  fclose(f); printf("G size %u\n",cnt); return 0;}
```

### G.3 `grp.c`

```c
/* grp.c - group G by c7 and write the classes with >= MINSZ members.
   usage: grp G.bin A1 A2 A3 E5 E6 E7 C4 minsz out_prefix
   c7(a0) = E7 - A3 - k3(a0) - S1(E6) - CH(E6,E5,a0+C4) - K7 ,  k3(a0) = K3C - MAJ(A2,A1,a0) , K3C = A3 - S0(A2)
   out_prefix.hist : size count ; out_prefix.cls : lines "c7 n a0 a0 ..." for classes with n >= minsz, sorted by (-n, c7) */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef uint32_t u32; typedef uint64_t u64;
static inline u32 ror(u32 x,int n){return (x>>n)|(x<<(32-n));}
static inline u32 S0(u32 x){return ror(x,2)^ror(x,13)^ror(x,22);}
static inline u32 S1(u32 x){return ror(x,6)^ror(x,11)^ror(x,25);}
static inline u32 CH(u32 x,u32 y,u32 z){return (x&y)^(~x&z);}
static inline u32 MAJ(u32 x,u32 y,u32 z){return (x&y)^(x&z)^(y&z);}
static int cmp(const void*a,const void*b){u64 x=*(const u64*)a,y=*(const u64*)b;return x<y?-1:x>y;}
int main(int argc,char**argv){
  if(argc<11){fprintf(stderr,"usage\n");return 2;}
  FILE*f=fopen(argv[1],"rb"); u32 A1=strtoul(argv[2],0,16),A2=strtoul(argv[3],0,16),A3=strtoul(argv[4],0,16),E5=strtoul(argv[5],0,16),E6=strtoul(argv[6],0,16),E7=strtoul(argv[7],0,16),C4=strtoul(argv[8],0,16);
  long minsz=atol(argv[9]); const char*pre=argv[10]; const u32 K7=0xab1c5ed5;
  fseek(f,0,SEEK_END); long n=ftell(f)/4; fseek(f,0,SEEK_SET); u32*g=malloc(n*4); if(fread(g,4,n,f)!=(size_t)n)return 3; fclose(f);
  u64*k=malloc(n*8); u32 K3C=A3-S0(A2);
  for(long i=0;i<n;i++){ u32 a0=g[i]; u32 e4=a0+C4; u32 k3=K3C-MAJ(A2,A1,a0); u32 c7=E7-A3-k3-S1(E6)-CH(E6,E5,e4)-K7; k[i]=((u64)c7<<32)|a0; }
  free(g); qsort(k,n,8,cmp);
  char nm[512]; snprintf(nm,512,"%s.hist",pre); FILE*h=fopen(nm,"w"); snprintf(nm,512,"%s.cls",pre); FILE*c=fopen(nm,"w");
  static long hist[1<<20]; long ncls=0; long i=0; long big=0, bigvar=0;
  /* pass 1: histogram */
  while(i<n){ long j=i; while(j<n&&(k[j]>>32)==(k[i]>>32))j++; long sz=j-i; ncls++; if(sz<(1<<20))hist[sz]++; i=j; }
  for(long s=0;s<(1<<20);s++) if(hist[s]) fprintf(h,"%ld %ld\n",s,hist[s]);
  fprintf(h,"# classes %ld variants %ld\n",ncls,n);
  { snprintf(nm,512,"%s.sum",pre); FILE*sm=fopen(nm,"w"); long a=0; while(a<n){ long j=a; u32 an=0xffffffffu,orr=0; while(j<n&&(k[j]>>32)==(k[a]>>32)){ u32 v=(u32)k[j]; an&=v; orr|=v; j++; } fprintf(sm,"%08x %ld %08x %08x\n",(u32)(k[a]>>32),j-a,an,orr); a=j; } fclose(sm); }
  /* pass 2: classes >= minsz (in c7 order) */
  i=0; while(i<n){ long j=i; while(j<n&&(k[j]>>32)==(k[i]>>32))j++; long sz=j-i;
    if(sz>=minsz){ big++; bigvar+=sz; fprintf(c,"%08x %ld",(u32)(k[i]>>32),sz); for(long q=i;q<j;q++)fprintf(c," %08x",(u32)k[q]); fprintf(c,"\n"); } i=j; }
  fclose(h); fclose(c); printf("classes %ld variants %ld ; classes>=%ld: %ld variants %ld\n",ncls,n,minsz,big,bigvar); return 0;}
```

### G.4 `lscan.c`

```c
/* lscan.c - the set L of (W14x, W15x) (rows 14 and 15 of both members follow the cells; the four expansion differences depending only on (W14,W15) equal the pair's)
   and L* (row-16 modular differences equal the characteristic's: dE16 and dA16).   usage: lscan cfg out_prefix
   Members: y words W14y = W14x ^ MASK14, W15y = W15x ^ MASK15.  Cells are (m,v,d,p): x&m==v, x^y==d; E '+' link p: (E_i ^ E_{i-1}) & p_i & p_{i-1} == 0 (x member).
   Scan: W14 over all 2^32 (cheap tests first), W15 over all 2^32 (tests independent of S), then the product. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
typedef uint32_t u32; typedef uint64_t u64;
static inline u32 ror(u32 x,int n){return (x>>n)|(x<<(32-n));}
static inline u32 S0(u32 x){return ror(x,2)^ror(x,13)^ror(x,22);}
static inline u32 S1(u32 x){return ror(x,6)^ror(x,11)^ror(x,25);}
static inline u32 s0(u32 x){return ror(x,7)^ror(x,18)^(x>>3);}
static inline u32 s1(u32 x){return ror(x,17)^ror(x,19)^(x>>10);}
static inline u32 CH(u32 x,u32 y,u32 z){return (x&y)^(~x&z);}
static inline u32 MAJ(u32 x,u32 y,u32 z){return (x&y)^(x&z)^(y&z);}
static const u32 K[17]={0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,0xe49b69c1};
typedef struct{u32 m,v,d,p;}Cell;
static u32 Ax[17],Ay[17],Ex[17],Ey[17];
static Cell CA[16],CE[16],CW[16];
static u32 W14x,W14y,W15x,W15y,T114,T115,T014,T015,MASK14,MASK15,DA16,DE16;
static u32 get(FILE*f,const char*name,u32*o,int n){ rewind(f); char ln[512]; while(fgets(ln,512,f)){ char nm[64]; int off=0; if(sscanf(ln,"%63s%n",nm,&off)!=1)continue; if(strcmp(nm,name))continue; char*p=ln+off; for(int i=0;i<n;i++){ char*e; o[i]=strtoul(p,&e,16); p=e; } return 1;} fprintf(stderr,"missing %s\n",name); exit(3);}
static int cellok(const Cell*c,u32 x,u32 y){ return (x&c->m)==c->v && (x^y)==c->d; }
static u32 rowE(const u32*A,const u32*E,int t,u32 W){ return A[t-4]+E[t-4]+S1(E[t-1])+CH(E[t-1],E[t-2],E[t-3])+K[t]+W; }
static u32 rowA(const u32*A,u32 e,int t){ return e-A[t-4]+S0(A[t-1])+MAJ(A[t-1],A[t-2],A[t-3]); }
int main(int argc,char**argv){
  FILE*f=fopen(argv[1],"r"); u32 t[4];
  for(int r=8;r<=13;r++){ char nm[16]; snprintf(nm,16,"A%d",r); get(f,nm,t,2); Ax[r]=t[0];Ay[r]=t[1]; snprintf(nm,16,"E%d",r); get(f,nm,t,2); Ex[r]=t[0];Ey[r]=t[1]; }
  get(f,"W14",t,2); get(f,"W15",t,2); /* only for reference output */
  u32 w9[2],w10[2]; get(f,"W9",w9,2); get(f,"W10",w10,2);
  for(int r=13;r<=15;r++){ char nm[16]; snprintf(nm,16,"CA%d",r); get(f,nm,t,4); CA[r]=(Cell){t[0],t[1],t[2],t[3]}; snprintf(nm,16,"CE%d",r); get(f,nm,t,4); CE[r]=(Cell){t[0],t[1],t[2],t[3]}; snprintf(nm,16,"CW%d",r); get(f,nm,t,4); CW[r]=(Cell){t[0],t[1],t[2],t[3]}; }
  get(f,"T114",&T114,1);get(f,"T115",&T115,1);get(f,"T014",&T014,1);get(f,"T015",&T015,1);get(f,"MASK14",&MASK14,1);get(f,"MASK15",&MASK15,1);get(f,"DA16",&DA16,1);get(f,"DE16",&DE16,1);
  /* Q14 */
  u32*Q14=malloc(sizeof(u32)*(1<<20)); long n14=0; u32 mw=CW[14].m,vw=CW[14].v;
  for(u64 w64=0; w64<(1ull<<32); w64++){ u32 w=(u32)w64; if((w&mw)!=vw)continue; u32 y=w^MASK14;
    if((u32)(s1(y)-s1(w))!=T114)continue; if((u32)(s0(y)-s0(w))!=T014)continue;
    u32 ex=rowE(Ax,Ex,14,w), ey=rowE(Ay,Ey,14,y); if(!cellok(&CE[14],ex,ey))continue;
    u32 pq=CE[14].p&CE[13].p; if((ex^Ex[13])&pq)continue;
    u32 ax=rowA(Ax,ex,14), ay=rowA(Ay,ey,14); if(!cellok(&CA[14],ax,ay))continue;
    if(n14>=(1<<20)){fprintf(stderr,"Q14 overflow\n");return 4;} Q14[n14++]=w; }
  printf("Q14 %ld\n",n14);
  u32*Q15=malloc(sizeof(u32)*((1<<25)+1024)); long n15=0; mw=CW[15].m; vw=CW[15].v;
  for(u64 w64=0; w64<(1ull<<32); w64++){ u32 w=(u32)w64; if((w&mw)!=vw)continue; u32 y=w^MASK15;
    if((u32)(s1(y)-s1(w))!=T115)continue; if((u32)(s0(y)-s0(w))!=T015)continue;
    if(n15>=(1<<25)+1024){fprintf(stderr,"Q15 overflow\n");return 4;} Q15[n15++]=w; }
  printf("Q15 %ld\n",n15);
  char nm[600]; snprintf(nm,600,"%s.L",argv[2]); FILE*fo=fopen(nm,"w"); snprintf(nm,600,"%s.Lstar",argv[2]); FILE*fs=fopen(nm,"w");
  long nL=0,nLs=0;
  for(long i=0;i<n14;i++){ u32 w14=Q14[i], y14=w14^MASK14;
    u32 AX[17],AY[17],EX[17],EY[17]; memcpy(AX,Ax,sizeof AX);memcpy(AY,Ay,sizeof AY);memcpy(EX,Ex,sizeof EX);memcpy(EY,Ey,sizeof EY);
    EX[14]=rowE(AX,EX,14,w14); EY[14]=rowE(AY,EY,14,y14); AX[14]=rowA(AX,EX[14],14); AY[14]=rowA(AY,EY[14],14);
    for(long j=0;j<n15;j++){ u32 w15=Q15[j], y15=w15^MASK15;
      u32 ex=rowE(AX,EX,15,w15), ey=rowE(AY,EY,15,y15); if(!cellok(&CE[15],ex,ey))continue;
      u32 pq=CE[15].p&CE[14].p; if((ex^EX[14])&pq)continue;
      u32 ax=rowA(AX,ex,15), ay=rowA(AY,ey,15); if(!cellok(&CA[15],ax,ay))continue;
      nL++; fprintf(fo,"%08x %08x\n",w14,w15);
      EX[15]=ex;EY[15]=ey;AX[15]=ax;AY[15]=ay;
      /* row 16: E16 = rest + W16, W16x = s1(w14)+W9x+s0(W1)+W0 (shared part cancels in the difference); dE16 = restY-restX + dW16 */
      u32 rx=AX[12]+EX[12]+S1(EX[15])+CH(EX[15],EX[14],EX[13])+K[16];
      u32 ry=AY[12]+EY[12]+S1(EY[15])+CH(EY[15],EY[14],EY[13])+K[16];
      u32 dW16=(s1(y14)-s1(w14))+(w9[1]-w9[0]);
      u32 dE16=(ry-rx)+dW16; if(dE16!=DE16)continue;
      /* A16 = E16 - A12 + S0(A15) + MAJ(A15,A14,A13); E16y = E16x + dE16 */
      u32 dA16=(dE16-(AY[12]-AX[12]))+((S0(AY[15])+MAJ(AY[15],AY[14],AY[13]))-(S0(AX[15])+MAJ(AX[15],AX[14],AX[13])));
      if(dA16!=DA16)continue;
      nLs++; fprintf(fs,"%08x %08x\n",w14,w15); } }
  fclose(fo);fclose(fs); printf("L %ld Lstar %ld\n",nL,nLs); return 0;}
```

### G.4b `mkcfg.py`

```python
# mkcfg.py MODE out.cfg   MODE = pub | s4   (pub: published pair + published cells with value bits; s4: seed-4 H3 model + signed-only cells for rows <=15)
import sys, json
sys.path.insert(0,'.')
import lowm_zf6 as L
M=L.M32
mode,out=sys.argv[1],sys.argv[2]
if mode=='pub':
    CV=L.CV0; MX=L.MX; MY=L.MY
    cell=lambda k,i: L.CELLS[k][i]
else:
    S=json.load(open('s4_S.json')); CV=S['CV']; MX=S['MX']; MY=S['MY']
    chi={}
    for ln in open('dec/chi37.txt'):
        t=ln.split()
        if len(t)==5 and t[0]=='row': chi[int(t[1])]=t[2:5]
    def cell(k,i):
        s=chi[i][{'A':0,'E':1,'W':2}[k]] if i in chi else '='*32
        s=''.join(c if c in 'nu' else '=' for c in s)
        return L.cell(s)
tx=L.trace(CV,MX,17); ty=L.trace(CV,MY,17)
lines=[]
def put(name,*vals): lines.append(name+' '+' '.join('%08x'%v for v in vals))
for r in range(8,14):
    put('A%d'%r,tx[0][r],ty[0][r]); put('E%d'%r,tx[1][r],ty[1][r])
put('W9',MX[9],MY[9]); put('W10',MX[10],MY[10]); put('W11',MX[11],MY[11]); put('W12',MX[12],MY[12]); put('W13',MX[13],MY[13])
put('W14',MX[14],MY[14]); put('W15',MX[15],MY[15])
for k in 'AEW':
    for r in (13,14,15):
        c=cell(k,r); put('C%s%d'%(k,r),*c)   # m v d p
# expansion targets
put('T114',(L.s1(MY[14])-L.s1(MX[14]))&M); put('T115',(L.s1(MY[15])-L.s1(MX[15]))&M)
put('T014',(L.s0(MY[14])-L.s0(MX[14]))&M); put('T015',(L.s0(MY[15])-L.s0(MX[15]))&M)
put('MASK14',MX[14]^MY[14]); put('MASK15',MX[15]^MY[15])
# row 16 target differences: dE16 = 0 ; dA16 = pair's
put('DA16',(ty[0][16]-tx[0][16])&M); put('DE16',(ty[1][16]-tx[1][16])&M)
open(out,'w').write('\n'.join(lines)+'\n')
print(open(out).read())
```

### G.5 `stats.c` and `dump_r16cfg.py`

```c
/* stats.c: exact counts for the ledger from the definitions.  usage: stats r16cfg.txt
   F6 = #{w : s0(w+D6)-s0(w) = T6}, F7 likewise (2^32 scan each); R16 = #{(e,l)}: e satisfies the exact row-16 test of lowm_gen.Env.exact (enumerated over the free bits of E16);
   PNZ = #{u mod 2^24 : some l has bits 0..23 of u + C_l satisfying the eight fixed-bit conditions of the filter stage}; MU numerator = sum over u of the number of such l */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
typedef uint32_t u32;
static inline u32 ror(u32 x,int n){return (x>>n)|(x<<(32-n));}
static inline u32 s0(u32 x){return ror(x,7)^ror(x,18)^(x>>3);}
int main(int argc,char**argv){
  FILE*f=fopen(argv[1],"r"); int nl; u32 E16M,E16V,D6,T6,D7,T7;
  if(fscanf(f,"%d %x %x %x %x %x %x",&nl,&E16M,&E16V,&D6,&T6,&D7,&T7)!=7)return 2;
  u32 C[64],CX[64],EX[64],VA[64];
  for(int l=0;l<nl;l++) if(fscanf(f,"%x %x %x %x",&C[l],&CX[l],&EX[l],&VA[l])!=4)return 3;
  long f6=0,f7=0; for(uint64_t w=0;w<(1ull<<32);w++){u32 x=(u32)w; u32 b=s0(x); if((u32)(s0(x+D6)-b)==T6)f6++; if((u32)(s0(x+D7)-b)==T7)f7++;}
  printf("F6 %ld F7 %ld\n",f6,f7);
  long r16=0; u32 fr=~E16M; 
  for(int l=0;l<nl;l++){ long cnt=0; u32 sub=0; do{ u32 e=sub|E16V; u32 A=e+CX[l];
      u32 t=((e&E16M)^E16V)|((e^EX[l])&0x10)|((A&0x22808000)^VA[l]);
      u32 x1=A^(A>>11),x2=A^(A>>12),x3=A^(A>>9);
      if((t|(((x1&0x200)|(x2&0x40)|(x3&0x100))^0x240))==0)cnt++;
      sub=(sub-fr)&fr; }while(sub); printf("l %d r16 %ld\n",l,cnt); r16+=cnt; }
  printf("R16 %ld\n",r16);
  /* filter stage: fixed bits of E16 in the low 24 bits and E16[4]=E15[4] */
  u32 FIX=E16M&0xffffff|0x10, VAL; long nz=0,tot=0;
  for(u32 u=0;u<(1u<<24);u++){int any=0; for(int l=0;l<nl;l++){u32 e=(u+C[l])&0xffffff; if((e&(E16M&0xffffff))==(E16V&0xffffff) && (((u+C[l])^EX[l])&0x10)==0){any=1;tot++;}} nz+=any;}
  printf("PNZ %ld TOT %ld (mean %.6f, NL/256 = %.6f)\n",nz,tot,(double)tot/(1u<<24),nl/256.0);
  (void)FIX;(void)VAL; return 0;}
```

```python
# dump_r16cfg.py: per-l constants of the exact row-16 test (from lowm_gen.Env) for the C counting tool stats.c
import lowm_gen as L
e = L.Env()
with open('r16cfg.txt', 'w') as f:
    f.write('%d %08x %08x %08x %08x %08x %08x\n' % (len(L.FEASIBLE_L), L.E16M, L.E16V, L.D6, L.T6, L.D7, L.T7))
    for l in L.FEASIBLE_L:
        c = e.LC[l]; f.write('%08x %08x %08x %08x\n' % (c['C'], c['cxA'], c['Ex15'], e.VA[l]))
print('ok')
```

### G.6 `f8.c` (the W8 conditions of G over all 2^32 words; output `F8&b29 268435456 cond 268435456 diff 0`, 6.83 s)

```c
#include <stdio.h>
#include <stdint.h>
typedef uint32_t u32;
static inline u32 ror(u32 x,int n){return (x>>n)|(x<<(32-n));}
static inline u32 s0(u32 x){return ror(x,7)^ror(x,18)^(x>>3);}
int main(){ uint64_t a=0,b=0,diff=0; for(uint64_t v=0;v<(1ull<<32);v++){u32 w=(u32)v; int f8=((u32)(s0(w+0xe0000000u)-s0(w))==0x043ff800u)&&((w>>29)&1);
  int c=((w>>29)&1)&&(((w>>1)&1)!=((w>>12)&1))&&(((w>>8)&1)!=((w>>25)&1))&&(((w>>14)&1)==((w>>18)&1)); a+=f8;b+=c;diff+=(f8!=c);} printf("F8&b29 %llu cond %llu diff %llu\n",(unsigned long long)a,(unsigned long long)b,(unsigned long long)diff);return 0;}
```

### G.7 `mk_h3.py` and `s4_derive.py`

```python
import re
R='D:/~~Projects/~HashSmash/workspace/research/'
def load(p):
    rows={}
    for ln in open(p):
        t=ln.split()
        if len(t)==5 and t[0]=='row': rows[int(t[1])]=t[2:5]
    return rows
sg=lambda s:''.join(c if c in 'nu' else '=' for c in s)
pub=load(R+'tools/traillab/chi/chi37.txt')
def w(fn,rows,note):
    with open(fn,'w') as f:
        f.write('# '+note+'\n')
        for r in sorted(rows): f.write("row %2d %s %s %s\n"%(r,*rows[r]))
base={r:[sg(x) for x in v] for r,v in pub.items()}
w('chi37_H3_pub.txt',base,'H3 control: published chi37 SIGNED CELLS ONLY (no 0/1/+ values, no x2)')
for k in (4,5,7):
    c=load(R+'levers_1016/r37char/map/seed%d.full.chi'%k)
    rows={r:list(v) for r,v in base.items()}
    for r in range(6,16): rows[r]=list(c[r])
    w('chi37_H3_seed%d.txt'%k,rows,'H3 seed %d: signed cells only, rows 6..15 from the SAT model seed %d, rows 4,5,16..24 published signed'%(k,k))
```

```python
# s4_derive.py - derive S (seed-4 H3 model), the SFS completion, d6/d7/t's, G conditions. Reads the kissat model + map; recomputes with the lowm trace (own implementation of the step function).
import sys, json
sys.path.insert(0,'.')
import lowm_zf6 as L
M=L.M32
def load_vals(path):
    vals=set()
    for ln in open(path):
        if ln.startswith('v '):
            for t in ln.split()[1:]:
                if t!='0': vals.add(int(t))
    return vals
def word(bits,vals):
    x=0
    for i,b in enumerate(bits):
        b=int(b)
        if b in vals: x|=1<<i
        elif -b not in vals: raise SystemExit('missing '+str(b))
    return x
vals=load_vals('H3s4_seed1.out')
words={}
for ln in open('dec/dense_chi.cnf.map'):
    p=ln.split()
    if p[0]=='true': continue
    words[p[0]]=word(p[1:],vals)
CV=[words[k] for k in ('A-1','A-2','A-3','A-4','E-1','E-2','E-3','E-4')]
MX=[words['W%d'%i] for i in range(16)]
masks={6:0x20000000,8:0x20000000,15:0x20000000,7:0x04400800,14:0x04400800,10:0x00081400,9:0x050112AA}
MY=[MX[i]^masks.get(i,0) for i in range(16)]
tx=L.trace(CV,MX,37); ty=L.trace(CV,MY,37)
# the pair is a real full SFS collision of the 37-step compression
assert L.compress(CV,MX)==L.compress(CV,MY)
# state rows from the SAT map agree with the independent trace
for i in range(0,25):
    assert words['Ax%d'%i]==tx[0][i] and words['Ex%d'%i]==tx[1][i]
S=dict(CV=CV,MX=MX,MY=MY,
       A=[tx[0][i] for i in range(14)],Ay=[ty[0][i] for i in range(14)],
       E=[tx[1][i] for i in range(14)],Ey=[ty[1][i] for i in range(14)])
A=S['A'];E=S['E'];Ey=S['Ey']
A1,A2,A3,A4=A[1],A[2],A[3],A[4]; E5,E6,E7=E[5],E[6],E[7]
C4=(A4-L.S0(A3)-L.MAJ(A3,A2,A1))&M
W8C=(E[8]-A4-L.S1(E7)-L.CH(E7,E6,E5)-L.K[8])&M
C6=(E6-2*A2+L.S0(A1)-L.S1(E5)-L.K[6])&M
K3C=(A3-L.S0(A2))&M
assert (W8C-(A[0]+C4))&M==MX[8]
# modular differences
d=lambda i:(MY[i]-MX[i])&M
D6=d(6);D7=d(7);D8=d(8)
T6=(L.s0(MY[6])-L.s0(MX[6]))&M; T7=(L.s0(MY[7])-L.s0(MX[7]))&M; T8=(L.s0(MY[8])-L.s0(MX[8]))&M
print('D6,D7,D8 %08x %08x %08x  T6,T7,T8 %08x %08x %08x'%(D6,D7,D8,T6,T7,T8))
print('published    20000000 fbc00800 e0000000   03c00800 017f8000 043ff800')
print('F6(W6x),F7(W7x):',L.inF(MX[6],D6,T6),L.inF(MX[7],D7,T7))
print('C4 %08x W8C %08x C6 %08x K3C %08x'%(C4,W8C,C6,K3C))
print('pub C4 000b362e W8C da3a7d2f C6 f538a8f7 K3C 478132ed')
# SFS completion check: invert_cv / words_from_cv on the model's CV
# (lowm_zf6.words_from_cv uses module globals SA/SAy of the PUBLISHED S; reimplement generically here)
def words_from_cv(cv,a0,SAx,SAy):
    out=[]
    for Sx in (SAx,SAy):
        Ar={-1:cv[0],-2:cv[1],-3:cv[2],-4:cv[3]}; Er={-1:cv[4],-2:cv[5],-3:cv[6],-4:cv[7]}
        for i in range(14): Ar[i]=Sx[i]
        Ar[0]=a0
        for i in range(14): Er[i]=(Ar[i]+Ar[i-4]-L.S0(Ar[i-1])-L.MAJ(Ar[i-1],Ar[i-2],Ar[i-3]))&M
        out.append([(Er[i]-Ar[i-4]-Er[i-4]-L.S1(Er[i-1])-L.CH(Er[i-1],Er[i-2],Er[i-3])-L.K[i])&M for i in range(14)])
    return out
wx,wy=words_from_cv(CV,A[0],S['A'],S['Ay'])
assert wx==MX[:14] and wy==MY[:14], 'completion mismatch'
print('words_from_cv(CV,A0,S) reproduces W0..W13 of both members: OK')
cv2=L.invert_cv(tx[0],tx[1],MX)
assert cv2==CV
print('invert_cv from state rows 4..7 and W0..W7 reproduces CV: OK')
json.dump({k:(v if not isinstance(v,list) else v) for k,v in dict(S).items()},open('s4_S.json','w'))
json.dump(dict(C4=C4,W8C=W8C,C6=C6,K3C=K3C,D6=D6,D7=D7,D8=D8,T6=T6,T7=T7,T8=T8,A1=A1,A2=A2,A3=A3,A4=A4,E5=E5,E6=E6,E7=E7,A0=A[0],E4=E[4]),open('s4_consts.json','w'),indent=1)
# d7 as a function of E4: only the bits where E6x != E6y matter
P=E[6]^Ey[6]
print('E6 xor diff bits mask %08x'%P, 'E6x %08x E6y %08x'%(E[6],Ey[6]))
bits=[b for b in range(32) if (P>>b)&1]
def d7_of(e4):
    # W7 = E7 - A3 - E3 - S1(E6) - CH(E6,E5,E4) - K7 ; x and y share A3,E3,E5,E4 ; E7 differs
    w7x=(E[7]-A3-0-L.S1(E[6])-L.CH(E[6],E5,e4)-L.K[7])&M
    w7y=(Ey[7]-A3-0-L.S1(Ey[6])-L.CH(Ey[6],E5,e4)-L.K[7])&M
    return (w7y-w7x)&M
good=[]
for assign in range(1<<len(bits)):
    e4=0
    for k,b in enumerate(bits):
        if (assign>>k)&1: e4|=1<<b
    if d7_of(e4)==D7: good.append(assign)
print('bits of E4 that matter',bits,' assignments giving d7=D7:',[ ''.join(str((a>>k)&1) for k in range(len(bits)-1,-1,-1)) for a in good])
print('model E4 %08x d7_of %08x'%(E[4],d7_of(E[4])))
json.dump(dict(bits=bits,good=good),open('s4_d7.json','w'))
```

```python
import sys
cnf, out = sys.argv[1], sys.argv[2]
vals=set(); st=None
for l in open(out):
    if l.startswith('s '): st=l.strip()
    if l.startswith('v '):
        for t in l.split()[1:]:
            if t!='0': vals.add(int(t))
nv=None; ncl=0; bad=0
cur=[]
for l in open(cnf):
    if l.startswith('p'): nv=int(l.split()[2]); continue
    if l.startswith('c'): continue
    for t in l.split():
        x=int(t)
        if x==0:
            ncl+=1
            if not any(v in vals for v in cur): bad+=1
            cur=[]
        else: cur.append(x)
miss=[v for v in range(1,nv+1) if v not in vals and -v not in vals]
import hashlib
print(st,'vars',nv,'model_lits',len(vals),'unassigned',len(miss),'clauses',ncl,'unsat_clauses',bad, 'cnf_sha256',hashlib.sha256(open(cnf,'rb').read()).hexdigest())
```

### G.8 `dense_sat.py` (the generator of the pair instance; sha256 above)

```python
# CNF for a semi-free-start pair whose message XOR is the one-bit family
# at disturbance bit 29, expanded differences live only in {22, 24},
# and the state differences obey the Section 4.1 window:
#   δA = 0 outside {6..16}, δE = 0 outside {6..20},
#   δE18 = -δW22, δE20 = δA16 = -δW24, δE16 = δE19 = δE21 = 0,
#   δA17 = δA18 = δA19 = 0, and the same through step 24.
# The algebraic masks are computed from σ. No cell from chi37.txt is read.
# The published pair is an optional encoding check (CHECK=1).

import sys
import time

MASK = 0xFFFFFFFF
B = 29

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

# Published pair, encoding check only.
CV = [0x63b4986c, 0x35d83dc0, 0xc98894e4, 0x784e08fc,
      0x78a7f752, 0x5ed877a8, 0x315a2db3, 0xd5614eb4]
MX = [0x4d7f86ff, 0x32ece589, 0xd8accfc4, 0x2cc2e433, 0x068b5b34, 0xeba68a28,
      0x0fe12cad, 0x6ee2630c, 0xbf0d78e1, 0x6d1a90dd, 0xfaa1d3e0, 0x56aed439,
      0xcc2dbbc2, 0xdd2ba0fc, 0xbd1d3f7b, 0x7dd43a81]
MY = [0x4d7f86ff, 0x32ece589, 0xd8accfc4, 0x2cc2e433, 0x068b5b34, 0xeba68a28,
      0x2fe12cad, 0x6aa26b0c, 0x9f0d78e1, 0x681b8277, 0xfaa9c7e0, 0x56aed439,
      0xcc2dbbc2, 0xdd2ba0fc, 0xb95d377b, 0x5dd43a81]


def rotr(x, n):
    x &= MASK
    return ((x >> n) | (x << (32 - n))) & MASK


def sig0_int(x):
    return rotr(x, 7) ^ rotr(x, 18) ^ ((x & MASK) >> 3)


def sig1_int(x):
    return rotr(x, 17) ^ rotr(x, 19) ^ ((x & MASK) >> 10)


def Sig0_int(x):
    return rotr(x, 2) ^ rotr(x, 13) ^ rotr(x, 22)


def Sig1_int(x):
    return rotr(x, 6) ^ rotr(x, 11) ^ rotr(x, 25)


def Ch_int(x, y, z):
    return ((x & y) ^ ((~x) & z)) & MASK


def Maj_int(x, y, z):
    return ((x & y) ^ (x & z) ^ (y & z)) & MASK


def masks_at(b):
    D = 1 << b
    return {
        6: D, 8: D, 15: D,
        7: sig0_int(D), 14: sig0_int(D),
        10: sig1_int(D),
        9: sig1_int(sig0_int(D)),
    }


class Ckt:
    def __init__(self, check_bits=None):
        self.n = 0
        self.clauses = []
        self.check = check_bits is not None
        self.val = {}
        self.true = None
        if self.check:
            self.seed = check_bits
        self.true = self.new(1 if self.check else None)
        self.clause(self.true)

    def new(self, value=None):
        self.n += 1
        if self.check:
            if value is None:
                raise RuntimeError("check mode needs a value")
            self.val[self.n] = value & 1
        return self.n

    def bit(self, lit):
        v = self.val[abs(lit)]
        return v if lit > 0 else 1 - v

    def clause(self, *lits):
        ls = [int(x) for x in lits if x != 0]
        self.clauses.append(ls)
        if self.check:
            if not any(self.bit(x) == 1 for x in ls):
                raise RuntimeError(f"clause fails {ls}")

    def xor2(self, a, b):
        if self.check:
            v = self.bit(a) ^ self.bit(b)
        else:
            v = None
        o = self.new(v)
        # even parity of (a, b, o)
        self.clause(-a, -b, -o)
        self.clause(a, b, -o)
        self.clause(a, -b, o)
        self.clause(-a, b, o)
        return o

    def and2(self, a, b):
        v = (self.bit(a) & self.bit(b)) if self.check else None
        o = self.new(v)
        self.clause(-a, -b, o)
        self.clause(a, -o)
        self.clause(b, -o)
        return o

    def or2(self, a, b):
        v = (self.bit(a) | self.bit(b)) if self.check else None
        o = self.new(v)
        self.clause(a, b, -o)
        self.clause(-a, o)
        self.clause(-b, o)
        return o

    def full_add(self, x, y, cin):
        s1 = self.xor2(x, y)
        sm = self.xor2(s1, cin)
        t = self.and2(x, y)
        u = self.and2(cin, s1)
        cout = self.or2(t, u)
        return sm, cout

    def add_words(self, words):
        """words: list of lists of 32 lits, bit 0 = LSB. Sum mod 2^32."""
        acc = words[0]
        for w in words[1:]:
            out = []
            cin = -self.true  # constant 0
            for i in range(32):
                sm, cin = self.full_add(acc[i], w[i], cin)
                out.append(sm)
            acc = out
        return acc

    def const_word(self, k):
        out = []
        for i in range(32):
            bit = (k >> i) & 1
            out.append(self.true if bit else -self.true)
        return out

    def new_word(self, concrete=None):
        out = []
        for i in range(32):
            if concrete is None:
                out.append(self.new(None if not self.check else 0))
            else:
                out.append(self.new((concrete >> i) & 1))
        return out

    def eq(self, a, b):
        for i in range(32):
            self.clause(a[i], -b[i])
            self.clause(-a[i], b[i])

    def eq_const(self, a, k):
        for i in range(32):
            bit = (k >> i) & 1
            self.clause(a[i] if bit else -a[i])

    def bit_eq_const(self, lit, bit):
        self.clause(lit if bit else -lit)

    def bit_eq(self, a, b):
        self.clause(a, -b)
        self.clause(-a, b)

    def word_int(self, w):
        x = 0
        for i in range(32):
            if self.bit(w[i]):
                x |= 1 << i
        return x


def xor_word_from_mask(ckt, xword, mask):
    y = []
    for j in range(32):
        if (mask >> j) & 1:
            y.append(-xword[j])
        else:
            y.append(xword[j])
    return y


def sigma_word(ckt, w, kind):
    if kind == 0:
        r1, r2, sh = 7, 18, 3
    else:
        r1, r2, sh = 17, 19, 10
    out = []
    for j in range(32):
        a = w[(j + r1) % 32]
        b = w[(j + r2) % 32]
        if j + sh < 32:
            out.append(ckt.xor2(ckt.xor2(a, b), w[j + sh]))
        else:
            out.append(ckt.xor2(a, b))
    return out


def Sigma_word(ckt, w, kind):
    rots = (2, 13, 22) if kind == 0 else (6, 11, 25)
    out = []
    for j in range(32):
        a = w[(j + rots[0]) % 32]
        b = w[(j + rots[1]) % 32]
        c = w[(j + rots[2]) % 32]
        out.append(ckt.xor2(ckt.xor2(a, b), c))
    return out


def Ch_word(ckt, e, f, g):
    out = []
    for j in range(32):
        t1 = ckt.and2(e[j], f[j])
        t2 = ckt.and2(-e[j], g[j])
        out.append(ckt.xor2(t1, t2))
    return out


def Maj_word(ckt, a, b, c):
    out = []
    for j in range(32):
        t1 = ckt.and2(a[j], b[j])
        t2 = ckt.and2(a[j], c[j])
        t3 = ckt.and2(b[j], c[j])
        out.append(ckt.xor2(ckt.xor2(t1, t2), t3))
    return out


def not_word(w):
    return [-b for b in w]


def parse_chi_file(path="chi37.txt"):
    A, E, W, x2 = {}, {}, {}, []
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.startswith("row "):
                p = line.split()
                i = int(p[1])
                A[i], E[i], W[i] = p[2], p[3], p[4]
            elif line.startswith("x2 "):
                x2.append(line[3:].strip())
    return A, E, W, x2


def apply_sym(ckt, sym, xw, yw):
    """Pin one characteristic row. '=' and '+' are cross-side equality.
    '0','1','n','u' are exact (x, y) pairs. n = (0,1), u = (1,0), x side first.
    """
    for p, ch in enumerate(sym):
        b = 31 - p
        xb, yb = xw[b], yw[b]
        if ch in ("=", "+", "?"):
            if xb != yb:
                ckt.bit_eq(xb, yb)
        elif ch == "0":
            ckt.bit_eq_const(xb, 0)
            if yb != xb:
                ckt.bit_eq_const(yb, 0)
        elif ch == "1":
            ckt.bit_eq_const(xb, 1)
            if yb != xb:
                ckt.bit_eq_const(yb, 1)
        elif ch == "n":
            ckt.bit_eq_const(xb, 0)
            ckt.bit_eq_const(yb, 1)
        elif ch == "u":
            ckt.bit_eq_const(xb, 1)
            ckt.bit_eq_const(yb, 0)
        else:
            raise RuntimeError(f"bad symbol {ch}")


def apply_plus_links(ckt, rows, X, Y):
    """A '+' bit equals the same bit on a neighbouring row that is also '+'.
    Measured on the characteristic: the 20 '+' marks form 10 consecutive pairs.
    """
    n = 0
    for i, sym in rows.items():
        nxt = rows.get(i + 1)
        if nxt is None:
            continue
        for p, ch in enumerate(sym):
            if ch != "+" or nxt[p] != "+":
                continue
            b = 31 - p
            ckt.bit_eq(X[i][b], X[i + 1][b])
            if Y[i][b] != X[i][b]:
                ckt.bit_eq(Y[i][b], Y[i + 1][b])
            n += 1
    return n


def apply_x2(ckt, conds, X, Y):
    """Two-bit conditions. Both sides are constrained: each held on the
    published pair independently (struct_probe, bad_x = bad_y = 0).
    """
    def atom(side, text):
        name, rest = text.strip().split("[")
        bit = int(rest[:-1])
        reg = name[0]
        idx = int(name[1:])
        return side[reg][idx][bit]

    for cond in conds:
        if "!=" in cond:
            left, right = cond.split("!=")
            differ = True
        else:
            left, right = cond.split("=")
            differ = False
        for side in (X, Y):
            a = atom(side, left)
            b = atom(side, right)
            if a == b:
                if differ:
                    raise RuntimeError(f"x2 differs on one literal: {cond}")
                continue
            if differ:
                ckt.clause(a, b)
                ckt.clause(-a, -b)
            else:
                ckt.bit_eq(a, b)


def apply_characteristic(ckt, Ax, Ay, Ex, Ey, Xx, Xy):
    A, E, W, x2 = parse_chi_file()
    for i, sym in A.items():
        apply_sym(ckt, sym, Ax[i], Ay[i])
    for i, sym in E.items():
        apply_sym(ckt, sym, Ex[i], Ey[i])
    for i, sym in W.items():
        apply_sym(ckt, sym, Xx[i], Xy[i])
    nplus = apply_plus_links(ckt, E, Ex, Ey)
    envx = {"A": Ax, "E": Ex, "W": Xx}
    envy = {"A": Ay, "E": Ey, "W": Xy}
    apply_x2(ckt, x2, envx, envy)
    return nplus, len(x2)


def build(mode, check_mx=None):
    """mode 'msg' or 'full'. If check_mx is the x message, evaluate clauses on it."""
    t0 = time.perf_counter()
    masks = masks_at(B)
    check_bits = None
    if check_mx is not None:
        # flat dict filled after we know var ids; we construct words from concrete
        # values directly inside new_word, so check mode does not need a pre-map.
        check_bits = {}
    ckt = Ckt(check_bits if check_mx is not None else None)

    # Message x. In check mode, load MX.
    Wx = []
    for i in range(16):
        Wx.append(ckt.new_word(None if check_mx is None else check_mx[i]))
    Wy = []
    for i in range(16):
        m = masks.get(i, 0)
        Wy.append(xor_word_from_mask(ckt, Wx[i], m))

    # Expand both sides to W36.
    def expand(W16):
        W = list(W16)
        for i in range(16, 37):
            s1 = sigma_word(ckt, W[i - 2], 1)
            s0 = sigma_word(ckt, W[i - 15], 0)
            W.append(ckt.add_words([s1, W[i - 7], s0, W[i - 16]]))
        return W

    Xx = expand(Wx)
    Xy = expand(Wy)
    for i in range(16, 37):
        if i in (22, 24):
            continue
        ckt.eq(Xx[i], Xy[i])

    named = {"W": Wx, "true": ckt.true}

    if mode in ("full", "bridge", "cond", "low", "anchor", "chi"):
        # Shared prefix state, steps -4..5. Check mode: compute it from the pair.
        if check_mx is not None:
            Ax_i, Ex_i, _, _ = compress_int(CV, check_mx, 25)
            Ay_i, Ey_i, _, _ = compress_int(CV, MY, 25)
        else:
            Ax_i = Ex_i = Ay_i = Ey_i = None

        def concrete_state(arr, idx):
            if arr is None:
                return None
            return arr[idx + 4]

        As = {}
        Es = {}
        for i in range(-4, 6):
            As[i] = ckt.new_word(concrete_state(Ax_i, i))
            Es[i] = ckt.new_word(concrete_state(Ex_i, i))
        Ax = dict(As)
        Ay = dict(As)  # same objects through step 5
        Ex = dict(Es)
        Ey = dict(Es)
        # CV is As[-1]..[-4], Es[-1]..[-4], shared, so the two sides match.

        def step_side(A, E, W, i):
            sig1 = Sigma_word(ckt, E[i - 1], 1)
            ch = Ch_word(ckt, E[i - 1], E[i - 2], E[i - 3])
            Ei = ckt.add_words([A[i - 4], E[i - 4], sig1, ch, ckt.const_word(K[i]), W[i]])
            sig0 = Sigma_word(ckt, A[i - 1], 0)
            maj = Maj_word(ckt, A[i - 1], A[i - 2], A[i - 3])
            # Ai = Ei - A[i-4] + Sig0 + Maj = Ei + ~A + 1 + Sig0 + Maj
            Ai = ckt.add_words([Ei, not_word(A[i - 4]), ckt.const_word(1), sig0, maj])
            return Ai, Ei

        last = {"bridge": 20, "cond": 22, "full": 24, "low": 20, "anchor": 20, "chi": 24}[mode]
        for i in range(0, last + 1):
            if i <= 5:
                # shared, already concrete in check mode; still must be
                # constrained by the step, unless we created them as inputs.
                # For i<=5 the words were created as free inputs (or loaded).
                # Tie them to the step by equating a computed step to them.
                Ai, Ei = step_side(Ax, Ex, Xx, i)
                ckt.eq(Ai, Ax[i])
                ckt.eq(Ei, Ex[i])
            else:
                Aix, Eix = step_side(Ax, Ex, Xx, i)
                Aiy, Eiy = step_side(Ay, Ey, Xy, i)
                Ax[i], Ex[i] = Aix, Eix
                Ay[i], Ey[i] = Aiy, Eiy

        # Window. Zeros are XOR-equality. Cross links are modular.
        # 'bridge' stops at the sparse connection (steps 16..20) and does not
        # force rows 21..24. 'full' forces those rows as well.
        if mode == "bridge":
            zero_e = (16, 19)
            zero_a = (17, 18, 19)
        elif mode == "cond":
            # E17, E18, E20 and A16 are pinned below (they differ).
            # E21 and E22 are equal; the blocker bits are pinned below.
            zero_e = (16, 19, 21, 22)
            zero_a = (17, 18, 19)
        elif mode in ("low", "anchor"):
            # Whole words are pinned below, both sides.
            zero_e = ()
            zero_a = ()
        else:
            zero_e = (16, 19, 21, 22, 23, 24)
            zero_a = tuple(range(17, 25))
        for i in zero_e:
            ckt.eq(Ex[i], Ey[i])
        for i in zero_a:
            ckt.eq(Ax[i], Ay[i])
        # δE18 + δW22 = 0 and δE20 + δW24 = 0 and δA16 + δW24 = 0
        ckt.eq(ckt.add_words([Ex[18], Xx[22]]), ckt.add_words([Ey[18], Xy[22]]))
        ckt.eq(ckt.add_words([Ex[20], Xx[24]]), ckt.add_words([Ey[20], Xy[24]]))
        ckt.eq(ckt.add_words([Ax[16], Xx[24]]), ckt.add_words([Ay[16], Xy[24]]))
        if mode in ("full", "chi"):
            # Step-23 blocker for a one-bit δE20: E22[29]=1, E21[29]=0.
            ckt.bit_eq_const(Ex[22][B], 1)
            ckt.bit_eq_const(Ey[22][B], 1)
            ckt.bit_eq_const(Ex[21][B], 0)
            ckt.bit_eq_const(Ey[21][B], 0)
        if mode == "cond":
            # Sparse-window signed pattern at bit 29 for dW22=017f8000,
            # dW24=20000000 (job108 sufficient set). Difference signs, plus
            # the value bits that the step-function check of the published
            # pair also meets. E18[29]=0 and E19[29]=0 are NOT pinned:
            # that same check fails them, so they are witness-specific.
            def pin_xor(xw, yw, diff):
                """diff: bit -> (xbit, ybit). Every other bit is equal."""
                for j in range(32):
                    if j in diff:
                        xb, yb = diff[j]
                        ckt.bit_eq_const(xw[j], xb)
                        ckt.bit_eq_const(yw[j], yb)
                    else:
                        ckt.bit_eq(xw[j], yw[j])

            pin_xor(Ex[17], Ey[17], {4: (1, 0), 18: (1, 0)})
            pin_xor(Ex[18], Ey[18], {15: (0, 1), 23: (1, 0), 24: (1, 0)})
            pin_xor(Ex[20], Ey[20], {29: (1, 0)})
            pin_xor(Ax[16], Ay[16], {29: (1, 0)})
            # value bits, both sides
            for bit, val in ((4, 1), (15, 0), (18, 1), (23, 0), (24, 0)):
                ckt.bit_eq_const(Ex[19][bit], val)
                ckt.bit_eq_const(Ey[19][bit], val)
            for bit, val in ((2, 1), (10, 0), (11, 0), (15, 1), (16, 0), (23, 0), (24, 1)):
                ckt.bit_eq_const(Ex[20][bit], val)
                ckt.bit_eq_const(Ey[20][bit], val)
            ckt.bit_eq_const(Ex[21][B], 0)
            ckt.bit_eq_const(Ey[21][B], 0)
            ckt.bit_eq_const(Ex[22][B], 1)
            ckt.bit_eq_const(Ey[22][B], 1)
        if mode == "low":
            # Concrete rows from dense_top (12..15) and the anchor (16..20).
            for i in range(12, 16):
                ckt.eq_const(Ax[i], TOP_A[i][0])
                ckt.eq_const(Ay[i], TOP_A[i][1])
                ckt.eq_const(Ex[i], TOP_E[i][0])
                ckt.eq_const(Ey[i], TOP_E[i][1])
        if mode in ("low", "anchor"):
            for i in range(16, 21):
                ckt.eq_const(Ax[i], ANCHOR_X[i][0])
                ckt.eq_const(Ay[i], ANCHOR_Y[i][0])
                ckt.eq_const(Ex[i], ANCHOR_X[i][1])
                ckt.eq_const(Ey[i], ANCHOR_Y[i][1])
        named["A-1"] = As[-1]
        named["A-2"] = As[-2]
        named["A-3"] = As[-3]
        named["A-4"] = As[-4]
        named["E-1"] = Es[-1]
        named["E-2"] = Es[-2]
        named["E-3"] = Es[-3]
        named["E-4"] = Es[-4]
        for i in range(0, last + 1):
            named[f"Ax{i}"] = Ax[i]
            named[f"Ex{i}"] = Ex[i]
            if i >= 6:
                named[f"Ay{i}"] = Ay[i]
                named[f"Ey{i}"] = Ey[i]
        if mode == "chi":
            # Characteristic signs and two-bit links. Not the published words.
            nplus, nx2 = apply_characteristic(ckt, Ax, Ay, Ex, Ey, Xx, Xy)
            print(f"chi_links plus_pairs {nplus} x2 {nx2}")

    dt = time.perf_counter() - t0
    return ckt, named, masks, dt


def compress_int(cv, m, steps):
    W = list(m)
    for i in range(16, 40):
        W.append((sig1_int(W[i - 2]) + W[i - 7] + sig0_int(W[i - 15]) + W[i - 16]) & MASK)
    A = [0] * (steps + 4)
    E = [0] * (steps + 4)
    A[-1 + 4] = cv[0]
    A[-2 + 4] = cv[1]
    A[-3 + 4] = cv[2]
    A[-4 + 4] = cv[3]
    E[-1 + 4] = cv[4]
    E[-2 + 4] = cv[5]
    E[-3 + 4] = cv[6]
    E[-4 + 4] = cv[7]
    for i in range(steps):
        Ei = (A[i - 4 + 4] + E[i - 4 + 4] + Sig1_int(E[i - 1 + 4])
              + Ch_int(E[i - 1 + 4], E[i - 2 + 4], E[i - 3 + 4]) + K[i] + W[i]) & MASK
        Ai = (Ei + ((-A[i - 4 + 4]) & MASK) + Sig0_int(A[i - 1 + 4])
              + Maj_int(A[i - 1 + 4], A[i - 2 + 4], A[i - 3 + 4])) & MASK
        E[i + 4] = Ei
        A[i + 4] = Ai
    return A, E, W, None


def write_cnf(ckt, path, named):
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"p cnf {ckt.n} {len(ckt.clauses)}\n")
        for c in ckt.clauses:
            f.write(" ".join(str(x) for x in c))
            f.write(" 0\n")
    with open(path + ".map", "w", encoding="utf-8") as f:
        for name, obj in named.items():
            if name == "true":
                f.write(f"true {obj}\n")
                continue
            if name == "W":
                for i, w in enumerate(obj):
                    f.write("W%d " % i + " ".join(str(b) for b in w) + "\n")
                continue
            f.write(name + " " + " ".join(str(b) for b in obj) + "\n")


# Concrete O1=5 anchor at bit 29, dW22=017f8000, dW24=20000000.
# Recomputed by dense_probe.build_anchor (ANCHOR_OK). Not read from chi37.txt.
ANCHOR_X = {
    16: (0x20000000, 0x93173B15),
    17: (0x24C75B46, 0x00040010),
    18: (0xC1CB5614, 0x01800000),
    19: (0x00000000, 0x00040010),
    20: (0x01C3D208, 0x21008004),
}
ANCHOR_Y = {
    16: (0x00000000, 0x93173B15),
    17: (0x24C75B46, 0x00000000),
    18: (0xC1CB5614, 0x00008000),
    19: (0x00000000, 0x00040010),
    20: (0x01C3D208, 0x01008004),
}


def step_into(ckt, A, E, W, i):
    sig1 = Sigma_word(ckt, E[i - 1], 1)
    ch = Ch_word(ckt, E[i - 1], E[i - 2], E[i - 3])
    Ei = ckt.add_words([A[i - 4], E[i - 4], sig1, ch, ckt.const_word(K[i]), W[i]])
    sig0 = Sigma_word(ckt, A[i - 1], 0)
    maj = Maj_word(ckt, A[i - 1], A[i - 2], A[i - 3])
    Ai = ckt.add_words([Ei, not_word(A[i - 4]), ckt.const_word(1), sig0, maj])
    return Ai, Ei


def build_top():
    """Connect free rows 8..15 to the concrete sparse anchor.
    No message expansion. W differs only on the algebraic masks.
    """
    t0 = time.perf_counter()
    masks = masks_at(B)
    ckt = Ckt(None)
    Ax, Ay, Ex, Ey = {}, {}, {}, {}
    for i in range(8, 12):
        Ax[i] = ckt.new_word()
        Ay[i] = ckt.new_word()
        Ex[i] = ckt.new_word()
        Ey[i] = ckt.new_word()
    Wx, Wy = {}, {}
    for i in range(12, 21):
        Wx[i] = ckt.new_word()
        m = masks.get(i, 0)
        Wy[i] = xor_word_from_mask(ckt, Wx[i], m) if m else Wx[i]
    for i in range(12, 21):
        Ax[i], Ex[i] = step_into(ckt, Ax, Ex, Wx, i)
        Ay[i], Ey[i] = step_into(ckt, Ay, Ey, Wy, i)
    for i in range(16, 21):
        ckt.eq_const(Ax[i], ANCHOR_X[i][0])
        ckt.eq_const(Ex[i], ANCHOR_X[i][1])
        ckt.eq_const(Ay[i], ANCHOR_Y[i][0])
        ckt.eq_const(Ey[i], ANCHOR_Y[i][1])
    named = {}
    for i in range(12, 21):
        named[f"W{i}"] = Wx[i]
    for i in range(8, 21):
        named[f"Ax{i}"] = Ax[i]
        named[f"Ay{i}"] = Ay[i]
        named[f"Ex{i}"] = Ex[i]
        named[f"Ey{i}"] = Ey[i]
    dt = time.perf_counter() - t0
    return ckt, named, masks, dt


# Rows 12..15 of the dense_top model (kissat, 259 conflicts). Both sides.
# Used as the concrete target for the next downward slice.
TOP_A = {
    12: (0xA5285F19, 0x01245E99),
    13: (0x857F6DF2, 0x7B7AED62),
    14: (0xB265ECA8, 0xB0E66CA8),
    15: (0xCE53DAEC, 0xAE53DAEC),
}
TOP_E = {
    12: (0xE1FEE8F5, 0xBF76FF32),
    13: (0xB5A9C3F7, 0x606B52C7),
    14: (0x9187A178, 0xF2C18C18),
    15: (0x7BD4D7C8, 0x5A9B05B8),
}
TOP_W = {12: 0xFFFF4FBF, 13: 0x7FFDFECA, 14: 0xF2A7A57A, 15: 0x7B23229A}


def build_mid():
    """Steps 8..15. History at 4..7 is free. Rows 12..15 and W12..W15
    are the dense_top model. Masks on W8, W9, W10; W11 equal.
    """
    t0 = time.perf_counter()
    masks = masks_at(B)
    ckt = Ckt(None)
    Ax, Ay, Ex, Ey = {}, {}, {}, {}
    for i in range(4, 8):
        Ax[i] = ckt.new_word()
        Ay[i] = ckt.new_word()
        Ex[i] = ckt.new_word()
        Ey[i] = ckt.new_word()
    Wx, Wy = {}, {}
    for i in range(8, 16):
        if i in TOP_W:
            Wx[i] = ckt.const_word(TOP_W[i])
            Wy[i] = ckt.const_word(TOP_W[i] ^ masks.get(i, 0))
        else:
            Wx[i] = ckt.new_word()
            m = masks.get(i, 0)
            Wy[i] = xor_word_from_mask(ckt, Wx[i], m) if m else Wx[i]
    for i in range(8, 16):
        Ax[i], Ex[i] = step_into(ckt, Ax, Ex, Wx, i)
        Ay[i], Ey[i] = step_into(ckt, Ay, Ey, Wy, i)
    for i in range(12, 16):
        ckt.eq_const(Ax[i], TOP_A[i][0])
        ckt.eq_const(Ay[i], TOP_A[i][1])
        ckt.eq_const(Ex[i], TOP_E[i][0])
        ckt.eq_const(Ey[i], TOP_E[i][1])
    named = {}
    for i in range(8, 12):
        named[f"W{i}"] = Wx[i]
    for i in range(4, 16):
        named[f"Ax{i}"] = Ax[i]
        named[f"Ay{i}"] = Ay[i]
        named[f"Ex{i}"] = Ex[i]
        named[f"Ey{i}"] = Ey[i]
    dt = time.perf_counter() - t0
    return ckt, named, masks, dt


MID_A = {
    8: (0x4277DEB4, 0x3576736D),
    9: (0x123E2B65, 0x96603601),
    10: (0xB81A6CD2, 0x8BD0671C),
    11: (0x315CB560, 0xAE7C564E),
}
MID_E = {
    8: (0x65B05D6C, 0xED36577D),
    9: (0x5F04840E, 0x5002EA38),
    10: (0x2C6CAD9B, 0xC171D648),
    11: (0x0D3AB22C, 0xA1D4D5C2),
}


def build_cv(pin_dense=True):
    """Shared chaining value, steps 0..20, no expansion.
    pin_dense also fixes rows 8..15 to the mid/top model.
    Otherwise only the anchor rows 16..20 are fixed.
    """
    t0 = time.perf_counter()
    masks = masks_at(B)
    ckt = Ckt(None)
    Ax, Ex, Ay, Ey = {}, {}, {}, {}
    for i in range(-4, 0):
        Ax[i] = ckt.new_word()
        Ex[i] = ckt.new_word()
        Ay[i] = Ax[i]
        Ey[i] = Ex[i]
    Wx, Wy = {}, {}
    for i in range(0, 21):
        if i < 16:
            Wx[i] = ckt.new_word()
            m = masks.get(i, 0)
            Wy[i] = xor_word_from_mask(ckt, Wx[i], m) if m else Wx[i]
        else:
            Wx[i] = ckt.new_word()
            Wy[i] = Wx[i]
    for i in range(0, 21):
        if i <= 5:
            Ax[i], Ex[i] = step_into(ckt, Ax, Ex, Wx, i)
            Ay[i], Ey[i] = Ax[i], Ex[i]
        else:
            Ax[i], Ex[i] = step_into(ckt, Ax, Ex, Wx, i)
            Ay[i], Ey[i] = step_into(ckt, Ay, Ey, Wy, i)
    pins_a = {}
    pins_e = {}
    if pin_dense:
        pins_a.update(MID_A)
        pins_e.update(MID_E)
        pins_a.update(TOP_A)
        pins_e.update(TOP_E)
    for i in range(16, 21):
        pins_a[i] = (ANCHOR_X[i][0], ANCHOR_Y[i][0])
        pins_e[i] = (ANCHOR_X[i][1], ANCHOR_Y[i][1])
    for i, (x, y) in pins_a.items():
        ckt.eq_const(Ax[i], x)
        ckt.eq_const(Ay[i], y)
    for i, (x, y) in pins_e.items():
        ckt.eq_const(Ex[i], x)
        ckt.eq_const(Ey[i], y)
    named = {"W": [Wx[i] for i in range(16)]}
    for i in range(-4, 0):
        named[f"A{i}"] = Ax[i]
        named[f"E{i}"] = Ex[i]
    for i in range(0, 21):
        named[f"Ax{i}"] = Ax[i]
        named[f"Ex{i}"] = Ex[i]
        if i >= 6:
            named[f"Ay{i}"] = Ay[i]
            named[f"Ey{i}"] = Ey[i]
    dt = time.perf_counter() - t0
    return ckt, named, masks, dt


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "msg"
    if mode == "cv":
        ckt, named, masks, dt = build_cv(True)
        path = "dense_cv.cnf"
        write_cnf(ckt, path, named)
        print(f"mode cv vars {ckt.n} clauses {len(ckt.clauses)} gen_sec {dt:.2f} file {path}")
        return

    if mode == "cva":
        ckt, named, masks, dt = build_cv(False)
        path = "dense_cva.cnf"
        write_cnf(ckt, path, named)
        print(f"mode cva vars {ckt.n} clauses {len(ckt.clauses)} gen_sec {dt:.2f} file {path}")
        return

    if mode == "top":
        ckt, named, masks, dt = build_top()
        path = "dense_top.cnf"
        write_cnf(ckt, path, named)
        print(f"mode top vars {ckt.n} clauses {len(ckt.clauses)} gen_sec {dt:.2f} file {path}")
        return

    if mode == "mid":
        ckt, named, masks, dt = build_mid()
        path = "dense_mid.cnf"
        write_cnf(ckt, path, named)
        print(f"mode mid vars {ckt.n} clauses {len(ckt.clauses)} gen_sec {dt:.2f} file {path}")
        return

    if mode == "check":
        masks = masks_at(B)
        print("masks", {k: f"{v:08x}" for k, v in masks.items()})
        bad = 0
        for i, m in masks.items():
            if (MX[i] ^ MY[i]) != m:
                bad += 1
                print(f"  XOR mismatch W{i} got {MX[i]^MY[i]:08x} mask {m:08x}")
        print("xor_mismatches", bad)
        Ax, Ex, Wx, _ = compress_int(CV, MX, 25)
        Ay, Ey, Wy, _ = compress_int(CV, MY, 25)
        print("dW22", f"{(Wy[22]-Wx[22])&MASK:08x}", "dW24", f"{(Wy[24]-Wx[24])&MASK:08x}")
        print("dE16", f"{(Ey[16+4]-Ex[16+4])&MASK:08x}",
              "dE18", f"{(Ey[18+4]-Ex[18+4])&MASK:08x}",
              "dE20", f"{(Ey[20+4]-Ex[20+4])&MASK:08x}",
              "dA16", f"{(Ay[16+4]-Ax[16+4])&MASK:08x}")
        # Clause check on the published x message, message circuit only,
        # then full. A raised RuntimeError means a wrong gate.
        print("building msg circuit on the published x message...")
        ckt, named, masks, dt = build("msg", check_mx=MX)
        print(f"MSG_CHECK_OK vars {ckt.n} clauses {len(ckt.clauses)} sec {dt:.2f}")
        print("building full circuit on the published pair...")
        ckt, named, masks, dt = build("full", check_mx=MX)
        print(f"FULL_CHECK_OK vars {ckt.n} clauses {len(ckt.clauses)} sec {dt:.2f}")
        print("building bridge circuit on the published pair...")
        ckt, named, masks, dt = build("bridge", check_mx=MX)
        print(f"BRIDGE_CHECK_OK vars {ckt.n} clauses {len(ckt.clauses)} sec {dt:.2f}")
        print("building cond circuit on the published pair...")
        ckt, named, masks, dt = build("cond", check_mx=MX)
        print(f"COND_CHECK_OK vars {ckt.n} clauses {len(ckt.clauses)} sec {dt:.2f}")
        print("building chi circuit on the published pair...")
        ckt, named, masks, dt = build("chi", check_mx=MX)
        print(f"CHI_CHECK_OK vars {ckt.n} clauses {len(ckt.clauses)} sec {dt:.2f}")
        return

    if mode not in ("msg", "full", "bridge", "cond", "low", "anchor", "chi"):
        print("usage: dense_sat.py check|msg|full|bridge|cond|low|anchor|top|mid|chi")
        return
    ckt, named, masks, dt = build(mode, check_mx=None)
    path = {
        "msg": "dense_msg.cnf",
        "full": "dense_full.cnf",
        "bridge": "dense_bridge.cnf",
        "cond": "dense_cond.cnf",
        "low": "dense_low.cnf",
        "anchor": "dense_anchor.cnf",
        "chi": "dense_chi.cnf",
    }[mode]
    write_cnf(ckt, path, named)
    print(f"mode {mode} vars {ckt.n} clauses {len(ckt.clauses)} "
          f"gen_sec {dt:.2f} file {path}")
    print("masks", " ".join(f"W{k}={v:08x}" for k, v in sorted(masks.items())))


if __name__ == "__main__":
    main()
```

## Appendix H. Memory, charges, the upper bound on q3, sensitivity tables, measurements

### H.1 What is a premise

**Nothing else in the claim is heuristic.** The operation counts and the ledger (Sections 9, 11 and Appendix B), the exactness of the filters F6 and F7, of the classes and of the row-16 test (Section 13.2, Appendix A), the success arithmetic (Section 10, Appendix C) and the cap are computed or checked exhaustively. The premises are H1, H2, H3 (probability), H4 (the charges of the construction), H5 (pricing), H6 (the memory bound) and H7 (the success floor), all in claim.heuristics. The answers to the ruling on 68f33bc4 are in Appendix M.

### H.2 Memory: a bound of 2^33 bytes over all phases and development runs

**Memory bound.** The procedure runs these phases: the construction of the characteristic P_C (generation of the SAT instance, its CNF dump, the solver search), the construction of S P_S (generation of the pair instance, the solver search, the decoding), the preprocessing P_F (Section 14.2) and the online phase. Its peak memory, with every development run, is declared at most 2^33 = 8,589,934,592 bytes (H6). The claimed memory_log2_bytes is 33, so the score is time_log2 + (33 - 20) = 58.98394 + 13 = 71.98394.

| phase | bound (bytes) | how | measured peak (bytes) | evidence file |
|---|---:|---|---:|---|
| online: tables, code, constants | 12,676,416 | computed | - | Section 14.1 (`lowm.py memory`) |
| P_C: gen37.py (LLW24 FunctionModel, 37 steps), dense_pub.cvc | 536,870,912 (2^29) | `prlimit --as` cap (P12 runs); cloud run uncapped | 100,712,448 (2^26.58) locally; 97,816 KB on the cloud | premise_tests/P12/logs_zf5/gen.time; r37char/gen37.time |
| P_C: translation to SMT2 (sha256 d1c1976d...68cc) | 536,870,912 (2^29) | same | 99,696,640 (2^26.57); 97,712 KB on the cloud | logs_zf5/shim.time |
| P_C: STP 2.4.1 CNF dump (200,534 variables, 954,732 clauses; sha256 445a880e...42f4) | 536,870,912 (2^29) | `prlimit --as` cap (P12), identical in 4 runs; fails under 2^28 | 499,384,320 (2^28.895); 500,424,704 (2^28.899) on the cloud | logs_zf5/stpcap29.time; r37char/RUN.md |
| P_C: kissat 4.0.4, 8 seeds to completion (seed 4: 81,652 KB) | 379,625,062 (2^28.5) | `prlimit --as` cap | resident set at most 83,820,544 (2^26.32) | r37char/out/seed1..8.time |
| P_S: dense_sat.py chi (107,359 variables, 373,031 clauses) | 536,870,912 (2^29) | `prlimit --as` cap | 72,527,872 (70,828 KB) | step2/pre_cloud/cnfgen.time |
| P_S: kissat 4.0.4 seeds 1 and 2 on that CNF (SAT) | 379,625,062 (2^28.5) | `prlimit --as` cap | 65,708,032 (64,168 KB) and 84,579,328 (82,596 KB) | step1/out/H3s4_seed1.time, H3s4_seed2.time |
| P_F: gscan.c | 536,870,912 (2^29) | `prlimit --as` cap | 1,957,888 (1,912 KB) | cloud_out/pre/gscan.time |
| P_F: grp.c | 536,870,912 (2^29) | `prlimit --as` cap | 352,547,000 (344,284 KB; 2^28.4) | cloud_out/pre/grp.time |
| P_F: lscan.c | 536,870,912 (2^29) | `prlimit --as` cap | 136,179,712 (132,988 KB) | cloud_out/pre/lscan.time |
| development: kissat 4.0.4 on the Step-1 diagnostics (H3 control 104,160 KB) and on the dense instance with rows 16..24 free (264,266 variables; open runs, address space at most 187,252 KB) | at most 268,435,456 (2^28) | measured (resident set, address space) | 191,746,048 (2^27.52) | step1/out/*.time; cloud /proc/PID/status |
| P_F: stats.c | 8 GiB address cap | `prlimit --as` | 1,695,744 (1,656 KB) | cloud_out/pre/stats.time |
| q3 study `smc_s4`, 144 seeds, 4 processes at a time (Appendix F) | 402,653,184 (cgroup MemoryMax, no swap) | `systemd-run --scope -p MemoryMax=402653184 -p MemorySwapMax=0` | aggregate of the scope, driver included: sum of the resident sets of all 11 processes alive together, sampled every 0.2 s, maximum 338,391,040 (2^28.33); cgroup memory.peak 304,959,488 (2^28.18); largest single process of the run 76,800,000; one process alone 75,403,264 (seed 40001) and 63,315,968 (seed 60001) | smc_raw_p4/mem_cgroup.txt, mem_sampled.txt |

**Aggregate peaks of the development runs** (sum of the peak resident sets of the processes of one launch that were alive together):

| development run | processes alive together | aggregate peak (bytes) |
|---|---:|---:|
| q3 study, this filing (4 at a time, one cgroup) | 4 | 338,391,040 (2^28.33) |
| q3 study, first run (12 at a time; same seeds, same outputs byte for byte) | 12 | 12 x 75,403,264 = 904,839,168 (2^29.75) |
| A_C, 8 kissat seeds (Appendix L), launched together | 8 | 594,068 KB = 608,325,632 (2^29.18) |
| Step-1 diagnostics H1/H2 (5 kissat runs, 0.04 to 18 s) | 5 | 289,312 KB = 296,255,488 (2^28.14) |
| Step-1 diagnostics H3 (4 kissat runs; includes the two A_S seeds) | 4 | 340,100 KB = 348,262,400 (2^28.38) |
| dense instance with rows 16..24 free (4 kissat seeds, open) | 4 | 557,520 KB = 570,900,480 (2^29.09), read 2026-10-17T01:15:30Z |
| counted-program checks, Python (`cal1`..`cal6`, `online`, `onlineall`, `sfs`, `family`, `memory`; largest single process 2,440,436 KB) | up to 6 | 6,816,468 KB = 6,980,063,232 (2^32.70) |
| scans gscan, grp, lscan, stats; local runs | 1 | largest 344,284 KB (grp); local runs not metered |

The bounds of the online phase and of the table construction are computed; the generator, dump and solver phases run under their caps; the peaks are our measurements. The claim is 2^33 because the Python counted-program checks of the development aggregate 2^32.70 bytes.

### H.3 The charges

| charge | CPU-seconds | units | log2 |
|---|---:|---:|---:|
| A_C (8 x 4,044 + 29.45) | 32,381.45 | 91,298,997,556 | 36.41 |
| A_S (2 x 2,188.09 + 0.37) | 4,376.55 | 12,339,615,049 | 33.52 |
| PRE (measured 75.48, charged 90) | 90 | 253,753,608 (= 670,924,540,390 word operations at C = 2644) | 27.9 (39.3 as operations) |
| DEV | - | 2^42 | 42 |

The conversion is 2^21.427 units per CPU-second at C = 2644, the price calibrated by 6eeefb64 on its complete re-run of the predecessor 35-step search (593,858 CPU-seconds). The effect of each charge on the claim is in H.5: the claim moves by less than 0.0001 bit if A_C or A_S is 2^44 units.

### H.4 The upper bound on q3 (used by H3 only)

H3 (b) uses an upper bound on q3. The preregistered rule of Section 7.4 produces lower bounds only. From the 64 replicate estimates of each of S1 and S2 (Appendix F.2) we compute here, for the mean of each set, the one-sided 99 percent **upper** Student bound mean + t(0.99, 63) sd / sqrt(64), t = 2.3870, and a percentile bootstrap upper bound (20,000 resamples of the 64 linear estimates, `random.Random(12345)`).

| set | mean (log2) | relative sd | skewness | Student lower / upper (log2) | bootstrap lower / upper (log2) | largest replicate (log2) |
|---|---:|---:|---:|---|---|---:|
| S1 | -70.2581 | 0.091 | 0.31 | -70.2979 / -70.2192 | -70.2960 / -70.2203 | -69.973 |
| S2 | -70.2885 | 0.116 | 0.15 | -70.3394 / -70.2394 | -70.3378 / -70.2418 | -69.976 |

Both lower bounds reproduce the values of Section 7.4. The larger upper bound is **2^-70.2192**, so q3 <= 2^-70.21 (rounded up to two decimals). H3 (b) is at most 2^35 x 2^22.06 x 2^5.46 x 2^-70.21 = 2^-7.69 and delta <= 2^-11 + 2^-7.69 = 2^-7.5502, below the declared 2^-7.5 with 0.05 bit to spare; the break-even q3 is 2^-70.15, 0.06 bit above the bound. The bound is the one-sided 99 percent Student bound of the mean of the 64 replicates of each set; the estimator is importance-weighted and agrees with the exact row-16 counts of stats.c and with the earlier study of the published pair. The bootstrap agrees with Student to 0.002 bit and the skewness is 0.15 to 0.31.

```python
import re, math, random
def load(lo, hi):
    out = []
    for s in range(lo, hi + 1):
        t = open('smc_raw/out_%d.txt' % s).read()
        n, e = (int(x) for x in re.search(r'n (\d+) stage22cells \d+ cellevent \d+ exact (\d+)', t).groups())
        out.append(2 ** float(re.search(r'RESULT seed \d+ log2est21 (\S+) ', t).group(1)) * e / n)
    return out
for lo, hi in ((40001, 40064), (50001, 50064)):
    Q = load(lo, hi); k = len(Q); m = sum(Q) / k; sd = (sum((q - m) ** 2 for q in Q) / (k - 1)) ** .5; se = sd / k ** .5
    rnd = random.Random(12345); bm = sorted(sum(rnd.choice(Q) for _ in range(k)) / k for _ in range(20000))
    print(math.log2(m - 2.387 * se), math.log2(m + 2.387 * se), math.log2(bm[200]), math.log2(bm[19799]))
```

### H.5 Sensitivity tables

Computed from the ledger (the H2, H3 and charge rows by `ledger()` of `experiments/lowm.py`, the H1 rows by scaling the attack term T - (A_C + A_S + DEV)).

**H1.** If the expected number of good pairs per first block is (1 - eps) of g, the number of first blocks, and with it the attack term, grow by 1/(1 - eps). This ignores the per-pair work saved, so it is an upper estimate.

| eps | 0 | 0.01 | 0.05 | 0.10 | 0.25 |
|---|---:|---:|---:|---:|---:|
| time_log2 that keeps 0.39 | 58.98394 | 58.99844 | 59.05794 | 59.13594 | 59.39898 |

**H2.** If the true q3 (the exact event) is 2^b below q3_used = 2^-70.34.

| b | 0 | 0.5 | 1 | 2 | 4 |
|---|---:|---:|---:|---:|---:|
| time_log2 that keeps 0.39 | 58.98394 | 59.47286 | 59.96490 | 60.95514 | 62.94771 |

A q3 above q3_used lowers the cost. The upper bound of H.4 gives nothing back, because the claim does not use it; it enters only H3.

**H3.** delta enters through the divisor 1 - delta/2 of the success floor (Section 10); filed delta = 2^-7.5.

| delta | 2^-7.5 (filed) | 2^-6 | 2^-4 | 0.1 | 0.25 |
|---|---:|---:|---:|---:|---:|
| time_log2 | 58.98394 | 58.99108 | 59.02468 | 59.05217 | 59.16798 |

**Joint.** q3 one bit lower, good-pair rate 10 percent lower and delta = 2^-4 together: time_log2 60.15816 (score 73.15816 with the memory term 13.0).

**Charges (H4), all other terms as filed.** A_C: 2^36.41: 58.98394, 2^40: 58.98394, 2^44: 58.98399, 2^48: 58.98465, 2^50: 58.98679, 2^56: 59.15566, 2^60: 60.57963. A_S: 2^33.52: 58.98394, 2^40: 58.98394, 2^44: 58.98399, 2^50: 58.98679. DEV: 2^40: 58.98393, 2^42: 58.98394, 2^44: 58.98397, 2^46: 58.98411, 2^50: 58.98678. PRE at 90, 900, 9,000 and 90,000 CPU-seconds: 58.98394, 58.98394, 58.98394, 58.98394.

**Memory term (score = time_log2 + memory_log2_bytes - 20).** Bound 2^33: 71.98394 (claimed). Largest measured aggregate 2^32.70: 71.68. A bound of 2^32 would not hold (the Python counted-program checks aggregate 2^32.70 bytes).

### H.6 Calibration of the ledger against the counted program (our runs)

`run_cal.py N TAG` (the program of `tests/`; seeds `s4cal<TAG>|<t>`): N real first blocks, all passing classes, no checks; counted operations per first block against the ledger FIXED + vbar = 402,383.

| run | first blocks | mean counted ops | standard error | ratio to ledger | passing classes per fb | good pairs per fb |
|---|---:|---:|---:|---:|---:|---:|
| cal1 | 2500 | 374320.6 | 18211.3 | 0.93026 | 16.186 | 4227.7 |
| cal2 | 2500 | 406519.9 | 19475.0 | 1.01028 | 17.618 | 4566.8 |
| cal3 | 2500 | 408557.6 | 19484.2 | 1.01535 | 17.084 | 4742.0 |
| cal4 | 7000 | 412690.5 | 12105.6 | 1.02562 | 17.344 | 4767.5 |
| cal5 | 7000 | 404005.8 | 12069.8 | 1.00403 | 16.975 | 4674.1 |
| cal6 | 7000 | 401166.6 | 12101.1 | 0.99698 | 17.009 | 4598.4 |

Pooled: 28,500 first blocks, mean 403,457, ratio 1.003 to the ledger (standard error 1.5%).

### H.7 The organizer experiments

The experiment budget is 65,536 bytes in total; `lowm.py` uses 57,556 and `nonce_h1h3.py` 1,757 (59,313 together). The entries `h1-cv1-filters-nonce` and `h3-cowpass-nonce` share the program `experiments/nonce_h1h3.py`. Each trial takes 150 first blocks from the organizer's trial seed (SHAKE-256 of seed and counter), computes the real 37-step compression (the program computes its 37 round constants as integer cube roots of the first 37 primes), and tests, for the first class of the family (c7 = 716a554f) and four of its variants (ee534104, ee534107, ee53410c, ee53410f), whether W7x = c7 - x is in F7 and W6x is in F6 (the filters of Section 5.1 in their definition form). It returns no message pair, so the event full-collision never succeeds by design. Observations: first blocks, W7 passes, W6 passes over the four variants, first blocks in which two or more variants pass F6, first blocks with both a W7 pass and a W6 pass, and the sum over those blocks of the number of variants passing. The entry `h1-cv1-filters-nonce` is the H1 consequence (the pass rates of the two filters on real chaining values: p7 = 2^-5.98 per class and p6 = 2^-3.90 per variant); the entry `h3-cowpass-nonce` reports the number of first blocks in which two or more of the four variants of one class pass F6. The variants of one class share most of their bits, so a count clearly above the independent value is expected; it measures the within-class correlation of the W6 filter, which the ledger does not need (it uses only expectations). The program was cross-checked against `lowm.py` on two trials (identical counts). Scope: the organizer's report keeps the message pairs it can check against the target; these programs return none, so their counts are program checks that anyone can replay. q3 is the study of Section 7.4; rows beyond the W6 filter and independence across first blocks are H3 and H1. The entry `h3-ladder-r37` (same program `lowm.py`, function `ladder_trial`; trials 0..15) is the H3 experiment at depth. Each trial scans the organizer's seed for four first blocks with at least two passing classes among the classes 0..15 (a fixed choice made before any run) and, over the variants of up to four of those classes, counts in turn the passes of F6, of the low and of the middle chunk table of the row-16 address, and of the exact row-16 test. Per level it reports the passes S and the pairs P of distinct passing variants of one first block (the candidates N and C, the sum of C(N,2) over the blocks, are the passes and pairs of the level before; for W6 they are w6_cand and w6_candpairs); the independent reference is E = C (S/N)^2 and the dependence factor R = P/E. Our replays of the 256-trial request (our seed sets 12345 and 777, and the organizer runner's own run of the staged package; 7 s each, identical on repetition): W6 R = 2.77, 2.55 and 2.44 (S = 63,820, 81,832 and 94,376); low table 0.99, 1.00 and 1.00; middle table 0.99, 1.02 and 1.00; exact row 16 1.25, 1.13 and 0.71 (S = 35, 58 and 63 of 9,471, 12,241 and 14,104; 33, 78 and 54 pairs against 26.5, 69.1 and 76.3). The returned pair is a generic witness (a second message with a counter word, found by search, whose digest agrees in 4 bits; event digest-xor-mask 0x0f), returned only by trials with a row-16 co-pass, so that the count of successes in the organizer's report is the number of those trials; it carries no cryptographic weight and the statistics are the observations. Scope: the levels end at the exact row-16 test; rows 17..36 of distinct good pairs are the allowance rho of H3.

## Appendix L. The run records of P_C (the 37-step dense model, eight kissat seeds)

Instance: the P12 pipeline of the 37-step dense model on the cloud machine (AMD EPYC Turin, 32 vCPU, shared; Ubuntu): `gen37.py dense_pub.cvc --chi chi37.txt --fix 16-24 --fixw 22,24 --W 25 --O2 7 --O3 25 --E 63` (the unmodified LLW24 FunctionModel; chi37 sha256 a13112c7...67f4, the cells of rows 16..24 and of W22, W24), `stp_cvc_shim.translate` to SMT2, `stp dense_pub.cvc.smt2 --output-CNF --exit-after-CNF` (STP 2.4.1). Hashes: dense_pub.cvc ae255eca184194d3f23c75f5e222ac2bbee6b3abad76851747f99e029429b520, dense_pub.cvc.smt2 d1c1976d206c0b22346ec475143fb86fe44cad5eac5986ecff572b7df21a68cc, dense_pub.cnf 445a880e5881fb0482f73c98922ee77b8db6e5f05d1e4c9ddf0d9e93b66b42f4 (200,534 variables, 954,732 clauses). Setup, user seconds / maximum resident set: gen37 7.63 s / 97,816 KB, translation 3.34 s / 97,712 KB, STP dump 18.48 s / 488,696 KB (500,424,704 bytes, 2^28.899); 29.45 s in all.

Solver: kissat 4.0.4 (binary sha256 4ebc02c3e4f5fe6ba448aec14b935fa6d2be9aff121ad4ad5015b3df8a256710), defaults, `--seed=k --time=172800`, one thread each, eight processes started together at 2026-10-16 17:04:55 UTC, for k = 1..8: `setsid nohup nice -n 10 prlimit --as=379625062 /usr/bin/time -v -o out/seedk.time /root/hs/bin/kissat --seed=k --time=172800 /root/r37char/dense_pub.cnf > out/seedk.out 2>&1 < /dev/null &` (379,625,062 = floor(2^28.5) bytes of address space). Other jobs ran on the machine (load average about 10), so wall time is at least CPU time for every seed.

**Results (all eight completed; `s SATISFIABLE`, exit status 10, no seed stopped by the cap or the time limit):**

| seed | user s | system s | CPU s | wall | max resident set (KB) | sha256 of seedk.out / seedk.time (first 16) |
|---:|---:|---:|---:|---:|---:|---|
| 1 | 1042.36 | 0.98 | 1043.34 | 17:25.17 | 79,104 | 9e7d473b6b717154 / 2105dd87ffd02164 |
| 2 | 1177.50 | 0.33 | 1177.83 | 19:41.34 | 77,928 | eede8a606a4f1a3e / 476a5a1a88ca7e4c |
| 3 | 463.68 | 0.11 | 463.79 | 7:44.03 | 57,252 | 6d1913e82fd6c08c / b8076fed558b238b |
| **4** | **4039.31** | **1.42** | **4040.73** | **1:07:24** | **81,652** | **9b292d1e98509eac / b8d3efd01e50572e** |
| 5 | 456.35 | 0.37 | 456.72 | 7:37.01 | 73,412 | 6f29eb2d8b78af0d / 88964cc001b543c0 |
| 6 | 859.80 | 0.48 | 860.28 | 14:22.43 | 81,856 | 3e02569602666e3b / a8557313b62cfca4 |
| 7 | 991.92 | 0.59 | 992.51 | 16:35.29 | 70,048 | ab40ce06760aa54a / 4a690e5c2fb3c5f9 |
| 8 | 883.31 | 0.84 | 884.15 | 14:47.81 | 72,816 | e186b3b279ebf5fb / 8f28fce9d9abbc86 |

**Charge.** The characteristic of this filing is the model of seed 4 (Section 11.2). The eight seeds used 9,919.35 CPU-seconds in all until each finished; the procedure that runs the eight and takes the model of seed 4 is charged eight times the wall time of seed 4, 8 x 4,044 = 32,352 CPU-seconds, plus the setup 29.45 s: 32,381.45 CPU-seconds x 2^21.427 = 91,298,997,556 units (2^36.41). The price is 2^21.427 units per CPU-second at C = 2644, the one of 6eeefb64.

**Checks of the models.** (1) Every model against the CNF (`verify_sat.py`: reads the `v` lines of seedk.out and the file, checks every clause): seeds 1..8 each "OK model_vars=200534 clauses=954732 all satisfied". (2) Decoding. STP's CNF dump cannot map variables back, so a read-only hook was added to the local STP build (`STP_VARMAP=file`: after the CNF conversion `lib/ToSat/ToSATAIG.cpp` writes each symbol with its DIMACS variables; 14 lines, no other change); the dump of the same SMT2 is byte-identical (sha256 445a880e...42f4) and the map lists 19,158 symbols. For each seed the 2,888 dense-model bits that have a variable are read from the model, asserted in the CVC model, and the repo's own backend (`stp_cvc_shim.py`, STP 2.4.1) completes the bits that the simplifier had substituted away; all eight answer sat and `decode_stp.py` prints "weights A=25 E=63 W=25 forbidden(v=1,d=0)=0" for every seed: the signed-difference weights meet the model's bounds A <= 25 (rows 6..24), E <= 63, W = 25. The decoded characteristics are written as `seedk.full.chi`; seed 4 differs from the published signed cells in E6[31], two signs of W9 and one sign of W10 and in no other cell of rows 6..15; its message XOR masks and the modular differences of W6, W7, W8, W14, W15, W22, W24 are the published ones. Seeds 4 and 7 have the XOR masks that the generator of P_S encodes; seed 5 differs in the modular difference of W8 (+2^29) and of W14, in the masks of W9, W10, W14.

## Appendix M. The ruling on 68f33bc4 (R37OWN)

**What changed vs e7176757-17f7-411b-83bd-fb13d0efc12d (our R37OWN2), ruled F-COST-MEMORY-SMC-PARALLEL (fatal, lane_cost):** "The 2^29-byte memory bound omits aggregate concurrent storage of the q3 development run." The q3 study was rerun with the same program, seeds and analysis at 4 processes at a time in one cgroup (MemoryMax 402,653,184 bytes): aggregate peak 338,391,040 bytes = 2^28.33, and all 144 outputs equal those of the first run byte for byte (Appendix F, Appendix H.2). The memory claim is now 2^33 bytes (score 71.98394), covering every development run in the table of Appendix H.2. Nothing else changed.

68f33bc4 (the same attack, program, ledger, experiments and numbers as this filing) was ruled not_evaluable on H2, H3 and H4 in lane_evaluability, with no fatal finding. This filing changes the statements of the premises (Section 12, claim.heuristics) and this appendix. The findings, by id:

| finding id | premise | answer | where |
|---|---|---|---|
| F-EVAL-H2-EXECUTION-GAP, F-EXP-H2-UNTRUSTED-REPLAY | H2 | The q3 interval is the preregistered study of Section 7.4: the estimator source, `PREREG_s4.md`, the analysis program and all 144 per-seed estimates are printed in Appendix F, so it replays from this text. `a0-sfs-r37` builds real 37-step semi-free-start collisions with the same end event. | Section 7.4, Appendix F |
| F-CRYPT-H2-PARTICIPANT-SMC, F-SUCCESS-H2-COVERAGE, F-EXP-SMC-COVERAGE | H2 | Student bounds over 64 replicates per set (one per seed); duplicated descendants are within a replicate. The percentile bootstrap (20,000 resamples) agrees to 0.002 bit and the skewness is 0.31 and 0.15. The row-16 stage equals the exact counts of `stats.c`; 40 of 40 hits are real collisions; the same source reproduces a filed output for the published pair bit for bit. | Section 7.4, Appendix H.4 |
| F-EXP-TARGET-SCOPE | H2 | The event of q3 is the second-block event from a good pair (Section 7.1), a semi-free-start collision from CV1; `a0-sfs-r37` builds such collisions. The first block that produces CV1 is H1 and H3. | Sections 7.1, 10 |
| F-SUCCESS-H3-LATE-DEPENDENCE, F-CRYPT-H3-LATE-ROUND-DEPENDENCE, F-EVAL-H3-LATE-ROUND-GAP | H3 | H3 is the allowance rho <= 2^35 for the dependence of two good pairs of one first block: (a) 0 further successes among 19,620,436 replayed Step-3 successes; (b) rho x N_good x 44 x q3 with the measured row-16 factor 0.98 and 1.00 and q3 <= 2^-70.21, giving delta <= 2^-7.55 against the declared 2^-7.5. `h3-cowpass-nonce` counts the W6-level co-passes on real first blocks and `h3-ladder-r37` the co-passes of distinct variants through the exact row-16 test (factors 0.71 to 1.25, Appendix H.7). | Section 10, 13.1, Appendix H.4, H.5 |
| F-COST-CALIBRATION, F-EVAL-RESOURCE-VALIDATION, F-EXP-RESOURCE-VALIDATION | H4 | A_C, A_S and PRE are the CPU-seconds of the completed runs of Appendix L (hashes, models verified against the CNF, kissat deterministic) at the price of 6eeefb64. The claim moves by under 0.0001 bit if A_C (about 190 times larger) or A_S (about 1,400 times larger) is 2^44 units; DEV = 2^42 covers the development 3.4 times. | Section 11.2, 13.4, Appendices H.3, H.5, L |
| F-SUCCESS-H1-SCALE, F-CRYPT-H1-FULL-SCALE, F-EVAL-H1-SCALE-GAP, F-EXP-H1-H3-COVERAGE | H1 | Unchanged: the filter rates measured on 2^21, 2^23 and 2.85 x 10^4 real first blocks (Sections 13.1, 13.3), applied by the attack at 2^51.7. | Sections 12, 13 |
| F-COST-ABSTRACT-IMPLEMENTATION, F-COST-RETAINED-STORAGE | H5, H6 | Unchanged. | Sections 9, 12, 14, Appendix H.2 |

## Appendix N. The ruling on 28ffb638 (R37OWN4)

**What changed vs 28ffb638-2f8f-4575-88f2-3e73d302a586 (our R37OWN4), ruled not_evaluable (no fatal finding):** the organizer experiment `h3-ladder-r37` is added (Appendix H.7) and the premises H2, H3 and H4 state their limits (claim.heuristics; Section 12). The attack, program logic, ledger, numbers and the other experiments are unchanged.

Each finding is quoted by its first sentence and answered.

| finding id | premise | quoted | answer |
|---|---|---|---|
| F-CRYPT-H2-SMC-COVERAGE | H2 | "The score-critical lower bound q3 >= 2^-70.34 is derived from participant-run SMC and Student coverage assumptions." | H2 is our theory (Section 7.4, Appendix F, H.4); the organizer-run `h3-ladder-r37` reproduces the row-16 stage of q3 on organizer seeds (6.5e-4 against 6.74e-4); the end event is not reachable at reduced scale (limitations of H2). |
| F-EVAL-H2-NO-ORGANIZER-EXECUTION | H2 | "The score-critical q3 interval is based on participant-reported SMC executions." | As above: stated premise; the row-16 stage runs in the organizer sandbox, rows 22..36 need the attack itself. |
| F-EXP-CORE-SMC-NOT-ORGANIZER-EXECUTED | H2 | "The score-critical q3 interval is based on a participant-run SMC study rather than an organizer execution." | As above; the SMC replays from the printed source (Appendix F). |
| F-SUCCESS-FULL-SCALE-EXTRAPOLATION | H1/H2 | "The fixed N_FB and hence both time and success bounds depend on extrapolating H1 and the participant-run H2 study to the full attack." | H1: unchanged (Sections 13.1, 13.3). H2: as above. |
| F-SUCCESS-H3-LATE-DEPENDENCE | H3 | "H3's decisive late-round dependence allowance is not directly tested for distinct good pairs of this family." | New organizer experiment `h3-ladder-r37`: distinct variants of one first block through the exact row-16 test, factors 0.71 to 1.25 (Appendix H.7); rows 17..36 are the stated allowance rho = 2^35. |
| F-CRYPT-H3-LATE-DEPENDENCE | H3 | "The claimed rho <= 2^35 allowance for late-round dependence between distinct good pairs of the same first block is not directly tested for the submitted family and event." | As above. |
| F-EVAL-H3-LATE-ROUND-SCOPE | H3 | "The organizer H3 experiment measures only W6-level co-passes and expressly does not test row 16 or later rounds, while H3's decisive rho=2^35 allowance concerns dependence through the late-round collision event." | As above: the organizer experiment now runs past W6 to the exact row-16 test. |
| F-EXP-H3-LATE-ROUND-GAP | H3 | "No supplied organizer experiment tests H3's decisive dependence among distinct good pairs through rows 17–36 for this family." | As above; rows 17..36 are not reachable in 20 s and are stated as the premise H3. |
| F-COST-CPU-SECOND-CONVERSION | H4 | "Construction and preprocessing are priced by transferring a CPU-second calibration from another filing rather than by a direct upper bound in v5 primitive operations." | Stated premise H4: CPU-seconds of completed runs at the price of 6eeefb64; under 0.0001 bit if A_C or A_S is 2^44 units (Appendix H.5). |
| F-EVAL-H4-CONSTRUCTION-COST-EXECUTION | H4 | "The P_C, P_S, and P_F CPU times and inherited CPU-second conversion are participant-reported." | As above; the runs do not fit the organizer sandbox. |
| F-EXP-RESOURCE-RUNS-UNVALIDATED | H4/H5/H6 | "The organizer report makes no attack-cost inference and did not execute the characteristic search, Step-1 solver, preprocessing pipeline, full counted attack, or peak-memory studies." | H4: as above. H5, H6: unchanged (Sections 9, 14, Appendix H.2). |

H1, H5, H6 findings (F-COST-ABSTRACT-OPERATION-PRICING, F-CRYPT-H1-SCALE, F-EXP-H1-SCALE-GAP, F-MEMORY-COVERAGE): unchanged.
