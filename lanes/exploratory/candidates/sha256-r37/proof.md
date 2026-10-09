# Collision attack on 37-step SHA-256 with a family of 2^18 Step-1 solutions: 2^64.0687

This package claims a worst-case total of at most 2^64.0687 target compressions for a classical randomized
algorithm that outputs an ordinary collision of the exact `sha256-r37-prefix-v1` target with probability at least
0.39 (our bound: 0.4054). The algorithm is the two-block collision attack of ePrint 2026/1120 (Li, Zhang, Li, Liu, Qian, Zhu, "Pushing
Collision Attacks on SHA-2 to 39 Steps") with one new ingredient. The Step-1 solution S of the dense part has a free
word: changing A0 changes only E4 and W8 inside the dense part. We use 2^18 such solutions S'_k at once, so every
first block is tested against 2^18 Step-2 filters through a lookup table. This removes the factor 2^9.88 of first
blocks per usable chaining value that dominates every earlier accounting of this attack. The previous best filing for
this track is 73.94602 (submission f09f56e7: one Step-1 solution, 2^77.9 first blocks evaluated bit-sliced at about
0.064 units each); the nominal reference is 128.

The cryptanalysis (characteristic, Step-1 solution, Step-2/3 structure) is the paper's. The transcription of its
tables, the exact Step-2 sets, the freedom set L*, Lemmas 1 to 4 and the allowances A_C/A_S/DEV are reused from the
public packages 6c77089c (winglock) and f09f56e7 (Th0rgal), declared as dependencies. We re-verified all of them with
independent code. New here: the variant family and its validity proof (Section 4), the table-driven program and its
instruction listing (Section 5), our own preregistered estimate of q3 for the variant family (Section 6), the
Chen-Stein success argument that needs no independence between variants of one chaining value (Section 7), and the
first-block measurements of Section 10.

## 0. Summary

- **Target and output (Section 1).** Two 128-byte messages M0 || M1 and M0 || M1' (FIPS padding appends the same third
  block) whose complete 37-step SHA-256 digests from the standard IV are equal. Every output is verified with the
  target before it is returned.
- **Variant family (Section 4).** For the published Step-1 solution S (rows 0..13 and W8..W13 of the paper's
  semi-free-start pair), replacing A0 by A0' = E4' + A0B changes, inside rows 0..13, only E4 (to E4') and W8 (to
  W8' = C8X - E4'). S'(E4') follows every cell of rows 0..15 for both members, keeps d6, d7, L* and the row-16
  differences, iff E4' < 2^29, W8' bit 29 = 1 and the sigma0 difference of W8 is unchanged. Exactly 12,103,680 values
  of E4' qualify (exhaustive count). We fix a set V of K = 2^18 of them by a closed formula. For every variant the
  law of rows 16..22 given a valid chaining value is the same as for S. Only W24's four bit conditions see W8'.
- **Algorithm (Section 5).** Preprocessing builds a table indexed by A_{-1}: bucket A lists every (k, u) with
  c7_k - A in F7. Online, each first block M0 (two fresh random words) gives CV1 = F_37(IV, M0). Its bucket
  (4160 entries on average) is scanned at 6 operations per entry with a table test of W6 in F6. A surviving (CV1, k)
  is a valid pair (278.28 per first block on average; a single S gives 2^-9.88). For each valid pair the program
  computes W0, W1, looks up which elements of L* pass the 10 bit conditions of E16, and on a hit (rate 28/1024) checks
  E17's 11 bit conditions, then compares the two second-block outputs with two target compressions.
- **Cost (Sections 5, 8).** Per first block: one target compression plus 91 operations; per bucket entry 6; per valid
  pair 46; rare paths 155 + 28 per hit; final checks 114 + 2 compressions. These counts come from the instruction
  listing of Section 5.2, which the organizer experiment executes and counts. With C = 2644,
  N = 1,115,062,431,311,676,075 first blocks (2^59.95183), caps 3.1% above the expected data-dependent work, the
  overshoot of one first block past a cap, and the allowances A_C = 2^60, A_S = 2^50, DEV = 2^40, every run costs at
  most T = 2^64.068697 units, claimed as 64.0687.
- **Probability (Sections 6, 7).** q3 = the average over k in V and l in L* of Pr[every cell of rows 16..36 holds] for
  a valid pair. Our preregistered SMC estimate (8,192 replicates) is 2^-73.9924, with a one-sided 99% bound of
  2^-74.0050, so q3_model = 2^-74.01, which equals (after rounding down to 0.01 bits) the earlier independent bound
  for S alone (2^-74.0074), and
  rho = q3_V/q3_S = 0.9993. Across 975,395 replayed successes of S and 240,260 of variants, no second element of L*
  ever succeeded (kappa = 255/256 is charged). N is chosen so that mu = N * 278.28 * 32 * q3_model * kappa = 0.52.
  The Chen-Stein bound gives Pr[success] >= 1 - e^-0.52 - 6e-7 > 0.4054. Success stays >= 0.39 even if q3 or the
  validity rate falls 4.9% short (q3 down to 2^-74.083).
- **Heuristics (Section 9).** H1 uniform chaining values, H2 the Step-3 probability of the variant family and H4 the
  advice allowances (all score-critical); H3 bounded dependence between variants of one chaining value (supporting; a
  factor 2^30 is allowed, 1.001 is measured). Independence across first blocks is exact.
- **Evidence (Section 10).** 7,792,827 rebuilt and verified 37-step semi-free-start collisions of variants S' != S
  (0 failures). On 40,000 real first blocks: 11,068,722 valid pairs (11,131,250 expected) and buckets of 4134.4 +- 43.7
  entries (4160 expected), and every pair follows every cell of rows -4..15 (354,199,104 checks, 0 failures). Two
  organizer experiments are in `experiments/v37.py`.

## 1. Target, cost model and output

- **Target** `sha256-r37-prefix-v1`: SHA-256 steps 0..36 on every padded block, the standard IV once at the start of
  the complete message, FIPS 180-4 padding, feed-forward, all eight digest words (`verifier/hash_functions.py:digest`
  with rounds 37). The relation is two distinct complete messages with byte-identical digests.
- **Cost model** `collision-frontier-v5`: one 37-step target compression (one call on a chaining value and a 512-bit
  block, including its feed-forward) costs 1 unit. Every other executed 256-bit word primitive costs 1/C units, with
  C = 2644 for sha256-r37. Primitives are load, store, add/sub, and/or/xor/not, shift, comparison, conditional
  branch and uniform random 256-bit word. Total time is summed over all processors and includes preprocessing,
  randomness, failed trials, sorting/lookups, checking and verification. Memory is reported only. Success must be at
  least 0.39 over fresh algorithmic coins.
- **Machine conventions.** A program with at most 64 registers. The listing uses 80 symbolic register names, but at
  most 38 are live at any instruction (backward liveness analysis, `live.py`, Appendix A), so they rename into 64
  physical registers. Each executed instruction costs one primitive. Every compare-and-branch costs two (comparison +
  conditional branch) and an unconditional jump costs one. `nop` only carries a label for the next instruction and
  is not an instruction.
  Immediates and shift amounts are instruction fields. A load or store addresses memory through a register. Every
  address computation is a separate add and is counted. A target-compression call costs 1 unit plus 4 counted
  operations for operand moves. These are the conventions of the d1 packages (6c77089c, f09f56e7).
- **Notation.** In step i, E_i = A_{i-4} + E_{i-4} + S1(E_{i-1}) + IF(E_{i-1}, E_{i-2}, E_{i-3}) + K_i + W_i and
  A_i = E_i - A_{i-4} + S0(A_{i-1}) + MAJ(A_{i-1}, A_{i-2}, A_{i-3}) (mod 2^32). The incoming chaining value is
  (A_{-1}, A_{-2}, A_{-3}, A_{-4}, E_{-1}, E_{-2}, E_{-3}, E_{-4}) = (a, b, c, d, e, f, g, h). The output is
  cv + (A_36, A_35, A_34, A_33, E_36, E_35, E_34, E_33). Member x is the message the paper prints second (M'),
  member y the one printed first; d = y - x for modular differences.

## 2. Sources, dependencies and what we checked

- **Paper.** Yingxin Li, Zhuolong Zhang, Muzhou Li, Fukang Liu, Haifeng Qian, Jinwei Zhu, "Pushing Collision Attacks on
  SHA-2 to 39 Steps", IACR ePrint 2026/1120. Its 37-step attack works in three steps. Step 1 solves the dense part
  (A0..A13, E4..E13, W8..W13) with a SAT solver (reported 2^41.3). Step 2 tries random first blocks until the chaining
  value satisfies the W6/W7 conditions. Step 3 uses the (W14, W15) freedom against the uncontrolled conditions of rows
  >= 16. The total is 2^79.1 as expected work with one Step-1 solution. Framework: Li, Liu, Wang, Shi, ePrint
  2026/1080 (CRYPTO 2026). Tool: Li, Liu, Wang, EUROCRYPT 2024.
- **Reused from earlier filings (declared dependencies).** 6c77089c (winglock) and f09f56e7 (Th0rgal) transcribed
  Tables 15 to 17 and verified them against the published pair. They found the exact Step-2 requirement (the sets
  F6, F7) and the exact freedom set L* (|L*| = 32, four elements that never succeed), and proved Lemmas 1 to 4 below. They
  designed the q3 SMC (staged proposals with x-value cells fixed, tail with W7 ~ U(F7)) and the allowance scheme
  A_C/A_S/DEV. We reuse these with credit. Any mistakes in the new parts are ours.
- **Independently re-verified by us** (own code, not executing any other package's code): the published pair
  collides under our compression and the repository verifier, and every cell of rows -4..36 holds with x = M'; S, d6,
  d7, t6, t7, c7 = d296fb78 and c6 = f538a8f7 for S; |F6| = 287,309,824 and |F7| = 68,157,440 by exhaustive count;
  L*'s 32 elements, and the 4 that never succeed (0, 2, 16, 18; they die at row 17) by our SMC; our own q3 estimate for S (2^-73.9914) agrees with
  f09f56e7's 2^-73.99.

## 3. The characteristic

Symbols are MSB first. `n` means bits (x, y) = (0, 1), `u` means (1, 0), `0`/`1` are fixed and equal, `=` means equal.
`+` (undefined in the paper) sits in vertical pairs E_r[b], E_{r+1}[b] and is read as equality, following the d1
packages. With x = M' every cell holds on the published pair. Rows with a non-`=` cell (i, A_i, E_i, W_i):

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

The `+` pairs are (r, b) = (5, 6), (5, 7), (8, 25), (9, 0), (9, 14), (13, 17), (13, 30), (15, 4), (16, 15),
(16, 24). The success event of this package uses the cells only. The printed two-bit conditions of the paper's
Table 16 are not used; on rows >= 16 the necessary ones are implied by later cells.

The published SFS pair (Table 17), from which S is read:

```text
CV  63b4986c 35d83dc0 c98894e4 784e08fc 78a7f752 5ed877a8 315a2db3 d5614eb4
M   4d7f86ff 32ece589 d8accfc4 2cc2e433 068b5b34 eba68a28 2fe12cad 6aa26b0c
    9f0d78e1 681b8277 faa9c7e0 56aed439 cc2dbbc2 dd2ba0fc b95d377b 5dd43a81
M'  4d7f86ff 32ece589 d8accfc4 2cc2e433 068b5b34 eba68a28 0fe12cad 6ee2630c
    bf0d78e1 6d1a90dd faa1d3e0 56aed439 cc2dbbc2 dd2ba0fc bd1d3f7b 7dd43a81
hash a856d46e 4b46eb28 4935248c 92a2fc98 e0fb2610 10a9951f 54264f5b 80954580
```

## 4. Step 1 solutions: the variant family

### 4.1 The published solution S

S is the inner part of the published pair: run F_37 from its CV on x = M' and y = M and keep A0..A13, E4..E13 and
W8..W13 of both members. Member-x values (member y differs only where the table has u/n):

```text
A0..A13  1b21ce20 62827866 987f24c4 44294b96 a8ccc9b3 a26653f8 210c2860 7246d008 7c4a1e59 edc43977
         030eaaa0 1ae4bc99 2fd3ea18 9992b350
E4..E13  1b2d044e e7f2c81f eb0b9c2d 9a404eb1 7b3e8fa7 9a3c74f0 87a8fadc b0741f5f 6fd5b358 66f25d89
W8..W13  x: bf0d78e1 6d1a90dd faa1d3e0 56aed439 cc2dbbc2 dd2ba0fc   y: 9f0d78e1 681b8277 faa9c7e0 (rest equal)
y-member A6 410c2860 A7 7267d818 A10 010e8aa0 A11 12c4b68b A12 4fd3ea18 A13 919033c0
y-member E6 0b0b9c2d E7 b2645641 E8 7f768aa3 E9 9a3c74e0 E10 a5a8dadc E11 a875495a E12 6825b602 E13 6eeedd89
```

### 4.2 Changing A0: the family S'(E4')

In the A/E form, E_i = A_i + A_{i-4} - S0(A_{i-1}) - MAJ(A_{i-1}, A_{i-2}, A_{i-3}) for every step. Hence, with
A1..A13 fixed, E_i for i = 5..13 depends only on A1..A13, while E4 = A0 + A4 - S0(A3) - MAJ(A3, A2, A1) = A0 - A0B,
with A0B = A0 - E4 = fff4c9d2 (mod 2^32). Rows 0..3 have no cell, so A0 is otherwise unconstrained. For a value E4'
define S'(E4') as S with A0 := E4' + A0B (both members) and E4 := E4'. The message words of rows 8..13 are
determined by the states: W_i = E_i - A_{i-4} - E_{i-4} - S1(E_{i-1}) - IF(E_{i-1}, E_{i-2}, E_{i-3}) - K_i. Among
W8..W13 only W8 contains E4 (as -E_{i-4} with i = 8), so S' keeps W9..W13 and has

```text
W8'x = C8X - E4',  W8'y = C8Y - E4',  C8X = da3a7d2f, C8Y = ba3a7d2f,  W8'x - W8'y = 2^29.
```

**Lemma V (validity of a variant).** S'(E4') follows every A, E and W cell of rows 0..13 for both members and the `+`
pairs, iff (i) E4'[31..29] = 000, (ii) W8'x[29] = 1, and (iii) s0(W8'y) - s0(W8'x) = 043ff800, the value on S.
Moreover d6 = 20000000, d7 = fbc00800 (y - x of W6, W7), L*, rows 14..15 and the modular differences of row 16 are
the same as for S.

