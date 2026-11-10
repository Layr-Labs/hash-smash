# Collision attack on 37-step SHA-256: the ePrint 2026/1120 two-block attack with A0-variants of the Step-1 solution, 222 classes and packed good-pair groups, 2^62.7133

Track `sha256-r37-exploratory`, target `sha256-r37-prefix-v1`, cost model `collision-frontier-v5` (C = 2644).
Claim: `time_log2 = 62.7133` target compressions on every run, success probability at least 0.39 (0.3900000047 under the
stated premises), memory 2^34.2 bytes (reported only), nonuniform advice below 2^13 bytes.

The attack is the 37-step collision attack of Li, Zhang, Li, Liu, Qian and Zhu, "Pushing Collision Attacks on SHA-2
to 39 Steps" (IACR ePrint 2026/1120, CC BY), in the two-block memory-efficient framework of [LLWS26] (Li, Liu, Wang,
Shi, ePrint 2026/1080). We reuse the paper's characteristic and its published semi-free-start pair exactly as
transcribed and verified in the earlier filing 6c77089c (winglock), and the exact Step-2 filter sets F6, F7 of that
filing. The A0 freedom of the Step-1 solution (Section 4.3: the second-block word A0 carries no condition of the
characteristic, so S has 12,103,680 *variants* that differ from S only in A0, E4, W8 and in the first-block-dependent
words W0..W7), the c7 classes (Section 5.3) and the per-class bit-sliced W6 test are those of itseasypop's 1c36817
(63.47455), found independently by qkniep (b947b377, 64.0687); the proof, the preregistered q3 estimate, the premises
and the exact-rational ledger below are the ones of GordoAR's 087a18c4 (63.45545), which is the base of this filing.
**What this filing changes is the counted program and its accounting** (Sections 4.3 - 5.3, 7, 9 - 13; the machine
of the attack, its geometry and the premises about the characteristic are unchanged): (i) all 222 classes with at least
3,456 variants (782,800 variants; 087a18c4 used 64 classes of 3,600) are tested for W7 by one bit-sliced program whose
lanes are the classes (375 counted operations per first block instead of 10 per class); (ii) the W6 programs process
up to four batches of 256 variants at once, sharing the broadcast loads and folding the constants of each batch;
(iii) the lane scan reads 24-bit chunks through a table; (iv) the good pairs are processed in packed groups of four
64-bit lanes (u = W0 + s0(W1) of four variants in 34 operations); (v) the row-16 test reads one presence word for the
block of 256 values of u that contains the pair's u. The Step-3 probability q3 is re-estimated for the 222-class
family by a second preregistered study (Section 7.4).

## 0. Summary

- **Algorithm (Sections 4-8).** Messages M0 || M1 and M0 || M1' (128 bytes; padding adds the same third block).
  A first block M0 is two fresh uniform 256-bit words; CV1 = F_37(IV, M0) costs one unit. One bit-sliced program
  (lanes = the 222 fixed classes of variants; 85 classes of 3600 variants, 26 of 3584 and 111 of 3456, 782,800 in
  total) tests W7x = c7 - A_{-1} in F7 for all classes at once. For each passing class counted bit-sliced programs
  (up to four batches of 256 variants each) test the W6 filter; each variant passing both filters (a *good pair*)
  is put in a group of four; the group computes u = W0 + s0(W1) of its four variants in one word (four 64-bit
  lanes) and each variant's row-16 presence is read from a table of 2^24 presence words (one word per block of 256 values of
  u); a pair whose u is in the table gets its exact row-16 mask over the 32 elements of L*, and each row-16 pass is
  checked through row 36. A pair that follows every cell of rows 16..36 collides; it is verified with the target and
  output.
- **Rates (exact under H1).** Per first block: 222 p7 = 3.52295 passing classes and
  g = 782,800 p7 p6 = 830.988 good pairs (p7 = |F7|/2^32 = 2^-5.97763, p6 = |F6|/2^32 = 2^-3.90197).
  Measured on 2^23 real first blocks: 1.0038 (the 2^17.6 run: 1.0014) x g.
- **Probability (Section 7, H2).** For a good pair, q3 = average over l in L* of Pr[rows 16..36 follow every cell
  and printed two-bit condition]. Rows 16..22 have exactly the same probability for every variant (Lemma 7.1); the
  variant enters rows >= 23 only through W8 in W23 = s1(W21) + W16 + s0(W8) + W7 and W24 = s1(W22) + W17 + s0(W9) +
  W8. A second preregistered sequential Monte-Carlo estimate (32 replicates, W8 drawn from the 782,800 variants of the
  222 classes) gives mean 2^-73.9980 and a one-sided 99% lower bound 2^-74.0251: q3_model = 2^-74.0252 (the bound
  rounded down at the fourth decimal of its logarithm; H6). The stage factors equal the published-S estimate of
  6c77089c (2^-74.01) row by row; on the same 524,640 row-22 samples the rows 23..36 pass at 2^-4.001 with the
  variants' W8 and 2^-3.996 with the published W8.
- **Cost (Sections 9, 11).** N_FB = 357,577,563,488,735,156 = 2^58.31103 first blocks; per first block 1 unit
  plus 421 counted operations (30 + 375 + a control allowance of 16), plus on average 44,137.3 counted
  data-dependent operations (23,361 for the bit-sliced W6 programs, 2,686 for the lane scans' fixed part, 7,364 for the
  groups of four, 10,233 for the per-pair operations, 326 per-first-block setup, 53 control and 116 for the row-16 path), all capped
  by V_MAX. T = A_C + A_S + DEV + N_FB + (N_FB 421 + V_MAX + overshoot + preprocessing + final)/C + 6 =
  9,995,711,239,180,937,961,565 / 1322 = 2^62.713293, claimed 62.7133.
- **Premises (Section 12).** H1 uniform independent chaining values; H2 q3 >= 2^-74.0252 for the variants (H6 fixes the
  level at the printed bound); H3 given one success, the expected number of further successes in the same first block is
  small (<= 2^-9.4); H4 advice allowances (A_C = 2^60, A_S = 2^50, DEV = 2^40, as in the earlier filings); H5
  counted word-RAM pricing of the bit-sliced W7 and W6 programs and of the four-lane groups (no target compression
  is priced this way: every compression is charged one unit). Without bit-slicing the W6 test: 64.91364; with
  scalar u computations instead of the four-lane groups: 63.11917.
- **Checks.** Exhaustive: |G| = 12,103,680; the 222 classes (sizes 3600, 3584, 3456); F6, F7 sizes and affine
  decompositions. End to end on real first blocks (Section 13): 2^23 and 2^17.6 real first blocks with all 222 classes: passing classes 1.0024 x and 1.0052 x the expectation (the count is overdispersed, variance 28.8 x mean on 2 x 10^7 uniform words, so +2.4 standard deviations at 2^23), good pairs 1.0038 x and 1.0014 x, row-16 passes 0.9985 x and 1.0000 x; 56,000 sampled good pairs checked exactly, 0 failures. The counted program on 100 further
  first blocks: every lane of every bit-sliced filter equals the scalar definition, the four-lane groups equal the
  scalar u on every good pair, every good pair satisfies the Step-2 equations; sampled good pairs follow every cell of
  rows -4..16. Semi-free-start collisions with variant dense parts (W8 different from the published pair) verified with the
  repository's `verifier/hash_functions._compress`. For 33,150 Step-3 successes of the SMC with the 222-class W8, none of the other
  31 elements of L* also succeeds. Two organizer experiments (Section 13.3) repeat the semi-free-start construction and
  the online program on organizer seeds.

## 1. Target, cost model and output

- **Target** sha256-r37-prefix-v1: SHA-256 steps 0..36 on every padded block, the standard IV once, FIPS 180-4
  padding, feed-forward, all eight digest words (repository `verifier/hash_functions.digest(m, "sha256", 37)`).
  The output is two distinct complete messages with equal digests, verified with the target before output.
- **Cost model** collision-frontier-v5: one 37-step target compression = 1 unit; every other executed 256-bit
  word-RAM primitive (load, store, add/sub, and/or/xor/not, shift/rotation, compare, branch, uniform random word)
  = 1/C unit with C = 2644. Immediates and shift amounts are instruction fields; 64 registers. Memory is reported
  only. Success must be at least 0.39 over fresh coins.
- **Notation.** In step i, E_i = A_{i-4} + E_{i-4} + S1(E_{i-1}) + CH(E_{i-1}, E_{i-2}, E_{i-3}) + K_i + W_i and
  A_i = E_i - A_{i-4} + S0(A_{i-1}) + MAJ(A_{i-1}, A_{i-2}, A_{i-3}) (mod 2^32); (A_{-1..-4}, E_{-1..-4}) = (a, b, c,
  d, e, f, g, h) of the incoming chaining value. F_R(cv, B) is the R-step compression with feed-forward; its output
  is cv + (A_{R-1}, A_{R-2}, A_{R-3}, A_{R-4}, E_{R-1}, E_{R-2}, E_{R-3}, E_{R-4}).

## 2. Sources, credit, and what is new

- [LZLLQZ26] Y. Li, Z. Zhang, M. Li, F. Liu, H. Qian, J. Zhu, "Pushing Collision Attacks on SHA-2 to 39 Steps",
  IACR ePrint 2026/1120: the 37-step characteristic (Table 15), its two-bit conditions (Table 16), the 37-step SFS
  pair (Table 17) and the three-step attack (Step 1: SAT solve of the dense part, 2^41.3; Step 2: random first
  blocks filtered on W6, W7; Step 3: the (W14, W15) freedom). Its stated total is 2^79.1 (expected work).
- [LLWS26] Y. Li, F. Liu, G. Wang, J. Shi, "Pushing the limit of memory-efficient collision attack framework for
  SHA-2", ePrint 2026/1080 (CRYPTO 2026): the framework. [LLW24] Y. Li, F. Liu, G. Wang, EUROCRYPT 2024: the tool.
- Filing 6c77089c (winglock, 74.22669): the transcription of Tables 15-17 (checked twice against the PDF and
  against the SFS pair), the member orientation, the reading of '+', the corrected two-bit condition
  A15[29] = A17[29], the exact Step-2 sets F6, F7 (Lemma 3 there), the exact set L* (|L*| = 32), and the SMC design
  for q3. Filing dd6656d (Th0rgal) published the affine decomposition of F6, F7 that our bit-sliced filter tests.
  We re-derived and re-checked everything we use with our own code (Section 13); we did not execute their code.
- Filing 6eeefb64 (sha256-r32-exploratory, promoted after organizer review): the measured re-run of the [LLWS26]
  35-step characteristic search (593,858 solver CPU-seconds, credited there to mitchuski's #396) and the calibrated
  price of a solver CPU-second (2^32.796 primitive operations), which Section 11.3 uses to bound the allowance A_C.
- Filings 1c36817 (itseasypop) and b947b377 (qkniep): the A0 freedom of the Step-1 solution, the variant family G, the
  c7 classes and the bit-sliced W6 test per class (1c36817), the table-indexed variant test (b947b377), and the
  first-block-level success analysis. Filing 087a18c4 (GordoAR): the preregistered q3 estimate for 64 classes, H6, H7
  and the exact-rational ledger, which this proof takes over. We ran 087a18c4's `a0core.py ledger` and reproduced its
  printed ledger (63.45545) before changing the program, and we re-derived everything else with our own code.
- **New here.** (i) All 222 classes with at least 3,456 variants and their one-program W7 test (Sections 5.3, 9.2);
  (ii) W6 programs for up to four batches with shared broadcast loads and per-batch constants (Section 9.3); (iii) the
  lane scan by 24-bit chunks (Section 9.3); (iv) the packed four-lane group computation of u (Section 9.4);
  (v) the block presence table of row 16 (Section 9.4); (vi) a second preregistered estimate of q3 for the 222-class
  family and the matching exact accounting (Sections 7, 10, 11).

## 3. The characteristic (from the paper, as transcribed in 6c77089c; verified here)

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

Rows -4..3 are entirely `=`: **A0..A3 and E0..E3 carry no condition** (they carry no difference because the
chaining value is common and A0..A5, E4, E5 have no difference).

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

F_37(CV, M) = F_37(CV, M') = the printed hash, under our code and under the repository's `_compress`; every cell of
rows -4..36 and every printed two-bit condition holds with x = M', y = M (our checks: `sfs.c`, `a0core.py`).

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
(each step inverted for its new coordinate). W8..W13 do not depend on CV1. *Proof.* Substitution; the selftest
of `a0core.py` and `sfs.c` checks the reproduction (and the inverse) on every constructed pair.

### 4.3 The A0-variants (new)

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
W8x[8] != W8x[25], W8x[14] = W8x[18]}**. Exhaustive enumeration of all 2^32 words: |G| = 12,103,680 = 2^23.529. The
published A0 (1b21ce20) is in G.

**Lemma 4.3 (validity).** For a0 in G, every chaining value CV1 whose words (Lemma 4.1 with A0 = a0) satisfy the
filters W7x in F7 and W6x in F6 (Section 5.1), and every l in L* (Section 6), the pair follows every cell of rows
-4..15 of A, E and W except the XOR cells of W6 and W7, and every printed two-bit condition closing at a row <= 15
except those on W6, W7; and every modular difference that enters the message expansion (W6..W15 and
s0(W6..W15), s1(W14), s1(W15)) equals that of the published pair. *Proof.* Lemma 4.2 for E4, W8 and d6, d7; the
filters for s0(W6), s0(W7) (Section 5.1); everything else is S's or l's. *Checks:* 300 random (CV1, a0) pairs
passing the filters x all 32 l; 16,000 good pairs of the online program on real first blocks (rows -4..16); the
organizer experiment `a0-online-r37` (all 32 l on sampled good pairs).

So a variant changes A0, E0..E4 and W0..W8 only. W8 is the only changed word that enters the expansion beyond W8
itself (W23 via s0(W8), W24 directly); Section 7 shows this is all that can change q3.

## 5. Step 2 with variants

### 5.1 The exact filters

The characteristic fixes the modular differences of W21, W22, W23; with S (or any variant) fixed, the only remaining
requirements on W6, W7 (6c77089c, Lemma 3) are W6x in F6 and W7x in F7, where F_k = {w : s0(w + d_k) - s0(w) = t_k
mod 2^32}, d6 = 20000000, t6 = 03c00800, d7 = fbc00800, t7 = 017f8000. |F7| = 68,157,440 and |F6| = 287,309,824
(exhaustive). By the carry pattern of w + d (s0 is linear), each set is a disjoint union of affine spaces:

```text
F6: [w29=0, 14^18=0, 8^25=1, 1^12=0]                                                    2^28 words
    [w29=1, w30=0, 14^18=0, 15^19=0, 8^25=1, 9^26=1, 1^12=0, 2^13=0]                      2^24 words
    [w29=1, w30=1, 14^18=0, 15^19=0, 16^20^31=0, 8^25=1, 9^26=1, 10^27^31=1, 1^12=0, 2^13=0, 3^14^31=0]  2^21
F7: [w11=0, w22=1, w26=1, 1^18^22=1, 9^26^30=1, 0^11^28=0]                                2^26 words
    [w11=1, w12=0, w22=0, w23=1, w26=0, w27=1, 1^18^22=0, 2^19^23=1, 9^26^30=0, 10^27^31=1, 0^11^28=1, 1^12^29=0]  2^20
```

(`i^j=b`: bit i XOR bit j of w equals b.) Both decompositions agree with the definitions on 200,000 random words
and sum to the exhaustive sizes.

For a variant a0 and CV1 the filter words are (member x, from Lemma 4.1):

```text
W7x = c7(a0) - A_{-1},           c7(a0) = ab9a1763 + MAJ(A2, A1, a0) - CH(E6, E5, a0 + C4)
W6x = C6 - A_{-2} + MAJ(A1, a0, A_{-1}) - CH(E5, a0 + C4, E3),   E3 = K3C - MAJ(A2, A1, a0) + A_{-1}
C6 = E6 - 2 A2 + S0(A1) - S1(E5) - K6 = f538a8f7,   K3C = A3 - S0(A2) = 478132ed
```

(c7(1b21ce20) = d296fb78, the published constant.)

### 5.2 Lemma 5.1 (distribution, per variant)

Under H1 (CV1 uniform), for every fixed variant a0: Pr[W7x in F7] = p7 = |F7|/2^32 = 2^-5.97763 and
Pr[W6x in F6 | W7x in F7] = p6 = |F6|/2^32 = 2^-3.90197 exactly; conditioned on both, (W0..W5) is uniform on
(2^32)^6, (W6, W7) is uniform on F6 x F7, and they are independent. For every l in L*, (W16, ..., W21) is then a
bijective image of (W0..W5) for fixed (W6, W9..W15), hence iid uniform and independent of (W6, W7).
*Proof.* Lemma 4.1 (bijection for fixed a0) and the inverse expansion W5 = W21 - s1(W19) - W14 - s0(W6),
W4 = W20 - s1(W18) - W13 - s0(W5), ..., W0 = W16 - s1(W14) - W9 - s0(W1). (6c77089c's Lemma 2, for each variant.)

### 5.3 The c7 classes and the selection

c7(a0) takes only **22,976 distinct values on G** (exhaustive). A *class* is G intersected with one value of c7.
For all variants of one class and a given CV1, W7x is the same word, so one membership test decides the W7 filter of
the whole class. The 222 classes used here are all the classes with at least 3456 variants: 85 classes have 3600
variants, 26 have 3584 and 111 have 3456 (exhaustive; the next class has 1856), taken in the order of decreasing
size, ties by smaller c7 (the first 64 are the classes of 1c36817 and 087a18c4); 782,800 variants in all. Each class
equals {base XOR s : s subset of mask, s in G, c7 = the class value} for the descriptors below (c7, base, mask;
checked exhaustively: the member counts above; the masks have 14 to 16 bits):

```text
cc968c4c 1c010142 01fec08d  |  cc968c5c 1c010112 01fec08d  |  cc968c6c 1c010122 01fec08d  |  cc968c7c 1c010132 01fec08d
cc968c8c 1c010102 01fec08d  |  cc968e1c 1c010352 01fec08d  |  cc968e2c 1c010362 01fec08d  |  cc968e3c 1c010372 01fec08d
cc968e4c 1c010342 01fec08d  |  cc968e5c 1c010312 01fec08d  |  cc968e6c 1c010322 01fec08d  |  cc968e7c 1c010332 01fec08d
cc968e8c 1c010302 01fec08d  |  cc96901c 1c010152 01fec48d  |  cc96902c 1c010162 01fec48d  |  cc96903c 1c010172 01fec48d
cc96904c 1c010542 01fec08d  |  cc96905c 1c010512 01fec08d  |  cc96906c 1c010522 01fec08d  |  cc96907c 1c010532 01fec08d
cc96908c 1c010502 01fec08d  |  ce968d1c 1e010052 01fec08d  |  ce968d2c 1e010062 01fec08d  |  ce968d3c 1e010072 01fec08d
ce968d4c 1e010042 01fec08d  |  ce968d5c 1e010012 01fec08d  |  ce968d6c 1e010022 01fec08d  |  ce968d7c 1e010032 01fec08d
ce968d8c 1e010002 01fec08d  |  ce968f1c 1e010252 01fec08d  |  ce968f2c 1e010262 01fec08d  |  ce968f3c 1e010272 01fec08d
ce968f4c 1e010242 01fec08d  |  ce968f5c 1e010212 01fec08d  |  ce968f6c 1e010222 01fec08d  |  ce968f7c 1e010232 01fec08d
ce968f8c 1e010202 01fec08d  |  ce96911c 1e010452 01fec08d  |  ce96912c 1e010462 01fec08d  |  ce96913c 1e010472 01fec08d
ce96914c 1e010442 01fec08d  |  ce96915c 1e010412 01fec08d  |  ce96916c 1e010422 01fec08d  |  ce96917c 1e010432 01fec08d
ce96918c 1e010402 01fec08d  |  ce96931c 1e010652 01fec08d  |  ce96932c 1e010662 01fec08d  |  ce96933c 1e010672 01fec08d
ce96934c 1e010642 01fec08d  |  ce96935c 1e010612 01fec08d  |  ce96936c 1e010622 01fec08d  |  ce96937c 1e010632 01fec08d
ce96938c 1e010602 01fec08d  |  d2968d1c 1a010052 01fec08d  |  d2968d2c 1a010062 01fec08d  |  d2968d3c 1a010072 01fec08d
d2968d4c 1a010042 01fec08d  |  d2968d5c 1a010012 01fec08d  |  d2968d6c 1a010022 01fec08d  |  d2968d7c 1a010032 01fec08d
d2968d8c 1a010002 01fec08d  |  d2968f1c 1a010252 01fec08d  |  d2968f2c 1a010262 01fec08d  |  d2968f3c 1a010272 01fec08d
d2968f4c 1a010242 01fec08d  |  d2968f5c 1a010212 01fec08d  |  d2968f6c 1a010222 01fec08d  |  d2968f7c 1a010232 01fec08d
d2968f8c 1a010202 01fec08d  |  d296911c 1a010452 01fec08d  |  d296912c 1a010462 01fec08d  |  d296913c 1a010472 01fec08d
d296914c 1a010442 01fec08d  |  d296915c 1a010412 01fec08d  |  d296916c 1a010422 01fec08d  |  d296917c 1a010432 01fec08d
d296918c 1a010402 01fec08d  |  d296931c 1a010652 01fec08d  |  d296932c 1a010662 01fec08d  |  d296933c 1a010672 01fec08d
d296934c 1a010642 01fec08d  |  d296935c 1a010612 01fec08d  |  d296936c 1a010622 01fec08d  |  d296937c 1a010632 01fec08d
d296938c 1a010602 01fec08d  |  cc969228 1c010760 01fec09d  |  cc969238 1c010760 01fec09d  |  cc969248 1c010740 01fec09d
cc969258 1c010700 01fec0dd  |  cc969268 1c010720 01fec09d  |  cc969278 1c010720 01fec09d  |  cc969288 1c010700 01fec09d
cc969448 1c010940 01fec09d  |  cc969458 1c010900 01fec0dd  |  cc969468 1c010920 01fec09d  |  cc969478 1c010920 01fec09d
cc969488 1c010900 01fec09d  |  ce969528 1e010860 01fec09d  |  ce969538 1e010860 01fec09d  |  ce969548 1e010840 01fec09d
ce969558 1e010800 01fec0dd  |  ce969568 1e010820 01fec09d  |  ce969578 1e010820 01fec09d  |  ce969588 1e010800 01fec09d
d2969528 1a010860 01fec09d  |  d2969538 1a010860 01fec09d  |  d2969548 1a010840 01fec09d  |  d2969558 1a010800 01fec0dd
d2969568 1a010820 01fec09d  |  d2969578 1a010820 01fec09d  |  d2969588 1a010800 01fec09d  |  cc8e8c4c 1c010142 01fec08d
cc8e8c5c 1c010112 01fec08d  |  cc8e8c6c 1c010122 01fec08d  |  cc8e8c7c 1c010132 01fec08d  |  cc8e8c8c 1c010102 01fec08d
cc8e8e1c 1c010352 01fec08d  |  cc8e8e2c 1c010362 01fec08d  |  cc8e8e3c 1c010372 01fec08d  |  cc8e8e4c 1c010342 01fec08d
cc8e8e5c 1c010312 01fec08d  |  cc8e8e6c 1c010322 01fec08d  |  cc8e8e7c 1c010332 01fec08d  |  cc8e8e8c 1c010302 01fec08d
cc8e901c 1c010152 01fec48d  |  cc8e902c 1c010162 01fec48d  |  cc8e903c 1c010172 01fec48d  |  cc8e904c 1c010542 01fec08d
cc8e905c 1c010512 01fec08d  |  cc8e906c 1c010522 01fec08d  |  cc8e907c 1c010532 01fec08d  |  cc8e908c 1c010502 01fec08d
cc8e9228 1c010760 01fec09d  |  cc8e9238 1c010760 01fec09d  |  cc8e9248 1c010740 01fec09d  |  cc8e9258 1c010700 01fec0dd
cc8e9268 1c010720 01fec09d  |  cc8e9278 1c010720 01fec09d  |  cc8e9288 1c010700 01fec09d  |  cc8e9448 1c010940 01fec09d
cc8e9458 1c010900 01fec0dd  |  cc8e9468 1c010920 01fec09d  |  cc8e9478 1c010920 01fec09d  |  cc8e9488 1c010900 01fec09d
ce8e8d1c 1e010052 01fec08d  |  ce8e8d2c 1e010062 01fec08d  |  ce8e8d3c 1e010072 01fec08d  |  ce8e8d4c 1e010042 01fec08d
ce8e8d5c 1e010012 01fec08d  |  ce8e8d6c 1e010022 01fec08d  |  ce8e8d7c 1e010032 01fec08d  |  ce8e8d8c 1e010002 01fec08d
ce8e8f1c 1e010252 01fec08d  |  ce8e8f2c 1e010262 01fec08d  |  ce8e8f3c 1e010272 01fec08d  |  ce8e8f4c 1e010242 01fec08d
ce8e8f5c 1e010212 01fec08d  |  ce8e8f6c 1e010222 01fec08d  |  ce8e8f7c 1e010232 01fec08d  |  ce8e8f8c 1e010202 01fec08d
ce8e911c 1e010452 01fec08d  |  ce8e912c 1e010462 01fec08d  |  ce8e913c 1e010472 01fec08d  |  ce8e914c 1e010442 01fec08d
ce8e915c 1e010412 01fec08d  |  ce8e916c 1e010422 01fec08d  |  ce8e917c 1e010432 01fec08d  |  ce8e918c 1e010402 01fec08d
ce8e931c 1e010652 01fec08d  |  ce8e932c 1e010662 01fec08d  |  ce8e933c 1e010672 01fec08d  |  ce8e934c 1e010642 01fec08d
ce8e935c 1e010612 01fec08d  |  ce8e936c 1e010622 01fec08d  |  ce8e937c 1e010632 01fec08d  |  ce8e938c 1e010602 01fec08d
ce8e9528 1e010860 01fec09d  |  ce8e9538 1e010860 01fec09d  |  ce8e9548 1e010840 01fec09d  |  ce8e9558 1e010800 01fec0dd
ce8e9568 1e010820 01fec09d  |  ce8e9578 1e010820 01fec09d  |  ce8e9588 1e010800 01fec09d  |  d28e8d1c 1a010052 01fec08d
d28e8d2c 1a010062 01fec08d  |  d28e8d3c 1a010072 01fec08d  |  d28e8d4c 1a010042 01fec08d  |  d28e8d5c 1a010012 01fec08d
d28e8d6c 1a010022 01fec08d  |  d28e8d7c 1a010032 01fec08d  |  d28e8d8c 1a010002 01fec08d  |  d28e8f1c 1a010252 01fec08d
d28e8f2c 1a010262 01fec08d  |  d28e8f3c 1a010272 01fec08d  |  d28e8f4c 1a010242 01fec08d  |  d28e8f5c 1a010212 01fec08d
d28e8f6c 1a010222 01fec08d  |  d28e8f7c 1a010232 01fec08d  |  d28e8f8c 1a010202 01fec08d  |  d28e911c 1a010452 01fec08d
d28e912c 1a010462 01fec08d  |  d28e913c 1a010472 01fec08d  |  d28e914c 1a010442 01fec08d  |  d28e915c 1a010412 01fec08d
d28e916c 1a010422 01fec08d  |  d28e917c 1a010432 01fec08d  |  d28e918c 1a010402 01fec08d  |  d28e931c 1a010652 01fec08d
d28e932c 1a010662 01fec08d  |  d28e933c 1a010672 01fec08d  |  d28e934c 1a010642 01fec08d  |  d28e935c 1a010612 01fec08d
d28e936c 1a010622 01fec08d  |  d28e937c 1a010632 01fec08d  |  d28e938c 1a010602 01fec08d  |  d28e9528 1a010860 01fec09d
d28e9538 1a010860 01fec09d  |  d28e9548 1a010840 01fec09d  |  d28e9558 1a010800 01fec0dd  |  d28e9568 1a010820 01fec09d
d28e9578 1a010820 01fec09d  |  d28e9588 1a010800 01fec09d
```

Per first block: E[number of passing classes] = 222 p7 = 3.52295 and the expected number of good pairs (variants
passing both filters) is g = 782,800 p7 p6 = 830.988 (Lemma 5.1, linearity). Passing classes are strongly correlated
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
members depend only on S and l, not on CV1 or the variant (rows 12, 13 are S; rows 14, 15 use rows 10..13 and
W14, W15).

### 6.2 Row 16 as a table, rows 17..36

For l in L*, E16x = C16_l + u with u = W0 + s0(W1) (W16 = s1(W14) + W9 + s0(W1) + W0; C16_l collects rows 12..15,
K16, s1(W14), W9), and every cell of row 16 of both members (E16y = E16x + const_l, A16 from E16 and rows 13..15) and
every two-bit condition closing at row 16 is a function of E16x only. Exhaustive enumeration (all E16x with the
row's ten fixed bits, 2^22 per l) gives the passing sets; per l (0..31): 0, 16384, 0, 16384, 32768, 8192, 32768,
4096, 65536, 49152, 65536, 49152, 32768, 57344, 32768, 59392, 0, 16384, 0, 16384, 32768, 16384, 24576, 12288,
65536, 49152, 65536, 49152, 32768, 49152, 45056, 55296; total 1,052,672 (= 6c77089c's counts). The table
R16[u] = {l : C16_l + u passes row 16} (2^32 entries of 32 bits) is built once (Section 11). By Lemma 5.1 u is
uniform for a good pair, so Pr[row 16 for l] = |R16_l|/2^32 exactly.

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

### 7.3 The estimator (`smc.c`, Appendix A)

Stages: row 16 exact (the enumeration of 6.2: the stage mean is (1/32) sum_l |R16_l| / 2^32 = 2^-16.994, and the
initial particles are drawn exactly from the passing (l, E16) pairs); rows 17..21: each child proposes E_t^x
uniformly with the row's fixed x-bits imposed (exact importance weight 2^-f), sets W_t^x = E_t^x - (the rest of step
t), W_t^y = W_t^x + its exact difference, and checks the whole row; row 22: (W6, W7) drawn uniformly from F6 x F7;
rows 23..36: W8 of a variant drawn uniformly from the 782,800 selected variants (the same row-22 survivor is also
evaluated with the published W8 for a paired comparison). NP particles, M children per particle per stage, MT tail
proposals per particle, multinomial resampling of the survivors after every stage; the product of the stage means
is an unbiased estimator of q3 (standard SMC normalising-constant estimator: given the particles before a stage, the
stage mean is unbiased for the particle average of that stage's conditional probability; multinomial resampling
keeps particle averages unbiased; the expectation of the product telescopes).

### 7.4 Preregistration and results

Frozen at 2026-10-09T17:45:34Z before any listed seed ran (`PREREG_q3b.txt`, SHA-256 3323fb58...; program `smc.c`
SHA-256 7ac6f21b..., `lab.h` 5e0e9605...): the program and the parameters of 087a18c4's study (NP = 2048, M = 512,
MT = 16384) with W8 drawn from the 782,800 variants of the 222 classes; replicate seeds 80000..80007, 81000..81007,
82000..82007, 83000..83007 (32 replicates); rule: one-sided 99% Student lower bound of the mean of the 32 linear
estimates (t = 2.4528, 31 df), q3_model = the bound at its printed face value, rounded down at the fourth decimal of
its logarithm (H6). All 32 replicates are reported. The earlier study of 087a18c4 (the same program with the 64
classes of 3600 variants, seeds 70000..73007: mean 2^-73.9908, relative sd 0.0419, bound 2^-74.0173; records A.5 - A.9) is
kept as a second, independent sample of the subfamily of the first 64 classes; it is not used for the claim.

| quantity | value |
|---|---|
| per-replicate log2 estimates (variant W8, seeds in order) | -74.0368 -73.9495 -74.0753 -73.9413 -74.0428 -73.9847 -73.9531 -73.9174 -74.1078 -74.0418 -73.9698 -74.0807 -74.0101 -74.0770 -74.0335 -73.9578 -74.1239 -73.9548 -74.0073 -73.9825 -74.1068 -73.8967 -73.9442 -73.9068 -73.9921 -74.0057 -73.9549 -73.9583 -74.0621 -73.9356 -73.9446 -74.0219 |
| mean | 2^-73.9980 |
| relative standard deviation | 0.0430 |
| 99% lower bound | 2^-74.0251 |
| **q3_model (H6, this filing)** | **2^-74.0252 (the bound, rounded down at the fourth decimal of its logarithm)** |
| stage means (log2) | 16: -16.994, 17: -12.999, 18: -15.005, 19: -6.000, 20: -7.000, 21: -1.000, 22: -10.999, 23..36: -4.002 |
| rows 23..36, paired, over 524,640 row-22 survivors | variant W8: 32,757 passes (2^-4.001); published W8: 32,878 (2^-3.996) |
| same replicates with the published W8 | mean 2^-73.9930 |

### 7.5 Consistency

- The stage factors equal, within 0.01 bit, the per-row condition counts of the printed tables (17, 13, 15, 6, 7,
  1, 11, 4; 74 in total) and 6c77089c's published-S stage factors (16.994, 13.000, 14.996, 6.000, 7.000, 1.000,
  15.002 for rows 22..36 together); their preregistered published-S estimate is q3 = 2^-74.01 (mean 2^-73.9916).
- Lemma 7.1 makes rows 16..22 identical by construction; the paired rows-23..36 rates differ by 0.005 bit
  (121 passes out of 32,800; the paired difference has a standard deviation of about 242 passes, z = -0.5).
- Real first blocks (Section 13.1): the row-16 rate of the attack's own good pairs is the exact 2^-12.0 (z = +0.51
  over 503,050 passes).
