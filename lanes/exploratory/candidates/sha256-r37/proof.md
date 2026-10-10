# Collision attack on 37-step SHA-256: the ePrint 2026/1120 two-block attack with 222 classes of A0-variants and an x-indexed table of W6 fibres, 2^61.68435 (one-change derivative of d3ec5c41)

Track `sha256-r37-exploratory`, target `sha256-r37-prefix-v1`, cost model `collision-frontier-v5` (C = 2644).
Claim: `time_log2 = 61.68435` target compressions on every run, success probability at least 0.39 (0.3900000003 under the stated premises),
memory 2^50.0 bytes (reported only), nonuniform advice below 2^13 bytes.

The attack is the 37-step collision attack of Li, Zhang, Li, Liu, Qian and Zhu, "Pushing Collision Attacks on SHA-2 to 39 Steps" (IACR ePrint
2026/1120, CC BY), in the two-block framework of [LLWS26] (ePrint 2026/1080), with the A0-variants of its Step-1 solution (itseasypop 1c368173,
qkniep b947b377), the 222 classes and packed good-pair stage of 1f12a09a, the exact-rational ledger of 087a18c4 and the program structure of
7319bba (all declared as dependencies). **What this filing changes is the counted online program and its precomputation, not the attack.**
The 32-bit value x = A_{-1} of a chaining value takes only 2^32 values, while the run draws about 2^58.3 first blocks: every x recurs about
2^26 times. Everything that depends on x alone is therefore computed once for all x (charged preprocessing, below 2^58 operations; memory is a
reported metric only) and read online: (i) the W7 class test becomes one table read, replacing the 191-operation decision DAG; (ii) for every
passing class, the values phi(a0, x) = W6x - cb of its ~3,500 variants are partitioned into **fibres** of equal value (on average only 293.2 distinct
values per class, 12.0 times fewer than variants; measured, Section 13.3), and the online W6 filter is one bit-sliced 32-bit addition of the scalar cb to the
fibre values of up to 256 lanes followed by the F6 test (200 counted operations per batch of 256 fibres; 1.547 batches per passing class on average, against
14 to 15 batches of variants in the earlier filings); (iii) the members of every passing fibre are read as a contiguous block, so the 8-operation scan-and-gather
per good pair of the earlier filings becomes about 14 operations per passing fibre plus the packed arithmetic. The attack, the good pairs, q3 and the packed
row-16 stage are unchanged; the set of good pairs found is *identical* to the earlier filings' (Lemma 8.1, checked against brute force in Section 13).
**Inheritance, stated up front:** the Monte-Carlo estimate of q3 (premise H2) and the evidence for H3 are 7319bba's and were *not* re-run for this filing; the table changes how the good pairs are found, not which pairs are good.

**This derivative.** Everything in this file except this paragraph, Appendix B and the passages it lists is the text of submission d3ec5c41 (companygardener, 61.71473),
and "I", "this filing" and "new" in that text refer to d3ec5c41. One thing is changed: the row-16 stage looks up the l-mask of u in a direct table
Rmask[u] (one load) instead of a bitmap probe followed by a binary search of the sorted (u, l) array. The lookup returns 0 exactly when the bitmap
bit was clear and otherwise exactly the mask the binary search returned (Lemma B.1), so every good pair, row-16 pass, output and premise is the same;
only the counted cost falls: 5 or 6 operations per lookup instead of 8 or 9, and no 132-operation search per member. Every figure that depends on
the ledger was recomputed with `ledger()`; the exact numerator, the certificate and the equivalence runs are in Appendix B.

## 0. Summary

- **Algorithm (Sections 4-8).** Messages M0 || M1 and M0 || M1' (128 bytes; padding adds the same third block). A first block M0 is two fresh uniform 256-bit
  words; CV1 = F_37(IV, M0) costs one unit. One table read at x = A_{-1} returns the list of the classes (among 222 fixed classes of 3456..3600 variants,
  782,800 variants in total) whose W7 test c7 - x in F7 passes, and for each of them the record of Section 8.2. For each batch of the record the program
  adds cb = C6 - A_{-2} to the fibre values bit-sliced and applies F6; the members of each passing fibre are good pairs. They are processed in packed groups of four:
  u = W0 + s0(W1), a presence word, and an exact row-16 table lookup over the 32 elements of L*; each row-16 pass is checked through row 36. A pair that follows
  every cell of rows 16..36 collides; it is verified with the target and output.
- **Rates (exact under H1).** Per first block: 222 p7 = 3.5229 passing classes and g = 782,800 x p7 x p6 = 830.99 good pairs
  (p7 = |F7|/2^32 = 2^-5.97763, p6 = |F6|/2^32 = 2^-3.90197).
- **Probability (Section 7, H2).** q3 = average over the 782,800 variants and l in L* of Pr[rows 16..36 follow every cell and printed two-bit condition]
  = at least 2^-74.03 (the registered floor of the preregistered studies of 7319bba, Section 7.4; not re-run here).
- **Cost (Sections 9, 11).** N_FB = 358,768,880,796,199,274 first blocks (2^58.31583); per first block 1 unit plus 51 counted operations, plus on average
  15859.09 counted data-dependent operations (10,524 for the fibre tests, scans and the packed arithmetic of the member blocks, 5,200 for the presence words and lookups,
  113.8 for rows >= 16), capped by V_MAX. T = A_C + A_S + DEV + N_FB + (N_FB x 51 + V_MAX + overshoot + preprocessing + final)/C + 6 = 9,797,125,415,937,815,688,179 / 2644 = 2^61.684342,
  claimed 61.68435. The base d3ec5c41 claims 61.71473 (7.23 units per first block) and 7319bba 62.34263 (13.08 units); 7.02 units here.
- **Premises (Section 12).** H2 and H3 are inherited from 7319bba and not re-run. H1 uniform independent chaining values; H2 q3 >= 2^-74.03; H3 given one success, at most 2^-9.4 further expected successes in the same
  first block; H4 advice allowances (A_C = 2^60, A_S = 2^50, DEV = 2^40, as in the accepted filings); H5 counted word-RAM pricing (every executed primitive costs one; tables are
  addressable memory; the program text is straight-line code); H7 the exact success floor of 087a18c4; **H9 (new) the table statistics and the preprocessing bound**.
  No decision-DAG branch pricing is used, so the premise H5 of 7319bba (branch = one primitive for DAG paths) and its conditional-law premise H8 do not occur.
- **Checks (Section 13).** Exhaustive in Tungsten: |F6| = 287,309,824 and |F7| = 68,157,440 and their bitwise forms against the definitions on all 2^32 words (0 mismatches),
  |G| = 12,103,680, the 222 classes (782,800 variants); the table pipeline against brute-force filtering (selftest and organizer experiments, 0 mismatches); the fibre statistics
  of all 222 classes; the executable counted program measured on 160,000 real first blocks against the ledger; 127 of 128 37-step semi-free-start constructions with variants, 16 of 16 found by the counted program.

## 1. Target, cost model and output

- **Target** sha256-r37-prefix-v1: SHA-256 steps 0..36 on every padded block, the standard IV once, FIPS 180-4 padding, feed-forward, all eight digest words
  (repository `verifier/hash_functions.digest(m, "sha256", 37)`). The output is two distinct complete messages with equal digests, verified with the target before output.
- **Cost model** collision-frontier-v5: one 37-step target compression = 1 unit; every other executed 256-bit word-RAM primitive (load, store, add/sub, and/or/xor/not,
  shift/rotation, compare, branch, uniform random word) = 1/C unit with C = 2644. Immediates and shift amounts are instruction fields; 64 registers. Memory is reported
  only. Success must be at least 0.39 over fresh coins.
- **Notation.** In step i, E_i = A_{i-4} + E_{i-4} + S1(E_{i-1}) + CH(E_{i-1}, E_{i-2}, E_{i-3}) + K_i + W_i and A_i = E_i - A_{i-4} + S0(A_{i-1}) + MAJ(A_{i-1}, A_{i-2}, A_{i-3}) (mod 2^32);
  (A_{-1..-4}, E_{-1..-4}) = (a, b, c, d, e, f, g, h) of the incoming chaining value. F_R(cv, B) is the R-step compression with feed-forward; its output is
  cv + (A_{R-1}, A_{R-2}, A_{R-3}, A_{R-4}, E_{R-1}, E_{R-2}, E_{R-3}, E_{R-4}).

## 2. Sources, credit, and what is new

- [LZLLQZ26] Y. Li, Z. Zhang, M. Li, F. Liu, H. Qian, J. Zhu, "Pushing Collision Attacks on SHA-2 to 39 Steps", IACR ePrint 2026/1120: the 37-step characteristic (Table 15), its two-bit
  conditions (Table 16), the 37-step SFS pair (Table 17) and the three-step attack (Step 1: SAT solve of the dense part, 2^41.3; Step 2: random first blocks filtered on W6, W7; Step 3: the
  (W14, W15) freedom). [LLWS26] Y. Li, F. Liu, G. Wang, J. Shi, ePrint 2026/1080 (the framework); [LLW24] EUROCRYPT 2024 (the tool).
- Filings on this track, all declared as dependencies: 6c77089c (winglock, 74.22669): transcription of Tables 15-17, member orientation, the reading of '+', the corrected two-bit condition
  A15[29] = A17[29], the exact Step-2 sets F6, F7, the exact set L* (|L*| = 32), the SMC design for q3. dd6656d (Th0rgal): affine decomposition of F6, F7. 1c368173 (itseasypop) and b947b377 (qkniep):
  the A0 freedom of the Step-1 solution (the family G), the c7 classes. 087a18c4 (GordoAR): exact-rational ledger, premises H1-H5, H7, the first-block-level success analysis. 1f12a09a (0xshikhar):
  the 222 classes with at least 3456 variants, packed groups of four 64-bit lanes, the presence word. 7319bba (winglock, 62.34263): the program structure, the packed good-pair program, the
  q3 studies for the 222-class family (Section 7.4), the end-to-end and replay statistics (Section 13.1, quoted), the registered allowances. 6eeefb64 (sha256-r32, promoted): the calibrated price of a solver CPU-second
  behind A_C.
- **How the earlier material is used.** Sections 3-7 restate definitions and lemmas that all filings share (re-typed; every constant was re-derived or re-checked here, Section 13). The Monte-Carlo estimate of q3
  (Section 7.4) and the statistics of Section 13.1 were produced by 7319bba's author with programs reproduced in Appendix A.5-A.7; **I did not re-run them**, and they enter only as the premises H2 and H3.
  I did not execute any peer code: every program that ran for this filing was written for it (Python `experiments/xtab.py`, Tungsten sources of Appendix A.1-A.3).
- **New here.** (i) The x-indexed table and the partition of each passing class into fibres of equal W6 value (Sections 8.2, 8.4); (ii) the fibre test: one bit-sliced addition of cb to the fibre values and F6 (Section 9.4),
  with an exact operation count independent of the data; (iii) the scan of passing fibres and the processing of their member blocks in place (Sections 9.5, 9.6); (iv) the offline algorithm, its exact operation bound and
  memory (Sections 8.2, 14); (v) the fibre statistics of all 222 classes by Tungsten sampling (Section 13.3); (vi) the new ledger (Section 11); (vii) exhaustive Tungsten checks of F6, F7 and |G|.

