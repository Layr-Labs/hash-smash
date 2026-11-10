# Collision attack on 37-step SHA-256: the ePrint 2026/1120 two-block attack with A0-variants of the Step-1 solution, 2^63.45545

Track `sha256-r37-exploratory`, target `sha256-r37-prefix-v1`, cost model `collision-frontier-v5` (C = 2644).
Claim: `time_log2 = 63.45545` target compressions on every run, success probability at least 0.39 (0.3900000035 under the
stated premises), memory 2^34.1 bytes (reported only), nonuniform advice below 2^13 bytes.

The attack is the 37-step collision attack of Li, Zhang, Li, Liu, Qian and Zhu, "Pushing Collision Attacks on SHA-2
to 39 Steps" (IACR ePrint 2026/1120, CC BY), in the two-block memory-efficient framework of [LLWS26] (Li, Liu, Wang,
Shi, ePrint 2026/1080). We reuse the paper's characteristic and its published semi-free-start pair exactly as
transcribed and verified in the earlier filing 6c77089c (winglock), and the exact Step-2 filter sets F6, F7 of that
filing. **The new step is Section 4.3:** the second-block word A0 carries no condition of the characteristic, so the
Step-1 solution S has 12,103,680 *variants* that differ from S only in A0, E4, W8 (and in the first-block-dependent
words W0..W7). Every variant is as good as S for Step 3 (Section 7), and variants that share their W7 constant c7
can be tested together (Section 5.3). This removes most of the paper's Step-2 cost: instead of 2^9.88 first blocks
per usable chaining value, every first block yields on average 244.58 usable (chaining value, variant) pairs.

## 0. Summary

- **Algorithm (Sections 4-8).** Messages M0 || M1 and M0 || M1' (128 bytes; padding adds the same third block).
  A first block M0 is two fresh uniform 256-bit words; CV1 = F_37(IV, M0) costs one unit. For each of 64 fixed
  classes of variants (3600 variants each, 230,400 in total) one test W7x = c7 - A_{-1} in F7 decides whether
  all 3600 variants of the class pass the W7 filter. For each passing class a counted bit-sliced program tests the
  W6 filter for 256 variants per batch; each variant passing both filters (a *good pair*) gets u = W0 + s0(W1)
  and an exact row-16 table lookup over the 32 elements of L*; each row-16 pass is checked through row 36. A
  pair that follows every cell of rows 16..36 collides; it is verified with the target and output.
- **Rates (exact under H1).** Per first block: 64 p7 = 1.015625 passing classes and
  g = 64 x 3600 x p7 x p6 = 2003625/8192 = 244.583 good pairs (p7 = |F7|/2^32 = 2^-5.97763,
  p6 = |F6|/2^32 = 2^-3.90197). Measured on 2^23 real first blocks: 0.9997 x g.
- **Probability (Section 7, H2).** For a good pair, q3 = average over l in L* of Pr[rows 16..36 follow every cell
  and printed two-bit condition]. Rows 16..22 have exactly the same probability for every variant (Lemma 7.1); the
  variant enters rows >= 23 only through W8 in W23 = s1(W21) + W16 + s0(W8) + W7 and W24 = s1(W22) + W17 + s0(W9) +
  W8. A preregistered sequential Monte-Carlo estimate (32 replicates, W8 drawn from the 230,400 variants) gives mean
  2^-73.991 and a one-sided 99% lower bound 2^-74.0173: q3_model = 2^-74.0173 at the bound's printed face value (H6; the prereg rule's 2-decimal floor 2^-74.02 is priced in Section 11.2). The stage factors equal the
  published-S estimate of 6c77089c (2^-74.01) row by row; on the same 523,611 row-22 samples the rows 23..36 pass at
  2^-4.003 with the variants' W8 and 2^-4.000 with the published W8.
- **Cost (Sections 9, 11).** N_FB = 1,208,258,991,931,193,082 = 2^60.06764 first blocks; per first block 1 unit
  plus 686 counted operations (670 plus a control allowance of 16), plus on average 21,735.1 counted
  data-dependent operations (8,439 for the bit-sliced W6 programs, lane scans and per-class control, 12,963 for the
  good pairs, 300 per-hit setup, 34 for rows >= 16), all capped by V_MAX.
  T = A_C + A_S + DEV + N_FB + (N_FB 686 + V_MAX + overshoot + preprocessing + final)/C + 6 =
  33,439,063,720,091,432,886,104 / 2644 = 2^63.455446, claimed 63.45545.
- **Premises (Section 12).** H1 uniform independent chaining values; H2 q3 >= 2^-74.0173 for the variants (H6 fixes the level at the printed bound); H3
  given one success, the expected number of further successes in the same first block is small (<= 2^-9.4); H4 advice allowances (A_C = 2^60, A_S = 2^50,
  DEV = 2^40, as in the earlier filings); H5 counted word-RAM pricing of the bit-sliced W6 filter (not of any target
  compression: every compression is charged one unit). Without bit-slicing anywhere: 65.08487. The H6/H7 de-pad knobs (Section 16) lower 1c36817's 63.47455 by 0.0191.
