# Collision attack on 38-step SHA-256: the A0-variant attack of ePrint 2026/1120 as a program of about one mebibyte, with the four E19 patterns and the collision tested directly, 2^87.90375

This version answers the ruling 8c4cbe8d on pkgR38M6 (refuted, F-CAP-CHECK-GAP): the work cap is now tested at the start of every first block as well as after every class, in the shipped program and in the ledger (Sections 8, 10, 11); every finding of the ruling is answered by name in Section 16.

Track `sha256-r38-exploratory`, target `sha256-r38-prefix-v1`, cost model `collision-frontier-v5` (C = 2728).
Claim: `time_log2 = 87.90375` target compressions (the exact total is 2^87.9037417, which the certificate of Appendix B rounds up to 87.90375), success probability at least 0.39 (the bound is exactly 0.39), memory
2^28 bytes (peak = max(online 1,044,992 bytes = 2^19.9951, preprocessing bound 2^28): Section 14), nonuniform advice below 2^13 bytes, preprocessing 2^78.09276 (allowances and counted precomputation, included in the time).

**This derivative.** Credited derivative of itseasypop's 2d1c4fc2-7bdd-4b92-af0c-f0c041883b07 (91.5962). That package is the 38-step
attack of ePrint 2026/1120 with the 2^26 A0-variants of the published dense part, the c7 classes of those variants (one W7 test decides a whole
class), a bit-sliced evaluation of the row-16 filter E16x for 256 variants per batch, and the premises H1, H2 and H3 with their evidence. Its
claim is 2^91.59620 time with 2^30.6 bytes of memory: two bitmaps of 2^32 bits (F7 and the row-16 set), the 245,760 variants with S0(a0) and a sort of the 2^26
pairs (c7, a0) of the precomputation. The construction, the characteristic, the 64 class descriptors it gives (26 more classes of the same family are added here, Section 9.3), the premises H1, H2, H3 and H4, the
success analysis and its allowances are theirs and those of the packages they credit (dependencies.json); we executed none of their code. This
package keeps all of that and changes how the program is built and priced, and which pairs it accepts as a collision, with these effects on log2 T (Section 11, each row computed by the exact ledger with the inputs of that row):

| step | log2 T | change |
|---|---:|---:|
| 2d1c4fc2 as filed (91.59619 recomputed from its printed ledger inputs) | 91.59619 | |
| the success target is exactly 0.39 and the work-cap margin is 2^-16 (the base targets 0.3934 and 2^-8) | 91.57341 | -0.02278 |
| no bitmaps: F7 by a decision tree on its affine description, the row-16 set by an affine test; the per-first-block scalars and planes only for first blocks with a passing class | 91.56653 | -0.00688 |
| own plane programs: constants of the class folded, complements absorbed, common subexpressions shared, a 64-register allocator that counts every load, store and spill, dead code removed (the ten cell bits tested, as in the base) | 91.34834 | -0.21819 |
| the 12 lowest bits shared by the 32 row-16 words are tested, so the carry chain of the E16x sum ends at bit 16; the passing lanes are resolved by a counted lane scan | 91.20612 | -0.14221 |
| rows 19 and 20 accept the four E19 patterns with E20[29] = E19[29] (Section 6.1); q3_model 2^-99.1523 (the program of the next row; its counts move T by less than 10^-6 bit) | 89.30887 | -1.89725 |
| rows 22..37 are not tested; the eight output words of the two members are compared after row 37 (the collision itself); step 3b 3000 -> 2829 operations; q3_model 2^-97.7838 = 2^-101.05 x 2^3.2662, the one-sided 99% lower bound of a preregistered paired measurement of both changes together (Section 7.4) | 87.94132 | -1.36755 |
| 90 classes of 3840 variants in 7 plane programs (Section 9.3): the 26 size-3840 classes whose shape lies in the three shapes are added, the W7 tests run as one loop (+4 operations per class), the plane programs are split along the shape bits and the operand order is (1, 3, 2, 0); q3_model unchanged | 87.90375 | -0.03759 |

The online memory falls from 2^30.6 to exactly 1,044,992 bytes (log2 = 19.99506046703272, under 2^20 = 1,048,576); the claimed peak is max(online, preprocessing bound 2^28 bytes) = 2^28 (Section 14, peak memory). The old 1,045,792-byte figure reserved 40 spill slots; the shipped allocator uses 15, reducing the total by 800 bytes. If memory above 2^20 bytes were priced at one bit of time per doubling (the proposal S = time + max(0, memory - 20)), the score S of the base is 102.196 and of this package 87.90375 + (28 - 20) = 95.90375; the time itself is also lower than the base's.

## 0. Summary

- **Algorithm (Sections 4-8).** Messages M0 || M1 and M0 || M1' (128 bytes; the same third block pads both). A first block M0 is two uniform 256-bit words; CV1 = F_38(IV, M0)
  costs one unit. For each of 90 fixed classes of variants of the published dense part S (3840 variants each, 345,600 in all) one test W7x = c7 - A_{-1} in F7 decides whether every variant of the class
  is a *good pair* (the 38-step characteristic has no W6 filter). For the variants of a passing class a counted bit-sliced program computes E16x = C16 + W0 + s0(W1) for 256 variants at a time and tests the 12 lowest bits that all 32
  row-16 words share (stage 3a, probability 2^-12 per good pair). A passing lane is resolved in scalar form (E16x against the exact 32-word set), a row-16 pass is checked through row 21 (rows 19 and 20 in the accepted form of Section 6.1), rows 22..37 are computed without tests and the two outputs are compared: equal outputs are a collision; it is verified with the target.
- **Rates (exact under H1).** Per first block: 90 p7 = 6.02051 passing classes and g = 90 x 3840 x p7 = 92475/4 = 23,118.75 good pairs (p7 = |F7| / 2^32 = 2^-3.90197). The classes are strongly correlated: the number of passing classes is 0 with probability 0.69681 (exhaustive pass over all 2^32 values of A_{-1}, Appendix A), so a scalar and plane block is needed for only 0.30319 of the first blocks.
- **Probability (Section 7, H2).** q3_model = 2^-97.7838: the printed event's 2^-101.05 (the base's one-sided 99% lower bound of its preregistered estimate) times 2^3.2662, the one-sided 99% lower bound of the gain of the accepted event in a preregistered paired run (32 seeds x 2^28 proposals; mean gain 2^3.3439). Our replica of q3 for the accepted event (an independent implementation, organizer experiment `a0-q3-r38`) has mean 2^-97.5860 over 960 replicates.
- **Cost (Sections 9 and 11).** N_FB = 5,840,904,760,525,073,226,269,327 = 2^82.27247 first blocks; per first block 1 unit plus 35 fixed operations, plus on average 132300.1864 counted data-dependent operations (W7 tests, 1497.66; the plane programs of the passing classes, 128796.72; passing lanes, 1714.3396; scalars, planes, hit list and row 16, 291.47), all capped by V_MAX (tested at the start of every first block and after every class, Lemma 8.1).
  The seven plane programs have 1410, 1413, 1421, 1426, 1425, 1426, 1425 instructions per batch of 256 variants (each covers the classes of one part of one of the three shapes; the shape is the set of bits of a0 that vary in the class), against 1,871 to 1,911 in the base.