- An earlier development run (8 replicates, NP = 1024, M = 256, MT = 4096, W8 from all of G) gave 2^-73.95 for both
  W8 choices; it is not part of the sample.

## 8. The algorithm (fixed caps)

```text
input: N_FB, V_MAX; precomputed: S, L*, the 222 classes and their variant data (Section 9.3), the class planes C7_j of the
       W7 program, the bitmaps of F6 and F7 (2^32 bits each), the table R16 (2^32 words of 32 bits) and its presence
       table (2^24 words of 256 bits: bit i of word b is set iff R16[256 b + i] is not 0), the 2^24-entry lane-scan table
V = 0
for f = 1 .. N_FB:
    draw two uniform 256-bit words; M0 := their sixteen 32-bit fields; CV1 := F_37(IV, M0)          [1 unit]
    hits := the classes c with c7_c - A_{-1} in F7: the pass plane of the bit-sliced W7 program (lane = class), scanned
    if hits:
        V += 1; compute the 64 broadcast planes of A_{-1} and C6 - A_{-2}
        for c in hits:
            V += 1
            for each group of up to four batches of 256 variants of c: run the group's bit-sliced W6 program -> fail planes
                for each batch of the group and each lane L with W6 in F6 (lane scan): append the variant a0 to the pending
                    group; when it has four variants (and at the end of the class, with the variants it has):
                        V += 1; (first time in this first block: per-first-block constants, V += 1)
                        u := W0 + s0(W1) of the variants of the group, in the four lanes of one word
                        for each variant: presence word of u's block of 256 values of u; if it is not 0 and bit u mod 256 is set:
                            mask := R16[u]; V += 1; recompute W6, W7; for l in mask: rows 16..36 with early abort
                                if all rows pass: build m, m'; if digest(m) = digest(m') and m != m': output, halt
            if V > V_MAX: halt (failure)
halt (failure)
```

V counts every data-dependent operation in units of operations: the program adds each counted routine's cost (the
increments are shown once per routine above and are themselves counted). The run executes at most N_FB
compressions, N_FB x 421 fixed operations, V_MAX + one class's maximum work of data-dependent operations, the
precomputation and one final verification, whatever the coins.

## 9. The counted program

### 9.1 Machine and pricing

256-bit word RAM, 64 registers, every executed primitive counted (loads and stores included). 32-bit values are
kept in the low bits; a reduction mod 2^32 is one AND; a 32-bit rotation pattern (S0, S1, s0, s1) costs 8:
d = x | (x << 32) (2), three shifts and two XORs (or two shifts, one XOR and the s-function's plain shift) and one
mask. A bitmap lookup (2^32 bits in 256-bit words) costs 6: shr 8, add base, load, and 255, shr, and 1. A table
lookup is an add of the base and a load. **Packed groups.** A word holds four 64-bit lanes, each lane a 32-bit value in
its low half (the upper half zero). Additions, subtractions and AND/OR/XOR act on the whole word and are lane-wise
as long as no lane carries or borrows out of its 64 bits; every lane value below stays below 2^36, and every
subtraction is a positive constant (kap1 + 2^35) minus a smaller sum, so neighbouring lanes never interact. A
rotation pattern costs the same 8 operations for the four lanes at once: d = x | (x << 32) stays inside each lane,
the shifted copies bring bits of the neighbouring lane only above bit 31, and the final mask removes them (an s-function
needs one more mask for its plain shift: 9). The target compression of a first block is one unit and its internal
operations are not counted again. All counts below are produced by running the routines of `experiments/a0core.py`
(`calibrate`, deterministic and asserted constant over 20 random inputs); `python3 a0core.py ledger` prints them.

### 9.2 Fixed per first block: 421 operations

- First block words: 2 random words, then the 16 fields (field 0 of a word: and; fields 1..6: shr, and; field 7:
  shr): 30.
- W7 tests of all 222 classes by one bit-sliced program (lane = class; `gen_w7`): the 32 broadcast planes
  NA_j = (bit j of A_{-1}) - 1, each formed in registers by shr, and, sub and not stored (96); the ripple adder
  W7x = c7 + ~A_{-1} + 1 over the 32 stored class planes C7_j (32 loads; per bit two XORs and a carry of three
  operations) and the exact F7 test of Section 5.1 (the triples t1 = w1^w18^w22, t2 = w9^w26^w30, t3 = w0^w11^w28 and the checks of the
  two affine spaces): 257 instructions of which the 32 NA are not loads, so 225 are counted, with at most 22 live
  values; the AND with the mask of the 222 lanes (1); the lane scan of the pass plane (53 as in 9.3, every
  chunk charged as nonzero; its 4 per passing class are counted with the class). 96 + 225 + 1 + 53 = 375. The pass plane
  equals the scalar test of every class on every first block of the calibration and of the organizer experiment.
- Control allowance: 16 per first block (the loop counter's add and compare-branch, the hit-list initialisation,
  the `if hits` branch, and 12 for any further loop or address arithmetic not itemised elsewhere), and 8 per
  passing class (iterating: load, add, branch; plus 5). The counted program adds both.

### 9.3 The bit-sliced W6 programs and the lane scan (per passing class)

Per first block with a passing class: cb = (C6 - A_{-2}) mod 2^32 (2) and 64 broadcast planes AB_j = 0 - ((A_{-1} >> j)
& 1) and CB_j = 0 - ((cb >> j) & 1), each stored (4): 258.

The variants of a class are stored in batches of 256 lanes (3600 = 14 batches and one with 16 used lanes; 3584 = 14
batches; 3456 = 13 batches and one with 128 used lanes; 3,193 batches in all). For each batch the stored planes are A0_j, K3_j (bit j of
K3C - MAJ(A2, A1, a0)) and NE4_j (bit j of ~E4) for the bit positions j where the value is not constant over the
batch (the constant bits of a batch are folded into its part of the program). One straight-line program per group of up to four
batches (GB = 4) of a class computes, bit-serially from j = 0 to 31, and for each batch of the group in turn within a bit:

```text
MAJ_j = A1_j ? (A0_j | AB_j) : (A0_j & AB_j)                                    (A1 is a global constant)
E3: ripple adder K3 + AB (carry needed up to bit 28)
Y_j = E5_j ? NE4_j : ~E3_j                                                        (= ~CH(E5, E4, E3), E5 constant)
carry-save add of (MAJ, Y, CB) then ripple add with carry-in 1:  W6 = cb + MAJ - CH  (mod 2^32)
fail = common | (W6_29 & B_bad & C_bad)                                         (the exact F6 test of 5.1)
```

where common = (w14^w18) | ~(w8^w25) | (w1^w12), bc = (w15^w19) | ~(w9^w26) | (w2^w13), B_bad = bc | w30, C_bad =
bc | ~w30 | (w16^w20^w31) | ~(w10^w27^w31) | (w3^w14^w31); each pair or triple is folded into an accumulator as soon as its
last bit exists (so that the sum bits are not kept), `fail` is formed at bit 31. A lane passes (W6x in F6) iff its fail bit is
0. The AB_j and CB_j loads (64) are shared by the batches of a group. Per class the programs have between 6,217 and 7,240
operations in all (mean 6,602.3 over the 222 classes, i.e. 459 per batch; at most 772 loads, every load counted); at most 57 values
are live in any group program (`peak_live`, computed from the instruction order), and the loads address the stored planes of
the group's batches and the broadcast planes through at most 5 base registers: 62 <= 64, no spills. Then pass = ~fail &
lanemask (2 per batch).

Lane scan per batch: 11 chunks of 24 bits (ten of 24 and one of 16): extraction (1 for the first chunk and for the last,
2 for the others): 20; a zero branch each: 11; for each nonzero chunk the add of the table base and the load of the chunk's entry in the
2^24-entry scan table (the entry lists the chunk's set positions as 6-bit fields position + 32, lowest first): 2, charged for
all chunks (22): 53 per batch. Per set lane: and 31 (the position), add the chunk's base (the lane's index in the class), shr 6, and
the loop branch: 4.

Class total: programs + 2 per batch + 53 per batch + 4 per passing lane + 3 (V update, compare, branch) + 8 (control).
**Correctness.** The program's fail planes equal the scalar definition (inF of W6x computed by Lemma 4.1) on every
lane of every batch processed by the organizer experiment `a0-online-r37` and by the counted program in the checks of
Section 13.1 (1,060,960 lanes in the stress run).

### 9.4 Good pairs: groups of four

Per first block, at its first group (66): MAJ(A_{-1}, A_{-2}, A_{-3}) (4), S0(A_{-1}) (8), e0b = A_{-4} - S0 - MAJ (3),
CH(E_{-1}, E_{-2}, E_{-3}) (3), S1(E_{-1}) (8), kap0 = e0b - A_{-4} - E_{-4} - S1 - CH - K0 (5) reduced (1),
A_{-1}|A_{-2}, A_{-1}&A_{-2}, E_{-1}^E_{-2} (3), kap1 = (A1 - K1) - E_{-3} + 2^35 (2); each of the seven constants (e0b, kap0,
o12 = A_{-1}|A_{-2}, n12 = A_{-1}&A_{-2}, X = E_{-1}^E_{-2}, E_{-2}, kap1) is broadcast to the four lanes (x | x << 64, then
| << 128: 4 each, 28), and the lane mask is loaded (1).

Per good pair: its lane scan (4, 9.3), the index add (1), the load of the variant's table entry (1; table k holds a0 | S0(a0) << 32
placed in lane k, k the pair's position in the group, so that no shift is needed) and the OR into the group word (1; none for lane 0).

Per group (34 operations and one V update): a = acc & pm; sa = (acc >> 32) & pm; E0 = (a + e0b) & pm; W0 = a + kap0;
mj = (a & o12) | n12; ch = (E0 & X) ^ E_{-2}; S1(E0) (8); T = sa + mj + S1 + ch (3); W1 = (kap1 - T) & pm (2); s0(W1) (9);
u = (W0 + s0(W1)) & pm (2): 1 + 2 + 2 + 1 + 2 + 2 + 8 + 3 + 2 + 9 + 2 = 34 (the seven constants and the mask pm are
register values; at most 15 values are live). The group is processed when it has four pairs and at the end of the class.
A group with fewer than four pairs costs the same (the empty lanes hold zero), which the ledger charges as
ceil(n / 4) <= (n + 3) / 4 groups for a class with n good pairs.

Per pair after the group: the block lookup: shr (64 k + 8), and 2^24 - 1, add base, load the presence word of the pair's
block of 256 values of u, branch if it is not 0: 5; the bit test when it is not 0 (at most 2^8 sum_l |R16_l| / 2^32 = 6.274% of the pairs,
since u is uniform): extract the low byte of u (shr, and; one operation for lane 0), shr of the presence word by it, and 1, branch: 5.
So a pair costs at most 4 + 1 + 1 + 1 + 5 + 5 x 0.06274 = 12.3137 operations on average plus 34 / 4 for its share of the group.

### 9.5 Rows >= 16 (rare)

Per good pair with a non-empty row-16 mask (probability 2^-12.0 per good pair): the mask word of R16 (7: u >> 3, add base,
load, and 7, shl 5, shr, and), a0 extracted from the packed word (2), V update (1), W6 and W7
recomputed (23, counted: MAJ(A1, a0, A_{-1}) 4, E4 2, MAJ(A2, A1, a0) 4, E3 3, CH 3, W6 4, W7 3), E0..E5 and W0..W5
by Lemma 4.1 and W8 (201). Per l in the mask: extract/branch (2), the three y-words with a difference (add, and
each: 6), and per row (both members): W_t (s1, s0, 3 adds, and: 20), CH (3), E_t (S1, 5 adds, and: 14), MAJ (4),
A_t (S0, sub, add, add, and: 12) = 53 per member, 106 per row; the row check (cells of A, E, W of both members:
and, xor, xor, xor, or per word = 15; the `+` pair: 3; at most seven two-bit conditions at 5 each) is charged 53 per
row, plus its branch. Rows 16 and 17 are always executed; row t >= 18 is executed only if row 17 passed, which
requires the nine fixed x-bits of E17 (probability exactly 2^-9, since W17 = s1(W15) + W10 + s0(W2) + W1 is uniform
and independent of rows <= 16 by Lemma 5.1). The full path for one l (all 21 rows) costs 201 + 8 + 21 x 160 = 3569
(asserted on the published pair by `calibrate`).

## 10. Success probability, independence and caps

Let a *trial* t = (f, a0, l) be a first block f, a selected variant a0 and l in L*, and A_t the event that a0 is
good for f and the pair follows every cell and printed two-bit condition of rows 16..36. The program examines every
good pair of every processed first block and every l whose row 16 holds, so it finds a success iff some A_t occurs
before the caps (and every output is verified, Lemma 6.1). Let X_f = sum over the trials of f of 1[A_t] and
X = sum_f X_f.

- **Expectation.** E[X_f] = g x 32 x q3 (Lemma 5.1 and Section 7) and E[X] = N_FB g 32 q3. With q3 >= q3_model
  (H2, H6): E[X] >= N_FB g 32 2^-74.0252 >= mu0 = 0.49466302 (H7) for N_FB = ceil(mu0 / (g 32 2^-74.0252)) =
  357,577,563,488,735,156 = 2^58.31103; mu0 is the smallest 8-decimal number strictly above
  -ln(0.61 - 2^-21.4 - 2^-60) / (1 - 2^-10.4) = 0.4946630123..., the value that makes the bound of the last item exceed 0.39.
- **One first block (H3).** By Bonferroni, Pr[X_f >= 1] >= E[X_f] - sum over pairs t < t' of f of Pr[A_t and A_t']
  = E[X_f] - (1/2) sum_t Pr[A_t] E[X_f - 1 | A_t]. H3: E[X_f - 1 | A_t] <= delta = 2^-9.4 for every trial t,
  so Pr[X_f >= 1] >= (1 - 2^-10.4) E[X_f]. (Only the expected number of *further* successes of the same
  first block given one success is needed; bursty goodness and shared W7/W6 values enter only through
  that conditional expectation, and do not affect E[X], which is linear.)
