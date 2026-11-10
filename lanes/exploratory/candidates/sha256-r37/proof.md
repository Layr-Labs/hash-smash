# Collision attack on 37-step SHA-256: the ePrint 2026/1120 two-block attack over the whole variant family G, with an x-indexed table of merged W6 fibres, 2^61.19411

Track `sha256-r37-exploratory`, target `sha256-r37-prefix-v1`, cost model `collision-frontier-v5` (C = 2644).
Claim: `time_log2 = 61.19411` target compressions on every run, success probability at least 0.39 (0.3900000013 under the stated premises),
memory 2^53.0 bytes (reported only), nonuniform advice below 2^13 bytes.

The attack is the 37-step collision attack of Li, Zhang, Li, Liu, Qian and Zhu, "Pushing Collision Attacks on SHA-2 to 39 Steps" (IACR ePrint
2026/1120, CC BY), in the two-block framework of [LLWS26] (ePrint 2026/1080), with the A0-variants of its Step-1 solution (itseasypop 1c368173,
qkniep b947b377), the packed good-pair stage of 1f12a09a, the exact-rational ledger of 087a18c4 and the program structure of 7319bba (all declared as
dependencies). It builds on this filer's d3ec5c41 (61.71473) and on three derivatives of it that were filed afterwards and are credited below
(8aeaed1c, def128fc, f2fe1d4d). **What this filing changes is the counted online program, its precomputation and the set of variants it examines, not the attack.**

*The idea.* The 32-bit value x = A_{-1} of a chaining value takes only 2^32 values, while the run draws about 2^55 first blocks: every x recurs about 2^23 times.
Everything that depends on x alone is computed once for all x (charged preprocessing, below 2^58 operations; memory is a reported metric only) and read online:
(i) the W7 class test becomes one table read; (ii) the values phi(a0, x) = W6x - cb of **all** variants whose c7-class passes W7 at x are partitioned into **fibres** of equal value, whatever their class;
(iii) only fibres of at least THETA = 40 variants are kept; (iv) online, the W6 filter is one bit-sliced 32-bit addition of the scalar cb to the fibre values of 256 lanes followed by the F6 test, and the members of
every passing fibre are read in place by the packed 4-lane stage. Before, the table was restricted to the 222 largest classes (782,800 variants) and fibres were per class (about 12 variants each);
the lower per-pair cost of large fibres makes it worthwhile to examine 122,253 variants per first block (on average) out of the whole family G (12,103,680 variants in 22,976 classes), so a first block yields
8,129 good pairs instead of 831 and N_FB falls by a factor of about 9.4 while the work per good pair falls too. The set of good pairs found among the examined variants is *exactly* the set defined by the
filters (Lemma 8.1, checked against brute force in Section 13).
**Inheritance, stated up front:** the Monte-Carlo estimate of q3 (premise H2) and the evidence for H3 are 7319bba's and were *not* re-run for this filing; q3 is defined as the mean over a family of variants, and this filing's examined family
is a different subset of the same family G (H2 explains why the dependence on the variant is a tail factor of 2^-4, and prices a hedge of 0.05 bit).

## 0. Summary

- **Algorithm (Sections 4-8).** Messages M0 || M1 and M0 || M1' (128 bytes; padding adds the same third block). A first block M0 is two fresh uniform 256-bit
  words; CV1 = F_37(IV, M0) costs one unit. One table read at x = A_{-1} returns the record R(x): the kept fibres (at least THETA = 40 variants with equal phi) of the variants of G whose class passes c7 - x in F7, as
  bit planes of the fibre values, fibre entries and contiguous member blocks. For each batch of 256 fibres the program adds cb = C6 - A_{-2} to the fibre values bit-sliced and applies F6; the members of each passing fibre are good pairs.
  They are processed in packed groups of four: u = W0 + s0(W1) and an exact row-16 mask-table lookup over the 32 elements of L* for every lane; each row-16 pass is checked through row 36. A pair that follows
  every cell of rows 16..36 collides; it is verified with the target and output.
- **Rates.** Per first block (means over uniform x, Tungsten, Section 13.3): 1,221.4 kept fibres, 122,253 kept variants, hence g = p6 x 122,253 / 1.006 = 8,129 examined good pairs (a lower bound)
  (p6 = |F6|/2^32 = 2^-3.90197; the statistics are scaled by 1.006 in the unfavourable direction).
- **Probability (Section 7, H2).** q3 = average over the examined variants and l in L* of Pr[rows 16..36 follow every cell and printed two-bit condition]
  = at least 2^-74.08 (the registered floor of the preregistered studies of 7319bba, Section 7.4, study B registered bound less the hedge of Section 7.6; not re-run here).
- **Cost (Sections 9, 11).** N_FB = 38,017,119,869,886,130 first blocks (2^55.07750); per first block 1 unit plus 264 counted data-independent operations, plus on average
  100,186 counted data-dependent operations (1,931 for fibre tests and scans, 96,113 for the packed groups and row-16 lookups, 1,156 for rows >= 16), capped by V_MAX. T = A_C + A_S + DEV + N_FB + (N_FB x 264 + V_MAX + overshoot + preprocessing + final)/C + 6 = 1,743,664,078,045,309,331,687 / 661 = 2^61.194106,
  claimed 61.19411. The earlier best on the board is 61.51197 (f2fe1d4d); this filer's d3ec5c41 is 61.71473.
- **Premises (Section 12).** H1 uniform independent chaining values; H2 q3 >= 2^-74.08 for the examined family (inherited, not re-run); H3 given one success, at most 2^-9.4 further expected successes in the same
  first block (inherited, stated for the new family); H4 advice allowances (A_C = 2^60, A_S = 2^50, DEV = 2^40, as in the accepted filings); H5 counted word-RAM pricing (every executed primitive costs one, address additions included; memory is reported only); H7 the exact success floor of 087a18c4;
  **H9 the table statistics and the preprocessing bound**. No decision-DAG branch pricing is used.
- **Checks (Section 13).** Exhaustive in Tungsten: |F6| = 287,309,824 and |F7| = 68,157,440 and their bitwise forms against the definitions on all 2^32 words (0 mismatches),
  |G| = 12,103,680 and its 22,976 classes; the table pipeline against brute-force filtering (selftest and organizer experiments, 0 mismatches); the fibre statistics over 3,200,000 uniform values of x (Tungsten, sixteen shards);
  an end-to-end Tungsten simulation of the counted program over 480,000 further values of x against the ledger; the executable counted program (Python) on real first blocks restricted to the 222 embedded classes; 37-step semi-free-start constructions with variants found by the counted program.

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
- Filings on this track (all declared as dependencies; 6eeefb64 belongs to the sha256-r32 track and is only cited for a measured price): 6c77089c (winglock, 74.22669): transcription of Tables 15-17, member orientation, the reading of '+', the corrected two-bit condition
  A15[29] = A17[29], the exact Step-2 sets F6, F7, the exact set L* (|L*| = 32), the SMC design for q3. dd6656d (Th0rgal): affine decomposition of F6, F7. 1c368173 (itseasypop) and b947b377 (qkniep):
  the A0 freedom of the Step-1 solution (the family G), the c7 classes. 087a18c4 (GordoAR): exact-rational ledger, premises H1-H5, H7, the first-block-level success analysis. 1f12a09a (0xshikhar):
  packed groups of four 64-bit lanes. 7319bba (winglock, 62.34263): the program structure, the packed good-pair program, the
  q3 studies for the 222-class family (Section 7.4), the end-to-end and replay statistics (Section 13.1, quoted), the registered allowances. 6eeefb64 (sha256-r32, promoted): the calibrated price of a solver CPU-second
  behind A_C. d3ec5c41 (this filer, 61.71473): the x-indexed table, fibres of equal W6 value, the bit-sliced fibre test, the exact ledger.
  Three later derivatives of d3ec5c41 contributed ideas that are re-derived and re-implemented here (no code of theirs was executed): 8aeaed1c (Jbenisek: the row-16 l-mask stored directly per value u, one load per lane instead of a bitmap probe and a binary search),
  def128fc (Jbenisek: no presence word; every lane looked up; the cap slack as the square in the Chebyshev bound; the count of cv_pre as executed), f2fe1d4d (Th0rgal: MAJ(a0, A_{-1}, A_{-2}) = (a0 & (A_{-1} ^ A_{-2})) + (A_{-1} & A_{-2}) with the second term folded into kap1; the
  unmasked first additions; the factoring of w[8] ^ w[25] out of the F6 test). Their operation counts were checked and some were not adopted (Section 9.4 and Section 16).
- **How the earlier material is used.** Sections 3-7 restate definitions and lemmas that all filings share (re-typed; every constant was re-derived or re-checked here, Section 13). The Monte-Carlo estimate of q3
  (Section 7.4) and the statistics of Section 13.1 were produced by 7319bba's author with programs reproduced in Appendix A.7-A.10; **I did not re-run them**, and they enter only as the premises H2 and H3.
  I did not execute any peer code: every program that ran for this filing was written for it (Python `experiments/xtab.py`, Tungsten sources of Appendix A.1-A.4 and A.12).
- **New here.** (i) The family G in full: all 22,976 classes, with fibres merged across classes and a size threshold (Sections 5.3, 8.1, 8.2); (ii) the per-fibre cost model that makes small fibres unprofitable (Section 11.4);
  (iii) the honest counting of addresses and scan operations that the earlier ledgers left implicit (Sections 9.1, 9.4, 9.5); (iv) the packed group at 32 operations plus 14 for the four lookups, with kap0 and the table base folded into one vector addition and the row-16 table stored three times, and segment loops unrolled by 8 (Section 9.6);
  (v) per-segment accounting of the work counter V (Section 9.8); (vi) the statistics of all x-averaged quantities by Tungsten sampling and an end-to-end Tungsten simulation (Sections 13.3, 13.4); (vii) the new ledger (Section 11).

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

### 5.3 The c7 classes; which variants are examined