- **Checks.** Exhaustive: |G| = 12,103,680; the 64 classes (3600 each); F6, F7 sizes and affine decompositions.
  End to end on real first blocks (Section 13): 2^21 + 2^23 first blocks, every rate as predicted; 496,800 lanes of
  the bit-sliced filter equal the scalar definition; every good pair satisfies the Step-2 equations; sampled good
  pairs follow every cell of rows -4..16. Semi-free-start collisions with variant dense parts (W8 different from the
  published pair) verified with the repository's `verifier/hash_functions._compress`. For 32,911 Step-3 successes
  of the SMC, none of the other 31 elements of L* also succeeds. Two organizer experiments
  (Section 13.3) repeat the semi-free-start construction and the online program on organizer seeds.

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
- **New here.** (i) The A0 freedom of the Step-1 solution and the variant family G (Section 4.3); (ii) the c7 classes
  and the per-class W7 test (Section 5.3); (iii) the bit-sliced per-class W6 program (Section 9.3); (iv) the proof
  that q3 is the same for all variants up to the W24 conditions, with a preregistered estimate (Section 7); (v) the
  first-block-level success analysis that allows many trials per first block (Section 10).

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
the whole class. The 64 classes used here have 3600 variants each (the 64 largest, ties by smaller c7; 85 classes
have 3600). Each class equals {base XOR s : s subset of mask, s in G, c7 = the class value} for the descriptors
below (c7, base, mask; checked exhaustively: 3600 members each):

```text
cc968c4c 1c2f8142 01fec08d  |  cc968c5c 1c2f8112 01fec08d  |  cc968c6c 1c2f8122 01fec08d  |  cc968c7c 1c2f8132 01fec08d
cc968c8c 1c2f8102 01fec08d  |  cc968e1c 1c2f8352 01fec08d  |  cc968e2c 1c2f8362 01fec08d  |  cc968e3c 1c2f8372 01fec08d
cc968e4c 1c2f8342 01fec08d  |  cc968e5c 1c2f8312 01fec08d  |  cc968e6c 1c2f8322 01fec08d  |  cc968e7c 1c2f8332 01fec08d
cc968e8c 1c2f8302 01fec08d  |  cc96901c 1c2f81d2 01fec48d  |  cc96902c 1c2f81e2 01fec48d  |  cc96903c 1c2f81f2 01fec48d
cc96904c 1c2f8542 01fec08d  |  cc96905c 1c2f8512 01fec08d  |  cc96906c 1c2f8522 01fec08d  |  cc96907c 1c2f8532 01fec08d
cc96908c 1c2f8502 01fec08d  |  ce968d1c 1e2f8052 01fec08d  |  ce968d2c 1e2f8062 01fec08d  |  ce968d3c 1e2f8072 01fec08d
ce968d4c 1e2f8042 01fec08d  |  ce968d5c 1e2f8012 01fec08d  |  ce968d6c 1e2f8022 01fec08d  |  ce968d7c 1e2f8032 01fec08d
ce968d8c 1e2f8002 01fec08d  |  ce968f1c 1e2f8252 01fec08d  |  ce968f2c 1e2f8262 01fec08d  |  ce968f3c 1e2f8272 01fec08d
ce968f4c 1e2f8242 01fec08d  |  ce968f5c 1e2f8212 01fec08d  |  ce968f6c 1e2f8222 01fec08d  |  ce968f7c 1e2f8232 01fec08d
ce968f8c 1e2f8202 01fec08d  |  ce96911c 1e2f8452 01fec08d  |  ce96912c 1e2f8462 01fec08d  |  ce96913c 1e2f8472 01fec08d
ce96914c 1e2f8442 01fec08d  |  ce96915c 1e2f8412 01fec08d  |  ce96916c 1e2f8422 01fec08d  |  ce96917c 1e2f8432 01fec08d
ce96918c 1e2f8402 01fec08d  |  ce96931c 1e2f8652 01fec08d  |  ce96932c 1e2f8662 01fec08d  |  ce96933c 1e2f8672 01fec08d
ce96934c 1e2f8642 01fec08d  |  ce96935c 1e2f8612 01fec08d  |  ce96936c 1e2f8622 01fec08d  |  ce96937c 1e2f8632 01fec08d
ce96938c 1e2f8602 01fec08d  |  d2968d1c 1a2f8052 01fec08d  |  d2968d2c 1a2f8062 01fec08d  |  d2968d3c 1a2f8072 01fec08d
d2968d4c 1a2f8042 01fec08d  |  d2968d5c 1a2f8012 01fec08d  |  d2968d6c 1a2f8022 01fec08d  |  d2968d7c 1a2f8032 01fec08d
d2968d8c 1a2f8002 01fec08d  |  d2968f1c 1a2f8252 01fec08d  |  d2968f2c 1a2f8262 01fec08d  |  d2968f3c 1a2f8272 01fec08d
```

Per first block: E[number of passing classes] = 64 p7 = 1.015625 and the expected number of good pairs (variants
passing both filters) is g = 64 x 3600 x p7 x p6 = 2003625/8192 = 244.583 (Lemma 5.1, linearity). Passing classes
are strongly correlated (their c7 values are close), so the counts are bursty; the expectations are exact.

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
two-bit condition closing at rows >= 16. q3 = average over the 230,400 selected variants and over l in L* of
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
rows 23..36: W8 of a variant drawn uniformly from the 230,400 selected variants (the same row-22 survivor is also
evaluated with the published W8 for a paired comparison). NP particles, M children per particle per stage, MT tail
proposals per particle, multinomial resampling of the survivors after every stage; the product of the stage means
is an unbiased estimator of q3 (standard SMC normalising-constant estimator: given the particles before a stage, the
stage mean is unbiased for the particle average of that stage's conditional probability; multinomial resampling
keeps particle averages unbiased; the expectation of the product telescopes).

