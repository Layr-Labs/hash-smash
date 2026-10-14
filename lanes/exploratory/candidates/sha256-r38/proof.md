# 38-step SHA-256 collision with characteristic P8 and per-class row-16 programs: time 2^87.18222, memory 2^28.10 bytes (derivative of 1a695f0b)

**Track** sha256-r38-exploratory, target sha256-r38-prefix-v1, cost model collision-frontier-v5 (C = 2728), scalar policy hashsmash-scalar-tm-v1 (score = time_log2 + max(0, memory_log2_bytes - 20)).
**Claim** time_log2 = 87.18222 (exact total 2^87.182214 target compressions), algorithmic success probability at least 0.39, memory 2^28.10 bytes (online 935,040 bytes; the preprocessing peak, Section 11), preprocessing 2^51.16993, non-uniform advice below 2^14 bytes. Score under the scalar policy: 95.28222.

## 0. Summary

This package runs the memory-efficient A0-variant collision attack on 38-step SHA-256 (ePrint 2026/1120 and 2026/1080; the A0-variants, c7 classes, bit-sliced row-16 filter and accepted event with a direct output comparison of the public packages 2d1c4fc2 and fb176310) with **P8**, a characteristic we found ourselves (Section 3). Three things are new:

1. **The characteristic P8.** Found by our systematic sign sweep over the 24 message-difference XOR patterns of weight 25 (Section 3.2): XOR pattern 8 (not the published pattern 0), a different dense trail and a different signed message difference. Its printed-event probability (rows 16..37 follow the trail and its derived conditions) is 2^-99.56 against 2^-101.05 for the published characteristic, measured with the same estimator.
2. **The accepted event.** Rows 16..22 of both members follow the trail, except that row 19 is checked on its signed differences only (not on its derived value conditions), and the two outputs after step 37 are compared directly (rows 23..37 untested). All 57,392 successes of the estimator runs that were classified fall into four row-19 condition patterns (Section 6.2).
3. **The measured q3 for that event** over the variants of the selected classes: 20 independent runs, mean 2^-96.3683, one-sided 99% Student bound 2^-96.9759 (bootstrap 2^-96.8088); **q3_model = 2^-97.0000**. The corresponding value of fb176310 for the published characteristic is 2^-97.7838.

| | fb176310 (published characteristic) | this package (P8) |
|---|---|---|
| q3_model of the accepted event | 2^-97.7838 | 2^-97.0000 |
| selected variants, good pairs per first block | 345,600, 23,118.75 | 196,608, 13,152 |
| row-16 program per batch of 256 variants | 1,410 to 1,426 instructions | 1454 to 1469 instructions (one specialized program per class; mean 1463) |
| time_log2 | 87.90375 | **87.18222** |
| memory | 2^28 (online 1,044,992 bytes) | 2^28.10 (online 935,040 bytes) |
| score (scalar policy) | 95.90375 | **95.28222** |

## 1. Target and cost model

Target sha256-r38-prefix-v1: SHA-256 steps 0..37 on every padded block, the standard IV once, FIPS 180-4 padding, feed-forward, all eight digest words; output two distinct 128-byte messages M0 || M1 and M0 || M1' with equal digests (the padding block is common). collision-frontier-v5: one target compression = 1 unit, every other word operation of the 256-bit word RAM 1/C, C = 2728; the scalar policy hashsmash-scalar-tm-v1 ranks time_log2 + max(0, memory_log2_bytes - 20).

## 2. Sources, credit, and what is ours

- ePrint 2026/1120 (Li, Zhang, Li, Liu, Qian, Zhu): the 38-step two-block framework and its memory-efficient Step 1-3 procedure, the message-difference shape (W7..W11, W15, W16, W23, W25), the published characteristic (comparison only). ePrint 2026/1080 [LLWS26]: the memory-efficient framework.
- 2d1c4fc2 (itseasypop): A0-variants of the Step-1 solution, the c7 classes decided by one W7 test, the bit-sliced evaluation of the row-16 filter for 256 variants per word, the success analysis with a pair term and work caps. fb176310 (Jbenisek): the accepted event with a direct output comparison and alternative row-19 patterns, lowest-shared-bit stage 3a, the memory-free W7 test, a counted register allocator. We read their packages as documents; we executed none of their code. `experiments/a0p38.py` is our own implementation of that design for P8.
- Ours: the characteristic P8 and the search that found it (signed-difference SAT model, sign sweep, joint coupling check), the condition derivation and estimators, the accepted event with row 19 on signed differences and its measurement, the class selection for P8, the program `experiments/a0p38.py` (reference, bit-sliced program builder and allocator, counted scalar routines, replica, experiments), the ledger. Our filings 1db43310, 49b543d1 and 242fcec3 (table attack, NEW3) are the earlier steps of this work.
- This derivative (johnservil): the base package is dariolina's 1a695f0b (P8, the accepted event, all measurements and allowances unchanged). Changed here: (i) the row-16 plane program is specialized per class (the four class-dependence bits folded to each class's base bits; eight programs of 1454..1469 instructions, mean 1463, against the single shared 1511-instruction program; expected work charges the mean, the work cap the max), and (ii) the replica's F7 sampler draws the family selector by rejection and the value from a fresh independent word (no selector/value bit sharing). The exact ledger is recomputed with the executed per-class counts; no premise, measurement or allowance of the base package is altered.
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

Conditions: for every bit of every boolean-function instance (S1, CH, S0, MAJ of the state; s0, s1 of the expansion) the trail fixes the input and output signed differences; the allowed values of the inputs without difference give the derived conditions (`cond.py`), which for P8 are all fixed bits or two-bit (in)equalities (the tables `_CH`, `PQ`, `X2` of `experiments/a0p38.py`, generated by `mkvt.py`; the conditions of rows 16..22, which define the accepted event, are listed in Appendix C). With W7 in F7 (D7 = 2^29, s0(W7y) - s0(W7x) = 03bff800: the same F7 as the published characteristic), the printed-event probability is 2^-99.56 (6 estimator runs of 2,000 particles; the published characteristic 2^-101.05 with the same estimator).

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

**c7 classes.** W7x = c7(a0) - A_{-1} with c7(a0) = E7 - 2 A3 + S0(A2) + MAJ(A2, A1, a0) - S1(E6) - CH(E6, E5, a0 + C4) - K7. For a chaining value, all variants with the same c7 share W7, so one F7 test decides a class. P8 has 32 classes of the maximal size 24,576 (the published characteristic: classes of 3,840). The attack uses the 8 classes of mask 7fe96c7c: class i = {base_i ^ s : s subset of 7fe96c7c, s in G, c7(base_i ^ s) = c7_i}, 24,576 members each (96 batches of 256), 196,608 variants in all; the bases differ only on bits 31, 18, 12 and 1 (outside the mask).

| class | c7 | base | members |
|---|---|---|---|
| 0 | 2a7beb1b | 9b649791 | 24,576 |
| 1 | 2a7bfb1b | 9b648791 | 24,576 |
| 2 | 2a7feb1b | 9b609793 | 24,576 |
| 3 | 2a7ffb1b | 9b608793 | 24,576 |
| 4 | aa7beb1b | 1b649791 | 24,576 |
| 5 | aa7bfb1b | 1b648791 | 24,576 |
| 6 | aa7feb1b | 1b609793 | 24,576 |
| 7 | aa7ffb1b | 1b608793 | 24,576 |

## 5. Step 2: the W7 test and the good pairs

F7 = {w : s0(w + D7) - s0(w) = 03bff800}, |F7| = 287,309,824 (exhaustive), p7 = |F7| / 2^32 = 2^-3.90197 (the same set as for the published characteristic; it is the union of three affine families of 2^28, 2^24 and 2^21 words, which the replica uses to sample W7). The program tests w = c7 - A_{-1} by computing s0(w + D7) - s0(w) and comparing (24 operations, no table).

**Lemma 5.1 (distribution, per variant).** Under H1, for every fixed a0: Pr[W7x in F7] = p7; conditioned on it, (W0..W6) is uniform and independent of W7, and (W16..W21) is a bijective image of (W0..W5) for fixed (W6, W9..W15), hence uniform and independent of (W6, W7) (Lemma 4.1). Per first block, E[good pairs] = g = 8 x 24,576 x p7 = 13,152 (exact by linearity).

## 6. Step 3: row 16 and the accepted event

### 6.1 Row 16

W16 = s1(W14) + W9 + s0(W1) + W0 and, by Lemma 4.1, W0 = a0 + KW0(CV1), W1 = K1(CV1) - S0(a0) - MAJ(a0, a, b) - S1(E0) - CH(E0, e, f) with E0 = a0 + HH(CV1). So E16x = KP + a0 + s0(W1) with per-first-block constants HH, KP, K1, and row 16 (both members, all its conditions) is a function of E16x alone: an exhaustive pass over all 2^32 values of W16 gives the 160 words of the set R16 (`q3tv.c`, the exhaustive pass of `main`; `selftest` item 2 re-checks it on 20,000 random words and the bit-flip neighbours). The 160 words share 19 bits (mask 4cc79bfa); the program tests the TK = 12 lowest of them (bits 1, 3, 4, 5, 6, 7, 8, 9, 11, 12, 15, 16): stage 3a passes with probability 2^-12 exactly (E16x uniform, Lemma 5.1), row 16 with 160 / 2^32.

### 6.2 The accepted event

The program accepts a row-16 pass iff (i) rows 16..22 of both members follow every cell, '+' pair and two-bit condition of P8 closing at rows 16..22, except that **row 19 is checked on its signed differences only** (the XOR differences of A19, E19, W19 and the member-x values on the difference bits), and (ii) the eight output words A34..A37, E34..E37 of the two members are equal after step 37. Nothing is tested at rows 23..37.

**Lemma 6.1.** If (ii) holds, the two second-block outputs are equal (chaining value plus the same eight words), so M0 || M1 and M0 || M1' collide under the target; M1 != M1' because W7 differs. The program certifies exactly what it outputs.

*Why row 19.* Measured with the estimator (one row at a time checked on signed differences only, the others strict, outputs compared): relaxing row 19 raises q3 by about 3.6 bits for P8 (and 3.4 for the published characteristic); rows 17 and 18 lead to dead ends (the derived conditions there are needed by the next row), rows 20..22 add little. In 20 runs every success has its row-19 conditions in one of four patterns (`pat19`; the 12 conditions: the fixed bits E19[4], E19[18] and ten two-bit conditions):

```
row-19 conditions (in order): E19[4] = 1, E19[18] = 0, E19[10] = E19[29], E19[2] != E19[20], E19[5] != E19[18], E19[6] = E19[19],
E19[10] != E19[28], E19[11] = E19[29], E19[1] = E19[28], A18[29] = A19[29], E19[4] != E19[9], E19[5] != E19[10]
successes of 20 estimator runs (seeds 3001..3020, rebuilt and checked), by the set of violated conditions (1 = violated):
17,497  010000110001   E19[18], conditions 7, 8 and 12 violated
14,829  010000110000   E19[18], conditions 7 and 8 violated
14,457  000000000000   none (the strict row)
10,609  000000000001   condition 12 violated
57,392 of 57,392 successes in these four patterns (the dumps of the runs at the time of the count)
```

## 7. The counted program (`experiments/a0p38.py`, 50,567 bytes, SHA-256 658d60222109bbdff0ef8f9f9c55dc5e865d40c997e54607ecee65b497a9dcf1)

### 7.1 Machine and scalar routines

256-bit word RAM, 64 registers; executed primitives count 1 (load, store, add, sub, and, or, xor, not, shift, immediate, random word), a compare-and-branch 2, one target compression 1 unit; S0, S1, s0, s1 cost 8 each (doubled word, shifts, xors, mask), CH 3, MAJ 4. The routines are executed with counting primitives; broadcast, lane_value, first_lane, r16test and deep add itemised declared counts (their docstrings) (`calibrate`):

| routine | operations |
|---|---|
| first block: 2 random words and their 16 fields (30), counter, cap test, hit-list test (5) | 35 |
| one W7 test (computed, no table), plus 4 for the class loop | 24 + 4 |
| per-first-block scalars HH, PP, QQ, EF, FF, K1, KP | 39 |
| the 7 x 32 broadcast planes (4 each) | 896 |
| per passing class: setup 3, end of class (work counter, cap test) 4 | 7 |
| per batch of 256 variants: the row-16 program of the batch's class + ok test 2 + pointer, compare, branch 4 | 1454..1469 by class (mean 1463) + 6 |
| per stage-3a lane: lowest lane (32), clear and loop (3), a0 from the stored planes (85), E16x (38+), the row-16 table test (42) | 200 |
| per row-16 pass (itemised declared count): Step 2 for both members, the expansion and rows 16..37 of both members with the tests of rows 16..22, the output comparison | 3105 |

### 7.2 The row-16 program

Bit L of a 256-bit plane belongs to lane L (one variant). Inputs: the planes of the 21 bits of a0 in the mask (stored per batch), the 4 bits where the class bases differ (class constants), the 224 broadcast planes; the 7 bits common to all 8 bases are folded. `build_e16` builds, bit-interleaved, the DAG of E0 = a0 + HH, then per bit j: S0(a0), MAJ(a0, a, b) = PP | (a0 & QQ), S1(E0), CH(E0, e, f) = FF ^ (E0 & EF), the three ripple adders of their sum T and the subtraction W1 = K1 - T, then per tested position j <= 16: s0(W1), the two adders of E16x and the comparison with the common value; constants are folded and equal nodes shared. `schedule` allocates 64 registers by Belady's rule (evict the value needed farthest ahead; store it first if it is needed again and has no copy); every load, store and spill is an instruction. Result with per-class specialization (this derivative): the four class-dependence bits are folded to each class's base bits, giving eight programs of **[1466, 1457, 1469, 1466, 1463, 1454, 1466, 1463] instructions** (mean 1463, max 1469), against 1511 for the single shared program of the base package; the ledger charges the mean for expected work and the max inside the work cap. The program is executed instruction by instruction (`run_prog`) and compared with the scalar definition lane by lane (`selftest` item 4 and the organizer experiment `a0p-online-r38`: 0 mismatches).