c7(a0) takes only **22,976 distinct values on G** (7319bba's enumeration, inherited; re-derived here in Tungsten, Appendix A.4: |G| = 12,103,680, 22,976 classes of 2 to 3600 variants). A *class* is G intersected with one
value of c7. For all variants of one class and a given CV1, W7x is the same word, so one membership test decides the
W7 filter of the whole class. The earlier filings used the 222 classes with at least 3456 variants (782,800 variants; 1f12a09a's selection), because their W7 test was a decision DAG of 191 operations per class and their W6 filter ran over all variants of a passing class.
In the x-indexed table of Section 8 the W7 test is a table read and the W6 filter runs over fibre values, so the cost is per fibre and per good pair; **this filing examines the variants that lie in fibres of at least THETA variants** (Section 8.1),
taken from all 22,976 classes (on average 122,253 variants per first block). The 222 classes of the earlier filings stay embedded in `xtab.py` (descriptors below) because the organizer sandbox (128 MiB, 20 s) cannot hold the whole family:
the organizer experiments run the same program with the table restricted to these classes and a smaller THETA (Section 13.2). Each of the 222 classes equals {base XOR s : s subset of mask, s in G, c7 = the class value}
for the descriptors below (c7, base, mask, size; `xtab.py` regenerates all 222 classes from them and asserts the sizes):

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

Per first block over uniform x: every class passes W7 for exactly |F7| = 68,157,440 values of x, so the number of passing classes has mean 22,976 p7 = 364.6 and the number of variants in passing classes has mean
12,103,680 p7 = 192,075 (exact; the Tungsten sample mean of Section 13.3 is 192,590). Passing classes are strongly correlated (their c7 values are close), so the counts are bursty (the standard deviation across x is about twice the mean);
the expectations are exact where stated and sampled for the fibre statistics.

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
R16[u] = {l : C16_l + u passes row 16} is stored as **Rmask** (8aeaed1c's idea, re-implemented): 2^32 words of 256 bits (stored three times in a row, Rmask3, Section 9.6), where word u holds the l-mask of u (bit l is set iff u lies in R16_l, so the word is zero iff u is not one of the
1,042,240 members). A lookup is the add of the table base to u and one load. The bitmap, the sorted array with its binary search and the presence word of the earlier filings are not used. By Lemma 5.1 u is uniform for a good pair, so
Pr[row 16 for l] = |R16_l|/2^32 exactly, and Pr[u in R16] = 1,042,240/2^32.

For each l in R16[u] the program computes W2..W5 (Lemma 4.1), W8 = W8C - E4, the y-words, and rows 16..36 of both
members, checking every cell and printed two-bit condition of each row, aborting at the first failing row.

**Lemma 6.1.** If rows 16..36 follow every cell, the two second-block outputs are equal (rows 33..36 of A and E have
no difference and the chaining value is common), hence m = M0 || M1 and m' = M0 || M1' collide under the
complete target (FIPS padding appends the same third block to both 128-byte messages; M1 is a full data block, so
W14, W15 are free). m != m' because M1 and M1' differ (W6..W10, W14, W15).

## 7. The Step-3 probability for the variants (H2)

### 7.1 The quantity

For a good pair (CV1, a0) and l in L*, let F_l be the event that rows 16..36 follow every cell and every printed
two-bit condition closing at rows >= 16. q3 = average over the examined variants (Section 8.1; the variants of kept fibres, whose distribution over G is a function of x) and over l in L* of
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
difference, and checks the whole row; row 22: (W6, W7) drawn uniformly from F6 x F7; rows 23..36: W8 of a variant drawn uniformly from the 782,800 variants of the 222 classes of that time (the same row-22 survivor
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
61.18850 (Section 11.2).

### 7.5 Consistency

- Lemma 7.1 makes rows 16..22 identical by construction; the paired rows-23..36 rates of the variants' and the published W8 differ by 0.002 bit in study B (7319bba).
- Real first blocks (7319bba, quoted in Section 13.1): the row-16 pass rate of the attack's own good pairs is the exact 2^-12 (z = +0.88 and +0.51 over 424,363 and 1,693,297 passes).
  This filing's end-to-end run (Section 13.4) finds row-16 passes at the same rate (2.423e-04 per good pair).


### 7.6 The examined family of this filing (new; the premise H2 is stated for it)

The registered studies drew W8 from the 782,800 variants of the 222 largest classes. This filing examines a different subset of the same family G (the variants of fibres with at least THETA members, from all 22,976 classes).
By Lemma 7.1 a variant changes nothing in rows 16..22 and enters rows 23..36 only through W8, i.e. through the four conditions on W24x = Z + W8x; if Z were exactly uniform given rows 16..22 these four conditions would hold with probability exactly 2^-4 for *every* W8x
(W24x would be uniform), so q3 would be the same for every subset of G. The same holds one stage earlier: W7 enters rows 16..36 only through W22 = s1(W20) + W15 + s0(W7) + W6, whose x-conditions (row 22: 11 bits) hold with probability 2^-11 for every (W6, W7) if s1(W20) + W15 is uniform given rows 16..21. The examined pairs are not uniform on F7: x = c7 - W7 is selected, so the law of W7 among examined good pairs is weighted by the number of kept variants at x = c7 - W7 (and the same for W6 only through cb, which is independent). Both facts are premises, not measurements, for the new subset. The stage factor of that tail in the registered studies is 2^-4.015 (study A) and 2^-4.007 (study B) against the exact 2^-4, and the paired comparison with the published W8 differs by 0.002 bit: the dependence on W8 is below the sampling resolution.
The premise H2 is therefore stated for the examined family with a hedge: **q3_used = 2^-74.08**, i.e. 0.05 bit below the registered bound 2^-74.03, covering a tail factor and a row-22 factor that differ from the studies' by up to that amount for the new subset (the hedge was raised from 0.02 to 0.05 bit after a reviewer pointed out that the examined pairs weight W7 by the number of kept variants at x = c7 - W7). This is a premise, not a re-estimate: the SMC program of 7319bba was not run here (Appendix A.7), and no
claim is made that the new subset's tail factor was measured. Section 11.2 prices the hedge: removing it (q3 = 2^-74.03) lowers log2 T by 0.02787.

## 8. The algorithm: the x-indexed table and the fibre test

### 8.1 Fibres, kept fibres and the examined variants

For a variant a0 and A_{-1} = x define (Section 5.1, Lemma 4.1)

```text
phi(a0, x) = MAJ(A1, a0, x) - CH(E5, a0 + C4, E3)   (mod 2^32),   E3 = K3C - MAJ(A2, A1, a0) + x,       W6x = cb + phi(a0, x),   cb = C6 - A_{-2}.
```

(`xtab.phi`; it equals `w6of(a0, x, A_{-2}) - cb`, asserted in the selftest.) Let P(x) = {a0 in G : c7(a0) - x in F7} be the variants whose class passes the W7 test at x (the union of the passing classes). The **fibres** of x are the classes of P(x) with equal phi, *whatever their class*;
the **fibre value** is the common phi. A fibre is **kept** if it has at least THETA = 40 members; E(x) denotes the union of the kept fibres, the **examined variants** at x. Since cb is independent of x (H1), each fibre passes the F6 test independently of its size with probability exactly p6
whatever x is (cb + v is uniform).

**Lemma 8.1.** For a first block with A_{-1} = x and cb, the good variants among the examined ones (a0 in E(x) with W7x = c7(a0) - x in F7 and W6x in F6) are exactly the members of the kept fibres whose value v satisfies cb + v in F6. *Proof.* W7x = c7(a0) - x is in F7 for every member of P(x) by definition;
W6x of a member is cb + phi(a0, x) = cb + v, and F6 depends on W6x only. QED. (Checked against the brute-force definition over all variants of the passing classes in Section 13.2.)

The expected number of examined good pairs per first block is g = p6 E_x|E(x)| (Section 13.3); all later stages are those of the earlier filings. Which variants are examined depends on x only (a function of the table); the choice of THETA is a performance parameter, not a premise:
the online program is the same for every THETA, and the success analysis (Section 10) uses only g and q3.

### 8.2 The table (offline; charged preprocessing; memory reported)

**T0** is an array of 2^32 words indexed by x = A_{-1}: T0[x] is the address of the record R(x) (a record with zero batches if no fibre is kept). R(x) holds

- the number B of batches (B = ceil(F/256) for F kept fibres) and, for each batch, its cost word;
- **planes:** for each batch b the 32 planes dl[0..31] (256-bit words): lane L of plane j is bit j of the value of fibre 256 b + L (fibres in increasing value order); unused lanes of the last batch repeat lane 0;
- **entries:** for each fibre one 256-bit word (start address of its member blocks in lane 0, V cost in lane 1, end address in lane 2, lane 3 zero);
- **members:** two parallel arrays of 64-bit lanes with zero high halves, the values a0 and the values S0(a0) of the members of each kept fibre, contiguous and word-aligned, each fibre padded to a multiple of four members by repeating its last member (so every group of four is one word of each array and every lane of every group is a real member).

**Construction and operation bound.** For x = 0, 1, ..., 2^32 - 1: (i) decide c7(c) - x in F7 for the 22,976 classes by the bitwise form of Section 5.1 (at most 80 operations per class: 2^52.8 in all); (ii) for every variant of a passing class
(12,103,680 x |F7| = 8.25 x 10^14 pairs (x, variant) in all, 2^49.55, because each class passes for exactly |F7| values of x) compute phi (at most 32 operations) and sort the (phi, record) pairs by phi by a four-pass byte radix sort (per pair and pass at most 40 operations: the count, the prefix sums amortised, the scatter and the loop;
so at most 160 per pair), scan the sorted array once to cut the fibres (at most 8 per pair), write the kept fibres' records, entries and cost words (at most 16 per pair) and transpose the kept fibre values into planes (at most 96 operations per kept fibre; at most (1/THETA) per pair).
This is at most 256 operations per pair, 2^57.55 in all; (iii) writing T0 and the record addresses: 2^32 x 8 operations; (iv) Rmask: zeroing 2^32 words (4 operations each) and OR-ing the 1,052,672 enumerated pairs (u, l) (at most 10 each): below 2^34.1 (the enumeration itself is 7319bba's, below 2^38.7 operations, Section 11.1 there).
The total is below **PRE = 2^58 operations**, which is 2^46.6 target compressions (about 2^-14.6 of the score); all of it is included in T and in the claimed preprocessing. The program text is straight-line code of a few thousand instructions; no part of the table depends on cb or on any other word of the chaining value.

### 8.3 The online algorithm

```text
input: N_FB, V_MAX; precomputed: S, L*, the table T0 and the records R(x), the row-16 mask table Rmask3 (Rmask three times in a row), the 24-bit lane-scan tables
V = 0
for f = 1 .. N_FB:
    draw two uniform 256-bit words; M0 := their sixteen 32-bit fields; CV1 := F_37(IV, M0)                       [1 unit]
    p := T0[A_{-1}]; load B, plane address, entry address; if B == 0: continue
    cb := C6 - A_{-2}; z_j := all-ones if bit j of cb else 0, j = 0..31; the per-first-block constants of W0, W1  (cv_pre)
    for each batch b of R(p):
        pass := F6(dl + cb) of the batch                                                                         (Section 9.4, 230 operations; +1 for a partial batch)
        V += the cost word of the batch
        for each set lane L of pass (24-bit chunk scan): entry := entries[256 b + L]; V += entry.cost; segment (start, end)
            for each group of four records in [start, end): u := W0 + s0(W1) (packed, Section 9.6)
                for each of the four lanes: mask := Rmask[u]; if mask != 0:
                    recompute W6, W7; for l in mask: rows 16..36 with early abort
                        if all rows pass: build m, m'; if digest(m) = digest(m') and m != m': output, halt
    V += (the executed cost of the rare paths of the first block, Section 9.8); if V > V_MAX: halt (failure)
halt (failure)
```

### 8.4 What is *not* assumed

The table lookup returns the record of x; no property of x other than being a 32-bit word is used. Distinct first blocks with the same x share the record; this does not couple their
success events beyond what H1 already assumes, because the record is a deterministic function of x and the success event depends on the remaining coordinates of the chaining value (cb, A_{-3}, A_{-4}, E_{-1..-4}).
The padding lanes of a fibre's last group repeat its last member: a duplicated member is probed twice and a hit would be processed twice; this changes the cost (charged, Section 11.1) and not the set of pairs found.

## 9. The counted program

### 9.1 Machine and pricing

256-bit word RAM, 64 registers, every executed primitive counted (loads, stores and branches included). 32-bit values are kept in the low bits; a reduction mod 2^32 is one AND; a 32-bit rotation pattern (S0, S1, s0, s1) costs 8:
d = x | (x << 32) (2), three shifts and two XORs and one mask. A conditional branch tests a register for nonzero and an unconditional jump is one primitive (as in all earlier filings' scans); where a comparison must first produce the register it is counted separately (the table read at x: 5 operations including it). The branch on a looked-up mask, which is a register, is one operation; Section 11.2 prices the reading in which each of the four lookups needs a comparison first. The program text is straight-line code. The target compression of a first block
is one unit and its internal operations are not counted again. **Addresses.** Unlike the earlier ledgers, which left address arithmetic implicit in some places, every address that is not already a register value is formed by an add that is counted:
31 adds for the 32 plane loads of a batch, the batch pointers, the table-entry address of each set lane, the entry address, the table read at x. The row-16 table is addressed by the lane value a0 + s0(W1) + (RBASE + kap0): the per-first-block constant C = RBASE + kap0 is formed once (in cv_pre) and added to all four lanes by one operation, so no per-lane base add is needed (Section 9.6).
The executable counted program is `experiments/xtab.py` (`process_cv`, `w6_batch`, `good_group`, `mask_lookup`); its routines count every executed primitive of the routines below, and the ledger (`ledger`) is computed from them with exact rationals.

### 9.2 Fixed per first block: 264 operations

- First block words: 2 random words, then the 16 fields (field 0 of a word: and; fields 1..6: shr, and; field 7: shr): 30.
- Control allowance 16 (loop counter add and compare-branch, the cap test, further loop or address arithmetic not itemised elsewhere).
- The table read: address (add) 1, load 1, test and branch 2, plus 1 for the shift of the 8-byte entry index: 5 (`T0_OPS`); three loads of the record header (B, plane address, entry address): 3.
- cb (2), the 32 broadcast planes z_j = 0 - ((cb >> j) & 1) (2 for j = 0, 3 for j >= 1: 95), the per-first-block constants of the packed stage (`cv_pre`: 81 as executed: 4 + 11 + 3 + 16 + 5 for the constants, 28 for the broadcasts of the seven constants to four lanes and 14 for unpacking the chaining value from the compression output).

These are charged to every first block, also to those whose record is empty (which skip them): 30 + 16 + 5 + 3 + 2 + 95 + 81 + 32 = 264 (the last 32: the 32 broadcast planes z_j are stored once, because the group stage needs the registers, and reloaded per batch, below) (`FBFIX`).

### 9.3 Batch loop

Per batch: the loop counter, compare and branch (3), the plane pointer and the entry pointer (2), the cost word of the batch (address add, load, add to V: 3), and the reload of the 32 planes z_j (32 loads, 31 address adds: 63): 71 operations (`BATCH_OVH`). (During the group stage about 62 of the 64 registers are in use; the planes z_j cannot stay live.)

### 9.4 The fibre test of one batch: 230 operations

The batch holds the 32 planes dl[0..31] of up to 256 fibre values; the scalar cb is given by the planes z_j. The program computes w = dl + cb bit-serially with the NOT-free full adder carry = a ^ ((a ^ b) & (a ^ c)):

| step | operations |
|---|---|
| address adds for the plane loads (31 after the first) | 31 |
| loads of dl[0..31] | 32 |
| bit 0: c = dl[0] & z[0] (the sum bit w0 is not needed) | 1 |
| bits 1..30: xy = dl[j] ^ z[j], xz = dl[j] ^ c, carry = dl[j] ^ (xy & xz) (4); the sum w_j = xy ^ c (1) only for the 19 bits of {1,2,3,8,9,10,12,13,14,15,16,18,19,20,25,26,27,29,30} | 30 x 4 + 19 = 139 |
| bit 31: xy, w31 = xy ^ c | 2 |
| F6: common = (w14^w18) \| (w1^w12) (3), bc = (w15^w19) \| ~(w9^w26) \| (w2^w13) (6), X = (w16^w20^w31) \| ~(w10^w27^w31) \| (w3^w14^w31) (9), fail = common \| (w29 & (bc \| (w30 & X))) (4), pass = (w8 ^ w25) & ~fail (3) | 25 |
| **total** | **230** (`W6_OPS`, asserted by the program) |

(The term ~(w8^w25) of the earlier filings' `common` is moved into the final mask: pass = (w8 ^ w25) & ~fail, which saves one operation. f2fe1d4d also claimed a saving of 10 operations by a 3-operation carry at the ten bits whose sum is not needed; that carry (a & b) | (c & (a ^ b)) costs 4 operations once a ^ b is counted, which is what the ripple already spends, so the saving does not exist and is not used.)
A partial batch (fewer than 256 fibre lanes) costs one more AND with the lane mask (231). The result is exact: lane L of the pass plane equals F6(cb + v_{256 b + L}) (checked on every lane, Section 13.2).
**Registers.** At bit j the live values are z_j..z_31 (32 - j), the carry, at most four temporaries, dl[j], and the retained sum bits (at most 19); the peak (about 40 at j around 14) and the F6 phase (20 sum bits and about 6 temporaries) are
below 64, with no spills. There is no data-dependent branch: the cost of a batch is the same for every cb and every record.

### 9.5 Scan of the pass plane and the segments

The pass plane (nl live lanes, zeros above) is scanned in 24-bit chunks: per chunk the extraction (the lowest and the highest chunk one operation, the others two) and a zero branch (`chunk_fixed_ops`); per set lane the address of the table entry (add of the chunk's table base), the load of the lane index from the 2^24-entry
table of the chunk position, the add of the entry base, x - 1, x & (x - 1) and the loop branch: 6 (`SCAN_LANE`). A set lane is a passing fibre: the load of its entry (1), the unpacking of start, cost and end (the entry word has the start in lane 0, the cost in lane 1, the end in lane 2 and zero above: AND, shr and AND, shr: 4) and the addition of the cost to V (1)
are `SEG_OVH` = 6; together 12 operations per passing fibre. (The earlier ledgers charged 14 per passing fibre of which the table address was implicit; f2fe1d4d's count of 4 per set lane used a de Bruijn multiplication, which is not a primitive of the cost model, and a missing negation, and is not used.)

### 9.6 Packed good pairs: the group of four, read in place

The member blocks of a segment lie contiguously and word-aligned in two parallel arrays; a *group* is the pair of 256-bit words A (a0 of four consecutive members in the low halves of the four 64-bit lanes, high halves zero) and S (S0(a0) likewise). With M = 2^32 - 1 in every lane the arithmetic is
E0 = (A + e0b) & M (A + e0b < 2^33; the mask removes the carry), mj = A & x12 (x12 = A_{-1} ^ A_{-2}: a0 & (A_{-1} ^ A_{-2})), ch = (E0 & X) ^ Em2, S1(E0) with the 8-operation pattern (masked), W1 = (kap1' + 2^34 - S - mj - S1(E0) - ch) & M
with kap1' = kap1 - (A_{-1} & A_{-2}) (MAJ(a0, A_{-1}, A_{-2}) = (a0 & (A_{-1} ^ A_{-2})) + (A_{-1} & A_{-2}), the two terms having disjoint supports; every subtrahend is below 2^32, so each lane stays in (2^34 - 3 x 2^32, 2^34 + 2^32) and no borrow crosses a lane boundary), s0(W1) with the 8-operation pattern (masked), and
**U = A + s0(W1) + bc(C)** with the per-first-block constant C = RBASE + kap0. Lane k of U is the address RBASE + a0 + kap0 + s0(W1) < RBASE + 2.5 x 2^32 (a0 < 2^29 on G: E4 > 0x1a3a7d2f, since W8x[29] = 1 forces it, checked over all 12,103,680 variants where max a0 = 0x1ff4c6ff; s0(W1) and kap0 < 2^32), nothing above bit 34. The row-16 table is stored three times in a row (**Rmask3**, 3 x 2^32 words, word i holding the l-mask of i mod 2^32),
so that the word at this address is the l-mask of u = (a0 + kap0 + s0(W1)) mod 2^32 = W0 + s0(W1) mod 2^32 without any reduction (and without the per-lane base add of the earlier ledgers; this folding of kap0 and of the base into one vector addition is new here). The constants e0b, kap0, x12, X, Em2, kap1', C are computed once per first block from the chaining value
(`cv_pre`, 39 operations; kap0 = e0b - A_{-4} - E_{-4} - S1(E_{-1}) - CH(E_{-1}, E_{-2}, E_{-3}) - K0, e0b = A_{-4} - S0(A_{-1}) - MAJ(A_{-1}, A_{-2}, A_{-3}), kap1 = A1 - K1 - E_{-3}, as in Lemma 4.1).
Group body: the two address adds of the A and S arrays (pointer of A; pointer of S = pointer of A + the offset of the S array) 2, ld A 1, ld S 1, E0 2, mj 1, ch 2, S1 8, W1 5, s0 8, U 2 = **32** (`GROUP_OPS`); the loop control is per segment (below).
Then the lookup of every lane (`mask_lookup`): extraction of the address from its lane (lane 0: and with a 64-bit mask; lanes 1, 2: shr, and; lane 3, the top lane: shr, nothing lies above it), the load of the word of Rmask3, the branch on a nonzero mask: 3, 4, 4, 3 = **14** per group (`PROBE_OPS`).
All four lanes of every group are probed (the padding lanes repeat a member of the same fibre), so a group costs 46 (`GROUP_FULL` = 32 + 14) whatever its content.
**Segment loop.** A segment of g = ceil(n/4) groups is run as floor(g/8) iterations of an unrolled block of 8 groups (control per iteration: update of the remaining count, compare, branch: 3; the pointer adds are the address adds of the groups), then, for the bits 4, 2, 1 of the remainder, blocks of 4, 2 and 1 groups chosen by a test (and, branch: 2 each) with the length computation (1) and the entry test of the main loop (2) the control is at most 9 + 3 floor(g/8) operations (`LOOP_SEG`, `LOOP_ITER`, `seg_ops`). The unrolled blocks are straight-line code of 8 x 44 + 4 x 44 + 2 x 44 + 44 = 8 x 46 + 4 x 46 + 2 x 46 + 46 = 690 instructions.
A segment of n members therefore costs 12 + 9 + 3 floor(g/8) + 46 g operations (the `cost` word of its entry, reaching V in one addition; the ledger evaluates it exactly for every fibre size).
**Verification:** `selftest` compares the address in the 4 lanes of U with the definition of u (W0 + s0(W1) from the chaining value and a0, plus RBASE and the multiple of 2^32) on 6,000 lanes with extreme chaining-value words (0, 1, 2^32 - 1, 2^31, ...) and variants of maximal S0, and asserts every lane value below 3 x 2^32; `mask_lookup` against the definition of the extraction on 8,000 lanes: 0 mismatches.

### 9.7 The rare path

A lane whose mask is nonzero (probability 1,042,240/2^32 per probed lane): V += 1; the a0 of the lane (2: shift, and, charged as RARE_LOOKUP); recompute W6 and W7 (23 operations) and c7(a0) for W7 (12 more, `RECOMP` = 35); then for the l in the mask W0..W5 and W8 (201),
the y-words (8) and rows 16..36 with early abort (each row 106 + 53 + 1: both members' W (20), CH (3), E (14), MAJ (4), A (12) per word; the cells and the two-bit conditions closing at the row at most 53), charged for rows 16 and 17 always and for rows 18..36 with probability at most 2^-9 each
(the SMC stage factors give 2^-15, 2^-6, ...). These are the counts of 7319bba's Section 9.7 (unchanged); the binary search of the earlier filings is gone because the mask is read directly.

### 9.8 The work counter V

V counts every executed operation in the units of Sections 9.2-9.7. The data-independent part (9.2) is charged per first block; the cost word of each batch (230 + 1 + 71 + the chunk operations of its nl lanes) and the cost word of each passing fibre (12 + 9 + 3 floor(g/8) + 46 g, g = ceil(n/4)) are stored in the record and reach V by one addition each (counted in `BATCH_OVH` and `SEG_OVH`);
the rare path adds its executed cost when it runs. The cap is tested after every first block (compare and branch, in the control allowance). The overshoot past V_MAX is at most the maximal data-dependent work of one first block, vmax_fb = 1,438,843,116,766 (every one of the 12,103,680 variants examined and good, every l past row 16 to row 36), which the ledger charges.

## 10. Success probability, independence and caps

Let a *trial* t = (f, a0, l) be a first block f, an examined variant a0 and l in L*, and A_t the event that a0 is good for f and the pair follows every cell and printed two-bit condition of rows 16..36. The program examines every good pair among the examined variants of every processed first block
(Lemma 8.1) and every l whose row 16 holds, so it finds a success iff some A_t occurs before the cap (and every output is verified, Lemma 6.1). Let X_f = sum over the trials of f of 1[A_t] and X = sum_f X_f.

- **Expectation.** E[X_f] = g x 32 x q3 (Lemma 5.1 and Section 7) with g = p6 E_x|E(x)| the expected number of examined good pairs per first block, and E[X] = N_FB g 32 q3. With g >= g_low (the sampled mean of Section 13.3 divided by the statistics safety factor 1.006, H9)
  and q3 >= q3_used (H2): E[X] >= N_FB g_low 32 q3_used >= mu0 = 0.49531249 (H7) for N_FB = ceil(mu0 / (g_low 32 q3_used)) = 38,017,119,869,886,130 = 2^55.07750;
  mu0 is the smallest 8-decimal number strictly above -ln(0.61 - Pcap - 2^-60) / (1 - 2^-10.4), with Pcap the work-cap failure bound below.
- **One first block (H3).** By Bonferroni, Pr[X_f >= 1] >= E[X_f] - sum over pairs t < t' of f of Pr[A_t and A_t'] = E[X_f] - (1/2) sum_t Pr[A_t] E[X_f - 1 | A_t]. H3: E[X_f - 1 | A_t] <= delta = 2^-9.4 for every trial t, so
  Pr[X_f >= 1] >= (1 - 2^-10.4) E[X_f]. (Only the expected number of *further* successes of the same first block given one success is needed; bursty goodness and shared W7/W6 values enter only through that conditional expectation, and do not affect E[X], which is linear.)
- **Many first blocks (H1).** Distinct first blocks have independent chaining values, so the events X_f >= 1 are independent and Pr[X >= 1] >= 1 - exp(-sum_f Pr[X_f >= 1]) >= 1 - exp(-(1 - 2^-10.4) mu0). The table record of x is a deterministic function of x (Section 8.4).
- **Work cap.** The data-dependent work v_f of a first block (everything except its compression and its 264 fixed operations) has mean at most vbar = 100,186 (Section 11) and is at most vmax_fb = 1,438,843,116,766 (< 2^40.4; every one of the 12,103,680 variants examined and good, every l past row 16 to row 36).
  The v_f are independent (H1), so by Chebyshev Pr[sum v_f > (1 + s) N_FB vbar] <= E[v_f^2]/(s^2 N_FB vbar^2) <= vmax_fb/(s^2 N_FB vbar) = Pcap < 2^-11.30 with the slack s = 2^-10 (def128fc observed that the deviation s N_FB vbar enters squared). V_MAX = ceil((1 + s) N_FB vbar) = 3,812,510,051,141,674,472,590 is reached with probability below Pcap; the run then fails, which is accounted for here.
  No part of v_f depends on a conditional law of the scalars: the cost of a fibre batch is the same for every cb and every record (Section 9.4), and the table statistics enter vbar as expectations over uniform x (H9).
- **Success.** Pr[output a collision] >= 1 - exp(-(1 - 2^-10.4) mu0) - Pcap - 2^-60 = 0.3900000013 > 0.39 (the 2^-60 covers a repeated first block among N_FB draws of 512 bits). Any output is a verified collision, independent of the premises.

## 11. Ledger (exact; `python3 experiments/xtab.py ledger`)

```text
T = A_C + A_S + DEV + N_FB + (N_FB x 264 + V_MAX + vmax_fb + PRE + FIN) / C + 6
  A_C = 2^60   characteristic search and SFS-pair search of the paper (allowance, H4)
  A_S = 2^50   Step-1 SAT solve (paper: 2^41.3)
  DEV = 2^40   all development computation (Section 13.5)
  N_FB = 38,017,119,869,886,130 compressions (2^55.07750; H7 mu0 = 0.49531249, q3 = 2^-74.08, g = 8,129 examined good pairs per first block)
  264     fixed operations per first block (9.2: 30 + 16 control + 5 table read + 3 header loads + 2 + 95 + 38)
  V_MAX = 3,812,510,051,141,674,472,590 = ceil((1 + 2^-10) N_FB vbar), vbar = 100,186 operations, of which
               fibre batches (ceil(F/256) <= F/256 + 1 batches, each charged as a full batch of 230 + 1 + 8 + 31): 1,931
               passing fibres (p6 F x 12): 986
               segments (p6 times the sum over kept fibres of 9 + 3 floor(g/8) + 46 g; every lane probed): 96,113
               rows >= 16 (every probed lane may hit): 1,156
               with F = 1,221.4 x 1.006 kept fibres and Q = 30,577.1 x 1.006 four-groups per first block (Section 13.3)
  vmax_fb = 1,438,843,116,766 (one first block's maximal work: overshoot past the cap test)
  PRE = 2^58 operations (bound on all precomputation, Section 8.2); FIN = 1600 operations and 6 compressions
T x 2644 = 6,974,656,312,181,237,326,748     ->   T = 2^61.194106   ->  time_log2 = 61.19411
preprocessing = A_C + A_S + DEV + PRE/C = 2^60.00155
```

Every count in this block is produced by `ledger()` of `experiments/xtab.py` from the executable routines and the constant HIST_Z (Section 13.3); the integer-tightness of the 5th decimal is asserted in both directions (T^100000 against 2^(p) and 2^(p-1)).
Per first block the program spends 38.99 units against 13.08 in 7319bba and 7.23 in d3ec5c41; per examined good pair the data-dependent work is 12.40 operations, of which 11.5 are the group and its four lookups.

### 11.1 Precomputation

Section 8.2: PRE < 2^58 operations, charged in full (2^46.6 units). Padding lanes: the groups of a fibre of n members are ceil(n/4); the (4 ceil(n/4) - n) padding lanes are probed too and charged (Section 9.6) and the statistics Q count them.
The rare path is charged for every probed lane, padding included.

### 11.2 Sensitivity (log2 T, one input changed)

| change | log2 T |
|---|---|
| as claimed (q3 = 2^-74.08, study B's registered bound less the hedge) | 61.19411 |
| q3 = 2^-74.03 (study B's registered bound, no hedge) | 61.16624 |
| q3 = 2^-74.0225 (study B's bound at face value) | 61.16209 |
| q3 = 2^-74.07 (study A's bound) | 61.18850 |
| q3 = 2^-74.25 | 61.29206 |
| q3 = 2^-74.5 | 61.44486 |
| q3 = 2^-75 (the paper's count of 75 conditions) | 61.78016 |
| A_C = 2^64 | 64.11171 |
| A_C = 2^56 | 60.43353 |
| table statistics at face value (x 1.00 instead of x 1.006) | 61.18459 |
| table statistics x 1.05 | 61.26368 |
| table statistics x 1.10 | 61.34217 |
| THETA = 16 (more fibres examined) | 61.21216 |
| THETA = 100 | 61.20181 |
| each of the four row-16 lookups needs a comparison before its branch (+4 per group) | 61.25740 |
| cap slack 2^-9 | 61.19408 |
| cap slack 2^-12 | 61.20918 |

The table is a sensitivity of the *claimed bound*, in the sense of what the bound would have to be if the stated input were different. For the algorithm as submitted the caps N_FB and V_MAX are fixed, so time is bounded by the claim by construction; a table statistic or an op count that is too small does not lengthen the run but lowers the success probability, which has only the slack of the 1.006 margin on the table statistics (0.6% of vbar and of g) and of the 2^-10 cap factor: a true mean above vbar by more than about 2% would make the cap bind and reduce the success probability below 0.39 unless N_FB and V_MAX are rescaled as the table says. Operations the program executes but does not count are not covered by the cap; the counts of Section 9 are those of the straight-line text described there.

### 11.3 The advice-construction allowances A_S and A_C (H4)

The cost model charges all construction of the advice, including searches omitted from the program. The advice is (i) the 37-step characteristic and its two-bit conditions (Tables 15, 16), (ii) the Step-1 solution S, and (iii) the semi-free-start pair (Table 17) from which S is read.
Everything derived from them (G, the classes, F6, F7, L*, R16, the table) is recomputed in the precomputation (Section 8.2).

- **(ii) and (iii): Step 1 and the SFS pair, charged A_S = 2^50.** The paper reports its Step-1 SAT solve at 2^41.3 compression-equivalents; A_S is 2^8.7 times that. Completing a Step-1 solution to a 37-step semi-free-start pair is cheap and is reproduced in this package: given the characteristic and a dense part (S or any of its A0-variants),
  the organizer experiment `a0-sfs-r37` builds complete 37-step semi-free-start collisions in about 25 milliseconds each (Section 13.2), so the SFS-pair search beyond Step 1 costs below 2^30 units, far inside A_S.
- **(i): the characteristic search, charged A_C = 2^60.** Its running time is not published. We bound it, as the accepted filings on this track do, by the only measured comparison point accepted on this challenge. The promoted filing 6eeefb64 (sha256-r32-exploratory) charged a measured, complete re-run of the four-step
  characteristic search of [LLWS26] for its 35-step characteristic: 593,858 solver CPU-seconds over 59 calls (it charged 32 times that for a blind rediscovery), with a calibrated price of one solver CPU-second of 2^32.796 primitive operations, i.e. 2^21.427 units at C = 2644. A_C = 2^60 units buys 2^38.573 = 4.1 x 10^11 solver
  CPU-seconds, about 13,000 CPU-years: 688,000 times (2^19.39) that measured complete re-run, 2^14.39 times the 32-fold rediscovery allowance, and 200 times a 1000-core cluster running without pause for two years. The 37-step characteristic of [LZLLQZ26] comes from the same group's improved search and its cost is unpublished; the premise is that it did not exceed
  this budget. The same allowance is charged by the accepted filings 087a18c4, 1f12a09a and 7319bba on this track. Sensitivity: 11.2. No other term depends on it.


### 11.4 Why fibres below THETA are not examined (the per-fibre cost model)

A kept fibre of n members costs, per first block, one lane of a batch in the fibre test (1.30 operations, whether or not it passes) and, with probability p6 = 0.0669, 21 + 3 floor(g/8) + 46 g operations, and yields p6 n good pairs. The marginal cost per good pair is therefore
r(n) = (19.4 + 21 + 3 floor(g/8) + 46 g) / n + 0.14 (the rare path) operations, which is 79.6 for n = 1, 16.1 at n = 8, 13.7 at n = 20, 12.9 at n = 40, 12.5 at n = 100 and tends to 11.6 for large n (the group and its four lookups cost 11.5 per member).
A first block costs a fixed 1 + 264/C units whatever it examines, so the cost per good pair including the fixed part, (2644 + 264 + vbar) / g = 12.68 operations at the optimum, is minimised by examining exactly the fibres whose marginal cost r(n) is below it: r(n) < 12.68 from n = 122 on (with oscillation caused by ceil(n/4) below that). Because the fixed cost (2644 + 264) is shared by all examined pairs, including a fibre with r(n) slightly above the optimum lowers the number of first blocks more than it raises the work per pair, which is why the ledger's minimum over THETA lies below the threshold of the marginal rule.
Section 11.2 prices THETA: log2 T varies by 0.0005 bit for THETA between 40 and 64 (the table of Section 13.3); THETA = 40 is the threshold covered by the end-to-end simulation of Section 13.4, and the minimum of the table (THETA = 52) is only 0.0005 bit lower. THETA was chosen on the same statistics that price it; the selection effect is of the order of that difference. The earlier filings' restriction to the 222 largest classes was the same kind of selection under their (much higher) per-class costs.

## 12. Premises

**H1 - uniform independent chaining values (score-critical).** The first blocks are fresh uniform 512-bit strings; their chaining values CV1 = F_37(IV, M0) behave as independent uniform 256-bit values; in particular x = A_{-1} is uniform on 2^32 and independent of cb = C6 - A_{-2} (uniform on 2^32).
Used for: Lemma 5.1 (exact filter rates and the law of the second-block words, per variant), the expected counts, the independence across first blocks (Section 10) and Chebyshev. Evidence: 7319bba's 2^21 and 2^23 real first blocks through the attack's own filters in C (quoted, Section 13.1: passing classes,
good pairs and row-16 passes at the predicted rates); this filing's end-to-end Tungsten simulation over uniform x and cb (Section 13.4) and d3ec5c41's 160,000 first blocks through its counted program (quoted; the same filters). Limitations: a premise; tested on 2^17 to 2^23 first blocks, not 2^58.3. Because the table is indexed by the 32-bit word x,
H1 for x is also an assumption about a single word of the digest of a 37-round compression: its distribution over random first blocks is uniform up to the sampling resolution of the runs above.

**H2 - Step-3 probability of the examined variants (score-critical).** q3 >= q3_used = 2^-74.08, where q3 is Section 7.1's average over the examined variants (the variants of kept fibres) and L*, and q3 <= 2^-70. Evidence: Lemma 7.1 (rows 16..22 identical for all variants; the variant enters only through W8 in W23, W24), the two preregistered SMC studies of 7319bba (Section 7.4; study B is the primary,
both are reported; their registered floor is 2^-74.03 for the 222-class family), Section 7.6 (the dependence on the variant is the tail factor 2^-4 of four conditions on Z + W8x, measured at 2^-4.007 and below the sampling resolution; this filing's subset of G is a different one, hence the hedge of 0.05 bit), the agreement of the stage factors with the printed tables and the peers' studies row by row,
the row-16 rate of real good pairs, and the 37-step semi-free-start collisions built with variant dense parts (Section 13.2). Limitations: a Monte-Carlo bound produced by another solver (its programs are in Appendix A.7; **not re-run here**, in particular not for the new subset), whose coverage rests on the approximate normality of the mean of 32 replicates (study B: relative sd 0.0378); the `+` reading;
the heavy duplication of row-22 survivors within a replicate. A stated premise, not an established fact.

**H3 - few further successes per first block (score-critical).** For every trial t, the expected number of other successful trials of the same first block given A_t is at most delta = 2^-9.4, i.e. E[X_f - 1 | A_t] <= 2^-9.4. It splits into (a) the same variant with another l in L*, and (b) other good pairs (other variants) of the same first block.
For (a) the premise is E[#other l succeeding | A_t] <= 2^-11; 7319bba measured it directly on 19,620,436 distinct Step-3 successes of the SMC (replay of Section 13.1: 0 further successes; rule-of-three 95% bound 2^-22.65). For (b) the expectation is at most rho x N_good x 32 x q3, where N_good bounds the expected number of examined good pairs of the same first block given A_t,
q3 <= 2^-70 (H2), and rho bounds Pr[t' succeeds | t succeeds, t' good] / Pr[t' succeeds | t' good]; the premise is rho <= 2^35 (the measured factor at the row-16 level is 0.98 and 1.00). **The earlier filings used N = all 782,800 variants of their family; with the whole family G (12,103,680 variants) that bound would be rho x 2^-41.5 = 2^-6.5 > 2^-9.4 and is not used.**
The number of other examined good pairs of the same first block is at most the number of examined good pairs, whose size-biased mean (the mean given that a particular pair is good: E[g_x^2]/E[g_x] over x, Section 13.4) is 127,978, below 2^17.0, with an allowance of 2^3 for the further bias of conditioning on A_t, so N_good <= 2^20.0 and delta <= 2^-11 + 2^35 x 2^20.0 x 2^5 x 2^-70 = 2^-11 + 2^-10.0 < 2^-9.4.
Measured here for the new structure (fibre mates share W6 exactly, all classes merged): on 54,000 real first blocks restricted to the 222 embedded classes (THETA = 8, Python counted program), 43,295,580 good pairs and 10,499 row-16 passes (rate 2.425e-4, exact 2.4e-4) give sum R(R-1) / (p^2 sum G(G-1)) = 0.991, the statistic of the earlier filings (0.98 and 1.00). Limitations: rows >= 17 of distinct good pairs cannot be measured jointly within one first block; the premise leaves a margin of 2^35 over the measured row-16 factor; with the size-biased mean alone (without the allowance of 2^3) the examined-pair term would be 2^-13.0.

**H4 - advice allowances (supporting).** The published characteristic and two-bit conditions, the SFS pair's inner values S and L* are advice. Their construction is charged A_S = 2^50 (Step 1 and the completion to an SFS pair) and A_C = 2^60 (the characteristic search). Evidence: Section 11.3.
The variant family, the classes, the filter sets, L*, R16, the table and the program text are recomputed in the preprocessing (Section 8.2). Limitations: the 37-step search time is unpublished; A_C is a bound by comparison, not a measurement.

**H5 - counted word-RAM pricing (score-critical; cost reading).** A word-RAM program of 256-bit primitives in which every executed load, store, logic operation, shift, addition, comparison, branch and unconditional jump costs one primitive is charged by the primitives it executes; tables are ordinary
memory (a read is an address computation plus one load; memory is a reported metric only under collision-frontier-v5); the preprocessing is charged in full; registers: 64, with the live-value bound of Section 9.4; every address that is not a register value is formed by a counted add (Section 9.1), the base of the row-16 mask table folded into the per-first-block constant C; the program text is straight-line code of a few thousand instructions and is not advice. Evidence: the
program is in `experiments/xtab.py` (`w6_batch`, `good_group`, `process_cv`) and is exact against the scalar definitions (Section 13.2); its totals agree with the ledger (Section 13.4, in Tungsten over the whole family). Limitation: no organizer ruling is cited; the premise that the table of 2^53.0 bytes is admissible follows the earlier accepted claims with
memory far above physical capacity (e.g. 2^137 bytes) and the cost model's statement that memory contributes nothing to the scalar. A reader who prices memory accesses higher should read Section 11.2 (the per-first-block time is dominated by the packed stage, not by table reads: about 8,521 table loads per first block, of which 8,182 are the row-16 lookups).

**H7 - exact success floor (supporting).** The cap target is mu0 = 0.49531249, the smallest 8-decimal number strictly above -ln(0.61 - Pcap - 2^-60) / (1 - 2^-10.4) with Pcap = 2^-11.30 the Chebyshev bound for the work cap. With E[X] >= mu0 the success bound of Section 10, 1 - exp(-(1 - 2^-10.4) mu0) - Pcap - 2^-60, is >= 0.39000000
with no further padding. `ledger()` computes mu0 with 60-digit decimals, asserts the success bound > 0.39 and the exact-rational ceiling N_FB g 32 q3 >= mu0. (087a18c4's H7.)

**H9 - table statistics and preprocessing bound (score-critical, new).** (a) Over uniform x, let F, V, Q be the means of the number of kept fibres, of the kept variants and of sum over kept fibres of ceil(size/4). The ledger charges the sample means of Section 13.3 (3,200,000 values of x, Tungsten, sixteen shards; the sixteen shard means differ from the pooled mean by at most 1.51%, the standard error of the pooled mean is 0.17%)
times 1.006 upwards for F and Q (costs) and downwards for V (the yield g), and assumes the exact means lie within that margin. (b) The preprocessing of Section 8.2 costs at most 2^58 operations and the table at most 2^53.0 bytes. Evidence for (a): sampling and the end-to-end simulation of Section 13.4 on 480,000 further values of x; the sensitivity of Section 11.2 (a 5% error in all table statistics would cost 0.079 bit).
Evidence for (b): the explicit algorithm and the arithmetic of Section 8.2 (the number of pairs (x, variant) is exactly 12,103,680 x |F7| = 8.25 x 10^14). Limitation: the means are sample estimates, not exact enumerations over all 2^32 x; the per-x counts are heavy-tailed (the standard deviation across x is about 2.4 times the mean).

## 13. Evidence and runs

All runs for this filing on one Apple-silicon Mac (18 cores): Python standard library (`experiments/xtab.py`) and Tungsten (the user's compiled language, sources in Appendix A); my own code, no rival code executed. The leader's programs and numbers that are used as premises are labelled as such. At most 9 processes ran at a time, with a free-memory guard.

### 13.1 Quoted from 7319bba (end to end on real first blocks; inherited evidence for H1, H3, H2)

C statistics of 7319bba (random M0 from xoshiro256**, CV1 = F_37(IV, M0), the 222 W7 tests of the 222-class family of that filing, the scalar W6 test of every variant of every passing class, u and the exact row-16 test for every l, exact checks of sampled pairs):

| run | first blocks | passing classes (expected) | good pairs (expected; ratio) | row-16 pairs (expected; z) | H3 factor: sum R(R-1) / p^2 sum G(G-1), p = 1052672/2^32, (p = R/G) |
|---|---|---|---|---|---|
| seed 5eed0021 | 2^21 | 7,400,134 (7,388,160) | 1,748,648,111 (1,742,708,500; 1.00341) | 424,363 (422,895; +0.88) | 0.981 (1.001) |
| seed 5eed0023 | 2^23 | 29,545,568 (29,552,640) | 6,978,649,557 (6,970,834,000; 1.00112) | 1,693,297 (1,691,580; +0.51) | 0.979 (0.999) |

The counts are strongly overdispersed (variance-to-mean ratios 28.8 for passing classes, about 23,100 for good pairs, 6.6 for row-16 pairs) because classes are correlated; their means match. 7319bba's replay of 19,620,436 distinct Step-3 successes of the SMC found 0 co-successes across the other 31 elements of L*
(rule-of-three 95% bound 2^-22.65 per success; the samples share SMC ancestors). These programs are not re-run here.

### 13.2 Exhaustive checks and equivalence with brute force (this filing)

- **F6, F7 (Tungsten, Appendix A.2).** For all 2^32 words w: the definition F_k = {w : s0(w + d_k) - s0(w) = t_k} against the bitwise forms of Section 5.1, four shards of 2^30 words: |F6| = 287,309,824 and |F7| = 68,157,440, **0 mismatches** for both.
- **The family G and its classes (Tungsten, Appendix A.1 and A.4).** |G| = 12,103,680 over the 2^29 values of E4 with E4[31:29] = 000; sorted by c7 in Tungsten: 22,976 classes (also found independently with numpy). The 222 embedded classes are regenerated by `xtab.py` from their descriptors, with their sizes asserted (782,800 variants).
- **Lane safety of the packed group.** max over all of G of S0(a0) = 0xffffff58 (numpy over the 12,103,680 variants; over the embedded 782,800 `selftest` finds 0xffffbb5c), so with S0(a0) + 2 < 2^32 no carry leaves a lane; a0 < 2^31 for every variant of G.
- **The table pipeline against brute force (`selftest`).** For 8 classes (indices 0, 17, 40, 77, 111, 150, 200, 221), 2 random x each with the class passing W7 and a random cb, for THETA = 1 and THETA = 8: the record (union fibres over all passing embedded classes, planes, entries, members) is built, every lane of every pass plane is compared with the scalar F6 test of its fibre value
  (155,092 fibre lanes) and the set of members of the passing fibres with the set {a0 in the passing classes : fibre size >= THETA and F6(w6of(a0, x, A_{-2}))} (108,798 good pairs): **0 mismatches**; the V cost word of every fibre equals 12 + seg_ops(n).
- **Packed arithmetic and mask lookup.** The 4-lane U against the definition of u (W0 + s0(W1) from the chaining value and a0): 6,000 lanes with extreme chaining-value words, 0 mismatches; `mask_lookup` against its definition: 8,000 lanes, 0 mismatches.
- **Organizer experiments (local replay of the request format with SHAKE-derived seeds; 6.5 s and 7.6 s, peak memory 30 MB and 74 MB; inside the organizer's 20 s and 128 MiB).**
  `a0-sfs-r37`: 127 of the 128 trials build a 37-step semi-free-start collision with a variant dense part (the others exhaust their proposal budget); for trials 0..15 the constructed chaining value is fed to the counted online program with the table restricted to the class of a0 (THETA = 1), which finds exactly the constructed pair in **16 of 16** cases (table read, fibre test, packed u, row-16 lookup, rows 16..36).
  `a0-online-r37` (trials 0..7): on seed-drawn first blocks until a record has kept fibres (the 222 embedded classes, THETA = 8): 43 first blocks drawn, 8 records with kept fibres, 20536 fibres, 2556 passing fibres, 128152 good pairs, 29 row-16 passes, 1524160 counted operations in all; lane, filter and cell mismatches: 0, 0, 0 (pairs checked against every cell of rows -4..15 for all 32 elements of L*: 14).

### 13.3 Statistics of the table (Tungsten; premise H9)

For each of 3,200,000 values of x drawn uniformly (sixteen shards: 100,000 (eight shards) and 300,000 (eight shards); a 64-bit LCG with different seeds): the 22,976 W7 tests of Section 5.1 (bitwise form), phi(a0, x) for every variant of every passing class (about 190,000 per x), a heap sort and a run scan (Appendix A.4). The output is the histogram of fibre sizes, summed over x; HIST_Z in `xtab.py` holds it for sizes of at least 16 (zlib + base85; the text is in Appendix A.11).
Means per first block: **1,221.4 kept fibres, 122,253 kept variants, 30,577.1 four-groups** for THETA = 40. Passing classes per x: 365.5 on average (22,976 p7 = 364.6 exact), variants in passing classes 192,590 (exact mean 12,103,680 p7 = 192,075).
The sixteen shard means of the kept variants are 121974, 121996, 122968, 122466, 121458, 122788, 120293, 121249, 121593, 122366, 123628, 123010, 121384, 122202, 122176, 122610 (relative standard error of the pooled mean: 0.17%). A first, smaller run of 4,000 values of x per shard (32,000 in all) had given kept variants 121,980 and kept fibres 1,214.2, consistent with the pooled values. The 800,000 values of the first eight shards had given 121,899 kept variants; the later 2,400,000 gave 122,371 (+0.4%). The ledger uses the pooled means times 1.006.

Table 13.3 (pooled over all 3200000 values of x; HIST_Z in `xtab.py` holds the counts; the text is in Appendix A.11):

| size n of the fibre | fibres per first block | variants per first block | share of variants in passing classes |
|---|---|---|---|
| 16..19 | 1080.24 | 17326.6 | 9.00% |
| 20..29 | 401.28 | 9773.7 | 5.07% |
| 30..39 | 799.83 | 25672.9 | 13.33% |
| 40..47 | 58.29 | 2384.0 | 1.24% |
| 48..59 | 252.91 | 12727.3 | 6.61% |
| 60..79 | 427.39 | 27459.5 | 14.26% |
| 80..99 | 123.91 | 11336.5 | 5.89% |
| 100..199 | 260.23 | 35156.3 | 18.25% |
| 200..399 | 78.64 | 20920.7 | 10.86% |
| 400..max | 20.06 | 12268.7 | 6.37% |
| 1..15 (not stored in HIST_Z; never kept) | - | - | - |

| THETA | kept fibres | kept variants | examined good pairs g | log2 T |
|---|---|---|---|---|
| 16 | 3503 | 175026 | 11638 | 61.21216 |
| 20 | 2423 | 157700 | 10486 | 61.20245 |
| 24 | 2367 | 156583 | 10412 | 61.20190 |
| 32 | 2003 | 147380 | 9800 | 61.19922 |
| 40 | 1221 | 122253 | 8129 | 61.19411 |
| 48 | 1163 | 119869 | 7971 | 61.19376 |
| 56 | 976 | 110836 | 7370 | 61.19364 |
| 64 | 888 | 105807 | 7036 | 61.19397 |
| 80 | 483 | 79682 | 5299 | 61.19746 |
| 100 | 359 | 68346 | 4545 | 61.20181 |


### 13.4 The counted program simulated end to end in Tungsten (this filing)

For 480,000 further values of x (eight shards, different seeds) and an independent uniform cb for each: the record of x is built as in Section 8.2 (union fibres, THETA in {20, 30, 40, 60}), the F6 test is applied to every kept fibre value + cb, and the operations of the counted program are summed by its own formulas (batches 230 + 71 + chunk operations (+1 for a partial batch), 12 per passing fibre, 46 per group plus 9 + 3 floor(g/8) per segment, 264 fixed; the rare path is not simulated):

| THETA | x values | kept fibres | kept variants | examined good pairs (simulated) | mean data-dependent ops (simulated) | sd / mean | ledger vbar (same THETA) |
|---|---|---|---|---|---|---|---|
| 20 | 480,000 | 2414.6 | 157213 | 10516 | 128430 | 3.33 | 131451 |
| 30 | 480,000 | 2014.7 | 147479 | 9862 | 119785 | 3.43 | 122669 |
| 40 | 480,000 | 1215.9 | 121838 | 8143 | 97652 | 3.78 | 100186 |
| 60 | 480,000 | 906.2 | 106810 | 7137 | 85163 | 4.01 | 87415 |

The measured mean agrees with the ledger's expectation for THETA = 40 (which carries the safety factor, the bound ceil(F/256) <= F/256 + 1 and the rare path): the simulated mean data-dependent work is 97652 operations, the ledger charges 100186 (99030 without the rare path), i.e. the ledger exceeds the simulation by 1.41% without the rare path. The counts are bursty (standard deviation across first blocks 3.8 times the mean), so the standard error is dominated by rare large records.
The simulation shares the formulas of the ledger but not its code or its source of statistics: it recomputes the fibres of each x from the variants, applies F6 to the fibre values and counts groups of the passing fibres. The size-biased mean of the examined good pairs per first block (the sum of squares over the sum, i.e. the mean number of examined good pairs of the first block that contains a given examined good pair) is 127,978 at THETA = 40 (used in H3).
The Python program itself (`experiments/xtab.py`, restricted to the 222 embedded classes) was run on 24,000 real first blocks with every operation counted by the routines of Section 9: mean 9953 operations per first block (sd 53737, largest 1,418,994), 0.1465 first blocks with a record that has kept fibres at THETA = 8, 754.8 examined good pairs and 0.18 row-16 passes per first block; the same configuration evaluated by the closed formula of the simulation (numpy, 600,000 values of x) gives 10286 operations per first block; on 700 single first blocks (two thirds of the x constructed to pass a class) the counted operations of the Python program equal the closed formula exactly (0 mismatches).

### 13.5 Development computation

Below 6 x 10^4 CPU-seconds in total (the exhaustive F6/F7 check about 600 CPU-seconds, the statistics about 1.2 x 10^4, the end-to-end simulation about 1.2 x 10^4, the selftests and experiment replays under 100, development and the aborted runs the rest), far inside DEV = 2^40 units (2^40 units are about 2^18.6 = 4 x 10^5 CPU-seconds at 2^21.4 units per CPU-second).
One earlier set of eight Tungsten shards leaked memory (untyped locals in helpers called inside a 5 x 10^8 iteration loop; about 10 GB each within 20 seconds) and was killed by hand after about 60 seconds, with no result used; the rewritten programs type every local and were measured flat at 110 MB per shard.

## 14. Memory and advice

Peak memory (all simultaneously resident during the online phase):

| item | bytes |
|---|---|
| T0: 2^32 words of 8 bytes | 2^35 |
| records R(x): members 2 x 8 x 4 ceil(n/4) per kept fibre (A and S arrays), entries 32 per fibre, planes 1024 per batch, cost words: mean 2,014,003 bytes per x over uniform x (Section 13.3, times 1.006), 2^32 records | 2^52.9 |
| Rmask3: 3 x 2^32 words of 32 bytes; the 24-bit lane-scan tables (11 x 2^24 entries); code | 2^38.6 |
| total | **2^53.0** |

Claimed memory: 2^53.0 bytes (the sum over all x of the record sizes, estimated from the sampled means; reported only under collision-frontier-v5; the earlier claims on this track report up to 2^137 bytes). The table is built entry by entry in the preprocessing and is never held twice.
Nonuniform advice: the characteristic, S, L*, and the 222 class descriptors used by the experiments (below 2^13 bytes), charged through A_C and A_S; everything else, including the class list of the whole family, the table and Rmask, is recomputed in the preprocessing.

## 15. Limitations

- H1, H2, H3 are premises. q3 is estimated (Monte Carlo, by another solver, not re-run here and not for this filing's subset of G), not proved; no collision has been found and none is expected at the scale we can run. The full-scale success probability cannot be observed.
- The table statistics (H9) are Tungsten sample means over 3,200,000 values of x, scaled by 1.006, not an enumeration of all 2^32 values of x (about 2^58 operations of Tungsten work). The per-x counts are heavy-tailed. Section 11.2 prices a 5% and a 10% error.
- The organizer experiments run the same program on the 222 embedded classes only (the sandbox cannot hold the family); the whole-family table and statistics are Tungsten computations of this filing, not organizer experiments.
- The memory of 2^53.0 bytes is far beyond any machine; memory is reported only under collision-frontier-v5 and earlier claims on this track report up to 2^137 bytes. A reader who charges table reads or memory differently should note that table reads are about 8,521 of the 100,186 data-dependent operations per first block.
- Study B of the q3 estimate was registered after study A had been read (7319bba, Section 7.4); study A's bound would price the claim at 61.18850. The hedge of 0.05 bit for the changed subset of variants is a judgment, not a measurement.
- The published characteristic and SFS pair are used as advice under allowances; the paper's SAT solve and characteristic search were not rerun.
- For 37 steps the measured q3 is about one bit better than the 75 conditions stated in the paper's text; the paper's own tables give 74, which the SMC matches stage by stage (6c77089c reached the same conclusion). With q3 = 2^-75, log2 T would be 61.78016.
- H3 (b) is measured at the row-16 level only (7319bba) and its bound on the number of examined good pairs is a premise.
- The program text, the table and the lane-scan tables are assumed addressable and free of charge to store (H5); the cost reviewer may price memory differently (Section 11.2).
- The counts of the earlier filings that this one corrects (Section 16) were accepted for review as they were; correcting them cost this filing 0.006 bit.

## 16. What this filing changes relative to d3ec5c41 (61.71473) and its derivatives (61.68435, 61.57882, 61.51197)

| change | effect |
|---|---|
| all 22,976 classes, fibres merged across classes by equal phi, only fibres of at least THETA variants examined (Sections 5.3, 8.1, 11.4) | 122,253 variants examined per first block, g = 8,129 examined good pairs instead of 831; N_FB 2^55.07750 instead of 2^58.32 |
| direct row-16 mask table, no presence word (8aeaed1c, def128fc; re-implemented) | lookup 3.5 operations per lane and no per-lane base add instead of 6.91; rare path 132 -> 2 |
| packed group 32 operations (with its two address adds) instead of 37 (MAJ identity and unmasked first additions of f2fe1d4d; kap0 and the table base folded into one vector addition with a table stored three times: no per-lane base add and no reduction mod 2^32), lookups 14 per group, segment loops unrolled by 8 (control 3 per 8 groups instead of 3 per group) | 46 per group of four instead of 37 + 4 x 6.9 = 65 |
| honest counts: 31 address adds per plane batch, SCAN_LANE 6 instead of 5, segment loop control 9 + 3 per 8 groups, the address adds of the A and S arrays, cv_pre with its broadcasts and unpacking (81), the reload of the z planes per batch (63), padding lanes probed and charged, BATCH_OVH 71, SEG_OVH 6 | 0.006 bit against the uncorrected counts |
| not adopted: f2fe1d4d's 3-operation carry (needs 4), 4-operation scan (needs a multiplication and a negation) | see Sections 9.4 and 9.5 |
| cap slack 2^-10 with the slack squared in Chebyshev's bound (def128fc) | small |
| same attack, variants' semantics, packed u formula, rare path, q3 studies, caps' structure, A_C, A_S, DEV | unchanged apart from H2's hedge |

## Appendix A. Programs and records

A.1, A.2, A.4, A.11 and A.12 were written and run for this filing (Tungsten, the user's compiled language, `tungsten file.w`; Python `experiments/xtab.py` is the counted program). A.3 and A.5-A.10 are reproduced **unchanged from 7319bba as inert text; they were not run for this filing** and support the premises H2 and H3 and the tables of the earlier filings. They are evidence for the reader, not part of the attack. References to `spec6core.py` in the inherited listings refer to 7319bba's program, which is not part of this package.

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


### A.4 `un_k.w`: the family G, its classes and the fibre-size histogram over uniform x (Tungsten; shard 0 shown, the other seven differ only in `seed` = 101 + k; `nx` = 100000)

Every local is typed (`## i64`): an earlier version with untyped locals in helpers leaked memory (Section 13.5). The program enumerates the 2^29 values of E4, keeps those in G, sorts the keys (c7 << 32 | a0) by heap sort, cuts the 22,976 classes, and for each uniform x tests every class with the bitwise F7 form, computes phi for the variants of the passing classes, sorts, and accumulates the histogram of fibre sizes. Output lines: `G size`, `classes`, `NX nx passc passv big`, and `H s count`.

```text
-> in_g(a0) (i64) i64
  e4 = 0 ## i64
  w = 0 ## i64
  ok = 1 ## i64
  e4 = (a0 + 734766) & 4294967295
  w = (3661266223 - e4) & 4294967295
  ok = 0 if (e4 >> 29) != 0
  ok = 0 if ((w >> 29) & 1) != 1
  ok = 0 if ((w >> 1) & 1) == ((w >> 12) & 1)
  ok = 0 if ((w >> 8) & 1) == ((w >> 25) & 1)
  ok = 0 if ((w >> 14) & 1) != ((w >> 18) & 1)
  ok
-> c7_of(a0) (i64) i64
  e4 = 0 ## i64
  m = 0 ## i64
  c = 0 ## i64
  e4 = (a0 + 734766) & 4294967295
  m = (2558469316 & 1652717670) | (2558469316 & a0) | (1652717670 & a0)
  c = (3943406637 & 3891447839) | ((3943406637 ^ 4294967295) & e4)
  (2879002467 + m - c) & 4294967295
-> phi_of(a0, x) (i64 i64) i64
  e4 = 0 ## i64
  e3 = 0 ## i64
  m = 0 ## i64
  m2 = 0 ## i64
  c = 0 ## i64
  e4 = (a0 + 734766) & 4294967295
  m = (2558469316 & 1652717670) | (2558469316 & a0) | (1652717670 & a0)
  e3 = (1199649517 - m + x) & 4294967295
  m2 = (1652717670 & a0) | (1652717670 & x) | (a0 & x)
  c = (3891447839 & e4) | ((3891447839 ^ 4294967295) & e3)
  (m2 - c) & 4294967295
-> f7b(w) (i64) i64
  b0 = 0 ## i64
  b1 = 0 ## i64
  b2 = 0 ## i64
  b9 = 0 ## i64
  b10 = 0 ## i64
  b11 = 0 ## i64
  b12 = 0 ## i64
  b18 = 0 ## i64
  b19 = 0 ## i64
  b22 = 0 ## i64
  b23 = 0 ## i64
  b26 = 0 ## i64
  b27 = 0 ## i64
  b28 = 0 ## i64
  b29 = 0 ## i64
  b30 = 0 ## i64
  b31 = 0 ## i64
  ok = 1 ## i64
  h1 = 0 ## i64
  h2 = 0 ## i64
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
  ok = 0 if b1 != b18
  ok = 0 if b0 != b28
  ok = 0 if b9 != b30
  h1 = 1 if b11 == 0 && b22 == 1 && b26 == 1
  h2 = 1 if b11 == 1 && b12 == 0 && b22 == 0 && b23 == 1 && b26 == 0 && b27 == 1 && b2 == b19 && b1 == b29 && b10 == b31
  ok = 0 if h1 == 0 && h2 == 0
  ok
-> sift(arr, start, end_) (i64[] i64 i64) i64
  root = start ## i64
  running = 1 ## i64
  child = 0 ## i64
  sw = 0 ## i64
  t = 0 ## i64
  while running == 1
    child = root * 2 + 1
    if child >= end_
      running = 0
    else
      sw = root
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
  end_ = 0 ## i64
  t = 0 ## i64
  while start >= 0
    sift(arr, start, n)
    start -= 1
  end_ = n - 1
  while end_ > 0
    t = arr[0]
    arr[0] = arr[end_]
    arr[end_] = t
    sift(arr, 0, end_)
    end_ -= 1
  0

-> main_run(dummy) (i64) i64
  nx = 100000 ## i64
  seed = 101 ## i64
  keys = i64[12103700]
  n = 0 ## i64
  e4 = 0 ## i64
  a0 = 0 ## i64
  while e4 < 536870912
    a0 = (e4 - 734766) & 4294967295
    if in_g(a0) == 1
      keys[n] = (c7_of(a0) << 32) | a0
      n += 1
    e4 += 1
  << "G size [n]"
  heapsort(keys, n)
  cstart = i64[23000]
  c7c = i64[23000]
  ncls = 0 ## i64
  i = 0 ## i64
  j = 0 ## i64
  while i < n
    cstart[ncls] = i
    c7c[ncls] = keys[i] >> 32
    j = i
    while j < n && (keys[j] >> 32) == c7c[ncls]
      j += 1
    ncls += 1
    i = j
  cstart[ncls] = n
  << "classes [ncls]"
  phis = i64[4000000]
  hist = i64[100000]
  big = 0 ## i64
  rng = 0 ## i64
  rng = 987654321987654321 + seed * 1000003
  t = 0 ## i64
  passc = 0 ## i64
  passv = 0 ## i64
  x = 0 ## i64
  m = 0 ## i64
  c = 0 ## i64
  w = 0 ## i64
  k = 0 ## i64
  sz = 0 ## i64
  while t < nx
    rng = rng * 6364136223846793005 + 1442695040888963407
    x = (rng >> 32) & 4294967295
    m = 0
    c = 0
    while c < ncls
      w = (c7c[c] - x) & 4294967295
      if f7b(w) == 1
        passc += 1
        k = cstart[c]
        while k < cstart[c + 1]
          a0 = keys[k] & 4294967295
          phis[m] = phi_of(a0, x)
          m += 1
          k += 1
      c += 1
    passv += m
    heapsort(phis, m)
    i = 0
    while i < m
      j = i
      while j < m && phis[j] == phis[i]
        j += 1
      sz = j - i
      if sz < 100000
        hist[sz] += 1
      else
        big += 1
      i = j
    t += 1
  << "NX [nx] passc=[passc] passv=[passv] big=[big]"
  s = 1 ## i64
  while s < 100000
    if hist[s] > 0
      << "H [s] [hist[s]]"
    s += 1
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

```text
shard 0: G size 12103680
shard 0: classes 22976
shard 0: NX 100000 passc=36550572 passv=19225992600 big=0
shard 1: G size 12103680
shard 1: classes 22976
shard 1: NX 100000 passc=36426947 passv=19194308282 big=0
shard 2: G size 12103680
shard 2: classes 22976
shard 2: NX 100000 passc=36623163 passv=19281619264 big=0
shard 3: G size 12103680
shard 3: classes 22976
shard 3: NX 100000 passc=36832906 passv=19389501252 big=0
shard 4: G size 12103680
shard 4: classes 22976
shard 4: NX 100000 passc=36215456 passv=19121193578 big=0
shard 5: G size 12103680
shard 5: classes 22976
shard 5: NX 100000 passc=36754484 passv=19417152366 big=0
shard 6: G size 12103680
shard 6: classes 22976
shard 6: NX 100000 passc=36105129 passv=19031132184 big=0
shard 7: G size 12103680
shard 7: classes 22976
shard 7: NX 100000 passc=36325841 passv=19125265462 big=0
shard 8: G size 12103680
shard 8: classes 22976
shard 8: NX 300000 passc=109560530 passv=57669681980 big=0
shard 9: G size 12103680
shard 9: classes 22976
shard 9: NX 300000 passc=109567049 passv=57756537864 big=0
shard 10: G size 12103680
shard 10: classes 22976
shard 10: NX 300000 passc=110421941 passv=58292141172 big=0
shard 11: G size 12103680
shard 11: classes 22976
shard 11: NX 300000 passc=110097244 passv=57997881456 big=0
shard 12: G size 12103680
shard 12: classes 22976
shard 12: NX 300000 passc=109379515 passv=57525818440 big=0
shard 13: G size 12103680
shard 13: classes 22976
shard 13: NX 300000 passc=109305968 passv=57641909208 big=0
shard 14: G size 12103680
shard 14: classes 22976
shard 14: NX 300000 passc=109641516 passv=57690379546 big=0
shard 15: G size 12103680
shard 15: classes 22976
shard 15: NX 300000 passc=109727455 passv=57927552054 big=0
e2e shard 0: EN 20 nx=60000 F=144629467 V=9367354768 GR=2343934699 PF=9513114 good=613035867 grp=153394146 sops=7192464801 ops=7504885246 ops2=11362381414734196 good2=79003366392395 v2=7956761751044288
e2e shard 0: EN 30 nx=60000 F=120595730 V=8782490742 GR=2197076901 PF=7923709 good=574371721 grp=143685779 sops=6731563973 ops=6993631578 ops2=10421761144247058 good2=72999960499753 v2=7306639394565876
e2e shard 0: EN 40 nx=60000 F=72549797 V=7240407502 GR=1810907209 PF=4783472 good=473581517 grp=118448512 sops=5532966847 ops=5694356812 ops2=8244438119864086 good2=58705344917975 v2=5763440110924820
e2e shard 0: EN 60 nx=60000 F=53910023 V=6335677386 GR=1584277243 PF=3541008 good=413260126 grp=103338297 sops=4822987389 ops=4944925632 ops2=6945002800418548 good2=49783322622170 v2=4860092895672604
e2e shard 1: EN 20 nx=60000 F=145845734 V=9515918268 GR=2381027239 PF=9757503 good=637496128 grp=159509176 sops=7478130388 ops=7795077669 ops2=12233049181735717 good2=85220434599250 v2=8174864277566104
e2e shard 1: EN 30 nx=60000 F=121812331 V=8931410748 GR=2234300688 PF=8138022 good=598127740 grp=149626702 sops=7008955549 ops=7275173667 ops2=11257866435508729 good2=78995525984146 v2=7510374048933656
e2e shard 1: EN 40 nx=60000 F=73600624 V=7383733096 GR=1846745646 PF=4901247 good=494201702 grp=123605104 sops=5773120741 ops=5937303949 ops2=8981996152670993 good2=64054319882006 v2=5941382976560088
e2e shard 1: EN 60 nx=60000 F=54808679 V=6472825224 GR=1618568432 PF=3648018 good=433570097 grp=108417164 sops=5059436753 ops=5183835675 ops2=7672072812645395 good2=55065502667459 v2=5016003114197392
e2e shard 2: EN 20 nx=60000 F=147776878 V=9548175092 GR=2389181413 PF=10106128 good=656589241 grp=164295799 sops=7702994938 ops=8026703599 ops2=12746817272289715 good2=88670550219237 v2=8165889155893024
e2e shard 2: EN 30 nx=60000 F=123157404 V=8948775694 GR=2238690894 PF=8431076 good=615773148 grp=154047827 sops=7216505012 ops=7488040268 ops2=11706975253732526 good2=82026074113056 v2=7494317215464620
e2e shard 2: EN 40 nx=60000 F=73805170 V=7364720136 GR=1842029909 PF=5062912 good=507650944 grp=126973067 sops=5930648084 ops=6097068702 ops2=9254284769168068 good2=65913552895816 v2=5889002984375960
e2e shard 2: EN 60 nx=60000 F=54960487 V=6449647676 GR=1612792841 PF=3783406 good=445561965 grp=111417133 sops=5199721048 ops=5326015383 ops2=7832626734434143 good2=56155085075105 v2=4962228943037104
e2e shard 3: EN 20 nx=60000 F=145680465 V=9470491130 GR=2369699649 PF=9737373 good=635237670 grp=158949883 sops=7452018607 ops=7768512788 ops2=12432329344193324 good2=86642702802948 v2=8182470982432820
e2e shard 3: EN 30 nx=60000 F=121557243 V=8883282670 GR=2222268584 PF=8134494 good=596206853 grp=149147866 sops=6986693440 ops=7252528349 ops2=11466266851154475 good2=80472627966601 v2=7516144756812484
e2e shard 3: EN 40 nx=60000 F=73331647 V=7335276162 GR=1834628805 PF=4918627 good=492988963 grp=123301796 sops=5759183816 ops=5923212495 ops2=9157493598979495 good2=65298611266563 v2=5933743031770924
e2e shard 3: EN 60 nx=60000 F=54674264 V=6429046846 GR=1607619040 PF=3680673 good=432836728 grp=108233271 sops=5051176218 ops=5175809578 ops2=7845856572213180 good2=56297402413766 v2=5014676441556140
e2e shard 4: EN 20 nx=60000 F=143319673 V=9427055340 GR=2358798425 PF=9543452 good=627482356 grp=157004182 sops=7360155673 ops=7671224093 ops2=11852661813346635 good2=82535891516358 v2=8086635649263640
e2e shard 4: EN 30 nx=60000 F=119706007 V=8852408296 GR=2214548032 PF=7963445 good=589087166 grp=147366640 sops=6902604160 ops=7163959037 ops2=10885841807912901 good2=76355485230830 v2=7437960608048032
e2e shard 4: EN 40 nx=60000 F=73012071 V=7353674894 GR=1839237078 PF=4886618 good=490300967 grp=122629605 sops=5727778626 ops=5890999143 ops2=8716268865632539 good2=62101925521639 v2=5916859547364588
e2e shard 4: EN 60 nx=60000 F=54583341 V=6459854268 GR=1615332374 PF=3649438 good=430412796 grp=107628127 sops=5022864478 ops=5147037228 ops2=7413962320233880 good2=53161990171424 v2=5006260930474304
e2e shard 5: EN 20 nx=60000 F=142158517 V=9283718044 GR=2322939108 PF=9590473 good=621117462 grp=155411485 sops=7286740153 ops=7596809886 ops2=11797632698413314 good2=82103220408708 v2=7930197615303720
e2e shard 5: EN 30 nx=60000 F=118730016 V=8712856882 GR=2179611094 PF=7989621 good=582138937 grp=145623750 sops=6822092094 ops=7082440214 ops2=10820429718956492 good2=75862590487109 v2=7287126015731172
e2e shard 5: EN 40 nx=60000 F=71481870 V=7196186910 GR=1799848380 PF=4763872 good=478586054 grp=119698125 sops=5590804356 ops=5750526288 ops2=8567499960473864 good2=61071989851550 v2=5766987271532556
e2e shard 5: EN 60 nx=60000 F=53358488 V=6315862636 GR=1579322961 PF=3548196 good=419569707 grp=104915496 sops=4896215310 ops=5017457621 ops2=7302356480145301 good2=52384672306391 v2=4883507944757664
e2e shard 6: EN 20 nx=60000 F=144148881 V=9394704544 GR=2350736293 PF=9653545 good=629273701 grp=157454510 sops=7381942421 ops=7695401778 ops2=12066877316221100 good2=83981832748585 v2=8063148820459016
e2e shard 6: EN 30 nx=60000 F=120237331 V=8812872284 GR=2204642699 PF=8047993 good=590187253 grp=147642216 sops=6916121586 ops=7179171401 ops2=11067216052277275 good2=77589050607935 v2=7411341358163016
e2e shard 6: EN 40 nx=60000 F=72561145 V=7282490476 GR=1821440894 PF=4877002 good=488403241 grp=122154921 sops=5705654124 ops=5868190989 ops2=8805591295396353 good2=62729809519765 v2=5884008658234240
e2e shard 6: EN 60 nx=60000 F=54142623 V=6388673534 GR=1597532949 PF=3627592 good=427802270 grp=106974741 sops=4992372924 ops=5115719471 ops2=7453421769946655 good2=53441502718860 v2=4982183457954916
e2e shard 7: EN 20 nx=60000 F=145442007 V=9454830576 GR=2365825222 PF=9740946 good=627524951 grp=157022665 sops=7362686416 ops=7678952302 ops2=11748571213048278 good2=81649956292039 v2=8084275690958624
e2e shard 7: EN 30 nx=60000 F=121257359 V=8865717892 GR=2217913851 PF=8106066 good=587702506 grp=147022425 sops=6887955714 ops=7153107806 ops2=10759591104182718 good2=75339929662084 v2=7426384214056248
e2e shard 7: EN 40 nx=60000 F=73275774 V=7325668194 GR=1832253418 PF=4834759 good=482707151 grp=120731464 sops=5639315824 ops=5802314826 ops2=8470805061100004 good2=60317570443907 v2=5860261520041660
e2e shard 7: EN 60 nx=60000 F=54552369 V=6416985872 GR=1604618138 PF=3601361 good=422873743 grp=105741919 sops=4934995978 ops=5058552422 ops2=7185513602789210 good2=51498563833537 v2=4937818119075384
python counted program: {"seed": "r1", "fb": 8000, "theta": 8, "mean": 9816.447625, "sd": 50294.26335442748, "max": 1418994, "hit": 1176, "good": 5944626, "fibres": 2999278, "seg": 192830, "r16": 1399, "secs": 155.07578778266907}
python counted program: {"seed": "r2", "fb": 8000, "theta": 8, "mean": 10152.6425, "sd": 51682.42261365748, "max": 1355651, "hit": 1205, "good": 6179580, "fibres": 3042094, "seg": 185433, "r16": 1515, "secs": 157.72287797927856}
python counted program: {"seed": "r3", "fb": 8000, "theta": 8, "mean": 9888.547625, "sd": 53737.45211374216, "max": 1204263, "hit": 1134, "good": 5990662, "fibres": 2873180, "seg": 201303, "r16": 1475, "secs": 150.02035999298096}
```

The pooled histogram of fibre sizes (the text whose zlib + base85 form is HIST_Z in `experiments/xtab.py`; first line the number of values of x, then size and count summed over all eight shards, sizes of at least 16):

```text
NX 3200000
16 3388086153
17 1617616
18 65843405
19 1209548
20 147625343
21 11017050
22 16418160
23 1215428
24 813905795
25 1443772
26 28049092
27 2317268
28 260267771
29 1849172
30 56570661
31 1616188
32 2409018306
33 1100332
34 4167414
35 1915832
36 80417489
37 225894
38 2893151
39 1517490
40 133122506
41 189308
42 26753115
43 263068
44 20437482
45 2607456
46 2920111
47 220134
48 552810466
49 793922
50 3384486
51 231384
52 35693508
53 208108
54 5000579
55 274044
56 206072898
57 372560
58 4325156
59 136624
60 66141128
61 223376
62 3894230
63 772828
64 1218734068
65 260846
66 2348888
67 51554
68 4786093
69 165784
70 4220181
71 80554
72 58236592
73 38794
74 479854
75 458706
76 3070457
77 222136
78 3367587
79 85768
80 80287523
81 127540
82 459224
83 20568
84 27063614
85 54296
86 556953
87 184542
88 14599199
89 33176
90 5515802
91 169204
92 3106725
93 185594
94 418287
95 49128
96 262058783
97 22916
98 1510297
99 79638
100 3190022
101 12642
102 498861
103 15446
104 25729209
105 382616
106 469027
107 33372
108 4531863
109 14926
110 502127
111 22630
112 103536832
113 41478
114 690624
115 41666
116 4447263
117 92878
118 243744
119 46844
120 44018814
121 43482
122 464860
123 28152
124 3988098
125 30796
126 1422284
127 13402
128 440361426
129 25726
130 527734
131 12086
132 2102307
133 39010
134 103000
135 148236
136 3241034
137 13026
138 289183
139 6448
140 3769064
141 24680
142 135138
143 20958
144 27469943
145 31610
146 79854
147 48422
148 427445
149 17624
150 890169
151 14902
152 1861652
153 11122
154 362114
155 30924
156 3039292
157 12016
158 154087
159 18684
160 33316659
161 18340
162 211942
163 3154
164 413295
165 44432
166 33030
167 3616
168 14959355
169 8850
170 111943
171 21720
172 463131
173 5390
174 359688
175 20204
176 6510540
177 14554
178 53258
179 2396
180 4727638
181 6170
182 275853
183 19202
184 1825449
185 9428
186 328889
187 6288
188 335599
189 24846
190 72287
191 3638
192 87337180
193 3220
194 49677
195 30608
196 1136559
197 2148
198 132097
199 1642
200 1656117
201 3802
202 18810
203 11766
204 429265
205 3944
206 30668
207 8706
208 11696820
209 3000
210 621677
211 3830
212 422175
213 5702
214 52574
215 4566
216 2299998
217 17292
218 24700
219 4760
220 348127
221 4312
222 35331
223 1798
224 34558151
225 37350
226 63321
227 4206
228 536515
229 1538
230 61851
231 10500
232 2690641
233 6804
234 161019
235 6442
236 175322
237 6838
238 76331
239 1948
240 18199010
241 5056
242 61722
243 4158
244 391420
245 6812
246 46212
247 5170
248 2327149
249 3608
250 54619
251 1422
252 1033944
253 2294
254 22101
255 6316
256 113657549
257 870
258 41555
259 1804
260 427864
261 6950
262 16780
263 1250
264 1038009
265 3152
266 48924
267 2234
268 78853
269 1066
270 237435
271 2168
272 1376489
273 7792
274 16553
275 2080
276 217432
277 954
278 10235
279 7796
280 1748331
281 1586
282 34106
283 1068
284 90037
285 9300
286 32904
287 2478
288 8693174
289 1110
290 57598
291 3610
292 62843
293 2728
294 75826
295 1816
296 208862
297 2618
298 22551
299 1228
300 644792
301 2200
302 21529
303 608
304 693576
305 3396
306 20834
307 512
308 222487
309 2572
310 53227
311 952
312 1484519
313 526
314 14805
315 13998
316 113305
317 628
318 28272
319 1020
320 9340749
321 1580
322 22192
323 478
324 127627
325 1368
326 3540
327 878
328 210737
329 1032
330 60399
331 274
332 21577
333 1402
334 5407
335 484
336 5054339
337 416
338 12771
339 1690
340 80823
341 2134
342 32201
343 1226
344 209690
345 3228
346 7930
347 568
348 280730
349 360
350 32464
351 2546
352 1865675
353 552
354 17602
355 610
356 31994
357 2218
358 2783
359 916
360 2148562
361 1648
362 6727
363 1584
364 184428
365 670
366 28791
367 744
368 638269
369 1216
370 13053
371 1760
372 228799
373 366
374 8577
375 2852
376 138629
377 944
378 37554
379 268
380 41123
381 766
382 5809
383 188
384 20209004
385 722
386 4571
387 578
388 42142
389 246
390 39901
391 574
392 445882
393 778
394 2871
395 980
396 85127
397 190
398 2947
399 2854
400 498678
401 190
402 5883
403 1086
404 11688
405 3432
406 16149
407 756
408 191442
409 230
410 7086
411 610
412 19301
413 508
414 10930
415 362
416 3490187
417 312
418 4104
419 130
420 415587
421 248
422 4812
423 810
424 191654
425 556
426 8101
427 1264
428 28876
429 638
430 6708
431 238
432 709139
433 196
434 23201
435 2184
436 15461
437 378
438 7206
439 210
440 124656
441 612
442 5340
443 430
444 20861
445 466
446 2674
447 856
448 7673088
449 230
450 47406
451 356
452 37852
453 1012
454 3728
455 954
456 221634
457 262
458 1777
459 490
460 37969
461 116
462 15868
463 366
464 1006201
465 2418
466 12730
467 614
468 109033
469 358
470 7922
471 496
472 66323
473 214
474 9111
475 348
476 43871
477 712
478 2662
479 248
480 4904427
481 360
482 5411
483 486
484 35134
485 384
486 5374
487 110
488 182503
489 384
490 8975
491 380
492 24778
493 188
494 7021
495 1180
496 809327
497 390
498 4145
499 144
500 30159
501 294
502 1453
503 144
504 368039
505 326
506 3572
507 270
508 12316
509 258
510 9661
511 230
512 20610947
513 484
514 1536
515 230
516 23414
517 124
518 2316
519 270
520 176229
521 178
522 10837
523 70
524 9386
525 1704
526 1111
527 270
528 309500
529 78
530 4601
531 328
532 24907
533 326
534 2753
535 166
536 28640
537 60
538 1734
539 256
540 140704
541 146
542 3202
543 232
544 367649
545 82
546 10435
547 58
548 8098
549 482
550 2078
551 282
552 81596
553 302
554 1263
555 608
556 6471
557 150
558 10616
559 140
560 456693
561 194
562 1740
563 40
564 19202
565 210
566 1258
567 298
568 31440
569 76
570 10053
571 92
572 17993
573 70
574 3109
575 90
576 1797748
577 118
578 1441
579 114
580 38053
581 146
582 4301
583 98
584 25970
585 754
586 2935
587 20
588 41768
589 402
590 2631
591 98
592 56297
593 96
594 3641
595 342
596 9911
597 34
598 1325
599 98
600 226840
601 48
602 2360
603 184
604 11297
605 240
606 918
607 28
608 159516
609 358
610 3806
611 286
612 12837
613 118
614 499
615 378
616 65355
617 98
618 3361
619 28
620 31615
621 58
622 1143
623 50
624 433321
625 166
626 782
627 186
628 6746
629 80
630 18506
631 20
632 43685
633 234
634 684
635 120
636 15516
637 212
638 1689
639 88
640 1748586
641 158
642 2023
643 24
644 10141
645 244
646 565
647 114
648 36564
649 156
650 1769
651 484
652 1929
653 68
654 1062
655 32
656 56840
657 224
658 1254
659 42
660 29010
661 16
662 322
663 74
664 7249
665 90
666 1210
667 30
668 2943
669 34
670 744
671 72
672 1059352
673 46
674 484
675 630
676 6488
677 22
678 2472
679 198
680 27454
681 96
682 2964
683 64
684 15550
685 54
686 1442
687 60
688 55907
689 114
690 3157
691 34
692 4062
693 136
694 477
695 108
696 115517
697 40
698 477
699 430
700 16478
701 48
702 3674
703 68
704 345751
705 248
706 427
707 24
708 8704
709 50
710 566
711 128
712 9048
713 142
714 3155
715 36
716 1201
717 96
718 856
719 26
720 572338
721 42
722 1962
723 106
724 3130
725 44
726 2313
727 10
728 61476
729 40
730 961
731 20
732 17050
733 24
734 1060
735 444
736 140859
737 42
738 1271
739 10
740 5889
741 120
742 1794
743 18
744 78010
745 100
746 544
747 48
748 3459
749 18
750 3626
751 32
752 33075
753 18
754 961
755 84
756 20275
757 34
758 364
759 88
760 10930
761 18
762 998
763 62
764 2243
765 138
766 187
767 42
768 3136000
769 34
770 805
771 16
772 2699
773 36
774 830
775 70
776 18586
777 30
778 390
779 72
780 20508
781 26
782 581
783 56
784 93772
785 26
786 723
787 20
788 1453
789 28
790 1329
791 88
792 26456
793 80
794 235
795 160
796 1407
797 36
798 2790
799 30
800 90701
801 34
802 191
803 20
804 2809
805 26
806 1045
807 26
808 3688
809 18
810 4356
811 18
812 8492
813 128
814 528
815 12
816 50990
817 32
818 241
819 118
820 3584
821 12
822 563
824 6708
825 42
826 814
827 40
828 5025
829 18
830 323
831 36
832 670055
833 10
834 359
835 4
836 1534
837 112
838 147
840 137101
841 18
842 196
843 88
844 2094
845 60
846 812
847 72
848 45664
849 16
850 799
851 22
852 3446
853 6
854 1517
855 216
856 7584
857 6
858 1074
859 36
860 3017
861 56
862 252
863 86
864 135035
865 58
866 168
867 26
868 10592
869 36
870 2029
871 8
872 4061
873 182
874 256
875 82
876 3833
877 6
878 214
879 96
880 25634
881 6
882 959
883 38
884 2569
885 46
886 573
887 10
888 6072
889 16
890 310
891 6
892 1127
893 4
894 964
895 4
896 1124881
897 22
898 149
899 10
900 23513
901 18
902 513
903 32
904 11199
905 46
906 768
907 2
908 1494
909 14
910 788
911 22
912 51777
913 48
914 250
915 154
916 626
917 12
918 470
919 14
920 10666
921 12
922 113
924 6344
925 100
926 385
927 56
928 243390
929 6
930 2275
931 100
932 8356
933 34
934 642
935 24
936 35248
937 14
938 326
939 2
940 3554
941 8
942 488
943 34
944 14796
945 120
946 353
947 42
948 4230
949 36
950 147
951 26
952 10939
953 2
954 599
955 74
956 1015
957 14
958 214
959 12
960 852866
961 28
962 237
963 12
964 1725
965 8
966 398
967 12
968 11237
969 38
970 448
971 18
972 2301
973 6
974 109
975 64
976 54677
977 52
978 638
979 46
980 3002
981 50
982 256
983 8
984 5767
985 6
986 207
987 10
988 2711
989 20
990 1363
992 165788
993 4
994 252
995 6
996 1453
997 16
998 112
999 18
1000 7705
1001 34
1002 376
1003 24
1004 547
1005 12
1006 475
1007 72
1008 67597
1009 22
1010 142
1011 6
1012 1679
1013 38
1014 305
1015 8
1016 2960
1017 22
1018 98
1020 4157
1021 8
1022 268
1023 70
1024 2570777
1025 28
1026 489
1027 28
1028 805
1029 18
1030 149
1031 4
1032 6650
1033 2
1034 84
1035 22
1036 708
1037 16
1038 390
1039 8
1040 40324
1041 32
1042 124
1043 6
1044 6505
1045 8
1046 134
1047 10
1048 2175
1050 2409
1052 435
1053 34
1054 361
1055 8
1056 56666
1057 16
1058 143
1059 10
1060 2090
1062 399
1063 46
1064 5526
1065 10
1066 283
1067 46
1068 949
1069 2
1070 104
1071 8
1072 5438
1073 36
1074 71
1075 18
1076 776
1077 44
1078 249
1079 4
1080 38852
1081 28
1082 197
1083 148
1084 1543
1085 62
1086 203
1087 4
1088 64199
1089 12
1090 96
1091 2
1092 4836
1094 38
1095 32
1096 2160
1098 718
1099 4
1100 643
1102 128
1103 2
1104 15912
1105 6
1106 448
1107 10
1108 612
1109 4
1110 352
1111 8
1112 1786
1113 4
1114 218
1115 2
1116 4960
1117 2
1118 194
1119 6
1120 69123
1121 8
1122 136
1123 2
1124 587
1125 30
1126 37
1127 2
1128 4561
1129 16
1130 235
1131 20
1132 348
1134 215
1135 12
1136 5815
1137 12
1138 109
1140 4268
1141 2
1142 109
1143 6
1144 4435
1145 14
1146 122
1147 10
1148 1212
1149 10
1150 187
1151 2
1152 237484
1153 2
1154 90
1155 50
1156 509
1158 173
1159 4
1160 12501
1161 6
1162 74
1163 4
1164 2100
1165 114
1166 175
1168 5978
1169 6
1170 748
1171 2
1172 1305
1173 10
1174 93
1175 6
1176 9055
1178 334
1179 6
1180 958
1181 10
1182 82
1184 8942
1185 48
1186 84
1188 1743
1189 12
1190 192
1191 8
1192 2467
1194 47
1196 621
1197 2
1198 93
1199 4
1200 43923
1202 43
1203 6
1204 779
1205 22
1206 92
1208 3028
1209 2
1210 198
1211 8
1212 478
1213 6
1214 53
1215 10
1216 21305
1217 6
1218 558
1220 2056
1221 10
1222 279
1223 8
1224 3106
1225 16
1226 41
1227 12
1228 198
1230 294
1231 2
1232 11117
1233 2
1234 69
1236 1225
1237 6
1238 25
1239 2
1240 8312
1241 2
1242 178
1244 291
1245 14
1246 83
1247 6
1248 74708
1250 157
1251 12
1252 252
1253 2
1254 228
1256 1335
1257 40
1258 138
1259 2
1260 8726
1261 6
1262 40
1263 2
1264 10548
1266 183
1267 28
1268 249
1269 8
1270 65
1271 14
1272 3688
1274 136
1275 44
1276 748
1277 4
1278 92
1280 217247
1281 26
1282 43
1283 8
1284 715
1286 33
1287 8
1288 2086
1290 172
1292 159
1293 8
1294 76
1295 4
1296 5566
1298 105
1299 2
1300 604
1302 416
1304 403
1305 8
1306 69
1307 2
1308 513
1309 2
1310 47
1312 8309
1314 198
1315 12
1316 496
1318 29
1319 2
1320 6495
1322 20
1324 110
1325 8
1326 116
1327 4
1328 1224
1329 14
1330 66
1332 445
1333 2
1334 47
1336 737
1338 64
1339 2
1340 238
1341 4
1342 134
1343 6
1344 129544
1346 22
1348 128
1350 634
1351 8
1352 1580
1353 4
1354 13
1355 12
1356 823
1358 178
1359 4
1360 5513
1362 138
1363 4
1364 1234
1365 30
1366 61
1367 6
1368 3305
1369 2
1370 47
1371 4
1372 501
1373 6
1374 39
1375 6
1376 7817
1377 6
1378 74
1380 1124
1382 43
1383 4
1384 828
1385 4
1386 193
1388 114
1389 4
1390 25
1392 28547
1394 41
1395 42
1396 173
1398 413
1400 4026
1401 6
1402 9
1403 12
1404 1890
1405 6
1406 24
1407 6
1408 42174
1410 229
1412 124
1414 56
1416 2191
1417 10
1418 51
1419 2
1420 175
1421 4
1422 179
1424 1404
1425 6
1426 115
1428 1054
1430 46
1431 2
1432 191
1433 2
1434 136
1436 228
1438 20
1440 94935
1441 8
1442 132
1443 2
1444 964
1446 120
1447 8
1448 770
1450 62
1451 6
1452 673
1454 9
1455 10
1456 10356
1458 23
1460 350
1462 16
1463 32
1464 4892
1465 2
1466 40
1467 18
1468 419
1469 2
1470 511
1472 19291
1473 2
1474 49
1475 2
1476 448
1478 3
1479 8
1480 1146
1482 146
1484 569
1485 8
1486 14
1487 4
1488 12798
1490 110
1491 4
1492 194
1494 26
1495 4
1496 486
1498 35
1500 1150
1501 16
1502 38
1504 4534
1506 30
1508 248
1509 2
1510 104
1512 3822
1513 2
1514 35
1515 2
1516 208
1518 93
1519 12
1520 1708
1521 6
1522 12
1523 2
1524 291
1525 4
1526 40
1528 367
1530 117
1532 74
1533 2
1534 16
1535 4
1536 316192
1537 10
1538 12
1539 4
1540 227
1542 37
1544 703
1545 2
1546 20
1548 223
1549 6
1550 65
1551 2
1552 4979
1554 53
1556 110
1557 4
1558 44
1560 4666
1562 9
1563 2
1564 146
1566 148
1568 11221
1570 26
1572 236
1574 8
1575 28
1576 336
1578 20
1580 514
1581 10
1582 87
1584 4286
1586 42
1587 10
1588 77
1590 68
1591 4
1592 297
1593 2
1594 30
1596 967
1598 46
1600 9768
1601 2
1602 53
1604 70
1606 18
1608 497
1610 36
1612 357
1614 50
1615 12
1616 593
1618 7
1620 1780
1621 2
1622 21
1623 2
1624 1979
1626 81
1627 2
1628 175
1629 10
1630 8
1631 8
1632 7947
1634 29
1635 2
1636 50
1637 6
1638 154
1640 511
1642 19
1644 182
1646 12
1648 1097
1649 6
1650 82
1652 307
1653 4
1654 38
1656 1038
1658 3
1659 4
1660 83
1662 16
1664 80065
1666 13
1668 128
1669 2
1670 3
1671 2
1672 302
1674 174
1676 52
1677 2
1678 16
1680 25061
1682 17
1684 66
1686 27
1688 438
1690 31
1692 312
1693 4
1694 40
1696 6165
1698 31
1700 372
1702 13
1703 12
1704 755
1705 4
1706 5
1708 439
1710 229
1712 911
1714 4
1716 264
1718 9
1720 589
1722 41
1723 6
1724 67
1726 116
1728 15191
1730 27
1731 4
1732 35
1733 4
1734 24
1736 2035
1738 32
1740 902
1742 8
1744 576
1746 178
1747 4
1748 62
1749 8
1750 109
1752 735
1754 8
1755 2
1756 45
1757 4
1758 112
1760 2901
1762 2
1763 2
1764 356
1766 12
1767 32
1768 366
1770 27
1771 2
1772 237
1774 14
1776 906
1778 82
1780 62
1782 18
1784 167
1786 4
1788 379
1790 2
1792 102227
1794 21
1795 2
1796 63
1797 2
1798 9
1799 2
1800 5006
1802 3
1804 126
1805 18
1806 40
1808 2031
1810 14
1812 196
1813 2
1814 5
1816 261
1818 53
1820 202
1822 22
1823 2
1824 6050
1826 6
1828 53
1829 2
1830 80
1832 121
1833 2
1834 15
1836 181
1838 27
1840 1643
1841 4
1842 15
1844 38
1845 2
1846 5
1848 897
1849 2
1850 13
1852 71
1854 27
1855 20
1856 40338
1858 10
1859 2
1860 781
1862 13
1864 3010
1866 7
1868 214
1869 2
1870 7
1872 5319
1874 7
1875 20
1876 63
1878 4
1880 632
1881 2
1883 6
1884 189
1885 4
1886 24
1888 2083
1890 281
1891 4
1892 58
1894 16
1896 946
1898 24
1900 46
1902 15
1904 1698
1906 8
1908 260
1910 70
1912 138
1914 34
1916 60
1918 4
1919 2
1920 94506
1922 19
1924 80
1926 10
1928 294
1930 6
1932 134
1933 2
1934 4
1935 6
1936 1776
1937 4
1938 20
1939 2
1940 301
1942 1
1944 297
1945 2
1946 8
1948 17
1950 30
1952 8850
1954 31
1956 243
1958 13
1960 441
1962 8
1964 34
1966 28
1968 580
1970 12
1972 90
1974 2
1976 374
1978 7
1980 334
1982 27
1984 19586
1986 6
1988 27
1989 4
1990 7
1992 246
1996 15
1998 8
2000 863
2002 39
2003 6
2004 83
2006 7
2008 75
2010 8
2012 108
2014 2
2016 6230
2017 4
2018 8
2019 2
2020 41
2022 2
2024 291
2026 13
2028 82
2030 16
2032 435
2034 27
2036 15
2038 2
2040 870
2041 8
2042 5
2044 85
2046 32
2048 211416
2050 8
2052 240
2053 2
2054 4
2056 145
2058 11
2060 23
2062 5
2064 861
2066 19
2068 13
2070 5
2072 64
2074 49
2076 60
2078 7
2080 4835
2082 5
2084 26
2086 13
2088 1395
2090 8
2092 73
2094 20
2096 360
2098 6
2100 926
2102 2
2104 67
2106 29
2108 84
2110 4
2112 5550
2114 14
2116 50
2118 8
2120 411
2122 2
2124 108
2126 2
2128 584
2130 13
2132 72
2134 35
2136 128
2138 4
2140 60
2141 4
2142 20
2144 627
2146 19
2148 25
2150 7
2151 2
2152 147
2153 12
2154 23
2156 74
2160 5083
2162 14
2164 52
2166 61
2168 333
2170 12
2172 62
2174 14
2176 7660
2178 15
2179 8
2180 20
2182 3
2184 651
2186 9
2187 2
2188 20
2190 29
2192 287
2194 6
2196 237
2198 18
2200 81
2202 45
2204 41
2206 1
2208 1749
2209 4
2210 3
2212 88
2214 26
2216 116
2218 5
2220 89
2222 2
2224 245
2226 4
2228 44
2230 5
2232 970
2234 2
2236 40
2238 15
2240 6176
2242 2
2244 32
2248 80
2250 18
2252 13
2254 3
2256 445
2258 30
2260 67
2262 23
2264 20
2266 2
2268 126
2271 2
2272 655
2274 8
2275 4
2276 23
2278 1
2280 641
2282 10
2284 68
2286 2
2288 474
2290 6
2292 22
2294 2
2296 126
2300 31
2304 19001
2306 9
2308 15
2310 66
2312 61
2316 38
2318 2
2320 2339
2322 1
2324 14
2326 1
2328 475
2330 97
2332 32
2335 6
2336 593
2338 1
2340 226
2342 5
2344 380
2346 5
2348 10
2350 7
2352 734
2353 12
2355 2
2356 71
2358 3
2360 123
2362 21
2364 35
2366 3
2368 917
2370 25
2372 16
2376 268
2378 5
2379 4
2380 47
2382 6
2384 446
2386 3
2388 14
2389 2
2390 2
2392 64
2394 14
2396 26
2400 4868
2402 1
2404 17
2406 3
2408 94
2410 8
2412 23
2416 500
2418 13
2420 55
2422 2
2424 80
2426 2
2428 11
2430 33
2432 1727
2434 10
2435 2
2436 166
2440 491
2442 9
2444 147
2448 372
2450 13
2451 2
2452 5
2454 7
2456 34
2460 41
2464 1183
2466 2
2468 61
2470 1
2472 153
2478 3
2480 840
2482 1
2484 14
2486 5
2488 33
2490 13
2492 39
2494 4
2496 6481
2497 2
2498 1
2500 33
2502 11
2504 33
2506 3
2508 23
2512 157
2514 18
2516 23
2520 1506
2522 3
2524 17
2526 1
2528 1362
2530 4
2532 32
2534 3
2536 14
2540 15
2542 4
2544 294
2548 37
2550 35
2552 144
2554 1
2556 9
2558 8
2560 15613
2562 22
2564 11
2568 77
2570 2
2572 11
2574 6
2576 311
2577 2
2578 2
2580 20
2582 1
2584 21
2586 3
2588 10
2590 3
2592 390
2594 1
2596 20
2598 4
2600 90
2602 1
2604 83
2608 45
2610 6
2612 20
2614 4
2616 42
2618 4
2620 21
2622 1
2624 645
2626 3
2628 44
2630 1
2632 59
2634 10
2635 4
2636 6
2638 3
2640 654
2642 5
2644 1
2648 20
2650 1
2652 25
2656 140
2658 6
2660 26
2662 4
2664 50
2666 1
2668 16
2672 58
2676 15
2678 14
2680 8
2682 9
2683 4
2684 25
2686 5
2688 8542
2692 6
2694 5
2696 18
2698 6
2700 136
2704 202
2706 7
2708 6
2710 16
2712 110
2716 40
2718 8
2720 499
2724 51
2726 3
2728 131
2730 9
2732 12
2736 193
2740 9
2744 63
2748 1
2750 4
2752 626
2754 14
2756 6
2760 170
2762 2
2764 2
2766 2
2768 105
2770 3
2772 7
2774 3
2776 36
2777 2
2778 2
2780 12
2784 3714
2786 2
2788 1
2790 48
2791 2
2792 20
2796 126
2800 532
2802 7
2804 2
2806 4
2808 253
2810 2
2812 10
2816 3205
2820 17
2821 8
2824 22
2828 10
2832 188
2836 10
2838 10
2840 43
2842 15
2844 39
2848 139
2850 3
2852 10
2856 96
2858 1
2860 10
2862 4
2864 27
2868 15
2872 17
2874 1
2876 10
2878 1
2880 8114
2882 8
2884 40
2888 266
2890 4
2892 15
2894 8
2896 87
2898 2
2900 26
2902 2
2904 69
2908 1
2910 10
2912 671
2914 2
2916 3
2920 73
2924 3
2928 621
2930 2
2932 14
2934 3
2936 67
2938 1
2939 4
2940 189
2944 1672
2948 17
2952 28
2954 7
2956 1
2958 10
2960 141
2964 16
2968 83
2970 16
2972 1
2974 1
2976 1114
2980 22
2982 1
2984 24
2988 3
2990 3
2992 58
2996 12
3000 225
3002 5
3004 7
3006 6
3008 392
3010 8
3012 11
3014 2
3016 21
3017 2
3018 6
3020 31
3024 329
3028 2
3030 1
3032 32
3034 5
3036 16
3038 4
3040 182
3042 4
3044 1
3046 5
3048 40
3056 34
3058 4
3060 24
3064 9
3068 14
3070 6
3072 18289
3073 8
3080 5
3082 3
3084 4
3085 8
3088 86
3096 70
3098 3
3100 12
3102 4
3104 514
3108 14
3112 10
3114 2
3116 2
3120 354
3124 9
3126 1
3128 28
3132 112
3134 1
3136 755
3140 1
3144 27
3148 1
3150 61
3152 39
3156 5
3160 84
3162 6
3164 14
3168 366
3170 8
3172 2
3174 1
3176 7
3178 1
3180 20
3184 39
3186 1
3188 7
3190 1
3192 98
3194 1
3196 5
3200 590
3204 2
3206 4
3208 9
3212 5
3214 3
3216 48
3220 1
3224 39
3228 14
3232 68
3234 1
3236 2
3240 255
3242 1
3244 3
3248 297
3252 30
3256 12
3258 6
3260 2
3262 10
3264 712
3270 5
3272 8
3274 1
3276 35
3280 23
3282 1
3286 2
3288 14
3292 4
3294 12
3296 112
3298 1
3300 7
3304 50
3306 1
3308 15
3312 86
3320 26
3324 4
3328 5614
3330 3
3332 1
3336 13
3338 4
3340 2
3342 13
3344 22
3348 24
3352 27
3354 2
3360 2437
3364 7
3368 3
3372 7
3376 39
3380 11
3384 12
3388 23
3392 521
3396 1
3400 77
3404 1
3406 2
3408 65
3412 3
3416 52
3420 10
3424 88
3426 12
3432 25
3440 52
3444 4
3446 1
3448 16
3452 17
3454 4
3456 850
3458 2
3460 1
3464 1
3466 1
3468 4
3472 161
3476 7
3480 119
3488 53
3492 36
3496 3
3500 50
3502 1
3504 60
3508 4
3512 23
3516 19
3518 3
3520 257
3524 4
3528 24
3530 2
3532 6
3534 2
3536 13
3540 19
3544 33
3548 4
3552 75
3556 12
3560 2
3564 4
3566 2
3568 13
3576 62
3582 1
3584 5714
3588 3
3590 4
3592 19
3596 3
3600 483
3604 1
3608 26
3610 14
3612 9
3616 241
3620 14
3624 38
3628 1
3632 22
3634 1
3636 17
3638 2
3640 20
3644 8
3648 335
3656 7
3660 9
3662 1
3664 6
3666 3
3668 3
3672 10
3676 2
3678 2
3680 98
3682 2
3684 1
3692 2
3696 46
3700 3
3704 4
3708 7
3712 4448
3716 2
3720 84
3722 1
3724 2
3728 500
3732 1
3736 30
3740 3
3744 458
3752 4
3754 2
3756 1
3760 46
3762 1
3766 3
3768 23
3772 6
3774 3
3776 113
3780 91
3782 4
3784 4
3786 1
3788 4
3792 66
3794 3
3798 1
3800 5
3804 2
3808 164
3810 2
3816 14
3820 7
3824 29
3828 3
3836 22
3840 6211
3844 4
3848 4
3852 1
3856 13
3860 3
3864 21
3868 2
3872 128
3880 38
3884 1
3888 28
3890 1
3900 2
3904 940
3906 2
3908 7
3912 25
3916 1
3920 18
3924 1
3928 1
3934 1
3936 46
3938 6
3944 9
3946 2
3948 3
3952 16
3954 1
3956 2
3960 21
3964 3
3968 1245
3976 1
3980 1
3984 20
3992 1
4000 84
4002 1
4004 11
4008 2
4012 1
4016 12
4018 1
4020 4
4024 11
4032 357
4048 23
4050 5
4052 1
4056 6
4060 3
4062 1
4064 21
4066 1
4068 8
4072 4
4080 73
4082 2
4088 5
4092 1
4096 10935
4100 1
4102 4
4104 20
4110 1
4112 8
4120 1
4128 84
4132 3
4134 2
4140 2
4144 12
4146 1
4148 3
4152 1
4156 4
4160 306
4168 4
4176 222
4180 1
4184 3
4188 1
4192 23
4194 5
4200 146
4204 1
4208 8
4212 10
4214 1
4216 14
4224 318
4228 3
4232 5
4234 1
4238 1
4240 11
4244 1
4248 4
4250 1
4252 1
4256 29
4260 3
4264 3
4266 4
4268 9
4280 6
4284 9
4288 28
4302 1
4304 6
4312 11
4320 399
4326 16
4332 21
4336 50
4340 1
4344 6
4352 520
4356 12
4358 8
4368 27
4376 2
4380 4
4384 22
4386 2
4392 22
4396 6
4398 1
4400 6
4404 3
4408 2
4416 154
4424 18
4432 4
4436 1
4440 2
4444 3
4448 14
4450 12
4456 2
4464 69
4472 4
4480 266
4488 2
4494 8
4496 2
4500 2
4504 2
4512 31
4516 6
4520 12
4528 3
4536 3
4544 27
4546 1
4548 4
4552 3
4560 31
4564 1
4568 5
4576 29
4592 4
4600 2
4608 765
4612 2
4616 2
4620 12
4624 6
4632 6
4640 388
4648 1
4652 1
4656 45
4660 23
4672 55
4680 22
4688 47
4696 2
4700 4
4704 29
4706 8
4712 11
4720 2
4724 7
4728 2
4736 56
4742 1
4744 2
4752 49
4768 25
4772 3
4776 1
4784 5
4792 3
4800 334
4808 1
4812 1
4816 1
4824 2
4832 38
4834 1
4836 1
4840 18
4844 4
4848 1
4860 12
4864 72
4872 4
4880 51
4888 19
4896 31
4912 4
4920 2
4928 43
4936 5
4944 10
4956 2
4960 19
4968 1
4976 4
4984 3
4992 272
5000 9
5008 9
5012 1
5016 3
5020 1
5022 1
5024 1
5028 4
5040 58
5044 1
5052 1
5054 2
5056 84
5064 3
5088 9
5096 2
5100 4
5104 10
5120 623
5124 1
5136 8
5144 1
5148 1
5152 11
5168 2
5172 1
5176 1
5180 1
5184 29
5192 2
5200 1
5208 3
5216 2
5228 1
5232 1
5248 26
5250 4
5264 6
5272 1
5280 34
5284 2
5288 1
5294 1
5300 1
5312 2
5316 2
5328 2
5344 6
5356 6
5368 2
5376 266
5388 1
5400 6
5402 1
5408 1
5420 2
5424 4
5432 6
5436 4
5440 37
5448 2
5456 4
5460 1
5472 7
5480 1
5488 4
5504 17
5520 8
5536 10
5568 390
5580 3
5584 1
5592 27
5600 70
5604 1
5616 8
5632 175
5640 6
5648 3
5651 2
5664 9
5680 15
5684 5
5688 3
5696 1
5712 3
5728 1
5730 1
5740 3
5760 369
5768 1
5776 69
5784 4
5792 4
5800 12
5808 3
5820 4
5822 2
5824 7
5840 4
5856 58
5868 2
5872 2
5880 7
5888 75
5892 1
5920 9
5948 1
5952 36
5960 1
5964 1
5984 4
5992 13
6000 2
6016 20
6024 4
6040 2
6048 1
6064 2
6080 17
6112 2
6128 1
6140 2
6144 492
6176 4
6196 3
6200 1
6204 2
6208 30
6212 1
6240 9
6248 2
6264 5
6272 16
6300 5
6336 9
6368 2
6372 1
6384 3
6400 8
6432 1
6448 2
6460 1
6464 6
6480 4
6496 36
6524 5
6528 18
6548 1
6576 1
6592 5
6600 1
6608 1
6624 2
6640 4
6656 184
6672 2
6680 1
6696 1
6720 116
6736 2
6752 1
6784 5
6800 5
6816 3
6832 10
6848 1
6852 1
6864 3
6880 3
6912 24
6960 22
6984 2
7000 2
7008 1
7024 2
7040 7
7056 1
7068 2
7072 1
7080 2
7104 2
7128 1
7152 14
7168 163
7200 7
7220 7
7232 17
7264 1
7266 1
7296 15
7424 310
7440 6
7456 55
7472 2
7480 2
7488 11
7502 2
7520 2
7536 4
7560 10
7568 2
7584 3
7616 9
7680 232
7728 1
7760 4
7766 2
7776 2
7808 60
7812 1
7920 2
7936 42
8000 9
8032 4
8064 9
8100 1
8128 1
8160 13
8184 1
8192 288
8256 8
8296 5
8320 12
8352 10
8368 2
8384 1
8388 2
8400 7
8448 10
8480 1
8640 10
8672 2
8700 1
8704 13
8716 1
8768 7
8784 2
8792 2
8832 5
8960 3
8992 1
9088 7
9136 4
9216 25
9240 1
9248 1
9280 21
9312 3
9320 2
9344 6
9360 3
9376 1
9472 2
9504 4
9728 7
9984 5
10080 1
10112 2
10240 10
10336 2
10396 1
10560 2
10752 5
10816 1
11008 2
11072 2
11136 5
11168 1
11200 4
11264 3
11520 4
11552 2
11648 1
11776 5
11904 2
12032 2
12288 16
12416 2
13184 2
13440 4
13600 2
14304 2
14848 9
14912 3
15360 4
16320 2
```
### A.12 `en_k.w`: the counted program simulated end to end over uniform x and cb (Tungsten; shard 0 shown; `seed` = 201 + k, `nx` = 60000)

The library of A.4 (without its main), the bitwise F6 test and the chunk-operation count, then the simulation of Section 13.4.

```text
-> f6b(w) (i64) i64
  b1 = 0 ## i64
  b2 = 0 ## i64
  b3 = 0 ## i64
  b8 = 0 ## i64
  b9 = 0 ## i64
  b10 = 0 ## i64
  b12 = 0 ## i64
  b13 = 0 ## i64
  b14 = 0 ## i64
  b15 = 0 ## i64
  b16 = 0 ## i64
  b18 = 0 ## i64
  b19 = 0 ## i64
  b20 = 0 ## i64
  b25 = 0 ## i64
  b26 = 0 ## i64
  b27 = 0 ## i64
  b29 = 0 ## i64
  b30 = 0 ## i64
  b31 = 0 ## i64
  common = 0 ## i64
  bc = 0 ## i64
  xx = 0 ## i64
  fail = 0 ## i64
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


-> chunk_ops(nl) (i64) i64
  nch = (nl + 23) / 24 ## i64
  ops = 0 ## i64
  c = 0 ## i64
  a = 0 ## i64
  while c < nch
    a = 2
    a = 0 if nch == 1
    a = 1 if nch > 1 && (c == 0 || c == nch - 1)
    ops += a + 1
    c += 1
  ops

-> main_run(dummy) (i64) i64
  nx = 60000 ## i64
  seed = 201 ## i64
  nth = 4 ## i64
  th = i64[4]
  th[0] = 20
  th[1] = 30
  th[2] = 40
  th[3] = 60
  keys = i64[12103700]
  n = 0 ## i64
  e4 = 0 ## i64
  a0 = 0 ## i64
  while e4 < 536870912
    a0 = (e4 - 734766) & 4294967295
    if in_g(a0) == 1
      keys[n] = (c7_of(a0) << 32) | a0
      n += 1
    e4 += 1
  heapsort(keys, n)
  cstart = i64[23000]
  c7c = i64[23000]
  ncls = 0 ## i64
  i = 0 ## i64
  j = 0 ## i64
  while i < n
    cstart[ncls] = i
    c7c[ncls] = keys[i] >> 32
    j = i
    while j < n && (keys[j] >> 32) == c7c[ncls]
      j += 1
    ncls += 1
    i = j
  cstart[ncls] = n
  phis = i64[4000000]
  s_f = i64[4]
  s_v = i64[4]
  s_gr = i64[4]
  s_pf = i64[4]
  s_good = i64[4]
  s_grp = i64[4]
  s_ops = i64[4]
  s_ops2 = i64[4]
  s_good2 = i64[4]
  s_v2 = i64[4]
  f_k = i64[4]
  v_k = i64[4]
  gr_k = i64[4]
  pf_k = i64[4]
  good_k = i64[4]
  grp_k = i64[4]
  sops_k = i64[4]
  s_sops = i64[4]
  rng = 0 ## i64
  rng = 987654321987654321 + seed * 1000003
  t = 0 ## i64
  x = 0 ## i64
  cb = 0 ## i64
  m = 0 ## i64
  c = 0 ## i64
  w = 0 ## i64
  k = 0 ## i64
  sz = 0 ## i64
  q = 0 ## i64
  v = 0 ## i64
  nb = 0 ## i64
  nl = 0 ## i64
  ops = 0 ## i64
  full = chunk_ops(256) ## i64
  while t < nx
    rng = rng * 6364136223846793005 + 1442695040888963407
    x = (rng >> 32) & 4294967295
    rng = rng * 6364136223846793005 + 1442695040888963407
    cb = (rng >> 32) & 4294967295
    m = 0
    c = 0
    while c < ncls
      w = (c7c[c] - x) & 4294967295
      if f7b(w) == 1
        k = cstart[c]
        while k < cstart[c + 1]
          a0 = keys[k] & 4294967295
          phis[m] = phi_of(a0, x)
          m += 1
          k += 1
      c += 1
    heapsort(phis, m)
    q = 0
    while q < nth
      f_k[q] = 0
      v_k[q] = 0
      gr_k[q] = 0
      pf_k[q] = 0
      good_k[q] = 0
      grp_k[q] = 0
      sops_k[q] = 0
      q += 1
    i = 0
    while i < m
      j = i
      while j < m && phis[j] == phis[i]
        j += 1
      sz = j - i
      v = phis[i]
      q = 0
      while q < nth
        if sz >= th[q]
          f_k[q] += 1
          v_k[q] += sz
          gr_k[q] += (sz + 3) / 4
          if f6b((v + cb) & 4294967295) == 1
            pf_k[q] += 1
            good_k[q] += sz
            grp_k[q] += (sz + 3) / 4
            sops_k[q] += 9 + 3 * (((sz + 3) / 4) / 8) + 46 * ((sz + 3) / 4)
        q += 1
      i = j
    q = 0
    while q < nth
      ops = 54
      if f_k[q] > 0
        nb = (f_k[q] + 255) / 256
        nl = f_k[q] - 256 * (nb - 1)
        ops = 264 + (nb - 1) * (230 + 71 + full) + 230 + 71 + chunk_ops(nl)
        ops += 1 if nl < 256
        ops += pf_k[q] * 12 + sops_k[q]
      s_f[q] += f_k[q]
      s_v[q] += v_k[q]
      s_gr[q] += gr_k[q]
      s_pf[q] += pf_k[q]
      s_good[q] += good_k[q]
      s_grp[q] += grp_k[q]
      s_sops[q] += sops_k[q]
      s_ops[q] += ops
      s_ops2[q] += ops * ops
      s_good2[q] += good_k[q] * good_k[q]
      s_v2[q] += v_k[q] * v_k[q]
      q += 1
    t += 1
  q = 0
  while q < nth
    << "EN [th[q]] nx=[nx] F=[s_f[q]] V=[s_v[q]] GR=[s_gr[q]] PF=[s_pf[q]] good=[s_good[q]] grp=[s_grp[q]] sops=[s_sops[q]] ops=[s_ops[q]] ops2=[s_ops2[q]] good2=[s_good2[q]] v2=[s_v2[q]]"
    q += 1
  0
main_run(0)

```

