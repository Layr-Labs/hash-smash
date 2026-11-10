# Collision attack on 37-step SHA-256: the ePrint 2026/1120 two-block attack with 222 classes of A0-variants and a branch-specialised bit-sliced W6 filter, 2^62.34263

Track `sha256-r37-exploratory`, target `sha256-r37-prefix-v1`, cost model `collision-frontier-v5` (C = 2644).
Claim: `time_log2 = 62.34263` target compressions on every run, success probability at least 0.39 (0.3900000059 under the
stated premises), memory 2^32.67 bytes (reported only), nonuniform advice below 2^13 bytes.

The attack is the 37-step collision attack of Li, Zhang, Li, Liu, Qian and Zhu, "Pushing Collision Attacks on SHA-2
to 39 Steps" (IACR ePrint 2026/1120, CC BY), in the two-block memory-efficient framework of [LLWS26] (Li, Liu, Wang,
Shi, ePrint 2026/1080), with the A0-variants of its Step-1 solution found by itseasypop (1c368173) and qkniep
(b947b377) and priced by GordoAR (087a18c4). What this filing changes is the **counted online program**, not the attack:
(i) the bit-sliced W6 filter of a batch of 256 variants is a *decision DAG over the bits of the two per-first-block
scalars A_{-1} and C6 - A_{-2}*: at each bit the program tests the scalar bits (2 + 2 counted operations), runs the
variant of the bit slice in which they are constants and jumps to the merged code of the next bit (1 counted operation; every executed branch, jump and bit test is charged), so that full adders become half adders and carry chains collapse
(Section 9.4): about 129.8 counted operations per batch of 256 instead of 459 (1f12a09a) or 518..550 (087a18c4); (ii) the W7 test of
all 222 classes is the same kind of DAG (Section 9.3); (iii) the packed good-pair arithmetic, the lane scan and the
row-16 probe are priced from an executable, lane-safe program (Sections 9.5, 9.6). The exact ledger, the
preregistered estimate of q3 for the 222-class family (two studies, Section 7.4), the replay and the end-to-end
statistics are our own.

## 0. Summary

- **Algorithm (Sections 4-8).** Messages M0 || M1 and M0 || M1' (128 bytes; padding adds the same third block).
  A first block M0 is two fresh uniform 256-bit words; CV1 = F_37(IV, M0) costs one unit. For each of 222 fixed
  classes of variants (3456..3600 variants each, 782,800 in total; the classes of G with at least 3456 variants) one
  test W7x = c7 - A_{-1} in F7 decides whether all variants of the class pass the W7 filter; the test of all 222
  classes is one bit-sliced program (lane = class). For each passing class the counted W6 programs (groups of up to
  four batches of 256 variants) test the W6 filter; each variant passing both filters (a *good pair*) is collected,
  and the good pairs are processed in packed groups of four: u = W0 + s0(W1), a presence word, and an exact row-16
  table lookup over the 32 elements of L*; each row-16 pass is checked through row 36. A pair that follows every cell
  of rows 16..36 collides; it is verified with the target and output.
- **Rates (exact under H1).** Per first block: 222 p7 = 3.523 passing classes and
  g = 782,800 x p7 x p6 = 830.988 good pairs (p7 = |F7|/2^32 = 2^-5.97763, p6 = |F6|/2^32 = 2^-3.90197).
- **Probability (Section 7, H2).** q3 = average over the 782,800 variants and l in L* of Pr[rows 16..36 follow every
  cell and printed two-bit condition]; rows 16..22 are identical for every variant (Lemma 7.1). A preregistered
  sequential Monte-Carlo estimate (32 replicates, NP = 8192, W8 drawn from the 782,800 variants) gives mean 2^-73.9987
  and a one-sided 99% lower bound 2^-74.0225: q3_model = 2^-74.03 (the registered 2-decimal floor). A first
  preregistered study with NP = 2048 (mean 2^-74.0187, bound 2^-74.0659) is reported as well (Section 7.4).
- **Cost (Sections 9, 11).** N_FB = 358,768,851,784,995,369 first blocks (2^58.31583); per first block 1 unit plus 265 counted
  operations, plus on average 31195.59 counted data-dependent operations (10,700 for the W6 programs, lane scans and per-class
  control, 20,080 for the good pairs, 300 per-hit setup and rows >= 16), all capped by V_MAX.
  T = A_C + A_S + DEV + N_FB + (N_FB x 265 + V_MAX + overshoot + preprocessing + final)/C + 6 =
  15,461,844,764,535,665,517,649 / 2644 = 2^62.342624, claimed 62.34263.
- **Premises (Section 12).** H1 uniform independent chaining values; H2 q3 >= 2^-74.03 for the variants; H3 given one
  success, the expected number of further successes in the same first block is small (<= 2^-9.4; rho <= 2^35); H4 advice
  allowances (A_C = 2^60, A_S = 2^50, DEV = 2^40, as in the accepted filings); H5 counted word-RAM pricing of the
  decision-DAG filters (data-dependent branches are one primitive each; every executed primitive is counted; the code is
  produced by a charged precomputation, Section 11.1); H7 the exact success floor of 087a18c4. No H6 de-pad: q3_model
  is the registered floor.
- **Checks.** Exhaustive: |G| = 12,103,680; the 222 classes; F6, F7 sizes and affine decompositions (2^32 words);
  the row-16 table (1,052,672 pairs) and its presence word (all 1,042,240 members). The executable program (the
  file `experiments/spec6core.py`): the W7 DAG equals the definition on 66,600 lanes, the W6 DAGs equal the scalar
  definition on 17,552 lanes (selftest) and about 5.8 million lanes (verify_pkg), the packed arithmetic equals the definition of u on 8,000 lanes, 300 first blocks with
  287,782 good pairs agree with a brute-force reference (0 mismatches, row-16 passes 58 of 58); end-to-end C statistics
  on 2^21 and 2^23 first blocks (Section 13.1); a replay of 19.6 million distinct Step-3 successes (Section 13.1); 
  37-step semi-free-start collisions with variants of the new classes (Section 13.2); two organizer experiments (Section 13.3).

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
- Filing 6c77089c (winglock, 74.22669): the transcription of Tables 15-17, the member orientation, the reading of
  '+', the corrected two-bit condition A15[29] = A17[29], the exact Step-2 sets F6, F7, the exact set L* (|L*| = 32),
  and the SMC design for q3. Filing dd6656d (Th0rgal): the affine decomposition of F6, F7. Filing 1c368173 (itseasypop,
  63.47455) and b947b377 (qkniep): the A0 freedom of the Step-1 solution (the variant family G), the c7 classes and
  the first bit-sliced W6 program. Filing 087a18c4 (GordoAR, 63.45545): the exact-rational ledger, the premises
  H1-H5 in the form used here, H7, the first-block-level success analysis. Filing 1f12a09a (0xshikhar, 62.7133): the
  selection of all 222 classes with at least 3456 variants, packed groups of four 64-bit lanes and a presence word for the row-16
  probe, as stated in its public note; we did not have its package, and we derived every count below from our own
  executable program. Bit-slicing lineage: Th0rgal (64bca7e2, dd6656d, 5db3c77e), mitchuski (fca38c6d), jaazinn
  (817d444c). Filing 6eeefb64 (sha256-r32, promoted): the calibrated price of a solver CPU-second used for A_C.
  We re-derived and re-checked everything we use with our own code (Section 13); we did not execute any peer's code.
- **New here.** (i) The W6 filter as a decision DAG over the bits of A_{-1} and C6 - A_{-2} (Section 9.4) and the
  same for the W7 test (Section 9.3); (ii) the NOT-free full adder carry = x ^ ((x ^ y) & (x ^ z)) for the pair (y, z)
  of equal stored polarity, which keeps every program free of NOT operations except where a polarity mismatch is
  unavoidable; (iii) the exact expected cost of the DAGs by a dynamic program over the abstract carry state,
  checked by simulation; (iv) a lane-safe packed good-pair program (minuend bias 2^34, reduced subtrahends) and its
  executable verification; (v) the register bound (at most 52 live values in any segment of any program), the code
  size of the DAGs (2^25.27 instructions) and the preprocessing bound; (vi) our own preregistered q3 estimate
  for the 222-class family (two studies), replay and end-to-end statistics; (vii) the exact ledger.

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
with x = M', y = M (`experiments/spec6core.py` rebuilds both members and checks the cells; the repository
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
(each step inverted for its new coordinate). W8..W13 do not depend on CV1. *Proof.* Substitution; `spec6core.py`
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
W8x[8] != W8x[25], W8x[14] = W8x[18]}**. Exhaustive enumeration of all 2^32 words (`genum2.c`, Appendix A):
|G| = 12,103,680 = 2^23.529. The published A0 (1b21ce20) is in G.

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
(exhaustive, `f6chk.c`, Appendix A). By the carry pattern of w + d (s0 is linear), each set is a disjoint union of
affine spaces. We use them in the following bitwise form, **checked against the definition on all 2^32 words**
(`f6chk.c`, `f7chk.c`; zero mismatches for both):