### 7.4 Preregistration and results

Frozen at 2026-10-09T13:44:50Z before any listed seed ran (`PREREG_q3.txt`, SHA-256 4b0a1d39...; program `smc.c`
SHA-256 4a78d371..., `lab.h` 5e0e9605...): NP = 2048, M = 512, MT = 16384; replicate seeds 70000..70007,
71000..71007, 72000..72007, 73000..73007 (32 replicates); rule: one-sided 99% Student lower bound of the mean of the
32 linear estimates (t = 2.4528, 31 df), q3_model = 2^(floor(100 log2 LB)/100). All 32 replicates are reported.

| quantity | value |
|---|---|
| per-replicate log2 estimates (variant W8, seeds in order) | -73.988 -73.915 -73.981 -74.043 -74.009 -73.899 -74.041 -73.941 -74.064 -74.091 -74.015 -74.039 -73.912 -73.907 -74.028 -74.045 -74.088 -73.970 -73.968 -74.000 -73.943 -74.050 -73.889 -73.994 -74.002 -73.917 -73.938 -73.914 -74.092 -74.038 -73.996 -74.028 |
| mean | 2^-73.9908 |
| relative standard deviation | 0.0419 |
| 99% lower bound | 2^-74.0173 |
| **q3_model (H6, this filing)** | **2^-74.0173 (LB face value; prereg floor 2^-74.02 priced in 11.2)** |
| stage means (log2) | 16: -16.994, 17: -12.999, 18: -14.992, 19: -6.000, 20: -7.000, 21: -1.000, 22: -11.002, 23..36: -4.004 |
| rows 23..36, paired, over 523,611 row-22 survivors | variant W8: 32,660 passes (2^-4.003); published W8: 32,737 (2^-4.000) |
| same replicates with the published W8 | mean 2^-73.9875 |

### 7.5 Consistency

- The stage factors equal, within 0.01 bit, the per-row condition counts of the printed tables (17, 13, 15, 6, 7,
  1, 11, 4; 74 in total) and 6c77089c's published-S stage factors (16.994, 13.000, 14.996, 6.000, 7.000, 1.000,
  15.002 for rows 22..36 together); their preregistered published-S estimate is q3 = 2^-74.01 (mean 2^-73.9916).
- Lemma 7.1 makes rows 16..22 identical by construction; the paired rows-23..36 rates differ by 0.003 bit
  (77 passes out of 32,700, well within one standard deviation of the difference).
- Real first blocks (Section 13.1): the row-16 rate of the attack's own good pairs is the exact 2^-12.0 (z = +0.51
  over 503,050 passes).
- An earlier development run (8 replicates, NP = 1024, M = 256, MT = 4096, W8 from all of G) gave 2^-73.95 for both
  W8 choices; it is not part of the sample.

## 8. The algorithm (fixed caps)

```text
input: N_FB, V_MAX; precomputed: S, L*, the 64 class descriptors and their variant data (Section 9.3), the bitmaps
       of F6 and F7 (2^32 bits each), the table R16 (2^32 words of 32 bits), a 2^16-entry bit-index table
V = 0
for f = 1 .. N_FB:
    draw two uniform 256-bit words; M0 := their sixteen 32-bit fields; CV1 := F_37(IV, M0)          [1 unit]
    hits := [c : c7_c - A_{-1} in F7]  (64 tests)
    if hits:
        V += 1; compute the 64 broadcast planes of A_{-1} and C6 - A_{-2}
        for c in hits:
            V += 1
            for each batch of 256 variants of c: run class c's bit-sliced W6 program -> fail plane
                for each lane L with W6 in F6 (lane scan):
                    V += 1; a0 := variant; (first time in this first block: per-first-block constants, V += 1)
                    u := W0 + s0(W1); mask := R16[u]
                    if mask: V += 1; recompute W6, W7; for l in mask: rows 16..36 with early abort
                        if all rows pass: build m, m'; if digest(m) = digest(m') and m != m': output, halt
            if V > V_MAX: halt (failure)
halt (failure)
```

V counts every data-dependent operation in units of operations: the program adds each counted routine's cost (the
increments are shown once per routine above and are themselves counted). The run executes at most N_FB
compressions, N_FB x 686 fixed operations, V_MAX + one class's maximum work of data-dependent operations, the
precomputation and one final verification, whatever the coins.

## 9. The counted program

### 9.1 Machine and pricing