*Proof.* The A and E values of rows 4..13 equal S's except E4, so all their cells hold except possibly E4's
(`000` on bits 31..29, which is (i)). No `+` cell involves E4. Of W8..W13 only W8 changes. Its cell (`u` at bit 29,
x - y = 2^29 fixed) holds iff (ii). W8 enters rows >= 16 only through s0(W8) in W23 and W8 in W24. W24's modular
difference is unchanged because d(W8) is. W23 needs d(s0(W8)) unchanged, which is (iii); (iii) is equivalent to the
three conditions W8[1] != W8[12], W8[8] != W8[25], W8[14] = W8[18] given (ii). For d6 and d7: W6 = E6 - A2 - E2 -
S1(E5) - IF(E5, E4, E3) - K6 and W7 = E7 - A3 - E3 - S1(E6) - IF(E6, E5, E4) - K7, where E2 and E3 carry no member
difference. So d6 = d(E6) is unchanged. d7 = d(E7) - d(S1(E6)) - d(IF(E6, E5, E4)). E6 differs only in bits 31..29,
where IF selects E5[31..29] = 111 for x and E4[31..29] for y, so (i) keeps d7. Rows 14 and 15 depend on rows
10..13 and (W14, W15) only, so L* and the row-16 differences are unchanged. []

The three conditions select an affine set of W8'x in the interval (C8X - 2^29, C8X], so E4' in [1a3a7d30, 1fffffff].
An exhaustive loop over all 2^29 values of E4' (condition (i)) finds 96,830,160 with (ii) and **12,103,680** with
(ii) and (iii) (`enum_e4.c`, Appendix A). The published E4 = 1b2d044e is among them.