- **Many first blocks (H1).** Distinct first blocks have independent chaining values, so the events X_f >= 1 are
  independent and Pr[X >= 1] >= 1 - exp(-sum_f Pr[X_f >= 1]) >= 1 - exp(-(1 - 2^-10.4) mu0)
  = 0.3900003660.
- **Work cap.** The data-dependent work v_f of a first block (everything except its compression and its 421 fixed
  operations) has mean at most vbar = 44,137.2565 (the sum of Section 11's terms, which charges the per-hit setup
  once per first block with a passing class and the row-16 work per (pair, l)) and is at most
  84,572,030,090 < 2^36.30 (every class passing, every variant good, every l past row 16 to row 36, plus the
  per-class and per-first-block control). The v_f are independent (H1), so by Chebyshev
  Pr[sum v_f > (1+2^-8) N_FB vbar] <= E[v_f^2]/(2^-16 N_FB vbar^2) <= 2^36.30/(2^-16 N_FB vbar)
  < 2^-21.4. V_MAX = ceil((1 + 2^-8) N_FB vbar) = 15,844,143,000,526,062,945,838 is reached with
  probability below 2^-21.4; the run then fails, which is accounted for here.
- **Success.** Pr[output a collision] >= 0.3900003660 - 2^-21.4 - 2^-60 = 0.3900000047 > 0.39 (the 2^-60 covers a
  repeated first block among N_FB draws of 512 bits). With q3 = the SMC mean instead of its lower bound the
  bound is 0.3908. Any output is a verified collision, independent of the premises.

## 11. Ledger (exact; `python3 experiments/a0core.py ledger`)

```text
T = A_C + A_S + DEV + N_FB + (N_FB x 421 + V_MAX + vmax_class + PRE + FIN) / C + 6
  A_C = 2^60   characteristic search and SFS-pair search of the paper (allowance, H4)
  A_S = 2^50   Step-1 SAT solve (paper: 2^41.3)
  DEV = 2^40   all development computation (Section 13.4)
  N_FB = 357,577,563,488,735,156 compressions (2^58.31103; H7 mu0 = 0.49466302, H6 q3 = 2^-74.0252)
  421          fixed operations per first block (9.2: 30 + 375 + 16 control)
  V_MAX = 15,844,143,000,526,062,945,838 = ceil((1 + 2^-8) N_FB vbar), vbar = 44,137.2565 ops, of which
               per first block with a passing class (probability at most 1): setup 1 + 258 + 66 + 1 = 326
               per passing class (222 p7 = 3.52295 per first block): control 8 + 4 + 1 + 2 -> 52.84;
                 W6 programs and 2 operations per batch: p7 x sum over the 222 classes of (programs + 2 nb) -> 23,361.04;
                 lane-scan fixed part: p7 x 53 x (3,193 batches) -> 2,685.52;
                 groups of four: p7 x sum over the classes of 35 (n p6 + 3) / 4 -> 7,363.62
               good pairs: g x 12.3137 -> 10,232.56
               rows >= 16: g x 2^-12.0 x (234 + 328 + (19/512) 160) -> 115.67
  vmax_class = 388,936,768 (one class's maximum work: overshoot past the last cap test)
  PRE = 2^40 operations (bound on all precomputation, Section 11.1); FIN = 1600 operations (the final verification and
  the next first block's setup after the last cap test) and 6 compressions
T x 1322 = 9,995,711,239,180,937,961,565 (the fraction T x 2644 / 2, reduced)     ->   T = 2^62.713293  ->  time_log2 = 62.7133
preprocessing = A_C + A_S + DEV + PRE/C = 2^60.00141
```

The online terms are 2^58.3110 (compressions), 2^55.6602 (fixed ops) and 2^62.3779 (V_MAX); A_C adds
2^60. Every count in this block is produced by `calibrate()` and `ledger()` of `experiments/a0core.py`.

### 11.1 Precomputation (bounded by 2^40 operations)

Enumerating G and c7 over all 2^32 words (about 40 operations each, 2^37.4); grouping the 12.1 million variants
by c7 and selecting the 222 classes (below 2^30); the bitmaps of F6 and F7 (each word: two s0 evaluations, an add,
a sub, a compare and an or into the bitmap word, about 22 operations, 2^37.5 for both, plus 2^28 stores); R16 (2^29
zeroing stores and 32 x 2^22 row-16 evaluations at about 150 operations, 2^34.3) and its presence table (one pass over R16:
2^32 words tested and 2^24 words written, below 2^34); the 2^24-entry lane-scan table (at most 80 operations per entry, below 2^31); the
four copies of the variant table (782,800 entries each, below 2^26); the class planes of the W7 program, the 3,193 batches of stored planes
and the 222 class programs (below 2^28). Total below 2^38.7 operations.

### 11.2 Sensitivity (log2 T, one input changed)

| change | log2 T |
|---|---|
| as claimed | 62.7133 |
| q3 lower by 0.25 bit | 62.92783 |
| q3 lower by 0.5 bit | 63.14732 |
| q3 lower by 1 bit | 63.59877 |
| q3 = 2^-75 (the paper's count of 75 conditions) | 63.57567 |
| q3 = the SMC mean 2^-73.9980 instead of its lower bound | 62.69028 |
| A_C = 2^64 | 64.43017 |
| A_C = 2^56 | 62.49075 |
| scalar W6 test (no bit-slicing anywhere; 18 operations per variant) | 64.91364 |
| four scalar computations of u (30 operations each) instead of the four-lane group | 63.11917 |
| 087a18c4's pads restored (q3 = 2^-74.03 as the 2-decimal floor, mu0 = 0.501953125) | 62.73528 |

### 11.3 The advice-construction allowances A_S and A_C (H4)

The cost model charges all construction of the advice, including searches omitted from the program. The advice is
(i) the 37-step characteristic and its two-bit conditions (Tables 15, 16), (ii) the Step-1 solution S, and (iii) the
semi-free-start pair (Table 17) from which S is read. Everything derived from them (G, the classes, F6, F7, L*, R16)
is recomputed inside the precomputation (Section 11.1).

- **(ii) and (iii): Step 1 and the SFS pair, charged A_S = 2^50.** The paper reports its Step-1 SAT solve at 2^41.3
  compression-equivalents; A_S is 2^8.7 times that. Completing a Step-1 solution to a 37-step semi-free-start pair is
  cheap and is reproduced in this package: given the characteristic and a dense part (S or any of its A0-variants),
  `sfs.c` and the organizer experiment `a0-sfs-r37` build complete 37-step semi-free-start collisions in about one
  second each (rows 16..21 by sampling, rows 22..36 by about 2^9 tail proposals; Section 13.2). The 18 + 16 verified
  pairs of Section 13 are such constructions. So the SFS-pair search beyond Step 1 costs below 2^30 units, far inside
  A_S.
- **(i): the characteristic search, charged A_C = 2^60.** Its running time is not published. We bound it by the only
  measured comparison point accepted on this challenge. The promoted filing 6eeefb64 (sha256-r32-exploratory, accepted
  by the organizers) charged a measured, complete re-run of the four-step characteristic search of [LLWS26] for its
  35-step characteristic (its Fig. 6), with the authors' open-source model library of [LLW24] and STP 2.3.4 with
  CryptoMiniSat 5.11.21: 593,858 solver CPU-seconds over 59 calls, output equal to the published characteristic (it
  charged 32 times that for a blind rediscovery). It calibrated the price of one solver CPU-second at
  2^32.796 primitive operations (callgrind instruction counts, with a 1.85 rate spread allowed). At this track's
  C = 2644 that is 2^21.427 units per CPU-second, so A_C = 2^60 units buys 2^38.573 = 4.1 x 10^11 solver
  CPU-seconds, about 13,000 CPU-years:
  - 688,000 times (2^19.39) that measured complete re-run;
  - 2^14.39 times the 32-fold rediscovery allowance charged in the accepted filing;
  - 200 times (2^2.7) a 1000-core cluster running without pause for two years (2^35.9 CPU-seconds).
  The 37-step characteristic of [LZLLQZ26] comes from the same group's improved search, building on that framework
  and tool, and its cost is unpublished. The premise is that it did not exceed this budget, which is 2^19 times the
  accepted measurement of the predecessor search.
- Sensitivity: A_C = 2^64 (another 16x) gives 64.43017; A_C = 2^56 gives 62.49075. No other term depends on it.

## 12. Premises

**H1 - uniform independent chaining values (score-critical).** The first blocks are fresh uniform 512-bit strings;
their chaining values CV1 = F_37(IV, M0) behave as independent uniform 256-bit values. Used for: Lemma 5.1 (exact
filter rates and the law of the second-block words, per variant), the expected counts, the independence across
first blocks (Section 10) and Chebyshev. Evidence: 2^17.6 and 2^23 real first blocks through the attack's own filters
(Section 13.1: passing classes, good pairs and row-16 passes at the predicted rates, within 0.4%); the organizer experiment
`a0-online-r37`. Limitations: a premise; tested on 2^23 first blocks, not 2^58.3; the counts of passing classes and of good pairs are
overdispersed (classes with close c7 pass together) and 0.24% and 0.38% above their expectations at 2^23 (about +2.4 and +2.1 standard
deviations of the per-first-block variance), in the direction that lowers the cost.

**H2 - Step-3 probability of the variants (score-critical).** q3 >= q3_model = 2^-74.0252 (H6 level; Section 7.1's average over
the 782,800 selected variants and L*), and q3 <= 2^-70. Evidence: Lemma 7.1 (rows 16..22 identical for all variants;
the variant enters only through W8 in W23, W24), the preregistered SMC (Section 7.4), the paired comparison of
rows 23..36, the agreement with 6c77089c's published-S estimate row by row, the row-16 rate of real good pairs, and
37-step semi-free-start collisions built with variant dense parts (Section 13.2, organizer experiment
`a0-sfs-r37`). The 32 replicate estimates are nearly symmetric (skewness -0.29, relative sd 0.043, all 32 at least 2^-74.124); a
percentile bootstrap of their mean (200,000 resamples) puts its 1% quantile at 2^-74.0236, above the Student
bound 2^-74.0251. The study of 087a18c4 on the first 64 classes (mean 2^-73.9908, bound 2^-74.0173) is consistent with it. Limitations: a Monte-Carlo bound whose coverage rests on the approximate normality of the mean of 32
replicates (each replicate is a product of eight stage means over at least 2^20 children); the `+` reading.

**H3 - few further successes per first block (score-critical).** For every trial t, the expected number of other
successful trials of the same first block given A_t is at most delta = 2^-9.4, i.e. E[X_f - 1 | A_t] <= 2^-9.4.
It splits into (a) the same variant with another l in L*, and (b) other good pairs (other variants) of the same
first block. For (a) the premise is E[#other l succeeding | A_t] <= 2^-11; measured directly on 33,150 Step-3
successes of the SMC with the 222-class W8 (`replay`, Section 13.1): rebuilding W0..W5 and testing the other 31
elements of L* through rows 16..36 gave 0 further successes (every success re-checked with its own l passes); the
95% upper bound of the per-success rate is 2^-13.4 (3 / 33,150; the samples share SMC ancestors, so they are not independent).
For (b) the expectation is at most rho x (782,800 x 32 x q3) <= rho x 2^-45.42 with q3 <= 2^-70 (H2), where rho bounds
Pr[t' succeeds | t succeeds, t' good] / Pr[t' succeeds | t' good] for good pairs t' != t of the first block; the
premise is rho <= 2^35, and the measured factor at the row-16 level over 2^23 real first blocks is 0.999 (sum of
R(R-1) = 9,807,146 against p^2 sum of G(G-1) = 9,817,977.6, R row-16 passes and G good pairs per first block; 1.003 over 2^17.6 first
blocks). So delta <= 2^-11 + 2^-10.42 < 2^-9.4 (the premise rho <= 2^37 of 087a18c4 became rho <= 2^35 because the number of
variants is 3.4 times larger). Bursty goodness (variants of one class share W7; a class's 3600 variants give
only 32..512 distinct W6 values for a given chaining value) does not enter: the bound conditions on t' being good.
Limitations: rows >= 17 of distinct good pairs cannot be measured jointly within one first block; the premise
leaves a margin of 2^35 over the measured row-16 factor.

**H4 - advice allowances (supporting).** The published characteristic and two-bit conditions, the SFS pair's inner
values S and L* are advice. Their construction is charged A_S = 2^50 (Step 1 and the completion to an SFS pair) and
A_C = 2^60 (the characteristic search). Evidence (Section 11.3):
- **A_S.** It is 2^8.7 times the paper's reported Step-1 cost. The completion of a Step-1 solution to a 37-step SFS
  pair is reproduced here in about one second per pair (34 verified constructions, including organizer-seeded ones).
- **A_C.** It buys about 13,000 CPU-years at the CPU-second price calibrated in the accepted filing 6eeefb64
  (2^32.796 operations per CPU-second, i.e. 2^21.427 units at C = 2644). That is 688,000 times the 593,858 CPU-seconds
  that filing measured for a complete re-run of the predecessor 35-step characteristic search ([LLWS26], with the
  [LLW24] tool).

The variant family, the classes, the filter sets, L* and R16 are recomputed in the precomputation (Section 11.1).
Limitations: the 37-step search time is unpublished; A_C is a bound by comparison, not a measurement. A_C = 2^64 would
give 64.43017.

**H5 - counted word-RAM pricing of the bit-sliced programs and of the four-lane groups (score-critical; cost reading).**
(a) A straight-line program of 256-bit primitives that evaluates a filter for 256 lanes at once (bit L of each word belongs to
lane L: the 222 classes for the W7 test, 256 variants for the W6 test) is charged its counted primitives (257 instructions
for W7, 459 per batch on average for W6, every load counted, at most 57 live values on 64 registers). (b) A routine on
256-bit words that treats a word as four independent 64-bit lanes (additions, subtractions and logic without a carry between the
lanes, a rotation pattern as one OR, three shifts, two XORs and a mask) is charged its counted primitives: 34 for the u of four
variants (15 live values). Neither evaluates a target compression; every compression is charged one unit. Evidence: the programs are
in `experiments/a0core.py` (`gen_w7`, `gen_w6`, `good_group`, `cv_pre`), bit-exact against the scalar definitions (Sections 9.2 - 9.4;
`calibrate` compares the group with the scalar u on random groups of four and of three, the experiment `a0-online-r37` and the
stress run of Section 13.1 on every good pair). Limitation: no organizer ruling is cited; bit-sliced programs counted in this way
and the 7 x 36-bit packing of earlier filings passed the AI screening on this track (fca38c6d, 817d444c, 64bca7e2, 6de1b685, 6c77089c);
with a scalar W6 test (18 operations per variant) the claim is 64.91364 and with four scalar computations of u instead of the
group it is 63.11917.

Not used: expected work, an independence-of-conditions model for q3 (replaced by the SMC), a random-oracle model,
any premise on the published pair beyond its verified values.

## 13. Evidence and runs

All runs on one Apple-silicon Mac (14 cores), our own code (C and Python standard library). We ran 087a18c4's `a0core.py ledger`
to reproduce its ledger; we executed no other code of another filing.

### 13.1 End to end on real first blocks (`e2e.c`, Appendix A)

Random M0 (xoshiro-style generator seeded per thread), CV1 = F_37(IV, M0) by our compression (equal to the
repository verifier on the checked pairs), the W7 tests of the 222 classes, the scalar W6 test of every variant of every passing
class, u and the exact row-16 test for every l, exact checks of sampled pairs (Lemma 4.1 words, W6/W7 filters,
every cell of rows -4..16 and the two-bit conditions closing at rows 15, 16).

| run | first blocks | passing classes (expected) | good pairs (expected) | row-16 passes (expected) | exact checks |
|---|---|---|---|---|---|
| seed 21 (222 classes) | 2^17.58 | 696,209 (692,640) | 163,607,020 (163,378,921.9; 1.0014) | 40,079 (40,099.1; z -0.10) | 24,000, 0 failures |
| seed 22 (222 classes) | 2^23 | 29,623,852 (29,552,640) | 6,997,476,590 (6,970,834,000; 1.0038) | 1,712,536 (1,715,041.6; z -1.91) | 32,000, 0 failures |
| seed 1 (64 classes, 087a18c4) | 2^21 | 2,134,874 (2,129,920) | 516,134,885 (512,928,000; 1.0063) | 126,066 (126,501.7; z -1.23) | 16,000, 0 failures |
| seed 3 (64 classes, 087a18c4) | 2^23 | 8,510,833 (8,519,680) | 2,051,007,293 (2,051,712,000; 0.9997) | 503,050 (502,690.2; z +0.51) | 16,000, 0 failures |

The passing-class counts are overdispersed relative to a Poisson model (classes are correlated: for uniform words A_{-1} the number of
passing classes has variance 28.8 x its mean 3.524, measured on 2 x 10^7 words, `w7var.c`), so the z of the counts is divided by 5.4 and the ratios 1.0014 .. 1.0052 are
+2.4 standard deviations at most. Within-first-block row-16 correlation (seed 22): factor 0.999 (H3); (seed 21): 1.003.
Same-pair co-successes (`replay`, the SMC program with one addition and the 222 classes, not part of the preregistered sample; seeds
94..97, NP = 2048, M = 512, MT = 16384): 33,150 Step-3 successes with the variants' W8; each was rebuilt (W0..W5 by
the inverse expansion) and re-checked with its own l (33,150 passes) and with the other 31 elements of L* through
rows 16..36: 0 further successes (H3 (a)); the 64-class run of 087a18c4 (seeds 90..93, 32,911 successes) gave 0 as well.
The condition tables of the C programs (`lab.h`) and of the attack program (`a0core.py`: cells of A, E, W and the 31
printed two-bit conditions) were compared programmatically: identical. Conversely, the semi-free-start pairs built by
the C program pass the attack program's own step 3b (Section 13.2), and the pairs built by `a0core.py` pass the
repository verifier.
The counted Python program (`a0core.online`, `stress.py` of Appendix A) on 100 further first blocks (seed
`final-check`): 300 passing classes (352.3 expected; classes pass in bursts), 80,588 good pairs (83,099 expected), 21 row-16 passes (step 3b
executed on each); all 1,060,960 lanes of the bit-sliced filters equal the scalar test; the u of all 80,588 good pairs (four-lane groups)
equals the scalar W0 + s0(W1); every good pair satisfies the Step-2 equations; 38,541 operations per first block on average (model
421 + vbar = 44,558; the difference is the sampling noise of the bursty classes).

### 13.2 Semi-free-start collisions with variant dense parts (`sfs.c`)

For a random variant a0 in G and a random l, rows 16..21 are sampled (uniform W_t), then (W6, W7) uniform on F6 x F7
with the variant's W8, until rows 22..36 pass; W0..W5 by the inverse expansion and CV1 by inverting steps 7..0.
Every constructed pair is checked: Lemma 4.1 maps (CV1, a0) back to exactly W0..W13, the two 37-step outputs are
equal, the blocks differ, and every cell of rows -4..36 (W6/W7 XOR cells excepted) and two-bit condition of rows
>= 9 holds. The 18 collisions of the development runs with seeds 1, 7, 11 and 21 (a few seconds each) were also checked with the
repository's `verifier/hash_functions._compress` (all equal 37-step outputs; W8x = bf2e620a, bf8b201f, bca2b331,
bb2ffe15, bebb9691, beeba66a, bb4a3044, bd8453cc, bf676862, bb2d4ed2 and eight more from seed 21, none equal to the
published bf0d78e1), as were the 16 pairs of the organizer-seed emulation of Section 13.3. The four pairs of seed 11
were also fed to the attack program (`a0core.py`: u, the row-16 table, step 3b) from their chaining value and
variant: each time step 3b found exactly the constructed l and returned the constructed pair. Example (a0 = 1eff48ec, l = 8):