256-bit word RAM, 64 registers, every executed primitive counted (loads and stores included). 32-bit values are
kept in the low bits; a reduction mod 2^32 is one AND; a 32-bit rotation pattern (S0, S1, s0, s1) costs 8:
d = x | (x << 32) (2), three shifts and two XORs (or two shifts, one XOR and the s-function's plain shift) and one
mask. A bitmap lookup (2^32 bits in 256-bit words) costs 6: shr 8, add base, load, and 255, shr, and 1. The
target compression of a first block is one unit and its internal operations are not counted again. All counts
below are produced by running the routines of `experiments/a0core.py` (`calibrate`, deterministic and asserted
constant over 20 random inputs); `python3 a0core.py ledger` prints them.

### 9.2 Fixed per first block: 686 operations

- First block words: 2 random words, then the 16 fields (field 0 of a word: and; fields 1..6: shr, and; field 7:
  shr): 30.
- W7 tests: per class load c7, sub, and, bitmap (6), branch: 10; 64 classes: 640.
- Control allowance: 16 per first block (the loop counter's add and compare-branch, the hit-list initialisation,
  the `if hits` branch, and 12 for any further loop or address arithmetic not itemised elsewhere), and 8 per
  passing class (appending it to the hit list: store, add; iterating: load, add, branch; plus 3). The counted
  program adds both.

### 9.3 The bit-sliced W6 program (per passing class)

Per first block with a passing class: cb = (C6 - A_{-2}) mod 2^32 (2) and 64 broadcast planes AB_j = 0 - ((A_{-1} >> j)
& 1) and CB_j = 0 - ((cb >> j) & 1), each stored (4): 258.

The 3600 variants of a class are stored as 15 batches of 256 lanes (the last batch has 16 used lanes). For each
batch the stored planes are A0_j, K3_j (bit j of K3C - MAJ(A2, A1, a0)) and NE4_j (bit j of ~E4) for the bit
positions j where the value is not constant on the class (constant bits are folded into the program). One
straight-line program per class computes, bit-serially from j = 0 to 31:

```text
MAJ_j = A1_j ? (A0_j | AB_j) : (A0_j & AB_j)                                    (A1 is a global constant)
E3: ripple adder K3 + AB (carry needed up to bit 28)
Y_j = E5_j ? NE4_j : ~E3_j                                                        (= ~CH(E5, E4, E3), E5 constant)
carry-save add of (MAJ, Y, CB) then ripple add with carry-in 1:  W6 = cb + MAJ - CH  (mod 2^32)
fail = common | (W6_29 & B_bad & C_bad)                                         (the exact F6 test of 5.1)
```

where common = (W6_14^W6_18) | ~(W6_8^W6_25) | (W6_1^W6_12), bc = (W6_15^W6_19) | ~(W6_9^W6_26) | (W6_2^W6_13),
B_bad = bc | W6_30, C_bad = bc | ~W6_30 | (W6_16^W6_20^W6_31) | ~(W6_10^W6_27^W6_31) | (W6_3^W6_14^W6_31). A lane
passes (W6x in F6) iff its fail bit is 0. Per class the program has between 518 and 550 primitives per batch (mean
529.2 over the 64 classes; at most 105 loads, every load counted), with at most 25 simultaneously live values (no
spills on 64 registers). Then pass = ~fail & lanemask (2).

Lane scan per batch: 8 chunks of 32 bits (extraction: 1 op for chunks 0 and 7, 2 for the others; a zero branch
each): 22; per set lane: isolate the lowest bit (sub, and), its index from the 2^16-entry table on the low or high
half (at most 6: and, branch, shr, add base, load, add 16), clear it and form the lane (xor, add), loop branch: 11.

Class total: 15 x (program + 2) + 15 x 22 + 11 per passing lane + 3 (V update, compare, branch) + 8 (control).

**Correctness.** The program's fail plane equals the scalar definition (inF of W6x computed by Lemma 4.1) on every
lane: 43,200 lanes in development, 496,800 lanes (138 passing classes of 120 real first blocks) in the end-to-end
check, and every lane of every processed batch in the organizer experiment `a0-online-r37`.

### 9.4 Good pairs: 53 operations each

Per first block, at its first good pair (35): MAJ(A_{-1}, A_{-2}, A_{-3}) (4), S0(A_{-1}) (8), e0b = A_{-4} - S0 - MAJ
(3), CH(E_{-1}, E_{-2}, E_{-3}) (3), S1(E_{-1}) (8), kap0 = e0b - A_{-4} - E_{-4} - S1 - CH - K0 (5), A_{-1}|A_{-2},
A_{-1}&A_{-2}, E_{-1}^E_{-2} (3), kap1 = (A1 - K1) - E_{-3} (1). Then W0 = a0 + kap0, E0 = a0 + e0b.

Per good pair: lane scan 11; load a0, load S0(a0), index add (3); V update (1); then (38): E0 (add, and), W0 (add),
MAJ(a0, A_{-1}, A_{-2}) (and, or), CH(E0, E_{-1}, E_{-2}) (and, xor), S1(E0) (8),
W1 = kap1 - S0(a0) - MAJ - S1 - CH (4 subs, and), s0(W1) (8), u = W0 + s0(W1) (add, and), R16 lookup (shr 3, add base,
load, and 7, shl 5, shr, and: 7), branch.

### 9.5 Rows >= 16 (rare)

Per good pair with a non-empty row-16 mask (probability 2^-12.0 per good pair): V update (1), W6 and W7
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
  (H2, H6): E[X] >= N_FB g 32 2^-74.0173 >= mu0 = 0.49466253 (H7) for N_FB = ceil(mu0 / (g 32 2^-74.0173)) =
  1,208,258,991,931,193,082 = 2^60.06764; mu0 is the smallest 8-decimal strictly above
- **One first block (H3).** By Bonferroni, Pr[X_f >= 1] >= E[X_f] - sum over pairs t < t' of f of Pr[A_t and A_t']
  = E[X_f] - (1/2) sum_t Pr[A_t] E[X_f - 1 | A_t]. H3: E[X_f - 1 | A_t] <= delta = 2^-9.4 for every trial t,
  so Pr[X_f >= 1] >= (1 - 2^-10.4) E[X_f]. (Only the expected number of *further* successes of the same
  first block given one success is needed; bursty goodness and shared W7/W6 values enter only through
  that conditional expectation, and do not affect E[X], which is linear.)