## 8. The algorithm (fixed caps)

```text
advice: S (the semi-free-start pair's rows 0..15), the 8 class descriptors (c7, base); precompute (charged): every class member (base ^ s, s subset of 7fe96c7c, in G, c7 = c7_i), stored as 96 batches of 21 bit planes; the row-16 program
V = 0
for f = 1 .. N_FB:
    if V > V_MAX: halt (failure)                    (V accumulates ALL data-dependent work of every first block: W7 tests, hit list, scalars, planes, classes, lanes, row-16 passes)
    two uniform 256-bit random words -> M0 (16 words, uniform on {0,1}^512); CV1 := F_38(IV, M0)                     [1 unit]
    hits := [i : c7_i - A_{-1} in F7]                                                                               [8 x (24 + 4)]
    if hits: the scalars and the broadcast planes
        for i in hits: for each of the 96 batches of class i: run the row-16 program -> ok plane
            for each lane of ok: a0 from the planes; E16x; if E16x in R16: Step 2, rows 16..37 of both members, the tests of rows 16..22
                (row 19 on signed differences), compare the outputs; if equal: output M0 || M1, M0 || M1' and halt
        V += the work of the class (and, before it, the W7 tests, the hit list, the scalars and the planes of this first block); if V > V_MAX: halt (failure)
halt (failure)
```

*Lemma 8.1 (the cap).* V accumulates every data-dependent operation of every first block (all of v_f in Section 9) and is tested before every first block and after every class, so V <= V_MAX + OVER at every moment, OVER = 650,923,471 (one first block at its maximum: all classes passing, every lane a row-16 pass). The 35 fixed operations per first block are charged separately (N_FB x 35). The run never outputs a non-collision (Lemma 6.1).

## 9. The success probability

*Trials and expectation.* A trial is (first block f, selected variant a0); A_t: a0 is good for f (W7 in F7) and the pair is in the accepted event. E[X_f] = g q3 (Lemma 5.1; H1, H2).

*q3 (H2).* q3 = the average over the 196,608 selected variants of Pr[accepted event | good pair] (including the row-16 factor 160 / 2^32). Estimator `q3tv.c` (`DIFFROW=19 RELAX_TAIL=1`): fixed-effort multilevel splitting, row 16 exact over the 160 W16 words, rows 17..22 with W_i^x uniform (Lemma 5.1) and the rows checked as in the event (row 19 on signed differences), tail: a variant drawn per proposal from the 196,608 selected variants, W7 uniform in F7, rows 23..37 computed, outputs compared. Every success is a verified collision; the successes are rebuilt into real pairs (300 of 300 checked with the reference). 20 runs, 4,000 particles, 16,384 tail proposals per particle, seeds 3001..3020 fixed before the runs:

| seed | stage factors log2 (rows 16..22, tail) | successes (all collisions) | log2 q3 |
|---|---|---|---|
| 3001 | -24.678 -17.014 -13.942 -2.991 -15.982 -6.976 -0.984 -14.206 | 3,467 | -96.7734 |
| 3002 | -24.678 -16.969 -13.908 -2.994 -14.506 -6.971 -0.999 -13.713 | 4,882 | -94.7369 |
| 3003 | -24.678 -17.007 -13.978 -2.985 -15.954 -7.010 -1.026 -14.224 | 3,424 | -96.8639 |
| 3004 | -24.678 -17.004 -13.914 -3.002 -15.158 -6.985 -1.000 -13.813 | 4,554 | -95.5535 |
| 3005 | -24.678 -17.031 -13.942 -3.021 -16.997 -7.015 -0.993 -13.456 | 5,834 | -97.1320 |
| 3006 | -24.678 -17.013 -13.971 -2.979 -16.377 -7.003 -1.015 -13.294 | 6,527 | -96.3298 |
| 3007 | -24.678 -16.988 -13.897 -3.028 -16.445 -6.972 -0.994 -13.494 | 5,680 | -96.4961 |
| 3008 | -24.678 -16.994 -13.924 -2.988 -16.376 -6.998 -1.019 -13.354 | 6,261 | -96.3297 |
| 3009 | -24.678 -16.978 -13.910 -3.011 -16.363 -7.029 -0.989 -14.227 | 3,418 | -97.1861 |
| 3010 | -24.678 -17.013 -13.936 -3.020 -15.634 -7.039 -1.025 -13.944 | 4,157 | -96.2893 |
| 3011 | -24.678 -16.991 -13.942 -3.027 -16.038 -7.005 -0.953 -13.732 | 4,816 | -96.3673 |
| 3012 | -24.678 -16.972 -13.979 -3.026 -15.977 -7.041 -1.003 -13.872 | 4,372 | -96.5483 |
| 3013 | -24.678 -17.014 -13.946 -3.033 -15.966 -7.001 -0.995 -13.847 | 4,449 | -96.4780 |
| 3014 | -24.678 -16.979 -13.850 -3.016 -16.398 -6.997 -1.024 -13.977 | 4,063 | -96.9199 |
| 3015 | -24.678 -16.983 -14.013 -2.983 -16.409 -7.020 -0.968 -13.733 | 4,814 | -96.7870 |
| 3016 | -24.678 -16.976 -13.892 -3.033 -15.652 -6.991 -1.019 -13.769 | 4,696 | -96.0099 |
| 3017 | -24.678 -17.015 -13.973 -2.993 -16.399 -6.965 -0.984 -13.569 | 5,393 | -96.5753 |
| 3018 | -24.678 -16.998 -13.943 -2.989 -15.657 -7.011 -1.013 -13.636 | 5,148 | -95.9257 |
| 3019 | stalled at row 20 (no estimate: counted as 0) | 0 | 0 (stalled) |
| 3020 | -24.678 -16.987 -13.903 -2.984 -15.965 -6.987 -1.005 -14.278 | 3,299 | -96.7867 |

Mean 2^-96.3683, relative sd 0.605, one-sided 99% Student bound (t = 2.539, 19 degrees of freedom) 2^-96.9759, bootstrap 1% quantile of the mean 2^-96.8088; 89,254 successes. The row-20 stage carries most of the variance (the row-19 pattern decides whether row 20 can hold); run 3019 found no row-20 survivor within its 2^34 trials and is counted as an estimate of 0. **q3_model = 2^-97.0000.**

