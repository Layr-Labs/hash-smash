# Collision attack on 37-step SHA-256: the ePrint 2026/1120 two-block attack over the whole variant family G, with an x-indexed table of merged W6 fibres, accepting the four feasible value patterns of rows 18 and 19 and every collision that follows rows 16..21, 2^60.16722

Track `sha256-r37-exploratory`, target `sha256-r37-prefix-v1`, cost model `collision-frontier-v5` (C = 2644).
Claim: `time_log2 = 60.16722` target compressions on every run, success probability at least 0.39 (0.3900000041 under the stated premises),
memory 2^52.1 bytes (reported only), nonuniform advice below 2^13 bytes.

**Credited derivative of Jbenisek's fcbc9c83-9032-4f79-a712-05f0705d24b9 (60.17144), our fe65a7cb-1504-4f2e-9b2f-9f1adf068b01 (60.37819), Jbenisek's ffbe30bb-ac92-4191-a589-3bf32661ee7d (60.38707) and our 7c46d8cb-aaaf-48a8-bc3e-705c2ef339a2 (61.12049)**, which build on 0xshikhar's fb039a6e-7dc6-4c2e-b2a7-aa0fb4cfcb91 (61.14135) and c3041753, with their lineage (Section 2): Th0rgal's 0db0eeb6 (61.17784), companygardener's d3ec5c41, 44921815 and 8de337d5, winglock's 6c77089c and 7319bba, GordoAR's 087a18c4,
itseasypop's 1c368173, qkniep's b947b377, 0xshikhar's 1f12a09a, Th0rgal's dd6656d and f2fe1d4d, Jbenisek's 8aeaed1c, def128fc and c22f86a2, and 6eeefb64 for the price of a solver CPU-second. The attack, the characteristic, the sets F6, F7, L*, the family of A0-variants and its classes,
the x-indexed table of merged fibres, the packed good-pair arithmetic, the rows 16..36 check, the counted program, the allowances A_C = 2^60, A_S = 2^50 and DEV = 2^40, the premises H1, H3-H9 and the ledger structure are fb039a6e's; the acceptance of four value patterns of rows 18 and 19 and the cell factor 2^-72.04 of q3 are ffbe30bb's; the collision event after row 21, the Bernstein work-cap bound and the rare path charged as executed are fcbc9c83's; the tightened online operation counts (Section 9) are 7c46d8cb's and fe65a7cb's.