- **Many first blocks (H1).** Distinct first blocks have independent chaining values, so the events X_f >= 1 are
  independent and Pr[X >= 1] >= 1 - exp(-sum_f Pr[X_f >= 1]) >= 1 - exp(-(1 - 2^-10.4) mu0)
  = 0.3900002 (H7 fixes mu0; Section 16 prices the slack).
- **Work cap.** The data-dependent work v_f of a first block (everything except its compression and its 686 fixed
  operations) has mean at most vbar = 21,735.1351 (the sum of Section 11's terms, which charges the per-hit setup
  per passing class rather than per first block and the row-16 work per (pair, l)) and is at most
  64 x 389,042,613 + 2000 < 2^34.55 (every class passing, every variant good, every l past row 16 to row
  row 36). The v_f are independent (H1), so by Chebyshev
  Pr[sum v_f > (1+2^-8) N_FB vbar] <= E[v_f^2]/(2^-16 N_FB vbar^2) <= 2^34.55/(2^-16 2^60.07 vbar)
  < 2^-23.9. V_MAX = ceil((1 + 2^-8) N_FB vbar) = 26,364,257,031,217,720,093,047 is reached with
  probability below 2^-23.9; the run then fails, which is accounted for here.
- **Success.** Pr[output a collision] >= 0.3900002 - 2^-23.9 - 2^-60 > 0.39 (the 2^-60 covers a repeated
  first block among N_FB draws of 512 bits). With q3 = the SMC mean instead of its lower bound the
  bound is 0.3920. Any output is a verified collision, independent of the premises.

## 11. Ledger (exact; `python3 experiments/a0core.py ledger`)

```text
T = A_C + A_S + DEV + N_FB + (N_FB x 686 + V_MAX + vmax_class + PRE + FIN) / C + 6
  A_C = 2^60   characteristic search and SFS-pair search of the paper (allowance, H4)
  A_S = 2^50   Step-1 SAT solve (paper: 2^41.3)
  DEV = 2^40   all development computation (Section 13.4)
  N_FB = 1,208,258,991,931,193,082 compressions (2^60.06764; H7 mu0 = 0.49466253, H6 q3 = 2^-74.0173)
  686          fixed operations per first block (9.2: 30 + 640 + 16 control)
  V_MAX = 26,364,257,031,217,720,093,047 = ceil((1 + 2^-8) N_FB vbar), vbar = 21,735.1351 ops, of which
               per passing class (64 p7 = 1.015625 per first block): setup 1 + 258 + 35 + 1 = 295 -> 299.61
               W6 programs, lane-scan fixed costs and class control: p7 x sum over the 64 classes of
                 (8 + 1 + 15 (prog_c + 2) + 330 + 2) = p7 x 531,794 -> 8,439.11
               good pairs: g x 53 -> 12,962.91
               rows >= 16: g x 2^-12.0 x (225 + 328 + (19/512) 160) -> 33.51
  vmax_class = 389,042,613 (one class max work: overshoot past the last cap test)
  PRE = 2^40 operations (bound on all precomputation, Section 11.1); FIN = 1600 operations (the final verification and
  the next first block's setup after the last cap test) and 6 compressions
T x 2644 = 33,439,063,720,091,432,886,104     ->   T = 2^63.455446  ->  time_log2 = 63.45545
preprocessing = A_C + A_S + DEV + PRE/C = 2^60.00141
```

The online terms are 2^60.0676 (compressions), 2^58.1212 (fixed ops) and 2^63.1125 (V_MAX); A_C adds
2^60. Every count in this block is produced by `calibrate()` and `ledger()` of `experiments/a0core.py`.

### 11.1 Precomputation (bounded by 2^40 operations)

Enumerating G and c7 over all 2^32 words (about 40 operations each, 2^37.4); grouping the 12.1 million variants
by c7 and selecting the 64 classes (below 2^30); the bitmaps of F6 and F7 (each word: two s0 evaluations, an add,
a sub, a compare and an or into the bitmap word, about 22 operations, 2^37.5 for both, plus 2^28 stores); R16 (2^29
zeroing stores and 32 x 2^22 row-16 evaluations at about 150 operations, 2^34.3); the 64 class programs and their
960 batches of stored planes (below 2^26); the 2^16-entry index table. Total below 2^38.6 operations.

### 11.2 Sensitivity (log2 T, one input changed)

