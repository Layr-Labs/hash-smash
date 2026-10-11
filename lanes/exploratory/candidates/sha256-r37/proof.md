# Collision attack on 37-step SHA-256: the ePrint 2026/1120 two-block attack over the whole variant family G, with an x-indexed table of merged W6 fibres, 2^61.20057

Track `sha256-r37-exploratory`, target `sha256-r37-prefix-v1`, cost model `collision-frontier-v5` (C = 2644).
Claim: `time_log2 = 61.20057` target compressions on every run, success probability at least 0.39 (0.3900000044 under the stated premises),
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
the lower per-pair cost of large fibres makes it worthwhile to examine 121,899 variants per first block (on average) out of the whole family G (12,103,680 variants in 22,976 classes), so a first block yields
8,074 good pairs instead of 831 and N_FB falls by a factor of about 9.4 while the work per good pair falls too. The set of good pairs found among the examined variants is *exactly* the set defined by the
filters (Lemma 8.1, checked against brute force in Section 13).
**Inheritance, stated up front:** the Monte-Carlo estimate of q3 (premise H2) and the evidence for H3 are 7319bba's and were *not* re-run for this filing; q3 is defined as the mean over a family of variants, and this filing's examined family
is a different subset of the same family G (H2 explains why the dependence on the variant is a tail factor of 2^-4, and prices a hedge of 0.05 bit).

## 0. Summary

- **Algorithm (Sections 4-8).** Messages M0 || M1 and M0 || M1' (128 bytes; padding adds the same third block). A first block M0 is two fresh uniform 256-bit
  words; CV1 = F_37(IV, M0) costs one unit. One table read at x = A_{-1} returns the record R(x): the kept fibres (at least THETA = 40 variants with equal phi) of the variants of G whose class passes c7 - x in F7, as
  bit planes of the fibre values, fibre entries and contiguous member blocks. For each batch of 256 fibres the program adds cb = C6 - A_{-2} to the fibre values bit-sliced and applies F6; the members of each passing fibre are good pairs.
  They are processed in packed groups of four: u = W0 + s0(W1) and an exact row-16 mask-table lookup over the 32 elements of L* for every lane; each row-16 pass is checked through row 36. A pair that follows
  every cell of rows 16..36 collides; it is verified with the target and output.
- **Rates.** Per first block (means over uniform x, Tungsten, Section 13.3): 1,219.8 kept fibres, 121,899 kept variants, hence g = p6 x 121,899 / 1.01 = 8,074 examined good pairs (a lower bound)
  (p6 = |F6|/2^32 = 2^-3.90197; the statistics are scaled by 1.01 in the unfavourable direction).
- **Probability (Section 7, H2).** q3 = average over the examined variants and l in L* of Pr[rows 16..36 follow every cell and printed two-bit condition]
  = at least 2^-74.08 (the registered floor of the preregistered studies of 7319bba, Section 7.4, study B registered bound less the hedge of Section 7.6; not re-run here).
- **Cost (Sections 9, 11).** N_FB = 38,278,771,277,512,846 first blocks (2^55.08739); per first block 1 unit plus 264 counted data-independent operations, plus on average
  100,298 counted data-dependent operations (1,936 for fibre tests and scans, 96,216 for the packed groups and row-16 lookups, 1,157 for rows >= 16), capped by V_MAX. T = A_C + A_S + DEV + N_FB + (N_FB x 264 + V_MAX + overshoot + preprocessing + final)/C + 6 = 1,751,485,538,759,125,556,364 / 661 = 2^61.200563,
  claimed 61.20057. The earlier best on the board is 61.51197 (f2fe1d4d); this filer's d3ec5c41 is 61.71473.
- **Premises (Section 12).** H1 uniform independent chaining values; H2 q3 >= 2^-74.08 for the examined family (inherited, not re-run); H3 given one success, at most 2^-9.4 further expected successes in the same
  first block (inherited, stated for the new family); H4 advice allowances (A_C = 2^60, A_S = 2^50, DEV = 2^40, as in the accepted filings); H5 counted word-RAM pricing (every executed primitive costs one, address additions included; memory is reported only); H7 the exact success floor of 087a18c4;
  **H9 the table statistics and the preprocessing bound**. No decision-DAG branch pricing is used.
- **Checks (Section 13).** Exhaustive in Tungsten: |F6| = 287,309,824 and |F7| = 68,157,440 and their bitwise forms against the definitions on all 2^32 words (0 mismatches),
  |G| = 12,103,680 and its 22,976 classes; the table pipeline against brute-force filtering (selftest and organizer experiments, 0 mismatches); the fibre statistics over 800,000 uniform values of x (Tungsten, eight shards);
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
taken from all 22,976 classes (on average 121,899 variants per first block). The 222 classes of the earlier filings stay embedded in `xtab.py` (descriptors below) because the organizer sandbox (128 MiB, 20 s) cannot hold the whole family:
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
12,103,680 p7 = 192,075 (exact; the Tungsten sample mean of Section 13.3 is 192,233). Passing classes are strongly correlated (their c7 values are close), so the counts are bursty (the standard deviation across x is about twice the mean);
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
61.19494 (Section 11.2).

### 7.5 Consistency

- Lemma 7.1 makes rows 16..22 identical by construction; the paired rows-23..36 rates of the variants' and the published W8 differ by 0.002 bit in study B (7319bba).
- Real first blocks (7319bba, quoted in Section 13.1): the row-16 pass rate of the attack's own good pairs is the exact 2^-12 (z = +0.88 and +0.51 over 424,363 and 1,693,297 passes).
  This filing's end-to-end run (Section 13.4) finds row-16 passes at the same rate (2.423e-04 per good pair).


### 7.6 The examined family of this filing (new; the premise H2 is stated for it)

The registered studies drew W8 from the 782,800 variants of the 222 largest classes. This filing examines a different subset of the same family G (the variants of fibres with at least THETA members, from all 22,976 classes).
By Lemma 7.1 a variant changes nothing in rows 16..22 and enters rows 23..36 only through W8, i.e. through the four conditions on W24x = Z + W8x; if Z were exactly uniform given rows 16..22 these four conditions would hold with probability exactly 2^-4 for *every* W8x
(W24x would be uniform), so q3 would be the same for every subset of G. The same holds one stage earlier: W7 enters rows 16..36 only through W22 = s1(W20) + W15 + s0(W7) + W6, whose x-conditions (row 22: 11 bits) hold with probability 2^-11 for every (W6, W7) if s1(W20) + W15 is uniform given rows 16..21. The examined pairs are not uniform on F7: x = c7 - W7 is selected, so the law of W7 among examined good pairs is weighted by the number of kept variants at x = c7 - W7 (and the same for W6 only through cb, which is independent). Both facts are premises, not measurements, for the new subset. The stage factor of that tail in the registered studies is 2^-4.015 (study A) and 2^-4.007 (study B) against the exact 2^-4, and the paired comparison with the published W8 differs by 0.002 bit: the dependence on W8 is below the sampling resolution.
The premise H2 is therefore stated for the examined family with a hedge: **q3_used = 2^-74.08**, i.e. 0.05 bit below the registered bound 2^-74.03, covering a tail factor and a row-22 factor that differ from the studies' by up to that amount for the new subset (the hedge was raised from 0.02 to 0.05 bit after a reviewer pointed out that the examined pairs weight W7 by the number of kept variants at x = c7 - W7). This is a premise, not a re-estimate: the SMC program of 7319bba was not run here (Appendix A.7), and no
claim is made that the new subset's tail factor was measured. Section 11.2 prices the hedge: removing it (q3 = 2^-74.03) lowers log2 T by 0.02797.

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