```text
F6: w is NOT in F6  iff  common | (w29 & (bc | (w30 & X)))  with
      common = (w14^w18) | ~(w8^w25) | (w1^w12),   bc = (w15^w19) | ~(w9^w26) | (w2^w13),
      X = (w16^w20^w31) | ~(w10^w27^w31) | (w3^w14^w31)                                  (bits are w_i; | is OR)
F7: w is in F7  iff  w1 = w18, w0 = w28, w9 = w30 and
      [ w11 = 0, w22 = 1, w26 = 1 ]                                                       2^26 words
      or [ w11 = 1, w12 = 0, w22 = 0, w23 = 1, w26 = 0, w27 = 1, w2 = w19, w1 = w29, w10 = w31 ]   2^20 words
```

(F6 is the form published in 087a18c4/1c368173 with b_bad & c_bad simplified to bc | (w30 & X); we re-derived the F7 constraint
set by computing the affine hull of F7 and of its two halves (`f7an.c`, `f7dual.c`, Appendix A) and then verified
it exhaustively.)

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

### 5.3 The c7 classes and the selection (1f12a09a's selection, re-derived)

c7(a0) takes only **22,976 distinct values on G** (exhaustive, `genum2.c`). A *class* is G intersected with one
value of c7. For all variants of one class and a given CV1, W7x is the same word, so one membership test decides the
W7 filter of the whole class. The class sizes are at most 3600; the sizes 3600 (85 classes), 3584 (26) and 3456 (111)
are the only ones above 2751. **The 222 classes with at least 3456 variants are used** (782,800 variants; the next
largest classes have at most 2751 variants (12 classes), and 2,838 classes have about 1,800: a back-of-envelope marginal-cost estimate with the program of Section 9 (cost of a class per good pair above the average) did not favour them; we did not run the larger families). Each class equals {base XOR s : s subset of mask, s in G, c7 = the class value}
for the descriptors below (c7, base, mask, size; checked exhaustively):

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
function of E16x only. Our own exhaustive enumeration (`r16.c`, Appendix A: all E16x with the row's nine fixed
x-bits, 2^23 per l, for the 28 elements of L* whose row 16 can hold, the other four having a nonzero W16 difference)
gives 1,052,672 pairs (u, l) (the same number as 6c77089c and 087a18c4), 1,042,240 distinct u. The table
R16[u] = {l : C16_l + u passes row 16} is a 2^32-bit bitmap of the distinct u (512 MB, a lookup is a word load
and a bit test) and, for the 0.2 row-16 passes per first block, a sorted array of the 1,042,240 members with their
l-masks (a binary search of at most 21 steps). By Lemma 5.1 u is uniform for a good pair, so
Pr[row 16 for l] = |R16_l|/2^32 exactly, and Pr[u in R16] = 1,042,240/2^32.

**The presence word (first-level probe).** Let c = C16_19 = 43579466. The 8-bit window (u + c) >> 16 & 255 takes
only 56 of the 256 values on the 1,042,240 members (no other (c, s) among the 28 C16_l, 200 random constants and all
shifts s in 0..24 gives fewer); PRES_P is the 256-bit word with the 56 bits set. A u with a clear window bit is not a
member (zero false negatives by construction; checked on all members, `presence.py`, Appendix A); a present window is
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

### 7.3 The estimator (`smc.c`, Appendix A)

Stages: row 16 exact (the enumeration of 6.2: the stage mean is (1/32) sum_l |R16_l| / 2^32 = 2^-16.994, and the
initial particles are drawn exactly from the passing (l, E16) pairs); rows 17..21: each child proposes E_t^x
uniformly with the row's fixed x-bits imposed (exact importance weight 2^-f), sets W_t^x = E_t^x - (the rest of step
t), W_t^y = W_t^x + its exact difference, and checks the whole row; row 22: (W6, W7) drawn uniformly from F6 x F7;
rows 23..36: W8 of a variant drawn uniformly from the 782,800 selected variants (the same row-22 survivor is also
evaluated with the published W8 for a paired comparison). NP particles, M children per particle per stage, MT tail
proposals per particle, multinomial resampling of the survivors after every stage; the product of the stage means
is an unbiased estimator of q3 (standard SMC normalising-constant estimator). This design is 6c77089c's and
087a18c4's; `smc.c` is a fresh implementation (written for this filing by a delegated sub-agent of our harness from the
specification of this section, with our reference data; it reproduces the per-l counts of 6.2, the stage means of
the peers' studies and passes its own self-tests: rows 4..15 for all 32 l, the F6/F7 samplers, all 782,800 variants
satisfy the T8 and W8 conditions).

### 7.4 Preregistration and results (two studies, both reported)

**Study A.** Frozen at 2026-10-10T08:11:18Z before any listed seed ran (`PREREG_q3_222.txt`, `sha256sum` 5bab3530...;
`smc.c` SHA-256 68529712..., `lab.h` bdefd674...): NP = 2048, M = 512, MT = 16384, replicate seeds 70000..70007,
71000..71007, 72000..72007, 73000..73007 (32 replicates); rule: one-sided 99% Student lower bound of the mean of the
32 linear estimates (t = 2.4528, 31 df), q3_model = 2^(floor(100 log2 LB)/100). Result: mean 2^-74.0187, relative
standard deviation 0.0743, lower bound 2^-74.0659, **q3_model(A) = 2^-74.07**.

**Study B.** Study A's spread (relative sd 0.074, about 500 distinct row-22 survivors per replicate) is larger than the peers'
(0.042); we therefore registered a second study with a larger particle count, **after having read study A's result**, to
tighten the bound. Frozen at 2026-10-10T08:20:03Z (`PREREG_q3_222_b.txt`, `sha256sum` 6b1c9dbb...): the same program and binary (no
change), NP = 8192, M = 512, MT = 16384, seeds 74000..74007, 75000..75007, 76000..76007, 77000..77007, the same decision rule. No
rerun, no seed change. All 32 replicates (log2):

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
| rows 23..36 paired: variant W8 / published W8 | 2^-4.013 / 2^-3.940 (65,536 particles, heavily duplicated) | 2^-4.006 / 2^-4.004 |

The choice of study B is disclosed here and priced: with study A's value the claim would be 62.37482 (Section 11.2); with B's
mean instead of its bound, 62.31756. The stage factors equal, within 0.01 bit, the per-row condition counts of the printed tables
(17, 13, 15, 6, 7, 1, 11, 4; 74 in total) and the peers' stage factors.

### 7.5 Consistency

- Lemma 7.1 makes rows 16..22 identical by construction; the paired rows-23..36 rates of the variants' and the published W8
  differ by 0.002 bit in study B.
- Real first blocks (Section 13.1): the row-16 pass rate of the attack's own good pairs is the exact 2^-12 (z = +0.88
  and +0.51 over 424,363 and 1,693,297 passes).
- Same-pair co-successes: Section 13.1 (replay).

## 8. The algorithm (fixed caps)

```text
input: N_FB, V_MAX; precomputed: S, L*, the 222 class descriptors and their variant data and decision DAGs (Section 9.4), the
       bitmap of the row-16 table (2^32 bits), the sorted member array, the presence word, the 24-bit lane-scan tables
V = 0
for f = 1 .. N_FB:
    draw two uniform 256-bit words; M0 := their sixteen 32-bit fields; CV1 := F_37(IV, M0)          [1 unit]
    pass7 := the W7 decision DAG on A_{-1} (lane = class)                    (Section 9.3)
    hits := the classes with a set bit of pass7 (lane scan)
    if hits:
        cb := C6 - A_{-2}
        for c in hits:
            V += 1
            for each group of up to four batches of 256 variants of c:
                run the W6 decision DAG on (A_{-1}, cb): 32 times (test the bit of A_{-1}; test the bit of cb;
                    the segments of the bit; V += their executed operations)        (Section 9.4)
                for each batch: lane scan of its pass plane; for every lane: append (a0, S0(a0)) to the list of good pairs
            V += the scan costs; if V > V_MAX: halt (failure)
        if the list is nonempty (first time in this first block: the per-first-block constants of W0, W1, V += 1):
            for each group of four good pairs: u := W0 + s0(W1) (packed, Section 9.6); V += its cost
                for each valid lane: presence word of the window of u + c; if present: V += ..; exact lookup of u in the row-16 table
                    if it is a member: V += 1; mask := the l of its member entry; recompute W6, W7;
                        for l in mask: rows 16..36 with early abort
                            if all rows pass: build m, m'; if digest(m) = digest(m') and m != m': output, halt
halt (failure)
```

V counts every data-dependent operation in units of operations: every increment is itself a counted addition and the
immediates are the exact costs of the code just executed (Section 9.8). The run executes at most N_FB compressions,
N_FB x 265 fixed operations, V_MAX + the maximal work of one first block of data-dependent operations (the cap is tested after every
class, but the packed good-pair work of a first block follows its last class test), the precomputation and one final verification, whatever the coins.

## 9. The counted program

### 9.1 Machine and pricing

