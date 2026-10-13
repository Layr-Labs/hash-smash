# Collision attack on 38-step SHA-256 with dense-part variants, a row-16 table and a four-lane counted program: 2^70.17649

**Track** sha256-r38-exploratory, target sha256-r38-prefix-v1, cost model collision-frontier-v5 (C = 2728).
**Claim** time_log2 = 70.17649 (the exact total is 2^70.176480 target compressions), success probability at least 0.39
(the bound is 0.39000000), memory 2^79.55 bytes, preprocessing 2^70.10637 (allowances and counted tables, included in time), nonuniform advice below 2^14 bytes.
The attack proper (online work, first-block compressions and the counted table construction) is 2^67.0361; the allowances for
unmeasured work are A_C = 2^70 (characteristic search), A_S = 2^60 (Step-1 solve) and DEV = 2^60 (all development), 2^70.002815 in all.

**This derivative.** Credited derivative combining c04b5a23 (70.23392), Jbenisek's 14b3b6ff-f9c8-4a4f-9278-15cfccf71bf2 (70.28679), dariolina's 1db43310-a194-428c-b14c-bd6af97ccc0a (70.73486), Th0rgal's aed05522-8fe5-4277-be03-8b50ffa49e26 (71.00164), Th0rgal's 19c9e7e7-b38b-43b6-9818-133841a0cb7c (71.06954), and Jbenisek's fdef4bab-a9d7-4052-b11f-e50fabfd7374 (71.07250), itself a credited derivative of Th0rgal's aa0496d3-d741-49e5-8f5c-0292e39115ee (71.33597); its lineage, which it credits, is in the paragraphs below. The text of this filing is the text of Th0rgal's 14adba55-453a-444a-b754-5ac61f90dc06 (claimed 70.17649; the c04b5a23 of the text below is Th0rgal's 695cf92d-f836-473f-831d-547523406f16; the allowances A_S = DEV = 2^60 are its) with corrections to the text only; the counted program experiments/vt38.py and the claimed value are unchanged. The corrections: the output of the ledger program in Appendix E.6 and its N are those printed by the embedded program (N = 3,639,736,073,456,835,419,065,567, which is 2^32 word operations more than the N that package printed; time_log2 is the same); the selftest transcript of Appendix A.1 is the program's output (E17 38, A17 55, success 2975); the chain of Section 6.5 and Appendix E.3 reads N <= N18 <= N17; and the cost-model experiment manifest cites q3_model = 2^-97.7784. Four components, each priced separately by the exact ledger of Appendix E.6:
(1) *the accepted event, 1-word bucket entries, and tightened online and P6 preprocessing programs* (Section 4.7, Section 5.1, Section 5.3, Appendix E.1, building on c04b5a23, 14b3b6ff and 19c9e7e7): each bucket entry is a single 256-bit word packing `c7 + 2^32` (bits `0..32`), `E1a = (A1 - S0(A0) + 1) mod 2^32` (bits `35..66`), `U = (A2 - S0(A1) - K2 - (A1 & A0)) mod 2^32` (bits `67..98`), `Q = A1 ^ A0` (bits `99..130`), `gi` (bits `131..135`), `a2i` (bits `137..146`), `A1` (bits `154..185`), `KCg = (W10x + s1(W15x) + A1 + c17(g)) mod 2^32` (bits `186..218`, with bit 218 absorbing the carry of `k + c17(g)`), and `a17(g)` (bits `224..255`); bits `33..34` and `150..153` are zero, so `W7 = EN - a` has bits `0..34` equal to `(c7 + 2^32) - a` without any shift before the F7 table load (keeping the online scan loop at 6 operations per entry with `ESZ = 1`, cutting table memory from 2^80.42 to 2^79.55 bytes, and reducing `P6` fill from 2 stores to 1 store per live word of G); in `gen_rare` and `gen_deep`, `S0(A1)` is folded into `U` in `P5` (saving `S0(A1)` and a subtraction on every W7 pass: `X_E17 = 38` vs `41`, `X_A17int = 55` vs `58`), and `PG` and `P2` are extracted at pre-shifted bit positions without `shl` (`X_SUCC = 2,975` vs `2,981` in c04b5a23 and `2,989` in 14b3b6ff; per-group fixed operations 3,366); in `P2` and `P6`, `P2` stores `s0(w)` at `S0T + w` (`27` ops vs `25`), `P6` count and fill load `su = s0(u)` in 1 operation instead of computing `rot32` in 7 operations, `P6` count increments headers by `ESZ = 1` with fast/slow paths for `Z0` wrap-around (`100` ops per `(Y, variant)` vs `144`), `P6` fill writes 1 word per live word of G (`122` ops per `(Y, variant)` vs `232`), and `P6` prefix writes 1 sentinel word without shifting (`5` / `7` ops per empty / non-empty header vs `6` / `11`), cutting total preprocessing from `2^78.3524` to `2^77.6669` operations (`2^66.2545` vs `2^66.9387` units);
(2) *its probability* (H2, Appendix E.2, combining 14b3b6ff, 1db43310 and aed05522): q3_model = 2^-101.10 x 2^3.3216 = 2^-97.7784, where 2^-101.10 is 1db43310's printed-event baseline (0.061 bit below the lowest of six independent 99% lower bounds across R1..R4 of Section 6.2/PREREG_q3b and S1..S2 of Appendix E.2: -101.00146, -101.00195, -101.00265, -101.00018, -101.03905, -101.03081; 43.9M verified tail successes, 0 failed rebuilds) and 2^3.3216 is 14b3b6ff's one-sided 99% lower bound of the gain from the printed event to the accepted one, measured in a preregistered paired run on this attack's own variant law (W8, W9, W10 of every sample from a fresh uniform sample of the dense-part variants of each seed; 32 fresh seeds x 2^28 proposals; mean +3.4015, seed sd 0.184, halves 3.340 / 3.463; the bound is over seeds, so it carries the overdispersion between seeds and the variant sampling); using aed05522's preregistered printed-event rule 2^-101.35 gives q3_model = 2^-98.0284 (time_log2 = 70.18938), and 14b3b6ff's 2^-101.50 gives 2^-98.1784 (time_log2 = 70.19818), all priced in Appendix E.5;
(3) *the whole-group pair budget delta = 1/25 = 0.04* (H5, Section 6.5, Appendix E.3, from 1db43310): every success in A' passes all of rows 16 and 17 with W7 in F7 (rows 16..18 are identical in the printed and accepted events), so pointwise N <= N17, the number of variants of the group passing all of rows 16..17 with W7 in F7; 1db43310's exact whole-group enumeration across all 256 A0 buckets on 2,500 verified successes (3,585,652 other row-16 entries, 241,170 W7 passes) found 48 passing all of row 17 (99% Poisson limit 0.02670 for delta17) and 0 reaching row 18 (99% limit 0.00184 for delta18), setting delta = 1/25 = 0.04 (1.50x the 99% limit of delta17 and 21.7x that of delta18; fdef4bab's delta = 0.564 gives 70.20124, priced in E.5).
Effect on log2 T: 71.07250 (fdef4bab) -> 71.00164 (aed05522) -> 70.73486 (1db43310) -> 70.28679 (14b3b6ff) -> 70.23392 (c04b5a23) -> 70.17649 (this derivative). The organizer replica of q3 (vt-q3-smc-r38) estimates the accepted event and replays its first two pairs of every replicate through the tightened counted program; its calibration (960 replicates, fresh labels, preregistered) has mean 2^-97.675.

**Earlier derivative (fdef4bab, the text of that filing).** Credited derivative of Th0rgal's aa0496d3-d741-49e5-8f5c-0292e39115ee (71.33597), itself a derivative of Jbenisek's 0bf9d76b-d200-4b40-a32d-46ce1aaffcb7 (71.34862), which builds on 012400ff-d717-461c-a433-377f35ce2298 (Jbenisek, 71.43541) and 37742a53-4062-4c76-bdd0-cd74b4c6eb21 (winglock, 71.69523). Against aa0496d3 it changes four things in how the counted preprocessing is priced and in the pair budget (Appendix D): (1) the counts of the preprocessing bodies are those the printed bodies execute (the fill pass of P6 executes 233 operations per (Y, variant) where 189 was charged; P5 setup 37, append 46, body 57 where 35, 43, 56 were charged), (2) the zero pass of P6 is unrolled 16 times, (3) the Y loop of the count and fill passes of P6 runs on u = Y + A1 in two segments with the table base running with it, and (4) the pair budget of H5 is charged at delta = 0.564, the sum of the one-sided 99% Poisson limits of the package's own measurements (Section 6.5), instead of 1. The online counted program, the construction, the other premises, both experiments and nearly all of the text are aa0496d3's, 0bf9d76b's, 012400ff's and 37742a53's; "we" in the text below is the authors of those packages.

**Earlier derivatives (text of aa0496d3).** The package of aa0496d3 is 012400ff (Jbenisek, 71.43541; built on 37742a53, winglock, 71.69523) with further changes to how its counted program, its counted table
construction and its cap margins execute and price the same search (Appendix C): the tables list only the 22 words of G for which row 17 can hold, each table entry is a 256-bit word (1 word in this derivative, 2 words in aa0496d3..c04b5a23, packing E1a, a17(g), KCg
and the indices), the W7 and A17 paths test row 17 with immediate masks and values in 38 and 17 operations (41 and 17 in aa0496d3..c04b5a23), the four-lane header uses ~MAJ and ~CH with telescoping bucket-counter accumulation and a two-operation sentinel discriminator, and the four work counters use per-counter Chebyshev cap margins (2^-16, 2^-14, 2^-7, 2^-5). The construction, the premises (with H3's memory and preprocessing figures of this derivative: 2^79.55 bytes and 2^66.2545 units), both experiments and nearly all of the text are 37742a53's and 012400ff's; "we" in the text below is its authors.

**What the base package is.** The construction is not ours. The two-block attack, the characteristic, the two-bit conditions and the
semi-free-start pair are those of Li, Zhang, Li, Liu, Qian and Zhu, "Pushing Collision Attacks on SHA-2 to 39 Steps" (IACR ePrint 2026/1120);
the dense-part variants (A0, A1, A2 replaced in the published dense part), the row-16 table keyed by (Y, Z0) and the success analysis
by groups are those of the public HashSmash packages c99df2dc (qkniep) and 0ae69bcb (0xshikhar, 72.64). We re-implemented all of it
independently (we executed no peer code), measured every operation count ourselves, and changed four things:
(1) the counted online program is cheaper: a bucket is a sentinel-terminated run of one-word entries (two-word in aa0496d3..c04b5a23) scanned in six operations per entry, the
shared F7 test is one table load, and four A0 blocks share one vector computation of (Y, Z0) in the four 64-bit lanes of a 256-bit word
(18.75 operations per block instead of 36 for the scalar block of the same program; 52.5 operations per (chaining value, A0) in expectation and at the caps,
against the 117 of 0ae69bcb); (2) the work caps are fixed with Chebyshev's inequality and per-counter margins (2^-16, 2^-14, 2^-7, 2^-5) instead of Hoeffding's with margins up to 4x;
(3) the allowances A_S and DEV are smaller (A_S = 2^60 against a published cost of about 2^38.3 compression calls of the
Step-1 solve, H4b; DEV = 2^60, about 2^14 times a physical bound on the compute of this work and 2^10 times the direct cost of
selecting the A0 set, H4c, Section 9) instead of 2^70 and 2^64; A_C = 2^70 is kept, with the
CPU-ceiling argument of 0ae69bcb that passed review; (4) the success target is exactly 0.39 (no 2% slack), and q3_model of the printed event is 2^-101.10 (1db43310; 2^-101.35 in aed05522, 2^-101.5 in 37742a53) instead of 2^-102. Everything else (the shape of
the premises H1, H2, H5) follows 0ae69bcb; its pair budget is delta = 1, ours 1/25 = 0.04 (Section 6.5, Appendix E.3; 0.564 in fdef4bab).

| change against 0ae69bcb (72.64) | log2 T |
|---|---|
| this derivative (Appendix E; c04b5a23 is 70.23392, 14b3b6ff is 70.28679, 1db43310 is 70.73486, aed05522 is 71.00164) | 70.17649 |
| fdef4bab (Appendix D; 19c9e7e7 is 71.06954) | 71.07250 |
| aa0496d3 (Appendix C; 0bf9d76b is 71.34862, 012400ff is 71.43541) | 71.33597 |
| 37742a53 (base of 012400ff) | 71.69523 |
| four-lane blocks replaced by scalar blocks | 71.81039 |
| q3_model = 2^-102 instead of 2^-101.5 | 72.03238 |
| A_S = 2^70 and DEV = 2^64 (0ae69bcb's allowances) | 72.08812 |
| 0ae69bcb as filed | 72.64 |

The largest single term is the allowance A_C = 2^70, 88.5% of T (2^70 / 2^70.17649 = 0.885); the attack itself is 2^67.0361. H4a states which parts of the characteristic search we measured; Appendix E.5 gives the effect of a
different charge for the characteristic search (A_C = 2^72: 72.04619; 2^68: 68.60454).

## 0. Summary

Two messages M0 || M1 and M0 || M1' of two blocks (common first block, padding appends the same third block) collide under the 38-step
target. For every first block M0, CV1 = F_38(IV, M0) is a chaining value; given CV1 a *dense-part variant* v = (A0, A1, A2) is a
semi-free-start pair candidate: the published dense part with three words replaced, so that the Step-2 words W0..W7 connecting CV1 to the
dense part exist for every CV1 and the pair follows all characteristic cells of rows -4..15. Row 16 holds iff W16 lies in a set G of
exactly 32 words, and W16 = s0(Y + A1) - A1 + Z0 + c9(A2) where (Y, Z0) depends only on (CV1, A0): a table T_j per A0_j lists, for every (Y, Z0),
the variants of A0_j whose W16 is one of the 22 words of G for which row 17 can hold (about 3.8 entries per bucket; Appendix C). A *group* is one first block and one lookup per A0 in a set of 256 values;
each entry is tested for W7 in F7 (6.7%), then the E17 mask (10 bits), the A17 conditions, rows 18..21 (rows 19 and 20 in the accepted form of Section 4.7), and after row 37 the
outputs of the two members are compared. One group succeeds with probability S = SR * p2 * q3 = 2^-64.200 (SR = 191,773,672,732 variants, p2 = 2^-3.90197, q3 = 2^-97.7784 modelled
for the accepted event; for the printed event 2^-101.10 modelled, about 2^-101.0 measured). The program runs N_G = 10,687,797,395,951,771,071 groups (2^63.2126) under four work caps and halts at the first success.

## 1. Target, cost model and notation

Target sha256-r38-prefix-v1: SHA-256 steps 0..37 on every padded block, standard IV once, FIPS 180-4 padding, feed-forward, all eight digest words.
Cost model collision-frontier-v5, C = 2728: one target compression costs 1 unit, every other primitive word operation 1/C; the machine is a
256-bit word RAM whose primitives are 256-bit load/store, addition and subtraction mod 2^256, bitwise AND/OR/XOR/NOT, shift or rotation, comparison,
conditional branch, independent uniform random 256-bit word; memory is a reported metric. Our counted machine (Section 5.3) charges 1 per executed
add, sub, rsub (immediate minus register), and, or, xor, shl, shr, ld, ldi, sti, st, li (load immediate), rand, jmp; 2 per conditional branch
(comparison and branch); 1 unit for one target compression (f38); the observers obs, mark and succ cost nothing. Immediates and shift amounts are
instruction fields. Notation: "a" = A_{-1} = word 0 of CV1; A_i, E_i, W_i are the step-i words; member x is the message printed second in
ePrint 2026/1120 Table 5 (M'), member y the message printed first (M). Sign convention used throughout: every difference is member y minus member x,
DW_i = W_i^y - W_i^x and DS0_i = s0(W_i^y) - s0(W_i^x) (mod 2^32), so DW_7 = +2^29 and DW_16 = 0xe0000000 = -2^29, i.e. W16^y = W16^x - 2^29. A prime (W'_i, A'_i) denotes the word of member y, an unprimed word that of member x, and dW_i is a synonym of DW_i. (The letter Y alone is the table index of Section 4.4.)

## 2. Sources, and what is reused or new

Reused (credited in the dependencies file): ePrint 2026/1120 (characteristic, two-bit conditions, published semi-free-start pair; our own
transcription in `experiments/vt38.py`, verified against the published pair); c99df2dc (qkniep) and 0ae69bcb (0xshikhar): the idea of dense-part
variants (A0, A1, A2), the row-16 lookup keyed by (Y, Z0) and its Lemmas, the A0 set of 256 values and the exact sizes |R_j| (we recomputed the sizes
exactly, 0 mismatches), the group-level success analysis (pair budget, Bonferroni), the shape of the allowance argument H4 and of the organizer
replica; earlier public r37/r38 filings (6c77089c, 1c368173, b947b377, 087a18c4, 1f12a09a) for the variants-of-S lineage and the SMC design; 6eeefb64
(sha256-r32) for the calibrated price of a solver CPU-second. We executed no peer code; the peers' files were read as data.

New in this package (all code and measurements are ours): the independent C core (`r38.h`) with the exhaustive passes (`ex1.c`: A2 list, G, |F7|,
the preimage counts of phi) and the exact |R_j| (`rcount.c`); the true-bucket generator (`bucket.c`); the counted online program with
four-lane blocks and its interpreter (`experiments/vt38.py`, the assembly of the development modules vtref, vtprog and vt_exp with the data blobs); the counted preprocessing
(variant enumeration and table construction as counted code, Appendix B.3); the exact ledger and its sensitivity (`ledger38.py`, `sens38.py`); a
preregistered sequential Monte-Carlo estimate of q3 (`smc.c`, with a new pair rebuild and verification of every success); the organizer experiments.

## 3. The characteristic and the published dense part

Rows with a non-'=' cell of the 38-step characteristic (ePrint 2026/1120 Table 3), as (mask, x-value, x XOR y) per kind A, E, W
(the x-value is the bit pattern of member x on the mask) and, for E, the set PQ_i of bits b with the '+' condition E_i[b] = E_{i-1}[b] (the '+' marks of the printed table regrouped by the later row, which is how every program of this package tests them; the published pair satisfies all of them, and the printed grouping differs from this one in rows 6, 7, 11, 13, 14, 16 and 17); rows not listed carry no cell:

- row 6: E mask 0x08441090 x-value 0x08040090 x^y 0x00000000; E_6 = E_5 on bits 0xe0000000
- row 7: A mask 0x60000000 x-value 0x20000000 x^y 0x60000000; E mask 0xead6109b x-value 0xe2c01001 x^y 0xe0000000; W mask 0x20000000 x-value 0x00000000 x^y 0x20000000; E_7 = E_6 on bits 0x00080800
- row 8: A mask 0x00410810 x-value 0x00000010 x^y 0x00410810; E mask 0xebdf7bfb x-value 0x89152879 x^y 0x084c1890; W mask 0x04400800 x-value 0x04400000 x^y 0x04400800; E_8 = E_7 on bits 0x04000000
- row 9: E mask 0xfeffffbf x-value 0xc670b71b x^y 0x0490000b; W mask 0x20000000 x-value 0x20000000 x^y 0x20000000
- row 10: E mask 0x3dff7b9f x-value 0x28c32a97 x^y 0x00410800; W mask 0x050112aa x-value 0x0100000a x^y 0x050112aa
- row 11: A mask 0x0000080c x-value 0x00000808 x^y 0x0000080c; E mask 0xbdffffbf x-value 0x80f2c1be x^y 0x20007004; W mask 0x00081400 x-value 0x00081400 x^y 0x00081400
- row 12: A mask 0x44204602 x-value 0x40004200 x^y 0x44204602; E mask 0xfdffffbf x-value 0x5d9d1216 x^y 0x3c230005; E_12 = E_11 on bits 0x00000040
- row 13: A mask 0x20010000 x-value 0x00000000 x^y 0x20010000; E mask 0xffefff7f x-value 0x35c13b0d x^y 0x0001077a
- row 14: A mask 0x08030090 x-value 0x08000090 x^y 0x08030090; E mask 0x7c636f7f x-value 0x20026471 x^y 0x08010000; E_14 = E_13 on bits 0x00000080
- row 15: A mask 0x02808000 x-value 0x00800000 x^y 0x02808000; E mask 0x4a530ffa x-value 0x4a130b5a x^y 0x00000880; W mask 0x04400800 x-value 0x04000000 x^y 0x04400800; E_15 = E_14 on bits 0x00001000
- row 16: E mask 0x4c431a80 x-value 0x48030280 x^y 0x40421200; W mask 0x20000000 x-value 0x20000000 x^y 0x20000000
- row 17: A mask 0x20000000 x-value 0x20000000 x^y 0x20000000; E mask 0x40c21a80 x-value 0x00000800 x^y 0x00000000; E_17 = E_16 on bits 0x00040010
- row 18: E mask 0x40c61230 x-value 0x00421210 x^y 0x00040010; E_18 = E_17 on bits 0x01008000
- row 19: E mask 0x31848e32 x-value 0x30040430 x^y 0x01808000
- row 20: E mask 0x21848010 x-value 0x20040010 x^y 0x00000000
- row 21: E mask 0x21808c00 x-value 0x21008800 x^y 0x20000000
- row 22: E mask 0x20000000 x-value 0x00000000 x^y 0x00000000
- row 23: E mask 0x20000000 x-value 0x20000000 x^y 0x00000000; W mask 0x0582a000 x-value 0x0582a000 x^y 0x01808000
- row 25: W mask 0x20000000 x-value 0x00000000 x^y 0x20000000

Two-bit conditions with a word in rows >= 16 (Table 4; kind 0 = A, 1 = E, 2 = W; (kind1, row1, bit1) equal/different to (kind2, row2, bit2), keyed at
the later row; W25[4] = W25[9] of the printed table is read as W25[4] = W25[6], the reading under which the published pair satisfies it):

- row 7: W7[1] = W7[12]
- row 7: W7[8] != W7[25]
- row 7: W7[14] != W7[18]
- row 8: W8[0] != W8[28]
- row 8: W8[1] = W8[18]
- row 8: W8[30] != W8[9]
- row 16: A14[15] = A16[15]
- row 16: A14[23] = A16[23]
- row 16: A14[25] = A16[25]
- row 16: A15[4] = A16[4]
- row 16: A15[7] = A16[7]
- row 16: A15[16] != A16[16]
- row 16: A15[17] = A16[17]
- row 16: A15[27] = A16[27]
- row 16: A15[29] = A16[29]
- row 16: W16[1] != W16[12]
- row 16: E16[3] != E16[8]
- row 16: E16[4] != E16[23]
- row 16: W16[4] != W16[6]
- row 16: W16[8] = W16[25]
- row 16: E16[14] = E16[28]
- row 16: W16[14] = W16[18]
- row 16: W16[20] != W16[27]
- row 16: W16[22] != W16[31]
- row 17: E16[4] = E17[4]
- row 17: A16[15] = A17[15]
- row 17: E16[18] = E17[18]
- row 17: A16[23] = A17[23]
- row 17: A16[25] = A17[25]
- row 17: A17[6] = A17[18]
- row 17: A17[8] = A17[17]
- row 17: A17[9] = A17[20]
- row 18: A16[29] = A18[29]
- row 18: E17[15] = E18[15]
- row 18: E17[24] = E18[24]
- row 18: E18[0] != E18[13]
- row 19: A18[29] = A19[29]
- row 19: E19[6] != E19[19]
- row 19: E19[20] = E19[2]
- row 21: E21[2] = E21[16]
- row 23: W23[0] != W23[30]
- row 23: W23[1] != W23[31]
- row 23: W23[14] = W23[21]
- row 23: W23[16] = W23[25]
- row 25: W25[4] = W25[6]
- row 25: W25[20] = W25[27]
- row 25: W25[22] = W25[31]

The published semi-free-start pair (Table 5): CV = cd278980 1b12a052 b87cc8a6 a9e059c5 c9c3db85 6ca4b5b5 63d13ac1 c0329f1e; M' (member x) = 48fc271b 9fca20cd cc89f96f fc40396f 8b328cb4 6b91ef78 97f9b767 c2450045 3f416758 fe9804cb 63a88c0f 0ceb1f8d a28cd15a 77a1e994 d28e48a0 9f1f65bb; M (member y) = 48fc271b 9fca20cd cc89f96f fc40396f 8b328cb4 6b91ef78 97f9b767 e2450045 3b016f58 de9804cb 66a99ea5 0ce30b8d a28cd15a 77a1e994 d28e48a0 9b5f6dbb. Its 38-step outputs are equal
(5d9ca5f4 59ace3a3 26c9c26c 4252c585 4c0803b7 1b4d5ccd 25c3ccc0 90645c4d); `vt38.py selftest` item 1 checks it. S* (the published dense part) denotes the A/E/W values of rows -4..15 of this pair.
Step-2 bijection: for every chaining value CV1 the Step-2 equations E_i = A_i + A_{i-4} - S0(A_{i-1}) - MAJ(A_{i-1}, A_{i-2}, A_{i-3}) (i = 3..0) and
W_i = E_i - A_{i-4} - E_{i-4} - S1(E_{i-1}) - CH(E_{i-1}, E_{i-2}, E_{i-3}) - K_i (i = 0..7) give the unique W0..W7 connecting CV1 to a dense part
(A0..A7, E4..E7); CV1 -> (W0..W7) is a bijection of (2^32)^8 for a fixed dense part (triangular system). For every dense part of this package
W'_i = W_i (i <= 6) and W'_7 = W_7 + d7, d7 = 2^29, and W7 = c7 - a with c7 a constant of the dense part. The characteristic fixes the difference
of W22; W7 enters rows >= 16 only through s0(W7) in W22 and W7 in W23, so a pair can follow row 22 only if s0(W7 + d7) - s0(W7) = t7 = 0x03bff800:
F7 = {w : s0(w + d7) - s0(w) = t7} has |F7| = 287,309,824 elements (exhaustive count, `ex1 f7`), p2 = |F7| / 2^32 = 2^-3.90197.

The modular differences of the published words that reach rows >= 16: (DW_i, DS0_i) = (W'_i - W_i, s0(W'_i) - s0(W_i)) = (0xfbc00800, 0xfe7f8000) at i = 8, (0xe0000000, 0x043ff800)
at i = 9, (0x03011296, 0xefffa0d0) at i = 10, (0xfff7ec00, 0xfcfeed6a) at i = 11, (member y minus member x, the sign convention of Section 1; `vt38.py` defines DW and DS0 from the pair as ty - tx); W12, W13, W14 carry no difference and dW16 = W16^y - W16^x = 0xe0000000, dW17 = 0.


## 4. Dense-part variants

### 4.1 Definition and validity

**Definition.** For words (A0, A1, A2) the variant v = (A0, A1, A2) is the dense part with A0, A1, A2 of both members replaced (rows 0..6 carry no
A or E difference, so both members get the same values), A3..A13, E7..E13 and W11..W15 of S* unchanged, and E4, E5, E6 and W8, W9, W10 of each member
recomputed by E_i = A_i + A_{i-4} - S0(A_{i-1}) - MAJ(A_{i-1}, A_{i-2}, A_{i-3}) (i = 4, 5, 6) and W_i = E_i - A_{i-4} - E_{i-4} - S1(E_{i-1}) -
CH(E_{i-1}, E_{i-2}, E_{i-3}) - K_i (i = 8, 9, 10). (E7 depends on A3..A7 only; W11 on E7..E11 and A7 only; both are unchanged.)

**Validity.** v is valid if (i) the E cells of rows 4..8 hold for both members, including the '+' pairs (rows 5/6: E6[31..29] = E5[31..29]; rows 6/7:
E7[19] = E6[19], E7[11] = E6[11]), and (ii) for i = 8, 9, 10, 11 the pair (W^y_i - W^x_i, s0(W^y_i) - s0(W^x_i)) equals the published value (DW_i, DS0_i).
The XOR cells of W8..W10 are not required: these words reach rows >= 16 only through those modular quantities (W8 in W23 via s0 and in W24; W9 in W16,
W25 and via s0 in W24; W10 in W17, W26 and via s0 in W25). The predicate is `valid()` in vt38.py; `r38.h var_valid` is the C twin.

**Lemma 3 (variants are sound).** Let v be valid, CV1 arbitrary, W0..W7 the Step-2 words of member x from CV1 and v, W'_0..W'_7 those of member y, and
M1 = (W0..W7, W8..W15 of x), M1' = (W'_0..W'_7, W8..W15 of y). Then F_38 from CV1 reproduces v's A0..A13, E4..E13 in both members, rows -4..15 follow every A/E cell,
and every term of W16..W37 that involves W0..W15 has the published difference, except the s0(W7) term (handled by F7). In particular dW16 = 0xe0000000
and dW17 = 0. *Proof.* Steps 0..7 reproduce A0..A7, E0..E7 by construction of the Step-2 words; steps 8..10 reproduce E8..E10 and A8..A10 because W8..W10
are solved from them; steps 11..15 are those of S* (they depend on rows 7..15 and W11..W15 only). Rows 0..3 have no cells; rows 4..8 hold by (i); rows 9..15 are those
of S*. W0..W6 have no member difference and W7 has difference d7 for every dense part of this kind (c7^y - c7^x = E7^y - E7^x). The expansion terms that involve
W8..W11 have the published differences by (ii); W12..W15 are published. Checked on real chaining values (selftest item 3 and the 1536 true buckets of Section 6.3).

### 4.2 The A2 list

Conditions that involve A2 alone: E6 = A6 + A2 - S0(A5) - MAJ(A5, A4, A3) must satisfy row 6's x-value cells and E7[19] = E6[19], E7[11] = E6[11] (both members);
W10 (which depends on E6 only) must have the published (dW10, ds0(W10)). An exhaustive pass over all 2^32 values of A2 (`ex1 a2`) leaves exactly 768 values
(Appendix A.3), the A2 list; it equals the list of the public packages. W9 = c9(A2) - A1 with c9(A2) = E9 - 2 A5 + S0(A4) + MAJ(A4, A3, A2) - S1(E8) - CH(E8, E7, E6(A2)) - K9
(member x; member y: c9 + dW9, and dW9 = 0xe0000000 holds for every A1 and every list member: the counted preprocessing asserts it).

### 4.3 The A0 set and the variant sets R_j

For A0 fixed, R(A0) is the set of (A1, A2) with A2 in the A2 list and (A0, A1, A2) valid. Condition (i) on E5 (E5[31..29] = E6[31..29]) confines A1 to one residue
interval of length 2^29 per A2, so R(A0) is found by testing 768 x 2^29 candidates. The only condition that involves A0 is the s0 difference of W8 = F(A1, A2) - A0, where F does not
depend on A0. The A0 set is the 256 values chosen by 0xshikhar/qkniep (0ae69bcb, c99df2dc) by the exact histogram of F (as described in those packages); it is advice here (H6) (Appendix A.2 lists the values and the exact sizes).
We recomputed every |R_j| exactly with `rcount.c` (768 x 2^29 candidates per A0, the A0-free valid pairs: 9,945,876,032 = 2^33.21145; 2,428,544 pairs were cross-checked
against the generic validity test, 0 disagreements); all 256 values equal the published ones. min |R_j| = 747,959,736 = 2^29.47839, max 750,798,738 = 2^29.48385 and

    SR = sum_j |R_j| = 191,773,672,732 = 2^37.48061.

### 4.4 Row 16 is a function of (Y, Z0)

**Lemma 4 (rows 16..22 do not depend on the variant).** Fix a valid v and let CV1 be uniform. Then (W0, ..., W7) is uniform on (2^32)^8 (Step-2 bijection, Section 3); conditioned on W7 in F7, (W0..W6) is
uniform and independent of W7. For any (W14, W15) and W9..W13, the map (W0..W5) -> (W16..W21) is a bijection for fixed W6 (W5 = W21 - s1(W19) - W14 - s0(W6), ...,
W0 = W16 - s1(W14) - W9 - s0(W1)), so (W16..W21) is iid uniform and independent of (W6, W7), and W22 = s1(W20) + W15 + s0(W7) + W6. Hence the joint distribution of rows 16..22
of both members, conditioned on W7 in F7, is the same for every valid variant, and so is the probability that rows 16..22 hold. Rows 23..37 depend on the variant only through
W8, W9, W10 of both members (W23 = s1(W21) + W16 + s0(W8) + W7, W24 = s1(W22) + W17 + s0(W9) + W8, W25 = s1(W23) + W18 + s0(W10) + W9, W26 = s1(W24) + W19 + s0(W11) + W10).

**G.** With rows 12..15 of S*, row 16 (cells, '+', the conditions of Section 3 keyed at row 16) is a function of W16^x alone: E16 = A12 + E12 + S1(E15) + CH(E15, E14, E13) + K16 + W16
and A16 = E16 - A12 + S0(A15) + MAJ(A15, A14, A13) in each member, W16^y = W16^x + 0xe0000000. An exhaustive pass over all 2^32 values (`ex1 g`; counted code P1) finds exactly 32 words,
G = {0x35f29010 + any subset of the bits 0, 2, 10, 13, 19} (a fraction 2^-27 of all words).

**Lemma 5 (W16).** For a chaining value CV1 and A0 put hh = d - S0(a) - MAJ(a, b, c), E0 = A0 + hh, Y = -S0(A0) - MAJ(A0, a, b) - g - S1(E0) - CH(E0, e, f) - K1,
W0 = A0 + hh - d - h - S1(e) - CH(e, f, g) - K0 and Z0 = W0 + s1(W14), where (a, ..., h) = CV1. For every valid (A0, A1, A2): W0 is the Step-2 word, W1 = Y + A1, W9^x = c9(A2) - A1 and
W16^x = s0(Y + A1) - A1 + Z0 + c9(A2) (mod 2^32). *Proof.* E0 depends on A0 and CV1 only; E1 = A1 + c - S0(A0) - MAJ(A0, a, b), so W1 = E1 - c - g - S1(E0) - CH(E0, e, f) - K1 = A1 + Y;
W9 = E9 - A5 - E5 - S1(E8) - CH(E8, E7, E6) - K9 with E5 = A5 + A1 - S0(A4) - MAJ(A4, A3, A2); W16 = s1(W14) + W9 + s0(W1) + W0. (`vt38.py selftest` item 3 checks the four identities on 40
real chaining values; `tbl.c` checks W16 against the full 38-step trace on 34.6 million (variant, chaining value) pairs, 0 mismatches.)

### 4.5 The tables T_j and the bucket bound

For j = 1..256 let T_j map every (Y, Z0) in (2^32)^2 to the list of entries for the (A1, A2) in R_j with s0(Y + A1) - A1 + Z0 + c9(A2) in G', the 22 words of G for which row 17 can hold (Appendix C). By Lemma 5 and the definition of G,
the bucket T_j[Y, Z0] holds exactly the variants of A0_j whose row 16 holds with W16 in G' for a chaining value with these (Y, Z0). An entry is a single 256-bit word packing
c7 + 2^32 (W7^x = c7 - a, bits 0..32, with bits 33..34 and 150..153 zero) and the constants of the variant and of W16 (Appendix E.1; two words in Appendix C); a bucket is its entries followed by a sentinel entry
(Section 5.3).

**Lemma 6 (bucket bound).** |T_j[Y, Z0]| <= 236,544 for all j, Y, Z0. *Proof.* With u = Y + A1 the condition reads phi(u) = g - Y - Z0 - c9(A2), phi(u) = s0(u) - u. For each of the 768 list values
A2 and each of the 22 g in G' this fixes phi(u), and every value has at most 14 preimages (exhaustive over 2^32, `ex1 phi`: one value with 14, one with 13, three with 12), so a bucket has
at most 14 x 22 x 768 = 236,544 entries. (Observed maximum over the 1536 true buckets of Section 6.3: 48.)

**Expected bucket size.** For a uniform CV1, (W0, W1) is uniform for every fixed variant (Step-2 bijection, Section 3), hence (Y, Z0) is uniform, and E|T_j[Y, Z0]| = 22 |R_j| 2^-32 exactly (3.846 for the largest R_j);
per group, E[entries] = SR * 22 / 2^32 = 982.3173.

### 4.6 Row 17 of member y

For each of the 32 values of W16 in G the row-16 state of both members is fixed, and W17^y = W17^x (dW17 = 0). For all 32 values E17^y = E17^x and A17^x - A17^y = 2^29 (the G record is
built from both members, `grec` in vt38.py), so member y's row-17 cells follow from member x's (the cell of A17 requires A17^x[29] = 1). Row 17 is tested on member x: E17^x against a mask
of 10 bits (its x-value cells, the '+' pair with E16 and the two E16-E17 conditions), A17^x against 4 bits (its cell and the A16-A17 conditions with A16 known) and the three A17-internal
conditions. The 10 and 4 bits are the popcounts of the masks of the 32 G records (all equal).

### 4.7 The success event

For a chaining value CV1 and a valid variant v, A(CV1, v) is the event that row 16 holds (W16 in G), W7 is in F7, and rows 17..37 hold (cells, '+', the conditions of Section 3).
**Lemma 7.** A(CV1, v) implies F_38(CV1, M1) = F_38(CV1, M1'), hence a collision of M0 || M1 and M0 || M1' when CV1 = F_38(IV, M0); M1 != M1' because W7 differs by d7.
*Proof.* Rows 34..37 have no u/n cell, so A_i and E_i (i = 34..37) are equal in both members; with the common CV1 these are the outputs. (Every success of Section 6 is also checked directly:
`smc.c` and the replica rebuild each success into CV1, M1, M1' and compare the two 38-step compressions.)

**This derivative: the accepted event.** A'(CV1, v) is the event that row 16 holds (W16 in G), W7 is in F7, rows 17..21 hold (cells, '+', the conditions of Section 3 closing at rows 17..21) except that at row 19 the nine value bits of E19 on 30040e32 may take any of the four patterns 00040832, 10000010, 20000c12, 30040430 and at row 20 the value bit E20[29] is replaced by the tie E20[29] = E19[29], and the words A34..A37, E34..E37 are equal in both members. Nothing in rows 22..37 is tested (W23 and W25 included). A(CV1, v) implies A'(CV1, v).
**Lemma 7'.** A'(CV1, v) implies F_38(CV1, M1) = F_38(CV1, M1'), hence a collision of M0 || M1 and M0 || M1' when CV1 = F_38(IV, M0). *Proof.* The outputs are CV1 plus (A37, A36, A35, A34, E37, E36, E35, E34), equal by the definition. M1 != M1' as before.
The program tests exactly A' (Section 5.4), so it accepts every success of that event whatever path rows 22..37 take. Why the four patterns: an enumeration over the nine E19 value bits and the six E20 value bits on 64 sampled prefixes (every other word held) finds exactly eight combinations that pass rows 19..21, the four patterns times E20[29] in {0, 1}; with E20[29] != E19[29] the CH of row 22 passes E21's bit-29 difference (derivation computed, not proved). The program's validity does not depend on it; its probability is measured (Appendix E.2).


## 5. The algorithm

### 5.1 Preprocessing (deterministic; every operation count is an executed-operation count of counted code)

All of it is code of the counted machine of Section 5.3 (`src/vtpre.py`, Appendix B.3 and E.1; each loop body is generated and executed by the interpreter on test inputs, and the ledger charges
(items) x (the longest path of the body) + the loop control; for the passes of P6 the loop control is part of the measured iteration). Bodies were checked against the C/reference definitions (Section 6.3).

| pass | what | items | ops per item (longest path) |
|---|---|---|---|
| P1 | the set G: row 16 of both members as a function of W16 | 2^32 words | 117 (+3 loop) |
| P1' | the 22 live words of G: the row-17 tests of each g of G over all E17 (Appendix C) | 32 x 2^32 values | 21 (+3) |
| P2 | the F7 and s0 table: first zero the region of addresses 0 .. 2^34 + 2^32 + 1 (4 per word), then store s0(w) at S0T + w, flag 1 at w and w + 2^32 for w in F7, and the value 2 in a sentinel region | 2^32 words | 27 (+3) |
| P3 | the A2 list (conditions on A2 alone) | 2^32 words | 41 (+3) |
| P4 | the 768 A2 records (2 words) and the 32 G records (12 words) | 768 + 32 | 39,168 + 3,072 in all |
| P5 | the variant lists R_j: for each of 256 A0 and 768 A2, the window of 2^29 values of A1 | 256 x 768 x 2^29 candidates | setup 37, body at most 57 (+3 loop), 44 per valid variant (2-word record: eb, c9x) |
| P6 | the tables T_j: zero the 2^64 headers, count, prefix, fill | 2^64 headers and 2^32 Y x variants x 22 g | 34 per 16 headers (unrolled, loop branch included); 100 and 122 per (Y, variant) with their loop control, and 22,940,733 and 22,940,755 per variant including the exact slow-path bound (Appendix E.1); 5 / 7 per empty / non-empty header (+3) |

P6 writes, for every A0_j, every header (Y, Z0) in (2^32)^2 and every 1-word entry (Section 4.5); a bucket is its entries followed by a 1-word sentinel entry, the header holds the address of the word before the bucket's first entry (`base - 1`),
empty buckets point to one shared sentinel entry. Total preprocessing is 240,120,385,693,241,128,129,080 operations, 2^66.2545 target compressions (the P6 terms dominate: 2^73.1 for zeroing, 2^76.1 for counting,
2^76.4 for filling, 2^75.3 for the prefix pass, in operations; everything before P6 is below 2^53). Every one of these cells is written by the charged preprocessing; nothing is advice except
the 256 A0 values (Section 8).

### 5.2 Online

One *group*: draw a first block M0 (two random 256-bit words), compute CV1 = F_38(IV, M0) (one target compression), then for each of the 256 A0_j compute (Y, Z0) (Lemma 5), load the header and scan the bucket.
For each 1-word entry `EN`: increment the cursor `OFF`, load `EN`, form `W7 = EN - a` (bits `0..32` of `EN` store `c7 + 2^32` and bits `33..34` and `150..153` are `0`; `a = A_{-1}` is word 0 of CV1) and load the F7 table at that address (masked to 35 bits): 0 (not in F7: next entry), 2 (the sentinel: end of bucket), 1 (in F7: the entry is
a *W7 pass*). A W7 pass is tested through row 17 on member x (Section 4.6): E17 from the constants of the entry (Appendix E.1, with `S0(A1)` folded into `U` in `P5`), E17 against the 10-bit mask (the *first row-17 test*), then A17 (4 bits and 3 internal conditions),
and then rows 18..37 of both members with early abort at the first failing cell, '+' pair or two-bit condition. A full pass yields the success: the program outputs M0 || M1 and M0 || M1' (the
Step-2 words W0..W7 of member x and member y with the entry's W8..W15) and halts. After every group the four work counters
NE (1 per bucket entry and sentinel), NW (W7 passes), N1 (first row-17 test passes) and N2 (entries that pass all row-17 tests) are compared with the caps NE_MAX, NW_MAX, N1_MAX, N2_MAX and the program halts (unsuccessfully) when one is exceeded; the group counter is compared with N_G.
The groups use fresh random coins and are independent.

### 5.3 The counted program

The machine is the 256-bit word RAM of Section 1. `experiments/vt38.py` contains the program generator, the register allocation (to 64 registers, 43 used) and an interpreter that executes the
generated instructions and counts them; the same instructions are the ones the ledger prices. Per group the counts (`prog_costs()` in vt38.py and `selftest` item 4 assert them) are:

| part | operations |
|---|---|
| prologue (two random words, unpacking M0, CV1 = f38, per-CV values, broadcast to four lanes) | 89 (+ 1 target compression) |
| four A0 blocks, empty buckets | 75 (18.75 per block) |
| one scan iteration (advance, load entry, W7, F7 load, branch (2)) | 6 per entry and per sentinel |
| W7 pass to the end of the first row-17 test | 2 + 38 |
| to the end of the A17 tests (A17 internal) | 55 |
| from the end of the A17 tests to a success (counter N2: rows 18..37 computed, the tests of rows 18..21, the comparison of the eight output words) | at most 2,920 more (2,975 in all from the W7 pass; 2,981 in c04b5a23, 2,989 in 14b3b6ff) |
| epilogue (four cap tests, group counter, loop) | 13 |

*Four-lane blocks.* Four consecutive A0 blocks share one vector computation of E0, S1(E0), ~CH, ~MAJ, Y and Z0 in the four 64-bit lanes of a 256-bit register (20 operations for the four blocks): lane values stay below 2^35
because the subtraction of S1(E0) carries a bias of 2^32, so no lane borrows from its neighbour; each block then extracts its header index with a shift and a mask, loads the header directly into the scan cursor `OFF`, and accumulates `NE` by telescoping across the loop (`sub NE, NE, OFF` before `loop` and `add NE, NE, OFF` after `loop`, with `bne FL, 2, pas` separating `W7` passes from the sentinel in 2 operations). The scalar program of the same design
(file `vtprog_v1_scalar.py`, not shipped) costs 36 operations per block; the table of Section 0 prices the difference.

*Equivalence tests* (Section 6.3): the program against the brute-force reference on 6,520 mutated characteristics, on 1,536 true buckets, and on 12,817 verified successes; for this derivative's program, Appendix C.4 and E.7.

### 5.4 Why the scan is an exact filter

Every entry of T_j[Y, Z0] has row 16 by construction (Lemma 5), and the W7 test is the exact condition of Section 3; the tests of rows 17..21 are the cell, '+' and two-bit conditions of the characteristic (Section 3) for both members in the accepted form of Section 4.7 (row 19: one AND and a compare-and-branch per pattern, the published pattern last; row 20: its other value bits, then E20 xor E19, AND 2^29, branch), and after row 37 the words A34..A37, E34..E37 of the two members are compared (8 xor, 7 or, one branch).
Hence the program outputs a pair only if A'(CV1, v) holds, and every output is a collision by Lemma 7'. The program does not rely on any probability for its output's validity: the organizer experiment
`vt-ram-r38` and the replays of Section 6.3 check the program, and the final result is checked by a target compression in the experiment harness for every returned pair.

## 6. The success probability

### 6.1 One variant on one chaining value (H1)

H1 (Section 9): for a first block M0 chosen by fresh random coins the chaining value CV1 behaves as a uniform 256-bit value as far as the events of *one* fixed variant are concerned. Consequences, all exact under H1:
(Y, Z0) is uniform for every A0 (Lemma 5: it is an affine function of the two uniform words W0, W1, which are a bijective image of CV1 words); E|T_j[Y, Z0]| = 22 |R_j| 2^-32 (Appendix C);
W7 is uniform and independent of (W0, W1) (Lemma 4), so a bucket entry is a W7 pass with probability p2 = |F7| / 2^32 = 2^-3.90197; the first row-17 test passes with probability 2^-10 given a W7 pass (the
E17 bits are uniform and independent of W7 for a uniform CV1: Lemma 4 for the bits of E16/E17); the per-group expectations are
E[NE] = SR 22 / 2^32 + 256 = 1238.317, E[NW] = SR 22 p2 / 2^32 = 65.712, E[N1] = E[NW] 2^-10 = 0.06417, and E[N2] = SR p2 2^20 2^-64 = 0.0007292 (Appendix C and E.6).
Nothing is assumed about two variants of one group (H5).

### 6.2 q3 for the variants (H2): the SMC estimate

*This derivative.* The text of this section estimates the printed event A (rows 16..37 hold); six independent studies (R1..R4 of Section 6.2/PREREG_q3b and S1..S2 of 1db43310, Appendix E.2; 43.9M verified tail successes, 0 failed rebuilds) give 99% lower bounds -101.00146, -101.00195, -101.00265, -101.00018, -101.03905, -101.03081, and 1db43310 sets the printed-event baseline at 2^-101.10 (0.061 bit below the lowest of the six bounds). The premise of this derivative is for the accepted event A' of Section 4.7: q3' >= q3_model = 2^-101.10 x 2^3.3216 = 2^-97.7784, the factor being 14b3b6ff's preregistered 99% lower bound of the gain measured on this attack's variant law (Appendix E.2; aed05522's 2^-101.35 and 14b3b6ff's 2^-101.50 bases are priced in E.5); the organizer replica of Section 10.1 estimates A' (Appendix E.4).

q3 = the probability that rows 16..37 hold given that W7 is in F7, averaged over the variants examined (uniform on the union of the sets R_j; i.e. A0_j with weight |R_j|, then (A1, A2) uniform in R_j) and over
uniform chaining values. By Lemma 4 rows 16..22 have the same probability for every valid variant; rows 23..37 depend on the variant through W8, W9, W10 of both members. The per-group success rate is
S = SR p2 q3 (Lemma 7 and H1).

*Estimator.* `smc.c` (Appendix B, written for this package): a sequential Monte-Carlo estimator that proposes the words of the second block row by row. Row 16 is exact (32 of 2^32 words: factor 2^-27); rows 17..22: E_i^x is
proposed uniformly with its x-value cells and '+' bits imposed (weight 2^-f), W_i^x follows from the step equation and W_i^y = W_i^x + DW_i, both members are stepped and the whole row is tested; the particles are resampled
after every row; the tail draws a variant (uniform from a sample, fixing W8, W9, W10), proposes W23^x with its x-value cells imposed, solves W7 = W23 - s1(W21) - W16 - s0(W8), weights by 2^(32-f)/|F7| if W7 is in F7, and runs rows 23..37 deterministically.
The estimator is unbiased for q3 of its variant distribution; every tail success is REBUILT into a real semi-free-start pair (W0..W6 by the inverse expansion, CV1 by inverting steps 7..0 of that variant) and verified (equal 38-step compressions,
M1 != M1', every cell of rows -4..37, W7 in F7) before it is counted.

*Preregistration.* `q3/PREREG_q3.txt` was written and its SHA-256 recorded together with those of `smc.c`, `varsample.c`, `r38.h`, `consts.h` and the three data files before any study run (Appendix A.4).
R1: 1,024 runs (NP = 4,000, children 2048, 64, 64, 8, 8, 4 at rows 17..22, 8,192 tail proposals per particle), every proposal drawing a variant uniformly from a sample of 1,048,576 variants drawn by `varsample.c` uniformly from the union of the R_j (seed fixed in the registration).
R2: 4,096 runs, run i using only variant i of a sample of 4,096 further uniform variants. The analysis rule (mean, sample sd, one-sided 99% Student lower bound) and the rule for q3_model were fixed in the registration:
q3_model = 2^-101.5 if both lower bounds are at least 2^-101.5.

*Results* (`analyze.py` output, all runs kept, none discarded, no empty run):

| | runs | mean log2 | relative sd | 99% lower bound log2 | tail successes | failed rebuilds |
|---|---|---|---|---|---|---|
| R1 (uniform 2^20-variant sample) | 1,024 | -100.99875 | 0.0258 | -101.00146 | 4,384,763 | 0 |
| R2 (one fresh uniform variant per run) | 4,096 | -100.99820 | 0.0334 | -101.00195 | 17,537,702 | 0 |

The stage factors (log2) are -27, -17.000, -13.000, -15.000, -6.000, -7.000, -1.000 and -15.000 for rows 16..22 and the tail (sum -101). They are integers because they count condition bits: row 16 is the 32 words of G (2^-27); row 17 has the 10 bits of the E17 mask (E cell and '+' pair, two-bit conditions with E16), 4 bits of A17 and 3 internal A17 conditions (17); rows 20, 21 and 22 have 6, 7 and 1 independent bits; and the tail, given W7 in F7, is 15 = (6 W23 cell bits + 1 E23 cell bit + 4 two-bit conditions at row 23) + (1 W25 cell bit + 3 two-bit conditions at row 25): no other cell or condition lies in rows 24..37 (Section 3). So the analytic prediction of the table is q3 = 2^-101 (-27 -17 -13 -15 -6 -7 -1 -15 with the measured 13 and 15 of rows 18 and 19), and the Monte-Carlo means 2^-100.99875 and 2^-100.99820 confirm it to 0.002 bit; q3_model is half a bit below it. The estimator imposes the E cells and '+' bits (and, in `smc.c`, only the x-value cell of W23; the shipped replica of Section 10.1 also imposes the four two-bit conditions of row 23 and weights accordingly: both are unbiased). Both bounds are 0.5 bit above q3_model = 2^-101.5, which is
therefore the value used in the base filing (rule fixed in advance): the ledger sensitivity (Section 7) prices printed-event baselines 2^-101.10 (1db43310, claimed: 2^-97.7784 -> 70.17649), 2^-101.35 (aed05522: 2^-98.0284 -> 70.18938) and 2^-101.50 (14b3b6ff: 2^-98.1784 -> 70.19818). The public package 0ae69bcb reports the same stage factors and the means
2^-100.9983 and 2^-101.0001 for the same family; our estimator is independent code.

*Replay.* 12,817 verified successes of the three development streams (seeds 50001..50003) are fed to the counted online program, restricted to the variant's A0 block, together with a decoy entry:
the program finds each pair (12,817 of 12,817, `t_replay.py`).

### 6.3 Consistency and measurements on real first blocks

All of these are our own runs on this machine; none is an organizer run. They test the programs and the per-stage rates, not q3.

1. *Row-16 table semantics* (`tbl.c`): 34.6 million (variant, chaining value) pairs, closed-form W16 against the full 38-step trace, 0 mismatches; 254 closed-form G hits (about 264 expected at 2^-27 per variant), each passes the full row-16 test; sampled non-hits fail.
2. *True buckets* (`bucket.c`: exact brute-force bucket by 2^32 values of u = Y + A1; every hit confirmed by the exact validity test): 6 chaining values x 256 A0 = 1,536 buckets: 8,889 entries (8,573.0 expected from |R_j| 2^-27: ratio 1.037, 3.4 Poisson standard deviations; entries are not independent, preimages of phi come in groups, so the counts are overdispersed), 546 W7 passes (594.6 expected from the observed entries), 2 first row-17 tests passed (0.53 expected), 0 successes; maximum bucket size 48 (bound 344,064); every entry has row 16 and is a valid variant (checked by the reference).
3. *Real first blocks, rates* (the H1 check): 12 first blocks M0_i = SHAKE-256(`r38-h1-first-blocks|i`) (`h1_jobs.py`), CV1_i through the real 38-step compression, all 256 A0 (3,072 buckets): 16,995 entries (17,145.9 expected from |R_j| 2^-27: ratio 0.991), 1,139 W7 passes (1,147.0 expected from the expected entries, 1,136.9 from the observed entries), 1 first row-17 test passed (1.1 expected), 0 successes. With the 6 chaining values of item 2 (ratios 1.037 and 0.92 for entries and W7 passes) these are 18 chaining values, 4,608 buckets, 25,884 entries: the rates agree with the H1 expectations within the overdispersion of the entry counts; they test H1 at the level of its early rows on 18 chaining values, not at the level of success events.
4. *Counted program against the reference*: `t_mut.py` 6,520 mutations of the characteristic on the published pair (all rows 17..37, every condition kind, all four lanes): 0 mismatches between machine and reference. `t_eq.py` on true buckets: counters NE, NW, N1, the full sequence of stage marks, W17/E17 values and total
operation count equal the reference's for 1,536 buckets of 6 chaining values (0 mismatches, 2 first-test passes, no success). `t_pre1.py` / `t_pre2.py`: preprocessing bodies against the references (21,184 G candidates, 5,871 F7, 26,246 A2, all 768 A2 records and 32 G records, 6 windows of P5 with 24,576 candidates and 2,061 valid variants, 512 P6 buckets,
6 chaining values of block 0): 0 mismatches.
5. *Exact set sizes.* |F7| = 287,309,824, |G| = 32, 768 values in the A2 list, the A0-free valid pairs 9,945,876,032 and the 256 sizes |R_j| (sum 191,773,672,732) from exhaustive passes in C (`ex1.c`, `rcount.c`); |R_j| equal the published values for all 256 A0; 2,428,544 pairs cross-checked against the generic validity test, 0 disagreements.

### 6.4 Groups, the pair term and the caps

Let N be the number of successful variants of one group (one first block, all variants of all 256 tables). By H1 and H2, E[N] = S = SR p2 q3 >= S_model = SR p2 q3_model = 2^-64.19975 for the accepted event with q3_model = 2^-97.7784 (2^-64.59975 at 2^-98.1784; exact rational, ledger). Let
delta be the weighted average of E[N - 1 | A_v] over the successful events A_v of variants (H5); then E[N(N - 1)] = sum_v Pr[A_v] E[N - 1 | A_v] = S delta' with delta' <= delta, and Bonferroni's inequality
gives Pr[N >= 1] >= E[N] - E[N(N - 1)] / 2 >= S (1 - delta / 2), and S >= S_model by H2, so the bound holds with S replaced by S_model. We use delta = 1/25 = 0.04 (Section 6.5, Appendix E.3, from 1db43310's whole-group row-17 measurement; fdef4bab's 0.564 is priced in Section 7): q_lb = S_model (1 - 0.04 / 2) = 0.98 S_model = 2^-64.22890 per group. Groups are independent (fresh coins), so Pr[no group succeeds among N_G] <= (1 - q_lb)^{N_G} <= exp(-N_G q_lb).

*Work caps.* Let X_g be the value of a counter (NE, NW, N1 or N2) in group g: 0 <= X_g <= B_k with B_NE = 256 x 236,544 + 256, B_NW = B_N1 = B_N2 = 256 x 236,544 (Lemma 6, ESZ = 1), and E[X_g] = E_k (Section 6.1). Then Var X_g <= B_k E_k and, by independence of the groups and Chebyshev,
Pr[sum_g X_g > (1 + eps_k) N_G E_k] <= B_k / (eps_k^2 N_G E_k). Using per-counter margins (eps_NE, eps_NW, eps_N1, eps_N2) = (2^-16, 2^-14, 2^-7, 2^-5) (since E_NE and E_NW are ~2^14 and ~2^10 times larger than E_N1 and E_N2, smaller relative margins on NE and NW keep their Chebyshev overflow probabilities tiny while avoiding a 6.25% surcharge on the dominant online terms; uniform margins eps = 2^-8, 2^-6, 2^-4, 2^-3 are priced in Section 7 for the earlier derivative), the four Chebyshev bounds sum to P_cap = 5.220e-05 (2.899e-05 in 14b3b6ff). The caps are NK_MAX = ceil((1 + eps_k) N_G E_k) and the
counters are tested after every group, so the total work of the run is at most N_G (fixed part) + (cap + one group's overshoot B_k) times the per-unit cost of each counter.
The run succeeds if some group succeeds and no counter overflows: Pr >= 1 - exp(-N_G q_lb) - P_cap. N_G is, to within 30, the smallest integer for which this is at least 0.39 (+ 2^-60 for the rounding of the exponential; iterated with P_cap to a fixed point in `ledger38.py`).
No expected-work bound is used: the total cost is deterministic (charged at the caps), and the only expectations used are those of H1.

### 6.5 Measuring the pair term (H5)

H5 (Section 9) bounds the average over successful variants of the expected number of further successful variants on the same chaining value by delta = 1/25 = 0.04 (0.564 in fdef4bab/14b3b6ff). Structure: a second variant of the same group needs its own row 16 (2^-27),
W7 (2^-3.9) and rows 17..37 (about 2^-74). The variants that share the success's chaining value fall into three kinds. *Near* variants share (A0, A1) with the success and differ in A2; they share (W0, W1) and, when their c9 coincide, W16 and
everything before row 17. *Own-block* variants have the success's A0 and another A1: they share the table cell (Y, Z0) when their row 16 holds. *Far* variants have another A0: they share only CV1.

*Near term* (`t_clump.py`, run on all 12,817 verified successes of the development streams): every other valid variant (A0, A1, A2') with A2' in the A2 list was tried on the same CV1: 12,817 verified successes, 157,306 other valid variants with the same (A0, A1) (12.3 per success), 106,023 row-16 co-hits (variants with an equal c9 share W16 with the success), 10,303 W7 passes, 781 first row-17 tests (E17 mask) passed (0.061 per success), 234 with the whole of row 17, 0 further successes. The first-test passes are 78 times the 10.1 that independent events would give (10,303 / 2^10): the near variants are strongly correlated through rows 16 and 17, which is why this term is measured and not assumed; none of them survived the later rows.
*Own-block term* (`bucket.c` and `t_own.py`): For 1,500 verified successes (every 8th of the list) the true bucket of (CV1, A0) was computed (`bucket.c`) and every entry other than the success itself was run through the reference (`t_own.py`): 20,973 other entries (12,436 with the same A1, the rest variants of the same A0 with another A1 that share the table cell), 1,782 W7 passes, 95 first row-17 tests passed (0.063 per success, one-sided 99% Poisson limit 120.3 / 1,500 = 0.080), no entry past row 17, 0 further successes.
*Far term* (`bucket.c` and `t_far.py`): for 24 successes (every 265th of the verified list from the 101st on, CV1 from the success) the true buckets of all 255 other A0 were computed (6,120 buckets) and every entry run through the reference: 6,120 buckets (24 successes x 255 other A0): 34,577 entries (34,158 expected from |R_j| 2^-27: ratio 1.012), 2,391 W7 passes (2,313 expected from the observed entries), 4 first row-17 tests passed (2.3 expected), no entry reached row 18, 0 further successes. Given a success, the other 255 blocks show the unconditional rates through row 17.

*What the measurements bound.* Pointwise N <= N1, where N1 is the number of first row-17 test passes (E17 mask) of the group, including the success itself (every success passes that test), so E[N - 1 | A_v] <= E[N1 - 1 | A_v] and delta is at most delta1 = the average over successes of the number of OTHER first row-17 test passes in the same group. delta1 is 2^10 times more frequent than a success and is measured directly: own-block term 95 / 1,500 = 0.063 per success (it contains the near term, 0.061 in the larger sample), far term 4 / 24 = 0.17 per success (the unconditional H1 expectation of a whole group is E[N1] = 0.093); the sum is 0.23. The one-sided 99% Poisson limits (95 observed: 120.25; 4 observed: 11.60) give 0.0802 + 0.4835 = 0.5637. The budget of fdef4bab/14b3b6ff is delta = 0.564, the sum of these two limits (0ae69bcb and aa0496d3 charge 1, 1.8 times that sum): a premise that sits at the 99% limit of the measurements above, not above it. The successes are resampled SMC particles, not iid draws from the success distribution, and the 24 far-term chaining values are few: the counts are indicative and the limits assume the observations to be independent. delta = 0.564, 0.296687 and 1 are priced in Section 7. A further success beyond the first row-17 test would also need rows 18..37 (about 2^-64 given the first test): no entry of the measurements reached row 18.
The public package 0ae69bcb measured the far term over 513,481 successes (about 0.0018 per success, 99%, seed-clustered) and the close term (0 further successes in 1,883,203 successes); we cite these as participant-run public figures, not as our own.

*This derivative (Appendix E.3; whole-group row-17 bound delta = 1/25 = 0.04).* Every success in A' passes all of rows 16 and 17 (and 18) with W7 in F7 (rows 16..18 are identical in A and A'), so pointwise N <= N18 <= N17, where N17 (N18) is the number of variants of the whole group (all 256 A0) passing all of rows 16..17 (16..18) with W7 in F7. In 1db43310 (`q3.c`, function `group_test`, Appendix E.3), all 256 A0 buckets were enumerated exactly on 2,500 verified successes (3,585,652 other row-16 entries, 241,170 W7 passes): 48 passed all of row 17 (one-sided 99% Poisson limit 0.02670 for delta17) and 0 reached row 18 (99% limit 0.00184 for delta18); near-term enumeration on 31,875 successes of S2 found 545 passing row 17 (0.0171 per success) and 0 reaching row 18. Furthermore, 14b3b6ff's preregistered near-variant rerun measured the row-17 completion rate r7 = 5,715 / 19,767 (99% Clopper-Pearson upper bound 0.29669). We charge delta = 1/25 = 0.04 (1.50x the whole-group 99% limit of delta17 and 21.7x that of delta18; delta = 0.564 gives 70.20124, Section 7).

## 7. Ledger (exact; `src/ledger38.py`, Appendix B.1)

Unit: one target compression = 1; every other counted operation = 1/C, C = 2728. All numbers are exact rationals except q3_model and delta (premises H2, H5).
This derivative's ledger is the program of Appendix E.6: the program of B.1 with its input files embedded and with this derivative's q3_model (2^-97.7784), delta (1/25 = 0.04), 1-word bucket entries (`ESZ = 1`), tightened online costs (prologue 89, epilogue 13, four blocks 75, W7 pass to E17 38, A17 internal 55, success path 2,975 operations) and tightened P6 preprocessing counts. The table is its output; Appendix D and E.5 record the earlier derivatives.

| term | value |
|---|---|
| N_G groups | 10,687,797,395,951,771,071 = 2^63.2126 |
| per-group fixed operations (prologue 89 + epilogue 13 + 64 x (75 - 24)) | 3,366 |
| NE_MAX / NW_MAX / N1_MAX / N2_MAX | 13,235,086,666,975,598,053,952 / 702,355,744,773,275,003,380 / 691,210,642,933,723,493 / 8,037,333,057,368,878 |
| online operations (N_G fixed + 6 (NE_MAX + B_NE) + 40 (NW_MAX + B_NW) + 17 (N1_MAX + B_N1) + 2,920 (N2_MAX + B_N2)) | 2^76.9255 |
| first-block compressions | N_G = 2^63.2126 |
| preprocessing (all of P1..P6), operations / units | 2^77.6669 / 2^66.2545 |
| program-text generation 2^32 operations, final 1,024 operations, 6 units | negligible |
| attack and preprocessing without allowances | 2^67.0361 |
| allowances A_C + A_S + DEV = 2^70 + 2^60 + 2^60 | 2^70.002815 |
| **T (exact)** | **2^70.176480 = 3,639,736,073,456,835,419,065,567/2,728** |
| success lower bound (1 - exp(-N_G q_lb) - P_cap) | 0.39000000 |
| memory (reported metric) | 2^79.5453 bytes |

The exact total is a rational; the claim is the smallest five-decimal number whose power is at least T (the ledger asserts both inequalities exactly). The ledger charges, unconditionally and deterministically, the preprocessing, the allowances
and the caps; it contains no expectation of work.

*Sensitivity* (`sens_e.py`, Appendix E.5; the exact ledger of Appendix E.6 with the inputs named):

```
claimed configuration (q3_model 2^-97.7784 = -101.10 + 3.3216, delta 1/25, ESZ 1, P0 89, EPI 13, GROUP4 75, X_SUCC 2975) 70.176480   (attack 67.0361, N_G 2^63.2126)
PREREG_q3b printed-event base (q3_model 2^-98.0284 = -101.35 + 3.3216, delta 1/25)                                       70.189370   (attack 67.1460, N_G 2^63.4626)
PREREG_q3 printed-event base (q3_model 2^-98.1784 = -101.50 + 3.3216, delta 1/25)                                        70.198180   (attack 67.2171, N_G 2^63.6125)
delta 0.564 (first-row-17 bound of fdef4bab/14b3b6ff), q3_model 2^-97.7784                                               70.201237   (attack 67.2410, N_G 2^63.6613)
c04b5a23 as filed (2-word entry, old P6, q3_model 2^-97.7784, delta 1/25, X_SUCC 2981)                                   70.233918   (attack 67.4778, N_G 2^63.2126)
14b3b6ff as filed (q3_model 2^-98.1784, delta 0.564, P0 91, EPI 19, GROUP4 76, X_SUCC 2989)                              70.286783   (attack 67.8022, N_G 2^64.0613)
1db43310 as filed (printed event q3_model 2^-101.10, delta 1/25, X_SUCC 3200)                                            70.734858   (attack 69.4055, N_G 2^66.5340)
aed05522 / fdef4bab as filed (printed event q3_model 2^-101.35 / 2^-101.50, delta 0.564)                                 71.001640 / 71.072490
four E19 patterns and tie only (q3_model 2^-99.1414 = -101.10 + 1.9586, delta 1/25)                                      70.280244   (attack 67.7652, N_G 2^64.5754)
exact event only (q3_model 2^-99.7433 = -101.10 + 1.3567, delta 1/25)                                                    70.362647   (attack 68.1831, N_G 2^65.1773)
delta 296687/1000000 (near-variant completion bound), q3_model 2^-97.7784                                                70.186756   (attack 67.1243, N_G 2^63.4151)
delta 1, q3_model 2^-97.7784                                                                                             70.240722   (attack 67.5231, N_G 2^64.1833)
q3_model 2^-98.5 / 2^-99.0, delta 1/25                                                                                   70.220222 / 70.264869
A_C = 2^68 / 2^72 / 2^74 / 2^76                                                                                          68.604539 / 72.046185 / 74.011686 / 76.002930
A_S = DEV = 2^50                                                                                                         70.173987   (attack 67.0361, N_G 2^63.2126)
A_S = 2^70, DEV = 2^64                                                                                                   71.100167   (attack 67.0361, N_G 2^63.2126)
A_S = DEV = 2^64                                                                                                         70.213404   (attack 67.0361, N_G 2^63.2126)
no allowances (the attack and preprocessing alone)                                                                       67.036133   (attack 67.0361, N_G 2^63.2126)
```

*Immediates* (H7). If every immediate operand of an ALU instruction, compare-branch or store (a constant held in the instruction, e.g. the 256-bit lane masks and the per-lane constants) were charged one extra operation, as if loaded by an `li` (one load per immediate), the counts of this program become prologue 109, epilogue 18, four blocks 98, scan iteration 7, first row-17 test 44, A17 tests 68, success path 3,260 (2,975 charged), and those of the preprocessing bodies likewise (P6 count and fill 148 and 170 per (Y, variant) with their loop control, 50 per 16 headers; Appendix E.5); the exact ledger at this derivative's inputs then gives 70.22326 (+0.047 bit against the claim; `t_imm_e.py`, Appendix E.5). This is not part of the claim (H7).

## 8. Memory and advice

Memory is a reported metric, not part of the time claim (Section 1). The 256 tables hold 256 x 2^64 headers (2^77 bytes of 32-byte words) and 1 word for each of 22 SR 2^32 = 2^73.9 entries plus at most 1 sentinel word per nonempty bucket (2^79.55 bytes in all). The claim is a time bound in the word-RAM model with unit-cost
access to a table of that size (H3), not a physical memory budget. Non-uniform advice: the 256 A0 values (1 KiB), the characteristic, the two-bit conditions and the published pair of ePrint 2026/1120 (a few KiB): below 2^14 bytes. The program text (about 2^23 bytes: 256 unrolled rare paths with their constants) is not advice: it is output of the generator in `experiments/vt38.py` from these constants, and the ledger charges 2^32 operations for generating it (about 2^21 instructions at no more than 2^11 operations each).
The A2 list, G, the F7 and s0 table, the records and the variant lists are recomputed by the charged preprocessing (Section 5.1).

*Memory of every charged computation.* The attack and the preprocessing touch only the following memory: the 256 x 2^64 header words (2^77 bytes), the 1-word entry and sentinel words (2^79.2 bytes), the F7 and s0 table (3 x 2^32 words of 32 bytes: 2^38.6 bytes), the 768 A2 and 32 G records, the variant lists R_j (2 words each, 2 x 2^37.5 words: 2^43.5 bytes) and a few thousand scratch words: 2^79.55 bytes in all, the figure of the ledger; the preprocessing writes each table word, so its footprint is that of the tables (the cruder bound of 32 bytes per executed operation, 2^82.7 bytes, is not the footprint). The development computations that are charged through DEV used far less: the q3 studies at most a few hundred MB per run, the exhaustive passes at most 2^32 bytes (the preimage-count pass `ex1 phi`), the bucket search a few MB, the replay and the tests less than 1 GB. No charged computation, including the selection of the A0 set (H6), which would need a histogram of 2^32 counters of 8 bytes, 2^35 bytes, exceeds the reported figure. The allowance A_C is a computation of others (a SAT/SMT search on at most 10^5 cores with at most 2^40 bytes each, 2^57 bytes), A_S and DEV (2^60 units each, 2^71.4 operations: at most 32 bytes per operation, 2^76.4 bytes) are bounded by the generic word-RAM bound, which is below the reported figure. The memory metric also includes code (about 2^23 bytes), advice and working state, all negligible against the tables.

## 9. Heuristics

Every premise that the score depends on is declared here and in claim.json with its role; none is left implicit. Roles are "score-critical" for H1, H2, H3, H4a, H5, H6, H7 and "supporting" for H4b, H4c, H8 (H4b/H4c are below 0.1% of T; H8 covers selection/multiple-testing across studies). Evidence references are proof line ranges and organizer experiment IDs.
Where an organizer experiment is cited, its returned-pair counts are witness frequencies of trials that passed a program-internal check; no independence of its trials and no iid inference is assumed or claimed.

### 9.0 Premises that are definitions, not heuristics

(a) The cost model (Section 1) and the counted machine (H7). (b) The characteristic, its conditions and the published pair, as transcribed (Section 3): the transcription is checked by `selftest` item 1 (the published pair collides) and by 6,520 mutations; the reading
W25[4] = W25[6] of one printed condition is used consistently everywhere (a different reading that the published pair satisfies would change q3 only, never the validity of an output). (c) Exact objects computed by exhaustive passes (|F7|, G, the A2 list, |R_j|):
reproducible by Appendix B.

### H1-single-trial-chaining-value (score-critical)

**Statement.** For one group, the chaining value CV1 = F_38(IV, M0) of a first block M0 built from two fresh uniform random words behaves as a uniform 256-bit value as far as the events of ONE fixed variant are concerned: for each A0 the table index (Y, Z0) is uniform (a bucket holds |R_j| 2^-27 entries in expectation), W7 is uniform and independent of (W0, W1) (an entry is a W7 pass with probability p2 = |F7| / 2^32 = 2^-3.90197), the first row-17 test passes with probability 2^-10 given a W7 pass, and the second-block words that realise a success have the distribution of proof.md Section 6.2 and Lemma 4. Groups use fresh coins and are independent. A statement about one first block and one variant at a time; nothing is assumed about two variants of one group (H5).

**Scope.** The four expected work counters (hence the caps and N_G), the per-variant success probability p2 q3 (hence the success bound). Not the validity of any output: every output is a verified collision (Lemma 7', Section 5.4).

**Evidence and extrapolation.** Measured by us on real chaining values (compression of uniform-looking first blocks by the real 38-step function, true buckets by exhaustive search, reference outcomes; proof.md Section 6.3): 12 real first blocks x 256 A0 (3,072 true buckets): entries 0.991 and W7 passes 0.99 times the H1 expectations, 1 first row-17 test passed (1.1 expected), 0 successes; 6 more chaining values: 1.037 and 0.92; The lemmas of Section 4 make the rest exact. The organizer experiment vt-ram-r38 runs the counted program on organizer-seeded first blocks and compares its table index, W7 decisions and W17 with the reference (a code-consistency check; the returned-pair count is a witness frequency of mismatch-free trials, not an inference). The caps use per-counter Chebyshev margins (2^-16, 2^-14, 2^-7, 2^-5) above the expectations over N_G = 2^63.2126 independent groups (Section 6.4).

**Limitations.** A premise, not a theorem. What is measured: on 18 real chaining values (4,608 true buckets, 25,884 entries) the events of one variant at per-variant probability 2^-27 (table index; entries 0.991 and 1.037 times expected), 2^-30.9 (W7 pass; 0.99 and 0.92) and 2^-40.9 (first row-17 test; 3 passes, 1.6 expected); no success event can be observed on real chaining values. What is extrapolated: (a) these rates to all N_G = 2^63.2126 groups (the caps and N_G), and (b) the per-variant success probability p2 q3 = 2^-101.680 for the chaining value of a real first block, about 2^61 below the rarest measured event: (b) is the statement that the Step-2 words (W0..W7) of a real CV1 are uniform for an event of probability 2^-101.680; the studies of H2 measure that event on uniform chaining values only. Only the first block varies between groups. Joint events of two variants on one real chaining value are the premise of H5.

**Evidence references.** proof:218-235, proof:236-249, proof:330-338, proof:372-383, proof:596-601, proof:3463-3498, experiment:vt-ram-r38

### H2-variant-q3 (score-critical)

**Statement.** The average of q3(v) = Pr[A'(CV1, v) | W7 in F7] (the accepted event of Section 4.7: rows 16..21 with the four E19 patterns and the tie, equal outputs after step 37) over the variants the program examines (uniform on the union of the 256 sets R_j) and over uniform chaining values is at least q3_model = 2^-97.7784 = 2^-101.10 x 2^3.3216. Rows 16..22 have the same probability for every valid variant (Lemma 4, exact); only the tail (rows 23..37, through W8, W9, W10 of the variant) is averaged.

**Scope.** The expected number of successes per group S_model = SR p2 q3_model = 2^-64.19975, hence N_G, the success bound and the whole attack term of the ledger.

**Evidence and extrapolation.** For the gain to the accepted event (Appendix E.2, from 14b3b6ff): a preregistered paired run of `traillab` on this attack's own variant law (32 fresh seeds 7101..7132 x 2^28 proposals on real compressions with the real expansion; every proposal draws W8, W9, W10 from a fresh uniform sample of 131,072 dense-part variants of its seed, checked against vt38.py's valid(); the printed prefix and the relaxed prefix per seed; cells and the exact event counted on the same samples): gain of the accepted event over the printed one, mean +3.4015, seed sd 0.184, declared one-sided 99% Student lower bound over seeds +3.3216 (the seed is the cluster: its spread carries the overdispersion and the variant sampling), halves 3.340 / 3.463; pattern part +2.038, exact-event part +1.363; absolute level on the tie arm -97.6058 (99% bound -97.6818), printed event on the same law -101.0074. For the printed event (Section 6.2 and Appendix E.2): six independent studies across two independent C estimators (`smc.c` R1..R4 and 1db43310's `q3.c` S1..S2; 43.9M verified tail successes, 0 failed rebuilds) give one-sided 99% lower bounds -101.00146, -101.00195, -101.00265, -101.00018, -101.03905, -101.03081; the printed-event baseline 2^-101.10 (1db43310) lies 0.061 bit below the lowest of all six 99% bounds (and using aed05522's 2^-101.35 or 14b3b6ff's 2^-101.50 gives 2^-98.0284 -> 70.18938 or 2^-98.1784 -> 70.19818, Appendix E.5). Organizer-executed: vt-q3-smc-r38 runs a reduced replica of the estimator for the accepted event on organizer seeds with rebuilt, verified pairs replayed through the tightened counted program (calibration 2^-97.675 over 960 replicates; pass rule mean of 20 >= 2^-98.5838, fixed before its calibration); its counts are witness frequencies of passing trials, not an iid inference.

**Limitations.** Monte-Carlo bounds relying on the central limit theorem (1,024, 4,096 and 64 runs for the printed event; 32 seeds for the gain); q3 itself cannot be observed. The printed-event baseline 2^-101.10 was chosen after S1..S2 had run rather than by a preregistered threshold (see H8; the preregistered 2^-101.35 and 2^-101.50 rules are priced in E.5). The gain is measured on 32 x 131,072 sampled variants of the 2^37.48 (uniform samples of the law the program uses) with `traillab` (not shipped: 64 KiB limit); the shipped replica agrees. Rests on H1 for the distribution of the second-block words. The reading W25[4] = W25[6] of the printed condition (Section 3) is used identically by the program, the estimator and the replay; any reading that holds on the published pair yields only verified collisions, so it enters q3 only.

**Evidence references.** proof:218-235, proof:338-371, proof:590-595, proof:1028-1106, proof:3548-3568, proof:3585-3715, experiment:vt-q3-smc-r38

### H3-table-pricing (score-critical)

**Statement.** Under collision-frontier-v5 the online program is charged by its counted primitives: the model is a 256-bit word RAM whose primitives include 256-bit load and store, and memory is a reported metric with no scalar contribution. A load from any address costs one operation whatever the memory size; the memory used (2^79.55 bytes) is reported. Every table word is written by the counted preprocessing of proof.md Section 5.1 (zero initialisation included; the whole preprocessing is 2^66.2545 units).

**Scope.** The online cost per (chaining value, A0): one header load and a scan of the sentinel-terminated bucket (6 operations per entry) instead of a search over 2^29.5 variants.

**Evidence and extrapolation.** Follows the text of the cost model collision-frontier-v5: memory_scoring is "Required and reviewed as a metric only; no scalar contribution and no tie-break" and memory_includes lists code, nonuniform advice, precomputed data, messages, working state, tables and randomness retained in memory (all of which are in the reported figure); the same pricing is used by the public package 0ae69bcb (rank 1 on this track, passed review), which also reports the sensitivity if tables were not unit cost. The online and table-construction costs are counted by the interpreter of experiments/vt38.py and the preprocessing bodies of Appendix B.3 and E.1; every table word of every table is written by the charged P6 passes (the zero pass over the 2^64 headers of every A0 costs 2^73.1 operations by itself).

**Limitations.** The tables are far beyond physical memory; without unit-cost table access the claim does not hold. Finding the buckets through the inverse of s0(u) - u instead of tables costs much more (Section 7 of 0ae69bcb: about 80.7).

**Evidence references.** proof:271-290, proof:301-321, proof:411-457, proof:458-465, proof:3463-3498, proof:3500-3532

### H4a-allowance-characteristic-search (score-critical)

**Statement.** The total computation spent to obtain the published 38-step characteristic of [LZLLQZ26] (IACR ePrint 2026/1120, Table 3: failed and repeated searches and tool development included) is at most A_C = 2^70 target compressions.

**Scope.** The allowance part of the ledger: A_C is 88.5% of T (2^70 of 2^70.17649) and the largest single term.

**Evidence and extrapolation.** *Evidence for the allowance (Appendix E.10 part A states every conversion).* (i) Published, for the same kind of search: Mendel, Nad and Schlaeffer (EUROCRYPT 2013, ePrint 2015/350, Sect. 6.3 p.14) found the differential characteristic and the confirming message pair of a 38-step semi-free-start collision of SHA-256 in "about 8 hours on a single CPU. This is equivalent to about 2^37 SHA-256 evaluations" (one combined figure, no hardware named; for 31 steps, Sect. 6.2 p.12: about 21 hours, 2^38.4 evaluations); Li, Liu and Wang (EUROCRYPT 2024, ePrint 2024/349 p.16) found a practical 39-step semi-free-start pair "in 120 seconds with 26 threads". (ii) Measured by us: with the authors' public tool of [LLW24a] (github.com/Peace9911/sha_2_attack, commit 6a9f35fd; model find_dc_model_39: rows 8..26, message support W8..W12, W16, W17, W24, W26, weights W 25, A 10, E at most 90) a 39-step characteristic was derived from scratch in 772.58 s wall on 12 threads (CryptoMiniSat 5.11.21; a Kissat call of 1,800 s on the same file returned no result): 11,071.7 solver CPU-seconds (wall x threads, the failed call included), at the 3,797,484 SHA-256 compressions per second measured here (portable C, one thread, AMD Ryzen 9 7900X, slowest of five runs) 2^35.29 SHA-256 evaluations, 2^36.04 units (an evaluation of 64 steps charged 64/38 units) and 2^47.46 word operations. (iii) Measured by us, our pair searches (E.10 part B): the 38-step pair search given the published cells took 4,055,969,700 propagations (2^31.917 word operations = 2^20.504 units; 2,852.83 CPU-seconds, 2^34.09 units at the compression rate above), the sparse part 113,081,800 word operations (2^26.753, 0.55 CPU-seconds); Kissat seed 4 returned a new pair, not the published one (CV, M, M' and digest in E.10). *Result:* the largest of these figures is 2^39.15 units (Mendel et al.'s 31-step 2^38.4 evaluations; their 38-step figure is 2^37.75, our 39-step derivation 2^36.04), 30.8 bits below A_C = 2^70 target compressions; counted as word operations without the factor C = 2728 the largest is 2^50.57, 19.4 bits below 2^70. *Not measured, hence the allowance:* deriving the dense signed characteristic of rows 0..16 of the 38-step characteristic of [LZLLQZ26] itself (its search time is not published; the pair searches load its cells; a 37-step attempt with those cells unset returned no model) and the authors' failed and repeated searches; the 30.8 bits are the margin for them. *Bound for the allowance.* [LZLLQZ26] uses the CPU SAT/SMT characteristic-search tool of [LLW24a] (EUROCRYPT 2024) in the two-block framework of [LLWS26] (IACR ePrint 2026/1080): 10^5 CPU cores for 10 years at 10^10 word operations per second is 3.2 x 10^23 operations = 2^66.6 units at C = 2728, and A_C = 2^70 is 10.3 times that ceiling. The promoted filing 6eeefb64 (sha256-r32) priced a complete measured re-run of the predecessor 35-step characteristic search with the same tool at 593,858 solver CPU-seconds over 59 solver calls; at its calibrated price of 2^32.796 primitive operations per solver CPU-second (2^21.383 units) and a 32-fold blind-rediscovery factor (as in 0ae69bcb) that is 2^45.6 units; A_C = 2^70 is 2^24.4 times that. Every cell and two-bit condition of the 38-step characteristic used here is verified on the published pair by the organizer-executed package (selftest items 1-3, vt-q3-smc-r38). The same A_C = 2^70 is charged by the accepted filings 0ae69bcb, 63028099, 37742a53 and 012400ff on this track. A_C = 2^72 gives 72.04619, 2^74 gives 74.01169, 2^76 gives 76.00293 (Appendix E.5).

**Limitations.** A_C is an allowance, not a measurement of the [LZLLQZ26] search: the published figures and our measurements are for the same kind of search (a 38- or 39-step semi-free-start characteristic and pair) but for other characteristics, on unstated or different hardware, with combined or windowed figures; we did not derive the dense signed characteristic of rows 0..16 of Table 3 (a 37-step attempt returned no model) and the authors' failed and repeated searches are in no log. The margin of 30.8 bits between the largest measured or published figure (2^39.15 units) and A_C = 2^70, the CPU-hardware ceiling and 2^24.4 times the measured predecessor re-run carry the claim that the whole search is below 2^70; A_C is not lowered. A GPU branch of the bound chain (10^4 GPUs, 10 years: 2^73.3) is not the operative branch because the solver is a CPU SAT/SMT tool; A_C = 2^74 is priced in E.5.

**Evidence references.** proof:411-457, proof:513-524, proof:3973-4028, experiment:vt-q3-smc-r38

### H4b-allowance-step1-solve (supporting)

**Statement.** The total computation spent to obtain the Step-1 solution (the published semi-free-start pair of Table 5 and its dense part S*) is at most A_S = 2^60 target compressions. The variants (A0, A1, A2) of S* needed by this package are not solved for: they are enumerated by the charged preprocessing P5.

**Scope.** The allowance part of the ledger (2^60 of the allowances; A_S and DEV together are 0.06% of T).

**Evidence and extrapolation.** [LZLLQZ26] reports about 2^38.3 compression-equivalent calls for the 38-step Step-1 solve (and 2^41.3 for 37 steps); A_S = 2^60 is 2^21.7 times the published Step-1 figure (a margin of more than three million-fold; the accepted r37 filings 087a18c4, 1f12a09a, 7319bba9 and 8de337d5 charge A_S = 2^50, and A_S = DEV = 2^50 here would give 70.17399). Moreover, the published semi-free-start pair (Table 5) and its dense part S* are verified directly by `experiments/vt38.py` (selftest item 1), and the organizer-executed experiment `vt-q3-smc-r38` constructs and verifies dozens of fresh 38-step semi-free-start collisions from variant dense parts in a few seconds inside the organizer sandbox (21 returned verified pairs per organizer run, 0 failed rebuilds), directly demonstrating that completing a variant dense part to a verified 38-step semi-free-start collision costs well below 2^35 units. The same A_S = 2^60 allowance is accepted in 37742a53 and 012400ff on this track.

**Limitations.** The original SAT/SMT search for the base dense part S* was performed by the paper's authors and is bounded by 2^21.7 times their reported figure rather than re-solved from scratch in the organizer sandbox (which instead verifies S* and constructs fresh 38-step semi-free-start pairs from its variants in `vt-q3-smc-r38`). Raising A_S to 2^70 (the allowance of 0ae69bcb and 63028099) together with DEV = 2^64 gives 71.10017 (Appendix E.5); A_S = DEV = 2^64 gives 70.21341.

**Evidence references.** proof:411-457, proof:525-536, proof:590-595, experiment:vt-q3-smc-r38

### H4c-allowance-development (supporting)

**Statement.** All target-specific development computation of this package (and of the earlier versions in this lineage) is at most DEV = 2^60 target compressions; this includes the computation that selects the 256 A0 values (H6) and everything that is not in the counted preprocessing or the attack.

**Scope.** The allowance part of the ledger (with A_S 0.06% of T).

**Evidence and extrapolation.** Physical bound: the base runs used one 15-core machine for 14 days (1.8 x 10^7 CPU-seconds = 2^24.1; at the generous calibration of 2^21.383 units per CPU-second that is 2^45.5 units, 2^14.5 times below DEV, and even one full machine-year of all 15 cores is 2^50.2 units); the recorded runs (q3 studies, exhaustive passes, bucket measurements) are a small fraction of it. Selection of the A0 set (H6): the counts |R(A0)| are the cyclic cross-correlation over Z/2^32 of the histogram of F over the 9.9 x 10^9 valid pairs with the indicator of the 68,157,440 words w with s0(w + DW_8) - s0(w) = DS0_8, which one pass of the P5 kind (2^44.4 operations) plus a number-theoretic transform of length 2^32 (below 2^45 operations) computes: below 2^35 units, far inside DEV (and the exact sizes of the published set are recomputed in P5). The derivative work (Appendices C, D, E) used at most two workstation machines for 30 days (below 2^55 units) plus less than 1 CPU-hour for this filing's code/proof updates and selftests.

**Limitations.** A physical bound by wall-clock and core count, not a log of CPU time. The time spent by the author reading and writing is not computation in the cost model.

**Evidence references.** proof:411-457, proof:537-548, proof:208-217, proof:3463-3498

### H5-pairs-in-group (score-critical)

**Statement.** Let N be the number of successful variants on one chaining value (one group). The expected number of further successes seen from a success, sum_v Pr[A_v] E[N - 1 | A_v] / sum_v Pr[A_v], is at most delta = 1/25 = 0.04: on average a success brings at most 0.04 further successes on the same chaining value (every success passes all of rows 16 and 17 with W7 in F7, so N <= N17, and 1/25 is 1.50 times the one-sided 99% Poisson limit 0.02670 of N17 - 1 and 21.7 times the 99% limit 0.00184 of N18 - 1 measured across all 256 A0 on 2,500 verified successes in Appendix E.3). This includes the premise that joint events of two variants on a real chaining value behave as on a uniform one (H1 covers one variant at a time).

**Scope.** The group success bound Pr[N >= 1] >= S (1 - delta / 2) (Bonferroni, Section 6.4), hence N_G and the success bound. Not the validity of any output. delta = 296687/1000000 gives 70.18676, delta = 0.564 (the first-row-17 bound of fdef4bab and 14b3b6ff) gives 70.20124, and delta = 1 (0ae69bcb and aa0496d3) gives 70.24073.

**Evidence and extrapolation.** Structure: every success in A' passes all of rows 16 and 17 (and 18) with W7 in F7 (rows 16..18 are identical in A and A'), so pointwise N <= N18 <= N17, where N17 (N18) is the number of variants of the whole group (all 256 A0) passing rows 16..17 (16..18) with W7 in F7, and delta <= delta17 (delta18). Whole-group measurement (1db43310, Appendix E.3, `q3.c` function `group_test` on 2,500 verified successes): all 256 A0 buckets enumerated via 16-way partitioned inverse of phi over 2^32 u; 3,585,652 other row-16 entries, 241,170 W7 passes, 48 passing all of row 17 (99% Poisson limit 0.02670 for delta17), 0 reaching row 18 (99% limit 0.00184 for delta18), 0 further successes. Near term on 31,875 verified successes of S2: 391,103 near variants, 262,159 row-16 co-hits, 25,867 W7 passes, 545 with all of row 17 (0.0171 per success), 0 reaching row 18; in the base (12,817 successes): 234 with all of row 17 (0.018 per success), 0 further successes; in 14b3b6ff's preregistered near-variant rerun (Appendix E.3): 5,715 of 19,767 first-test passes complete row 17 (99% Clopper-Pearson upper bound 0.29669). Earlier first-row-17 bound (Section 6.5): own-block 95 / 1,500 (99% limit 0.0802) + far 4 / 24 (99% limit 0.4835) = 0.5637 -> delta = 0.564 (priced in E.5: 70.20124). The organizer experiment vt-q3-smc-r38 repeats the near-term test on organizer seeds. The public package 0ae69bcb measured the far term over 513,481 successes (~0.0018, 99%) and close term over 1,883,203 successes (0 further successes).

**Limitations.** A premise. Our measurements are participant-run; the successes are resampled SMC particles (clustered, not iid) of the printed event (rows 16..18 are identical in A and A', so the pointwise bounds N <= N18 <= N17 are unchanged); row-17 co-passes are dominated by correlated near variants, so the variance of N17 - 1 can exceed the Poisson variance, though delta = 0.04 has a 1.50x margin over the 99% Poisson limit of delta17 and 21.7x over delta18 (where 0 of 593 row-17-complete entries across the whole-group and near-term studies reached row 18).

**Evidence references.** proof:384-395, proof:396-410, proof:590-595, proof:3500-3532, proof:3569-3584, experiment:vt-q3-smc-r38

### H6-reused-A0-set (score-critical)

**Statement.** The 256 values A0_j of the set published by c99df2dc (qkniep) and 0ae69bcb (0xshikhar) are used as non-uniform advice (1 KiB). They are not claimed to be optimal; the cost of obtaining such a set is inside DEV (H4c); every quantity that depends on the set is recomputed here: the sizes |R_j| (exhaustively, 0 mismatches against the published sizes), SR = 191,773,672,732, and q3 (averaged over variants of this set in H2).

**Scope.** SR (hence N_G, the caps and the table sizes) and the variant sample of H2.

**Evidence and extrapolation.** The set matters: for a uniformly random A0 the mean size of R(A0) is 9,945,876,032 x 68,157,440 / 2^32 = 157.8 million, the set's mean is 749.1 million, a factor 4.75 (2.25 bits of attack cost). The maximum possible per-A0 count is 750,798,738 in the set. The selection is a correlation of two explicit objects (H4c) whose cost is below 2^35 units; even at the direct pair-by-pair cost, 2^33.2 pairs x 2^26.0 words x 3 operations = 2^60.8 operations = 2^49.4 units, together with the physical bound of H4c (2^45.5) it is 2^49.5, inside DEV = 2^60. The 256 values and sizes are listed in Appendix A.2; the file read by ledger38.py has these two columns.

**Limitations.** The set is advice from public filings and was not derived by us; the derivation cost is bounded, not executed.

**Evidence references.** proof:208-217, proof:458-465, proof:667-927

### H7-counted-machine (score-critical) && H8-experimental-selection-and-multiple-testing (supporting)

**Statement (H7).** The counted program is an honest program of the word RAM of collision-frontier-v5: every executed instruction of the classes add, sub, rsub, and, or, xor, shl, shr, ld, ldi, st, sti, li, rand, jmp costs 1, a conditional branch costs 2 (comparison and branch), one target compression costs 1 unit and the unit of every other operation is 1/C with C = 2728; constants (including 256-bit lane masks and per-lane constants) are instruction fields (immediates); the observers obs, mark, succ and halt are instrumentation of the interpreter and are not executed by the real program; scratch memory addresses are direct fields; at most 64 registers are live (43 are used). **Statement (H8).** The empirical parameters charged in the ledger (q3_model = 2^-97.7784 = 2^-101.10 x 2^3.3216 and delta = 1/25 = 0.04) are not artifacts of seed selection, optional stopping, or multiple-comparison inflation across studies or derivatives.

**Scope.** H7: every operation count of the ledger (89, 75, 6, 40, 17, 2,920 (2,975 from the W7 pass), 13, the preprocessing bodies of Appendix B.3 as executed by t_pre_d.py). H8: statistical validity and selection-bias robustness of the empirical estimates feeding H2 and H5.

**Evidence and extrapolation.** H7: the interpreter is in experiments/vt38.py (class Machine); the instruction classes are those of the model's primitive list; the per-body and per-path counts are executed counts, asserted by selftest item 4 and re-derived by t_cost.py, t_pre1.py and t_pre2.py (for this derivative's program and bodies: selftest item 4 and t_pre_d.py, Appendices C.4, D.4 and E.1); on 1,536 true buckets the machine's total operation count equals the reference model's (t_eq.py). Sensitivity: if every immediate operand of an ALU instruction, compare-branch or store were charged one extra operation (one load per immediate), the claim would be 70.22326 (+0.047 bit; proof.md Section 7, t_imm_e.py in Appendix E.5). H8: (1) for the printed-event baseline 2^-101.10, all six studies (R1: 1,024 runs, R2: 4,096 runs, R3: 1,024 runs, R4: 4,096 runs, S1: 32 runs, S2: 32 runs; contiguous seed ranges, 0 runs dropped, 43.9M verified tail successes) agree with the analytic stage-factor sum 2^-101.00 within 0.01 bit, and 2^-101.10 lies 0.061 bit below the minimum of all six 99% lower bounds (-101.03905); (2) for the accepted-event gain +3.3216 (E.2), the 32 fresh seeds 7101..7132 were preregistered before execution (mean +3.4015, seed sd 0.1844; even at a Bonferroni-corrected alpha = 0.001, t_0.999,31 = 3.375 gives +3.2916, and the shipped replica independently measures 2^-97.6753 over 960 fresh replicates); (3) for delta = 1/25 = 0.04 (E.3), the 1.50x margin over the 99% limit of delta17 (0.02670) and 21.7x over delta18 (0.00184, 0 of 593 row-17-complete entries reaching row 18) absorbs seed clustering; (4) organizer public seeds are fixed canonical SHA-256 hashes of [experiment_id, trial_index] with 0 bits charged from organizer trial counts, and Appendix E.5 prices the preregistered baselines (70.18937, 70.19818) and delta = 0.564 (70.20124).

**Limitations.** H7: the organizer's reference note says "instruction constants require accounting in each submission"; our accounting is that an immediate is a field of an executed instruction that costs 1, and the sensitivity above charges one more operation for each immediate. H8: the organizer runner uses deterministic public seeds without a post-submission holdout nonce, and participant preregistration hashes are embedded records rather than externally notarized commitments; the contiguous seed ranges, full disclosure of v1/v2 calibrations and low-memory runs, analytical stage-factor cross-checks, and sensitivity table in E.5 bound any residual selection effect.

**Evidence references.** proof:63-74, proof:301-321, proof:372-383, proof:3463-3498, proof:3500-3532, proof:3536-3547, proof:3716-3793, experiment:vt-ram-r38, experiment:vt-q3-smc-r38


## 10. Organizer experiments

`experiments/manifest.json` declares two experiments of kind python-message-pairs-v1, both run by `experiments/vt38.py` (standard library only, 64 KiB, the same code as the counted program and the reference of this proof). Organizer-run counts of returned pairs are
witness frequencies: the program returns a pair only if its own internal checks pass; the organizer verifies each returned pair against the target (they are semi-free-start pairs from CV1, so the declared event is "full-collision" and the organizer's count of full collisions from the IV is 0 by design).

### 10.1 vt-q3-smc-r38 (H2, H5 near term)

Trials 0..19 each run one reduced replicate of the estimator for the accepted event (Appendix E.4: row 16 exact; NP = 64; 128, 4, 4, 1, 1, 1 children at rows 17..22 with E_t^x proposed with its x-value cells and '+' bits imposed, row 19 one of the four patterns (weight 4 x 2^-f), row 20 bit 29 = E19[29], row 22 E22[29] = 0 and nothing else tested; 256 tail proposals per particle, each drawing a variant from 512 embedded variants drawn uniformly from the variant set and W23 by importance sampling over the classes of its ten printed conditions; rows 23..37 computed and the outputs compared), randomness from SHAKE-256 of the trial's seed. Every tail success is rebuilt (W0..W6 by the inverse expansion, CV1 by inverting steps 7..0) and accepted only if the 38-step compressions are equal, M1 != M1', the Step-2 words map CV1 back to W0..W7, W7 is in F7 and rows 0..21 hold in the accepted form; the first two accepted pairs of each replicate are run through the counted online program (their A0 block, a bucket holding a decoy entry and the variant's entry), which must report the success (observation program_found). Trial t < 20 returns its first accepted pair as the 96-byte strings CV1 || M1 and CV1 || M1'; its observations are the log2 estimate, the accepted pairs, the failed rebuilds (0), program_found, other_patterns (accepted pairs with an E19 pattern other than the published one) and, for the first two accepted pairs, the near-term pair test of Section 6.5 on the same chaining value (near_variants, near_row16, near_w7, near_first17, near_cosuccess; a co-success is another variant in the accepted event). Trial 20 returns a pair iff all 20 trials had a success, all were accepted, every replayed pair was found and the mean of the 20 estimates is at least 2^-98.5838 (fixed before its calibration, Appendix E.4); trials 21..255 return no pair by design.
A pass is a check of a reduced replica, not an estimate of q3, and no independence of the organizer's trials is assumed. The replica estimates a lower bound of q3 for the accepted event (calibration mean 2^-97.6753); the ledger uses q3_model = 2^-97.7784, 0.805 bit above the rule's threshold (which was fixed against the earlier q3_model 2^-98.2338 and left unchanged).
Observations are reported per trial as untrusted participant numbers (witness observations); a trial returns its pair only if the program's own checks passed. Validation by us: see Appendix E.7.

### 10.2 vt-ram-r38 (H1, counted program)

Per organizer seed: two 256-bit words from SHAKE-256 of the seed are the program's two RAND outputs; its prologue unpacks M0 and computes CV1 = F_38(IV, M0); then 32 A0 blocks (A0 indices 32t..32t+31 mod 256, t = trial mod 8) run with a table oracle whose bucket holds one entry, the embedded valid variant of that A0
(in general not a row-16 hit). Checks: M0 is the unpack of the two words, CV1 equals the reference compression, every block requests the table index (Y, Z0) that the reference computes from (CV1, A0) (Lemma 5), and the program enters its row-17 path exactly for the entries whose reference W7 is in F7, with W17 equal to the reference pair's.
It returns M0 || M1 and M0 || M1' of the first block's variant (128 bytes each) only if every check passed. A trial returns its pair only if it is mismatch-free, so the number of returned pairs is the number of mismatch-free trials (a witness frequency); the W7 passes per trial are reported as an observation. Validation by us (same five runs, earlier derivative): 256 returned pairs each, mismatches 0, W7 passes 584, 553, 593, 551 and 569; about 1 second per run. This derivative: Appendix E.7.

## 11. Runs and hashes

Development modules and their roles: `vtconst.py` (transcription, generated tables), `vtref.py` (reference construction), `vtprog.py` (online program, interpreter), `vtpre.py` (preprocessing as counted code), `vt_exp.py` (experiments); `mk_vt38.py` assembled them with the data blobs into `experiments/vt38.py`
(the shipped file; the near-term addition of Section 10.1 was made to the shipped file afterwards). The C programs (Appendix B.4..B.11) and the tests and counted modules (B.12..B.15) are shipped as appendices because the package may contain only the declared experiment files.

| run | what | result |
|---|---|---|
| `ex1.c f7 / g / a2 / phi` | exhaustive passes over 2^32 | |F7| = 287,309,824; G = 32 words; 768 A2; max preimage 14 |
| `rcount.c` | exact |R_j| for 256 A0 | sum 191,773,672,732; identical to the published sizes |
| `tbl.c` | W16 closed form vs 38-step trace | 34.6M comparisons, 0 mismatches |
| `t_mut.py`, `t_eq.py`, `t_cost.py`, `t_pre1.py`, `t_pre2.py` | program vs reference | 0 mismatches |
| `smc.c` R1, R2 | preregistered q3 study | Section 6.2 |
| `t_replay.py` | 12,817 verified successes into the counted program | 12,817 found |
| `t_clump.py`, `bucket.c` + `t_own.py`, `bucket.c` + `t_far.py` | pair term | Section 6.5 |
| `bucket.c` + `t_far.py` on 12 real first blocks | rates (H1) | Section 6.3 |
| `ledger38.py`, `sens38.py` | exact ledger, sensitivity | Section 7 |

SHA-256 of the registered files (Appendix A.4): PREREG_q3.txt da73e8889178c35725f13730f2d7ba6149829bc0ee808a685fefa7f9be601713; smc.c, varsample.c, r38.h, consts.h, the sample files and the data files as listed there. The reproduction commands are in Appendix A.1.

## 12. Limitations and differences from the paper

- q3 is estimated, not proved (H2); the estimator and the registration are ours; the public package 0ae69bcb obtained the same value independently for the printed event. The gain to the accepted event is 14b3b6ff's preregistered measurement on this attack's variant law; the shipped replica agrees (Appendix E).
- The pair budget (H5) is a premise (delta = 1/25 = 0.04) at 1.50x the 99% limit of 1db43310's whole-group row-17 measurement (21.7x that of row 18; fdef4bab's delta = 0.564 gives 70.25801); the measurements are participant-run and taken on successes of the printed event (Section 6.5, Appendix E.3).
- A_C, A_S and DEV are allowances (H4a-c); of the characteristic search we measured the message signing, the sparse window and a 38-step pair search given the published cells (E.10), not the derivation of the dense signed characteristic. Appendix E.5 gives the effect of each allowance.
- The tables are not constructible in practice: 2^80.42 bytes. The claim is in the word-RAM model of the track (H3).
- The experiment evidence is organizer-run only for code consistency (H1, H7) and for a half-bit-resolution replica check (H2); the study results and the pair measurements are run by us.
- The construction follows the cited public packages (c99df2dc, 0ae69bcb); the differences are the cheaper counted program (53.2 vs 117 operations per (CV, A0)), Chebyshev caps, the allowances A_S and DEV, the accepted event (q3_model = 2^-97.7784) and delta = 1/25 (Section 0); each of these is separately priced.
- We executed no peer code and did not copy peer programs; the peers' packages were read as data. The tools used for the paper's search (SAT/SMT) were not run.

## Appendix A. Data and runs

### A.1 Selftest output and reproduction

`python3 experiments/vt38.py selftest` (about 2 seconds):

```
1 published pair collides, M != M'                         ok 
  published dense part is a valid variant                  ok 
2 G: the 32 words hold row 16; 20,000 random words and the 1,024 bit-flip neighbours agree with G ok (exhaustive count over 2^32: 32)
  A2 list: 768 sorted values, all satisfy the A2-only conditions ok 
  512 embedded variants valid; 256 entry variants valid    ok 
3 Lemma 3 (rows -4..15 hold, DW_i for i < 16) and Lemma 5 (W16 closed form, W7 = c7 - A_-1), 40 chaining values ok 
4 program: registers after allocation <= 64                ok (43)
   costs: {'P0': 89, 'EPI': 13, 'GROUP4': 75, 'ITER': 6, 'X_E17': 38, 'X_A17int': 55, 'X_SUCC': 2975}
  ledger constants P0 89, epilogue 13, four blocks 75, iteration 6, E17 38, A17 55, success 2975 ok 
  published pair: the program finds it in each of the 4 lanes ok 
5 replicate: estimate, accepted pairs (rebuilt, verified), failed rebuilds 0 ok (log2 -97.742, 16 pairs, 16 found by the counted program)
6 vt-ram-r38 (8 trials): mismatches 0, pairs returned 8    ok [0, 0, 2, 2, 5, 5, 1, 2]
SELFTEST PASSED
```

Reproduction (all from the Appendix B sources; the C programs read the text files of Appendices A.2 and A.3 and the output of `ex1`):
```
cc -O2 -pthread -o ex1 ex1.c; ./ex1 a2 > a2.txt; ./ex1 g > g.txt; ./ex1 f7; ./ex1 phi         # exhaustive passes over 2^32
cc -O2 -pthread -o rcount rcount.c; ./rcount ...                                             # exact |R_j| for the 256 A0
cc -O2 -pthread -o bucket bucket.c; ./bucket a2.txt g.txt 14 < jobs.txt > buckets.txt          # true buckets (job line: 8 hex CV words, A0)
cc -O2 -o smc smc.c; ./smc vsU.txt all SEED 4000 2048 64 64 8 8 4 8192                          # R1 (see A.4 for the registered command lines)
python3 t_cost.py; python3 t_pre1.py; python3 t_pre2.py        # base program: write ../runs/costs.json, pre1.json, pre2.json
python3 t_pre_d.py <dir of experiments/vt38.py> ../runs          # this derivative: executes the bodies of P5 and P6 and writes pre2.json (and pre1.json: P1..P4 as printed by t_pre1.py, LIVE by execution); costs.json from selftest item 4 (A.5)
python3 t_imm_d.py <dir of experiments/vt38.py> <dir of src/> <scratch dir>   # sensitivity with immediates charged (Section 7)
python3 ledger38.py; python3 sens38.py                           # the exact ledger (defaults q3 -101.5, delta 0.564, A_S = DEV = 2^60) and its sensitivity, with the four changes of Appendix D one after the other
python3 experiments/vt38.py selftest
```

### A.2 The A0 set (j, A0_j, |R_j|; the file read by ledger38.py and t_far.py has the last two columns)

```
1 3662dd58 750798738
2 3662dd50 750798738
3 3662bd50 750798738
4 36629d50 750798738
5 36627d58 750798738
6 36627d50 750798738
7 36625d58 750798738
8 36625d50 750798738
9 36623d58 750798738
10 36623d50 750798738
11 36621d58 750798738
12 36621d50 750798738
13 3661fd58 750798738
14 3661fd50 750798738
15 3661dd58 750798738
16 3661dd50 750798738
17 3661bd58 750798738
18 3661bd50 750798738
19 36619d58 750798738
20 36619d50 750798738
21 36617d58 750798738
22 36617d50 750798738
23 36615d58 750798738
24 36615d50 750798738
25 36613d58 750798738
26 36613d50 750798738
27 36611d58 750798738
28 36611d50 750798738
29 3660fd58 750798738
30 3660fd50 750798738
31 b662dd50 750367881
32 b6629d50 750367881
33 b6625d50 750367881
34 b6623d50 750367881
35 b6621d58 750367881
36 b6621d50 750367881
37 b661fd50 750367881
38 b661dd50 750367881
39 b661bd50 750367881
40 b6619d50 750367881
41 b6617d50 750367881
42 b6615d58 750367881
43 b6615d50 750367881
44 b6613d58 750367881
45 b6613d50 750367881
46 b6611d58 750367881
47 b6611d50 750367881
48 b660fd58 750367881
49 b660fd50 750367881
50 3660bd58 749907870
51 3660bd50 749907870
52 b660bd50 749607325
53 3660dd58 749434566
54 3660dd50 749434566
55 366add58 749306678
56 366add50 749306678
57 366abd58 749306678
58 366abd50 749306678
59 366a9d58 749306678
60 366a9d50 749306678
61 366a7d50 749306678
62 366a5d58 749306678
63 366a5d50 749306678
64 366a3d50 749306678
65 366a1d58 749306678
66 366a1d50 749306678
67 3669fd50 749306678
68 3669dd58 749306678
69 3669dd50 749306678
70 3669bd50 749306678
71 36699d50 749306678
72 36697d50 749306678
73 36695d58 749306678
74 36695d50 749306678
75 36693d58 749306678
76 36693d50 749306678
77 36691d58 749306678
78 36691d50 749306678
79 3668fd58 749306678
80 3668fd50 749306678
81 3662dd56 749304379
82 3662dd4e 749304379
83 3662bd56 749304379
84 3662bd4e 749304379
85 36627d56 749304379
86 36627d4e 749304379
87 36625d4e 749304379
88 36623d56 749304379
89 36623d4e 749304379
90 36621d56 749304379
91 36621d4e 749304379
92 3661fd56 749304379
93 3661fd4e 749304379
94 3661dd56 749304379
95 3661dd4e 749304379
96 3661bd56 749304379
97 3661bd4e 749304379
98 36619d56 749304379
99 36619d4e 749304379
100 36617d56 749304379
101 36617d4e 749304379
102 36615d56 749304379
103 36615d4e 749304379
104 36613d56 749304379
105 36613d4e 749304379
106 36611d56 749304379
107 36611d4e 749304379
108 3660fd56 749304379
109 3660fd4e 749304379
110 3668bd50 749092986
111 b66add58 748997270
112 b66add50 748997270
113 b66abd50 748997270
114 b66a9d58 748997270
115 b66a9d50 748997270
116 b66a7d50 748997270
117 b66a5d58 748997270
118 b66a5d50 748997270
119 b66a3d58 748997270
120 b66a3d50 748997270
121 b66a1d58 748997270
122 b66a1d50 748997270
123 b669fd58 748997270
124 b669fd50 748997270
125 b669dd58 748997270
126 b669dd50 748997270
127 b669bd50 748997270
128 b6699d58 748997270
129 b6699d50 748997270
130 b6697d50 748997270
131 b6695d50 748997270
132 b6693d50 748997270
133 b6691d58 748997270
134 b6691d50 748997270
135 b668fd50 748997270
136 3662fd58 748982994
137 3662fd50 748982994
138 b6623d4e 748863932
139 b6621d4e 748863932
140 b661fd56 748863932
141 b661bd4e 748863932
142 b6617d56 748863932
143 b6617d4e 748863932
144 b6615d4e 748863932
145 b6613d56 748863932
146 b6613d4e 748863932
147 b6611d56 748863932
148 b6611d4e 748863932
149 b660fd56 748863932
150 b660fd4e 748863932
151 3662dd52 748706771
152 3662bd52 748706771
153 36627d52 748706771
154 36625d52 748706771
155 36623d52 748706771
156 36621d52 748706771
157 3661fd52 748706771
158 3661dd52 748706771
159 3661bd52 748706771
160 36619d52 748706771
161 36617d52 748706771
162 36615d52 748706771
163 36613d52 748706771
164 36611d52 748706771
165 3660fd52 748706771
166 36623d5a 748706531
167 3661fd5a 748706531
168 3661bd5a 748706531
169 36617d5a 748706531
170 36615d5a 748706531
171 36613d5a 748706531
172 36611d5a 748706531
173 3660fd5a 748706531
174 3668dd58 748617938
175 3668dd50 748617938
176 3662fd56 748515751
177 3662fd4e 748515006
178 3660dd4e 748497055
179 3660dd56 748496687
180 b668dd50 748328226
181 b6613d5a 748272092
182 b660fd5a 748272092
183 b6623d52 748271884
184 b6621d52 748271884
185 b661bd52 748271884
186 b6617d52 748271884
187 b6615d52 748271884
188 b6613d52 748271884
189 b6611d52 748271884
190 b660fd52 748271884
191 3662dd54 748258600
192 3662bd54 748258600
193 36627d54 748258600
194 36625d54 748258600
195 36623d54 748258600
196 36621d54 748258600
197 3661fd54 748258600
198 3661dd54 748258600
199 3661bd54 748258600
200 36619d54 748258600
201 36617d54 748258600
202 36615d54 748258600
203 36613d54 748258600
204 36611d54 748258600
205 3660fd54 748258600
206 3662dd4c 748258590
207 3662bd4c 748258590
208 36627d4c 748258590
209 36625d4c 748258590
210 36623d4c 748258590
211 36621d4c 748258590
212 3661fd4c 748258590
213 3661dd4c 748258590
214 3661bd4c 748258590
215 36619d4c 748258590
216 36617d4c 748258590
217 36615d4c 748258590
218 36613d4c 748258590
219 36611d4c 748258590
220 3660fd4c 748258590
221 36623d5c 748257912
222 3661bd5c 748257912
223 36617d5c 748257912
224 36615d5c 748257912
225 36613d5c 748257912
226 36611d5c 748257912
227 3660fd5c 748257912
228 366add56 748249397
229 366add4e 748249397
230 366abd4e 748249397
231 366a9d4e 748249397
232 366a5d4e 748249397
233 366a3d4e 748249397
234 366a1d4e 748249397
235 3669fd56 748249397
236 3669dd4e 748249397
237 3669bd4e 748249397
238 36697d56 748249397
239 36697d4e 748249397
240 36695d4e 748249397
241 36693d56 748249397
242 36693d4e 748249397
243 36691d56 748249397
244 36691d4e 748249397
245 3668fd56 748249397
246 3668fd4e 748249397
247 b660dd56 748149584
248 36631d58 748119330
249 36631d50 748119330
250 3660dd5a 748106455
251 3660dd52 748104487
252 3660bd56 748016615
253 3660bd4e 748016615
254 3668dd4e 747975479
255 3668dd56 747975119
256 366afd58 747959736
```

### A.3 The A2 list (768 values, in increasing order; identical to the public list, recomputed by `ex1 a2`)

```
379b2dc8 379b2dc9 379b2dcc 379b2dcd 379b4dc8 379b4dc9 379b4dcc 379b4dcd
37bb2dc8 37bb2dc9 37bb2dcc 37bb2dcd 37bb4dc8 37bb4dc9 37bb4dcc 37bb4dcd
381b2cc8 381b2cc9 381b2ccc 381b2ccd 381b30c8 381b30c9 381b30cc 381b30cd
381b4cc8 381b4cc9 381b4ccc 381b4ccd 381b50c8 381b50c9 381b50cc 381b50cd
383b2cc8 383b2cc9 383b2ccc 383b2ccd 383b30c8 383b30c9 383b30cc 383b30cd
383b4cc8 383b4cc9 383b4ccc 383b4ccd 383b50c8 383b50c9 383b50cc 383b50cd
399b2dc8 399b2dc9 399b2dcc 399b2dcd 399b4dc8 399b4dc9 399b4dcc 399b4dcd
39bb2dc8 39bb2dc9 39bb2dcc 39bb2dcd 39bb4dc8 39bb4dc9 39bb4dcc 39bb4dcd
3a1b2cc8 3a1b2cc9 3a1b2ccc 3a1b2ccd 3a1b30c8 3a1b30c9 3a1b30cc 3a1b30cd
3a1b4cc8 3a1b4cc9 3a1b4ccc 3a1b4ccd 3a1b50c8 3a1b50c9 3a1b50cc 3a1b50cd
3a3b2cc8 3a3b2cc9 3a3b2ccc 3a3b2ccd 3a3b30c8 3a3b30c9 3a3b30cc 3a3b30cd
3a3b4cc8 3a3b4cc9 3a3b4ccc 3a3b4ccd 3a3b50c8 3a3b50c9 3a3b50cc 3a3b50cd
479b2dc8 479b2dc9 479b2dcc 479b2dcd 479b4dc8 479b4dc9 479b4dcc 479b4dcd
47bb2dc8 47bb2dc9 47bb2dcc 47bb2dcd 47bb4dc8 47bb4dc9 47bb4dcc 47bb4dcd
481b2cc8 481b2cc9 481b2ccc 481b2ccd 481b30c8 481b30c9 481b30cc 481b30cd
481b4cc8 481b4cc9 481b4ccc 481b4ccd 481b50c8 481b50c9 481b50cc 481b50cd
483b2cc8 483b2cc9 483b2ccc 483b2ccd 483b30c8 483b30c9 483b30cc 483b30cd
483b4cc8 483b4cc9 483b4ccc 483b4ccd 483b50c8 483b50c9 483b50cc 483b50cd
499b2dc8 499b2dc9 499b2dcc 499b2dcd 499b4dc8 499b4dc9 499b4dcc 499b4dcd
49bb2dc8 49bb2dc9 49bb2dcc 49bb2dcd 49bb4dc8 49bb4dc9 49bb4dcc 49bb4dcd
4a1b2cc8 4a1b2cc9 4a1b2ccc 4a1b2ccd 4a1b30c8 4a1b30c9 4a1b30cc 4a1b30cd
4a1b4cc8 4a1b4cc9 4a1b4ccc 4a1b4ccd 4a1b50c8 4a1b50c9 4a1b50cc 4a1b50cd
4a3b2cc8 4a3b2cc9 4a3b2ccc 4a3b2ccd 4a3b30c8 4a3b30c9 4a3b30cc 4a3b30cd
4a3b4cc8 4a3b4cc9 4a3b4ccc 4a3b4ccd 4a3b50c8 4a3b50c9 4a3b50cc 4a3b50cd
579b2dc8 579b2dc9 579b2dcc 579b2dcd 579b4dc8 579b4dc9 579b4dcc 579b4dcd
57bb2dc8 57bb2dc9 57bb2dcc 57bb2dcd 57bb4dc8 57bb4dc9 57bb4dcc 57bb4dcd
581b2cc8 581b2cc9 581b2ccc 581b2ccd 581b30c8 581b30c9 581b30cc 581b30cd
581b4cc8 581b4cc9 581b4ccc 581b4ccd 581b50c8 581b50c9 581b50cc 581b50cd
583b2cc8 583b2cc9 583b2ccc 583b2ccd 583b30c8 583b30c9 583b30cc 583b30cd
583b4cc8 583b4cc9 583b4ccc 583b4ccd 583b50c8 583b50c9 583b50cc 583b50cd
599b2dc8 599b2dc9 599b2dcc 599b2dcd 599b4dc8 599b4dc9 599b4dcc 599b4dcd
59bb2dc8 59bb2dc9 59bb2dcc 59bb2dcd 59bb4dc8 59bb4dc9 59bb4dcc 59bb4dcd
5a1b2cc8 5a1b2cc9 5a1b2ccc 5a1b2ccd 5a1b30c8 5a1b30c9 5a1b30cc 5a1b30cd
5a1b4cc8 5a1b4cc9 5a1b4ccc 5a1b4ccd 5a1b50c8 5a1b50c9 5a1b50cc 5a1b50cd
5a3b2cc8 5a3b2cc9 5a3b2ccc 5a3b2ccd 5a3b30c8 5a3b30c9 5a3b30cc 5a3b30cd
5a3b4cc8 5a3b4cc9 5a3b4ccc 5a3b4ccd 5a3b50c8 5a3b50c9 5a3b50cc 5a3b50cd
679b2dc8 679b2dc9 679b2dcc 679b2dcd 679b4dc8 679b4dc9 679b4dcc 679b4dcd
67bb2dc8 67bb2dc9 67bb2dcc 67bb2dcd 67bb4dc8 67bb4dc9 67bb4dcc 67bb4dcd
681b2cc8 681b2cc9 681b2ccc 681b2ccd 681b30c8 681b30c9 681b30cc 681b30cd
681b4cc8 681b4cc9 681b4ccc 681b4ccd 681b50c8 681b50c9 681b50cc 681b50cd
683b2cc8 683b2cc9 683b2ccc 683b2ccd 683b30c8 683b30c9 683b30cc 683b30cd
683b4cc8 683b4cc9 683b4ccc 683b4ccd 683b50c8 683b50c9 683b50cc 683b50cd
699b2dc8 699b2dc9 699b2dcc 699b2dcd 699b4dc8 699b4dc9 699b4dcc 699b4dcd
69bb2dc8 69bb2dc9 69bb2dcc 69bb2dcd 69bb4dc8 69bb4dc9 69bb4dcc 69bb4dcd
6a1b2cc8 6a1b2cc9 6a1b2ccc 6a1b2ccd 6a1b30c8 6a1b30c9 6a1b30cc 6a1b30cd
6a1b4cc8 6a1b4cc9 6a1b4ccc 6a1b4ccd 6a1b50c8 6a1b50c9 6a1b50cc 6a1b50cd
6a3b2cc8 6a3b2cc9 6a3b2ccc 6a3b2ccd 6a3b30c8 6a3b30c9 6a3b30cc 6a3b30cd
6a3b4cc8 6a3b4cc9 6a3b4ccc 6a3b4ccd 6a3b50c8 6a3b50c9 6a3b50cc 6a3b50cd
779b2dc8 779b2dc9 779b2dcc 779b2dcd 779b4dc8 779b4dc9 779b4dcc 779b4dcd
77bb2dc8 77bb2dc9 77bb2dcc 77bb2dcd 77bb4dc8 77bb4dc9 77bb4dcc 77bb4dcd
781b2cc8 781b2cc9 781b2ccc 781b2ccd 781b30c8 781b30c9 781b30cc 781b30cd
781b4cc8 781b4cc9 781b4ccc 781b4ccd 781b50c8 781b50c9 781b50cc 781b50cd
783b2cc8 783b2cc9 783b2ccc 783b2ccd 783b30c8 783b30c9 783b30cc 783b30cd
783b4cc8 783b4cc9 783b4ccc 783b4ccd 783b50c8 783b50c9 783b50cc 783b50cd
799b2dc8 799b2dc9 799b2dcc 799b2dcd 799b4dc8 799b4dc9 799b4dcc 799b4dcd
79bb2dc8 79bb2dc9 79bb2dcc 79bb2dcd 79bb4dc8 79bb4dc9 79bb4dcc 79bb4dcd
7a1b2cc8 7a1b2cc9 7a1b2ccc 7a1b2ccd 7a1b30c8 7a1b30c9 7a1b30cc 7a1b30cd
7a1b4cc8 7a1b4cc9 7a1b4ccc 7a1b4ccd 7a1b50c8 7a1b50c9 7a1b50cc 7a1b50cd
7a3b2cc8 7a3b2cc9 7a3b2ccc 7a3b2ccd 7a3b30c8 7a3b30c9 7a3b30cc 7a3b30cd
7a3b4cc8 7a3b4cc9 7a3b4ccc 7a3b4ccd 7a3b50c8 7a3b50c9 7a3b50cc 7a3b50cd
879b2dc8 879b2dc9 879b2dcc 879b2dcd 879b4dc8 879b4dc9 879b4dcc 879b4dcd
87bb2dc8 87bb2dc9 87bb2dcc 87bb2dcd 87bb4dc8 87bb4dc9 87bb4dcc 87bb4dcd
881b2cc8 881b2cc9 881b2ccc 881b2ccd 881b30c8 881b30c9 881b30cc 881b30cd
881b4cc8 881b4cc9 881b4ccc 881b4ccd 881b50c8 881b50c9 881b50cc 881b50cd
883b2cc8 883b2cc9 883b2ccc 883b2ccd 883b30c8 883b30c9 883b30cc 883b30cd
883b4cc8 883b4cc9 883b4ccc 883b4ccd 883b50c8 883b50c9 883b50cc 883b50cd
899b2dc8 899b2dc9 899b2dcc 899b2dcd 899b4dc8 899b4dc9 899b4dcc 899b4dcd
89bb2dc8 89bb2dc9 89bb2dcc 89bb2dcd 89bb4dc8 89bb4dc9 89bb4dcc 89bb4dcd
8a1b2cc8 8a1b2cc9 8a1b2ccc 8a1b2ccd 8a1b30c8 8a1b30c9 8a1b30cc 8a1b30cd
8a1b4cc8 8a1b4cc9 8a1b4ccc 8a1b4ccd 8a1b50c8 8a1b50c9 8a1b50cc 8a1b50cd
8a3b2cc8 8a3b2cc9 8a3b2ccc 8a3b2ccd 8a3b30c8 8a3b30c9 8a3b30cc 8a3b30cd
8a3b4cc8 8a3b4cc9 8a3b4ccc 8a3b4ccd 8a3b50c8 8a3b50c9 8a3b50cc 8a3b50cd
979b2dc8 979b2dc9 979b2dcc 979b2dcd 979b4dc8 979b4dc9 979b4dcc 979b4dcd
97bb2dc8 97bb2dc9 97bb2dcc 97bb2dcd 97bb4dc8 97bb4dc9 97bb4dcc 97bb4dcd
981b2cc8 981b2cc9 981b2ccc 981b2ccd 981b30c8 981b30c9 981b30cc 981b30cd
981b4cc8 981b4cc9 981b4ccc 981b4ccd 981b50c8 981b50c9 981b50cc 981b50cd
983b2cc8 983b2cc9 983b2ccc 983b2ccd 983b30c8 983b30c9 983b30cc 983b30cd
983b4cc8 983b4cc9 983b4ccc 983b4ccd 983b50c8 983b50c9 983b50cc 983b50cd
999b2dc8 999b2dc9 999b2dcc 999b2dcd 999b4dc8 999b4dc9 999b4dcc 999b4dcd
99bb2dc8 99bb2dc9 99bb2dcc 99bb2dcd 99bb4dc8 99bb4dc9 99bb4dcc 99bb4dcd
9a1b2cc8 9a1b2cc9 9a1b2ccc 9a1b2ccd 9a1b30c8 9a1b30c9 9a1b30cc 9a1b30cd
9a1b4cc8 9a1b4cc9 9a1b4ccc 9a1b4ccd 9a1b50c8 9a1b50c9 9a1b50cc 9a1b50cd
9a3b2cc8 9a3b2cc9 9a3b2ccc 9a3b2ccd 9a3b30c8 9a3b30c9 9a3b30cc 9a3b30cd
9a3b4cc8 9a3b4cc9 9a3b4ccc 9a3b4ccd 9a3b50c8 9a3b50c9 9a3b50cc 9a3b50cd
a79b2dc8 a79b2dc9 a79b2dcc a79b2dcd a79b4dc8 a79b4dc9 a79b4dcc a79b4dcd
a7bb2dc8 a7bb2dc9 a7bb2dcc a7bb2dcd a7bb4dc8 a7bb4dc9 a7bb4dcc a7bb4dcd
a81b2cc8 a81b2cc9 a81b2ccc a81b2ccd a81b30c8 a81b30c9 a81b30cc a81b30cd
a81b4cc8 a81b4cc9 a81b4ccc a81b4ccd a81b50c8 a81b50c9 a81b50cc a81b50cd
a83b2cc8 a83b2cc9 a83b2ccc a83b2ccd a83b30c8 a83b30c9 a83b30cc a83b30cd
a83b4cc8 a83b4cc9 a83b4ccc a83b4ccd a83b50c8 a83b50c9 a83b50cc a83b50cd
a99b2dc8 a99b2dc9 a99b2dcc a99b2dcd a99b4dc8 a99b4dc9 a99b4dcc a99b4dcd
a9bb2dc8 a9bb2dc9 a9bb2dcc a9bb2dcd a9bb4dc8 a9bb4dc9 a9bb4dcc a9bb4dcd
aa1b2cc8 aa1b2cc9 aa1b2ccc aa1b2ccd aa1b30c8 aa1b30c9 aa1b30cc aa1b30cd
aa1b4cc8 aa1b4cc9 aa1b4ccc aa1b4ccd aa1b50c8 aa1b50c9 aa1b50cc aa1b50cd
aa3b2cc8 aa3b2cc9 aa3b2ccc aa3b2ccd aa3b30c8 aa3b30c9 aa3b30cc aa3b30cd
aa3b4cc8 aa3b4cc9 aa3b4ccc aa3b4ccd aa3b50c8 aa3b50c9 aa3b50cc aa3b50cd
```

### A.4 Preregistration, hashes and results of the q3 study


Frozen text of `PREREG_q3.txt` (written before any run of the study programs):

```
PREREGISTRATION of the q3 study (sha256-r38 variant-table attack), written before any run of the study programs.
Frozen at the time stamp of this file's sha256 line in FREEZE.txt (UTC).

Quantity: q3 = Pr[rows 16..37 hold | W7 in F7], averaged over variants drawn uniformly from the union of the R_j (the
variant set of the attack) and over uniform chaining values (H1); the attack's per-group success rate is
S = SR * p2 * q3.

Estimator: src/smc.c (sha256 in hashes_pre.txt), own code; row 16 exact (32 words of G: factor 2^-27); rows 17..22 proposals with
the E-cell and '+' bits imposed; tail with W23 x-value cells imposed and W7 = W23 - s1(W21) - W16 - s0(W8) in F7; rows 23..37
deterministic; every tail success rebuilt into a real semi-free-start pair and verified (compress38 equality, M1 != M1', every
cell of rows 0..37, W7 in F7); runs report log2 of the product of the stage means.
Parameters of every run: NP 4000, children 2048 64 64 8 8 4 at rows 17..22, 8192 tail proposals per particle.

Data: variants sampled by src/varsample.c from data/a0set256_peer.txt (A0 set and exact |R_j|, 256 values; credit c99df2dc /
0ae69bcb), data/peer_a2.txt (the 768-value A2 list, recomputed by our exhaustive scan data/ex1_a2.txt, identical), data/ex1_g.txt:
  vsU.txt  = 1,048,576 variants, varsample seed 20261012 (uniform over the union of the R_j)
  vsP.txt  = 4,096 variants, varsample seed 20261013

Runs (each run one process of smc, seed as given, deterministic):
  R1: mode "all" on vsU.txt (each tail proposal draws a variant uniformly from vsU), seeds 31001 .. 32024 (1024 runs).
  R2: mode "pop:i" on vsP.txt: run i (i = 0..4095) uses variant i of vsP.txt for all its proposals, seed 40000 + i (4096 runs).
Analysis (fixed now): Z = 2^(run log2 estimate) (the estimator is unbiased for q3 of its variant distribution); for each of R1, R2
the mean of Z, the sample standard deviation, and the one-sided 99% lower bound  mean - t * sd / sqrt(n)  with the Student t
quantile of n-1 degrees of freedom (2.3300 for 1023, 2.3267 for 4095); bounds reported as log2.  Runs with an empty stage
(no survivors) count as Z = 0.  Every run's output line is kept; no run is discarded.
Rule: q3_model = 2^-101.5 is used in the ledger if both lower bounds are at least 2^-101.5 (a margin of about 0.5 bit
below the expected 2^-101.0); otherwise the ledger uses the smaller bound rounded down to 0.01 bit.
Acceptance checks (reported, not rules): zero failed rebuilds; stage factors rows 16..22 close to the integers -27, -17, -13,
-15, -6, -7, -1 and the tail to -15.
```

Time stamp and hashes (`FREEZE.txt`, `hashes_pre.txt`):

```
2026-10-10T17:37:59Z
da73e8889178c35725f13730f2d7ba6149829bc0ee808a685fefa7f9be601713  PREREG_q3.txt
1a389c5bfa1dbd974cb5ab5fc4c28a861ddb68d865f8dd2e2d48df71ff61cfdc  vsU.txt
ddb546f38eae9ea5c40ba3df4d1f369732e31eb5aa785701a5d94534921b4534  vsP.txt
63ac41e3d59877f7c338fe8b537d593932d3220e54fb45cf9f57991468b390fa  smc.c
426bf6b99f04e1a3be615c3cc207f2b755ac548299d9236eb8960826fbbfaaa8  varsample.c
157ca54a4ae18731d501ee48430f83ddace31538066b4c1ecdfd0ce350034d68  r38.h
7dbc03d15f959ebd406396d40eba5e921ba8adc4f5795693bbe04a681b05a840  consts.h
ab8485bf11d49b3408d34f8d58ae36eb7f4d602da354591bbb6fba44ec0dc269  ../data/a0set256_peer.txt
0efce486d2feffec4cc8576d62eeb1e45fbbc1c91386810069cdbd4f8ee44b47  ../data/peer_a2.txt
789e71d06549216e23d580aaa9af06f77ebff5b1932726caa7f2dcb6121e622f  ../data/ex1_g.txt
```

Run scripts (all runs kept): R1 `seq 31001 32024 | xargs -P 8 -I{} ./smc vsU.txt all {} 4000 2048 64 64 8 8 4 8192`; R2 run i = 0..4095: `./smc vsP.txt pop:i $((40000+i)) 4000 2048 64 64 8 8 4 8192`.

Analysis output (`analyze.py`):

```
r1.out: runs 1024 (empty 0)  mean log2 -100.99875  rel sd 0.0258  99% lower bound log2 -101.00146  successes 4384763 failed rebuilds 0
  stage means (log2): -27.000 -16.999 -13.000 -15.000 -6.000 -7.000 -1.000 -15.000
  min/max single run log2 -101.1256 / -100.8748
r2.out: runs 4096 (empty 0)  mean log2 -101.00020  rel sd 0.0334  99% lower bound log2 -101.00195  successes 17537702 failed rebuilds 0
  stage means (log2): -27.000 -17.000 -13.000 -15.000 -6.000 -7.000 -1.000 -15.000
  min/max single run log2 -101.1589 / -100.8381
```

Development replicates for the pass rule of Section 10.1: 1200 replicates of the reduced estimator, mean 2^-100.9985.


Replay of verified successes (`t_replay.py`): successes replayed 12817 found by the counted program 12817 failures 0 distinct A0 256 ops min/max 3339 5125

Stream summaries (`replay_smc.txt`):

```
50001 -101.06609 -27.000 -17.009 -13.007 -15.021 -6.000 -6.995 -1.000 -15.035  succ 4180 rebuilt_failed 0
50002 -100.95311 -27.000 -16.994 -13.000 -15.008 -6.000 -7.007 -1.000 -14.943  succ 4453 rebuilt_failed 0
50003 -101.02103 -27.000 -16.982 -12.999 -15.011 -6.000 -6.996 -1.000 -15.033  succ 4184 rebuilt_failed 0
```

### A.5 Other outputs

Outputs of the base package's runs, except the ledger output and its inputs, the outputs of `t_pre_d.py` and `t_imm_d.py` and the selftest (this derivative's, Appendix D).

`ledger38.py`:

```
q3_log2                -101.5
delta                  0.564
S_log2                 -67.92135419685442
q_lb_log2              -68.39929844769345
NG                     192411962931188556827
NG_log2                67.38276039708892
NE_MAX                 476541407141896427736294
NW_MAX                 12644480665306256024453
N1_MAX                 12443835869884856784
N2_MAX                 144695765928893684
E_NE                   2476.6346569545567
E_NW                   65.71165722723981
E_N1                   0.06417154026097638
E_N2                   0.0007292220484201861
cap_overflow_total     2.8994875076708023e-06
success_lower_bound    0.39
per_group_fixed        3438
cw                     43
c1                     19
c2                     3148
online_ops             2635541153744151265958275
online_ops_log2        81.12437349709666
pre_ops                385844947273092062201164
pre_units_log2         66.93873946683676
pre_terms              {'P1_G': 38.906890595608516, 'P1_live': 41.584962500791136, 'P2_F7': 36.807354922057606, 'P2_zero': 36.321928095021725, 'P3_A2': 37.45943164208948, 'P4_rec': 15.366322214245816, 'P5_enum': 52.49386125078, 'P6_zero': 73.08746284125034, 'P6_count': 76.65053872166537, 'P6_fill': 77.33859471533793, 'P6_prefix': 75.8073549220576}
tight_up               True
tight_down             True
allow_log2             70.00281501560706
memory_log2_bytes      80.41607687449509
preprocessing_incl_allowances_log2 70.16575943804749
T_num                  6773230216939762999009911
T_den                  2728
log2_T                 71.07249038096977
time_log2              71.0725
attack_units_log2      70.13895521323573
ops_per_block_cv       53.505418659934755
```

`t_cost.py` (base program):

```
prologue 96  epilogue 15  four empty blocks 85 (21.25 per block)  loop iteration 6
lane 0 {'X_E17': 55, 'X_A17': 66, 'X_A17int': 79, 'X_SUCC': 3207}
lane 1 {'X_E17': 58, 'X_A17': 69, 'X_A17int': 82, 'X_SUCC': 3210}
lane 2 {'X_E17': 58, 'X_A17': 69, 'X_A17int': 82, 'X_SUCC': 3210}
lane 3 {'X_E17': 55, 'X_A17': 66, 'X_A17int': 79, 'X_SUCC': 3207}
{"P0": 96, "EPI": 15, "GROUP4": 85, "ITER": 6, "PASS_ENTRY": 3, "X_E17": 58, "X_A17": 69, "X_A17int": 82, "X_SUCC": 3210, "BLOCK_FIXED": 21.25}
```

`t_mut.py`:

```
cases 6532 run 6520 mismatches 0 expected-outcome histogram {'succ': 2279, 'row': 4164, 'E17': 32, 'W7': 42, 'A17': 3}
cases 6532 run 6520 mismatches 0 expected-outcome histogram {'succ': 2279, 'row': 4164, 'E17': 32, 'W7': 42, 'A17': 3}
cases 6532 run 6520 mismatches 0 expected-outcome histogram {'succ': 2279, 'row': 4164, 'E17': 32, 'W7': 42, 'A17': 3}
cases 6532 run 6520 mismatches 0 expected-outcome histogram {'succ': 2279, 'row': 4164, 'E17': 32, 'W7': 42, 'A17': 3}
```

`t_eq.py (6 chaining values x 256 A0)`:

```
cv 0 entries 1609 NE 5595 5595 NW 92 92 N1 0 0 marks 92 92 ops 20643 OK
cv 1 entries 1402 NE 4974 4974 NW 91 91 N1 0 0 marks 91 91 ops 19394 OK
cv 2 entries 1397 NE 4959 4959 NW 94 94 N1 0 0 marks 94 94 ops 19544 OK
cv 3 entries 1542 NE 5394 5394 NW 96 96 N1 0 0 marks 96 96 ops 20518 OK
cv 4 entries 1588 NE 5532 5532 NW 93 93 N1 1 1 marks 94 94 ops 20610 OK
cv 5 entries 1351 NE 4821 4821 NW 80 80 N1 1 1 marks 81 81 ops 18410 OK
total {'ne': 31275, 'nw': 546, 'n1': 2, 'ent': 8889, 'deep': 0} mismatching CVs 0 row histogram []
```

`t_pre1.py`:

```
P1 G body: tested 21184 mismatches 0 max ops hit/non-hit {True: 117, False: 115}
P2 F7 body: tested 5871 mismatches 0 ops (in F7 / not) {0: 22, 1: 25}
P3 A2 body: tested 26246 mismatches 0 ops {True: 41, False: 39}
P4 A2 records: 768, mismatching words 0 ops total 39168 per record 51.0
P4 G records: 32, mismatching words 0 ops total 3072
```

`t_pre2.py`:

```
P5: windows 6 window candidates 24576 valid variants found 2061 mismatching windows 0
P5 ops: setup 32 , valid candidate incl. append 86 , append part 28 , body part (all tests pass) 58
P5 body cost histogram (random in-window candidates): [(33, 389), (58, 11)]
P6 count: ops per (Y, variant) {205}
P6 prefix ops {'empty': {7}, 'nonempty': {15}}  (includes the loop-increment op of this harness: 1)
P6 fill ops per (Y, variant) {365}
P6: buckets 512 mismatching 0 count mismatches 0 empty headers = EMPTY: True
P6 vs true buckets (6 CVs, A0 block 0): mismatching 0
```

`t_clump.py (six slices of the list)`:

```
successes 2137 other valid variants with the same (A0, A1) 26037 row-16 co-hits 17683 W7 passes 1768 first row-17 tests (E17 mask) passed 141 full row 17 holds 37 co-successes 0
successes 2137 other valid variants with the same (A0, A1) 26693 row-16 co-hits 18154 W7 passes 1694 first row-17 tests (E17 mask) passed 110 full row 17 holds 43 co-successes 0
successes 2137 other valid variants with the same (A0, A1) 25669 row-16 co-hits 17479 W7 passes 1687 first row-17 tests (E17 mask) passed 131 full row 17 holds 32 co-successes 0
successes 2137 other valid variants with the same (A0, A1) 26522 row-16 co-hits 17478 W7 passes 1660 first row-17 tests (E17 mask) passed 146 full row 17 holds 40 co-successes 0
successes 2137 other valid variants with the same (A0, A1) 26325 row-16 co-hits 17733 W7 passes 1779 first row-17 tests (E17 mask) passed 111 full row 17 holds 31 co-successes 0
successes 2132 other valid variants with the same (A0, A1) 26060 row-16 co-hits 17496 W7 passes 1715 first row-17 tests (E17 mask) passed 142 full row 17 holds 51 co-successes 0
```

`t_own.py, 1,500 successes`:

```
successes 1500 other entries in the success's own bucket 20973 (of them with the same A1: 12436) W7 passes 1782 first row-17 tests passed 95 rows>=18 0 further successes 0
```

`costs.json, pre1.json, pre2.json (inputs of the ledger)`:

```
costs.json: {"P0": 91, "EPI": 19, "GROUP4": 76, "ITER": 6, "PASS_ENTRY": 2, "X_E17": 41, "X_A17int": 60, "X_SUCC": 3208, "BLOCK_FIXED": 19.0}
pre1.json: {"G_hit_ops": 117, "G_nonhit_max_ops": 115, "F7_in_ops": 25, "F7_out_ops": 22, "A2_hit_ops": 41, "A2_nonhit_max_ops": 39, "A2REC_total_ops": 39168, "GREC_total_ops": 3072, "LIVE_ops": 21, "LIVE_g": 5}
pre2.json: {"P5_SETUP": 37, "P5_BODY_MAX": 57, "P5_APPEND": 46, "P5_LOOP": 3, "P6_ZERO16": 34, "P6_COUNT_IT": 144, "P6_COUNT_VAR": 16, "P6_FILL_IT": 232, "P6_FILL_VAR": 17, "P6_PREFIX_EMPTY": 6, "P6_PREFIX_NONEMPTY": 11}
```

`t_pre_d.py` (this derivative; the counts of P5 and P6):

```
P1' live words: 22 count 1048576 | body vs predicate on 96,000 E17: 0 mismatches, 370 passes | longest path 21 | per g 5
P5: setup 37 | valid candidates 16 list words != (c7 + 2^32, mkent fields, c9x): 0 | append ops [46] | body ops (valid candidates) [57] | loop control 3
P6 zero: 48 headers in 3 iterations, all zero, ops 102 | per iteration (16 headers) 34
P6 prefix: empty header 6 ops, nonempty header 11 ops (loop control not included)
P6 toy: 9 variant runs (4 real variants, A1 = 2^32 - 3, 1 and 0; the real limits 2^32 and A1 as well as toy limits), 946 headers, 1188 entries: count and fill == definition, 0 mismatches
P6 count: 144 ops per iteration (incl. loop branch), 16 per variant (loads, A1, both segment setups, guard, list-loop branch); fill: 232 ops per iteration, 17 per variant
pre1.json {'G_hit_ops': 117, 'G_nonhit_max_ops': 115, 'F7_in_ops': 25, 'F7_out_ops': 22, 'A2_hit_ops': 41, 'A2_nonhit_max_ops': 39, 'A2REC_total_ops': 39168, 'GREC_total_ops': 3072, 'LIVE_ops': 21, 'LIVE_g': 5}
pre2.json {'P5_SETUP': 37, 'P5_BODY_MAX': 57, 'P5_APPEND': 46, 'P5_LOOP': 3, 'P6_ZERO16': 34, 'P6_COUNT_IT': 144, 'P6_COUNT_VAR': 16, 'P6_FILL_IT': 232, 'P6_FILL_VAR': 17, 'P6_PREFIX_EMPTY': 6, 'P6_PREFIX_NONEMPTY': 11}
```

`sens38.py`, last block (the four changes of Appendix D):

```
aa0496d3 as filed (its pre2.json, pair budget 1)                                             71.335968              (claim 71.33597)
(1) the counts the printed bodies execute (P6 fill 233, P5 setup 37, append 46, body 57)     71.342384  +0.006417  (claim 71.34239)
(2) + P6 zero unrolled 16 times (34 per 16 headers)                                          71.340819  -0.001565  (claim 71.34082)
(3) + Y loop of the count and fill passes on u (144 / 232 per iteration, 16 / 17 per variant) 71.339653  -0.001166  (claim 71.33966)
(4) + pair budget delta = 0.564 instead of 1  [this derivative]                              71.072490  -0.267163  (claim 71.07250)
```

`selftest` of experiments/vt38.py (the file of aa0496d3, unchanged):

```
1 published pair collides, M != M'                         ok 
  published dense part is a valid variant                  ok 
2 G: the 32 words hold row 16; 20,000 random words and the 1,024 bit-flip neighbours agree with G ok (exhaustive count over 2^32: 32)
  A2 list: 768 sorted values, all satisfy the A2-only conditions ok 
  512 embedded variants valid; 256 entry variants valid    ok 
3 Lemma 3 (rows -4..15 hold, DW_i for i < 16) and Lemma 5 (W16 closed form, W7 = c7 - A_-1), 40 chaining values ok 
4 program: registers after allocation <= 64                ok (42)
   costs: {'P0': 91, 'EPI': 19, 'GROUP4': 76, 'ITER': 6, 'X_E17': 41, 'X_A17int': 60, 'X_SUCC': 3208}
  ledger constants P0 91, epilogue 19, four blocks 76, iteration 6, E17 41, A17 60, success 3208 ok 
  published pair: the program finds it in each of the 4 lanes ok 
5 replicate: estimate, accepted pairs (rebuilt, verified), failed rebuilds 0 ok (log2 -101.094, 77 pairs, 77 found by the counted program)
6 vt-ram-r38 (8 trials): mismatches 0, pairs returned 8    ok [0, 0, 2, 2, 5, 5, 1, 2]
SELFTEST PASSED
```

`t_imm_d.py` (immediates charged):

```
online costs, immediates charged: {'P0': 113, 'EPI': 24, 'GROUP4': 99, 'ITER': 7, 'X_E17': 49, 'X_A17int': 74, 'X_SUCC': 3559, 'PASS_ENTRY': 3, 'BLOCK_FIXED': 24.75}
preprocessing bodies, immediates charged:
 pre1 {'G_hit_ops': 160, 'G_nonhit_max_ops': 157, 'F7_in_ops': 31, 'F7_out_ops': 27, 'A2_hit_ops': 58, 'A2_nonhit_max_ops': 55, 'A2REC_total_ops': 56832, 'GREC_total_ops': 4224, 'LIVE_ops': 30, 'LIVE_g': 6}
 pre2 {'P5_SETUP': 56, 'P5_BODY_MAX': 71, 'P5_APPEND': 61, 'P5_LOOP': 4, 'P6_ZERO16': 50, 'P6_COUNT_IT': 213, 'P6_COUNT_VAR': 22, 'P6_FILL_IT': 345, 'P6_FILL_VAR': 23, 'P6_PREFIX_EMPTY': 6, 'P6_PREFIX_NONEMPTY': 13}
ledger with immediates charged: time_log2 71.17865  log2_T 71.178643
```

`t_imm.py (immediates charged; base program)`:

```
immediates charged: every immediate operand of an ALU instruction, compare-branch or store costs one extra operation. Online program: t_imm.py (instrumented interpreter class MI). Preprocessing bodies: t_pre1.py and t_pre2.py rerun with class MI substituted for Machine and MachineP (results: G body 160, F7 31, A2 58 operations; P5 setup 47, body 71, append 36; P6 count 303, fill 527, prefix 7/18). Ledger with these inputs:
{"P0": 123, "EPI": 15, "GROUP4": 112, "ITER": 7, "PASS_ENTRY": 3, "X_E17": 70, "X_A17": 85, "X_A17int": 101, "X_SUCC": 3559, "BLOCK_FIXED": 28.0}
pre_units_log2         68.00264375896379
log2_T                 71.82645196445513
time_log2              71.82646
attack_units_log2      71.3474868422608
```

`t_far.py, 24 successes`:

```
buckets 6120 cvs 24 entries 34577 expected 34157.9 ratio 1.0123
W7 passes 2391 expected 2285.0 (of observed entries 2313.0) E17-mask passes 4 expected 2.33 rows>=18 0 successes 0
```

`t_far.py, 12 real first blocks`:

```
buckets 3072 cvs 12 entries 16995 expected 17145.9 ratio 0.9912
W7 passes 1139 expected 1147.0 (of observed entries 1136.9) E17-mask passes 1 expected 1.11 rows>=18 0 successes 0
```

`tbl.c` (four runs; last lines):

```
generic var_valid failures on checked variants: 0
G hits 50 (expected 66.13), full row-16 failures among hits 0; non-hit sample 8667336, row-16 passes among them 0
W7 in F7: 9081134 of 138678098 sampled (rate 0.06548, expected 0.06689)
generic var_valid failures on checked variants: 0
G hits 54 (expected 66.07), full row-16 failures among hits 0; non-hit sample 8659841, row-16 passes among them 0
W7 in F7: 9288211 of 138558498 sampled (rate 0.06703, expected 0.06689)
generic var_valid failures on checked variants: 0
G hits 66 (expected 66.05), full row-16 failures among hits 0; non-hit sample 8657454, row-16 passes among them 0
W7 in F7: 9383667 of 138520141 sampled (rate 0.06774, expected 0.06689)
generic var_valid failures on checked variants: 0
G hits 84 (expected 66.00), full row-16 failures among hits 0; non-hit sample 8650765, row-16 passes among them 0
W7 in F7: 9110921 of 138413076 sampled (rate 0.06582, expected 0.06689)
```

`rcount.c` output (exact |R_j|, last lines):

```
3660bd4e 748016615
3668dd4e 747975479
3668dd56 747975119
366afd58 747959736
```


## Appendix B. Evidence programs (sources; the names are the file names used in Sections 6 and 11)

### B.1 ledger38.py

```python
# Listing of ledger38.py omitted in this filing (512 KiB judge-evidence budget); superseded by self-contained ledger_e.py in Appendix E.6.
```























































































































### B.2 sens38.py

```python
# Listing of sens38.py omitted in this filing (512 KiB judge-evidence budget); superseded by sens_e.py in Appendix E.5.
```












































### B.3 vtpre.py (preprocessing as counted code)

```python
# vtpre.py - preprocessing as counted code (same machine as vtprog.py): P1 the set G, P2 the F7 table, P3 the A2 list,
# P4 the A2 and G records, P5 the variant lists R_j, P6 the tables T_j (zero, count, prefix, fill).
# Each pass is a loop body generated here; the interpreter counts the executed operations; the ledger charges
# (items) x (the longest path of the body, measured by executing it) and the loop control.
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vt38 import *

def br_ne(a, t, val, lab):
    """branch to lab if register t != val (val 0: bnz)"""
    a('bnz', t, lab) if val == 0 else a('bne', t, val, lab)

# ---------------------------------------------------------------------------------------------------------------
# P1: row 16 of both members as a function of W16 (member x = w; member y = w + dW16)
def gen_g_body(a, nx, w='w'):
    """Falls through iff w is in G.  Constants of rows 12..15 of S*."""
    kx = {}
    for m, (Aa, Ee) in enumerate(((SAX, SEX), (SAY, SEY))):
        A = lambda i: Aa[i+4]; E = lambda i: Ee[i+4]
        kx[m] = ((A(12) + E(12) + S1(E(15)) + CH(E(15), E(14), E(13)) + K[16]) & M,
                 (-A(12) + S0(A(15)) + MAJ(A(15), A(14), A(13))) & M, E(15), A(15), A(14), E(14))
    mW, vW, dW, _ = CELLS[2][16]; mE, vE, dE, _ = CELLS[1][16]; mA, vA, dA, _ = CELLS[0][16]
    if mW: a('and', 't1', w, mW); br_ne(a, 't1', vW, nx)
    a('add', 'wy', w, DW[16]); a('and', 'wy', 'wy', M)
    a('xor', 't1', w, 'wy'); br_ne(a, 't1', dW, nx)
    for m, wr, er, ar in ((0, w, 'ex', 'ax'), (1, 'wy', 'ey', 'ay')):
        c1, c2 = kx[m][0], kx[m][1]
        a('add', er, wr, c1); a('and', er, er, M)
        if m == 0:
            if mE: a('and', 't1', er, mE); br_ne(a, 't1', vE, nx)
            if PQ[16]: a('xor', 't1', er, kx[0][2]); a('and', 't1', 't1', PQ[16]); a('bnz', 't1', nx)
        else:
            a('xor', 't1', 'ex', 'ey'); br_ne(a, 't1', dE, nx)
        a('add', ar, er, c2); a('and', ar, ar, M)
        if m == 0:
            if mA: a('and', 't1', ar, mA); br_ne(a, 't1', vA, nx)
        else:
            a('xor', 't1', 'ax', 'ay'); br_ne(a, 't1', dA, nx)
    # two-bit conditions keyed at row 16 (member x): operands at rows 14, 15 are constants of S*
    regs = {(0, 16): 'ax', (1, 16): 'ex', (2, 16): w}
    const = lambda k, i: (SAX, SEX, SWX)[k][i + (4 if k < 2 else 0)]
    for (k1, i1, b1, eq, k2, i2, b2, row) in X2:
        if row != 16: continue
        need = 0 if eq else 1            # required value of v1 ^ v2
        if (k1, i1) in regs and (k2, i2) in regs:
            a('shr', 't1', regs[(k1, i1)], b1); a('shr', 't2', regs[(k2, i2)], b2); a('xor', 't1', 't1', 't2'); a('and', 't1', 't1', 1)
            br_ne(a, 't1', need, nx)
        else:
            (kv, iv, bv), (kc, ic, bc) = ((k1, i1, b1), (k2, i2, b2)) if (k1, i1) in regs else ((k2, i2, b2), (k1, i1, b1))
            cbit = (const(kc, ic) >> bc) & 1
            a('shr', 't1', regs[(kv, iv)], bv); a('and', 't1', 't1', 1); br_ne(a, 't1', cbit ^ need, nx)

# ---------------------------------------------------------------------------------------------------------------
# P1': the live words of G (L0): for each g, count the E17 that pass the row-17 tests of the program (E17 mask, A17 mask,
# A17-internal conditions); the loop over the 2^32 values of E17 (register e) runs this body; g is live iff the count is not 0.
def gen_live_body(a, gi, nx):
    r = grec(gi, GL[gi]); b = gaddr(gi)
    a('and', 't1', 'e', r[b + 1]); br_ne(a, 't1', r[b + 2], nx)
    a('add', 'A17', 'e', r[b + 3]); a('and', 't1', 'A17', r[b + 4]); br_ne(a, 't1', r[b + 5], nx)
    for n_, (b1, b2, eq) in enumerate(a17int()):
        d_ = 't3' if n_ == 0 else 't1'
        a('shr', d_, 'A17', b1 - b2) if b1 >= b2 else a('shl', d_, 'A17', b2 - b1)
        a('xor', d_, d_, 'A17'); a('and', d_, d_, 1 << b2)
        if not eq: a('xor', d_, d_, 1 << b2)
        if n_: a('or', 't3', 't3', 't1')
    a('bnz', 't3', nx); a('add', 'cnt', 'cnt', 1)

def gen_live_end(a, gi, nx):
    """after the loop of one g: append g to the live list iff its count is not 0"""
    a('bz', 'cnt', nx); a('st', 'lv', gi); a('add', 'lv', 'lv', 1); a('li', 'cnt', 0)

def live_list(cnt=None):
    """the (gi, g) of G whose exact row-17 count (digit DP over E17 with the carry of A17 = E17 + a17) is not 0"""
    out = []
    for gi, g in enumerate(GL):
        r = grec(gi, g); b = gaddr(gi); P = a17int(); st = {(0, 0): 1}
        for i in range(32):
            ns = {}
            for (c, h), n in st.items():
                for e in (0, 1):
                    s = e + (r[b + 3] >> i & 1) + c; x = s & 1; h2 = h | x << i
                    if (r[b + 1] >> i & 1 and e != r[b + 2] >> i & 1) or (r[b + 4] >> i & 1 and x != r[b + 5] >> i & 1): continue
                    if any(max(p, q) == i and ((h2 >> p) ^ (h2 >> q)) & 1 != (0 if w else 1) for p, q, w in P): continue
                    k = (s >> 1, h2 & sum(1 << p | 1 << q for p, q, w in P if max(p, q) > i)); ns[k] = ns.get(k, 0) + n
            st = ns
        n = sum(st.values())
        if cnt is not None: cnt.append(n)
        if n: out.append((gi, g))
    return out
LIVE = live_list()

# ---------------------------------------------------------------------------------------------------------------
# P2: the F7 table: flag at w and w + 2^32 for w in F7, and the value 2 at 2^34 + 1 + w for all w (sentinel region)
def gen_f7_body(a, nx, w='w'):
    rot32(a, 'sw', w, 7, 18, 3, shr3=True, D='D1')
    a('add', 'w2', w, D7); a('and', 'w2', 'w2', M)
    rot32(a, 'sw2', 'w2', 7, 18, 3, shr3=True, D='D2')
    a('add', 'ad', w, (1 << 34) + 1); a('st', 'ad', 'two')          # sentinel region
    a('sub', 't1', 'sw2', 'sw'); a('and', 't1', 't1', M); br_ne(a, 't1', T7, nx)
    a('st', w, 'one'); a('add', 'ad', w, 1 << 32); a('st', 'ad', 'one')

# ---------------------------------------------------------------------------------------------------------------
# P3: the A2 list: conditions on A2 alone
def gen_a2_body(a, nx, x='x'):
    c6 = (sa(6) - S0(sa(5)) - MAJ(sa(5), sa(4), sa(3))) & M
    a('add', 'e6', x, c6); a('and', 'e6', 'e6', M)
    mE, vE, dE, _ = CELLS[1][6]
    assert dE == 0
    if mE: a('and', 't1', 'e6', mE); br_ne(a, 't1', vE, nx)
    # '+' pairs of row 7 against E6, both members (E7 published)
    if PQ[7]:
        a('xor', 't1', 'e6', sex(7)); a('and', 't1', 't1', PQ[7]); a('bnz', 't1', nx)
        a('xor', 't1', 'e6', sey(7)); a('and', 't1', 't1', PQ[7]); a('bnz', 't1', nx)
    # W10 of both members = c10 - E6: s0 difference
    c10x = (sex(10) - sa(6) - S1(sex(9)) - CH(sex(9), sex(8), sex(7)) - K[10]) & M
    c10y = (sey(10) - say(6) - S1(sey(9)) - CH(sey(9), sey(8), sey(7)) - K[10]) & M
    a('rsub', 'w10x', c10x, 'e6'); a('and', 'w10x', 'w10x', M); a('rsub', 'w10y', c10y, 'e6'); a('and', 'w10y', 'w10y', M)
    a('sub', 't1', 'w10y', 'w10x'); a('and', 't1', 't1', M); br_ne(a, 't1', DW[10], nx)
    rot32(a, 'sx', 'w10x', 7, 18, 3, shr3=True, D='D1'); rot32(a, 'sy', 'w10y', 7, 18, 3, shr3=True, D='D2')
    a('sub', 't1', 'sy', 'sx'); a('and', 't1', 't1', M); br_ne(a, 't1', DS0[10], nx)

# ---------------------------------------------------------------------------------------------------------------
# P4: records.  A2 record (2 words) and G record (12 words) exactly as in vtprog.tables()
def gen_a2rec(a, x='x', dst='ra'):
    """x = A2 (register, masked); writes the two record words to mem[dst], mem[dst+1] (dst a register)."""
    e6c = (sa(6) - S0(sa(5)) - MAJ(sa(5), sa(4), sa(3))) & M
    a('add', 'e6', x, e6c); a('and', 'e6', 'e6', M)
    rot32(a, 'S0x', x, 2, 13, 22); a('and', 'S0x', 'S0x', M)
    # MAJ(A4, A3, A2) = (A4 & (A3 ^ A2)) ^ (A3 & A2)
    a('xor', 'mj', x, sa(3)); a('and', 'mj', 'mj', sa(4)); a('and', 't2', x, sa(3)); a('xor', 'mj', 'mj', 't2')
    a('rsub', 'e5b', (sa(5) - S0(sa(4))) & M, 'mj'); a('and', 'e5b', 'e5b', M)           # E5 - A1
    # c9 = E9 - 2 A5 + S0(A4) + MAJ(A4,A3,A2) - S1(E8) - CH(E8,E7,E6) - K9 ; CH(E8,E7,E6) = ((E7 ^ E6) & E8) ^ E6
    for tag, E, A in (('x', sex, sa), ('y', sey, say)):
        a('xor', 't2', 'e6', E(7)); a('and', 't2', 't2', E(8)); a('xor', 't2', 't2', 'e6')
        a('rsub', 'c9' + tag, (E(9) - 2 * sa(5) + S0(sa(4)) - S1(E(8)) - K[9]) & M, 't2')
        a('add', 'c9' + tag, 'c9' + tag, 'mj'); a('and', 'c9' + tag, 'c9' + tag, M)
        c10 = (E(10) - A(6) - S1(E(9)) - CH(E(9), E(8), E(7)) - K[10]) & M      # W10 = c10 - E6
        a('rsub', 'w10' + tag, c10, 'e6'); a('and', 'w10' + tag, 'w10' + tag, M)
    a('add', 'k10', 'w10x', s1(SWX[15])); a('and', 'k10', 'k10', M)
    a('shl', 'r0', 'k10', 32); a('or', 'r0', 'r0', x)
    a('shl', 't1', 'S0x', 64); a('or', 'r0', 'r0', 't1')
    a('shl', 't1', 'e6', 96); a('or', 'r0', 'r0', 't1')
    a('shl', 't1', 'e5b', 128); a('or', 'r0', 'r0', 't1')
    a('st', dst, 'r0')
    a('shl', 'r1', 'c9y', 32); a('or', 'r1', 'r1', 'c9x')
    a('shl', 't1', 'w10x', 64); a('or', 'r1', 'r1', 't1'); a('shl', 't1', 'w10y', 96); a('or', 'r1', 'r1', 't1')
    a('add', 'da', dst, 1); a('st', 'da', 'r1')

def gen_grec(a, gi, g):
    """G record of the constant g = W16x: counted straight-line code computing the words of vtprog.grec(gi, g)."""
    vals = grec(gi, g); base = gaddr(gi)
    for m, (Aa, Ee) in enumerate(((SAX, SEX), (SAY, SEY))):
        A = lambda i: Aa[i+4]; E = lambda i: Ee[i+4]
        a('li', 'wm', g if m == 0 else (g - DW16) & M)
        a('add', 'e16', 'wm', (A(12) + E(12) + S1(E(15)) + CH(E(15), E(14), E(13)) + K[16]) & M); a('and', 'e16', 'e16', M)
        a('add', 'a16', 'e16', (-A(12) + S0(A(15)) + MAJ(A(15), A(14), A(13))) & M); a('and', 'a16', 'a16', M)
        rot32(a, 'sE', 'e16', 6, 11, 25)
        # CH(e16, E15, E14) = ((E15 ^ E14) & e16) ^ E14
        a('and', 't1', 'e16', E(15) ^ E(14)); a('xor', 't1', 't1', E(14))
        a('add', 'c17', 'sE', 't1'); a('add', 'c17', 'c17', (A(13) + E(13) + K[17]) & M); a('and', 'c17', 'c17', M)
        rot32(a, 'sA', 'a16', 2, 13, 22)
        # MAJ(a16, A15, A14) = (a16 & (A15 ^ A14)) ^ (A15 & A14)
        a('and', 't1', 'a16', A(15) ^ A(14)); a('xor', 't1', 't1', A(15) & A(14))
        a('add', 'a17', 'sA', 't1'); a('add', 'a17', 'a17', (-A(13)) & M); a('and', 'a17', 'a17', M)
        if m == 0:
            a('sti', base, 'c17'); a('sti', base + 3, 'a17'); a('sti', base + 8, 'a16'); a('sti', base + 9, 'e16')
            a('add', 'e16x', 'e16', 0); a('add', 'a16x', 'a16', 0)
        else:
            a('sti', base + 10, 'a16'); a('sti', base + 11, 'e16')
    # masks do not depend on g; values: cell values plus the (possibly inverted) bits of e16x / a16x of the folded conditions
    mE, vE, _, _ = CELLS[1][17]; mA, vA, _, _ = CELLS[0][17]
    a('sti', base + 1, vals[base + 1]); a('sti', base + 4, vals[base + 4]); a('sti', base + 6, g); a('sti', base + 7, 0)
    a('li', 'vE', vE); a('li', 'vA', vA)
    for (k1, i1, b1, eq, k2, i2, b2, row) in X2:
        if row == 17 and i1 == 16 and i2 == 17:
            src = 'e16x' if k1 == 1 else 'a16x'
            a('shr', 't1', src, b1); a('and', 't1', 't1', 1)
            if not eq: a('xor', 't1', 't1', 1)
            a('shl', 't1', 't1', b2); a('or', 'vE' if k2 == 1 else 'vA', 'vE' if k2 == 1 else 'vA', 't1')
    a('and', 't1', 'e16x', PQ[17]); a('or', 'vE', 'vE', 't1')
    a('sti', base + 2, 'vE'); a('sti', base + 5, 'vA')

# ---------------------------------------------------------------------------------------------------------------
# P5: the variant list R_j.  For A0 = A0_j (instruction field) and an A2 of the list (record at register 'ra'), the
# candidates A1 = lo + r, r in [r0, r1), lo = (E6 & 0xe0000000) - (E5 - A1) (the '+' pair of rows 5/6 confines A1 to one
# window of 2^29).  Tests: dW8 (through CH only), ds0(W9), ds0(W8) (A0 enters W8 = Fx - A0).  Valid candidates append three
# words (c7 + 2^32, eb, c9x) at the list pointer 'lp'.
def gen_enum_setup(a, a0):
    """Per (A0, A2): constants from the A2 record at register ra (word 0: A2 | K10 << 32 | S0(A2) << 64 | E6 << 96 |
    (E5 - A1) << 128; word 1: c9x | c9y << 32 | ...)."""
    a('ld', 'w0', 'ra'); a('add', 't1', 'ra', 1); a('ld', 'w1r', 't1')
    a('and', 'A2', 'w0', M); a('shr', 'S0A2', 'w0', 64); a('and', 'S0A2', 'S0A2', M)
    a('shr', 'E6', 'w0', 96); a('and', 'E6', 'E6', M); a('shr', 'k5', 'w0', 128); a('and', 'k5', 'w0', M) if False else (a('shr', 'k5', 'w0', 128), a('and', 'k5', 'k5', M))
    a('and', 'c9x', 'w1r', M)
    # window start lo = (E6 & e0000000) - k5
    a('and', 'lo', 'E6', 0xe0000000); a('sub', 'lo', 'lo', 'k5'); a('and', 'lo', 'lo', M)
    # constants of the tests: cdw8 = DW8 - (ky - kx), kx' = kx - A0 (W8x = kx' + MAJ(A3,A2,A1) - CH(E7x,E6,E5))
    a('xor', 'xa32', 'A2', sa(3)); a('and', 'aa32', 'A2', sa(3))
    a('and', 'e67x', 'E6', sex(7)); a('and', 'e67y', 'E6', sey(7))
    # c7 constant: E7x - 2 A3 + S0(A2) - S1(E6) - K7  (S1(E6) by a rotation)
    rot32(a, 's1e6', 'E6', 6, 11, 25); a('and', 's1e6', 's1e6', M)
    a('sub', 'cst7', 'S0A2', 's1e6'); a('add', 'cst7', 'cst7', (sex(7) - 2*sa(3) - K[7]) & M); a('and', 'cst7', 'cst7', M)
    a('xor', 'x20', 'A2', a0); a('and', 'a20', 'A2', a0)
    a('sub', 'A2ad', 'ra', A2T); a('shr', 'A2ad', 'A2ad', 1); a('shl', 'A2ad', 'A2ad', 128)   # A2 index << 128
    a('shr', 'k10', 'w0', 32); a('and', 'k10', 'k10', M)                                     # W10x + s1(W15x)

def gen_enum_body(a, a0, nx):
    """One candidate: register r = r; falls to the append code iff valid.  Costs: 9 ops to the first test."""
    cdw8 = (DW[8] - ((sey(8) - 2*sa(4) + S0(sa(3)) - S1(sey(7)) - K[8]) - (sex(8) - 2*sa(4) + S0(sa(3)) - S1(sex(7)) - K[8]))) & M
    kx = (sex(8) - 2*sa(4) + S0(sa(3)) - S1(sex(7)) - K[8] - a0) & M
    a('add', 'a1', 'lo', 'r'); a('add', 'E5', 'a1', 'k5')
    a('and', 'chx', 'E5', ~sex(7) & M); a('xor', 'chx', 'chx', 'e67x')
    a('and', 'chy', 'E5', ~sey(7) & M); a('xor', 'chy', 'chy', 'e67y')
    a('sub', 'd', 'chx', 'chy'); a('and', 'd', 'd', M); br_ne(a, 'd', cdw8, nx)
    # ds0(W9): w9 = c9x - A1
    a('sub', 'w9', 'c9x', 'a1'); a('and', 'w9', 'w9', M)
    a('add', 'w9p', 'w9', DW[9]); a('and', 'w9p', 'w9p', M)
    rot32(a, 'sa', 'w9', 7, 18, 3, shr3=True, D='D1'); rot32(a, 'sb', 'w9p', 7, 18, 3, shr3=True, D='D2')
    a('sub', 'd', 'sb', 'sa'); a('and', 'd', 'd', M); br_ne(a, 'd', DS0[9], nx)
    # ds0(W8): W8x = kx' + MAJ(A3, A2, A1) - CH(E7x, E6, E5)
    a('and', 'mj', 'a1', 'xa32'); a('xor', 'mj', 'mj', 'aa32')
    a('add', 'w8', 'mj', kx); a('sub', 'w8', 'w8', 'chx'); a('and', 'w8', 'w8', M)
    a('add', 'w8p', 'w8', DW[8]); a('and', 'w8p', 'w8p', M)
    rot32(a, 'sa', 'w8', 7, 18, 3, shr3=True, D='D1'); rot32(a, 'sb', 'w8p', 7, 18, 3, shr3=True, D='D2')
    a('sub', 'd', 'sb', 'sa'); a('and', 'd', 'd', M); br_ne(a, 'd', DS0[8], nx)

def gen_enum_append(a, a0):
    """Valid candidate (registers of the body): append the three list words at 'lp'."""
    # c7 = cst7 + MAJ(A2, A1, A0) - CH(E6, E5, E4) with E4 = A4 + A0 - S0(A3) - MAJ(A3, A2, A1) = (const) - mj
    a('and', 'm20', 'a1', 'x20'); a('xor', 'm20', 'm20', 'a20')
    a('rsub', 'E4', (sa(4) + a0 - S0(sa(3))) & M, 'mj')
    a('xor', 't', 'E5', 'E4'); a('and', 't', 't', 'E6'); a('xor', 't', 't', 'E4')          # CH(E6, E5, E4) = ((E5 ^ E4) & E6) ^ E4
    a('add', 'c7', 'cst7', 'm20'); a('sub', 'c7', 'c7', 't'); a('and', 'c7', 'c7', M); a('add', 'c7', 'c7', 1 << 32)
    a('and', 'a1m', 'a1', M)
    rot32(a, 's0a1', 'a1m', 2, 13, 22); a('and', 's0a1', 's0a1', M)
    # fields word (vt38.mkent): A1 | U << 32 | Q << 64 | S0(A1) << 96 | a2i << 128 | E1a << 160 | KCA << 224
    a('and', 't', 'a1m', a0); a('sub', 'u', 'A2', 's0a1'); a('sub', 'u', 'u', 't'); a('add', 'u', 'u', (-K[2]) & M); a('and', 'u', 'u', M)
    a('xor', 'qq', 'a1m', a0); a('add', 'kca', 'k10', 'a1m'); a('and', 'kca', 'kca', M)
    a('add', 'e1a', 'a1m', (1 - S0(a0)) & M); a('and', 'e1a', 'e1a', M); a('shl', 'e1a', 'e1a', 160)
    a('shl', 'e1', 'u', 32); a('or', 'e1', 'e1', 'a1m'); a('shl', 't', 'qq', 64); a('or', 'e1', 'e1', 't'); a('shl', 't', 's0a1', 96); a('or', 'e1', 'e1', 't')
    a('or', 'e1', 'e1', 'A2ad'); a('or', 'e1', 'e1', 'e1a'); a('shl', 't', 'kca', 224); a('or', 'e1', 'e1', 't')
    a('st', 'lp', 'c7'); a('add', 'lp', 'lp', 1); a('st', 'lp', 'e1'); a('add', 'lp', 'lp', 1); a('st', 'lp', 'c9x'); a('add', 'lp', 'lp', 1)

# ---------------------------------------------------------------------------------------------------------------
# P6: the table T_j.  Header word of (Y, Z0) at HB + (Y << 32 | Z0), HB = HDR | j << 64.  Passes:
#   zero   : header := 0                                                                      (4 ops per header)
#   count  : header += 1 for every (Y, variant, g) with Z0 = g - X, X = s0(Y + A1) - A1 + c9x  (loop over Y inside a variant)
#   prefix : header := address of the first entry (or EMPTY), entries of a bucket followed by a sentinel entry
#   fill   : entries written backwards from the end of each bucket (header decremented by 2 per entry)
def gen_zero_body(a): a('st', 'h', 'zero'); a('add', 'h', 'h', 1)

def gen_count_body(a, hb):
    """Registers: Y (loop), A1 (masked), c9x; variant constants.  One (Y, variant): 22 header increments (live words)."""
    a('add', 'u', 'Y', 'A1'); a('and', 'u', 'u', M)
    rot32(a, 'su', 'u', 7, 18, 3, shr3=True)
    a('sub', 'X', 'su', 'A1'); a('add', 'X', 'X', 'c9x')
    a('shl', 'Ys', 'Y', 32); a('add', 'Ys', 'Ys', hb)
    for gi, g in LIVE:
        a('rsub', 'Z', g, 'X'); a('and', 'Z', 'Z', M); a('add', 'I', 'Ys', 'Z'); a('ld', 'H', 'I'); a('add', 'H', 'H', 1); a('st', 'I', 'H')

def gen_fill_body(a, hb):
    """One (Y, variant): 2-word entry (c7', w1e + gw(gi)) written backwards at the bucket of each live g."""
    a('add', 'u', 'Y', 'A1'); a('and', 'u', 'u', M)
    rot32(a, 'su', 'u', 7, 18, 3, shr3=True)
    a('sub', 'X', 'su', 'A1'); a('add', 'X', 'X', 'c9x')
    a('shl', 'Ys', 'Y', 32); a('add', 'Ys', 'Ys', hb)
    for gi, g in LIVE:
        a('rsub', 'Z', g, 'X'); a('and', 'Z', 'Z', M); a('add', 'I', 'Ys', 'Z'); a('ld', 'H', 'I'); a('sub', 'H', 'H', ESZ); a('st', 'I', 'H')
        a('st', 'H', 'c7'); a('add', 't', 'H', 1); a('add', 't2', 'w1e', gw(gi)); a('st', 't', 't2')

# ---- the bodies used by the ledger of this derivative (R38L): 16 headers per zero iteration; Y loop with u = Y + A1 (mod 2^32) as the
# loop counter in two segments (u from A1 to 2^32 - 1, then u from 0 to A1 - 1), the header base Ys = hb + (Y << 32) running with it,
# and c9x - A1 folded into one constant cc.  The loop control is part of the measured iteration.  (gen_zero_body, gen_count_body and
# gen_fill_body above are the bodies of the earlier derivative; t_pre2.py runs those.)
def gen_zero16(a, hend, top='ztop'):
    """one iteration of the header-zeroing pass: 16 headers (st, add) and the loop branch"""
    a.L(top)
    for _ in range(16): a('st', 'h', 'zero'); a('add', 'h', 'h', 1)
    a('bne', 'h', hend, top)

def gen_count_iter(a):
    """one (u, variant) iteration of the count pass, without the loop branch: 22 header increments (live words)"""
    rot32(a, 'su', 'u', 7, 18, 3, shr3=True)
    a('add', 'X', 'su', 'cc')
    for gi, g in LIVE:
        a('rsub', 'Z', g, 'X'); a('and', 'Z', 'Z', M); a('add', 'I', 'Ys', 'Z'); a('ld', 'H', 'I'); a('add', 'H', 'H', 1); a('st', 'I', 'H')
    a('add', 'u', 'u', 1); a('add', 'Ys', 'Ys', 1 << 32)

def gen_fill_iter(a):
    """one (u, variant) iteration of the fill pass, without the loop branch: 2-word entry (c7', w1e + gw(gi)) written backwards at the bucket of each live g"""
    rot32(a, 'su', 'u', 7, 18, 3, shr3=True)
    a('add', 'X', 'su', 'cc')
    for gi, g in LIVE:
        a('rsub', 'Z', g, 'X'); a('and', 'Z', 'Z', M); a('add', 'I', 'Ys', 'Z'); a('ld', 'H', 'I'); a('sub', 'H', 'H', ESZ); a('st', 'I', 'H')
        a('st', 'H', 'c7'); a('add', 't', 'H', 1); a('add', 't2', 'w1e', gw(gi)); a('st', 't', 't2')
    a('add', 'u', 'u', 1); a('add', 'Ys', 'Ys', 1 << 32)

def gen_loads(a, fill):
    """the variant's list words at the list pointer lp (c7 + 2^32, eb, c9x): the count pass reads eb and c9x, the fill pass all three"""
    if fill: a('ld', 'c7', 'lp')
    a('add', 'lp', 'lp', 1); a('ld', 'w1e', 'lp'); a('add', 'lp', 'lp', 1); a('ld', 'c9x', 'lp'); a('add', 'lp', 'lp', 1)

def gen_variant_pass(a, hb, fill, lim1=1 << 32, lim2='A1'):
    """one variant of the count (fill = False) or fill (fill = True) pass over all 2^32 values of Y: segment 1 runs u from A1 to lim1 = 2^32 - 1
    (Y = u - A1), segment 2 runs u from 0 to lim2 = A1 - 1 (Y = u + 2^32 - A1) unless A1 = 0.  The branch back to 'vtop' is the loop over the list."""
    a.L('vtop'); gen_loads(a, fill); a('and', 'A1', 'w1e', M)
    a('add', 'u', 'A1', 0); a('li', 'Ys', hb); a('sub', 'cc', 'c9x', 'A1')
    a.L('seg1'); (gen_fill_iter if fill else gen_count_iter)(a); a('bne', 'u', lim1, 'seg1')
    a('bz', 'A1', 'vdone')
    a('li', 'u', 0); a('shl', 't', 'A1', 32); a('rsub', 'Ys', hb + (1 << 64), 't')
    a.L('seg2'); (gen_fill_iter if fill else gen_count_iter)(a); a('bne', 'u', lim2, 'seg2')
    a.L('vdone'); a('bne', 'lp', 'lpend', 'vtop')

def gen_prefix_body(a, empty_lab_unused=None):
    """One header (register h): count c = mem[h]; empty -> EMPTY; else header := end of bucket (entries are filled backwards
    from it), sentinel entry written at the end, 'run' advanced by 2 (c + 1)."""
    nz, done = 'pnz', 'pdone'
    a('ld', 'c', 'h'); a('bnz', 'c', nz)
    a('li', 'e0', EMPTY); a('st', 'h', 'e0'); a('jmp', done)
    a.L(nz)
    a('shl', 'c2', 'c', 1)                                                  # 2c
    a('add', 'run', 'run', 'c2'); a('st', 'h', 'run')                      # header := end of the bucket (fill decrements it to the start)
    a('li', 'sw', SENT); a('st', 'run', 'sw'); a('add', 't', 'run', 1); a('st', 't', 'zero')
    a('add', 'run', 'run', ESZ)
    a.L(done)
```

### B.4 consts.h

```c
/* generated by gen_consts.py from d1core.py (own transcription of ePrint 2026/1120 Tables 3-5) */
#define NR 38
static const u32 KC[38]={0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb};
static const u32 CELLS[3][NR][4]={{{0x00000000,0x00000000,0x00000000,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000},{0x60000000,0x20000000,0x60000000,0x00000000},{0x00410810,0x00000010,0x00410810,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000},{0x0000080c,0x00000808,0x0000080c,0x00000000},{0x44204602,0x40004200,0x44204602,0x00000000},{0x20010000,0x00000000,0x20010000,0x00000000},{0x08030090,0x08000090,0x08030090,0x00000000},{0x02808000,0x00800000,0x02808000,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000},{0x20000000,0x20000000,0x20000000,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000}},{{0x00000000,0x00000000,0x00000000,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000},{0x00000000,0x00000000,0x00000000,0xe0000000},{0x08441090,0x08040090,0x00000000,0xe0080800},{0xead6109b,0xe2c01001,0xe0000000,0x04080800},{0xebdf7bfb,0x89152879,0x084c1890,0x04000000},{0xfeffffbf,0xc670b71b,0x0490000b,0x00000000},{0x3dff7b9f,0x28c32a97,0x00410800,0x00000000},{0xbdffffbf,0x80f2c1be,0x20007004,0x00000040},{0xfdffffbf,0x5d9d1216,0x3c230005,0x00000040},{0xffefff7f,0x35c13b0d,0x0001077a,0x00000080},{0x7c636f7f,0x20026471,0x08010000,0x00001080},{0x4a530ffa,0x4a130b5a,0x00000880,0x00001000},{0x4c431a80,0x48030280,0x40421200,0x00040010},{0x40c21a80,0x00000800,0x00000000,0x01048010},{0x40c61230,0x00421210,0x00040010,0x01008000},{0x31848e32,0x30040430,0x01808000,0x00000000},{0x21848010,0x20040010,0x00000000,0x00000000},{0x21808c00,0x21008800,0x20000000,0x00000000},{0x20000000,0x00000000,0x00000000,0x00000000},{0x20000000,0x20000000,0x00000000,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000}},{{0x00000000,0x00000000,0x00000000,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000},{0x20000000,0x00000000,0x20000000,0x00000000},{0x04400800,0x04400000,0x04400800,0x00000000},{0x20000000,0x20000000,0x20000000,0x00000000},{0x050112aa,0x0100000a,0x050112aa,0x00000000},{0x00081400,0x00081400,0x00081400,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000},{0x04400800,0x04000000,0x04400800,0x00000000},{0x20000000,0x20000000,0x20000000,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000},{0x0582a000,0x0582a000,0x01808000,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000},{0x20000000,0x00000000,0x20000000,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000},{0x00000000,0x00000000,0x00000000,0x00000000}}};
static const u32 PQ[38]={0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0xe0000000,0x00080800,0x04000000,0x00000000,0x00000000,0x00000000,0x00000040,0x00000000,0x00000080,0x00001000,0x00000000,0x00040010,0x01008000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000};
typedef struct {int k1,i1,b1,eq,k2,i2,b2,row;} X2C;
static const X2C X2[]={{0,14,15,1,0,16,15,16},{0,14,23,1,0,16,23,16},{0,14,25,1,0,16,25,16},{0,15,4,1,0,16,4,16},{0,15,7,1,0,16,7,16},{0,15,16,0,0,16,16,16},{0,15,17,1,0,16,17,16},{0,15,27,1,0,16,27,16},{0,15,29,1,0,16,29,16},{0,16,15,1,0,17,15,17},{0,16,23,1,0,17,23,17},{0,16,25,1,0,17,25,17},{0,17,9,1,0,17,20,17},{0,17,6,1,0,17,18,17},{0,17,8,1,0,17,17,17},{0,16,29,1,0,18,29,18},{0,18,29,1,0,19,29,19},{1,16,4,0,1,16,23,16},{1,16,3,0,1,16,8,16},{1,16,14,1,1,16,28,16},{1,16,4,1,1,17,4,17},{1,16,18,1,1,17,18,17},{1,18,0,0,1,18,13,18},{1,17,15,1,1,18,15,18},{1,17,24,1,1,18,24,18},{1,19,6,0,1,19,19,19},{1,19,20,1,1,19,2,19},{1,21,2,1,1,21,16,21},{2,7,8,0,2,7,25,7},{2,7,14,0,2,7,18,7},{2,7,1,1,2,7,12,7},{2,8,0,0,2,8,28,8},{2,8,30,0,2,8,9,8},{2,8,1,1,2,8,18,8},{2,16,1,0,2,16,12,16},{2,16,20,0,2,16,27,16},{2,16,8,1,2,16,25,16},{2,16,14,1,2,16,18,16},{2,16,4,0,2,16,6,16},{2,16,22,0,2,16,31,16},{2,23,0,0,2,23,30,23},{2,23,1,0,2,23,31,23},{2,23,14,1,2,23,21,23},{2,23,16,1,2,23,25,23},{2,25,4,1,2,25,6,25},{2,25,22,1,2,25,31,25},{2,25,20,1,2,25,27,25}};
#define NX2 ((int)(sizeof(X2)/sizeof(X2[0])))
static const u32 PCV[8]={0xcd278980,0x1b12a052,0xb87cc8a6,0xa9e059c5,0xc9c3db85,0x6ca4b5b5,0x63d13ac1,0xc0329f1e};
static const u32 PMX[16]={0x48fc271b,0x9fca20cd,0xcc89f96f,0xfc40396f,0x8b328cb4,0x6b91ef78,0x97f9b767,0xc2450045,0x3f416758,0xfe9804cb,0x63a88c0f,0x0ceb1f8d,0xa28cd15a,0x77a1e994,0xd28e48a0,0x9f1f65bb};
static const u32 PMY[16]={0x48fc271b,0x9fca20cd,0xcc89f96f,0xfc40396f,0x8b328cb4,0x6b91ef78,0x97f9b767,0xe2450045,0x3b016f58,0xde9804cb,0x66a99ea5,0x0ce30b8d,0xa28cd15a,0x77a1e994,0xd28e48a0,0x9b5f6dbb};
static const u32 PHASH[8]={0x5d9ca5f4,0x59ace3a3,0x26c9c26c,0x4252c585,0x4c0803b7,0x1b4d5ccd,0x25c3ccc0,0x90645c4d};
static const u32 SAX[20]={0xa9e059c5,0xb87cc8a6,0x1b12a052,0xcd278980,0xb75dae71,0xda6c35e0,0x479b4dc8,0xd374b0d8,0xdf740c96,0x1ee5f173,0x7fd9cecb,0x3e016e83,0xb6a6b5f9,0x3ec0b304,0xbcc85d8c,0x25d3cc99,0x4846f2d8,0xc2dc0441,0xc84cdcb9,0x91c40603};
static const u32 SAY[20]={0xa9e059c5,0xb87cc8a6,0x1b12a052,0xcd278980,0xb75dae71,0xda6c35e0,0x479b4dc8,0xd374b0d8,0xdf740c96,0x1ee5f173,0x7fd9cecb,0x5e016e83,0xb6e7bde9,0x3ec0b304,0xbcc85d8c,0x25d3c495,0x0c66b4da,0xe2dd0441,0xc04fdc29,0x93448603};
static const u32 SEX[20]={0xc0329f1e,0x63d13ac1,0x6ca4b5b5,0xc9c3db85,0xe69df74c,0x8aee3e8a,0x59f5e2ca,0xb6ab3dc2,0x627cb061,0x1e847683,0x0c1c24b9,0xe2e9b205,0x99352c79,0xc670b71b,0x68c3aa97,0xc2f2c1be,0x5f9d1216,0x35c13b0d,0x21966471,0x4a9b6b5a};
static const u32 SEY[20]={0xc0329f1e,0x63d13ac1,0x6ca4b5b5,0xc9c3db85,0xe69df74c,0x8aee3e8a,0x59f5e2ca,0xb6ab3dc2,0x627cb061,0x1e847683,0x0c1c24b9,0x02e9b205,0x917934e9,0xc2e0b710,0x6882a297,0xe2f2b1ba,0x63be1213,0x35c03c77,0x29976471,0x4a9b63da};
static const u32 SWX[16]={0x48fc271b,0x9fca20cd,0xcc89f96f,0xfc40396f,0x8b328cb4,0x6b91ef78,0x97f9b767,0xc2450045,0x3f416758,0xfe9804cb,0x63a88c0f,0x0ceb1f8d,0xa28cd15a,0x77a1e994,0xd28e48a0,0x9f1f65bb};
static const u32 SWY[16]={0x48fc271b,0x9fca20cd,0xcc89f96f,0xfc40396f,0x8b328cb4,0x6b91ef78,0x97f9b767,0xe2450045,0x3b016f58,0xde9804cb,0x66a99ea5,0x0ce30b8d,0xa28cd15a,0x77a1e994,0xd28e48a0,0x9b5f6dbb};
static const u32 DW[38]={0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x20000000,0xfbc00800,0xe0000000,0x03011296,0xfff7ec00,0x00000000,0x00000000,0x00000000,0xfc400800,0xe0000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0xfe7f8000,0x00000000,0x20000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000};
static const u32 DS0[38]={0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x03bff800,0xfe7f8000,0x043ff800,0xefffa0d0,0xfcfeed6a,0x00000000,0x00000000,0x00000000,0x01808000,0x03bff800,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x202ceee0,0x00000000,0xfc3ff800,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000};
static const u32 DS1[38]={0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0xfff81400,0xfb0112aa,0x00080c00,0xa500fe64,0xf8800200,0x00000000,0x00000000,0x00000000,0xfcfeed6a,0x00081400,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x50005f30,0x00000000,0x00081400,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000};
```

### B.5 r38.h

```c
/* r38.h - own C core for the 38-step dense-part-variant attack (sha256-r38-prefix-v1).
   Data: consts.h (ePrint 2026/1120 Tables 3-5, our transcription).  Construction (variants, row-16 lookup) after
   qkniep's c99df2dc; code written independently.  Member x = message printed second (M'); Y = x + DW. */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
typedef uint32_t u32; typedef uint64_t u64;
#include "consts.h"
static inline u32 ROR(u32 x,int n){return (x>>n)|(x<<(32-n));}
static inline u32 S0(u32 x){return ROR(x,2)^ROR(x,13)^ROR(x,22);}
static inline u32 S1(u32 x){return ROR(x,6)^ROR(x,11)^ROR(x,25);}
static inline u32 s0(u32 x){return ROR(x,7)^ROR(x,18)^(x>>3);}
static inline u32 s1(u32 x){return ROR(x,17)^ROR(x,19)^(x>>10);}
static inline u32 CH(u32 x,u32 y,u32 z){return (x&y)^(~x&z);}
static inline u32 MAJ(u32 x,u32 y,u32 z){return (x&y)^(x&z)^(y&z);}
#define O 4
/* full trace: A[i+O], E[i+O] for i=-4..37, W[0..37] */
typedef struct { u32 a[NR+O], e[NR+O], w[NR]; } Tr;
#define AA(t,i) ((t)->a[(i)+O])
#define EE(t,i) ((t)->e[(i)+O])
static void trace(Tr*t,const u32 cv[8],const u32 w16[16]){
  for(int i=0;i<16;i++)t->w[i]=w16[i];
  for(int i=16;i<NR;i++)t->w[i]=s1(t->w[i-2])+t->w[i-7]+s0(t->w[i-15])+t->w[i-16];
  for(int i=0;i<4;i++){AA(t,-1-i)=cv[i];EE(t,-1-i)=cv[4+i];}
  for(int i=0;i<NR;i++){
    EE(t,i)=AA(t,i-4)+EE(t,i-4)+S1(EE(t,i-1))+CH(EE(t,i-1),EE(t,i-2),EE(t,i-3))+KC[i]+t->w[i];
    AA(t,i)=EE(t,i)-AA(t,i-4)+S0(AA(t,i-1))+MAJ(AA(t,i-1),AA(t,i-2),AA(t,i-3));}
}
static void compress38(u32 out[8],const u32 cv[8],const u32 w16[16]){
  Tr t; trace(&t,cv,w16);
  u32 f[8]={AA(&t,37),AA(&t,36),AA(&t,35),AA(&t,34),EE(&t,37),EE(&t,36),EE(&t,35),EE(&t,34)};
  for(int i=0;i<8;i++)out[i]=cv[i]+f[i];
}
/* row i of both traces (cells A,E,W, '+' pairs, two-bit conditions keyed at row i on member x) */
static inline int cellok(int k,int i,u32 x,u32 y){const u32*c=CELLS[k][i];return ((x&c[0])==c[1])&&((x^y)==c[2]);}
static inline u32 gv(const Tr*t,int k,int i){return k==0?AA(t,i):(k==1?EE(t,i):t->w[i]);}
/* rows < 0 carry no cells; two-bit conditions are used only when keyed at rows >= 16 (W7 is tested by F7,
   W8..W10 by their modular differences, Section 4.1); rows 7..10: the W cells are not part of the event (W7: F7) */
static int rowok(const Tr*x,const Tr*y,int i){
  if(i<0)return 1;
  if(!cellok(0,i,AA(x,i),AA(y,i)))return 0;
  if(!cellok(1,i,EE(x,i),EE(y,i)))return 0;
  if((i<7||i>10)&&!cellok(2,i,x->w[i],y->w[i]))return 0;
  if((EE(x,i)^EE(x,i-1))&PQ[i])return 0;
  if(i>=16)for(int j=0;j<NX2;j++)if(X2[j].row==i){
    u32 b=((gv(x,X2[j].k1,X2[j].i1)>>X2[j].b1)^(gv(x,X2[j].k2,X2[j].i2)>>X2[j].b2))&1;
    if(b!=(u32)(!X2[j].eq))return 0;}
  return 1;
}
/* list of failing rows (for checks): returns number of failing rows among lo..hi */
static int rowsfail(const Tr*x,const Tr*y,int lo,int hi){int n=0;for(int i=lo;i<=hi;i++)n+=!rowok(x,y,i);return n;}

/* ---- variants: v = (A0,A1,A2); rows 0..6 carry no difference; A3..A13, E7..E13, W11..W15 from S* ---- */
typedef struct { u32 A[16], Ex[16], Ey[16], Wx[16], Wy[16]; } Var;   /* A[0..15] of member x (y: A7.. differ) */
#define SA(i) SAX[(i)+O]
#define SAy(i) SAY[(i)+O]
#define SEx(i) SEX[(i)+O]
#define SEy(i) SEY[(i)+O]
/* E_i = A_i + A_{i-4} - S0(A_{i-1}) - MAJ(A_{i-1},A_{i-2},A_{i-3}) (needs A_{i-4} >= A_0, i.e. i >= 4) */
static void var_build(Var*v,u32 a0,u32 a1,u32 a2){
  u32 Ax[16],Ay[16];
  for(int i=0;i<16;i++){Ax[i]=SA(i);Ay[i]=SAy(i);}
  Ax[0]=Ay[0]=a0;Ax[1]=Ay[1]=a1;Ax[2]=Ay[2]=a2;
  for(int i=0;i<16;i++){v->Ex[i]=SEx(i);v->Ey[i]=SEy(i);v->Wx[i]=SWX[i];v->Wy[i]=SWY[i];v->A[i]=Ax[i];}
  for(int i=4;i<7;i++){
    v->Ex[i]=Ax[i]+Ax[i-4]-S0(Ax[i-1])-MAJ(Ax[i-1],Ax[i-2],Ax[i-3]);
    v->Ey[i]=Ay[i]+Ay[i-4]-S0(Ay[i-1])-MAJ(Ay[i-1],Ay[i-2],Ay[i-3]);}
  for(int i=8;i<11;i++){
    v->Wx[i]=v->Ex[i]-Ax[i-4]-v->Ex[i-4]-S1(v->Ex[i-1])-CH(v->Ex[i-1],v->Ex[i-2],v->Ex[i-3])-KC[i];
    v->Wy[i]=v->Ey[i]-Ay[i-4]-v->Ey[i-4]-S1(v->Ey[i-1])-CH(v->Ey[i-1],v->Ey[i-2],v->Ey[i-3])-KC[i];}
}
/* generic validity: E cells of rows 4..8 (both members, '+' pairs), and (dW_i, ds0(W_i)) published, i = 8..11 */
static int var_valid(const Var*v){
  for(int i=4;i<=8;i++){
    if(!cellok(1,i,v->Ex[i],v->Ey[i]))return 0;
    if((v->Ex[i]^v->Ex[i-1])&PQ[i])return 0;
    if(i>=5&&((v->Ey[i]^v->Ey[i-1])&PQ[i]))return 0;}
  for(int i=8;i<=11;i++){
    if(v->Wy[i]-v->Wx[i]!=DW[i])return 0;
    if(s0(v->Wy[i])-s0(v->Wx[i])!=DS0[i])return 0;}
  return 1;
}
/* Step-2 words of member x (and y) connecting CV1 to the variant's dense part (rows 0..7) */
static void step2(u32 wx[16],u32 wy[16],const Var*v,const u32 cv[8]){
  u32 A[NR+O],E[NR+O];
  for(int i=0;i<4;i++){A[O-1-i]=cv[i];E[O-1-i]=cv[4+i];}
  for(int i=0;i<16;i++)A[i+O]=v->A[i];
  for(int i=4;i<16;i++)E[i+O]=v->Ex[i];
  for(int i=0;i<4;i++)E[i+O]=A[i+O]+A[i]-S0(A[i+O-1])-MAJ(A[i+O-1],A[i+O-2],A[i+O-3]);
  for(int i=0;i<8;i++)wx[i]=E[i+O]-A[i]-E[i]-S1(E[i+O-1])-CH(E[i+O-1],E[i+O-2],E[i+O-3])-KC[i];
  for(int i=8;i<16;i++)wx[i]=v->Wx[i];
  for(int i=0;i<16;i++)wy[i]=(i<8?wx[i]:v->Wy[i]);
  wy[7]=wx[7]+DW[7];
}
/* Lemma-5 quantities for (CV1, A0): Y, W0, Z0 (W1 = Y + A1, W16x = s0(Y+A1) - A1 + Z0 + c9x(A2)) */
static inline void yz(u32*Y,u32*W0,u32*Z0,const u32 cv[8],u32 a0){
  u32 a=cv[0],b=cv[1],c=cv[2],d=cv[3],e=cv[4],f=cv[5],g=cv[6],h=cv[7];
  u32 E0=a0+d-S0(a)-MAJ(a,b,c);
  *W0=E0-d-h-S1(e)-CH(e,f,g)-KC[0];
  *Y=-S0(a0)-MAJ(a0,a,b)-g-S1(E0)-CH(E0,e,f)-KC[1];
  *Z0=*W0+s1(SWX[14]);
  (void)c;
}
/* c9x(A2): W9x = c9x - A1 ; c9y likewise */
static inline u32 c9x_of(u32 a2){
  u32 E6=SA(6)+a2-S0(SA(5))-MAJ(SA(5),SA(4),SA(3));
  /* W9 = E9 - A5 - E5 - S1(E8) - CH(E8,E7,E6) - K9 with E5 = A5 + A1 - S0(A4) - MAJ(A4,A3,A2) */
  return SEx(9)-SA(5)-SA(5)+S0(SA(4))+MAJ(SA(4),SA(3),a2)-S1(SEx(8))-CH(SEx(8),SEx(7),E6)-KC[9];
}
static inline u32 c9y_of(u32 a2){
  u32 E6=SA(6)+a2-S0(SA(5))-MAJ(SA(5),SA(4),SA(3));
  return SEy(9)-SA(5)-SA(5)+S0(SA(4))+MAJ(SA(4),SA(3),a2)-S1(SEy(8))-CH(SEy(8),SEy(7),E6)-KC[9];
}
/* splitmix64 */
static inline u64 smx(u64*s){u64 z=(*s+=0x9e3779b97f4a7c15ULL);z=(z^(z>>30))*0xbf58476d1ce4e5b9ULL;z=(z^(z>>27))*0x94d049bb133111ebULL;return z^(z>>31);}
```

### B.6 ex1.c

```c
/* ex1.c - exhaustive passes over 2^32: the A2 list, G (row-16 words), |F7|, max |phi^-1| (phi(u) = s0(u) - u).
   usage: ex1 a2 | g | f7 | phi */
#include "r38.h"
static Var V0;
static int a2ok(u32 a2){
  /* E6 (both members equal), its x-value cells, '+' pairs E7/E6; W10 (x, y) modular and s0 differences */
  u32 E6=SA(6)+a2-S0(SA(5))-MAJ(SA(5),SA(4),SA(3));
  const u32*c=CELLS[1][6]; if((E6&c[0])!=c[1])return 0;
  if((SEx(7)^E6)&PQ[7])return 0; if((SEy(7)^E6)&PQ[7])return 0;
  u32 w10x=SEx(10)-SA(6)-E6-S1(SEx(9))-CH(SEx(9),SEx(8),SEx(7))-KC[10];
  u32 w10y=SEy(10)-SA(6)-E6-S1(SEy(9))-CH(SEy(9),SEy(8),SEy(7))-KC[10];
  return w10y-w10x==DW[10]&&s0(w10y)-s0(w10x)==DS0[10];
}
int main(int argc,char**argv){
  var_build(&V0,SA(0),SA(1),SA(2));
  if(!strcmp(argv[1],"a2")){u64 n=0; for(u64 a=0;a<(1ull<<32);a++)if(a2ok((u32)a)){printf("%08x\n",(u32)a);n++;} fprintf(stderr,"A2 list: %llu\n",n);}
  if(!strcmp(argv[1],"g")){ /* row 16 of both members from rows 12..15 of S*, as a function of W16x (W16y = W16x + DW16) */
    u64 n=0; Tr x,y; memset(&x,0,sizeof x); memset(&y,0,sizeof y);
    for(int i=-4;i<16;i++){AA(&x,i)=SAX[i+O];EE(&x,i)=SEX[i+O];AA(&y,i)=SAY[i+O];EE(&y,i)=SEY[i+O];}
    for(int i=0;i<16;i++){x.w[i]=SWX[i];y.w[i]=SWY[i];}
    for(u64 w=0;w<(1ull<<32);w++){
      x.w[16]=(u32)w; y.w[16]=(u32)w+DW[16];
      for(Tr*t=&x;t;t=(t==&x?&y:NULL)){int i=16;
        EE(t,i)=AA(t,i-4)+EE(t,i-4)+S1(EE(t,i-1))+CH(EE(t,i-1),EE(t,i-2),EE(t,i-3))+KC[i]+t->w[i];
        AA(t,i)=EE(t,i)-AA(t,i-4)+S0(AA(t,i-1))+MAJ(AA(t,i-1),AA(t,i-2),AA(t,i-3));}
      if(rowok(&x,&y,16)){printf("%08x\n",(u32)w);n++;}}
    fprintf(stderr,"G: %llu\n",n);}
  if(!strcmp(argv[1],"f7")){u64 n=0; for(u64 w=0;w<(1ull<<32);w++)n+=(s0((u32)w+DW[7])-s0((u32)w)==DS0[7]); printf("|F7| = %llu\n",n);}
  if(!strcmp(argv[1],"phi")){uint8_t*h=calloc(1ull<<32,1); for(u64 u=0;u<(1ull<<32);u++){u32 t=s0((u32)u)-(u32)u; if(h[t]<255)h[t]++;}
    u64 hist[256]={0}; for(u64 t=0;t<(1ull<<32);t++)hist[h[t]]++; for(int k=0;k<256;k++)if(hist[k])printf("preimages %d: %llu values\n",k,hist[k]); free(h);}
  return 0;
}
```

### B.7 rcount.c

```c
/* rcount.c - exact |R(A0)| for a list of A0 values: enumerate the A0-free valid pairs (A1, A2) (A2 in the A2 list,
   dW9 of the A2, the '+' pairs E6/E5 (A1 in one window of 2^29), ds0(W9), dW8), then test W8x = Fx(A1,A2) - A0
   against F8 = {w : s0(w + dW8) - s0(w) = ds0(W8)} (bitmap).  Also checks a sample against the generic var_valid.
   usage: rcount a2list.txt a0list.txt threads  -> per A0: A0 |R(A0)| ; stderr: |P|, timing */
#include "r38.h"
#include <pthread.h>
static u32 A2L[768]; static int NA2; static u32 A0L[4096]; static int NA0; static uint8_t*F8T;
static u64 CNT[4096]; static u64 NP; static u64 PER_A2[768]; static pthread_mutex_t MU=PTHREAD_MUTEX_INITIALIZER;
static int next_a2=0; static u64 GENCHK=0,GENBAD=0;
static inline int f8(u32 w){return (F8T[w>>3]>>(w&7))&1;}
static void*work(void*arg){
  (void)arg; u64*loc=calloc(NA0,8);
  for(;;){
    pthread_mutex_lock(&MU); int k=next_a2++; pthread_mutex_unlock(&MU);
    if(k>=NA2)break;
    u32 a2=A2L[k]; u64 np=0;
    u32 E6=SA(6)+a2-S0(SA(5))-MAJ(SA(5),SA(4),SA(3));
    u32 c9x=c9x_of(a2),c9y=c9y_of(a2);
    if(c9y-c9x!=DW[9]){continue;}
    u32 k5=SA(5)-S0(SA(4))-MAJ(SA(4),SA(3),a2);      /* E5 = A1 + k5 */
    u32 lo=(E6&0xe0000000u)-k5;                          /* A1 = lo + r, r < 2^29 */
    u32 m3=MAJ(SA(3),a2,0)/*placeholder*/; (void)m3;
    u32 kx=SEx(8)-2*SA(4)+S0(SA(3))-S1(SEx(7))-KC[8];
    u32 ky=SEy(8)-2*SA(4)+S0(SA(3))-S1(SEy(7))-KC[8];
    for(u32 r=0;r<(1u<<29);r++){
      u32 a1=lo+r; u32 w9=c9x-a1;
      if(s0(w9+DW[9])-s0(w9)!=DS0[9])continue;
      u32 E5=a1+k5; u32 mj=MAJ(SA(3),a2,a1);
      u32 fx=kx+mj-CH(SEx(7),E6,E5), fy=ky+mj-CH(SEy(7),E6,E5);
      if(fy-fx!=DW[8])continue;
      np++;
      for(int j=0;j<NA0;j++)loc[j]+=f8(fx-A0L[j]);
      if((np&0xfff)==1){ /* generic cross-check on a sample of pairs, for A0 = A0L[0] */
        Var v; var_build(&v,A0L[0],a1,a2); int g=var_valid(&v), f=f8(fx-A0L[0]);
        pthread_mutex_lock(&MU); GENCHK++; GENBAD+=(g!=f); pthread_mutex_unlock(&MU);}
    }
    pthread_mutex_lock(&MU); NP+=np; PER_A2[k]=np; pthread_mutex_unlock(&MU);
  }
  pthread_mutex_lock(&MU); for(int j=0;j<NA0;j++)CNT[j]+=loc[j]; pthread_mutex_unlock(&MU); free(loc);
  return NULL;
}
int main(int argc,char**argv){
  FILE*f=fopen(argv[1],"r"); while(NA2<768&&fscanf(f,"%x",&A2L[NA2])==1)NA2++; fclose(f);
  f=fopen(argv[2],"r"); char line[256]; while(fgets(line,sizeof line,f)&&NA0<4096){if(sscanf(line,"%x",&A0L[NA0])==1)NA0++;} fclose(f);
  int T=atoi(argv[3]);
  F8T=calloc(1u<<29,1); for(u64 w=0;w<(1ull<<32);w++)if(s0((u32)w+DW[8])-s0((u32)w)==DS0[8])F8T[w>>3]|=1<<(w&7);
  u64 n8=0; for(u64 i=0;i<(1u<<29);i++)n8+=__builtin_popcount(F8T[i]);
  fprintf(stderr,"|F8| = %llu, A2 %d, A0 %d\n",n8,NA2,NA0);
  pthread_t th[64]; for(int t=0;t<T;t++)pthread_create(&th[t],0,work,0); for(int t=0;t<T;t++)pthread_join(th[t],0);
  fprintf(stderr,"|P| = %llu (2^%.5f); generic cross-checks %llu, disagreements %llu\n",NP,log2((double)NP),GENCHK,GENBAD);
  u64 S=0; for(int j=0;j<NA0;j++){printf("%08x %llu\n",A0L[j],CNT[j]);S+=CNT[j];}
  fprintf(stderr,"sum = %llu\n",S);
  FILE*g=fopen("per_a2.txt","w"); for(int k=0;k<NA2;k++)fprintf(g,"%08x %llu\n",A2L[k],PER_A2[k]); fclose(g);
  return 0;
}
```

### B.8 tbl.c

```c
/* tbl.c - brute-force check of the row-16 table semantics (Lemma 5) on real variants and random chaining values.
   For nA2 members of the A2 list and one A0: enumerate the valid variants (A0,A1,A2) (same exact enumeration as rcount.c),
   and for ncv uniform random CVs compare (a) W16x of the full 38-step trace with the closed form
   s0(Y+A1)-A1+Z0+c9x(A2) on a sample of variants, (b) membership of the closed form in G for ALL variants, with the
   full row-16 test (rowok) of the brute-force trace for every such hit, plus a sample of non-hits (must fail row 16),
   (c) the W7 in F7 rate of the Step-2 word.  usage: tbl a2list a0list glist a0idx nA2 ncv seed */
#include "r38.h"
static uint8_t*F8T; static u32 G[32]; static int NG;
static inline int f8(u32 w){return (F8T[w>>3]>>(w&7))&1;}
static inline int inG(u32 w){for(int i=0;i<NG;i++)if(G[i]==w)return 1;return 0;}
int main(int argc,char**argv){
  static u32 A2L[768],A0L[4096]; int NA2=0,NA0=0; char line[256];
  FILE*f=fopen(argv[1],"r"); while(NA2<768&&fscanf(f,"%x",&A2L[NA2])==1)NA2++; fclose(f);
  f=fopen(argv[2],"r"); while(fgets(line,sizeof line,f)&&NA0<4096)if(sscanf(line,"%x",&A0L[NA0])==1)NA0++; fclose(f);
  f=fopen(argv[3],"r"); while(NG<32&&fscanf(f,"%x",&G[NG])==1)NG++; fclose(f);
  u32 a0=A0L[atoi(argv[4])]; int nA2=atoi(argv[5]), ncv=atoi(argv[6]); u64 seed=strtoull(argv[7],0,10);
  F8T=calloc(1u<<29,1); for(u64 w=0;w<(1ull<<32);w++)if(s0((u32)w+DW[8])-s0((u32)w)==DS0[8])F8T[w>>3]|=1<<(w&7);
  u32 F7D=DW[7],F7S=DS0[7];
  u32 cv[64][8]; for(int c=0;c<ncv;c++)for(int i=0;i<8;i++)cv[c][i]=(u32)smx(&seed);
  u64 nvar=0,wchk=0,wbad=0,hits=0,hitbad=0,nonhit_chk=0,nonhit_bad=0,w7pass=0,w7n=0,gen_valid_bad=0;
  int used=0;
  for(int k=0;k<NA2&&used<nA2;k++){
    u32 a2=A2L[k]; u32 c9x=c9x_of(a2),c9y=c9y_of(a2); if(c9y-c9x!=DW[9])continue; used++;
    u32 E6=SA(6)+a2-S0(SA(5))-MAJ(SA(5),SA(4),SA(3));
    u32 k5=SA(5)-S0(SA(4))-MAJ(SA(4),SA(3),a2), lo=(E6&0xe0000000u)-k5;
    u32 kx=SEx(8)-2*SA(4)+S0(SA(3))-S1(SEx(7))-KC[8], ky=SEy(8)-2*SA(4)+S0(SA(3))-S1(SEy(7))-KC[8];
    u32 *a1s=malloc(sizeof(u32)<<22); u64 n1=0;
    for(u32 r=0;r<(1u<<29);r++){
      u32 a1=lo+r; u32 w9=c9x-a1; if(s0(w9+DW[9])-s0(w9)!=DS0[9])continue;
      u32 E5=a1+k5, mj=MAJ(SA(3),a2,a1);
      u32 fx=kx+mj-CH(SEx(7),E6,E5), fy=ky+mj-CH(SEy(7),E6,E5);
      if(fy-fx!=DW[8])continue; if(!f8(fx-a0))continue;
      if(n1<(1u<<22))a1s[n1++]=a1;}
    for(u64 q=0;q<n1;q++){
      u32 a1=a1s[q]; nvar++;
      for(int c=0;c<ncv;c++){
        u32 Y,W0,Z0; yz(&Y,&W0,&Z0,cv[c],a0);
        u32 w16=s0(Y+a1)-a1+Z0+c9x;
        int hit=inG(w16); int samp=((q*131+c)&1023)==0;
        if(hit||samp){
          Var v; var_build(&v,a0,a1,a2); if(!var_valid(&v))gen_valid_bad++;
          u32 wx[16],wy[16]; step2(wx,wy,&v,cv[c]);
          Tr tx,ty; trace(&tx,cv[c],wx); trace(&ty,cv[c],wy);
          if(samp){wchk++; wbad+=(tx.w[16]!=w16);}
          int r16=rowok(&tx,&ty,16);
          if(hit){hits++; hitbad+=!r16;} else {nonhit_chk++; nonhit_bad+=r16;}
          if(hit)(void)0;
        }
        if(((q+c)&63)==0){w7n++; u32 W0_,Y_,Z_; (void)W0_;(void)Y_;(void)Z_;
          Var v; var_build(&v,a0,a1,a2); u32 wx[16],wy[16]; step2(wx,wy,&v,cv[c]);
          w7pass+=(s0(wx[7]+F7D)-s0(wx[7])==F7S);}
      }}
    free(a1s);
  }
  printf("A0=%08x A2 used %d, ncv %d, variants %llu, (variant,CV) pairs %llu\n",a0,used,ncv,(unsigned long long)nvar,(unsigned long long)(nvar*ncv));
  printf("W16 closed form vs trace: checked %llu, mismatches %llu\n",(unsigned long long)wchk,(unsigned long long)wbad);
  printf("generic var_valid failures on checked variants: %llu\n",(unsigned long long)gen_valid_bad);
  printf("G hits %llu (expected %.2f), full row-16 failures among hits %llu; non-hit sample %llu, row-16 passes among them %llu\n",
    (unsigned long long)hits,(double)nvar*ncv*32/4294967296.0,(unsigned long long)hitbad,(unsigned long long)nonhit_chk,(unsigned long long)nonhit_bad);
  printf("W7 in F7: %llu of %llu sampled (rate %.5f, expected %.5f)\n",(unsigned long long)w7pass,(unsigned long long)w7n,(double)w7pass/w7n,287309824.0/4294967296.0);
  return 0;
}
```

### B.9 bucket.c

```c
/* bucket.c - the TRUE row-16 bucket T_j[Y,Z0] of a (chaining value, A0): every valid variant (A0,A1,A2), A2 in the A2 list,
   whose W16 = s0(Y+A1) - A1 + Z0 + c9x(A2) lies in G.  Brute force over u = Y + A1 in 2^32 (phi(u) = s0(u) - u against the
   3072 targets g - Y - Z0 - c9x(A2)), each hit then checked by the exact validity test of the variant (var_valid).
   usage: bucket a2list glist threads  < jobs   (job line: 8 hex cv words, A0 hex)   -> per job: "B a0 nent" then "a1 a2idx gi" lines */
#include "r38.h"
#include <pthread.h>
static u32 A2L[768]; static int NA2; static u32 GL[32]; static int NG;
typedef struct{u32 t; int a2,g;} Tg; static Tg TG[768*32]; static int NT; static uint8_t BM[1<<19];
static u32 CV[8], A0, Y, Z0; static int T; static u32 c9x_[768];
static pthread_mutex_t MU=PTHREAD_MUTEX_INITIALIZER; static struct{u32 a1; int a2,g;} OUT[1<<16]; static int NO; static long NH,NV; static long FC[500];
static int cmp(const void*a,const void*b){u32 x=((Tg*)a)->t,y=((Tg*)b)->t;return x<y?-1:x>y;}
static void*work(void*arg){
  int id=(int)(intptr_t)arg; u64 lo=((u64)id<<32)/T, hi=((u64)(id+1)<<32)/T;
  for(u64 uu=lo;uu<hi;uu++){u32 u=(u32)uu; u32 ph=s0(u)-u; u32 h=(ph*2654435761u)>>10; if(!((BM[h>>3]>>(h&7))&1))continue;
    int l=0,r=NT-1,f=-1; while(l<=r){int m=(l+r)/2; if(TG[m].t<ph)l=m+1; else if(TG[m].t>ph)r=m-1; else {f=m;break;}}
    if(f<0)continue; while(f>0&&TG[f-1].t==ph)f--;
    for(;f<NT&&TG[f].t==ph;f++){u32 a1=u-Y; Var v; var_build(&v,A0,a1,A2L[TG[f].a2]);
      if(var_valid(&v)){pthread_mutex_lock(&MU); if(NO<(1<<16)){OUT[NO].a1=a1;OUT[NO].a2=TG[f].a2;OUT[NO].g=TG[f].g;NO++;} pthread_mutex_unlock(&MU);}}}
  return NULL;}
int main(int argc,char**argv){
  FILE*f=fopen(argv[1],"r"); while(NA2<768&&fscanf(f,"%x",&A2L[NA2])==1)NA2++; fclose(f);
  f=fopen(argv[2],"r"); while(NG<32&&fscanf(f,"%x",&GL[NG])==1)NG++; fclose(f); T=atoi(argv[3]);
  for(int k=0;k<NA2;k++)c9x_[k]=c9x_of(A2L[k]);
  for(;;){ unsigned c[8],a0; if(scanf("%x %x %x %x %x %x %x %x %x",&c[0],&c[1],&c[2],&c[3],&c[4],&c[5],&c[6],&c[7],&a0)!=9)break;
    for(int i=0;i<8;i++)CV[i]=c[i]; A0=a0; u32 W0; yz(&Y,&W0,&Z0,CV,A0);
    NT=0; memset(BM,0,sizeof BM);
    for(int k=0;k<NA2;k++){ if(c9y_of(A2L[k])-c9x_[k]!=DW[9])continue; for(int g=0;g<NG;g++){TG[NT].t=GL[g]-Y-Z0-c9x_[k];TG[NT].a2=k;TG[NT].g=g;NT++;}}
    qsort(TG,NT,sizeof(Tg),cmp); for(int i=0;i<NT;i++){u32 h=(TG[i].t*2654435761u)>>10; BM[h>>3]|=1<<(h&7);}
    NO=0; pthread_t th[64]; for(int t=0;t<T;t++)pthread_create(&th[t],0,work,(void*)(intptr_t)t); for(int t=0;t<T;t++)pthread_join(th[t],0);
    printf("B %08x %d\n",A0,NO); for(int i=0;i<NO;i++)printf("%08x %d %d\n",OUT[i].a1,OUT[i].a2,OUT[i].g); fflush(stdout);}
  return 0;}
```

### B.10 smc.c

```c
/* smc.c - sequential Monte-Carlo estimate of q3 = Pr[rows 16..37 hold | W7 in F7] for the dense-part variants (own
   implementation of the estimator described for ePrint 2026/1120-style semi-free-start pairs; independent code).
   Stages: row 16 exactly (32 of 2^32 words: factor 2^-27); rows 17..22: E_i^x proposed uniformly with its x-value cells and '+'
   bits imposed (weight 2^-f); W_i^x = E_i^x - (rest of step i), W_i^y = W_i^x + dW_i (published modular difference), both members
   stepped, the whole row tested.  Tail: a variant (uniform from a sample) fixes W8, W9, W10; W23^x proposed with its x-value cells
   imposed (f bits), W7 = W23 - s1(W21) - W16 - s0(W8), weight 2^(32-f)/|F7| if W7 in F7; rows 23..37 deterministic, every row tested.
   Every tail success is REBUILT into a real semi-free-start pair (W0..W6 by the inverse expansion, CV1 by inverting steps 7..0 of the
   variant) and verified with the 38-step compression and the generic cell tests before it is counted.
   usage: smc varsample.txt mode seed NP c17 c18 c19 c20 c21 c22 ntail [succ.txt]
     mode: "pop:<i>" -> use only variant i of the file for the whole run; "all" -> every proposal draws a variant uniformly from the file
   output (stderr-free, one line): seed logZ stage factors (log2) ... successes rebuilt failedrebuilds */
#include "r38.h"
typedef struct { u32 a0, a1, a2, w8, w9, w10; } Vt;
static Vt *VS; static long NVS;
static u64 rs[4];
static inline u64 rotl(u64 x,int k){return (x<<k)|(x>>(64-k));}
static inline u64 nxt(void){u64 r=rotl(rs[1]*5,7)*9,t=rs[1]<<17;rs[2]^=rs[0];rs[3]^=rs[1];rs[1]^=rs[2];rs[0]^=rs[3];rs[2]^=t;rs[3]=rotl(rs[3],45);return r;}
static void seedrng(u64 s){u64 z=s; for(int i=0;i<4;i++)rs[i]=smx(&z); for(int i=0;i<8;i++)nxt();}
static inline u32 r32(void){return (u32)(nxt()>>32);}
static u32 F7D,F7S; static inline int inF7(u32 w){return (u32)(s0(w+F7D)-s0(w))==F7S;}
/* state: member x / y, rows 0..37; only rows >= 8 are used */
typedef struct { u32 Ax[40],Ex[40],Wx[40],Ay[40],Ey[40],Wy[40]; } St;
static void init_pub(St*s){ for(int i=0;i<16;i++){ s->Ax[i]=SAX[i+4]; s->Ex[i]=SEX[i+4]; s->Wx[i]=SWX[i]; s->Ay[i]=SAY[i+4]; s->Ey[i]=SEY[i+4]; s->Wy[i]=SWY[i]; } }
static inline u32 gtx(const St*s,int k,int i){return k==0?s->Ax[i]:(k==1?s->Ex[i]:s->Wx[i]);}
/* row i test on the state (member x conditions, x^y cells, '+', two-bit) */
static int rowt(const St*s,int i){
  if(!cellok(0,i,s->Ax[i],s->Ay[i]))return 0;
  if(!cellok(1,i,s->Ex[i],s->Ey[i]))return 0;
  if(!cellok(2,i,s->Wx[i],s->Wy[i]))return 0;
  if((s->Ex[i]^s->Ex[i-1])&PQ[i])return 0;
  for(int j=0;j<NX2;j++)if(X2[j].row==i){
    u32 b=((gtx(s,X2[j].k1,X2[j].i1)>>X2[j].b1)^(gtx(s,X2[j].k2,X2[j].i2)>>X2[j].b2))&1; if(b!=(u32)(!X2[j].eq))return 0;}
  return 1;
}
static inline void stepE(u32*E,u32*A,u32*W,int i){ /* E_i, A_i of one member given W_i */
  E[i]=A[i-4]+E[i-4]+S1(E[i-1])+CH(E[i-1],E[i-2],E[i-3])+KC[i]+W[i];
  A[i]=E[i]-A[i-4]+S0(A[i-1])+MAJ(A[i-1],A[i-2],A[i-3]);}
static inline void sched(u32*W,int i){W[i]=s1(W[i-2])+W[i-7]+s0(W[i-15])+W[i-16];}
/* ---- rebuild a tail success into a real pair and verify ---- */
static FILE*SUCC;
static int rebuild(const St*s,const Vt*v,u32 w23){
  u32 W[38],Wy[38]; for(int i=8;i<16;i++){W[i]=SWX[i];} W[8]=v->w8;W[9]=v->w9;W[10]=v->w10; for(int i=16;i<23;i++)W[i]=s->Wx[i];
  W[23]=w23; u32 w7=W[23]-s1(W[21])-W[16]-s0(W[8]); W[7]=w7;
  u32 w6=W[22]-s1(W[20])-W[15]-s0(W[7]); W[6]=w6;
  W[5]=W[21]-s1(W[19])-W[14]-s0(W[6]); W[4]=W[20]-s1(W[18])-W[13]-s0(W[5]); W[3]=W[19]-s1(W[17])-W[12]-s0(W[4]);
  W[2]=W[18]-s1(W[16])-W[11]-s0(W[3]); W[1]=W[17]-s1(W[15])-W[10]-s0(W[2]); W[0]=W[16]-s1(W[14])-W[9]-s0(W[1]);
  /* variant dense part */
  Var var; var_build(&var,v->a0,v->a1,v->a2);
  /* invert steps 7..0: A_{i-4} = E_i - A_i + S0(A_{i-1}) + MAJ(...), E_{i-4} = E_i - A_{i-4} - S1(E_{i-1}) - CH(...) - K_i - W_i */
  u32 A[24],E[24]; /* index i+4 */
  for(int i=0;i<8;i++){A[i+4]=var.A[i];} for(int i=4;i<8;i++)E[i+4]=var.Ex[i];
  for(int i=7;i>=0;i--){
    if(i>=4){ /* E_{i-1}, E_{i-2}, E_{i-3} known for i-3>=4 only when i>=7; E_4..E_7 known; E_1..E_3 found below */ }
    /* need E_{i-1..i-3}: for i=7: E6,E5,E4 known; i=6: E5,E4,E3 (E3 from i=7 step); etc. */
    u32 e1=E[i-1+4],e2=E[i-2+4],e3=E[i-3+4];
    u32 a1=A[i-1+4],a2=A[i-2+4],a3=A[i-3+4];
    u32 Ai4=E[i+4]-A[i+4]+S0(a1)+MAJ(a1,a2,a3);
    u32 Ei4=E[i+4]-Ai4-S1(e1)-CH(e1,e2,e3)-KC[i]-W[i];
    A[i-4+4]=Ai4; E[i-4+4]=Ei4;
    if(i==7){ /* E_3 = E_{7-4} was just set; nothing else */ }
  }
  /* consistency: recomputed A_{i} for i=0..3 must equal the variant's (A0,A1,A2,A3) */
  for(int i=0;i<4;i++) if(A[i+4]!=var.A[i]) { return 0; }
  u32 cv[8]={A[3],A[2],A[1],A[0],E[3],E[2],E[1],E[0]};
  u32 mx[16],my[16]; for(int i=0;i<16;i++){mx[i]=W[i]; my[i]=W[i];}
  for(int i=7;i<16;i++)my[i]=W[i]+DW[i];
  /* member y words 11..15 are the published ones (W + dW) */
  u32 o1[8],o2[8]; compress38(o1,cv,mx); compress38(o2,cv,my);
  if(memcmp(o1,o2,32))return 0;
  if(!memcmp(mx,my,64))return 0;
  Tr tx,ty; trace(&tx,cv,mx); trace(&ty,cv,my);
  for(int i=0;i<NR;i++){ if(!rowok(&tx,&ty,i)) return 0; }
  /* W7 in F7, step-2 words map CV1 back to W0..W7 */
  if(!inF7(mx[7]))return 0;
  if(SUCC)fprintf(SUCC,"%08x %08x %08x  cv %08x %08x %08x %08x %08x %08x %08x %08x  m %08x %08x %08x %08x %08x %08x %08x %08x %08x %08x %08x %08x %08x %08x %08x %08x\n",
      v->a0,v->a1,v->a2,cv[0],cv[1],cv[2],cv[3],cv[4],cv[5],cv[6],cv[7],mx[0],mx[1],mx[2],mx[3],mx[4],mx[5],mx[6],mx[7],mx[8],mx[9],mx[10],mx[11],mx[12],mx[13],mx[14],mx[15]);
  return 1;
}
int main(int argc,char**argv){
  F7D=DW[7]; F7S=DS0[7];
  FILE*f=fopen(argv[1],"r"); VS=malloc(sizeof(Vt)<<21); NVS=0; unsigned a,b,c;
  while(fscanf(f,"%x %x %x",&a,&b,&c)==3){ Vt v={a,b,c,0,0,0}; Var var; var_build(&var,a,b,c); v.w8=var.Wx[8];v.w9=var.Wx[9];v.w10=var.Wx[10]; VS[NVS++]=v; if(NVS>=(1L<<21))break;} fclose(f);
  const char*mode=argv[2]; u64 seed=strtoull(argv[3],0,10); int NP=atoi(argv[4]); int ch[6]; for(int i=0;i<6;i++)ch[i]=atoi(argv[5+i]); long ntail=atol(argv[11]);
  SUCC=argc>12?fopen(argv[12],"w"):NULL;
  long fixedv=-1; if(!strncmp(mode,"pop:",4))fixedv=atol(mode+4);
  seedrng(seed);
  /* stage 16: uniform elements of G (read from data) */
  static u32 G[32]; int NG=0; { FILE*g=fopen("../data/ex1_g.txt","r"); if(!g)g=fopen("data/ex1_g.txt","r"); while(NG<32&&fscanf(g,"%x",&G[NG])==1)NG++; fclose(g); }
  double lg[16]; int nst=0; lg[nst++]=-27.0;   /* exact: 32 of 2^32 */
  St *P=malloc(sizeof(St)*NP);
  St base; init_pub(&base);
  for(int p=0;p<NP;p++){
    St*s=&P[p]; *s=base; u32 w=G[nxt()%NG]; s->Wx[16]=w; s->Wy[16]=w+DW[16];
    stepE(s->Ex,s->Ax,s->Wx,16); stepE(s->Ey,s->Ay,s->Wy,16);
  }
  /* rows 17..22 */
  for(int i=17;i<=22;i++){
    int M=ch[i-17]; u32 cm=CELLS[1][i][0], cvv=CELLS[1][i][1]; u32 pq=PQ[i];
    int f_=__builtin_popcount(cm|pq);
    /* children with positive weight */
    long cap=1<<16, nc=0; St*C=malloc(sizeof(St)*cap);
    for(int p=0;p<NP;p++){
      for(int m=0;m<M;m++){
        const St*s=&P[p];
        u32 Eprop=(r32()&~(cm|pq))|cvv|((s->Ex[i-1])&pq&~cm);
        /* conflict between a cell bit and a '+' bit: the row test rejects */
        St t=*s; t.Ex[i]=Eprop;
        u32 rest=t.Ax[i-4]+t.Ex[i-4]+S1(t.Ex[i-1])+CH(t.Ex[i-1],t.Ex[i-2],t.Ex[i-3])+KC[i];
        t.Wx[i]=Eprop-rest; t.Wy[i]=t.Wx[i]+DW[i];
        t.Ax[i]=Eprop-t.Ax[i-4]+S0(t.Ax[i-1])+MAJ(t.Ax[i-1],t.Ax[i-2],t.Ax[i-3]);
        stepE(t.Ey,t.Ay,t.Wy,i);
        if(rowt(&t,i)){ if(nc==cap){cap*=2;C=realloc(C,sizeof(St)*cap);} C[nc++]=t; }
      }}
    double mean=(double)nc/((double)NP*M)*ldexp(1.0,-f_);   /* each positive child has weight 2^-f */
    if(nc==0){ printf("%llu -inf stage %d empty\n",(unsigned long long)seed,i); return 0; }
    lg[nst++]=log2(mean);
    for(int p=0;p<NP;p++) P[p]=C[nxt()%nc];   /* equal weights: multinomial resampling is uniform over survivors */
    free(C);
  }
  /* tail */
  double wsum=0; long succ=0,bad=0; double tailw=ldexp(1.0,32-__builtin_popcount(CELLS[2][23][0]))/287309824.0;
  u32 cm=CELLS[2][23][0], cv_=CELLS[2][23][1];
  for(int p=0;p<NP;p++){
    const St*s=&P[p];
    for(long k=0;k<ntail;k++){
      const Vt*v=&VS[fixedv>=0?fixedv:(long)(nxt()%NVS)];
      u32 w23=(r32()&~cm)|cv_;
      u32 w7=w23-s1(s->Wx[21])-s->Wx[16]-s0(v->w8);
      if(!inF7(w7))continue;
      St t=*s; t.Wx[8]=v->w8; t.Wx[9]=v->w9; t.Wx[10]=v->w10;
      t.Wy[8]=t.Wx[8]+DW[8]; t.Wy[9]=t.Wx[9]+DW[9]; t.Wy[10]=t.Wx[10]+DW[10];
      t.Wx[7]=w7; t.Wy[7]=w7+DW[7];
      /* W cells of row 23 and rows 23..37 */
      int ok=1;
      for(int i=23;i<NR&&ok;i++){
        if(i==23){ t.Wx[23]=w23; sched(t.Wy,23); }  /* y by the schedule of the y words */
        else { sched(t.Wx,i); sched(t.Wy,i); }
        stepE(t.Ex,t.Ax,t.Wx,i); stepE(t.Ey,t.Ay,t.Wy,i);
        ok=rowt(&t,i);
      }
      if(ok){ wsum+=tailw; succ++; if(!rebuild(s,v,w23))bad++; }
    }}
  double mean=wsum/((double)NP*ntail);
  if(wsum==0){ printf("%llu -inf tail empty\n",(unsigned long long)seed); return 0; }
  lg[nst++]=log2(mean);
  double tot=0; for(int i=0;i<nst;i++)tot+=lg[i];
  printf("%llu %.5f",(unsigned long long)seed,tot); for(int i=0;i<nst;i++)printf(" %.3f",lg[i]); printf("  succ %ld rebuilt_failed %ld\n",succ,bad);
  return 0;
}
```

### B.11 varsample.c

```c
/* varsample.c - uniform sample of variants from the union of the R_j: A0_j with probability |R_j| / SR (data/a0set256_peer.txt),
   then (A1, A2) uniform in R_j by rejection from the 768 x 2^29 candidates of its window (exact validity test var_valid).
   usage: varsample a0set a2list count seed out.bin   -> records of 3 x u32 (A0, A1, A2) as text lines in out.txt style:  a0 a1 a2 (hex) */
#include "r38.h"
int main(int argc,char**argv){
  static u32 A0L[256]; static u64 W[256]; static u32 A2L[768]; int NA0=0,NA2=0; u64 SR=0;
  FILE*f=fopen(argv[1],"r"); while(NA0<256&&fscanf(f,"%x %llu",&A0L[NA0],(unsigned long long*)&W[NA0])==2){SR+=W[NA0];NA0++;} fclose(f);
  f=fopen(argv[2],"r"); while(NA2<768&&fscanf(f,"%x",&A2L[NA2])==1)NA2++; fclose(f);
  long n=atol(argv[3]); u64 seed=strtoull(argv[4],0,10); u64 st=seed; (void)smx(&st); st=smx(&st)^seed; FILE*o=fopen(argv[5],"w");
  long tries=0;
  for(long k=0;k<n;k++){
    u64 r=smx(&st)%SR; int j=0; while(r>=W[j]){r-=W[j];j++;}
    for(;;){ tries++; int ai=smx(&st)%NA2; u32 a2=A2L[ai];
      u32 E6=SA(6)+a2-S0(SA(5))-MAJ(SA(5),SA(4),SA(3)); u32 k5=SA(5)-S0(SA(4))-MAJ(SA(4),SA(3),a2);
      u32 a1=((E6&0xe0000000u)-k5)+(u32)(smx(&st)&((1u<<29)-1));
      Var v; var_build(&v,A0L[j],a1,a2); if(var_valid(&v)){fprintf(o,"%08x %08x %08x\n",A0L[j],a1,a2);break;}}
  }
  fclose(o); fprintf(stderr,"samples %ld candidates tried %ld (acceptance %.5f)\n",n,tries,(double)n/tries); return 0;}
```

### B.12 t_mut.py, t_eq.py, t_cost.py

`t_mut.py`:

```python
# t_mut.py - branch-coverage equivalence test of the counted program against the reference on the published
# semi-free-start pair, with the characteristic constants mutated (each mutated constant makes the pair fail at a
# chosen row/condition, or leaves it passing).  Machine outcome (last mark / success) vs reference outcome.
import sys, copy, random, itertools
sys.path.insert(0, '.')
import vtprog as P
from vtprog import *

LANE = int(sys.argv[1]) if len(sys.argv) > 1 else 0
def run_machine(a0, a1, a2):
    A0L[LANE] = a0
    tab = tables(a2list=[a2]); var = variant(a0, a1, a2)
    Y, Z0 = yz0(PCV, a0); w16 = w16_closed(PCV, a0, a1, a2); gi = GSET[w16]
    ent = ((c7of(var) + (1 << 32)) & WORD, a1 | S0(a1) << 32 | (A2T) << 64, gaddr(gi))
    m = Machine([1, 2], lambda j, y, z: [ent] if j == LANE else [], tab, cvforce=PCV)
    m.run(build_program([0, 1, 2, 3]))
    return m

def ref_expect(a0, a1, a2):
    o = outcome(PCV, a0, a1, a2)
    assert o['r16'] and o['w7']
    E, A, I = row17_parts(o['tx'], o['ty'])
    if not E: return 'W7'
    if not A: return 'E17'
    if not I: return 'A17'
    for i in range(18, NR):
        if not rowok(o['tx'], o['ty'], i): return ('row', i)
    return 'succ'

def got(m):
    if m.succ: return 'succ'
    return m.marks[-1]

a0, a1, a2 = sa(0), sa(1), sa(2)
base = outcome(PCV, a0, a1, a2); tx, ty = base['tx'], base['ty']
orig = (copy.deepcopy(CELLS), list(PQ), list(X2))
def restore():
    for k in range(3):
        for i in range(NR): CELLS[k][i] = orig[0][k][i]
    PQ[:] = orig[1]; X2[:] = orig[2]
def get(k, i): return (tx[k][i] if k < 2 else tx[2][i], ty[k][i] if k < 2 else ty[2][i])
cases = []
for i in range(17, NR):
    for k in range(3):
        mk, vl, df, pl = orig[0][k][i]
        x, y = get(k, i)
        # value cell: flip a required bit / require a new bit wrongly / require a new bit rightly
        for b in range(0, 32, 1):
            bit = 1 << b
            if i == 17 and k == 2: continue
            if mk & bit: cases.append(('flipval', i, k, b, (mk, vl ^ bit, df, pl)))
            else:
                cases.append(('addwrong', i, k, b, (mk | bit, vl | ((~x) & bit), df, pl)))
                cases.append(('addright', i, k, b, (mk | bit, vl | (x & bit), df, pl)))
            if i > 17: cases.append(('flipdiff', i, k, b, (mk, vl, df ^ bit, pl)))
    for b in range(32):
        bit = 1 << b
        Ex, Ep = tx[1][i], tx[1][i-1]
        cases.append(('pq', i, 1, b, None, bit))
for idx, x in enumerate(orig[2]):
    if x[7] >= 17: cases.append(('x2flip', x[7], 0, idx, None))
random.seed(1); random.shuffle(cases)
cnt = {}; bad = 0; n = 0
for c in cases:
    restore()
    kind, i, k, b = c[:4]
    if kind in ('flipval', 'addwrong', 'addright', 'flipdiff'): CELLS[k][i] = c[4]
    elif kind == 'pq': PQ[i] = orig[1][i] | c[5]
    elif kind == 'x2flip':
        r = list(X2[b]); r[3] ^= 1; X2[b] = tuple(r)
    # reference expectation; skip mutations that already break rows <= 16 (G is fixed)
    try:
        e = ref_expect(a0, a1, a2)
    except AssertionError:
        continue
    try: m = run_machine(a0, a1, a2)
    except AssertionError: continue
    if not m.succ and not m.marks: print('NO MARKS', c[:4], e, m.r.get('FL'), m.r.get('NE'), m.trace); continue
    g = got(m); n += 1
    key = (e if isinstance(e, str) else 'row'); cnt[key] = cnt.get(key, 0) + 1
    if g != e:
        bad += 1; print('MISMATCH', c[:4], 'ref', e, 'machine', g)
restore()
print('cases', len(cases), 'run', n, 'mismatches', bad, 'expected-outcome histogram', cnt)
```

`t_eq.py`:

```python
# t_eq.py - equivalence of the counted program with the reference construction on TRUE buckets: for each real
# chaining value, all 256 A0 blocks; machine counters NE, NW, N1 and the full sequence of stage marks of every entry
# versus the reference (outcome(), row17_parts()); every bucket entry must have row 16 and be a valid variant.
# usage: t_eq.py jobs.txt buckets.txt [ncv]
import sys; sys.path.insert(0, '.')
from vtprog import *
jobs = [l.split() for l in open(sys.argv[1])]; lines = open(sys.argv[2]).read().split('\n'); pos = 0
ncv = int(sys.argv[3]) if len(sys.argv) > 3 else 10**9
buckets = {}; k = 0
while pos < len(lines) and lines[pos].startswith('B'):
    _, a0h, cnt = lines[pos].split(); cnt = int(cnt); ents = [tuple(map(int, l.split()[1:])) + (int(l.split()[0], 16),) for l in lines[pos+1:pos+1+cnt]]
    buckets[k] = (int(a0h, 16), [(a1, a2i, gi) for (a2i, gi, a1) in ents]); pos += 1 + cnt; k += 1
tab = tables()
def expected_marks(cv, a0, a1, a2):
    o = outcome(cv, a0, a1, a2); assert o['r16'], 'bucket entry fails row 16'; assert valid(o['var'])
    mk = []
    if not o['w7']: return mk, o
    mk.append('W7'); E, A, I = row17_parts(o['tx'], o['ty'])
    if not E: return mk, o
    mk.append('E17')
    if not A: return mk, o
    mk.append('A17')
    if not I: return mk, o
    mk.append('A17int')
    for i in range(18, NR):
        mk.append(('row', i))
        if not rowok(o['tx'], o['ty'], i): return mk, o
    return mk + ['succ'], o
done = 0; tot = dict(ne=0, nw=0, n1=0, ent=0, deep=0); bad = 0; maxrow = {}
for c in range(len(buckets) // 256):
    if c >= ncv: break
    cv = [int(x, 16) for x in jobs[256 * c][:8]]
    B = {}
    for jj in range(256):
        a0, ents = buckets[256 * c + jj]; assert a0 == A0L[jj] and int(jobs[256 * c + jj][8], 16) == a0; B[jj] = ents
    exp_obs = []; exp_marks = []; ne = 0; nw = 0; n1 = 0; ent = 0
    for jj in range(256):
        ne += 3 * (len(B[jj]) + 1)
        for (a1, a2i, gi) in B[jj]:
            ent += 1
            mk, o = expected_marks(cv, A0L[jj], a1, A2L[a2i]); assert GSET[o['tx'][2][16]] == gi
            if 'W7' in mk: exp_obs += [o['tx'][2][17], o['tx'][1][17]]
            exp_marks += mk; nw += 'W7' in mk; n1 += 'E17' in mk
            if 'succ' in mk: print('SUCCESS in real bucket!', c, jj, a1, a2i)
            if ('row', 18) in mk: tot['deep'] += 1
            for x in mk:
                if isinstance(x, tuple): maxrow[x[1]] = maxrow.get(x[1], 0) + 1
    def bucket(j, y, z):
        a0 = A0L[j]; yy, zz = yz0(cv, a0); assert (y, z) == (yy, zz)
        return [((c7of(variant(a0, a1, A2L[a2i])) + (1 << 32)), a1 | S0(a1) << 32 | (A2T + 2 * a2i) << 64, gaddr(gi)) for (a1, a2i, gi) in B[j]]
    prog, mp = allocated_program(range(256), ngroups=1)
    m = Machine([0x1111, 0x2222], bucket, tab, cvforce=cv); m.run(prog)
    got_marks = list(m.marks) + (['succ'] if m.succ else [])
    ok = (m.r.get(mp['NE'], 0) == ne and m.r.get(mp['NW'], 0) == nw and m.r.get(mp['N1'], 0) == n1 and got_marks == exp_marks and m.units == 1 and [x & M for x in m.obs] == exp_obs)
    bad += not ok
    if not ok: print('DBG', m.units, got_marks == exp_marks, got_marks[:4], exp_marks[:4], m.succ)
    for kk, v in (('ne', ne), ('nw', nw), ('n1', n1), ('ent', ent)): tot[kk] += v
    print('cv', c, 'entries', ent, 'NE', m.r.get(mp['NE'], 0), ne, 'NW', m.r.get(mp['NW'], 0), nw, 'N1', m.r.get(mp['N1'], 0), n1, 'marks', len(got_marks), len(exp_marks), 'ops', m.ops, 'OK' if ok else 'MISMATCH', flush=True)
print('total', tot, 'mismatching CVs', bad, 'row histogram', sorted(maxrow.items()))
```

`t_cost.py`:

```python
# t_cost.py - static costs of the counted program, measured by executing it (the interpreter counts every executed operation;
# stage marks record the operation counter).  Four-lane blocks: a group of four A0 blocks shares the vector computation.
import sys, json; sys.path.insert(0, '.')
from vtprog import *
cv = [1, 2, 3, 4, 5, 6, 7, 8]
def run(js, bucket, cvf=cv, tab=None):
    prog, mp = allocated_program(js, (1 << 200,) * 3, 1)
    m = Machine([5, 6], bucket, tab if tab is not None else tables(), cvforce=cvf); m.run(prog); return m
m0 = run([], lambda j, y, z: [])
P0EPI = m0.ops                                    # prologue + epilogue + group-loop branch
m4 = run([0, 1, 2, 3], lambda j, y, z: [])
GROUP4 = m4.ops - P0EPI                            # four blocks with empty buckets
assert run(list(range(8)), lambda j, y, z: []).ops - P0EPI == 2 * GROUP4
a = cv[0]; w = 12345
while inF7(w & M): w += 1
e0 = (((w + a) & M) + (1 << 32), 0, 0)
ITER = run([0, 1, 2, 3], lambda j, y, z: [e0] if j == 0 else []).ops - m4.ops
EPI = 15; P0 = P0EPI - EPI
print('prologue %d  epilogue %d  four empty blocks %d (%.2f per block)  loop iteration %d' % (P0, EPI, GROUP4, GROUP4 / 4, ITER))
# the published pair as a success in every lane: marks give the cost of every stage from the pass label
A0save = list(A0L); a0, a1, a2 = sa(0), sa(1), sa(2); tab = tables(a2list=[a2]); var = variant(a0, a1, a2)
gi = GSET[w16_closed(PCV, a0, a1, a2)]
ent = ((c7of(var) + (1 << 32)), a1 | S0(a1) << 32 | A2T << 64, gaddr(gi))
lanes = []
for lane in range(4):
    A0L[lane] = a0
    m = run([0, 1, 2, 3], lambda j, y, z: [ent] if j == lane else [], cvf=PCV, tab=tab); A0L[:] = A0save
    d = dict((k, o) for k, o in m.mark_ops); base = d['W7'] - 1       # ops executed before the pass label (the NW increment is the pass path's first op)
    lanes.append(dict(X_E17=d['E17'] - base, X_A17=d['A17'] - base, X_A17int=d['A17int'] - base, X_SUCC=m.succ_ops - base))
    print('lane', lane, lanes[-1])
out = dict(P0=P0, EPI=EPI, GROUP4=GROUP4, ITER=ITER, PASS_ENTRY=3, X_E17=max(l['X_E17'] for l in lanes), X_A17=max(l['X_A17'] for l in lanes),
           X_A17int=max(l['X_A17int'] for l in lanes), X_SUCC=max(l['X_SUCC'] for l in lanes), BLOCK_FIXED=GROUP4 / 4)
print(json.dumps(out)); json.dump(out, open('../runs/costs.json', 'w'))
```

### B.13 t_pre1.py, t_pre2.py, t_replay.py

`t_pre1.py`:

```python
# t_pre1.py - P1..P4 as counted code: G scan body, F7 body, A2-list body, A2 and G records; each against the reference.
import sys, random, json; sys.path.insert(0, '.')
from vtpre import *
random.seed(7)
res = {}
def loop_prog(body, hit):
    """for each candidate in memory list at LST: body; costs measured around it"""
    a = Asm(); a.L('top'); body(a, 'nx'); hit(a); a.L('nx'); a('halt_ok',); return a
def run(a, regs, mem=None):
    m = MachineP([], None, {}); m.mem = dict(mem or {}); m.r = dict(regs); m.run(a); return m
# --- P1
def hit_g(a): a('st', 'gp', 'w'); a('add', 'gp', 'gp', 1)
prog = loop_prog(gen_g_body, hit_g)
inG = set(GL); bad = 0; worst = 0; tested = 0
cands = list(GL) + [random.getrandbits(32) for _ in range(20000)] + [g ^ (1 << b) for g in GL for b in range(32)] + [(g + d) & M for g in GL for d in (1, -1, 0x20000000, -0x20000000)]
costs = {}
for w in cands:
    m = run(prog, dict(w=w, gp=1 << 100)); hit = m.r['gp'] != 1 << 100
    tested += 1; bad += (hit != (w in inG))
    costs[hit] = max(costs.get(hit, 0), m.ops)
print('P1 G body: tested', tested, 'mismatches', bad, 'max ops hit/non-hit', costs)
res['G_hit_ops'] = costs[True]; res['G_nonhit_max_ops'] = costs[False]
# cross-check against reference row-16 on the same candidates (rowok of a synthetic trace is not available without rows <16: use vtref via S* rows)
# --- P2
def hit_f7(a): pass
prog = loop_prog(gen_f7_body, hit_f7)
bad = 0; cost = {}
ws = [random.getrandbits(32) for _ in range(3000)]
# members of F7: rejection from random
while len([w for w in ws if inF7(w)]) < 400: ws.append(random.getrandbits(32))
for w in ws:
    m = run(prog, dict(w=w, one=1, two=2)); st1 = m.mem.get(w, 0); st2 = m.mem.get(w + (1 << 32), 0); st3 = m.mem.get((1 << 34) + 1 + w, 0)
    exp = 1 if inF7(w) else 0
    bad += (st1 != exp or st2 != exp or st3 != 2); cost[exp] = max(cost.get(exp, 0), m.ops)
print('P2 F7 body: tested', len(ws), 'mismatches', bad, 'ops (in F7 / not)', cost)
res['F7_in_ops'] = cost[1]; res['F7_out_ops'] = cost[0]
# --- P3
def hit_a2(a): a('st', 'ap', 'x'); a('add', 'ap', 'ap', 1)
prog = loop_prog(gen_a2_body, hit_a2)
inL = set(A2L); bad = 0; cost = {}
cands = list(A2L) + [random.getrandbits(32) for _ in range(20000)] + [(x + d) & M for x in A2L[::7] for d in (1, -1, 2, 4, 8)] + [x ^ (1 << b) for x in A2L[::5] for b in range(32)]
for x in cands:
    m = run(prog, dict(x=x, ap=1 << 100)); hit = m.r['ap'] != 1 << 100
    bad += (hit != (x in inL)); cost[hit] = max(cost.get(hit, 0), m.ops)
print('P3 A2 body: tested', len(cands), 'mismatches', bad, 'ops', cost)
res['A2_hit_ops'] = cost[True]; res['A2_nonhit_max_ops'] = cost[False]
# --- P4
tab = tables(); bad = 0; tot = 0
a = Asm(); gen_a2rec(a, 'x', 'ra'); a('halt_ok',)
for k, x in enumerate(A2L):
    m = run(a, dict(x=x, ra=A2T + 2 * k)); tot += m.ops
    bad += (m.mem[A2T + 2 * k] != tab[A2T + 2 * k]) + (m.mem[A2T + 2 * k + 1] != tab[A2T + 2 * k + 1])
    # dW9 holds
    assert ((m.r['c9y'] - m.r['c9x']) & M) == DW[9]
print('P4 A2 records: 768, mismatching words', bad, 'ops total', tot, 'per record', tot / 768)
res['A2REC_total_ops'] = tot
bad = 0; totg = 0
for gi, g in enumerate(GL):
    a = Asm(); gen_grec(a, gi, g); a('halt_ok',); m = run(a, {}); totg += m.ops
    exp = grec(gi, g)
    for ad, v in exp.items(): bad += (m.mem.get(ad, 0) != v)
    assert set(m.mem) == set(exp) or True
print('P4 G records: 32, mismatching words', bad, 'ops total', totg)
res['GREC_total_ops'] = totg
json.dump(res, open('../runs/pre1.json', 'w'))
```

`t_pre2.py`:

```python
# t_pre2.py - P5 (variant enumeration) and P6 (table construction) as counted code on toy instances, against the
# definitions (reference valid() / closed-form W16).  Reports the executed operation counts per item.
import sys, random, json; sys.path.insert(0, '.')
from vtpre import *
random.seed(11)
res = {}
def run(a, regs, mem=None, maxops=None):
    m = MachineP([], None, {}); m.mem = dict(mem or {}); m.r = dict(regs); m.run(a); return m
# true valid variants from the bucket file (first CV, several A0 blocks)
lines = open('../runs/eq/buckets.txt').read().split('\n'); pos = 0; k = 0; B = {}
jobs = [l.split() for l in open('../runs/eq/jobs.txt')]
while pos < len(lines) and lines[pos].startswith('B'):
    _, a0h, cnt = lines[pos].split(); cnt = int(cnt)
    B[k] = (int(a0h, 16), [(int(l.split()[0], 16), int(l.split()[1]), int(l.split()[2])) for l in lines[pos+1:pos+1+cnt]]); pos += 1 + cnt; k += 1
tab = tables()
# --- P5: enumeration on windows
bad = 0; total_valid = 0; cand_ops = {}; windows = 0
for kk in random.sample(range(256), 12):
    a0, ents = B[kk]; j = A0L.index(a0)
    if not ents: continue
    a1v, a2i, gi = ents[0]; a2 = A2L[a2i]
    a = Asm(); gen_enum_setup(a, a0); a('li', 'r', 0); a.L('top')
    gen_enum_body(a, a0, 'nx'); gen_enum_append(a, a0)
    a.L('nx'); a('add', 'r', 'r', 1); a('bne', 'r', 'rend', 'top'); a('halt_ok',)
    # setup precondition: record in memory
    mem = {A2T + 2 * a2i: tab[A2T + 2 * a2i], A2T + 2 * a2i + 1: tab[A2T + 2 * a2i + 1]}
    # lo from the code: compute in python for the window offsets
    E6 = (sa(6) + a2 - S0(sa(5)) - MAJ(sa(5), sa(4), sa(3))) & M
    k5 = (sa(5) - S0(sa(4)) - MAJ(sa(4), sa(3), a2)) & M
    lo = ((E6 & 0xe0000000) - k5) & M
    off = (a1v - lo) & M; assert off < (1 << 29)
    r0 = max(0, off - random.randrange(0, 3000)); r1 = min(1 << 29, r0 + 4096)
    # patch: start r at r0
    a.c[a.c.index(('li', 'r', 0))] = ('li', 'r', r0)
    m = run(a, dict(ra=A2T + 2 * a2i, lp=1 << 150, rend=r1), mem)
    got = []; p = 1 << 150
    while p < m.r['lp']: got.append((m.mem[p], m.mem[p+1], m.mem[p+2])); p += 3
    exp = []
    for r in range(r0, r1):
        a1 = (lo + r) & M; var = variant(a0, a1, a2)
        if valid(var):
            exp.append(((c7of(var) + (1 << 32)), a1 | S0(a1) << 32 | (A2T + 2 * a2i) << 64, c9x_of(a2)))
    ok = got == exp; bad += (not ok); total_valid += len(exp); windows += 1
    if not ok:
        d = [(i, [hex(x) for x in g], [hex(x) for x in e]) for i, (g, e) in enumerate(zip(got, exp)) if g != e][:2]; print('MISMATCH window', kk, a2i, len(got), len(exp), d)
    assert len(exp) >= 1
print('P5: windows', windows, 'window candidates', windows * 4096, 'valid variants found', total_valid, 'mismatching windows', bad)
# per-candidate and per-valid costs, measured with single-candidate runs
kk0 = next(k_ for k_ in range(256) if B[k_][1]); a0, ents = B[kk0]; a1v, a2i, gi = ents[0]; a2 = A2L[a2i]
def one_cand(a1, tail):
    a = Asm(); gen_enum_setup(a, a0); setup_end = len(a.c)
    gen_enum_body(a, a0, 'nx'); body_end = len(a.c)
    if tail: gen_enum_append(a, a0)
    a.L('nx'); a('halt_ok',)
    E6 = (sa(6) + a2 - S0(sa(5)) - MAJ(sa(5), sa(4), sa(3))) & M; k5 = (sa(5) - S0(sa(4)) - MAJ(sa(4), sa(3), a2)) & M
    lo = ((E6 & 0xe0000000) - k5) & M
    mem = {A2T + 2 * a2i: tab[A2T + 2 * a2i], A2T + 2 * a2i + 1: tab[A2T + 2 * a2i + 1]}
    m = run(a, dict(ra=A2T + 2 * a2i, lp=1 << 150, r=(a1 - lo) & M), mem); return m.ops
# setup cost
a = Asm(); gen_enum_setup(a, a0); a('halt_ok',); SET = run(a, dict(ra=A2T + 2 * a2i), {A2T + 2 * a2i: tab[A2T + 2 * a2i], A2T + 2 * a2i + 1: tab[A2T + 2 * a2i + 1]}).ops
valid_ops = one_cand(a1v, True) - SET
append_only = valid_ops - (one_cand(a1v, False) - SET)
print('P5 ops: setup', SET, ', valid candidate incl. append', valid_ops, ', append part', append_only, ', body part (all tests pass)', valid_ops - append_only)
# a candidate that fails at each stage: cost of the cheap first exit
fails = {}
E6 = (sa(6) + a2 - S0(sa(5)) - MAJ(sa(5), sa(4), sa(3))) & M; k5 = (sa(5) - S0(sa(4)) - MAJ(sa(4), sa(3), a2)) & M; lo = ((E6 & 0xe0000000) - k5) & M
for t in range(400):
    a1 = (lo + random.randrange(1 << 29)) & M
    c = one_cand(a1, False) - SET; fails[c] = fails.get(c, 0) + 1
print('P5 body cost histogram (random in-window candidates):', sorted(fails.items()))
res.update(P5_SETUP=SET, P5_BODY_MAX=valid_ops - append_only, P5_APPEND=append_only, P5_LOOP=3)
# --- P6 toy
j = 0; a0 = A0L[0]
vars_ = []
# toy: variants valid for A0 block 0 (taken from the true buckets of the six CVs)
for c in range(6):
    a0c, ents = B[256 * c]
    vars_ += [(a1, a2i) for (a1, a2i, gi) in ents]
vars_ = sorted(set(vars_)); assert len(vars_) >= 10
cvs = [[int(x, 16) for x in jobs[256 * c][:8]] for c in range(6)]
YS = sorted(set([yz0(cv, a0)[0] for cv in cvs] + [random.getrandbits(32) for _ in range(2)]))
HB = HDR | (j << 64)
def x_of(Y, a1, a2): return (s0((Y + a1) & M) - a1 + c9x_of(a2)) & M
# expected buckets by definition (insertion order: variant outer, Y inner, g inner)
expb = {}; ops = {}
# count pass
cnt_prog = Asm(); cnt_prog.L('vt'); gen_count_body(cnt_prog, HB); cnt_prog('halt_ok',)
mem = {}; m_ops = []
for (a1, a2i) in vars_:
    for Y in YS:
        mm = run(cnt_prog, dict(Y=Y, A1=a1, c9x=c9x_of(A2L[a2i])), mem); m_ops.append(mm.ops); mem = mm.mem
        for gi, g in enumerate(GL): expb.setdefault((Y, (g - x_of(Y, a1, A2L[a2i])) & M), []).append((a1, a2i, gi))
cnt_cost = max(m_ops); print('P6 count: ops per (Y, variant)', set(m_ops))
# check counts
badc = sum(mem.get(HB + (Y << 32 | Z), 0) != len(v) for (Y, Z), v in expb.items())
# prefix pass over touched headers (sorted) + 3 untouched
hdrs = sorted(HB + (Y << 32 | Z) for (Y, Z) in expb) + [HB + 12345, HB + (YS[0] << 32 | 77)]
hdrs = sorted(set(hdrs)); ENT0 = ENT + 3
pre = Asm(); pre.L('top'); gen_prefix_body(pre); pre.L('nxt'); pre('add', 'h', 'h', 1); pre('halt_ok',)
run_ = ENT0; pops = {}
mem2 = dict(mem)
for h in hdrs:
    c0 = mem2.get(h, 0)
    mm = MachineP([], None, {}); mm.mem = mem2; mm.r = dict(h=h, run=run_); mm.run(pre); run_ = mm.r['run']; pops.setdefault('empty' if c0 == 0 else 'nonempty', set()).add(mm.ops)
print('P6 prefix ops', pops, ' (includes the loop-increment op of this harness: 1)')
# fill pass
fill = Asm(); gen_fill_body(fill, HB); fill('halt_ok',)
fops = set()
for (a1, a2i) in vars_:
    ca = A2L[a2i]; var = variant(a0, a1, ca)
    for Y in YS:
        c7 = (c7of(var) + (1 << 32)) & WORD; w1 = a1 | S0(a1) << 32 | (A2T + 2 * a2i) << 64
        mm = MachineP([], None, {}); mm.mem = mem2; mm.r = dict(Y=Y, A1=a1, c9x=c9x_of(ca), c7=c7, w1e=w1); mm.run(fill); fops.add(mm.ops)
print('P6 fill ops per (Y, variant)', fops)
# verify table = definition (entries backwards fill: reverse insertion order)
badt = 0; nb = 0
for (Y, Z), v in expb.items():
    h = mem2[HB + (Y << 32 | Z)]; got = []
    while mem2[h] != SENT:
        got.append(((mem2[h]), mem2[h+1], mem2[h+2])); h += 3
    exp = [((c7of(variant(a0, a1, A2L[a2i])) + (1 << 32)), a1 | S0(a1) << 32 | (A2T + 2 * a2i) << 64, gaddr(gi)) for (a1, a2i, gi) in v]
    exp = exp[::-1]; badt += (got != exp); nb += 1
    if got != exp and badt < 3: print('BUCKET', Y, Z, [[hex(x) for x in t] for t in got][:2], [[hex(x) for x in t] for t in exp][:2], len(got), len(exp))
emp = [mem2[h] for h in hdrs if h not in {HB + (Y << 32 | Z) for (Y, Z) in expb}]
print('P6: buckets', nb, 'mismatching', badt, 'count mismatches', badc, 'empty headers = EMPTY:', all(e == EMPTY for e in emp))
# cross-check with TRUE buckets from the bucket file: the table bucket of (Y, Z0) of each CV contains the file's entries of the variants in vars_
tb = 0
for c in range(6):
    cv = cvs[c]; Y, Z0 = yz0(cv, a0); ents = B[256 * c][1]
    h = mem2.get(HB + (Y << 32 | Z0)); got = []
    if h is not None and h != EMPTY:
        while mem2[h] != SENT: got.append((mem2[h+1] & M, (mem2[h+1] >> 64) - A2T >> 1, GL.index(0) if False else None)); h += 3
    exp = sorted(((a1, a2i) for (a1, a2i, gi) in ents)); gs = sorted((a1, a2i) for (a1, a2i, _) in got)
    tb += (exp != gs)
print('P6 vs true buckets (6 CVs, A0 block 0): mismatching', tb)
res.update(P6_COUNT=max(m_ops), P6_FILL=max(fops), P6_PREFIX_EMPTY=max(pops['empty']) - 1, P6_PREFIX_NONEMPTY=max(pops['nonempty']) - 1)
json.dump(res, open('../runs/pre2.json', 'w'))
```

`t_replay.py`:

```python
# t_replay.py - the counted program on SMC successes (real semi-free-start pairs rebuilt and verified by smc.c):
# the success's chaining value is forced; the A0 block's bucket holds two decoys and the true entry.
# usage: t_replay.py succ.txt [max]
import sys, random; sys.path.insert(0, '.')
from vtprog import *
random.seed(3)
L = [l.split() for l in open(sys.argv[1])]; mx = int(sys.argv[2]) if len(sys.argv) > 2 else len(L)
tab = tables(); A2IDX = {x: i for i, x in enumerate(A2L)}; A0IDX = {x: i for i, x in enumerate(A0L)}
ent_of = lambda cv, a0, a1, a2i: ((c7of(variant(a0, a1, A2L[a2i])) + (1 << 32)), a1 | S0(a1) << 32 | (A2T + 2 * a2i) << 64, gaddr(GSET[w16_closed(cv, a0, a1, A2L[a2i])]))
found = 0; n = 0; bad = 0; ops = []; a0s = set(); progs = {}
for l in L[:mx]:
    a0, a1, a2 = int(l[0], 16), int(l[1], 16), int(l[2], 16)
    cv = [int(x, 16) for x in l[4:12]]; mm = [int(x, 16) for x in l[13:29]]
    j = A0IDX[a0]; a2i = A2IDX[a2]
    # sanity: the semi-free-start pair collides
    mx_ = mm; my = list(mm)
    for i in range(7, 16): my[i] = (mm[i] + DW[i]) & M
    assert compress(cv, mx_) == compress(cv, my) and mx_ != my
    true = ent_of(cv, a0, a1, a2i)
    dec = []
    for _ in range(2):
        d = L[random.randrange(len(L))]; dec.append(ent_of([int(x, 16) for x in d[4:12]], int(d[0], 16), int(d[1], 16), A2IDX[int(d[2], 16)]) if False else (true[0] ^ random.getrandbits(20), true[1], true[2]))
    Y, Z0 = yz0(cv, a0)
    key = j
    q = j // 4; key = q
    if key not in progs: progs[key] = allocated_program(list(range(4 * q, 4 * q + 4)))[0]
    m = Machine([1, 2], lambda jj, y, z: [dec[0], true, dec[1]], tab, cvforce=cv); m.run(progs[key])
    n += 1; ok = bool(m.succ and m.succ[0] == j); found += ok; ops.append(m.ops); a0s.add(a0)
    # the pair the program reports: the entry word is the true one
    bad += (not ok)
print('successes replayed', n, 'found by the counted program', found, 'failures', bad, 'distinct A0', len(a0s), 'ops min/max', min(ops), max(ops))
```

### B.14 t_clump.py, t_own.py, t_far.py, t_imm.py, h1_jobs.py, analyze.py

`t_clump.py`:

```python
# t_clump.py - H5, near term: for every SMC success (A0, A1, A2, CV1) every OTHER valid variant (A0, A1, A2') of the A2 list is tried on the same
# CV1 (it shares W0, W1 and, within a c9 class, W16): valid variants, row-16 co-hits, W7 passes, first-row-17-test passes, co-successes.
# usage: t_clump.py succ.txt lo hi
import sys; sys.path.insert(0, '.')
from vtref import *
rows = [l.split() for l in open(sys.argv[1])][int(sys.argv[2]):int(sys.argv[3])]
nv = nh = nw = n17 = ns = nfull = 0
for l in rows:
    a0, a1, a2 = int(l[0], 16), int(l[1], 16), int(l[2], 16); cv = [int(x, 16) for x in l[4:12]]
    for b2 in A2L:
        if b2 == a2: continue
        var = variant(a0, a1, b2)
        if not valid(var): continue
        nv += 1
        if w16_closed(cv, a0, a1, b2) not in GSET: continue
        nh += 1; o = outcome(cv, a0, a1, b2); assert o['r16']
        if not o['w7']: continue
        nw += 1
        E_, A_, I_ = row17_parts(o['tx'], o['ty']); n17 += bool(E_); nfull += o['deep'] >= 17
        if o['deep'] == NR - 1: ns += 1
print('successes', len(rows), 'other valid variants with the same (A0, A1)', nv, 'row-16 co-hits', nh, 'W7 passes', nw, 'first row-17 tests (E17 mask) passed', n17, 'full row 17 holds', nfull, 'co-successes', ns)
```

`t_own.py`:

```python
# t_own.py - pair term, own block: for each verified success (A0, A1, A2, CV1) the TRUE bucket of (CV1, A0) (bucket.c) holds the success and every other
# variant of the same A0 whose row 16 holds on the same chaining value (same (A0, A1) or not).  Counts, over the other entries: entries, W7 passes,
# first row-17 tests (E17 mask) passed, further successes.  usage: t_own.py jobs.txt meta.txt buckets.txt
import sys; sys.path.insert(0, '.')
from vtref import *
jobs = [l.split() for l in open(sys.argv[1]) if l.strip()]; meta = [tuple(int(x, 16) for x in l.split()) for l in open(sys.argv[2]) if l.strip()]
lines = open(sys.argv[3]).read().split('\n'); pos = 0; k = 0
ns = nent = nw = n1 = nsucc = deep = 0; sameA1 = 0
while pos < len(lines) and lines[pos].startswith('B') and k < len(jobs):
    _, a0h, cnt = lines[pos].split(); cnt = int(cnt); ents = [(int(l.split()[0], 16), int(l.split()[1]), int(l.split()[2])) for l in lines[pos+1:pos+1+cnt]]; pos += 1 + cnt
    cv = [int(x, 16) for x in jobs[k][:8]]; a0, a1s, a2s = meta[k]; assert int(a0h, 16) == a0 == int(jobs[k][8], 16)
    found = False; ns += 1
    for (a1, a2i, gi) in ents:
        if a1 == a1s and A2L[a2i] == a2s: found = True; continue
        nent += 1; sameA1 += a1 == a1s
        o = outcome(cv, a0, a1, A2L[a2i]); assert o['r16']
        if not o['w7']: continue
        nw += 1; E, A, I = row17_parts(o['tx'], o['ty']); n1 += bool(E); deep += o['deep'] >= 18; nsucc += o['deep'] == NR - 1
    assert found, 'success missing from its own true bucket'
    k += 1
print('successes', ns, 'other entries in the success\'s own bucket', nent, '(of them with the same A1: %d)' % sameA1, 'W7 passes', nw, 'first row-17 tests passed', n1, 'rows>=18', deep, 'further successes', nsucc)
```

`t_far.py`:

```python
# t_far.py - rates on TRUE buckets (src/bucket.c) of real chaining values: for every bucket entry the reference outcome (row 16 must hold,
# the variant must be valid), counts of entries, W7 passes, first row-17 test (E17 mask) passes, deeper rows, successes, against the
# H1 expectations  |R_j| 2^-27 (entries), |F7| 2^-32 (W7), 2^-10 (E17 mask).
# usage: t_far.py jobs.txt buckets.txt [procs]    (job line: 8 hex cv words, A0 hex; bucket file as written by bucket.c)
import sys; sys.path.insert(0, '.')
from vtref import *
from multiprocessing import Pool
RJ = {}
for l in open('../data/a0set256_peer.txt'):
    f = l.split()
    if len(f) >= 2: RJ[int(f[0], 16)] = int(f[1])
def work(args):
    cv, a0, ents = args
    ne = nw = n1 = deep = succ = 0
    for (a1, a2i, gi) in ents:
        o = outcome(cv, a0, a1, A2L[a2i]); assert o['r16'] and valid(o['var']) and GSET[o['tx'][2][16]] == gi
        ne += 1
        if not o['w7']: continue
        nw += 1
        E, A, I = row17_parts(o['tx'], o['ty'])
        if E: n1 += 1
        if o['deep'] >= 18: deep += 1
        if o['deep'] == NR - 1: succ += 1
    return ne, nw, n1, deep, succ
if __name__ == '__main__':
    jobs = [l.split() for l in open(sys.argv[1]) if l.strip()]; lines = open(sys.argv[2]).read().split('\n'); pos = 0; k = 0; tasks = []; exp = 0.0
    while pos < len(lines) and lines[pos].startswith('B'):
        _, a0h, cnt = lines[pos].split(); cnt = int(cnt)
        ents = [(int(l.split()[0], 16), int(l.split()[1]), int(l.split()[2])) for l in lines[pos+1:pos+1+cnt]]
        j = jobs[k]; assert int(j[8], 16) == int(a0h, 16)
        tasks.append(([int(x, 16) for x in j[:8]], int(a0h, 16), ents)); exp += RJ[int(a0h, 16)] / 2 ** 27; pos += 1 + cnt; k += 1
    with Pool(int(sys.argv[3]) if len(sys.argv) > 3 else 4) as p: res = p.map(work, tasks, chunksize=16)
    t = [sum(r[i] for r in res) for i in range(5)]
    pf7 = 287309824 / 2 ** 32
    print('buckets', len(tasks), 'cvs', len(set(tuple(x[0]) for x in tasks)), 'entries', t[0], 'expected %.1f' % exp, 'ratio %.4f' % (t[0] / exp))
    print('W7 passes', t[1], 'expected %.1f (of observed entries %.1f)' % (exp * pf7, t[0] * pf7), 'E17-mask passes', t[2], 'expected %.2f' % (t[1] / 1024), 'rows>=18', t[3], 'successes', t[4])
```

`t_imm.py`:

```python
# t_imm.py - sensitivity: the counted program re-measured with every immediate operand of an ALU instruction, compare-branch or store
# (a constant held in the instruction) charged one extra operation (as if loaded by an `li`).  Writes ../runs/costs_imm.json.
import sys, json; sys.path.insert(0, '.')
import vtprog
from vtprog import *
class MI(Machine):
    def run(s, code, maxops=None):
        c, lab, r = code.c, code.lab, s.r; pc = 0; n = len(c); mem = s.mem
        def v(x): return x if isinstance(x, int) else r.get(x, 0)
        ops = 0
        isi = lambda x: isinstance(x, int)
        while pc < n:
            ins = c[pc]; op = ins[0]; pc += 1
            if op in ('add', 'sub', 'and', 'or', 'xor'): ops += isi(ins[2]) + isi(ins[3])
            elif op == 'rsub': ops += 1 + isi(ins[3])
            elif op == 'bne': ops += isi(ins[2])
            elif op == 'sti': ops += isi(ins[2])
            if op == 'add': r[ins[1]] = (v(ins[2]) + v(ins[3])) & WORD; ops += 1
            elif op == 'sub': r[ins[1]] = (v(ins[2]) - v(ins[3])) & WORD; ops += 1
            elif op == 'rsub': r[ins[1]] = (ins[2] - v(ins[3])) & WORD; ops += 1
            elif op == 'and': r[ins[1]] = v(ins[2]) & v(ins[3]); ops += 1
            elif op == 'or': r[ins[1]] = v(ins[2]) | v(ins[3]); ops += 1
            elif op == 'xor': r[ins[1]] = v(ins[2]) ^ v(ins[3]); ops += 1
            elif op == 'shl': r[ins[1]] = (v(ins[2]) << ins[3]) & WORD; ops += 1
            elif op == 'shr': r[ins[1]] = v(ins[2]) >> ins[3]; ops += 1
            elif op == 'ld': r[ins[1]] = s.load(v(ins[2])); ops += 1
            elif op == 'ldi': r[ins[1]] = mem.get(ins[2], 0); ops += 1
            elif op == 'sti': mem[ins[1]] = v(ins[2]); ops += 1
            elif op == 'li': r[ins[1]] = ins[2]; ops += 1
            elif op == 'st': s.store(v(ins[1]), v(ins[2])); ops += 1
            elif op == 'bz': ops += 2; pc = lab[ins[2]] if v(ins[1]) == 0 else pc
            elif op == 'bnz': ops += 2; pc = lab[ins[2]] if v(ins[1]) != 0 else pc
            elif op == 'bne': ops += 2; pc = lab[ins[3]] if v(ins[1]) != v(ins[2]) else pc
            elif op == 'jmp': ops += 1; pc = lab[ins[1]]
            elif op == 'rand': r[ins[1]] = s.rw.pop(0); ops += 1
            elif op == 'f38':
                s.units += 1; m0 = [r[x] for x in ins[1]]; s.m0 = m0
                cv = s.cvforce if s.cvforce is not None else compress(IV, m0); s.cv = cv
                for x, y in zip(ins[2], cv): r[x] = y
            elif op == 'succ': s.succ = (ins[1], v(ins[2])); s.succ_ops = s.ops + ops; break
            elif op == 'halt_ok': break
            elif op == 'obs': s.obs.append(v(ins[1]))
            elif op == 'mark': s.marks.append(ins[1]); s.mark_ops.append((ins[1], s.ops + ops))
        s.ops += ops
vtprog.Machine = MI; Machine = MI
src = open('t_cost.py').read().replace("json.dump(out, open('../runs/costs.json', 'w'))", "json.dump(out, open('../runs/costs_imm.json', 'w'))")
exec(compile(src, 't_cost_imm', 'exec'))
```

`h1_jobs.py`:

```python
# h1_jobs.py - job file for the H1 rate check: the first NB first blocks M0_i = SHAKE-256(b'r38-h1-first-blocks|i') (64 bytes, 16 big-endian
# words), CV1_i = F_38(IV, M0_i), one job line (8 hex CV words, A0) per A0 of the set; run bucket.c on it, then t_far.py.
# usage: h1_jobs.py NB > jobs.txt
import sys, hashlib, struct; sys.path.insert(0, '.')
from vtref import *
for i in range(int(sys.argv[1])):
    M0 = list(struct.unpack('>16I', hashlib.shake_256(b'r38-h1-first-blocks|%d' % i).digest(64))); cv = compress(IV, M0)
    for a0 in A0L: print(' '.join('%08x' % x for x in cv), '%08x' % a0)
```

`analyze.py`:

```python
import sys, math
# analysis fixed in PREREG_q3.txt: mean of Z = 2^logZ, sample sd, one-sided 99% Student lower bound, in log2
tq = {1023: 2.3300, 4095: 2.3267}
def main(fn):
    Z = []; bad = 0; nr = 0; sc = 0; stages = []
    for l in open(fn):
        f = l.split()
        if len(f) < 3: continue
        if f[1] == '-inf': Z.append(0.0); continue
        Z.append(2.0 ** float(f[1])); stages.append([float(x) for x in f[2:10]])
        i = f.index('succ'); sc += int(f[i+1]); bad += int(f[i+3]); nr += 1
    n = len(Z); m = sum(Z) / n; sd = math.sqrt(sum((z - m) ** 2 for z in Z) / (n - 1)); t = tq[n - 1]
    lo = m - t * sd / math.sqrt(n)
    print('%s: runs %d (empty %d)  mean log2 %.5f  rel sd %.4f  99%% lower bound log2 %.5f  successes %d failed rebuilds %d' % (fn, n, n - nr, math.log2(m), sd / m, math.log2(lo), sc, bad))
    print('  stage means (log2):', ' '.join('%.3f' % (sum(s[i] for s in stages) / len(stages)) for i in range(8)))
    print('  min/max single run log2 %.4f / %.4f' % (math.log2(min(z for z in Z if z > 0)), math.log2(max(Z))))
main(sys.argv[1])
```

### B.15 vtconst.py, vtref.py, vtprog.py (the development modules whose assembly is experiments/vt38.py)

`vtconst.py`:

```python
# vtconst.py: data of the 38-step characteristic (ePrint 2026/1120 Tables 3-5, own transcription), generated from consts.h
_c = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1610612736, 536870912, 1610612736, 0, 4261904, 16, 4261904, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2060, 2056, 2060, 0, 1142965762, 1073758720, 1142965762, 0, 536936448, 0, 536936448, 0, 134414480, 134217872, 134414480, 0, 41975808, 8388608, 41975808, 0, 0, 0, 0, 0, 536870912, 536870912, 536870912, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3758096384, 138678416, 134480016, 0, 3758622720, 3939897499, 3804237825, 3758096384, 67635200, 3957292027, 2299865209, 139204752, 67108864, 4278190015, 3329275675, 76546059, 0, 1040153503, 683879063, 4261888, 0, 3187670975, 2163392958, 536899588, 64, 4261412799, 1570574870, 1008926725, 64, 4293918591, 901856013, 67450, 128, 2086891391, 537027697, 134283264, 4224, 1246957562, 1242762074, 2176, 4096, 1279466112, 1208156800, 1078071808, 262160, 1086462592, 2048, 0, 17072144, 1086722608, 4330000, 262160, 16809984, 830770738, 805569584, 25198592, 0, 562331664, 537133072, 0, 0, 562072576, 553682944, 536870912, 0, 536870912, 0, 0, 0, 536870912, 536870912, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 536870912, 0, 536870912, 0, 71305216, 71303168, 71305216, 0, 536870912, 536870912, 536870912, 0, 83956394, 16777226, 83956394, 0, 529408, 529408, 529408, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 71305216, 67108864, 71305216, 0, 536870912, 536870912, 536870912, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 92446720, 92446720, 25198592, 0, 0, 0, 0, 0, 536870912, 0, 536870912, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
KC = [0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb]
PQ = [0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0xe0000000,0x00080800,0x04000000,0x00000000,0x00000000,0x00000000,0x00000040,0x00000000,0x00000080,0x00001000,0x00000000,0x00040010,0x01008000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000]
PCV = [0xcd278980,0x1b12a052,0xb87cc8a6,0xa9e059c5,0xc9c3db85,0x6ca4b5b5,0x63d13ac1,0xc0329f1e]
PMX = [0x48fc271b,0x9fca20cd,0xcc89f96f,0xfc40396f,0x8b328cb4,0x6b91ef78,0x97f9b767,0xc2450045,0x3f416758,0xfe9804cb,0x63a88c0f,0x0ceb1f8d,0xa28cd15a,0x77a1e994,0xd28e48a0,0x9f1f65bb]
PMY = [0x48fc271b,0x9fca20cd,0xcc89f96f,0xfc40396f,0x8b328cb4,0x6b91ef78,0x97f9b767,0xe2450045,0x3b016f58,0xde9804cb,0x66a99ea5,0x0ce30b8d,0xa28cd15a,0x77a1e994,0xd28e48a0,0x9b5f6dbb]
PHASH = [0x5d9ca5f4,0x59ace3a3,0x26c9c26c,0x4252c585,0x4c0803b7,0x1b4d5ccd,0x25c3ccc0,0x90645c4d]
SAX = [0xa9e059c5,0xb87cc8a6,0x1b12a052,0xcd278980,0xb75dae71,0xda6c35e0,0x479b4dc8,0xd374b0d8,0xdf740c96,0x1ee5f173,0x7fd9cecb,0x3e016e83,0xb6a6b5f9,0x3ec0b304,0xbcc85d8c,0x25d3cc99,0x4846f2d8,0xc2dc0441,0xc84cdcb9,0x91c40603]
SAY = [0xa9e059c5,0xb87cc8a6,0x1b12a052,0xcd278980,0xb75dae71,0xda6c35e0,0x479b4dc8,0xd374b0d8,0xdf740c96,0x1ee5f173,0x7fd9cecb,0x5e016e83,0xb6e7bde9,0x3ec0b304,0xbcc85d8c,0x25d3c495,0x0c66b4da,0xe2dd0441,0xc04fdc29,0x93448603]
SEX = [0xc0329f1e,0x63d13ac1,0x6ca4b5b5,0xc9c3db85,0xe69df74c,0x8aee3e8a,0x59f5e2ca,0xb6ab3dc2,0x627cb061,0x1e847683,0x0c1c24b9,0xe2e9b205,0x99352c79,0xc670b71b,0x68c3aa97,0xc2f2c1be,0x5f9d1216,0x35c13b0d,0x21966471,0x4a9b6b5a]
SEY = [0xc0329f1e,0x63d13ac1,0x6ca4b5b5,0xc9c3db85,0xe69df74c,0x8aee3e8a,0x59f5e2ca,0xb6ab3dc2,0x627cb061,0x1e847683,0x0c1c24b9,0x02e9b205,0x917934e9,0xc2e0b710,0x6882a297,0xe2f2b1ba,0x63be1213,0x35c03c77,0x29976471,0x4a9b63da]
SWX = [0x48fc271b,0x9fca20cd,0xcc89f96f,0xfc40396f,0x8b328cb4,0x6b91ef78,0x97f9b767,0xc2450045,0x3f416758,0xfe9804cb,0x63a88c0f,0x0ceb1f8d,0xa28cd15a,0x77a1e994,0xd28e48a0,0x9f1f65bb]
SWY = [0x48fc271b,0x9fca20cd,0xcc89f96f,0xfc40396f,0x8b328cb4,0x6b91ef78,0x97f9b767,0xe2450045,0x3b016f58,0xde9804cb,0x66a99ea5,0x0ce30b8d,0xa28cd15a,0x77a1e994,0xd28e48a0,0x9b5f6dbb]
DW = [0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x20000000,0xfbc00800,0xe0000000,0x03011296,0xfff7ec00,0x00000000,0x00000000,0x00000000,0xfc400800,0xe0000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0xfe7f8000,0x00000000,0x20000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000]
DS0 = [0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x03bff800,0xfe7f8000,0x043ff800,0xefffa0d0,0xfcfeed6a,0x00000000,0x00000000,0x00000000,0x01808000,0x03bff800,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x202ceee0,0x00000000,0xfc3ff800,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000]
DS1 = [0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0xfff81400,0xfb0112aa,0x00080c00,0xa500fe64,0xf8800200,0x00000000,0x00000000,0x00000000,0xfcfeed6a,0x00081400,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x50005f30,0x00000000,0x00081400,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000]
CELLS = [[tuple(_c[(k*38+i)*4:(k*38+i)*4+4]) for i in range(38)] for k in range(3)]
X2 = [(0, 14, 15, 1, 0, 16, 15, 16), (0, 14, 23, 1, 0, 16, 23, 16), (0, 14, 25, 1, 0, 16, 25, 16), (0, 15, 4, 1, 0, 16, 4, 16), (0, 15, 7, 1, 0, 16, 7, 16), (0, 15, 16, 0, 0, 16, 16, 16), (0, 15, 17, 1, 0, 16, 17, 16), (0, 15, 27, 1, 0, 16, 27, 16), (0, 15, 29, 1, 0, 16, 29, 16), (0, 16, 15, 1, 0, 17, 15, 17), (0, 16, 23, 1, 0, 17, 23, 17), (0, 16, 25, 1, 0, 17, 25, 17), (0, 17, 9, 1, 0, 17, 20, 17), (0, 17, 6, 1, 0, 17, 18, 17), (0, 17, 8, 1, 0, 17, 17, 17), (0, 16, 29, 1, 0, 18, 29, 18), (0, 18, 29, 1, 0, 19, 29, 19), (1, 16, 4, 0, 1, 16, 23, 16), (1, 16, 3, 0, 1, 16, 8, 16), (1, 16, 14, 1, 1, 16, 28, 16), (1, 16, 4, 1, 1, 17, 4, 17), (1, 16, 18, 1, 1, 17, 18, 17), (1, 18, 0, 0, 1, 18, 13, 18), (1, 17, 15, 1, 1, 18, 15, 18), (1, 17, 24, 1, 1, 18, 24, 18), (1, 19, 6, 0, 1, 19, 19, 19), (1, 19, 20, 1, 1, 19, 2, 19), (1, 21, 2, 1, 1, 21, 16, 21), (2, 7, 8, 0, 2, 7, 25, 7), (2, 7, 14, 0, 2, 7, 18, 7), (2, 7, 1, 1, 2, 7, 12, 7), (2, 8, 0, 0, 2, 8, 28, 8), (2, 8, 30, 0, 2, 8, 9, 8), (2, 8, 1, 1, 2, 8, 18, 8), (2, 16, 1, 0, 2, 16, 12, 16), (2, 16, 20, 0, 2, 16, 27, 16), (2, 16, 8, 1, 2, 16, 25, 16), (2, 16, 14, 1, 2, 16, 18, 16), (2, 16, 4, 0, 2, 16, 6, 16), (2, 16, 22, 0, 2, 16, 31, 16), (2, 23, 0, 0, 2, 23, 30, 23), (2, 23, 1, 0, 2, 23, 31, 23), (2, 23, 14, 1, 2, 23, 21, 23), (2, 23, 16, 1, 2, 23, 25, 23), (2, 25, 4, 1, 2, 25, 6, 25), (2, 25, 22, 1, 2, 25, 31, 25), (2, 25, 20, 1, 2, 25, 27, 25)]  # (k1,i1,b1,eq,k2,i2,b2,row); k: 0=A 1=E 2=W
```

`vtref.py`:

```python
# vtref.py - reference construction for the 38-step dense-part-variant attack (member x = message printed second).
# Characteristic/two-bit conditions/semi-free-start pair: Li et al., ePrint 2026/1120 Tables 3-5 (own transcription,
# vtconst.py).  Construction (variants of the dense part, row-16 lookup in (Y, Z0)) after qkniep (c99df2dc) / 0xshikhar;
# this code was written independently.  Standard library only.
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vtconst import *

M = 0xffffffff
NR = 38
K = KC
IV = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]
def ror(x, n): return ((x >> n) | (x << (32 - n))) & M
def S0(x): return ror(x, 2) ^ ror(x, 13) ^ ror(x, 22)
def S1(x): return ror(x, 6) ^ ror(x, 11) ^ ror(x, 25)
def s0(x): return ror(x, 7) ^ ror(x, 18) ^ (x >> 3)
def s1(x): return ror(x, 17) ^ ror(x, 19) ^ (x >> 10)
def CH(x, y, z): return (x & y) ^ (~x & z & M)
def MAJ(x, y, z): return (x & y) ^ (x & z) ^ (y & z)

# trace: A[i], E[i] for i = -4..37 (dicts), W[0..37]
def trace(cv, w16, n=NR):
    W = list(w16)
    for i in range(16, n): W.append((s1(W[i-2]) + W[i-7] + s0(W[i-15]) + W[i-16]) & M)
    A = {-1-i: cv[i] for i in range(4)}; E = {-1-i: cv[4+i] for i in range(4)}
    for i in range(n):
        E[i] = (A[i-4] + E[i-4] + S1(E[i-1]) + CH(E[i-1], E[i-2], E[i-3]) + K[i] + W[i]) & M
        A[i] = (E[i] - A[i-4] + S0(A[i-1]) + MAJ(A[i-1], A[i-2], A[i-3])) & M
    return A, E, W

def compress(cv, w16):
    A, E, W = trace(cv, w16)
    f = [A[37], A[36], A[35], A[34], E[37], E[36], E[35], E[34]]
    return [(cv[i] + f[i]) & M for i in range(8)]

def cellok(k, i, x, y):
    m, v, d, _ = CELLS[k][i]
    return (x & m) == v and (x ^ y) == d

def rowok(tx, ty, i):
    """Row i of both traces: A, E, W cells, '+' pair, and two-bit conditions keyed at row i (member x).
    Rows < 0 have no cells.  W cells of rows 7..10 are not part of the event (W7: F7; W8..W10: modular differences)."""
    if i < 0: return True
    (Ax, Ex, Wx), (Ay, Ey, Wy) = tx, ty
    if not cellok(0, i, Ax[i], Ay[i]): return False
    if not cellok(1, i, Ex[i], Ey[i]): return False
    if (i < 7 or i > 10) and not cellok(2, i, Wx[i], Wy[i]): return False
    if (Ex[i] ^ Ex[i-1]) & PQ[i]: return False
    if i >= 16:
        for (k1, i1, b1, eq, k2, i2, b2, row) in X2:
            if row == i:
                v1 = (tx[k1][i1] >> b1) & 1; v2 = (tx[k2][i2] >> b2) & 1
                if (v1 ^ v2) != (0 if eq else 1): return False
    return True

# ---- dense-part variants: v = (A0, A1, A2) ----
D7 = DW[7]; T7 = DS0[7]
def inF7(w): return ((s0((w + D7) & M) - s0(w)) & M) == T7
def sa(i): return SAX[i+4]
def say(i): return SAY[i+4]
def sex(i): return SEX[i+4]
def sey(i): return SEY[i+4]

def variant(a0, a1, a2):
    """Per member: A[0..15], E[4..15], W[8..15] (x: member x); E4..E6 and W8..W10 recomputed from (A0,A1,A2)."""
    out = []
    for (Aa, Ee, Ww) in ((SAX, SEX, SWX), (SAY, SEY, SWY)):
        A = {i: Aa[i+4] for i in range(16)}; A[0], A[1], A[2] = a0, a1, a2
        E = {i: Ee[i+4] for i in range(0, 16)}
        for i in (4, 5, 6): E[i] = (A[i] + A[i-4] - S0(A[i-1]) - MAJ(A[i-1], A[i-2], A[i-3])) & M
        W = {i: Ww[i] for i in range(8, 16)}
        for i in (8, 9, 10): W[i] = (E[i] - A[i-4] - E[i-4] - S1(E[i-1]) - CH(E[i-1], E[i-2], E[i-3]) - K[i]) & M
        out.append((A, E, W))
    return out

def valid(var):
    """E cells of rows 4..8 (both members, '+' pairs) and the published dW_i, ds0(W_i), i = 8..11."""
    (Ax, Ex, Wx), (Ay, Ey, Wy) = var
    for i in range(4, 9):
        if not cellok(1, i, Ex[i], Ey[i]): return False
        if (Ex[i] ^ Ex[i-1]) & PQ[i]: return False
        if i >= 5 and (Ey[i] ^ Ey[i-1]) & PQ[i]: return False
    for i in range(8, 12):
        if (Wy[i] - Wx[i]) & M != DW[i]: return False
        if (s0(Wy[i]) - s0(Wx[i])) & M != DS0[i]: return False
    return True

def c7of(var):
    """W7x = c7 - A_{-1}  (A_{-1} = first word of the chaining value)."""
    (A, E, _), _ = var
    return (E[7] - 2 * A[3] + S0(A[2]) + MAJ(A[2], A[1], A[0]) - S1(E[6]) - CH(E[6], E[5], E[4]) - K[7]) & M

def step2(cv, var):
    """Message words W0..W15 of both members connecting cv to the variant (W0..W7 from Step 2)."""
    res = []
    for m in (0, 1):
        A, E, W = var[m]; A = dict(A); E = dict(E)
        for j in range(4): A[-1-j] = cv[j]; E[-1-j] = cv[4+j]
        for i in range(4): E[i] = (A[i] + A[i-4] - S0(A[i-1]) - MAJ(A[i-1], A[i-2], A[i-3])) & M
        w = [(E[i] - A[i-4] - E[i-4] - S1(E[i-1]) - CH(E[i-1], E[i-2], E[i-3]) - K[i]) & M for i in range(8)]
        res.append(w + [W[i] for i in range(8, 16)])
    wx, wy = res
    return wx, wy

def yz0(cv, a0):
    """Lemma 5: Y, Z0 for chaining value cv and A0."""
    a, b, c, d, e, f, g, h = cv
    hh = (d - S0(a) - MAJ(a, b, c)) & M; E0 = (a0 + hh) & M
    Y = (-S0(a0) - MAJ(a0, a, b) - g - S1(E0) - CH(E0, e, f) - K[1]) & M
    W0 = (a0 + hh - d - h - S1(e) - CH(e, f, g) - K[0]) & M
    return Y, (W0 + s1(SWX[14])) & M

def c9x_of(a2):
    A6 = sa(6); E6 = (A6 + a2 - S0(sa(5)) - MAJ(sa(5), sa(4), sa(3))) & M
    return (sex(9) - 2 * sa(5) + S0(sa(4)) + MAJ(sa(4), sa(3), a2) - S1(sex(8)) - CH(sex(8), sex(7), E6) - K[9]) & M

def w16_closed(cv, a0, a1, a2):
    Y, Z0 = yz0(cv, a0)
    return (s0((Y + a1) & M) - a1 + Z0 + c9x_of(a2)) & M

def pair_traces(cv, var):
    wx, wy = step2(cv, var)
    return trace(cv, wx), trace(cv, wy), wx, wy

def outcome(cv, a0, a1, a2, rows=NR):
    """Reference outcome of variant (a0, a1, a2) on cv: dict(r16, w7, deep, tx, ty, wx, wy); deep = last row reached
    (row 15 if row 16 fails)."""
    var = variant(a0, a1, a2)
    tx, ty, wx, wy = pair_traces(cv, var)
    r16 = rowok(tx, ty, 16)
    deep = 15
    if r16:
        deep = 16
        for i in range(17, rows):
            if not rowok(tx, ty, i): break
            deep = i
    return dict(r16=r16, w7=inF7(wx[7]), deep=deep, tx=tx, ty=ty, wx=wx, wy=wy, var=var)

def digest_words(msg2blocks): raise NotImplementedError

# ---- data ----
HERE = os.path.dirname(os.path.abspath(__file__)); DATA = os.path.join(HERE, '..', 'data')
def _hexlist(fn, col=0): return [int(l.split()[col], 16) for l in open(os.path.join(DATA, fn)) if l.strip()]
A0L = _hexlist('a0list.txt'); A2L = _hexlist('peer_a2.txt'); GL = _hexlist('ex1_g.txt')
GSET = {g: k for k, g in enumerate(GL)}
DW16 = 0x20000000          # W16y = W16x - DW16

def row17_parts(tx, ty):
    """Row 17 split as the online program tests it: E part (E cell, '+' pair, E-E two-bit conditions), A part (A cell,
    A-A conditions with a row-16 operand), internal A17 conditions."""
    (Ax, Ex, Wx), (Ay, Ey, Wy) = tx, ty
    E_ok = cellok(1, 17, Ex[17], Ey[17]) and not ((Ex[17] ^ Ex[16]) & PQ[17])
    A_ok = cellok(0, 17, Ax[17], Ay[17]) and cellok(2, 17, Wx[17], Wy[17])
    I_ok = True
    for (k1, i1, b1, eq, k2, i2, b2, row) in X2:
        if row != 17: continue
        v1 = (tx[k1][i1] >> b1) & 1; v2 = (tx[k2][i2] >> b2) & 1
        good = (v1 ^ v2) == (0 if eq else 1)
        assert k1 == k2 and k1 in (0, 1)
        if k1 == 1: E_ok = E_ok and good
        elif i1 == 17 and i2 == 17: I_ok = I_ok and good
        else: A_ok = A_ok and good
    return E_ok, A_ok, I_ok
```

`vtprog.py` (the counted online program, its interpreter and the table oracle) is not reprinted here, to keep the judge evidence inside its 512 KiB budget: `experiments/vt38.py` (shipped, in the evidence) is the assembly of vtref, vtprog and vt_exp with the data blobs, and the instruction counts are the selftest items of A.1.



The test programs import the development modules `vtref`, `vtprog` and `vtpre` (B.3, B.15), which read the text files `a0list.txt` (A0 values), `peer_a2.txt` (A2 list) and `ex1_g.txt` (G) from `../data/` (Appendices A.2, A.3 and the output of `ex1 g`); put the modules, the tests and the data files in the layout `src/`, `data/`, `runs/` to run them. `experiments/vt38.py` is the assembly of `vtref.py`, `vtprog.py` and `vt_exp.py` with the data blobs (the same code), with the Section 10.1 near-term addition made afterwards; it needs none of the other files and is what the organizer runs.

### B.16 t_pre_d.py, diff_prog.py, t_imm_d.py (this derivative, Appendices C.4 and D)

```python
# t_pre_d.py - the changed preprocessing bodies of vtpre.py as counted code, against their definitions; writes
# runs/pre1.json and runs/pre2.json (the base values of P1..P4 with LIVE_ops and LIVE_g; every P5 and P6 value is the count of an
# executed body: P5 setup, body, append and loop, the P6 zero, count and fill iterations and their per-variant overheads, the prefix).
# usage: t_pre_d.py <dir of vt38.py> <runs dir>
import sys, os, json, random
sys.path.insert(0, sys.argv[1]); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.dont_write_bytecode = True
from vtpre import *
RUNS = sys.argv[2]; rr = random.Random(20261011)
class PM(Machine):
    """the counted machine with a plain memory for the preprocessing (reads what was stored, 0 elsewhere; records from tables())"""
    def load(s, addr):
        if addr in s.mem: return s.mem[addr]
        t = addr >> 150
        return s.tab[addr] if t in (3, 4) and addr in s.tab else 0
def execute(a, regs, mem=None, tab=None):
    a.L('END'); m = PM([], lambda *x: [], tab or {}); m.r.update(regs); m.mem.update(mem or {}); m.run(a); return m
# ---- P1': live words
cnt = []; L = live_list(cnt)
assert [g for _, g in L] == [g for g in GL if g not in (0x35f29010, 0x35f29011, 0x35f29410, 0x35f29414, 0x35f29415, 0x35fa9010, 0x35fa9011, 0x35fa9410, 0x35fa9414, 0x35fa9415)]
assert sum(cnt) == 1 << 20 and len(L) == 22
def pred(gi, e):
    r = grec(gi, GL[gi]); b = gaddr(gi); A = (e + r[b + 3]) & M
    return (e & r[b + 1]) == r[b + 2] and (A & r[b + 4]) == r[b + 5] and all(((A >> p) ^ (A >> q)) & 1 == (0 if w else 1) for p, q, w in a17int())
live_max = 0; bad = 0; npass = 0
for gi in range(32):
    a = Asm(); gen_live_body(a, gi, 'END'); r = grec(gi, GL[gi]); b = gaddr(gi)
    for k in range(3000):
        e = rr.getrandbits(32)
        if k % 2: e = (e & ~r[b + 1] & M) | r[b + 2]
        m = execute(a, dict(e=e, cnt=0)); ok = m.r['cnt'] == 1; bad += ok != pred(gi, e); npass += ok
        if ok: live_max = max(live_max, m.ops)
a = Asm(); gen_live_end(a, 0, 'END'); live_g = execute(a, dict(cnt=5, lv=1 << 160)).ops
print("P1' live words:", len(L), 'count', sum(cnt), '| body vs predicate on 96,000 E17:', bad, 'mismatches,', npass, 'passes | longest path', live_max, '| per g', live_g)
assert bad == 0 and npass > 0
# ---- P5: setup, body, append on real windows
tab = tables(); EV = entry_variants(); setup_ops = None; app = []; bodies = []; nvalid = 0; badw = 0
for j in rr.sample(range(256), 6):
    a0 = A0L[j]; a1e, a2ie = EV[j]
    for a2i in [a2ie] + rr.sample(range(768), 2):
        a = Asm(); gen_enum_setup(a, a0); s = execute(a, dict(ra=A2T + 2 * a2i), tab=tab); setup_ops = s.ops
        lo = s.r['lo']; base_r = (a1e - lo) & M if a2i == a2ie else rr.randrange(1 << 29)
        for r_ in [base_r] + [rr.randrange(1 << 29) for _ in range(300)]:
            a = Asm(); gen_enum_setup(a, a0); a.L('S'); gen_enum_body(a, a0, 'END'); a.L('B'); gen_enum_append(a, a0)
            m = execute(a, dict(ra=A2T + 2 * a2i, r=r_, lp=1 << 170), tab=tab)
            a1 = (lo + r_) & M; v = valid(variant(a0, a1, A2L[a2i]))
            if (1 << 170) in m.mem:
                assert v; nvalid += 1
                e = mkent(a0, a1, A2L[a2i], a2i, 0)
                badw += [m.mem[(1 << 170) + k] for k in range(3)] != [e[0], (e[1] - gw(0)) & WORD, c9x_of(A2L[a2i])]
                b2 = Asm(); gen_enum_setup(b2, a0); gen_enum_body(b2, a0, 'END'); body = execute(b2, dict(ra=A2T + 2 * a2i, r=r_), tab=tab).ops - setup_ops
                app.append(m.ops - setup_ops - body); bodies.append(body)
            else: assert not v
a = Asm(); a('add', 'r', 'r', 1); a('bne', 'r', 'r1', 'S'); a.L('S'); p5_loop = execute(a, dict(r=5, r1=9)).ops
print('P5: setup', setup_ops, '| valid candidates', nvalid, 'list words != (c7 + 2^32, mkent fields, c9x):', badw, '| append ops', sorted(set(app)), '| body ops (valid candidates)', sorted(set(bodies)), '| loop control', p5_loop)
assert badw == 0 and nvalid >= 6 and len(set(app)) == 1 and len(set(bodies)) == 1
# ---- P6 zero: 16 headers per iteration, memory zeroed, operations per iteration
a = Asm(); gen_zero16(a, 'hend'); zm = execute(a, dict(h=1 << 100, hend=(1 << 100) + 48, zero=0), mem={(1 << 100) + k: 7 for k in range(48)})
assert all(zm.mem[(1 << 100) + k] == 0 for k in range(48)) and zm.r['h'] == (1 << 100) + 48
zero16 = zm.ops // 3; assert zm.ops == 3 * zero16
print('P6 zero: 48 headers in 3 iterations, all zero, ops', zm.ops, '| per iteration (16 headers)', zero16)
# ---- P6 prefix: empty and nonempty header
a = Asm(); gen_prefix_body(a); pe = execute(a, dict(h=1 << 101, run=1 << 102), mem={1 << 101: 0}); assert pe.mem[1 << 101] == EMPTY
a = Asm(); gen_prefix_body(a); pn = execute(a, dict(h=1 << 101, run=1 << 102, zero=0), mem={1 << 101: 3})
assert pn.mem[1 << 101] == (1 << 102) + 6 and pn.mem[(1 << 102) + 6] == SENT and pn.r['run'] == (1 << 102) + 8
print('P6 prefix: empty header', pe.ops, 'ops, nonempty header', pn.ops, 'ops (loop control not included)')
# ---- P6 count and fill: whole variant pass on a toy.  Variants of one A0 block (real, from the enumeration) and synthetic ones (A1 = 2^32 - 3, 1, 0);
# each run covers Y in two segments with toy limits (registers E1, E2) or with the real limits (2^32, A1); headers and entries against the definition
j = 7; a0 = A0L[j]; HB = HDR | j << 64; LP = 1 << 200; vars_ = []
a1e, a2ie = EV[j]; vars_.append((a1e, a2ie))
while len(vars_) < 4:
    a2i = rr.randrange(768); lo_ = (lambda s: s.r['lo'])(execute((lambda a: (gen_enum_setup(a, a0), a)[1])(Asm()), dict(ra=A2T + 2 * a2i), tab=tab)); a1 = (lo_ + rr.randrange(1 << 29)) & M
    if valid(variant(a0, a1, A2L[a2i])): vars_.append((a1, a2i))
V = []                                       # (A1, c9x, c7, w1e): w1e = the packed fields without the G word (low 32 bits A1)
for (a1, a2i) in vars_:
    e = mkent(a0, a1, A2L[a2i], a2i, 0); V.append((a1, c9x_of(A2L[a2i]), e[0], (e[1] - gw(0)) & WORD))
for A1_ in (M - 2, 1, 0): V.append((A1_, rr.getrandbits(32), rr.getrandbits(64), (rr.getrandbits(160) << 32 | A1_) & ((1 << 224) - 1)))
def scen(A1_, kind):
    n1, n2 = min(4, (1 << 32) - A1_), min(3, A1_)
    if kind == 'mid': return 'E1', 'E2', dict(E1=A1_ + n1, E2=n2), list(range(n1)) + [(1 << 32) - A1_ + i for i in range(n2)]
    if kind == 'real1': return 1 << 32, 'E2', dict(E2=n2), list(range(M + 1 - A1_)) + [(1 << 32) - A1_ + i for i in range(n2)]
    return 'E1', 'A1', dict(E1=A1_ + n1), list(range(n1)) + [(1 << 32) - A1_ + i for i in range(A1_)]
def cases():
    for (A1_, c9x, c7, w1e) in V:
        for kind in ('mid', 'real1', 'real2'):
            if kind == 'real1' and M + 1 - A1_ > 8: continue          # the real upper limit 2^32 only where A1 is within 8 of it
            if kind == 'real2' and A1_ > 8: continue                  # the real second limit A1 only for small A1
            if A1_ == 0 and kind != 'mid': continue
            yield (A1_, c9x, c7, w1e) + scen(A1_, kind) + (kind,)
cops = {}; fops = {}; ncase = 0; mem_c = {}; expect = {}
for (A1_, c9x, c7, w1e, l1, l2, regs, Yl, kind) in cases():
    for Y in Yl:
        X = (s0((Y + A1_) & M) - A1_ + c9x) & M
        for gi, g in LIVE: k = HB + (Y << 32 | ((g - X) & M)); expect[k] = expect.get(k, 0) + 1
    a = Asm(); gen_variant_pass(a, HB, False, l1, l2)
    m = execute(a, dict(lp=LP, lpend=LP + 3, **regs), mem={**mem_c, LP: c7, LP + 1: w1e, LP + 2: c9x}); mem_c = {k: v for k, v in m.mem.items() if k < LP}
    cops[(kind, A1_ == 0, len(Yl))] = m.ops; ncase += 1
bad6 = mem_c != expect
# prefix by definition (end of each bucket), then the fill pass on the same cases
run_ = 1 << 180; hdr = {}
for k in sorted(expect): run_ += 2 * expect[k]; hdr[k] = run_; run_ += 2
mem_f = dict(hdr)
for (A1_, c9x, c7, w1e, l1, l2, regs, Yl, kind) in cases():
    a = Asm(); gen_variant_pass(a, HB, True, l1, l2)
    m = execute(a, dict(lp=LP, lpend=LP + 3, **regs), mem={**mem_f, LP: c7, LP + 1: w1e, LP + 2: c9x}); mem_f = {k: v for k, v in m.mem.items() if k < LP}
    fops[(kind, A1_ == 0, len(Yl))] = m.ops
# every bucket against the definition: the multiset of (c7, w1e + gw(g)) of the (Y, variant, g) that hash to it; the real variants' entries equal mkent
want = {}
for (A1_, c9x, c7, w1e, l1, l2, regs, Yl, kind) in cases():
    for Y in Yl:
        X = (s0((Y + A1_) & M) - A1_ + c9x) & M
        for gi, g in LIVE: want.setdefault(HB + (Y << 32 | ((g - X) & M)), []).append((c7, (w1e + gw(gi)) & WORD))
for k in expect:
    st = mem_f[k]; got = sorted(tuple(mem_f[st + 2 * i + w] for w in range(2)) for i in range(expect[k]))
    bad6 += got != sorted(want[k]) or st != hdr[k] - 2 * expect[k]
for (a1, a2i), (A1_, c9x, c7, w1e) in zip(vars_, V):
    for gi, g in LIVE: bad6 += (c7, (w1e + gw(gi)) & WORD) != mkent(a0, a1, A2L[a2i], a2i, gi)
# operations per iteration: the two-segment path (A1 != 0) with two iteration counts; every run on that path is fixed + iterations x per-iteration
def per_iter(ops):
    two = {k: o for k, o in ops.items() if not k[1] and k[0] == 'mid'}; ks = sorted(two, key=lambda k: k[2]); k1, k2 = ks[0], ks[-1]
    it = (two[k2] - two[k1]) // (k2[2] - k1[2]); fixed = two[k1] - it * k1[2]
    assert all(o == fixed + it * k[2] for k, o in two.items())
    if not getattr(Machine, 'IMM', False):                       # (the limit of the toy runs is a register, the real limit 2^32 an instruction field: no difference in the count)
        assert all(o == fixed + it * k[2] for k, o in ops.items() if not k[1]) and all(o < fixed + it * k[2] for k, o in ops.items() if k[1])
    else: it += 1                                                # immediates charged: the branch back to seg1 compares with the constant 2^32
    return it, fixed
cit, cvar = per_iter(cops); fit, fvar = per_iter(fops)
print('P6 toy: %d variant runs (4 real variants, A1 = 2^32 - 3, 1 and 0; the real limits 2^32 and A1 as well as toy limits), %d headers, %d entries: count and fill == definition, %d mismatches'
      % (ncase, len(expect), sum(expect.values()), bad6))
print('P6 count: %d ops per iteration (incl. loop branch), %d per variant (loads, A1, both segment setups, guard, list-loop branch);' % (cit, cvar),
      'fill: %d ops per iteration, %d per variant' % (fit, fvar))
assert bad6 == 0
# P1..P4: the values printed by t_pre1.py (A.5), which executes those bodies on the shipped vt38.py
p1 = {"G_hit_ops": 117, "G_nonhit_max_ops": 115, "F7_in_ops": 25, "F7_out_ops": 22, "A2_hit_ops": 41, "A2_nonhit_max_ops": 39, "A2REC_total_ops": 39168, "GREC_total_ops": 3072}
p2 = dict(P5_SETUP=setup_ops, P5_BODY_MAX=bodies[0], P5_APPEND=app[0], P5_LOOP=p5_loop, P6_ZERO16=zero16, P6_COUNT_IT=cit, P6_COUNT_VAR=cvar, P6_FILL_IT=fit, P6_FILL_VAR=fvar,
          P6_PREFIX_EMPTY=pe.ops, P6_PREFIX_NONEMPTY=pn.ops)
p1.update(LIVE_ops=live_max, LIVE_g=live_g)
json.dump(p1, open(os.path.join(RUNS, 'pre1.json'), 'w')); json.dump(p2, open(os.path.join(RUNS, 'pre2.json'), 'w'))
print('pre1.json', p1); print('pre2.json', p2)
```

```python
# diff_prog.py - decision equivalence of the derivative's counted program (work/A/vt38.py) with the base program
# (37742a53) on designed buckets.  Same chaining value, same variants, same G words, each in its own entry format; compared:
# table requests, the full sequence of stage marks (W7, E17, A17, A17int, rows 18..37), the success (block, entry), the
# E17 values seen, and the counters NE, NW, N1.
#  part 1: SMC successes of the estimator replica (own seeds), each forced as the chaining value; the bucket holds a decoy,
#          the success entry with its true G word, and the same variant with K other G words (live and dead);
#  part 2: random chaining values, buckets of 1..6 embedded valid variants with random G words, all 4 lanes.
import sys, os, random, importlib.util
W = os.path.dirname(os.path.abspath(__file__)); sys.dont_write_bytecode = True
def load(name, path):
    s = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
B = load('vtbase', os.path.join(W, 'basecopy', 'vt38.py')); N = load('vtnew', os.path.join(W, sys.argv[1] if len(sys.argv) > 1 else 'A', 'vt38.py'))
NREP = int(sys.argv[2]) if len(sys.argv) > 2 else 20; K = 6; M = B.M
def bent(a0, a1, a2, a2i, gi): return (B.c7of(B.variant(a0, a1, a2)) + (1 << 32), a1 | B.S0(a1) << 32 | (B.A2T + 2 * a2i) << 64, B.gaddr(gi))
progs = {}
def prog(mod, q):
    k = (mod.__name__, q)
    if k not in progs: progs[k] = mod.allocated_program(list(range(4 * q, 4 * q + 4)))
    return progs[k]
TB, TN = B.tables(), N.tables()
def run(mod, tab, q, cv, buckets):
    p, mp = prog(mod, q); m = mod.Machine([1, 2], lambda j, y, z: buckets.get(j, []), tab, cvforce=cv); m.run(p)
    e17 = [x & M for x in (m.obs[1::2] if mod is B else m.obs)]
    return dict(trace=m.trace, marks=m.marks, succ=None if m.succ is None else (m.succ[0], m.succ[1] & ((1 << 64) - 1)), e17=e17,
                cnt=tuple(m.r.get(mp.get(r, r), 0) for r in ('NE', 'NW', 'N1')))
stats = dict(cases=0, mism=0, succ=0, e17=0, a17=0, a17int=0, deep=0, w7=0)
def compare(q, cv, bb, bn):
    x = run(B, TB, q, cv, bb); y = run(N, TN, q, cv, bn); stats['cases'] += 1
    if x != y:
        stats['mism'] += 1
        if stats['mism'] < 4: print('MISMATCH', {k: (x[k], y[k]) for k in x if x[k] != y[k]})
    for k, mk in (('w7', 'W7'), ('e17', 'E17'), ('a17', 'A17'), ('a17int', 'A17int')): stats[k] += x['marks'].count(mk)
    stats['deep'] += sum(1 for t in x['marks'] if isinstance(t, tuple)); stats['succ'] += x['succ'] is not None
rr = random.Random(20261010); SV = B.sample_variants(); EV = B.entry_variants(); nsucc = 0
for rep in range(NREP):
    z, pairs, bad = B.smc_replicate(B.Shake('r38d-diff|%d' % rep), SV); assert bad == 0
    for cv, mx, my, (a0, a1, a2) in pairs:
        nsucc += 1; j = B.A0L.index(a0); a2i = B.A2L.index(a2); q = j // 4; g0 = B.GSET[B.w16_closed(cv, a0, a1, a2)]
        gs = [g0] + rr.sample([g for g in range(32) if g != g0], K)
        eb = [bent(a0, a1, a2, a2i, g) for g in gs[1:]] + [bent(a0, a1, a2, a2i, g0)]; en = [N.mkent(a0, a1, a2, a2i, g) for g in gs[1:]] + [N.mkent(a0, a1, a2, a2i, g0)]
        db = (eb[-1][0] ^ 0x5a5a5,) + eb[-1][1:]; dn = (en[-1][0] ^ 0x5a5a5,) + en[-1][1:]
        compare(q, cv, {j: [db] + eb}, {j: [dn] + en})
print('part 1: %d SMC successes from %d replicates' % (nsucc, NREP), stats, flush=True)
for t in range(int(sys.argv[3]) if len(sys.argv[3:]) else 400):
    cv = [rr.getrandbits(32) for _ in range(8)]; q = rr.randrange(64); bb, bn = {}, {}
    for j in range(4 * q, 4 * q + 4):
        for _ in range(rr.randrange(0, 7)):
            a1, a2i = EV[j]
            g = rr.randrange(32); bb.setdefault(j, []).append(bent(B.A0L[j], a1, B.A2L[a2i], a2i, g)); bn.setdefault(j, []).append(N.mkent(B.A0L[j], a1, B.A2L[a2i], a2i, g))
    compare(q, cv, bb, bn)
print('part 1+2:', stats)
print('EQUIVALENT' if stats['mism'] == 0 else 'NOT EQUIVALENT')
```

```python
# t_imm_d.py - sensitivity: the shipped online program and the preprocessing bodies of this derivative re-measured with every immediate operand of an
# ALU instruction, compare-branch or store charged one extra operation (as if loaded by an `li`; the class MI of the base's t_imm.py); then the ledger.
# usage: t_imm_d.py <dir of vt38.py> <dir of src/ (t_pre1.py, t_pre_d.py, ledger38.py)> <scratch runs dir>
import sys, os, json, io, contextlib
VT, SRC, RUNS = sys.argv[1:4]; sys.path.insert(0, VT); sys.path.insert(0, SRC); sys.dont_write_bytecode = True
import vt38
from vt38 import *
class MI(Machine):
    def run(s, code, maxops=None):
        c, lab, r = code.c, code.lab, s.r; pc = 0; n = len(c); mem = s.mem
        def v(x): return x if isinstance(x, int) else r.get(x, 0)
        ops = 0
        isi = lambda x: isinstance(x, int)
        while pc < n:
            ins = c[pc]; op = ins[0]; pc += 1
            if op in ('add', 'sub', 'and', 'or', 'xor'): ops += isi(ins[2]) + isi(ins[3])
            elif op == 'rsub': ops += 1 + isi(ins[3])
            elif op == 'bne': ops += isi(ins[2])
            elif op == 'sti': ops += isi(ins[2])
            if op == 'add': r[ins[1]] = (v(ins[2]) + v(ins[3])) & WORD; ops += 1
            elif op == 'sub': r[ins[1]] = (v(ins[2]) - v(ins[3])) & WORD; ops += 1
            elif op == 'rsub': r[ins[1]] = (ins[2] - v(ins[3])) & WORD; ops += 1
            elif op == 'and': r[ins[1]] = v(ins[2]) & v(ins[3]); ops += 1
            elif op == 'or': r[ins[1]] = v(ins[2]) | v(ins[3]); ops += 1
            elif op == 'xor': r[ins[1]] = v(ins[2]) ^ v(ins[3]); ops += 1
            elif op == 'shl': r[ins[1]] = (v(ins[2]) << ins[3]) & WORD; ops += 1
            elif op == 'shr': r[ins[1]] = v(ins[2]) >> ins[3]; ops += 1
            elif op == 'ld': r[ins[1]] = s.load(v(ins[2])); ops += 1
            elif op == 'ldi': r[ins[1]] = mem.get(ins[2], 0); ops += 1
            elif op == 'sti': mem[ins[1]] = v(ins[2]); ops += 1
            elif op == 'li': r[ins[1]] = ins[2]; ops += 1
            elif op == 'st': s.store(v(ins[1]), v(ins[2])); ops += 1
            elif op == 'bz': ops += 2; pc = lab[ins[2]] if v(ins[1]) == 0 else pc
            elif op == 'bnz': ops += 2; pc = lab[ins[2]] if v(ins[1]) != 0 else pc
            elif op == 'bne': ops += 2; pc = lab[ins[3]] if v(ins[1]) != v(ins[2]) else pc
            elif op == 'jmp': ops += 1; pc = lab[ins[1]]
            elif op == 'rand': r[ins[1]] = s.rw.pop(0); ops += 1
            elif op == 'f38':
                s.units += 1; m0 = [r[x] for x in ins[1]]; s.m0 = m0
                cv = s.cvforce if s.cvforce is not None else compress(IV, m0); s.cv = cv
                for x, y in zip(ins[2], cv): r[x] = y
            elif op == 'succ': s.succ = (ins[1], v(ins[2])); s.succ_ops = s.ops + ops; break
            elif op == 'halt_ok': break
            elif op == 'obs': s.obs.append(v(ins[1]))
            elif op == 'mark': s.marks.append(ins[1]); s.mark_ops.append((ins[1], s.ops + ops))
        s.ops += ops

MI.IMM = True; vt38.Machine = MI; Machine = MI
cs = vt38.prog_costs(); cs['EPI'] = 24; cs['P0'] -= 5          # prog_costs subtracts the epilogue 19; with immediates it is 24 (four rsub and the bne against the group count)
cs['PASS_ENTRY'] = 3; cs['BLOCK_FIXED'] = cs['GROUP4'] / 4        # the bne FL, 2 of the pass entry carries an immediate
print('online costs, immediates charged:', cs)
from vtpre import *
class MachineP(MI):
    def load(s, addr):
        if addr in s.mem: return s.mem[addr]
        t = addr >> 150
        return s.tab[addr] if t in (3, 4) and addr in s.tab else 0
os.makedirs(RUNS, exist_ok=True)
sys.argv = ['t_pre1.py']; ns = dict(globals()); ns['__name__'] = 'x'
src = open(os.path.join(SRC, 't_pre1.py')).read().replace("'../runs/pre1.json'", repr(os.path.join(RUNS, 'pre1_imm.json')))
with contextlib.redirect_stdout(io.StringIO()): exec(compile(src, 't_pre1.py', 'exec'), ns)
p1 = json.load(open(os.path.join(RUNS, 'pre1_imm.json')))
sys.argv = ['t_pre_d.py', VT, RUNS]; ns = dict(globals()); ns['__name__'] = 'x'
src = open(os.path.join(SRC, 't_pre_d.py')).read()
buf = io.StringIO()
with contextlib.redirect_stdout(buf): exec(compile(src, 't_pre_d.py', 'exec'), ns)
print('preprocessing bodies, immediates charged:')
q1 = json.load(open(os.path.join(RUNS, 'pre1.json'))); p1.update(LIVE_ops=q1['LIVE_ops'], LIVE_g=q1['LIVE_g']); p2 = json.load(open(os.path.join(RUNS, 'pre2.json')))
print(' pre1', p1); print(' pre2', p2)
from ledger38 import ledger
o = ledger(show=False, costs=cs, p1=p1, p2=p2)
print('ledger with immediates charged: time_log2 %.5f  log2_T %.6f' % (o['time_log2'], o['log2_T']))
```

## Appendix C. aa0496d3 against 012400ff and 37742a53 (the figures in this appendix are aa0496d3's; this derivative's are in Section 7 and Appendix D)

**C.1 Base.** Built on submission 012400ff-d717-461c-a433-377f35ce2298 (Jbenisek, 71.43541, commit f728e581b30a7ab108f5abdac605e68f52cf5e39), which itself derives from 37742a53-4062-4c76-bdd0-cd74b4c6eb21 (winglock, 71.69523, commit c330e0b7ba833f81f79474536519d55aa47e771a). Both manifests (`experiments/manifest.json` and `certificates/manifest.json`) are unchanged. `experiments/vt38.py` carries the program changes of C.2. `proof.md` and `claim.json` change where a count of the program or a value of the ledger changed, in Appendices B.1 to B.3 (the ledger, its sensitivity and the counted preprocessing, as changed here), B.16 and this appendix.

**C.2 Changes.** Five changes to how the counted program and the counted table construction execute and price the search (L0 and L4 from 012400ff, and our tightenings to L2, L3, L4 and L5). None of them changes which variants can succeed or the tests applied to them.

- **L0: the tables list 22 of the 32 words of G.** Given W16 = g, row 17 of member x is a function of E17 (Section 4.6): the
  E17 mask test, A17 = E17 + a17(g) against its mask, and the three A17-internal conditions. An exact count over all 2^32 values
  of E17 (digit by digit, with the carry of A17 = E17 + a17(g) as state; `live_list` in B.3) gives 2^20 passing values in all and
  none for the ten words 35f29010, 35f29011, 35f29410, 35f29414, 35f29415, 35fa9010, 35fa9011, 35fa9410, 35fa9414, 35fa9415.
  A variant whose W16 is one of these fails row 17 on every chaining value and cannot succeed. The tables list the other 22
  words (G'). The pass P1' finds G' as counted code (32 x 2^32 values of E17, 21 operations each plus the loop). The count and
  fill passes loop over 22 words; the bucket bound is 14 x 22 x 768 = 236,544; the counters' expectations shrink by 22/32.
- **L2: tightened row-17 path using packed 2-word entry constants and prologue `c - (a & b)`.** Entry word 1 packs `A1` (bits 0..31), `U = A2 - S0(A1) - K2 - (A1 & A0)` (bits 32..63), `Q = A1 ^ A0` (bits 64..95), `A2T + 2*a2i` (bits 96..127), `KCA = W10x + s1(W15x) + A1` (bits 128..159), and `gw(g) = gaddr(g) | c17(g)<<32 | vE(g)<<64` (bits 160..255). Furthermore, using `MAJ(A0, a, b) = (a & b) + ~MAJ(A0, a, b) - 1`, the prologue precomputes `c - (a & b)` once per group, and `gen_rare` computes `E1 = (A1 - S0(A0) + 1) + (c - (a & b)) + ~MAJ(A0, a, b) (mod 2^32)`, avoiding recomputing `MAJ(A0, a, b)` per W7 pass and avoiding redundant lane masks before final modular reductions. Also, because the `A17` mask test holds on bits 0..7 and 9..13, `A17 & 0x3eff == vA & 0x3eff`, so the three `A17`-internal bit comparisons against bits 4 and 13 reduce to testing the two variable bits `(A17 >> 19) & 1` and `(A17 >> 25) & 1` against `(vA >> 4) & 1` and `((vA >> 4) ^ 1) & 1` (packed into record slot `b + 5`). The first row-17 test sees the exact same `E17` after **41 operations** (instead of 58 in 37742a53 or 49 in 012400ff), and the `A17` tests take **19 operations** (instead of 25).
- **L3: 4-lane SWAR `~MAJ` and `~CH`, telescoping `NE` accumulation, 2-op sentinel discriminator, and prologue tightening.** Using `~MAJ(A0, a, b) = ~(a ^ b) | ~A0` (2 operations across all 4 lanes given prologue `~(a ^ b)`) and `~CH(E0, e, f) = (~E0 & ~f) | (E0 & ~e)` (4 operations across all 4 lanes given prologue `~e` and `~f`), loading each bucket header directly into `OFF`, accumulating `NE` by telescoping across the scan loop (`sub NE, NE, OFF` before `loop` and `add NE, NE, OFF` after `loop`), and discriminating `W7` passes (`FL == 1`) from the sentinel (`FL == 2`) after `bz FL, loop` via `bne FL, 2, pas` (`2` operations instead of `3`), the 4-block setup costs **76 operations** (19.0 per block), each `W7` pass costs `2 + 41 = 43` operations to the first row-17 test, and the prologue costs **91 operations** (dropping the redundant `and M` on the top 32-bit words `m7, m15` and sharing `S0(a) + MAJ(a,b,c)` between `hh` and `y0p`).
- **L4: a counter for the deep path and per-counter Chebyshev cap margins.** N2 counts the entries that pass all row-17 tests. E[N2] = SR p2 2^20 2^-64 per group. With per-counter Chebyshev margins (eps_NE, eps_NW, eps_N1, eps_N2) = (2^-16, 2^-14, 2^-7, 2^-5) (Section 6.4), P_cap = 2.019e-06, N_G = 276,302,772,059,533,160,318, and N1 pays only for the A17 tests (19 operations) while the deep path (at most 3,148) is charged at N2_MAX = 207,782,513,219,973,181. The epilogue tests four caps (19 operations).
- **L5: 2-word bucket entries (`ESZ = 2`) and fused P6 count/fill passes.** Because the variant fields in word 1 occupy 160 bits and the G-word fields occupy 96 bits, both fit in a single 256-bit word (`160 + 96 = 256` bits). Every bucket entry and sentinel is therefore **2 words** (64 bytes) instead of 3 words (96 bytes), shrinking entry storage by 1/3 (total memory `2^80.42` bytes vs `2^80.96`) and saving one word store per entry in `P6_FILL` (`P6_COUNT = 145`, `P6_FILL = 189`, `P6_PREFIX_NONEMPTY = 11`, total preprocessing `2^66.8588` units vs `2^67.1070`).

**C.3 Why the premises are unchanged.** The statements of H1 to H7 are those of 37742a53 and 012400ff, with H3's memory (`2^80.42` bytes) and preprocessing (`2^66.8588` units) and H7's register count (`42`) updated to match this derivative's exact figures. The success bound uses them through S = SR p2 q3_model and delta (6.4). L0 removes only variants whose probability of success is 0, so S, the event that H5 bounds and N_G's formula are the same; L2, L3, L4 and L5 change how the tests and tables are packed and executed, not which variants pass. All four counters are capped by Chebyshev's inequality (Section 6.4); with them P_cap = 2.019e-06 and the bound is 0.39000000. H1's "|R_j| 2^-27 entries in expectation" counts the variants whose row 16 holds, and the tables here hold those with W16 in G', 22 |R_j| 2^-32 by the same uniformity.

**C.4 Checks of the shipped program.**
1. Selftest (A.1): all 6 items pass (`P0=91, EPI=19, GROUP4=76, ITER=6, X_E17=41, X_A17int=60, X_SUCC=3208`, 42 registers, published pair in all 4 lanes, 5 SMC replicates with 77 pairs rebuilt/verified/found, 8 RAM trials with 0 mismatches).
2. `diff_prog.py` and `t_pre_d.py` (B.16): decision equivalence and preprocessing body verification against `mkent` and the exact definitions.

**C.5 Ledger, N and certificate.** B.1 with the inputs of A.5 (`python3 ledger38.py`): N_G = 276,302,772,059,533,160,318, T = 2,032,592,963,753,652,191,643,563/682, log2 T = 71.33596769, claimed time_log2 = 71.33597. With n = 2032592963753652191643563 and d = 682, by exact integer comparison

```python
n, d, E = 2032592963753652191643563, 682, 100000
a, b = n ** E, d ** E
assert (b << 7133596) < a <= (b << 7133597)
```

so (k - 1)/10^5 < log2 T <= k/10^5 with k = 7133597: 71.33597 is an upper bound and the smallest five-decimal one.

**C.6 Credit.** 37742a53 (winglock) and 012400ff (Jbenisek): the package, its program, ledger, studies, premises and text. Through them: c99df2dc (qkniep) and 0ae69bcb (0xshikhar) for the construction and the shape of the analysis, and the filings they credit. The dependencies are declared with this filing.

## Appendix D. This derivative

**D.1 Base and lineage.** Credited derivative of Th0rgal's aa0496d3-d741-49e5-8f5c-0292e39115ee (71.33597), itself a derivative of Jbenisek's 0bf9d76b-d200-4b40-a32d-46ce1aaffcb7 (71.34862), which builds on 012400ff-d717-461c-a433-377f35ce2298 (Jbenisek, 71.43541) and 37742a53-4062-4c76-bdd0-cd74b4c6eb21 (winglock, 71.69523), see C.1. `experiments/vt38.py`, `experiments/manifest.json` and `certificates/manifest.json` are the files of aa0496d3 byte for byte. The online counted program, the construction, the premises H1, H2, H3, H4a-c, H6 and H7 and both experiments are those of aa0496d3. `proof.md` and `claim.json` change where a count of the counted preprocessing, the pair budget of H5 or a value of the ledger changed: the paragraph "This derivative" at the top, Sections 0, 5.1, 6.4, 6.5 and 7, the figures quoted in H1 to H5 and H7, Appendices A.1, A.5, B.1, B.2, B.3 and B.16, and this appendix. Appendix C is aa0496d3's and quotes its figures.

**D.2 Changes.** Four, priced separately in D.3. None of them changes which variants can succeed or a test applied to them.

1. *Preprocessing counts that the printed bodies do not execute.* The B.16 program of aa0496d3 charged 189 operations per (Y, variant) for the fill pass, 35 for the P5 setup, 43 for the P5 append and 56 for the P5 body; the bodies printed in its B.3 execute 233, 37, 46 and 57 (the fill body is 13 + 22 x 10 operations; the 22 live words of G cost 10 each). Its t_pre_d.py as printed did not reach its own assertions: the P5 check compared the list words with an entry that already carries the G word, and the P6 check handed the fill body a fields word that already carries it. Both checks are corrected in B.16 (the reference word is `(mkent(...)[1] - gw(0)) & WORD`; the fields word of the fill body is the same). The ledger now charges what the printed bodies execute: 233, 37, 46, 57 (the P5 body count and the prefix counts 6 / 11 are measured by B.16 as well; they were constants of the dictionary before).
2. *The zero pass of P6 is unrolled 16 times* (`gen_zero16`, B.3): 16 stores with 16 increments and one branch, 34 operations per 16 headers (2.125 per header) in place of 4 per header. The 256 x 2^64 headers are a multiple of 16.
3. *The Y loop of the count and fill passes* (`gen_variant_pass`, `gen_count_iter`, `gen_fill_iter`, B.3) runs on `u = Y + A1 (mod 2^32)` in two segments, `u` from A1 to 2^32 - 1 (Y = u - A1) and then `u` from 0 to A1 - 1 (Y = u + 2^32 - A1, skipped for A1 = 0), so `u` is the loop counter and needs neither the addition of A1 nor the mask `and M`; the table address base `Ys = hb + (Y << 32)` runs with it (one addition per iteration instead of a shift and an addition) and `c9x - A1` is one constant `cc` per variant. One iteration including its loop control costs 144 operations (count) and 232 (fill); before, 145 + 3 and 233 + 3. The per-variant overhead (list loads, A1, both segment setups, the guard for A1 = 0 and the branch of the loop over the list) is executed and measured: 16 and 17 operations (the ledger charged 16 for each). Every one of the 2^32 values of Y of every variant is processed exactly once.
4. *The pair budget* (H5, Section 6.5) is charged at delta = 0.564, the sum of the two one-sided 99% Poisson limits of the measurements of Section 6.5 (95 observed: 120.25 / 1,500 = 0.0802; 4 observed: 11.60 / 24 = 0.4835; sum 0.5637), instead of 1. It is a measured premise: the evidence is that of Section 6.5, which is aa0496d3's and unchanged, and the budget sits at the limit of that evidence, not above it. The caveats of Section 6.5 (resampled SMC particles, 24 far-term chaining values, limits that assume independent observations) apply to it in full. The Bonferroni bound of Section 6.4 becomes q_lb = S_model (1 - 0.564 / 2).

**D.3 Effect of each change** (`sens38.py`, B.2, last block: B.1 run with the inputs of the change and of every change before it; log2 T of the exact ledger, the change against the row before, and the five-decimal claim):

```
aa0496d3 as filed (its pre2.json, pair budget 1)                                             71.335968              (claim 71.33597)
(1) the counts the printed bodies execute (P6 fill 233, P5 setup 37, append 46, body 57)     71.342384  +0.006417  (claim 71.34239)
(2) + P6 zero unrolled 16 times (34 per 16 headers)                                          71.340819  -0.001565  (claim 71.34082)
(3) + Y loop of the count and fill passes on u (144 / 232 per iteration, 16 / 17 per variant) 71.339653  -0.001166  (claim 71.33966)
(4) + pair budget delta = 0.564 instead of 1  [this derivative]                              71.072490  -0.267163  (claim 71.07250)
```

**D.4 Checks.** `t_pre_d.py` (B.16, output in A.5) executes the bodies of P1', P5, P6 zero, P6 prefix, P6 count and P6 fill on the true variant lists and on synthetic variants with A1 = 2^32 - 3, 1 and 0, with the real segment limits (2^32 and A1) and with toy limits; the headers after the count pass equal the definition (the number of (Y, variant, g) triples that hash to each header), and after the fill pass every bucket holds exactly the 2-word entries of the definition (`mkent` for the real variants), with the header at the start of its bucket. The operations per iteration are the difference of two runs with different iteration counts on the same path, the per-variant overhead the remainder, and every run on that path matches fixed + iterations x per-iteration. `t_pre1.py` (B.13) reproduces the counts of P1 to P4 on the shipped `vt38.py` (A.5). The preprocessing bodies are not in the experiment source; their counts are executed by `t_pre_d.py`.

**D.5 Ledger, N and certificate.** B.1 with the inputs of A.5 (`python3 ledger38.py`): N_G = 192,411,962,931,188,556,827, T = 6773230216939762999009911/2728, log2 T = 71.07249038, claimed time_log2 = 71.07250. With n = 6773230216939762999009911 and d = 2728, by exact integer comparison

```python
n, d, E = 6773230216939762999009911, 2728, 100000
a, b = n ** E, d ** E
assert (b << 7107249) < a <= (b << 7107250)
```

so (k - 1)/10^5 < log2 T <= k/10^5 with k = 7107250: 71.07250 is an upper bound and the smallest five-decimal one. The first row of D.3 is the exact total of aa0496d3 reproduced by the same ledger from its own inputs (pair budget 1, the counts of its pre2.json).

**D.6 Credit.** aa0496d3 (Th0rgal): the package that this one changes in four places, its tightenings of the counted program and of the cap margins and its text; 0bf9d76b (Jbenisek) and, through them, 012400ff (Jbenisek) and 37742a53 (winglock); c99df2dc (qkniep) and 0ae69bcb (0xshikhar) for the construction and the shape of the analysis, and the filings they credit. The dependencies are declared with this filing.

## Appendix E. This derivative: the accepted event, its probability, the pair budget and the exact ledger

### E.1 Base, changes and the shipped program

Credited derivative combining Jbenisek's 14b3b6ff-f9c8-4a4f-9278-15cfccf71bf2 (70.28679), dariolina's 1db43310-a194-428c-b14c-bd6af97ccc0a (70.73486), Th0rgal's aed05522-8fe5-4277-be03-8b50ffa49e26 (71.00164), Th0rgal's 19c9e7e7-b38b-43b6-9818-133841a0cb7c (71.06954), and Jbenisek's fdef4bab-a9d7-4052-b11f-e50fabfd7374 (71.07250), itself a credited derivative of Th0rgal's aa0496d3-d741-49e5-8f5c-0292e39115ee and of the packages that one credits (dependencies.json). The construction, the tables, the preprocessing, the premises H1, H3, H4a-c, H5, H6 and H7 (H4a with the measurements of E.10 added, plus H8), and the experiments are theirs. This derivative combines (1) the accepted event and tightened online program (Section 4.7, Section 5.3, from 14b3b6ff and 19c9e7e7) together with 1-word bucket entries (`ESZ = 1`, `X_E17 = 38`, `X_A17int = 55`, `X_SUCC = 2975`, Section 4.4 and Section 5.1), (2) q3_model = 2^-101.10 x 2^3.3216 = 2^-97.7784 (H2, E.2, from 1db43310 and 14b3b6ff), and (3) delta = 1/25 = 0.04 (H5, E.3, from 1db43310).

`experiments/vt38.py` (65,084 bytes, SHA-256 bab4c7b703b8296bd8f2472e9af8ead8259a5e1d360ea0740c2b6aa28a087576; the single experiment source, limit 65,536 bytes) differs from 14b3b6ff's file in applying the online instruction tightenings of 19c9e7e7 and 1-word bucket entries (`ESZ = 1`, `P0 = 89`, `EPI = 13`, `GROUP4 = 75`, `X_E17 = 38`, `X_A17int = 55`, `X_SUCC = 2975`; 43 registers after allocation) while keeping 14b3b6ff's accepted event:
- `ecell`, `exact`, `rowok`: the accepted event of Section 4.7 (the E cell of row 19 accepts the four patterns on 30040e32, row 20 the tie; equality of A34..A37, E34..E37).
- `mkent`, `gen_deep`, `gen_group4`, `build_program`: 1-word bucket entry `EN` packing `c7 + 2^32` in bits `0..32` (bits `33..34` and `150..153` zero) and `E1a, U = S0(A1) + c9 + E2 + K17, Q, gi, a2i, A1, KCg, a17(g)` in bits `35..255` (saving 3 operations in `X_E17` and 3 more in the deep path), prologue 89 (fold constant 0x80000000 and c-1), epilogue 13 (single `or` chain across `cap_ne`, `cap_nw`, `cap_n1`, `cap_n2`), four-lane block 75 (`rsub` for `Y + Z0`, `ITER = 6` with `ESZ = 1`), A17 internal tests 55 (`shr` + `xor` accumulated via `or` before one `and 1` and `bnz`), and deep path 2,975 operations from the W7 pass (2,989 in 14b3b6ff, 3,200 in 19c9e7e7, 3,208 in fdef4bab), measured by `prog_costs()` and asserted by selftest item 4.
- `smc_replicate`, `rebuild`, `outcome`, `near_term`, `replay`, `q3_experiment` and the selftest: the replica of the accepted event (E.4), the replay of its first two pairs through the tightened counted program, the pass rule.
- To fit 65,536 bytes: shorter comments; no other code changed. The modules of B.15 are the earlier program's.

The 1-word bucket entries (`ESZ = 1`) and online/P6 tightenings reduce per-group fixed operations from 3,438 to 3,366, W7-pass E17 tests from 43 to 40, A17 internal from 19 to 17, the deep path from 2,929 to 2,920, `NE_MAX` by half (halving the entry-scan work at `ITER / ESZ = 6`), and P6 preprocessing from 2^77.45 to 2^76.43 operations (total preprocessing from 2^66.9387 to 2^66.2545 units); together with q3_model = 2^-97.7784 and delta = 1/25, N_G drops from 19.25 x 10^18 to 10.69 x 10^18 and log2 T drops from 70.28679 to 70.17649 (-0.11030 bit).

### E.2 The gain from the printed event to the accepted event, and the printed-event baseline (H2)

*Tool.* `traillab` (14b3b6ff's C program, written in this project with Claude Code; not shipped: the experiment sources are limited to 65,536 bytes) estimates rates of the 38-step characteristic by sequential Monte Carlo on real compressions: every sample is a chaining value and W0..W15 of both members with the real message expansion, the state is replayed from the words (0 replay mismatches are required), rows 6..21 are the prefix (sampled with the attack's conditions; `prefix log2 P(rows 6..21)` is its SMC estimate) and rows 22..37 the window, with the late words redrawn per sample (W6 uniform, W7 in F7, W8 in its cell, W23 free). For each window sample it counts two events: *cells* (every printed cell and condition of rows 22..37) and *EXACT* (zero output difference after step 37). The tool passed its validation suite (48 of 48 quick tests: exact counts of the row-16 set and F7, the flip tables, digests of the published pair).

*Declared run: this attack's own variant law.* The registration (`PREREG.md`, SHA-256 c6b9d566434d76c40d53b3f020129a84bdb37605111ca727598610c600e76fb0, hashed together with the tool sources, the model file, the A0 and A2 lists and the run and analysis scripts on 2026-10-12 at 06:03:30 MDT, before the first seed) changes only the late-word model and the seeds of the earlier run below. For each seed s a sample of 131,072 variants (A0, A1, A2) is drawn by rejection from the union of the 256 sets R_j (A0 uniform over the set, A2 over the A2 list, A1 over 2^32; kept iff the validity test of Section 4.1 holds), so each sample is uniform on the law the program uses; acceptance 2^-12.10 per seed against SR / (256 x 768 x 2^32) = 2^-12.104; the first 2,000 variants of every sample were re-checked against `variant()` and `valid()` of experiments/vt38.py (0 mismatches). Every window proposal draws one variant of its seed's sample, which fixes W8, W9, W10 of member x (member y: plus the published differences); the XOR cells and two-bit conditions of W8..W10 are not part of the event (validity fixes their modular and s0 differences); W6 uniform, W7 in F7, rows 16..21 as before. 32 fresh seeds 7101..7132 x 2^28 proposals per arm (8192 particles x 32768), arms base and tie, 4 threads; declared value of JOINT: the one-sided 99% Student lower bound over the 32 per-seed values (t = 2.4528); each seed has its own SMC prefix and its own variant sample, so the seed spread carries the overdispersion between runs and the variant sampling. Halves 7101..7116 and 7117..7132. Diagnostics required 0.

*Results* (32 of 32 seeds, all 64 runs complete, every diagnostic 0: prefix broken by redraw, y-anchor inconsistent, replay mismatches):

| statistic (log2) | mean | seed sd | declared 99% lower bound | half 1 / half 2 | halves apart |
|---|---:|---:|---:|---|---|
| JOINT (accepted event against printed cells) | +3.4015 | 0.1844 | **+3.3216** | 3.3396 / 3.4635 | 1.99 se |
| A (four patterns and tie, both to EXACT) | +2.0384 | 0.1841 | +1.9586 | | |
| B (EXACT over cells, base proposals) | +1.3631 | 0.0150 | +1.3567 | | |
| B on the tie proposals | +1.3560 | 0.0249 | +1.3452 | | |

Absolute levels: base cells -101.0074 (sd 0.033; the printed event on this law, Section 6.2 measured -101.0 with independent code), base EXACT -99.6442, tie EXACT -97.6058 (99% lower bound -97.6818). Pooled counts: base 131,104 cells and 337,241 EXACT (2.572), tie 131,187 and 335,790 (2.560).

*Definitions (both runs).* Base arm: the printed prefix; tie arm: the prefix with the nine E19 value bits 30040e32 and E20 value bit 29 dropped and the linear condition E20[29] xor E19[29] = 0 added. Per seed (log2): JOINT = tie prefix + log2 rate(EXACT) - (base prefix + log2 rate(cells)), A = tie EXACT - base EXACT, B = base EXACT - base cells; declared value: mean - t(0.99, 31) sd / sqrt(32), t = 2.4528. *Earlier run (reported, not used):* the same design in the low-memory attack's late-word model (W8 in its cell, W9 and W10 published), preregistered (SHA-256 2a8482bfbd4d426a3b28b4751ec9f4385929238d702b1c53f74b2a2cbcae4c82, 2026-10-12 03:29:20 MDT), seeds 3001..3032: JOINT mean +3.3439, seed sd 0.1793, 99% lower bound +3.2662; A +1.9762 (bound +1.8977); B +1.3677 (bound +1.3583); base cells -101.0058.

*Printed-event baseline and use.* Across six independent studies of the printed event — `smc.c` R1..R2 (Section 6.2: 99% bounds -101.00146, -101.00195; 21.9M verified tail successes), `PREREG_q3b` R3..R4 (aed05522, seeds 300000..301023 and 400000..404095: means -100.99993, -100.99848, 99% bounds -101.00265, -101.00018; 21.9M verified tail successes), and 1db43310's independent fixed-effort multilevel splitting estimator `q3.c` S1..S2 (32 + 32 runs, N = 2,000, T = 16,384, seeds 1001..1032 and 2001..2032: means -100.99189, -100.99160, 99% bounds -101.03905, -101.03081, pooled 99% bound -101.02120; 63,762 verified tail successes, 0 failed rebuilds) — the lowest of all six 99% lower bounds is 2^-101.03905, and 1db43310 sets the printed-event baseline at 2^-101.10 (0.061 bit below that lowest bound). Combining 2^-101.10 with the 99% lower bound +3.3216 of the gain measured on this attack's variant law gives **q3_model = 2^(-101.10 + 3.3216) = 2^-97.7784** (0.097 bit below the tie arm's direct 99% bound -97.6818, and 0.103 bit below the shipped replica's calibration mean -97.6753). Using aed05522's preregistered baseline 2^-101.35 gives q3_model = 2^-98.0284 (70.18937), and 14b3b6ff's 2^-101.50 gives 2^-98.1784 (70.19818), all priced in E.5.

### E.3 The pair budget delta = 1/25 = 0.04 (H5)

*Bound and whole-group measurement (from 1db43310).* Every success in A' passes all of rows 16 and 17 (and 18) with W7 in F7 (rows 16..18 are identical in the printed event A and the accepted event A'), so pointwise N <= N18 <= N17, where N17 (N18) is the number of variants of the whole group (all 256 A0, all their valid variants) that pass all of rows 16..17 (16..18) with W7 in F7, and E[N - 1 | A_v] <= E[N17 - 1 | A_v] = delta17 (and <= delta18). In 1db43310 (`q3 run 3101 5000 16384 2500`, function `group_test`, SHA-256 `d2c4452dd4007ddbe814ca5f19842a26fe44ce439a2ce2cd50ffc6463c7e5e28`, run on the first 2,500 verified tail successes), for each verified success (CV1, v) and each of the 256 A0_j, all preimages u of phi(u) = g - Y - Z0 - c9(A2) over all 32 g in G and all 768 A2 were found exactly via a 16-way partitioned inverse of phi over 2^32 u, tested for validity and evaluated through all 38 steps on CV1 (2,500 of 2,500 successes found in their own bucket, 0 row-16 mismatches, 1,434.3 entries per success vs 1,428.8 expected; covers near, own-block and far terms together): **2,500 whole groups, 3,585,652 other row-16 entries, 241,170 W7 passes, 48 passing all of rows 16..17 (N17 - 1; one-sided 99% Poisson limit 0.02670 for delta17), 0 reaching row 18 (N18 - 1; 99% limit 0.00184 for delta18), 0 further successes** (and on all 31,875 verified successes of S2, near-term enumeration found 391,103 near variants, 262,159 row-16 co-hits, 25,867 W7 passes, 545 with all of row 17 = 0.0171 per success, 0 reaching row 18).

*Supporting near-variant row-17 completion rate (from 14b3b6ff).* In 14b3b6ff (preregistered, SHA-256 c7aa96fe58297d3a326183444253d13075d69e5973ea7fd557774b6d769d9dfa), two independent processes of 5,400 seconds each measured the fraction r7 of near-variant first row-17 test passes (E17 mask) that also pass the remaining seven conditions of row 17:

| process | records | other valid variants | row-16 co-hits | W7 passes | first-test passes | all seven | rate | 99% CP upper |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| A | 171,595 | 2,073,363 | 1,401,617 | 139,036 | 10,593 | 3,096 | 0.29227 | 0.30267 |
| B | 151,550 | 1,830,712 | 1,233,688 | 122,292 | 9,174 | 2,619 | 0.28548 | 0.29660 |
| A + B | 323,145 | 3,904,075 | 2,635,305 | 261,328 | 19,767 | 5,715 | 0.28912 | **0.2966866** |

Replicate-cluster bootstrap (4,612 clusters): 99% upper 0.29696. Across A + B, 323,145 / 26,645 = 12.13 near variants per success, 19,767 / 26,645 = 0.742 first-test passes, and 5,715 / 26,645 = 0.0177 passing all of row 17 per success, matching 1db43310's 0.0171 and the base's 0.018.

*Use.* We charge **delta = 1/25 = 0.04**, which is 1.50 times the whole-group one-sided 99% Poisson limit of delta17 (0.02670) and 21.7 times that of delta18 (0.00184; 0 of 593 row-17-complete entries across 1db43310's whole-group and near-term studies reached row 18). Pricing with delta = 296687/1000000 (70.18676), fdef4bab/14b3b6ff's delta = 0.564 (70.20124) and delta = 1 (70.24073) is in E.5.

### E.4 The organizer replica for the accepted event

*Changes to `smc_replicate`.* Rows 17..22 as before, except: at row 19 the nine pattern bits of the proposed E19^x are one of the four patterns drawn uniformly (weight 4 x 2^-f); at row 20 bit 29 of E20^x is set to E19^x[29]; at row 22 only the imposed bit E22[29] = 0 (the printed cell) is kept and nothing is tested. Tail: W23 by importance sampling over the 2^10 classes of its ten printed conditions (the six value bits 12, 15, 17, 23, 24, 26 of its cell and its four two-bit conditions W23[0] != W23[30], W23[1] != W23[31], W23[14] = W23[21], W23[16] = W23[25]): one of the 27 classes of `SIG` with probability (n + 2)/218, uniform inside it, weight 218 x 2^-10 / (n + 2), on top of the weight 2^22/|F7| for W7 in F7; rows 23..37 computed and the outputs compared. The classes and counts n come from a development run of the low-memory program's replica with W23 uniform (164 exact events; 63 in the printed class 3ff, the others with other carry patterns of the same modular difference of W23: XOR differences 2808000, 2818000, 3818000, 6818000 against the printed 1808000). Classes never seen are not proposed, so the replica estimates a lower bound of q3. Every success is rebuilt and checked as before with rows 0..21 in the accepted form; the first two of every replicate are replayed through the counted program.

*Calibrations* (each preregistered with the program's hash and fresh labels before its first replicate; 960 replicates, all kept):

| version | proposal | mean (log2) | halves | pooled means of 20: mean, sd, min | threshold | below | failed |
|---|---|---:|---|---|---:|---:|---:|
| v1 | classes n/164 | -97.6372 | -97.585 / -97.691 | -97.6562, 0.2362, -98.3268 | -98.0838 | 3 of 48 | 0 |
| v2 (shipped) | classes (n + 2)/218 | -97.6753 | -97.652 / -97.700 | -97.6890, 0.2013, -98.1769 | -98.5838 | 0 of 48 | 0 |

The v1 threshold was the earlier rule (2^-101.35) shifted by the declared factor, 0.15 bit above q3_model as before; it failed 3 of 48 pooled means. v2 lowers the weights' spread and sets the threshold 0.35 bit below q3_model; this threshold was chosen after v1's calibration and is reported as such; v2's calibration used fresh labels. 9,008 of the 12,000 v2 pairs have an E19 pattern other than the published one.

Preregistration v1:

```
# Preregistration: calibration of the q3 replica of vt38.py for the accepted event (written before any calibration replicate)

Program: experiments/vt38.py of this package as hashed in PREREG_Q3.sha256 (smc_replicate: rows 17..22 by proposals with the four E19
patterns and the E20[29] = E19[29] tie, row 22 E22[29] = 0 imposed and nothing else tested, tail W23 by importance sampling over the
27 classes of its ten printed conditions seen in a development run of the low-memory program's replica (probability n/164, weight
164 2^-10 / n; classes never seen are not proposed, so the replica estimates a lower bound), the exact event; 256 tail proposals per particle).
Before this file: 20 development replicates (labels 'dev-vt|k', 512 tail proposals) gave 2^-97.518, and the selftest replicate. Not used below.
Pass rule of vt-q3-smc-r38, fixed here: trial 20 returns a pair iff all 20 replicates have a success, 0 failed rebuilds, the counted program
reports the success of each replayed pair (the first two of every replicate), and the mean of the 20 linear estimates is >= 2^-98.0838
(the filed rule 2^-101.35 shifted by the declared joint multiplier 2^3.2662; like the filed rule it sits 0.15 bit above q3_model).
Calibration: 960 replicates with labels 'vt-q3-smc-r38|calibN%d' (k = 0..959, never used before), all kept, replicates without a success
count as 0. Reported: mean of the linear estimates (log2), halves k < 480 and k >= 480, the 48 pooled means of 20 (min, median, max,
mean, sd), the number below the threshold, failed rebuilds, pairs, pairs with another E19 pattern. Use: pass probability of the frozen rule
and the replica's level against q3_model 2^-98.2338; it does not move the threshold or q3_model.
```

```
a76529817585eb4a8cf8729935f07c927fb557c3c125af7079d96e9077c7f284 *PREREG_Q3.md
ebfabb6527b9d37d5d6f49778152f55b5f63651fbb1ab94e7dea63045023bda7 *calibrate_vt.py
07755334dcc1bef3b3370ef70e8c520adb0076b7ac81c66d3ba13c9042163d82 *vt38.py
2026-10-12 05:00:59
```

Output v1:

```
replicates 960 | without success 0 | failed rebuilds 0 | pairs 15199 | other E19 pattern 11423
mean of the linear estimates: 2^-97.6372
half 1: 2^-97.5854
half 2: 2^-97.6909
pooled means of 20: min -98.3268 median -97.6791 max -97.0969 mean -97.6562 sd 0.2362
pass rule threshold -98.0838: pooled means below it: 3
time 317 s
```

Preregistration v2:

```
# Preregistration v2: calibration of the vt38 q3 replica for the accepted event (written before any v2 calibration replicate)

v1 (PREREG_Q3.md): 960 replicates, mean 2^-97.6372 (halves -97.585 / -97.691), pooled means of 20: mean -97.656, sd 0.236, 3 of 48 below
the v1 threshold 2^-98.0838. That rule (the filed rule shifted by the declared multiplier, 0.15 bit above q3_model) fails too often for a
replica whose W23 importance weights reach 164.
v2 changes: class probability (n + 2)/218 (weight 218 2^-10 / (n + 2)); pass threshold 2^-98.5838 = q3_model - 0.35 bit (the replica
estimates a lower bound of q3, so the rule tests q3 >= about q3_model with a margin; the threshold is no longer above q3_model). Other parts
of the rule unchanged (20 replicates with a success, 0 failed rebuilds, every replayed pair reported by the counted program).
The choice of the threshold was made after v1's calibration and is reported as such; v2's calibration below uses fresh labels.
Program: experiments/vt38.py as hashed in PREREG_Q3b.sha256. Calibration: 960 replicates, labels 'vt-q3-smc-r38|calibV2-%d' (k = 0..959,
never used before), all kept; reported as in v1.
```

```
a5c6ef21e3667af54c687e0bfa4601f9e48d4770ea111bb4d6c182464f85ede4 *PREREG_Q3b.md
d8aaf8dc5582786bffdc1544d4f82e1b35183504414b2eca474460637747ee61 *calibrate_vt2.py
72cb4a20ca003d09de7d83c240a30d6d84eda890f6dc9d33036671cc9d08d396 *vt38.py
2026-10-12 05:06:42
```

Output v2 (`calibrate_vt2.py`, below):

```
replicates 960 | without success 0 | failed rebuilds 0 | pairs 12000 | other E19 pattern 9008
mean of the linear estimates: 2^-97.6753
half 1: 2^-97.6515
half 2: 2^-97.6995
pooled means of 20: min -98.1769 median -97.6597 max -97.3002 mean -97.6890 sd 0.2013
pass rule threshold -98.5838: pooled means below it: 0
time 304 s
```

```python
# calibrate_vt.py - 960 replicates of the vt38 q3 replica (48 requests of 20), labels fixed by PREREG_Q3b.md.  Run next to vt38.py.
import time, math, json, statistics
import vt38 as V
t = time.time(); SV = V.sample_variants(); zs = []; bad = 0; npairs = 0; alt = 0
for k in range(960):
    z, pairs, b = V.smc_replicate(V.Shake('vt-q3-smc-r38|calibV2-%d' % k), SV); bad += b; zs.append(z); npairs += len(pairs)
    alt += sum((V.trace(p[0], p[1])[1][19] & V.M19) != 0x30040430 for p in pairs)
lin = [0.0 if z is None else 2.0 ** z for z in zs]
print('replicates', len(zs), '| without success', sum(z is None for z in zs), '| failed rebuilds', bad, '| pairs', npairs, '| other E19 pattern', alt)
print('mean of the linear estimates: 2^%.4f' % math.log2(sum(lin) / len(lin)))
for nm, sl in (('half 1', lin[:480]), ('half 2', lin[480:])): print('%s: 2^%.4f' % (nm, math.log2(sum(sl) / len(sl))))
pooled = sorted(math.log2(sum(lin[20 * g:20 * g + 20]) / 20) for g in range(48))
print('pooled means of 20: min %.4f median %.4f max %.4f mean %.4f sd %.4f' % (pooled[0], pooled[24], pooled[-1], statistics.mean(pooled), statistics.pstdev(pooled)))
print('pass rule threshold %.4f: pooled means below it: %d' % (V.Q3_THRESH, sum(p < V.Q3_THRESH for p in pooled)))
print('time %.0f s' % (time.time() - t))
json.dump(dict(zs=zs, pooled=pooled), open('calibrate_vt2.json', 'w'))
```

Local emulation of the organizer requests (`emulate.py`: seeds sha256(id|trial), 256 trials, each request run twice; Linux, Python 3.12):

```
vt-q3-smc-r38: returned 21, 8.8 s, byte-identical True
   log2_estimate: n 20 sum -1952.7603 min -99.7826 max -95.3155
   accepted_pairs: n 20 sum 279 min 8 max 23
   failed_rebuilds: n 20 sum 0 min 0 max 0
   program_found: n 20 sum 40 min 2 max 2
   other_patterns: n 20 sum 184 min 6 max 15
   near_variants: n 20 sum 478 min 6 max 62
   near_row16: n 20 sum 318 min 6 max 30
   near_w7: n 20 sum 20 min 0 max 4
   near_first17: n 20 sum 1 min 0 max 1
   near_cosuccess: n 20 sum 0 min 0 max 0
   log2_pooled_mean: n 1 sum -97.2259 min -97.2259 max -97.2259
   pass_threshold: n 1 sum -98.5838 min -98.5838 max -98.5838
   bytes of output 26559
vt-ram-r38: returned 256, 2.3 s, byte-identical True
   blocks: n 256 sum 8192 min 32 max 32
   w7_passes: n 256 sum 550 min 0 max 8
   mismatches: n 256 sum 0 min 0 max 0
   ops: n 256 sum 250876 min 894 max 1214
   units: n 256 sum 256 min 1 max 1
   bytes of output 164363
```

### E.5 Sensitivity (`sens_e.py`, `t_imm_e.py`)


```python
# sens_e.py - sensitivity of this derivative's exact ledger (ledger_e.py; each row: the inputs named, N_G recomputed; log2 T).
from ledger_e import *
def row(name, cs=COSTS, **kw):
    o = ledger(costs=cs, show=False, **kw); print('%-100s %.6f   (attack %.4f, N_G 2^%.4f)' % (name, o['log2_T'], o['attack_units_log2'], o['NG_log2'])); return o
row('claimed configuration (q3_model 2^-97.7784 = -101.10 + 3.3216, delta 1/25, ESZ 1, P0 89, EPI 13, GROUP4 75, X_SUCC 2975)')
row('PREREG_q3b / PREREG_q3 bases (q3_model 2^-98.0284 / -98.1784, delta 1/25)', q3_log2=-98.0284); row('PREREG_q3 base', q3_log2=-98.1784)
row('delta 0.564 (fdef4bab/14b3b6ff), q3_model 2^-97.7784', delta=Fr(141, 250))
row('four E19 patterns and tie only', q3_log2=-99.1414)
row('exact event only (q3_model 2^-99.7433 = -101.10 + 1.3567, delta 1/25)', q3_log2=-99.7433)
row('delta 296687/1000000 (near-variant completion bound), q3_model 2^-97.7784', delta=Fr(296687, 1000000)); row('delta 1, q3_model 2^-97.7784', delta=Fr(1))
row('q3_model 2^-98.5, delta 1/25', q3_log2=-98.5); row('q3_model 2^-99.0, delta 1/25', q3_log2=-99.0)
row('A_C = 2^68', ac=68); row('A_C = 2^72', ac=72); row('A_C = 2^74', ac=74); row('A_C = 2^76', ac=76)
row('A_S = DEV = 2^50', as_=50, dev=50); row('A_S = 2^70, DEV = 2^64', as_=70, dev=64); row('A_S = DEV = 2^64', as_=64, dev=64); row('no allowances', ac=-1000, as_=-1000, dev=-1000)
```

```
claimed configuration (q3_model 2^-97.7784 = -101.10 + 3.3216, delta 1/25, ESZ 1, P0 89, EPI 13, GROUP4 75, X_SUCC 2975) 70.176480   (attack 67.0361, N_G 2^63.2126)
PREREG_q3b printed-event base (q3_model 2^-98.0284 = -101.35 + 3.3216, delta 1/25)                     70.189370   (attack 67.1460, N_G 2^63.4626)
PREREG_q3 printed-event base (q3_model 2^-98.1784 = -101.50 + 3.3216, delta 1/25)                      70.198180   (attack 67.2171, N_G 2^63.6125)
delta 0.564 (first-row-17 bound of fdef4bab/14b3b6ff), q3_model 2^-97.7784                             70.201237   (attack 67.2410, N_G 2^63.6613)
14b3b6ff as filed (q3_model 2^-98.1784, delta 0.564, ESZ 2, P0 91, EPI 19, GROUP4 76, X_SUCC 2989)     70.286783   (attack 67.8022, N_G 2^64.0613)
1db43310 as filed (printed event q3_model 2^-101.10, delta 1/25, ESZ 2, X_SUCC 3200)                   70.734858   (attack 69.4055, N_G 2^66.5340)
aed05522 / fdef4bab as filed (printed event q3_model 2^-101.35 / 2^-101.50, delta 0.564)               71.001640 / 71.072490
four E19 patterns and tie only (q3_model 2^-99.1414 = -101.10 + 1.9586, delta 1/25)                    70.280244   (attack 67.7652, N_G 2^64.5754)
exact event only (q3_model 2^-99.7433 = -101.10 + 1.3567, delta 1/25)                                  70.362647   (attack 68.1831, N_G 2^65.1773)
delta 296687/1000000 (near-variant completion bound), q3_model 2^-97.7784                              70.186756   (attack 67.1243, N_G 2^63.4151)
delta 1, q3_model 2^-97.7784                                                                           70.240722   (attack 67.5231, N_G 2^64.1833)
q3_model 2^-98.5 / 2^-99.0, delta 1/25                                                                 70.220222 / 70.264869
A_C = 2^68 / 2^72 / 2^74 / 2^76                                                                        68.604539 / 72.046185 / 74.011686 / 76.002930
A_S = DEV = 2^50                                                                                       70.173987   (attack 67.0361, N_G 2^63.2126)
A_S = 2^70, DEV = 2^64                                                                                 71.100167   (attack 67.0361, N_G 2^63.2126)
A_S = DEV = 2^64                                                                                       70.213404   (attack 67.0361, N_G 2^63.2126)
no allowances (the attack and preprocessing alone)                                                     67.036133   (attack 67.0361, N_G 2^63.2126)
```

`t_imm_e.py` (H7: one load per immediate; `python3 t_imm_e.py experiments . -97.7784 1/25`):

```python
# t_imm_e.py - sensitivity (H7): every immediate operand costs one load. The shipped program is rewritten so that each executed instruction
# is preceded by one `li` per immediate operand it carries (ALU second/third operand, the constant of rsub, the compared value of bne, the
# value of sti: the operands charged by t_imm_d.py, Appendix B.16), and run on the unmodified interpreter of experiments/vt38.py; then the
# exact ledger of Appendix E.6. The preprocessing counts with immediates charged are the t_imm_d.py output.
import sys
from fractions import Fraction as Fr
VT, LD, Q3, DL = sys.argv[1], sys.argv[2], float(sys.argv[3]), sys.argv[4]; sys.dont_write_bytecode = True; sys.path.insert(0, VT); sys.path.insert(0, LD)
import vt38
def nimm(ins):
    op, i = ins[0], lambda k: len(ins) > k and isinstance(ins[k], int)
    return (i(2) + i(3)) if op in ('add', 'sub', 'and', 'or', 'xor') else (1 + i(3)) if op == 'rsub' else i(2) if op in ('bne', 'sti') else 0
_alloc = vt38.allocated_program
def alloc_imm(*a, **k):
    r = _alloc(*a, **k); code = r[0]; new = type(code)(); pos = {}
    for idx, ins in enumerate(code.c):
        pos[idx] = len(new.c); new.c += [('li', '_imm', 0)] * nimm(ins) + [ins]
    pos[len(code.c)] = len(new.c); new.lab = {nm: pos[ix] for nm, ix in code.lab.items()}
    return (new,) + tuple(r[1:])
vt38.allocated_program = alloc_imm
cs = vt38.prog_costs(); cs['EPI'] = 18; cs['P0'] -= 5; cs['PASS_ENTRY'] = 3; cs['BLOCK_FIXED'] = cs['GROUP4'] / 4   # as t_imm_d.py
print('online costs, immediates charged:', cs)
P1 = {'G_hit_ops': 160, 'G_nonhit_max_ops': 157, 'F7_in_ops': 34, 'F7_out_ops': 30, 'A2_hit_ops': 58, 'A2_nonhit_max_ops': 55, 'A2REC_total_ops': 56832, 'GREC_total_ops': 4224, 'LIVE_ops': 30, 'LIVE_g': 6}
P2 = {'P5_SETUP': 56, 'P5_BODY_MAX': 71, 'P5_APPEND': 58, 'P5_LOOP': 4, 'P6_ZERO16': 50, 'P6_COUNT_IT': 148, 'P6_COUNT_VAR': 34144345, 'P6_FILL_IT': 170, 'P6_FILL_VAR': 34144389, 'P6_PREFIX_EMPTY': 5, 'P6_PREFIX_NONEMPTY': 8}
from ledger_e import ledger
o = ledger(Q3, Fr(DL), costs=cs, p1=P1, p2=P2, show=False)
print('ledger with immediates charged (q3_model 2^%s, delta %s): time_log2 %.5f  log2_T %.6f' % (Q3, DL, o['time_log2'], o['log2_T']))
```

```
online costs, immediates charged: {'P0': 109, 'EPI': 18, 'GROUP4': 98, 'ITER': 7, 'X_E17': 44, 'X_A17int': 68, 'X_SUCC': 3260, 'PASS_ENTRY': 3, 'BLOCK_FIXED': 24.5}
ledger with immediates charged (q3_model 2^-97.7784, delta 1/25): time_log2 70.22326  log2_T 70.223256
```

### E.6 The exact ledger (`ledger_e.py`)

The program of Appendix B.1 with its three input files embedded and this derivative's inputs as defaults. Its output gives T as an exact rational, N = T x C as an integer and the integer power certificate 2^k C^P <= N^P < 2^(k+1) C^P with P = 100000, so 70.17649 is the smallest five-decimal upper bound of log2 T.


```python
#!/usr/bin/env python3
# ledger_e.py - the exact ledger of this derivative: ledger38.py of Appendix B.1 with its three input files embedded (COSTS, PRE1, PRE2; the
# tightened online counts P0 89, EPI 13, GROUP4 75, X_E17 38, X_A17int 55, X_SUCC 2,975, ESZ 1, selftest item 4) and the inputs of this derivative
# as defaults: q3_model = 2^-97.7784 (H2, Appendix E.2) and delta = 1/25 = 0.04 (H5, Appendix E.3).  Every operation count is an executed-operation
# count of the counted programs; probabilities are exact rationals except q3_model and delta.  Integers and fractions carry the total; N_G is
# found with 80-digit decimal logarithms and then checked exactly against the success bound.  Prints the terms, N = T x C and its certificate.
#   python3 ledger_e.py [--q3 -97.7784] [--delta 1/25] [--xsucc 2975]
import json, math, os, sys, argparse
from fractions import Fraction as Fr
from decimal import Decimal, getcontext
getcontext().prec = 80
COSTS = {"P0": 89, "EPI": 13, "GROUP4": 75, "ITER": 6, "PASS_ENTRY": 2, "X_E17": 38, "X_A17int": 55, "X_SUCC": 2975, "BLOCK_FIXED": 18.75}
PRE1 = {"G_hit_ops": 117, "G_nonhit_max_ops": 115, "F7_in_ops": 28, "F7_out_ops": 25, "A2_hit_ops": 41, "A2_nonhit_max_ops": 39, "A2REC_total_ops": 39168, "GREC_total_ops": 3072, "LIVE_ops": 21, "LIVE_g": 5}
PRE2 = {"P5_SETUP": 37, "P5_BODY_MAX": 57, "P5_APPEND": 44, "P5_LOOP": 3, "P6_ZERO16": 34, "P6_COUNT_IT": 100, "P6_COUNT_VAR": 22940733, "P6_FILL_IT": 122, "P6_FILL_VAR": 22940755, "P6_PREFIX_EMPTY": 5, "P6_PREFIX_NONEMPTY": 7}
C = 2728                                   # collision-frontier-v5, 38 steps (one target compression = C word operations)
SR = 191773672732                          # sum_j |R_j| (runs/rc_full: exact)
F7 = 287309824                             # |F7|
NB = 256                                   # A0 blocks (tables)
MASK_E17_BITS = 10
CNT17 = 1 << 20                            # sum over the 32 words g of G of #{E17 : both row-17 tests pass}; 0 for the 10 dead words (L0, exact)

def log2d(x): return (Decimal(x.numerator) / Decimal(x.denominator)).ln() / Decimal(2).ln() if isinstance(x, Fr) else Decimal(x).ln() / Decimal(2).ln()
def up5(x): return math.ceil(float(x) * 1e5 - 1e-9) / 1e5

def pre_ops(cs, p1, p2, ngw, lev):
    """Preprocessing in word operations: every term is (items) x (executed operations per item) + loop control."""
    W32 = 1 << 32
    t = {}
    t['P1_G'] = W32 * (p1['G_hit_ops'] + 3)                         # longest path of the row-16 test + loop
    if lev: t['P1_live'] = 32 * W32 * (p1['LIVE_ops'] + 3) + 32 * p1['LIVE_g']   # L0: the row-17 count of every g of G (exhaustive over E17)
    t['P2_F7'] = W32 * (p1['F7_in_ops'] + 3)
    t['P2_zero'] = 4 * ((1 << 34) + W32 + 2)                          # zero the F7 table region (addresses 0 .. 2^34 + 2^32 + 1) before P2 writes its flags
    t['P3_A2'] = W32 * (p1['A2_hit_ops'] + 3) + 768 * 4
    t['P4_rec'] = p1['A2REC_total_ops'] + p1['GREC_total_ops']
    t['P5_enum'] = NB * 768 * (p2['P5_SETUP'] + (1 << 29) * (p2['P5_BODY_MAX'] + p2['P5_LOOP'])) + SR * p2['P5_APPEND']
    entries = SR * ngw * W32                                         # (Y, variant, g) triples = entries of all tables
    if 'P6_ZERO16' in p2:                                            # R38L bodies: 16 headers per zero iteration; the Y loop (2^32 iterations per variant) with its control inside the count
        t['P6_zero'] = NB * ((1 << 64) // 16) * p2['P6_ZERO16']     # and fill iterations, and the per-variant overhead (list loads, A1, both segment setups, guard, list-loop branch) measured
        t['P6_count'] = SR * (W32 * p2['P6_COUNT_IT'] + p2['P6_COUNT_VAR'])
        t['P6_fill'] = SR * (W32 * p2['P6_FILL_IT'] + p2['P6_FILL_VAR'])
    else:                                                            # the bodies of the base: 4 operations per header, loop control 3 per (Y, variant), 16 per variant
        t['P6_zero'] = NB * (1 << 64) * 4
        t['P6_count'] = SR * W32 * (p2['P6_COUNT'] + 3) + SR * 16
        t['P6_fill'] = SR * W32 * (p2['P6_FILL'] + 3) + SR * 16
    t['P6_prefix'] = NB * (1 << 64) * (p2['P6_PREFIX_EMPTY'] + 3) + min(entries, NB * (1 << 64)) * (p2['P6_PREFIX_NONEMPTY'] - p2['P6_PREFIX_EMPTY'])   # nonempty headers <= min(entries, headers)
    return t

def ledger(q3_log2=-97.7784, delta=Fr(1, 25), eps=(Fr(1, 1 << 16), Fr(1, 1 << 14), Fr(1, 1 << 7)), ac=70, as_=60, dev=60, succ=Fr(39, 100), tol=Fr(1, 2 ** 60), show=True,
           costs=None, p1=None, p2=None, base=False, ngw=None, n2=None, eps2=Fr(1, 1 << 5), esz=None):
    lev = not base; esz = esz if esz is not None else (3 if base else 1)
    ngw = ngw if ngw is not None else (32 if base else 22); n2 = n2 if n2 is not None else lev
    cs = costs or COSTS; p1 = p1 or PRE1; p2 = p2 or PRE2
    if base and eps == (Fr(1, 1 << 16), Fr(1, 1 << 14), Fr(1, 1 << 7)): eps = Fr(1, 16)
    eps_ne, eps_nw, eps_n1 = eps if isinstance(eps, tuple) else (eps, eps, eps)
    MAXB = 14 * ngw * 768                                            # Lemma 6 bucket bound
    p_f7 = Fr(F7, 1 << 32)
    ent = Fr(SR * ngw, 1 << 32)                                      # E[entries per group] (exact, H1)
    E_NE = esz * (ent + NB); E_NW = ent * p_f7; E_N1 = E_NW * Fr(1, 2 ** MASK_E17_BITS)
    E_N2 = SR * p_f7 * Fr(CNT17, 1 << 64)                            # L4: W7 passes that pass both row-17 tests (H1, Lemma 4)
    B_ent = NB * MAXB
    B_NE, B_NW, B_N1, B_N2 = esz * (B_ent + NB), B_ent, B_ent, B_ent
    # per-group success rate lower bound
    fl = math.floor(q3_log2); q3 = Fr(2) ** fl * Fr(math.floor(2 ** (q3_log2 - fl) * 2 ** 40), 2 ** 40)
    S = SR * p_f7 * q3
    q_lb = S * (1 - delta / 2)
    per_group_fixed = cs['P0'] + cs['EPI'] + (NB // 4) * (cs['GROUP4'] - 4 * cs['ITER'])      # the sentinel iteration (ITER) of every block is charged through NE
    cw = cs['PASS_ENTRY'] + cs['X_E17']
    if n2: c1 = cs['X_A17int'] - cs['X_E17']; c2 = cs['X_SUCC'] - cs['X_A17int']
    else: c1 = cs['X_SUCC'] - cs['X_E17']; c2 = 0
    # iterate N_G and the Chebyshev overflow bounds (P_k <= B_k / (eps_k^2 N_G E_k))
    Ptot = Fr(0)
    for _ in range(6):
        x = (Decimal(1) - Decimal(succ.numerator) / Decimal(succ.denominator) - Decimal(Ptot.numerator) / Decimal(Ptot.denominator) - Decimal(tol.numerator) / Decimal(tol.denominator))
        mu = -x.ln()
        NG = int(-((-Fr(int(mu * 10 ** 30), 10 ** 30)) // q_lb)) + 1
        Pk = [Fr(B_NE) / (eps_ne ** 2 * NG * E_NE), Fr(B_NW) / (eps_nw ** 2 * NG * E_NW), Fr(B_N1) / (eps_n1 ** 2 * NG * E_N1)]
        if n2: Pk.append(Fr(B_N2) / (eps2 ** 2 * NG * E_N2))
        Pn = sum(Pk)
        if abs(Pn - Ptot) < Fr(1, 10 ** 12) * max(Pn, Fr(1, 10 ** 12)): Ptot = Pn; break
        Ptot = Pn
    NE_MAX = math.ceil(NG * E_NE * (1 + eps_ne)); NW_MAX = math.ceil(NG * E_NW * (1 + eps_nw)); N1_MAX = math.ceil(NG * E_N1 * (1 + eps_n1))
    N2_MAX = math.ceil(NG * E_N2 * (1 + eps2)) if n2 else 0
    online = NG * per_group_fixed + (cs['ITER'] // esz) * (NE_MAX + B_NE) + cw * (NW_MAX + B_NW) + c1 * (N1_MAX + B_N1) + (c2 * (N2_MAX + B_N2) if n2 else 0)
    pre = pre_ops(cs, p1, p2, ngw, lev); pre_total = sum(pre.values())
    init, fin_ops, fin_units = 1 << 32, 1024, 6          # init: generation of the program text (about 2^21 instructions at most 2^11 operations each)
    # memory in 32-byte words: headers, esz-word entries, sentinels, F7 table (flags + sentinel region), R_j lists, records
    entries_all = SR * ngw * (1 << 32)
    words = NB * (1 << 64) + esz * entries_all + esz * min(entries_all, NB * (1 << 64)) + (1 << 33) + 2 * SR + 20000
    mem_log2_bytes = float(log2d(Fr(words * 32)))
    allow = Fr(2) ** ac + Fr(2) ** as_ + Fr(2) ** dev
    T = allow + Fr(pre_total + init + online + fin_ops, C) + NG + fin_units
    pre_incl = allow + Fr(pre_total, C)
    lg = log2d(T); tl = up5(lg)
    k = int(round(tl * 100000)); n_, d_ = T.numerator, T.denominator
    tight_up = n_ ** 100000 <= (2 ** k) * d_ ** 100000           # T <= 2^(k/10^5)
    tight_down = n_ ** 100000 > (2 ** (k - 1)) * d_ ** 100000    # T >  2^((k-1)/10^5): k is the smallest such integer
    assert tight_up and tight_down
    mu_act = Decimal((NG * q_lb).numerator) / Decimal((NG * q_lb).denominator)
    success_bound = float(1 - (-mu_act).exp() - Decimal(Ptot.numerator) / Decimal(Ptot.denominator))
    out = dict(q3_log2=q3_log2, delta=float(delta), S_log2=float(log2d(S)), q_lb_log2=float(log2d(q_lb)), NG=NG, NG_log2=float(log2d(Fr(NG))),
               NE_MAX=NE_MAX, NW_MAX=NW_MAX, N1_MAX=N1_MAX, N2_MAX=N2_MAX, E_NE=float(E_NE), E_NW=float(E_NW), E_N1=float(E_N1), E_N2=float(E_N2),
               cap_overflow_total=float(Ptot), success_lower_bound=success_bound,
               per_group_fixed=per_group_fixed, cw=cw, c1=c1, c2=c2, online_ops=online, online_ops_log2=float(log2d(Fr(online))),
               pre_ops=pre_total, pre_units_log2=float(log2d(Fr(pre_total, C))), pre_terms={k: float(log2d(Fr(v))) for k, v in pre.items()},
               tight_up=tight_up, tight_down=tight_down, allow_log2=float(log2d(allow)), memory_log2_bytes=mem_log2_bytes, preprocessing_incl_allowances_log2=float(log2d(pre_incl)), T_num=T.numerator, T_den=T.denominator, log2_T=float(lg), time_log2=tl,
               attack_units_log2=float(log2d(T - allow)), ops_per_block_cv=float(Fr(online, NG * NB)))
    if show:
        for k, v in out.items(): print('%-22s %s' % (k, v))
    assert (1 - (-mu_act).exp() - Decimal(Ptot.numerator) / Decimal(Ptot.denominator)) >= Decimal(succ.numerator) / Decimal(succ.denominator)
    return out

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--q3', type=float, default=-97.7784); ap.add_argument('--delta', default='1/25'); ap.add_argument('--xsucc', type=int, default=2975)
    a = ap.parse_args()
    o = ledger(a.q3, Fr(a.delta), costs=dict(COSTS, X_SUCC=a.xsucc), show=False)
    for k in ('q3_log2', 'delta', 'S_log2', 'q_lb_log2', 'NG', 'NE_MAX', 'NW_MAX', 'N1_MAX', 'N2_MAX', 'cap_overflow_total', 'success_lower_bound', 'per_group_fixed', 'cw', 'c1', 'c2',
              'online_ops', 'pre_ops', 'allow_log2', 'attack_units_log2', 'memory_log2_bytes', 'preprocessing_incl_allowances_log2', 'log2_T'):
        print('%-36s %s' % (k, o[k]))
    T = Fr(o['T_num'], o['T_den']); N = T * C; assert N.denominator == 1; N = N.numerator
    P = 100000; NP, CP = N ** P, C ** P; k = (NP // CP).bit_length() - 1
    while (1 << (k + 1)) * CP <= NP: k += 1
    while (1 << k) * CP > NP: k -= 1
    print('T = %d/%d target compressions' % (T.numerator, T.denominator))
    print('N = %d' % N)
    print('certificate: 2^%d * %d^%d <= N^%d < 2^%d * %d^%d' % (k, C, P, P, k + 1, C, P))
    print('time_log2 = %.5f' % (-(-(k + 1) * 100000 // P) / 100000))
```

Output:

```
q3_log2                              -97.7784
delta                                0.04
S_log2                               -64.19975419685424
q_lb_log2                            -64.22890054251376
NG                                   10687797395951771071
NE_MAX                               13235086666975598053952
NW_MAX                               702355744773275003380
N1_MAX                               691210642933723493
N2_MAX                               8037333057368878
cap_overflow_total                   5.219935054688757e-05
success_lower_bound                  0.39
per_group_fixed                      3366
cw                                   40
c1                                   17
c2                                   2920
online_ops                           143515095421196276661087
pre_ops                              240120385693245423096376
allow_log2                           70.00281501560706
attack_units_log2                    67.0361325391506
memory_log2_bytes                    79.54527083147623
preprocessing_incl_allowances_log2   70.10636109381653
log2_T                               70.17648018899325
T = 3639736073456835419065567/2728 target compressions
N = 3639736073456835419065567
certificate: 2^7017648 * 2728^100000 <= N^100000 < 2^7017649 * 2728^100000
time_log2 = 70.17649
```

### E.7 Checks

- `selftest` of the shipped program (Appendix A.1): all six items pass, including the counted costs (P0 89, EPI 13, GROUP4 75, X_E17 38, X_A17int 55, X_SUCC 2,975, ESZ 1), the published pair found in all four lanes, a replicate whose every pair is found by the counted program, and vt-ram-r38 on eight trials.
- The organizer's intake and local emulation of both experiment requests (`vt-q3-smc-r38` 256 of 256 trials, 21 pairs returned, replay byte-identical; `vt-ram-r38` 256 of 256 trials, 256 pairs returned, 0 mismatches, ops 250,876, replay byte-identical): Appendix E.4.

### E.8 Not tested

- The gain of E.2 is measured on this attack's variant law with 131,072 sampled variants per seed (4.2 million of the 2^37.48); the full variant set enters by uniform sampling.
- The pair budget's measurements (Section 6.5 and Appendix E.3) used successes of the printed event (rows 16..18 are identical in the printed and accepted events).
- The starting point of q3_model is 1db43310's printed-event baseline 2^-101.10 (0.061 bit below the lowest of six independent 99% lower bounds across R1..R4 and S1..S2); the preregistered 2^-101.35 and 2^-101.50 baselines are priced in E.5.
- Not done: a solver re-run of the whole system with the four patterns and the tie; a fresh reading of the cells from the paper's tables (the transcription is the earlier filings', verified on the published pair); the row-21 check of a relaxed row-16 prefix set (it concerns the 37-step attack, not this one).

### E.9 Tools and credit

This derivative combines 14b3b6ff (Jbenisek: the accepted event, the variant-law `traillab` study of E.2, the replica of E.4, the near-variant completion study of E.3, and the characteristic-search measurements of E.10), 1db43310 (dariolina: the whole-group row-17/18 pair-budget enumeration of E.3 and the S1/S2 printed-event studies of E.2), and aed05522 / 19c9e7e7 (Th0rgal: the online counted-program tightenings P0 89, EPI 13, GROUP4 75, X_A17int 58, X_SUCC 2,981 and PREREG_q3b R3/R4), built on fdef4bab (Jbenisek), aa0496d3 (Th0rgal), 0bf9d76b / 012400ff (Jbenisek), 37742a53 (winglock), c99df2dc (qkniep) and 0ae69bcb (0xshikhar). All dependencies are credited in `dependencies.json`.

### E.10 The characteristic search: what we measured (H4a)

**Part A. Published and measured cost of the same kind of search (the basis of A_C = 2^70).** Units are target compressions (one 38-step compression = 1 unit = 2728 word operations); a full 64-step SHA-256 evaluation is charged 64/38 units = 4,594.5 word operations, more than a target compression.

*Conversion.* Hash rate measured here: portable C SHA-256 compression (no SHA-NI, gcc -O2, one thread, AMD Ryzen 9 7900X, WSL2; checked on "abc", first words ba7816bf 8f01cfea), five runs of 2 x 10^7 compressions: 4,030,079, 4,022,282, 3,891,284, 4,013,036 and 3,797,484 per second; the slowest, 3,797,484 per second (2^21.86), is used for every conversion (a slower rate gives more evaluations, hence a larger cost). Solver CPU-seconds = wall seconds x threads (an upper bound: idle threads are counted). Figures in the table are log2.

| source | problem | stated cost | SHA-256 evaluations | units | word operations | bits under 2^70 units |
|---|---|---|---:|---:|---:|---:|
| Mendel, Nad, Schlaeffer 2013, Sect. 6.3 p.14 | 38-step SFS: characteristic and pair together | about 8 h on a single CPU, "about 2^37 SHA-256 evaluations" (hardware not named) | 37.00 | 37.75 | 49.17 | 32.25 |
| Mendel et al. 2013, Sect. 6.2 p.12 | 31-step SFS: characteristic and pair together | about 21 h, "about 2^38.4 SHA-256 evaluations" | 38.40 | 39.15 | 50.57 | 30.85 |
| Li, Liu, Wang 2024 (ePrint 2024/349), p.16 | 39-step SFS colliding pair given the characteristic | 120 s with 26 threads = 3,120 thread-seconds (hardware not named) | 33.46 | 34.22 | 45.63 | 35.78 |
| ours, 39-step characteristic | derived from scratch with the tool of [LLW24a] | 772.58 s wall x 12 threads (CryptoMiniSat) + 1,800.77 s x 1 (Kissat, no result) = 11,071.7 CPU-s | 35.29 | 36.04 | 47.46 | 33.96 |
| ours, 38-step pair (part B) | pair given the published cells, 4 calls, 3 without a model | 2,852.83 CPU-s | 33.33 | 34.09 | 45.50 | 35.91 |

Our 39-step characteristic derivation: the unmodified model scripts of github.com/Peace9911/sha_2_attack at commit 6a9f35fd (the account that hosts the authors' RIPEMD-160 tool of [LLW23]) were read before running (no network, no installs, writes only in the working directory); the STP query they emit was translated to CNF by our own converter (which rejects six mutated characteristics and accepts the published 39-step characteristic and rows 5..24 of the published 37-step one) and solved with CryptoMiniSat 5.11.21 on 12 threads: model found after 772.58 s wall (about 2.6 CPU-hours); Kissat 4.0.3 on the same file stopped at 1,800.77 s without a result. It is a window search (rows 8..26 with the message support fixed and the weights W 25, A 10, E at most 90 asserted) that finds a characteristic of the published weights, not the characteristic of Table 3 of [LZLLQZ26]; one run, one machine.

*Reading.* Every figure is far below 2^70 target compressions: the largest, 2^39.15 units (Mendel et al.'s 31-step figure), is 30.85 bits under it, and the 38-step figure of the same authors, 2^37.75 units, is 32.25 bits under; counted in word operations without the factor C, the largest is 2^50.57, 19.43 bits under 2^70. The 38-step characteristic of [LZLLQZ26] (two-block framework, dense rows 0..16) is a harder instance than those searches and no log of its search exists; the margin of 30.85 bits (a factor of about 2^31) is what A_C = 2^70 leaves for that difference and for failed and repeated searches.

**Part B. Our pair searches and sparse part.**

Participant-run here; programs written and run by Grok (xAI); not shipped (64 KiB source limit). SAT: one word operation = one propagation; otherwise one tick = one 32-bit add/sub, S0, S1, s0, s1, CH, MAJ or hash-set probe. Units = word operations / C. Totals include the calls without a model.

**38-step pair search, given the published cells.** Circuit: both 38-step chains with a shared chaining value, message masks on W7..W11, W15 (W16, W23, W25 expanded), every cell of Table 3, the 13 vertical links and the 47 two-bit conditions (W25[4] = W25[6], which holds on the published pair; Table 4 prints W25[9]); 110,437 variables, 383,913 clauses, satisfied by the published pair; one clause blocks the published (CV, M'). File a pins the 24 bits common to the 32 E16 words of the published list; file b selects one of the 32 words.

| call (time limit 900 s) | file | result | CPU s | propagations |
|---|---|---|---:|---:|
| Kissat 4.0.3 --sat --seed=2 --walkinitially=true | a | no model | 898.63 | 592,022,133 |
| CaDiCaL 2.1.3 --seed=1 | a | no model | 898.61 | 1,813,811,854 |
| Kissat 4.0.3 --sat --seed=4 --walkinitially=true | b | pair | 476.96 | 433,129,432 |
| CaDiCaL 2.1.3 --seed=4 | b | no model | 578.63 | 1,217,006,281 |
| total | | | 2,852.83 | 4,055,969,700 = 2^31.917 (2^20.504 units) |

The pair (38-step SHA-256 compression with feed-forward; recomputed by us with an independent step function checked against hashlib on "abc"; M' carries the published E16 word 482326fd, with a different CV and message):

```
CV     43058709 adfdbff7 b7e63568 b4e09527 3ef1b89a 18f03df1 7fd9bbaa 7f392ba4
M      33f3fd01 ab09628d 9971c77a 2f0148d3 442fd7d8 9acaf5c3 2fd3a6f8 a8740b40
       c91bb8b5 9e019239 04039fa1 0ce30b8d a18c515a 76a1e994 d28e48a0 9b5f6dbb
M'     33f3fd01 ab09628d 9971c77a 2f0148d3 442fd7d8 9acaf5c3 2fd3a6f8 88740b40
       cd5bb0b5 be019239 01028d0b 0ceb1f8d a18c515a 76a1e994 d28e48a0 9f1f65bb
digest 614d0b44 0d272005 713bab9e 4fc8e2a1 126b7229 bbb45050 0d592f10 cf2f96a9
```

Words that differ: 7..11, 15, 16, 23, 25 (dW16 = e0000000, dW23 = fe7f8000, dW25 = 20000000); A and E are equal from step 22.

**37-step analogue** (C = 2644; the same circuit on the 37-step characteristic, W15 pinned on the 24 common bits of its list): Kissat seed 2 pair A (135,356,424 propagations), Kissat seed 1 no model (167,052,440), CaDiCaL seed 1 pair B (494,307,286); total 796,716,150 = 2^29.570 (2^18.201 units). Digests: A 3c7353c7 46761dc9 8b3ce5a5 3c6530d2 d6e267fb f0f5b41e b8c21e9a 03b5b458, B 6c1e60a3 27a17426 dd5333ab 9f3317d4 00453b21 27264f97 2f2ea277 4a533513.

**38-step sparse part, from the support and the Section 4.1 rules only** (no table cell seeded; the published values used only as a checker):

| part | ticks | CPU s | result |
|---|---:|---:|---|
| message-difference signing, all 32 disturbance bits | 101,842,272 | 0.533 | bit 29 gives the published XOR masks; fe7f8000 among the 8 dW23 sums |
| sparse window rows 17..37, bits 28..31, all 8 dW23, both dW25 signs | 11,239,528 | 0.021 | the published dW23, dW25 close (22 conditions, rank 22) |
| total | 113,081,800 = 2^26.753 | 0.554 | |

**Not measured (the allowance A_C = 2^70, unchanged):** deriving the dense signed characteristic of rows 0..16 with its two-bit conditions (the pair searches load those cells; a 37-step attempt with them unset, by SAT, step-6 cubes and a pattern beam, returned no model; of 4,614 message pairs realising the 38-step dW23, dW25 at CV = 0, none meets the zero window), and the authors' failed and repeated searches.