```text
a0  1eff48ec   (E4 = 1f0a7f1a, W8x = bb2ffe15; published: 1b21ce20, 1b2d044e, bf0d78e1)
CV1 ca1e70d8 d0e7642d afe0a795 53407f04 8756f134 6eeb3485 7b5500f6 939a18de
M1  d2398fcd 1894b31d 2a8d5ba4 b437321e 939d62c1 cdc21432 57ed42bc 05782450
    bb2ffe15 6d1a90dd faa1d3e0 56aed439 cc2dbbc2 dd2ba0fc bd1d3f7b 7dd43680
M1' d2398fcd 1894b31d 2a8d5ba4 b437321e 939d62c1 cdc21432 77ed42bc 01382c50
    9b2ffe15 681b8277 faa9c7e0 56aed439 cc2dbbc2 dd2ba0fc b95d377b 5dd43680
F_37(CV1, M1) = F_37(CV1, M1') = 3c2953ac 2add5464 5718fd2a 5e87021a 55c64d86 a5d28a3f b283e3a6 99d6eabf
```

### 13.3 Organizer experiments (`experiments/a0core.py`, one program, two ids)

- `a0-sfs-r37` (H2): trials 0..15 each build a 37-step semi-free-start collision as in 13.2 but with a seed-chosen
  class and variant from the 222 selected classes and a seed-chosen l among the 28 elements of L* whose row 16 can
  hold (rows 16..21 by proposals with the row's fixed x-bits of E imposed; row 22 by W22 proposals with its x-cells
  and two-bit conditions imposed, W7 uniform on F7, W6 = W22 - s1(W20) - W15 - s0(W7) accepted iff in F6). It
  returns CV1 || M1 and CV1 || M1' (96 bytes each) iff every check of 13.2 passes plus class membership. These are
  semi-free-start collisions (CV1 is not the IV), so the organizer's full-collision event is not expected; anyone
  can verify them from the raw report with `_compress(..., 37)`. Rows 16..21 restart from row 16 if a row needs more
  than 2^11 proposals (at most 12 restarts); W7 is drawn exactly from F7's affine decomposition. Local emulation of
  the organizer's public-seed request (seed protocol of `experiments/runner.py`, seed `hashsmash-public-seed-v1`, no
  holdout nonce, target configuration 3e8cc338...; `run_exp_org.py` of Appendix A): 16 of 16 trials returned a pair, all 16 verified
  37-step semi-free-start collisions under the repository verifier; 0.54 s; stdout SHA-256 53f34c59..., byte-identical on a
  second run.