**The set V used by the algorithm (K = 2^18).** For j in [0, 2^18), let t = (j * 9E3779B1) mod 2^23 (a bijection on
residues since the multiplier is odd). Deposit t's bits into the 23 positions {0, 2..7, 9..13, 15..25} of
w = bc000000, then set w[1] = NOT w[12], w[8] = NOT w[25] and w[14] = w[18]. W8'x(j) = w and E4'(j) = C8X - w.
All 2^18 values are distinct and satisfy (i) to (iii) (checked exhaustively; E4'(j) in [1a3a7e73, 1e3a7c2d]).
`Setup.variant` in `experiments/v37.py` is this formula. The odd multiplier scatters A0' across the family. A first
choice that varied only the low 16 bits of W8' gave near-identical W7 high bits within a chaining value; we replaced
it (Section 10.4).

### 4.3 Step 2 for a variant: the filter and the second-block words

**Lemma 1 (triangular bijection; d1 packages, unchanged for S').** For a variant S'_k and a chaining value CV1,
E_i = A_i + A_{i-4} - S0(A_{i-1}) - MAJ(A_{i-1}, A_{i-2}, A_{i-3}) for i = 3, 2, 1, 0 and
W_i = E_i - A_{i-4} - E_{i-4} - S1(E_{i-1}) - IF(E_{i-1}, E_{i-2}, E_{i-3}) - K_i for i = 0..7 connect CV1 to S'_k.
The map CV1 -> (W0, ..., W7) is a bijection of (2^32)^8. W7 depends only on A_{-1}, W6 is -A_{-2} plus a function
of A_{-1}, W5 is -A_{-3} plus a function of (A_{-1}, A_{-2}), and so on. Member y uses W'_i = W_i (i <= 5),
W'_6 = W6 + d6, W'_7 = W7 + d7 and S'_k's y-values of W8..W13. Explicitly

```text
W7 = c7_k - A_{-1},  c7_k = E7 - 2 A3 + S0(A2) + MAJ(A2, A1, A0_k) - S1(E6) - IF(E6, E5, E4_k) - K7
W6 = u_k(A_{-1}) - A_{-2},  u_k(A) = c6 + MAJ(A1, A0_k, A) - IF(E5, E4_k, k3_k + A),
c6 = E6 - 2 A2 + S0(A1) - S1(E5) - K6 = f538a8f7 (independent of k),  k3_k = A3 - S0(A2) - MAJ(A2, A1, A0_k)
```

(S's values A1..A3, E5..E7; A0_k = E4'_k + A0B). For S these give c7 = d296fb78 and k3 = 2d5dc689, as in the d1
packages.

**Exact Step-2 sets.** F_k = {w : s0(w + d_k) - s0(w) = t_k mod 2^32} with t6 = 03c00800 and t7 = 017f8000.
**Lemma 3 (d1 packages).** W6, W7 reach rows >= 16 only through s0(W6) in W21, W6 in W22, s0(W7) in W22 and W7 in W23.
The cells of rows 21..23 therefore need exactly W6 in F6 and W7 in F7. The XOR cells of W6 and W7 themselves need not
hold. |F6| = 287,309,824 and |F7| = 68,157,440 (our exhaustive count). A pair (CV1, k) is **valid** iff W7 in F7
and W6 in F6. For uniform CV1 this has probability p2 = |F6||F7|/2^64 = 2^-9.87960 for every k (Lemma 1).

**Lemma 2 (second-block law; d1 packages, per variant).** For fixed k and uniform CV1 conditioned on validity, (W0..W5)
is uniform on (2^32)^6 and (W6, W7) is uniform on F6 x F7, independently. For each l = (W14, W15) the words
(W16, ..., W21) are a bijective image of (W0, ..., W5) given (W6, W14, W15) (W5 = W21 - s1(W19) - W14 - s0(W6), ...,
W0 = W16 - s1(W14) - W9 - s0(W1)), so they are iid uniform. Hence E16..E21 of member x are iid uniform for every k.

**Lemma V2 (what a variant changes in rows >= 16).** For every k, the joint law of the A, E and W values of both
members in rows 12..22, given a valid CV1 and l, is the same as for S. Rows 12..15 are fixed by Lemma V. W16..W21
follow Lemma 2. W22 = s1(W20) + W15 + s0(W7) + W6 does not involve W8, and neither do the member differences. The
only difference is W8' in W23 = s1(W21) + W16 + s0(W8) + W7 and W24 = s1(W22) + W17 + s0(W9) + W8. Rows 23..36 carry
no A/E cell with a value condition, and W23's difference is fixed by Lemma V(iii). So the only W8'-dependent part of
the success event is W24's cell (`n` at bit 29) together with the sign conditions of s1(W24) that make W26's
difference vanish. In our sampler the full cell check of rows 23..36 agreed with this four-condition W24 predicate on
every one of 2,245,436,631 spot checks (Section 6: the published S and eight random variants per row-22 survivor). The family average of q3 is estimated directly
in Section 6, so H2 covers this W24 dependence; no separate invariance assumption is made.

### 4.4 The freedom set L* and Step 3 (d1 packages)

L* is the set of (W14, W15) for which rows 14 and 15 follow the cells for both members and the expansion
differences of W16.. equal the characteristic's. All 32 elements share W14 = bd1d3f7b (y: b95d377b). Their W15 (x)
values are, in order l = 0..31, `7dd4 | {1680,1681,16a0,16a1,1a80,1a81,1aa0,1aa1,3680,3681,36a0,36a1,3a80,3a81,3aa0,
3aa1}` followed by the same 16 low halves with high half `fdb4`. W15y = W15x - 2^29. Every element passes row 16
with probability exactly 2^-11 (exhaustive over E16, `row16.c`). Elements 0, 2, 16 and 18 never pass row 17 (0 of
300,000 proposals in our sampler; all their SMC replicates die there). The program tests the 28 others; the published pair uses l = 13. By Lemma V, L* is the same for
every variant.

**Lemma 4 (d1 packages).** If every cell of rows 16..36 holds (event F_l), the two second-block outputs are equal,
since rows 33..36 carry no u/n cell and the chaining value is common. Then m = M0 || M1 and m' = M0 || M1' collide:
both are 128 bytes long, so FIPS padding appends the same third block. m != m' since W6 differs. M1 must be a full data
block; a final padded block would fix W14 and W15.

**Early abort.** Two necessary conditions of F_l are checked first. Stage 3a is the 10 x-value bits of E16
(cells, and the `+` bit 4 against E15), where E16 = C16_l + s0(W1) + W0 with a per-l constant C16_l. Its bits
0..30 depend only on X = (s0(W1) + W0) mod 2^31, so a table T3[X] lists the passing l. Stage 3b is the 11 x-value bits
of E17 (9 cells and the `+` bits 24 and 15 against E16), where E17 = A13 + E13 + K17 + S1(E16) + IF(E16, E15_l, E14)
+ s1(W15_l) + W10 + s0(W2) + W1. Given a valid pair, X mod 2^31 and W2 are uniform (Lemma 2), so each l passes 3a
with probability exactly 2^-10 and then 3b with probability exactly 2^-11.

## 5. The algorithm and the counted program

### 5.1 Preprocessing and memory layout (word addresses)

| Region | Contents | Words |
| --- | --- | ---: |
| T6 at [0, 2^34] | T6[w] = 1 iff w < 2^33 and (w mod 2^32) in F6; 0 for other w < 2^33; 2 for 2^33 <= w <= 2^34 | 2^34 + 1 |
| CNT at 2^35 + A, IDX at 2^36 + A | size of bucket A and address of its first entry, A in [0, 2^32) | 2^33 |
| ENTU from 2^40 | buckets in order of A; entry u' = 2^32 + u_k(A), each bucket closed by the sentinel 2^34 | K F7 + 2^32 < 2^45 |
| ENTA at ENTU + 2^47, ENTS at ENTU + 2^48 | parallel arrays A0_k and S0(A0_k) for each entry | 2 (K F7 + 2^32) |
| T3 at 2^50 + X | T3[X] = bit mask of the viable l whose E16 x-cells hold for X, X in [0, 2^31) | 2^31 |

Building them costs, in primitive operations (upper bounds): T6, 40 per word; the F7 list, 25 per candidate w
in [0, 2^32) plus 3 per element; the variant records, 300 per variant; the buckets by counting sort over all (k, w)
with w in F7 (pass 1 counts, prefix sums, pass 2 stores u', A0_k and S0(A0_k)), 45 per pair plus 24 per bucket;
T3, 28 x 6 + 5 per X; program and constants 2^24. Total pre = 805,287,340,539,968 operations = 2^38.148 units.
Every entry (k, A) appears once, since for fixed k each A determines w7 = c7_k - A. Peak memory is dominated by the
three entry arrays: 3 (2^18 x 68,157,440 + 2^32) words = 2^45.61 words = 2^50.61 bytes < 2^51 bytes. The bases
above are spaced for readability. Since every base is an immediate, the regions can be placed contiguously at no
change in operation count, so the address range equals the allocated 2^45.61 words.

### 5.2 The online program (instruction listing)

N first blocks are processed. Registers Ve, Vh, Vr, Vb, Vf count bucket entries, valid pairs, rare paths, set
l-bits and FINAL blocks. The run halts as a failure when any exceeds its cap (Section 8). One instruction per line:
`op dst a b`, where an operand is a register, an immediate or a named constant. `b<cond>` costs 2 and `jmp` costs 1.
`call` costs 1 unit plus 4 operations. The block labels attribute counts; BIT and FINAL are instantiated once per
viable l. Named constants are fixed by S (for example A1MK1 = A1 - K1, A2MS0A1 = A2 - S0(A1), C7C = E7 - 2 A3 + S0(A2)
- S1(E6) - (E6 AND E5) - K7, NE6 = NOT E6, CW1X_l = W9..W13 || W14 || W15_l packed, X1514_l = E15_l XOR E14).
The text below is byte-identical to `LISTING` in `experiments/v37.py`, which the organizer experiment executes and
counts instruction by instruction.

```text
CV  TOP:  rand r0
CV        rand r1
CV        call Y IVW r0 r1
CV        shr a1 Y 224
CV        shr t Y 192
CV        and a2 t M32
CV        shr t Y 160
CV        and a3 t M32
CV        shr t Y 128
CV        and a4 t M32
CV        shr t Y 96
CV        and e1 t M32
CV        shr t Y 64
CV        and e2 t M32
CV        shr t Y 32
CV        and e3 t M32
CV        and e4 Y M32
CV        add q a1 CNT0
CV        ld n q
CV        add Ve Ve n
CV        beq n 0 NEXT
CV        shr x a1 2
CV        shl y a1 30
CV        or u x y
CV        shr x a1 13
CV        shl y a1 19
CV        or v x y
CV        xor u u v
CV        shr x a1 22
CV        shl y a1 10
CV        or v x y
CV        xor u u v
CV        and S0a u M32
CV        and x a1 a2
CV        or y a1 a2
CV        and y a3 y
CV        or MJ1 x y
CV        shr x e1 6
CV        shl y e1 26
CV        or u x y
CV        shr x e1 11
CV        shl y e1 21
CV        or v x y
CV        xor u u v
CV        shr x e1 25
CV        shl y e1 7
CV        or v x y
CV        xor u u v
CV        and S1e u M32
CV        xor x e2 e3
CV        and x e1 x
CV        xor IF1 e3 x
CV        sub G0 0 S0a
CV        sub G0 G0 MJ1
CV        sub G0 G0 e4
CV        sub G0 G0 S1e
CV        sub G0 G0 IF1
CV        sub G0 G0 K0
CV        sub Ec a4 S0a
CV        sub Ec Ec MJ1
CV        xor Xe e1 e2
CV        or Ao a1 a2
CV        and Aa a1 a2
CV        sub C1 A1MK1 e3
CV        add q a1 IDX0
CV        ld p q
ENTRY L:  ld e p
ENTRY     add p p 1
ENTRY     sub w e a2
ENTRY     ld t w
ENTRY     beq t 0 L
HIT       beq t 2 NEXT
HIT       add q p DA0M1
HIT       ld a0 q
HIT       add q p DS0M1
HIT       ld sa0 q
HIT       add W0 a0 G0
HIT       add E0 a0 Ec
HIT       and E0 E0 M32
HIT       shr x E0 6
HIT       shl y E0 26
HIT       or u x y
HIT       shr x E0 11
HIT       shl y E0 21
HIT       or v x y
HIT       xor u u v
HIT       shr x E0 25
HIT       shl y E0 7
HIT       or v x y
HIT       xor S1E0 u v
HIT       and x E0 Xe
HIT       xor IFE e2 x
HIT       and x a0 Ao
HIT       or MJ Aa x
HIT       sub W1 C1 sa0
HIT       sub W1 W1 MJ
HIT       sub W1 W1 S1E0
HIT       sub W1 W1 IFE
HIT       and W1 W1 M32
HIT       shr x W1 7
HIT       shl y W1 25
HIT       or u x y
HIT       shr x W1 18
HIT       shl y W1 14
HIT       or v x y
HIT       xor u u v
HIT       shr x W1 3
HIT       xor s0w u x
HIT       add X0 s0w W0
HIT       and X X0 M31
HIT       add q X T3B
HIT       ld m q
HIT       add Vh Vh 1
HIT       bne m 0 RARE
HIT       jmp L
RARE RARE: add Vr Vr 1
RARE      add E1 a3 A1
RARE      sub E1 E1 sa0
RARE      sub E1 E1 MJ
RARE      and E1 E1 M32
RARE      or x a0 a1
RARE      and x x A1
RARE      and y a0 a1
RARE      or MJ2 x y
RARE      add E2 a2 A2MS0A1
RARE      sub E2 E2 MJ2
RARE      and E2 E2 M32
RARE      shr x E1 6
RARE      shl y E1 26
RARE      or u x y
RARE      shr x E1 11
RARE      shl y E1 21
RARE      or v x y
RARE      xor u u v
RARE      shr x E1 25
RARE      shl y E1 7
RARE      or v x y
RARE      xor S1E1 u v
RARE      xor x E0 e1
RARE      and x E1 x
RARE      xor IFE1 e1 x
RARE      sub W2 E2 a2
RARE      sub W2 W2 e2
RARE      sub W2 W2 S1E1
RARE      sub W2 W2 IFE1
RARE      sub W2 W2 K2
RARE      and W2 W2 M32
RARE      shr x W2 7
RARE      shl y W2 25
RARE      or u x y
RARE      shr x W2 18
RARE      shl y W2 14
RARE      or v x y
RARE      xor u u v
RARE      shr x W2 3
RARE      xor u u x
RARE      add R17 u W1
RARE      @BITS
RARE      jmp L
BIT  B_l: shr x m L_l
BIT       and x x 1
BIT       beq x 0 N_l
BIT       add Vb Vb 1
BIT       add E16 X0 C16_l
BIT       and E16 E16 M32
BIT       add W17 R17 Q17_l
BIT       shr x E16 6
BIT       shl y E16 26
BIT       or u x y
BIT       shr x E16 11
BIT       shl y E16 21
BIT       or v x y
BIT       xor u u v
BIT       shr x E16 25
BIT       shl y E16 7
BIT       or v x y
BIT       xor S1E16 u v
BIT       and x E16 X1514_l
BIT       xor IF2 x E14
BIT       add E17 W17 R17C
BIT       add E17 E17 S1E16
BIT       add E17 E17 IF2
BIT       and E17 E17 M32
BIT       and x E17 F17
BIT       bne x V17 N_l
BIT       xor x E17 E16
BIT       and x x P17
BIT       bne x 0 N_l
FINAL     add Vf Vf 1
FINAL     and x a0 A21O
FINAL     or x x A21A
FINAL     add E3 a1 A3MS0A2
FINAL     sub E3 E3 x
FINAL     and E3 E3 M32
FINAL     sub E4p a0 A0B
FINAL     and E4p E4p M32
FINAL     shr x E2 6
FINAL     shl y E2 26
FINAL     or u x y
FINAL     shr x E2 11
FINAL     shl y E2 21
FINAL     or v x y
FINAL     xor u u v
FINAL     shr x E2 25
FINAL     shl y E2 7
FINAL     or v x y
FINAL     xor S1E2 u v
FINAL     xor x E1 E0
FINAL     and x E2 x
FINAL     xor x E0 x
FINAL     sub W3 E3 a1
FINAL     sub W3 W3 e1
FINAL     sub W3 W3 S1E2
FINAL     sub W3 W3 x
FINAL     sub W3 W3 K3
FINAL     and W3 W3 M32
FINAL     shr x E3 6
FINAL     shl y E3 26
FINAL     or u x y
FINAL     shr x E3 11
FINAL     shl y E3 21
FINAL     or v x y
FINAL     xor u u v
FINAL     shr x E3 25
FINAL     shl y E3 7
FINAL     or v x y
FINAL     xor S1E3 u v
FINAL     xor x E2 E1
FINAL     and x E3 x
FINAL     xor x E1 x
FINAL     sub W4 E4p a0
FINAL     sub W4 W4 E0
FINAL     sub W4 W4 S1E3
FINAL     sub W4 W4 x
FINAL     sub W4 W4 K4
FINAL     and W4 W4 M32
FINAL     shr x E4p 6
FINAL     shl y E4p 26
FINAL     or u x y
FINAL     shr x E4p 11
FINAL     shl y E4p 21
FINAL     or v x y
FINAL     xor u u v
FINAL     shr x E4p 25
FINAL     shl y E4p 7
FINAL     or v x y
FINAL     xor S1E4 u v
FINAL     xor x E3 E2
FINAL     and x E4p x
FINAL     xor x E2 x
FINAL     sub W5 E5MA1K5 E1
FINAL     sub W5 W5 S1E4
FINAL     sub W5 W5 x
FINAL     and W5 W5 M32
FINAL     sub W6 e a2
FINAL     and W6 W6 M32
FINAL     and x a0 A21O
FINAL     or x x A21A
FINAL     and y E4p NE6
FINAL     add W7 C7C x
FINAL     sub W7 W7 y
FINAL     sub W7 W7 a1
FINAL     and W7 W7 M32
FINAL     sub W8x C8X E4p
FINAL     sub W8y C8Y E4p
FINAL     and W0 W0 M32
FINAL     shl x W0 32
FINAL     or x x W1
FINAL     shl x x 32
FINAL     or x x W2
FINAL     shl x x 32
FINAL     or x x W3
FINAL     shl x x 32
FINAL     or x x W4
FINAL     shl x x 32
FINAL     or x x W5
FINAL     shl hx x 64
FINAL     shl y W6 32
FINAL     or y y W7
FINAL     or x0 hx y
FINAL     shl y W8x 224
FINAL     or x1 y CW1X_l
FINAL     add u W6 D6
FINAL     and u u M32
FINAL     add v W7 D7
FINAL     and v v M32
FINAL     shl u u 32
FINAL     or u u v
FINAL     or y0 hx u
FINAL     shl y W8y 224
FINAL     or y1 y CW1Y_l
FINAL     call Zx Y x0 x1
FINAL     call Zy Y y0 y1
FINAL     bne Zx Zy N_l
FINAL     jmp SUCCESS_l
BIT  N_l: nop
CV  NEXT: bgt Ve EMAX HALT
CV        bgt Vh HMAX HALT
CV        bgt Vr RMAX HALT
CV        bgt Vb BMAX HALT
CV        bgt Vf FMAX HALT
CV        add i i 1
CV        blt i N TOP
```

SUCCESS (reached at most once) recomputes both complete digests from the IV (6 target compressions), compares them,
outputs both 128-byte messages and halts. It is charged 6 units + 64 operations.

**Per-block counts (exact, from the listing; checked by the organizer experiment).**

| Block | When | Operations |
| --- | --- | ---: |
| CV | every first block: 2 RAND, call (1 unit + 4), unpack 14, bucket size 3, empty test 2, caps 10, loop 3 | 38 (+1 unit) |
| CV | nonempty bucket: + per-CV constants 43, bucket start 2, and the sentinel iteration (ENTRY 6 + HIT test 2) | 91 (+1 unit) |
| ENTRY | per bucket entry (load, increment, subtract, table load, compare-branch) | 6 |
| HIT | per valid pair (W0, W1, X, T3 lookup, counter, branch, return) | 46 |
| RARE | per valid pair with T3[X] != 0: W2, E1, E2, R17 (42), return (1), 28 bit tests (112) | 155 |
| BIT | per set bit l: E16, W17, E17, the 11-bit test | <= 28 |
| FINAL | per E17 pass: W3..W8, both blocks, two compressions, compare | <= 114 (+2 units) |
| SUCCESS | once | 64 (+6 units) |

The per-entry cost is 6 because W6 in F6 is one table load at address u' - A_{-2} (in [1, 2^33)). The bucket end is
the sentinel, whose table value 2 sends the HIT test to NEXT. Empty buckets skip the loop and the constants.

### 5.3 Correctness

The entries of bucket A_{-1} are exactly the k with W7 = c7_k - A_{-1} in F7, and for them
u' - A_{-2} = 2^32 + W6, so the ENTRY loop stops exactly at the valid pairs (and at the sentinel). The HIT block
computes W0 = A0_k + G0 and W1 = C1 - S0(A0_k) - MAJ(A0_k, A_{-1}, A_{-2}) - S1(E0) - IF(E0, E_{-1}, E_{-2}) with
E0 = A0_k + Ec, which is Lemma 1. Its per-CV constants are G0 = -S0(A_{-1}) - MAJ(A_{-1}, A_{-2}, A_{-3}) - E_{-4}
- S1(E_{-1}) - IF(E_{-1}, E_{-2}, E_{-3}) - K0, Ec = A_{-4} - S0(A_{-1}) - MAJ(A_{-1}, A_{-2}, A_{-3}) and
C1 = A1 - K1 - E_{-3}. RARE computes E1, E2 and W2, and BIT computes E16, W17 and E17 of Section 4.4. FINAL
computes E3, W3, W4, W5 (Lemma 1), W6 = u' - A_{-2}, W7 = c7_k - A_{-1} (C7C + MAJ(A2, A1, A0_k) - (E4' AND NOT E6)
- A_{-1}, using IF(E6, E5, E4') = (E6 AND E5) + (NOT E6 AND E4')) and W8'. It assembles both members' blocks and
compares the two compressions from CV1. Every value is reduced mod 2^32 before it is shifted right or packed, except
where only low bits are used afterwards. The organizer experiment executes this exact listing on real chaining values
and compares every decision (the valid set, W1, X, the l-mask) with a direct implementation of Lemma 1. It also runs
it end to end from the published pair's CV with a bucket holding S: the program reaches FINAL for l = 13 and the two
outputs agree. Finally, it runs the listing from the chaining value of every rebuilt variant collision of
`v37-sfs`, which it finds again (Section 10).

## 6. The Step-3 probability of the variant family (H2)

**Estimand.** q3_V = (1/32) sum over l in L* of (1/K) sum over k in V of Pr[F_l | valid (CV1, k)], where F_l is every
A, E, W cell and `+` pair of rows 16..36 for both members. The algorithm's per-l success for a valid pair is at
least Pr[F_l] (Lemma 4, and the early aborts test only necessary conditions of F_l).

**Estimator (`smc.c`, Appendix A).** Sequential Monte Carlo over the exact second-block law of Lemma 2; the design is
that of the d1 packages and the implementation is ours.
- Rows 16..21: E_i^x is proposed uniformly with its x-value cells and `+` bits fixed (weight 2^-f), and the whole
  row is checked (A, E, W of both members). Then multinomial resampling with NP = 1024 particles and 8, 32, 8, 8, 2, 4
  children per particle.
- Tail: TP = 1024 proposals per particle. W22 is proposed uniformly with its x-value cells fixed, W7 ~ U(F7) is
  drawn, and W6 = W22 - s1(W20) - W15 - s0(W7) is implied, with weight 1{W6 in F6} 2^(32 - f22) / |F6|. Row 22 is
  checked.
- Rows 23..36: the published S gets the full cell check, and the family average uses the W24 predicate averaged over
  all k in V. The predicate is checked against the full cell check for the published S and eight random variants
  per row-22 survivor (nine spot checks each).
- The product of the stage means is unbiased for q3 (standard SMC normalizing-constant estimate).
- Every published-S success is rebuilt (W0..W5 by the inverse expansion, CV1 by inverting steps 7..0) and replayed
  against all 32 elements of L*. Every spot-variant success is rebuilt with its own S' and verified with the
  reference compression.

**Preregistration and result.** Before running, we froze the program hash, V, seed 20261011, parameters and the
rule: per l the mean of 256 replicates; q3_hat the average over l; se from the per-l sample variances;
LB = q3_hat - 2.3263 se; q3_model = 2^(floor(100 log2 LB)/100). All 8,192 replicates are used (1,079 die before the
tail and count as 0; they include all replicates of the four dead elements).

| Quantity | Value |
| --- | --- |
| q3_V hat (variant family) | 2^-73.9924, relative se 0.0037 |
| one-sided 99% lower bound | 2^-74.0050, so q3_model = 2^-74.01 |
| q3 hat for the published S (same replicates) | 2^-73.9914; rho = q3_V/q3_S = 0.9993 |
| published-S successes, replayed over all 32 l | 975,395; another l' succeeds in 0 |
| W24 predicate vs full tail check | 0 disagreements in 2,245,436,631 spot checks (nine per row-22 survivor) |
| spot-variant successes rebuilt as SFS collisions of S'_k and verified | 7,792,827; 0 failures |

**Disclosed earlier and later runs** (same program and rule, NP 1024; none excluded):

| Run | Variant set | Seed | Replicates | TP | Result |
| --- | --- | --- | --- | --- | --- |
| Pilot | evenly spaced 2^16-subset of the 12.1M variants | 1001 | 1,024 | 1024 | q3_V = 2^-74.021, q3_S = 2^-74.033 (relative se 0.011; too small for the rule's 0.01-bit resolution) |
| Full run | structured 2^16 set, superseded (Section 10.4) | 20261009 | 8,192 | 1024 | 2^-73.9876, LB 2^-74.0004 |
| Full run | scattered 2^16 set, superseded by K = 2^18 | 20261010 | 8,192 | 1024 | 2^-73.9821, LB 2^-73.9949 |
| kappa run for variants (after the decisive run) | V | 20261012 | 1,024, NP 512 | 512 | 240,260 rebuilt variant successes, 0 with a second l |

All three full runs pass the rule at 2^-74.01. The pilot's point estimates lie 0.7 and 1.4 of its standard errors
below 2^-74.01, which is consistent with the full runs. Our q3 for S agrees with the preregistered 32-seed estimate
for S of 6c77089c/f09f56e7 (mean 2^-73.9916 including the printed two-bit conditions, bound 2^-74.0074). The
algorithm needs only q3 >= 2^-74.083 (Section 7), 0.078 bits below q3_model.

**kappa.** The union over l in L* for one valid pair is at least (sum over l of Pr[F_l]) (1 - eps), where eps bounds
the overlap. We charge kappa = 255/256. Overlaps were never observed: 0 in 975,395 published-S successes and 0 in
240,260 variant successes. These successes share SMC ancestry, so the iid zero-event bound (4.7e-6) is only
indicative, but the allowance 1/256 is about 800 times larger. A valid pair succeeds with probability at least
p_pair = 32 q3_model kappa = 2^-69.01565.

## 7. Success probability and caps

**Independence across first blocks is exact.** The first blocks M0_t are independent uniform 512-bit strings (two
RAND words each), so the chaining values CV1_t are independent random variables. Everything the program does for
first block t is a deterministic function of CV1_t.

**Chen-Stein.**
- Indicators: for each (t, k) let I_tk = 1[(CV1_t, k) valid and F_l holds for some l]. W = sum I_tk counts
  successful pairs. The run succeeds if W >= 1, no cap overflows and the final verification passes; it does after
  F_l, by Lemma 4.
- Neighbourhoods: B_tk = {(t, k') : k' in V}. I_tk is independent of the I outside B_tk, so b3 = 0, and the
  Arratia-Goldstein-Gordon theorem gives |Pr[W = 0] - e^-mu| <= (b1 + b2)(1 - e^-mu)/mu <= b1 + b2.
- The mean: mu = E[W] >= N K p2 p_pair, by H1 (uniform CV1) and Lemma 1, under which every (t, k) is valid with
  probability p2.
- Upper value of the per-pair success probability: b1 and b2 are upper-bound terms, so they use
  p_up = 32 x 2^-73.95 (about 8 standard errors above the point estimate).
- b1 = sum_tk sum over B_tk of E[I_tk] E[I_tk'] <= N (K p2 p_up)^2 = 2.7e-19.
- b2 = sum_tk sum over k' != k of E[I_tk I_tk'] <= N 2^30 p_up^2 E[n^2] <= N 2^30 p_up^2 K E[n] = 2.7e-7. This uses
  H3 (dependence factor at most 2^30) and the deterministic bound n <= K on the number n of valid pairs per first
  block. The measured E[n^2] = 2^19.90 is 2^6.2 below K E[n].
- Validity is strongly clustered by A_{-1} (72.8% of first blocks have no valid pair; the largest count was 23,694).
  The clustering enters only through E[n^2].

With N = 1,115,062,431,311,676,075, mu = 0.52 (rounding N up), and

Pr[success] >= 1 - e^-0.52 - 2(b1 + b2) - Pr[cap overflow] >= 0.405479 - 6e-7 - 5 e^-128 > 0.4054 >= 0.39.

**Sensitivity.** Success stays >= 0.39 as long as mu >= 0.4943, that is, if the product of the validity rate and q3
is at least 95.06% of the model value (q3 >= 2^-74.083 at the nominal validity rate). H3 could be violated by a
factor up to 2^44 (with the deterministic E[n^2] bound) before the bound drops below 0.39. All three margins exceed the corresponding measured
uncertainties: q3 rel. se 0.37%, validity mean 276.72 +- 4.75 (1.7%), row-16 cross moment 1.001.

**Caps.**
- Every run performs exactly N first blocks unless it succeeds or halts.
- The data-dependent counts are capped by EMAX, HMAX, RMAX and BMAX, set at (1 + 2^-5) times their expectations
  under H1 (3.1% slack), and by FMAX at (1 + 2^-2) times its expectation.
- The expectations per first block are E[entries] = K |F7| / 2^32 = 4160 exactly, E[valid] = K p2 = 278.28125,
  E[RARE] <= E[set bits] = 278.28125 x 28/1024 and E[FINAL] = E[set bits] x 2^-11.
- Measured on 40,000 real first blocks: 4134.4 +- 43.7 entries and 276.72 +- 4.75 valid pairs, both within 0.6 of
  their standard errors of the model and 2% of it.
- The per-first-block counts are independent and bounded (by K, K, K, 28K, 28K). Bernstein's inequality bounds each
  overflow probability by exp(-delta^2 mu_c / (2 R (1 + delta/3))). The smallest exponent is FMAX's: about
  2^-4 x 2^51.9 / 2^23.8 = 2^24 at delta = 2^-2 (BMAX: about 2^29 at delta = 2^-5). Every cap therefore overflows
  with probability <= e^-128.
- The caps are tested after each first block. The work of one block past a cap (at most K entries, valid pairs and
  rare paths, and 28K set bits and FINAL blocks) is added to the ledger as an overshoot term.
- On every run the work is at most the capped totals of Section 8, whatever the coins.

## 8. Ledger (exact)

| Item | Count | Cost each |
| --- | ---: | ---: |
| first blocks N | 1,115,062,431,311,676,075 | 1 unit + 91 ops |
| bucket entries EMAX | 4,783,617,830,327,090,361,750 | 6 ops |
| valid pairs HMAX | 319,997,872,438,872,743,926 | 46 ops |
| rare paths RMAX | 8,749,941,824,500,426,592 | 155 ops |
| set l-bits BMAX | 8,749,941,824,500,426,592 | 28 ops |
| FINAL blocks FMAX | 5,178,706,098,781,029 | 2 units + 114 ops |
| cap overshoot (one first block) | K (6 + 46 + 155) + 28K (28 + 114) ops, 56K units | 1,096,548,352 ops + 14,680,064 units |
| SUCCESS | 1 | 6 units + 64 ops |

Totals:
- online: 1,125,419,843,523,918,203 units + 45,124,909,521,779,986,565,979 ops = 2^63.979964;
- preprocessing (tables): 805,287,340,539,968 ops = 2^38.148 units;
- allowances A_C + A_S + DEV: 2^60 + 2^50 + 2^40 units.

T = A_C + A_S + DEV + pre/C + online = 51,151,824,637,987,505,976,823 / 2644 (exact rational before reduction;
`cert37.py`, Appendix A) = **2^64.068697**, claimed as **64.0687** (rounded up). Preprocessing (allowances and
tables) is 2^60.00141 and is already included in T. The expected cost per first block is 15.85 units: 1 compression,
then 4160 x 6 + 278.28 x 46 operations, then the rare paths. Shares of T: bucket scan 56%, valid pairs 29%, A_C 6%,
first-block compressions 6%, rare paths 3%. With A_C = 2^62, log2 T would be 64.30599.

## 9. Heuristics

- **H1-uniform-chaining-value (score-critical).** For independent uniform M0, the chaining values CV1 = F_37(IV, M0)
  behave as independent uniform 256-bit values for: (a) the validity rate K p2 = 278.28 per first block; (b) the
  bucket-size expectation 4160, on which the caps rest; and (c) the conditional law of Lemma 2 used by q3.
  Independence across first blocks is exact.
  - Evidence: 40,000 real first blocks, with 11,068,722 valid pairs (276.72 +- 4.75 per block) and buckets of
    4134.4 +- 43.7. The row-16 rate is 2^-11.002 per (pair, l) over all 32 elements, against the exact law-of-Lemma-2
    value 2^-11.000. Also the organizer experiment `v37-first-blocks`.
  - Scope: random first blocks, 37 steps. Extrapolation: from 2^15.3 blocks to 2^59.95.
  - Margins: 4.9% in the validity rate, 3.1% in the cap means.
- **H2-step3-probability (score-critical).** q3_V >= 2^-74.01 for the family V, and the l-overlap fraction is at most
  1/256.
  - Evidence: the preregistered SMC of Section 6 (8,192 replicates, 975,395 + 240,260 replayed successes), its
    agreement with the earlier estimate for S, Lemma V2, and the organizer replica `v37-sfs`.
  - Scope: the 28 viable elements of L*, all of V.
  - Extrapolation: the SMC estimates a probability of 2^-74 that cannot be observed directly. The algorithm needs
    2^-74.083.
- **H3-cross-variant-dependence (supporting).** For two distinct variants k != k' valid for the same CV1, the joint
  probability that both pairs succeed is at most 2^30 times the product of the two marginals. It only makes b2
  negligible (2.7e-7).
  - Evidence: across 40,000 first blocks, the within-chaining-value cross moment of row-16 passes between
    different variants is 1.001 times the product. The second blocks of two variants differ in W0..W7 through A0_k,
    which enters every W_i (i <= 7) nonlinearly.
  - Scope: rows 16..36. Limitation: measured only at row 16; deeper events are too rare to sample jointly.
- **H4-advice-allowances (score-critical).** The characteristic, S and L* are advice of < 8 KiB. They are charged as
  in the d1 packages: A_C = 2^60 for the authors' characteristic and SFS-pair search (cost unpublished), A_S = 2^50
  for a Step-1 SAT solve (the paper reports 2^41.3), and DEV = 2^40 for all development (ours: about 7,000
  CPU-seconds, mostly SMC). The variants are derived algebraically from S at no search cost. A_C is 6% of T; if it
  were 2^62, log2 T would be 64.30599.

## 10. Evidence

### 10.1 Exact checks
- The published pair collides from its CV under our compression and the repository verifier, and every cell of
  rows -4..36 holds.
- Lemma V's three conditions were enumerated over all 2^29 candidates: 12,103,680 valid variants. All 2^18 elements
  of V are valid and distinct.
- |F6| and |F7| were counted exhaustively.
- Row 16 holds for exactly 2^21 of the 2^32 values of E16^x, for each of the 32 elements of L* (`row16.c`).
- The listing uses at most 38 live registers (`live.py`).

### 10.2 Real first blocks (`fbtest.c`, Appendix A)
For 40,000 first blocks M0 (uniform; xoshiro256** seeds 17, 27, ..., 167, 2,500 blocks each) and every k in V:
- Bucket sizes: 4134.4 +- 43.7 per block (expected 4160; maximum 50,243).
- Valid pairs: 11,068,722, or 276.72 per block with standard error 4.75 (expected 278.28). E[n^2] = 2^19.90;
  29,110 blocks have none; the maximum is 23,694.
- For every valid pair and every one of the 32 elements of L*, rows -4..15 follow every cell (W6/W7 XOR cells
  excepted, Lemma 3): 354,199,104 checks, 0 failures. This verifies the implementation of Lemma 1 and Lemma V on real
  chaining values. It is not evidence for H1, which these cells do not depend on.
- Row 16 holds with rate 2^-11.002 per (pair, l) over all 32 elements, against the exact 2^-11 of Section 10.1 under
  H1(c).
- Between different variants of the same block, the cross moment of row-16 pass counts is 1.001 times the squared
  mean.

### 10.3 Organizer experiments (`experiments/v37.py`, manifest `experiments/manifest.json`)

**`v37-first-blocks`.**
- Trial 0 runs the listing from the published pair's CV with a bucket holding S and 4,096 elements of V. The
  program must reach FINAL for l = 13 with equal outputs.
- Trials 1..64 draw M0 as the program's two RAND words from SHAKE-256 of the trial seed. They compute CV1 and its
  bucket over the first 2^14 elements of V (time budget), and execute the listing instruction by instruction.
- They compare the trace of every valid pair (A0_k, W1, X, l-mask) with a direct computation. They check the
  per-block operation counts against Section 5.2 exactly (FINAL: 113 or 114 per entry). They check the cells of rows
  -4..15, and row 16, of every valid pair with one l each.
- A trial returns M0 || M1 and M0 || M1' of its first valid pair when every check passed; these are not collisions.
- Our local run on our own seeds took 2.9 s on one core. It checked 1,323 valid pairs with 0 decision mismatches and
  0 cell failures, op counts were exact in all 64 trials, and it found the published pair end to end.

**`v37-sfs`.**
- Trials 0..9 run a reduced replicate of the Section 6 estimator (NP 64, 384 tail proposals per particle) for
  l = VIABLE[11 t mod 28]. Each tail proposal uses a fresh random variant of V. W7 is drawn exactly uniformly from F7
  as the disjoint union of its two affine parts (2^26 and 2^20 words; both descriptions are checked at setup).
- Every success is rebuilt into CV1 and both second blocks. It is accepted only if the two 37-step compressions from
  CV1 agree, M1 != M1' and every cell of rows -4..36 holds.
- Up to two per trial are then given to the counted program from CV1. Attempts and successes are both reported.
- A trial returns CV1 || M1 and CV1 || M1' (96 bytes each): a semi-free-start collision, not a collision from the IV.
- Our local runs on four of our own seeds took 1.8 to 2.4 s and each verified 18 to 21 collisions of as many distinct
  variants. Every refind attempt succeeded (9 to 14 per run).

These experiments are deterministic regression checks of the program and of the variant family. They do not test
the magnitude of q3 or of the validity rate with statistical power; those rest on Sections 6 and 10.2.

### 10.4 Disclosed course corrections
- **Variant set.** A first variant set deposited a 16-bit index into W8's low bits. Validity became nearly
  all-or-nothing per chaining value, because the variants' c7_k shared their high bits and their second blocks
  differed only in low bits. We replaced it by the scattered set, then raised K from 2^16 to 2^18. Each set got its
  own full run (Section 6).
- **Listing bugs.** Two bugs were found by the end-to-end test before submission: E16 used the 31-bit table index
  instead of the full 32-bit sum, and E4' was not reduced mod 2^32 before its rotation. Both are fixed in the
  listing above and covered by the experiment.
- **Changes after advisory review.** Four read-only critics, one per review role, reviewed an earlier version of this
  package. On their findings we:
  - raised mu from 0.50 to 0.52 and the cap slack from 2^-16 to 2^-5 (together +0.092 bits);
  - added the cap-overshoot term;
  - bounded b1 and b2 with an upper value of p_pair and the deterministic E[n^2] <= K E[n], and lowered H3's factor
    to 2^30;
  - reclassified H4 as score-critical;
  - measured kappa on variant successes and the bucket-size mean;
  - corrected the statement about the four dead elements (they die at row 17, not 16);
  - added the header generator and the liveness check;
  - shortened `v37-sfs` for the time limit.
- **Changes after a second advisory review.** The second review found no fatal defect. In response we:
  - replaced the rejection sampling of W7 in `v37-sfs` by an exact affine draw (several times faster);
  - fixed the experiment's op-count check for trials that reach FINAL;
  - required l = 13 in the end-to-end test;
  - corrected wording (spot checks, standard errors, Bernstein exponents, rows where elements die).

## 11. Memory and advice

Peak memory is 2^50.61 bytes < 2^51 bytes, almost all of it the three bucket-entry arrays. It also covers T6 (2^39 bytes),
CNT/IDX (2^38 bytes), T3 (2^36 bytes), the F7 list, the variant records, code and constants. It is a theoretical
RAM size and feasibility on existing hardware is not asserted. Nonuniform advice is the characteristic, S, L* and
the constants of the listing: < 8 KiB, so 2^13 bytes. Its construction is charged by H4.

## 12. Limitations

- H1, H2 and H4 are premises. The full-scale success probability cannot be observed; no collision of the target has
  been found by us, and none is expected at the scale we can run.
- q3 rests on an SMC estimate, rows 16..22 of which do not depend on the variant (Lemma V2); the W24 dependence is
  averaged over V inside the estimate. The 99% bound uses a normal approximation over 256 replicates per l.
- H3 is only tested at row 16; its allowance (2^30) is far above the measured 1.001.
- The paper's characteristic search and SFS-pair search are charged by allowance (A_C = 2^60) because their cost is
  unpublished.
- The organizer experiments are regression checks with little statistical power; the quantitative evidence comes from
  our local runs, whose sources and generators are in Appendix A.

## Appendix A. Local tools (not executed by the organizer)

### cert37.py (exact ledger of Section 8; sha256 15a5d7b7b4a00cc4)

```python
#!/usr/bin/env python3
"""cert37.py - exact ledger of the variant-family package (proof.md Section 8).  Exact rationals throughout,
except q3_model = 2^-74.01 which enters only through a rational lower bound Q3 <= 2^-74.01."""
from fractions import Fraction as Fr
import math, json

C = 2644                      # reference_operation_costs["sha256-r37"]
K = 1 << 18                   # |V|
F7, F6 = 68157440, 287309824  # exhaustive sizes
L_VIABLE = 28                 # elements of L* that can pass row 17 (0, 2, 16, 18 never do)
p2 = Fr(F7 * F6, 1 << 64)
e_ent = Fr(K * F7, 1 << 32)   # expected bucket size per CV (exactly 4160)
e_hit = K * p2                # expected valid pairs per CV
e_rare = e_hit * Fr(L_VIABLE, 1024)   # >= E[#RARE] and = E[#set bits]
e_fin = e_rare * Fr(1, 2048)          # E[#FINAL]
# q3_model = 2^-74.01, rational lower bound with 2^-110 resolution
Q3 = Fr(math.floor(2 ** (110 - 74.01)), 1 << 110)
assert Q3 <= Fr(2) ** -74 and float(Q3) <= 2 ** -74.01
kappa = Fr(255, 256)
p_pair = 32 * Q3 * kappa      # lower bound on Pr[some l succeeds | valid pair]
mu_cv = e_hit * p_pair
MU = Fr(52, 100)                     # target mean number of successful pairs (slack over the 0.4943 needed)
N = math.ceil(MU / mu_cv)            # first blocks: mu = N * mu_cv >= 0.52
mu = N * mu_cv
# per-item operation counts of the counted program (proof.md Section 5)
OPS = dict(cv=91, entry=6, hit=46, rare=155, bit=28, final=114, success=64)
UNITS = dict(cv=1, final=2, success=6)
d_main, d_fin = Fr(1, 1 << 5), Fr(1, 1 << 2)   # caps 3.1% / 25% above the H1 expectations
EMAX = math.ceil((1 + d_main) * N * e_ent)
HMAX = math.ceil((1 + d_main) * N * e_hit)
RMAX = math.ceil((1 + d_main) * N * e_rare)
BMAX = RMAX
FMAX = math.ceil((1 + d_fin) * N * e_fin)
# preprocessing (proof.md Section 8.1), in primitive operations
pre_T6 = 40 * ((1 << 34) + 1)
pre_var = 300 * K
pre_F7 = 25 * (1 << 32) + 3 * F7
pre_tab = 45 * K * F7 + 24 * ((1 << 32) + 1)
pre_T3 = (28 * 6 + 5) * (1 << 31)
pre_misc = 1 << 24
pre_ops = pre_T6 + pre_var + pre_F7 + pre_tab + pre_T3 + pre_misc
A_C, A_S, DEV = 1 << 60, 1 << 50, 1 << 40
online_ops = (N * OPS["cv"] + EMAX * OPS["entry"] + HMAX * OPS["hit"] + RMAX * OPS["rare"] + BMAX * OPS["bit"]
              + FMAX * OPS["final"] + OPS["success"])
online_units = N * UNITS["cv"] + FMAX * UNITS["final"] + UNITS["success"]
# caps are tested after each first block: one block can overshoot each cap by its own maximal work
ov_ops = K * (OPS["entry"] + OPS["hit"] + OPS["rare"]) + 28 * K * (OPS["bit"] + OPS["final"])
ov_units = 28 * K * UNITS["final"]
online_ops += ov_ops
online_units += ov_units
T = A_C + A_S + DEV + Fr(pre_ops, C) + online_units + Fr(online_ops, C)
P = A_C + A_S + DEV + Fr(pre_ops, C)
log2T = math.log2(T.numerator) - math.log2(T.denominator)
claim = math.ceil(log2T * 1e5) / 1e5
succ = 1 - math.exp(-float(mu))
# Chen-Stein terms (proof.md Section 7) use an upper value of the per-pair success probability
p_up = 32 * 2.0 ** -73.95             # q3 upper value (point estimate 2^-73.9924 plus about 8 se)
En2 = (1 << 18) * float(e_hit)         # E[n^2] <= K E[n] since n <= K (measured 2^19.90)
b1 = N * float(e_hit) ** 2 * p_up ** 2
b2 = N * 2.0 ** 30 * p_up ** 2 * En2   # H3: dependence factor at most 2^30
out = {
    "p2_log2": math.log2(float(p2)), "valid_pairs_per_cv": float(e_hit), "bucket_mean": float(e_ent),
    "N": N, "log2N": math.log2(N), "mu": float(mu), "1-exp(-mu)": succ, "b1": b1, "b2": b2,
    "EMAX": EMAX, "HMAX": HMAX, "RMAX": RMAX, "BMAX": BMAX, "FMAX": FMAX,
    "pre_ops": pre_ops, "pre_units_log2": math.log2(pre_ops / C),
    "online_units": online_units, "online_ops": online_ops, "overshoot_ops": ov_ops, "overshoot_units": ov_units,
    "online_log2": math.log2(online_units + online_ops / C),
    "T_num": T.numerator, "T_den": T.denominator, "log2T": log2T, "claim_time_log2": claim,
    "preprocessing_log2": math.ceil(math.log2(float(P)) * 1e5) / 1e5,
    "per_cv_expected_units": float(1 + (OPS["cv"] + OPS["entry"] * e_ent + OPS["hit"] * e_hit
                                      + (OPS["rare"] + OPS["bit"]) * e_rare + OPS["final"] * e_fin) / C + 2 * e_fin),
}
print(json.dumps(out, indent=1))
out["success_lower_bound"] = succ - 2 * (b1 + b2) - 5 * math.exp(-128)
print(json.dumps({k: out[k] for k in ("success_lower_bound",)}))
assert out["success_lower_bound"] > 0.40
```

### gen_headers.py (writes consts.h, consts2.h and V18.bin for the C tools from experiments/v37.py alone; its output is byte-identical to the headers our runs used; sha256 fb7bf0f59e424b6e)

```python
#!/usr/bin/env python3
"""gen_headers.py - writes consts.h, consts2.h and V18.bin for smc.c / fbtest.c from experiments/v37.py alone.
usage: PYTHONPATH=experiments python3 gen_headers.py"""
import array
from v37 import Setup, CM, PLUS, KC, IV, LW15, W14X, W14Y, M, S1, s1, IF, steps, expand, PCV
St = Setup()
out = ["static const uint32_t CM[37][3][5] = {"]
for i in range(37):
    out.append("{" + ",".join("{" + ",".join(f"0x{m:08x}u" for m in CM[i][j]) + "}" for j in range(3)) + "},")
out.append("};")
P = sorted(PLUS)
out.append(f"#define NPLUS {len(P)}")
out.append("static const int PLUS[NPLUS][2] = {" + ",".join(f"{{{r},{b}}}" for r, b in P) + "};")
out.append("static const uint32_t KK[37] = {" + ",".join(f"0x{k:08x}u" for k in KC[:37]) + "};")
out.append("typedef struct { uint32_t Ax[4], Ex[4], Ay[4], Ey[4], wx[16], wy[16], dW[6], dW22; } base_t;")
out.append("static const base_t BASES[32] = {")
T6, T7, D6 = 0x03c00800, 0x017f8000, 0x20000000
for l in range(32):
    wx = list(St.Wx[:14]) + [W14X, LW15[l]]
    wy = list(St.Wy[:14]) + [W14Y, (LW15[l] - (1 << 29)) & M]
    Ax, Ex = steps(PCV, expand(wx, 16), 16)
    Ay, Ey = steps(PCV, expand(wy, 16), 16)
    dW = [(s1(wy[14]) - s1(wx[14]) + wy[9] - wx[9]) & M, (s1(wy[15]) - s1(wx[15]) + wy[10] - wx[10]) & M, 0, 0, 0,
          (wy[14] - wx[14] + T6) & M]
    dW22 = (wy[15] - wx[15] + T7 + D6) & M
    f = lambda d: ",".join(f"0x{d[i]:08x}u" for i in range(12, 16))
    out.append("{{" + f(Ax) + "},{" + f(Ex) + "},{" + f(Ay) + "},{" + f(Ey) + "},{" + ",".join(f"0x{w:08x}u" for w in wx)
               + "},{" + ",".join(f"0x{w:08x}u" for w in wy) + "},{" + ",".join(f"0x{v:08x}u" for v in dW) + f"}},0x{dW22:08x}u}},")
out.append("};")
out.append(f"#define W8XPUB 0x{St.Wx[8]:08x}u\n#define W8YPUB 0x{St.Wy[8]:08x}u\n#define C8X 0x{St.C8X:08x}u\n#define C8Y 0x{St.C8Y:08x}u")
out.append("static const uint32_t SAX[14] = {" + ",".join(f"0x{St.Ax[i]:08x}u" for i in range(14)) + "};")
out.append("static const uint32_t SEX[14] = {" + ",".join(f"0x{St.Ex[i]:08x}u" for i in range(14)) + "};")
open("consts.h", "w").write("\n".join(out) + "\n")
ex = ["static const uint32_t SAY[14] = {" + ",".join(f"0x{St.Ay[i]:08x}u" for i in range(14)) + "};",
      "static const uint32_t SEY[14] = {" + ",".join(f"0x{St.Ey[i]:08x}u" for i in range(14)) + "};",
      f"#define A0BASE 0x{St.A0B:08x}u",
      "static const uint32_t IV[8] = {" + ",".join(f"0x{v:08x}u" for v in IV) + "};"]
open("consts2.h", "w").write("\n".join(ex) + "\n")
open("V18.bin", "wb").write(array.array("I", [St.variant(j) for j in range(1 << 18)]).tobytes())
```

### enum_e4.c (Lemma V count over all 2^29 candidates; s1const.h defines C8X da3a7d2f, C8Y ba3a7d2f, T8 043ff800, E4PUB 1b2d044e; sha256 1ea319257a71017f)

```c
#include <stdio.h>
#include <stdint.h>
#include "s1const.h"
#define ROR(x,n) (((x) >> (n)) | ((x) << (32 - (n))))
#define s0(x) (ROR(x,7) ^ ROR(x,18) ^ ((x) >> 3))
int main(void) {
  uint64_t n_cell = 0, n_exact = 0; int pub_ok = 0;
  FILE *f = fopen("e4_valid.bin", "wb");
  for (uint32_t e4 = 0; e4 < (1u << 29); e4++) {
    uint32_t wx = C8X - e4, wy = C8Y - e4;
    if ((wx ^ wy) != 0x20000000u || !((wx >> 29) & 1)) continue;   /* W8 cell ==u===... */
    n_cell++;
    if ((uint32_t)(s0(wy) - s0(wx)) != T8) continue;                 /* exact sigma0 difference */
    n_exact++; fwrite(&e4, 4, 1, f);
    if (e4 == E4PUB) pub_ok = 1;
  }
  fclose(f);
  printf("E4 top3=000: 2^29; W8 cell ok: %llu; + exact s0 diff: %llu (pub included: %d)\n",
         (unsigned long long)n_cell, (unsigned long long)n_exact, pub_ok);
  return 0;
}
```

### fcount.c (exhaustive |F6|, |F7|; sha256 6477a40f105efcda)

```c
#include <stdio.h>
#include <stdint.h>
#define ROR(x,n) (((x) >> (n)) | ((x) << (32 - (n))))
#define s0(x) (ROR(x,7) ^ ROR(x,18) ^ ((x) >> 3))
int main(void) {
  uint64_t f6 = 0, f7 = 0, f6a = 0, f7a = 0;
  uint32_t w = 0;
  do {
    if ((uint32_t)(s0(w + 0x20000000u) - s0(w)) == 0x03c00800u) { f6++; if (!((w >> 29) & 1)) f6a++; }
    if ((uint32_t)(s0(w + 0xfbc00800u) - s0(w)) == 0x017f8000u) { f7++; if ((w & 0x04400800u) == 0x04400000u) f7a++; }
  } while (++w);
  printf("|F6| = %llu (w29=0 part %llu)  |F7| = %llu (w26=w22=1,w11=0 part %llu)\n",
         (unsigned long long)f6, (unsigned long long)f6a, (unsigned long long)f7, (unsigned long long)f7a);
  return 0;
}
```

### row16.c (exact row-16 probability per element of L* (Section 10.1); sha256 69995d1f0fbf976a)

```c
/* row16.c - exact Pr[row 16 holds] per l in L*: all 2^22 E16^x values with the 10 x-fixed bits set (the other
 * 2^32 - 2^22 values fail a fixed x-cell), each checked for every A, E, W cell of row 16 and the '+' bit. */
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include "consts.h"
#define ROR(x,n) (((x) >> (n)) | ((x) << (32 - (n))))
#define BS0(x) (ROR(x,2) ^ ROR(x,13) ^ ROR(x,22))
#define BS1(x) (ROR(x,6) ^ ROR(x,11) ^ ROR(x,25))
#define IFF(x,y,z) (((x) & (y)) ^ (~(x) & (z)))
#define MAJ(x,y,z) (((x) & (y)) ^ ((x) & (z)) ^ ((y) & (z)))
static inline int cell(int i, int j, uint32_t x, uint32_t y) { const uint32_t *m = CM[i][j];
  if ((x ^ y) & m[0]) return 0; if ((x & m[1]) != m[1] || (y & m[1])) return 0;
  if ((x & m[2]) || (y & m[2]) != m[2]) return 0; if ((x | y) & m[3]) return 0; if ((x & y & m[4]) != m[4]) return 0; return 1; }
int main(void) {
  double tot = 0; const uint32_t *m = CM[16][1];
  uint32_t fix = m[1] | m[2] | m[3] | m[4] | (1u << 4), val = m[1] | m[4];
  uint32_t freem = ~fix; int nf = 32 - __builtin_popcount(fix);
  for (int l = 0; l < 32; l++) {
    const base_t *B = &BASES[l];
    /* rows 12..15 at index 0..3 */
    uint32_t v = val | (B->Ex[3] & (1u << 4)), cnt = 0;
    for (uint64_t c = 0; c < (1ull << nf); c++) {
      uint32_t ex = v, t = (uint32_t)c, mm = freem;   /* deposit c into the free bits */
      for (int b = 0; b < 32; b++) if (mm >> b & 1) { ex |= (t & 1) << b; t >>= 1; }
      uint32_t wx = ex - (B->Ax[0] + B->Ex[0] + BS1(B->Ex[3]) + IFF(B->Ex[3], B->Ex[2], B->Ex[1]) + KK[16]);
      uint32_t wy = wx + B->dW[0];
      uint32_t ey = B->Ay[0] + B->Ey[0] + BS1(B->Ey[3]) + IFF(B->Ey[3], B->Ey[2], B->Ey[1]) + KK[16] + wy;
      uint32_t ax = ex - B->Ax[0] + BS0(B->Ax[3]) + MAJ(B->Ax[3], B->Ax[2], B->Ax[1]);
      uint32_t ay = ey - B->Ay[0] + BS0(B->Ay[3]) + MAJ(B->Ay[3], B->Ay[2], B->Ay[1]);
      if (cell(16, 0, ax, ay) && cell(16, 1, ex, ey) && cell(16, 2, wx, wy)) cnt++;
    }
    double p = cnt / 4294967296.0; tot += p;
    printf("l %2d passes %7u  Pr = 2^%.4f\n", l, cnt, cnt ? __builtin_log2(p) : -999.0);
  }
  printf("average over 32 l: 2^%.4f; over the 28 viable: 2^%.4f\n", __builtin_log2(tot / 32), __builtin_log2(tot / 28));
  return 0;
}
```

### fbtest.c (Section 10.2; run as fbtest <seed> 2500 V18.bin for seeds 17, 27, ..., 167; sha256 afb307332adfa116)

```c
/* fbtest.c - real first blocks: bucket sizes and valid (CV1, k) pairs over V, cells of rows -4..15 for all 32 l,
 * row 16, and within-CV dependence of row-16 outcomes across variants.  usage: fbtest seed nCV V18.bin
 * output per CV: n_valid, row-16 passes (sum over pairs and l), sum of squared per-pair passes, bucket size */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "consts.h"
#include "consts2.h"
#define ROR(x,n) (((x) >> (n)) | ((x) << (32 - (n))))
#define BS0(x) (ROR(x,2) ^ ROR(x,13) ^ ROR(x,22))
#define BS1(x) (ROR(x,6) ^ ROR(x,11) ^ ROR(x,25))
#define ss0(x) (ROR(x,7) ^ ROR(x,18) ^ ((x) >> 3))
#define ss1(x) (ROR(x,17) ^ ROR(x,19) ^ ((x) >> 10))
#define IFF(x,y,z) (((x) & (y)) ^ (~(x) & (z)))
#define MAJ(x,y,z) (((x) & (y)) ^ ((x) & (z)) ^ ((y) & (z)))
#define D6 0x20000000u
#define D7 0xfbc00800u
#define T6 0x03c00800u
#define T7 0x017f8000u
static uint64_t rs[4];
static inline uint64_t rotl(uint64_t x, int k) { return (x << k) | (x >> (64 - k)); }
static inline uint64_t rnd64(void) { uint64_t r = rotl(rs[1] * 5, 7) * 9, t = rs[1] << 17;
  rs[2] ^= rs[0]; rs[3] ^= rs[1]; rs[1] ^= rs[2]; rs[0] ^= rs[3]; rs[2] ^= t; rs[3] = rotl(rs[3], 45); return r; }
static void seed_rng(uint64_t s) { for (int i = 0; i < 4; i++) { s += 0x9e3779b97f4a7c15ull; uint64_t z = s;
  z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9ull; z = (z ^ (z >> 27)) * 0x94d049bb133111ebull; rs[i] = z ^ (z >> 31); } }
static inline int inF(uint32_t w, uint32_t d, uint32_t t) { return (uint32_t)(ss0(w + d) - ss0(w)) == t; }
static inline int cell(int i, int j, uint32_t x, uint32_t y) { const uint32_t *m = CM[i][j];
  if ((x ^ y) & m[0]) return 0; if ((x & m[1]) != m[1] || (y & m[1])) return 0;
  if ((x & m[2]) || (y & m[2]) != m[2]) return 0; if ((x | y) & m[3]) return 0; if ((x & y & m[4]) != m[4]) return 0; return 1; }
static void compress37(const uint32_t cv[8], const uint32_t w16[16], uint32_t out[8]) {
  uint32_t W[37]; for (int i = 0; i < 16; i++) W[i] = w16[i];
  for (int i = 16; i < 37; i++) W[i] = ss1(W[i-2]) + W[i-7] + ss0(W[i-15]) + W[i-16];
  uint32_t A[41], E[41]; for (int i = 0; i < 4; i++) { A[3 - i] = cv[i]; E[3 - i] = cv[4 + i]; }
  for (int i = 0; i < 37; i++) { E[i+4] = A[i] + E[i] + BS1(E[i+3]) + IFF(E[i+3], E[i+2], E[i+1]) + KK[i] + W[i];
    A[i+4] = E[i+4] - A[i] + BS0(A[i+3]) + MAJ(A[i+3], A[i+2], A[i+1]); }
  for (int i = 0; i < 4; i++) { out[i] = cv[i] + A[40 - i]; out[4 + i] = cv[4 + i] + E[40 - i]; }
}
/* run steps 0..16 for both members, check cells rows -4..15 (skip W6/W7 cells) and row 16 */
static int rows(const uint32_t cv[8], const uint32_t *wx, const uint32_t *wy, int *r16) {
  uint32_t A[2][21], E[2][21], W[2][17];
  for (int m = 0; m < 2; m++) {
    const uint32_t *w = m ? wy : wx;
    for (int i = 0; i < 16; i++) W[m][i] = w[i];
    W[m][16] = ss1(w[14]) + w[9] + ss0(w[1]) + w[0];
    for (int i = 0; i < 4; i++) { A[m][3 - i] = cv[i]; E[m][3 - i] = cv[4 + i]; }
    for (int i = 0; i < 17; i++) { E[m][i+4] = A[m][i] + E[m][i] + BS1(E[m][i+3]) + IFF(E[m][i+3], E[m][i+2], E[m][i+1]) + KK[i] + W[m][i];
      A[m][i+4] = E[m][i+4] - A[m][i] + BS0(A[m][i+3]) + MAJ(A[m][i+3], A[m][i+2], A[m][i+1]); }
  }
  int bad = 0;
  for (int i = 0; i <= 16; i++) {
    int ok = cell(i, 0, A[0][i+4], A[1][i+4]) && cell(i, 1, E[0][i+4], E[1][i+4]) && (i == 6 || i == 7 || cell(i, 2, W[0][i], W[1][i]));
    for (int p = 0; p < NPLUS; p++) if (PLUS[p][0] + 1 == i && (((E[0][PLUS[p][0] + 4] ^ E[0][i + 4]) >> PLUS[p][1]) & 1)) ok = 0;
    if (i < 16 && !ok) bad = 1;
    if (i == 16) *r16 = ok;
  }
  return bad;
}
int main(int argc, char **argv) {
  uint64_t seed = strtoull(argv[1], 0, 10); long ncv = atol(argv[2]);
  FILE *f = fopen(argv[3], "rb"); static uint32_t V[1 << 18]; int Kv = (int)fread(V, 4, 1 << 18, f); fclose(f);
  seed_rng(seed);
  long tot_valid = 0, mism = 0, tot_c = 0; double s_cc = 0, s_c2 = 0, s_n = 0, s_S2 = 0, s_dev2 = 0;
  for (long t = 0; t < ncv; t++) {
    uint32_t m0[16], cv[8];
    for (int i = 0; i < 16; i += 2) { uint64_t r = rnd64(); m0[i] = (uint32_t)r; m0[i+1] = (uint32_t)(r >> 32); }
    compress37(IV, m0, cv);
    long nvalid = 0, S = 0, Sc2 = 0, nent = 0;
    for (int k = 0; k < Kv; k++) {
      uint32_t A[12], E[12];   /* rows -4..7 at i+4 */
      for (int i = 0; i < 4; i++) { A[3 - i] = cv[i]; E[3 - i] = cv[4 + i]; }
      A[4] = V[k] + A0BASE; A[5] = SAX[1]; A[6] = SAX[2]; A[7] = SAX[3];
      E[8] = V[k]; E[9] = SEX[5]; E[10] = SEX[6]; E[11] = SEX[7];
      for (int i = 3; i >= 0; i--) E[i+4] = A[i+4] + A[i] - BS0(A[i+3]) - MAJ(A[i+3], A[i+2], A[i+1]);
      uint32_t W[8];
      W[7] = E[11] - A[7] - E[7] - BS1(E[10]) - IFF(E[10], E[9], E[8]) - KK[7];
      if (!inF(W[7], D7, T7)) continue;
      nent++;
      W[6] = E[10] - A[6] - E[6] - BS1(E[9]) - IFF(E[9], E[8], E[7]) - KK[6];
      if (!inF(W[6], D6, T6)) continue;
      for (int i = 0; i < 6; i++) W[i] = E[i+4] - A[i] - E[i] - BS1(E[i+3]) - IFF(E[i+3], E[i+2], E[i+1]) - KK[i];
      nvalid++;
      long c = 0;
      for (int l = 0; l < 32; l++) {
        uint32_t wx[16], wy[16];
        for (int i = 0; i < 8; i++) wx[i] = wy[i] = W[i];
        wy[6] = W[6] + D6; wy[7] = W[7] + D7;
        for (int i = 8; i < 16; i++) { wx[i] = BASES[l].wx[i]; wy[i] = BASES[l].wy[i]; }
        wx[8] = C8X - V[k]; wy[8] = C8Y - V[k];
        int r16 = 0; mism += rows(cv, wx, wy, &r16); c += r16;
      }
      S += c; Sc2 += c * c;
    }
    tot_valid += nvalid; tot_c += S;
    s_n += nvalid; s_S2 += (double)S * S; s_c2 += Sc2; s_cc += (double)S * S - Sc2;  /* cross terms */
    printf("%ld %ld %ld %ld\n", nvalid, S, Sc2, nent);
  }
  fprintf(stderr, "CVs %ld valid pairs %ld (mean %.3f) cell mismatches rows<=15: %ld row16 passes %ld\n",
          ncv, tot_valid, (double)tot_valid / ncv, mism, tot_c);
  return 0;
}
```

### smc.c (Section 6 estimator, replay and rebuild, as frozen by the preregistration (its usage comment predates the final file name: the decisive run read V18.bin); the kappa run for variants used the same program with one added counter: the variant rebuild line became `int vc = replay(&P[j], l, w6x, w7x, V[k], &so); if (so) vver++; else vbad++; if (vc > 1) vmulti++;` and vmulti was printed as a 15th column; sha256 50b25dda08fc3ce5)

```c
/* smc.c - SMC estimate of q3 (rows 16..36 of the 37-step characteristic) for the published S and averaged
 * over a variant set V (S' = S with E4' / A0' changed; only W8 changes in rows >= 8).
 * usage: smc l seed NP reps V16.bin  -> one line per replicate:
 *   l seed rep log2(est_pub) log2(est_V) stage counts..., checks
 * Rows 16..21: proposals fix the x-value cells of E_i (weight 2^-f), resampling after each row.
 * Tail: W22 proposed with its x-value cells fixed, W7 ~ U(F7) by rejection, W6 implied, weight
 * 1{W6 in F6} 2^(32-f22)/|F6|; rows 22..36 checked cell by cell (pub and 8 spot variants);
 * the V-average uses the W24 predicate (D == 2^30 and h(W24x)), cross-checked against the full tail. */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "consts.h"
#include "consts2.h"
#define E4PUBV SEX[4]
#define ROR(x,n) (((x) >> (n)) | ((x) << (32 - (n))))
#define BS0(x) (ROR(x,2) ^ ROR(x,13) ^ ROR(x,22))
#define BS1(x) (ROR(x,6) ^ ROR(x,11) ^ ROR(x,25))
#define ss0(x) (ROR(x,7) ^ ROR(x,18) ^ ((x) >> 3))
#define ss1(x) (ROR(x,17) ^ ROR(x,19) ^ ((x) >> 10))
#define IFF(x,y,z) (((x) & (y)) ^ (~(x) & (z)))
#define MAJ(x,y,z) (((x) & (y)) ^ ((x) & (z)) ^ ((y) & (z)))
#define D6 0x20000000u
#define D7 0xfbc00800u
#define T6 0x03c00800u
#define T7 0x017f8000u
#define NF6 287309824.0

static uint64_t rs[4];
static inline uint64_t rotl(uint64_t x, int k) { return (x << k) | (x >> (64 - k)); }
static inline uint64_t rnd64(void) {
  uint64_t r = rotl(rs[1] * 5, 7) * 9, t = rs[1] << 17;
  rs[2] ^= rs[0]; rs[3] ^= rs[1]; rs[1] ^= rs[2]; rs[0] ^= rs[3]; rs[2] ^= t; rs[3] = rotl(rs[3], 45);
  return r;
}
static inline uint32_t rnd32(void) { return (uint32_t)(rnd64() >> 32); }
static void seed_rng(uint64_t s) {
  for (int i = 0; i < 4; i++) { s += 0x9e3779b97f4a7c15ull; uint64_t z = s;
    z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9ull; z = (z ^ (z >> 27)) * 0x94d049bb133111ebull; rs[i] = z ^ (z >> 31); }
}
static inline int inF(uint32_t w, uint32_t d, uint32_t t) { return (uint32_t)(ss0(w + d) - ss0(w)) == t; }
static inline int cell(int i, int j, uint32_t x, uint32_t y) {
  const uint32_t *m = CM[i][j];
  if ((x ^ y) & m[0]) return 0;
  if ((x & m[1]) != m[1] || (y & m[1])) return 0;
  if ((x & m[2]) || (y & m[2]) != m[2]) return 0;
  if ((x | y) & m[3]) return 0;
  if ((x & y & m[4]) != m[4]) return 0;
  return 1;
}
/* state: index i+4 for rows -4..36 */
typedef struct { uint32_t A[2][41], E[2][41], W[2][37]; } st_t;
#define AX(s,i) (s).A[0][(i)+4]
static int plus_ok(const st_t *s, int i) {
  for (int p = 0; p < NPLUS; p++)
    if (PLUS[p][0] + 1 == i && (((s->E[0][PLUS[p][0] + 4] ^ s->E[0][i + 4]) >> PLUS[p][1]) & 1)) return 0;
  return 1;
}
static inline void step(st_t *s, int m, int i) {
  uint32_t *A = s->A[m] + 4, *E = s->E[m] + 4;
  E[i] = A[i-4] + E[i-4] + BS1(E[i-1]) + IFF(E[i-1], E[i-2], E[i-3]) + KK[i] + s->W[m][i];
  A[i] = E[i] - A[i-4] + BS0(A[i-1]) + MAJ(A[i-1], A[i-2], A[i-3]);
}
static const base_t *B;
static uint32_t REQ26;
static int row_try(const st_t *p, st_t *q, int i, uint32_t ex) {
  const uint32_t *Ax = p->A[0] + 4, *Ex = p->E[0] + 4, *Ay = p->A[1] + 4, *Ey = p->E[1] + 4;
  uint32_t wx = ex - (Ax[i-4] + Ex[i-4] + BS1(Ex[i-1]) + IFF(Ex[i-1], Ex[i-2], Ex[i-3]) + KK[i]);
  uint32_t wy = wx + B->dW[i - 16];
  uint32_t ey = Ay[i-4] + Ey[i-4] + BS1(Ey[i-1]) + IFF(Ey[i-1], Ey[i-2], Ey[i-3]) + KK[i] + wy;
  if (!cell(i, 1, ex, ey) || !cell(i, 2, wx, wy)) return 0;
  uint32_t ax = ex - Ax[i-4] + BS0(Ax[i-1]) + MAJ(Ax[i-1], Ax[i-2], Ax[i-3]);
  uint32_t ay = ey - Ay[i-4] + BS0(Ay[i-1]) + MAJ(Ay[i-1], Ay[i-2], Ay[i-3]);
  if (!cell(i, 0, ax, ay)) return 0;
  *q = *p;
  q->A[0][i+4] = ax; q->E[0][i+4] = ex; q->W[0][i] = wx; q->A[1][i+4] = ay; q->E[1][i+4] = ey; q->W[1][i] = wy;
  if (!plus_ok(q, i)) return 0;
  return 1;
}
/* full tail rows 22..36 for given W6/W7/W8 (x,y); s has rows <= 21 */
static int tail_full(const st_t *p, uint32_t w6x, uint32_t w7x, uint32_t w8x, uint32_t w8y) {
  st_t s = *p;
  s.W[0][6] = w6x; s.W[1][6] = w6x + D6; s.W[0][7] = w7x; s.W[1][7] = w7x + D7;
  s.W[0][8] = w8x; s.W[1][8] = w8y;
  for (int m = 0; m < 2; m++)
    for (int j = 22; j < 37; j++)
      s.W[m][j] = ss1(s.W[m][j-2]) + s.W[m][j-7] + ss0(s.W[m][j-15]) + s.W[m][j-16];
  for (int i = 22; i < 37; i++) {
    step(&s, 0, i); step(&s, 1, i);
    if (!cell(i, 0, s.A[0][i+4], s.A[1][i+4]) || !cell(i, 1, s.E[0][i+4], s.E[1][i+4]) ||
        !cell(i, 2, s.W[0][i], s.W[1][i]) || !plus_ok(&s, i)) return 0;
  }
  return 1;
}
static inline int hpred(uint32_t x) { return !((x >> 29) & 1) && (uint32_t)(ss1(x + 0x20000000u) - ss1(x)) == REQ26; }


static void compress37(const uint32_t cv[8], const uint32_t w16[16], uint32_t out[8]) {
  uint32_t W[37]; for (int i = 0; i < 16; i++) W[i] = w16[i];
  for (int i = 16; i < 37; i++) W[i] = ss1(W[i-2]) + W[i-7] + ss0(W[i-15]) + W[i-16];
  uint32_t A[41], E[41];
  for (int i = 0; i < 4; i++) { A[3 - i] = cv[i]; E[3 - i] = cv[4 + i]; }
  for (int i = 0; i < 37; i++) {
    E[i+4] = A[i] + E[i] + BS1(E[i+3]) + IFF(E[i+3], E[i+2], E[i+1]) + KK[i] + W[i];
    A[i+4] = E[i+4] - A[i] + BS0(A[i+3]) + MAJ(A[i+3], A[i+2], A[i+1]);
  }
  for (int i = 0; i < 4; i++) { out[i] = cv[i] + A[40 - i]; out[4 + i] = cv[4 + i] + E[40 - i]; }
}
/* kappa replay of a published-S success for l: count l' (incl. l) whose second blocks collide from the same CV1 */
static int replay(const st_t *p, int l, uint32_t w6x, uint32_t w7x, uint32_t e4, int *self_ok) {
  uint32_t w8x = C8X - e4, w8y = C8Y - e4;
  uint32_t W[22];
  for (int i = 16; i < 22; i++) W[i] = p->W[0][i];
  W[6] = w6x; W[7] = w7x; W[8] = w8x;
  for (int i = 9; i < 14; i++) W[i] = BASES[l].wx[i];
  W[14] = BASES[l].wx[14]; W[15] = BASES[l].wx[15];
  for (int j = 5; j >= 0; j--) W[j] = W[j+16] - ss1(W[j+14]) - W[j+9] - ss0(W[j+1]);
  uint32_t A[12], E[12];   /* index i+4 for rows -4..7 */
  for (int i = 0; i < 8; i++) { A[i+4] = SAX[i]; if (i >= 4) E[i+4] = SEX[i]; }
  A[4] = e4 + A0BASE; E[8] = e4;
  for (int i = 7; i >= 0; i--) {
    A[i] = E[i+4] - A[i+4] + BS0(A[i+3]) + MAJ(A[i+3], A[i+2], A[i+1]);
    E[i] = E[i+4] - A[i] - BS1(E[i+3]) - IFF(E[i+3], E[i+2], E[i+1]) - KK[i] - W[i];
  }
  uint32_t cv[8] = {A[3], A[2], A[1], A[0], E[3], E[2], E[1], E[0]};
  int cnt = 0;
  for (int lp = 0; lp < 32; lp++) {
    uint32_t mx[16], my[16], hx[8], hy[8];
    for (int i = 0; i < 8; i++) mx[i] = my[i] = W[i];
    my[6] = W[6] + D6; my[7] = W[7] + D7;
    for (int i = 8; i < 16; i++) { mx[i] = BASES[lp].wx[i]; my[i] = BASES[lp].wy[i]; }
    mx[8] = w8x; my[8] = w8y;
    compress37(cv, mx, hx); compress37(cv, my, hy);
    int eq = !memcmp(hx, hy, sizeof hx);
    if (lp == l) *self_ok = eq;
    cnt += eq;
  }
  return cnt;
}

int main(int argc, char **argv) {
  int l = atoi(argv[1]); uint64_t seed = strtoull(argv[2], 0, 10); int NP = atoi(argv[3]), reps = atoi(argv[4]);
  int TP = argc > 6 ? atoi(argv[6]) : 1024;
  FILE *f = fopen(argv[5], "rb"); static uint32_t V[1 << 18]; int Kv = (int)fread(V, 4, 1 << 18, f); fclose(f);
  static uint32_t W8XV[1 << 18]; for (int k = 0; k < Kv; k++) W8XV[k] = C8X - V[k];
  B = &BASES[l];
  REQ26 = -(B->wy[10] - B->wx[10]);
  int children[6] = {8, 32, 8, 8, 2, 4};
  st_t s0; memset(&s0, 0, sizeof s0);
  for (int m = 0; m < 2; m++) {
    for (int i = 0; i < 16; i++) s0.W[m][i] = m ? B->wy[i] : B->wx[i];
    for (int r = 0; r < 4; r++) {
      s0.A[m][12 + r + 4] = m ? B->Ay[r] : B->Ax[r]; s0.E[m][12 + r + 4] = m ? B->Ey[r] : B->Ex[r];
    }
  }
  st_t *P = malloc(sizeof(st_t) * NP), *Q = malloc(sizeof(st_t) * (size_t)NP * 64);
  uint32_t fix22 = CM[22][2][1] | CM[22][2][2] | CM[22][2][3] | CM[22][2][4], val22 = CM[22][2][1] | CM[22][2][4];
  int f22 = __builtin_popcount(fix22);
  for (int rep = 0; rep < reps; rep++) {
    seed_rng(seed * 1000003ull + (uint64_t)rep * 7919ull + (uint64_t)l);
    for (int j = 0; j < NP; j++) P[j] = s0;
    double logest = 0; int dead = 0; long surv_counts[6];
    for (int k = 0; k < 6 && !dead; k++) {
      int i = 16 + k;
      const uint32_t *m = CM[i][1];
      uint32_t fix = m[1] | m[2] | m[3] | m[4], val = m[1] | m[4], plusm = 0;
      for (int p = 0; p < NPLUS; p++) if (PLUS[p][0] + 1 == i) plusm |= 1u << PLUS[p][1];
      int f = __builtin_popcount(fix | plusm);
      long ns = 0, props = 0;
      for (int j = 0; j < NP; j++)
        for (int c = 0; c < children[k]; c++) {
          uint32_t ex = (rnd32() & ~(fix | plusm)) | val;
          ex |= P[j].E[0][i - 1 + 4] & plusm;   /* '+' pairs with the previous row */
          props++;
          if (row_try(&P[j], &Q[ns], i, ex)) ns++;
        }
      surv_counts[k] = ns;
      if (!ns) { dead = 1; break; }
      logest += log2((double)ns / props) - f;
      for (int j = 0; j < NP; j++) P[j] = Q[rnd64() % (uint64_t)ns];
    }
    double tpub = 0, tV = 0; long acc22 = 0, accD = 0, spot_mis = 0, nsucc = 0, multi = 0, selfbad = 0, vver = 0, vbad = 0;
    if (!dead) {
      double wgt = ldexp(1.0, 32 - f22) / NF6;
      for (int j = 0; j < NP; j++)
        for (int t = 0; t < TP; t++) {
          uint32_t w22x = (rnd32() & ~fix22) | val22, w7x;
          do { w7x = rnd32(); } while (!inF(w7x, D7, T7));
          uint32_t w6x = w22x - ss1(P[j].W[0][20]) - B->wx[15] - ss0(w7x);
          if (!inF(w6x, D6, T6)) continue;
          /* row 22 (independent of W8) */
          st_t s = P[j];
          s.W[0][6] = w6x; s.W[1][6] = w6x + D6; s.W[0][7] = w7x; s.W[1][7] = w7x + D7;
          for (int mm = 0; mm < 2; mm++) s.W[mm][22] = ss1(s.W[mm][20]) + s.W[mm][15] + ss0(s.W[mm][7]) + s.W[mm][6];
          step(&s, 0, 22); step(&s, 1, 22);
          int ok22 = cell(22, 0, s.A[0][26], s.A[1][26]) && cell(22, 1, s.E[0][26], s.E[1][26]) &&
                     cell(22, 2, s.W[0][22], s.W[1][22]) && plus_ok(&s, 22);
          int full_pub = ok22 && tail_full(&P[j], w6x, w7x, W8XPUB, W8YPUB);
          if (full_pub) { tpub += wgt; nsucc++; int so = 0; int c = replay(&P[j], l, w6x, w7x, E4PUBV, &so); if (!so) selfbad++; if (c > 1) multi++; }
          if (!ok22) continue;
          acc22++;
          uint32_t Yx = ss1(s.W[0][22]) + s.W[0][17] + ss0(s.W[0][9]);
          uint32_t Yy = ss1(s.W[1][22]) + s.W[1][17] + ss0(s.W[1][9]);
          int Dok = (uint32_t)(Yy - Yx) == 0x40000000u;
          /* predicate vs full tail: published S and 8 spot variants */
          if ((Dok && hpred(Yx + W8XPUB)) != full_pub) spot_mis++;
          for (int q = 0; q < 8; q++) {
            int k = (int)(rnd64() % (uint64_t)Kv);
            int fv = tail_full(&P[j], w6x, w7x, W8XV[k], W8XV[k] - 0x20000000u);
            if ((Dok && hpred(Yx + W8XV[k])) != fv) spot_mis++;
            if (fv) { int so = 0; replay(&P[j], l, w6x, w7x, V[k], &so); if (so) vver++; else vbad++; }
          }
          if (!Dok) continue;
          accD++;
          long cnt = 0;
          for (int k = 0; k < Kv; k++) cnt += hpred(Yx + W8XV[k]);
          tV += wgt * (double)cnt / Kv;
        }
    }
    double denom = (double)NP * TP;
    double lp = dead || tpub == 0 ? -INFINITY : logest + log2(tpub / denom);
    double lv = dead || tV == 0 ? -INFINITY : logest + log2(tV / denom);
    printf("%d %llu %d %.6f %.6f %.6f %ld %ld %ld %ld %ld %ld %ld %ld\n", l, (unsigned long long)seed, rep, dead ? -INFINITY : logest,
           lp, lv, acc22, accD, nsucc, spot_mis, multi, selfbad, vver, vbad);
    fflush(stdout);
  }
  return 0;
}
```

### live.py (register liveness of the listing; sha256 f21020cbca867c9a)

```python
import sys
sys.path.insert(0, "pkg/experiments")
from v37 import Setup, Machine, bucket_for, PCV
St = Setup()
mc = Machine(St, bucket_for(St, PCV[0], [St.Ex[4]]), PCV[0])
prog, lab, sym = mc.prog, mc.lab, mc.sym
def isreg(t): return not (t in sym or t.lstrip("-").isdigit() or t in lab or t.startswith("SUCCESS_"))
uses, defs, succ = [], [], []
for i, (blk, _, tk) in enumerate(prog):
    op = tk[0]; u, d = set(), set()
    if op in ("add", "sub", "and", "or", "xor", "shl", "shr"): d = {tk[1]}; u = {t for t in tk[2:4] if isreg(t)}
    elif op == "ld": d = {tk[1]}; u = {tk[2]} if isreg(tk[2]) else set()
    elif op == "rand": d = {tk[1]}
    elif op == "call": d = {tk[1]}; u = {t for t in tk[2:5] if isreg(t)}
    elif op[0] == "b": u = {t for t in tk[1:3] if isreg(t)}
    nxt = []
    if op == "jmp": nxt = [lab["N_" + tk[1][8:]] if tk[1].startswith("SUCCESS_") else lab[tk[1]]]
    elif op[0] == "b":
        nxt = ([i + 1] if i + 1 < len(prog) else []) + ([] if tk[3] == "HALT" else [lab[tk[3]]])
    else: nxt = [i + 1] if i + 1 < len(prog) else []
    uses.append(u); defs.append(d); succ.append(nxt)
# counters and loop state live across the whole loop
glob = {"Ve", "Vh", "Vr", "Vb", "Vf", "i"}
live_in = [set() for _ in prog]
changed = True
while changed:
    changed = False
    for i in range(len(prog) - 1, -1, -1):
        out = set().union(*[live_in[j] for j in succ[i]]) if succ[i] else set()
        new = uses[i] | (out - defs[i])
        if new != live_in[i]: live_in[i] = new; changed = True
names = set().union(*uses, *defs)
mx = max(len(live_in[i] | defs[i] | glob) for i in range(len(prog)))
print("register names", len(names), "max simultaneously live (incl. counters, loop index)", mx)
```

Data: consts.h sha256 18fa51a72931c2bf, consts2.h sha256 783a7f253d248363, V18.bin sha256 3dd4b6ccd507e5d9 (all three regenerated identically by gen_headers.py).

