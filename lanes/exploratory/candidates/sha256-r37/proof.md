# Collision attack on 37-step SHA-256: the ePrint 2026/1120 two-block attack over the 222 largest classes of A0-variants, bit-sliced, online tables under 2^20 bytes (memory at most 2^29 bytes, the declared bound over all phases including the construction of the characteristic), the exact end event of rows 22..36, 2^60.4854

Track `sha256-r37-exploratory`, target `sha256-r37-prefix-v1`, cost model `collision-frontier-v5` (C = 2644).
Claim: `time_log2 = 60.4854` target compressions on every run, success probability at least 0.39 (0.3900000020 under the stated premises),
memory 2^29 bytes (the declared bound H6 on the maximum over all phases including the construction of the characteristic: online tables, code and constants 607,744 bytes = 2^19.21, computed; the construction phases measured below it, the largest the STP CNF dump at 499,384,320 bytes = 2^28.895, each run under an address-space cap of 2^29 bytes; Section 14.1 and Appendix H.2), nonuniform advice below 2^13 bytes.

**Credited derivative of Th0rgal's 0db0eeb6-9958-43af-9700-ea9e99cee016 (61.17784)**, with the four-value-pattern acceptance of rows 18 and 19 from Jbenisek's ffbe30bb-ac92-4191-a589-3bf32661ee7d (60.38707), and with the lineage of both (Section 2): winglock's 6c77089c and 7319bba9, dd6656d4 (Th0rgal), itseasypop's 1c368173, qkniep's b947b377, GordoAR's 087a18c4,
0xshikhar's 1f12a09a and fb039a6e, companygardener's d3ec5c41, 44921815 and 8de337d5, our 8aeaed1c and def128fc, Th0rgal's f2fe1d4d and Jbenisek's c22f86a2, and 6eeefb64 for the price of a solver CPU-second.
The attack, the characteristic, the sets F6, F7, L*, the family of A0-variants and its 222 largest classes, the packed good-pair arithmetic, the rows 16..36 check, the premises H1-H3 and the ledger structure are theirs.
**What this filing changes is where the work is done: no table indexed by x = A_{-1} and no 2^32-word row-16 mask table. It also accepts the four feasible value patterns of rows 18 and 19 (credit: ffbe30bb) and, new here, the R16x relaxation of rows 16 and 17 (E16[23] = 0 and E16[24] = E17[24] dropped together; Section 7.4c), and q3 is measured for this family, jointly for both relaxations, with an estimator written for this filing (Sections 7.4b, 7.4c, Appendices F, G).** The 0db0eeb6 program reads its W7 class test, its fibres of equal W6 value and its row-16 mask
from tables of 2^52.1 bytes; this program recomputes all three from 128 KB of lists and two 128 KB chunk tables. Per first block it runs the W7 test of all 222 classes at once, bit-sliced; for each passing class the W6 test of all its variants,
bit-sliced in batches of 256 reps (a class is `base | s` for s in one of ten shared lists, so only 17 bit planes vary, and the cube bits 0, 2, 3 of s are handled by one main run and at most 7 cheap subtraction runs instead of 8 times the lanes); it gathers the good pairs in packed groups of four; and it decides row 16 by a necessary condition from two 4096-word chunk
tables and an exact straight-line test of the few survivors. Every operation is counted (Section 9); the online memory is 2^19.21 bytes, so the tables themselves cost nothing under a rule that charges memory above 2^20 bytes (the claimed memory, 2^29 bytes, is the declared bound H6 over all phases including the construction of the characteristic, Section 14.1 and Appendix H.2). The price is time:
with the same characteristic-search allowance A_C = 2^60 that 0db0eeb6 charges, this program costs 2^60.4854 against 2^61.17784, because the per-pair work is about 55.4 operations instead of 12, less the 3.87 bits that the four patterns of rows 18 and 19, R16x and the exact end event of rows 22..36 give on q3 together (2^-70.16 against 2^-74.03).
**The construction of the published characteristic and SFS pair is charged here, in time (A_C = 2^60, H4) and in memory (2^29 bytes, H6): Section 11.2, Appendices H.2, H.3 and I answer the fatal finding F-COST-001 of 96933f8e. The exact end event of rows 22..36 instead of the cells of those rows (Section 7.4d, Appendix J) is kept: the claim is 2^60.4854 (96933f8e: 2^59.98193).**

## 0. Summary

- **Algorithm (Sections 4-8).** Messages M0 || M1 and M0 || M1' (128 bytes; padding adds the same third block). A first block M0 is two fresh uniform 256-bit words; CV1 = F_37(IV, M0) costs one unit.
  (1) One bit-sliced F7 test of c7 - x over the 222 classes (x = A_{-1}) finds the passing classes (3.52 per first block on average). (2) For each passing class, in a main run and subtraction runs over the cube combinations that matter (Lemma 8.2), with sweeps of two batches of 256 reps, the planes of
  W6x = CB3 + (s & q) - H are formed (Lemma 8.1) and the F6 test gives the plane of good reps, each standing for 1 to 8 members. (3) The good pairs (831 per first block on average) are read from packed entry words in groups of four and the row-16 address
  u = W0 + s0(W1) of the group is computed. (4) Two table reads per lane give the l in L* whose E16x = u + C_l satisfies eight fixed-bit conditions; each of the (on average 0.125 per lane) survivors gets an exact straight-line test (34 operations).
  (5) A row-16 pass is checked through row 36: the cells and printed two-bit conditions of rows 16..21, then rows 22..36 of both members replayed on the raw schedule words, accepted iff the eight registers agree after row 36 (Section 7.4d). Such a pair collides; it is verified with the target and output.
- **Cost (Sections 9, 11).** N_FB = 24,650,628,322,256,370 first blocks (2^54.45247); per first block 1 unit, 615 counted fixed operations and on average 46070.09 counted data-dependent operations (18.66 units in all), capped by V_MAX.
  T = A_C + A_S + DEV + N_FB + (N_FB x 615 + V_MAX + vmax_fb + PRE + FIN) / C + 6 = N / C with N = 4,267,574,450,285,246,393,181, 2^60.4854 target compressions, claimed 60.4854. The characteristic and the SFS pair are published (ePrint 2026/1120, Tables 15-17; Section 3) and their construction is charged A_C and A_S (Section 11.2).
- **Probability (Section 7, H2).** q3 = at least 2^-70.16, the probability of the exact end event (rows 22..36 replayed, registers equal; Section 7.4d). It is the product of two 99% one-sided lower bounds: the cell-event q3_cell >= 2^-71.4629 (the lower of two preregistered blocks of 128 replicates of a sequential Monte-Carlo estimator written for this filing, run on exactly this family of 782,800 variants drawn uniformly, with the four value patterns of rows 18 and 19 and R16x accepted jointly; Section 7.4c; 96933f8e used it rounded down, 2^-71.47) and the exact/cell ratio >= 2.4786 (preregistered 2 x 128 seeds, pooled 2.4848; Section 7.4d), rounded down to two decimals; the same program with Table 15's cells reproduces the registered study of 7319bba (validation, 2^-74.03). No hedge is needed: every variant of every passing class is examined.
- **Memory (Section 14).** Online 607,744 bytes = 2^19.21, of which the lists 127,744, the two chunk tables 262,144, the lane-scan table 65,536, code (bound) 65,536; the construction of the characteristic (generator, STP CNF dump, kissat) runs under an address-space cap of 2^29 bytes with measured peaks up to 499,384,320 bytes; the Step-1 re-solve runs under 117,440,512 bytes (measured peak 88,006,656); claimed 2^29 bytes, the declared bound over all phases (H6, Appendix H.2).
- **Premises (Section 12).** H1 uniform independent chaining values; H2 q3; H3 few further successes per first block; H4 advice allowances A_C = 2^60 (a labelled allowance, not a measurement: Appendix H.3), A_S = 2^50 (bounded by the caps of the Step-1 re-solve, Section 11.2), DEV = 2^40 (Section 13.4); H5 counted word-RAM pricing of the bit-sliced program, 64 registers; H6 the memory bound 2^29 over all phases including the construction of the characteristic (Appendix H.2); H7 exact success floor. Nothing else is heuristic (Appendix H.1).
  No table statistics are used: every count in the ledger is an exact expectation or a stated bound on one.
- **Checks (Section 13).** `lowm.py selftest` (classes and lists against the definitions for all 782,800 variants; the plane programs against the scalar definitions on 87,372 lanes; the row-16 stage against the row-16 definition; the packed address on 400 lanes);
  an exhaustive comparison of the exact row-16 test with the enumeration of 2,097,152 pairs (u, l) (Appendix A); the three alternative collisions of the new patterns against the cells (Section 7.6); the q3 studies (Section 7.4b); both organizer experiments, all 256 trials; a simulation of the counted program on 50,000 first blocks against the ledger.

## 1. Target, cost model and output

- **Target** sha256-r37-prefix-v1: SHA-256 steps 0..36 on every padded block, the standard IV once, FIPS 180-4 padding, feed-forward, all eight digest words (repository `verifier/hash_functions.digest(m, "sha256", 37)`).
  The output is two distinct complete messages with equal digests, verified with the target before output.
- **Cost model** collision-frontier-v5: one 37-step target compression = 1 unit; every other executed 256-bit word-RAM primitive (load, store, add/sub, and/or/xor/not, shift/rotation, compare, branch,
  uniform random word) = 1/C unit with C = 2644. Immediates and shift amounts are instruction fields; 64 registers. Success must be at least 0.39 over fresh coins.
- **Notation.** In step i, E_i = A_{i-4} + E_{i-4} + S1(E_{i-1}) + CH(E_{i-1}, E_{i-2}, E_{i-3}) + K_i + W_i and A_i = E_i - A_{i-4} + S0(A_{i-1}) + MAJ(A_{i-1}, A_{i-2}, A_{i-3}) (mod 2^32);
  (A_{-1..-4}, E_{-1..-4}) = (a, b, c, d, e, f, g, h) of the incoming chaining value. F_R(cv, B) is the R-step compression with feed-forward; its output is cv + (A_{R-1}, A_{R-2}, A_{R-3}, A_{R-4}, E_{R-1}, E_{R-2}, E_{R-3}, E_{R-4}).

## 2. Sources and credit

- [LZLLQZ26] Y. Li, Z. Zhang, M. Li, F. Liu, H. Qian, J. Zhu, "Pushing Collision Attacks on SHA-2 to 39 Steps", IACR ePrint 2026/1120 (CC BY): the 37-step characteristic (Table 15), its two-bit conditions (Table 16), the SFS pair (Table 17) and the three-step attack.
  [LLWS26] Y. Li, F. Liu, G. Wang, J. Shi, ePrint 2026/1080 (the framework).
- ffbe30bb-ac92-4191-a589-3bf32661ee7d (Jbenisek, 60.38707, a credited derivative of fb039a6e): the four feasible value patterns of E18[1,5,10,11,18,28,29] and E19[29] and the change of the cell strings, the solver enumeration and the three verified collisions behind them (Section 7.6); this filing re-measures q3 for its own family.
- Filings on this track, declared as dependencies: 6c77089c (winglock): transcription of Tables 15-17, the exact sets F6, F7 and L*, the SMC design for q3. dd6656d4 (Th0rgal): affine decomposition of F6, F7. 1c368173 (itseasypop), b947b377 (qkniep): the A0 freedom of the Step-1 solution and the c7 classes.
  087a18c4 (GordoAR): the exact-rational ledger and the success analysis. 1f12a09a (0xshikhar): the 222 classes and the packed groups of four 64-bit lanes. 7319bba9 (winglock): the program structure, the row-16 enumeration, the preregistered q3 studies, the end-to-end rates.
  d3ec5c41, 44921815, 8de337d5 (companygardener): the counted-program framework and the ledger. 8aeaed1c, def128fc (ours) and c22f86a2 (Jbenisek): the direct row-16 lane read and the cap slack squared in the Chebyshev bound.
  f2fe1d4d, 0db0eeb6 (Th0rgal): the MAJ identity, the single packed member word `Gw` and its 31-operation group. fb039a6e (0xshikhar): the bit-sliced additions with register-resident planes and the q3 studies over the whole family (cited, not used). 6eeefb64 (sha256-r32): the calibrated price of a solver CPU-second (Sections 11.2, 13.4).
- **New here.** The exact end event of rows 22..36 in place of the cells of those rows and its preregistered ratio study (Section 7.4d, Appendix K), the R16x relaxation of rows 16 and 17 and its joint study with the four patterns (Section 7.4c, Appendix G), the q3 estimator `q3smc.c` and its preregistered studies (Section 7.4b, Appendix F), the application of the four-pattern acceptance to the table-free program (Section 7.6), the class list structure (Section 5.3), the bit-sliced W7 and W6 programs (Lemma 8.1, Section 9), the plane algebra with static constants and inversion flags, the gather of good pairs from packed entries, the two-chunk-table row-16 probe and its exact test (Section 6.2), and the memory accounting (Section 14).


## 3. The characteristic (from the paper, as transcribed in 6c77089c; re-checked by `experiments/lowm.py`)

### 3.1 Notation and orientation