| change | log2 T |
|---|---|
| as claimed | 63.45544 |
| q3 lower by 0.25 bit | 63.68435 |
| q3 lower by 0.5 bit | 63.91637 |
| q3 lower by 1 bit | 64.38808 |
| q3 = 2^-75 (the paper's count of 75 conditions) | 64.37161 |
| A_C = 2^64 | 64.69876 |
| A_C = 2^56 | 63.32656 |
| scalar W6 test (no bit-slicing anywhere; 18 operations per variant) | 65.08487 |
| H6 pad kept q3=2^-74.02 / 1c36817 verbatim (mu=0.501953125) | 63.45790 / 63.47455 |

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
- Sensitivity: A_C = 2^64 (another 16x) gives 64.69876; A_C = 2^56 gives 63.32656. No other term depends on it.

## 12. Premises

**H1 - uniform independent chaining values (score-critical).** The first blocks are fresh uniform 512-bit strings;
their chaining values CV1 = F_37(IV, M0) behave as independent uniform 256-bit values. Used for: Lemma 5.1 (exact
filter rates and the law of the second-block words, per variant), the expected counts, the independence across
first blocks (Section 10) and Chebyshev. Evidence: 2^21 and 2^23 real first blocks through the attack's own filters
(Section 13.1: passing classes, good pairs and row-16 passes at the predicted rates); the organizer experiment
`a0-online-r37`. Limitations: a premise; tested on 2^23 first blocks, not 2^60.07.

**H2 - Step-3 probability of the variants (score-critical).** q3 >= q3_model = 2^-74.0173 (H6 level; Section 7.1's average over
the 230,400 selected variants and L*), and q3 <= 2^-70. Evidence: Lemma 7.1 (rows 16..22 identical for all variants;
the variant enters only through W8 in W23, W24), the preregistered SMC (Section 7.4), the paired comparison of
rows 23..36, the agreement with 6c77089c's published-S estimate row by row, the row-16 rate of real good pairs, and
37-step semi-free-start collisions built with variant dense parts (Section 13.2, organizer experiment
`a0-sfs-r37`). The 32 replicate estimates are nearly symmetric (skewness 0.15, relative sd 0.042, all 32 at least 2^-74.092); a
percentile bootstrap of their mean (200,000 resamples) puts its 1% quantile at 2^-74.015, agreeing with the Student
bound 2^-74.017. Limitations: a Monte-Carlo bound whose coverage rests on the approximate normality of the mean of 32
replicates (each replicate is a product of eight stage means over at least 2^20 children); the `+` reading.

**H3 - few further successes per first block (score-critical).** For every trial t, the expected number of other
successful trials of the same first block given A_t is at most delta = 2^-9.4, i.e. E[X_f - 1 | A_t] <= 2^-9.4.
It splits into (a) the same variant with another l in L*, and (b) other good pairs (other variants) of the same
first block. For (a) the premise is E[#other l succeeding | A_t] <= 2^-11; measured directly on 32,911 Step-3
successes of the SMC with the variants' W8 (`replay`, Section 13.1): rebuilding W0..W5 and testing the other 31
elements of L* through rows 16..36 gave 0 further successes (every success re-checked with its own l passes); the
95% upper bound of the per-success rate is 2^-13.4 (the samples share SMC ancestors, so they are not independent).
For (b) the expectation is at most rho x (230,400 x 32 x q3) <= rho x 2^-47.19 with q3 <= 2^-70 (H2), where rho bounds
Pr[t' succeeds | t succeeds, t' good] / Pr[t' succeeds | t' good] for good pairs t' != t of the first block; the
premise is rho <= 2^37, and the measured factor at the row-16 level over 2^23 real first blocks is 1.001 (sum of
R(R-1) = 1,436,276 against p^2 sum of G(G-1) = 1,435,367.8, R row-16 passes and G good pairs per first block). So
delta <= 2^-11 + 2^-10.19 < 2^-9.4. Bursty goodness (variants of one class share W7; a class's 3600 variants give
only 32..512 distinct W6 values for a given chaining value) does not enter: the bound conditions on t' being good.
Limitations: rows >= 17 of distinct good pairs cannot be measured jointly within one first block; the premise
leaves a margin of 2^37 over the measured row-16 factor.

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
give 64.69876.

**H5 - counted word-RAM pricing of the bit-sliced W6 filter (score-critical; cost reading).** A straight-line
program of 256-bit primitives that evaluates the W6 filter of 256 variants at once (bit L of each word belongs to
variant L) is charged its counted primitives (518..550 per batch, every load counted, at most 25 live values on 64
registers). This program evaluates no target compression; every compression is charged one unit. Evidence: the
program is in `experiments/a0core.py` (`gen_w6`, `run_w6`), bit-exact against the scalar definition (Section 9.3).
Limitation: no organizer ruling is cited; with a scalar W6 test (18 operations per variant) the claim is 65.08487.

Not used: expected work, an independence-of-conditions model for q3 (replaced by the SMC), a random-oracle model,
any premise on the published pair beyond its verified values.

## 13. Evidence and runs

All runs on one Apple-silicon Mac (8 cores), our own code (C and Python standard library; no rival code executed).

### 13.1 End to end on real first blocks (`e2e.c`, Appendix A)

Random M0 (xoshiro-style generator seeded per thread), CV1 = F_37(IV, M0) by our compression (equal to the
repository verifier on the checked pairs), the 64 W7 tests, the scalar W6 test of every variant of every passing
class, u and the exact row-16 test for every l, exact checks of sampled pairs (Lemma 4.1 words, W6/W7 filters,
every cell of rows -4..16 and the two-bit conditions closing at rows 15, 16).

| run | first blocks | passing classes (expected) | good pairs (expected) | row-16 passes (expected) | exact checks |
|---|---|---|---|---|---|
| seed 1 | 2^21 | 2,134,874 (2,129,920) | 516,134,885 (512,928,000; 1.0063) | 126,066 (126,501.7; z -1.23) | 16,000, 0 failures |
| seed 3 | 2^23 | 8,510,833 (8,519,680) | 2,051,007,293 (2,051,712,000; 0.9997) | 503,050 (502,690.2; z +0.51) | 16,000, 0 failures |

The passing-class counts are overdispersed relative to a Poisson model (classes are correlated) but their means
match (ratios 1.0023 and 0.9990). Within-first-block row-16 correlation (seed 3): factor 1.001 (H3).
Same-pair co-successes (`replay`, the SMC program with one addition, not part of the preregistered sample; seeds
90..93, NP = 2048, M = 512, MT = 16384): 32,911 Step-3 successes with the variants' W8; each was rebuilt (W0..W5 by
the inverse expansion) and re-checked with its own l (32,911 passes) and with the other 31 elements of L* through
rows 16..36: 0 further successes (H3 (a)).
The condition tables of the C programs (`lab.h`) and of the attack program (`a0core.py`: cells of A, E, W and the 31
printed two-bit conditions) were compared programmatically: identical. Conversely, the semi-free-start pairs built by
the C program pass the attack program's own step 3b (Section 13.2), and the pairs built by `a0core.py` pass the
repository verifier.
The counted Python program (`a0core.online`) on 120 further first blocks: 138 passing classes, 26,716 good pairs, 8
row-16 passes; all 496,800 lanes of its bit-sliced filter equal the scalar test; every good pair satisfies the
Step-2 equations; 22,110 operations per first block on average (model 670 + vbar = 22,396; the difference is the
sampling noise of 138 bursty classes).

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
  class and variant from the 64 selected classes and a seed-chosen l among the 28 elements of L* whose row 16 can
  hold (rows 16..21 by proposals with the row's fixed x-bits of E imposed; row 22 by W22 proposals with its x-cells
  and two-bit conditions imposed, W7 uniform on F7, W6 = W22 - s1(W20) - W15 - s0(W7) accepted iff in F6). It
  returns CV1 || M1 and CV1 || M1' (96 bytes each) iff every check of 13.2 passes plus class membership. These are
  semi-free-start collisions (CV1 is not the IV), so the organizer's full-collision event is not expected; anyone
  can verify them from the raw report with `_compress(..., 37)`. Rows 16..21 restart from row 16 if a row needs more
  than 2^11 proposals (at most 12 restarts); W7 is drawn exactly from F7's affine decomposition. Local emulation of
  the organizer's public-seed request (seed protocol of `experiments/runner.py`, seed `hashsmash-public-seed-v1`, no
  holdout nonce, target configuration 3e8cc338...): 16 of 16 trials returned a pair, all 16 verified 37-step
  semi-free-start collisions under the repository verifier; 1.2 s; stdout SHA-256 1e9acad2..., byte-identical on a
  second run.