- `a0-online-r37` (H1, H3, H5): trials 0..7 each run the counted online program on seed-drawn first blocks until a
  first block with a passing class (at most 64), processing at most two passing classes; every lane of every batch
  is checked against the scalar W6 definition, the u of every good pair (the four-lane group) against the scalar
  W0 + s0(W1), every good pair against the Step-2 equations, and up to 12 good
  pairs against every cell of rows -4..15 for all 32 l. It returns the complete 128-byte messages M0 || M1 and
  M0 || M1' (l = 13) of the first good pair iff all checks passed (they are not expected to collide: that needs rows
  16..36). Local emulation of the public-seed request: 0 mismatches of every kind in all 8 trials (79 first blocks, 137
  passing classes found and 16 processed, 2768 good pairs, 206266 operations counted); 2 trials returned a pair (good pairs per trial 1808, 0, 0, 960, 0, 0, 0, 0; the
  other first blocks' passing classes had no W6 pass among the two processed classes: good pairs come in bursts, Section 5.3);
  1.18 s; stdout SHA-256 c78124a5..., byte-identical on a second run.
- Both are deterministic, standard library only, and run well inside the executor's limits locally.

### 13.4 Development computation

About 25,000 CPU-seconds in total for this filing (the second preregistered SMC study about 1,000; the replay about 1,000;
the two 222-class end-to-end runs about 10,000; the counted Python program, its emulations and the other checks the rest), on top of
the 40,000 of the earlier filings, far inside DEV = 2^40 units (2^40 units are about 2^18.3 = 330,000 CPU-seconds at 2^21.7 units
per CPU-second).

## 14. Memory and advice

Peak memory (all simultaneously resident during the online phase):

| item | bytes |
|---|---|
| R16: 2^32 entries of 32 bits | 17,179,869,184 |
| F6 and F7 bitmaps: 2 x 2^32 bits | 1,073,741,824 |
| row-16 presence table: 2^24 words of 32 bytes | 536,870,912 |
| lane-scan table: 2^24 words of 32 bytes | 536,870,912 |
| variant data: 4 tables x 782,800 x (a0, S0(a0)) in one 32-byte word each | 100,198,400 |
| stored planes: 3,193 batches x at most 41 planes x 32 bytes | 4,189,216 |
| class programs: 1,465,719 instructions (all 222 classes) x 32 bytes | 46,903,008 |
| class planes of the W7 program, broadcast planes, registers, S, L*, row constants, code of the driver | 1,048,576 |
| total | below 19,479,692,032 = 2^34.181 |

Claimed memory: 2^34.2 bytes. The precomputation's temporaries (the 12.1 million (c7, a0) pairs, 97 MB) are freed
before the tables reach their peak. Nonuniform advice: the characteristic, S, L* and the 222 class descriptors (below
2^13 bytes), charged through A_C and A_S; everything else is recomputed in the precomputation.

## 15. Limitations

- H1, H2, H3 are premises. q3 is estimated (Monte Carlo), not proved; no collision has been found and none is
  expected at the scale we can run. The full-scale success probability cannot be observed.
- The published characteristic and SFS pair are used as advice under allowances; we did not rerun the paper's
  SAT solve or characteristic search.
- For 37 steps the measured q3 is about one bit better than the 75 conditions stated in the paper's text; the
  paper's own tables give 74, which the SMC matches stage by stage (6c77089c reached the same conclusion). With
  q3 = 2^-75, log2 T would be 63.57567.
- The bit-slicing of the W6 test and the four-lane groups rely on H5; without the first the claim is 64.91364, without the second 63.11917.
- Memory is large compared with the earlier filings (2^34.2 bytes instead of 2^20) because of the R16 and filter
  tables; memory is reported only under v5.


## Appendix A. Local evidence programs and records

These are the C programs (C99 + pthreads, `cc -O3`) and Python programs that produced the local evidence of Sections 4, 7, 10 and 13,
and the records of the preregistered estimates, of the replay and of the end-to-end runs. They are evidence for the reader, not part of the
attack. The attack's counted program, the class data and the organizer experiments are `experiments/a0core.py`
(standard-library Python; `python3 a0core.py ledger` prints Section 11's numbers). Each block's SHA-256 is given in
its header line. `e2e.c` is the program of the end-to-end runs (Section 13.1; the argument K of its command line is the number of classes:
the runs of this filing use `./e2e 21 14 222 12` and `./e2e 22 19 222 16`). `smc.c` (A.2) and `replay.c` (A.10) are the programs of the
second study with the 222 classes (the 64-class programs of 087a18c4, hashes 4a78d371... and 3879da40..., differ from them only in the two
lines that select the classes and in a header line; their records are A.5 - A.9, A.11 - A.13 below). `replay.c` is `smc.c` with the replay block
added (not part of the preregistered sample). A.14 - A.18 are the second preregistration and its records, A.19 - A.21 the new end-to-end and
replay records, A.22 is `w7var.c` (the variance of the number of passing classes; it reads the first column of Section 5.3's descriptors from `top222.txt`),
A.23 - A.24 the emulation of the organizer requests (Section 13.3; run as `REPO_ROOT=<checkout> python3 run_exp_org.py out.json` in the directory of
`a0core.py`) and A.25 - A.26 the stress run of the counted program (`python3 stress.py SEED N` in that directory).

### A.1 `lab.h` (12574 bytes, SHA-256 5e0e96055fe2042b825e08345e4a2343dca8d7e84bd947312b7856799f27bedf)

```c
/* lab.h - 37-step SHA-256, the ePrint 2026/1120 37-step characteristic, S, L*, and the A0 variant family. */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
typedef uint32_t u32; typedef uint64_t u64;
#define NR 37
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
static const X2c X2[] = {{'A',15,15,'!','A',16,15},{'A',15,23,'=','A',16,23},{'A',15,25,'=','A',16,25},{'A',16,9,'!','A',16,20},
 {'A',16,18,'!','A',16,6},{'A',16,8,'=','A',16,17},{'A',15,29,'=','A',17,29},{'A',17,29,'=','A',18,29},
 {'E',15,4,'=','E',16,4},{'E',17,0,'!','E',17,13},{'E',16,24,'=','E',17,24},{'E',16,15,'=','E',17,15},
 {'E',18,6,'!','E',18,19},{'E',18,2,'=','E',18,20},{'E',20,2,'!','E',20,16},
 {'W',6,1,'=','W',6,12},{'W',6,8,'!','W',6,25},{'W',6,14,'=','W',6,18},
 {'W',7,0,'=','W',7,28},{'W',7,9,'=','W',7,30},{'W',7,1,'=','W',7,18},
 {'W',8,1,'!','W',8,12},{'W',8,8,'!','W',8,25},{'W',8,14,'=','W',8,18},
 {'W',22,31,'!','W',22,1},{'W',22,30,'!','W',22,0},{'W',22,16,'!','W',22,25},{'W',22,14,'!','W',22,21},
 {'W',24,4,'!','W',24,6},{'W',24,22,'=','W',24,31},{'W',24,20,'!','W',24,27}};
#define NX2 ((int)(sizeof(X2)/sizeof(X2[0])))
static void init_char(void) {
  const char *EQ = "================================";
  for (int i = -4; i < NR; i++) { mkcell(&CA[i+O], EQ); mkcell(&CE[i+O], EQ); }
  for (int i = 0; i < NR; i++) mkcell(&CW[i], EQ);
  struct { int i; const char *s; } a[] = {{6,"=nu============================="},{7,"==========n====n====n======n===="},
   {10,"======u===========u============="},{11,"====u=====u=========u=n====u==n="},{12,"=nu============================="},
   {13,"====u=========u=u=======n==u===="},{14,"======u=n=======n==============="},{16,"==u============================="}};
  struct { int i; const char *s; } e[] = {{4,"000============================="},{5,"111=0=====1==0=====01===++01===="},
   {6,"uuu=1011=00=10111=0111=0++1011=="},{7,"10n=u01001n00n00010nu110unuu0001"},{8,"011=1n+1=n11u1101=001u1u1010=u=1"},
   {9,"1=0110+=001=1100=+110100111u=0=+"},{10,"10n001u110101==01+u1101011=1110+"},{11,"=01un000011101=n0n0u1uu101011u1u"},
   {12,"01101uuuuunu010110110n1u0u0uu0n0"},{13,"0+10n110111unn+0n101110110001001"},{14,"=+0=1000000111+=1==1n010u0=0101="},
   {15,"=u==01===n=011n01==u0=u=1==+===="},{16,"=0=====+00===11=+==01=0=0==+===="},{17,"=0=====+01===u1=+==0==1===1u===="},
   {18,"==10===uu====0==n===111===01==1="},{19,"==1====00====1==0==========1===="},{20,"==u====10=======1===00=========="},
   {21,"==0============================="},{22,"==1============================="}};
  struct { int i; const char *s; } w[] = {{6,"==n============================="},{7,"=====u===u==========n==========="},
   {8,"==u============================="},{9,"=====u=u=======n===u==n=u=n=u=n="},{10,"============n======u=n=========="},
   {14,"=0===u===n=1=1====1=u=1=====1=1="},{15,"==u============================="},{22,"=====0=nn=====1=u=1============="},
   {24,"==n============================="}};
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
static const u32 CV0[8] = {0x63b4986c,0x35d83dc0,0xc98894e4,0x784e08fc,0x78a7f752,0x5ed877a8,0x315a2db3,0xd5614eb4};
static const u32 MY[16] = {0x4d7f86ff,0x32ece589,0xd8accfc4,0x2cc2e433,0x068b5b34,0xeba68a28,0x2fe12cad,0x6aa26b0c,
 0x9f0d78e1,0x681b8277,0xfaa9c7e0,0x56aed439,0xcc2dbbc2,0xdd2ba0fc,0xb95d377b,0x5dd43a81};
static const u32 MX[16] = {0x4d7f86ff,0x32ece589,0xd8accfc4,0x2cc2e433,0x068b5b34,0xeba68a28,0x0fe12cad,0x6ee2630c,
 0xbf0d78e1,0x6d1a90dd,0xfaa1d3e0,0x56aed439,0xcc2dbbc2,0xdd2ba0fc,0xbd1d3f7b,0x7dd43a81};
static const u32 HASH0[8] = {0xa856d46e,0x4b46eb28,0x4935248c,0x92a2fc98,0xe0fb2610,0x10a9951f,0x54264f5b,0x80954580};
static const u32 LW15[32] = {0x7dd41680,0x7dd41681,0x7dd416a0,0x7dd416a1,0x7dd41a80,0x7dd41a81,0x7dd41aa0,0x7dd41aa1,
 0x7dd43680,0x7dd43681,0x7dd436a0,0x7dd436a1,0x7dd43a80,0x7dd43a81,0x7dd43aa0,0x7dd43aa1,
 0xfdb41680,0xfdb41681,0xfdb416a0,0xfdb416a1,0xfdb41a80,0xfdb41a81,0xfdb41aa0,0xfdb41aa1,
 0xfdb43680,0xfdb43681,0xfdb436a0,0xfdb436a1,0xfdb43a80,0xfdb43a81,0xfdb43aa0,0xfdb43aa1};
#define W14X 0xbd1d3f7bu
#define W14Y (W14X ^ 0x04400800u)
static Tr PX, PY;                     /* traces of the published pair (x, y) */
static u32 SAx[14], SAy[14];          /* A0..A13 of S */
#define D6 0x20000000u
#define T6 0x03c00800u
#define D7 0xfbc00800u
#define T7 0x017f8000u
#define D8 0xe0000000u
#define T8 0x043ff800u
static inline int inF(u32 w, u32 d, u32 t) { return (u32)(s0(w + d) - s0(w)) == t; }
static u32 C4, W8C;                   /* E4 = a0 + C4; W8x = W8C - E4 */
static void init_S(void) {
  init_char(); trace(CV0, MX, &PX); trace(CV0, MY, &PY);
  for (int i = 0; i < 14; i++) { SAx[i] = PX.A[i+O]; SAy[i] = PY.A[i+O]; }
  C4 = SAx[4] - S0(SAx[3]) - MAJ(SAx[3], SAx[2], SAx[1]);
  const u32 *E = PX.E + O;
  W8C = E[8] - SAx[4] - S1(E[7]) - CH(E[7], E[6], E[5]) - K[8];
}
/* variant family G (cell semantics): E4 = a0 + C4 has E4[31:29] = 000; W8x = W8C - E4 has W8x[29] = 1 (cell u, so W8y =
   W8x - 2^29 differs only in bit 29) and the printed two-bit conditions W8[1] != W8[12], W8[8] != W8[25], W8[14] = W8[18]. */
static inline int inG(u32 a0) {
  u32 e4 = a0 + C4; if (e4 >> 29) return 0;
  u32 w = W8C - e4;
  if (!((w >> 29) & 1)) return 0;
  if (((w >> 1) ^ (w >> 12)) & 1 ^ 1) return 0;
  if (((w >> 8) ^ (w >> 25)) & 1 ^ 1) return 0;
  if (((w >> 14) ^ (w >> 18)) & 1) return 0;
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
  CP *v = malloc(sizeof(CP) * 12200000u); u32 n = 0;
  for (u64 a = 0; a < (1ull << 32); a++) if (inG((u32)a)) { v[n].a0 = (u32)a; v[n].c7 = c7of((u32)a); n++; }
  qsort(v, n, sizeof(CP), cmpCP);
  CL *cl = malloc(sizeof(CL) * 30000); u32 nc = 0;
  for (u32 i = 0; i < n; ) { u32 j = i; while (j < n && v[j].c7 == v[i].c7) j++; cl[nc].c7 = v[i].c7; cl[nc].start = i; cl[nc].n = j - i; nc++; i = j; }
  qsort(cl, nc, sizeof(CL), cmpCL);
  u32 tot = 0; for (int c = 0; c < k; c++) tot += cl[c].n;
  *sel = malloc(4 * tot); u32 q = 0;
  for (int c = 0; c < k; c++) { outc[c] = cl[c]; outc[c].start = q; for (u32 i = 0; i < cl[c].n; i++) (*sel)[q++] = v[cl[c].start + i].a0; }
  free(v); free(cl); return tot;
}
```

### A.2 `smc.c` (7669 bytes, SHA-256 7ac6f21b9aaaba983ddca27df63150aac2cac267a54729309c53ba9181c2ab98)

```c
/* smc.c - sequential Monte-Carlo estimate of q3 = avg over l in L* of Pr[rows 16..36 follow every cell and the
   printed two-bit conditions], for the A0 variant family: W16..W21 iid uniform, (W6, W7) uniform on F6 x F7, and
   W8 = W8C - E4(a0) with a0 uniform on the 222 selected classes (782,800 variants; SMC_ALLG: all of G).  Stages: row 16 (exact enumeration), rows 17..21 (proposal: E_t^x uniform
   with its fixed x-bits, exact weight 2^-f), row 22 (proposal (W6, W7) from F6 x F7), rows 23..36 (W8 from a uniform
   variant).  The stage-23 children are also evaluated with the published W8 (paired comparison).
   usage: smc <seed> <NP> <M> <MT>   (one replicate; prints the stage means and the estimate) */
#include "lab.h"
#include <pthread.h>

static Tr T0x[32], T0y[32];          /* rows <= 15 for each l */
static u32 dW16[32], dW17[32], dW21[32];
static u32 *P16[32]; static u32 C16[32];
static u32 *Glist; static u32 Gn;

static void step_rows(Tr *x, Tr *y, int t) {
  for (int m = 0; m < 2; m++) { Tr *s = m ? y : x; u32 *A = s->A + O, *E = s->E + O;
    E[t] = A[t-4] + E[t-4] + S1(E[t-1]) + CH(E[t-1], E[t-2], E[t-3]) + K[t] + s->W[t];
    A[t] = E[t] - A[t-4] + S0(A[t-1]) + MAJ(A[t-1], A[t-2], A[t-3]); }
}
static void setup(void) {
  init_S();
  for (int l = 0; l < 32; l++) {
    u32 wx[16], wy[16]; memcpy(wx, MX, 64); memcpy(wy, MY, 64);
    wx[15] = LW15[l]; wy[15] = LW15[l] ^ 0x20000000u;
    trace(CV0, wx, &T0x[l]); trace(CV0, wy, &T0y[l]);
    for (int i = -4; i < 16; i++) if (!row_ok(&T0x[l], &T0y[l], i, i != 6 && i != 7)) { fprintf(stderr, "l %d row %d\n", l, i); exit(1); }
    Tr *x = &T0x[l], *y = &T0y[l];
    dW16[l] = (s1(y->W[14]) - s1(x->W[14])) + (y->W[9] - x->W[9]);
    dW17[l] = (s1(y->W[15]) - s1(x->W[15])) + (y->W[10] - x->W[10]);
    dW21[l] = (y->W[14] - x->W[14]) + T6;
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
  else { static CL cc[222]; Gn = select_classes(222, cc, &Glist); }
}

typedef struct { Tr x, y; } Part;
static int NP, M, MT;

static void one(u64 seed, double out[16]) {
  Rng rg; rseed(&rg, seed);
  Part *P = malloc(sizeof(Part) * NP), *Q = malloc(sizeof(Part) * NP);
  int *L = malloc(sizeof(int) * NP), *L2 = malloc(sizeof(int) * NP);
  /* stage 16 */
  u64 tot = 0; for (int l = 0; l < 32; l++) tot += C16[l];
  double z16 = (double)tot / 32.0 / 4294967296.0; out[0] = z16;
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
      u32 dW = (t == 17) ? dW17[l] : (t == 21) ? dW21[l] : 0;
      dW += (t >= 18) ? (u32)(s1(y->W[t-2]) - s1(x->W[t-2])) : 0;
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
      do w7 = r32(&rg); while (!inF(w7, D7, T7)); do w6 = r32(&rg); while (!inF(w6, D6, T6));
      C.x.W[6] = w6; C.y.W[6] = w6 + D6; C.x.W[7] = w7; C.y.W[7] = w7 + D7;
      for (int m = 0; m < 2; m++) { Tr *s = m ? &C.y : &C.x; s->W[22] = s1(s->W[20]) + s->W[15] + s0(s->W[7]) + s->W[6]; }
      step_rows(&C.x, &C.y, 22);
      if (!(row_ok(&C.x, &C.y, 22, 1) && x2_row_ok(&C.x, 22))) continue;
      p22++;
      int okv[2];
      for (int which = 0; which < 2; which++) {
        Part D = C;
        u32 w8x = which ? PX.W[8] : (W8C - (Glist[rnext(&rg) % Gn] + C4));
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
  u64 tot = 0; for (int l = 0; l < 32; l++) tot += C16[l];
  printf("row16 words per l:"); for (int l = 0; l < 32; l++) printf(" %u", C16[l]); printf("  total %llu  |G| %u\n", (unsigned long long)tot, Gn);
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

### A.3 `e2e.c` (9282 bytes, SHA-256 df3086ef7cf4d4763a978718041b2047e50802c16001a6d36504aeddecc0c731)

```c
/* e2e.c - the online phase of the A0-variant attack on real first blocks (scaled down): random M0, CV = F37(IV, M0),
   W7 test per class (K largest c7 classes of G), W6 test per variant of every passing class, then u = W0 + s0(W1) and
   the exact row-16 test for every l in L*.  Reports rates against the model and checks a sample of pairs exactly.
   usage: e2e <seed> <log2 first blocks per thread> <K> <threads> */
#include "lab.h"
#include <pthread.h>

typedef struct { u32 c7, a0; } P;
static int cmpP(const void *a, const void *b) { const P *x = a, *y = b; return x->c7 != y->c7 ? (x->c7 < y->c7 ? -1 : 1) : (x->a0 < y->a0 ? -1 : x->a0 > y->a0); }
typedef struct { u32 c7, start, n; } Cl;
static int cmpC(const void *a, const void *b) { const Cl *x = a, *y = b; return x->n != y->n ? (x->n > y->n ? -1 : 1) : (x->c7 < y->c7 ? -1 : 1); }

static int KC; static Cl *cls; static P *vars;
static u32 *va0, *ve54, *vk3, *vS0;          /* per variant, class-major */
static u64 *F6bm, *F7bm;
static u32 C6, A1c, nE5, KAP1;
static u32 *R16v[32]; static u32 R16n[32]; static u32 C16[32];
static inline int bm(const u64 *b, u32 w) { return (b[w >> 6] >> (w & 63)) & 1; }
static int cmpu(const void *a, const void *b) { u32 x = *(u32*)a, y = *(u32*)b; return x < y ? -1 : x > y; }
static int inR16(int l, u32 e) { u32 lo = 0, hi = R16n[l]; while (lo < hi) { u32 m = (lo + hi) / 2; if (R16v[l][m] < e) lo = m + 1; else hi = m; } return lo < R16n[l] && R16v[l][lo] == e; }

static void step_rows(Tr *x, Tr *y, int t) {
  for (int m = 0; m < 2; m++) { Tr *s = m ? y : x; u32 *A = s->A + O, *E = s->E + O;
    E[t] = A[t-4] + E[t-4] + S1(E[t-1]) + CH(E[t-1], E[t-2], E[t-3]) + K[t] + s->W[t];
    A[t] = E[t] - A[t-4] + S0(A[t-1]) + MAJ(A[t-1], A[t-2], A[t-3]); }
}
static void setup(int Kn) {
  init_S(); KC = Kn;
  vars = malloc(sizeof(P) * 12200000u); u32 n = 0;
  for (u64 a = 0; a < (1ull << 32); a++) if (inG((u32)a)) { vars[n].a0 = (u32)a; vars[n].c7 = c7of((u32)a); n++; }
  qsort(vars, n, sizeof(P), cmpP);
  cls = malloc(sizeof(Cl) * 30000); u32 nc = 0;
  for (u32 i = 0; i < n; ) { u32 j = i; while (j < n && vars[j].c7 == vars[i].c7) j++; cls[nc].c7 = vars[i].c7; cls[nc].start = i; cls[nc].n = j - i; nc++; i = j; }
  qsort(cls, nc, sizeof(Cl), cmpC);
  u32 tot = 0; for (int c = 0; c < Kn; c++) tot += cls[c].n;
  va0 = malloc(4 * tot); ve54 = malloc(4 * tot); vk3 = malloc(4 * tot); vS0 = malloc(4 * tot);
  const u32 *A = SAx, *E = PX.E + O; u32 k = 0;
  for (int c = 0; c < Kn; c++) { u32 st = cls[c].start; cls[c].start = k;
    for (u32 i = 0; i < cls[c].n; i++, k++) { u32 a0 = vars[st + i].a0; va0[k] = a0; ve54[k] = E[5] & (a0 + C4);
      vk3[k] = A[3] - S0(A[2]) - MAJ(A[2], A[1], a0); vS0[k] = S0(a0); } }
  C6 = E[6] - 2 * A[2] + S0(A[1]) - S1(E[5]) - K[6]; A1c = A[1]; nE5 = ~E[5]; KAP1 = A[1] - K[1];
  F6bm = calloc(1u << 26, 8); F7bm = calloc(1u << 26, 8);
  for (u64 w = 0; w < (1ull << 32); w++) { if (inF((u32)w, D6, T6)) F6bm[w >> 6] |= 1ull << (w & 63); if (inF((u32)w, D7, T7)) F7bm[w >> 6] |= 1ull << (w & 63); }
  /* row 16 sets: E16x values per l passing the whole row 16 (both members) */
  for (int l = 0; l < 32; l++) {
    u32 wx[16], wy[16]; memcpy(wx, MX, 64); memcpy(wy, MY, 64); wx[15] = LW15[l]; wy[15] = LW15[l] ^ 0x20000000u;
    Tr x, y; trace(CV0, wx, &x); trace(CV0, wy, &y);
    u32 dW16 = (s1(y.W[14]) - s1(x.W[14])) + (y.W[9] - x.W[9]);
    u32 base = x.A[12+O] + x.E[12+O] + S1(x.E[15+O]) + CH(x.E[15+O], x.E[14+O], x.E[13+O]) + K[16];
    C16[l] = base + s1(x.W[14]) + x.W[9];                  /* E16x = C16[l] + W0 + s0(W1) */
    Cell *c = &CE[16+O]; u32 fr = ~c->m, e = 0, cnt = 0; R16v[l] = malloc(4u << 22);
    do { u32 E16 = e | c->v; Tr X = x, Y = y; X.W[16] = E16 - base; Y.W[16] = X.W[16] + dW16; step_rows(&X, &Y, 16);
      if (row_ok(&X, &Y, 16, 1) && x2_row_ok(&X, 16)) R16v[l][cnt++] = E16; e = (e - fr) & fr; } while (e);
    R16n[l] = cnt; qsort(R16v[l], cnt, 4, cmpu);
  }
  fprintf(stderr, "setup: |G| %u, %u classes, K %d with %u variants (2^%.3f)\n", n, nc, Kn, tot, log2((double)tot));
}

typedef struct { u64 seed; int lg; u64 fb, w7pass, good, r16, r16pairs, clumps2, chk, chkbad, gp_hist[8]; double sumsq, gg1, rr1; } Job;
static void *run(void *arg) {
  Job *J = arg; Rng rg; rseed(&rg, J->seed);
  u64 nfb = 1ull << J->lg;
  for (u64 f = 0; f < nfb; f++) {
    u32 m0[16], cv[8]; for (int j = 0; j < 16; j++) m0[j] = r32(&rg);
    compress(IV0, m0, cv); J->fb++;
    u32 a = cv[0], b = cv[1];
    u32 cb = C6 - b, Pm = A1c & a, Qm = A1c | a;
    /* per-CV constants for u */
    u32 Am1 = cv[0], Am2 = cv[1], Am3 = cv[2], Am4 = cv[3], Em1 = cv[4], Em2 = cv[5], Em3 = cv[6], Em4 = cv[7];
    u32 e0b = Am4 - S0(Am1) - MAJ(Am1, Am2, Am3);
    u32 kap0 = e0b - Am4 - Em4 - S1(Em1) - CH(Em1, Em2, Em3) - K[0];
    u32 o12 = Am1 | Am2, n12 = Am1 & Am2, X = Em1 ^ Em2, kap1 = KAP1 - Em3;
    u64 goodcv = 0, r16cv = 0;
    for (int c = 0; c < KC; c++) {
      if (!bm(F7bm, cls[c].c7 - a)) continue;
      J->w7pass++;
      u32 st = cls[c].start, n = cls[c].n; u64 r16here = 0;
      for (u32 i = st; i < st + n; i++) {
        u32 maj = Pm | (va0[i] & Qm), e3 = vk3[i] + a;
        u32 w6 = cb + maj - ve54[i] - (nE5 & e3);
        if (!bm(F6bm, w6)) continue;
        J->good++; goodcv++;
        u32 a0 = va0[i], E0 = a0 + e0b, W0 = a0 + kap0;
        u32 mj = n12 | (a0 & o12), ch = (E0 & X) ^ Em2;
        u32 W1 = kap1 - vS0[i] - mj - S1(E0) - ch, u = W0 + s0(W1);
        int any = 0;
        for (int l = 0; l < 32; l++) if (R16n[l] && inR16(l, C16[l] + u)) { any = 1; J->r16++;
          /* exact check of this pair: words, filters, rows -4..16 */
          if (J->chk < 2000) { u32 wx[16], wy[16]; words_from_cv(cv, a0, wx, wy);
            wx[14] = W14X; wx[15] = LW15[l]; wy[14] = W14Y; wy[15] = LW15[l] ^ 0x20000000u;
            Tr tx, ty; trace(cv, wx, &tx); trace(cv, wy, &ty); int ok = inF(wx[6], D6, T6) && inF(wx[7], D7, T7) && wx[6] == w6 && wx[0] == W0 && wx[1] == W1;
            for (int r = -4; r <= 16; r++) ok &= row_ok(&tx, &ty, r, r != 6 && r != 7);
            ok &= x2_row_ok(&tx, 16) && x2_row_ok(&tx, 15); J->chk++; J->chkbad += !ok; } }
        r16here += any;
      }
      J->r16pairs += r16here; J->clumps2 += r16here >= 2; r16cv += r16here;
    }
    J->gp_hist[goodcv == 0 ? 0 : goodcv < 128 ? 1 : goodcv < 256 ? 2 : goodcv < 512 ? 3 : goodcv < 1024 ? 4 : 5]++;
    J->sumsq += (double)goodcv * goodcv; J->gg1 += (double)goodcv * (goodcv ? goodcv - 1 : 0); J->rr1 += (double)r16cv * (r16cv ? r16cv - 1 : 0);
  }
  return 0;
}
int main(int argc, char **argv) {
  u64 seed = argc > 1 ? strtoull(argv[1], 0, 10) : 1; int lg = argc > 2 ? atoi(argv[2]) : 16, Kq = argc > 3 ? atoi(argv[3]) : 64, nt = argc > 4 ? atoi(argv[4]) : 8;
  setup(Kq);
  u64 Vt = 0; for (int c = 0; c < Kq; c++) Vt += cls[c].n;
  Job J[64]; pthread_t th[64]; memset(J, 0, sizeof J);
  for (int i = 0; i < nt; i++) { J[i].seed = seed * 100 + i; J[i].lg = lg; pthread_create(&th[i], 0, run, &J[i]); }
  Job T; memset(&T, 0, sizeof T);
  for (int i = 0; i < nt; i++) { pthread_join(th[i], 0); T.fb += J[i].fb; T.w7pass += J[i].w7pass; T.good += J[i].good; T.r16 += J[i].r16;
    T.r16pairs += J[i].r16pairs; T.clumps2 += J[i].clumps2; T.chk += J[i].chk; T.chkbad += J[i].chkbad; T.sumsq += J[i].sumsq; T.gg1 += J[i].gg1; T.rr1 += J[i].rr1;
    for (int h = 0; h < 8; h++) T.gp_hist[h] += J[i].gp_hist[h]; }
  double p7 = 68157440.0 / 4294967296.0, p6 = 287309824.0 / 4294967296.0, r16tot = 0; for (int l = 0; l < 32; l++) r16tot += R16n[l];
  double ew7 = T.fb * Kq * p7, egood = T.fb * (double)Vt * p7 * p6, er16 = T.good * r16tot / 4294967296.0;
  printf("first blocks %llu (2^%.2f), K %d, V_tot %llu\n", (unsigned long long)T.fb, log2((double)T.fb), Kq, (unsigned long long)Vt);
  printf("W7-passing (CV, class): %llu, expected %.1f (z %+.2f)\n", (unsigned long long)T.w7pass, ew7, (T.w7pass - ew7) / sqrt(ew7));
  printf("good pairs: %llu, expected %.1f (ratio %.4f)\n", (unsigned long long)T.good, egood, T.good / egood);
  printf("row-16 passes (pair, l): %llu, expected %.1f (z %+.2f); pairs with >=1: %llu\n", (unsigned long long)T.r16, er16, (T.r16 - er16) / sqrt(er16), (unsigned long long)T.r16pairs);
  double lam = (double)T.r16pairs / T.w7pass;  /* per (CV, class) clump */
  double nc = (double)T.good / T.w7pass;
  printf("clumps with >=2 row-16 pairs: %llu; independent-binomial expectation %.1f\n", (unsigned long long)T.clumps2,
         T.w7pass * (1 - pow(1 - lam / nc, nc) - nc * (lam / nc) * pow(1 - lam / nc, nc - 1)));
  { double p = (double)T.r16pairs / T.good; printf("within-first-block pairwise correlation of row-16 success (any l): rho = %.3f (sum R(R-1) %.0f, p^2 sum G(G-1) %.1f)\n", T.rr1 / (p * p * T.gg1), T.rr1, p * p * T.gg1); }
  printf("exact pair checks: %llu, failures %llu\n", (unsigned long long)T.chk, (unsigned long long)T.chkbad);
  printf("good pairs per CV: mean %.2f, var %.1f; hist 0:%llu <128:%llu <256:%llu <512:%llu <1024:%llu more:%llu\n", (double)T.good / T.fb,
         T.sumsq / T.fb - pow((double)T.good / T.fb, 2), (unsigned long long)T.gp_hist[0], (unsigned long long)T.gp_hist[1], (unsigned long long)T.gp_hist[2],
         (unsigned long long)T.gp_hist[3], (unsigned long long)T.gp_hist[4], (unsigned long long)T.gp_hist[5]);
  return 0;
}
```

### A.4 `sfs.c` (5550 bytes, SHA-256 0af715352b5afdc45f47818167f1ba952801cbad523d5ed6d08972a114e5f0d7)

```c
/* sfs.c - checks of S and the A0 variant family, and construction of 37-step semi-free-start collisions whose
   second-block state uses a random variant a0 in G (so E4, W8 differ from the published pair).
   usage: sfs <seed> <count>   prints each pair as: SFS a0 cv[8] mx[16] my[16] */
#include "lab.h"

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
  if (seed == 1) { u64 g = 0; for (u64 a = 0; a < (1ull << 32); a++) g += inG((u32)a);
    fprintf(stderr, "|G| = %llu = 2^%.4f\n", (unsigned long long)g, log2((double)g)); }
  /* 3. semi-free-start collisions with random variants */
  for (int c = 0; c < count; c++) {
    u32 a0; do a0 = r32(&rg); while (!inG(a0) || a0 == SAx[0]);
    int l = (int)(r32(&rg) & 31);
    words_from_cv(CV0, a0, wx, wy);
    wx[14] = W14X; wx[15] = LW15[l]; wy[14] = W14Y; wy[15] = LW15[l] ^ 0x20000000u;
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
    for (int r = 9; r < NR; r++) okc &= x2_row_ok(&X, r);
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

### A.5 `PREREG_q3.txt` (975 bytes, SHA-256 4b0a1d39c8b09bd30d1656906adbe5c42633c6403986f287530c0fac48d8a57d)

```text
q3 SMC preregistration (A0-variant attack, sha256-r37), frozen 2026-10-09T13:44:50Z before any listed seed ran.
program: smc.c sha256 4a78d3718e22ca887a6e2dbb351d24a2ed539ab9908127ce6b756bf24264ccca  lab.h sha256 5e0e96055fe2042b825e08345e4a2343dca8d7e84bd947312b7856799f27bedf
build: cc -O3 -march=native -o smc smc.c -lm -lpthread
W8 drawn uniformly from the 230,400 variants of the 64 selected classes (default; SMC_ALLG unset).
parameters: NP=2048 M=512 MT=16384, 8 replicates per invocation.
invocations: ./smc 70 2048 512 16384 8 ; ./smc 71 ... ; ./smc 72 ... ; ./smc 73 ...  -> replicate seeds 70000..70007, 71000..71007, 72000..72007, 73000..73007 (32 replicates).
estimate per replicate: product of stage means (16 exact, 17..21, 22, 23..36 with the variant W8) = 'q3 variant'.
rule: Z_s linear estimates (32); LB = mean - t*sd/sqrt(32), t = 2.4528 (one-sided 99%, 31 df); q3_model = 2^(floor(100*log2(LB))/100).
All 32 replicates are reported; none may be dropped.
```

### A.6 `smc_70.txt` (1837 bytes, SHA-256 a957ed56a8f7d76a1343da9e0af42b02e6b72d90feb6d6654f7cf1aaeb106d8e)

```text
row16 words per l: 0 16384 0 16384 32768 8192 32768 4096 65536 49152 65536 49152 32768 57344 32768 59392 0 16384 0 16384 32768 16384 24576 12288 65536 49152 65536 49152 32768 49152 45056 55296  total 1052672  |G| 230400
seed 70000 stages(log2) 16:-16.994 17:-12.997 18:-14.950 19:-6.000 20:-6.999 21:-1.000 22:-10.996 23v:-4.051 23p:-4.058 | q3 variant 2^-73.9876 published-W8 2^-73.9949 | n22 16425 v 991 p 986 both 95
seed 70001 stages(log2) 16:-16.994 17:-13.001 18:-14.940 19:-6.000 20:-6.999 21:-1.000 22:-11.007 23v:-3.974 23p:-3.995 | q3 variant 2^-73.9155 published-W8 2^-73.9365 | n22 16310 v 1038 p 1023 both 129
seed 70002 stages(log2) 16:-16.994 17:-12.994 18:-14.988 19:-6.000 20:-6.999 21:-1.000 22:-11.017 23v:-3.989 23p:-3.988 | q3 variant 2^-73.9814 published-W8 2^-73.9800 | n22 16197 v 1020 p 1021 both 103
seed 70003 stages(log2) 16:-16.994 17:-13.001 18:-14.988 19:-6.000 20:-7.001 21:-1.000 22:-10.991 23v:-4.068 23p:-4.009 | q3 variant 2^-74.0432 published-W8 2^-73.9843 | n22 16484 v 983 p 1024 both 108
seed 70004 stages(log2) 16:-16.994 17:-13.006 18:-15.002 19:-6.000 20:-7.002 21:-1.000 22:-11.006 23v:-3.998 23p:-3.990 | q3 variant 2^-74.0088 published-W8 2^-74.0003 | n22 16313 v 1021 p 1027 both 96
seed 70005 stages(log2) 16:-16.994 17:-12.992 18:-14.942 19:-6.000 20:-7.000 21:-1.000 22:-11.004 23v:-3.966 23p:-4.110 | q3 variant 2^-73.8994 published-W8 2^-74.0430 | n22 16334 v 1045 p 946 both 117
seed 70006 stages(log2) 16:-16.994 17:-12.991 18:-15.007 19:-6.000 20:-7.001 21:-1.000 22:-10.994 23v:-4.054 23p:-3.984 | q3 variant 2^-74.0406 published-W8 2^-73.9710 | n22 16456 v 991 p 1040 both 121
seed 70007 stages(log2) 16:-16.994 17:-13.010 18:-14.957 19:-6.000 20:-6.999 21:-1.000 22:-11.004 23v:-3.976 23p:-3.894 | q3 variant 2^-73.9408 published-W8 2^-73.8584 | n22 16339 v 1038 p 1099 both 107
```

### A.7 `smc_71.txt` (1837 bytes, SHA-256 c2a9a32646c865f92561019347741ba5df64bf831b62e11fb01db90e79fc0c2e)

```text
row16 words per l: 0 16384 0 16384 32768 8192 32768 4096 65536 49152 65536 49152 32768 57344 32768 59392 0 16384 0 16384 32768 16384 24576 12288 65536 49152 65536 49152 32768 49152 45056 55296  total 1052672  |G| 230400
seed 71000 stages(log2) 16:-16.994 17:-13.009 18:-15.028 19:-6.000 20:-7.001 21:-1.000 22:-10.984 23v:-4.047 23p:-4.155 | q3 variant 2^-74.0639 published-W8 2^-74.1715 | n22 16563 v 1002 p 930 both 92
seed 71001 stages(log2) 16:-16.994 17:-13.001 18:-14.995 19:-6.000 20:-7.001 21:-1.000 22:-11.020 23v:-4.080 23p:-4.000 | q3 variant 2^-74.0915 published-W8 2^-74.0107 | n22 16155 v 955 p 1010 both 100
seed 71002 stages(log2) 16:-16.994 17:-12.995 18:-15.002 19:-6.000 20:-6.998 21:-1.000 22:-11.024 23v:-4.002 23p:-3.995 | q3 variant 2^-74.0153 published-W8 2^-74.0082 | n22 16117 v 1006 p 1011 both 127
seed 71003 stages(log2) 16:-16.994 17:-12.989 18:-15.051 19:-6.000 20:-7.002 21:-1.000 22:-11.010 23v:-3.993 23p:-3.920 | q3 variant 2^-74.0387 published-W8 2^-73.9658 | n22 16270 v 1022 p 1075 both 121
seed 71004 stages(log2) 16:-16.994 17:-12.998 18:-14.997 19:-6.000 20:-7.002 21:-1.000 22:-11.002 23v:-3.918 23p:-4.003 | q3 variant 2^-73.9118 published-W8 2^-73.9970 | n22 16357 v 1082 p 1020 both 116
seed 71005 stages(log2) 16:-16.994 17:-13.008 18:-14.984 19:-6.000 20:-7.001 21:-1.000 22:-10.996 23v:-3.925 23p:-3.983 | q3 variant 2^-73.9072 published-W8 2^-73.9657 | n22 16430 v 1082 p 1039 both 120
seed 71006 stages(log2) 16:-16.994 17:-12.996 18:-14.979 19:-6.000 20:-7.002 21:-1.000 22:-11.000 23v:-4.058 23p:-3.895 | q3 variant 2^-74.0282 published-W8 2^-73.8648 | n22 16389 v 984 p 1102 both 111
seed 71007 stages(log2) 16:-16.994 17:-12.995 18:-14.994 19:-6.000 20:-7.002 21:-1.000 22:-10.991 23v:-4.068 23p:-4.055 | q3 variant 2^-74.0446 published-W8 2^-74.0314 | n22 16486 v 983 p 992 both 92
```

### A.8 `smc_72.txt` (1840 bytes, SHA-256 8c8ddd5c5525cfed8ca170b59dae2042322ab651b8a3741c88e26cd66ec5aa60)

```text
row16 words per l: 0 16384 0 16384 32768 8192 32768 4096 65536 49152 65536 49152 32768 57344 32768 59392 0 16384 0 16384 32768 16384 24576 12288 65536 49152 65536 49152 32768 49152 45056 55296  total 1052672  |G| 230400
seed 72000 stages(log2) 16:-16.994 17:-13.003 18:-15.015 19:-6.000 20:-6.999 21:-1.000 22:-10.992 23v:-4.084 23p:-4.055 | q3 variant 2^-74.0879 published-W8 2^-74.0585 | n22 16470 v 971 p 991 both 125
seed 72001 stages(log2) 16:-16.994 17:-12.995 18:-14.987 19:-6.000 20:-6.999 21:-1.000 22:-11.030 23v:-3.964 23p:-3.964 | q3 variant 2^-73.9697 published-W8 2^-73.9697 | n22 16047 v 1028 p 1028 both 116
seed 72002 stages(log2) 16:-16.994 17:-12.997 18:-15.015 19:-6.000 20:-7.002 21:-1.000 22:-10.992 23v:-3.967 23p:-4.078 | q3 variant 2^-73.9680 published-W8 2^-74.0791 | n22 16472 v 1053 p 975 both 116
seed 72003 stages(log2) 16:-16.994 17:-12.993 18:-14.988 19:-6.000 20:-7.002 21:-1.000 22:-11.006 23v:-4.017 23p:-3.951 | q3 variant 2^-74.0003 published-W8 2^-73.9346 | n22 16316 v 1008 p 1055 both 110
seed 72004 stages(log2) 16:-16.994 17:-12.998 18:-14.970 19:-6.000 20:-6.999 21:-1.000 22:-11.010 23v:-3.972 23p:-3.983 | q3 variant 2^-73.9431 published-W8 2^-73.9543 | n22 16269 v 1037 p 1029 both 125
seed 72005 stages(log2) 16:-16.994 17:-12.990 18:-15.000 19:-6.000 20:-6.999 21:-1.000 22:-11.006 23v:-4.060 23p:-3.941 | q3 variant 2^-74.0498 published-W8 2^-73.9309 | n22 16313 v 978 p 1062 both 123
seed 72006 stages(log2) 16:-16.994 17:-13.000 18:-14.957 19:-6.000 20:-7.001 21:-1.000 22:-10.991 23v:-3.946 23p:-3.988 | q3 variant 2^-73.8889 published-W8 2^-73.9314 | n22 16486 v 1070 p 1039 both 134
seed 72007 stages(log2) 16:-16.994 17:-13.002 18:-15.000 19:-6.000 20:-7.000 21:-1.000 22:-11.016 23v:-3.982 23p:-4.019 | q3 variant 2^-73.9943 published-W8 2^-74.0313 | n22 16207 v 1026 p 1000 both 107
```

### A.9 `smc_73.txt` (1840 bytes, SHA-256 ea9392afe72e83bf34c846841782b6a2b70af8484258d8800b149e1e037f5de9)

```text
row16 words per l: 0 16384 0 16384 32768 8192 32768 4096 65536 49152 65536 49152 32768 57344 32768 59392 0 16384 0 16384 32768 16384 24576 12288 65536 49152 65536 49152 32768 49152 45056 55296  total 1052672  |G| 230400
seed 73000 stages(log2) 16:-16.994 17:-13.008 18:-15.020 19:-6.000 20:-7.002 21:-1.000 22:-10.999 23v:-3.979 23p:-4.044 | q3 variant 2^-74.0025 published-W8 2^-74.0678 | n22 16398 v 1040 p 994 both 118
seed 73001 stages(log2) 16:-16.994 17:-13.003 18:-15.012 19:-6.000 20:-7.000 21:-1.000 22:-10.994 23v:-3.914 23p:-4.095 | q3 variant 2^-73.9169 published-W8 2^-74.0983 | n22 16457 v 1092 p 963 both 98
seed 73002 stages(log2) 16:-16.994 17:-12.997 18:-14.989 19:-6.000 20:-7.002 21:-1.000 22:-10.997 23v:-3.959 23p:-4.023 | q3 variant 2^-73.9381 published-W8 2^-74.0024 | n22 16420 v 1056 p 1010 both 104
seed 73003 stages(log2) 16:-16.994 17:-13.006 18:-14.965 19:-6.000 20:-6.999 21:-1.000 22:-10.988 23v:-3.962 23p:-3.989 | q3 variant 2^-73.9141 published-W8 2^-73.9415 | n22 16516 v 1060 p 1040 both 119
seed 73004 stages(log2) 16:-16.994 17:-13.009 18:-15.015 19:-6.000 20:-7.000 21:-1.000 22:-11.013 23v:-4.060 23p:-3.948 | q3 variant 2^-74.0919 published-W8 2^-73.9793 | n22 16232 v 973 p 1052 both 111
seed 73005 stages(log2) 16:-16.994 17:-12.995 18:-15.016 19:-6.000 20:-7.001 21:-1.000 22:-10.998 23v:-4.034 23p:-3.992 | q3 variant 2^-74.0380 published-W8 2^-73.9968 | n22 16410 v 1002 p 1031 both 108
seed 73006 stages(log2) 16:-16.994 17:-13.002 18:-14.986 19:-6.000 20:-7.001 21:-1.000 22:-10.988 23v:-4.025 23p:-3.998 | q3 variant 2^-73.9956 published-W8 2^-73.9689 | n22 16526 v 1015 p 1034 both 105
seed 73007 stages(log2) 16:-16.994 17:-13.003 18:-15.008 19:-6.000 20:-7.000 21:-1.000 22:-10.994 23v:-4.028 23p:-3.917 | q3 variant 2^-74.0285 published-W8 2^-73.9170 | n22 16447 v 1008 p 1089 both 116
```

### A.10 `replay.c` (9522 bytes, SHA-256 80eb9d20250c068fddc2d3fd0c6cd5fc0a3e240d358b43f4081a09e34c3e96b2)

```c
/* replay.c - (from smc.c) for every tail success with a variant's W8, rebuild W0..W5 and test every other l in L*
   through rows 16..36 (same first-block words, same variant): counts co-successes.  Not part of the preregistered sample.
   Original header: sequential Monte-Carlo estimate of q3 = avg over l in L* of Pr[rows 16..36 follow every cell and the
   printed two-bit conditions], for the A0 variant family: W16..W21 iid uniform, (W6, W7) uniform on F6 x F7, and
   W8 = W8C - E4(a0) with a0 uniform on the 222 selected classes (782,800 variants).  Stages: row 16 (exact enumeration), rows 17..21 (proposal: E_t^x uniform
   with its fixed x-bits, exact weight 2^-f), row 22 (proposal (W6, W7) from F6 x F7), rows 23..36 (W8 from a uniform
   variant).  The stage-23 children are also evaluated with the published W8 (paired comparison).
   usage: smc <seed> <NP> <M> <MT>   (one replicate; prints the stage means and the estimate) */
#include "lab.h"
#include <pthread.h>

static Tr T0x[32], T0y[32];          /* rows <= 15 for each l */
static u32 dW16[32], dW17[32], dW21[32];
static u32 *P16[32]; static u32 C16[32];
static u32 *Glist; static u32 Gn;

static void step_rows(Tr *x, Tr *y, int t) {
  for (int m = 0; m < 2; m++) { Tr *s = m ? y : x; u32 *A = s->A + O, *E = s->E + O;
    E[t] = A[t-4] + E[t-4] + S1(E[t-1]) + CH(E[t-1], E[t-2], E[t-3]) + K[t] + s->W[t];
    A[t] = E[t] - A[t-4] + S0(A[t-1]) + MAJ(A[t-1], A[t-2], A[t-3]); }
}
static void setup(void) {
  init_S();
  for (int l = 0; l < 32; l++) {
    u32 wx[16], wy[16]; memcpy(wx, MX, 64); memcpy(wy, MY, 64);
    wx[15] = LW15[l]; wy[15] = LW15[l] ^ 0x20000000u;
    trace(CV0, wx, &T0x[l]); trace(CV0, wy, &T0y[l]);
    for (int i = -4; i < 16; i++) if (!row_ok(&T0x[l], &T0y[l], i, i != 6 && i != 7)) { fprintf(stderr, "l %d row %d\n", l, i); exit(1); }
    Tr *x = &T0x[l], *y = &T0y[l];
    dW16[l] = (s1(y->W[14]) - s1(x->W[14])) + (y->W[9] - x->W[9]);
    dW17[l] = (s1(y->W[15]) - s1(x->W[15])) + (y->W[10] - x->W[10]);
    dW21[l] = (y->W[14] - x->W[14]) + T6;
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
  else { static CL cc[222]; Gn = select_classes(222, cc, &Glist); }
}

typedef struct { Tr x, y; } Part;
static int NP, M, MT;
static u64 REP_SUCC[64], REP_CO[64], REP_SELF[64];

static void one(u64 seed, double out[16]) {
  Rng rg; rseed(&rg, seed);
  Part *P = malloc(sizeof(Part) * NP), *Q = malloc(sizeof(Part) * NP);
  int *L = malloc(sizeof(int) * NP), *L2 = malloc(sizeof(int) * NP);
  /* stage 16 */
  u64 tot = 0; for (int l = 0; l < 32; l++) tot += C16[l];
  double z16 = (double)tot / 32.0 / 4294967296.0; out[0] = z16;
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
      u32 dW = (t == 17) ? dW17[l] : (t == 21) ? dW21[l] : 0;
      dW += (t >= 18) ? (u32)(s1(y->W[t-2]) - s1(x->W[t-2])) : 0;
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
      do w7 = r32(&rg); while (!inF(w7, D7, T7)); do w6 = r32(&rg); while (!inF(w6, D6, T6));
      C.x.W[6] = w6; C.y.W[6] = w6 + D6; C.x.W[7] = w7; C.y.W[7] = w7 + D7;
      for (int m = 0; m < 2; m++) { Tr *s = m ? &C.y : &C.x; s->W[22] = s1(s->W[20]) + s->W[15] + s0(s->W[7]) + s->W[6]; }
      step_rows(&C.x, &C.y, 22);
      if (!(row_ok(&C.x, &C.y, 22, 1) && x2_row_ok(&C.x, 22))) continue;
      p22++;
      int okv[2];
      for (int which = 0; which < 2; which++) {
        Part D = C;
        u32 w8x = which ? PX.W[8] : (W8C - (Glist[rnext(&rg) % Gn] + C4));
        D.x.W[8] = w8x; D.y.W[8] = w8x + D8;
        int ok = 1;
        for (int t = 23; t < NR && ok; t++) {
          for (int m = 0; m < 2; m++) { Tr *s = m ? &D.y : &D.x; s->W[t] = s1(s->W[t-2]) + s->W[t-7] + s0(s->W[t-15]) + s->W[t-16]; }
          step_rows(&D.x, &D.y, t);
          ok = row_ok(&D.x, &D.y, t, 1) && x2_row_ok(&D.x, t);
        }
        okv[which] = ok;
        if (ok && which == 0) {   /* replay over all l' */
          int tid = (int)(seed % 1000); u32 W[16]; Tr *x = &D.x;
          for (int i = 6; i < 16; i++) W[i] = x->W[i];
          W[5] = x->W[21] - s1(x->W[19]) - x->W[14] - s0(W[6]); W[4] = x->W[20] - s1(x->W[18]) - x->W[13] - s0(W[5]);
          W[3] = x->W[19] - s1(x->W[17]) - x->W[12] - s0(W[4]); W[2] = x->W[18] - s1(x->W[16]) - x->W[11] - s0(W[3]);
          W[1] = x->W[17] - s1(x->W[15]) - x->W[10] - s0(W[2]); W[0] = x->W[16] - s1(x->W[14]) - x->W[9] - s0(W[1]);
          REP_SUCC[tid]++;
          for (int l2 = 0; l2 < 32; l2++) {
            Tr X = T0x[l2], Y = T0y[l2];
            for (int i = 0; i < 16; i++) { X.W[i] = W[i]; Y.W[i] = W[i]; }
            for (int i = 6; i < 14; i++) Y.W[i] = D.y.W[i];
            X.W[14] = W14X; X.W[15] = LW15[l2]; Y.W[14] = W14Y; Y.W[15] = LW15[l2] ^ 0x20000000u;
            int ok2 = 1;
            for (int t = 16; t < NR && ok2; t++) {
              for (int m = 0; m < 2; m++) { Tr *s = m ? &Y : &X; s->W[t] = s1(s->W[t-2]) + s->W[t-7] + s0(s->W[t-15]) + s->W[t-16]; }
              step_rows(&X, &Y, t); ok2 = row_ok(&X, &Y, t, 1) && x2_row_ok(&X, t);
            }
            if (l2 == L[p]) REP_SELF[tid] += ok2; else REP_CO[tid] += ok2;
          }
        }
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
  u64 tot = 0; for (int l = 0; l < 32; l++) tot += C16[l];
  printf("row16 words per l:"); for (int l = 0; l < 32; l++) printf(" %u", C16[l]); printf("  total %llu  |G| %u\n", (unsigned long long)tot, Gn);
  pthread_t th[64]; Job jb[64];
  for (int i = 0; i < nt; i++) { jb[i].seed = seed * 1000 + i; pthread_create(&th[i], 0, run, &jb[i]); }
  for (int i = 0; i < nt; i++) pthread_join(th[i], 0);
  { u64 su = 0, co = 0, se = 0; for (int i = 0; i < 64; i++) { su += REP_SUCC[i]; co += REP_CO[i]; se += REP_SELF[i]; }
    printf("REPLAY tail successes %llu, self re-checks passed %llu, other-l co-successes %llu\n", (unsigned long long)su, (unsigned long long)se, (unsigned long long)co); }
  for (int i = 0; i < nt; i++) { double *o = jb[i].out, zv = 1, zp;
    for (int s = 0; s < 7; s++) zv *= o[s]; zp = zv * o[8]; zv *= o[7];
    printf("seed %llu stages(log2) 16:%.3f 17:%.3f 18:%.3f 19:%.3f 20:%.3f 21:%.3f 22:%.3f 23v:%.3f 23p:%.3f | q3 variant 2^%.4f published-W8 2^%.4f | n22 %.0f v %.0f p %.0f both %.0f\n",
      (unsigned long long)jb[i].seed, log2(o[0]), log2(o[1]), log2(o[2]), log2(o[3]), log2(o[4]), log2(o[5]), log2(o[6]), log2(o[7]), log2(o[8]),
      log2(zv), log2(zp), o[9], o[10], o[11], o[12]); }
  return 0;
}
```

### A.11 `replay_90_93.txt` (7673 bytes, SHA-256 ce42847999a5eca0c416113b473ddc698f66b382343d70c52de70753b49ea650)

```text
row16 words per l: 0 16384 0 16384 32768 8192 32768 4096 65536 49152 65536 49152 32768 57344 32768 59392 0 16384 0 16384 32768 16384 24576 12288 65536 49152 65536 49152 32768 49152 45056 55296  total 1052672  |G| 230400
REPLAY tail successes 8062, self re-checks passed 8062, other-l co-successes 0
seed 90000 stages(log2) 16:-16.994 17:-13.007 18:-15.005 19:-6.000 20:-7.001 21:-1.000 22:-10.988 23v:-4.068 23p:-4.022 | q3 variant 2^-74.0626 published-W8 2^-74.0165 | n22 16517 v 985 p 1017 both 114
seed 90001 stages(log2) 16:-16.994 17:-12.990 18:-14.958 19:-6.000 20:-7.000 21:-1.000 22:-11.014 23v:-4.020 23p:-3.988 | q3 variant 2^-73.9767 published-W8 2^-73.9453 | n22 16221 v 1000 p 1022 both 119
seed 90002 stages(log2) 16:-16.994 17:-12.996 18:-15.066 19:-6.000 20:-7.001 21:-1.000 22:-11.021 23v:-4.044 23p:-4.127 | q3 variant 2^-74.1209 published-W8 2^-74.2044 | n22 16144 v 979 p 924 both 89
seed 90003 stages(log2) 16:-16.994 17:-12.983 18:-14.990 19:-6.000 20:-7.001 21:-1.000 22:-11.031 23v:-3.914 23p:-3.968 | q3 variant 2^-73.9129 published-W8 2^-73.9668 | n22 16035 v 1064 p 1025 both 108
seed 90004 stages(log2) 16:-16.994 17:-12.993 18:-15.015 19:-6.000 20:-7.001 21:-1.000 22:-10.995 23v:-3.973 23p:-4.000 | q3 variant 2^-73.9703 published-W8 2^-73.9967 | n22 16444 v 1047 p 1028 both 113
seed 90005 stages(log2) 16:-16.994 17:-13.004 18:-15.014 19:-6.000 20:-6.999 21:-1.000 22:-11.012 23v:-4.027 23p:-3.965 | q3 variant 2^-74.0499 published-W8 2^-73.9876 | n22 16253 v 997 p 1041 both 117
seed 90006 stages(log2) 16:-16.994 17:-13.002 18:-14.961 19:-6.000 20:-6.999 21:-1.000 22:-10.993 23v:-4.061 23p:-4.018 | q3 variant 2^-74.0114 published-W8 2^-73.9682 | n22 16460 v 986 p 1016 both 112
seed 90007 stages(log2) 16:-16.994 17:-13.001 18:-15.061 19:-6.000 20:-7.001 21:-1.000 22:-11.017 23v:-4.012 23p:-3.947 | q3 variant 2^-74.0851 published-W8 2^-74.0205 | n22 16195 v 1004 p 1050 both 104
row16 words per l: 0 16384 0 16384 32768 8192 32768 4096 65536 49152 65536 49152 32768 57344 32768 59392 0 16384 0 16384 32768 16384 24576 12288 65536 49152 65536 49152 32768 49152 45056 55296  total 1052672  |G| 230400
REPLAY tail successes 8326, self re-checks passed 8326, other-l co-successes 0
seed 91000 stages(log2) 16:-16.994 17:-13.001 18:-15.007 19:-6.000 20:-7.001 21:-1.000 22:-11.021 23v:-3.925 23p:-3.996 | q3 variant 2^-73.9486 published-W8 2^-74.0196 | n22 16142 v 1063 p 1012 both 117
seed 91001 stages(log2) 16:-16.994 17:-13.004 18:-14.967 19:-6.000 20:-6.998 21:-1.000 22:-10.987 23v:-3.993 23p:-4.028 | q3 variant 2^-73.9426 published-W8 2^-73.9778 | n22 16538 v 1039 p 1014 both 114
seed 91002 stages(log2) 16:-16.994 17:-13.004 18:-14.980 19:-6.000 20:-7.000 21:-1.000 22:-10.998 23v:-3.958 23p:-3.990 | q3 variant 2^-73.9335 published-W8 2^-73.9653 | n22 16411 v 1056 p 1033 both 112
seed 91003 stages(log2) 16:-16.994 17:-12.995 18:-15.038 19:-6.000 20:-7.001 21:-1.000 22:-10.995 23v:-4.000 23p:-3.993 | q3 variant 2^-74.0224 published-W8 2^-74.0154 | n22 16445 v 1028 p 1033 both 98
seed 91004 stages(log2) 16:-16.994 17:-12.995 18:-14.978 19:-6.000 20:-6.998 21:-1.000 22:-10.999 23v:-3.877 23p:-4.136 | q3 variant 2^-73.8412 published-W8 2^-74.0996 | n22 16399 v 1116 p 933 both 105
seed 91005 stages(log2) 16:-16.994 17:-12.999 18:-14.992 19:-6.000 20:-7.000 21:-1.000 22:-11.015 23v:-4.041 23p:-4.046 | q3 variant 2^-74.0416 published-W8 2^-74.0460 | n22 16217 v 985 p 982 both 104
seed 91006 stages(log2) 16:-16.994 17:-12.997 18:-15.057 19:-6.000 20:-6.997 21:-1.000 22:-11.004 23v:-3.994 23p:-4.038 | q3 variant 2^-74.0441 published-W8 2^-74.0884 | n22 16333 v 1025 p 994 both 101
seed 91007 stages(log2) 16:-16.994 17:-13.009 18:-14.982 19:-6.000 20:-7.000 21:-1.000 22:-11.009 23v:-4.005 23p:-4.083 | q3 variant 2^-74.0004 published-W8 2^-74.0779 | n22 16281 v 1014 p 961 both 98
row16 words per l: 0 16384 0 16384 32768 8192 32768 4096 65536 49152 65536 49152 32768 57344 32768 59392 0 16384 0 16384 32768 16384 24576 12288 65536 49152 65536 49152 32768 49152 45056 55296  total 1052672  |G| 230400
REPLAY tail successes 8217, self re-checks passed 8217, other-l co-successes 0
seed 92000 stages(log2) 16:-16.994 17:-12.995 18:-14.972 19:-6.000 20:-7.000 21:-1.000 22:-11.020 23v:-3.937 23p:-3.912 | q3 variant 2^-73.9190 published-W8 2^-73.8932 | n22 16162 v 1055 p 1074 both 116
seed 92001 stages(log2) 16:-16.994 17:-12.995 18:-15.024 19:-6.000 20:-6.998 21:-1.000 22:-11.010 23v:-3.980 23p:-3.932 | q3 variant 2^-74.0005 published-W8 2^-73.9523 | n22 16266 v 1031 p 1066 both 105
seed 92002 stages(log2) 16:-16.994 17:-13.006 18:-15.034 19:-6.000 20:-6.999 21:-1.000 22:-11.002 23v:-3.966 23p:-4.001 | q3 variant 2^-74.0021 published-W8 2^-74.0369 | n22 16360 v 1047 p 1022 both 104
seed 92003 stages(log2) 16:-16.994 17:-12.990 18:-14.990 19:-6.000 20:-6.997 21:-1.000 22:-10.986 23v:-3.931 23p:-3.958 | q3 variant 2^-73.8871 published-W8 2^-73.9140 | n22 16549 v 1085 p 1065 both 100
seed 92004 stages(log2) 16:-16.994 17:-13.001 18:-15.030 19:-6.000 20:-7.000 21:-1.000 22:-10.991 23v:-4.028 23p:-3.945 | q3 variant 2^-74.0452 published-W8 2^-73.9620 | n22 16481 v 1010 p 1070 both 124
seed 92005 stages(log2) 16:-16.994 17:-13.006 18:-14.969 19:-6.000 20:-7.001 21:-1.000 22:-10.998 23v:-3.979 23p:-3.926 | q3 variant 2^-73.9481 published-W8 2^-73.8950 | n22 16403 v 1040 p 1079 both 121
seed 92006 stages(log2) 16:-16.994 17:-12.993 18:-14.982 19:-6.000 20:-7.000 21:-1.000 22:-11.005 23v:-4.097 23p:-3.949 | q3 variant 2^-74.0713 published-W8 2^-73.9233 | n22 16324 v 954 p 1057 both 108
seed 92007 stages(log2) 16:-16.994 17:-12.998 18:-15.031 19:-6.000 20:-7.001 21:-1.000 22:-10.986 23v:-4.055 23p:-3.967 | q3 variant 2^-74.0655 published-W8 2^-73.9769 | n22 16541 v 995 p 1058 both 102
row16 words per l: 0 16384 0 16384 32768 8192 32768 4096 65536 49152 65536 49152 32768 57344 32768 59392 0 16384 0 16384 32768 16384 24576 12288 65536 49152 65536 49152 32768 49152 45056 55296  total 1052672  |G| 230400
REPLAY tail successes 8306, self re-checks passed 8306, other-l co-successes 0
seed 93000 stages(log2) 16:-16.994 17:-13.001 18:-14.971 19:-6.000 20:-7.001 21:-1.000 22:-11.007 23v:-4.044 23p:-4.041 | q3 variant 2^-74.0173 published-W8 2^-74.0143 | n22 16309 v 989 p 991 both 108
seed 93001 stages(log2) 16:-16.994 17:-12.988 18:-15.013 19:-6.000 20:-6.998 21:-1.000 22:-10.988 23v:-3.954 23p:-4.034 | q3 variant 2^-73.9354 published-W8 2^-74.0147 | n22 16524 v 1066 p 1009 both 94
seed 93002 stages(log2) 16:-16.994 17:-12.997 18:-14.966 19:-6.000 20:-6.998 21:-1.000 22:-10.989 23v:-3.980 23p:-3.979 | q3 variant 2^-73.9252 published-W8 2^-73.9239 | n22 16507 v 1046 p 1047 both 122
seed 93003 stages(log2) 16:-16.994 17:-13.003 18:-15.025 19:-6.000 20:-7.000 21:-1.000 22:-10.998 23v:-4.037 23p:-4.005 | q3 variant 2^-74.0568 published-W8 2^-74.0254 | n22 16411 v 1000 p 1022 both 115
seed 93004 stages(log2) 16:-16.994 17:-12.997 18:-15.009 19:-6.000 20:-6.999 21:-1.000 22:-10.989 23v:-3.978 23p:-3.933 | q3 variant 2^-73.9658 published-W8 2^-73.9211 | n22 16513 v 1048 p 1081 both 117
seed 93005 stages(log2) 16:-16.994 17:-12.991 18:-15.019 19:-6.000 20:-7.001 21:-1.000 22:-10.989 23v:-3.927 23p:-4.039 | q3 variant 2^-73.9224 published-W8 2^-74.0343 | n22 16504 v 1085 p 1004 both 113
seed 93006 stages(log2) 16:-16.994 17:-12.999 18:-14.961 19:-6.000 20:-7.001 21:-1.000 22:-11.004 23v:-3.943 23p:-4.046 | q3 variant 2^-73.9026 published-W8 2^-74.0053 | n22 16338 v 1062 p 989 both 109
seed 93007 stages(log2) 16:-16.994 17:-13.001 18:-14.999 19:-6.000 20:-7.000 21:-1.000 22:-11.007 23v:-4.013 23p:-4.014 | q3 variant 2^-74.0144 published-W8 2^-74.0159 | n22 16302 v 1010 p 1009 both 120
```

### A.12 `e2e_seed3.txt` (691 bytes, SHA-256 fde67fee14e8fdff88764138e9e3f3ee8c1cb9c9aec511e4f0631bd16556728f)

```text
setup: |G| 12103680, 22976 classes, K 64 with 230400 variants (2^17.814)
first blocks 8388608 (2^23.00), K 64, V_tot 230400
W7-passing (CV, class): 8510833, expected 8519680.0 (z -3.03)
good pairs: 2051007293, expected 2051712000.0 (ratio 0.9997)
row-16 passes (pair, l): 503050, expected 502690.2 (z +0.51); pairs with >=1: 498111
clumps with >=2 row-16 pairs: 51002; independent-binomial expectation 13966.2
within-first-block pairwise correlation of row-16 success (any l): rho = 1.001 (sum R(R-1) 1436276, p^2 sum G(G-1) 1435367.8)
exact pair checks: 16000, failures 0
good pairs per CV: mean 244.50, var 2841516.3; hist 0:8024814 <128:8766 <256:10104 <512:18559 <1024:30960 more:295405
```

### A.13 `e2e_seed1.txt` (682 bytes, SHA-256 66021a29f1010103e33d614cc3d50ec3e1d13a97706c0cfb5ba94a198d6644e6)

```text
setup: |G| 12103680, 22976 classes, K 64 with 230400 variants (2^17.814)
first blocks 2097152 (2^21.00), K 64, V_tot 230400
W7-passing (CV, class): 2134874, expected 2129920.0 (z +3.39)
good pairs: 516134885, expected 512928000.0 (ratio 1.0063)
row-16 passes (pair, l): 126066, expected 126501.7 (z -1.23); pairs with >=1: 124808
clumps with >=2 row-16 pairs: 12801; independent-binomial expectation 3495.7
within-first-block pairwise correlation of row-16 success (any l): rho = 1.001 (sum R(R-1) 361072, p^2 sum G(G-1) 360532.2)
exact pair checks: 16000, failures 0
good pairs per CV: mean 246.11, var 2879731.7; hist 0:2005973 <128:2276 <256:2493 <512:4683 <1024:7849 more:73878
```

### A.14 `PREREG_q3b.txt` (1183 bytes, SHA-256 3323fb5809e29cb5e95561c55eabb7d98380cbf4494e735fe7d6a16a2f9a1cd1)

```text
q3 SMC preregistration, second study (the 222-class family), A0-variant attack, sha256-r37, frozen 2026-10-09T17:45:34Z before any listed seed ran.
program: smc.c sha256 7ac6f21b9aaaba983ddca27df63150aac2cac267a54729309c53ba9181c2ab98  lab.h sha256 5e0e96055fe2042b825e08345e4a2343dca8d7e84bd947312b7856799f27bedf
build: cc -O3 -march=native -o smc smc.c -lm -lpthread
W8 drawn uniformly from the 782,800 variants of the 222 selected classes (default; SMC_ALLG unset).
parameters: NP=2048 M=512 MT=16384, 8 replicates per invocation (the parameters of PREREG_q3.txt).
invocations: ./smc 80 2048 512 16384 8 ; ./smc 81 ... ; ./smc 82 ... ; ./smc 83 ...  -> replicate seeds 80000..80007, 81000..81007, 82000..82007, 83000..83007 (32 replicates).
estimate per replicate: product of stage means (16 exact, 17..21, 22, 23..36 with the variant W8) = 'q3 variant'.
rule: Z_s linear estimates (32); LB = mean - t*sd/sqrt(32), t = 2.4528 (one-sided 99%, 31 df); q3_model = LB at face value (H6) rounded down to 4 decimals of log2 (this study replaces the 64-class study as the basis of the claim; the 64-class record stays in Appendix A).
All 32 replicates are reported; none may be dropped.
```

### A.15 `smc_80.txt` (1838 bytes, SHA-256 0b844971ef1fb4a399b9f898e2750a63fd7d3caea8f2acce8a02a1ab05543a09)

```text
row16 words per l: 0 16384 0 16384 32768 8192 32768 4096 65536 49152 65536 49152 32768 57344 32768 59392 0 16384 0 16384 32768 16384 24576 12288 65536 49152 65536 49152 32768 49152 45056 55296  total 1052672  |G| 782800
seed 80000 stages(log2) 16:-16.994 17:-12.994 18:-15.011 19:-6.000 20:-6.997 21:-1.000 22:-10.978 23v:-4.062 23p:-4.026 | q3 variant 2^-74.0368 published-W8 2^-74.0011 | n22 16637 v 996 p 1021 both 92
seed 80001 stages(log2) 16:-16.994 17:-12.996 18:-14.986 19:-6.000 20:-6.999 21:-1.000 22:-10.994 23v:-3.981 23p:-4.000 | q3 variant 2^-73.9495 published-W8 2^-73.9690 | n22 16450 v 1042 p 1028 both 123
seed 80002 stages(log2) 16:-16.994 17:-13.003 18:-15.051 19:-6.000 20:-7.000 21:-1.000 22:-11.005 23v:-4.022 23p:-4.064 | q3 variant 2^-74.0753 published-W8 2^-74.1175 | n22 16322 v 1005 p 976 both 100
seed 80003 stages(log2) 16:-16.994 17:-13.000 18:-14.982 19:-6.000 20:-6.998 21:-1.000 22:-10.982 23v:-3.985 23p:-4.046 | q3 variant 2^-73.9413 published-W8 2^-74.0032 | n22 16590 v 1048 p 1004 both 124
seed 80004 stages(log2) 16:-16.994 17:-12.998 18:-14.980 19:-6.000 20:-6.998 21:-1.000 22:-11.006 23v:-4.067 23p:-3.975 | q3 variant 2^-74.0428 published-W8 2^-73.9510 | n22 16320 v 974 p 1038 both 113
seed 80005 stages(log2) 16:-16.994 17:-12.997 18:-14.991 19:-6.000 20:-6.999 21:-1.000 22:-11.013 23v:-3.989 23p:-4.024 | q3 variant 2^-73.9847 published-W8 2^-74.0190 | n22 16232 v 1022 p 998 both 107
seed 80006 stages(log2) 16:-16.994 17:-12.993 18:-15.012 19:-6.000 20:-6.999 21:-1.000 22:-11.011 23v:-3.944 23p:-3.906 | q3 variant 2^-73.9531 published-W8 2^-73.9154 | n22 16265 v 1057 p 1085 both 130
seed 80007 stages(log2) 16:-16.994 17:-12.987 18:-14.948 19:-6.000 20:-7.000 21:-1.000 22:-11.028 23v:-3.960 23p:-4.023 | q3 variant 2^-73.9174 published-W8 2^-73.9802 | n22 16066 v 1032 p 988 both 108
```

### A.16 `smc_81.txt` (1836 bytes, SHA-256 1cdb839312390eb235713463e079ddbb8ae98e401ef298584c05d254e9387f29)

```text
row16 words per l: 0 16384 0 16384 32768 8192 32768 4096 65536 49152 65536 49152 32768 57344 32768 59392 0 16384 0 16384 32768 16384 24576 12288 65536 49152 65536 49152 32768 49152 45056 55296  total 1052672  |G| 782800
seed 81000 stages(log2) 16:-16.994 17:-13.006 18:-15.007 19:-6.000 20:-6.999 21:-1.000 22:-11.023 23v:-4.080 23p:-3.958 | q3 variant 2^-74.1078 published-W8 2^-73.9861 | n22 16129 v 954 p 1038 both 117
seed 81001 stages(log2) 16:-16.994 17:-13.001 18:-15.022 19:-6.000 20:-7.001 21:-1.000 22:-10.986 23v:-4.037 23p:-3.982 | q3 variant 2^-74.0418 published-W8 2^-73.9870 | n22 16544 v 1008 p 1047 both 125
seed 81002 stages(log2) 16:-16.994 17:-13.000 18:-14.989 19:-6.000 20:-7.002 21:-1.000 22:-10.986 23v:-3.999 23p:-3.986 | q3 variant 2^-73.9698 published-W8 2^-73.9573 | n22 16545 v 1035 p 1044 both 122
seed 81003 stages(log2) 16:-16.994 17:-13.009 18:-15.041 19:-6.000 20:-6.999 21:-1.000 22:-11.011 23v:-4.026 23p:-3.987 | q3 variant 2^-74.0807 published-W8 2^-74.0422 | n22 16258 v 998 p 1025 both 97
seed 81004 stages(log2) 16:-16.994 17:-13.003 18:-15.018 19:-6.000 20:-7.002 21:-1.000 22:-10.992 23v:-4.001 23p:-3.946 | q3 variant 2^-74.0101 published-W8 2^-73.9551 | n22 16470 v 1029 p 1069 both 129
seed 81005 stages(log2) 16:-16.994 17:-12.994 18:-15.015 19:-6.000 20:-6.998 21:-1.000 22:-11.006 23v:-4.070 23p:-4.063 | q3 variant 2^-74.0770 published-W8 2^-74.0696 | n22 16314 v 971 p 976 both 91
seed 81006 stages(log2) 16:-16.994 17:-13.011 18:-15.011 19:-6.000 20:-7.001 21:-1.000 22:-10.999 23v:-4.016 23p:-4.068 | q3 variant 2^-74.0335 published-W8 2^-74.0857 | n22 16391 v 1013 p 977 both 101
seed 81007 stages(log2) 16:-16.994 17:-12.996 18:-14.961 19:-6.000 20:-7.000 21:-1.000 22:-11.016 23v:-3.991 23p:-3.960 | q3 variant 2^-73.9578 published-W8 2^-73.9269 | n22 16200 v 1019 p 1041 both 94
```

### A.17 `smc_82.txt` (1839 bytes, SHA-256 46f0e8e3dbc8eb5d584a4fee6df69531390811509d98f40a872b2341c9296d6d)

```text
row16 words per l: 0 16384 0 16384 32768 8192 32768 4096 65536 49152 65536 49152 32768 57344 32768 59392 0 16384 0 16384 32768 16384 24576 12288 65536 49152 65536 49152 32768 49152 45056 55296  total 1052672  |G| 782800
seed 82000 stages(log2) 16:-16.994 17:-13.003 18:-15.042 19:-6.000 20:-6.999 21:-1.000 22:-11.009 23v:-4.077 23p:-4.036 | q3 variant 2^-74.1239 published-W8 2^-74.0826 | n22 16287 v 965 p 993 both 105
seed 82001 stages(log2) 16:-16.994 17:-13.002 18:-15.026 19:-6.000 20:-7.003 21:-1.000 22:-11.000 23v:-3.930 23p:-3.866 | q3 variant 2^-73.9548 published-W8 2^-73.8905 | n22 16386 v 1075 p 1124 both 121
seed 82002 stages(log2) 16:-16.994 17:-12.995 18:-15.042 19:-6.000 20:-6.999 21:-1.000 22:-10.997 23v:-3.981 23p:-3.951 | q3 variant 2^-74.0073 published-W8 2^-73.9771 | n22 16419 v 1040 p 1062 both 121
seed 82003 stages(log2) 16:-16.994 17:-12.997 18:-14.989 19:-6.000 20:-6.998 21:-1.000 22:-10.987 23v:-4.017 23p:-4.053 | q3 variant 2^-73.9825 published-W8 2^-74.0182 | n22 16529 v 1021 p 996 both 104
seed 82004 stages(log2) 16:-16.994 17:-13.008 18:-15.026 19:-6.000 20:-7.001 21:-1.000 22:-10.999 23v:-4.079 23p:-3.913 | q3 variant 2^-74.1068 published-W8 2^-73.9398 | n22 16399 v 970 p 1089 both 123
seed 82005 stages(log2) 16:-16.994 17:-12.993 18:-14.997 19:-6.000 20:-6.997 21:-1.000 22:-10.986 23v:-3.930 23p:-4.107 | q3 variant 2^-73.8967 published-W8 2^-74.0733 | n22 16540 v 1085 p 960 both 100
seed 82006 stages(log2) 16:-16.994 17:-13.003 18:-14.953 19:-6.000 20:-7.000 21:-1.000 22:-10.985 23v:-4.008 23p:-3.991 | q3 variant 2^-73.9442 published-W8 2^-73.9275 | n22 16550 v 1029 p 1041 both 125
seed 82007 stages(log2) 16:-16.994 17:-12.998 18:-14.955 19:-6.000 20:-7.000 21:-1.000 22:-10.990 23v:-3.970 23p:-4.017 | q3 variant 2^-73.9068 published-W8 2^-73.9541 | n22 16500 v 1053 p 1019 both 121
```

### A.18 `smc_83.txt` (1842 bytes, SHA-256 05ac94179ce998b7c861d39b3db13d70c217e4146df7b4725856c00905ef4791)

```text
row16 words per l: 0 16384 0 16384 32768 8192 32768 4096 65536 49152 65536 49152 32768 57344 32768 59392 0 16384 0 16384 32768 16384 24576 12288 65536 49152 65536 49152 32768 49152 45056 55296  total 1052672  |G| 782800
seed 83000 stages(log2) 16:-16.994 17:-13.000 18:-15.016 19:-6.000 20:-7.000 21:-1.000 22:-11.017 23v:-3.965 23p:-3.986 | q3 variant 2^-73.9921 published-W8 2^-74.0132 | n22 16190 v 1037 p 1022 both 121
seed 83001 stages(log2) 16:-16.994 17:-13.002 18:-15.051 19:-6.000 20:-6.999 21:-1.000 22:-11.008 23v:-3.952 23p:-3.952 | q3 variant 2^-74.0057 published-W8 2^-74.0057 | n22 16295 v 1053 p 1053 both 117
seed 83002 stages(log2) 16:-16.994 17:-12.994 18:-14.973 19:-6.000 20:-7.000 21:-1.000 22:-10.995 23v:-4.000 23p:-3.893 | q3 variant 2^-73.9549 published-W8 2^-73.8481 | n22 16445 v 1028 p 1107 both 115
seed 83003 stages(log2) 16:-16.994 17:-13.001 18:-15.019 19:-6.000 20:-6.999 21:-1.000 22:-10.999 23v:-3.945 23p:-4.028 | q3 variant 2^-73.9583 published-W8 2^-74.0406 | n22 16390 v 1064 p 1005 both 105
seed 83004 stages(log2) 16:-16.994 17:-13.003 18:-15.011 19:-6.000 20:-6.999 21:-1.000 22:-10.996 23v:-4.058 23p:-4.032 | q3 variant 2^-74.0621 published-W8 2^-74.0360 | n22 16427 v 986 p 1004 both 99
seed 83005 stages(log2) 16:-16.994 17:-12.991 18:-14.966 19:-6.000 20:-7.002 21:-1.000 22:-10.981 23v:-4.001 23p:-4.036 | q3 variant 2^-73.9356 published-W8 2^-73.9708 | n22 16605 v 1037 p 1012 both 115
seed 83006 stages(log2) 16:-16.994 17:-12.995 18:-15.025 19:-6.000 20:-7.000 21:-1.000 22:-10.993 23v:-3.937 23p:-3.995 | q3 variant 2^-73.9446 published-W8 2^-74.0021 | n22 16468 v 1075 p 1033 both 121
seed 83007 stages(log2) 16:-16.994 17:-13.006 18:-15.040 19:-6.000 20:-6.999 21:-1.000 22:-10.992 23v:-3.991 23p:-4.038 | q3 variant 2^-74.0219 published-W8 2^-74.0686 | n22 16477 v 1036 p 1003 both 111
```

### A.19 `e2e_seed21.txt` (673 bytes, SHA-256 99a0466a5856684dad67334b22c13df0cafbad3bdd92611bfa6165f4671f3a05)

```text
setup: |G| 12103680, 22976 classes, K 222 with 782800 variants (2^19.578)
first blocks 196608 (2^17.58), K 222, V_tot 782800
W7-passing (CV, class): 696209, expected 692640.0 (z +4.29)
good pairs: 163607020, expected 163378921.9 (ratio 1.0014)
row-16 passes (pair, l): 40079, expected 40099.1 (z -0.10); pairs with >=1: 39660
clumps with >=2 row-16 pairs: 4091; independent-binomial expectation 1083.3
within-first-block pairwise correlation of row-16 success (any l): rho = 1.003 (sum R(R-1) 232338, p^2 sum G(G-1) 231693.5)
exact pair checks: 24000, failures 0
good pairs per CV: mean 832.15, var 19362830.3; hist 0:181745 <128:228 <256:235 <512:521 <1024:812 more:13067
```

### A.20 `e2e_seed22.txt` (701 bytes, SHA-256 516c69a977db07f484e6b86d7199166c58c204e7360435b0bf2f3d63956b41e6)

```text
setup: |G| 12103680, 22976 classes, K 222 with 782800 variants (2^19.578)
first blocks 8388608 (2^23.00), K 222, V_tot 782800
W7-passing (CV, class): 29623852, expected 29552640.0 (z +13.10)
good pairs: 6997476590, expected 6970834000.0 (ratio 1.0038)
row-16 passes (pair, l): 1712536, expected 1715041.6 (z -1.91); pairs with >=1: 1695467
clumps with >=2 row-16 pairs: 170711; independent-binomial expectation 46523.4
within-first-block pairwise correlation of row-16 success (any l): rho = 0.999 (sum R(R-1) 9807146, p^2 sum G(G-1) 9817977.6)
exact pair checks: 32000, failures 0
good pairs per CV: mean 834.16, var 19240927.9; hist 0:7756589 <128:9256 <256:10876 <512:20382 <1024:34775 more:556730
```

### A.21 `replay_94_97.txt` (7677 bytes, SHA-256 665ca2c8fd30ae5e818f4a863caa86159a286dcca4c7f97f3b68907f952cbb77)

```text
row16 words per l: 0 16384 0 16384 32768 8192 32768 4096 65536 49152 65536 49152 32768 57344 32768 59392 0 16384 0 16384 32768 16384 24576 12288 65536 49152 65536 49152 32768 49152 45056 55296  total 1052672  |G| 782800
REPLAY tail successes 8390, self re-checks passed 8390, other-l co-successes 0
seed 94000 stages(log2) 16:-16.994 17:-12.996 18:-14.967 19:-6.000 20:-7.000 21:-1.000 22:-10.992 23v:-3.962 23p:-4.037 | q3 variant 2^-73.9116 published-W8 2^-73.9872 | n22 16470 v 1057 p 1003 both 108
seed 94001 stages(log2) 16:-16.994 17:-13.007 18:-14.979 19:-6.000 20:-7.001 21:-1.000 22:-10.989 23v:-3.945 23p:-4.089 | q3 variant 2^-73.9152 published-W8 2^-74.0594 | n22 16506 v 1072 p 970 both 102
seed 94002 stages(log2) 16:-16.994 17:-13.007 18:-14.992 19:-6.000 20:-7.001 21:-1.000 22:-10.998 23v:-3.977 23p:-3.974 | q3 variant 2^-73.9686 published-W8 2^-73.9658 | n22 16411 v 1042 p 1044 both 99
seed 94003 stages(log2) 16:-16.994 17:-13.000 18:-15.032 19:-6.000 20:-6.999 21:-1.000 22:-10.998 23v:-3.935 23p:-3.974 | q3 variant 2^-73.9589 published-W8 2^-73.9971 | n22 16402 v 1072 p 1044 both 136
seed 94004 stages(log2) 16:-16.994 17:-12.998 18:-15.017 19:-6.000 20:-6.998 21:-1.000 22:-10.997 23v:-4.020 23p:-3.949 | q3 variant 2^-74.0236 published-W8 2^-73.9527 | n22 16422 v 1012 p 1063 both 108
seed 94005 stages(log2) 16:-16.994 17:-13.002 18:-15.004 19:-6.000 20:-7.003 21:-1.000 22:-10.982 23v:-3.989 23p:-4.092 | q3 variant 2^-73.9747 published-W8 2^-74.0777 | n22 16591 v 1045 p 973 both 106
seed 94006 stages(log2) 16:-16.994 17:-13.003 18:-14.987 19:-6.000 20:-7.001 21:-1.000 22:-11.002 23v:-3.983 23p:-4.015 | q3 variant 2^-73.9694 published-W8 2^-74.0019 | n22 16366 v 1035 p 1012 both 124
seed 94007 stages(log2) 16:-16.994 17:-12.995 18:-14.980 19:-6.000 20:-7.002 21:-1.000 22:-11.004 23v:-3.953 23p:-3.946 | q3 variant 2^-73.9284 published-W8 2^-73.9216 | n22 16341 v 1055 p 1060 both 122
row16 words per l: 0 16384 0 16384 32768 8192 32768 4096 65536 49152 65536 49152 32768 57344 32768 59392 0 16384 0 16384 32768 16384 24576 12288 65536 49152 65536 49152 32768 49152 45056 55296  total 1052672  |G| 782800
REPLAY tail successes 8319, self re-checks passed 8319, other-l co-successes 0
seed 95000 stages(log2) 16:-16.994 17:-12.991 18:-14.980 19:-6.000 20:-6.999 21:-1.000 22:-11.011 23v:-3.950 23p:-3.985 | q3 variant 2^-73.9257 published-W8 2^-73.9604 | n22 16260 v 1052 p 1027 both 121
seed 95001 stages(log2) 16:-16.994 17:-12.999 18:-15.025 19:-6.000 20:-7.000 21:-1.000 22:-11.008 23v:-4.057 23p:-3.981 | q3 variant 2^-74.0837 published-W8 2^-74.0077 | n22 16292 v 979 p 1032 both 106
seed 95002 stages(log2) 16:-16.994 17:-13.000 18:-15.024 19:-6.000 20:-7.000 21:-1.000 22:-10.993 23v:-3.930 23p:-3.965 | q3 variant 2^-73.9414 published-W8 2^-73.9766 | n22 16458 v 1080 p 1054 both 131
seed 95003 stages(log2) 16:-16.994 17:-13.006 18:-14.956 19:-6.000 20:-6.999 21:-1.000 22:-10.990 23v:-4.013 23p:-4.067 | q3 variant 2^-73.9581 published-W8 2^-74.0128 | n22 16496 v 1022 p 984 both 124
seed 95004 stages(log2) 16:-16.994 17:-13.002 18:-14.997 19:-6.000 20:-7.003 21:-1.000 22:-11.004 23v:-4.022 23p:-3.923 | q3 variant 2^-74.0216 published-W8 2^-73.9232 | n22 16341 v 1006 p 1077 both 125
seed 95005 stages(log2) 16:-16.994 17:-12.998 18:-15.032 19:-6.000 20:-7.001 21:-1.000 22:-11.007 23v:-3.942 23p:-3.951 | q3 variant 2^-73.9733 published-W8 2^-73.9829 | n22 16304 v 1061 p 1054 both 123
seed 95006 stages(log2) 16:-16.994 17:-12.994 18:-15.021 19:-6.000 20:-6.999 21:-1.000 22:-11.006 23v:-3.929 23p:-4.040 | q3 variant 2^-73.9438 published-W8 2^-74.0544 | n22 16318 v 1071 p 992 both 122
seed 95007 stages(log2) 16:-16.994 17:-12.999 18:-14.991 19:-6.000 20:-7.001 21:-1.000 22:-10.994 23v:-3.973 23p:-3.992 | q3 variant 2^-73.9518 published-W8 2^-73.9712 | n22 16452 v 1048 p 1034 both 114
row16 words per l: 0 16384 0 16384 32768 8192 32768 4096 65536 49152 65536 49152 32768 57344 32768 59392 0 16384 0 16384 32768 16384 24576 12288 65536 49152 65536 49152 32768 49152 45056 55296  total 1052672  |G| 782800
REPLAY tail successes 8184, self re-checks passed 8184, other-l co-successes 0
seed 96000 stages(log2) 16:-16.994 17:-12.994 18:-15.044 19:-6.000 20:-7.000 21:-1.000 22:-10.987 23v:-4.001 23p:-4.001 | q3 variant 2^-74.0206 published-W8 2^-74.0206 | n22 16537 v 1033 p 1033 both 117
seed 96001 stages(log2) 16:-16.994 17:-13.006 18:-14.959 19:-6.000 20:-7.002 21:-1.000 22:-10.979 23v:-3.996 23p:-3.922 | q3 variant 2^-73.9360 published-W8 2^-73.8618 | n22 16626 v 1042 p 1097 both 122
seed 96002 stages(log2) 16:-16.994 17:-12.998 18:-14.969 19:-6.000 20:-6.999 21:-1.000 22:-10.986 23v:-3.962 23p:-4.057 | q3 variant 2^-73.9075 published-W8 2^-74.0030 | n22 16547 v 1062 p 994 both 126
seed 96003 stages(log2) 16:-16.994 17:-13.004 18:-14.990 19:-6.000 20:-7.002 21:-1.000 22:-11.006 23v:-4.005 23p:-4.022 | q3 variant 2^-74.0014 published-W8 2^-74.0186 | n22 16315 v 1016 p 1004 both 112
seed 96004 stages(log2) 16:-16.994 17:-12.999 18:-14.991 19:-6.000 20:-7.000 21:-1.000 22:-10.987 23v:-3.991 23p:-3.969 | q3 variant 2^-73.9623 published-W8 2^-73.9402 | n22 16532 v 1040 p 1056 both 115
seed 96005 stages(log2) 16:-16.994 17:-13.005 18:-15.019 19:-6.000 20:-7.000 21:-1.000 22:-11.029 23v:-3.998 23p:-4.016 | q3 variant 2^-74.0456 published-W8 2^-74.0629 | n22 16060 v 1005 p 993 both 134
seed 96006 stages(log2) 16:-16.994 17:-12.993 18:-14.972 19:-6.000 20:-7.000 21:-1.000 22:-11.004 23v:-4.058 23p:-4.003 | q3 variant 2^-74.0212 published-W8 2^-73.9664 | n22 16339 v 981 p 1019 both 103
seed 96007 stages(log2) 16:-16.994 17:-13.001 18:-15.049 19:-6.000 20:-7.002 21:-1.000 22:-11.004 23v:-4.023 23p:-4.018 | q3 variant 2^-74.0737 published-W8 2^-74.0694 | n22 16334 v 1005 p 1008 both 112
row16 words per l: 0 16384 0 16384 32768 8192 32768 4096 65536 49152 65536 49152 32768 57344 32768 59392 0 16384 0 16384 32768 16384 24576 12288 65536 49152 65536 49152 32768 49152 45056 55296  total 1052672  |G| 782800
REPLAY tail successes 8257, self re-checks passed 8257, other-l co-successes 0
seed 97000 stages(log2) 16:-16.994 17:-12.996 18:-14.978 19:-6.000 20:-7.000 21:-1.000 22:-11.011 23v:-4.086 23p:-4.039 | q3 variant 2^-74.0650 published-W8 2^-74.0176 | n22 16254 v 957 p 989 both 121
seed 97001 stages(log2) 16:-16.994 17:-12.999 18:-14.976 19:-6.000 20:-7.001 21:-1.000 22:-11.000 23v:-3.953 23p:-4.080 | q3 variant 2^-73.9235 published-W8 2^-74.0502 | n22 16384 v 1058 p 969 both 123
seed 97002 stages(log2) 16:-16.994 17:-12.994 18:-14.998 19:-6.000 20:-7.000 21:-1.000 22:-11.007 23v:-3.925 23p:-4.036 | q3 variant 2^-73.9188 published-W8 2^-74.0291 | n22 16301 v 1073 p 994 both 123
seed 97003 stages(log2) 16:-16.994 17:-13.001 18:-15.003 19:-6.000 20:-7.001 21:-1.000 22:-11.001 23v:-4.019 23p:-4.015 | q3 variant 2^-74.0189 published-W8 2^-74.0147 | n22 16372 v 1010 p 1013 both 98
seed 97004 stages(log2) 16:-16.994 17:-12.993 18:-15.035 19:-6.000 20:-6.999 21:-1.000 22:-10.990 23v:-3.983 23p:-4.025 | q3 variant 2^-73.9948 published-W8 2^-74.0369 | n22 16495 v 1043 p 1013 both 114
seed 97005 stages(log2) 16:-16.994 17:-12.994 18:-15.019 19:-6.000 20:-7.001 21:-1.000 22:-10.991 23v:-3.956 23p:-4.092 | q3 variant 2^-73.9554 published-W8 2^-74.0906 | n22 16487 v 1062 p 967 both 115
seed 97006 stages(log2) 16:-16.994 17:-12.995 18:-14.971 19:-6.000 20:-7.000 21:-1.000 22:-11.008 23v:-3.967 23p:-4.008 | q3 variant 2^-73.9356 published-W8 2^-73.9763 | n22 16293 v 1042 p 1013 both 123
seed 97007 stages(log2) 16:-16.994 17:-13.006 18:-15.006 19:-6.000 20:-7.000 21:-1.000 22:-11.005 23v:-4.012 23p:-3.958 | q3 variant 2^-74.0246 published-W8 2^-73.9714 | n22 16323 v 1012 p 1050 both 119
```

### A.22 `w7var.c` (1454 bytes, SHA-256 30e0e83866c40dd6603fcd854afd721e51c2de3265dc9e1b0fa80a63b02e8edc)

```c
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
typedef uint32_t u32; typedef uint64_t u64;
static inline u32 ror(u32 x,int n){return (x>>n)|(x<<(32-n));}
static inline u32 s0(u32 x){return ror(x,7)^ror(x,18)^(x>>3);}
static u64 *bm;
static u64 st[4]={0x9e3779b97f4a7c15ULL,0xbf58476d1ce4e5b9ULL,0x94d049bb133111ebULL,0x2545f4914f6cdd1dULL};
static inline u64 rotl(u64 x,int k){return (x<<k)|(x>>(64-k));}
static u64 nxt(){u64 r=rotl(st[1]*5,7)*9,t=st[1]<<17;st[2]^=st[0];st[3]^=st[1];st[1]^=st[2];st[0]^=st[3];st[2]^=t;st[3]=rotl(st[3],45);return r;}
int main(int argc,char**argv){
  long N=atol(argv[1]); u32 c7[222]; FILE*f=fopen("top222.txt","r"); char l[100]; int k=0;
  while(k<222&&fgets(l,100,f)){unsigned a; sscanf(l,"%x",&a); c7[k++]=a;} fclose(f);
  bm=calloc(1u<<26,8);
  for(u64 w=0;w<(1ull<<32);w++){u32 x=(u32)w; if(((s0(x+0xfbc00800u)-s0(x))&0xffffffffu)==0x017f8000u) bm[w>>6]|=1ull<<(w&63);}
  double s=0,ss=0; u64 tot=0; long hist[32]={0};
  for(long i=0;i<N;i++){u32 a=(u32)nxt(); int n=0; for(int c=0;c<222;c++){u32 w=c7[c]-a; n+=(bm[w>>6]>>(w&63))&1;} s+=n; ss+=(double)n*n; hist[n>31?31:n]++;}
  double m=s/N, v=ss/N-m*m; printf("N %ld mean %.5f (expected %.5f) var %.3f var/mean %.2f sd of mean %.5f z %+.2f\n",N,m,222*68157440.0/4294967296.0,v,v/m,sqrt(v/N),(m-222*68157440.0/4294967296.0)/sqrt(v/N));
  for(int i=0;i<12;i++) printf("%d:%ld ",i,hist[i]); printf("\n"); return 0;}
```

### A.23 `run_exp_org.py` (3750 bytes, SHA-256 ab80b71ba96669eeade52604e601229d4915906215c79330b611f4ecea4b8e35)

```python
#!/usr/bin/env python3
# run_exp_org.py - local emulation of the organizer requests of this package's experiments with the public seed protocol of
# experiments/runner.py (seed 'hashsmash-public-seed-v1', no holdout nonce, 256 trials): builds the request exactly as
# _python_result does, runs a0core.py twice (python3 -B -s), compares the stdout bytes, recomputes the target digest of every
# returned message pair with the repository verifier, and summarizes.   usage: REPO_ROOT=... run_exp_org.py OUT.json
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
           program_sha256=hashlib.sha256(open('a0core.py', 'rb').read()).hexdigest())
for eid in ('a0-sfs-r37', 'a0-online-r37'):
    req = {"schema_version": 1, "experiment_id": eid, "target_profile": tr.profile_id, "event": {"kind": "full-collision"},
           "max_message_bytes": 4096, "trials": [{"trial": i, "seed": hashlib.sha256(sm + canon([eid, i])).hexdigest()} for i in range(256)]}
    rq = canon(req) + b"\n"; t0 = time.time()
    o1 = subprocess.run([sys.executable, '-B', '-s', 'a0core.py'], input=rq, capture_output=True, check=True).stdout; dt = time.time() - t0
    o2 = subprocess.run([sys.executable, '-B', '-s', 'a0core.py'], input=rq, capture_output=True, check=True).stdout
    out = json.loads(o1); rows = out['trials']; ret = [r for r in rows if r['message_a_hex'] is not None]
    full = sum(1 for r in ret if r['message_a_hex'] != r['message_b_hex'] and
               digest(bytes.fromhex(r['message_a_hex']), 'sha256', R) == digest(bytes.fromhex(r['message_b_hex']), 'sha256', R))
    pairs = [hashlib.sha256(canon(sorted([r['message_a_hex'], r['message_b_hex']]))).hexdigest() for r in ret]
    s = dict(sec=round(dt, 2), byte_identical=o1 == o2, request_sha256=hashlib.sha256(rq).hexdigest(),
             stdout_sha256=hashlib.sha256(o1).hexdigest(), stdout_bytes=len(o1), returned=len(ret), full_collisions=full,
             repeated=len(pairs) - len(set(pairs)), max_obs=max(len(r.get('observations', {})) for r in rows))
    if eid == 'a0-sfs-r37':
        sfs = 0
        for r in ret:
            a, b = bytes.fromhex(r['message_a_hex']), bytes.fromhex(r['message_b_hex'])
            cv = tuple(int.from_bytes(a[4 * i:4 * i + 4], 'big') for i in range(8))
            if a[:32] == b[:32] and a[32:] != b[32:] and hf._compress('sha256', cv, a[32:], R) == hf._compress('sha256', cv, b[32:], R): sfs += 1
        s['sfs_collisions_repo_verifier'] = sfs
        s['checks_passed'] = sum(r['observations']['checks_passed'] for r in rows if 'observations' in r)
    else:
        obs = [r['observations'] for r in rows if 'observations' in r]
        for key in ('first_blocks', 'w7_classes', 'classes_processed', 'good_pairs', 'row16_pairs', 'counted_ops', 'lane_mismatches',
                    'filter_mismatches', 'cell_mismatches', 'pairs_cell_checked'):
            s[key] = sum(o[key] for o in obs)
        s['trials_with_pairs'] = len(ret); s['good_pairs_per_trial'] = [o['good_pairs'] for o in obs]
    res[eid] = s
open(sys.argv[1], 'w').write(json.dumps(res, indent=1)); print(json.dumps(res, indent=1))
```

### A.24 `org_a0.json` (1362 bytes, SHA-256 f88a297d91cbaafe07bc46e2879d20893706a69c2eed605166363c2671551cae)

```json
{
 "track": "sha256-r37-exploratory",
 "profile": "sha256-r37-prefix-v1",
 "target_config_sha256": "3e8cc3387122592a1349a1b4937bf8843ee23f3c71cb0d4e7b3aec515b0e4189",
 "python": "3.14.0",
 "program_sha256": "1962b040026014ec04bcee4c24d9f5db4cfdc571f5ed0904a7d19b6fa0cd62dd",
 "a0-sfs-r37": {
  "sec": 0.54,
  "byte_identical": true,
  "request_sha256": "18b3dba0780dc421eed2259e341096308b2eb28767d91aaf6127617ea5d1c523",
  "stdout_sha256": "53f34c5948a10e3a2edd00814338795a89673d59dff31d0d5bc4e31a36a110e3",
  "stdout_bytes": 22504,
  "returned": 16,
  "full_collisions": 0,
  "repeated": 0,
  "max_obs": 7,
  "sfs_collisions_repo_verifier": 16,
  "checks_passed": 16
 },
 "a0-online-r37": {
  "sec": 1.18,
  "byte_identical": true,
  "request_sha256": "848e9d74333e064bd34ba95be619cdd40555283fbc38fe09844c88d61149163d",
  "stdout_sha256": "c78124a5eb61e1b8ae4be6e59b9a45311913ffa89cab47728d87677debfa8838",
  "stdout_bytes": 16946,
  "returned": 2,
  "full_collisions": 0,
  "repeated": 0,
  "max_obs": 10,
  "first_blocks": 79,
  "w7_classes": 137,
  "classes_processed": 16,
  "good_pairs": 2768,
  "row16_pairs": 1,
  "counted_ops": 206266,
  "lane_mismatches": 0,
  "filter_mismatches": 0,
  "cell_mismatches": 0,
  "pairs_cell_checked": 24,
  "trials_with_pairs": 2,
  "good_pairs_per_trial": [
   1808,
   0,
   0,
   960,
   0,
   0,
   0,
   0
  ]
 }
}
```

### A.25 `stress.py` (1093 bytes, SHA-256 d73e0e324b211af3ccd6e093a69177cb1786d8cb473cc35218424e0b9710d201)

```python
import sys, time; sys.path.insert(0, '.')
import a0core as a
from a0core import *
Lt = setup_l(); R16 = make_R16(Lt); CD = {}
bad = [0, 0, 0, 0]; cnt = dict(lanes=0, u=0, good=0)
def check(kind, cv, a0, cd, bt=None, fail=None, nl=None, u=None):
    if kind == 'u':
        wx = words_from_cv(cv, a0)[0]
        cnt['u'] += 1
        if u != (wx[0] + s0(wx[1])) & M32: bad[1] += 1
    elif kind == 'good':
        cnt['good'] += 1; wx, wy = words_from_cv(cv, a0)
        if not (inF(wx[7], D7, T7) and inF(wx[6], D6, T6)): bad[3] += 1
    else:
        cnt['lanes'] += nl
        for L in range(nl):
            a0_ = cd.members[256 * bt + L]
            w6 = (C6 - cv[1] + MAJ(A1, a0_, cv[0]) - CH(E5, (a0_ + C4) & M32, (k3of(a0_) + cv[0]) & M32)) & M32
            if ((fail >> L) & 1) == inF(w6, D6, T6): bad[0] += 1
rng = Shake(sys.argv[1]); n = int(sys.argv[2])
stats = dict(fb=0, hits=0, good=0, r16=0)
t = time.time(); ops, found = online(n, rng, CD, Lt, R16, stats, check, None)
print(stats, 'ops/fb %.0f' % (ops / n), 'bad', bad, cnt, 'found', len(found), '%.1fs' % (time.time() - t))
```

### A.26 `stress_final.txt` (355 bytes, SHA-256 778ef697fd276d2d9e00989c4300f1814128bc5bc2606851d7e9747fca97ac31)

```text
{'fb': 100, 'hits': 300, 'good': 80588, 'r16': 21, 'm0': [863391965, 1561714937, 4227982174, 3884942433, 3834236777, 1590519364, 68333900, 2506615278, 1750243991, 1816622856, 768067820, 1791929408, 1320829363, 1599351468, 441046876, 3033374987], 'hits_found': 300} ops/fb 38541 bad [0, 0, 0, 0] {'lanes': 1060960, 'u': 80588, 'good': 80588} found 0 17.2s
```

## 16. What this filing changes relative to the base 087a18c4

The characteristic, the variant family G, the c7 classes (the first 64 of the 222), the exact ledger structure, H7, the premises
H1 - H4 and the preregistered-estimate procedure are 087a18c4's (and, through it, 1c36817's and 6c77089c's), with their
authors credited. This filing changes the counted program, its accounting and one estimate:

- **Classes.** All 222 classes with at least 3,456 variants (782,800 variants) instead of 64 classes of 3,600; the W7 test of
  all of them is one bit-sliced program of 375 counted operations per first block (the 64 tests cost 640). Per first block
  g = 830.99 good pairs instead of 244.58, so the compression, the fixed operations and the W7 test are shared by 3.4
  times more good pairs.
- **W6 programs.** Up to four batches per program (shared broadcast loads), constants folded per batch, the F6 conditions folded as
  soon as their bits exist: 459 operations per batch instead of 530.
- **Lane scan and good pairs.** 24-bit chunks through a table (53 per batch and 4 per lane instead of 22 and 11); four good pairs per
  group (34 operations instead of 4 x 30 for u); one V update per group; the row-16 test through a presence word of 256 values of u
  (5 + 5 x 0.0627 instead of 8 per pair) with the mask word read only for a hit.
- **q3.** A second preregistered study with W8 drawn from the 782,800 variants of the 222 classes: bound 2^-74.0252 (H6 at its
  face value, rounded down at the fourth decimal of its logarithm) instead of 2^-74.0173.
- **Ledger.** `a0core.py ledger` computes the Chebyshev exponent from the work cap (2^-21.4 instead of 2^-23.9; it is larger because one
  first block can now do more work), and mu0 = 0.49466302 from it; H3's premise on rho is 2^35 instead of 2^37.

Claim: T = 9,995,711,239,180,937,961,565 / 1322 = 2^62.713293, time_log2 62.7133. 087a18c4 claims 63.45545; the delta is 0.7421 bits.
The sensitivity table (Section 11.2) prices the alternatives, including 087a18c4's pads (62.73528) and the scalar readings.