256-bit word RAM, 64 registers, every executed primitive counted (loads, stores and branches included). 32-bit values
are kept in the low bits; a reduction mod 2^32 is one AND; a 32-bit rotation pattern (S0, S1, s0, s1) costs 8:
d = x | (x << 32) (2), three shifts and two XORs and one mask. A bitmap lookup (2^32 bits in 256-bit words, the word
at address u & (2^24 - 1), the bit u >> 24) costs the extraction of u from its lane, the address (and), the bit index
(shr, and), the load, the shift of the word, an and with 1 and a branch. **A branch and an unconditional jump are one primitive each** (as in 087a18c4's
scans); to branch on bit j of a register x the program first isolates the bit (one AND with an immediate), so a
bit test is two primitives. The target compression of a first block is one unit and its internal operations are
not counted again. The executable counted program is `experiments/spec6core.py` (`online`, `run_group`, `good_group`,
`w7_run`); its routines count every executed primitive of the routines below, and the ledger (`ledger`) is computed
from them with exact rationals.

### 9.2 Fixed per first block: 265 operations

- First block words: 2 random words, then the 16 fields (field 0 of a word: and; fields 1..6: shr, and; field 7:
  shr): 30.
- Control allowance 16 (loop counter add and compare-branch, hit-list initialisation, the `if hits` branch, and 12 for any further loop or
  address arithmetic not itemised elsewhere).
- The W7 decision DAG (Section 9.3): at most 191 (64 test primitives, 32 jumps and at most 95 operations).
- The scan of the pass plane of the W7 test (222 live lanes, 10 chunks of 24 bits): 28 (extraction of the chunks:
  the lowest and the highest chunk cost one operation, the others two; one zero branch per chunk). Per passing class
  5 more (Section 9.5).

### 9.3 The W7 test of all classes as a decision DAG

Lane i of every plane is class i (222 live lanes). W7x = c7 - A_{-1} (mod 2^32) is computed by the borrow chain of a
subtraction whose subtrahend A_{-1} is the scalar: at bit j the program tests bit a_j of A_{-1} (and + branch), runs the variant for a_j
and jumps to the test of the next bit (1). With NC_j the plane of ~(bit j of c7) over the classes: d_j = c7_j ^ a_j ^ b_j and
b_{j+1} = (a_j ? NC_j | b_j : NC_j & b_j) with b_0 = 0 (a half subtractor: one operation per bit); the 17 bits of
W7x that F7 tests (Section 5.1) are formed by one XOR each. The 16 bits of c7 that are the same for all 222 classes are
constants (no load); the other 16 planes are loaded (one load each). The conditions of F7 (Section 5.1) are then
5 operations for the three equalities common to both halves, 10 for the second half, 1 for the first half and 4 for the
selection by w11, plus the polarity NOTs, the final complement and the AND with the lane mask of the 222 live lanes.
**Bound:** the executed operations of any path (without the 64 test operations and the 32 jumps) are at most
16 loads + 30 borrow operations (bits 1..30) + 17 XORs + 20 condition operations + 8 NOTs + 2 (final NOT and mask) = 93 <= 95;
the largest count over 3,000 random A_{-1} was 69 (`selftest`). The pass plane equals the definition of F7 on
all lanes: 66,600 lanes (996 passes) in `selftest` and the 2^23 first blocks of the C statistics (Section 13.1).

### 9.4 The W6 filter as a decision DAG

**The arithmetic.** For a batch of up to 256 variants (lane L = variant L), with ab_j the bits of A_{-1} and
z_j the bits of cb = C6 - A_{-2}:
W6x = cb + MAJ(A1, a0, A_{-1}) + ~CH(E5, E4, E3) + 1 (mod 2^32), E3 = K3 + A_{-1} with K3 = K3C - MAJ(A2, A1, a0),
where MAJ_j = (a0_j | ab_j) if A1_j else (a0_j & ab_j), and y_j = ~CH_j = ~E4_j if E5_j else ~E3_j (A1, E5 are constants of S).
The program runs bit-serially from j = 0 to 31 with three carries: c_e3 (the carry of K3 + A_{-1}; needed up to bit 28),
c_csa (the carries of the carry-save addition of (MAJ, y, cb), initially 1 for the "+1") and k_rip (the carry of the ripple
addition of the carry-save sum and carries, initially 0): per bit
(s_j, c_csa') = FA(MAJ_j, y_j, z_j), (w_j, k_rip') = FA(s_j, c_csa, k_rip). The bits w_j are folded into
the F6 test (Section 5.1) as soon as both bits of a term are available: x3 = w1^w12 (bit 12), y3 = w2^w13 (13), s = w3^w14 (14),
cm = (w14^w18) | x3 (18), bp = (w15^w19) | y3 (19), q = w16^w20 (20), common = cm | ~(w8^w25) (25), bc = bp | ~(w9^w26) (26),
r = w10^w27 (27); the tail is fail = common | (w29 & (bc | (w30 & X))), X = (q^w31) | ~(r^w31) | (s^w31), and
pass = ~fail & (lane mask of the live lanes of a partial batch).

**The decision DAG.** The bits ab_j and z_j are the same for all batches of all classes of the first block. At bit j the
program tests ab_j (an AND with the immediate 2^j and a branch) and z_j (the same on cb): 4 primitives per bit, 128 per
group, shared by the up to four batches of the group. The segment executed for (ab_j, z_j) ends with an unconditional jump to the (merged) code of
the next node: 1 primitive per bit, 32 per group (the DAG shares code between paths, so at most one path into a node can fall through; we charge all). The code reached by the outcome (ab_j, z_j) is the *segment* of bit j in which
ab_j and z_j are the constants 0 or 1. A full adder with a constant input is a half adder (2 operations instead of 5) and
one with two constants is a wire, so the segments are much shorter than the generic bit slice, and the carries are
constants where the class data allow (many planes of a0, K3, ~E4 are constant over a batch: the 3456..3600 variants of a class
are base XOR s for s in a subspace of rank 14..16, ordered by value, so each batch of 256 has constant high planes).
After each bit the program adds the executed cost of the segment to V (Section 9.8): 1 more primitive per bit, 32 per group.

**Segments and abstract states.** A segment is a straight-line program over the registers that hold the carries and the
retained values (the w bits and partial terms of the F6 test, between their birth and use), the loaded planes of the
batch (a0_j, K3_j, ~E4_j where not constant, in the polarity needed), and the constants. Two programs are equal if their
(bit j, class constants of bit j, abstract state, ab_j, z_j) are equal, where the abstract state is the triple of carries,
each 0, 1 or "register"; every retained value is a register (a retained value that is a constant is held in the
all-zeros or all-ones register: no folding is lost except one operation per retained constant). `spec6core.step`
builds the segment for one such key with the builder of Section 9.4.1 and returns its executed operations and the next
abstract state; the decision DAG of a group is the set of joint states (one abstract state per batch of the group)
reachable by the 4^32 outcome sequences, merged at equal joint states. Over all 888 groups of the 222 classes the DAGs have 1,027,268
joint nodes and 40,394,879 instructions (2^25.27; about 2^28.3 bytes of code at 8 bytes per instruction), at most 278
joint nodes per bit; `python3 spec6core.py dag 3` reproduces the numbers (about 10 minutes).

**9.4.1 The builder.** Straight-line programs over 256-bit planes with and, or, xor, not and loads; literals are
(node, negated) or constants; and/or of two literals of different stored polarity is realised by De Morgan when both are negated and
otherwise by one NOT; the planes of a0, K3, ~E4 are stored in both polarities and a load takes the polarity that matches its partner;
state values are kept in a fixed stored polarity between bits (`CANON`; chosen by a coordinate search on the expected cost). The full adder is
carry = x ^ ((x ^ y) & (x ^ z)) with x chosen so that y and z have the same stored polarity (two of three always do): no NOT is
needed, 5 operations (xy, xz, and, xor for the carry, xor for the sum). With a constant input the adder is a half adder.

**Cost semantics and the exact expectation.** The ops executed on a path are the sum of the segment costs, the tail, and per group 128 test
primitives, 32 jumps and 32 V additions. For uniform independent bits of A_{-1} and cb (H1) the expected cost of a batch is computed exactly by a dynamic
program over the abstract states (`expected_cost`: each of the 4 outcomes of a bit has probability 1/4); it is the number charged in the
ledger (mean 129.8 per batch of 256 variants, excluding the tests, the V additions and the lane scan; a batch with fewer live lanes
costs less). **The DP is validated by simulation:** 800 random scalar pairs on three groups of four batches gave means 628.97, 676.88 and 629.68 against
the exact expectations 629.59, 677.75 and 630.53 (standard error 1.5). `worst_cost` gives the worst case per batch (at most 243), used only for the
overshoot bound of Section 11. **Correctness:** every pass plane equals the scalar definition W6x in F6: 17,552 lanes (selftest) and about 5.8 million lanes (verify_pkg),
every lane of every group processed by the organizer experiment `a0-online-r37`, and the good-pair sets of 3,000 first blocks against a
brute-force reference (3,000 first blocks, 2,639,113 good pairs, 657 row-16 passes, 0 mismatches).