**What this filing changes: combining fcbc9c83's collision-event acceptance and Bernstein cap bound with 7c46d8cb/fe65a7cb's tightened online operation counts.** ffbe30bb accepted a pair only if rows 16..36 followed every printed cell and two-bit condition. A collision needs less: the two 37-step outputs must be equal.
The counted program now checks rows 16..21 cell by cell as before, computes rows 22..36 of both members with no cell test, and accepts the pair iff the two outputs are equal (16 more operations; the same comparison every output is verified with). Given rows 16..21, the collision event is small and exactly described: E22[29] = 1,
s1(W22') - s1(W22) = 0x4fff9f30 (75 x 2^17 words W22, against the 2^22 allowed by the printed cells and two-bit conditions of W22), the W24 condition (17 x 2^24 words against 2^28) and dW26 = 0 (17/256 against 16/256); uniform-model ratio 1275/512 = 2.49 (Appendix D.2).
q3 is therefore ffbe30bb's cell factor 2^-72.04 times R = Pr[equal outputs | rows 16..21] / Pr[cells of rows 22..36 | rows 16..21], charged at **R = 2.4331**: the one-sided 99 percent Clopper-Pearson lower bound from three runs on ffbe30bb's own row-21 states (402,680 equal-output events against 164,011 cell events in 5 x 2^30 late proposals; every cell event was also an equal-output event; point estimate 2.4552),
fixed by a rule preregistered before the third run, under which the third run could only lower the value (Appendix D.3). The cell factor and R are separate one-sided 99 percent bounds, so their product holds with probability at least 98 percent; R was measured with W6, W7 uniform on F6 x F7 and W8 from the whole variant family, and the third, preregistered run alone gives 2.4502 (with its seed-to-seed overdispersion allowed for, 2.4445), above the charged value. The work cap is bounded by Bernstein's inequality instead of Chebyshev's (same premises, slack 1/3680; Appendix D.4), the rare path is charged as executed (row 16 is not re-checked because the row-16 mask lookup is its exact enumeration; rows 22..36 carry no checks; Appendix D.5), and the online operation counts incorporate 7c46d8cb/fe65a7cb's tightenings (`ZPLANE_OPS = 66`, `CVPRE_OPS = 73`, `FBFIX = 195`, `SCAN_LANE = 5`, `SEG_OVH = 4`, `GROUP_OPS = 30`, `GROUP_FULL = 44`, `UNROLL = 32`, `LOOP_SEG = 13`, Section 9).
`time_log2` falls from 60.38707 to 60.17144 in fcbc9c83 and to **60.16722** here (Section 16a, Appendix C). The organizer experiment `a0-sfs-r37` now accepts its constructions by equal outputs: 85 of its 128 collisions in our local replay lie outside the printed cells of rows 22..36, and the counted program finds every constructed pair it is given (16 of 16, 12 of them outside the cells).
**Organizer-run evidence for H1 and H3, and R under the attack's own law of the late words (Section 13.6, Appendix D.3b).** `a1-cv-r37` (H1): on 6,144 real first blocks whose chaining values are the organizer's own digests, the organizer-checked four-plus-four-bit coincidence of x and A_{-2} holds in 175 of 256 trials (Binomial(256, 0.67134): mean 171.9, sd 7.5) and the filter inputs hit their exact rates. `a3-dep-r37` (H3): given 32 constructed successes, 65,251 other good pairs of their chaining values give 16 row-16 passes (16.0 expected unconditionally), none reaching row 17; the matched control `a3-ctl-r37` gives 14 among 65,536 (16.1). These are tests at the stated scale, not at 2^51.78. R under the attack's kept-fibre law of (W7, W8) (preregistered, 2^32 late proposals): 2.46455, overdispersion-robust 99 percent bounds 2.4515 and 2.4520 (2.4464 and 2.4408 on the runs with W7 uniform); the charge 2.4331 is below all of them, and the ledger, N_FB and `time_log2` are unchanged.
**What ffbe30bb changed (kept here) is one acceptance rule and the q3 that follows from it.** Table 15 fixes eight value bits in the E cells of rows 18 and 19: E18[1] = 1, E18[5] = 0, E18[10] = 1, E18[11] = 1, E18[18] = 0, E18[28] = 0, E18[29] = 1 and E19[29] = 1
(bits counted from the least significant bit, 0). They are not all required: with every other cell and every printed two-bit condition of rows 4..36 kept, the 37-step semi-free-start system has exactly **four** solutions for these eight bits
(Appendix B.2: exhaustive all-solutions enumeration; three further verified 37-step semi-free-start collisions with the three other patterns), because the bits enter only through six parity conditions: E18[1] = E18[11], E18[1] != E18[28], E18[10] = E18[29], E18[10] = E19[29], E18[5] = E18[18], E18[5] ^ E18[1] ^ E18[10] = 0.
The counted program no longer imposes the eight values (its exact signed-difference checks of both members, which it always made, decide), so a pair that follows the cells with any of the four patterns is a collision and is accepted (Appendix B.1). The q3 of premise H2 is re-measured with the base filing's own program `smc.c`, byte-identical,
and the same parameters, replicates and bounds, with the eight characters changed in `lab.h` and nothing else (Appendix B.3; three studies preregistered before any listed seed ran): the bounds are 2^-72.0129 (all of G), 2^-72.0367 (kept-fibre-weighted pool) and 2^-72.0155 (stratified per x), and the charge is q3 = 2^-72.04 instead of 2^-74.02, **1.98 bits more probable**.
Combining ffbe30bb's q3 = 2^-72.04 with 7c46d8cb/fe65a7cb's tightened online operation counts (Section 9) gave `time_log2 = 60.37819` in fe65a7cb, and with fcbc9c83's collision event, Bernstein cap bound and rare-path execution charge gives `time_log2 = 60.16722`.


The attack is the 37-step collision attack of Li, Zhang, Li, Liu, Qian and Zhu, "Pushing Collision Attacks on SHA-2 to 39 Steps" (IACR ePrint
2026/1120, CC BY), in the two-block framework of [LLWS26] (ePrint 2026/1080), with the A0-variants of its Step-1 solution (itseasypop 1c368173,
qkniep b947b377), the packed good-pair stage of 1f12a09a, the exact-rational ledger of 087a18c4 and the program structure of 7319bba (all declared as
dependencies). It builds on companygardener's d3ec5c41 (61.71473), 44921815 (61.20057) and 8de337d5 (61.19411), and on the derivatives credited below
(8aeaed1c, def128fc, f2fe1d4d, c22f86a2). (fb039a6e's own changes to 0db0eeb6 were the register residency of the bit-sliced addition, the fibre threshold and the q3 evidence; they are the base of this filing and are described in the text below as the base's.)

*The idea.* The 32-bit value x = A_{-1} of a chaining value takes only 2^32 values, while the run draws about 2^55 first blocks: every x recurs about 2^23 times.
Everything that depends on x alone is computed once for all x (charged preprocessing, below 2^58 operations; memory is a reported metric only) and read online:
(i) the W7 class test becomes one table read; (ii) the values phi(a0, x) = W6x - cb of **all** variants whose c7-class passes W7 at x are partitioned into **fibres** of equal value, whatever their class;
(iii) only fibres of at least THETA = 48 variants are kept; (iv) online, the W6 filter is one bit-sliced 32-bit addition of the scalar cb to the fibre values of 256 lanes followed by the F6 test, and the members of
every passing fibre are read in place by the packed 4-lane stage. Before, the table was restricted to the 222 largest classes (782,800 variants) and fibres were per class (about 12 variants each);
the lower per-pair cost of large fibres makes it worthwhile to examine 119,869 variants per first block (on average) out of the whole family G (12,103,680 variants in 22,976 classes), so a first block yields
7,971 good pairs instead of 831 and N_FB falls by a factor of about 9.6 while the work per good pair falls too. The set of good pairs found among the examined variants is *exactly* the set defined by the
filters (Lemma 8.1, checked against brute force in Section 13).
**Measurements of the base filing, stated up front (Table 15 value pattern only; this filing's own studies are in Appendix B.3):** the Monte-Carlo estimate of q3 (premise H2) was measured directly on the examined family: a preregistered 128-replicate study over the whole family G
(12,103,680 variants) gives a one-sided 99% Student bound of 2^-74.0088, a preregistered 64-replicate study over a kept-fibre-weighted pool of 9,090,990 variant draws (the actual examined
distribution of 64 uniform values of x) gives 2^-73.9984, and a stratified 160-replicate study over the same pool's per-x files gives a cluster ratio-estimator bound of 2^-74.009 that also covers the
finite-64-x sampling error; the base charged q3 = 2^-74.02 for the Table 15 pattern, 0.011 bit below the examined-law bound (Section 7.6). The evidence for H3 remains 7319bba's (stated for the
new family in Section 7.6).

## 0. Summary

- **Algorithm (Sections 4-8).** Messages M0 || M1 and M0 || M1' (128 bytes; padding adds the same third block). A first block M0 is two fresh uniform 256-bit
  words; CV1 = F_37(IV, M0) costs one unit. One table read at x = A_{-1} returns the record R(x): the kept fibres (at least THETA = 48 variants with equal phi) of the variants of G whose class passes c7 - x in F7, as
  bit planes of the fibre values, fibre entries and contiguous member blocks. For each batch of 256 fibres the program adds cb = C6 - A_{-2} to the fibre values bit-sliced and applies F6; the members of each passing fibre are good pairs.
  They are processed in packed groups of four: u = W0 + s0(W1) and an exact row-16 mask-table lookup over the 32 elements of L* for every lane; each row-16 pass is checked cell by cell through row 21 and computed through row 36,
  and the pair is accepted iff the two 37-step outputs are equal (Appendix D); it is verified with the target and output.
- **Rates.** Per first block (means over uniform x, Tungsten, Section 13.3): 1,163.1 kept fibres, 119,869 kept variants, hence g = p6 x 119,869 / 1.006 = 7,971 examined good pairs (a lower bound)
  (p6 = |F6|/2^32 = 2^-3.90197; the statistics are scaled by 1.006 in the unfavourable direction).
- **Probability (Sections 7.1, 7.7, Appendices B and D, H2).** q3 = average over the examined variants and l in L* of Pr[rows 16..21 follow every cell and printed two-bit condition, the eight value bits of rows 18 and 19 not imposed, and the two 37-step outputs are equal]
  = at least 2^-72.04 x 2.4331 = 2^-70.75720: the cell factor 2^-72.04 (ffbe30bb's three preregistered SMC studies, Appendix B.3: 2^-72.0129 on the whole family, 2^-72.0367 pooled and 2^-72.0155 stratified on the examined distribution; Table 15 pattern alone: 2^-74.02) times 2.4331, below every overdispersion-robust 99 percent lower bound on the ratio of the collision event to the cell event of rows 22..36 (Appendix D.3, D.3b; point estimates 2.4552, and 2.4646 under the attack's kept-fibre law of (W7, W8)).
- **Cost (Sections 9, 11).** N_FB = 3,869,961,979,885,410 first blocks (2^51.78124); per first block 1 unit plus 195 counted data-independent operations, plus on average
  93,087 counted data-dependent operations (1,504 for fibre tests, 704 for scans, 89,863 for the packed groups and row-16 lookups, 1,016 for rows >= 16), capped by V_MAX. T = A_C + A_S + DEV + N_FB + (N_FB x 195 + V_MAX + overshoot + preprocessing + final)/C + 6 = 3,422,921,269,986,078,257,473 / 2644 = 2^60.167212,
  claimed 60.16722. fcbc9c83 claims 60.17144; fe65a7cb claims 60.37819; ffbe30bb claims 60.38707; 7c46d8cb claims 61.12049; fb039a6e claims 61.14135.
- **Premises (Section 12).** H1 uniform independent chaining values (organizer experiment `a1-cv-r37`, Section 13.6); H2 q3 >= 2^-72.04 x 2.4331 for the examined family with the four row-18/19 patterns accepted and success the collision event (preregistered studies, Appendices B.3 and D.3); H3 given one success, at most 2^-9.4 further expected successes in the same
  first block (inherited, stated for the new family; organizer experiments `a3-dep-r37` and `a3-ctl-r37`, Section 13.6); H4 advice allowances (A_C = 2^60, A_S = 2^50, DEV = 2^40, as in the accepted filings); H5 counted word-RAM pricing (every executed primitive costs one, address additions included; memory is reported only); H7 the exact success floor of 087a18c4 (with Bernstein's bound for the work cap);
  **H9 the table statistics and the preprocessing bound**. No decision-DAG branch pricing is used.
- **Checks (Section 13, Appendices B and D).** The collision event: the W22 set of 75 x 2^17 words counted over all 2^32 words and enumerated as 10 disjoint affine pieces (Appendix D.2); three runs in which every cell event was also a collision (Appendix D.3); the organizer experiment `a0-sfs-r37` accepts by equal outputs (128 of 128 trials in our replay, 85 outside the printed cells of rows 22..36, 16 of 16 found by the counted program). Exhaustive in Tungsten: |F6| = 287,309,824 and |F7| = 68,157,440 and their bitwise forms against the definitions on all 2^32 words (0 mismatches),
  |G| = 12,103,680 and its 22,976 classes; the table pipeline against brute-force filtering (selftest and organizer experiments, 0 mismatches); the fibre statistics over 3,200,000 uniform values of x (Tungsten, sixteen shards);
  an end-to-end Tungsten simulation of the counted program over 480,000 further values of x against the ledger; the executable counted program (Python) on real first blocks restricted to the 222 embedded classes; 37-step semi-free-start constructions with variants found by the counted program.
  The patterns of rows 18 and 19: the base filing's three solver-checked claims re-run (the exhaustive all-solutions enumeration over the eight bits, three verified 37-step semi-free-start collisions with the other three patterns; Appendix B.2), the four patterns constructed by the organizer experiment `a0-sfs-r37` (trial t imposes pattern t mod 4;
  in ffbe30bb's replay 127 of 128 trials built a verified collision, 16 of 16 found again by the counted program), and the SMC stage counts (Appendix B.3).

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

- **This filing.** A credited derivative of Jbenisek's fcbc9c83-9032-4f79-a712-05f0705d24b9 (60.17144), our fe65a7cb-1504-4f2e-9b2f-9f1adf068b01 (60.37819), Jbenisek's ffbe30bb-ac92-4191-a589-3bf32661ee7d (60.38707) and our 7c46d8cb-aaaf-48a8-bc3e-705c2ef339a2 (61.12049). It combines fcbc9c83's collision event as the success event of the counted program and of q3, Bernstein cap bound, rare path charged as executed, organizer experiments `a1-cv-r37`, `a3-dep-r37` and `a3-ctl-r37`, and run of R under the kept-fibre law (Sections 9.7, 10, 11, 12, 13.2, 13.6, 16a, Appendix C and Appendix D) with 7c46d8cb/fe65a7cb's tightened online operation counts (Section 9). fcbc9c83, fe65a7cb, ffbe30bb, 7c46d8cb and their lineage are declared as dependencies. Appendix B is ffbe30bb's record, kept as ffbe30bb filed it.
- **The base, ffbe30bb.** ffbe30bb is a credited derivative of 0xshikhar's fb039a6e-7dc6-4c2e-b2a7-aa0fb4cfcb91 (61.14135). The text of Sections 1-16 and Appendix A is fb039a6e's proof, with "this filing" in those passages meaning fb039a6e unless a passage says "this derivative"; the numbers that this derivative changes (In the text kept from ffbe30bb, "this derivative" means ffbe30bb; the passages added by this filing say "this filing" and are listed in the bullet above.)
  (q3, N_FB, V_MAX, mu0, Pcap, the claim and the quantities of the ledger) are replaced in place, and everything that is the base's own record (Sections 7.4-7.6, Appendices A.8 and A.13: the studies of the Table 15 pattern) is left as the base reported it. The derivative's own material is Section 7.7, Section 16, Appendix B and Appendix C.
  The lineage is declared as dependencies: fcbc9c83, fe65a7cb, ffbe30bb, 7c46d8cb, c3041753, fb039a6e, 0db0eeb6, 6c77089c, 7319bba9, dd6656d4, 1c368173, b947b377, 087a18c4, 1f12a09a, d3ec5c41, 44921815, 8de337d5, 8aeaed1c, def128fc, f2fe1d4d, c22f86a2 and 6eeefb64.
- [LZLLQZ26] Y. Li, Z. Zhang, M. Li, F. Liu, H. Qian, J. Zhu, "Pushing Collision Attacks on SHA-2 to 39 Steps", IACR ePrint 2026/1120: the 37-step characteristic (Table 15), its two-bit
  conditions (Table 16), the 37-step SFS pair (Table 17) and the three-step attack (Step 1: SAT solve of the dense part, 2^41.3; Step 2: random first blocks filtered on W6, W7; Step 3: the
  (W14, W15) freedom). [LLWS26] Y. Li, F. Liu, G. Wang, J. Shi, ePrint 2026/1080 (the framework); [LLW24] EUROCRYPT 2024 (the tool).
- Filings on this track (all declared as dependencies; 6eeefb64 belongs to the sha256-r32 track and is only cited for a measured price): 6c77089c (winglock, 74.22669): transcription of Tables 15-17, member orientation, the reading of '+', the corrected two-bit condition
  A15[29] = A17[29], the exact Step-2 sets F6, F7, the exact set L* (|L*| = 32), the SMC design for q3. dd6656d (Th0rgal): affine decomposition of F6, F7. 1c368173 (itseasypop) and b947b377 (qkniep):
  the A0 freedom of the Step-1 solution (the family G), the c7 classes. 087a18c4 (GordoAR): exact-rational ledger, premises H1-H5, H7, the first-block-level success analysis. 1f12a09a (0xshikhar):
  packed groups of four 64-bit lanes. 7319bba (winglock, 62.34263): the program structure, the packed good-pair program, the
  q3 studies for the 222-class family (Section 7.4), the end-to-end and replay statistics (Section 13.1, quoted), the registered allowances. 6eeefb64 (sha256-r32, promoted): the calibrated price of a solver CPU-second
  behind A_C. d3ec5c41, 44921815, and 8de337d5 (companygardener, 61.71473, 61.20057, 61.19411): the x-indexed table over all 22,976 classes, fibres merged across classes of equal W6 value, the bit-sliced fibre test, the Tungsten statistics, and the exact ledger.
  Derivatives of d3ec5c41: 8aeaed1c, def128fc, and c22f86a2 (Jbenisek: the row-16 l-mask stored directly per value u, one load per lane; no presence word; cap slack squared in Chebyshev), f2fe1d4d (Th0rgal: MAJ(a0, A_{-1}, A_{-2}) = (a0 & (A_{-1} ^ A_{-2})) + (A_{-1} & A_{-2}) with the second term folded into kap1; unmasked first additions; factoring of w[8] ^ w[25] out of the F6 test).
- **How the earlier material is used.** Sections 3-7 restate definitions and lemmas that all filings share. The statistics of Section 13.1 were produced by 7319bba's author with programs reproduced in Appendix A.7-A.10; they enter only as the premise H3. The Monte-Carlo estimate of q3 (premise H2) is measured here on the examined family itself (Section 7.4b).
- **New here.** Building on 0db0eeb6 (61.17784), which packs each 4-member group into one 256-bit word `Gw`: (i) the 32 broadcast planes `z_j = 0 - ((cb >> j) & 1)` of the bit-sliced addition are now **register-resident across the whole batch loop** — they are built once per first block (66 operations: `z_0 = 0 - (cb & 1)` in 2 ops and for `j = 1..31`, `cb_j = cb >> 1` and `z_j = 0 - (cb_j & 1)` in 3 ops only for `j < 31` since `cb_31` is already 0 or 1, saving 29 shifts) and kept in registers, because at most 26 values are live in the adder and the F6 phase and 32 + 26 <= 64 — the per-batch overhead drops from 71 to 8 operations and the fixed charge from 264 to 195 (with `CVPRE_OPS` = 73); (ii) the fibre threshold is re-optimized under the reduced costs, `THETA` from `40` to **`48`** (Section 13.3); (iii) **q3 is measured on the examined family**: a new preregistered 128-replicate SMC study over the whole family G gives the bound 2^-74.0088, a new preregistered 64-replicate study over a kept-fibre-weighted variant pool of 9,090,990 draws (64 uniform x values, the actual examined distribution) gives 2^-73.9984, and a stratified 160-replicate study over the same pool's per-x files gives a cluster ratio-estimator bound of 2^-74.009 that also covers the finite-64-x sampling error, supporting `q3_model = 2^-74.02` with 0.011 bit of margin; (iv) the segment scan and unrolled group loop are tightened (`SCAN_LANE` = 5, `SEG_OVH` = 4, `GROUP_OPS` = 30, `GROUP_FULL` = 44, `UNROLL` = 32, `LOOP_SEG` = 13). Together with ffbe30bb's `q3 = 2^-72.04` and fcbc9c83's collision event (`EXQ = 2.4331`), Bernstein cap bound and rare-path execution charge: `T = 2^60.167212` (**`60.16722`**).

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

In this table rows 18 and 19 are the paper's. This derivative's program keeps the cells of every row but does not impose the value bits E18[1,5,10,11,18,28,29] and E19[29] of those two rows (the characters `1`, `0` there); the four patterns it accepts are listed in Appendix B.1.

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
taken from all 22,976 classes (on average 119,869 variants per first block at THETA = 48). The 222 classes of the earlier filings stay embedded in `xtab.py` (descriptors below) because the organizer sandbox (128 MiB, 20 s) cannot hold the whole family:
the organizer experiments run the same program with the table restricted to these classes and a smaller THETA (Section 13.2). Each of the 222 classes equals {base XOR s : s subset of mask, s in G, c7 = the class value}
for the descriptors below (c7, base, mask, size; `xtab.py` regenerates all 222 classes from them and asserts the sizes; it stores the descriptor text, one line per class in this order, as zlib + base85 in `CLASSES_Z` and asserts its SHA-256, 22ac1c38a055492a6679aaf735ece4f42d029065f806fab6021840fea1f479e7):

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


(For ffbe30bb the event F_l of the next paragraph is the same except that the eight value bits of rows 18 and 19 are not imposed; Section 7.7. **For this filing F_l is: rows 16..21 follow every cell and printed two-bit condition closing at rows 16..21 (the eight value bits not imposed) and the two 37-step outputs are equal**; Appendix D. Sections 7.4-7.6 report fb039a6e's studies of the Table 15 pattern.)
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


### 7.3 The estimator (7319bba's `smc.c`, Appendix A.7; byte-identical program, re-run here on this filing's family)

Stages: row 16 exact (the enumeration of 6.2: the stage mean is (1/32) sum_l |R16_l| / 2^32 = 2^-16.994, and the initial particles are drawn exactly from the passing (l, E16) pairs);
rows 17..21: each child proposes E_t^x uniformly with the row's fixed x-bits imposed (exact importance weight 2^-f), sets W_t^x = E_t^x - (the rest of step t), W_t^y = W_t^x + its exact
difference, and checks the whole row; row 22: (W6, W7) drawn uniformly from F6 x F7; rows 23..36: W8 of a variant drawn uniformly from the variant list passed to the program (the same row-22 survivor
is also evaluated with the published W8 for a paired comparison). NP particles, M children per particle per stage, MT tail proposals per particle, multinomial resampling of the survivors after
every stage; the product of the stage means is an unbiased estimator of q3 (the standard SMC normalising-constant estimator). The design is 6c77089c's and 087a18c4's; the program of Appendix A.7 is
7319bba's (`smc.c`, sha256 `685297129cda47b247e6d19b1799d73b198e1511334e161fa7583ef6c1175a65`, byte-identical to the registered studies, verified by hash; it takes the variant list as a command-line
file, so no program change was needed). **This filing runs it twice** (Section 7.4b): once over the whole family G, once over the examined distribution itself.

### 7.4 The registered studies of 7319bba (reported unchanged)

**Study A** (registered 2026-10-10T08:11:18Z, before any listed seed ran): NP = 2048, M = 512, MT = 16384, 32 replicates; rule: the one-sided 99% Student lower bound of the mean of the 32 linear
estimates (t = 2.4528, 31 df), q3_model = 2^(floor(100 log2 LB)/100). Result: mean 2^-74.0187, relative standard deviation 0.0743, lower bound 2^-74.0659, q3_model(A) = 2^-74.07.
**Study B** (registered after study A had been read, to tighten the spread; same program, NP = 8192): mean 2^-73.9987, relative standard deviation 0.0378, lower bound 2^-74.0225,
**q3_model = 2^-74.03 (the base of the earlier filings' charge)**. All 32 replicates of study B (log2):

```text
-74.022 -73.967 -74.038 -73.934 -74.032 -74.059 -74.000 -74.017 -74.043 -74.070 -73.984 -73.942 -73.949 -73.956 -73.853 -73.965
-74.109 -73.985 -73.979 -73.927 -74.027 -73.983 -73.990 -74.065 -73.925 -74.057 -74.071 -74.052 -74.001 -74.025 -73.984 -73.976
```

| quantity | study A (NP 2048) | study B (NP 8192) |
|---|---|---|
| mean | 2^-74.0187 | 2^-73.9987 |
| relative standard deviation | 0.0743 | 0.0378 |
| 99% lower bound | 2^-74.0659 | 2^-74.0225 |
| **q3_model** | 2^-74.07 | **2^-74.03 (the base of the earlier filings' charge)** |
| stage means (log2) | 16: -16.994, 17: -13.000, 18: -15.004, 19: -6.000, 20: -7.001, 21: -1.000, 22: -11.009, tail -4.015 | 16: -16.994, 17: -13.000, 18: -15.001, 19: -6.000, 20: -7.000, 21: -1.000, 22: -10.998, tail -4.007 |

The stage factors equal, within 0.01 bit, the per-row condition counts of the printed tables (17, 13, 15, 6, 7, 1, 11, 4; 74 in total). With study A's value this filing's claim would be
61.16883 (Section 11.2).

### 7.4b The studies of this filing (new; preregistered; on the examined family)

The registered studies drew W8 uniformly from the 782,800 variants of the 222 largest classes. This filing examines the variants of kept fibres (at least THETA members) of all 22,976 classes — a
size-biased subset of the same family. Two new preregistered studies with the byte-identical program of A.7 (same parameters NP = 8192, M = 512, MT = 16384 as study B) measure it directly:

**Study G** (all-G uniform; registered before any listed seed ran, Appendix A.13): the variant list is the whole family G, generated by `genvar.c` (12,103,680 variants; the list re-checked: every
entry in G, the T8 and cell conditions of A.4 hold for every variant, no duplicates). 128 replicates, seeds 96000-96127: mean 2^-73.9992, relative standard deviation 0.0317,
**one-sided 99% Student lower bound 2^-74.0088** (t = 2.3483, 127 df, the registered value). All 128 log2 estimates in Appendix A.13.

**Study K** (the examined distribution; registered before any listed seed ran, Appendix A.13): the variant list is a kept-fibre-weighted pool — for 64 values of x drawn uniformly on the full
2^32 domain by a fixed LCG, every variant whose c7-class passes W7 at x is grouped into fibres by equal w6(a0, x, 0), and every variant of a fibre of at least THETA = 48 members is emitted once
per x (9,090,990 emitted variants, mean 142,047 kept per x against the histogram mean 119,869 — the 64 draws are heavy-tailed, the weighting is what matters). A variant kept at k sampled values
of x enters k times: the pool samples the law of the examined variants exactly. 64 replicates, seeds 99000-99063: mean 2^-73.9829, relative standard deviation 0.0358,
**one-sided 99% Student lower bound 2^-73.9984** (t = 2.385, 63 df). All 64 log2 estimates in Appendix A.13. (An earlier pool whose LCG used only the top 31 bits of its 64-bit state — every x
below 2^31 — was run first; it was re-registered and re-run on the corrected domain rather than reused: Appendix A.13 keeps it for transparency and it is not used for the bound.)

**Study K3** (the examined distribution, stratified per x; registered before any listed seed ran, Appendix A.13): study K's bound treats the 64-x pool as fixed — it does not measure the error of
having sampled 64 of the 2^32 values of x. Study K3 measures it: the registered pool file is split by line into the 64 per-x lists (each line of the pool is one sampled x's kept list), 8 replicates
are run per non-empty file (160 total, NP = min(8192, nk_i)), and the bound is the one-sided 99% cluster ratio-estimator lower bound over the 64 sampled x's — Y_i = nk_i m_i, X_i = nk_i,
R = sum Y_i / sum X_i, se^2 = sum_i (Y_i - R X_i)^2 / (64 x 63 x mean_X^2), R - 2.385 se. The per-x means are homogeneous: 2^-73.968 to 2^-74.034 over the 20 non-empty files. Mean 2^-73.9953,
**bound 2^-74.009** (relative se 0.0040). All 160 log2 estimates and the per-file table in Appendix A.13. This is the headline examined-law bound: it covers both the replicate noise and the
finite-64-x sampling error that study K's pooled bound leaves unmeasured.

The examined-law mean (2^-73.9953 stratified, 2^-73.9829 pooled) lies *above* the all-G mean (2^-73.9992): the kept-fibre weighting shifts the estimate in the favourable direction by 0.004 to 0.016 bit.
**q3_model = 2^-74.02 (used)**: 0.011 bit below the stratified examined-law bound and 0.011 below the all-G bound — the margin replaces the unmeasured 0.05-bit
hedge of the earlier filing with three preregistered measurements, and the stratified bound already covers the finite-64-x sampling error. The stage means of the new studies equal study B's within 0.013 bit (Appendix A.13).

### 7.5 Consistency

- Lemma 7.1 makes rows 16..22 identical by construction; the paired rows-23..36 rates of the variants' and the published W8 differ by 0.002 bit in study B (7319bba).
- Real first blocks (7319bba, quoted in Section 13.1): the row-16 pass rate of the attack's own good pairs is the exact 2^-12 (z = +0.88 and +0.51 over 424,363 and 1,693,297 passes).
  This filing's end-to-end run (Section 13.4) finds row-16 passes at the same rate (2.423e-04 per good pair).


### 7.6 The examined family of this filing (the premise H2, now measured for it)

The registered studies drew W8 from the 782,800 variants of the 222 largest classes. This filing examines a different subset of the same family G (the variants of fibres with at least THETA members, from all 22,976 classes).
By Lemma 7.1 a variant changes nothing in rows 16..22 and enters rows 23..36 only through W8, i.e. through the four conditions on W24x = Z + W8x; if Z were exactly uniform given rows 16..22 these four conditions would hold with probability exactly 2^-4 for *every* W8x
(W24x would be uniform), so q3 would be the same for every subset of G. The same holds one stage earlier: W7 enters rows 16..36 only through W22 = s1(W20) + W15 + s0(W7) + W6, whose x-conditions (row 22: 11 bits) hold with probability 2^-11 for every (W6, W7) if s1(W20) + W15 is uniform given rows 16..21. The examined pairs are not uniform on F7: x = c7 - W7 is selected, so the law of W7 among examined good pairs is weighted by the number of kept variants at x = c7 - W7 (and the same for W6 only through cb, which is independent). The stage factor of that tail in the registered studies is 2^-4.015 (study A) and 2^-4.007 (study B) against the exact 2^-4, and the paired comparison with the published W8 differs by 0.002 bit: the dependence on W8 is below the sampling resolution.
The new studies of Section 7.4b *measure* the variant side of this directly: study G draws W8 uniformly over the whole family G (bound 2^-74.0088), and studies K/K3 draw W8 under the kept-fibre-weighted
law of the examined variants themselves (pooled bound 2^-73.9984, mean 2^-73.9829; stratified bound 2^-74.009 covering the finite-64-x error, mean 2^-73.9953 - the kept-fibre weighting shifts the estimate up from the all-G mean by up to 0.016 bit). What remains a premise rather than a measurement is the conditional
uniformity at row 22: in every study (registered or new) the row-22 stage draws (W6, W7) *uniformly* on F6 x F7, while the examined pairs weight W7 by kept-count at x = c7 - W7; the premise that the
11 row-22 conditions hold at 2^-11 for every (W6, W7) (because s1(W20) + W15 is uniform given rows 16..21) is common to all filings on this track, and its measured stage factor (-10.998 to -11.009
against the exact -11.000) sits inside the bound's margin.
The premise H2 is therefore stated for the examined family at the measured bound with a residual margin: **q3_used = 2^-74.02**, i.e. 0.011 bit below the stratified examined-law bound of study K3
(which already covers the finite-64-x sampling error) and 0.011 bit below the all-G bound of study G, covering the unweighted row-22 stage and the studies' common caveats (approximate normality of the
Student and ratio-estimator bounds, the heavy duplication of row-22 survivors within a replicate, the `+` reading). This is a measured premise, not a subset-transfer hedge: the earlier filing charged
0.05 bit *below* the same bound for a subset it had not measured. Section 11.2 prices alternatives: at the examined-law bound face value (2^-74.009) the claim would be 61.13536.

### 7.7 Rows 18 and 19: the accepted value patterns (ffbe30bb; Appendix B)

Table 15 fixes the value bits E18[1] = 1, E18[5] = 0, E18[10] = 1, E18[11] = 1, E18[18] = 0, E18[28] = 0, E18[29] = 1 and E19[29] = 1. This derivative's program and its SMC (the base's `smc.c`, byte-identical, with the eight characters of `lab.h` changed) do not impose them. Everything else is checked as before on every row: the cells, the adjacent-`+` equalities,
the printed two-bit conditions closing at the row, and for both members the exact signed differences of A, E and W (the member y is computed from the schedule or, in rows 16..21, from the exact difference of its words). Rows 16..22 are functions of the rows 12..15 of S, of l and of W16..W22 only (Lemma 7.1),
so what the accepted patterns are is the same for every variant of G, and the variant still enters only through W8. By Appendix B.2 exactly four patterns of the eight bits are feasible and the base's is one of them; by Appendix B.3 the SMC measures the probability of rows 16..36 with these patterns accepted at
2^-72.04 against 2^-74.02, i.e. 1.98 bits, the two bits being the structural count (4 patterns of equal weight) and its measured value at the row 18/19 stages (Appendix B.3). The stage factors of rows 20..22 and of the tail are the base's within sampling error. H2 is stated at the measured bound (Section 12). This filing replaces the cell event of rows 22..36 by the collision event and multiplies the cell factor 2^-72.04 by the lower bound 2.4331 of Appendix D.3.


## 8. The algorithm: the x-indexed table and the fibre test

### 8.1 Fibres, kept fibres and the examined variants

For a variant a0 and A_{-1} = x define (Section 5.1, Lemma 4.1)

```text
phi(a0, x) = MAJ(A1, a0, x) - CH(E5, a0 + C4, E3)   (mod 2^32),   E3 = K3C - MAJ(A2, A1, a0) + x,       W6x = cb + phi(a0, x),   cb = C6 - A_{-2}.
```

(`xtab.phi`; it equals `w6of(a0, x, A_{-2}) - cb`, asserted in the selftest.) Let P(x) = {a0 in G : c7(a0) - x in F7} be the variants whose class passes the W7 test at x (the union of the passing classes). The **fibres** of x are the classes of P(x) with equal phi, *whatever their class*;
the **fibre value** is the common phi. A fibre is **kept** if it has at least THETA = 48 members; E(x) denotes the union of the kept fibres, the **examined variants** at x. Since cb is independent of x (H1), each fibre passes the F6 test independently of its size with probability exactly p6
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
- **members:** one array of 256-bit words (`Gw`), where each 64-bit lane holds `a0` in bits `0..31` and `(~S0(a0) & M32)` in bits `32..63` of four consecutive members of a kept fibre, contiguous and word-aligned, each fibre padded to a multiple of four members by repeating its last member (so every group of four is one 256-bit word and every lane of every group is a real member).

**Construction and operation bound.** For x = 0, 1, ..., 2^32 - 1: (i) decide c7(c) - x in F7 for the 22,976 classes by the bitwise form of Section 5.1 (at most 80 operations per class: 2^52.8 in all); (ii) for every variant of a passing class
(12,103,680 x |F7| = 8.25 x 10^14 pairs (x, variant) in all, 2^49.55, because each class passes for exactly |F7| values of x) compute phi (at most 32 operations) and sort the (phi, record) pairs by phi by a four-pass byte radix sort (per pair and pass at most 40 operations: the count, the prefix sums amortised, the scatter and the loop;
so at most 160 per pair), scan the sorted array once to cut the fibres (at most 8 per pair), write the kept fibres' records, entries and cost words (at most 16 per pair) and transpose the kept fibre values into planes (at most 96 operations per kept fibre; at most (1/THETA) per pair).
This is at most 256 operations per pair, 2^57.55 in all; (iii) writing T0 and the record addresses: 2^32 x 8 operations; (iv) Rmask: zeroing 2^32 words (4 operations each) and OR-ing the 1,052,672 enumerated pairs (u, l) (at most 10 each): below 2^34.1 (the enumeration itself is 7319bba's, below 2^38.7 operations, Section 11.1 there).
The total is below **PRE = 2^58 operations**, which is 2^46.6 target compressions (about 2^-14.5 of the score); all of it is included in T and in the claimed preprocessing. The program text is straight-line code of a few thousand instructions; no part of the table depends on cb or on any other word of the chaining value.

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
31 adds for the 32 plane loads of a batch, the batch pointers, the table-entry address of each set lane, the entry address, the table read at x. The row-16 table is addressed by the lane value E0 + s0(W1) + (RBASE + ((kap0 - e0b) mod 2^32)): the per-first-block constant C = RBASE + ((kap0 - e0b) mod 2^32) is formed once (in cv_pre) and added to all four lanes by one operation, so no per-lane base add is needed (Section 9.6).
The executable counted program is `experiments/xtab.py` (`process_cv`, `w6_batch`, `good_group`, `mask_lookup`); its routines count every executed primitive of the routines below, and the ledger (`ledger`) is computed from them with exact rationals.

### 9.2 Fixed per first block: 195 operations

- First block words: 2 random words, then the 16 fields (field 0 of a word: and; fields 1..6: shr, and; field 7: shr): 30.
- Control allowance 16 (loop counter add and compare-branch, the cap test, further loop or address arithmetic not itemised elsewhere).
- The table read: address (add) 1, load 1, test and branch 2, plus 1 for the shift of the 8-byte entry index: 5 (`T0_OPS`); three loads of the record header (B, plane address, entry address): 3.
- cb (2), the 32 broadcast planes z_j = 0 - ((cb >> j) & 1) (2 for j = 0 (`z_0 = 0 - (cb & 1)`), 3 for j = 1..30 (`cb_j = cb_{j-1} >> 1; z_j = 0 - (cb_j & 1)`), 2 for j = 31 (`cb_31 = cb_30 >> 1; z_31 = 0 - cb_31`, since cb < 2^32 so cb_31 in {0,1}): 2 + 90 - 26 = 66, `ZPLANE_OPS`), the per-first-block constants of the packed stage (`cv_pre`: 73 as executed: 4 + 11 + 3 + 15 + 2 for the constants, 24 for the broadcasts of the six non-constant per-first-block words to four lanes and 14 for unpacking the chaining value from the compression output).

These are charged to every first block, also to those whose record is empty (which skip them): 30 + 16 + 5 + 3 + 2 + 66 + 73 = 195 (`FBFIX`). The 32 broadcast planes z_j are formed once into registers and stay there for the whole batch loop (Section 9.4: at most about 26 other values are live in the adder and the F6 phase, and 32 + 26 <= 64). They are dead before the group stage starts, which needs about 62 registers — so they are neither stored to memory nor reloaded per batch, unlike the earlier layout (264 fixed, plus 63 per batch).

### 9.3 Batch loop

Per batch: the loop counter, compare and branch (3), the plane pointer and the entry pointer (2), the cost word of the batch (address add, load, add to V: 3): 8 operations (`BATCH_OVH`). The z_j are operands in registers (Section 9.2), not loads.

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
**Registers.** The 32 planes z_j stay register-resident through the whole batch loop (Section 9.3). At bit j the live values are the 32 z_j (all retained for the later bits and the next batches), the carry, at most four temporaries, dl[j], and the retained sum bits (at most 19); the peak (about 57) and the F6 phase (20 sum bits and about 6 temporaries alongside the 32 z planes) are
below 64, with no spills. There is no data-dependent branch: the cost of a batch is the same for every cb and every record.

### 9.5 Scan of the pass plane and the segments

The pass plane (nl live lanes, zeros above) is scanned in 24-bit chunks: per chunk the extraction (the lowest and the highest chunk one operation, the others two) and a zero branch (`chunk_fixed_ops`); per set lane the address of the table entry (add of the batch's chunk-table base, which incorporates `entry_base`), the load of the pre-scaled entry address `entry_base + (256 b + L) * 32` from the 2^24-entry
table of the chunk position, x - 1, x & (x - 1) and the loop branch: 5 (`SCAN_LANE`). A set lane is a passing fibre: the load of its entry (1), the unpacking of start, cost and end (the entry word has the pre-scaled start pointer in lane 0, the end pointer in lane 1 and the cost in lane 2 with zero above: AND, shr and AND, shr: 3) and the addition of the cost to V (1)
are `SEG_OVH` = 4; together 9 operations per passing fibre.

### 9.6 Packed good pairs: the group of four, read in place from a single 256-bit word

The member blocks of a segment lie contiguously and word-aligned in a single array; a *group* is one 256-bit word `Gw` holding four consecutive members in its four 64-bit lanes, with `a0` in bits `0..31` and `(~S0(a0) & M32)` in bits `32..63` (`S0pack(a0)`). With `LM` = `2^32 - 1` in every lane:
- `Sw = Gw >> 32` (1 op): bits `0..31` of lane `k` hold `~S0(a0_k)` and bits `32..63` hold `a0_{k+1} < 2^29` (no mask needed);
- `E0 = (Gw + bc(e0b)) & LM` (2 ops): because `S0(a0) >= 8` on `G`, `(~S0(a0) & M32) <= 0xfffffff7 < 2^32 - 1`, so a carry of `1` from `a0 + e0b` in bits `0..31` never overflows bit `63`;
- `mj = Gw & bc(x12)` (1 op, `x12 = A_{-1} ^ A_{-2}`, high 32 bits zero);
- `ch = (E0 & bc(X)) ^ bc(Em2)` (2 ops, high 32 bits zero);
- `S1(E0)` with the 8-operation pattern (`d = E0 | (E0 << 32)` (2), three shifts, two XORs, one mask `& LM`: 8 ops, high 32 bits zero);
- `W1 = (bc(kap1' + 1 + 3*2^32) + Sw - mj - S1(E0) - ch) & LM` (5 ops: 1 add, 3 sub, 1 `& LM`): since `-S0(a0) = ~S0(a0) + 1 (mod 2^32)`, adding `Sw` and `1` replaces `- S0(a0)`; the bias `3 * 2^32` absorbs the three 32-bit borrows in bits `0..31`, while in bits `32..63` of lane `k` the sum is `a0_{k+1} + carry_lo < 2^30` and the subtrahends `mj`, `S1(E0)`, `ch` are zero in bits `32..63`, so no carry or borrow ever crosses a 64-bit lane boundary;
- `s0(W1)` with the 8-operation pattern (`d1 = W1 | (W1 << 32)` (2), `(d1 >> 7) ^ (d1 >> 18) ^ (W1 >> 3)` (5), `& LM` (1): 8 ops, high 32 bits zero);
- `U = E0 + s0(W1) + bc64(C)` (2 ops), where `C = RBASE + ((kap0 - e0b) mod 2^32)` (formed once per first block in `cv_pre`, 64-bit broadcast): since `E0 = (a0 + e0b) mod 2^32` and `s0(W1)` both have zero in bits `32..63`, `E0 + s0(W1) + C = RBASE + u + {0, 2^32, 2 * 2^32} < RBASE + 3 * 2^32` in each 64-bit lane without needing a masked copy of `a0`, and `Rmask3` is three consecutive copies of `Rmask` (total `3 x 2^32` words): **30 operations** (`GROUP_OPS`: load `Gw` 1, `Sw` 1, `E0` 2, `mj` 1, `ch` 2, `S1(E0)` 8, `W1` 5, `s0(W1)` 8, `U` 2; in the unrolled blocks of 32, 16, 8, 4, 2, 1 groups, group `0` loads from `[ptr]` directly and groups `1..k-1` fold their fixed immediate offset into the per-first-block constant `bc(e0b)` via `Gw_i_shifted = Gw_i + offset`, or use immediate-displacement loads where `ptr` is updated once per unrolled block in the loop control).
Then the lookup of every lane (`mask_lookup`): extraction of the address from its lane (lane 0: and with a 64-bit mask; lanes 1, 2: shr, and; lane 3, the top lane: shr, nothing lies above it), the load of the word of Rmask3, the branch on a nonzero mask: 3, 4, 4, 3 = **14** per group (`PROBE_OPS`).
All four lanes of every group are probed (the padding lanes repeat a member of the same fibre), so a group costs 44 (`GROUP_FULL` = 30 + 14) whatever its content.
**Segment loop.** A segment of g = ceil(n/4) groups is run as floor(g/32) iterations of an unrolled block of 32 groups (control per iteration: pointer/count update, compare, branch: 3), then, for the bits 16, 8, 4, 2, 1 of the remainder, blocks of 16, 8, 4, 2 and 1 groups chosen by a test (and, branch: 2 each) with the length computation (1) and the entry test of the main loop (2) the control is at most 13 + 3 floor(g/32) operations (`LOOP_SEG`, `LOOP_ITER`, `seg_ops`).
A segment of n members therefore costs 9 + 13 + 3 floor(g/32) + 44 g operations (the `cost` word of its entry, reaching V in one addition; the ledger evaluates it exactly for every fibre size).
**Verification:** `selftest` compares the address in the 4 lanes of U with the definition of u (W0 + s0(W1) from the chaining value and a0, plus RBASE and the multiple of 2^32) on 6,000 lanes with extreme chaining-value words (0, 1, 2^32 - 1, 2^31, ...) and variants of maximal S0, and asserts every lane value below 3 x 2^32; `mask_lookup` against the definition of the extraction on 8,000 lanes: 0 mismatches.

### 9.7 The rare path

A lane whose mask is nonzero (probability 1,042,240/2^32 per probed lane): V += 1; the a0 of the lane (2: shift, and, charged as RARE_LOOKUP); recompute W6 and W7 (23 operations) and c7(a0) for W7 (12 more, `RECOMP` = 35); then for the l in the mask W0..W5 and W8 (201),
the y-words (8) and the rows: computing a row of both members costs 106 (W (20), CH (3), E (14), MAJ (4), A (12) per word), its check of the cells and the two-bit conditions closing at the row at most 53, and the branch 1 (7319bba's counts). **This filing (Appendix D.5):** row 16 is computed (106) but not checked, because the l-mask is the exact enumeration of the row-16 test
(`make_R16` evaluates the same `row_ok` and `x2_ok`); row 17 is computed and checked (160); rows 18..21 are computed and checked with early abort (160 each); rows 22..36 are computed without checks (106 each) and the outputs are compared (8 XOR, 7 OR, 1 branch: 16). Charged: the y-words and rows 16 and 17 always (8 + 106 + 160),
rows 18..36 and the comparison (4 x 160 + 15 x 106 + 16 = 2,246) with probability 2^-12 (the stage factor of row 17 is 2^-13.000 in every study of Appendix B.3; one bit of margin, and every later row is reached less often). ffbe30bb charged rows 16 and 17 with their checks and rows 18..36 at 160 each with probability 2^-9. The binary search of the earlier filings is gone because the mask is read directly.

### 9.8 The work counter V

V counts every executed operation in the units of Sections 9.2-9.7. The data-independent part (9.2) is charged per first block; the cost word of each batch (230 + 1 + 8 + the chunk operations of its nl lanes) and the cost word of each passing fibre (9 + 13 + 3 floor(g/32) + 44 g, g = ceil(n/4)) are stored in the record and reach V by one addition each (counted in `BATCH_OVH` and `SEG_OVH`);
the rare path adds its executed cost when it runs. The cap is tested after every first block (compare and branch, in the control allowance). The overshoot past V_MAX is at most the maximal data-dependent work of one first block, vmax_fb = 1,077,492,591,596 (every one of the 12,103,680 variants examined and good, every l past row 16 to row 36 and the output comparison; fcbc9c83: 1,077,541,006,432; ffbe30bb: 1,438,831,012,960), which the ledger charges.

## 10. Success probability, independence and caps

Let a *trial* t = (f, a0, l) be a first block f, an examined variant a0 and l in L*, and A_t the event that a0 is good for f, the pair follows every cell and printed two-bit condition of rows 16..21 and the two 37-step outputs are equal (this filing's success event; Appendix D). The program examines every good pair among the examined variants of every processed first block
(Lemma 8.1) and every l whose row 16 holds, so it finds a success iff some A_t occurs before the cap (and every output is verified, Lemma 6.1). Let X_f = sum over the trials of f of 1[A_t] and X = sum_f X_f.

- **Expectation.** E[X_f] = g x 32 x q3 (Lemma 5.1 and Section 7) with g = p6 E_x|E(x)| the expected number of examined good pairs per first block, and E[X] = N_FB g 32 q3. With g >= g_low (the sampled mean of Section 13.3 divided by the statistics safety factor 1.006, H9)
  and q3 >= q3_used (H2, this filing: 2^-72.04 x 2.4331 = 2^-70.75720): E[X] >= N_FB g_low 32 q3_used >= mu0 = 0.49466958 (H7) for N_FB = ceil(mu0 / (g_low 32 q3_used)) = 3,869,961,979,885,410 = 2^51.78124;
  mu0 is the smallest 8-decimal number strictly above -ln(0.61 - Pcap - 2^-60) / (1 - 2^-10.4), with Pcap the work-cap failure bound below.
- **One first block (H3).** By Bonferroni, Pr[X_f >= 1] >= E[X_f] - sum over pairs t < t' of f of Pr[A_t and A_t'] = E[X_f] - (1/2) sum_t Pr[A_t] E[X_f - 1 | A_t]. H3: E[X_f - 1 | A_t] <= delta = 2^-9.4 for every trial t, so
  Pr[X_f >= 1] >= (1 - 2^-10.4) E[X_f]. (Only the expected number of *further* successes of the same first block given one success is needed; bursty goodness and shared W7/W6 values enter only through that conditional expectation, and do not affect E[X], which is linear.)
- **Many first blocks (H1).** Distinct first blocks have independent chaining values, so the events X_f >= 1 are independent and Pr[X >= 1] >= 1 - exp(-sum_f Pr[X_f >= 1]) >= 1 - exp(-(1 - 2^-10.4) mu0). The table record of x is a deterministic function of x (Section 8.4).
- **Work cap.** The data-dependent work v_f of a first block (everything except its compression and its 195 fixed operations) has mean at most vbar = 93,087 (Section 11) and satisfies 0 <= v_f <= vmax_fb = 1,077,492,591,596 (< 2^40.0; every one of the 12,103,680 variants examined and good, every l past row 16 to row 36 and the output comparison).
  The v_f are independent (H1) with E[v_f^2] <= vmax_fb vbar, so by Bernstein's inequality (this filing; ffbe30bb used Chebyshev) Pr[sum v_f > (1 + s) N_FB vbar] <= exp(-s^2 N_FB vbar / (2 vmax_fb (1 + s/3))) = Pcap = 2^-17.80706 with the slack s = 1/3680 (Appendix D.4). V_MAX = ceil((1 + s) N_FB vbar) = 360,341,971,828,600,115,535 is reached with probability below Pcap; the run then fails, which is accounted for here.
  No part of v_f depends on a conditional law of the scalars: the cost of a fibre batch is the same for every cb and every record (Section 9.4), and the table statistics enter vbar as expectations over uniform x (H9).
- **Success.** Pr[output a collision] >= 1 - exp(-(1 - 2^-10.4) mu0) - Pcap - 2^-60 = 0.3900000041 > 0.39 (the 2^-60 covers a repeated first block among N_FB draws of 512 bits). Any output is a verified collision, independent of the premises.

## 11. Ledger (exact; `python3 experiments/xtab.py ledger`)

```text
T = A_C + A_S + DEV + N_FB + (N_FB x 195 + V_MAX + vmax_fb + PRE + FIN) / C + 6
  A_C = 2^60   characteristic search and SFS-pair search of the paper (allowance, H4)
  A_S = 2^50   Step-1 SAT solve (paper: 2^41.3)
  DEV = 2^40   all development computation (Section 13.5)
  N_FB = 3,869,961,979,885,410 compressions (2^51.78124; H7 mu0 = 0.49466958, q3 = 2^-72.04 x 2.4331 = 2^-70.75720, g = 7,971 examined good pairs per first block)
  195     fixed operations per first block (9.2: 30 + 16 control + 5 table read + 3 header loads + 2 + 66 + 73)
  V_MAX = 360,341,971,828,600,115,535 = ceil((1 + 1/3680) N_FB vbar), vbar = 93,087 operations, of which
               fibre batches (ceil(F/256) <= F/256 + 1 batches, each charged as a full batch of 230 + 1 + 8 + 31): 1,504
               passing fibres (p6 F x 9): 704
               segments (p6 times the sum over kept fibres of 13 + 3 floor(g/32) + 44 g; every lane probed): 89,863
               rows >= 16 (every probed lane may hit; Section 9.7, Appendix D.5): 1,016
               with F = 1,163.1 x 1.006 kept fibres and Q = 29,975.7 x 1.006 four-groups per first block (Section 13.3)
  vmax_fb = 1,077,492,591,596 (one first block's maximal work: overshoot past the cap test)
  PRE = 2^58 operations (bound on all precomputation, Section 8.2); FIN = 1600 operations and 6 compressions
T x 2644 = 3,422,921,269,986,078,257,473    ->   T = 2^60.167212   ->  time_log2 = 60.16722
  (cap failure: Bernstein, Pcap = 2^-17.80706, Section 10 and Appendix D.4)
preprocessing = A_C + A_S + DEV + PRE/C = 2^60.00155
```

Every count in this block is produced by `ledger()` of `experiments/xtab.py` from the executable routines and the constant HIST_Z (Section 13.3); the integer-tightness of the 5th decimal is asserted in both directions (T^100000 against 2^(p) and 2^(p-1)).
Per first block the program spends 36.28 units (fcbc9c83: 37.26; fe65a7cb: 36.33; ffbe30bb: 37.31; 0db0eeb6: 38.21); per examined good pair the data-dependent work is 11.68 operations, of which about 11.3 are the group and its four lookups.

### 11.1 Precomputation

Section 8.2: PRE < 2^58 operations, charged in full (2^46.6 units). Padding lanes: the groups of a fibre of n members are ceil(n/4); the (4 ceil(n/4) - n) padding lanes are probed too and charged (Section 9.6) and the statistics Q count them.
The rare path is charged for every probed lane, padding included.

### 11.2 Sensitivity (log2 T, one input changed)

| change | log2 T |
|---|---|
| as claimed (q3 = 2^-72.04 x 2.4331, Bernstein slack 1/3680, rare path as executed) | 60.16722 |
| exact-event multiplier at the pooled point estimate of all three runs, 402,680/164,011 | 60.16581 |
| exact-event multiplier 2.40 | 60.16937 |
| exact-event multiplier 1 (the cell event of rows 22..36 only, all other changes kept) | 60.37569 |
| q3 cell factor 2^-72.0129 (study G of Appendix B.3 at face value) | 60.16430 |
| q3 cell factor 2^-72.5 | 60.22482 |
| q3 cell factor 2^-73 | 60.30806 |
| q3 cell factor 2^-74.02 (Table 15 pattern only) | 60.56717 |
| A_C = 2^64 | 64.01104 |
| A_C = 2^56 | 57.56861 |
| table statistics at face value (x 1.00 instead of x 1.006) | 60.16538 |
| table statistics x 1.05 | 60.18091 |
| table statistics x 1.10 | 60.19700 |
| THETA = 16 | 60.17080 |
| THETA = 40 | 60.16728 |
| THETA = 100 | 60.16891 |
| cap slack 1/2048 (Bernstein) | 60.16725 |
| cap slack 1/8192 (Bernstein) | 60.19626 |
| Chebyshev cap bound with slack 2^-10 instead of Bernstein | 60.16894 |
| each of the four row-16 lookups needs a comparison before its branch (+4 per group) | 60.18032 |

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

A kept fibre of n members costs, per first block, one lane of a batch in the fibre test (1.05 operations amortized, whether or not it passes) and, with probability p6 = 0.0669, 22 + 3 floor(g/32) + 44 g operations, and yields p6 n good pairs. The marginal cost per good pair is therefore
r(n) = (15.8 + 22 + 3 floor(g/32) + 44 g) / n + 0.13 (the rare path) operations, which tends to about 11.15 for large n (the group and its four lookups cost 11.0 per member).
Section 11.2 prices THETA: log2 T varies by less than 0.001 bit for THETA between 36 and 64 (the table of Section 13.3); THETA = 48 is within 0.00003 bit of the minimum of the ledger's own table under this filing's reduced costs, and the threshold THETA = 40 of the earlier filing would cost only 0.00006 bit more (60.16728). The simulation of Section 13.4 ran at THETA = 40 on the same histogram.

## 12. Premises

**H1 - uniform independent chaining values (score-critical).** The first blocks are fresh uniform 512-bit strings; their chaining values CV1 = F_37(IV, M0) behave as independent uniform 256-bit values; in particular x = A_{-1} is uniform on 2^32 and independent of cb = C6 - A_{-2} (uniform on 2^32).
Used for: Lemma 5.1 (exact filter rates and the law of the second-block words, per variant), the expected counts, the independence across first blocks (Section 10) and Chebyshev. Evidence: 7319bba's 2^21 and 2^23 real first blocks through the attack's own filters in C (quoted, Section 13.1: passing classes,
good pairs and row-16 passes at the predicted rates); this filing's end-to-end Tungsten simulation over uniform x and cb (Section 13.4) and d3ec5c41's 160,000 first blocks through its counted program (quoted; the same filters); organizer-run (Section 13.6, `a1-cv-r37`): on 6,144 real first blocks whose chaining values are the organizer's own digests, the organizer-checked four-plus-four-bit coincidence of x and A_{-2} in 175 of 256 trials (Binomial(256, 0.67134): mean 171.9, sd 7.5), the W7 tests of two classes 98 and 98 (mean 97.5 each), cb in F6 421 (mean 411.0), passing classes 6,988 on 2,048 first blocks (mean 7,214.9). Limitations: a premise; tested on 2^17 to 2^23 first blocks, not 2^58.3. Because the table is indexed by the 32-bit word x,
H1 for x is also an assumption about a single word of the digest of a 37-round compression: its distribution over random first blocks is uniform up to the sampling resolution of the runs above.

**H2 - Step-3 probability of the examined variants (score-critical).** q3 >= q3_used = 2^-72.04 x 2.4331 = 2^-70.75720, where q3 is Section 7.1's average over the examined variants (the variants of kept fibres) and L* of the probability that rows 16..21 follow every cell and printed two-bit condition **with the eight value bits of rows 18 and 19 not imposed** (Section 7.7) **and the two 37-step outputs are equal** (Appendix D), and q3 <= 2^-70.
*This filing.* q3 = q3_cell x R, where q3_cell is ffbe30bb's probability that rows 16..36 follow every cell (bound 2^-72.04, the evidence below) and R = Pr[equal outputs | rows 16..21] / Pr[cells of rows 22..36 | rows 16..21] under the same law of the late words; R >= 2.4331 is the preregistered one-sided 99 percent Clopper-Pearson bound of Appendix D.3 (402,680 equal-output events against 164,011 cell events, every cell event also an equal-output event; the preregistered third run alone gives 2.4502, and 2.4445 with its measured overdispersion). Because the late proposals share resampled row-21 states, the binomial reading is not exact; with overdispersion allowed for, the bounds are 2.4408 (quasi-binomial) and 2.4464 (cluster ratio over 48 seeds) on these runs, and 2.4520 and 2.4515 on a preregistered run of 2^32 late proposals with (W7, W8) drawn from the attack's own kept-fibre law (Appendix D.3b; ratio 2.46455). 2.4331 is below all of them. The product of a 99 percent bound with a 99 percent bound holds with probability at least 98 percent. The upper bound q3 <= 2^-70 used by H3 holds with 0.69 bit of margin (point estimate 2^-70.70).
Evidence: Appendix B.2 (exactly four patterns of those bits are feasible; three further verified 37-step semi-free-start collisions; the organizer experiment `a0-sfs-r37`, whose four pattern classes are each constructed and found again by the counted program), Appendix B.3 (the base filing's own program `smc.c`, byte-identical, with the eight characters of `lab.h` changed, run under three preregistered studies that repeat the base filing's studies G, K and K3 with fresh seeds:
study G over the whole family G, 128 replicates, bound 2^-72.0129; study K over the kept-fibre-weighted pool of the examined distribution, 64 replicates, bound 2^-72.0367; study K3 stratified per x over the same pool, 160 replicates, cluster ratio-estimator bound 2^-72.0155 covering the finite-64-x error; the charge is the lowest of the three bounds rounded down to two decimals of log2),
Appendix D (the collision event, its exact structure, the three runs and the organizer experiment that constructs collisions outside the printed cells of rows 22..36), Lemma 7.1 and Section 7.6 (the variant enters only through the four conditions on W24x, measured by the stage factor of the tail, -3.997 against the exact -4), the agreement of the stage factors of rows 16..17 and 20..22 with the base's, and the base filing's evidence for the unchanged part (Sections 7.4-7.6, the row-16 rate of real good pairs, the semi-free-start collisions with variant dense parts, Section 13.2).
Limitations: Monte-Carlo bounds whose coverage rests on the approximate normality of the replicate means (study G: relative sd 0.0758 over 128 replicates; study K: 0.0765 over 64; study K3: relative se 0.0081 on the ratio estimate; the relative spread is about twice the base's because the row-19 stage keeps one child in 32); the `+` reading; the heavy duplication of row-22 survivors within a replicate;
and the studies' row-22 stage draws (W6, W7) uniformly, so the conditional-uniformity argument of Section 7.6 remains a premise there. The count of four feasible patterns is a solver enumeration for the published dense part with the signed cells of rows 14 and 15 (Appendix B.2); it is cross-checked by the SMC, which applies the program's own exact difference checks, not by a proof. A stated premise, not an established fact.


**H3 - few further successes per first block (score-critical).** For every trial t, the expected number of other successful trials of the same first block given A_t is at most delta = 2^-9.4, i.e. E[X_f - 1 | A_t] <= 2^-9.4. It splits into (a) the same variant with another l in L*, and (b) other good pairs (other variants) of the same first block.
For (a) the premise is E[#other l succeeding | A_t] <= 2^-11; 7319bba measured it directly on 19,620,436 distinct Step-3 successes of the SMC (replay of Section 13.1: 0 further successes; rule-of-three 95% bound 2^-22.65). For (b) the expectation is at most rho x N_good x 32 x q3, where N_good bounds the expected number of examined good pairs of the same first block given A_t,
q3 <= 2^-70 (H2), and rho bounds Pr[t' succeeds | t succeeds, t' good] / Pr[t' succeeds | t' good]; the premise is rho <= 2^35 (the measured factor at the row-16 level is 0.98 and 1.00). **The earlier filings used N = all 782,800 variants of their family; with the whole family G (12,103,680 variants) that bound would be rho x 2^-41.5 = 2^-6.5 > 2^-9.4 and is not used.**
The number of other examined good pairs of the same first block is at most the number of examined good pairs, whose size-biased mean (the mean given that a particular pair is good: E[g_x^2]/E[g_x] over x, Section 13.4) is 127,978, below 2^17.0, with an allowance of 2^3 for the further bias of conditioning on A_t, so N_good <= 2^20.0 and delta <= 2^-11 + 2^35 x 2^20.0 x 2^5 x 2^-70 = 2^-11 + 2^-10.0 < 2^-9.4.
Measured here for the new structure (fibre mates share W6 exactly, all classes merged): on 54,000 real first blocks restricted to the 222 embedded classes (THETA = 8, Python counted program), 43,295,580 good pairs and 10,499 row-16 passes (rate 2.425e-4, exact 2.4e-4) give sum R(R-1) / (p^2 sum G(G-1)) = 0.991, the statistic of the earlier filings (0.98 and 1.00). Limitations: rows >= 17 of distinct good pairs cannot be measured jointly within one first block; the premise leaves a margin of 2^35 over the measured row-16 factor; with the size-biased mean alone (without the allowance of 2^3) the examined-pair term would be 2^-13.0.
*Organizer-run (this filing, Section 13.6).* `a3-dep-r37` constructs 32 successes (37-step semi-free-start collisions through rows 16..21 with equal outputs) and examines up to 2,048 other good pairs of each success's own chaining value (65,251 in all): 16 row-16 passes (16.0 expected at the unconditional rate 1,052,672/2^32 per good pair), none reaching row 17, no further success; the other l of the success's own variant: 3 row-16 passes, none reaching row 17. The matched control `a3-ctl-r37`, with a good pair of the same class by construction and no success imposed: 14 row-16 passes among 65,536 good pairs. Conditioning on a success does not raise the row-16 rate of the other pairs at this scale; rows >= 18 of distinct pairs remain unobservable jointly.
*This derivative.* The accepted patterns change which pairs succeed at rows >= 18, not which pairs reach row 18. In the replay quoted above the other elements l' of L* fail at row 16 (99.94 percent) or row 17 (0.06 percent) and none reaches row 18 (Appendix A.9), so for (a) the premise 2^-11 is not touched; had one reached row 18 the accepted patterns multiply
its chance of succeeding by about 4 (Appendix B.3), which turns the measured rule-of-three bound 2^-22.65 into 2^-20.65, far below 2^-11. For (b) the premise uses q3 <= 2^-70, which holds for 2^-72.04, and the pair counts of the base. A pair (variant, l) succeeds with exactly one pattern, the pattern its own W-words produce.


**H4 - advice allowances (supporting).** The published characteristic and two-bit conditions, the SFS pair's inner values S and L* are advice. Their construction is charged A_S = 2^50 (Step 1 and the completion to an SFS pair) and A_C = 2^60 (the characteristic search). Evidence: Section 11.3.
The variant family, the classes, the filter sets, L*, R16, the table and the program text are recomputed in the preprocessing (Section 8.2). Limitations: the 37-step search time is unpublished; A_C is a bound by comparison, not a measurement.

**H5 - counted word-RAM pricing (score-critical; cost reading).** A word-RAM program of 256-bit primitives in which every executed load, store, logic operation, shift, addition, comparison, branch and unconditional jump costs one primitive is charged by the primitives it executes; tables are ordinary
memory (a read is an address computation plus one load; memory is a reported metric only under collision-frontier-v5); the preprocessing is charged in full; registers: 64, with the live-value bound of Section 9.4; every address that is not a register value is formed by a counted add (Section 9.1), the base of the row-16 mask table folded into the per-first-block constant C; the program text is straight-line code of a few thousand instructions and is not advice. Evidence: the
program is in `experiments/xtab.py` (`w6_batch`, `good_group`, `process_cv`) and is exact against the scalar definitions (Section 13.2); its totals agree with the ledger (Section 13.4, in Tungsten over the whole family). Limitation: no organizer ruling is cited; the premise that the table of 2^52.1 bytes is admissible follows the earlier accepted claims with
memory far above physical capacity (e.g. 2^137 bytes) and the cost model's statement that memory contributes nothing to the scalar. A reader who prices memory accesses higher should read Section 11.2 (the per-first-block time is dominated by the packed stage, not by table reads).

**H7 - exact success floor (supporting).** The cap target is mu0 = 0.49466958, the smallest 8-decimal number strictly above -ln(0.61 - Pcap - 2^-60) / (1 - 2^-10.4) with Pcap = exp(-s^2 N_FB vbar / (2 vmax_fb (1 + s/3))) = 2^-17.80706 the Bernstein bound for the work cap (s = 1/3680; ffbe30bb: Chebyshev, 2^-9.23112). With E[X] >= mu0 the success bound of Section 10, 1 - exp(-(1 - 2^-10.4) mu0) - Pcap - 2^-60, is >= 0.39000000 with no further padding. `ledger()` computes mu0 with 60-digit decimals, asserts the success bound > 0.39 and the exact-rational ceiling N_FB g 32 q3 >= mu0. (087a18c4's H7.)
**H8 - experimental selection and multiple-testing control (supporting).** The score-critical empirical bounds charged in the ledger (q3_cell = 2^-72.04, R = 2.4331, and the table-statistic safety factor 1.006) are not artifacts of seed selection, optional stopping, or multiple-comparison inflation: their conservative margins and minimum-over-studies rules absorb family-wise multiple-testing and selection uncertainty across all disclosed pilot, exploratory, and confirmation runs, as well as the absence of an external holdout nonce on the organizer's public-seed runner. Evidence: (1) all SMC and ratio studies run on contiguous integer seed blocks (61000..61127, 62000..62063, 63000..63159; 9101..9116, 9201..9204, 9501..9532, 920001..920064) with 0 seeds dropped, taking min(LB_G, LB_K, LB_K3) rounded down to 2^-72.04 and EXQ = min(2.4331, declared) so confirmation runs 3 and 4 could only lower the charge (even at a Bonferroni alpha = 0.001 across 10 comparisons, t_0.999 bounds in G, K3 and run 4 remain above 2^-72.04 and 2.4331, backed by analytical affine counts 1275/512 = 2.4902 and the 4-pattern 1.93-2.00 bit gain); (2) H9's 1.006 safety factor over 16 contiguous shards (3.2M x, SE 0.17%) is >3.5 SE (p < 0.0003) and verified on an independent 480,000-x simulation; (3) the organizer seeds are fixed canonical SHA-256 hashes of [experiment_id, trial_index] inherited across the track with 0 bits charged from organizer trial counts. Limitation: preregistrations are participant-embedded rather than externally notarized and the organizer runner has no post-submission holdout nonce, so H8 is a plausible premise rather than externally certified pre-commitment.

**H9 - table statistics and preprocessing bound (score-critical, new).** (a) Over uniform x, let F, V, Q be the means of the number of kept fibres, of the kept variants and of sum over kept fibres of ceil(size/4). The ledger charges the sample means of Section 13.3 (3,200,000 values of x, Tungsten, sixteen shards; the sixteen shard means (recorded at THETA = 40) differ from the pooled mean by at most 1.51%, the standard error of the pooled mean is 0.17%)
times 1.006 upwards for F and Q (costs) and downwards for V (the yield g), and assumes the exact means lie within that margin. (b) The preprocessing of Section 8.2 costs at most 2^58 operations and the table at most 2^52.1 bytes — the record total is a deterministic function of the same F, V, Q and is therefore bounded by the same x 1.006 one-sided bound, Section 14. Evidence for (a): sampling and the end-to-end simulation of Section 13.4 on 480,000 further values of x; the sensitivity of Section 11.2 (a 5% error in all table statistics would cost 0.014 bit).
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
- **Lane safety of the packed group.** max over all of G of S0(a0) = 0xffffff58 and min is 8 (over the embedded 782,800 `selftest` finds max 0xffffbb5c), so `(~S0(a0) & M32) <= 0xfffffff7 < 2^32 - 1` and no carry leaves a lane; `a0 < 2^29` for every variant of G.
- **The table pipeline against brute force (`selftest`).** For 8 classes (indices 0, 17, 40, 77, 111, 150, 200, 221), 2 random x each with the class passing W7 and a random cb, for THETA = 1 and THETA = 8: the record (union fibres over all passing embedded classes, planes, entries, members) is built, every lane of every pass plane is compared with the scalar F6 test of its fibre value
  (155,092 fibre lanes) and the set of members of the passing fibres with the set {a0 in the passing classes : fibre size >= THETA and F6(w6of(a0, x, A_{-2}))} (108,798 good pairs): **0 mismatches**; the V cost word of every fibre equals 9 + seg_ops(n).
- **Packed arithmetic and mask lookup.** The 4-lane U against the definition of u (W0 + s0(W1) from the chaining value and a0): 6,000 lanes with extreme chaining-value words, 0 mismatches; `mask_lookup` against its definition: 8,000 lanes, 0 mismatches.
- **Organizer experiments (local replay of the request format with SHAKE-derived seeds; inside the organizer's 20 s and 128 MiB).**
  `a0-sfs-r37` (this filing's version; local replay of the 256-trial request, 9.9 s on one core, ffbe30bb's version 9.5 s): 128 of the 128 trials build a 37-step semi-free-start collision with a variant dense part, trial t with the value pattern t mod 4 of rows 18 and 19 (32 per pattern); W22 is proposed from the 75 x 2^17 words of Appendix D.2 and the proposal is accepted iff the two outputs are equal, and 85 of the 128 collisions do not follow the printed cells of rows 22..36 (observation `cells_22_36` = 0; 43 do). For trials 0..15 the constructed chaining value is fed to the counted online program with the table restricted to the class of a0 (THETA = 1), which finds exactly the constructed pair in **16 of 16** cases, 12 of them outside the printed cells (table read, fibre test, packed u, row-16 lookup, rows 16..21 checked, rows 22..36 computed, outputs compared).
  `a0-online-r37` (trials 0..7): on seed-drawn first blocks until a record has kept fibres (the 222 embedded classes, THETA = 8): 43 first blocks drawn, 8 records with kept fibres, 20536 fibres, 2556 passing fibres, 128152 good pairs, 29 row-16 passes; lane, filter and cell mismatches: 0, 0, 0 (pairs checked against every cell of rows -4..15 for all 32 elements of L*: 14).

### 13.3 Statistics of the table (Tungsten; premise H9)

For each of 3,200,000 values of x drawn uniformly (sixteen shards: 100,000 (eight shards) and 300,000 (eight shards); a 64-bit LCG with different seeds): the 22,976 W7 tests of Section 5.1 (bitwise form), phi(a0, x) for every variant of every passing class (about 190,000 per x), a heap sort and a run scan (Appendix A.4). The output is the histogram of fibre sizes, summed over x; HIST_Z in `xtab.py` holds it for sizes of at least 16 (zlib + base85; the text is in Appendix A.11).
Means per first block: **1,163.1 kept fibres, 119,869 kept variants, 29,975.7 four-groups** for THETA = 48 (at the earlier filing's THETA = 40: 1,221.4 / 122,253 / 30,577.1). Passing classes per x: 365.5 on average (22,976 p7 = 364.6 exact), variants in passing classes 192,590 (exact mean 12,103,680 p7 = 192,075).
The sixteen shard means of the kept variants at THETA = 40 (the per-shard records of the earlier filing; the pooled histogram is what is stored, so the THETA = 48 figures are pooled-only) are 121974, 121996, 122968, 122466, 121458, 122788, 120293, 121249, 121593, 122366, 123628, 123010, 121384, 122202, 122176, 122610 (relative standard error of the pooled mean: 0.17%). A first, smaller run of 4,000 values of x per shard (32,000 in all) had given kept variants 121,980 and kept fibres 1,214.2, consistent with the pooled values. The 800,000 values of the first eight shards had given 121,899 kept variants; the later 2,400,000 gave 122,371 (+0.4%). The ledger uses the pooled means times 1.006.

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
| 16 | 3503 | 175026 | 11638 | 60.17080 |
| 20 | 2423 | 157700 | 10486 | 60.16887 |
| 24 | 2367 | 156583 | 10412 | 60.16876 |
| 32 | 2003 | 147380 | 9800 | 60.16820 |
| 40 | 1221 | 122253 | 8129 | 60.16728 |
| 48 | 1163 | 119869 | 7971 | **60.16722** |
| 56 | 976 | 110836 | 7370 | 60.16719 |
| 64 | 888 | 105807 | 7036 | 60.16725 |
| 80 | 483 | 79682 | 5299 | 60.16802 |
| 100 | 359 | 68346 | 4545 | 60.16891 |


### 13.4 The counted program simulated end to end in Tungsten (8de337d5)

For 480,000 further values of x (eight shards, different seeds) and an independent uniform cb for each: the record of x is built as in Section 8.2 (union fibres, THETA in {20, 30, 40, 60}), the F6 test is applied to every kept fibre value + cb, and the operations of the counted program are summed by its formulas (at the 46-op group count and 71-op batch overhead of 8de337d5; this filing's 44-op group and 8-op batch overhead are 2 and 63 operations lower still, for both the simulated and the ledger values):

| THETA | x values | kept fibres | kept variants | examined good pairs (simulated) | mean data-dependent ops (simulated, 46/grp) | sd / mean | ledger vbar (45/grp, fb039a6e constants) |
|---|---|---|---|---|---|---|---|
| 20 | 480,000 | 2414.6 | 157213 | 10516 | 128430 | 3.33 | 128132 |
| 30 | 480,000 | 2014.7 | 147479 | 9862 | 119785 | 3.43 | 119615 |
| 40 | 480,000 | 1215.9 | 121838 | 8143 | 97652 | 3.78 | 97763 |
| 60 | 480,000 | 906.2 | 106810 | 7137 | 85163 | 4.01 | 85323 |

The measured mean agrees with the ledger's expectation for THETA = 40 (which carries the safety factor, the bound ceil(F/256) <= F/256 + 1 and the rare path). The counts are bursty (standard deviation across first blocks 3.8 times the mean), so the standard error is dominated by rare large records.
The simulation shares the formulas of the ledger but not its code or its source of statistics: it recomputes the fibres of each x from the variants, applies F6 to the fibre values and counts groups of the passing fibres. The size-biased mean of the examined good pairs per first block (the sum of squares over the sum, i.e. the mean number of examined good pairs of the first block that contains a given examined good pair) is 127,978 at THETA = 40 (used in H3; the claim's THETA = 48 examines 2% fewer variants, and the H3 bound of 2^20 carries an allowance of 2^3 over this measurement).
The Python program itself (`experiments/xtab.py`, restricted to the 222 embedded classes) was run on real first blocks with every operation counted by the routines of Section 9; on 700 single first blocks (two thirds of the x constructed to pass a class) the counted operations of the Python program equal the closed formula exactly (0 mismatches).

### 13.5 Development computation

Below 6 x 10^4 CPU-seconds in total (the exhaustive F6/F7 check about 600 CPU-seconds, the statistics about 1.2 x 10^4, the end-to-end simulation about 1.2 x 10^4, the selftests and experiment replays under 100, development and the aborted runs the rest), far inside DEV = 2^40 units (2^40 units are about 2^18.6 = 4 x 10^5 CPU-seconds at 2^21.4 units per CPU-second).
One earlier set of eight Tungsten shards leaked memory (untyped locals in helpers called inside a 5 x 10^8 iteration loop; about 10 GB each within 20 seconds) and was killed by hand after about 60 seconds, with no result used; the rewritten programs type every local and were measured flat at 110 MB per shard.

### 13.6 Organizer experiments for H1 and H3 (this filing)

Run by the organizer on its public seeds (the trial seed is SHA-256 of the organizer's canonical seed material and [experiment id, trial index]; we derive the seeds the same way, and on them our runs of `a0-sfs-r37` and `a0-online-r37` reproduce the stdout hashes of the organizer's report of the earlier filing of this program, 5546d208... and d5ec52ad...). The program is `experiments/xtab.py` (`cv_trial`, `dep_trial`, `ctl_trial`, `others`, `uof`); each experiment fits the 20 s and 128 MiB of the sandbox (locally 4.8 s, 9.3 s and 7.4 s on one loaded core, against 13.3 s for `a0-sfs-r37`). Development runs on other seeds were made while sizing the experiments (trial counts and examined pairs were reduced for run time); the designs and canonical experiment IDs below were fixed before the organizer-seed runs, whose numbers are reported in full with 0 trials dropped and 0 bits of the ledger score derived from organizer trial counts (H8).

- **`a1-cv-r37` (H1; event `digest-xor-mask`, mask the top four bits of digest words 0 and 1, expected 0).** Trial t draws 24 messages of 55 bytes; the padded block of each is a first block, and its 37-step chaining value is the target digest of the message, computed by the organizer (x = word 0 = A_{-1}, A_{-2} = word 1, cb = C6 - A_{-2}). The trial returns the first pair (i < j, ordered by j, then i) whose digests agree on the masked bits. Under H1 a trial succeeds with probability 1 - prod_{i=1..23} (1 - i/256) = 0.67134, independently. Result: **175 successes of 256** (reference mean 171.9, sd 7.5; z = +0.4, well within any multiple-testing band; used as a bounded-scale sanity check rather than an iid probability estimate), every one an organizer-checked event.
  Observations of the same run (participant numbers, deterministic from the seeds): 6,144 first blocks; x in C7S[0] - F7: 98, x in C7S[1] - F7: 98 (each Binomial(6144, p7), mean 97.5, sd 9.8); cb in F6: 421 (Binomial(6144, p6), mean 411.0, sd 19.6); passing classes of 222 over the first 8 first blocks of each trial: 6,988 (mean exactly 2,048 x 222 p7 = 7,214.9; overdispersed because classes with close c7 pass together, standard deviation about 2 x 3.52 per first block, so about 320 on this total).
- **`a3-dep-r37` (H3 given a success; event `full-collision`, none expected).** Trial t < 32 builds a success of the counted program on its own chaining value cv: a 37-step semi-free-start collision for a variant a0 of class (7t + 3) mod 64 and an element l of L* (rows 16..21 cell by cell with pattern t mod 4, then W22 from the 75 x 2^17 words and equal outputs, exactly as `a0-sfs-r37`).
  (a) The other l of the same variant whose row 16 holds (from the row-16 mask of u = W0 + s0(W1)) are run through rows 17..36 by `step3b`. (b) `others` takes the good pairs of cv over the classes c < 64 (W7 in F7, W6 in F6; passing classes in index order, members in order; a0 excluded) until 2,048 are examined, looks up the row-16 mask of each and runs rows 17..36 of every row-16 pass. The trial returns (cv || M1, cv || M1') iff at least one other (good pair, l) passes row 16.
  Result: 32 of 32 successes constructed, the success's own l in the looked-up mask in 32 of 32; (a) 3 other l with row 16, 0 reaching row 17, 0 successes; (b) 65,251 other good pairs (31 trials reach 2,048; one has 1,763), **16 row-16 passes** (65,251 x 1,052,672 / 2^32 = 16.0 expected), 0 reaching row 17, 0 reaching rows 18..21, 0 successes; returned pairs **12 of 32**.
- **`a3-ctl-r37` (matched control; event `full-collision`, none expected).** Trial t < 32 builds a chaining value with a good pair of a member a0 of the same class (7t + 3) mod 64 by construction (x = c7 - W7 with W7 uniform on F7, cb = W6 - phi(a0, x) with W6 uniform on F6, the other six words uniform), with no success imposed, and runs `others` on it (a0 excluded). Result: 65,536 good pairs, **14 row-16 passes** (16.1 expected), 0 reaching row 17, 0 successes; returned pairs (an indicator of at least one row-16 pass, not a collision) **11 of 32**.

Reading. H1: the organizer-checked coincidence count and the filter rates on real 37-step chaining values agree with their exact values under H1 at 6,144 first blocks; this is a bounded-scale consistency check of x, A_{-2} and the filter inputs rather than an iid probability estimate or a test of 256-bit independence at 2^51.78 first blocks. H3: given a success on a chaining value, its other good pairs pass row 16 at the unconditional rate (16 against 16.0; the control 14 against 16.1), and neither experiment has another pair reaching row 17 (about 0.002 expected in each at the row-17 stage factor 2^-13). Descriptive one-sided 99 percent bounds on the row-16 rate of the other pairs given a success: 1.75 times the exact unconditional rate (Poisson, 16 passes against 16.0 expected) and 2.93 times the control's rate (binomial split of the 30 passes). A conditional factor rho up to 2^35 at the full event, which H3 allows, is not excluded by these numbers; they exclude a dependence that already acts at row 16 by more than those factors.

## 14. Memory and advice

Peak memory (all simultaneously resident during the online phase):

| item | bytes |
|---|---|
| T0: 2^32 words of 8 bytes | 2^35 |
| records R(x): members 8 x 4 ceil(n/4) bytes per kept fibre (single packed `Gw` array), entries 32 per fibre, planes 1024 per batch, cost words: mean about 1,008,000 bytes per x over uniform x (the same terms at THETA = 48, Section 13.3, times 1.006), 2^32 records | 2^52.0 |
| Rmask3: 3 x 2^32 words of 32 bytes; the 24-bit lane-scan tables (11 x 2^24 entries); code | 2^38.6 |
| total | **2^52.1** |

Claimed memory: 2^52.1 bytes (the sum over all x of the record sizes; reported only under collision-frontier-v5; the earlier claims on this track report up to 2^137 bytes). The table is built entry by entry in the preprocessing and is never held twice.
The record total is a deterministic function of the same kept statistics F, V, Q bounded under H9 — members 32 bytes per 4-group, 32 per kept fibre, 1024 per batch — so it inherits
their bound rather than resting on the raw estimate alone: at the one-sided x 1.006 bound on those means (a >3.5-standard-error bound; the pooled standard error over 3,200,000 x is 0.17%) the
record total is <= 2^52.0 and the total is <= 2^52.1, reported at that bound. T0, Rmask3 and the lane-scan tables have exact sizes.
Nonuniform advice: the characteristic, S, L*, and the 222 class descriptors used by the experiments (below 2^13 bytes), charged through A_C and A_S; everything else, including the class list of the whole family, the table and Rmask, is recomputed in the preprocessing.

## 15. Limitations

- H1, H2, H3, H8, H9 are premises. q3 is estimated (Monte Carlo; this filing's studies cover the whole family and a 64-x kept-weighted pool, not every examined set), not proved; no collision has been found and none is expected at the scale we can run. The full-scale success probability cannot be observed.
- The table statistics (H9) are Tungsten sample means over 3,200,000 values of x, scaled by 1.006 (>3.5 SE), not an enumeration of all 2^32 values of x (about 2^58 operations of Tungsten work). The per-x counts are heavy-tailed. Section 11.2 prices a 5% and a 10% error.
- The organizer experiments run the same program on the 222 embedded classes only (the sandbox cannot hold the family) on deterministic public seeds without a post-submission holdout nonce (H8); the whole-family table and statistics are Tungsten computations, not organizer experiments.
- The memory of 2^52.1 bytes is far beyond any machine; memory is reported only under collision-frontier-v5 and earlier claims on this track report up to 2^137 bytes. A reader who charges table reads or memory differently should note that table reads are about 6,472 of the 93,087 data-dependent operations per first block.
- Study B of the inherited q3 evidence was registered after study A had been read (7319bba, Section 7.4); study A's bound would price this claim at 61.16883. This filing's own studies G, K and K3 (Section 7.4b, Appendix B.3) were preregistered on contiguous seed blocks before any listed seed ran, and taking min(LB_G, LB_K, LB_K3) rounded down to 2^-72.04 absorbs multiple-testing selection across studies (H8).
- The published characteristic and SFS pair are used as advice under allowances; the paper's SAT solve and characteristic search were not rerun.
- For 37 steps the measured q3 is about one bit better than the 75 conditions stated in the paper's text; the paper's own tables give 74, which the SMC matches stage by stage (6c77089c reached the same conclusion). With q3 = 2^-75 for the Table 15 pattern alone, log2 T would be 61.75525 (base); this derivative accepts four patterns (Appendix B) and measures 2^-72.04.
- This derivative: the count of four feasible patterns is for the published dense part with the signed cells of rows 14 and 15 of the characteristic kept (Appendix B.2); the same enumeration with the cells of rows 12..15 removed as well admits many more patterns, so the saving rests on those differences. Different value patterns of E16 and E17 become possible if the dense values change; this was not explored (the variants of G change A0 only, and Lemma 7.1 shows rows 16..22 do not see them).
  H2 for ffbe30bb's cell factor is a Monte-Carlo bound; the solver enumeration is not a proof and the SMC is the measurement that the charge rests on.
- H3 (b) is measured at the row-16 level (7319bba; and, given a constructed success, by the organizer experiments `a3-dep-r37` and `a3-ctl-r37` at rows 16 and 17, Section 13.6) and its bound on the number of examined good pairs is a premise. H1 is tested by the organizer at 6,144 first blocks (`a1-cv-r37`), not at full scale.
- This filing: the ratio R of the collision event to the cell event is measured (three runs, Appendix D.3, plus run 4 in D.3b), not proved; its exact uniform-model value 1275/512 = 2.49 (Appendix D.2) is above the charge, and the real law of W24 (correlated with W22 through W24 = s1(W22) + W17 + s0(W9) + W8) lowers it to the measured 2.455-2.465. The third run shows overdispersion across seeds (chi-square 55.4 on 31 degrees of freedom); the charge 2.4331 stays below all overdispersion-adjusted and Bonferroni-adjusted bounds (2.4408 for all runs, 2.4445 for the third alone, 2.4515 and 2.4470 at alpha = 0.001 for the preregistered fourth run under the kept-fibre law of (W7, W8), Appendix D.3b, H8), from a pool of 16,384 values of x, which is a sample of that law; per-l strata were not run separately.
- The program text, the table and the lane-scan tables are assumed addressable and free of charge to store (H5); the cost reviewer may price memory differently (Section 11.2).

## 16. What ffbe30bb and fe65a7cb changed relative to fb039a6e (61.14135) and 7c46d8cb (61.12049)

| change | effect |
|---|---|
| the E cells of rows 18 and 19 no longer impose the eight value bits E18[1,5,10,11,18,28,29], E19[29] (four patterns of those bits are feasible, six parity conditions replace the eight values; Appendix B.1, B.2); the counted program is otherwise unchanged and has the same operation counts | none in the operation counts (`ROWCHECK`, `ROWCOMP`, `W6_OPS`, `FBFIX`, `vbar` unchanged from 7c46d8cb) |
| q3 re-measured by the base's own program with that change: three preregistered studies (Appendix B.3) | `q3_used` from `2^-74.02` to `2^-72.04`; N_FB from 37,202,693,716,812,676 to 9,469,323,637,133,286; `time_log2` `61.12049` -> **`60.37819`** (ffbe30bb on fb039a6e: `61.14135` -> `60.38707`) |
| the organizer experiment `a0-sfs-r37` constructs the four patterns (trial t imposes pattern t mod 4) and the counted program finds each constructed pair | evidence for the accepted patterns; the experiment sources stay below 64 KiB |
| the ledger is printed as a standalone program with its output (Appendix C) | `python3 experiments/xtab.py ledger` prints the same figures |
| attack, family, classes, table, program text, allowances A_C, A_S, DEV, memory, premises H1, H3-H9 | unchanged |

## 16a. What fcbc9c83 and this filing change relative to ffbe30bb (60.38707) and fe65a7cb (60.37819)

| change | effect (log2 T, applied in this order) |
|---|---|
| success is the collision event: rows 16..21 checked as before, rows 22..36 computed without cell tests, the pair accepted iff the two outputs are equal (`step3b`, `same_out`; Appendix D.1); q3 multiplied by the preregistered lower bound 2.4331 on the collision/cell ratio (Appendix D.3) | fcbc9c83: 60.387065 -> 60.173378 (-0.213687); N_FB 9,467,902,869,405,105 -> 3,909,568,277,931,367 |
| Bernstein's inequality for the work cap instead of Chebyshev's, same premises, slack re-optimised at the new q3 (1/3680; Appendix D.4) | fcbc9c83: -> 60.171626 (-0.001752); Pcap 2^-8.342 -> 2^-17.935 |
| rare path charged as executed: no re-check of row 16 (the mask lookup is its exact enumeration), rows 18..36 and the comparison at 2^-12 (Appendix D.5) | fcbc9c83: -> 60.171440 (-0.000187); rows >= 16 per first block 1,130.0 -> 1,015.6 operations |
| organizer experiment `a0-sfs-r37` accepts by equal outputs, W22 proposed from the 75 x 2^17 words; new observation `cells_22_36` | 85 of 128 collisions outside the printed cells; 16 of 16 found by the counted program |
| organizer experiments `a1-cv-r37` (H1), `a3-dep-r37` and `a3-ctl-r37` (H3) added to `xtab.py` (`cv_trial`, `dep_trial`, `ctl_trial`, `others`, `uof`; `step3b` records the last row reached for the experiments only); `class_members` tests in_G and c7 inline (the same sets, checked against the definition), `sfs_trial` reads the cached class; the class descriptors stored as `CLASSES_Z` (Section 5.3) | none in the ledger (`a0-sfs-r37` and `a0-online-r37` give byte-identical output) |
| R re-measured under the attack's kept-fibre law of (W7, W8), preregistered (Appendix D.3b); the charge 2.4331 read against overdispersion-robust bounds | none (2.4331 stays below every bound) |
| combined with 7c46d8cb/fe65a7cb tightened online operation counts (`FBFIX = 195`, `SCAN_LANE = 5`, `SEG_OVH = 4`, `GROUP_OPS = 30`, `GROUP_FULL = 44`, `UNROLL = 32`, `LOOP_SEG = 13`, Section 9) | 60.171440 -> **60.167212** (-0.004228), claimed **60.16722** |

Total: `time_log2` 60.38707 -> 60.17144 (fcbc9c83) -> **60.16722** (this filing; from fe65a7cb's 60.37819 -> **60.16722**). Not counted: a ratio credit from any other reading of rows 22..36 (the four-condition description of Appendix D.2 is the same event, not a second one).

## 17. What the base filing changed relative to 0db0eeb6 (61.17784) and earlier filings (fb039a6e's own record)


| change | effect |
|---|---|
| the 32 broadcast planes `z_j` of the bit-sliced addition are register-resident across the batch loop instead of stored once and reloaded per batch (Sections 9.2-9.4; the batch stage completes before the register-hungry group stage, so no conflict) | `BATCH_OVH` from `71` to `8`, `FBFIX` from `264` to `232`, `vbar` from `98,128` to `95,763`, `time_log2` `61.17784` -> `61.17468` at THETA = 40 |
| the fibre threshold re-optimized under the reduced costs | `THETA` from `40` to `48`, `time_log2` `61.17468` -> `61.17438` |
| q3 measured on the examined family instead of inherited with a subset hedge: three new preregistered SMC studies (all-G uniform, 128 replicates, bound 2^-74.0088; kept-fibre-weighted pool of the examined distribution, 64 replicates, bound 2^-73.9984; stratified per x over the same pool, 160 replicates, cluster ratio-estimator bound 2^-74.009 covering the finite-64-x error; byte-identical registered program) | `q3_used` from `2^-74.08` (bound 2^-74.03 less an unmeasured 0.05-bit hedge) to `2^-74.02` (0.011 bit below the measured stratified examined-law bound), `time_log2` `61.17438` -> **`61.14135`** |
| all 22,976 classes, fibres merged across classes by equal phi, only fibres of at least THETA variants examined (8de337d5; Sections 5.3, 8.1, 11.4) | unchanged (the table itself is identical; only its THETA parameter changed) |
| single packed member word `Gw`, packed u, direct row-16 mask table, rare path (0db0eeb6; Section 9.6) | unchanged: `W6_OPS = 230`, `SCAN_LANE = 6`, `SEG_OVH = 6`, `GROUP_OPS = 31`, `GROUP_FULL = 45`, `CVPRE_OPS = 81`, padding lanes probed and charged |
| attack, variants' semantics, success analysis, caps' structure, A_C, A_S, DEV, memory | unchanged |

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

### A.7 (7319bba, inherited) `smc.c`, `lab.h`: the sequential Monte-Carlo estimator of q3 (Section 7.3; the program re-run here byte-identically for the three studies of Appendix A.13 — the records below are 7319bba's)

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
16 3388086153; 17 1617616; 18 65843405; 19 1209548; 20 147625343; 21 11017050; 22 16418160; 23 1215428
24 813905795; 25 1443772; 26 28049092; 27 2317268; 28 260267771; 29 1849172; 30 56570661; 31 1616188
32 2409018306; 33 1100332; 34 4167414; 35 1915832; 36 80417489; 37 225894; 38 2893151; 39 1517490
40 133122506; 41 189308; 42 26753115; 43 263068; 44 20437482; 45 2607456; 46 2920111; 47 220134
48 552810466; 49 793922; 50 3384486; 51 231384; 52 35693508; 53 208108; 54 5000579; 55 274044
56 206072898; 57 372560; 58 4325156; 59 136624; 60 66141128; 61 223376; 62 3894230; 63 772828
64 1218734068; 65 260846; 66 2348888; 67 51554; 68 4786093; 69 165784; 70 4220181; 71 80554
72 58236592; 73 38794; 74 479854; 75 458706; 76 3070457; 77 222136; 78 3367587; 79 85768
80 80287523; 81 127540; 82 459224; 83 20568; 84 27063614; 85 54296; 86 556953; 87 184542
88 14599199; 89 33176; 90 5515802; 91 169204; 92 3106725; 93 185594; 94 418287; 95 49128
96 262058783; 97 22916; 98 1510297; 99 79638; 100 3190022; 101 12642; 102 498861; 103 15446
104 25729209; 105 382616; 106 469027; 107 33372; 108 4531863; 109 14926; 110 502127; 111 22630
112 103536832; 113 41478; 114 690624; 115 41666; 116 4447263; 117 92878; 118 243744; 119 46844
120 44018814; 121 43482; 122 464860; 123 28152; 124 3988098; 125 30796; 126 1422284; 127 13402
128 440361426; 129 25726; 130 527734; 131 12086; 132 2102307; 133 39010; 134 103000; 135 148236
136 3241034; 137 13026; 138 289183; 139 6448; 140 3769064; 141 24680; 142 135138; 143 20958
144 27469943; 145 31610; 146 79854; 147 48422; 148 427445; 149 17624; 150 890169; 151 14902
152 1861652; 153 11122; 154 362114; 155 30924; 156 3039292; 157 12016; 158 154087; 159 18684
160 33316659; 161 18340; 162 211942; 163 3154; 164 413295; 165 44432; 166 33030; 167 3616
168 14959355; 169 8850; 170 111943; 171 21720; 172 463131; 173 5390; 174 359688; 175 20204
176 6510540; 177 14554; 178 53258; 179 2396; 180 4727638; 181 6170; 182 275853; 183 19202
184 1825449; 185 9428; 186 328889; 187 6288; 188 335599; 189 24846; 190 72287; 191 3638
192 87337180; 193 3220; 194 49677; 195 30608; 196 1136559; 197 2148; 198 132097; 199 1642
200 1656117; 201 3802; 202 18810; 203 11766; 204 429265; 205 3944; 206 30668; 207 8706
208 11696820; 209 3000; 210 621677; 211 3830; 212 422175; 213 5702; 214 52574; 215 4566
216 2299998; 217 17292; 218 24700; 219 4760; 220 348127; 221 4312; 222 35331; 223 1798
224 34558151; 225 37350; 226 63321; 227 4206; 228 536515; 229 1538; 230 61851; 231 10500
232 2690641; 233 6804; 234 161019; 235 6442; 236 175322; 237 6838; 238 76331; 239 1948
240 18199010; 241 5056; 242 61722; 243 4158; 244 391420; 245 6812; 246 46212; 247 5170
248 2327149; 249 3608; 250 54619; 251 1422; 252 1033944; 253 2294; 254 22101; 255 6316
256 113657549; 257 870; 258 41555; 259 1804; 260 427864; 261 6950; 262 16780; 263 1250
264 1038009; 265 3152; 266 48924; 267 2234; 268 78853; 269 1066; 270 237435; 271 2168
272 1376489; 273 7792; 274 16553; 275 2080; 276 217432; 277 954; 278 10235; 279 7796
280 1748331; 281 1586; 282 34106; 283 1068; 284 90037; 285 9300; 286 32904; 287 2478
288 8693174; 289 1110; 290 57598; 291 3610; 292 62843; 293 2728; 294 75826; 295 1816
296 208862; 297 2618; 298 22551; 299 1228; 300 644792; 301 2200; 302 21529; 303 608
304 693576; 305 3396; 306 20834; 307 512; 308 222487; 309 2572; 310 53227; 311 952
312 1484519; 313 526; 314 14805; 315 13998; 316 113305; 317 628; 318 28272; 319 1020
320 9340749; 321 1580; 322 22192; 323 478; 324 127627; 325 1368; 326 3540; 327 878
328 210737; 329 1032; 330 60399; 331 274; 332 21577; 333 1402; 334 5407; 335 484
336 5054339; 337 416; 338 12771; 339 1690; 340 80823; 341 2134; 342 32201; 343 1226
344 209690; 345 3228; 346 7930; 347 568; 348 280730; 349 360; 350 32464; 351 2546
352 1865675; 353 552; 354 17602; 355 610; 356 31994; 357 2218; 358 2783; 359 916
360 2148562; 361 1648; 362 6727; 363 1584; 364 184428; 365 670; 366 28791; 367 744
368 638269; 369 1216; 370 13053; 371 1760; 372 228799; 373 366; 374 8577; 375 2852
376 138629; 377 944; 378 37554; 379 268; 380 41123; 381 766; 382 5809; 383 188
384 20209004; 385 722; 386 4571; 387 578; 388 42142; 389 246; 390 39901; 391 574
392 445882; 393 778; 394 2871; 395 980; 396 85127; 397 190; 398 2947; 399 2854
400 498678; 401 190; 402 5883; 403 1086; 404 11688; 405 3432; 406 16149; 407 756
408 191442; 409 230; 410 7086; 411 610; 412 19301; 413 508; 414 10930; 415 362
416 3490187; 417 312; 418 4104; 419 130; 420 415587; 421 248; 422 4812; 423 810
424 191654; 425 556; 426 8101; 427 1264; 428 28876; 429 638; 430 6708; 431 238
432 709139; 433 196; 434 23201; 435 2184; 436 15461; 437 378; 438 7206; 439 210
440 124656; 441 612; 442 5340; 443 430; 444 20861; 445 466; 446 2674; 447 856
448 7673088; 449 230; 450 47406; 451 356; 452 37852; 453 1012; 454 3728; 455 954
456 221634; 457 262; 458 1777; 459 490; 460 37969; 461 116; 462 15868; 463 366
464 1006201; 465 2418; 466 12730; 467 614; 468 109033; 469 358; 470 7922; 471 496
472 66323; 473 214; 474 9111; 475 348; 476 43871; 477 712; 478 2662; 479 248
480 4904427; 481 360; 482 5411; 483 486; 484 35134; 485 384; 486 5374; 487 110
488 182503; 489 384; 490 8975; 491 380; 492 24778; 493 188; 494 7021; 495 1180
496 809327; 497 390; 498 4145; 499 144; 500 30159; 501 294; 502 1453; 503 144
504 368039; 505 326; 506 3572; 507 270; 508 12316; 509 258; 510 9661; 511 230
512 20610947; 513 484; 514 1536; 515 230; 516 23414; 517 124; 518 2316; 519 270
520 176229; 521 178; 522 10837; 523 70; 524 9386; 525 1704; 526 1111; 527 270
528 309500; 529 78; 530 4601; 531 328; 532 24907; 533 326; 534 2753; 535 166
536 28640; 537 60; 538 1734; 539 256; 540 140704; 541 146; 542 3202; 543 232
544 367649; 545 82; 546 10435; 547 58; 548 8098; 549 482; 550 2078; 551 282
552 81596; 553 302; 554 1263; 555 608; 556 6471; 557 150; 558 10616; 559 140
560 456693; 561 194; 562 1740; 563 40; 564 19202; 565 210; 566 1258; 567 298
568 31440; 569 76; 570 10053; 571 92; 572 17993; 573 70; 574 3109; 575 90
576 1797748; 577 118; 578 1441; 579 114; 580 38053; 581 146; 582 4301; 583 98
584 25970; 585 754; 586 2935; 587 20; 588 41768; 589 402; 590 2631; 591 98
592 56297; 593 96; 594 3641; 595 342; 596 9911; 597 34; 598 1325; 599 98
600 226840; 601 48; 602 2360; 603 184; 604 11297; 605 240; 606 918; 607 28
608 159516; 609 358; 610 3806; 611 286; 612 12837; 613 118; 614 499; 615 378
616 65355; 617 98; 618 3361; 619 28; 620 31615; 621 58; 622 1143; 623 50
624 433321; 625 166; 626 782; 627 186; 628 6746; 629 80; 630 18506; 631 20
632 43685; 633 234; 634 684; 635 120; 636 15516; 637 212; 638 1689; 639 88
640 1748586; 641 158; 642 2023; 643 24; 644 10141; 645 244; 646 565; 647 114
648 36564; 649 156; 650 1769; 651 484; 652 1929; 653 68; 654 1062; 655 32
656 56840; 657 224; 658 1254; 659 42; 660 29010; 661 16; 662 322; 663 74
664 7249; 665 90; 666 1210; 667 30; 668 2943; 669 34; 670 744; 671 72
672 1059352; 673 46; 674 484; 675 630; 676 6488; 677 22; 678 2472; 679 198
680 27454; 681 96; 682 2964; 683 64; 684 15550; 685 54; 686 1442; 687 60
688 55907; 689 114; 690 3157; 691 34; 692 4062; 693 136; 694 477; 695 108
696 115517; 697 40; 698 477; 699 430; 700 16478; 701 48; 702 3674; 703 68
704 345751; 705 248; 706 427; 707 24; 708 8704; 709 50; 710 566; 711 128
712 9048; 713 142; 714 3155; 715 36; 716 1201; 717 96; 718 856; 719 26
720 572338; 721 42; 722 1962; 723 106; 724 3130; 725 44; 726 2313; 727 10
728 61476; 729 40; 730 961; 731 20; 732 17050; 733 24; 734 1060; 735 444
736 140859; 737 42; 738 1271; 739 10; 740 5889; 741 120; 742 1794; 743 18
744 78010; 745 100; 746 544; 747 48; 748 3459; 749 18; 750 3626; 751 32
752 33075; 753 18; 754 961; 755 84; 756 20275; 757 34; 758 364; 759 88
760 10930; 761 18; 762 998; 763 62; 764 2243; 765 138; 766 187; 767 42
768 3136000; 769 34; 770 805; 771 16; 772 2699; 773 36; 774 830; 775 70
776 18586; 777 30; 778 390; 779 72; 780 20508; 781 26; 782 581; 783 56
784 93772; 785 26; 786 723; 787 20; 788 1453; 789 28; 790 1329; 791 88
792 26456; 793 80; 794 235; 795 160; 796 1407; 797 36; 798 2790; 799 30
800 90701; 801 34; 802 191; 803 20; 804 2809; 805 26; 806 1045; 807 26
808 3688; 809 18; 810 4356; 811 18; 812 8492; 813 128; 814 528; 815 12
816 50990; 817 32; 818 241; 819 118; 820 3584; 821 12; 822 563; 824 6708
825 42; 826 814; 827 40; 828 5025; 829 18; 830 323; 831 36; 832 670055
833 10; 834 359; 835 4; 836 1534; 837 112; 838 147; 840 137101; 841 18
842 196; 843 88; 844 2094; 845 60; 846 812; 847 72; 848 45664; 849 16
850 799; 851 22; 852 3446; 853 6; 854 1517; 855 216; 856 7584; 857 6
858 1074; 859 36; 860 3017; 861 56; 862 252; 863 86; 864 135035; 865 58
866 168; 867 26; 868 10592; 869 36; 870 2029; 871 8; 872 4061; 873 182
874 256; 875 82; 876 3833; 877 6; 878 214; 879 96; 880 25634; 881 6
882 959; 883 38; 884 2569; 885 46; 886 573; 887 10; 888 6072; 889 16
890 310; 891 6; 892 1127; 893 4; 894 964; 895 4; 896 1124881; 897 22
898 149; 899 10; 900 23513; 901 18; 902 513; 903 32; 904 11199; 905 46
906 768; 907 2; 908 1494; 909 14; 910 788; 911 22; 912 51777; 913 48
914 250; 915 154; 916 626; 917 12; 918 470; 919 14; 920 10666; 921 12
922 113; 924 6344; 925 100; 926 385; 927 56; 928 243390; 929 6; 930 2275
931 100; 932 8356; 933 34; 934 642; 935 24; 936 35248; 937 14; 938 326
939 2; 940 3554; 941 8; 942 488; 943 34; 944 14796; 945 120; 946 353
947 42; 948 4230; 949 36; 950 147; 951 26; 952 10939; 953 2; 954 599
955 74; 956 1015; 957 14; 958 214; 959 12; 960 852866; 961 28; 962 237
963 12; 964 1725; 965 8; 966 398; 967 12; 968 11237; 969 38; 970 448
971 18; 972 2301; 973 6; 974 109; 975 64; 976 54677; 977 52; 978 638
979 46; 980 3002; 981 50; 982 256; 983 8; 984 5767; 985 6; 986 207
987 10; 988 2711; 989 20; 990 1363; 992 165788; 993 4; 994 252; 995 6
996 1453; 997 16; 998 112; 999 18; 1000 7705; 1001 34; 1002 376; 1003 24
1004 547; 1005 12; 1006 475; 1007 72; 1008 67597; 1009 22; 1010 142; 1011 6
1012 1679; 1013 38; 1014 305; 1015 8; 1016 2960; 1017 22; 1018 98; 1020 4157
1021 8; 1022 268; 1023 70; 1024 2570777; 1025 28; 1026 489; 1027 28; 1028 805
1029 18; 1030 149; 1031 4; 1032 6650; 1033 2; 1034 84; 1035 22; 1036 708
1037 16; 1038 390; 1039 8; 1040 40324; 1041 32; 1042 124; 1043 6; 1044 6505
1045 8; 1046 134; 1047 10; 1048 2175; 1050 2409; 1052 435; 1053 34; 1054 361
1055 8; 1056 56666; 1057 16; 1058 143; 1059 10; 1060 2090; 1062 399; 1063 46
1064 5526; 1065 10; 1066 283; 1067 46; 1068 949; 1069 2; 1070 104; 1071 8
1072 5438; 1073 36; 1074 71; 1075 18; 1076 776; 1077 44; 1078 249; 1079 4
1080 38852; 1081 28; 1082 197; 1083 148; 1084 1543; 1085 62; 1086 203; 1087 4
1088 64199; 1089 12; 1090 96; 1091 2; 1092 4836; 1094 38; 1095 32; 1096 2160
1098 718; 1099 4; 1100 643; 1102 128; 1103 2; 1104 15912; 1105 6; 1106 448
1107 10; 1108 612; 1109 4; 1110 352; 1111 8; 1112 1786; 1113 4; 1114 218
1115 2; 1116 4960; 1117 2; 1118 194; 1119 6; 1120 69123; 1121 8; 1122 136
1123 2; 1124 587; 1125 30; 1126 37; 1127 2; 1128 4561; 1129 16; 1130 235
1131 20; 1132 348; 1134 215; 1135 12; 1136 5815; 1137 12; 1138 109; 1140 4268
1141 2; 1142 109; 1143 6; 1144 4435; 1145 14; 1146 122; 1147 10; 1148 1212
1149 10; 1150 187; 1151 2; 1152 237484; 1153 2; 1154 90; 1155 50; 1156 509
1158 173; 1159 4; 1160 12501; 1161 6; 1162 74; 1163 4; 1164 2100; 1165 114
1166 175; 1168 5978; 1169 6; 1170 748; 1171 2; 1172 1305; 1173 10; 1174 93
1175 6; 1176 9055; 1178 334; 1179 6; 1180 958; 1181 10; 1182 82; 1184 8942
1185 48; 1186 84; 1188 1743; 1189 12; 1190 192; 1191 8; 1192 2467; 1194 47
1196 621; 1197 2; 1198 93; 1199 4; 1200 43923; 1202 43; 1203 6; 1204 779
1205 22; 1206 92; 1208 3028; 1209 2; 1210 198; 1211 8; 1212 478; 1213 6
1214 53; 1215 10; 1216 21305; 1217 6; 1218 558; 1220 2056; 1221 10; 1222 279
1223 8; 1224 3106; 1225 16; 1226 41; 1227 12; 1228 198; 1230 294; 1231 2
1232 11117; 1233 2; 1234 69; 1236 1225; 1237 6; 1238 25; 1239 2; 1240 8312
1241 2; 1242 178; 1244 291; 1245 14; 1246 83; 1247 6; 1248 74708; 1250 157
1251 12; 1252 252; 1253 2; 1254 228; 1256 1335; 1257 40; 1258 138; 1259 2
1260 8726; 1261 6; 1262 40; 1263 2; 1264 10548; 1266 183; 1267 28; 1268 249
1269 8; 1270 65; 1271 14; 1272 3688; 1274 136; 1275 44; 1276 748; 1277 4
1278 92; 1280 217247; 1281 26; 1282 43; 1283 8; 1284 715; 1286 33; 1287 8
1288 2086; 1290 172; 1292 159; 1293 8; 1294 76; 1295 4; 1296 5566; 1298 105
1299 2; 1300 604; 1302 416; 1304 403; 1305 8; 1306 69; 1307 2; 1308 513
1309 2; 1310 47; 1312 8309; 1314 198; 1315 12; 1316 496; 1318 29; 1319 2
1320 6495; 1322 20; 1324 110; 1325 8; 1326 116; 1327 4; 1328 1224; 1329 14
1330 66; 1332 445; 1333 2; 1334 47; 1336 737; 1338 64; 1339 2; 1340 238
1341 4; 1342 134; 1343 6; 1344 129544; 1346 22; 1348 128; 1350 634; 1351 8
1352 1580; 1353 4; 1354 13; 1355 12; 1356 823; 1358 178; 1359 4; 1360 5513
1362 138; 1363 4; 1364 1234; 1365 30; 1366 61; 1367 6; 1368 3305; 1369 2
1370 47; 1371 4; 1372 501; 1373 6; 1374 39; 1375 6; 1376 7817; 1377 6
1378 74; 1380 1124; 1382 43; 1383 4; 1384 828; 1385 4; 1386 193; 1388 114
1389 4; 1390 25; 1392 28547; 1394 41; 1395 42; 1396 173; 1398 413; 1400 4026
1401 6; 1402 9; 1403 12; 1404 1890; 1405 6; 1406 24; 1407 6; 1408 42174
1410 229; 1412 124; 1414 56; 1416 2191; 1417 10; 1418 51; 1419 2; 1420 175
1421 4; 1422 179; 1424 1404; 1425 6; 1426 115; 1428 1054; 1430 46; 1431 2
1432 191; 1433 2; 1434 136; 1436 228; 1438 20; 1440 94935; 1441 8; 1442 132
1443 2; 1444 964; 1446 120; 1447 8; 1448 770; 1450 62; 1451 6; 1452 673
1454 9; 1455 10; 1456 10356; 1458 23; 1460 350; 1462 16; 1463 32; 1464 4892
1465 2; 1466 40; 1467 18; 1468 419; 1469 2; 1470 511; 1472 19291; 1473 2
1474 49; 1475 2; 1476 448; 1478 3; 1479 8; 1480 1146; 1482 146; 1484 569
1485 8; 1486 14; 1487 4; 1488 12798; 1490 110; 1491 4; 1492 194; 1494 26
1495 4; 1496 486; 1498 35; 1500 1150; 1501 16; 1502 38; 1504 4534; 1506 30
1508 248; 1509 2; 1510 104; 1512 3822; 1513 2; 1514 35; 1515 2; 1516 208
1518 93; 1519 12; 1520 1708; 1521 6; 1522 12; 1523 2; 1524 291; 1525 4
1526 40; 1528 367; 1530 117; 1532 74; 1533 2; 1534 16; 1535 4; 1536 316192
1537 10; 1538 12; 1539 4; 1540 227; 1542 37; 1544 703; 1545 2; 1546 20
1548 223; 1549 6; 1550 65; 1551 2; 1552 4979; 1554 53; 1556 110; 1557 4
1558 44; 1560 4666; 1562 9; 1563 2; 1564 146; 1566 148; 1568 11221; 1570 26
1572 236; 1574 8; 1575 28; 1576 336; 1578 20; 1580 514; 1581 10; 1582 87
1584 4286; 1586 42; 1587 10; 1588 77; 1590 68; 1591 4; 1592 297; 1593 2
1594 30; 1596 967; 1598 46; 1600 9768; 1601 2; 1602 53; 1604 70; 1606 18
1608 497; 1610 36; 1612 357; 1614 50; 1615 12; 1616 593; 1618 7; 1620 1780
1621 2; 1622 21; 1623 2; 1624 1979; 1626 81; 1627 2; 1628 175; 1629 10
1630 8; 1631 8; 1632 7947; 1634 29; 1635 2; 1636 50; 1637 6; 1638 154
1640 511; 1642 19; 1644 182; 1646 12; 1648 1097; 1649 6; 1650 82; 1652 307
1653 4; 1654 38; 1656 1038; 1658 3; 1659 4; 1660 83; 1662 16; 1664 80065
1666 13; 1668 128; 1669 2; 1670 3; 1671 2; 1672 302; 1674 174; 1676 52
1677 2; 1678 16; 1680 25061; 1682 17; 1684 66; 1686 27; 1688 438; 1690 31
1692 312; 1693 4; 1694 40; 1696 6165; 1698 31; 1700 372; 1702 13; 1703 12
1704 755; 1705 4; 1706 5; 1708 439; 1710 229; 1712 911; 1714 4; 1716 264
1718 9; 1720 589; 1722 41; 1723 6; 1724 67; 1726 116; 1728 15191; 1730 27
1731 4; 1732 35; 1733 4; 1734 24; 1736 2035; 1738 32; 1740 902; 1742 8
1744 576; 1746 178; 1747 4; 1748 62; 1749 8; 1750 109; 1752 735; 1754 8
1755 2; 1756 45; 1757 4; 1758 112; 1760 2901; 1762 2; 1763 2; 1764 356
1766 12; 1767 32; 1768 366; 1770 27; 1771 2; 1772 237; 1774 14; 1776 906
1778 82; 1780 62; 1782 18; 1784 167; 1786 4; 1788 379; 1790 2; 1792 102227
1794 21; 1795 2; 1796 63; 1797 2; 1798 9; 1799 2; 1800 5006; 1802 3
1804 126; 1805 18; 1806 40; 1808 2031; 1810 14; 1812 196; 1813 2; 1814 5
1816 261; 1818 53; 1820 202; 1822 22; 1823 2; 1824 6050; 1826 6; 1828 53
1829 2; 1830 80; 1832 121; 1833 2; 1834 15; 1836 181; 1838 27; 1840 1643
1841 4; 1842 15; 1844 38; 1845 2; 1846 5; 1848 897; 1849 2; 1850 13
1852 71; 1854 27; 1855 20; 1856 40338; 1858 10; 1859 2; 1860 781; 1862 13
1864 3010; 1866 7; 1868 214; 1869 2; 1870 7; 1872 5319; 1874 7; 1875 20
1876 63; 1878 4; 1880 632; 1881 2; 1883 6; 1884 189; 1885 4; 1886 24
1888 2083; 1890 281; 1891 4; 1892 58; 1894 16; 1896 946; 1898 24; 1900 46
1902 15; 1904 1698; 1906 8; 1908 260; 1910 70; 1912 138; 1914 34; 1916 60
1918 4; 1919 2; 1920 94506; 1922 19; 1924 80; 1926 10; 1928 294; 1930 6
1932 134; 1933 2; 1934 4; 1935 6; 1936 1776; 1937 4; 1938 20; 1939 2
1940 301; 1942 1; 1944 297; 1945 2; 1946 8; 1948 17; 1950 30; 1952 8850
1954 31; 1956 243; 1958 13; 1960 441; 1962 8; 1964 34; 1966 28; 1968 580
1970 12; 1972 90; 1974 2; 1976 374; 1978 7; 1980 334; 1982 27; 1984 19586
1986 6; 1988 27; 1989 4; 1990 7; 1992 246; 1996 15; 1998 8; 2000 863
2002 39; 2003 6; 2004 83; 2006 7; 2008 75; 2010 8; 2012 108; 2014 2
2016 6230; 2017 4; 2018 8; 2019 2; 2020 41; 2022 2; 2024 291; 2026 13
2028 82; 2030 16; 2032 435; 2034 27; 2036 15; 2038 2; 2040 870; 2041 8
2042 5; 2044 85; 2046 32; 2048 211416; 2050 8; 2052 240; 2053 2; 2054 4
2056 145; 2058 11; 2060 23; 2062 5; 2064 861; 2066 19; 2068 13; 2070 5
2072 64; 2074 49; 2076 60; 2078 7; 2080 4835; 2082 5; 2084 26; 2086 13
2088 1395; 2090 8; 2092 73; 2094 20; 2096 360; 2098 6; 2100 926; 2102 2
2104 67; 2106 29; 2108 84; 2110 4; 2112 5550; 2114 14; 2116 50; 2118 8
2120 411; 2122 2; 2124 108; 2126 2; 2128 584; 2130 13; 2132 72; 2134 35
2136 128; 2138 4; 2140 60; 2141 4; 2142 20; 2144 627; 2146 19; 2148 25
2150 7; 2151 2; 2152 147; 2153 12; 2154 23; 2156 74; 2160 5083; 2162 14
2164 52; 2166 61; 2168 333; 2170 12; 2172 62; 2174 14; 2176 7660; 2178 15
2179 8; 2180 20; 2182 3; 2184 651; 2186 9; 2187 2; 2188 20; 2190 29
2192 287; 2194 6; 2196 237; 2198 18; 2200 81; 2202 45; 2204 41; 2206 1
2208 1749; 2209 4; 2210 3; 2212 88; 2214 26; 2216 116; 2218 5; 2220 89
2222 2; 2224 245; 2226 4; 2228 44; 2230 5; 2232 970; 2234 2; 2236 40
2238 15; 2240 6176; 2242 2; 2244 32; 2248 80; 2250 18; 2252 13; 2254 3
2256 445; 2258 30; 2260 67; 2262 23; 2264 20; 2266 2; 2268 126; 2271 2
2272 655; 2274 8; 2275 4; 2276 23; 2278 1; 2280 641; 2282 10; 2284 68
2286 2; 2288 474; 2290 6; 2292 22; 2294 2; 2296 126; 2300 31; 2304 19001
2306 9; 2308 15; 2310 66; 2312 61; 2316 38; 2318 2; 2320 2339; 2322 1
2324 14; 2326 1; 2328 475; 2330 97; 2332 32; 2335 6; 2336 593; 2338 1
2340 226; 2342 5; 2344 380; 2346 5; 2348 10; 2350 7; 2352 734; 2353 12
2355 2; 2356 71; 2358 3; 2360 123; 2362 21; 2364 35; 2366 3; 2368 917
2370 25; 2372 16; 2376 268; 2378 5; 2379 4; 2380 47; 2382 6; 2384 446
2386 3; 2388 14; 2389 2; 2390 2; 2392 64; 2394 14; 2396 26; 2400 4868
2402 1; 2404 17; 2406 3; 2408 94; 2410 8; 2412 23; 2416 500; 2418 13
2420 55; 2422 2; 2424 80; 2426 2; 2428 11; 2430 33; 2432 1727; 2434 10
2435 2; 2436 166; 2440 491; 2442 9; 2444 147; 2448 372; 2450 13; 2451 2
2452 5; 2454 7; 2456 34; 2460 41; 2464 1183; 2466 2; 2468 61; 2470 1
2472 153; 2478 3; 2480 840; 2482 1; 2484 14; 2486 5; 2488 33; 2490 13
2492 39; 2494 4; 2496 6481; 2497 2; 2498 1; 2500 33; 2502 11; 2504 33
2506 3; 2508 23; 2512 157; 2514 18; 2516 23; 2520 1506; 2522 3; 2524 17
2526 1; 2528 1362; 2530 4; 2532 32; 2534 3; 2536 14; 2540 15; 2542 4
2544 294; 2548 37; 2550 35; 2552 144; 2554 1; 2556 9; 2558 8; 2560 15613
2562 22; 2564 11; 2568 77; 2570 2; 2572 11; 2574 6; 2576 311; 2577 2
2578 2; 2580 20; 2582 1; 2584 21; 2586 3; 2588 10; 2590 3; 2592 390
2594 1; 2596 20; 2598 4; 2600 90; 2602 1; 2604 83; 2608 45; 2610 6
2612 20; 2614 4; 2616 42; 2618 4; 2620 21; 2622 1; 2624 645; 2626 3
2628 44; 2630 1; 2632 59; 2634 10; 2635 4; 2636 6; 2638 3; 2640 654
2642 5; 2644 1; 2648 20; 2650 1; 2652 25; 2656 140; 2658 6; 2660 26
2662 4; 2664 50; 2666 1; 2668 16; 2672 58; 2676 15; 2678 14; 2680 8
2682 9; 2683 4; 2684 25; 2686 5; 2688 8542; 2692 6; 2694 5; 2696 18
2698 6; 2700 136; 2704 202; 2706 7; 2708 6; 2710 16; 2712 110; 2716 40
2718 8; 2720 499; 2724 51; 2726 3; 2728 131; 2730 9; 2732 12; 2736 193
2740 9; 2744 63; 2748 1; 2750 4; 2752 626; 2754 14; 2756 6; 2760 170
2762 2; 2764 2; 2766 2; 2768 105; 2770 3; 2772 7; 2774 3; 2776 36
2777 2; 2778 2; 2780 12; 2784 3714; 2786 2; 2788 1; 2790 48; 2791 2
2792 20; 2796 126; 2800 532; 2802 7; 2804 2; 2806 4; 2808 253; 2810 2
2812 10; 2816 3205; 2820 17; 2821 8; 2824 22; 2828 10; 2832 188; 2836 10
2838 10; 2840 43; 2842 15; 2844 39; 2848 139; 2850 3; 2852 10; 2856 96
2858 1; 2860 10; 2862 4; 2864 27; 2868 15; 2872 17; 2874 1; 2876 10
2878 1; 2880 8114; 2882 8; 2884 40; 2888 266; 2890 4; 2892 15; 2894 8
2896 87; 2898 2; 2900 26; 2902 2; 2904 69; 2908 1; 2910 10; 2912 671
2914 2; 2916 3; 2920 73; 2924 3; 2928 621; 2930 2; 2932 14; 2934 3
2936 67; 2938 1; 2939 4; 2940 189; 2944 1672; 2948 17; 2952 28; 2954 7
2956 1; 2958 10; 2960 141; 2964 16; 2968 83; 2970 16; 2972 1; 2974 1
2976 1114; 2980 22; 2982 1; 2984 24; 2988 3; 2990 3; 2992 58; 2996 12
3000 225; 3002 5; 3004 7; 3006 6; 3008 392; 3010 8; 3012 11; 3014 2
3016 21; 3017 2; 3018 6; 3020 31; 3024 329; 3028 2; 3030 1; 3032 32
3034 5; 3036 16; 3038 4; 3040 182; 3042 4; 3044 1; 3046 5; 3048 40
3056 34; 3058 4; 3060 24; 3064 9; 3068 14; 3070 6; 3072 18289; 3073 8
3080 5; 3082 3; 3084 4; 3085 8; 3088 86; 3096 70; 3098 3; 3100 12
3102 4; 3104 514; 3108 14; 3112 10; 3114 2; 3116 2; 3120 354; 3124 9
3126 1; 3128 28; 3132 112; 3134 1; 3136 755; 3140 1; 3144 27; 3148 1
3150 61; 3152 39; 3156 5; 3160 84; 3162 6; 3164 14; 3168 366; 3170 8
3172 2; 3174 1; 3176 7; 3178 1; 3180 20; 3184 39; 3186 1; 3188 7
3190 1; 3192 98; 3194 1; 3196 5; 3200 590; 3204 2; 3206 4; 3208 9
3212 5; 3214 3; 3216 48; 3220 1; 3224 39; 3228 14; 3232 68; 3234 1
3236 2; 3240 255; 3242 1; 3244 3; 3248 297; 3252 30; 3256 12; 3258 6
3260 2; 3262 10; 3264 712; 3270 5; 3272 8; 3274 1; 3276 35; 3280 23
3282 1; 3286 2; 3288 14; 3292 4; 3294 12; 3296 112; 3298 1; 3300 7
3304 50; 3306 1; 3308 15; 3312 86; 3320 26; 3324 4; 3328 5614; 3330 3
3332 1; 3336 13; 3338 4; 3340 2; 3342 13; 3344 22; 3348 24; 3352 27
3354 2; 3360 2437; 3364 7; 3368 3; 3372 7; 3376 39; 3380 11; 3384 12
3388 23; 3392 521; 3396 1; 3400 77; 3404 1; 3406 2; 3408 65; 3412 3
3416 52; 3420 10; 3424 88; 3426 12; 3432 25; 3440 52; 3444 4; 3446 1
3448 16; 3452 17; 3454 4; 3456 850; 3458 2; 3460 1; 3464 1; 3466 1
3468 4; 3472 161; 3476 7; 3480 119; 3488 53; 3492 36; 3496 3; 3500 50
3502 1; 3504 60; 3508 4; 3512 23; 3516 19; 3518 3; 3520 257; 3524 4
3528 24; 3530 2; 3532 6; 3534 2; 3536 13; 3540 19; 3544 33; 3548 4
3552 75; 3556 12; 3560 2; 3564 4; 3566 2; 3568 13; 3576 62; 3582 1
3584 5714; 3588 3; 3590 4; 3592 19; 3596 3; 3600 483; 3604 1; 3608 26
3610 14; 3612 9; 3616 241; 3620 14; 3624 38; 3628 1; 3632 22; 3634 1
3636 17; 3638 2; 3640 20; 3644 8; 3648 335; 3656 7; 3660 9; 3662 1
3664 6; 3666 3; 3668 3; 3672 10; 3676 2; 3678 2; 3680 98; 3682 2
3684 1; 3692 2; 3696 46; 3700 3; 3704 4; 3708 7; 3712 4448; 3716 2
3720 84; 3722 1; 3724 2; 3728 500; 3732 1; 3736 30; 3740 3; 3744 458
3752 4; 3754 2; 3756 1; 3760 46; 3762 1; 3766 3; 3768 23; 3772 6
3774 3; 3776 113; 3780 91; 3782 4; 3784 4; 3786 1; 3788 4; 3792 66
3794 3; 3798 1; 3800 5; 3804 2; 3808 164; 3810 2; 3816 14; 3820 7
3824 29; 3828 3; 3836 22; 3840 6211; 3844 4; 3848 4; 3852 1; 3856 13
3860 3; 3864 21; 3868 2; 3872 128; 3880 38; 3884 1; 3888 28; 3890 1
3900 2; 3904 940; 3906 2; 3908 7; 3912 25; 3916 1; 3920 18; 3924 1
3928 1; 3934 1; 3936 46; 3938 6; 3944 9; 3946 2; 3948 3; 3952 16
3954 1; 3956 2; 3960 21; 3964 3; 3968 1245; 3976 1; 3980 1; 3984 20
3992 1; 4000 84; 4002 1; 4004 11; 4008 2; 4012 1; 4016 12; 4018 1
4020 4; 4024 11; 4032 357; 4048 23; 4050 5; 4052 1; 4056 6; 4060 3
4062 1; 4064 21; 4066 1; 4068 8; 4072 4; 4080 73; 4082 2; 4088 5
4092 1; 4096 10935; 4100 1; 4102 4; 4104 20; 4110 1; 4112 8; 4120 1
4128 84; 4132 3; 4134 2; 4140 2; 4144 12; 4146 1; 4148 3; 4152 1
4156 4; 4160 306; 4168 4; 4176 222; 4180 1; 4184 3; 4188 1; 4192 23
4194 5; 4200 146; 4204 1; 4208 8; 4212 10; 4214 1; 4216 14; 4224 318
4228 3; 4232 5; 4234 1; 4238 1; 4240 11; 4244 1; 4248 4; 4250 1
4252 1; 4256 29; 4260 3; 4264 3; 4266 4; 4268 9; 4280 6; 4284 9
4288 28; 4302 1; 4304 6; 4312 11; 4320 399; 4326 16; 4332 21; 4336 50
4340 1; 4344 6; 4352 520; 4356 12; 4358 8; 4368 27; 4376 2; 4380 4
4384 22; 4386 2; 4392 22; 4396 6; 4398 1; 4400 6; 4404 3; 4408 2
4416 154; 4424 18; 4432 4; 4436 1; 4440 2; 4444 3; 4448 14; 4450 12
4456 2; 4464 69; 4472 4; 4480 266; 4488 2; 4494 8; 4496 2; 4500 2
4504 2; 4512 31; 4516 6; 4520 12; 4528 3; 4536 3; 4544 27; 4546 1
4548 4; 4552 3; 4560 31; 4564 1; 4568 5; 4576 29; 4592 4; 4600 2
4608 765; 4612 2; 4616 2; 4620 12; 4624 6; 4632 6; 4640 388; 4648 1
4652 1; 4656 45; 4660 23; 4672 55; 4680 22; 4688 47; 4696 2; 4700 4
4704 29; 4706 8; 4712 11; 4720 2; 4724 7; 4728 2; 4736 56; 4742 1
4744 2; 4752 49; 4768 25; 4772 3; 4776 1; 4784 5; 4792 3; 4800 334
4808 1; 4812 1; 4816 1; 4824 2; 4832 38; 4834 1; 4836 1; 4840 18
4844 4; 4848 1; 4860 12; 4864 72; 4872 4; 4880 51; 4888 19; 4896 31
4912 4; 4920 2; 4928 43; 4936 5; 4944 10; 4956 2; 4960 19; 4968 1
4976 4; 4984 3; 4992 272; 5000 9; 5008 9; 5012 1; 5016 3; 5020 1
5022 1; 5024 1; 5028 4; 5040 58; 5044 1; 5052 1; 5054 2; 5056 84
5064 3; 5088 9; 5096 2; 5100 4; 5104 10; 5120 623; 5124 1; 5136 8
5144 1; 5148 1; 5152 11; 5168 2; 5172 1; 5176 1; 5180 1; 5184 29
5192 2; 5200 1; 5208 3; 5216 2; 5228 1; 5232 1; 5248 26; 5250 4
5264 6; 5272 1; 5280 34; 5284 2; 5288 1; 5294 1; 5300 1; 5312 2
5316 2; 5328 2; 5344 6; 5356 6; 5368 2; 5376 266; 5388 1; 5400 6
5402 1; 5408 1; 5420 2; 5424 4; 5432 6; 5436 4; 5440 37; 5448 2
5456 4; 5460 1; 5472 7; 5480 1; 5488 4; 5504 17; 5520 8; 5536 10
5568 390; 5580 3; 5584 1; 5592 27; 5600 70; 5604 1; 5616 8; 5632 175
5640 6; 5648 3; 5651 2; 5664 9; 5680 15; 5684 5; 5688 3; 5696 1
5712 3; 5728 1; 5730 1; 5740 3; 5760 369; 5768 1; 5776 69; 5784 4
5792 4; 5800 12; 5808 3; 5820 4; 5822 2; 5824 7; 5840 4; 5856 58
5868 2; 5872 2; 5880 7; 5888 75; 5892 1; 5920 9; 5948 1; 5952 36
5960 1; 5964 1; 5984 4; 5992 13; 6000 2; 6016 20; 6024 4; 6040 2
6048 1; 6064 2; 6080 17; 6112 2; 6128 1; 6140 2; 6144 492; 6176 4
6196 3; 6200 1; 6204 2; 6208 30; 6212 1; 6240 9; 6248 2; 6264 5
6272 16; 6300 5; 6336 9; 6368 2; 6372 1; 6384 3; 6400 8; 6432 1
6448 2; 6460 1; 6464 6; 6480 4; 6496 36; 6524 5; 6528 18; 6548 1
6576 1; 6592 5; 6600 1; 6608 1; 6624 2; 6640 4; 6656 184; 6672 2
6680 1; 6696 1; 6720 116; 6736 2; 6752 1; 6784 5; 6800 5; 6816 3
6832 10; 6848 1; 6852 1; 6864 3; 6880 3; 6912 24; 6960 22; 6984 2
7000 2; 7008 1; 7024 2; 7040 7; 7056 1; 7068 2; 7072 1; 7080 2
7104 2; 7128 1; 7152 14; 7168 163; 7200 7; 7220 7; 7232 17; 7264 1
7266 1; 7296 15; 7424 310; 7440 6; 7456 55; 7472 2; 7480 2; 7488 11
7502 2; 7520 2; 7536 4; 7560 10; 7568 2; 7584 3; 7616 9; 7680 232
7728 1; 7760 4; 7766 2; 7776 2; 7808 60; 7812 1; 7920 2; 7936 42
8000 9; 8032 4; 8064 9; 8100 1; 8128 1; 8160 13; 8184 1; 8192 288
8256 8; 8296 5; 8320 12; 8352 10; 8368 2; 8384 1; 8388 2; 8400 7
8448 10; 8480 1; 8640 10; 8672 2; 8700 1; 8704 13; 8716 1; 8768 7
8784 2; 8792 2; 8832 5; 8960 3; 8992 1; 9088 7; 9136 4; 9216 25
9240 1; 9248 1; 9280 21; 9312 3; 9320 2; 9344 6; 9360 3; 9376 1
9472 2; 9504 4; 9728 7; 9984 5; 10080 1; 10112 2; 10240 10; 10336 2
10396 1; 10560 2; 10752 5; 10816 1; 11008 2; 11072 2; 11136 5; 11168 1
11200 4; 11264 3; 11520 4; 11552 2; 11648 1; 11776 5; 11904 2; 12032 2
12288 16; 12416 2; 13184 2; 13440 4; 13600 2; 14304 2; 14848 9; 14912 3
15360 4; 16320 2
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

### A.13 The q3 studies of this filing (new; preregistered before any listed seed ran)

Two studies with the byte-identical registered program `smc.c` of Appendix A.7 (sha256 `685297129cda47b247e6d19b1799d73b198e1511334e161fa7583ef6c1175a65`), same parameters NP = 8192, M = 512, MT = 16384 as study B.
The variant list is a command-line file; the studies change only which variants the tail stage draws W8 from.

**Study G - all-G uniform.** The variant list `allg_classes.txt` (sha256 `04000004e910947dfef57181d24101eb063b61a247823631c179661e95384b46`, 108,936,080 bytes) holds all 12,103,680 variants of G, generated by `genvar.c` below
(the same enumeration as `xtab.py`'s `in_G`: a0 = e4 - C4 for every e4 < 2^29 whose W8x = W8C - e4 satisfies the W8 cell and the three printed two-bit conditions). Verified by `smc -t`: 12,103,680 variants, 0 T8/cell violations;
published-L* rows 4..15 all check, row-16 pair count 1,052,672 exact; F6/F7 sampler violations 0.
Preregistration `PREREG_q3G.txt` (sha256 `258952ec2064d22fb90307fe81f9fa4cd8b45e81bc8c0d661f57b72df1ba4160`), seeds 96000-96127, 128 replicates, all reported, no reruns:

```text
preregistration 2026-10-12: sequential-Monte-Carlo estimate of q3 for the A0-variant attack on 37-step SHA-256
program: smc.c (7319bba's, byte-identical to the Appendix A.7 text embedded in 0db0eeb6's proof.md), lab.h likewise.
parameters (identical to the registered study B): NP = 8192, M = 512, MT = 16384.
the variant-W8 tail draws W8 uniformly at random from allg_classes.txt: **all 12,103,680 variants of the family G** (every
class of G, not a 222-class subset), generated by genvar.c as a0 = e4 - C4P for every e4 < 2^29 whose W8x = W8C - e4
satisfies the W8 cell and three two-bit conditions (verified: NVAR 12,103,680, ./smc -t selftest ok, 0 violations).
sample: replicate seeds 96000..96127 (128 replicates), all reported.
rule: Z_s = the linear estimates of the 128 replicates; LB = mean(Z_s) - t * sd(Z_s) / sqrt(128), t = 2.3483 (one-sided
99%, 127 df); q3_model = LB rounded down to 4 decimals of log2 (face value). Every seed run under this preregistration
is reported; no listed seed may be dropped.
```

Per-replicate log2 estimates (seeds 96000-96127, in order):

```text
-73.990 -74.005 -73.941 -74.011 -73.921 -74.090 -74.062 -74.010 -73.997 -74.005 -74.006 -73.951 -73.959 -74.085 -74.061 -73.953
-73.964 -73.994 -73.937 -73.987 -74.042 -73.958 -74.044 -74.111 -74.040 -74.006 -73.983 -74.017 -73.954 -73.935 -74.046 -73.941
-74.055 -74.045 -73.933 -74.050 -73.941 -73.952 -74.000 -73.976 -74.006 -73.978 -74.078 -73.974 -74.017 -74.105 -73.942 -73.981
-74.058 -73.971 -74.118 -73.971 -74.021 -73.969 -73.992 -73.909 -73.941 -73.953 -74.016 -73.933 -73.990 -73.987 -74.027 -74.052
-74.021 -73.998 -74.064 -74.016 -73.976 -74.034 -73.982 -74.011 -73.976 -73.996 -73.951 -73.992 -74.002 -73.972 -74.004 -74.020
-73.985 -73.952 -74.020 -73.988 -73.976 -74.065 -74.094 -73.971 -74.011 -73.995 -74.001 -74.020 -73.989 -74.041 -73.993 -73.997
-74.086 -74.120 -73.990 -73.957 -74.062 -74.017 -74.009 -73.948 -73.991 -74.036 -73.988 -73.970 -73.919 -73.917 -73.984 -74.003
-73.971 -73.971 -74.011 -74.026 -73.964 -74.005 -73.977 -74.137 -73.976 -73.964 -74.017 -73.988 -73.946 -73.989 -73.951 -74.043

```

Result: mean 2^-73.9992, relative sd 0.0317, one-sided 99% Student lower bound (t = 2.3483, 127 df, the registered value) 2^-74.0088.
Stage means over the 128 replicates (log2): 17: -12.9995, 18: -14.9995, 19: -6.0000, 20: -7.0000, 21: -1.0000, 22: -11.0054, tail -4.0011
(registered study B: 22: -10.998, tail -4.007; the published-W8 paired comparison agrees within 0.01 bit).

`genvar.c` (sha256 `16ba549e7181c51d45327ca1a3818f2ddd56b8e030ad04d0fefdb37be46a7a48`), the all-G variant generator (compiles against the same `lab.h`):

```c
#include "lab.h"
int main(void){
  u32 Ax[13],Ex[13];
  Ax[0]=CV0[3];Ax[1]=CV0[2];Ax[2]=CV0[1];Ax[3]=CV0[0];
  Ex[0]=CV0[7];Ex[1]=CV0[6];Ex[2]=CV0[5];Ex[3]=CV0[4];
  for(int i=0;i<9;i++){
    u32 e=(Ax[i]+Ex[i]+S1(Ex[i+3])+CH(Ex[i+3],Ex[i+2],Ex[i+1])+KC[i]+MX[i]);
    u32 a=(e-Ax[i]+S0(Ax[i+3])+MAJ(Ax[i+3],Ax[i+2],Ax[i+1]));
    Ex[i+4]=e; Ax[i+4]=a;
  }
  u32 A4=Ax[8],A3=Ax[7],A2=Ax[6],A1=Ax[5],E8=Ex[12],E7=Ex[11],E6=Ex[10],E5=Ex[9];
  u32 C4P=A4-S0(A3)-MAJ(A3,A2,A1), W8C=E8-A4-S1(E7)-CH(E7,E6,E5)-KC[8];
  fprintf(stderr,"C4P=%08x W8C=%08x\n",C4P,W8C);
  long n=0;
  for(u64 e4=0;e4<(1u<<29);e4++){
    u32 w=W8C-(u32)e4;
    if((w>>29&1)!=1) continue;
    if(((w>>1)&1)==((w>>12)&1)) continue;
    if(((w>>8)&1)==((w>>25)&1)) continue;
    if(((w>>14)&1)!=((w>>18)&1)) continue;
    u32 a0=(u32)e4-C4P;
    printf("%08x ",a0); n++;
    if(n%16==0)printf("\n");
  }
  fprintf(stderr,"NVAR %ld\n",n);
  return 0;
}
```

**Study K - the examined distribution.** The variant list `keptpool48b.txt` (sha256 `0261ae69022e707eb60c0dfffd59f717ee5759e5adef36ab070fb4cef00b152b`, 82,721,934 bytes, 9,090,990 variant draws) is the kept-fibre-weighted
pool of Section 7.4b: for 64 values of x drawn uniformly on the full 2^32 domain by the LCG below, every variant of a kept fibre (at least THETA = 48 members, fibres merged across classes by equal w6(a0, x, 0)) is emitted once per x.
A variant kept at k of the 64 sampled x values appears k times, so the pool samples the examined law with the correct weights. Built by `pool.c` below from `allg_classes.txt`; per-x kept counts (mean 142,047) bracket the histogram mean
(119,869) within the bursty per-x dispersion. Preregistration `PREREG_q3kept2.txt` (sha256 `bc287f91a8725fa105a6c9cf5b9d7e0fa35ce34480fe22ee28e019a6ae58e61a`), seeds 99000-99063, 64 replicates, all reported, no reruns.

An earlier pool (`keptpool48.txt`, sha256 `8376ccb477ff05e15f61c3ae7b06b936b66602c2cb47ebc5853db306268f0314`, 7,129,386 draws over 64 x, mean 2^-73.9904, bound 2^-74.0061 on 64 replicates, seeds 98000-98063) drew its x values
from the top 31 bits of the LCG state, so every x lay below 2^31: the pool estimated the examined law only on that half-domain. It was caught, re-registered and re-run on the corrected domain; it is kept here for transparency and is
not used for the bound (it agrees with study K2 within 0.008 bit anyway).

```text
PREREG q3 SMC, kept-fibre-weighted variant pool of the x-indexed attack (THETA=48), corrected x domain

Supersedes PREREG_q3kept.txt: the first pool's LCG took the top 31 bits of its 64-bit state, so every x had its
most significant bit zero and the pool sampled x < 2^31 only, not the uniform 2^32 domain the attack draws from.
The same pool.c with the mask corrected to the top 32 bits ((u32)(state>>32)) is used here; the study is
re-registered fresh with a new file and new replicate seeds. The earlier pool and its 64 replicates are kept in
the record for transparency and are not used for the bound.

Pool: for 64 x values drawn by the LCG x_{i+1}=6364136223846793005*x_i+1442695040888963407 (seed 888002, top 32 bits used),
all variants whose c7-class passes W7 at x are grouped into fibres by equal w6(a0,x,0); variants in fibres of >=48
members are emitted once per x (kept-weighted multiset, pool.c).
File: keptpool48b.txt

Rule (fixed in advance): the reported bound is the one-sided 99% Student lower bound on the mean of the 64 linear
estimates (mean minus t_{0.99,63}*sd/sqrt(64), t=2.385), computed on the 'est' (variant-W8) estimates.
All 64 replicates are reported; no reruns, no seed changes. Seeds 99000..99063.
smc.c sha256 685297129cda47b247e6d19b1799d73b198e1511334e161fa7583ef6c1175a65 (unchanged, registered program)
pool.c sha256 0b866300c2180198d4191295ad138bf806076689db9f127641a346e6666acb8c
Command per replicate: ./smc <seed> 8192 512 16384 keptpool48b.txt
```

Per-replicate log2 estimates (seeds 99000-99063, in order):

```text
-74.014 -74.031 -74.029 -74.096 -73.992 -73.949 -73.985 -73.918 -74.004 -73.908 -74.043 -74.035 -74.049 -73.971 -73.918 -73.892
-73.988 -73.956 -73.981 -73.984 -73.988 -73.979 -73.956 -74.102 -73.974 -73.986 -74.052 -73.903 -73.973 -73.998 -73.983 -73.967
-73.941 -73.990 -73.972 -73.913 -73.935 -73.971 -74.051 -74.063 -73.894 -74.026 -74.027 -74.035 -74.010 -73.960 -73.963 -73.902
-73.969 -73.967 -74.044 -73.956 -74.043 -73.959 -73.997 -73.882 -74.030 -73.983 -73.993 -73.941 -74.046 -74.053 -73.969 -73.874

```

Result: mean 2^-73.9829, relative sd 0.0358, one-sided 99% Student lower bound (t = 2.385, 63 df, the registered value) 2^-73.9984.
Stage means over the 64 replicates (log2): 17: -13.0000, 18: -14.9979, 19: -6.0000, 20: -7.0001, 21: -1.0000, 22: -10.9974, tail -3.9940.

`pool.c` (sha256 `0b866300c2180198d4191295ad138bf806076689db9f127641a346e6666acb8c`), the kept-weighted pool builder:

```c
/* pool.c - emit the kept-fibre (THETA-weighted) variant pool of the x-indexed
   table attack on 37-step SHA-256, in the smc classes.txt format.
   For each of NX uniform x values (LCG below), a variant a0 is emitted iff
   c7(a0)-x is in F7 (its class passes W7 at x) and its fibre
   {a0' passing : w6(a0',x,0) = w6(a0,x,0)} has at least THETA members.
   A variant kept at k sampled x values appears k times: the pool samples the
   examined distribution, weighted by kept-fibre membership (P6-independent).

   usage: pool classes.txt nx theta seed > pool.txt
   Input format per line: <tag> <count> <a0> <a0> ...   (tag ignored)
*/
#include "lab.h"
#include <string.h>
#include <stdlib.h>

/* state constants of the r37 pair (identical to xtab.py / genvar.c) */
static const u32 A1c=0x62827866,A2c=0x987f24c4,A3c=0x44294b96,A4c=0xa8ccc9b3;
static const u32 E5c=0xe7f2c81f,E6c=0xeb0b9c2d,E7c=0x9a404eb1;
static const u32 C4=0x000b362e,W8C=0xda3a7d2f,K3C=0x478132ed,C6=0xf538a8f7;

static inline int in_G(u32 a0){
  u32 e4=a0+C4; if(e4>>29)return 0; u32 w=W8C-e4;
  return ((w>>29)&1)==1 && ((w>>1)&1)!=((w>>12)&1) && ((w>>8)&1)!=((w>>25)&1) && ((w>>14)&1)==((w>>18)&1);
}
static inline u32 k3of(u32 a0){return K3C-MAJ(A2c,A1c,a0);}
static inline u32 c7of(u32 a0){
  u32 e4=a0+C4;
  return E7c-A3c-k3of(a0)-S1(E6c)-CH(E6c,E5c,e4)-KC[7];
}
static inline u32 w6of0(u32 a0,u32 x){ /* w6of(a0,x,0) */
  u32 e4=a0+C4,e3=k3of(a0)+x;
  return C6+MAJ(A1c,a0,x)-CH(E5c,e4,e3);
}

int main(int argc,char**argv){
  if(argc<5){fprintf(stderr,"usage: pool classes.txt nx theta seed\n");return 1;}
  const char*path=argv[1]; long nx=atol(argv[2]); u32 TH=(u32)atol(argv[3]);
  u64 seed=strtoull(argv[4],0,10);
  FILE*f=fopen(path,"r"); if(!f){fprintf(stderr,"cannot open %s\n",path);return 1;}
  long cap=1<<22; u32*A=malloc(cap*4); long N=0; char*line=NULL; size_t lc=0;
  while(getline(&line,&lc,f)>0){
    char*tok=strtok(line," \n"); if(!tok)continue; tok=strtok(NULL," \n"); long n=atol(tok);
    for(long i=0;i<n;i++){tok=strtok(NULL," \n"); u32 a0=(u32)strtoul(tok,NULL,16);
      if(N==cap){cap*=2;A=realloc(A,cap*4);} A[N++]=a0;}
  }
  fclose(f);
  fprintf(stderr,"loaded %ld variants\n",N);
  /* verify the family */
  {long bad=0; for(long i=0;i<N;i++)bad+=!in_G(A[i]); fprintf(stderr,"in_G violations %ld\n",bad);}

  /* scratch buffers: passing phi+variant pairs, then a sort by phi */
  u32*PH=malloc(N*4); u32*ID=malloc(N*4); u32*KP=malloc(N*4);
  long tot=0;
  for(long ix=0;ix<nx;ix++){
    seed=seed*6364136223846793005ull+1442695040888963407ull; u32 x=(u32)(seed>>32);
    long np=0;
    for(long i=0;i<N;i++){
      u32 a0=A[i];
      if(!inF7(c7of(a0)-x))continue;          /* class passes W7 at x */
      PH[np]=w6of0(a0,x); ID[np]=a0; np++;
    }
    /* sort by phi: counting via qsort on packed (phi,a0) is heavy; use radix on phi */
    /* simple approach: 2-pass radix on 32-bit phi */
    static u32 cnt[65536]; u32*t1=malloc(np*4),*t2=malloc(np*4);
    for(int pass=0;pass<2;pass++){
      int sh=pass*16; memset(cnt,0,sizeof cnt);
      for(long i=0;i<np;i++)cnt[(PH[i]>>sh)&65535]++;
      long s=0; for(int b=0;b<65536;b++){u32 c=cnt[b];cnt[b]=s;s+=c;}
      for(long i=0;i<np;i++){long p=cnt[(PH[i]>>sh)&65535]++;t1[p]=PH[i];t2[p]=ID[i];}
      memcpy(PH,t1,np*4);memcpy(ID,t2,np*4);
    }
    free(t1);free(t2);
    /* run-length over phi: keep members of runs >= TH */
    long nk=0;
    for(long i=0;i<np;){long j=i+1;while(j<np&&PH[j]==PH[i])j++;
      if(j-i>=(long)TH)for(long k=i;k<j;k++)KP[nk++]=ID[k];
      i=j;}
    tot+=nk;
    /* emit one smc-format line */
    printf("x %ld",nk);
    /* chunk to keep line length sane handled by reader (count then a0s) */
    for(long k=0;k<nk;k++)printf(" %08x",KP[k]);
    printf("\n");
    fprintf(stderr,"x %ld pass %ld kept %ld\n",ix,np,nk);
  }
  fprintf(stderr,"total kept %ld\n",tot);
  return 0;
}
```

The two data files are larger than this appendix can hold (109 MB and 83 MB); they are reproduced byte-identically by:
`cc -O2 -o genvar genvar.c` then `./genvar > raw.txt` formatted to `<tag> <count> <a0 ...>` lines (allg_classes.txt);
`cc -O2 -o pool pool.c` then `./pool allg_classes.txt 64 48 888002 > keptpool48b.txt`. The sha256 sums above identify them.
Per-replicate full outputs (RESULT/STAGES lines): study G 128 files and study K 64 files, regenerated by `./smc <seed> 8192 512 16384 <list>`; the first of each:

```text
seed 96000 NP 8192 M 512 MT 16384 NVAR 12103680 pairs 1052672
stage 17 pass 262496 mean_log2 -12.99806
stage 18 pass 529824 mean_log2 -14.98485
stage 19 pass 4194304 mean_log2 -6.00000
stage 20 pass 2097204 mean_log2 -6.99996
stage 21 pass 4194304 mean_log2 -1.00000
stage 22 pass 2041 mean_log2 -11.00494
tail variant passes 8345994 of 134217728  mean_log2 -4.00735 ; published-W8 passes 510 of 8192 mean_log2 -4.00565
RESULT seed 96000 est 5.3324887148094839e-23 log2est -73.98954 estpub 5.3387795992608765e-23 log2estpub -73.98784
STAGES -16.99438 -12.99806 -14.98485 -6.00000 -6.99996 -1.00000 -11.00494 tail -4.00735


```
```text
seed 99000 NP 8192 M 512 MT 16384 NVAR 9090990 pairs 1052672
stage 17 pass 262762 mean_log2 -12.99660
stage 18 pass 525068 mean_log2 -14.99786
stage 19 pass 4194304 mean_log2 -6.00000
stage 20 pass 2098581 mean_log2 -6.99902
stage 21 pass 4194304 mean_log2 -1.00000
stage 22 pass 2024 mean_log2 -11.01701
tail variant passes 8335667 of 134217728  mean_log2 -4.00913 ; published-W8 passes 479 of 8192 mean_log2 -4.09612
RESULT seed 99000 est 5.2428639647750407e-23 log2est -74.01399 estpub 4.9360969976680661e-23 log2estpub -74.10098
STAGES -16.99438 -12.99660 -14.99786 -6.00000 -6.99902 -1.00000 -11.01701 tail -4.00913

```

**Study K3 (stratified per x; the headline examined-law bound).** The bound of study K treats its 64-x pool as fixed: the Student bound covers the replicate draws but not the
error of having sampled 64 of the 2^32 values of x. Study K3 measures that second error source on the *same* registered pool `keptpool48b.txt` (sha256
0261ae69022e707eb60c0dfffd59f717ee5759e5adef36ab070fb4cef00b152b): the file's 64 lines are split into per-x lists `poolx_00.txt` .. `poolx_63.txt` (line i+1 becomes file i, in the
registered LCG order; 20 of the 64 sampled x's have non-empty kept lists — the kept-mass concentration of Section 13.3). For each non-empty file, 8 replicates of the registered
program were run before unblinding (preregistration PREREG_q3kept3.txt, sha256 8d70a744108757fc74b3b6ab6d27643adfd0050308d25b5876bcf6a83ea0ca8e): seeds 87000+8k+j, j = 0..7,
k enumerating the non-empty files in order, NP = min(8192, nk_i), M = 512, MT = 16384 — 160 replicates in all, all reported below. Per file, m_i = the mean of its 8 linear
estimates; the cluster ratio estimator over the 64 sampled x's (empty files contribute Y_i = X_i = 0) is R = sum_i nk_i m_i / sum_i nk_i = 2^-73.99526, with the one-stage
cluster standard error se^2 = sum_i (nk_i (m_i - R))^2 / (64 x 63 x mean_X^2), mean_X = 142,046.7: relative se 0.0040, and the registered bound R - t_0.99,63 se =
**2^-74.00899 -> 2^-74.009** (t = 2.385). The per-x means are homogeneous — m_i between 2^-73.968 and 2^-74.034 — so the finite-64-x error is small; the bound covers both error
sources and is the headline examined-law bound of Section 7.4b. Sample output (seed 87000, file poolx_01.txt, nk_1 = 184,944):

```text
seed 87000 NP 8192 M 512 MT 16384 NVAR 184944 pairs 1052672
stage 17 pass 261902 mean_log2 -13.00133
stage 18 pass 517709 mean_log2 -15.01822
stage 19 pass 4194304 mean_log2 -6.00000
stage 20 pass 2096843 mean_log2 -7.00021
stage 21 pass 4194304 mean_log2 -1.00000
stage 22 pass 2023 mean_log2 -11.01772
tail variant passes 8654740 of 134217728  mean_log2 -3.95494 ; published-W8 passes 447 of 8192 mean_log2 -4.19587
RESULT seed 87000 est 5.3426193180624552e-23 log2est -73.98680 estpub 4.520928795491195e-23 log2estpub -74.22773
STAGES -16.99438 -13.00133 -15.01822 -6.00000 -7.00021 -1.00000 -11.01772 tail -3.95494
```

Per-file means m_i (log2 of the linear mean of the 8 replicates; `nk` = kept variants of that x; `range` = min..max log2est of the file's replicates):

```text
file i   nk_i     log2 m_i   replicate log2est range
 1       184944   -73.9533   -74.028..-73.907
 5         1896   -74.0307   -74.295..-73.849
 7        22272   -74.0036   -74.044..-73.946
 8       630848   -73.9895   -74.049..-73.944
11        51168   -73.9972   -74.026..-73.952
13       675524   -73.9775   -74.016..-73.935
14       805888   -74.0052   -74.052..-73.941
27       182400   -74.0054   -74.106..-73.890
33       243792   -73.9958   -74.075..-73.857
35      1511954   -74.0113   -74.121..-73.956
42       429896   -73.9701   -74.045..-73.917
43       824256   -74.0335   -74.081..-73.963
44      1421056   -73.9888   -74.081..-73.928
45       362464   -73.9985   -74.084..-73.891
46       210160   -73.9824   -74.083..-73.920
48        95276   -74.0119   -74.045..-73.975
49       199754   -74.0132   -74.116..-73.932
53       144240   -73.9845   -74.067..-73.907
57       886226   -73.9678   -74.035..-73.915
63       206976   -73.9988   -74.046..-73.957
```

The mean and bound are computed on the linear estimates (not on the log2 column, which is shown for inspection).

## Appendix B. ffbe30bb (the base): the four accepted value patterns of rows 18 and 19

(ffbe30bb's record, kept as filed: "this derivative" here means ffbe30bb. Its ledger figures in B.4 (mu0, Pcap) are superseded by Section 10 and Appendix C; its program description in B.1 is extended by Appendix D.1.)

### B.1 The change in the program

Table 15's E cells of rows 18 and 19 are `==10===uu====0==n===111===01==1=` and `==1====00====1==0==========1====` (Section 3.2). Their characters `1` and `0` at the bit positions E18[29], E18[28], E18[18], E18[11], E18[10], E18[5], E18[1] and E19[29] are the eight value bits. In `experiments/xtab.py` the strings of `CHE[18]` and `CHE[19]` are now

```text
 row 18   Table 15 ==10===uu====0==n===111===01==1=     program =======uu=======n=====1====1====
 row 19   Table 15 ==1====00====1==0==========1====     program =======00====1==0==========1====
```

(the remaining `1` of row 18 are E18[9] and E18[4], which stay imposed; so do the differences `u`, `n` and every other character). That is the whole change to the counted program: `row_ok` tests the masks and values of the cells as constants of the straight-line text, so the operation counts of Section 9 (`ROWCHECK = 53`, `ROWCOMP = 106` per row) and the ledger's `c3b_row` are unchanged;
no operation was added and none removed. The six parity conditions are not tested separately: the exact signed-difference check of both members that `row_ok` always made, at row 19 and row 21, rejects the other patterns (the SMC stage counts of Appendix B.3 show it: of the 128 patterns of E18's seven bits the check at row 19 lets 4 through, one child in 32, and the bit E19[29] is rejected at row 21 for one child in 2), and a separate test would only add operations.
The patterns the program accepts, as flips of the Table 15 values (E18 bits 29,28,18,11,10,5,1 | E19 bit 29), are the table's own pattern and three others, each determined by its own flips:

| pattern | name | flipped bits of Table 15's values | `xtab.py` flip masks (E18, E19) | value bits as a string (E18[29,28,18,11,10,5,1] E19[29]) |
|---|---|---|---|---|
| 0 | Table 15 | none | 0x00000000, 0x00000000 | 1 0 0 1 1 0 1 \| 1 |
| 1 | G1 | E18[5], E18[10], E18[18], E18[29], E19[29] | 0x20040420, 0x20000000 | 0 0 1 1 0 1 1 \| 0 |
| 2 | G2 | E18[1], E18[5], E18[11], E18[18], E18[28] | 0x10040822, 0x00000000 | 1 1 1 0 1 1 0 \| 1 |
| 3 | G1 xor G2 | E18[1], E18[10], E18[11], E18[28], E18[29], E19[29] | 0x30000c02, 0x20000000 | 0 1 0 0 0 0 0 \| 0 |

The organizer experiment `a0-sfs-r37` imposes pattern t mod 4 on its construction of trial t (constants `IMP` and `PAT` in `xtab.py`; the proposals of rows 18 and 19 impose the pattern's eight values, as the base imposed Table 15's), and checks every cell of rows -4..36 with the program's own `row_ok`, which now accepts all four. For trials 0..15 the constructed chaining value is then fed to the counted online program, which must find exactly the constructed pair (Section 13.2).
The base's program rejects the pairs of patterns 1, 2 and 3 (checked on the three pairs of B.2 below and on the pairs of the experiment).

### B.2 Evidence that exactly four patterns are feasible

All items of this subsection are a re-run of a solver study (GPT Luna's verified 37-step model, Bitwuzla 0.9.1 and Z3 5.1.0) on the published dense part; they explain and corroborate the SMC measurement of B.3, which does not use the solver and is the evidence the charge rests on.

- **The model.** Both executions of the 37-step compression with exact modular additions; the published dense part (A0..A15, E4..E15, W8..W15 of Table 17) fixed; W6, W7, W16..W21 free (W0..W5 recovered by inversion); every cell of Table 15 and every relation of Table 16 for rows 16..36 kept (A15[29] = A17[29] as corrected, Section 3.3). The model reproduces the published pair (SAT, 3.2 s, the pair verifies).
- **Nothing else is removable.** Of the 74 conditions of rows 16..36 (52 value bits and 22 two-bit relations), each flipped alone makes the system UNSAT (74 of 74, longest 3.03 s; Z3 agrees on the smaller cases), including the seven value conditions of rows 20..22 (E20[10], E20[11], E20[15], E20[23], E20[24], E21[29], E22[29]) that another model's sampling had suggested were unforced; all seven flipped together: UNSAT; and by a hand check of the signed differences each of them is required (step 21 needs dE17 + dS1(E20) + dCh(E20,E19,E18) = 0 and the five bits E20[10,11,15,23,24] fix the signs of dS1; E21[29] enters step 22, E22[29] step 23). Exact enumeration of all 2^32 values of W20 for 23 conforming prefixes gives the same number of continuations with and without those conditions imposed.
- **Four patterns.** Dropping the 52 value bits of rows 16..36 at once (differences and the 22 relations kept) and enumerating all solutions over the 52 deviation bits gives exactly four feasible deviation patterns: none, G1 = {E18[5], E18[10], E18[18], E18[29], E19[29]}, G2 = {E18[1], E18[5], E18[11], E18[18], E18[28]} and G1 xor G2 = {E18[1], E18[10], E18[11], E18[28], E18[29], E19[29]};
  dropping the 22 relations as well (74 bits) still gives exactly these four. The value bits E18[1,5,10,11,18,28,29] enter only through the signs of dS1(E18) at step 19 (each output bit of S1 is the XOR of three taps, and the sign of the difference at that bit depends on the XOR of the two taps that carry no difference) and E19[29] only through E18[29] ^ E19[29] = 0 in dCh(E19,E18,E17) at step 21.
  That is a 2-dimensional affine set, equivalent to the six parity conditions of the header. With the signed cells of rows 14 and 15 and all of rows 16..21 kept but the dense values free, the same enumeration again gives exactly four patterns; with the cells of rows 12..15 removed as well it gives 128 (so the count depends on the characteristic's differences, not on the dense values).
- **Three further 37-step semi-free-start collisions**, one per new pattern, each verified by compressing both messages 37 steps (equal 256-bit outputs) and by the program's `row_ok` over rows -4..36 (the new cells accept them, the base's reject them; checked with this package's `xtab.py` and the base's). Words are given MSB first as in Section 3.4; the chaining value is common, x = M', y = M.

```text
G1   CV 063c3500 078f49ec 15f3f954 b92ec209 8988f13d 35819c7c 63e0bf72 236a0c73
     M  da42b17c 211c7ff3 76ab73f3 6af71849 370eee2f 309c7244 fca0a79d c81ace78 9f0d78e1 681b8277 faa9c7e0 56aed439 cc2dbbc2 dd2ba0fc b95d377b 5dd43a81
     M' da42b17c 211c7ff3 76ab73f3 6af71849 370eee2f 309c7244 dca0a79d cc5ac678 bf0d78e1 6d1a90dd faa1d3e0 56aed439 cc2dbbc2 dd2ba0fc bd1d3f7b 7dd43a81
G2   CV 3c2679fb 0adeef20 3589a7a5 83ef1642 ad5f1106 e029b47e 6b4d40e9 4ee553b3
     M  3bfa2198 3aeec0b8 10348d11 5ba77ac0 b56da910 6997b907 395831ab 9230897d 9f0d78e1 681b8277 faa9c7e0 56aed439 cc2dbbc2 dd2ba0fc b95d377b 5dd43a81
     M' 3bfa2198 3aeec0b8 10348d11 5ba77ac0 b56da910 6997b907 195831ab 9670817d bf0d78e1 6d1a90dd faa1d3e0 56aed439 cc2dbbc2 dd2ba0fc bd1d3f7b 7dd43a81
G12  CV a49c8638 3696c10f 2a0f741c 55456216 c7b75338 54905dab c30d520e e749445c
     M  bb6ca525 d640983d 28963f42 5ca2459f 116481ee 4e1a472b edfab13a 29ba7d40 9f0d78e1 681b8277 faa9c7e0 56aed439 cc2dbbc2 dd2ba0fc b95d377b 5dd43a81
     M' bb6ca525 d640983d 28963f42 5ca2459f 116481ee 4e1a472b cdfab13a 2dfa7540 bf0d78e1 6d1a90dd faa1d3e0 56aed439 cc2dbbc2 dd2ba0fc bd1d3f7b 7dd43a81
```

  The digests are c620f218888e2f8c1d2789598cac47b447f6af47b99e1f4f184e50d0a8079905 (G1), 88b85c49b1307244db554e5340c7e9dfc00163e14b81f2fb236db34d7dd8fc59 (G2) and 420db0b04932e6288e98650a154d4e67abc1b7c63050ebae5b18b8f090b6b62f (G12), all 37-step semi-free-start collisions (not ordinary collisions).
- **Exact stage measurement.** For 199 uniform prefixes through row 17 (all W16 passing row 16, a random one; all 2^32 W17, a random one passing row 17) every one of the 2^32 values of W18 was enumerated with the seven E18 bits dropped from row 18 and step 19's output difference tested: per prefix 2^24 values pass row 18, about 2^19 of them also give dE19 = dA19 = 0, in the four patterns in shares 0.237 / 0.256 / 0.263 / 0.244;
  the Table 15 pattern gets 137,933 = 2^17.074 on average (0 for 26.6 percent of the prefixes) of a total of 524,319 = 2^19.0001. Ratio 3.80, that is 1.93 bits (bootstrap 95 percent interval 1.78 to 2.09), against the structural 2.00.

### B.3 The q3 studies of this derivative (preregistered before any listed seed ran)

The program is the base's `smc.c` (Appendix A.7; sha256 `685297129cda47b247e6d19b1799d73b198e1511334e161fa7583ef6c1175a65`, byte-identical) compiled with `cc -O2 smc.c -lm`; the header `lab.h` is the base's (sha256 `bdefd6747d41727a378bc124c241db1f635275d3a2901b96a1c6c6b0e5c5e456`) with exactly the two lines of the cell table changed as in B.1
(sha256 of the changed header `4dd73de5c7addcd4bf5519781151b4a7813dd233bd6098df194e2dd253fec1b3`):

```text
-{18,"==10===uu====0==n===111===01==1="},
+{18,"=======uu=======n=====1====1===="},
-{19,"==1====00====1==0==========1===="},
+{19,"=======00====1==0==========1===="},
```

Nothing else is different: every other cell, every printed two-bit condition (`X2`), the `+` equalities and the exact y-member difference check of every row stay in force, so a particle survives rows 18..21 only if its eight bits make the signed differences cancel. The importance weight of rows 17..21 is 2^-f with f the number of imposed bits of the row's E cell, now 5 (instead of 12) at row 18 and 5 (instead of 6) at row 19.
*Reproduction control:* with the base's `lab.h` and its all-family list, seed 96000 reproduces the base filing's replicate (log2 -73.98954, stages 17..22 -12.99806 -14.98485 -6.00000 -6.99996 -1.00000 -11.00494, tail -4.00735) to the printed digit. *Pilot, disclosed and not part of any study:* one run, seed 5, all-family list, changed `lab.h`: log2 -71.98391 (stage 18: -8.00020, stage 19: -9.99438, stage 21: -1.97729).

**Preregistration** (the file `PREREG_q3R.txt`, sha256 5255e36eab518e7fb2845919165e15e1db0ed494afd6cbdb13d0126c14aabeda, written at 2026-10-12T03:12:10Z before any listed seed ran; reproduced here):

```text
preregistration: sequential-Monte-Carlo estimate of q3 for the A0-variant attack on 37-step SHA-256 when the alternative value patterns of rows 18 and 19 are accepted
written before any listed seed was run; the date and time stamp of this file are given by the line "stamp" below.
stamp: 2026-10-12T03:12:10Z
change from the registered studies of the base filing: ONE. Table 15 rows 18 and 19 of the E cell fix the value bits E18[1]=1, E18[5]=0, E18[10]=1, E18[11]=1, E18[18]=0, E18[28]=0, E18[29]=1 and E19[29]=1.
lab.h here (lab_relaxed.h, sha256 4dd73de5c7addcd4bf5519781151b4a7813dd233bd6098df194e2dd253fec1b3) replaces these eight characters by '=' in the two strings of CHE and changes nothing else; the base lab.h has sha256 bdefd6747d41727a378bc124c241db1f635275d3a2901b96a1c6c6b0e5c5e456.
program: smc.c, byte-identical to the base filing's (sha256 685297129cda47b247e6d19b1799d73b198e1511334e161fa7583ef6c1175a65); every other cell, every printed two-bit condition, and the exact difference
check of the y member (rowy) of every row stay in force, so a particle survives rows 18..21 only if its E18/E19 bits make the signed differences cancel (the alternative patterns), and the program itself decides
which patterns do. Reproduction control: the unchanged lab.h with seed 96000 on the whole family reproduces the base filing's replicate (log2est -73.98954) to the printed digit.
parameters (identical to the base filing's studies): NP = 8192, M = 512, MT = 16384 (study K3: NP = min(8192, nk_i)).
pilot (disclosed, not part of any study): one run, seed 5, whole-family list, relaxed lab.h: log2est -71.98391 (stages 18: -8.00020, 19: -9.99438, 21: -1.97729). Seeds 5 is not used below.
variant lists (same files as the base filing; hashes): allg_classes: all 12,103,680 variants of G generated by genvar.c (sha256 16ba549e7181c51d45327ca1a3818f2ddd56b8e030ad04d0fefdb37be46a7a48 for the source), one line "g 12103680 a0 a0 ...";
keptpool48b.txt: ./pool allg_classes.txt 64 48 888002 (pool.c sha256 0b866300c2180198d4191295ad138bf806076689db9f127641a346e6666acb8c), output sha256 0261ae69022e707eb60c0dfffd59f717ee5759e5adef36ab070fb4cef00b152b (9,090,990 variant draws; the same hash as the base filing's pool).
study G (whole family G, uniform): seeds 61000..61127 (128 replicates). bound LB_G = mean(Z) - 2.3483 sd(Z)/sqrt(128), Z the linear 'est' values.
study K (kept-fibre-weighted pool): seeds 62000..62063 (64 replicates). bound LB_K = mean(Z) - 2.385 sd(Z)/sqrt(64).
study K3 (per-x lists poolx_i.txt = line i of keptpool48b.txt, empty lines skipped, 20 non-empty files in order of i): seeds 63000 + 8k + j for the k-th non-empty file (k = 0..19) and j = 0..7 (160 replicates), NP = min(8192, nk_i).
 per file m_i = mean of its 8 linear estimates; cluster ratio estimator over all 64 sampled x (empty files contribute 0): Y_i = nk_i m_i, X_i = nk_i, R = sum Y_i / sum X_i,
 se^2 = sum_i (Y_i - R X_i)^2 / (64 x 63 x meanX^2), meanX = sum X_i / 64, LB_K3 = R - 2.385 se.
rule (fixed in advance): q3_model_log2 = floor(100 x log2(min(LB_G, LB_K, LB_K3))) / 100 (rounded down to two decimals of log2, that is, never rounded up). The charge in the filing is q3 = 2^q3_model_log2.
every listed seed is run and reported; no seed is dropped, replaced or rerun, whatever the result. Failed (crashed) runs are reported as such and would be re-run with the same seed only if the crash is not a property of the program.
the E18/E19 pattern diagnostic (a separate program, smc_pat.c, which is smc.c plus a histogram of the 8 value bits of the surviving particles after row 21) is a description, not part of the bound.
```

**Variant lists.** Study G: all 12,103,680 variants of G, generated by `genvar.c` (Appendix A.13; sha256 of the source `16ba549e7181c51d45327ca1a3818f2ddd56b8e030ad04d0fefdb37be46a7a48`) and written as one line `g 12103680 a0 a0 ...` (sha256 of the file `05d967567f56d5c61359e21156397da2cf5b995f477f91254d2b643facc77319`). Studies K and K3: the pool `keptpool48b.txt` built by `./pool allg_classes.txt 64 48 888002` from `pool.c` (Appendix A.13; source sha256 `0b866300c2180198d4191295ad138bf806076689db9f127641a346e6666acb8c`):
its sha256 is `0261ae69022e707eb60c0dfffd59f717ee5759e5adef36ab070fb4cef00b152b`, 9,090,990 variant draws over 64 uniform values of x, the same hash as the base filing's pool.

**Results.**

| study | replicates | seeds | mean of the linear estimates | relative sd (K3: relative se) | one-sided 99 percent lower bound |
|---|---|---|---|---|---|
| G, all of G | 128 | 61000-61127 | 2^-71.9901 | 0.0758 | **2^-72.0129** (t = 2.3483) |
| K, kept-weighted pool | 64 | 62000-62063 | 2^-72.0034 | 0.0765 | **2^-72.0367** (t = 2.385) |
| K3, stratified per x | 160 | 63000-63159 | R = 2^-71.98731 | 0.0081 | **2^-72.0155** (t = 2.385) |

Rule applied (fixed in advance): the lowest bound, 2^-72.0367, rounded down to two decimals of log2: **q3_used = 2^-72.04**. The base's charge for the Table 15 pattern was 2^-74.02, so the gain is 1.98 bits against a structural value of 2.00 and an exact-enumeration value of 1.93 (1.78 to 2.09).
Stage means over the replicates (log2): study G: rows 16..22 16: -16.994 17: -13.000 18: -8.000 19: -10.007 20: -7.000 21: -1.999 22: -10.997, tail -3.997; study K: rows 16..22 16: -16.994 17: -13.000 18: -8.000 19: -10.010 20: -7.000 21: -2.004 22: -10.998, tail -4.001; study K3: rows 16..22 16: -16.994 17: -13.000 18: -8.000 19: -10.002 20: -7.000 21: -2.002 22: -11.005, tail -4.004. The base's studies: 16: -16.994, 17: -13.000, 18: -15.00, 19: -6.000, 20: -7.000, 21: -1.000, 22: -11.00, tail -4.00.
Rows 18+19 contribute -15.00 - 6.00 = -21.00 in the base and -18.01 here, row 21 -1.00 in the base and -2.00 here: the net change of the product of stage means is 1.98 bits. The stages of rows 17, 20, 22 and the tail agree with the base's within the sampling resolution.
*Pattern diagnostic* (a separate program `smc_pat.c` = `smc.c` plus a histogram of the eight value bits of the 8192 particles that passed rows 16..22; seeds 11, 12, 13; the bit string is E18[1,5,10,11,18,28,29] as bits 0..6, E19[29] as bit 7, in hexadecimal; Table 15's pattern is cd, G1 = 1b, G2 = f6, G1 xor G2 = 20): seed 11: 1b:1886 20:1843 cd:2476 f6:1987; seed 12: 1b:2100 20:1529 cd:2261 f6:2302; seed 13: 1b:2026 20:2700 cd:1846 f6:1620. Exactly the four predicted patterns occur in every run and no other (counts of the 8192 particles, hexadecimal pattern:count; this diagnostic used the first 4 MB of the variant list and MT = 16, since only rows 16..22 are inspected).

All 128 log2 estimates of study G (seeds 61000-61127, in order):

```text
-71.928 -71.959 -71.999 -71.945 -72.075 -72.116 -71.870 -71.861 -71.946 -71.971 -72.091 -71.911 -71.878 -72.066 -72.195 -71.941
-71.896 -72.084 -72.103 -72.132 -72.011 -72.018 -71.934 -71.790 -71.762 -72.040 -71.938 -71.979 -72.002 -71.969 -72.164 -72.034
-71.748 -72.107 -72.040 -71.993 -72.015 -72.098 -72.193 -71.984 -71.985 -71.901 -72.024 -71.984 -71.878 -71.946 -71.969 -71.903
-72.183 -72.259 -72.053 -72.027 -72.007 -71.936 -71.856 -71.965 -72.086 -72.019 -71.845 -71.963 -72.023 -71.873 -71.967 -72.116
-71.938 -72.080 -71.865 -71.951 -71.997 -72.026 -71.935 -72.088 -72.077 -71.869 -71.957 -72.150 -71.907 -71.955 -72.024 -71.631
-72.012 -72.196 -72.050 -71.997 -72.091 -71.995 -72.027 -71.964 -71.930 -72.032 -71.971 -72.051 -72.092 -71.914 -72.069 -71.842
-72.088 -71.969 -72.112 -72.209 -71.871 -71.919 -71.968 -72.146 -72.095 -71.996 -72.191 -71.832 -72.080 -71.820 -72.000 -71.815
-72.174 -71.948 -71.852 -72.105 -71.774 -72.151 -71.830 -72.040 -72.027 -72.138 -72.024 -72.000 -71.921 -72.026 -71.950 -71.940
```

All 64 log2 estimates of study K (seeds 62000-62063, in order):

```text
-71.979 -72.215 -71.996 -71.890 -72.043 -72.046 -72.113 -71.922 -72.093 -72.141 -72.060 -72.007 -71.827 -71.907 -71.880 -72.059
-72.025 -72.118 -72.241 -71.804 -72.056 -72.176 -71.894 -72.009 -71.833 -71.922 -72.084 -71.909 -72.075 -71.862 -72.179 -72.190
-71.776 -71.991 -71.828 -72.010 -72.056 -72.128 -72.188 -71.995 -71.827 -71.965 -71.982 -71.946 -72.082 -72.030 -71.868 -72.071
-72.020 -72.026 -72.007 -71.910 -72.067 -71.854 -72.015 -72.020 -72.051 -71.931 -71.998 -71.980 -72.018 -71.998 -72.238 -72.059
```

Study K3: the pool's 64 lines are split into per-x lists (20 of the 64 sampled x have non-empty kept lists), 8 replicates each (seeds 63000 + 8k + j, k the index among the non-empty files, NP = min(8192, nk_i)). Per file: nk_i, the log2 of the mean m_i of its 8 linear estimates, and the range of the replicates' log2 estimates:

```text
file i   nk_i     log2 m_i   replicate log2est range
 1     184944   -72.0135   -72.18511310207306..-71.87204850788726
 5       1896   -71.9949   -72.39120978733506..-71.69550848895858
 7      22272   -71.9943   -72.10960180532878..-71.89062132124472
 8     630848   -71.9870   -72.14987995250573..-71.82421818050128
11      51168   -72.0200   -72.1542868597943..-71.89821535998382
13     675524   -71.9302   -72.11916541724729..-71.80485666459167
14     805888   -71.9639   -72.13666852830637..-71.74525202440606
27     182400   -72.0243   -72.146885853512..-71.88390255676234
33     243792   -72.0419   -72.14175210623095..-71.93235577572813
35    1511954   -72.0358   -72.1659217565381..-71.85441048212705
42     429896   -72.0273   -72.13122043088232..-71.90682433167194
43     824256   -71.9563   -72.025140692126..-71.76864723614274
44    1421056   -71.9550   -72.01800479119012..-71.82009228625247
45     362464   -72.0001   -72.1930323073174..-71.9040431802871
46     210160   -71.9767   -72.18184544186522..-71.8265823833162
48      95276   -72.0686   -72.2430429861937..-71.7952997743579
49     199754   -72.0665   -72.41892603786007..-71.8932854934029
53     144240   -71.9840   -72.110026315482..-71.90403920393189
57     886226   -71.9685   -72.11440226461279..-71.83690794779845
63     206976   -72.0234   -72.10868439105361..-71.8816565066452
```

First output of each study (seed 61000, 62000, 63000):

```text
seed 61000:
seed 61000 NP 8192 M 512 MT 16384 NVAR 12103680 pairs 1052672
stage 17 pass 262452 mean_log2 -12.99831
stage 18 pass 524680 mean_log2 -7.99892
stage 19 pass 137216 mean_log2 -9.93391
stage 20 pass 2097148 mean_log2 -7.00000
stage 21 pass 2102784 mean_log2 -1.99613
stage 22 pass 2037 mean_log2 -11.00777
tail variant passes 8394501 of 134217728  mean_log2 -3.99899 ; published-W8 passes 601 of 8192 mean_log2 -3.76878
RESULT seed 61000 est 2.2253219104812025e-22 log2est -71.92840 estpub 2.6103117008355515e-22 log2estpub -71.69820
STAGES -16.99438 -12.99831 -7.99892 -9.93391 -7.00000 -1.99613 -11.00777 tail -3.99899
seed 62000:
seed 62000 NP 8192 M 512 MT 16384 NVAR 9090990 pairs 1052672
stage 17 pass 262811 mean_log2 -12.99633
stage 18 pass 524372 mean_log2 -7.99977
stage 19 pass 134144 mean_log2 -9.96658
stage 20 pass 2097369 mean_log2 -6.99985
stage 21 pass 2089472 mean_log2 -2.00529
stage 22 pass 2018 mean_log2 -11.02129
tail variant passes 8416889 of 134217728  mean_log2 -3.99514 ; published-W8 passes 502 of 8192 mean_log2 -4.02846
RESULT seed 62000 est 2.1491784667889932e-22 log2est -71.97863 estpub 2.10012206171843e-22 log2estpub -72.01194
STAGES -16.99438 -12.99633 -7.99977 -9.96658 -6.99985 -2.00529 -11.02129 tail -3.99514
seed 63000:
seed 63000 NP 8192 M 512 MT 16384 NVAR 184944 pairs 1052672
stage 17 pass 261765 mean_log2 -13.00209
stage 18 pass 522911 mean_log2 -8.00379
stage 19 pass 126464 mean_log2 -10.05163
stage 20 pass 2095904 mean_log2 -7.00086
stage 21 pass 2094592 mean_log2 -2.00176
stage 22 pass 2116 mean_log2 -10.95288
tail variant passes 8342181 of 134217728  mean_log2 -4.00801 ; published-W8 passes 585 of 8192 mean_log2 -3.80771
RESULT seed 63000 est 2.0951079379452138e-22 log2est -72.01539 estpub 2.4071469255278942e-22 log2estpub -71.81509
STAGES -16.99438 -13.00209 -8.00379 -10.05163 -7.00086 -2.00176 -10.95288 tail -4.00801
```

### B.4 Premises

H2 is the premise above (Section 12). H1, H3-H9 are the base's, unchanged: the program's text and operation counts are the same, the examined variants, the good pairs and the row-16 passes are the same pairs in the same order; only the final event (rows 18..21 with four accepted patterns) is larger. H3: see the paragraph "This derivative" in Section 12. H7 (the success floor) is recomputed by the ledger (Appendix C): mu0 = 0.49739606, Pcap = 2^-9.23112,
success bound 0.3900000005. The cap V_MAX scales with N_FB, which is 4 times smaller; the Chebyshev bound with the unchanged slack 2^-10 (squared) is therefore 4 times larger, 2^-9.23112, and is paid for inside mu0 and N_FB by the ledger itself.

### B.5 What was not tested

- The count of four patterns is a solver enumeration for the published dense part; it was not proved by hand beyond the sign argument of B.2, and only Bitwuzla finished the 37-step instances (Z3 confirmed the smaller ones). The SMC does not rely on it: it applies the program's own exact difference checks to particles proposed with the eight bits free.
- The studies draw (W6, W7) uniformly from F6 x F7 at row 22, as the base's did (the premise of Section 7.6); W6, W7 and W8 variants do not enter rows 18 and 19.
- Other dense parts than the published one were not explored (for them the set of feasible patterns could differ; the variants of G keep rows 16..22 identical, Lemma 7.1).
- The organizer experiments verify constructed witnesses and the exactness of the filters; none estimates q3 or the rate of the four patterns.

### B.6 Credit

Jbenisek, with Claude (Anthropic, Claude Code): the derivative, the program change, the studies, the ledger and the text. The analysis that found the four patterns (the all-solutions enumeration, the exact stage enumeration, the three verified collisions and the check of the seven bits of rows 20..22) was done with Claude (Anthropic) running the verified 37-step model of GPT Luna (OpenAI) with Bitwuzla and Z3;
Grok (xAI) and GPT Luna were consulted for the ideas behind the unforced-condition test. 0xshikhar (fb039a6e): the attack program, the proof text, the studies G, K and K3 of the base and every number not listed above; through it Th0rgal (0db0eeb6, f2fe1d4d, dd6656d), companygardener (d3ec5c41, 44921815, 8de337d5), winglock (6c77089c, 7319bba), GordoAR (087a18c4), itseasypop (1c368173), qkniep (b947b377) and our own 8aeaed1c, def128fc and c22f86a2. None of them reviewed this derivative; mistakes are ours.

## Appendix C. The exact ledger: program and output

The ledger of Section 11 as a standalone Python program (integers, Fractions and 60-digit Decimals only), run on this filing's inputs. It reproduces the figures that `python3 experiments/xtab.py ledger` prints (the shipped ledger prints `time_log2 60.16722`, `T_num 3422921269986078257473`, `T_den 2644`, i.e. T = N / C with the N below; the table statistics enter as the four exact fractions that `table_stats(48)` of `xtab.py` computes from the histogram `HIST_Z`;
every constant is the one asserted by the counted program of Section 9 and Appendix D.1: `W6_OPS` 230, `BATCH_OVH` 8, `ZPLANE_OPS` 66, `FBFIX` 195, `ROWCOMP` 106, `ROWCHECK` 53, `OUTCMP` 16, `GROUP_FULL` 44, and so on).
Changed from ffbe30bb/fe65a7cb's Appendix C: q3 carries the factor EXQ = 24331/10000 (Appendix D.3); the cap-failure bound is Bernstein's with SLACK = 1/3680 (Appendix D.4); the rare path is c3b_l = 2 + 6 + 106 + 160 per l and c3b_t = 4 x 160 + 15 x 106 + 16 at probability REACH = 2^-12 (Appendix D.5), also in vmax_fb.

```python
from fractions import Fraction as Fr
from decimal import Decimal, getcontext
import math
# Exact ledger of the counted program (proof.md Sections 9-11, 12 premise H9 and Appendix D). Integers, Fractions and 60-digit Decimals only.
C = 2644                                     # reference cost of one target compression, in word operations
W6_OPS, BATCH_OVH, CHUNK256, ZPLANE_OPS, FBFIX = 230, 8, 31, 66, 195       # fibre test, per-batch overhead, chunk ops of a 256-lane plane, broadcast planes, fixed operations per first block
SCAN_LANE, SEG_OVH, GROUP_FULL, RECOMP, RARE_LOOKUP, ROWCOMP, ROWCHECK, OUTCMP = 5, 4, 44, 35, 2, 106, 53, 16
THETA, NVAR = 48, 12103680
P6, R16F = Fr(287309824, 1 << 32), Fr(1052672, 1 << 32)
# table statistics at THETA = 48: means over uniform x of kept fibres, kept variants, four-groups and segment operations (Tungsten histogram of Section 13.3, 3,200,000 values of x)
Fm, Vm, GRm, SOm = Fr(3722025299, 3200000), Fr(7671614937, 64000), Fr(95922334773, 3200000), Fr(4273094763257, 3200000)
SAFETY, PRE_OPS = Fr(1006, 1000), 1 << 58
Q3_LOG2 = -72.04                             # rows 16..36 follow every cell (four row-18/19 patterns): the studies of Appendix B.3
EXQ = Fr(24331, 10000)                       # exact collision event / cell event: preregistered 99% lower bound (Appendix D.3)
SLACK = Fr(1, 3680)                          # cap slack of the Bernstein bound (Appendix D.4)
REACH = Fr(1, 4096)                          # probability bound for reaching row 18 (and each later row) for one l (Appendix D.5)
g = P6 * Vm / SAFETY                         # yield: expected examined good pairs per first block (lower bound)
F, GR, SO = Fm * SAFETY, GRm * SAFETY, SOm * SAFETY      # costs: kept fibres, four-groups, segment operations (upper bounds)
batch_cost = W6_OPS + 1 + BATCH_OVH + CHUNK256
c3b_pair = 201 + RECOMP + 1 + RARE_LOOKUP; c3b_row = ROWCOMP + ROWCHECK + 1
c3b_l = 2 + 6 + ROWCOMP + c3b_row            # per l of the mask: y-words, row 16 computed (holds by the table), row 17 computed and checked
c3b_t = 4 * c3b_row + 15 * ROWCOMP + OUTCMP  # rows 18..21 checked, rows 22..36 computed, the output comparison
w6_part = (F / 256 + 1) * batch_cost
seg_part = P6 * F * (SCAN_LANE + SEG_OVH)
grp_part = P6 * SO
rare = 4 * P6 * GR * R16F * (c3b_pair + c3b_l + REACH * c3b_t)
vbar = w6_part + seg_part + grp_part + rare  # expected data-dependent operations per first block
fl = math.floor(Q3_LOG2); q3 = Fr(2) ** fl * Fr(math.floor(2 ** (Q3_LOG2 - fl) * 2 ** 40), 2 ** 40) * EXQ
vmax_fb = NVAR * (GROUP_FULL + SCAN_LANE + SEG_OVH + 2 + Fr(11, 10) * (c3b_pair + 32 * (c3b_l + c3b_t))) + 2 * (batch_cost + 2 * ZPLANE_OPS) + 200
getcontext().prec = 60
def mu_req(pcap):                            # smallest 8-decimal mu0 strictly above -ln(0.61 - Pcap - 2^-60) / (1 - 2^-10.4)
    x = Decimal('0.61') - Decimal(pcap.numerator) / Decimal(pcap.denominator) - Decimal(2) ** -60
    d = Decimal(1) - (Decimal(-10.4) * Decimal(2).ln()).exp()
    return Fr(int(math.floor(-x.ln() / d * 10 ** 8)) + 1, 10 ** 8)
def bern(nfb):                               # Bernstein: Pr[sum v_f > (1 + s) N_FB vbar] <= exp(-s^2 N_FB vbar / (2 vmax_fb (1 + s/3))), rounded up
    e = SLACK * SLACK * nfb * vbar / (2 * vmax_fb * (1 + SLACK / 3))
    return Fr((Decimal(-e.numerator) / Decimal(e.denominator)).exp()) * Fr(10 ** 30 + 1, 10 ** 30)
pcap = Fr(1, 1 << 24)
for _ in range(6):                           # fixed point of N_FB and the cap-failure bound
    MU0 = mu_req(pcap); NFB = int(-(-MU0 // (g * 32 * q3)))
    pcap = bern(NFB)
assert MU0 >= mu_req(pcap)
VMAX = math.ceil((1 + SLACK) * NFB * vbar)
A_C, A_S, DEV, FIN = 1 << 60, 1 << 50, 1 << 40, 1600
ROWS = [("A_C: characteristic and SFS-pair search (units x C)", A_C * C), ("A_S: Step-1 solve (units x C)", A_S * C), ("DEV: development (units x C)", DEV * C),
        ("N_FB first-block compressions (units x C)", NFB * C), ("fixed operations: N_FB x 195", NFB * FBFIX), ("V_MAX: data-dependent operations", VMAX),
        ("overshoot past the cap: vmax_fb", math.ceil(vmax_fb)), ("PRE: preprocessing", PRE_OPS), ("FIN: final verification", FIN), ("6 further compressions (units x C)", 6 * C)]
N = sum(int(v) for _, v in ROWS)
P = 100000
a = (N ** P // C ** P).bit_length() - 1
while (1 << (a + 1)) * C ** P <= N ** P: a += 1
while (1 << a) * C ** P > N ** P: a -= 1
claim = Fr(-(-(a + 1) * 10 ** 5 // P), 10 ** 5)
w = max(len(k) for k, _ in ROWS)
for k, v in ROWS: print(k.ljust(w), format(int(v), ","))
print("q3 = 2^%s x %s = 2^%.5f, g = %.4f examined good pairs per first block, vbar = %.2f (rows >= 16: %.2f), mu0 = %s, N_FB = %d, Pcap = 2^%.5f, success bound %.10f"
      % (Q3_LOG2, EXQ, math.log2(q3), float(g), float(vbar), float(rare), float(MU0), NFB, math.log2(float(pcap)), 1 - math.exp(-(1 - 2.0 ** -10.4) * float(MU0)) - float(pcap) - 2.0 ** -60))
assert 1 - math.exp(-(1 - 2.0 ** -10.4) * float(MU0)) - float(pcap) - 2.0 ** -60 > 0.39
print("N = %d" % N)
print("certificate: 2^%d * %d^%d <= N^%d < 2^%d * %d^%d" % (a, C, P, P, a + 1, C, P))
print("time_log2 = %.5f" % float(claim))
```

Output:

```text
A_C: characteristic and SFS-pair search (units x C) 3,048,324,458,180,503,404,544
A_S: Step-1 solve (units x C)                       2,976,879,353,691,897,856
DEV: development (units x C)                        2,907,108,743,839,744
N_FB first-block compressions (units x C)           10,232,179,474,817,024,040
fixed operations: N_FB x 195                        754,642,586,077,654,950
V_MAX: data-dependent operations                    360,341,971,828,600,115,535
overshoot past the cap: vmax_fb                     1,077,492,591,596
PRE: preprocessing                                  288,230,376,151,711,744
FIN: final verification                             1,600
6 further compressions (units x C)                  15,864
q3 = 2^-72.04 x 24331/10000 = 2^-70.75720, g = 7970.7549 examined good pairs per first block, vbar = 93087.24 (rows >= 16: 1015.62), mu0 = 0.49466958, N_FB = 3869961979885410, Pcap = 2^-17.80706, success bound 0.3900000041
N = 3422921269986078257473
certificate: 2^6016721 * 2644^100000 <= N^100000 < 2^6016722 * 2644^100000
time_log2 = 60.16722
```

## Appendix D. This filing: the collision event after row 21, the Bernstein cap bound, the rare path as executed

### D.1 The change in the program

`step3b` of `experiments/xtab.py` (the routine that runs rows 16..36 for every l of a looked-up mask) now reads, for each l:

```python
        ok = True
        for t in range(16, R):
            for (_, _, Ww) in (X, Y): Ww[t] = (s1(Ww[t-2]) + Ww[t-7] + s0(Ww[t-15]) + Ww[t-16]) & M32
            step_rows(X, Y, t); mc.n += ROWCOMP
            if t == 16 or t >= EXR: continue  # row 16: implied by the mask; rows 22..36: no cell test
            mc.n += ROWCHECK + 1
            if not (row_ok(X, Y, t) and x2_ok(X, t)): ok = False; break
        if ok:
            mc.n += OUTCMP  # the event: equal outputs (8 xor, 7 or, 1 branch)
            if same_out(X, Y): return l, Wx[:16], Wy[:16]
    return None
def same_out(X, Y): return all(X[k][t] == Y[k][t] for k in (0, 1) for t in range(R - 4, R))
```

with `ROWCHECK, ROWCOMP, OUTCMP, EXR = 53, 106, 16, 22`. Both members share the chaining value, so their 37-step outputs cv + (A36, A35, A34, A33, E36, E35, E34, E33) are equal iff the eight registers are equal: `same_out` is the collision test itself (the final verification with the target then runs as before).
Rows 16..21 are checked exactly as in ffbe30bb (every cell, the `+` equalities, every printed two-bit condition closing at the row, the exact signed differences of both members; rows 18 and 19 with the four value patterns). Row 16 is computed and not checked: the l-mask of the lane is read from the table of all (u, l) whose row 16 holds (Section 6.2; `make_R16` evaluates the same `row_ok(X, Y, 16)` and `x2_ok(X, 16)`), so the check could never fail and dropping it removes no pair.
Every pair the old program accepted is accepted (equal outputs follow from the cells of rows 22..36; the cell event was never larger than the collision event in any of the 5 x 2^30 late proposals of D.3, and it is contained in it by construction because the characteristic ends with zero differences), and every pair accepted is a collision of the second block.
The counted operations per l: 8 (y-words and loop) + 106 (row 16) + 160 (row 17) + 160 per reached row 18..21 + 15 x 106 (rows 22..36) + 16 (comparison) when row 21 passes; the ledger's charge is in D.5.
The organizer experiment `a0-sfs-r37` (`sfs_trial`) builds rows 16..21 as before and then proposes W22 uniformly from the set of D.2 (`draw_s22`, a proposal law only: no cell or two-bit condition of rows 22..36 is imposed), W7 from F7, W6 = W22 - s1(W20) - W15 - s0(W7) required in F6, computes rows 22..36 and accepts iff `same_out`; the returned pair must also pass every cell of rows -4..21, the Step-2 equations and the 37-step compression; the observation `cells_22_36` says whether it also follows the printed cells of rows 22..36.

### D.2 The structure of the event (exact counts)

Fix a prefix whose rows 16..21 follow the cells. The schedule forces dW22 = W22' - W22 = 2^24 + 2^23 - 2^15 = 0x017f8000 (dW20 = 0, dW15 + dW6 = 0, s0(W7') - s0(W7) = T7 on F7). The two outputs are equal iff
(i) E22[29] = 1, (ii) s1(W22') - s1(W22) = 0x4fff9f30 (so that dW24 = +2^29), (iii) s1(W24 + 2^29) - s1(W24) = 0xfff80c00 (dW26 = 0), with the rows in between following from these (the reverse direction is computed: 0 exceptions in 2^31 and 2^34 proposals; the forward direction is proved by inverting the step map for fixed W: dW25, dW29, dW30, dW31 are 0 as constants of the expansion, dW27, dW28, dW32..dW36 are 0 when dW25 = dW26 = 0, and equal states after step 24 with zero later word differences stay equal to step 36).
- **W22.** |{w : s1(w + 0x017f8000) - s1(w) = 0x4fff9f30}| = **9,830,400 = 75 x 2^17**, counted over all 2^32 words (numpy, this filing) and independently enumerated in `xtab.py` (`s22set`) as 10 disjoint affine pieces: for each signed-digit form of 0x017f8000 (145 forms; w + d = w ^ dl iff the bits of w under dl are fixed by the signs) and each signed-digit form of 0x4fff9f30 supported on s1(dl) (linear conditions on s1(w)), the solutions form an affine space;
  the pieces have sizes 2 x 2^22, 2 x 2^19, 2 x 2^17 and 4 x 2^15, total 9,830,400. The printed cells and two-bit conditions of W22 allow 2^22 words (the piece with dl = 0x01808000). Ratio 75/32.
- **W24.** 285,212,672 = 17 x 2^24 words satisfy (iii) against 2^28 for the printed cells and conditions (17/16); given equality after step 24, dW26 = 0 has probability 17/256 against 16/256 for the four step-24 conditions.
- **Uniform model.** q_event = 1275/2^24 = 2^-13.684 against q_cell = 2^-15 after row 21, ratio 1275/512 = 2.4902. Under the attack's law W24 = s1(W22) + W17 + s0(W9) + W8 is correlated with W22, so the ratio is measured (D.3): 2.4648 +- 0.0145 on Table 15 states and 2.4552 on ffbe30bb's.
The program does not use this description: it tests equal outputs. The description explains why the ratio is about 2.45 and gives the organizer experiment a proposal law that reaches collisions outside the printed cells.

### D.3 The ratio R: three runs, the preregistered rule and the charged bound

**Program.** `smc_pair0.c`: the base estimator `smc.c` of Appendix A.7 (sha256 685297129cda47b247e6d19b1799d73b198e1511334e161fa7583ef6c1175a65) with ffbe30bb's removal of the eight value bits of rows 18 and 19 (compile flag `FFBE_RELAX`; the same eight mask bits as Appendix B.1) and with the final proposal loop scoring every late proposal (W6, W7 uniform on F6 x F7, W8 from the variant list, W22..W36 recomputed from the schedule) twice: **C**, rows 22..36 follow every cell, `+` equality, two-bit condition and exact difference (smc.c's own stage 22 and tail), and **E**, rows 22..36 replayed with no cells and all eight registers equal after step 36.
sha256 of `smc_pair0.c` 4cd63da8f3afc7812c4d92495dd4b3bab14021fdc109c1518e2cb13dcad624ec, `lab.h` bdefd6747d41727a378bc124c241db1f635275d3a2901b96a1c6c6b0e5c5e456 (the base's, unchanged), binary 12b3296d463b94f68ec90756ec35e9098ae3b938d4b8e1264e721908f2287b01 (`cc -O2 -DFFBE_RELAX`). Our own code; the difference to Appendix A.7's `smc.c` (ignoring line endings; the function `exact_coll21` and `MODE` other than 0 are not used by any run below):

```diff
--- smc_A7.c	2026-10-12 00:56:12.656399600 -0600
+++ smc_pair0.c	2026-10-12 00:18:30.494737500 -0600
@@ -82,6 +82,17 @@
 }
 static void init_all(void){
   init_cells();
+#ifdef FFBE_RELAX
+  /* ffbe30bb's only characteristic change: remove the eight E18/E19 value
+     masks; retain every signed-difference and X2 test.  The bit positions are
+     the published LSB indices, matching the ffbe proof and its four-pattern
+     SMC.  This is a compile-time research variant; the ordinary control build
+     is unchanged. */
+  { const u32 e18 = (1u<<1)|(1u<<5)|(1u<<10)|(1u<<11)|(1u<<18)|(1u<<28)|(1u<<29);
+    const u32 e19 = (1u<<29);
+    CELL[1][18].m &= ~e18; CELL[1][18].v &= ~e18;
+    CELL[1][19].m &= ~e19; CELL[1][19].v &= ~e19; }
+#endif
   const char*all[]={0};(void)all;
   for(unsigned i=0;i<sizeof CHA/sizeof*CHA;i++)if(strlen(CHA[i].s)!=32)exit(90);
   for(unsigned i=0;i<sizeof CHE/sizeof*CHE;i++)if(strlen(CHE[i].s)!=32)exit(91);
@@ -111,38 +122,86 @@
     if(BIT(w,1)==BIT(w,12)||BIT(w,8)==BIT(w,25)||BIT(w,14)!=BIT(w,18))v2++;}
   printf("variants %ld; T8 violations %ld; W8 cell/2-bit violations %ld\n",NVAR,v1,v2); bad+=v1+v2;
   printf("selftest %s\n",bad?"FAILED":"ok"); return bad!=0;}
+static u32 samp7m(Rng*r,int mode){ if(!mode)return samp7(r); for(;;){u32 w=samp7(r); int br=((w>>11)&1); if(mode==1&&!br)return w; if(mode==2&&br)return w; if(mode==3&&(w&1))return w; if(mode==4&&!(w&1))return w;} }
+static int MODE=0;
+/* exact end event: rows 22..36 replayed on raw schedule words, no cells; collision <=> all 8 registers equal after step 36 (same cv, feed-forward cancels) */
+static int exact_coll(P*q,u32 w6,u32 w7,u32 w8){
+  u32 Wx[NR],Wy[NR]; for(int t=0;t<22;t++){Wx[t]=q->Wx[t];Wy[t]=q->Wy[t];}
+  Wx[6]=w6;Wy[6]=w6+D6;Wx[7]=w7;Wy[7]=w7+D7;Wx[8]=w8;Wy[8]=w8+D8;
+  for(int t=22;t<NR;t++){Wx[t]=s1(Wx[t-2])+Wx[t-7]+s0(Wx[t-15])+Wx[t-16];Wy[t]=s1(Wy[t-2])+Wy[t-7]+s0(Wy[t-15])+Wy[t-16];}
+  u32 ax[NR+O],ex[NR+O],ay[NR+O],ey[NR+O];
+  for(int i=-4;i<=21;i++){ax[i+O]=AX(q,i);ex[i+O]=EX(q,i);ay[i+O]=AY(q,i);ey[i+O]=EY(q,i);}
+  for(int t=22;t<NR;t++){
+    u32 e=ax[t-4+O]+ex[t-4+O]+S1(ex[t-1+O])+CH(ex[t-1+O],ex[t-2+O],ex[t-3+O])+KC[t]+Wx[t];
+    ex[t+O]=e;ax[t+O]=e-ax[t-4+O]+S0(ax[t-1+O])+MAJ(ax[t-1+O],ax[t-2+O],ax[t-3+O]);
+    e=ay[t-4+O]+ey[t-4+O]+S1(ey[t-1+O])+CH(ey[t-1+O],ey[t-2+O],ey[t-3+O])+KC[t]+Wy[t];
+    ey[t+O]=e;ay[t+O]=e-ay[t-4+O]+S0(ay[t-1+O])+MAJ(ay[t-1+O],ay[t-2+O],ay[t-3+O]);}
+  for(int t=33;t<NR;t++) if(ax[t+O]!=ay[t+O]||ex[t+O]!=ey[t+O]) return 0;
+  return 1;}
+
+/* row-21 exact: E21 arbitrary (no cell, no exact-diff filter on row 21); W21x derived from E21, W21y from the real schedule difference */
+static int exact_coll21(P*q,u32 e21,u32 w6,u32 w7,u32 w8){
+  u32 Wx[NR],Wy[NR]; for(int t=0;t<21;t++){Wx[t]=q->Wx[t];Wy[t]=q->Wy[t];}
+  u32 ax[NR+O],ex[NR+O],ay[NR+O],ey[NR+O];
+  for(int i=-4;i<=20;i++){ax[i+O]=AX(q,i);ex[i+O]=EX(q,i);ay[i+O]=AY(q,i);ey[i+O]=EY(q,i);}
+  u32 rest=ax[17+O]+ex[17+O]+S1(ex[20+O])+CH(ex[20+O],ex[19+O],ex[18+O])+KC[21];
+  Wx[21]=e21-rest; Wy[21]=Wx[21]+(s1(Wy[19])-s1(Wx[19]))+(Wy[14]-Wx[14])+(s0(w6+D6)-s0(w6));
+  Wx[6]=w6;Wy[6]=w6+D6;Wx[7]=w7;Wy[7]=w7+D7;Wx[8]=w8;Wy[8]=w8+D8;
+  for(int t=22;t<NR;t++){Wx[t]=s1(Wx[t-2])+Wx[t-7]+s0(Wx[t-15])+Wx[t-16];Wy[t]=s1(Wy[t-2])+Wy[t-7]+s0(Wy[t-15])+Wy[t-16];}
+  for(int t=21;t<NR;t++){
+    u32 e=ax[t-4+O]+ex[t-4+O]+S1(ex[t-1+O])+CH(ex[t-1+O],ex[t-2+O],ex[t-3+O])+KC[t]+Wx[t];
+    ex[t+O]=e;ax[t+O]=e-ax[t-4+O]+S0(ax[t-1+O])+MAJ(ax[t-1+O],ax[t-2+O],ax[t-3+O]);
+    e=ay[t-4+O]+ey[t-4+O]+S1(ey[t-1+O])+CH(ey[t-1+O],ey[t-2+O],ey[t-3+O])+KC[t]+Wy[t];
+    ey[t+O]=e;ay[t+O]=e-ay[t-4+O]+S0(ay[t-1+O])+MAJ(ay[t-1+O],ay[t-2+O],ay[t-3+O]);}
+  for(int t=33;t<NR;t++) if(ax[t+O]!=ay[t+O]||ex[t+O]!=ey[t+O]) return 0;
+  return 1;}
 int main(int argc,char**argv){
-  if(argc>=3&&!strcmp(argv[1],"-t"))return selftest(argv[2]);
-  if(argc<6){fprintf(stderr,"usage\n");return 2;}
+  if(argc<7){fprintf(stderr,"usage: smc_exact seed NP M MT2 classes.txt mode(0=w6w7 F6xF7)\n");return 2;}
   u64 seed=strtoull(argv[1],0,10); int NP=atoi(argv[2]),M=atoi(argv[3]),MT=atoi(argv[4]);
-  init_all(); if(load_variants(argv[5])){fprintf(stderr,"variants\n");return 3;}
+  MODE=atoi(argv[6]); init_all(); if(load_variants(argv[5])){fprintf(stderr,"variants\n");return 3;}
   build_r16(); Rng R;rseed(&R,seed);
   P *pop=malloc((size_t)NP*sizeof(P)),*pop2=malloc((size_t)NP*sizeof(P)); Rec*rec=malloc((size_t)NP*M*sizeof(Rec));
-  double lg[40];int nst=0; double st16=(double)NPAIR/32.0/4294967296.0; lg[nst++]=log2(st16);
-  printf("seed %llu NP %d M %d MT %d NVAR %ld pairs %ld\n",(unsigned long long)seed,NP,M,MT,NVAR,NPAIR);
+  double est=(double)NPAIR/32.0/4294967296.0;
+  printf("seed %llu NP %d M %d MT2 %d\n",(unsigned long long)seed,NP,M,MT);
   for(int i=0;i<NP;i++){long k=rbelow(&R,NPAIR);pop[i]=P0[pairL[k]];
     if(!(rowx(&pop[i],16,0,pairE[k])&&rowy(&pop[i],16,0))){fprintf(stderr,"init fail\n");return 4;}}
-  double est=st16; int dead=0;
-  for(int t=17;t<=22&&!dead;t++){
-    u32 fm=CELL[1][t].m,fv=CELL[1][t].v; double w=(t<=21)?ldexp(1.0,-__builtin_popcount(fm)):1.0; long cnt=0;
+  int TEND=(MODE>=10)?20:21;
+  for(int t=17;t<=TEND;t++){
+    u32 fm=CELL[1][t].m,fv=CELL[1][t].v; double w=ldexp(1.0,-__builtin_popcount(fm)); long cnt=0;
     for(int i=0;i<NP;i++){P s=pop[i];
-      for(int c=0;c<M;c++){ u32 a,b=0; if(t<=21)a=(r32(&R)&~fm)|fv; else{a=samp6(&R);b=samp7(&R);}
-        if(apply_stage(&s,t,a,b)){rec[cnt].pi=i;rec[cnt].a=a;rec[cnt].b=b;cnt++;} } }
-    double mean=w*(double)cnt/((double)NP*M); lg[nst++]=cnt?log2(mean):-1e9; est*=mean;
-    printf("stage %d pass %ld mean_log2 %.5f\n",t,cnt,cnt?log2(mean):-1e9);
-    if(!cnt){dead=1;break;}
+      for(int c=0;c<M;c++){ u32 a=(r32(&R)&~fm)|fv;
+        if(apply_stage(&s,t,a,0)){rec[cnt].pi=i;rec[cnt].a=a;rec[cnt].b=0;cnt++;} } }
+    est*=w*(double)cnt/((double)NP*M);
+    if(!cnt){printf("dead\n");return 0;}
     for(int i=0;i<NP;i++){long k=rbelow(&R,cnt);pop2[i]=pop[rec[k].pi];
-      if(!apply_stage(&pop2[i],t,rec[k].a,rec[k].b)){fprintf(stderr,"resample fail\n");return 5;}}
+      if(!apply_stage(&pop2[i],t,rec[k].a,0)){fprintf(stderr,"resample fail\n");return 5;}}
     P*tmp=pop;pop=pop2;pop2=tmp; }
-  if(dead){printf("RESULT seed %llu est 0 log2est -inf\n",(unsigned long long)seed);return 0;}
-  /* tail rows 23..36: variant W8 (MT proposals per particle) and published W8 (same particle) */
-  long tp=0,tpub=0,both=0; 
+  /* joint 22+tail: proposals (W6,W7,W8); control = cell event (stage-22 cells + tail cells), test = exact collision */
+  if(MODE>=10){ MODE-=10; long n=0,cell=0,ex=0,x=0;
+    for(int i=0;i<NP;i++){ P s=pop[i];
+      for(int j=0;j<MT;j++){ u32 e21=r32(&R),w6=samp6(&R),w7=samp7m(&R,MODE),w8=VAR[rbelow(&R,NVAR)];
+        int e=exact_coll21(&s,e21,w6,w7,w8);
+        s.Wx[8]=w8;s.Wy[8]=w8+D8; int c=0;
+        if(apply_stage(&s,21,e21,0)&&apply_stage(&s,22,w6,w7)) c=tail_eval(&s);
+        n++;cell+=c;ex+=e;x+=(c&&!e);} }
+    printf("n %ld cellevent %ld exact %ld cell_not_exact %ld\n",n,cell,ex,x);
+    printf("RESULT21 seed %llu log2est20 %.5f log2cell %.5f log2exact %.5f ratio %.4f\n",(unsigned long long)seed,log2(est),log2((double)cell/n),log2((double)ex/n),(double)ex/cell);
+    return 0; }
+  /* tag every proposal by its particle's relaxed bits: E18x[1,5,10,11,18,28,29], E19x[29] (8-bit key k) */
+  static long bn[256],bc[256],be[256],bb[256],bx[256],bpart[256];
+  long n=0,cell=0,ex=0,both=0,cell_notex=0,s22=0;
   for(int i=0;i<NP;i++){ P s=pop[i];
-    for(int j=0;j<MT;j++){ u32 w8=VAR[rbelow(&R,NVAR)]; s.Wx[8]=w8;s.Wy[8]=w8+D8; tp+=tail_eval(&s); }
-    s.Wx[8]=MX[8];s.Wy[8]=MY[8]; int ok=tail_eval(&s); tpub+=ok; }
-  double tm=(double)tp/((double)NP*MT), tmp_=(double)tpub/NP;
-  printf("tail variant passes %ld of %ld  mean_log2 %.5f ; published-W8 passes %ld of %d mean_log2 %.5f\n",tp,(long)NP*MT,tp?log2(tm):-1e9,tpub,NP,tpub?log2(tmp_):-1e9);
-  double estv=est*tm, estp=est*tmp_;
-  printf("RESULT seed %llu est %.17g log2est %.5f estpub %.17g log2estpub %.5f\n",(unsigned long long)seed,estv,estv>0?log2(estv):-1e9,estp,estp>0?log2(estp):-1e9);
-  printf("STAGES"); for(int i=0;i<nst;i++)printf(" %.5f",lg[i]); printf(" tail %.5f\n",tp?log2(tm):-1e9);
+    u32 e18=EX(&s,18),e19=EX(&s,19);
+    int k=(int)(BIT(e18,1)|BIT(e18,5)<<1|BIT(e18,10)<<2|BIT(e18,11)<<3|BIT(e18,18)<<4|BIT(e18,28)<<5|BIT(e18,29)<<6|BIT(e19,29)<<7);
+    bpart[k]++;
+    for(int j=0;j<MT;j++){ u32 w6=samp6(&R),w7=samp7m(&R,MODE),w8=VAR[rbelow(&R,NVAR)];
+      int e=exact_coll(&s,w6,w7,w8);
+      s.Wx[8]=w8;s.Wy[8]=w8+D8;
+      int c=0; if(apply_stage(&s,22,w6,w7)){ s22++; c=tail_eval(&s); }
+      n++;cell+=c;ex+=e;both+=(c&&e);cell_notex+=(c&&!e);
+      bn[k]++;bc[k]+=c;be[k]+=e;bb[k]+=(c&&e);bx[k]+=(c&&!e);} }
+  printf("n %ld stage22cells %ld cellevent %ld exact %ld both %ld cell_not_exact %ld\n",n,s22,cell,ex,both,cell_notex);
+  printf("RESULT seed %llu log2est21 %.5f log2cell %.5f log2exact %.5f ratio %.4f\n",(unsigned long long)seed,log2(est),log2((double)cell/n),log2((double)ex/n),(double)ex/cell);
+  printf("EST21 %.17g\n",est);
+  for(int k=0;k<256;k++) if(bn[k]) printf("BIN %d particles %ld n %ld cell %ld exact %ld both %ld cell_not_exact %ld\n",k,bpart[k],bn[k],bc[k],be[k],bb[k],bx[k]);
   return 0;}
```

**Runs.** NP 8192, M 512, MT 8192 (2^26 late proposals per seed), the variant list of all 12,103,680 variants of G (`allg_classes.txt`, sha256 05d967567f56d5c61359e21156397da2cf5b995f477f91254d2b643facc77319), MODE 0.
- Run 1 (2026-10-12, an interaction test with a written plan; its plan file is not timestamped before the run, so it is not claimed as preregistered): seeds 9101..9116, 2^30 late proposals: E 80,487, C 32,745, ratio 2.45799, cell-and-not-collision 0; the four row-18/19 pattern bins 2.4779 / 2.4789 / 2.4551 / 2.4184 (chi-square 5.39, 3 df).
- Run 2 (same day, interaction test with a written plan): row-21 states of seeds 9201..9204 (8,192 particles each) dumped by the same program, late proposals scored by a second program of ours (`pair1.c`, sha256 849a11b7e167070f9ec9ab5466d0be0a90db0ab3dc5cbfa4fa99c5fd135785ec) that replays rows 22..36 the same way and also evaluates conditions (i)-(iii) of D.2 (0 mismatches against the replay): halves seed 9411 (states 9201, 9202) and seed 9413 (states 9203, 9204), 2^30 proposals each: E 79,605 / 80,658, C 32,602 / 33,036, pooled E 160,263, C 65,638, ratio 2.44162, cell-and-not-collision 0.
- Run 3 (**preregistered**; the file below, sha256 50541e67ffb13a27ca94aa581e82e05f3b2d117d761b812f63e12665eb79d206, written before any of its seeds ran): seeds 9501..9532, 2^31 late proposals: E 161,930, C 65,628, ratio 2.46739, cell-and-not-collision 0 in every seed; per-seed dispersion chi-square 55.36 on 31 df (p 0.005).

```text
preregistration: confirmation run of the exact-event multiplier for the A0-variant attack on 37-step SHA-256 (rows 18/19 accepting the four value patterns)
written before any listed seed was run. stamp: 2026-10-12T06:46:30Z
quantity: R = Pr[two 37-step outputs equal | rows <= 21 follow every cell and two-bit condition] / Pr[rows 22..36 follow every cell and two-bit condition | same], estimated by E/C,
 E = number of late proposals whose rows 22..36 replay ends with equal outputs (all eight registers), C = number whose rows 22..36 follow every cell; cell_not_exact = number with C-event and not E-event.
program: smc_pair0.c (sha256 4cd63da8f3afc7812c4d92495dd4b3bab14021fdc109c1518e2cb13dcad624ec) built with -DFFBE_RELAX as p0_ffbe (sha256 12b3296d463b94f68ec90756ec35e9098ae3b938d4b8e1264e721908f2287b01), unchanged from the earlier runs;
 rows 22..36 are replayed on schedule words recomputed from W6, W7, W8 for every proposal (no expanded word held fixed).
parameters: NP 8192, M 512, MT 8192 (2^26 late proposals per seed), variant list allg_classes.txt (all 12,103,680 variants of G), MODE 0.
seeds: 9501..9532 (32 seeds, 2^31 late proposals). Every listed seed is run and reported; none is dropped, replaced or rerun.
earlier runs pooled with this one (their counts are fixed): run 1 seeds 9101..9116: E 80,487 C 32,745; run 2 (two halves, seeds 9411, 9413 on SMC states of seeds 9201..9204): E 160,263 C 65,638.
declared value (fixed now): with E_all, C_all the pooled counts of the three runs, u = the one-sided 99 percent Clopper-Pearson upper bound of C_all/E_all
 (C | E binomial: every cell-event proposal is an exact-event proposal), L = 1/u, and the filed multiplier is EXQ = min(24331/10000, floor(10^4 L)/10^4).
 24331/10000 is the same bound computed on the two earlier runs alone, so this run can only lower the filed value.
 if cell_not_exact > 0 in any seed, the bound is instead L = L_E/U_C (simultaneous one-sided 99.5 percent Clopper-Pearson bounds on the two rates) and it is reported as such.
diagnostic (no decision): per-seed dispersion chi-square of C given E against the pooled ratio (df 31).
```

**Rule applied.** Pooled over the three runs: E_all = 402,680, C_all = 164,011 (ratio 2.45520). Every cell event was a collision event (`both` = C in every seed of every run), so C_all given E_all is binomial and the one-sided 99 percent Clopper-Pearson upper bound of C_all/E_all is u = 0.40910197, L = 1/u = 2.444378, floor(10^4 L)/10^4 = 2.4443.
The rule's value is **EXQ = min(2.4331, 2.4443) = 2.4331**, the value charged (2.4331 is the same bound on runs 1 and 2 alone: Pr[Bin(240,750, 10000/24331) <= 98,383] = 0.00969 < 0.01). Checks of the charge against the other ways of reading the data: run 3 alone, 99 percent Clopper-Pearson 2.4502; with run 3's measured overdispersion (factor 1.786) 2.4445 for run 3 alone and 2.4408 for all runs; a cluster ratio-estimator bound over the 48 seeds of runs 1 and 3 (one-sided 99 percent, t with 47 df) 2.4464. All are above 2.4331.
Pr[Bin(402,680, 10000/24331) <= 164,011] = 9.1 x 10^-7.

Per-seed counts (seed E C). Run 1:

```text
9101 5104 2040      9102 4972 2046      9103 5073 2074      9104 5009 2084
9105 4971 1975      9106 5014 2054      9107 5096 2113      9108 4942 2074
9109 4992 2048      9110 5002 2026      9111 5107 2066      9112 5201 2108
9113 4975 1961      9114 4939 2001      9115 5138 2077      9116 4952 1998
```

Run 3:

```text
9501 5044 2076      9502 5276 2096      9503 4934 2004      9504 5065 2008
9505 5145 2093      9506 5090 2085      9507 5050 2020      9508 5108 2037
9509 4975 2034      9510 5029 2123      9511 5086 1983      9512 5087 2058
9513 5033 2058      9514 4953 2069      9515 5118 2072      9516 5002 2037
9517 5059 2158      9518 5099 1988      9519 4970 1959      9520 5026 2017
9521 5051 2070      9522 5045 2092      9523 4977 2084      9524 4930 1991
9525 5104 2009      9526 5132 2031      9527 5014 2084      9528 4976 2038
9529 5161 2044      9530 5182 2058      9531 5156 2078      9532 5053 2074
```

### D.3b The ratio R under the attack's own law of (W7, W8): a preregistered run (this filing)

**Why.** Runs 1-3 draw W7 uniform on F7 and W8x from the whole variant list, independently. The online attack examines only the variants of kept fibres (Section 8.1), so its late words (W7x, W8x) = (c7(a0) - x, W8C - E4(a0)) follow the kept-fibre law, jointly and through x. W6 stays uniform on F6 given everything else (cb uniform, Lemma 5.1). This run measures R under that law.

**Programs (ours).** `genk.c` writes the pool: for 16,384 uniform values of x (two processes, seeds 11 and 12, 8,192 each), every class of the whole family G (12,103,680 variants, 22,976 classes, regenerated from the definition of G) whose W7x is in F7 passes, the variants of all passing classes are merged into fibres by phi(a0, x), fibres of at least 48 variants are kept, and each kept variant is written with probability 2^-10 as (W7x, W8x); fixed-probability thinning keeps the pool uniform over all examined (x, variant) pairs. Pool: 1,835,460 pairs (919,629 + 915,831); per-x means 356.0 passing classes (exact 364.6), 185,399 variants in passing classes (exact 192,075), 1,115.9 kept fibres and 114,715 kept variants (Tungsten, 3,200,000 x: 1,163.1 and 119,869; the per-x counts are heavy-tailed, so 16,384 values of x sample the law, not enumerate it).
`q3k.c` is our own SMC estimator of R (row 16 exact from the enumeration of the row-16 pairs, rows 17..21 by proposals with each row's fixed x-bits imposed, uniform resampling to NP after each stage; the late proposals recompute W22..W36 of both members from the schedule and score C and E exactly as `smc_pair0.c` does in D.3) with the late draw `w6 = drawF6(); pi = below(nv); w7 = pool[2 pi]; w8 = pool[2 pi + 1]` (W7 and W8 jointly from the pool; every pooled W7 is checked to lie in F7 at start). Hashes, recorded before the run:

```text
0654b92fa08b7c32ded8051e5b5589615826b422abd53144c52e689c408b482e  q3k.c
378ad63cc59e629c5449e33ebebca8e7ba871bcb8219865e9c864410bfb14f91  q3k
238ae2238d18a7503772e22df72bd2c081905f42e40cf4da9aa6d81ea37b3c5f  genk.c
f01e0c355afbb0aff8df6a06b2367cdd43644d3ad10af6c7470f2a44e535d47e  q3consts_relaxed.h
3e151c716a1b1c5688587227b8570495f80240729c9651f12a9c85a38b914308  pool.bin
f5c706b0bfe21eb569bf8837cc6c807b62196c10a5c17d9a6fef411d5505c809  analyze.py
3ccc6e94f3920c8cde00bf3aff954317e2f7b2423b803a98c6ab6f0a7f8ade4c  PREREG_kept.txt
```

**Preregistration** (written before any main seed ran; its stamp and hash above):

```text
preregistration: the exact-event multiplier R under the attack's own examined law of the late words (kept fibres, THETA = 48), for the A0-variant attack on 37-step SHA-256 with the four value patterns of rows 18 and 19 accepted
written before any main seed was run; stamp: 2026-10-12T07:54:17Z
why: the filed R (2.4331) was measured with W7 uniform on F7 and W8x uniform on the variant list, independently; the online attack examines the variants of kept fibres only,
 so (W7x, W8x) = (c7(a0) - x, W8C - E4(a0)) follow the kept-fibre law, jointly and x-dependently. This study measures R under that law. W6 stays uniform on F6 (cb uniform, Lemma 5.1).
quantity: R = Pr[two 37-step outputs equal | rows 16..21 follow every cell and two-bit condition] / Pr[rows 22..36 follow every cell and two-bit condition | same].
program: q3k.c = our q3x.c with one change (the late proposal draws (W7x, W8x) jointly from the pool); built gcc -O2 -DCONSTS='"q3consts_relaxed.h"' q3k.c -lm -o q3k.
pool: genk.c (ours): x uniform (xoshiro256++, seeds 11 and 12, 8192 values each, 16,384 in all); for each x every class of the whole family G (12,103,680 variants, 22,976 classes)
 whose W7x is in F7 passes, variants of passing classes are merged into fibres by phi(a0, x), fibres of at least 48 variants are kept, and each kept variant is written with
 probability 2^-10 as (W7x, W8x). Fixed-probability thinning makes the pool uniform over all examined (x, variant) pairs. pool.bin = pool_a.bin || pool_b.bin.
 (smoke check, disclosed: 1024 x of seed 2 gave per-x means 349.6 passing classes, 184,328 variants, 115,259 kept variants against the filed 364.6, 192,075 and 119,869.)
smoke (disclosed, not used): q3k seed 1, MT 512, on a 1024-x smoke pool: E 296 C 117.
parameters: NP 8192, M 512, MT 8192 (2^26 late proposals per seed).
main seeds: 920001..920064 (64 seeds, 2^32 late proposals), three processes (seeds 920001..920022, 920023..920043, 920044..920064). Every listed seed is run and reported; none is dropped, replaced or rerun
 (a crash that is not a property of the program is rerun with the same seed).
statistic: per seed E_s, C_s; pooled ratio R = sum E / sum C.
declared value (rule fixed now; the same rule as our earlier own-code preregistration): the smaller of two one-sided 99 percent lower bounds that allow overdispersion across seeds:
 (a) cluster ratio estimator over seeds: se^2 = sum_s (E_s - R C_s)^2 / (S (S-1) Cbar^2), Cbar = sum C / S, LB_a = R - t(0.99, 63 df = 2.3870) se;
 (b) quasi-binomial (C_s | E_s binomial with p): p = sum C / sum E, phi = max(1, Pearson chi2 / (S-1)), u = p + 2.3263 sqrt(phi p (1-p) / sum E), L_b = 1/u;
 declared = floor(10^4 min(LB_a, L_b)) / 10^4. If any proposal has C and not E, declared = floor(10^4 LB_a)/10^4 and this is reported.
filed multiplier after this study: EXQ = min(24331/10000, declared). The study can only lower the filed value.
analysis: analyze.py (copied unchanged from our earlier own-code study).
at most 4 processes at once.
```

**Result** (`analyze.py`, as preregistered): 64 seeds, 2^32 late proposals; E = 323,337, C = 131,195, cell-and-not-collision 0 in every seed; pooled ratio **2.46455** (per seed 2.3491 to 2.5736); (a) cluster ratio estimator: se 0.00545, LB_a = 2.46455 - 2.3870 x 0.00545 = **2.45154**; (b) quasi-binomial: Pearson chi-square 67.72 on 63 df, phi 1.0749, u = 0.407836, L_b = **2.45197**; declared value floor(10^4 min) / 10^4 = **2.4515**. The filed multiplier is min(2.4331, 2.4515) = **2.4331**, unchanged.
The same run's cell-event factor (rows 16..36 follow every cell, under the kept-fibre law) has mean 2^-71.97397 over the 64 seeds (relative sd 0.0678), above the charged 2^-72.04; the stage factors of rows 16..21 are -16.9944, -12.9995, -8.0000, -9.9822, -6.9999, -2.0022 (log2).
Overdispersion-robust reading of runs 1-3 (uniform law): quasi-binomial with run 3's dispersion factor 1.786 on all three runs 2.4408; cluster ratio estimator over the 48 seeds of runs 1 and 3 (t with 47 df) 2.4464. Every bound computed is above the charge 2.4331.

Per-seed counts (seed E C):

```text
920001 5040 2034      920002 4943 2029      920003 4966 2054      920004 5074 2046
920005 5070 2044      920006 5078 2012      920007 5167 2149      920008 5225 2053
920009 5001 2053      920010 5137 1996      920011 5031 2065      920012 5055 2080
920013 5079 2083      920014 5113 2071      920015 5150 2038      920016 4954 1977
920017 5092 2084      920018 4980 2034      920019 5190 2145      920020 5070 2017
920021 4965 2018      920022 5000 1990      920023 5064 2012      920024 5050 2039
920025 5135 2071      920026 5026 1991      920027 5089 2144      920028 5183 2128
920029 5003 2015      920030 5101 2105      920031 4979 2038      920032 4993 2053
920033 4982 2049      920034 4984 1995      920035 5076 2018      920036 4936 1992
920037 4995 2002      920038 5060 2154      920039 5012 2021      920040 5040 2038
920041 5070 2043      920042 5102 2060      920043 4979 2046      920044 5024 2069
920045 5110 2070      920046 5100 2092      920047 5019 2028      920048 5009 2017
920049 5044 2106      920050 5179 2095      920051 5035 2031      920052 5119 2079
920053 5059 2066      920054 4991 2021      920055 5104 2055      920056 5126 2014
920057 4888 1933      920058 5142 2086      920059 5056 2019      920060 4918 1977
920061 5042 2061      920062 4963 2077      920063 5176 2154      920064 4994 2059
```

`genk.c` and `q3k.c` are identified by the hashes above and are not listed here (evidence size limit); `genk.c` is the definition of G (Lemma 4.2) and of the kept fibres (Section 8.1, THETA = 48) written as loops over E4 and x, as described above.

### D.4 The work cap by Bernstein's inequality

Section 10's premises are unchanged: the v_f are independent (H1), 0 <= v_f <= vmax_fb, E[v_f] <= vbar and therefore E[v_f^2] <= vmax_fb vbar. Bernstein's inequality for a sum of N independent variables with |v_f - E v_f| <= vmax_fb and total variance at most N vmax_fb vbar gives, with t = s N vbar,
Pr[sum v_f - sum E v_f >= t] <= exp(-t^2 / (2 (N vmax_fb vbar + vmax_fb t / 3))) = exp(-s^2 N vbar / (2 vmax_fb (1 + s/3))); since sum E v_f <= N vbar, this bounds Pr[sum v_f > (1 + s) N vbar]. The ledger evaluates the exponent as an exact fraction, its exponential with 60-digit decimals, and rounds the result up by a factor 1 + 10^-30.
The slack s = 1/3680 minimises T over s = 1/k at this filing's q3 (log2 T 60.16721164; fcbc9c83: 60.17143973). Chebyshev with ffbe30bb's slack 2^-10 would give 60.16894 here (fcbc9c83: 60.17316).
This is the inequality of the accepted ledgers' work-cap analysis with a sharper tail; no new premise is introduced.

### D.5 The rare path as executed

Per l of a looked-up mask the program runs (D.1): the y-words and loop 8, row 16 computed 106, row 17 computed and checked 160; rows 18..21 computed and checked (160 each) while they pass; when row 21 passes, rows 22..36 computed (15 x 106) and the comparison (16). The ledger charges c3b_l = 8 + 106 + 160 = 274 always and c3b_t = 4 x 160 + 15 x 106 + 16 = 2,246 with probability REACH = 2^-12, for every probed lane and every l of its mask (c3b_pair = 239 per hit lane as before).
REACH bounds the probability that row 17 passes for one l (then rows 18..36 may run): the mean SMC stage factor of row 17 is 2^-13.000 in each of the three studies of Appendix B.3 (352 replicates; 2^-12.998, 2^-12.996 and 2^-13.002 in the three replicates printed there), and every later row is reached with a smaller probability, so charging all of c3b_t at 2^-12 is an upper bound with one bit of margin. ffbe30bb charged 2 x 160 for rows 16 and 17 and 19 x 160 at 2^-9.
The worst case of one first block, vmax_fb, charges every l through row 36 and the comparison: NVAR x (44 + 5 + 4 + 2 + 1.1 x (239 + 32 x (274 + 2,246))) + 2 x (270 + 132) + 200 = 1,077,492,591,596 (fcbc9c83: 1,077,541,006,432).

### D.6 What was not tested

- R is measured by Monte Carlo, not proved: runs 1-3 under the studies' law of the late words (W6, W7 uniform on F6 x F7, W8 from the variant list), and the preregistered run of D.3b under the attack's kept-fibre law of (W7, W8) (a pool of 16,384 values of x, a sample of that law). No stratification by l was run (an earlier control on Table 15 states with kept-pool W8 weighting gave 2.484 over 4 x 2^26 proposals; F7 branch strata 2.43 to 2.50).
- Runs 1 and 2 were run before the declared-value rule was written; only run 3 is preregistered. The rule makes the charge the smaller of the bound on runs 1 and 2 and the bound on all three, and the charge is below every bound computed from run 3 alone.
- The reverse direction of D.2 (equal outputs imply conditions (i)-(iii)) is computed, not proved; the program does not depend on it.
- The organizer experiments construct collisions outside the printed cells and check that the counted program accepts them; they do not estimate R.
- The overdispersion of run 3 (chi-square 55.4 on 31 df) is allowed for by the quasi-binomial and cluster bounds of D.3 and D.3b; these rest on approximate normality of the pooled counts and of the per-seed ratio estimator.

### D.7 Credit

Jbenisek (fcbc9c83, ffbe30bb), with Claude (Anthropic, Claude Code): the collision-event program change, the runs, the preregistration, the Bernstein bound, the rare-path execution charge, Appendix B and Appendix D. Th0rgal (7c46d8cb, fe65a7cb): the tightened online operation counts of Section 9 (`ZPLANE_OPS = 66`, `CVPRE_OPS = 73`, `FBFIX = 195`, `SCAN_LANE = 5`, `SEG_OVH = 4`, `GROUP_OPS = 30`, `GROUP_FULL = 44`, `UNROLL = 32`, `LOOP_SEG = 13`) and their synthesis with fcbc9c83 and ffbe30bb. 0xshikhar (fb039a6e, c3041753) and their lineage: everything else.