- `a0-online-r37` (H1, H3, H5): trials 0..7 each run the counted online program on seed-drawn first blocks until a
  first block with a passing class (at most 64), processing at most two passing classes; every lane of every batch
  is checked against the scalar W6 definition, every good pair against the Step-2 equations, and up to 12 good
  pairs against every cell of rows -4..15 for all 32 l. It returns the complete 128-byte messages M0 || M1 and
  M0 || M1' (l = 13) of the first good pair iff all checks passed (they are not expected to collide: that needs rows
  16..36). Local emulation of the public-seed request: 0 mismatches of every kind in all 8 trials; 4 trials returned
  a pair (good pairs 1808, 960, 1792, 96; the other first blocks' passing classes had no W6 pass among the two
  processed classes: good pairs come in bursts, Section 5.3); 2.4 s; stdout SHA-256 96f7f076...,
  byte-identical on a second run.
- Both are deterministic, standard library only, and run well inside the executor's limits locally.

### 13.4 Development computation

Below 40,000 CPU-seconds in total (the preregistered SMC about 1,000; the end-to-end runs, each made twice, about
25,000; enumerations, the counted Python program and checks the rest), far inside DEV = 2^40 units (2^40 units are
about 2^18.3 = 330,000 CPU-seconds at 2^21.7 units per CPU-second).

## 14. Memory and advice

Peak memory (all simultaneously resident during the online phase):

| item | bytes |
|---|---|
| R16: 2^32 entries of 32 bits | 17,179,869,184 |
| F6 and F7 bitmaps: 2 x 2^32 bits | 1,073,741,824 |
| bit-index table: 2^16 words of 32 bytes | 2,097,152 |
| variant data: 230,400 x (a0, S0(a0)), one 32-byte word each | 14,745,600 |
| stored planes: 960 batches x at most 41 planes x 32 bytes | 1,259,520 |
| class programs: 64 x at most 550 instructions x 32 bytes | 1,126,400 |
| broadcast planes, registers, S, L*, row constants, code of the driver | below 1,048,576 |
| total | below 18,273,888,256 = 2^34.090 |