Symbols are MSB first: `n` = bits (x, y) = (0, 1), `u` = (1, 0), `0`/`1` fixed and equal, `=` equal, `+` = equal on
both members and equal to the same bit of the vertically adjacent `+` (E_i[b] = E_{i+1}[b]). Member x is the
message the paper prints second (M'); with this orientation every cell holds on the published pair (checked).

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

In this table rows 18 and 19 are the paper's. This filing's program keeps the cells of every row but does not impose the value bits E18[1,5,10,11,18,28,29] and E19[29] of those two rows (the characters `1`, `0` there); the four patterns it accepts are listed in Section 7.6. It also does not impose E16[23] = 0 and the `+` pair E16[24] = E17[24] of rows 16 and 17 (R16x, Section 7.4c).

Rows -4..3 are entirely `=`: **A0..A3 and E0..E3 carry no condition** (the chaining value is common and A0..A5, E4, E5
have no difference).

### 3.3 Two-bit conditions as printed (Table 16), with the corrected reading

```text
A15[15] != A16[15], A15[23] = A16[23], A15[25] = A16[25], A16[9] != A16[20], A16[18] != A16[6]
A16[8] = A16[17], A15[29] = A17[29] (printed: A16[29] = A17[29]), A17[29] = A18[29], E15[4] = E16[4]
E17[0] != E17[13], E16[24] = E17[24], E16[15] = E17[15], E18[6] != E18[19], E18[2] = E18[20], E20[2] != E20[16]
W6[1] = W6[12], W6[8] != W6[25], W6[14] = W6[18], W7[0] = W7[28], W7[9] = W7[30], W7[1] = W7[18]
W8[1] != W8[12], W8[8] != W8[25], W8[14] = W8[18], W22[31] != W22[1], W22[30] != W22[0]
W22[16] != W22[25], W22[14] != W22[21], W24[4] != W24[6], W24[22] = W24[31], W24[20] != W24[27]
```

The algorithm checks every cell; on rows >= 16 it also checks the printed two-bit conditions (they can only lower
the success probability, and q3 is defined with them). The W6, W7 two-bit conditions are replaced by the exact
filters of Section 5.1; the W8 conditions are part of the definition of G (Section 4.3).

### 3.4 The SFS pair (Table 17)

```text
CV  63b4986c 35d83dc0 c98894e4 784e08fc 78a7f752 5ed877a8 315a2db3 d5614eb4
M   4d7f86ff 32ece589 d8accfc4 2cc2e433 068b5b34 eba68a28 2fe12cad 6aa26b0c
    9f0d78e1 681b8277 faa9c7e0 56aed439 cc2dbbc2 dd2ba0fc b95d377b 5dd43a81
M'  4d7f86ff 32ece589 d8accfc4 2cc2e433 068b5b34 eba68a28 0fe12cad 6ee2630c
    bf0d78e1 6d1a90dd faa1d3e0 56aed439 cc2dbbc2 dd2ba0fc bd1d3f7b 7dd43a81
hash a856d46e 4b46eb28 4935248c 92a2fc98 e0fb2610 10a9951f 54264f5b 80954580
```

F_37(CV, M) = F_37(CV, M') = the printed hash; every cell of rows -4..36 and every printed two-bit condition holds
with x = M', y = M (`experiments/lowm.py` rebuilds both members and checks the cells; the repository
verifier reproduces the hash).


## 4. Step 1: the solution S and its A0-variants

### 4.1 S

S is the inner part of the published pair: A0..A13, E4..E13 and W8..W13 of both members (x | y):

```text
A0  1b21ce20 | 1b21ce20   A5  a26653f8 | a26653f8   A10 030eaaa0 | 010e8aa0   E4  1b2d044e | 1b2d044e   E9  9a3c74f0 | 9a3c74e0
A1  62827866 | 62827866   A6  210c2860 | 410c2860   A11 1ae4bc99 | 12c4b68b   E5  e7f2c81f | e7f2c81f   E10 87a8fadc | a5a8dadc
A2  987f24c4 | 987f24c4   A7  7246d008 | 7267d818   A12 2fd3ea18 | 4fd3ea18   E6  eb0b9c2d | 0b0b9c2d   E11 b0741f5f | a875495a
A3  44294b96 | 44294b96   A8  7c4a1e59 | 7c4a1e59   A13 9992b350 | 919033c0   E7  9a404eb1 | b2645641   E12 6fd5b358 | 6825b602
A4  a8ccc9b3 | a8ccc9b3   A9  edc43977 | edc43977   W8  bf0d78e1 | 9f0d78e1   E8  7b3e8fa7 | 7f768aa3   E13 66f25d89 | 6eeedd89
W9  6d1a90dd | 681b8277   W10 faa1d3e0 | faa9c7e0   W11 56aed439 | 56aed439   W12 cc2dbbc2 | cc2dbbc2   W13 dd2ba0fc | dd2ba0fc
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

### 4.3 The A0-variants (itseasypop 1c368173, qkniep b947b377; re-derived here)

**Lemma 4.2 (variants).** Replace A0 of S by any a0 (both members: rows 0..5 of S carry no difference) and keep
A1..A13 of both members. Then, for every chaining value:
(a) E5..E13 and W9..W13 are unchanged (E_i for i >= 5 involves A_{i-4..i} with i-4 >= 1; W_i for i >= 9 involves
    E_{i-4..i}, A_{i-4} with i-4 >= 5);
(b) E4 = a0 + C4 with C4 = A4 - S0(A3) - MAJ(A3, A2, A1) = 000b362e, and W8x = W8C - E4 with
    W8C = E8 - A4 - S1(E7) - CH(E7, E6, E5) - K8 = da3a7d2f; E4 enters W8 of both members with the same sign
    (as E_{i-4} of step 8, without a member difference), so the modular difference W8y - W8x = e0000000 is
    unchanged;
(c) W0..W7 change (they absorb E0..E4); the member differences W_i^y - W_i^x are 0 for i <= 5, d6 = 20000000 for
    i = 6 (E5, E4, E3 carry no difference) and d7 = fbc00800 for i = 7 **provided E4[31:29] = 000**: in step 7,
    CH(E6, E5, E4) selects E5 for member x and E4 for member y on bits 31..29 (E6 = `uuu` there; E5 = `111`), so
    d7 depends on E4[31:29] and equals the published value exactly when the row-4 cells `000` hold;
(d) the cells of rows -4..15 that involve E4 or W8: E4's cells (`000`) and W8's cell (`u` at bit 29) with its three
    printed two-bit conditions. The latter fix the signed XOR difference of s0(W8) (s0 is linear; bits 22, 11, 26
    of s0(W8x) are W8x[29]^W8x[8]^W8x[25], W8x[29]^W8x[14]^W8x[18], W8x[29]^W8x[1]^W8x[12]), hence the modular
    difference s0(W8y) - s0(W8x) = 043ff800 = -d7 that makes W23 = s1(W21) + W16 + s0(W8) + W7 difference-free.

Define **G = {a0 : E4 = a0 + C4 has E4[31:29] = 000, W8x = W8C - E4 has W8x[29] = 1, W8x[1] != W8x[12],
W8x[8] != W8x[25], W8x[14] = W8x[18]}**. Exhaustive count over the 2^29 values of E4 with E4[31:29] = 000 (a0 = E4 - C4 is a bijection; counted by 0db0eeb6, and 7319bba's `genum2.c` agrees):
|G| = 12,103,680 = 2^23.529 (the count of 7319bba's `genum2.c` is reproduced). The published A0 (1b21ce20) is in G.

**Lemma 4.3 (validity).** For a0 in G, every chaining value CV1 whose words (Lemma 4.1 with A0 = a0) satisfy the
filters W7x in F7 and W6x in F6 (Section 5.1), and every l in L* (Section 6), the pair follows every cell of rows
-4..15 of A, E and W except the XOR cells of W6 and W7, and every printed two-bit condition closing at a row <= 15
except those on W6, W7; and every modular difference that enters the message expansion (W6..W15 and
s0(W6..W15), s1(W14), s1(W15)) equals that of the published pair. *Proof.* Lemma 4.2 for E4, W8 and d6, d7; the
filters for s0(W6), s0(W7) (Section 5.1); everything else is S's or l's. *Checks:* every good pair of the
organizer experiment `a0-online-r37` and of the end-to-end runs (Section 13.1) against all 32 l.

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
W7x = c7(a0) - A_{-1},           c7(a0) = ab9a1763 + MAJ(A2, A1, a0) - CH(E6, E5, a0 + C4)
W6x = C6 - A_{-2} + MAJ(A1, a0, A_{-1}) - CH(E5, a0 + C4, E3),   E3 = K3C - MAJ(A2, A1, a0) + A_{-1}
C6 = E6 - 2 A2 + S0(A1) - S1(E5) - K6 = f538a8f7,   K3C = A3 - S0(A2) = 478132ed
```

### 5.2 Lemma 5.1 (distribution, per variant)

Under H1 (CV1 uniform), for every fixed variant a0: Pr[W7x in F7] = p7 = |F7|/2^32 = 2^-5.97763 and
Pr[W6x in F6 | W7x in F7] = p6 = |F6|/2^32 = 2^-3.90197 exactly; conditioned on both, (W0..W5) is uniform on
(2^32)^6, (W6, W7) is uniform on F6 x F7, and they are independent. For every l in L*, (W16, ..., W21) is then a
bijective image of (W0..W5) for fixed (W6, W9..W15), hence iid uniform and independent of (W6, W7).
*Proof.* Lemma 4.1 (bijection for fixed a0) and the inverse expansion W5 = W21 - s1(W19) - W14 - s0(W6),
W4 = W20 - s1(W18) - W13 - s0(W5), ..., W0 = W16 - s1(W14) - W9 - s0(W1). (6c77089c's Lemma 2, for each variant.)


### 5.3 The 222 classes and their ten lists

c7(a0) takes 22,976 distinct values on G (7319bba and 0db0eeb6 enumerate them). A *class* is G intersected with one value of c7; for all variants of a class and a given CV1, W7x is the same word, so one membership test decides the W7 filter of the whole class.
**This filing examines the 222 classes with at least 3456 variants** (782,800 variants; 1f12a09a's selection, the family of 7319bba's registered q3 studies). Each class is {base XOR s : s subset of mask, a0 in G, c7(a0) = the class value} (the descriptors c7, base, mask, size are the table `CLASSES` of `lowm.py`).

**Fact (computed; `selftest` re-derives it for every class).** For all 222 classes base & mask = 0, so a0 = base + s = base | s = base ^ s with s a subset of the mask, and the set of s depends only on one of **ten lists**:

```text
list  mask      size  classes      list  mask      size  classes
 0    01fec08d  3456   82           5    01fec08d  3600   82
 1    01fec48d  3456    3           6    01fec48d  3600    3
 2    01fec09d  3456   15           7    01fec09d  3584   15
 3    01fec09d  3456    7           8    01fec09d  3584    7
 4    01fec0dd  3456    4           9    01fec0dd  3584    4
```

(111 classes of 3456, 85 of 3600 and 26 of 3584 variants; 17 bits vary in all: the union of the masks is 01fec4dd = bits 0, 2, 3, 4, 6, 7, 10, 14, 15, 17..24; the bits 0, 2, 3, 7, 14, 15, 17..24 are in every mask.) The program builds the ten lists as the member sets of the first class of each list (by enumerating the 2^14 or 2^15 subsets of the mask against the definitions of G and c7)
and lets every other class of the list use them; `selftest` checks, for all 222 classes and all 782,800 variants, that the variant base | s is in G, has the class's c7 and that the class has its size (0 mismatches). **The cube of a list (computed; asserted when the list is built).** The bits 0, 2, 3 of s are *free* in the lists 0, 1, 5, 6 (every member has its partner with the bit flipped) and bit 0 is free in the other six; B is the set of these bits (the cube of the list), and the list is the union over f subset of B of (reps xor f), where reps = the members with no cube bit:
432 reps (lists 0, 1), 450 (lists 5, 6), 1728 (lists 2, 3, 4) and 1792 (lists 7, 8, 9). The classes of the lists 0, 1, 5, 6 have a0 bit 1 set (base bit 1 = 1), which Lemma 8.2 needs for the bits 2, 3; the classes of the other lists have base bit 1 clear and use bit 0 only. A list is stored as the planes of its reps (14 or 16 bit planes per batch of 256: the cube bits are static zeros of the main run) and as packed entries (Section 9.6), 50 batches in all.
S0(a0) >= 8 on G and a0 < 2^29; over the 782,800 variants max S0(a0) = 0xffffbb5c (`selftest`), so (~S0(a0) & M32) <= 0xfffffff7 and no carry leaves a 64-bit lane of the packed words of Section 9.

Per first block over uniform x, every class passes the W7 test for exactly |F7| = 68,157,440 values of x, so the number of passing classes has mean 222 p7 = 3.523 and the number of variants in passing classes has mean 782,800 p7 = 12,422.
Passing classes are strongly correlated (their c7 values are close), so the counts are bursty; only expectations are used.


## 6. Step 3

### 6.1 L* (exact; from 6c77089c, re-checked)

L is the set of (W14, W15) for which rows 14, 15 of both members follow the cells (with the `+` pairs) and the four
expansion differences depending only on (W14, W15) equal the published pair's; |L| = 4096. L* keeps the elements
whose row-16 modular differences equal the characteristic's: |L*| = 32, all with W14x = bd1d3f7b and W15x in

```text
 0:7dd41680  1:7dd41681  2:7dd416a0  3:7dd416a1  4:7dd41a80  5:7dd41a81  6:7dd41aa0  7:7dd41aa1
 8:7dd43680  9:7dd43681 10:7dd436a0 11:7dd436a1 12:7dd43a80 13:7dd43a81 14:7dd43aa0 15:7dd43aa1
16:fdb41680 17:fdb41681 18:fdb416a0 19:fdb416a1 20:fdb41a80 21:fdb41a81 22:fdb41aa0 23:fdb41aa1
24:fdb43680 25:fdb43681 26:fdb436a0 27:fdb436a1 28:fdb43a80 29:fdb43a81 30:fdb43aa0 31:fdb43aa1
```

(y side: W14y = W14x ^ 04400800, W15y = W15x ^ 20000000; element 13 is the published one.) Rows 12..15 of both
members depend only on S and l, not on CV1 or the variant.


### 6.2 Row 16 without a mask table

For l in L*, E16x = C_l + u with u = W0 + s0(W1) (W16 = s1(W14) + W9 + s0(W1) + W0; C_l collects rows 12..15 of l, K16, s1(W14) and W9). With the cell E16[23] = 0 of Table 15, 28 elements of L* can hold row 16 (7319bba enumerated all E16x with the row's nine fixed x-bits, 2^23 per l, and found 1,052,672 pairs (u, l); l = 0, 2, 16, 18 have none).
**With R16x (Section 7.4c) the E cell of row 16 has eight fixed bits and every one of the 32 elements of L* holds row 16 for exactly 65,536 values of E16x: 2,097,152 pairs (u, l)** (`r16.c` with `r16data.h` generated from `experiments/lowm.py`, exhaustive over the 2^24 values of E16x with the eight fixed bits for each l; Appendix A). By Lemma 5.1 u is uniform for a good pair, so Pr[row 16 holds for l] = 65,536 / 2^32 = 2^-16 exactly and the expected number of row-16 hits per probed lane is 2^21 / 2^32 = 2^-11.
The earlier filings read the l-mask of u from a table of 2^32 words. **This filing decides row 16 from the cells.**

**Lemma 6.2 (the exact test).** For each of the 32 l let A16x = E16x + cxA_l with cxA_l = -A12x + S0(A15x) + MAJ(A15x, A14x, A13x) (rows 12..15 of member x for l). Then E16y = E16x and A16y = A16x - 2^29 (mod 2^32), computed for all 32 l.
Row 16 holds for (u, l) iff all of the following hold (cells of row 16 and the two-bit conditions closing at row 16):

```text
E16x & 40461a80 = 00060800         the eight fixed bits 30, 22, 18, 17, 12, 11, 9, 7 of the E cell (E16 has no difference: E16y = E16x; bit 23 is free under R16x)
E16x[4] = E15x[4]                  the '+' pair of the E cells of rows 15 and 16 (E15[4] = E16[4])
A16x[29] = 1                       the A cell 'u' at bit 29: with A16y = A16x - 2^29 the XOR difference is 2^29 iff A16x[29] = 1
A16x[15] != A15x[15], A16x[23] = A15x[23], A16x[25] = A15x[25]          (A15x of l is a constant)
A16x[9] != A16x[20], A16x[18] != A16x[6], A16x[8] = A16x[17]
```

*Proof.* The cells of row 16 are the A cell (u at bit 29), the E cell (eight fixed bits, no difference), the W cell (none); the printed conditions closing at row 16 are the seven of Section 3.3 (A15/A16 three, A16 three, E15/E16 one);
for all 32 l the difference of E16 is zero and cyA_l - cxA_l = e0000000, which is the statement on A16y. *Checks:* the test applied to all 2^24 values of E16x with the eight fixed bits, for each of the 32 l, gives exactly the set of u of the enumeration by `r16.c` (2,097,152 pairs, no pair missing and none added; Appendix A);
the experiments and `selftest` compare it with the generic row check (`row16_ok`) on random and near-miss values. QED.

**The table stage.** A necessary condition on all 32 l at once, from two tables of 4096 words (one 256-bit word each, two 32-bit masks in the 64-bit lanes 0 and 1): for the chunk lo = u mod 2^12 and mid = (u >> 12) mod 2^12,
LO[lo] = (pm, pm & cm) with pm the l for which E16x = u + C_l satisfies E16x[4] = E15x[4] and the fixed bits 7, 9, 11, and cm the l for which lo + (C_l mod 2^12) carries into bit 12;
MID[mid] = (P0, P0 ^ P1) with P_c the l for which E16x satisfies the fixed bits 12, 17, 18, 22 when the carry into bit 12 is c. The mask of the l that can still pass is

    filt(u) = pm & (P0 ^ ((P0 ^ P1) & cm)) = lane 0 xor lane 1 of T,   T = LO[lo] & MID[mid] (a single AND of two words),

a superset of {l : row 16 holds for (u, l)} (it uses seven of the eight fixed bits and E16x[4] = E15x[4]: eight conditions on the bits 4, 7, 9, 11, 12, 17, 18, 22; bit 30 and the A conditions are left to the exact test). For uniform u,
E16x = u + C_l is uniform, so each l is in filt(u) with probability exactly 2^-8 and E|filt(u)| = 32/256 = 0.125; counted over all 2^24 values of u mod 2^24 (Appendix A), the sum of |filt| is 2,097,152 = 32 x 2^16 and filt(u) != 0 for exactly 1,521,152 of them, so Pr[filt(u) != 0] = 1,521,152 / 2^24 = 0.0907 exactly. The tables are built in the preprocessing from the cells (no use of 7319bba's enumeration); `selftest` and the organizer experiments check filt(u) against the generic row check on random and near-miss values (members seen and missed: 0).


## 7. The Step-3 probability for the variants (H2)

### 7.1 The quantity

For a good pair (CV1, a0) and l in L*, let F_l be the event that rows 16..36 follow every cell and every printed
two-bit condition closing at rows >= 16. q3 = average over the 782,800 variants of the 222 classes and over l in L* of
Pr[F_l | good], the probability over CV1 (Lemma 5.1 gives the exact joint law of all second-block words). The
expected number of successful (variant, l) per first block is g x 32 x q3.

(For this filing the event F_l is the same except that the eight value bits of rows 18 and 19 of Table 15 are not imposed, neither are E16[23] = 0 and E16[24] = E17[24] (R16x), and no cell or printed condition is imposed at rows 22..36: those rows are replayed and the event is that the eight registers of the two members agree after step 36 (Sections 7.4b, 7.4c, 7.4d and 7.6). q3_cell denotes the probability of the same event with the cells of rows 22..36 imposed (Section 7.4c); q3 without a subscript is the exact event of this filing. Sections 7.3 and 7.4 describe the estimator and report the registered studies of 7319bba for the Table 15 pattern.)

### 7.2 Lemma 7.1 (what a variant can change)

Rows 16..22 (all their cells and two-bit conditions) are functions of S's rows 12..15, l, and W16..W22, where
W16..W21 are functions of (W0..W6, W9..W15) and W22 = s1(W20) + W15 + s0(W7) + W6. By Lemma 5.1 the law of
(W16..W22) given goodness is the same for every variant (W8 does not occur). **Hence the probability that rows
16..22 pass is identical for all variants, and equal to its value for the published S.** The variant enters rows
23..36 only through W8, which occurs in W23 = s1(W21) + W16 + s0(W8) + W7 and W24 = s1(W22) + W17 + s0(W9) + W8 (and
in later words through them). Its modular differences are fixed (Lemma 4.2 (d)), so only the *values* of W23, W24
move; the conditions of rows 23..36 are the four on W24 (cell `n` at bit 29 and W24[4] != W24[6],
W24[22] = W24[31], W24[20] != W24[27]); all other cells of rows 23..36 are `=` and hold automatically once the
differences cancel. W24x = Z + W8x with Z = s1(W22x) + W17x + s0(W9x), and Z is (nearly) uniform given rows 16..22,
so the four W24 conditions have probability about 2^-4 for every W8.


### 7.3 The estimator (7319bba's design; re-implemented and re-run for this filing, Section 7.4b and Appendix F)

Stages: row 16 exact (the enumeration of 6.2: the stage mean is (1/32) sum_l |R16_l| / 2^32 = 2^-16.994, and the initial particles are drawn exactly from the passing (l, E16) pairs);
rows 17..21: each child proposes E_t^x uniformly with the row's fixed x-bits imposed (exact importance weight 2^-f), sets W_t^x = E_t^x - (the rest of step t), W_t^y = W_t^x + its exact
difference, and checks the whole row; row 22: (W6, W7) drawn uniformly from F6 x F7; rows 23..36: W8 of a variant drawn uniformly from the 782,800 variants of the 222 classes of that time (the same row-22 survivor
is also evaluated with the published W8 for a paired comparison). NP particles, M children per particle per stage, MT tail proposals per particle, multinomial resampling of the survivors after
every stage; the product of the stage means is an unbiased estimator of q3 (the standard SMC normalising-constant estimator). The design is 6c77089c's and 087a18c4's; the program of the registered studies is
7319bba's. **This filing re-estimates q3 with its own program** (Section 7.4b, Appendix F), because it accepts four value patterns of rows 18 and 19: the family of variants, the classes, the filters and every row of the characteristic are those of 7319bba, and this filing changes only how the
good pairs are *found* (Lemmas 8.1, 8.2) and which patterns of rows 16..19 count as a success (Sections 7.4c, 7.6), not which pairs are good or how they are tested. The estimate enters as premise H2.

### 7.4 The registered studies of 7319bba (reported unchanged)

**Study A** (registered 2026-10-10T08:11:18Z, before any listed seed ran): NP = 2048, M = 512, MT = 16384, 32 replicates; rule: the one-sided 99% Student lower bound of the mean of the 32 linear
estimates (t = 2.4528, 31 df), q3_model = 2^(floor(100 log2 LB)/100). Result: mean 2^-74.0187, relative standard deviation 0.0743, lower bound 2^-74.0659, q3_model(A) = 2^-74.07.
**Study B** (registered after study A had been read, to tighten the spread; same program, NP = 8192): mean 2^-73.9987, relative standard deviation 0.0378, lower bound 2^-74.0225,
**q3_model = 2^-74.03 (the Table 15 value; this filing's value is in Section 7.4c)**. All 32 replicates of study B (log2):

```text
-74.022 -73.967 -74.038 -73.934 -74.032 -74.059 -74.000 -74.017 -74.043 -74.070 -73.984 -73.942 -73.949 -73.956 -73.853 -73.965
-74.109 -73.985 -73.979 -73.927 -74.027 -73.983 -73.990 -74.065 -73.925 -74.057 -74.071 -74.052 -74.001 -74.025 -73.984 -73.976
```

| quantity | study A (NP 2048) | study B (NP 8192) |
|---|---|---|
| mean | 2^-74.0187 | 2^-73.9987 |
| relative standard deviation | 0.0743 | 0.0378 |
| 99% lower bound | 2^-74.0659 | 2^-74.0225 |
| **q3_model** | 2^-74.07 | **2^-74.03** |
| stage means (log2) | 16: -16.994, 17: -13.000, 18: -15.004, 19: -6.000, 20: -7.001, 21: -1.000, 22: -11.009, tail -4.015 | 16: -16.994, 17: -13.000, 18: -15.001, 19: -6.000, 20: -7.000, 21: -1.000, 22: -10.998, tail -4.007 |

The stage factors equal, within 0.01 bit, the per-row condition counts of the printed tables (17, 13, 15, 6, 7, 1, 11, 4; 74 in total). 


### 7.4b The studies of this filing (new; preregistered; our own estimator)

The registered studies above measure the Table 15 pattern. This filing accepts four value patterns of rows 18 and 19 (Section 7.6), so q3 is measured again, and for that we wrote our own estimator, `q3smc.c` (Appendix F), from the description of Section 7.3. It shares no code with the earlier filings' program, and no other participant's program was compiled or run here.
Its constants (the cells of rows 0..36, the printed two-bit conditions, the rows 12..15 of the published pair for each l, the variant list) are written by `gen_consts.py` from `experiments/lowm.py`, so the cells it checks are the ones the counted program checks. Stage 16 is an exact enumeration (with the Table 15 cell E16[23] = 0 of this study it gives the 1,052,672 pairs (u, l) of 7319bba's enumeration); stages 17..21 impose the fixed x-bits of the E cell of the row (weight 2^-f) and check the whole row for both members, including the exact difference of the schedule word;
stage 22 draws (W6, W7) uniformly from F6 x F7 (W7 from its affine decomposition, W6 by rejection); the tail draws W8x uniformly from the 782,800 variants and checks rows 23..36 for both members. All parameters are those of the registered studies: NP = 8192, M = 512, MT = 16384, uniform resampling of the survivors after each of the stages 17..22, estimate = the product of the stage means.

**Preregistration** (`PREREG_q3M.txt`, sha256 9187c4519d463838b90eefb4c0aa9df1eb12be95cf463076ad06511c7aaaaabf, stamp 2026-10-12T05:26:30Z, written before any listed seed ran; the file is reproduced in Appendix F).
- *Validation V* (original cells of rows 18 and 19): 64 replicates, seeds 710000..710063. V passes if (a) its mean differs from the registered study B of 7319bba (mean 2^-73.9987, relative sd 0.0378, 32 replicates) by at most 2.576 standard errors and (b) log2 of its one-sided 99% bound is within 0.04 of study B's bound (-74.0225). It is the test that our program reproduces the q3 = 2^-74.03 of the table-free program with Table 15's cells (the program of this filing before its cells were relaxed); if V fails, no q3 is declared from it.
- *Main study* (the four patterns accepted: the eight characters removed from the two E cells): two independent blocks R1 (seeds 720000..720127) and R2 (seeds 721000..721127) of 128 replicates; rule fixed in advance: **declared q3 = 2^x, x = floor(100 log2 min(LB_R1, LB_R2)) / 100**, LB the one-sided 99% Student lower bound of the mean of the linear estimates of the block. Every listed seed was run and is reported (Appendix F); none was dropped or rerun.

**Results.** Validation V: mean 2^-73.9911, relative sd 0.0353, bound 2^-74.0064; z = +0.66 against study B; validation PASSES both preregistered criteria (|z| <= 2.576; bound within 0.04 of -74.0225). Its stage means (log2, rows 16..22 and the tail) are 16: -16.994, 17: -13.000, 18: -14.999, 19: -6.000, 20: -7.000, 21: -1.000, 22: -10.999, tail -4.000, against the registered study B's -16.994, -13.000, -15.001, -6.000, -7.000, -1.000, -10.998, -4.007.
Main study: R1 mean 2^-71.9975, relative sd 0.0714, **bound 2^-72.0191**; R2 mean 2^-71.9868, relative sd 0.0681, **bound 2^-72.0074**. Rule applied: the lowest bound, rounded down to two decimals: **2^-72.02** for the four patterns alone (it was the q3 of the filing before R16x; the q3 used here is that of the joint study, Section 7.4c), 2.01 bits above the Table 15 value 2^-74.03 (structural count 2.00 bits: four patterns of equal weight; exact stage enumeration 1.93, interval 1.78 to 2.09, Appendix B of the filing this one credits for the relaxation).
Stage means of the main study (log2 averaged over the 256 replicates), rows 16..22 and the tail: 16: -16.994, 17: -13.000, 18: -8.000, 19: -10.000, 20: -7.000, 21: -1.999, 22: -11.002, tail -4.000; rows 18 and 19 together contribute -18.00 against -21.00 for Table 15 and row 21 -2.00 against -1.00, the net gain being the sum of the differences. The stages of rows 16, 17, 20, 22 and of the tail are those of the Table 15 study within the sampling resolution.
The pattern diagnostic (a description, not part of the bound; the program's `-d` option, seeds 730001..730003, histogram of the eight value bits E18[1,5,10,11,18,28,29], E19[29] of the 8192 particles that survived rows 16..22, as bits 0..7 in hexadecimal; Table 15's pattern is cd, the others 1b, f6 and 20): seed 730001: 1b:2349 20:1607 cd:2461 f6:1775; seed 730002: 1b:1710 20:2180 cd:2145 f6:2157; seed 730003: 1b:1714 20:1891 cd:2040 f6:2547. Exactly the four predicted patterns occur and no other.

### 7.4c Rows 16 and 17: the R16x relaxation, measured jointly with the four patterns (new; preregistered; our own estimator)

Table 15 imposes E16[23] = 0 (a `0` in the E cell of row 16) and E16[24] = E17[24] (a `+` pair of the E cells of rows 16 and 17, printed again as a two-bit condition). Neither can be dropped alone: a pair that breaks only one of them dies at row 19.
Dropped together they can: at step 19, CH(E18, E17, E16) emits terms at bits 24 and 23 whenever E17 and E16 differ there, and the signed sum of row 19 absorbs them with a different sign solution of S1(E18); the pairs that continue keep the parity E16[23] ^ E19[29] ^ E18[1] ^ E18[5] = 0 together with the four patterns' parities (our backward analysis of the characteristic).
Our own full-path test before this build (rows 16..36, sequential Monte Carlo with same-sample tagging, 6 fresh seeds, 4.0e8 samples, 30,814 collisions, every collision rebuilt and hashed again independently, 0 false) gave a ratio of 1.5055 (+0.590 bit, per-seed 95% interval [0.548, 0.631]) over the four patterns with the six A16 two-bit relations of row 16 necessary (0 of 49.9M violating proposals continue). A preregistered sweep of 30 further pairs of conditions of rows 16..21, each dropped together on top of R16x, found no further gain (each pair, and each member alone, gave 0 collisions; 0 false among 928,760 rehashed).

**The change to the counted program** (`experiments/lowm.py`): the character of bit 23 of `CHE[16]` is `=` instead of `0`, the character of bit 24 of `CHE[17]` is `=` instead of `+`, and the two-bit condition (E, 16, 24, =, E, 17, 24) is removed from `X2`:

```text
 row 16   Table 15 =0=====+00===11=+==01=0=0==+====     program =0=====+=0===11=+==01=0=0==+====
 row 17   Table 15 =0=====+01===u1=+==0==1===1u====     program =0======01===u1=+==0==1===1u====
```

The parity is not tested by the program: every pair that follows the remaining cells of rows 16..36 has zero output difference and is verified with the target before output, so testing it would only add operations, and the estimator below counts exactly the pairs that the program accepts. `row_ok` reads the masks and values of the cells as constants, so `ROWCHECK` and `ROWCOMP` are unchanged.
What the change does cost is at row 16 (Section 6.2): every l in L* now has row-16 values, the table stage has eight conditions instead of nine (E|filt(u)| = 0.125 per lane against 0.0547, Pr[filt(u) != 0] = 0.0907), and the expected number of row-16 hits per probed lane is 2^-11 instead of 1,052,672 / 2^32. These are in the ledger (Section 11) and in the simulation of the counted program (Section 13.3).

**Joint study.** The estimator of Section 7.4b, with its constants written by `gen_consts.py` from this `experiments/lowm.py` (`q3consts_r16x.h`), so that it checks exactly the cells and conditions the counted program checks: the four patterns of rows 18 and 19 and R16x are one carrier, measured together. Stage 16 enumerates all 2^24 values of E16x with the eight fixed bits for each l and reproduces the 2,097,152 pairs (u, l) of Appendix A.
The binary differs from that of Section 7.4b only by a TAG line that counts the full passes whose member x keeps E16[23] = 0 and E16[24] = E17[24]; it draws no random numbers, and built with the constants of Section 7.4b it reproduces the filed outputs of seeds 720000 and 721000 byte for byte (known-answer check).
**Preregistration** (`PREREG_q3R16x.txt`, sha256 18569704b1115d99c138e641986101687836aa408e1f29d670cad354da0691d3, stamp 2026-10-12T16:13:47Z, written before any listed seed ran; reproduced in Appendix G): two independent blocks J1 (seeds 740000..740127) and J2 (seeds 741000..741127) of 128 replicates, NP = 8192, M = 512, MT = 16384; rule fixed in advance: **declared q3 = 2^x, x = floor(100 log2 min(LB_J1, LB_J2)) / 100**, LB the one-sided 99% Student lower bound of the mean of the 128 linear estimates of the block (the spread between replicates carries any overdispersion of the counts within a run). Every listed seed was run and is reported (Appendix G); none was dropped or rerun.

**Results.** J1 mean 2^-71.4296, relative sd 0.1096, **bound 2^-71.4629**; J2 mean 2^-71.4177, relative sd 0.1143, **bound 2^-71.4524**. Rule applied: **q3_cell = 2^-71.47** (the cell event; the q3_used of this filing is in Section 7.4d), 0.55 bits above the four patterns alone (2^-72.02, Section 7.4b) and 2.56 bits above Table 15 (2^-74.03). pooled 256 replicates: mean 2^-71.4236, relative sd 0.1118, bound 2^-71.4474 (descriptive); the pooled mean is 0.569 bits above the pooled mean of the four-pattern study.
Stage means (log2 averaged over the 256 replicates), rows 16..22 and the tail: 16: -16.000, 17: -12.000, 18: -8.000, 19: -11.430, 20: -7.000, 21: -2.000, 22: -11.003, tail -3.999 (row 16 is -16.000 exactly: 2^21 of 2^37 pairs (u, l)). Of the 2,149,260,669 full passes counted in the tails, 1,438,939,086 (a share of 0.6695) keep E16[23] = 0 and E16[24] = E17[24]; the rest use R16x, including the four l (0, 2, 16, 18) that have no row-16 value under Table 15. These shares are a description of the resampled particles, not a part of the bound.

### 7.4d Rows 22..36: the exact end event (new; preregistered; our own estimator)

The program of 96933f8e checked every cell and every printed two-bit condition of rows 22..36 and so accepted only some of the pairs whose two members collide. This program checks the cells and printed conditions through row 21, replays rows 22..36 of both members on the raw schedule words (W6, W7, W8 as drawn; W_t for t >= 22 from the schedule recurrence on each member's own words) and accepts a pair iff all eight registers (A33..A36, E33..E36) of the two members agree after step 36 (the chaining value is common and the feed-forward cancels); the pair is then verified with the target as before. In `experiments/lowm.py` this is `step3b`: the cell test applies for t < 22 and one comparison of the eight register pairs follows row 36.
The ledger is unchanged: each row 16..36 is still charged ROWCOMP + ROWCHECK + 1 = 160, of which the cell test of at most 53 is not executed at rows 22..36; the single comparison of 8 register pairs (at most 16 operations) is covered by those unused charges, and rows 22..36 are reached only by a pair that has passed rows 16..21 (at most 2^-9 as in Section 9.9). The counted program accepts every pair of the exact event; every pair of the cell event is in it (cell_not_exact = 0 in every replicate listed below and in Appendix K).

**The study.** `smc_r16x.c` (Appendix K) is the estimator of Section 7.4c (same cells, same R16x and four-pattern carrier, its own constants header `lab.h`) with two additions: for each of its proposals (W6, W7, W8) of a particle that has passed rows 16..21 it evaluates both the cell event (the stage-22 cells and the tail cells) and the exact event, on the same proposal. Both events therefore have the same particle weights, and exact/cell = (number of exact events) / (number of cell events) over the same proposals estimates q3 / q3_cell. W6 and W7 are drawn uniformly from F6 x F7 and W8 uniformly from the variant list, as in Section 7.4c; the list file is read by the program. Build: `gcc -O2 -DFFBE_RELAX -DR16X smc_r16x.c -lm` (the control without the flags is the Table 15 carrier).
**Preregistration** (written before any of the listed cloud runs; the rule was fixed before the data): two sets of 128 seeds (20001..20128 and 30001..30128), NP = 8192, M = 512, MT = 8192 (2^26 proposals per seed), run on a cloud machine; PASS iff both sets have a pooled ratio >= 2.30, the sets agree within 2 standard errors and cell_not_exact = 0; then q3_used = 2^x, x = floor(100 (log2 LB_cell + log2 LB_ratio)) / 100, with LB_cell = 2^-71.4629 (the lower bound of Section 7.4c, unrounded) and LB_ratio the one-sided 99% lower bound (z = 2.326) of the pooled ratio. Every listed seed was run and is reported; none was dropped.

| set | seeds | cell events | exact events | exact / cell | standard error |
|---|---|---:|---:|---:|---:|
| 1 | 20001..20128 | 261,852 | 651,235 | 2.4870 | 0.0038 |
| 2 | 30001..30128 | 262,599 | 651,923 | 2.4826 | 0.0037 |
| pooled | 256 seeds | 524,451 | 1,303,158 | 2.4848 | 0.0027 |

Rule applied: both sets >= 2.30, the sets differ by 0.0045 < 2 standard errors (0.0106), cell_not_exact = 0: PASS. LB_ratio = 2.4848 - 2.326 x 0.0027 = 2.4786 (log2 1.3095); log2 LB_cell + 1.3095 = -71.4629 + 1.3095 = -70.1534, rounded down to two decimals: **q3_used = 2^-70.16**, 1.31 bits above q3_cell. The two bounds come from different runs, so the product is a bound with coverage at least 98% by the union of the two 99% statements. The control with the table carrier (4 seeds, 2^28 proposals) gave 2.4935 (standard error 0.0216), the same on the cloud and locally; a local pilot of the joint carrier (16 seeds, a different machine) gave 2.4799 (95% interval [2.459, 2.501]); the eight bins of (E16[23], the four patterns) of that pilot have ratios between 2.44 and 2.59 without a trend. Seeds, binary hashes and per-seed outputs are those named in Appendix K.
**Check on this filing's family.** The preregistered runs draw W8 from the family G (12,103,680 variants); the 782,800 variants of the 222 classes are a subset of it. The same program with the variant list restricted to these 782,800 variants (16 seeds 9201..9216, 2^30 proposals, one local machine; a check, not part of the rule) gave 32,754 cell events and 81,028 exact events: ratio 2.4738 (standard error 0.0106), cell_not_exact = 0, consistent with the pooled 2.4848 (difference 0.011, about one standard error).
**What the ratio is used for.** The claim uses only the lower bound q3 >= 2^-70.16 (H2). The upper bound for H3 is derived in Appendix H.4: q3 <= 2^-70.06.

### 7.5 The examined family of this filing

The registered studies drew W8 from the 782,800 variants of the 222 classes, and (W6, W7) uniformly from F6 x F7. This filing examines **exactly that family**: every variant of every passing class is examined, and given a good pair the variant, W6 and W7 have the laws of the studies
(Lemma 5.1: for every variant a0, W7x is uniform on F7 and W6x uniform on F6 given that the pair is good, independent of each other and of the variant). So q3 = the mean over the 782,800 variants and the 32 elements of L* of the study's conditional probability, and the studies' value applies without the hedge
that a different or x-weighted subset would need (0db0eeb6 Section 7.6 prices 0.05 bit for such weighting; there is none here). Our own studies of Section 7.4b draw exactly this family.
**q3_used = 2^-70.16** (the exact end event, Section 7.4d; cell event q3_cell = 2^-71.47, Section 7.4c; four patterns alone with cells 2^-72.02, Section 7.4b). For the Table 15 pattern the registered floor of study B is 2^-74.03 (its one-sided 99% bound is 2^-74.0225, its mean 2^-73.9987; study A's bound is 2^-74.0659), and fb039a6e measured the same quantity over the whole family G (a preregistered 128-replicate study: one-sided 99% bound 2^-74.0088) and over a kept-fibre-weighted pool (2^-73.9984);
our validation V reproduces the registered study (Section 7.4b). That the dependence on the variant is the four W24 conditions, about 2^-4 for every W8 (Lemma 7.1), is unchanged by the relaxations, which act on rows 16..19 only.
Real first blocks (7319bba, Section 13.1, Table 15 cells): the row-16 pass rate of the attack's own good pairs is the exact 1,052,672 / 2^32 (z = +0.88 and +0.51 over 424,363 and 1,693,297 passes); this program's own simulation (Section 13.3) finds row-16 passes at its exact rate under R16x, 2^-11 per probed lane.

### 7.6 Rows 18 and 19: the accepted value patterns (credit: Jbenisek's ffbe30bb-ac92-4191-a589-3bf32661ee7d)

Table 15 fixes the value bits E18[1] = 1, E18[5] = 0, E18[10] = 1, E18[11] = 1, E18[18] = 0, E18[28] = 0, E18[29] = 1 and E19[29] = 1. They are not all required. With every other cell and printed two-bit condition of rows 4..36 kept, exactly four patterns of these eight bits admit a 37-step semi-free-start collision for the published dense part
(an all-solutions enumeration with a verified 37-step model, Bitwuzla and Z3, done for ffbe30bb; the three further collisions are checked below), because the bits enter only through six parity conditions: E18[1] = E18[11], E18[1] != E18[28], E18[10] = E18[29], E18[10] = E19[29], E18[5] = E18[18] and E18[5] ^ E18[1] ^ E18[10] = 0.
The seven E18 bits enter only through the signs of the signed difference of S1(E18) at step 19 (each output bit of S1 is the XOR of three taps, and the sign of the difference at that bit depends on the XOR of the two taps that carry no difference), and E19[29] only through E18[29] ^ E19[29] = 0 in the signed difference of Ch(E19, E18, E17) at step 21.
The relaxation, its pattern table, the 74 single-flip tests, the seven unforced candidates of rows 20..22 (all necessary) and the exact stage enumeration (3.80 times as many W18 reach row 19 with the four patterns, 1.93 bits, interval 1.78 to 2.09) are ffbe30bb's and are quoted, not redone here, except for the check of the three alternative collisions and the q3 studies of Section 7.4b, which were run for this filing's family.

The strings of the E cells of rows 18 and 19 in `experiments/lowm.py` (`CHE[18]`, `CHE[19]`) are now

```text
 row 18   Table 15 ==10===uu====0==n===111===01==1=     program =======uu=======n=====1====1====
 row 19   Table 15 ==1====00====1==0==========1====     program =======00====1==0==========1====
```

(the remaining `1` of row 18 are E18[9] and E18[4], which stay imposed; so do the differences `u`, `n` and every other character). That is the whole change to the counted program: `row_ok` tests the masks and values of the cells as constants of the straight-line text, so the operation counts of Section 9 (`ROWCHECK`, `ROWCOMP` per row) and the ledger are unchanged;
no operation was added and none removed. The six parity conditions are not tested separately: the exact signed-difference check of both members that `row_ok` always made, at rows 19 and 21, rejects the other patterns, and a separate test would only add operations. The patterns accepted, as flips of Table 15's values (E18 bits 29,28,18,11,10,5,1 | E19 bit 29):

| pattern | flipped bits of Table 15's values | flip masks (E18, E19) | value bits (E18[29,28,18,11,10,5,1] E19[29]) |
|---|---|---|---|
| 0 Table 15 | none | 0x00000000, 0x00000000 | 1 0 0 1 1 0 1 \| 1 |
| 1 | E18[5], E18[10], E18[18], E18[29], E19[29] | 0x20040420, 0x20000000 | 0 0 1 1 0 1 1 \| 0 |
| 2 | E18[1], E18[5], E18[11], E18[18], E18[28] | 0x10040822, 0x00000000 | 1 1 1 0 1 1 0 \| 1 |
| 3 | E18[1], E18[10], E18[11], E18[28], E18[29], E19[29] | 0x30000c02, 0x20000000 | 0 1 0 0 0 0 0 \| 0 |

The organizer experiment `a0-sfs-r37` imposes pattern t mod 8 on its construction of trial t (`IMP` and `PAT` in `experiments/lowm.py`): patterns 0..3 are the four above with E16[23] = 0 and E17[24] = E16[24], patterns 4..7 the four R16x patterns with E16[23] = 1 and E17[24] != E16[24] (value bits E18[1,5,10,11,18,28,29], E19[29] with E18[11] != E18[1], E18[28] = E18[1], E18[10] = E18[29] = E19[29], E18[5] = E18[18] = 1 ^ E18[1] ^ E18[10]; Section 7.4c); it checks every cell of rows -4..36 with the program's own `row_ok`, which accepts all eight; for trials 0..15 the constructed chaining value is fed to the counted online program, which must find exactly the constructed pair (Section 13.2).
**Check of the three alternative collisions** (`check_alt.py`, Appendix F; words MSB first, chaining value common, x = M', y = M; the pairs are ffbe30bb's, and here they are compressed 37 steps again and their cells tested with this package's `row_ok` and, for contrast, with the Table 15 cells of the program this one derives from):

```text
pair (x = M', y = M)         collides  cells of this lowm.py    cells of Table 15       
Table 15 (published pair)    True      True                     True                    
G1                           True      True                     False                   
G2                           True      True                     False                   
G1 xor G2                    True      True                     False
```

The CVs and messages of the three pairs are listed in `check_alt.py` (Appendix F). They are 37-step semi-free-start collisions, not ordinary collisions. Rows 16..22 are functions of the rows 12..15 of S, of l and of W16..W22 only (Lemma 7.1), so what the accepted patterns are is the same for every variant of the family.

## 8. The algorithm

### 8.1 Lemmas 8.1 and 8.2 (the class test, the W6 test and the cube of a list)

Let x = A_{-1}, cb = C6 - A_{-2}, q = A1 ^ x, and for a class with base and mask put

```text
CB3 = cb + (A1 & x) + (base & q),   KZ = K3C + x - (A1 & A2) - (base & FA),   FA = A1 ^ A2,   C4 = 000b362e,   e4 = a0 + C4,   e3 = KZ - (s & FA).
```

**Lemma 8.1.** (a) The class passes the W7 filter at x iff F7(c7 - x). (b) For a0 = base | s of the class, W6x = cb + phi(a0, x) = CB3 + (s & q) - H, mod 2^32, where H_j = e4_j for the bits j with E5_j = 1 and H_j = e3_j for the bits with E5_j = 0 (E5 = e7f2c81f).
Hence a0 is good (W7x in F7 and W6x in F6) iff its class passes and F6(CB3 + (s & q) - H).
*Proof.* (a) Section 5.1. (b) W6x = C6 - A_{-2} + MAJ(A1, a0, x) - CH(E5, e4, e3) with e4 = a0 + C4 and e3 = K3C - MAJ(A2, A1, a0) + x (Section 5.1), and CH(E5, e4, e3) selects bit j of e4 where E5_j = 1 and of e3 where E5_j = 0.
MAJ(A1, a0, x) = (a0 & (A1 ^ x)) | (A1 & x) with disjoint bit sets, so MAJ = (a0 & q) + (A1 & x); likewise MAJ(A2, A1, a0) = (a0 & FA) + (A1 & A2). Since a0 = base + s with base & s = 0 (Section 5.3), a0 & m = (base & m) + (s & m) for every mask m.
Collecting the scalar terms gives CB3 and KZ. QED. (Checked on every lane of every pass plane of the experiments and of `selftest`, 0 mismatches.)

**Lemma 8.2 (the cube).** Let b be 0, 2 or 3, and let a0 have bit 1 set if b is 2 or 3. If q_b = 1 then W6x(a0 xor 2^b) = W6x(a0) (equality mod 2^32); if q_b = 0 then W6x(a0 with bit b set) = W6x(a0 with bit b clear) - 2^b.
Hence for a rep t (no cube bit set), Q0 = {b in B : q_b = 0}, cu a submask of Q0 and i a submask of I = B xor Q0: W6x(t xor cu xor i) = W6x(t) - cu (mod 2^32), cu read as the integer sum of its bits.
*Proof.* A1 = 62827866, FA = fafd5ca2, C4 = 000b362e, E5 = e7f2c81f: bits 0, 2, 3 of FA are 0, so e3 = KZ - (s & FA) does not depend on s_b; bits 0..4 of E5 are 1, so H_b = e4_b for b = 0, 2, 3. In e4 = a0 + C4: C4_0 = 0, so e4_0 = a0_0 and there is no carry out of bit 0;
for b = 2, 3 with a0_1 = 1 (and C4_1 = C4_2 = C4_3 = 1) the carry out of bit 1 is 1, a0_2 + 1 + 1 gives the sum bit a0_2 and carry 1, a0_3 + 1 + 1 gives the sum bit a0_3 and carry 1, so e4_2 = a0_2, e4_3 = a0_3 and the carry into bit 4 is 1 whatever a0_2, a0_3 are.
Thus s_b enters W6x = CB3 + (s & q) - H exactly through (q_b - 1) s_b 2^b, which is 0 if q_b = 1 and -s_b 2^b if q_b = 0. QED. (Checked on 27,840 (class, x, member, combination) tuples in `selftest`.)

*The cube of a list.* The bits of {0, 2, 3} in which a list is closed under the flip form its cube B (computed; Section 5.3): B = {0, 2, 3} for the lists 0, 1, 5, 6 (their classes have a0 bit 1 set) and B = {0} for the other six. The list is the union over f subset of B of (reps xor f), reps = the members with no cube bit (432, 432, 450, 450 and 1728, 1728, 1728, 1792, 1792, 1792 reps).
For a first block put I = q & B (the cube bits that do not matter at this x) and Q0 = B xor I. By Lemma 8.2, W6x(t xor f) = W6x(t) - (f & Q0) for a rep t and f subset of B, so one test of F6 on W6x(t) - cu decides the 2^|I| members t xor cu xor i, i subset of I: the program computes the sums W6x(t) once (the main run) and obtains the other 2^|Q0| - 1 runs by subtracting the constant cu from the stored sums.
Given that a class passes the W7 test, x mod 16 is uniform: in both affine pieces of the bitwise form of F7 (Section 5.1) the bits w0..w3 of w = c7 - x are individually free (w0 = w28, w1 = w18 (= w29), w2 = w19 tie them to other free bits), so w mod 16 and hence x mod 16 = (c7 - w) mod 16 are uniform; q_0, q_2, q_3 are independent uniform bits and |I| is Binomial(|B|, 1/2).

The scalars CB3 and KZ are computed once per passing class; the planes of the reps (14 or 16 bits) are the only lane-dependent data. Both tests are programs on *planes*: a plane is a 256-bit word holding one bit of each of 256 lanes (the lanes of a batch are 256 consecutive reps of a list).

### 8.2 The online algorithm

```text
input: N_FB, V_MAX; precomputed: S, L*, the ten lists as planes of reps and packed entries, the 222 class descriptors, the c7 planes, the chunk tables LO and MID, the lane-scan table, per-l constants
V = 0
for f = 1 .. N_FB:
    draw two uniform 256-bit words; M0 := their sixteen 32-bit fields; CV1 := F_37(IV, M0)                                     [1 unit]
    x := A_{-1}; cb, q, CB2 = cb + (A1 & x), KXA = K3C - (A1 & A2) + x; the 17 planes of q; cv_pre(CV1)                          (Section 9.2)
    plane P7 := F7(c7 - x) over the 222 class lanes (bit-sliced)
    for each set lane c of P7:                                                                                                    (passing class)
        CB3, KZ; the planes of CB3 (32), KZ (bits 0..28) and base (18 bits) are formed and stored; I = q & B, Q0 = B xor I        (Section 9.3)
        main run: for each sweep of two batches of reps of the class's list:
            load the 96 scalar planes; for each batch: load the planes of the reps; sums W := W6 program (all 32 sums, stored, if Q0 != 0); pass plane := F6(W)   (Sections 9.4, 9.5)
            gather(pass plane, cu = 0)
        if Q0 != 0: for each batch: reload the 32 sums; for each nonzero submask cu of Q0: pass plane := F6(W - cu); gather(pass plane, cu)               (Section 9.5)
        where gather(plane, cu): for each set lane (r, i) of the plane (11-bit chunk scan):
                    entry := (packed word i of the batch)[part r] xor BP(class) xor D[cu]
                    for each submask ii of I (the 2^|I| members of this rep): place entry xor D[ii] in the next slot of the group register
                        when the group register holds four entries: U := packed row-16 address of the group                           (Section 9.7)
                            for each of the four lanes: u := U lane; G := filt(u) (two table reads)
                                if G != 0: for each l in G: if exact(u, l): recompute W6, W7; rows 16..21 of both members by cells with early abort, rows 22..36 replayed, eight registers compared   (Sections 7.4d, 9.8, 9.9)
                                    if all rows pass: build m, m'; if digest(m) = digest(m') and m != m': output, halt
    the last group of the first block is padded by repeating its last entry and processed
    V += the counted work of this first block; if V > V_MAX: halt (failure)
halt (failure)
```

The loop is the function `attack(nfb, vmax)` of `experiments/lowm.py` (`python3 lowm.py attack N V`): at most N first blocks, V the counted data-dependent operations of Section 9, halt when V exceeds the cap; an output is verified with the target digest before it is returned.

### 8.3 What is not assumed

No property of x other than being a 32-bit word is used (and, for the cube, that x mod 16 is uniform given that a class passes: Section 8.1), and nothing about the correlation of the classes of one first block: the ledger uses only the exact marginal law of each class test (probability p7 = |F7| / 2^32) and of each variant's F6 test given its class passes (p6 = |F6| / 2^32, exactly,
because cb is uniform and independent of x), the law of |I|, and linearity of expectation. Padding lanes (the repeated last entry of a first block's last group) are probed and charged; a duplicated member that hit would be processed twice, which changes the cost (charged) and not the set of pairs found.

## 9. The counted program

### 9.1 Machine and pricing

256-bit word RAM, 64 registers, every executed primitive counted (loads, stores, branches and address additions included). 32-bit values are kept in the low bits; a reduction mod 2^32 is one AND; a 32-bit rotation pattern (S0, S1, s0, s1) costs 8: d = x | (x << 32) (2), three shifts and two XORs and one mask.
A conditional branch tests a register for nonzero and is one primitive. Every address that is not a register value is formed by a counted add (one add per plane or word load; a table read is an index extraction, an add of the table base and a load). The program text is straight-line code.
The target compression of a first block is one unit and its internal operations are not counted again.

**Plane algebra.** The plane programs are executed by `lowm.py` on Python integers of 256 bits through a small algebra whose every call is a primitive of the straight-line text: a plane carries a *static constant tag* (all-zero, all-one: a constant of S such as C4, E5, A1 ^ A2) and an *inversion flag* (the stored word is the complement of the true plane).
These are compile-time facts of the text, not data: x ^ 0 = x, x ^ 1 = ~x (flag flips; no primitive), x & 0 = 0, x & 1 = x, x | 1 = 1, x | 0 = x cost nothing; an AND or OR of two planes with equal flags is one primitive (both flagged: De Morgan, the stored words are combined with the dual operation);
an AND or OR of unequal flags costs a NOT first (2 primitives); every other XOR, AND, OR on dynamic planes is one primitive. A full-adder bit is `xy = a ^ b; sum = xy ^ c; carry = a ^ (xy & (a ^ c))`: 5 primitives, 4 without the sum; with a static constant operand bit b: xy = a or ~a (free) and carry = a & c or a | c: 1 primitive.
The counter `CN.n` of the algebra is the count of the plane programs; `process_cv` asserts the counts of the plane programs (W6 by cube size, the subtraction runs, F7 = 166) at every execution (the counts do not depend on the data). The scalar and control steps are counted where they execute by the constants below.

### 9.2 Fixed per first block: FIXED = 615 operations

First block words: 2 random words and the 16 fields (field 0 of a word: and; fields 1..6: shr, and; field 7: shr): 30; control 16 (loop counter add and compare-branch, the cap test, address arithmetic not itemised below): 46. Then:

- **Class test, 397:** -x mod 2^32 (2); the planes of -x, z_j = 0 - ((s >> j) & 1), consumed bit by bit (3 per plane, 2 for plane 0: 95); the 32 planes of c7 (32 loads and 31 address adds: 63); the adder c7 + (-x) with sums for the 17 bits {0, 1, 2, 9, 10, 11, 12, 18, 19, 22, 23, 26, 27, 28, 29, 30, 31} (140) and the F7 test (26):
  F7 is in the bitwise form of Section 5.1; F7_OPS = 166; the mask of the 222 valid lanes (1); the scan of the plane (SCAN_FIX = 70: for each of the four 64-bit parts the extraction of the part (1 or 2) and for each of its six chunks (five of 11 bits, one of 9) the extraction (1 or 2) and a zero branch).
- **Scalars and planes, 172:** cb = C6 - A_{-2} (2), q = A1 ^ x (1), A1 & x (1), CB2 = cb + (A1 & x) (2), KXA = K3C - (A1 & A2) + x (2); the 17 planes of q (bits 0, 2, 3, 4, 6, 7, 10, 14, 15, 17..24; 50) and their stores (17 stores and 16 address adds: 33);
  `cv_pre` (81 as in 0db0eeb6 Section 9.2: e0b, kap0, C = RBASE + (kap0 - e0b), x12, n12, X, Em2, kap1 and the broadcasts of the constants to four lanes, and the unpacking of the chaining value from the compression output).

### 9.3 Per passing class: 410 + 6 operations, and per subtraction run

Per set lane of the class plane: table address 1, table load 1, chunk offset add 1, c & (c - 1) 2, branch 1: CLS_LANE = 6. Then: five loads of the class descriptor (base, BP = base | ((~S0(base) & M32) << 32), list pointers, batch count, cost word) with their address adds (10);
CB3 = CB2 + (base & q) (3) and KZ = KXA - (base & FA) (3); the planes of CB3 (95), of KZ for the bits 0..28 (86; e3 is needed up to bit 28, the highest bit with E5 = 0) and of base for the 18 bits that are not in every mask (54), 3 per plane; their stores
(79 stores and 79 address adds: 158); one work-counter update (1): 10 + 6 + 235 + 158 + 1 = 410. The cube: the mask B of the list (load and address add 2), I = q & B (1), Q0 = B xor I (1), the tests I == 0 and Q0 == 0 (2): CF_CLASS = 6.
**The main run** (cu = 0) has no extra cost: the cube planes of s are static zeros of the text. **A subtraction run** (a nonzero submask cu of Q0, per batch, in increasing order): the next submask (cu - Q0) & Q0 and its test (3); BP xor D[cu] with D[cu] = cu | (S0(cu) << 32) read from a table of eight words (address 1, load 1, xor 1: 3);
the work-counter update (1): RUN_CU = 7, and the pass plane of F6(W - cu) (Section 9.5).

### 9.4 Sweeps of two batches

A list of r reps is processed in nb = ceil(r / 256) batches (2 for 432 and 450 reps, 7 for 1728 and 1792), two at a time. A sweep loads the 96 scalar planes it needs once for both batches: zq (17), zKZ (29), zCB3 (32), zb (18), each one load and one address add, plus 3 of control: SWEEP_OVH = 195.
Per batch: the stored planes of the reps (14 or 16, with their address adds) and the two pointers of the batch (30 or 34 operations).

### 9.5 The W6 program of one batch and the subtraction runs

Straight-line on planes (Lemma 8.1), with sums produced only for the bits that are used. The cube bits of s (0, 2, 3 or 0) are static zero planes in the main run, so the constants fold. For the lists with the cube {0, 2, 3}:

| step | primitives |
|---|---|
| a_j for the 14 non-cube mask bits: a_j = s_j for the 11 bits in every mask; a_j = s_j or zb_j for bits 4, 6, 10; a_j = zb_j (loaded) elsewhere | 3 |
| e4 = a + C4 (C4 static: carry = a & c or a \| c), sums for the 19 bits with E5 = 1 | 42 |
| e3 = zKZ - (s & FA) (FA & mask has 9 dynamic bits: 7, 10, 14, 18..23), sums for the 13 bits with E5 = 0 (5..28) | 66 |
| Sq = s & zq on the 14 non-cube mask bits | 14 |
| W6a = zCB3 + Sq | 95 |
| W = W6a - H, sums for the 20 bits {1, 2, 3, 8, 9, 10, 12, 13, 14, 15, 16, 18, 19, 20, 25, 26, 27, 29, 30, 31} that F6 reads (all 32 sums when Q0 != 0: 168) | 157 |
| F6 in the bitwise form of Section 5.1: pass = (w8 ^ w25) & ~fail | 27 |
| **total** | **404** (415 with all 32 sums) |

For the lists with the cube {0}: 420 and 431. The ledger's W6_OPS is the table by (cube bits, all sums): k = 3: 404 / 415, k = 1: 420 / 431. The pass plane carries no inversion flag in the shipped text; `measure_ops` adds one primitive if it did, and `process_cv` asserts the total. A partial batch (the last, with fewer than 256 live lanes) costs one more AND with the lane mask.
**The subtraction runs.** When Q0 != 0 the 32 sums of each batch (flagged planes included) are stored after the main run (SPILL = 64: 32 stores and 32 address adds) and reloaded once per batch for all its runs (64); for each nonzero submask cu of Q0 the pass plane is F6(W - cu) with the static constant cu: a borrow chain of one primitive per bit,
sums for the 20 bits that F6 reads, and the F6 test; SUBF = k = 3: cu = 1: 94, cu = 4: 89, cu = 5: 95, cu = 8: 88, cu = 9: 94, cu = 12: 89, cu = 13: 95; k = 1: cu = 1: 94 primitives by (cube bits, cu). Exactness: W6x(rep xor cu) = W6x(rep) - cu (Lemma 8.2), checked on every lane of every run (Section 13).
**Registers.** The two batches of a sweep are processed together bit by bit, j = 0..31; the loaded planes of bit j are dead after use. Each batch holds the four carries (e4, e3, W6a, W) and the F6 operands that are kept for later bits, folded as soon as both operands of a term exist:
the pairs (w1, w12), (w2, w13), (w3, w14), (w14, w18), (w15, w19), (w9, w26), (w10, w27), (w16, w20), (w8, w25) and the three single bits w29, w30, w31; at most ten values at any bit. With at most six temporaries that is at most 20 live planes per batch, 40 for the sweep, plus about eight addresses, counters and constants: below 64, with no spill.
A subtraction run holds the 32 reloaded sums, the borrow and at most ten F6 operands (about 45 planes); the scan state of its pass plane (about 10 values) is added only after the F6 test has released its operands: below 64.

### 9.6 Scan of the pass plane, the reps and their members

The pass plane (zero in the unused lanes) is scanned in four 64-bit parts of six chunks (SCAN_FIX = 70 per plane); per set lane (a passing rep): table address 1, table load of the bit index 1, add of the chunk offset 1, add of the batch word pointer 1, load of the packed word 1, c & (c - 1) 2, loop branch 1: SCAN_LANE = 8.
The packed word i of a batch holds in its 64-bit part r the entry s | (S0(s) << 32) of the rep of lane 64 r + i. The entry is extracted (EXTR = 1, 2, 2, 1 for r = 0..3) and XOR'ed with BP xor D[cu] (BP in the main run; the result is a0 | ((~S0(a0) & M32) << 32) for the member a0 = base | rep | cu, because S0 is linear and base, rep, cu have disjoint bits).
If I = 0 the member is placed: shift into slot k of the group register 1, or 1, slot update (sh + 64) & 255 2, branch on the full group 1, work-counter update 1, and the xor 1: PLACE = 7. If I != 0 the rep stands for m = 2^|I| members: the first is placed (6, the xor with BP xor D[cu] being 1 of the rep's operations), and for each further submask ii of I: the next submask (ii - I) & I and its test (3),
D[ii] (address 1, load 1) xor'ed (1) and placed (6): 12 per further member and 3 for the final test; in all EXTR + 12 m - 2 per rep. A group of four members is complete after four placements; the last group of a first block is padded (PAD_OPS = 7).

### 9.7 The packed group: GROUP_BODY = 31, probe 11 + 12 + 12 + 12

Gw holds in each 64-bit lane a0 in bits 0..31 and ~S0(a0) & M32 in bits 32..63. With LM = 2^32 - 1 in every lane (as in 0db0eeb6 Section 9.6): Sw = Gw >> 32 (1); E0 = (Gw + bc(e0b)) & LM (2); mj = Gw & bc(x12) (1); ch = (E0 & bc(X)) ^ bc(Em2) (2); S1(E0) with the 8-primitive pattern (8);
W1 = (bc(kap1 + 1 + 3 2^32) + Sw - mj - S1(E0) - ch) & LM (5); s0(W1) (8); U = E0 + s0(W1) + bc64(C) (2); clearing the group register (1) and the work-counter update (1): 31. Lane k of U holds u + {0, 2^32, 2 2^32}, u = W0 + s0(W1) mod 2^32 (verified on 400 lanes with extreme chaining-value words: 0 mismatches).
The probe of lane k: the lane to the low end (k > 0: 1); lo = v & 0xfff (1); mid = (v >> 12) & 0xfff (2); the address of LO (add of the table base: 1; the table MID is placed at address 0, so mid is its address) and the two loads (2); T = LOw & MIDw (1), T >> 64 (1), their xor (1), & M32 (1); the branch on nonzero (1): 11 for lane 0 and 12 for the others.
This is the stage of Section 6.2; for G = filt(u) the table words are LOw = (pm, pm & cm) and MIDw = (P0, P0 ^ P1) in the 64-bit lanes 0 and 1.

### 9.8 Survivors and the exact test

When G != 0 (probability exactly 1,521,152 / 2^24 per lane, Section 6.2): u = lane & M32 and the scan of the 32-bit mask G in three chunks (SURV_FIX = 8); for each set bit l: table address 1, load 1, chunk offset 1, c & (c - 1) 2, branch 1, work-counter update 1 and the l-to-constant-address add 1 (SURV_LANE = 7), then the exact test of Lemma 6.2, straight-line, EX_OPS = 34:
e = u + C_l (load C_l 2, add 1, and 1); (e & 40461a80) ^ 00060800 (2); (e ^ E15x[4] word) & 0x10 (load 2, 2); A = e + cxA_l (load 2, add 1, and 1); (A & 22808000) ^ VA_l (and 1, load 2, xor 1); the three pair conditions with shifts 11, 12, 9 (x1 = A ^ (A >> 11), x2, x3: 6; and with 0x200, 0x40, 0x100: 3; or 2; xor 0x240: 1);
the OR of the four results (3) and the branch (1): 34, with no early exit.

### 9.9 The rare path

A pair with a row-16 pass for some l (probability at most 2^21 / 2^32 = 2^-11 per probed lane): work-counter update and lookup of the member (1 + 2); recompute W6 and W7 (RECOMP = 35); W0..W5 and W8 (201); then for each such l the y-words (8) and rows 16..36, each row 106 + 53 + 1 (both members' W 20, CH 3, E 14, MAJ 4, A 12 per word; the cells and two-bit conditions closing at the row at most 53, executed for rows 16..21 only, with early abort; rows 22..36 are replayed without a cell test and the eight registers are compared after row 36, at most 16 operations, covered by the unused 53 of those rows; the work-counter update 1),
charged for rows 16 and 17 always and for rows 18..36 with probability at most 2^-9 each (the SMC stage factor of row 17 is 2^-12 under R16x, Section 7.4c). These are the counts of 0db0eeb6 Section 9.7 and 7319bba.

### 9.10 The work counter V and the cap

V counts every executed data-dependent primitive: each of the following updates it by a constant (one primitive each, counted in the item): a passing class (its fixed price, sweeps, main run and spills), a subtraction run (its F6 test and scan), a member (its placement and, for a rep, its scan and extraction), a group (its body and four probes), a survivor lane, a survivor bit (its exact test) and every row of the rare path.
The data-independent part (FIXED) is charged per first block. The cap is tested after every first block (compare and branch, in the control of 9.2). The overshoot past V_MAX is at most the maximal data-dependent work of one first block, vmax_fb = 94,072,525,785 (every class passes with its worst |I|, every rep good, every l surviving, every probe hitting), which the ledger charges.


## 10. Success probability, independence and caps

Let a *trial* t = (f, a0, l) be a first block f, a variant a0 of a passing class and l in L*, and A_t the event that a0 is good for f, the pair follows every cell and printed two-bit condition of rows 16..21 and the eight registers of its two members agree after the replay of rows 22..36 (Section 7.4d). The program examines every good pair of every processed first block (Lemma 8.1) and every l whose row 16 holds
(Lemma 6.2, exact), so it finds a success iff some A_t occurs before the cap, and every output is verified (Lemma 6.1). Let X_f = sum over the trials of f of 1[A_t] and X = sum_f X_f.

- **Expectation.** E[X_f] = g x 32 x q3 (Lemma 5.1 and Section 7) with g = p7 p6 x 782,800 = 830.988 the expected number of good pairs per first block (exact: each of the 222 classes passes with probability p7 and each of its variants then passes F6 with probability p6), and E[X] = N_FB g 32 q3.
  With q3 >= q3_used = 2^-70.16 (H2): E[X] >= mu0 = 0.49694499 (H7) for N_FB = ceil(mu0 / (g 32 q3_used)) = 24,650,628,322,256,370 = 2^54.45247, where mu0 is the smallest 8-decimal number strictly above -ln(0.61 - Pcap - 2^-60) / (1 - 2^-10.4), with Pcap = 0.00138975 the assumed bound of the work-cap failure probability below (Appendix C).
- **One first block (H3).** By Bonferroni, Pr[X_f >= 1] >= E[X_f] - sum over pairs t < t' of f of Pr[A_t and A_t'] = E[X_f] - (1/2) sum_t Pr[A_t] E[X_f - 1 | A_t]. H3: the average of E[X_f - 1 | A_t] over the trials t with the weights Pr[A_t] (the only quantity this sum needs) is at most delta = 2^-9.4, and we assume the bound for every trial t, so Pr[X_f >= 1] >= (1 - 2^-10.4) E[X_f].
  H3 splits into (a) the same variant with another l: at most 2^-11 (7319bba measured 0 further successes among 19,620,436 distinct Step-3 successes of its SMC, rule-of-three bound 2^-22.65; the four accepted patterns multiply the chance of passing rows 18 and 19 by about 4 and R16x the chance of the path by about 1.6, with four more l holding row 16, which gives about 2^-19.8, far below 2^-11), and (b) other good pairs of the same first block (rho and q3 as stated below; the measurements of Appendix H.6 are program checks, not a proof): at most rho x N_good x 32 x q3 with rho <= 2^35 (the measured factor at row 16 is 0.98 and 1.00), q3 <= 2^-70.06 (the exact event; derived in Appendix H.4: the 99 percent upper bound 2^-71.38 of the cell event times the 99 percent upper bound 2^1.32 of the exact/cell ratio) and
  N_good <= 782,800 (all variants of the family, 2^19.58), so (b) <= 2^35 x 2^19.58 x 2^5 x 2^-70.06 = 2^-10.48 and delta <= 2^-11 + 2^-10.48 = 2^-9.71 < 2^-9.4 (margin 0.31 bit; the break-even q3 is 2^-69.56). (N_good is the number of all variants of the family, as in the earlier filings on this family; no size-biased mean is needed.)
- **Many first blocks (H1).** Distinct first blocks have independent chaining values, so the events X_f >= 1 are independent and Pr[X >= 1] >= 1 - exp(-sum_f Pr[X_f >= 1]) >= 1 - exp(-(1 - 2^-10.4) mu0).
- **Work cap.** The data-dependent work v_f of a first block (everything except its compression and its FIXED operations) has mean vbar = 46070.09 (Section 11) and is at most vmax_fb = 94,072,525,785. The v_f are independent (H1), so by Chebyshev
  Pr[sum v_f > (1 + s) N_FB vbar] <= E[v_f^2] / (s^2 N_FB vbar^2) <= vmax_fb / (s^2 N_FB vbar) = Pcap with the slack s = 2^-12: Pcap = 2^-9.49 (<= 0.00138975). V_MAX = ceil((1 + s) N_FB vbar) = 1,135,933,807,571,123,291,014 is exceeded with probability below Pcap; the run then fails, which is accounted for here.
  No part of v_f depends on a conditional law of the scalars: the plane programs cost the same for every data, and the data-dependent items are linear in the numbers of passing classes, good pairs, groups, survivors and hits, whose exact means the ledger uses.
- **Success.** Pr[output a collision] >= 1 - exp(-(1 - 2^-10.4) mu0) - Pcap - 2^-60 = 0.3900000020 > 0.39 (the 2^-60 covers a repeated first block among N_FB draws of 512 bits). Any output is a verified collision, independent of the premises.

## 11. Ledger (exact; `python3 experiments/lowm.py ledger`; the program of Appendix B reproduces it from the stage prices)

```text
T = A_C + A_S + DEV + N_FB + (N_FB x 615 + V_MAX + vmax_fb + PRE + FIN) / C + 6
  A_C = 2^60   characteristic search and SFS-pair search of the paper (allowance, H4)
  A_S = 2^50   Step-1 re-solve, bounded by its caps (Section 11.2)
  DEV = 2^40   all development computation (Section 13.4; unchanged)
  N_FB = 24,650,628,322,256,370 compressions (2^54.45247; mu0 = 0.49694499, q3 = 2^-70.16, g = 830.988 good pairs per first block)
  615  fixed operations per first block (Section 9.2: first block and control 46, class test 397, scalars and planes 172)
  V_MAX = 1,135,933,807,571,123,291,014 = ceil((1 + 2^-12) N_FB vbar), vbar = 46070.09 operations, of which (per first block, exact expectations or the stated bounds)
               class scans (6 per passing class, 222 p7 classes):                                  21.14
               passing classes (p7 x [preparation, runs, sweeps, W6 programs, scans, reps, members]):  24666.75
               groups (E ceil(N/4) <= (g + 3)/4 groups of 31 + 47, plus the last-group padding):  16269.77
               survivors (per probed lane 0.0907 x 8 + 32/256 x (7 + 34); probed lanes <= g + 3): 4879.12
               row-16 hits (every probed lane may hit, 2^21 / 2^32 per lane):                     233.31
  vmax_fb = 94,072,525,785 (one first block's maximal work: every class passes, every variant is good, every l survives, every probe hits)
  PRE = 2^38 operations (bound on all precomputation, Section 14.2); FIN = 1600 operations and 6 compressions
N = C T = 4,267,574,450,285,246,393,181     ->   T = 2^60.485400   ->   time_log2 = 60.4854
preprocessing = A_C + A_S + DEV + PRE / C = 2^60.00141
```

Every count in this block is produced by `ledger()` of `experiments/lowm.py` from the executable routines (stage prices asserted by the plane programs; the scalar items as listed in Section 9), and Appendix B reproduces N from the stage prices alone with integers and Fractions; the integer tightness of the fifth decimal is asserted in both directions.
Per first block the program spends 18.66 units (1 + 615/C + vbar/C); per good pair the data-dependent work is 55.4 operations. The one sensitivity a declared premise needs: with q3 one bit lower, 2^-71.16, the claim would be 60.84571; with the cell-event value q3_cell = 2^-71.47 (rows 22..36 by cells) it would be 60.99099; with the four patterns alone with cells, 2^-72.02 (R16x accepted in the program but not credited in q3), 61.28957; with the Table 15 value 2^-74.03 (neither relaxation accepted) 62.76763.

### 11.1 Exactness of the expectations

Each row is linear in a count whose expectation is exact: a class passes with probability p7 (Section 5.3), the number of runs of a passing class is 2^(|B| - j) with j = |I| Binomial(|B|, 1/2) (Section 8.1), a rep of a run is good with probability p6 (Lemma 5.1), a probed lane has exactly 32/256 survivors on average and a nonzero filter with probability exactly 1,521,152/2^24 (Section 6.2), and 2^21/2^32 row-16 hits (Lemma 5.1: u uniform).
One row is a bound on an expectation that is not exact: the number of groups E ceil(N / 4) <= (E N + 3) / 4 (the padding of the last group of a first block is charged at its worst case; the exact value is E N / 4 + E[(4 - N mod 4) mod 4] / 4 <= E N / 4 + 3/4).
It is below 0.2% of vbar.

### 11.2 The advice-construction allowances A_S and A_C (H4)

The 37-step characteristic with its two-bit conditions (ePrint 2026/1120, Tables 15 and 16) and the semi-free-start pair with its inner values S (Table 17) are published, and this package carries them (Section 3; `experiments/lowm.py` rebuilds and re-checks them). Publication does not make their construction free: collision-frontier-v5 requires "All construction/preprocessing and advice must be accounted for, including any search omitted from the submitted program", so the construction is charged. The characteristic search is charged A_C = 2^60 (the paper's search, whose time is unpublished; bounded by comparison with the measured complete re-run of the predecessor 35-step search accepted in 6eeefb64: 593,858 solver CPU-seconds, a calibrated price of 2^21.427 units per CPU-second; 2^60 units are 2^38.57 CPU-seconds, 688,000 times that re-run; 0db0eeb6 charges the same A_C), and the memory of that construction is in the bound of H6 (Appendix H.2). Everything derived from the characteristic and S (G, the classes, the lists, F6, F7, L*, the tables) is recomputed in the preprocessing (Section 14.2) or is the 222 class descriptors (below 2^13 bytes of advice).
Step 1 is charged A_S = 2^50 (the paper's Step-1 SAT solve is 2^41.3).
The procedure re-solves Step 1 (the stage-37 SAT formula s37_all.cnf, 124,043 variables, 731,652 clauses) with kissat 4.0.4, one thread, `--time=7200` and `prlimit --as=117440512` per seed, at most 2^13 seeds; if no seed returns a model, the published S is used. A_S = 2^50 bounds this phase by construction: 2^13 x 7200 CPU-seconds = 2^25.81 CPU-seconds, at the calibrated price of 6eeefb64 (2^21.427 units per CPU-second at C = 2644) 2^47.24 units, below 2^50. Measured: seeds 101 and 102 return verified models after 57:54 and 24:26 (Appendix H.2). Completing a Step-1 solution to a 37-step semi-free-start pair takes about 25 milliseconds (organizer experiment `a0-sfs-r37`) and is inside A_S.


## 12. Premises

**H1 (score-critical).** The first blocks M0 are fresh uniform 512-bit strings; their chaining values CV1 = F_37(IV, M0) behave as independent uniform 256-bit values; in particular x = A_{-1} is uniform on 2^32 and independent of cb = C6 - A_{-2}, which is uniform on 2^32. Consequences used: each of the 222 classes passes the W7 test with probability p7 = |F7|/2^32 exactly, each variant of a passing class then passes F6 with probability p6 = |F6|/2^32 exactly, and given both, W0..W5 are uniform and independent of (W6, W7) (proof.md Lemma 5.1); hence the expected number of good pairs per first block is g = 782,800 p7 p6 = 830.988, the expected counts of the ledger, and the independence of distinct first blocks.

*Scope.* The expected numbers of passing classes, good pairs, survivors and row-16 passes per first block; the expected operation count of the counted program; the law of the second-block words that defines q3; independence across first blocks (proof.md Section 10). Not the validity of any output: every output is verified with the target. *Evidence.* Measured by 7319bba with the attack's own filters on real first blocks in C (2^21 and 2^23 first blocks: passing classes 7,400,134 and 29,545,568 against 7,388,160 and 29,552,640 expected; good pairs ratio 1.0034 and 1.0011; row-16 pairs z = +0.88, +0.51), and by this filing's simulation of the counted program on 50,000 real first blocks (passing classes per first block 3.529 against the exact 3.523, good pairs 835.0 against 831.0, mean counted operations 46965 against the ledger's 46685). These are at most 2^23 real first blocks, not 2^58.3; the organizer experiment a0-online-r37 checks functional exactness only and is not evidence for H1. *Limitations.* A premise, not a theorem; tested on at most 2^23 first blocks. The class tests of one first block are strongly correlated (their c7 values are close), so per-first-block counts are overdispersed; only their expectations and the independence across first blocks are used. The class test uses the single word x, so H1 is also an assumption about that word of the digest of a 37-step compression.

**H2 (score-critical).** For a good pair, q3 = the average over the 782,800 variants of the 222 classes (each equally likely, as examined here) and the 32 elements of L* of Pr[rows 16..21 of both members follow every cell and every printed two-bit condition closing at rows 16..21 (corrected reading A15[29] = A17[29]), the eight value bits E18[1,5,10,11,18,28,29] and E19[29] of Table 15 not imposed, and (R16x) E16[23] = 0 and E16[24] = E17[24] not imposed, and rows 22..36 replayed on the raw schedule words end with the eight registers of the two members equal: exactly the checks of experiments/lowm.py step3b] satisfies q3_used = 2^-70.16 <= q3 <= 2^-70.06, where 2^-70.16 is the sum, rounded down to two decimals of log2, of the 99 percent lower bound 2^-71.4629 of q3_cell (the same event with the cells of rows 22..36 imposed; the lower bound of the two preregistered blocks of 128 replicates, NP = 8192, of a sequential Monte-Carlo estimator written for this filing, Appendices F and G) and the 99 percent lower bound 2.4786 of the ratio q3 / q3_cell (preregistered, 2 x 128 seeds, pooled ratio 2.4848; Section 7.4d, Appendix K), run on exactly this family with both relaxations as one carrier.

*Scope.* The expected number of successes E[X] = N_FB g 32 q3 and hence N_FB (proof.md Sections 7 and 10). The good pairs and the later rows are those of 7319bba; this filing changes how the good pairs are found, not which pairs are good, and which pairs count as a success: (from ffbe30bb) the value patterns of rows 18 and 19 and (new) R16x at rows 16 and 17, which also gives the four l = 0, 2, 16, 18 row-16 values. *Evidence.* Lemma 7.1: rows 16..22 have exactly the same probability for every variant; a variant enters rows >= 23 only through W8 in W23 and W24, so only the four W24 conditions can depend on it (about 2^-4 for every W8x). Our estimator (exact row 16, exact importance weights at rows 17..21, (W6, W7) uniform on F6 x F7, W8 drawn uniformly from the 782,800 variants; Appendix F) was preregistered (validation V with Table 15 cells: mean 2^-73.9911, bound 2^-74.0064, z = +0.66 against the registered study B of 7319bba, mean 2^-73.9987, bound 2^-74.0225, validation PASSES both preregistered criteria (|z| <= 2.576; bound within 0.04 of -74.0225); main blocks R1 and R2 with the eight value characters of the two E cells removed: means 2^-71.9975 and 2^-71.9868, relative sd 0.0714 and 0.0681, bounds 2^-72.0191 and 2^-72.0074, declared 2^-72.02; stage factors of rows 18, 19 and 21 -8.00, -10.00 and -2.00 bits against -15.00, -6.00 and -1.00 for Table 15, structural gain 2.00) and again with R16x (constants written from the counted program; the same binary reproduces the four-pattern outputs byte for byte; joint blocks J1 and J2: means 2^-71.4296 and 2^-71.4177, relative sd 0.1096 and 0.1143, bounds 2^-71.4629 and 2^-71.4524, 0.55 bits above the four patterns alone; our earlier full-path test of R16x with independent rehash of all 30,814 collisions gave +0.590 bit [0.548, 0.631]). The four-pattern relaxation (exactly four feasible patterns, three verified further collisions) is ffbe30bb's; here the three collisions are re-checked against this package's cells. R16x is ours (each of its two conditions alone is necessary; a sweep of 30 further condition pairs found no further gain). Here the examined law is the studied law (every variant of every passing class, no weighting), so no hedge is added. The exact event adds the ratio of Section 7.4d (+1.31 bit): the ratio is measured on the same proposals as the cell event, in 256 preregistered seeds (cell_not_exact = 0). With q3 one bit lower the claim would be 60.84571, with the cell-event value 2^-71.47 60.99099, with the four patterns alone with cells (2^-72.02) 61.28957 and with the Table 15 value 2^-74.03 62.76763. The two bounds of the product come from different runs (coverage at least 98 percent by the union bound). *Limitations.* A Monte-Carlo bound, not a theorem; its coverage rests on the approximate normality of the mean of 128 replicates (relative sd 0.1096 and 0.1143, about twice the Table 15 study's because few children survive the row-19 stage); row-22 survivors are heavily duplicated within a replicate; the row-22 stage draws (W6, W7) uniformly from F6 x F7, which is argued, not measured; the ratio was measured with W8 drawn from the family G of 12,103,680 variants and checked on the 782,800 variants of this filing (Section 7.4d); depends on the reading of the '+' cells. The estimator is ours and was validated against the registered study, not against a second independent implementation. The count of four patterns is a solver enumeration (Bitwuzla; Z3 on smaller cases) for the published dense part with the signed cells of rows 14 and 15 kept (with rows 12..15 removed as well it admits 128 patterns); other dense parts were not explored, and our estimator does not use the solver. R16x has no solver enumeration: its value rests on the estimator and on our full-path test with rehashed collisions; patterns of rows 16..21 outside the program's cells (for example the E18 XOR pattern {24,23,16,15}) are not counted. No organizer experiment estimates q3. A stated premise, not an established fact.

**H3 (score-critical).** For every trial t = (first block, variant, l), the expected number of other successful trials of the same first block given that t succeeds is at most 2^-9.4: E[X_f - 1 | A_t] <= 2^-9.4. Equivalently: (a) the expected number of other l in L* succeeding with the same variant is at most 2^-11, and (b) for other good pairs t' of the same first block, Pr[t' succeeds | t succeeds, t' good] <= 2^35 Pr[t' succeeds | t' good].

*Scope.* The per-first-block Bonferroni bound Pr[X_f >= 1] >= (1 - 2^-10.4) E[X_f] (proof.md Section 10). The good pairs of a first block and their dependence structure are those of 7319bba; this filing changes the order in which they are processed, not the set. *Evidence.* (a) 7319bba's replay of 19,620,436 distinct Step-3 successes of the SMC: rebuilding W0..W5 and testing the other 31 elements of L* through rows 14..36 gave 0 further successes (rule-of-three 95 percent bound 2^-22.65 per success; the accepted patterns raise the chance of passing rows 18 and 19 by about 4 and R16x the chance of the whole path by about 1.6, with four more l holding row 16, so about 2^-19.8, far below 2^-11; in that replay the other l fail at row 16 or 17). (b) With q3 <= 2^-70.06 (H2, the exact event; Appendix H.4), the expected number of further successes among other good pairs is at most rho x N_good x 32 x q3 with N_good <= 782,800 (all variants of the family): 2^35 x 2^19.58 x 2^5 x 2^-70.06 = 2^-10.48, so delta <= 2^-11 + 2^-10.48 = 2^-9.71 < 2^-9.4; the measured factor at the row-16 level over 2^21 and 2^23 real first blocks is 0.98 and 1.00. This is the bound of the earlier filings on this family; the whole family G would give 2^-6.5 and is not used. *Limitations.* Rows >= 17 of distinct good pairs cannot be measured jointly within one first block; the premise leaves a margin of 2^35 over the measured row-16 factor, and the margin over the number of examined pairs is thin (delta <= 2^-9.71 against 2^-9.4). The replay samples are correlated through SMC resampling. A stated premise, not an established fact.

**H4 (supporting).** The published characteristic, its two-bit conditions, the SFS pair's inner values S and L* are used as advice, and their construction is charged (Section 11.2). A_S = 2^50 (the Step-1 SAT solve, reported by the paper at 2^41.3, and the completion of a Step-1 solution to the SFS pair) and A_C = 2^60 (the characteristic search of the paper, whose time is unpublished); all development computation at DEV = 2^40. The variant family, the 222 class descriptors (below 2^13 bytes), the lists, the filter sets, L* and the tables are recomputed in the preprocessing (2^38 operations bound, itemised in proof.md Section 14.2).

*Scope.* The preprocessing part of the ledger (2^60.00141) and the advice (below 2^13 bytes). *Evidence.* proof.md Section 11.2 and Appendix H.3. A_S: 2^8.7 times the paper's reported Step-1 cost; the completion of a Step-1 solution to a full 37-step semi-free-start pair is reproduced in this package in about 25 milliseconds per pair (organizer experiment a0-sfs-r37). A_C: at the CPU-second price calibrated in the accepted filing 6eeefb64 (2^21.427 units at C = 2644 per solver CPU-second), 2^60 units is 2^38.57 CPU-seconds, 688,000 times the 593,858 CPU-seconds that filing charged as a measured complete re-run of the predecessor 35-step search; 0db0eeb6 charges the same A_C. *Limitations.* The 37-step characteristic search time is unpublished and we did not complete a re-run of it: our attempt on the dense instance of the 37-step model (kissat, three seeds, 2^22 conflicts each, 66 to 99 single-thread minutes per seed) did not solve it, so it gives no bound (Appendix H.3). A_C is a bound by comparison with the accepted measurement of the predecessor search, not a measurement of this one; that the authors' search was no cheaper is a premise. With A_C = 2^56 the claim would be 58.88745.

**H5 (score-critical).** Under collision-frontier-v5 a word-RAM program of 256-bit primitives in which every executed load, store, logic operation, shift, addition, comparison, branch and jump is one primitive is charged by the primitives it executes. The W7 class test (166 primitives for all 222 classes) and the W6 test of a batch of 256 reps (404 to 431 primitives, and 88 to 95 for each subtraction run) are straight-line plane programs whose counts do not depend on the data, produced by a plane algebra in which static constants fold and complemented planes carry an inversion flag at no cost, and in which a NOT is paid when an AND or OR meets unequal flags; two batches are processed together bit by bit with at most 20 live planes each (64 registers, no spill). The group of four members is 31 primitives, the probe of a lane 11 or 12, the exact row-16 test 34, with the scalar and control items of proof.md Section 9. All tables, the code (bounded by 2^16 bytes) and the constants occupy 607,744 bytes = 2^19.21, below 2^20 bytes. The 222 classes are base | s for s in ten lists (computed, checked for all 782,800 variants); a list is the union of 2^|B| translates of its reps by the cube B of free bits {0, 2, 3} or {0}, and W6x does not depend on a cube bit s_b when q_b = 1 (Lemma 8.2: proved from the constants of S and checked), which the program uses to run only the main combination and subtract the constants of the other 2^|Q0| - 1 combinations that matter.

*Scope.* The class-test, W6, scan, gather, group, probe and survivor terms of the ledger (essentially all of the 46070.09 data-dependent operations per first block), the fixed terms, the memory figure and the preprocessing bound (2^38 operations). *Evidence.* The program is experiments/lowm.py (the plane programs assert their counts at every execution; process_cv counts every scalar item where it executes; the realized operation count of every category equals its closed formula on 50,000 simulated first blocks). It is exact against the scalar definitions: every lane of every class-test plane and every pass plane equals the F7 or F6 test of its definition (44,400 and 42,972 lanes in selftest, and every lane of every processed class in a0-online-r37), the sets of good pairs (all members, after the expansion of the reps) equal the brute-force sets, the address u equals W0 + s0(W1) from the step equations, the exact row-16 test equals the exhaustive enumeration of 2,097,152 pairs on all 32 l under the row-16 parity relaxation (Appendix A) and the generic row check on random and near-miss values, and the table stage never rejects a member. *Limitations.* No organizer ruling is cited for the plane algebra (static constants and inversion flags are compile-time facts of the text; the W6 programs have 81 to 82 inversion flips that cost nothing because XORs absorb them and AND/OR of equally flagged planes use De Morgan; pricing every one of them as a NOT would give about 58.7198) or for the register argument, which is a count of live planes, not a register allocation. The code size is a bound (at most 8192 primitives of at most 8 bytes). Branch pricing follows the earlier filings (a branch on a register is one primitive). The ceiling of the group count and the survivor scan are charged at their worst case (below 0.2 percent of the data-dependent work).

**H6 (score-critical).** ASSUMPTION (a declared bound, enforced by an address-space cap): the peak memory of the whole procedure, the online program, the construction of the characteristic (the generation of the SAT instance of the 37-step dense model, its CNF dump and the solver search, charged as A_C), the Step-1 solve and its completion, development and the preprocessing, is at most 2^29 = 536,870,912 bytes, so memory_log2_bytes = 29 and the score is time_log2 + 9. The online tables, code and constants take 607,744 bytes = 2^19.21.

*Scope.* The memory term of the score; the time ledger is unchanged. *Evidence.* Measured peaks (resident set, one thread, our machine, not run by the organizer; Appendix H.2): generator gen37.py 98,352 KB, translation to SMT2 97,360 KB, STP 2.4.1 CNF dump (200,534 variables, 954,732 clauses) 487,680 KB = 499,384,320 bytes (2^28.895), each of these three run under `prlimit --as=536870912` and reproducing byte for byte the earlier outputs (sha256 of the CNF 445a880e...42f4); kissat 4.0.3 on that CNF under an address-space cap of 2^28: zero-conflict peak 157,622,272 bytes (2^27.232) and, in three seeds run to 2^22 conflicts, an address-space peak of at most 2^27.790; the Step-1 solve and the other stand-ins at most 2^27.569; online 607,744 bytes. *Limitations.* A declared bound, not a theorem. We did not complete the paper's search: 2^22 conflicts did not solve the dense instance, and the memory beyond that point is unmeasured (from 2^21 to 2^22 conflicts the address-space peak of one seed rose by 0.205 bit, against 0.210 bit of headroom under 2^28; the bound here is 2^29, one bit higher). The cap ends any run that would exceed it, and then the construction fails. The STP dump alone needs 2^28.895 bytes, so a bound of 2^28 would not hold.

**H7 (supporting).** The cap target is mu0 = 0.49694499, the smallest 8-decimal number strictly above -ln(0.61 - Pcap - 2^-60) / (1 - 2^-10.4) with Pcap = 0.00138975 the assumed bound of the Chebyshev work-cap failure probability. With E[X] >= mu0 the success bound of proof.md Section 10, 1 - exp(-(1 - 2^-10.4) mu0) - Pcap - 2^-60, is >= 0.39000000 with no further padding.

*Scope.* N_FB (the cap) in the ledger. *Evidence.* Every allowance is an explicit term of the floor equation: the Chebyshev cap-failure bound Pcap (priced in proof.md Section 10 from the exact vmax_fb and vbar of the ledger; the computed bound is 2^-9.49), the repeated-first-block allowance 2^-60, and the H3 dependence discount as the divisor (1 - 2^-10.4). Appendix C computes mu0 and the bound with 60-digit decimals and asserts the bound > 0.39; lowm.py ledger() iterates Pcap and N_FB to a fixed point and asserts the same. *Limitations.* The 0.39 floor is the organizer's success requirement; the equation makes the success arithmetic exact rather than adding slack.


## 13. Evidence and runs

All runs for this filing on one Windows PC (24 threads) and its WSL Ubuntu: Python standard library (`experiments/lowm.py`), numpy and gcc for Appendix A. At most two processes ran at a time. The programs and numbers that are used as premises (7319bba, fb039a6e, ffbe30bb) are labelled as such; the q3 studies of Section 7.4b were run for this filing with `q3smc.c` (Appendix F, at most two processes at a time).

### 13.1 Quoted from 7319bba (end to end on real first blocks; inherited evidence for H1, H3, H2)

C statistics of 7319bba (random M0 from xoshiro256**, CV1 = F_37(IV, M0), the 222 W7 tests of the 222-class family, the scalar W6 test of every variant of every passing class, u and the exact row-16 test for every l, exact checks of sampled pairs):

| run | first blocks | passing classes (expected) | good pairs (expected; ratio) | row-16 pairs (expected; z) | H3 factor: sum R(R-1) / p^2 sum G(G-1), p = 1052672/2^32 |
|---|---|---|---|---|---|
| seed 5eed0021 | 2^21 | 7,400,134 (7,388,160) | 1,748,648,111 (1,742,708,500; 1.00341) | 424,363 (422,895; +0.88) | 0.981 |
| seed 5eed0023 | 2^23 | 29,545,568 (29,552,640) | 6,978,649,557 (6,970,834,000; 1.00112) | 1,693,297 (1,691,580; +0.51) | 0.979 |

The counts are strongly overdispersed (variance-to-mean ratios 28.8 for passing classes, about 23,100 for good pairs, 6.6 for row-16 pairs) because classes are correlated; their means match. 7319bba's replay of 19,620,436 distinct Step-3 successes of the SMC found 0 co-successes across the other 31 elements of L*.
These programs are not re-run here; the family and the filters of this filing are theirs.

### 13.2 Exhaustive checks and equivalence with the definitions (this filing)

- **F6, F7 and G (inherited).** For all 2^32 words w the definitions of F6 and F7 against their bitwise forms, |F6| = 287,309,824 and |F7| = 68,157,440, 0 mismatches (0db0eeb6, Tungsten; the bitwise forms are those used by the plane programs here, which `selftest` and the experiments compare with the definitions on the lanes below); |G| = 12,103,680.
- **The classes and the lists (`selftest`).** For all 222 classes and all 782,800 variants: the variant base | s is in G, has the class's c7, and the class has its size; 0 mismatches. Maximum S0(a0) over the variants 0xffffbb5c (lane safety of the packed words).
- **The cube (`selftest`).** For 8 classes spread over the lists, 60 random (x, cb) each and 8 random reps each: W6x(rep xor f) = W6x(rep xor (f & Q0)) for all f subset of the cube B (Lemma 8.2): 27,840 tuples, 0 mismatches; all classes of the lists with bit 2 or 3 in the cube have base bit 1 set.
- **The plane programs (`selftest`).** The W6 program on 42,972 lanes (8 classes spread over the ten lists, 3 random (x, cb) each, every batch and every cube combination): 1,531 F6 passes, 0 mismatches against F6(w6of(a0, x, A_{-2})) of the member rep xor f. The class test on 44,400 lanes (200 values of x, half of them constructed to pass a class): 0 mismatches against F7(c7 - x).
- **Row 16 (`selftest`, Appendix A).** The exact test of Lemma 6.2 equals the exhaustive enumeration of `r16.c` on all 32 l (2,097,152 pairs, none missing, none added) and rejects all 1,046,639 non-members among 2^20 random (u, l); filt(u) contains every l of every enumerated pair, and its sums over the 2^24 values of u mod 2^24 are the exact means of the ledger; against the generic row check (`row16_ok`) on random values, on near-miss values (the fixed bits of E16x imposed) and on single-bit changes of members: 0 mismatches; filt(u) contains every l with a row-16 pass.
- **Packed address.** The 4-lane U against the definition u = W0 + s0(W1) of the chaining value and a0 (400 lanes, extreme chaining-value words): 0 mismatches.
- **Unrestricted run of the experiment checks.** The checks of `a0-online-r37` (every lane of the class-test and pass planes, the good sets against brute force, the addresses, the table stage and the exact test against the row-16 definition, the cells of rows -4..15) on 526 first blocks with a passing class (3,565 seed-drawn), **all passing classes** of each processed (12,286 classes, 2,847,103 good pairs, 711,784 groups, 356,960 survivors of the table stage, 1,383 row-16 passes): 0 mismatches of every kind.
- **Organizer experiments (local replay of the request format with seeds `seed<t>`; inside the organizer's 20 s and 128 MiB).**
  `a0-sfs-r37`: trial t imposes pattern t mod 8 (0..3: the four value patterns of rows 18 and 19 with E16[23] = 0; 4..7: the four R16x patterns with E16[23] = 1); 124 of the first 128 trials build a 37-step semi-free-start collision with a variant dense part (patterns 0 to 7: 16/16/15/16/16/15/15/15; the others exhaust their proposal budget); for trials 0..15 the constructed chaining value is fed to the counted online program restricted to the class of a0, which finds exactly the constructed pair in **16 of 16** cases (class test, W6 test, gather, packed address, probe, exact test, rows 16..36); 3.4 s.
  `a0-online-r37` (trials 0..7): 43 first blocks drawn, 24 classes processed, 11884 good pairs, 2971 groups, 1490 survivors of the table stage, 6 row-16 passes; class-lane, pass-lane, good-set, address, row-16 and cell mismatches: 0, 0, 0, 0, 0, 0 (pairs checked against every cell of rows -4..15 for all 32 elements of L*: 12); 0.8 s.

### 13.3 The counted program simulated on real first blocks (premises H1, H5)

`experiments/lowm.py`'s `process_cv` was run on 50,000 real first blocks (first words from SHAKE-256 of the seed `valI, valJ`, real 37-step compressions, all 222 classes, every operation counted), without any restriction of the family.
Realized counts: 176,467 passing classes (3.529 per first block against the exact 3.523), 41,748,140 good pairs (835.0 per first block against the exact 831.0), 10,437,035 groups, 5,216,590 survivors, 19,827 first-block-level row-16 passes (4.749e-04 per good pair against the exact 4.790e-04 = 2,057,184 / 2^32, the number of distinct u among the 2,097,152 pairs of Appendix A; the ledger charges the rare path per pair (u, l), 2^21 / 2^32 = 4.883e-04).
The counted operations per first block (the 46 first-block operations included): mean 46965, standard error 879 (1.9%) (the counts are bursty: standard deviation across first blocks 4.2 times the mean), against the ledger's expectation 46685 (= FIXED + vbar).
The realized operations of every category (class test, scalars, class preparation, sweeps, W6 programs, scans, members, groups, probes, survivors, rare path) equal the closed formulas of Section 9 evaluated on the realized counts: **0 difference in every category** (`experiments/lowm.py` is the program; the check is the identity of Section 9's prices with the executed counts).

### 13.4 Development computation

Below 3,000 CPU-seconds in all (the exhaustive row-16 comparison 20 CPU-seconds in C and 60 in numpy, the simulation about 267 CPU-seconds, selftests and experiment replays under 300, aborted runs the rest), far inside DEV = 2^40 units (2^18.6 CPU-seconds at the calibrated 2^21.4 units per CPU-second).


## 14. Memory, preprocessing and advice

### 14.1 Memory

Everything resident during the online phase (`python3 experiments/lowm.py memory`; words of 32 bytes):

| item | bytes |
|---|---|
| planes of the reps: 8 batches x 14 planes and 42 batches x 16 planes | 25,088 |
| packed entries of the reps: 50 batches x 64 words | 102,400 |
| cube entries D[c]: 8 words | 256 |
| spill area of the sums of a class's batches: 7 x 32 words | 7,168 |
| c7 planes: 32 words | 1,024 |
| chunk table LO: 4096 words | 131,072 |
| chunk table MID: 4096 words | 131,072 |
| lane-scan table: 2048 words | 65,536 |
| class descriptors: 222 x 4 words (base, BP, list data, c7) | 28,416 |
| per-l constants: 32 x 4 words (C_l, cxA_l, E15x word, VA_l) | 4,096 |
| scalar planes in memory: 96 words | 3,072 |
| characteristic cells, L* rows, S: bound 1280 words | 40,960 |
| chaining-value constants (cv_pre) and the first-block buffer: 64 words | 2,048 |
| code (bound: at most 8192 primitives of at most 8 bytes) | 65,536 |
| **total** | **607,744 = 2^19.21** |

The online limit 2^20 = 1,048,576 bytes is not reached: online memory 2^19.3 bytes (rounded up). The claimed memory is 2^29 bytes, the declared bound H6 over all phases including the construction of the characteristic (Appendix H.2): the generator, the STP dump and the solver phases run under an address-space cap of 2^29 bytes (the Step-1 re-solve under 117,440,512) and every other phase is computed below it. The messages (128 bytes), the registers (64 x 32 bytes) and the compression state are included in the last constants. Nonuniform advice: the characteristic, S, L* and the 222 class descriptors (222 x 12 bytes), below 2^13 bytes.
The tables are built in the preprocessing and are never held twice. Preprocessing memory (measured by us on our server, single thread, not run by the organizer; stand-ins for the Step-1 solve of A_S, on the stage-37 SAT formulas of the llw24 model: s37_all, s37b_all, s37c_all with 124,043 variables and 731,652 to 731,653 clauses, and the loose variants with 68,811 variables): Kissat solved every formula (SAT, 36.6 s to 16 min 48 s) with a peak of 38,136 to 73,632 KB; CaDiCaL peaked at up to 194,344 KB (the three full formulas stopped at their 3600 s cap without a result; the loose ones solved at 78,912 and 84,844 KB). The largest of these, 194,344 KB = 199,008,256 bytes = 2^27.568 (2^27.569 rounded up), lies below 2^28: these phases peak at most 2^28 = 268,435,456 bytes; with the construction of the characteristic (A_C; its measured peaks in H6 and Appendix H.2) the bound over all phases is 2^29 = 536,870,912 bytes: peak = max(online 607,744 bytes, preprocessing phases, construction of the characteristic) <= 2^29 (Appendix H.2).

### 14.2 Preprocessing: PRE < 2^38 operations

(i) Discovery of the family: the 2^29 values of E4 with E4[31:29] = 000 (a0 = E4 - C4), each tested against the W8x conditions (about 20 operations) and c7 (about 60), grouped by c7 and the classes of at least 3456 variants kept: 2^29 x 80 + 12.1 x 10^6 x 100 < 2^36; the descriptors (base, mask) of the 222 classes are read off their members (782,800 x 30).
(ii) The ten lists: 10 x 2^15 subsets x about 80 operations < 2^25. (iii) The planes and packed entries: 142 batches x (17 x 256 bit insertions x 3 + 64 x 4 x 10) < 2^22. (iv) The tables LO and MID: 32 x (4096 x 10 + 2 x 4096 x 6) < 2^23, the per-l constants 28 x 200; the scan table 2048 x 6; the c7 planes 222 x 32 x 3.
The sum is below 2^36.1; PRE = 2^38 is charged. Nothing depends on cb or on any other word of the chaining value.

## 15. Limitations

- H1, H2, H3 are premises. q3 is estimated (Monte Carlo, by an estimator written for this filing and validated against the registered study of 7319bba, times a preregistered exact/cell ratio), not proved; no collision has been found and none is expected at the scale that can be run. The full-scale success probability cannot be observed.
- The counted program is a straight-line text whose plane programs are executed and counted by an algebra with static constants and inversion flags; the scalar and control items are counted by the constants of Section 9. There is no machine code; the register argument of Section 9.5 is a count of live planes.
- The simulation of Section 13.3 samples 50,000 first blocks of the 2^58.3 the run draws; the per-first-block counts are heavy-tailed (standard deviation 4.2 times the mean), so its mean has a standard error of 1.9%; the ledger does not use it.
- The organizer experiments run the same program on the whole family of 222 classes; to fit the sandbox a trial processes at most the first three passing classes of its first block.
- H3 (b) is measured at the row-16 level only (7319bba) and leaves a margin of 2^35 on rho; its bound on the number of examined good pairs is the whole family, and with the exact event its margin to 2^-9.4 is 0.31 bit (Appendix H.4).
- The characteristic and the SFS pair are published, but their construction is charged (Section 11.2): A_C is an allowance, not a measurement, and the memory of the construction is a declared bound (H4, H6, Appendix H.2 and H.3). The Step-1 re-solve runs under the caps of Section 11.2.
- For 37 steps the measured q3 for the Table 15 pattern is about one bit better than the 75 conditions stated in the paper's text; the paper's own tables give 74, which the SMC matches stage by stage. With the four patterns of rows 18 and 19 accepted the count is 72, in accordance with the structural 2 bits. With q3 one bit lower, 2^-71.16, time_log2 would be 60.84571.
- The count of four patterns is a solver enumeration for the published dense part (ffbe30bb); other dense parts were not explored. Our q3 estimator applies the program's own difference checks and does not use the solver.
- The simulation of the counted program (Section 13.3) was run again with this package's program after the R16x change (rows 16 and 17); its figures are from that run.


## Appendix A. Row 16: the exact test against the exhaustive enumeration

`r16.c` (7319bba; 0db0eeb6 Appendix A.5) with `r16data.h` generated from the cells of `experiments/lowm.py` (with R16x: eight fixed bits of E16), compiled with `gcc -O2` and run unchanged, prints `total pairs 2097152` (65,536 for each of the 32 l) and writes `r16.bin`, the pairs (u, l). Then, with numpy:

```python
import sys
import numpy as np
sys.path.insert(0, 'experiments'); import lowm as L
env = L.Env(); d = np.fromfile('r16.bin', dtype=np.uint32).reshape(-1, 2)      # the pairs (u, l) of r16.c
M, V = L.E16M, L.E16V
free = [b for b in range(32) if not (M >> b) & 1]
t = np.arange(1 << len(free), dtype=np.uint64); e = np.full(t.shape, V, dtype=np.uint64)
for i, b in enumerate(free): e |= ((t >> np.uint64(i)) & np.uint64(1)) << np.uint64(b)
e = e.astype(np.uint32); bit = lambda v, k: (v >> np.uint32(k)) & np.uint32(1); tot = 0
for l in L.FEASIBLE_L:                                  # the 2^24 values of E16x with the eight fixed bits, the cells of Lemma 6.2 applied to all of them
    c = env.LC[l]; a15 = np.uint32(c['Ax15']); A = e + np.uint32(c['cxA'])
    ok = ((e ^ np.uint32(c['Ex15'])) & np.uint32(0x10)) == 0
    ok &= bit(A, 29) == 1
    ok &= bit(A, 15) != bit(a15, 15)
    ok &= bit(A, 23) == bit(a15, 23); ok &= bit(A, 25) == bit(a15, 25)
    ok &= bit(A, 9) != bit(A, 20); ok &= bit(A, 18) != bit(A, 6); ok &= bit(A, 8) == bit(A, 17)
    us = set((e[ok] - np.uint32(c['C'])).tolist()); ref = set(d[d[:, 1] == l, 0].tolist())
    assert us == ref, l
    tot += len(us)
print('all %d per-l sets of u' % len(L.FEASIBLE_L) + ' equal the enumeration of r16.c; total', tot, 'pairs;', len(set(d[:, 0].tolist())), 'distinct u')
```

Output:

```text
all 32 per-l sets of u equal the enumeration of r16.c; total 2097152 pairs; 2057184 distinct u
```

## Appendix B. The exact ledger

Self-contained (integers and Fractions); the stage prices are the constants of Section 9, asserted by `lowm.py`. It reproduces `python3 experiments/lowm.py ledger`.

```python
from fractions import Fraction as Fr
# Exact ledger of the counted program (proof.md Sections 9-11). Integers and Fractions only.
C = 2644                                   # reference cost of one target compression, in word operations
# stage prices (primitives of the straight-line text, proof.md Section 9; the plane-program counts are measured by lowm.py and asserted at every execution)
W6_OPS = {(3, False): 404, (3, True): 415, (1, False): 420, (1, True): 431}                              # W6 program of a batch of reps by (cube bits k, all 32 sums needed)
SUBF = {(3, 1): 94, (3, 4): 89, (3, 5): 95, (3, 8): 88, (3, 9): 94, (3, 12): 89, (3, 13): 95, (1, 1): 94}                              # F6 of W - cu by (k, cu)
F7_OPS, SCAN_FIX, SCAN_LANE, CLS_LANE = 166, 70, 8, 6
EXTR, PLACE, GROUP_BODY, PAD_OPS, PROBE = (1, 2, 2, 1), 7, 31, 7, (11, 12, 12, 12)
SURV_FIX, SURV_LANE, EX_OPS, RARE_LOOKUP, RECOMP, ROWCHECK, ROWCOMP = 8, 7, 34, 2, 35, 53, 106
CPREP, CF_CLASS, SWEEP_OVH, FIXED, RUN_CU, SPILL = 410, 6, 195, 615, 7, 64
SP_LOADS = {3: 30, 1: 34}             # per batch: stored planes of the reps (14 or 16) with their address adds, two pointers
# the 222 classes: (variants, cube bits k, classes): lists 0, 1 / 2, 3, 4 / 5, 6 / 7, 8, 9 (proof.md Section 5.3)
CLASS_TYPES = [(3456, 3, 85), (3456, 1, 26), (3600, 3, 85), (3584, 1, 26)]
CUBE = {3: 13, 1: 1}                        # the cube bits {0, 2, 3} or {0} as a mask
NCLS = 222; NVAR = sum(n * c for n, k, c in CLASS_TYPES); NFEAS = 32
P7 = Fr(68157440, 1 << 32); P6 = Fr(287309824, 1 << 32); R16F = Fr(2097152, 1 << 32); MU = Fr(NFEAS, 256); PNZ = Fr(1521152, 1 << 24)
# fixed charges (Sections 11.2, 13.4, 14.2) and the success-floor constants
A_C, A_S, DEV, PRE, FIN = 1 << 60, 1 << 50, 1 << 40, 1 << 38, 1600
Q3 = Fr(1968180945272, 1 << 111)                 # q3 = 2^-70.16 rounded down to a 40-bit mantissa (2^40.84 / 2^111)
MU0 = Fr(49694499, 100000000)                   # smallest 8-decimal number above -ln(0.61 - PCAP_ASSUMED - 2^-60) / (1 - 2^-10.4)  (Appendix C)
SLACK = Fr(1, 4096); PCAP_ASSUMED = Fr(5559, 4000000)
def subsets(mask): return [s for s in range(16) if s & ~mask == 0]
def lane_costs(nls): return sum(SCAN_LANE + EXTR[L // 64] for nl in nls for L in range(nl))   # scan and extraction of every lane of the batches of reps
def memcost(j): return PLACE if j == 0 else 12 * (1 << j) - 2                                 # members of a rep with |I| = j
def class_det(n, k, Q0):
    # operations of a passing class with relevant cube bits Q0 that do not depend on which reps are good (2^|Q0| runs)
    nr = n >> k; nb = (nr + 255) // 256; nsw = (nb + 1) // 2; part = 1 if nr % 256 else 0; full = Q0 != 0
    tot = CPREP + CF_CLASS + nsw * SWEEP_OVH + nb * (SP_LOADS[k] + W6_OPS[(k, full)] + SCAN_FIX) + part
    if full:
        tot += 2 * nb * SPILL
        for cu in subsets(Q0):
            if cu: tot += nb * (RUN_CU + SUBF[(k, cu)] + SCAN_FIX) + part
    return tot
def class_run_cost(n, k, Q0):
    # scan, extraction and members of one run if all reps are good (times p6 for the expectation)
    nr = n >> k; nb = (nr + 255) // 256; nls = [min(256, nr - 256 * b) for b in range(nb)]
    return lane_costs(nls) + nr * memcost(k - bin(Q0).count('1'))
def class_expected(n, k):
    # Q0 is uniform among the submasks of the cube given that the class passes (x mod 16 is uniform)
    return sum(Fr(1, 1 << k) * (class_det(n, k, Q0) + (1 << bin(Q0).count('1')) * P6 * class_run_cost(n, k, Q0)) for Q0 in subsets(CUBE[k]))
def class_max(n, k):
    return max(class_det(n, k, Q0) + (1 << bin(Q0).count('1')) * class_run_cost(n, k, Q0) for Q0 in subsets(CUBE[k]))
perclass = pairs = Fr(0); vmax = Fr(0)
c3b_row = ROWCOMP + ROWCHECK + 1; c3b_pair = 201 + RECOMP + 1 + RARE_LOOKUP; c3b_l = 2 + 6 + 2 * c3b_row
for n, k, cnt in CLASS_TYPES:
    perclass += cnt * P7 * class_expected(n, k); pairs += cnt * P7 * P6 * n; vmax += cnt * class_max(n, k)
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
NFB = int(-(-MU0 // (g * 32 * Q3)))                     # first blocks: E[successes] = NFB g 32 q3 >= MU0
PCAP = vmax_fb / (SLACK * SLACK * NFB * vbar)           # Chebyshev bound of the work-cap overflow
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
A_C: characteristic search (units x C)    3,048,324,458,180,503,404,544
A_S: Step-1 solve (units x C)             2,976,879,353,691,897,856
DEV: development (units x C)              2,907,108,743,839,744
N_FB first-block compressions (units x C) 65,176,261,284,045,842,280
fixed operations: N_FB x FIXED            15,160,136,418,187,667,550
V_MAX: data-dependent operations          1,135,933,807,571,123,291,014
overshoot past the cap: vmax_fb           94,072,525,785
PRE: preprocessing                        274,877,906,944
FIN: final verification                   1,600
6 further compressions (units x C)        15,864
N_FB = 24650628322256370, g = 830.9881687164307, vbar = 46070.08522563445, Pcap = 0.0013897468279438338 <= 0.00138975
N = 4267574450285246393181
certificate: 2^6048539 * 2644^100000 <= N^100000 < 2^6048540 * 2644^100000
time_log2 = 60.48540
```

## Appendix C. The success floor

```python
from decimal import Decimal, getcontext
getcontext().prec = 60
PCAP = Decimal(5559) / Decimal(4000000)           # the assumed bound of the Chebyshev work-cap failure probability (Appendix B asserts the computed bound is below it)
EPS = Decimal(2) ** -60                          # a repeated first block among N_FB draws
D = 1 - Decimal(2) ** Decimal('-10.4')           # the H3 discount 1 - 2^-10.4
req = -(Decimal('0.61') - PCAP - EPS).ln() / D   # mu0 must exceed this
MU0 = Decimal(49694499) / Decimal(10 ** 8)
assert req < MU0 <= req + Decimal(2) / Decimal(10 ** 8)
succ = 1 - (-D * MU0).exp() - PCAP - EPS
print('required %.12f, mu0 %.8f, success bound %.12f' % (req, MU0, succ))
assert succ > Decimal('0.39')
print('OK')
```

Output:

```text
required 0.496944986716, mu0 0.49694499, success bound 0.390000001997
OK
```

## Appendix D. `selftest` output

```text
classes 222, variants 782800 (782,800), mismatches 0
W6_OPS (k, full): {(3, False): 404, (3, True): 415, (1, False): 420, (1, True): 431} SUBF_OPS: {(3, 1): 94, (3, 4): 89, (3, 5): 95, (3, 8): 88, (3, 9): 94, (3, 12): 89, (3, 13): 95, (1, 1): 94} F7_OPS 166 FIXED 615
F7 sampler violations 0
lists (size, cube bits): [(3456, 1), (3456, 3), (3584, 1), (3600, 3)]  classes with a cube bit 2 or 3 and base bit 1 clear: 0
invariance of W6x under the flips of the bits of I: 27840 checks, 0 mismatches
w6 plane lanes 42972, F6 passes 1531, mismatches 0
class-test lanes 44400, mismatches 0
row-16 checks: members seen 22, mismatches 0
packed u lanes 400, mismatches 0
max S0 over the 782,800 variants 0xffffbb5c True
```

## Appendix E. Credits

Authors of the work this filing builds on are named in Section 2 and in the dependency list. The paper: Y. Li, Z. Zhang, M. Li, F. Liu, H. Qian, J. Zhu. This filing: Jbenisek with Claude Sonnet 5.5 and Claude Opus 5.5 (Claude Code), which built, ran and checked the program and the q3 estimator `q3smc.c` and wrote this text; Grok (xAI) pointed to the memory-efficient mode of the paper as the lead; GPT Luna priced the memory trade of the table package that this filing replaces and, with Claude, built the verified 37-step solver model (Bitwuzla, Z3) behind ffbe30bb's enumeration of the four patterns, whose result this filing uses. ffbe30bb-ac92-4191-a589-3bf32661ee7d (Jbenisek): the four-pattern acceptance of rows 18 and 19, its enumeration and the three collisions of Section 7.6. None of the AI tools reviewed this filing; mistakes are ours.

## Appendix F. The q3 studies: program, preregistration, results

All files are in `q3/` of the working directory of this filing. The estimator `q3smc.c` was written for this filing from the description of Section 7.3; the constants it checks (cells of rows 0..36, the printed two-bit conditions closing at rows >= 16, rows 12..15 of the published pair for each l, the variant list) are generated by `gen_consts.py` from `experiments/lowm.py`, once with the Table 15 cells (`q3consts_orig.h`) and once with the two relaxed cell strings of rows 18 and 19 (`q3consts_relaxed.h`, sha256 f01e0c355afbb0aff8df6a06b2367cdd43644d3ad10af6c7470f2a44e535d47e, written from the program before the R16x change; regenerating from `experiments/lowm.py` as filed gives `q3consts_r16x.h` of Appendix G byte for byte; `q3consts_orig.h`, sha256 07aca8a40daf199c7d85cc28f97ec0d84c3976f6d751950f7b2cd0b3799ad8bd, comes from the program with the Table 15 cells, sha256 691563bedd682044a4e9f936ba98cddc8242d2cafa4a14cd4f7585f19a9be597). Build: `gcc -O2 -DCONSTS='"q3consts_relaxed.h"' q3smc.c -lm -o q3smc_relaxed`; run: `q3smc SEED 1 8192 512 16384` with `variants.bin` (782,800 little-endian 32-bit words, W8x of the variants, written by `gen_consts.py`) in the working directory; `-d` as the sixth argument prints the pattern histogram.

### F.1 Preregistration (written before any listed seed ran; stamp 2026-10-12T05:26:30Z, sha256 9187c4519d463838b90eefb4c0aa9df1eb12be95cf463076ad06511c7aaaaabf)

```text
preregistration: our own sequential-Monte-Carlo estimate of q3 for the 222-class A0-variant attack on 37-step SHA-256, with the original cells of rows 18 and 19 (validation) and with the four value patterns of rows 18 and 19 accepted
written before any listed seed was run; the stamp is the line below.
stamp: 2026-10-12T05:26:30Z
program: q3smc.c (written for this filing from the description of the estimator in the earlier proofs; it shares no code with any other participant's program and no other participant's code was compiled or run), sha256 2d8a406a5dd1ba0f3d6502b0e887d3b106a865a8970cce21d6c9ec5dcdd3ed71.
constants: q3consts_orig.h (sha256 07aca8a40daf199c7d85cc28f97ec0d84c3976f6d751950f7b2cd0b3799ad8bd) and q3consts_relaxed.h (sha256 f01e0c355afbb0aff8df6a06b2367cdd43644d3ad10af6c7470f2a44e535d47e), written by gen_consts.py (sha256 14ea0015f43b1ea86109ccc78e86cf392c12a9a34c7ece6a1c3babc1be6b4ae7) from this package's lowm.py (original cells: sha256 691563bedd682044a4e9f936ba98cddc8242d2cafa4a14cd4f7585f19a9be597; relaxed cells: the same file with exactly the two strings CHE[18] and CHE[19] changed, sha256 1e97095c79b1bcf50888c00cb908f31d99a059ccdfe08743c1f58b8822261756).
 the relaxed cells replace the eight characters of Table 15 that fix E18[1]=1, E18[5]=0, E18[10]=1, E18[11]=1, E18[18]=0, E18[28]=0, E18[29]=1 and E19[29]=1 by '=' and change nothing else: row 18 becomes =======uu=======n=====1====1====, row 19 becomes =======00====1==0==========1====.
variant list: variants.bin, the W8x = W8C - (a0 + C4) of the 782,800 variants of the 222 classes (all distinct), as listed by lowm.py (sha256 6900f64cec67217eb352fd43cd0552c92b2514b892481c95f761d19619d1e3c5).
estimator: stage 16 exact (count of the (l, E16x) pairs that pass row 16), stages 17..21 (E_t^x proposed uniformly with the fixed x-bits of the cell imposed, weight 2^-f), stage 22 ((W6, W7) uniform on F6 x F7), tail (variant uniform), uniform resampling of the survivors after each stage, product of the stage means. Parameters of every replicate: NP = 8192, M = 512, MT = 16384.
smoke runs, disclosed and not part of any study: seed 1 with each binary (original cells: stage 16 = 1,052,672 pairs, log2est -73.92417; relaxed cells: log2est -72.15193, patterns cd 1b f6 20 only). Seed 1 is not used below.
validation study V (original cells, binary q3smc_orig): seeds 710000..710063 (64 replicates). Computed: mean and sd of the linear estimates, one-sided 99% Student lower bound LB_V = mean - t(0.99, 63 df) sd / sqrt(64).
 V passes if both (a) the difference of the means from study B of the registered studies of the earlier filing (mean 2^-73.9987, relative sd 0.0378, 32 replicates) is at most 2.576 standard errors, z = (mean_V/mean_B - 1)/sqrt(relse_V^2 + relse_B^2), relse_B = 0.0378/sqrt(32), and (b) log2 LB_V is within 0.04 of log2 of study B's bound (-74.0225). It is the check that this program reproduces R37M's own q3 = 2^-74.03 (which is that study's floor). If V fails, no q3 is declared from this program and the failure is reported.
main study (relaxed cells, binary q3smc_relaxed), two independent blocks of the same design: R1 seeds 720000..720127 (128 replicates), R2 seeds 721000..721127 (128 replicates). For each block the one-sided 99% Student lower bound LB = mean - t(0.99, 127 df) sd / sqrt(128).
rule (fixed in advance): declared q3 = 2^x with x = floor(100 x log2(min(LB_R1, LB_R2))) / 100 (the lowest 99% bound, rounded down to two decimals of log2, never up). It is used only if V passes.
every listed seed is run and reported; none is dropped, replaced or rerun whatever the result; a crashed run would be re-run with the same seed only if the crash is not a property of the program.
the E18/E19 pattern diagnostic (the program's -d option: a histogram of the eight value bits of the 8192 particles that survived rows 16..22; seeds 730001..730003 with the relaxed binary) is a description, not part of the bound.
at most 2 processes at once.
```

In the preregistration the name of the table-free program with Table 15's cells is a working label: it denotes the program of this filing before its two cell strings were relaxed (its q3 is 2^-74.03).

### F.2 Results

Rule applied: V passes (validation PASSES both preregistered criteria (|z| <= 2.576; bound within 0.04 of -74.0225)); lowest bound 2^-72.01914 of R1 (2^-72.0191) and R2 (2^-72.0074), rounded down to two decimals: **2^-72.02** for the four patterns alone (the q3 used is that of the joint study, Appendix G). pooled 256 replicates: mean 2^-71.9922, relative sd 0.0697, bound 2^-72.0070 (descriptive).

Stage means of validation V (log2): 16: -16.994, 17: -13.000, 18: -14.999, 19: -6.000, 20: -7.000, 21: -1.000, 22: -10.999, tail -4.000. Stage means of the main study (256 replicates): 16: -16.994, 17: -13.000, 18: -8.000, 19: -10.000, 20: -7.000, 21: -1.999, 22: -11.002, tail -4.000.

All 64 log2 estimates of V (seeds 710000..710063, in order):

```text
-74.063 -74.004 -73.897 -73.950 -73.943 -73.949 -73.953 -74.009 -73.999 -73.922 -73.999 -74.094 -74.063 -73.986 -73.858 -73.956
-73.960 -73.996 -74.025 -74.057 -74.062 -73.921 -73.993 -73.984 -73.983 -74.134 -73.978 -74.022 -74.019 -73.999 -74.065 -74.063
-73.999 -74.036 -73.963 -73.994 -73.938 -73.952 -73.989 -73.988 -73.963 -73.959 -74.039 -73.954 -73.985 -74.047 -73.991 -74.030
-73.988 -73.939 -73.894 -73.966 -73.992 -74.075 -74.029 -74.008 -73.908 -73.999 -74.034 -74.020 -73.981 -73.933 -73.994 -73.996
```

All 128 log2 estimates of R1 (seeds 720000..720127):

```text
-71.892 -71.944 -72.050 -71.918 -72.020 -71.794 -71.924 -71.947 -71.930 -71.844 -71.948 -72.018 -71.983 -71.888 -72.062 -72.014
-71.845 -71.868 -71.917 -71.880 -72.099 -72.098 -71.860 -71.864 -71.866 -71.856 -71.856 -71.986 -71.910 -72.264 -71.890 -71.884
-71.987 -72.094 -72.039 -71.985 -71.993 -72.095 -72.131 -72.097 -71.835 -71.979 -72.078 -71.934 -72.183 -72.184 -72.152 -72.120
-72.085 -72.179 -71.943 -71.983 -72.224 -72.060 -71.925 -72.056 -72.117 -71.959 -72.173 -72.014 -72.072 -72.081 -71.941 -72.040
-71.851 -71.869 -71.984 -71.946 -71.896 -71.943 -71.946 -72.069 -72.136 -72.148 -71.941 -71.791 -72.037 -71.991 -72.161 -72.098
-72.001 -71.960 -72.059 -71.952 -71.983 -71.950 -72.094 -71.984 -72.072 -72.169 -72.059 -71.980 -72.112 -72.092 -72.080 -72.096
-71.943 -71.835 -72.091 -72.030 -72.102 -72.141 -72.070 -71.964 -71.931 -71.969 -72.065 -71.968 -71.724 -72.060 -71.944 -72.016
-71.991 -72.174 -71.944 -72.042 -72.142 -71.879 -71.869 -72.077 -72.053 -71.930 -71.931 -71.899 -72.064 -72.090 -71.962 -71.942
```

All 128 log2 estimates of R2 (seeds 721000..721127):

```text
-71.950 -71.834 -71.974 -72.061 -71.941 -71.976 -72.030 -71.860 -72.142 -71.898 -72.028 -72.001 -71.844 -72.084 -72.126 -71.734
-72.022 -72.019 -71.880 -72.057 -71.895 -72.199 -71.972 -72.114 -72.038 -71.954 -71.925 -71.971 -71.889 -71.994 -72.068 -72.085
-72.027 -72.045 -72.085 -71.912 -71.961 -71.938 -71.804 -71.990 -72.004 -71.809 -72.012 -71.946 -72.095 -71.858 -72.005 -72.135
-71.939 -71.929 -72.040 -71.788 -72.115 -71.817 -71.852 -72.081 -72.008 -71.944 -72.106 -72.106 -72.006 -72.063 -71.939 -72.049
-71.938 -71.944 -71.957 -72.060 -72.037 -72.057 -71.976 -71.867 -72.133 -72.138 -72.209 -72.061 -71.971 -72.070 -72.010 -72.137
-72.071 -72.021 -71.995 -72.101 -71.979 -71.945 -72.017 -71.927 -71.948 -72.009 -71.920 -72.024 -71.821 -72.015 -71.907 -71.991
-71.851 -72.090 -71.927 -72.042 -72.000 -71.886 -71.919 -71.811 -71.834 -71.950 -72.090 -71.976 -72.007 -72.271 -71.961 -71.929
-71.980 -71.958 -71.977 -72.014 -72.082 -71.977 -72.188 -71.965 -72.106 -72.115 -71.907 -71.954 -71.946 -71.866 -71.795 -72.136
```

The program's own output for the first seed of each block:

```text
--- seed 710000 ---
RESULT seed 710000 NP 8192 M 512 MT 16384 log2est -74.06303 est 5.0676630297e-23
STAGES -16.99438 -12.99553 -15.03271 -6.00000 -6.99930 -1.00000 -11.05236 tail -3.98874  (row-24 survivors 8454312 of 134217728, full passes 8454312)
--- seed 720000 ---
RESULT seed 720000 NP 8192 M 512 MT 16384 log2est -71.89162 est 2.2827903663e-22
STAGES -16.99438 -13.00028 -7.99856 -9.93391 -6.99967 -1.98006 -10.98319 tail -4.00157  (row-24 survivors 8379473 of 134217728, full passes 8379473)
--- seed 721000 ---
RESULT seed 721000 NP 8192 M 512 MT 16384 log2est -71.94963 est 2.1928148179e-22
STAGES -16.99438 -12.99632 -8.00176 -9.98877 -7.00009 -2.00954 -10.97902 tail -3.97975  (row-24 survivors 8507175 of 134217728, full passes 8507175)
```

Pattern diagnostic (relaxed binary, `-d`, seeds 730001..730003; bit string E18[1,5,10,11,18,28,29] as bits 0..6 and E19[29] as bit 7, hexadecimal; Table 15 is cd, the others 1b, f6, 20): seed 730001: 1b:2349 20:1607 cd:2461 f6:1775; seed 730002: 1b:1710 20:2180 cd:2145 f6:2157; seed 730003: 1b:1714 20:1891 cd:2040 f6:2547.

Interim looks: the analysis script was run on the partial outputs while the blocks were running, to monitor progress; no seed, parameter or rule was changed after any look.

### F.3 The check of the three alternative collisions (`check_alt.py` as run)

```text
pair (x = M', y = M)         collides  cells of this lowm.py    cells of Table 15       
Table 15 (published pair)    True      True                     True                    
G1                           True      True                     False                   
G2                           True      True                     False                   
G1 xor G2                    True      True                     False
```

### F.4 `q3smc.c`

```c
/* q3smc.c - importance-weighted sequential Monte Carlo estimate of q3 for the A0-variant attack on 37-step SHA-256 (rows 16..36), written for this filing
   from the description of the estimator in the proofs of the earlier filings; it shares no code with theirs.
   q3 = (1/32) sum_l Pr[rows 16..36 of both members follow every cell and every printed two-bit condition closing at rows >= 16 | (variant, l, good pair)].
   Stage 16: exact (all E16x with the fixed x-bits of the E16 cell that pass row 16, for each l; the initial particles are drawn uniformly from these (l, E16x) pairs).
   Stages 17..21: each child proposes E_t^x uniformly with the fixed x-bits of the row's E cell imposed (weight 2^-f), W_t^x = E_t^x - (rest of step t), W_t^y = W_t^x + the exact difference
   given by the schedule, and the whole row is checked (cells of A, E, W for both members, '+' equalities, printed two-bit conditions).
   Stage 22: (W6, W7) drawn uniformly from F6 x F7 (W7 from the affine decomposition, W6 by rejection), W22 from the schedule, row 22 checked.
   Tail: a variant (W8x) drawn uniformly from the variant list; rows 23..36 for both members, all cells and conditions checked (row 24's W cell and relations first, which is exact: it is a part of the check).
   After each of the stages 17..22 the survivors are resampled uniformly (all survivors of a stage have the same weight) to NP particles; the product of the stage means is unbiased for q3.
   usage: q3smc seed0 nrep NP M MT [-d]    (variants.bin in the working directory)
   build: gcc -O2 -DCONSTS='"q3consts_orig.h"' q3smc.c -lm -o q3smc_orig   (or q3consts_relaxed.h, q3consts_r16x.h)
   the TAG line (added for the R16x study) counts the full passes whose member x has E16[23]=0 and E16[24]=E17[24]; it draws no random numbers, so every other output is unchanged */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#include CONSTS
typedef uint32_t u32; typedef uint64_t u64;
#define ROR(x,n) (((x)>>(n))|((x)<<(32-(n))))
static inline u32 S0f(u32 x){return ROR(x,2)^ROR(x,13)^ROR(x,22);}
static inline u32 S1f(u32 x){return ROR(x,6)^ROR(x,11)^ROR(x,25);}
static inline u32 s0f(u32 x){return ROR(x,7)^ROR(x,18)^(x>>3);}
static inline u32 s1f(u32 x){return ROR(x,17)^ROR(x,19)^(x>>10);}
static inline u32 CHf(u32 x,u32 y,u32 z){return (x&y)^(~x&z);}
static inline u32 MAJf(u32 x,u32 y,u32 z){return (x&y)^(x&z)^(y&z);}
/* rng: xoshiro256++ seeded by splitmix64 */
static u64 rs[4];
static u64 sm(u64*x){u64 z=(*x+=0x9e3779b97f4a7c15ULL);z=(z^(z>>30))*0xbf58476d1ce4e5b9ULL;z=(z^(z>>27))*0x94d049bb133111ebULL;return z^(z>>31);}
static void seedrng(u64 s){u64 x=s;for(int i=0;i<4;i++)rs[i]=sm(&x);}
static inline u64 rotl(u64 x,int k){return (x<<k)|(x>>(64-k));}
static inline u64 rnd64(void){u64 r=rotl(rs[0]+rs[3],23)+rs[0],t=rs[1]<<17;rs[2]^=rs[0];rs[3]^=rs[1];rs[1]^=rs[2];rs[0]^=rs[3];rs[2]^=t;rs[3]=rotl(rs[3],45);return r;}
static inline u32 rnd32(void){return (u32)(rnd64()>>32);}
static inline u64 below(u64 n){return (u64)(((__uint128_t)rnd64()*n)>>64);}

/* member 0 = x, member 1 = y; A and E are stored at index i+4 (A_{-4} at 0), W at index i */
typedef struct { u32 A[2][41], E[2][41], W[2][37]; int l; } St;
static inline void stepm(St*s,int m,int t){
  u32*A=s->A[m]+4,*E=s->E[m]+4,*W=s->W[m];
  E[t]=A[t-4]+E[t-4]+S1f(E[t-1])+CHf(E[t-1],E[t-2],E[t-3])+KK[t]+W[t];
  A[t]=E[t]-A[t-4]+S0f(A[t-1])+MAJf(A[t-1],A[t-2],A[t-3]);
}
static inline int row_ok(const St*s,int t){
  u32 X=s->A[0][t+4],Y=s->A[1][t+4];
  if((X&CA_m[t])!=CA_v[t]||(X^Y)!=CA_d[t])return 0;
  X=s->E[0][t+4];Y=s->E[1][t+4];
  if((X&CE_m[t])!=CE_v[t]||(X^Y)!=CE_d[t])return 0;
  u32 q=CE_p[t]&CE_p[t-1];
  if(q&&((X^s->E[0][t+3])&q))return 0;
  X=s->W[0][t];Y=s->W[1][t];
  if((X&CW_m[t])!=CW_v[t]||(X^Y)!=CW_d[t])return 0;
  return 1;
}
static inline u32 gets(const St*s,int k,int i){return k==0?s->A[0][i+4]:k==1?s->E[0][i+4]:s->W[0][i];}
static inline int x2_ok(const St*s,int r){
  for(int j=0;j<NX2;j++){
    if(X2T[j][7]!=r)continue;
    int a=(gets(s,X2T[j][0],X2T[j][1])>>X2T[j][2])&1,b=(gets(s,X2T[j][4],X2T[j][5])>>X2T[j][6])&1;
    if((X2T[j][3]==1)!=(a==b))return 0;
  }
  return 1;
}
static int infw(u32 w,u32 d,u32 t){return (u32)(s0f(w+d)-s0f(w))==t;}
static u32 drawF7(void){
  u64 r=rnd64();u32 w=(u32)r;
  #define SETB(k,v) w=(w&~(1u<<(k)))|((u32)(v)<<(k))
  #define BIT(k) ((w>>(k))&1)
  if((r>>32)%65){SETB(11,0);SETB(22,1);SETB(26,1);SETB(18,BIT(1));SETB(30,BIT(9));SETB(28,BIT(0));}
  else{SETB(11,1);SETB(12,0);SETB(22,0);SETB(23,1);SETB(26,0);SETB(27,1);SETB(18,BIT(1));SETB(19,BIT(2));SETB(30,BIT(9));SETB(31,BIT(10));SETB(28,BIT(0));SETB(29,BIT(1));}
  return w;
}
static u32 drawF6(void){u32 w;do w=rnd32();while(!infw(w,D6,T6));return w;}
static void init_l(St*s,int l){
  memset(s,0,sizeof *s);s->l=l;
  for(int j=0;j<4;j++){s->A[0][4+12+j]=LAx[l][j];s->E[0][4+12+j]=LEx[l][j];s->A[1][4+12+j]=LAy[l][j];s->E[1][4+12+j]=LEy[l][j];}
  for(int j=0;j<7;j++){s->W[0][9+j]=LWx[l][j];s->W[1][9+j]=LWy[l][j];}
}
/* exact y-x difference of the schedule word t (t = 16..21): words 0..5 are equal in both members; W6 enters W21 through its F6 property */
static inline u32 dWsched(const St*s,int t){
  u32 d=s1f(s->W[1][t-2])-s1f(s->W[0][t-2])+s->W[1][t-7]-s->W[0][t-7];
  if(t==21)d+=T6;
  return d;
}
/* the part of step t that does not involve W_t or the proposal: A_{t-4} + E_{t-4} + S1(E_{t-1}) + CH(E_{t-1},E_{t-2},E_{t-3}) + K_t */
static inline u32 basef(const St*s,int t){return s->A[0][t]+s->E[0][t]+S1f(s->E[0][t+3])+CHf(s->E[0][t+3],s->E[0][t+2],s->E[0][t+1])+KK[t];}
typedef struct { u32 par, a, b; } Ch;
typedef struct { int l; u32 e; } R16e;
static int pc(u32 x){return __builtin_popcount(x);}

int main(int argc,char**argv){
  if(argc<6){fprintf(stderr,"usage: q3smc seed0 nrep NP M MT [-d]\n");return 1;}
  u64 seed0=strtoull(argv[1],0,10);int nrep=atoi(argv[2]);int NP=atoi(argv[3]);int M=atoi(argv[4]);long MT=atol(argv[5]);int diag=argc>6&&!strcmp(argv[6],"-d");
  FILE*f=fopen("variants.bin","rb");if(!f){fprintf(stderr,"no variants.bin\n");return 1;}
  fseek(f,0,SEEK_END);long nv=ftell(f)/4;fseek(f,0,SEEK_SET);u32*var=malloc(nv*4);if(fread(var,4,nv,f)!=(size_t)nv){return 1;}fclose(f);
  /* stage 16: exact enumeration of the (l, E16x) pairs that pass row 16 */
  long cap=1<<22,n16=0;R16e*r16=malloc(cap*sizeof(R16e));long per_l[32];
  {
    u32 v=CE_v[16];u32 fr=~CE_m[16];
    for(int l=0;l<32;l++){
      St s;init_l(&s,l);long c0=n16;
      u32 base=basef(&s,16),dW=dWsched(&s,16),sub=0;
      do{
        u32 e=v|sub;
        s.W[0][16]=e-base;s.W[1][16]=s.W[0][16]+dW;
        stepm(&s,0,16);stepm(&s,1,16);
        if(row_ok(&s,16)&&x2_ok(&s,16)){if(n16==cap){cap*=2;r16=realloc(r16,cap*sizeof(R16e));}r16[n16].l=l;r16[n16].e=e;n16++;}
        sub=(sub-fr)&fr;
      }while(sub);
      per_l[l]=n16-c0;
    }
  }
  fprintf(stderr,"stage 16: %ld pairs (u,l); per l:",n16);for(int l=0;l<32;l++)fprintf(stderr," %ld",per_l[l]);fprintf(stderr,"\n");
  double lz16=log2((double)n16)-37.0;
  int fb[23];for(int t=17;t<=21;t++)fb[t]=pc(CE_m[t]);
  St*P=malloc((size_t)NP*sizeof(St)),*Q=malloc((size_t)NP*sizeof(St));
  long maxch=(long)NP*M;Ch*chl=malloc(maxch*sizeof(Ch));
  for(int rep=0;rep<nrep;rep++){
    u64 seed=seed0+rep;seedrng(seed);
    for(int i=0;i<NP;i++){
      R16e e=r16[below(n16)];St*s=&P[i];init_l(s,e.l);
      s->W[0][16]=e.e-basef(s,16);s->W[1][16]=s->W[0][16]+dWsched(s,16);stepm(s,0,16);stepm(s,1,16);
    }
    double lz[40];for(int i=0;i<40;i++)lz[i]=-1e9;
    double lsum=lz16;lz[16]=lz16;int dead=0;
    for(int t=17;t<=22&&!dead;t++){
      long nc=0;
      for(int i=0;i<NP;i++){
        St s=P[i];
        if(t<=21){
          u32 m=CE_m[t],v=CE_v[t],base=basef(&s,t);
          for(int c=0;c<M;c++){
            u32 e=(rnd32()&~m)|v;
            s.W[0][t]=e-base;s.W[1][t]=s.W[0][t]+dWsched(&s,t);
            stepm(&s,0,t);stepm(&s,1,t);
            if(row_ok(&s,t)&&x2_ok(&s,t)){chl[nc].par=i;chl[nc].a=s.W[0][t];chl[nc].b=0;nc++;}
          }
        } else {
          for(int c=0;c<M;c++){
            u32 w6=drawF6(),w7=drawF7();
            s.W[0][6]=w6;s.W[1][6]=w6+D6;s.W[0][7]=w7;s.W[1][7]=w7+D7;
            for(int m2=0;m2<2;m2++){u32*W=s.W[m2];W[22]=s1f(W[20])+W[15]+s0f(W[7])+W[6];}
            stepm(&s,0,22);stepm(&s,1,22);
            if(row_ok(&s,22)&&x2_ok(&s,22)){chl[nc].par=i;chl[nc].a=w6;chl[nc].b=w7;nc++;}
          }
        }
      }
      double ft=(t<=21)?fb[t]:0;
      if(nc==0){dead=1;break;}
      lz[t]=log2((double)nc)-ft-log2((double)NP*M);lsum+=lz[t];
      for(int i=0;i<NP;i++){
        Ch c=chl[below(nc)];St*s=&Q[i];*s=P[c.par];
        if(t<=21){s->W[0][t]=c.a;s->W[1][t]=c.a+dWsched(s,t);stepm(s,0,t);stepm(s,1,t);}
        else{s->W[0][6]=c.a;s->W[1][6]=c.a+D6;s->W[0][7]=c.b;s->W[1][7]=c.b+D7;
          for(int m2=0;m2<2;m2++){u32*W=s->W[m2];W[22]=s1f(W[20])+W[15]+s0f(W[7])+W[6];}
          stepm(s,0,22);stepm(s,1,22);}
      }
      St*tmp=P;P=Q;Q=tmp;
      if(t==22&&diag){
        int hist[256];memset(hist,0,sizeof hist);
        for(int i=0;i<NP;i++){u32 e18=P[i].E[0][18+4],e19=P[i].E[0][19+4];int h=0;
          int b18[7]={1,5,10,11,18,28,29};for(int j=0;j<7;j++)h|=((e18>>b18[j])&1)<<j;h|=((e19>>29)&1)<<7;hist[h]++;}
        printf("PATTERNS seed %llu:",(unsigned long long)seed);for(int h=0;h<256;h++)if(hist[h])printf(" %02x:%d",h,hist[h]);printf("\n");
      }
    }
    long pass=0,tot=0,full=0,passreq=0;double ltail=-1e9;
    if(!dead){
      for(int i=0;i<NP;i++){
        St*s=&P[i];
        u32 Zx=s1f(s->W[0][22])+s->W[0][17]+s0f(s->W[0][9]),Zy=s1f(s->W[1][22])+s->W[1][17]+s0f(s->W[1][9]);
        for(long j=0;j<MT;j++){
          u32 w8=var[below(nv)];tot++;
          u32 wx=Zx+w8,wy=Zy+w8+D8;
          if((wx&CW_m[24])!=CW_v[24]||(wx^wy)!=CW_d[24])continue;
          int ok=1;
          for(int k=0;k<NX2;k++){if(X2T[k][0]!=2||X2T[k][1]!=24||X2T[k][5]!=24)continue;
            int a=(wx>>X2T[k][2])&1,b=(wx>>X2T[k][6])&1;if((X2T[k][3]==1)!=(a==b)){ok=0;break;}}
          if(!ok)continue;
          full++;
          St u=*s;
          u.W[0][8]=w8;u.W[1][8]=w8+D8;
          for(int t=23;t<=36&&ok;t++){
            for(int m2=0;m2<2;m2++){u32*W=u.W[m2];W[t]=s1f(W[t-2])+W[t-7]+s0f(W[t-15])+W[t-16];}
            stepm(&u,0,t);stepm(&u,1,t);
            ok=row_ok(&u,t)&&x2_ok(&u,t);
          }
          pass+=ok;
          if(ok&&!((u.E[0][16+4]>>23)&1)&&!(((u.E[0][16+4]^u.E[0][17+4])>>24)&1))passreq++;
        }
      }
      if(pass>0){ltail=log2((double)pass)-log2((double)tot);lsum+=ltail;}
    }
    int bad=dead||pass==0;
    printf("RESULT seed %llu NP %d M %d MT %ld log2est %.5f est %.10e\n",(unsigned long long)seed,NP,M,MT,bad?-1e9:lsum,bad?0.0:exp2(lsum));
    printf("TAG seed %llu full passes %ld, of which with E16[23]=0 and E16[24]=E17[24] (member x): %ld\n",(unsigned long long)seed,pass,passreq);
    printf("STAGES");for(int t=16;t<=22;t++)printf(" %.5f",lz[t]);printf(" tail %.5f  (row-24 survivors %ld of %ld, full passes %ld)\n",ltail,full,tot,pass);
    fflush(stdout);
  }
  return 0;
}
```

### F.5 `gen_consts.py`

```python
#!/usr/bin/env python3
# gen_consts.py - writes q3consts.h (the characteristic's cells, relations, per-l rows 12..15 of the published pair) and variants.bin (the W8x of the 782,800 variants of the 222 classes)
# from our own lowm.py (this package's counted program).  usage: gen_consts.py <lowm.py> [--relaxed]
import sys, importlib.util, struct, os
sys.dont_write_bytecode = True
path = sys.argv[1]; relaxed = '--relaxed' in sys.argv
spec = importlib.util.spec_from_file_location('lw', path); lw = importlib.util.module_from_spec(spec); spec.loader.exec_module(lw)
out = []
def arr(name, vals, typ='uint32_t'): out.append('static const %s %s[%d] = {%s};' % (typ, name, len(vals), ','.join('0x%x' % v if isinstance(v, int) else str(v) for v in vals)))
R = lw.R
out.append('/* generated by gen_consts.py from lowm.py (cells of rows 0..36; relaxed=%d) */' % relaxed)
arr('KK', lw.K)
for k in 'AEW':
    for j, nm in enumerate('mvdp'):
        arr('C%s_%s' % (k, nm), [lw.CELLS[k][i][j] if i in lw.CELLS[k] else 0 for i in range(0, R)])
x2 = [e for e in lw.X2 if max(e[1], e[5]) >= 16]
out.append('#define NX2 %d' % len(x2))
kmap = {'A': 0, 'E': 1, 'W': 2}
out.append('static const int X2T[NX2][8] = {%s};' % ','.join('{%d,%d,%d,%d,%d,%d,%d,%d}' % (kmap[e[0]], e[1], e[2], 1 if e[3] == '=' else 0, kmap[e[4]], e[5], e[6], max(e[1], e[5])) for e in x2))
Lt = lw.setup_l()
for nm, ix in (('LAx', 0), ('LEx', 1)):
    out.append('static const uint32_t %s[32][4] = {%s};' % (nm, ','.join('{%s}' % ','.join('0x%x' % Lt[l]['tx'][ix][i] for i in range(12, 16)) for l in range(32))))
for nm, ix in (('LAy', 0), ('LEy', 1)):
    out.append('static const uint32_t %s[32][4] = {%s};' % (nm, ','.join('{%s}' % ','.join('0x%x' % Lt[l]['ty'][ix][i] for i in range(12, 16)) for l in range(32))))
# words W9..W15 of both members
wx = [[lw.MX[9 + j] for j in range(5)] + list(lw.lstar(l)[0]) for l in range(32)]
wy = [[lw.MY[9 + j] for j in range(5)] + list(lw.lstar(l)[1]) for l in range(32)]
out.append('static const uint32_t LWx[32][7] = {%s};' % ','.join('{%s}' % ','.join('0x%x' % v for v in r) for r in wx))
out.append('static const uint32_t LWy[32][7] = {%s};' % ','.join('{%s}' % ','.join('0x%x' % v for v in r) for r in wy))
out.append('#define D6 0x%xu\n#define T6 0x%xu\n#define D7 0x%xu\n#define T7 0x%xu\n#define D8 0x%xu\n#define T8 0x%xu' % (lw.D6, lw.T6, lw.D7, lw.T7, lw.D8, lw.T8))
open('q3consts_%s.h' % ('relaxed' if relaxed else 'orig'), 'w').write('\n'.join(out) + '\n')
if not os.path.exists('variants.bin'):
    env = lw.Env(); w8 = []
    for ci in range(lw.NCLS):
        for a in env.members(ci): w8.append((lw.W8C - ((a + lw.C4) & lw.M32)) & lw.M32)
    print('variants', len(w8), 'distinct W8x', len(set(w8)))
    open('variants.bin', 'wb').write(struct.pack('<%dI' % len(w8), *w8))
```

### F.6 `analyze.py` (the preregistered rules)

```python
#!/usr/bin/env python3
# analyze.py - applies the preregistered rules of PREREG_q3M.txt to the outputs in out/ ; usage: analyze.py [dir]
import glob, math, re, statistics, sys, json
from scipy.stats import t as student_t
d = sys.argv[1] if len(sys.argv) > 1 else 'out'
def res(f):
    tx = open(f).read()
    m = re.search(r'RESULT seed (\d+) NP \d+ M \d+ MT \d+ log2est (\S+) est (\S+)', tx)
    st = re.search(r'STAGES (.*?) tail (\S+)', tx)
    return int(m.group(1)), float(m.group(3)), float(m.group(2)), [float(v) for v in st.group(1).split()] + [float(st.group(2))]
def load(tag): return sorted(res(f) for f in glob.glob('%s/%s_*.txt' % (d, tag)))
def bound(Z, name, n_exp):
    n = len(Z); mean = statistics.mean(Z); sd = statistics.stdev(Z); tq = float(student_t.ppf(0.99, n - 1)); lb = mean - tq * sd / math.sqrt(n)
    print('%s: %d replicates (registered %d), mean 2^%.4f, relative sd %.4f, t(0.99, %d df) = %.4f, one-sided 99%% lower bound 2^%.4f' % (name, n, n_exp, math.log2(mean), sd / mean, n - 1, tq, math.log2(lb)))
    return mean, sd, lb
def stagemeans(R):
    cols = list(zip(*[r[3] for r in R])); return [statistics.mean(c) for c in cols]
out = {}
V = load('V'); R1 = load('R1'); R2 = load('R2')
if V:
    Z = [r[1] for r in V]; mean, sd, lb = bound(Z, 'V (original cells)', 64)
    # reference: study B of 7319bba (32 replicates): mean 2^-73.9987, relative sd 0.0378, bound 2^-74.0225
    mB = 2 ** -73.9987; rsB = 0.0378; nB = 32
    rseV = sd / mean / math.sqrt(len(Z)); rseB = rsB / math.sqrt(nB)
    z = (mean / mB - 1) / math.sqrt(rseV ** 2 + rseB ** 2)
    lbl = math.log2(lb)
    a = abs(z) <= 2.576; b = abs(lbl - (-74.0225)) <= 0.04
    print('   stage means (log2):', ['%.4f' % v for v in stagemeans(V)])
    print('   criterion (a): z = %.3f against study B (|z| <= 2.576): %s ; criterion (b): |LB_V - (-74.0225)| = %.4f <= 0.04: %s ; VALIDATION %s' % (z, 'PASS' if a else 'FAIL', abs(lbl - (-74.0225)), 'PASS' if b else 'FAIL', 'PASS' if (a and b) else 'FAIL'))
    out['V'] = dict(n=len(Z), mean_log2=math.log2(mean), relsd=sd / mean, lb_log2=lbl, z=z, pass_=bool(a and b), stages=stagemeans(V))
lbs = {}
for name, Rr, n in (('R1', R1, 128), ('R2', R2, 128)):
    if not Rr: continue
    Z = [r[1] for r in Rr]; mean, sd, lb = bound(Z, name + ' (relaxed cells)', n)
    print('   stage means (log2):', ['%.4f' % v for v in stagemeans(Rr)])
    lbs[name] = math.log2(lb)
    out[name] = dict(n=len(Z), mean_log2=math.log2(mean), relsd=sd / mean, lb_log2=math.log2(lb), log2est=[r[2] for r in Rr], stages=stagemeans(Rr))
if len(lbs) == 2:
    m = min(lbs.values()); q = math.floor(100 * m + 1e-9) / 100
    print('lowest bound 2^%.5f -> declared q3 = 2^%.2f' % (m, q))
    out['declared'] = q
    if 'V' in out: print('gain over R37M base 2^-74.03: %.2f bits (declared)' % (q + 74.03))
# pooled (descriptive only)
if R1 and R2:
    Z = [r[1] for r in R1 + R2]; mean = statistics.mean(Z); sd = statistics.stdev(Z)
    print('pooled R1+R2 (descriptive): n %d mean 2^%.4f relative sd %.4f, 99%% bound 2^%.4f' % (len(Z), math.log2(mean), sd / mean, math.log2(mean - float(student_t.ppf(0.99, len(Z) - 1)) * sd / math.sqrt(len(Z)))))
json.dump(out, open('analysis.json', 'w'), indent=1)
```

### F.7 `check_alt.py`

```python
#!/usr/bin/env python3
# check_alt.py - the three alternative 37-step semi-free-start collisions (one per new pattern of E18/E19) against the cells of this package's lowm.py and of the program with the Table 15 cells
import sys, importlib.util
sys.dont_write_bytecode = True
def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
new = load(sys.argv[1], 'lw_new'); old = load(sys.argv[2], 'lw_old')
h8 = new.h8
PAIRS = {
 'Table 15 (published pair)': (new.CV0, new.MY, new.MX),
 'G1': (h8('063c3500 078f49ec 15f3f954 b92ec209 8988f13d 35819c7c 63e0bf72 236a0c73'),
        h8('da42b17c 211c7ff3 76ab73f3 6af71849 370eee2f 309c7244 fca0a79d c81ace78 9f0d78e1 681b8277 faa9c7e0 56aed439 cc2dbbc2 dd2ba0fc b95d377b 5dd43a81'),
        h8('da42b17c 211c7ff3 76ab73f3 6af71849 370eee2f 309c7244 dca0a79d cc5ac678 bf0d78e1 6d1a90dd faa1d3e0 56aed439 cc2dbbc2 dd2ba0fc bd1d3f7b 7dd43a81')),
 'G2': (h8('3c2679fb 0adeef20 3589a7a5 83ef1642 ad5f1106 e029b47e 6b4d40e9 4ee553b3'),
        h8('3bfa2198 3aeec0b8 10348d11 5ba77ac0 b56da910 6997b907 395831ab 9230897d 9f0d78e1 681b8277 faa9c7e0 56aed439 cc2dbbc2 dd2ba0fc b95d377b 5dd43a81'),
        h8('3bfa2198 3aeec0b8 10348d11 5ba77ac0 b56da910 6997b907 195831ab 9670817d bf0d78e1 6d1a90dd faa1d3e0 56aed439 cc2dbbc2 dd2ba0fc bd1d3f7b 7dd43a81')),
 'G1 xor G2': (h8('a49c8638 3696c10f 2a0f741c 55456216 c7b75338 54905dab c30d520e e749445c'),
        h8('bb6ca525 d640983d 28963f42 5ca2459f 116481ee 4e1a472b edfab13a 29ba7d40 9f0d78e1 681b8277 faa9c7e0 56aed439 cc2dbbc2 dd2ba0fc b95d377b 5dd43a81'),
        h8('bb6ca525 d640983d 28963f42 5ca2459f 116481ee 4e1a472b cdfab13a 2dfa7540 bf0d78e1 6d1a90dd faa1d3e0 56aed439 cc2dbbc2 dd2ba0fc bd1d3f7b 7dd43a81')),
}
def cells(lw, cv, mx, my):
    tx, ty = lw.trace(cv, mx), lw.trace(cv, my)
    return all(lw.row_ok(tx, ty, i, i not in (6, 7)) for i in range(-4, lw.R)) and all(lw.x2_ok(tx, r) for r in range(8, lw.R))
print('%-28s %-9s %-24s %-24s' % ('pair (x = M\', y = M)', 'collides', 'cells of this lowm.py', 'cells of Table 15'))
for k, (cv, my, mx) in PAIRS.items():
    c = new.compress(cv, mx) == new.compress(cv, my) and mx != my
    print('%-28s %-9s %-24s %-24s' % (k, c, cells(new, cv, mx, my), cells(old, cv, mx, my)))
```

## Appendix G. The joint study of the four patterns and R16x: preregistration, results

Files in `q3/` (`q3smc.c` as listed in F.4, `q3consts_r16x.h` written by `gen_consts.py` from `experiments/lowm.py` as filed, sha256 aa4356605422aa4eb070efe67e1938f071fd17e9ed60a7a5266199a62bbc6b9b; `variants.bin` unchanged; outputs in `studyX/out/`). Build: `gcc -O2 -DCONSTS='"q3consts_r16x.h"' q3smc.c -lm -o q3smc_r16x`; run: `q3smc_r16x SEED 1 8192 512 16384`.

### G.1 Preregistration (written before any listed seed ran; stamp 2026-10-12T16:13:47Z, sha256 18569704b1115d99c138e641986101687836aa408e1f29d670cad354da0691d3)

```text
preregistration: our own sequential-Monte-Carlo estimate of q3 for the 222-class A0-variant attack on 37-step SHA-256 (R37M family) with the four row-18/19 value patterns AND the R16x relaxation accepted JOINTLY (one carrier)
written before any listed seed was run; the stamp is the line below.
stamp: 2026-10-12T16:13:47Z
program: q3smc.c (ours; the filed R37M estimator plus a TAG line that draws no random numbers), sha256 f0e3efc8d06c58c03c7dd7fe86ef08d8d00b8868202e6c49557f85c479c61f9c.
constants: q3consts_r16x.h (sha256 aa4356605422aa4eb070efe67e1938f071fd17e9ed60a7a5266199a62bbc6b9b), written by gen_consts.py (sha256 14ea0015f43b1ea86109ccc78e86cf392c12a9a34c7ece6a1c3babc1be6b4ae7) from this package's lowm.py (sha256 5107f3f734729e9156bbf1ecbd4c5097d1258d78f5515128379ea6f370facb67).
 the carrier = R37M's relaxed cells (rows 18/19 eight value bits free) with three further changes, all in lowm.py's characteristic: CHE[16] bit 23 '0' -> '=' (E16[23] free), CHE[17] bit 24 '+' -> '=' and the two-bit condition E16[24]=E17[24] removed. The R16x parity E16[23]^E19[29]^E18[1]^E18[5]=0 and the other row-18 linear relations are NOT imposed (weaker carrier; any pass through row 36 is still a full collision: rows 22..36 cells unchanged, zero output difference).
variant list: variants.bin (sha256 6900f64cec67217eb352fd43cd0552c92b2514b892481c95f761d19619d1e3c5), unchanged from R37M.
known answer (run before this stamp, disclosed): the new binary built with q3consts_relaxed.h reproduces byte-identically the filed R37M study outputs of seeds 720000 and 721000 (RESULT and STAGES lines). Smoke: seed 1 with q3consts_r16x.h (stage 16 = 2,097,152 pairs, 65,536 per l for all 32 l; log2est -71.63000). Seed 1 is not used below.
main study (binary q3smc_r16x), two independent blocks: J1 seeds 740000..740127 (128 replicates), J2 seeds 741000..741127 (128 replicates); NP = 8192, M = 512, MT = 16384 for every replicate.
bound: per block LB = mean - t(0.99, 127 df) sd / sqrt(128) over the replicate linear estimates (the replicate spread carries any overdispersion of the within-run counts).
rule (fixed in advance): declared q3 = 2^x with x = floor(100 log2(min(LB_J1, LB_J2))) / 100. Gain over the filed R37M q3 2^-72.02 = x + 72.02 (bits).
descriptive only: pooled mean; per-replicate TAG share (full passes whose member x keeps E16[23]=0 and E16[24]=E17[24]); comparison with r16_settle +0.590 [0.548, 0.631].
every listed seed is run and reported; none dropped or rerun except a crash not caused by the program. At most 2 processes at once; wait while load > 35.
```

The program hash named in the preregistration is that of `lowm.py` when the constants were written; the later edits of the program (the row-16 constants of the ledger, `FEASIBLE_L`, q3) do not touch the cells, and regenerating the constants from the program as filed gives the same file (sha256 above).

### G.2 Results

Rule applied: lowest bound 2^-71.46286 of J1 (2^-71.4629) and J2 (2^-71.4524), rounded down to two decimals: **q3 = 2^-71.47**. pooled 256 replicates: mean 2^-71.4236, relative sd 0.1118, bound 2^-71.4474 (descriptive). Stage means (log2): 16: -16.000, 17: -12.000, 18: -8.000, 19: -11.430, 20: -7.000, 21: -2.000, 22: -11.003, tail -3.999. TAG: 1,438,939,086 of 2,149,260,669 full passes keep E16[23] = 0 and E16[24] = E17[24] (share 0.6695).

All 128 log2 estimates of J1 (seeds 740000..740127, in order):

```text
-71.641 -71.683 -71.399 -71.499 -71.485 -71.546 -71.447 -71.435 -71.327 -71.389 -71.528 -71.535 -71.239 -71.454 -70.975 -71.672
-71.370 -71.139 -71.243 -71.644 -71.359 -71.528 -71.703 -71.312 -71.404 -71.306 -71.255 -71.283 -71.464 -71.335 -71.715 -71.343
-71.498 -71.420 -71.379 -71.739 -71.317 -71.226 -71.874 -71.547 -71.679 -71.328 -71.426 -71.311 -71.270 -71.214 -71.602 -71.365
-71.407 -71.256 -71.257 -71.497 -71.249 -71.416 -71.365 -71.388 -71.466 -71.529 -71.349 -71.357 -71.535 -71.619 -71.519 -71.580
-71.201 -71.261 -71.270 -71.404 -71.498 -71.709 -71.428 -71.472 -71.589 -71.381 -71.631 -71.692 -71.598 -71.465 -71.429 -71.516
-71.243 -71.508 -71.350 -71.408 -71.325 -71.468 -71.621 -71.535 -71.359 -71.656 -70.986 -71.492 -71.396 -71.528 -71.565 -71.334
-71.345 -71.438 -71.382 -71.563 -71.450 -71.363 -71.326 -71.351 -71.335 -71.783 -71.566 -71.262 -71.327 -71.518 -71.336 -71.697
-71.280 -71.365 -71.511 -71.513 -71.481 -71.451 -71.213 -71.666 -71.441 -71.323 -71.121 -71.745 -71.378 -71.449 -71.574 -71.562
```

All 128 log2 estimates of J2 (seeds 741000..741127):

```text
-71.386 -71.166 -71.802 -71.670 -71.447 -71.439 -71.487 -71.555 -71.871 -71.542 -71.515 -71.371 -71.288 -71.276 -71.488 -71.260
-71.363 -71.234 -71.439 -71.527 -71.404 -71.335 -71.323 -71.282 -71.142 -71.495 -71.486 -71.440 -71.567 -71.526 -71.225 -71.547
-71.708 -71.498 -71.396 -71.172 -71.207 -71.244 -71.477 -71.456 -71.622 -71.626 -71.392 -71.570 -71.325 -71.502 -71.625 -71.627
-71.299 -71.168 -71.402 -71.708 -71.461 -71.514 -71.707 -71.631 -71.452 -71.285 -71.512 -71.535 -71.549 -71.321 -71.384 -71.237
-71.459 -71.641 -71.667 -71.292 -71.207 -71.079 -71.272 -71.638 -71.430 -71.117 -71.399 -71.567 -71.437 -71.051 -71.477 -71.343
-71.388 -71.454 -71.556 -71.575 -71.740 -71.627 -71.380 -71.609 -71.428 -71.192 -71.347 -71.640 -71.401 -71.653 -71.590 -71.648
-71.225 -71.195 -71.167 -71.189 -71.351 -71.680 -71.416 -71.386 -71.274 -71.511 -71.581 -71.551 -71.439 -71.265 -71.324 -71.431
-71.446 -71.377 -71.256 -71.158 -71.443 -71.393 -71.283 -71.442 -71.357 -71.124 -71.344 -71.565 -71.410 -71.382 -71.269 -71.606
```

Interim looks: the analysis was run on partial outputs while the blocks were running, to monitor progress; no seed, parameter or rule was changed after any look.

The program's own output for the first seed of each block:

```text
--- seed 740000 ---
RESULT seed 740000 NP 8192 M 512 MT 16384 log2est -71.64139 est 2.7151355317e-22
TAG seed 740000 full passes 8247250, of which with E16[23]=0 and E16[24]=E17[24] (member x): 5723505
STAGES -16.00000 -12.00196 -8.00105 -11.57374 -7.00012 -2.05054 -10.98947 tail -4.02452  (row-24 survivors 8247250 of 134217728, full passes 8247250)
--- seed 741000 ---
RESULT seed 741000 NP 8192 M 512 MT 16384 log2est -71.38558 est 3.2419013954e-22
TAG seed 741000 full passes 8731984, of which with E16[23]=0 and E16[24]=E17[24] (member x): 6561999
STAGES -16.00000 -11.99869 -8.00174 -11.38529 -6.99964 -2.01665 -11.04145 tail -3.94212  (row-24 survivors 8731984 of 134217728, full passes 8731984)
```


## Appendix H. Refile additions (R37ZF2): memory bound, the upper bound on q3, sensitivity tables and the measurements of that refile

### H.1 The ruling on e30cf5a1 and how each blocking reason is answered

The filing e30cf5a1 (R37ZF, the same attack, claimed 60.99099, with the measured preprocessing peak as its memory) was ruled not_evaluable in the exploratory lane with seven reasons and no fatal finding; every heuristic was rated plausible. This text answers each reason. No operation count and no cell of the program changed: `experiments/lowm.py` was byte-identical to the one filed in e30cf5a1 (in R37ZF3 the A_C term was removed from `ledger()`; R37ZF5 restores it, Appendix I).
- **resources_defined (F1 and F2: memory of the characteristic search not bounded; F2: time allowance).** Memory is stated as the maximum over named phases with the bound 2^29 bytes (Section H.2), with the measured peaks, including the construction of the characteristic, and their evidence files. A_C is charged (Section 11.2, H.3, Appendix I).
- **heuristics_disclosed (F4: the impossible sentence).** The filed sentence "A_C = 2^56 would give 63.09331" was wrong, because a smaller allowance gives a smaller total. A_C = 2^60 is charged and its sensitivity table is in H.5 (Section 11.2). H1, H2 and H3 are each stated as an assumption in the four-field form, each with a sensitivity table (H.5). Nothing else in the claim is heuristic (end of this section).
- **evidence_relevant (F1: score-critical experiments not run by the organizer).** Two further organizer-run experiments (H.7) check consequences of H1 and H3 on seeds the organizer chooses. The measurements of this refile (H.6) are ours and are labelled as ours. What none of them can show is stated in H.7.
- **H1 (F-H1-EXTRAPOLATION).** The C measurement is extended from 2^23 to 2^31.0 first blocks (H.6c), with a sensitivity table (H.5). H1 stays an assumption and is stated as one.
- **H2 (F-H2-UPPER-BOUND, F-H2-STATISTICAL-COVERAGE).** q3 <= 2^-70 is no longer taken from a lower bound: H.4 derives a one-sided upper bound from the same 256 replicates (Student and percentile bootstrap), 2^-71.38 for the cell event, which is 1.38 bits below 2^-70; this refile (R37ZF4) has the exact event and its bound is 2^-70.06 (H.4). The coverage of the Student bound is checked against the bootstrap (H.4). No second independent estimator was written; that is a limit and is stated.
- **H3 (F-H3-UNIVERSAL-DEPENDENCE).** H3 is restated as an average over the trials with the weights Pr[A_t], which is the only quantity the Bonferroni sum of Section 10 needs; the dependence of distinct good pairs of one first block is checked through rows 16 to 22 as a program check (H.6b). Dependence of later rows at full scale cannot be measured; the margin and a delta table are in H.5.
- **Characteristic-search memory.** The construction of the characteristic is a phase of the memory bound: generator, CNF dump and solver, measured under an address-space cap of 2^29 bytes (H6, H.2, Appendix I).

Finding by finding (ids of the judge dossier of e30cf5a1; the answers about A_C and the memory are those of R37ZF5):

| finding id | severity | answer | where |
|---|---|---|---|
| EXP-001 | material | No organizer run estimates q3; still true. The q3 studies stay participant-run and are labelled so; the coverage of their bound is checked against a bootstrap and an upper bound is derived. | H.4, H2 |
| EXP-002 | material | The q3 replay files cannot be added to the experiment sources (65,536 bytes, of which lowm.py uses 63,351). q3smc.c, gen_consts.py and analyze.py are in this proof as text with the hashes of the files that were run; the raw outputs are the 256 listed estimates of Appendix G.2. Left out: the C source as a file, the headers, the variant data and the raw outputs as files. | H.8, Appendix F, G |
| EXP-003 | material | Unfixable at full scale: zero full collisions of the 37-step target are found and none is claimed. The two original experiments stay as functional checks of the counted program. | Section 13.2, H.7 |
| EXP-004 | material | H1 is measured on 2^31.0 blocks instead of 2^23; H3 is checked through row 22 as a program check, and its remaining extrapolation is stated. | H.6b, H.6c, H.5 |
| EXP-005 | material | Two added experiments run on the organizer's seeds; no holdout nonce is claimed; most trials return no pair by design. | H.7 |
| F-H1-EXTRAPOLATION | material | Extended measurement, sensitivity table, H1 stated as an assumption. | H.5, H.6c |
| F-H2-STATISTICAL-COVERAGE | material | Student bounds checked against a percentile bootstrap; no second independent estimator (stated). | H.4 |
| F-H2-UPPER-BOUND | material | A one-sided upper bound from the same replicates, 2^-71.38; 2^-70 is a weaker consequence. | H.4 |
| F-H3-UNIVERSAL-DEPENDENCE | material | H3 restated as the average over trials with weights Pr[A_t]; rows 16 to 22 checked as a program check; delta table. | Section 10, H.5, H.6b |
| F1-unmeasured-characteristic-search-memory | material | The generator, the CNF dump and the solver on the real 37-step dense model are measured (H6); the completion of the search under the cap is not, and is stated. | H.2, Appendix I |
| F2-unbounded-characteristic-search-memory | material | Bound 2^29 bytes, enforced by an address-space cap on every construction phase. | H.2 |
| F1-unreported-score-critical-experiments | material | Two organizer-run program checks added; our measurements labelled as ours; limits stated. | H.6, H.7 |
| F2-indirect-preprocessing-time-allowance | material | A_C = 2^60 is a labelled allowance with a sensitivity table; not resolved by a metered run. | Section 11.2, H.3, H.5 |
| F3-full-scale-success-extrapolation | material | Joint sensitivity: the H1, H2 and H3 tables of H.5 and one joint line (q3 one bit lower, eps = 0.10 and delta = 2^-4 together: 61.73889). | H.5 |
| F4-preprocessing-sensitivity-inconsistency | minor | A_C = 2^56 gives 58.88745 (a smaller allowance gives a smaller total). | H4, H.5 |

**Nothing else in the claim is heuristic.** The operation counts and the ledger (Sections 9, 11 and Appendix B), the exactness of the filters F6 and F7 and of the row-16 test (Section 13.2, Appendix A), the success arithmetic (Section 10, Appendix C) and the cap are computed or checked exhaustively. The premises are H1, H2, H3 (probability), H4 (the advice allowances), H5 (pricing), H6 (the memory bound) and H7 (the success floor), all in claim.heuristics. A_S is bounded by the caps of its re-solve (Section 11.2).

### H.2 Memory: a bound of 2^29 bytes over all phases

**Memory bound.** The procedure runs these phases: the construction of the characteristic (charged as A_C: generation of the SAT instance, its CNF dump, the solver search), the preprocessing of Section 14.2 (tables computed from the characteristic and S), the Step-1 re-solve and its completion (Section 11.2), and the online phase. Its peak memory is declared at most 2^29 = 536,870,912 bytes (H6): the online phase by its computed size, 607,744 bytes; the preprocessing by its computed working set (step (i) of Section 14.2 groups the 12.1 x 10^6 values of the family, below 2^24 entries of 8 bytes = 2^27 bytes, and the tables of Section 14.1 are built once); the Step-1 re-solve by the address-space cap `prlimit --as=117440512` under which it runs; the completion by the organizer's 128 MB experiment sandbox in which `a0-sfs-r37` runs it; the construction of the characteristic by the address-space cap `prlimit --as=536870912` under which its generator, translation and CNF dump were run and under which its solver is run (the process cannot hold more), the largest measured peak being the STP CNF dump, 499,384,320 bytes (2^28.895). The development solver runs of this line were made under an address-space cap of at most 2^28 bytes or measured below it (table). The claimed memory_log2_bytes is 29, so the score is time_log2 + (29 - 20) = 60.4854 + 9 = 69.4854.

| phase | bound (bytes) | how | measured peak (bytes) | evidence file |
|---|---:|---|---:|---|
| online: tables, code, constants | 607,744 | computed | - | Section 14.1 (`lowm.py memory`) |
| preprocessing (Section 14.2) | < 2^27 + 607,744 | computed | - | Section 14.2 |
| characteristic construction: gen37.py (LLW24 FunctionModel, 37 steps), dense_pub.cvc | 536,870,912 (2^29) | `prlimit --as` cap | 100,712,448 (2^26.58) | premise_tests/P12/logs_zf5/gen.time |
| characteristic construction: translation to SMT2 (dense_pub.cvc.smt2, sha256 d1c1976d...68cc) | 536,870,912 (2^29) | `prlimit --as` cap | 99,696,640 (2^26.57) | premise_tests/P12/logs_zf5/shim.time |
| characteristic construction: STP 2.4.1 CNF dump (200,534 variables, 954,732 clauses; sha256 445a880e...42f4, identical in 4 runs) | 536,870,912 (2^29) | `prlimit --as` cap | 499,384,320 (2^28.895); 499,286,016 and 499,290,112 in two earlier runs; fails under 2^28 | premise_tests/P12/logs_zf5/stpcap29.time, P12/RESULT.md |
| characteristic construction: kissat 4.0.3 on that CNF, zero conflicts | 268,435,456 (2^28) | `prlimit --as` cap | 157,622,272 (2^27.232) | P12/RESULT.md |
| characteristic construction: kissat 4.0.3, seeds 1, 2, 3 to 2^22 conflicts, each run twice (no solution) | 268,435,456 (2^28) | `prlimit --as` cap | address space at most 232,087,552 (2^27.790) | P12/RESULT.md |
| Step-1 re-solve, s37_all.cnf, kissat 4.0.4, 2 seeds, SAT, models verified | 117,440,512 (2^26.807) | `prlimit --as` cap | 88,006,656 (2^26.39) | stepback/STEP1_CAP_LADDER.md, step1_cap_ladder/devmem.jsonl |
| completion to an SFS pair | 128 MB | organizer sandbox | - | experiment `a0-sfs-r37` |
| development: derivation instance ex39_search_90.cnf (39-step, from our r38 work), kissat 4.0.4, SAT in 85 s, model verified | 268,435,456 (2^28) | `prlimit --as` cap | 94,281,728 (2^26.49) | H.6a |
| development: derivation instance, cadical 2.1.3 / kissat 4.0.3 | - | measured | 198,053,888 / 188,432,384 | stepback/PREP_MEMORY.md |
| development: Step-1 cap ladder, 25 runs (kissat, cadical) | caps <= 2^28 | `prlimit --as` cap | <= 183,078,912 | step1_cap_ladder/devmem.jsonl |
| development: Step-1 stand-ins of Section 14.1 (CaDiCaL largest) | - | measured | <= 199,008,256 (2^27.569) | Section 14.1 |

The bounds of the online and preprocessing phases are computed, not measured; the caps bound the generator, dump and solver phases; the peaks are our measurements on one machine, not run by the organizer (the logs of the three construction runs under the 2^29 cap are `premise_tests/P12/logs_zf5/`, the rest `premise_tests/P12/`). The search itself was not completed: three seeds to 2^22 conflicts did not solve the dense instance (H6, H.3). The claim is 2^29 and not 2^28 because the STP dump needs 2^28.895 bytes, and not 2^26.81 because the construction does not fit 112 MiB (kissat aborts at zero conflicts under that cap).

### H.3 A_C = 2^60: a labelled allowance, and how it is justified

A_C is the charge for the search that produced the characteristic of the paper; it is charged because collision-frontier-v5 requires the construction of nonuniform input to be accounted for even when the search is omitted from the program (F-COST-001 of 96933f8e). It is an **allowance, not a measurement**, and it is nearly all of the preprocessing charge (2^60 of 2^60.00141). Its justification, stated as it is: (1) the accepted filing 6eeefb64 charged a measured complete re-run of the predecessor 35-step search at 593,858 solver CPU-seconds, priced at 2^21.427 units per CPU-second at C = 2644; 2^60 units are 2^38.57 CPU-seconds, 688,000 times that re-run; (2) 0db0eeb6 charges the same A_C. What is not shown: the time of the paper's own 37-step search is unpublished, we did not complete a re-run of it (on the dense instance of the 37-step model, kissat 4.0.3 with three seeds ran 2^22 conflicts each, 66 to 99 single-thread minutes per seed, without a solution, H6 and H.2, and a 16-thread CryptoMiniSat run of 2026-10-12 did not solve it within 7,200 s either), and that the authors' search was no cheaper than 2^60 units is a premise (H4). The effect of that premise on the claim is in H.5. Replacing the allowance by a metered re-derivation would lower the claim; that was not done.

### H.4 The upper bound on q3 (used by H3 only) and the coverage of the bound

H3 (b) uses an upper bound on q3. The preregistered procedures of Appendices G and K produce lower bounds only. The table below is for the cell event q3_cell; the exact-event bound that H3 uses follows it. From the 128 replicate estimates of each block listed in Appendix G.2 (log2, rounded to 0.001 bit) we compute here, for the mean of each block, the one-sided 99 percent **upper** Student bound mean + t(0.99, 127) sd / sqrt(128), with t = 2.3563, and a percentile bootstrap upper bound (20,000 resamples of the 128 linear estimates, `random.Random(12345)`). The script is at the end of this section.

| block | mean (log2) | relative sd | skewness | Student lower / upper (log2) | bootstrap lower / upper (log2) | largest replicate (log2) |
|---|---:|---:|---:|---|---|---:|
| J1 | -71.4295 | 0.110 | 0.36 | -71.4628 / -71.3970 | -71.4620 / -71.3974 | -70.975 | |
| J2 | -71.4176 | 0.114 | 0.22 | -71.4524 / -71.3837 | -71.4521 / -71.3837 | -71.051 | |

Both lower bounds reproduce the filed values 2^-71.4629 and 2^-71.4524. The larger upper bound is **2^-71.38**, so q3_cell <= 2^-71.38 (the raw per-replicate outputs give 2^-71.3837 and 2^-71.3970). For the cell event, H3 (b) is at most 2^35 x 2^19.58 x 2^5 x 2^-71.38 = 2^-11.80 and delta <= 2^-11 + 2^-11.80 = 2^-10.34.

**The exact event (this filing).** q3 = q3_cell x (exact/cell), and the ratio has the one-sided 99 percent upper bound 2.4848 + 2.326 x 0.0027 = 2.4911 (log2 1.3167, Section 7.4d). Hence q3 <= 2^(-71.3837 + 1.3167) = 2^-70.067, rounded up to **q3 <= 2^-70.06**; this is above 2^-70, so the earlier statement q3 <= 2^-70 no longer holds for this event and is not used. H3 (b) is at most 2^35 x 2^19.58 x 2^5 x 2^-70.06 = 2^-10.48 and delta <= 2^-11 + 2^-10.48 = 2^-9.7167, written 2^-9.71, below the budget 2^-9.4 with 0.31 bit to spare; the break-even q3 is 2^-69.557, 0.50 bit above the bound. The statements of this Appendix that name q3_cell refer to the cell event (the q3_used of 96933f8e, 2^-71.47), those that name q3 to the exact event. What the bound rests on: that the mean of the estimator is q3 (an importance-weighted estimator written for this filing and validated against the registered study of 7319bba, not against a second independent implementation) and that the mean of 128 replicates is close to normal. The bootstrap agrees with Student to 0.001 bit, the skewness is 0.2 to 0.4, and the largest single replicate of the cell event is 2^-70.98. These are checks of the coverage, not a proof of it.

```python
import sys,math,random
L=open(sys.argv[1],encoding='utf8').read().split('\n')
def blk(a,b): return [float(x) for l in L[a-1:b] for x in l.split()]
i1=[i for i,l in enumerate(L) if l.startswith('All 128 log2 estimates of J1')][0]
i2=[i for i,l in enumerate(L) if l.startswith('All 128 log2 estimates of J2')][0]
for J in (blk(i1+4,i1+11),blk(i2+4,i2+11)):
    v=[2**x for x in J]; k=len(v); m=sum(v)/k; sd=(sum((a-m)**2 for a in v)/(k-1))**.5; se=sd/k**.5
    rnd=random.Random(12345); bm=sorted(sum(rnd.choice(v) for _ in range(k))/k for _ in range(20000))
    print(math.log2(m-2.3563*se),math.log2(m+2.3563*se),math.log2(bm[200]),math.log2(bm[19799]))
```

### H.5 Sensitivity tables

Computed from the ledger (the H2 rows by the ledger code, the H1 and H3 rows by scaling the attack term 2^58.68 = T - (A_C + A_S + DEV)).

**H1.** If the expected number of good pairs per first block is (1 - eps) of g, the number of first blocks, and with it the attack term, grow by 1/(1 - eps). This ignores the per-pair work saved, so it is an upper estimate.

| eps | 0 | 0.01 | 0.05 | 0.10 | 0.25 |
|---|---:|---:|---:|---:|---:|
| time_log2 that keeps 0.39 | 60.48540 | 60.48955 | 60.50688 | 60.53038 | 60.61634 |

**H2.** If the true q3 (the exact event) is 2^b below q3_used = 2^-70.16.

| b | 0 | 0.5 | 1 | 2 | 4 |
|---|---:|---:|---:|---:|---:|
| time_log2 that keeps 0.39 | 60.48540 | 60.64569 | 60.84571 | 61.37378 | 62.87921 |

A q3 above q3_used lowers the cost. The upper bound of H.4 gives nothing back, because the claim does not use it; it enters only H3. With the cell-event value 2^-71.47 (b = 1.31) the ledger gives 60.99099.

**H3.** delta enters through the divisor 1 - delta of the success floor (Section 10); filed delta = 2^-9.4.

| delta | 2^-9.4 (filed) | 2^-8 | 2^-6 | 2^-4 | 0.1 | 0.25 |
|---|---:|---:|---:|---:|---:|---:|
| time_log2 | 60.48540 | 60.48671 | 60.49161 | 60.51224 | 60.53005 | 60.61597 |

**Joint.** q3 one bit lower, good-pair rate 10 percent lower and delta = 2^-4 together: time_log2 60.95894 (score 69.95894 with the memory term 9.0).

**A_C (H4), all other terms as filed.** A_C = 2^56: 58.88745; 2^58: 59.37846; 2^60 (filed): 60.48540; 2^62: 62.13750; 2^64: 64.03563.

**Memory term (score = time_log2 + memory_log2_bytes - 20).** Bound 2^29: 69.48540 (claimed). Largest measured peak 2^28.895: 69.38. A bound of 2^28 would not hold (the STP dump needs 2^28.895).

### H.6 Measurements of this refile (ours, not run by the organizer; one local machine; no statistic is claimed)

All three were run on the local PC (WSL Ubuntu, nice 10, one thread per process) on 2026-10-15; the sources are `r37zf2_meas/` in our working directory and are not in the package (the experiment budget is full); their hashes are listed in H.8.

**H.6a. The derivation instance under a 2^28-byte cap.** `prlimit --as=268435456 kissat404 --time=3600 ex39_search_90.cnf` (kissat 4.0.4, sha256 4ebc02c3...a256710; CNF sha256 682845346dd1...04840f7c; one thread): result SATISFIABLE after 85 s, maximum resident set 94,281,728 bytes (2^26.49; /usr/bin/time -v), and the model satisfies all 771,857 clauses with all 132,265 variables assigned (`verify_model.py`). The same run under `--as=117440512` (112 MiB) aborts after 39 s with "out-of-memory reallocating from 16777216 to 33554432 bytes" and no result. So this run fits 2^28 bytes and not 112 MiB. This is a stand-in instance (H.2), and one seed.

**H.6b. Rows 16 to 22 over the good pairs of one first block (a program check for H3).** The filed counted program (`lowm.py` `process_cv`, all 222 classes) on 1,173,546 first blocks drawn from SHAKE-256 seeds `h3rows|b1..b3`, with `step3b` replaced by a recorder that runs rows 16..36 for every l of every row-16 survivor without stopping at the first success. Counted: first blocks with a good pair 88,146; good pairs 978,760,264; row-16 survivors (pair, l) 477,777. For each row r the number of distinct good pairs that reach row r, and the number of unordered pairs of distinct good pairs of the same first block that both reach it, against the number expected if the pairs reached the row independently with the pooled rate (rate squared times the number of same-block pairs, 11,683,584,591,945):

| row reached | pairs reaching | same-block pairs observed | expected if independent |
|---|---:|---:|---:|
| 16 | 468540 | 2688811 | 2.677e+06 |
| 17 | 108 | 2 | 0.1423 |
| 18 | 1 | 0 | 1.22e-05 |
| 19 | 0 | 0 | 0 |
| 20 | 0 | 0 | 0 |
| 21 | 0 | 0 | 0 |
| 22 | 0 | 0 | 0 |
| 36 | 0 | 0 | 0 |

Reading, without a statistic: the observed same-block count at row 16 is 1.00 times the independent expectation (7319bba measured 0.98 and 1.00 for the row-16 factor on 2^21 and 2^23 first blocks); at the later rows the counts are row 17: 2 observed against 0.142 expected; row 18: 0 observed against 1.22e-05 expected. The row-17 count is two events against about 0.14 expected; two events cannot be read as a rate, but if it is a real excess it is a factor of about 14 over independence, against the factor rho <= 2^35 that H3 allows; it is reported as found and is a reason for the thin-margin wording of H3, not a measurement of rho. This cannot show H3 at the claimed scale: the rows beyond 17 have too few events to say anything, and the premise concerns about 2^55.76 first blocks.

**H.6c. The first-block measurement extended (a check for H1).** The program `h1ext.c` (our C, 43 lines; the attack's own filters: the 37-step compression of 16 random words from xoshiro256** seeded 900001..900004, the 222 W7 class tests F7(c7 - x) and the scalar W6 test F6(w6of(a0, x, A_-2)) of every variant of every passing class, with the constants and the 782,800 variants written from the filed `lowm.py`; cross-checked against `lowm.py` on the first 30 blocks of seed 7: identical x, A_-2, passing classes and good pairs) on 2,147,483,648 first blocks (2^31.0) in four processes. Passing classes per first block 3.52287 against the exact 3.52295 (ratio 0.99998, relative standard error of the mean from the per-block variance 0.00006, variance-to-mean ratio 28.8); good pairs per first block 830.970 against the exact 830.988 (ratio 0.99998, relative standard error 0.00011, variance-to-mean ratio 23051). The four runs' good-pair ratios: 900001: 0.99993, 900002: 1.00008, 900003: 0.99988, 900004: 1.00002. The 256 buckets of the top byte of x and of C6 - A_-2 over the same blocks deviate from the mean count by -0.00094 to 0.00108 and -0.00106 to 0.00087 (relative; the Poisson spread would be +-0.00035 (one sd)). This is the same kind of evidence as in Section 13.1, 2^31.0 instead of 2^23 blocks, and it tests the means of the class and good-pair counts and the uniformity of two words, not the joint law and not 2^55.76 blocks.

### H.7 Organizer experiments added, and what they cannot show

The experiment budget is 65,536 bytes in total; `lowm.py` uses 63,351, so two more entries share one 1,792-byte program `experiments/nonce_h1h3.py`. Each trial takes 150 first blocks from the organizer's trial seed (SHAKE-256 of seed and counter), computes the real 37-step compression (the program computes its 37 round constants as integer cube roots of the first 37 primes), and tests, for the first class of the family (c7 = cc8e8c4c) and four of its variants (1c354142, 1c6bc14a, 1ce981ca, 1db781c2), whether W7x = c7 - x is in F7 and W6x is in F6 (the filters of Section 5.1 in their definition form). It returns no message pair, so the event full-collision never succeeds by design. Observations: first blocks, W7 passes, W6 passes over the four variants, first blocks in which two or more variants pass F6, first blocks with both a W7 pass and a W6 pass, and the sum over those blocks of the number of variants passing. The entry `h1-cv1-filters-nonce` is the H1 consequence (the pass rates of the two filters on real chaining values: p7 = 2^-5.98 per class and p6 = 2^-3.90 per variant); the entry `h3-cowpass-nonce` reports the number of first blocks in which two or more of the four variants of one class pass F6. Independent variants would give 0.0246 of the first blocks; the replay gives about 2.9 times that, because the variants of one class share most of their bits. This is the within-class correlation of the W6 filter (it is why the counts per first block are overdispersed, Section 13.1); the ledger uses only expectations, which correlation does not change, and H3 itself is about later rows, which this entry does not test. The program was cross-checked against `lowm.py` on two trials (identical counts). Local replay of 256 trials: 38,400 first blocks: 625 W7 passes (609 at the exact rate), 10,222 W6 passes over the four variants (10,275 at the exact rate), 2,720 first blocks with two or more variants passing F6 (945 if the variants were independent), 110 first blocks with both a W7 pass and a W6 pass; seeds s0..s255 of our local replay (the organizer's own seeds differ).

What they cannot show: the organizer's report discards participant observations from the judge's view and keeps only message pairs it can check against the target, and this program returns none; a judge therefore sees the program and the organizer's note that it returned no pair, not the counts. The counts are a program check that anyone can replay; they are not evidence about q3, about rows beyond the W6 filter, about independence across 2^55 first blocks, or about cost. The four variants are not drawn at random from the family and the two entries do not test row 16 or later rows, where H3 has its weight. No statistic is claimed.

### H.8 What is not in the package

`q3smc.c`, `gen_consts.py`, `analyze.py` and `check_alt.py` are in this proof (Appendix F) as text, with the hashes of the files that were run (Appendix F.1 and G.1); they are not experiment files, because lowm.py leaves 2,185 bytes of the 65,536 and q3smc.c alone is about 9 KB. The measurement sources of H.6 (`h1ext.c` 575b7d41a3ceb7fa, `h3rows.py` b60c04dfd5311d10, `export_consts.py` 9216870509f13fe2, `h1ext_check.py`, `q3ub.py`) are not in the package either; their hashes (sha256 of the files as run) are given so that the numbers can be tied to them. No second independent q3 estimator and no extended H1 run to 2^26 beyond what H.6c reports were made.

## Appendix I. Refile R37ZF5: the rulings on 96933f8e and 4939fc06 and what changed

**The ruling on 96933f8e (R37ZF3, refuted).** Its fatal finding in lane_cost, quoted: F-COST-001 (cost_omission, fatal): "The submission removes the construction cost and peak memory of the published characteristic and semi-free-start input, contrary to collision-frontier-v5's requirement to account for construction of nonuniform collision material even when omitted from the submitted program. Consequently the declared total time, preprocessing, memory maximum, and derived score are incomplete." The same lane's obligations time_bound, memory_bound and data_preprocessing_advice were fatal for the same reason ("Publication does not waive the model requirement to account for construction of stored nonuniform collision material"; for the bound on the construction phase the ruling states that none is given). The benchmark text it cites (benchmark.cost_model:/nonuniform_advice): "A stored precomputed collision is not a cheap construction. All construction/preprocessing and advice must be accounted for, including any search omitted from the submitted program."

**What changed, each change against one quoted sentence** (nothing else changed relative to R37ZF4, whose program, cells, operation counts, exact end event, N_FB and V_MAX are kept):
1. "removes the construction cost ... of the published characteristic and semi-free-start input" -> the construction is charged: A_C = 2^60 is a term of the ledger again (Section 11, 11.2, Appendix B, H.3); time_log2 58.67798 -> 60.4854 (`python3 experiments/lowm.py ledger`: `ledger()` has the term A_C = 2^ac_log2, default 60, the only change to `lowm.py`); preprocessing 2^50.00141 -> 2^60.00141. H4 (advice allowances) is a premise again.
2. "construction cost and peak memory of the published characteristic and semi-free-start input" (the second half) -> the construction is a phase of the memory bound (Section 14.1, H.2): the generator, the translation, the STP CNF dump and the solver on the real 37-step dense model were run under `prlimit --as=536870912` or the 2^28 cap and their peaks are listed; the largest, the STP dump, is 499,384,320 bytes (2^28.895), so memory_log2_bytes 28 -> 29 and the memory term 8 -> 9. H6 is a premise again.
3. "the declared total time, preprocessing, memory maximum, and derived score are incomplete" -> claim.json: time_log2 60.4854, preprocessing_log2 60.00141, memory_log2_bytes 29; score 60.4854 + 9 = 69.4854.
4. F-CRYPT-005 / F-EVAL-003 (minor; "The proof gives inconsistent sensitivity values for lowering q3 by one bit") -> every statement of that sensitivity now reads 60.84571 (Sections 11, 15, H.5).

| finding id (96933f8e) | severity | answer | where |
|---|---|---|---|
| F-COST-001 | fatal | The construction of the characteristic and SFS pair is charged, in time (A_C = 2^60) and in memory (2^29). | Sections 11, 11.2, 14.1, Appendices B, H.2, H.3 |
| F-COST-002 | material | Unchanged for A_S and DEV ("converted from CPU-seconds using a calibration attributed to another filing"). A_C uses the same calibration and is stated as an allowance. | Section 11.2, H4 |
| F-COST-003 | material | Unchanged: H5 stays a premise. | Section 12 |
| F-CRYPT-001, F-CRYPT-002, F-CRYPT-003 | material | Unchanged (H1, H2, H3 stay premises with their sensitivity tables, recomputed for the new ledger). | Section 12, H.5 |
| F-CRYPT-004 | minor | Unchanged: the Bonferroni sum uses the weighted average. | Section 10 |
| F-CRYPT-005, F-EVAL-003 | minor | One value for the one-bit sensitivity of q3 everywhere: 60.84571. | Sections 11, 15, H.5 |
| F-EVAL-001, F-EVAL-002, EXP-001, EXP-002, EXP-003, EXP-004 | material | Unchanged: the q3, H1 and H3 evidence is ours and is labelled so; the organizer experiments are functional checks. | Appendices F, G, H.6, H.7 |

**The ruling on 4939fc06 (R37ZF2, not_evaluable)** had two reasons in lane_experiments, `H4-advice-allowances` and `H6-characteristic-search-memory`, with the finding EXP-005: "The organizer executions authorize no attack-cost inference and do not run the characteristic search. Consequently the 2^60 preprocessing allowance, full bit-sliced operation ledger, and 2^28 all-phase memory envelope are not empirically validated by the trusted report; the actual characteristic-search time and memory remain unmeasured." R37ZF3 and R37ZF4 removed both premises, and 96933f8e was refuted for the omission, so both are restored here with what the first filing lacked:
- H6: the memory of the construction is now measured where it can be (generator, translation, CNF dump, and the solver to 2^22 conflicts; H6, H.2), and the bound is 2^29 because the measured STP dump exceeds 2^28. The completion of the search under the cap is not measured and is stated in H6 as a limit.
- H4: A_C = 2^60 is still an allowance, not a measurement. We did not complete a re-run of the search, and that is stated in H4 and H.3. No organizer experiment can run the search (experiment kinds and the 20 s limit), so none is added.

| finding id (4939fc06) | severity | answer | where |
|---|---|---|---|
| F-COST-001 | material | "The dominant A_C=2^60 preprocessing term is an allowance, not a measured upper bound for the actual characteristic search": still true and stated; A_C = 2^60 is charged as a labelled allowance with a sensitivity table. | Sections 11, 11.2, H.3, H.5 |
| F-COST-002 | material | "it is inferred from stand-ins, while some alternative solver settings exceeded the claimed envelope": the generator, the translation, the CNF dump and the solver are now measured on the real 37-step dense model, not on stand-ins, and the bound is 2^29; the completion of the search is not measured (stated). | H6, H.2 |
| F-COST-003, F-COST-004 | material | Unchanged: H1-H3 and H5 stay premises. | Section 12 |
| F-H1-EXTRAPOLATION, F-H2-STATISTICAL-COVERAGE, F-H3-LATE-ROUND-DEPENDENCE, F-EVAL-001, EXP-001, EXP-002, EXP-003, EXP-004 | material | Unchanged. | H.4, H.5, H.6, Appendices F, G |
| F-H3-QUANTIFIER-WORDING | minor | The Bonferroni sum uses only the weighted average; the per-trial form is a sufficient condition for it. | Section 10 |
| F-EVAL-002, EXP-005 | material | "The actual characteristic-search computation was not rerun or measured": measured where possible (H6, H.2); the search time stays an allowance (H4, H.3). | H.2, H.3 |

## Appendix J. Refile R37ZF4 (the exact end event, kept in R37ZF5): what changed vs 96933f8e

96933f8e (R37ZF3, claimed 59.98193, refuted for F-COST-001) is the base of this change; it is in the dependency list. One change of the algorithm and its consequences, with the terms of R37ZF4 before the charge of Appendix I:

| item | 96933f8e | R37ZF4 (before the charge of Appendix I) |
|---|---|---|
| event accepted at rows 22..36 | every cell and printed two-bit condition | replay of rows 22..36 on the raw schedule words; accepted iff the eight registers agree after step 36 (Section 7.4d) |
| `experiments/lowm.py` | | `step3b` (the cell test for t < 22 only, then the register comparison) and `Q3_LOG2` |
| q3 used (H2) | 2^-71.47 (q3_cell) | 2^-70.16 = log2 LB_cell + log2 LB_ratio (Section 7.4d, Appendix K) |
| q3 upper bound (H3 only) | 2^-71.38 (delta <= 2^-10.34) | 2^-70.06 (delta <= 2^-9.71 against 2^-9.4; Appendix H.4) |
| N_FB | 60,951,875,249,131,685 | 24,650,628,322,256,370 |
| V_MAX | 2,808,743,648,446,227,477,989 | 1,135,933,807,571,123,291,014 |
| mu0, Pcap | 0.49558494, 0.00056206 | 0.49694499, 0.00138975 |
| time_log2 | 59.98193 | 58.67798 (60.4854 with A_C, this filing) |
| operation counts, ROWCOMP, ROWCHECK, success floor 0.39 | | unchanged (preprocessing and memory: Appendix I) |

The sensitivity tables (H.5) and the ledger code (Appendix B) are recomputed. The counted program, the cells of rows 0..21, the classes and all operation counts are those of 96933f8e.

## Appendix K. The exact/cell study: program and runs

Files (working directory of the study): `smc_r16x.c` sha256 42a309bf41b6a07c228c5cba108923f804896f233ff5492cb66ae7d1d55fc105, `lab.h` sha256 bdefd6747d41727a378bc124c241db1f635275d3a2901b96a1c6c6b0e5c5e456 (constants of the characteristic and the row functions, written by us from the paper's tables as transcribed in this package), the variant list `allg_classes.txt` (one line `g 12103680` followed by the 12,103,680 values of a0 of the family G in hexadecimal, sha256 05d967567f56d5c61359e21156397da2cf5b995f477f91254d2b643facc77319, 108,933,131 bytes; it is not in the package; its 782,800 members that lie in the 222 classes are the variants of this filing, `experiments/lowm.py` lists them). Build A: `gcc -O2 -DFFBE_RELAX -DR16X smc_r16x.c -lm`; control build B: `gcc -O2 smc_r16x.c -lm`. Run: `./smc seed 8192 512 8192 allg_classes.txt 0`. Cloud runs: seeds 20001..20128 and 30001..30128 (build A), 9001..9004 (build B), 12 processes. Output per seed: `n`, `cellevent`, `exact`, `cell_not_exact` and a line RESULT with the three log2 values.

### K.1 smc_r16x.c

```c
/* smc.c - sequential Monte-Carlo estimator of q3 (37-step SHA-256 second block, rows 16..36), variant-W8 tail.
   usage: smc seed NP M MT classes.txt      |      smc -t classes.txt   (self tests) */
#include "lab.h"
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
  P0=malloc(32*sizeof(P)); long cap=1<<21; pairE=malloc(cap*4); pairL=malloc(cap); NPAIR=0;
  u32 M16=CELL[1][16].m,V16=CELL[1][16].v,fr=~M16;
  for(int l=0;l<32;l++){ setup_l(&P0[l],l); P s=P0[l];
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
  P *pop=malloc((size_t)NP*sizeof(P)),*pop2=malloc((size_t)NP*sizeof(P)); Rec*rec=malloc((size_t)NP*M*sizeof(Rec));
  double est=(double)NPAIR/32.0/4294967296.0;
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

### K.2 lab.h

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
static const u32 CV0[8]={0x63b4986c,0x35d83dc0,0xc98894e4,0x784e08fc,0x78a7f752,0x5ed877a8,0x315a2db3,0xd5614eb4};
static const u32 MX[16]={0x4d7f86ff,0x32ece589,0xd8accfc4,0x2cc2e433,0x068b5b34,0xeba68a28,0x0fe12cad,0x6ee2630c,
 0xbf0d78e1,0x6d1a90dd,0xfaa1d3e0,0x56aed439,0xcc2dbbc2,0xdd2ba0fc,0xbd1d3f7b,0x7dd43a81};
static const u32 MY[16]={0x4d7f86ff,0x32ece589,0xd8accfc4,0x2cc2e433,0x068b5b34,0xeba68a28,0x2fe12cad,0x6aa26b0c,
 0x9f0d78e1,0x681b8277,0xfaa9c7e0,0x56aed439,0xcc2dbbc2,0xdd2ba0fc,0xb95d377b,0x5dd43a81};
static const u32 W14X=0xbd1d3f7bu;
static const u32 LW15[32]={0x7dd41680,0x7dd41681,0x7dd416a0,0x7dd416a1,0x7dd41a80,0x7dd41a81,0x7dd41aa0,0x7dd41aa1,
0x7dd43680,0x7dd43681,0x7dd436a0,0x7dd436a1,0x7dd43a80,0x7dd43a81,0x7dd43aa0,0x7dd43aa1,
0xfdb41680,0xfdb41681,0xfdb416a0,0xfdb416a1,0xfdb41a80,0xfdb41a81,0xfdb41aa0,0xfdb41aa1,
0xfdb43680,0xfdb43681,0xfdb436a0,0xfdb436a1,0xfdb43a80,0xfdb43a81,0xfdb43aa0,0xfdb43aa1};
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