## 3. The characteristic (from the paper, as transcribed in 6c77089c; re-checked by `experiments/xtab.py`)

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
with x = M', y = M (`experiments/xtab.py` rebuilds both members and checks the cells; the repository
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
(each step inverted for its new coordinate). W8..W13 do not depend on CV1. *Proof.* Substitution; `xtab.py`
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
W8x[8] != W8x[25], W8x[14] = W8x[18]}**. Exhaustive count over the 2^29 values of E4 with E4[31:29] = 000 (a0 = E4 - C4 is a bijection; Tungsten, Appendix A.1):
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
(exhaustive over all 2^32 words, Tungsten, Appendix A.2; the counts of 7319bba's `f6chk.c` are reproduced). By the carry pattern of w + d (s0 is linear), each set is a disjoint union of
affine spaces. We use them in the following bitwise form, **checked against the definition on all 2^32 words**
(Tungsten, Appendix A.2: about 10 CPU-minutes, zero mismatches for both):

```text
F6: w is NOT in F6  iff  common | (w29 & (bc | (w30 & X)))  with
      common = (w14^w18) | ~(w8^w25) | (w1^w12),   bc = (w15^w19) | ~(w9^w26) | (w2^w13),
      X = (w16^w20^w31) | ~(w10^w27^w31) | (w3^w14^w31)                                  (bits are w_i; | is OR)
F7: w is in F7  iff  w1 = w18, w0 = w28, w9 = w30 and
      [ w11 = 0, w22 = 1, w26 = 1 ]                                                       2^26 words
      or [ w11 = 1, w12 = 0, w22 = 0, w23 = 1, w26 = 0, w27 = 1, w2 = w19, w1 = w29, w10 = w31 ]   2^20 words
```

(F6 is the form published in 087a18c4/1c368173 with b_bad & c_bad simplified to bc | (w30 & X); 7319bba derived the F7 constraint
set from the affine hull of F7 and of its two halves (Appendix A.3); here it is verified
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

### 5.3 The c7 classes and the selection (1f12a09a's selection)

c7(a0) takes only **22,976 distinct values on G** (7319bba's enumeration, inherited). A *class* is G intersected with one
value of c7. For all variants of one class and a given CV1, W7x is the same word, so one membership test decides the
W7 filter of the whole class. The class sizes are at most 3600; the sizes 3600 (85 classes), 3584 (26) and 3456 (111)
are the only ones above 2751. **The 222 classes with at least 3456 variants are used** (782,800 variants), as in 1f12a09a and 7319bba; the selection is kept and not re-optimised here (the marginal cost per variant of a class of s variants is dominated by the same u-stage cost per good pair, Section 11.3). Each class equals {base XOR s : s subset of mask, s in G, c7 = the class value}
for the descriptors below (c7, base, mask, size; `xtab.py` regenerates all 222 classes from them and asserts the sizes; Tungsten re-derives the class of the first descriptor and the sizes of all 222):

```text
cc8e8c4c 1c010142 01fec08d 3456  |  cc8e8c5c 1c010112 01fec08d 3456  |  cc8e8c6c 1c010122 01fec08d 3456
cc8e8c7c 1c010132 01fec08d 3456  |  cc8e8c8c 1c010102 01fec08d 3456  |  cc8e8e1c 1c010352 01fec08d 3456
cc8e8e2c 1c010362 01fec08d 3456  |  cc8e8e3c 1c010372 01fec08d 3456  |  cc8e8e4c 1c010342 01fec08d 3456
cc8e8e5c 1c010312 01fec08d 3456  |  cc8e8e6c 1c010322 01fec08d 3456  |  cc8e8e7c 1c010332 01fec08d 3456
cc8e8e8c 1c010302 01fec08d 3456  |  cc8e901c 1c010152 01fec48d 3456  |  cc8e902c 1c010162 01fec48d 3456
cc8e903c 1c010172 01fec48d 3456  |  cc8e904c 1c010542 01fec08d 3456  |  cc8e905c 1c010512 01fec08d 3456
cc8e906c 1c010522 01fec08d 3456  |  cc8e907c 1c010532 01fec08d 3456  |  cc8e908c 1c010502 01fec08d 3456
cc8e9228 1c010760 01fec09d 3456  |  cc8e9238 1c010760 01fec09d 3456  |  cc8e9248 1c010740 01fec09d 3456
cc8e9258 1c010700 01fec0dd 3456  |  cc8e9268 1c010720 01fec09d 3456  |  cc8e9278 1c010720 01fec09d 3456
cc8e9288 1c010700 01fec09d 3456  |  cc8e9448 1c010940 01fec09d 3456  |  cc8e9458 1c010900 01fec0dd 3456
cc8e9468 1c010920 01fec09d 3456  |  cc8e9478 1c010920 01fec09d 3456  |  cc8e9488 1c010900 01fec09d 3456
cc968c4c 1c010142 01fec08d 3600  |  cc968c5c 1c010112 01fec08d 3600  |  cc968c6c 1c010122 01fec08d 3600
cc968c7c 1c010132 01fec08d 3600  |  cc968c8c 1c010102 01fec08d 3600  |  cc968e1c 1c010352 01fec08d 3600
cc968e2c 1c010362 01fec08d 3600  |  cc968e3c 1c010372 01fec08d 3600  |  cc968e4c 1c010342 01fec08d 3600
cc968e5c 1c010312 01fec08d 3600  |  cc968e6c 1c010322 01fec08d 3600  |  cc968e7c 1c010332 01fec08d 3600
cc968e8c 1c010302 01fec08d 3600  |  cc96901c 1c010152 01fec48d 3600  |  cc96902c 1c010162 01fec48d 3600
cc96903c 1c010172 01fec48d 3600  |  cc96904c 1c010542 01fec08d 3600  |  cc96905c 1c010512 01fec08d 3600
cc96906c 1c010522 01fec08d 3600  |  cc96907c 1c010532 01fec08d 3600  |  cc96908c 1c010502 01fec08d 3600
cc969228 1c010760 01fec09d 3584  |  cc969238 1c010760 01fec09d 3584  |  cc969248 1c010740 01fec09d 3584
cc969258 1c010700 01fec0dd 3584  |  cc969268 1c010720 01fec09d 3584  |  cc969278 1c010720 01fec09d 3584
cc969288 1c010700 01fec09d 3584  |  cc969448 1c010940 01fec09d 3584  |  cc969458 1c010900 01fec0dd 3584
cc969468 1c010920 01fec09d 3584  |  cc969478 1c010920 01fec09d 3584  |  cc969488 1c010900 01fec09d 3584
ce8e8d1c 1e010052 01fec08d 3456  |  ce8e8d2c 1e010062 01fec08d 3456  |  ce8e8d3c 1e010072 01fec08d 3456
ce8e8d4c 1e010042 01fec08d 3456  |  ce8e8d5c 1e010012 01fec08d 3456  |  ce8e8d6c 1e010022 01fec08d 3456
ce8e8d7c 1e010032 01fec08d 3456  |  ce8e8d8c 1e010002 01fec08d 3456  |  ce8e8f1c 1e010252 01fec08d 3456
ce8e8f2c 1e010262 01fec08d 3456  |  ce8e8f3c 1e010272 01fec08d 3456  |  ce8e8f4c 1e010242 01fec08d 3456
ce8e8f5c 1e010212 01fec08d 3456  |  ce8e8f6c 1e010222 01fec08d 3456  |  ce8e8f7c 1e010232 01fec08d 3456
ce8e8f8c 1e010202 01fec08d 3456  |  ce8e911c 1e010452 01fec08d 3456  |  ce8e912c 1e010462 01fec08d 3456
ce8e913c 1e010472 01fec08d 3456  |  ce8e914c 1e010442 01fec08d 3456  |  ce8e915c 1e010412 01fec08d 3456
ce8e916c 1e010422 01fec08d 3456  |  ce8e917c 1e010432 01fec08d 3456  |  ce8e918c 1e010402 01fec08d 3456
ce8e931c 1e010652 01fec08d 3456  |  ce8e932c 1e010662 01fec08d 3456  |  ce8e933c 1e010672 01fec08d 3456
ce8e934c 1e010642 01fec08d 3456  |  ce8e935c 1e010612 01fec08d 3456  |  ce8e936c 1e010622 01fec08d 3456
ce8e937c 1e010632 01fec08d 3456  |  ce8e938c 1e010602 01fec08d 3456  |  ce8e9528 1e010860 01fec09d 3456
ce8e9538 1e010860 01fec09d 3456  |  ce8e9548 1e010840 01fec09d 3456  |  ce8e9558 1e010800 01fec0dd 3456
ce8e9568 1e010820 01fec09d 3456  |  ce8e9578 1e010820 01fec09d 3456  |  ce8e9588 1e010800 01fec09d 3456
ce968d1c 1e010052 01fec08d 3600  |  ce968d2c 1e010062 01fec08d 3600  |  ce968d3c 1e010072 01fec08d 3600
ce968d4c 1e010042 01fec08d 3600  |  ce968d5c 1e010012 01fec08d 3600  |  ce968d6c 1e010022 01fec08d 3600
ce968d7c 1e010032 01fec08d 3600  |  ce968d8c 1e010002 01fec08d 3600  |  ce968f1c 1e010252 01fec08d 3600
ce968f2c 1e010262 01fec08d 3600  |  ce968f3c 1e010272 01fec08d 3600  |  ce968f4c 1e010242 01fec08d 3600
ce968f5c 1e010212 01fec08d 3600  |  ce968f6c 1e010222 01fec08d 3600  |  ce968f7c 1e010232 01fec08d 3600
ce968f8c 1e010202 01fec08d 3600  |  ce96911c 1e010452 01fec08d 3600  |  ce96912c 1e010462 01fec08d 3600
ce96913c 1e010472 01fec08d 3600  |  ce96914c 1e010442 01fec08d 3600  |  ce96915c 1e010412 01fec08d 3600
ce96916c 1e010422 01fec08d 3600  |  ce96917c 1e010432 01fec08d 3600  |  ce96918c 1e010402 01fec08d 3600
ce96931c 1e010652 01fec08d 3600  |  ce96932c 1e010662 01fec08d 3600  |  ce96933c 1e010672 01fec08d 3600
ce96934c 1e010642 01fec08d 3600  |  ce96935c 1e010612 01fec08d 3600  |  ce96936c 1e010622 01fec08d 3600
ce96937c 1e010632 01fec08d 3600  |  ce96938c 1e010602 01fec08d 3600  |  ce969528 1e010860 01fec09d 3584
ce969538 1e010860 01fec09d 3584  |  ce969548 1e010840 01fec09d 3584  |  ce969558 1e010800 01fec0dd 3584
ce969568 1e010820 01fec09d 3584  |  ce969578 1e010820 01fec09d 3584  |  ce969588 1e010800 01fec09d 3584
d28e8d1c 1a010052 01fec08d 3456  |  d28e8d2c 1a010062 01fec08d 3456  |  d28e8d3c 1a010072 01fec08d 3456
d28e8d4c 1a010042 01fec08d 3456  |  d28e8d5c 1a010012 01fec08d 3456  |  d28e8d6c 1a010022 01fec08d 3456
d28e8d7c 1a010032 01fec08d 3456  |  d28e8d8c 1a010002 01fec08d 3456  |  d28e8f1c 1a010252 01fec08d 3456
d28e8f2c 1a010262 01fec08d 3456  |  d28e8f3c 1a010272 01fec08d 3456  |  d28e8f4c 1a010242 01fec08d 3456
d28e8f5c 1a010212 01fec08d 3456  |  d28e8f6c 1a010222 01fec08d 3456  |  d28e8f7c 1a010232 01fec08d 3456
d28e8f8c 1a010202 01fec08d 3456  |  d28e911c 1a010452 01fec08d 3456  |  d28e912c 1a010462 01fec08d 3456
d28e913c 1a010472 01fec08d 3456  |  d28e914c 1a010442 01fec08d 3456  |  d28e915c 1a010412 01fec08d 3456
d28e916c 1a010422 01fec08d 3456  |  d28e917c 1a010432 01fec08d 3456  |  d28e918c 1a010402 01fec08d 3456
d28e931c 1a010652 01fec08d 3456  |  d28e932c 1a010662 01fec08d 3456  |  d28e933c 1a010672 01fec08d 3456
d28e934c 1a010642 01fec08d 3456  |  d28e935c 1a010612 01fec08d 3456  |  d28e936c 1a010622 01fec08d 3456
d28e937c 1a010632 01fec08d 3456  |  d28e938c 1a010602 01fec08d 3456  |  d28e9528 1a010860 01fec09d 3456
d28e9538 1a010860 01fec09d 3456  |  d28e9548 1a010840 01fec09d 3456  |  d28e9558 1a010800 01fec0dd 3456
d28e9568 1a010820 01fec09d 3456  |  d28e9578 1a010820 01fec09d 3456  |  d28e9588 1a010800 01fec09d 3456
d2968d1c 1a010052 01fec08d 3600  |  d2968d2c 1a010062 01fec08d 3600  |  d2968d3c 1a010072 01fec08d 3600
d2968d4c 1a010042 01fec08d 3600  |  d2968d5c 1a010012 01fec08d 3600  |  d2968d6c 1a010022 01fec08d 3600
d2968d7c 1a010032 01fec08d 3600  |  d2968d8c 1a010002 01fec08d 3600  |  d2968f1c 1a010252 01fec08d 3600
d2968f2c 1a010262 01fec08d 3600  |  d2968f3c 1a010272 01fec08d 3600  |  d2968f4c 1a010242 01fec08d 3600
d2968f5c 1a010212 01fec08d 3600  |  d2968f6c 1a010222 01fec08d 3600  |  d2968f7c 1a010232 01fec08d 3600
d2968f8c 1a010202 01fec08d 3600  |  d296911c 1a010452 01fec08d 3600  |  d296912c 1a010462 01fec08d 3600
d296913c 1a010472 01fec08d 3600  |  d296914c 1a010442 01fec08d 3600  |  d296915c 1a010412 01fec08d 3600
d296916c 1a010422 01fec08d 3600  |  d296917c 1a010432 01fec08d 3600  |  d296918c 1a010402 01fec08d 3600
d296931c 1a010652 01fec08d 3600  |  d296932c 1a010662 01fec08d 3600  |  d296933c 1a010672 01fec08d 3600
d296934c 1a010642 01fec08d 3600  |  d296935c 1a010612 01fec08d 3600  |  d296936c 1a010622 01fec08d 3600
d296937c 1a010632 01fec08d 3600  |  d296938c 1a010602 01fec08d 3600  |  d2969528 1a010860 01fec09d 3584
d2969538 1a010860 01fec09d 3584  |  d2969548 1a010840 01fec09d 3584  |  d2969558 1a010800 01fec0dd 3584
d2969568 1a010820 01fec09d 3584  |  d2969578 1a010820 01fec09d 3584  |  d2969588 1a010800 01fec09d 3584
```

Per first block: E[number of passing classes] = 222 p7 = 3.523 and the expected number of good pairs (variants
passing both filters) is g = 782,800 x p7 x p6 = 830.988 (Lemma 5.1, linearity). Passing classes are strongly correlated
(their c7 values are close), so the counts are bursty; the expectations are exact.

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

### 6.2 Row 16 as a table, rows 17..36

For l in L*, E16x = C16_l + u with u = W0 + s0(W1) (W16 = s1(W14) + W9 + s0(W1) + W0; C16_l collects rows 12..15,
K16, s1(W14), W9), and every cell of row 16 of both members and every two-bit condition closing at row 16 is a
function of E16x only. The exhaustive enumeration of 7319bba (`r16.c`, Appendix A.5; inherited, not re-run: all E16x with the row's nine fixed
x-bits, 2^23 per l, for the 28 elements of L* whose row 16 can hold, the other four having a nonzero W16 difference)
gives 1,052,672 pairs (u, l) (the same number as 6c77089c and 087a18c4), 1,042,240 distinct u. The table
R16[u] = {l : C16_l + u passes row 16} is stored as the direct mask table Rmask[u] = OR of 2^l over the pairs (u, l), one
256-bit word for each u in 0..2^32 - 1 (2^37 bytes; bits 0, 2, 16, 18 are always zero; this derivative, Appendix B): one load
returns 0 if u is not a member and its l-mask otherwise. By Lemma 5.1 u is uniform for a good pair, so
Pr[row 16 for l] = |R16_l|/2^32 exactly, and Pr[u in R16] = 1,042,240/2^32.

**The presence word (first-level probe).** Let c = C16_19 = 43579466. The 8-bit window (u + c) >> 16 & 255 takes
only 56 of the 256 values on the 1,042,240 members (no other (c, s) among the 28 C16_l, 200 random constants and all
shifts s in 0..24 gives fewer); PRES_P is the 256-bit word with the 56 bits set. A u with a clear window bit is not a
member (zero false negatives by construction; checked on all members by 7319bba's `presence.py`, Appendix A.6); a present window is
followed by the exact lookup. For a uniform u the window is present with probability 56/256 exactly.

For each l in R16[u] the program computes W2..W5 (Lemma 4.1), W8 = W8C - E4, the y-words, and rows 16..36 of both
members, checking every cell and printed two-bit condition of each row, aborting at the first failing row.

**Lemma 6.1.** If rows 16..36 follow every cell, the two second-block outputs are equal (rows 33..36 of A and E have
no difference and the chaining value is common), hence m = M0 || M1 and m' = M0 || M1' collide under the
complete target (FIPS padding appends the same third block to both 128-byte messages; M1 is a full data block, so
W14, W15 are free). m != m' because M1 and M1' differ (W6..W10, W14, W15).

## 7. The Step-3 probability for the variants (H2)

### 7.1 The quantity

For a good pair (CV1, a0) and l in L*, let F_l be the event that rows 16..36 follow every cell and every printed
two-bit condition closing at rows >= 16. q3 = average over the 782,800 selected variants and over l in L* of
Pr[F_l | good], the probability over CV1 (Lemma 5.1 gives the exact joint law of all second-block words). The
expected number of successful (variant, l) per first block is g x 32 x q3.

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


### 7.3 The estimator (7319bba's `smc.c`, Appendix A.7; inherited, not re-run here)

Stages: row 16 exact (the enumeration of 6.2: the stage mean is (1/32) sum_l |R16_l| / 2^32 = 2^-16.994, and the initial particles are drawn exactly from the passing (l, E16) pairs);
rows 17..21: each child proposes E_t^x uniformly with the row's fixed x-bits imposed (exact importance weight 2^-f), sets W_t^x = E_t^x - (the rest of step t), W_t^y = W_t^x + its exact
difference, and checks the whole row; row 22: (W6, W7) drawn uniformly from F6 x F7; rows 23..36: W8 of a variant drawn uniformly from the 782,800 selected variants (the same row-22 survivor
is also evaluated with the published W8 for a paired comparison). NP particles, M children per particle per stage, MT tail proposals per particle, multinomial resampling of the survivors after
every stage; the product of the stage means is an unbiased estimator of q3 (the standard SMC normalising-constant estimator). The design is 6c77089c's and 087a18c4's; the program of Appendix A.7 is
7319bba's. **This filing does not re-estimate q3**: the family of variants, the classes, the filters and every row of the characteristic are those of 7319bba, and the table of this filing changes only how the
good pairs are *found* (Lemma 8.1), not which pairs are good or how they are tested. The estimate enters as premise H2.

### 7.4 The registered studies of 7319bba (reported unchanged)

**Study A** (registered 2026-10-10T08:11:18Z, before any listed seed ran): NP = 2048, M = 512, MT = 16384, 32 replicates; rule: the one-sided 99% Student lower bound of the mean of the 32 linear
estimates (t = 2.4528, 31 df), q3_model = 2^(floor(100 log2 LB)/100). Result: mean 2^-74.0187, relative standard deviation 0.0743, lower bound 2^-74.0659, q3_model(A) = 2^-74.07.
**Study B** (registered after study A had been read, to tighten the spread; same program, NP = 8192): mean 2^-73.9987, relative standard deviation 0.0378, lower bound 2^-74.0225,
**q3_model = 2^-74.03 (used here)**. All 32 replicates of study B (log2):

```text
-74.022 -73.967 -74.038 -73.934 -74.032 -74.059 -74.000 -74.017 -74.043 -74.070 -73.984 -73.942 -73.949 -73.956 -73.853 -73.965
-74.109 -73.985 -73.979 -73.927 -74.027 -73.983 -73.990 -74.065 -73.925 -74.057 -74.071 -74.052 -74.001 -74.025 -73.984 -73.976
```

| quantity | study A (NP 2048) | study B (NP 8192) |
|---|---|---|
| mean | 2^-74.0187 | 2^-73.9987 |
| relative standard deviation | 0.0743 | 0.0378 |
| 99% lower bound | 2^-74.0659 | 2^-74.0225 |
| **q3_model** | 2^-74.07 | **2^-74.03 (used)** |
| stage means (log2) | 16: -16.994, 17: -13.000, 18: -15.004, 19: -6.000, 20: -7.001, 21: -1.000, 22: -11.009, tail -4.015 | 16: -16.994, 17: -13.000, 18: -15.001, 19: -6.000, 20: -7.000, 21: -1.000, 22: -10.998, tail -4.007 |

The stage factors equal, within 0.01 bit, the per-row condition counts of the printed tables (17, 13, 15, 6, 7, 1, 11, 4; 74 in total). With study A's value this filing's claim would be
61.71201 (Section 11.2).

### 7.5 Consistency

- Lemma 7.1 makes rows 16..22 identical by construction; the paired rows-23..36 rates of the variants' and the published W8 differ by 0.002 bit in study B (7319bba).
- Real first blocks (7319bba, quoted in Section 13.1): the row-16 pass rate of the attack's own good pairs is the exact 2^-12 (z = +0.88 and +0.51 over 424,363 and 1,693,297 passes).
  This filing's end-to-end run (Section 13.4) finds row-16 passes at the same rate (2.403e-04 per good pair).

## 8. The algorithm: the x-indexed table and the fibre test

### 8.1 Fibres

For a variant a0 of a class c and A_{-1} = x define (Section 5.1, Lemma 4.1)

```text
phi(a0, x) = MAJ(A1, a0, x) - CH(E5, a0 + C4, E3)   (mod 2^32),   E3 = K3C - MAJ(A2, A1, a0) + x,       W6x = cb + phi(a0, x),   cb = C6 - A_{-2}.
```

(`xtab.phi`; it equals `w6of(a0, x, A_{-2}) - cb`, asserted in the selftest.) For fixed (c, x) the **fibres** are the classes of variants of c with equal phi; the **fibre values** are the distinct
values v_0 < v_1 < ... < v_{f-1}. Since cb is independent of x (H1), each fibre passes the F6 test independently of its size with probability exactly p6 whatever x is (cb + v is uniform).

**Lemma 8.1.** For a class c with W7x = c7 - x in F7, the good variants of c for (x, cb) are exactly the members of the fibres whose value v satisfies cb + v in F6. *Proof.* W6x of a member is cb + phi(a0, x) = cb + v, and
F6 depends on W6x only; W7x is the same word for the whole class (Section 5.3). QED. (Checked against the brute-force definition over all variants in Section 13.2.)

The expected number of good pairs per first block is therefore unchanged, g = 782,800 p7 p6 = 830.99, as are all later stages.

### 8.2 The table (offline; charged preprocessing; memory reported)

**T0** is an array of 2^32 words indexed by x = A_{-1}: T0[x] = 0 if no class passes, otherwise the address of the record R(x). R(x) lists, in increasing class order, the classes c with c7(c) - x in F7 (the test of Section 5.1), and for each:

- the number f of fibres and the number of batches nb = ceil(f / 256);
- **planes:** for each batch b the 32 planes dl[0..31] (256-bit words): lane L of plane j is bit j of the value of fibre 256 b + L; unused lanes of the last batch repeat lane 0;
- **fibre table:** for each fibre i one 64-bit word (offset_i, length_i) into the member array;
- **members:** the 64-bit records (a0 | S0(a0) << 32) of all variants of the class, grouped by fibre in increasing fibre-value order (each fibre contiguous).

**Construction and operation bound.** For x = 0, 1, ..., 2^32 - 1: (i) decide c7(c) - x in F7 for the 222 classes by the bitwise form of Section 5.1: at most 80 operations per class, 17,760 per x, 2^46.2 in all;
(ii) for each passing class (222 x |F7| = 15,130,951,680 pairs (x, class) in all, 2^33.82) and each of its n <= 3600 variants compute phi (at most 32 operations including the stores of (phi, record)),
sort the n pairs by phi with the bottom-up two-buffer merge sort (per record and pass at most (24 + 8) x 8 = 256 operations: 24 elementary statements for the emission of a record (exhaustion tests, two front-key loads, key comparison and branch, source and destination pointer advance, the loads and stores of the record fields, loop control, spill allowance), 8 for the per-pair set-up spread over at least two emissions, each elementary statement at most 8 primitives, as in the organizer baseline package's analysis of the same procedure; at most 12 passes since n < 2^12), then scan the sorted
array once to cut the fibres, write the fibre table and the members (at most 8 operations per record), and transpose the f <= 3600 fibre values into planes (at most 96 operations per fibre value). This is at most
3600 (32 + 12 x 256) + 3600 x 96 + 3600 x 8 = 11,548,800 operations per pair (x, class), 2^57.28 in all; (iii) writing T0 and the record addresses: 2^32 x 8 operations; (iv) the tables of the earlier filings (row-16 table, presence word,
variant records, lane-scan tables), below 2^38.7 operations (7319bba, Section 11.1 there); (v) the direct mask table Rmask of Section 6.2 (this derivative): zeroing its 2^32 words (store, pointer add, compare, branch: 4 operations each) and OR-ing 2^l into Rmask[u] for each of the 1,052,672 enumerated pairs (u, l) (at most 10 operations each), 17,190,395,904 operations (2^34.0009) in all. The total is below **PRE = 2^58 operations** (the five items sum to 2^57.2787; `PRE_ITEMS` in `experiments/xtab.py` asserts it), which is 2^46.6 target compressions (about 2^-15 of the score); all of it is included in T and in the claimed preprocessing.
The program text is straight-line code of a few thousand instructions; no part of the table depends on cb or on any other word of the chaining value.

### 8.3 The online algorithm

```text
input: N_FB, V_MAX; precomputed: S, L*, the class data, the table T0 and the records R(x), the row-16 mask table Rmask and the presence word, the 24-bit lane-scan tables
V = 0
for f = 1 .. N_FB:
    draw two uniform 256-bit words; M0 := their sixteen 32-bit fields; CV1 := F_37(IV, M0)                       [1 unit]
    p := T0[A_{-1}]; if p == 0: continue                                                                         (85% of first blocks)
    cb := C6 - A_{-2}; z_j := all-ones if bit j of cb else 0, j = 0..31                                          (the 32 broadcast planes)
    for each class c of R(p), for each batch b of its record:
        pass := F6(dl + cb) of the batch                                                                         (Section 9.4, 200 operations; +1 for a partial batch)
        for each set lane L of pass (24-bit chunk scan): (offset, length) := fibre table[256 b + L]; append the segment (offset, length)
    if the list of segments is nonempty (first time in this first block: the per-first-block constants of W0, W1):
        for each segment, for each group of up to four consecutive members: u := W0 + s0(W1) (packed, Section 9.6)
            for each valid lane: presence word of the window of u + c; if present: mask := Rmask[u] (one load)
                if mask != 0 (u is a member): recompute W6, W7;
                    for l in mask: rows 16..36 with early abort
                        if all rows pass: build m, m'; if digest(m) = digest(m') and m != m': output, halt
    V += (the executed cost of the first block, Section 9.8); if V > V_MAX: halt (failure)
halt (failure)
```

### 8.4 What is *not* assumed

The table lookup returns the class list of x as a stored record; no property of x other than being a 32-bit word is used. Distinct first blocks with the same x share the record; this does not couple their
success events beyond what H1 already assumes, because the record is a deterministic function of x and the success event depends on the remaining coordinates of the chaining value (cb, A_{-3}, A_{-4}, E_{-1..-4}).

## 9. The counted program

### 9.1 Machine and pricing

256-bit word RAM, 64 registers, every executed primitive counted (loads, stores and branches included). 32-bit values are kept in the low bits; a reduction mod 2^32 is one AND; a 32-bit rotation pattern (S0, S1, s0, s1) costs 8:
d = x | (x << 32) (2), three shifts and two XORs and one mask. A row-16 lookup (this derivative: the table Rmask of 2^32 words, entry u at word address RBASE + u) costs the extraction of u from its lane, the address (add),
the load, the V addition and a branch on zero. A branch and an unconditional jump are one primitive each (as in all earlier filings' scans); the program text is straight-line code. The target compression of a first block
is one unit and its internal operations are not counted again. Addresses of the tables are below 2^50 and fit a 256-bit word; a table read is one load after the address arithmetic. The executable counted program is `experiments/xtab.py`
(`process_cv`, `w6_batch`, `good_group`); its routines count every executed primitive of the routines below, and the ledger (`ledger`) is computed from them with exact rationals.

### 9.2 Fixed per first block: 51 operations

- First block words: 2 random words, then the 16 fields (field 0 of a word: and; fields 1..6: shr, and; field 7: shr): 30.
- Control allowance 16 (loop counter add and compare-branch, and further loop or address arithmetic not itemised elsewhere).
- The table read: address (shift, add) 2, load 1, test and branch 2: 5 (`T0_OPS`).

For a first block with a passing class (probability at most 0.16; measured 0.153): cb (2), the 32 broadcast planes z_j = 0 - ((cb >> j) & 1) (2 for j = 0, 3 for j >= 1: 95), the per-first-block constants of the packed stage (36 including the first-use flag): 133 in all.

### 9.3 Class loop

For each passing class: reading the record header (number of batches, plane address, fibre-table address, member address), the loop and branch: 8 operations (`CLASS_OVH`).

### 9.4 The fibre test of one batch: 200 operations

The batch holds the 32 planes dl[0..31] of up to 256 fibre values; the scalar cb is given by the planes z_j. The program computes w = dl + cb bit-serially with the NOT-free full adder carry = a ^ ((a ^ b) & (a ^ c)):

| step | operations |
|---|---|
| loads of dl[0..31] | 32 |
| bit 0: c = dl[0] & z[0] (the sum bit w0 is not needed) | 1 |
| bits 1..30: xy = dl[j] ^ z[j], xz = dl[j] ^ c, carry = dl[j] ^ (xy & xz) (4); the sum w_j = xy ^ c (1) only for the 19 bits of {1,2,3,8,9,10,12,13,14,15,16,18,19,20,25,26,27,29,30} | 30 x 4 + 19 = 139 |
| bit 31: xy, w31 = xy ^ c | 2 |
| F6: common = (w14^w18) \| ~(w8^w25) \| (w1^w12) (6), bc = (w15^w19) \| ~(w9^w26) \| (w2^w13) (6), X = (w16^w20^w31) \| ~(w10^w27^w31) \| (w3^w14^w31) (9), fail = common \| (w29 & (bc \| (w30 & X))) (4), pass = ~fail (1) | 26 |
| **total** | **200** (`W6_OPS`, asserted by the program) |

A partial batch (fewer than 256 fibre lanes) costs one more AND with the lane mask (201; the ledger charges 201 for every batch). The result is exact: lane L of the pass plane equals F6(cb + v_{256 b + L}) (checked on every lane, Section 13.2).
**Registers.** At bit j the live values are z_j..z_31 (32 - j), the carry, at most four temporaries, dl[j], and the retained sum bits (at most 19); the peak (about 40 at j around 14) and the F6 phase (20 sum bits and about 6 temporaries) are
below 64, with no spills. There is no data-dependent branch: the cost of a batch is the same for every cb and every record.

### 9.5 Scan of the pass plane and the segments

The pass plane (nl live lanes, zeros above) is scanned in 24-bit chunks: per chunk the extraction (the lowest and the highest chunk one operation, the others two) and a zero branch (`chunk_fixed_ops`); per set lane the load of the lane index from the 2^24-entry
table of the chunk position, the add of the batch base, x - 1, x & (x - 1) and the loop branch: 5 (`SCAN_LANE`). A set lane is a passing fibre: the load of its (offset, length) word from the fibre table (1) and the segment set-up (unpacking offset and length 2, the number of groups (length + 3) >> 2: 2, the source pointer 1, the loop initialisation and branch 2, one spare for the segment-list update: 8, `SEG_OVH`) complete the 14 operations per passing fibre.

### 9.6 Packed good pairs: the group of four, read in place

The member records of a segment lie contiguously in the table; a *group* is the 256-bit word at the address of four consecutive records, whose four 64-bit lanes (a0 | S0(a0) << 32) are processed together. The arithmetic is lane-safe: with M = 2^32 - 1 in every lane,
a0 = G & M, S0a = (G >> 32) & M, E0 = (a0 + e0b) & M, W0 = a0 + kap0 (< 2^33), mj = (a0 & o12) | n12, ch = (E0 & X) ^ Em2, S1(E0) with the 8-operation pattern (masked), W1 = (kap1 + 2^34 - S0a - mj - S1(E0) - ch) & M (the bias 2^34 keeps every
lane positive: each subtrahend is below 2^32, so the lane stays in [2^34 - 2^32 ... , 2^35) and no borrow or carry crosses a lane boundary), s0(W1) with the 8-operation pattern (masked), and U = W0 + s0(W1) (< 2^34). The constants e0b, kap0, o12, n12, X, Em2, kap1 are computed once per
first block from the chaining value (35 operations; kap0 = e0b - A_{-4} - E_{-4} - S1(E_{-1}) - CH(E_{-1}, E_{-2}, E_{-3}) - K0, e0b = A_{-4} - S0(A_{-1}) - MAJ(A_{-1}, A_{-2}, A_{-3}), kap1 = A1 - K1 - E_{-3}, as in Lemma 4.1).
Group cost: ld G 1, unpack 3, E0 2, W0 1, mj 2, ch 2, S1 8, W1 5, s0 8, u 1, U + c 1, loop control 2, V addition 1 = **37** (`GROUP_OPS`). The last group of a segment may read records beyond the end of the segment (the first records of the next
fibre); **only the valid lanes (those within the segment's length) are probed and counted as pairs**; the arithmetic of the other lanes is wasted work and is charged (it is part of the 37). Then, per valid lane k: the presence word (shr of U + c by 64 k + 16, and 255, shr of PRES_P, and 1, branch: **5**).
If the window is present, the direct lookup (`mask_lookup`, which counts each primitive where it executes and asserts the total): extraction of u from its lane (k = 0: and; k >= 1: shr, and), the word address RBASE + u (add), the load of Rmask[u], the V addition and the branch on zero: **5** (k = 0) or **6** (k >= 1), against 8 or 9 for d3ec5c41's bitmap probe. Under H1 the window is present with probability 56/256 = 7/32 exactly
(u is uniform, Lemma 5.1), so the expected cost per valid lane is 5 + (7/32) x 5.75 = 6.26.
**Verification:** `selftest` compares the 4 lanes of U with the definition of u (W0 + s0(W1) from the chaining value and a0) on 8,000 lanes: 0 mismatches.

### 9.7 The rare path

A member of the row-16 table (a nonzero mask; probability 1,042,240/2^32 per good pair): V += 1; the l-mask is the word the lookup already loaded (d3ec5c41's binary search of 132 operations is not needed); recompute W6, W7 (23 operations); then for the l in the mask W0..W5 and W8 (201),
the y-words (8) and rows 16..36 with early abort (each row 106 + 53 + 1: both members' W (20), CH (3), E (14), MAJ (4), A (12) per word; the cells and the two-bit conditions closing at the row at most 53), charged for rows 16 and 17 always and for rows 18..36 with probability at most 2^-9 each
(the SMC stage factors give 2^-15, 2^-6, ...). These are the counts of 7319bba's Section 9.7 without its binary search.

### 9.8 The work counter V

V counts every data-dependent operation in the units of Sections 9.3-9.7: after each first block with a passing class V receives the exact executed cost of that first block; the cap is tested after every first block (2 operations, in the fixed 51). The overshoot past V_MAX is at most
the maximal data-dependent work of one first block, vmax_fb = 84,591,095,557.625 (all 222 classes passing, every fibre a singleton and good, every l past row 16 to row 36), which the ledger charges (rounded up).

## 10. Success probability, independence and caps

Let a *trial* t = (f, a0, l) be a first block f, a selected variant a0 and l in L*, and A_t the event that a0 is good for f and the pair follows every cell and printed two-bit condition of rows 16..36. The program examines every good pair of every processed first block
(Lemma 8.1) and every l whose row 16 holds, so it finds a success iff some A_t occurs before the cap (and every output is verified, Lemma 6.1). Let X_f = sum over the trials of f of 1[A_t] and X = sum_f X_f.

- **Expectation.** E[X_f] = g x 32 x q3 (Lemma 5.1 and Section 7) and E[X] = N_FB g 32 q3. With q3 >= q3_model (H2): E[X] >= N_FB g 32 2^-74.03 >= mu0 = 0.49466252 (H7) for N_FB = ceil(mu0 / (g 32 2^-74.03)) = 358,768,880,796,199,274 = 2^58.31583;
  mu0 is the smallest 8-decimal number strictly above -ln(0.61 - Pcap - 2^-60) / (1 - 2^-10.4), with Pcap the work-cap failure bound below.
- **One first block (H3).** By Bonferroni, Pr[X_f >= 1] >= E[X_f] - sum over pairs t < t' of f of Pr[A_t and A_t'] = E[X_f] - (1/2) sum_t Pr[A_t] E[X_f - 1 | A_t]. H3: E[X_f - 1 | A_t] <= delta = 2^-9.4 for every trial t, so
  Pr[X_f >= 1] >= (1 - 2^-10.4) E[X_f]. (Only the expected number of *further* successes of the same first block given one success is needed; bursty goodness and shared W7/W6 values enter only through that conditional expectation, and do not affect E[X], which is linear.)
- **Many first blocks (H1).** Distinct first blocks have independent chaining values, so the events X_f >= 1 are independent and Pr[X >= 1] >= 1 - exp(-sum_f Pr[X_f >= 1]) >= 1 - exp(-(1 - 2^-10.4) mu0). The table record of x is a deterministic function of x (Section 8.4).
- **Work cap.** The data-dependent work v_f of a first block (everything except its compression and its 51 fixed operations) has mean at most vbar = 15859.09 (Section 11) and is at most vmax_fb = 84,591,095,557.625 (< 2^36.4; every class passing, every fibre a singleton and good, every l past row 16 to row 36).
  The v_f are independent (H1), so by Chebyshev Pr[sum v_f > (1 + 2^-6) N_FB vbar] <= E[v_f^2]/(2^-12 N_FB vbar^2) <= vmax_fb/(2^-12 N_FB vbar) = Pcap < 2^-23.96 (2^-23.969). V_MAX = ceil((1 + 2^-6) N_FB vbar) = 5,778,650,807,088,376,677,839 is reached with probability below Pcap; the run then fails, which is accounted for here.
  Unlike the decision-DAG filter of 7319bba, no part of v_f depends on a conditional law of the scalars: the cost of a fibre batch is the same for every cb and every record (Section 9.4), and the table statistics enter vbar as expectations over uniform x (H9).
- **Success.** Pr[output a collision] >= 1 - exp(-(1 - 2^-10.4) mu0) - Pcap - 2^-60 = 0.3900000003 > 0.39 (the 2^-60 covers a repeated first block among N_FB draws of 512 bits). Any output is a verified collision, independent of the premises.

## 11. Ledger (exact; `python3 experiments/xtab.py ledger`)

```text
T = A_C + A_S + DEV + N_FB + (N_FB x 51 + V_MAX + vmax_fb + PRE + FIN) / C + 6
  A_C = 2^60   characteristic search and SFS-pair search of the paper (allowance, H4)
  A_S = 2^50   Step-1 SAT solve (paper: 2^41.3)
  DEV = 2^40   all development computation (Section 13.5)
  N_FB = 358,768,880,796,199,274 compressions (2^58.31583; H7 mu0 = 0.49466252, q3 = 2^-74.03)
  51           fixed operations per first block (9.2: 30 + 16 control + 5 table read)
  V_MAX = 5,778,650,807,088,376,677,839 = ceil((1 + 2^-6) N_FB vbar), vbar = 15859.09 operations, of which
               first blocks with a passing class (probability <= 0.16): cb, the 32 broadcast planes and the constants of the packed stage: 21.28
               fibre tests, scans, segments and the packed arithmetic of the member blocks (the 37 operations of every group, wasted lanes included): 10,524
                 = p7 x sum over the 222 classes of (8 + b_c x (201 + chunk256) + p6 f_c x (5 + 1 + 8) + p6 q_c x 37)
                   with f_c, b_c, q_c = the means over x of the number of fibres, of 256-batches and of 4-groups of the class given that it passes, each from Section 13.3 times 1.02
               presence word and direct lookup per good pair: g x (5 + 7/32 x 5.75) -> 5,200
               rows >= 16: g x 2^-12.0 x (225 + 328 + (19/512) x 160) -> 113.8
  vmax_fb = 84,591,095,557.625 (one first block's maximal work: overshoot past the cap test; charged rounded up)
  PRE = 2^58 operations (bound on all precomputation, Section 8.2); FIN = 1600 operations and 6 compressions
T x 2644 = 9,797,125,415,937,815,688,179     ->   T = 2^61.684342   ->  time_log2 = 61.68435
preprocessing = A_C + A_S + DEV + PRE/C = 2^60.00155
```

Every count in this block is produced by `ledger()` of `experiments/xtab.py` from the executable routines and the constants STATS (Section 13.3); the integer-tightness of the 5th decimal is asserted in both directions (T^100000 against 2^(p) and 2^(p-1)).
Per first block the program spends 7.02 units, against 7.23 in d3ec5c41 and 13.08 in 7319bba: the fibre test costs 2,304 operations per first block instead of 10,700 (W6) + 191 + 28 (W7 and its scan), and the gather of 8 operations per good pair is replaced by 14 operations per passing fibre.

### 11.1 Precomputation

Section 8.2: PRE < 2^58 operations, charged in full (2^46.6 units). The earlier tables (row-16 enumeration, presence word, variant records, lane-scan tables) and the direct mask table Rmask of this derivative (item (v)) are included in that bound.

### 11.2 Sensitivity (log2 T, one input changed)

| change | log2 T |
|---|---|
| as claimed (q3 = 2^-74.03, study B's bound) | 61.68435 |
| q3 = 2^-74.0225 (study B's bound at face value) | 61.67919 |
| q3 = 2^-74.07 (study A's bound) | 61.71201 |
| q3 = 2^-74.25 | 61.83935 |
| q3 = 2^-74.5 | 62.02366 |
| q3 = 2^-75 (the paper's count of 75 conditions) | 62.41569 |
| A_C = 2^64 | 64.18698 |
| A_C = 2^56 | 61.18678 |
| table statistics at face value (x 1.00 instead of x 1.02) | 61.67326 |
| table statistics x 1.10 | 61.72785 |
| table statistics x 1.50 | 61.92765 |

The table is a sensitivity of the *claimed bound*, in the sense of what the bound would have to be if the stated input were different. For the algorithm as submitted the caps N_FB and V_MAX are fixed, so time is bounded by the claim by construction; a table statistic or an op count that is too small does not lengthen the run but lowers the success probability, which has only the slack of the 1.02 margin on the table statistics (about 0.4% of vbar) and of the 2^-6 cap factor (1.6%): a true mean above vbar by more than about 2% would make the cap bind and reduce the success probability below 0.39 unless N_FB and V_MAX are rescaled as the table says. Operations the program executes but does not count are not covered by the cap; the counts of Section 9 are those of the straight-line text described there.

### 11.3 The advice-construction allowances A_S and A_C (H4)

The cost model charges all construction of the advice, including searches omitted from the program. The advice is (i) the 37-step characteristic and its two-bit conditions (Tables 15, 16), (ii) the Step-1 solution S, and (iii) the semi-free-start pair (Table 17) from which S is read.
Everything derived from them (G, the classes, F6, F7, L*, R16, the table) is recomputed in the precomputation (Section 8.2).

- **(ii) and (iii): Step 1 and the SFS pair, charged A_S = 2^50.** The paper reports its Step-1 SAT solve at 2^41.3 compression-equivalents; A_S is 2^8.7 times that. Completing a Step-1 solution to a 37-step semi-free-start pair is cheap and is reproduced in this package: given the characteristic and a dense part (S or any of its A0-variants),
  the organizer experiment `a0-sfs-r37` builds complete 37-step semi-free-start collisions in about 25 milliseconds each (Section 13.2), so the SFS-pair search beyond Step 1 costs below 2^30 units, far inside A_S.
- **(i): the characteristic search, charged A_C = 2^60.** Its running time is not published. We bound it, as the accepted filings on this track do, by the only measured comparison point accepted on this challenge. The promoted filing 6eeefb64 (sha256-r32-exploratory) charged a measured, complete re-run of the four-step
  characteristic search of [LLWS26] for its 35-step characteristic: 593,858 solver CPU-seconds over 59 calls (it charged 32 times that for a blind rediscovery), with a calibrated price of one solver CPU-second of 2^32.796 primitive operations, i.e. 2^21.427 units at C = 2644. A_C = 2^60 units buys 2^38.573 = 4.1 x 10^11 solver
  CPU-seconds, about 13,000 CPU-years: 688,000 times (2^19.39) that measured complete re-run, 2^14.39 times the 32-fold rediscovery allowance, and 200 times a 1000-core cluster running without pause for two years. The 37-step characteristic of [LZLLQZ26] comes from the same group's improved search and its cost is unpublished; the premise is that it did not exceed
  this budget. The same allowance is charged by the accepted filings 087a18c4, 1f12a09a and 7319bba on this track. Sensitivity: 11.2. No other term depends on it.

## 12. Premises

**H1 - uniform independent chaining values (score-critical).** The first blocks are fresh uniform 512-bit strings; their chaining values CV1 = F_37(IV, M0) behave as independent uniform 256-bit values; in particular x = A_{-1} is uniform on 2^32 and independent of cb = C6 - A_{-2} (uniform on 2^32).
Used for: Lemma 5.1 (exact filter rates and the law of the second-block words, per variant), the expected counts, the independence across first blocks (Section 10) and Chebyshev. Evidence: 7319bba's 2^21 and 2^23 real first blocks through the attack's own filters in C (quoted, Section 13.1: passing classes,
good pairs and row-16 passes at the predicted rates); this filing's 160,000 first blocks through the counted program (Section 13.4: passing-class and good-pair counts, row-16 passes). Limitations: a premise; tested on 2^17 to 2^23 first blocks, not 2^58.3. Because the table is indexed by the 32-bit word x,
H1 for x is also an assumption about a single word of the digest of a 37-round compression: its distribution over random first blocks is uniform up to the sampling resolution of the runs above.

**H2 - Step-3 probability of the variants (score-critical).** q3 >= q3_model = 2^-74.03 (Section 7.1's average over the 782,800 selected variants and L*), and q3 <= 2^-70. Evidence: Lemma 7.1 (rows 16..22 identical for all variants; the variant enters only through W8 in W23, W24), the two preregistered SMC studies of 7319bba (Section 7.4; study B is the primary,
both are reported), the agreement of the stage factors with the printed tables and the peers' studies row by row, the row-16 rate of real good pairs, and the 37-step semi-free-start collisions built with variant dense parts (Section 13.2). Limitations: a Monte-Carlo bound produced by another solver (its
programs are in Appendix A.7; **not re-run here**), whose coverage rests on the approximate normality of the mean of 32 replicates (study B: relative sd 0.0378); the `+` reading; the heavy duplication of row-22 survivors within a replicate. A stated premise, not an established fact.

**H3 - few further successes per first block (score-critical).** For every trial t, the expected number of other successful trials of the same first block given A_t is at most delta = 2^-9.4, i.e. E[X_f - 1 | A_t] <= 2^-9.4. It splits into (a) the same variant with another l in L*, and (b) other good pairs (other variants) of the same first block.
For (a) the premise is E[#other l succeeding | A_t] <= 2^-11; 7319bba measured it directly on 19,620,436 distinct Step-3 successes of the SMC (replay of Section 13.1: 0 further successes; rule-of-three 95% bound 2^-22.65). For (b) the expectation is at most rho x (782,800 x 32 x q3) <= rho x 2^-45.42 with q3 <= 2^-70 (H2), where rho bounds
Pr[t' succeeds | t succeeds, t' good] / Pr[t' succeeds | t' good]; the premise is rho <= 2^35 (the measured factor at the row-16 level is 0.98 and 1.00), so delta <= 2^-11 + 2^-10.42 < 2^-9.4. The table changes nothing here: the good pairs and their order within a first block are those of the earlier filings up to permutation.
Limitations: rows >= 17 of distinct good pairs cannot be measured jointly within one first block; the premise leaves a margin of 2^35 over the measured row-16 factor.

**H4 - advice allowances (supporting).** The published characteristic and two-bit conditions, the SFS pair's inner values S and L* are advice. Their construction is charged A_S = 2^50 (Step 1 and the completion to an SFS pair) and A_C = 2^60 (the characteristic search). Evidence: Section 11.3.
The variant family, the classes, the filter sets, L*, R16, the table and the program text are recomputed in the preprocessing (Section 8.2). Limitations: the 37-step search time is unpublished; A_C is a bound by comparison, not a measurement.

**H5 - counted word-RAM pricing (score-critical; cost reading).** A word-RAM program of 256-bit primitives in which every executed load, store, logic operation, shift, addition, comparison, branch and unconditional jump costs one primitive is charged by the primitives it executes; tables are ordinary
memory (a read is an address computation plus one load; memory is a reported metric only under collision-frontier-v5); the preprocessing is charged in full; registers: 64, with the live-value bound of Section 9.4; the program text is straight-line code of a few thousand instructions and is not advice. Evidence: the
program is in `experiments/xtab.py` (`w6_batch`, `good_group`, `process_cv`) and is exact against the scalar definitions (Section 13.2); its totals agree with the ledger (Section 13.4). Limitation: no organizer ruling is cited; the premise that the table of 2^50 bytes is admissible follows the earlier accepted claims with
memory far above physical capacity (e.g. 2^137 bytes) and the cost model's statement that memory contributes nothing to the scalar. A reader who prices memory accesses higher should read Section 11.2 (the per-first-block time is dominated by the packed stage, not by table reads: about 550 table loads per first block).

**H7 - exact success floor (supporting).** The cap target is mu0 = 0.49466252, the smallest 8-decimal number strictly above -ln(0.61 - Pcap - 2^-60) / (1 - 2^-10.4) with Pcap = 2^-23.969 the Chebyshev bound for the work cap. With E[X] >= mu0 the success bound of Section 10, 1 - exp(-(1 - 2^-10.4) mu0) - Pcap - 2^-60, is >= 0.39000000
with no further padding. `ledger()` computes mu0 with 60-digit decimals, asserts the success bound > 0.39 and the exact-rational ceiling N_FB g 32 q3 >= mu0. (087a18c4's H7.)

**H9 - table statistics and preprocessing bound (score-critical, new).** (a) For each of the 222 classes let f_c, b_c, q_c be the means, over the x for which the class passes W7, of the number of fibres, of ceil(fibres/256) and of sum over fibres of ceil(size/4). The ledger charges 1.02 times the sample means of Section 13.3 (1,500 values of x per class
drawn uniformly from the passing set c7 - F7; two further independent samples of 1,500 differ from the first by at most 0.31% (fibres), 0.26% (batches), 0.05% (four-groups) in the totals), and assumes these are upper bounds of the exact means. (b) The preprocessing of Section 8.2 costs at most 2^58 operations and the table at most 2^50 bytes. Evidence for (a): sampling, with the standard error of the aggregate
below 0.1% and the sensitivity of Section 11.2 (a 50% error in all table statistics would cost 0.24 bit); the quantity multiplies only the fibre-test terms (66% of the data-dependent work). Evidence for (b): the explicit algorithm and the arithmetic of Section 8.2; 7319bba's bound for the old tables. Limitation: the means are sample estimates, not exact enumerations over all 2^32 x.

## 13. Evidence and runs

All runs for this filing on one Apple-silicon Mac (18 cores): Python standard library (`experiments/xtab.py`) and Tungsten (the user's compiled language, sources in Appendix A); my own code, no rival code executed. The leader's programs and numbers that are used as premises are labelled as such.

### 13.1 Quoted from 7319bba (end to end on real first blocks; inherited evidence for H1, H3, H2)

C statistics of 7319bba (random M0 from xoshiro256**, CV1 = F_37(IV, M0), the 222 W7 tests, the scalar W6 test of every variant of every passing class, u and the exact row-16 test for every l, exact checks of sampled pairs):

| run | first blocks | passing classes (expected) | good pairs (expected; ratio) | row-16 pairs (expected; z) | H3 factor: sum R(R-1) / p^2 sum G(G-1), p = 1052672/2^32, (p = R/G) |
|---|---|---|---|---|---|
| seed 5eed0021 | 2^21 | 7,400,134 (7,388,160) | 1,748,648,111 (1,742,708,500; 1.00341) | 424,363 (422,895; +0.88) | 0.981 (1.001) |
| seed 5eed0023 | 2^23 | 29,545,568 (29,552,640) | 6,978,649,557 (6,970,834,000; 1.00112) | 1,693,297 (1,691,580; +0.51) | 0.979 (0.999) |

The counts are strongly overdispersed (variance-to-mean ratios 28.8 for passing classes, about 23,100 for good pairs, 6.6 for row-16 pairs) because classes are correlated; their means match. 7319bba's replay of 19,620,436 distinct Step-3 successes of the SMC found 0 co-successes across the other 31 elements of L*
(rule-of-three 95% bound 2^-22.65 per success; the samples share SMC ancestors). These programs are not re-run here.

### 13.2 Exhaustive checks and equivalence with brute force (this filing)

- **F6, F7 (Tungsten, Appendix A.2).** For all 2^32 words w: the definition F_k = {w : s0(w + d_k) - s0(w) = t_k} against the bitwise forms of Section 5.1, four shards of 2^30 words: |F6| = 287,309,824 and |F7| = 68,157,440, **0 mismatches** for both.
- **The family G (Tungsten, Appendix A.1).** |G| = 12,103,680 over the 2^29 values of E4 with E4[31:29] = 000.
- **The classes.** `xtab.py` regenerates all 222 classes from the descriptors of Section 5.3 and asserts their sizes (782,800 variants in all).
- **The table pipeline against brute force (`selftest`).** For 8 classes (indices 0, 17, 40, 77, 111, 150, 200, 221), 4 random x each with the class passing W7 and a random cb: the entry (fibres, planes, members) is built, every lane of every pass plane is compared with the scalar F6 test of its fibre value
  (9,556 lanes) and the set of members of the passing fibres with the set {a0 in class : F6(w6of(a0, x, A_{-2}))} (5,882 good pairs): **0 mismatches**; every entry partitions the class exactly (the lengths sum to the class size, asserted). 15 further random (class, x, cb) triples
  checked independently: 3,160 good pairs, 0 mismatches.
- **Packed arithmetic and presence word.** The 4-lane U against the definition of u (W0 + s0(W1) from the chaining value and a0): 8,000 lanes, 0 mismatches; the presence word has 0 false negatives on 3,000 random u (and on all 1,042,240 members: 7319bba, Appendix A.6).
- **Organizer experiments (local replay of the request format with SHAKE-derived seeds; byte-identical on a second run; 1.0 s and 3.5 s, peak memory 42 MB and 32 MB, inside the organizer's 20 s and 128 MB).**
  `a0-sfs-r37`: 127 of the 128 trials build a 37-step semi-free-start collision with a variant dense part (the 128th exhausts its proposal budget); for trials 0..15 the constructed chaining value is fed to the counted online program restricted to the class of a0,
  which finds exactly the constructed pair in **16 of 16** cases (W7 test of the class, table read, fibre test, packed u, presence word, row-16 probe, rows 16..36). `a0-online-r37` (trials 0..7): 0 lane, filter and cell mismatches.

### 13.3 Fibre statistics of all 222 classes (Tungsten; premise H9)

For each class, 1,500 values x = c7 - w with w uniform on F7 (the exact sampler of Section 5.1, an affine decomposition into 2^26 and 2^20 words with probabilities 64/65 and 1/65), phi(a0, x) for all variants, a heap sort and a run scan. Means per passing class over the 222 classes
(average class size 3,526.1): **293.2 fibres** (min 221, max 407 over classes), **1.547 batches of 256**, **924.1 four-groups** (against 881.5 without the fibre structure), **170.4 padding lanes** (4.8% of the members); these are the means of the three samples below. Per-class values are the constant STATS of `xtab.py`; the generator is Appendix A.4.
Two further independent samples of 1,500 values of x per class (different seeds) give aggregate means within 0.31% (fibres), 0.26% (batches), 0.05% (four-groups) and 1.1% (padding) of the first; per class the samples differ by 2.6% on average and up to 10.5% in the fibre counts. The ledger uses the mean of the three samples times 1.02. Raw outputs: Appendix A.11.

### 13.4 The counted program measured end to end (this filing)

`experiments/xtab.py` run on 160,000 real first blocks (8 independent seeds x 20,000; the table entries of each first block are built on the fly with the same code as in the experiments; every operation is counted by the routines of Section 9):

| quantity | measured | ledger / exact |
|---|---|---|
| mean counted operations per first block (fixed + data-dependent), d3ec5c41's row-16 probe | **16,028 +- 198** | 16,482 (51 + d3ec5c41's vbar) |
| the same with this derivative's direct lookup, our re-run of 80,000 first blocks (Appendix B) | **15,472 +- 272** | 15,910 (51 + vbar) |
| first blocks with a passing class | 0.1505 | <= 0.16 charged |
| passing classes per first block | 3.5265 | 3.5229 exact |
| good pairs per first block | 821.1 | 830.99 exact |
| row-16 passes per good pair | 2.403e-04 | 2.4268e-4 (1,042,240/2^32) |
| largest single first block | 2,218,945 operations (d3ec5c41's run); 2,262,982 (our re-run) | vmax_fb = 84,591,095,557.625 |

The counts are bursty (a first block with many passing classes costs up to 2 x 10^6 operations), so the standard error is dominated by rare large first blocks; the measured mean is below the ledger's expectation, which is therefore not exceeded by chance in this run.
It does not replace the exact expectations of the ledger, which are linear in the exact rates p7, p6 and the fibre means of H9.

### 13.5 Development computation

Below 10^5 CPU-seconds in total (the exhaustive F6/F7 check about 600 CPU-seconds, the fibre statistics about 10^4, the end-to-end runs about 2.4 x 10^3, the selftests and experiment replays under 100, development and the aborted runs the rest), far inside DEV = 2^40 units (2^40 units are about 2^18.6 = 4 x 10^5 CPU-seconds at 2^21.4 units per CPU-second).

## 14. Memory and advice

Peak memory (all simultaneously resident during the online phase):

| item | bytes |
|---|---|
| T0: 2^32 words of 8 bytes | 2^35 |
| records R(x): 15,130,951,680 pairs (x, class) x (members 8 n + fibre table 8 f + planes 1024 b + 64 header): typical 32,208 bytes, at most 73,024 | 2^48.79 typical, **at most 2^49.97** |
| row-16 mask table Rmask (this derivative; Section 6.2): 2^32 words of 32 bytes; lane-scan tables, variant records, code (7319bba's tables, without its row-16 bitmap and sorted array, its stored DAG planes and 323 MB code) | 2^37 + below 2^33 |
| total | **below 2^50** (at most 2^49.9732) |

Claimed memory: 2^50.0 bytes (an upper bound; reported only under collision-frontier-v5). The table is built entry by entry in the preprocessing and is never held twice. Nonuniform advice: the characteristic, S, L*, and the 222 class descriptors (below 2^13 bytes), charged through A_C and A_S; everything else, including the table, is recomputed in the preprocessing.

## 15. Limitations

- H1, H2, H3 are premises. q3 is estimated (Monte Carlo, by another solver, not re-run here), not proved; no collision has been found and none is expected at the scale we can run. The full-scale success probability cannot be observed.
- The table statistics (H9) are Tungsten sample means over 1,500 values of x per class, scaled by 1.02, not an enumeration of all 2^32 values of x (2^51 operations of Tungsten work). Section 11.2 prices a 10% and a 50% error.
- The memory of 2^50 bytes is far beyond any machine; memory is reported only under collision-frontier-v5 and earlier claims on this track report up to 2^137 bytes. A reader who charges table reads or memory differently should note that table reads are about 550 of the 15859.09 data-dependent operations per first block.
- Study B of the q3 estimate was registered after study A had been read (7319bba, Section 7.4); study A's bound would price the claim at 61.71201.
- The published characteristic and SFS pair are used as advice under allowances; the paper's SAT solve and characteristic search were not rerun.
- For 37 steps the measured q3 is about one bit better than the 75 conditions stated in the paper's text; the paper's own tables give 74, which the SMC matches stage by stage (6c77089c reached the same conclusion). With q3 = 2^-75, log2 T would be 62.41569.
- H3 (b) is measured at the row-16 level only (7319bba).
- The program text, the table and the lane-scan tables are assumed addressable and free of charge to store (H5); the cost reviewer may price memory differently (Section 11.2).

## 16. What this filing changes relative to 7319bba (62.34263)

| change | effect |
|---|---|
| x-indexed table (Section 8.2): the W7 test becomes one read | 191 + 28 operations per first block replaced by 5 |
| W6 filter on fibre values (Sections 8.1, 9.4): 293.6 fibres instead of 3,526 variants per passing class; one addition of cb and F6 per batch of 256 fibres | 10,700 operations per first block replaced by about 2,304 for tests and scans |
| member blocks read in place (Section 9.6): 14 operations per passing fibre instead of 8 per good pair | the gather of 6,650 operations per first block replaced by about 1,000 |
| no decision-DAG pricing (no premise on branches), no 40-million-instruction program, no conditional-law premise | simpler cost reading; no 10-minute ledger |
| same attack, variants, classes, packed u-stage, presence word, rare path, q3, caps | unchanged (Sections 4-7, 9.6-9.7, 10), except that this derivative looks up the row-16 l-mask directly (Appendix B) |

## Appendix A. Programs and records

A.1, A.2, A.4 and A.11 were written and run for this filing (Tungsten, the user's compiled language, `tungsten file.w`; Python `experiments/xtab.py` is the counted program). A.3 and A.5-A.10 are reproduced **unchanged from 7319bba as inert text; they were not run for this filing** and support the premises H2 and H3 and the tables of the earlier filings. They are evidence for the reader, not part of the attack. References to `spec6core.py` in the inherited listings refer to 7319bba's program, which is not part of this package.

### A.1 `gcount.w`: |G| over the 2^29 values of E4 with E4[31:29] = 000 (result: 12,103,680)

```text
-> count_g(lo, hi) (i64 i64) i64
  c4 = 734766 ## i64
  w8c = 3661266223 ## i64
  n = 0 ## i64
  e4 = lo ## i64
  while e4 < hi
    w = (w8c - e4) & 4294967295
    if ((w >> 29) & 1) == 1 && ((w >> 1) & 1) != ((w >> 12) & 1) && ((w >> 8) & 1) != ((w >> 25) & 1) && ((w >> 14) & 1) == ((w >> 18) & 1)
      n += 1
    e4 += 1
  n
# E4 = a0 + C4 has E4[31:29] = 000, so E4 < 2^29; a0 = E4 - C4 is a bijection on these
g_total = count_g(0, 536870912)
<< "G_count [g_total]"
```

### A.2 F6 and F7: the definitions against the bitwise forms of Section 5.1 on all 2^32 words (four shards of 2^30; shard k calls `run_shard(k * 2^30, (k + 1) * 2^30)`)

```text
-> s0g(x) (i64) i64
  a = ((x >> 7) | (x << 25)) & 0xFFFFFFFF
  b = ((x >> 18) | (x << 14)) & 0xFFFFFFFF
  a ^ b ^ (x >> 3)
-> inf2(w, d, t) (i64 i64 i64) i64
  u = (w + d) & 0xFFFFFFFF
  v = (s0g(u) - s0g(w)) & 0xFFFFFFFF
  r = 0 ## i64
  r = 1 if v == t
  r
-> f6b(w) (i64) i64
  b1 = (w >> 1) & 1
  b2 = (w >> 2) & 1
  b3 = (w >> 3) & 1
  b8 = (w >> 8) & 1
  b9 = (w >> 9) & 1
  b10 = (w >> 10) & 1
  b12 = (w >> 12) & 1
  b13 = (w >> 13) & 1
  b14 = (w >> 14) & 1
  b15 = (w >> 15) & 1
  b16 = (w >> 16) & 1
  b18 = (w >> 18) & 1
  b19 = (w >> 19) & 1
  b20 = (w >> 20) & 1
  b25 = (w >> 25) & 1
  b26 = (w >> 26) & 1
  b27 = (w >> 27) & 1
  b29 = (w >> 29) & 1
  b30 = (w >> 30) & 1
  b31 = (w >> 31) & 1
  common = (b14 ^ b18) | (1 ^ (b8 ^ b25)) | (b1 ^ b12)
  bc = (b15 ^ b19) | (1 ^ (b9 ^ b26)) | (b2 ^ b13)
  xx = (b16 ^ b20 ^ b31) | (1 ^ (b10 ^ b27 ^ b31)) | (b3 ^ b14 ^ b31)
  fail = common | (b29 & (bc | (b30 & xx)))
  1 - fail
-> f7b(w) (i64) i64
  b0 = w & 1
  b1 = (w >> 1) & 1
  b2 = (w >> 2) & 1
  b9 = (w >> 9) & 1
  b10 = (w >> 10) & 1
  b11 = (w >> 11) & 1
  b12 = (w >> 12) & 1
  b18 = (w >> 18) & 1
  b19 = (w >> 19) & 1
  b22 = (w >> 22) & 1
  b23 = (w >> 23) & 1
  b26 = (w >> 26) & 1
  b27 = (w >> 27) & 1
  b28 = (w >> 28) & 1
  b29 = (w >> 29) & 1
  b30 = (w >> 30) & 1
  b31 = (w >> 31) & 1
  ok = 1 ## i64
  ok = 0 if b1 != b18
  ok = 0 if b0 != b28
  ok = 0 if b9 != b30
  h1 = 0 ## i64
  h1 = 1 if b11 == 0 && b22 == 1 && b26 == 1
  h2 = 0 ## i64
  h2 = 1 if b11 == 1 && b12 == 0 && b22 == 0 && b23 == 1 && b26 == 0 && b27 == 1 && b2 == b19 && b1 == b29 && b10 == b31
  ok = 0 if h1 == 0 && h2 == 0
  ok
-> run_shard(lo, hi) (i64 i64) i64
  d6 = 536870912 ## i64
  t6 = 62916608 ## i64
  d7 = 4223666176 ## i64
  t7 = 25133056 ## i64
  n6 = 0 ## i64
  n7 = 0 ## i64
  bad6 = 0 ## i64
  bad7 = 0 ## i64
  w = lo ## i64
  while w < hi
    a6 = inf2(w, d6, t6)
    b6 = f6b(w)
    n6 += a6
    bad6 += 1 if a6 != b6
    a7 = inf2(w, d7, t7)
    b7 = f7b(w)
    n7 += a7
    bad7 += 1 if a7 != b7
    w += 1
  << "SHARD [lo] n6=[n6] n7=[n7] bad6=[bad6] bad7=[bad7]"
  0
```

### A.3 (7319bba, inherited, not run here) `f7an.c`, `f7dual.c`: the affine hull of F7 and of its two halves; the parity constraints (weight <= 5) of each half

```c
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef uint32_t u32;
#define ROR(x,n) (((x)>>(n))|((x)<<(32-(n))))
static u32 s0(u32 x){return ROR(x,7)^ROR(x,18)^(x>>3);}
typedef struct{u32 b[32];u32 w0;int has;int dim;uint64_t n;}H;
static void ins(H*h,u32 w){h->n++;if(!h->has){h->has=1;h->w0=w;return;}u32 v=w^h->w0;
 for(int i=31;i>=0;i--){if(!((v>>i)&1))continue;if(!h->b[i]){h->b[i]=v;h->dim++;return;}v^=h->b[i];}}
int main(){u32 D7=0xfbc00800,T7=0x017f8000;
 static H all; static H sp[32][2];
 for(uint64_t t=0;t<(1ull<<32);t++){u32 w=t; if((s0(w+D7)-s0(w))!=T7)continue; ins(&all,w);
   for(int k=0;k<32;k++)ins(&sp[k][(w>>k)&1],w);}
 printf("all n=%llu dim=%d (2^dim=%llu)\n",all.n,all.dim,1ull<<all.dim);
 for(int k=0;k<32;k++)for(int v=0;v<2;v++){H*h=&sp[k][v];printf("bit%d=%d n=%llu dim=%d %s\n",k,v,h->n,h->dim,(1ull<<h->dim)==h->n?"AFFINE":"");}
}
```

### 

```c
#include <stdio.h>
#include <stdint.h>
typedef uint32_t u32;
#define ROR(x,n) (((x)>>(n))|((x)<<(32-(n))))
static u32 s0(u32 x){return ROR(x,7)^ROR(x,18)^(x>>3);}
// for part p (bit11=p) find all parity constraints (mask m, const c): parity(w&m)==c for all members, enumerate all masks via counting
int main(){u32 D7=0xfbc00800,T7=0x017f8000;
 for(int p=0;p<2;p++){
  // collect members, test masks of weight<=4 (35960 masks) incrementally: keep list of candidate masks, filter
  static u32 mem[1<<26]; size_t n=0;
  for(uint64_t t=0;t<(1ull<<32);t++){u32 w=t;if(((w>>11)&1)!=p)continue;if((s0(w+D7)-s0(w))!=T7)continue;mem[n++]=w;}
  printf("part %d n=%zu\n",p,n);
  for(u32 m=1;m;m++){ if(__builtin_popcount(m)>5)continue; int c=__builtin_parity(mem[0]&m); size_t i=1; for(;i<n;i++)if(__builtin_parity(mem[i]&m)!=c)break; if(i==n)printf("  mask %08x w=%d const=%d\n",m,__builtin_popcount(m),c);}
 }}
```


### A.4 `fs_k.w`: fibre statistics of the classes k, k+4, k+8, ... (shard 0 shown; the other shards differ only in the class arrays and the seed; 1,500 values of x per class)

```text

-> maj3(x, y, z) (i64 i64 i64) i64
  (x & y) | (x & z) | (y & z)
-> ch3(x, y, z) (i64 i64 i64) i64
  (x & y) | ((x ^ 4294967295) & z)
-> in_g(a0) (i64) i64
  e4 = (a0 + 734766) & 4294967295
  w = (3661266223 - e4) & 4294967295
  ok = 1 ## i64
  ok = 0 if (e4 >> 29) != 0
  ok = 0 if ((w >> 29) & 1) != 1
  ok = 0 if ((w >> 1) & 1) == ((w >> 12) & 1)
  ok = 0 if ((w >> 8) & 1) == ((w >> 25) & 1)
  ok = 0 if ((w >> 14) & 1) != ((w >> 18) & 1)
  ok
-> c7_of(a0) (i64) i64
  e4 = (a0 + 734766) & 4294967295
  (2879002467 + maj3(2558469316, 1652717670, a0) - ch3(3943406637, 3891447839, e4)) & 4294967295
-> phi_of(a0, x) (i64 i64) i64
  e4 = (a0 + 734766) & 4294967295
  e3 = (1199649517 - maj3(2558469316, 1652717670, a0) + x) & 4294967295
  (maj3(1652717670, a0, x) - ch3(3891447839, e4, e3)) & 4294967295
-> sample_f7(r1, r2) (i64 i64) i64
  w = r2 & 4294967295
  w = (w & 4294705151) | (((w >> 1) & 1) << 18)
  w = (w & 4026531839) | ((w & 1) << 28)
  w = (w & 3221225471) | (((w >> 9) & 1) << 30)
  if (r1 % 65) != 0
    w = w & 4294965247
    w = w | 4194304
    w = w | 67108864
  else
    w = w | 2048
    w = w & 4294963199
    w = w & 4290772991
    w = w | 8388608
    w = w & 4227858431
    w = w | 134217728
    w = (w & 4294443007) | (((w >> 2) & 1) << 19)
    w = (w & 3758096383) | (((w >> 1) & 1) << 29)
    w = (w & 2147483647) | (((w >> 10) & 1) << 31)
  w
-> sift(arr, start, end_) (i64[] i64 i64) i64
  root = start ## i64
  running = 1 ## i64
  while running == 1
    child = root * 2 + 1
    if child >= end_
      running = 0
    else
      sw = root ## i64
      sw = child if arr[sw] < arr[child]
      sw = child + 1 if child + 1 < end_ && arr[sw] < arr[child + 1]
      if sw == root
        running = 0
      else
        t = arr[root]
        arr[root] = arr[sw]
        arr[sw] = t
        root = sw
  0
-> heapsort(arr, n) (i64[] i64) i64
  start = (n - 2) / 2 ## i64
  while start >= 0
    sift(arr, start, n)
    start -= 1
  end_ = n - 1 ## i64
  while end_ > 0
    t = arr[0]
    arr[0] = arr[end_]
    arr[end_] = t
    sift(arr, 0, end_)
    end_ -= 1
  0
-> main_run(dummy) (i64) i64
  ncls = 56 ## i64
  c7s = i64[512]
  bases = i64[512]
  masks = i64[512]
  c7s[0] = 3431894092
  bases[0] = 469827906
  masks[0] = 33472653
  c7s[1] = 3431894156
  bases[1] = 469827842
  masks[1] = 33472653
  c7s[2] = 3431894604
  bases[2] = 469828418
  masks[2] = 33472653
  c7s[3] = 3431894668
  bases[3] = 469828354
  masks[3] = 33472653
  c7s[4] = 3431895116
  bases[4] = 469828930
  masks[4] = 33472653
  c7s[5] = 3431895180
  bases[5] = 469828866
  masks[5] = 33472653
  c7s[6] = 3431895640
  bases[6] = 469829376
  masks[6] = 33472733
  c7s[7] = 3431896136
  bases[7] = 469829952
  masks[7] = 33472669
  c7s[8] = 3431896200
  bases[8] = 469829888
  masks[8] = 33472669
  c7s[9] = 3432418428
  bases[9] = 469827890
  masks[9] = 33472653
  c7s[10] = 3432418876
  bases[10] = 469828466
  masks[10] = 33472653
  c7s[11] = 3432418940
  bases[11] = 469828402
  masks[11] = 33472653
  c7s[12] = 3432419388
  bases[12] = 469827954
  masks[12] = 33473677
  c7s[13] = 3432419452
  bases[13] = 469828914
  masks[13] = 33472653
  c7s[14] = 3432419912
  bases[14] = 469829440
  masks[14] = 33472669
  c7s[15] = 3432419976
  bases[15] = 469829376
  masks[15] = 33472669
  c7s[16] = 3432420472
  bases[16] = 469829920
  masks[16] = 33472669
  c7s[17] = 3465448764
  bases[17] = 503382130
  masks[17] = 33472653
  c7s[18] = 3465448828
  bases[18] = 503382066
  masks[18] = 33472653
  c7s[19] = 3465449276
  bases[19] = 503382642
  masks[19] = 33472653
  c7s[20] = 3465449340
  bases[20] = 503382578
  masks[20] = 33472653
  c7s[21] = 3465449788
  bases[21] = 503383154
  masks[21] = 33472653
  c7s[22] = 3465449852
  bases[22] = 503383090
  masks[22] = 33472653
  c7s[23] = 3465450300
  bases[23] = 503383666
  masks[23] = 33472653
  c7s[24] = 3465450364
  bases[24] = 503383602
  masks[24] = 33472653
  c7s[25] = 3465450824
  bases[25] = 503384128
  masks[25] = 33472669
  c7s[26] = 3465450888
  bases[26] = 503384064
  masks[26] = 33472669
  c7s[27] = 3465973068
  bases[27] = 503382082
  masks[27] = 33472653
  c7s[28] = 3465973132
  bases[28] = 503382018
  masks[28] = 33472653
  c7s[29] = 3465973580
  bases[29] = 503382594
  masks[29] = 33472653
  c7s[30] = 3465973644
  bases[30] = 503382530
  masks[30] = 33472653
  c7s[31] = 3465974092
  bases[31] = 503383106
  masks[31] = 33472653
  c7s[32] = 3465974156
  bases[32] = 503383042
  masks[32] = 33472653
  c7s[33] = 3465974604
  bases[33] = 503383618
  masks[33] = 33472653
  c7s[34] = 3465974668
  bases[34] = 503383554
  masks[34] = 33472653
  c7s[35] = 3465975128
  bases[35] = 503384064
  masks[35] = 33472733
  c7s[36] = 3532557596
  bases[36] = 436273234
  masks[36] = 33472653
  c7s[37] = 3532557660
  bases[37] = 436273170
  masks[37] = 33472653
  c7s[38] = 3532558108
  bases[38] = 436273746
  masks[38] = 33472653
  c7s[39] = 3532558172
  bases[39] = 436273682
  masks[39] = 33472653
  c7s[40] = 3532558620
  bases[40] = 436274258
  masks[40] = 33472653
  c7s[41] = 3532558684
  bases[41] = 436274194
  masks[41] = 33472653
  c7s[42] = 3532559132
  bases[42] = 436274770
  masks[42] = 33472653
  c7s[43] = 3532559196
  bases[43] = 436274706
  masks[43] = 33472653
  c7s[44] = 3532559656
  bases[44] = 436275296
  masks[44] = 33472669
  c7s[45] = 3532559720
  bases[45] = 436275232
  masks[45] = 33472669
  c7s[46] = 3533081900
  bases[46] = 436273250
  masks[46] = 33472653
  c7s[47] = 3533081964
  bases[47] = 436273186
  masks[47] = 33472653
  c7s[48] = 3533082412
  bases[48] = 436273762
  masks[48] = 33472653
  c7s[49] = 3533082476
  bases[49] = 436273698
  masks[49] = 33472653
  c7s[50] = 3533082924
  bases[50] = 436274274
  masks[50] = 33472653
  c7s[51] = 3533082988
  bases[51] = 436274210
  masks[51] = 33472653
  c7s[52] = 3533083436
  bases[52] = 436274786
  masks[52] = 33472653
  c7s[53] = 3533083500
  bases[53] = 436274722
  masks[53] = 33472653
  c7s[54] = 3533083960
  bases[54] = 436275296
  masks[54] = 33472669
  c7s[55] = 3533084024
  bases[55] = 436275232
  masks[55] = 33472669
  vars = i64[20000]
  phis = i64[20000]
  rng = 1234567890123456789 + 1000003 ## i64
  samples = 1500 ## i64
  ci = 0 ## i64
  while ci < ncls
    c7 = c7s[ci] ## i64
    base = bases[ci] ## i64
    mask = masks[ci] ## i64
    n = 0 ## i64
    s = 0 ## i64
    done = 0 ## i64
    while done == 0
      a0 = base ^ s
      if in_g(a0) == 1 && c7_of(a0) == c7
        vars[n] = a0
        n += 1
      if s == mask
        done = 1
      else
        s = ((s - mask) & mask)
    sf = 0 ## i64
    sb = 0 ## i64
    sg = 0 ## i64
    sp = 0 ## i64
    t = 0 ## i64
    while t < samples
      rng = rng * 6364136223846793005 + 1442695040888963407
      w = sample_f7(rng >> 33, rng >> 7)
      x = (c7 - w) & 4294967295
      i = 0 ## i64
      while i < n
        phis[i] = phi_of(vars[i], x)
        i += 1
      heapsort(phis, n)
      f = 0 ## i64
      groups = 0 ## i64
      pad = 0 ## i64
      i = 0
      while i < n
        j = i ## i64
        while j < n && phis[j] == phis[i]
          j += 1
        sz = j - i
        f += 1
        groups += (sz + 3) / 4
        pad += (4 - (sz & 3)) & 3
        i = j
      sf += f
      sb += (f + 255) / 256
      sg += groups
      sp += pad
      t += 1
    << "CLASS [ci] n=[n] sumfib=[sf] sumbatch=[sb] sumgroups=[sg] sumpad=[sp] samples=[samples]"
    ci += 1
  0
main_run(0)
```

### A.5 (7319bba, inherited, not run here) `r16.c` (with `gen_r16data.py` writing its constants): the row-16 enumeration, 1,052,672 pairs (u, l)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "r16data.h"
#define ROR(x,n) (((x)>>(n))|((x)<<(32-(n))))
static u32 S0(u32 x){return ROR(x,2)^ROR(x,13)^ROR(x,22);}
static u32 S1(u32 x){return ROR(x,6)^ROR(x,11)^ROR(x,25);}
static u32 MAJ(u32 x,u32 y,u32 z){return (x&y)^(x&z)^(y&z);}
// rows: for member m (0=x,1=y), A12..A15 at [l*4+0..3], E12..E15 similarly.  W16 needed only for the difference check and K16: E16x = e16 given; A16 = E16 - A12 + S0(A15)+MAJ(A15,A14,A13)
int main(){
  // x2 conditions at row16 involve A15/A16/E15/E16 of x only (checked below generically for A,E; W conditions don't close at 16)
  FILE*fo=fopen("r16.bin","wb"); size_t total=0; uint64_t freeb[32];int nf=0;for(int b=0;b<32;b++)if(!((E16M>>b)&1))freeb[nf++]=b;
  static unsigned long long mask_by_u_cnt=0;
  for(int l=0;l<32;l++){
    if(LDW[l]!=0) continue; // W16 difference cell '=' requires dW16 == 0 (xor difference zero)
    size_t cnt=0;
    for(uint64_t t=0;t<(1ull<<nf);t++){
      u32 e=E16V; for(int i=0;i<nf;i++) if((t>>i)&1) e|=1u<<freeb[i];
      // member x
      u32 W16x=e-LBASE[l]; (void)W16x;
      u32 Ax12=LXA[l*4+0],Ax13=LXA[l*4+1],Ax14=LXA[l*4+2],Ax15=LXA[l*4+3];
      u32 Ex15=LXE[l*4+3];
      u32 Ax16=e-Ax12+S0(Ax15)+MAJ(Ax15,Ax14,Ax13);
      // member y: E16y = Ay12+Ey12+S1(Ey15)+CH(Ey15,Ey14,Ey13)+K16+W16y ; W16y=W16x+dW (dW=0 here)
      u32 Ay12=LYA[l*4+0],Ay13=LYA[l*4+1],Ay14=LYA[l*4+2],Ay15=LYA[l*4+3];
      u32 Ey12=LYE[l*4+0],Ey13=LYE[l*4+1],Ey14=LYE[l*4+2],Ey15=LYE[l*4+3];
      u32 chy=(Ey15&Ey14)^(~Ey15&Ey13);
      u32 Ey16=Ay12+Ey12+S1(Ey15)+chy+0xe49b69c1u+(e-LBASE[l])+LDW[l];
      u32 Ay16=Ey16-Ay12+S0(Ay15)+MAJ(Ay15,Ay14,Ay13);
      if((e&CEM_16)!=CEV_16)continue; if((e^Ey16)!=CED_16)continue;
      if((Ax16&CAM_16)!=CAV_16)continue; if((Ax16^Ay16)!=CAD_16)continue;
      u32 q=CEP_16&CEP_15; if(q && ((e^Ex15)&q))continue;
      int ok=1; u32 Aa[2]={0,0};
      for(int c=0;c<NX2;c++){
        u32 v1,v2;
        // k: 0=A,1=E ; i 15 or 16
        v1 = X2K1[c]==0 ? (X2I1[c]==16?Ax16:Ax15) : (X2I1[c]==16?e:Ex15);
        v2 = X2K2[c]==0 ? (X2I2[c]==16?Ax16:Ax15) : (X2I2[c]==16?e:Ex15);
        int a=(v1>>X2B1[c])&1,b=(v2>>X2B2[c])&1;
        if((X2OP[c]!=0)!=(a==b)){ok=0;break;}
      }
      if(!ok)continue;
      u32 u=e-LC16[l]; struct{u32 u;u32 l;}rec={u,(u32)l}; fwrite(&rec,8,1,fo); cnt++;
    }
    total+=cnt; printf("l=%d pairs=%zu\n",l,cnt);
  }
  fclose(fo); printf("total pairs %zu\n",total); return 0;}
```

### 

```python
# generates r16data.h (the constants r16.c needs) from spec6core.py's data
import sys; sys.path.insert(0, '.')
from spec6core import *
Lt = setup_l(); h = ["#include <stdint.h>", "typedef uint32_t u32;"]
def arr(name, vals): h.append("static const u32 %s[]={%s};" % (name, ",".join("0x%08xu" % (v & M32) for v in vals)))
for nm, sel in (('X', 0), ('Y', 1)):
    for key, idx in (('A', 0), ('E', 1)):
        arr("L%s%s" % (nm, key), [(Ld['tx'] if sel == 0 else Ld['ty'])[idx][i] for Ld in Lt for i in (12, 13, 14, 15)])
arr("LBASE", [Ld['base'] for Ld in Lt]); arr("LC16", [Ld['C16'] for Ld in Lt]); arr("LDW", [Ld['dW16'] for Ld in Lt])
for k in 'AE':
    for nm, i in (('M', 0), ('V', 1), ('D', 2), ('P', 3)): h.append("static const u32 C%s%s_16=0x%08xu;" % (k, nm, CELLS[k][16][i]))
h.append("static const u32 CEP_15=0x%08xu;" % CELLS['E'][15][3])
x16 = [t for t in X2 if max(t[1], t[5]) == 16]
h.append("static const int NX2=%d;" % len(x16))
col = lambda f: ",".join(str(f(t)) for t in x16)
h.append("static const int X2K1[]={%s},X2I1[]={%s},X2B1[]={%s},X2OP[]={%s},X2K2[]={%s},X2I2[]={%s},X2B2[]={%s};" % (
    col(lambda t: {'A': 0, 'E': 1, 'W': 2}[t[0]]), col(lambda t: t[1]), col(lambda t: t[2]), col(lambda t: 1 if t[3] == '=' else 0),
    col(lambda t: {'A': 0, 'E': 1, 'W': 2}[t[4]]), col(lambda t: t[5]), col(lambda t: t[6])))
h.append("static const u32 E16M=0x%08xu,E16V=0x%08xu;" % (CELLS['E'][16][0], CELLS['E'][16][1]))
open('r16data.h', 'w').write("\n".join(h) + "\n")
```

### A.6 (7319bba, inherited, not run here) `presence.py`: the presence word against all members of the table

```python
# presence.py: the presence word of Section 6.2 against all 1,042,240 members of the row-16 table (r16.bin: little-endian (u, l) uint32 pairs)
import struct, sys
sys.path.insert(0, '.')
from spec6core import PRES_C, PRES_P, PRES_S, M32
d = open(sys.argv[1], 'rb').read(); us = set()
for i in range(len(d) // 8): us.add(struct.unpack_from('<I', d, 8 * i)[0])
win = {((u + PRES_C) & M32) >> PRES_S & 255 for u in us}
print('pairs', len(d) // 8, 'distinct u', len(us), 'distinct windows', len(win), 'popcount(PRES_P)', bin(PRES_P).count('1'),
      'members with a clear window bit:', sum(1 for u in us if not (PRES_P >> ((((u + PRES_C) & M32) >> PRES_S) & 255)) & 1))
```

### A.7 (7319bba, inherited, not run here) `smc.c`, `lab.h`: the sequential Monte-Carlo estimator of q3 (Section 7.3)

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
  const char*all[]={0};(void)all;
  for(unsigned i=0;i<sizeof CHA/sizeof*CHA;i++)if(strlen(CHA[i].s)!=32)exit(90);
  for(unsigned i=0;i<sizeof CHE/sizeof*CHE;i++)if(strlen(CHE[i].s)!=32)exit(91);
  for(unsigned i=0;i<sizeof CHW/sizeof*CHW;i++)if(strlen(CHW[i].s)!=32)exit(92);
  memset(nx2row,0,sizeof nx2row);
  for(int c=0;c<NX2;c++){int r=X2[c].i1>X2[c].i2?X2[c].i1:X2[c].i2; x2row[r][nx2row[r]++]=c;}
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
int main(int argc,char**argv){
  if(argc>=3&&!strcmp(argv[1],"-t"))return selftest(argv[2]);
  if(argc<6){fprintf(stderr,"usage\n");return 2;}
  u64 seed=strtoull(argv[1],0,10); int NP=atoi(argv[2]),M=atoi(argv[3]),MT=atoi(argv[4]);
  init_all(); if(load_variants(argv[5])){fprintf(stderr,"variants\n");return 3;}
  build_r16(); Rng R;rseed(&R,seed);
  P *pop=malloc((size_t)NP*sizeof(P)),*pop2=malloc((size_t)NP*sizeof(P)); Rec*rec=malloc((size_t)NP*M*sizeof(Rec));
  double lg[40];int nst=0; double st16=(double)NPAIR/32.0/4294967296.0; lg[nst++]=log2(st16);
  printf("seed %llu NP %d M %d MT %d NVAR %ld pairs %ld\n",(unsigned long long)seed,NP,M,MT,NVAR,NPAIR);
  for(int i=0;i<NP;i++){long k=rbelow(&R,NPAIR);pop[i]=P0[pairL[k]];
    if(!(rowx(&pop[i],16,0,pairE[k])&&rowy(&pop[i],16,0))){fprintf(stderr,"init fail\n");return 4;}}
  double est=st16; int dead=0;
  for(int t=17;t<=22&&!dead;t++){
    u32 fm=CELL[1][t].m,fv=CELL[1][t].v; double w=(t<=21)?ldexp(1.0,-__builtin_popcount(fm)):1.0; long cnt=0;
    for(int i=0;i<NP;i++){P s=pop[i];
      for(int c=0;c<M;c++){ u32 a,b=0; if(t<=21)a=(r32(&R)&~fm)|fv; else{a=samp6(&R);b=samp7(&R);}
        if(apply_stage(&s,t,a,b)){rec[cnt].pi=i;rec[cnt].a=a;rec[cnt].b=b;cnt++;} } }
    double mean=w*(double)cnt/((double)NP*M); lg[nst++]=cnt?log2(mean):-1e9; est*=mean;
    printf("stage %d pass %ld mean_log2 %.5f\n",t,cnt,cnt?log2(mean):-1e9);
    if(!cnt){dead=1;break;}
    for(int i=0;i<NP;i++){long k=rbelow(&R,cnt);pop2[i]=pop[rec[k].pi];
      if(!apply_stage(&pop2[i],t,rec[k].a,rec[k].b)){fprintf(stderr,"resample fail\n");return 5;}}
    P*tmp=pop;pop=pop2;pop2=tmp; }
  if(dead){printf("RESULT seed %llu est 0 log2est -inf\n",(unsigned long long)seed);return 0;}
  /* tail rows 23..36: variant W8 (MT proposals per particle) and published W8 (same particle) */
  long tp=0,tpub=0,both=0; 
  for(int i=0;i<NP;i++){ P s=pop[i];
    for(int j=0;j<MT;j++){ u32 w8=VAR[rbelow(&R,NVAR)]; s.Wx[8]=w8;s.Wy[8]=w8+D8; tp+=tail_eval(&s); }
    s.Wx[8]=MX[8];s.Wy[8]=MY[8]; int ok=tail_eval(&s); tpub+=ok; }
  double tm=(double)tp/((double)NP*MT), tmp_=(double)tpub/NP;
  printf("tail variant passes %ld of %ld  mean_log2 %.5f ; published-W8 passes %ld of %d mean_log2 %.5f\n",tp,(long)NP*MT,tp?log2(tm):-1e9,tpub,NP,tpub?log2(tmp_):-1e9);
  double estv=est*tm, estp=est*tmp_;
  printf("RESULT seed %llu est %.17g log2est %.5f estpub %.17g log2estpub %.5f\n",(unsigned long long)seed,estv,estv>0?log2(estv):-1e9,estp,estp>0?log2(estp):-1e9);
  printf("STAGES"); for(int i=0;i<nst;i++)printf(" %.5f",lg[i]); printf(" tail %.5f\n",tp?log2(tm):-1e9);
  return 0;}
```

### 

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

### A.8 (7319bba, inherited, not run here) Preregistrations and results of the two studies

```text
PREREG q3 SMC, 222-class variant family (782,800 variants)
UTC timestamp: 2026-10-10T08:11:18Z
smc.c   SHA-256: 685297129cda47b247e6d19b1799d73b198e1511334e161fa7583ef6c1175a65
lab.h   SHA-256: bdefd6747d41727a378bc124c241db1f635275d3a2901b96a1c6c6b0e5c5e456
classes222.txt SHA-256: 6d501b22a872ba7a4ff2b88959a951b63aaab005a0c00036312df10008800c4f  (variant family input, 222 classes, 782,800 a0 values)
Command per replicate: ./smc <seed> 2048 512 16384 ../r37b/classes222.txt
NP=2048  M=512  MT=16384
Replicate seeds (32): 70000 70001 70002 70003 70004 70005 70006 70007 71000 71001 71002 71003 71004 71005 71006 71007 72000 72001 72002 72003 72004 72005 72006 72007 73000 73001 73002 73003 73004 73005 73006 73007 
Decision rule: one-sided 99% Student lower bound LB of the mean of the 32 linear (non-log) estimates
 (t = 2.4528, 31 df): LB = mean - t*sd/sqrt(32); q3_model = 2^(floor(100*log2(LB))/100).
All 32 replicates are reported; no reruns, no seed changes. Technical crashes may be fixed only by value-independent fixes, stated explicitly.
Tests before registration used seeds 1 and 2 only (outside the registered range).
```

### 

```text
PREREG q3 SMC study B (larger particle count), 222-class variant family (782,800 variants)
UTC timestamp: 2026-10-10T08:20:03Z
smc.c   SHA-256: 685297129cda47b247e6d19b1799d73b198e1511334e161fa7583ef6c1175a65   (unchanged from study 1, no logic change)
lab.h   SHA-256: bdefd6747d41727a378bc124c241db1f635275d3a2901b96a1c6c6b0e5c5e456
binary smc SHA-256: df086fed5867182f057f72fe4600ed2180e1134a137c3c2d0910f503b8758f30 (same binary as study 1)
Command per replicate: ./smc <seed> 8192 512 16384 ../r37b/classes222.txt
NP=8192  M=512  MT=16384
Replicate seeds (32): 74000 74001 74002 74003 74004 74005 74006 74007 75000 75001 75002 75003 75004 75005 75006 75007 76000 76001 76002 76003 76004 76005 76006 76007 77000 77001 77002 77003 77004 77005 77006 77007 
Decision rule: one-sided 99% Student lower bound LB of the mean of the 32 linear estimates
 (t = 2.4528, 31 df): LB = mean - t*sd/sqrt(32); q3_model = 2^(floor(100*log2(LB))/100).
All 32 replicates reported; no reruns, no seed changes.
```

### 

```text
# q3 SMC, 222-class variant family (782,800 variants) - RESULT
Preregistration: PREREG_q3_222.txt (sha256sum 5bab3530633c9aba086e45f7719ece655ffcb25dc802e0538ba87702101cd628, 2026-10-10T08:11:18Z). NP=2048, M=512, MT=16384, 32 seeds as registered, no reruns, no crashes, no code changes after registration.
Per-replicate outputs: out/rep_<seed>.txt. Runtime: 46 s total for 32 replicates (about 1.4 s each, single thread, nice 10).

Per-replicate log2 estimates (seeds 70000-70007, 71000-71007, 72000-72007, 73000-73007):
-74.056 -74.095 -73.991 -73.909 -74.152 -74.189 -73.990 -73.960 | -73.876 -74.038 -74.029 -73.978 -74.125 -73.950 -74.196 -73.905 | -74.006 -74.060 -73.775 -73.962 -74.031 -74.156 -73.915 -73.962 | -74.074 -73.901 -74.101 -73.969 -74.274 -73.928 -74.072 -74.097

- mean (linear) = 5.2259e-23 = 2^-74.0187
- relative sd = 0.0743 (sd of log2 estimates 0.108; mean of log2 = -74.0225)
- 99% one-sided lower bound (t=2.4528) = 5.0576e-23 = 2^-74.0659
- **q3_model = 2^-74.07** (floor to 0.01 of log2 LB)

Stage means (log2, average over 32 replicates): 16: -16.9944 (exact), 17: -13.0001, 18: -15.0036, 19: -6.0000, 20: -7.0005, 21: -1.0000, 22: -11.0094, rows 23..36 (variant W8): -4.0146 (pooled over all trials -4.0131).
Sum = -74.0225 (consistent with the log-mean).

Paired comparison, rows 23..36 on the same row-22 survivors (32 replicates x 2048 particles = 65,536 particles):
variant W8 (16384 draws per particle, 1,073,741,824 trials): 66,500,765 passes = 2^-4.0131; published W8 (one evaluation per particle): 4,271 of 65,536 = 2^-3.9396.
Same replicates with the published W8: mean estimate 2^-73.9457 (relative sd 0.197).
Caveats: the particle set after the row-22 resampling contains heavy duplication (about 500 distinct survivors per replicate), so the published-W8 count has an effective sample far below 65,536 and the 0.07 bit gap to the variant rate is not a clean significance test.

Deviations/notes: (1) the peer's pairing statistic ("523,611 row-22 survivors") was not defined precisely; I report per-particle published-W8 evaluations as above. (2) Variance is larger than the peer's (rel sd 0.074 vs 0.042), driven by the row-22 stage (about 500 survivors per replicate out of 1M children); per-replicate values fall -73.78..-74.27 rather than -73.99 +- 0.04. (3) Row-22 W6, W7 enter W21 only through the assumed s0(W6) difference T6 (exact check at row 22), as the specification implies.
Self-tests (./smc -t): rows 4..15 of all 32 (l) pass cells and two-bit conditions; row 16 enumeration gives 1,052,672 pairs with the per-l counts of the proof; F6/F7 samplers 0 violations in 2M draws; 200M random words, 3,170,857 in F7 (expected 3,173,828), all inside the given decomposition; all 782,800 variants satisfy the s0 difference T8 and the W8 cell and two-bit conditions.
```

### 

```text
# q3 SMC study B (NP=8192) - RESULT_b
Prereg: PREREG_q3_222_b.txt (sha256sum 6b1c9dbbbd1678b0ebecf89a14a9129b38776d88bc1d28848e63aeb7f03bd5de, UTC 2026-10-10T08:20:03Z). NP=8192, M=512, MT=16384, seeds 74000-77007 as registered, same smc.c/binary as study 1 (no change), no reruns. Outputs: out_b/rep_<seed>.txt. Runtime 113 s total.

Per-replicate log2 estimates (seed order):
-74.022 -73.967 -74.038 -73.934 -74.032 -74.059 -74.000 -74.017 -74.043 -74.070 -73.984 -73.942 -73.949 -73.956 -73.853 -73.965 -74.109 -73.985 -73.979 -73.927 -74.027 -73.983 -73.990 -74.065 -73.925 -74.057 -74.071 -74.052 -74.001 -74.025 -73.984 -73.976

- mean = 5.29886e-23 = 2^-73.9987
- relative sd = 0.0378
- 99% LB = 5.21196e-23 = 2^-74.0225
- q3_model = 2^-74.03
- stage means (log2, avg): 16: -16.9944, 17: -13.0002, 18: -15.0008, 19: -6.0000, 20: -7.0000, 21: -1.0000, 22: -10.9976, tail: -4.0066
- tail paired: variant W8 267282163/4294967296 = 2^-4.0062; published W8 16343/262144 = 2^-4.0036; published-W8 mean estimate 2^-73.9958
- Comparison with study 1 (NP=2048): mean 2^-74.0187, LB 2^-74.0659, rel sd 0.0743; study B mean 2^-73.9987, LB 2^-74.0225, rel sd 0.0378.
```

### A.9 (7319bba, inherited, not run here) `replay.c` (a copy of `smc.c` with replay hooks): the difference to `smc.c`, and the record

```diff
--- ../q3smc/smc.c	2026-10-10 17:10:59
+++ ../q3smc/replay.c	2026-10-10 17:38:55
@@ -89,6 +89,37 @@
   memset(nx2row,0,sizeof nx2row);
   for(int c=0;c<NX2;c++){int r=X2[c].i1>X2[c].i2?X2[c].i1:X2[c].i2; x2row[r][nx2row[r]++]=c;}
 }
+
+/* ---- replay (H3(a)): rebuild W0..W15 of a Step-3 success, re-check rows 14..36 for its own l and for every other l' in L* ---- */
+static u64 *seen; static const u64 SEEN_N=1ull<<24;
+static int seen_add(u64 h){h|=1;u64 i=(h*0x9e3779b97f4a7c15ull)>>40; while(seen[i]){if(seen[i]==h)return 0;i=(i+1)&(SEEN_N-1);}seen[i]=h;return 1;}
+static u64 hsucc(const P*s){u64 h=s->l+1;const int idx[]={6,7,8,16,17,18,19,20,21,22};for(int k=0;k<10;k++)h=(h^s->Wx[idx[k]])*0x100000001b3ull+0x9e3779b97f4a7c15ull*(k+1),h^=h>>29;return h;}
+/* returns 99 if rows 14..36 all pass for l'=lp with the given x words W[0..13] (x), else the failing row */
+static int replay_rows(const u32*W,const P*s,int lp){
+  P q=P0[lp]; u32 Y[16],X[16];
+  for(int i=0;i<14;i++)X[i]=W[i]; X[14]=W14X;X[15]=LW15[lp];
+  for(int i=0;i<6;i++)Y[i]=X[i]; Y[6]=X[6]+D6;Y[7]=X[7]+D7;Y[8]=X[8]+D8;Y[9]=MY[9];Y[10]=MY[10];Y[11]=X[11];Y[12]=X[12];Y[13]=X[13];
+  Y[14]=X[14]^W14DX;Y[15]=X[15]^W15DX;
+  for(int i=0;i<16;i++){q.Wx[i]=X[i];q.Wy[i]=Y[i];}
+  for(int t=14;t<16;t++){ if(!rowx(&q,t,1,X[t])||!rowy(&q,t,2))return t; }
+  for(int t=16;t<NR;t++){
+    u32 wx=s1(q.Wx[t-2])+q.Wx[t-7]+s0(q.Wx[t-15])+q.Wx[t-16], wy=s1(q.Wy[t-2])+q.Wy[t-7]+s0(q.Wy[t-15])+q.Wy[t-16];
+    q.Wy[t]=wy; if(!rowx(&q,t,1,wx)||!rowy(&q,t,2))return t; }
+  return 99;}
+static long R_succ,R_dist,R_ownfail,R_cosucc_pairs,R_cosucc_succ,R_fail[100],R_fail_other_hist[100];
+static void replay_success(const P*s){
+  R_succ++; if(!seen_add(hsucc(s)))return; R_dist++;
+  u32 W[16]; for(int i=6;i<=8;i++)W[i]=s->Wx[i]; for(int i=9;i<=13;i++)W[i]=MX[i];
+  u32 w14=W14X,w15=LW15[s->l];
+  W[5]=s->Wx[21]-s1(s->Wx[19])-w14-s0(W[6]);
+  W[4]=s->Wx[20]-s1(s->Wx[18])-W[13]-s0(W[5]);
+  W[3]=s->Wx[19]-s1(s->Wx[17])-W[12]-s0(W[4]);
+  W[2]=s->Wx[18]-s1(s->Wx[16])-W[11]-s0(W[3]);
+  W[1]=s->Wx[17]-s1(w15)-W[10]-s0(W[2]);
+  W[0]=s->Wx[16]-s1(w14)-W[9]-s0(W[1]);
+  if(replay_rows(W,s,s->l)!=99){R_ownfail++;return;}
+  int any=0; for(int lp=0;lp<32;lp++){ if(lp==s->l)continue; int r=replay_rows(W,s,lp); R_fail[r]++; if(r==99){R_cosucc_pairs++;any=1;} }
+  R_cosucc_succ+=any; }
 typedef struct { u32 pi,a,b; } Rec;
 static int selftest(const char*cls){
   init_all(); int bad=0;
@@ -116,7 +147,7 @@
   if(argc<6){fprintf(stderr,"usage\n");return 2;}
   u64 seed=strtoull(argv[1],0,10); int NP=atoi(argv[2]),M=atoi(argv[3]),MT=atoi(argv[4]);
   init_all(); if(load_variants(argv[5])){fprintf(stderr,"variants\n");return 3;}
-  build_r16(); Rng R;rseed(&R,seed);
+  build_r16(); Rng R;rseed(&R,seed); seen=calloc(SEEN_N,8);
   P *pop=malloc((size_t)NP*sizeof(P)),*pop2=malloc((size_t)NP*sizeof(P)); Rec*rec=malloc((size_t)NP*M*sizeof(Rec));
   double lg[40];int nst=0; double st16=(double)NPAIR/32.0/4294967296.0; lg[nst++]=log2(st16);
   printf("seed %llu NP %d M %d MT %d NVAR %ld pairs %ld\n",(unsigned long long)seed,NP,M,MT,NVAR,NPAIR);
@@ -138,11 +169,13 @@
   /* tail rows 23..36: variant W8 (MT proposals per particle) and published W8 (same particle) */
   long tp=0,tpub=0,both=0; 
   for(int i=0;i<NP;i++){ P s=pop[i];
-    for(int j=0;j<MT;j++){ u32 w8=VAR[rbelow(&R,NVAR)]; s.Wx[8]=w8;s.Wy[8]=w8+D8; tp+=tail_eval(&s); }
+    for(int j=0;j<MT;j++){ u32 w8=VAR[rbelow(&R,NVAR)]; s.Wx[8]=w8;s.Wy[8]=w8+D8; if(tail_eval(&s)){tp++;replay_success(&s);} }
     s.Wx[8]=MX[8];s.Wy[8]=MY[8]; int ok=tail_eval(&s); tpub+=ok; }
   double tm=(double)tp/((double)NP*MT), tmp_=(double)tpub/NP;
   printf("tail variant passes %ld of %ld  mean_log2 %.5f ; published-W8 passes %ld of %d mean_log2 %.5f\n",tp,(long)NP*MT,tp?log2(tm):-1e9,tpub,NP,tpub?log2(tmp_):-1e9);
   double estv=est*tm, estp=est*tmp_;
+  printf("REPLAY seed %llu successes %ld distinct_tested %ld own_l_fail %ld cosuccess_pairs %ld successes_with_cosuccess %ld\n",(unsigned long long)seed,R_succ,R_dist,R_ownfail,R_cosucc_pairs,R_cosucc_succ);
+  printf("REPLAYFAIL"); for(int r=0;r<100;r++)if(R_fail[r])printf(" row%d:%ld",r,R_fail[r]); printf("\n");
   printf("RESULT seed %llu est %.17g log2est %.5f estpub %.17g log2estpub %.5f\n",(unsigned long long)seed,estv,estv>0?log2(estv):-1e9,estp,estp>0?log2(estp):-1e9);
   printf("STAGES"); for(int i=0;i<nst;i++)printf(" %.5f",lg[i]); printf(" tail %.5f\n",tp?log2(tm):-1e9);
   return 0;}
```

### 

```text
# Replay for premise H3(a) (co-successes across L*)
NOT part of either preregistered sample (study 1 seeds 70000-73007, study B seeds 74000-77007). Seeds 90..99 (10 seeds; the coordinator asked for 90..93, the extra six were cheap), NP=2048, M=512, MT=16384, variant-W8 tail. Code: replay.c (copy of smc.c plus replay hooks; smc.c untouched). Raw output: out_replay/rep_<seed>.txt (concatenated in out_replay/raw_all.txt).
Commands: cc -O2 -march=native -o replay replay.c -lm ; for s in 90..99: nice -n 10 ./replay $s 2048 512 16384 ../r37b/classes222.txt. Runtime 33 s for all ten (heavy.lock held, single thread).

Method: each tail proposal passing rows 23..36 (particle already passed 16..22, so it passes every cell and printed two-bit condition of rows 16..36 for its own l) is a success. Words rebuilt: W6,W7 (row 22), W8 (variant), W9..W13 published, W14,W15 = lstar(l), W5..W0 by the inverse expansion exactly as specified. Re-check (i) own l: rows 14..36 of both members (y words: W0..W5,W11..W13 equal, W6/7/8 + D6/D7/D8, W9,W10 published y, W14/15 y of lstar; full forward schedule on both members, so the y side is an independent recomputation); (ii) each of the other 31 l': same W0..W13, W14,W15 = lstar(l'), rows 14..36, all cells and two-bit conditions. States of rows <= 13 are the published S's, as in the SMC.
Duplicates (same l, W6,W7,W8, W16..W22) are tested once per seed (64-bit hash, not across seeds).

Results (10 seeds summed): successes 20,669,447; distinct tested 19,620,436; own-l re-check failures 0; co-successes (success, l') pairs 0; successes with any co-success 0.
95% upper bound (rule of three): per success, 3/19,620,436 = 1.53e-7 (2^-22.65); per (success, l') pair, 3/(31 x 19,620,436) = 4.9e-9.
Where the other l' fail (608,233,516 pairs): row 16 in 607,845,872 (99.94%), row 17 in 387,644 (0.06%); none reaches row 18. Rows 14,15 always pass.
Caveats: successes share SMC ancestors (about 500 distinct row-22 survivors per seed, resampled), so they are not independent and the rule-of-three bound is a bound on this sampled, importance-weighted population, not an iid rate. The SMC is not a uniform sampler of true successes (weights are equal within a stage but the sample is conditioned on resampled ancestors), so the bound applies to the SMC's success distribution.
```

### A.10 (7319bba, inherited, not run here) `e2e.c`: end-to-end rates on random first blocks (its constants are generated by `gen_data.py` from `spec6core.py`)

```c
// e2e.c - end-to-end rates of the public filters of the 222-class A0-variant family (37-step SHA-256, ePrint 2026/1120) on random first blocks.
//   cc -O3 -mcpu=native -pthread -o e2e e2e.c -lm      (Linux: -march=native)
//   ./e2e classes222.txt r16.bin <seed> <log2 first blocks> <threads>
// Per first block: CV1 = F_37(IV,M0); class filter F7 on W7x = c7 - A_{-1}; per variant a0: W6x in F6 (good pair); u = W0 + s0(W1);
// row-16 table lookup (bitmap + sorted per-u l-masks).  Independent exact checks (generic trace + character cells) on sampled pairs.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <pthread.h>
#include <math.h>
#include <time.h>
typedef uint32_t u32; typedef uint64_t u64;
#include "e2e_data.h"
static inline u32 ror(u32 x, int n) { return x >> n | x << (32 - n); }
static inline u32 S0(u32 x) { return ror(x, 2) ^ ror(x, 13) ^ ror(x, 22); }
static inline u32 S1(u32 x) { return ror(x, 6) ^ ror(x, 11) ^ ror(x, 25); }
static inline u32 s0(u32 x) { return ror(x, 7) ^ ror(x, 18) ^ x >> 3; }
static inline u32 s1(u32 x) { return ror(x, 17) ^ ror(x, 19) ^ x >> 10; }
static inline u32 CH(u32 x, u32 y, u32 z) { return (x & y) ^ (~x & z); }
static inline u32 MAJ(u32 x, u32 y, u32 z) { return (x & y) ^ (x & z) ^ (y & z); }
#define D6 0x20000000u
#define T6 0x03c00800u
#define D7 0xfbc00800u
#define T7 0x017f8000u
#define D8 0xe0000000u
static inline int F6(u32 w) { return s0(w + D6) - s0(w) == T6; }
static inline int F7(u32 w) { return s0(w + D7) - s0(w) == T7; }

// ---- generic trace; row i is stored at index i+4 (rows -4..-1 = chaining value) ----
typedef struct { u32 A[44], E[44], W[40]; } Tr;
#define A_(t, i) (t)->A[(i) + 4]
#define E_(t, i) (t)->E[(i) + 4]
static void step(Tr *t, int i) {
  E_(t, i) = A_(t, i - 4) + E_(t, i - 4) + S1(E_(t, i - 1)) + CH(E_(t, i - 1), E_(t, i - 2), E_(t, i - 3)) + K[i] + t->W[i];
  A_(t, i) = E_(t, i) - A_(t, i - 4) + S0(A_(t, i - 1)) + MAJ(A_(t, i - 1), A_(t, i - 2), A_(t, i - 3));
}
static void trace(Tr *t, const u32 cv[8], const u32 *w16, int n) {
  for (int j = 0; j < 4; j++) { A_(t, -1 - j) = cv[j]; E_(t, -1 - j) = cv[4 + j]; }
  memcpy(t->W, w16, 64);
  for (int i = 16; i < n; i++) t->W[i] = s1(t->W[i - 2]) + t->W[i - 7] + s0(t->W[i - 15]) + t->W[i - 16];
  for (int i = 0; i < n; i++) step(t, i);
}
static void compress(u32 out[8], const u32 w[16]) {
  Tr t; trace(&t, IV, w, 37);
  for (int j = 0; j < 4; j++) { out[j] = IV[j] + A_(&t, 36 - j); out[4 + j] = IV[4 + j] + E_(&t, 36 - j); }
}

// ---- characteristic cells (mask, value, difference, '+' mask) and two-bit conditions ----
static u32 cell[3][41][4];
static void init_cells(void) {
  for (unsigned n = 0; n < sizeof CHR / sizeof *CHR; n++)
    for (int c = 0; c < 32; c++) {
      char s = CHR[n].s[c]; u32 b = 1u << (31 - c); u32 *m = cell[CHR[n].k][CHR[n].r + 4];
      if (s == '0' || s == '1' || s == 'u' || s == 'n') m[0] |= b;
      if (s == '1' || s == 'u') m[1] |= b;
      if (s == 'u' || s == 'n') m[2] |= b;
      if (s == '+') m[3] |= b;
    }
}
static int row_ok(const Tr *x, const Tr *y, int i, int chkW) {
  for (int k = 0; k < 2; k++) {
    const u32 *c = cell[k][i + 4], *X = k ? x->E : x->A, *Y = k ? y->E : y->A;
    if ((X[i + 4] & c[0]) != c[1] || (X[i + 4] ^ Y[i + 4]) != c[2]) return 0;
    if (k && i > -4) { u32 q = c[3] & cell[1][i + 3][3]; if (q && ((X[i + 4] ^ X[i + 3]) & q)) return 0; }
  }
  if (chkW && i >= 0) { const u32 *c = cell[2][i + 4]; if ((x->W[i] & c[0]) != c[1] || (x->W[i] ^ y->W[i]) != c[2]) return 0; }
  return 1;
}
static int x2_ok(const Tr *x, int r) {
  for (unsigned n = 0; n < sizeof X2 / sizeof *X2; n++) {
    const int *c = X2[n]; if ((c[1] > c[5] ? c[1] : c[5]) != r) continue;
    int a = (c[0] == 0 ? A_(x, c[1]) : c[0] == 1 ? E_(x, c[1]) : x->W[c[1]]) >> c[2] & 1;
    int b = (c[4] == 0 ? A_(x, c[5]) : c[4] == 1 ? E_(x, c[5]) : x->W[c[5]]) >> c[6] & 1;
    if ((c[3] == 0) != (a == b)) return 0;
  }
  return 1;
}

// ---- constants derived from the semi-free-start pair (as in spec6core.py) ----
static u32 SA[2][14], A1, A2, A3, A4, E5, E6, E7, C4, W8C, C6, K3C;
static void init_derived(void) {
  Tr t; trace(&t, CV0, MX, 14); for (int i = 0; i < 14; i++) SA[0][i] = A_(&t, i);
  A1 = SA[0][1]; A2 = SA[0][2]; A3 = SA[0][3]; A4 = SA[0][4]; E5 = E_(&t, 5); E6 = E_(&t, 6); E7 = E_(&t, 7);
  C4 = A4 - S0(A3) - MAJ(A3, A2, A1); W8C = E_(&t, 8) - A4 - S1(E7) - CH(E7, E6, E5) - K[8];
  C6 = E6 - 2 * A2 + S0(A1) - S1(E5) - K[6]; K3C = A3 - S0(A2);
  trace(&t, CV0, MY, 14); for (int i = 0; i < 14; i++) SA[1][i] = A_(&t, i);
}
static u32 k3of(u32 a0) { return K3C - MAJ(A2, A1, a0); }
static u32 c7of(u32 a0) { u32 e4 = a0 + C4; return E7 - A3 - k3of(a0) - S1(E6) - CH(E6, E5, e4) - K[7]; }
static int in_G(u32 a0) {
  u32 e4 = a0 + C4; if (e4 >> 29) return 0; u32 w = W8C - e4; return ((w >> 29) & 1) && ((w >> 1 & 1) != (w >> 12 & 1)) &&
    ((w >> 8 & 1) != (w >> 25 & 1)) && ((w >> 14 & 1) == (w >> 18 & 1));
}

// ---- data: classes (flattened variants with per-variant precomputation), row-16 table ----
#define NC 222
#define NV 782800
static u32 c7[NC], cstart[NC + 1], va0[NV], ve4[NV], vk3[NV];
static size_t g_np; static u64 *bitmap; static u32 *Us, *Um; static size_t nU;       // 2^32-bit set of u; sorted distinct u with l-masks
static u32 mask_of(u32 u) {
  if (!(bitmap[u >> 6] >> (u & 63) & 1)) return 0;
  size_t lo = 0, hi = nU; while (hi - lo > 1) { size_t m = (lo + hi) / 2; if (Us[m] <= u) lo = m; else hi = m; }
  return Um[lo];
}
static int cmp64(const void *a, const void *b) { u64 x = *(u64 *)a, y = *(u64 *)b; return x < y ? -1 : x > y; }
static void load(const char *cf, const char *rf) {
  FILE *f = fopen(cf, "r"); if (!f) { perror(cf); exit(1); }
  static char line[1 << 20]; int c = 0; u32 n = 0;
  while (fgets(line, sizeof line, f)) {
    char *p = line; c7[c] = strtoul(p, &p, 16); u32 cnt = strtoul(p, &p, 10); cstart[c] = n;
    for (u32 k = 0; k < cnt; k++) {
      u32 a = strtoul(p, &p, 16); va0[n] = a; ve4[n] = a + C4; vk3[n] = k3of(a);
      if (!in_G(a) || c7of(a) != c7[c]) { fprintf(stderr, "class file mismatch c=%d a0=%08x\n", c, a); exit(1); }
      n++;
    }
    c++;
  }
  fclose(f); cstart[c] = n; if (c != NC || n != NV) { fprintf(stderr, "bad class file %d %u\n", c, n); exit(1); }
  f = fopen(rf, "rb"); if (!f) { perror(rf); exit(1); }
  fseek(f, 0, SEEK_END); size_t np = ftell(f) / 8; rewind(f); u32 *raw = malloc(np * 8);
  if (fread(raw, 8, np, f) != np) exit(1); fclose(f);
  u64 *key = malloc(np * 8); for (size_t i = 0; i < np; i++) { if (raw[2 * i + 1] > 31) exit(2); key[i] = (u64)raw[2 * i] << 32 | raw[2 * i + 1]; }
  qsort(key, np, 8, cmp64); Us = malloc(np * 4); Um = calloc(np, 4); bitmap = calloc(1ull << 26, 8); nU = 0;
  for (size_t i = 0; i < np; i++) {
    u32 u = key[i] >> 32; if (!nU || Us[nU - 1] != u) Us[nU++] = u;
    Um[nU - 1] |= 1u << (key[i] & 31); bitmap[u >> 6] |= 1ull << (u & 63);
  }
  printf("table: %zu (u,l) pairs, %zu distinct u\n", np, nU); free(raw); free(key);
  g_np = np;
}

// ---- row 16 reference (per l in L*: rows 0..15 of both members of the semi-free-start pair with W14, W15 of l) ----
#ifndef NEG
#define NEG 0   /* negative control: -DNEG=1 must produce failures */
#endif
typedef struct { Tr tx, ty; u32 base, C16, dW16; } Ldat;
static Ldat Lt[32];
static void lstar(int l, u32 x[2], u32 y[2]) { x[0] = W14X; x[1] = LW15[l]; y[0] = W14X ^ 0x04400800u; y[1] = LW15[l] ^ 0x20000000u; }
static void setup_l(void) {
  for (int l = 0; l < 32; l++) {
    u32 x[2], y[2], wx[16], wy[16]; lstar(l, x, y); memcpy(wx, MX, 64); memcpy(wy, MY, 64);
    wx[14] = x[0]; wx[15] = x[1]; wy[14] = y[0]; wy[15] = y[1];
    Ldat *d = &Lt[l]; trace(&d->tx, CV0, wx, 16); trace(&d->ty, CV0, wy, 16);
    d->base = A_(&d->tx, 12) + E_(&d->tx, 12) + S1(E_(&d->tx, 15)) + CH(E_(&d->tx, 15), E_(&d->tx, 14), E_(&d->tx, 13)) + K[16];
    d->C16 = d->base + s1(x[0]) + MX[9]; d->dW16 = s1(y[0]) - s1(x[0]) + MY[9] - MX[9];
  }
}
static int row16_ok(int l, u32 e16) {
  Ldat *d = &Lt[l]; Tr X = d->tx, Y = d->ty;
  X.W[16] = e16 - d->base; Y.W[16] = X.W[16] + d->dW16; step(&X, 16); step(&Y, 16);
  return row_ok(&X, &Y, 16, 1) && x2_ok(&X, 16);
}

// ---- Lemma 4.1: W0..W13 of both members connecting cv to the rows of the variant a0 ----
static void words_from_cv(const u32 cv[8], u32 a0, u32 W[2][14]) {
  for (int m = 0; m < 2; m++) {
    Tr t; for (int j = 0; j < 4; j++) { A_(&t, -1 - j) = cv[j]; E_(&t, -1 - j) = cv[4 + j]; }
    for (int i = 0; i < 14; i++) A_(&t, i) = SA[m][i];
    A_(&t, 0) = a0;
    for (int i = 0; i < 14; i++) E_(&t, i) = A_(&t, i) + A_(&t, i - 4) - S0(A_(&t, i - 1)) - MAJ(A_(&t, i - 1), A_(&t, i - 2), A_(&t, i - 3));
    for (int i = 0; i < 14; i++)
      W[m][i] = E_(&t, i) - A_(&t, i - 4) - E_(&t, i - 4) - S1(E_(&t, i - 1)) - CH(E_(&t, i - 1), E_(&t, i - 2), E_(&t, i - 3)) - K[i];
  }
}
// independent exact check of one good pair; returns a bit set of failures (0 = all hold)
static int check_pair(const u32 cv[8], u32 a0, u32 w6x, u32 w7x, u32 u, u32 mask) {
  int bad = 0; u32 W[2][14], real = 0; words_from_cv(cv, a0, W);
  if (!F7(w7x) || !F6(w6x) || W[0][7] != w7x || W[0][6] != w6x) bad |= 1;           // W7x, W6x in F7/F6 and equal the Lemma words
  if (W[1][6] - W[0][6] != D6 || W[1][7] - W[0][7] != D7 || W[1][8] - W[0][8] != D8) bad |= 2;
  if (W[0][0] + s0(W[0][1]) != u) bad |= 4;
  for (int l = 0; l < 32; l++) {
    Tr t[2]; u32 w[16], x[2], y[2]; lstar(l, x, y); int ok = 1;
    for (int m = 0; m < 2; m++) {
      memcpy(w, W[m], 14 * 4); w[14] = m ? y[0] : x[0]; w[15] = m ? y[1] : x[1]; trace(&t[m], cv, w, 17);
      for (int i = 1; i < 14; i++) if (A_(&t[m], i) != SA[m][i]) bad |= 8;           // rows 0..13 reproduced
      if (A_(&t[m], 0) != a0) bad |= 8;
    }
    for (int i = -4; i < 16; i++) if (!row_ok(&t[0], &t[1], i, i != 6 && i != 7) || !x2_ok(&t[0], i)) ok = 0;
    if (!ok) bad |= 16;
    if (row_ok(&t[0], &t[1], 16, 1) && x2_ok(&t[0], 16)) real |= 1u << l;
  }
  if (real != mask) bad |= 32;                                                         // row 16 for all 32 l == table mask
  return bad;
}

// ---- driver ----
typedef struct { int id; u64 nb, seed, samp; u64 s[4][2], chk, fail, r16chk, r16fail, fchk, ffail; int firstbad; } Job;
static u64 sm64(u64 *x) { u64 z = (*x += 0x9e3779b97f4a7c15ull); z = (z ^ z >> 30) * 0xbf58476d1ce4e5b9ull; z = (z ^ z >> 27) * 0x94d049bb133111ebull; return z ^ z >> 31; }
static inline u64 rotl(u64 x, int k) { return x << k | x >> (64 - k); }
static u64 xo(u64 *s) { u64 r = rotl(s[1] * 5, 7) * 9, t = s[1] << 17; s[2] ^= s[0]; s[3] ^= s[1]; s[1] ^= s[2]; s[0] ^= s[3]; s[2] ^= t; s[3] = rotl(s[3], 45); return r; }
static void *worker(void *arg) {
  Job *J = arg; u64 sd = J->seed ^ (0x1234567ull * (J->id + 1)), st[4]; for (int i = 0; i < 4; i++) st[i] = sm64(&sd);
  u64 cnt = 0;
  for (u64 b = 0; b < J->nb; b++) {
    u32 m0[16], cv[8]; for (int k = 0; k < 8; k++) { u64 r = xo(st); m0[2 * k] = (u32)r; m0[2 * k + 1] = r >> 32; }
    compress(cv, m0); u32 am1 = cv[0], am2 = cv[1];
    u32 mj0 = MAJ(cv[0], cv[1], cv[2]), kap0 = 0 - S0(cv[0]) - mj0 - cv[7] - S1(cv[4]) - CH(cv[4], cv[5], cv[6]) - K[0];
    u64 n7 = 0, g = 0, r = 0, q = 0;
    for (int c = 0; c < NC; c++) {
      u32 w7 = c7[c] - am1; if (!F7(w7)) continue; n7++;
      for (u32 v = cstart[c]; v < cstart[c + 1]; v++) {
        u32 a0 = va0[v], w6 = C6 - am2 + MAJ(A1, a0, am1) - CH(E5, ve4[v], vk3[v] + am1);
        if (!F6(w6)) continue;
        g++;
        u32 e0 = a0 + cv[3] - S0(cv[0]) - mj0, W0 = a0 + kap0;
        u32 W1 = A1 + cv[2] - S0(a0) - MAJ(a0, cv[0], cv[1]) - cv[2] - cv[6] - S1(e0) - CH(e0, cv[4], cv[5]) - K[1], u = W0 + s0(W1);
        u32 mk = mask_of(u);
        if (mk) {
          r++; q += __builtin_popcount(mk);
          for (int l = 0; l < 32; l++) if (mk >> l & 1) { J->r16chk++; if (!row16_ok(l, Lt[l].C16 + u)) J->r16fail++; }
          J->fchk++; if (check_pair(cv, a0, w6, w7, u, mk ^ NEG)) J->ffail++;   // full exact check of every row-16 pass pair as well
        }
        if (++cnt % J->samp == 0) {
          int bad = check_pair(cv, a0, w6, w7, u, mk); J->chk++;
          if (bad) { J->fail++; if (J->firstbad < 5) { J->firstbad++; printf("FAIL flags=%d a0=%08x u=%08x mask=%08x\n", bad, a0, u, mk); } }
        }
      }
    }
    u64 x[4] = {n7, g, r, q}; for (int i = 0; i < 4; i++) { J->s[i][0] += x[i]; J->s[i][1] += x[i] * x[i]; }
  }
  return 0;
}
static void report(const char *nm, u64 n, u64 s1_, u64 s2_, double e) {
  double mean = (double)s1_ / n, var = ((double)s2_ - n * mean * mean) / (n - 1);
  printf("%-22s total %-14llu expected %-14.1f ratio %.5f  mean/blk %.4f var/blk %.3f VMR %.3f  z %+.2f\n", nm, (unsigned long long)s1_, e * n, mean / e,
         mean, var, var / mean, ((double)s1_ - e * n) / sqrt(var * n));
}
int main(int argc, char **argv) {
  if (argc < 6) { fprintf(stderr, "usage: e2e classes222.txt r16.bin seed log2blocks threads\n"); return 1; }
  init_cells(); init_derived(); load(argv[1], argv[2]); setup_l();
  u64 seed = strtoull(argv[3], 0, 0), nb = 1ull << atoi(argv[4]); int T = atoi(argv[5]); struct timespec t0, t1; clock_gettime(CLOCK_MONOTONIC, &t0);
  double p7 = 68157440.0 / 4294967296.0, p6 = 287309824.0 / 4294967296.0, Eg = 782800 * p7 * p6;
  pthread_t th[64]; Job jb[64]; memset(jb, 0, sizeof jb);
  for (int i = 0; i < T; i++) { jb[i].id = i; jb[i].nb = nb / T; jb[i].seed = seed; jb[i].samp = (u64)(Eg * nb / 16000) + 1; pthread_create(&th[i], 0, worker, &jb[i]); }
  Job S; memset(&S, 0, sizeof S);
  for (int i = 0; i < T; i++) {
    pthread_join(th[i], 0); S.nb += jb[i].nb; S.chk += jb[i].chk; S.fail += jb[i].fail; S.r16chk += jb[i].r16chk; S.r16fail += jb[i].r16fail; S.fchk += jb[i].fchk; S.ffail += jb[i].ffail;
    for (int k = 0; k < 4; k++) for (int j = 0; j < 2; j++) S.s[k][j] += jb[i].s[k][j];
  }
  clock_gettime(CLOCK_MONOTONIC, &t1); u64 n = S.nb;
  printf("seed %s  first blocks %llu  threads %d  time %.1f s\n", argv[3], (unsigned long long)n, T, (t1.tv_sec - t0.tv_sec) + 1e-9 * (t1.tv_nsec - t0.tv_nsec));
  report("passing classes", n, S.s[0][0], S.s[0][1], NC * p7);
  report("good pairs", n, S.s[1][0], S.s[1][1], Eg);
  report("row-16 pairs", n, S.s[2][0], S.s[2][1], Eg * nU / 4294967296.0);
  report("row-16 (pair,l)", n, S.s[3][0], S.s[3][1], Eg * g_np / 4294967296.0);
  double G = S.s[1][0], Gs = S.s[1][1] - G, Rs = S.s[2][1] - S.s[2][0], R = S.s[2][0], p1 = g_np / 4294967296.0, p2 = R / G;
  printf("H3: sum G(G-1) %.0f  sum R(R-1) %.0f  | p=%.6e: p^2 sum G(G-1) %.2f ratio %.3f | p=R/G=%.6e: %.2f ratio %.3f\n", Gs, Rs, p1, p1 * p1 * Gs,
         Rs / (p1 * p1 * Gs), p2, p2 * p2 * Gs, Rs / (p2 * p2 * Gs));
  printf("exact: sampled good pairs %llu failures %llu | row16_ok checks (pair,l) %llu failures %llu\n", (unsigned long long)S.chk, (unsigned long long)S.fail,
         (unsigned long long)S.r16chk, (unsigned long long)S.r16fail);
  printf("exact: full check_pair on all row-16 pass pairs %llu failures %llu\n", (unsigned long long)S.fchk, (unsigned long long)S.ffail);
  return 0;
}
```

### 

```python
# generates e2e_data.h (constants/tables) from the reference spec6core.py (data transcription only)
import sys; sys.path.insert(0, sys.argv[1]); import spec6core as s
def arr(n, v): return "static const u32 %s[%d]={%s};\n" % (n, len(v), ",".join("0x%08x" % x for x in v))
o = "// generated from spec6core.py by gen_data.py\n"
o += arr("K", s.K) + arr("IV", s.IV) + arr("CV0", s.CV0) + arr("MX", s.MX) + arr("MY", s.MY) + arr("LW15", s.LW15)
o += "static const u32 W14X=0x%08x;\n" % s.W14X
o += "static const struct{int k,r;const char*s;}CHR[]={\n"
kk = {'A': 0, 'E': 1, 'W': 2}
for k, t in (('A', s.CHA), ('E', s.CHE), ('W', s.CHW)):
    for r in sorted(t): o += '{%d,%d,"%s"},\n' % (kk[k], r, t[r])
o += "};\nstatic const int X2[%d][7]={\n" % len(s.X2)
for (k1, i1, b1, op, k2, i2, b2) in s.X2: o += "{%d,%d,%d,%d,%d,%d,%d},\n" % (kk[k1], i1, b1, 0 if op == '=' else 1, kk[k2], i2, b2)
o += "};\n"
open(sys.argv[2], "w").write(o)
```

### 

```text
# e2e: end-to-end rates of the 222-class A0-variant filters on random first blocks

Build/run (cwd = work dir; inputs ../r37b/classes222.txt, ../r37c/r16.bin; data header regenerated by `python3 -I gen/gen_data.py <r37pkg dir> e2e_data.h`):
    clang -O3 -mcpu=native -pthread -o e2e e2e.c -lm
    nice -n 10 ./e2e ../r37b/classes222.txt ../r37c/r16.bin 0x5eed0021 21 8 > run_a.out
    nice -n 10 ./e2e ../r37b/classes222.txt ../r37c/r16.bin 0x5eed0023 23 8 > run_b.out
(args: classes file, table, seed, log2 first blocks, threads; 8 threads, heavy.lock held). Raw output: run_a.out, run_b.out.
Negative control: `-DNEG=1` flips the expected mask in the full check and yields failures for every row-16 pair (checks are live).

| run | first blocks | passing classes (exp) | good pairs (exp, ratio) | row-16 pairs (exp, z) | (pair,l) (exp, z) | exact checks | H3 sumR(R-1) / p^2 sumG(G-1) | time |
|---|---|---|---|---|---|---|---|---|
| a | 2^21 | 7,400,134 (7,388,160) | 1,748,648,111 (1,742,708,500; 1.00341) | 424,363 (422,895; z +0.88) | 428,617 (427,128; z +0.88) | 16,051 sampled pairs + all 424,363 row-16 pairs + 428,617 row16_ok: 0 failures | 0.981 (p=1052672/2^32), 1.001 (p=R/G) | 12.1 s |
| b | 2^23 | 29,545,568 (29,552,640) | 6,978,649,557 (6,970,834,000; 1.00112) | 1,693,297 (1,691,580; z +0.51) | 1,710,031 (1,708,512; z +0.45) | 16,013 sampled + all 1,693,297 + 1,710,031 row16_ok: 0 failures | 0.979, 0.999 | 41.7 s |

Notes: z uses the observed per-first-block variance. Variance-to-mean ratios (a/b): passing classes 28.8/28.8, good pairs 23118/23133, row-16 pairs 6.62/6.61,
(pair,l) 6.69/6.68 (strongly overdispersed). Expected row-16 pairs use the 1,042,240 distinct u (E = g*1042240/2^32 per block); (pair,l) uses 1,052,672/2^32.
Exact checks per good pair: Lemma-4.1 words reproduce A rows 0..13 of both members, W7x/W6x in F7/F6 and equal the Lemma words, y-x = D6/D7/D8 on W6..W8,
u = W0+s0(W1), all cells and two-bit conditions of rows -4..15 (W-cells of rows 6,7 excluded) for all 32 l, and row 16 over all 32 l equals the table mask.
Expected counts: 222*p7 = 3.52295 classes, g = 830.988 good pairs per first block.
Source size: e2e.c 15 KB + generated e2e_data.h 3.8 KB (a bit over the 12 KB target).
```

### 

```text
table: 1052672 (u,l) pairs, 1042240 distinct u
seed 0x5eed0021  first blocks 2097152  threads 8  time 12.1 s
passing classes        total 7400134        expected 7388160.0      ratio 1.00162  mean/blk 3.5287 var/blk 101.474 VMR 28.757  z +0.82
good pairs             total 1748648111     expected 1742708500.0   ratio 1.00341  mean/blk 833.8204 var/blk 19275899.199 VMR 23117.567  z +0.93
row-16 pairs           total 424363         expected 422895.1       ratio 1.00347  mean/blk 0.2024 var/blk 1.339 VMR 6.616  z +0.88
row-16 (pair,l)        total 428617         expected 427127.9       ratio 1.00349  mean/blk 0.2044 var/blk 1.367 VMR 6.690  z +0.88
H3: sum G(G-1) 41880781093616  sum R(R-1) 2469276  | p=2.450943e-04: p^2 sum G(G-1) 2515829.43 ratio 0.981 | p=R/G=2.426806e-04: 2466521.75 ratio 1.001
exact: sampled good pairs 16051 failures 0 | row16_ok checks (pair,l) 428617 failures 0
exact: full check_pair on all row-16 pass pairs 424363 failures 0
```

### 

```text
table: 1052672 (u,l) pairs, 1042240 distinct u
seed 0x5eed0023  first blocks 8388608  threads 8  time 41.7 s
passing classes        total 29545568       expected 29552640.0     ratio 0.99976  mean/blk 3.5221 var/blk 101.338 VMR 28.772  z -0.24
good pairs             total 6978649557     expected 6970834000.0   ratio 1.00112  mean/blk 831.9199 var/blk 19244496.196 VMR 23132.632  z +0.62
row-16 pairs           total 1693297        expected 1691580.3      ratio 1.00101  mean/blk 0.2019 var/blk 1.334 VMR 6.607  z +0.51
row-16 (pair,l)        total 1710031        expected 1708511.7      ratio 1.00089  mean/blk 0.2039 var/blk 1.362 VMR 6.683  z +0.45
H3: sum G(G-1) 167233213983536  sum R(R-1) 9836086  | p=2.450943e-04: p^2 sum G(G-1) 10045902.45 ratio 0.979 | p=R/G=2.426396e-04: 9845687.20 ratio 0.999
exact: sampled good pairs 16013 failures 0 | row16_ok checks (pair,l) 1710031 failures 0
exact: full check_pair on all row-16 pass pairs 1693297 failures 0
```

### A.11 Raw records of this filing

F6/F7 exhaustive check (A.2), output of the four shards:

```text
SHARD 0 n6=75497472 n7=17039360 bad6=0 bad7=0
SHARD 1073741824 n6=68157440 n7=17039360 bad6=0 bad7=0
SHARD 2147483648 n6=75497472 n7=17039360 bad6=0 bad7=0
SHARD 3221225472 n6=68157440 n7=17039360 bad6=0 bad7=0
```

|G| (A.1): `G_count 12103680`.

Fibre statistics (A.4), totals of the three samples:

```text
sample 1: classes 222, samples per class 1500, sums over all (class, x): fibres 97773367 batches 515729 groups4 307829918 pad 57119672
sample 2: classes 222, samples per class 1500, sums over all (class, x): fibres 97466854 batches 514400 groups4 307679210 pad 56516840
sample 3: classes 222, samples per class 1500, sums over all (class, x): fibres 97649350 batches 515274 groups4 307705376 pad 56621504
```

End-to-end counted-program runs (Section 13.4; `measure.py seed 20000`: first_block, compress, `process_cv`, every operation counted):

```text
{"seed": "m1", "fb": 20000, "mean_ops": 15712.17435, "sd_mean": 541.0074889655026, "hit_fb": 3022, "classes": 70775, "good": 16298726, "r16": 3925, "max_ops": 2016232, "secs": 304}
{"seed": "m2", "fb": 20000, "mean_ops": 15683.5204, "sd_mean": 545.2558380542163, "hit_fb": 3085, "classes": 72425, "good": 16289842, "r16": 3873, "max_ops": 1592465, "secs": 306}
{"seed": "m3", "fb": 20000, "mean_ops": 15703.8577, "sd_mean": 538.6414376904523, "hit_fb": 3040, "classes": 71127, "good": 16360897, "r16": 3864, "max_ops": 2128397, "secs": 305}
{"seed": "m4", "fb": 20000, "mean_ops": 15115.944, "sd_mean": 532.1602362461896, "hit_fb": 2937, "classes": 69386, "good": 15812122, "r16": 3828, "max_ops": 2097442, "secs": 296}
{"seed": "m5", "fb": 20000, "mean_ops": 15873.49655, "sd_mean": 547.9052473683238, "hit_fb": 2980, "classes": 69238, "good": 16476779, "r16": 3997, "max_ops": 1634984, "secs": 298}
{"seed": "m6", "fb": 20000, "mean_ops": 15990.9249, "sd_mean": 557.8376438631258, "hit_fb": 3032, "classes": 70522, "good": 16647341, "r16": 4147, "max_ops": 1587650, "secs": 302}
{"seed": "m7", "fb": 20000, "mean_ops": 16376.2438, "sd_mean": 582.3397526786837, "hit_fb": 2967, "classes": 71410, "good": 17210020, "r16": 3990, "max_ops": 2008374, "secs": 302}
{"seed": "m8", "fb": 20000, "mean_ops": 15583.3621, "sd_mean": 552.1261502875324, "hit_fb": 3009, "classes": 69355, "good": 16272974, "r16": 3947, "max_ops": 1780535, "secs": 295}
```

Per-class statistics used by the ledger (`STATS` in `experiments/xtab.py`: class index, size, mean fibres, batches, four-groups, padding; mean of the three samples):

see `experiments/xtab.py`.

## Appendix B. This derivative: a direct row-16 mask table on d3ec5c41

**Base.** Submission d3ec5c41-c5b1-4b5a-b54d-838fbd4de535 (companygardener; claim 61.71473; in review when this was
built), read from its submission branch of the organizer repository Layr-Labs/hash-smash (commit
dad7eb42c1d458d24bdd4abc615543289096af01, parent 43ae27d), every file checked against the branch's blob ids. Its
candidate files by SHA-256 (first 16 hex digits): claim.json 1d02e7e4610869a3, proof.md a7c0e52b80c006cc,
experiments/xtab.py 682ed198ffcb83a3, experiments/manifest.json dc4655b19d0bf297, certificates/manifest.json
a3c78779269ab224. The two manifests are unchanged here; xtab.py, claim.json and proof.md differ only as listed below.

**The change.** In d3ec5c41 a valid lane whose presence window is set reads bit u of a 2^32-bit bitmap (8 counted
operations in lane 0, 9 in lanes 1..3), and a member then recovers its l-mask by a binary search of the sorted array
of the 1,042,240 members (132 operations). Here the l-mask is stored directly:

```text
Rmask[u] = OR { 2^l : (u, l) in the row-16 enumeration E }      for 0 <= u < 2^32,   one 256-bit word per u
build:   Rmask[u] := 0 for every u;   then for every (u, l) in E:  Rmask[u] := Rmask[u] | 2^l
lookup:  u := lane k of U reduced to 32 bits; m := Rmask[u]; V += cost; if m == 0: next lane; else rare path with mask m
```

E is the exhaustive enumeration of Section 6.2 (1,052,672 pairs; Appendix A.5), u is the same 32-bit value
u = W0 + s0(W1) mod 2^32 that d3ec5c41's probe used, and the four elements of L* whose row 16 cannot hold (0, 2, 16,
18) have no pair in E, so their bits are zero in every word.

**Lemma B.1 (pointwise equivalence).** For every u in [0, 2^32): Rmask[u] = 0 if and only if d3ec5c41's bitmap bit of
u is clear, and otherwise Rmask[u] is exactly the l-mask its binary search returns. *Proof.* After the build, Rmask[u]
is the OR of 2^l over the pairs of E with first coordinate u (zero if there is none). The bitmap bit of u is set iff E
has a pair (u, l), and the sorted array's entry for u is the OR of 2^l over those pairs. QED. Hence the two programs
take the same branch at every lookup, enumerate the same l in the same order on the rare path, run the same checks of
rows 16..36 and output the same pairs; the trials t, the events A_t, the good pairs, N_FB and the premises (H1-H5, H7,
H9) are those of d3ec5c41. Only the counted cost of the lookup changes.

**Program (`experiments/xtab.py`).** New: `mask_lookup` (the lookup above; it counts each primitive where it executes:
extraction 1 for lane 0, shr and and for lanes 1..3; the add of the table base; the load; the V addition; the branch on
zero; and asserts the totals PROBE_OPS = [5, 6, 6, 6]) and `Env.rmask` (Rmask[u], evaluated from its definition and
cached, as d3ec5c41's program evaluated its bitmap and binary search). Changed: `good_group` calls `mask_lookup` and
returns the mask with each hit; the rare path of `process_cv` uses that mask (V += 1, RARE_LOOKUP = 0); `PRE_ITEMS`
asserts that the five preprocessing items of Section 8.2 sum below PRE = 2^58; `selftest` gained one block (below).
Everything else, including `ledger()`, the experiments and their observation keys, is d3ec5c41's code. The V addition
is kept because d3ec5c41's count of 8 or 9 includes one and the cap of Section 10 holds only if every executed
operation reaches V.

**Build charge and memory.** Item (v) of Section 8.2: zeroing 2^32 words (store, pointer add, compare, branch: 4
operations each) and 1,052,672 OR-updates (load of the pair, 2^l, address add, load, or, store, loop: at most 10 each)
cost 17,190,395,904 operations (2^34.0009); the five items sum to 2^57.2787 < 2^58, so PRE, the claimed preprocessing
2^60.00155 and its charge in T are unchanged. Rmask holds 2^32 words of 32 bytes, 2^37 bytes; the bitmap (2^29 bytes)
and the sorted array are not needed; the memory total stays below 2^50 bytes (Section 14), and memory is reported only.

**Ledger.** `python3 experiments/xtab.py ledger`; only PROBE_OPS and RARE_LOOKUP differ from d3ec5c41's inputs.

| | d3ec5c41 | this version |
|---|---|---|
| lookup per present window; rare-path search | 8 or 9; 132 | 5 or 6; 0 |
| presence word and lookup per good pair | 6.914 | 6.258 |
| rows >= 16 per first block | 140.72 | 113.84 |
| vbar (data-dependent operations per first block) | 16431.31 | 15859.09 |
| V_MAX | 5,987,153,443,586,154,090,544 | 5,778,650,807,088,376,677,839 |
| vmax_fb | 84,694,938,870.125 | 84,591,095,557.625 |
| Pcap (Chebyshev) | 2^-24.018 | 2^-23.969 |
| mu0; N_FB | 0.49466252; 358,768,880,796,199,274 | the same |
| success bound | 0.3900000024 | 0.3900000003 |
| 2644 T | 10,005,628,052,435,696,944,197 | 9,797,125,415,937,815,688,179 |
| log2 T; claimed time_log2 | 61.7147233539; 61.71473 | 61.6843420399; 61.68435 |
| units per first block | 7.234 | 7.017 |
| preprocessing; memory | 2^60.00155; 2^50 | the same |

**Certificate.** With N = 2644 T = 9,797,125,415,937,815,688,179, exact integer comparison gives

    2644^100000 * 2^6168434 < N^100000 <= 2644^100000 * 2^6168435,

so 61.68434 < log2 T <= 61.68435 and time_log2 = 61.68435 is log2 T rounded up at the fifth decimal (the same test
that `ledger()` asserts as tight_up and tight_down):

```python
N, C, E, k = 9797125415937815688179, 2644, 100000, 6168435
a, b = N ** E, C ** E
assert (b << (k - 1)) < a <= (b << k)
```

**Equivalence runs** (d3ec5c41's program and this one, side by side, on every test the package runs). Both organizer
experiments, all 256 trials each, in the organizer's request format with seeds SHAKE-256("pkgR37a|<experiment>|<t>"):
the returned message pairs are byte-identical (`a0-sfs-r37`: 126 pairs; `a0-online-r37`: 4) and every observation is
identical except counted_ops. Instrumented, every bitmap probe of d3ec5c41's program (3,962 and 2,380) equals the new
lookup's zero test on the same u in the same order, every mask its binary search returned (22 and 3) equals the loaded
word, and on each of the 24 trials that report counted_ops the two counts differ by exactly 3 per lookup plus 132 per
member. `selftest` prints d3ec5c41's lines unchanged (F7 sampler, 9,556 fibre lanes and 5,882 good pairs against brute
force, 8,000 packed lanes, presence word) and then: Rmask against row 16 evaluated directly on 80 members drawn from
the row's fixed E16 bits and on 1,000 random u, 0 mismatches, lookup operations [5, 6, 6, 6]. The same side-by-side
comparison with the organizer's own trial seeds (public seed hashsmash-public-seed-v1 and this package's target
configuration, derived as the organizer's experiments/runner.py does): 124 and 2 returned pairs identical, 3,561 and
1,737 probes and 17 and 1 recovered masks equal, the counted_ops identity on all 23 trials that report it; and this
program's stdout for both organizer requests is byte-identical (same SHA-256) to the stdout of the organizer's intake
run in the pinned image python:3.12.12-slim-bookworm (both experiments 256 of 256 trials, replay identical).

**The enumeration E, re-run.** d3ec5c41 inherits E from 7319bba without re-running it. We re-enumerated it (numpy,
vectorized, from this program's own `setup_l`, `CELLS` and `X2`: every l in L*, every E16x with the row's fixed
x-bits, the cells of row 16 of both members with the `+` condition against row 15 and the two-bit conditions closing
at row 16, as `row16_ok`): 1,052,672 pairs (u, l) and 1,042,240 distinct u, as quoted in Section 6.2; pairs occur for
exactly the 28 l of `FEASIBLE_L` (none for 0, 2, 16, 18; the OR of all masks is fffafffa); 10,432 u carry two l. The
Rmask built from this E (zero, then OR) equals `Env.rmask` on 3,200 members (all 200 of them with two l included) and
is zero on 3,000 random non-members, and the presence word has no false negative on any of the 1,042,240 members.

**End-to-end run of this program.** `online()` of this `experiments/xtab.py` on 80,000 real first blocks (SHAKE-256
seeds 'r37a-1', 'r37a-2', 'r37a-3', 'r37a-4', 20,000 first blocks each; the table entries built on the fly as in the
experiments; every operation counted): mean 15,472 +- 272 counted operations per first block (fixed + data-dependent)
against the ledger's 15,910; 0.1511 first blocks with a passing class, 3.5564 passing classes and 816.7 good pairs per
first block, 2.4237e-04 row-16 members and 0.2187 lookups per good pair (exact: 1,042,240/2^32 = 2.4267e-4 and 7/32 =
0.21875); largest first block 2,262,982. For the same first blocks d3ec5c41's counting (this count plus 3 per lookup
and 132 per member, the identity checked trial by trial above) gives 16,034 +- 283 against its ledger's 16,482. The
seeds are ours, so these first blocks are not those of d3ec5c41's runs of Appendix A.11; the standard errors combine
the per-run standard errors of the mean.

**What else moved.** Besides the paragraph "This derivative" above Section 0 and the description of the lookup itself
(Sections 6.2, 8.2 item (v), 8.3, 9.1, 9.6, 9.7, 11.1, 14 and the last row of Section 16), only figures that follow
from the ledger: the title and the Claim line; the cost bullet of Section 0; vmax_fb in 9.8; vbar, Pcap, V_MAX and the
success bound in Section 10; the ledger block of Section 11 and every row of the sensitivity table 11.2 (recomputed
with the new constants); the study-A and 75-condition values in 7.4 and 15; Pcap in H7; the 50% cost and the
fibre-test share in H9; the operation count in Section 15; the counted-program rows of 13.4 (d3ec5c41's measurement is
kept and labelled; our re-run is added).
In claim.json: time_log2, the second restriction (one sentence naming this change), the cost and success restrictions,
and the ledger figures inside H1 and H5 (operation counts), H2 (study-A value), H4 (A_C sensitivity), H7 (Pcap) and H9
(sensitivity, share); every statement keeps its id, role and wording otherwise, and the evidence line ranges moved with
the inserted lines. The work for this version (ledger runs, the equivalence runs and the measurement above, about 1.3
CPU hours) added to d3ec5c41's development (Section 13.5) stays far inside DEV = 2^40 units.

**Credit.** Construction, x-indexed table, fibre test, counted program, ledger, premises, experiments and all text
outside this appendix, the paragraph above Section 0 and the passages listed above: companygardener (d3ec5c41). Reused
through d3ec5c41 and relied on by this change: winglock (7319bba: the row-16 enumeration of Appendix A.5 that fills
Rmask, the packed row-16 stage and its rare path; 6c77089c: L*), 0xshikhar (1f12a09a: packed lanes, presence word),
GordoAR (087a18c4: exact ledger and success floor). The idea of storing the l-mask directly, with a first ledger row,
is from GPT Luna's note D68 (an OpenAI model consulted by the submitter); its count of 4 or 5 per lookup left out the
V addition, which the native count above keeps. This derivative (Jbenisek, working with Claude Opus 5.5 in Claude
Code): the change, its counts, the recomputation, the certificate and the equivalence runs. None of the credited
authors reviewed it.
