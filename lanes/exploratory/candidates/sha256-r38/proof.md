# 38-step SHA-256 collision with the characteristic P8 in the memory-efficient A0-variant attack, 32 classes and invariant-folded carry-save row-16 programs: time 2^86.89079, memory 2^28.10 bytes

**Track** sha256-r38-exploratory, target sha256-r38-prefix-v1, cost model collision-frontier-v5 (C = 2728), scalar policy hashsmash-scalar-tm-v1 (score = time_log2 + max(0, memory_log2_bytes - 20)).
**Claim** time_log2 = 86.89079 (exact total 2^86.890780 target compressions), algorithmic success probability at least 0.39, memory 2^28.10 bytes (online 3,476,064 bytes; the preprocessing peak, Section 11), preprocessing 2^78.09276, non-uniform advice below 2^14 bytes. Score under the scalar policy: 94.99079.

## 0. Summary

This package runs the memory-efficient A0-variant collision attack on 38-step SHA-256 (ePrint 2026/1120 and 2026/1080; the A0-variants, c7 classes, bit-sliced row-16 filter and accepted event with a direct output comparison of the public packages 2d1c4fc2 and fb176310) with **P8**, a characteristic we found ourselves (Section 3). It extends our filing 1a695f0b (same P8, same Step-1 solution S); the changes are listed in Section 0.1. What is new against the published characteristic:

1. **The characteristic P8.** Found by our systematic sign sweep over the 24 message-difference XOR patterns of weight 25 (Section 3.2): XOR pattern 8 (not the published pattern 0), a different dense trail and a different signed message difference. Its printed-event probability (rows 16..37 follow the trail and its derived conditions) is 2^-99.56 against 2^-101.05 for the published characteristic, measured with the same estimator.
2. **The accepted event.** Rows 16..22 of both members follow the trail, except that row 19 is checked on its signed differences only (not on its derived value conditions), and the two outputs after step 37 are compared directly (rows 23..37 untested). All 188,796 estimator successes that were classified fall into four row-19 condition patterns (Section 6.2).
3. **The measured q3 for that event** over the variants of the selected classes: 40 independent runs, mean 2^-96.1821, one-sided 99% Student bound 2^-96.5603 (bootstrap 2^-96.5278); **q3_model = 2^-97.0000**. The corresponding value of fb176310 for the published characteristic is 2^-97.7838.

| | fb176310 (published characteristic) | 1a695f0b (P8, 8 classes) | 08e2e0d3 (P8, 32 classes) | this package (P8, 32 classes) |
|---|---|---|---|---|
| q3_model of the accepted event | 2^-97.7838 | 2^-97.0000 | 2^-97.0000 | 2^-97.0000 |
| selected variants, good pairs per first block | 345,600, 23,118.75 | 196,608, 13,152 | 786,432, 52,608 | 786,432, 52,608 |
| row-16 program per batch of 256 variants | 1,410 to 1,426 instructions | 1,511 instructions (one shared program) | 1,438 to 1,482 instructions (per class; mean 1462.25) | 1,169 to 1,207 instructions (per class; mean 1188.31) |
| time_log2 | 87.90375 | 87.22358 | 87.14808 | **86.89079** |
| memory | 2^28 (online 1,044,992 bytes) | 2^28.10 | 2^28.10 (online 3,659,904 bytes) | 2^28.10 (online 3,476,064 bytes) |
| score (scalar policy) | 95.90375 | 95.32358 | 95.24808 | **94.99079** |

### 0.1 Changes from 1a695f0b and 08e2e0d3

1. **All 32 largest c7 classes (from 08e2e0d3).** 1a695f0b used the 8 classes of mask 7fe96c7c (196,608 variants). 08e2e0d3 and this package use every class of the maximal size 24,576 of P8 (32 classes, 786,432 variants), with 6 different masks: 7feb6c7c (22 bits) x 8, 7fe96c7c (21 bits) x 8, 7feb6c7e (23 bits) x 4, 7fe96c7e (22 bits) x 4, 3feb6c7c (21 bits) x 4, 3fe96c7c (20 bits) x 4. Good pairs per first block: 52,608 (was 13,152).
2. **Carry-save per-class row-16 programs and algebraic invariant folding (new over 08e2e0d3 and 0906b03e).** Each class gets its own bit-sliced row-16 program in which every bit of a0 outside the class's mask is the class's base bit, folded as a constant (Section 7.2; 08be594 and 08e2e0d3). In 08e2e0d3 the 32 programs took 1,438 to 1,482 instructions (mean 1462.25, with 16..20 spill stores); in 0906b03e carry-save column reduction (`reduce_col`), polarity-carrying wires, and absorbing `A0_CONST = 0x380` into `HH, K1, KP` reduced them to 1,179..1,220 (mean 1200.38, 0 spills). Here (`build_e16`, `cbits`, `fb_scalars`, `broadcast` in `experiments/a0p38.py`) we further exploit exact algebraic invariants across all 786,432 variants of the 32 classes: (i) `a0[11] ^ a0[10] = 1` (`a0[10] + 2 a0[11] = 1 + a0[11]`, absorbed into `A0_ADD = 0x780` in `HH` and `KP` with `a0e[10] = a0[11], a0e[11] = 0`), `a0[22] = a0[21]`, `a0[20] = 0` (`AB` bit 20 omitted), and per-class `a0[28] = a0[27] ^ 1` (folded into `E0` bit 27 in classes `ci % 16 in {0,2,4,6}`) or `a0[28] = a0[27]` (in the remaining 24 classes) plus `a0[16] = a0[1] ^ 1` (in classes `ci % 16 in {8,9,10,11}`), eliminating 3 to 4 `a0` plane loads per batch; (ii) pruning `W1` to bits 0..30 (`max(TBITS) + 18 = 30` for `TK = 10`, omitting bit 31 of `EF, FF, K1, AB`), reducing per-first-block scalars from 44 to 39 ops and broadcast planes from 173 (692 ops) to 165 (660 ops). Result: 32 programs, **1,169 to 1,207 instructions, mean 1188.31**, with 0 spill stores across all 32 classes, lowering time_log2 to **86.89079** (score **94.99079**).
3. **The F7 sampler of the organizer replica (from 08e2e0d3 / 08be594).** 1a695f0b sampled W7 in F7 by its three affine families, choosing the family by `(w >> 4) % 274` of the same random word whose bits then formed the value: the family choice was correlated with the value and had a modulo bias. Both were pointed out in 08be594 (johnservil). The replica draws the family by rejection from its own word (9 bits, accepted below 274: shares 256, 16, 2, no bias) and the value bits from a fresh word (`f7_sample`; 200,000 draws: all in F7, family frequencies 93,187 + 93,579 / 11,769 / 1,465 against 186,861 / 11,679 / 1,460 expected). A generic rejection sampler on the definition is kept for other (D7, T7) only, as it is slower.
4. **Deterministic class selection (from 08e2e0d3).** The classes are selected by `lp_classes.py` (ALLMAX=1: every class of the largest size, ordered by c7) from the output of `a0cls.c`, replacing the hand-run selection of 1a695f0b.
5. **Stage-3a tested bits (TK = 10) and canonical-batch lane cost.** Testing the TK = 10 lowest shared bits of R16 (bits 1, 3, 4, 5, 6, 7, 8, 9, 11, 12; `max(TBITS) = 12` instead of 16) avoids computing bits 13..16 of E16x and bit 31 of W1 in every batch while keeping stage-3a lane work small (24,576 x 2^-10 = 24 expected lanes per passing class). Because each class decomposes as 24 high-11-bit prefixes times 1,024 = 4 x 256 low-21-bit solutions (`LV_MASK = 0x1fffff`), bits 21..31 of a0 are constant across all 256 lanes of every canonical batch (`planes['base']`), so `lane_value` recovers only the varying bits in `mk & 0x1fffff` (at most 13 bits: 4 x 13 + 1 = 53 ops) and `scalar_e16` costs 38 ops: 168 operations per stage-3a lane (was 209 in 0906b03e).
6. **q3 re-measured** over the 786,432 variants of the 32 classes (seeds 4001..4040, Section 9, from 08e2e0d3). Memory is unchanged at 2^28.10 (online memory is 3,476,064 bytes; the preprocessing peak is unchanged, Section 11).

## 1. Target and cost model

Target sha256-r38-prefix-v1: SHA-256 steps 0..37 on every padded block, the standard IV once, FIPS 180-4 padding, feed-forward, all eight digest words; output two distinct 128-byte messages M0 || M1 and M0 || M1' with equal digests (the padding block is common). collision-frontier-v5: one target compression = 1 unit, every other word operation of the 256-bit word RAM 1/C, C = 2728; the scalar policy hashsmash-scalar-tm-v1 ranks time_log2 + max(0, memory_log2_bytes - 20).

## 2. Sources, credit, and what is ours

- ePrint 2026/1120 (Li, Zhang, Li, Liu, Qian, Zhu): the 38-step two-block framework and its memory-efficient Step 1-3 procedure, the message-difference shape (W7..W11, W15, W16, W23, W25), the published characteristic (comparison only). ePrint 2026/1080 [LLWS26]: the memory-efficient framework.
- 2d1c4fc2 (itseasypop): A0-variants of the Step-1 solution, the c7 classes decided by one W7 test, the bit-sliced evaluation of the row-16 filter for 256 variants per word, the success analysis with a pair term and work caps. fb176310 (Jbenisek): the accepted event with a direct output comparison and alternative row-19 patterns, lowest-shared-bit stage 3a, the memory-free W7 test, a counted register allocator. We read their packages as documents; we executed none of their code. `experiments/a0p38.py` is our own implementation of that design for P8.
- 08be594 (johnservil): per-class row-16 programs with the class's non-mask bits folded as constants (for the 8 classes of 1a695f0b), and the observation that the F7 sampler of 1a695f0b's replica correlated the family choice with the value and had a modulo bias. Our per-class programs and the corrected sampler are our own implementation (for those 8 classes our per-class counts, [1466, 1457, 1469, 1466, 1463, 1454, 1466, 1463], equal the counts listed in 08be594's submission note).
- 08e2e0d3 (dariolina, base package of this line; extending 1a695f0b, 49b543d1, 242fcec3 and 1db43310): the characteristic P8 and the search that found it (signed-difference SAT model, sign sweep, joint coupling check), the condition derivation and estimators, the accepted event with row 19 on signed differences and its 40-run measurement, the 32-class selection (`lp_classes.py`), the base program `experiments/a0p38.py` and `ledger_a0p.py`. Our prior filing 0906b03e introduced `reduce_col` carry-save column reduction, polarity-carrying wires, `A0_CONST = 0x380` folding, and `TK = 10` (1,179..1,220 instructions, mean 1200.38, `time_log2` = 86.91630; a concurrent derivative fa3a15cc by 2121 adjusted `fb_scalars` and `scalar_e16` to 86.91627). This package extends 0906b03e in `a0p_core.py`, `a0p_prog.py`, `a0p_scal.py`, `a0p_run.py` and `ledger_a0p.py` with algebraic invariant folding across all 32 classes (`a0[11]^a0[10]=1`, `a0[22]=a0[21]`, `a0[20]=0`, `a0[28]=a0[27]^c`, `a0[16]=a0[1]^1`), `W1` pruning to bit 30 (165 broadcast planes / 660 ops, 39 scalar ops), and canonical-batch `LV_MASK = 0x1fffff` lane recovery (168 ops per lane), reducing the 32 per-class programs to 1,169..1,207 (mean 1188.31) instructions and `time_log2` to 86.89079.
- Execution: everything ran in Linux containers on one 10-core machine (OrbStack; Ubuntu 22.04 for the C tools and solvers; the shipped program also on the official python:3.12.12-slim-bookworm image, Section 13).

## 3. The characteristic P8

### 3.1 The trail and a semi-free-start pair

Signed differences (u: member x has 1, member y 0; n: the reverse), most significant bit first, rows -4..37, columns A_i, E_i, W_i (rows without a difference in all three words omitted: -4..6 and 26..37 are all `=`):

```
   6  ================================  ================================  ================================
   7  =nu=============================  uuu=============================  ==n=============================
   8  =========n=====n====n======n====  ==n=u====n==nu=====nu===u==n====  =====u===u==========n===========
   9  ================================  ======nn===n================n=nn  ==u=============================
  10  ===============n===========u====  =u=============n===========u====  =====u=n=======n===u==u=n=u=n=n=
  11  ====n===============n========u==  ==n==n==u=====un================  ============u=======nn==========
  12  ==u====u==u==========uu=======u=  =nu=u==n==n=====u=n=nn=========u  ================================
  13  ==n=============================  =========n============n=nuu==uu=  ================================
  14  ====n=========n=========n==n====  ====u=========n=================  ================================
  15  ======n=u======un===============  ====================n===u=======  =====u===n==========n===========
  16  ================================  =u=======n====u====u==u=========  ==u=============================
  17  ==u=============================  ================================  ================================
  18  ================================  =============n=============n====  ================================
  19  ================================  =======nn=======u===============  ================================
  20  ================================  ================================  ================================
  21  ================================  ==u=============================  ================================
  22  ================================  ================================  ================================
  23  ================================  ================================  =======uu=======n===============
  24  ================================  ================================  ================================
  25  ================================  ================================  ==n=============================
  26  ================================  ================================  ================================
```

Conditions: for every bit of every boolean-function instance (S1, CH, S0, MAJ of the state; s0, s1 of the expansion) the trail fixes the input and output signed differences; the allowed values of the inputs without difference give the derived conditions (`cond.py`), which for P8 are all fixed bits or two-bit (in)equalities (the tables `_CH`, `PQ`, `X2` of `experiments/a0p38.py`, generated by `mkvt.py`; the conditions of rows 16..22, which define the accepted event, are listed in Appendix B). With W7 in F7 (D7 = 2^29, s0(W7y) - s0(W7x) = 03bff800: the same F7 as the published characteristic), the printed-event probability is 2^-99.56 (6 estimator runs of 2,000 particles; the published characteristic 2^-101.05 with the same estimator).

An explicit 38-step semi-free-start collision in the accepted event (Section 6), rebuilt from an estimator success and verified with the reference of `experiments/a0p38.py` (`selftest` item 1) and the organizer reference `verifier/hash_functions.py`; its rows 0..15 are the Step-1 solution S of Section 4 (A0 = c500a7ff):

```
CV1 = 95a24959 b4053f95 1bf0473e 1eab3b7c 650c63d3 e6493d3b ed004f1d eb7eaad3
M   = bd047e95 1dc94891 4bbe458b c7dc3c0a 8b6235e1 9d7630ee 569da3a0 94ddb1c2 464e545d a804c932 acecbe75 c8280172 9a4d6768 16139532 e00d6a99 5fb2827b
M'  = bd047e95 1dc94891 4bbe458b c7dc3c0a 8b6235e1 9d7630ee 569da3a0 b4ddb1c2 420e5c5d 8804c932 a9edacdf c8200d72 9a4d6768 16139532 e00d6a99 5bf28a7b
out = c7dfd8a1 35575813 87ce86fa f1d48e72 29b25310 e8ff5e13 15d145de 81104761
```

### 3.2 How P8 was found (the sign sweep)

Our signed-difference SAT model (`sdmodel.py`, `stepk.py`) was run over the 24 XOR patterns of weight 25 on the shape W7..W11, W15, W16, W23, W25, with the signs free, the dense part bounded by the published weight profile (HW(dA7..15) <= 26, HW(dE7..15) <= 47, HW(dE14..15) <= 4, HW(dA13..15) <= 10) and the tail by an attack-aware weight (P <= 43); every signed message difference already found for a pattern (and its member-swapped mirror) was blocked. Each solution went through the value-level coupling check (`joint.py`: value-exact dense part and value-exact tail steps 16..19) and the estimator (`sweep.py`). Summary (`runs/sweep`): 

```
SW_p05_k0    UNSAT 13s         
SW_p06_k0    UNSAT 14s         
SW_p07_k0    UNSAT 16s         
SW_p00_k0    SAT 3547s          coupled; G 16, printed-event q 2^-102.0063 (one run)
SW_p01_k0    SAT 7349s          not coupled
SW_p09_k0    SAT 9890s          not coupled
SW_p02_k0    TIMEOUT 10800s    
SW_p03_k0    TIMEOUT 10800s    
SW_p04_k0    TIMEOUT 10800s    
SW_p08_k0    TIMEOUT 10800s    
SW_p11_k0    UNSAT 22s         
SW_p16_k0    UNSAT 9s          
SW_p17_k0    UNSAT 8s          
SW_p18_k0    UNSAT 9s          
SW_p19_k0    UNSAT 13s         
SW_p20_k0    UNSAT 10s         
SW_p21_k0    UNSAT 10s         
SW_p22_k0    UNSAT 10s         
SW_p23_k0    UNSAT 11s         
SW_p10_k0    TIMEOUT 10800s    
SW_p14_k0    SAT 8395s          not coupled
SW_p01_k1    SAT 5668s          coupled; G 32, printed-event q 2^-101.8546 (one run)
SW_p12_k0    TIMEOUT 10800s    
SW_p13_k0    TIMEOUT 10800s    
SW_p15_k0    TIMEOUT 10800s    
SW_p00_k1    TIMEOUT 10800s    
SW_p08_k1    SAT 4714s          coupled; G 160, printed-event q 2^-99.7963 (one run)
SW_p03_k1    SAT 4784s          coupled; G 64, printed-event q 2^-100.4655 (one run)
SW_p04_k1    SAT 5055s          coupled; G 64, printed-event q 2^-100.8176 (one run)
SW_p02_k1    TIMEOUT 10800s    
SW_p10_k1    SAT 2514s          coupled; G 129, printed-event q 2^-99.7105 (one run)
SW_p09_k1    SAT 9145s          not coupled
SW_p13_k1    SAT 6977s          not coupled
SW_p12_k1    TIMEOUT 10800s    
SW_p14_k1    TIMEOUT 10800s    
SW_p15_k1    TIMEOUT 10800s    
SW_p00_k2    TIMEOUT 10800s    
SW_p01_k2    TIMEOUT 10800s    
```

P8 = SW_p08_k1 (pattern 8, second iteration; search 4,714 s, coupling 662 s). For the A0-variant attack the relevant quantities are q3 of the accepted event and the c7 class structure (Sections 4-6); P8 has the best of both among the coupled characteristics.

## 4. Step 1: the solution S and its A0-variants

**Lemma 4.1 (Step 2).** For fixed state rows A0..A15, E4..E15 of both members and a chaining value CV1 = (A_{-1..-4}, E_{-1..-4}), the words W0..W7 with E_i = A_i + A_{i-4} - S0(A_{i-1}) - MAJ(A_{i-1}, A_{i-2}, A_{i-3}) (i = 0..3) and W_i = E_i - A_{i-4} - E_{i-4} - S1(E_{i-1}) - CH(E_{i-1}, E_{i-2}, E_{i-3}) - K_i (i = 0..7) reproduce the state rows; CV1 -> (W0, ..., W7) is a bijection (invert steps 7..0); W8..W15 do not depend on CV1. W0..W6 carry no difference (rows 0..6 have none), W7 differs by D7.

**Lemma 4.2 (A0-variants).** Replace A0 of S by a0 in both members. Then E4 = a0 + C4 (C4 = A4 - S0(A3) - MAJ(A3, A2, A1)), W8 = W8C - E4 in each member (W8C = E8 - A4 - S1(E7) - CH(E7, E6, E5) - K8), so dW8 = W8y - W8x is unchanged, and all other words and rows 5..15 are unchanged. The variant is valid iff s0(W8y) - s0(W8x) also equals S's (W8 reaches rows >= 16 only through W23 = s1(W21) + W16 + s0(W8) + W7, W24 = s1(W22) + W17 + s0(W9) + W8 and the later words through them). G = {a0 : valid}; exhaustively (`a0fam.c`):

```
family 68157440 = 2^26.022
distinct c7 45032, largest class 24576
largest classes: 24576 24576 24576 24576 24576 24576 24576 24576 24576 24576 24576 24576
variants in the 64 largest classes: 1474560 = 2^20.492
variants in the 90 largest classes: 1966080 = 2^20.907
variants in the 128 largest classes: 2614272 = 2^21.318
variants in the 256 largest classes: 4292736 = 2^22.033
variants in the 1024 largest classes: 13130880 = 2^23.646
```

**c7 classes.** W7x = c7(a0) - A_{-1} with c7(a0) = E7 - 2 A3 + S0(A2) + MAJ(A2, A1, a0) - S1(E6) - CH(E6, E5, a0 + C4) - K7. For a chaining value, all variants with the same c7 share W7, so one F7 test decides a class. P8 has 32 classes of the maximal size 24,576 (the published characteristic: classes of 3,840). The attack uses all 32 of them: class i = {base_i ^ s : s subset of mask_i, base_i ^ s in G, c7(base_i ^ s) = c7_i}, 24,576 members each (96 batches of 256), 786,432 variants in all. The mask of a class is the set of bits on which its members vary (`lp_classes.py`: the OR of a0 ^ (smallest member)); the masks have 20 to 23 bits: 7feb6c7c (22 bits) x 8, 7fe96c7c (21 bits) x 8, 7feb6c7e (23 bits) x 4, 7fe96c7e (22 bits) x 4, 3feb6c7c (21 bits) x 4, 3fe96c7c (20 bits) x 4.

| class | c7 | base | mask | members |
|---|---|---|---|---|
| 0 | 2a7beb19 | 8b649792 | 3fe96c7c | 24,576 |
| 1 | 2a7beb1b | 9b649791 | 7fe96c7c | 24,576 |
| 2 | 2a7bfb19 | 8b648792 | 3fe96c7c | 24,576 |
| 3 | 2a7bfb1b | 9b648791 | 7fe96c7c | 24,576 |
| 4 | 2a7c6b19 | 8b645b92 | 3feb6c7c | 24,576 |
| 5 | 2a7c6b1b | 9b645b91 | 7feb6c7c | 24,576 |
| 6 | 2a7c7b19 | 8b646792 | 3feb6c7c | 24,576 |
| 7 | 2a7c7b1b | 9b646791 | 7feb6c7c | 24,576 |
| 8 | 2a7deb1b | 9b629793 | 7fe96c7e | 24,576 |
| 9 | 2a7dfb1b | 9b628793 | 7fe96c7e | 24,576 |
| 10 | 2a7e6b1b | 9b601793 | 7feb6c7e | 24,576 |
| 11 | 2a7e7b1b | 9b600793 | 7feb6c7e | 24,576 |
| 12 | 2a7feb1b | 9b609793 | 7fe96c7c | 24,576 |
| 13 | 2a7ffb1b | 9b608793 | 7fe96c7c | 24,576 |
| 14 | 2a806b1b | 9b605b93 | 7feb6c7c | 24,576 |
| 15 | 2a807b1b | 9b606793 | 7feb6c7c | 24,576 |
| 16 | aa7beb19 | 0b649792 | 3fe96c7c | 24,576 |
| 17 | aa7beb1b | 1b649791 | 7fe96c7c | 24,576 |
| 18 | aa7bfb19 | 0b648792 | 3fe96c7c | 24,576 |
| 19 | aa7bfb1b | 1b648791 | 7fe96c7c | 24,576 |
| 20 | aa7c6b19 | 0b645b92 | 3feb6c7c | 24,576 |
| 21 | aa7c6b1b | 1b645b91 | 7feb6c7c | 24,576 |
| 22 | aa7c7b19 | 0b646792 | 3feb6c7c | 24,576 |
| 23 | aa7c7b1b | 1b646791 | 7feb6c7c | 24,576 |
| 24 | aa7deb1b | 1b629793 | 7fe96c7e | 24,576 |
| 25 | aa7dfb1b | 1b628793 | 7fe96c7e | 24,576 |
| 26 | aa7e6b1b | 1b601793 | 7feb6c7e | 24,576 |
| 27 | aa7e7b1b | 1b600793 | 7feb6c7e | 24,576 |
| 28 | aa7feb1b | 1b609793 | 7fe96c7c | 24,576 |
| 29 | aa7ffb1b | 1b608793 | 7fe96c7c | 24,576 |
| 30 | aa806b1b | 1b605b93 | 7feb6c7c | 24,576 |
| 31 | aa807b1b | 1b606793 | 7feb6c7c | 24,576 |

## 5. Step 2: the W7 test and the good pairs

F7 = {w : s0(w + D7) - s0(w) = 03bff800}, |F7| = 287,309,824 (exhaustive), p7 = |F7| / 2^32 = 2^-3.90197 (the same set as for the published characteristic; it is the union of three affine families of 2^28, 2^24 and 2^21 words). The program tests w = c7 - A_{-1} by computing s0(w + D7) - s0(w) and comparing (24 operations, no table).

**Lemma 5.1 (distribution, per variant).** Under H1, for every fixed a0: Pr[W7x in F7] = p7; conditioned on it, (W0..W6) is uniform and independent of W7, and (W16..W21) is a bijective image of (W0..W5) for fixed (W6, W9..W15), hence uniform and independent of (W6, W7) (Lemma 4.1). Per first block, E[good pairs] = g = 32 x 24,576 x p7 = 52,608 (exact by linearity).

## 6. Step 3: row 16 and the accepted event

### 6.1 Row 16

W16 = s1(W14) + W9 + s0(W1) + W0 and, by Lemma 4.1, W0 = a0 + KW0(CV1), W1 = K1(CV1) - S0(a0) - MAJ(a0, a, b) - S1(E0) - CH(E0, e, f) with E0 = a0 + HH(CV1). So E16x = KP + a0 + s0(W1) with per-first-block constants HH, KP, K1, and row 16 (both members, all its conditions) is a function of E16x alone: an exhaustive pass over all 2^32 values of W16 gives the 160 words of the set R16 (`q3tv.c`, the exhaustive pass of `main`; `selftest` item 2 re-checks it on 20,000 random words and the bit-flip neighbours). The 160 words share 19 bits (mask 4cc79bfa); the program tests the TK = 10 lowest of them (bits 1, 3, 4, 5, 6, 7, 8, 9, 11, 12): stage 3a passes with probability 2^-10 exactly (E16x uniform, Lemma 5.1), row 16 with 160 / 2^32.

### 6.2 The accepted event

The program accepts a row-16 pass iff (i) rows 16..22 of both members follow every cell, '+' pair and two-bit condition of P8 closing at rows 16..22, except that **row 19 is checked on its signed differences only** (the XOR differences of A19, E19, W19 and the member-x values on the difference bits), and (ii) the eight output words A34..A37, E34..E37 of the two members are equal after step 37. Nothing is tested at rows 23..37.

**Lemma 6.1.** If (ii) holds, the two second-block outputs are equal (chaining value plus the same eight words), so M0 || M1 and M0 || M1' collide under the target; M1 != M1' because W7 differs. The program certifies exactly what it outputs.

*Why row 19.* Measured with the estimator (one row at a time checked on signed differences only, the others strict, outputs compared): relaxing row 19 raises q3 by about 3.6 bits for P8 (and 3.4 for the published characteristic); rows 17 and 18 lead to dead ends (the derived conditions there are needed by the next row), rows 20..22 add little. In the 40 runs of the study of Section 9 (seeds 4001..4040), 188,796 of 188,796 classified successes have their row-19 conditions in one of four patterns (`pat19`; the 12 conditions: the fixed bits E19[4], E19[18] and ten two-bit conditions):

```
row-19 conditions (in order): E19[4] = 1, E19[18] = 0, E19[10] = E19[29], E19[2] != E19[20], E19[5] != E19[18], E19[6] = E19[19],
E19[10] != E19[28], E19[11] = E19[29], E19[1] = E19[28], A18[29] = A19[29], E19[4] != E19[9], E19[5] != E19[10]
successes of 40 estimator runs (seeds 4001..4040, 32 classes, rebuilt and checked), by the set of violated conditions (1 = violated):
42,216  010000110001   E19[18], conditions 7, 8 and 12 violated
51,411  010000110000   E19[18], conditions 7 and 8 violated
46,939  000000000000   none (the strict row)
48,230  000000000001   condition 12 violated
188,796 of 188,796 successes in these four patterns (complete dumps)
```

## 7. The counted program (`experiments/a0p38.py`, 56,008 bytes, SHA-256 9be5d888d551fb0b12646132b5498183ab18d6087a158c1c65d7659b848a4dc5)

### 7.1 Machine and scalar routines

256-bit word RAM, 64 registers; executed primitives count 1 (load, store, add, sub, and, or, xor, not, shift, immediate, random word), a compare-and-branch 2, one target compression 1 unit; S0, S1, s0, s1 cost 8 each (doubled word, shifts, xors, mask), CH 3, MAJ 4. The routines are executed with counting primitives; broadcast, lane_value, first_lane, r16test and deep add itemised declared counts (their docstrings) (`calibrate`):

| routine | operations |
|---|---|
| first block: 2 random words and their 16 fields (30), counter, cap test, hit-list test (5) | 35 |
| one W7 test (computed, no table), plus 4 for the class loop | 24 + 4 |
| per-first-block scalars HH, AB, EF, FF, K1, KP | 39 |
| the 165 per-first-block broadcast planes (32 + 27 + 3 x 31 + 13; 4 operations each) | 660 |
| per passing class: setup 3, end of class (work counter, cap test) 4 | 7 |
| per batch of 256 variants: the class's row-16 program (1,169 to 1,207, mean 1188.31) + ok test 2 + pointer, compare, branch 4 | prog_i + 6 |
| per stage-3a lane: lowest lane (32), clear and loop (3), a0 from the stored low-21-bit planes (4 x 13 + 1 = 53, widest low mask), E16x (38), the row-16 table test (42) | 168 |
| per row-16 pass (itemised declared count): Step 2 for both members, the expansion and rows 16..37 of both members with the tests of rows 16..22, the output comparison | 3105 |

### 7.2 The row-16 programs (one per class)

Bit L of a 256-bit plane belongs to lane L (one variant). Inputs of the program of class i: the independent varying planes of a0 in mask_i (16 to 19 planes loaded per batch after folding `a0[11] = ~a0[10]`, `a0[22] = a0[21]`, `a0[28] = a0[27] ^ c`, and `a0[16] = ~a0[1]` in classes `ci % 16 in {8,9,10,11}`) and the 165 per-first-block broadcast planes (`HH` 0..31, `AB` on the 27 active bits of `AB_MASK = 0x7feffc7f`, `EF, FF, K1` 0..30, `KP` 0..12); every bit of a0 outside mask_i is the corresponding bit of base_i and is folded as a constant (Section 0.1). `build_e16` builds the DAG of `E0 = a0e + HH` (with `A0_ADD = 0x780` and `a0[10] + 2 a0[11] = 1 + a0[11]` absorbed into `HH, KP` and `a0e`), then for j = 0..30 (`max(TBITS) + 18` for `TK = 10`, `max(TBITS) = 12`): `S0(a0)`, `a0z & AB`, `S1(E0)`, `CH(E0, e, f) = FF ^ (E0 & EF)`, and reduces each column of `~W1 = K1 + S0(a0) + (a0z & AB) + S1(E0) + CH(E0, e, f)` via `reduce_col` (pairing same-polarity wires), then for k = 0..12: `s0(W1)`, `E16x = KP + a0e + s0(W1)` and the comparison with the common value on the 10 tested bits; constants are folded and equal nodes shared. `schedule` allocates 64 registers by Belady's rule (evict the value needed farthest ahead; store it first if it is needed again and has no copy); every load, store and spill is an instruction. Result: 32 programs (32 distinct input patterns), **1,169 to 1,207 instructions per batch, mean 1188.31, with 0 spill stores across all 32 classes** (calibration list in Section 10). The expected work uses the mean (each class passes its W7 test with the same p7), the work cap the maximum. The programs are executed instruction by instruction (`run_prog`) and compared with the scalar definition lane by lane (`selftest` item 4 and the organizer experiment `a0p-online-r38`: 0 mismatches).

## 8. The algorithm (fixed caps)

```text
advice: S (the semi-free-start pair's rows 0..15), the 32 class descriptors (c7, base, mask); precompute (charged): every class member (base ^ s, s subset of mask, in G, c7 = c7_i), stored as 96 batches of |mask| bit planes per class; the 32 row-16 programs
V = 0
for f = 1 .. N_FB:
    if V > V_MAX: halt (failure)                    (V accumulates ALL data-dependent work of every first block: W7 tests, hit list, scalars, planes, classes, lanes, row-16 passes)
    two uniform 256-bit random words -> M0 (16 words, uniform on {0,1}^512); CV1 := F_38(IV, M0)                     [1 unit]
    hits := [i : c7_i - A_{-1} in F7]                                                                               [32 x (24 + 4)]
    if hits: the scalars and the broadcast planes
        for i in hits: for each of the 96 batches of class i: run the row-16 program of class i -> ok plane
            for each lane of ok: a0 from the planes; E16x; if E16x in R16: Step 2, rows 16..37 of both members, the tests of rows 16..22
                (row 19 on signed differences), compare the outputs; if equal: output M0 || M1, M0 || M1' and halt
        V += the work of the class (and, before it, the W7 tests, the hit list, the scalars and the planes of this first block); if V > V_MAX: halt (failure)
halt (failure)
```

*Lemma 8.1 (the cap).* V accumulates every data-dependent operation of every first block (all of v_f in Section 9) and is tested before every first block and after every class, so V <= V_MAX + OVER at every moment (V is updated for every first block, including first blocks with no passing class: their data-dependent work is the W7 tests and the hit-list test, added to V before the next cap test), OVER = 2,577,720,155 (one first block at its maximum: all classes passing, each charged at the longest program, every lane a row-16 pass). The 35 fixed operations per first block are charged separately (N_FB x 35). The run never outputs a non-collision (Lemma 6.1).

## 9. The success probability

*Trials and expectation.* A trial is (first block f, selected variant a0); A_t: a0 is good for f (W7 in F7) and the pair is in the accepted event. E[X_f] = g q3 (Lemma 5.1; H1, H2).

*q3 (H2).* q3 = the average over the 786,432 selected variants of Pr[accepted event | good pair] (including the row-16 factor 160 / 2^32). Estimator `q3tv.c` (binary q3tv2, `DIFFROW=19 RELAX_TAIL=1`, `VARS` = the variant pool of the 32 classes): fixed-effort multilevel splitting, row 16 exact over the 160 W16 words, rows 17..22 with W_i^x uniform (Lemma 5.1) and the rows checked as in the event (row 19 on signed differences), tail: a variant drawn per proposal from the 786,432 selected variants, W7 uniform in F7, rows 23..37 computed, outputs compared. Every success is a verified collision; the successes are rebuilt into real pairs (750 of 750 checked with the reference). 40 runs, 4,000 particles, 16,384 tail proposals per particle, seeds 4001..4040 fixed before the runs:

| seed | stage factors log2 (rows 16..22, tail) | successes (all collisions) | log2 q3 |
|---|---|---|---|
| 4001 | -24.678 -16.997 -13.928 -2.967 -15.967 -6.961 -0.999 -14.152 | 3,601 | -96.6490 |
| 4002 | -24.678 -17.000 -13.895 -3.019 -16.401 -6.989 -1.007 -13.836 | 4,483 | -96.8250 |
| 4003 | -24.678 -17.003 -13.936 -3.038 -15.991 -7.020 -0.992 -13.843 | 4,459 | -96.5012 |
| 4004 | -24.678 -16.984 -13.941 -3.005 -15.639 -6.990 -0.998 -13.949 | 4,145 | -96.1841 |
| 4005 | -24.678 -17.003 -13.949 -3.010 -17.958 -6.985 -1.026 -13.777 | 4,670 | -98.3867 |
| 4006 | -24.678 -17.008 -13.931 -3.014 -15.972 -6.988 -1.024 -14.020 | 3,946 | -96.6351 |
| 4007 | -24.678 -16.965 -13.963 -2.995 -15.401 -6.985 -1.017 -13.910 | 4,258 | -95.9134 |
| 4008 | -24.678 -17.017 -13.940 -2.999 -16.945 -6.963 -1.023 -13.458 | 5,822 | -97.0241 |
| 4009 | -24.678 -16.983 -14.010 -2.995 -15.358 -7.042 -1.003 -13.942 | 4,165 | -96.0106 |
| 4010 | -24.678 -16.962 -13.935 -3.002 -15.665 -6.979 -0.996 -13.918 | 4,235 | -96.1354 |
| 4011 | -24.678 -17.010 -13.916 -2.969 -15.346 -7.001 -0.986 -13.529 | 5,546 | -95.4346 |
| 4012 | stalled at row 20 (no estimate: counted as 0) | 0 | 0 (stalled) |
| 4013 | -24.678 -16.956 -13.877 -2.962 -15.607 -7.016 -0.989 -13.331 | 6,359 | -95.4169 |
| 4014 | -24.678 -17.025 -13.930 -3.019 -16.386 -7.017 -0.978 -13.887 | 4,327 | -96.9191 |
| 4015 | -24.678 -17.006 -13.894 -3.000 -15.205 -7.020 -1.003 -13.867 | 4,386 | -95.6743 |
| 4016 | -24.678 -17.028 -13.974 -2.999 -17.980 -6.992 -1.010 -13.671 | 5,023 | -98.3326 |
| 4017 | -24.678 -17.012 -13.940 -3.013 -15.142 -6.997 -1.028 -13.785 | 4,644 | -95.5965 |
| 4018 | stalled at row 20 (no estimate: counted as 0) | 0 | 0 (stalled) |
| 4019 | -24.678 -16.983 -13.977 -3.033 -14.623 -7.004 -1.000 -13.569 | 5,394 | -94.8670 |
| 4020 | -24.678 -16.954 -13.906 -3.034 -16.338 -6.999 -1.017 -13.542 | 5,494 | -96.4681 |
| 4021 | -24.678 -17.001 -13.956 -3.040 -15.933 -6.991 -0.995 -13.596 | 5,294 | -96.1892 |
| 4022 | -24.678 -16.961 -13.888 -2.990 -17.969 -6.985 -1.000 -13.453 | 5,846 | -97.9234 |
| 4023 | -24.678 -17.027 -13.945 -2.979 -17.967 -7.013 -1.015 -13.333 | 6,351 | -97.9565 |
| 4024 | -24.678 -16.962 -13.865 -2.987 -15.674 -6.988 -0.984 -13.561 | 5,422 | -95.6982 |
| 4025 | -24.678 -17.014 -13.898 -2.981 -17.990 -7.005 -1.021 -14.004 | 3,990 | -98.5903 |
| 4026 | -24.678 -17.030 -13.954 -2.992 -15.630 -6.957 -0.995 -13.567 | 5,401 | -95.8012 |
| 4027 | -24.678 -17.011 -13.956 -2.985 -14.936 -7.015 -1.009 -13.572 | 5,380 | -95.1633 |
| 4028 | -24.678 -17.021 -13.869 -3.027 -15.997 -6.981 -1.008 -13.942 | 4,164 | -96.5232 |
| 4029 | -24.678 -17.005 -13.924 -3.024 -15.973 -7.010 -1.027 -13.571 | 5,386 | -96.2125 |
| 4030 | -24.678 -17.006 -13.913 -2.982 -16.393 -6.990 -1.019 -13.656 | 5,076 | -96.6365 |
| 4031 | -24.678 -17.016 -13.929 -2.977 -16.395 -6.984 -1.013 -13.776 | 4,673 | -96.7677 |
| 4032 | -24.678 -17.013 -13.944 -3.010 -14.975 -6.976 -1.016 -13.758 | 4,732 | -95.3691 |
| 4033 | -24.678 -16.980 -13.889 -2.988 -15.634 -7.005 -0.969 -13.618 | 5,214 | -95.7600 |
| 4034 | -24.678 -16.992 -13.897 -3.052 -15.407 -7.033 -0.975 -13.543 | 5,491 | -95.5758 |
| 4035 | -24.678 -16.999 -13.885 -3.041 -16.413 -7.017 -1.003 -13.762 | 4,717 | -96.7975 |
| 4036 | -24.678 -17.013 -13.952 -3.038 -17.962 -6.999 -1.000 -13.776 | 4,672 | -98.4201 |
| 4037 | -24.678 -17.016 -13.937 -2.989 -14.970 -6.984 -1.035 -13.639 | 5,139 | -95.2474 |
| 4038 | -24.678 -17.007 -13.912 -3.024 -15.625 -6.999 -1.006 -13.543 | 5,492 | -95.7934 |
| 4039 | -24.678 -17.017 -13.926 -3.031 -15.195 -6.994 -1.022 -13.541 | 5,500 | -95.4025 |
| 4040 | -24.678 -17.004 -13.954 -2.983 -15.604 -6.983 -1.005 -13.440 | 5,899 | -95.6513 |

Mean 2^-96.1821, relative sd 0.601, one-sided 99% Student bound (t = 2.4258, 39 degrees of freedom) 2^-96.5603, bootstrap 1% quantile of the mean 2^-96.5278; 188,796 successes. The row-20 stage has the largest spread across the runs (sd 0.97 bits of its log2 factor; the others at most 0.20). Runs 4012 and 4018 found no survivor at row 20 and are counted as an estimate of 0. **q3_model = 2^-97.0000.** q3_model = 2^-97.0 was set from the first 20 runs (seeds 4001..4020: their 99% bound 2^-96.9989, rounded down to a tenth) and kept when 20 further runs were added after a first review found its margin thin (seeds 4021..4040, fixed before those runs; all runs are reported); over all 40 runs the 99% bound is 0.4397 bits above q3_model. Rounding the 40-run bound down would give 2^-96.6; we keep 2^-97.0 for the margin. At the 40-run bound 2^-96.5603 the ledger gives 86.45224.

*The pair term (H3).* Every success passes row 16, so given A_t, X_f - 1 <= R_f - 1 (the other row-16 passes of f). Measured (`h3p.py`): 750 successes rebuilt and verified (all accepted by the program's event, so the estimator's event and the program's agree on every one; 99% bound on a disagreement rate 0.6%), all 750 re-found in their own class; every selected variant of every passing class evaluated on the success's CV1: 6,252 passing classes, 153,649,152 variants, **6 other row-16 passes, 0 further accepted pairs** (5.72 expected under independence). One-sided 99% Poisson limit of E[R_f - 1 | A_t]: 0.0194 = 2^-5.69; charged 2^-5.1 (the limit rounded up to a tenth plus 0.5, the rule of 1a695f0b). Sampling: every 25th success line of the study's dump files in sorted file order, the first 750 of them (`h3p.py`, `POOL` and `STUDY` set to this study's pool and dumps), so they come from the first runs and successes within a run are not independent; the Poisson limit assumes independence, which the 0.5 margin only partly covers (pair term 2^-3 moves the claim by +0.07, Section 10). A second sample of 750 successes spread evenly over all 40 runs (`SPREAD=750`; every success of the sorted dump files, equally spaced) gives 750 verified, 6,278 passing classes, 154,288,128 variants, 6 other row-16 passes, 0 further accepted pairs: 99% limit 2^-5.69, charge 2^-5.1 by the same rule. We charge the larger value, that of the first sample. Given a success, its CV1 passes the W7 test for 8.34 classes on average (1 + 31 p7 = 3.07 if the classes were independent): the c7 values of the classes are related, so their W7 tests pass together. The expectations of the ledger are linear and unaffected; the effect is inside the measured pair term and the work cap.

*Bonferroni, independence, caps.* Pr[X_f >= 1] >= E[X_f] - E[X_f (X_f - 1)] / 2 >= g q3 (1 - 2^h3 / 2); first blocks are independent (fresh coins); the data-dependent work v_f of a first block satisfies 0 <= v_f <= vmax_f = 2,577,720,155 with mean at most vbar = 255682.5696 (exact rational in the ledger), so Var(sum v_f) <= N_FB vmax_f vbar and Chebyshev bounds Pr[sum v_f > (1 + 2^-16) N_FB vbar] by P_cap = 2.866e-11; V_MAX = ceil((1 + 2^-16) N_FB vbar). On the complement no cap halts the run. N_FB is the least integer with 1 - exp(-N_FB g q3_model (1 - 2^h3 / 2)) - P_cap - 2^-60 >= 0.39 (2^-60 covers the rounding of the exponential, evaluated at 80 decimal digits).

## 10. Ledger (exact; `ledger_a0p.py`, Appendix C)

```text
T = A_C + A_S + DEV + N_FB + (N_FB x 35 + V_MAX + OVER + PRE + FIN) / C + 6
  A_C = 2^78, A_S = 2^74, DEV = 2^70 (Section 12, H4; the levels of fb176310)
  N_FB = 1,510,856,422,656,568,670,938,611 = 2^80.32164   (g = 52,608 good pairs per first block, g q3_model = 2^-81.3170)
  vbar = 255682.5696 operations per first block: W7 tests 32 x (24 + 4), hit list, scalars and planes (699) x min(1, 32 p7),
         passing classes 32 p7 x (7 + 96 x (19013/16 + 6)) (the mean program, 19013/16 = 1188.3125), stage-3a lanes 32 p7 x 24,576 x 2^-10 x 168, row-16 passes 32 p7 x 24,576 x 160 / 2^32 x 3105
  vmax_f = OVER: every class at the longest program (1,207), every lane a row-16 pass
  V_MAX = 386,305,546,840,284,932,073,036,074,922, OVER = 2,577,720,155, PRE = 8,858,632,192 (member tests over the 32 class cubes, the batch planes, program generation)
  FIN = 1,600 operations and 6 units (the final verification)
N = T x 2728 = 391,359,281,662,064,599,086,033,030,886  ->  T = 2^86.89078048  ->  time_log2 = 86.89079
```

Calibration (`calibrate.json`, the output of `calibrate()` of `experiments/a0p38.py`; `selftest` prints the same):

```
{"prog": [1173, 1186, 1169, 1180, 1182, 1195, 1176, 1189, 1201, 1196, 1204, 1199, 1186, 1182, 1194, 1190, 1174, 1186, 1170, 1180, 1183, 1195, 1177, 1189, 1204, 1199, 1207, 1202, 1187, 1183, 1196, 1192], "w7": 24, "fb_fixed": 35, "w7_loop": 4, "scalars": 39, "planes": 660, "batch_ctl": 6, "class_ctl": 7, "lane": 168, "deep": 3105, "tk": 10, "classes": 32, "class_size": 24576}
```

*Certificate.* `python3 ledger_a0p.py --q3 -97.0 --h3 -5.1 --cal calibrate.json` prints the ledger and checks `(2728^E << 8689078) < N^E <= (2728^E << 8689079)` with E = 100000 (exact integers), so 86.89079 is the smallest five-decimal upper bound on log2 T. *Sensitivity* (each row recomputed by the ledger with this calibration unless marked reference):

```
claimed                                                                                          86.89079   (N_FB 2^80.3216)
q3_model = the study mean 2^-96.1821                                                             86.07536   (N_FB 2^79.5037)
q3_model 2^-97.78 (the q3_model of fb176310 for the published characteristic)                    87.66943   (N_FB 2^81.1016)
pair term 2^-3                                                                                   86.96255   (N_FB 2^80.3936)
allowances of 1a695f0b (A_C = 2^48, A_S = 2^50, DEV = 2^50)                                      86.88754   (N_FB 2^80.3216)
A_C = 2^84                                                                                       87.07058   (N_FB 2^80.3216)
08e2e0d3: 32 classes, per-class programs (1,438..1,482, mean 1462.25), TK = 12                   87.14808   (reference)
1a695f0b: 8 classes, one shared program of 1,511, q3_model 2^-97.0, pair term 2^-5.9             87.22358   (reference)
the same with per-class programs (08be594's construction; ours, 1,454..1,469, mean 1463.00)      87.17957   (reference)
```

## 11. Memory and advice

```
online 3476064 bytes = 2^21.729: 32 row-16 programs (one per class) 38,058 instructions, class planes and batch base words 32 x 96 batches x ((20..23) + 1) words = 69,120 words,
  class table 32 x 6 words, broadcast planes 165 words, row-16 table 160 words, spill slots 0 words, scalar routines at most 700 instructions,
  the deep path's two traces (200 words), M0, CV1 and counters (32 words); 32 bytes per word or instruction
preprocessing (single-threaded, sequential stages; peak of the summed resident memory of all processes, sampled every 0.2 s):
  Step-1 solve of P8 (joint.py: Python model + Kissat; the S in use, as in 1a695f0b): 279,720 KB = 2^28.0936
  signed search of P8 (stepk.py): at most 2^27.92
  class descriptors (a0cls.c, 32 hash passes): 37,036 KB = 2^25.14; class selection (lp_classes.py with the a0cls member pass): 46,804 KB = 2^25.48
  condition tables and pair (mkvt.py, fromjoint.py): below 2^24
preprocessing peak 2^28.0936
```

*Sampling.* The peaks are maxima of the summed resident memory sampled every 0.2 s, so a shorter allocation spike could be missed; the claim 2^28.10 bytes = 288,630 KiB is 3.2%% above the largest sample (279,720 KiB), and the Step-1 solve is a single Kissat process whose resident memory grows with its clause database (it does not spike).

*Scope of the memory bound.* Peak memory covers code, advice, retained data, tables and working state of the whole computation: the online algorithm, the charged precomputation (class members, planes, the 32 programs) and the computations behind the advice and the allowances (the characteristic search, the Step-1 solve, the class descriptors and their selection, the condition tables), each run single-threaded and sequentially. P8 and S are those of 1a695f0b (produced by `stepk.py` and `joint.py`); the claimed figure is the largest measured peak in the record above. The class descriptors are found in 32 passes over a hash of c7 (`a0cls.c`, at most 2^23 pairs resident) and selected by `lp_classes.py`. The online figure also covers the deep path's working state (two traces, about 6 KB) and M0, CV1.

Claimed memory 2^28.10 bytes: the maximum of the online footprint and the measured preprocessing peaks. Advice: S (16 words of each member and CV1), the 32 class descriptors (c7, base, mask: 384 bytes), the constants of the characteristic: below 2^14 bytes; everything else (class members, planes, the programs) is computed by the charged preprocessing.

## 12. Premises

- **H1** single-trial chaining value: CV1 = F_38(IV, M0) for uniform M0 behaves as uniform for the events of one variant (Lemma 5.1).
- **H2** q3 >= q3_model for the accepted event, averaged over the selected variants (Section 9; 40 runs).
- **H3** the pair term within a first block is at most 2^h3 (Section 9; measured).
- **H4** allowances: The allowances are envelopes, not measurements: A_C = 2^78, A_S = 2^74, DEV = 2^70 target compressions (the levels charged by fb176310). All of our computation for this line of work (the characteristic search and sweep, the Step-1 solve, the class data, the q3 studies and all development) ran on one 10-core machine, for less than 2^22 core-seconds by our own accounting. The bound does not depend on that accounting or on a rate: ten cores running continuously for a full year are 2^28.3 core-seconds, and even at 2^30 target compressions per core-second (above any CPU core; SHA-256 runs at about 2^24 compressions per second per core) that is 2^58.3, below DEV = 2^70 alone. With A_C = 2^84 the ledger gives time_log2 = 87.07058 (+0.17979; Section 10); with the smaller allowances of 1a695f0b, 86.88754.
- **H5** unit-cost bit-sliced planes: the row-16 programs are charged as their instruction counts on 256-bit planes, as in the cost model.

## 13. Organizer experiments (`experiments/manifest.json`)

**a0p-online-r38** (H1, H5, Lemma 4.1). Trials 0..7: first blocks drawn from the organizer seed (two uniform words each, real 38-step compressions) until one has a passing class (at most 64); its first passing class is run on two batches (the class's first 512 members) with that class's program: the ok plane is compared lane by lane with E16x from the Step-2 words and the 38-step trace, and W7 with c7 - A_{-1} and F7; trial 0 also runs the batch of the semi-free-start pair's variant and requires the counted program to find and accept it. A pair M0 || M1, M0 || M1' (one variant, not a collision) is returned iff there is no mismatch. Trials 8..255 return no pair by design. Before any selection, each active trial draws 64 first blocks from the organizer seed and counts the W7 passes of all 32 classes (observations uncond_first_blocks, uncond_class_passes; expectation 64 x 32 x |F7| / 2^32 = 137.0 per trial under H1). Validation by us: 2,560 unconditional first blocks over 5 requests, 5,514 class W7 passes against 5,480 expected (ratio 1.006); passes come in groups of related classes (a success's CV1 passes 8.3 classes on average), so the per-trial count has a large variance.

**a0p-q3-r38** (consistency check of H2). Trials 0..9: 10 replicates of the estimator of q3 for the accepted event (64 particles; 64, 8, 8, 4, 2, 1 children at rows 17..22 with the row's E bits imposed, at row 19 one of the four patterns drawn uniformly, weight 4 x 2^-f; tail: 192 proposals per particle, a variant of 512 embedded samples of the selected classes (32 of the 32 classes represented), W7 uniform in F7 (its three affine families; the family drawn by rejection from its own word, the value bits from a fresh word), rows 23..37, outputs compared; every success rebuilt into CV1, M1, M1' and accepted only if it is a 38-step collision in the accepted event with W7 in F7). Trial t < 10 returns its first verified pair as CV1 || M1 and CV1 || M1' (semi-free-start collisions, never collisions from the IV); trial 10 returns a pair iff no rebuild failed and the mean of the 10 estimates is at least 2^-98.6000 (pass rule fixed from 48 development requests before any validation run; their pooled means: minimum -98.100, 5% quantile -97.100, median -96.398; replicate mean 2^-96.2059).
 What a pass shows: the replica estimates the same event as the study, restricted to the four row-19 patterns (a lower bound) and to 512 of the selected variants; its 48 development requests (480 replicates) have mean 2^-96.2059 against the study mean 2^-96.1821. Shifting their pooled means down by 1, 2 or 3 bits (a q3 that much lower) makes 2%, 38% and 90% of requests fail the rule (none at the claimed level): a pass excludes a gross error in the estimator or the program, it does not certify the bound.

*Validation by us* (the shipped file; 256 trials; network-less container, 1 CPU, 128 MiB; python:3.12.12-slim-bookworm):

```
holdA  a0p-online-r38  returned  8  lanes 4096  mismatches 0  stage-3a passes 3  first blocks 21  unconditional: 512 first blocks, 1127 class W7 passes (expected 1096.0)  0.4s
holdA  a0p-q3-r38      returned  8  pooled 2^-95.857 (rule >= 2^-98.6)  replicates with a success 7/10  verified pairs 12  failed rebuilds 0  5.6s
holdB  a0p-online-r38  returned  8  lanes 4096  mismatches 0  stage-3a passes 4  first blocks 21  unconditional: 512 first blocks, 1145 class W7 passes (expected 1096.0)  0.5s
holdB  a0p-q3-r38      returned  9  pooled 2^-96.047 (rule >= 2^-98.6)  replicates with a success 8/10  verified pairs 13  failed rebuilds 0  5.7s
holdC  a0p-online-r38  returned  8  lanes 4096  mismatches 0  stage-3a passes 5  first blocks 31  unconditional: 512 first blocks, 1110 class W7 passes (expected 1096.0)  0.4s
holdC  a0p-q3-r38      returned 10  pooled 2^-95.773 (rule >= 2^-98.6)  replicates with a success 9/10  verified pairs 16  failed rebuilds 0  5.8s
holdD  a0p-online-r38  returned  8  lanes 4096  mismatches 0  stage-3a passes 5  first blocks 36  unconditional: 512 first blocks, 1048 class W7 passes (expected 1096.0)  0.4s
holdD  a0p-q3-r38      returned  8  pooled 2^-96.397 (rule >= 2^-98.6)  replicates with a success 7/10  verified pairs 14  failed rebuilds 0  5.8s
public a0p-online-r38  returned  8  lanes 4096  mismatches 0  stage-3a passes 10  first blocks 20  unconditional: 512 first blocks, 1084 class W7 passes (expected 1096.0)  0.4s
public a0p-q3-r38      returned  9  pooled 2^-95.650 (rule >= 2^-98.6)  replicates with a success 8/10  verified pairs 14  failed rebuilds 0  5.6s
```

## 14. Limitations

- q3 is a Monte Carlo estimate (participant-run, resampled particles; the Student bound assumes independent runs); the organizer replica checks a reduced version of it. The row-19 pattern support of the replica is the four patterns of Section 9, which cover all 188,796 classified successes of this study (as they did in the study of 1a695f0b), so the replica estimates a lower bound of the event's probability.
- The pair term and the success distribution are measured on rebuilt estimator successes (H1 premise for real chaining values).
- The bit-sliced programs are executed on sampled batches; full-scale execution is infeasible.

## Appendix A. Self-test and calibration of `experiments/a0p38.py`

```
1 the semi-free-start pair collides, M != M', accepted event, W7 in F7 ok 
  its variant A0 is in G and in a selected class                       ok (class 13)
2 row 16: the 160 W16 words hold it; 20,000 random words and 1,280 neighbours agree ok 
3 Lemma 4.1: E16x formula, W7 = c7 - A_-1, rows 11..15 and the word differences on 20 chaining values ok 
4 row-16 programs (one per class): instructions mean / max, loads, spill stores ok 1188.31 / 1207 (loads 186..193, stores 0..0)
  program against the definition on 2 x 512 lanes of real first blocks ok [{'uncond_first_blocks': 64, 'uncond_class_passes': 181, 'first_blocks': 2, 'passing_classes': 8, 'lanes': 512, 'stage3a_passes': 0, 'mismatches': 0}, {'uncond_first_blocks': 64, 'uncond_class_passes': 134, 'first_blocks': 1, 'passing_classes': 6, 'lanes': 512, 'stage3a_passes': 0, 'mismatches': 0}]
5 the counted program finds the semi-free-start pair in its batch      ok (5312 operations)
6 replicate: estimate, accepted pairs rebuilt and verified, failed rebuilds 0 ok (log2 -94.887, 3 pairs)
   calibrate: {'prog': [1173, 1186, 1169, 1180, 1182, 1195, 1176, 1189, 1201, 1196, 1204, 1199, 1186, 1182, 1194, 1190, 1174, 1186, 1170, 1180, 1183, 1195, 1177, 1189, 1204, 1199, 1207, 1202, 1187, 1183, 1196, 1192], 'w7': 24, 'fb_fixed': 35, 'w7_loop': 4, 'scalars': 39, 'planes': 660, 'batch_ctl': 6, 'class_ctl': 7, 'lane': 168, 'deep': 3105, 'tk': 10, 'classes': 32, 'class_size': 24576}
SELFTEST PASSED
```

## Appendix B. The conditions of rows 16..22 (the accepted event; member x, `experiments/a0p38.py` tables)

Per row: for A, E, W the mask of fixed x-values (trail difference bits and one-bit conditions), their x-values and the XOR difference; the '+' pairs E_i[b] = E_{i-1}[b]; the two-bit conditions (kind 0 A / 1 E / 2 W, row, bit; = or !=). Row 19 is checked on its XOR differences and the x-values of its difference bits only.

```
row 16 E: mask 48421a80 x-value 48021200 xor 40421200
row 16 W: mask 20000000 x-value 20000000 xor 20000000
row 16: E16[7] = E16[26]
row 16: E16[14] != E16[28]
row 16: A15[4] = A16[4]
row 16: E16[11] = E16[16]
row 16: A15[7] = A16[7]
row 16: A14[15] = A16[15]
row 16: A14[16] = A16[16]
row 16: A15[17] = A16[17]
row 16: A14[23] = A16[23]
row 16: A14[25] = A16[25]
row 16: A15[27] = A16[27]
row 16: E16[3] != E16[8]
row 16: E16[4] = E16[23]
row 16: W16[20] != W16[27]
row 16: W16[22] = W16[31]
row 16: W16[4] != W16[6]
row 16: A15[29] = A16[29]
row 16: W16[14] = W16[18]
row 16: W16[8] = W16[25]
row 16: W16[1] != W16[12]
row 17 A: mask 20000000 x-value 20000000 xor 20000000
row 17 E: mask 40421a80 x-value 00000800 xor 00000000
row 17 +: E17[b] = E16[b] for the bits of 00040010
row 17: A17[9] != A17[20]
row 17: A16[15] = A17[15]
row 17: A17[6] = A17[18]
row 17: A16[16] != A17[16]
row 17: A16[23] = A17[23]
row 17: A16[25] = A17[25]
row 17: A17[8] != A17[17]
row 18 E: mask 40461210 x-value 00421200 xor 00040010
row 18 +: E18[b] = E17[b] for the bits of 01808000
row 18: E18[0] = E18[13]
row 18: E18[17] = E18[22]
row 18: E18[5] != E18[23]
row 18: A16[29] = A18[29]
row 18: E18[9] = E18[23]
row 19 E: mask 01848010 x-value 00008010 xor 01808000
row 19: E19[10] = E19[29]
row 19: E19[2] != E19[20]
row 19: E19[5] != E19[18]
row 19: E19[6] = E19[19]
row 19: E19[10] != E19[28]
row 19: E19[11] = E19[29]
row 19: E19[1] = E19[28]
row 19: A18[29] = A19[29]
row 19: E19[4] != E19[9]
row 19: E19[5] != E19[10]
row 20 E: mask 01848010 x-value 00040010 xor 00000000
row 20 +: E20[b] = E19[b] for the bits of 20000000
row 21 E: mask 21808000 x-value 21008000 xor 20000000
row 21: E21[10] = E21[15]
row 21: E21[11] = E21[24]
row 21: E21[2] = E21[16]
row 22 E: mask 20000000 x-value 00000000 xor 00000000
```

## Appendix C. Programs (SHA-256 and full listings; `experiments/a0p38.py` is assembled by `mka0p.py` from the `a0p_*.py` parts)

- `experiments/a0p38.py`: 9be5d888d551fb0b12646132b5498183ab18d6087a158c1c65d7659b848a4dc5
- `ledger_a0p.py`: bf183e83d5393c99f5674c24880a5c859bdd38c148dbf043104082c2bf088649
- `lp_classes.py`: f2df440ab9ef74f5d9aedfa57ca1b1c86a8ba5d379509dcb5b1afe2cadf2f1f5
- `a0cls.c`: 6521cee23d00bd58118dddec95d3b47edf9b1cef6efd9e66ba141cc69f90aa72
- `a0p_ref.py`: 74b6b6d789225225fa9aef2a11f3d6a97106a896277707e560c0138600070c48
- `a0p_core.py`: e36d2d5665bf944eee1935290aaeb825eea1138016d3c5c6a60e069dac4cc3f1
- `a0p_prog.py`: dadbb5ae5e0f455bbce1c1ba67ed8779cf8024d0125baa9c64773809a9b8cb1d
- `a0p_scal.py`: 2c91c10be225c23c52f836f4e3d94609c2ac26a2499188a37b473a3c887d2300
- `a0p_run.py`: 31e607d05b2272ad3a53ab573b0c118a08017ed24debfd49f2e625eb997902ec
- `a0p_main.py`: 2ec04f94538d0893a2dc1f441dfb01ba4ce5159edd1a4d3d62abbecc0dadfd0e
- `mka0p.py`: 03042e080b33dfaec2add1e23af1be06ed3bda2543b5ddc02e07cada09e9f3ec
- `mkvt.py`: 19e95c874e6d0b05447836aea5d7289a467c581bcb03bb94376154d04e25b26a
- `a0fam.c`: e74ead8bd7d20ce7ef40284fd91a104ce71b3fe5b8cadcd59b9c274b3ad4eb69
- `h3p.py`: 0ce84d4db2dbe6e696b962e84db6f24e67e56d03535c6ab266e57042625b6717
- `q3tv.c`: e01dbb414ef2a7e0cecf79638bb287130e1309dfa439727b57bc8b32b3957ead
- `sweep.py`: 7e2dcef5b849da79236857a328306ddee77c3acf34975e6c5bb72ab69dcbc918
- `stepk.py`: 59284d8f7f19bb62cc0265f3b9e18ac2d1532b79a755d6e3d3b672298dfc9ab0
- `score.py`: 22df6e29bdeef726bb395123426656641e262e8d5cd3117839caba4e1682493e
- `joint.py`: 7e641e68540e79d3be7902d52bccb372febe17dc16ca5364f9390c3ecf37cb95
- `fromjoint.py`: a05593f8e0104ee3d2d378257159d45bce7108f7d5130f43a53c5850bd762b61
- `prep.py`: 7550447964f6b5444638db1b60142475ea839cb066e262b6bfeb6d713b957299
- `cond.py`: 2220ff08693b795d999eabb5c31dac06fcf9905eb57f403bdd2dbe05901426a8
- `sdmodel.py`: 023a387e5eeb2f5ac58bc7e6175c0aa44e80775ddb88b1964dde21b461eaf420
- `vmodel.py`: 86bafa88614a1b85b1d3601f3b27479c381442769b0fda054ff7651dbd84244d
- `sha38.py`: 7aa83ceebd6baede02877736640e066e09d640656a08929e792ae1c5c1b0fe67
- `mkpkg4.py`: 78347ae128bf31c2b4ab2c511902fc50c2c8676495e47443dc522899b0ac2f07

### ledger_a0p.py

```python
#!/usr/bin/env python3
"""ledger_a0p.py - exact ledger of the A0-variant attack with P8 (own code; the structure of the ledger of 2d1c4fc2 / fb176310).
T = A_C + A_S + DEV + N_FB + (N_FB x FIXED + V_MAX + OVER + PRE + FIN_OPS) / C + FIN_UNITS, in target compressions, C = 2728.
Every count is an executed count of experiments/a0p38.py (`calibrate`); probabilities: p7 = |F7| / 2^32 (exhaustive), the stage-3a rate 2^-10
and the row-16 rate 160 / 2^32 (exact under Lemma 5.1), q3_model (H2), the pair term (H3).  Integers and fractions; logs at 80 digits."""
from fractions import Fraction as Fr
from decimal import Decimal as D, getcontext
import math, argparse, json
getcontext().prec = 80
C = 2728
F7 = 287_309_824; p7 = Fr(F7, 2 ** 32)
CAL = dict(prog=[1173, 1186, 1169, 1180, 1182, 1195, 1176, 1189, 1201, 1196, 1204, 1199, 1186, 1182, 1194, 1190, 1174, 1186, 1170, 1180, 1183, 1195, 1177, 1189, 1204, 1199, 1207, 1202, 1187, 1183, 1196, 1192],
           w7=24, fb_fixed=35, w7_loop=4, scalars=39, planes=660, batch_ctl=6, class_ctl=7, lane=168, deep=3105, tk=10, classes=32, class_size=24576, gl=160, f7=F7,
           mask_bits=[20, 21, 20, 21, 21, 22, 21, 22, 22, 22, 23, 23, 21, 21, 22, 22, 20, 21, 20, 21, 21, 22, 21, 22, 22, 22, 23, 23, 21, 21, 22, 22])   # the 32 classes of P8 (per-class programs; mask widths of the classes, in class order)

def dlog2(x):
    x = Fr(x); return (D(x.numerator).ln() - D(x.denominator).ln()) / D(2).ln()
def qmodel(q):
    num = Fr(round(q * 10000)) / 10000
    return Fr(int((D(2) ** (D(num.numerator) / D(num.denominator))) * D(10) ** 75), 10 ** 75)

def ledger(q3=-97.0, h3=-5.1, AC=78, AS=74, DEV=70, succ=Fr(39, 100), eps=Fr(1, 2 ** 16), cal=None, NFB=None):
    k = dict(CAL, **(cal or {}))
    ncl, size = k['classes'], k['class_size']; nb = size // 256
    p7 = Fr(k['f7'], 2 ** 32)
    q = qmodel(q3); g = ncl * size * p7                              # good pairs per first block (exact, linearity)
    pr = k['prog'] if isinstance(k['prog'], list) else [k['prog']] * ncl   # per-class program lengths (one per class)
    assert len(pr) == ncl
    per_class = k['class_ctl'] + nb * (Fr(sum(pr), ncl) + k['batch_ctl'])     # expected work of one passing class (each passes with p7: the mean is exact)
    per_class_max = k['class_ctl'] + nb * (max(pr) + k['batch_ctl'])          # the most expensive class (work cap)
    lanes = Fr(size, 2 ** k['tk']) * k['lane']                         # expected stage-3a lanes of a passing class x their cost
    r16 = Fr(size * k['gl'], 2 ** 32) * k['deep']                          # expected row-16 passes of a passing class x their cost
    vbar = ncl * (k['w7'] + k['w7_loop']) + 2 * ncl * p7 + min(Fr(1), ncl * p7) * (k['scalars'] + k['planes']) + ncl * p7 * (per_class + lanes + r16)
    vmax = ncl * (k['w7'] + k['w7_loop'] + 2) + k['scalars'] + k['planes'] + ncl * (per_class_max + size * (k['lane'] + k['deep']))
    over = vmax                                                        # a first block's maximal work beyond V_MAX (the cap is tested before each first block and after each class)
    h3f = Fr(int(D(2) ** D(str(h3)) * D(10) ** 30), 10 ** 30)          # H3: sum_t Pr[A_t] E[R_f - 1 | A_t] <= 2^h3 E[X_f]
    lam = g * q * (1 - h3f / 2)                                        # per first block, Bonferroni
    def pcap(n): return Fr(vmax, 1) / (eps ** 2 * n * vbar)
    def ok(n): return D(1) - (-(D(n) * D(lam.numerator) / D(lam.denominator))).exp() - D(pcap(n).numerator) / D(pcap(n).denominator) - D(2) ** -60 - D(succ.numerator) / D(succ.denominator) >= 0
    if NFB is None:
        lo, hi = 1, 2 ** 100
        while lo < hi:
            mid = (lo + hi) // 2
            if ok(mid): hi = mid
            else: lo = mid + 1
        NFB = lo
    VMAX = math.ceil((1 + eps) * NFB * vbar)
    mb = k.get('mask_bits'); mb = mb if isinstance(mb, list) and len(mb) == ncl else [21] * ncl   # mask width of each class (21: the mask 7fe96c7c)
    PRE = sum((1 << b) * 40 + nb * 256 * b * 2 for b in mb) + 2 ** 32   # member tests over each class's cube (40 each), planes (2 per member bit), program generation
    FIN_OPS, FIN_UNITS = 1600, 6
    alw = 2 ** AC + 2 ** AS + 2 ** DEV
    N = C * (alw + NFB + FIN_UNITS) + NFB * k['fb_fixed'] + VMAX + over + PRE + FIN_OPS
    T = Fr(N, C); claim = math.ceil(float(dlog2(T)) * 1e5) / 1e5
    assert D(N).ln() - D(C).ln() <= D(round(claim * 1e5)) / D(100000) * D(2).ln()
    return dict(NFB=NFB, log2NFB=float(dlog2(NFB)), g=float(g), log2gq=float(dlog2(g * q)), vbar=float(vbar), vbar_exact=vbar, vmax=vmax, VMAX=VMAX,
                over=over, PRE=PRE, Pcap=float(pcap(NFB)), N=N, log2T=float(dlog2(T)), claim=claim, per_class=per_class, alw=float(dlog2(alw)),
                pre_log2=float(dlog2(Fr(PRE, C) + alw)), attack=float(dlog2(Fr(N - C * alw, C))))

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--q3', type=float, default=-97.0); ap.add_argument('--h3', type=float, default=-5.1)
    ap.add_argument('--cal', default=None); ap.add_argument('--sens', action='store_true'); a = ap.parse_args()
    cal = json.loads(open(a.cal).read()) if a.cal else None
    r = ledger(a.q3, a.h3, cal=cal)
    for key in ('NFB', 'log2NFB', 'g', 'log2gq', 'vbar', 'vmax', 'VMAX', 'over', 'PRE', 'Pcap', 'per_class', 'alw', 'pre_log2', 'attack', 'N', 'log2T', 'claim'): print(key, r[key])
    n, E5, kk = r['N'], 100000, round(r['claim'] * 100000)
    assert (C ** E5 << (kk - 1)) < n ** E5 <= (C ** E5 << kk); print('certificate: (2728^E << %d) < N^E <= (2728^E << %d)' % (kk - 1, kk))
    if a.sens:
        for nm, kw in [('q3_model = the study mean 2^-96.2971', dict(q3=-96.2971)), ('q3_model 2^-97.78 (the q3_model of fb176310)', dict(q3=-97.78)),
                       ('pair term 2^-3', dict(h3=-3.0)), ('A_C = 2^78', dict(AC=78)), ('A_C = 2^84', dict(AC=84)), ('one shared row-16 program of 1,511 for every class', dict(cal=dict(prog=1511)))]:
            kw2 = dict(q3=a.q3, h3=a.h3, cal=cal); kw2.update(kw); x = ledger(**kw2); print('%-40s %.5f (attack %.4f)' % (nm, x['claim'], x['attack']))
```

### lp_classes.py

```python
"""lp_classes.py <S prefix> <out dir> [n classes]: deterministic class selection for the A0-variant attack (own code; replaces the
hand-run selection used for P8). From <S>.cls.txt (a0cls: c7 size, classes of size >= 256) and the members of the largest classes
(a0cls member pass): mask of a class = OR of (a0 ^ min member); keep the mask shared by the most largest-size classes (ties: smaller
mask value), take the first n of them by c7. Writes classes.txt (c7 base size), vars_pool.txt (j a0 A1 A2 w8 Wx9 Wx10, the q3tv VARS
format) and derived.json (D7, T7, MASK, CBITS, class size, classes). With ALLMAX=1: every largest-size class, whatever its mask (for
per-class programs); classes.txt then has a fourth column, the class's own mask."""
import sys, os, json, subprocess, collections
sys.path.insert(0, '/work/m38')
from sha38 import trace, S0, S1, s0, CH, MAJ, M32 as M
pre, out = sys.argv[1], sys.argv[2]; NC = int(sys.argv[3]) if len(sys.argv) > 3 else 8
os.makedirs(out, exist_ok=True)
sizes = [(int(c, 16), int(n)) for c, n in (l.split() for l in open(pre + '.cls.txt'))]
top = max(n for _, n in sizes); big = sorted(c for c, n in sizes if n == top)
open(out + '/big_c7.txt', 'w').write(''.join('%08x\n' % c for c in big))
r = subprocess.run(['/work/m38/a0cls', pre + '.a0.txt', '0', out + '/big_agg.txt', out + '/big_c7.txt', 'agg'], capture_output=True, text=True, check=True)
info = {}                                                             # c7 -> (min member, mask = bits that vary)
for l in open(out + '/big_agg.txt'):
    c, b, m, n = l.split(); info[int(c, 16)] = (int(b, 16), int(m, 16))
cnt = collections.Counter(m for _, m in info.values())
MASK = min(cnt, key=lambda m: (-cnt[m], m))
ALL = os.environ.get('ALLMAX') == '1'
sel = sorted(info)[:NC] if ALL else [c for c in sorted(info) if info[c][1] == MASK][:NC]
open(out + '/sel_c7.txt', 'w').write(''.join('%08x\n' % c for c in sel))
subprocess.run(['/work/m38/a0cls', pre + '.a0.txt', '0', out + '/sel_members.txt', out + '/sel_c7.txt'], capture_output=True, text=True, check=True)
mem = collections.defaultdict(list)                                   # members of the selected classes only
for l in open(out + '/sel_members.txt'):
    c, a = l.split(); mem[int(c, 16)].append(int(a, 16))
cbits = 0
for c in sel: cbits |= info[c][0] ^ info[sel[0]][0]
P = json.load(open(pre + '.pair.json')); cv, Wx, Wy = P['cv'], P['Wx'], P['Wy']
tx = trace(cv, Wx, 16); A, E = tx[0], tx[1]
C4 = (A[4] - S0(A[3]) - MAJ(A[3], A[2], A[1])) & M
W8C = (E[8] - A[4] - S1(E[7]) - CH(E[7], E[6], E[5]) - 0xd807aa98) & M
assert ((W8C - ((A[0] + C4) & M)) & M) == Wx[8], 'S own A0 does not reproduce W8'
with open(out + '/classes.txt', 'w') as f:
    for c in sel: f.write('%08x %08x %d' % (c, info[c][0], len(mem[c])) + (' %08x\n' % info[c][1] if ALL else '\n'))
with open(out + '/vars_pool.txt', 'w') as f:
    for j, c in enumerate(sel):
        for a0 in sorted(mem[c]): f.write('%d %08x %08x %08x %08x %08x %08x\n' % (j, a0, A[1], A[2], (W8C - ((a0 + C4) & M)) & M, Wx[9], Wx[10]))
sval = lambda row: sum((-(1 << (31 - k)) if c == 'u' else (1 << (31 - k))) for k, c in enumerate(row) if c in 'un') & M   # as prep.py
C = json.load(open(pre + '.char.json'))
D7 = (Wy[7] - Wx[7]) & M; T7 = (sval(C['22']['W']) - ((Wy[15] - Wx[15]) & M)) & M   # s0 difference of W7 the trail needs (W22 = .. + W15 + s0(W7))
d = dict(D7='%08x' % D7, T7='%08x' % T7, MASK='%08x' % MASK, mask_bits=bin(MASK).count('1'), CBITS='%08x' % cbits, class_size=top,
         classes_with_mask=cnt[MASK], n_largest=len(big), selected=['%08x' % c for c in sel], a0cls=r.stdout.strip())
json.dump(d, open(out + '/derived.json', 'w'), indent=1); print(json.dumps(d))
```

### a0cls.c

```c
// A0-only variant family of a dense part and its c7 classes (own code). a0fam <pair: cv Wx[16] Wy[16] hex> [min class size, out file]
// a0cls: the same in 32 passes over a hash of c7 (at most 2^23 pairs resident; peak memory measured in proof.md 11).
// a0cls <pair> 0 <out> <c7 list>: one pass writing "c7 a0" for every member of the listed classes (in a0 order).
// a0cls <pair> 0 <out> <c7 list> agg: one pass writing "c7 min mask size" per listed class (mask = bits that vary = OR & ~AND).
// A variant changes A0 only (both members): E4 and W8 of each member change; valid iff the modular difference dW8 and the
// s0 difference ds0(W8) equal the pair's (W8 enters rows >= 16 only through them). c7 = W7^x + A_{-1} depends on A0 through
// MAJ(A2, A1, A0) and CH(E6, E5, E4). Prints the family size, the number of distinct c7 values and the largest class sizes.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
typedef uint32_t u32;
static const u32 K[16] = {0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174};
static inline u32 ror(u32 x, int n) { return (x >> n) | (x << (32 - n)); }
static inline u32 S0(u32 x) { return ror(x, 2) ^ ror(x, 13) ^ ror(x, 22); }
static inline u32 S1(u32 x) { return ror(x, 6) ^ ror(x, 11) ^ ror(x, 25); }
static inline u32 s0(u32 x) { return ror(x, 7) ^ ror(x, 18) ^ (x >> 3); }
static inline u32 CH(u32 x, u32 y, u32 z) { return (x & y) ^ (~x & z); }
static inline u32 MAJ(u32 x, u32 y, u32 z) { return (x & y) ^ (x & z) ^ (y & z); }
static u32 A[2][20], E[2][20], W[2][16];
static int cmp(const void *a, const void *b) { u32 x = *(const u32 *)a, y = *(const u32 *)b; return x < y ? -1 : x > y; }
static int cmp64(const void *a, const void *b) { uint64_t x = *(const uint64_t *)a, y = *(const uint64_t *)b; return x < y ? -1 : x > y; }
static int cmpl(const void *a, const void *b) { long x = *(const long *)a, y = *(const long *)b; return x > y ? -1 : x < y; }   // descending
int main(int argc, char **argv) {
    FILE *f = fopen(argv[1], "r"); u32 cv[8];
    for (int j = 0; j < 8; j++) fscanf(f, "%x", &cv[j]);
    for (int m = 0; m < 2; m++) for (int i = 0; i < 16; i++) fscanf(f, "%x", &W[m][i]);
    fclose(f);
    for (int m = 0; m < 2; m++) {
        for (int j = 0; j < 4; j++) { A[m][3 - j] = cv[j]; E[m][3 - j] = cv[4 + j]; }
        for (int i = 0; i < 16; i++) {
            u32 T1 = E[m][i] + S1(E[m][i + 3]) + CH(E[m][i + 3], E[m][i + 2], E[m][i + 1]) + K[i] + W[m][i];
            E[m][i + 4] = A[m][i] + T1; A[m][i + 4] = T1 + S0(A[m][i + 3]) + MAJ(A[m][i + 3], A[m][i + 2], A[m][i + 1]);
        }
    }
#define a(m, i) A[m][(i) + 4]
#define e(m, i) E[m][(i) + 4]
    u32 dW8 = W[1][8] - W[0][8], ds8 = s0(W[1][8]) - s0(W[0][8]); int thr = atoi(argv[2]);
    if (argc > 4) {                                             // members of the listed classes
        static u32 sel[1 << 16]; int ns = 0; FILE *g = fopen(argv[4], "r"); FILE *o = fopen(argv[3], "w");
        while (ns < (1 << 16) && fscanf(g, "%x%*[^\n]", &sel[ns]) == 1) ns++;
        fclose(g); qsort(sel, ns, 4, cmp); long nm = 0; int agg = argc > 5;
        static u32 mn[1 << 16], ro[1 << 16], ra[1 << 16]; static long cn[1 << 16];
        for (int i = 0; i < ns; i++) { mn[i] = 0xffffffffu; ro[i] = 0; ra[i] = 0xffffffffu; cn[i] = 0; }
        for (uint64_t x = 0; x < (1ULL << 32); x++) {
            u32 a0 = (u32)x, w8[2], e4 = 0;
            for (int m = 0; m < 2; m++) { e4 = a(m, 4) + a0 - S0(a(m, 3)) - MAJ(a(m, 3), a(m, 2), a(m, 1)); w8[m] = e(m, 8) - a(m, 4) - e4 - S1(e(m, 7)) - CH(e(m, 7), e(m, 6), e(m, 5)) - K[8]; }
            if (w8[1] - w8[0] != dW8 || s0(w8[1]) - s0(w8[0]) != ds8) continue;
            u32 c = e(0, 7) - 2 * a(0, 3) + S0(a(0, 2)) + MAJ(a(0, 2), a(0, 1), a0) - S1(e(0, 6)) - CH(e(0, 6), e(0, 5), e4) - K[7];
            u32 *h = bsearch(&c, sel, ns, 4, cmp);
            if (!h) continue;
            nm++;
            if (!agg) { fprintf(o, "%08x %08x\n", c, a0); continue; }
            long i = h - sel; if (a0 < mn[i]) mn[i] = a0; ro[i] |= a0; ra[i] &= a0; cn[i]++;
        }
        if (agg) for (int i = 0; i < ns; i++) fprintf(o, "%08x %08x %08x %ld\n", sel[i], mn[i], ro[i] & ~ra[i], cn[i]);
        fclose(o); printf("members of %d classes: %ld\n", ns, nm); return 0;
    }
    long cap = 1L << 23; uint64_t *pr = malloc(8 * cap); long fam = 0, ncls = 0; FILE *o = fopen(argv[3], "w");
    for (u32 p = 0; p < 32; p++) {
        long n = 0;
        for (uint64_t x = 0; x < (1ULL << 32); x++) {
            u32 a0 = (u32)x, w8[2], e4 = 0;
            for (int m = 0; m < 2; m++) { e4 = a(m, 4) + a0 - S0(a(m, 3)) - MAJ(a(m, 3), a(m, 2), a(m, 1)); w8[m] = e(m, 8) - a(m, 4) - e4 - S1(e(m, 7)) - CH(e(m, 7), e(m, 6), e(m, 5)) - K[8]; }
            if (w8[1] - w8[0] != dW8 || s0(w8[1]) - s0(w8[0]) != ds8) continue;
            u32 c = e(0, 7) - 2 * a(0, 3) + S0(a(0, 2)) + MAJ(a(0, 2), a(0, 1), a0) - S1(e(0, 6)) - CH(e(0, 6), e(0, 5), e4) - K[7];
            if (((c * 0x9e3779b1u) >> 27) != p) continue;           // pass by a hash of c7 (a class stays in one pass)
            if (n >= cap) { fprintf(stderr, "pass too large\n"); return 1; }
            pr[n++] = ((uint64_t)c << 32) | a0;
        }
        fam += n; qsort(pr, n, 8, cmp64);
        for (long i = 0; i < n; ) { long j = i; while (j < n && (pr[j] >> 32) == (pr[i] >> 32)) j++; if (j - i >= thr) { ncls++; fprintf(o, "%08x %ld\n", (u32)(pr[i] >> 32), j - i); } i = j; }
    }
    fclose(o); printf("family %ld = 2^%.3f; classes of size >= %d: %ld\n", fam, log2((double)fam), thr, ncls); return 0;
}
```

### a0p_ref.py

```python
# a0p_ref.py - part 1 of experiments/a0p38.py: target, characteristic P8 and the reference construction of the A0-variant attack (own code).
# The attack design (A0-variants of one Step-1 solution, c7 classes decided by one W7 test, bit-sliced row-16 filter, accepted event with a
# direct output comparison) is that of the public packages 2d1c4fc2 (itseasypop) and fb176310 (Jbenisek) on the framework of ePrint
# 2026/1120 / 2026/1080; per-class row-16 programs (class bits folded as constants) follow 08be594 (johnservil); this code, the
# characteristic P8, its accepted event (row 19 on signed differences) and the 32-class selection are ours.
import sys, json, hashlib, struct, zlib, base64, math
M = 0xffffffff
NR = 38
K = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5, 0xd807aa98, 0x12835b01, 0x243185be,
     0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174, 0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa,
     0x5cb0a9dc, 0x76f988da, 0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967, 0x27b70a85,
     0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb]
IV = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]
def ror(x, n): return ((x >> n) | (x << (32 - n))) & M
def S0(x): return ror(x, 2) ^ ror(x, 13) ^ ror(x, 22)
def S1(x): return ror(x, 6) ^ ror(x, 11) ^ ror(x, 25)
def s0(x): return ror(x, 7) ^ ror(x, 18) ^ (x >> 3)
def s1(x): return ror(x, 17) ^ ror(x, 19) ^ (x >> 10)
def CH(x, y, z): return (x & y) ^ (~x & z & M)
def MAJ(x, y, z): return (x & y) ^ (x & z) ^ (y & z)

def trace(cv, w16, n=NR):
    """A[i], E[i] (i = -4..n-1, dicts) and W[0..n-1] of the first n steps from the chaining value cv."""
    W = list(w16)
    for i in range(16, n): W.append((s1(W[i-2]) + W[i-7] + s0(W[i-15]) + W[i-16]) & M)
    A = {-1-i: cv[i] for i in range(4)}; E = {-1-i: cv[4+i] for i in range(4)}
    for i in range(n):
        E[i] = (A[i-4] + E[i-4] + S1(E[i-1]) + CH(E[i-1], E[i-2], E[i-3]) + K[i] + W[i]) & M
        A[i] = (E[i] - A[i-4] + S0(A[i-1]) + MAJ(A[i-1], A[i-2], A[i-3])) & M
    return A, E, W

def compress(cv, w16, n=NR):
    A, E, W = trace(cv, w16, n)
    f = [A[n-1], A[n-2], A[n-3], A[n-4], E[n-1], E[n-2], E[n-3], E[n-4]]
    return [(cv[i] + f[i]) & M for i in range(8)]
```

### a0p_core.py

```python

# ---- the characteristic P8 (proof.md Section 3); member x = M, member y = M'.  PCV/PMX/PMY: a 38-step semi-free-start pair in the accepted
# event whose rows 0..15 are the Step-1 solution S.  Cells per kind (A, E, W) and row: (mask, x-value, x^y difference, 0) = the signed trail with
# its one-bit conditions; PQ[i]: bits with E_i = E_{i-1}; X2: the other two-bit conditions (k1, i1, b1, equal, k2, i2, b2, row), member x.
_CH = [{7: (1610612736, 536870912, 1610612736, 0), 8: (4261904, 0, 4261904, 0), 10: (65552, 16, 65552, 0), 11: (134219780, 4, 134219780, 0), 12: (555746818, 555746818, 555746818, 0), 13: (536870912, 0, 536870912, 0), 14: (134348944, 0, 134348944, 0), 15: (42041344, 8454144, 42041344, 0), 17: (536870912, 536870912, 536870912, 0)}, {5: (536870912, 536870912, 0, 0), 6: (675811328, 4718592, 0, 0), 7: (3897036800, 3892318208, 3758096384, 0), 8: (3897301136, 3355707520, 676075664, 0), 9: (51380235, 0, 51380235, 0), 10: (1073807376, 1073741840, 1073807376, 0), 11: (612564992, 8519680, 612564992, 0), 12: (1763748865, 671121409, 1763748865, 0), 13: (4195046, 102, 4195046, 0), 14: (134348800, 134217728, 134348800, 0), 15: (2176, 128, 2176, 0), 16: (1212291712, 1208095232, 1078071808, 0), 17: (1078073984, 2048, 0, 0), 18: (1078333968, 4329984, 262160, 0), 19: (25460752, 32784, 25198592, 0), 20: (25460752, 262160, 0, 0), 21: (562069504, 553680896, 536870912, 0), 22: (536870912, 0, 0, 0), 23: (536870912, 536870912, 0, 0)}, {7: (536870912, 0, 536870912, 0), 8: (71305216, 71303168, 71305216, 0), 9: (536870912, 536870912, 536870912, 0), 10: (83956394, 67113504, 83956394, 0), 11: (527360, 524288, 527360, 0), 15: (71305216, 67108864, 71305216, 0), 16: (536870912, 536870912, 536870912, 0), 23: (25337856, 25165824, 25198592, 0), 25: (536870912, 0, 536870912, 0)}]
PQ = [0, 0, 0, 0, 0, 0, 3221225472, 264336, 0, 0, 0, 0, 0, 0, 0, 0, 0, 262160, 25198592, 0, 536870912, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
X2 = [(1, 16, 7, 1, 1, 16, 26, 16), (1, 16, 14, 0, 1, 16, 28, 16), (0, 15, 4, 1, 0, 16, 4, 16), (1, 16, 11, 1, 1, 16, 16, 16), (0, 15, 7, 1, 0, 16, 7, 16), (0, 14, 15, 1, 0, 16, 15, 16), (0, 14, 16, 1, 0, 16, 16, 16), (0, 15, 17, 1, 0, 16, 17, 16), (0, 14, 23, 1, 0, 16, 23, 16), (0, 14, 25, 1, 0, 16, 25, 16), (0, 15, 27, 1, 0, 16, 27, 16), (1, 16, 3, 0, 1, 16, 8, 16), (1, 16, 4, 1, 1, 16, 23, 16), (0, 17, 9, 0, 0, 17, 20, 17), (2, 16, 20, 0, 2, 16, 27, 16), (2, 16, 22, 1, 2, 16, 31, 16), (0, 16, 15, 1, 0, 17, 15, 17), (0, 17, 6, 1, 0, 17, 18, 17), (0, 16, 16, 0, 0, 17, 16, 17), (2, 16, 4, 0, 2, 16, 6, 16), (0, 16, 23, 1, 0, 17, 23, 17), (0, 16, 25, 1, 0, 17, 25, 17), (0, 17, 8, 0, 0, 17, 17, 17), (0, 15, 29, 1, 0, 16, 29, 16), (1, 18, 0, 1, 1, 18, 13, 18), (1, 18, 17, 1, 1, 18, 22, 18), (1, 18, 5, 0, 1, 18, 23, 18), (0, 16, 29, 1, 0, 18, 29, 18), (1, 18, 9, 1, 1, 18, 23, 18), (1, 19, 10, 1, 1, 19, 29, 19), (1, 19, 2, 0, 1, 19, 20, 19), (1, 19, 5, 0, 1, 19, 18, 19), (1, 19, 6, 1, 1, 19, 19, 19), (1, 19, 10, 0, 1, 19, 28, 19), (1, 19, 11, 1, 1, 19, 29, 19), (1, 19, 1, 1, 1, 19, 28, 19), (0, 18, 29, 1, 0, 19, 29, 19), (1, 19, 4, 0, 1, 19, 9, 19), (1, 19, 5, 0, 1, 19, 10, 19), (1, 21, 10, 1, 1, 21, 15, 21), (1, 21, 11, 1, 1, 21, 24, 21), (1, 21, 2, 1, 1, 21, 16, 21), (2, 23, 14, 0, 2, 23, 21, 23), (2, 23, 16, 0, 2, 23, 25, 23), (2, 23, 17, 0, 2, 23, 26, 23), (2, 23, 0, 1, 2, 23, 30, 23), (2, 23, 1, 1, 2, 23, 31, 23), (2, 25, 20, 1, 2, 25, 27, 25), (2, 25, 22, 0, 2, 25, 31, 25), (2, 25, 4, 1, 2, 25, 6, 25), (2, 16, 14, 1, 2, 16, 18, 16), (2, 16, 8, 1, 2, 16, 25, 16), (2, 16, 1, 0, 2, 16, 12, 16)]
GL = [549441552, 549441553, 549441556, 549441557, 549442576, 549442577, 549442580, 549442581, 1891627024, 1891627025, 1891627028, 1891627029, 1891628048, 1891628049, 1891628052, 1891628053, 2698498064, 2698498065, 2698498068, 2698498069, 2698499088, 2698499089, 2698499092, 2698499093, 2699022352, 2699022353, 2699022356, 2699022357, 2699023376, 2699023377, 2699023380, 2699023381, 2700595216, 2700595217, 2700595220, 2700595221, 2700596240, 2700596241, 2700596244, 2700596245, 3988787216, 3988787217, 3988787220, 3988787221, 3988788240, 3988788241, 3988788244, 3988788245, 3989303312, 3989303313, 3989303316, 3989303317, 3989304336, 3989304337, 3989304340, 3989304341, 3989311504, 3989311505, 3989311508, 3989311509, 3989312528, 3989312529, 3989312532, 3989312533, 3989827600, 3989827601, 3989827604, 3989827605, 3989828624, 3989828625, 3989828628, 3989828629, 3990884368, 3990884369, 3990884372, 3990884373, 3990885392, 3990885393, 3990885396, 3990885397, 3991400464, 3991400465, 3991400468, 3991400469, 3991401488, 3991401489, 3991401492, 3991401493, 3991408656, 3991408657, 3991408660, 3991408661, 3991409680, 3991409681, 3991409684, 3991409685, 3991924752, 3991924753, 3991924756, 3991924757, 3991925776, 3991925777, 3991925780, 3991925781, 4040167440, 4040167441, 4040167444, 4040167445, 4040168464, 4040168465, 4040168468, 4040168469, 4040683536, 4040683537, 4040683540, 4040683541, 4040684560, 4040684561, 4040684564, 4040684565, 4040691728, 4040691729, 4040691732, 4040691733, 4040692752, 4040692753, 4040692756, 4040692757, 4041207824, 4041207825, 4041207828, 4041207829, 4041208848, 4041208849, 4041208852, 4041208853, 4042264592, 4042264593, 4042264596, 4042264597, 4042265616, 4042265617, 4042265620, 4042265621, 4042780688, 4042780689, 4042780692, 4042780693, 4042781712, 4042781713, 4042781716, 4042781717, 4042788880, 4042788881, 4042788884, 4042788885, 4042789904, 4042789905, 4042789908, 4042789909]
#<<CONSTS>>
CELLS = [[(0, 0, 0, 0)] * NR for _ in range(3)]
for _k in range(3):
    for _i, _c in _CH[_k].items(): CELLS[_k][_i] = _c
_tx, _ty = trace(PCV, PMX), trace(PCV, PMY)
SAx = {i: _tx[0][i] for i in range(-4, 16)}; SEx = {i: _tx[1][i] for i in range(-4, 16)}
SAy = {i: _ty[0][i] for i in range(-4, 16)}; SEy = {i: _ty[1][i] for i in range(-4, 16)}
DWT = [(_ty[2][i] - _tx[2][i]) & M for i in range(NR)]          # modular differences of the words (y - x) of the pair
D7 = DWT[7]; T7 = T7_C                                         # s0(W7y) - s0(W7x) required by rows 22/23 (the trail)
def inF7(w): return ((s0((w + D7) & M) - s0(w)) & M) == T7
R19 = 19                                                         # the row checked on its signed differences only (accepted event)

def rowok(tx, ty, i, relax=True):
    """Row i of both traces: cells (x-value on the mask, XOR difference), '+' pairs and two-bit conditions keyed at row i (member x).
    The W cells of rows 7..10 are not part of the event (W7: F7; W8..W10: modular differences).  With relax, row R19 is checked on its
    signed differences only (XOR difference and member-x value on the difference bits)."""
    (Ax, Ex, Wx), (Ay, Ey, Wy) = tx, ty
    sig = relax and i == R19
    for k, (x, y) in enumerate(((Ax[i], Ay[i]), (Ex[i], Ey[i]), (Wx[i], Wy[i]))):
        if k == 2 and 7 <= i <= 10: continue
        m, v, d, _ = CELLS[k][i]
        if (x ^ y) != d: return False
        if (x & (d if sig else m)) != (v & (d if sig else m)): return False
    if sig: return True
    if (Ex[i] ^ Ex[i-1]) & PQ[i]: return False
    for (k1, i1, b1, eq, k2, i2, b2, row) in X2:
        if row == i and (((tx[k1][i1] >> b1) ^ (tx[k2][i2] >> b2)) & 1) != (0 if eq else 1): return False
    return True

def accepted(tx, ty):
    """The accepted event: rows 16..22 (row 19 on signed differences) and equal outputs after step 37."""
    return all(rowok(tx, ty, i) for i in range(16, 23)) and all(tx[k][i] == ty[k][i] for k in (0, 1) for i in range(34, 38))

# ---- A0-variants (proof.md Section 4) ----
C4 = (SAx[4] - S0(SAx[3]) - MAJ(SAx[3], SAx[2], SAx[1])) & M                                    # E4 = a0 + C4 (both members)
W8C = [(E[8] - A[4] - S1(E[7]) - CH(E[7], E[6], E[5]) - K[8]) & M for A, E in ((SAx, SEx), (SAy, SEy))]   # W8 = W8C - E4
D8 = DWT[8]; DS8 = (s0(PMY[8]) - s0(PMX[8])) & M
def in_G(a0):
    e4 = (a0 + C4) & M; x = (W8C[0] - e4) & M; y = (W8C[1] - e4) & M
    return ((y - x) & M) == D8 and ((s0(y) - s0(x)) & M) == DS8
def c7of(a0):
    """W7x = c7(a0) - A_{-1}."""
    return (SEx[7] - 2 * SAx[3] + S0(SAx[2]) + MAJ(SAx[2], SAx[1], a0) - S1(SEx[6]) - CH(SEx[6], SEx[5], (a0 + C4) & M) - K[7]) & M
def words(cv, a0):
    """Step 2: the message words W0..W15 of both members connecting cv to the variant a0 of S."""
    out = []
    for SA, SE, wp in ((SAx, SEx, PMX), (SAy, SEy, PMY)):
        A = dict(SA); E = dict(SE); A[0] = a0
        for j in range(4): A[-1-j] = cv[j]; E[-1-j] = cv[4+j]
        for i in range(5): E[i] = (A[i] + A[i-4] - S0(A[i-1]) - MAJ(A[i-1], A[i-2], A[i-3])) & M
        w = [(E[i] - A[i-4] - E[i-4] - S1(E[i-1]) - CH(E[i-1], E[i-2], E[i-3]) - K[i]) & M for i in range(9)]
        out.append(w + list(wp[9:16]))
    return out
def e16x(cv, a0): return trace(cv, words(cv, a0)[0], 17)[1][16]
C16 = (SAx[12] + SEx[12] + S1(SEx[15]) + CH(SEx[15], SEx[14], SEx[13]) + K[16]) & M
R16 = sorted((C16 + g) & M for g in GL)                          # the E16x values with row 16 holding (exhaustive, 160 words)
R16SET = frozenset(R16)
_sh = M
for _v in R16: _sh &= ~(_v ^ R16[0]) & M
SHARED = _sh                                                       # bits on which all row-16 words agree
TK = 10                                                            # tested bits of the row-16 filter: the TK lowest shared bits
TBITS = [j for j in range(32) if (SHARED >> j) & 1][:TK]

# ---- classes (proof.md Section 5): class i = {base ^ s : s subset of its mask, a0 in G, c7(a0) = c7_i}, 24,576 variants each ----
def dep(t, mask):
    """bits of t deposited on the set bits of mask (lowest first)"""
    r = 0; j = 0
    while mask:
        b = mask & -mask
        if (t >> j) & 1: r |= b
        mask ^= b; j += 1
    return r
_MEM = {}
def members(ci, count, start=0):
    """the members number start..start+count-1 of class ci in the canonical order (increasing t of base ^ dep(t, mask))"""
    if ci not in _MEM:
        c7, base, mk = CLASSES[ci]; mlo = mk & 0x1fffff; mhi = mk & 0xffe00000; blo = base & 0x1fffff; bhi = base & 0xffe00000
        lo = [x for t in range(1 << bin(mlo).count('1')) if in_G(bhi | (x := blo ^ dep(t, mlo))) and c7of(bhi | x) == c7]
        hi = [y for t in range(1 << bin(mhi).count('1')) if in_G((y := bhi ^ dep(t, mhi)) | lo[0]) and c7of(y | lo[0]) == c7]
        _MEM[ci] = [y | x for y in hi for x in lo]
    return _MEM[ci][start:start + count]

def rebuild(W, a0):
    """A success of the estimator (member-x words W[7..22] with W7 in F7, rows 16..22 sampled) and its variant a0 -> (cv, Mx, My):
    W0..W6 by the inverse expansion, CV1 by inverting steps 7..0 of the variant."""
    W = dict(W)
    for i in range(22, 15, -1): W[i - 16] = (W[i] - s1(W[i - 2]) - W[i - 7] - s0(W[i - 15])) & M
    A = {i: SAx[i] for i in range(8)}; A[0] = a0; E = {i: SEx[i] for i in range(4, 8)}; E[4] = (a0 + C4) & M
    for i in range(7, -1, -1):
        A[i - 4] = (E[i] - A[i] + S0(A[i - 1]) + MAJ(A[i - 1], A[i - 2], A[i - 3])) & M
        E[i - 4] = (E[i] - A[i - 4] - S1(E[i - 1]) - CH(E[i - 1], E[i - 2], E[i - 3]) - K[i] - W[i]) & M
    cv = [A[-1], A[-2], A[-3], A[-4], E[-1], E[-2], E[-3], E[-4]]
    wx, wy = words(cv, a0)
    return cv, wx, wy
```

### a0p_prog.py

```python

# ---- the bit-sliced row-16 program (proof.md Section 7.2) ----
# Bit L of every 256-bit plane belongs to lane L (one variant).  The program computes, for 256 variants of one batch, the TK tested bits of
# E16x = KP + a0e + s0(W1), ~W1 = K1 + S0(a0) + (a0z & AB) + S1(E0) + CH(E0, e, f), E0 = a0e + HH (Lemma 4.1, with A0_CONST = 0x380 absorbed into
# K1 and a0z = a0 & ~0x380, and A0_ADD = 0x780 plus a0[11]^a0[10]=1 absorbed into HH, KP and a0e), and their AND with the tested values.
# Constant and correlated bits of a0 are folded; wires carry a polarity bit (0 or 1) so complementation is free until materialised.  The allocator
# gives a spill-free instruction list over 64 registers in which every load, store and spill is one instruction; the list is the charge.
ONES = (1 << 256) - 1
A0_CONST = 0x380                                                    # bits 7..9 of a0 are 1 in all 786,432 variants across all 32 classes
A0_ADD = 0x780                                                      # 0x380 + 2^10 (from a0[10] + 2*a0[11] = 2^10 + a0[11]*2^10)
AB_MASK = 0x7feffc7f                                                # bits 0..30 except 7..9 (folded into K1) and 20 (always 0 in a0)
class Prog:
    def __init__(s): s.nodes = [None]; s.cache = {}; s.inputs = {}
    def inp(s, name):
        if name not in s.inputs: s.nodes.append(('in', name)); s.inputs[name] = len(s.nodes) - 1
        return (s.inputs[name], 0)
    def _mk(s, op, a, b=None):
        key = (op, a, b) if op == 'not' or b is None else (op,) + tuple(sorted((a, b)))
        if key not in s.cache: s.nodes.append(key); s.cache[key] = len(s.nodes) - 1
        return s.cache[key]
    def not_(s, a): return (a[0], a[1] ^ 1)
    def _mat(s, a):
        if a[0] == 0: return a[1]
        return s._mk('not', a[0]) if a[1] else a[0]
    def xor(s, a, b):
        if a[0] == 0: return (b[0], b[1] ^ a[1])
        if b[0] == 0: return (a[0], a[1] ^ b[1])
        if a[0] == b[0]: return (0, a[1] ^ b[1])
        return (s._mk('xor', a[0], b[0]), a[1] ^ b[1])
    def and_(s, a, b):
        if a[0] == 0: return b if a[1] else (0, 0)
        if b[0] == 0: return a if b[1] else (0, 0)
        if a == b: return a
        if a[0] == b[0] and a[1] != b[1]: return (0, 0)
        if a[1] and b[1]: return (s._mk('or', a[0], b[0]), 1)
        return (s._mk('and', s._mat(a), s._mat(b)), 0)
    def or_(s, a, b): return s.not_(s.and_(s.not_(a), s.not_(b)))
    def ha(s, x, y): return s.xor(x, y), s.and_(x, y)
    def fa(s, x, y, z):
        if x[0] == 0 and x[1] == 0: return s.ha(y, z)
        if y[0] == 0 and y[1] == 0: return s.ha(x, z)
        if z[0] == 0 and z[1] == 0: return s.ha(x, y)
        if x[0] == 0 and x[1] == 1: return s.not_(s.xor(y, z)), s.or_(y, z)
        if y[0] == 0 and y[1] == 1: return s.not_(s.xor(x, z)), s.or_(x, z)
        if z[0] == 0 and z[1] == 1: return s.not_(s.xor(x, y)), s.or_(x, y)
        if x[1] == y[1]: p, q, r = x, y, z
        elif x[1] == z[1]: p, q, r = x, z, y
        else: p, q, r = y, z, x
        t = s.xor(p, q); u = s.xor(p, r) if p[1] == r[1] else s.xor((p[0], 0), (r[0], 0))
        return s.xor(t, r), s.xor(p if p[1] == r[1] else q, s.and_(t, u))

def reduce_col(p, col, nxt_col, last=False):
    """Carry-save reduction of one bit column col to a single wire, pairing same-polarity wires and pushing carries to nxt_col."""
    col = [x for x in col if not (x[0] == 0 and x[1] == 0)]
    while sum(1 for x in col if x == (0, 1)) >= 2:
        col.remove((0, 1)); col.remove((0, 1))
        if nxt_col is not None: nxt_col.append((0, 1))
    def pop_pair(arr):
        for i in range(len(arr)):
            for j in range(i + 1, len(arr)):
                if arr[i][0] != 0 and arr[j][0] != 0 and arr[i][1] == arr[j][1]:
                    y = arr.pop(j); x = arr.pop(i); return x, y
        return arr.pop(0), arr.pop(0)
    while len(col) > 1:
        c1 = [x for x in col if x == (0, 1)]; vs = [x for x in col if x != (0, 1)]
        if len(col) == 2:
            a, b = col.pop(0), col.pop(0)
            if last: col.append(p.xor(a, b)); break
            sm, cy = p.ha(a, b); col.append(sm)
            if nxt_col is not None: nxt_col.append(cy)
        elif c1 and len(vs) >= 2:
            col.remove((0, 1)); x, y = pop_pair(col)
            if last and not col: col.append(p.xor(p.xor((0, 1), x), y)); break
            sm, cy = p.fa((0, 1), x, y); col.append(sm)
            if nxt_col is not None: nxt_col.append(cy)
        elif not c1 and len(vs) % 2 == 0 and len(vs) >= 2:
            x, y = pop_pair(col); sm, cy = p.ha(x, y); col.append(sm)
            if nxt_col is not None: nxt_col.append(cy)
        else:
            a, b, c = col.pop(0), col.pop(0), col.pop(0)
            if last and not col: col.append(p.xor(p.xor(a, b), c)); break
            sm, cy = p.fa(a, b, c); col.append(sm)
            if nxt_col is not None: nxt_col.append(cy)
    return col[0] if col else (0, 0)

def build_e16(cbits, nlane):
    """cbits[j]: 'L' (lane-varying bit of a0), (nm, pol) (correlated plane), 0 or 1 (folded).  Returns (Prog, ok node)."""
    p = Prog()
    def a0_wire(c, j):
        if c == 'L': return p.inp('A%d' % j)
        if isinstance(c, tuple): w = p.inp(c[0]); return p.not_(w) if c[1] else w
        return (0, c)
    a0 = [a0_wire(cbits[j], j) for j in range(32)]
    a0z = [(0, 0) if (A0_CONST >> j) & 1 else a0[j] for j in range(32)]
    a0e = list(a0z); a0e[10] = a0[11]; a0e[11] = (0, 0); c27 = (cbits[28] == ('A27', 1))
    if c27: a0e[27] = a0[28]; a0e[28] = (0, 0)
    bc = lambda nm, n=32: [p.inp('%s%d' % (nm, j)) for j in range(n)]
    HH = bc('HH', 32); EF, FF, K1 = (bc(nm, 31) for nm in ('EF', 'FF', 'K1'))
    AB = [p.inp('AB%d' % j) if (AB_MASK >> j) & 1 else (0, 0) for j in range(31)]
    hi = max(TBITS); n = hi + 1; KP = bc('KP', n)
    ec = [[] for _ in range(32)]; E0 = [None] * 32; e0_idx = 0
    if c27: ec[27].append((0, 1))
    def get_e0(m):
        nonlocal e0_idx
        while e0_idx <= m:
            k = e0_idx; ec[k].extend([a0e[k], HH[k]])
            E0[k] = reduce_col(p, ec[k], ec[k + 1] if k + 1 < 32 else None, last=(k == 31)); e0_idx += 1
        return E0[m]
    cols = [[] for _ in range(31)]; W1 = []; u = {}; ecols = [[] for _ in range(n)]; ok0 = (0, 1); ok1 = (0, 1); tset = set(TBITS)
    def step_e16(k, s0w):
        nonlocal ok0, ok1
        ecols[k].extend([KP[k], a0e[k], s0w])
        e = reduce_col(p, ecols[k], ecols[k + 1] if k + 1 < n else None, last=(k == hi))
        if k in tset:
            b = e if (R16[0] >> k) & 1 else p.not_(e)
            if b[1] == 0: ok0 = p.and_(ok0, b)
            else: ok1 = p.and_(ok1, b)
    for j in range(31):
        e0_j = get_e0(j); e0_6 = get_e0((j + 6) % 32); e0_11 = get_e0((j + 11) % 32); e0_25 = get_e0((j + 25) % 32)
        ss = p.xor(p.xor(e0_6, e0_11), e0_25); cv = p.xor(FF[j], p.and_(e0_j, EF[j]))
        sa = p.xor(p.xor(a0[(j + 2) % 32], a0[(j + 13) % 32]), a0[(j + 22) % 32]); mj = p.and_(a0z[j], AB[j])
        cols[j].extend([K1[j], sa, mj, ss, cv])
        nw1 = reduce_col(p, cols[j], cols[j + 1] if j + 1 < 31 else None, last=(j == 30)); W1.append(p.not_(nw1))
        if 7 <= j <= 7 + min(hi, 13): k = j - 7; u[k] = p.xor(W1[k + 3], W1[k + 7])
        elif 21 <= j <= 7 + hi: k = j - 7; u[k] = p.xor(p.xor(W1[k - 14], W1[k + 3]), W1[k + 7])
        if 18 <= j <= 18 + min(hi, 13): k = j - 18; step_e16(k, p.xor(u.pop(k), W1[j]))
    for k in range(14, hi + 1): step_e16(k, u.pop(k))
    return p, p._mat(p.and_(ok0, ok1))

def schedule(p, root, nreg=64):
    """Belady allocation of the nodes root depends on, in creation order: instruction list [(op, dst, src...)] with 'ld' (input or spill
    slot), 'st' (spill), 'xor', 'and', 'or', 'not', 'out'; returns (instructions, spill slots used)."""
    if isinstance(root, tuple): root = p._mat(root)
    need = set(); st = [root]
    while st:
        x = st.pop()
        if x < 1 or x in need: continue
        need.add(x); n = p.nodes[x]
        if n[0] != 'in': st.extend(n[1:] if n[0] != 'not' else n[1:2])
    order = [x for x in range(1, len(p.nodes)) if x in need and p.nodes[x][0] != 'in']
    uses = {}
    for t, x in enumerate(order):
        n = p.nodes[x]
        for o in (n[1:] if n[0] != 'not' else n[1:2]):
            if o >= 1: uses.setdefault(o, []).append(t)
    uses.setdefault(root, []).append(len(order))
    ptr = {x: 0 for x in uses}
    def nxt(x):
        u = uses.get(x, []); i = ptr.get(x, 0)
        return u[i] if i < len(u) else 1 << 40
    reg = {}; free = list(range(nreg)); inmem = set(x for x in need if p.nodes[x][0] == 'in'); slots = {}; ins = []; maxslot = 0
    def evict(t, keep):
        nonlocal maxslot
        v = max((x for x in reg if x not in keep), key=lambda x: (x in inmem, nxt(x)))
        if nxt(v) < (1 << 40) and v not in inmem:
            if v not in slots: slots[v] = len(slots); maxslot = max(maxslot, len(slots))
            ins.append(('st', ('S', slots[v]), reg[v])); inmem.add(v)
        free.append(reg.pop(v))
    def getreg(t, keep):
        if not free: evict(t, keep)
        return free.pop()
    def load(x, t, keep):
        if x in reg: return reg[x]
        r = getreg(t, keep); src = ('I', p.nodes[x][1]) if p.nodes[x][0] == 'in' else ('S', slots[x])
        ins.append(('ld', r, src)); reg[x] = r; return r
    CONST = {0: 'Z', 1: 'O'}
    for t, x in enumerate(order):
        n = p.nodes[x]; ops = n[1:] if n[0] != 'not' else n[1:2]
        keep = set(o for o in ops if o >= 1)
        rs = [CONST[o] if o < 1 else load(o, t, keep) for o in ops]
        for o in ops:
            if o >= 1: ptr[o] += 1
        dead = [o for o in ops if o >= 1 and nxt(o) >= (1 << 40) and o in reg]
        if dead: r = reg.pop(dead[0]); [free.append(reg.pop(d)) for d in dead[1:] if d in reg]
        else: r = getreg(t, keep)
        ins.append((n[0], r) + tuple(rs)); reg[x] = r
    ins.append(('out', reg[root] if root >= 1 else CONST[root]))
    return ins, maxslot

def run_prog(ins, inputs):
    """execute an instruction list on 256-bit planes; inputs: name -> plane.  Returns (ok plane, executed instructions)."""
    R = {}; S = {}; v = lambda a: 0 if a == 'Z' else ONES if a == 'O' else R[a]
    for i in ins:
        op = i[0]
        if op == 'ld': R[i[1]] = inputs[i[2][1]] if i[2][0] == 'I' else S[i[2][1]]
        elif op == 'st': S[i[1][1]] = R[i[2]]
        elif op == 'xor': R[i[1]] = v(i[2]) ^ v(i[3])
        elif op == 'and': R[i[1]] = v(i[2]) & v(i[3])
        elif op == 'or': R[i[1]] = v(i[2]) | v(i[3])
        elif op == 'not': R[i[1]] = v(i[2]) ^ ONES
        elif op == 'out': return v(i[1]), len(ins) - 1
    raise ValueError('no out')
```

### a0p_scal.py

```python

# ---- counted scalar routines (proof.md Section 7.1) ----
# Machine: 256-bit word RAM; every executed primitive counts 1 (add, sub, and, or, xor, not, shl, shr, ld, st, li, rand), a compare-and-branch
# counts 2, one target compression counts 1 unit.  32-bit values are reduced with one AND where the program needs a masked value.  The
# routines below are written with the counting primitives of Mach and executed; broadcast, lane_value, first_lane, r16test, step_m and deep add
# itemised declared counts (stated in their docstrings) instead of counting each primitive (the `calibrate` command).
class Mach:
    def __init__(s): s.ops = 0; s.units = 0
    def op(s, v, n=1): s.ops += n; return v
    def add(s, a, b): return s.op((a + b) & M)
    def sub(s, a, b): return s.op((a - b) & M)
    def xor(s, a, b): return s.op(a ^ b)
    def and_(s, a, b): return s.op(a & b)
    def or_(s, a, b): return s.op(a | b)
    def shr(s, a, n): return s.op(a >> n)
    def ld(s, v): return s.op(v)
    def br(s, c): s.ops += 2; return c
def sg(m, x, r1, r2, r3, shr3):
    """ROTR(x,r1) ^ ROTR(x,r2) ^ (SHR or ROTR)(x,r3) of a masked 32-bit x: the doubled word D = x | x << 32 makes a rotation one shift; 8 ops"""
    m.op(0, 2)                                                       # D = x << 32, D |= x
    t = m.op(ror(x, r1) ^ ror(x, r2), 3); u = m.op((x >> r3) if shr3 else ror(x, r3), 1); return m.op((t ^ u) & M, 2)
def S0m(m, x): return sg(m, x, 2, 13, 22, False)
def S1m(m, x): return sg(m, x, 6, 11, 25, False)
def s0m(m, x): return sg(m, x, 7, 18, 3, True)
def s1m(m, x): return sg(m, x, 17, 19, 10, True)
def CHm(m, e, f, g): return m.xor(g, m.and_(e, m.xor(f, g)))                    # 3
def MAJm(m, a, b, c): return m.or_(m.and_(a, b), m.and_(c, m.or_(a, b)))       # 4

def w7test(m, c7, a):
    """W7 = c7 - A_{-1} in F7, computed (no table): s0(w + D7) - s0(w) = T7; 24 operations including the branch"""
    w = m.and_(m.sub(c7, a), M); w2 = m.and_(m.add(w, D7), M)
    d = m.and_(m.sub(s0m(m, w2), s0m(m, w)), M)
    return m.br(d == T7)

def fb_scalars(m, cv):
    """per first block: HH, AB, EF, FF, K1, KP of the program (Lemma 4.1, with A0_CONST = 0x380 and A0_ADD = 0x780 absorbed)"""
    a, b, c, d, e, f, g, h = cv
    ab0 = m.xor(a, b); anb = m.and_(a, b)
    sm = m.add(S0m(m, a), m.or_(anb, m.and_(c, ab0)))
    hh = m.and_(m.sub(m.add(d, A0_ADD), sm), M)
    kp = m.and_(m.sub(m.sub(m.sub(m.sub(KKP0, sm), h), S1m(m, e)), CHm(m, e, f, g)), M)
    k1 = m.and_(m.add(m.add(KK1_N, g), m.or_(anb, m.and_(ab0, A0_CONST))), M)
    return dict(HH=hh, AB=m.and_(ab0, ~A0_CONST & M), EF=m.xor(e, f), FF=f, K1=k1, KP=kp)
KK1 = (SAx[1] - K[1]) & M; KK1_N = (~KK1) & M                       # K1 = ~KK1 + g + ((a & b) | (0x380 & (a ^ b)))
KKP = (C16 + s1(PMX[14]) + PMX[9] + A0_ADD) & M; KKP0 = (KKP - K[0]) & M
PLANE_OPS = 4                                                       # one broadcast plane: shift, and, negate, store
KP_BITS = max(TBITS) + 1                                            # KP is only needed on bits 0..12
LV_MASK = 0x1fffff                                                  # bits 21..31 of a0 are constant within each 256-lane canonical batch

def broadcast(m, sc):
    """the 32 + 27 + 3 x 31 + 13 = 165 broadcast planes (plane j = 0 - ((x >> j) & 1)); 4 operations each (660 operations)"""
    out = {}; nplanes = 0
    for nm, v in sc.items():
        if nm == 'AB':
            for j in range(31):
                if (AB_MASK >> j) & 1: out['AB%d' % j] = ONES if (v >> j) & 1 else 0; nplanes += 1
            continue
        nb = KP_BITS if nm == 'KP' else 32 if nm == 'HH' else 31; nplanes += nb
        for j in range(nb): out['%s%d' % (nm, j)] = ONES if (v >> j) & 1 else 0
    m.ops += PLANE_OPS * nplanes; return out

def lane_value(m, planes, L, cmask, base):
    """a0 of lane L from the stored planes of the varying bits: per bit one shift, and, shift-left, or (4), plus the batch base (1)"""
    v = base
    for j in range(32):
        if (cmask >> j) & 1:
            v |= ((planes[j] >> L) & 1) << j
    m.ops += 4 * bin(cmask).count('1') + 1; return v

def first_lane(m, ok):
    """lowest set lane of a nonzero 256-bit word: binary search, 8 steps of (and, compare-and-branch, shift) = 32 operations"""
    m.ops += 32; return (ok & -ok).bit_length() - 1

def scalar_e16(m, sc, a0):
    """E16x of one variant (Lemma 4.1): ae = a0 - 0x780, E0, S0(a0), MAJ, S1(E0), CH, ~W1, s0(W1), E16x"""
    ae = m.sub(a0, A0_ADD)
    e0 = m.and_(m.add(ae, sc['HH']), M)
    mj = m.and_(a0, sc['AB'])
    ch = m.xor(sc['FF'], m.and_(e0, sc['EF']))
    nw1 = m.add(m.add(m.add(m.add(sc['K1'], S0m(m, a0)), mj), S1m(m, e0)), ch)
    return m.and_(m.add(m.add(sc['KP'], ae), s0m(m, m.xor(nw1, M))), M)

def r16test(m, e):
    """E16x in the 160-word row-16 set: binary search in the sorted table (8 steps of load, compare-and-branch, shift: 5 each) + 2"""
    m.ops += 8 * 5 + 2; return e in R16SET

def step_m(m, A, E, W, i):
    """one step of one member: 2 sigma (16), CH 3, MAJ 4, 9 additions/subtractions, 2 masks"""
    m.ops += 16 + 3 + 4 + 9 + 2
    E[i] = (A[i-4] + E[i-4] + S1(E[i-1]) + CH(E[i-1], E[i-2], E[i-3]) + K[i] + W[i]) & M
    A[i] = (E[i] - A[i-4] + S0(A[i-1]) + MAJ(A[i-1], A[i-2], A[i-3])) & M

def rowtest_m(m, tx, ty, i):
    """the accepted tests of row i (Section 6): per word (A, E, W) one xor and compare-and-branch for the difference and one and +
    compare-and-branch for the x-value bits (6 each, 18), the '+' pair (xor, and, branch: 4), per two-bit condition (2 shifts, xor, and,
    branch: 6)"""
    m.ops += 18 + (4 if PQ[i] and i != R19 else 0) + (6 * sum(1 for x in X2 if x[7] == i) if i != R19 else 0)
    return rowok(tx, ty, i)

def deep(m, cv, a0):
    """a row-16 pass: the words of both members (Step 2: 5 E words and 9 W words each, 13 operations per word), the expansion W16..W37
    (s0, s1, 3 additions, mask: 20 each), rows 16..37 of both members with the tests of rows 16..22 (early abort), the output comparison
    (8 xor, 7 or, branch).  Returns True iff the pair is in the accepted event."""
    wx, wy = words(cv, a0); m.ops += 2 * 14 * 13
    tx = trace(cv, wx); ty = trace(cv, wy)
    for i in range(16, 38):
        m.ops += 2 * 20 + 2 * 34
        if i <= 22 and not rowtest_m(m, tx, ty, i): return False
    m.ops += 8 + 7 + 2
    return all(tx[k][i] == ty[k][i] for k in (0, 1) for i in range(34, 38))
```

### a0p_run.py

```python

# ---- the online algorithm on one first block (proof.md Section 6) ----
def cbits(ci):
    """per-class program inputs: 'L' (a plane) on the class's independent mask bits, correlated planes on bits 11, 16, 22, 28, elsewhere constant"""
    c7, base, mk = CLASSES[ci]
    cb = ['L' if (mk >> j) & 1 else (base >> j) & 1 for j in range(32)]
    cb[11] = ('A10', 1); cb[22] = ('A21', 0); cb[28] = ('A27', 1 if (ci % 16) in (0, 2, 4, 6) else 0)
    if (ci % 16) in (8, 9, 10, 11): cb[16] = ('A1', 1)
    return cb
_PROG = {}
def program(ci=0):
    """the row-16 plane program of class ci (one per distinct mask and base bits outside it; constants folded)"""
    key = tuple(cbits(ci))
    if key not in _PROG:
        p, ok = build_e16(list(key), 256); _PROG[key] = schedule(p, ok)[0]
    return _PROG[key]
BATCH_CTL = 6          # per batch: ok test (compare-and-branch 2) and pointer advance, compare and branch (4)
CLASS_CTL = 3 + 4      # per passing class: setup 3 (batch pointer, end pointer, class constants) and end of class (work counter, cap test) 4
LANE_CTL = 3           # per passing lane: clear the lane (xor) and the loop test (compare-and-branch)
FB_FIXED = 30 + 5      # per first block: two random words and their 16 fields (30), counter, cap test and hit-list test (5)
W7_LOOP = 4            # per class: load c7, advance the class pointer, compare and branch

def batch_planes(mem):
    """the stored planes of a batch: plane j = bits j of the 256 variants (lane L = variant L), plus the batch base word"""
    d = {j: sum(((x >> j) & 1) << L for L, x in enumerate(mem)) for j in range(32)}
    d['base'] = mem[0] & ~LV_MASK & M; return d

def process_batch(m, ins, inp, planes, ci, cv, sc, found):
    """one batch of one passing class: the plane program, then every passing lane in scalar form; row-16 passes go to the deep check"""
    mk = CLASSES[ci][2]; lmk = mk & LV_MASK; b0 = planes['base'] | (CLASSES[ci][1] & ~mk & LV_MASK)
    for j in range(32):
        if (mk >> j) & 1: inp['A%d' % j] = planes[j]
    ok, n = run_prog(ins, inp); m.ops += n + BATCH_CTL
    while ok:
        L = first_lane(m, ok); ok &= ok - 1; m.ops += LANE_CTL
        a0 = lane_value(m, planes, L, lmk, b0)
        e = scalar_e16(m, sc, a0)
        if r16test(m, e) and deep(m, cv, a0): found.append(a0)
    return found

def process_fb(m, cv, batches_of, check=None):
    """one first block with chaining value cv: the W7 tests of all classes; for each passing class all its batches (batches_of(ci) yields
    the member lists).  Returns the accepted variants found.  check(ci, mem, ok-plane-recomputation) may verify lanes."""
    m.ops += FB_FIXED
    hits = []
    for ci, (c7, base, mk) in enumerate(CLASSES):
        m.ops += W7_LOOP
        if w7test(m, c7, cv[0]): hits.append(ci); m.ops += 2
    found = []
    if not hits: return found, hits
    sc = fb_scalars(m, cv); inp = broadcast(m, sc)
    for ci in hits:
        m.ops += CLASS_CTL; ins = program(ci)
        for mem in batches_of(ci):
            process_batch(m, ins, inp, batch_planes(mem), ci, cv, sc, found)
    return found, hits

# ---- organizer experiments (proof.md Section 13).  Randomness: SHAKE-256 of (experiment id | trial seed) ----
class Shake:
    def __init__(self, seed): self.seed = seed.encode(); self.k = 0; self.buf = b''; self.pos = 0
    def word(self):
        if self.pos + 32 > len(self.buf):
            self.buf = hashlib.shake_256(self.seed + b'|' + str(self.k).encode()).digest(1 << 14); self.k += 1; self.pos = 0
        v = int.from_bytes(self.buf[self.pos:self.pos + 32], 'little'); self.pos += 32; return v
    def u32(self): return self.word() & M
    def below(self, n): return self.word() % n

def vsample():
    return list(struct.unpack('<512I', zlib.decompress(base64.b64decode(VS_B64))))

def f7_sample(rng):
    """W7 uniform on F7 = {w : s0(w + D7) - s0(w) = T7}.  For D7 = 2^29, T7 = 03bff800 (P8): its three affine families (2^28, 2^24 and
    2^21 words; proof.md 5.1), the family drawn by rejection from its own word (shares 256, 16, 2 of 274; no modulo bias) and the value
    bits from a fresh word (selector and value independent; the fix of 08be594).  Any other (D7, T7): rejection on the definition."""
    if D7 != 1 << 29 or T7 != 0x03bff800:
        while True:
            w = rng.u32()
            if inF7(w): return w
    while True:
        r = rng.u32() >> 23                                             # 9 bits; accept r < 274
        if r < 274: break
    w = rng.u32()
    b = lambda x, j: (x >> j) & 1
    def setb(x, j, v): return (x & ~(1 << j)) | (v << j)
    if r < 256: w = setb(w, 29, 0)
    elif r < 272: w = setb(setb(w, 29, 1), 30, 0)
    else: w = setb(setb(w, 29, 1), 30, 1)
    w = setb(w, 18, b(w, 14) ^ 1); w = setb(w, 25, b(w, 8) ^ 1); w = setb(w, 12, b(w, 1))
    if r >= 256:
        w = setb(w, 19, b(w, 15) ^ 1); w = setb(w, 26, b(w, 9) ^ 1); w = setb(w, 13, b(w, 2))
    if r >= 272:
        w = setb(w, 20, b(w, 16) ^ b(w, 31) ^ 1); w = setb(w, 27, b(w, 10) ^ b(w, 31) ^ 1); w = setb(w, 14, b(w, 3) ^ b(w, 31))
        w = setb(w, 18, b(w, 14) ^ 1)
    return w

def step_row(A, E, W, i):
    E[i] = (A[i-4] + E[i-4] + S1(E[i-1]) + CH(E[i-1], E[i-2], E[i-3]) + K[i] + W[i]) & M
    A[i] = (E[i] - A[i-4] + S0(A[i-1]) + MAJ(A[i-1], A[i-2], A[i-3])) & M

def erow_plan(i, cm, pq):
    """bits of E_i imposed on a row-i proposal: x-value cells, '+' pairs, two-bit conditions with an earlier E row (prev) and inside E_i
    (inner), each imposed once from a bit fixed before it (as in vt38n.py)"""
    imp = cm | pq; prev = []; inner = []
    for (k1, i1, b1, eq, k2, i2, b2, row) in X2:
        if row != i or k1 != 1 or k2 != 1 or i2 != i: continue
        fl = 0 if eq else 1
        if i1 < i:
            if not (imp >> b2) & 1: prev.append((i1, b1, b2, fl)); imp |= 1 << b2
        elif not (imp >> b2) & 1: inner.append((b1, b2, fl)); imp |= 1 << b2
        elif not (imp >> b1) & 1: inner.append((b2, b1, fl)); imp |= 1 << b1
    done = cm | pq | sum(1 << b2 for (_, _, b2, _) in prev); out = []; todo = list(inner)
    while todo:
        nx = [t for t in todo if (done >> t[0]) & 1 or not any(u[1] == t[0] for u in todo)]
        if not nx: imp &= ~sum(1 << t[1] for t in todo); break
        for t in nx: out.append(t); done |= 1 << t[1]; todo.remove(t)
    return imp, prev, out

NP_R, CH_R, NT_R = 64, (64, 8, 8, 4, 2, 1), 192
P19F = 1 << 18; P19A = ((10, 28), (11, 29)); P19B = ((5, 10),)   # the row-19 pattern flips: A = E19[18], conditions 6 and 7; B = condition 11
def smc_replicate(rng, VS):
    """one replicate of the estimator of q3 for the accepted event: row 16 exact (the 160 W16 words), rows 17..22 by proposals of E_i^x
    with the row's E bits imposed (row 19: only its difference bits), tail: a variant of the sample, W7 uniform in F7, rows 23..37,
    output comparison.  Returns (log2 estimate or None, accepted pairs, failed rebuilds)."""
    lg = [math.log2(len(GL)) - 32]; P = []
    for _ in range(NP_R):
        w = GL[rng.below(len(GL))]; st = []
        for (SA, SE, wp, dw) in ((SAx, SEx, PMX, 0), (SAy, SEy, PMY, DWT[16])):
            A = dict(SA); E = dict(SE); W = {i: wp[i] for i in range(16)}; W[16] = (w + dw) & M; step_row(A, E, W, 16); st += [A, E, W]
        P.append(st)
    for i in range(17, 23):
        cm, cvv, d, _ = CELLS[1][i]; pq = PQ[i] & ~cm
        imp, prev, inner = erow_plan(i, cm, pq); f = bin(imp).count('1'); Mi = CH_R[i - 17]; surv = []
        if i == R19:                     # one of the four row-19 patterns (proof.md 6.1), drawn uniformly: weight 4 x 2^-f
            f -= 2; inners = []
            for fa, fb in ((0, 0), (0, 1), (1, 0), (1, 1)):
                fl = {(b1, b2) for b1, b2 in (P19A if fa else ()) + (P19B if fb else ())}
                inners.append(([(bs, bd, x ^ ((bs, bd) in fl or (bd, bs) in fl)) for (bs, bd, x) in inner], cvv ^ (P19F if fa else 0)))
        for (Ax, Ex, Wx, Ay, Ey, Wy) in P:
            rx = (Ax[i-4] + Ex[i-4] + S1(Ex[i-1]) + CH(Ex[i-1], Ex[i-2], Ex[i-3]) + K[i]) & M
            for _ in range(Mi):
                inn, cv0 = inners[rng.below(4)] if i == R19 else (inner, cvv)
                fixed = cv0 | (Ex[i-1] & pq)
                for (i1, b1, b2, fl) in prev: fixed |= (((Ex[i1] >> b1) & 1) ^ fl) << b2
                e = (rng.u32() & ~imp & M) | fixed
                for (bs, bd, fl) in inn: e = (e & ~(1 << bd)) | (((e >> bs) & 1) ^ fl) << bd
                Wxi = (e - rx) & M
                nA = dict(Ax); nE = dict(Ex); nW = dict(Wx); mA = dict(Ay); mE = dict(Ey); mW = dict(Wy)
                nW[i] = Wxi                                          # W_i^y = W_i^x + the schedule difference (W0..W6 carry none)
                mW[i] = (Wxi + s1(mW[i-2]) - s1(nW[i-2]) + mW[i-7] - nW[i-7] + (T7 if i == 22 else s0(mW[i-15]) - s0(nW[i-15]))) & M
                step_row(nA, nE, nW, i); step_row(mA, mE, mW, i)
                if nE[i] == e and rowok((nA, nE, nW), (mA, mE, mW), i): surv.append((nA, nE, nW, mA, mE, mW))
        if not surv: return None, [], 0
        lg.append(math.log2(len(surv) / (len(P) * Mi)) - f)
        P = [surv[rng.below(len(surv))] for _ in range(NP_R)]
    pairs = []; bad = 0; succ = 0
    Kt = K
    for (Ax, Ex, Wx, Ay, Ey, Wy) in P:
        bx = [Ax[18], Ax[19], Ax[20], Ax[21], Ax[22], Ex[18], Ex[19], Ex[20], Ex[21], Ex[22]]
        by = [Ay[18], Ay[19], Ay[20], Ay[21], Ay[22], Ey[18], Ey[19], Ey[20], Ey[21], Ey[22]]
        wxb = [Wx[i] for i in range(23)]; wyb = [Wy[i] for i in range(23)]
        for _ in range(NT_R):
            a0 = VS[rng.below(len(VS))]
            w7 = f7_sample(rng)
            w8 = (W8C[0] - ((a0 + C4) & M)) & M
            ok = True; outs = []
            for (b0, wb, d7, d8) in ((bx, wxb, 0, 0), (by, wyb, D7, D8)):
                W = list(wb); W[7] = (w7 + d7) & M; W[8] = (w8 + d8) & M
                a4, a3, a2, a1, a = b0[0], b0[1], b0[2], b0[3], b0[4]; e4, e3, e2, e1, e = b0[5], b0[6], b0[7], b0[8], b0[9]
                for i in range(23, NR):                          # the step and expansion inlined; a3 = A[i-4], a = A[i-1]
                    x = W[i-2]; y = W[i-15]; d = (x | x << 32); z = (y | y << 32)
                    w = ((((d >> 17) ^ (d >> 19)) & M ^ (x >> 10)) + W[i-7] + (((z >> 7) ^ (z >> 18)) & M ^ (y >> 3)) + W[i-16]) & M; W.append(w)
                    d = e | e << 32; ne = (a3 + e3 + ((d >> 6) ^ (d >> 11) ^ (d >> 25)) + ((e & e1) ^ (~e & e2)) + Kt[i] + w) & M
                    d = a | a << 32; na = (ne - a3 + ((d >> 2) ^ (d >> 13) ^ (d >> 22)) + ((a & a1) ^ (a & a2) ^ (a1 & a2))) & M
                    a4, a3, a2, a1, a = a3, a2, a1, a, na; e4, e3, e2, e1, e = e3, e2, e1, e, ne
                outs.append((a, a1, a2, a3, e, e1, e2, e3))
            if outs[0] == outs[1]:
                succ += 1; cv, wx, wy = rebuild({i: (wxb[i] if i > 8 else w7 if i == 7 else w8) for i in range(7, 23)}, a0)
                tx, ty = trace(cv, wx), trace(cv, wy)
                if compress(cv, wx) == compress(cv, wy) and wx != wy and accepted(tx, ty) and inF7(wx[7]) and wx[7] == w7: pairs.append((cv, wx, wy, a0))
                else: bad += 1
    if succ == 0: return None, pairs, bad
    lg.append(math.log2(succ / (NP_R * NT_R))); return sum(lg), pairs, bad
```

### a0p_main.py

```python

Q3_REPS = 10
ONLINE_TRIALS = 8
UNCOND_FB = 64          # per active online trial: unconditional first blocks whose class W7 passes are counted (H1)
Q3_THRESH = -98.6       # log2 threshold of the pooled mean of the 10 replicates (fixed from 48 development requests before any validation run)

def class_of(a0):
    c = c7of(a0)
    for ci, (c7, base, mk) in enumerate(CLASSES):
        if c == c7 and in_G(a0) and (a0 ^ base) & ~mk & M == 0: return ci
    return None

def q3_experiment(req):
    VS = vsample(); out = []; est = []; allok = True; last = None
    for tr in req['trials']:
        t = tr['trial']; rec = dict(trial=t, message_a_hex=None, message_b_hex=None)
        if t < Q3_REPS:
            z, pairs, bad = smc_replicate(Shake(req['experiment_id'] + '|' + tr['seed']), VS)
            est.append(z); allok = allok and bad == 0
            rec['observations'] = dict(log2_estimate=z if z is not None else -1000.0, accepted_pairs=len(pairs), failed_rebuilds=bad)
            if pairs:
                cv, mx, my, a0 = pairs[0]; last = pairs[0]
                rec['message_a_hex'] = struct.pack('>24I', *(cv + mx)).hex(); rec['message_b_hex'] = struct.pack('>24I', *(cv + my)).hex()
        elif t == Q3_REPS and len(est) == Q3_REPS:
            mean = sum(2.0 ** z for z in est if z is not None) / Q3_REPS; lz = math.log2(mean) if mean > 0 else -1000.0
            rec['observations'] = dict(log2_pooled_mean=lz)
            if allok and Q3_THRESH is not None and lz >= Q3_THRESH and last:
                cv, mx, my, a0 = last
                rec['message_a_hex'] = struct.pack('>24I', *(cv + mx)).hex(); rec['message_b_hex'] = struct.pack('>24I', *(cv + my)).hex()
        out.append(rec)
    return dict(schema_version=1, trials=out)

def online_experiment(req):
    """the counted online program on organizer-seeded first blocks (real compressions): first UNCOND_FB first blocks are drawn and the W7
    passes of all classes counted without any selection (H1: expected UNCOND_FB x len(CLASSES) x |F7| / 2^32); then first blocks are drawn until one has a passing
    class (at most 64); its first passing class is run on two batches (the class's first 512 members) and every lane is compared with
    the scalar definition (E16x from the Step-2 words and the 38-step trace); trial 0 also runs the batch of the semi-free-start pair's
    variant on its chaining value and requires the counted program to find and accept it"""
    out = []
    for tr in req['trials']:
        rng = Shake(req['experiment_id'] + '|' + tr['seed']); rec = dict(trial=tr['trial'], message_a_hex=None, message_b_hex=None)
        if tr['trial'] >= ONLINE_TRIALS: out.append(rec); continue          # trials 8..255 return no pair by design
        un = 0                                                             # H1: unconditional first blocks, before any selection
        for k in range(UNCOND_FB):
            r0, r1 = rng.word(), rng.word()
            cv = compress(IV, [(r0 >> (32 * q)) & M for q in range(8)] + [(r1 >> (32 * q)) & M for q in range(8)])
            un += sum(1 for c7, b, mk in CLASSES if inF7((c7 - cv[0]) & M))
        for k in range(64):
            r0, r1 = rng.word(), rng.word()
            M0 = [(r0 >> (32 * q)) & M for q in range(8)] + [(r1 >> (32 * q)) & M for q in range(8)]
            cv = compress(IV, M0); m = Mach()
            hits = [ci for ci, (c7, b, mk) in enumerate(CLASSES) if inF7((c7 - cv[0]) & M)]
            if hits: break
        bad = 0; lanes = 0; passed = 0
        if hits:
            ci = hits[0]; mem = members(ci, 512)
            sc = fb_scalars(m, cv); inp = broadcast(m, sc); ins = program(ci); mk = CLASSES[ci][2]
            for b in range(2):
                bm = mem[256 * b:256 * b + 256]; planes = batch_planes(bm)
                for j in range(32):
                    if (mk >> j) & 1: inp['A%d' % j] = planes[j]
                ok, n = run_prog(ins, inp)
                for L, a0 in enumerate(bm):
                    wx = words(cv, a0)[0]; e = trace(cv, wx, 17)[1][16]
                    want = all(((e >> j) & 1) == ((R16[0] >> j) & 1) for j in TBITS)
                    bad += want != bool((ok >> L) & 1) or wx[7] != (CLASSES[ci][0] - cv[0]) & M or not inF7(wx[7]); lanes += 1; passed += want
            if not bad:
                wx, wy = words(cv, mem[0])
                rec['message_a_hex'] = struct.pack('>32I', *(M0 + wx)).hex(); rec['message_b_hex'] = struct.pack('>32I', *(M0 + wy)).hex()
        if tr['trial'] == 0:                                               # positive lanes: the batch of the semi-free-start pair's variant
            ci = class_of(A0S); mem = members(ci, 256, 78 * 256)
            m2 = Mach(); sc2 = fb_scalars(m2, PCV); inp2 = broadcast(m2, sc2); fnd = []
            process_batch(m2, program(ci), inp2, batch_planes(mem), ci, PCV, sc2, fnd); bad += A0S not in fnd
        rec['observations'] = dict(uncond_first_blocks=UNCOND_FB, uncond_class_passes=un, first_blocks=k + 1, passing_classes=len(hits), lanes=lanes, stage3a_passes=passed, mismatches=bad)
        out.append(rec)
    return dict(schema_version=1, trials=out)

def calibrate():
    """the executed counts used by the ledger (proof.md Section 7)"""
    import random
    rr = random.Random(9); m = Mach(); cv = [rr.getrandbits(32) for _ in range(8)]
    w7 = []
    for _ in range(200): m = Mach(); w7test(m, rr.getrandbits(32), rr.getrandbits(32)); w7.append(m.ops)
    m = Mach(); sc = fb_scalars(m, cv); n_sc = m.ops; m = Mach(); broadcast(m, sc); n_bc = m.ops
    m = Mach(); a0 = members(0, 1)[0]; lane_value(m, {j: 0 for j in range(32)}, 0, max((c[2] & LV_MASK for c in CLASSES), key=lambda x: bin(x).count('1')), 0); n_lv = m.ops
    m = Mach(); scalar_e16(m, sc, a0); n_e16 = m.ops
    m = Mach(); deep(m, PCV, A0S); n_deep = m.ops
    progs = [len(program(ci)) - 1 for ci in range(len(CLASSES))]
    return dict(prog=progs, w7=max(w7), fb_fixed=FB_FIXED, w7_loop=W7_LOOP, scalars=n_sc, planes=n_bc, batch_ctl=BATCH_CTL,
                class_ctl=CLASS_CTL, lane=32 + LANE_CTL + n_lv + n_e16 + 42, deep=n_deep, tk=TK, classes=len(CLASSES), class_size=CLASS_SIZE)

def selftest():
    import random
    rr = random.Random(5); ok = True
    def chk(name, cond, extra=''):
        nonlocal ok; ok = ok and bool(cond); print('%-70s %s %s' % (name, 'ok' if cond else 'FAIL', extra), flush=True)
    tx, ty = trace(PCV, PMX), trace(PCV, PMY)
    chk('1 the semi-free-start pair collides, M != M\', accepted event, W7 in F7', compress(PCV, PMX) == compress(PCV, PMY) and PMX != PMY and accepted(tx, ty) and inF7(PMX[7]))
    chk('  its variant A0 is in G and in a selected class', in_G(A0S) and class_of(A0S) is not None, '(class %s)' % class_of(A0S))
    def g16(w):
        A = dict(SAx); E = dict(SEx); W = {i: PMX[i] for i in range(16)}; B = dict(SAy); F = dict(SEy); V = {i: PMY[i] for i in range(16)}
        W[16] = w; V[16] = (w + DWT[16]) & M; step_row(A, E, W, 16); step_row(B, F, V, 16)
        return rowok((A, E, W), (B, F, V), 16)
    cand = list(GL) + [rr.getrandbits(32) for _ in range(20000)] + [g ^ (1 << b) for g in GL[:40] for b in range(32)]
    gs = set(GL); chk('2 row 16: the 160 W16 words hold it; 20,000 random words and 1,280 neighbours agree', all(g16(w) == (w in gs) for w in cand))
    bad = 0
    for _ in range(20):
        cv = [rr.getrandbits(32) for _ in range(8)]; ci = rr.randrange(len(CLASSES)); a0 = members(ci, 1, rr.randrange(40))[0]
        wx, wy = words(cv, a0); t = trace(cv, wx, 17); u = trace(cv, wy, 17); m = Mach(); sc = fb_scalars(m, cv)
        bad += scalar_e16(m, sc, a0) != t[1][16] or wx[7] != (CLASSES[ci][0] - cv[0]) & M or not all(rowok(t, u, i) for i in range(11, 16))
        bad += any(((wy[i] - wx[i]) & M) != DWT[i] for i in range(16))
    chk('3 Lemma 4.1: E16x formula, W7 = c7 - A_-1, rows 11..15 and the word differences on 20 chaining values', bad == 0)
    from collections import Counter
    cnt = [(len(p) - 1, Counter(i[0] for i in p)) for p in (program(ci) for ci in range(len(CLASSES)))]
    chk('4 row-16 programs (one per class): instructions mean / max, loads, spill stores', True, '%.2f / %d (loads %d..%d, stores %d..%d)' % (
        sum(n for n, _ in cnt) / len(cnt), max(n for n, _ in cnt), min(c['ld'] for _, c in cnt), max(c['ld'] for _, c in cnt), min(c['st'] for _, c in cnt), max(c['st'] for _, c in cnt)))
    r = online_experiment(dict(experiment_id='a0p-online-r38', trials=[dict(trial=t, seed='%064x' % t) for t in range(2)]))
    chk('  program against the definition on 2 x 512 lanes of real first blocks', all(t['observations']['mismatches'] == 0 for t in r['trials']), str([t['observations'] for t in r['trials']]))
    ci = class_of(A0S); mem = members(ci, 256, 78 * 256); found = []
    m = Mach(); sc = fb_scalars(m, PCV); inp = broadcast(m, sc); process_batch(m, program(ci), inp, batch_planes(mem), ci, PCV, sc, found)
    chk('5 the counted program finds the semi-free-start pair in its batch', A0S in found, '(%d operations)' % m.ops)
    z, pairs, bad = smc_replicate(Shake('selftest'), vsample())
    chk('6 replicate: estimate, accepted pairs rebuilt and verified, failed rebuilds 0', bad == 0, '(log2 %s, %d pairs)' % (None if z is None else round(z, 3), len(pairs)))
    print('   calibrate:', calibrate())
    print('SELFTEST', 'PASSED' if ok else 'FAILED'); return ok

def run_request(req): return online_experiment(req) if 'online' in req['experiment_id'] else q3_experiment(req)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'selftest': sys.exit(0 if selftest() else 1)
    if len(sys.argv) > 1 and sys.argv[1] == 'calibrate': print(json.dumps(calibrate())); sys.exit(0)
    sys.stdout.write(json.dumps(run_request(json.loads(sys.stdin.read())), separators=(',', ':')))
```

### mka0p.py

```python
"""mka0p.py <sha2-search dir> <out.py> [selection dir] [tables .py] [sfs pair .json]: assemble experiments/a0p38.py from its parts with the
constants of one characteristic (own code). Defaults: P8. The selection dir is lp_classes.py output (derived.json, classes.txt, vars_pool.txt)."""
import sys, json, re, os
R, OUT = sys.argv[1], sys.argv[2]; parts = ['a0p_ref.py', 'a0p_core.py', 'a0p_prog.py', 'a0p_scal.py', 'a0p_run.py', 'a0p_main.py']
SEL = sys.argv[3] if len(sys.argv) > 3 else None
TAB = sys.argv[4] if len(sys.argv) > 4 else R + '/runs/vt/consts_p08.py'
C = open(TAB).read().split('\n')
keep = [l for l in C if l.startswith(('PCV', 'PMX', 'PMY', '_CH', 'PQ', 'X2', 'GL'))]
sfs = sys.argv[5] if len(sys.argv) > 5 else R + '/runs/c/P08.sfs_pair.json'
try:
    P = json.load(open(sfs)); keep = [l for l in keep if not l.startswith(('PCV', 'PMX', 'PMY'))] + ['PCV = %s' % P['cv'], 'PMX = %s' % P['M'], 'PMY = %s' % P['M2'], 'A0S = 0x%08x' % P['a0']]
except FileNotFoundError: pass
if SEL:
    DV = json.load(open(SEL + '/derived.json')); cls = [l.split() for l in open(SEL + '/classes.txt')]; pool = SEL + '/vars_pool.txt'
    keep += ['MASK = 0x%s' % DV['MASK'], 'T7_C = 0x%s' % DV['T7'], 'CBITS_C = 0x%s' % DV['CBITS'], 'CLASS_SIZE = %d' % DV['class_size']]
else:
    cls = [l.split() for l in open(R + '/runs/p08_classes.txt')]; pool = R + '/runs/vars_p08_pool.txt'
    keep += ['MASK = 0x7fe96c7c', 'T7_C = 0x03bff800', 'CBITS_C = 0x80041002', 'CLASS_SIZE = 24576']
import random, struct as _st, zlib as _z, base64 as _b
_pool = [int(l.split()[1], 16) for l in open(pool)]
_vs = random.Random(20261014).sample(_pool, 512)
keep.append("VS_B64 = '%s'" % _b.b64encode(_z.compress(_st.pack('<512I', *_vs), 9)).decode())
_gm = [l for l in keep if l.startswith('MASK = ')][0].split()[-1]
keep.append('CLASSES = [%s]' % ', '.join('(0x%s, 0x%s, 0x%s)' % (r[0], r[1], r[3] if len(r) > 3 else _gm[2:]) for r in cls))
src = ''.join(open(R + '/m38/' + p).read() for p in parts).replace('#<<CONSTS>>', '\n'.join(keep))
open(OUT, 'w').write(src); print('bytes', len(src.encode()))
```

### mkvt.py

```python
#!/usr/bin/env python3
"""mkvt.py - constants of the NEW3 instantiation of the variant-table program (own code).
Reads the NEW3 data files and writes the constants block of experiments/vt38n.py: the dense pair S*, the semi-free-start pair,
the trail cells of rows 0..37 (mask, x-value, x^y difference, 0) with the fixed-bit conditions merged in, the '+' pairs PQ
(E_i[b] = E_{i-1}[b]), the remaining two-bit conditions X2, the variant-validity conditions VC, G, the 64 A0 values, the A2
list, 512 sampled variants and one valid variant per A0. Usage: mkvt.py <sha2-search dir> <out.py>"""
import sys, json, struct, zlib, base64, os
R = sys.argv[1]; OUT = sys.argv[2]
PRE = sys.argv[3] if len(sys.argv) > 3 else R + '/runs/c/NEW3'   # characteristic prefix (char.json, .dat, .var.dat, .pair.json)
SFS = sys.argv[4] if len(sys.argv) > 4 else R + '/runs/c/NEW3.sfs_pair.json'
M = 0xffffffff
char = {int(k): v for k, v in json.load(open(PRE + '.char.json')).items()}
pair = json.load(open(PRE + '.pair.json')); sfs = json.load(open(SFS)) if os.path.exists(SFS) else dict(cv=pair['cv'], M=pair['Wx'], M2=pair['Wy'])
KI = {'A': 0, 'E': 1, 'W': 2}

def trail(row):
    m = sum(1 << (31 - k) for k, c in enumerate(row) if c in 'un'); x = sum(1 << (31 - k) for k, c in enumerate(row) if c == 'u')
    return m, x

CELL = [[[0, 0, 0] for _ in range(38)] for _ in range(3)]          # mask, x-value, difference
for i in range(38):
    for k, kk in KI.items():
        m, x = trail(char.get(i, {k: '=' * 32})[k]); CELL[kk][i] = [m, x, m]
# conditions: rows >= 16 from the q3 data file (keyed), dense-part validity from the variant data file (key = largest row)
def parse(fn, keyed):
    out = []
    for l in open(fn):
        t = l.split()
        if not t or t[0] != 'COND': continue
        if keyed: key, n = int(t[1]), int(t[2]); rest = t[3:]
        else: n = int(t[1]); rest = t[2:]; key = None
        refs = [tuple(int(v) for v in rest[3 * q:3 * q + 3]) for q in range(n)]; al = int(rest[3 * n], 16)
        out.append((key if keyed else max(r[1] for r in refs), refs, al))
    return out
TAIL = parse(PRE + '.dat', True); DENSE = parse(PRE + '.var.dat', False)
PQ = [0] * 38; X2 = []
def fix(k, i, b, v):
    m, x, d = CELL[k][i]
    if (m >> b) & 1: assert ((x >> b) & 1) == v, ('conflicting fixed bit', k, i, b)
    CELL[k][i] = [m | 1 << b, (x & ~(1 << b)) | v << b, d]
for key, refs, al in TAIL + DENSE:
    ok = [idx for idx in range(1 << len(refs)) if (al >> idx) & 1]
    if len(refs) == 1:
        assert len(ok) == 1; fix(*refs[0], ok[0]); continue
    assert len(refs) == 2, refs
    b0 = {idx & 1 for idx in ok}; b1 = {idx >> 1 for idx in ok}
    if len(ok) == 2 and (len(b0) == 1 or len(b1) == 1):            # one operand fixed, the other free
        if len(b0) == 1: fix(*refs[0], b0.pop())
        else: fix(*refs[1], b1.pop())
        continue
    if len(ok) == 1: fix(*refs[0], ok[0] & 1); fix(*refs[1], ok[0] >> 1); continue
    assert sorted(ok) in ([0, 3], [1, 2]), (refs, al)
    eq = 1 if sorted(ok) == [0, 3] else 0
    (k1, i1, c1), (k2, i2, c2) = sorted(refs, key=lambda r: (r[1], r[0], r[2]))
    if k1 == k2 == 1 and c1 == c2 and i2 == i1 + 1 and eq: PQ[i2] |= 1 << c1; continue
    X2.append((k1, i1, c1, eq, k2, i2, c2, key))
_g = open(PRE + '.dat.g16', 'rb').read(); G = list(struct.unpack('<%dI' % (len(_g) // 4), _g))
NEW3 = PRE.endswith('NEW3')
if NEW3:
    A0 = [int(x, 16) for x in open(R + '/runs/a0_selected64.txt').read().split()]
    pool = [l.split() for l in open(R + '/runs/vars_new3_pool.txt')]
    A2 = sorted({int(t[3], 16) for t in pool}); assert len(A2) == 1408, len(A2)
    A2I = {a: k for k, a in enumerate(A2)}
    samp = [l.split() for l in open(R + '/runs/vars_new3_s17.txt')][:512]
    S512 = b''.join(struct.pack('<BIH', int(t[0]), int(t[2], 16), A2I[int(t[3], 16)]) for t in samp)
    ent = {}
    for t in pool:
        j = int(t[0]); ent.setdefault(j, (int(t[2], 16), A2I[int(t[3], 16)]))
    assert len(ent) == 64
    E64 = b''.join(struct.pack('<IH', *ent[j]) for j in range(64))
b64 = lambda b: base64.b64encode(zlib.compress(b, 9)).decode()
_CH = [{i: (CELL[k][i][0], CELL[k][i][1], CELL[k][i][2], 0) for i in range(38) if CELL[k][i][0]} for k in range(3)]
o = []
o.append('PCV = %s' % [w for w in pair['cv']]); o.append('PMX = %s' % pair['Wx']); o.append('PMY = %s' % pair['Wy'])
o.append('SFS_CV = %s' % sfs['cv']); o.append('SFS_MX = %s' % sfs['M']); o.append('SFS_MY = %s' % sfs['M2'])
o.append('_CH = %r' % _CH)
o.append('PQ = %r' % PQ); o.append('X2 = %r' % X2)
o.append('VC = %r' % [(refs, al) for key, refs, al in DENSE])
o.append('GL = %r' % G)
if NEW3:
    o.append("A0_B64 = '%s'" % b64(struct.pack('<64I', *A0))); o.append("A2_B64 = '%s'" % b64(struct.pack('<1408I', *A2)))
    o.append("S512_B64 = '%s'" % b64(S512)); o.append("E64_B64 = '%s'" % b64(E64))
open(OUT, 'w').write('\n'.join(o) + '\n')
print('cells', sum(len(c) for c in _CH), 'PQ rows', [i for i in range(38) if PQ[i]], 'X2', len(X2), 'VC', len(DENSE), 'G', len(G))
for x in X2: print('  X2', x)
```

### a0fam.c

```c
// A0-only variant family of a dense part and its c7 classes (own code). a0fam <pair: cv Wx[16] Wy[16] hex> [min class size, out file]
// a0cls: the same in 16 passes over the top four bits of c7 (at most about 2^22.1 pairs resident; peak memory measured in proof.md 11).
// A variant changes A0 only (both members): E4 and W8 of each member change; valid iff the modular difference dW8 and the
// s0 difference ds0(W8) equal the pair's (W8 enters rows >= 16 only through them). c7 = W7^x + A_{-1} depends on A0 through
// MAJ(A2, A1, A0) and CH(E6, E5, E4). Prints the family size, the number of distinct c7 values and the largest class sizes.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
typedef uint32_t u32;
static const u32 K[16] = {0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174};
static inline u32 ror(u32 x, int n) { return (x >> n) | (x << (32 - n)); }
static inline u32 S0(u32 x) { return ror(x, 2) ^ ror(x, 13) ^ ror(x, 22); }
static inline u32 S1(u32 x) { return ror(x, 6) ^ ror(x, 11) ^ ror(x, 25); }
static inline u32 s0(u32 x) { return ror(x, 7) ^ ror(x, 18) ^ (x >> 3); }
static inline u32 CH(u32 x, u32 y, u32 z) { return (x & y) ^ (~x & z); }
static inline u32 MAJ(u32 x, u32 y, u32 z) { return (x & y) ^ (x & z) ^ (y & z); }
static u32 A[2][20], E[2][20], W[2][16];
static int cmp(const void *a, const void *b) { u32 x = *(const u32 *)a, y = *(const u32 *)b; return x < y ? -1 : x > y; }
static int cmp64(const void *a, const void *b) { uint64_t x = *(const uint64_t *)a, y = *(const uint64_t *)b; return x < y ? -1 : x > y; }
static int cmpl(const void *a, const void *b) { long x = *(const long *)a, y = *(const long *)b; return x > y ? -1 : x < y; }   // descending
int main(int argc, char **argv) {
    FILE *f = fopen(argv[1], "r"); u32 cv[8];
    for (int j = 0; j < 8; j++) fscanf(f, "%x", &cv[j]);
    for (int m = 0; m < 2; m++) for (int i = 0; i < 16; i++) fscanf(f, "%x", &W[m][i]);
    fclose(f);
    for (int m = 0; m < 2; m++) {
        for (int j = 0; j < 4; j++) { A[m][3 - j] = cv[j]; E[m][3 - j] = cv[4 + j]; }
        for (int i = 0; i < 16; i++) {
            u32 T1 = E[m][i] + S1(E[m][i + 3]) + CH(E[m][i + 3], E[m][i + 2], E[m][i + 1]) + K[i] + W[m][i];
            E[m][i + 4] = A[m][i] + T1; A[m][i + 4] = T1 + S0(A[m][i + 3]) + MAJ(A[m][i + 3], A[m][i + 2], A[m][i + 1]);
        }
    }
#define a(m, i) A[m][(i) + 4]
#define e(m, i) E[m][(i) + 4]
    u32 dW8 = W[1][8] - W[0][8], ds8 = s0(W[1][8]) - s0(W[0][8]);
    u32 *c7 = malloc(sizeof(u32) << 28); uint64_t *pr = malloc(sizeof(uint64_t) << 27); long n = 0;
    for (uint64_t x = 0; x < (1ULL << 32); x++) {
        u32 a0 = (u32)x, w8[2], e4 = 0;
        for (int m = 0; m < 2; m++) {
            e4 = a(m, 4) + a0 - S0(a(m, 3)) - MAJ(a(m, 3), a(m, 2), a(m, 1));
            w8[m] = e(m, 8) - a(m, 4) - e4 - S1(e(m, 7)) - CH(e(m, 7), e(m, 6), e(m, 5)) - K[8];
        }
        if (w8[1] - w8[0] != dW8 || s0(w8[1]) - s0(w8[0]) != ds8) continue;
        u32 c = e(0, 7) - 2 * a(0, 3) + S0(a(0, 2)) + MAJ(a(0, 2), a(0, 1), a0) - S1(e(0, 6)) - CH(e(0, 6), e(0, 5), e4) - K[7];
        if (n < (1L << 27)) { c7[n] = c; pr[n] = ((uint64_t)c << 32) | a0; } n++;
    }
    printf("family %ld = 2^%.3f\n", n, log2((double)n));
    if (argc > 2) {   // dump members of classes with size >= argv[2]
        long m = n < (1L << 27) ? n : (1L << 27); int thr = atoi(argv[2]);
        qsort(pr, m, 8, cmp64);
        FILE *o = fopen(argv[3], "w");
        for (long i = 0; i < m; ) { long j = i; while (j < m && (pr[j] >> 32) == (pr[i] >> 32)) j++; if (j - i >= thr) for (long k = i; k < j; k++) fprintf(o, "%08x %08x\n", (u32)(pr[k] >> 32), (u32)pr[k]); i = j; }
        fclose(o);
    }
    if (n > (1L << 28)) n = 1L << 28;
    qsort(c7, n, 4, cmp);
    long *sz = malloc(sizeof(long) * (n + 1)); long nc = 0;
    for (long i = 0; i < n; ) { long j = i; while (j < n && c7[j] == c7[i]) j++; sz[nc++] = j - i; i = j; }
    qsort(sz, nc, sizeof(long), cmpl);
    printf("distinct c7 %ld, largest class %ld\nlargest classes:", nc, sz[0]);
    for (long i = 0; i < nc && i < 12; i++) printf(" %ld", sz[i]);
    printf("\n");
    long ks[5] = {64, 90, 128, 256, 1024}, acc = 0; int ki = 0;
    for (long i = 0; i < nc && ki < 5; i++) { acc += sz[i]; if (i + 1 == ks[ki]) { printf("variants in the %ld largest classes: %ld = 2^%.3f\n", ks[ki], acc, log2((double)acc)); ki++; } }
    return 0;
}
```

### h3p.py

```python
"""h3p.py <a0p38 dir> <sha2-search dir> <first> <count>: the other row-16 passes of a successful first block (H3; own code).
For each success of the q3 study (rebuilt into CV1, M1, M1'; checked), every variant of every selected class that passes its W7 test on
CV1 is evaluated (E16x by the Step-2 formula); counts the row-16 passes other than the success and the further accepted pairs."""
import sys, glob, collections
sys.path.insert(0, sys.argv[1]); from a0p38 import *
R = sys.argv[2]; first, count = int(sys.argv[3]), int(sys.argv[4])
import os
POOL = os.environ.get('POOL', R + '/runs/vars_p08_pool.txt'); STUDY = os.environ.get('STUDY', R + '/runs/q3p8')
SPREAD = int(os.environ.get('SPREAD', '0'))         # 0: every 25th line, files in sorted order (the 1a695f0b sampling)
pool = [l.split() for l in open(POOL)]
sel = {c[0] for c in CLASSES}; mem = collections.defaultdict(list)
for l in open(R + '/runs/c/P08.cls.txt'):
    c, a = l.split(); c = int(c, 16)
    if c in sel: mem[c].append(int(a, 16))
succ = []
for f in sorted(glob.glob(STUDY + '/succ_*.txt')):
    for k, l in enumerate(open(f)):
        t = l.split()
        if len(t) == 33 and (SPREAD or k % 25 == 0): succ.append(t)
if SPREAD: succ = [succ[i * len(succ) // SPREAD] for i in range(SPREAD)]   # SPREAD successes evenly over all runs (sorted files, file order)
tot = dict(successes=0, verified=0, passing_classes=0, variants=0, other_r16=0, other_accepted=0, own_found=0)
for t in succ[first:first + count]:
    vi = int(t[1]); W = {7 + k: int(x, 16) for k, x in enumerate(t[2:])}; a0s = int(pool[vi][1], 16)
    cv, wx, wy = rebuild(W, a0s); tx, ty = trace(cv, wx), trace(cv, wy)
    tot['successes'] += 1
    if not (compress(cv, wx) == compress(cv, wy) and accepted(tx, ty) and inF7(wx[7])): continue
    tot['verified'] += 1
    m = Mach(); sc = fb_scalars(m, cv); a, b = cv[0], cv[1]
    for c, base, mk in CLASSES:
        if not inF7((c - cv[0]) & M): continue
        tot['passing_classes'] += 1
        for a0 in mem[c]:
            tot['variants'] += 1
            e0 = (a0 + sc['HH']) & M
            w1 = (sc['K1'] - S0(a0) - (sc['PP'] | (a0 & sc['QQ'])) - S1(e0) - (sc['FF'] ^ (e0 & sc['EF']))) & M
            e16 = (sc['KP'] + a0 + s0(w1)) & M
            if e16 in R16SET:
                if a0 == a0s: tot['own_found'] += 1; continue
                tot['other_r16'] += 1
                if deep(Mach(), cv, a0): tot['other_accepted'] += 1
print(tot)
```

### q3tv.c

```c
// Trail-based estimator of the uncontrolled probability of a 38-step SHA-256 characteristic (own code).
// q3tv: q3t with the tail drawing a dense-part variant per proposal (env VARS = vsamp output: j a0 a1 a2 w8x w9x w10x;
// member y gets w + dW_i of the base pair) and every success written to env DUMPALL (variant index, W7..W37 of member x).
// q = Pr[rows 16..37 follow the signed trail | dense part, W7 in F7], W0..W6 uniform (Lemma 4 structure).
// Input file (text, hex words): see prep.py. Usage: q3t <datafile> <seed> <N> <T> [g-cache]
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdint.h>
typedef uint32_t u32;
static const u32 K[64] = {
 0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,
 0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,
 0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070};
static inline u32 ror(u32 x, int n) { return (x >> n) | (x << (32 - n)); }
static inline u32 S0(u32 x) { return ror(x, 2) ^ ror(x, 13) ^ ror(x, 22); }
static inline u32 S1(u32 x) { return ror(x, 6) ^ ror(x, 11) ^ ror(x, 25); }
static inline u32 s0(u32 x) { return ror(x, 7) ^ ror(x, 18) ^ (x >> 3); }
static inline u32 s1(u32 x) { return ror(x, 17) ^ ror(x, 19) ^ (x >> 10); }
static inline u32 CH(u32 x, u32 y, u32 z) { return (x & y) ^ (~x & z); }
static inline u32 MAJ(u32 x, u32 y, u32 z) { return (x & y) ^ (x & z) ^ (y & z); }
static uint64_t rs[4];
static inline uint64_t rotl(uint64_t x, int k) { return (x << k) | (x >> (64 - k)); }
static uint64_t nxt(void) { uint64_t r = rotl(rs[1] * 5, 7) * 9, t = rs[1] << 17; rs[2] ^= rs[0]; rs[3] ^= rs[1]; rs[1] ^= rs[2]; rs[0] ^= rs[3]; rs[2] ^= t; rs[3] = rotl(rs[3], 45); return r; }
static void seed(uint64_t s) { for (int i = 0; i < 4; i++) { s += 0x9e3779b97f4a7c15ULL; uint64_t z = s; z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9ULL; z = (z ^ (z >> 27)) * 0x94d049bb133111ebULL; rs[i] = z ^ (z >> 31); } }
static inline u32 r32(void) { return (u32)(nxt() >> 32); }

typedef struct { u32 A[2][42], E[2][42], W[2][38]; } St;     // A/E index +4
#define AA(s, m, i) (s)->A[m][(i) + 4]
#define EE(s, m, i) (s)->E[m][(i) + 4]
static u32 MA[38], SA[38], ME[38], SE[38], MW[38], SW[38];   // trail: xor mask and x-value on the mask, rows 0..37
static St base; static u32 D7, T7;
typedef struct { int key, n, kind[3], row[3], bit[3]; u32 allowed; } Cond;
static Cond CO[8192]; static int nCO;
static u32 (*VW)[4]; static long nV;

static inline void step(St *s, int i) {
    for (int m = 0; m < 2; m++) {
        u32 a = AA(s, m, i - 1), b = AA(s, m, i - 2), c = AA(s, m, i - 3), d = AA(s, m, i - 4);
        u32 e = EE(s, m, i - 1), f = EE(s, m, i - 2), g = EE(s, m, i - 3), h = EE(s, m, i - 4);
        u32 T1 = h + S1(e) + CH(e, f, g) + K[i] + s->W[m][i];
        EE(s, m, i) = d + T1; AA(s, m, i) = T1 + S0(a) + MAJ(a, b, c);
    }
}
static inline int condok(const St *s, int r) {
    for (int c = 0; c < nCO; c++) {
        if (CO[c].key != r) continue;
        int idx = 0;
        for (int q = 0; q < CO[c].n; q++) { u32 w = CO[c].kind[q] == 2 ? s->W[0][CO[c].row[q]] : CO[c].kind[q] ? EE(s, 0, CO[c].row[q]) : AA(s, 0, CO[c].row[q]); idx |= ((w >> CO[c].bit[q]) & 1) << q; }
        if (!((CO[c].allowed >> idx) & 1)) return 0;
    }
    return 1;
}
static inline int rowok(const St *s, int r) {
    u32 ax = AA(s, 0, r), ex = EE(s, 0, r), wx = s->W[0][r];
    static long dfm = -1;   // DIFFROW=r[,r...]: these rows checked on signed differences only (no derived value conditions)
    if (dfm < 0) { dfm = 0; const char *e = getenv("DIFFROW"); while (e && *e) { int v = atoi(e); if (v > 0) dfm |= 1L << v; while (*e && *e != ',') e++; if (*e) e++; } }
    if (!((dfm >> r) & 1) && !condok(s, r)) return 0;
    return ((ax ^ AA(s, 1, r)) == MA[r]) && ((ax & MA[r]) == SA[r]) && ((ex ^ EE(s, 1, r)) == ME[r]) && ((ex & ME[r]) == SE[r])
        && ((wx ^ s->W[1][r]) == MW[r]) && ((wx & MW[r]) == SW[r]);
}
static inline void sched(St *s, int i) { for (int m = 0; m < 2; m++) s->W[m][i] = s1(s->W[m][i - 2]) + s->W[m][i - 7] + s0(s->W[m][i - 15]) + s->W[m][i - 16]; }
static inline int inF7(u32 w) { return s0(w + D7) - s0(w) == T7; }

static void load(const char *fn) {
    FILE *f = fopen(fn, "r"); if (!f) { perror(fn); exit(1); }
    char key[32];
    while (fscanf(f, "%31s", key) == 1) {
        if (!strcmp(key, "D7")) fscanf(f, "%x", &D7);
        else if (!strcmp(key, "T7")) fscanf(f, "%x", &T7);
        else if (!strcmp(key, "ROW")) { int r; u32 a, b, c, d, e, g; fscanf(f, "%d %x %x %x %x %x %x", &r, &a, &b, &c, &d, &e, &g); MA[r] = a; SA[r] = b; ME[r] = c; SE[r] = d; MW[r] = e; SW[r] = g; }
        else if (!strcmp(key, "ST")) { int m, i; u32 a, e; fscanf(f, "%d %d %x %x", &m, &i, &a, &e); AA(&base, m, i) = a; EE(&base, m, i) = e; }
        else if (!strcmp(key, "COND")) { Cond *c = &CO[nCO++]; fscanf(f, "%d %d", &c->key, &c->n); for (int q = 0; q < c->n; q++) fscanf(f, "%d %d %d", &c->kind[q], &c->row[q], &c->bit[q]); fscanf(f, "%x", &c->allowed); }
        else if (!strcmp(key, "W")) { int m, i; u32 w; fscanf(f, "%d %d %x", &m, &i, &w); base.W[m][i] = w; }
    }
    fclose(f);
}

int main(int argc, char **argv) {
    load(argv[1]); uint64_t sd = strtoull(argv[2], 0, 10); int N = atoi(argv[3]), T = atoi(argv[4]);
    seed(sd);
    u32 dW16 = (s1(base.W[1][14]) + base.W[1][9]) - (s1(base.W[0][14]) + base.W[0][9]);   // W0, W1 carry no difference
    // row 16 exhaustive (cached)
    static u32 G[1 << 20]; long nG = 0;
    char cache[512]; snprintf(cache, sizeof cache, "%s.g16", argv[1]);
    FILE *fc = fopen(cache, "rb");
    if (fc) { nG = fread(G, 4, 1 << 20, fc); fclose(fc); }
    else {
        for (uint64_t w = 0; w < (1ULL << 32); w++) {
            St s; memcpy(s.A, base.A, sizeof s.A); memcpy(s.E, base.E, sizeof s.E);
            s.W[0][16] = (u32)w; s.W[1][16] = (u32)w + dW16; step(&s, 16);
            if (rowok(&s, 16)) { if (nG < (1 << 20)) G[nG] = (u32)w; nG++; }
        }
        if (nG > (1 << 20)) { fprintf(stderr, "G too large %ld\n", nG); nG = 1 << 20; }
        fc = fopen(cache, "wb"); fwrite(G, 4, nG, fc); fclose(fc);
    }
    if (argc > 5 && !strcmp(argv[5], "live")) {   // row-17 pass counts per G word (sampled W17)
        int live = 0; uint64_t S = 1ULL << 24;
        for (long gi = 0; gi < nG; gi++) {
            St s = base; s.W[0][16] = G[gi]; s.W[1][16] = G[gi] + dW16; step(&s, 16);
            uint64_t pass = 0;
            for (uint64_t k = 0; k < S; k++) {
                St t = s; u32 wx = r32();
                u32 dsch = (s1(t.W[1][15]) + t.W[1][10]) - (s1(t.W[0][15]) + t.W[0][10]) + s0(t.W[1][2]) - s0(t.W[0][2]);
                t.W[0][17] = wx; t.W[1][17] = wx + dsch; step(&t, 17); pass += rowok(&t, 17);
            }
            live += pass > 0;
            printf("G %08x row17 passes %llu / 2^24\n", G[gi], (unsigned long long)pass);
        }
        printf("live G words: %d of %ld\n", live, nG); return 0;
    }
    uint64_t f7 = 0; for (int k = 0; k < 1 << 20; k++) f7 += inF7(r32());
    double lv[8]; lv[0] = nG ? log2((double)nG) - 32 : -INFINITY;
    if (!nG) { printf("seed %llu row16 impossible\n", (unsigned long long)sd); return 0; }
    St *cur = malloc(sizeof(St) * N), *nx = malloc(sizeof(St) * N); int ncur = N;
    for (int k = 0; k < N; k++) { St s = base; u32 w = G[nxt() % nG]; s.W[0][16] = w; s.W[1][16] = w + dW16; step(&s, 16); cur[k] = s; }
    for (int r = 17; r <= 22; r++) {
        uint64_t tries = 0; int got = 0;
        while (got < N) {
            if (tries > (1ULL << 34)) { printf("seed %llu stalled at row %d\n", (unsigned long long)sd, r); return 0; }
            const St *p = &cur[nxt() % ncur]; tries++;
            u32 wx = r32();
            u32 dsch = (s1(p->W[1][r - 2]) + p->W[1][r - 7]) - (s1(p->W[0][r - 2]) + p->W[0][r - 7]);
            if (r == 22) dsch += T7; else dsch += s0(p->W[1][r - 15]) - s0(p->W[0][r - 15]);
            St s = *p; s.W[0][r] = wx; s.W[1][r] = wx + dsch; step(&s, r);
            if (rowok(&s, r)) nx[got++] = s;
        }
        lv[r - 16] = log2((double)(N - 1) / (double)(tries - 1));
        St *t = cur; cur = nx; nx = t;
    }
    FILE *dall = getenv("DUMPALL") ? fopen(getenv("DUMPALL"), "w") : 0;
    if (getenv("VARS")) {
        FILE *fv = fopen(getenv("VARS"), "r"); long cap = 1 << 22; VW = malloc(sizeof(*VW) * cap); int j; u32 a0, a1, a2, w8, w9, w10;
        while (nV < cap && fscanf(fv, "%d %x %x %x %x %x %x", &j, &a0, &a1, &a2, &w8, &w9, &w10) == 7) { VW[nV][0] = (u32)nV; VW[nV][1] = w8; VW[nV][2] = w9; VW[nV][3] = w10; nV++; }
        fclose(fv); fprintf(stderr, "variants %ld\n", nV);
    }
    uint64_t prop = (uint64_t)N * T, succ = 0, coll = 0;
    for (uint64_t k = 0; k < prop; k++) {
        St s = cur[k % N]; u32 w7; do w7 = r32(); while (!inF7(w7));
        s.W[0][7] = w7; s.W[1][7] = w7 + D7;
        long vi = -1;
        if (nV) { vi = nxt() % nV; for (int i = 8; i <= 10; i++) { s.W[0][i] = VW[vi][i - 7]; s.W[1][i] = VW[vi][i - 7] + (base.W[1][i] - base.W[0][i]); } }
        int ok = 1;
        static int relax = -1; if (relax < 0) relax = getenv("RELAX_TAIL") != 0;
        for (int r = 23; r < 38 && ok; r++) { sched(&s, r); step(&s, r); if (!relax) ok = rowok(&s, r); }
        if (relax) { for (int i = 34; i < 38 && ok; i++) if (AA(&s, 0, i) != AA(&s, 1, i) || EE(&s, 0, i) != EE(&s, 1, i)) ok = 0; }
        if (ok) {
            succ++;
            if (succ == 1 && getenv("DUMP")) {
                FILE *fd = fopen(getenv("DUMP"), "w");
                for (int m = 0; m < 2; m++) for (int i = 0; i < 38; i++) fprintf(fd, "W %d %d %08x\n", m, i, s.W[m][i]);
                fclose(fd);
            }
            if (dall) { fprintf(dall, "S %ld", vi); for (int i = 7; i < 38; i++) fprintf(dall, " %08x", s.W[0][i]); fprintf(dall, "\n"); }
            int eq = 1; for (int i = 34; i < 38; i++) if (AA(&s, 0, i) != AA(&s, 1, i) || EE(&s, 0, i) != EE(&s, 1, i)) eq = 0;
            coll += eq;
        }
    }
    lv[7] = succ ? log2((double)succ / prop) : -INFINITY;
    double tot = 0; for (int i = 0; i < 8; i++) tot += lv[i];
    printf("seed %llu |G| %ld p2 %.4f stages", (unsigned long long)sd, nG, log2((double)f7 / (1 << 20)));
    for (int i = 0; i < 8; i++) printf(" %.3f", lv[i]);
    printf(" | succ %llu coll %llu | log2q %.4f%s\n", (unsigned long long)succ, (unsigned long long)coll, tot, nV ? " (variant tail)" : "");
    if (dall) fclose(dall);
    return 0;
}
```

### sweep.py

```python
"""sweep.py <outdir> <workers> <iters> [patterns]: systematic sign sweep over the HW-25 XOR patterns (own code).
For each XOR pattern (round robin) and iteration k: signed search with the DT43 bounds (attack-aware tail weight P <= 43, published
dense weight profile), the pattern fixed, signs free, and every signed message difference already found for that pattern blocked
together with its member-swapped mirror; a solution goes through score.py -> joint.py (value-exact dense part + value-exact tail
steps 16..19, P <= 43) -> fromjoint.py -> q3t (quick) and var (A2 list, mean |R(A0)|). One JSON line per stage in <outdir>/sweep.jsonl."""
import sys, json, os, subprocess, time, re, threading, queue, glob
OUT, NW, ITERS = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
os.makedirs(OUT, exist_ok=True)
PAT = json.load(open('/work/runs/dWxor_hw25.json'))
pats = [int(x) for x in sys.argv[4].split(',')] if len(sys.argv) > 4 else list(range(len(PAT)))
WN = ['W7', 'W8', 'W9', 'W10', 'W11', 'W15', 'W16', 'W23', 'W25']
BASE = {"wbounds": [[[["E", [16], 2], ["E", [15], 1], ["E", list(range(17, 26)), 3], ["A", list(range(16, 26)), 3], ["W", list(range(16, 38)), 2]], "<=", 43]],
        "solver": "kissat", "bounds": [["A", list(range(7, 16)), "<=", 26], ["E", list(range(7, 16)), "<=", 47], ["E", [14, 15], "<=", 4], ["A", [13, 14, 15], "<=", 10]]}
flip = lambda r: r.translate(str.maketrans('un', 'nu'))
lock = threading.Lock()
def log(**kw):
    kw['t'] = time.strftime('%H:%M:%S')
    with lock:
        with open(OUT + '/sweep.jsonl', 'a') as f: f.write(json.dumps(kw) + '\n')
# signed message differences already known (published, earlier runs) -> blocked per pattern
known = {p: [] for p in range(len(PAT))}
def xorpat(rows): return tuple(''.join('x' if c in 'un' else '=' for c in rows[w]) for w in WN)
patkey = {tuple(''.join('x' if c in 'un' else '=' for c in PAT[p][w[1:]]) for w in WN): p for p in range(len(PAT))}
def add_known(rows):
    p = patkey.get(xorpat(rows))
    if p is None: return
    s = {w: rows[w] for w in WN}
    for b in (s, {w: flip(r) for w, r in s.items()}):
        if b not in known[p]: known[p].append(b)
pub = json.load(open('/work/m38/paper_table3.json')); add_known({w: pub[w[1:]]['W'] for w in WN})
for f in glob.glob('/work/runs/q/*.json') + glob.glob(OUT + '/q/*.json'):
    try:
        q = json.load(open(f))
        if q.get('sat') and all(w in q['rows'] for w in WN): add_known(q['rows'])
    except Exception: pass
def sh(cmd, tmo, env=None):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=tmo, env=dict(os.environ, **(env or {})))
        return r.returncode, r.stdout, r.stderr
    except subprocess.TimeoutExpired: return -1, '', 'TIMEOUT'
def process(tag):
    c = '/work/runs/c/' + tag
    rc, o, e = sh('cd /work/m38 && python3 score.py /work/runs/q/%s.json %s' % (tag, c), 600)
    log(tag=tag, stage='score', out=o.strip()[-600:], err=e[-200:])
    rc, o, e = sh('cd /work/m38 && python3 joint.py %s 43 1 %s_j43' % (c, c), 7200, env=dict(EXACT_TAIL='16,17,18,19'))
    coupled = os.path.exists(c + '_j43.tail.json')
    log(tag=tag, stage='joint', coupled=coupled, out=o.strip()[-300:], err=e[-200:])
    if not coupled: return
    rc, o, e = sh('cd /work/m38 && python3 fromjoint.py %s_j43' % c, 1200)
    log(tag=tag, stage='fromjoint', out=o.strip()[-600:], err=e[-300:])
    if not os.path.exists(c + '_j43.dat'): return
    rc, o, e = sh('/work/m38/q3t %s_j43.dat 7 1000 4096' % c, 7200)
    log(tag=tag, stage='q3t', out=o.strip()[-400:], err=e[-200:])
    rc, o, e = sh('/work/m38/var %s_j43.var.dat 7 32 200000 | tail -2' % c, 7200)
    log(tag=tag, stage='var', out=o.strip()[-400:], err=e[-200:])
tasks = queue.Queue()
for k in range(ITERS):
    for p in pats: tasks.put((p, k))
dead = set()
def worker():
    while True:
        try: p, k = tasks.get_nowait()
        except queue.Empty: return
        if p in dead: continue
        tag = 'SW_p%02d_k%d' % (p, k)
        with lock: blocks = list(known[p])
        spec = dict(BASE, fix_xor={'W' + w: r for w, r in PAT[p].items()}, seed=100 + k, block_w=blocks)
        t0 = time.time()
        rc, o, e = sh("cd /work/m38 && python3 stepk.py %s '%s'" % (tag, json.dumps(spec)), 3 * 3600)
        res = 'TIMEOUT' if e == 'TIMEOUT' else ('SAT' if ' SAT' in o else 'UNSAT' if 'UNSAT' in o else 'ERR ' + e[-200:])
        log(tag=tag, stage='search', pattern=p, iter=k, blocked=len(blocks), result=res, wall=round(time.time() - t0))
        if res == 'UNSAT':
            with lock: dead.add(p)
            continue
        if res != 'SAT': continue
        q = json.load(open('/work/runs/q/%s.json' % tag))
        with lock: add_known(q['rows'])
        process(tag)
ths = [threading.Thread(target=worker) for _ in range(NW)]
for t in ths: t.start()
for t in ths: t.join()
log(stage='done')
```

### stepk.py

```python
"""Generic bounded query: python3 stepk.py <name> <json spec>; spec: {"hw_w": 25, "bounds": [[kind, rows, op, k], ...], "fix": {...}}"""
import sys, time, json, os
sys.path.insert(0, '/work/m38')
from sdmodel import sha256_model, decode
from pysat.solvers import Solver
name, spec = sys.argv[1], json.loads(sys.argv[2])
t0 = time.time()
m = sha256_model(n_msg=spec.get('n_msg', 38), diff_words=tuple(spec.get('diff_words', (7, 8, 9, 10, 11, 15, 16, 23, 25))), with_state=spec.get('with_state', True), state=tuple(spec.get('state', (7, 26))), zero_start=spec.get('zero_start', True), relax_steps=set(spec.get('relax_steps', ())), relax_kinds=tuple(spec.get('relax_kinds', ('S', 'B'))), exact_steps=set(spec.get('exact_steps', ())))
if 'hw_w' in spec: m.card(m.hw_lits(m.W), spec.get('hw_w_op', '='), spec['hw_w'])
for kind, rows, op, k in spec.get('bounds', []):
    ws = [m.words['%s%d' % (kind, i)] for i in rows if '%s%d' % (kind, i) in m.words]
    m.card(m.hw_lits(ws), op, k)
for terms, op, k in spec.get('wbounds', []):   # weighted: terms = [[kind, rows, weight], ...] (literals repeated by weight)
    lits = []
    for kind, rows, wt in terms:
        lits += m.hw_lits([m.words['%s%d' % (kind, i)] for i in rows]) * wt
    from pysat.card import EncType
    m.card(lits, op, k, enc=EncType.kmtotalizer if op == '<=' else EncType.totalizer)
for wname, row in spec.get('fix_xor', {}).items():     # difference positions only, signs free
    for q, ch in enumerate(row):
        v_, d_ = m.words[wname][31 - q]; m.cnf.append([d_] if ch in 'un' else [-d_])
for wname, row in spec.get('fix', {}).items():
    m.fix(m.words[wname], row)
for blk in spec.get('block_w', []):    # exclude a signed message difference: some difference bit of the listed words gets the other sign
    cl = []
    for wname, row in blk.items():
        for q, ch in enumerate(row):
            if ch in 'un':
                v_, d_ = m.words[wname][31 - q]; cl.append(-v_ if ch == 'u' else v_)
    if cl: m.cnf.append(cl)
t1 = time.time()
class _K:
    def __init__(self, clauses, nv): self.clauses, self.nv = clauses, nv
    def __enter__(self): return self
    def __exit__(self, *a): pass
    def solve(self):
        import subprocess, tempfile
        fn = tempfile.mktemp(suffix='.cnf', dir='/tmp')
        with open(fn, 'w') as f:
            f.write('p cnf %d %d\n' % (self.nv, len(self.clauses)))
            for c in self.clauses: f.write(' '.join(map(str, c)) + ' 0\n')
        r = subprocess.run(['kissat', '-q', '--seed=%d' % spec.get('seed', 0), fn], capture_output=True, text=True)
        os.unlink(fn)
        self.model = [int(x) for l in r.stdout.splitlines() if l.startswith('v') for x in l[1:].split() if x != '0']
        return 's SATISFIABLE' in r.stdout
    def get_model(self): return self.model
_solver = (lambda: _K(m.cnf.clauses, m.pool.top)) if spec.get('solver') == 'kissat' else (lambda: Solver(name=spec.get('solver', 'cadical195'), bootstrap_with=m.cnf.clauses))
with _solver() as s:
    ok = s.solve()
    dt = time.time() - t1
    out = dict(name=name, spec=spec, sat=ok, solve_s=round(dt, 1), build_s=round(t1 - t0, 1))
    if ok:
        ms = set(l for l in s.get_model() if l > 0)
        names = [n for n in ['A%d' % i for i in range(-4, 40)] + ['E%d' % i for i in range(-4, 40)] if n in m.words] + ['W%d' % i for i in range(spec.get('n_msg', 38))]
        names += [n for n in m.words if n.split('_')[0] in ('S1', 'IF', 'S0', 'MJ', 's1', 's0') and n.count('_') == 1]
        out['rows'] = decode(m, ms, names)
os.makedirs('/work/runs/q', exist_ok=True)
json.dump(out, open('/work/runs/q/%s.json' % name, 'w'))
print(name, 'SAT' if ok else 'UNSAT', '%.1fs' % dt)
```

### score.py

```python
"""score.py <query.json> [out_prefix]: turn a SAT characteristic (stepk output) into char.json and inter.json,
and count derived conditions per key row (own code)."""
import sys, json
sys.path.insert(0, '/work/m38')
from cond import derive
from collections import Counter
Q = json.load(open(sys.argv[1])); R = Q['rows']
NS = Q.get('spec', {}).get('n_msg', 38); ST0 = Q.get('spec', {}).get('state', [7, 26])[0]
char = {}
for i in range(-4, NS):
    char[i] = {'A': R.get('A%d' % i, '=' * 32), 'E': R.get('E%d' % i, '=' * 32), 'W': R.get('W%d' % i, '=' * 32) if i >= 0 else '=' * 32}
inter = {}
for n, row in R.items():
    if '_' in n:
        k, r = n.split('_'); inter[(k, int(r))] = row
rows = {}
for i, r in char.items():
    rows[('A', i)] = r['A']; rows[('E', i)] = r['E']; rows[('W', i)] = r['W']
conds, bad = derive(rows, inter, range(ST0, NS))
cnt = Counter(c['key'] for c in conds)
bits = lambda c: len(c['refs']) - __import__('math').log2(len(c['allowed']))
cost = Counter()
for c in conds: cost[c['key']] += bits(c)
hw = lambda s: sum(ch in 'un' for ch in s)
summary = dict(name=Q['name'], bad=len(bad), cond_bits_by_key={k: round(v, 1) for k, v in sorted(cost.items())},
               cond_bits_ge17=round(sum(v for k, v in cost.items() if k >= 17), 1), cond_bits_16=round(cost.get(16, 0), 1), cond_bits_ge16=round(sum(v for k, v in cost.items() if k >= 16), 1),
               hwE=[hw(char[i]['E']) for i in range(14, 23)], hwA=[hw(char[i]['A']) for i in range(14, 19)],
               hwW=[hw(char[i]['W']) for i in (7, 8, 9, 10, 11, 15, 16, 23, 25)])
print(json.dumps(summary))
if len(sys.argv) > 2:
    json.dump({str(k): v for k, v in char.items()}, open(sys.argv[2] + '.char.json', 'w'))
    json.dump({'%s_%d' % k: v for k, v in inter.items()}, open(sys.argv[2] + '.inter.json', 'w'))
```

### joint.py

```python
"""joint.py <char prefix> <P> <seed> <out prefix>: one CNF = value-exact dense part (rows <= 15, signed dense trail
of <prefix>.char.json, expansion constraints) + signed tail model (steps 16..25, weighted bound P), linked at rows
12..15 (tail (v, d) = dense (x, x XOR y)) and on the message words. Solved with Kissat (own code)."""
import sys, json, time, subprocess, os, math
sys.path.insert(0, '/work/m38')
from sdmodel import sha256_model, decode
from vmodel import dense_model, value
from cond import derive
from collections import Counter
from pysat.card import EncType
pre, P, seed, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
C = {int(k): v for k, v in json.load(open(pre + '.char.json')).items()}
free15 = len(sys.argv) > 5 and sys.argv[5] == 'free1215'   # let the dense rows 12..15 trail be free (only the tail fixes them)
freerows = [int(x) for x in sys.argv[5].split(',')] if len(sys.argv) > 5 and sys.argv[5] != 'free1215' else (range(12, 16) if free15 else ())
import os as _os
m = sha256_model(state=(16, 26), zero_start=False, exact_steps=set(int(x) for x in _os.environ.get('EXACT_TAIL', '').split(',') if x))
for i in range(38): m.fix(m.words['W%d' % i], ''.join(c if c in 'un' else '=' for c in C[i]['W']))
lits = []
for kind, rows, wt in (('E', [16], 2), ('E', [15], 1), ('E', range(17, 26), 3), ('A', range(16, 26), 3), ('W', range(16, 38), 2)):
    lits += m.hw_lits([m.words['%s%d' % (kind, i)] for i in rows if '%s%d' % (kind, i) in m.words]) * wt
m.card(lits, '<=', P, enc=EncType.kmtotalizer)
N1 = m.pool.top
v = dense_model(C, expansion=True, free_rows=freerows)
sh = lambda l: (abs(l) + N1) * (1 if l > 0 else -1)
cl = [list(c) for c in m.cnf.clauses] + [[sh(l) for l in c] for c in v.cl]
nv = N1 + v.pool.top
def xorvar(a, b):
    global nv
    nv += 1; d = nv
    cl.extend([[-a, -b, -d], [a, b, -d], [a, -b, d], [-a, b, d]]); return d
def eqlit(a, b): cl.extend([[-a, b], [a, -b]])
for i in range(12, 16):
    for nm, X, Y in (('A', v.A, v.Ay), ('E', v.E, v.Ey)):
        for j in range(32):
            sv, sd = m.words['%s%d' % (nm, i)][j]
            x, y = sh(X[i][j]), sh(Y[i][j])
            eqlit(sv, x); eqlit(sd, xorvar(x, y))
for i in range(8, 16):     # message words: tail model value bits = dense member-x values
    for j in range(32):
        sv, sd = m.words['W%d' % i][j]; eqlit(sv, sh(v.W[i][j]))
fn = out + '.cnf'
with open(fn, 'w') as f:
    f.write('p cnf %d %d\n' % (nv, len(cl)))
    for c in cl: f.write(' '.join(map(str, c)) + ' 0\n')
t = time.time(); r = subprocess.run(['kissat', '-q', '--seed=%d' % seed, fn], capture_output=True, text=True); os.unlink(fn)
ok = 's SATISFIABLE' in r.stdout; print('joint SAT:', ok, '%.1fs' % (time.time() - t), 'vars', nv, 'clauses', len(cl), flush=True)
if not ok: sys.exit(1)
model = set(int(x) for l in r.stdout.splitlines() if l.startswith('v') for x in l[1:].split() if x != '0' and int(x) > 0)
ms_sd = {l for l in model if l <= N1}
ms_v = {l - N1 for l in model if N1 < l <= N1 + v.pool.top}
names = ['A%d' % i for i in range(12, 26)] + ['E%d' % i for i in range(12, 26)] + ['W%d' % i for i in range(38)]
names += [x for x in m.words if x.split('_')[0] in ('S1', 'IF', 'S0', 'MJ', 's1', 's0') and x.count('_') == 1]
R = decode(m, ms_sd, names)
rows = {(k, i): R.get('%s%d' % (k, i), '=' * 32) for k in 'AEW' for i in range(-4, 38)}
inter = {(x.split('_')[0], int(x.split('_')[1])): rr for x, rr in R.items() if '_' in x}
conds, bad = derive(rows, inter, range(17, 38))
cost = Counter()
for c in conds: cost[c['key']] += len(c['refs']) - math.log2(len(c['allowed']))
print('tail ge17 %.1f k16 %.1f bad %d' % (sum(vv for kk, vv in cost.items() if kk >= 17), cost.get(16, 0), len(bad)), flush=True)
Ws = {str(i): C[i]['W'] for i in range(38) if any(c in 'un' for c in C[i]['W'])}
json.dump(dict(A={i: value(ms_v, v.A[i]) for i in range(0, 16)}, E={i: value(ms_v, v.E[i]) for i in range(3, 16)},
               W={i: value(ms_v, v.W[i]) for i in range(7, 16)}, Ay={i: value(ms_v, v.Ay[i]) for i in range(7, 16)},
               Ey={i: value(ms_v, v.Ey[i]) for i in range(7, 16)}, Wy={i: value(ms_v, v.Wy[i]) for i in range(7, 16)}, Wsigned=Ws),
          open(out + '.dense.json', 'w'))
json.dump(dict(rows=R, ge17=sum(vv for kk, vv in cost.items() if kk >= 17)), open(out + '.tail.json', 'w'))
```

### fromjoint.py

```python
"""fromjoint.py <joint out prefix> [seed]: dense values + tail of a joint solve -> char/inter/pair/q3t data/var data (own code)."""
import sys, json, random, subprocess
sys.path.insert(0, '/work/m38')
from sha38 import S0, S1, CH, MAJ, M32, trace
from vmodel import K
pre = sys.argv[1]; seed = int(sys.argv[2]) if len(sys.argv) > 2 else 1
D = json.load(open(pre + '.dense.json')); T = json.load(open(pre + '.tail.json'))['rows']
A = {int(k): v for k, v in D['A'].items()}; E = {int(k): v for k, v in D['E'].items()}; W = {int(k): v for k, v in D['W'].items()}
Wyd = {int(k): v for k, v in D['Wy'].items()}
rnd = random.Random(seed); Af = dict(A); Ef = dict(E)
for i in (-2, -3, -4): Af[i] = rnd.getrandbits(32)
Af[-1] = (E[3] - A[3] + S0(A[2]) + MAJ(A[2], A[1], A[0])) & M32
for i in (2, 1, 0): Ef[i] = (A[i] + Af[i - 4] - S0(Af[i - 1]) - MAJ(Af[i - 1], Af[i - 2], Af[i - 3])) & M32
for i in (-1, -2, -3, -4): Ef[i] = rnd.getrandbits(32)
Wx = [0] * 16
for i in range(0, 7): Wx[i] = (Ef[i] - Af[i - 4] - Ef[i - 4] - S1(Ef[i - 1]) - CH(Ef[i - 1], Ef[i - 2], Ef[i - 3]) - K[i]) & M32
for i in range(7, 16): Wx[i] = W[i]
Wy = list(Wx)
for i in range(7, 16): Wy[i] = Wyd[i]
cv = [Af[-1], Af[-2], Af[-3], Af[-4], Ef[-1], Ef[-2], Ef[-3], Ef[-4]]
ax, ex, wx, _ = trace(cv, Wx, 16); ay, ey, wy, _ = trace(cv, Wy, 16)
sym = lambda x, y: ''.join('=' if ((x >> j) & 1) == ((y >> j) & 1) else ('u' if (x >> j) & 1 else 'n') for j in range(31, -1, -1))
Z = '=' * 32
char = {}
for i in range(-4, 38):
    if i <= 15: char[i] = {'A': sym(ax[i], ay[i]), 'E': sym(ex[i], ey[i]), 'W': sym(wx[i], wy[i]) if i >= 0 else Z}
    else: char[i] = {'A': T.get('A%d' % i, Z), 'E': T.get('E%d' % i, Z), 'W': T.get('W%d' % i, Z)}
for i in range(12, 16):   # consistency of the joint link
    assert char[i]['A'] == ''.join(c if c in 'un' else '=' for c in T['A%d' % i]) and char[i]['E'] == ''.join(c if c in 'un' else '=' for c in T['E%d' % i]), i
inter = {x: r for x, r in T.items() if '_' in x}
json.dump({str(k): v for k, v in char.items()}, open(pre + '.char.json', 'w'))
json.dump(inter, open(pre + '.inter.json', 'w'))
json.dump(dict(cv=cv, Wx=Wx, Wy=Wy), open(pre + '.pair.json', 'w'))
r = subprocess.run(['python3', '/work/m38/prep.py', pre + '.char.json', pre + '.pair.json', pre + '.dat', pre + '.inter.json'], capture_output=True, text=True)
print(r.stdout.strip(), r.stderr.strip()[-600:])
r = subprocess.run(['python3', '/work/m38/prepvar.py', pre], capture_output=True, text=True)
print(r.stdout.strip(), r.stderr.strip()[-600:])
```

### prep.py

```python
"""prep.py <char.json> <pair.json> <out.dat> [inter.json]: data file for q3t.c (own code).
pair.json: {"cv": [8 words], "Wx": [16], "Wy": [16]} (dense pair; if it is a full 38-step
conforming pair and no inter.json is given, intermediates of rows >= 16 are taken from it).
inter.json: {"S1_16": row, ...} intermediate signed outputs from the SAT solution."""
import sys, json
sys.path.insert(0, '/work/m38'); sys.path.insert(0, sys.argv[0].rsplit('/', 1)[0])
from sha38 import trace, s1, M32
from cond import derive, check, intermediates_from_pair
C = {int(k): v for k, v in json.load(open(sys.argv[1])).items()}
P = json.load(open(sys.argv[2]))
cv, Wx, Wy = P['cv'], P['Wx'], P['Wy']
ax, ex, _, _ = trace(cv, Wx, 16); ay, ey, _, _ = trace(cv, Wy, 16)
def ms(row):
    m = sum(1 << (31 - k) for k, c in enumerate(row) if c in 'un'); s = sum(1 << (31 - k) for k, c in enumerate(row) if c == 'u')
    return m, s
def sval(row):   # y - x for the signed row ('u': x = 1, y = 0)
    return sum((-(1 << (31 - k)) if c == 'u' else (1 << (31 - k))) for k, c in enumerate(row) if c in 'un') & M32
out = []
for r in range(16, 38):
    row = C.get(r, {'A': '=' * 32, 'E': '=' * 32, 'W': '=' * 32})
    out.append('ROW %d %08x %08x %08x %08x %08x %08x' % ((r,) + ms(row['A']) + ms(row['E']) + ms(row['W'])))
for m, (A, E) in enumerate(((ax, ex), (ay, ey))):
    for i in range(-4, 16): out.append('ST %d %d %08x %08x' % (m, i, A[i], E[i]))
for m, W in enumerate((Wx, Wy)):
    for i in range(16): out.append('W %d %d %08x' % (m, i, W[i]))
assert all(c not in 'un' for c in C.get(20, {'W': '='})['W']), 'W20 difference not supported'
d7 = (Wy[7] - Wx[7]) & M32
t7 = (sval(C.get(22, {'W': '=' * 32})['W']) - ((Wy[15] - Wx[15]) & M32)) & M32
out = ['D7 %08x' % d7, 'T7 %08x' % t7] + out
# value conditions of the boolean functions of steps 16..37
rows = {}
for i, r in C.items():
    rows[('A', i)] = r['A']; rows[('E', i)] = r['E']; rows[('W', i)] = r['W']
if len(sys.argv) > 4:
    I = json.load(open(sys.argv[4])); inter = {(k.split('_')[0], int(k.split('_')[1])): v for k, v in I.items()}
else:
    fx, fy = trace(cv, Wx, 38), trace(cv, Wy, 38)
    inter = intermediates_from_pair((fx[0], fx[1]), (fy[0], fy[1]), range(16, 38), fx[2], fy[2])
conds, bad = derive(rows, inter, range(16, 38))
assert not bad, ('impossible boolean instances', bad[:5])
Ax, Ex = ax, ex
early = [c for c in conds if c['key'] <= 15]
fails = check(early, lambda k, i: {'A': Ax, 'E': Ex, 'W': dict(enumerate(Wx))}[k][i])
print('conditions: %d (keyed <= 15: %d, violated by the dense pair: %d)' % (len(conds), len(early), len(fails)))
for c in fails[:10]: print('  violated', c['src'], c['refs'], c['allowed'])
for c in conds:
    if c['key'] <= 15: continue
    am = sum(1 << sum(b << q for q, b in enumerate(t)) for t in c['allowed'])
    out.append('COND %d %d %s %x' % (c['key'], len(c['refs']), ' '.join('%d %d %d' % ({'A': 0, 'E': 1, 'W': 2}[k], i, b) for k, i, b in c['refs']), am))
open(sys.argv[3], 'w').write('\n'.join(out) + '\n')
from collections import Counter
print('conditions per key row:', sorted(Counter(c['key'] for c in conds).items()))
print('D7 %08x T7 %08x' % (d7, t7))
```

### cond.py

```python
"""Derive value conditions of a signed trail from its boolean-function instances (own code).
For each step r and bit j, the instances Sigma1(E_{r-1}), IF(E_{r-1}, E_{r-2}, E_{r-3}),
Sigma0(A_{r-1}), MAJ(A_{r-1}, A_{r-2}, A_{r-3}) must produce the trail's output signed difference
(intermediate words S1_r, IF_r, S0_r, MJ_r). Inputs with a difference have their x value fixed by
the sign; for the inputs without a difference, enumerate their values and keep the allowed set.
A condition is (refs, allowed): refs = [(kind, row, bit)] of the non-difference inputs, allowed =
set of value tuples. Keyed at the largest input row."""
import itertools

def sym_xy(s, v):
    """symbol and a value for non-diff bits -> (x, y)"""
    if s == 'u': return 1, 0
    if s == 'n': return 0, 1
    return v, v

FN = {'XOR': lambda a, b, c: a ^ b ^ c, 'IF': lambda a, b, c: (a & b) ^ ((1 - a) & c), 'MAJ': lambda a, b, c: (a & b) ^ (a & c) ^ (b & c)}

def bit(row, j):    # row string MSB first
    return row[31 - j]

def derive(rows, inter, steps):
    """rows[(kind, i)] -> 32-symbol string ('=', 'u', 'n'; others mean '='), kinds 'A', 'E';
    inter[(name, r)] -> 32-symbol output string for name in S1, IF, S0, MJ. Returns list of
    dicts {key, refs, allowed, src} and a list of impossible instances."""
    conds, bad = [], []
    def g(kind, i, j):
        if kind == 'Z': return '0'
        s = rows.get((kind, i), '=' * 32)[31 - j]
        return s if s in 'un' else '='
    for r in steps:
        specs = []
        for j in range(32):
            specs.append(('S1', 'XOR', [('E', r - 1, (j + 6) % 32), ('E', r - 1, (j + 11) % 32), ('E', r - 1, (j + 25) % 32)], j))
            specs.append(('IF', 'IF', [('E', r - 1, j), ('E', r - 2, j), ('E', r - 3, j)], j))
            specs.append(('S0', 'XOR', [('A', r - 1, (j + 2) % 32), ('A', r - 1, (j + 13) % 32), ('A', r - 1, (j + 22) % 32)], j))
            specs.append(('MJ', 'MAJ', [('A', r - 1, j), ('A', r - 2, j), ('A', r - 3, j)], j))
            if r >= 16:   # W_r = s1(W_{r-2}) + W_{r-7} + s0(W_{r-15}) + W_{r-16}
                specs.append(('s1', 'XOR', [('W', r - 2, (j + 17) % 32), ('W', r - 2, (j + 19) % 32)] + ([('W', r - 2, j + 10)] if j + 10 < 32 else [('Z', 0, 0)]), j))
                specs.append(('s0', 'XOR', [('W', r - 15, (j + 7) % 32), ('W', r - 15, (j + 18) % 32)] + ([('W', r - 15, j + 3)] if j + 3 < 32 else [('Z', 0, 0)]), j))
        for name, fn, ins, j in specs:
            out = inter.get((name, r), '=' * 32)[31 - j]
            out = out if out in 'un' else '='
            syms = [g(*t) for t in ins]
            free = [k for k, s in enumerate(syms) if s == '=']
            syms = [('=' if s == '0' else s) for s in syms]
            # deduplicate repeated references (rotations never repeat a bit, MAJ/IF use distinct rows)
            allowed = set()
            for vals in itertools.product((0, 1), repeat=len(free)):
                vv = dict(zip(free, vals))
                xs, ys = zip(*[sym_xy(syms[k], vv.get(k, 0)) for k in range(3)])
                ox, oy = FN[fn](*xs), FN[fn](*ys)
                o = '=' if ox == oy else ('u' if ox == 1 else 'n')
                if o == out: allowed.add(vals)
            if not allowed:
                bad.append((name, r, j)); continue
            if len(allowed) < 2 ** len(free):
                refs = [ins[k] for k in free]
                conds.append(dict(key=max(t[1] for t in refs), refs=refs, allowed=sorted(allowed), src='%s_%d[%d]' % (name, r, j)))
    return conds, bad

def check(conds, val):
    """val(kind, row) -> 32-bit word of member x. Returns failing conditions."""
    fails = []
    for c in conds:
        t = tuple((val(k, i) >> b) & 1 for k, i, b in c['refs'])
        if t not in set(map(tuple, c['allowed'])): fails.append(c)
    return fails

def intermediates_from_pair(trace_x, trace_y, steps, Wx=None, Wy=None):
    """exact intermediate output differences from a conforming pair (A, E dicts of both members; W lists)."""
    from sha38 import S0, S1, CH, MAJ, s0, s1
    (Ax, Ex), (Ay, Ey) = trace_x, trace_y
    def sym(x, y):
        return ''.join('=' if ((x >> j) & 1) == ((y >> j) & 1) else ('u' if (x >> j) & 1 else 'n') for j in range(31, -1, -1))
    inter = {}
    for r in steps:
        inter[('S1', r)] = sym(S1(Ex[r - 1]), S1(Ey[r - 1]))
        inter[('IF', r)] = sym(CH(Ex[r - 1], Ex[r - 2], Ex[r - 3]), CH(Ey[r - 1], Ey[r - 2], Ey[r - 3]))
        inter[('S0', r)] = sym(S0(Ax[r - 1]), S0(Ay[r - 1]))
        inter[('MJ', r)] = sym(MAJ(Ax[r - 1], Ax[r - 2], Ax[r - 3]), MAJ(Ay[r - 1], Ay[r - 2], Ay[r - 3]))
        if Wx is not None and r >= 16:
            inter[('s1', r)] = sym(s1(Wx[r - 2]), s1(Wy[r - 2])); inter[('s0', r)] = sym(s0(Wx[r - 15]), s0(Wy[r - 15]))
    return inter
```

### sdmodel.py

```python
"""Own signed-difference CNF model of reduced SHA-256 (written from scratch for this search).

Each bit of every word is a pair (v, d): v = value in member x, d = 1 iff member y differs
(member y's bit is v XOR d). Symbols: d = 0 '=' (value v), (v, d) = (1, 1) 'u', (0, 1) 'n'.
- Boolean functions (XOR3 for Sigma/sigma, IF, MAJ): exact two-member relations.
- Modular addition: signed-carry relation s_a + s_b + s_c = s_z + 2 s_c' with s = d (2v - 1),
  values ignored (the standard signed-difference relaxation; value consistency is checked later
  by solving for a conforming pair).
Rows of the state are indexed as in FIPS / the paper: A_i, E_i for i = -4..; step i uses W_i."""
import itertools
from functools import lru_cache
from pysat.formula import CNF, IDPool
from pysat.card import CardEnc, EncType

B = 32
K = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5, 0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174, 0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da, 0x983e5152, 0xa831c66d]
ROT = lambda w, n: w[n:] + w[:n]          # w[j] = bit j; ROTR by n: new[j] = old[j + n]


def qm_cnf(nvars, allowed, dontcare=()):
    """Minimal-ish CNF (prime implicates covering the forbidden set) of a boolean relation
    over nvars variables; allowed and dontcare are sets of assignments (tuples of 0/1)."""
    allowed, dontcare = set(allowed), set(dontcare)
    forbidden = [a for a in itertools.product((0, 1), repeat=nvars) if a not in allowed and a not in dontcare]
    if not forbidden:
        return []
    # implicants of the forbidden function (as cubes with None = free), merging with don't-cares
    on = set(forbidden) | dontcare
    cubes = {tuple(a) for a in on}
    primes = set()
    while cubes:
        nxt, used = set(), set()
        cl = list(cubes)
        idx = {}
        for c in cl:
            for k in range(nvars):
                if c[k] is None: continue
                key = c[:k] + (None,) + c[k + 1:]
                idx.setdefault((k, key), []).append(c)
        for (k, key), group in idx.items():
            vals = {g[k] for g in group}
            if vals == {0, 1}:
                nxt.add(key); used.update(group)
        primes |= cubes - used
        cubes = nxt
    primes = sorted(primes, key=lambda p: tuple(2 if x is None else x for x in p))   # deterministic order (None hashes by address)
    # greedy cover of the forbidden minterms (don't-cares need not be covered)
    def covers(p, m): return all(p[k] is None or p[k] == m[k] for k in range(nvars))
    todo = set(forbidden); chosen = []
    while todo:
        best = max(primes, key=lambda p: (sum(covers(p, m) for m in todo), -sum(x is not None for x in p)))
        chosen.append(best); todo = {m for m in todo if not covers(best, m)}
    # a cube of the forbidden set -> clause forbidding it
    return [[(k + 1) * (-1 if p[k] == 1 else 1) for k in range(nvars) if p[k] is not None] for p in chosen]


@lru_cache(None)
def rel_bool(fn):
    """inputs (v0,d0,v1,d1,v2,d2) -> output (vo,do); exact for both members."""
    f = {'XOR': lambda a, b, c: a ^ b ^ c, 'IF': lambda a, b, c: (a & b) ^ ((1 - a) & c), 'MAJ': lambda a, b, c: (a & b) ^ (a & c) ^ (b & c)}[fn]
    allowed = set()
    for v0, d0, v1, d1, v2, d2 in itertools.product((0, 1), repeat=6):
        x = f(v0, v1, v2); y = f(v0 ^ d0, v1 ^ d1, v2 ^ d2)
        allowed.add((v0, d0, v1, d1, v2, d2, x, x ^ y))
    return qm_cnf(8, allowed)


@lru_cache(None)
def rel_add():
    """signed-carry addition bit: (va,da,vb,db,vc,dc,vz,dz,vn,dn) with s_a+s_b+s_c = s_z + 2 s_n.
    For d = 0 the value bit is free (don't care)."""
    allowed = set()
    sg = lambda v, d: (2 * v - 1) if d else 0
    for t in itertools.product((0, 1), repeat=10):
        va, da, vb, db, vc, dc, vz, dz, vn, dn = t
        if sg(va, da) + sg(vb, db) + sg(vc, dc) == sg(vz, dz) + 2 * sg(vn, dn):
            allowed.add(t)
    return qm_cnf(10, allowed)


class SD:
    def __init__(self):
        self.pool = IDPool(); self.cnf = CNF(); self.words = {}

    def word(self, name):
        if name not in self.words:
            self.words[name] = [(self.pool.id((name, j, 'v')), self.pool.id((name, j, 'd'))) for j in range(B)]
        return self.words[name]

    def const_word(self, c):
        name = 'K_%08x' % c
        if name not in self.words:
            w = self.word(name)
            for j, (v, d) in enumerate(w):
                self.cnf.append([-d]); self.cnf.append([v] if (c >> j) & 1 else [-v])
        return self.words[name]

    def const0(self):
        if 'ZERO' not in self.words:
            w = self.word('ZERO')
            for v, d in w: self.cnf.append([-v]); self.cnf.append([-d])
        return self.words['ZERO'][0]

    def apply(self, clauses, lits):
        for c in clauses:
            self.cnf.append([lits[abs(l) - 1] * (1 if l > 0 else -1) for l in c])

    def relaxed_copy(self, w):
        """per-instance value bits: shared sign (v when d = 1), free value when d = 0"""
        out = []
        for v, d in w:
            v2 = self.pool.id()
            self.cnf.append([-d, -v, v2]); self.cnf.append([-d, v, -v2])
            out.append((v2, d))
        return out

    def boolfn(self, fn, a, b, c, out, relax=False):
        cl = rel_bool(fn)
        if relax: a, b, c = self.relaxed_copy(a), self.relaxed_copy(b), self.relaxed_copy(c)
        for j in range(B):
            self.apply(cl, [a[j][0], a[j][1], b[j][0], b[j][1], c[j][0], c[j][1], out[j][0], out[j][1]])

    def add(self, a, b, out, tag):
        """out = a + b with signed carries."""
        cl = rel_add()
        carry = [(self.pool.id((tag, j, 'cv')), self.pool.id((tag, j, 'cd'))) for j in range(B + 1)]
        self.cnf.append([-carry[0][1]])          # no carry difference into bit 0
        for j in range(B):
            self.apply(cl, [a[j][0], a[j][1], b[j][0], b[j][1], carry[j][0], carry[j][1], out[j][0], out[j][1], carry[j + 1][0], carry[j + 1][1]])
        # carry out of bit 31 is discarded (mod 2^32): no constraint

    def yval(self, v, d):
        y = self.pool.id(); self.cnf.extend([[-v, -d, -y], [v, d, -y], [v, -d, y], [-v, d, y]]); return y

    def exact_add(self, a, b, out):
        """value-exact z = a + b for member x (bits v) and member y (bits v XOR d)."""
        for m in (0, 1):
            av = [x[0] if m == 0 else self.yval(*x) for x in a]
            bv = [x[0] if m == 0 else self.yval(*x) for x in b]
            zv = [x[0] if m == 0 else self.yval(*x) for x in out]
            c = None
            for j in range(B):
                if c is None:
                    self.xor_eq(av[j], bv[j], None, zv[j]); c = self.pool.id()
                    self.cnf.extend([[-av[j], -bv[j], c], [av[j], -c], [bv[j], -c]])
                else:
                    self.xor_eq(av[j], bv[j], c, zv[j])
                    if j < B - 1:
                        c2 = self.pool.id()
                        self.cnf.extend([[-av[j], -bv[j], c2], [-av[j], -c, c2], [-bv[j], -c, c2], [av[j], bv[j], -c2], [av[j], c, -c2], [bv[j], c, -c2]])
                        c = c2

    def xor_eq(self, a, b, c, z):
        lits = [a, b] + ([c] if c is not None else [])
        import itertools
        for vals in itertools.product((0, 1), repeat=len(lits)):
            r = sum(vals) & 1
            self.cnf.append([(-l if v else l) for l, v in zip(lits, vals)] + [z if r else -z])

    def addn(self, terms, out, tag, exact=False):
        acc = terms[0]
        for k, t in enumerate(terms[1:]):
            dst = out if k == len(terms) - 2 else self.word('%s_t%d' % (tag, k))
            self.add(acc, t, dst, '%s_c%d' % (tag, k))
            if exact: self.exact_add(acc, t, dst)
            acc = dst

    def sigma(self, w, r1, r2, r3, shift, out, relax=False):
        z = self.const0()
        if relax: w = self.relaxed_copy(w)
        third = ROT(w, r3) if not shift else (w[r3:] + [z] * r3)
        self.boolfn('XOR', ROT(w, r1), ROT(w, r2), third, out)

    def zero_diff(self, w):
        for v, d in w: self.cnf.append([-d])

    def hw_lits(self, ws):
        return [d for w in ws for v, d in w]

    def fix(self, w, row):
        """row: 32 symbols MSB first; '=' no diff (value free), 'u'/'n' diff, '0'/'1' value condition, '-' free."""
        for k, s in enumerate(row):
            v, d = w[B - 1 - k]
            if s in '=0123456789+-' and s not in 'un':
                self.cnf.append([-d])
                if s == '0': self.cnf.append([-v])
                if s == '1': self.cnf.append([v])
            elif s == 'u': self.cnf.append([d]); self.cnf.append([v])
            elif s == 'n': self.cnf.append([d]); self.cnf.append([-v])

    def card(self, lits, op, k, enc=EncType.totalizer):
        f = {'<=': CardEnc.atmost, '>=': CardEnc.atleast, '=': CardEnc.equals}[op](lits=lits, bound=k, vpool=self.pool, encoding=enc)
        self.cnf.extend(f.clauses)


def sha256_model(n_msg=38, diff_words=(7, 8, 9, 10, 11, 15, 16, 23, 25), state=(7, 26), with_state=True, zero_start=True, relax_steps=(), relax_kinds=('S', 'B'), exact_steps=()):
    m = SD()
    W = [m.word('W%d' % i) for i in range(n_msg)]
    for i in range(16, n_msg):
        s1, s0 = m.word('s1_%d' % i), m.word('s0_%d' % i)
        m.sigma(W[i - 2], 17, 19, 10, True, s1)
        m.sigma(W[i - 15], 7, 18, 3, True, s0)
        m.addn([s1, W[i - 7], s0, W[i - 16]], W[i], 'mx%d' % i)
    for i in range(n_msg):
        if i not in diff_words: m.zero_diff(W[i])
    A = {i: m.word('A%d' % i) for i in range(state[0] - 4, state[1])}
    E = {i: m.word('E%d' % i) for i in range(state[0] - 4, state[1])}
    if with_state:
        for i in range(state[0], state[1]):
            S1, IF, S0, MJ, T1 = (m.word('%s_%d' % (n, i)) for n in ('S1', 'IF', 'S0', 'MJ', 'T1'))
            rs = i in relax_steps and 'S' in relax_kinds; rb = i in relax_steps and 'B' in relax_kinds
            m.sigma(E[i - 1], 6, 11, 25, False, S1, relax=rs)
            m.boolfn('IF', E[i - 1], E[i - 2], E[i - 3], IF, relax=rb)
            ex = i in exact_steps
            m.addn([E[i - 4], S1, IF, W[i], m.const_word(K[i]) if ex else None][:5 if ex else 4], T1, 't1_%d' % i, exact=ex)
            m.add(A[i - 4], T1, E[i], 'e_%d' % i)
            if ex: m.exact_add(A[i - 4], T1, E[i])
            m.sigma(A[i - 1], 2, 13, 22, False, S0, relax=rs)
            m.boolfn('MAJ', A[i - 1], A[i - 2], A[i - 3], MJ, relax=rb)
            m.addn([T1, S0, MJ], A[i], 'a_%d' % i, exact=ex)
        for i in range(state[0] - 4, state[0]):
            if zero_start: m.zero_diff(A[i]); m.zero_diff(E[i])
        for i in range(state[1] - 8, state[1]): m.zero_diff(A[i])
        for i in range(state[1] - 4, state[1]): m.zero_diff(E[i])
    m.W, m.A, m.E = W, A, E
    return m


def decode(m, model_set, words):
    rows = {}
    for name in words:
        w = m.words[name]; s = ''
        for j in range(B - 1, -1, -1):
            v, d = w[j]
            s += ('u' if v in model_set else 'n') if d in model_set else '='
        rows[name] = s
    return rows
```

### vmodel.py

```python
"""Exact value-level two-member model of SHA-256 rows 0..15 for a given signed characteristic
(own code). Member x is computed exactly; member y's words are x XOR (difference mask) with the
sign bits fixed ('u': x bit 1, 'n': x bit 0), and y's rows are also computed exactly, so every
difference of the characteristic holds with real carries. Free: A0..A6 (with A_-4..A_-1, E_-4..E_-1
implied by the Step-2 bijection, they need not be modeled), W7..W15. Rows 4..6 E words are derived
from A0..A6 (E_i = A_i + A_{i-4} - S0(A_{i-1}) - MAJ(A_{i-1}, A_{i-2}, A_{i-3}), i >= 4)."""
from pysat.formula import IDPool
K = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
     0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
     0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
     0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
     0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85]
B = 32


class V:
    XOR_NATIVE = False
    def __init__(self):
        self.pool = IDPool(); self.cl = []; self.xors = []
        self.T = self.pool.id('TRUE'); self.cl.append([self.T])

    def new(self, n=B, tag=None):
        return [self.pool.id() for _ in range(n)]

    def const(self, c):
        return [self.T if (c >> j) & 1 else -self.T for j in range(B)]

    def xor2(self, a, b):
        o = self.pool.id()
        if V.XOR_NATIVE: self.xors.append([a, b, -o]); return o      # a ^ b ^ ~o = 1  <=>  o = a ^ b
        self.cl += [[-a, -b, -o], [a, b, -o], [a, -b, o], [-a, b, o]]
        return o

    def xor3(self, a, b, c):
        o = self.pool.id()
        if V.XOR_NATIVE: self.xors.append([a, b, c, -o]); return o
        for s in range(8):
            x, y, z = s & 1, s >> 1 & 1, s >> 2 & 1
            r = x ^ y ^ z
            self.cl.append([(-a if x else a), (-b if y else b), (-c if z else c), (o if r else -o)])
        return o

    def maj(self, a, b, c):
        o = self.pool.id()
        self.cl += [[-a, -b, o], [-a, -c, o], [-b, -c, o], [a, b, -o], [a, c, -o], [b, c, -o]]
        return o

    def ifn(self, e, f, g):
        o = self.pool.id()
        self.cl += [[-e, -f, o], [-e, f, -o], [e, -g, o], [e, g, -o]]
        return o

    def add(self, a, b):
        out, c = [], None
        for j in range(B):
            if c is None:
                out.append(self.xor2(a[j], b[j])); c = self.and2(a[j], b[j])
            else:
                out.append(self.xor3(a[j], b[j], c))
                if j < B - 1: c = self.maj(a[j], b[j], c)
        return out

    def and2(self, a, b):
        o = self.pool.id()
        self.cl += [[-a, -b, o], [a, -o], [b, -o]]
        return o

    def addn(self, ws):
        acc = ws[0]
        for w in ws[1:]: acc = self.add(acc, w)
        return acc

    def neg(self, w):  # two's complement: ~w + 1
        return self.add([-x for x in w], self.const(1))

    def rot(self, w, n): return w[n:] + w[:n]

    def S0(self, w): return [self.xor3(*t) for t in zip(self.rot(w, 2), self.rot(w, 13), self.rot(w, 22))]
    def S1(self, w): return [self.xor3(*t) for t in zip(self.rot(w, 6), self.rot(w, 11), self.rot(w, 25))]
    def s0(self, w): return [self.xor3(*t) for t in zip(self.rot(w, 7), self.rot(w, 18), w[3:] + [-self.T] * 3)]
    def s1(self, w): return [self.xor3(*t) for t in zip(self.rot(w, 17), self.rot(w, 19), w[10:] + [-self.T] * 10)]
    def IF(self, e, f, g): return [self.ifn(*t) for t in zip(e, f, g)]
    def MAJ(self, a, b, c): return [self.maj(*t) for t in zip(a, b, c)]

    def eq(self, a, b):
        for x, y in zip(a, b): self.cl += [[-x, y], [x, -y]]


def masks(row):
    """row MSB first -> (xor mask, sign fixes {bit: x value})"""
    m, fx = 0, {}
    for k, s in enumerate(row):
        j = B - 1 - k
        if s in 'un': m |= 1 << j; fx[j] = 1 if s == 'u' else 0
    return m, fx


def add_conditions(v, conds, Ax, Ex, W):
    """value conditions on member-x bits (rows <= 15, W7 excluded) as clauses forbidding disallowed tuples."""
    import itertools
    n = 0
    for c in conds:
        if c['key'] > 15 or any(k == 'W' and i == 7 for k, i, b in c['refs']): continue
        lits = []
        for k, i, b in c['refs']:
            src = {'A': Ax, 'E': Ex, 'W': W}[k]
            if i not in src: lits = None; break
            lits.append(src[i][b])
        if lits is None: continue
        allowed = set(map(tuple, c['allowed']))
        for t in itertools.product((0, 1), repeat=len(lits)):
            if t not in allowed:
                v.cl.append([(-l if bit else l) for l, bit in zip(lits, t)])
        n += 1
    return n


def dense_model(char, last=15, extra_rows=(), free_rows=(), skip=(), free_signs=False, expansion=False):
    """char: {row: {'A': str, 'E': str, 'W': str}} for rows 0..last (signed differences only are used)."""
    v = V()
    A = {i: v.new() for i in range(0, 7)}          # member x A0..A6 (equal in y: rows < 7 carry no difference)
    W = {i: v.new() for i in range(7, last + 1)}   # member x W7..W15
    # E4..E6 from A0..A6
    E = {3: v.new()}                              # E3 is free (it fixes A_-1 of the chaining value)
    for i in (4, 5, 6):
        E[i] = v.addn([A[i], A[i - 4], v.neg(v.S0(A[i - 1])), v.neg(v.MAJ(A[i - 1], A[i - 2], A[i - 3]))])
    def ymask(w, row):
        m, fx = masks(row)
        if not free_signs:
            for j, val in fx.items(): v.cl.append([w[j] if val else -w[j]])
        return [(-x if (m >> j) & 1 else x) for j, x in enumerate(w)]
    Wy = {i: ymask(W[i], char[i]['W']) for i in W}
    # rows 4..6: no differences allowed
    for i in (4, 5, 6):
        assert set(char[i]['E']) <= set('=01+-') and set(char[i]['A']) <= set('=01+-'), i
    Ax = dict(A); Ex = dict(E); Ay = dict(A); Ey = dict(E)
    for i in range(7, last + 1):
        for (AA, EE, WW) in ((Ax, Ex, W), (Ay, Ey, Wy)):
            T1 = v.addn([EE[i - 4], v.S1(EE[i - 1]), v.IF(EE[i - 1], EE[i - 2], EE[i - 3]), v.const(K[i]), WW[i]])
            EE[i] = v.add(AA[i - 4], T1)
            AA[i] = v.addn([T1, v.S0(AA[i - 1]), v.MAJ(AA[i - 1], AA[i - 2], AA[i - 3])])
        # link: y = x XOR mask with signs fixed (rows in free_rows: no link, the trail is whatever the values give)
        if i in free_rows: continue
        for nm, X, Y in (('A', Ax, Ay), ('E', Ex, Ey)):
            if (nm, i) in skip: continue
            m, fx = masks(char[i][nm])
            for j, val in fx.items(): v.cl.append([X[i][j] if val else -X[i][j]])
            v.eq(Y[i], [(-x if (m >> j) & 1 else x) for j, x in enumerate(X[i])])
    if expansion:   # modular conditions of the expansion on the dense words (dW17 = dW24 = dW26 = dW30 = 0)
        def diff(fx, fy): return v.add(fy, v.neg(fx))
        zero = v.const(0)
        v.eq(v.add(diff(v.s1(W[15]), v.s1(Wy[15])), diff(W[10], Wy[10])), zero)
        v.eq(v.add(diff(v.s0(W[9]), v.s0(Wy[9])), diff(W[8], Wy[8])), zero)
        v.eq(v.add(diff(v.s0(W[11]), v.s0(Wy[11])), diff(W[10], Wy[10])), zero)
        v.eq(v.addn([diff(v.s0(W[15]), v.s0(Wy[15])), diff(W[9], Wy[9]), diff(v.s0(W[8]), v.s0(Wy[8])), diff(W[7], Wy[7])]), zero)
    v.A, v.E, v.W, v.Ay, v.Ey, v.Wy = Ax, Ex, W, Ay, Ey, Wy
    return v


def value(model_set, w):
    """model_set: set of true positive literals"""
    return sum(1 << j for j, x in enumerate(w) if (x > 0 and x in model_set) or (x < 0 and (-x) not in model_set))


def write_dimacs(v, fn):
    """CNF plus CryptoMiniSat native XOR lines ('x' prefix: XOR of literals = true)."""
    with open(fn, 'w') as f:
        f.write('p cnf %d %d\n' % (v.pool.top, len(v.cl) + len(v.xors)))
        for c in v.cl: f.write(' '.join(map(str, c)) + ' 0\n')
        for x in v.xors: f.write('x' + ' '.join(map(str, x)) + ' 0\n')
```

### sha38.py

```python
"""Independent reduced-round SHA-256 (FIPS 180-4) with full trace, written from the spec."""
M32 = 0xFFFFFFFF
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
IV = (0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19)


def ror(x, n):
    return ((x >> n) | (x << (32 - n))) & M32


def S0(x): return ror(x, 2) ^ ror(x, 13) ^ ror(x, 22)
def S1(x): return ror(x, 6) ^ ror(x, 11) ^ ror(x, 25)
def s0(x): return ror(x, 7) ^ ror(x, 18) ^ (x >> 3)
def s1(x): return ror(x, 17) ^ ror(x, 19) ^ (x >> 10)
def CH(x, y, z): return (x & y) ^ (~x & z & M32)
def MAJ(x, y, z): return (x & y) ^ (x & z) ^ (y & z)


def expand(W16, n):
    W = list(W16)
    for i in range(16, n):
        W.append((s1(W[i - 2]) + W[i - 7] + s0(W[i - 15]) + W[i - 16]) & M32)
    return W


def trace(cv, W16, rounds=38):
    """Return (A, E, W, out) with A[i], E[i] indexed i = -4..rounds-1 via dict."""
    a, b, c, d, e, f, g, h = cv
    A = {-1: a, -2: b, -3: c, -4: d}
    E = {-1: e, -2: f, -3: g, -4: h}
    W = expand(W16, rounds)
    for i in range(rounds):
        T1 = (h + S1(e) + CH(e, f, g) + K[i] + W[i]) & M32
        T2 = (S0(a) + MAJ(a, b, c)) & M32
        h, g, f = g, f, e
        e = (d + T1) & M32
        d, c, b = c, b, a
        a = (T1 + T2) & M32
        A[i], E[i] = a, e
    out = tuple((x + y) & M32 for x, y in zip(cv, (a, b, c, d, e, f, g, h)))
    return A, E, W, out


def compress(cv, W16, rounds=38):
    return trace(cv, W16, rounds)[3]
```

### mkpkg4.py

```python
#!/usr/bin/env python3
"""mkpkg4.py <sha2-search dir> <candidate dir> <q3_model> <q3 threshold> [options]: proof.md, claim.json, dependencies.json and
experiments/ of the A0-variant package with the characteristic P8, 32 classes and per-class row-16 programs (successor of the package
filed as 1a695f0b, generated by mkpkg3.py).  Every number in the prose that derives from data is read from the run files listed in the
INPUTS block below (each overridable on the command line) or recomputed here; a value that cannot be computed from files is a required
option.  Without --allow-missing the generator stops before writing anything if an input is missing or inconsistent, and lists them.
With --allow-missing it writes a dry-run package with **TODO(...)** markers and a banner listing every missing or provisional input."""
import sys
sys.dont_write_bytecode = True
import argparse, json, re, glob, math, statistics as st, hashlib, os, shutil, collections, random, importlib.util
from fractions import Fraction as Fr

# ---- inputs (paths relative to the sha2-search dir) ----
INPUTS = dict(
    q3dir='runs/q3p8_32',                       # q3 study: out_<seed>.txt (q3tv2, DIFFROW=19 RELAX_TAIL=1, VARS = the class pool)
    h3glob='runs/a0p32/h3_first750/h3_*.txt',   # pair term, charged sample (h3p.py output; last line a dict)
    h3spread='runs/a0p32/h3_*.txt',             # pair term, cross-check sample spread over all runs (SPREAD=750)
    devdir='runs/a0p32/dev',                    # replica development requests (dev_*.txt)
    calib='runs/a0p32/calibrate.json',          # executed counts of experiments/a0p38.py (prog = list of per-class counts)
    valid='runs/a0p32/validation.txt',          # our validation of the shipped experiments
    memory='runs/a0p32/memory.txt',             # memory record
    pat19='runs/a0p32/pat19.txt',               # row-19 patterns of the study's successes
    selftest='runs/a0p32/selftest.txt',         # selftest output of the shipped program
    classes='runs/lp/P8_32/classes.txt',        # c7 base size mask (lp_classes.py, ALLMAX=1)
    vars='runs/lp/P8_32/vars_pool.txt',         # the variant pool of the selected classes
    derived='runs/lp/P8_32/derived.json',       # lp_classes.py summary (number of largest classes etc.)
    exp='runs/a0p32/a0p38.py',                  # the shipped program
    fam='runs/a0p/a0fam_p08.txt',               # A0-variant family of S (same S as 1a695f0b)
    sweep='runs/a0p/sweep_summary.txt',         # sign sweep summary (same as 1a695f0b)
    char='runs/c/SW_p08_k1_j43.char.json',      # the characteristic P8
    sfs='runs/c/P08.sfs_pair.json',             # the semi-free-start pair
    ref_calib='runs/a0p/calibrate.json',        # 1a695f0b's calibration (8 classes, one shared program): reference rows
    ref_classes='runs/p08_classes.txt',         # 1a695f0b's 8 classes (c7 base size): reference rows
)
# ---- reference values of earlier packages (filed numbers, used for comparison and checked where recomputable) ----
REF = dict(id='1a695f0b', q3=-97.0, h3=-5.9, claim=87.22358, mem=28.10, score=95.32358, shared_prog=1511, mask=0x7fe96c7c)
FB = dict(q3=-97.7838, variants='345,600', g='23,118.75', prog='1,410 to 1,426', claim='87.90375', mem='2^28 (online 1,044,992 bytes)', score='95.90375')
# ---- study parameters (q3tv2 command-line arguments; not recorded in the out files; see DOWNSTREAM_RUNBOOK.md) ----
STUDY = dict(seed0=4001, nruns=20, particles=4000, tail=16384)
SRC = ['ledger_a0p.py', 'lp_classes.py', 'a0cls.c', 'a0p_ref.py', 'a0p_core.py', 'a0p_prog.py', 'a0p_scal.py', 'a0p_run.py', 'a0p_main.py',
       'mka0p.py', 'mkvt.py', 'a0fam.c', 'h3p.py', 'q3tv.c', 'sweep.py', 'stepk.py', 'score.py', 'joint.py', 'fromjoint.py', 'prep.py', 'cond.py',
       'sdmodel.py', 'vmodel.py', 'sha38.py', 'mkpkg4.py']
DEPS_UUID = {'2d1c4fc2': '2d1c4fc2-7bdd-4b92-af0c-f0c041883b07', 'fb176310': 'fb176310-a5ab-4671-b610-23d90f5a3814',
             '242fcec3': '242fcec3-3fb4-41a4-b808-945e2a75ced1', '49b543d1': '49b543d1-5b0d-48fa-bf34-a09503d37231',
             '1a695f0b': '1a695f0b-4221-4159-b01f-a145022b5334', '08be594': None}     # 08be594: full id via --dep-08be594

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument('R'); ap.add_argument('OUT'); ap.add_argument('q3_model', type=float); ap.add_argument('q3_threshold', type=float)
for k, v in INPUTS.items(): ap.add_argument('--' + k.replace('_', '-'), dest=k, default=v, help='default %(default)s')
for k, v in STUDY.items(): ap.add_argument('--' + k, dest=k, type=int, default=v, help='default %(default)s')
ap.add_argument('--rebuilt-checked', default=None, help='rebuild check of the study successes, e.g. "300 of 300" (not in the run files)')
ap.add_argument('--core-seconds-log2', type=float, default=None, help='bound (log2) on all core-seconds of search and development (H4)')
ap.add_argument('--dep-08be594', default=None, help='full submission id of 08be594 (johnservil)')
ap.add_argument('--allow-missing', action='store_true', help='write a dry-run package with TODO markers instead of failing')
A = ap.parse_args()
R, OUT, Q3M, THR = A.R, A.OUT, A.q3_model, A.q3_threshold
P_ = lambda k: os.path.join(R, getattr(A, k))
sys.path.insert(0, R + '/m38')
from ledger_a0p import ledger

MISSING, PROVISIONAL = [], []
def miss(what): MISSING.append(what)
def todo(name): return '**TODO(%s)**' % name
def rd(k):
    p = P_(k)
    if not os.path.isfile(p) or os.path.getsize(p) == 0: miss('%s: %s' % (k, p)); return None
    return open(p).read().rstrip('\n')
c = lambda n: f'{n:,}'
cg = lambda g: c(int(g)) if float(g) == int(g) else c(round(float(g), 2))   # good pairs per first block
nz = lambda s: ''.join(ch if ch in 'un' else '=' for ch in s)
WORDS = {1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six', 7: 'seven', 8: 'eight', 9: 'nine', 10: 'ten'}
wd = lambda n: WORDS.get(n, str(n))
pop = lambda x: bin(x).count('1')

# ---- fixed inputs (same P8 and S as 1a695f0b) ----
CH = {int(k): v for k, v in json.load(open(P_('char'))).items()}
PUB = {int(k): v for k, v in json.load(open(R + '/m38/paper_table3.json')).items()}
SFS = json.load(open(P_('sfs')))
FAM, SWEEP = rd('fam'), rd('sweep')
for f in SRC:
    if not os.path.isfile(R + '/m38/' + f): miss('source m38/' + f)

# ---- the shipped program ----
VT = P_('exp')
spec = importlib.util.spec_from_file_location('a0p38', VT); AP = importlib.util.module_from_spec(spec); spec.loader.exec_module(AP)
SHB = pop(AP.SHARED)
vt_src = open(VT).read(); vt_hash = hashlib.sha256(open(VT, 'rb').read()).hexdigest(); vt_size = os.path.getsize(VT)
if AP.Q3_THRESH != THR: miss('inconsistent: Q3_THRESH = %s in %s, q3 threshold argument %s' % (AP.Q3_THRESH, VT, THR))

# ---- classes ----
CLS = [l.split() for l in open(P_('classes')) if l.strip()]
assert all(len(x) == 4 for x in CLS), 'classes.txt needs four columns (c7 base size mask): run lp_classes.py with ALLMAX=1'
CLS = [(int(a, 16), int(b, 16), int(n), int(m, 16)) for a, b, n, m in CLS]
ncl = len(CLS); sizes = sorted({n for _, _, n, _ in CLS}); nvar = sum(n for _, _, n, _ in CLS)
assert len(sizes) == 1, 'classes of different sizes: the ledger assumes one class size'
csize = sizes[0]; nb = csize // 256
maskcnt = collections.Counter(m for _, _, _, m in CLS); masks_desc = ', '.join('%08x (%d bits) x %d' % (m, pop(m), n) for m, n in sorted(maskcnt.items(), key=lambda t: (-t[1], -t[0])))
wmin, wmax = min(pop(m) for m in maskcnt), max(pop(m) for m in maskcnt); widest = max(maskcnt, key=lambda m: (pop(m), m))
DER = json.load(open(P_('derived')))
nlargest = DER['n_largest']
assert DER['class_size'] == csize
if [(a, b, m) for a, b, _, m in CLS] != [tuple(x) for x in AP.CLASSES]: miss('inconsistent: CLASSES of %s differ from %s' % (VT, P_('classes')))
if AP.CLASS_SIZE != csize: miss('inconsistent: CLASS_SIZE of %s' % VT)
pool_n = 0; pool_cls = set()
with open(P_('vars')) as f:
    for l in f: pool_n += 1; pool_cls.add(l.split(' ', 1)[0])
if pool_n != nvar or len(pool_cls) != ncl: miss('inconsistent: %s has %d variants of %d classes, classes.txt %d of %d' % (P_('vars'), pool_n, len(pool_cls), nvar, ncl))
# 1a695f0b's classes (reference) and our per-class programs for them
RCLS = [l.split() for l in open(P_('ref_classes')) if l.strip()]
ref_idx = [next(i for i, x in enumerate(AP.CLASSES) if x[0] == int(a, 16) and x[1] == int(b, 16)) for a, b, _ in RCLS]
ref_nvar = sum(int(n) for _, _, n in RCLS)
ref_progs = [len(AP.program(i)) - 1 for i in ref_idx]

# ---- calibration (cross-checked against the shipped program) ----
CAL_LIVE = AP.calibrate()
CALT = rd('calib')
if CALT is None:
    CAL = CAL_LIVE; PROVISIONAL.append('calibration computed by calibrate() of %s (no %s)' % (VT, P_('calib')))
else:
    CAL = json.loads(CALT)
    if CAL != CAL_LIVE: miss('inconsistent: %s differs from calibrate() of %s' % (P_('calib'), VT))
CALREF = json.load(open(P_('ref_calib')))
progs = CAL['prog']; assert isinstance(progs, list) and len(progs) == ncl == CAL['classes'] and CAL['class_size'] == csize
pmean = Fr(sum(progs), ncl); pmin, pmax = min(progs), max(progs); ndistinct = len({tuple(AP.cbits(i)) for i in range(ncl)})
# the lane cost, itemised from the shipped routines
_m = AP.Mach(); AP.lane_value(_m, {j: 0 for j in range(32)}, 0, widest, 0); n_lv = _m.ops
_m = AP.Mach(); _sc = AP.fb_scalars(_m, [1] * 8); _m = AP.Mach(); AP.scalar_e16(_m, _sc, AP.members(0, 1)[0]); n_e16 = _m.ops
assert 32 + AP.LANE_CTL + n_lv + n_e16 + 42 == CAL['lane'], 'lane cost does not itemise'
# the replica's embedded variant sample
VS = AP.vsample(); vs_cls = collections.Counter(AP.class_of(a) for a in VS)
if None in vs_cls: miss('inconsistent: %d embedded replica samples are not in a selected class' % vs_cls[None])

# ---- q3 study ----
RUNS, STALLED, qmiss = [], [], []
seeds = list(range(A.seed0, A.seed0 + A.nruns))
for sd in seeds:
    f = '%s/out_%d.txt' % (P_('q3dir'), sd); t = open(f).read() if os.path.isfile(f) else ''
    mv = re.search(r'variants (\d+)', t)
    if mv and int(mv.group(1)) != nvar: miss('inconsistent: %s used %s variants, the classes have %d' % (f, mv.group(1), nvar))
    m = re.search(r'seed (\d+) .*stages (.*) \| succ (\d+) coll (\d+) \| log2q (-?[\d.]+)', t)
    if m: RUNS.append((int(m.group(1)), m.group(2), int(m.group(3)), int(m.group(4)), float(m.group(5))))
    elif re.search(r'seed %d stalled' % sd, t):
        s = re.search(r'seed (\d+) (stalled.*)', t); RUNS.append((sd, s.group(2) + ' (no estimate: counted as 0)', 0, 0, None)); STALLED.append((sd, s.group(2)))
    else: qmiss.append(sd)
if qmiss: miss('q3 study %s: %d of %d runs not finished (seeds %s)' % (P_('q3dir'), len(qmiss), A.nruns, ' '.join(map(str, qmiss))))
nq = len(RUNS)
def t_quant(p, v):
    lc = math.lgamma((v + 1) / 2) - math.lgamma(v / 2) - 0.5 * math.log(v * math.pi)
    pdf = lambda x: math.exp(lc - (v + 1) / 2 * math.log1p(x * x / v))
    def cdf(x, n=4000):
        h = x / n; return 0.5 + h / 3 * sum(pdf(i * h) * (1 if i in (0, n) else 4 if i % 2 else 2) for i in range(n + 1))
    lo, hi = 0.0, 50.0
    for _ in range(60):
        mid = (lo + hi) / 2; lo, hi = (mid, hi) if cdf(mid) < p else (lo, mid)
    return (lo + hi) / 2
if nq >= 2:
    qs = [2 ** r[4] if r[4] is not None else 0.0 for r in RUNS]; qm = sum(qs) / nq; qsd = st.stdev(qs); tq = t_quant(0.99, nq - 1)
    qlo = math.log2(qm - tq * qsd / math.sqrt(nq))
    rr = random.Random(1); bs = sorted(math.log2(sum(rr.choice(qs) for _ in qs) / nq) for _ in range(20000)); qbs = bs[200]
    qsucc = sum(r[2] for r in RUNS)
    if not all(r[2] == r[3] for r in RUNS): miss('inconsistent: a study run has successes that are not collisions')
    stg = [list(map(float, r[1].split())) for r in RUNS if r[4] is not None]
    lab = ['16', '17', '18', '19', '20', '21', '22', 'tail'] if all(len(x) == 8 for x in stg) else None
    if lab and len(stg) >= 2:
        sds = [st.stdev(x[k] for x in stg) for k in range(8)]; kmax = max(range(1, 8), key=lambda k: sds[k])
        spread = 'The %s stage has the largest spread across the runs (sd %.2f bits of its log2 factor; the others at most %.2f)' % (
            ('row-%s' % lab[kmax]) if lab[kmax] != 'tail' else 'tail', sds[kmax], max(sds[k] for k in range(1, 8) if k != kmax))
    else: spread = todo('stage spread')
    S_q = dict(mean='%.4f' % math.log2(qm), rsd='%.3f' % (qsd / qm), t='%.4f' % tq, df=str(nq - 1), lo='%.4f' % qlo, bs='%.4f' % qbs, succ=c(qsucc), n=str(nq))
    if qmiss: PROVISIONAL.append('q3 study statistics over %d of %d runs' % (nq, A.nruns))
else:
    qm = None; spread = todo('stage spread'); S_q = {k: todo('q3 study') for k in ('mean', 'rsd', 't', 'df', 'lo', 'bs', 'succ', 'n')}
stall_txt = (('Run%s %s found no survivor at row %s and %s counted as an estimate of 0.' % ('s' if len(STALLED) > 1 else '', ' and '.join(str(sd) for sd, _ in STALLED),
              '/'.join(sorted({x.split()[-1] for _, x in STALLED})), 'are' if len(STALLED) > 1 else 'is')) if STALLED else 'No run stalled.')
seed_txt = '%d..%d' % (seeds[0], seeds[-1])

# ---- replica development requests ----
DEV = []
for f in sorted(glob.glob(P_('devdir') + '/dev_*.txt')):
    for l in open(f):
        t = l.split()
        if len(t) >= 14: DEV.append((int(t[0]), float(t[1]), int(t[2]), int(t[3]), [None if v == 'None' else float(v) for v in t[4:14]]))
if DEV:
    reps = [z for d in DEV for z in d[4]]; rmean = math.log2(sum(2 ** z if z is not None else 0.0 for z in reps) / len(reps))
    pm = sorted(d[1] for d in DEV); rs = [sum(z is not None for z in d[4]) for d in DEV]
    S_d = dict(n=str(len(DEV)), nrep=str(len(reps)), min='%.3f' % pm[0], q5='%.3f' % pm[int(0.05 * len(pm))], med='%.3f' % ((pm[(len(pm) - 1) // 2] + pm[len(pm) // 2]) / 2),
               rmean='%.4f' % rmean, rs='%d to %d' % (min(rs), max(rs)))
    mm = re.search(r'fixed from (\d+) development requests', vt_src)
    if mm and int(mm.group(1)) != len(DEV): miss('inconsistent: %s says the pass rule was fixed from %s development requests, %s has %d' % (VT, mm.group(1), P_('devdir'), len(DEV)))
else:
    miss('replica development requests: %s/dev_*.txt' % P_('devdir')); S_d = {k: todo('dev') for k in ('n', 'nrep', 'min', 'q5', 'med', 'rmean', 'rs')}

# ---- replica power (approximation: a lower q3 shifts the replica's pooled means) ----
_dv = sorted(float(l.split()[1]) for f in glob.glob(os.path.join(P_('devdir'), 'dev_*.txt')) for l in open(f) if len(l.split()) > 2)
POW = {sh: sum(1 for x in _dv if x - sh < THR) / len(_dv) for sh in (0, 1, 2, 3)} if _dv else {}
# ---- pair term ----
H3 = collections.Counter(); h3f = glob.glob(P_('h3glob'))
for f in h3f:
    d = eval(open(f).read().strip().split('\n')[-1]); H3.update(d)
def pois_up(k, a=0.01):
    lo, hi = 0.0, 100.0 + 10 * k
    for _ in range(200):
        mid = (lo + hi) / 2; cdf = sum(math.exp(-mid) * mid ** i / math.factorial(i) for i in range(k + 1))
        lo, hi = (mid, hi) if cdf > a else (lo, mid)
    return hi
if h3f and H3['verified']:
    h3lim = pois_up(H3['other_r16']) / H3['verified']; H3B = math.ceil(math.log2(h3lim) * 10) / 10 + 0.5
    if not (H3['verified'] == H3['successes'] == H3['own_found']): miss('inconsistent: pair-term run has unverified or not re-found successes (%s)' % dict(H3))
    dis = 1 - 0.01 ** (1 / H3['verified'])
    S_h = dict(succ=c(H3['successes']), own=c(H3['own_found']), pc=c(H3['passing_classes']), var=c(H3['variants']), r16=str(H3['other_r16']),
               acc=str(H3['other_accepted']), exp='%.2f' % (H3['variants'] * 160 / 2 ** 32), lim='%.4f' % h3lim, llim='%.2f' % math.log2(h3lim),
               H3B='%.1f' % H3B, ver=c(H3['verified']), dis='%.1f%%' % (100 * dis))
    H3S = collections.Counter()
    for f in glob.glob(P_('h3spread')): H3S.update(eval(open(f).read().strip().split('\n')[-1]))
    if H3S['verified']:
        h3lims = pois_up(H3S['other_r16']) / H3S['verified']
        S_h['spread'] = ('A second sample of %s successes spread evenly over all %d runs (`SPREAD=%d`; every success of the sorted dump files, '
            'equally spaced) gives %s verified, %s passing classes, %s variants, %s other row-16 passes, %s further accepted pairs: 99%% limit 2^%.2f, '
            'charge 2^%.1f by the same rule. We charge the larger value, that of the first sample.') % (c(H3S['successes']), A.nruns, H3S['successes'],
            c(H3S['verified']), c(H3S['passing_classes']), c(H3S['variants']), H3S['other_r16'], H3S['other_accepted'], math.log2(h3lims),
            math.ceil(math.log2(h3lims) * 10) / 10 + 0.5)
        H3B = max(H3B, math.ceil(math.log2(h3lims) * 10) / 10 + 0.5); S_h['H3B'] = '%.1f' % H3B
    else: S_h['spread'] = ''
else:
    miss('pair term: %s' % P_('h3glob')); H3B = REF['h3']; PROVISIONAL.append('pair term h3 = %.1f (the value of %s) for the ledger' % (H3B, REF['id']))
    S_h = {k: todo('pair term') for k in ('succ', 'own', 'pc', 'var', 'r16', 'acc', 'exp', 'lim', 'llim', 'ver', 'dis')}; S_h['H3B'] = '%.1f %s' % (H3B, todo('pair term'))

# ---- memory ----
MEM = rd('memory')
if MEM:
    memonline = int(re.search(r'online (\d+)', MEM).group(1)); mempre = float(re.search(r'preprocessing peak 2\^([\d.]+)', MEM).group(1))
    memclaim = math.ceil(max(mempre, math.log2(memonline)) * 100) / 100
    if 'lp_classes' not in MEM: miss('memory record %s does not cover lp_classes.py (class selection)' % P_('memory'))
    S_m = dict(online=c(memonline))
else:
    memclaim = REF['mem']; PROVISIONAL.append('memory 2^%.2f (the value of %s; no memory record)' % (memclaim, REF['id'])); S_m = dict(online=todo('memory'))

# ---- remaining files ----
SELF, VAL, PAT19 = rd('selftest'), rd('valid'), rd('pat19')
if SELF and 'SELFTEST PASSED' not in SELF: miss('selftest did not pass: %s' % P_('selftest'))
if PAT19:
    pats = re.findall(r'^\s*([\d,]+)\s+([01]{8,})\s', PAT19, re.M)
    mp = re.search(r'([\d,]+) of ([\d,]+) successes in these (\w+) patterns', PAT19); ms = re.search(r'seeds (\d+)\.\.(\d+)', PAT19)
    if not ms or (int(ms.group(1)), int(ms.group(2))) != (seeds[0], seeds[-1]): miss('inconsistent: %s is not from the study seeds %s' % (P_('pat19'), seed_txt))
    npat = len(pats)
    S_p = dict(npat=wd(npat), cls=mp.group(1) if mp else todo('pat19 count'), tot=mp.group(2) if mp else todo('pat19 count'))
    S_p['all'] = mp is not None and mp.group(1) == mp.group(2)
else:
    S_p = dict(npat=todo('pat19'), cls=None, tot=todo('pat19'), all=False)
if VAL:
    on = [(int(a), int(b), float(t)) for a, b, t in re.findall(r'a0p-online-r38\s+returned\s+(\d+).*?mismatches (\d+).*?([\d.]+)s\s*$', VAL, re.M)]
    un = [(int(a), int(b), float(e)) for a, b, e in re.findall(r'unconditional: (\d+) first blocks, (\d+) class W7 passes \(expected ([\d.]+)\)', VAL)]
    UNC = dict(fb=c(sum(x[0] for x in un)), passes=c(sum(x[1] for x in un)), exp=c(round(sum(x[2] for x in un))), req=len(un),
               ratio='%.3f' % (sum(x[1] for x in un) / sum(x[2] for x in un))) if un else None
    if not un: miss('validation: no unconditional first-block counts (H1)')
    qv = [(float(p), float(r), int(s), int(n), int(fr)) for p, r, s, n, fr in re.findall(
        r'a0p-q3-r38\s+returned\s+\d+\s+pooled 2\^(-?[\d.]+) \(rule >= 2\^(-?[\d.]+)\)\s+replicates with a success (\d+)/(\d+)\s+verified pairs \d+\s+failed rebuilds (\d+)', VAL)]
    if any(r != THR for _, r, _, _, _ in qv): miss('inconsistent: validation used a different pass rule')
    S_v = dict(on_ret='%d to %d' % (min(x[0] for x in on), max(x[0] for x in on)) if on else todo('validation'), on_mis=str(sum(x[1] for x in on)) if on else todo('validation'),
               on_t='%.1f' % max(x[2] for x in on) if on else todo('validation'), q_rs='%d to %d' % (min(x[2] for x in qv), max(x[2] for x in qv)) if qv else todo('validation'),
               q_pool='%.3f to %.3f' % (min(x[0] for x in qv), max(x[0] for x in qv)) if qv else todo('validation'), n=str(len(qv)))
    if on and min(x[0] for x in on) == max(x[0] for x in on): S_v['on_ret'] = str(on[0][0])
else:
    S_v = {k: todo('validation') for k in ('on_ret', 'on_mis', 'on_t', 'q_rs', 'q_pool', 'n')}
REB = A.rebuilt_checked or todo('rebuild check of the study successes: --rebuilt-checked')
if not A.rebuilt_checked: miss('--rebuilt-checked (how many study successes were rebuilt and checked with the reference)')
CORE = ('%g' % A.core_seconds_log2) if A.core_seconds_log2 is not None else None
if CORE is None: miss('--core-seconds-log2 (H4: core-seconds of search and all development, including the 32-class study)')
CORE_S = CORE or todo('core-seconds, --core-seconds-log2')
DEP08 = A.dep_08be594 or DEPS_UUID['08be594']
if not DEP08: miss('--dep-08be594 (full submission id of 08be594)')

# ---- ledger and sensitivity ----
L = ledger(q3=Q3M, h3=H3B, cal=CAL); claim = L['claim']
score = claim + max(0.0, memclaim - 20)
pre_own = sum((1 << pop(m)) * 40 + nb * 256 * pop(m) * 2 for _, _, _, m in CLS) + 2 ** 32   # PRE with each class's own mask width
pre_note = ''
if pre_own != L['PRE']:
    from ledger_a0p import dlog2
    alt = math.ceil(float(dlog2(Fr(L['N'] - L['PRE'] + pre_own, 2728))) * 1e5) / 1e5
    if alt == claim:
        pre_note = '(the ledger counts 2^21 cube points and 21 planes per class, the width of %08x; with each class\'s own mask width PRE = %s and time_log2 is unchanged)' % (REF['mask'], c(pre_own))
        print('mkpkg4: note: ledger PRE uses 21-bit masks; own masks give PRE %s, time_log2 unchanged' % c(pre_own), file=sys.stderr)
    else:
        pre_note = todo('ledger PRE assumes 21-bit class masks; with each class\'s own mask PRE = %s and time_log2 = %.5f' % (c(pre_own), alt))
        miss('ledger_a0p.py PRE uses popcount(%08x) for every class; own masks give PRE %s instead of %s (time_log2 %.5f vs %.5f)' % (REF['mask'], c(pre_own), c(L['PRE']), alt, claim))
ref_shared = ledger(q3=REF['q3'], h3=REF['h3'], cal=CALREF, AC=48, AS=50, DEV=50)   # 1a695f0b's allowances
assert ref_shared['claim'] == REF['claim'], 'reference ledger does not reproduce %s' % REF['id']
ref_pc = ledger(q3=REF['q3'], h3=REF['h3'], cal=dict(CALREF, prog=ref_progs), AC=48, AS=50, DEV=50)
base = dict(q3=Q3M, h3=H3B, cal=CAL)
SENS = [('claimed', {})]
if qm: SENS.append(('q3_model = the study mean 2^%.4f' % math.log2(qm), dict(q3=round(math.log2(qm), 4))))
SENS += [('q3_model 2^-97.78 (the q3_model of fb176310 for the published characteristic)', dict(q3=-97.78)), ('pair term 2^-3', dict(h3=-3.0)),
         ('allowances of %s (A_C = 2^48, A_S = 2^50, DEV = 2^50)' % REF['id'], dict(AC=48, AS=50, DEV=50)), ('A_C = 2^84', dict(AC=84))]
sens = []
for nm, kw in SENS:
    x = ledger(**dict(base, **kw)); sens.append('%-96s %.5f   (N_FB 2^%.4f)' % (nm, x['claim'], x['log2NFB']))
    if nm == 'A_C = 2^84': ac84 = x['claim']
sens.append('%-96s %.5f   (reference)' % ('%s: %d classes, one shared program of %s, q3_model 2^%.1f, pair term 2^%.1f' % (REF['id'], len(RCLS), c(CALREF['prog']), REF['q3'], REF['h3']), ref_shared['claim']))
sens.append('%-96s %.5f   (reference)' % ('the same with per-class programs (08be594\'s construction; ours, %s..%s, mean %.2f)' % (c(min(ref_progs)), c(max(ref_progs)), sum(ref_progs) / len(ref_progs)), ref_pc['claim']))

if MISSING and not A.allow_missing:
    print('mkpkg4: missing or inconsistent inputs (nothing written):', file=sys.stderr)
    for x in MISSING: print('  - ' + x, file=sys.stderr)
    print('rerun with --allow-missing for a dry run with TODO markers', file=sys.stderr); sys.exit(2)

src = {f: open(R + '/m38/' + f).read() for f in SRC if os.path.isfile(R + '/m38/' + f)}
hs = {f: hashlib.sha256(open(R + '/m38/' + f, 'rb').read()).hexdigest() for f in src}
ref_g = len(RCLS) * int(RCLS[0][2]) * Fr(287309824, 2 ** 32)
pat_src = ('%s of %s' % (S_p['cls'], S_p['tot'])) if S_p['cls'] else todo('pat19')

P = []
def add(s=''): P.extend(s.split('\n'))
add('# 38-step SHA-256 collision with the characteristic P8 in the memory-efficient A0-variant attack, %d classes and per-class row-16 programs: time 2^%.5f, memory 2^%.2f bytes' % (ncl, claim, memclaim))
add('')
if MISSING or PROVISIONAL:
    add('> **DRY RUN: not for submission.** Missing or inconsistent inputs:')
    for x in MISSING: add('> - ' + x)
    for x in PROVISIONAL: add('> - provisional: ' + x)
    add('')
add('**Track** sha256-r38-exploratory, target sha256-r38-prefix-v1, cost model collision-frontier-v5 (C = 2728), scalar policy hashsmash-scalar-tm-v1 (score = time_log2 + max(0, memory_log2_bytes - 20)).')
add('**Claim** time_log2 = %.5f (exact total 2^%.6f target compressions), algorithmic success probability at least 0.39, memory 2^%.2f bytes (online %s bytes; the preprocessing peak, Section 11), preprocessing 2^%.5f, non-uniform advice below 2^14 bytes. Score under the scalar policy: %.5f.' % (claim, L['log2T'], memclaim, S_m['online'], L['pre_log2'], score))
add('')
add('## 0. Summary')
add('')
add('This package runs the memory-efficient A0-variant collision attack on 38-step SHA-256 (ePrint 2026/1120 and 2026/1080; the A0-variants, c7 classes, bit-sliced row-16 filter and accepted event with a direct output comparison of the public packages 2d1c4fc2 and fb176310) with **P8**, a characteristic we found ourselves (Section 3). It extends our filing %s (same P8, same Step-1 solution S); the changes are listed in Section 0.1. What is new against the published characteristic:' % REF['id'])
add('')
add('1. **The characteristic P8.** Found by our systematic sign sweep over the 24 message-difference XOR patterns of weight 25 (Section 3.2): XOR pattern 8 (not the published pattern 0), a different dense trail and a different signed message difference. Its printed-event probability (rows 16..37 follow the trail and its derived conditions) is 2^-99.56 against 2^-101.05 for the published characteristic, measured with the same estimator.')
add('2. **The accepted event.** Rows 16..22 of both members follow the trail, except that row 19 is checked on its signed differences only (not on its derived value conditions), and the two outputs after step 37 are compared directly (rows 23..37 untested). %s fall into %s row-19 condition patterns (Section 6.2).' % (('All %s estimator successes that were classified' % S_p['tot']) if S_p['all'] else ('%s estimator successes that were classified' % pat_src), S_p['npat']))
add('3. **The measured q3 for that event** over the variants of the selected classes: %s independent runs, mean 2^%s, one-sided 99%% Student bound 2^%s (bootstrap 2^%s); **q3_model = 2^%.4f**. The corresponding value of fb176310 for the published characteristic is 2^%.4f.' % (S_q['n'], S_q['mean'], S_q['lo'], S_q['bs'], Q3M, FB['q3']))
add('')
add('| | fb176310 (published characteristic) | %s (P8, %d classes) | this package (P8, %d classes) |' % (REF['id'], len(RCLS), ncl))
add('|---|---|---|---|')
add('| q3_model of the accepted event | 2^%.4f | 2^%.4f | 2^%.4f |' % (FB['q3'], REF['q3'], Q3M))
add('| selected variants, good pairs per first block | %s, %s | %s, %s | %s, %s |' % (FB['variants'], FB['g'], c(ref_nvar), cg(ref_g), c(nvar), cg(L['g'])))
add('| row-16 program per batch of 256 variants | %s instructions | %s instructions (one shared program) | %s to %s instructions (per class; mean %.2f) |' % (FB['prog'], c(CALREF['prog']), c(pmin), c(pmax), float(pmean)))
add('| time_log2 | %s | %.5f | **%.5f** |' % (FB['claim'], REF['claim'], claim))
add('| memory | %s | 2^%.2f | 2^%.2f (online %s bytes) |' % (FB['mem'], REF['mem'], memclaim, S_m['online']))
add('| score (scalar policy) | %s | %.5f | **%.5f** |' % (FB['score'], REF['score'], score))
add('')
add('### 0.1 Changes from %s' % REF['id'])
add('')
add('1. **All %d largest c7 classes.** %s used the %d classes of mask %08x (%s variants). This package uses every class of the maximal size %s of P8 (%d classes, %s variants), with %d different masks: %s. Good pairs per first block: %s (was %s).' % (ncl, REF['id'], len(RCLS), REF['mask'], c(ref_nvar), c(csize), ncl, c(nvar), len(maskcnt), masks_desc, cg(L['g']), cg(ref_g)))
add('2. **Per-class row-16 programs.** Each class gets its own bit-sliced row-16 program in which every bit of a0 outside the class\'s mask is the class\'s base bit, folded as a constant (Section 7.2). The idea is that of 08be594 (johnservil), which did it for the %d classes of %s; our implementation (`cbits`, `program` in `experiments/a0p38.py`) is our own. %d programs, %s to %s instructions, mean %.2f, against the shared program of %s instructions of %s. On the %d classes of %s alone this lowers time_log2 from %.5f to %.5f (Section 10).' % (len(RCLS), REF['id'], ncl, c(pmin), c(pmax), float(pmean), c(CALREF['prog']), REF['id'], len(RCLS), REF['id'], ref_shared['claim'], ref_pc['claim']))
add('3. **The F7 sampler of the organizer replica.** %s sampled W7 in F7 by its three affine families, choosing the family by `(w >> 4) %% 274` of the same random word whose bits then formed the value: the family choice was correlated with the value and had a modulo bias. Both were pointed out in 08be594 (johnservil). The replica now draws the family by rejection from its own word (9 bits, accepted below 274: shares 256, 16, 2, no bias) and the value bits from a fresh word (`f7_sample`; 200,000 draws: all in F7, family frequencies 93,187 + 93,579 / 11,769 / 1,465 against 186,861 / 11,679 / 1,460 expected). A generic rejection sampler on the definition is kept for other (D7, T7) only, as it is slower.' % REF['id'])
add('4. **Deterministic class selection.** The classes are selected by `lp_classes.py` (ALLMAX=1: every class of the largest size, ordered by c7) from the output of `a0cls.c`, replacing the hand-run selection of %s.' % REF['id'])
add('5. **Lane cost.** The scalar recovery of a0 from the stored planes costs 4 per mask bit; it is charged at the widest mask (%08x, %d bits): %d operations per stage-3a lane (was %d).' % (widest, pop(widest), CAL['lane'], CALREF['lane']))
add('6. **q3 re-measured** over the %s variants of the %d classes (seeds %s, Section 9). Memory %s: P8 and S are those of %s (Section 11).' % (c(nvar), ncl, seed_txt, ('is unchanged at 2^%.2f' % memclaim) if memclaim == REF['mem'] else ('changes from 2^%.2f to 2^%.2f' % (REF['mem'], memclaim)), REF['id']))
add('')
add('## 1. Target and cost model')
add('')
add('Target sha256-r38-prefix-v1: SHA-256 steps 0..37 on every padded block, the standard IV once, FIPS 180-4 padding, feed-forward, all eight digest words; output two distinct 128-byte messages M0 || M1 and M0 || M1\' with equal digests (the padding block is common). collision-frontier-v5: one target compression = 1 unit, every other word operation of the 256-bit word RAM 1/C, C = 2728; the scalar policy hashsmash-scalar-tm-v1 ranks time_log2 + max(0, memory_log2_bytes - 20).')
add('')
add('## 2. Sources, credit, and what is ours')
add('')
add('- ePrint 2026/1120 (Li, Zhang, Li, Liu, Qian, Zhu): the 38-step two-block framework and its memory-efficient Step 1-3 procedure, the message-difference shape (W7..W11, W15, W16, W23, W25), the published characteristic (comparison only). ePrint 2026/1080 [LLWS26]: the memory-efficient framework.')
add('- 2d1c4fc2 (itseasypop): A0-variants of the Step-1 solution, the c7 classes decided by one W7 test, the bit-sliced evaluation of the row-16 filter for 256 variants per word, the success analysis with a pair term and work caps. fb176310 (Jbenisek): the accepted event with a direct output comparison and alternative row-19 patterns, lowest-shared-bit stage 3a, the memory-free W7 test, a counted register allocator. We read their packages as documents; we executed none of their code. `experiments/a0p38.py` is our own implementation of that design for P8.')
add('- 08be594 (johnservil): per-class row-16 programs with the class\'s non-mask bits folded as constants (for the %d classes of %s), and the observation that the F7 sampler of %s\'s replica correlated the family choice with the value and had a modulo bias. Our per-class programs and the corrected sampler are our own implementation (for those 8 classes our per-class counts, [1466, 1457, 1469, 1466, 1463, 1454, 1466, 1463], equal the counts listed in 08be594\'s submission note).' % (len(RCLS), REF['id'], REF['id']))
add('- Ours: the characteristic P8 and the search that found it (signed-difference SAT model, sign sweep, joint coupling check), the condition derivation and estimators, the accepted event with row 19 on signed differences and its measurement, the class selection for P8 (`lp_classes.py`), the program `experiments/a0p38.py` (reference, bit-sliced program builder and allocator, counted scalar routines, replica, experiments), the ledger. Our filings 1db43310, 49b543d1 and 242fcec3 (table attack, NEW3) and %s (this attack with %d classes) are the earlier steps of this work.' % (REF['id'], len(RCLS)))
add('- Execution: everything ran in Linux containers on one 10-core machine (OrbStack; Ubuntu 22.04 for the C tools and solvers; the shipped program also on the official python:3.12.12-slim-bookworm image, Section 13).')
add('')
add('## 3. The characteristic P8')
add('')
add('### 3.1 The trail and a semi-free-start pair')
add('')
add('Signed differences (u: member x has 1, member y 0; n: the reverse), most significant bit first, rows -4..37, columns A_i, E_i, W_i (rows without a difference in all three words omitted: -4..6 and 26..37 are all `=`):')
add('')
add('```')
for i in range(6, 27): add('%4d  %s  %s  %s' % (i, nz(CH[i]['A']), nz(CH[i]['E']), nz(CH[i]['W'])))
add('```')
add('')
add('Conditions: for every bit of every boolean-function instance (S1, CH, S0, MAJ of the state; s0, s1 of the expansion) the trail fixes the input and output signed differences; the allowed values of the inputs without difference give the derived conditions (`cond.py`), which for P8 are all fixed bits or two-bit (in)equalities (the tables `_CH`, `PQ`, `X2` of `experiments/a0p38.py`, generated by `mkvt.py`; the conditions of rows 16..22, which define the accepted event, are listed in Appendix B). With W7 in F7 (D7 = 2^29, s0(W7y) - s0(W7x) = %08x: the same F7 as the published characteristic), the printed-event probability is 2^-99.56 (6 estimator runs of 2,000 particles; the published characteristic 2^-101.05 with the same estimator).' % AP.T7)
add('')
add('An explicit 38-step semi-free-start collision in the accepted event (Section 6), rebuilt from an estimator success and verified with the reference of `experiments/a0p38.py` (`selftest` item 1) and the organizer reference `verifier/hash_functions.py`; its rows 0..15 are the Step-1 solution S of Section 4 (A0 = %08x):' % SFS['a0'])
add('')
add('```')
add('CV1 = ' + ' '.join('%08x' % x for x in SFS['cv'])); add('M   = ' + ' '.join('%08x' % x for x in SFS['M'])); add("M'  = " + ' '.join('%08x' % x for x in SFS['M2'])); add('out = ' + ' '.join('%08x' % x for x in SFS['out']))
add('```')
add('')
add('### 3.2 How P8 was found (the sign sweep)')
add('')
add('Our signed-difference SAT model (`sdmodel.py`, `stepk.py`) was run over the 24 XOR patterns of weight 25 on the shape W7..W11, W15, W16, W23, W25, with the signs free, the dense part bounded by the published weight profile (HW(dA7..15) <= 26, HW(dE7..15) <= 47, HW(dE14..15) <= 4, HW(dA13..15) <= 10) and the tail by an attack-aware weight (P <= 43); every signed message difference already found for a pattern (and its member-swapped mirror) was blocked. Each solution went through the value-level coupling check (`joint.py`: value-exact dense part and value-exact tail steps 16..19) and the estimator (`sweep.py`). Summary (`runs/sweep`): ')
add('')
add('```'); add(SWEEP or todo('sweep')); add('```')
add('')
add('P8 = SW_p08_k1 (pattern 8, second iteration; search 4,714 s, coupling 662 s). For the A0-variant attack the relevant quantities are q3 of the accepted event and the c7 class structure (Sections 4-6); P8 has the best of both among the coupled characteristics.')
add('')
add('## 4. Step 1: the solution S and its A0-variants')
add('')
add('**Lemma 4.1 (Step 2).** For fixed state rows A0..A15, E4..E15 of both members and a chaining value CV1 = (A_{-1..-4}, E_{-1..-4}), the words W0..W7 with E_i = A_i + A_{i-4} - S0(A_{i-1}) - MAJ(A_{i-1}, A_{i-2}, A_{i-3}) (i = 0..3) and W_i = E_i - A_{i-4} - E_{i-4} - S1(E_{i-1}) - CH(E_{i-1}, E_{i-2}, E_{i-3}) - K_i (i = 0..7) reproduce the state rows; CV1 -> (W0, ..., W7) is a bijection (invert steps 7..0); W8..W15 do not depend on CV1. W0..W6 carry no difference (rows 0..6 have none), W7 differs by D7.')
add('')
add('**Lemma 4.2 (A0-variants).** Replace A0 of S by a0 in both members. Then E4 = a0 + C4 (C4 = A4 - S0(A3) - MAJ(A3, A2, A1)), W8 = W8C - E4 in each member (W8C = E8 - A4 - S1(E7) - CH(E7, E6, E5) - K8), so dW8 = W8y - W8x is unchanged, and all other words and rows 5..15 are unchanged. The variant is valid iff s0(W8y) - s0(W8x) also equals S\'s (W8 reaches rows >= 16 only through W23 = s1(W21) + W16 + s0(W8) + W7, W24 = s1(W22) + W17 + s0(W9) + W8 and the later words through them). G = {a0 : valid}; exhaustively (`a0fam.c`):')
add('')
add('```'); add(FAM or todo('a0fam')); add('```')
add('')
add('**c7 classes.** W7x = c7(a0) - A_{-1} with c7(a0) = E7 - 2 A3 + S0(A2) + MAJ(A2, A1, a0) - S1(E6) - CH(E6, E5, a0 + C4) - K7. For a chaining value, all variants with the same c7 share W7, so one F7 test decides a class. P8 has %d classes of the maximal size %s (the published characteristic: classes of 3,840). The attack uses %s: class i = {base_i ^ s : s subset of mask_i, base_i ^ s in G, c7(base_i ^ s) = c7_i}, %s members each (%d batches of 256), %s variants in all. The mask of a class is the set of bits on which its members vary (`lp_classes.py`: the OR of a0 ^ (smallest member)); the masks have %d to %d bits: %s.' % (
    nlargest, c(csize), ('all %d of them' % ncl) if ncl == nlargest else ('%d of them' % ncl), c(csize), nb, c(nvar), wmin, wmax, masks_desc))
add('')
add('| class | c7 | base | mask | members |'); add('|---|---|---|---|---|')
for k, (c7, b, n, m) in enumerate(CLS): add('| %d | %08x | %08x | %08x | %s |' % (k, c7, b, m, c(n)))
add('')
add('## 5. Step 2: the W7 test and the good pairs')
add('')
add('F7 = {w : s0(w + D7) - s0(w) = %08x}, |F7| = 287,309,824 (exhaustive), p7 = |F7| / 2^32 = 2^-3.90197 (the same set as for the published characteristic; it is the union of three affine families of 2^28, 2^24 and 2^21 words). The program tests w = c7 - A_{-1} by computing s0(w + D7) - s0(w) and comparing (%d operations, no table).' % (AP.T7, CAL['w7']))
add('')
add('**Lemma 5.1 (distribution, per variant).** Under H1, for every fixed a0: Pr[W7x in F7] = p7; conditioned on it, (W0..W6) is uniform and independent of W7, and (W16..W21) is a bijective image of (W0..W5) for fixed (W6, W9..W15), hence uniform and independent of (W6, W7) (Lemma 4.1). Per first block, E[good pairs] = g = %d x %s x p7 = %s (exact by linearity).' % (ncl, c(csize), cg(L['g'])))
add('')
add('## 6. Step 3: row 16 and the accepted event')
add('')
add('### 6.1 Row 16')
add('')
add('W16 = s1(W14) + W9 + s0(W1) + W0 and, by Lemma 4.1, W0 = a0 + KW0(CV1), W1 = K1(CV1) - S0(a0) - MAJ(a0, a, b) - S1(E0) - CH(E0, e, f) with E0 = a0 + HH(CV1). So E16x = KP + a0 + s0(W1) with per-first-block constants HH, KP, K1, and row 16 (both members, all its conditions) is a function of E16x alone: an exhaustive pass over all 2^32 values of W16 gives the %d words of the set R16 (`q3tv.c`, the exhaustive pass of `main`; `selftest` item 2 re-checks it on 20,000 random words and the bit-flip neighbours). The %d words share %d bits (mask %08x); the program tests the TK = %d lowest of them (bits %s): stage 3a passes with probability 2^-%d exactly (E16x uniform, Lemma 5.1), row 16 with %d / 2^32.' % (len(AP.R16), len(AP.R16), SHB, AP.SHARED, AP.TK, ', '.join(map(str, AP.TBITS)), AP.TK, len(AP.R16)))
add('')
add('### 6.2 The accepted event')
add('')
add('The program accepts a row-16 pass iff (i) rows 16..22 of both members follow every cell, \'+\' pair and two-bit condition of P8 closing at rows 16..22, except that **row 19 is checked on its signed differences only** (the XOR differences of A19, E19, W19 and the member-x values on the difference bits), and (ii) the eight output words A34..A37, E34..E37 of the two members are equal after step 37. Nothing is tested at rows 23..37.')
add('')
add('**Lemma 6.1.** If (ii) holds, the two second-block outputs are equal (chaining value plus the same eight words), so M0 || M1 and M0 || M1\' collide under the target; M1 != M1\' because W7 differs. The program certifies exactly what it outputs.')
add('')
add('*Why row 19.* Measured with the estimator (one row at a time checked on signed differences only, the others strict, outputs compared): relaxing row 19 raises q3 by about 3.6 bits for P8 (and 3.4 for the published characteristic); rows 17 and 18 lead to dead ends (the derived conditions there are needed by the next row), rows 20..22 add little. In the %s runs of the study of Section 9 (seeds %s), %s classified successes have their row-19 conditions in one of %s patterns (`pat19`; the 12 conditions: the fixed bits E19[4], E19[18] and ten two-bit conditions):' % (S_q['n'], seed_txt, pat_src, S_p['npat']))
add('')
add('```'); add(PAT19 or todo('pat19')); add('```')
add('')
add('## 7. The counted program (`experiments/a0p38.py`, %s bytes, SHA-256 %s)' % (c(vt_size), vt_hash))
add('')
add('### 7.1 Machine and scalar routines')
add('')
add('256-bit word RAM, 64 registers; executed primitives count 1 (load, store, add, sub, and, or, xor, not, shift, immediate, random word), a compare-and-branch 2, one target compression 1 unit; S0, S1, s0, s1 cost 8 each (doubled word, shifts, xors, mask), CH 3, MAJ 4. The routines are executed with counting primitives; broadcast, lane_value, first_lane, r16test and deep add itemised declared counts (their docstrings) (`calibrate`):')
add('')
add('| routine | operations |'); add('|---|---|')
add('| first block: 2 random words and their 16 fields (30), counter, cap test, hit-list test (5) | %d |' % CAL['fb_fixed'])
add('| one W7 test (computed, no table), plus %d for the class loop | %d + %d |' % (CAL['w7_loop'], CAL['w7'], CAL['w7_loop']))
add('| per-first-block scalars HH, PP, QQ, EF, FF, K1, KP | %d |' % CAL['scalars'])
add('| the 7 x 32 broadcast planes (%d each) | %d |' % (AP.PLANE_OPS, CAL['planes']))
add('| per passing class: setup 3, end of class (work counter, cap test) 4 | %d |' % CAL['class_ctl'])
add('| per batch of 256 variants: the class\'s row-16 program (%s to %s, mean %.2f) + ok test 2 + pointer, compare, branch 4 | prog_i + %d |' % (c(pmin), c(pmax), float(pmean), CAL['batch_ctl']))
add('| per stage-3a lane: lowest lane (32), clear and loop (%d), a0 from the stored planes (4 x %d + 1 = %d, the widest mask), E16x (%d), the row-16 table test (42) | %d |' % (AP.LANE_CTL, pop(widest), n_lv, n_e16, CAL['lane']))
add('| per row-16 pass (itemised declared count): Step 2 for both members, the expansion and rows 16..37 of both members with the tests of rows 16..22, the output comparison | %d |' % CAL['deep'])
add('')
add('### 7.2 The row-16 programs (one per class)')
add('')
add('Bit L of a 256-bit plane belongs to lane L (one variant). Inputs of the program of class i: the planes of the bits of a0 in mask_i (%d to %d bits, stored per batch) and the 224 broadcast planes; every bit of a0 outside mask_i is the corresponding bit of base_i and is folded as a constant (the per-class construction of 08be594; Section 0.1). `build_e16` builds, bit-interleaved, the DAG of E0 = a0 + HH, then per bit j: S0(a0), MAJ(a0, a, b) = PP | (a0 & QQ), S1(E0), CH(E0, e, f) = FF ^ (E0 & EF), the three ripple adders of their sum T and the subtraction W1 = K1 - T, then per tested position j <= %d: s0(W1), the two adders of E16x and the comparison with the common value; constants are folded and equal nodes shared. `schedule` allocates 64 registers by Belady\'s rule (evict the value needed farthest ahead; store it first if it is needed again and has no copy); every load, store and spill is an instruction. Result: %d programs (%d distinct input patterns), **%s to %s instructions per batch, mean %.2f** (calibration list in Section 10). The expected work uses the mean (each class passes its W7 test with the same p7), the work cap the maximum. The programs are executed instruction by instruction (`run_prog`) and compared with the scalar definition lane by lane (`selftest` item 4 and the organizer experiment `a0p-online-r38`: 0 mismatches).' % (wmin, wmax, max(AP.TBITS), ncl, ndistinct, c(pmin), c(pmax), float(pmean)))
add('')
add('## 8. The algorithm (fixed caps)')
add('')
add('```text')
add('advice: S (the semi-free-start pair\'s rows 0..15), the %d class descriptors (c7, base, mask); precompute (charged): every class member (base ^ s, s subset of mask, in G, c7 = c7_i), stored as %d batches of |mask| bit planes per class; the %d row-16 programs' % (ncl, nb, ncl))
add('V = 0')
add('for f = 1 .. N_FB:')
add('    if V > V_MAX: halt (failure)                    (V accumulates ALL data-dependent work of every first block: W7 tests, hit list, scalars, planes, classes, lanes, row-16 passes)')
add('    two uniform 256-bit random words -> M0 (16 words, uniform on {0,1}^512); CV1 := F_38(IV, M0)                     [1 unit]')
add('    hits := [i : c7_i - A_{-1} in F7]                                                                               [%d x (%d + %d)]' % (ncl, CAL['w7'], CAL['w7_loop']))
add('    if hits: the scalars and the broadcast planes')
add('        for i in hits: for each of the %d batches of class i: run the row-16 program of class i -> ok plane' % nb)
add('            for each lane of ok: a0 from the planes; E16x; if E16x in R16: Step 2, rows 16..37 of both members, the tests of rows 16..22')
add('                (row 19 on signed differences), compare the outputs; if equal: output M0 || M1, M0 || M1\' and halt')
add('        V += the work of the class (and, before it, the W7 tests, the hit list, the scalars and the planes of this first block); if V > V_MAX: halt (failure)')
add('halt (failure)')
add('```')
add('')
add('*Lemma 8.1 (the cap).* V accumulates every data-dependent operation of every first block (all of v_f in Section 9) and is tested before every first block and after every class, so V <= V_MAX + OVER at every moment (V is updated for every first block, including first blocks with no passing class: their data-dependent work is the W7 tests and the hit-list test, added to V before the next cap test), OVER = %s (one first block at its maximum: all classes passing, each charged at the longest program, every lane a row-16 pass). The %d fixed operations per first block are charged separately (N_FB x %d). The run never outputs a non-collision (Lemma 6.1).' % (c(L['over']), CAL['fb_fixed'], CAL['fb_fixed']))
add('')
add('## 9. The success probability')
add('')
add('*Trials and expectation.* A trial is (first block f, selected variant a0); A_t: a0 is good for f (W7 in F7) and the pair is in the accepted event. E[X_f] = g q3 (Lemma 5.1; H1, H2).')
add('')
add('*q3 (H2).* q3 = the average over the %s selected variants of Pr[accepted event | good pair] (including the row-16 factor %d / 2^32). Estimator `q3tv.c` (binary q3tv2, `DIFFROW=19 RELAX_TAIL=1`, `VARS` = the variant pool of the %d classes): fixed-effort multilevel splitting, row 16 exact over the %d W16 words, rows 17..22 with W_i^x uniform (Lemma 5.1) and the rows checked as in the event (row 19 on signed differences), tail: a variant drawn per proposal from the %s selected variants, W7 uniform in F7, rows 23..37 computed, outputs compared. Every success is a verified collision; the successes are rebuilt into real pairs (%s checked with the reference). %d runs, %s particles, %s tail proposals per particle, seeds %s fixed before the runs:' % (c(nvar), len(AP.R16), ncl, len(AP.R16), c(nvar), REB, A.nruns, c(A.particles), c(A.tail), seed_txt))
add('')
add('| seed | stage factors log2 (rows 16..22, tail) | successes (all collisions) | log2 q3 |'); add('|---|---|---|---|')
RUND = {r[0]: r for r in RUNS}
for sd in seeds:
    if sd in RUND: _, stg_, sc_, cc, lq = RUND[sd]; add('| %d | %s | %s | %s |' % (sd, stg_, c(sc_), '%.4f' % lq if lq is not None else '0 (stalled)'))
    else: add('| %d | %s | | |' % (sd, todo('run not finished')))
add('')
add('Mean 2^%s, relative sd %s, one-sided 99%% Student bound (t = %s, %s degrees of freedom) 2^%s, bootstrap 1%% quantile of the mean 2^%s; %s successes. %s. %s **q3_model = 2^%.4f.**' % (S_q['mean'], S_q['rsd'], S_q['t'], S_q['df'], S_q['lo'], S_q['bs'], S_q['succ'], spread, stall_txt, Q3M) + (' q3_model = 2^%.1f was set from the first 20 runs (seeds %d..%d: their 99%% bound 2^-96.9989, rounded down to a tenth) and kept when 20 further runs were added after a first review found its margin thin (seeds %d..%d, fixed before those runs; all runs are reported); over all %d runs the 99%% bound is %.4f bits above q3_model. Rounding the %d-run bound down would give 2^%.1f; we keep 2^%.1f for the margin. At the %d-run bound 2^%s the ledger gives %.5f.' % (Q3M, seeds[0], seeds[0] + 19, seeds[0] + 20, seeds[-1], A.nruns, float(S_q['lo']) - Q3M, A.nruns, math.floor(float(S_q['lo']) * 10) / 10, Q3M, A.nruns, S_q['lo'], ledger(q3=float(S_q['lo']), h3=H3B, cal=CAL)['claim']) if 'TODO' not in S_q['lo'] else ''))
add('')
add('*The pair term (H3).* Every success passes row 16, so given A_t, X_f - 1 <= R_f - 1 (the other row-16 passes of f). Measured (`h3p.py`): %s successes rebuilt and verified (all accepted by the program\'s event, so the estimator\'s event and the program\'s agree on every one; 99%% bound on a disagreement rate %s), all %s re-found in their own class; every selected variant of every passing class evaluated on the success\'s CV1: %s passing classes, %s variants, **%s other row-16 passes, %s further accepted pairs** (%s expected under independence). One-sided 99%% Poisson limit of E[R_f - 1 | A_t]: %s = 2^%s; charged 2^%s (the limit rounded up to a tenth plus 0.5, the rule of 1a695f0b). Sampling: every 25th success line of the study\'s dump files in sorted file order, the first %s of them (`h3p.py`, `POOL` and `STUDY` set to this study\'s pool and dumps), so they come from the first runs and successes within a run are not independent; the Poisson limit assumes independence, which the 0.5 margin only partly covers (pair term 2^-3 moves the claim by +0.07, Section 10). %s' % (S_h['succ'], S_h['dis'], S_h['own'], S_h['pc'], S_h['var'], S_h['r16'], S_h['acc'], S_h['exp'], S_h['lim'], S_h['llim'], S_h['H3B'], S_h['succ'], S_h.get('spread', '')) + (' Given a success, its CV1 passes the W7 test for %.2f classes on average (1 + %d p7 = %.2f if the classes were independent): the c7 values of the classes are related, so their W7 tests pass together. The expectations of the ledger are linear and unaffected; the effect is inside the measured pair term and the work cap.' % (H3['passing_classes'] / H3['verified'], ncl - 1, 1 + (ncl - 1) * 287309824 / 2 ** 32) if H3['verified'] else ''))
add('')
add('*Bonferroni, independence, caps.* Pr[X_f >= 1] >= E[X_f] - E[X_f (X_f - 1)] / 2 >= g q3 (1 - 2^h3 / 2); first blocks are independent (fresh coins); the data-dependent work v_f of a first block satisfies 0 <= v_f <= vmax_f = %s with mean at most vbar = %.4f (exact rational in the ledger), so Var(sum v_f) <= N_FB vmax_f vbar and Chebyshev bounds Pr[sum v_f > (1 + 2^-16) N_FB vbar] by P_cap = %.3e; V_MAX = ceil((1 + 2^-16) N_FB vbar). On the complement no cap halts the run. N_FB is the least integer with 1 - exp(-N_FB g q3_model (1 - 2^h3 / 2)) - P_cap - 2^-60 >= 0.39 (2^-60 covers the rounding of the exponential, evaluated at 80 decimal digits).' % (c(L['vmax']), L['vbar'], L['Pcap']))
add('')
add('## 10. Ledger (exact; `ledger_a0p.py`, Appendix C)')
add('')
add('```text')
add('T = A_C + A_S + DEV + N_FB + (N_FB x %d + V_MAX + OVER + PRE + FIN) / C + 6' % CAL['fb_fixed'])
add('  A_C = 2^78, A_S = 2^74, DEV = 2^70 (Section 12, H4; the levels of fb176310)')
add('  N_FB = %s = 2^%.5f   (g = %s good pairs per first block, g q3_model = 2^%.4f)' % (c(L['NFB']), L['log2NFB'], cg(L['g']), L['log2gq']))
add('  vbar = %.4f operations per first block: W7 tests %d x (%d + %d), hit list, scalars and planes (%d) x min(1, %d p7),' % (L['vbar'], ncl, CAL['w7'], CAL['w7_loop'], CAL['scalars'] + CAL['planes'], ncl))
add('         passing classes %d p7 x (%d + %d x (%s + %d)) (the mean program, %s = %.2f), stage-3a lanes %d p7 x %s x 2^-%d x %d, row-16 passes %d p7 x %s x %d / 2^32 x %d' % (ncl, CAL['class_ctl'], nb, pmean, CAL['batch_ctl'], pmean, float(pmean), ncl, c(csize), CAL['tk'], CAL['lane'], ncl, c(csize), len(AP.R16), CAL['deep']))
add('  vmax_f = OVER: every class at the longest program (%s), every lane a row-16 pass' % c(pmax))
add('  V_MAX = %s, OVER = %s, PRE = %s (member tests over the %d class cubes, the batch planes, program generation)%s' % (c(L['VMAX']), c(L['over']), c(L['PRE']), ncl, (' ' + pre_note) if pre_note else ''))
add('  FIN = 1,600 operations and 6 units (the final verification)')
add('N = T x 2728 = %s  ->  T = 2^%.8f  ->  time_log2 = %.5f' % (c(L['N']), L['log2T'], claim))
add('```')
add('')
add('Calibration (`calibrate.json`, the output of `calibrate()` of `experiments/a0p38.py`; `selftest` prints the same):')
add('')
add('```'); add(json.dumps(CAL)); add('```')
add('')
add('*Certificate.* `python3 ledger_a0p.py --q3 %s --h3 %s --cal calibrate.json` prints the ledger and checks `(2728^E << %d) < N^E <= (2728^E << %d)` with E = 100000 (exact integers), so %.5f is the smallest five-decimal upper bound on log2 T. *Sensitivity* (each row recomputed by the ledger with this calibration unless marked reference):' % (Q3M, H3B, round(claim * 1e5) - 1, round(claim * 1e5), claim))
add('')
add('```'); [add(x) for x in sens]; add('```')
add('')
add('## 11. Memory and advice')
add('')
add('```'); add(MEM or todo('memory record')); add('```')
add('')
add('*Sampling.* The peaks are maxima of the summed resident memory sampled every 0.2 s, so a shorter allocation spike could be missed; the claim 2^28.10 bytes = 288,630 KiB is 3.2%% above the largest sample (279,720 KiB), and the Step-1 solve is a single Kissat process whose resident memory grows with its clause database (it does not spike).')
add('')
add('*Scope of the memory bound.* Peak memory covers code, advice, retained data, tables and working state of the whole computation: the online algorithm, the charged precomputation (class members, planes, the %d programs) and the computations behind the advice and the allowances (the characteristic search, the Step-1 solve, the class descriptors and their selection, the condition tables), each run single-threaded and sequentially. P8 and S are those of %s (produced by `stepk.py` and `joint.py`); the claimed figure is the largest measured peak in the record above. The class descriptors are found in 32 passes over a hash of c7 (`a0cls.c`, at most 2^23 pairs resident) and selected by `lp_classes.py`. The online figure also covers the deep path\'s working state (two traces, about 6 KB) and M0, CV1.' % (ncl, REF['id']))
add('')
add('Claimed memory 2^%.2f bytes: the maximum of the online footprint and the measured preprocessing peaks. Advice: S (16 words of each member and CV1), the %d class descriptors (c7, base, mask: %s bytes), the constants of the characteristic: below 2^14 bytes; everything else (class members, planes, the programs) is computed by the charged preprocessing.' % (memclaim, ncl, c(12 * ncl)))
add('')
add('## 12. Premises')
add('')
add('- **H1** single-trial chaining value: CV1 = F_38(IV, M0) for uniform M0 behaves as uniform for the events of one variant (Lemma 5.1).')
add('- **H2** q3 >= q3_model for the accepted event, averaged over the selected variants (Section 9; %s runs).' % S_q['n'])
add('- **H3** the pair term within a first block is at most 2^h3 (Section 9; measured).')
add('- **H4** allowances: ' + 'The allowances are envelopes, not measurements: A_C = 2^78, A_S = 2^74, DEV = 2^70 target compressions (the levels charged by fb176310). All of our computation for this line of work (the characteristic search and sweep, the Step-1 solve, the class data, the q3 studies and all development) ran on one 10-core machine, for less than 2^%s core-seconds by our own accounting. The bound does not depend on that accounting or on a rate: ten cores running continuously for a full year are 2^28.3 core-seconds, and even at 2^30 target compressions per core-second (above any CPU core; SHA-256 runs at about 2^24 compressions per second per core) that is 2^58.3, below DEV = 2^70 alone. With A_C = 2^84 the ledger gives time_log2 = %.5f (+%.5f; Section 10); with the smaller allowances of %s, %.5f.' % (CORE_S, ac84, ac84 - claim, REF['id'], ledger(**dict(base, AC=48, AS=50, DEV=50))['claim']))
add('- **H5** unit-cost bit-sliced planes: the row-16 programs are charged as their instruction counts on 256-bit planes, as in the cost model.')
add('')
add('## 13. Organizer experiments (`experiments/manifest.json`)')
add('')
add('**a0p-online-r38** (H1, H5, Lemma 4.1). Trials 0..%d: first blocks drawn from the organizer seed (two uniform words each, real 38-step compressions) until one has a passing class (at most 64); its first passing class is run on two batches (the class\'s first 512 members) with that class\'s program: the ok plane is compared lane by lane with E16x from the Step-2 words and the 38-step trace, and W7 with c7 - A_{-1} and F7; trial 0 also runs the batch of the semi-free-start pair\'s variant and requires the counted program to find and accept it. A pair M0 || M1, M0 || M1\' (one variant, not a collision) is returned iff there is no mismatch. Trials %d..255 return no pair by design.' % (AP.ONLINE_TRIALS - 1, AP.ONLINE_TRIALS) + (' Before any selection, each active trial draws %d first blocks from the organizer seed and counts the W7 passes of all %d classes (observations uncond_first_blocks, uncond_class_passes; expectation %d x %d x |F7| / 2^32 = %.1f per trial under H1). Validation by us: %s unconditional first blocks over %d requests, %s class W7 passes against %s expected (ratio %s); passes come in groups of related classes (a success\'s CV1 passes %.1f classes on average), so the per-trial count has a large variance.' % (AP.UNCOND_FB, ncl, AP.UNCOND_FB, ncl, AP.UNCOND_FB * ncl * 287309824 / 2 ** 32, UNC['fb'], UNC['req'], UNC['passes'], UNC['exp'], UNC['ratio'], H3['passing_classes'] / H3['verified']) if UNC else ''))
ch_r = ', '.join(map(str, AP.CH_R))
add('')
add('**a0p-q3-r38** (consistency check of H2). Trials 0..%d: %d replicates of the estimator of q3 for the accepted event (%d particles; %s children at rows 17..22 with the row\'s E bits imposed, at row 19 one of the four patterns drawn uniformly, weight 4 x 2^-f; tail: %d proposals per particle, a variant of %d embedded samples of the selected classes (%d of the %d classes represented), W7 uniform in F7 (its three affine families; the family drawn by rejection from its own word, the value bits from a fresh word), rows 23..37, outputs compared; every success rebuilt into CV1, M1, M1\' and accepted only if it is a 38-step collision in the accepted event with W7 in F7). Trial t < %d returns its first verified pair as CV1 || M1 and CV1 || M1\' (semi-free-start collisions, never collisions from the IV); trial %d returns a pair iff no rebuild failed and the mean of the %d estimates is at least 2^%.4f (pass rule fixed from %s development requests before any validation run; their pooled means: minimum %s, 5%% quantile %s, median %s; replicate mean 2^%s).' % (
    AP.Q3_REPS - 1, AP.Q3_REPS, AP.NP_R, ch_r, AP.NT_R, len(VS), len(vs_cls), ncl, AP.Q3_REPS, AP.Q3_REPS, AP.Q3_REPS, THR, S_d['n'], S_d['min'], S_d['q5'], S_d['med'], S_d['rmean']))
add((' What a pass shows: the replica estimates the same event as the study, restricted to the four row-19 patterns (a lower bound) and to %d of the selected variants; its 48 development requests (480 replicates) have mean 2^%s against the study mean 2^%s. Shifting their pooled means down by 1, 2 or 3 bits (a q3 that much lower) makes %.0f%%, %.0f%% and %.0f%% of requests fail the rule (none at the claimed level): a pass excludes a gross error in the estimator or the program, it does not certify the bound.' % (len(VS), S_d['rmean'], S_q['mean'], 100 * POW[1], 100 * POW[2], 100 * POW[3]) if POW else ''))
add('')
add('*Validation by us* (the shipped file; 256 trials; network-less container, 1 CPU, 128 MiB; python:3.12.12-slim-bookworm):')
add('')
add('```'); add(VAL or todo('validation')); add('```')
add('')
add('## 14. Limitations')
add('')
add('- q3 is a Monte Carlo estimate (participant-run, resampled particles; the Student bound assumes independent runs); the organizer replica checks a reduced version of it. The row-19 pattern support of the replica is the four patterns of Section 9, which cover all %s classified successes of this study (as they did in the study of %s), so the replica estimates a lower bound of the event\'s probability.' % (S_p['tot'], REF['id']))
add('- The pair term and the success distribution are measured on rebuilt estimator successes (H1 premise for real chaining values).')
add('- The bit-sliced programs are executed on sampled batches; full-scale execution is infeasible.')
add('')
add('## Appendix A. Self-test and calibration of `experiments/a0p38.py`')
add('')
add('```'); add(SELF or todo('selftest')); add('```')
add('')
add('## Appendix B. The conditions of rows 16..22 (the accepted event; member x, `experiments/a0p38.py` tables)')
add('')
add('Per row: for A, E, W the mask of fixed x-values (trail difference bits and one-bit conditions), their x-values and the XOR difference; the \'+\' pairs E_i[b] = E_{i-1}[b]; the two-bit conditions (kind 0 A / 1 E / 2 W, row, bit; = or !=). Row 19 is checked on its XOR differences and the x-values of its difference bits only.')
add('')
add('```')
KN = 'AEW'
for i in range(16, 23):
    for k in range(3):
        m_, v_, d_, _ = AP.CELLS[k][i]
        if m_ or d_: add('row %d %s: mask %08x x-value %08x xor %08x' % (i, KN[k], m_, v_ & m_, d_))
    if AP.PQ[i]: add('row %d +: E%d[b] = E%d[b] for the bits of %08x' % (i, i, i - 1, AP.PQ[i]))
    for (k1, i1, b1, eq, k2, i2, b2, row) in AP.X2:
        if row == i: add('row %d: %s%d[%d] %s %s%d[%d]' % (i, KN[k1], i1, b1, '=' if eq else '!=', KN[k2], i2, b2))
add('```')
add('')
add('## Appendix C. Programs (SHA-256 and full listings; `experiments/a0p38.py` is assembled by `mka0p.py` from the `a0p_*.py` parts)')
add('')
add('- `experiments/a0p38.py`: %s' % vt_hash)
for f in SRC: add('- `%s`: %s' % (f, hs.get(f, todo('missing source'))))
add('')
for f in SRC:
    add('### %s' % f); add(''); add('```' + ('c' if f.endswith('.c') else 'python')); add(src.get(f, todo('missing source')).rstrip('\n')); add('```'); add('')

os.makedirs(OUT + '/experiments', exist_ok=True)
stray = [f for f in os.listdir(OUT + '/experiments') if f.endswith('.py') and f != 'a0p38.py']
if stray: sys.exit('mkpkg4: %s/experiments has other programs (%s); remove them first (nothing written)' % (OUT, ', '.join(stray)))
open(OUT + '/proof.md', 'w').write('\n'.join(P) + '\n')

def rng(start, end=None):
    a = next(i for i, l in enumerate(P) if l.startswith(start)) + 1
    b = next(i for i, l in enumerate(P) if i >= a and l.startswith(end)) if end else len(P)
    return 'proof:%d-%d' % (a, b)
r0, r4, r5, r6, r7, r9, r10, r11, r13 = (rng('### 0.1', '## 1.'), rng('## 4.', '## 5.'), rng('## 5.', '## 6.'), rng('## 6.', '## 7.'), rng('## 7.', '## 8.'), rng('## 9.', '## 10.'),
                                         rng('## 10.', '## 11.'), rng('## 11.', '## 12.'), rng('## 13.', '## 14.'))
H = []
def h(i, stmt, scope, ext, lim, ev): H.append(dict(id=i, role='score-critical', statement=stmt, scope=scope, extrapolation=ext, limitations=lim, evidence_ids=ev))
nstall = len(STALLED)
h('H1-single-trial-chaining-value', 'For M0 uniform on {0,1}^512 (two fresh random words per first block), CV1 = F_38(IV, M0) behaves as a uniform 256-bit value for the events of one fixed variant (W7, W16..W22 and E16x distributed as in Lemma 5.1).', 'g, the per-first-block success probability and the expected work.', ('The premise of the A0-variant lineage. Organizer evidence: a0p-online-r38 draws %d unconditional first blocks per active trial and counts the W7 passes of all %d classes (our validation: %s passes in %s blocks against %s expected); it then runs the counted program on real first blocks.' % (AP.UNCOND_FB, ncl, UNC['passes'], UNC['fb'], UNC['exp']) if UNC else 'The premise of the A0-variant lineage; the organizer experiment a0p-online-r38 runs the program on real first blocks.'), 'A premise about the first-block compression.', [r5, r13])
h('H2-q3-accepted-event', 'The average over the %s selected variants (%d classes) of Pr[the pair is in the accepted event (rows 16..22 with row 19 on signed differences, equal outputs) | good pair] is at least q3_model = 2^%.4f.' % (c(nvar), ncl, Q3M), 'N_FB and the whole attack term.',
  '%s multilevel-splitting runs (seeds %s) with the variants of the selected classes: mean 2^%s, one-sided 99%% Student bound 2^%s, bootstrap 2^%s, %s verified collisions (%s); an independent Python implementation (the organizer replica, a lower-bound event restricted to four row-19 patterns and %d sampled variants): %s development replicates, mean 2^%s; organizer replica a0p-q3-r38 with a frozen pass rule.' % (
      S_q['n'], seed_txt, S_q['mean'], S_q['lo'], S_q['bs'], S_q['succ'], ('%s stalled run%s counted as 0' % (wd(nstall), 's' if nstall > 1 else '')) if nstall else 'no stalled run', len(VS), S_d['nrep'], S_d['rmean']),
  'Participant-run Monte Carlo with a heavy-tailed middle stage; the replica tests a reduced version.', [r9, r13])
h('H3-pairs-in-first-block', 'The average over successes of the expected number of other row-16 passes of the same first block is at most 2^%s.' % S_h['H3B'], 'The Bonferroni factor of a first block.', '%s rebuilt successes: %s other row-16 passes among %s evaluated variants of the passing classes; 99%% Poisson limit 2^%s.' % (S_h['ver'], S_h['r16'], S_h['var'], S_h['llim']), 'Measured on rebuilt estimator successes.', [r9])
h('H4-allowances', 'The computation spent on the characteristic search, S and the class data, and all development is at most A_C + A_S + DEV = 2^78 + 2^74 + 2^70 target compressions.', 'The allowance term (negligible against T).', 'One 10-core machine, less than 2^%s core-seconds in all (participant accounting); the envelope holds for any machine running ten cores for a full year at up to 2^30 target compressions per core-second (2^58.3 < 2^70).' % CORE_S, 'Envelope independent of the measured rate; with A_C = 2^84 the ledger gives time_log2 = %.5f (+%.5f).' % (ac84, ac84 - claim), [r10])
h('H5-bitsliced-planes', 'One instruction on a 256-bit plane costs one word operation (the 256-bit word RAM of the cost model); each class\'s row-16 program is charged at its executed instruction count, loads and stores included (expected work at the mean over the classes, the work cap at the maximum).', 'The dominant work term.', 'Executed instruction by instruction and compared with the scalar definition on sampled batches (selftest, a0p-online-r38).', 'Full-scale execution is infeasible.', [r7, r13])
CL = dict(schema_version=3, submission_state='ready', target_profile='sha256-r38-prefix-v1', attack_class='ordinary-collision', rounds=38, lane='exploratory',
          baseline_improved='sha256-r38-nominal-v2', certificate_manifest='certificates/manifest.json', experiment_manifest='experiments/manifest.json',
          claim=dict(time_log2=claim, time_unit='target-compressions', memory_log2_bytes=memclaim, preprocessing_log2=math.ceil(L['pre_log2'] * 1e5) / 1e5, success_probability=0.39, nonuniform_advice_log2_bytes=14),
          restrictions=['Target sha256-r38-prefix-v1 exactly: SHA-256 steps 0..37 on every padded block, the standard IV once, FIPS 180-4 padding, feed-forward, all eight digest words; outputs two distinct 128-byte messages M0 || M1, M0 || M1\' with equal digests.',
                        'Construction: the memory-efficient A0-variant attack (design of 2d1c4fc2 and fb176310 on ePrint 2026/1120 / 2026/1080; per-class row-16 programs as in 08be594), our implementation experiments/a0p38.py, with our characteristic P8 and the accepted event rows 16..22 (row 19 on signed differences) plus a direct output comparison.',
                        'Cost: exact ledger ledger_a0p.py: N_FB = %s first blocks, %d classes of %s variants (%s in all), per-class row-16 programs of %s to %s instructions (mean %.2f) per 256 variants, executed counts; T x 2728 = %d; claimed %.5f.' % (c(L['NFB']), ncl, c(csize), c(nvar), c(pmin), c(pmax), float(pmean), L['N'], claim),
                        'Success probability at least 0.39 under H1, H2 (q3_model 2^%.4f), H3, by Bonferroni per first block, independent first blocks and Chebyshev caps.' % Q3M,
                        'Memory 2^%.2f bytes (online %s bytes; the preprocessing peak).' % (memclaim, S_m['online'])],
          heuristics=H)
if MISSING or PROVISIONAL: CL['submission_state'] = 'draft'; CL['dry_run_todo'] = MISSING + ['provisional: ' + x for x in PROVISIONAL]
for x in H:
    for k, v in x.items():
        if isinstance(v, str): assert len(v) <= 4096
json.dump(CL, open(OUT + '/claim.json', 'w'), indent=2); open(OUT + '/claim.json', 'a').write('\n')
shutil.copyfile(VT, OUT + '/experiments/a0p38.py')
MAN = dict(schema_version=1, experiments=[
    dict(id='a0p-online-r38', kind='python-message-pairs-v1', program='experiments/a0p38.py', event=dict(kind='full-collision'),
         scope='H1 (unconditional first blocks), H5 and the Lemma 4.1 identities on real first blocks (proof.md Sections 4, 7, 13). Trials 0..%d: first %d unconditional organizer-seeded first blocks per trial, the W7 passes of all %d classes counted without selection (expectation %.1f per trial under H1); then first blocks drawn from the organizer seed (two uniform 256-bit words from SHAKE-256 of the experiment id and seed per first block; real 38-step compressions) until one has a passing class (at most 64); its first passing class is run on two batches (its first 512 members): the counted row-16 program of that class is executed instruction by instruction and its ok plane compared lane by lane with E16x computed from the Step-2 words and the 38-step trace; W7 is compared with c7 - A_{-1} and checked in F7. Trial 0 also runs the batch of the semi-free-start pair\'s variant on its chaining value: the counted program must find and accept it (positive lanes). Returns M0 || M1 and M0 || M1\' of the class\'s first member (128 bytes each; one variant of one chaining value, not a collision) iff there is no mismatch. Trials %d..255 return no pair by design.' % (AP.ONLINE_TRIALS - 1, AP.UNCOND_FB, ncl, AP.UNCOND_FB * ncl * 287309824 / 2 ** 32, AP.ONLINE_TRIALS),
         hypothesis='Returned pairs: %d (every executed trial mismatch-free); full collisions of the target: 0 (a returned pair is not a collision). Observations (untrusted): uncond_first_blocks (%d), uncond_class_passes (H1: mean %.1f per trial; grouped passes give a large variance), first_blocks, passing_classes, lanes (512), stage3a_passes, mismatches (0). Validation by us: %s pairs returned per request, %s mismatches, at most %s s; unconditional: %s class W7 passes in %s first blocks against %s expected.' % (AP.ONLINE_TRIALS, AP.UNCOND_FB, AP.UNCOND_FB * ncl * 287309824 / 2 ** 32, S_v['on_ret'], S_v['on_mis'], S_v['on_t'], UNC['passes'] if UNC else '-', UNC['fb'] if UNC else '-', UNC['exp'] if UNC else '-')),
    dict(id='a0p-q3-r38', kind='python-message-pairs-v1', program='experiments/a0p38.py', event=dict(kind='full-collision'),
         scope='Consistency check of the q3 estimator (H2; proof.md Sections 6, 9, 13): it is not an estimate of q3 and not evidence for the bound q3_model, which rests on the participant study. Trials 0..%d: %d independent replicates of the estimator of q3 for the accepted event (row 16 exact over the %d W16 words; rows 17..22 by proposals with the row\'s E bits imposed, at row 19 one of the four observed condition patterns drawn uniformly with weight 4 x 2^-f and the row checked on signed differences; tail: a variant of %d embedded samples of the selected classes, W7 uniform in F7 (its three affine families; the family drawn by rejection from its own word, the value bits from a fresh word), rows 23..37, outputs compared; randomness SHAKE-256 of the experiment id and trial seed). Every success is rebuilt into (CV1, M1, M1\') and accepted only if the two 38-step compressions from CV1 are equal, M1 != M1\', the pair is in the accepted event and W7 is in F7. Trial t < %d returns its first verified pair as CV1 || M1 and CV1 || M1\' (96 bytes each; semi-free-start collisions, never collisions from the IV); trial %d returns a pair iff no rebuild failed and the mean of the %d estimates is at least 2^%.4f; trials %d..255 return no pair by design.' % (
             AP.Q3_REPS - 1, AP.Q3_REPS, len(AP.R16), len(VS), AP.Q3_REPS, AP.Q3_REPS, AP.Q3_REPS, THR, AP.Q3_REPS + 1),
         hypothesis='Returned pairs: one semi-free-start pair per replicate with a tail success (development requests: %s of %d replicates; validation by us: %s) and 1 from trial %d (a pass; trial %d needs trials 0..%d in the same request); full collisions of the target: 0. The pass rule was fixed from %s development requests (pooled means: min %s, median %s) before any validation run; a pass checks a reduced replica, it is not an estimate of q3. Observations (untrusted): log2_estimate (-1000 for no success), accepted_pairs, failed_rebuilds (0); trial %d log2_pooled_mean.' % (
             S_d['rs'], AP.Q3_REPS, S_v['q_rs'], AP.Q3_REPS, AP.Q3_REPS, AP.Q3_REPS - 1, S_d['n'], S_d['min'], S_d['med'], AP.Q3_REPS) + (' What a pass shows: the replica estimates the same event as the study, restricted to the four row-19 patterns (a lower bound) and to %d of the selected variants; its 48 development requests (480 replicates) have mean 2^%s against the study mean 2^%s. Shifting their pooled means down by 1, 2 or 3 bits (a q3 that much lower) makes %.0f%%, %.0f%% and %.0f%% of requests fail the rule (none at the claimed level): a pass excludes a gross error in the estimator or the program, it does not certify the bound.' % (len(VS), S_d['rmean'], S_q['mean'], 100 * POW[1], 100 * POW[2], 100 * POW[3]) if POW else ''))])
json.dump(MAN, open(OUT + '/experiments/manifest.json', 'w'), indent=2); open(OUT + '/experiments/manifest.json', 'a').write('\n')
RAT = {
    '2d1c4fc2': ('A0-variants of one Step-1 solution, c7 classes decided by one W7 test, the bit-sliced row-16 filter for 256 variants per word, the success analysis with a pair term and work caps; implemented anew in experiments/a0p38.py.', 'proof.md Section 2; Sections 4 to 9.'),
    'fb176310': ('The accepted event with a direct output comparison and alternative row-19 patterns, lowest-shared-bit stage 3a, the memory-free W7 test and a counted register allocator; implemented anew.', 'proof.md Sections 2, 6 and 7.'),
    '242fcec3': ('Our earlier filing (table attack with NEW3): the estimator, condition derivation and ledger methodology reused here.', 'proof.md Section 2.'),
    '49b543d1': ('Our earlier filing that introduced the characteristic search (signed-difference SAT model) that later found P8.', 'proof.md Sections 2 and 3.2.'),
    '1a695f0b': ('Our previous filing of this attack with P8 and %d classes; this package extends it to %d classes with per-class programs, an unbiased F7 sampler in the replica and a deterministic class selection.' % (len(RCLS), ncl), 'proof.md Sections 0 and 0.1.'),
    '08be594': ('Per-class row-16 programs with the class\'s non-mask bits folded as constants (the idea used here for all %d classes, our implementation), and the observation that the F7 sampler of 1a695f0b\'s replica correlated the family choice with the value and had a modulo bias (fixed here).' % ncl, 'proof.md Sections 0.1, 2, 7.2 and 13.')}
DEPS = [dict(submissionId=(DEPS_UUID[k] if k != '08be594' else (DEP08 or 'TODO-08be594-full-submission-id')), rationale=RAT[k][0], evidence=RAT[k][1])
        for k in ('2d1c4fc2', 'fb176310', '242fcec3', '49b543d1', '1a695f0b', '08be594')]
json.dump(DEPS, open(OUT + '/dependencies.json', 'w'), indent=2); open(OUT + '/dependencies.json', 'a').write('\n')
if MISSING or PROVISIONAL:
    print('DRY RUN (--allow-missing): %d missing/inconsistent, %d provisional' % (len(MISSING), len(PROVISIONAL)), file=sys.stderr)
    for x in MISSING: print('  - ' + x, file=sys.stderr)
    for x in PROVISIONAL: print('  - provisional: ' + x, file=sys.stderr)
print('proof lines', len(P), 'bytes', len('\n'.join(P).encode()), 'claim', claim, 'memory', memclaim, 'score', round(score, 5))
```