*The pair term (H3).* Every success passes row 16, so given A_t, X_f - 1 <= R_f - 1 (the other row-16 passes of f). Measured (`h3p.py`): 750 successes rebuilt and verified (all accepted by the program's event, so the estimator's event and the program's agree on every one; 99% bound on a disagreement rate 0.6%), all 750 re-found in their own class; every selected variant of every passing class evaluated on the success's CV1: 1,495 passing classes, 36,741,120 variants, **2 other row-16 passes, 0 further accepted pairs** (1.37 expected under independence). One-sided 99% Poisson limit of E[R_f - 1 | A_t]: 0.0112 = 2^-6.48; charged 2^-5.9.

*Bonferroni, independence, caps.* Pr[X_f >= 1] >= E[X_f] - E[X_f (X_f - 1)] / 2 >= g q3 (1 - 2^h3 / 2); first blocks are independent (fresh coins); the data-dependent work v_f of a first block satisfies 0 <= v_f <= vmax_f = 650,955,727 with mean at most vbar = 79308.7713 (exact rational in the ledger), so Var(sum v_f) <= N_FB vmax_f vbar and Chebyshev bounds Pr[sum v_f > (1 + 2^-16) N_FB vbar] by P_cap = 5.870e-12; V_MAX = ceil((1 + 2^-16) N_FB vbar). On the complement no cap halts the run. N_FB is the least integer with 1 - exp(-N_FB g q3_model (1 - 2^h3 / 2)) - P_cap - 2^-60 >= 0.39 (2^-60 covers the rounding of the exponential, evaluated at 80 decimal digits).

## 10. Ledger (exact; `ledger_a0p.py`, Appendix B)

```text
T = A_C + A_S + DEV + N_FB + (N_FB x 35 + V_MAX + OVER + PRE + FIN) / C + 6
  A_C = 2^48, A_S = 2^50, DEV = 2^50 (Section 12, H4)
  N_FB = 6,005,607,090,204,795,643,666,036 = 2^82.31258   (g = 13,152 good pairs per first block, g q3_model = 2^-83.3170)
  vbar = 76842.7713 operations per first block: W7 tests 8 x (24 + 4), hit list, scalars and planes (935) x min(1, 8 p7),
         passing classes 8 p7 x (7 + 96 x (1463 + 6)) (mean program count; the cap uses the max, 1469), stage-3a lanes 8 p7 x 24,576 x 2^-12 x 200, row-16 passes 8 p7 x 24,576 x 160 / 2^32 x 3105
  V_MAX = 461,494,533,862,390,953,116,437,989,059, OVER = 650,923,471, PRE = 4,974,313,472 (member tests over the 8 class cubes, the batch planes, program generation)
  FIN = 1,600 operations and 6 units (the final verification)
N = T x 2728 = 478,967,264,778,606,371,249,269,704,894  ->  T = 2^87.18221388  ->  time_log2 = 87.18222
```

*Certificate.* `python3 ledger_a0p.py --q3 -97.0 --h3 -5.9` (the defaults) prints the ledger and checks `(2728^E << 8718221) < N^E <= (2728^E << 8718222)` with E = 100000 (exact integers), so 87.18222 is the smallest five-decimal upper bound on log2 T. *Sensitivity:*

```
claimed                                                                        87.18222   (N_FB 2^82.3126)
q3_model = the C-study mean 2^-96.3683                                         86.55197   (N_FB 2^81.6809)
q3_model 2^-97.0                                                               87.18222   (N_FB 2^82.3126)
q3_model 2^-97.78 (the q3_model of fb176310 for the published characteristic)  87.96111   (N_FB 2^83.0926)
pair term 2^-3                                                                 87.26305   (N_FB 2^82.3936)
A_C = 2^48, A_S = 2^50, DEV = 2^50 (the charges of 1a695f0b)                   87.17957   (N_FB 2^82.3126)
A_C = 2^84                                                                     87.33076   (N_FB 2^82.3126)
row-16 program at 1511 instructions (the shared program of 1a695f0b)           87.22615   (N_FB 2^82.3126)
```

## 11. Memory and advice

```
online 935040 bytes = 2^19.835: row-16 programs 11,704 instructions in total (eight per-class programs), class planes 8 x 96 batches x 21 words, class table 8 x 6 words,
  broadcast planes 224 words, row-16 table 160 words, spill slots 24 words, scalar routines at most 700 instructions, the deep path's two
  traces (200 words), M0, CV1 and counters (32 words); 32 bytes per word or instruction
preprocessing (single-threaded, sequential; peak of the summed resident memory of all processes of each computation):
  Step-1 solve of P8 (joint.py: value-exact dense part and tail, Python model + Kissat): 279,720 KB = 2^28.094 (sampled every 0.2 s)
  the signed search that found P8 (stepk.py + Kissat, same specification and seed): at most 248,000 KB = 2^27.92 over 2 h 20 min
    (Python 152,868 KB and Kissat 80,816 to 88,096 KB resident together; stopped after the original 78-minute solve time)
  the class descriptors (a0cls.c, 32 passes): 37,036 KB = 2^25.14; the condition tables and pair (mkvt.py, fromjoint.py): below 2^24
preprocessing peak 2^28.094
```

*Scope of the memory bound.* Peak memory covers code, advice, retained data, tables and working state of the whole computation: the online algorithm, the charged precomputation (class members, planes, the program) and the computations behind the advice and the allowances (the characteristic search, the Step-1 solve, the class descriptors, the condition tables), each run single-threaded and sequentially. The class descriptors are found in 32 passes over a hash of c7 (`a0cls.c`, at most 2^23 pairs resident). The online figure also covers the deep path's working state (two traces, about 6 KB) and M0, CV1.

Claimed memory 2^28.10 bytes: the maximum of the online footprint and the measured preprocessing peaks. Advice: S (16 words of each member and CV1), the 8 class descriptors, the constants of the characteristic: below 2^14 bytes; everything else (class members, planes, the program) is computed by the charged preprocessing.

## 12. Premises

- **H1** single-trial chaining value: CV1 = F_38(IV, M0) for uniform M0 behaves as uniform for the events of one variant (Lemma 5.1).
- **H2** q3 >= q3_model for the accepted event, averaged over the selected variants (Section 9; 20 runs).
- **H3** the pair term within a first block is at most 2^h3 (Section 9; measured).
- **H4** allowances: this derivative charges A_C = 2^78, A_S = 2^74, DEV = 2^70 (the allowance levels of fb176310) as envelopes. The base package measured its campaign at under 2^21 core-seconds in all and charged 2^48/2^50/2^50 (which would give 87.17957 here); the charged envelopes are more than 2^29 above that, so the claim is insensitive to the wall-clock conversion (A_C = 2^84 gives 87.33061; Section 10 sensitivity).
- **H5** unit-cost bit-sliced planes: the row-16 program is charged as its instruction count on 256-bit planes, as in the cost model.

## 13. Organizer experiments (`experiments/manifest.json`)

**a0p-online-r38** (H1, H5, Lemma 4.1). Each active trial first draws 32 unconditional organizer-seeded first blocks and counts passing classes (H1 expectation 32 x 8 x |F7|/2^32 = 17.1 passing classes, reported as uncond_class_passes), then draws first blocks from the organizer seed (two uniform words each, real 38-step compressions) until one has a passing class (at most 64); its first passing class is run on two batches (the class's first 512 members): the row-16 program's ok plane is compared lane by lane with E16x from the Step-2 words and the 38-step trace, and W7 with c7 - A_{-1} and F7; trial 0 also runs the batch of the semi-free-start pair's variant and requires the counted program to find and accept it. A pair M0 || M1, M0 || M1' (one variant, not a collision) is returned iff there is no mismatch. Trials 8..255 return no pair by design.

**a0p-q3-r38** (H2, H3 near term). Trials 0..9: 10 replicates of the estimator of q3 for the accepted event; the first replicate with an accepted pair also reports near_row16, the other full row-16 passes among the 24,575 other variants of the success's class on the same chaining value (organizer-run H3 near term; first replicate only, for the organizer time budget) (64 particles; 64, 8, 8, 4, 2, 1 children at rows 17..22 with the row's E bits imposed, at row 19 one of the four patterns drawn uniformly, weight 4 x 2^-f; tail: 192 proposals per particle, a variant of 512 embedded samples of the selected classes, W7 sampled uniformly in F7 by its affine families, rows 23..37, outputs compared; every success rebuilt into CV1, M1, M1' and accepted only if it is a 38-step collision in the accepted event with W7 in F7). Trial t < 10 returns its first verified pair as CV1 || M1 and CV1 || M1' (semi-free-start collisions, never collisions from the IV); trial 10 returns a pair iff no rebuild failed and the mean of the 10 estimates is at least 2^-98.6000 (pass rule fixed from 48 development requests before any validation run; their pooled means: minimum -98.527, 5% quantile -97.251, median -96.327; replicate mean 2^-96.2992).

*Validation by us* (the shipped file; 256 trials; network-less container, 1 CPU, 128 MiB; python:3.12.12-slim-bookworm):

```
holdA  a0p-online-r38  returned  8  lanes 4096  mismatches 0  stage-3a passes 0  first blocks 20  0.3s
holdA  a0p-q3-r38      returned  5  pooled 2^-97.053 (rule >= 2^-98.6)  replicates with a success 4/10  verified pairs 5  failed rebuilds 0  5.7s
holdB  a0p-online-r38  returned  8  lanes 4096  mismatches 0  stage-3a passes 0  first blocks 28  0.3s
holdB  a0p-q3-r38      returned  9  pooled 2^-96.288 (rule >= 2^-98.6)  replicates with a success 8/10  verified pairs 11  failed rebuilds 0  5.6s
holdC  a0p-online-r38  returned  8  lanes 4096  mismatches 0  stage-3a passes 1  first blocks 19  0.4s
holdC  a0p-q3-r38      returned  8  pooled 2^-96.266 (rule >= 2^-98.6)  replicates with a success 7/10  verified pairs 11  failed rebuilds 0  5.7s
holdD  a0p-online-r38  returned  8  lanes 4096  mismatches 0  stage-3a passes 0  first blocks 30  0.3s
holdD  a0p-q3-r38      returned  8  pooled 2^-95.893 (rule >= 2^-98.6)  replicates with a success 7/10  verified pairs 9  failed rebuilds 0  5.6s
public a0p-online-r38  returned  8  lanes 4096  mismatches 0  stage-3a passes 0  first blocks 36  0.3s
public a0p-q3-r38      returned  7  pooled 2^-96.555 (rule >= 2^-98.6)  replicates with a success 6/10  verified pairs 8  failed rebuilds 0  5.6s
```

## 14. Limitations

- q3 is a Monte Carlo estimate (participant-run, resampled particles; the Student bound assumes independent runs); the organizer replica checks a reduced version of it. The row-19 pattern support of the replica is the four patterns seen in the study, so the replica estimates a lower bound of the event's probability.
- The pair term and the success distribution are measured on rebuilt estimator successes (H1 premise for real chaining values).
- The bit-sliced program is executed on sampled batches; full-scale execution is infeasible.

## Appendix A. Self-test and calibration of `experiments/a0p38.py`

```
1 the semi-free-start pair collides, M != M', accepted event, W7 in F7 ok 
  its variant A0 is in G and in a selected class                       ok (class 3)
2 row 16: the 160 W16 words hold it; 20,000 random words and 1,280 neighbours agree ok 
3 Lemma 4.1: E16x formula, W7 = c7 - A_-1, rows 11..15 and the word differences on 20 chaining values ok 
4 row-16 programs (one per class): instructions, loads, spill stores   ok [1466, 1457, 1469, 1466, 1463, 1454, 1466, 1463] (245 loads, 18 stores)
  program against the definition on 2 x 512 lanes of real first blocks ok [{'first_blocks': 2, 'passing_classes': 2, 'lanes': 512, 'stage3a_passes': 1, 'mismatches': 0}, {'first_blocks': 4, 'passing_classes': 2, 'lanes': 512, 'stage3a_passes': 0, 'mismatches': 0}]
5 the counted program finds the semi-free-start pair in its batch      ok (5757 operations)
6 replicate: estimate, accepted pairs rebuilt and verified, failed rebuilds 0 ok (log2 None, 0 pairs)
   calibrate: {'prog': [1466, 1457, 1469, 1466, 1463, 1454, 1466, 1463], 'prog_max': 1469, 'w7': 24, 'fb_fixed': 35, 'w7_loop': 4, 'scalars': 39, 'planes': 896, 'batch_ctl': 6, 'class_ctl': 7, 'lane': 200, 'deep': 3105, 'tk': 12, 'classes': 8, 'class_size': 24576}
SELFTEST PASSED
```

## Appendix C. The conditions of rows 16..22 (the accepted event; member x, `experiments/a0p38.py` tables)

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

## Appendix B. Programs (SHA-256 and full listings; `experiments/a0p38.py` is assembled by `mka0p.py` from the `a0p_*.py` parts)

- `experiments/a0p38.py`: 658d60222109bbdff0ef8f9f9c55dc5e865d40c997e54607ecee65b497a9dcf1 (this derivative; base package file e58aeda0a79c9367fa02d3b652e84fa13cb787e42d43be3b05367e484c46c7d8)
- `ledger_a0p.py`: d839ac11051e0a457dfec35ad2fddb42e5fed250b4bb710080ae7798450788ef
- `a0cls.c`: d8226a2dc82ccd814848e43393ca49e48cc18a5b91202e2ace0118bfb43d1b5d
- `a0p_ref.py`: 43b45ada08445b79c6e1e22ea630e76fc4d4299a1274f863f770a004f49aeadc
- `a0p_core.py`: 435f2837545b9f3b52b04fa8b915cc8b0d6cc045b0b986fe1cd33fd1211747cd
- `a0p_prog.py`: 8a57e82530b0f3518653b793af3b2579b240d4139b98f0d02b22e076b16b002b
- `a0p_scal.py`: d4ee1e2db69ca2968a71c736996c34e821fe25e71a30b3afca8ef207d757a3ed
- `a0p_run.py`: 3fa0cde4750ca267779438f369d4ebe1a204698c6807873c333332122b4876fa
- `a0p_main.py`: da5375b63d77fb35dd3e8e00c90fe138bf2c8b041585a0ea476ed76110ef7875
- `mka0p.py`: e41ddcfff8c76bbe9c796ad7214f28367b6eb8aa2c1ca24c0ab606bebc98db1e
- `mkvt.py`: 19e95c874e6d0b05447836aea5d7289a467c581bcb03bb94376154d04e25b26a
- `a0fam.c`: e74ead8bd7d20ce7ef40284fd91a104ce71b3fe5b8cadcd59b9c274b3ad4eb69
- `h3p.py`: 04ec03dc0da1134d677a02a4d4195c1aa05747805e6063e47c195233256c6d43
- `q3tv.c`: e01dbb414ef2a7e0cecf79638bb287130e1309dfa439727b57bc8b32b3957ead
- `sweep.py`: 7e2dcef5b849da79236857a328306ddee77c3acf34975e6c5bb72ab69dcbc918
- `stepk.py`: 59284d8f7f19bb62cc0265f3b9e18ac2d1532b79a755d6e3d3b672298dfc9ab0
- `score.py`: 22df6e29bdeef726bb395123426656641e262e8d5cd3117839caba4e1682493e
- `joint.py`: 7e641e68540e79d3be7902d52bccb372febe17dc16ca5364f9390c3ecf37cb95
- `fromjoint.py`: a05593f8e0104ee3d2d378257159d45bce7108f7d5130f43a53c5850bd762b61
- `prep.py`: 7550447964f6b5444638db1b60142475ea839cb066e262b6bfeb6d713b957299
- `cond.py`: 2220ff08693b795d999eabb5c31dac06fcf9905eb57f403bdd2dbe05901426a8
- `sdmodel.py`: fac660e9f5de63bf4e071ec7538598ceff1362466b26e37be28f9f8f3cfae416
- `vmodel.py`: 86bafa88614a1b85b1d3601f3b27479c381442769b0fda054ff7651dbd84244d
- `sha38.py`: 7aa83ceebd6baede02877736640e066e09d640656a08929e792ae1c5c1b0fe67
- `mkpkg3.py`: 6b4b960bdb216e23b9d76cb09fb843f170fa01971f2a447184c6f1216f319afe

### ledger_a0p.py

```python
#!/usr/bin/env python3
"""ledger_a0p.py - exact ledger of the A0-variant attack with P8 (own code; the structure of the ledger of 2d1c4fc2 / fb176310).
T = A_C + A_S + DEV + N_FB + (N_FB x FIXED + V_MAX + OVER + PRE + FIN_OPS) / C + FIN_UNITS, in target compressions, C = 2728.
Every count is an executed count of experiments/a0p38.py (`calibrate`); probabilities: p7 = |F7| / 2^32 (exhaustive), the stage-3a rate 2^-12
and the row-16 rate 160 / 2^32 (exact under Lemma 5.1), q3_model (H2), the pair term (H3).  Integers and fractions; logs at 80 digits."""
from fractions import Fraction as Fr
from decimal import Decimal as D, getcontext
import math, argparse, json
getcontext().prec = 80
C = 2728
F7 = 287_309_824; p7 = Fr(F7, 2 ** 32)
CAL = dict(prog=[1466, 1457, 1469, 1466, 1463, 1454, 1466, 1463], w7=24, fb_fixed=35, w7_loop=4, scalars=39, planes=896, batch_ctl=6, class_ctl=7, lane=200, deep=3105, tk=12, classes=8, class_size=24576)

def dlog2(x):
    x = Fr(x); return (D(x.numerator).ln() - D(x.denominator).ln()) / D(2).ln()
def qmodel(q):
    num = Fr(round(q * 10000)) / 10000
    return Fr(int((D(2) ** (D(num.numerator) / D(num.denominator))) * D(10) ** 75), 10 ** 75)

def ledger(q3=-97.0, h3=-5.9, AC=78, AS=74, DEV=70, succ=Fr(39, 100), eps=Fr(1, 2 ** 16), cal=None, NFB=None):
    k = dict(CAL, **(cal or {}))
    ncl, size = k['classes'], k['class_size']; nb = size // 256
    q = qmodel(q3); g = ncl * size * p7                              # good pairs per first block (exact, linearity)
    prog_list = k['prog'] if isinstance(k['prog'], list) else [k['prog']] * ncl
    per_class = k['class_ctl'] + nb * (Fr(sum(prog_list), ncl) + k['batch_ctl'])     # expected work of one passing class (mean program)
    per_class_max = k['class_ctl'] + nb * (max(prog_list) + k['batch_ctl'])       # maximal work of one passing class (cap)
    lanes = Fr(size, 2 ** k['tk']) * k['lane']                         # expected stage-3a lanes of a passing class x their cost
    r16 = Fr(size * 160, 2 ** 32) * k['deep']                          # expected row-16 passes of a passing class x their cost
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
    PRE = ncl * (1 << (bin(0x7fe96c7c).count('1'))) * 40 + ncl * nb * 256 * 21 * 2 + 2 ** 32   # member tests over the class cubes (40 each), planes (2 per member bit), program generation
    FIN_OPS, FIN_UNITS = 1600, 6
    alw = 2 ** AC + 2 ** AS + 2 ** DEV
    N = C * (alw + NFB + FIN_UNITS) + NFB * k['fb_fixed'] + VMAX + over + PRE + FIN_OPS
    T = Fr(N, C); claim = math.ceil(float(dlog2(T)) * 1e5) / 1e5
    assert D(N).ln() - D(C).ln() <= D(round(claim * 1e5)) / D(100000) * D(2).ln()
    return dict(NFB=NFB, log2NFB=float(dlog2(NFB)), g=float(g), log2gq=float(dlog2(g * q)), vbar=float(vbar), vbar_exact=vbar, vmax=vmax, VMAX=VMAX,
                over=over, PRE=PRE, Pcap=float(pcap(NFB)), N=N, log2T=float(dlog2(T)), claim=claim, per_class=per_class, alw=float(dlog2(alw)),
                pre_log2=float(dlog2(Fr(PRE, C) + alw)), attack=float(dlog2(Fr(N - C * alw, C))))

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--q3', type=float, default=-97.0); ap.add_argument('--h3', type=float, default=-5.9)
    ap.add_argument('--cal', default=None); ap.add_argument('--sens', action='store_true'); a = ap.parse_args()
    cal = json.loads(open(a.cal).read()) if a.cal else None
    r = ledger(a.q3, a.h3, cal=cal)
    for key in ('NFB', 'log2NFB', 'g', 'log2gq', 'vbar', 'vmax', 'VMAX', 'over', 'PRE', 'Pcap', 'per_class', 'alw', 'pre_log2', 'attack', 'N', 'log2T', 'claim'): print(key, r[key])
    n, E5, kk = r['N'], 100000, round(r['claim'] * 100000)
    assert (C ** E5 << (kk - 1)) < n ** E5 <= (C ** E5 << kk); print('certificate: (2728^E << %d) < N^E <= (2728^E << %d)' % (kk - 1, kk))
    if a.sens:
        for nm, kw in [('q3_model = the C-study mean 2^-96.3683', dict(q3=-96.3683)), ('q3_model 2^-97.78 (the q3_model of fb176310)', dict(q3=-97.78)),
                       ('pair term 2^-3', dict(h3=-3.0)), ('A_C = 2^78', dict(AC=78)), ('A_C = 2^84', dict(AC=84)), ('row-16 program at 1511 instructions (the shared program of 1a695f0b)', dict(cal=dict(prog=1511)))]:
            kw2 = dict(q3=a.q3, h3=a.h3, cal=cal); kw2.update(kw); x = ledger(**kw2); print('%-40s %.5f (attack %.4f)' % (nm, x['claim'], x['attack']))
```

### a0cls.c

```c
// A0-only variant family of a dense part and its c7 classes (own code). a0fam <pair: cv Wx[16] Wy[16] hex> [min class size, out file]
// a0cls: the same in 32 passes over a hash of c7 (at most 2^23 pairs resident; peak memory measured in proof.md 11).
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
# 2026/1120 / 2026/1080; this code, the characteristic P8 and its accepted event (row 19 on signed differences) are ours.
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
#<<CONSTS>>
CELLS = [[(0, 0, 0, 0)] * NR for _ in range(3)]
for _k in range(3):
    for _i, _c in _CH[_k].items(): CELLS[_k][_i] = _c
_tx, _ty = trace(PCV, PMX), trace(PCV, PMY)
SAx = {i: _tx[0][i] for i in range(-4, 16)}; SEx = {i: _tx[1][i] for i in range(-4, 16)}
SAy = {i: _ty[0][i] for i in range(-4, 16)}; SEy = {i: _ty[1][i] for i in range(-4, 16)}
DWT = [(_ty[2][i] - _tx[2][i]) & M for i in range(NR)]          # modular differences of the words (y - x) of the pair
D7 = DWT[7]; T7 = 0x03bff800                                   # s0(W7y) - s0(W7x) required by rows 22/23 (the trail)
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
TK = 12                                                            # tested bits of the row-16 filter: the TK lowest shared bits
TBITS = [j for j in range(32) if (SHARED >> j) & 1][:TK]

# ---- classes (proof.md Section 5): class i = {base ^ s : s subset of MASK, a0 in G, c7(a0) = c7_i}, 24,576 variants each ----
def dep(t, mask):
    """bits of t deposited on the set bits of mask (lowest first)"""
    r = 0; j = 0
    while mask:
        b = mask & -mask
        if (t >> j) & 1: r |= b
        mask ^= b; j += 1
    return r
def members(ci, count, start=0):
    """the members number start..start+count-1 of class ci in the canonical order (increasing t of base ^ dep(t, MASK))"""
    c7, base = CLASSES[ci]; out = []; t = 0; k = 0
    while len(out) < count and t < (1 << bin(MASK).count('1')):
        a0 = base ^ dep(t, MASK); t += 1
        if in_G(a0) and c7of(a0) == c7:
            if k >= start: out.append(a0)
            k += 1
    return out

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
# E16x = KP + a0 + s0(W1), W1 = K1 - S0(a0) - MAJ(a0, a, b) - S1(E0) - CH(E0, e, f), E0 = a0 + HH (Lemma 4.1), and their AND with the
# tested values.  Inputs: the planes of the bits of a0 that vary in the batch (A<j>), the class constants (C<j>, broadcast words), and the
# per-first-block broadcast planes of HH, PP = a & b, QQ = a | b, EF = e ^ f, FF = f, K1 = A1 - g - K1, KP (7 x 32).  Constant bits of a0 are
# folded.  Nodes: xor, and, or, not; equal nodes are shared.  The allocator gives an instruction list over 64 registers in which every
# load, store and spill is one instruction; the list is the charge.
ONES = (1 << 256) - 1
class Prog:
    def __init__(s): s.nodes = [None, None]; s.cache = {}; s.inputs = {}
    def inp(s, name):
        if name not in s.inputs: s.nodes.append(('in', name)); s.inputs[name] = len(s.nodes) - 1
        return s.inputs[name]
    def _mk(s, op, a, b=None):
        key = (op, a, b) if op == 'not' or b is None else (op,) + tuple(sorted((a, b)))
        if key not in s.cache: s.nodes.append(key); s.cache[key] = len(s.nodes) - 1
        return s.cache[key]
    def not_(s, a):
        if a < 2: return 1 - a
        n = s.nodes[a]
        return n[1] if n[0] == 'not' else s._mk('not', a)
    def xor(s, a, b):
        if a == 0: return b
        if b == 0: return a
        if a == b: return 0
        if a == 1: return s.not_(b)
        if b == 1: return s.not_(a)
        return s._mk('xor', a, b)
    def and_(s, a, b):
        if a == 0 or b == 0: return 0
        if a == 1: return b
        if b == 1 or a == b: return a
        return s._mk('and', a, b)
    def or_(s, a, b):
        if a == 1 or b == 1: return 1
        if a == 0: return b
        if b == 0 or a == b: return a
        return s._mk('or', a, b)
    def add(s, x, y, cin=0, n=32):
        """ripple addition of two bit lists (LSB first), n result bits"""
        out = []; c = cin
        for j in range(n):
            t = s.xor(x[j], y[j]); out.append(s.xor(t, c))
            c = s.or_(s.and_(x[j], y[j]), s.and_(c, t))
        return out

def build_e16(cbits, nlane):
    """cbits[j]: 'L' (lane-varying bit of a0), 'C' (class constant, input), 0 or 1 (folded).  Returns (Prog, ok node)."""
    p = Prog()
    a0 = [p.inp('A%d' % j) if cbits[j] == 'L' else p.inp('C%d' % j) if cbits[j] == 'C' else cbits[j] for j in range(32)]
    bc = lambda nm: [p.inp('%s%d' % (nm, j)) for j in range(32)]
    HH, PP, QQ, EF, FF, K1, KP = (bc(n) for n in ('HH', 'PP', 'QQ', 'EF', 'FF', 'K1', 'KP'))
    rot = lambda w, r: [w[(j + r) % 32] for j in range(32)]
    x3 = lambda u, v, w: [p.xor(p.xor(u[j], v[j]), w[j]) for j in range(32)]
    E0 = p.add(a0, HH)
    # bit-interleaved: at bit j the four operands of T = S0(a0) + MAJ + S1(E0) + CH, the three adders of T and the subtraction K1 - T
    c = [0, 0, 0, 1]; T1 = []; W1 = []
    def fa(x, y, ci):
        t = p.xor(x, y); return p.xor(t, ci), p.or_(p.and_(x, y), p.and_(ci, t))
    for j in range(32):
        sa = p.xor(p.xor(a0[(j + 2) % 32], a0[(j + 13) % 32]), a0[(j + 22) % 32])
        mj = p.or_(PP[j], p.and_(a0[j], QQ[j]))
        ss = p.xor(p.xor(E0[(j + 6) % 32], E0[(j + 11) % 32]), E0[(j + 25) % 32])
        cv = p.xor(FF[j], p.and_(E0[j], EF[j]))
        u, c[0] = fa(sa, mj, c[0]); v, c[1] = fa(ss, cv, c[1]); t, c[2] = fa(u, v, c[2])
        w, c[3] = fa(K1[j], p.not_(t), c[3]); W1.append(w)
    n = max(TBITS) + 1; d = [0, 0]; ok = 1
    for j in range(n):
        s0w = p.xor(p.xor(W1[(j + 7) % 32], W1[(j + 18) % 32]), W1[j + 3] if j + 3 < 32 else 0)
        u, d[0] = fa(KP[j], a0[j], d[0]); e, d[1] = fa(u, s0w, d[1])
        if j in TBITS: ok = p.and_(ok, e if (R16[0] >> j) & 1 else p.not_(e))
    return p, ok

def schedule(p, root, nreg=64):
    """Belady allocation of the nodes root depends on, in creation order: instruction list [(op, dst, src...)] with 'ld' (input or spill
    slot), 'st' (spill), 'xor', 'and', 'or', 'not', 'out'; returns (instructions, spill slots used)."""
    need = set(); st = [root]
    while st:
        x = st.pop()
        if x < 2 or x in need: continue
        need.add(x); n = p.nodes[x]
        if n[0] != 'in': st.extend(n[1:] if n[0] != 'not' else n[1:2])
    order = [x for x in range(2, len(p.nodes)) if x in need and p.nodes[x][0] != 'in']
    uses = {}
    for t, x in enumerate(order):
        n = p.nodes[x]
        for o in (n[1:] if n[0] != 'not' else n[1:2]):
            if o >= 2: uses.setdefault(o, []).append(t)
    uses.setdefault(root, []).append(len(order))
    ptr = {x: 0 for x in uses}
    def nxt(x):
        u = uses.get(x, []); i = ptr.get(x, 0)
        return u[i] if i < len(u) else 1 << 40
    reg = {}; free = list(range(nreg)); inmem = set(x for x in need if p.nodes[x][0] == 'in'); slots = {}; ins = []; maxslot = 0
    def evict(t, keep):
        nonlocal maxslot
        v = max((x for x in reg if x not in keep), key=nxt)
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
        keep = set(o for o in ops if o >= 2)
        rs = []
        for o in ops:
            if o < 2: rs.append(CONST[o])
            else: rs.append(load(o, t, keep))
        for o in ops:
            if o >= 2: ptr[o] += 1
        dead = [o for o in ops if o >= 2 and nxt(o) >= (1 << 40) and o in reg]
        if dead: r = reg.pop(dead[0]); [free.append(reg.pop(d)) for d in dead[1:] if d in reg]
        else: r = getreg(t, keep)
        ins.append((n[0], r) + tuple(rs)); reg[x] = r
    ins.append(('out', reg[root] if root >= 2 else CONST[root]))
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
    """per first block: HH, PP, QQ, EF, FF, K1, KP of the program (Lemma 4.1) and A1-independent words"""
    a, b, c, d, e, f, g, h = cv
    hh = m.and_(m.sub(m.sub(d, S0m(m, a)), MAJm(m, a, b, c)), M)
    kw0 = m.and_(m.sub(m.sub(m.sub(m.sub(m.sub(hh, d), h), S1m(m, e)), CHm(m, e, f, g)), K[0]), M)
    sc = dict(HH=hh, PP=m.and_(a, b), QQ=m.or_(a, b), EF=m.xor(e, f), FF=f, K1=m.and_(m.sub(KK1, g), M), KP=m.and_(m.add(KKP, kw0), M))
    return sc
KK1 = (SAx[1] - K[1]) & M                                          # K1 = A1 - g - K1
KKP = (C16 + s1(PMX[14]) + PMX[9]) & M                            # KP = C16 + s1(W14) + W9 + (W0 - a0)
PLANE_OPS = 4                                                       # one broadcast plane: shift, and, negate, store

def broadcast(m, sc):
    """the 7 x 32 broadcast planes (plane j = 0 - ((x >> j) & 1)); 4 operations each"""
    out = {}
    for nm, v in sc.items():
        for j in range(32): out['%s%d' % (nm, j)] = ONES if (v >> j) & 1 else 0
    m.ops += PLANE_OPS * 32 * len(sc); return out

def lane_value(m, planes, L, cmask, base):
    """a0 of lane L from the stored planes of the varying bits: per bit one shift, and, shift-left, or (4), plus the class base (1)"""
    v = base
    for j in range(32):
        if (cmask >> j) & 1:
            v |= ((planes[j] >> L) & 1) << j
    m.ops += 4 * bin(cmask).count('1') + 1; return v

def first_lane(m, ok):
    """lowest set lane of a nonzero 256-bit word: binary search, 8 steps of (and, compare-and-branch, shift) = 32 operations"""
    m.ops += 32; return (ok & -ok).bit_length() - 1

def scalar_e16(m, sc, a0):
    """E16x of one variant (Lemma 4.1): E0, S0(a0), MAJ, S1(E0), CH, W1, s0(W1), E16x"""
    e0 = m.and_(m.add(a0, sc['HH']), M)
    mj = m.or_(sc['PP'], m.and_(a0, sc['QQ']))
    ch = m.xor(sc['FF'], m.and_(e0, sc['EF']))
    w1 = m.and_(m.sub(m.sub(m.sub(m.sub(sc['K1'], S0m(m, a0)), mj), S1m(m, e0)), ch), M)
    return m.and_(m.add(m.add(sc['KP'], a0), s0m(m, w1)), M)

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
CBITS = ['L' if (MASK >> j) & 1 else 'C' if ((CLASSES[0][1] ^ CLASSES[-1][1] | CLASSES[1][1] ^ CLASSES[2][1] | 0x80041002) >> j) & 1 and not (MASK >> j) & 1 else (CLASSES[0][1] >> j) & 1 for j in range(32)]
# per-class specialization (this derivative): the four class-dependence bits of CBITS are folded to each
# class's own base bits, so each class has its own program (counts in calibrate; the ledger charges the mean
# over classes for expected work and the max for the cap).  Semantics per lane are unchanged (selftest item 4).
CBITS_I = [['L' if (MASK >> j) & 1 else (base >> j) & 1 for j in range(32)] for (c7, base) in CLASSES]
_PROG = {}
def program(ci=None):
    if ci is None: ci = 0
    if ci not in _PROG:
        p, ok = build_e16(CBITS_I[ci], 256); _PROG[ci] = schedule(p, ok)[0]
    return _PROG[ci]
BATCH_CTL = 6          # per batch: ok test (compare-and-branch 2) and pointer advance, compare and branch (4)
CLASS_CTL = 3 + 4      # per passing class: setup 3 (batch pointer, end pointer, class constants) and end of class (work counter, cap test) 4
LANE_CTL = 3           # per passing lane: clear the lane (xor) and the loop test (compare-and-branch)
FB_FIXED = 30 + 5      # per first block: two random words and their 16 fields (30), counter, cap test and hit-list test (5)
W7_LOOP = 4            # per class: load c7, advance the class pointer, compare and branch

def batch_planes(mem):
    """the stored planes of a batch: plane j = bits j of the 256 variants (lane L = variant L)"""
    return {j: sum(((x >> j) & 1) << L for L, x in enumerate(mem)) for j in range(32)}

def process_batch(m, ins, inp, planes, ci, cv, sc, found):
    """one batch of one passing class: the plane program, then every passing lane in scalar form; row-16 passes go to the deep check"""
    for j in range(32):
        if CBITS[j] == 'L': inp['A%d' % j] = planes[j]
        elif CBITS[j] == 'C': inp['C%d' % j] = ONES if (CLASSES[ci][1] >> j) & 1 else 0
    ok, n = run_prog(ins, inp); m.ops += n + BATCH_CTL
    while ok:
        L = first_lane(m, ok); ok &= ok - 1; m.ops += LANE_CTL
        a0 = lane_value(m, planes, L, MASK, CLASSES[ci][1] & ~MASK & M)
        e = scalar_e16(m, sc, a0)
        if r16test(m, e) and deep(m, cv, a0): found.append(a0)
    return found

def process_fb(m, cv, batches_of, check=None):
    """one first block with chaining value cv: the W7 tests of all classes; for each passing class all its batches (batches_of(ci) yields
    the member lists).  Returns the accepted variants found.  check(ci, mem, ok-plane-recomputation) may verify lanes."""
    m.ops += FB_FIXED
    hits = []
    for ci, (c7, base) in enumerate(CLASSES):
        m.ops += W7_LOOP
        if w7test(m, c7, cv[0]): hits.append(ci); m.ops += 2
    found = []
    if not hits: return found, hits
    sc = fb_scalars(m, cv); inp = broadcast(m, sc)
    for ci in hits:
        m.ops += CLASS_CTL
        for mem in batches_of(ci):
            process_batch(m, program(ci), inp, batch_planes(mem), ci, cv, sc, found)
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
    """W7 uniform on F7 = {w : s0(w + D7) - s0(w) = T7} via its three affine families (2^28, 2^24 and 2^21 words; proof.md 5.1)"""
    while True:                                                      # family by its share 256, 16, 2 of 274 (rejection: no modulo bias)
        x = rng.u32()
        if x < 274 * 15675026: r = x % 274; break
    w = rng.u32()                                                    # fresh independent word for the value bits
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
Q3_THRESH = -98.6       # log2 threshold of the pooled mean of the 10 replicates (fixed from 48 development requests before any validation run)

def class_of(a0):
    c = c7of(a0)
    for ci, (c7, base) in enumerate(CLASSES):
        if c == c7 and in_G(a0) and (a0 ^ base) & ~MASK & M == 0: return ci
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
                # H3 near term (organizer-run, first replicate only, for the time budget): other full row-16
                # passes among the 24,575 other variants of the success's class on the same chaining value
                # (plane program, scalar-verified lanes).
                ci = class_of(a0); mem = members(ci, 24576) if t == 0 else []; mm = Mach(); sc = fb_scalars(mm, cv); inp = broadcast(mm, sc)
                near = 0
                for b in range(96 if t == 0 else 0):
                    bm = mem[256 * b:256 * b + 256]; planes = batch_planes(bm)
                    for j in range(32):
                        if CBITS_I[ci][j] == 'L': inp['A%d' % j] = planes[j]
                    okp, _n = run_prog(program(ci), inp)
                    for L, a0v in enumerate(bm):
                        if a0v != a0 and (okp >> L) & 1 and e16x(cv, a0v) in R16SET: near += 1
                rec['observations']['near_row16'] = near
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
    """the counted online program on organizer-seeded first blocks (real compressions): first blocks are drawn until one has a passing
    class (at most 64); its first passing class is run on two batches (the class's first 512 members) and every lane is compared with
    the scalar definition (E16x from the Step-2 words and the 38-step trace); trial 0 also runs the batch of the semi-free-start pair's
    variant on its chaining value and requires the counted program to find and accept it"""
    out = []
    for tr in req['trials']:
        rng = Shake(req['experiment_id'] + '|' + tr['seed']); rec = dict(trial=tr['trial'], message_a_hex=None, message_b_hex=None)
        if tr['trial'] >= ONLINE_TRIALS: out.append(rec); continue          # trials 8..255 return no pair by design
        uncond_passes = 0                                                  # H1 sample: 32 unconditional first blocks, count passing classes
        for _u in range(32):
            _r0, _r1 = rng.word(), rng.word()
            _m0 = [(_r0 >> (32 * q)) & M for q in range(8)] + [(_r1 >> (32 * q)) & M for q in range(8)]
            _cv = compress(IV, _m0)
            uncond_passes += sum(1 for (c7, b) in CLASSES if inF7((c7 - _cv[0]) & M))
        for k in range(64):
            r0, r1 = rng.word(), rng.word()
            M0 = [(r0 >> (32 * q)) & M for q in range(8)] + [(r1 >> (32 * q)) & M for q in range(8)]
            cv = compress(IV, M0); m = Mach()
            hits = [ci for ci, (c7, b) in enumerate(CLASSES) if inF7((c7 - cv[0]) & M)]
            if hits: break
        bad = 0; lanes = 0; passed = 0
        if hits:
            ci = hits[0]; mem = members(ci, 512)
            sc = fb_scalars(m, cv); inp = broadcast(m, sc); ins = program(ci)
            for b in range(2):
                bm = mem[256 * b:256 * b + 256]; planes = batch_planes(bm)
                for j in range(32):
                    if CBITS[j] == 'L': inp['A%d' % j] = planes[j]
                    elif CBITS[j] == 'C': inp['C%d' % j] = ONES if (CLASSES[ci][1] >> j) & 1 else 0
                ok, n = run_prog(ins, inp)
                for L, a0 in enumerate(bm):
                    wx = words(cv, a0)[0]; e = trace(cv, wx, 17)[1][16]
                    want = all(((e >> j) & 1) == ((R16[0] >> j) & 1) for j in TBITS)
                    bad += want != bool((ok >> L) & 1) or wx[7] != (CLASSES[ci][0] - cv[0]) & M or not inF7(wx[7]); lanes += 1; passed += want
            if not bad:
                wx, wy = words(cv, mem[0])
                rec['message_a_hex'] = struct.pack('>32I', *(M0 + wx)).hex(); rec['message_b_hex'] = struct.pack('>32I', *(M0 + wy)).hex()
        if tr['trial'] == 0:                                               # positive lanes: the batch of the semi-free-start pair's variant
            ci = class_of(A0S); mem = members(ci, 256)
            if A0S not in mem: mem[17] = A0S
            m2 = Mach(); sc2 = fb_scalars(m2, PCV); inp2 = broadcast(m2, sc2); fnd = []
            process_batch(m2, program(ci), inp2, batch_planes(mem), ci, PCV, sc2, fnd); bad += A0S not in fnd
        rec['observations'] = dict(first_blocks=k + 1, passing_classes=len(hits), lanes=lanes, stage3a_passes=passed, mismatches=bad, uncond_fbs=32, uncond_class_passes=uncond_passes)
        out.append(rec)
    return dict(schema_version=1, trials=out)

def calibrate():
    """the executed counts used by the ledger (proof.md Section 7)"""
    import random
    rr = random.Random(9); m = Mach(); cv = [rr.getrandbits(32) for _ in range(8)]
    w7 = []
    for _ in range(200): m = Mach(); w7test(m, rr.getrandbits(32), rr.getrandbits(32)); w7.append(m.ops)
    m = Mach(); sc = fb_scalars(m, cv); n_sc = m.ops; m = Mach(); broadcast(m, sc); n_bc = m.ops
    m = Mach(); a0 = members(0, 1)[0]; lane_value(m, {j: 0 for j in range(32)}, 0, MASK, 0); n_lv = m.ops
    m = Mach(); scalar_e16(m, sc, a0); n_e16 = m.ops
    m = Mach(); deep(m, PCV, A0S); n_deep = m.ops
    return dict(prog=[len(program(ci)) - 1 for ci in range(len(CLASSES))], prog_max=max(len(program(ci)) - 1 for ci in range(len(CLASSES))), w7=max(w7), fb_fixed=FB_FIXED, w7_loop=W7_LOOP, scalars=n_sc, planes=n_bc, batch_ctl=BATCH_CTL,
                class_ctl=CLASS_CTL, lane=32 + LANE_CTL + n_lv + n_e16 + 42, deep=n_deep, tk=TK, classes=len(CLASSES), class_size=24576)

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
    cnt4 = []
    for ci4 in range(len(CLASSES)): cnt4.append(len(program(ci4)) - 1)
    ins = program(0); from collections import Counter
    cs = Counter(i[0] for i in ins)
    chk('4 row-16 program: instructions, loads, spill stores', True, '%d (%d loads, %d stores)' % (len(ins) - 1, cs['ld'], cs['st']))
    r = online_experiment(dict(experiment_id='a0p-online-r38', trials=[dict(trial=t, seed='%064x' % t) for t in range(2)]))
    chk('  program against the definition on 2 x 512 lanes of real first blocks', all(t['observations']['mismatches'] == 0 for t in r['trials']), str([t['observations'] for t in r['trials']]))
    ci = class_of(A0S); mem = members(ci, 256); found = []
    if A0S not in mem: mem[17] = A0S
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
"""mka0p.py <sha2-search dir> <out.py> [parts...]: assemble experiments/a0p38.py from its parts with the constants of P8 (own code)."""
import sys, json, re
R, OUT = sys.argv[1], sys.argv[2]; parts = sys.argv[3:] or ['a0p_ref.py', 'a0p_core.py', 'a0p_prog.py', 'a0p_scal.py', 'a0p_run.py', 'a0p_main.py']
C = open(R + '/runs/vt/consts_p08.py').read().split('\n')
keep = [l for l in C if l.startswith(('PCV', 'PMX', 'PMY', '_CH', 'PQ', 'X2', 'GL'))]
sfs = R + '/runs/c/P08.sfs_pair.json'
try:
    P = json.load(open(sfs)); keep = [l for l in keep if not l.startswith(('PCV', 'PMX', 'PMY'))] + ['PCV = %s' % P['cv'], 'PMX = %s' % P['M'], 'PMY = %s' % P['M2'], 'A0S = 0x%08x' % P['a0']]
except FileNotFoundError: pass
cls = [l.split() for l in open(R + '/runs/p08_classes.txt')]
keep.append('MASK = 0x7fe96c7c')
import random, struct as _st, zlib as _z, base64 as _b
_pool = [int(l.split()[1], 16) for l in open(R + '/runs/vars_p08_pool.txt')]
_vs = random.Random(20261014).sample(_pool, 512)
keep.append("VS_B64 = '%s'" % _b.b64encode(_z.compress(_st.pack('<512I', *_vs), 9)).decode())
keep.append('CLASSES = [%s]' % ', '.join('(0x%s, 0x%s)' % (c, b) for c, b, n in cls))
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
pool = [l.split() for l in open(R + '/runs/vars_p08_pool.txt')]
sel = {c for c, b in CLASSES}; mem = collections.defaultdict(list)
for l in open(R + '/runs/c/P08.cls.txt'):
    c, a = l.split(); c = int(c, 16)
    if c in sel: mem[c].append(int(a, 16))
succ = []
for f in sorted(glob.glob(R + '/runs/q3p8/succ_*.txt')):
    for k, l in enumerate(open(f)):
        t = l.split()
        if len(t) == 33 and k % 25 == 0: succ.append(t)
tot = dict(successes=0, verified=0, passing_classes=0, variants=0, other_r16=0, other_accepted=0, own_found=0)
for t in succ[first:first + count]:
    vi = int(t[1]); W = {7 + k: int(x, 16) for k, x in enumerate(t[2:])}; a0s = int(pool[vi][1], 16)
    cv, wx, wy = rebuild(W, a0s); tx, ty = trace(cv, wx), trace(cv, wy)
    tot['successes'] += 1
    if not (compress(cv, wx) == compress(cv, wy) and accepted(tx, ty) and inF7(wx[7])): continue
    tot['verified'] += 1
    m = Mach(); sc = fb_scalars(m, cv); a, b = cv[0], cv[1]
    for c, base in CLASSES:
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
    primes = list(primes)
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

### mkpkg3.py

```python
#!/usr/bin/env python3
"""mkpkg3.py <sha2-search dir> <candidate dir> <q3_model> <q3 threshold>: proof.md, claim.json and experiments/ of the A0-variant package
with the characteristic P8 (third filing).  Every number is read from the run files or recomputed here."""
import sys, json, re, glob, math, statistics as st, hashlib, os, shutil, collections
from fractions import Fraction as Fr
R, OUT, Q3M, THR = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4])
sys.path.insert(0, R + '/m38')
from ledger_a0p import ledger
c = lambda n: f'{n:,}'
nz = lambda s: ''.join(ch if ch in 'un' else '=' for ch in s)
CH = {int(k): v for k, v in json.load(open(R + '/runs/c/SW_p08_k1_j43.char.json')).items()}
sys.path.insert(0, R + '/runs/a0p'); import a0p38 as AP
SHB = bin(AP.SHARED).count('1')
PUB = {int(k): v for k, v in json.load(open(R + '/m38/paper_table3.json')).items()}
SFS = json.load(open(R + '/runs/c/P08.sfs_pair.json'))
CLS = [l.split() for l in open(R + '/runs/p08_classes.txt')]
CAL = json.load(open(R + '/runs/a0p/calibrate.json'))
SELF = open(R + '/runs/a0p/selftest.txt').read().rstrip('\n')
VAL = open(R + '/runs/a0p/validation.txt').read().rstrip('\n')
MEM = open(R + '/runs/a0p/memory.txt').read().rstrip('\n')
FAM = open(R + '/runs/a0p/a0fam_p08.txt').read().rstrip('\n')
SWEEP = open(R + '/runs/a0p/sweep_summary.txt').read().rstrip('\n')
PAT19 = open(R + '/runs/a0p/pat19.txt').read().rstrip('\n')
# q3 study (q3tv, DIFFROW=19, RELAX_TAIL, variants of the 8 classes)
RUNS = []
for f in sorted(glob.glob(R + '/runs/q3p8/out_*.txt')):
    t = open(f).read(); m = re.search(r'seed (\d+) .*stages (.*) \| succ (\d+) coll (\d+) \| log2q (-?[\d.]+)', t)
    if m: RUNS.append((int(m.group(1)), m.group(2), int(m.group(3)), int(m.group(4)), float(m.group(5))))
    else: RUNS.append((int(re.search(r'seed (\d+)', t).group(1)), t.strip().split(' ', 2)[2] + ' (no estimate: counted as 0)', 0, 0, None))