- **Memory (Section 14).** Peak 2^28 bytes (preprocessing bound); online exactly 1,044,992 bytes (log2 = 19.99506046703272, under 2^20): the batch planes of the 90 classes (675,840 bytes), shared constants, broadcast planes, 15 used spill slots (480 bytes), scalar/counter/hit/F7 storage, class table, code and other routines. Nothing is stored that a computation of the program does not write.
- **Premises (Section 12).** H1 uniform independent chaining values; H2 q3 >= 2^-97.7838 for the accepted event; H3 given a success, the other variants of the same first block pass row 16 at most 2^-8.5 times on average (measured at 2^-10.63 by the base on 65,030 successes and again here on 33,222, both on the first 64 classes; scaled to 90 classes, Section 12); H4 advice allowances (the base's, unchanged); H5 counted word-RAM pricing of the bit-sliced filter with a 64-register allocator; H6 the memory figure.
- **Checks (Section 13).** Exhaustive: |G| = 2^26, 102,696 c7 values, 180 classes of 3840 (90 used), |F7| = 287,309,824, the 32-word row-16 set (2^22 values enumerated). End to end on 2^22, 2^23 and 2^24 real first blocks with the first 64 classes (C, Appendix A.3): every rate as predicted and all 3,561 row-16 passes checked exactly in Python (the first block gives the chaining value, W7 is in F7, every cell of rows -4..16). The shipped program is run on seed-drawn first blocks by two organizer experiments and by `selftest`.

## 1. Target, cost model and output

- **Target** sha256-r38-prefix-v1: SHA-256 steps 0..37 on every padded block, the standard IV once, FIPS 180-4 padding, feed-forward, all eight digest words
  (repository `verifier/hash_functions.digest(m, "sha256", 38)`). The output is two distinct complete messages with equal digests, verified with the target before output.
- **Cost model** collision-frontier-v5: one 38-step target compression = 1 unit; every other executed 256-bit word-RAM primitive (load, store, add/sub, and/or/xor/not, shift, compare, branch, uniform random word) = 1/C unit
  with C = 2728; a conditional branch (compare and branch) counts 2, everything else 1; 64 registers; immediates and shift amounts are instruction fields; memory is reported (and, under the rule that prices it, charged above 2^20 bytes).
- **Notation.** E_i = A_{i-4} + E_{i-4} + S1(E_{i-1}) + CH(E_{i-1}, E_{i-2}, E_{i-3}) + K_i + W_i and A_i = E_i - A_{i-4} + S0(A_{i-1}) + MAJ(A_{i-1}, A_{i-2}, A_{i-3}) (mod 2^32); (A_{-1..-4}, E_{-1..-4}) = (a, ..., h) of the
  incoming chaining value; F_R(cv, B) is the R-step compression with feed-forward. Member x is the message printed second in the paper (M'), member y the message printed first (M).

## 2. Sources, credit, and what is reused or new

- [LZLLQZ26] ePrint 2026/1120 (Li, Zhang, Li, Liu, Qian, Zhu, "Pushing Collision Attacks on SHA-2 to 39 Steps"): the 38-step characteristic (Table 3), the two-bit conditions (Table 4), the semi-free-start pair (Table 5), the two-block memory-efficient
  framework (Section 3.1) with its Step 1 (a SAT solve of the dense part, reported at 2^38.3 compressions), Step 2 (first blocks filtered on W7, 2^-4 in the paper) and Step 3 (the freedom in (W14, W15)), total 2^104.3 time with negligible memory; [LLWS26] ePrint 2026/1080 (the framework); [LLW24] EUROCRYPT 2024 (the SAT/SMT tool).
- itseasypop's 2d1c4fc2 (91.5962): the A0-variants of the Step-1 solution (the word A0 carries no condition of the 38-step characteristic), the c7 classes and the 64 class descriptors, the observation that every variant of a passing class is a good pair, the
  bit-sliced E16x filter for 256 variants per word, the success analysis (Bonferroni per first block, Chebyshev caps), the premises H1 to H3 and their evidence, and the allowances. Their result is quoted where it is used and marked as theirs. Its own lineage, which it credits, is in dependencies.json: the earlier r38 filings of the same attack
  (b99301f4 leech1996, 349e3a6a Th0rgal, 20dbd783 GordoAR: transcription of Tables 3-5, orientation, the `+` reading, the corrected condition W25[4] = W25[6], the exact set F7, the q3 estimator design), 1c368173 (the r37 filing the method comes from) and 6eeefb64 (the calibrated price of a solver CPU-second).
- The numeric tables of the characteristic in the program (cells of A, E and W by row, the + pairs, the two-bit conditions) are data, taken from Th0rgal's transcription in aa0496d3 (experiments/vt38.py) through our earlier r38 package and verified here on the published pair (`selftest`); this is the only thing taken from a participant's program, as data.
- New in this package (all code and measurements are ours; nothing of any other participant's program was executed): the memory-free decision tree for F7 and the affine test for the row-16 set; the plane-program builder with constant folding, absorbed complements, common subexpressions, dead-code removal and a 64-register Belady allocator whose loads, stores and spills are counted; the choice of the 12 tested bits;
  the counted online program (first-block words, W7 tests, per-first-block scalars and planes, lane scan, step 3b); the exact ledger and its inputs; the exhaustive passes (`fam38.c`, `hits38.c`), the end-to-end program on real first blocks (`e2e38m.c`); a sequential Monte-Carlo replica of q3 and its calibration; the two organizer experiments.
- Tools and credit for them: this package was written, run and checked by Claude Code (models Claude Sonnet 5.5 and, for this version, Claude Opus 5.5; Anthropic) under the direction of the project owner; the trail tool of Section 7.4 was written in this project with Claude Code; Grok (xAI) pointed out that the paper's Table 1 lists the 38-step attack at 2^104.3 time with negligible memory and framed the memory-rule arithmetic; GPT Luna (OpenAI) computed the earlier sharded-table memory trade that this result is compared with in the note; Grok (xAI) computed the class schedule of Section 9.3 (which classes, how many plane programs, the operand order, the looped W7 test) and its ledger, which we re-derived with the program of this package (the same N).

## 3. The characteristic (ePrint 2026/1120, as transcribed in the earlier r38 filings of this attack; verified here)

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

F_38(CV, M) = F_38(CV, M') = the printed hash under our reference code (`a0lean38.py`, `selftest`); every cell of rows -4..37 and every two-bit condition (corrected reading) holds with x = M', y = M.


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
E_i = A_i + A_{i-4} - S0(A_{i-1}) - MAJ(A_{i-1}, A_{i-2}, A_{i-3}) and W_i = E_i - A_{i-4} - E_{i-4} - S1(E_{i-1}) - CH(E_{i-1}, E_{i-2}, E_{i-3}) - K_i (i = 0..13), the words of the incoming CV1 entering as A_{-1..-4}, E_{-1..-4}.
**Lemma 4.1.** Steps 0..13 of F_38 from CV1 with these words reproduce the state rows; for fixed A0..A13 the map CV1 -> (W0, ..., W7) is a bijection (W7 depends only on A_{-1}, W6 is -A_{-2} plus a function of A_{-1}, ..., W0 is -E_{-4} plus
a function of the earlier coordinates); W8..W13 do not depend on CV1. (This is the framework of [LLWS26] for a dense part with no conditions on W5, W6 and E1..E3; checked here on every constructed pair, Section 13.)

### 4.3 The A0-variants

**Lemma 4.2.** Replace A0 of S by any a0 (both members) and keep A1..A13. For every chaining value: (a) E5..E13 and W9..W13 are unchanged; (b) E4 = a0 + C4 with C4 = A4 - S0(A3) - MAJ(A3, A2, A1), and W8x = W8C - E4 with
W8C = E8 - A4 - S1(E7) - CH(E7, E6, E5) - K8 (both members shift by the same E4, so W8y - W8x = D8 = fbc00800 is unchanged); (c) W0..W7 absorb E0..E4; their member differences are 0 for i <= 6 and d7 = 20000000 for i = 7, because E4, E5, E6 carry
no difference; (d) the only cells involving E4 or W8 are W8's cell (u at bits 26, 22, n at bit 11, the x-values fixed there) and the printed W8 two-bit conditions W8[0] != W8[28], W8[30] != W8[9], W8[1] = W8[18]; these fix the signed XOR difference of s0(W8) and hence
s0(W8y) - s0(W8x) = fe7f8000, the value of the published pair.

Define **G = {a0 : W8x = W8C - (a0 + C4) and W8y = W8x + D8 follow W8's cell, and the three W8 two-bit conditions hold}**. Exhaustively (`fam38.c`, Appendix A) |G| = 67,108,864 = 2^26, the modular difference s0(W8y) - s0(W8x) equals fe7f8000 for all of them, and the published A0 (b75dae71) is in G.

**Lemma 4.3 (validity).** For a0 in G, every chaining value whose words satisfy W7x in F7 (Section 5.1) and the single l in L*, the pair follows every cell of rows -4..15 (W7's XOR cell excepted) and every printed two-bit condition closing at a row <= 15 except those on W7, and every
modular difference entering the expansion equals the published pair's. (Checked on 3,561 real row-16 passes, Section 13.1, and on every constructed pair.)

## 5. Step 2 with variants

### 5.1 The exact filter F7 and its decision tree

With d7 = 20000000, the cells of rows 22/23 require s0(W7y) - s0(W7x) = t7 = 03bff800; W6 carries no difference in the 38-step characteristic, so there is no W6 filter: F7 = {w : s0(w + d7) - s0(w) = t7}, |F7| = 287,309,824 (exhaustive pass of `fam38.c`), p7 = |F7| / 2^32 = 2^-3.90197 = 274/4096.
By the carry pattern of w + d7, F7 is the union of three affine families:

```text
[w29=0, 14^18=1, 8^25=1, 1^12=0]                                                          2^28 words
[w29=1, w30=0, 14^18=1, 15^19=1, 8^25=1, 9^26=1, 1^12=0, 2^13=0]                            2^24 words
[w29=1, w30=1, 14^18=1, 15^19=1, 16^20^31=1, 8^25=1, 9^26=1, 10^27^31=1, 1^12=0, 2^13=0, 3^14^31=0]  2^21 words
```

(a^b is the XOR of bits a and b of w.) Memory-free test of w = c7 - A_{-1} (the program of `w7test`): form t = w ^ (w >> 4), u = w ^ (w >> 17), v = w ^ (w >> 11) (bits 14..16 of t are 14^18, 15^19, 16^20; bits 8..10 of u are 8^25, 9^26, 10^27; bits 1..3 of v are 1^12, 2^13, 3^14); leave if t[14] = 0, then if u[8] = 0, then if v[1] = 1;
if w29 = 0 accept; else leave unless t[15] = 1, u[9] = 1, v[2] = 0 (one comparison of three masked bits); if w30 = 0 accept; else compare the three words t[16], u[10], v[3] each XOR w31 with (1, 1, 0). Every exit adds one operation to the work counter. The operation counts of the exits are
8 (probability 1/2), 13 (probability 1/4), 18 (probability 1/8), 21 (probability 1/16), 28 (probability 7/128), 31 (probability 1/256), 45 (probability 7/2048), 45 (probability 1/2048) and the expected count is 809/64 = 12.640625 operations per test (64 tests: 809.00 per first block, the counter update included). `selftest` and the test of Section 13.2 compare the tree with the definition of F7 on random and structured words (0 disagreements in 1.1 million words). The base looks the word up in a bitmap of 2^32 bits (2^29 bytes); this is the only change at this place.

### 5.2 Lemma 5.1 (distribution, per variant)

Under H1, for every fixed a0: Pr[W7x in F7] = p7 exactly; conditioned on it, (W0..W6) is uniform on (2^32)^7 and independent of W7, which is uniform on F7; for the l of L*, (W16..W21) is a bijective image of (W0..W5) for fixed (W6, W9..W15) (inverse expansion), hence iid uniform and independent of (W6, W7).

### 5.3 The c7 classes and the first-block statistics

W7x = c7(a0) - A_{-1} with c7(a0) = E7 - 2 A3 + S0(A2) + MAJ(A2, A1, a0) - S1(E6) - CH(E6, E5, a0 + C4) - K7 (c7(b75dae71) = 8f6c89c5, the published constant). The exhaustive pass of `fam38.c` finds 102,696 distinct c7 values on G and
180 classes of size 3840 (the maximum). The 64 smallest c7 among them are the 64 descriptors of the base (the pass reproduces their c7 values and member sets); the 180 classes of size 3840 have only three masks (15, 16 or 17 bits: 91eb5491 for 96 classes, 91eb54d1 for 52, 91eb55d1 for 32), and each class equals {base ^ s : s subset of mask, in G, c7 = the class value} with 3840 members. The 90 used are the 64 of the base and the 26 other classes whose constant bits outside the mask already lie in the shape of the base classes of that mask (48 classes of mask 91eb5491, 26 of 91eb54d1, 16 of 91eb55d1); no class that would enlarge a shape is used.
For a given CV1, W7x is the same word for all variants of a class, so one membership test decides the whole class and every variant of a passing class is a good pair. Per first block E[passing classes] = 90 p7 = 6.02051 and E[good pairs] = g = 90 x 3840 x p7 = 23,118.75 (exact under H1, by linearity).
The classes are not independent: the 90 selected c7 values are close, so the passing classes of one first block come in clumps. The exact distribution (all 2^32 values of A_{-1}, `hits38.c`, Appendix A.2) has Pr[no class passes] = 2,992,758,256 / 2^32 = 0.69681, Pr[some class passes] = 0.30319, mean 6.02051 and second moment 148.226 (maximum 39 passing classes). Only the expectations enter the ledger (linearity); the exact Pr[some class passes] prices the per-first-block scalars and planes.

## 6. Step 3: row 16

L* (from the earlier filings, re-checked): for the published S, |L| = 8 and |L*| = 1, the published (W14, W15) = (d28e48a0, 9f1f65bb) on the x side ((d28e48a0, 9b5f6dbb) on the y side). Rows 12..15 of both members depend only on S and l, not on CV1 or the variant.

**Row 16.** W16 = s1(W14) + W9 + s0(W1) + W0, so E16x = C16 + W0 + s0(W1) with C16 = A12 + E12 + S1(E15) + CH(E15, E14, E13) + K16 + s1(W14) + W9 = fe314838 (member x), and every cell of row 16 (both members) and every two-bit condition closing at row 16 is a function of E16x. The ten fixed bits of the E16 cell form the mask 4c431a80.
Exhaustive enumeration of the 2^22 values with those bits (`r16enum.py`, Appendix A.4) gives exactly 32 passing words:

```text
481b02f9 481b02fa 481b02fd 481b02fe 481b06f9 481b06fa 481b06fd 481b06fe 481b22f9 481b22fa 481b22fd 481b22fe
481b26f9 481b26fa 481b26fd 481b26fe 482302f9 482302fa 482302fd 482302fe 482306f9 482306fa 482306fd 482306fe
482322f9 482322fa 482322fd 482322fe 482326f9 482326fa 482326fd 482326fe
```

They are R16B = 481b02f9 plus any subset sum of {1, 4, 0x400, 0x2000, 0x80000}, so E16x is in the set iff (E16x - R16B) & ~0x82405 = 0 (an affine test: three operations and a branch). All 32 words agree on 24 bits; the 12 lowest of them are bits 3, 4, 5, 6, 7, 8, 9, 11, 12, 14, 15, 16, with common value 481b02f9 on the mask 0001dbf8. By Lemma 5.1 E16x is uniform for a good pair, so Pr[stage 3a] = 2^-12 and Pr[row 16] = 32/2^32 = 2^-27 exactly.
Stage 3a is a necessary condition of row 16 (a lane that fails a shared bit cannot be in the set), and it tests the *lowest* shared bits on purpose: the sum E16x = KP + a0 + s0(W1) is formed by a ripple adder whose length is set by the highest tested bit (here 16) and nothing above it is computed; the base tests the ten cell bits, the highest being bit 30.
For a row-16 pass the program computes W0..W8 of both members (Lemma 4.1), the y-words, rows 16..37 of both members with the tests of rows 16..21 (early abort), and then compares the eight words A34..A37, E34..E37 of the two members.

### 6.1 The accepted event (this version)

The program accepts a row-16 pass iff (i) rows 16..21 of both members follow every printed cell, '+' pair and two-bit condition closing at rows 16..21, except that at row 19 the nine value bits of E19 on the mask 30040e32 may take any of the four patterns 00040832, 10000010, 20000c12, 30040430 (the published one is 30040430) and at row 20 the value bit E20[29] is replaced by the tie E20[29] = E19[29]; and (ii) the state words A34..A37, E34..E37 after step 37 are equal for the two members. No cell, difference or two-bit condition of rows 22..37 (W23 and W25 included) is tested.

**Lemma 6.1.** If (ii) holds, the two second-block outputs are equal (the output is the chaining value plus (A37, A36, A35, A34, E37, E36, E35, E34), and the chaining value is common), so m = M0 || M1 and m' = M0 || M1' collide under the complete target (the third block is the common FIPS padding block; M1 is a full data block). m != m' because M1 and M1' differ in W7, W8..W11, W15. The program accepts exactly the pairs it can certify, whatever path rows 22..37 take; condition (i) only decides where the tests stop.

Why these four patterns: an exhaustive enumeration over the nine E19 value bits and the six E20 value bits on 64 sampled prefixes (every other word held) finds exactly eight combinations that pass rows 19..21, the four E19 patterns times E20[29] in {0, 1}; with E20[29] != E19[29] the CH of row 22 passes E21's bit-29 difference and the pair dies at row 22 (derivation computed, not proved). Correctness does not depend on this: the program tests exactly the event whose probability H2 states, and that probability is measured (Section 7.4). The counted tests: row 19 is one AND with the cell mask and one compare-and-branch per pattern (the published pattern last, so the longest path is charged), row 20 tests its other value bits and then E20 xor E19, AND 2^29, branch; the comparison of the outputs is 8 xor, 7 or and one branch. `selftest` checks the counted tests against the definition on all 512 values of the nine bits and the four values of (E19[29], E20[29]).

## 7. The Step-3 probability for the variants (H2)

### 7.1 Quantity and Lemma 7.1

q3 = the average over the 345,600 selected variants of Pr[the pair is in the accepted event of Section 6.1 | good pair], the probability over CV1 (Lemma 5.1). (The earlier filings used the printed event, every cell and printed two-bit condition of rows 16..37; Sections 7.2 and 7.3 quote its estimates where they are the starting point.) **Lemma 7.1.** Rows 16..22 are functions of S's rows 12..15, l and W16..W22 (W22 = s1(W20) + W15 + s0(W7) + W6), whose law given goodness is the same for every variant: the probability of rows 16..22 is identical for all variants (so also for the 26 classes added in Section 9.3, whose variants are in G like the others).
W8 enters rows >= 23 only through W23 = s1(W21) + W16 + s0(W8) + W7 and W24 = s1(W22) + W17 + s0(W9) + W8 (and later words through them), with fixed modular differences (Lemma 4.2); only the values of W23, W24 move, each by a constant added to a word that is near-uniform given rows 16..22.

### 7.2 The estimate of the base for the printed event (quoted)

The base's preregistered sequential Monte-Carlo estimate of the printed-event probability (32 replicates, W8 drawn from the 245,760 variants; from its public proof, Section 7.3; participant-run, not repeated here): mean 2^-101.015, one-sided 99% lower bound 2^-101.045 (Student and bootstrap agree), all replicates at least 2^-101.19; on 1,073,754,023 common row-22 samples rows 23..37 pass 32,542 times with the variants' W8 and 32,538 times with the published W8.
The stage factors (log2) are -27, -17, -13, -15, -6, -7, -1 for rows 16..22 and -15 for the tail, whose sum -101 is the analytic prediction (the factors count condition bits). 2^-101.05 is the base's value for the printed event; Section 7.4 measures the factor from the printed event to the accepted one.

### 7.3 Our own estimator for the accepted event and its calibration (`smc_replicate`)

An independent implementation of the base's estimator, changed for the accepted event: row 16 exact (64 particles uniform on the 32 words); rows 17..21 with 32, 8, 2, 2, 2 proposals per particle (E_t^x proposed uniformly with its fixed x-bits imposed and its '+' bits copied from E_{t-1}^x, exact weight 2^-f; at row 19 the nine pattern bits are one of the four patterns drawn uniformly, weight 4 x 2^-f; at row 20 bit 29 is set to E19[29]; W_t^x from the step equation, W_t^y = W_t^x + the published difference, the whole row in the accepted form and its two-bit conditions checked, multinomial resampling);
tail: 384 proposals per particle of a variant (one of 512 embedded variants drawn once and uniformly from the 245,760 variants of the first 64 classes by SHAKE-256 of a fixed label, each checked to be in G and in a selected class; it was not redrawn for the 26 added classes, Section 12 H2), W23 by importance sampling over the classes of its ten printed conditions (the six value bits of its cell and its four two-bit conditions): one of the 27 classes listed in `SIG` with probability (n + 2)/218, uniform inside it, weight 218 x 2^-10 / (n + 2); W7 = W23 - s1(W21) - W16 - s0(W8) accepted iff in F7 (weight 2^22/|F7| on top), W6 uniform, rows 22..37 computed and the outputs compared.
The 27 classes and their counts n are those seen among the 164 exact events of a development run with W23 uniform (Appendix A.5); 63 of the 164 were in the printed class. Classes never seen are not proposed, so the replica estimates a lower bound of q3 (the unseen classes held at most a few percent of the development events: 6 classes were seen once).
The replicate estimate is the product of the stage means. Every tail success is rebuilt into a real 38-step semi-free-start pair (W7..W0 by the inverse expansion, CV1 by inverting steps 7..0 of the variant) and verified: equal outputs, M1 != M1', Lemma 4.1 returns W0..W13 of both members, rows -4..21 in the accepted form except W7's XOR cell, W7 in F7; then the counted program `step3b` is run on (CV1, a0) and must accept it. A failure of either check counts as a failed check.
Calibrations (Appendix A.5; each preregistered with its program hash and fresh labels before its first replicate; all replicates kept):

| version | proposal of W23 | replicates | mean (log2) | halves | pooled means of 20: mean, sd, min | below 2^-98.4338 | failed checks |
|---|---|---:|---:|---|---|---:|---:|
| printed event (earlier package) | printed class | 960 | -101.0253 | | -101.0356, 0.1719, -101.4077 | | 0 |
| v1 | printed class | 960 | -98.8675 | -98.847 / -98.889 | -98.8763, 0.1606, -99.3667 | 48 | 0 |
| v2 | classes, n/164, 192 per particle | 960 | -97.6273 | -97.637 / -97.617 | -97.6777, 0.3815, -98.4245 | 0 | 0 |
| v3 (shipped) | classes, (n + 2)/218, 384 per particle | 960 | -97.5860 | -97.590 / -97.582 | -97.5997, 0.2007, -98.0335 | 0 | 0 |

v1 kept the printed W23 class and measured 2^-98.87: the accepted event does not need the printed W23 class (in the development run 101 of 164 exact events lie outside it), so v1 is a lower bound that misses most of the gain at row 23; the rule fails for it. v2 and v3 propose the other classes; v3 only lowers the variance (Appendix A.5). In v3, 6,813 of 9,090 successes have an E19 pattern other than the published one.
The replica is an estimate of a lower bound of q3 by an implementation independent of the tool of Section 7.4; its mean is 0.198 bit above q3_model.

### 7.4 The preregistered paired measurement of the gain (H2's declared value)

*Tool.* `traillab` (our own C program, written for this project with Claude Code; not shipped: the experiment sources are limited to 65,536 bytes) estimates rates of the 38-step characteristic by sequential Monte Carlo on real compressions: every sample is a chaining value and W0..W15 of both members with the real message expansion, the state is replayed from the words (0 replay mismatches are required), rows 6..21 are the prefix (sampled with the attack's conditions; `prefix log2 P(rows 6..21)` is its SMC estimate) and rows 22..37 the window, with the late words of the attack redrawn per sample (W6 uniform, W7 in F7, W8 in its cell, W23 free). For each window sample it counts two events: *cells* (every printed cell and condition of rows 22..37) and *EXACT* (zero output difference after step 37). The tool passed its validation suite (48 of 48 quick tests: exact counts of the row-16 set and F7, the flip tables, digests of the published pair).

*Preregistration* (written and hashed, SHA-256 2a8482bfbd4d426a3b28b4751ec9f4385929238d702b1c53f74b2a2cbcae4c82, together with the run script, 2026-10-12 03:29:20 MDT; the first seed started 03:29:30): 32 fresh seeds 3001..3032, each 2^28 window proposals (8192 particles, 32768 per particle), each seed run twice: *base* (the printed prefix) and *tie* (prefix with the nine E19 value bits 30040e32 and E20 value bit 29 dropped and the linear condition E20[29] xor E19[29] = 0 added). Per seed (log2): JOINT = tie prefix + log2 rate(EXACT) - (base prefix + log2 rate(cells)), A = tie EXACT - base EXACT, B = base EXACT - base cells. Declared value of each: the one-sided 99% Student lower bound over the 32 per-seed values, mean - t(0.99, 31) sd / sqrt(32), t = 2.4528 (the seed is the cluster, which absorbs over-dispersion). Halves 3001..3016 and 3017..3032. Diagnostics required 0: prefix broken by redraw, y-anchor inconsistent, replay mismatches. No interim look, no stopping rule used.

*Results* (all 64 runs completed, every diagnostic 0):

| statistic (log2) | mean | seed sd | declared 99% lower bound | half 1 / half 2 | halves apart |
|---|---:|---:|---:|---|---|
| JOINT (accepted event against printed cells) | +3.3439 | 0.1793 | **+3.2662** | 3.3502 / 3.3377 | 0.19 se |
| A (four patterns and tie, both to EXACT) | +1.9762 | 0.1811 | +1.8977 | 1.9854 / 1.9669 | 0.28 se |
| B (EXACT over cells, base proposals) | +1.3677 | 0.0217 | +1.3583 | 1.3647 / 1.3707 | 0.77 se |
| B on the tie proposals | +1.3627 | 0.0520 | +1.3401 | | |

Absolute levels: base cells -101.0058 (sd 0.034), base EXACT -99.6381, tie EXACT -97.6619 (99% lower bound -97.7396). Pooled counts: base 130,815 cells and 337,541 EXACT (2.580), tie 131,865 and 338,678 (2.568). A and B do not interact (B on the tie proposals equals B), and JOINT = A + B.
Per-seed JOINT values: 3.1888 3.1705 3.3086 3.3669 3.1971 3.4284 3.5346 3.2685 3.4709 3.7306 3.3312 3.6130 3.5114 3.3677 2.9719 3.1429 3.4818 3.5111 3.3630 3.4275 3.5465 3.1062 3.5527 3.2206 3.4169 3.2265 3.5234 3.1995 3.0763 3.1393 3.1931 3.4181.

*Use.* q3_model = 2^(-101.05 + 3.2662) = 2^-97.7838: the base's 99% lower bound for the printed event times the 99% lower bound of the paired gain. The tool's own level for the printed event (2^-101.006) is 0.044 bit above the base's 2^-101.05; the gain is applied to the lower value. The joint factor replaces every earlier credit for the same effects (the E19 coset of earlier analyses, the measured exact-event factor and the W25 carry factor); none of them is used. The tool's model is the one of this package (W8 in its cell, W6 uniform, W7 in F7); the shipped replica of Section 7.3 (another implementation, the shipped law of W8) agrees: 2^-97.5860 against 2^-97.6619 for the tool's mean.

## 8. The algorithm (fixed caps)

```text
input: N_FB, V_MAX; advice: S, L*, the 90 class descriptors (c7, base, mask, program), the three shapes
precompute: for each class every subset s of mask: a0 = base ^ s, kept iff in G and c7(a0) = c7 (3840 variants), stored as 15 batches of 256 in bit-sliced form;
            the seven plane programs (each covers the classes of one part of one shape)
V = 0                                   (V = the data-dependent operations executed so far, a register of the program)
for f = 1 .. N_FB:
    draw two uniform 256-bit words; M0 := their sixteen 32-bit fields; CV1 := F_38(IV, M0)                       [1 unit]
    if V > V_MAX: halt (failure)            (cap test on EVERY first block, hit or not, before the 90 W7 tests; its compare-and-branch is among the 35 fixed operations)
    hits := [c : c7_c - A_{-1} in F7]   (one decision tree run in a loop over the 90 classes; V += its operations and 4 per class)
    if hits: the per-first-block scalars (HH, PP, QQ, EF, FF, K1, KP) and their 224 broadcast planes; V += 920
        for c in hits:
            for each of the 15 batches of c: run the plane program of c -> ok plane (lanes passing the 12 tested bits of E16x)
                for each passing lane (lowest first): a0 from the stored planes; E16x in scalar form; V += ...
                    if E16x in the row-16 set: Step 2 (rows -4..15), rows 16..37 of both members, the tests of rows 16..21 with early abort
                        if they pass and A34..A37, E34..E37 are equal for both members: build m, m'; if digest(m) = digest(m') and m != m': output, halt
            V += the class's counted work; if V > V_MAX: halt (failure)
halt (failure)
```

The run executes at most N_FB compressions, N_FB x 35 fixed operations, at most V_MAX + OVER data-dependent operations, the precomputation and one final verification, whatever the coins. OVER = 12,119,157 = P0 + one class at its maximum (12,113,647), with P0 = 5,510 = 90 x (45 + 4 + 2) + 38 + 882, the work of a block before its first class cap test (all 90 W7 tests at their longest path of 45 operations, with the loop and the hit-list append, the scalars and the planes).

*Lemma 8.1 (the cap).* Every first block starts with V <= V_MAX, or the run halts at once (at most 33 of the 35 fixed operations are executed). From a start with V <= V_MAX the block adds at most P0 before its first class cap test; after each class the test either halts or leaves V <= V_MAX, and a class adds at most 12,113,647. A block with no passing class adds at most P0 and is followed by the start test of the next block. Hence at every moment V <= V_MAX + P0 + 12,113,647 = V_MAX + OVER, for every execution and every coin sequence: a run of hitless first blocks cannot pass V_MAX by more than one block's W7 phase. (The previous version tested only after a class, which hitless blocks never reach: the fatal finding F-CAP-CHECK-GAP.) `selftest` runs the test: after a block with V > V_MAX the next block halts before any W7 test, with at most 35 operations.

## 9. The counted program (`experiments/a0lean38.py`, commands `calibrate` and `ledger`)

### 9.1 Machine, pricing and scalar routines

A 256-bit word RAM with 64 registers; every executed primitive is counted: load, store, add, sub, and, or, xor, not, shift, immediate load, random word 1 each; compare-and-branch 2; one target compression 1 unit; immediates and shift amounts are instruction fields; reduction mod 2^32 is one AND where the program needs a masked value.
S0, S1, s0, s1 cost 8 each (doubled word, shifts, xors, one mask), CH 3, MAJ 4. The scalar routines are written in the machine's primitives (class `Mach`) and executed; the table lists their counts as produced by `calibrate`.

| routine | operations |
|---|---|
| first-block words (2 random words, 16 fields) | 30 |
| first-block control (counter, cap compare and branch executed on every first block as `if V > V_MAX: halt` before the W7 tests, the test of the hit list) | 5 (the 35 of the ledger are these 5 and the 30 above) |
| one W7 test: 7, 12, 17, 20, 27, 30, 44 operations by exit, plus 1 for the work counter; the loop over the class table adds 4 (load c7, advance the pointer, compare and branch 2) | mean 12.640625 + 4 |
| appending a passing class to the hit list | 2 |
| per-first-block scalars HH, PP, QQ, EF, FF, K1, KP (`fb_scalars`) and one work-counter update | 38 |
| the 7 x 32 broadcast planes (plane j = 0 - ((x >> j) & 1), stored; 3 or 4 operations each) | 882 |
| per passing class: setup 3 (batch pointer, end pointer, class constants; the class entry's mask word also holds the number of its plane program), per batch of 256 variants the plane program + `ok` test 2 + pointer, compare, branch 4, end of class (work counter, cap test) 4 | 7 + 15 x (program + 6) |
| the plane program of a part of a shape (Section 9.2) | 1410, 1413, 1421, 1426, 1425, 1426, 1425 |
| a passing lane: `first_lane` (chunk scan, binary search), `lane_value` (conditional shifts of the stored planes, assembly of a0), `scalar_e16`, the row-16 test, the work counter, clearing the lane and the loop test | at most 296, 308, 320 for the shapes of mask 91eb5491, 91eb54d1, 91eb55d1 (maximum over the 256 lanes of one class of each shape) |
| `scalar_e16`: E0, S0(a0), MAJ(a0, a, b) from PP and QQ, S1(E0), CH from EF and FF, W1, s0(W1), E16x | 38 |
| a row-16 pass: Step 2 (E0..E4, W0..W8 of both members), rows 16..37 of both members (106 per row), the tests of rows 16..21 (cells, differences, '+' pair, two-bit conditions; row 19 one AND and four compare-and-branches, row 20 the tie by xor, and, branch) with an early abort, and the comparison of the eight output words (8 xor, 7 or, 1 branch); `step3b` on the published pair, every test passing, the published E19 pattern compared last | 2829 (maximum; 3000 with the printed tests of rows 16..37) |

The per-first-block block (scalars and planes, 920 operations with the counter update) is executed only when a class passes (`process_fb`); the 35 fixed operations are executed on every first block.

### 9.2 The plane program (per program, per batch of 256 variants)

Bit L of every 256-bit plane belongs to the variant 256 b + L of the class. Per first block the broadcast planes of Section 9.1 are stored (HH, PP, QQ, EF, FF, K1, KP; a plane is all zero or all one). Per batch the stored planes A<j> of the bits j of a0 that vary in the class (15, 16 or 17 of them) are loaded through the batch base register; bits that are
constant on the class are folded into the program, and the 3 to 5 positions where the classes of one program differ are inputs C<j> (all-zero or all-one words stored with the class, loaded through the class base register). With E0 = a0 + HH, S1(E0), CH(E0, e, f) = FF ^ (E0 & EF), MAJ(a0, a, b) = PP | (a0 & QQ) (or PP, or QQ, where a0 is constant), S0(a0) and K1' = K1:

```text
W1   = K1 - S0(a0) - MAJ(a0,a,b) - S1(E0) - CH(E0,e,f)      (K1 + ~SA + ~MAJ + ~S1 + ~CH + 4: three carry-save layers, then one ripple step per bit)
E16x = KP + a0 + s0(W1)                                       (one carry-save layer, then a ripple adder up to the highest tested bit)
ok   = AND over the 12 tested bits j of (E16x[j] == common bit j of the 32 row-16 words)
```

The program is built by `build_e16` as a DAG of xor/and/or nodes over 256-bit planes. A value carries a complement flag (complements cost nothing, except a mixed and/or: one extra operation, no fused AND-NOT); constants are folded; equal nodes are shared; only nodes that `ok` depends on are emitted.
The allocator (`Prog.schedule`) walks the nodes in creation order with 64 registers: an operand that is not in a register is loaded (inputs from their address, a spilled value from its slot), the register whose value is needed farthest in the future is evicted and stored first if it has a later use and no copy in memory (Belady's rule), a dead operand's register is reused for the result.
Every load, store and spill is one instruction of the list, and the instruction count is the charge (`run_prog` executes the list; nothing else is charged or free). The loop over the bit positions interleaves S1/CH/MAJ/SA of bit j, the three carry-save layers and the ripple step of W1 so that the carry-save vectors are never stored; the operand order of the layers is (1, 3, 2, 0), the best of the 24 orders on the final cut (on the three full shapes the 24 orders give 4342 to 4346 instructions in total; the order of the earlier filing gave 4342, this one 4343).

| program | mask of a0 bits that vary | classes | varying bits | shared input positions | instructions | spill stores |
|---:|---|---:|---:|---:|---:|---:|
| 0 | 91eb5491 | 16 | 15 | 4 | 1410 | 14 |
| 1 | 91eb5491 | 16 | 15 | 4 | 1413 | 14 |
| 2 | 91eb5491 | 16 | 15 | 5 | 1421 | 15 |
| 3 | 91eb54d1 | 14 | 16 | 4 | 1426 | 15 |
| 4 | 91eb54d1 | 12 | 16 | 4 | 1425 | 15 |
| 5 | 91eb55d1 | 8 | 17 | 3 | 1426 | 15 |
| 6 | 91eb55d1 | 8 | 17 | 3 | 1425 | 15 |

The seven programs total 9,946 instructions; at most 15 spill slots are used (the memory budget has 40).

The programs are executed on the lanes of 768 variants of each program in `selftest` and on every lane of every processed batch in the organizer experiment `a0-online-r38`, and their `ok` plane is compared with the scalar definition (E16x from the Step-2 equations, Lemma 4.1) lane by lane: 0 disagreements (Section 13).
Section 11 scans the number of tested bits (`TK`): fewer tested bits shorten the program but pass more lanes to the scalar lane scan, more tested bits lengthen the carry chain.

### 9.3 The class schedule (credit: Grok, xAI)

Grok (xAI), asked to re-optimise the schedule of the earlier filing for the memory rule, proposed this schedule; we re-derived its counts with the program of this package (the same programs, the same N). The earlier filing ran the 64 smallest size-3840 classes as three unrolled programs (one per mask) with 64 unrolled W7 tests, 775,680 bytes. The new schedule uses the memory that the loop frees:

- **90 classes.** All size-3840 classes whose constant bits outside the mask already lie in one of the three shapes (48 + 26 + 16); the 64 of the earlier filing are among them (the 64 smallest c7). The list is the table `CLASSES` of the program (c7, base, mask, program number). One more class that keeps a shape does not exist; a class that enlarges a shape needs another program of about 1,400 instructions (about 45 KB), which does not fit under 2^20.
- **A looped W7 test.** The decision tree of Section 5.1 is stored once (52 instructions) with a loop over the class table (load c7, pointer add, compare-and-branch: 4 operations per class, charged); the unrolled 64 copies took 106,496 bytes, the loop 1,824.
- **Seven plane programs.** Each shape is cut along its shape bits (a guillotine partition; every cut tried, the cheapest total kept under the byte budget): a part has more constant bits, hence a shorter program (1410 to 1426 instructions against 1445 to 1452). The class table lists, for each class, its program; the sum over classes of the program length is 127,776 (130,374 for three unsplit programs).
- **Operand order (1, 3, 2, 0)** of the carry-save layers and TK = 12 tested bits (rescanned on the seven programs: 11 and 13 bits are worse); lane caps 296, 308 and 320 measured per shape.
- Memory 1,044,992 bytes (Section 14), 3,584 bytes under 2^20. The model counts the dispatch to a class's program and its loop as the 7 + 4 operations listed in Section 9.1; no other charge is made for it.

Not established: q3 and the H3 rate were not measured again on the 26 added classes (Section 12); the loop is a count under the machine model, not an instruction list from the allocator (charging 5 instead of 4 operations per class gives 87.90470).

## 10. Success probability, independence and caps

A *trial* is (first block f, selected variant a0); A_t: a0 is good for f and the pair is in the accepted event (Section 6.1). The program examines every good pair of every processed first block and every row-16 pass, so it finds a success iff some A_t occurs before the caps; every output is verified (Lemma 6.1).

- **Expectation.** E[X_f] = g q3 with g = 23,118.75 and q3 >= q3_model = 2^-97.7838.
- **One first block (H3).** Bonferroni: Pr[X_f >= 1] >= E[X_f] - (1/2) E[X_f (X_f - 1)], and E[X_f (X_f - 1)] = sum_t Pr[A_t] E[X_f - 1 | A_t]. Let R_f be the number of selected variants of f that are good and pass row 16. Every success passes row 16, so given A_t, X_f - 1 <= R_f - 1 (the other variants of f that pass row 16).
  H3 states sum_t Pr[A_t] E[R_f - 1 | A_t] <= 2^-8.5 E[X_f]. Hence Pr[X_f >= 1] >= (1 - 2^-9.5) E[X_f].
- **Many first blocks (H1).** Independent chaining values give Pr[X >= 1] >= 1 - exp(-N_FB g q3 (1 - 2^-9.5)).
- **Work cap.** The data-dependent work v_f of a first block (W7 tests, scalars, planes, programs, lanes) has mean at most vbar = 132300.1864 (exact rational in Appendix B) and is at most 1,090,233,650 (all 90 classes passing, every lane of every batch passing stage 3a and row 16 with the longest path); by Chebyshev over the independent first blocks, Pr[sum v_f > (1 + 2^-16) N_FB vbar] <= vmax_f / (2^-32 N_FB vbar) = 3.29e-31.
  V_MAX = ceil((1 + 2^-16) N_FB vbar), tested at the start of every first block and after every class (Lemma 8.1); the overshoot is at most OVER = 12,119,157 operations (a block's work before its first class test, 5,510, and one class at its maximum, 12,113,647). vmax_f = 5,510 + 90 x 12,113,647 = 1,090,233,740 (P_cap = 3.285e-31).
- **The abort in the success bound (proved, not sampled).** Let S = the sum of v_f over all N_FB first blocks, the whole work of each block counted, and E_cap = {S > V_MAX}. Every value of V that a test reads counts a part of the work of the first blocks started so far, all terms are nonnegative, so it is at most S; on the complement of E_cap no test ever halts and the program examines all N_FB first blocks exactly as the success analysis assumes. Hence Pr[output a collision] >= Pr[some X_f >= 1] - Pr[E_cap], and Pr[E_cap] <= P_cap by Chebyshev as above (the variance of a sum of independent terms in [0, vmax_f] with mean vbar is at most N_FB vmax_f vbar). When the program halts it halts with a failure, never with a wrong output (Lemma 6.1). No cap probability is sampled and no expected-work bound is used.
- **Success.** N_FB is the least integer with 1 - exp(-N_FB g q3 (1 - 2^-9.5)) - P_cap - 2^-60 >= 0.39, i.e. N_FB = 5,840,904,760,525,073,226,269,327. Pr[output a collision] >= 0.39. The base targets 0.3934 with a 2^-8 cap margin; the exact target and the smaller margin account for 0.02278 bit (Section 11).

## 11. Ledger (exact; `python3 experiments/a0lean38.py ledger`, program of Appendix B)

```text
T = A_C + A_S + DEV + N_FB + (N_FB x 35 + V_MAX + OVER + PRE + FIN) / C + 6
  A_C = 2^78, A_S = 2^74 (the base's allowances, unchanged, H4a, H4b), DEV = 2^70 (this package's explicit development charge, Section 13.4; together 2^-9.8 of T)
  N_FB = 5,840,904,760,525,073,226,269,327 first-block compressions (2^82.27247)
  35 fixed operations per first block (Section 9.1)
  V_MAX = 772,764,579,970,529,091,929,220,381,051 = ceil((1 + 2^-16) N_FB vbar), vbar = 71028121742895 / 536870912 = 132300.1864 (unchanged: the compare-and-branch of the new test was already among the 35 fixed operations):
      W7 tests (90 x (12.640625 + 4))            1497.66
      hit list (2 per passing class)             12.041
      scalars and planes, 920 x Pr[some class passes]   278.94
      plane programs of the passing classes      128796.72   (sum over the 90 classes of p7 x (7 + 15 x (program + 6)))
      passing lanes (sum over the classes of p7 x 3840 x 2^-12 x the lane cap of the shape: 296, 308, 320)        1714.3396
      row-16 passes (g 2^-27 x 2829)        0.4873
  OVER = 12,119,157 = 5,510 + 12,113,647 (the work of a block before its first class cap test, plus one class at its maximum; Lemma 8.1; replaces the earlier 12,114,647)
  PRE = 4,515,430,400 operations (2^32.0722): the member tests of the 90 classes, the batch planes, and 2^32 for the generation of the seven programs (all charged)
  FIN = 1600 operations and 6 compressions (the final verification with the target)
N = T x 2728 = 789,782,238,349,839,437,021,687,302,533   ->   T = 2^87.9037417   ->   time_log2 = 87.90375 (certificate of Appendix B; the ledger of the refuted version differed by 4,510 operations)
preprocessing = A_C + A_S + DEV + PRE/C = 2^78.09276
```

Sensitivity (`ledger` with the inputs named, N_FB recomputed; `sens.py`, Appendix A.7; log2 T):

```text
claimed configuration (q3_model 2^-97.7838, H3 2^-9.5, success 0.39, cap margin 2^-16, A_C 2^78, A_S 2^74, DEV 2^70)   87.90374
q3_model 2^-97.6619 (the mean of the preregistered run, not its lower bound)                                           87.78198
q3_model 2^-98.0                                                                                                       88.11972
q3_model 2^-98.5                                                                                                       88.61931
q3_model 2^-99.0                                                                                                       89.11903
four patterns and tie only (q3_model 2^-99.1523, this program)                                                         89.27126
exact event only (q3_model 2^-99.6917, this program)                                                                   89.81046
neither (q3_model 2^-101.05, this program)                                                                             91.16850
neither, with the printed tests (q3_model 2^-101.05, step3b 3000: the earlier package)                                 91.16850
H3 premise 2^-7.5                                                                                                      87.90973
A_C = 2^84                                                                                                             87.99564
```

## 12. Premises

**H1 - uniform independent chaining values (score-critical).** First blocks are fresh uniform 512-bit strings (two uniform 256-bit words each); their chaining values behave as independent uniform 256-bit values. Used for Lemma 5.1 (exact p7 and the law of the second-block words, per variant), the expected counts and the independence across first blocks.
Evidence: the exact distribution of the number of passing classes over all 2^32 values of A_{-1} (Appendix A.2); 29,360,128 (2^22 + 2^23 + 2^24) real first blocks through the attack's own filters (Section 13.1): passing classes, good pairs, stage-3a passes and row-16 passes at 1.00, 1.00, 1.00 and 0.99 of their expectations, every row-16 pass checked exactly; the organizer experiment `a0-online-r38`; the base's own runs on 2^23 first blocks (quoted: good pairs 1.0005 x expected). Limitations: tested on 2^24 first blocks, not 2^86.

**H2 - Step-3 probability of the variants for the accepted event (score-critical).** q3 >= q3_model = 2^-97.7838, q3 being the probability of the accepted event of Section 6.1 (rows 16..21 with the four E19 patterns and the tie, equal outputs after step 37) for a good pair, averaged over the selected variants (345,600 here). Evidence: Lemma 7.1; the base's preregistered estimate for the printed event (quoted, Section 7.2: mean 2^-101.015, 99% lower bound 2^-101.045); the preregistered paired measurement of the gain from the printed to the accepted event (Section 7.4: 32 seeds x 2^28, mean +3.3439, declared one-sided 99% lower bound +3.2662, halves agree); q3_model = 2^(-101.05 + 3.2662). Our own replica for the accepted event (Section 7.3: mean 2^-97.5860 over 960 replicates, every success rebuilt into a verified 38-step semi-free-start collision and accepted by the counted program) and the organizer experiment `a0-q3-r38` that runs it with a frozen pass rule (pooled mean >= 2^-98.4338).
Limitations: a product of two Monte-Carlo lower bounds (the base's for the printed event, ours for the gain); the gain was measured by our own tool, whose model is this package's (W8 in its cell, W6 uniform, W7 in F7), and confirmed by the shipped replica, an independent implementation that estimates a lower bound; the replica resolves q3 to about 0.3 bit in 20 replicates; the `+` reading and the W25 correction of the printed event are those of the earlier filings. The base's estimate, our gain and the replica all drew the tail variant (W8) from the first 64 classes; q3 was not measured again with variants of the 26 added classes. By Lemma 7.1 rows 16..22 do not depend on the variant and W8 enters only W23 and W24 (each moved by a constant), so we take the average over 90 classes to equal that over 64; this is a premise, not a measurement.

**H3 - few other row-16 passes in a successful first block (score-critical).** With R_f the number of selected variants of first block f that are good and pass row 16: sum_t Pr[A_t] E[R_f - 1 | A_t] <= 2^-8.5 E[X_f]. Evidence: the base's direct measurement on 65,030 sampled successes (quoted from its public proof, Section 13.5; participant-run, not repeated here): 41 other row-16 passes against 35.45 under independence, 2^-10.63 per success, one-sided 99% upper bounds 2^-10.12 (Poisson) and 2^-9.92 (Student over 8 runs), 1.4 bits below the premise;
the clumped passing classes of one first block (73,169 other good pairs per success, 4.45 g) are included in that measurement. The premise ignores rows 17..37 of the other variants. Our own repetition (Section 13.5, Appendix A.8): 33,222 sampled successes of 8 independent runs, all selected variants of each rebuilt chaining value tested, 21 other row-16 passes against 18.15 under independence, 2^-10.63 per success, one-sided 99% upper bounds 2^-9.92 (Poisson) and 2^-9.85 (Student over the 8 runs): 1.3 bits below the premise.
Both measurements sampled successes of the printed event. Every success of the accepted event also passes row 16, so the pointwise bound X_f - 1 <= R_f - 1 of Section 10 is unchanged; the average of R_f - 1 over successes of the accepted event was not measured again (the accepted event differs at rows 19, 20 and 22..37, while R_f counts row-16 passes of the other variants). This is a premise. Both measurements are on the first 64 classes (245,760 variants). Scaled to 90 classes the rate is 21 x 90 / (33,222 x 64) = 2^-10.14 per success, below the premise 2^-8.5 and the ledger factor (derived by scaling, not a new sample).

**H4 - advice allowances (H4a score-critical, H4b supporting).** The published characteristic, its two-bit conditions, S, L* and the 90 class descriptors are advice, charged as in the base through two allowances: A_C = 2^78 (the characteristic search, H4a) and A_S = 2^74 (the Step-1 solve, H4b); the development of this package is charged by an explicit item of the ledger, DEV = 2^70 (Section 13.4), which is a declared charge and not a premise. Together the three are 2^-9.8 of T. Their memory is covered by the preprocessing bound of H6 (2^28 bytes, Section 14, peak memory).

**H4a - characteristic search (score-critical).** *Statement.* The total computation spent to obtain the published 38-step characteristic of [LZLLQZ26] (IACR ePrint 2026/1120, Table 3: failed and repeated searches and tool development included) is at most A_C = 2^78 target compressions.

*Scope.* The preprocessing part of the ledger: A_C = 2^78 is the largest allowance (0.104% of T: 2^78 of 2^87.90375; A_C + A_S + DEV together 0.111%). It enters the claimed time and preprocessing (78.09276); its memory enters the preprocessing bound of H6.

*Evidence and extrapolation.* *Evidence for the allowance (Appendix C part A states every conversion).* (i) Published, for the same kind of search: Mendel, Nad and Schlaeffer (EUROCRYPT 2013, ePrint 2015/350, Sect. 6.3 p.14) found the differential characteristic and the confirming message pair of a 38-step semi-free-start collision of SHA-256 in "about 8 hours on a single CPU. This is equivalent to about 2^37 SHA-256 evaluations" (one combined figure, no hardware named; for 31 steps, Sect. 6.2 p.12: about 21 hours, 2^38.4 evaluations); Li, Liu and Wang (EUROCRYPT 2024, ePrint 2024/349 p.16) found a practical 39-step semi-free-start pair "in 120 seconds with 26 threads". (ii) Measured by us: with the authors' public tool of [LLW24a] (github.com/Peace9911/sha_2_attack, commit 6a9f35fd; model find_dc_model_39: rows 8..26, message support W8..W12, W16, W17, W24, W26, weights W 25, A 10, E at most 90) a 39-step characteristic was derived from scratch in 772.58 s wall on 12 threads (CryptoMiniSat 5.11.21; a Kissat call of 1,800 s on the same file returned no result): 11,071.7 solver CPU-seconds (wall x threads, the failed call included), at the 3,797,484 SHA-256 compressions per second measured here (portable C, one thread, AMD Ryzen 9 7900X, slowest of five runs) 2^35.29 SHA-256 evaluations, 2^36.04 units (an evaluation of 64 steps charged 64/38 units) and 2^47.46 word operations. (iii) Measured by us, our pair searches (Appendix C part B): the 38-step pair search given the published cells took 4,055,969,700 propagations (2^31.917 word operations = 2^20.504 units; 2,852.83 CPU-seconds, 2^34.09 units at the compression rate above), the sparse part 113,081,800 word operations (2^26.753, 0.55 CPU-seconds); Kissat seed 4 returned a new pair, not the published one (CV, M, M' and digest in Appendix C). *Result:* the largest of these figures is 2^39.15 units (Mendel et al.'s 31-step 2^38.4 evaluations; their 38-step figure is 2^37.75, our 39-step derivation 2^36.04), 38.85 bits below A_C = 2^78 target compressions; counted as word operations without the factor C = 2728 the largest is 2^50.57, 27.43 bits below 2^78. *Not measured, hence the allowance:* deriving the dense signed characteristic of rows 0..16 of the 38-step characteristic of [LZLLQZ26] itself (its search time is not published; the pair searches load its cells; a 37-step attempt with those cells unset returned no model) and the authors' failed and repeated searches; the 38.85 bits are the margin for them. *Bound for the allowance.* [LZLLQZ26] uses the CPU SAT/SMT characteristic-search tool of [LLW24a] (EUROCRYPT 2024) in the two-block framework of [LLWS26] (IACR ePrint 2026/1080): 10^5 CPU cores for 10 years at 10^10 word operations per second is 3.2 x 10^23 operations = 2^66.6 units at C = 2728, and A_C = 2^78 is 2^11.4 (about 2,600) times that ceiling. The promoted filing 6eeefb64 (sha256-r32) priced a complete measured re-run of the predecessor 35-step characteristic search with the same tool at 593,858 solver CPU-seconds over 59 solver calls; at its calibrated price of 2^32.796 primitive operations per solver CPU-second (2^21.383 units) and a 32-fold blind-rediscovery factor (as in 0ae69bcb) that is 2^45.6 units; A_C = 2^78 is 2^32.4 times that. Every cell and two-bit condition of the 38-step characteristic used here is verified on the published pair by `selftest` (Section 13.2, first item, run locally) and, on fresh pairs, by the organizer experiments `a0-online-r38` (cells of rows -4..15) and `a0-q3-r38` (step3b, all rows). For comparison, the accepted filings 0ae69bcb, 63028099, 37742a53 and 012400ff on this track charge A_C = 2^70, and the time-only filing 14b3b6ff (sha256-r38, 70.28679), which carries the same evidence, passed review at A_C = 2^70; this package charges 2^78, 256 times more. A_C = 2^84 gives 87.99564 (Appendix A.7).

*Limitations.* A_C is an allowance, not a measurement of the [LZLLQZ26] search: the published figures and our measurements are for the same kind of search (a 38- or 39-step semi-free-start characteristic and pair) but for other characteristics, on unstated or different hardware, with combined or windowed figures; we did not derive the dense signed characteristic of rows 0..16 of Table 3 (a 37-step attempt returned no model) and the authors' failed and repeated searches are in no log. The margin of 38.85 bits between the largest measured or published figure (2^39.15 units) and A_C = 2^78, the CPU-hardware ceiling (A_C is 2^11.4 times it) and 2^32.4 times the measured predecessor re-run carry the claim that the whole search is below 2^78; A_C is not lowered. A GPU branch of the bound chain (10^4 GPUs, 10 years: 2^73.3) is not the operative branch because the solver is a CPU SAT/SMT tool; A_C = 2^78 is also 4.7 bits above it. The memory of these computations is bounded in H6 (2^28 bytes).

*Evidence references.* Section 11 (ledger), this paragraph, Section 13.2 and 13.3, Appendix C (parts A and B), the organizer experiments `a0-online-r38` and `a0-q3-r38`.

**H4b - Step-1 solve (supporting).** The Step-1 solution (the published semi-free-start pair of Table 5 and its dense part S) is obtained at a total cost of at most A_S = 2^74 target compressions (the Step-1 SAT solve, reported at 2^38.3 compressions, and the completion to the SFS pair). A_S is 2^35.7 times the paper's reported Step-1 cost of 2^38.3. Limitations: a bound by comparison with the paper's reported figure, not a re-solve.

**DEV - development charge (a declared ledger item, not a premise).** DEV = 2^70 target compressions (= 2^70 x 2,728 word operations in the ledger) is charged for all development of this package, failed trials and reruns included: the exhaustive passes, end-to-end runs, replica calibration, H3 measurement, program scans and the SAT pair-search and derivation runs of Section 13.4. That development was below 10^5 CPU-seconds; at 10^10 word operations per second per CPU-second this is below 2^50 operations = 2^38.3 compressions, so 2^70 is more than 2^31 times the recorded work, which leaves room for any unlogged or discarded trial.

**H5 - counted word-RAM pricing of the bit-sliced filter (score-critical; cost reading).** A straight-line program of 256-bit primitives that evaluates E16x and its stage-3a test for 256 variants at once (bit L of each word belongs to variant L) is charged its instruction list: every load, store and spill counted, 64 registers, complements free but a mixed and/or charged one more, no fused AND-NOT; it evaluates no target compression, every compression is charged one unit.
Evidence: the programs are generated and counted by `experiments/a0lean38.py` (`build_e16`, `Prog.schedule`, `run_prog`), equal to the scalar definition on every checked lane (Section 13). The same reading in the base was accepted by the AI review lanes with no organizer ruling cited. With a scalar evaluation (38 operations per variant) the claim would be about 2.79 bits higher (93.99125 at the earlier q3_model 2^-101.05, 64 classes).

**H6 - memory (score-critical under a rule that prices it; otherwise a reported metric).** Peak = max(online, preprocessing) = 2^28 bytes (claim 28); the preprocessing bound is 2^28 bytes from the measured solver peaks and the assumptions of Section 14 (peak memory). The online program needs exactly 1,044,992 bytes (log2 = 19.99506046703272; 3,584 under 2^20): Section 14 lists every component, with the code counted at 32 bytes (one word) per instruction and 15 spill slots actually allocated rather than the 40-slot upper budget. The online figure covers the online program, its tables and the precomputation of Section 5.3 (the member lists of the classes are produced one class at a time from the 90 descriptors; no array indexed by a 32-bit quantity is built).
Not included: the allowance computations of H4 (the paper's solver runs and our development), as in the base. Limitations: the machine model does not define a code size; with 4 bytes per instruction the code (10,603 instructions) would be 42 KB instead of 339 KB, with 32 bytes it is already counted in full.

## 13. Evidence and runs

### 13.1 End to end on real first blocks (`e2e38m.c`, Appendix A.3)

The runs of this section are those of the 64-class schedule of the earlier filing (e2e38m.c reads its class list; the filters of the added classes are the same code on other c7 values and masks, and are exercised by `selftest`, the hit distribution of Appendix A.2 and `a0-online-r38`). Random M0, CV1 = F_38(IV, M0) (38 steps, feed-forward), the 64 W7 tests (a bitmap of F7), E16x of every variant of every passing class by the closed form of Section 6, stage 3a (12 bits), the exact row-16 set; every row-16 pass is printed with M0 and checked in Python (`verify_r16.py`, Appendix A.3):
CV1 equals F_38(IV, M0), a0 is in G and in a selected class, W7 is in F7, every cell of rows -4..16 and every two-bit condition closing at rows 8..16 holds (none reaches row 17, as expected at 2^-17).

| seed | first blocks | passing classes (expected) | good pairs (ratio) | stage-3a passes (ratio) | row-16 passes (expected; z) | exact checks |
|---|---|---|---|---|---|---|
| 19 | 2^22 | 17,972,582 (17,956,864) | 69,014,714,880 (1.0009) | 16,849,545 (1.0009) | 468 (513.75; -2.02) | 468, 0 failures |
| 23 | 2^23 | 35,894,449 (35,913,728) | 137,834,684,160 (0.9995) | 33,644,771 (0.9993) | 1062 (1027.50; +1.08) | 1062, 0 failures |
| 17 | 2^24 | 71,766,725 (71,827,456) | 275,584,224,000 (0.9992) | 67,279,849 (0.9991) | 2031 (2055.00; -0.53) | 2031, 0 failures |

### 13.2 Self-test (`python3 experiments/a0lean38.py selftest`, 11 s)

```text
ok  published pair: equal 38-step outputs (hash 5d9ca5f4 ...), every printed cell and condition of rows -4..37
ok  published A0 is in G, c7 = 8f6c89c5, Step 2 returns the published words
ok  90 classes of 3840 members in 7 plane programs, distinct c7 values, masks ['0x91eb5491', '0x91eb54d1', '0x91eb55d1']
ok  row-16 set: 32 words pass the full row-16 test; 3000 random words with the ten cell bits and 1280 two-bit neighbours of the members agree with the affine description
ok  the 12 prefilter bits are shared by all 32 words
ok  W7 decision tree agrees with the definition of F7 on 8000 words
ok  step 3b on the published pair: all rows pass, exact event, traces equal the reference (2865 operations)
ok  counted rows 19 and 20 equal the definition: row 19 accepts exactly the patterns ['0x40832', '0x10000010', '0x20000c12', '0x30040430'] of 512, row 20 exactly when E20[29] = E19[29]
ok  bit-sliced prefilter equals the scalar definition on 768 lanes of each of the 7 plane programs ([1410, 1413, 1421, 1426, 1425, 1426, 1425] instructions)
ok  online program: first block 3, one class of 3840 good pairs, 0 lane mismatches
ok  q3 replicate: estimate 2^-96.92, 11 verified 38-step semi-free-start collisions accepted by step3b, 0 failed checks, 4 with another E19 pattern
ok  cap test on every block: V > V_MAX halts at the next block start, before its 90 W7 tests
ok  512 embedded variants are in G and in the selected classes
```

A longer development run of the W7 tree against the definition of F7 (`w7check.py`, Appendix A.6) compared 1,100,000 words (random words and words forced into each of the three families): 0 disagreements.

### 13.3 Organizer experiments (`experiments/a0lean38.py`)

- `a0-online-r38` (H1, H5): trials 0..5 run the counted online program on seed-drawn first blocks (two uniform words from SHAKE-256 of the seed per first block; real 38-step compressions) until a first block has a passing class (at most 16 first blocks), processing one passing class (3840 good pairs, 15 bit-sliced batches): the stage-3a decision of every lane is compared with the scalar definition,
  every passing lane is extracted from the stored planes and compared with the class member, the hit list is compared with the definition of F7 for all 90 classes, and 8 good pairs are checked against every cell of rows -4..15. A trial returns the complete 128-byte messages M0||M1 and M0||M1' of its first good pair iff all checks passed. Trials 6..255 return no pair by design. Local emulation of the organizer request (seeds sha256(id|trial), no container): 6 pairs returned, 13 first blocks, 128 passing classes in the final first blocks of the trials, 23,040 good pairs checked lane by lane, 3 stage-3a passes, 0 row-16 passes, filter mismatches 0, cell mismatches 0, lane mismatches 0, 154,458 counted operations; 1.0 s, byte-identical on the second run.
- `a0-q3-r38` (H2): the organizer replica of q3 for the accepted event (Section 7.3). Trials 0..19 are replicates, each returning its first verified 38-step semi-free-start collision (CV1||M1, CV1||M1', 96 bytes each) that the counted program `step3b` also accepts (so the organizer's run executes the new tests of rows 19 and 20 and the output comparison on real successes, most of them with an E19 pattern other than the published one); trial 20 returns a pair iff the pooled mean of the 20 linear estimates is at least 2^-98.4338 and no check failed. Trials 21..255 return no pair by design. Local emulation of the organizer request: 21 pairs returned (20 replicates with a success and trial 20), 178 successes (139 of them with an E19 pattern other than the published one), every one rebuilt, verified and accepted by `step3b`, 0 failed checks, estimates 2^-100.21 to 2^-96.01, log2 of the pooled mean -97.620 (threshold -98.4338); 7.4 s, byte-identical on the second run.
- Both experiments are deterministic (the second execution of the organizer is byte-identical). Locally (Python 3.14) `a0-online-r38` takes 1.0 s and `a0-q3-r38` 7 to 13 s (the second under machine load; the q3 replica code is unchanged from the earlier version and returns the same 21 pairs and the same pooled mean); the organizer's intake on a scratch clone of its code (pinned Python 3.12 container, 128 MB, 20-second limit per experiment, each experiment run twice) of the earlier version took 18 s in all, returned 6 and 21 pairs with byte-identical replays, and its judge evidence was 230,358 bytes (this version: Section A.7).

### 13.4 Development computation

Below 10^5 CPU-seconds in total (the exhaustive passes, the end-to-end runs, the calibration of the replica, the H3 measurement, the scans of the program), far inside the charge DEV = 2^70 (Section 11). Machine: Windows 10 with Python 3.14 for the programs in Python, and an Ubuntu 26.04 distribution with 24 cores, 46 GB and gcc for the programs in C.

### 13.5 The other variants of a successful first block (H3; `h3gen.py`, `h3count.c`, Appendix A.8)

*The law of a success.* Fix a variant a0. Lemma 4.1 is a bijection between CV1 and W0..W7 (given S), and the inverse expansion is a bijection between W0..W5 and W16..W21 (given W6..W15). Under H1, CV1 is uniform, so (W16..W21, W6, W7) is uniform and, for good pairs, W7 is uniform on F7 (Lemma 5.1);
a0 is uniform on the selected variants because every first block tries all of them. Hence the law of (CV1, a0) given a success is the law of (rows 16..21, W6, W7, a0) given that rows 16..37 hold, mapped back to CV1: exactly what the sampler of Section 7.3 draws (constant weights, so its surviving particles are draws of the conditional law, correlated through common ancestors).

*Measurement.* `h3gen.py` runs that sampler with 512 particles (the proposal counts of Section 7.3) and a0 drawn from all 245,760 variants, 8 independent runs of 80 replicates, every success rebuilt and verified as a 38-step semi-free-start pair; `h3count.c` takes each success (CV1, a0) and tries every other selected variant b0 of that CV1:
b0's class passes iff c7 - A_{-1} is in F7; for a good b0 it computes E16x by the closed form, the 12-bit prefilter and the exact 32-word set. Each success must itself pass row 16 (self failures: 0).

| run | successes | other good pairs | other stage-3a passes (independent expectation) | other row-16 passes (independent expectation) |
|---|---|---|---|---|
| 1 | 4,088 | 301,147,912 | 73,681 (73522.4) | 5 (2.24) |
| 2 | 4,204 | 307,042,196 | 74,943 (74961.5) | 3 (2.29) |
| 3 | 4,225 | 308,102,015 | 74,839 (75220.2) | 1 (2.30) |
| 4 | 4,183 | 307,337,897 | 75,205 (75033.7) | 0 (2.29) |
| 5 | 4,212 | 308,539,788 | 75,484 (75327.1) | 3 (2.30) |
| 6 | 4,051 | 297,530,669 | 72,492 (72639.3) | 2 (2.22) |
| 7 | 4,088 | 301,151,752 | 74,062 (73523.4) | 2 (2.24) |
| 8 | 4,171 | 304,669,109 | 74,686 (74382.1) | 5 (2.27) |
| **total** | **33,222** | **2,435,521,338** | **595,392 (594609.7; ratio 1.0013)** | **21 (18.15; ratio 1.16, z = +0.67)** |

E[R_f - 1 | success] is estimated by 21 / 33,222 = 2^-10.63; one-sided 99% upper bounds: Poisson 2^-9.92; Student t over the 8 runs (7 degrees of freedom; the runs are independent, the successes within a run are not) 2^-9.85. H3 assumes 2^-8.5. The conditional number of good pairs (73310.5 per success, 4.46 g) is larger than the unconditional g because the
W7 tests of one first block are positively correlated (Section 5.3); the measurement includes this. The base's measurement (65,030 successes: 41 passes, 2^-10.63; 2^-10.12 and 2^-9.92) agrees with ours.

## 14. Memory and advice

| component | bytes |
|---:|---:|
| batch planes of the 90 classes (15 batches, one word per variable bit of a0) | 675,840 |
| shared-constant words of the classes | 11,520 |
| per-first-block broadcast planes (7 x 32 words) | 7,168 |
| spill slots of the plane programs (15 used; the 40-word figure was only a budget) | 480 |
| scalars, counters, hit list and F7 constants (64 words) | 2,048 |
| class table (c7, base, mask and program number: 3 words each) | 8,640 |
| code of the seven plane programs: 9,946 instructions at 32 bytes | 318,272 |
| code of the W7 test loop: 57 instructions at 32 bytes (the 52-instruction tree once, 5 for the loop) | 1,824 |
| code of the other routines (first-block words, scalars, planes, lane scan, row 16, step 3b, loops): 600 instructions at 32 bytes | 19,200 |
| **total** | **1,044,992 bytes** (log2 = 19.99506046703272; under 2^20 = 1,048,576 by 3,584 bytes; online figure; the peak is 2^28, see below) |

If the hit list kept one 32-byte word per class instead of the 64-word lump, 832 bytes more: 1,046,624, still under 2^20. The model has no code size of its own; 5 instruction slots for the loop is the figure used, and any loop whose static size exceeds this by fewer than 87 instructions stays under 2^20.

The precomputation (Section 5.3) builds one class at a time: it tests every subset s of the mask (at most 2^17 candidates, 3840 survivors, 15 KB) and writes the 15 x (varying bits) planes of the class; nothing larger than a class is held. The seven programs are generated once (about 1,400 instructions each). The online program touches only the components above.
Nonuniform advice: the characteristic, S, L*, the 90 class descriptors (1,080 bytes) and the three shapes: below 2^13 bytes, charged through the allowances (H4). The 512 embedded variants of the replica are not part of the attack; they are in the experiment source only.

**Peak memory: online and preprocessing (H6).** The peak is max(online, preprocessing). Online: 1,044,992 bytes (table above). Preprocessing bound: 2^28 bytes = 268,435,456, derived below. Online and preprocessing do not run at the same time, so peak = 2^28 bytes (log2 = 28).
(a) Measured. Single-thread Kissat 4.0.3 and CaDiCaL 2.1.3 (`/usr/bin/time -v`, 600 s cap, nice 10, four runs at once on separate cores) on the two Appendix C pair-search files: file a `dense_chi38_e16_new.cnf` (110,437 variables, 383,938 clauses) and file b `dense_chi38_elist_new.cnf` (110,469 variables, 385,435 clauses), the circuit of Appendix C part B with the file-specific pins or selection. Maximum resident set size: Kissat a 115,688 kB (118,464,512 bytes, 2^26.82), Kissat b 118,648 kB (121,495,552 bytes, 2^26.86), CaDiCaL b 136,468 kB (139,743,232 bytes, 2^27.06; this run found the pair, 8:28.98), CaDiCaL a 145,868 kB (149,368,832 bytes, 2^27.15). Largest: 149,368,832 bytes = 2^27.15. The logs are not shipped (evidence budget, declared-file list); the four `Maximum resident set size` values are quoted here.
Further, on the characteristic-derivation instance itself (the 39-step window search of Appendix C part A, the CNF `ex39_search_90.cnf` of 132,265 variables and 771,857 clauses that CryptoMiniSat 5.11.21 solved in 772.58 s on 12 threads), single-thread runs (`/usr/bin/time -v`, 900 s cap, nice 10, run side by side): CaDiCaL 2.1.3 found a model in 1:52.11 with maximum resident set size 193,412 kB (198,053,888 bytes, 2^27.56); Kissat 4.0.3 found a model in 7:33.76 with 184,016 kB (188,432,384 bytes, 2^27.49). Largest measured preprocessing peak: 198,053,888 bytes = 2^27.56.
(b) Characteristic derivation (H4a, Appendix C part A): measured above on its own CNF with single-thread CaDiCaL and Kissat, peak 2^27.56 bytes. The operation count of the preprocessing (the allowances A_C, A_S and the charge DEV, in target compressions) does not depend on the number of threads, and this package declares that every preprocessing solver run is single-threaded; the recorded 12-thread CryptoMiniSat run is the timing evidence of H4a only and its memory is not claimed. Bound: 2^27.56 < 2^28 bytes.
(c) Step-1 solve (H4b) and development (DEV): the package gives no measured basis for their memory. Declared statement: the development runs the same solver family (Kissat, CaDiCaL), single-threaded, on instances no larger than the measured characteristic-derivation instance (largest peak 2^27.56), together with the package's own Python and C programs; the Step-1 solve is declared to run single-threaded solvers of the same family (SAT solves of the dense part and of the pair-search circuit, no larger than the instances of (a) and (b), whose largest peak is 2^27.56); both are covered by the same 2^28-byte envelope (1.35 times the largest measured peak).
Not measured: the resident size of the Step-1 solve and of the development; (c) rests on the stated assumption. The 12-thread CryptoMiniSat run is not claimed to fit the envelope. Score under the rule S = time + max(0, memory - 20): 87.90375 + (28 - 20) = 95.90375.

## 15. Limitations

- H1, H2, H3 are premises; q3 is a product of two Monte-Carlo lower bounds (the base's printed-event estimate and our preregistered gain), replicated for the accepted event by our own code and by the organizer experiment `a0-q3-r38` to about 0.3 bit; H3 is measured on sampled successes of the printed event (the base's 65,030 and our 33,222), not on real collisions and not again for the accepted event; no collision has been found and none is expected at our scale.
- The gain of Section 7.4 was measured with our own tool (not shipped); the shipped replica, an independent implementation, agrees with it. Not done for this version: a solver re-run of the whole system with the four patterns and the tie, and a fresh reading of the cells from the paper's tables (the tables are those of the earlier filings, verified on the published pair).
- The replica's W23 classes come from a development run; classes never seen there are not proposed (the replica is a lower bound).
- The published characteristic and SFS pair are advice under allowances (H4a, H4b) and the development charge DEV; we did not rerun the paper's searches, and the memory of the allowance computations is bounded in H6 by 2^28 bytes (measured for the pair searches, assumed for the characteristic derivation, Step-1 solve and development). A_C = 2^78 is an allowance, not a measurement of the [LZLLQZ26] characteristic search: we measured a 39-step characteristic derivation with the authors' tool (2^36.04 units), our 38-step pair searches and the sparse part (Appendix C), and compared with published figures (largest 2^39.15 units, 38.85 bits under A_C); we did not derive the dense signed characteristic of rows 0..16 of Table 3 and the authors' failed and repeated searches are in no log (H4a).
- The single element of L* is the published one; the paper's stated 2^2 freedom is not reproduced for S. With q3 = 2^-102 (the paper's text count of 102 conditions) log2 T would be 92.15605.
- The bit-sliced filter relies on H5 (no organizer ruling is cited); the memory figure relies on H6, on the 2^28-byte preprocessing envelope (unmeasured for the CryptoMiniSat run, the Step-1 solve and the development) and, for the online part, on the instruction size chosen there (it is 2,784 bytes under 2^20; the loop of the W7 test and the dispatch to the class's program are counted, not an instruction list from the allocator).
- The lane scan and the preprocessing are counted code but are not part of an organizer experiment at full size; their counts are produced by `calibrate` and printed in Appendix A.7. The step-3b path is run by `a0-q3-r38` on every replicate success.

## Appendix A. Local evidence programs and records

All programs are ours. `a0lean38.py` is the shipped experiment source; the others are evidence code (not shipped). Python 3.14 and C on the machine named in Section 13.4, C compiled with `gcc -O3 -march=native -fopenmp`.

### A.1 `fam38.c`: the exhaustive passes over G, the c7 classes and F7 (4,460 bytes)

Enumerates all 2^32 values of a0, keeps those in G (W8's cell and its three two-bit conditions), computes c7 for each, sorts the 2^26 pairs, reports the runs, regenerates the 64 class descriptors of `classes.txt` (c7, base, mask) and checks them, and counts F7. Output (the earlier version of the pass; the pass writes all 180 size-3840 classes, and Grok's run of an independent enumeration of all 2^32 values of a0 (not shipped) found the same 180 classes, the same three masks (96, 52 and 32 classes), the same 102,696 c7 values and |F7|, and the 90 used):

```text
|G| = 67108864 (2^26 = 67108864), modular s0 difference of W8 wrong on 0
distinct c7 = 102696, max class size = 3840
classes of size >= 3840: 180 (size 3840: 180)
descriptors checked: 64, bad 0
first 64 size-3840 runs by c7 vs descriptors: mismatches 0 (selected 64)
|F7| = 287309824
```

```c
// fam.c - exhaustive check of the A0-variant family G, its c7 classes and the exact filter F7 (own code).
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
typedef uint32_t u32; typedef uint64_t u64;
static inline u32 ror(u32 x, int n){ return (x>>n)|(x<<(32-n)); }
static inline u32 S0(u32 x){ return ror(x,2)^ror(x,13)^ror(x,22); }
static inline u32 S1(u32 x){ return ror(x,6)^ror(x,11)^ror(x,25); }
static inline u32 s0(u32 x){ return ror(x,7)^ror(x,18)^(x>>3); }
static inline u32 MAJ(u32 x,u32 y,u32 z){ return (x&y)^(x&z)^(y&z); }
static inline u32 CH(u32 x,u32 y,u32 z){ return (x&y)^(~x&z); }
#define C4 0xab1f01f0u
#define W8C 0xa1be17b9u
#define D8 0xfbc00800u
#define T8 0xfe7f8000u
#define SE7 0xe2e9b205u
#define SE6 0x0c1c24b9u
#define SE5 0x1e847683u
#define A3 0xd374b0d8u
#define A2 0x479b4dc8u
#define A1 0xda6c35e0u
#define K7 0xab1c5ed5u
#define CM 71305216u
#define CV 71303168u
#define CD 71305216u
static inline int inG(u32 a0){
  u32 w = W8C - (a0 + C4), y = w + D8;
  if ((w & CM) != CV || (w ^ y) != CD) return 0;
  int b0=(w>>0)&1,b28=(w>>28)&1,b30=(w>>30)&1,b9=(w>>9)&1,b1=(w>>1)&1,b18=(w>>18)&1;
  return b0!=b28 && b30!=b9 && b1==b18;
}
static inline u32 c7of(u32 a0){ u32 e4=a0+C4; return SE7 - 2*A3 + S0(A2) + MAJ(A2,A1,a0) - S1(SE6) - CH(SE6,SE5,e4) - K7; }
typedef struct { u32 c7, a0; } pr;
static int cmp(const void*a,const void*b){ const pr*x=a,*y=b; if(x->c7!=y->c7) return x->c7<y->c7?-1:1; return x->a0<y->a0?-1:(x->a0>y->a0); }
int main(int argc,char**argv){
  u64 n=0; pr *v = malloc(sizeof(pr)*(1u<<26));
  u64 ds0bad=0;
  for (u64 a=0;a<(1ull<<32);a++){ u32 a0=(u32)a; if(inG(a0)){ if(n>=(1u<<26)){ fprintf(stderr,"more than 2^26\n"); return 1;} v[n].c7=c7of(a0); v[n].a0=a0; n++;
       u32 w = W8C - (a0 + C4), y = w + D8; if ((s0(y)-s0(w))!=T8) ds0bad++; } }
  printf("|G| = %llu (2^26 = %u), modular s0 difference of W8 wrong on %llu\n",(unsigned long long)n,1u<<26,(unsigned long long)ds0bad);
  qsort(v,n,sizeof(pr),cmp);
  // runs
  u64 nr=0, i=0; u64 hist[8192]; memset(hist,0,sizeof hist); u32 maxsz=0;
  typedef struct { u64 start; u32 size, c7; } run;
  run *rs = malloc(sizeof(run)*200000);
  while(i<n){ u64 j=i; while(j<n && v[j].c7==v[i].c7) j++; rs[nr].start=i; rs[nr].size=(u32)(j-i); rs[nr].c7=v[i].c7; nr++; if(j-i<8192) hist[j-i]++; if(j-i>maxsz) maxsz=(u32)(j-i); i=j; }
  printf("distinct c7 = %llu, max class size = %u\n",(unsigned long long)nr,maxsz);
  u64 big=0; for(int s=3840;s<8192;s++) big+=hist[s]; printf("classes of size >= 3840: %llu (size 3840: %llu)\n",(unsigned long long)big,(unsigned long long)hist[3840]);
  { FILE*g=fopen("allclasses.txt","w"); for(u64 k=0;k<nr;k++) if(rs[k].size==3840){ u32 b0=v[rs[k].start].a0, m=0; for(u32 t=0;t<3840;t++) m|=v[rs[k].start+t].a0^b0; fprintf(g,"%08x %08x %08x\n",rs[k].c7,b0&~m,m);} fclose(g);}
  // descriptors
  FILE*f=fopen("classes.txt","r"); unsigned c7,base,mask; int nc=0, bad=0;
  while(fscanf(f,"%x %x %x",&c7,&base,&mask)==3){
    // find run
    u64 k; for(k=0;k<nr;k++) if(rs[k].c7==c7) break;
    if(k==nr){ printf("class %08x not found\n",c7); bad++; continue; }
    // members from descriptor: base ^ s, s subset of mask
    u32 s=0; u32 cnt=0, hit=0;
    do { u32 a=base^s; if(inG(a)&&c7of(a)==c7){ cnt++; // check membership in run
          // binary search in run
          u64 lo=rs[k].start, hi=rs[k].start+rs[k].size; while(lo<hi){ u64 mid=(lo+hi)/2; if(v[mid].a0<a) lo=mid+1; else hi=mid; }
          if(lo<rs[k].start+rs[k].size && v[lo].a0==a) hit++; }
      s=(s-mask)&mask; } while(s!=0);
    if(cnt!=3840 || hit!=3840 || rs[k].size!=3840) { printf("class %08x: desc count %u hit %u run size %u  BAD\n",c7,cnt,hit,rs[k].size); bad++; }
    nc++;
  }
  printf("descriptors checked: %d, bad %d\n",nc,bad);
  // the 64 largest by (size desc, c7 asc)
  // selection check: all runs of size 3840 sorted by c7; the first 64 must be the descriptors' c7
  int idx=0; rewind(f); unsigned want[64]; int nw=0; while(fscanf(f,"%x %x %x",&c7,&base,&mask)==3) want[nw++]=c7;
  int sel=0, mism=0; for(u64 k=0;k<nr && sel<64;k++){ if(rs[k].size==maxsz && maxsz==3840){ if(rs[k].c7!=want[sel]) mism++; sel++; } }
  printf("first 64 size-3840 runs by c7 vs descriptors: mismatches %d (selected %d)\n",mism,sel);
  // F7 size
  u64 nf=0; for(u64 w=0;w<(1ull<<32);w++){ u32 x=(u32)w; if(((s0(x+0x20000000u)-s0(x))==0x03bff800u)) nf++; }
  printf("|F7| = %llu\n",(unsigned long long)nf);
  return 0; }
```

### A.2 `hits38.c`: the exact distribution of the number of passing classes (1751 bytes)

For every value of A_{-1} (all 2^32) the number k of classes c (the 90 classes of `classes.txt`) with c7_c - A_{-1} in F7. Output (k, number of values of A_{-1}); the pass over the 64 classes of the earlier version gave 0 for 3,013,859,374 values, mean 4.28125, second moment 81.606 and maximum 32:

```text
0 2992758256
1 14982596
2 29466208
3 9487100
4 41863120
5 280912
6 36005328
7 1384098
8 23652456
9 314348
10 9213978
11 1455818
12 190149696
13 111234
14 201331328
15 350198
16 114181246
17 137312
18 16670376
19 220314
20 32708046
21 61102
22 47246654
23 14831352
24 48762716
25 2474
26 16257032
27 3410
28 40646914
29 2254
30 40644516
31 3928
32 369709316
33 2842
34 9154
35 7516
36 10924
37 4008
38 22200
39 15016
total 4294967296 sum_k 25857884160 sum_k2 636623874688  (90*|F7| = 25857884160)
```

```c
// hits.c - exact distribution of the number of passing classes per first block under H1 (a = A_{-1} uniform): for each of the 2^32
// values of a count the classes c with c7_c - a in F7.  Own code.  Output: histogram of the count, E, E^2, P(any).
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <omp.h>
typedef uint32_t u32; typedef uint64_t u64;
static inline u32 ror(u32 x, int n){ return (x>>n)|(x<<(32-n)); }
static inline u32 s0(u32 x){ return ror(x,7)^ror(x,18)^(x>>3); }
int main(){
  u32 c7[90]; int n=0; FILE*f=fopen("classes.txt","r"); unsigned a,b,c; while(fscanf(f,"%x %x %x",&a,&b,&c)==3) c7[n++]=a;
  fclose(f);
  u64 words = 1ull<<26; uint64_t *bm = calloc(words, 8);   // 2^32 bits
  #pragma omp parallel for schedule(static)
  for (u64 q=0;q<words;q++){ u64 v=0; for(int k=0;k<64;k++){ u32 w=(u32)(q*64+k); if (((s0(w+0x20000000u)-s0(w))==0x03bff800u)) v|=1ull<<k; } bm[q]=v; }
  u64 nf=0; for(u64 q=0;q<words;q++) nf+=__builtin_popcountll(bm[q]);
  printf("|F7| = %llu\n",(unsigned long long)nf);
  u64 hist[91]; memset(hist,0,sizeof hist);
  #pragma omp parallel
  { u64 h[91]; memset(h,0,sizeof h);
    #pragma omp for schedule(static)
    for (long long x=0;x<(1ll<<32);x++){ u32 av=(u32)x; int k=0; for(int i=0;i<n;i++){ u32 w=c7[i]-av; k+=(bm[w>>6]>>(w&63))&1; } h[k]++; }
    #pragma omp critical
    for(int i=0;i<91;i++) hist[i]+=h[i];
  }
  u64 tot=0, s1=0, s2=0; for(int k=0;k<=90;k++){ tot+=hist[k]; s1+=hist[k]*k; s2+=hist[k]*(u64)k*k; if(hist[k]) printf("%d %llu\n",k,(unsigned long long)hist[k]); }
  printf("total %llu sum_k %llu sum_k2 %llu  (90*|F7| = %llu)\n",(unsigned long long)tot,(unsigned long long)s1,(unsigned long long)s2,(unsigned long long)(90*nf));
  return 0; }
```

### A.3 `e2e38m.c`: the attack's filters on real first blocks, and `verify_r16.py`

`consts_m.h` is generated from `a0lean38.py` (the values of S, C16, the row-16 set and the mask of the 12 tested bits):

```c
// consts_m.h - generated from a0lean38.py (values of S and of the row-16 set)
#define C4 0xab1f01f0u
#define W8C 0xa1be17b9u
#define D8 0xfbc00800u
#define CM 71305216u
#define CV 71303168u
#define CD 71305216u
#define SE7 0xe2e9b205u
#define SE6 0xc1c24b9u
#define SE5 0x1e847683u
#define SA1 0xda6c35e0u
#define SA2 0x479b4dc8u
#define SA3 0xd374b0d8u
#define C16 0xfe314838u
#define R16B 0x481b02f9u
#define R16F 0x82405u
#define TVAL 0x481b02f9u
#define PMASK 0x1dbf8u
```

```c
// e2e38m.c - the attack's own filters on real first blocks (own code).  Random M0, CV1 = F_38(IV, M0) (38 steps, feed-forward), the 64 W7
// tests (F7 bitmap), E16x of every variant of every passing class by the closed form of Section 6, the 14-bit prefilter, the exact row-16
// set.  Every row-16 pass is printed (first block words, a0) for an exact check in Python.  Usage: ./e2e38m <seed> <log2 first blocks>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <omp.h>
typedef uint32_t u32; typedef uint64_t u64;
static inline u32 ror(u32 x, int n){ return (x>>n)|(x<<(32-n)); }
static inline u32 S0(u32 x){ return ror(x,2)^ror(x,13)^ror(x,22); }
static inline u32 S1(u32 x){ return ror(x,6)^ror(x,11)^ror(x,25); }
static inline u32 s0(u32 x){ return ror(x,7)^ror(x,18)^(x>>3); }
static inline u32 s1(u32 x){ return ror(x,17)^ror(x,19)^(x>>10); }
static inline u32 MAJ(u32 x,u32 y,u32 z){ return (x&y)^(x&z)^(y&z); }
static inline u32 CH(u32 x,u32 y,u32 z){ return (x&y)^(~x&z); }
static const u32 K[64]={0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2};
static const u32 IVW[8]={0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19};
static void comp38(const u32*cv,const u32*w16,u32*out){
  u32 W[38]; for(int i=0;i<16;i++)W[i]=w16[i]; for(int i=16;i<38;i++)W[i]=s1(W[i-2])+W[i-7]+s0(W[i-15])+W[i-16];
  u32 a=cv[0],b=cv[1],c=cv[2],d=cv[3],e=cv[4],f=cv[5],g=cv[6],h=cv[7];
  for(int i=0;i<38;i++){ u32 t1=h+S1(e)+CH(e,f,g)+K[i]+W[i], t2=S0(a)+MAJ(a,b,c); h=g;g=f;f=e;e=d+t1;d=c;c=b;b=a;a=t1+t2; }
  out[0]=cv[0]+a;out[1]=cv[1]+b;out[2]=cv[2]+c;out[3]=cv[3]+d;out[4]=cv[4]+e;out[5]=cv[5]+f;out[6]=cv[6]+g;out[7]=cv[7]+h; }
// S constants (Python prints them)
#include "consts_m.h"
static u32 *mem; static int ncls; static u32 c7s[64];
static inline u64 sm(u64 *s){ u64 z=(*s+=0x9e3779b97f4a7c15ull); z=(z^(z>>30))*0xbf58476d1ce4e5b9ull; z=(z^(z>>27))*0x94d049bb133111ebull; return z^(z>>31); }
int main(int argc,char**argv){
  u64 seed=argc>1?strtoull(argv[1],0,10):1; int lg=argc>2?atoi(argv[2]):20; u64 nfb=1ull<<lg;
  // F7 bitmap
  u64 words=1ull<<26; u64*bm=calloc(words,8);
  #pragma omp parallel for schedule(static)
  for(u64 q=0;q<words;q++){ u64 v=0; for(int k=0;k<64;k++){ u32 w=(u32)(q*64+k); if((s0(w+0x20000000u)-s0(w))==0x03bff800u) v|=1ull<<k; } bm[q]=v; }
  // classes
  mem=malloc(4*3840*64); FILE*f=fopen("classes.txt","r"); unsigned c7,base,mask; ncls=0;
  while(fscanf(f,"%x %x %x",&c7,&base,&mask)==3){ u32 s=0; int n=0; do{ u32 a=base^s; u32 w=W8C-(a+C4), y=w+D8;
      if((w&CM)==CV && (w^y)==CD){ int b0=w&1,b28=(w>>28)&1,b30=(w>>30)&1,b9=(w>>9)&1,b1=(w>>1)&1,b18=(w>>18)&1;
        if(b0!=b28&&b30!=b9&&b1==b18){ u32 e4=a+C4; u32 c=SE7-2*SA3+S0(SA2)+MAJ(SA2,SA1,a)-S1(SE6)-CH(SE6,SE5,e4)-0xab1c5ed5u; if(c==c7){ mem[ncls*3840+n]=a; n++; } } }
      s=(s-mask)&mask; }while(s); if(n!=3840){ fprintf(stderr,"class %08x has %d\n",c7,n); return 1; } c7s[ncls++]=c7; }
  fclose(f);
  u64 hist[65]; memset(hist,0,sizeof hist); u64 good=0, pre=0, r16=0, nhit=0;
  #pragma omp parallel
  { u64 h[65]; memset(h,0,sizeof h); u64 g=0,p=0,r=0,nh=0; u64 st=seed*0x1000193ull+omp_get_thread_num()*7919+12345;
    #pragma omp for schedule(dynamic,4096)
    for(u64 it=0; it<nfb; it++){
      u32 m0[16]; for(int i=0;i<16;i+=2){ u64 x=sm(&st); m0[i]=(u32)x; m0[i+1]=(u32)(x>>32); }
      u32 cv[8]; comp38(IVW,m0,cv);
      u32 a=cv[0],b=cv[1],c=cv[2],d=cv[3],e=cv[4],ff=cv[5],gg=cv[6],hh_=cv[7];
      int k=0; int hit[64];
      for(int i=0;i<64;i++){ u32 w=c7s[i]-a; if((bm[w>>6]>>(w&63))&1) hit[k++]=i; }
      h[k]++;
      if(k){ u32 PP=a&b, QQ=a|b, HH=d-S0(a)-MAJ(a,b,c), EF=e^ff, FF=ff, K1=SA1-gg-0x71374491u;
             u32 kap0=HH-d-hh_-S1(e)-CH(e,ff,gg)-0x428a2f98u, KP=C16+kap0;
        for(int q=0;q<k;q++){ u32*mm=mem+hit[q]*3840;
          for(int t=0;t<3840;t++){ u32 a0=mm[t]; u32 E0=a0+HH; u32 T=S0(a0)+(PP|(a0&QQ))+S1(E0)+(FF^(E0&EF)); u32 W1=K1-T; u32 E16=KP+a0+s0(W1);
            g++; if(((E16^TVAL)&PMASK)==0){ p++; u32 dd=(E16-R16B); if((dd&~R16F)==0){ r++;
               #pragma omp critical
               { printf("R16 %08x %08x %08x %08x %08x %08x %08x %08x %08x\n",cv[0],cv[1],cv[2],cv[3],cv[4],cv[5],cv[6],cv[7],a0); for(int i=0;i<16;i++)printf("M %08x\n",m0[i]); } } } } } }
      nh+=k;
    }
    #pragma omp critical
    { for(int i=0;i<65;i++) hist[i]+=h[i]; good+=g; pre+=p; r16+=r; nhit+=nh; }
  }
  printf("FB %llu\nhits_total %llu\ngood_pairs %llu\nprefilter_passes %llu\nrow16_passes %llu\n",(unsigned long long)nfb,(unsigned long long)nhit,(unsigned long long)good,(unsigned long long)pre,(unsigned long long)r16);
  for(int i=0;i<65;i++) if(hist[i]) printf("H %d %llu\n",i,(unsigned long long)hist[i]);
  return 0; }
```

Outputs (the lines of the row-16 passes, `R16` and sixteen `M` lines each, are omitted here; they are checked by the script below):

```text
seed 19:
FB 4194304
hits_total 17972582
good_pairs 69014714880
prefilter_passes 16849545
row16_passes 468
seed 23:
FB 8388608
hits_total 35894449
good_pairs 137834684160
prefilter_passes 33644771
row16_passes 1062
seed 17:
FB 16777216
hits_total 71766725
good_pairs 275584224000
prefilter_passes 67279849
row16_passes 2031
```

`verify_r16.py` (reads those lines) and its output on both runs:

```python
# verify_r16.py - exact check of the row-16 passes printed by e2e38m (R16 line: CV1 and a0; sixteen M lines: the first block).  Run next to a0lean38.py.
import sys
import a0lean38 as T
lines = open(sys.argv[1]).read().split('\n'); recs = []; i = 0
while i < len(lines):
    if lines[i].startswith('R16 '):
        t = lines[i].split(); cv = [int(x, 16) for x in t[1:9]]; a0 = int(t[9], 16)
        recs.append((cv, a0, [int(lines[i + 1 + k].split()[1], 16) for k in range(16)])); i += 17
    else: i += 1
cvbad = vbad = w7bad = cellbad = 0; deepest = {}
for cv, a0, m0 in recs:
    cvbad += T.compress(T.IV, m0) != cv
    vbad += not T.variant_ok(a0)
    wx, wy = T.words_from_cv(cv, a0); mx = wx + [T.PMX[14], T.PMX[15]]; my = wy + [T.PMY[14], T.PMY[15]]
    w7bad += not T.inF7(mx[7])
    tx, ty = T.trace(cv, mx), T.trace(cv, my)
    ok = all(T.rowok(tx, ty, i) for i in range(-4, 17))
    for (k1, i1, b1, eq, k2, i2, b2, row) in T.X2:
        if 8 <= row <= 16 and (((tx[k1][i1] >> b1) ^ (tx[k2][i2] >> b2)) & 1) != (0 if eq else 1): ok = False
    cellbad += not ok
    r = 16
    while r < 37 and T.rowok(tx, ty, r + 1): r += 1
    deepest[r] = deepest.get(r, 0) + 1
print('row-16 passes', len(recs), '| CV1 != F38(IV, M0):', cvbad, '| variant not selected:', vbad, '| W7 not in F7:', w7bad, '| failures of rows -4..16:', cellbad, '| deepest row reached:', deepest)
```

```text
== e2e_19_22.txt
row-16 passes 468 | CV1 != F38(IV, M0): 0 | variant not selected: 0 | W7 not in F7: 0 | failures of rows -4..16: 0 | deepest row reached: {16: 468}
== e2e_23_23.txt
row-16 passes 1062 | CV1 != F38(IV, M0): 0 | variant not selected: 0 | W7 not in F7: 0 | failures of rows -4..16: 0 | deepest row reached: {16: 1062}
== e2e_17_24.txt
row-16 passes 2031 | CV1 != F38(IV, M0): 0 | variant not selected: 0 | W7 not in F7: 0 | failures of rows -4..16: 0 | deepest row reached: {16: 2031}
```

### A.4 `r16enum.py`: the row-16 set by exhaustive enumeration

```python
# r16enum.py - exhaustive derivation of the row-16 set: every E16x with the ten fixed cell bits (2^22 values), tested with row16_full
# (every cell of row 16 of both members and every two-bit condition closing at row 16).  Run next to a0lean38.py.
import sys, time
sys.path.insert(0, '.')
import a0lean38 as T
free = ~T.EM & T.M; s = 0; good = []; t0 = time.time(); n = 0
while True:
    e = T.EV | s; n += 1
    if T.row16_full(e): good.append(e)
    s = (s - free) & free
    if s == 0: break
print('candidates', n, 'passing', len(good))
print(' '.join('%08x' % x for x in sorted(good)))
print('equals the affine set R16B + subset sums of 0x1, 0x4, 0x400, 0x2000, 0x80000:', sorted(good) == T.R16W)
print('time %.0f s' % (time.time() - t0))
```

```text
candidates 4194304 passing 32
481b02f9 481b02fa 481b02fd 481b02fe 481b06f9 481b06fa 481b06fd 481b06fe 481b22f9 481b22fa 481b22fd 481b22fe 481b26f9 481b26fa 481b26fd 481b26fe 482302f9 482302fa 482302fd 482302fe 482306f9 482306fa 482306fd 482306fe 482322f9 482322fa 482322fd 482322fe 482326f9 482326fa 482326fd 482326fe
equals the affine set R16B + subset sums of 0x1, 0x4, 0x400, 0x2000, 0x80000: True
time 141 s
```

### A.5 The q3 replica for the accepted event: development run, preregistrations, calibrations

*Development run of the W23 classes* (`diag_w23.py`, five processes of 24 replicates, labels `diag-w23|k`, k = 0..119; the front of Section 7.3 with the four patterns and the tie, then 8192 tail proposals per particle with W23 uniform, W7 in F7). For every exact event it records which of the ten printed conditions of W23 hold (bit t of the class: the six value bits of the cell in increasing bit order 12, 15, 17, 23, 24, 26, then the two-bit conditions W23[0] != W23[30], W23[1] != W23[31], W23[14] = W23[21], W23[16] = W23[25]); 3ff is the printed class.

```python
# Development diagnostic (not part of any declared value): exact events with W23 drawn uniformly (only W7 in F7 required);
# records which of the 10 printed W23 conditions (6 value bits of the cell, 4 two-bit conditions) each exact event satisfies.
import sys, json
import a0lean38 as T
from a0lean38 import *
_tx = T._tx; _ty = T._ty
def front(rng):
    P = []
    for _ in range(NP_R):
        e16 = R16W[rng.below(32)]
        Ax = {i: _tx[0][i] for i in range(-4, 16)}; Ex = {i: _tx[1][i] for i in range(-4, 16)}; Wx = {i: PMX[i] for i in range(16)}
        Ay = {i: _ty[0][i] for i in range(-4, 16)}; Ey = {i: _ty[1][i] for i in range(-4, 16)}; Wy = {i: PMY[i] for i in range(16)}
        Wx[16] = (e16 - (Ax[12] + Ex[12] + S1(Ex[15]) + CH(Ex[15], Ex[14], Ex[13]) + K[16])) & M
        Wy[16] = (Wx[16] + ((s1(PMY[14]) + PMY[9] - s1(PMX[14]) - PMX[9]) & M)) & M
        for (A, E, W) in ((Ax, Ex, Wx), (Ay, Ey, Wy)): step_row(A, E, W, 16)
        P.append((Ax, Ex, Wx, Ay, Ey, Wy))
    for i in range(17, 22):
        cm, cvv = CELLS[1][i][:2]; pq = PQ[i]; imp = cm | pq; Mi = CH_R[i - 17]; surv = []
        for (Ax, Ex, Wx, Ay, Ey, Wy) in P:
            rx = (Ax[i-4] + Ex[i-4] + S1(Ex[i-1]) + CH(Ex[i-1], Ex[i-2], Ex[i-3]) + K[i]) & M
            fixed = cvv | (Ex[i-1] & pq & ~cm & M)
            if i == 20: fixed = (fixed & ~B29) | (Ex[19] & B29)
            for _ in range(Mi):
                e = (rng.u32() & ~imp & M) | (fixed if i != 19 else (fixed & ~M19) | P19[rng.below(4)])
                Wxi = (e - rx) & M; Wyi = (Wxi + DWT[i]) & M
                nA = {**Ax}; nE = {**Ex}; nW = {**Wx}; mA = {**Ay}; mE = {**Ey}; mW = {**Wy}
                nW[i] = Wxi; mW[i] = Wyi; step_row(nA, nE, nW, i); step_row(mA, mE, mW, i)
                if nE[i] == e and rowok((nA, nE, nW), (mA, mE, mW), i): surv.append((nA, nE, nW, mA, mE, mW))
        if not surv: return None
        P = [surv[rng.below(len(surv))] for _ in range(NP_R)]
    return P
cm, cvv = CELLS[2][23][:2]
X23 = [(b1, b2, eq) for (k1, i1, b1, eq, k2, i2, b2, row) in X2 if row == 23]
def sig(w):
    s = [((w >> b) & 1) == ((cvv >> b) & 1) for b in range(32) if (cm >> b) & 1]
    s += [(((w >> b1) ^ (w >> b2)) & 1) == (0 if eq else 1) for (b1, b2, eq) in X23]
    return ''.join('1' if x else '0' for x in s)
def work(k0, k1, out):
    ev = []; props = 0
    for k in range(k0, k1):
        rng = Shake('diag-w23|%d' % k); P = front(rng)
        if not P: continue
        for (Ax, Ex, Wx, Ay, Ey, Wy) in P:
            for _ in range(8192):
                a0 = VARIANTS[rng.below(len(VARIANTS))]; w8 = (W8C - (a0 + C4)) & M; w23 = rng.u32()
                w7 = (w23 - s1(Wx[21]) - Wx[16] - s0(w8)) & M
                if not inF7(w7): continue
                props += 1; w6 = rng.u32()
                nA = {**Ax}; nE = {**Ex}; nW = {**Wx}; mA = {**Ay}; mE = {**Ey}; mW = {**Wy}
                for i, v in ((7, w7), (8, w8)): nW[i] = v; mW[i] = (v + DWT[i]) & M
                nW[6] = w6; mW[6] = w6
                for i in range(22, NR):
                    nW[i] = (s1(nW[i-2]) + nW[i-7] + s0(nW[i-15]) + nW[i-16]) & M
                    mW[i] = (s1(mW[i-2]) + mW[i-7] + s0(mW[i-15]) + mW[i-16]) & M
                    step_row(nA, nE, nW, i); step_row(mA, mE, mW, i)
                if exact((nA, nE), (mA, mE)): ev.append((k, sig(nW[23]), hex(nW[23] ^ mW[23]), hex(nW[25] ^ mW[25])))
    json.dump(dict(props=props, ev=ev), open(out, 'w'))
if __name__ == '__main__':
    work(int(sys.argv[1]), int(sys.argv[2]), sys.argv[3])
```

```text
F7 tail proposals 4206855, exact events 164, in the printed class 3ff: 63, classes seen 27
class:count  3ff:63 177:14 357:9 377:7 367:7 167:7 1f7:5 3c7:5 347:5 3e5:4 3ed:4 1d7:4 3d7:4 1c7:3 157:3 3e7:3 3f7:3 147:2 355:2 345:2 3c5:2 1e7:1 3d5:1 3f5:1 365:1 375:1 165:1
XOR difference of W23 in the exact events: 0x2808000 82, 0x1808000 63, 0x2818000 14, 0x3818000 4, 0x6818000 1
```

The 101 exact events outside the printed class are real: every one of them carries the published modular difference of W23 with another carry pattern (XOR differences 2808000, 2818000, 3818000, 6818000 against the printed 1808000), and the replica rebuilds and verifies every success it counts (Section 7.3).

*Calibration program* (v3; v1 and v2 differ only in the labels and output file names):

```python
# calibrate_q3.py - 960 replicates of the q3 estimator for the accepted event (48 requests of 20), labels fixed by PREREG_Q3c.md.  Run next to a0lean38.py.
import sys, time, math, json, statistics
import a0lean38 as T
t = time.time(); zs = []; bad = 0; alt = 0; succ = 0
for k in range(960):
    z, pairs, b, s, lg, a = T.smc_replicate(T.Shake('a0-q3-r38|calib38v3-%d' % k)); bad += b; zs.append(z); alt += a; succ += s
lin = [0.0 if z is None else 2.0 ** z for z in zs]
print('replicates', len(zs), '| without success', sum(z is None for z in zs), '| failed checks', bad, '| successes', succ, '| other E19 pattern', alt)
print('mean of the linear estimates: 2^%.4f' % math.log2(sum(lin) / len(lin)))
for nm, sl in (('half 1', lin[:480]), ('half 2', lin[480:])): print('%s: 2^%.4f' % (nm, math.log2(sum(sl) / len(sl))))
pooled = sorted(math.log2(sum(lin[20 * g:20 * g + 20]) / 20) for g in range(48))
print('pooled means of 20: min %.4f median %.4f max %.4f mean %.4f sd %.4f' % (pooled[0], pooled[24], pooled[-1], statistics.mean(pooled), statistics.pstdev(pooled)))
print('pass rule threshold %.4f: pooled means below it: %d' % (T.Q3_THRESH, sum(p < T.Q3_THRESH for p in pooled)))
print('time %.0f s' % (time.time() - t))
json.dump(dict(zs=zs, pooled=pooled), open('calibrate_q3c.json', 'w'))
```

*v1: preregistration* (SHA-256 lines and the time they were written):

```text
# Preregistration: calibration of the q3 replica for the accepted event (written before any calibration replicate)

Program: experiments/a0lean38.py of this package (smc_replicate with four E19 patterns, the E20[29] = E19[29] tie and the exact event).
Before this file only the one selftest replicate (label 'selftest-q3') was run with the new estimator.
Pass rule of the organizer experiment a0-q3-r38, fixed here: pooled mean of the 20 linear estimates >= 2^-98.4338
(the filed rule 2^-101.7 shifted by the declared joint multiplier 2^3.2662, so its distance to q3_model 2^-97.7838 is the filed 0.65 bit), and 0 failed checks.
Calibration: 960 replicates with labels 'a0-q3-r38|calib38n%d' (k = 0..959, never used before), all kept, replicates without a success count as 0.
Reported: mean of the linear estimates (log2), the 48 pooled means of 20 (min, median, max, mean, sd), the number below the threshold,
failed checks, successes with an E19 pattern other than the published one; halves k < 480 and k >= 480 separately.
Use: the calibration reports the pass probability of the frozen rule; it does not move the threshold or q3_model.
```

```text
a2ac275a16f8b0d9c03588ca32f569897be9f723dde074eed20a555cf71b5541 *PREREG_Q3.md
550675c62076a84705ac065924d6dcaf9adc79a01171fefc0c410c25e42ccbfc *calibrate_q3.py
fe61174d09f9b9b9f7be63681673fd22b587269ef2e0a01c40300c71bacaf31c *a0lean38.py
2026-10-12 04:49:21
```

(In this preregistration "the filed rule" means the rule of the earlier version of this package, 2^-101.7; that version was not submitted.)

*v1: output*

```text
replicates 960 | without success 3 | failed checks 0 | successes 6776 | other E19 pattern 5065
mean of the linear estimates: 2^-98.8675
half 1: 2^-98.8468
half 2: 2^-98.8885
pooled means of 20: min -99.3667 median -98.8739 max -98.5506 mean -98.8763 sd 0.1606
pass rule threshold -98.4338: pooled means below it: 48
time 93 s
```

*v2: preregistration* (SHA-256 lines and the time they were written):

```text
# Preregistration v2: calibration of the q3 replica for the accepted event (written before any v2 calibration replicate)

v1 (PREREG_Q3.md, run 04:49) imposed the printed W23 cell and its four two-bit conditions in the tail. Its 960 replicates gave
2^-98.8675 and every pooled mean failed the rule. A development diagnostic (diag_w23.py: 120 replicates x 64 particles x 8192 tail
proposals with W23 uniform; 164 exact events, 63 of them in the printed W23 class, 27 classes seen) showed that the exact event does not
need the printed W23 class. v2 draws W23 by importance sampling over the classes seen (probability n/164, weight 164 2^-10 / n; classes
never seen are not proposed, so the replica estimates a lower bound) with 192 tail proposals per particle. 40 development replicates
(labels 'dev-try|k') gave 2^-97.956; they are not used below.

Program: experiments/a0lean38.py of this package as hashed in PREREG_Q3b.sha256.
Pass rule of a0-q3-r38 (unchanged from v1): pooled mean of 20 linear estimates >= 2^-98.4338, and 0 failed checks.
Calibration: 960 replicates, labels 'a0-q3-r38|calib38v2-%d' (k = 0..959, never used before), all kept, replicates without a
success count as 0. Reported: mean of the linear estimates (log2), halves k < 480 and k >= 480, the 48 pooled means of 20 (min,
median, max, mean, sd), the number below the threshold, failed checks, successes, successes with an E19 pattern other than the
published one. The calibration reports the pass probability of the frozen rule and the replica's level against q3_model 2^-97.7838;
it does not move the threshold or q3_model. If the replica's mean is below q3_model this is reported as found.
```

```text
7b6e48ecc75d232bbb7d6ff8f33ebf334219fc2e43b2d1d4cb83dbb14e0640b5 *PREREG_Q3b.md
cad1398ece67f8676e13ed12c42369e11cd79b13a182e9311c2f1ffad2663b3b *calibrate_q3b.py
edf502f79db355050e9dee1e3ad64c941eee307f1a429dc37fe6863d8b10d674 *a0lean38.py
2026-10-12 04:58:32
```

*v2: output*

```text
replicates 960 | without success 7 | failed checks 0 | successes 5842 | other E19 pattern 4419
mean of the linear estimates: 2^-97.6273
half 1: 2^-97.6374
half 2: 2^-97.6173
pooled means of 20: min -98.4245 median -97.6774 max -96.8874 mean -97.6777 sd 0.3815
pass rule threshold -98.4338: pooled means below it: 0
time 196 s
```

*v3 (shipped program): preregistration* (SHA-256 lines and the time they were written):

```text
# Preregistration v3: calibration of the q3 replica for the accepted event (written before any v3 calibration replicate)

v2 (PREREG_Q3b.md) gave mean 2^-97.6273 over 960 replicates and 0 of 48 pooled means below the rule, but a pooled sd of 0.38 bit (the
importance weights of the W23 classes seen once reach 164). v3 changes only the proposal: class probability (n + 2)/218 (weight
218 2^-10 / (n + 2)) and 384 tail proposals per particle. 100 development replicates of v3 (labels 'dev3|k') gave relative sd 0.73 per
replicate (v2 1.17); they are not used below.
Program: experiments/a0lean38.py as hashed in PREREG_Q3c.sha256. Pass rule of a0-q3-r38 unchanged: pooled mean of 20 >= 2^-98.4338,
0 failed checks. Calibration: 960 replicates, labels 'a0-q3-r38|calib38v3-%d' (k = 0..959, never used before), all kept. Reported as in
v1/v2. The v2 and v3 results are both reported in the package; the declared q3_model does not depend on either.
```

```text
eb5040a855c7c2762e55f7e957101b88849687323c19a27ba0b5838ef13d3d0a *PREREG_Q3c.md
16ad0685e08992d2c9fc1cb6b73c0daff0639e7447494a72749e6102a0054c1d *calibrate_q3c.py
3b53ce763f483236bd644151b542908ced37d5825efc7be1d24bf634663f7ca9 *a0lean38.py
2026-10-12 05:03:49
```

*v3 (shipped program): output*

```text
replicates 960 | without success 0 | failed checks 0 | successes 9090 | other E19 pattern 6813
mean of the linear estimates: 2^-97.5860
half 1: 2^-97.5903
half 2: 2^-97.5816
pooled means of 20: min -98.0335 median -97.5731 max -97.2483 mean -97.5997 sd 0.2007
pass rule threshold -98.4338: pooled means below it: 0
time 378 s
```

In v1 and v2 the program file differed from the shipped one only in the tail of `smc_replicate` (v1: the printed W23 class imposed, 96 proposals; v2: classes with probability n/164, 192 proposals). The earlier package (printed event) calibrated its replica on 960 replicates at 2^-101.0253 (pooled means of 20: mean -101.0356, sd 0.1719, min -101.4077).

### A.6 `w7check.py`: the W7 decision tree against the definition of F7

```python
# w7check.py - the decision tree of w7test against the definition of F7 on 1,100,000 words (run next to a0lean38.py)
import random
import a0lean38 as T
rr = random.Random(2026); bad = 0; mem = 0
def force(w, i, j, v):
    return w if ((w >> i) ^ (w >> j)) & 1 == v else w ^ (1 << j)
for n in range(1100000):
    w = rr.getrandbits(32)
    if n % 3:
        w = force(force(force(w, 14, 18, 1), 8, 25, 1), 1, 12, 0)
        if n % 3 == 2:
            w |= 1 << 29; w = force(force(force(w, 15, 19, 1), 9, 26, 1), 2, 13, 0)
            if rr.random() < 0.5: w &= ~(1 << 30)
            else:
                w |= 1 << 30
                for (i, j, k, v) in ((16, 20, 31, 1), (10, 27, 31, 1), (3, 14, 31, 0)):
                    if (((w >> i) ^ (w >> j) ^ (w >> k)) & 1) != v: w ^= 1 << i
    got = T.w7test(T.Mach(), w, 0); want = T.inF7(w); bad += got != want; mem += want
print('words 1100000, members of F7', mem, ', disagreements', bad)
```

```text
words 1100000, members of F7 587344 , disagreements 0
```

### A.7 The shipped program: size, hash, `selftest`, `calibrate`, `sens.py`

`experiments/a0lean38.py`: 65459 bytes, SHA-256 c72b756b489ab89687ffca1b28c02b58b621096d47b6770267c02bc13e45b6ee (the only experiment source; the limit is 65,536 bytes). The class table is stored compressed (zlib, base64); `selftest` regenerates and checks all 90 classes. The code of `smc_replicate` and of the two organizer experiments is unchanged from the version that was calibrated in Appendix A.5 (its outputs, the 21 pairs and the pooled mean, are identical); `process_fb` and `process_class` (the cap tests: `vmax`, `st.halt`), `Stats`, the overshoot row of `ledger` and one `selftest` item are new in this version, and the class table, the plane-program builder keys, the operand order, the W7 loop, `calibrate`, `ledger` and `memory` changed.

```text
ok  published pair: equal 38-step outputs (hash 5d9ca5f4 ...), every printed cell and condition of rows -4..37
ok  published A0 is in G, c7 = 8f6c89c5, Step 2 returns the published words
ok  90 classes of 3840 members in 7 plane programs, distinct c7 values, masks ['0x91eb5491', '0x91eb54d1', '0x91eb55d1']
ok  row-16 set: 32 words pass the full row-16 test; 3000 random words with the ten cell bits and 1280 two-bit neighbours of the members agree with the affine description
ok  the 12 prefilter bits are shared by all 32 words
ok  W7 decision tree agrees with the definition of F7 on 8000 words
ok  step 3b on the published pair: all rows pass, exact event, traces equal the reference (2865 operations)
ok  counted rows 19 and 20 equal the definition: row 19 accepts exactly the patterns ['0x40832', '0x10000010', '0x20000c12', '0x30040430'] of 512, row 20 exactly when E20[29] = E19[29]
ok  bit-sliced prefilter equals the scalar definition on 768 lanes of each of the 7 plane programs ([1410, 1413, 1421, 1426, 1425, 1426, 1425] instructions)
ok  online program: first block 3, one class of 3840 good pairs, 0 lane mismatches
ok  q3 replicate: estimate 2^-96.92, 11 verified 38-step semi-free-start collisions accepted by step3b, 0 failed checks, 4 with another E19 pattern
ok  cap test on every block: V > V_MAX halts at the next block start, before its 90 W7 tests
ok  512 embedded variants are in G and in the selected classes
```

```text
{
 "fb_scalars": 38,
 "planes": 882,
 "step3b": 2829,
 "fixed": 35,
 "prog": {
  "0": "1410",
  "1": "1413",
  "2": "1421",
  "3": "1426",
  "4": "1425",
  "5": "1426",
  "6": "1425"
 },
 "classes_of": {
  "0": "16",
  "1": "16",
  "2": "16",
  "3": "14",
  "4": "12",
  "5": "8",
  "6": "8"
 },
 "w7": {
  "(8, False)": "1/2",
  "(13, False)": "1/4",
  "(21, True)": "1/16",
  "(18, False)": "1/8",
  "(28, False)": "7/128",
  "(31, True)": "1/256",
  "(45, False)": "7/2048",
  "(45, True)": "1/2048"
 },
 "lane_max": {
  "2448118929": "296",
  "2448118993": "308",
  "2448119249": "320"
 }
}
```

`sens.py` (the sensitivity rows of Section 11):

```python
# sens.py - sensitivity of the exact ledger of a0lean38.py (each row: ledger() with the inputs named; N_FB recomputed).
import a0lean38 as L
cal = L.calibrate()
def t(**kw):
    c = dict(cal); c.update(kw.pop('cal', {}))
    rows, info = L.ledger(cal=c, show=False, **kw); N = sum(int(v) for _, v in rows); a, cl = L.certificate(N, 2728)
    import math; return math.log2(N) - math.log2(2728)
R = [('claimed configuration (q3_model 2^-97.7838, H3 2^-9.5, success 0.39, cap margin 2^-16, A_C 2^78, A_S 2^74, DEV 2^70)', {}),
     ('q3_model 2^-97.6619 (the mean of the preregistered run, not its lower bound)', dict(q3_log2='-97.6619')),
     ('q3_model 2^-98.0', dict(q3_log2='-98.0')), ('q3_model 2^-98.5', dict(q3_log2='-98.5')), ('q3_model 2^-99.0', dict(q3_log2='-99.0')),
     ('four patterns and tie only (q3_model 2^-99.1523, this program)', dict(q3_log2='-99.1523')),
     ('exact event only (q3_model 2^-99.6917, this program)', dict(q3_log2='-99.6917')),
     ('neither (q3_model 2^-101.05, this program)', dict(q3_log2='-101.05')),
     ('neither, with the printed tests (q3_model 2^-101.05, step3b 3000: the earlier package)', dict(q3_log2='-101.05', cal=dict(step3b=3000))),
     ('H3 premise 2^-7.5', dict(h3_log2='-7.5')), ('A_C = 2^84', dict(A_C=2**84))]
for k, kw in R: print('%-118s %.5f' % (k, t(**kw)))
```

```text
claimed configuration (q3_model 2^-97.7838, H3 2^-9.5, success 0.39, cap margin 2^-16, A_C 2^78, A_S 2^74, DEV 2^70)   87.90374
q3_model 2^-97.6619 (the mean of the preregistered run, not its lower bound)                                           87.78198
q3_model 2^-98.0                                                                                                       88.11972
q3_model 2^-98.5                                                                                                       88.61931
q3_model 2^-99.0                                                                                                       89.11903
four patterns and tie only (q3_model 2^-99.1523, this program)                                                         89.27126
exact event only (q3_model 2^-99.6917, this program)                                                                   89.81046
neither (q3_model 2^-101.05, this program)                                                                             91.16850
neither, with the printed tests (q3_model 2^-101.05, step3b 3000: the earlier package)                                 91.16850
H3 premise 2^-7.5                                                                                                      87.90973
A_C = 2^84                                                                                                             87.99564
```

### A.8 `h3gen.py` and `h3count.c`: the other variants of a successful first block (H3)

```python
# h3gen.py - successes of the Step-3 sampler for the measurement of H3: 8 independent runs of R replicates (NP particles), a0 drawn from all 245,760 variants.
import sys, time, struct
import a0lean38 as T
run = int(sys.argv[1]); R = int(sys.argv[2]); NP = int(sys.argv[3])
allv = []
for c7, base, mask in T.CLASSES: allv.extend(T.class_members(c7, base, mask))
T.VARIANTS[:] = allv
T.NP_R = NP
out = open('h3_run%d.bin' % run, 'wb'); n = 0; t0 = time.time()
for rep in range(R):
    z, pairs, bad, succ, lg, alt = T.smc_replicate(T.Shake('h3|%d|%d' % (run, rep)))
    assert bad == 0
    for cv, mx, my in pairs:
        # recover a0: the variant is in the rebuild (words_from_cv must return mx[:14]); find it from E4: A0 = E4 - C4 via the Step-2 inversion is implicit, so store cv and mx
        out.write(struct.pack('<8I16I', *(cv + mx))); n += 1
out.close(); print('run', run, 'successes', n, 'time %.0f s' % (time.time() - t0))
```

```c
// h3count.c - the other variants of a successful first block (H3), own code.  Input: records of 24 words (CV1: 8, M1 of member x: 16) written
// by h3gen.py.  For each success (CV1, a0) every selected variant b0 != a0 of the same CV1 is tried: its class passes F7 iff c7 - A_{-1} is in F7;
// for a good b0 the closed form E16x, the 12-bit prefilter and the exact row-16 set.  Usage: ./h3count file1 file2 ...  (one line per file).
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
typedef uint32_t u32; typedef uint64_t u64;
static inline u32 ror(u32 x, int n){ return (x>>n)|(x<<(32-n)); }
static inline u32 S0(u32 x){ return ror(x,2)^ror(x,13)^ror(x,22); }
static inline u32 S1(u32 x){ return ror(x,6)^ror(x,11)^ror(x,25); }
static inline u32 s0(u32 x){ return ror(x,7)^ror(x,18)^(x>>3); }
static inline u32 MAJ(u32 x,u32 y,u32 z){ return (x&y)^(x&z)^(y&z); }
static inline u32 CH(u32 x,u32 y,u32 z){ return (x&y)^(~x&z); }
#include "consts_m.h"
static u32 mem[64*3840], c7s[64];
static inline int inF7(u32 w){ return (s0(w+0x20000000u)-s0(w))==0x03bff800u; }
int main(int argc,char**argv){
  FILE*f=fopen("classes.txt","r"); unsigned c7,base,mask; int nc=0;
  while(fscanf(f,"%x %x %x",&c7,&base,&mask)==3){ u32 s=0; int n=0; do{ u32 a=base^s; u32 w=W8C-(a+C4), y=w+D8;
      if((w&CM)==CV && (w^y)==CD){ int b0=w&1,b28=(w>>28)&1,b30=(w>>30)&1,b9=(w>>9)&1,b1=(w>>1)&1,b18=(w>>18)&1;
        if(b0!=b28&&b30!=b9&&b1==b18){ u32 e4=a+C4; u32 c=SE7-2*SA3+S0(SA2)+MAJ(SA2,SA1,a)-S1(SE6)-CH(SE6,SE5,e4)-0xab1c5ed5u; if(c==c7) mem[nc*3840+n++]=a; } }
      s=(s-mask)&mask; }while(s); if(n!=3840) return 1; c7s[nc++]=c7; }
  fclose(f);
  for(int ai=1; ai<argc; ai++){
    FILE*g=fopen(argv[ai],"rb"); u32 rec[24]; u64 succ=0, good=0, pre=0, r16=0, selfbad=0;
    while(fread(rec,4,24,g)==24){
      u32 cv[8]; for(int i=0;i<8;i++) cv[i]=rec[i]; u32 *mx=rec+8; u32 a0s=W8C-mx[8]-C4;
      u32 a=cv[0],b=cv[1],c=cv[2],d=cv[3],e=cv[4],ff=cv[5],gg=cv[6],hh_=cv[7];
      u32 PP=a&b, QQ=a|b, HH=d-S0(a)-MAJ(a,b,c), EF=e^ff, FF=ff, K1=SA1-gg-0x71374491u;
      u32 kap0=HH-d-hh_-S1(e)-CH(e,ff,gg)-0x428a2f98u, KP=C16+kap0; int self_seen=0;
      succ++;
      for(int ci=0; ci<64; ci++){ u32 w=c7s[ci]-a; if(!inF7(w)) continue;
        for(int t=0;t<3840;t++){ u32 a0=mem[ci*3840+t]; u32 E0=a0+HH; u32 T=S0(a0)+(PP|(a0&QQ))+S1(E0)+(FF^(E0&EF)); u32 W1=K1-T; u32 E16=KP+a0+s0(W1);
          int pp=(((E16^TVAL)&PMASK)==0), rr=pp && (((E16-R16B)&~R16F)==0);
          if(a0==a0s){ self_seen=1; if(!rr) selfbad++; continue; }
          good++; pre+=pp; r16+=rr; } }
      if(!self_seen) selfbad++;
    }
    fclose(g);
    printf("%s successes %llu other_good %llu other_prefilter %llu other_row16 %llu self_failures %llu\n",argv[ai],(unsigned long long)succ,(unsigned long long)good,(unsigned long long)pre,(unsigned long long)r16,(unsigned long long)selfbad);
  }
  return 0; }
```

Output of `h3count` on the eight runs (one line per run):

```text
h3_run1.bin successes 4088 other_good 301147912 other_prefilter 73681 other_row16 5 self_failures 0
h3_run2.bin successes 4204 other_good 307042196 other_prefilter 74943 other_row16 3 self_failures 0
h3_run3.bin successes 4225 other_good 308102015 other_prefilter 74839 other_row16 1 self_failures 0
h3_run4.bin successes 4183 other_good 307337897 other_prefilter 75205 other_row16 0 self_failures 0
h3_run5.bin successes 4212 other_good 308539788 other_prefilter 75484 other_row16 3 self_failures 0
h3_run6.bin successes 4051 other_good 297530669 other_prefilter 72492 other_row16 2 self_failures 0
h3_run7.bin successes 4088 other_good 301151752 other_prefilter 74062 other_row16 2 self_failures 0
h3_run8.bin successes 4171 other_good 304669109 other_prefilter 74686 other_row16 5 self_failures 0
```

## Appendix B. The exact ledger (integers and fractions only)

The program recomputes the exact total from the counted inputs of Sections 9 and 11 and prints N, its integer certificate and time_log2 (`python3 experiments/a0lean38.py ledger` computes the same inputs from the machine; N_FB is the integer of Section 10).

```python
from fractions import Fraction
C = 2728
N_FB = 5840904760525073226269327
FIXED = 35                       # operations on every first block (Section 9.1)
VBAR = Fraction(71028121742895, 536870912)       # mean data-dependent operations per first block (Section 11)
EPS = Fraction(1, 2 ** 16)
V_MAX = -((-N_FB * VBAR * (1 + EPS)) // 1)
OVER = 12119157                     # Lemma 8.1: 5,510 (work before a block's first class cap test) + 12,113,647 (one class at its maximum)
PRE = 4515430400
rows = [("allowance A_C (characteristic search)", 2 ** 78 * C), ("allowance A_S (Step-1 solve)", 2 ** 74 * C), ("allowance DEV (development)", 2 ** 70 * C),
        ("first-block compressions, N_FB x C", N_FB * C), ("fixed operations per first block, N_FB x 35", N_FB * FIXED),
        ("data-dependent operations, cap V_MAX", V_MAX), ("overshoot past V_MAX: the work before the first class cap test of a block plus one class at its maximum", OVER),
        ("precomputation (member tests, batch planes, program generation)", PRE), ("final verification (6 compressions and 1600 operations)", 6 * C + 1600)]
def certificate(N, C, P=100000, digits=5):
    NP, CP = N ** P, C ** P
    a = (NP // CP).bit_length() - 1
    while (1 << (a + 1)) * CP <= NP: a += 1
    while (1 << a) * CP > NP: a -= 1
    sc = 10 ** digits
    return a, Fraction(-(-(a + 1) * sc // P), sc)
N = sum(int(v) for _, v in rows)
for k, v in rows: print("%s  %48s" % (k.ljust(70), format(int(v), ",")))
a, claim = certificate(N, C)
print("N = %d" % N)
print("certificate: 2^%d * %d^100000 <= N^100000 < 2^%d * %d^100000" %  (a, C, a + 1, C))
print("time_log2 = %.5f" % float(claim))
```

Output:

```text
allowance A_C (characteristic search)                                                824,487,408,977,177,097,149,612,032
allowance A_S (Step-1 solve)                                                          51,530,463,061,073,568,571,850,752
allowance DEV (development)                                                               3,220,653,941,317,098,035,740,672
first-block compressions, N_FB x C                                                15,933,988,186,712,399,761,262,724,056
fixed operations per first block, N_FB x 35                                          204,431,666,618,377,562,919,426,445
data-dependent operations, cap V_MAX                                             772,764,579,970,529,091,929,220,381,051
overshoot past V_MAX: the work before the first class cap test of a block plus one class at its maximum   12,119,157
precomputation (member tests, batch planes, program generation)                                            4,515,430,400
final verification (6 compressions and 1600 operations)                                                           17,968
N = 789782238349839437021687302533
certificate: 2^8790374 * 2728^100000 <= N^100000 < 2^8790375 * 2728^100000
time_log2 = 87.90375
```


## Appendix C. The characteristic search: what we measured (H4a)

**Part A. Published and measured cost of the same kind of search (the basis of A_C = 2^78).** Units are target compressions (one 38-step compression = 1 unit = 2728 word operations); a full 64-step SHA-256 evaluation is charged 64/38 units = 4,594.5 word operations, more than a target compression.

*Conversion.* Hash rate measured here: portable C SHA-256 compression (no SHA-NI, gcc -O2, one thread, AMD Ryzen 9 7900X, WSL2; checked on "abc", first words ba7816bf 8f01cfea), five runs of 2 x 10^7 compressions: 4,030,079, 4,022,282, 3,891,284, 4,013,036 and 3,797,484 per second; the slowest, 3,797,484 per second (2^21.86), is used for every conversion (a slower rate gives more evaluations, hence a larger cost). Solver CPU-seconds = wall seconds x threads (an upper bound: idle threads are counted). Figures in the table are log2.

| source | problem | stated cost | SHA-256 evaluations | units | word operations | bits under 2^78 units |
|---|---|---|---:|---:|---:|---:|
| Mendel, Nad, Schlaeffer 2013, Sect. 6.3 p.14 | 38-step SFS: characteristic and pair together | about 8 h on a single CPU, "about 2^37 SHA-256 evaluations" (hardware not named) | 37.00 | 37.75 | 49.17 | 40.25 |
| Mendel et al. 2013, Sect. 6.2 p.12 | 31-step SFS: characteristic and pair together | about 21 h, "about 2^38.4 SHA-256 evaluations" | 38.40 | 39.15 | 50.57 | 38.85 |
| Li, Liu, Wang 2024 (ePrint 2024/349), p.16 | 39-step SFS colliding pair given the characteristic | 120 s with 26 threads = 3,120 thread-seconds (hardware not named) | 33.46 | 34.22 | 45.63 | 43.78 |
| ours, 39-step characteristic | derived from scratch with the tool of [LLW24a] | 772.58 s wall x 12 threads (CryptoMiniSat) + 1,800.77 s x 1 (Kissat, no result) = 11,071.7 CPU-s | 35.29 | 36.04 | 47.46 | 41.96 |
| ours, 38-step pair (part B) | pair given the published cells, 4 calls, 3 without a model | 2,852.83 CPU-s | 33.33 | 34.09 | 45.50 | 43.91 |

Our 39-step characteristic derivation: the unmodified model scripts of github.com/Peace9911/sha_2_attack at commit 6a9f35fd (the account that hosts the authors' RIPEMD-160 tool of [LLW23]) were read before running (no network, no installs, writes only in the working directory); the STP query they emit was translated to CNF by our own converter (which rejects six mutated characteristics and accepts the published 39-step characteristic and rows 5..24 of the published 37-step one) and solved with CryptoMiniSat 5.11.21 on 12 threads: model found after 772.58 s wall (about 2.6 CPU-hours); Kissat 4.0.3 on the same file stopped at 1,800.77 s without a result. It is a window search (rows 8..26 with the message support fixed and the weights W 25, A 10, E at most 90 asserted) that finds a characteristic of the published weights, not the characteristic of Table 3 of [LZLLQZ26]; one run, one machine.

*Reading.* Every figure is far below 2^78 target compressions: the largest, 2^39.15 units (Mendel et al.'s 31-step figure), is 38.85 bits under it, and the 38-step figure of the same authors, 2^37.75 units, is 40.25 bits under; counted in word operations without the factor C, the largest is 2^50.57, 27.43 bits under 2^78. The 38-step characteristic of [LZLLQZ26] (two-block framework, dense rows 0..16) is a harder instance than those searches and no log of its search exists; the margin of 38.85 bits (a factor of about 2^39) is what A_C = 2^78 leaves for that difference and for failed and repeated searches.

**Part B. Our pair searches and sparse part.**

Participant-run here; programs written and run by Grok (xAI); not shipped (64 KiB source limit; the figures are not used in the ledger, which charges the allowance). SAT: one word operation = one propagation; otherwise one tick = one 32-bit add/sub, S0, S1, s0, s1, CH, MAJ or hash-set probe. Units = word operations / C. Totals include the calls without a model.

**38-step pair search, given the published cells.** Circuit: both 38-step chains with a shared chaining value, message masks on W7..W11, W15 (W16, W23, W25 expanded), every cell of Table 3, the 13 vertical links and the 47 two-bit conditions (W25[4] = W25[6], which holds on the published pair; Table 4 prints W25[9]); 110,437 variables, 383,913 clauses, satisfied by the published pair; one clause blocks the published (CV, M'). File a pins the 24 bits common to the 32 E16 words of the published list; file b selects one of the 32 words.

| call (time limit 900 s) | file | result | CPU s | propagations |
|---|---|---|---:|---:|
| Kissat 4.0.3 --sat --seed=2 --walkinitially=true | a | no model | 898.63 | 592,022,133 |
| CaDiCaL 2.1.3 --seed=1 | a | no model | 898.61 | 1,813,811,854 |
| Kissat 4.0.3 --sat --seed=4 --walkinitially=true | b | pair | 476.96 | 433,129,432 |
| CaDiCaL 2.1.3 --seed=4 | b | no model | 578.63 | 1,217,006,281 |
| total | | | 2,852.83 | 4,055,969,700 = 2^31.917 (2^20.504 units) |

The pair (38-step SHA-256 compression with feed-forward; recomputed by us with an independent step function checked against hashlib on "abc"; M' carries the published E16 word 482326fd, with a different CV and message):

```
CV     43058709 adfdbff7 b7e63568 b4e09527 3ef1b89a 18f03df1 7fd9bbaa 7f392ba4
M      33f3fd01 ab09628d 9971c77a 2f0148d3 442fd7d8 9acaf5c3 2fd3a6f8 a8740b40
       c91bb8b5 9e019239 04039fa1 0ce30b8d a18c515a 76a1e994 d28e48a0 9b5f6dbb
M'     33f3fd01 ab09628d 9971c77a 2f0148d3 442fd7d8 9acaf5c3 2fd3a6f8 88740b40
       cd5bb0b5 be019239 01028d0b 0ceb1f8d a18c515a 76a1e994 d28e48a0 9f1f65bb
digest 614d0b44 0d272005 713bab9e 4fc8e2a1 126b7229 bbb45050 0d592f10 cf2f96a9
```

Words that differ: 7..11, 15, 16, 23, 25 (dW16 = e0000000, dW23 = fe7f8000, dW25 = 20000000); A and E are equal from step 22.

**37-step analogue** (C = 2644; the same circuit on the 37-step characteristic, W15 pinned on the 24 common bits of its list): Kissat seed 2 pair A (135,356,424 propagations), Kissat seed 1 no model (167,052,440), CaDiCaL seed 1 pair B (494,307,286); total 796,716,150 = 2^29.570 (2^18.201 units). Digests: A 3c7353c7 46761dc9 8b3ce5a5 3c6530d2 d6e267fb f0f5b41e b8c21e9a 03b5b458, B 6c1e60a3 27a17426 dd5333ab 9f3317d4 00453b21 27264f97 2f2ea277 4a533513.

**38-step sparse part, from the support and the Section 4.1 rules only** (no table cell seeded; the published values used only as a checker):

| part | ticks | CPU s | result |
|---|---:|---:|---|
| message-difference signing, all 32 disturbance bits | 101,842,272 | 0.533 | bit 29 gives the published XOR masks; fe7f8000 among the 8 dW23 sums |
| sparse window rows 17..37, bits 28..31, all 8 dW23, both dW25 signs | 11,239,528 | 0.021 | the published dW23, dW25 close (22 conditions, rank 22) |
| total | 113,081,800 = 2^26.753 | 0.554 | |

**Not measured (the allowance A_C = 2^78):** deriving the dense signed characteristic of rows 0..16 with its two-bit conditions (the pair searches load those cells; a 37-step attempt with them unset, by SAT, step-6 cubes and a pattern beam, returned no model; of 4,614 message pairs realising the 38-step dW23, dW25 at CV = 0, none meets the zero window), and the authors' failed and repeated searches.

## 16. Answers to the ruling 8c4cbe8d (pkgR38M6, refuted), finding by finding

Each finding of the ruling is answered here by its identifier; what is fixed is marked FIXED, what is stated plainly and left as it is is marked STATED.

- **F-CAP-CHECK-GAP (fatal).** FIXED. The cap was tested only after a class, so first blocks without a passing class ran all 90 W7 tests unchecked. Now `if V > V_MAX: halt` runs at the start of every first block (Section 8; `process_fb`, with `vmax`) and after every class (`process_class`); Lemma 8.1 proves V <= V_MAX + OVER at every moment, OVER = 12,119,157 (5,510 for a block's work before its first class test, which includes all 90 W7 tests at 45 + 4 + 2 operations, plus one class at its maximum). The test is one compare-and-branch, already among the 35 fixed operations; the ledger is recomputed (Section 11, Appendix B: N = 789,782,238,349,839,437,021,687,302,533, T = 2^87.9037417, claim 87.90375 unchanged at five decimals). The success bound accounts for the abort by a proof: the run halts only on E_cap = {S > V_MAX}, whose probability is bounded by the Chebyshev P_cap = 3.285e-31 already inside N_FB (Section 10). The reviewers' reconstruction (87.9501) added 4,410 operations to each of N_FB blocks; with the test in place that charge does not arise, because the run stops at the first block that starts above V_MAX.
- **F-MEMORY-ENVELOPE, F-COST-AND-MEMORY-VALIDATION.** STATED. The 2^28-byte preprocessing envelope is measured for the pair searches and the characteristic-derivation instance (largest peak 2^27.56) and assumed for the Step-1 solve and the development (Section 14, H6); no organizer experiment exercises the preprocessing at full size. Nothing new was measured; the claim keeps 2^28 bytes as declared in H6.
- **F-PREPROCESSING-ALLOWANCES, F-EXP-05 (H4a, H4b).** STATED. A_C = 2^78 and A_S = 2^74 are allowances, not measurements of the historical computations (Section 12, Appendix C); the authors' failed and repeated searches are unavailable. They are the base's, unchanged, and sit 38.85 bits above the largest figure we measured or found published. The organizer experiments do not exercise them.
- **F-PROBABILITY-EXTRAPOLATION, F-H2-UNMEASURED-CLASSES, F-EXP-03, CRYPTO-H2-CLASS-EXTRAPOLATION.** STATED. q3 was measured with variants of the first 64 classes. For the 26 added classes the claim rests on Lemma 7.1 (rows 16..22 are the same for every variant; W8 enters only W23 and W24, with fixed modular differences) and on the declared premise H2 that their tail averages are at least those of the 64. No new sample was drawn in this version.
- **CRYPTO-H3-CONDITIONING-GAP, F-H3-EVENT-AND-CLASS-TRANSFER.** STATED. H3 was measured on sampled successes of the printed event and the first 64 classes (33,222 successes, 2^-10.63 against the 2^-8.5 used, 1.3 bits of margin); the transfer to the accepted event (every success of it also passes row 16) and to 90 classes is the declared premise H3, not a new measurement.
- **CRYPTO-H1-EXTRAPOLATION, F-H1-EXTRAPOLATION.** STATED. H1 (independent uniform chaining values) is a declared score-critical premise, tested on 2^24 first blocks and by `a0-online-r38`, not on 2^82 first blocks; the correlation of the class tests inside a first block is measured and enters only through expectations and the exact probability that some class passes.
- **F-EXP-01.** STATED. The organizer assigns no probability or cost inference to the experiments and treats observations as untrusted. The package uses them as executions of the shipped code on organizer seeds (checks in Section 13.3), not as the evidence for H1, H2, H3 or the counts, which come from the local runs of Section 13 and the exact ledger.
- **F-EXP-02.** STATED, scope text corrected. `a0-q3-r38` returns 96-byte CV1 || M1 and CV1 || M1' witnesses: each is a verified 38-step semi-free-start collision from the chaining value CV1 (the second-block step of the attack), and it is not a full collision of the target. The organizer's schema offers only the events `full-collision` and `digest-xor-mask`, so the manifest keeps `full-collision` and its hypothesis now says that the organizer's recomputation finds 0 full collisions in this experiment, by design. The experiment tests the replica of q3 and the counted step-3b program, not the complete two-block attack. `a0-online-r38` returns 128-byte M0 || M1 candidates that are not collisions either (0 full collisions by design). No experiment finds a full collision and none is claimed.
- **F-EXP-04.** STATED. The organizer fixes the seeds and the holdout nonce; a candidate cannot supply a holdout. A split inside the experiment was not added: the source is 65,459 of 65,536 bytes and the pass rule was frozen before its calibration, whose versions are all listed in Appendix A.5 (v1 failed, a development diagnostic, v2, v3; all replicates kept). The pass rule has 0.40 bit of margin (lowest of the 48 calibration pooled means 2^-98.034 against the threshold 2^-98.4338). The claim does not take its probability from the experiment's outcome: q3_model comes from the preregistered paired run and the base's bound.
- **F-STEP3B-TRANSCRIPT-DISCREPANCY.** STATED. The selftest line prints 2865 operations for the published pair because its machine also holds the 37 operations of `fb_scalars`, executed there before step 3b; 2865 - 37 + 1 (the work-counter update) = 2829, the figure `calibrate` takes from a fresh machine and the ledger charges (the scalars are charged separately, 38 per first block with a passing class).