- **Expectation.** E[X_f] = g x 32 x q3 (Lemma 5.1 and Section 7) with g = p6 E_x|E(x)| the expected number of examined good pairs per first block, and E[X] = N_FB g 32 q3. With g >= g_low (the sampled mean of Section 13.3 divided by the statistics safety factor 1.01, H9)
  and q3 >= q3_used (H2): E[X] >= N_FB g_low 32 q3_used >= mu0 = 0.49530733 (H7) for N_FB = ceil(mu0 / (g_low 32 q3_used)) = 38,278,771,277,512,846 = 2^55.08739;
  mu0 is the smallest 8-decimal number strictly above -ln(0.61 - Pcap - 2^-60) / (1 - 2^-10.4), with Pcap the work-cap failure bound below.
- **One first block (H3).** By Bonferroni, Pr[X_f >= 1] >= E[X_f] - sum over pairs t < t' of f of Pr[A_t and A_t'] = E[X_f] - (1/2) sum_t Pr[A_t] E[X_f - 1 | A_t]. H3: E[X_f - 1 | A_t] <= delta = 2^-9.4 for every trial t, so
  Pr[X_f >= 1] >= (1 - 2^-10.4) E[X_f]. (Only the expected number of *further* successes of the same first block given one success is needed; bursty goodness and shared W7/W6 values enter only through that conditional expectation, and do not affect E[X], which is linear.)
- **Many first blocks (H1).** Distinct first blocks have independent chaining values, so the events X_f >= 1 are independent and Pr[X >= 1] >= 1 - exp(-sum_f Pr[X_f >= 1]) >= 1 - exp(-(1 - 2^-10.4) mu0). The table record of x is a deterministic function of x (Section 8.4).
- **Work cap.** The data-dependent work v_f of a first block (everything except its compression and its 264 fixed operations) has mean at most vbar = 100,298 (Section 11) and is at most vmax_fb = 1,438,843,116,766 (< 2^40.4; every one of the 12,103,680 variants examined and good, every l past row 16 to row 36).
  The v_f are independent (H1), so by Chebyshev Pr[sum v_f > (1 + s) N_FB vbar] <= E[v_f^2]/(s^2 N_FB vbar^2) <= vmax_fb/(s^2 N_FB vbar) = Pcap < 2^-11.31 with the slack s = 2^-10 (def128fc observed that the deviation s N_FB vbar enters squared). V_MAX = ceil((1 + s) N_FB vbar) = 3,843,035,011,703,560,881,170 is reached with probability below Pcap; the run then fails, which is accounted for here.
  No part of v_f depends on a conditional law of the scalars: the cost of a fibre batch is the same for every cb and every record (Section 9.4), and the table statistics enter vbar as expectations over uniform x (H9).
- **Success.** Pr[output a collision] >= 1 - exp(-(1 - 2^-10.4) mu0) - Pcap - 2^-60 = 0.3900000044 > 0.39 (the 2^-60 covers a repeated first block among N_FB draws of 512 bits). Any output is a verified collision, independent of the premises.

## 11. Ledger (exact; `python3 experiments/xtab.py ledger`)

```text
T = A_C + A_S + DEV + N_FB + (N_FB x 264 + V_MAX + vmax_fb + PRE + FIN) / C + 6
  A_C = 2^60   characteristic search and SFS-pair search of the paper (allowance, H4)
  A_S = 2^50   Step-1 SAT solve (paper: 2^41.3)
  DEV = 2^40   all development computation (Section 13.5)
  N_FB = 38,278,771,277,512,846 compressions (2^55.08739; H7 mu0 = 0.49530733, q3 = 2^-74.08, g = 8,074 examined good pairs per first block)
  264     fixed operations per first block (9.2: 30 + 16 control + 5 table read + 3 header loads + 2 + 95 + 38)
  V_MAX = 3,843,035,011,703,560,881,170 = ceil((1 + 2^-10) N_FB vbar), vbar = 100,298 operations, of which
               fibre batches (ceil(F/256) <= F/256 + 1 batches, each charged as a full batch of 230 + 1 + 8 + 31): 1,936
               passing fibres (p6 F x 12): 989
               segments (p6 times the sum over kept fibres of 9 + 3 floor(g/8) + 46 g; every lane probed): 96,216
               rows >= 16 (every probed lane may hit): 1,157
               with F = 1,219.8 x 1.01 kept fibres and Q = 30,488.5 x 1.01 four-groups per first block (Section 13.3)
  vmax_fb = 1,438,843,116,766 (one first block's maximal work: overshoot past the cap test)
  PRE = 2^58 operations (bound on all precomputation, Section 8.2); FIN = 1600 operations and 6 compressions
T x 2644 = 7,005,942,155,036,502,225,456     ->   T = 2^61.200563   ->  time_log2 = 61.20057
preprocessing = A_C + A_S + DEV + PRE/C = 2^60.00155
```

Every count in this block is produced by `ledger()` of `experiments/xtab.py` from the executable routines and the constant HIST_Z (Section 13.3); the integer-tightness of the 5th decimal is asserted in both directions (T^100000 against 2^(p) and 2^(p-1)).
Per first block the program spends 39.03 units against 13.08 in 7319bba and 7.23 in d3ec5c41; per examined good pair the data-dependent work is 12.55 operations, of which 11.5 are the group and its four lookups.

### 11.1 Precomputation

Section 8.2: PRE < 2^58 operations, charged in full (2^46.6 units). Padding lanes: the groups of a fibre of n members are ceil(n/4); the (4 ceil(n/4) - n) padding lanes are probed too and charged (Section 9.6) and the statistics Q count them.
The rare path is charged for every probed lane, padding included.

### 11.2 Sensitivity (log2 T, one input changed)