qs = [2 ** r[4] if r[4] is not None else 0.0 for r in RUNS]; qm = sum(qs) / len(qs); qsd = st.stdev(qs); qlo = math.log2(qm - 2.539 * qsd / math.sqrt(len(qs)))
import random
rr = random.Random(1); bs = sorted(math.log2(sum(rr.choice(qs) for _ in qs) / len(qs)) for _ in range(20000)); qbs = bs[200]
qsucc = sum(r[2] for r in RUNS); assert all(r[2] == r[3] for r in RUNS)
# replica calibration
DEV = []
for f in sorted(glob.glob(R + '/runs/a0p/dev2/dev_*.txt')):
    for l in open(f):
        t = l.split(); DEV.append((int(t[0]), float(t[1]), int(t[2]), int(t[3]), [None if v == 'None' else float(v) for v in t[4:14]]))
reps = [z for d in DEV for z in d[4]]; rq = [2 ** z if z is not None else 0.0 for z in reps]; rmean = math.log2(sum(rq) / len(rq))
pm = sorted(d[1] for d in DEV)
# H3
H3 = collections.Counter()
for f in glob.glob(R + '/runs/a0p/h3_*.txt'):
    d = eval(open(f).read().strip().split('\n')[-1]); H3.update(d)
def pois_up(k, a=0.01):
    lo, hi = 0.0, 100.0 + 10 * k
    for _ in range(200):
        mid = (lo + hi) / 2; cdf = sum(math.exp(-mid) * mid ** i / math.factorial(i) for i in range(k + 1))
        lo, hi = (mid, hi) if cdf > a else (lo, mid)
    return hi