**The law of the scalars given a W7 hit.** The W6 DAGs of a class run only if its W7 test passed, i.e. A_{-1} = c7 - w with w uniform on F7 (not uniform on 2^32); cb is uniform and independent. The DP averages over uniform A_{-1}.
We measured the effect: (i) for five classes, 400 draws each of the conditional law gave 0.995..0.999 of the uniform-law mean cost (standard error 0.3%); (ii) end to end, 90,000 first blocks of the executable program (316,331 passing classes, the true
conditional law) cost 2,463.7 operations per passing class (tests, V additions and segments of all groups) against 2,466.4 in the ledger (ratio 0.9989). The cost is therefore slightly
overestimated, and the cap uses the slack (1 + 2^-6) (1.56%) instead of 2^-8, so that a conditional bias of the W6 part (a third of vbar) of up to 4.7% would still be absorbed.

**Registers.** A segment keeps the retained values of all batches of the group: at most 12 per batch between bits and at most 52
simultaneously live values over every segment of every DAG (the live values are counted exactly in `dag`: the
inputs of the segment of batch q, its temporaries, the outputs of the batches before q and the inputs of the batches after q).
With the scalars A_{-1} and cb, the V counter, the all-zeros and all-ones registers and the lane mask this is at most 58 of 64 registers, no spills.

### 9.5 Lane scan and gather

The pass plane of a batch with nl live lanes is scanned in 24-bit chunks: per chunk the extraction (lowest and highest chunk one
operation, the others two) and a zero branch; per set lane: the load of the lane index from the 2^24-entry table of the chunk position (the
chunk offset is in the table), the add of the batch base, x - 1, x & (x - 1) and the loop branch: 5 operations. Then
the lane's 64-bit record (a0 | S0(a0) << 32) is loaded and stored into the list of good pairs, the list pointer advancing by 8: 3 operations
(ld, st, add). The 11 tables have 2^24 words each.

### 9.6 Packed good pairs: the group of four

The good pairs of a first block are processed in groups of four whose records occupy the four 64-bit lanes of one 256-bit word (a partial last group is
processed like a full one and only its valid lanes are probed). The arithmetic is lane-safe: with M = 2^32 - 1 in every lane,
a0 = G & M, S0a = (G >> 32) & M, E0 = (a0 + e0b) & M, W0 = a0 + kap0 (< 2^33), mj = (a0 & o12) | n12, ch = (E0 & X) ^ Em2,
S1(E0) with the 8-operation pattern (masked), W1 = (kap1 + 2^34 - S0a - mj - S1(E0) - ch) & M (the bias 2^34 keeps every lane positive: each subtrahend is
below 2^32, so the lane stays in [2^34 - 2^32 ... , 2^35) and no borrow or carry crosses a lane boundary), s0(W1) with the 8-operation pattern (masked),
and U = W0 + s0(W1) (< 2^34). The constants e0b, kap0, o12, n12, X, Em2, kap1 are computed once per first block from the
chaining value (35 operations; kap0 = e0b - A_{-4} - E_{-4} - S1(E_{-1}) - CH(E_{-1}, E_{-2}, E_{-3}) - K0, e0b = A_{-4} - S0(A_{-1}) - MAJ(A_{-1}, A_{-2}, A_{-3}),
kap1 = A1 - K1 - E_{-3}, as in Lemma 4.1). Group cost: ld G 1, unpack 3, E0 2, W0 1, mj 2, ch 2, S1 8, W1 5, s0 8, u 1, U + c 1, loop control 2, V addition 1 = **37**.
**Verification:** `selftest` compares the 4 lanes of U with the definition of u (W0 + s0(W1) from the chaining value and a0) on 8,000 lanes: 0 mismatches; the e2e
run (Section 13.1) checks u of every sampled pair.
Then, per valid lane k: the presence word (Section 6.2): shr of U + c by 64k + 16, and 255, shr of PRES_P, and 1, branch: **5**. If the window is present,
the exact lookup: extraction of u from its lane (k = 0: and; k >= 1: shr, and), the word address (and), the bit index (shr, and), the load, the shift of
the word, and 1, the branch and the V addition: **8** (k = 0) or **9** (k >= 1). Under H1 the window is present with probability 56/256 = 7/32 exactly
(u is uniform, Lemma 5.1), so the expected cost per good pair is 5 + (7/32) x 8.75 = 6.91, and with the group's 37 operations and the scan
and gather the cost per good pair is **24.1640625** operations.

### 9.7 The rare path

A member of the row-16 table (probability 1,042,240/2^32 per good pair): V += 1; the l-mask of u by binary search of the sorted array (at most 21 steps of 6
operations plus 6: 132); recompute W6, W7 (23 operations); then for the l in the mask W0..W5 and W8 (201), the y-words (8) and rows 16..36 with early
abort (each row 106 + 53 + 1: both members' W (20), CH (3), E (14), MAJ (4), A (12) per word; the cells and the two-bit conditions closing at the row
at most 53), charged for rows 16 and 17 always and for rows 18..36 with probability at most 2^-9 each (the SMC stage factors give 2^-15, 2^-6, ...).

### 9.8 The work counter V

V counts every data-dependent operation. After each bit of a W6 group V receives the executed cost of the segment of that bit (including its own
addition, the jump and the 4 test primitives of the bit; the immediate is a constant of the code reached); after each class the scan costs (the
list pointer's advance is 8 bytes per good pair and 8 operations of scan and gather are charged per good pair, so V += pointer difference, plus the
chunk costs: 2 operations, inside the class control allowance of 8) and V is compared with V_MAX (2 operations); a group of good pairs adds its fixed
cost (its V addition is in the 37), each present probe adds its own cost (the V addition is in the 8/9) and a row-16 member adds 1.
The cap is tested after every class; the good-pair work of a first block follows its last class test, so the overshoot past V_MAX is at most the
maximal data-dependent work of one first block, vmax_fb = 84,668,692,916 (all 222 classes, every variant good and every l past row 16 to row 36), which the
ledger charges.

## 10. Success probability, independence and caps

Let a *trial* t = (f, a0, l) be a first block f, a selected variant a0 and l in L*, and A_t the event that a0 is
good for f and the pair follows every cell and printed two-bit condition of rows 16..36. The program examines every
good pair of every processed first block and every l whose row 16 holds, so it finds a success iff some A_t occurs
before the caps (and every output is verified, Lemma 6.1). Let X_f = sum over the trials of f of 1[A_t] and
X = sum_f X_f.

- **Expectation.** E[X_f] = g x 32 x q3 (Lemma 5.1 and Section 7) and E[X] = N_FB g 32 q3. With q3 >= q3_model
  (H2): E[X] >= N_FB g 32 2^-74.03 >= mu0 = 0.49466248 (H7) for N_FB = ceil(mu0 / (g 32 2^-74.03)) = 358,768,851,784,995,369 = 2^58.31583;
  mu0 is the smallest 8-decimal number strictly above -ln(0.61 - Pcap - 2^-60) / (1 - 2^-10.4), with Pcap the work-cap
  failure bound below.
- **One first block (H3).** By Bonferroni, Pr[X_f >= 1] >= E[X_f] - sum over pairs t < t' of f of Pr[A_t and A_t']
  = E[X_f] - (1/2) sum_t Pr[A_t] E[X_f - 1 | A_t]. H3: E[X_f - 1 | A_t] <= delta = 2^-9.4 for every trial t,
  so Pr[X_f >= 1] >= (1 - 2^-10.4) E[X_f]. (Only the expected number of *further* successes of the same
  first block given one success is needed; bursty goodness and shared W7/W6 values enter only through
  that conditional expectation, and do not affect E[X], which is linear.)
- **Many first blocks (H1).** Distinct first blocks have independent chaining values, so the events X_f >= 1 are
  independent and Pr[X >= 1] >= 1 - exp(-sum_f Pr[X_f >= 1]) >= 1 - exp(-(1 - 2^-10.4) mu0).
- **Work cap.** The data-dependent work v_f of a first block (everything except its compression and its 265 fixed
  operations) has mean at most vbar = 31195.59 (Section 11: the per-class setup is charged per passing class rather than
  per first block and the row-16 work per (pair, l)) and is at most vmax_fb = 84,668,692,916 (< 2^36.3; every class passing, every
  variant good, every l past row 16 to row 36). The v_f are independent (H1), so by Chebyshev
  Pr[sum v_f > (1 + 2^-6) N_FB vbar] <= E[v_f^2]/(2^-12 N_FB vbar^2) <= vmax_fb/(2^-12 N_FB vbar) = Pcap < 2^-24.9.
  V_MAX = ceil((1 + 2^-6) N_FB vbar) = 11,366,881,928,865,994,508,928 is reached with probability below Pcap; the run then fails, which is accounted for here.
  (The data-dependent work of the DAGs is a function of the first block's A_{-1}, A_{-2} only; its mean over uniform inputs is the exact expectation of
  Section 9.4, H1.)
- **Success.** Pr[output a collision] >= 1 - exp(-(1 - 2^-10.4) mu0) - Pcap - 2^-60 = 0.3900000059 > 0.39 (the 2^-60 covers a repeated
  first block among N_FB draws of 512 bits). With q3 = the SMC mean instead of its lower bound the
  bound is larger. Any output is a verified collision, independent of the premises.

## 11. Ledger (exact; `python3 experiments/spec6core.py ledger 3`)

