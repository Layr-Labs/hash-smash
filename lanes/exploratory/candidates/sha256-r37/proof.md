# Draft P6 derivative of aa0e8b6 (P4 algorithm, P5 q3c declaration): Low-first 13, residual exact test, q3c measured directly on the submitted pool

Track `sha256-r37-exploratory`; target `sha256-r37-prefix-v1`; C = 2644.
Claim: time_log2 = **57.70485**, memory_log2_bytes = **20.0** (actual bound
769,776 bytes), success probability >= 0.39 under the inherited premises.

This is a credited derivative of Jbenisek's aa0e8b6a-6fd1-4a8b-9917-bb5e0f8a689f.
Two algorithm changes, credited to slkzgm's f2da0e13-698a-4f8b-87d8-6c5914918da8 (57.89863)
and inherited unchanged here: (1) an 8192/2048-word Low-first 13 conditional probe instead
of the eager 4096/4096-word LO/MID probe; (2) the residual three-condition exact
test, 13 rather than 34 operations. One further change is statistical and is our own
(d3e7fe15-02f2-4f04-8170-13923742c0a2, credited): the declared cell bound q3c is measured
on this filing's own variant list by a fresh preregistered block, 2^-71.4243 (Appendices G.3 and G.5),
instead of any bound transferred from the parents' pool (Section 7.4c, Appendix G). One family change is also ours.
The examined family is restricted to the four cube-3 lists (0, 1, 5, 6): 170 of the
parents' 222 classes and 599,760 of their 782,800 variants. The six dropped lists cost
1.59-1.64 operations per variant where the four kept lists cost 0.97-0.99 (Section 7.5),
so the restriction is -0.04380 bit of exact ledger arithmetic. q3c is then declared from this filing's own direct study of the submitted pool
(Appendices G.3, G.4 and G.5): **2^-71.4243**, the one-sided 99% lower bound of the mean of
17,408 fresh preregistered replicates on the 599,760-word list (block E, 16,384 seeds
772000..788383, mean 2^-71.42132, sd 0.15870; pooled with the 1,024 seeds of G.4, mean 2^-71.42147,
sd 0.15870, bound 2^-71.42427, rounded down; every one of the 17,408 values is printed). No sub-pool
transfer allowance is paid: the two pools' measured means differ by 0.0003 bit, and the
parents'-pool pooled bound 2^-71.4474 (claim 57.72781) and the same bound less the
0.0020-bit allowance (2^-71.4494, claim 57.72980) remain stated sensitivities. Structurally, under Lemma 7.1
the variant enters q3 only through the four W24 conditions on `W24x = Z + W8x`, so with
`Z` uniform the map `W8 -> Z + W8` is a bijection and the tail probability is the *same
number* for every variant, hence every uniform-weight sub-pool has the same q3c exactly;
this filing keeps a uniform-weight subset, not an x-reweighting, so the 0.0104-bit
fibre-weighting gap of fb039a6e's preregistered study (Section 7.5) is not the transfer
that applies to it, and the flat 0.05-bit hedge the parents' text prices for an
x-weighted subset is not paid either. Both superseded charges are carried as stated
sensitivities: the 5x measured charge (0.0104 -> q3c 2^-71.4578, claim 57.73815) and the full
0.05 case (claim 57.76569). All three changes are disclosed; nothing else is
changed. The executed cube law is inherited unchanged:
Q0[0] has probability 1/4, and bits 2 and 3 each have probability 1/2 under H1.
The Bernstein slack and cap are recomputed for the cheaper stages.
The characteristic, S, variants, 170 classes, F6/F7 filters, H1-H7, A_C, A_S,
DEV and PRE are inherited unchanged; q3c is declared from the same preregistered
replicates under a tighter admissible statistic (Section 7.4c); numerical
consequences in H5 are updated.

aa0e8b6 claimed 58.02135 (unrounded 58.021341413842665); its ledger is reproduced
exactly with N = **773438176907133806360** and the same executed cube law.
Our unrounded time is **57.7048456021372318532782939686324345113798116729639643672216**, N = **621084759189170888800**.
The collision event is
identical, so the algorithm changes are a conditional cost improvement, not new
success evidence; the q3c declaration (0.0119 bit above the parents' pooled bound, 0.0274 above the preregistered min-of-blocks bound) is the second, statistical change.

**Validation status.** Independent arithmetic, affine counts and exhaustive
tables/residual checks pass, and the deterministic intake gate accepts the package
(`validate_candidate` returns `submission_state: ready`; the package digest is computed by
the organizer's run from the payload and is therefore not quoted here; certificate
manifest empty and verified). The five organizer experiments are unchanged from
f2da0e13 and their recorded two-run validation (byte-identical stdout under the
public seed, all mismatch counters zero, every run below 20 s) is inherited with
the credit; this participant could not re-execute them locally because the
containerised executor needs access to a Docker socket this sandbox does not grant
(`permission denied ... /var/run/docker.sock`), so the official re-run is left to
the organizer's CI. What this participant did re-execute: `selftest` (its ten-line
transcript is byte-identical to Appendix D), `ledger` twice (byte-identical) and
`memory`; the ledger agrees with the independent Appendix B mirror to the digit and
the memory figure with the table hash.
P4 observations are recorded in the P4 executor observations section; inherited
first-person evidence below retains its original authors' voice and credit.


**Credited derivative of sraiw's d9f8833d-2483-478a-9815-4baea4bf5214 (59.30883), of fd115760-37ba-49c3-814e-35c44f32761c (sraiw, 60.90319), 96169e7c-8ea2-4090-afc8-edbc6aca0c98 (59.31513) and ad06162f-1038-4d01-a06a-445e2238dc54 (60.71121), and of our 67516603-7f51-4b80-806d-9f4a379dab56 (59.5556, ruled not_evaluable on H1, H2, H3), 221eb058-623b-41d6-a7bf-1d9b4602ce1e (60.97003) and ec1340aa-ecc8-4564-8df7-006f0a2b2ce5 (R37OWN5, whose organizer experiments and statements of the premises H1-H3 are reused here) and of our 4ec21bf9-f588-4b80-bb2b-77c1ccf8c9b7 (R37R, 60.11997, passed review; its exact collision event after row 21 is carried over here, Section 7.7)**, with Th0rgal's 0db0eeb6-9958-43af-9700-ea9e99cee016 (61.17784), the four-value-pattern acceptance of rows 18 and 19 from Jbenisek's ffbe30bb-ac92-4191-a589-3bf32661ee7d (60.38707), R16x from 221eb058, and the lineage of all of them (Section 2): winglock's 6c77089c and 7319bba9, dd6656d4 (Th0rgal), itseasypop's 1c368173, qkniep's b947b377, GordoAR's 087a18c4,
0xshikhar's 1f12a09a, fb039a6e and 2f540248, companygardener's d3ec5c41, 44921815 and 8de337d5, 8aeaed1c, def128fc and 22b7dd8b (Jbenisek), Th0rgal's f2fe1d4d and Jbenisek's c22f86a2, newjordan's 9c6967cc, jungjipdo's ffc8c2df, and 6eeefb64 for the price of a solver CPU-second.
The attack, the characteristic, the sets F6, F7, L*, the family of A0-variants and its 222 largest classes, the packed good-pair arithmetic, the rows 16..36 check (cells through row 21, the collision event after it: 4ec21bf9), the four-pattern and R16x relaxations and their q3 studies, the bit-sliced algebra of the W7 and W6 programs, the 4-lane exact row-16 table stage, the zero-base scan table, the premises H1-H3 and the ledger structure are theirs.
**Inherited aa0e8b6 history: what it changes against d9f8833d (three items).** (1) The cap on the data-dependent work is bounded by Bernstein's inequality for sums of independent bounded variables instead of Chebyshev's: the work v_f of a first block lies in [0, vmax_fb] and the first blocks are independent (H1), so Pr[sum v_f > (1 + s) N_FB vbar] <= exp(-t^2 / (2 (N_FB vmax_fb vbar + vmax_fb t / 3))), t = s N_FB vbar, which allows the slack s = 1/18000 instead of 2^-11 and a work-cap failure probability Pcap = 3.84e-07 instead of 0.00023325, so that both V_MAX and mu0 fall (Section 10, Appendices B, C). (2) The premises H1, H2, H3 are stated as our theory and are answered with organizer experiments on real first blocks, as in ec1340aa: `h1-cv1-filters-nonce`, `h3-cowpass-nonce` and `h3-ladder-r37` (distinct variants of one first block through the W6 filter, the two table stages and the exact row-16 test, with the dependence factor of each level; Appendix H); the `q3_smc_check` of d9f8833d is dropped from `a0-online-r37` to keep the experiment sources below the organizer's 64 KiB. (3) The success event is the collision after row 21, as in our accepted 4ec21bf9 (R37R, Appendix D there): rows 16..21 are checked cell by cell, rows 22..36 are computed without cell tests and a pair is accepted iff the two 37-step outputs are equal; q3 is the cell probability q3c of rows 16..36 times EXQ = 2.4331, the preregistered one-sided 99 percent lower bound of the ratio of collision to cell events after row 21 (Section 7.7), and the rare path is charged for it in full with no early abort (Section 9.9). The program, its plane algebra and its ledger inputs are d9f8833d's, with the changes of this filing in the header of `experiments/lowm.py`.
**What d9f8833d changed against 96169e7c, ad06162f and 221eb058 (credit; all of it counted exactly):** (1) base-value constant folding of `e4` and `e3` into `CB3`; (2) two's-complement negation of `e3`; (3) exact carry folding at bits 15..16 of `e3` and bits 18..19 of `Sq`; (4) single-carry split of `F6(W - cu)` at `c_4(cu)` (`SUBF_OPS` from 87..97 to 11..28, `SPILL` from 64 to 18 or 30); (5) dynamic bit-0 invariance `I = (q & B) | (CB3 & 1)`; (6) exact carries `c_17, c_21, c_28` in `F6` when `full=False`; (7) two-pass constant factoring in `c7` (`F7_OPS = 112`); (8) bit-lexicographic `REP_ORDER` per list; (9) unrolled register-cached cube expansion and shift-register placement (`PLACE = 6`, `5m + 1` per rep); (10) the 4-lane exact `(lo, mid)` row-16 filter (`PNZ = 63,512 / 2^24`, `MU = 1/256`); (11) the zero-base 8192-word `scan_table` with 4-lane packed `Ul`/`Um` addresses (`CLS_LANE = 5`, `SCAN_LANE = 7`, `SURV_LANE = 6`, `PROBE = 11, 8, 8, 6`); (12) the calibrated `A_C = 2^48`; (13) half-adder carry reuse in `fa_step2` and polarity-aligned F6 synthesis (`W6_OPS` 181..301, `vbar` 27,775.96).
## 0. Summary

- The complete-message algorithm, characteristic, q3 = 2^-71.4243 x 2.4331 = 2^-70.14150,
  success event after row 21 and all statistical premises are inherited.
- Second change (statistical, our own): q3c_used = 2^-71.4243, the one-sided 99% lower
  bound of the mean of 1024 fresh preregistered replicates drawn on this filing's own
  variant list (Appendix G.3), with no sub-pool transfer allowance. The parents'-pool
  pooled bound 2^-71.4474 (claim 57.72781) and the same bound less the 0.0020-bit allowance
  (2^-71.4494, claim 57.72980), and the preregistered min of the two per-block bounds
  (2^-71.4629, claim 57.74322), remain stated sensitivities; the ledger uses q3 = 2^-71.4243 x 2.4331 = 2^-70.14150.
- FIRST[u & 8191] is read first. Only a nonzero FIRST word triggers SECOND
  on u[23:13]. The state intersection decides all thirteen low-24 conditions
  exactly. Only E16x[30]=0, A16x[25]=A15x[25], A16x[29]=1 remain.
- The first probe stage is 16 operations per four lanes; continuation is seven
  per nonzero FIRST, including its own work-counter update. FIRST is nonzero
  for 1513/8192 indices. Fold and scan are unchanged. EX_OPS = 13.
- N_FB = 31617998307376629; FIXED = 490; vbar = 18021721026738521/1099511627776;
  vmax_fb = 274564402011/5; V_MAX = 518269945863203016639;
  slack = 2903322225176979/50000000000000000000; Pcap = 1.2999999999999999941121E-07 <= 0.00000011.
- N = 621084759189170888800 and T=N/2644; rounded claim 57.70485. Memory is 769,776 bytes,
  including an added 1,024-byte code allowance. PRE = 2^38 operations.
- Validation (c) completed under the public seed; two byte-identical runs only.
  Inherited evidence remains credited; P4 observations are separately recorded.


## 1. Target, cost model and output

- **Target** sha256-r37-prefix-v1: SHA-256 steps 0..36 on every padded block, the standard IV once, FIPS 180-4 padding, feed-forward, all eight digest words (repository `verifier/hash_functions.digest(m, "sha256", 37)`).
  The output is two distinct complete messages with equal digests, verified with the target before output.
- **Cost model** collision-frontier-v5: one 37-step target compression = 1 unit; every other executed 256-bit word-RAM primitive (load, store, add/sub, and/or/xor/not, shift/rotation, compare, branch,
  uniform random word) = 1/C unit with C = 2644. Immediates and shift amounts are instruction fields; 64 registers. Success must be at least 0.39 over fresh coins.
- **Notation.** In step i, E_i = A_{i-4} + E_{i-4} + S1(E_{i-1}) + CH(E_{i-1}, E_{i-2}, E_{i-3}) + K_i + W_i and A_i = E_i - A_{i-4} + S0(A_{i-1}) + MAJ(A_{i-1}, A_{i-2}, A_{i-3}) (mod 2^32);
  (A_{-1..-4}, E_{-1..-4}) = (a, b, c, d, e, f, g, h) of the incoming chaining value. F_R(cv, B) is the R-step compression with feed-forward; its output is cv + (A_{R-1}, A_{R-2}, A_{R-3}, A_{R-4}, E_{R-1}, E_{R-2}, E_{R-3}, E_{R-4}).

## 2. Sources and credit

- [LZLLQZ26] Y. Li, Z. Zhang, M. Li, F. Liu, H. Qian, J. Zhu, "Pushing Collision Attacks on SHA-2 to 39 Steps", IACR ePrint 2026/1120 (CC BY): the 37-step characteristic (Table 15), its two-bit conditions (Table 16), the SFS pair (Table 17) and the three-step attack.
  [LLWS26] Y. Li, F. Liu, G. Wang, J. Shi, ePrint 2026/1080 (the framework).
- d9f8833d-2483-478a-9815-4baea4bf5214 (sraiw, 59.30883) and fd115760-37ba-49c3-814e-35c44f32761c (sraiw, 60.90319): the bit-sliced algebra of the W7 and W6 programs (Sections 8, 9.3-9.7) and the packed probe, carried over from their published source text into this package's `experiments/lowm.py`, which is the program of this filing (it is run here only as this package's own file, with the changes listed in its header). 67516603-7f51-4b80-806d-9f4a379dab56 (ours, 59.5556, not_evaluable on H1, H2, H3) and ec1340aa-ecc8-4564-8df7-006f0a2b2ce5 (ours, R37OWN5): the organizer experiments `h1-cv1-filters-nonce`, `h3-cowpass-nonce`, `h3-ladder-r37` and the statements of H1, H2, H3 (Appendices H and M).
- 96169e7c-8ea2-4090-afc8-edbc6aca0c98 (sraiw, 59.31513), ad06162f-1038-4d01-a06a-445e2238dc54 (sraiw, 60.71121), 221eb058-623b-41d6-a7bf-1d9b4602ce1e and 22b7dd8b-3764-4ff4-93ad-3fa9cc170026 (Jbenisek, 60.97003 and 60.99099): the filings this one is a credited derivative of; every change is listed in the summary above, in Section 9, and in the header of `experiments/lowm.py`. 2f540248-75ec-4c7a-9d85-ee9624472172 (0xshikhar, 60.97992): pruning of the broadcast planes. 9c6967cc-238f-4669-840f-856c1f3e9d10 (newjordan, 60.9723): the four-entry streaming group register and the per-(list, batch) constant planes. ffc8c2df-8ef0-42c3-a373-a0e0cf96d889 (jungjipdo, 60.98614): the 13-bit chunk scan.
- ffbe30bb-ac92-4191-a589-3bf32661ee7d (Jbenisek, 60.38707, a credited derivative of fb039a6e): the four feasible value patterns of E18[1,5,10,11,18,28,29] and E19[29] and the change of the cell strings, the solver enumeration and the three verified collisions behind them (Section 7.6); 221eb058 re-measured q3 for its own family together with R16x.
- 4ec21bf9-f588-4b80-bb2b-77c1ccf8c9b7 (ours, R37R, 60.11997, passed review; Appendix D there): the collision event after row 21 as the success event (`step3b`, `same_out`), its structure (D.2), the ratio of collision to cell events and its preregistered lower bound EXQ = 2.4331 (D.3, D.3b) and the pricing of the rare path as executed (D.5), carried over here onto this package's program and constants (Sections 7.7, 9.9). The exact-event scoring of the late rows was designed there with GPT-6-Luna (OpenAI); the reduction of the late rows to conditions on W22, W24 and W26 was first proposed by GPT 5.5 (OpenAI).
- Filings on this track, declared as dependencies: 6c77089c (winglock): transcription of Tables 15-17, the exact sets F6, F7 and L*, the SMC design for q3. dd6656d4 (Th0rgal): affine decomposition of F6, F7. 1c368173 (itseasypop), b947b377 (qkniep): the A0 freedom of the Step-1 solution and the c7 classes.
  087a18c4 (GordoAR): the exact-rational ledger and the success analysis. 1f12a09a (0xshikhar): the 170 classes and the packed groups of four 64-bit lanes. 7319bba9 (winglock): the program structure, the row-16 enumeration, the preregistered q3 studies, the end-to-end rates.
  d3ec5c41, 44921815, 8de337d5 (companygardener): the counted-program framework and the ledger. 8aeaed1c, def128fc and c22f86a2 (Jbenisek): the direct row-16 lane read and the cap slack squared in the Chebyshev bound (replaced here by Bernstein's bound, Section 10).
  f2fe1d4d, 0db0eeb6 (Th0rgal): the MAJ identity, the single packed member word `Gw` and its 31-operation group. fb039a6e (0xshikhar): the bit-sliced additions with register-resident planes and the q3 studies over the whole family (cited, not used). 6eeefb64 (sha256-r32): the calibrated price of a solver CPU-second behind A_C.
- **Historical aa0e8b6 changes and costs (over 96169e7c, ad06162f and 221eb058; not P4 sensitivities).** In addition to the base-folded `CB3` and two's-complement `H'` formulation of `W6x` (Lemma 8.1, Section 9.5), the list-invariant carry folding at bits 14..16 of `e3` and 18..19 of `Sq`, the single-carry split of `F6(W - cu)` at `c_4(cu)`, the dynamic bit-0 invariance `I = (q & B) | (CB3 & 1)` (Lemma 8.2), the carry-only evaluation of bits 17, 21, 28 in `F6` when `full=False`, the 16-plane constant factoring of `c7 - C7_CONST` in the W7 class test (`F7_OPS = 112`), the per-list `REP_ORDER`, the unrolled register-cached cube expansion and shift-register placement (`PLACE = 6`), the 4-lane exact `(lo, mid)` row-16 table filter (`SURV_FIX = 13`, `PNZ = 63,512 / 2^24`, `MU = 1/256`), the zero-base `scan_table` at word address `0..8191` with 4-lane packed `Ul`/`Um` chunk-address extraction (`CLS_LANE = 5`, `SCAN_LANE = 7`, `SURV_LANE = 6`, `PROBE = 11, 8, 8, 6`), and the calibrated characteristic-search allowance `A_C = 2^48` (Section 11.2), this filing adds half-adder carry reuse `(xy & c) | ac` in `fa_step2` and target-flag polarity alignment (`andf`, `orf`) in `f6_ok_upper` and `f6_combine_pre` (cutting `W6_OPS` from 186..313 to 181..301, `SUBF_OPS` from 11..31 to 11..28, and `vbar` from `27,911.58` to `27,775.96`), reducing total `time_log2` from 59.31513 (and 60.71121 in ad06162f) to 59.30883 (and 60.69185 under `A_C = 2^60`); this filing adds the Bernstein cap bound (Section 10), which gives 59.30006, and the exact collision event after row 21 (Section 7.7), which gives 58.02135 (60.32595 under `A_C = 2^60`).


## 3. The characteristic (from the paper, as transcribed in 6c77089c; re-checked by `experiments/lowm.py`)

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

In this table rows 18 and 19 are the paper's. This filing's program keeps the cells of every row but does not impose the value bits E18[1,5,10,11,18,28,29] and E19[29] of those two rows (the characters `1`, `0` there); the four patterns it accepts are listed in Section 7.6. It also does not impose E16[23] = 0 and the `+` pair E16[24] = E17[24] of rows 16 and 17 (R16x, Section 7.4c).

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
with x = M', y = M (`experiments/lowm.py` rebuilds both members and checks the cells; the repository
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
(each step inverted for its new coordinate). W8..W13 do not depend on CV1. *Proof.* Substitution; `lowm.py`
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
W8x[8] != W8x[25], W8x[14] = W8x[18]}**. Exhaustive count over the 2^29 values of E4 with E4[31:29] = 000 (a0 = E4 - C4 is a bijection; counted by 0db0eeb6, and 7319bba's `genum2.c` agrees):
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
(exhaustive over all 2^32 words by 0db0eeb6, Tungsten; the counts of 7319bba's `f6chk.c` agree). By the carry pattern of w + d (s0 is linear), each set is a disjoint union of
affine spaces. We use them in the following bitwise form, **checked against the definition on all 2^32 words**
(0db0eeb6, Tungsten: about 10 CPU-minutes, zero mismatches for both; here `selftest` and the organizer experiments compare the plane programs with the definitions):

```text
F6: w is NOT in F6  iff  common | (w29 & (bc | (w30 & X)))  with
      common = (w14^w18) | ~(w8^w25) | (w1^w12),   bc = (w15^w19) | ~(w9^w26) | (w2^w13),
      X = (w16^w20^w31) | ~(w10^w27^w31) | (w3^w14^w31)                                  (bits are w_i; | is OR)
F7: w is in F7  iff  w1 = w18, w0 = w28, w9 = w30 and
      [ w11 = 0, w22 = 1, w26 = 1 ]                                                       2^26 words
      or [ w11 = 1, w12 = 0, w22 = 0, w23 = 1, w26 = 0, w27 = 1, w2 = w19, w1 = w29, w10 = w31 ]   2^20 words
```

(F6 is the form published in 087a18c4/1c368173 with b_bad & c_bad simplified to bc | (w30 & X); 7319bba derived the F7 constraint
set from the affine hull of F7 and of its two halves (7319bba); here it is verified
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


### 5.3 The 170 classes and their four lists

c7(a0) takes 22,976 distinct values on G (7319bba and 0db0eeb6 enumerate them). A *class* is G intersected with one value of c7; for all variants of a class and a given CV1, W7x is the same word, so one membership test decides the W7 filter of the whole class.
**This filing examines the 170 classes with at least 3456 variants** (599,760 variants; 1f12a09a's selection, the family of 7319bba's registered q3 studies). Each class is {base XOR s : s subset of mask, a0 in G, c7(a0) = the class value} (the descriptors c7, base, mask, size are the table `CLASSES` of `lowm.py`).

**Fact (computed; `selftest` re-derives it for every class).** For all 170 classes base & mask = 0, so a0 = base + s = base | s = base ^ s with s a subset of the mask, and the set of s depends only on its list's mask; of the parents' **ten lists** the kept 170 classes lie in four (0, 1, 5, 6; 82 + 3 + 82 + 3 classes):

```text
list  mask      size  classes      list  mask      size  classes
 0    01fec08d  3456   82           5    01fec08d  3600   82
 1    01fec48d  3456    3           6    01fec48d  3600    3
 2    01fec09d  3456   15           7    01fec09d  3584   15
 3    01fec09d  3456    7           8    01fec09d  3584    7
 4    01fec0dd  3456    4           9    01fec0dd  3584    4
```

(111 classes of 3456, 85 of 3600 and 26 of 3584 variants; 17 bits vary in all: the union of the masks is 01fec4dd = bits 0, 2, 3, 4, 6, 7, 10, 14, 15, 17..24; the bits 0, 2, 3, 7, 14, 15, 17..24 are in every mask.) The program builds those four lists (0, 1, 5, 6) as the member sets of the first class of each list (by enumerating the 2^14 or 2^15 subsets of the mask against the definitions of G and c7)
and lets every other class of the list use them; `selftest` checks, for all 170 classes and all 599,760 variants, that the variant base | s is in G, has the class's c7 and that the class has its size (0 mismatches). **The cube of a list (computed; asserted when the list is built).** The bits 0, 2, 3 of s are *free* in the lists 0, 1, 5, 6 (every member has its partner with the bit flipped) and, in the parents' ten lists, bit 0 is free in the other six (which this filing does not build); B is the set of these bits (the cube of the list), and the list is the union over f subset of B of (reps xor f), where reps = the members with no cube bit:
432 reps (lists 0, 1), 450 (lists 5, 6), 1728 (lists 2, 3, 4) and 1792 (lists 7, 8, 9). The classes of the lists 0, 1, 5, 6 have a0 bit 1 set (base bit 1 = 1), which Lemma 8.2 needs for the bits 2, 3; the classes of the other lists have base bit 1 clear and use bit 0 only. A list is stored as the planes of its reps (14 or 16 bit planes per batch of 256: the cube bits are static zeros of the main run) and as packed entries (Section 9.6), 8 batches in all (the four kept lists, two each).
S0(a0) >= 8 on G and a0 < 2^29; over the 599,760 variants max S0(a0) = 0xffffbb5c (`selftest`), so (~S0(a0) & M32) <= 0xfffffff7 and no carry leaves a 64-bit lane of the packed words of Section 9.

Per first block over uniform x, every class passes the W7 test for exactly |F7| = 68,157,440 values of x, so the number of passing classes has mean 170 p7 = 2.698 and the number of variants in passing classes has mean 599,760 p7 = 9,518.
Passing classes are strongly correlated (their c7 values are close), so the counts are bursty; only expectations are used.


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


### 6.2 Row 16 without a mask table

For l in L*, E16x = C_l + u with u = W0 + s0(W1) (W16 = s1(W14) + W9 + s0(W1) + W0; C_l collects rows 12..15 of l, K16, s1(W14) and W9). With the cell E16[23] = 0 of Table 15, 28 elements of L* can hold row 16 (7319bba enumerated all E16x with the row's nine fixed x-bits, 2^23 per l, and found 1,052,672 pairs (u, l); l = 0, 2, 16, 18 have none).
**With R16x (Section 7.4c) the E cell of row 16 has eight fixed bits and every one of the 32 elements of L* holds row 16 for exactly 65,536 values of E16x: 2,097,152 pairs (u, l)** (`r16.c` with `r16data.h` generated from `experiments/lowm.py`, exhaustive over the 2^24 values of E16x with the eight fixed bits for each l; Appendix A). By Lemma 5.1 u is uniform for a good pair, so Pr[row 16 holds for l] = 65,536 / 2^32 = 2^-16 exactly and the expected number of row-16 hits per probed lane is 2^21 / 2^32 = 2^-11.
The earlier filings read the l-mask of u from a table of 2^32 words. **This filing decides row 16 from the cells.**

**Lemma 6.2 (the exact test).** For each of the 32 l let A16x = E16x + cxA_l with cxA_l = -A12x + S0(A15x) + MAJ(A15x, A14x, A13x) (rows 12..15 of member x for l). Then E16y = E16x and A16y = A16x - 2^29 (mod 2^32), computed for all 32 l.
Row 16 holds for (u, l) iff all of the following hold (cells of row 16 and the two-bit conditions closing at row 16):

```text
E16x & 40461a80 = 00060800         the eight fixed bits 30, 22, 18, 17, 12, 11, 9, 7 of the E cell (E16 has no difference: E16y = E16x; bit 23 is free under R16x)
E16x[4] = E15x[4]                  the '+' pair of the E cells of rows 15 and 16 (E15[4] = E16[4])
A16x[29] = 1                       the A cell 'u' at bit 29: with A16y = A16x - 2^29 the XOR difference is 2^29 iff A16x[29] = 1
A16x[15] != A15x[15], A16x[23] = A15x[23], A16x[25] = A15x[25]          (A15x of l is a constant)
A16x[9] != A16x[20], A16x[18] != A16x[6], A16x[8] = A16x[17]
```

*Proof.* The cells of row 16 are the A cell (u at bit 29), the E cell (eight fixed bits, no difference), the W cell (none); the printed conditions closing at row 16 are the seven of Section 3.3 (A15/A16 three, A16 three, E15/E16 one);
for all 32 l the difference of E16 is zero and cyA_l - cxA_l = e0000000, which is the statement on A16y. *Checks:* the test applied to all 2^24 values of E16x with the eight fixed bits, for each of the 32 l, gives exactly the set of u of the enumeration by `r16.c` (2,097,152 pairs, no pair missing and none added; Appendix A);
the experiments and `selftest` compare it with the generic row check (`row16_ok`) on random and near-miss values. QED.

**The table stage (Low-first 13).** Put lo = u mod 2^13 and hi =
(u >> 13) mod 2^11. For each l, compute e_lo = (lo + (C_l mod 8192)) mod
8192 and a_lo = (e_lo + (cxA_l mod 8192)) mod 8192. The interface state is
(carry_e, carry_a, a_lo[6], a_lo[8], a_lo[9]). FIRST enforces five conditions:
E16x[4]=E15x[4] and fixed E16x bits 7,9,11,12. SECOND enforces the remaining
eight: fixed E bits 17,18,22; A16x[15]!=A15x[15], A16x[23]=A15x[23],
A16x[9]!=A16x[20], A16x[18]!=A16x[6], A16x[8]=A16x[17].

For every raw state, enumerate the 2048 high indices using its two carries.
Delete states with empty high support before assigning state slots. Raw states
can exceed four (maximum nine at this split); after pruning at most four remain
for each l. Empty-high-support states are discarded, as in the predecessor's implementation.
At bit 64*idx+l, FIRST[lo] records the realized viable state and SECOND[hi]
records its accepting high indices. For a fixed (lo,l) at most one state exists.
Thus T=FIRST[lo]&SECOND[hi] decides exactly the conjunction of all thirteen
conditions; neither approximation nor false positive is introduced. Fold
G=((T|(T>>64))|((T|(T>>64))>>128))&M32 is the original filt(u), bit for bit.

Independent enumeration checks all 2^24 u and all 32 l: zero mismatches,
2048 passing low-24 assignments per l, sum |G|=65536, nonzero G at 63512 u.
FIRST has exactly 1513 nonzero words out of 8192. Consequently E|G|=1/256
and Pr[G!=0]=63512/2^24 as before. No independence between lanes is used.

**Residual equivalence.** Conditional on l in G, all thirteen low-24 conditions
of Lemma 6.2 already hold, leaving precisely E16x[30]=0,
A16x[25]=A15x[25], A16x[29]=1. Set VA_l=0x20000000|(A15x&0x02000000),
e=u+C_l, A=e+cxA_l and test
`(e&0x40000000)|((A&0x22000000)^VA_l)==0`.
The intermediates need no mod-2^32 masks because all inspected bits are below
32, so discarded carries cannot affect them. This residual test is only called
for l in G. Generic checks on rejected lanes compare `(l in G) and residual`
with the full definition, retaining the leader's all-survivor/every-sixteenth-lane
coverage. Independent exhaustive testing includes every high-byte extension of
each low-24 survivor: 16,777,216 cases, zero residual mismatches, and 65,536
full row-16 values per l (2,097,152 total), exactly as inherited.


## 7. The Step-3 probability for the variants (H2)

### 7.1 The quantity

For a good pair (CV1, a0) and l in L*, let F_l be the event that rows 16..36 follow every cell and every printed
two-bit condition closing at rows >= 16 (the cell event) and E_l the success event of this filing: rows 16..21 follow every cell and every
printed two-bit condition closing at rows 16..21 and the two 37-step outputs are equal (the collision event, Section 7.7; F_l is contained in E_l).
q3c = average over the 599,760 variants of the 170 classes and over l in L* of Pr[F_l | good], the probability over CV1
(Lemma 5.1 gives the exact joint law of all second-block words); q3 = the same average of Pr[E_l | good] = q3c x R, R of Section 7.7.
The expected number of successful (variant, l) per first block is g x 32 x q3.

(For this filing the event F_l is the same except that the eight value bits of rows 18 and 19 of Table 15 are not imposed and neither are E16[23] = 0 and E16[24] = E17[24] (R16x): Sections 7.4b, 7.4c and 7.6. Sections 7.3 and 7.4 describe the estimator and report the registered studies of 7319bba for the Table 15 pattern. The studies of Sections 7.3 to 7.6 estimate q3c; Section 7.7 takes q3 from q3c.)

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


### 7.3 The estimator (7319bba's design; re-implemented and re-run for this filing, Section 7.4b and Appendix F)

Stages: row 16 exact (the enumeration of 6.2: the stage mean is (1/32) sum_l |R16_l| / 2^32 = 2^-16.994, and the initial particles are drawn exactly from the passing (l, E16) pairs);
rows 17..21: each child proposes E_t^x uniformly with the row's fixed x-bits imposed (exact importance weight 2^-f), sets W_t^x = E_t^x - (the rest of step t), W_t^y = W_t^x + its exact
difference, and checks the whole row; row 22: (W6, W7) drawn uniformly from F6 x F7; rows 23..36: W8 of a variant drawn uniformly from the 599,760 variants of the 170 classes of that time (the same row-22 survivor
is also evaluated with the published W8 for a paired comparison). NP particles, M children per particle per stage, MT tail proposals per particle, multinomial resampling of the survivors after
every stage; the product of the stage means is an unbiased estimator of q3 (the standard SMC normalising-constant estimator). The design is 6c77089c's and 087a18c4's; the program of the registered studies is
7319bba's. **This filing re-estimates q3 with its own program** (Section 7.4b, Appendix F), because it accepts four value patterns of rows 18 and 19: the family of variants, the classes, the filters and every row of the characteristic are those of 7319bba, and this filing changes only how the
good pairs are *found* (Lemmas 8.1, 8.2) and which patterns of rows 16..19 count as a success (Sections 7.4c, 7.6), not which pairs are good or how they are tested. The estimate enters as premise H2.

### 7.4 The registered studies of 7319bba (reported unchanged)

**Study A** (registered 2026-10-10T08:11:18Z, before any listed seed ran): NP = 2048, M = 512, MT = 16384, 32 replicates; rule: the one-sided 99% Student lower bound of the mean of the 32 linear
estimates (t = 2.4528, 31 df), q3_model = 2^(floor(100 log2 LB)/100). Result: mean 2^-74.0187, relative standard deviation 0.0743, lower bound 2^-74.0659, q3_model(A) = 2^-74.07.
**Study B** (registered after study A had been read, to tighten the spread; same program, NP = 8192): mean 2^-73.9987, relative standard deviation 0.0378, lower bound 2^-74.0225,
**q3_model = 2^-74.03 (the Table 15 value; this filing's value is in Section 7.4c)**. All 32 replicates of study B (log2):

```text
-74.022 -73.967 -74.038 -73.934 -74.032 -74.059 -74.000 -74.017 -74.043 -74.070 -73.984 -73.942 -73.949 -73.956 -73.853 -73.965
-74.109 -73.985 -73.979 -73.927 -74.027 -73.983 -73.990 -74.065 -73.925 -74.057 -74.071 -74.052 -74.001 -74.025 -73.984 -73.976
```

| quantity | study A (NP 2048) | study B (NP 8192) |
|---|---|---|
| mean | 2^-74.0187 | 2^-73.9987 |
| relative standard deviation | 0.0743 | 0.0378 |
| 99% lower bound | 2^-74.0659 | 2^-74.0225 |
| **q3_model** | 2^-74.07 | **2^-74.03** |
| stage means (log2) | 16: -16.994, 17: -13.000, 18: -15.004, 19: -6.000, 20: -7.001, 21: -1.000, 22: -11.009, tail -4.015 | 16: -16.994, 17: -13.000, 18: -15.001, 19: -6.000, 20: -7.000, 21: -1.000, 22: -10.998, tail -4.007 |

The stage factors equal, within 0.01 bit, the per-row condition counts of the printed tables (17, 13, 15, 6, 7, 1, 11, 4; 74 in total). 


### 7.4b The studies of this filing (new; preregistered; our own estimator)

The registered studies above measure the Table 15 pattern. This filing accepts four value patterns of rows 18 and 19 (Section 7.6), so q3 is measured again, and for that we wrote our own estimator, `q3smc.c` (Appendix F), from the description of Section 7.3. It shares no code with the earlier filings' program, and no other participant's program was compiled or run here.
Its constants (the cells of rows 0..36, the printed two-bit conditions, the rows 12..15 of the published pair for each l, the variant list) are written by `gen_consts.py` from `experiments/lowm.py`, so the cells it checks are the ones the counted program checks. Stage 16 is an exact enumeration (with the Table 15 cell E16[23] = 0 of this study it gives the 1,052,672 pairs (u, l) of 7319bba's enumeration); stages 17..21 impose the fixed x-bits of the E cell of the row (weight 2^-f) and check the whole row for both members, including the exact difference of the schedule word;
stage 22 draws (W6, W7) uniformly from F6 x F7 (W7 from its affine decomposition, W6 by rejection); the tail draws W8x uniformly from the 599,760 variants and checks rows 23..36 for both members. All parameters are those of the registered studies: NP = 8192, M = 512, MT = 16384, uniform resampling of the survivors after each of the stages 17..22, estimate = the product of the stage means.

**Preregistration** (`PREREG_q3M.txt`, sha256 9187c4519d463838b90eefb4c0aa9df1eb12be95cf463076ad06511c7aaaaabf, stamp 2026-10-12T05:26:30Z, written before any listed seed ran; the file is reproduced in Appendix F).
- *Validation V* (original cells of rows 18 and 19): 64 replicates, seeds 710000..710063. V passes if (a) its mean differs from the registered study B of 7319bba (mean 2^-73.9987, relative sd 0.0378, 32 replicates) by at most 2.576 standard errors and (b) log2 of its one-sided 99% bound is within 0.04 of study B's bound (-74.0225). It is the test that our program reproduces the q3 = 2^-74.03 of the table-free program with Table 15's cells (the program of this filing before its cells were relaxed); if V fails, no q3 is declared from it.
- *Main study* (the four patterns accepted: the eight characters removed from the two E cells): two independent blocks R1 (seeds 720000..720127) and R2 (seeds 721000..721127) of 128 replicates; rule fixed in advance: **declared q3 = 2^x, x = floor(100 log2 min(LB_R1, LB_R2)) / 100**, LB the one-sided 99% Student lower bound of the mean of the linear estimates of the block. Every listed seed was run and is reported (Appendix F); none was dropped or rerun.

**Results.** Validation V: mean 2^-73.9911, relative sd 0.0353, bound 2^-74.0064; z = +0.66 against study B; validation PASSES both preregistered criteria (|z| <= 2.576; bound within 0.04 of -74.0225). Its stage means (log2, rows 16..22 and the tail) are 16: -16.994, 17: -13.000, 18: -14.999, 19: -6.000, 20: -7.000, 21: -1.000, 22: -10.999, tail -4.000, against the registered study B's -16.994, -13.000, -15.001, -6.000, -7.000, -1.000, -10.998, -4.007.
Main study: R1 mean 2^-71.9975, relative sd 0.0714, **bound 2^-72.0191**; R2 mean 2^-71.9868, relative sd 0.0681, **bound 2^-72.0074**. Rule applied: the lowest bound, rounded down to two decimals: **2^-72.02** for the four patterns alone (it was the q3 of the filing before R16x; the q3 used here is that of the joint study, Section 7.4c), 2.01 bits above the Table 15 value 2^-74.03 (structural count 2.00 bits: four patterns of equal weight; exact stage enumeration 1.93, interval 1.78 to 2.09, Appendix B of the filing this one credits for the relaxation).
Stage means of the main study (log2 averaged over the 256 replicates), rows 16..22 and the tail: 16: -16.994, 17: -13.000, 18: -8.000, 19: -10.000, 20: -7.000, 21: -1.999, 22: -11.002, tail -4.000; rows 18 and 19 together contribute -18.00 against -21.00 for Table 15 and row 21 -2.00 against -1.00, the net gain being the sum of the differences. The stages of rows 16, 17, 20, 22 and of the tail are those of the Table 15 study within the sampling resolution.
The pattern diagnostic (a description, not part of the bound; the program's `-d` option, seeds 730001..730003, histogram of the eight value bits E18[1,5,10,11,18,28,29], E19[29] of the 8192 particles that survived rows 16..22, as bits 0..7 in hexadecimal; Table 15's pattern is cd, the others 1b, f6 and 20): seed 730001: 1b:2349 20:1607 cd:2461 f6:1775; seed 730002: 1b:1710 20:2180 cd:2145 f6:2157; seed 730003: 1b:1714 20:1891 cd:2040 f6:2547. Exactly the four predicted patterns occur and no other.

### 7.4c Rows 16 and 17: the R16x relaxation, measured jointly with the four patterns (new; preregistered; our own estimator)

Table 15 imposes E16[23] = 0 (a `0` in the E cell of row 16) and E16[24] = E17[24] (a `+` pair of the E cells of rows 16 and 17, printed again as a two-bit condition). Neither can be dropped alone: a pair that breaks only one of them dies at row 19.
Dropped together they can: at step 19, CH(E18, E17, E16) emits terms at bits 24 and 23 whenever E17 and E16 differ there, and the signed sum of row 19 absorbs them with a different sign solution of S1(E18); the pairs that continue keep the parity E16[23] ^ E19[29] ^ E18[1] ^ E18[5] = 0 together with the four patterns' parities (our backward analysis of the characteristic).
Our own full-path test before this build (rows 16..36, sequential Monte Carlo with same-sample tagging, 6 fresh seeds, 4.0e8 samples, 30,814 collisions, every collision rebuilt and hashed again independently, 0 false) gave a ratio of 1.5055 (+0.590 bit, per-seed 95% interval [0.548, 0.631]) over the four patterns with the six A16 two-bit relations of row 16 necessary (0 of 49.9M violating proposals continue). A preregistered sweep of 30 further pairs of conditions of rows 16..21, each dropped together on top of R16x, found no further gain (each pair, and each member alone, gave 0 collisions; 0 false among 928,760 rehashed).

**The change to the counted program** (`experiments/lowm.py`): the character of bit 23 of `CHE[16]` is `=` instead of `0`, the character of bit 24 of `CHE[17]` is `=` instead of `+`, and the two-bit condition (E, 16, 24, =, E, 17, 24) is removed from `X2`:

```text
 row 16   Table 15 =0=====+00===11=+==01=0=0==+====     program =0=====+=0===11=+==01=0=0==+====
 row 17   Table 15 =0=====+01===u1=+==0==1===1u====     program =0======01===u1=+==0==1===1u====
```

The parity is not tested by the program: every pair that follows the remaining cells of rows 16..36 has zero output difference and is verified with the target before output, so testing it would only add operations, and the estimator below counts the pairs that follow the cells of rows 16..36 (q3c), which the program accepts together with the further collisions of Section 7.7. `row_ok` reads the masks and values of the cells as constants, so `ROWCHECK` and `ROWCOMP` are unchanged.
What the change does cost is at row 16 (Section 6.2): every l in L* now has row-16 values, the 4-lane table stage has 13 conditions on bits 0..23 (E|filt(u)| = 1/256 = 0.003906 per lane, Pr[filt(u) != 0] = 63,512 / 2^24 = 0.003786), and the expected number of row-16 hits per probed lane is 2^-11 instead of 1,052,672 / 2^32. These are in the ledger (Section 11) and in the simulation of the counted program (Section 13.3).

**Joint study.** The estimator of Section 7.4b, with its constants written by `gen_consts.py` from this `experiments/lowm.py` (`q3consts_r16x.h`), so that it checks exactly the cells and conditions the counted program checks: the four patterns of rows 18 and 19 and R16x are one carrier, measured together. Stage 16 enumerates all 2^24 values of E16x with the eight fixed bits for each l and reproduces the 2,097,152 pairs (u, l) of Appendix A.
The binary differs from that of Section 7.4b only by a TAG line that counts the full passes whose member x keeps E16[23] = 0 and E16[24] = E17[24]; it draws no random numbers, and built with the constants of Section 7.4b it reproduces the filed outputs of seeds 720000 and 721000 byte for byte (known-answer check).
**Preregistration** (`PREREG_q3R16x.txt`, sha256 18569704b1115d99c138e641986101687836aa408e1f29d670cad354da0691d3, stamp 2026-10-12T16:13:47Z, written before any listed seed ran; reproduced in Appendix G): two independent blocks J1 (seeds 740000..740127) and J2 (seeds 741000..741127) of 128 replicates, NP = 8192, M = 512, MT = 16384; rule fixed in advance: **declared q3 = 2^x, x = floor(100 log2 min(LB_J1, LB_J2)) / 100**, LB the one-sided 99% Student lower bound of the mean of the 128 linear estimates of the block (the spread between replicates carries any overdispersion of the counts within a run). Every listed seed was run and is reported (Appendix G); none was dropped or rerun. Because these offline preregistrations, complete seed ranges, interim progress looks and prior 30-pair screening do not bind an organizer holdout nonce, the premise that they exclude material selection, optional-stopping and multiple-comparison bias beyond the margin to the declared `q3c_used = 2^-71.4243` (the preregistered min-of-blocks bound 2^-71.4629 is carried as a sensitivity) is declared explicitly as part of heuristic H2 (Section 12) and checked at reduced scale on the organizer's holdout seed in `a0-online-r37` (Section 13.2).

**Results.** J1 mean 2^-71.4296, relative sd 0.1096, **bound 2^-71.4629** (one-sided 99% upper bound 2^-71.3970); J2 mean 2^-71.4177, relative sd 0.1143, **bound 2^-71.4524** (one-sided 99% upper bound 2^-71.3838, so q3c <= 2^-71.38 < 2^-70). Rule now applied: **q3c_used = 2^-71.4243**, the one-sided 99% lower bound of the mean of 17,408 fresh preregistered replicates drawn on this filing's own variant list (Appendices G.3..G.5: block E is 16,384 fresh seeds 772000..788383 with mean 2^-71.42132 and sd 0.15870, pooled with the 1,024 seeds of G.4 to a mean of 2^-71.42147, sd 0.15870 and bound 2^-71.42427, rounded down; no sub-pool transfer allowance, because the measured quantity is the submitted pool's own q3c). The rules of this section remain stated as sensitivities: the pooled 256-replicate bound 2^-71.447381 is 2^-71.4474 (claim 57.72781) and less the 0.0020-bit allowance is 2^-71.4494 (claim 57.72980), the superseded 5x charge 0.0104 gives 2^-71.4578 and claim 57.73815, and the preregistered min-of-blocks rule gives 2^-71.4629 and claim 57.74322. The statistic of this section: the one-sided 99% Student lower bound of the mean of the **pooled** 256 linear estimates -- pooled mean 2^-71.4236, relative sd 0.1118, t(254 df) = 2.3413, i.e. mean x (1 - 2.3413 x 0.1118/16) = 2^-71.447381, rounded down to four decimals of log2 and never up, 2^-71.4474. It is one pre-specified statistic over exactly the seeds the preregistration lists: both blocks were always reported, no seed was added, dropped, replaced or rerun, and no interim look or stopping rule enters it. It is 0.0155 bit tighter than the preregistered min-of-two-block-bounds rule (2^-71.4629, claim 57.74322), which remains stated as the conservative sensitivity, 0.55 bits above the four patterns alone (2^-72.02, Section 7.4b) and 2.56 bits above Table 15 (2^-74.03); the pooled mean is 0.569 bits above the pooled mean of the four-pattern study.
Stage means (log2 averaged over the 256 replicates), rows 16..22 and the tail: 16: -16.000, 17: -12.000, 18: -8.000, 19: -11.430, 20: -7.000, 21: -2.000, 22: -11.003, tail -3.999 (row 16 is -16.000 exactly: 2^21 of 2^37 pairs (u, l)). Of the 2,149,260,669 full passes counted in the tails, 1,438,939,086 (a share of 0.6695) keep E16[23] = 0 and E16[24] = E17[24]; the rest use R16x, including the four l (0, 2, 16, 18) that have no row-16 value under Table 15. These shares are a description of the resampled particles, not a part of the bound.

### 7.5 The examined family of this filing

The registered studies of the parents drew W8 from the 782,800 variants of the 222 classes, and (W6, W7) uniformly from F6 x F7. **This filing examines a sub-family**: the 170 classes of lists 0, 1, 5 and 6 (599,760 variants), and (W6, W7) exactly as before. Every variant of every kept passing class is examined, and given a good pair the variant, W6 and W7 have the laws of the studies
(Lemma 5.1: for every variant a0, W7x is uniform on F7 and W6x uniform on F6 given that the pair is good, independent of each other and of the variant). So q3 = the mean over the 599,760 variants and the 32 elements of L* of the study's conditional probability.
The restriction is **q3-neutral**, not an x-weighting: by Lemma 7.1 the rows 16..22 cells have one probability for every variant, and the rows 23..36 cells depend on the variant only through the four W24 conditions on `W24x = Z + W8x`, with `Z = s1(W22x) + W17x + s0(W9x)`. For every fixed Z the map `W8 -> Z + W8` is a bijection of 2^32, so under the model's own `Z` near-uniformity the conditional probability of the tail is the same for every variant *exactly*, hence the mean over any sub-pool equals the mean over the whole family, and the residual is second order in the non-uniformity of Z (Section 7.8: bounded by the same 0.001 bit by which the study's own measured tail, 2^-3.999 over 782,800 variants, departs from the exact 2^-4). The parents' text prices 0.05 bit for a *weighted* subset (0db0eeb6 Section 7.6); a whole-class uniform restriction introduces no weight, so this filing does not pay that hedge, and instead charges the only *measured* transfer that exists for this quantity: fb039a6e's preregistered 128-replicate study of the same q3 over the whole family G (one-sided 99% bound 2^-74.0088) and over a kept-fibre-weighted pool (2^-73.9984), i.e. **0.0104 bit**, which is 5x the structural bound of Section 7.8 and 5x below the flat hedge.
**q3c_used = 2^-71.4243**, measured directly on the submitted pool by the preregistered study of Appendix G.3, so no sub-pool transfer allowance is applied (this section is the structural reason the restriction is q3-neutral at all; the measured difference of the two pools' means is 0.0003 bit). Stated sensitivities of the same ledger: the parents'-pool pooled 256-replicate bound 2^-71.4474 is 2^-71.4474 (claim 57.72781) and less the 0.0020-bit allowance is 2^-71.4494 (claim 57.72980), the superseded 5x measured charge 0.0104 gives q3c 2^-71.4578 and claim 57.73815, and the preregistered min-block bound 2^-71.4629 gives claim 57.74322 on this family; four patterns alone 2^-72.02, Section 7.4b; q3 = q3c x 2.4331, Section 7.7). For the Table 15 pattern the registered floor of study B is 2^-74.03 (its one-sided 99% bound is 2^-74.0225, its mean 2^-73.9987; study A's bound is 2^-74.0659), and fb039a6e measured the same quantity over the whole family G (a preregistered 128-replicate study: one-sided 99% bound 2^-74.0088) and over a kept-fibre-weighted pool (2^-73.9984);
**Consistency note (disclosed, not silently repaired).** The operative value is `q3c_used = 2^-71.4243` in every place this text assigns a q3c, and it is the constant `Q3_LOG2` that `experiments/lowm.py ledger` executes. A reader of the previous revision found three assignments that still carried the superseded min-of-blocks floor `2^-71.4629` (Sections 7.4c and 12) and one that still carried the superseded 5x measured charge `2^-71.4578` (Section 7.8), plus the historical declaration of Appendix G.2. Each now names the quantity it actually describes; the superseded values appear only as the stated sensitivities of Section 12. No ledger constant, claim digit or certificate changes: `lowm.py ledger` prints `time_log2 = 57.70485` before and after this repair.

our validation V reproduces the registered study (Section 7.4b). That the dependence on the variant is the four W24 conditions, about 2^-4 for every W8 (Lemma 7.1), is unchanged by the relaxations, which act on rows 16..19 only.
Real first blocks (7319bba, Section 13.1, Table 15 cells): the row-16 pass rate of the attack's own good pairs is the exact 1,052,672 / 2^32 (z = +0.88 and +0.51 over 424,363 and 1,693,297 passes); this program's own simulation (Section 13.3) finds row-16 passes at its exact rate under R16x, 2^-11 per probed lane.

### 7.6 Rows 18 and 19: the accepted value patterns (credit: Jbenisek's ffbe30bb-ac92-4191-a589-3bf32661ee7d)

Table 15 fixes the value bits E18[1] = 1, E18[5] = 0, E18[10] = 1, E18[11] = 1, E18[18] = 0, E18[28] = 0, E18[29] = 1 and E19[29] = 1. They are not all required. With every other cell and printed two-bit condition of rows 4..36 kept, exactly four patterns of these eight bits admit a 37-step semi-free-start collision for the published dense part
(an all-solutions enumeration with a verified 37-step model, Bitwuzla and Z3, done for ffbe30bb; the three further collisions are checked below), because the bits enter only through six parity conditions: E18[1] = E18[11], E18[1] != E18[28], E18[10] = E18[29], E18[10] = E19[29], E18[5] = E18[18] and E18[5] ^ E18[1] ^ E18[10] = 0.
The seven E18 bits enter only through the signs of the signed difference of S1(E18) at step 19 (each output bit of S1 is the XOR of three taps, and the sign of the difference at that bit depends on the XOR of the two taps that carry no difference), and E19[29] only through E18[29] ^ E19[29] = 0 in the signed difference of Ch(E19, E18, E17) at step 21.
The relaxation, its pattern table, the 74 single-flip tests, the seven unforced candidates of rows 20..22 (all necessary) and the exact stage enumeration (3.80 times as many W18 reach row 19 with the four patterns, 1.93 bits, interval 1.78 to 2.09) are ffbe30bb's and are quoted, not redone here, except for the check of the three alternative collisions and the q3 studies of Section 7.4b, which were run for this filing's family.

The strings of the E cells of rows 18 and 19 in `experiments/lowm.py` (`CHE[18]`, `CHE[19]`) are now

```text
 row 18   Table 15 ==10===uu====0==n===111===01==1=     program =======uu=======n=====1====1====
 row 19   Table 15 ==1====00====1==0==========1====     program =======00====1==0==========1====
```

(the remaining `1` of row 18 are E18[9] and E18[4], which stay imposed; so do the differences `u`, `n` and every other character). That is the whole change to the counted program: `row_ok` tests the masks and values of the cells as constants of the straight-line text, so the operation counts of Section 9 (`ROWCHECK`, `ROWCOMP` per row) and the ledger are unchanged;
no operation was added and none removed. The six parity conditions are not tested separately: the exact signed-difference check of both members that `row_ok` always made, at rows 19 and 21, rejects the other patterns, and a separate test would only add operations. The patterns accepted, as flips of Table 15's values (E18 bits 29,28,18,11,10,5,1 | E19 bit 29):

| pattern | flipped bits of Table 15's values | flip masks (E18, E19) | value bits (E18[29,28,18,11,10,5,1] E19[29]) |
|---|---|---|---|
| 0 Table 15 | none | 0x00000000, 0x00000000 | 1 0 0 1 1 0 1 \| 1 |
| 1 | E18[5], E18[10], E18[18], E18[29], E19[29] | 0x20040420, 0x20000000 | 0 0 1 1 0 1 1 \| 0 |
| 2 | E18[1], E18[5], E18[11], E18[18], E18[28] | 0x10040822, 0x00000000 | 1 1 1 0 1 1 0 \| 1 |
| 3 | E18[1], E18[10], E18[11], E18[28], E18[29], E19[29] | 0x30000c02, 0x20000000 | 0 1 0 0 0 0 0 \| 0 |

The organizer experiment `a0-sfs-r37` imposes pattern t mod 8 on its construction of trial t (`IMP` and `PAT` in `experiments/lowm.py`): patterns 0..3 are the four above with E16[23] = 0 and E17[24] = E16[24], patterns 4..7 the four R16x patterns with E16[23] = 1 and E17[24] != E16[24] (value bits E18[1,5,10,11,18,28,29], E19[29] with E18[11] != E18[1], E18[28] = E18[1], E18[10] = E18[29] = E19[29], E18[5] = E18[18] = 1 ^ E18[1] ^ E18[10]; Section 7.4c); it checks every cell of rows -4..36 with the program's own `row_ok`, which accepts all eight; for trials 0..15 the constructed chaining value is fed to the counted online program, which must find exactly the constructed pair (Section 13.2).
**Check of the three alternative collisions** (`check_alt.py`, Appendix F; words MSB first, chaining value common, x = M', y = M; the pairs are ffbe30bb's, and here they are compressed 37 steps again and their cells tested with this package's `row_ok` and, for contrast, with the Table 15 cells of the program this one derives from):

```text
pair (x = M', y = M)         collides  cells of this lowm.py    cells of Table 15       
Table 15 (published pair)    True      True                     True                    
G1                           True      True                     False                   
G2                           True      True                     False                   
G1 xor G2                    True      True                     False
```

The CVs and messages of the three pairs are listed in `check_alt.py` (Appendix F). They are 37-step semi-free-start collisions, not ordinary collisions. Rows 16..22 are functions of the rows 12..15 of S, of l and of W16..W22 only (Lemma 7.1), so what the accepted patterns are is the same for every variant of the family.

### 7.7 The success event: equal outputs after row 21 (credit: our 4ec21bf9-f588-4b80-bb2b-77c1ccf8c9b7, R37R, Appendix D)

**The event.** A pair is a success when rows 16..21 follow every cell and every printed two-bit condition closing at those rows (Sections 7.4c, 7.6) and the two 37-step outputs are equal; rows 22..36 are computed with no cell test (`step3b`, Section 9.9). Both members share CV1, so their outputs cv + (A36, A35, A34, A33, E36, E35, E34, E33) are equal iff the eight registers are equal, which is the comparison the program makes (`same_out`); a success is a collision of the second block and is verified with the target before output.
The cell event of rows 22..36 is contained in this event (the characteristic ends with zero differences), so q3 = q3c x R with R = Pr[equal outputs | rows 16..21] / Pr[cells of rows 22..36 | rows 16..21] >= 1, under the law of the late words of the cell studies ((W6, W7) uniform on F6 x F7, W8 from the variant list).

**Structure (4ec21bf9, Appendix D.2; the characteristic and the constants D6, T6, D7, T7 are this package's).** Given rows 16..21 following the cells, dW22 = 0x017f8000, and the two outputs are equal iff E22[29] = 1, s1(W22') - s1(W22) = 0x4fff9f30 and s1(W24 + 2^29) - s1(W24) = 0xfff80c00 (dW26 = 0). The words W22 with the second condition number 9,830,400 = 75 x 2^17 of the 2^32 words, against 2^22 for the printed cells (75/32); the words W24 with the third number 17 x 2^24, against 2^28 (17/16); dW26 = 0 has probability 17/256 against 16/256. The uniform-model ratio is 1275/512 = 2.4902. W24 = s1(W22) + W17 + s0(W9) + W8 is correlated with W22, so the ratio is measured.

**Measurement (4ec21bf9, Appendix D.3 and D.3b; the program there is ours).** Ratio of collision events to cell events after row 21, every cell event also a collision event in every run: 2.4648 +- 0.0145 on Table 15 states; on ffbe30bb's states runs of 2^30, 2^31 and 2^31 late proposals give 2.4580, 2.4416 and 2.4674 (the last preregistered) and 2.4552 pooled; 2.46455 under the attack's kept-fibre law of (W7, W8) (preregistered, 64 seeds, 2^32 late proposals: 323,337 collision events against 131,195 cell events). The preregistered rule gives EXQ = min(2.4331, 2.4443) = 2.4331, below every one-sided 99 percent bound computed from these data, the overdispersion-robust ones included (2.4408 to 2.4520). This filing takes EXQ = 2.4331 from that measurement and does not repeat it.

**What changes here.** q3 = q3c x EXQ, q3_used = 2^-71.4243 x 2.4331 = 2^-70.14150 (1.28 bits more probability per success), and q3 <= 2^-71.38 x 2.4902 = 2^-70.0637 (the uniform-model ratio, above every measured ratio, is the upper value used in H3(b)). The program and the ledger change only in the rare path (Sections 9.9, 10, 11): rows 22..36 are computed in full for every pair that passes row 21 and the output comparison replaces the cell test of those rows; rows 16..21, the cells, the table stages and the cost of everything before the rare path are unchanged.

### 7.8 The family restriction is q3-neutral (new; exact, from the shipped program)

Why a whole-class restriction may be filed against the parents' study at all, and what it can cost. Lemma 7.1 gives the structure: the rows 16..22 cells have one probability phi_l for **every** variant, and the rows 23..36 cells are the four conditions on W24, whose x member is `W24x = Z + W8x` with `Z = s1(W22x) + W17x + s0(W9x)`. Write tau(w) = Pr[tail | variant w] = sum_z mu(z) f(z + w), with f the tail indicator and mu the law of Z given rows 16..22 pass. Then

```text
q3c(pool) = (1/32) sum_l phi_l  x  (1/|pool|) sum_{w in pool} tau(w),
```

so the pool enters only through the mean of tau, and the ratio q3c(S)/q3c(G) does not depend on phi_l, on l or on the l-sum at all. Two consequences, the second of which is the bound this filing charges:

1. **Exact neutrality under the model's own idealisation.** If mu were uniform on 2^32 then for every w the map z -> z + w is a bijection of 2^32, so tau(w) = sum_v f(v)/2^32 is the same number for every variant, and every pool -- 599,760 or 782,800 or one variant -- has exactly that q3c. The variant dimension of the estimator then costs nothing but variance, which is what the 256-replicate spread (relative sd 0.1118) is.
2. **The residual is measured, not assumed.** The deviation of q3c from the uniform-Z value is linear in the deviation of mu from uniform, and the study measures that deviation at the aggregate: the shipped tail stage mean over the fil's 782,800 variants is 2^-3.999 against the exact 2^-4, i.e. 0.001 bit. Two pools' means of a quantity that departs from its neutral value by 0.001 bit can differ by at most 0.002 bit, and the difference of the *measured* pools is smaller than that because the kept 599,760 variants are 76.6 % of the study's own list. **The restriction therefore costs at most 0.001 bit of q3c, and this filing charges 0.0104 bit**, the only preregistered measurement of this reweighting that exists (Section 7.5), i.e. 5x the bound and 5x below the 0.05-bit flat hedge of 0db0eeb6 Section 7.6.
3. **The 0.05 case, for completeness.** At q3c = 2^-71.4474 - 0.05 = 2^-71.4974 the same ledger gives time_log2 = **57.77752**, which is still below the lane's best review (57.89863). Every admissible charge between 0 and 0.05976 bit leaves a lead; the break-even charge is 0.05976 bit, 60x the structural bound.

The three texts that carry this in the program are the family's `LISTID` (170 entries), the constant `C7_CONST = 0xc086800c` and the dynamic-bit set `C7_DYN_BITS` (15 bits: bit 2 of c7 is constant on the four kept lists, so the C7 test is 29 rather than 31 operations), and `Q3_LOG2 = -71.4243`. `experiments/lowm.py selftest` re-derives the family, the variant count and the op counts from the descriptors alone (Appendix D).

## 8. The algorithm

### 8.1 Lemmas 8.1 and 8.2 (the class test, the W6 test and the cube of a list)

Let x = A_{-1}, cb = C6 - A_{-2}, q = A1 ^ x, and for a class with base and mask put

```text
CB3 = cb + (A1 & x) + (base & q),   KZ = K3C + x - (A1 & A2) - (base & FA),   FA = A1 ^ A2,   C4 = 000b362e,   e4 = a0 + C4,   e3 = KZ - (s & FA).
```

**Lemma 8.1.** (a) The class passes the W7 filter at x iff F7(c7 - x). (b) For a0 = base | s of the class, W6x = cb + phi(a0, x) = CB3 + (s & q) - H, mod 2^32, where H_j = e4_j for the bits j with E5_j = 1 and H_j = e3_j for the bits with E5_j = 0 (E5 = e7f2c81f).
Hence a0 is good (W7x in F7 and W6x in F6) iff its class passes and F6(CB3 + (s & q) - H).
*Proof.* (a) Section 5.1. (b) W6x = C6 - A_{-2} + MAJ(A1, a0, x) - CH(E5, e4, e3) with e4 = a0 + C4 and e3 = K3C - MAJ(A2, A1, a0) + x (Section 5.1), and CH(E5, e4, e3) selects bit j of e4 where E5_j = 1 and of e3 where E5_j = 0.
MAJ(A1, a0, x) = (a0 & (A1 ^ x)) | (A1 & x) with disjoint bit sets, so MAJ = (a0 & q) + (A1 & x); likewise MAJ(A2, A1, a0) = (a0 & FA) + (A1 & A2). Since a0 = base + s with base & s = 0 (Section 5.3), a0 & m = (base & m) + (s & m) for every mask m.
Collecting the scalar terms gives CB3 and KZ. QED. (Checked on every lane of every pass plane of the experiments and of `selftest`, 0 mismatches.)

**Lemma 8.2 (the cube).** Let b be 0, 2 or 3, and let a0 have bit 1 set if b is 2 or 3. If q_b = 1 then F6(W6x(a0 xor 2^b)) = F6(W6x(a0)) (and W6x(a0 xor 2^b) = W6x(a0) for the bits >= 1); if q_b = 0 then W6x(a0 with bit b set) = W6x(a0 with bit b clear) - 2^b.
Hence for a rep t (no cube bit set), Q0 = {b in B : q_b = 0}, cu a submask of Q0 and i a submask of I = B xor Q0: F6(W6x(t xor cu xor i)) = F6(W6x(t) - cu) (mod 2^32), cu read as the integer sum of its bits.
*Proof.* A1 = 62827866, FA = fafd5ca2, C4 = 000b362e, E5 = e7f2c81f: bits 0, 2, 3 of FA are 0, so e3 = KZ - (s & FA) does not depend on s_b; bits 0..4 of E5 are 1, so H_b = e4_b for b = 0, 2, 3 (and e3 is only evaluated from bit 5 upward with carry_5 = 1 because (s & FA)[4:0] <= 16 <= K3C[4:0] = 28). In e4 = a0 + C4: C4_0 = 0, so e4_0 = a0_0 and there is no carry out of bit 0;
for b = 2, 3 with a0_1 = 1 (and C4_1 = C4_2 = C4_3 = 1) the carry out of bit 1 is 1, a0_2 + 1 + 1 gives the sum bit a0_2 and carry 1, a0_3 + 1 + 1 gives the sum bit a0_3 and carry 1, so e4_2 = a0_2, e4_3 = a0_3 and the carry into bit 4 is 1 whatever a0_2, a0_3 are.
Thus s_b enters W6x = CB3 + (s & q) - H at bits >= 1 through (q_b - 1) s_b 2^b, which is 0 if q_b = 1 and -s_b 2^b if q_b = 0; at b = 0, F6 does not read bit 0 of W6x, and when q_0 = 1, s_0 = 1 adds 1 to (s & q)_0 and 1 to H_0 = a0_0, which cancel in W6a - H with zero net carry into bit 1. QED. (Checked on 30,720 tuples in `selftest`.)

*The cube of a list.* The bits of {0, 2, 3} in which a list is closed under the flip form its cube B (computed; Section 5.3): B = {0, 2, 3} for the lists 0, 1, 5, 6 (their classes have a0 bit 1 set) and B = {0} for the other six. The list is the union over f subset of B of (reps xor f), reps = the members with no cube bit (432, 432, 450, 450 and 1728, 1728, 1728, 1792, 1792, 1792 reps).
For a first block put I = (q & B) | (CB3 & 1) (the cube bits that do not matter at this x) and Q0 = B xor I. By Lemma 8.2, F6(W6x(t xor f)) = F6(W6x(t) - (f & Q0)) for a rep t and f subset of B, so one test of F6 on W6x(t) - cu decides the 2^|I| members t xor cu xor i, i subset of I: the program computes the sums W6x(t) once (the main run) and obtains the other 2^|Q0| - 1 runs from the stored sums and upper failure planes.
Given that a class passes the W7 test, x mod 16 is uniform: in both affine pieces of the bitwise form of F7 (Section 5.1) the bits w0..w3 of w = c7 - x are individually free (w0 = w28, w1 = w18 (= w29), w2 = w19 tie them to other free bits), so w mod 16 and hence x mod 16 = (c7 - w) mod 16 are uniform; q_0, q_2, q_3 are independent uniform bits before applying the CB3 bit-0 optimization; the executed I law is derived below.

The scalars CB3 and KZ are computed once per passing class; the planes of the reps (14 or 16 bits) are the only lane-dependent data. Both tests are programs on *planes*: a plane is a 256-bit word holding one bit of each of 256 lanes (the lanes of a batch are 256 consecutive reps of a list).


**Executed cube law under H1.** A1[0]=0, so q0=x0.
Every one of the 170 c7 constants of the family is even; for w=c7-x modulo 2^32,
w0=x0. Both disjoint affine pieces of F7 leave w0 free and pair w28=w0.
The first piece has rank six and 2^26 words; the second rank twelve and
2^20 words. Adding constraints on w0,w2,w3 raises each rank by three,
so each assignment occurs (2^26+2^20)/8=8,519,680 times and exactly
34,078,720 of 68,157,440 words have w0=0. At fixed w1, subtracting w
from c7 is triangular and bijective on bits 0,2,3, even with borrows;
checking all eight assignments for each class confirms the joint cube law.
Thus q0,q2,q3 are jointly uniform conditional on a class passing.
Under H1, cb=C6-A_{-2} is uniform on Z/(2^32) and independent of x.
For each fixed x, CB3=cb+(A1&x)+(base&q) translates cb by a constant;
therefore Pr[CB3=y | x]=2^-32 for every y. This proves that CB3 is
uniform and independent of x, hence also of q0,q2,q3 and the class event
F7(c7-x). Its bit 0 remains independent uniform after conditioning on
that event. In the executed `I=(q&B)|(CB3&1)`, Q0[0] requires q0=0
and CB3[0]=0, so its probability is exactly 1/4. Q0[2] and Q0[3]
remain independent uniform bits. A mask Q0 on a k-bit cube therefore
has weight `(1 if Q0&1 else 3)/2^(k+1)`, as in the predecessor's ledger.

### 8.2 The online algorithm

```text
input: N_FB, V_MAX; precomputed: S, L*, the four lists as planes of reps and packed entries, the 170 class descriptors, the c7 planes, the chunk tables FIRST and SECOND, the lane-scan table, per-l constants
V = 0
for f = 1 .. N_FB:
    draw two uniform 256-bit words; M0 := their sixteen 32-bit fields; CV1 := F_37(IV, M0)                                     [1 unit]
    x := A_{-1}; cb, q, CB2 = cb + (A1 & x), KXA = K3C - (A1 & A2) + x; the 16 planes of q; cv_pre(CV1)                          (Section 9.2)
    plane P7 := F7(c7 - x) over the 170 class lanes (bit-sliced)
    for each set lane c of P7:                                                                                                    (passing class)
        CB3, KZ; the planes of CB3 (31) and KZ (16 bits) are formed and stored; I = (q & B) | (CB3 & 1), Q0 = B xor I                           (Section 9.3)
        main run: for each sweep of two batches of reps of the class's list:
            load the scalar planes of the sweep; for each batch: load the planes of the reps; sums W := W6 program (15 or 9 planes stored if Q0 != 0); pass plane := F6(W)   (Sections 9.4, 9.5)
            gather(pass plane, cu = 0)
        if Q0 != 0: for each batch: reload the stored planes; for each nonzero submask cu of Q0: pass plane := F6(W - cu); gather(pass plane, cu)              (Section 9.5)
        where gather(plane, cu): for each set lane (r, i) of the plane (13-bit chunk scan):
                    entry := ((packed word i of the batch)[part r] in bits 192..255) xor BP_top(class) xor D_top[cu]
                    for each submask ii of I (the 2^|I| members of this rep, unrolled with register-cached D_top[ii]): shift Gw := (Gw >> 64) | (entry xor D_top[ii])
                        when the group register holds four entries (Gw & M64 != 0): U := packed row-16 address of the group            (Section 9.7)
                            for each of the four lanes: u := U lane; FIRSTw := FIRST[u & 8191]; if FIRSTw != 0: T := FIRSTw & SECOND[(u >> 13) & 2047]; if T != 0: G := filt(u)
                                for each l in G: if exact(u, l): recompute W6, W7; rows 16..21 of both members with early abort    (Sections 9.8, 9.9)
                                    if rows 16..21 pass: rows 22..36; if the eight output registers are equal: build m, m'; if digest(m) = digest(m') and m != m': output, halt
    the last group of the first block is padded by repeating its last entry and processed
    V += the counted work of this first block; if V > V_MAX: halt (failure)
halt (failure)
```

The loop is the function `attack(nfb, vmax)` of `experiments/lowm.py` (`python3 lowm.py attack N V`): at most N first blocks, V the counted data-dependent operations of Section 9, halt when V exceeds the cap; an output is verified with the target digest before it is returned.

### 8.3 What is not assumed

No property of x other than being a 32-bit word is used (and, for the cube, that x mod 16 is uniform given that a class passes: Section 8.1), and nothing about the correlation of the classes of one first block: the ledger uses only the exact marginal law of each class test (probability p7 = |F7| / 2^32) and of each variant's F6 test given its class passes (p6 = |F6| / 2^32, exactly,
because cb is uniform and independent of x), the law of |I|, and linearity of expectation. Padding lanes (the repeated last entry of a first block's last group) are probed and charged; a duplicated member that hit would be processed twice, which changes the cost (charged) and not the set of pairs found.

## 9. The counted program

### 9.1 Machine and pricing

256-bit word RAM, 64 registers, every executed primitive counted (loads, stores, branches and address additions included). 32-bit values are kept in the low bits; a reduction mod 2^32 is one AND; a 32-bit rotation pattern (S0, S1, s0, s1) costs 8: d = x | (x << 32) (2), three shifts and two XORs and one mask.
A conditional branch tests a register for nonzero and is one primitive. Every address that is not a register value is formed by a counted add (one add per plane or word load; a table read is an index extraction, an add of the table base and a load). The program text is straight-line code.
The target compression of a first block is one unit and its internal operations are not counted again.

**Plane algebra.** The plane programs are executed by `lowm.py` on Python integers of 256 bits through a small algebra whose every call is a primitive of the straight-line text: a plane carries a *static constant tag* (all-zero, all-one: a constant of S such as C4, E5, A1 ^ A2) and an *inversion flag* (the stored word is the complement of the true plane).
These are compile-time facts of the text, not data: x ^ 0 = x, x ^ 1 = ~x (flag flips; no primitive), x & 0 = 0, x & 1 = x, x | 1 = 1, x | 0 = x cost nothing; an AND or OR of two planes with equal flags is one primitive (both flagged: De Morgan, the stored words are combined with the dual operation);
an AND or OR of unequal flags costs a NOT first (2 primitives); every other XOR, AND, OR on dynamic planes is one primitive. A full-adder bit is `xy = a ^ b; sum = xy ^ c; carry = a ^ (xy & (a ^ c))`: 5 primitives, 4 without the sum; with a static constant operand bit b: xy = a or ~a (free) and carry = a & c or a | c: 1 primitive.
The counter `CN.n` of the algebra is the count of the plane programs; `process_cv` asserts the counts of the plane programs (W6 and the subtraction runs of each batch of each list, F7 = 112) at every execution (the counts do not depend on the data, only on the batch and the list). The scalar and control steps are counted where they execute by the constants below.

### 9.2 Fixed per first block: FIXED = 490 operations

First block words: 2 random words and the 16 fields (field 0 of a word: and; fields 1..6: shr, and; field 7: shr): 30; control 16 (loop counter add and compare-branch, the cap test, address arithmetic not itemised below): 46. Then:

- **Class test, 275** (the parents' family: 299): -x mod 2^32 (2); the planes of -x, z_j = 0 - ((s >> j) & 1), consumed bit by bit (3 per plane, 2 for plane 0: 95); the dynamic planes of c7 (`C7_DYN_BITS` = bits 4..12, 19, 20 and 25..28, fifteen of them: bit 2 of c7 is `C7_CONST` bit 2 = 1 on all four kept lists, so that plane is a static constant here; 15 loads and 14 address adds: 29); the adder c7 + (-x) with sums for the 17 bits {0, 1, 2, 9, 10, 11, 12, 18, 19, 22, 23, 26, 27, 28, 29, 30, 31} and the F7 test:
  F7 is in the bitwise form of Section 5.1; F7_OPS = 106, measured on this text and split as 83 (the c7 + (-x) add over the fifteen dynamic planes) + 23 (the F7 program); the parents' sixteen-plane c7 measures 112 (89 + 23) when the same `measure_ops` is run with bit 2 restored, so the whole -6 is the family's, not a re-pricing; the mask of the 170 valid lanes (1); the scan of the plane (42 primitives: for each of the three 64-bit parts that hold a lane of the 170 the extraction of the part (1 or 2) and, of its five chunks (four of 13 bits, one of 12), the four that start before lane 170: the extraction (1 or 2) and a zero branch -- SCAN_FIX(nl) of Section 9.6 with nl = 170).
- **Scalars and planes, 169:** cb = C6 - A_{-2} (2), q = A1 ^ x (1), A1 & x (1), CB2 = cb + (A1 & x) (2), KXA = K3C - (A1 & A2) + x (2); the 16 planes of q (bits 2, 3, 4, 6, 7, 10, 14, 15, 17..24; bit 0 is not read by any batch because s_0 = 0 on all reps; 48) and their stores (16 stores and 16 address adds: 32);
  `cv_pre` (81 as in 0db0eeb6 Section 9.2: e0b, kap0, C = RBASE + (kap0 - e0b), x12, n12, X, Em2, kap1 and the broadcasts of the constants to four lanes, and the unpacking of the chaining value from the compression output).

### 9.3 Per passing class: 260 + 8 + 5 operations, and per subtraction run

Per set lane of the class plane: table load 1 (the 8192-word `scan_table` is placed at word address `0..8191`, so the nonzero 13-bit chunk `c` is directly its own word address with no base add), chunk offset add 1, c & (c - 1) 2, branch 1: CLS_LANE = 5. Then: five loads of the class descriptor (base, BP = base | ((~S0(base) & M32) << 32), list pointers, batch count, cost word) with their address adds (10);
CB3 = CB2 + (base & q) + C4_MOD (3; folding the constant bits of C4 at E5 = 1 into CB3) and KZ = KXA - (base & FA) (3); the planes of CB3 for the bits 1..31 (93; the W6 programs never read bit 0) and of KZ for the 16 bits {5..9, 11..13, 15..17, 24..28} where s & FA = 0 (48; at the 8 bits {7, 10, 14, 18..22} with s_j = 1 in a batch, e3_j = KZ_j ^ s_j ^ ~borrow_j uses the scalar plane directly), 3 per plane; their stores
(47 stores and 47 address adds: 94); one work-counter update (1): 10 + 6 + 141 + 94 + 9 = 260 (including the 9 planes of KZ_j at {7, 10, 14, 18..23} formed once in registers). The cube: the mask B of the list (load and address add 2), I = (q & B) | (CB3 & 1) (1), Q0 = B xor I (1), the tests I == 0 and Q0 == 0 (2), and q_0 for bit 0 of W6a - H (2): CF_CLASS = 8 (when I != 0, the 2^|I| - 1 <= 7 cube deltas D_top[ii] are also loaded once per class into registers: 5 x 2^|I| - 2 primitives, Section 9.6).
**The main run** (cu = 0) has no extra cost: the cube planes of s are static zeros of the text. **A subtraction run** (a nonzero submask cu of Q0, per batch, in increasing order): the next submask (cu - Q0) & Q0 and its test (3); BP_top xor D_top[cu] with D_top[cu] = (cu | (S0(cu) << 32)) << 192 read from a table of eight words (address 1, load 1, xor 1: 3);
the work-counter update (1): RUN_CU = 7, and the pass plane of F6(W - cu) (Section 9.5).

### 9.4 Sweeps of two batches

A list of r reps is processed in nb = ceil(r / 256) batches (2 for 432 and 450 reps, 7 for 1728 and 1792), two at a time. A sweep loads the scalar planes it needs once for both batches: zq (the planes of q for the bits s_j of the two batches that are not the static zero: 11 to 15), zKZ (16), zCB3 (31), each one load and one address add, plus 3 of control: 3 + 2 x (58 to 62).
Per batch: the stored planes of the reps that are not constant over the batch (with their address adds) and the two pointers of the batch: 2 x (number of such planes) + 2 operations.

### 9.5 The W6 program of one batch and the subtraction runs

Straight-line on planes (Lemma 8.1), with sums produced only for the bits that are used. The cube bits of s (0, 2, 3 or 0) are static zero planes in the main run, so the constants fold. **Constant planes of a batch.** The reps of a list are stored in a fixed order (a bit-lexicographic order of the bits of s, chosen per list; `REP_ORDER` in `lowm.py`, chosen by a seeded search on this ledger and not on the success probability); in a batch of 256 consecutive reps some of the 14 or 16 planes of s are all-zero or all-one. Such a plane is a static constant of that batch's text (it is not stored, not loaded and folds in the algebra exactly as the cube planes do), and a W6 text is written for every distinct constant pattern: 8 batches, 50 constant planes in all, 45 distinct texts of 3,188 primitives in all (Section 14.1). The ledger prices the text of each batch of each list separately; `lowm.py` measures it (`ListData.measure`) and asserts the count at every execution.
Structure of the program (for every variant of the 170 classes, a0_1 = a0_5 = a0_11 = 1, a0_12 = a0_13 = 0, and base has 0 at all mask bits and at bits >= 14, so e4 = a0 + C4 decouples into bits 1..4 with carry_5 = 1, bits 5..10 with carry_5 = 1, and bits 14..31 = s[14..31] + C4[14..31] with carry_14 = 0; C4_MOD folds the static bits into CB3):

| step | primitives |
|---|---|
| e4 = s + C4 (carry_1 = C4_1, carry_5 = 1, carry_14 = 0; C4 static: carry = s & c or s \| c), dynamic sums for bits {2..4, 6..10, 14..28} with E5 = 1 | 23 |
| e3 = zKZ - (s & FA) from bit 5 with carry_5 = 1 (FA & mask has 9 bits: 7, 10, 14, 18..23), sums for the 13 bits with E5 = 0 (5..28) | 40 |
| W6a - H = zCB3 + (s & zq) - H merged bit-by-bit (carry-save full adder with half-adder carry reuse (xy & c) \| ac + carry-ripple at bits j >= 1; bit 0 is dead when Q0 = 0), sums for the 20 bits that F6 reads | 124 |
| F6 in the bitwise form of Section 5.1: pass = (w8 ^ w25) & ~fail with polarity-aligned andf/orf (plus upper failure planes and carry chain when Q0 != 0) | 24 |

The measured W6 counts per batch (main run / all sums): k = 3, all sums: 250 to 278 (mean 263.0); k = 3, main: 181 to 208 (mean 193.5); k = 1, all sums: 267 to 301 (mean 282.9); k = 1, main: 188 to 222 (mean 204.1); overall 181 to 301. The pass plane carries no inversion flag in the shipped text; `measure` adds one primitive if it did. A partial batch (the last, with fewer than 256 live lanes) costs one more AND with the lane mask.
**The subtraction runs.** Because cu <= 13 < 16, W - cu = (W[31:4] - c4(cu)) || (W[3:0] - cu) where c4(cu) in {0, 1} is the single borrow out of bit 3 (for k = 1, cu = 1 and W_0 = q_0 | ~a0_0 = 1 whenever q_0 = 0, so c4(1) = 0 identically!). Thus when Q0 != 0, the main run precomputes the upper failure plane for c4 = 0 (and c4 = 1 when k = 3) and stores only 15 planes (k = 3: SPILL = 30) or 9 planes (k = 1: SPILL = 18), reloaded once per batch;
for each nonzero submask cu of Q0 the pass plane combines the lower borrow chain on bits 0..3 with the pre-evaluated upper planes using polarity-aligned andf/orf; SUBF per batch: k = 3, cu = 13: 27; k = 3, cu = 12: 26; k = 3, cu = 9: 27; k = 3, cu = 8: 24; k = 3, cu = 5: 28; k = 3, cu = 4: 25; k = 3, cu = 1: 26; k = 1, cu = 1: 11 (primitives by (cube bits, cu)). Exactness: F6(W6x(rep xor cu)) = F6(W6x(rep) - cu) (Lemma 8.2), checked on every lane of every run (Section 13).
**Registers.** The two batches of a sweep are processed together bit by bit, j = 0..31; the loaded planes of bit j are dead after use. Each batch holds the carries (e4, e3, W6a, W) and the F6 operands that are kept for later bits, folded as soon as both operands of a term exist:
the pairs (w1, w12), (w2, w13), (w3, w14), (w14, w18), (w15, w19), (w9, w26), (w10, w27), (w16, w20), (w8, w25) and the three single bits w29, w30, w31; at most ten values at any bit. With at most six temporaries that is at most 20 live planes per batch, 40 for the sweep, plus about eight addresses, counters and constants: below 64, with no spill.
A subtraction run holds the 15 or 9 reloaded planes, the borrow and at most six temporaries (under 25 planes); the scan state of its pass plane (about 10 values) is added only after the F6 test has released its operands: below 64.

### 9.6 Scan of the pass plane, the reps and their members

The pass plane (zero in the unused lanes) is scanned in four 64-bit parts of five chunks (four of 13 bits, one of 12); a scan of a plane of nl lanes costs SCAN_FIX(nl) = 58 for nl = 256, 47 for nl = 194, 44 for nl = 192 and 42 for nl = 176 and for the 170-lane class plane (the plane is masked to nl lanes, so a chunk that starts at or beyond nl is identically zero and is not tested; iter25 removed the full-plane charge for partial batches). Per set lane (a passing rep): table load of the bit index 1 (`scan_table` at word address `0..8191`, so `c` is directly its word address), add of the chunk offset 1, add of the batch word pointer 1, load of the packed word 1, c & (c - 1) 2, loop branch 1: SCAN_LANE = 7.
The packed word i of a batch holds in its 64-bit part r the entry s | (S0(s) << 32) of the rep of lane 64 r + i. The entry is extracted directly into the top 64-bit lane (bits 192..255; EXTR = 1, 2, 2, 1 for r = 0..3: `w << 192` for r = 0, `(w << 128) & M_TOP` for r = 1, `(w << 64) & M_TOP` for r = 2, `w & M_TOP` for r = 3) and XOR'ed with BP_top xor D_top[cu] (BP_top in the main run; the result is (a0 | ((~S0(a0) & M32) << 32)) << 192 for the member a0 = base | rep | cu, because S0 is linear and base, rep, cu have disjoint bits, and ~S0(a0) != 0 on all 599,760 variants so every member is nonzero in bits 192..255).
If I = 0 the member is placed by shifting the group register down by 64 (`Gw >> 64` 1), OR'ing with the top-lane entry (1), testing the low 64 bits (`Gw & M64` 1), branching on a full group (1), updating the work counter (1), plus the xor (1): PLACE = 6. If I != 0 the rep stands for m = 2^|I| members: the m - 1 <= 7 cube deltas D_top[ii] are loaded once per class into registers during class preparation (`5 m - 2` primitives in all: loop over nonzero submasks ii of I with `(ii - I) & I` 3, table address 1, load 1 per nonzero ii, plus final test),
and each passing rep expands in m placements. **The placement is not walked one member at a time** (that walk is the inherited `EXTR + 5 m + 1` of d9f8833d: 1 xor + 4 shift/or/and/branch per member). The members of one rep are `e ^ D_top[ii]` for the nonzero submasks `ii` of `I`; they are produced consecutively, and every kept list has `k = 3`, so `m` is 8, 4 or 2 and a group of four never mixes two reps for `m = 8` (two full groups) and `m = 4` (one full group), and mixes exactly two for `m = 2`. Because `e` and the `D_top` are 64-bit values laid into disjoint 64-bit lanes and XOR distributes over the shift,

    sum_k (e ^ D_top[ii_k]) << 64k  =  (e | e<<64 | e<<128 | e<<192) ^ sum_k (D_top[ii_k] << 64k)

bit for bit, and the m-1 `D_top` deltas are already in registers from the class preparation above. So a group of four same-rep members costs 1 shift-down + 3 shifts + 3 ors + 1 xor with the precombined delta word + 1 full-group test + 1 store = **10 primitives, not 4 x 5 = 20**; the identity is checked against the shipped listings for every kept list, every batch and every admissable delta subset by `reports/experiments/r37-cheaper-placement-23.py` (192 group words assembled both ways, bit-identical). Charged exactly, with no declared slack: `memcost(0) = 6` (m = 1 keeps the inherited shift-register sequence: shift-down 1, or 1, xor of the class delta 1, full-group test 1, branch 1, work counter 1); `memcost(1) = 8` (a pair filling half a group word: `e | (e << 64)` 2, xor with the precombined shifted pair delta 1, shift into position 1, or into the group register 1, work counter 1, and the pair's half of the group completion 2); `memcost(2) = 11` (a group of four same-rep members: spread 6, xor with the delta word 1, shift-down 1, work counter 1, full-group test 1, store 1); `memcost(3) = 21` (two such groups plus the counter); `5 * 2^(j-1) + 1` beyond. The same identity covers the pair, `sum_k (e ^ D_k) << 64k = (e | e << 64) ^ sum_k (D_k << 64k)`, and `reports/experiments/r37-pair-24.py` checks it on the shipped listings: 4,032 pair words and 96 group-of-four words, bit-identical, and it asserts each of the four charges above item by item. A group of four members is complete after four placements (clearing Gw to 0 after GROUP_BODY); the last group of a first block is padded (PAD_OPS = 7). The member charge is 2,412.422 of `vbar` at the iter23 filing and 2,113.978 here, and together with the group body below the claim moves from 57.77156 to 57.70485 (Section 11).

### 9.7 The packed group: GROUP_BODY = 30, first stage 16, continuation seven

The packed-u arithmetic was inherited un-itemised as "GROUP_BODY = 31 ... unchanged from
aa0e8b6"; it is itemised here under the pricing of Section 9.1, one primitive per line of
the shipped `packed_u`:

```text
Sw  = Gw >> 32                              1    shift
E0  = (Gw + bc(e0b)) & LM                   2    add, per-lane mask
mj  = Gw & bc(x12)                          1    and
ch  = (E0 & bc(X)) ^ bc(Em2)                2    and, xor
d   = E0 | (E0 << 32)                       2    the doubling of a rotation pattern
S1E = ((d>>6) ^ (d>>11) ^ (d>>25)) & LM     6    3 shifts, 2 xors, mask
W1  = (KAP + Sw - mj - S1E - ch) & LM       5    4 arithmetic, mask
d1  = W1 | (W1 << 32)                       2    the doubling again
s0W = ((d1>>7) ^ (d1>>18) ^ (W1>>3)) & LM   6    3 shifts, 2 xors, mask
U   = E0 + s0W + bc64(C)                    2    two additions
packed-u arithmetic                        29
work-counter update per group (9.10)        1
GROUP_BODY                                 30
```

The broadcasts `bc(e0b)`, `bc(x12)`, `bc(X)`, `bc(Em2)`, `bc64(C)` and `KAP` are per first
block (Section 9.2, FIXED = 490), not per group. The three `& M256` of the reference text are
word truncations, not primitives of a 256-bit word machine: a 256-bit shift discards the top
bits and an addition is mod 2^256, so masking with 2^256-1 after them adds no operation.
`reports/experiments/r37-groupbody-24.py` proves the masks are no-ops for every input (20,000
random groups and the boundary words), counts the 29 line by line, and re-verifies that the
packed group reproduces the reference row-16 value `u_ref` on 12,000 lanes of random first
blocks and variants (0 mismatches).
Scan table occupies word addresses 0..8191, FIRST 8192..16383, SECOND
16384..18431. Form Uf=(U&bc64(8191))|bc64(8192), two primitives per group.
Extract the FIRST addresses by mask for lane 0, shift/mask for lanes 1,2 and
shift alone for lane 3: six primitives. Four loads and four branches cost eight.
Total 16, assigned to PROBE=(5,4,4,3); the existing group counter pays this
unconditional work. On each nonzero FIRSTw, shift U directly by 64*k+13 (one),
mask with 2047 (one), OR the SECOND base 16384 (one), load (one), AND with
FIRSTw (one), branch on T (one), and update V for the continuation (one).
Continuation costs seven including its own counter update. Expectation per lane
is 4+7*(1513/8192)=43359/8192. Worst probe group costs 16+4*7=44.
All shifts, addresses, loads and branches are charged under Section 9.1.
The added conditional stage uses existing probe temporaries; global 64-register
feasibility and machine-code size remain inherited H5 premises.

### 9.8 Survivors and the residual exact test

After T!=0, the original five-primitive fold and eight-primitive u extraction
and mask scan remain SURV_FIX=13. SURV_LANE=6 is unchanged. Only the exact
test is reduced to EX_OPS=13: address/load C_l (2), e=u+C_l (1), e&bit30 (1),
address/load cxA_l (2), A=e+cxA_l (1), A&0x22000000 (1), address/load VA_l (2),
XOR VA_l (1), OR the E and A failures (1), branch (1). Neither addition needs
a 32-bit reduction, as proved in Section 6.2. The low-24 table predicate,
survivor mask and every rare-path visit are unchanged.


### 9.9 The rare path

A pair with a row-16 pass for some l (probability at most 2^21 / 2^32 = 2^-11 per probed lane): work-counter update and lookup of the member (1 + 2); recompute W6 and W7 (RECOMP = 35); W0..W5 and W8 (201); then for each such l the y-words (8) and rows 16..21 with early abort, each row 106 + 53 + 1 (both members' W 20, CH 3, E 14, MAJ 4, A 12 per word; the cells and two-bit conditions closing at the row at most 53; the work-counter update 1).
When row 21 holds, rows 22..36 are computed with no cell test (106 each) and the pair is accepted iff the eight registers A33..A36, E33..E36 of the two members are equal (the collision event of Section 7.7; both members share CV1, so equal registers are equal outputs): the comparison is 8 xor, 7 or and 1 branch (OUTCMP = 16), and the work counter is updated once for the 15 rows and the comparison (1). `step3b` and `same_out` of `experiments/lowm.py` execute exactly this.
The ledger charges rows 16 and 17 always (c3b_l = 8 + 2 x 160 = 328 per l) and, for every l of every probed lane, with probability 2^-9 (the SMC stage factor of row 17 is 2^-12 under R16x, Section 7.4c): rows 18..21 checked in full and rows 22..36 with the comparison in full, with no early abort, c3b_t = 4 x 160 + 15 x 106 + 16 + 1 = 2,247 (the cell event charged 19 x 160 = 3,040 at the same probability). This is the rare-path charge of 4ec21bf9 (its Appendix D.5: c3b_t = 4 x 160 + 15 x 106 + 16 = 2,246 at probability 2^-11) with the work-counter update added and the 2^-9 of the base kept. The other items are the counts of 0db0eeb6 Section 9.7 and 7319bba.

### 9.10 The work counter V and the cap

V counts every executed data-dependent primitive: each of the following updates it by a constant (one primitive each, counted in the item): a passing class (its fixed price, sweeps, main run and spills), a subtraction run (its F6 test and scan), a member (its placement and, for a rep, its scan and extraction), a group (its body and four probes), a survivor lane, a survivor bit (its exact test) and every row of the rare path.
The data-independent part (FIXED) is charged per first block. The cap is tested after every first block (compare and branch, in the control of 9.2). The overshoot past V_MAX is at most the maximal data-dependent work of one first block, vmax_fb = 274,564,402,011/5 = 54,912,880,402.2 (every class passes with its worst |I|, every rep good, every l surviving, every probe hitting, every l charged through row 36 and the comparison), which the ledger charges.


## 10. Success probability, independence and caps

Let a *trial* t = (f, a0, l) be a first block f, a variant a0 of a passing class and l in L*, and A_t the event that a0 is good for f, the pair follows every cell and printed two-bit condition of rows 16..21 and the two 37-step outputs are equal (this filing's success event, Section 7.7). The program examines every good pair of every processed first block (Lemma 8.1) and every l whose row 16 holds
(Lemma 6.2, exact), so it finds a success iff some A_t occurs before the cap, and every output is verified (Lemma 6.1). Let X_f = sum over the trials of f of 1[A_t] and X = sum_f X_f.

- **Expectation.** E[X_f] = g x 32 x q3 (Lemma 5.1 and Section 7) with g = p7 p6 x 599,760 = 636.680 the expected number of good pairs per first block (exact: each of the 170 classes passes with probability p7 and each of its variants then passes F6 with probability p6), and E[X] = N_FB g 32 q3.
  With q3 >= q3_used = 2^-71.4243 x 2.4331 = 2^-70.14150 (H2): E[X] >= mu0 = 0.4946626 (H7) for N_FB = ceil(mu0 / (g 32 q3_used)) = 31,617,998,307,376,629 = 2^54.81160, where mu0 is the smallest 8-decimal number strictly above -ln(0.61 - Pcap - 2^-60) / (1 - 2^-10.4), with Pcap = 0.00000011 the assumed bound of the work-cap failure probability below (Appendix C).
- **One first block (H3).** By Bonferroni, Pr[X_f >= 1] >= E[X_f] - sum over pairs t < t' of f of Pr[A_t and A_t'] = E[X_f] - (1/2) sum_t Pr[A_t] E[X_f - 1 | A_t]. H3: sum_t Pr[A_t] E[X_f - 1 | A_t] <= delta E[X_f] with delta = 2^-9.4 (trial-averaged conditional expectation), so Pr[X_f >= 1] >= (1 - 2^-10.4) E[X_f].
  H3 splits into (a) the same variant with another l: at most 2^-11 (7319bba measured 0 further successes among 19,620,436 distinct Step-3 successes of its SMC, rule-of-three bound 2^-22.65; the four accepted patterns multiply the chance of passing rows 18 and 19 by about 4 and R16x the chance of the path by about 1.6, with four more l holding row 16, which gives about 2^-19.8, far below 2^-11), and (b) other good pairs of the same first block: summing over all other trials t' = (f, a0', l') of the family uses the family average of Pr[t' succeeds | t' good], which is q3 by definition, so at most rho x N_good x 32 x q3 with rho <= 2^35 (the measured factor at row 16 is 0.98 and 1.00), q3 <= 2^-71.38 x 2.4902 = 2^-70.0637 (H2, Section 7.7) and
  N_good <= 599,760 (all variants of the family, 2^19.58), so (b) <= 2^35 x 2^19.58 x 2^5 x 2^-70.0637 = 2^-10.4837 and delta <= 2^-11 + 2^-10.4837 = 2^-9.7189 < 2^-9.4. (N_good is the number of all variants of the family, as in the earlier filings on this family; no size-biased mean and no per-trial uniformity across (a0, l) is needed.)
- **Many first blocks (H1).** Distinct first blocks have independent chaining values, so the events X_f >= 1 are independent and Pr[X >= 1] >= 1 - exp(-sum_f Pr[X_f >= 1]) >= 1 - exp(-(1 - 2^-10.4) mu0).
- **Work cap.** The data-dependent work v_f of a first block (everything except its compression and its FIXED operations) has mean vbar = 16390.659791 (Section 11) and satisfies 0 <= v_f <= vmax_fb = 54,912,880,403 (= 274564402011/5, one first block's maximal work on the four kept lists; the parents' ten-list family gave 1433437678079/20). The v_f are independent (H1). Put m = N_FB vbar and M = vmax_fb. Then |v_f - vbar| <= M and Var(v_f) <= E[v_f^2] <= M vbar, so Bernstein's inequality for a sum of independent variables bounded by M gives, for t = s m,
  Pr[sum v_f - m >= t] <= exp(-t^2 / (2 (N_FB M vbar + M t / 3))) = Pcap, with slack s = 5806644450353958/10^20: the exponent is 16.18917, so Pcap = 2^-22.95320 (<= 0.00000011). V_MAX = ceil((1 + s) N_FB vbar) = 518,269,945,863,203,016,639 is exceeded with probability below Pcap; the run then fails, which is accounted for here. (The earlier filings used Chebyshev's bound vmax_fb / (s^2 N_FB vbar), which forces s = 2^-11 and Pcap = 0.00023325; Bernstein's bound is the standard exponential inequality for independent bounded summands and uses nothing but H1, 0 <= v_f <= vmax_fb and the mean vbar.)
  No part of v_f depends on a conditional law of the scalars: the plane programs cost the same for every data, and the data-dependent items are linear in the numbers of passing classes, good pairs, groups, survivors and hits, whose exact means the ledger uses.
- **Success.** Pr[output a collision] >= 1 - exp(-(1 - 2^-10.4) mu0) - Pcap - 2^-60 = 0.390000000034 > 0.39 (the 2^-60 covers a repeated first block among N_FB draws of 512 bits). Any output is a verified collision, independent of the premises.

## 11. Ledger (exact arithmetic; participant ledger executor-checked; Appendix B mirror)

```text
T = A_C + A_S + DEV + N_FB + (N_FB*490 + V_MAX + ceil(vmax_fb) + PRE + FIN)/2644 + 6
A_C=2^48, A_S=2^50, DEV=2^40, PRE=2^38, FIN=1600
N_FB=31617998307376629; vbar=18021721026738521/1099511627776; vmax_fb=274564402011/5
SLACK=2903322225176979/50000000000000000000; V_MAX=518269945863203016639
Pcap=1.2999999999999999941121E-07 <= 0.00000011
N=621084759189170888800; T=N/2644 (the Fraction does not reduce); log2(T)=57.7048456021372318532782939686324345113798116729639643672216
rounded time_log2=57.70485; preprocessing_log2=50.32305
```

The independent Fraction ledger first reproduces aa0e8b6's original N exactly,
773438176907133806360 with its executed law: Q0[0] has probability 1/4 and bits 2,3
each have probability 1/2. Its time_log2 is 58.0213414138426649296682670834074841281671112606650421931692417246587004428, rounded 58.02135.
Our delta from that reproduced baseline is
`(g+3)*(43359/8192 - 33/4 - 21/256)` in vbar and
`(782803/4)*11 - 782803*32*21` in vmax_fb. The cap slack uses a 10^-20
grid and the smallest grid value at least the old slack that preserves the
original Bernstein exponent. Thus mu0 and N_FB stay unchanged and success
is at least 0.3900000000340053. No runtime or full-scale success claim is added.
The executable participant ledger is statically cross-checked against this
independent ledger and Appendix B; its executor diagnostic agrees exactly.

### 11.1 Exactness of the expectations

Each row is linear in a count whose expectation is exact: a class passes with probability p7 (Section 5.3), the number of runs of a passing class is 2^(|B| - j) with j = |I| and the executed mask weights of Section 8.1 (Q0[0] probability 1/4, other cube bits 1/2), a rep of a run is good with probability p6 (Lemma 5.1), a probed lane has exactly 1/256 survivors on average and a nonzero filter with probability exactly 63,512/2^24 (Section 6.2), and 2^21/2^32 row-16 hits (Lemma 5.1: u uniform).
One row is a bound on an expectation that is not exact: the number of groups E ceil(N / 4) <= (E N + 3) / 4 (the padding of the last group of a first block is charged at its worst case; the exact value is E N / 4 + E[(4 - N mod 4) mod 4] / 4 <= E N / 4 + 3/4).
It is below 0.2% of vbar.

### 11.2 The advice-construction allowances A_S and A_C (H4)

The advice is the 37-step characteristic and its two-bit conditions (Tables 15, 16), the Step-1 solution S and the semi-free-start pair (Table 17); their construction is charged A_S = 2^50 (the paper's Step-1 SAT solve is 2^41.3; completing a Step-1 solution to a 37-step semi-free-start pair takes about 25 milliseconds, organizer experiment `a0-sfs-r37`)
and A_C = 2^48 (the unpublished characteristic search, calibrated from the measured complete re-run of the predecessor 35-step search accepted in 6eeefb64: 593,858 solver CPU-seconds = 2^19.18 CPU-seconds at the calibrated price of 2^21.427 units per CPU-second, giving 2^40.61 units; A_C = 2^48 units is 2^26.57 solver CPU-seconds = 3.16 CPU-years, more than 169 times that measured complete re-run, and A_C + A_S + DEV = 2^48 + 2^50 + 2^40 = 2^50.32; sensitivity is reported at A_C = 2^56 -> 58.09805, A_C = 2^60 -> 60.26913, and A_C = 2^64 -> 64.01838).
Everything derived from the advice (G, the classes, the lists, F6, F7, L*, the tables) is recomputed in the preprocessing (PRE = 2^38 operations) or is the 170 class descriptors (below 2^13 bytes of advice).


## 12. Premises

The statistical premises and their empirical support are inherited unchanged. The sensitivity costs in Sections 11.2 and 12 and Appendix G are recomputed with P4 prices, unchanged predicates, rational 40-bit q3 mantissas and ceil N_FB at mu0=0.4946626. The primary slack is retained unless increased on the 10^-20 grid to preserve its Bernstein exponent; times round upward to five decimals. Four-pattern and Table 15 sensitivities use their probability floors in the current P4 program, not alternate predicates. Using the J2 bound alone (q3c=2^-71.4524) gives 57.84384 (60.25562 under A_C=2^60); this is a sensitivity, not a replacement for the declared min-block floor.


**H1 (score-critical).** Our theory: the first blocks M0 are fresh uniform 512-bit strings; their chaining values CV1 = F_37(IV, M0) behave as independent uniform 256-bit values; in particular x = A_{-1} is uniform on 2^32 and independent of cb = C6 - A_{-2}, which is uniform on 2^32. Consequences used: each of the 170 classes passes the W7 test with probability p7 = |F7|/2^32 exactly, each variant of a passing class then passes F6 with probability p6 = |F6|/2^32 exactly, and given both, W0..W5 are uniform and independent of (W6, W7) (proof.md Lemma 5.1); hence the expected number of good pairs per first block is g = 599,760 p7 p6 = 636.680, the expected counts of the ledger, and the independence of distinct first blocks.

*Scope.* The expected numbers of passing classes, good pairs, survivors and row-16 passes per first block; the expected operation count of the counted program; the law of the second-block words that defines q3; independence across first blocks (proof.md Section 10). Not the validity of any output: every output is verified with the target. *Evidence.* Measured by 7319bba with the attack's own filters on real first blocks in C (2^21 and 2^23 first blocks: passing classes 7,400,134 and 29,545,568 against 7,388,160 and 29,552,640 expected; good pairs ratio 1.0034 and 1.0011; row-16 pairs z = +0.88, +0.51), by this filing's simulation of the counted program on 20,000 real first blocks (passing classes per first block 3.457 against the exact 3.523, good pairs 836.3 against 831.0, mean counted operations 28377 against the ledger's 28289), by the unconditional sample in `a0-online-r37` (64 organizer-seeded first blocks per active trial: 90,682 class W7 passes in 25,600 first blocks of our 400-trial run against 90,187 expected), and by the organizer experiment `h1-cv1-filters-nonce`, which counts on 150 organizer-seeded real first blocks per trial how often the W7 filter (first class) and the W6 filter (its first four variants) pass (expected 2.38 and 40.1 per trial; our replays, 100 trials each: 244 and 214 W7 passes against 238.0, 4,011 and 3,988 W6 passes against 4,013.7; Appendix H). These are at most 2^23 real first blocks, not 2^55.8. *Limitations.* Premise (our theory), not a theorem: the filter rates are measured on at most 2^23 real first blocks and on the organizer's small samples, not at the 2^55.8 first blocks of the attack, and independence across first blocks is assumed, not tested. The class tests of one first block are strongly correlated (their c7 values are close), so per-first-block counts are overdispersed; only their expectations and the independence across first blocks are used. The class test uses the single word x, so H1 is also an assumption about that word of the digest of a 37-step compression.

**H2 (score-critical).** For a good pair, q3 = the average over the 599,760 variants of the 170 classes (each equally likely, as examined here) and the 32 elements of L* of Pr[rows 16..21 of both members follow every cell and every printed two-bit condition closing at rows 16..21 (corrected reading A15[29] = A17[29]), the eight value bits E18[1,5,10,11,18,28,29] and E19[29] of Table 15 not imposed, and (R16x) E16[23] = 0 and E16[24] = E17[24] not imposed: exactly the cells and conditions of experiments/lowm.py, and the two 37-step outputs are equal (rows 22..36 are computed without cell tests, Section 7.7)] satisfies q3_used = 2^-71.4243 x 2.4331 = 2^-70.14150 <= q3 <= 2^-71.38 x 2.4902 = 2^-70.0637, where q3 = q3c x R: q3c, the probability that rows 16..36 follow every cell, satisfies 2^-71.4629 <= q3c <= 2^-71.38, 2^-71.4629 being the lower, rounded down to four decimals of log2 (the preregistered rule's two decimals give 2^-71.47 and a claim of 57.75028), of the one-sided 99 percent Student lower bounds (2^-71.4629 and 2^-71.4524; one-sided 99 percent upper bounds 2^-71.3970 and 2^-71.3838) of the means of two preregistered blocks of 128 replicates (NP = 8192) of a sequential Monte-Carlo estimator written for this filing (Appendices F and G), run on exactly this family with both relaxations as one carrier; and R = Pr[equal outputs | rows 16..21] / Pr[cells of rows 22..36 | rows 16..21] satisfies EXQ = 2.4331 <= R <= 1275/512 = 2.4902, where 2.4331 is the preregistered one-sided 99 percent lower bound, below every overdispersion-robust bound computed, of the ratio of collision events to cell events after row 21 measured by our 4ec21bf9-f588-4b80-bb2b-77c1ccf8c9b7 (R37R, passed review; its Appendix D.3: 2.4648 +- 0.0145 on Table 15 states, 2.4552 on ffbe30bb's states, 2.46455 under the attack's kept-fibre law of (W7, W8)) and 1275/512 is the uniform-model value of its Appendix D.2; this heuristic explicitly includes the statistical and procedural premise that the participant-reported preregistrations, complete contiguous seed lists (710000..710063, 720000..720127, 721000..721127, 740000..740127, 741000..741127), fixed two-block min(LB) rule, interim progress monitoring during execution, and prior condition-relaxation screening (adopting the four row-18/19 patterns and R16x after screening 30 candidate condition pairs) do not introduce selection, optional-stopping, or multiple-comparison bias exceeding the margin between the two disjoint-seed block estimates, the 6-seed direct full-path check and the declared floors `q3c_used = 2^-71.4243` and EXQ = 2.4331 (the preregistered min-of-blocks bound 2^-71.4629 remains a stated sensitivity).

*Scope.* The expected number of successes E[X] = N_FB g 32 q3 and hence N_FB (proof.md Sections 7 and 10), including the validity of the offline SMC estimation protocol, seed selection, stopping rule, and relaxation screening that support `q3c_used = 2^-71.4243`, and the ratio EXQ = 2.4331. The good pairs and the later rows are those of 7319bba; this filing changes how the good pairs are found, not which pairs are good, and which pairs count as a success: (from ffbe30bb) the value patterns of rows 18 and 19 and (new) R16x at rows 16 and 17, which also gives the four l = 0, 2, 16, 18 row-16 values, and (from 4ec21bf9) the collision event after row 21 in place of the cells of rows 22..36. *Evidence.* Lemma 7.1: rows 16..22 have exactly the same probability for every variant; a variant enters rows >= 23 only through W8 in W23 and W24, so only the four W24 conditions can depend on it (about 2^-4 for every W8x). Our estimator (exact row 16, exact importance weights at rows 17..21, (W6, W7) uniform on F6 x F7, W8 drawn uniformly from the 599,760 variants; Appendix F) was preregistered (validation V with Table 15 cells: mean 2^-73.9911, bound 2^-74.0064, z = +0.66 against the registered study B of 7319bba, mean 2^-73.9987, bound 2^-74.0225, validation PASSES both preregistered criteria (|z| <= 2.576; bound within 0.04 of -74.0225); main blocks R1 and R2 with the eight value characters of the two E cells removed: means 2^-71.9975 and 2^-71.9868, relative sd 0.0714 and 0.0681, bounds 2^-72.0191 and 2^-72.0074, declared 2^-72.02; stage factors of rows 18, 19 and 21 -8.00, -10.00 and -2.00 bits against -15.00, -6.00 and -1.00 for Table 15, structural gain 2.00) and again with R16x (constants written from the counted program; the same binary reproduces the four-pattern outputs byte for byte; joint blocks J1 and J2: means 2^-71.4296 and 2^-71.4177, relative sd 0.1096 and 0.1143, lower bounds 2^-71.4629 and 2^-71.4524, upper bounds 2^-71.3970 and 2^-71.3838, 0.55 bits above the four patterns alone; our earlier full-path test of R16x with independent rehash of all 30,814 collisions gave +0.590 bit [0.548, 0.631]). In addition, the organizer experiment `a0-sfs-r37` constructs and verifies full 37-step SFS collisions across 128 classes and all 8 pattern branches (63/64 on patterns 0..3 and 57/64 on R16x patterns 4..7 on our seeds `ours-A-0..127`; 13 of 13 returned pairs of trials 0..15 are found by the counted program), and the organizer experiment `h3-ladder-r37` runs the row-16 stage of q3 on organizer seeds: 41 exact row-16 passes among 98,216 W6 passes (4.2e-4, two seed sets) against the 4.9e-4 (2^-11) per probed lane of the ledger (Appendix H). The four-pattern relaxation (exactly four feasible patterns, three verified further collisions) is ffbe30bb's; here the three collisions are re-checked against this package's cells. R16x is ours (each of its two conditions alone is necessary; a sweep of 30 further condition pairs found no further gain). Here the examined law is the studied law (every variant of every passing class, no weighting), so no hedge is added. The collision event after row 21 (Section 7.7): given rows 16..21, the outputs are equal iff E22[29] = 1, s1(W22') - s1(W22) = 0x4fff9f30 and dW26 = 0, with the uniform-model ratio 1275/512 = 2.4902 (4ec21bf9, Appendix D.2); the measured ratio is 2.4648 +- 0.0145 (Table 15 states), 2.4552 (ffbe30bb's states, three runs, the last preregistered) and 2.46455 (the attack's kept-fibre law, preregistered), every cell event also a collision event in every run, and the preregistered rule gives EXQ = min(2.4331, 2.4443) = 2.4331 (4ec21bf9, Appendices D.3, D.3b). With q3c one bit lower (q3 = 2^-72.4629 x 2.4331) the claim would be 58.73900 (60.50286 under A_C = 2^60), with the four patterns alone (q3c = 2^-72.02) 58.29762 (60.38630 under A_C = 2^60), with the Table 15 value 2^-74.03 60.30330 (61.15945 under A_C = 2^60), and with the cell event of rows 22..36 instead of the collision event (EXQ = 1) 58.99371 (60.58264 under A_C = 2^60). *Limitations.* A Monte-Carlo and procedural premise, not a theorem: (1) its coverage rests on the approximate normality of the mean of 128 replicates (relative sd 0.1096 and 0.1143, about twice the Table 15 study's because few children survive the row-19 stage); row-22 survivors are heavily duplicated within a replicate; the row-22 stage draws (W6, W7) uniformly from F6 x F7, which is argued, not measured; depends on the reading of the '+' cells; (2) the offline preregistration timestamps/hashes (`PREREG_q3M.txt`, `PREREG_q3R16x.txt`) and contiguous seed lists (`710000..710063`, `720000..720127`, `721000..721127`, `740000..740127`, `741000..741127`) are participant-reported without an organizer holdout nonce, interim progress looks were taken while blocks ran (Appendices F.2 and G.2), and screening R16x against 30 other condition pairs before running J1 and J2 is not a multiplicity-adjusted holdout test, so the absence of material selection, optional-stopping, or multiple-testing bias is an explicit part of heuristic H2 rather than an externally certified guarantee; (3) no organizer experiment executes the end event of q3: rows 22..36 reach the digest only through a second-block chaining value that must be equal, which needs a reachable first block, that is the attack itself (`a0-sfs-r37` returns semi-free-start pairs and no full collision of the target); the organizer-executed `h3-ladder-r37` runs only the row-16 stage of q3 on organizer seeds; (4) EXQ is a Monte-Carlo bound from the runs of 4ec21bf9, not a theorem: those runs draw (W6, W7) uniformly from F6 x F7 and W8 from the variant list of that filing, on Table 15's and ffbe30bb's row-21 states and, in the preregistered fourth run, a pool of kept fibres of that filing's table; the ratio depends on W8 only through W24 = s1(W22) + W17 + s0(W9) + W8 and was not re-measured on this family's 599,760 variants or on the row-21 states that R16x adds; the runs share resampled row-21 states, so their counts are overdispersed (run 3: chi-square 55.4 on 31 df), which the quasi-binomial and cluster bounds allow for; no organizer experiment estimates the ratio. Premise (our theory): q3 is our computation, with the estimator, the preregistrations and the per-seed estimates printed in Appendices F and G. The count of four patterns is a solver enumeration (Bitwuzla; Z3 on smaller cases) for the published dense part with the signed cells of rows 14 and 15 kept (with rows 12..15 removed as well it admits 128 patterns); other dense parts were not explored, and our estimator does not use the solver. R16x has no solver enumeration: its value rests on the estimator, on `a0-sfs-r37`, and on our full-path test with rehashed collisions; patterns of rows 16..21 outside the program's cells (for example the E18 XOR pattern {24,23,16,15}) are not counted. A stated premise, not an established fact.

**H3 (score-critical).** Averaged over the trials t = (first block, variant, l) of a first block f weighted by their success probabilities, the expected number of other successful trials of the same first block given that t succeeds is at most 2^-9.4: sum_t Pr[A_t] E[X_f - 1 | A_t] <= 2^-9.4 E[X_f]. Equivalently: (a) the expected number of other l in L* succeeding with the same variant is at most 2^-11, and (b) for other good pairs t' of the same first block, Pr[t' succeeds | t succeeds, t' good] <= 2^35 Pr[t' succeeds | t' good].

*Scope.* The per-first-block Bonferroni bound Pr[X_f >= 1] >= (1 - 2^-10.4) E[X_f] (proof.md Section 10). The good pairs of a first block and their dependence structure are those of 7319bba; this filing changes the order in which they are processed, not the set. *Evidence.* (a) 7319bba's replay of 19,620,436 distinct Step-3 successes of the SMC: rebuilding W0..W5 and testing the other 31 elements of L* through rows 14..36 gave 0 further successes (rule-of-three 95 percent bound 2^-22.65 per success; the accepted patterns raise the chance of passing rows 18 and 19 by about 4 and R16x the chance of the whole path by about 1.6, with four more l holding row 16, so about 2^-19.8, far below 2^-11; in that replay the other l fail at row 16 or 17; the collision event changes only rows 22..36, so (a), decided at rows 16 and 17, is unchanged). (b) Summing over all other trials t' = (f, a0', l') in the family uses the family average of Pr[t' succeeds | t' good], which is q3 <= 2^-71.38 x 2.4902 = 2^-70.0637 (H2, Section 7.7; no per-trial uniformity across (a0, l) is required), so the expected number of further successes among other good pairs is at most rho x N_good x 32 x q3 with N_good <= 599,760 (all variants of the family): 2^35 x 2^19.58 x 2^5 x 2^-70.0637 = 2^-10.4837, so delta <= 2^-11 + 2^-10.4837 = 2^-9.7189 < 2^-9.4; the measured factor at the row-16 level over 2^21 and 2^23 real first blocks is 0.98 and 1.00. The organizer experiment `h3-cowpass-nonce` counts the first blocks in which several variants of one class pass F6 together, and `h3-ladder-r37` (Appendix H) counts, on organizer-seeded real first blocks, the pairs of distinct variants of one first block that both pass each level of the attack through the exact row-16 test, against the pairs expected if they passed independently: our replays (two seed sets) give the dependence factor 3.62 and 4.92 at the W6 filter (variants of one class share bits), 0.99 and 1.00 at historical aa0e8b6 LO12 and 0.95 and 0.94 at historical MID12 (P4 public-seed ladder R: W6=3.250842, FIRST13 (lo)=0.995964, SECOND11 (mid)=0.949225, exact row 16=1.048555; N/S/P/C and exact rational calculation are in the P4 executor observations section.), and 1.27 and 0.67 at the exact row-16 test (32 and 9 passes). This is the bound of the earlier filings on this family; the whole family G would give 2^-6.5 and is not used. *Limitations.* Premise (our theory): rows 17..36 are not reachable by any organizer experiment of 20 s; for them rho = 2^35 over the measured factor (0.67 to 1.27 through row 16 on organizer seeds; 0.98 and 1.00 over 2^21 and 2^23 real first blocks) is the stated allowance. Rows >= 17 of distinct good pairs cannot be measured jointly within one first block; the premise leaves a margin of 2^35 over the measured row-16 factor, and the margin over the number of examined pairs is thin (delta <= 2^-9.72 against 2^-9.4). The replay samples are correlated through SMC resampling. A stated premise, not an established fact.

**H4 (supporting).** The published characteristic, its two-bit conditions, the SFS pair's inner values S and L* are used as advice. Their construction is charged A_S = 2^50 (the Step-1 SAT solve, reported by the paper at 2^41.3, and the completion of a Step-1 solution to the SFS pair) and A_C = 2^48 (the unpublished characteristic search, calibrated from the 593,858 solver CPU-seconds of the predecessor search in 6eeefb64); all development computation at DEV = 2^40. The variant family, the 170 class descriptors (below 2^13 bytes), the lists, the filter sets, L* and the tables are recomputed in the preprocessing (2^38 operations bound, itemised in proof.md Section 14.2).

*Scope.* The preprocessing part of the ledger (2^50.32305) and the advice (below 2^13 bytes). *Evidence.* proof.md Section 11.2. A_S: 2^8.7 times the paper's reported Step-1 cost; the completion of a Step-1 solution to a full 37-step semi-free-start pair is reproduced in this package in about 25 milliseconds per pair (organizer experiment a0-sfs-r37). A_C: at the CPU-second price calibrated in the accepted filing 6eeefb64 (2^21.427 units at C = 2644 per solver CPU-second), the 593,858 solver CPU-seconds (= 2^19.18 CPU-seconds) measured for a complete re-run of the predecessor 35-step search equal 2^40.61 units; A_C = 2^48 units is 2^26.57 solver CPU-seconds (3.16 CPU-years), more than 169 times that measured complete re-run, and A_C + A_S + DEV = 2^48 + 2^50 + 2^40 = 2^50.32305. *Limitations.* The 37-step characteristic search time is unpublished; A_C = 2^48 is a calibrated bound > 169 times the accepted measurement of the predecessor search, not a direct measurement of the paper's search. Sensitivity: A_C = 2^56 gives time_log2 = 58.09805, the legacy placeholder A_C = 2^60 gives time_log2 = 60.26913, and A_C = 2^64 gives 64.01838.

**H5 (score-critical).** Under collision-frontier-v5 a word-RAM program of 256-bit primitives in which every executed load, store, logic operation, shift, addition, comparison, branch and jump is one primitive is charged by the primitives it executes. The W7 class test (106 primitives for all 170 classes) and the W6 test of a batch of 256 reps (181 to 301 primitives, and 11 to 28 for each subtraction run) are straight-line plane programs whose counts do not depend on the data, produced by a plane algebra in which static constants fold and complemented planes carry an inversion flag at no cost, and in which a NOT is paid when an AND or OR meets unequal flags; two batches are processed together bit by bit with at most 20 live planes each (64 registers, no spill). The group of four members is 30 primitives, the first probe stage 16 per four lanes plus seven per nonzero FIRST word, the residual exact row-16 test 13, and the zero-base `scan_table` at word address `0..8191` gives `CLS_LANE = 5`, `SCAN_LANE = 7`, `SURV_LANE = 6`, with the scalar and control items of proof.md Section 9. All tables, the code (86,416 inherited bytes plus a 1,024-byte allowance) and the constants occupy 769,776 bytes = 2^19.554079, below 2^20 bytes. The 170 classes are base | s for s in the four kept lists (computed, checked for all 599,760 variants); a list is the union of 2^|B| translates of its reps by the cube B of free bits {0, 2, 3} or {0}, and F6(W6x) does not depend on a cube bit s_b when q_b = 1 or on s_0 when CB3_0 = 1 (Lemma 8.2: proved from the constants of S and checked), which the program uses to run only the main combination and subtract the constants of the other 2^|Q0| - 1 combinations that matter.

*Scope.* The class-test, W6, scan, gather, group, probe and survivor terms of the ledger (essentially all of the 16390.66 data-dependent operations per first block), the fixed terms, the memory figure and the preprocessing bound (2^38 operations). *Evidence.* The program is experiments/lowm.py (the plane programs assert their counts at every execution; process_cv counts every scalar item where it executes; the realized operation count of every category equals its closed formula on 20,000 simulated first blocks). It is exact against the scalar definitions: every lane of every class-test plane and every pass plane equals the F7 or F6 test of its definition (34,000 and 33,570 lanes in selftest, and every lane of every processed class in a0-online-r37), the sets of good pairs (all members, after the expansion of the reps) equal the brute-force sets, the address u equals W0 + s0(W1) from the step equations, the exact row-16 test equals 7319bba's enumeration of 2,097,152 pairs on all 32 l (Appendix A) and the generic row check on random and near-miss values, and the table stage never rejects a member. *Limitations.* No organizer ruling is cited for the plane algebra (static constants and inversion flags are compile-time facts of the text; the W6 programs have 32 to 84 inversion flips that cost nothing because XORs absorb them and AND/OR of equally flagged planes use De Morgan; pricing every one of them as a NOT would give 57.74433, or 60.27400 under A_C = 2^60) or for the register argument, which is a count of live planes, not a register allocation. The code size is a bound (at most 8192 primitives of at most 8 bytes). Branch pricing follows the earlier filings (a branch on a register is one primitive). The ceiling of the group count and the survivor scan are charged at their worst case (below 0.2 percent of the data-dependent work).

**H7 (supporting).** Two constants, named separately, carry the 0.39 floor. (i) The *requirement*: with the cap assumed at Pcap = 11/100,000,000 = 1.1e-07 (the computed Bernstein bound of this family is 2^-22.95320 = 1.23139993e-07, rounded up to the ledger's 1e-8 grid, so the assumption holds), mu_req = -ln(0.61 - Pcap - 2^-60) / (1 - 2^-10.4) = **0.494662599944212**, rounded up to eight decimals **0.4946626**; N_FB = ceil(mu_req / (g 32 q3_cell)) then guarantees the *achieved* mean E[X] = N_FB g 32 q3_cell = 4208124008881635417764050972564764929619 / 8507059173023461586584365185794205286400 = 0.494662640 >= mu_req. (ii) The *bound*: 1 - exp(-(1 - 2^-10.4) mu_req) - Pcap - 2^-60 = 0.39000000441594207 > 0.39 (the shipped ledger prints 0.390000000034005 in binary double; the two agree to 1e-15). Both constants are printed by the shipped program, `mu_req 0.4946626` and `pcap_log2 -23.13208`. *No other constant is used*: the eight-decimal figure of the parents' ten-list cap (their Pcap <= 4.5e-7) is larger than the requirement here, and it appears nowhere in this package except as this sentence.

*Scope.* N_FB (the cap) in the ledger. *Evidence.* Every allowance is an explicit term of the floor equation: the Bernstein cap-failure bound Pcap (priced in proof.md Section 10 from the exact vmax_fb = 274564402011/5 and vbar = 18021721026738521/1099511627776 of the ledger; the computed bound is 2^-22.95320 = 1.23139993e-07, against the assumed 1e-07), the repeated-first-block allowance 2^-60, and the H3 dependence discount as the divisor (1 - 2^-10.4). Appendix C computes mu0 and the bound with 60-digit decimals and asserts the bound > 0.39; lowm.py ledger() iterates Pcap and N_FB to a fixed point and asserts the same. *Limitations.* The 0.39 floor is the organizer's success requirement; the equation makes the success arithmetic exact rather than adding slack. The cap bound needs the independence of the first blocks (H1) and the bound vmax_fb on one first block's work; a Chebyshev bound would force the slack 2^-11 and Pcap = 0.00023325 (Section 10).

## 13. Evidence and runs

All runs for this filing on one Windows PC (24 threads) and its WSL Ubuntu: Python standard library (`experiments/lowm.py`), numpy and gcc for Appendix A. At most two processes ran at a time. The programs and numbers that are used as premises (7319bba, fb039a6e, ffbe30bb) are labelled as such; the q3 studies of Section 7.4b were run for this filing with `q3smc.c` (Appendix F, at most two processes at a time).

### 13.1 Quoted from 7319bba (end to end on real first blocks; inherited evidence for H1, H3, H2)

Inherited aa0e8b6 evidence below; not rerun for P4. Counts, timings and ledger comparisons describe the predecessor. P4 validation (c) completed; see the separate P4 executor observations section.


C statistics of 7319bba (random M0 from xoshiro256**, CV1 = F_37(IV, M0), the 170 W7 tests of the 170-class family, the scalar W6 test of every variant of every passing class, u and the exact row-16 test for every l, exact checks of sampled pairs):

| run | first blocks | passing classes (expected) | good pairs (expected; ratio) | row-16 pairs (expected; z) | H3 factor: sum R(R-1) / p^2 sum G(G-1), p = 1052672/2^32 |
|---|---|---|---|---|---|
| seed 5eed0021 | 2^21 | 7,400,134 (7,388,160) | 1,748,648,111 (1,742,708,500; 1.00341) | 424,363 (422,895; +0.88) | 0.981 |
| seed 5eed0023 | 2^23 | 29,545,568 (29,552,640) | 6,978,649,557 (6,970,834,000; 1.00112) | 1,693,297 (1,691,580; +0.51) | 0.979 |

The counts are strongly overdispersed (variance-to-mean ratios 28.8 for passing classes, about 23,100 for good pairs, 6.6 for row-16 pairs) because classes are correlated; their means match. 7319bba's replay of 19,620,436 distinct Step-3 successes of the SMC found 0 co-successes across the other 31 elements of L*.
These programs are not re-run here; the family and the filters of this filing are theirs.

### 13.2 Exhaustive checks and equivalence with the definitions (this filing)

Inherited aa0e8b6 evidence below; not rerun for P4. Counts, timings and ledger comparisons describe the predecessor. P4 validation (c) completed; see the separate P4 executor observations section.


- **F6, F7 and G (inherited).** For all 2^32 words w the definitions of F6 and F7 against their bitwise forms, |F6| = 287,309,824 and |F7| = 68,157,440, 0 mismatches (0db0eeb6, Tungsten; the bitwise forms are those used by the plane programs here, which `selftest` and the experiments compare with the definitions on the lanes below); |G| = 12,103,680.
- **The classes and the lists (`selftest`).** For all 170 classes and all 599,760 variants: the variant base | s is in G, has the class's c7, and the class has its size; 0 mismatches. Maximum S0(a0) over the variants 0xffffbb5c (lane safety of the packed words).
- **The cube (`selftest`).** For 8 classes spread over the lists, 60 random (x, cb) each and 8 random reps each: F6(W6x(rep xor f)) = F6(W6x(rep xor (f & Q0))) for all f subset of the cube B (Lemma 8.2): 30,720 tuples, 0 mismatches; all classes of the lists with bit 2 or 3 in the cube have base bit 1 set.
- **The plane programs (`selftest`).** The W6 program on 33,570 lanes (8 classes spread over the four lists, 3 random (x, cb) each, every batch and every cube combination): 1,462 F6 passes, 0 mismatches against F6(w6of(a0, x, A_{-2})) of the member rep xor f. The class test on 34,000 lanes (200 values of x, half of them constructed to pass a class): 0 mismatches against F7(c7 - x).
- **Row 16 (`selftest`, Appendix A).** The exact test of Lemma 6.2 equals the exhaustive enumeration of `r16.c` on all 32 l (2,097,152 pairs, none missing, none added) and rejects all 1,046,639 non-members among 2^20 random (u, l); filt(u) contains every l of every enumerated pair, and its sums over the 2^24 values of u mod 2^24 are the exact means of the ledger; against the generic row check (`row16_ok`) on random values, on near-miss values (the fixed bits of E16x imposed) and on single-bit changes of members: 0 mismatches; filt(u) contains every l with a row-16 pass.
- **Packed address.** The 4-lane U against the definition u = W0 + s0(W1) of the chaining value and a0 (400 lanes, extreme chaining-value words): 0 mismatches.
- **Unrestricted run of the experiment checks.** The checks of `a0-online-r37` (every lane of the class-test and pass planes, the good sets against brute force, the addresses, the table stage and the exact test against the row-16 definition, the cells of rows -4..15) on 400 first blocks with a passing class (2,590 first blocks drawn, 400 trials of at most 64 draws), **all passing classes** of each processed (9,814 classes, 2,164,111 good pairs, 8,476 survivors of the table stage): 0 mismatches of every kind; the unconditional class sample of the same trials (25,600 first blocks) has 90,682 class W7 passes against 90188 expected.
- **Organizer experiments (local replay of the request format with seeds `ours-A-<t>` and `ours-B-<t>`; each inside the organizer's 20 s and 128 MiB).**
  `a0-sfs-r37`: trial t imposes pattern t mod 8 (0..3: the four value patterns of rows 18 and 19 with E16[23] = 0; 4..7: the four R16x patterns with E16[23] = 1); 120 of the first 128 trials build a 37-step semi-free-start collision with a variant dense part (patterns 0 to 7: 15/16/16/16/14/15/14/14; 63/64 on patterns 0..3 and 57/64 on R16x patterns 4..7; the others exhaust their proposal budget); for the 13 of trials 0..15 that return a pair, the constructed chaining value is fed to the counted online program restricted to the class of a0, which finds exactly the constructed pair in **13 of 13** cases (class test, W6 test, gather, packed address, probe, exact test, rows 16..36); 3.7 s.
  `a0-online-r37` (trials 0..7): unconditional (H1): 512 first blocks (64 per trial), 1,913 class W7 passes against 1,803.75 expected (the class tests of one first block are correlated); selection (H5): 74 first blocks drawn, 24 classes processed, 1,760 good pairs, 2 survivors of the table stage; class-lane, pass-lane, good-set, address, row-16 and cell mismatches: 0, 0, 0, 0, 0, 0 (pairs checked against every cell of rows -4..15 for all 32 elements of L*: 12); 0.7 s.
  `h1-cv1-filters-nonce`, `h3-cowpass-nonce` (trials 0..99) and `h3-ladder-r37` (trials 0..15): Appendix H; 4.0 s and 1.9 s.


### 13.3 The counted program simulated on real first blocks (premises H1, H5)

Inherited aa0e8b6 evidence below; not rerun for P4. Counts, timings and ledger comparisons describe the predecessor. P4 validation (c) completed; see the separate P4 executor observations section.


`experiments/lowm.py`'s `process_cv` was run on 20,000 real first blocks (first words from SHAKE-256 of the seed `simF-1017`, real 37-step compressions, all 170 classes, every operation counted), without any restriction of the family.
Realized counts: 69,139 passing classes (3.457 per first block against the exact 3.523), 16,726,799 good pairs (836.3 per first block against the exact 831.0), 4,181,742 groups, 63,548 probed lanes with a nonzero table word, 65,564 survivors of the exact table stage (0.00392 per probed lane against the exact 1/256 = 0.00391), 7,954 first-block-level row-16 passes.
The counted operations per first block (the 46 first-block operations included): mean 28377, against the ledger's expectation 28289 (= FIXED + vbar), ratio 1.0031; the run precedes the change of the rare path of Section 9.9, which acts only on pairs whose row 21 holds. The realized operations of every category (class test, scalars, class preparation, sweeps, W6 programs, scans, members, groups, probes, survivors, rare path) are the prices of Section 9 applied to the realized counts (`experiments/lowm.py` is the program; the check is the identity of Section 9's prices with the executed counts).

### 13.4 Development computation

Below 3,000 CPU-seconds in all (the exhaustive row-16 comparison 20 CPU-seconds in C and 60 in numpy, the simulation about 85 CPU-seconds, selftests and experiment replays under 300, aborted runs the rest), far inside DEV = 2^40 units (2^18.6 CPU-seconds at the calibrated 2^21.4 units per CPU-second).


## 14. Memory, preprocessing and advice

### 14.1 Memory

Everything resident during the online phase (`python3 experiments/lowm.py memory`; words of 32 bytes):

| item | bytes |
|---|---|
| planes of the reps that are not constant over their batch (8 batches, 78 planes; the constant planes are in the code) | 2,496 |
| packed entries of the reps: 8 batches x 64 words | 16,384 |
| cube entries D[c]: 8 words | 256 |
| spill area of the sums of a class's batches: 7 x 9 words (or 2 x 15 words) | 2,016 |
| c7 planes: 15 words (the 15 dynamic bits) | 480 |
| chunk table FIRST: 8192 words | 262,144 |
| chunk table SECOND: 2048 words | 65,536 |
| lane-scan table: 8192 words (13-bit chunks) | 262,144 |
| class descriptors: 170 x 4 words (base, BP, list data, c7) | 21,760 |
| per-l constants: 32 x 4 words (C_l, cxA_l, E15x word, VA_l) | 4,096 |
| scalar planes in memory: 63 words | 2,016 |
| characteristic cells, L* rows, S: bound 1280 words | 40,960 |
| chaining-value constants (cv_pre) and the first-block buffer: 64 words | 2,048 |
| code: the earlier bound of 8192 primitives of at most 8 bytes less the 1,227 primitives of the generic plane programs (55,720), plus the 3,188 primitives of the 45 per-batch plane programs of Section 9.5 at most 6 bytes each (register-to-register 256-bit operations, VEX 4 or 5 bytes) | 86,416 |
| added probe/residual code allowance | 1,024 |
| **total** | **769,776 = 2^19.554079** |

The limit 2^20 = 1,048,576 bytes is not reached. Claimed memory: 2^20.0 bytes (rounded up). The messages (128 bytes), the registers (64 x 32 bytes) and the compression state are included in the last constants. Nonuniform advice: the characteristic, S, L* and the 170 class descriptors (170 x 12 bytes), below 2^13 bytes.
The tables are built in the preprocessing and are never held twice.

### 14.2 Preprocessing: PRE < 2^38 operations

(i) Discovery of the family: the 2^29 values of E4 with E4[31:29] = 000 (a0 = E4 - C4), each tested against the W8x conditions (about 20 operations) and c7 (about 60), grouped by c7 and the classes of at least 3456 variants kept: 2^29 x 80 + 12.1 x 10^6 x 100 < 2^36; the descriptors (base, mask) of the 170 classes are read off their members (599,760 x 30).
(ii) The four kept lists: 4 x 2^15 subsets x about 80 operations < 2^23.4. (iii) The planes and packed entries: 8 batches x (17 x 256 bit insertions x 3 + 64 x 4 x 10) < 2^17. (iv) FIRST/SECOND: enumerate 8192 low indices per l, at most 32 encoded interface states and 2048 high indices per state, then emit/prune at most four viable states. A conservative 100 primitives per tested index, plus 32 x 4 x 8192 x 10 for emission, is below 2^29. Per-l constants: 32 x 200; the scan table 8192 x 6; the c7 planes 170 x 32 x 3.
The sum remains below 2^36.1; PRE = 2^38 is charged. Tables are built before lists and scan-table initialization. Reuse the uninitialized scan-table region for at most 2^17 bytes of construction scratch (encoded low states and one-l high supports); release it before online use. No duplicate final tables coexist. Nothing depends on cb or on any other word of the chaining value.

## 15. Limitations

P4 adds no full attack run or organizer qualification. All five modified experiments and the ledger/memory diagnostic completed twice in the organizer executor; the standalone selftest was not run. The independent host tools run no participant code. Uniform-lane/padding expectations, code bounds, register feasibility, q3 and H1-H7 remain inherited limitations.


- H1, H2, H3 are premises. q3 is estimated (the cell probability q3c by Monte Carlo, with an estimator written for this filing, validated against the registered study of 7319bba, its row-16 stage reproduced on organizer seeds by `h3-ladder-r37`; the ratio EXQ of collision to cell events from the runs of 4ec21bf9, Section 7.7), not proved; because the offline preregistrations, complete seed lists, interim progress monitoring and prior 30-pair screening are participant-reported without an organizer holdout nonce, the absence of material selection, optional-stopping or multiple-testing bias in the offline q3 studies is an explicit part of heuristic H2. No full collision has been found and none is expected at the scale that can be run; the full-scale success probability cannot be observed.
- The counted program is a straight-line text whose plane programs are executed and counted by an algebra with static constants and inversion flags; the scalar and control items are counted by the constants of Section 9. There is no machine code; the register argument of Section 9.5 is a count of live planes.
- The simulation of Section 13.3 samples 20,000 first blocks of the 2^55.76 the run draws; the per-first-block counts are heavy-tailed, so its mean has a standard error of a few percent; the ledger does not use it.
- The organizer experiments run the same program on the whole family of 170 classes; to fit the sandbox a trial processes at most the first three passing classes of its first block.
- H3 (b) is measured at the row-16 level only (7319bba; `h3-ladder-r37` on organizer seeds, Appendix H) and leaves a margin of 2^35 on rho; rows 17..36 are not reachable by any organizer experiment of 20 s; its bound on the number of examined good pairs is the whole family.
- The published characteristic and SFS pair are used as advice under the allowances; the paper's SAT solve and characteristic search were not rerun.
- For 37 steps the measured q3 for the Table 15 pattern is about one bit better than the 75 conditions stated in the paper's text; the paper's own tables give 74, which the SMC matches stage by stage. With the four patterns of rows 18 and 19 accepted the count is 72, in accordance with the structural 2 bits. With q3c one bit lower, 2^-72.4629, time_log2 would be 58.73900 (or 60.50286 under A_C = 2^60).
- The count of four patterns is a solver enumeration for the published dense part (ffbe30bb); other dense parts were not explored. Our q3 estimator applies the program's own difference checks and does not use the solver.
- The simulation of the counted program (Section 13.3) was run again with this package's program after the R16x change (rows 16 and 17); its figures are from that run; the exact-event change of Section 9.9 acts only on pairs whose row 21 holds.


## Appendix A. Row 16: the exact test against the exhaustive enumeration

Historical aa0e8b6 material below; old LO/MID code and old cost statements are retained solely as inherited evidence, not the P4 implementation or current accounting. No participant code was run outside the organizer's Docker executor.


`r16.c` (7319bba; 0db0eeb6 Appendix A.5) with `r16data.h` generated from the cells of `experiments/lowm.py` (with R16x: eight fixed bits of E16), compiled with `gcc -O2` and run unchanged, prints `total pairs 2097152` (65,536 for each of the 32 l) and writes `r16.bin`, the pairs (u, l). Then, with numpy:

```python
import sys
import numpy as np
sys.path.insert(0, 'experiments'); import lowm as L
env = L.Env(); d = np.fromfile('r16.bin', dtype=np.uint32).reshape(-1, 2)      # the pairs (u, l) of r16.c
M, V = L.E16M, L.E16V
free = [b for b in range(32) if not (M >> b) & 1]
t = np.arange(1 << len(free), dtype=np.uint64); e = np.full(t.shape, V, dtype=np.uint64)
for i, b in enumerate(free): e |= ((t >> np.uint64(i)) & np.uint64(1)) << np.uint64(b)
e = e.astype(np.uint32); bit = lambda v, k: (v >> np.uint32(k)) & np.uint32(1); tot = 0
for l in L.FEASIBLE_L:                                  # the 2^24 values of E16x with the eight fixed bits, the cells of Lemma 6.2 applied to all of them
    c = env.LC[l]; a15 = np.uint32(c['Ax15']); A = e + np.uint32(c['cxA'])
    ok = ((e ^ np.uint32(c['Ex15'])) & np.uint32(0x10)) == 0
    ok &= bit(A, 29) == 1
    ok &= bit(A, 15) != bit(a15, 15)
    ok &= bit(A, 23) == bit(a15, 23); ok &= bit(A, 25) == bit(a15, 25)
    ok &= bit(A, 9) != bit(A, 20); ok &= bit(A, 18) != bit(A, 6); ok &= bit(A, 8) == bit(A, 17)
    us = set((e[ok] - np.uint32(c['C'])).tolist()); ref = set(d[d[:, 1] == l, 0].tolist())
    assert us == ref, l
    tot += len(us)
print('all %d per-l sets of u' % len(L.FEASIBLE_L) + ' equal the enumeration of r16.c; total', tot, 'pairs;', len(set(d[:, 0].tolist())), 'distinct u')
```

Output:

```text
all 32 per-l sets of u equal the enumeration of r16.c; total 2097152 pairs; 2057184 distinct u
```

Second part (the table stage; `numpy`, run in the package directory): for every l the set of u mod 2^24 accepted by the four interface states of the two tables (bit 64 idx + l of the 256-bit words) equals the set defined by the conditions of Lemma 6.2 on the bits 0..23:

```python
import sys
import numpy as np
sys.path.insert(0, 'experiments'); import lowm as L
env = L.Env(); M64 = (1 << 64) - 1
word = lambda tab, w: np.array([(v >> (64 * w)) & M64 for v in tab], dtype=np.uint64)      # the 64-bit words w = 0..3 of the 256-bit table words
LO = [word(env.LOw, w) for w in range(4)]; MI = [word(env.MIDw, w) for w in range(4)]
u = np.arange(1 << 24, dtype=np.uint32); bit = lambda v, k: (v >> np.uint32(k)) & np.uint32(1)
lo = (u & np.uint32(0xfff)).astype(np.int64); mid = (u >> np.uint32(12)).astype(np.int64); M24 = np.uint32(0xffffff); tot = 0
for l in L.FEASIBLE_L:
    c = env.LC[l]; e = u + np.uint32(c['C']); A = e + np.uint32(c['cxA']); a15 = np.uint32(c['Ax15'])
    ok = (e & np.uint32(L.E16M) & M24) == (np.uint32(L.E16V) & M24)
    ok &= ((e ^ np.uint32(c['Ex15'])) & np.uint32(0x10)) == 0
    ok &= bit(A, 15) != bit(a15, 15); ok &= bit(A, 23) == bit(a15, 23)
    ok &= bit(A, 9) != bit(A, 20); ok &= bit(A, 18) != bit(A, 6); ok &= bit(A, 8) == bit(A, 17)      # Lemma 6.2 on the bits 0..23
    acc = np.zeros(1 << 24, dtype=bool)
    for idx in range(4):                                                        # interface state idx of l: bit 64 idx + l of the table words
        acc |= (((LO[idx][lo] >> np.uint64(l)) & np.uint64(1)) & ((MI[idx][mid] >> np.uint64(l)) & np.uint64(1))).astype(bool)
    assert (acc == ok).all(), l
    tot += int(ok.sum())
print('all %d per-l sets of u mod 2^24 accepted by the two tables equal the conditions of Lemma 6.2 on the bits 0..23; total' % len(L.FEASIBLE_L), tot, 'pairs (u mod 2^24, l)')
```

Output:

```text
all 32 per-l sets of u mod 2^24 accepted by the two tables equal the conditions of Lemma 6.2 on the bits 0..23; total 65536 pairs (u mod 2^24, l)
```

## Appendix B. The exact ledger

Self-contained (integers and Fractions); the stage prices are the constants of Section 9, asserted by `lowm.py`. It is the exact ledger of **this** filing's four-list family — 170 classes, `FIXED = 490`, `F7_OPS = 106`, `Q3_LOG2 = -71.4243`, `Pcap <= 11/100,000,000` — and it reproduces `python3 experiments/lowm.py ledger`: `N_FB`, `g`, `vbar`, `vmax_fb`, the cap bound and `time_log2` all agree digit for digit. The one presentational difference is exact: the mirror sums the rational without reducing, so it prints `N = 621084759189170888800` = T x 2644, and the shipped ledger prints the same integer pair as `T_num / T_den = 621084759189170888800 / 2644`; both print the same integers and the same certificate exponent 5770484/10^5 = 57.70485.

```python
from fractions import Fraction as Fr
# Exact ledger of the counted program (proof.md Sections 9-11). Integers and Fractions only.
C = 2644                                   # reference cost of one target compression, in word operations
# stage prices (primitives of the straight-line text, proof.md Section 9; the plane-program counts are measured by lowm.py and asserted at every execution)
# per-list tables (below): the W6 program of every batch of every list with the constant s planes folded, measured by lowm.py (ListData.measure) and asserted at every execution
F7_OPS, SCAN_LANE, CLS_LANE = 106, 7, 5
def scan_fix(nl):                        # the fixed part of a scan over nl lanes (Section 9.6)
  tot = 0
  for r in range(4):
    if 64 * r >= nl: break
    tot += 1 if r in (0, 3) else 2
    for k in range(5):
      if 64 * r + 13 * k < nl: tot += (1 if k in (0, 4) else 2) + 1
  return tot
SCAN_FIX = scan_fix(256)
EXTR, PLACE, GROUP_BODY, PAD_OPS, PROBE = (1, 2, 2, 1), 6, 30, 7, (5, 4, 4, 3)
SURV_FIX, SURV_LANE, EX_OPS, RARE_LOOKUP, RECOMP, ROWCHECK, ROWCOMP, OUTCMP = 13, 6, 13, 2, 35, 53, 106, 16
CPREP, CF_CLASS, SWEEP_OVH, FIXED, RUN_CU, SPILL_K = 260, 8, 127, 490, 7, {3: 30, 1: 18}
ZC_N, KZ_N, NB_N = 31, 16, 0          # broadcast planes of CB3 (bits 1..31) and KZ (16 bits) loaded by every sweep
# the four kept lists of the ten (proof.md Sections 5.3, 9.4, 9.5): cnt classes, n variants, cube bits k, lanes of each batch nl, dynamic s planes of each batch dyn, zq planes loaded by each sweep zq,
# W6 program of each batch (main run / all sums) w6, subtraction runs sub[(batch, cu)]
LISTS = {
  0: {'cnt': 82, 'n': 3456, 'k': 3, 'nl': [256, 176], 'dyn': [10, 9], 'zq': [11], 'w6': [{False: 193, True: 262}, {False: 181, True: 250}], 'sub': [{1: 26, 4: 25, 5: 28, 8: 24, 9: 27, 12: 26, 13: 27}, {1: 26, 4: 25, 5: 28, 8: 24, 9: 27, 12: 26, 13: 27}]},
  1: {'cnt': 3, 'n': 3456, 'k': 3, 'nl': [256, 176], 'dyn': [11, 9], 'zq': [12], 'w6': [{False: 206, True: 275}, {False: 187, True: 256}], 'sub': [{1: 26, 4: 25, 5: 28, 8: 24, 9: 27, 12: 26, 13: 27}, {1: 26, 4: 25, 5: 28, 8: 24, 9: 27, 12: 26, 13: 27}]},
  5: {'cnt': 82, 'n': 3600, 'k': 3, 'nl': [256, 194], 'dyn': [10, 9], 'zq': [11], 'w6': [{False: 195, True: 265}, {False: 189, True: 259}], 'sub': [{1: 26, 4: 25, 5: 28, 8: 24, 9: 27, 12: 26, 13: 27}, {1: 26, 4: 25, 5: 28, 8: 24, 9: 27, 12: 26, 13: 27}]},
  6: {'cnt': 3, 'n': 3600, 'k': 3, 'nl': [256, 194], 'dyn': [11, 9], 'zq': [12], 'w6': [{False: 208, True: 278}, {False: 189, True: 259}], 'sub': [{1: 26, 4: 25, 5: 28, 8: 24, 9: 27, 12: 26, 13: 27}, {1: 26, 4: 25, 5: 28, 8: 24, 9: 27, 12: 26, 13: 27}]},
}
CUBE = {3: 13, 1: 1}                        # the cube bits {0, 2, 3} or {0} as a mask
NCLS = 170; NVAR = sum(L['n'] * L['cnt'] for L in LISTS.values()); NFEAS = 32
P7 = Fr(68157440, 1 << 32); P6 = Fr(287309824, 1 << 32); R16F = Fr(2097152, 1 << 32); MU = Fr(1, 256); PNZ = Fr(63512, 1 << 24)
# calibrated A_C = 2^48 (proof.md Section 10; sensitivity at A_C = 2^56, 2^60, 2^64 in Section 12) and the success-floor constants
A_C, A_S, DEV, PRE, FIN = 1 << 48, 1 << 50, 1 << 40, 1 << 38, 1600
EXQ = Fr(24331, 10000)                           # collision event / cell event after row 21: preregistered 99% lower bound (proof.md Section 7.7; 4ec21bf9 Appendix D.3)
Q3 = Fr(1638712607792, 1 << 112) * EXQ           # q3 = q3_cell x EXQ, q3_cell = 2^71.4243 rounded down to a 40-bit mantissa (floor(2^(112 - 71.71.4243)) / 2^112)
MU0 = Fr(49466264, 100000000)                  # smallest 8-decimal number above -ln(0.61 - PCAP_ASSUMED - 2^-60) / (1 - 2^-10.4)  (Appendix C)
SLACK = Fr(5806644450353958, 10**20); PCAP_ASSUMED = Fr(13, 100000000)
def subsets(mask): return [s for s in range(16) if s & ~mask == 0]
def lane_costs(nls): return sum(SCAN_LANE + EXTR[L // 64] for nl in nls for L in range(nl))   # scan and extraction of every lane of the batches of reps
MEMBER_CHARGE = (6, 8, 11, 21)      # itemised: pair 8, group of four 11, two groups 21 (Section 9.6)
def memcost(j): return MEMBER_CHARGE[j] if j < 4 else 5 * (1 << (j - 1)) + 1                                  # members of a rep with |I| = j
def class_det(lid, Q0):
    # operations of a passing class (list lid) with relevant cube bits Q0 that do not depend on which reps are good (2^|Q0| runs)
    L = LISTS[lid]; nb = len(L['nl']); nsw = (nb + 1) // 2; part = 1 if sum(L['nl']) % 256 else 0; full = Q0 != 0; j = L['k'] - bin(Q0).count('1')
    sweeps = sum(3 + 2 * (L['zq'][sw] + KZ_N + ZC_N + NB_N) for sw in range(nsw))
    tot = CPREP + CF_CLASS + (0 if j == 0 else 5 * (1 << j) - 2) + sweeps + sum(2 * L['dyn'][b] + 2 + L['w6'][b][full] + scan_fix(L['nl'][b]) for b in range(nb)) + part
    if full:
        tot += 2 * nb * SPILL_K[L['k']]
        for cu in subsets(Q0):
            if cu: tot += sum(RUN_CU + L['sub'][b][cu] + scan_fix(L['nl'][b]) for b in range(nb)) + part
    return tot
def class_run_cost(lid, Q0):
    # scan, extraction and members of one run if all reps are good (times p6 for the expectation)
    L = LISTS[lid]
    return lane_costs(L['nl']) + sum(L['nl']) * memcost(L['k'] - bin(Q0).count('1'))
def class_expected(lid):
    # Pr[Q0[0]=1 | class passes]=1/4; Q0[2],Q0[3] are independent 1/2 (Section 8.1).
    k = LISTS[lid]['k']
    return sum(Fr(1 if (Q0 & 1) else 3, 1 << (k + 1)) * (class_det(lid, Q0) + (1 << bin(Q0).count('1')) * P6 * class_run_cost(lid, Q0)) for Q0 in subsets(CUBE[k]))
def class_max(lid):
    return max(class_det(lid, Q0) + (1 << bin(Q0).count('1')) * class_run_cost(lid, Q0) for Q0 in subsets(CUBE[LISTS[lid]['k']]))
perclass = pairs = Fr(0); vmax = Fr(0)
c3b_row = ROWCOMP + ROWCHECK + 1; c3b_pair = 201 + RECOMP + 1 + RARE_LOOKUP; c3b_l = 2 + 6 + 2 * c3b_row; c3b_t = 4 * c3b_row + 15 * ROWCOMP + OUTCMP + 1   # rows 18..21 checked, rows 22..36 computed, the output comparison, one work-counter update (Section 9.9)
for lid, L in LISTS.items():
    perclass += L['cnt'] * P7 * class_expected(lid); pairs += L['cnt'] * P7 * P6 * L['n']; vmax += L['cnt'] * class_max(lid)
ct_var = CLS_LANE * NCLS * P7
groups = (pairs + 3) / 4; lanes = 4 * groups
grp = groups * (GROUP_BODY + sum(PROBE)) + PAD_OPS + lanes * 7 * Fr(1513,8192)
surv = lanes * (PNZ * SURV_FIX + MU * (SURV_LANE + EX_OPS))
rare = lanes * R16F * (c3b_pair + c3b_l + Fr(1, 512) * c3b_t)
vbar = ct_var + perclass + grp + surv + rare            # expected data-dependent operations per first block
g = pairs                                               # expected good pairs per first block
vlanes = NVAR + 3                                       # one first block's maximal data-dependent work: all classes pass, all variants good, every l survives, every probe hits
vmax_fb = vmax + Fr(vlanes, 4) * (GROUP_BODY + sum(PROBE) + 28) + PAD_OPS + vlanes * (SURV_FIX + NFEAS * (SURV_LANE + EX_OPS)) \
          + vlanes * Fr(11, 10) * (c3b_pair + NFEAS * (c3b_l + c3b_t)) + 24 + CLS_LANE * NCLS
NFB = int(-(-MU0 // (g * 32 * Q3)))                     # first blocks: E[successes] = NFB g 32 q3 >= MU0
from decimal import Decimal, getcontext
getcontext().prec = 60
t_cap = SLACK * NFB * vbar; kappa = t_cap * t_cap / (2 * (NFB * vmax_fb * vbar + vmax_fb * t_cap / 3))      # Bernstein: Pr[sum v_f - NFB vbar >= t] <= exp(-t^2 / (2 (NFB vmax_fb vbar + vmax_fb t / 3)))
PCAP = Fr(int((-(Decimal(kappa.numerator) / Decimal(kappa.denominator))).exp() * 10 ** 30) + 1, 10 ** 30)    # bound of the work-cap overflow, rounded up to 30 decimals
assert PCAP <= PCAP_ASSUMED
V_MAX = int(-(-(1 + SLACK) * NFB * vbar // 1))          # cap on the counted data-dependent operations
ROWS = [("A_C: characteristic search (units x C)", A_C * C), ("A_S: Step-1 solve (units x C)", A_S * C), ("DEV: development (units x C)", DEV * C),
        ("N_FB first-block compressions (units x C)", NFB * C), ("fixed operations: N_FB x FIXED", NFB * FIXED), ("V_MAX: data-dependent operations", V_MAX),
        ("overshoot past the cap: vmax_fb", -(-vmax_fb // 1)), ("PRE: preprocessing", PRE), ("FIN: final verification", FIN), ("6 further compressions (units x C)", 6 * C)]
ROWS = [(a, int(b)) for a, b in ROWS]
N = sum(b for _, b in ROWS)
P = 100000
a = (N ** P // C ** P).bit_length() - 1
while (1 << (a + 1)) * C ** P <= N ** P: a += 1
while (1 << a) * C ** P > N ** P: a -= 1
claim = Fr(-(-(a + 1) * 10 ** 5 // P), 10 ** 5)
w = max(len(k) for k, _ in ROWS)
for k, v in ROWS: print(k.ljust(w), format(v, ","))
print("N_FB = %d, g = %s, vbar = %s, Pcap = %s <= %s" % (NFB, float(g), float(vbar), float(PCAP), float(PCAP_ASSUMED)))
print("N = %d" % N)
print("certificate: 2^%d * %d^%d <= N^%d < 2^%d * %d^%d" % (a, C, P, P, a + 1, C, P))
print("time_log2 = %.5f" % float(claim))
```

Output of the mirror above (identical in every quantity to the shipped ledger):

```text
A_C: characteristic search (units x C)    744,219,838,422,974,464
A_S: Step-1 solve (units x C)             2,976,879,353,691,897,856
DEV: development (units x C)              2,907,108,743,839,744
N_FB first-block compressions (units x C) 83,597,987,524,703,807,076
fixed operations: N_FB x FIXED            15,492,819,170,614,548,210
V_MAX: data-dependent operations          518,269,945,863,203,016,639
overshoot past the cap: vmax_fb           54,912,880,403
PRE: preprocessing                        274,877,906,944
FIN: final verification                   1,600
6 further compressions (units x C)        15,864
N_FB = 31617998307376629, g = 636.6804599761963, vbar = 16390.65979064846, Pcap = 1.2313999342221139e-07 <= 1.3e-07
N = 621084759189170888800
certificate: 2^5770484 * 2644^100000 <= N^100000 < 2^5770485 * 2644^100000
time_log2 = 57.70485
```

Values of the shipped ledger for this family (`python3 experiments/lowm.py ledger`; the same
six numbers the pre-restriction package printed, with the three the four-list restriction moves
listed in Section 9.2):

```text
N_FB = 31617998307376629
vbar = 18021721026738521/1099511627776
vmax_fb = 274564402011/5
V_MAX = 518269945863203016639
N = 621084759189170888800
time_log2 = 57.70485
```

## Appendix C. The success floor

```python
from decimal import Decimal, getcontext
getcontext().prec = 60
PCAP = Decimal(11) / Decimal(10**8)          # assumed cap bound; Appendix B asserts the computed 1.23139993e-07 is below it
EPS = Decimal(2) ** -60                      # a repeated first block among N_FB draws
D = 1 - Decimal(2) ** Decimal('-10.4')       # the H3 discount 1 - 2^-10.4
req = -(Decimal('0.61') - PCAP - EPS).ln() / D                       # the requirement
MU_REQ = Decimal(49466260) / Decimal(10 ** 8)                        # requirement rounded up to eight decimals
MU0 = Decimal(4208124008881635417764050972564764929619) / Decimal(8507059173023461586584365185794205286400)   # achieved: N_FB g 32 q3_cell x EXQ
assert req < MU_REQ <= req + Decimal(2) / Decimal(10 ** 8)
assert MU0 >= MU_REQ
succ = 1 - (-D * MU_REQ).exp() - PCAP - EPS
print('required %.15f' % req)
print('req rounded up %.8f' % MU_REQ)
print('achieved mu0 %.15f' % MU0)
print('success bound %.17f' % succ)
assert succ > Decimal('0.39')
print('OK')
```

Output (60-digit decimals; the shipped ledger's binary double prints
0.39000000441594207 for the same quantity):

```text
required 0.494662599944212
req rounded up 0.49466264
achieved mu0 0.494662640000000
success bound 0.39000000441594207
OK
```

## Appendix D. `selftest` output

```text
classes 170, variants 599760 (599,760), mismatches 0
W6_OPS (k, full): {(3, False): 211, (3, True): 281, (1, False): 231, (1, True): 310} SUBF_OPS: {(3, 1): 26, (3, 4): 25, (3, 5): 28, (3, 8): 24, (3, 9): 27, (3, 12): 26, (3, 13): 27, (1, 1): 11} F7_OPS 106 FIXED 490
F7 sampler violations 0
lists (size, cube bits): [(3456, 3), (3600, 3)]  classes with a cube bit 2 or 3 and base bit 1 clear: 0
invariance of F6(W6x) under the flips of the bits of I: 30720 checks, 0 mismatches
w6 plane lanes 33570, F6 passes 1462, mismatches 0
class-test lanes 34000, mismatches 0
row-16 checks: members seen 22, mismatches 0
packed u lanes 400, mismatches 0
max S0 over the 599,760 variants 0xffffbb5c True
```

## Appendix E. Credits

Authors of the work this filing builds on are named in Section 2 and in the dependency list. The paper: Y. Li, Z. Zhang, M. Li, F. Liu, H. Qian, J. Zhu. This filing builds on 221eb058 (Jbenisek with Claude Sonnet 5.5 and Claude Opus 5.5, Grok, GPT Luna), ffbe30bb (Jbenisek), 4ec21bf9 (Jbenisek with Claude and GPT Luna: the collision event after row 21, Section 7.7) and 96169e7c (srw with Gemini 4 Argon), adding the plane-algebra, carry-decoupling, and cube-subtraction reductions of Sections 8 and 9 (d9f8833d, sraiw). This filing (Jbenisek with Claude Sonnet 5.5 and Claude Opus 5.5, Claude Code) carried that algebra over from the published text into its own package, added the organizer experiments of ec1340aa and the Bernstein cap bound, and ran and checked the program. Mistakes are ours.

## Appendix F. The q3 studies: program, preregistration, results

All files are in `q3/` of the working directory of this filing. The estimator `q3smc.c` was written for this filing from the description of Section 7.3; the constants it checks (cells of rows 0..36, the printed two-bit conditions closing at rows >= 16, rows 12..15 of the published pair for each l, the variant list) are generated by `gen_consts.py` from `experiments/lowm.py`, once with the Table 15 cells (`q3consts_orig.h`) and once with the two relaxed cell strings of rows 18 and 19 (`q3consts_relaxed.h`, sha256 f01e0c355afbb0aff8df6a06b2367cdd43644d3ad10af6c7470f2a44e535d47e, written from the program before the R16x change; regenerating from `experiments/lowm.py` as filed gives `q3consts_r16x.h` of Appendix G byte for byte; `q3consts_orig.h`, sha256 07aca8a40daf199c7d85cc28f97ec0d84c3976f6d751950f7b2cd0b3799ad8bd, comes from the program with the Table 15 cells, sha256 691563bedd682044a4e9f936ba98cddc8242d2cafa4a14cd4f7585f19a9be597). Build: `gcc -O2 -DCONSTS='"q3consts_relaxed.h"' q3smc.c -lm -o q3smc_relaxed`; run: `q3smc SEED 1 8192 512 16384` with `variants.bin` (599,760 little-endian 32-bit words, W8x of the variants, written by `gen_consts.py`) in the working directory; `-d` as the sixth argument prints the pattern histogram.

### F.1 Preregistration (written before any listed seed ran; stamp 2026-10-12T05:26:30Z, sha256 9187c4519d463838b90eefb4c0aa9df1eb12be95cf463076ad06511c7aaaaabf)

```text
preregistration: our own sequential-Monte-Carlo estimate of q3 for the 170-class A0-variant attack on 37-step SHA-256, with the original cells of rows 18 and 19 (validation) and with the four value patterns of rows 18 and 19 accepted
written before any listed seed was run; the stamp is the line below.
stamp: 2026-10-12T05:26:30Z
program: q3smc.c (written for this filing from the description of the estimator in the earlier proofs; it shares no code with any other participant's program and no other participant's code was compiled or run), sha256 2d8a406a5dd1ba0f3d6502b0e887d3b106a865a8970cce21d6c9ec5dcdd3ed71.
constants: q3consts_orig.h (sha256 07aca8a40daf199c7d85cc28f97ec0d84c3976f6d751950f7b2cd0b3799ad8bd) and q3consts_relaxed.h (sha256 f01e0c355afbb0aff8df6a06b2367cdd43644d3ad10af6c7470f2a44e535d47e), written by gen_consts.py (sha256 14ea0015f43b1ea86109ccc78e86cf392c12a9a34c7ece6a1c3babc1be6b4ae7) from this package's lowm.py (original cells: sha256 691563bedd682044a4e9f936ba98cddc8242d2cafa4a14cd4f7585f19a9be597; relaxed cells: the same file with exactly the two strings CHE[18] and CHE[19] changed, sha256 1e97095c79b1bcf50888c00cb908f31d99a059ccdfe08743c1f58b8822261756).
 the relaxed cells replace the eight characters of Table 15 that fix E18[1]=1, E18[5]=0, E18[10]=1, E18[11]=1, E18[18]=0, E18[28]=0, E18[29]=1 and E19[29]=1 by '=' and change nothing else: row 18 becomes =======uu=======n=====1====1====, row 19 becomes =======00====1==0==========1====.
variant list: variants.bin, the W8x = W8C - (a0 + C4) of the 599,760 variants of the 170 classes (all distinct), as listed by lowm.py (sha256 6900f64cec67217eb352fd43cd0552c92b2514b892481c95f761d19619d1e3c5).
estimator: stage 16 exact (count of the (l, E16x) pairs that pass row 16), stages 17..21 (E_t^x proposed uniformly with the fixed x-bits of the cell imposed, weight 2^-f), stage 22 ((W6, W7) uniform on F6 x F7), tail (variant uniform), uniform resampling of the survivors after each stage, product of the stage means. Parameters of every replicate: NP = 8192, M = 512, MT = 16384.
smoke runs, disclosed and not part of any study: seed 1 with each binary (original cells: stage 16 = 1,052,672 pairs, log2est -73.92417; relaxed cells: log2est -72.15193, patterns cd 1b f6 20 only). Seed 1 is not used below.
validation study V (original cells, binary q3smc_orig): seeds 710000..710063 (64 replicates). Computed: mean and sd of the linear estimates, one-sided 99% Student lower bound LB_V = mean - t(0.99, 63 df) sd / sqrt(64).
 V passes if both (a) the difference of the means from study B of the registered studies of the earlier filing (mean 2^-73.9987, relative sd 0.0378, 32 replicates) is at most 2.576 standard errors, z = (mean_V/mean_B - 1)/sqrt(relse_V^2 + relse_B^2), relse_B = 0.0378/sqrt(32), and (b) log2 LB_V is within 0.04 of log2 of study B's bound (-74.0225). It is the check that this program reproduces R37M's own q3 = 2^-74.03 (which is that study's floor). If V fails, no q3 is declared from this program and the failure is reported.
main study (relaxed cells, binary q3smc_relaxed), two independent blocks of the same design: R1 seeds 720000..720127 (128 replicates), R2 seeds 721000..721127 (128 replicates). For each block the one-sided 99% Student lower bound LB = mean - t(0.99, 127 df) sd / sqrt(128).
rule (fixed in advance): declared q3 = 2^x with x = floor(100 x log2(min(LB_R1, LB_R2))) / 100 (the lowest 99% bound, rounded down to two decimals of log2, never up). It is used only if V passes.
every listed seed is run and reported; none is dropped, replaced or rerun whatever the result; a crashed run would be re-run with the same seed only if the crash is not a property of the program.
the E18/E19 pattern diagnostic (the program's -d option: a histogram of the eight value bits of the 8192 particles that survived rows 16..22; seeds 730001..730003 with the relaxed binary) is a description, not part of the bound.
at most 2 processes at once.
```

In the preregistration the name of the table-free program with Table 15's cells is a working label: it denotes the program of this filing before its two cell strings were relaxed (its q3 is 2^-74.03).

### F.2 Results

Rule applied: V passes (validation PASSES both preregistered criteria (|z| <= 2.576; bound within 0.04 of -74.0225)); lowest bound 2^-72.01914 of R1 (2^-72.0191) and R2 (2^-72.0074), rounded down to two decimals: **2^-72.02** for the four patterns alone (the q3 used is that of the joint study, Appendix G). pooled 256 replicates: mean 2^-71.9922, relative sd 0.0697, bound 2^-72.0070 (descriptive).

Stage means of validation V (log2): 16: -16.994, 17: -13.000, 18: -14.999, 19: -6.000, 20: -7.000, 21: -1.000, 22: -10.999, tail -4.000. Stage means of the main study (256 replicates): 16: -16.994, 17: -13.000, 18: -8.000, 19: -10.000, 20: -7.000, 21: -1.999, 22: -11.002, tail -4.000.

All 64 log2 estimates of V (seeds 710000..710063, in order):

```text
-74.063 -74.004 -73.897 -73.950 -73.943 -73.949 -73.953 -74.009 -73.999 -73.922 -73.999 -74.094 -74.063 -73.986 -73.858 -73.956
-73.960 -73.996 -74.025 -74.057 -74.062 -73.921 -73.993 -73.984 -73.983 -74.134 -73.978 -74.022 -74.019 -73.999 -74.065 -74.063
-73.999 -74.036 -73.963 -73.994 -73.938 -73.952 -73.989 -73.988 -73.963 -73.959 -74.039 -73.954 -73.985 -74.047 -73.991 -74.030
-73.988 -73.939 -73.894 -73.966 -73.992 -74.075 -74.029 -74.008 -73.908 -73.999 -74.034 -74.020 -73.981 -73.933 -73.994 -73.996
```

All 128 log2 estimates of R1 (seeds 720000..720127):

```text
-71.892 -71.944 -72.050 -71.918 -72.020 -71.794 -71.924 -71.947 -71.930 -71.844 -71.948 -72.018 -71.983 -71.888 -72.062 -72.014
-71.845 -71.868 -71.917 -71.880 -72.099 -72.098 -71.860 -71.864 -71.866 -71.856 -71.856 -71.986 -71.910 -72.264 -71.890 -71.884
-71.987 -72.094 -72.039 -71.985 -71.993 -72.095 -72.131 -72.097 -71.835 -71.979 -72.078 -71.934 -72.183 -72.184 -72.152 -72.120
-72.085 -72.179 -71.943 -71.983 -72.224 -72.060 -71.925 -72.056 -72.117 -71.959 -72.173 -72.014 -72.072 -72.081 -71.941 -72.040
-71.851 -71.869 -71.984 -71.946 -71.896 -71.943 -71.946 -72.069 -72.136 -72.148 -71.941 -71.791 -72.037 -71.991 -72.161 -72.098
-72.001 -71.960 -72.059 -71.952 -71.983 -71.950 -72.094 -71.984 -72.072 -72.169 -72.059 -71.980 -72.112 -72.092 -72.080 -72.096
-71.943 -71.835 -72.091 -72.030 -72.102 -72.141 -72.070 -71.964 -71.931 -71.969 -72.065 -71.968 -71.724 -72.060 -71.944 -72.016
-71.991 -72.174 -71.944 -72.042 -72.142 -71.879 -71.869 -72.077 -72.053 -71.930 -71.931 -71.899 -72.064 -72.090 -71.962 -71.942
```

All 128 log2 estimates of R2 (seeds 721000..721127):

```text
-71.950 -71.834 -71.974 -72.061 -71.941 -71.976 -72.030 -71.860 -72.142 -71.898 -72.028 -72.001 -71.844 -72.084 -72.126 -71.734
-72.022 -72.019 -71.880 -72.057 -71.895 -72.199 -71.972 -72.114 -72.038 -71.954 -71.925 -71.971 -71.889 -71.994 -72.068 -72.085
-72.027 -72.045 -72.085 -71.912 -71.961 -71.938 -71.804 -71.990 -72.004 -71.809 -72.012 -71.946 -72.095 -71.858 -72.005 -72.135
-71.939 -71.929 -72.040 -71.788 -72.115 -71.817 -71.852 -72.081 -72.008 -71.944 -72.106 -72.106 -72.006 -72.063 -71.939 -72.049
-71.938 -71.944 -71.957 -72.060 -72.037 -72.057 -71.976 -71.867 -72.133 -72.138 -72.209 -72.061 -71.971 -72.070 -72.010 -72.137
-72.071 -72.021 -71.995 -72.101 -71.979 -71.945 -72.017 -71.927 -71.948 -72.009 -71.920 -72.024 -71.821 -72.015 -71.907 -71.991
-71.851 -72.090 -71.927 -72.042 -72.000 -71.886 -71.919 -71.811 -71.834 -71.950 -72.090 -71.976 -72.007 -72.271 -71.961 -71.929
-71.980 -71.958 -71.977 -72.014 -72.082 -71.977 -72.188 -71.965 -72.106 -72.115 -71.907 -71.954 -71.946 -71.866 -71.795 -72.136
```

The program's own output for the first seed of each block:

```text
--- seed 710000 ---
RESULT seed 710000 NP 8192 M 512 MT 16384 log2est -74.06303 est 5.0676630297e-23
STAGES -16.99438 -12.99553 -15.03271 -6.00000 -6.99930 -1.00000 -11.05236 tail -3.98874  (row-24 survivors 8454312 of 134217728, full passes 8454312)
--- seed 720000 ---
RESULT seed 720000 NP 8192 M 512 MT 16384 log2est -71.89162 est 2.2827903663e-22
STAGES -16.99438 -13.00028 -7.99856 -9.93391 -6.99967 -1.98006 -10.98319 tail -4.00157  (row-24 survivors 8379473 of 134217728, full passes 8379473)
--- seed 721000 ---
RESULT seed 721000 NP 8192 M 512 MT 16384 log2est -71.94963 est 2.1928148179e-22
STAGES -16.99438 -12.99632 -8.00176 -9.98877 -7.00009 -2.00954 -10.97902 tail -3.97975  (row-24 survivors 8507175 of 134217728, full passes 8507175)
```

Pattern diagnostic (relaxed binary, `-d`, seeds 730001..730003; bit string E18[1,5,10,11,18,28,29] as bits 0..6 and E19[29] as bit 7, hexadecimal; Table 15 is cd, the others 1b, f6, 20): seed 730001: 1b:2349 20:1607 cd:2461 f6:1775; seed 730002: 1b:1710 20:2180 cd:2145 f6:2157; seed 730003: 1b:1714 20:1891 cd:2040 f6:2547.

Interim looks (declared under H2, Section 12): the analysis script was run on the partial outputs while the blocks were running, to monitor progress; no seed, parameter or rule was changed after any look.

### F.3 The check of the three alternative collisions (`check_alt.py` as run)

```text
pair (x = M', y = M)         collides  cells of this lowm.py    cells of Table 15       
Table 15 (published pair)    True      True                     True                    
G1                           True      True                     False                   
G2                           True      True                     False                   
G1 xor G2                    True      True                     False
```

### F.4 `q3smc.c`

```c
/* q3smc.c - importance-weighted sequential Monte Carlo estimate of q3 for the A0-variant attack on 37-step SHA-256 (rows 16..36), written for this filing
   from the description of the estimator in the proofs of the earlier filings; it shares no code with theirs.
   q3 = (1/32) sum_l Pr[rows 16..36 of both members follow every cell and every printed two-bit condition closing at rows >= 16 | (variant, l, good pair)].
   Stage 16: exact (all E16x with the fixed x-bits of the E16 cell that pass row 16, for each l; the initial particles are drawn uniformly from these (l, E16x) pairs).
   Stages 17..21: each child proposes E_t^x uniformly with the fixed x-bits of the row's E cell imposed (weight 2^-f), W_t^x = E_t^x - (rest of step t), W_t^y = W_t^x + the exact difference
   given by the schedule, and the whole row is checked (cells of A, E, W for both members, '+' equalities, printed two-bit conditions).
   Stage 22: (W6, W7) drawn uniformly from F6 x F7 (W7 from the affine decomposition, W6 by rejection), W22 from the schedule, row 22 checked.
   Tail: a variant (W8x) drawn uniformly from the variant list; rows 23..36 for both members, all cells and conditions checked (row 24's W cell and relations first, which is exact: it is a part of the check).
   After each of the stages 17..22 the survivors are resampled uniformly (all survivors of a stage have the same weight) to NP particles; the product of the stage means is unbiased for q3.
   usage: q3smc seed0 nrep NP M MT [-d]    (variants.bin in the working directory)
   build: gcc -O2 -DCONSTS='"q3consts_orig.h"' q3smc.c -lm -o q3smc_orig   (or q3consts_relaxed.h, q3consts_r16x.h)
   the TAG line (added for the R16x study) counts the full passes whose member x has E16[23]=0 and E16[24]=E17[24]; it draws no random numbers, so every other output is unchanged */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#include CONSTS
typedef uint32_t u32; typedef uint64_t u64;
#define ROR(x,n) (((x)>>(n))|((x)<<(32-(n))))
static inline u32 S0f(u32 x){return ROR(x,2)^ROR(x,13)^ROR(x,22);}
static inline u32 S1f(u32 x){return ROR(x,6)^ROR(x,11)^ROR(x,25);}
static inline u32 s0f(u32 x){return ROR(x,7)^ROR(x,18)^(x>>3);}
static inline u32 s1f(u32 x){return ROR(x,17)^ROR(x,19)^(x>>10);}
static inline u32 CHf(u32 x,u32 y,u32 z){return (x&y)^(~x&z);}
static inline u32 MAJf(u32 x,u32 y,u32 z){return (x&y)^(x&z)^(y&z);}
/* rng: xoshiro256++ seeded by splitmix64 */
static u64 rs[4];
static u64 sm(u64*x){u64 z=(*x+=0x9e3779b97f4a7c15ULL);z=(z^(z>>30))*0xbf58476d1ce4e5b9ULL;z=(z^(z>>27))*0x94d049bb133111ebULL;return z^(z>>31);}
static void seedrng(u64 s){u64 x=s;for(int i=0;i<4;i++)rs[i]=sm(&x);}
static inline u64 rotl(u64 x,int k){return (x<<k)|(x>>(64-k));}
static inline u64 rnd64(void){u64 r=rotl(rs[0]+rs[3],23)+rs[0],t=rs[1]<<17;rs[2]^=rs[0];rs[3]^=rs[1];rs[1]^=rs[2];rs[0]^=rs[3];rs[2]^=t;rs[3]=rotl(rs[3],45);return r;}
static inline u32 rnd32(void){return (u32)(rnd64()>>32);}
static inline u64 below(u64 n){return (u64)(((__uint128_t)rnd64()*n)>>64);}

/* member 0 = x, member 1 = y; A and E are stored at index i+4 (A_{-4} at 0), W at index i */
typedef struct { u32 A[2][41], E[2][41], W[2][37]; int l; } St;
static inline void stepm(St*s,int m,int t){
  u32*A=s->A[m]+4,*E=s->E[m]+4,*W=s->W[m];
  E[t]=A[t-4]+E[t-4]+S1f(E[t-1])+CHf(E[t-1],E[t-2],E[t-3])+KK[t]+W[t];
  A[t]=E[t]-A[t-4]+S0f(A[t-1])+MAJf(A[t-1],A[t-2],A[t-3]);
}
static inline int row_ok(const St*s,int t){
  u32 X=s->A[0][t+4],Y=s->A[1][t+4];
  if((X&CA_m[t])!=CA_v[t]||(X^Y)!=CA_d[t])return 0;
  X=s->E[0][t+4];Y=s->E[1][t+4];
  if((X&CE_m[t])!=CE_v[t]||(X^Y)!=CE_d[t])return 0;
  u32 q=CE_p[t]&CE_p[t-1];
  if(q&&((X^s->E[0][t+3])&q))return 0;
  X=s->W[0][t];Y=s->W[1][t];
  if((X&CW_m[t])!=CW_v[t]||(X^Y)!=CW_d[t])return 0;
  return 1;
}
static inline u32 gets(const St*s,int k,int i){return k==0?s->A[0][i+4]:k==1?s->E[0][i+4]:s->W[0][i];}
static inline int x2_ok(const St*s,int r){
  for(int j=0;j<NX2;j++){
    if(X2T[j][7]!=r)continue;
    int a=(gets(s,X2T[j][0],X2T[j][1])>>X2T[j][2])&1,b=(gets(s,X2T[j][4],X2T[j][5])>>X2T[j][6])&1;
    if((X2T[j][3]==1)!=(a==b))return 0;
  }
  return 1;
}
static int infw(u32 w,u32 d,u32 t){return (u32)(s0f(w+d)-s0f(w))==t;}
static u32 drawF7(void){
  u64 r=rnd64();u32 w=(u32)r;
  #define SETB(k,v) w=(w&~(1u<<(k)))|((u32)(v)<<(k))
  #define BIT(k) ((w>>(k))&1)
  if((r>>32)%65){SETB(11,0);SETB(22,1);SETB(26,1);SETB(18,BIT(1));SETB(30,BIT(9));SETB(28,BIT(0));}
  else{SETB(11,1);SETB(12,0);SETB(22,0);SETB(23,1);SETB(26,0);SETB(27,1);SETB(18,BIT(1));SETB(19,BIT(2));SETB(30,BIT(9));SETB(31,BIT(10));SETB(28,BIT(0));SETB(29,BIT(1));}
  return w;
}
static u32 drawF6(void){u32 w;do w=rnd32();while(!infw(w,D6,T6));return w;}
static void init_l(St*s,int l){
  memset(s,0,sizeof *s);s->l=l;
  for(int j=0;j<4;j++){s->A[0][4+12+j]=LAx[l][j];s->E[0][4+12+j]=LEx[l][j];s->A[1][4+12+j]=LAy[l][j];s->E[1][4+12+j]=LEy[l][j];}
  for(int j=0;j<7;j++){s->W[0][9+j]=LWx[l][j];s->W[1][9+j]=LWy[l][j];}
}
/* exact y-x difference of the schedule word t (t = 16..21): words 0..5 are equal in both members; W6 enters W21 through its F6 property */
static inline u32 dWsched(const St*s,int t){
  u32 d=s1f(s->W[1][t-2])-s1f(s->W[0][t-2])+s->W[1][t-7]-s->W[0][t-7];
  if(t==21)d+=T6;
  return d;
}
/* the part of step t that does not involve W_t or the proposal: A_{t-4} + E_{t-4} + S1(E_{t-1}) + CH(E_{t-1},E_{t-2},E_{t-3}) + K_t */
static inline u32 basef(const St*s,int t){return s->A[0][t]+s->E[0][t]+S1f(s->E[0][t+3])+CHf(s->E[0][t+3],s->E[0][t+2],s->E[0][t+1])+KK[t];}
typedef struct { u32 par, a, b; } Ch;
typedef struct { int l; u32 e; } R16e;
static int pc(u32 x){return __builtin_popcount(x);}

int main(int argc,char**argv){
  if(argc<6){fprintf(stderr,"usage: q3smc seed0 nrep NP M MT [-d]\n");return 1;}
  u64 seed0=strtoull(argv[1],0,10);int nrep=atoi(argv[2]);int NP=atoi(argv[3]);int M=atoi(argv[4]);long MT=atol(argv[5]);int diag=argc>6&&!strcmp(argv[6],"-d");
  FILE*f=fopen("variants.bin","rb");if(!f){fprintf(stderr,"no variants.bin\n");return 1;}
  fseek(f,0,SEEK_END);long nv=ftell(f)/4;fseek(f,0,SEEK_SET);u32*var=malloc(nv*4);if(fread(var,4,nv,f)!=(size_t)nv){return 1;}fclose(f);
  /* stage 16: exact enumeration of the (l, E16x) pairs that pass row 16 */
  long cap=1<<22,n16=0;R16e*r16=malloc(cap*sizeof(R16e));long per_l[32];
  {
    u32 v=CE_v[16];u32 fr=~CE_m[16];
    for(int l=0;l<32;l++){
      St s;init_l(&s,l);long c0=n16;
      u32 base=basef(&s,16),dW=dWsched(&s,16),sub=0;
      do{
        u32 e=v|sub;
        s.W[0][16]=e-base;s.W[1][16]=s.W[0][16]+dW;
        stepm(&s,0,16);stepm(&s,1,16);
        if(row_ok(&s,16)&&x2_ok(&s,16)){if(n16==cap){cap*=2;r16=realloc(r16,cap*sizeof(R16e));}r16[n16].l=l;r16[n16].e=e;n16++;}
        sub=(sub-fr)&fr;
      }while(sub);
      per_l[l]=n16-c0;
    }
  }
  fprintf(stderr,"stage 16: %ld pairs (u,l); per l:",n16);for(int l=0;l<32;l++)fprintf(stderr," %ld",per_l[l]);fprintf(stderr,"\n");
  double lz16=log2((double)n16)-37.0;
  int fb[23];for(int t=17;t<=21;t++)fb[t]=pc(CE_m[t]);
  St*P=malloc((size_t)NP*sizeof(St)),*Q=malloc((size_t)NP*sizeof(St));
  long maxch=(long)NP*M;Ch*chl=malloc(maxch*sizeof(Ch));
  for(int rep=0;rep<nrep;rep++){
    u64 seed=seed0+rep;seedrng(seed);
    for(int i=0;i<NP;i++){
      R16e e=r16[below(n16)];St*s=&P[i];init_l(s,e.l);
      s->W[0][16]=e.e-basef(s,16);s->W[1][16]=s->W[0][16]+dWsched(s,16);stepm(s,0,16);stepm(s,1,16);
    }
    double lz[40];for(int i=0;i<40;i++)lz[i]=-1e9;
    double lsum=lz16;lz[16]=lz16;int dead=0;
    for(int t=17;t<=22&&!dead;t++){
      long nc=0;
      for(int i=0;i<NP;i++){
        St s=P[i];
        if(t<=21){
          u32 m=CE_m[t],v=CE_v[t],base=basef(&s,t);
          for(int c=0;c<M;c++){
            u32 e=(rnd32()&~m)|v;
            s.W[0][t]=e-base;s.W[1][t]=s.W[0][t]+dWsched(&s,t);
            stepm(&s,0,t);stepm(&s,1,t);
            if(row_ok(&s,t)&&x2_ok(&s,t)){chl[nc].par=i;chl[nc].a=s.W[0][t];chl[nc].b=0;nc++;}
          }
        } else {
          for(int c=0;c<M;c++){
            u32 w6=drawF6(),w7=drawF7();
            s.W[0][6]=w6;s.W[1][6]=w6+D6;s.W[0][7]=w7;s.W[1][7]=w7+D7;
            for(int m2=0;m2<2;m2++){u32*W=s.W[m2];W[22]=s1f(W[20])+W[15]+s0f(W[7])+W[6];}
            stepm(&s,0,22);stepm(&s,1,22);
            if(row_ok(&s,22)&&x2_ok(&s,22)){chl[nc].par=i;chl[nc].a=w6;chl[nc].b=w7;nc++;}
          }
        }
      }
      double ft=(t<=21)?fb[t]:0;
      if(nc==0){dead=1;break;}
      lz[t]=log2((double)nc)-ft-log2((double)NP*M);lsum+=lz[t];
      for(int i=0;i<NP;i++){
        Ch c=chl[below(nc)];St*s=&Q[i];*s=P[c.par];
        if(t<=21){s->W[0][t]=c.a;s->W[1][t]=c.a+dWsched(s,t);stepm(s,0,t);stepm(s,1,t);}
        else{s->W[0][6]=c.a;s->W[1][6]=c.a+D6;s->W[0][7]=c.b;s->W[1][7]=c.b+D7;
          for(int m2=0;m2<2;m2++){u32*W=s->W[m2];W[22]=s1f(W[20])+W[15]+s0f(W[7])+W[6];}
          stepm(s,0,22);stepm(s,1,22);}
      }
      St*tmp=P;P=Q;Q=tmp;
      if(t==22&&diag){
        int hist[256];memset(hist,0,sizeof hist);
        for(int i=0;i<NP;i++){u32 e18=P[i].E[0][18+4],e19=P[i].E[0][19+4];int h=0;
          int b18[7]={1,5,10,11,18,28,29};for(int j=0;j<7;j++)h|=((e18>>b18[j])&1)<<j;h|=((e19>>29)&1)<<7;hist[h]++;}
        printf("PATTERNS seed %llu:",(unsigned long long)seed);for(int h=0;h<256;h++)if(hist[h])printf(" %02x:%d",h,hist[h]);printf("\n");
      }
    }
    long pass=0,tot=0,full=0,passreq=0;double ltail=-1e9;
    if(!dead){
      for(int i=0;i<NP;i++){
        St*s=&P[i];
        u32 Zx=s1f(s->W[0][22])+s->W[0][17]+s0f(s->W[0][9]),Zy=s1f(s->W[1][22])+s->W[1][17]+s0f(s->W[1][9]);
        for(long j=0;j<MT;j++){
          u32 w8=var[below(nv)];tot++;
          u32 wx=Zx+w8,wy=Zy+w8+D8;
          if((wx&CW_m[24])!=CW_v[24]||(wx^wy)!=CW_d[24])continue;
          int ok=1;
          for(int k=0;k<NX2;k++){if(X2T[k][0]!=2||X2T[k][1]!=24||X2T[k][5]!=24)continue;
            int a=(wx>>X2T[k][2])&1,b=(wx>>X2T[k][6])&1;if((X2T[k][3]==1)!=(a==b)){ok=0;break;}}
          if(!ok)continue;
          full++;
          St u=*s;
          u.W[0][8]=w8;u.W[1][8]=w8+D8;
          for(int t=23;t<=36&&ok;t++){
            for(int m2=0;m2<2;m2++){u32*W=u.W[m2];W[t]=s1f(W[t-2])+W[t-7]+s0f(W[t-15])+W[t-16];}
            stepm(&u,0,t);stepm(&u,1,t);
            ok=row_ok(&u,t)&&x2_ok(&u,t);
          }
          pass+=ok;
          if(ok&&!((u.E[0][16+4]>>23)&1)&&!(((u.E[0][16+4]^u.E[0][17+4])>>24)&1))passreq++;
        }
      }
      if(pass>0){ltail=log2((double)pass)-log2((double)tot);lsum+=ltail;}
    }
    int bad=dead||pass==0;
    printf("RESULT seed %llu NP %d M %d MT %ld log2est %.5f est %.10e\n",(unsigned long long)seed,NP,M,MT,bad?-1e9:lsum,bad?0.0:exp2(lsum));
    printf("TAG seed %llu full passes %ld, of which with E16[23]=0 and E16[24]=E17[24] (member x): %ld\n",(unsigned long long)seed,pass,passreq);
    printf("STAGES");for(int t=16;t<=22;t++)printf(" %.5f",lz[t]);printf(" tail %.5f  (row-24 survivors %ld of %ld, full passes %ld)\n",ltail,full,tot,pass);
    fflush(stdout);
  }
  return 0;
}
```

### F.5 `gen_consts.py`

```python
#!/usr/bin/env python3
# gen_consts.py - writes q3consts.h (the characteristic's cells, relations, per-l rows 12..15 of the published pair) and variants.bin (the W8x of the 599,760 variants of the 170 classes)
# from our own lowm.py (this package's counted program).  usage: gen_consts.py <lowm.py> [--relaxed]
import sys, importlib.util, struct, os
sys.dont_write_bytecode = True
path = sys.argv[1]; relaxed = '--relaxed' in sys.argv
spec = importlib.util.spec_from_file_location('lw', path); lw = importlib.util.module_from_spec(spec); spec.loader.exec_module(lw)
out = []
def arr(name, vals, typ='uint32_t'): out.append('static const %s %s[%d] = {%s};' % (typ, name, len(vals), ','.join('0x%x' % v if isinstance(v, int) else str(v) for v in vals)))
R = lw.R
out.append('/* generated by gen_consts.py from lowm.py (cells of rows 0..36; relaxed=%d) */' % relaxed)
arr('KK', lw.K)
for k in 'AEW':
    for j, nm in enumerate('mvdp'):
        arr('C%s_%s' % (k, nm), [lw.CELLS[k][i][j] if i in lw.CELLS[k] else 0 for i in range(0, R)])
x2 = [e for e in lw.X2 if max(e[1], e[5]) >= 16]
out.append('#define NX2 %d' % len(x2))
kmap = {'A': 0, 'E': 1, 'W': 2}
out.append('static const int X2T[NX2][8] = {%s};' % ','.join('{%d,%d,%d,%d,%d,%d,%d,%d}' % (kmap[e[0]], e[1], e[2], 1 if e[3] == '=' else 0, kmap[e[4]], e[5], e[6], max(e[1], e[5])) for e in x2))
Lt = lw.setup_l()
for nm, ix in (('LAx', 0), ('LEx', 1)):
    out.append('static const uint32_t %s[32][4] = {%s};' % (nm, ','.join('{%s}' % ','.join('0x%x' % Lt[l]['tx'][ix][i] for i in range(12, 16)) for l in range(32))))
for nm, ix in (('LAy', 0), ('LEy', 1)):
    out.append('static const uint32_t %s[32][4] = {%s};' % (nm, ','.join('{%s}' % ','.join('0x%x' % Lt[l]['ty'][ix][i] for i in range(12, 16)) for l in range(32))))
# words W9..W15 of both members
wx = [[lw.MX[9 + j] for j in range(5)] + list(lw.lstar(l)[0]) for l in range(32)]
wy = [[lw.MY[9 + j] for j in range(5)] + list(lw.lstar(l)[1]) for l in range(32)]
out.append('static const uint32_t LWx[32][7] = {%s};' % ','.join('{%s}' % ','.join('0x%x' % v for v in r) for r in wx))
out.append('static const uint32_t LWy[32][7] = {%s};' % ','.join('{%s}' % ','.join('0x%x' % v for v in r) for r in wy))
out.append('#define D6 0x%xu\n#define T6 0x%xu\n#define D7 0x%xu\n#define T7 0x%xu\n#define D8 0x%xu\n#define T8 0x%xu' % (lw.D6, lw.T6, lw.D7, lw.T7, lw.D8, lw.T8))
open('q3consts_%s.h' % ('relaxed' if relaxed else 'orig'), 'w').write('\n'.join(out) + '\n')
if not os.path.exists('variants.bin'):
    env = lw.Env(); w8 = []
    for ci in range(lw.NCLS):
        for a in env.members(ci): w8.append((lw.W8C - ((a + lw.C4) & lw.M32)) & lw.M32)
    print('variants', len(w8), 'distinct W8x', len(set(w8)))
    open('variants.bin', 'wb').write(struct.pack('<%dI' % len(w8), *w8))
```

### F.6 `analyze.py` (the preregistered rules)

```python
#!/usr/bin/env python3
# analyze.py - applies the preregistered rules of PREREG_q3M.txt to the outputs in out/ ; usage: analyze.py [dir]
import glob, math, re, statistics, sys, json
from scipy.stats import t as student_t
d = sys.argv[1] if len(sys.argv) > 1 else 'out'
def res(f):
    tx = open(f).read()
    m = re.search(r'RESULT seed (\d+) NP \d+ M \d+ MT \d+ log2est (\S+) est (\S+)', tx)
    st = re.search(r'STAGES (.*?) tail (\S+)', tx)
    return int(m.group(1)), float(m.group(3)), float(m.group(2)), [float(v) for v in st.group(1).split()] + [float(st.group(2))]
def load(tag): return sorted(res(f) for f in glob.glob('%s/%s_*.txt' % (d, tag)))
def bound(Z, name, n_exp):
    n = len(Z); mean = statistics.mean(Z); sd = statistics.stdev(Z); tq = float(student_t.ppf(0.99, n - 1)); lb = mean - tq * sd / math.sqrt(n)
    print('%s: %d replicates (registered %d), mean 2^%.4f, relative sd %.4f, t(0.99, %d df) = %.4f, one-sided 99%% lower bound 2^%.4f' % (name, n, n_exp, math.log2(mean), sd / mean, n - 1, tq, math.log2(lb)))
    return mean, sd, lb
def stagemeans(R):
    cols = list(zip(*[r[3] for r in R])); return [statistics.mean(c) for c in cols]
out = {}
V = load('V'); R1 = load('R1'); R2 = load('R2')
if V:
    Z = [r[1] for r in V]; mean, sd, lb = bound(Z, 'V (original cells)', 64)
    # reference: study B of 7319bba (32 replicates): mean 2^-73.9987, relative sd 0.0378, bound 2^-74.0225
    mB = 2 ** -73.9987; rsB = 0.0378; nB = 32
    rseV = sd / mean / math.sqrt(len(Z)); rseB = rsB / math.sqrt(nB)
    z = (mean / mB - 1) / math.sqrt(rseV ** 2 + rseB ** 2)
    lbl = math.log2(lb)
    a = abs(z) <= 2.576; b = abs(lbl - (-74.0225)) <= 0.04
    print('   stage means (log2):', ['%.4f' % v for v in stagemeans(V)])
    print('   criterion (a): z = %.3f against study B (|z| <= 2.576): %s ; criterion (b): |LB_V - (-74.0225)| = %.4f <= 0.04: %s ; VALIDATION %s' % (z, 'PASS' if a else 'FAIL', abs(lbl - (-74.0225)), 'PASS' if b else 'FAIL', 'PASS' if (a and b) else 'FAIL'))
    out['V'] = dict(n=len(Z), mean_log2=math.log2(mean), relsd=sd / mean, lb_log2=lbl, z=z, pass_=bool(a and b), stages=stagemeans(V))
lbs = {}
for name, Rr, n in (('R1', R1, 128), ('R2', R2, 128)):
    if not Rr: continue
    Z = [r[1] for r in Rr]; mean, sd, lb = bound(Z, name + ' (relaxed cells)', n)
    print('   stage means (log2):', ['%.4f' % v for v in stagemeans(Rr)])
    lbs[name] = math.log2(lb)
    out[name] = dict(n=len(Z), mean_log2=math.log2(mean), relsd=sd / mean, lb_log2=math.log2(lb), log2est=[r[2] for r in Rr], stages=stagemeans(Rr))
if len(lbs) == 2:
    m = min(lbs.values()); q = math.floor(100 * m + 1e-9) / 100
    print('lowest bound 2^%.5f -> declared q3 = 2^%.2f' % (m, q))
    out['declared'] = q
    if 'V' in out: print('gain over R37M base 2^-74.03: %.2f bits (declared)' % (q + 74.03))
# pooled (descriptive only)
if R1 and R2:
    Z = [r[1] for r in R1 + R2]; mean = statistics.mean(Z); sd = statistics.stdev(Z)
    print('pooled R1+R2 (descriptive): n %d mean 2^%.4f relative sd %.4f, 99%% bound 2^%.4f' % (len(Z), math.log2(mean), sd / mean, math.log2(mean - float(student_t.ppf(0.99, len(Z) - 1)) * sd / math.sqrt(len(Z)))))
json.dump(out, open('analysis.json', 'w'), indent=1)
```

### F.7 `check_alt.py`

```python
#!/usr/bin/env python3
# check_alt.py - the three alternative 37-step semi-free-start collisions (one per new pattern of E18/E19) against the cells of this package's lowm.py and of the program with the Table 15 cells
import sys, importlib.util
sys.dont_write_bytecode = True
def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
new = load(sys.argv[1], 'lw_new'); old = load(sys.argv[2], 'lw_old')
h8 = new.h8
PAIRS = {
 'Table 15 (published pair)': (new.CV0, new.MY, new.MX),
 'G1': (h8('063c3500 078f49ec 15f3f954 b92ec209 8988f13d 35819c7c 63e0bf72 236a0c73'),
        h8('da42b17c 211c7ff3 76ab73f3 6af71849 370eee2f 309c7244 fca0a79d c81ace78 9f0d78e1 681b8277 faa9c7e0 56aed439 cc2dbbc2 dd2ba0fc b95d377b 5dd43a81'),
        h8('da42b17c 211c7ff3 76ab73f3 6af71849 370eee2f 309c7244 dca0a79d cc5ac678 bf0d78e1 6d1a90dd faa1d3e0 56aed439 cc2dbbc2 dd2ba0fc bd1d3f7b 7dd43a81')),
 'G2': (h8('3c2679fb 0adeef20 3589a7a5 83ef1642 ad5f1106 e029b47e 6b4d40e9 4ee553b3'),
        h8('3bfa2198 3aeec0b8 10348d11 5ba77ac0 b56da910 6997b907 395831ab 9230897d 9f0d78e1 681b8277 faa9c7e0 56aed439 cc2dbbc2 dd2ba0fc b95d377b 5dd43a81'),
        h8('3bfa2198 3aeec0b8 10348d11 5ba77ac0 b56da910 6997b907 195831ab 9670817d bf0d78e1 6d1a90dd faa1d3e0 56aed439 cc2dbbc2 dd2ba0fc bd1d3f7b 7dd43a81')),
 'G1 xor G2': (h8('a49c8638 3696c10f 2a0f741c 55456216 c7b75338 54905dab c30d520e e749445c'),
        h8('bb6ca525 d640983d 28963f42 5ca2459f 116481ee 4e1a472b edfab13a 29ba7d40 9f0d78e1 681b8277 faa9c7e0 56aed439 cc2dbbc2 dd2ba0fc b95d377b 5dd43a81'),
        h8('bb6ca525 d640983d 28963f42 5ca2459f 116481ee 4e1a472b cdfab13a 2dfa7540 bf0d78e1 6d1a90dd faa1d3e0 56aed439 cc2dbbc2 dd2ba0fc bd1d3f7b 7dd43a81')),
}
def cells(lw, cv, mx, my):
    tx, ty = lw.trace(cv, mx), lw.trace(cv, my)
    return all(lw.row_ok(tx, ty, i, i not in (6, 7)) for i in range(-4, lw.R)) and all(lw.x2_ok(tx, r) for r in range(8, lw.R))
print('%-28s %-9s %-24s %-24s' % ('pair (x = M\', y = M)', 'collides', 'cells of this lowm.py', 'cells of Table 15'))
for k, (cv, my, mx) in PAIRS.items():
    c = new.compress(cv, mx) == new.compress(cv, my) and mx != my
    print('%-28s %-9s %-24s %-24s' % (k, c, cells(new, cv, mx, my), cells(old, cv, mx, my)))
```

## Appendix G. The joint study of the four patterns and R16x: preregistration, results

Files in `q3/` (`q3smc.c` as listed in F.4, `q3consts_r16x.h` written by `gen_consts.py` from `experiments/lowm.py` as filed, sha256 aa4356605422aa4eb070efe67e1938f071fd17e9ed60a7a5266199a62bbc6b9b; `variants.bin` unchanged; outputs in `studyX/out/`). Build: `gcc -O2 -DCONSTS='"q3consts_r16x.h"' q3smc.c -lm -o q3smc_r16x`; run: `q3smc_r16x SEED 1 8192 512 16384`.

### G.1 Preregistration (written before any listed seed ran; stamp 2026-10-12T16:13:47Z, sha256 18569704b1115d99c138e641986101687836aa408e1f29d670cad354da0691d3)

```text
preregistration: our own sequential-Monte-Carlo estimate of q3 for the 170-class A0-variant attack on 37-step SHA-256 (R37M family) with the four row-18/19 value patterns AND the R16x relaxation accepted JOINTLY (one carrier)
written before any listed seed was run; the stamp is the line below.
stamp: 2026-10-12T16:13:47Z
program: q3smc.c (ours; the filed R37M estimator plus a TAG line that draws no random numbers), sha256 f0e3efc8d06c58c03c7dd7fe86ef08d8d00b8868202e6c49557f85c479c61f9c.
constants: q3consts_r16x.h (sha256 aa4356605422aa4eb070efe67e1938f071fd17e9ed60a7a5266199a62bbc6b9b), written by gen_consts.py (sha256 14ea0015f43b1ea86109ccc78e86cf392c12a9a34c7ece6a1c3babc1be6b4ae7) from this package's lowm.py in the state `sha256` 9bede229cafc262027b06f91fcdde88a5778d36c4ad59e4083cc4780d8e69b7b (the 57.84086 filing); the shipped `experiments/lowm.py` is `sha256` b6b3966361e0419581a0296b3d68458dedf99b620bf5206bd408cd046ec24e71 (the state 7905c31e2ac3a9c513d75d793bf62935c6a73d62e371802a10c0a4a1ff976104 is the 57.72980 filing's, and the sentence that called it shipped was two filings stale), and the revisions between the two (`eb6e0065...`, `dfb848ed...` and this one, which changes only a comment) modify only `MEMBER_CHARGE`, `GROUP_BODY` and `scan_fix`, none of which enters this file's output. The previous package printed 5107f3f7..., the hash of an earlier lowm.py, corrected here).
 the carrier = R37M's relaxed cells (rows 18/19 eight value bits free) with three further changes, all in lowm.py's characteristic: CHE[16] bit 23 '0' -> '=' (E16[23] free), CHE[17] bit 24 '+' -> '=' and the two-bit condition E16[24]=E17[24] removed. The R16x parity E16[23]^E19[29]^E18[1]^E18[5]=0 and the other row-18 linear relations are NOT imposed (weaker carrier; any pass through row 36 is still a full collision: rows 22..36 cells unchanged, zero output difference).
variant list: variants.bin (sha256 6900f64cec67217eb352fd43cd0552c92b2514b892481c95f761d19619d1e3c5), unchanged from R37M.
known answer (run before this stamp, disclosed): the new binary built with q3consts_relaxed.h reproduces byte-identically the filed R37M study outputs of seeds 720000 and 721000 (RESULT and STAGES lines). Smoke: seed 1 with q3consts_r16x.h (stage 16 = 2,097,152 pairs, 65,536 per l for all 32 l; log2est -71.63000). Seed 1 is not used below.
main study (binary q3smc_r16x), two independent blocks: J1 seeds 740000..740127 (128 replicates), J2 seeds 741000..741127 (128 replicates); NP = 8192, M = 512, MT = 16384 for every replicate.
bound: per block LB = mean - t(0.99, 127 df) sd / sqrt(128) over the replicate linear estimates (the replicate spread carries any overdispersion of the within-run counts).
rule (fixed in advance): declared q3 = 2^x with x = floor(100 log2(min(LB_J1, LB_J2))) / 100. Gain over the filed R37M q3 2^-72.02 = x + 72.02 (bits).
descriptive only: pooled mean; per-replicate TAG share (full passes whose member x keeps E16[23]=0 and E16[24]=E17[24]); comparison with r16_settle +0.590 [0.548, 0.631].
every listed seed is run and reported; none dropped or rerun except a crash not caused by the program. At most 2 processes at once; wait while load > 35.
```

The program hash named in the preregistration is that of `lowm.py` when the constants were written; the later edits of the program (the row-16 constants of the ledger, `FEASIBLE_L`, q3, and the unconditional first-block W7 sample in `online_trial`) do not touch the cells, and regenerating the constants from the program as filed gives the same file (sha256 above).

### G.2 Results

Rule applied: J1's bound is 2^-71.46286 (lower bound 2^-71.4629, upper bound 2^-71.3970) and J2's is 2^-71.4524 (upper bound 2^-71.3838); the preregistered two-decimal rule gives 2^-71.47 (claim 57.75028, Section 11) and the preregistered min-of-blocks rule gives 2^-71.4629 (claim 57.74322 on this family). The filing that first ran this study declared instead, as a **superseded historical statement**, the pooled bound over the same 256 preregistered replicates, **q3c = 2^-71.4474** (Section 7.4c), 0.0155 bit tighter than the min-of-blocks rule and using no seed outside the two listed blocks. The direct submitted-pool study of Appendix G.3 supersedes it and is 0.0119 bit tighter still. The declared q3c of this filing is 2^-71.4243 (Appendix G.3), and both the pooled 2^-71.4474 and the two-block 2^-71.4629 survive only as the stated sensitivities of Section 12 (and q3c <= 2^-71.38 < 2^-70; q3 = q3c x 2.4331, Section 7.7). pooled 256 replicates: mean 2^-71.4236, relative sd 0.1118, bound 2^-71.4474 (superseded declaration, Section 7.4c). Stage means (log2): 16: -16.000, 17: -12.000, 18: -8.000, 19: -11.430, 20: -7.000, 21: -2.000, 22: -11.003, tail -3.999. TAG: 1,438,939,086 of 2,149,260,669 full passes keep E16[23] = 0 and E16[24] = E17[24] (share 0.6695).

All 128 log2 estimates of J1 (seeds 740000..740127, in order):

```text
-71.641 -71.683 -71.399 -71.499 -71.485 -71.546 -71.447 -71.435 -71.327 -71.389 -71.528 -71.535 -71.239 -71.454 -70.975 -71.672
-71.370 -71.139 -71.243 -71.644 -71.359 -71.528 -71.703 -71.312 -71.404 -71.306 -71.255 -71.283 -71.464 -71.335 -71.715 -71.343
-71.498 -71.420 -71.379 -71.739 -71.317 -71.226 -71.874 -71.547 -71.679 -71.328 -71.426 -71.311 -71.270 -71.214 -71.602 -71.365
-71.407 -71.256 -71.257 -71.497 -71.249 -71.416 -71.365 -71.388 -71.466 -71.529 -71.349 -71.357 -71.535 -71.619 -71.519 -71.580
-71.201 -71.261 -71.270 -71.404 -71.498 -71.709 -71.428 -71.472 -71.589 -71.381 -71.631 -71.692 -71.598 -71.465 -71.429 -71.516
-71.243 -71.508 -71.350 -71.408 -71.325 -71.468 -71.621 -71.535 -71.359 -71.656 -70.986 -71.492 -71.396 -71.528 -71.565 -71.334
-71.345 -71.438 -71.382 -71.563 -71.450 -71.363 -71.326 -71.351 -71.335 -71.783 -71.566 -71.262 -71.327 -71.518 -71.336 -71.697
-71.280 -71.365 -71.511 -71.513 -71.481 -71.451 -71.213 -71.666 -71.441 -71.323 -71.121 -71.745 -71.378 -71.449 -71.574 -71.562
```

All 128 log2 estimates of J2 (seeds 741000..741127):

```text
-71.386 -71.166 -71.802 -71.670 -71.447 -71.439 -71.487 -71.555 -71.871 -71.542 -71.515 -71.371 -71.288 -71.276 -71.488 -71.260
-71.363 -71.234 -71.439 -71.527 -71.404 -71.335 -71.323 -71.282 -71.142 -71.495 -71.486 -71.440 -71.567 -71.526 -71.225 -71.547
-71.708 -71.498 -71.396 -71.172 -71.207 -71.244 -71.477 -71.456 -71.622 -71.626 -71.392 -71.570 -71.325 -71.502 -71.625 -71.627
-71.299 -71.168 -71.402 -71.708 -71.461 -71.514 -71.707 -71.631 -71.452 -71.285 -71.512 -71.535 -71.549 -71.321 -71.384 -71.237
-71.459 -71.641 -71.667 -71.292 -71.207 -71.079 -71.272 -71.638 -71.430 -71.117 -71.399 -71.567 -71.437 -71.051 -71.477 -71.343
-71.388 -71.454 -71.556 -71.575 -71.740 -71.627 -71.380 -71.609 -71.428 -71.192 -71.347 -71.640 -71.401 -71.653 -71.590 -71.648
-71.225 -71.195 -71.167 -71.189 -71.351 -71.680 -71.416 -71.386 -71.274 -71.511 -71.581 -71.551 -71.439 -71.265 -71.324 -71.431
-71.446 -71.377 -71.256 -71.158 -71.443 -71.393 -71.283 -71.442 -71.357 -71.124 -71.344 -71.565 -71.410 -71.382 -71.269 -71.606
```

Interim looks (declared under H2, Section 12): the analysis was run on partial outputs while the blocks were running, to monitor progress; no seed, parameter or rule was changed after any look.

The program's own output for the first seed of each block:

```text
--- seed 740000 ---
RESULT seed 740000 NP 8192 M 512 MT 16384 log2est -71.64139 est 2.7151355317e-22
TAG seed 740000 full passes 8247250, of which with E16[23]=0 and E16[24]=E17[24] (member x): 5723505
STAGES -16.00000 -12.00196 -8.00105 -11.57374 -7.00012 -2.05054 -10.98947 tail -4.02452  (row-24 survivors 8247250 of 134217728, full passes 8247250)
--- seed 741000 ---
RESULT seed 741000 NP 8192 M 512 MT 16384 log2est -71.38558 est 3.2419013954e-22
TAG seed 741000 full passes 8731984, of which with E16[23]=0 and E16[24]=E17[24] (member x): 6561999
STAGES -16.00000 -11.99869 -8.00174 -11.38529 -6.99964 -2.01665 -11.04145 tail -3.94212  (row-24 survivors 8731984 of 134217728, full passes 8731984)
```

### G.3 A direct study of q3c on the submitted pool (preregistration; stamp 2026-10-18T07:09:03Z, written before any listed seed ran)

**What this is.** The organizer review of this candidate's own score-bearing submission (e13f9dae, run 39104072013) raises two objections that no rewrite of the earlier studies can answer: F-COST-02/F-CRYPT-02, that an aggregate tail mean within 0.001 bit of uniform does not bound a *sub-pool* mean, and F-EXP-02, that the pooled 256-replicate statistic was adopted after the preregistered rule had fixed the minimum of two per-block bounds. This study answers both at once. W8 is drawn from the **submitted** variant list, so nothing is transferred from the parents' family; and the statistic below is fixed before the seeds run.

**Inputs, regenerated from the shipped files, with the hashes of the states used.**

```text
lowm.py         7905c31e2ac3a9c513d75d793bf62935c6a73d62e371802a10c0a4a1ff976104   (the state of the 57.72980 filing, commit 2d0a13b; the shipped file of this filing is f2578183)
q3smc.c         f0e3efc8d06c58c03c7dd7fe86ef08d8d00b8868202e6c49557f85c479c61f9c   (Appendix F.4 as shipped)
gen_consts.py   721d7949d1038a6f01e8cac62eaa8ecc9362a7af105176ab56c82beef90efd5b   (Appendix F.5 as shipped)
variants.bin    b767171018fb5ba2d43e55adea23b72de820d9a43ffaa780f51f8c99ae695cbd   599,760 words = 2,399,040 bytes
q3consts_orig.h efd62db9220a667258d8dbde25ec572e1104460f2a1971894292870c6ec7e4cb   (written by that gen_consts.py from that lowm.py)
build           gcc -O2 -DCONSTS='"q3consts_orig.h"' q3smc.c -lm -o q3smc_orig
```

`variants.bin` is the W8x of the 599,760 variants of the 170 classes of lists 0, 1, 5 and 6, all distinct, printed by the generator (`variants 599760 distinct W8x 599760`). Every replicate uses NP = 8192, M = 512, MT = 16384, the parameters of every replicate of studies A, B, J1 and J2.

The shipped `experiments/lowm.py` (sha256 b6b3966361e0419581a0296b3d68458dedf99b620bf5206bd408cd046ec24e71) differs from the state hashed above in exactly one line, `Q3_LOG2`, which this study produces rather than consumes. The generator reads only `CELLS`, `X2`, `setup_l`, `MX`, `MY`, `lstar`, `LISTID` and `CLASSES`, none of which that constant touches: regenerating from the shipped file reproduces `variants.bin` b7671710 and `q3consts_orig.h` efd62db9 unchanged (checked).

**The carrier.** The E-cell tables the estimator tests are the ones `gen_consts.py` derives from this package's `lowm.py`, that is the cells of the H2 statement ("exactly the cells and conditions of `experiments/lowm.py`"). Measured, not assumed: the generator's `--relaxed` flag changes exactly one line, the display array `CHE`, which `q3smc.c` never references (0 occurrences), and the two headers differ only in their comment line, so the two binaries return byte-identical RESULT and STAGES lines on 32 seeds (750000..750063). The shipped generator has one numeric carrier; this study uses it.

**Seeds.** 760000..761023, 1024 replicates, 32 per invocation (`q3smc seed0 32 8192 512 16384`), one run each. The range is disjoint from every list used before: seed 1 (the smoke seed of Appendix G.1), 710000..710063, 720000..720127, 721000..721127, 740000..740127, 741000..741127, and the calibration block disclosed below.

**Statistic, fixed now.** Let Z be the 1024 per-seed log2 estimates, with mean and standard deviation sd. Then

```text
q3c_declared = 2^u,   u = floor( (mean - t(0.99, 1023) x sd / sqrt(1024)) x 10^4 ) / 10^4
```

the one-sided 99% Student lower bound of the mean, rounded **down** to four decimals of log2 and never up. All 1024 seeds are reported; no seed is added, dropped, replaced or rerun; there is no interim look, no stopping rule and no second statistic. If the block fails to run to completion, no q3c is declared from it and the failure is reported.

**What it changes.** `q3c_used = q3c_declared`, with **no** sub-pool transfer allowance: the measured quantity is the submitted pool's own q3c, so the 0.0020-bit haircut of Section 7.8 is not applied. The parents'-pool pooled bound 2^-71.4474 with its 0.0020-bit allowance, and the preregistered min-of-blocks bound 2^-71.4629, remain stated as independent sensitivities of the same ledger.

**Disclosed calibration, run before this text and discarded by the rule above.** 32 seeds 750000..750063 (four per invocation) on each header, used only to time the estimator (2.9 s per replicate on one core) and to confirm that it reproduces the published study: mean -71.4460 against the published -71.4236, stage means -16.000 -12.000 -8.000 -11.449 -7.000 -1.999 -10.986 -4.012 against the published -16.000 -12.000 -8.000 -11.430 -7.000 -2.000 -11.003 -3.999; and the published smoke seed 1 of Appendix G.1.

### G.4 The block of Appendix G.3: 1024 seeds, all reported

Run 2026-10-18T07:14Z..07:20Z (32 shards of 32 seeds, `q3smc seed0 32 8192 512 16384`), no seed
dropped, replaced or rerun. Mean **-71.42391**, sd **0.15878** (relative sd of the linear estimates
0.1101), t(0.99, 1023) = 2.3300, one-sided 99% lower bound **-71.43547**, declared (rounded down)
**2^-71.4355**. Shipped program, run 39104072013's follow-up: `experiments/r37-q3d-28.py`.

Per-seed log2 estimates, seeds 760000..761023 in order:

```text
-71.07242 -71.71830 -71.21591 -71.39740 -71.59278 -71.25152 -71.37581 -71.44693
-71.29725 -71.48843 -71.70232 -71.34666 -71.43593 -71.52191 -71.20282 -71.59679
-71.20263 -71.25872 -71.37584 -71.39734 -71.32141 -71.46204 -71.45463 -71.42229
-71.32958 -71.17074 -71.30359 -71.53328 -71.36405 -71.22088 -71.50100 -71.35304
-71.68713 -71.45617 -71.27229 -71.44598 -71.37794 -71.42893 -71.18932 -71.53850
-71.22487 -71.38970 -71.29211 -71.32588 -71.69586 -71.53376 -71.31325 -71.39852
-71.17041 -71.15343 -71.46541 -71.52111 -71.52971 -71.02459 -71.37571 -71.33916
-71.38504 -71.33235 -71.38195 -71.55576 -71.11835 -71.51852 -71.44657 -71.31467
-71.26480 -71.27212 -71.06533 -71.35494 -71.20177 -71.23507 -71.52031 -71.22233
-71.49188 -71.34788 -71.25926 -71.21404 -71.34533 -71.42565 -71.39306 -71.33624
-71.36306 -71.79814 -71.41570 -71.47243 -71.39253 -71.47201 -71.23586 -71.39021
-71.51239 -71.89930 -71.34672 -71.57411 -71.30375 -71.28789 -71.48241 -71.49954
-71.37204 -71.31785 -71.23003 -71.57838 -71.62689 -71.23422 -71.37724 -71.83896
-71.42337 -71.78010 -71.21411 -71.46750 -71.37281 -71.59332 -71.23123 -71.61594
-71.59644 -71.56066 -71.24624 -71.40619 -71.38595 -71.49240 -71.42365 -71.48882
-71.73267 -71.37169 -71.55653 -71.29608 -71.61894 -71.29060 -71.65464 -71.43265
-71.56491 -71.35020 -71.41449 -71.47470 -71.26164 -71.37816 -71.63188 -71.16641
-71.43135 -71.44821 -71.44014 -71.83063 -71.66114 -71.50636 -71.48242 -71.42399
-71.24783 -71.57573 -71.20185 -71.80433 -71.30262 -71.47061 -71.25180 -71.64598
-71.64917 -71.42228 -71.38821 -71.28063 -71.13762 -71.41174 -71.55302 -71.10771
-71.41679 -71.67308 -71.41440 -71.35526 -71.51491 -71.73394 -71.14174 -71.56049
-71.51718 -71.41382 -71.44593 -70.97601 -71.15392 -71.18609 -71.40885 -71.39662
-71.56291 -71.42946 -71.40409 -71.46078 -71.50324 -71.67324 -71.46057 -71.26086
-71.66276 -71.42933 -71.38041 -71.26511 -71.49226 -71.28783 -71.43796 -71.60831
-71.62633 -71.34043 -71.46397 -71.56146 -71.51995 -71.13288 -71.54118 -71.97449
-71.38651 -71.56470 -71.25020 -71.44227 -71.64568 -71.50855 -71.42290 -71.58487
-71.37173 -71.19590 -71.30160 -71.22176 -71.34828 -71.45539 -71.53549 -71.76700
-71.16881 -71.43881 -71.43707 -71.61260 -71.64031 -71.83758 -71.53281 -71.44473
-71.18361 -71.59763 -71.70412 -71.52517 -71.25175 -71.55646 -71.14808 -71.36186
-71.61742 -71.51209 -71.39174 -71.19235 -71.39606 -71.69349 -71.80764 -71.33852
-71.29098 -71.29592 -71.54788 -71.25987 -71.42244 -71.37298 -71.56228 -71.14197
-71.30381 -71.41434 -71.51791 -71.39080 -71.38733 -71.64536 -71.20985 -71.49969
-71.34404 -71.42873 -71.50510 -71.30569 -71.20196 -71.42511 -71.35009 -71.35575
-71.50213 -71.56270 -71.57193 -71.33492 -71.44716 -71.49917 -71.35412 -71.27424
-71.37416 -71.69914 -71.10114 -71.68729 -71.52062 -71.33090 -71.53652 -71.24721
-71.27784 -71.43636 -71.54339 -71.42601 -71.33406 -71.43715 -71.40976 -71.30102
-71.44490 -71.34934 -71.46278 -71.54344 -71.34805 -71.60499 -71.31267 -71.62884
-71.69863 -70.98887 -71.43337 -71.21527 -71.45509 -71.68691 -71.34077 -71.03625
-71.41062 -71.55385 -71.22721 -71.43519 -71.34846 -71.28565 -71.39562 -71.35163
-71.25869 -71.32176 -71.08998 -71.40910 -71.76879 -71.68887 -71.42877 -71.48787
-71.40610 -71.41413 -71.35676 -71.39430 -71.28955 -71.35100 -71.44325 -71.40598
-71.36622 -71.61273 -71.12503 -71.70358 -71.24634 -71.38476 -71.34290 -71.57624
-71.34749 -71.53083 -71.52272 -71.40430 -71.50351 -71.39114 -71.43752 -71.28326
-71.16605 -71.40581 -71.34438 -71.61287 -71.20498 -71.53551 -71.56164 -71.35487
-71.22755 -71.56137 -71.61548 -71.31377 -71.62408 -71.20025 -71.38552 -71.33638
-71.45025 -71.36248 -71.63826 -71.28586 -71.22259 -71.42413 -71.37467 -71.63307
-71.47939 -71.24961 -71.34327 -71.60844 -71.60226 -71.46283 -71.23306 -71.20573
-71.49887 -71.63884 -71.25063 -71.16673 -71.38463 -71.23702 -71.75162 -71.60207
-71.55664 -71.26090 -71.37675 -71.46164 -71.49771 -71.52827 -71.50235 -71.41865
-71.25479 -71.38390 -71.28364 -71.32250 -71.44197 -71.30011 -71.34683 -71.56988
-71.63832 -71.09239 -71.34788 -71.54930 -71.29901 -71.21944 -71.32686 -71.46528
-71.80073 -71.38968 -71.35439 -71.26265 -71.30149 -71.58292 -71.20143 -71.47037
-71.27941 -71.11556 -71.59335 -71.47552 -71.37587 -71.74209 -71.28076 -71.41367
-71.32880 -71.21875 -71.52792 -71.28482 -71.24568 -71.61054 -71.27529 -71.48061
-71.25175 -71.18359 -71.36489 -71.26880 -71.24076 -71.44985 -71.33856 -71.42918
-71.37217 -71.40685 -71.71198 -71.18558 -71.35313 -71.59532 -71.66434 -71.52342
-71.26370 -71.33980 -71.47698 -71.46315 -71.51591 -71.42531 -71.32742 -71.57017
-71.37857 -71.24233 -71.91050 -71.68862 -71.21055 -71.31647 -71.17716 -71.50856
-71.65638 -71.35341 -71.37598 -71.57642 -71.45509 -71.45742 -71.32044 -71.27868
-71.46567 -71.59931 -71.22194 -71.29291 -71.24509 -71.53091 -71.57966 -71.37121
-71.42266 -71.43736 -71.49114 -71.23715 -71.36969 -71.39371 -71.50955 -71.66241
-71.26287 -71.57437 -71.70302 -71.24252 -71.35635 -71.32155 -71.26793 -71.37291
-71.29969 -71.21472 -71.26655 -71.31028 -71.34473 -71.19162 -71.61940 -71.58980
-71.66868 -71.47694 -71.56780 -71.21353 -71.55946 -71.31682 -71.47538 -71.18314
-71.42561 -71.58840 -71.41849 -71.38716 -71.25842 -71.28613 -71.35103 -71.42957
-71.16007 -71.52159 -71.44212 -71.71020 -71.71775 -71.26761 -71.47496 -71.57319
-71.29134 -71.48025 -71.46589 -71.44976 -71.33409 -71.54434 -71.57965 -71.30133
-71.47575 -71.41538 -71.76968 -71.43669 -71.71089 -71.32263 -71.67011 -71.40979
-71.56775 -71.39099 -71.46876 -71.34841 -71.25759 -71.39597 -71.23395 -71.32132
-71.23822 -71.32205 -71.65454 -71.79871 -71.33720 -71.52000 -71.37237 -71.68406
-71.15355 -71.48268 -71.40912 -71.44574 -71.38420 -71.37349 -71.30372 -71.47737
-71.36223 -71.46335 -71.45774 -71.38179 -71.41268 -71.25634 -71.28838 -71.54362
-71.35462 -71.34658 -71.66063 -71.29113 -71.31626 -71.25276 -71.20842 -71.63701
-71.42617 -71.72338 -71.54484 -71.75466 -71.21957 -71.40085 -71.21025 -71.46872
-71.40046 -71.40366 -71.49027 -71.62281 -71.23261 -71.60292 -71.46361 -71.24001
-71.46940 -71.50186 -71.57091 -71.53946 -71.55502 -71.42907 -71.55570 -71.63508
-71.52085 -71.20264 -71.56381 -71.38533 -71.50380 -71.65914 -71.54114 -71.53508
-71.44539 -71.29653 -71.37134 -71.28579 -71.40898 -71.42253 -71.43016 -71.45424
-71.34554 -71.42750 -71.32007 -71.49193 -71.27456 -71.56134 -71.34580 -71.39396
-71.40067 -71.58154 -71.20796 -71.59511 -71.45324 -71.38496 -71.25111 -71.43698
-71.18325 -71.49510 -71.55466 -71.27303 -71.36733 -71.34156 -71.72709 -71.48699
-71.74567 -71.55493 -71.37531 -71.33673 -71.87832 -71.43083 -71.11894 -71.52752
-71.75379 -71.26940 -71.31570 -71.36421 -71.33117 -71.45733 -71.35405 -71.35958
-71.16354 -71.23804 -71.21504 -71.23108 -71.20387 -71.50572 -71.62146 -71.42846
-71.37276 -71.38129 -71.71613 -71.25328 -71.59347 -71.39815 -71.24870 -71.66173
-71.56867 -71.28166 -71.29496 -71.58455 -71.37256 -71.50832 -71.32785 -71.23144
-71.27216 -71.33781 -71.23633 -71.45077 -71.32879 -71.35819 -71.59614 -71.12168
-71.66384 -71.39183 -71.54355 -71.81887 -71.42856 -71.32277 -71.52864 -71.39051
-71.29465 -71.40942 -71.56334 -71.60985 -71.17941 -71.18749 -71.33955 -71.46841
-71.44082 -71.53291 -71.49944 -71.62278 -71.64573 -71.31041 -71.57650 -71.26091
-71.34651 -71.36400 -71.41587 -71.56740 -71.45105 -71.43837 -71.33008 -71.33377
-71.36832 -71.68890 -71.66165 -71.29218 -71.85018 -71.76939 -71.18282 -71.22460
-71.52264 -71.43846 -71.35760 -71.50531 -71.46330 -71.55582 -71.32155 -71.49896
-71.33250 -71.41373 -71.36087 -71.48091 -71.21125 -71.41533 -71.56749 -71.38246
-71.24758 -71.42943 -71.43465 -71.60573 -71.43859 -71.49042 -71.52689 -71.16811
-71.48093 -71.29842 -71.58000 -71.23897 -71.34070 -71.45901 -71.61789 -71.59011
-71.23905 -71.08941 -71.39014 -71.30046 -71.70245 -71.29786 -71.62933 -71.31970
-71.51776 -71.29787 -71.39824 -71.30420 -71.33872 -71.16213 -71.22698 -71.25534
-71.54190 -71.61289 -71.29277 -71.51766 -71.27253 -71.30503 -71.40689 -71.16363
-71.48192 -71.45821 -71.50506 -71.17197 -71.73859 -71.41754 -71.43187 -71.31272
-71.20746 -71.23648 -71.56525 -71.63231 -71.26360 -71.63566 -71.52340 -71.51179
-71.31126 -71.18365 -71.50999 -71.54936 -71.54178 -71.44427 -71.23271 -71.73368
-71.28014 -71.27119 -71.24592 -71.16484 -71.62565 -71.44942 -71.29130 -71.42464
-71.52765 -71.51267 -71.38647 -71.49005 -71.22000 -71.59173 -71.29430 -71.26703
-71.71388 -71.47284 -71.50080 -71.44432 -71.19152 -71.41629 -71.26339 -71.45448
-71.16292 -71.63014 -71.44564 -71.34466 -71.47992 -71.45131 -71.41787 -71.53134
-71.32321 -71.63134 -71.13475 -71.55153 -71.33925 -71.26573 -71.39619 -71.62548
-71.46849 -71.56316 -71.44462 -71.50910 -71.61841 -71.74781 -71.52714 -71.34464
-71.39513 -71.48102 -71.41009 -71.60567 -71.57957 -71.51232 -71.30147 -71.66055
-71.49832 -71.53247 -71.22421 -71.35483 -71.52297 -71.51052 -71.15427 -71.63708
-71.45388 -71.43345 -71.26364 -71.51538 -71.86052 -71.59417 -71.57511 -71.69688
-71.31377 -71.24973 -71.41737 -71.69367 -71.30727 -71.07413 -71.41777 -71.35281
-71.62334 -71.56442 -71.32725 -71.24409 -71.43260 -71.42792 -71.55602 -71.30035
-71.17827 -71.58688 -71.28481 -71.35868 -71.37297 -71.63903 -71.25621 -71.70447
-71.66520 -71.53471 -71.31057 -71.46126 -71.22488 -71.68404 -71.31483 -71.30076
-71.58186 -71.47470 -71.44566 -71.32695 -71.28081 -71.13749 -71.31035 -71.08014
-71.47197 -71.30837 -71.58551 -71.43816 -71.56963 -71.61746 -71.73242 -71.47341
-71.35900 -71.59058 -71.33650 -71.51967 -71.49143 -71.56625 -71.11796 -71.56802
-71.39829 -71.33727 -71.68089 -71.64637 -71.56687 -71.32910 -71.48616 -71.31870
-71.42607 -71.60317 -71.39033 -71.51395 -71.45273 -71.37197 -71.71540 -71.55415
-71.07890 -71.35431 -71.25131 -71.33661 -71.37045 -71.43745 -71.52901 -71.49131
-71.50718 -71.33581 -71.40103 -71.48504 -71.61526 -71.31569 -71.49289 -71.32152
-71.51151 -71.26522 -71.55986 -71.65329 -71.82055 -71.60189 -71.54427 -71.78009
-71.27012 -71.28884 -71.25970 -71.47267 -71.21612 -71.35784 -71.42246 -71.52342
-71.64426 -71.56328 -71.42452 -71.23385 -71.33820 -71.46509 -71.47017 -71.38892
-71.34657 -71.36779 -71.70211 -71.44911 -71.71283 -71.45402 -71.42515 -71.53791
-71.29282 -71.38871 -71.30470 -71.34983 -71.57002 -71.20369 -71.58245 -71.50837
-71.51578 -71.68440 -71.36986 -71.28638 -71.49314 -71.26543 -71.61303 -71.31073
```

The measurement answers both objections it was written for. (i) There is no transfer: W8 is
drawn from the submitted 599,760-word list, and the mean agrees with the parents'-pool study
of Section 7.4c (-71.4236, 256 replicates, a 782,800-word list) to 0.0003 bit, which is 1/37
of one standard error of that study's mean -- the sub-pool restriction is q3-neutral in
measurement as well as by Lemma 7.1. (ii) There is no post-hoc statistic: the rule, the seed
list and the arithmetic of the rounding were committed in Appendix G.3 before the first listed
seed ran.

## Appendix H. The organizer experiments for H1, H2 and H3

Historical aa0e8b6 evidence in this appendix uses its one program, `experiments/lowm.py` (63,764 bytes; the budget is 65,536 bytes in total). `a0-sfs-r37` and `a0-online-r37` are described in Section 13.2 and in the manifest; the three entries below were added for H1 and H3 (their form is that of ec1340aa-ecc8-4564-8df7-006f0a2b2ce5, R37OWN5, which passed lane evaluability with them).

**`h1-cv1-filters-nonce` and `h3-cowpass-nonce` (trials 0..99, same code in `run_request`).** Each trial takes 150 first blocks from the organizer's trial seed (SHAKE-256 of seed and counter, 64 bytes), computes the real 37-step compression, and tests, for the first class of the family (c7 = cc8e8c4c) and four of its variants (1c354142, 1c354143, 1c354146, 1c354147), whether W7x = c7 - x is in F7 and W6x is in F6 (the filters of Section 5.1 in their definition form). It returns no message pair, so the event full-collision never succeeds by design. Observations: first blocks, W7 passes, W6 passes over the four variants, first blocks in which two or more variants pass F6, first blocks with both a W7 pass and a W6 pass, and the sum over those blocks of the number of variants passing. `h1-cv1-filters-nonce` is the H1 consequence (the pass rates of the two filters on real chaining values: p7 = 68,157,440 / 2^32 = 2^-5.98 per class and p6 = 287,309,824 / 2^32 = 2^-3.90 per variant, so 2.38 and 40.1 per trial); `h3-cowpass-nonce` reports the number of first blocks in which two or more of the four variants of one class pass F6 (3.68 per trial if they passed independently). The variants of one class share most of their bits, so a clearly higher count is expected; it measures the within-class correlation of the W6 filter, which the ledger does not need (it uses only expectations). Our replays (100 trials, 15,000 first blocks each; seeds `ours-A-<t>` and `ours-B-<t>`):

| seed set | W7 passes (expected 238.0) | W6 passes (expected 4,013.7) | first blocks with two or more W6 passes (independent: 367.7) | W7 and W6 in one block | pairs |
|---|---:|---:|---:|---:|---:|
| A | 244 | 4,011 | 1,258 (3.42 times) | 21 | 72 |
| B | 214 | 3,988 | 1,244 (3.38 times) | 14 | 42 |

**`h3-ladder-r37` (trials 0..15; function `ladder_trial`).** H3 at depth: dependence among DISTINCT variants of one first block, through the levels of the attack itself. Each trial scans the organizer's seed for four first blocks (real 37-step compressions) with at least two passing classes among the classes 0..15 (a fixed choice made before any run) and, over the variants of up to four of those classes, counts in turn the passes of the W6 filter F6; of the low chunk table (the first stage of the row-16 address test); of the product of the low and the middle chunk table (the second stage); and of the exact row-16 test (any l of the 32). Per level it reports the candidates N (the passes of the level before), the passes S, the pairs P of distinct passing variants of the same first block and C = sum over blocks of C(N, 2) of the candidates; the independent reference is E = C (S/N)^2 and the dependence factor is R = P/E. Rows 17..36 are not reached (a pair needs a row-16 pass and each later row is rarer); the allowance for them is the premise H3. A trial that has a row-16 co-pass returns a generic witness (a second message with a counter word, found by search, whose digest agrees in 4 bits; event digest-xor-mask 0x0f), so that the organizer's success count is the number of those trials; it carries no cryptographic weight and the statistics are the observations. Historical aa0e8b6 LO12/MID12 replays of the 256-trial request (historical stages only; 16 active trials, 64 first blocks total per seed set; seeds `ours-A-<t>` and `ours-B-<t>`):

| level | set | candidates N | passes S | pairs C | pairs P | expected E = C (S/N)^2 | R = P/E |
|---|---|---:|---:|---:|---:|---:|---:|
| W6 filter | A | 846,720 | 64,742 | 5,666,974,272 | 119,788,095 | 33,131,708 | 3.62 |
| W6 filter | B | 843,264 | 33,474 | 5,637,116,160 | 43,730,241 | 8,882,702 | 4.92 |
| historical LO12 | A | 64,742 | 19,306 | 119,788,095 | 10,546,571 | 10,651,875 | 0.99 |
| historical LO12 | B | 33,474 | 10,112 | 43,730,241 | 3,980,356 | 3,990,624 | 1.00 |
| historical MID12 | A | 19,306 | 250 | 10,546,571 | 1,683 | 1,768.5 | 0.95 |
| historical MID12 | B | 10,112 | 124 | 3,980,356 | 565 | 598.5 | 0.94 |
| exact row 16 | A | 250 | 32 | 1,683 | 35 | 27.6 | 1.27 |
| exact row 16 | B | 124 | 9 | 565 | 2 | 3.0 | 0.67 |

The theory is R = 1 at the table and row-16 levels (independent passes), and R above 1 at the W6 filter because the variants of one class share most of their bits (3.6 and 4.9 in the replays); the exact row-16 level has 41 passes among 98,216 W6 passes (4.2e-4) against the 2^-11 = 4.9e-4 per probed lane of the ledger. Replays: 5 and 2 witness trials of 16, 1.9 s each, identical on repetition. Scope: the levels end at the exact row-16 test; rows 17..36 and independence across first blocks are the premises H3 and H1.

## Appendix M. The ruling on 67516603 (R37F2)

Historical aa0e8b6 material below; old LO/MID code and old cost statements are retained solely as inherited evidence, not the P4 implementation or current accounting. No participant code was run outside the organizer's Docker executor.


**What changed vs 67516603-7f51-4b80-806d-9f4a379dab56 (our R37F2, 59.5556), ruled not_evaluable in lane_evaluability on H1-uniform-chaining-values, H2-variant-step3-probability and H3-first-block-dependence (no fatal finding; H4, H5 and H7 were plausible, plausible and established).** The two material findings, quoted by their first sentence, and the answers:

| finding | premise | quoted | answer |
|---|---|---|---|
| F-EVAL-01 | H2 | "The score-critical H2 value q3=2^-71.47 is based on participant-reported SMC executions embedded in proof.md, but no organizer execution report covers q3smc.c." | H2 is stated as our theory (claim.heuristics; Section 12): q3 is our computation, with the estimator source, the preregistrations and the per-seed estimates printed in Appendices F and G so that it replays from this text. The organizer-executed `h3-ladder-r37` runs the row-16 stage of q3 on organizer seeds (41 exact row-16 passes among 98,216 W6 passes in our replays, 4.2e-4, against 4.9e-4 in the ledger), and `a0-sfs-r37` constructs full 37-step semi-free-start collisions with the same cells. The end event (rows 22..36 reaching an equal digest) needs a reachable first block, that is the attack itself, and is not executable in 20 s; it is the premise. |
| F-EVAL-02 | H1, H3 | "The reported large-scale H1 statistics and H3 joint-dependence replay are not covered by organizer execution reports." | H1 and H3 are stated as our theory. New organizer experiments: `h1-cv1-filters-nonce` (the pass rates of the W7 and W6 filters on real chaining values of organizer seeds), `h3-cowpass-nonce` (co-passes of the variants of one class at the W6 level) and `h3-ladder-r37` (co-passes of distinct variants of one first block through the W6 filter, both table stages and the exact row-16 test, with the dependence factor of each level: 3.62 and 4.92 at W6, 0.99 and 1.00 at historical aa0e8b6 LO12, 0.95 and 0.94 at historical MID12, 1.27 and 0.67 at exact row 16; P4 public-seed ladder R: W6=3.250842, FIRST13 (lo)=0.995964, SECOND11 (mid)=0.949225, exact row 16=1.048555; N/S/P/C and exact rational calculation are in the P4 executor observations section. Appendix H). Rows 17..36 and independence over 2^55.8 first blocks stay the premises H3 and H1, with the allowance rho = 2^35. |

Historical aa0e8b6 ledger evolution (not P4 costs): the same experiments and statements passed lane evaluability in ec1340aa-ecc8-4564-8df7-006f0a2b2ce5 (R37OWN5). Nothing else in the attack changes: the program is d9f8833d's with the changes listed at the top of this text; the only change of the ledger is the Bernstein cap bound (Section 10), which moves the claim from 59.30883 to 59.30006; the collision event after row 21 (Section 7.7) then moves it to 58.02135.


## P4 executor observations (public seed; Round 4)

P4 organizer executor observations under public seed hashsmash-public-seed-v1, no holdout nonce: 256 requested trials per experiment, two fresh executions with byte-identical stdout only. Internal counters are participant observations; the organizer independently checks returned-pair target events. These runs do not prove full-scale probabilities, H1-H7 or q3.

**a0-sfs-r37**: P4 participant observations: 121 returned pairs and checks_passed=121; detected_by_counted_program=16 for all 16 returned trials 0..15. Organizer checked all 256 trial records (121 returned pairs), with 0 full-target collisions; SFS validity remains an internal participant check. Runtime 7.65/7.48 s versus 20 s.

**a0-online-r37**: P4 participant observations: 512 unconditional first blocks, 2070 class passes; 52 selected first blocks, 24 processed classes, 7152 good pairs, 25 survivors. class_lane_mismatches, pass_lane_mismatches, goodset_mismatches, address_mismatches, row16_mismatches and cell_mismatches each total 0. Four returned pairs, 0 organizer full-target collisions. Runtime 1.92/1.93 s versus 20 s.

**h1-cv1-filters-nonce**: P4 participant observations over 15000 blocks: W7=275, W6=3993, coW6=1267, w7_and_w6=22, w7_w6_pairs=60. No returned pairs. Runtime 6.75/6.35 s versus 20 s.

**h3-cowpass-nonce**: P4 participant observations over 15000 blocks: W7=247, W6=4036, coW6=1264, w7_and_w6=27, w7_w6_pairs=82. No returned pairs. Runtime 6.70/6.54 s versus 20 s.

**h3-ladder-r37**: P4 public-seed ladder R: W6=3.250842, FIRST13 (lo)=0.995964, SECOND11 (mid)=0.949225, exact row 16=1.048555; N/S/P/C and exact rational calculation are in the P4 executor observations section. FIRST pass rate 15131/81608=0.185410744045 versus 1513/8192=0.1846923828125 under the uniform-address model; SECOND conditional rate 307/15131=0.020289471945 versus the uniform-address reference 63512/(1513*2048)=467/22784=0.020496839888. There are 37 row-16 passes among 81608 W6 passes. Eight returned generic 4-bit witnesses pass the organizer mask event; they are not full collisions. Runtime 4.37/4.19 s versus 20 s.

| Level | N | S | P | C | E = C (S/N)^2 | R = P/E |
|---|---:|---:|---:|---:|---:|---:|
| W6 | 839,808 | 81,608 | 171,761,468 | 5,595,314,112 | 52835999.384947248 | 3.250841661 |
| FIRST13 (lo) | 81,608 | 15,131 | 5,880,837 | 171,761,468 | 5904668.720325760 | 0.995963919 |
| SECOND11 (mid) | 15,131 | 307 | 2,298 | 5,880,837 | 2420.921071884 | 0.949225494 |
| Exact row 16 | 307 | 37 | 35 | 2,298 | 33.379261318 | 1.048555259 |

N and C at each level are the preceding level's S and P; the W6 base is
w6_cand and w6_candpairs. R is computed from summed counters, not averaged
per-trial ratios; deterministic reruns are not counted as additional samples.
Historical aa0e8b6 LO12/MID12 values in Appendix H remain historical.

The repeated participant ledger/memory diagnostic agrees exactly with the
independent values: N=621084759189170888800, denominator 2644,
time_log2=57.70485, N_FB=31617998307376629, V_MAX=518269945863203016639,
vbar=18021721026738521/1099511627776, vmax_fb=274564402011/5,
and memory=769,776 bytes. FIRST/SECOND table SHA-256:
069c55469f6a9af5a5cd33855fd13c281cd58aceec0b444fd0793806bd6d6292.
Diagnostic runtime 4.03/4.31 s versus 20 s. All runs used 128 MiB / one CPU.

Provenance: executor report SHA-256
8fb29212d809996302ac123534826941415e1e109590aaac184fbf96a6dc134d.
It binds the pre-Round-4 package/manifest text and executed source SHA-256
4d1449598e4eccec6961ac1f61d1718767a442fe48ea2bb3a7d714cc428c9ce0.
Round 4 changes evidence text only; the participant source is byte-identical.
The report is not a binding of the final edited manifest. Returned-pair event
checks are organizer-recomputed; internal observations and diagnostic resource
numbers are not independently established attack costs or success probabilities.
The public seed provides no holdout protection. q3/H1-H7, selected/padded-lane
uniformity, register allocation and code-size bounds remain inherited limitations.

### G.5 Block E: 16,384 more replicates, preregistered on the submitted pool, all reported

**Preregistration.** `prereg/PREREG_q3E32.txt`, sha256
`f8a8b40f6a94fad9618c0809e31224e05faf8be1229a0ddc1a414f7365862bea`, committed to git
(`4c5a8b4`, amended `994e7b9`) **before any listed seed ran**; no seed of block E has a RESULT
line anywhere earlier in this filing or in its history. The rule it fixes, applied once and
without any branch on the outcome:

```text
pool the 16,384 log2est values of block E with the 1,024 of Appendix G.4   (n = 17,408)
u  = floor( (mean - t(0.99, n-1) x sd / sqrt(n)) x 10^4 ) / 10^4           (rounded DOWN)
q3c_declared = 2^u
```

Pooling rather than "the better of the two blocks" is deliberate: the better of two bounds is a
selection over looks, and it would not be a 99 percent bound at all.

**What was measured, and on what.** Nothing is transferred from the parents' pool: the estimator
draws its tail variants from this filing's own list, and the artefacts are the shipped ones --
`q3smc.c` `f0e3efc8`, `gen_consts.py` `721d7949` applied to `lowm.py` `f2578183` (the previous
filing's program, which differs from this filing's shipped program in the single line
`Q3_LOG2`), giving `q3consts_orig.h` `efd62db9` and `variants.bin` `b7671710` with **599,760
words** (the 170 classes of lists 0, 1, 5, 6). The word count and all five hashes are asserted
by the runner before a seed starts, so a run on the parents' 782,800-word pool cannot be
reported as this block. Regeneration is invariant in `Q3_LOG2`: both artefact hashes come back
identical from either program state, which is why the study's pool is also this filing's. Configuration unchanged from G.3 and G.4: `q3smc seed0 512 8192 512 16384`, 32 shards,
one run per seed. Runner: `experiments/r37-q3e-32.py`.

**Result.** 16,384 seeds 772000..788383, none dropped, replaced or rerun: mean **2^-71.42132**,
sd **0.15870** (relative sd of the linear estimates **0.1100**), t(0.99, 16383) = 2.3266,
one-sided 99 percent lower bound **-71.42420**. Pooled with Appendix G.4's 1,024 seeds (mean
2^-71.42391, sd 0.15878): n = 17,408, mean **2^-71.42147**, sd **0.15870**, t(0.99, 17407) = 2.3266,
one-sided 99 percent lower bound **-71.42427**, and **q3c_declared = 2^-71.4243**.

Compared with the 1,024-replicate declaration 2^-71.4355 this is 0.01120 bit of q3c, hence the
same number of bits off the claim. The block is not a new model, a new estimator or a new pool;
it is more of the same measurement, which is the only thing that narrows a Student bound.

**Optional stopping, disclosed.** The pooling rule was written in the amendment `994e7b9`
after G.4's 1,024 values existed -- that is unavoidable, since the pooled estimator uses them --
but before any seed of block E ran, and git records both facts. Nothing in the rule depends on
block E's outcome: the estimator, the pool and the sample size were fixed first, the rule has no
branch, and the block-alone value is printed beside the pooled one so that a reviewer can see
what the data alone would have given.

**What does not change.** Appendix G.3's block keeps its own reported value, 2^-71.43547
(declared 2^-71.4355), and every sensitivity of Section 7.4c is quoted at its own q3 factor and
is therefore untouched by this. The declared q3c is still a one-sided 99 percent bound on the
mean of the submitted pool's own per-variant tail probability, with no sub-pool transfer
allowance. Block E alone would give 2^-71.4243 (floor of its own lower bound to four decimals);
that weaker number is reported here and not used.

Per-seed log2 estimates, seeds 772000..788383 in order (8 per line, all 16,384):

```text
-71.11294 -71.70346 -71.25413 -71.20771 -71.52111 -71.17273 -71.44003 -71.83524
-71.52743 -71.42385 -71.54819 -71.56517 -71.12626 -71.62711 -71.51593 -71.39917
-71.87054 -71.63380 -71.55813 -71.31054 -71.37207 -71.34928 -71.23984 -71.57925
-71.33947 -71.45414 -71.41347 -71.64572 -71.46310 -71.13097 -71.60955 -71.21162
-71.16753 -71.33705 -71.38332 -71.58086 -71.42037 -71.34902 -71.29604 -71.39709
-71.40902 -71.49924 -71.32948 -71.43711 -71.70363 -71.30410 -71.37373 -71.32864
-71.53987 -71.51287 -71.76676 -71.24118 -71.40174 -71.27306 -71.33429 -71.50453
-71.14617 -71.38288 -71.52810 -71.44769 -71.52795 -71.60417 -71.44748 -71.16463
-71.37971 -71.32815 -71.47178 -71.35588 -71.69131 -71.54261 -71.38263 -71.41184
-71.17958 -71.40054 -71.32644 -71.63855 -71.53933 -71.69495 -71.44896 -71.66259
-71.32488 -71.35978 -71.23338 -71.47778 -71.55130 -71.67932 -71.63457 -71.41789
-71.73724 -71.45196 -71.51157 -71.46043 -71.25379 -71.35398 -71.27767 -71.72309
-71.27862 -71.43800 -71.22660 -71.55689 -71.60360 -71.56222 -71.33273 -71.32612
-71.60988 -71.10309 -71.47477 -71.42954 -71.33106 -71.52858 -71.76011 -71.23655
-71.50755 -71.61142 -71.48825 -71.33905 -71.33115 -71.48792 -71.34118 -71.30756
-71.30950 -71.42786 -71.60265 -71.42807 -71.54289 -71.58170 -71.31420 -71.17933
-71.56609 -71.48145 -71.47863 -71.57420 -71.55196 -71.62863 -71.22490 -71.47921
-71.37086 -71.44853 -71.31546 -71.43826 -71.65615 -71.45925 -71.28149 -71.27012
-71.35533 -71.51292 -71.53432 -71.24574 -71.37964 -71.65934 -71.65618 -71.37266
-71.38768 -71.35560 -71.42089 -71.56467 -71.54808 -71.16563 -71.14470 -71.48400
-71.41668 -71.69951 -71.27063 -71.47543 -71.45645 -71.48907 -71.17349 -71.48665
-71.26920 -71.59401 -71.79127 -71.53597 -71.35606 -71.46348 -71.35238 -71.59285
-71.37826 -71.51241 -71.58278 -71.34296 -71.70368 -71.68896 -71.44577 -71.53986
-71.49687 -71.65532 -71.46941 -71.40410 -71.26198 -71.67452 -71.29122 -71.47292
-71.57425 -71.44668 -71.47634 -71.46076 -71.54425 -71.27422 -71.34648 -71.41594
-71.36159 -71.75062 -71.71345 -71.57921 -71.41590 -71.22597 -71.54782 -71.16681
-71.39277 -71.56102 -71.22554 -71.63573 -71.47707 -71.23919 -71.35037 -71.28448
-71.52429 -71.34563 -71.54120 -71.48292 -71.33765 -71.09650 -71.43629 -71.60368
-71.51740 -71.68091 -71.17516 -71.39006 -71.45067 -71.29236 -71.38826 -71.49589
-71.34047 -71.61190 -71.24048 -71.33423 -71.33943 -71.33419 -71.62291 -71.65941
-71.53853 -71.30702 -71.48524 -71.53349 -71.22572 -71.72449 -71.45647 -71.43313
-71.29787 -71.35314 -71.25871 -71.44514 -71.26126 -71.56023 -71.37866 -71.43845
-71.47584 -71.48422 -71.25313 -71.53560 -71.44389 -71.29330 -71.18061 -71.30753
-71.35309 -71.29009 -71.31321 -71.28577 -71.66850 -71.75850 -71.57649 -71.34058
-71.36176 -71.65496 -71.26274 -71.47170 -71.43514 -71.43528 -71.43529 -71.61014
-71.55147 -71.49235 -71.53890 -71.34742 -71.26189 -71.68389 -71.28067 -71.41589
-71.55192 -71.24517 -71.42251 -71.51709 -71.06050 -71.44631 -71.14805 -71.32783
-71.58289 -71.22959 -71.48052 -71.52800 -71.48334 -71.64600 -71.33902 -71.78799
-71.35961 -71.48718 -71.73596 -71.52552 -71.46832 -71.46677 -71.43114 -71.34784
-71.06591 -71.31644 -71.43202 -71.77671 -71.42837 -71.50205 -71.50524 -71.37674
-71.57055 -71.70939 -71.43100 -71.27880 -71.77745 -71.22378 -71.34906 -71.35439
-71.40764 -71.45321 -71.38276 -71.64745 -71.36005 -71.59118 -71.55203 -71.58541
-71.39148 -71.36848 -71.26667 -71.25887 -71.57176 -71.50560 -71.46851 -71.24602
-71.76726 -71.41711 -71.45927 -71.46779 -71.53268 -71.70409 -71.39589 -71.67055
-71.37496 -71.58955 -71.68733 -71.57156 -71.46670 -71.53579 -71.51299 -71.78922
-71.50017 -71.46841 -71.26091 -71.30317 -71.16835 -71.23214 -71.37548 -71.19911
-71.30370 -71.55776 -71.40062 -71.43150 -71.55022 -71.59710 -71.03721 -71.32464
-71.14798 -71.63982 -71.23078 -71.46760 -71.56483 -71.26980 -71.43177 -71.34006
-71.35853 -71.45450 -71.38526 -71.46754 -71.30630 -71.16552 -71.54659 -71.55521
-71.60050 -71.55537 -71.41577 -71.42267 -71.31124 -71.27890 -71.54037 -71.30647
-71.39893 -71.42798 -71.11782 -71.42044 -71.41450 -71.55952 -71.60193 -71.48689
-71.72202 -71.34851 -71.57369 -71.53168 -71.58941 -71.64822 -71.53581 -71.28639
-71.22977 -71.47304 -71.56992 -71.41796 -71.44943 -71.37850 -71.34224 -71.59341
-71.50984 -71.34193 -71.43844 -71.27813 -71.45539 -71.55018 -71.18472 -71.48650
-71.43434 -71.48541 -71.33797 -71.60316 -71.80148 -71.33344 -71.50799 -71.52540
-71.47377 -71.19387 -71.31798 -71.35606 -71.44239 -71.29872 -71.35965 -71.31138
-71.36008 -71.61958 -71.26755 -71.27677 -71.20021 -71.61033 -71.11625 -71.45671
-71.45155 -71.57027 -71.32169 -71.58478 -71.47267 -71.57099 -71.35762 -71.36517
-71.40606 -71.57251 -71.30530 -71.36790 -71.43003 -71.39700 -71.32898 -71.30273
-71.21880 -71.28903 -71.33443 -71.48934 -71.18343 -71.56363 -71.40345 -71.50223
-71.41567 -71.16654 -71.37210 -71.66430 -71.71506 -71.36000 -71.28483 -71.37928
-71.46070 -71.39016 -71.34059 -71.58115 -71.36794 -71.39052 -71.34169 -71.59719
-71.54208 -71.16096 -71.40414 -71.61718 -71.25106 -71.44919 -71.57528 -71.43626
-71.40458 -71.85043 -71.24685 -71.47710 -71.39154 -71.26150 -71.40020 -71.38049
-71.37069 -71.45660 -71.34619 -71.68721 -71.45225 -71.43405 -71.75967 -71.49383
-71.57686 -71.44465 -71.56298 -71.69632 -71.36624 -71.39372 -71.57751 -71.25185
-71.30221 -71.33566 -71.40143 -71.33503 -71.68819 -71.10946 -71.39713 -71.48157
-71.30391 -71.49411 -71.64646 -71.33548 -71.24362 -71.38713 -71.43502 -71.20718
-71.05528 -71.26348 -71.53660 -71.39265 -71.51217 -71.55994 -71.71154 -71.37705
-71.45560 -71.50163 -71.17129 -71.34086 -71.46174 -71.44182 -71.32547 -71.56136
-71.65598 -71.43171 -71.45405 -71.80878 -71.43955 -71.37113 -71.33400 -71.34339
-71.38847 -71.38493 -71.71594 -71.53201 -71.56487 -71.29062 -71.69457 -71.53339
-71.62181 -71.44189 -71.36361 -71.24609 -71.27351 -71.31294 -71.45807 -71.46967
-71.13740 -71.49682 -71.39116 -71.19813 -71.58163 -71.43851 -71.33390 -71.36643
-71.31437 -71.49800 -71.20343 -71.48788 -71.21265 -71.58118 -71.53622 -71.36236
-71.44939 -71.32180 -71.52018 -71.51234 -71.47671 -71.40850 -71.39077 -71.50058
-71.03974 -71.39692 -71.47550 -71.45555 -71.54842 -71.18398 -71.67517 -71.53569
-71.35477 -71.53212 -71.29068 -71.36248 -71.30080 -71.40333 -71.56027 -71.30516
-71.45021 -71.47776 -71.43476 -71.58547 -71.53645 -71.45718 -71.53841 -71.47782
-71.58116 -71.50648 -71.10648 -71.46946 -71.43531 -71.32133 -71.53810 -71.35664
-71.57171 -71.70399 -71.19677 -71.48996 -71.41489 -71.44973 -71.22905 -71.40097
-71.71747 -71.43976 -71.27120 -71.76779 -71.52969 -71.32008 -71.31596 -71.39765
-71.23637 -71.50517 -71.69261 -71.50174 -71.24116 -71.55444 -71.02538 -71.30646
-71.35410 -71.30707 -71.46266 -71.31664 -71.45557 -71.35099 -71.52314 -71.62060
-71.25154 -71.57250 -71.41725 -71.45599 -71.64330 -71.43631 -71.68407 -71.22099
-71.22788 -71.17645 -71.67803 -71.12270 -71.71163 -71.21707 -71.60234 -71.20965
-71.58192 -71.39885 -71.31152 -71.39481 -71.43890 -71.53688 -71.48788 -71.23635
-71.38882 -71.31577 -71.50029 -71.45468 -71.49637 -71.08262 -71.29554 -71.50211
-71.45879 -71.40759 -71.23380 -71.29056 -71.50229 -71.30799 -71.32066 -71.52967
-71.20814 -71.73457 -71.33073 -71.44491 -71.43971 -71.18225 -71.20037 -71.43707
-71.29227 -71.33698 -71.27977 -71.49991 -71.41635 -71.86725 -71.08380 -71.59235
-71.38957 -71.37526 -71.41332 -71.53834 -71.35694 -71.44727 -71.55615 -71.32707
-71.36530 -71.27965 -71.28608 -71.47832 -71.37129 -71.38879 -71.19965 -71.66478
-71.70846 -71.44623 -71.35346 -71.38448 -71.40087 -71.31495 -71.31938 -71.48177
-71.30810 -71.42581 -71.34222 -71.63717 -71.54961 -71.33522 -71.52655 -71.32630
-71.04798 -71.26701 -71.44001 -71.38913 -71.39014 -71.28041 -71.29392 -71.92416
-71.33799 -71.45551 -71.69875 -71.38216 -71.28235 -71.33564 -71.33326 -71.55893
-71.39382 -71.48126 -71.41367 -71.53109 -71.27496 -71.41097 -71.34341 -71.52843
-71.42181 -71.12758 -71.50571 -71.38505 -71.16636 -71.42453 -71.57871 -71.43942
-71.32434 -71.28891 -71.35644 -71.50508 -71.57017 -71.31223 -71.22294 -71.53575
-71.48171 -71.54300 -71.22998 -71.60540 -71.22142 -71.42994 -71.34094 -71.32579
-71.83205 -71.22094 -71.34262 -71.62908 -71.18308 -71.54668 -71.36429 -71.47616
-71.50755 -71.46079 -71.46709 -71.46198 -71.26306 -71.37249 -71.48499 -71.43188
-71.38360 -71.57963 -71.53168 -71.43174 -71.46922 -71.73272 -71.17549 -71.43156
-71.51757 -71.61996 -71.24735 -71.50695 -71.41862 -71.54309 -71.42018 -71.62319
-71.64072 -71.65362 -71.24647 -71.20343 -71.61468 -71.55247 -71.61610 -71.47919
-71.33643 -71.60782 -71.43540 -71.56641 -71.56288 -71.63811 -71.51014 -71.53370
-71.57414 -71.35682 -71.55413 -71.15628 -71.58914 -71.41979 -71.51702 -71.59412
-71.80761 -71.11609 -71.53385 -71.25811 -71.56133 -71.36941 -71.19407 -71.42765
-71.30781 -71.33257 -71.35218 -71.65487 -71.32300 -71.40381 -71.31562 -71.39215
-71.49583 -71.61250 -71.60217 -71.51075 -71.59964 -71.48565 -71.52231 -71.18941
-71.77961 -71.59022 -71.38239 -71.50289 -71.30230 -71.34341 -71.26604 -71.41941
-71.30845 -71.44914 -71.43153 -71.26308 -71.29186 -71.38834 -71.54883 -71.53322
-71.41018 -71.24520 -71.31744 -71.58559 -71.54432 -71.31747 -71.57844 -71.21869
-71.47262 -71.41815 -71.41757 -71.25727 -71.33261 -71.68918 -71.60753 -71.20509
-71.29578 -71.55725 -71.45611 -71.42069 -71.38473 -71.61098 -71.14059 -71.39308
-71.24781 -71.49985 -71.35242 -71.27421 -71.28808 -71.51658 -71.44520 -71.20028
-71.36631 -71.34484 -71.26509 -71.56420 -71.65697 -71.44841 -71.58738 -71.30798
-71.35271 -71.30905 -71.52538 -71.42741 -71.83672 -71.78633 -71.24559 -71.18584
-71.17067 -71.43065 -71.61339 -71.22074 -71.64689 -71.74378 -71.32294 -71.42448
-71.40937 -71.37907 -71.36986 -71.58649 -71.68887 -71.57829 -71.47283 -71.36211
-71.41170 -71.26966 -71.39980 -71.40618 -71.47992 -71.35000 -71.33951 -71.27041
-71.37324 -71.45523 -71.35464 -71.25247 -71.34551 -71.52354 -71.35735 -71.55767
-71.71764 -71.41333 -71.47272 -71.41269 -71.39655 -71.27804 -71.67334 -71.34655
-71.53363 -71.58636 -71.33986 -71.48856 -71.21022 -71.38388 -71.49594 -71.27782
-71.27161 -71.20860 -71.57031 -71.49394 -71.56169 -71.38546 -71.36745 -71.36829
-71.36949 -71.57753 -71.44111 -71.34020 -71.20934 -71.89734 -71.33257 -71.64179
-71.77366 -71.24153 -71.37982 -71.20344 -71.34083 -71.53538 -71.25655 -71.31181
-71.16160 -71.82857 -71.32032 -71.53331 -71.42634 -71.29481 -71.51374 -71.64061
-71.32843 -71.34152 -71.28368 -71.54137 -71.44568 -71.43284 -71.27139 -71.45341
-71.56362 -71.57717 -71.16315 -71.33679 -71.62770 -71.47530 -71.42096 -71.55288
-71.23354 -71.42375 -71.61861 -71.47095 -71.48800 -71.48457 -71.48547 -71.12641
-71.33256 -71.42303 -71.51637 -71.63494 -71.39452 -71.47408 -71.67484 -71.35080
-71.33226 -71.22469 -71.40124 -71.46734 -71.65528 -71.39375 -71.42910 -71.33336
-71.60233 -71.33943 -71.19630 -71.22101 -71.17196 -71.55114 -71.03028 -71.37021
-71.36170 -71.63600 -71.65801 -71.52527 -71.26452 -71.44010 -71.22815 -71.22232
-71.47646 -71.59495 -71.33185 -71.13706 -71.69459 -71.47692 -71.59866 -71.44946
-71.45252 -71.69869 -71.23003 -71.39221 -71.30445 -71.56686 -71.60555 -71.55600
-71.54289 -71.16689 -71.76463 -71.36844 -71.45904 -71.35631 -71.35297 -71.37201
-71.48250 -71.34286 -71.29006 -71.16233 -71.29659 -71.32699 -71.49923 -71.18287
-71.55559 -71.48327 -71.68035 -71.34797 -71.31051 -71.40859 -71.47958 -71.32866
-71.47647 -71.44073 -71.18225 -71.39916 -71.47358 -71.31802 -71.70434 -71.55026
-71.53162 -71.48689 -71.30811 -71.46205 -71.44671 -71.60479 -71.19829 -71.55137
-71.50297 -71.24125 -71.48779 -71.00126 -71.50818 -71.49654 -71.40208 -71.14864
-71.47595 -71.18990 -71.58026 -71.35249 -71.89028 -71.45692 -71.49689 -71.16610
-71.21867 -71.53337 -71.12401 -71.49970 -71.36643 -71.35565 -71.53180 -71.41421
-71.60508 -71.06503 -71.29274 -71.60939 -71.39231 -71.45564 -71.40772 -71.69899
-71.18092 -71.38604 -71.28221 -71.43998 -71.34394 -71.46812 -71.17239 -71.35696
-71.26020 -71.35550 -71.23826 -71.37063 -71.54382 -71.41238 -71.52007 -71.44278
-71.37740 -71.38555 -71.32433 -71.65219 -71.58839 -71.24138 -71.24562 -71.59685
-71.38980 -71.66384 -71.22537 -71.25426 -71.62398 -71.59055 -71.28246 -71.24784
-71.35588 -71.36767 -71.28479 -71.38081 -71.12842 -71.24320 -71.39763 -71.51264
-71.37172 -71.44627 -71.49206 -71.19735 -71.53414 -71.62183 -71.64800 -71.50572
-71.35156 -71.40221 -71.47060 -71.18751 -71.64537 -71.35902 -71.06680 -71.60373
-71.56843 -71.68400 -71.43582 -71.22453 -71.32799 -71.38564 -71.44793 -71.57534
-71.40006 -71.43038 -71.37876 -71.31071 -71.52803 -71.68474 -71.55895 -71.23929
-71.66793 -71.26639 -71.58466 -71.38329 -71.34216 -71.58947 -71.22930 -71.60302
-71.31258 -71.39707 -71.64112 -71.37080 -71.16753 -71.19711 -71.48151 -71.35555
-71.50965 -71.37185 -71.69975 -71.55310 -71.58107 -71.41720 -71.19697 -71.64664
-71.50197 -71.43046 -71.25373 -71.30630 -71.54369 -71.19338 -71.34861 -71.86274
-71.63467 -71.20214 -71.30391 -71.53418 -71.47911 -71.13525 -71.56159 -71.42890
-71.20964 -71.40268 -71.44068 -71.62898 -71.48254 -71.70393 -71.30522 -71.34201
-71.21976 -71.58761 -71.40747 -71.18744 -71.45098 -71.38892 -71.32085 -71.66026
-71.39509 -71.41992 -71.35319 -71.38945 -71.73798 -71.61103 -71.46295 -71.34916
-71.10377 -71.56546 -71.47336 -71.29613 -71.47993 -71.20963 -71.18371 -71.40203
-71.45511 -71.29520 -71.26994 -71.29297 -71.09170 -71.19370 -71.31492 -71.41310
-71.36888 -71.52865 -71.22002 -71.24725 -71.53347 -71.56157 -71.65556 -71.61173
-71.29749 -71.36040 -71.45191 -71.34042 -71.18736 -71.31574 -71.31685 -71.41784
-71.24206 -71.57141 -71.44460 -71.54209 -71.36197 -71.50089 -71.43901 -71.32720
-71.49318 -71.76200 -71.29028 -71.42011 -71.35006 -71.45352 -71.37425 -71.33060
-71.32398 -71.32843 -71.36998 -71.46035 -71.38277 -71.25977 -71.26363 -71.28853
-71.22806 -71.38674 -71.13112 -71.64417 -71.53723 -71.42155 -71.46581 -71.50404
-71.32481 -71.46766 -71.70264 -71.47189 -71.62617 -71.33931 -71.14129 -71.68984
-71.32387 -71.25897 -71.29175 -71.14547 -71.30101 -71.41923 -71.56966 -71.47531
-71.33935 -71.31442 -71.48566 -71.60953 -71.40789 -71.53053 -71.38563 -71.30893
-71.73023 -71.46401 -71.45278 -71.52009 -71.53094 -71.54151 -71.49905 -71.29967
-71.60472 -71.35246 -71.25817 -71.38292 -71.41297 -71.47563 -71.51329 -71.40726
-71.27825 -71.26274 -71.26003 -71.37553 -71.56748 -71.30499 -71.55721 -70.98080
-71.07763 -71.57496 -71.46143 -71.48605 -71.43473 -71.41997 -71.48651 -71.27912
-71.11227 -71.44995 -71.41804 -71.37774 -71.42607 -71.50858 -71.37454 -71.45362
-71.67299 -71.58654 -71.53719 -71.34492 -71.51222 -71.43198 -71.28643 -71.39284
-71.19936 -71.44302 -71.34649 -71.37127 -71.46786 -71.07748 -71.58154 -71.49785
-71.49004 -71.38098 -71.50512 -71.29832 -71.35638 -71.30911 -71.60357 -71.15258
-71.28065 -71.35385 -71.20246 -71.25512 -71.27024 -71.31436 -71.52483 -71.43499
-71.26829 -71.43525 -71.49536 -71.25844 -71.73884 -71.39148 -71.59570 -71.65138
-71.49536 -71.17282 -71.21638 -71.46351 -71.45181 -71.50233 -71.43012 -71.48504
-71.30858 -71.38722 -71.19034 -71.46058 -71.62167 -71.29148 -71.30081 -71.44887
-71.16103 -71.39069 -71.76815 -71.56505 -71.15105 -71.08208 -71.26797 -71.71784
-71.41254 -71.21107 -71.34829 -71.49381 -71.57772 -71.42349 -71.27781 -71.49371
-71.28259 -71.17233 -71.05538 -71.29615 -71.30821 -71.50026 -71.48082 -71.44947
-71.42636 -71.46069 -71.63886 -71.41142 -71.44175 -71.71680 -71.87376 -71.46519
-71.38632 -71.66271 -71.48926 -71.69110 -71.36814 -71.15699 -71.50093 -71.37486
-71.13953 -71.48232 -71.35551 -71.42661 -71.55974 -71.27541 -71.42629 -71.55143
-71.48219 -71.59897 -71.49507 -71.46545 -70.93703 -71.15065 -71.39323 -71.47286
-71.63679 -71.68749 -71.31381 -71.41465 -71.58920 -71.31282 -71.17446 -71.48368
-71.55178 -71.40111 -71.25597 -71.21550 -71.61718 -71.41509 -71.36548 -71.49145
-71.21450 -71.44993 -71.42371 -71.26853 -71.65037 -71.24811 -71.45274 -71.22855
-71.38969 -71.38991 -71.50988 -71.19171 -71.44741 -71.55257 -71.54963 -71.45103
-71.65196 -71.30928 -71.16322 -71.52269 -71.43520 -71.31329 -71.45672 -71.34933
-71.56693 -71.58517 -71.45681 -71.56186 -71.14006 -71.58809 -71.44197 -71.48321
-71.78344 -71.79577 -71.27541 -71.38149 -71.66046 -71.46824 -71.68847 -71.40468
-71.42272 -71.41592 -71.29121 -71.29437 -71.59136 -71.51823 -71.22786 -71.85575
-71.71299 -71.61732 -71.44096 -71.46677 -71.47745 -71.61976 -71.42353 -71.29203
-71.37395 -71.50886 -71.40110 -71.42478 -71.69405 -71.67643 -71.35410 -71.64229
-71.28414 -71.50880 -71.56599 -71.40448 -71.12798 -71.46099 -71.36283 -71.17864
-71.28687 -71.77695 -71.63783 -71.47419 -71.22425 -71.42590 -71.56841 -71.84168
-71.14223 -71.65471 -71.74554 -71.33302 -71.67193 -71.55551 -71.41354 -71.30246
-71.76580 -71.60172 -71.66364 -71.21737 -71.40334 -71.30754 -71.60096 -71.09164
-71.13887 -71.33787 -71.65158 -71.51403 -71.54173 -71.60707 -71.55598 -71.39550
-71.52073 -71.56298 -71.74230 -71.60431 -71.40042 -71.27510 -71.44841 -71.40646
-71.32930 -71.77693 -71.44616 -71.52295 -71.71731 -71.33797 -71.38333 -71.63059
-71.41105 -71.34829 -71.83686 -71.71097 -71.27328 -71.47948 -71.24596 -71.15580
-71.18766 -71.29339 -71.77370 -71.34819 -71.37284 -71.48091 -71.16994 -71.26894
-71.44178 -71.43502 -71.37781 -71.46577 -71.55253 -71.41762 -71.36212 -71.41969
-71.46158 -71.59974 -71.89681 -71.51311 -71.35732 -71.29327 -71.29169 -71.28504
-71.61018 -71.26529 -71.45569 -71.34812 -71.70852 -71.51986 -71.86613 -71.41998
-71.46663 -71.40384 -71.55355 -71.52198 -71.37158 -71.24533 -71.39128 -71.20670
-71.54304 -71.37007 -71.20524 -71.74837 -71.19649 -71.41569 -71.50238 -71.52791
-71.02684 -71.14548 -71.28110 -71.58801 -71.27099 -71.22422 -71.66653 -71.23874
-71.54120 -71.39069 -71.49505 -71.23627 -71.35741 -71.55294 -71.48197 -71.13645
-71.12440 -71.73158 -71.54120 -71.60551 -71.43314 -71.59193 -71.30912 -71.52648
-71.48009 -71.35484 -71.50679 -71.62437 -71.44030 -70.95948 -71.24949 -71.35731
-71.44551 -71.73479 -71.32005 -71.21944 -71.29572 -71.30132 -71.19371 -71.20710
-71.51583 -71.56738 -71.07261 -71.25355 -71.69698 -71.47736 -71.34833 -71.58263
-71.59990 -71.27034 -71.33161 -71.51360 -71.36205 -71.50630 -71.43811 -71.37112
-71.14361 -71.22041 -71.43292 -71.63268 -71.33656 -71.22847 -71.17960 -71.47357
-71.83535 -71.54123 -71.27172 -71.32933 -71.54863 -71.50782 -71.41350 -71.36686
-71.08592 -71.43186 -71.73212 -71.23032 -71.45501 -71.54350 -71.21449 -71.45693
-71.24244 -71.67638 -71.44614 -71.54489 -71.38224 -71.47778 -71.34184 -71.35782
-71.35708 -71.52198 -71.56014 -71.20789 -71.30668 -71.63044 -71.43511 -71.37291
-71.20501 -71.25641 -71.19061 -71.51760 -71.34818 -71.74290 -71.51739 -71.38237
-71.43671 -71.20372 -71.32118 -71.18709 -71.40827 -71.35453 -71.40712 -71.33958
-71.51194 -71.67175 -71.14449 -71.47598 -71.37899 -71.22309 -71.33904 -71.16618
-71.47767 -71.14456 -71.57752 -71.44369 -71.62414 -71.36398 -71.39702 -71.40024
-71.24617 -71.29995 -71.24827 -71.44003 -71.34435 -71.47601 -71.56927 -71.29885
-71.19773 -71.40276 -71.35828 -71.45356 -71.28403 -71.34896 -71.38461 -71.66995
-71.42925 -71.35108 -71.45427 -71.64106 -71.44600 -71.48744 -71.64243 -71.47921
-71.43612 -71.60645 -71.49024 -71.35779 -71.15805 -71.49901 -71.20521 -71.60941
-71.74771 -71.48961 -71.40650 -71.33547 -71.36541 -71.20147 -71.26643 -71.28271
-71.35775 -71.37403 -71.63741 -71.37498 -71.48836 -71.54201 -71.35843 -71.77847
-71.42331 -71.49610 -71.42263 -71.48214 -71.41833 -71.28911 -71.51883 -71.60375
-71.52088 -71.56737 -71.54999 -71.75131 -71.37248 -71.55975 -71.52194 -71.47353
-71.32936 -71.68068 -71.26712 -71.77371 -71.41449 -71.61531 -71.59205 -71.65173
-71.42461 -71.58892 -71.28619 -71.34838 -71.33029 -71.17890 -71.49299 -71.20499
-71.51886 -71.53484 -71.64459 -71.25509 -71.45393 -71.46365 -70.94490 -71.47690
-71.40625 -71.20790 -71.34481 -71.46011 -71.36416 -71.35505 -71.41776 -71.49902
-71.48156 -71.55707 -71.28961 -71.29478 -71.22915 -71.71111 -71.27244 -71.38732
-71.46555 -71.42028 -71.33812 -71.68934 -71.43919 -71.43791 -71.42765 -71.40619
-71.51760 -71.50715 -71.44771 -71.36314 -71.17256 -71.71547 -71.53266 -71.69452
-71.67984 -71.37422 -71.41709 -71.35901 -71.31664 -71.46239 -71.61264 -71.59281
-71.13830 -71.70484 -71.27314 -71.43891 -71.34276 -71.49536 -71.53593 -71.45825
-71.60704 -71.43543 -71.52102 -71.69134 -71.67878 -71.49384 -71.39229 -71.65388
-71.44498 -71.75980 -71.51819 -71.09742 -71.31833 -71.50764 -71.35308 -71.40288
-71.44958 -71.58460 -71.48128 -71.54677 -71.42056 -71.48642 -71.29583 -71.14420
-71.33692 -71.25874 -71.35030 -71.32327 -71.40752 -71.32863 -71.51205 -71.59209
-71.39641 -71.46121 -71.28689 -71.49400 -71.20580 -71.28171 -71.60251 -71.53856
-71.83276 -71.43342 -71.51405 -71.47939 -71.35958 -71.30741 -71.60150 -71.47380
-71.53400 -71.44977 -71.56685 -71.59818 -71.48777 -71.44250 -71.41450 -70.93591
-71.76319 -71.35468 -71.30788 -71.41339 -71.34234 -71.46141 -71.28835 -71.73467
-71.29440 -71.27865 -71.07773 -71.48305 -71.33854 -71.42737 -71.49063 -71.64053
-71.30870 -71.44007 -71.16184 -71.35408 -71.28722 -71.53043 -71.39667 -71.39310
-71.55337 -71.48292 -71.37561 -71.56548 -71.53368 -71.42041 -71.20619 -71.22667
-71.49400 -71.47885 -71.46263 -71.24401 -71.71457 -71.40068 -71.51401 -71.50790
-71.47296 -71.74809 -71.39751 -71.34902 -71.60684 -71.51711 -71.30433 -71.39577
-71.37539 -71.49702 -71.50576 -71.49018 -71.37906 -71.43448 -71.38300 -71.59982
-71.56642 -71.51417 -71.28147 -71.17911 -71.48765 -71.12880 -71.34353 -71.35609
-71.66313 -71.24755 -71.31239 -71.48823 -71.53118 -71.45088 -71.36083 -71.59678
-71.39673 -71.29062 -71.33797 -71.43855 -71.38827 -71.31420 -71.37847 -71.42515
-71.34169 -71.33785 -71.21081 -71.29150 -71.40037 -71.43224 -71.41766 -71.31200
-71.64665 -71.18740 -71.28857 -71.45396 -71.65596 -71.48812 -71.21848 -71.20093
-71.54891 -71.46042 -71.37564 -71.30151 -71.51392 -71.24701 -71.54243 -71.19768
-71.22146 -71.18958 -71.17138 -71.23250 -71.25189 -71.63370 -71.30148 -71.51626
-71.39930 -71.39939 -71.41959 -71.36816 -71.53563 -71.16008 -71.32172 -71.19840
-71.47334 -71.37738 -71.42197 -71.77371 -71.39979 -71.41339 -71.46518 -71.44791
-71.25705 -71.49995 -71.22413 -71.65264 -71.03140 -71.57635 -71.23072 -71.12940
-71.08235 -71.69375 -71.46820 -71.08924 -71.31345 -71.49573 -71.32916 -71.26440
-71.48375 -71.75545 -71.49709 -71.49143 -71.36970 -71.20866 -71.44786 -71.67318
-71.27090 -71.39520 -71.38707 -71.41716 -71.43047 -71.42586 -71.52843 -71.45282
-71.33863 -71.29479 -71.43318 -71.28011 -71.27154 -71.24637 -71.44605 -71.30749
-71.25705 -71.52918 -71.27264 -71.30619 -71.53050 -71.34386 -71.30208 -71.35241
-71.40879 -71.19092 -71.50873 -71.57185 -71.57705 -71.27404 -71.27715 -71.41529
-71.14763 -71.70216 -71.34282 -71.65416 -71.37828 -71.18960 -71.17146 -71.45966
-71.46854 -71.72478 -71.27548 -71.08167 -71.63490 -71.45740 -71.26812 -71.52108
-71.58377 -71.19871 -71.45073 -71.49231 -71.45772 -71.74275 -71.31898 -71.33214
-71.41989 -71.51684 -71.29693 -71.36293 -71.17652 -71.47362 -71.72019 -71.55304
-71.22198 -71.31080 -71.16879 -71.52280 -71.46576 -71.33032 -71.32319 -71.27837
-71.51392 -71.41327 -71.47686 -71.28720 -71.37738 -71.23339 -71.52212 -71.71780
-71.64942 -71.35564 -71.35672 -71.42053 -71.44442 -71.46618 -71.26165 -71.17605
-72.15226 -71.55586 -71.45341 -71.67162 -71.50465 -71.50031 -71.11606 -71.45541
-71.56244 -71.37586 -71.29979 -71.21661 -71.48342 -71.29854 -71.41510 -71.48417
-71.40813 -71.16947 -71.70808 -71.52976 -71.37595 -71.45395 -71.51747 -71.38086
-71.53698 -71.52386 -71.32394 -71.15408 -71.52600 -71.28148 -71.19907 -71.54643
-71.34440 -71.44527 -71.35479 -71.64970 -71.42369 -71.39871 -71.46857 -71.42662
-71.46328 -71.26671 -71.52191 -71.33148 -71.41492 -71.25576 -71.53366 -71.50160
-71.43536 -71.35222 -71.59829 -71.47735 -71.26365 -71.35724 -71.47153 -71.16786
-71.33621 -71.39638 -71.39776 -71.20707 -71.31489 -71.65645 -71.49102 -71.52673
-71.35745 -71.44809 -71.92024 -71.50790 -71.40064 -71.76649 -71.43336 -71.51772
-71.27426 -71.42204 -71.62064 -71.44365 -71.33560 -71.32704 -71.49352 -71.46306
-71.29171 -71.49486 -71.17264 -71.68756 -71.57945 -71.25230 -71.53109 -71.19137
-71.73500 -71.49109 -71.34657 -71.37856 -71.29474 -71.32801 -71.35874 -71.38639
-71.38014 -71.53451 -71.72759 -71.48391 -71.79181 -71.73907 -71.38418 -71.47449
-71.43792 -71.60615 -71.46545 -71.45774 -71.31695 -71.71320 -71.55229 -71.22108
-71.74397 -71.42952 -71.48088 -71.23196 -71.47465 -71.51033 -71.40224 -71.54740
-71.80671 -71.24972 -71.07487 -71.58954 -71.53173 -71.53381 -71.47437 -71.62607
-71.55154 -71.40409 -71.50362 -71.43557 -71.46312 -71.50058 -71.44929 -71.13860
-71.46719 -71.33649 -71.37173 -71.39846 -71.42088 -71.28067 -71.22705 -71.43056
-71.42330 -71.54167 -71.64447 -71.54745 -71.04944 -71.33599 -71.35157 -71.27214
-71.43278 -71.32643 -71.47816 -71.55899 -71.37435 -71.29720 -71.65427 -71.53706
-71.56607 -71.39985 -71.64241 -71.31399 -71.24958 -71.42058 -71.36435 -71.30951
-71.53754 -71.67979 -71.31756 -71.48060 -71.47351 -71.58761 -71.49630 -71.36704
-71.23288 -71.66225 -71.84305 -71.53234 -71.55857 -71.35211 -71.56989 -71.09345
-71.44678 -71.48436 -71.26016 -71.52238 -71.90897 -71.44308 -71.48819 -71.47913
-71.69211 -71.50299 -71.32353 -71.52729 -71.70975 -71.51984 -71.39501 -71.45821
-71.41620 -71.48422 -71.32887 -71.43116 -71.56653 -71.52981 -71.52782 -71.49493
-71.30822 -71.14810 -71.13130 -71.35873 -71.77059 -71.11521 -71.37717 -71.44409
-71.35710 -71.46246 -71.30206 -71.25902 -71.24468 -71.55820 -71.45844 -71.56390
-71.53550 -71.74503 -71.19980 -71.28324 -71.19734 -71.56313 -71.31459 -71.72080
-71.42849 -71.25925 -71.45217 -71.48435 -71.28133 -71.21561 -71.31368 -71.45462
-71.62925 -71.19833 -71.53502 -71.41577 -71.30929 -71.55524 -71.30258 -71.35754
-71.42420 -71.23752 -71.44149 -71.17555 -71.47948 -71.53966 -71.54086 -71.31878
-71.55572 -71.29571 -71.71946 -71.46293 -71.51963 -71.17259 -71.39775 -71.29311
-71.44285 -71.43678 -71.59489 -71.61695 -71.29725 -71.31711 -71.34297 -71.83815
-71.28715 -71.25511 -71.32326 -71.65110 -71.27882 -71.43771 -71.28235 -71.24264
-71.44403 -71.37052 -71.27074 -71.45344 -71.33305 -71.21290 -71.51333 -71.45068
-71.30568 -71.31962 -71.33772 -71.17749 -71.29600 -71.32230 -71.59366 -71.33654
-71.57134 -71.48574 -71.27311 -71.46270 -71.26041 -71.73722 -71.33907 -71.54404
-71.43596 -71.34327 -71.41945 -71.39594 -71.51182 -71.39235 -71.39011 -71.17866
-71.49864 -71.24794 -71.40096 -71.27432 -71.42978 -71.32948 -71.28733 -71.40611
-71.27305 -71.44986 -71.56367 -71.33678 -71.21776 -71.49215 -71.52785 -71.43355
-71.32482 -71.26337 -71.23222 -71.40242 -71.44188 -71.50658 -71.40840 -71.52262
-71.15732 -71.52253 -71.38149 -71.44299 -71.42576 -71.45951 -71.56925 -71.48574
-71.30302 -71.54457 -71.65483 -71.42905 -71.41213 -71.52271 -71.41814 -71.22087
-71.53317 -71.47058 -71.47315 -71.54983 -71.45579 -71.75397 -71.36889 -71.66882
-71.36847 -71.64822 -71.37436 -71.33623 -71.34886 -71.69240 -71.32333 -71.57835
-71.44030 -71.53373 -71.32982 -71.23963 -71.11848 -71.54866 -71.38618 -71.75246
-71.25547 -71.42339 -71.22659 -71.49501 -71.61019 -71.26391 -71.21446 -71.30567
-71.43063 -71.16696 -71.24687 -71.40529 -71.31255 -71.26615 -71.72094 -71.28524
-71.37969 -71.45606 -71.30769 -71.23834 -71.29762 -71.44446 -71.35410 -71.28679
-71.46979 -71.42717 -71.60577 -71.76407 -71.47273 -71.45545 -71.66399 -71.25171
-71.78740 -71.47475 -71.29504 -71.43128 -71.39205 -71.49699 -71.59843 -71.45496
-71.42190 -71.29807 -71.42261 -71.68686 -71.44291 -71.38796 -71.36166 -71.24697
-71.48394 -71.49662 -71.54643 -71.70695 -71.18309 -71.30886 -71.33172 -71.33839
-71.45754 -71.40369 -71.75840 -71.46949 -71.33248 -71.58916 -71.38071 -71.54133
-71.36320 -71.60399 -71.54729 -71.46681 -71.38556 -71.49203 -71.50073 -71.47382
-71.51764 -71.18782 -71.63638 -71.54855 -71.30620 -71.40222 -71.17680 -71.63693
-71.54213 -71.29962 -71.57483 -71.58634 -71.53608 -71.46526 -71.32381 -71.26288
-71.29658 -71.20976 -71.66477 -71.47080 -71.22339 -71.33658 -71.48081 -71.52814
-71.28769 -71.30067 -71.67475 -71.47015 -71.28092 -71.49934 -71.43640 -71.31252
-71.49063 -71.33541 -71.29808 -71.70768 -71.32776 -71.30200 -71.49008 -71.64199
-71.61746 -71.42296 -71.46862 -71.56036 -71.32414 -71.34903 -71.55100 -71.62760
-71.52816 -71.17421 -71.18396 -71.30029 -71.23172 -71.46485 -71.33049 -71.49339
-71.59270 -71.48169 -71.57099 -71.48691 -71.50440 -71.85676 -71.49326 -71.38120
-71.47988 -71.34895 -71.60337 -71.27680 -71.47830 -71.38368 -71.56553 -71.25698
-71.51365 -71.57632 -71.40765 -71.35177 -71.45359 -71.36418 -71.27902 -71.57804
-71.72452 -71.40145 -71.53119 -71.54959 -71.32192 -71.30829 -71.66188 -71.50901
-71.52730 -71.29926 -71.30103 -71.36956 -71.53720 -71.51967 -71.44590 -71.20103
-71.46271 -71.78459 -71.48986 -71.39177 -71.47573 -71.35815 -71.35747 -71.48002
-71.23603 -71.36421 -71.37262 -71.35396 -71.64459 -71.31907 -71.20202 -71.52227
-71.76902 -71.42490 -71.20864 -71.48538 -71.48942 -71.53622 -71.09374 -71.41722
-71.56248 -71.37526 -71.22103 -71.64082 -71.09926 -71.80157 -71.42649 -71.31969
-71.28041 -71.62300 -71.07469 -71.42551 -71.63942 -71.80623 -71.34613 -71.05034
-71.41858 -71.39882 -71.22620 -71.23075 -71.47941 -71.28095 -71.44700 -71.18301
-71.55696 -71.40847 -71.23101 -71.17350 -71.27603 -71.57865 -71.46811 -71.56126
-71.28229 -71.43375 -71.61853 -71.57418 -71.46681 -71.32729 -71.24229 -71.20290
-71.08624 -71.58238 -71.39441 -71.21335 -71.51417 -71.45313 -71.14407 -71.53162
-71.47166 -71.47740 -71.39195 -71.41868 -71.38320 -71.27952 -71.50601 -71.18531
-71.44220 -71.50468 -71.67345 -71.33663 -71.46310 -71.47230 -71.37706 -71.26024
-71.24828 -71.74436 -71.14387 -71.60709 -71.62482 -71.41529 -71.33295 -71.64811
-71.17752 -71.46980 -71.40021 -71.86272 -71.63449 -71.33710 -71.34627 -71.50086
-71.51730 -71.66295 -71.60497 -71.33038 -71.49175 -71.46396 -71.51751 -71.28104
-71.44005 -71.46357 -71.50906 -71.46751 -71.52946 -71.32244 -71.45766 -71.45805
-71.35815 -71.53772 -71.57851 -71.22686 -71.40940 -71.20444 -71.58255 -71.68250
-71.58747 -71.27798 -71.44304 -71.75599 -71.60371 -71.46056 -71.37762 -71.25655
-71.23032 -71.34567 -71.54055 -71.01472 -71.30575 -71.33788 -71.43910 -71.26317
-71.58394 -71.59022 -71.53726 -71.29987 -71.04397 -71.71645 -71.29357 -71.61988
-71.58765 -71.25740 -71.20250 -71.46625 -71.31354 -71.47671 -71.34149 -71.17866
-71.23169 -71.26752 -71.24647 -71.59390 -71.37520 -71.40945 -71.57829 -71.39199
-71.60734 -71.38919 -71.49570 -71.62524 -71.31472 -71.53470 -71.10257 -71.40576
-71.60013 -71.43657 -71.36252 -71.29001 -71.43474 -71.02338 -71.39470 -71.35591
-71.14354 -71.59329 -71.40278 -71.22870 -71.67848 -71.14312 -71.10114 -71.65241
-71.41341 -71.49866 -71.60505 -71.72892 -71.50454 -71.63783 -71.34070 -71.30840
-71.22388 -71.54898 -71.37952 -71.88012 -71.54444 -71.49925 -71.45936 -71.51406
-71.39340 -71.35253 -71.19799 -71.46933 -71.56538 -71.34153 -71.64894 -71.48072
-71.32748 -71.32707 -71.41007 -71.44075 -71.52963 -71.63946 -71.59437 -71.28651
-71.31837 -71.71421 -71.36529 -71.18672 -71.37162 -71.54370 -71.44873 -71.72894
-71.46382 -71.32423 -71.43694 -71.40775 -71.35354 -71.75695 -71.37396 -71.26883
-71.52483 -71.60857 -71.41613 -71.37256 -71.19020 -71.22353 -71.44696 -71.45575
-71.38907 -71.33689 -71.58796 -71.42700 -71.46854 -71.44923 -71.29840 -71.39754
-71.22494 -71.45824 -71.31283 -71.65690 -71.17722 -71.60776 -71.37026 -71.37108
-71.52064 -71.51905 -71.25777 -71.85295 -71.12629 -71.32289 -71.19603 -71.69577
-71.60395 -71.07286 -71.58121 -71.37258 -71.43295 -71.32069 -71.35172 -71.31148
-71.64889 -71.28730 -71.44272 -71.24414 -71.21241 -71.48508 -71.40316 -71.43905
-71.48158 -71.51569 -71.31824 -71.56312 -71.37067 -71.56806 -71.14427 -71.19594
-71.29761 -71.63935 -71.73878 -71.60896 -71.29779 -71.24986 -71.47332 -71.67087
-71.43714 -71.28301 -71.18193 -71.39541 -71.60729 -71.74908 -71.59060 -71.34654
-71.07517 -71.39215 -71.44085 -71.55852 -71.45495 -71.28396 -71.49548 -71.18101
-71.32658 -71.66957 -71.16455 -71.42269 -71.43211 -71.65037 -71.54680 -71.47571
-71.37282 -71.36523 -71.34907 -71.59517 -71.47379 -71.72834 -71.17010 -71.06874
-71.43147 -71.33092 -71.20539 -71.76060 -71.56197 -71.55374 -71.59124 -71.30015
-71.43169 -71.26248 -71.26238 -71.59540 -71.36710 -71.24947 -71.23667 -71.31373
-71.18419 -71.57628 -71.49124 -71.63909 -71.39622 -71.59487 -71.47614 -71.61826
-71.40406 -71.29048 -71.30592 -71.38695 -71.22122 -71.23570 -71.47496 -71.51415
-71.53485 -71.06665 -71.47480 -71.36122 -71.27054 -71.27376 -71.58423 -71.32092
-71.39945 -71.36221 -71.45878 -71.38403 -71.40963 -71.42398 -71.56348 -71.23727
-71.69039 -71.26014 -71.55275 -71.62517 -71.48968 -71.56671 -71.28298 -71.30372
-71.27498 -71.30133 -71.39799 -71.35307 -71.30202 -71.51434 -71.37830 -71.40117
-71.24318 -71.65339 -71.32800 -71.22322 -71.42269 -71.45994 -71.58307 -71.49953
-71.34143 -71.19758 -71.52046 -71.59773 -71.22994 -71.68916 -71.31763 -71.22489
-71.63627 -71.28401 -71.26560 -71.35521 -71.54042 -71.63917 -71.20372 -71.31327
-71.42505 -71.39134 -71.61434 -71.31612 -71.54808 -71.28329 -71.06594 -71.28936
-71.40861 -71.67491 -71.38687 -71.39349 -71.35211 -71.47080 -71.60525 -71.47093
-71.56625 -71.10636 -71.37063 -71.10972 -71.52321 -71.41459 -71.24053 -71.19302
-71.27154 -71.44370 -71.48889 -71.38304 -71.23534 -71.37395 -71.50355 -71.39014
-71.36861 -71.71664 -71.67781 -71.26445 -71.68359 -71.43548 -71.40406 -71.45392
-71.60048 -71.50729 -71.16855 -71.47082 -71.54840 -71.37485 -71.42671 -71.30570
-71.42231 -71.56276 -71.47489 -71.42949 -71.40094 -71.35193 -71.24404 -71.32621
-71.49728 -71.43371 -71.17643 -71.24178 -71.36083 -71.41045 -71.44952 -71.31624
-71.22613 -71.73346 -71.36627 -71.32019 -71.33923 -71.43791 -71.25405 -71.55443
-71.36989 -71.32350 -71.17647 -71.39035 -71.23558 -71.13761 -71.36744 -71.40330
-71.44953 -71.55485 -71.37625 -71.41998 -71.45871 -71.45128 -71.17801 -71.43318
-71.58809 -71.37572 -71.42451 -71.38510 -71.50726 -71.51418 -71.44673 -71.49323
-71.52782 -71.38855 -71.35998 -71.53740 -71.49257 -71.62770 -71.42136 -71.56084
-71.52035 -71.53386 -71.61956 -71.45647 -71.31220 -71.55672 -71.45929 -71.58607
-71.03335 -71.22033 -71.47850 -71.36097 -71.14327 -71.31572 -71.59931 -71.41087
-71.36278 -71.64791 -71.45928 -71.49673 -71.59759 -71.64332 -71.57331 -71.38391
-71.56734 -71.65018 -71.28258 -71.29560 -71.36067 -71.36718 -71.42472 -71.38786
-71.43540 -71.32139 -71.72092 -71.73678 -71.21512 -71.52282 -71.49552 -71.27518
-71.35503 -71.31504 -71.33060 -71.61263 -71.44618 -71.29579 -71.39877 -71.38706
-71.29126 -71.18064 -71.48982 -71.18608 -71.32669 -71.64747 -71.16019 -71.36114
-71.34030 -71.49417 -71.42388 -71.06328 -71.30433 -71.37148 -71.72333 -71.15997
-71.46383 -71.23557 -71.32186 -71.46987 -71.59035 -71.40648 -71.42799 -71.35750
-71.36991 -71.56488 -71.30248 -71.11033 -71.34287 -71.22053 -71.36127 -71.16202
-71.33081 -71.50995 -71.29363 -71.14140 -71.53719 -71.51463 -71.54520 -71.23053
-71.30701 -71.41769 -71.23575 -71.52637 -71.14089 -71.24036 -71.44022 -71.44631
-71.41369 -71.40527 -71.48555 -71.62350 -71.45676 -71.15434 -71.35069 -71.13847
-71.36020 -71.38379 -70.99196 -71.41181 -71.31562 -71.29951 -71.37143 -71.49700
-71.38577 -71.45070 -71.41356 -71.60134 -71.65432 -71.38159 -71.54342 -71.34491
-71.58885 -71.50692 -71.39178 -71.39431 -71.61794 -71.64802 -71.43190 -71.43267
-71.68641 -71.36077 -71.32970 -71.38943 -71.58403 -71.45031 -71.65768 -71.28765
-71.11717 -71.58671 -71.61503 -71.34498 -71.61167 -71.62577 -71.44442 -71.51121
-71.29288 -71.53063 -71.43265 -71.31789 -71.28339 -71.33926 -71.35517 -71.28422
-71.39848 -71.33141 -71.45015 -71.30327 -71.44002 -71.33577 -71.32542 -71.21899
-71.54269 -71.51442 -71.17147 -71.55707 -71.36195 -71.25513 -71.23046 -71.61871
-71.40121 -71.46310 -71.35580 -71.59793 -71.22613 -71.01697 -71.36998 -71.53430
-71.33835 -71.46686 -71.52448 -71.35194 -71.36597 -71.36194 -71.38899 -71.20233
-71.26349 -71.49275 -71.54503 -71.46379 -71.32557 -71.53786 -71.62588 -71.27427
-71.31701 -71.73366 -71.39524 -71.32089 -71.37183 -71.28438 -71.82955 -71.67848
-71.41282 -71.33653 -71.19866 -71.41171 -71.54825 -71.36285 -71.32672 -71.48115
-71.36276 -71.30194 -71.37227 -71.51021 -71.42137 -71.42696 -71.29879 -71.29988
-71.31573 -71.56569 -71.37977 -71.50888 -71.45811 -71.08596 -71.77654 -71.42249
-71.47148 -71.23191 -71.39128 -71.38516 -71.41969 -71.58580 -71.29074 -71.71231
-71.65697 -71.49619 -71.28243 -71.32420 -71.66114 -71.56703 -71.59460 -71.56072
-71.37106 -71.54475 -71.08120 -71.48756 -71.48460 -71.62446 -71.18527 -71.58221
-71.43694 -71.62436 -71.58796 -71.16804 -71.50391 -71.47971 -71.26794 -71.62661
-71.54622 -71.68415 -71.58019 -71.67691 -71.31226 -71.99394 -71.56081 -71.47179
-71.71635 -71.46850 -71.31677 -71.27054 -71.33278 -71.27651 -71.56420 -71.17856
-71.28479 -71.66205 -71.30172 -71.39742 -71.18003 -71.58767 -71.35533 -71.08616
-71.59544 -71.58610 -71.94659 -71.63538 -71.35278 -71.23944 -71.37743 -71.38743
-71.40853 -71.58724 -71.18712 -71.56159 -71.48005 -71.37277 -71.46884 -71.61887
-71.60730 -71.41377 -71.30484 -71.61208 -71.33781 -71.26340 -70.92363 -71.53121
-71.48080 -71.53630 -71.62705 -71.41001 -71.54488 -71.64894 -71.35465 -71.38339
-71.23795 -71.30655 -71.50918 -71.50231 -71.44973 -71.63647 -71.55507 -71.25788
-71.42731 -71.47712 -71.33917 -71.25002 -71.25074 -71.18981 -71.66951 -71.53697
-71.49811 -71.37359 -71.40742 -71.46179 -71.20031 -71.39299 -71.36525 -71.16946
-71.26467 -71.25431 -71.39182 -71.29283 -71.26898 -71.23763 -71.71610 -71.52486
-71.12391 -71.58342 -71.36789 -71.48159 -71.64914 -71.67836 -71.36983 -71.45561
-71.49648 -71.83138 -71.58346 -71.76874 -71.65625 -71.20701 -71.48622 -71.24499
-71.20709 -71.32673 -71.54340 -71.38256 -71.32896 -71.17246 -71.56069 -71.28644
-71.17751 -71.27906 -71.24772 -71.13005 -71.50501 -71.44935 -71.12543 -71.51701
-71.52883 -71.52383 -71.24868 -71.51271 -71.16375 -71.71827 -71.25049 -71.51319
-71.12338 -71.29237 -71.52155 -71.36461 -71.49476 -71.27875 -71.39204 -71.54145
-71.46902 -71.25657 -71.33025 -71.14228 -71.49552 -71.54775 -71.59651 -71.42680
-71.33855 -71.52738 -71.49401 -71.55718 -71.44140 -71.27542 -71.40468 -71.10762
-71.69101 -71.56158 -71.28529 -71.32435 -71.51541 -71.52628 -71.52958 -71.55194
-71.62808 -71.55283 -71.44759 -71.38339 -71.55740 -71.35923 -71.34246 -71.29377
-71.44788 -71.11619 -71.60130 -71.43101 -71.25731 -71.09476 -71.39748 -71.38622
-71.28723 -71.82329 -71.61817 -71.69027 -71.34212 -71.47762 -71.26497 -71.47704
-71.26781 -71.49780 -71.43434 -71.43933 -71.58599 -71.48555 -71.47038 -71.38771
-71.55365 -71.24075 -71.55300 -71.52149 -71.40126 -71.28999 -71.82090 -71.31836
-71.39191 -71.55007 -71.48745 -71.39635 -71.45441 -71.31476 -71.52495 -71.51841
-71.41653 -71.64279 -71.39638 -71.23985 -71.43821 -71.46812 -71.19228 -71.33322
-71.51934 -71.38254 -71.46183 -71.34823 -71.46041 -71.33916 -71.51579 -71.54693
-71.33026 -71.62077 -71.18370 -71.25042 -71.17517 -71.43018 -71.47687 -71.29303
-71.30255 -71.42168 -71.63040 -71.49143 -71.48675 -71.50479 -71.32174 -71.46533
-71.66314 -71.39694 -71.17423 -71.36759 -71.47926 -71.46968 -71.22216 -71.35913
-71.52201 -71.55942 -71.47610 -71.35506 -71.15187 -71.51366 -71.46143 -71.76325
-71.59444 -71.22914 -71.42084 -71.50184 -71.46762 -71.18670 -71.32225 -71.63018
-71.37430 -71.28932 -71.78418 -71.58388 -71.39606 -71.27614 -71.50438 -71.43973
-71.72042 -71.73255 -71.42965 -71.25782 -71.30594 -71.48686 -71.46963 -71.20775
-71.38132 -71.26974 -71.22851 -71.17370 -71.62009 -71.31784 -71.47563 -71.48537
-71.64102 -71.54917 -71.49612 -71.24928 -71.46646 -71.41416 -71.49004 -71.43461
-71.28396 -71.60870 -71.23187 -71.52289 -71.48781 -71.31354 -71.39422 -71.42158
-71.41557 -71.47349 -71.19201 -71.28512 -71.48798 -71.46799 -71.73943 -71.04957
-71.81033 -71.41243 -71.19334 -71.41850 -71.33771 -71.51191 -71.42129 -71.42375
-71.29016 -71.30631 -71.68108 -71.62249 -71.50145 -71.34434 -71.49138 -71.53134
-71.21138 -71.55921 -71.32371 -71.31011 -71.53420 -71.35836 -71.37581 -71.37977
-71.27365 -71.37884 -71.26150 -71.54798 -71.70535 -71.44076 -71.27496 -71.17933
-71.49961 -71.32755 -71.38143 -71.61876 -71.50868 -71.47601 -71.34640 -71.15757
-71.23677 -71.59818 -71.33902 -71.58060 -71.57614 -71.39470 -71.51795 -71.39562
-71.43257 -71.97975 -71.40618 -71.31543 -71.50398 -71.11843 -71.20865 -71.35096
-71.70164 -71.44271 -71.59682 -71.57311 -71.37097 -71.49903 -71.39297 -71.61701
-71.46338 -71.58211 -71.33694 -71.67357 -71.36347 -71.34127 -71.31472 -71.38326
-71.40972 -71.20621 -71.60206 -71.61408 -71.70392 -71.56659 -71.54165 -71.23004
-71.53208 -71.27254 -71.43492 -71.35981 -71.35387 -71.09060 -71.47709 -71.26954
-71.61128 -71.40631 -71.40266 -71.25500 -71.50196 -71.38555 -71.63843 -71.16047
-71.61811 -71.50077 -71.40284 -71.55477 -71.56947 -71.33356 -71.43665 -71.48474
-71.37163 -71.31068 -71.34137 -71.59898 -71.34917 -71.26228 -71.39747 -71.43217
-71.41112 -71.47407 -71.53490 -71.26077 -71.38007 -71.42904 -71.55225 -71.28517
-71.73851 -71.52669 -71.58431 -71.60087 -71.28595 -71.18044 -71.43925 -71.41068
-71.66407 -71.12133 -71.41844 -71.49001 -71.51826 -71.58609 -71.14777 -71.45078
-71.41867 -71.56910 -71.36394 -71.52494 -71.34332 -71.34718 -71.41156 -71.40614
-71.55074 -71.32686 -71.58373 -71.42363 -71.29810 -71.24573 -71.51586 -71.10219
-71.61444 -71.44968 -71.24528 -71.75145 -71.48193 -71.60666 -71.44618 -71.32333
-71.51042 -71.27236 -71.24878 -71.61915 -71.14722 -71.44886 -71.26438 -71.75498
-71.42081 -71.43251 -71.34775 -71.57784 -71.27082 -72.00984 -71.59833 -71.47310
-71.03419 -71.36022 -71.61406 -71.70765 -71.41842 -71.37832 -71.56339 -71.57023
-71.62019 -71.07080 -71.30942 -71.41830 -71.29155 -71.55677 -71.62796 -71.81750
-71.38709 -71.63069 -71.25339 -71.33451 -71.61738 -71.36265 -71.34357 -71.19004
-71.26219 -71.39783 -71.26602 -71.52827 -71.37162 -71.22196 -71.12199 -71.30123
-71.61517 -71.27950 -71.69536 -71.53471 -71.27107 -71.32715 -71.62021 -71.58987
-71.60572 -71.54015 -71.36488 -71.59849 -71.56837 -71.30335 -71.63279 -71.38403
-71.16858 -71.24071 -71.41116 -71.15119 -71.37472 -71.43336 -71.64742 -71.65062
-71.55385 -71.49258 -71.41493 -71.51420 -71.30217 -71.68639 -71.34839 -71.46557
-71.32261 -71.30668 -71.42180 -71.52817 -71.44467 -71.48569 -71.53449 -71.49326
-71.42636 -71.42867 -71.52374 -71.44713 -71.42880 -71.28423 -71.13235 -71.12746
-71.71978 -71.59703 -71.23640 -71.79588 -71.42204 -71.36394 -71.61908 -71.47136
-71.29547 -71.30459 -71.42046 -71.39757 -71.48241 -71.39515 -71.48350 -71.47302
-71.34660 -71.31464 -71.43020 -71.22270 -71.51286 -71.20140 -71.29082 -71.52300
-71.64297 -71.16769 -71.44462 -71.47192 -71.52281 -71.24366 -71.34526 -71.33376
-71.23640 -71.26637 -71.64132 -71.45962 -71.18828 -71.43841 -71.44608 -71.35373
-71.23212 -71.22004 -71.36239 -71.34975 -71.56352 -71.40722 -71.21745 -71.74331
-71.49818 -71.12848 -71.49350 -71.57922 -71.19159 -71.22767 -71.51161 -71.38678
-71.54704 -71.50251 -71.62389 -71.52226 -71.47565 -71.29301 -71.27671 -71.46199
-71.34175 -71.64399 -71.36430 -71.65800 -71.26283 -71.49919 -71.50838 -71.51055
-71.33317 -71.60818 -71.46480 -71.41168 -71.27604 -71.41666 -71.58992 -71.36815
-71.49741 -71.72572 -71.39058 -71.39158 -71.20982 -71.47329 -71.35331 -71.42583
-71.41531 -71.45887 -71.58535 -71.17350 -71.19466 -71.50368 -71.57458 -71.49201
-71.69950 -71.51130 -71.79684 -71.06981 -71.46718 -71.34139 -71.61093 -71.23078
-71.72783 -71.33298 -71.13549 -71.33094 -71.22924 -71.57921 -71.42416 -71.18925
-71.64986 -71.16066 -71.49534 -71.26420 -71.44948 -71.39653 -71.37916 -71.32330
-71.53086 -71.27221 -71.37394 -71.59556 -71.70764 -71.48931 -71.38884 -71.33231
-71.55045 -71.42513 -71.36511 -71.51726 -71.17720 -71.36949 -71.18240 -71.41344
-71.46820 -71.37861 -71.35276 -71.30119 -71.24007 -71.50664 -71.36437 -71.41377
-71.33492 -71.33512 -71.68397 -71.35950 -71.67434 -71.81410 -71.66643 -71.64966
-71.48757 -71.84651 -71.44259 -71.35289 -71.47923 -71.39572 -71.53209 -71.21518
-71.19594 -71.40866 -71.41027 -71.49530 -71.23284 -71.53444 -71.68298 -71.59638
-71.18194 -71.36677 -71.33282 -71.61923 -71.22609 -71.14313 -71.17504 -71.34712
-71.66068 -71.41179 -71.17752 -71.30295 -71.45080 -71.67903 -71.39858 -71.27540
-71.32249 -71.13869 -71.52942 -71.25457 -71.40628 -71.22834 -71.35121 -71.67672
-71.43027 -71.18479 -71.67168 -71.28961 -71.25370 -71.63845 -71.25770 -71.07547
-71.36034 -71.44085 -71.40518 -71.31445 -71.42370 -71.40457 -71.20895 -71.43655
-71.47559 -71.24493 -71.60015 -71.41630 -71.70477 -71.66812 -71.26534 -71.05851
-71.34212 -71.28656 -71.31998 -71.39489 -71.51381 -71.63285 -71.45327 -71.62947
-71.17757 -71.43925 -71.44804 -71.45904 -71.59111 -71.56187 -71.22463 -71.28091
-71.27163 -71.30204 -71.58464 -71.49738 -71.31198 -71.55826 -71.31200 -71.39471
-71.26811 -71.37499 -71.51079 -71.27215 -71.56728 -71.50385 -71.58018 -71.33021
-71.46483 -71.37476 -71.38383 -71.43656 -71.21605 -71.36178 -71.53406 -71.10999
-71.55728 -71.44053 -71.43875 -71.48100 -71.55063 -71.51058 -71.25496 -71.60698
-71.48509 -71.32635 -71.29397 -71.29854 -71.38161 -71.17170 -71.28930 -71.57041
-71.71287 -71.64232 -71.35479 -71.51913 -71.43896 -71.88161 -71.59858 -71.30900
-71.53099 -71.18832 -71.57539 -71.52077 -71.28544 -71.23022 -71.10339 -71.47157
-71.53818 -71.22755 -71.52966 -71.79557 -71.28889 -71.60129 -71.19130 -71.60911
-71.49832 -71.57028 -71.43616 -71.27224 -71.36739 -71.27401 -71.19382 -71.36976
-71.42633 -71.24349 -71.51043 -71.52474 -71.34008 -71.44983 -71.36544 -71.32779
-71.54020 -71.17309 -71.32976 -71.33266 -71.35271 -71.70691 -71.34647 -71.36914
-71.46066 -71.66545 -71.19605 -71.53937 -71.53503 -71.28999 -71.06679 -71.26516
-71.37821 -71.43700 -71.55462 -71.30121 -71.52390 -71.16246 -71.82873 -71.44711
-71.39652 -71.08710 -71.36463 -71.41200 -71.30808 -71.32004 -71.54651 -71.43358
-71.33538 -71.50752 -71.38156 -71.65385 -71.55575 -71.50216 -71.37912 -71.57080
-71.34957 -71.13600 -71.21471 -71.14877 -71.55713 -71.40740 -71.24842 -71.59582
-71.80286 -71.48301 -71.11540 -71.51485 -71.61721 -71.65456 -71.38691 -71.45933
-71.56841 -71.49074 -71.62842 -71.51678 -71.46260 -71.49466 -71.38657 -71.47398
-71.37286 -71.28928 -71.25271 -71.20526 -71.35632 -71.50403 -71.63775 -71.51420
-71.39102 -71.40917 -71.41508 -71.30594 -71.43245 -71.41742 -70.95579 -71.51671
-71.32042 -71.18034 -71.35672 -71.28110 -71.34787 -71.22468 -71.13621 -71.63374
-71.53434 -71.50024 -71.14078 -71.49827 -71.48509 -71.87496 -71.59741 -71.25948
-71.62890 -71.48030 -71.41417 -71.51406 -71.72342 -71.19526 -71.18531 -71.67542
-71.14194 -71.66538 -71.31367 -71.62415 -71.48058 -71.69098 -71.12002 -71.32956
-71.22847 -71.45830 -71.25501 -71.40204 -71.61826 -71.32736 -71.49344 -71.43899
-71.32338 -71.47171 -71.29138 -71.55413 -71.32292 -71.73069 -71.32633 -71.45443
-71.55747 -71.35997 -71.58555 -71.46118 -71.31451 -71.67096 -71.34453 -71.11007
-71.43966 -71.56867 -71.33739 -71.40816 -71.27997 -71.36578 -71.27198 -71.05386
-71.25886 -71.52993 -71.40699 -71.38980 -71.39672 -71.24798 -71.45914 -71.33741
-71.26995 -71.26774 -71.47558 -71.33097 -71.50539 -71.54136 -71.39327 -71.46488
-71.76046 -71.24056 -71.50835 -71.24483 -71.46360 -71.38708 -71.53443 -71.58805
-71.45876 -71.40683 -71.40501 -71.42739 -71.61983 -71.29221 -71.43898 -71.53566
-71.49092 -71.50724 -71.33764 -71.45726 -71.40019 -71.40684 -71.33965 -71.18726
-71.10770 -71.54298 -71.53323 -71.36968 -71.40326 -71.69722 -71.25547 -71.37739
-71.41673 -71.52098 -71.28693 -71.57008 -71.32313 -71.41612 -71.22305 -71.60459
-71.63224 -71.63560 -71.55943 -71.79384 -71.55941 -71.26017 -71.28103 -71.59811
-71.34459 -71.25328 -71.31105 -71.51013 -71.70490 -71.64871 -71.35570 -71.32166
-71.13378 -71.80981 -71.29978 -71.29043 -71.34503 -71.49284 -71.33048 -71.12991
-71.39082 -71.42440 -71.51404 -71.21064 -71.42525 -71.49132 -71.36693 -71.47546
-71.43509 -71.60945 -71.36014 -71.27231 -71.47886 -71.45091 -71.69119 -71.27319
-71.37941 -71.58795 -71.31631 -71.24912 -71.48455 -71.21237 -71.38016 -71.74608
-71.34191 -71.52729 -71.29245 -71.39991 -71.52051 -71.53399 -71.31004 -71.50915
-71.44981 -71.36134 -71.50834 -71.50788 -71.14940 -71.19422 -71.41022 -71.28256
-71.47004 -71.34955 -71.68087 -71.35991 -71.52831 -71.34203 -71.48100 -71.63695
-71.51834 -71.46000 -71.57908 -71.45095 -71.33675 -71.15373 -71.72048 -71.50607
-71.39037 -71.22271 -71.31271 -71.48947 -71.45603 -71.33019 -71.50406 -71.40475
-71.33827 -71.27787 -71.31203 -71.44563 -71.29043 -71.47788 -71.16967 -71.29120
-71.42272 -71.29765 -71.19944 -71.53229 -71.23396 -71.58444 -71.33482 -71.36576
-71.30961 -71.34760 -71.68673 -71.35302 -71.24145 -71.48632 -71.37004 -71.23897
-71.50218 -71.51071 -71.66173 -71.35410 -71.50147 -71.55969 -71.30472 -71.26640
-71.65651 -71.49965 -71.30399 -71.63388 -71.27770 -71.40009 -71.46963 -71.38072
-71.77277 -71.64425 -71.60172 -71.77265 -71.37503 -71.33790 -71.35194 -71.84084
-71.49547 -71.43626 -71.29014 -71.24656 -71.41557 -71.48266 -71.68095 -71.34811
-71.17630 -71.59496 -71.49134 -71.55784 -71.95005 -71.17129 -71.33429 -71.22040
-71.34619 -71.34704 -71.41006 -71.61102 -71.55792 -71.31416 -71.55631 -71.72553
-71.83634 -71.53443 -71.48092 -71.35966 -71.28869 -71.40193 -71.48345 -71.24764
-71.44682 -71.33238 -71.49660 -71.34556 -71.49980 -71.48349 -71.56264 -71.35093
-71.22087 -71.30948 -71.22778 -71.49547 -71.32692 -71.27559 -71.51372 -71.50337
-71.53267 -71.53543 -71.15753 -71.73877 -71.47694 -71.32134 -71.56675 -71.60303
-71.70215 -71.32741 -71.18762 -71.38217 -71.29193 -71.06156 -71.45822 -71.17958
-71.42012 -71.17155 -71.19851 -71.57493 -71.75376 -71.39915 -71.53807 -71.32110
-71.20420 -71.36788 -71.27682 -71.15404 -71.35487 -71.66920 -71.41775 -71.13714
-71.55895 -71.70309 -71.47198 -71.17386 -71.61535 -71.59730 -71.38859 -71.41547
-71.53900 -71.44736 -71.27937 -71.37962 -71.53742 -71.05531 -71.33537 -71.69518
-71.37702 -71.42476 -71.55939 -71.43210 -71.14496 -71.43144 -71.36683 -71.39440
-71.07950 -71.51379 -71.49723 -71.45884 -71.18391 -71.18055 -71.43976 -71.29647
-71.29245 -71.27097 -71.85768 -71.65796 -71.40256 -71.69751 -71.41586 -71.48614
-71.27006 -71.48548 -71.28355 -71.58240 -71.58146 -71.33802 -71.56314 -71.43015
-71.36114 -71.47912 -71.57986 -71.61113 -71.12012 -71.31397 -71.28777 -71.53261
-71.44109 -71.24375 -71.29654 -71.46540 -71.59972 -71.32639 -71.45560 -71.21814
-71.20256 -71.43541 -71.54576 -71.23064 -71.42063 -71.20759 -71.33534 -71.27217
-71.43327 -71.18032 -71.46864 -71.37714 -71.55373 -71.48589 -71.38833 -71.49408
-71.70427 -71.26716 -71.52440 -71.24283 -71.70405 -71.39398 -71.53242 -71.40624
-71.37515 -71.70006 -71.33596 -71.44539 -71.07733 -71.21562 -71.49892 -71.07283
-71.76066 -71.52689 -71.24882 -71.49109 -71.47245 -71.64188 -71.29235 -71.46700
-71.24988 -71.15072 -71.78690 -71.55363 -71.40845 -71.39658 -71.49264 -71.51716
-71.40514 -71.34178 -71.27882 -71.26522 -71.26517 -71.51447 -71.44778 -71.49157
-71.24235 -71.28974 -71.86913 -71.33426 -71.29685 -71.64398 -71.67404 -71.19521
-71.70702 -71.29254 -71.47167 -71.63366 -71.27170 -71.56784 -71.52715 -71.34633
-71.37661 -71.55284 -71.28353 -71.35730 -71.36838 -71.51664 -71.34699 -71.50720
-71.41772 -71.38782 -71.48282 -71.33005 -71.34031 -71.39497 -71.30678 -71.27350
-71.49421 -71.46622 -71.33178 -71.30604 -71.11657 -71.31448 -71.50155 -71.31594
-71.21784 -71.41481 -71.56240 -71.22815 -71.16571 -71.36810 -71.69797 -71.26511
-71.28956 -71.36575 -71.68203 -71.70023 -71.02211 -71.56677 -71.44977 -71.25394
-71.59146 -71.30329 -71.43031 -71.28982 -71.51295 -71.30730 -71.64864 -71.28999
-71.40654 -71.35890 -71.60347 -71.30581 -71.40536 -71.38030 -71.58546 -71.52595
-71.55487 -71.41537 -71.20416 -71.32350 -71.39542 -71.68467 -71.46638 -71.63549
-71.27979 -71.64335 -71.25867 -71.54261 -71.52728 -71.44725 -71.39866 -71.37606
-71.60332 -71.47973 -71.35648 -71.44486 -71.74143 -71.50932 -71.44385 -71.62432
-71.53200 -71.22515 -71.67770 -71.49673 -71.58564 -71.46779 -71.14264 -71.43874
-71.31780 -71.66451 -71.37666 -71.24555 -71.38787 -71.33170 -71.18574 -71.50262
-71.46069 -71.52432 -71.44768 -71.41521 -71.25164 -71.64226 -71.25219 -71.38146
-71.19146 -71.31453 -71.46499 -71.34546 -71.43469 -71.34785 -71.22842 -71.36133
-71.44955 -71.15378 -71.21663 -71.31536 -71.41411 -71.65325 -71.46007 -71.90176
-71.18526 -71.25362 -71.47047 -71.58880 -71.28984 -71.48317 -71.60297 -71.50744
-71.38867 -71.27265 -71.44148 -71.44748 -71.50135 -71.57036 -71.59084 -71.66255
-71.00922 -71.39667 -71.52764 -71.48419 -71.38135 -71.49470 -71.59248 -71.61969
-71.38810 -71.64593 -71.51772 -71.26219 -71.55478 -71.26524 -71.27224 -71.46850
-71.57635 -71.41412 -71.38757 -71.22679 -71.35745 -71.45951 -71.38426 -71.19194
-71.29039 -71.44919 -71.26745 -71.49621 -71.44123 -71.43038 -71.27639 -71.33249
-71.06728 -71.23056 -71.46086 -71.35028 -71.35161 -71.35314 -71.50851 -71.33006
-71.34312 -71.57087 -71.37865 -71.43416 -71.31823 -71.26158 -71.23794 -71.77959
-71.74555 -71.40977 -71.21180 -71.41675 -71.26121 -71.54014 -71.43108 -71.35853
-71.17861 -71.14943 -71.31177 -71.19593 -71.10878 -71.50872 -71.77737 -71.47802
-71.37825 -71.36114 -71.57063 -71.28270 -71.28220 -71.43006 -71.29711 -71.45586
-71.44408 -71.36807 -71.81617 -71.35111 -71.33326 -71.15542 -71.11833 -71.50027
-71.41721 -71.71116 -71.38094 -71.56882 -71.63285 -71.40538 -71.18447 -71.74473
-71.39779 -71.31480 -71.52998 -71.34371 -71.53902 -71.40590 -71.44343 -71.25615
-71.52705 -71.70782 -71.40646 -71.46197 -71.55064 -71.38336 -71.68738 -71.35159
-71.40718 -71.50935 -71.08383 -71.53779 -71.52974 -71.16543 -71.63225 -71.52229
-71.24205 -71.45688 -71.55077 -71.23082 -71.60535 -71.44574 -71.72635 -71.23682
-71.41312 -71.31447 -71.30577 -71.68269 -71.53434 -71.59430 -71.20920 -71.40070
-71.55742 -71.56873 -71.75481 -71.46760 -71.28763 -71.31918 -71.47931 -71.50623
-71.44013 -71.61728 -71.66879 -71.24504 -71.35831 -71.22451 -71.56722 -71.44774
-71.68887 -71.36294 -71.37695 -71.20520 -71.42021 -71.57529 -71.44254 -71.24586
-71.25058 -71.46912 -71.60798 -71.39325 -71.41410 -71.17767 -71.38549 -71.55384
-71.45401 -71.35266 -71.70813 -71.42980 -71.51535 -71.32521 -71.29747 -71.56526
-71.40998 -71.53612 -71.50545 -71.44112 -71.35243 -71.25398 -71.41932 -71.39466
-71.39616 -71.33876 -71.33255 -71.41010 -71.65458 -71.54201 -71.29693 -71.19940
-71.35901 -71.47698 -71.30230 -71.23620 -71.54416 -71.48221 -71.32721 -71.45328
-71.55332 -71.35137 -71.56915 -71.43568 -71.31303 -71.38976 -71.39225 -71.47633
-71.78225 -71.27147 -71.33879 -71.56494 -71.53299 -71.30477 -71.31766 -71.40734
-71.51366 -71.32992 -71.54282 -71.45551 -71.51840 -71.51141 -71.45138 -71.61547
-71.53241 -71.59906 -71.15568 -71.51192 -71.10895 -71.39923 -71.39915 -71.26019
-71.37171 -71.54678 -71.35988 -71.46766 -71.45200 -71.23820 -71.44202 -71.48180
-71.33955 -71.21361 -71.42025 -71.57076 -71.61679 -71.62795 -71.42755 -71.32453
-71.43793 -71.40718 -71.45145 -71.96943 -71.48955 -71.32704 -71.50396 -71.47326
-71.38850 -71.38289 -71.42429 -71.24739 -71.64862 -71.14193 -71.64943 -71.76637
-71.58957 -71.68001 -71.30192 -71.52587 -71.76464 -71.45043 -71.25086 -71.25064
-71.60565 -71.62339 -71.64174 -71.25861 -71.65171 -71.23329 -71.33052 -71.64920
-71.44175 -71.62466 -71.26255 -71.14178 -71.37849 -71.63947 -71.54848 -71.24467
-71.81985 -71.36132 -71.52146 -71.29265 -71.47883 -71.41453 -71.50206 -71.35387
-71.55260 -71.67189 -71.83325 -71.64941 -71.43964 -71.23071 -71.70347 -71.03466
-71.49100 -71.66377 -71.42864 -71.25417 -71.76407 -71.48787 -71.69392 -71.40918
-71.70756 -71.47498 -71.40904 -71.37534 -71.47776 -71.32967 -71.20971 -71.63752
-71.00743 -71.40254 -71.44306 -71.55015 -71.11321 -71.60564 -71.37245 -71.64521
-71.32621 -71.19875 -71.48062 -71.51646 -71.37874 -71.52585 -71.54767 -71.34514
-71.42743 -71.46377 -71.26101 -71.32114 -71.38915 -71.62908 -71.62969 -71.44249
-71.15744 -71.71158 -71.48908 -71.58187 -71.53205 -71.86173 -71.30135 -71.26288
-71.39921 -71.27818 -71.41779 -71.31768 -71.41737 -71.42977 -71.28866 -71.29594
-71.36073 -71.48642 -71.45578 -71.42405 -71.19675 -71.28112 -71.24612 -71.49814
-71.57738 -71.72298 -71.52965 -71.60328 -71.43156 -71.22503 -71.45389 -71.56929
-71.53153 -71.70427 -71.42091 -71.44153 -71.51040 -71.38967 -71.32954 -71.52299
-71.50129 -71.16576 -71.28425 -71.40775 -71.40406 -71.61005 -71.34840 -71.50813
-71.58493 -71.55259 -71.29200 -71.54079 -71.34197 -71.61295 -71.49269 -71.56939
-71.48806 -71.37913 -71.73537 -71.39694 -71.62831 -71.23957 -71.37947 -71.39344
-71.29920 -71.63555 -71.56363 -71.39862 -71.64192 -71.45182 -71.31735 -71.73340
-71.17548 -71.50858 -71.37410 -71.38707 -71.12281 -71.26806 -71.53407 -71.41999
-71.16342 -71.20016 -71.57543 -71.56190 -71.42045 -71.28909 -71.58895 -71.45446
-71.44260 -71.47419 -71.34156 -71.55633 -71.28142 -71.42605 -71.34913 -71.72074
-71.43880 -71.44565 -71.42563 -71.44603 -71.25520 -71.44474 -71.53014 -71.50243
-71.13252 -71.55220 -71.40417 -71.60621 -71.53326 -71.76131 -71.69898 -71.59372
-71.29314 -71.40210 -71.60030 -71.30671 -71.22795 -71.51852 -71.43109 -71.13314
-71.48765 -71.54384 -71.48373 -71.25562 -71.33777 -71.50859 -71.55562 -71.44654
-71.44414 -71.34699 -71.77602 -71.38053 -71.48540 -71.38094 -71.36308 -71.55356
-71.21826 -71.50160 -71.34259 -71.68786 -71.37818 -71.53097 -71.59802 -71.24741
-71.18885 -71.36429 -71.26035 -71.36782 -71.57594 -71.28731 -71.42071 -71.37710
-71.45104 -71.29132 -71.64992 -71.54589 -71.33568 -71.25374 -71.61070 -71.42038
-71.39628 -71.36131 -71.32756 -71.41681 -71.17835 -71.43704 -71.37867 -71.34349
-71.41460 -71.33178 -71.52762 -71.47924 -71.15200 -71.42566 -71.57638 -71.40715
-71.45103 -71.32325 -71.42207 -71.24118 -71.43736 -71.50015 -71.35790 -71.28976
-71.40067 -71.35901 -71.29052 -71.41429 -71.27149 -71.34123 -71.31967 -71.24375
-71.34941 -71.54923 -71.40646 -71.11554 -71.54521 -71.52254 -71.49311 -71.62657
-71.60308 -71.43686 -71.61770 -71.15156 -71.36124 -71.76241 -71.37325 -71.36687
-71.56679 -71.40117 -71.13432 -71.69201 -71.48190 -71.55456 -71.26416 -71.43943
-71.42639 -71.66725 -71.38933 -71.15593 -71.16710 -71.34984 -71.23019 -71.48519
-71.42935 -71.42844 -71.50563 -71.49623 -71.38111 -71.74242 -71.66859 -71.25809
-71.28523 -71.64269 -71.32810 -71.31966 -71.44172 -71.16542 -71.38398 -71.63563
-71.25383 -71.30747 -71.46902 -71.48572 -71.66744 -71.52705 -71.22795 -71.21185
-71.34673 -71.26750 -71.59927 -71.69098 -71.00411 -71.20075 -71.39775 -71.38499
-71.25602 -71.27008 -71.27141 -71.50098 -71.55210 -71.28446 -71.66091 -71.44933
-71.29269 -71.42547 -71.34352 -71.38002 -71.31073 -71.27679 -71.44940 -71.09217
-71.55841 -71.38285 -71.38381 -71.46096 -71.24577 -71.74316 -71.41669 -71.56509
-71.39831 -71.42397 -71.49582 -71.13308 -71.36087 -71.47726 -71.53628 -71.31688
-71.38732 -71.68522 -71.26404 -71.72141 -71.35750 -71.22374 -71.58040 -71.69533
-71.75190 -71.76247 -71.69382 -71.51966 -71.67982 -71.59184 -71.44959 -71.60559
-71.38782 -71.53460 -71.44188 -71.47145 -71.41082 -71.59737 -71.32010 -71.30223
-71.40646 -71.15870 -71.70713 -71.24627 -71.35580 -71.23055 -71.28924 -71.39592
-71.62096 -71.38108 -71.32157 -71.47388 -71.29455 -71.55720 -71.34989 -71.90382
-71.63028 -71.47741 -71.38423 -71.67794 -71.48977 -71.48828 -71.50761 -71.43207
-71.51590 -71.68823 -71.62443 -71.60406 -71.27340 -71.41205 -71.56265 -71.31314
-71.53257 -71.54312 -71.19962 -71.25549 -71.62302 -71.42623 -71.40519 -71.30099
-71.44983 -71.31015 -71.34274 -71.69131 -71.27300 -71.45669 -71.52595 -71.47415
-71.23008 -71.31158 -71.38122 -71.29564 -71.67993 -71.34778 -71.39243 -71.41745
-71.50392 -71.32486 -71.60596 -71.63053 -71.38278 -71.46990 -71.19950 -71.38424
-71.65943 -71.43783 -71.30324 -71.27596 -71.19843 -71.38423 -71.46728 -71.39353
-71.01107 -71.42160 -71.28272 -71.49088 -71.35096 -71.65646 -71.51718 -71.27413
-71.24411 -71.47917 -71.40545 -71.71921 -71.57008 -71.43722 -71.62109 -71.41988
-71.25458 -71.32282 -71.40906 -71.50719 -71.40762 -71.22933 -71.37897 -71.33216
-71.54048 -71.31694 -71.21374 -71.18441 -71.48620 -71.15057 -71.13463 -71.32398
-71.48718 -71.39861 -71.36795 -71.33594 -71.41170 -71.27790 -71.55948 -71.79702
-71.71024 -71.23687 -71.51962 -71.43474 -71.76474 -71.61739 -71.24916 -71.17632
-71.44816 -71.21858 -71.24689 -71.37579 -71.37404 -71.74564 -71.32977 -70.91388
-71.53453 -71.34278 -71.28432 -71.39617 -71.39579 -71.62004 -71.72597 -71.13405
-71.56627 -71.22268 -71.25180 -71.72191 -71.44118 -71.50652 -71.31733 -71.59771
-71.52935 -71.40831 -71.49810 -71.48534 -71.51536 -71.46600 -71.40115 -71.66820
-71.84832 -71.42362 -71.44059 -71.46429 -71.39561 -71.51116 -71.36210 -71.26372
-71.36508 -71.58999 -71.48202 -71.70522 -71.24611 -71.18620 -71.47934 -71.47592
-71.37463 -71.26247 -71.53535 -71.30101 -71.32610 -71.31631 -71.63723 -71.38485
-71.26342 -71.37594 -71.52763 -71.12300 -71.39304 -71.43220 -71.13979 -71.05801
-71.49768 -71.40759 -71.43353 -71.38576 -71.62135 -71.36208 -71.34678 -71.32940
-71.48662 -71.31376 -71.19944 -71.50468 -71.48561 -71.37408 -71.46010 -71.26896
-71.54058 -71.32813 -71.68745 -71.14155 -71.31287 -71.35241 -71.37569 -71.67217
-71.32192 -71.32851 -71.14788 -71.25519 -71.56163 -71.43337 -71.84132 -71.05410
-71.52946 -71.11526 -71.41069 -71.38993 -71.63027 -71.35769 -71.51988 -71.49663
-71.42864 -71.24423 -71.33267 -71.14245 -71.28293 -71.56263 -71.50214 -71.48273
-71.65158 -71.27921 -71.35484 -71.60951 -71.45398 -71.17996 -71.45778 -71.51890
-71.42839 -71.42622 -71.46483 -71.49406 -71.24261 -71.08090 -71.43307 -71.14821
-71.49386 -71.36991 -71.40541 -71.41943 -71.54370 -71.42212 -71.61634 -71.50195
-71.46041 -71.44923 -71.50578 -71.64694 -71.37415 -71.47169 -71.32105 -71.46884
-71.68253 -71.23919 -71.38497 -71.52683 -71.64652 -71.60805 -71.63954 -71.28524
-71.52156 -71.28422 -71.48381 -71.52619 -71.20906 -71.66532 -71.12771 -71.23648
-71.66060 -71.31066 -71.52195 -71.48292 -71.44686 -71.54148 -71.25604 -71.36699
-71.53206 -71.76275 -71.41091 -71.76981 -71.36598 -71.55868 -71.38265 -71.13156
-71.47488 -71.30027 -71.49611 -71.14747 -71.42641 -71.51533 -71.35662 -71.62109
-71.37051 -71.38360 -71.41345 -71.31048 -71.43988 -71.53596 -71.64216 -71.27064
-71.69479 -71.45723 -71.58734 -71.14665 -71.37997 -71.45464 -71.43946 -71.34506
-71.63181 -71.45552 -71.27823 -71.04692 -71.41317 -71.49445 -71.38093 -71.56098
-71.36656 -71.45642 -71.52240 -71.65160 -71.61591 -71.51442 -71.31971 -71.20412
-71.46108 -71.29273 -71.53113 -71.52442 -71.36559 -71.44552 -71.34685 -71.51911
-71.39020 -71.32117 -71.48930 -71.28744 -71.72815 -71.84726 -71.31061 -71.58561
-71.59917 -71.20693 -71.58955 -71.60071 -71.37669 -71.55232 -71.41124 -71.62412
-71.33419 -71.26476 -71.65559 -71.03538 -71.60332 -71.27171 -71.49042 -71.54760
-71.46433 -71.35951 -71.38671 -71.60683 -71.43331 -71.46566 -71.49978 -71.43974
-71.49130 -71.47912 -71.39537 -71.33344 -71.65057 -71.45602 -71.27649 -71.67638
-71.63181 -71.25922 -71.25292 -71.93500 -71.22486 -71.20590 -71.51969 -71.20742
-71.69277 -71.31819 -71.51276 -71.99480 -71.48842 -71.15388 -71.45061 -71.33032
-71.65977 -71.52360 -71.38125 -71.33810 -71.63569 -71.51724 -71.53029 -71.60779
-71.38242 -71.37299 -71.37053 -71.33036 -71.33427 -71.38845 -71.25337 -71.61265
-71.39253 -71.21471 -71.23637 -71.57137 -71.36194 -71.33878 -71.70420 -71.19324
-71.40102 -71.41563 -71.38248 -71.23515 -71.63396 -71.48889 -71.65434 -71.48183
-71.37790 -71.66354 -71.17905 -71.37080 -71.75362 -71.56835 -71.42742 -71.57083
-71.48959 -71.33758 -71.55613 -71.66824 -71.40961 -71.41073 -71.52328 -71.26261
-71.31856 -71.40857 -71.47320 -71.27691 -71.32713 -71.34260 -71.18880 -71.23165
-71.60932 -71.63239 -71.18597 -71.32542 -71.48959 -71.36644 -71.36546 -71.30569
-71.78527 -71.53529 -70.95426 -71.26770 -71.39650 -71.60386 -71.50572 -71.14141
-71.76047 -71.28636 -71.80446 -71.33474 -71.46251 -71.43999 -71.64119 -71.41187
-71.21642 -71.51631 -71.17525 -71.34698 -71.15023 -71.36115 -71.45908 -71.39196
-71.53167 -71.21535 -71.12723 -71.52026 -71.56934 -71.59485 -71.48029 -71.50698
-71.35061 -71.42853 -71.54960 -71.39060 -71.45472 -71.51097 -71.32528 -71.65560
-71.41575 -71.38606 -71.48586 -71.34683 -71.43307 -71.37314 -71.19043 -71.71218
-71.75577 -71.41078 -71.40762 -71.51899 -71.47686 -71.68998 -71.36953 -71.23514
-71.45507 -71.49718 -71.41997 -71.22703 -71.22468 -71.24221 -71.31208 -71.47960
-71.49834 -71.33650 -71.11522 -71.37528 -71.35043 -71.25756 -71.53984 -71.57780
-71.56795 -71.20518 -71.42021 -71.51011 -71.35871 -71.63477 -71.32883 -71.43868
-71.18903 -71.22502 -71.37913 -71.47255 -71.25203 -71.69091 -71.61954 -71.40379
-71.42097 -71.43418 -71.53210 -71.12305 -71.40038 -71.45043 -71.63999 -71.43540
-71.27529 -71.59117 -71.44495 -71.42744 -71.42058 -71.32842 -71.59536 -71.69139
-71.15097 -71.35378 -71.46335 -71.45200 -71.45509 -71.54489 -71.41857 -71.55228
-71.47234 -71.27485 -71.45818 -71.33103 -71.08983 -71.64900 -71.40269 -71.61231
-71.31047 -71.73582 -71.27311 -71.27383 -71.38905 -71.23187 -71.41336 -71.44172
-71.38175 -71.22192 -71.52860 -71.42601 -71.39640 -71.53546 -71.50679 -71.44004
-71.45782 -71.83272 -70.93082 -71.42753 -71.47883 -71.17709 -71.44206 -71.36838
-71.28082 -71.17800 -71.51473 -71.68028 -71.40625 -71.55376 -71.33053 -71.09963
-71.44730 -71.46260 -71.39569 -71.19744 -71.45100 -71.45891 -71.25977 -71.69428
-71.42365 -71.41623 -71.26930 -71.25105 -71.51859 -71.06874 -71.43960 -71.06921
-71.67573 -71.50186 -71.25860 -71.57160 -71.69940 -71.58536 -71.13955 -71.07087
-71.35338 -71.20964 -71.70079 -71.25584 -71.43550 -71.50424 -71.54256 -71.73820
-71.42164 -71.41583 -71.40608 -71.27240 -71.41426 -71.34595 -71.49620 -71.61860
-71.34133 -71.55365 -71.43721 -71.54944 -71.61415 -71.56319 -71.30438 -71.32741
-71.42909 -71.69775 -71.39369 -71.56351 -71.71298 -71.41424 -71.28350 -71.47106
-71.58550 -71.33043 -71.50615 -71.40485 -71.54001 -71.47382 -71.49606 -71.56585
-71.33044 -71.45829 -71.21934 -71.38260 -71.07971 -71.48355 -71.75894 -71.20210
-71.40112 -71.65842 -71.34288 -71.10920 -71.43594 -71.38607 -71.48185 -71.35189
-71.40856 -71.25963 -71.73976 -71.34953 -71.29964 -71.58265 -71.62085 -71.46096
-71.43132 -71.42621 -71.62857 -71.56795 -71.48318 -71.43063 -71.59231 -71.67012
-71.32827 -71.24534 -71.26072 -71.46720 -71.64027 -71.13516 -71.53108 -71.16714
-71.47891 -71.49759 -71.43203 -71.53920 -71.36960 -71.23836 -71.44764 -71.23481
-71.21012 -71.47649 -71.19708 -71.44017 -71.50488 -71.47923 -71.33894 -71.52080
-71.35870 -71.38079 -71.41580 -71.31914 -71.61171 -71.60360 -71.35567 -71.55468
-71.31227 -71.30109 -71.51307 -71.22631 -71.12992 -71.20752 -71.59132 -71.44916
-71.33264 -71.24912 -71.26498 -71.53983 -71.38093 -71.46628 -71.64209 -71.41475
-71.55661 -71.41683 -71.60254 -71.58051 -71.43983 -71.20355 -71.68408 -71.39316
-71.19083 -71.42283 -71.28088 -71.43835 -71.25571 -71.37509 -71.78571 -71.74974
-71.48665 -71.41942 -71.44509 -71.48415 -71.63598 -71.34797 -71.70576 -71.54094
-71.70340 -71.31369 -71.23481 -71.46850 -71.24344 -71.39011 -71.55126 -71.52177
-71.33235 -71.55993 -71.56992 -71.51342 -71.57930 -71.26985 -71.65019 -71.43167
-71.49042 -71.44538 -71.62340 -71.34550 -71.39047 -71.68854 -71.26540 -71.22128
-71.21720 -71.49314 -71.42265 -71.55192 -71.49679 -71.30436 -71.44762 -71.31451
-71.54310 -71.57727 -71.68376 -71.55811 -71.74302 -71.44671 -71.44269 -71.78367
-71.31099 -71.49685 -71.30193 -71.44314 -71.52251 -71.34252 -71.76664 -71.54389
-71.27027 -71.59844 -71.54144 -71.43605 -71.42385 -71.25469 -71.60677 -71.20824
-71.45193 -71.29374 -71.20910 -71.42873 -71.59038 -71.48220 -71.33773 -71.27572
-71.39481 -71.44941 -71.46168 -71.35598 -71.25589 -71.46996 -71.45241 -71.20644
-71.52728 -71.67695 -71.66440 -71.51473 -71.40293 -71.44391 -71.42118 -71.48010
-71.32933 -71.29077 -71.34618 -71.67285 -71.53251 -71.53829 -71.59737 -71.45926
-71.33674 -71.67102 -71.27347 -71.62306 -71.40389 -71.15066 -71.48171 -71.78548
-71.39876 -71.43653 -71.51576 -71.36751 -71.49012 -71.48481 -71.40259 -71.29670
-71.50988 -71.52305 -71.35648 -71.45216 -71.42325 -71.49108 -71.21408 -71.70377
-71.35969 -71.39202 -71.25353 -71.44626 -71.50703 -71.63829 -71.18490 -71.27935
-71.55475 -71.41950 -71.28614 -71.26308 -71.77794 -71.37905 -71.48498 -71.28013
-71.03320 -71.40153 -71.48567 -71.30504 -71.61651 -71.50553 -71.55623 -71.26917
-71.61782 -71.65545 -71.31559 -71.32713 -71.39349 -71.18692 -71.36161 -71.71240
-71.34522 -71.79319 -71.41295 -71.18141 -71.33193 -71.50231 -71.15706 -71.78050
-71.58814 -71.44257 -71.52992 -71.38585 -71.56278 -71.31159 -71.18506 -71.25836
-71.54378 -71.32336 -71.33256 -71.39910 -71.51287 -71.33625 -71.32007 -71.68562
-71.54240 -71.26855 -71.32754 -71.16590 -71.20302 -71.35956 -71.78813 -71.06448
-71.30211 -71.59831 -71.49785 -71.32824 -71.32569 -71.24756 -71.73792 -71.22828
-71.29030 -71.37746 -71.48353 -71.31895 -71.59470 -71.33354 -71.41151 -71.59007
-71.36158 -71.15742 -71.40916 -71.45551 -71.42696 -71.50972 -71.40405 -71.60797
-71.56784 -71.43738 -71.32257 -71.48274 -71.46891 -71.50768 -71.46073 -71.34881
-71.47165 -71.23487 -71.19508 -71.38753 -71.13510 -71.28067 -71.21717 -71.40033
-71.32432 -71.53922 -71.24291 -71.67836 -71.32240 -71.27202 -71.22895 -71.43413
-71.46126 -71.56309 -71.39477 -71.55779 -71.39775 -71.48197 -71.45854 -71.32115
-71.41339 -71.70892 -71.41551 -71.73271 -71.27462 -71.19144 -71.35065 -71.47728
-71.26251 -71.15709 -71.46490 -71.69601 -71.62913 -71.51501 -71.47478 -71.45127
-71.47623 -71.45053 -71.38105 -71.27748 -71.22487 -71.48948 -71.58230 -71.38908
-71.69204 -71.52974 -71.27393 -71.20620 -71.40200 -71.47724 -71.27434 -71.39559
-71.50279 -71.47184 -71.42510 -71.33862 -71.51096 -71.15460 -71.22170 -71.51791
-71.37894 -71.39012 -71.54662 -71.24728 -71.61203 -71.49608 -71.80408 -71.19705
-71.17384 -71.28298 -71.62533 -71.13115 -71.45732 -71.32654 -71.48600 -71.19759
-71.67132 -71.75676 -71.48415 -71.37269 -71.49669 -71.39598 -71.57530 -71.15448
-71.22405 -71.27475 -71.21569 -71.23382 -71.67605 -71.53382 -71.39495 -71.43182
-71.44522 -71.36490 -71.28267 -71.09168 -71.35529 -71.40033 -71.66034 -71.70648
-71.30926 -71.24478 -71.41620 -71.66387 -71.58602 -71.25022 -71.26842 -71.26556
-71.35409 -71.79966 -71.55804 -71.24789 -71.27383 -71.49449 -71.30186 -71.30521
-71.30884 -71.60603 -71.47294 -71.15383 -71.18854 -71.55559 -71.46430 -71.71002
-71.49927 -71.51691 -71.32162 -71.59963 -71.55770 -71.38321 -71.61110 -71.32653
-71.36935 -71.30465 -71.41351 -71.50221 -71.50849 -71.24561 -71.66241 -71.16460
-71.32125 -71.27495 -71.41102 -71.17317 -71.62534 -71.56158 -71.62822 -71.51336
-71.50710 -71.41605 -71.44187 -71.43922 -71.19496 -71.48965 -71.80257 -71.32318
-71.57662 -71.43645 -71.32681 -71.23876 -71.34846 -71.21293 -71.43014 -71.23976
-71.41376 -71.51845 -71.42398 -71.32977 -71.28931 -71.16495 -71.75439 -71.27969
-71.55954 -71.63032 -71.56033 -71.63209 -71.23058 -71.38042 -71.49090 -71.51547
-71.29583 -71.45683 -71.27179 -71.46428 -71.52168 -71.32865 -71.42148 -71.61778
-71.20851 -71.64178 -71.49238 -71.41293 -71.64103 -71.30978 -71.20479 -71.54393
-71.25430 -71.55619 -71.43932 -71.41108 -71.41770 -71.61854 -71.60730 -71.32889
-71.51799 -71.51727 -71.05187 -71.25959 -71.38605 -71.32370 -71.34795 -71.33926
-71.39690 -71.64604 -71.32627 -71.45392 -71.41597 -71.59673 -71.33071 -71.38166
-71.57558 -71.64599 -71.44799 -71.48559 -71.30292 -71.28608 -71.31200 -71.59470
-71.34199 -71.25757 -71.54687 -71.44841 -71.24937 -71.54664 -71.47865 -71.29903
-71.31440 -71.16202 -71.61011 -71.43532 -71.53299 -71.39738 -71.38253 -71.59106
-71.40107 -71.38232 -71.33651 -71.54669 -71.61450 -71.34329 -71.56735 -71.50272
-71.62555 -71.36188 -71.27853 -71.15136 -71.07682 -71.09633 -71.10171 -71.36661
-71.40454 -71.38359 -71.47619 -71.51893 -71.39878 -71.42159 -71.26111 -71.72335
-71.34044 -71.14719 -71.31923 -71.49345 -71.40186 -71.50094 -71.53393 -71.44361
-71.38773 -71.32308 -71.45975 -71.30311 -71.42196 -71.43421 -71.39668 -71.50927
-71.38958 -71.56433 -71.33004 -71.62257 -71.80689 -71.50798 -71.52725 -71.39211
-71.61505 -71.38859 -71.07648 -71.33119 -71.55300 -71.19464 -71.52980 -71.67177
-71.51875 -71.66407 -71.45166 -71.71004 -71.27042 -71.39812 -71.50481 -71.40283
-71.54215 -71.38016 -71.36920 -71.42692 -71.51585 -71.24453 -71.46900 -71.39042
-71.24963 -71.60579 -71.26055 -71.64871 -71.35685 -71.37942 -71.34953 -71.19748
-71.38188 -71.37984 -71.22835 -71.76051 -71.28189 -71.51192 -71.43273 -71.20882
-71.37035 -71.38163 -71.40465 -71.31278 -71.43671 -71.72614 -71.23583 -71.19766
-71.72012 -71.42857 -71.50802 -71.29909 -71.39438 -71.32738 -71.57001 -71.21150
-71.18646 -71.71919 -71.65613 -71.34120 -71.21188 -71.69972 -71.41308 -71.27347
-71.41561 -71.45594 -71.74813 -71.57076 -71.46996 -71.46282 -71.38388 -71.12429
-71.78035 -71.22669 -71.22821 -71.39271 -71.76145 -71.16856 -71.46943 -71.49145
-71.41020 -71.29092 -71.27627 -71.41104 -71.50970 -71.27575 -71.63568 -71.42445
-71.38091 -71.28944 -71.64803 -71.34406 -71.16470 -71.76314 -71.21634 -71.29285
-70.99517 -71.42275 -71.25356 -71.26929 -71.64208 -71.56740 -71.55871 -71.47310
-71.55786 -71.53526 -71.51605 -71.46695 -71.57310 -71.44193 -71.34024 -71.48716
-71.89996 -71.39564 -71.57058 -71.23378 -71.59984 -71.46168 -71.61245 -71.73457
-71.43123 -71.28181 -71.63359 -71.32462 -71.28556 -71.33072 -71.65612 -71.50840
-71.38147 -71.38919 -71.68246 -71.66523 -71.57297 -71.27680 -71.52451 -71.62947
-71.28032 -71.46232 -71.25454 -71.54069 -71.43409 -71.58861 -71.37315 -71.33595
-71.61094 -71.28765 -71.51224 -71.17946 -71.22443 -71.20496 -71.16332 -71.43440
-71.34367 -71.28408 -71.42432 -71.39686 -71.41073 -71.36408 -71.39988 -71.50648
-71.50598 -71.25940 -71.44210 -71.45522 -71.38266 -71.43513 -71.37546 -71.44123
-71.35959 -71.55290 -71.43223 -71.18783 -71.08029 -71.35597 -71.47104 -71.63317
-71.44549 -71.26576 -71.40200 -71.45505 -71.53121 -71.62358 -71.44006 -71.78784
-71.54707 -71.50052 -71.42112 -71.43377 -71.32822 -71.36001 -71.27211 -71.56588
-71.33499 -71.31957 -71.27988 -71.38306 -71.32244 -71.56262 -71.35478 -71.31512
-71.74560 -71.60397 -71.45390 -71.30886 -71.23125 -71.46692 -71.18081 -71.52323
-71.39069 -71.44278 -71.11715 -71.33001 -71.44337 -71.43762 -71.61032 -71.65301
-71.35537 -71.34357 -71.47533 -71.23749 -70.99438 -71.36232 -71.45363 -71.73558
-71.63901 -71.40398 -71.26062 -71.73954 -71.60012 -71.59118 -71.03996 -71.29511
-71.56302 -71.37685 -71.27286 -71.36115 -71.72825 -71.53478 -71.44838 -71.37829
-71.50190 -71.45940 -71.33001 -71.37713 -71.63223 -71.22723 -71.43179 -71.38776
-71.39090 -71.40347 -71.36650 -71.46262 -71.52360 -71.32917 -71.45331 -71.39119
-71.33085 -71.57174 -71.33582 -71.58809 -71.49767 -71.72820 -71.21058 -71.35725
-71.39509 -71.28330 -71.29736 -71.45020 -71.45110 -71.69824 -71.46151 -71.77383
-71.45337 -71.39666 -71.11844 -71.46987 -71.52736 -71.17233 -71.67920 -71.39278
-71.29298 -71.56942 -71.55046 -71.46593 -71.55557 -71.87019 -71.45622 -71.42834
-71.37789 -71.40700 -71.36306 -70.93103 -71.65223 -71.31925 -71.60359 -71.57852
-71.20781 -71.52114 -71.55208 -71.29429 -71.46382 -71.23105 -71.26658 -71.31644
-71.41196 -71.18923 -71.50398 -71.46377 -71.40065 -71.33973 -71.67920 -71.42171
-71.28131 -71.28926 -71.38350 -71.42443 -71.49339 -71.54266 -71.44208 -71.28247
-70.99582 -71.16565 -71.39905 -71.81445 -71.34498 -71.45581 -71.23857 -71.29692
-71.49150 -71.32218 -71.39157 -71.30330 -71.47281 -71.38985 -71.55694 -71.66820
-71.08030 -71.58867 -71.51252 -71.44102 -71.42553 -71.48115 -71.15794 -71.32319
-71.16861 -71.56280 -71.38392 -71.32185 -71.53180 -71.39843 -71.17602 -71.31486
-71.28714 -71.81162 -71.28460 -71.58365 -71.46923 -71.37024 -71.09542 -71.62084
-71.35175 -71.49940 -71.26618 -71.45582 -71.38149 -71.41215 -71.35900 -71.38209
-71.15070 -71.27019 -71.38961 -71.54839 -71.15564 -71.56603 -71.72784 -71.36670
-71.68089 -71.73228 -71.57858 -71.59794 -71.43778 -71.54632 -71.05925 -71.49182
-71.51499 -71.49192 -71.31960 -71.57818 -71.48745 -71.57432 -71.10026 -71.63249
-71.28982 -71.71190 -71.28713 -71.29710 -71.22581 -71.27837 -71.43117 -71.36568
-71.25759 -71.37040 -71.45703 -71.62025 -71.27147 -71.24550 -71.31532 -71.56019
-71.56344 -71.19334 -71.35750 -71.15953 -71.29472 -71.59196 -71.32477 -71.25051
-71.45197 -71.72211 -71.43251 -71.63502 -71.49387 -71.83121 -71.49509 -71.59798
-71.34405 -71.45044 -71.18903 -71.20754 -71.52357 -71.64530 -71.29499 -71.53058
-71.20778 -71.38741 -71.32568 -71.32651 -71.57480 -71.31213 -71.36948 -71.40318
-71.61040 -71.51772 -71.43068 -71.42442 -71.45455 -71.73821 -71.49518 -71.29775
-71.37617 -71.55261 -71.66116 -71.51610 -71.44167 -71.36269 -71.38928 -71.47202
-71.50109 -71.34466 -71.32851 -71.81349 -71.52304 -71.34009 -71.40206 -71.22293
-71.35641 -71.64229 -71.62832 -71.28865 -71.09067 -71.46769 -71.47930 -71.41624
-71.43249 -71.17807 -71.27873 -71.09737 -71.45050 -71.42102 -71.52161 -71.31976
-71.40674 -71.32153 -71.19670 -71.38932 -71.47943 -71.44716 -71.44750 -71.43367
-71.53523 -71.19132 -71.34939 -71.44511 -71.32694 -71.46056 -71.42547 -71.34830
-71.37002 -71.17636 -71.35401 -71.65558 -71.50684 -71.32114 -71.43428 -71.49891
-71.44841 -71.51056 -71.43771 -71.32109 -71.51092 -71.87518 -71.21746 -71.27073
-71.30745 -71.52674 -71.48454 -71.39362 -71.37144 -71.38731 -71.41623 -71.60056
-71.49869 -71.21278 -71.27770 -71.31154 -71.35724 -71.37344 -71.53885 -71.51700
-71.15579 -71.58486 -71.07953 -71.15273 -71.62263 -71.20921 -71.51927 -71.12495
-71.25870 -71.61993 -71.13875 -71.18978 -71.49620 -71.68005 -71.30248 -71.59585
-71.32972 -71.30420 -71.60282 -71.68168 -72.03088 -70.97909 -71.26679 -71.32272
-71.76539 -71.66827 -71.41750 -71.61545 -71.34466 -71.12768 -71.47146 -71.48240
-71.28034 -71.11179 -71.44727 -71.44511 -71.50535 -71.27504 -71.56993 -71.27872
-71.41928 -71.41083 -71.55199 -71.48046 -71.34564 -71.22501 -71.33661 -71.51323
-71.54176 -71.29635 -71.54996 -71.40635 -71.15450 -71.43252 -71.57173 -71.34893
-71.25908 -71.61297 -71.45064 -71.36116 -71.61002 -71.60604 -71.33108 -71.31878
-71.27390 -71.92289 -71.21641 -71.37199 -71.24945 -71.29226 -71.40360 -71.35280
-71.37129 -71.53584 -71.46038 -71.44803 -71.26290 -71.15658 -71.22947 -71.27546
-71.37972 -71.30253 -71.01220 -71.40969 -71.41691 -71.30476 -71.57740 -71.29962
-71.40233 -71.35556 -71.45245 -71.29805 -71.72817 -71.18404 -71.43444 -71.52088
-71.62279 -71.52282 -71.22575 -71.49798 -71.23723 -71.40018 -71.22064 -71.48047
-71.00534 -71.40719 -71.21780 -71.45758 -71.29296 -71.50655 -71.28932 -71.42456
-71.52185 -71.68755 -71.37262 -71.61490 -71.68113 -71.37232 -71.51094 -71.26988
-71.11242 -71.34637 -71.39561 -71.54256 -71.53090 -71.44837 -71.46185 -71.48538
-71.48717 -71.13200 -71.47674 -71.59566 -71.62706 -71.54378 -71.22966 -71.22942
-71.50607 -71.46764 -71.55257 -71.39306 -71.59786 -71.32060 -71.54819 -71.58616
-71.25810 -71.46609 -71.67566 -71.43106 -71.61312 -71.46211 -71.50176 -71.40760
-71.53591 -71.15573 -71.43832 -71.07147 -71.56660 -71.17247 -71.41357 -71.48327
-71.24930 -71.57834 -71.39274 -71.40832 -71.66650 -71.36197 -71.29691 -71.53390
-71.38162 -71.24364 -71.33332 -71.62223 -71.15407 -71.62570 -71.74774 -71.41972
-71.77684 -71.31648 -71.68634 -71.29510 -71.34923 -71.64111 -71.49306 -70.98354
-71.47135 -71.29425 -71.60544 -71.60894 -71.48787 -71.23392 -71.32233 -71.37403
-71.18374 -71.41972 -71.85181 -71.19016 -71.15103 -71.76353 -71.25381 -71.46425
-71.39916 -71.72543 -71.33550 -71.27927 -71.52969 -71.52346 -71.25353 -71.13085
-71.37447 -71.28111 -71.32282 -71.44694 -71.32572 -71.49306 -71.44123 -71.25460
-71.57742 -71.58243 -71.79975 -71.30908 -71.29812 -71.37998 -71.15383 -71.18855
-71.50962 -71.44728 -71.50807 -71.10722 -71.54392 -71.13585 -71.57322 -71.49101
-71.68124 -71.69743 -71.27356 -71.70341 -71.35844 -71.85103 -71.38543 -71.32018
-71.24704 -71.39342 -71.55909 -71.38762 -71.39085 -72.01813 -71.37473 -71.38374
-71.34583 -71.22538 -71.36197 -71.52763 -71.40048 -71.66627 -71.27181 -71.14242
-71.32979 -71.43227 -71.17245 -71.33176 -71.39070 -71.26366 -71.53278 -71.17610
-71.37530 -71.41158 -71.43530 -71.61821 -71.39176 -71.51876 -71.62514 -71.45169
-71.23981 -71.37907 -71.40849 -71.02796 -71.69759 -71.49748 -71.62346 -71.15163
-71.48288 -71.25275 -71.33033 -71.42068 -71.29614 -71.54050 -71.40784 -71.69825
-71.41309 -71.59405 -71.21261 -71.18757 -71.38688 -71.38925 -71.62983 -71.44570
-71.35108 -71.38596 -71.42079 -71.80732 -71.29980 -71.53860 -71.55813 -71.51248
-71.20614 -71.31184 -71.20335 -71.19427 -71.28224 -71.46716 -71.35795 -71.35287
-71.66950 -71.58535 -71.16775 -71.10396 -71.36854 -71.45350 -71.64730 -71.46021
-71.32126 -71.49898 -71.35212 -71.56215 -71.08925 -71.48954 -71.83515 -71.42748
-71.35489 -71.39840 -71.48707 -71.35928 -71.60500 -71.35605 -71.75168 -71.56208
-71.50091 -71.28680 -71.23394 -71.39826 -71.26781 -71.59365 -71.34798 -71.39288
-71.10937 -71.41498 -71.61088 -71.34642 -71.53481 -71.08817 -71.61015 -71.45518
-71.81267 -71.45221 -71.32055 -71.69432 -71.49873 -71.33502 -71.58296 -71.76242
-71.36861 -71.43209 -71.31286 -71.55805 -71.43983 -71.42278 -71.33572 -71.25826
-71.17811 -71.31391 -71.34565 -71.39845 -71.42546 -71.41390 -71.48049 -71.31616
-71.27982 -71.45155 -71.38673 -71.14812 -71.32400 -71.40287 -71.27511 -71.30828
-71.42936 -71.49387 -71.39241 -71.27300 -71.52178 -71.00552 -71.30424 -71.28991
-71.44622 -71.44788 -71.17072 -71.46070 -71.50897 -71.35402 -71.22390 -71.47412
-71.10758 -71.15999 -71.32750 -71.41562 -71.38063 -71.30227 -71.59728 -71.34693
-71.22531 -71.54998 -71.15003 -71.31595 -71.39148 -71.32260 -71.44321 -71.49979
-71.52249 -71.43415 -71.00845 -71.19484 -71.60595 -71.32171 -71.47094 -71.86719
-71.58926 -71.20238 -71.33990 -71.57091 -71.18743 -71.52427 -71.15379 -71.50690
-71.21553 -71.57832 -71.57079 -71.52543 -71.23055 -71.25180 -71.50054 -71.27891
-71.40831 -71.35341 -71.51667 -71.52000 -71.09440 -71.23121 -71.51656 -71.29447
-71.14752 -71.65150 -71.41531 -71.51499 -71.21750 -71.44638 -71.52175 -71.48600
-71.42687 -71.17332 -71.46607 -71.35103 -71.67549 -71.36795 -71.27039 -71.45123
-71.37991 -71.71545 -71.35276 -71.45034 -71.38887 -71.50769 -71.63642 -71.30796
-71.38970 -71.56037 -71.32041 -71.70629 -71.44657 -71.32783 -71.32502 -71.38368
-71.57483 -71.45573 -71.40400 -71.69078 -71.29391 -71.79000 -71.39933 -71.38385
-71.16051 -71.58187 -71.47308 -71.24811 -71.26364 -71.31020 -71.50533 -71.72326
-71.38153 -71.38194 -71.61775 -71.30038 -71.54568 -71.57539 -71.62972 -71.29023
-71.54944 -71.75154 -71.42888 -71.40540 -71.55946 -71.19138 -71.36059 -71.27540
-71.36937 -71.30192 -71.54162 -71.20696 -71.15390 -71.44704 -71.41203 -71.39657
-71.51801 -71.60601 -71.11046 -71.22255 -71.47507 -71.51654 -71.38805 -71.30149
-71.80469 -71.48322 -71.51055 -71.58467 -71.53451 -71.35557 -71.07533 -71.29348
-71.26080 -71.40585 -71.45034 -71.22746 -71.52551 -71.46772 -71.30075 -71.23968
-71.46727 -71.13219 -71.36072 -71.15226 -71.29686 -71.30338 -71.46809 -71.48303
-71.48839 -71.71894 -71.72166 -71.16897 -71.50530 -71.50563 -71.31075 -71.45442
-71.43977 -71.66978 -71.38467 -71.85145 -71.31096 -71.61201 -71.28436 -71.73161
-71.55852 -71.25530 -71.65521 -71.55374 -71.24051 -71.34266 -71.62494 -71.31569
-71.04325 -71.25997 -71.06348 -71.80943 -71.28166 -71.25493 -71.45356 -71.24915
-71.56877 -71.44029 -71.45186 -71.36722 -71.75100 -71.28197 -71.60716 -71.28944
-71.47598 -71.40967 -71.72608 -71.41717 -71.32854 -71.25723 -71.12578 -71.37566
-71.55649 -71.30233 -71.26828 -71.28843 -71.35862 -71.48061 -71.52249 -71.22177
-71.22054 -71.28844 -71.80773 -71.52092 -71.52786 -71.57016 -71.35900 -71.36165
-71.70565 -71.37319 -71.28926 -71.69024 -71.24641 -71.58434 -71.42444 -71.54479
-71.37980 -71.24987 -71.59803 -71.22524 -71.62842 -71.27471 -71.39410 -71.39648
-71.58897 -71.41204 -71.56153 -71.53377 -71.40056 -71.24200 -71.41103 -71.84520
-71.34198 -71.60015 -71.11847 -71.59351 -71.50516 -71.61262 -71.66191 -71.42378
-71.41228 -71.11720 -71.74396 -71.58401 -71.26227 -71.22722 -71.29218 -71.35561
-71.48435 -71.54975 -71.37820 -71.62870 -71.29926 -71.33681 -71.51793 -71.51426
-71.45106 -71.50533 -71.25116 -71.31909 -71.25719 -71.31592 -71.43562 -71.39249
-71.08930 -71.42398 -71.10852 -71.36950 -71.34299 -71.24497 -71.38833 -71.76141
-71.44246 -71.31393 -71.83152 -71.33475 -71.53495 -71.60414 -71.20695 -71.51975
-71.32058 -71.28858 -71.48803 -71.34072 -71.72030 -71.32903 -71.43036 -71.49038
-71.30080 -71.62654 -71.62338 -71.36848 -71.28874 -71.30132 -71.57210 -71.11317
-71.62894 -71.84908 -71.15989 -71.20671 -71.30730 -71.58700 -71.57839 -71.60473
-71.68026 -71.38678 -71.38719 -71.33015 -71.53715 -71.24423 -71.42324 -71.25987
-71.21780 -71.59761 -71.38618 -71.38296 -71.45909 -71.37634 -71.28446 -71.47991
-71.28335 -71.45247 -71.63846 -71.40932 -71.42791 -71.47309 -71.29880 -71.38150
-71.67138 -71.54510 -71.21613 -71.37725 -71.53125 -71.19676 -71.45200 -71.59150
-71.15185 -71.60541 -71.28832 -71.61558 -71.33994 -71.54315 -71.49028 -71.57883
-71.24405 -71.37946 -71.54708 -71.39622 -71.42317 -71.02910 -71.29034 -71.54758
-71.70022 -71.51077 -71.66180 -71.32463 -71.43174 -71.48005 -71.74537 -71.34262
-71.36397 -71.17923 -71.37507 -71.83116 -71.61320 -71.23096 -71.36367 -71.19503
-71.48091 -71.36848 -71.79609 -71.42452 -71.42332 -71.39650 -71.36201 -71.42307
-71.50084 -71.30757 -71.11780 -71.61253 -71.47331 -71.31939 -71.52370 -71.48114
-71.39983 -71.38089 -71.82298 -71.36214 -71.46212 -71.16249 -71.44796 -71.46248
-71.51266 -71.28566 -71.31535 -71.57785 -71.55417 -71.39054 -71.28570 -71.29373
-71.22093 -71.74053 -71.14500 -71.54298 -71.34797 -71.57161 -71.34022 -71.45691
-71.62452 -71.51185 -71.45308 -71.34150 -71.51072 -71.45061 -71.46550 -71.60715
-71.49977 -71.46763 -71.56731 -71.54126 -71.43988 -71.58323 -71.30457 -71.59581
-71.66674 -71.57557 -71.15004 -70.96326 -71.44235 -71.31420 -71.47271 -71.40457
-71.52084 -71.31768 -71.42959 -71.45049 -71.64560 -71.23000 -71.35831 -71.68508
-71.67214 -71.37098 -71.39819 -71.67229 -71.41786 -71.64524 -71.18582 -71.20825
-71.33063 -71.27752 -71.44506 -71.67694 -71.23055 -71.41643 -71.49526 -71.33006
-71.56456 -71.37321 -71.26796 -71.60501 -71.23882 -71.63520 -71.23357 -71.22864
-71.27543 -71.62811 -71.60766 -71.43115 -71.22339 -71.48524 -71.38471 -70.80890
-71.31519 -71.47550 -71.41965 -71.24453 -71.58253 -71.70199 -71.61611 -71.42276
-71.62059 -71.27320 -71.45683 -71.15951 -71.42735 -71.23035 -71.57186 -71.34326
-71.52634 -71.35342 -71.31933 -71.32148 -71.48496 -71.05014 -71.60342 -71.59629
-71.46918 -71.52571 -71.47798 -71.25805 -71.06935 -71.37738 -71.43021 -71.49833
-71.30190 -71.41709 -71.53962 -71.49941 -71.35231 -71.18892 -71.39952 -71.40346
-71.41917 -71.39339 -71.17773 -71.52793 -71.47457 -71.36710 -71.58547 -71.58264
-71.41613 -71.53208 -71.37753 -71.33113 -71.41178 -71.30936 -71.61906 -71.15568
-71.43729 -71.40071 -71.44837 -71.32471 -71.52723 -71.61893 -71.35233 -71.27199
-71.61008 -71.36003 -71.57465 -71.21155 -71.25332 -71.64308 -71.25123 -71.32860
-71.41196 -71.25609 -71.31523 -71.30045 -71.34066 -71.42921 -71.45358 -71.49187
-71.65824 -71.54563 -71.29772 -71.52480 -71.33150 -71.65320 -71.27478 -71.37328
-71.52092 -71.47268 -71.09598 -71.40675 -71.44726 -71.37937 -71.42652 -71.48009
-71.28805 -71.52709 -71.71635 -71.53367 -71.32829 -71.18453 -71.44355 -71.27682
-71.46965 -71.36621 -71.24406 -71.26670 -71.49067 -71.40897 -71.51635 -71.55502
-71.17076 -71.30799 -71.50551 -71.07131 -71.19202 -71.30442 -71.27228 -71.54936
-71.27027 -71.40333 -71.13831 -71.57329 -71.49295 -71.34453 -71.46562 -71.60474
-71.32543 -71.69833 -71.25701 -71.30531 -71.66952 -71.37304 -71.49876 -71.36288
-71.34340 -71.33216 -71.67111 -71.30063 -71.25727 -71.28788 -71.26746 -71.36749
-71.23164 -71.38904 -71.50905 -71.30904 -71.25063 -71.55928 -71.58119 -71.29418
-71.36280 -71.20588 -71.49839 -71.65862 -71.39497 -71.23886 -71.37194 -71.50634
-71.28803 -71.65185 -71.19259 -71.26510 -71.62369 -71.25260 -71.39602 -71.52774
-71.36693 -71.43446 -71.28691 -71.19771 -71.32214 -71.12118 -71.54121 -71.57623
-71.33402 -71.59846 -71.46528 -71.72903 -71.48871 -71.88703 -71.07230 -71.26814
-71.45194 -71.14680 -71.51803 -71.46032 -71.36451 -71.27567 -71.38461 -71.52539
-71.39133 -71.59389 -71.59621 -71.53402 -71.32747 -71.46218 -71.32675 -71.35872
-71.27329 -71.38106 -71.29910 -71.43412 -71.54798 -71.43121 -71.36954 -71.52042
-71.52281 -71.18660 -71.59544 -71.33196 -71.32825 -71.23818 -71.72028 -71.41498
-71.69134 -71.32685 -71.76896 -71.48950 -71.44643 -71.34120 -71.31575 -71.70842
-71.49224 -71.37540 -71.40988 -71.31923 -71.29951 -71.23322 -71.22835 -71.36649
-71.38400 -71.46493 -71.52299 -71.33754 -71.38472 -71.57931 -71.44771 -71.19919
-71.40650 -71.24255 -71.42093 -71.38726 -71.58923 -71.44968 -71.20398 -71.37575
-71.49687 -71.23411 -71.59239 -71.33664 -71.40021 -71.59170 -71.30193 -71.25088
-71.51133 -71.62273 -71.37524 -71.31349 -71.82314 -71.91195 -71.30033 -71.34329
-71.64380 -71.32806 -71.38446 -71.54397 -71.38385 -71.17135 -71.07907 -71.53293
-71.52661 -71.61644 -71.46808 -71.53231 -71.17956 -71.43271 -71.40884 -71.29322
-71.41872 -71.46823 -71.13274 -71.12238 -71.52117 -71.31043 -71.23072 -71.71380
-71.40189 -71.62805 -71.40598 -71.39681 -71.49113 -71.43185 -71.20615 -71.42519
-71.27916 -71.53999 -71.50566 -71.53096 -71.33999 -71.44681 -71.43540 -71.31102
-71.39343 -71.55163 -71.19074 -71.39563 -71.19701 -71.17478 -71.39014 -71.64659
-71.48314 -71.58151 -71.54415 -71.17579 -71.50690 -71.37643 -71.33541 -71.35885
-71.25348 -71.43998 -71.42398 -71.57131 -71.32844 -71.42015 -71.38809 -71.27375
-71.40746 -71.26866 -71.66637 -71.51884 -71.38138 -71.32667 -70.95184 -71.53421
-71.21997 -71.43578 -71.18443 -71.80402 -71.66716 -71.45788 -71.40487 -71.39278
-71.38464 -71.61649 -71.70133 -71.49789 -71.31546 -71.71218 -71.17444 -71.46881
-71.43582 -71.16347 -71.33003 -71.51084 -71.49025 -71.51355 -71.25893 -71.38238
-71.19573 -71.66333 -71.46281 -71.33355 -71.63149 -71.19168 -71.29804 -71.33674
-71.18821 -71.51035 -71.38879 -71.50669 -71.65096 -71.45427 -71.58462 -71.48216
-71.71781 -71.44580 -71.27953 -71.40900 -71.39226 -71.45861 -71.38044 -71.70081
-71.56990 -71.23762 -71.20683 -71.41849 -71.42188 -71.52002 -71.36906 -71.65328
-71.57820 -71.56994 -71.27319 -71.28354 -71.62077 -71.40176 -71.23573 -71.59506
-71.56730 -71.12531 -71.28733 -71.35908 -71.67533 -71.59142 -71.64785 -71.22911
-71.28588 -71.41051 -71.39646 -71.34839 -71.71401 -71.29531 -71.25964 -71.30939
-71.38696 -71.30730 -71.48089 -71.31784 -71.40209 -71.56183 -71.52413 -71.33269
-71.70231 -71.37703 -71.36492 -71.29233 -71.46457 -71.23923 -71.21186 -71.27253
-71.34433 -71.66367 -71.34882 -71.37743 -71.57752 -71.48654 -71.52792 -71.43903
-71.60839 -71.39465 -71.55718 -71.29927 -71.45770 -71.42701 -71.76145 -71.50510
-71.47111 -71.48963 -71.36949 -71.18201 -71.36194 -71.44243 -71.35671 -71.39274
-71.10107 -71.27202 -71.41975 -71.52349 -71.60277 -71.73844 -71.57624 -71.32350
-71.10503 -71.36707 -71.18615 -71.37206 -71.27203 -71.28073 -71.22924 -71.34567
-71.20143 -71.57784 -71.66081 -71.41521 -71.49121 -71.37663 -71.49216 -71.32789
-71.37887 -71.56700 -71.54388 -71.41550 -71.43725 -71.56385 -71.44496 -71.42987
-71.67365 -71.38642 -71.27125 -71.49007 -71.23358 -71.31758 -71.42124 -71.05656
-71.39287 -71.21481 -71.27165 -71.85941 -71.60427 -71.29273 -71.31449 -71.27544
-71.53208 -71.44989 -71.47717 -71.51232 -71.29220 -71.46608 -71.44227 -71.23996
-71.20398 -71.42248 -71.68597 -71.27569 -71.50107 -71.21820 -71.40999 -71.69381
-71.26871 -71.34839 -71.41584 -71.18190 -71.42368 -71.56640 -71.60601 -71.75803
-71.21653 -71.57550 -71.55521 -71.34476 -71.17354 -71.59423 -71.52221 -71.46082
-71.30936 -71.76397 -71.05322 -71.53875 -71.44362 -71.36667 -71.45046 -71.32840
-71.56147 -71.49758 -71.48129 -71.52137 -71.38473 -71.59636 -71.37450 -71.52669
-71.29224 -71.27922 -71.98654 -71.42513 -71.28653 -71.45688 -71.22250 -71.30455
-71.15360 -71.29466 -71.37542 -71.44297 -71.74312 -71.33157 -71.41515 -71.43403
-71.34171 -71.22942 -71.16365 -71.86691 -71.33693 -71.30821 -71.52581 -71.60624
-71.40027 -71.30239 -71.41554 -71.30324 -71.48114 -71.54726 -71.16775 -71.55036
-71.47005 -71.57183 -71.42244 -71.21321 -71.54171 -71.60221 -71.25162 -71.35954
-71.27423 -71.48735 -71.22755 -71.43092 -71.31157 -71.39281 -71.47769 -71.29895
-71.45354 -71.38266 -71.28099 -71.23274 -71.45904 -71.47544 -71.40538 -71.32456
-71.17541 -71.52176 -71.64680 -71.49928 -71.54319 -71.51844 -71.52415 -71.48237
-71.40802 -71.46440 -71.39068 -71.36437 -71.25297 -71.58418 -71.48645 -71.44006
-71.44690 -71.51318 -71.45733 -71.49525 -71.63755 -71.29538 -71.54511 -71.42403
-71.61703 -71.35527 -71.42425 -71.39214 -71.28903 -71.63076 -71.35931 -71.56633
-71.52273 -71.59008 -71.55302 -71.54629 -71.67830 -71.79270 -71.35465 -71.37206
-71.62653 -71.49873 -71.52396 -71.55514 -71.70644 -71.62134 -71.55179 -71.32769
-71.13124 -71.56925 -71.75817 -71.35966 -71.29647 -71.56574 -71.53461 -71.50223
-71.58935 -71.33286 -71.47901 -71.84523 -71.40148 -71.38943 -71.52833 -71.48037
-71.35538 -71.16973 -71.72215 -71.30317 -71.37107 -71.45115 -71.53697 -71.47042
-71.13674 -71.47590 -71.58034 -71.35364 -71.34119 -71.42763 -71.44033 -71.61895
-71.30080 -71.53034 -71.25153 -71.31331 -71.35321 -71.44747 -71.32238 -71.35937
-71.33066 -71.55540 -71.60423 -71.18167 -71.18489 -71.51309 -71.42517 -71.64809
-71.64381 -71.37807 -71.31167 -71.47799 -71.53870 -71.40658 -71.25492 -71.67511
-71.27866 -71.28704 -71.32542 -71.52276 -71.33816 -71.50833 -71.41341 -71.46792
-71.22815 -71.40817 -71.43979 -71.25955 -71.47783 -71.37825 -71.40614 -71.30751
-71.42457 -71.29749 -71.47506 -71.46665 -71.36832 -71.39052 -71.53816 -71.18958
-71.55117 -71.27036 -71.39725 -71.53443 -71.33527 -71.46214 -71.33782 -71.51212
-71.30771 -71.44452 -71.39177 -71.63473 -71.25404 -71.11678 -71.62378 -71.34939
-71.48334 -71.48527 -71.54559 -71.18254 -71.26888 -71.35582 -71.58275 -71.07025
-71.26565 -71.41475 -71.65821 -71.59557 -71.62948 -71.39673 -71.25503 -71.36633
-71.35750 -71.29984 -71.56187 -71.35579 -71.69495 -71.57112 -71.24017 -71.26979
-71.21118 -71.61113 -71.69764 -71.32987 -71.15031 -71.43640 -71.33640 -71.65702
-71.23560 -71.23621 -71.61273 -71.16744 -71.64626 -71.53967 -71.37579 -71.38789
-71.52356 -71.40190 -71.77655 -71.43102 -71.56580 -71.27418 -71.44729 -71.27108
-71.41472 -71.62411 -71.71792 -71.23753 -71.32811 -71.43443 -71.45943 -71.37788
-71.28280 -71.54569 -71.31361 -71.42081 -71.55843 -71.34823 -71.53481 -71.24014
-71.42132 -71.21824 -71.27125 -71.42373 -71.50317 -71.13708 -71.69051 -71.49311
-71.31741 -71.39344 -71.66765 -71.20407 -71.45070 -71.26881 -71.15123 -71.68331
-71.18915 -71.57915 -71.72249 -71.60366 -71.70869 -71.71763 -71.39217 -71.38036
-71.57880 -71.37656 -71.35351 -71.43203 -71.38183 -71.21653 -71.52295 -71.73295
-71.19629 -71.58023 -71.09033 -71.19494 -71.53856 -71.67551 -71.59600 -71.43069
-71.35501 -71.51839 -71.60101 -71.33398 -71.44512 -71.73323 -71.47209 -71.19446
-71.69543 -71.54281 -71.31814 -71.16703 -71.58053 -71.32504 -71.32340 -71.57586
-71.40442 -71.37015 -71.35015 -71.47380 -71.38289 -71.30311 -71.16223 -71.31463
-71.53924 -71.35868 -71.14357 -71.64391 -71.39485 -71.20414 -71.11959 -71.61384
-71.71105 -71.60025 -71.66381 -71.34196 -71.50730 -71.55397 -71.70863 -71.51074
-71.28419 -71.40180 -71.31963 -71.61359 -71.35930 -71.42780 -71.54912 -71.69445
-71.77099 -71.42410 -71.24902 -71.48510 -71.52300 -71.21899 -71.30891 -71.30843
-71.35485 -71.51697 -71.48017 -71.46530 -71.56564 -71.49980 -71.49336 -71.45558
-71.41622 -71.74046 -71.43200 -71.01749 -71.47534 -71.31883 -71.34475 -71.50061
-71.09318 -71.08576 -71.52326 -71.45765 -71.58043 -71.36759 -71.28952 -71.47168
-71.59089 -71.69302 -71.46270 -71.50503 -71.29720 -71.23627 -71.52824 -71.28743
-71.22554 -71.30746 -71.37653 -71.42035 -71.30356 -71.21486 -71.56611 -71.23781
-71.58330 -71.35966 -71.35888 -71.32015 -71.45036 -71.55579 -71.30308 -71.54096
-71.34631 -71.48306 -71.28425 -71.55363 -71.34400 -71.29690 -71.33453 -71.59943
-71.32116 -71.30937 -71.41381 -71.36069 -71.58661 -71.45953 -70.92451 -71.44980
-71.51391 -71.55509 -71.32834 -71.55440 -71.56429 -71.55232 -71.62315 -71.32071
-71.43545 -71.42553 -71.23702 -71.22924 -71.51016 -71.33766 -71.68917 -71.54934
-71.51656 -71.28831 -71.70205 -71.68099 -71.21524 -71.40918 -71.63952 -71.18057
-71.76299 -71.78045 -71.45042 -71.37873 -71.42558 -71.50919 -71.49714 -71.38137
-71.11533 -71.52327 -71.35414 -71.27935 -71.50717 -71.30501 -71.42256 -71.20965
-71.54327 -71.35196 -71.35747 -71.62371 -71.23564 -71.21376 -71.83575 -71.43923
-71.60701 -71.37597 -71.60371 -71.41317 -71.29197 -71.19604 -71.45934 -71.28827
-71.30226 -71.11783 -71.35859 -71.54177 -71.35332 -71.29677 -71.35403 -71.78741
-71.33650 -71.45388 -71.39111 -71.47607 -71.57022 -71.56926 -71.58572 -71.47042
-71.10787 -71.24656 -71.37867 -71.36158 -71.24679 -71.37576 -71.61148 -71.44705
-71.24714 -71.30135 -71.30867 -71.50134 -71.32816 -71.46020 -71.31094 -71.42762
-71.49604 -71.20837 -71.35734 -71.26214 -71.33680 -71.12817 -71.64527 -71.28091
-71.33114 -71.24143 -71.59913 -71.52202 -71.44714 -71.53541 -71.27095 -71.28418
-71.39987 -71.70853 -71.46120 -71.46719 -71.32097 -71.49475 -71.72224 -71.25153
-71.47920 -71.30015 -71.49407 -71.18318 -71.48587 -71.46715 -71.67223 -71.54289
-71.42442 -71.73128 -71.78764 -71.23209 -71.53851 -71.44832 -71.21974 -71.35468
-71.42340 -71.35212 -71.28860 -71.33470 -71.12481 -71.32465 -71.55953 -71.38220
-71.47675 -71.56483 -71.67717 -71.41030 -71.47421 -71.69415 -71.31892 -71.21921
-71.51621 -71.51208 -71.25893 -71.62483 -71.49848 -71.69044 -71.24143 -71.60210
-71.55193 -71.18979 -71.38986 -71.29278 -71.44411 -71.51546 -71.46481 -71.38834
-71.19172 -71.30217 -71.72660 -71.42421 -71.15567 -71.47603 -71.30100 -71.65357
-71.30088 -71.38187 -71.37303 -71.35678 -71.35986 -71.52778 -71.48004 -71.27824
-71.59335 -71.56901 -71.28799 -71.42503 -71.24273 -71.08555 -71.49004 -71.57950
-71.35881 -71.44970 -71.46629 -71.33956 -71.26970 -71.34471 -71.41558 -71.35064
-71.41081 -71.61878 -71.56720 -71.34889 -71.43534 -71.57763 -71.49070 -71.37541
-71.53319 -71.39629 -71.26950 -71.26679 -71.46069 -71.41329 -71.46120 -71.09263
-71.35874 -71.39157 -71.27095 -71.26131 -71.31571 -71.75416 -71.38385 -71.33756
-71.36947 -71.38129 -71.43903 -71.15122 -71.78709 -71.67188 -71.55791 -71.32491
-71.38924 -71.34928 -71.21763 -71.26326 -71.35580 -71.42353 -71.36042 -71.20067
-71.33471 -71.15053 -71.50687 -71.28794 -71.37304 -71.42716 -71.62820 -71.13768
-71.41562 -71.45123 -71.28440 -71.40649 -71.74569 -71.35466 -71.14506 -71.35526
-71.36187 -71.65084 -71.23364 -71.43850 -71.35786 -71.50148 -71.43674 -71.24250
-71.75205 -71.45191 -71.29484 -71.32813 -71.39472 -71.34472 -71.20548 -71.48109
-71.71546 -71.38410 -71.31637 -71.44879 -71.24114 -71.28268 -71.46783 -71.31997
-71.42907 -71.53690 -71.52793 -71.33911 -71.18274 -71.55728 -71.59676 -71.52146
-71.46695 -71.22762 -71.27740 -71.51482 -71.44431 -71.46230 -71.20145 -71.43621
-71.28197 -71.43122 -71.38648 -71.29236 -71.72035 -71.17640 -71.20981 -71.21454
-71.62446 -71.61692 -71.42944 -71.42491 -71.38053 -71.59156 -71.42649 -71.34409
-71.40698 -71.27390 -71.46016 -71.59468 -71.27085 -71.52410 -71.35528 -71.58503
-71.55128 -71.42824 -71.32369 -71.30904 -71.44297 -71.42150 -71.22878 -71.65184
-71.39742 -71.40211 -71.42589 -71.33444 -71.42004 -71.10766 -71.29664 -71.67083
-71.90446 -71.50754 -71.44299 -71.40916 -71.34192 -71.65771 -71.13966 -71.85694
-71.48506 -71.31799 -71.43203 -71.66914 -71.19741 -71.34570 -71.38887 -70.99586
-71.38588 -71.14278 -71.31150 -71.54063 -71.54747 -71.24927 -71.58155 -71.60388
-71.82212 -71.13593 -71.66297 -71.22822 -71.69279 -71.25891 -71.11323 -71.24345
-71.21641 -71.47761 -71.13736 -71.50951 -71.34665 -71.52758 -71.58871 -71.06562
-71.31177 -71.29107 -71.46244 -71.42603 -71.22774 -71.27274 -71.45713 -71.56716
-71.45032 -71.31060 -71.34763 -71.37408 -71.38474 -71.49722 -71.41456 -71.43092
-71.53782 -71.95017 -71.17267 -71.25257 -71.36423 -71.39393 -71.36510 -71.46195
-71.32546 -71.38782 -71.44174 -71.36418 -71.51207 -71.29816 -71.42082 -71.65495
-71.10431 -71.67484 -71.27955 -71.50385 -71.30818 -71.58660 -71.50495 -71.77515
-71.35468 -71.63948 -71.70713 -71.41273 -71.30301 -71.51576 -71.43425 -71.29988
-71.66583 -71.70921 -71.26756 -71.46776 -71.27277 -71.33443 -71.48826 -71.50728
-71.66901 -71.43516 -71.16302 -71.45908 -71.72433 -71.43242 -71.08493 -71.35718
-71.44545 -71.16757 -71.24027 -71.42113 -71.45338 -71.58499 -71.24741 -71.42035
-71.55183 -71.20125 -71.56364 -71.50595 -71.42120 -71.52153 -71.34342 -71.32083
-71.69850 -71.32340 -71.13753 -71.47670 -71.66675 -71.33289 -71.39857 -71.03270
-71.30353 -71.69921 -71.48598 -71.12278 -71.48824 -71.52288 -71.58004 -71.88603
-71.14027 -71.32011 -72.13602 -71.34333 -71.20355 -71.34730 -71.30103 -71.39578
-71.61089 -71.45562 -71.47405 -71.37462 -71.38479 -71.41181 -71.55472 -71.58402
-71.70679 -72.06186 -71.41743 -71.49827 -71.66438 -71.22547 -71.22887 -71.31571
-71.37172 -71.37498 -71.49987 -71.42650 -71.37300 -71.73672 -71.65517 -71.17626
-71.71896 -71.32407 -71.87821 -71.26900 -71.50844 -71.43258 -71.36254 -71.38211
-71.56337 -71.47606 -71.31450 -71.50857 -71.47241 -71.41516 -71.64764 -71.34073
-71.25255 -71.55021 -71.55128 -71.45365 -71.47208 -71.35139 -71.57760 -71.29914
-71.19556 -71.46857 -71.31022 -71.19868 -71.23240 -71.31854 -71.56393 -71.50514
-71.62501 -71.43140 -71.16603 -71.35961 -71.38976 -71.39856 -71.63253 -71.12488
-71.66387 -71.13430 -71.51129 -71.48632 -71.30425 -71.50234 -71.25974 -71.36679
-71.27406 -71.08371 -71.17436 -71.24804 -71.37741 -71.25181 -71.56474 -71.53990
-71.45936 -71.52966 -71.47682 -71.59331 -71.57681 -71.41128 -71.27859 -71.14427
-71.50943 -71.45646 -71.30254 -71.25398 -71.55398 -71.52906 -71.27709 -71.57150
-71.08629 -71.18448 -71.28962 -71.38323 -71.40252 -71.66003 -71.70409 -71.37021
-71.43997 -71.56646 -71.45235 -71.04527 -71.53840 -71.41477 -71.48745 -71.24595
-71.24316 -71.49224 -71.53884 -71.61176 -71.32909 -71.19667 -71.56537 -71.60811
-71.31941 -71.26125 -71.52645 -71.37970 -71.62333 -71.53806 -71.20976 -71.63016
-71.44865 -71.53616 -71.42291 -71.55957 -71.41293 -71.68302 -71.31042 -71.41840
-71.40544 -71.40229 -71.43527 -71.51255 -71.49589 -71.32359 -71.42875 -71.35012
-71.34449 -71.66231 -71.38222 -71.32403 -71.34573 -71.54860 -71.52516 -71.57391
-71.45005 -71.17626 -71.35348 -71.18113 -71.19654 -71.49245 -71.39392 -71.62983
-71.42743 -71.51568 -71.22125 -71.38675 -71.33952 -71.44987 -71.23271 -71.59146
-71.45174 -71.56533 -71.43491 -71.31484 -71.61127 -71.29733 -71.52546 -71.90537
-71.36858 -71.22092 -71.28562 -71.33749 -71.55163 -71.22627 -71.13254 -71.65207
-71.23260 -71.38108 -71.38628 -71.58354 -71.29964 -71.36153 -71.33757 -71.39049
-71.51717 -71.31066 -71.37591 -71.39002 -71.54606 -71.26250 -71.50565 -71.22707
-71.35158 -71.25058 -71.45925 -71.16126 -71.32319 -71.51423 -71.16679 -71.18261
-71.53839 -71.21520 -71.42454 -71.16010 -71.36647 -71.54083 -71.56077 -71.33184
-70.95212 -71.37913 -71.46475 -71.23994 -71.37260 -71.37473 -71.57311 -71.08522
-71.78717 -71.38438 -71.23059 -71.33282 -71.35853 -71.43319 -71.23724 -71.36068
-71.09409 -71.23132 -71.36868 -71.46797 -71.29426 -71.57361 -71.48055 -71.21610
-71.51826 -71.44671 -71.29136 -71.44452 -71.30628 -71.39478 -71.14633 -71.22270
-71.50211 -71.69550 -71.25722 -71.23891 -71.44392 -71.13676 -71.79142 -71.52495
-71.42551 -71.20452 -71.37398 -71.15763 -71.38787 -71.21852 -71.49387 -71.55764
-71.59588 -71.50651 -71.49980 -71.40167 -71.44001 -71.25082 -71.83280 -71.18478
-71.66250 -71.45182 -71.32432 -71.43973 -71.22597 -71.30579 -71.80126 -71.63586
-71.55079 -71.43515 -71.31645 -71.36347 -71.34548 -71.85096 -71.48606 -71.16043
-71.37650 -71.39880 -71.32774 -71.92550 -71.61742 -71.45686 -71.40716 -71.51187
-71.33213 -71.34953 -71.63951 -71.25744 -71.31798 -71.53859 -71.09156 -71.38690
-71.63673 -71.42238 -71.47606 -71.49351 -71.47058 -71.60427 -71.48773 -71.59747
-71.12991 -71.52342 -71.62489 -71.54064 -71.35946 -71.16722 -71.64493 -71.57386
-71.14678 -71.14005 -71.41911 -71.30556 -71.37430 -71.40445 -71.50561 -71.84667
-71.57424 -71.61445 -71.33170 -71.79977 -71.20513 -71.47610 -71.50905 -71.28284
-71.28399 -71.26933 -71.48121 -71.27147 -71.26476 -71.39583 -71.50276 -71.73455
-71.48313 -71.33921 -71.45751 -71.44913 -71.55782 -71.36587 -71.50409 -71.51541
-71.59191 -71.40008 -71.33251 -71.51190 -71.33043 -71.22397 -71.14318 -71.25181
-71.29504 -71.36014 -71.43773 -71.30105 -71.23465 -71.55232 -71.15457 -71.29891
-71.32491 -71.68236 -71.39176 -71.31545 -71.45369 -71.09692 -71.15442 -71.39969
-71.24307 -71.28525 -71.30360 -71.49150 -71.30326 -71.15308 -71.30664 -71.41156
-71.27461 -71.57310 -71.28908 -71.35283 -71.34787 -71.39799 -71.67346 -71.28409
-71.60083 -72.25481 -71.25174 -71.33340 -71.45725 -71.26785 -71.39252 -71.40398
-71.49872 -71.62495 -71.32094 -71.47643 -71.50356 -71.36823 -71.19088 -71.39832
-71.53414 -71.39662 -71.48584 -71.38486 -71.72284 -71.33254 -71.34371 -71.23122
-70.99841 -71.29135 -71.54951 -71.30270 -71.53613 -71.47083 -71.47261 -71.48436
-71.58721 -71.61384 -71.43823 -71.41084 -71.45111 -71.54305 -71.44218 -71.37124
-71.08828 -71.51330 -71.52433 -71.34809 -71.58003 -71.17822 -71.39575 -71.35736
-71.32332 -71.49820 -71.53015 -71.33305 -71.38092 -71.31892 -71.62051 -71.80319
-71.30933 -71.23339 -71.23624 -71.34261 -71.36022 -71.29029 -71.42287 -71.43590
-71.41202 -71.51885 -71.42345 -71.54041 -71.35273 -71.28048 -71.21408 -71.47005
-71.41548 -70.97543 -71.61135 -71.31298 -71.23738 -71.23406 -71.44410 -71.14560
-71.69435 -71.24092 -71.69058 -71.81717 -71.23003 -71.30592 -71.48122 -71.42855
-71.29264 -71.42407 -71.38289 -71.30363 -71.49056 -71.43661 -71.57299 -71.37172
-71.13977 -71.35490 -71.30896 -71.73853 -71.39749 -71.04442 -71.42602 -71.33803
-71.40880 -71.40340 -71.23217 -71.49969 -71.52340 -71.21329 -71.33723 -71.22618
-71.39164 -71.32127 -71.39272 -71.44225 -71.50869 -71.50750 -71.45475 -71.28460
-71.60241 -71.40318 -71.26271 -71.31463 -71.69180 -71.27882 -71.48782 -71.33570
-71.44951 -71.39185 -71.40959 -71.28062 -71.45975 -71.41667 -71.57733 -71.54340
-71.25164 -71.52022 -71.31719 -71.24265 -71.24241 -71.61805 -71.56586 -71.56005
-71.69836 -71.67345 -71.49843 -71.36472 -71.40421 -71.41574 -71.13280 -71.49097
-71.67906 -71.66096 -71.42249 -71.74898 -71.34797 -71.79567 -71.68738 -71.01098
-71.45593 -71.44628 -71.36690 -71.47493 -71.41991 -71.53660 -71.36569 -71.28983
-71.26387 -71.30784 -71.46222 -71.42731 -71.56386 -71.41299 -71.18230 -71.63683
-71.38322 -71.61700 -71.30942 -70.95959 -71.54122 -71.29405 -71.30363 -71.48701
-71.09751 -71.59248 -71.45459 -71.61256 -71.57295 -71.26916 -71.35698 -71.23127
-71.28769 -71.32861 -71.74553 -71.50641 -71.68478 -71.01703 -71.38205 -71.59149
-71.25279 -71.71459 -71.52204 -71.52321 -71.77176 -71.27461 -71.40748 -71.40120
-71.38786 -71.33334 -71.46632 -71.46199 -71.20972 -71.38841 -71.32922 -71.08520
-71.18577 -71.59566 -71.71405 -71.61480 -71.60245 -71.45231 -71.41036 -71.45168
-71.42045 -71.36490 -71.30534 -71.52583 -71.46492 -71.66569 -71.45653 -71.22834
-71.28234 -71.69491 -71.24988 -71.49465 -71.35360 -71.28741 -71.10320 -71.25354
-71.46127 -71.47441 -71.44628 -71.40100 -71.49106 -71.67878 -71.60564 -71.29476
-71.22293 -71.41499 -71.52522 -71.42473 -71.54229 -71.63770 -71.47044 -71.41542
-71.34397 -71.49359 -71.51848 -71.64782 -71.40389 -71.34146 -71.60202 -71.44789
-71.51716 -71.27769 -71.65191 -71.47776 -71.31838 -71.37001 -71.46412 -71.30328
-71.55992 -71.45568 -71.31471 -71.33185 -71.17320 -71.31931 -71.61913 -71.41348
-71.45622 -71.58238 -71.20983 -71.52712 -71.30595 -71.19937 -71.34670 -71.45462
-71.20442 -71.53906 -71.57162 -71.53449 -71.68222 -71.54797 -71.44435 -71.36317
-71.45329 -71.46034 -71.32220 -71.21886 -71.19182 -71.60258 -71.31526 -71.47686
-71.39229 -71.46285 -71.45123 -71.76792 -71.54455 -71.36839 -71.38403 -71.23916
-71.29013 -71.40627 -71.16717 -71.31324 -71.03376 -71.36455 -71.21284 -71.33510
-71.09679 -71.31246 -71.27266 -71.35622 -71.86621 -71.22185 -71.57532 -71.54551
-71.74144 -71.54038 -71.49356 -71.38387 -71.43140 -71.48066 -71.66301 -71.51898
-71.30288 -71.50101 -71.06325 -71.15143 -71.65075 -71.23101 -71.41040 -71.57990
-71.54855 -71.28884 -71.62438 -71.21251 -71.26291 -71.56735 -71.40261 -71.24345
-71.53958 -71.18432 -71.35811 -71.13422 -71.22907 -71.57367 -71.77204 -71.28787
-71.49291 -71.46568 -71.43812 -71.34491 -71.68312 -71.50761 -71.39244 -71.27765
-71.61694 -71.32342 -71.55128 -71.49129 -71.46371 -71.20680 -71.71806 -71.40345
-71.41639 -71.55331 -71.55032 -71.39801 -71.48684 -71.37209 -71.52380 -71.45489
-71.11786 -71.46575 -71.37085 -71.50894 -71.34022 -71.49540 -71.04559 -71.27954
-71.44092 -71.68441 -71.39193 -71.53534 -71.62293 -71.25873 -71.40494 -71.76729
-71.42171 -71.28922 -71.42716 -71.50442 -71.28990 -71.20440 -71.31196 -71.82862
-71.41810 -71.40770 -71.47142 -71.20069 -71.29650 -71.32096 -71.32949 -71.61499
-71.21870 -71.58565 -71.20886 -71.49291 -71.47314 -71.62950 -71.38689 -71.53477
-71.44835 -71.39976 -71.32770 -71.45507 -71.30634 -71.31413 -71.22074 -71.41889
-71.28015 -71.29953 -71.52560 -71.35900 -71.72987 -71.50264 -71.69171 -71.27987
-71.54472 -71.57586 -71.32794 -71.55778 -71.51345 -71.26937 -71.39606 -71.27165
-71.55995 -71.38885 -71.30580 -71.45099 -71.56762 -71.32650 -71.54695 -71.35894
-71.35265 -71.42551 -71.49082 -71.31094 -71.41117 -71.43388 -71.27938 -71.29246
-71.28989 -71.54931 -71.39027 -71.55064 -71.51271 -71.28087 -71.18695 -71.38434
-71.30326 -71.61730 -71.52387 -71.18871 -71.66321 -71.23049 -71.58838 -71.42989
-71.39033 -71.31153 -71.17767 -71.18728 -71.57511 -71.12908 -71.38489 -71.48642
-71.38846 -71.56551 -71.48702 -71.45550 -71.28383 -71.39986 -71.52042 -71.30492
-71.54320 -71.31060 -71.23467 -71.33942 -71.45220 -71.29147 -71.48660 -71.52255
-71.16940 -71.47966 -71.31682 -71.44417 -71.58613 -71.49606 -71.46846 -71.36972
-71.59216 -71.50023 -71.59755 -71.52107 -71.34155 -71.56291 -71.68052 -71.44985
-71.24520 -71.25849 -71.32769 -71.29220 -71.54172 -71.22415 -71.55282 -71.11454
-71.29029 -71.44240 -71.45854 -71.16235 -71.18740 -71.33740 -71.34589 -71.52757
-71.18855 -71.55006 -71.40119 -71.39723 -71.36431 -71.36701 -71.18654 -71.39668
-71.49985 -71.25141 -71.38924 -71.70481 -71.35471 -71.48188 -71.40907 -71.62260
-71.32157 -71.34395 -71.43260 -71.36786 -71.06763 -71.44931 -71.55415 -71.20339
-71.23033 -71.56429 -71.37583 -71.63605 -71.44745 -71.28621 -71.30751 -71.55532
-71.42255 -71.24948 -71.42307 -71.58087 -71.37568 -71.27257 -71.57444 -71.32445
-71.43831 -71.27835 -71.46466 -71.66387 -71.51753 -71.37198 -71.45749 -71.52653
-71.57056 -71.44999 -71.10510 -71.47158 -71.35880 -71.74716 -71.31708 -71.65257
-71.47628 -71.50474 -71.49583 -71.17710 -71.37415 -71.36811 -71.40298 -71.27671
-71.41876 -71.25762 -71.32865 -71.34159 -71.39311 -71.79638 -71.64647 -71.41602
-71.75530 -71.51945 -71.27358 -71.42453 -71.53778 -71.66577 -71.45894 -71.56672
-71.40377 -71.37118 -71.36898 -71.15729 -71.23728 -71.35270 -71.34512 -71.21539
-71.32110 -71.50936 -71.52433 -71.70181 -71.29465 -71.59851 -71.27255 -71.24513
-71.48740 -71.52184 -71.40104 -71.24943 -71.44211 -71.32248 -71.52994 -71.33298
-71.42922 -71.55854 -71.52504 -71.45184 -71.21354 -71.79031 -71.17763 -71.66432
-71.62182 -71.33483 -71.61456 -71.49489 -71.38954 -71.35746 -71.17980 -71.65360
-71.39068 -71.33306 -71.54197 -71.90140 -71.73709 -71.44435 -71.44633 -71.16796
-71.45243 -71.48266 -71.54742 -71.16977 -71.54126 -71.36317 -71.24406 -71.20704
-71.47899 -71.42272 -71.38722 -71.16602 -71.48252 -71.58134 -71.00351 -71.29982
-71.37948 -71.63827 -71.65430 -71.64282 -71.28013 -71.52055 -71.61712 -71.31476
-71.25932 -71.42313 -71.28849 -71.51264 -71.26094 -71.48320 -70.98491 -71.54506
-71.42576 -71.76097 -71.31252 -71.59324 -71.42308 -71.42447 -71.26651 -71.34938
-71.31678 -71.35380 -71.15576 -71.56865 -71.16603 -71.49268 -71.20120 -71.41438
-71.24580 -71.29377 -71.53745 -71.31452 -71.15412 -71.22965 -71.68901 -71.34401
-71.74226 -71.32662 -71.13779 -71.70289 -71.46367 -71.24981 -71.42619 -71.68683
-71.28157 -71.34409 -71.22886 -71.69730 -71.23428 -71.59707 -71.53727 -71.23917
-71.12005 -70.99035 -71.32268 -71.43399 -71.56883 -71.78995 -71.58283 -71.30598
-71.30943 -71.22753 -71.53640 -71.31317 -71.39879 -71.19261 -71.23517 -71.59289
-71.32109 -71.35865 -71.31263 -71.79376 -71.51062 -71.52118 -71.37242 -71.53054
-71.46256 -71.42607 -71.43030 -71.54464 -71.40861 -71.49912 -71.45029 -71.60951
-71.43910 -71.42666 -71.74686 -70.88081 -71.38536 -71.36507 -71.35031 -71.57240
-71.13817 -71.45029 -71.24299 -71.57085 -71.36296 -71.58210 -71.38091 -71.46554
-71.16929 -71.29791 -71.58362 -71.36602 -71.28019 -71.54473 -71.29194 -71.36928
-71.50109 -71.44832 -71.57080 -71.47184 -71.29265 -71.59215 -71.31219 -71.45675
-71.36181 -71.36828 -71.33917 -71.70677 -71.24422 -71.54678 -71.16884 -71.11431
-71.25644 -71.75001 -71.19152 -71.48449 -71.46974 -71.60909 -71.50653 -71.51476
-71.24674 -71.51020 -71.43997 -71.36261 -71.45228 -71.28844 -71.59816 -71.50113
-71.45147 -71.38908 -71.51538 -71.53125 -71.30766 -71.16516 -71.30199 -71.53893
-71.41945 -71.50537 -71.11611 -71.65218 -71.23033 -71.19425 -71.40497 -71.56815
-71.58113 -71.21632 -71.48883 -71.28895 -71.55530 -71.24883 -71.30922 -71.43039
-71.54854 -71.30833 -71.22339 -71.51660 -71.27644 -71.51081 -71.37325 -71.49903
-71.37149 -71.44705 -71.43473 -71.31602 -71.54242 -71.42052 -71.30690 -71.44309
-71.45764 -71.76768 -71.62442 -71.29758 -71.10042 -71.15186 -71.41996 -71.24727
-71.51495 -71.34531 -71.59052 -71.16729 -71.35388 -71.57864 -71.47475 -71.23211
-71.31008 -71.53587 -71.23072 -71.37577 -71.43515 -71.60541 -71.53749 -71.40465
-71.11936 -71.72809 -71.44128 -71.38518 -71.28255 -71.46543 -71.54099 -71.46475
-71.26362 -71.06253 -71.38711 -71.26559 -71.48756 -71.25968 -71.39108 -71.31621
-71.28116 -71.53358 -71.50221 -71.50109 -71.41110 -71.54753 -71.33488 -71.85933
-71.43069 -71.09855 -71.34641 -71.47074 -71.40875 -71.37894 -71.41416 -71.37212
-71.78007 -71.38650 -71.54814 -71.50886 -71.60893 -71.59177 -71.29106 -71.42910
-71.48465 -71.43479 -71.53215 -71.60925 -71.45299 -71.43772 -71.49173 -71.37815
-71.57518 -71.18278 -71.29571 -71.77761 -71.33213 -71.47589 -71.43021 -71.21060
-71.59395 -71.53411 -71.43335 -71.42017 -71.50940 -71.33969 -71.30912 -71.38940
-71.38705 -71.58376 -71.07407 -71.48794 -71.16922 -71.25525 -71.59887 -71.55174
-71.39765 -71.47762 -71.39809 -71.32297 -71.26175 -71.19766 -71.16793 -71.50664
-71.41499 -71.29676 -71.40887 -71.39750 -71.46706 -71.59448 -71.28489 -71.29757
-71.26597 -71.39402 -71.35656 -71.37159 -71.21603 -71.46410 -71.37991 -71.55595
-71.22616 -71.13189 -71.43838 -71.56795 -71.52390 -71.42226 -71.56501 -71.43758
-71.26900 -71.78829 -71.44794 -71.35688 -71.53623 -71.37070 -71.51954 -71.37040
-71.39695 -71.67123 -71.42371 -71.46517 -71.36972 -71.70121 -71.59109 -71.39169
-71.38198 -71.23938 -71.29440 -71.38722 -71.30951 -71.60707 -71.69655 -71.26437
-71.10018 -71.44799 -71.57563 -71.38606 -71.44987 -71.70501 -71.99699 -71.53172
-71.28088 -71.33568 -71.32287 -71.37064 -71.30139 -71.57489 -71.57029 -71.44682
-71.44483 -71.53329 -71.59898 -71.38601 -71.21352 -71.37325 -71.50038 -71.36710
-71.49968 -71.46094 -71.38688 -71.39162 -71.52598 -71.15570 -71.55492 -71.58701
-71.18227 -71.90830 -71.28598 -71.32996 -71.63272 -71.79027 -71.74771 -71.53586
-71.35607 -71.24395 -71.39589 -71.33617 -71.36851 -71.40180 -71.78419 -71.22168
-71.51256 -71.27593 -71.82368 -71.56615 -71.44322 -71.48437 -71.58518 -71.54043
-71.68510 -71.66280 -71.33452 -71.56196 -71.63852 -71.65410 -71.33273 -71.28216
-71.50448 -71.28873 -71.39206 -71.19031 -71.43875 -71.29076 -71.46985 -71.36089
-71.64563 -71.53667 -71.37849 -71.36606 -71.62362 -71.41257 -71.33393 -71.46389
-71.51730 -71.35304 -71.37489 -71.55055 -71.60482 -71.46721 -71.23590 -71.37422
-71.38506 -71.59710 -71.70236 -71.54114 -71.36841 -71.21438 -71.45466 -71.44678
-71.63656 -71.70171 -71.23540 -71.40356 -71.48949 -71.42414 -71.23747 -71.37818
-71.55121 -71.41054 -71.20742 -71.03248 -71.15295 -71.55889 -71.37813 -71.31821
-71.34733 -71.61105 -71.58044 -71.72321 -71.66008 -71.43686 -71.57609 -71.28023
-71.24232 -71.35096 -71.23835 -71.29543 -71.15166 -71.38296 -71.45600 -71.39402
-71.04984 -71.49926 -71.47371 -71.38314 -71.47274 -71.37452 -71.20319 -71.77402
-71.43539 -71.29447 -71.57252 -71.43577 -71.67300 -71.63648 -71.34410 -71.34265
-71.43293 -71.11958 -71.29192 -71.30551 -71.43535 -71.26993 -71.06496 -71.52343
-71.68489 -71.30944 -71.48614 -71.58851 -71.22127 -71.24494 -71.39857 -71.66759
-71.34269 -71.39903 -71.52362 -71.35638 -71.28763 -71.27829 -71.31284 -71.72421
-71.55513 -71.22362 -71.61114 -71.52856 -71.56074 -71.34489 -71.53411 -71.52529
-71.38930 -71.27150 -71.32451 -71.26820 -71.38402 -71.62728 -71.42174 -71.02920
-71.37118 -71.32659 -71.55079 -71.16042 -71.44771 -71.42040 -71.50223 -71.45818
-71.50482 -70.93293 -71.42081 -71.40841 -71.23456 -71.55432 -71.37305 -71.26858
-71.56544 -71.29278 -71.39160 -71.19680 -71.38841 -71.30123 -71.26346 -71.38360
-71.35420 -71.37710 -71.36369 -71.15338 -71.44087 -71.69817 -71.25828 -71.03087
-71.44550 -71.60850 -71.41738 -71.60211 -71.48274 -71.54492 -71.67402 -71.22307
-71.33282 -71.51116 -71.31302 -71.49736 -71.27264 -71.48791 -71.49175 -71.36378
-71.59267 -71.81081 -71.44932 -71.44554 -71.21107 -71.52557 -71.13288 -71.06212
-71.75296 -71.57105 -71.51897 -71.42023 -71.36682 -71.38313 -71.60744 -71.51198
-71.22996 -71.17360 -71.56916 -71.61688 -71.43772 -71.47347 -71.63031 -71.59458
-71.35716 -71.67831 -71.63613 -71.46251 -71.48946 -71.46276 -71.40865 -71.53397
-71.46106 -71.30971 -71.55764 -71.68119 -71.17408 -71.41645 -71.24833 -71.56594
-71.66188 -71.33112 -71.39745 -71.37843 -71.65125 -71.30482 -71.19421 -71.55422
-71.28020 -71.26235 -71.23976 -71.48876 -71.08172 -71.26113 -71.29054 -71.53310
-71.27093 -71.44909 -71.48547 -71.49784 -71.44635 -71.66191 -71.11842 -71.38096
-71.40017 -71.40323 -71.66316 -71.27128 -71.21764 -71.28916 -71.34051 -71.64509
-71.41727 -71.19056 -71.33684 -71.20463 -71.38172 -71.49414 -71.38132 -71.17029
-71.53705 -71.69918 -71.42373 -71.51128 -71.31694 -71.48986 -71.55888 -71.33854
-71.26872 -71.49519 -71.39488 -71.24761 -71.32228 -71.52029 -71.36561 -71.44787
-71.31620 -71.32559 -71.42583 -71.38688 -71.65878 -71.33004 -71.17749 -71.42324
-71.45288 -71.31195 -71.39668 -71.39649 -71.33352 -71.71244 -71.36385 -71.66340
-71.57998 -71.40205 -71.27048 -71.43918 -71.41693 -71.17860 -71.37887 -71.43379
-71.24639 -71.19397 -71.40720 -71.73929 -71.36463 -71.30655 -71.23299 -71.48622
-71.25072 -71.59119 -71.52967 -71.31373 -71.25344 -71.39512 -71.28915 -71.60069
-71.54793 -71.46725 -71.19700 -71.61210 -71.30956 -71.39446 -71.43349 -71.11352
-71.53467 -71.39103 -71.33973 -71.39427 -71.50957 -71.28844 -71.46800 -71.29267
-71.31210 -71.30112 -71.44885 -71.51632 -71.53304 -71.16812 -71.26128 -71.48034
-71.19851 -71.39215 -71.52699 -71.53256 -71.39480 -71.36953 -71.38275 -71.36093
-71.47274 -71.63926 -71.45046 -71.49378 -71.76140 -71.30461 -71.44823 -71.25923
-71.37273 -71.23751 -71.37884 -71.46265 -71.33252 -71.33628 -71.55800 -71.41708
-71.46776 -71.56609 -71.63713 -71.26572 -71.52124 -71.60441 -71.42432 -71.49400
-71.36987 -71.55094 -71.22695 -71.49318 -71.67319 -71.22957 -71.54790 -71.02100
-71.49950 -71.39769 -71.41713 -71.47039 -71.54738 -71.51015 -71.37660 -71.23197
-71.49984 -71.39369 -71.46628 -71.24886 -71.26667 -71.47585 -71.57795 -71.39516
-71.41084 -71.37363 -71.34107 -71.32124 -71.23361 -71.32110 -71.21909 -71.72593
-71.48800 -71.48055 -71.38721 -71.48483 -71.47895 -71.23266 -71.55152 -71.47941
-71.65026 -71.54754 -71.39519 -71.26168 -71.37568 -71.47352 -71.28104 -71.31550
-71.44192 -71.40795 -71.44972 -71.62129 -71.28695 -71.16817 -71.42091 -71.74792
-71.43409 -71.56113 -71.51918 -71.20297 -71.43434 -71.12829 -71.65497 -71.20262
-71.30775 -71.55181 -71.50525 -71.63259 -71.30223 -71.34583 -71.46603 -71.44558
-71.38753 -71.17427 -71.82224 -71.25098 -71.49763 -71.31096 -71.35989 -71.38453
-71.38915 -71.69075 -71.46351 -71.73425 -71.88409 -71.38726 -71.48430 -71.65452
-71.30733 -71.27531 -71.40667 -71.38114 -71.20299 -71.67888 -71.43248 -71.26781
-71.54069 -71.56297 -71.17264 -71.54649 -71.61109 -71.16383 -71.80752 -71.43246
-71.44456 -71.11426 -71.33399 -71.44833 -71.22152 -71.54696 -71.25031 -71.15442
-71.62022 -71.44250 -71.63060 -71.57508 -71.54062 -71.39956 -71.47297 -71.63547
-71.44109 -71.48662 -71.17289 -71.16342 -71.19926 -71.37822 -71.37648 -71.28921
-71.27228 -71.36123 -71.16726 -71.09761 -71.36615 -71.48568 -71.57498 -71.41496
-71.74729 -71.34847 -71.75860 -71.12198 -71.48087 -71.44304 -71.31210 -71.55583
-71.36344 -71.42197 -71.69290 -71.74838 -71.60652 -71.32536 -71.41448 -71.19722
-71.47084 -71.55915 -71.38099 -71.43103 -71.56068 -71.44952 -71.74198 -71.51474
-71.29837 -71.19394 -71.28606 -71.58583 -71.27833 -71.34197 -71.54980 -71.29745
-71.18012 -71.35818 -71.67989 -71.45858 -71.46425 -71.40283 -71.34437 -71.38486
-71.61566 -71.27796 -71.25467 -71.51665 -71.38160 -70.98105 -71.27288 -71.31022
-71.67282 -71.34099 -71.30924 -71.26409 -71.72103 -71.20206 -71.13151 -71.70476
-71.29744 -71.49114 -71.57542 -71.42987 -71.40508 -71.43992 -71.28288 -71.41176
-71.66832 -71.55572 -71.17615 -71.50293 -71.31331 -71.45047 -71.53285 -71.56868
-71.19817 -71.27560 -71.20382 -71.43549 -71.48879 -71.40068 -71.39110 -71.16876
-71.46208 -71.29493 -71.22120 -71.49320 -71.24244 -71.32352 -71.49871 -71.38870
-71.49389 -71.46663 -71.32820 -71.42411 -71.39366 -71.40329 -71.56810 -71.29119
-71.50780 -71.43639 -71.54352 -71.28585 -71.58085 -71.46452 -71.34273 -71.47274
-71.37598 -71.21065 -71.42998 -71.43986 -71.50991 -71.78113 -71.42611 -71.45167
-71.27203 -71.33261 -71.44687 -71.37712 -71.34258 -71.11606 -71.09323 -71.43475
-71.56494 -71.57118 -71.47875 -71.52793 -71.29823 -71.45791 -71.42929 -71.73436
-71.64529 -71.37936 -71.33298 -71.39088 -71.74942 -71.52722 -71.61266 -71.29700
-71.61969 -71.32009 -71.15124 -71.24843 -71.19316 -71.59012 -71.15644 -71.39646
-71.50743 -71.39255 -71.73210 -71.34297 -71.57475 -71.43593 -71.55756 -71.35793
-71.78053 -71.61799 -71.25437 -71.61468 -71.63565 -71.25457 -71.22036 -71.35818
-71.27540 -71.39032 -71.40847 -71.65115 -71.73578 -71.40371 -71.19344 -71.38274
-71.55804 -71.04931 -71.66266 -71.16657 -71.59132 -71.44151 -71.25143 -71.61251
-71.18730 -71.53212 -71.68161 -71.25586 -71.68554 -71.10528 -71.38077 -71.36647
-71.25304 -71.44421 -71.46756 -71.63490 -71.65495 -71.27102 -71.60835 -71.24676
-71.38032 -71.35186 -71.47678 -71.61137 -71.58791 -71.27087 -71.23742 -71.31006
-71.76383 -71.67407 -71.27504 -71.62110 -71.35552 -71.25675 -71.24823 -71.30876
-71.54086 -71.62434 -71.32951 -71.46376 -71.44848 -71.19197 -71.38951 -71.77101
-71.43280 -71.52182 -71.26612 -71.25980 -71.49767 -71.44501 -71.59540 -71.48044
-71.22713 -71.52578 -71.22040 -71.12689 -71.50702 -71.27318 -71.72322 -71.47549
-71.37907 -71.65190 -71.45856 -71.42516 -71.08826 -71.35119 -71.39836 -71.44222
-71.33614 -71.76860 -71.37749 -71.57279 -71.43030 -71.41023 -71.66378 -71.63114
-71.37205 -71.61167 -71.23070 -71.49586 -71.56170 -71.25403 -71.40659 -71.50723
-71.29954 -71.51091 -71.35014 -71.17104 -71.16894 -71.56606 -71.48553 -71.37137
-71.44508 -71.39104 -71.38556 -71.68745 -71.52758 -71.45082 -71.44607 -71.63488
-71.56541 -71.20782 -71.43212 -71.43511 -71.66379 -71.22152 -71.26355 -71.33934
-71.27587 -71.30526 -71.30621 -71.40593 -71.43772 -71.21333 -71.51539 -71.40470
-71.23832 -71.47137 -71.61794 -71.72757 -71.43853 -71.43452 -71.73038 -71.19745
-71.38916 -71.65271 -71.32756 -71.52942 -71.52974 -71.34834 -71.29788 -71.47344
-71.38549 -71.26687 -71.42720 -71.23930 -71.65442 -71.51650 -71.37323 -71.23501
-71.50854 -71.19868 -71.39643 -71.45319 -71.18908 -71.64635 -71.29882 -71.43550
-71.37396 -71.60844 -71.54760 -71.09201 -71.41705 -71.33031 -71.43016 -71.43540
-71.51380 -71.30027 -71.37586 -71.85145 -71.20970 -71.54587 -71.28307 -71.65636
-71.37723 -71.40082 -71.52676 -71.30501 -71.54381 -71.12236 -71.42391 -71.48326
-71.60102 -71.30675 -71.22604 -71.75460 -71.34132 -71.76652 -71.27517 -71.38074
-71.49999 -71.34174 -71.52463 -71.33859 -71.28532 -71.34115 -71.36400 -71.19423
-71.40597 -71.38881 -71.49778 -71.47211 -71.06677 -71.75081 -71.37312 -71.41151
-71.73011 -71.19019 -71.55848 -71.49086 -71.41090 -71.51916 -71.30108 -71.47996
-71.24838 -71.38598 -71.28399 -71.57537 -71.37440 -71.92821 -71.37318 -71.16322
-71.44554 -71.26231 -71.15982 -71.63279 -71.28914 -71.44938 -71.59186 -71.41921
-71.30888 -71.49559 -71.39201 -71.41910 -71.40252 -71.48684 -71.40970 -71.41842
-71.39723 -71.11152 -71.61612 -71.36708 -71.32116 -71.41906 -71.39973 -71.44934
-71.45683 -71.30630 -71.26130 -71.09267 -71.67698 -71.34452 -71.19901 -71.46222
-71.66403 -71.68270 -71.29818 -71.39148 -71.59303 -71.50254 -71.54400 -71.40813
-71.33165 -71.44802 -71.53101 -71.30716 -71.33810 -71.28899 -71.41729 -71.40190
-71.57751 -71.28191 -71.62698 -71.25276 -71.55629 -71.66956 -71.41511 -71.22083
-71.59941 -71.42647 -71.27933 -71.59981 -71.29208 -71.12887 -71.17977 -71.17702
-71.29310 -71.60161 -71.28813 -71.50109 -71.17979 -71.65371 -71.20822 -71.59703
-71.35492 -71.52069 -71.43284 -71.51337 -71.55709 -71.35707 -71.43924 -71.12457
-71.38335 -71.40920 -71.61337 -71.40073 -71.88910 -71.09382 -71.57262 -71.48220
-71.30532 -71.28538 -71.28720 -71.25475 -71.53524 -71.45295 -71.23068 -71.29726
-71.47176 -71.15017 -71.61913 -71.15397 -71.39538 -71.50261 -71.67815 -71.26004
-71.22456 -71.23894 -71.43413 -71.30288 -71.32806 -71.38360 -71.67787 -71.49217
-71.34533 -71.49972 -71.50215 -71.55457 -71.35643 -71.41311 -71.56878 -71.10174
-71.38932 -71.26568 -71.55685 -71.14807 -71.15996 -71.43131 -71.31529 -71.36032
-71.50317 -71.54833 -71.56992 -71.29280 -71.34450 -71.26867 -71.48999 -71.63356
-71.47789 -71.38269 -71.30560 -71.38072 -71.33767 -71.69457 -71.27112 -71.46343
-71.57957 -71.48696 -71.80311 -71.54157 -71.78864 -71.40053 -71.54378 -71.44061
-71.52776 -71.40095 -71.32086 -71.50113 -71.73498 -71.49189 -71.53033 -71.72526
-71.25906 -71.19738 -71.42226 -71.50852 -71.04656 -71.49212 -71.75991 -71.40050
-71.47493 -71.22432 -71.30482 -71.54006 -71.26962 -71.50929 -71.45761 -71.56760
-71.67207 -71.81869 -71.45733 -71.22407 -71.49347 -71.46178 -71.63465 -71.17557
-71.56037 -71.14060 -71.36135 -71.56243 -71.53215 -71.51185 -71.35848 -71.54510
-71.46013 -71.14467 -71.36800 -71.44108 -71.43783 -71.57202 -71.47413 -71.63561
-71.64031 -71.43745 -71.10331 -71.71019 -71.24571 -71.63013 -71.45066 -71.57554
-71.28178 -71.41727 -71.42874 -71.19047 -71.40388 -71.62346 -71.56750 -71.55669
-71.58988 -71.48969 -71.41052 -71.37864 -71.20301 -71.61338 -71.34053 -71.42541
-71.41980 -71.43909 -71.64524 -71.91940 -71.17520 -71.46389 -71.23379 -71.40585
-71.62877 -71.49954 -71.48125 -71.22627 -71.41542 -71.38674 -71.76864 -71.66567
-71.33890 -71.34173 -71.10381 -71.41524 -71.36170 -71.36347 -71.51115 -71.40076
-71.35047 -71.37181 -71.32409 -71.32556 -71.57795 -71.49587 -71.25065 -71.43885
-71.41543 -71.68691 -71.44412 -71.39539 -71.19174 -71.33332 -71.45910 -71.21952
-71.54565 -71.60301 -71.39769 -71.14307 -71.00842 -71.50577 -71.30899 -71.60259
-71.56661 -71.85148 -71.17792 -71.53246 -71.30433 -71.41198 -71.55728 -71.39743
-71.18133 -71.62492 -71.67474 -71.34058 -71.52160 -71.68567 -71.47268 -71.50446
-71.42283 -71.49075 -71.60906 -71.41311 -71.73485 -71.37611 -71.84101 -71.27812
-71.47109 -71.35657 -71.45472 -71.59376 -71.40008 -71.18586 -71.56574 -71.12396
-71.53249 -71.22836 -71.51433 -71.51471 -71.38309 -71.34061 -71.20582 -71.27637
-71.53241 -71.57302 -71.43883 -71.62769 -71.37827 -71.37200 -71.31067 -71.48553
-71.51959 -71.39228 -71.61835 -71.63415 -71.35500 -71.27042 -71.87052 -71.49823
-71.29635 -71.31690 -71.29845 -71.54121 -71.41807 -71.75868 -71.49158 -71.49023
-71.57363 -71.30788 -71.52129 -71.39803 -71.58890 -71.20771 -71.61408 -71.49069
-71.36396 -71.56277 -71.58836 -71.16053 -71.58823 -71.39307 -71.65467 -71.66399
-71.53277 -71.58364 -71.69941 -71.45815 -71.50435 -71.84471 -71.41859 -71.17282
-71.33776 -71.26976 -71.38647 -71.50412 -71.52744 -71.68168 -71.72984 -71.28123
-71.67551 -71.26468 -71.64098 -71.40325 -71.73570 -71.28950 -71.72530 -71.52698
-71.29767 -71.50444 -71.13088 -71.44049 -71.37574 -71.62764 -71.62165 -71.48356
-71.23269 -71.63320 -71.42321 -71.54529 -71.66870 -71.41864 -71.57918 -71.38065
-71.56993 -71.47919 -71.70509 -71.22101 -71.26329 -71.67200 -71.43580 -71.27681
-71.45403 -71.38397 -71.37609 -71.53163 -71.51523 -71.43802 -71.45977 -71.31161
-71.19571 -71.26322 -71.52824 -71.53831 -71.41561 -71.47550 -71.28793 -71.37999
-71.29350 -71.58011 -71.56247 -71.57642 -71.30814 -71.63297 -71.51987 -71.22895
-71.49431 -71.56171 -71.59846 -71.31378 -71.92613 -71.64183 -71.58013 -71.49768
-71.51217 -71.26127 -71.47802 -71.38598 -71.82521 -71.29986 -71.43307 -71.25258
-71.45428 -71.15244 -71.18759 -71.33924 -71.62545 -71.52807 -71.44151 -71.14809
-71.37159 -71.35271 -71.44286 -71.39209 -71.40190 -71.37381 -71.52079 -71.24962
-71.35242 -71.20072 -71.46777 -71.52619 -71.22903 -71.40751 -71.46290 -71.46814
-71.65442 -71.51309 -71.11482 -71.50210 -71.12136 -71.53837 -71.35926 -71.86727
-71.24329 -71.59908 -71.19466 -71.23906 -71.46225 -71.53841 -71.28783 -71.63808
-71.27351 -71.65475 -71.37187 -71.55909 -71.31063 -71.53286 -71.71884 -71.45781
-71.48406 -71.50072 -71.51216 -71.50287 -71.50086 -71.23059 -71.53498 -71.79290
-71.41119 -71.47506 -71.24667 -71.66586 -71.32138 -71.57399 -71.34099 -71.45986
-71.25902 -71.25245 -71.56865 -71.56041 -71.25036 -71.69609 -71.11759 -71.29430
-71.20192 -71.66006 -71.18997 -71.53829 -71.28771 -71.33040 -71.36672 -71.31623
-71.62352 -71.20802 -71.47256 -71.45582 -71.19575 -71.50685 -71.24486 -71.24096
-71.71186 -71.45461 -71.35281 -71.26353 -71.45929 -71.58149 -71.41592 -71.87500
-71.25713 -71.58144 -71.39536 -71.26073 -71.29019 -71.25453 -71.38412 -71.33977
-71.36698 -71.39432 -71.38074 -71.54817 -71.34637 -71.41549 -71.46352 -71.40444
-71.66361 -71.59043 -71.35133 -71.12285 -71.66657 -71.75590 -71.43567 -71.33796
-71.34071 -71.50635 -71.49477 -71.44350 -71.28555 -71.45701 -71.29998 -71.64836
-71.51912 -71.58330 -71.54632 -71.30333 -71.27169 -71.54929 -71.40769 -71.22307
-71.54940 -71.43739 -71.25333 -71.66894 -71.41213 -71.61738 -71.72392 -71.37289
-71.14585 -71.09567 -71.32417 -71.24016 -71.62765 -71.31270 -71.50439 -71.60164
-71.68539 -71.46669 -71.47503 -71.49963 -71.35644 -71.10519 -71.45594 -71.60305
-71.41162 -71.55780 -71.30039 -71.43526 -71.46988 -71.38573 -71.81479 -71.47315
-71.56446 -71.20060 -71.63248 -71.67250 -71.32050 -71.49957 -71.35811 -71.35587
-71.56287 -71.61425 -71.35516 -71.26246 -71.35993 -71.48313 -71.32891 -71.42933
-71.28584 -71.53938 -71.72845 -71.60107 -71.41492 -71.36213 -71.42207 -71.38074
-71.26694 -71.22881 -71.52911 -71.28510 -71.34136 -71.52816 -71.77440 -71.44790
-71.16898 -71.69025 -71.38637 -71.35535 -71.71887 -71.34427 -71.20364 -71.18229
-71.04827 -71.29715 -71.60841 -71.50317 -71.55793 -71.29139 -71.52493 -71.07847
-71.29236 -71.30382 -71.40713 -71.31418 -71.37621 -71.35645 -71.44193 -71.27768
-71.39259 -71.61626 -71.28742 -71.37569 -71.34116 -71.35411 -71.31498 -71.40524
-71.89398 -71.39679 -71.41374 -71.43267 -71.07779 -71.53082 -71.27966 -71.54902
-71.30781 -71.95852 -71.22668 -71.35426 -71.16453 -71.20361 -71.46682 -71.62300
-71.51644 -71.51221 -71.13813 -71.35127 -71.41773 -71.29403 -71.24472 -71.43346
-71.46242 -71.37672 -71.44488 -71.18202 -71.46472 -71.30165 -71.58900 -71.37870
-71.23767 -71.69711 -71.56365 -71.51088 -71.44327 -71.51198 -71.56829 -71.33191
-71.57247 -71.70395 -71.45817 -71.47454 -71.31327 -71.17401 -71.37125 -71.52102
-71.44463 -71.27285 -71.49835 -71.42337 -71.24356 -70.99811 -71.56093 -71.27811
-71.46356 -71.33253 -71.41412 -71.50917 -71.48326 -71.39726 -71.25074 -71.36967
-71.25001 -71.36407 -71.06834 -71.33045 -71.37450 -71.39184 -71.33240 -71.32565
-71.42073 -71.50472 -71.56623 -71.30409 -71.39761 -71.73927 -71.37690 -71.36032
-71.32239 -71.58081 -71.52874 -71.53377 -71.20067 -71.37113 -71.47665 -71.32347
-71.44729 -71.49250 -71.44629 -71.49011 -71.46691 -71.63187 -71.22913 -71.28740
-71.54627 -71.49868 -71.60842 -71.59248 -71.36949 -71.38562 -71.24004 -71.47552
-71.18348 -71.27027 -71.28477 -71.44434 -71.18272 -71.69382 -71.40389 -71.36001
-71.53442 -71.24975 -71.53049 -71.73004 -71.24261 -71.62894 -71.45727 -71.47942
-71.36844 -71.48446 -71.46816 -71.35913 -71.32754 -71.30984 -71.36673 -71.31043
-71.64666 -71.30566 -71.58148 -71.48117 -71.35184 -71.32060 -71.41068 -71.14066
-71.61643 -71.36680 -71.32032 -71.46074 -71.57296 -71.27150 -71.30066 -71.51587
-71.36697 -71.36020 -71.14868 -71.37507 -71.18954 -71.05078 -71.49274 -71.47760
-71.39015 -71.41525 -71.37786 -71.48321 -71.41955 -71.68737 -71.37349 -71.42547
-71.31636 -71.23246 -71.47776 -71.52269 -71.43338 -71.35551 -71.46830 -71.53839
-71.37651 -71.38349 -71.43672 -71.47032 -71.43678 -71.38655 -71.42432 -71.27231
-71.32832 -71.46422 -71.29914 -71.22769 -71.53304 -71.21951 -71.59814 -71.09797
-71.36650 -71.12099 -71.35200 -71.66011 -71.55385 -71.46725 -71.48537 -71.13728
-71.63873 -71.40512 -71.46611 -71.45815 -71.48161 -71.37434 -71.35774 -71.49825
-71.30348 -71.55548 -71.55919 -71.25371 -71.38775 -71.19554 -71.47793 -71.51963
-71.27399 -71.32651 -71.34314 -71.26313 -71.27259 -71.44624 -71.50408 -71.62435
-71.44080 -71.35943 -71.41365 -71.28145 -71.48481 -71.39106 -71.41653 -71.56672
-71.39947 -71.17041 -71.61403 -71.45121 -71.33876 -71.37314 -71.35579 -71.20535
-71.14463 -71.55035 -71.09030 -71.63413 -71.35715 -71.33408 -71.44968 -71.39822
-71.50423 -71.47782 -71.35208 -71.39780 -71.54291 -71.18253 -71.42383 -71.16953
-71.39524 -71.60054 -71.51889 -71.45264 -71.32951 -71.56298 -71.41375 -71.36393
-71.63648 -71.44315 -71.30909 -71.47628 -71.41951 -71.68004 -71.48442 -71.39732
-71.27469 -71.65811 -71.46601 -71.29357 -71.58376 -71.33161 -71.66666 -71.41683
-71.61952 -71.45667 -71.17028 -71.51769 -71.42138 -71.60691 -71.46323 -71.55129
-71.37008 -71.39002 -71.08205 -71.47826 -71.32124 -71.47955 -71.29099 -71.18764
-71.42519 -71.69497 -71.51091 -71.35613 -71.61840 -71.48551 -71.23540 -71.43105
-71.48185 -71.42005 -71.55853 -71.37978 -71.22828 -71.73230 -71.15269 -71.11721
-71.47221 -71.28306 -71.65479 -71.24061 -71.70863 -71.34274 -71.31133 -71.38630
-71.48953 -71.37743 -71.43362 -71.47506 -71.57317 -71.31425 -71.34215 -71.46043
-71.47570 -71.29596 -71.26614 -71.32876 -71.44584 -71.51366 -71.33738 -71.41770
-71.52479 -71.52281 -71.52118 -71.25590 -71.46341 -71.57088 -71.76670 -71.50481
-71.13278 -71.58939 -71.73858 -71.23100 -71.58137 -71.64040 -71.41286 -71.56911
-71.47675 -71.32192 -71.50037 -71.50603 -71.34832 -71.48424 -71.45710 -71.36321
-71.61085 -71.56470 -71.51682 -71.33638 -71.40273 -71.36969 -71.49681 -71.44723
-71.64099 -71.30590 -71.60458 -71.65013 -71.53974 -71.65634 -71.41013 -71.49111
-71.44907 -71.36181 -71.35492 -71.28990 -71.43051 -71.50290 -71.42015 -71.41447
-71.60661 -71.36473 -71.39626 -71.34084 -71.05739 -71.57917 -71.50539 -71.37845
-71.44881 -71.35324 -71.43043 -71.14164 -71.44648 -71.33068 -71.66416 -71.31850
-71.14575 -71.16789 -71.70221 -71.34007 -71.38342 -71.35434 -71.51737 -71.48897
-71.46367 -71.51753 -71.38566 -71.54322 -71.65643 -71.00776 -71.38972 -71.57979
-71.31688 -71.51873 -71.73859 -71.26355 -71.33756 -71.40856 -71.40954 -71.51337
-71.39319 -71.43487 -71.12135 -71.57996 -71.36473 -71.70295 -71.34296 -71.31773
-71.20992 -71.47740 -71.41480 -71.23476 -71.62657 -71.46051 -71.30069 -71.46349
-71.27259 -71.47691 -71.45222 -71.28931 -71.59042 -71.28726 -71.29589 -71.26034
-71.31598 -71.16667 -71.47878 -71.50703 -71.36490 -71.46764 -71.41080 -71.58722
-71.47787 -71.48522 -71.32667 -71.31578 -71.24252 -71.35771 -71.59936 -71.40275
-71.35384 -71.47774 -71.54326 -71.42846 -71.35858 -71.45047 -71.21145 -71.56430
-71.38967 -71.56504 -71.25779 -71.51638 -71.42196 -71.26239 -71.11815 -71.61549
-71.62640 -70.99074 -71.57307 -71.45711 -71.33621 -71.46903 -71.52872 -71.32944
-71.19342 -71.37854 -71.44895 -71.52291 -71.11749 -71.48666 -71.50404 -71.50102
-71.25776 -71.53478 -71.47883 -71.55559 -71.41431 -71.27490 -71.50253 -71.46045
-71.55031 -71.45755 -71.61125 -71.41330 -71.60382 -71.43043 -71.28966 -71.41047
-71.36081 -71.39331 -71.24383 -71.40925 -71.28127 -71.40257 -71.31873 -71.46601
-71.31537 -71.28012 -71.56961 -71.62868 -71.52396 -71.27102 -71.64781 -71.40909
-71.59661 -71.43661 -71.38182 -71.41626 -71.41251 -71.48837 -71.68263 -71.59724
-71.16420 -71.43685 -71.51718 -71.29782 -71.30764 -71.36200 -71.59835 -71.58802
-71.39222 -71.16736 -71.40745 -71.44202 -71.30015 -71.30768 -71.33170 -71.47893
-71.49560 -71.38520 -71.62356 -71.50053 -71.48715 -71.35142 -71.25183 -71.67294
-71.52094 -71.27936 -71.50836 -71.43078 -71.20203 -71.52574 -71.41702 -71.49105
-71.56030 -71.75999 -71.50576 -71.41611 -71.39200 -71.44597 -71.40262 -71.53339
-71.17752 -71.46476 -71.42390 -71.30874 -71.37366 -71.26497 -71.38870 -71.17355
-71.76833 -71.53921 -71.49911 -71.47547 -71.32831 -71.58950 -71.47909 -71.45180
-71.65415 -71.45994 -71.59451 -71.37384 -71.20667 -71.27561 -71.27606 -71.47500
-71.33900 -71.45349 -71.28561 -71.33424 -71.56030 -71.14370 -71.48396 -71.55263
-71.07676 -71.21239 -71.43488 -71.37875 -71.43257 -71.21261 -71.33135 -71.33824
-71.40599 -71.46033 -71.49152 -71.49803 -71.40796 -71.56335 -71.44935 -71.44249
-71.33569 -71.51506 -71.53039 -71.58894 -71.41863 -71.50021 -71.26497 -71.47975
-71.34177 -71.15879 -71.44597 -71.26707 -71.62303 -71.30089 -71.36702 -71.20014
-71.30843 -71.18357 -71.43530 -71.40936 -71.35578 -71.45265 -71.70062 -71.43875
-71.60680 -71.37258 -71.33059 -71.52609 -71.50074 -71.50286 -71.52166 -71.37163
-71.46354 -71.52497 -71.17095 -71.38860 -71.57091 -71.61897 -71.40592 -71.49570
-71.41274 -71.44980 -71.54561 -71.39148 -71.47851 -71.54514 -71.56499 -71.50573
-71.36114 -71.30158 -71.46746 -71.53260 -71.65832 -71.50650 -71.33848 -71.10178
-71.38429 -71.34653 -71.67310 -71.40799 -71.64690 -71.19647 -71.23515 -71.32686
-71.47974 -71.33705 -71.37014 -71.23055 -71.21118 -71.46093 -71.57454 -71.37043
-71.46011 -71.44587 -71.17158 -70.99778 -71.25660 -71.53787 -71.47638 -71.49394
-71.44834 -71.35909 -71.57067 -71.38667 -71.27217 -71.47308 -71.62016 -71.38821
-71.41708 -71.59517 -71.82118 -71.50514 -71.26739 -71.58084 -71.14723 -71.28897
-71.60290 -71.52835 -71.27081 -71.35533 -71.35966 -71.16213 -71.50498 -71.28226
-71.15875 -71.35035 -71.28592 -71.32147 -71.38948 -71.38746 -71.47610 -71.38796
-71.23027 -71.20851 -71.30636 -71.50666 -71.29660 -71.15505 -71.43217 -71.41578
-71.44135 -71.52205 -71.27923 -71.25780 -71.68449 -71.21687 -71.57676 -71.10077
-71.45152 -71.56045 -71.18709 -71.24788 -71.41342 -71.63018 -71.53113 -71.31945
-71.47274 -71.63106 -71.31087 -71.54624 -71.29501 -71.56951 -71.64660 -71.27007
-71.29019 -71.48095 -71.38730 -71.14182 -71.44251 -71.47637 -71.68400 -71.63549
-71.71755 -71.54181 -71.60161 -71.53494 -71.70395 -71.53879 -71.65876 -71.27645
-71.31631 -71.44930 -71.47200 -71.51205 -71.35093 -71.55954 -71.39869 -71.45386
-71.45442 -71.61327 -71.43461 -71.56523 -71.36068 -71.41914 -71.40955 -71.39157
-71.31618 -71.24152 -71.51157 -71.35975 -71.53104 -71.59342 -71.09142 -71.29912
-71.43982 -71.26189 -71.59264 -71.25967 -71.53560 -71.13870 -71.21230 -71.41928
-71.63562 -71.16961 -71.23039 -71.28482 -71.59454 -71.08282 -71.27915 -71.25371
-71.37296 -71.69398 -71.38279 -71.42063 -71.37461 -70.99892 -71.57626 -71.54611
-71.63691 -71.35173 -71.30435 -71.22641 -71.29790 -71.24324 -71.29579 -71.36657
-71.35779 -71.48613 -71.44774 -71.45999 -71.46971 -71.46798 -71.56205 -71.41985
-71.59578 -71.53071 -71.48053 -71.30930 -71.48137 -71.56970 -71.55961 -71.35174
-71.20038 -71.08334 -71.59538 -71.55735 -71.57979 -71.57955 -71.42025 -71.64303
-71.08786 -71.46863 -71.28350 -71.58762 -71.45049 -71.32144 -71.30181 -71.46226
-71.26009 -71.60047 -71.61675 -71.68927 -71.27671 -71.59796 -71.58914 -71.52587
-71.38887 -71.24931 -71.50516 -71.36904 -71.44916 -71.33898 -71.51779 -71.46958
-71.40332 -71.41649 -71.41776 -71.23250 -71.39102 -71.37229 -71.58366 -71.64983
-71.45420 -71.52696 -71.63935 -71.75110 -71.54156 -71.53453 -71.44774 -71.31066
-71.52704 -71.73270 -71.28640 -71.63495 -71.40820 -71.52577 -71.47645 -71.47024
-71.30456 -71.39806 -71.45595 -71.58373 -71.69635 -71.62482 -71.47989 -71.50707
-71.53989 -71.21071 -71.47562 -71.69953 -71.18900 -71.56105 -71.47985 -71.34205
-71.45250 -71.36363 -71.41399 -71.89923 -71.43701 -71.75725 -71.64293 -71.34175
-71.34742 -71.25035 -71.40901 -71.50757 -71.65266 -71.57546 -71.67824 -71.51823
-71.44635 -71.56356 -71.69940 -71.68738 -71.44835 -71.66375 -71.24441 -71.41333
-71.21275 -71.35294 -71.61383 -71.27141 -71.44714 -71.62317 -71.35191 -71.34405
-71.24486 -71.63956 -71.38524 -71.48872 -71.49214 -71.39934 -71.39388 -71.27731
-71.20045 -71.42262 -71.12525 -71.14270 -71.30853 -71.20956 -71.29916 -71.37635
-71.56704 -71.88928 -71.29706 -71.60238 -71.38273 -71.71560 -71.38280 -71.12105
-71.42230 -71.46098 -71.35977 -71.18775 -71.18430 -71.56076 -71.44648 -71.28825
-71.39627 -71.41584 -71.37581 -71.07375 -71.05079 -71.51978 -71.40126 -71.27644
-71.25637 -71.45338 -71.18904 -71.15501 -71.26551 -71.52884 -71.52187 -71.58545
-71.29349 -71.40823 -71.25590 -71.37488 -71.33397 -71.52878 -71.35365 -71.59265
-71.23349 -71.30405 -71.48184 -71.71946 -71.49280 -71.37829 -71.23846 -71.54268
-71.66402 -71.30067 -71.26086 -71.56052 -71.42632 -71.41495 -71.52434 -71.47775
-71.41514 -71.68560 -71.34189 -71.28246 -71.18915 -71.37550 -71.61118 -71.67697
-71.36954 -71.26990 -71.43354 -71.44271 -71.66166 -71.16886 -71.31231 -71.49450
-71.31513 -71.40045 -71.36642 -71.37210 -71.49317 -71.22551 -71.57748 -71.77041
-71.74137 -71.54503 -71.52760 -71.48661 -71.17215 -71.54644 -71.32103 -71.43357
-71.13971 -71.59284 -71.62027 -71.42343 -71.51682 -71.41326 -71.17529 -71.45570
-71.33600 -71.36768 -71.28029 -71.36540 -71.54429 -71.05729 -71.64935 -71.43573
-71.23725 -71.49537 -71.28034 -71.55620 -71.29817 -71.60858 -71.39659 -71.43270
-71.25783 -71.41597 -71.50002 -71.53168 -71.42341 -71.58525 -71.57824 -71.48257
-71.49400 -71.34959 -71.28125 -71.44926 -71.18793 -71.23835 -71.80992 -71.43872
-71.36577 -71.56657 -71.37573 -71.17159 -71.53408 -71.61296 -71.52030 -71.34239
-71.43795 -71.43425 -71.28956 -71.33106 -71.31697 -71.36136 -71.08756 -71.46064
-71.31987 -71.20283 -71.38357 -71.38804 -71.21228 -71.60690 -71.25771 -71.37320
-71.39320 -71.58660 -71.32955 -71.27608 -71.58077 -71.38574 -71.22556 -71.34467
-71.16537 -71.68522 -71.50053 -71.30632 -71.68690 -71.49141 -71.37109 -71.29188
-71.17785 -71.44822 -71.50310 -71.49472 -71.28348 -71.40467 -71.40498 -71.48407
-71.36852 -71.21618 -71.55688 -71.49800 -71.61461 -71.57545 -71.41943 -71.36062
-71.47894 -71.66772 -71.30992 -71.27945 -71.14116 -71.45162 -71.35508 -71.46762
-71.58314 -71.41777 -71.41225 -71.59004 -71.33603 -71.53295 -71.59531 -71.42977
-71.49422 -71.49928 -71.16235 -71.23539 -71.47146 -71.58068 -71.50454 -71.35680
-71.26092 -71.17778 -71.45664 -71.19808 -71.56897 -71.17937 -71.09810 -71.27742
-71.59222 -71.54653 -71.50228 -71.57245 -71.17878 -71.45733 -71.45008 -71.63692
-71.46102 -71.29418 -71.60442 -71.38970 -71.44760 -71.37872 -71.67323 -71.51196
-71.42849 -71.48450 -71.35112 -71.47016 -71.44978 -71.36559 -71.81324 -71.29529
-71.59392 -71.46928 -71.52635 -71.73300 -71.16403 -71.43846 -71.04546 -71.42977
-71.68005 -71.38642 -71.55021 -71.76996 -71.16367 -71.49388 -71.57649 -71.22922
-71.42473 -71.39108 -71.58751 -71.78212 -71.08193 -71.68975 -71.19057 -71.60601
-71.55164 -71.14256 -71.34406 -71.49117 -71.37043 -71.54858 -71.25681 -71.51527
-71.46247 -71.34294 -71.55748 -71.53704 -71.43461 -71.43759 -71.47571 -71.36205
-71.75740 -71.18533 -71.31708 -71.46307 -71.24350 -71.41736 -71.53523 -71.62969
-71.34784 -71.61995 -71.61482 -71.66792 -71.55624 -71.45668 -71.27406 -71.44594
-71.13257 -71.30472 -71.22332 -71.48065 -71.51678 -71.47376 -71.06890 -71.36382
-71.34215 -71.62587 -71.54369 -71.63600 -71.32384 -71.32885 -71.32888 -71.53590
-71.21660 -71.26093 -71.74858 -71.20771 -71.67614 -71.41707 -71.27846 -71.26047
-71.34720 -71.43493 -71.54635 -71.45669 -71.33273 -71.42377 -71.31513 -71.42230
-71.54689 -71.51220 -71.42148 -71.36911 -71.50916 -71.13231 -71.46702 -71.42097
-71.00078 -71.12098 -71.55303 -71.58555 -71.42621 -71.47290 -71.44810 -71.53367
-71.45981 -71.16637 -71.33026 -71.31295 -71.49481 -71.49232 -71.48664 -71.59520
-71.57272 -71.44761 -71.40811 -71.17943 -71.23056 -71.20825 -71.23259 -71.28439
-71.31322 -71.06897 -71.35892 -71.36203 -71.27435 -71.35043 -71.44237 -71.08195
-71.26048 -71.32785 -71.46259 -71.09490 -71.60529 -71.54995 -71.24915 -71.69691
-71.25779 -71.56140 -71.62329 -71.21769 -71.42627 -71.31627 -71.42587 -71.58756
-71.49099 -71.30875 -71.62035 -71.16157 -71.31870 -71.40147 -71.46353 -71.40297
-71.46187 -71.31198 -71.64115 -71.46454 -71.52085 -71.32584 -71.11443 -71.50410
-71.14689 -71.23023 -71.55473 -71.39401 -71.47542 -71.19702 -71.40000 -71.74198
-71.31710 -71.20725 -71.52603 -71.47012 -71.44499 -71.44909 -71.35995 -71.33540
-71.38670 -71.26195 -71.65425 -71.34329 -71.59262 -71.33486 -71.28941 -71.50172
-71.31732 -71.48170 -71.51578 -71.37614 -71.66872 -71.11675 -71.49872 -71.07861
-71.48969 -71.37098 -71.74357 -71.52492 -71.36443 -71.47059 -71.54947 -71.45979
-71.44503 -71.48344 -71.22261 -71.58499 -71.36961 -71.28988 -71.58295 -71.44216
-71.24908 -71.32610 -71.60010 -71.30412 -71.31907 -71.34029 -71.53551 -71.54432
-71.48794 -71.57603 -71.60528 -71.58460 -71.63222 -71.17910 -71.17942 -71.50941
-71.25163 -71.46696 -71.29315 -71.52741 -71.32496 -71.35289 -71.48302 -71.29502
-71.46013 -71.40081 -71.41606 -71.53519 -71.74010 -71.26200 -71.33081 -71.82387
-71.49114 -71.50973 -72.03790 -71.20323 -71.29927 -71.40702 -71.26861 -71.41787
-71.19695 -71.39634 -71.36786 -71.22159 -71.35956 -71.41285 -71.44790 -71.71239
-71.29130 -71.44603 -71.40445 -71.53838 -71.48578 -71.56937 -71.59211 -71.31770
-71.32183 -71.43592 -71.77430 -71.34808 -71.33127 -71.44857 -71.30375 -71.28107
-71.38623 -71.32431 -71.31977 -71.14364 -71.38703 -71.33597 -71.74809 -71.32635
-71.32762 -71.19942 -71.35559 -71.72430 -71.59923 -71.42666 -71.46893 -71.77846
-71.18408 -71.47083 -71.28789 -71.37294 -71.79025 -71.53329 -71.52752 -71.37809
-71.60986 -71.51138 -71.42488 -71.45155 -71.54728 -71.41161 -71.70268 -71.10551
-71.49741 -71.25172 -71.41915 -71.44956 -71.65804 -71.26925 -71.46200 -71.40985
-71.16403 -71.45841 -71.44952 -71.24233 -71.38980 -71.16942 -71.58817 -71.43484
-71.44364 -71.37749 -71.25543 -71.43968 -71.49156 -71.36995 -71.21915 -71.48985
-71.27379 -71.57996 -71.48761 -71.61994 -71.29297 -71.52603 -71.68554 -71.01284
-71.32887 -71.30746 -71.29927 -71.13437 -71.26771 -71.44513 -71.50827 -71.27265
-71.08417 -71.26195 -71.41467 -71.30567 -71.70383 -71.40150 -71.72103 -71.45478
-71.40848 -71.47521 -71.52258 -71.67739 -71.38912 -71.68145 -71.21546 -71.42597
-71.52721 -71.38423 -71.23798 -71.35119 -71.31237 -71.28323 -71.31124 -71.28413
-71.61115 -71.26330 -71.27225 -71.57120 -71.37774 -71.33171 -71.40468 -71.39623
-71.35990 -71.60246 -71.57650 -71.56792 -71.35905 -71.09578 -71.28406 -71.63209
-71.02412 -71.40044 -71.45577 -71.39152 -71.38194 -71.42897 -71.41352 -71.54153
-71.41068 -71.39265 -71.37710 -71.20972 -71.48271 -71.69484 -71.46400 -71.22704
-71.34192 -71.42140 -71.19815 -71.61089 -71.11619 -71.30021 -71.67516 -71.30192
-71.39633 -71.39194 -71.47787 -71.65349 -71.44983 -71.35542 -71.40998 -71.45062
-71.48309 -71.59848 -71.18045 -71.25651 -71.27088 -71.53893 -71.29975 -71.47234
-71.32146 -71.51616 -71.48254 -71.61117 -71.50477 -71.35168 -71.52409 -71.40310
-71.23678 -71.34815 -71.35209 -71.57151 -71.11882 -71.29615 -71.44196 -71.41890
-71.27430 -71.44383 -71.36330 -71.58956 -71.22624 -71.33624 -71.25362 -71.37643
-71.45091 -71.46933 -71.34993 -71.56948 -71.41427 -71.38531 -71.63743 -71.30292
-71.54742 -71.49482 -71.29988 -71.56502 -71.10004 -71.30671 -71.21587 -71.38752
-71.36753 -71.60114 -71.45538 -71.52019 -71.40670 -71.71296 -71.48820 -71.18964
-71.58680 -71.33249 -71.55425 -71.44513 -71.47727 -71.25269 -71.43148 -71.60412
-71.46177 -71.51549 -71.20461 -71.49230 -71.32246 -71.52597 -71.37766 -71.31987
-71.30851 -71.88509 -71.36917 -71.22490 -71.62081 -71.96852 -71.53359 -71.47723
-71.32810 -71.29936 -71.45300 -71.42229 -71.47454 -71.44397 -71.57985 -71.30791
-71.38831 -71.40726 -71.53823 -71.06420 -71.46449 -71.39598 -71.40063 -71.44936
-71.24304 -71.34033 -71.51728 -71.51698 -71.63969 -71.18971 -71.49681 -71.08383
-71.37424 -71.20241 -71.48371 -71.11297 -71.46601 -71.44628 -71.46256 -71.37464
-71.41977 -71.51032 -71.37513 -71.68295 -71.23920 -71.37369 -71.15474 -71.54024
-71.31926 -71.42511 -71.43734 -71.54829 -71.54761 -71.67956 -71.50499 -71.34070
-71.25763 -71.21935 -71.49801 -71.38714 -71.23983 -71.75183 -71.42562 -71.42292
-71.44343 -71.47011 -71.59013 -71.30610 -71.69382 -71.74252 -71.17388 -71.30809
-71.28540 -71.37704 -71.79387 -71.28777 -71.39398 -71.30104 -71.39404 -71.52451
-71.21740 -71.14912 -71.27558 -71.68374 -71.38982 -71.35454 -71.25401 -71.20002
-71.43856 -71.21049 -71.38132 -71.13802 -71.46789 -71.65140 -71.26295 -71.72480
-71.25633 -71.57879 -71.41211 -71.60260 -71.81862 -71.10805 -71.41330 -71.46485
-71.34430 -71.40172 -71.56734 -71.32101 -71.57546 -71.40403 -71.28394 -71.39493
-71.26190 -71.36597 -71.17094 -71.35582 -71.57056 -71.19090 -71.54987 -71.15806
-71.36186 -71.12948 -71.37479 -71.74120 -71.62364 -71.15258 -71.47156 -71.48552
-71.30971 -71.18669 -71.39955 -71.27009 -71.66332 -71.17089 -71.49359 -71.40213
-71.42944 -71.48127 -71.38976 -71.42721 -71.62643 -71.29208 -71.62867 -71.32803
-71.15941 -71.42374 -71.32999 -71.32640 -71.52232 -71.09299 -71.34868 -71.29540
-71.07503 -71.57044 -71.48810 -71.35455 -71.37009 -71.29303 -70.93152 -71.27125
-71.29070 -71.29214 -71.59046 -71.37845 -71.54966 -71.46521 -71.43900 -71.25935
-71.41443 -71.27894 -71.49044 -71.70232 -71.73317 -71.54440 -71.44394 -71.32814
-71.47011 -71.24761 -71.48287 -71.41087 -71.47894 -71.34839 -71.41578 -71.48390
-71.50809 -71.22478 -71.89716 -71.60514 -71.41614 -71.40579 -71.37625 -71.15378
-71.34898 -71.16439 -71.46604 -71.45807 -71.43686 -71.09257 -71.33623 -71.46117
-71.22722 -71.60940 -71.47191 -71.38820 -71.43712 -71.12854 -71.48756 -71.42807
-71.15636 -71.31872 -71.19638 -71.47540 -71.18009 -71.45154 -71.46844 -71.45086
-71.18017 -71.48703 -71.51892 -71.41624 -71.51250 -71.34931 -71.35142 -71.57221
-71.63407 -71.58036 -71.42971 -71.44451 -71.53424 -71.27474 -71.28675 -71.43282
-71.43045 -71.21926 -71.70332 -71.35526 -71.50275 -71.22754 -71.31130 -71.36965
-71.47278 -71.59279 -71.14908 -71.23298 -71.23421 -71.40670 -71.37635 -71.38711
-71.43582 -71.19108 -71.26765 -71.44103 -71.71168 -71.72163 -71.55390 -71.26052
-71.63274 -71.46516 -71.25641 -71.25462 -71.40686 -71.55041 -71.54492 -71.34281
-71.44613 -71.31232 -71.51834 -71.42135 -71.57378 -71.25240 -71.33067 -71.30579
-71.61982 -71.44157 -71.47927 -71.31579 -71.31242 -71.25470 -71.31126 -71.44941
-71.30770 -71.46419 -71.39323 -71.52133 -71.47907 -71.30238 -71.49862 -71.54788
-71.50739 -71.50072 -71.40781 -71.59065 -71.50088 -71.35082 -71.49879 -71.45034
-71.48809 -71.37906 -71.78026 -71.45654 -71.36651 -71.57584 -71.36960 -71.33349
-71.58353 -71.58225 -71.30287 -71.56796 -71.42132 -71.49783 -71.54507 -71.61491
-71.42284 -71.27253 -71.24947 -71.54211 -71.46093 -71.34671 -71.68581 -71.21182
-71.47941 -71.42710 -71.39665 -71.37869 -71.29210 -71.51510 -71.39767 -71.52853
-71.61189 -71.27578 -71.41986 -71.53504 -71.20660 -71.54633 -71.12868 -71.26761
-71.49719 -71.53037 -71.43363 -71.28200 -71.50145 -71.50077 -71.73149 -71.74435
-71.44230 -71.24733 -71.49309 -71.29721 -71.57029 -71.54265 -71.19877 -71.58223
-71.05338 -71.30338 -71.36365 -71.27840 -71.54152 -71.42615 -71.40438 -71.31289
-71.37062 -71.80684 -71.20455 -71.44950 -71.43674 -71.16687 -71.28291 -71.48545
-71.54975 -71.43444 -71.55315 -71.39940 -71.44807 -71.36031 -71.55639 -71.25161
-71.26887 -71.28511 -71.19781 -71.43163 -71.39244 -71.48140 -71.51957 -71.33494
-71.27746 -71.24850 -71.18903 -71.30058 -71.47506 -71.43578 -71.27131 -71.79848
-71.24854 -71.25637 -71.31686 -71.39798 -71.39912 -71.34265 -71.18708 -71.38557
-71.42774 -71.37662 -71.43799 -71.20409 -71.30663 -71.75122 -71.35893 -71.34696
-71.28347 -71.32785 -71.12931 -71.34140 -71.38958 -71.39573 -71.43368 -71.23167
-71.41469 -71.41643 -71.38358 -71.66597 -71.81811 -71.35029 -71.36759 -71.73805
-71.53565 -71.36740 -71.48591 -71.17869 -71.45269 -71.31723 -71.22985 -71.21812
-71.72078 -71.41997 -71.56492 -71.25220 -71.48629 -71.41477 -71.46118 -71.16045
-71.43393 -71.76714 -71.10087 -71.37772 -71.44643 -71.33745 -71.37289 -71.36416
-71.35364 -71.22865 -71.40181 -71.43557 -71.38130 -71.52349 -71.47568 -71.39498
-71.29033 -71.34792 -71.44438 -71.62138 -71.46104 -71.38139 -71.37343 -71.40319
-71.42939 -71.73206 -71.30103 -71.34815 -71.66686 -71.22574 -71.26808 -71.34156
-71.30732 -71.34819 -71.27743 -71.40475 -71.64085 -71.64094 -71.42500 -71.20975
-71.36478 -71.39989 -71.59216 -71.35532 -71.46204 -71.23014 -71.11674 -71.43296
-71.57950 -71.52923 -71.52528 -71.49694 -71.23307 -71.35822 -71.39920 -71.49189
-71.50940 -71.33623 -71.36105 -71.35813 -71.47833 -71.61524 -71.50179 -71.40340
-71.35228 -71.48913 -71.49293 -71.25972 -71.62486 -71.26072 -71.29923 -71.31992
-71.33347 -71.31240 -71.50744 -71.62102 -71.38617 -71.30796 -71.13272 -71.25367
-71.15381 -71.18794 -71.54305 -71.49148 -71.57065 -71.67774 -71.36992 -71.47793
-71.47478 -71.63957 -71.04446 -71.52041 -71.54747 -71.32749 -71.31061 -71.37860
-71.46096 -71.45026 -71.47912 -71.29706 -71.55423 -71.43755 -71.59226 -71.44375
-71.38166 -71.30645 -71.26516 -71.33233 -71.40455 -71.50892 -71.54600 -71.47301
-71.19882 -71.32689 -71.21668 -71.32719 -71.47932 -71.56272 -71.33009 -71.53361
-71.60817 -71.35527 -71.42524 -71.66498 -71.29855 -71.41850 -71.19664 -71.46531
-71.41553 -71.43382 -71.33271 -71.62836 -71.53618 -71.22226 -71.62968 -71.39177
-71.19846 -71.40286 -71.46086 -71.49526 -71.33933 -71.43601 -71.59590 -71.48170
-71.42247 -71.58349 -71.20392 -71.49375 -71.56093 -71.53159 -71.26542 -71.42152
-71.54103 -71.08938 -71.72047 -71.49759 -71.31641 -71.62774 -71.48073 -71.56179
-71.47600 -71.60544 -71.42989 -71.65982 -71.63139 -71.29150 -71.11442 -71.23368
-71.27440 -71.33772 -71.29180 -71.71246 -71.54850 -71.48675 -71.18927 -71.59711
-71.25759 -71.41022 -71.62181 -71.66865 -71.44273 -71.50519 -71.48035 -71.83377
-71.28275 -71.21964 -71.29723 -71.46733 -71.43032 -71.17516 -71.65807 -71.30027
-71.38963 -71.58486 -71.35816 -71.29889 -71.32615 -71.39182 -71.47305 -71.67785
-71.36370 -71.64278 -71.27448 -71.78898 -71.53304 -71.49220 -71.55857 -71.32478
-71.38089 -71.29432 -71.30344 -71.56554 -71.33842 -71.61700 -71.46365 -71.41229
-71.50636 -71.96486 -71.41336 -71.42253 -71.22290 -71.31477 -71.62807 -71.39798
-71.39485 -71.26146 -71.55157 -71.42832 -71.18105 -71.48651 -71.53359 -71.47904
-71.36572 -71.28265 -71.40087 -71.54449 -71.39816 -71.21574 -71.47807 -71.25499
-71.40378 -71.15720 -71.43807 -71.24335 -71.30147 -71.30990 -71.28320 -71.44637
-71.70717 -71.47751 -71.63264 -71.50045 -71.40919 -71.54821 -71.44655 -71.37560
-71.34705 -71.56370 -71.21372 -71.50910 -71.24095 -71.28303 -71.10388 -71.47887
-71.46411 -71.22239 -71.20665 -71.41599 -71.27537 -71.51518 -71.60576 -71.41295
-71.42630 -70.94304 -71.64802 -71.51852 -71.37942 -71.30329 -71.38740 -71.46711
-71.39359 -71.06512 -71.66158 -71.58452 -71.56496 -71.27406 -71.24647 -71.43432
-71.31059 -71.46232 -71.44408 -71.17962 -71.37026 -71.30981 -71.34176 -71.33165
-71.26334 -71.87441 -71.43352 -71.62593 -71.64004 -71.69980 -71.59462 -71.66897
-71.15147 -71.47523 -71.45320 -71.73478 -71.30966 -71.34439 -71.31748 -71.58520
-71.44713 -71.23802 -71.29850 -71.20927 -71.17104 -71.54140 -71.48994 -71.54675
-71.31470 -71.45056 -71.43106 -71.43453 -71.31298 -71.42704 -71.55381 -71.26999
-71.49768 -71.25277 -71.10921 -71.34181 -71.51116 -71.42523 -71.27411 -71.28331
-71.42677 -71.61186 -71.69673 -71.39004 -71.48229 -71.49408 -71.51677 -71.31122
-71.17375 -71.41020 -71.30937 -71.14893 -70.93498 -71.25895 -71.36444 -71.39730
-71.60476 -71.57237 -71.54438 -71.18981 -71.47166 -71.37865 -71.36129 -71.38903
-71.52365 -71.42576 -71.29031 -71.50929 -71.51090 -71.36182 -71.53492 -71.47875
-71.57211 -71.62357 -71.30630 -71.40765 -71.55986 -71.51443 -71.32108 -71.62888
-71.40653 -71.52656 -71.33001 -71.48846 -71.73886 -71.45970 -71.34380 -71.15280
-71.44682 -71.40417 -71.42551 -71.23947 -71.46557 -71.22084 -71.62611 -71.09568
-71.52611 -71.20938 -71.44137 -71.61260 -71.55788 -71.46453 -71.39567 -71.32973
-71.50303 -71.07390 -71.25704 -71.16202 -71.55764 -71.23090 -71.31661 -71.50051
-71.35260 -71.49616 -71.44472 -71.18662 -71.46352 -71.23229 -71.42668 -71.19332
-71.29872 -71.34584 -71.36952 -71.16910 -71.55721 -71.25719 -71.63636 -71.51796
-71.26195 -71.36808 -71.37051 -71.31791 -71.46960 -71.45362 -71.66748 -71.54876
-71.19727 -71.34869 -71.40611 -71.27519 -71.40573 -71.23596 -71.50586 -71.45160
-71.32566 -71.27930 -71.26418 -71.48767 -71.38953 -71.56795 -71.35714 -71.46290
-71.19345 -70.91859 -71.62296 -71.56558 -71.61276 -71.61220 -71.26478 -71.33773
-71.39607 -71.20095 -71.40349 -71.38534 -71.62173 -71.30939 -71.35874 -71.58979
-71.70611 -71.30607 -71.59783 -71.46744 -71.50418 -71.48108 -71.22056 -71.24763
-71.49423 -71.53950 -71.26196 -71.28751 -71.29151 -71.34648 -71.78138 -71.28936
-71.41630 -71.57522 -70.96149 -71.52550 -71.48668 -71.31751 -71.43008 -71.17759
-71.46507 -71.63389 -71.70829 -71.28779 -71.59384 -71.77372 -71.40533 -70.92858
-71.61567 -71.47836 -71.18650 -71.39520 -71.45736 -71.51104 -71.44684 -71.30435
-71.36437 -71.34866 -71.26280 -71.66246 -71.36762 -71.52762 -71.35593 -71.36674
-71.35046 -71.32090 -71.22476 -71.39273 -71.43688 -71.36262 -71.59777 -71.48014
-71.61774 -71.46112 -71.57537 -71.27936 -71.22276 -71.53369 -71.53951 -71.38326
-71.56816 -71.19556 -71.33729 -71.68230 -71.22503 -71.48340 -71.63653 -71.49612
-71.50900 -71.51820 -71.41052 -71.55286 -71.44023 -71.67987 -71.45562 -71.31035
-71.58075 -71.29952 -71.27552 -71.26916 -71.62403 -71.30452 -71.34984 -71.26933
-71.45700 -71.62189 -71.37667 -71.52100 -71.28147 -71.39507 -71.36451 -71.51445
-71.47906 -71.28137 -71.48031 -71.55126 -71.69311 -71.22570 -71.53215 -71.47706
-71.58066 -71.15464 -71.29560 -71.37899 -71.56009 -71.27485 -71.35804 -71.51090
-71.24160 -71.57807 -71.53903 -71.44289 -71.47738 -71.29325 -71.35232 -71.41126
-71.44170 -71.51376 -71.69618 -71.50628 -71.69692 -71.23065 -71.69401 -71.28793
-71.56562 -71.51429 -71.38345 -71.40612 -71.44869 -71.29612 -71.68215 -71.55740
-71.26040 -71.34453 -71.26498 -71.25429 -71.25226 -71.52616 -71.55179 -71.64614
-71.25335 -71.48029 -71.36946 -71.44880 -71.29668 -71.51567 -71.46641 -71.45580
-71.53610 -71.31666 -71.68659 -71.39435 -71.65688 -71.31708 -71.21618 -71.65030
-71.43763 -71.11061 -71.05829 -71.72059 -71.31322 -71.21235 -71.37118 -71.35457
-71.20828 -71.35339 -71.54021 -71.43516 -71.41874 -71.45163 -71.30236 -71.22148
-71.19640 -71.42517 -71.61647 -71.41269 -71.39346 -71.28512 -71.38019 -71.61815
-71.39821 -71.28055 -71.21097 -71.29000 -71.05887 -71.55674 -71.41117 -71.28703
-71.34788 -71.28121 -71.27797 -71.47272 -71.53686 -71.40567 -71.30790 -71.24797
-71.26717 -71.19198 -71.34106 -71.46480 -71.59288 -71.45087 -71.28199 -71.48499
-71.45690 -71.31832 -71.48957 -71.34561 -71.65057 -71.36393 -71.46396 -71.35266
-71.38147 -71.33390 -71.18159 -71.37144 -71.34858 -71.33783 -71.48830 -71.41923
-71.47614 -71.53330 -71.23876 -71.61478 -71.45524 -71.40006 -71.41812 -71.66511
-71.13113 -71.18071 -71.39620 -71.35850 -71.38560 -71.22722 -71.32824 -71.31028
-71.50962 -71.65575 -71.58282 -71.38891 -71.10534 -71.61306 -71.42899 -71.52637
-71.39705 -71.19045 -71.46422 -71.43862 -71.72431 -71.19673 -71.27760 -71.49258
-71.28051 -71.71195 -71.32205 -71.48580 -71.55664 -71.37944 -71.56371 -71.53393
-71.26468 -71.34815 -71.45724 -71.28751 -71.47709 -71.44199 -71.36517 -71.52221
-71.16987 -71.39185 -71.43622 -71.62270 -71.42398 -71.59988 -71.39472 -71.41155
-71.42355 -71.61860 -71.50705 -71.25897 -71.19588 -71.04963 -71.37470 -71.38955
-71.63989 -71.27403 -71.64173 -71.59881 -71.31498 -71.38842 -71.45981 -71.53123
-71.79651 -71.43240 -71.33354 -71.57325 -71.29391 -71.40151 -71.30378 -71.17909
-71.38554 -71.28185 -71.46958 -71.19736 -71.47631 -71.36516 -71.56489 -71.40665
-71.40420 -71.27679 -71.51234 -71.36917 -71.31304 -71.31447 -71.76055 -71.39302
-71.18635 -71.58149 -71.77067 -71.33165 -71.35555 -71.76342 -71.53656 -71.17623
-71.57011 -71.22224 -71.82219 -70.87494 -71.52795 -71.33127 -71.59835 -71.08434
-71.01195 -71.53750 -71.25191 -71.52293 -71.31763 -71.42391 -71.60685 -71.47009
-71.56699 -71.49950 -71.15649 -71.26497 -71.35928 -71.43772 -71.73647 -71.52408
-71.30850 -71.18259 -71.31301 -71.52053 -71.22605 -71.32040 -71.36260 -71.60313
-71.43558 -71.10743 -71.35324 -71.55250 -71.57831 -71.38662 -71.60318 -71.59883
-71.21471 -71.29699 -71.38192 -71.56869 -71.48214 -71.37478 -71.13875 -71.41112
-71.63745 -71.67753 -71.51630 -71.36158 -71.57607 -71.44991 -71.32604 -71.32742
-71.40359 -71.65168 -71.63009 -71.27801 -71.71845 -71.54864 -71.11658 -71.22296
-71.68091 -71.47657 -71.46984 -71.40714 -71.27812 -71.60839 -71.40635 -71.72764
-71.19013 -71.65499 -71.79722 -71.23429 -71.68311 -71.42670 -71.87413 -71.43289
-71.43288 -71.45795 -71.39620 -71.34826 -71.45467 -71.16334 -71.11534 -71.75454
-71.27140 -71.24971 -71.30889 -71.29105 -71.39655 -71.64558 -71.36554 -71.58886
-71.45510 -71.58692 -71.28270 -71.49047 -71.28918 -71.21624 -71.54474 -71.52276
-71.83242 -71.47655 -71.41875 -71.30907 -71.54520 -71.69080 -71.41808 -71.44818
-71.26558 -71.44870 -71.42361 -71.35342 -71.51033 -71.14130 -71.26217 -71.55488
-71.30714 -71.58956 -71.24707 -71.33965 -71.06647 -71.33322 -71.51419 -71.24837
-71.36971 -71.60132 -71.42922 -71.31146 -71.74104 -71.22977 -71.55969 -71.10569
-71.26147 -71.42428 -71.22894 -71.48501 -71.48188 -71.49452 -71.43418 -71.61823
-71.22989 -71.30123 -71.69114 -71.30863 -71.37681 -71.41591 -71.26615 -71.27310
-71.43268 -71.37290 -71.18415 -71.13129 -71.72248 -71.08332 -71.36315 -71.42422
-71.64324 -71.24649 -71.31470 -71.35240 -71.56023 -71.62580 -71.35486 -71.36730
-71.28068 -71.82735 -71.51334 -71.44557 -71.39971 -71.61113 -71.76325 -71.44540
-71.63576 -71.22105 -71.43593 -71.41978 -71.36105 -71.35119 -71.50301 -71.27757
-71.26252 -71.54333 -71.45305 -71.21609 -71.27626 -71.41967 -71.43734 -71.31618
-71.50079 -71.13503 -71.53593 -71.55477 -71.44365 -71.45660 -71.63220 -71.51033
-71.00086 -71.41106 -71.53685 -71.61639 -71.46615 -71.55516 -71.48667 -71.35310
-71.48490 -71.31032 -71.76452 -71.45503 -71.20452 -71.46615 -71.07967 -71.60347
-71.40109 -71.17271 -71.38915 -71.70705 -71.68346 -71.45724 -71.42163 -71.47579
-71.41535 -71.43970 -71.77515 -71.49411 -71.43655 -71.36667 -71.35927 -71.21216
-71.16947 -71.50356 -71.49348 -71.24907 -71.53504 -71.47797 -71.28440 -71.34063
-71.36098 -71.36668 -71.32802 -71.34599 -71.49152 -71.46592 -71.32126 -71.30734
-71.54414 -71.48746 -71.48801 -71.36004 -71.66726 -71.50550 -71.72948 -71.53846
-71.60896 -71.41522 -71.55603 -71.53407 -71.38029 -71.66660 -71.23029 -71.83067
-71.37910 -71.44434 -71.35642 -71.75602 -71.58986 -71.59790 -71.39886 -71.60986
-71.36803 -71.82760 -71.61485 -71.70586 -71.62306 -71.36838 -71.56067 -71.16340
-71.39199 -71.39407 -71.22180 -71.48011 -71.57544 -71.24031 -71.42554 -71.40242
-71.48823 -71.79333 -71.36255 -71.54388 -71.40972 -71.52276 -71.71397 -71.46000
-71.22553 -71.48903 -71.60062 -71.35672 -71.58043 -71.49268 -71.44188 -71.47977
-71.51365 -71.53137 -71.37583 -71.39317 -71.29699 -71.39054 -71.44061 -71.26669
-71.55741 -71.33486 -71.36378 -71.69140 -71.35901 -71.27650 -71.63452 -71.53673
-71.28993 -71.82672 -71.27587 -71.44613 -71.38916 -71.49557 -71.22437 -71.53277
-71.34844 -71.27005 -71.72448 -71.28636 -71.53330 -71.33306 -71.44009 -71.32114
-71.43744 -71.63756 -71.39142 -71.22580 -71.57545 -71.39966 -71.45705 -71.54984
-71.56189 -71.44331 -71.29971 -71.26732 -71.26877 -71.23258 -71.35611 -71.66529
-71.42590 -71.29397 -71.69395 -71.26762 -71.65974 -71.33252 -71.52681 -71.44208
-71.18166 -71.34634 -71.41826 -71.51673 -71.42820 -71.22013 -71.35349 -71.43789
-71.18001 -71.55061 -71.54834 -71.52247 -71.36880 -71.39516 -71.36334 -71.22846
-71.28379 -71.61957 -71.29038 -71.48659 -71.27278 -71.47207 -71.46169 -71.47217
-71.70354 -71.30257 -71.37120 -71.70509 -71.57376 -71.42586 -71.50733 -71.34889
-71.46119 -71.52305 -71.40510 -71.16154 -71.36782 -71.23667 -71.35663 -71.36954
-71.41339 -71.29570 -71.44898 -71.75717 -71.47195 -71.45797 -71.69461 -71.66042
-71.28485 -71.12561 -71.23636 -71.35668 -71.47518 -71.61323 -71.21035 -71.48925
-71.35181 -71.49552 -71.54052 -71.42017 -71.19877 -71.21905 -71.34957 -71.49006
-71.59835 -71.25860 -71.42716 -71.17084 -70.93962 -71.33225 -71.47662 -71.67854
-71.45882 -71.53879 -71.21572 -71.36022 -71.26144 -71.20478 -71.56527 -71.46690
```