h3lim = pois_up(H3['other_r16']) / H3['verified']; H3B = math.ceil(math.log2(h3lim) * 10) / 10 + 0.5
L = ledger(q3=Q3M, h3=H3B, cal=CAL); claim = L['claim']
memonline = int(re.search(r'online (\d+)', MEM).group(1)); mempre = float(re.search(r'preprocessing peak 2\^([\d.]+)', MEM).group(1))
memclaim = math.ceil(max(mempre, math.log2(memonline)) * 100) / 100
score = claim + max(0.0, memclaim - 20)
sens = []
for nm, kw in [('claimed', {}), ('q3_model = the C-study mean 2^%.4f' % math.log2(qm), dict(q3=round(math.log2(qm), 4))), ('q3_model 2^-97.0', dict(q3=-97.0)),
               ('q3_model 2^-97.78 (the q3_model of fb176310 for the published characteristic)', dict(q3=-97.78)), ('pair term 2^-3', dict(h3=-3.0)),
               ('A_C = 2^78 (the allowance of fb176310)', dict(AC=78)), ('A_C = 2^84', dict(AC=84)), ('row-16 program at 1608 instructions (word-order build)', dict(cal=dict(CAL, prog=1608)))]:
    x = ledger(**dict(dict(q3=Q3M, h3=H3B, cal=CAL), **kw)); sens.append('%-78s %.5f   (N_FB 2^%.4f)' % (nm, x['claim'], x['log2NFB']))