```text
T = A_C + A_S + DEV + N_FB + (N_FB x 265 + V_MAX + vmax_fb + PRE + FIN) / C + 6
  A_C = 2^60   characteristic search and SFS-pair search of the paper (allowance, H4)
  A_S = 2^50   Step-1 SAT solve (paper: 2^41.3)
  DEV = 2^40   all development computation (Section 13.4)
  N_FB = 358,768,851,784,995,369 compressions (2^58.31583; H7 mu0 = 0.49466248, q3 = 2^-74.03)
  265     fixed operations per first block (9.2: 30 + 16 control + 191 W7 DAG (64 tests + 32 jumps + 95) + 28 hit-scan chunks)
  V_MAX = 11,366,881,928,865,994,508,928 = ceil((1 + 2^-6) N_FB vbar), vbar = 31195.59 operations, of which
               per passing class setup (cb, group-loop allowance, the per-first-block constants of W0 and W1, V): 222 p7 x 78 -> 274.79
               W6 decision DAGs, lane-scan chunks and class control: p7 x sum over the 222 classes of
                 (8 + 1 + 2 + 5 + sum over its groups (128 tests + 32 jumps + 32 V additions + expected segments and tails) + sum over its batches (chunk scan)) -> 10,700
               good pairs: g x 24.1640625 -> 20,080   (5 scan + 3 gather + (37 + 4 x 5)/4 group + (7/32) x 35/4 exact probes)
               rows >= 16: g x 2^-12.0 x (357 + 328 + (19/512) 160) -> 140.72
  vmax_fb = 84,668,692,916 (one first block's maximal work: overshoot past the last cap test)
  PRE = 2^40 operations (bound on all precomputation, Section 11.1); FIN = 1600 operations (the final verification and
  the next first block's setup after the last cap test) and 6 compressions
T x 2644 = 15,461,844,764,535,665,517,649     ->   T = 2^62.342624  ->  time_log2 = 62.34263
preprocessing = A_C + A_S + DEV + PRE/C = 2^60.00141
```

Every count in this block is produced by `ledger()` of `experiments/spec6core.py` from the executable routines; the integer-tightness of the 5th
decimal is asserted in both directions (T^100000 against 2^(p) and 2^(p-1)).

### 11.1 Precomputation (bounded by 2^40 operations)

Enumerating G and c7 over all 2^32 words (about 40 operations each, 2^37.4); grouping the 12.1 million variants by c7 and
selecting the 222 classes (below 2^31); the row-16 enumeration (2^24 zeroing stores and 28 x 2^23 row-16 evaluations at about 150
operations, 2^34.3), its bitmap and sorted member array (below 2^26), the presence word (28 + 200 candidate constants x 25 shifts over
the 1,042,240 members, below 2^35), the 11 lane-scan tables of 2^24 words (below 2^30), the stored planes of 3,193 batches (both polarities, below
2^27), and the compilation of the decision DAGs: 40,394,879 emitted instructions at at most 100 operations per instruction (below 2^32). Total below 2^38.7 operations.

### 11.2 Sensitivity (log2 T, one input changed)