Claimed memory: 2^34.1 bytes. The precomputation's temporaries (the 12.1 million (c7, a0) pairs, 97 MB) are freed
before the tables reach their peak. Nonuniform advice: the characteristic, S, L* and the 64 class descriptors (below
2^13 bytes), charged through A_C and A_S; everything else is recomputed in the precomputation.

## 15. Limitations

- H1, H2, H3 are premises. q3 is estimated (Monte Carlo), not proved; no collision has been found and none is
  expected at the scale we can run. The full-scale success probability cannot be observed.
- The published characteristic and SFS pair are used as advice under allowances; we did not rerun the paper's
  SAT solve or characteristic search.
- For 37 steps the measured q3 is about one bit better than the 75 conditions stated in the paper's text; the
  paper's own tables give 74, which the SMC matches stage by stage (6c77089c reached the same conclusion). With
  q3 = 2^-75, log2 T would be 64.38903.
- The W6 bit-slicing relies on H5; without it the claim is 65.08487.
- Memory is large compared with the earlier filings (2^34.1 bytes instead of 2^20) because of the R16 and filter
  tables; memory is reported only under v5.


## Appendix A. Local evidence programs and records

These are the C programs (C99 + pthreads, `cc -O3`) that produced the local evidence of Sections 4, 7, 10 and 13,
and the records of the preregistered estimate and of the replay. They are evidence for the reader, not part of the
attack. The attack's counted program, the class data and the organizer experiments are `experiments/a0core.py`
(standard-library Python; `python3 a0core.py ledger` prints Section 11's numbers). Each block's SHA-256 is given in
its header line. `e2e.c` is the program of both end-to-end runs (Section 13.1). `replay.c` is `smc.c` with the
replay block added (not part of the preregistered sample).

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

### A.2 `smc.c` (7605 bytes, SHA-256 4a78d3718e22ca887a6e2dbb351d24a2ed539ab9908127ce6b756bf24264ccca)

```c
/* smc.c - sequential Monte-Carlo estimate of q3 = avg over l in L* of Pr[rows 16..36 follow every cell and the
   printed two-bit conditions], for the A0 variant family: W16..W21 iid uniform, (W6, W7) uniform on F6 x F7, and
   W8 = W8C - E4(a0) with a0 uniform on G.  Stages: row 16 (exact enumeration), rows 17..21 (proposal: E_t^x uniform
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
  else { static CL cc[64]; Gn = select_classes(64, cc, &Glist); }
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

### A.10 `replay.c` (9478 bytes, SHA-256 3879da40b97a6c4d75283dd4810ce16d01d1dbd39cb59f90b228065692cb3807)

```c
/* replay.c - (from smc.c) for every tail success with a variant's W8, rebuild W0..W5 and test every other l in L*
   through rows 16..36 (same first-block words, same variant): counts co-successes.  Not part of the preregistered sample.
   Original header: sequential Monte-Carlo estimate of q3 = avg over l in L* of Pr[rows 16..36 follow every cell and the
   printed two-bit conditions], for the A0 variant family: W16..W21 iid uniform, (W6, W7) uniform on F6 x F7, and
   W8 = W8C - E4(a0) with a0 uniform on G.  Stages: row 16 (exact enumeration), rows 17..21 (proposal: E_t^x uniform
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
  else { static CL cc[64]; Gn = select_classes(64, cc, &Glist); }
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

## 16. What this filing changes relative to the head 1c36817

The machine, the geometry, the counted program, the preregistered SMC run and
every premise H1-H5 are 1c36817's, unchanged, with its authors credited. This
filing changes two declared readings (Section 12, H6 and H7) and nothing else:

- **H6 (score-critical, -0.0026 bits).** q3_model = 2^-74.0173, the printed
  one-sided 99% bound at face value, instead of the prereg print rule's
  2-decimal floor 2^-74.02. The bound is conservative twice over (99%
  confidence; the bootstrap 1% quantile 2^-74.015 is even higher).
- **H7 (supporting, -0.0166 bits).** The cap target is mu0 = 0.49466253, the
  smallest 8-decimal strictly above -ln(0.61 - 2^-23.9 - 2^-60)/(1 -
  2^-10.4) (proof.md Section 10), instead of (1 + 2^-9)/2 = 0.501953125. The
  Chebyshev (2^-23.9) and repeated-first-block (2^-60) allowances sit as
  explicit terms inside the floor instead of inside an unexplained pad; the
  success bound is 0.3900000035.
- `experiments/a0core.py ledger` now computes N_FB with an exact-rational
  ceiling and asserts, at every run: N_FB g 32 q3 >= mu0, the success bound
  > 0.39, and T^100000 bracketing 2^(claim x 100000) both ways between
  2^(claim x 100000 - 1) and 2^(claim x 100000) (integer-tight at 5 dp in
  both directions).

Claim: T = 8,359,765,930,022,858,221,526 / 661 = 2^63.455446, time_log2
63.45545. Head 1c36817 claims 63.47455; the delta is 0.0191 bits. The
q3-sensitivity table (Section 11) prices every alternative reading within
0.25 bits, including both pads restored (63.47455, the head).