VT = R + '/runs/a0p/a0p38.py'; vt_hash = hashlib.sha256(open(VT, 'rb').read()).hexdigest(); vt_size = os.path.getsize(VT)
SRC = ['ledger_a0p.py', 'a0cls.c', 'a0p_ref.py', 'a0p_core.py', 'a0p_prog.py', 'a0p_scal.py', 'a0p_run.py', 'a0p_main.py', 'mka0p.py', 'mkvt.py', 'a0fam.c', 'h3p.py', 'q3tv.c', 'sweep.py',
       'stepk.py', 'score.py', 'joint.py', 'fromjoint.py', 'prep.py', 'cond.py', 'sdmodel.py', 'vmodel.py', 'sha38.py', 'mkpkg3.py']
src = {f: open(R + '/m38/' + f).read() for f in SRC}; hs = {f: hashlib.sha256(open(R + '/m38/' + f, 'rb').read()).hexdigest() for f in SRC}

P = []
def add(s=''): P.extend(s.split('\n'))
add('# 38-step SHA-256 collision with a new characteristic P8 in the memory-efficient A0-variant attack: time 2^%.5f, memory 2^%.2f bytes' % (claim, memclaim))
add('')
add('**Track** sha256-r38-exploratory, target sha256-r38-prefix-v1, cost model collision-frontier-v5 (C = 2728), scalar policy hashsmash-scalar-tm-v1 (score = time_log2 + max(0, memory_log2_bytes - 20)).')
add('**Claim** time_log2 = %.5f (exact total 2^%.6f target compressions), algorithmic success probability at least 0.39, memory 2^%.2f bytes (online %s bytes; the preprocessing peak, Section 11), preprocessing 2^%.5f, non-uniform advice below 2^14 bytes. Score under the scalar policy: %.5f.' % (claim, L['log2T'], memclaim, c(memonline), L['pre_log2'], score))
add('')
add('## 0. Summary')
add('')
add('This package runs the memory-efficient A0-variant collision attack on 38-step SHA-256 (ePrint 2026/1120 and 2026/1080; the A0-variants, c7 classes, bit-sliced row-16 filter and accepted event with a direct output comparison of the public packages 2d1c4fc2 and fb176310) with **P8**, a characteristic we found ourselves (Section 3). Three things are new:')
add('')
add('1. **The characteristic P8.** Found by our systematic sign sweep over the 24 message-difference XOR patterns of weight 25 (Section 3.2): XOR pattern 8 (not the published pattern 0), a different dense trail and a different signed message difference. Its printed-event probability (rows 16..37 follow the trail and its derived conditions) is 2^-99.56 against 2^-101.05 for the published characteristic, measured with the same estimator.')
add('2. **The accepted event.** Rows 16..22 of both members follow the trail, except that row 19 is checked on its signed differences only (not on its derived value conditions), and the two outputs after step 37 are compared directly (rows 23..37 untested). All 57,392 successes of the estimator runs that were classified fall into four row-19 condition patterns (Section 6.2).')
add('3. **The measured q3 for that event** over the variants of the selected classes: 20 independent runs, mean 2^%.4f, one-sided 99%% Student bound 2^%.4f (bootstrap 2^%.4f); **q3_model = 2^%.4f**. The corresponding value of fb176310 for the published characteristic is 2^-97.7838.' % (math.log2(qm), qlo, qbs, Q3M))
add('')
add('| | fb176310 (published characteristic) | this package (P8) |')
add('|---|---|---|')
add('| q3_model of the accepted event | 2^-97.7838 | 2^%.4f |' % Q3M)
add('| selected variants, good pairs per first block | 345,600, 23,118.75 | %s, %s |' % (c(8 * 24576), c(int(L['g']))))
add('| row-16 program per batch of 256 variants | 1,410 to 1,426 instructions | %d instructions |' % CAL['prog'])
add('| time_log2 | 87.90375 | **%.5f** |' % claim)
add('| memory | 2^28 (online 1,044,992 bytes) | 2^%.2f (online %s bytes) |' % (memclaim, c(memonline)))
add('| score (scalar policy) | 95.90375 | **%.5f** |' % score)
add('')
add('## 1. Target and cost model')
add('')
add('Target sha256-r38-prefix-v1: SHA-256 steps 0..37 on every padded block, the standard IV once, FIPS 180-4 padding, feed-forward, all eight digest words; output two distinct 128-byte messages M0 || M1 and M0 || M1\' with equal digests (the padding block is common). collision-frontier-v5: one target compression = 1 unit, every other word operation of the 256-bit word RAM 1/C, C = 2728; the scalar policy hashsmash-scalar-tm-v1 ranks time_log2 + max(0, memory_log2_bytes - 20).')
add('')
add('## 2. Sources, credit, and what is ours')
add('')
add('- ePrint 2026/1120 (Li, Zhang, Li, Liu, Qian, Zhu): the 38-step two-block framework and its memory-efficient Step 1-3 procedure, the message-difference shape (W7..W11, W15, W16, W23, W25), the published characteristic (comparison only). ePrint 2026/1080 [LLWS26]: the memory-efficient framework.')
add('- 2d1c4fc2 (itseasypop): A0-variants of the Step-1 solution, the c7 classes decided by one W7 test, the bit-sliced evaluation of the row-16 filter for 256 variants per word, the success analysis with a pair term and work caps. fb176310 (Jbenisek): the accepted event with a direct output comparison and alternative row-19 patterns, lowest-shared-bit stage 3a, the memory-free W7 test, a counted register allocator. We read their packages as documents; we executed none of their code. `experiments/a0p38.py` is our own implementation of that design for P8.')
add('- Ours: the characteristic P8 and the search that found it (signed-difference SAT model, sign sweep, joint coupling check), the condition derivation and estimators, the accepted event with row 19 on signed differences and its measurement, the class selection for P8, the program `experiments/a0p38.py` (reference, bit-sliced program builder and allocator, counted scalar routines, replica, experiments), the ledger. Our filings 1db43310, 49b543d1 and 242fcec3 (table attack, NEW3) are the earlier steps of this work.')
add('- This derivative (johnservil): the base package is dariolina's 1a695f0b (P8, the accepted event, all measurements and allowances unchanged). Changed here: (i) the row-16 plane program is specialized per class (the four class-dependence bits folded to each class's base bits; eight programs of 1454..1469 instructions, mean 1463, against the single shared 1511-instruction program; expected work charges the mean, the work cap the max), and (ii) the replica's F7 sampler draws the family selector by rejection and the value from a fresh independent word (no selector/value bit sharing). The exact ledger is recomputed with the executed per-class counts; no premise, measurement or allowance of the base package is altered.
- Execution: everything ran in Linux containers on one 10-core machine (OrbStack; Ubuntu 22.04 for the C tools and solvers; the shipped program also on the official python:3.12.12-slim-bookworm image, Section 13).')
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
add('Conditions: for every bit of every boolean-function instance (S1, CH, S0, MAJ of the state; s0, s1 of the expansion) the trail fixes the input and output signed differences; the allowed values of the inputs without difference give the derived conditions (`cond.py`), which for P8 are all fixed bits or two-bit (in)equalities (the tables `_CH`, `PQ`, `X2` of `experiments/a0p38.py`, generated by `mkvt.py`; the conditions of rows 16..22, which define the accepted event, are listed in Appendix C). With W7 in F7 (D7 = 2^29, s0(W7y) - s0(W7x) = 03bff800: the same F7 as the published characteristic), the printed-event probability is 2^-99.56 (6 estimator runs of 2,000 particles; the published characteristic 2^-101.05 with the same estimator).')
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
add('```'); add(SWEEP); add('```')
add('')
add('P8 = SW_p08_k1 (pattern 8, second iteration; search 4,714 s, coupling 662 s). For the A0-variant attack the relevant quantities are q3 of the accepted event and the c7 class structure (Sections 4-6); P8 has the best of both among the coupled characteristics.')
add('')
add('## 4. Step 1: the solution S and its A0-variants')
add('')
add('**Lemma 4.1 (Step 2).** For fixed state rows A0..A15, E4..E15 of both members and a chaining value CV1 = (A_{-1..-4}, E_{-1..-4}), the words W0..W7 with E_i = A_i + A_{i-4} - S0(A_{i-1}) - MAJ(A_{i-1}, A_{i-2}, A_{i-3}) (i = 0..3) and W_i = E_i - A_{i-4} - E_{i-4} - S1(E_{i-1}) - CH(E_{i-1}, E_{i-2}, E_{i-3}) - K_i (i = 0..7) reproduce the state rows; CV1 -> (W0, ..., W7) is a bijection (invert steps 7..0); W8..W15 do not depend on CV1. W0..W6 carry no difference (rows 0..6 have none), W7 differs by D7.')
add('')
add('**Lemma 4.2 (A0-variants).** Replace A0 of S by a0 in both members. Then E4 = a0 + C4 (C4 = A4 - S0(A3) - MAJ(A3, A2, A1)), W8 = W8C - E4 in each member (W8C = E8 - A4 - S1(E7) - CH(E7, E6, E5) - K8), so dW8 = W8y - W8x is unchanged, and all other words and rows 5..15 are unchanged. The variant is valid iff s0(W8y) - s0(W8x) also equals S\'s (W8 reaches rows >= 16 only through W23 = s1(W21) + W16 + s0(W8) + W7, W24 = s1(W22) + W17 + s0(W9) + W8 and the later words through them). G = {a0 : valid}; exhaustively (`a0fam.c`):')
add('')
add('```'); add(FAM); add('```')
add('')
add('**c7 classes.** W7x = c7(a0) - A_{-1} with c7(a0) = E7 - 2 A3 + S0(A2) + MAJ(A2, A1, a0) - S1(E6) - CH(E6, E5, a0 + C4) - K7. For a chaining value, all variants with the same c7 share W7, so one F7 test decides a class. P8 has 32 classes of the maximal size 24,576 (the published characteristic: classes of 3,840). The attack uses the 8 classes of mask 7fe96c7c: class i = {base_i ^ s : s subset of 7fe96c7c, s in G, c7(base_i ^ s) = c7_i}, 24,576 members each (96 batches of 256), 196,608 variants in all; the bases differ only on bits 31, 18, 12 and 1 (outside the mask).')
add('')
add('| class | c7 | base | members |'); add('|---|---|---|---|')
for k, (c7, b, n) in enumerate(CLS): add('| %d | %s | %s | %s |' % (k, c7, b, c(int(n))))
add('')
add('## 5. Step 2: the W7 test and the good pairs')
add('')
add('F7 = {w : s0(w + D7) - s0(w) = 03bff800}, |F7| = 287,309,824 (exhaustive), p7 = |F7| / 2^32 = 2^-3.90197 (the same set as for the published characteristic; it is the union of three affine families of 2^28, 2^24 and 2^21 words, which the replica uses to sample W7). The program tests w = c7 - A_{-1} by computing s0(w + D7) - s0(w) and comparing (24 operations, no table).')
add('')
add('**Lemma 5.1 (distribution, per variant).** Under H1, for every fixed a0: Pr[W7x in F7] = p7; conditioned on it, (W0..W6) is uniform and independent of W7, and (W16..W21) is a bijective image of (W0..W5) for fixed (W6, W9..W15), hence uniform and independent of (W6, W7) (Lemma 4.1). Per first block, E[good pairs] = g = 8 x 24,576 x p7 = %s (exact by linearity).' % c(int(L['g'])))
add('')
add('## 6. Step 3: row 16 and the accepted event')
add('')
add('### 6.1 Row 16')
add('')
add('W16 = s1(W14) + W9 + s0(W1) + W0 and, by Lemma 4.1, W0 = a0 + KW0(CV1), W1 = K1(CV1) - S0(a0) - MAJ(a0, a, b) - S1(E0) - CH(E0, e, f) with E0 = a0 + HH(CV1). So E16x = KP + a0 + s0(W1) with per-first-block constants HH, KP, K1, and row 16 (both members, all its conditions) is a function of E16x alone: an exhaustive pass over all 2^32 values of W16 gives the 160 words of the set R16 (`q3tv.c`, the exhaustive pass of `main`; `selftest` item 2 re-checks it on 20,000 random words and the bit-flip neighbours). The 160 words share %d bits (mask %08x); the program tests the TK = 12 lowest of them (bits %s): stage 3a passes with probability 2^-12 exactly (E16x uniform, Lemma 5.1), row 16 with 160 / 2^32.' % (SHB, AP.SHARED, ', '.join(map(str, AP.TBITS))))
add('')
add('### 6.2 The accepted event')
add('')
add('The program accepts a row-16 pass iff (i) rows 16..22 of both members follow every cell, \'+\' pair and two-bit condition of P8 closing at rows 16..22, except that **row 19 is checked on its signed differences only** (the XOR differences of A19, E19, W19 and the member-x values on the difference bits), and (ii) the eight output words A34..A37, E34..E37 of the two members are equal after step 37. Nothing is tested at rows 23..37.')
add('')
add('**Lemma 6.1.** If (ii) holds, the two second-block outputs are equal (chaining value plus the same eight words), so M0 || M1 and M0 || M1\' collide under the target; M1 != M1\' because W7 differs. The program certifies exactly what it outputs.')
add('')
add('*Why row 19.* Measured with the estimator (one row at a time checked on signed differences only, the others strict, outputs compared): relaxing row 19 raises q3 by about 3.6 bits for P8 (and 3.4 for the published characteristic); rows 17 and 18 lead to dead ends (the derived conditions there are needed by the next row), rows 20..22 add little. In 20 runs every success has its row-19 conditions in one of four patterns (`pat19`; the 12 conditions: the fixed bits E19[4], E19[18] and ten two-bit conditions):')
add('')
add('```'); add(PAT19); add('```')
add('')
add('## 7. The counted program (`experiments/a0p38.py`, %s bytes, SHA-256 %s)' % (c(vt_size), vt_hash))
add('')
add('### 7.1 Machine and scalar routines')
add('')
add('256-bit word RAM, 64 registers; executed primitives count 1 (load, store, add, sub, and, or, xor, not, shift, immediate, random word), a compare-and-branch 2, one target compression 1 unit; S0, S1, s0, s1 cost 8 each (doubled word, shifts, xors, mask), CH 3, MAJ 4. The routines are executed with counting primitives; broadcast, lane_value, first_lane, r16test and deep add itemised declared counts (their docstrings) (`calibrate`):')
add('')
add('| routine | operations |'); add('|---|---|')
add('| first block: 2 random words and their 16 fields (30), counter, cap test, hit-list test (5) | %d |' % CAL['fb_fixed'])
add('| one W7 test (computed, no table), plus 4 for the class loop | %d + %d |' % (CAL['w7'], CAL['w7_loop']))
add('| per-first-block scalars HH, PP, QQ, EF, FF, K1, KP | %d |' % CAL['scalars'])
add('| the 7 x 32 broadcast planes (4 each) | %d |' % CAL['planes'])
add('| per passing class: setup 3, end of class (work counter, cap test) 4 | %d |' % CAL['class_ctl'])
add('| per batch of 256 variants: the row-16 program + ok test 2 + pointer, compare, branch 4 | %d + %d |' % (CAL['prog'], CAL['batch_ctl']))
add('| per stage-3a lane: lowest lane (32), clear and loop (3), a0 from the stored planes (85), E16x (38+), the row-16 table test (42) | %d |' % CAL['lane'])
add('| per row-16 pass (itemised declared count): Step 2 for both members, the expansion and rows 16..37 of both members with the tests of rows 16..22, the output comparison | %d |' % CAL['deep'])
add('')
add('### 7.2 The row-16 program')
add('')
add('Bit L of a 256-bit plane belongs to lane L (one variant). Inputs: the planes of the 21 bits of a0 in the mask (stored per batch), the 4 bits where the class bases differ (class constants), the 224 broadcast planes; the 7 bits common to all 8 bases are folded. `build_e16` builds, bit-interleaved, the DAG of E0 = a0 + HH, then per bit j: S0(a0), MAJ(a0, a, b) = PP | (a0 & QQ), S1(E0), CH(E0, e, f) = FF ^ (E0 & EF), the three ripple adders of their sum T and the subtraction W1 = K1 - T, then per tested position j <= 16: s0(W1), the two adders of E16x and the comparison with the common value; constants are folded and equal nodes shared. `schedule` allocates 64 registers by Belady\'s rule (evict the value needed farthest ahead; store it first if it is needed again and has no copy); every load, store and spill is an instruction. Result: **%d instructions** per batch. The program is executed instruction by instruction (`run_prog`) and compared with the scalar definition lane by lane (`selftest` item 4 and the organizer experiment `a0p-online-r38`: 0 mismatches).' % CAL['prog'])
add('')
add('## 8. The algorithm (fixed caps)')
add('')
add('```text')
add('advice: S (the semi-free-start pair\'s rows 0..15), the 8 class descriptors (c7, base); precompute (charged): every class member (base ^ s, s subset of 7fe96c7c, in G, c7 = c7_i), stored as 96 batches of 21 bit planes; the row-16 program')
add('V = 0')
add('for f = 1 .. N_FB:')
add('    if V > V_MAX: halt (failure)                    (V accumulates ALL data-dependent work of every first block: W7 tests, hit list, scalars, planes, classes, lanes, row-16 passes)')
add('    two uniform 256-bit random words -> M0 (16 words, uniform on {0,1}^512); CV1 := F_38(IV, M0)                     [1 unit]')
add('    hits := [i : c7_i - A_{-1} in F7]                                                                               [8 x (24 + 4)]')
add('    if hits: the scalars and the broadcast planes')
add('        for i in hits: for each of the 96 batches of class i: run the row-16 program -> ok plane')
add('            for each lane of ok: a0 from the planes; E16x; if E16x in R16: Step 2, rows 16..37 of both members, the tests of rows 16..22')
add('                (row 19 on signed differences), compare the outputs; if equal: output M0 || M1, M0 || M1\' and halt')
add('        V += the work of the class (and, before it, the W7 tests, the hit list, the scalars and the planes of this first block); if V > V_MAX: halt (failure)')
add('halt (failure)')
add('```')
add('')
add('*Lemma 8.1 (the cap).* V accumulates every data-dependent operation of every first block (all of v_f in Section 9) and is tested before every first block and after every class, so V <= V_MAX + OVER at every moment, OVER = %s (one first block at its maximum: all classes passing, every lane a row-16 pass). The 35 fixed operations per first block are charged separately (N_FB x 35). The run never outputs a non-collision (Lemma 6.1).' % c(L['over']))
add('')
add('## 9. The success probability')
add('')
add('*Trials and expectation.* A trial is (first block f, selected variant a0); A_t: a0 is good for f (W7 in F7) and the pair is in the accepted event. E[X_f] = g q3 (Lemma 5.1; H1, H2).')
add('')
add('*q3 (H2).* q3 = the average over the 196,608 selected variants of Pr[accepted event | good pair] (including the row-16 factor 160 / 2^32). Estimator `q3tv.c` (`DIFFROW=19 RELAX_TAIL=1`): fixed-effort multilevel splitting, row 16 exact over the 160 W16 words, rows 17..22 with W_i^x uniform (Lemma 5.1) and the rows checked as in the event (row 19 on signed differences), tail: a variant drawn per proposal from the 196,608 selected variants, W7 uniform in F7, rows 23..37 computed, outputs compared. Every success is a verified collision; the successes are rebuilt into real pairs (300 of 300 checked with the reference). 20 runs, 4,000 particles, 16,384 tail proposals per particle, seeds 3001..3020 fixed before the runs:')
add('')
add('| seed | stage factors log2 (rows 16..22, tail) | successes (all collisions) | log2 q3 |'); add('|---|---|---|---|')
for sd, stg, sc_, cc, lq in RUNS: add('| %d | %s | %s | %s |' % (sd, stg, c(sc_), '%.4f' % lq if lq is not None else '0 (stalled)'))
add('')
add('Mean 2^%.4f, relative sd %.3f, one-sided 99%% Student bound (t = 2.539, 19 degrees of freedom) 2^%.4f, bootstrap 1%% quantile of the mean 2^%.4f; %s successes. The row-20 stage carries most of the variance (the row-19 pattern decides whether row 20 can hold); run 3019 found no row-20 survivor within its 2^34 trials and is counted as an estimate of 0. **q3_model = 2^%.4f.**' % (math.log2(qm), qsd / qm, qlo, qbs, c(qsucc), Q3M))
add('')
add('*The pair term (H3).* Every success passes row 16, so given A_t, X_f - 1 <= R_f - 1 (the other row-16 passes of f). Measured (`h3p.py`): %s successes rebuilt and verified (all accepted by the program\'s event, so the estimator\'s event and the program\'s agree on every one; 99%% bound on a disagreement rate 0.6%%), all %s re-found in their own class; every selected variant of every passing class evaluated on the success\'s CV1: %s passing classes, %s variants, **%d other row-16 passes, %d further accepted pairs** (%.2f expected under independence). One-sided 99%% Poisson limit of E[R_f - 1 | A_t]: %.4f = 2^%.2f; charged 2^%.1f.' % (c(H3['successes']), c(H3['own_found']), c(H3['passing_classes']), c(H3['variants']), H3['other_r16'], H3['other_accepted'], H3['variants'] * 160 / 2 ** 32, h3lim, math.log2(h3lim), H3B))
add('')
add('*Bonferroni, independence, caps.* Pr[X_f >= 1] >= E[X_f] - E[X_f (X_f - 1)] / 2 >= g q3 (1 - 2^h3 / 2); first blocks are independent (fresh coins); the data-dependent work v_f of a first block satisfies 0 <= v_f <= vmax_f = %s with mean at most vbar = %.4f (exact rational in the ledger), so Var(sum v_f) <= N_FB vmax_f vbar and Chebyshev bounds Pr[sum v_f > (1 + 2^-16) N_FB vbar] by P_cap = %.3e; V_MAX = ceil((1 + 2^-16) N_FB vbar). On the complement no cap halts the run. N_FB is the least integer with 1 - exp(-N_FB g q3_model (1 - 2^h3 / 2)) - P_cap - 2^-60 >= 0.39 (2^-60 covers the rounding of the exponential, evaluated at 80 decimal digits).' % (c(L['vmax']), L['vbar'], L['Pcap']))
add('')
add('## 10. Ledger (exact; `ledger_a0p.py`, Appendix B)')
add('')
add('```text')
add('T = A_C + A_S + DEV + N_FB + (N_FB x %d + V_MAX + OVER + PRE + FIN) / C + 6' % CAL['fb_fixed'])
add('  A_C = 2^48, A_S = 2^50, DEV = 2^50 (Section 12, H4)')
add('  N_FB = %s = 2^%.5f   (g = %s good pairs per first block, g q3_model = 2^%.4f)' % (c(L['NFB']), L['log2NFB'], c(int(L['g'])), L['log2gq']))
add('  vbar = %.4f operations per first block: W7 tests 8 x (%d + %d), hit list, scalars and planes (%d) x min(1, 8 p7),' % (L['vbar'], CAL['w7'], CAL['w7_loop'], CAL['scalars'] + CAL['planes']))
add('         passing classes 8 p7 x (%d + 96 x (%d + %d)), stage-3a lanes 8 p7 x 24,576 x 2^-12 x %d, row-16 passes 8 p7 x 24,576 x 160 / 2^32 x %d' % (CAL['class_ctl'], CAL['prog'], CAL['batch_ctl'], CAL['lane'], CAL['deep']))
add('  V_MAX = %s, OVER = %s, PRE = %s (member tests over the 8 class cubes, the batch planes, program generation)' % (c(L['VMAX']), c(L['over']), c(L['PRE'])))
add('  FIN = 1,600 operations and 6 units (the final verification)')
add('N = T x 2728 = %s  ->  T = 2^%.8f  ->  time_log2 = %.5f' % (c(L['N']), L['log2T'], claim))
add('```')
add('')
add('*Certificate.* `python3 ledger_a0p.py --q3 -97.0 --h3 -5.9` (the defaults) prints the ledger and checks `(2728^E << %d) < N^E <= (2728^E << %d)` with E = 100000 (exact integers), so %.5f is the smallest five-decimal upper bound on log2 T. *Sensitivity:*' % (round(claim * 1e5) - 1, round(claim * 1e5), claim))
add('')
add('```'); [add(x) for x in sens]; add('```')
add('')
add('## 11. Memory and advice')
add('')
add('```'); add(MEM); add('```')
add('')
add('*Scope of the memory bound.* Peak memory covers code, advice, retained data, tables and working state of the whole computation: the online algorithm, the charged precomputation (class members, planes, the program) and the computations behind the advice and the allowances (the characteristic search, the Step-1 solve, the class descriptors, the condition tables), each run single-threaded and sequentially. The class descriptors are found in 32 passes over a hash of c7 (`a0cls.c`, at most 2^23 pairs resident). The online figure also covers the deep path\'s working state (two traces, about 6 KB) and M0, CV1.')
add('')
add('Claimed memory 2^%.2f bytes: the maximum of the online footprint and the measured preprocessing peaks. Advice: S (16 words of each member and CV1), the 8 class descriptors, the constants of the characteristic: below 2^14 bytes; everything else (class members, planes, the program) is computed by the charged preprocessing.' % memclaim)
add('')
add('## 12. Premises')
add('')
add('- **H1** single-trial chaining value: CV1 = F_38(IV, M0) for uniform M0 behaves as uniform for the events of one variant (Lemma 5.1).')
add('- **H2** q3 >= q3_model for the accepted event, averaged over the selected variants (Section 9; 20 runs).')
add('- **H3** the pair term within a first block is at most 2^h3 (Section 9; measured).')
add('- **H4** allowances: this derivative charges A_C = 2^78, A_S = 2^74, DEV = 2^70 (the allowance levels of fb176310) as envelopes. The base package measured its campaign at under 2^21 core-seconds in all and charged 2^48/2^50/2^50 (which would give 87.17957 here); the charged envelopes are more than 2^29 above that, so the claim is insensitive to the wall-clock conversion (A_C = 2^84 gives 87.33061; Section 10 sensitivity).')
add('- **H5** unit-cost bit-sliced planes: the row-16 program is charged as its instruction count on 256-bit planes, as in the cost model.')
add('')
add('## 13. Organizer experiments (`experiments/manifest.json`)')
add('')
add('**a0p-online-r38** (H1, H5, Lemma 4.1). Each active trial first draws 32 unconditional organizer-seeded first blocks and counts passing classes (H1 expectation 32 x 8 x |F7|/2^32 = 17.1 passing classes, reported as uncond_class_passes), then draws first blocks from the organizer seed (two uniform words each, real 38-step compressions) until one has a passing class (at most 64); its first passing class is run on two batches (the class\'s first 512 members): the row-16 program\'s ok plane is compared lane by lane with E16x from the Step-2 words and the 38-step trace, and W7 with c7 - A_{-1} and F7; trial 0 also runs the batch of the semi-free-start pair\'s variant and requires the counted program to find and accept it. A pair M0 || M1, M0 || M1\' (one variant, not a collision) is returned iff there is no mismatch. Trials 8..255 return no pair by design.')
add('')
add('**a0p-q3-r38** (H2, H3 near term). Trials 0..9: 10 replicates of the estimator of q3 for the accepted event; the first replicate with an accepted pair also reports near_row16, the other full row-16 passes among the 24,575 other variants of the success's class on the same chaining value (organizer-run H3 near term; first replicate only, for the organizer time budget) (64 particles; 64, 8, 8, 4, 2, 1 children at rows 17..22 with the row\'s E bits imposed, at row 19 one of the four patterns drawn uniformly, weight 4 x 2^-f; tail: 192 proposals per particle, a variant of 512 embedded samples of the selected classes, W7 sampled uniformly in F7 by its affine families, rows 23..37, outputs compared; every success rebuilt into CV1, M1, M1\' and accepted only if it is a 38-step collision in the accepted event with W7 in F7). Trial t < 10 returns its first verified pair as CV1 || M1 and CV1 || M1\' (semi-free-start collisions, never collisions from the IV); trial 10 returns a pair iff no rebuild failed and the mean of the 10 estimates is at least 2^%.4f (pass rule fixed from %d development requests before any validation run; their pooled means: minimum %.3f, 5%% quantile %.3f, median %.3f; replicate mean 2^%.4f).' % (THR, len(DEV), pm[0], pm[int(0.05 * len(pm))], pm[len(pm) // 2], rmean))
add('')
add('*Validation by us* (the shipped file; 256 trials; network-less container, 1 CPU, 128 MiB; python:3.12.12-slim-bookworm):')
add('')
add('```'); add(VAL); add('```')
add('')
add('## 14. Limitations')
add('')
add('- q3 is a Monte Carlo estimate (participant-run, resampled particles; the Student bound assumes independent runs); the organizer replica checks a reduced version of it. The row-19 pattern support of the replica is the four patterns seen in the study, so the replica estimates a lower bound of the event\'s probability.')
add('- The pair term and the success distribution are measured on rebuilt estimator successes (H1 premise for real chaining values).')
add('- The bit-sliced program is executed on sampled batches; full-scale execution is infeasible.')
add('')
add('## Appendix A. Self-test and calibration of `experiments/a0p38.py`')
add('')
add('```'); add(SELF); add('```')
add('')
add('## Appendix C. The conditions of rows 16..22 (the accepted event; member x, `experiments/a0p38.py` tables)')
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
add('## Appendix B. Programs (SHA-256 and full listings; `experiments/a0p38.py` is assembled by `mka0p.py` from the `a0p_*.py` parts)')
add('')
add('- `experiments/a0p38.py`: %s' % vt_hash)
for f in SRC: add('- `%s`: %s' % (f, hs[f]))
add('')
for f in SRC:
    add('### %s' % f); add(''); add('```' + ('c' if f.endswith('.c') else 'python')); add(src[f].rstrip('\n')); add('```'); add('')
open(OUT + '/proof.md', 'w').write('\n'.join(P) + '\n')

def rng(start, end=None):
    a = next(i for i, l in enumerate(P) if l.startswith(start)) + 1
    b = next(i for i, l in enumerate(P) if i >= a and l.startswith(end)) if end else len(P)
    return 'proof:%d-%d' % (a, b)
r4, r5, r6, r7, r9, r10, r11, r13 = (rng('## 4.', '## 5.'), rng('## 5.', '## 6.'), rng('## 6.', '## 7.'), rng('## 7.', '## 8.'), rng('## 9.', '## 10.'), rng('## 10.', '## 11.'), rng('## 11.', '## 12.'), rng('## 13.', '## 14.'))
H = []
def h(i, stmt, scope, ext, lim, ev): H.append(dict(id=i, role='score-critical', statement=stmt, scope=scope, extrapolation=ext, limitations=lim, evidence_ids=ev))
h('H1-single-trial-chaining-value', 'For M0 uniform on {0,1}^512 (two fresh random words per first block), CV1 = F_38(IV, M0) behaves as a uniform 256-bit value for the events of one fixed variant (W7, W16..W22 and E16x distributed as in Lemma 5.1).', 'g, the per-first-block success probability and the expected work.', 'The premise of the A0-variant lineage; the organizer experiment a0p-online-r38 runs the program on real first blocks.', 'A premise about the first-block compression.', [r5, r13])
h('H2-q3-accepted-event', 'The average over the 196,608 selected variants of Pr[the pair is in the accepted event (rows 16..22 with row 19 on signed differences, equal outputs) | good pair] is at least q3_model = 2^%.4f.' % Q3M, 'N_FB and the whole attack term.', '20 multilevel-splitting runs (C) with the variants of the selected classes: mean 2^%.4f, one-sided 99%% Student bound 2^%.4f, bootstrap 2^%.4f, %s verified collisions (one stalled run counted as 0); an independent Python implementation (the organizer replica, a lower-bound event restricted to four row-19 patterns and 512 sampled variants): %d development replicates, mean 2^%.4f; organizer replica a0p-q3-r38 with a frozen pass rule.' % (math.log2(qm), qlo, qbs, c(qsucc), len(reps), rmean), 'Participant-run Monte Carlo with a heavy-tailed row-20 stage; the replica tests a reduced version.', [r9, r13])
h('H3-pairs-in-first-block', 'The average over successes of the expected number of other row-16 passes of the same first block is at most 2^%.1f.' % H3B, 'The Bonferroni factor of a first block.', '%s rebuilt successes: %d other row-16 passes among %s evaluated variants of the passing classes; 99%% Poisson limit 2^%.2f.' % (c(H3['verified']), H3['other_r16'], c(H3['variants']), math.log2(h3lim)), 'Measured on rebuilt estimator successes.', [r9])
h('H4-allowances', 'The computation spent on the characteristic search, S and the class data, and all development is at most A_C + A_S + DEV = 2^48 + 2^50 + 2^50 target compressions.', 'The allowance term (negligible against T).', 'One 10-core machine, less than 2^21 core-seconds in all; holds at up to 2^27 compressions per core-second.', 'Wall-clock bound; A_C up to 2^84 changes the claim by less than 0.003.', [r10])
h('H5-bitsliced-planes', 'One instruction on a 256-bit plane costs one word operation (the 256-bit word RAM of the cost model); the row-16 program is charged at its executed instruction count, loads and stores included.', 'The dominant work term.', 'Executed instruction by instruction and compared with the scalar definition on sampled batches (selftest, a0p-online-r38).', 'Full-scale execution is infeasible.', [r7, r13])
CL = dict(schema_version=3, submission_state='ready', target_profile='sha256-r38-prefix-v1', attack_class='ordinary-collision', rounds=38, lane='exploratory',
          baseline_improved='sha256-r38-nominal-v2', certificate_manifest='certificates/manifest.json', experiment_manifest='experiments/manifest.json',
          claim=dict(time_log2=claim, time_unit='target-compressions', memory_log2_bytes=memclaim, preprocessing_log2=math.ceil(L['pre_log2'] * 1e5) / 1e5, success_probability=0.39, nonuniform_advice_log2_bytes=14),
          restrictions=['Target sha256-r38-prefix-v1 exactly: SHA-256 steps 0..37 on every padded block, the standard IV once, FIPS 180-4 padding, feed-forward, all eight digest words; outputs two distinct 128-byte messages M0 || M1, M0 || M1\' with equal digests.',
                        'Construction: the memory-efficient A0-variant attack (design of 2d1c4fc2 and fb176310 on ePrint 2026/1120 / 2026/1080), our implementation experiments/a0p38.py, with our characteristic P8 and the accepted event rows 16..22 (row 19 on signed differences) plus a direct output comparison.',
                        'Cost: exact ledger ledger_a0p.py: N_FB = %s first blocks, 8 classes of 24,576 variants, the row-16 program of %d instructions per 256 variants, executed counts; T x 2728 = %d; claimed %.5f.' % (c(L['NFB']), CAL['prog'], L['N'], claim),
                        'Success probability at least 0.39 under H1, H2 (q3_model 2^%.4f), H3, by Bonferroni per first block, independent first blocks and Chebyshev caps.' % Q3M,
                        'Memory 2^%.2f bytes (online %s bytes; the preprocessing peak).' % (memclaim, c(memonline))],
          heuristics=H)
for x in H:
    for k, v in x.items():
        if isinstance(v, str): assert len(v) <= 4096
json.dump(CL, open(OUT + '/claim.json', 'w'), indent=2); open(OUT + '/claim.json', 'a').write('\n')
os.makedirs(OUT + '/experiments', exist_ok=True)
for f in os.listdir(OUT + '/experiments'):
    if f.endswith('.py') and f != 'a0p38.py': os.rename(OUT + '/experiments/' + f, R + '/runs/a0p/old_' + f)
shutil.copyfile(VT, OUT + '/experiments/a0p38.py')
MAN = dict(schema_version=1, experiments=[
    dict(id='a0p-online-r38', kind='python-message-pairs-v1', program='experiments/a0p38.py', event=dict(kind='full-collision'),
         scope='H5 and the Lemma 4.1 identities on real first blocks (proof.md Sections 4, 7, 13). Trials 0..7: first blocks drawn from the organizer seed (two uniform 256-bit words from SHAKE-256 of the experiment id and seed per first block; real 38-step compressions) until one has a passing class (at most 64); its first passing class is run on two batches (its first 512 members): the counted row-16 program is executed instruction by instruction and its ok plane compared lane by lane with E16x computed from the Step-2 words and the 38-step trace; W7 is compared with c7 - A_{-1} and checked in F7. Trial 0 also runs the batch of the semi-free-start pair\'s variant on its chaining value: the counted program must find and accept it (positive lanes). Returns M0 || M1 and M0 || M1\' of the class\'s first member (128 bytes each; one variant of one chaining value, not a collision) iff there is no mismatch. Trials 8..255 return no pair by design.',
         hypothesis='Returned pairs: 8 (every executed trial mismatch-free); full collisions of the target: 0 (a returned pair is not a collision). Observations (untrusted): first_blocks, passing_classes, lanes (512), stage3a_passes, mismatches (0). Validation by us: 8 pairs returned, 0 mismatches, under 1 s.'),
    dict(id='a0p-q3-r38', kind='python-message-pairs-v1', program='experiments/a0p38.py', event=dict(kind='full-collision'),
         scope='H2 (proof.md Sections 6, 9, 13). Trials 0..9: 10 independent replicates of the estimator of q3 for the accepted event (row 16 exact over the 160 W16 words; rows 17..22 by proposals with the row\'s E bits imposed, at row 19 one of the four observed condition patterns drawn uniformly with weight 4 x 2^-f and the row checked on signed differences; tail: a variant of 512 embedded samples of the selected classes, W7 uniform in F7 by its affine families, rows 23..37, outputs compared; randomness SHAKE-256 of the experiment id and trial seed). Every success is rebuilt into (CV1, M1, M1\') and accepted only if the two 38-step compressions from CV1 are equal, M1 != M1\', the pair is in the accepted event and W7 is in F7. Trial t < 10 returns its first verified pair as CV1 || M1 and CV1 || M1\' (96 bytes each; semi-free-start collisions, never collisions from the IV); trial 10 returns a pair iff no rebuild failed and the mean of the 10 estimates is at least 2^%.4f; trials 11..255 return no pair by design.' % THR,
         hypothesis='Returned pairs: 3 to 10 semi-free-start pairs from the replicates (a replicate without a tail success returns none; validation by us: 4 to 9) and 1 from trial 10 (a pass; trial 10 needs trials 0..9 in the same request); full collisions of the target: 0. The pass rule was fixed from %d development requests (pooled means: min %.3f, median %.3f) before any validation run; a pass checks a reduced replica, it is not an estimate of q3. Observations (untrusted): log2_estimate (-1000 for no success), accepted_pairs, failed_rebuilds (0); trial 10 log2_pooled_mean.' % (len(DEV), pm[0], pm[len(pm) // 2]))])
json.dump(MAN, open(OUT + '/experiments/manifest.json', 'w'), indent=2); open(OUT + '/experiments/manifest.json', 'a').write('\n')
print('proof lines', len(P), 'bytes', len('\n'.join(P).encode()), 'claim', claim, 'memory', memclaim, 'score', round(score, 5))
```