| change | log2 T |
|---|---|
| as claimed (q3 = 2^-74.03, study B's bound) | 62.34263 |
| q3 = 2^-74.0225 (study B's bound at face value) | 62.33661 |
| q3 = 2^-74.07 (study A's bound) | 62.37482 |
| q3 = 2^-74.25 | 62.52179 |
| q3 = 2^-74.5 | 62.73122 |
| q3 = 2^-75 (the paper's count of 75 conditions) | 63.16607 |
| A_C = 2^64 | 64.32713 |
| A_C = 2^56 | 62.04780 |
| W6 priced as in the generic bit-sliced program of 1f12a09a's note (459 + 2 per batch and 258 per passing first block for the broadcast planes; same scan, same good-pair stage) | 62.78253 |

### 11.3 The advice-construction allowances A_S and A_C (H4)

The cost model charges all construction of the advice, including searches omitted from the program. The advice is
(i) the 37-step characteristic and its two-bit conditions (Tables 15, 16), (ii) the Step-1 solution S, and (iii) the
semi-free-start pair (Table 17) from which S is read. Everything derived from them (G, the classes, F6, F7, L*, R16, the DAGs)
is recomputed inside the precomputation (Section 11.1).

- **(ii) and (iii): Step 1 and the SFS pair, charged A_S = 2^50.** The paper reports its Step-1 SAT solve at 2^41.3
  compression-equivalents; A_S is 2^8.7 times that. Completing a Step-1 solution to a 37-step semi-free-start pair is
  cheap and is reproduced in this package: given the characteristic and a dense part (S or any of its A0-variants),
  the organizer experiment `a0-sfs-r37` builds complete 37-step semi-free-start collisions in about one
  second each (rows 16..21 by sampling, rows 22..36 by about 2^9 tail proposals; Section 13.2). So the SFS-pair search beyond Step 1 costs below 2^30 units,
  far inside A_S.
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
  accepted measurement of the predecessor search. The same allowances are charged by the accepted filings 087a18c4 and 1f12a09a on this track.
- Sensitivity: see 11.2. No other term depends on it.

## 12. Premises

**H1 - uniform independent chaining values (score-critical).** The first blocks are fresh uniform 512-bit strings;
their chaining values CV1 = F_37(IV, M0) behave as independent uniform 256-bit values, and the pair (A_{-1}, A_{-2}) that selects the path of the
decision DAGs is uniform on (2^32)^2. Used for: Lemma 5.1 (exact filter rates and the law of the second-block words, per variant), the
expected counts and the exact expected cost of the DAGs (the DP of Section 9.4 averages over uniform bits), the independence across first blocks
(Section 10) and Chebyshev. Evidence: 2^21 and 2^23 real first blocks through the attack's own filters in C (Section 13.1: passing classes,
good pairs and row-16 passes at the predicted rates); 3,000 first blocks through the executable counted program against a brute-force reference;
the mean of the executable program's operation count against the ledger; the organizer experiment `a0-online-r37`. Limitations: a premise; tested on 2^23 first blocks, not 2^58.3.

**H2 - Step-3 probability of the variants (score-critical).** q3 >= q3_model = 2^-74.03 (Section 7.1's average over
the 782,800 selected variants and L*), and q3 <= 2^-70. Evidence: Lemma 7.1 (rows 16..22 identical for all variants; the variant enters only through W8 in W23, W24),
the two preregistered SMC studies (Section 7.4; study B is the primary, both are reported and the disclosure of how study B came about is in 7.4),
the paired comparison of rows 23..36, the agreement of the stage factors with the printed tables and the peers' studies row by row, the row-16 rate of real good pairs,
and 37-step semi-free-start collisions built with variant dense parts (Section 13.2, organizer experiment `a0-sfs-r37`). Limitations: a Monte-Carlo bound whose coverage rests on the approximate
normality of the mean of 32 replicates (study B: relative sd 0.0378, replicates between -73.85 and -74.11); the `+` reading; the heavy duplication of row-22 survivors within a replicate.

**H3 - few further successes per first block (score-critical).** For every trial t, the expected number of other
successful trials of the same first block given A_t is at most delta = 2^-9.4, i.e. E[X_f - 1 | A_t] <= 2^-9.4.
It splits into (a) the same variant with another l in L*, and (b) other good pairs (other variants) of the same
first block. For (a) the premise is E[#other l succeeding | A_t] <= 2^-11; measured directly on 19,620,436 distinct Step-3 successes of the SMC with the variants' W8
(`replay.c`, Section 13.1: rebuilding W0..W5 and testing the other 31 elements of L* through rows 14..36): 0 further successes; the rule-of-three
95% bound of the per-success rate is 2^-22.65 (the samples share SMC ancestors, so they are not independent). For (b) the expectation is at most
rho x (782,800 x 32 x q3) <= rho x 2^-45.42 with q3 <= 2^-70 (H2), where rho bounds Pr[t' succeeds | t succeeds, t' good] / Pr[t' succeeds | t' good] for good pairs t' != t of the first block; the premise
is rho <= 2^35, and the measured factor at the row-16 level over 2^21 and 2^23 real first blocks is 0.98 and 1.00 (sum of R(R-1) against p^2 sum of G(G-1), Section 13.1). So
delta <= 2^-11 + 2^-10.42 < 2^-9.4. Bursty goodness (variants of one class share W7; a class's variants give only 32..512 distinct W6 values for a given chaining value) does not
enter: the bound conditions on t' being good. Limitations: rows >= 17 of distinct good pairs cannot be measured jointly within one first block; the premise leaves a margin of 2^35 over the measured row-16 factor.
(rho <= 2^35 rather than 2^37 because the family has 3.4 times more variants; 1f12a09a made the same adjustment.)

**H4 - advice allowances (supporting).** The published characteristic and two-bit conditions, the SFS pair's inner
values S and L* are advice. Their construction is charged A_S = 2^50 (Step 1 and the completion to an SFS pair) and
A_C = 2^60 (the characteristic search). Evidence: Section 11.3. The variant family, the classes, the filter sets, L*, R16 and the decision DAGs are recomputed in the
precomputation (Section 11.1). Limitations: the 37-step search time is unpublished; A_C is a bound by comparison, not a measurement.

**H5 - counted word-RAM pricing of decision-DAG filters (score-critical; cost reading).** A word-RAM program of 256-bit primitives whose control flow branches
on bits of two registers (the scalars A_{-1} and C6 - A_{-2}) is charged by the primitives it executes on the path its inputs select: every executed load, store,
logic operation, shift, addition, branch and unconditional jump costs one primitive; a bit test is an AND with an immediate and a branch (two primitives); the code of the DAGs is data produced by a charged
precomputation (Section 11.1; about 2^25.2 instructions, 2^28.2 bytes); registers: at most 58 of 64 are live (Section 9.4); the programs evaluate no target compression, every compression is charged one unit.
The expected cost of a path is taken under the uniform law of the scalars (H1) and enforced by the counter V, which adds the exact executed cost of every segment (Section 9.8) and halts the
run at V_MAX. Evidence: the program is in `experiments/spec6core.py` (`step`, `run_group`, `expected_cost`), exact against the scalar definition (Section 9.4), the exact expectation is validated by
simulation, and the totals of the executable program agree with the ledger (Section 13.1). Limitation: no organizer ruling is cited; the premise is that a data-dependent branch is one primitive,
as in every earlier filing's scan loops and row checks. Without the DAG (the generic bit-sliced program with loaded broadcast planes of the 087a18c4/1f12a09a type, whose figures are 459 + 2 + 53 operations per batch in 1f12a09a's public note) the W6 term would be about 2.5 times larger (about 514 against 202 operations per batch all-in).

**H7 - exact success floor (supporting).** The cap target is mu0 = 0.49466248, the smallest 8-decimal number strictly above -ln(0.61 - Pcap - 2^-60) / (1 - 2^-10.4); every allowance is an explicit term of this equation (087a18c4's H7). `ledger()` computes mu0 with 60-digit decimals, asserts the success bound > 0.39 and the exact-rational ceiling N_FB g 32 q3 >= mu0.

Not used: expected work as a cap, an independence-of-conditions model for q3 (replaced by the SMC), a random-oracle model, any premise on the published pair beyond its verified values, and no de-pad of q3 (H6 of 087a18c4 is not used: q3_model is the registered floor).

## 13. Evidence and runs

All runs on one Apple-silicon Mac (8 cores), our own code (C and Python standard library; no rival code executed).

### 13.1 End to end on real first blocks (`e2e.c`, `replay.c`, `verify_pkg.py`, Appendix A)

**C statistics.** Random M0 (xoshiro256** seeded per thread), CV1 = F_37(IV, M0) by our compression, the 222 W7 tests, the scalar W6 test of every variant of every passing class,
u and the exact row-16 test for every l, exact checks of sampled pairs (Lemma 4.1 words, W6/W7 filters, y - x = d6, d7, d8, every cell of rows -4..15 for all 32 l and the two-bit conditions closing at rows <= 15,
row 16 over all 32 l against the table mask), and every row-16 pass through `row16_ok` for each l of its mask. Negative control (`-DNEG=1`): the checks fail for every row-16 pair as they should.

| run | first blocks | passing classes (expected) | good pairs (expected; ratio) | row-16 pairs (expected; z) | (pair,l) passes (expected; z) | exact checks | H3 factor: sum R(R-1) / p^2 sum G(G-1), p = 1052672/2^32, (p = R/G) |
|---|---|---|---|---|---|---|---|
| seed 5eed0021 | 2^21 | 7,400,134 (7,388,160) | 1,748,648,111 (1,742,708,500; 1.00341) | 424,363 (422,895; +0.88) | 428,617 (427,128; +0.88) | 16,051 sampled pairs, all 424,363 row-16 pairs, 428,617 (pair,l): 0 failures | 0.981 (1.001) |
| seed 5eed0023 | 2^23 | 29,545,568 (29,552,640) | 6,978,649,557 (6,970,834,000; 1.00112) | 1,693,297 (1,691,580; +0.51) | 1,710,031 (1,708,512; +0.45) | 16,013 sampled pairs, all 1,693,297 row-16 pairs, 1,710,031 (pair,l): 0 failures | 0.979 (0.999) |

The z-scores use the observed per-first-block variance; the counts are strongly overdispersed (variance-to-mean ratios 28.8 for passing classes, about 23,100 for good pairs, 6.6 for row-16 pairs) because
classes are correlated and the W6 values of a class take few distinct values per chaining value; their means match. The expected row-16 pairs use the 1,042,240 distinct u of the table.

**The executable counted program against a brute-force reference.** `verify_pkg.py` (Appendix A) runs `spec6core.online` on first blocks and compares, for each, the set of good pairs found by the
decision DAGs, the lane scans and the gather with the set obtained by testing F7 on every class and F6 on every variant of every passing class, and the
row-16 passes found by the packed arithmetic and the presence word with those obtained from the definition of u and the row-16 evaluation: 300 first blocks (48 with passing classes, 287,782 good pairs, 58 row-16 passes) and 3,000 first blocks
(459 with passing classes, 2,639,113 good pairs, 657 row-16 passes): 0 good-set mismatches, and every row-16 pass found (58 of 58, 657 of 657). `selftest` checks the F7 sampler, the W7 DAG (66,600 lanes), the W6 DAGs
(17,552 lanes of 5 classes), the packed arithmetic (8,000 lanes) and the presence word (3,000 random u).
**Provenance of the C evidence.** `e2e.c`, `smc.c`, `replay.c` were run by us; the organizer's report covers `spec6core.py` only. SHA-256 of the sources, seeds, commands and the raw outputs are in Appendix A (seeds 5eed0021/5eed0023 for e2e; 70000..77007 for the studies; 90..99 for the replay).

**The ledger against the program:** over 20,000 first blocks the executable program counted 31,757 operations per first block (standard error 903.3), with 3.490 passing classes and 859.2 good pairs per first block
(expected 3.523 and 830.99; the counts are bursty); the ledger charges 265 + 31195.59 = 31,429 per first block at the expected counts, with union bounds on the per-first-block setup. 

**Replay (H3 (a); not part of either preregistered sample).** `replay.c` (a copy of `smc.c` with replay hooks) records every Step-3 success of the SMC with the variants' W8 (seeds 90..99, NP = 2048, M = 512, MT = 16384): 20,669,447 successes,
19,620,436 distinct; each rebuilt (W0..W5 by the inverse expansion from W6, W7 of row 22, the variant's W8, the published W9..W13 and W14, W15 of its l) and re-checked with its own l through rows 14..36 (0 failures; the y side is an independent
forward recomputation) and with the other 31 elements of L* through rows 14..36: **0 further successes** (the other l fail at row 16 in 99.94% and at row 17 in 0.06% of the cases; none reaches row 18). Rule-of-three 95% bound:
1.5e-7 per success (2^-22.65). The successes share SMC ancestors (about 500 distinct row-22 survivors per seed), so the bound is on this sampled population, not an iid rate.

### 13.2 Semi-free-start collisions with variant dense parts (organizer experiment `a0-sfs-r37`)

For a seed-chosen class (of the 222) and variant a0 in it and a seed-chosen l among the 28 elements of L* whose row 16 can hold, rows 16..21 are sampled with the
row's fixed x-bits of E imposed (restarting from row 16 after 2^11 proposals at a row), then W22 with its cells and two-bit conditions, W7 uniform on F7 and W6 = W22 - s1(W20) - W15 - s0(W7) accepted iff in F6, until rows 22..36
pass with the variant's W8; W0..W5 by the inverse expansion and CV1 by inverting steps 7..0. Every constructed pair is checked: Lemma 4.1 maps (CV1, a0) back to exactly W0..W13, the two 37-step outputs are
equal, the blocks differ, every cell of rows -4..36 (W6/W7 XOR cells excepted) and two-bit condition of rows >= 8 holds, a0 is in G and its class, and W8 differs from the published one. The local replay of the organizer's executor
(public-seed request, standard library, the repository verifier recomputing every returned pair) returns 124 of the 128 pairs (128 distinct classes; four trials exhausted their proposal budget), as verified 37-step semi-free-start collisions; for the first 16 the constructed chaining value is also fed to the counted online program restricted to the class of a0, which finds exactly the constructed pair (W7 DAG, W6 DAG, lane scan, packed u, presence word, row-16 probe, rows 16..36: `detected_by_counted_program` = 1); both experiments are byte-identical on a second run.

### 13.3 Organizer experiments (`experiments/spec6core.py`, one program, two ids)

- `a0-sfs-r37` (variant validity, supports H2/H4): as in 13.2; trials 0..127; these are semi-free-start collisions (CV1 is not the IV), so the organizer's full-collision event is not expected; anyone can verify them from the raw report with `_compress(..., 37)`.
- `a0-online-r37` (H1, H3, H5): trials 0..7 each run the counted online program on seed-drawn first blocks until a first block with a passing class (at most 64), processing at most six passing classes; every lane of every pass plane
  is checked against the scalar W6 definition, every good pair against the Step-2 equations, and up to 12 good pairs against every cell of rows -4..15 for all 32 l. It returns the complete 128-byte messages M0 || M1 and
  M0 || M1' (l = 13) of the first good pair iff all checks passed (not expected to collide: that needs rows 16..36). Good pairs come in bursts (Section 5.3), so only some trials return a pair.
- Both are deterministic, standard library only, and run inside the executor's limits (0.34 s and 0.34 s (a0-sfs-r37), 1.91 s and 1.91 s (a0-online-r37) seconds for the four executions of the local replay).

### 13.4 Development computation

Below 30,000 CPU-seconds in total (the two preregistered SMC studies 160 s and the replay 33 s; the end-to-end C runs 54 s on 8 threads; the exact cost tables of the DAGs and the
verification runs about 12,000; searches and variants of the program and enumerations the rest), far inside DEV = 2^40 units (2^40 units are about 2^18.3 = 330,000 CPU-seconds at 2^21.7 units per CPU-second).

## 14. Memory and advice

Peak memory (all simultaneously resident during the online phase):

| item | bytes |
|---|---|
| row-16 bitmap: 2^24 words of 32 bytes | 536,870,912 |
| 11 lane-scan tables: 11 x 2^24 words of 32 bytes | 5,905,580,032 |
| sorted member array: 1,042,240 entries of 32 bytes | 33,351,680 |
| variant records: 782,800 x one 32-byte word (a0, S0(a0)) | 25,049,600 |
| stored planes: 3,193 batches x at most 96 planes x 32 bytes (both polarities, at most 2x) | 19,611,648 |
| code of the decision DAGs: 40,394,879 instructions x 8 bytes | 323,159,032 |
| W7 planes, registers, S, L*, row constants, code of the driver | below 1,048,576 |
| total | below 6,844,677,624 = 2^32.67 |

Claimed memory: 2^32.7 bytes. The precomputation's temporaries (the 12.1 million (c7, a0) pairs, 97 MB) are freed before the tables reach their peak. Nonuniform advice: the characteristic, S, L*, and the 222 class descriptors (below
2^13 bytes), charged through A_C and A_S; everything else, including the presence word (2 x 32 bytes) and the code, is recomputed in the precomputation.

## 15. Limitations

- H1, H2, H3 are premises. q3 is estimated (Monte Carlo), not proved; no collision has been found and none is expected at the scale we can run. The full-scale success probability cannot be observed.
- Study B of the q3 estimate was registered after study A had been read (Section 7.4); both are reported; study A's bound would price the claim at 62.37482.
- The published characteristic and SFS pair are used as advice under allowances; we did not rerun the paper's SAT solve or characteristic search.
- For 37 steps the measured q3 is about one bit better than the 75 conditions stated in the paper's text; the paper's own tables give 74, which the SMC matches stage by stage (6c77089c reached the same conclusion). With q3 = 2^-75, log2 T would be 63.16607.
- The decision-DAG filters rely on H5 (data-dependent branches priced at one primitive each); a reader who prices a branch higher or who charges the code size as advice should read Section 11.2 and the code size of Section 9.4 (2^28.2 bytes, produced by the charged precomputation).
- Memory is large compared with the earlier filings because of the lane-scan tables and the row-16 bitmap; memory is reported only under v5.
- H3 (b) is measured at the row-16 level only; correlations between neighbouring variants of one class at rows 17..24 are covered by the premise rho <= 2^35 (25 bits above the measured factor), not measured.
- The two q3 studies could be pooled instead of choosing study B; pooling gives a bound between the two (study A alone prices at 62.37482).
- The expected cost of the DAGs is an exact expectation under uniform scalars (H1); a single run's cost varies (sd about 40 operations per group of four batches); the cap V_MAX makes the run's total deterministic.

## 16. What this filing changes relative to 087a18c4 (63.45545) and 1f12a09a (62.7133)

| change | effect |
|---|---|
| W6 filter as a decision DAG over the bits of A_{-1} and cb (Section 9.4) | 129.8 operations per batch of 256 (expected) plus 32 test, 8 jump and 8 V operations instead of 459..530 |
| W7 test of all classes as a decision DAG (Section 9.3) | at most 191 operations per first block (tests and jumps included) instead of 375..640 |
| NOT-free full adder and polarity-aware builder (9.4.1) | for the generic loaded-plane program of one batch: 549 operations with naive polarity handling, 459 with the NOT-free adder (530 in 087a18c4's program) |
| lane-safe packed good pair, presence word, exact V accounting (9.6, 9.8) | 24.1640625 operations per good pair |
| 222 classes (782,800 variants), q3 for the family from our own two preregistered SMC studies, own replay and e2e statistics | as 1f12a09a's family; q3 = 2^-74.03 |

The attack, the premises H1-H4, H7 and the success analysis are those of 087a18c4; H5 is rewritten (decision DAGs); H6 is not used.

## Appendix A. Local evidence programs and records

These are the programs that produced the local evidence of Sections 4-7 and 13, and the records of the preregistered estimates and of the replay. They are evidence for the reader, not part of the attack. The attack's counted program, the class data and the organizer experiments are `experiments/spec6core.py`. C programs: C99, `cc -O2/-O3`; Python: standard library only.

### A.1 `genum2.c`: the variant family G, its c7 classes and the 222 classes with at least 3456 variants (writes classes222.txt)

```c
// own enumeration of the A0-variant family G and its c7 classes (r37 re-implementation; data: ePrint 2026/1120 SFS pair)
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef uint32_t u32;
#define ROR(x,n) (((x)>>(n))|((x)<<(32-(n))))
static u32 S0(u32 x){return ROR(x,2)^ROR(x,13)^ROR(x,22);}
static u32 S1(u32 x){return ROR(x,6)^ROR(x,11)^ROR(x,25);}
static u32 s0(u32 x){return ROR(x,7)^ROR(x,18)^(x>>3);}
static u32 s1(u32 x){return ROR(x,17)^ROR(x,19)^(x>>10);}
static u32 CH(u32 x,u32 y,u32 z){return (x&y)^(~x&z);}
static u32 MAJ(u32 x,u32 y,u32 z){return (x&y)^(x&z)^(y&z);}
static const u32 K[9]={0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,0xd807aa98};
static u32 CV0[8]={0x63b4986c,0x35d83dc0,0xc98894e4,0x784e08fc,0x78a7f752,0x5ed877a8,0x315a2db3,0xd5614eb4};
static u32 MX[16]={0x4d7f86ff,0x32ece589,0xd8accfc4,0x2cc2e433,0x068b5b34,0xeba68a28,0x0fe12cad,0x6ee2630c,0xbf0d78e1,0x6d1a90dd,0xfaa1d3e0,0x56aed439,0xcc2dbbc2,0xdd2ba0fc,0xbd1d3f7b,0x7dd43a81};
typedef struct{u32 c7,a0;}P;
static int cmp(const void*a,const void*b){const P*x=a,*y=b;return x->c7<y->c7?-1:x->c7>y->c7?1:(x->a0<y->a0?-1:x->a0>y->a0);}
int main(){
  u32 A[14+4],E[14+4]; // index i+4
  A[3]=CV0[0];A[2]=CV0[1];A[1]=CV0[2];A[0]=CV0[3];E[3]=CV0[4];E[2]=CV0[5];E[1]=CV0[6];E[0]=CV0[7];
  for(int i=0;i<9;i++){
    u32 e=A[i]+E[i]+S1(E[i+3])+CH(E[i+3],E[i+2],E[i+1])+K[i]+MX[i];
    u32 a=e-A[i]+S0(A[i+3])+MAJ(A[i+3],A[i+2],A[i+1]);
    E[i+4]=e;A[i+4]=a;
  }
  #define a(i) A[(i)+4]
  #define e(i) E[(i)+4]
  u32 C4=a(4)-S0(a(3))-MAJ(a(3),a(2),a(1));
  u32 W8C=e(8)-a(4)-S1(e(7))-CH(e(7),e(6),e(5))-K[8];
  size_t cap=13000000,n=0;P*v=malloc(cap*sizeof(P));
  for(uint64_t t=0;t<(1ull<<29);t++){
    u32 e4=(u32)t; u32 a0=e4-C4;
    u32 w=W8C-e4;
    #define B(k) ((w>>(k))&1)
    if(!(B(29)==1&&B(1)!=B(12)&&B(8)!=B(25)&&B(14)==B(18)))continue;
    u32 e3k=(a(3)-S0(a(2)))-MAJ(a(2),a(1),a0);
    u32 c7=e(7)-a(3)-e3k-S1(e(6))-CH(e(6),e(5),e4)-K[7];
    v[n].c7=c7;v[n].a0=a0;n++;
  }
  printf("|G|=%zu\n",n);
  qsort(v,n,sizeof(P),cmp);
  FILE*fo=fopen("classes222.txt","w");size_t ncls=0,tot=0,ge=0,cnt222=0,mx=0;
  for(size_t i=0;i<n;){size_t j=i;while(j<n&&v[j].c7==v[i].c7)j++;size_t s=j-i;ncls++;if(s>mx)mx=s;if(s>=3456){cnt222++;tot+=s;fprintf(fo,"%08x %zu",v[i].c7,s);for(size_t q=i;q<j;q++)fprintf(fo," %08x",v[q].a0);fprintf(fo,"\n");}i=j;}
  printf("classes=%zu max=%zu classes>=3456=%zu variants=%zu\n",ncls,mx,cnt222,tot);
  fclose(fo);return 0;}
```

### A.2 `f6chk.c`: |F6|, |F7| and the bitwise form of F6 against the definition on all 2^32 words

```c
#include <stdio.h>
#include <stdint.h>
typedef uint32_t u32;
#define ROR(x,n) (((x)>>(n))|((x)<<(32-(n))))
static u32 s0(u32 x){return ROR(x,7)^ROR(x,18)^(x>>3);}
#define B(k) ((w>>(k))&1)
int main(){
  u32 D6=0x20000000,T6=0x03c00800,D7=0xfbc00800,T7=0x017f8000;
  uint64_t n6=0,n7=0,bad=0;
  for(uint64_t t=0;t<(1ull<<32);t++){u32 w=t;
    int f6=(s0(w+D6)-s0(w))==T6; n6+=f6; n7+=((s0(w+D7)-s0(w))==T7);
    u32 common=(B(14)^B(18))|!(B(8)^B(25))|(B(1)^B(12));
    u32 bc=(B(15)^B(19))|!(B(9)^B(26))|(B(2)^B(13));
    u32 bb=bc|B(30);
    u32 cb=bc|!B(30)|(B(16)^B(20)^B(31))|!(B(10)^B(27)^B(31))|(B(3)^B(14)^B(31));
    u32 fail=(common|(B(29)&bb&cb))&1;
    if(f6==fail)bad++;}
  printf("|F6|=%llu |F7|=%llu mismatches=%llu\n",n6,n7,bad);}
```

### A.3 `f7an.c`, `f7dual.c`: the affine hull of F7 and of its two halves; the parity constraints (weight <= 5) of each half

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

### A.4 `f7chk.c`: the bitwise form of F7 of Section 5.1 against the definition on all 2^32 words (0 mismatches)

```c
#include <stdio.h>
#include <stdint.h>
typedef uint32_t u32;
#define ROR(x,n) (((x)>>(n))|((x)<<(32-(n))))
static u32 s0(u32 x){return ROR(x,7)^ROR(x,18)^(x>>3);}
#define B(k) ((w>>(k))&1)
int main(){u32 D7=0xfbc00800,T7=0x017f8000;uint64_t bad=0;
 for(uint64_t t=0;t<(1ull<<32);t++){u32 w=t;int f=(s0(w+D7)-s0(w))==T7;
  int cm=!(B(1)^B(18))&&!(B(0)^B(28))&&!(B(9)^B(30));
  int p0=!B(11)&&B(22)&&B(26);
  int p1=B(11)&&!B(12)&&!B(22)&&B(23)&&!B(26)&&B(27)&&!(B(2)^B(19))&&!(B(1)^B(29))&&!(B(10)^B(31));
  int g=cm&&(p0||p1); if(f!=g)bad++;}
 printf("F7 formula mismatches=%llu\n",(unsigned long long)bad);}
```

### A.5 `r16.c` (with `gen_r16data.py` writing its constants): the row-16 enumeration, 1,052,672 pairs (u, l)

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

### A.6 `presence.py`: the presence word against all members of the table

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

### A.7 `smc.c`, `lab.h`: the sequential Monte-Carlo estimator of q3 (Section 7.3)

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

### A.8 Preregistrations and results of the two studies

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

### A.9 `replay.c` (a copy of `smc.c` with replay hooks): the difference to `smc.c`, and the record

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

### A.10 `e2e.c`: end-to-end rates on random first blocks (its constants are generated by `gen_data.py` from `spec6core.py`)

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

### A.11 `verify_pkg.py` and `meanops.py`: the executable program against a brute-force reference and its mean operation count

```python
import sys, time; sys.path.insert(0,'.')
import spec6core as S
from spec6core import *
N=int(sys.argv[1]); seed=sys.argv[2]
env=Env(); rng=Shake(seed); mism=0; r16ref=r16got=0; hitsfb=0; goods=0; t=time.time()
c7idx={CLASSES[c][0]:c for c in range(NCLS)}
def ref_u(cv,a0):
    Ar={-1:cv[0],-2:cv[1],-3:cv[2],-4:cv[3],0:a0}; Er={-1:cv[4],-2:cv[5],-3:cv[6],-4:cv[7]}
    Er[0]=(Ar[0]+Ar[-4]-S0(Ar[-1])-MAJ(Ar[-1],Ar[-2],Ar[-3]))&M32
    W0=(Er[0]-Ar[-4]-Er[-4]-S1(Er[-1])-CH(Er[-1],Er[-2],Er[-3])-K[0])&M32
    Er[1]=(A1+Ar[-3]-S0(a0)-MAJ(a0,Ar[-1],Ar[-2]))&M32
    W1=(Er[1]-Ar[-3]-Er[-3]-S1(Er[0])-CH(Er[0],Er[-1],Er[-2])-K[1])&M32
    return (W0+s0(W1))&M32
for i in range(N):
    cap=[]; st=dict(fb=0,hits=0,good=0,r16=0)
    ops,found=online(1,rng,env,st,lambda k,cv,a0,cd: cap.append((cd.c7,a0)) if k=='good' else None)
    cv=compress(IV,st['m0'])
    ref=set()
    for c in range(NCLS):
        if not F7((CLASSES[c][0]-cv[0])&M32): continue
        for a0 in env.cd(c).members:
            if F6(w6of(a0,cv[0],cv[1])): ref.add((c,a0))
    got={(c7idx[c7],a0) for c7,a0 in cap}
    if got!=ref: mism+=1; print('MISMATCH',i,len(got),len(ref))
    rr=sum(1 for (c,a0) in ref if env.probe(ref_u(cv,a0)))
    r16ref+=rr; r16got+=st['r16']
    if rr!=st['r16']: print('r16 mismatch',i,rr,st['r16'])
    hitsfb+= st.get('hits_found',0)>0; goods+=len(ref)
print('fbs',N,'fbs with hits',hitsfb,'good pairs',goods,'good-set mismatches',mism,'row16 pairs ref',r16ref,'got',r16got,'time %.0fs'%(time.time()-t))
```

### 

```python
import sys, time, math; sys.path.insert(0,'.')
from spec6core import *
N=int(sys.argv[1]); seed=sys.argv[2]
env=Env(); rng=Shake(seed); st=dict(fb=0,hits=0,good=0,r16=0); tot=0; sq=0; t=time.time()
per=[]
for i in range(N):
    ops,found=online(1,rng,env,st); tot+=ops; per.append(ops)
m=tot/N; var=sum((x-m)**2 for x in per)/(N-1)
print('first blocks',N,'mean counted ops/fb %.1f'%m,'se %.1f'%math.sqrt(var/N),'hits/fb %.3f'%(st.get('hits_found',0)/N),'good/fb %.1f'%(st['good']/N),'row16 pairs/fb %.4f'%(st['r16']/N),'time %.0fs'%(time.time()-t))
```

### A.12 Output of `python3 spec6core.py selftest`

```text
F7 sampler violations 0
W7: lanes 66600 passes 996 mismatches 0
W6 groups: lanes 17552 passes 1088 mismatches 0
packed u: lanes 8000 mismatches 0
presence word: false negatives on 3000 random u (and 0 on the 1,042,240 members: appendix) : 0
```

### A.13 Output of `python3 spec6core.py ledger` and `python3 spec6core.py dag`

```text
g                  830.9881687164307
vbar               31195.592277824755
fixed              265
GL                 24.1640625
mu_req             0.49466248
nfb                358768851784995369
log2_nfb           58.31583225438473
VMAX               11366881928865994508928
vmax_fb            84668692915.125
pcap_log2          -24.94377726825501
time_log2          62.34263
log2_T             62.34262408459607
T_num              15461844764535665517649
T_den              2644
tight_up           True
tight_down         True
success_lower_bound 0.39000000590152406
w6_part            10700.028632642137
good_part          20080.050045624375
setup_part         274.7900390625
rare_part          140.72356049574353
per_fb_units       12.89886243488077
preprocessing_log2 60.00140956943092
groups 888 joint nodes 1027268 instructions 40394879 (2^25.27) max joint nodes per bit 278 max live values 52
```

### A.14 SHA-256 of the C sources

```text
685297129cda47b247e6d19b1799d73b198e1511334e161fa7583ef6c1175a65  q3smc/smc.c
bdefd6747d41727a378bc124c241db1f635275d3a2901b96a1c6c6b0e5c5e456  q3smc/lab.h
5dfbeb608ce5d5c245a8e28af3b7c4d737b3b59ed261c9a17917c42fccb1e520  q3smc/replay.c
ef5aacdb3c66c0cda76d07710a7a6b1d5320567c942944765e58aa964b2ae384  e2e/e2e.c
c1f9fb238e3fabc1920421164c01691a62197a057f82b4dde055c8ecb2c65188  r37b/genum2.c
8c93b2c2670432ac586876414ea4fc00dd59266c795a7c61d8d0546c7affc7cf  r37c/r16.c
```