| change | log2 T |
|---|---|
| as claimed (q3 = 2^-74.08, study B's registered bound less the hedge) | 61.20057 |
| q3 = 2^-74.03 (study B's registered bound, no hedge) | 61.17260 |
| q3 = 2^-74.0225 (study B's bound at face value) | 61.16844 |
| q3 = 2^-74.07 (study A's bound) | 61.19494 |
| q3 = 2^-74.25 | 61.29885 |
| q3 = 2^-74.5 | 61.45212 |
| q3 = 2^-75 (the paper's count of 75 conditions) | 61.78830 |
| A_C = 2^64 | 64.11256 |
| A_C = 2^56 | 60.44445 |
| table statistics at face value (x 1.00 instead of x 1.01) | 61.18471 |
| table statistics x 1.05 | 61.26380 |
| table statistics x 1.10 | 61.34229 |
| THETA = 16 (more fibres examined) | 61.21870 |
| THETA = 100 | 61.20833 |
| each of the four row-16 lookups needs a comparison before its branch (+4 per group) | 61.26407 |
| cap slack 2^-9 | 61.20054 |
| cap slack 2^-12 | 61.21556 |

The table is a sensitivity of the *claimed bound*, in the sense of what the bound would have to be if the stated input were different. For the algorithm as submitted the caps N_FB and V_MAX are fixed, so time is bounded by the claim by construction; a table statistic or an op count that is too small does not lengthen the run but lowers the success probability, which has only the slack of the 1.01 margin on the table statistics (1.0% of vbar and of g) and of the 2^-10 cap factor: a true mean above vbar by more than about 2% would make the cap bind and reduce the success probability below 0.39 unless N_FB and V_MAX are rescaled as the table says. Operations the program executes but does not count are not covered by the cap; the counts of Section 9 are those of the straight-line text described there.

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
A first block costs a fixed 1 + 264/C units whatever it examines, so the cost per good pair including the fixed part, (2644 + 264 + vbar) / g = 12.78 operations at the optimum, is minimised by examining exactly the fibres whose marginal cost r(n) is below it: r(n) < 12.78 from n = 106 on (with oscillation caused by ceil(n/4) below that). Because the fixed cost (2644 + 264) is shared by all examined pairs, including a fibre with r(n) slightly above the optimum lowers the number of first blocks more than it raises the work per pair, which is why the ledger's minimum over THETA lies below the threshold of the marginal rule.
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
Limitations: rows >= 17 of distinct good pairs cannot be measured jointly within one first block; the premise leaves a margin of 2^35 over the measured row-16 factor; with the size-biased mean alone (without the allowance of 2^3) the examined-pair term would be 2^-13.0.

**H4 - advice allowances (supporting).** The published characteristic and two-bit conditions, the SFS pair's inner values S and L* are advice. Their construction is charged A_S = 2^50 (Step 1 and the completion to an SFS pair) and A_C = 2^60 (the characteristic search). Evidence: Section 11.3.
The variant family, the classes, the filter sets, L*, R16, the table and the program text are recomputed in the preprocessing (Section 8.2). Limitations: the 37-step search time is unpublished; A_C is a bound by comparison, not a measurement.

**H5 - counted word-RAM pricing (score-critical; cost reading).** A word-RAM program of 256-bit primitives in which every executed load, store, logic operation, shift, addition, comparison, branch and unconditional jump costs one primitive is charged by the primitives it executes; tables are ordinary
memory (a read is an address computation plus one load; memory is a reported metric only under collision-frontier-v5); the preprocessing is charged in full; registers: 64, with the live-value bound of Section 9.4; every address that is not a register value is formed by a counted add (Section 9.1), the base of the row-16 mask table folded into the per-first-block constant C; the program text is straight-line code of a few thousand instructions and is not advice. Evidence: the
program is in `experiments/xtab.py` (`w6_batch`, `good_group`, `process_cv`) and is exact against the scalar definitions (Section 13.2); its totals agree with the ledger (Section 13.4, in Tungsten over the whole family). Limitation: no organizer ruling is cited; the premise that the table of 2^53.0 bytes is admissible follows the earlier accepted claims with
memory far above physical capacity (e.g. 2^137 bytes) and the cost model's statement that memory contributes nothing to the scalar. A reader who prices memory accesses higher should read Section 11.2 (the per-first-block time is dominated by the packed stage, not by table reads: about 8,497 table loads per first block, of which 8,159 are the row-16 lookups).

**H7 - exact success floor (supporting).** The cap target is mu0 = 0.49530733, the smallest 8-decimal number strictly above -ln(0.61 - Pcap - 2^-60) / (1 - 2^-10.4) with Pcap = 2^-11.31 the Chebyshev bound for the work cap. With E[X] >= mu0 the success bound of Section 10, 1 - exp(-(1 - 2^-10.4) mu0) - Pcap - 2^-60, is >= 0.39000000
with no further padding. `ledger()` computes mu0 with 60-digit decimals, asserts the success bound > 0.39 and the exact-rational ceiling N_FB g 32 q3 >= mu0. (087a18c4's H7.)

**H9 - table statistics and preprocessing bound (score-critical, new).** (a) Over uniform x, let F, V, Q be the means of the number of kept fibres, of the kept variants and of sum over kept fibres of ceil(size/4). The ledger charges the sample means of Section 13.3 (800,000 values of x, Tungsten, eight shards; the eight shard means differ from the pooled mean by at most 1.32%, the standard error of the pooled mean is 0.26%)
times 1.01 upwards for F and Q (costs) and downwards for V (the yield g), and assumes the exact means lie within that margin. (b) The preprocessing of Section 8.2 costs at most 2^58 operations and the table at most 2^53.0 bytes. Evidence for (a): sampling and the end-to-end simulation of Section 13.4 on 480,000 further values of x; the sensitivity of Section 11.2 (a 5% error in all table statistics would cost 0.079 bit).
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

For each of 800,000 values of x drawn uniformly (eight shards of 100,000 values, a 64-bit LCG with different seeds): the 22,976 W7 tests of Section 5.1 (bitwise form), phi(a0, x) for every variant of every passing class (about 190,000 per x), a heap sort and a run scan (Appendix A.4). The output is the histogram of fibre sizes, summed over x; HIST_Z in `xtab.py` holds it for sizes of at least 16 (zlib + base85; the text is in Appendix A.11).
Means per first block: **1,219.8 kept fibres, 121,899 kept variants, 30,488.5 four-groups** for THETA = 40. Passing classes per x: 364.8 on average (22,976 p7 = 364.6 exact), variants in passing classes 192,233 (exact mean 12,103,680 p7 = 192,075).
The eight shard means of the kept variants are 121974, 121996, 122968, 122466, 121458, 122788, 120293, 121249 (relative standard error of the pooled mean: 0.26%). A first, smaller run of 4,000 values of x per shard (32,000 in all) had given kept variants 121,980 and kept fibres 1,214.2, consistent with the pooled values. The ledger uses the pooled means times 1.01.

Table 13.3 (pooled over all 800000 values of x; HIST_Z in `xtab.py` holds the counts; the text is in Appendix A.11):

| size n of the fibre | fibres per first block | variants per first block | share of variants in passing classes |
|---|---|---|---|
| 16..19 | 1078.67 | 17300.9 | 9.00% |
| 20..29 | 400.87 | 9765.2 | 5.08% |
| 30..39 | 800.67 | 25699.2 | 13.37% |
| 40..47 | 58.16 | 2378.4 | 1.24% |
| 48..59 | 252.48 | 12706.9 | 6.61% |
| 60..79 | 427.64 | 27474.9 | 14.29% |
| 80..99 | 123.38 | 11290.1 | 5.87% |
| 100..199 | 260.04 | 35126.8 | 18.27% |
| 200..399 | 78.31 | 20829.8 | 10.84% |
| 400..max | 19.82 | 12092.0 | 6.29% |
| 1..15 (not stored in HIST_Z; never kept) | - | - | - |

| THETA | kept fibres | kept variants | examined good pairs g | log2 T |
|---|---|---|---|---|
| 16 | 3500 | 174664 | 11568 | 61.21870 |
| 20 | 2421 | 157363 | 10423 | 61.20895 |
| 24 | 2366 | 156247 | 10349 | 61.20840 |
| 32 | 2002 | 147052 | 9740 | 61.20571 |
| 40 | 1220 | 121899 | 8074 | 61.20057 |
| 48 | 1162 | 119520 | 7916 | 61.20021 |
| 56 | 975 | 110511 | 7319 | 61.20010 |
| 64 | 887 | 105478 | 6986 | 61.20043 |
| 80 | 482 | 79339 | 5255 | 61.20396 |
| 100 | 358 | 68049 | 4507 | 61.20833 |


### 13.4 The counted program simulated end to end in Tungsten (this filing)

For 480,000 further values of x (eight shards, different seeds) and an independent uniform cb for each: the record of x is built as in Section 8.2 (union fibres, THETA in {20, 30, 40, 60}), the F6 test is applied to every kept fibre value + cb, and the operations of the counted program are summed by its own formulas (batches 230 + 71 + chunk operations (+1 for a partial batch), 12 per passing fibre, 46 per group plus 9 + 3 floor(g/8) per segment, 264 fixed; the rare path is not simulated):

| THETA | x values | kept fibres | kept variants | examined good pairs (simulated) | mean data-dependent ops (simulated) | sd / mean | ledger vbar (same THETA) |
|---|---|---|---|---|---|---|---|
| 20 | 480,000 | 2414.6 | 157213 | 10516 | 128430 | 3.33 | 131702 |
| 30 | 480,000 | 2014.7 | 147479 | 9862 | 119785 | 3.43 | 122893 |
| 40 | 480,000 | 1215.9 | 121838 | 8143 | 97652 | 3.78 | 100298 |
| 60 | 480,000 | 906.2 | 106810 | 7137 | 85163 | 4.01 | 87498 |

The measured mean agrees with the ledger's expectation for THETA = 40 (which carries the safety factor, the bound ceil(F/256) <= F/256 + 1 and the rare path): the simulated mean data-dependent work is 97652 operations, the ledger charges 100298 (99141 without the rare path), i.e. the ledger exceeds the simulation by 1.53% without the rare path. The counts are bursty (standard deviation across first blocks 3.8 times the mean), so the standard error is dominated by rare large records.
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
| records R(x): members 2 x 8 x 4 ceil(n/4) per kept fibre (A and S arrays), entries 32 per fibre, planes 1024 per batch, cost words: mean 2,016,226 bytes per x over uniform x (Section 13.3, times 1.01), 2^32 records | 2^52.9 |
| Rmask3: 3 x 2^32 words of 32 bytes; the 24-bit lane-scan tables (11 x 2^24 entries); code | 2^38.6 |
| total | **2^53.0** |

Claimed memory: 2^53.0 bytes (the sum over all x of the record sizes, estimated from the sampled means; reported only under collision-frontier-v5; the earlier claims on this track report up to 2^137 bytes). The table is built entry by entry in the preprocessing and is never held twice.
Nonuniform advice: the characteristic, S, L*, and the 222 class descriptors used by the experiments (below 2^13 bytes), charged through A_C and A_S; everything else, including the class list of the whole family, the table and Rmask, is recomputed in the preprocessing.

## 15. Limitations

- H1, H2, H3 are premises. q3 is estimated (Monte Carlo, by another solver, not re-run here and not for this filing's subset of G), not proved; no collision has been found and none is expected at the scale we can run. The full-scale success probability cannot be observed.
- The table statistics (H9) are Tungsten sample means over 800,000 values of x, scaled by 1.01, not an enumeration of all 2^32 values of x (about 2^58 operations of Tungsten work). The per-x counts are heavy-tailed. Section 11.2 prices a 5% and a 10% error.
- The organizer experiments run the same program on the 222 embedded classes only (the sandbox cannot hold the family); the whole-family table and statistics are Tungsten computations of this filing, not organizer experiments.
- The memory of 2^53.0 bytes is far beyond any machine; memory is reported only under collision-frontier-v5 and earlier claims on this track report up to 2^137 bytes. A reader who charges table reads or memory differently should note that table reads are about 8,497 of the 100,298 data-dependent operations per first block.
- Study B of the q3 estimate was registered after study A had been read (7319bba, Section 7.4); study A's bound would price the claim at 61.19494. The hedge of 0.05 bit for the changed subset of variants is a judgment, not a measurement.
- The published characteristic and SFS pair are used as advice under allowances; the paper's SAT solve and characteristic search were not rerun.
- For 37 steps the measured q3 is about one bit better than the 75 conditions stated in the paper's text; the paper's own tables give 74, which the SMC matches stage by stage (6c77089c reached the same conclusion). With q3 = 2^-75, log2 T would be 61.78830.
- H3 (b) is measured at the row-16 level only (7319bba) and its bound on the number of examined good pairs is a premise.
- The program text, the table and the lane-scan tables are assumed addressable and free of charge to store (H5); the cost reviewer may price memory differently (Section 11.2).
- The counts of the earlier filings that this one corrects (Section 16) were accepted for review as they were; correcting them cost this filing 0.006 bit.

## 16. What this filing changes relative to d3ec5c41 (61.71473) and its derivatives (61.68435, 61.57882, 61.51197)

| change | effect |
|---|---|
| all 22,976 classes, fibres merged across classes by equal phi, only fibres of at least THETA variants examined (Sections 5.3, 8.1, 11.4) | 121,899 variants examined per first block, g = 8,074 examined good pairs instead of 831; N_FB 2^55.08739 instead of 2^58.32 |
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
NX 800000
16 845970049
17 406078
18 16248781
19 307358
20 37036833
21 2695620
22 4080736
23 270148
24 202830035
25 370166
26 6932420
27 572018
28 65421208
29 487408
30 14149005
31 410218
32 603116031
33 261408
34 1048031
35 478250
36 19898036
37 58892
38 735492
39 384206
40 33285301
41 47456
42 6671292
43 69366
44 5068038
45 642408
46 688553
47 55438
48 137826898
49 201954
50 861600
51 54684
52 8907265
53 55170
54 1223433
55 70538
56 51605769
57 97652
58 1042584
59 34648
60 16517854
61 58134
62 993919
63 193628
64 304988044
65 66854
66 575491
67 12392
68 1221575
69 38866
70 1045086
71 18822
72 14435066
73 10616
74 122121
75 116740
76 776988
77 54232
78 846795
79 21584
80 19870528
81 29210
82 117749
83 5002
84 6794522
85 13796
86 141147
87 43510
88 3624908
89 8218
90 1378910
91 43284
92 766559
93 48846
94 103221
95 12962
96 65294658
97 5956
98 385409
99 17958
100 790803
101 3176
102 124055
103 3344
104 6442160
105 100516
106 115709
107 9380
108 1121228
109 4054
110 124933
111 5086
112 25830935
113 10796
114 177635
115 8724
116 1090611
117 22404
118 58525
119 13196
120 10968143
121 12024
122 114167
123 6906
124 990588
125 7938
126 354169
127 3094
128 110216153
129 6618
130 131303
131 2918
132 518161
133 10478
134 25500
135 35914
136 814281
137 3304
138 71062
139 1598
140 939347
141 6366
142 33099
143 5128
144 6848818
145 6696
146 20479
147 12064
148 107692
149 4460
150 220269
151 3764
152 470689
153 2740
154 92143
155 8228
156 753055
157 3026
158 35696
159 4978
160 8227156
161 3466
162 50872
163 624
164 100292
165 11470
166 8094
167 740
168 3732067
169 2338
170 27271
171 5324
172 116937
173 1510
174 88934
175 4942
176 1624071
177 3646
178 12540
179 600
180 1180321
181 1202
182 70335
183 5378
184 460744
185 2334
186 80218
187 1520
188 82087
189 6146
190 17223
191 850
192 21828621
193 644
194 11691
195 8646
196 284796
197 592
198 31866
199 368
200 412544
201 966
202 4473
203 3222
204 103974
205 914
206 6251
207 2156
208 2910826
209 682
210 156042
211 992
212 100295
213 1346
214 13733
215 1094
216 557492
217 3914
218 6183
219 1300
220 87158
221 1410
222 9278
223 546
224 8611369
225 9516
226 14885
227 994
228 139437
229 456
230 14942
231 2624
232 674393
233 2006
234 39100
235 1848
236 42803
237 1778
238 19720
239 554
240 4530874
241 1196
242 15499
243 984
244 99612
245 1958
246 11697
247 926
248 568157
249 830
250 13274
251 368
252 257109
253 530
254 5787
255 1998
256 28375429
257 312
258 10622
259 354
260 106629
261 1610
262 3661
263 368
264 253228
265 832
266 12929
267 588
268 20460
269 254
270 56617
271 372
272 338200
273 1998
274 4240
275 386
276 52453
277 244
278 2414
279 1710
280 436878
281 382
282 8413
283 326
284 21754
285 2176
286 7473
287 698
288 2134548
289 296
290 14054
291 750
292 16583
293 626
294 19295
295 474
296 53202
297 572
298 5540
299 266
300 159334
301 644
302 5622
303 186
304 171541
305 1114
306 4878
307 132
308 55568
309 552
310 12792
311 186
312 368790
313 108
314 3848
315 3626
316 28347
317 144
318 7311
319 310
320 2324647
321 436
322 5047
323 110
324 30989
325 334
326 925
327 272
328 50244
329 304
330 13989
331 38
332 5453
333 322
334 1487
335 128
336 1264886
337 78
338 3157
339 356
340 19812
341 488
342 7618
343 284
344 52622
345 632
346 1932
347 162
348 68377
349 114
350 7654
351 542
352 461132
353 176
354 3853
355 192
356 7721
357 558
358 667
359 218
360 531799
361 360
362 1955
363 420
364 45176
365 126
366 7037
367 174
368 157248
369 322
370 3325
371 546
372 56360
373 100
374 2306
375 656
376 33421
377 242
378 9416
379 70
380 9994
381 246
382 1598
383 18
384 5019895
385 158
386 1153
387 146
388 11248
389 76
390 10425
391 94
392 112012
393 278
394 748
395 192
396 20482
397 32
398 657
399 718
400 128586
401 50
402 1485
403 286
404 2980
405 582
406 4179
407 116
408 46634
409 84
410 1579
411 162
412 4449
413 78
414 2445
415 72
416 860362
417 92
418 1025
419 34
420 101943
421 72
422 1273
423 226
424 46492
425 140
426 1978
427 156
428 7433
429 176
430 1480
431 60
432 174884
433 44
434 5377
435 618
436 3702
437 144
438 1874
439 52
440 31194
441 140
442 1463
443 84
444 5415
445 88
446 659
447 254
448 1905862
449 50
450 11847
451 86
452 9079
453 400
454 1041
455 240
456 56146
457 44
458 411
459 74
460 9244
461 28
462 4189
463 98
464 251355
465 634
466 2995
467 122
468 25181
469 134
470 1714
471 164
472 15269
473 74
474 2189
475 70
476 11098
477 184
478 622
479 50
480 1209746
481 94
482 1422
483 110
484 9570
485 64
486 1383
487 18
488 45150
489 68
490 2365
491 70
492 6225
493 48
494 1547
495 272
496 199178
497 74
498 1081
499 36
500 7570
501 46
502 430
503 32
504 91942
505 62
506 804
507 70
508 3047
509 50
510 2339
511 54
512 5105171
513 160
514 300
515 62
516 5766
517 26
518 599
519 100
520 44156
521 34
522 2691
523 20
524 2253
525 434
526 260
527 94
528 78107
529 10
530 1154
531 54
532 6632
533 106
534 644
535 58
536 7105
537 14
538 352
539 60
540 33632
541 26
542 792
543 114
544 86740
545 20
546 2295
547 6
548 2131
549 56
550 503
551 70
552 19642
553 62
554 278
555 72
556 1665
557 74
558 2410
559 36
560 115870
561 36
562 474
563 8
564 4422
565 40
566 359
567 32
568 7467
569 12
570 2203
571 10
572 4240
573 8
574 741
576 446634
577 26
578 396
579 8
580 9884
581 6
582 1184
583 28
584 6307
585 198
586 702
587 2
588 10178
589 148
590 647
591 24
592 13969
593 56
594 762
595 102
596 2390
597 6
598 280
599 14
600 56018
601 16
602 637
603 28
604 3126
605 118
606 185
607 16
608 39615
609 150
610 1387
611 52
612 2837
613 36
614 110
615 116
616 16781
617 28
618 852
619 14
620 7384
621 4
622 355
623 20
624 105197
625 28
626 228
627 58
628 1724
629 16
630 4518
631 10
632 10483
633 68
634 186
635 28
636 3631
637 12
638 352
639 18
640 439106
641 8
642 479
643 4
644 2787
645 84
646 119
647 4
648 8713
649 34
650 493
651 116
652 451
653 32
654 250
655 6
656 13555
657 50
658 291
659 16
660 7264
661 2
662 66
663 14
664 1923
665 10
666 390
667 8
668 773
669 8
670 180
671 16
672 266028
673 16
674 124
675 200
676 1607
677 6
678 585
679 52
680 7142
681 10
682 706
683 20
684 3864
685 24
686 382
687 18
688 14042
689 18
690 689
691 2
692 991
693 38
694 122
695 38
696 27397
697 8
698 116
699 136
700 4214
701 8
702 941
703 22
704 85139
705 100
706 123
707 12
708 2168
709 26
710 204
711 28
712 2209
713 30
714 851
715 12
716 259
717 32
718 265
719 4
720 136927
721 2
722 501
723 36
724 820
725 18
726 551
727 4
728 14585
729 8
730 206
731 8
732 4107
734 242
735 160
736 35499
737 16
738 327
740 1315
741 12
742 421
743 2
744 18345
745 36
746 144
747 6
748 880
750 808
752 7165
754 210
756 4897
757 8
758 90
759 28
760 2773
761 4
762 214
764 533
765 44
766 52
768 774775
769 6
770 227
771 6
772 654
773 8
774 237
775 20
776 4454
778 87
779 16
780 5012
781 2
782 136
783 10
784 22821
785 4
786 218
788 303
789 8
790 291
791 18
792 6274
793 2
794 43
795 30
796 269
797 12
798 562
799 2
800 23595
801 10
802 37
804 622
805 4
806 258
807 2
808 958
809 2
810 977
812 2244
813 32
814 137
815 2
816 11544
817 2
818 70
819 10
820 815
821 6
822 153
824 1471
825 8
826 241
828 1469
830 81
831 4
832 160150
834 116
836 391
837 22
838 38
840 33474
842 31
843 26
844 464
845 22
846 277
847 22
848 11013
850 201
851 2
852 880
854 375
855 40
856 2073
858 278
859 24
860 724
861 20
862 56
863 8
864 32924
866 36
868 2440
869 6
870 569
872 905
873 28
874 56
875 18
876 1028
878 57
879 10
880 6595
881 4
882 215
883 12
884 686
885 2
886 156
888 1389
889 8
890 60
891 2
892 261
894 325
896 276929
897 2
898 13
899 2
900 5486
901 4
902 145
903 12
904 2878
905 32
906 233
907 2
908 345
909 4
910 204
911 6
912 12630
913 10
914 23
915 42
916 160
918 96
919 4
920 2870
921 4
922 19
924 1678
925 36
926 83
927 16
928 60384
930 543
932 2250
933 12
934 185
935 2
936 8717
937 4
938 55
939 2
940 846
941 6
942 135
943 10
944 3395
945 34
946 111
947 4
948 1060
949 4
950 34
952 2614
954 181
955 30
956 200
957 10
958 49
960 209291
961 10
962 44
964 535
966 142
967 4
968 2831
969 12
970 149
971 10
972 593
974 30
975 8
976 13173
977 2
978 146
980 768
981 8
982 70
983 4
984 1430
986 75
987 6
988 717
989 2
990 298
992 39552
994 67
996 405
997 16
998 42
999 4
1000 1783
1002 61
1003 6
1004 105
1005 2
1006 147
1008 16600
1010 23
1012 412
1013 10
1014 45
1015 2
1016 751
1018 28
1020 923
1021 2
1022 48
1023 18
1024 630885
1026 122
1027 2
1028 255
1030 16
1032 1483
1034 13
1035 2
1036 197
1038 56
1040 10155
1041 2
1042 17
1044 1633
1045 2
1046 31
1048 535
1050 511
1052 84
1053 4
1054 98
1056 13822
1058 38
1059 6
1060 534
1062 75
1064 1422
1065 2
1066 74
1068 203
1070 27
1071 4
1072 1252
1074 13
1075 14
1076 218
1077 14
1078 83
1079 2
1080 9162
1082 48
1083 16
1084 237
1085 22
1086 53
1088 14578
1090 32
1091 2
1092 959
1094 9
1095 6
1096 521
1098 135
1100 175
1102 56
1104 3789
1105 2
1106 132
1107 4
1108 178
1110 70
1112 380
1114 42
1116 1061
1118 35
1119 4
1120 16820
1121 4
1122 38
1124 131
1126 4
1128 1019
1129 16
1130 59
1131 6
1132 90
1134 44
1136 1301
1137 12
1138 32
1140 937
1142 17
1144 941
1146 17
1148 234
1149 2
1150 37
1152 56786
1154 28
1155 12
1156 113
1158 31
1159 4
1160 3338
1161 6
1162 18
1164 548
1165 24
1166 23
1168 1212
1170 201
1172 313
1174 11
1176 2027
1178 115
1180 256
1181 4
1182 24
1184 2163
1185 14
1186 26
1188 458
1189 10
1190 83
1192 572
1194 5
1196 128
1198 28
1199 4
1200 10548
1202 12
1204 199
1206 23
1208 707
1209 2
1210 72
1211 2
1212 111
1214 15
1215 2
1216 4980
1218 159
1220 619
1222 87
1224 641
1226 16
1228 33
1230 95
1231 2
1232 2806
1234 14
1236 257
1237 4
1238 3
1240 1985
1241 2
1242 50
1244 49
1245 10
1246 21
1247 2
1248 18452
1250 28
1252 61
1254 69
1256 363
1257 6
1258 55
1260 2000
1261 2
1262 18
1263 2
1264 2447
1266 34
1268 45
1270 13
1272 869
1274 21
1275 8
1276 240
1278 14
1280 53686
1281 4
1282 4
1283 4
1284 143
1286 8
1287 2
1288 655
1290 53
1292 40
1294 5
1296 1273
1298 20
1299 2
1300 129
1302 83
1304 84
1305 8
1306 15
1307 2
1308 131
1309 2
1310 11
1312 2046
1314 54
1315 8
1316 142
1318 9
1320 1553
1322 4
1324 31
1325 2
1326 26
1327 4
1328 271
1329 4
1330 31
1332 97
1334 4
1336 234
1338 27
1340 89
1341 4
1342 54
1343 6
1344 32474
1346 4
1348 32
1350 197
1352 357
1354 1
1356 188
1358 67
1359 2
1360 1289
1362 25
1364 274
1365 10
1366 14
1368 755
1370 9
1371 2
1372 142
1374 18
1376 1748
1378 10
1380 202
1382 13
1384 148
1386 52
1388 14
1390 11
1392 6652
1394 7
1395 16
1396 28
1398 84
1400 875
1403 8
1404 450
1406 6
1408 10059
1410 40
1412 34
1414 21
1416 434
1418 14
1420 64
1421 2
1422 28
1424 343
1425 2
1426 19
1428 261
1430 5
1432 51
1434 28
1436 66
1438 8
1440 23158
1441 6
1442 23
1444 119
1446 32
1448 139
1450 16
1451 4
1452 169
1454 2
1455 10
1456 2408
1458 12
1460 85
1462 4
1463 20
1464 1183
1466 7
1467 2
1468 145
1469 2
1470 118
1472 4385
1474 13
1476 100
1478 1
1480 258
1482 28
1484 189
1485 6
1488 2650
1490 19
1492 34
1494 9
1496 99
1498 8
1500 260
1501 16
1502 1
1504 1101
1506 6
1508 71
1510 31
1512 919
1514 9
1515 2
1516 29
1518 22
1519 4
1520 440
1522 2
1524 75
1528 54
1530 35
1532 35
1534 1
1536 75560
1540 38
1542 11
1544 162
1546 2
1548 34
1550 12
1552 1107
1554 17
1556 32
1558 2
1560 1233
1562 3
1564 23
1566 63
1568 2657
1570 6
1572 58
1574 5
1576 74
1578 1
1580 139
1582 30
1584 940
1586 1
1588 7
1590 12
1592 55
1593 2
1594 1
1596 244
1598 10
1600 2455
1602 19
1604 20
1606 8
1608 107
1610 12
1612 64
1614 10
1616 145
1618 1
1620 401
1622 2
1624 501
1626 8
1628 54
1630 5
1632 1678
1634 8
1636 6
1637 2
1638 25
1640 145
1642 2
1644 50
1646 1
1648 213
1649 6
1650 33
1652 89
1654 5
1656 312
1660 24
1662 10
1664 19851
1666 3
1668 38
1670 2
1672 66
1674 61
1676 30
1677 2
1678 1
1680 6231
1684 11
1686 16
1688 72
1690 8
1692 78
1694 2
1696 1524
1698 26
1700 63
1702 5
1703 8
1704 147
1706 1
1708 115
1710 53
1712 195
1716 42
1720 126
1722 10
1724 22
1726 20
1728 3341
1730 3
1731 2
1732 12
1736 458
1738 2
1740 259
1742 4
1744 119
1746 66
1748 35
1750 26
1752 189
1755 2
1756 15
1758 33
1760 709
1764 112
1766 4
1767 6
1768 78
1770 7
1772 48
1774 3
1776 221
1778 2
1780 16
1782 8
1784 34
1788 90
1792 23991
1794 1
1796 2
1797 2
1798 1
1799 2
1800 1279
1802 1
1804 28
1806 3
1808 392
1810 4
1812 45
1814 1
1816 54
1818 18
1820 35
1822 2
1824 1181
1826 3
1828 7
1830 20
1832 19
1834 4
1836 25
1838 3
1840 479
1842 4
1844 13
1848 208
1852 33
1854 11
1855 20
1856 9875
1858 1
1859 2
1860 226
1862 6
1864 449
1866 3
1868 39
1869 2
1870 1
1872 1359
1874 1
1875 20
1876 25
1880 132
1881 2
1884 53
1886 4
1888 423
1890 35
1892 19
1894 5
1896 243
1898 5
1900 10
1902 3
1904 290
1906 4
1908 81
1910 17
1912 30
1914 16
1916 10
1918 4
1920 22934
1922 1
1924 23
1926 6
1928 71
1930 1
1932 39
1935 2
1936 421
1938 2
1940 83
1944 67
1946 1
1948 3
1950 8
1952 2367
1954 5
1956 55
1958 1
1960 117
1964 10
1966 3
1968 116
1970 9
1972 42
1974 1
1976 110
1980 51
1982 13
1984 4846
1988 4
1990 1
1992 77
1998 3
2000 216
2002 7
2004 29
2006 4
2008 7
2012 27
2014 1
2016 1649
2018 8
2020 12
2024 77
2026 4
2028 17
2030 9
2032 104
2034 4
2036 6
2040 202
2041 4
2042 1
2044 20
2046 8
2048 52461
2052 54
2056 32
2058 1
2060 8
2064 154
2066 3
2068 1
2072 18
2074 1
2076 5
2080 1143
2082 1
2084 1
2086 2
2088 313
2090 4
2092 15
2094 11
2096 86
2100 193
2104 4
2106 7
2108 14
2112 1281
2114 1
2116 6
2118 4
2120 106
2124 26
2126 1
2128 158
2130 11
2132 14
2134 4
2136 24
2140 24
2142 5
2144 122
2146 3
2148 4
2150 1
2151 2
2152 25
2154 9
2156 21
2160 1191
2164 13
2166 4
2168 58
2172 10
2174 2
2176 1716
2178 1
2180 3
2184 154
2186 6
2187 2
2188 1
2190 2
2192 60
2194 2
2196 53
2198 3
2200 11
2202 28
2204 28
2208 512
2212 37
2214 3
2216 46
2220 15
2224 86
2226 1
2228 18
2232 217
2234 2
2236 14
2238 1
2240 1551
2244 10
2248 19
2250 5
2252 6
2256 142
2258 3
2260 5
2262 2
2264 2
2268 44
2272 115
2276 8
2278 1
2280 163
2282 8
2284 12
2286 1
2288 64
2292 8
2296 26
2304 4152
2308 3
2310 6
2312 17
2316 11
2320 579
2324 5
2326 1
2328 151
2330 31
2332 1
2336 165
2338 1
2340 64
2344 98
2352 188
2353 6
2356 16
2358 1
2360 18
2362 10
2364 11
2368 188
2370 14
2372 7
2376 50
2378 2
2379 4
2380 13
2384 90
2388 6
2392 9
2394 4
2396 3
2400 1141
2404 5
2406 1
2408 29
2412 3
2416 86
2418 6
2420 15
2424 33
2430 1
2432 332
2436 71
2440 121
2444 43
2448 62
2451 2
2452 1
2456 2
2460 8
2464 257
2466 1
2468 31
2472 23
2478 1
2480 201
2482 1
2484 5
2488 7
2490 1
2492 25
2496 1484
2498 1
2500 2
2502 3
2504 8
2508 3
2512 39
2514 3
2516 7
2520 438
2524 10
2526 1
2528 375
2536 10
2540 4
2544 65
2548 3
2552 27
2554 1
2560 3985
2562 5
2564 1
2568 14
2570 1
2572 5
2576 126
2580 8
2584 2
2592 96
2596 7
2598 4
2600 14
2604 15
2608 14
2612 1
2616 6
2618 2
2620 6
2624 169
2626 3
2628 6
2632 16
2634 2
2635 4
2636 2
2640 117
2642 2
2648 6
2652 6
2656 33
2658 1
2660 23
2664 7
2672 17
2676 3
2678 6
2680 2
2682 4
2684 14
2688 2120
2692 1
2696 9
2700 43
2704 42
2708 1
2712 35
2716 8
2720 129
2728 23
2730 1
2736 30
2740 2
2744 18
2752 138
2754 1
2760 53
2768 13
2770 1
2780 4
2784 821
2790 16
2792 2
2796 29
2800 107
2808 50
2812 1
2816 666
2820 3
2824 5
2828 1
2832 65
2836 4
2838 8
2840 11
2842 4
2844 14
2848 31
2850 3
2852 4
2856 24
2862 2
2864 3
2868 4
2872 3
2876 8
2880 2057
2882 8
2884 19
2888 17
2892 1
2894 8
2896 33
2900 3
2904 16
2910 4
2912 96
2916 1
2920 32
2928 128
2932 8
2936 23
2940 51
2944 565
2948 8
2952 7
2960 70
2964 5
2968 49
2970 9
2976 301
2980 5
2988 1
2992 6
2996 8
3000 72
3004 1
3008 82
3012 2
3014 2
3016 2
3018 4
3020 8
3024 77
3032 7
3034 5
3036 7
3038 1
3040 29
3048 11
3056 22
3060 5
3064 1
3068 3
3072 4316
3073 8
3080 3
3082 1
3084 1
3085 8
3088 14
3096 2
3100 5
3104 184
3112 3
3114 2
3120 79
3124 2
3128 1
3132 66
3136 158
3144 14
3150 16
3152 11
3160 19
3168 65
3170 4
3176 4
3180 4
3184 7
3188 2
3190 1
3192 29
3200 157
3212 5
3214 1
3216 15
3220 1
3224 10
3228 1
3232 20
3236 2
3240 55
3248 76
3252 7
3260 1
3262 4
3264 104
3270 1
3272 2
3276 6
3280 4
3292 3
3296 16
3298 1
3304 8
3306 1
3312 13
3328 1313
3336 4
3344 8
3348 4
3352 27
3360 670
3376 7
3384 2
3388 5
3392 197
3400 16
3404 1
3408 2
3412 3
3416 19
3420 3
3424 15
3432 3
3440 9
3448 1
3452 7
3454 1
3456 231
3472 25
3476 2
3480 24
3488 5
3492 7
3500 10
3504 20
3512 20
3516 3
3520 44
3528 4
3532 1
3540 2
3544 10
3552 4
3560 1
3576 11
3582 1
3584 1420
3588 1
3592 2
3596 1
3600 101
3608 4
3610 6
3612 2
3616 62
3624 5
3632 3
3644 2
3648 65
3660 1
3662 1
3664 1
3672 2
3676 1
3680 15
3692 2
3696 5
3708 1
3712 1336
3720 25
3724 1
3728 183
3736 7
3740 1
3744 122
3752 3
3760 12
3766 2
3768 5
3776 18
3780 24
3782 4
3788 1
3792 10
3798 1
3800 1
3808 35
3816 1
3820 2
3824 22
3828 1
3836 17
3840 1464
3848 4
3856 8
3864 6
3872 31
3880 27
3888 3
3890 1
3904 213
3908 4
3912 3
3916 1
3920 2
3924 1
3936 3
3944 2
3946 2
3948 1
3952 6
3960 3
3964 2
3968 343
3984 1
3992 1
4000 9
4004 1
4020 3
4024 1
4032 65
4048 7
4052 1
4062 1
4064 6
4068 2
4080 15
4088 1
4096 2743
4102 1
4104 4
4110 1
4112 1
4120 1
4128 3
4132 2
4146 1
4160 61
4176 32
4192 5
4200 18
4216 1
4224 72
4228 1
4240 1
4248 1
4256 10
4268 4
4284 8
4288 6
4304 2
4312 4
4320 70
4326 16
4332 8
4336 13
4344 4
4352 84
4356 1
4358 3
4368 3
4384 6
4392 7
4396 3
4398 1
4400 4
4408 1
4416 44
4424 3
4440 2
4448 6
4456 2
4464 15
4472 2
4480 34
4488 1
4494 8
4504 1
4512 10
4516 5
4520 2
4544 2
4548 2
4552 2
4560 9
4576 3
4608 147
4640 111
4656 8
4660 2
4672 17
4680 1
4688 12
4696 2
4704 3
4712 6
4728 1
4736 12
4752 4
4776 1
4800 47
4824 2
4832 5
4840 1
4864 23
4872 2
4880 5
4888 5
4896 14
4928 14
4936 2
4944 8
4956 1
4960 5
4968 1
4976 2
4992 56
5008 6
5016 2
5040 24
5056 41
5100 2
5104 1
5120 153
5136 6
5152 2
5184 8
5248 3
5250 4
5280 8
5284 2
5316 2
5356 2
5376 68
5436 2
5440 7
5488 1
5504 5
5520 6
5568 124
5592 4
5600 26
5616 4
5632 37
5640 2
5648 2
5664 4
5680 2
5684 1
5760 88
5776 20
5822 2
5840 2
5856 27
5868 1
5872 1
5880 2
5888 24
5920 3
5948 1
5952 2
6000 2
6016 3
6024 2
6080 2
6144 123
6200 1
6208 6
6212 1
6248 2
6264 2
6272 5
6300 2
6480 2
6496 31
6524 1
6528 1
6608 1
6624 1
6656 36
6720 39
6800 1
6832 10
6848 1
6912 7
6960 12
7168 27
7232 4
7296 3
7424 113
7440 2
7456 21
7472 2
7560 6
7584 1
7680 53
7760 2
7808 28
7936 13
8000 3
8064 6
8192 64
8320 2
8352 9
8368 2
8384 1
8388 2
8400 7
8448 4
8480 1
8640 6
8784 2
8792 2
8832 3
9216 8
9280 9
9344 2
9360 3
9504 2
9728 1
10080 1
10112 2
10240 3
11264 2
11520 2
11552 2
11776 1
12288 4
13440 2
14848 3
14912 3
15360 2
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

