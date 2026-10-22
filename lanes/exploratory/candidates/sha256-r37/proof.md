# Draft P6 derivative of aa0e8b6 (P4 algorithm, P5 q3c declaration, P9 contiguous-scratch cells): Top-first 15, residual exact test, q3c measured directly on the submitted pool

Track `sha256-r37-exploratory`; target `sha256-r37-prefix-v1`; C = 2644. Claim: time_log2 = **57.15316**, memory_log2_bytes = **20.0** (actual bound 962,826 bytes), success probability >= 0.39 under the inherited premises. The first blocks are computed seven at a time in one 256-bit register (P8, Section 9.11, inherited unchanged); the mechanism is credited to samsmith's f1163fcf, lamb356's 22fc4519 and dredozubov's ffca313a, the text and its count are written here from scratch.

This is a credited derivative of Jbenisek's aa0e8b6a-6fd1-4a8b-9917-bb5e0f8a689f. Two algorithm changes, credited to slkzgm's f2da0e13-698a-4f8b-87d8-6c5914918da8 (57.89863) and inherited unchanged here: (1) an 8192/2048-word Low-first 13 conditional probe instead of the eager 4096/4096-word LO/MID probe; (2) the residual three-condition exact test, 13 rather than 34 operations. One further change is statistical and is our own (d3e7fe15-02f2-4f04-8170-13923742c0a2, credited): the declared cell bound q3c is measured on this filing's own variant list by fresh preregistered blocks, 2^-71.4162 (Appendices G.3, G.5 and N), instead of any bound transferred from the parents' pool (Section 7.4c, Appendix G). One family change is also ours. The examined family is restricted to the four kept lists (0, 1, 5, 6): 170 of the parents' 222 classes and 599,760 of their 782,800 variants. The restriction is **0.18163 bit** of exact ledger arithmetic on R37P29's program: the filed family's row 57.21653 against the ten-list family's 57.39816, both priced by `experiments/lowm.py` on the
same group stage (`reports/receipts/r37-tenlist-60.out`; its control reproduces the filed family bit for bit). This revision does not re-price it: on the four-bit program the ten-list table holds a cube-{0, 7} class this filing does not build (`r37-cube4file-100.out`). The earlier cells (0.11133 bit at 57.33131 on R37P23's program, 0.11361 at R37P24) are superseded by this re-pricing. The charge that decides it is the per-pair preparation `c_c = E_class/(P6 n)`: 10.6860-10.9224 on the four kept lists against 20.1644-20.7967 on the six dropped ones, against a break-even of 11.5060 ops per pair on the filed family, so every dropped list is dearer than the family it would join. The member charge per variant runs the other way (2.4709-2.4734 kept against 0.9867-0.9882 dropped) and is not the deciding quantity; the earlier per-variant member-charge comparison of the dropped and the kept lists is a superseded sensitivity that does not reproduce under this revision's member charge (the receipt prints both ranges). q3c is then declared from this filing's own direct study of the submitted pool (Appendix N): **2^-71.4162**, the one-sided 99% lower bound of the mean of the 16,384 *linear* estimates of block F on the 599,760-word list (seeds 800000..816383, mean 2^-71.41331, relative sd
of the linear estimates 0.1095, bound 2^-71.41618, rounded down; the 32 shard statistics and the digest of all 16,384 values are in N). Block E's log-scale declaration 2^-71.4243 (claim 57.58779) is 0.0087 bit weaker on the same data and is a stated sensitivity (Appendix G.5). No sub-pool transfer allowance is paid: the two pools' measured means differ by 0.0003 bit, and the parents'-pool pooled bound 2^-71.4474 (claim 57.61074) and the same bound less the 0.0020-bit allowance (2^-71.4494, claim 57.61273) remain stated sensitivities. Structurally, under Lemma 7.1 the variant enters q3 only through the four W24 conditions on `W24x = Z + W8x`, so with `Z` uniform the map `W8 -> Z + W8` is a bijection and the tail probability is the *same number* for every variant, hence every uniform-weight sub-pool has the same q3c exactly; this filing keeps a uniform-weight subset, not an x-reweighting, so the 0.0104-bit fibre-weighting gap of fb039a6e's preregistered study (Section 7.5) is not the transfer that applies to it, and the flat 0.05-bit hedge the parents' text prices for an x-weighted subset is not paid either. Both superseded charges are carried as stated
sensitivities: the 5x measured charge (0.0104 -> q3c 2^-71.4578, claim 57.62108) and the full 0.05 case (claim 57.62942). All three changes are disclosed; nothing else is changed. The executed cube law is inherited unchanged: Q0[0] has probability 1/4, and bits 2 and 3 each have probability 1/2 under H1. The Bernstein slack and cap are recomputed for the cheaper stages. The characteristic, S, variants, 170 classes, F6/F7 filters, H1-H7, A_C, A_S, DEV and PRE are inherited unchanged; q3c is declared from the same preregistered replicates under a tighter admissible statistic (Section 7.4c); numerical consequences in H5 are updated.

aa0e8b6 claimed 58.02135 (unrounded 58.021341413842665); its ledger is reproduced exactly with N = **773438176907133806360** and the same executed cube law. Our unrounded time is **57.15315147653251**, N = **423715539702882534803**. The collision event is identical, so the algorithm changes are a conditional cost improvement, not new success evidence; the q3c declaration (0.0119 bit above the parents' pooled bound, 0.0274 above the preregistered min-of-blocks bound) is the second, statistical change.

**Validation status.** Independent arithmetic, affine counts and exhaustive tables/residual checks pass, and the deterministic intake gate accepts the package (`validate_candidate` returns `submission_state: ready`; the package digest is computed by the organizer's run from the payload and is therefore not quoted here; certificate manifest empty and verified). The five organizer experiments are unchanged from f2da0e13, and their two-run validation is now reproduced here rather than inherited: the organizer's containerised executor runs through the rootless Docker socket (`DOCKER_HOST=unix:///run/user/1000/docker.sock`, 45 s for all five), and two local executions produced byte-identical reports (`report_sha256` 79f5e4f39f8e1f6fe5725e7e1fd41d2f565e24f4c62a6cf273da9bcb9f4aa716; 256 trials each, every status `completed`, every recorded mismatch counter zero). This participant also re-executed `selftest` (its ten-line transcript is byte-identical to Appendix D), `ledger` twice (byte-identical) and `memory`; the ledger agrees with the independent Appendix B mirror to the digit and the memory figure with the table hash.
P4 observations are recorded in the P4 executor observations section; inherited first-person evidence below retains its original authors' voice and credit.

**Credited derivative of sraiw's d9f8833d-2483-478a-9815-4baea4bf5214 (59.30883), of fd115760-37ba-49c3-814e-35c44f32761c (sraiw, 60.90319), 96169e7c-8ea2-4090-afc8-edbc6aca0c98 (59.31513) and ad06162f-1038-4d01-a06a-445e2238dc54 (60.71121), and of our 67516603-7f51-4b80-806d-9f4a379dab56 (59.5556, ruled not_evaluable on H1, H2, H3), 221eb058-623b-41d6-a7bf-1d9b4602ce1e (60.97003) and ec1340aa-ecc8-4564-8df7-006f0a2b2ce5 (R37OWN5, whose organizer experiments and statements of the premises H1-H3 are reused here) and of our 4ec21bf9-f588-4b80-bb2b-77c1ccf8c9b7 (R37R, 60.11997, passed review; its exact collision event after row 21 is carried over here, Section 7.7)**, with Th0rgal's 0db0eeb6-9958-43af-9700-ea9e99cee016 (61.17784), the four-value-pattern acceptance of rows 18 and 19 from Jbenisek's ffbe30bb-ac92-4191-a589-3bf32661ee7d (60.38707), R16x from 221eb058, and the lineage of all of them (Section 2): winglock's 6c77089c and 7319bba9, dd6656d4 (Th0rgal), itseasypop's 1c368173, qkniep's b947b377, GordoAR's 087a18c4,
0xshikhar's 1f12a09a, fb039a6e and 2f540248, companygardener's d3ec5c41, 44921815 and 8de337d5, 8aeaed1c, def128fc and 22b7dd8b (Jbenisek), Th0rgal's f2fe1d4d and Jbenisek's c22f86a2, newjordan's 9c6967cc, jungjipdo's ffc8c2df, and 6eeefb64 for the price of a solver CPU-second.
The attack, the characteristic, the sets F6, F7, L*, the family of A0-variants and its 222 largest classes, the packed good-pair arithmetic, the rows 16..36 check (cells through row 21, the collision event after it: 4ec21bf9), the four-pattern and R16x relaxations and their q3 studies, the bit-sliced algebra of the W7 and W6 programs, the 4-lane exact row-16 table stage, the zero-base scan table, the premises H1-H3 and the ledger structure are theirs.
**Inherited aa0e8b6 history: what it changes against d9f8833d (three items).** (1) The cap on the data-dependent work is bounded by Bernstein's inequality for sums of independent bounded variables instead of Chebyshev's: the work v_f of a first block lies in [0, vmax_fb] and the first blocks are independent (H1), so Pr[sum v_f > (1 + s) N_FB vbar] <= exp(-t^2 / (2 (N_FB vmax_fb vbar + vmax_fb t / 3))), t = s N_FB vbar, which allows the slack s = 1/18000 instead of 2^-11 and a work-cap failure probability Pcap = 3.84e-07 instead of 0.00023325, so that both V_MAX and mu0 fall (Section 10, Appendices B, C). (2) The premises H1, H2, H3 are stated as our theory and are answered with organizer experiments on real first blocks, as in ec1340aa: `h1-cv1-filters-nonce`, `h3-cowpass-nonce` and `h3-ladder-r37` (distinct variants of one first block through the W6 filter, the two table stages and the exact row-16 test, with the dependence factor of each level; Appendix H); the `q3_smc_check` of d9f8833d is dropped from `a0-online-r37` to keep the experiment sources below the organizer's 64 KiB. (3) The success event is the collision after row 21, as in our accepted 4ec21bf9 (R37R, Appendix D there): rows 16..21 are checked cell by cell, rows 22..36 are computed without cell tests and a pair is accepted iff the two 37-step outputs are equal; q3 is the cell probability q3c of rows 16..36 times EXQ = 2.4331 (the inherited value; Appendix O supersedes it), the preregistered one-sided 99 percent lower bound of the ratio of collision to cell events after row 21 (Section 7.7), and the rare path is charged for it in full with no early abort (Section 9.9). The program, its plane algebra and its ledger inputs are d9f8833d's, with the changes of this filing in the header of `experiments/lowm.py`.
**What d9f8833d changed against 96169e7c, ad06162f and 221eb058 (credit; all of it counted exactly):** (1) base-value constant folding of `e4` and `e3` into `CB3`; (2) two's-complement negation of `e3`; (3) exact carry folding at bits 15..16 of `e3` and bits 18..19 of `Sq`; (4) single-carry split of `F6(W - cu)` at `c_4(cu)` (`SUBF_OPS` from 87..97 to 11..28, `SPILL` from 64 to 18 or 30); (5) dynamic bit-0 invariance `I = (q & B) | (CB3 & 1)`; (6) exact carries `c_17, c_21, c_28` in `F6` when `full=False`; (7) two-pass constant factoring in `c7` (`F7_OPS = 112`); (8) bit-lexicographic `REP_ORDER` per list; (9) unrolled register-cached cube expansion and shift-register placement (`PLACE = 6`, `5m + 1` per rep); (10) the 4-lane exact `(lo, mid)` row-16 filter (`PNZ = 63,512 / 2^24`, `MU = 1/256`); (11) the zero-base 8192-word `scan_table` with 4-lane packed `Ul`/`Um` addresses (`CLS_LANE = 5`, `SCAN_LANE = 7`, `SURV_LANE = 6`, `PROBE = 11, 8, 8, 6`); (12) the calibrated `A_C = 2^48`; (13) half-adder carry reuse in `fa_step2` and polarity-aligned F6 synthesis (`W6_OPS` 181..301, `vbar` 27,775.96).
## 0. Summary

- The complete-message algorithm, characteristic, q3 = 2^-71.4162 x 2.482 = 2^-70.10470,
  success event after row 21 and all statistical premises are inherited.
- Second change (statistical, our own): q3c_used = 2^-71.4162, the one-sided 99% lower bound of
  the mean of the 16,384 linear estimates of block F, fresh seeds preregistered on this filing's own variant list (Appendix N), with no sub-pool transfer allowance; block E's log-scale 2^-71.4243 (claim 57.58779) is a stated sensitivity. The parents'-pool pooled bound 2^-71.4474 (claim 57.61074) and the same bound less the 0.0020-bit allowance (2^-71.4494, claim 57.61273), and the preregistered min of the two per-block bounds (2^-71.4629, claim 57.62615), remain stated sensitivities; the ledger uses q3 = 2^-71.4162 x 2.482 = 2^-70.10470.
- FIRST[u[23:9]] is read first. Only a nonzero FIRST word triggers SECOND
  on u[8:0]. The state intersection decides all thirteen low-24 conditions exactly. Only E16x[30]=0, A16x[25]=A15x[25], A16x[29]=1 remain.
- The first probe stage is 12 operations per four lanes (bits 9..23 are shifted on every lane, 9.7c/d); continuation is six
  per nonzero FIRST, including its own work-counter update. FIRST is nonzero for 2207/32768 indices. Fold and scan are unchanged. EX_OPS = 13.
- N_FB = 30821562976875433; FIXED = 490; FIXED_P7 = 464 (Section 9.11);
  vbar = 136845530424683277834001/10737418240000000000; vmax_fb = 857953744881187/15625; V_MAX = 392837736089609602185; slack = 1/15625; Pcap = 4.40E-07 <= 4.40e-07.
- P8 (Section 9.11): seven first blocks per 256-bit register, SB_OPS = 2,914 per seven,
  charged as SB_FB = 417 per first block (the ceiling paid) instead of one compression; FIXED_P7 = 464 because the batch carries the 30 word-extraction primitives. Per first block 6.94232 units at R37P22, 5.24937 at this revision.
- N = 423715539702882534803 and T=N/2644; rounded claim 57.15316. Memory is 962,826 bytes,
  including an added 1,024-byte code allowance; the batch adds no resident item (inside the 64-register file). PRE = 2^38 operations.
- Validation (c) completed under the public seed; two byte-identical runs only.
- **This filing (R37P22) changes one ledger cell: `MEMBER_CHARGE` 6,7,8,11 -> 4,6,7,9** (the completion test and its branch are not executed where the discipline completes a group word on a fixed schedule, Section 9.6). Nothing else moves: `selftest` and `memory` are byte-identical to the previous filing (6,548-byte diff of `lowm.py` text: one tuple), the experiment source budget is 65,499 <= 65,536, vbar 15221.48773651485 -> 14711.52812450294, per_fb 6.09020 -> 5.89733, N 500055279001585913851 -> 484337152086165523954, claim **57.39215 -> 57.36716 -> 57.34607**.

- **P10 moves one chosen constant**: the cap slack s = 1/15625 (the assumed cap and N_FB follow), the interior optimum of T at this vbar (Section 10); claim **57.15317 -> 57.15316**.
- **P9 re-priced two cells and nothing else**: the 47 broadcast planes of `CB3` and `KZ` are a fixed set in one contiguous scratch area (slot `32k`), so each store and load is `base + immediate` with no address add (the zero-base `scan_table` precedent, Section 9.6). `CPREP` 260 -> 213 (`10 + 6 + 141 + 47 + 9`), sweep `3 + 2 (len(u) + 47)` -> `3 + 2 len(u) + 47`; `zq` keeps its add (data-dependent selection). vbar 12998.322039161183 -> 12744.733171973683, N_FB -> 30822109419656358, N -> 423720655015460848838, claim **57.17954 -> 57.15317**; no probability, family, memory or other ledger cell moves (`selftest` 0 mismatches, `memory` 962,826 bytes).
- **Earlier revisions of this line (R37P21, R37P22, R37P23) moved one ledger cell each**: `MEMBER_CHARGE` 6,7,8,11 -> 4,6,7,9 (57.39215 -> 57.36716), the per-group work counter with `GROUP_BODY` 32 -> 31 and `CF_CLASS` 8 -> 9 (57.36716 -> 57.34607), and the body's two address masks collapsed into one, `GROUP_BODY` 31 -> 30 (57.34607 -> 57.33131). Each is filed, with its own cap constants, in its own revision's package.

- **R37P24 changed two cells of the group stage: `GROUP_BODY` 30 -> 29 and `PROBE` 12 -> 11 per group**
  (Section 9.7d): vbar 14551.608009508891 -> 14231.767779520793, per_fb 5.83684 -> 5.71587, N_FB 30821625285060259 -> 30821662669971155, N 479408110915732052688 -> 469550107797560996585, claim **57.33131 -> 57.30134**, mu0 0.49466475, floor 0.3900000005617252 > 0.39.
- **R37P26 removed one primitive per group body: the `& LM` on `s0W` is not executed** (Section 9.7e) --
  `GROUP_BODY` 29 -> 28, vbar -> 14071.847664526744, per_fb -> 5.65539, N_FB -> 30821686347081389, N -> 464621171808912507747, claim **57.30134 -> 57.28612**; cap 1.648032611817215e-06 <= 1.65e-06, mu0 0.49466513, floor 0.3900000021895876 > 0.39.
- **R37P27 charged the residual group word at its measured rate (Section 11.1)**: the `pad` counter fires in 9 of
  5,000 first blocks, so the one-sided 99% Poisson bound replaces the worst case; claim **57.28612 -> 57.28224**.
- **R37P28 removed the scan's chunk extraction from zero rows (Section 9.6)**: the row test charges
  21.514/18.507/15.858 at nl = 256/194/176 at the measured 99% nonzero-row rate; claim **57.28224 -> 57.23502**.
- **This revision (R37P29) hoists the scan's chunk base (Section 9.6)**: inside a nonzero row the two
  per-lane address adds become one running chunk base per nonzero chunk plus one add per set lane, SCAN_LANE 6 -> 5 and the base charged at the measured chunks per run (2.8941/2.3063/2.0717 at nl = 256/194/176, one-sided 99%; `r37-chunkrate-79.out`, 30,430 runs). vbar -> 13362.00091275684645, per_fb -> 5.38691, N_FB -> 30821847725280088, N -> 442743526089601565433, claim **57.23502 -> 57.21653**; cap 3.23e-06, mu0 0.49466772, floor 0.39000000091399101 > 0.39; ten-list comparison 0.18163 bit.
- **This revision (R37P30) installs the four-bit form of Section 8.1 for the 164 classes whose cube has bit 7 free**: the class is stored as its 216/225-rep half and the two batches of Section 9.4 are that one rep set with plane 7 clear and set (`nl` (216, 216) and (225, 225)); the six classes without the free fourth bit keep (256, 176) and (256, 194). `CUBE_CAND` gains 7, `SPILL_K` gains k = 4, `CUBE_D` is built over 0x8d, `ROW_FIX` gains 216/225 and `gather` flips the second batch by 0x80. vbar -> 13287.411417157862, per_fb -> 5.35870, N_FB -> 30821872648554019, N -> 440444759662825425482, claim **57.21653 -> 57.20902**; floor 0.39000000473206742 > 0.39. Source 65,214 of 65,536 B (605 B of trailing comments and 156 B of section notes removed, the credit header intact; +150 B of checks).

- **This revision (R37P38) resplits the row-16 probe top-first 15/9** (Section 6.2): the first stage is
  indexed by u[23:9], the second by u[8:0], the interface state is (carry_e, carry_a, a_lo[6], a_lo[8]),
  and at most two states per l survive the prune (two on 22 of the 32 l). Nothing else in the ledger
  moves: `GROUP_BODY` stays 28 and the continuation stays six, but every lane's first address is now
  `(U >> 64k+9) & 32767`, so lane 0 no longer saves a shift and `PROBE` returns to (3,3,3,3), 12 per
  group. The gain is the density: the first stage fires on 2207 of 32768 indices instead of 1513 of
  8192, which takes the continuation term from 705.601 to 257.301 ops. vbar -> 12998.322039161183,
  per_fb -> 5.24937, N_FB -> 30821984180204858, N -> 431535514349995688838, claim **57.20902 ->
  57.17954**; floor 0.39000000582 > 0.39; the memory falls to 962,826 B. Source 65,152 of 65,536 B.
  The h3-ladder row of Appendix H and the P4 participant diagnostic were measured against the 13/11
  tables and remain historical records of those revisions.

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
- 4ec21bf9-f588-4b80-bb2b-77c1ccf8c9b7 (ours, R37R, 60.11997, passed review; Appendix D there): the collision event after row 21 as the success event (`step3b`, `same_out`), its structure (D.2), the ratio of collision to cell events and its preregistered lower bound EXQ = 2.4331 (D.3, D.3b) (superseded here by Appendix O) and the pricing of the rare path as executed (D.5), carried over here onto this package's program and constants (Sections 7.7, 9.9). The exact-event scoring of the late rows was designed there with GPT-6-Luna (OpenAI); the reduction of the late rows to conditions on W22, W24 and W26 was first proposed by GPT 5.5 (OpenAI).
- Filings on this track, declared as dependencies: 6c77089c (winglock): transcription of Tables 15-17, the exact sets F6, F7 and L*, the SMC design for q3. dd6656d4 (Th0rgal): affine decomposition of F6, F7. 1c368173 (itseasypop), b947b377 (qkniep): the A0 freedom of the Step-1 solution and the c7 classes.
  087a18c4 (GordoAR): the exact-rational ledger and the success analysis. 1f12a09a (0xshikhar): the 170 classes and the packed groups of four 64-bit lanes. 7319bba9 (winglock): the program structure, the row-16 enumeration, the preregistered q3 studies, the end-to-end rates. d3ec5c41, 44921815, 8de337d5 (companygardener): the counted-program framework and the ledger. 8aeaed1c, def128fc and c22f86a2 (Jbenisek): the direct row-16 lane read and the cap slack squared in the Chebyshev bound (replaced here by Bernstein's bound, Section 10).
  f2fe1d4d, 0db0eeb6 (Th0rgal): the MAJ identity, the single packed member word `Gw` and its 31-operation group. fb039a6e (0xshikhar): the bit-sliced additions with register-resident planes and the q3 studies over the whole family (cited, not used). 6eeefb64 (sha256-r32): the calibrated price of a solver CPU-second behind A_C.
- **Historical aa0e8b6 changes and costs (over 96169e7c, ad06162f and 221eb058; not P4 sensitivities).** In addition to the base-folded `CB3` and two's-complement `H'` formulation of `W6x` (Lemma 8.1, Section 9.5), the list-invariant carry folding at bits 14..16 of `e3` and 18..19 of `Sq`, the single-carry split of `F6(W - cu)` at `c_4(cu)`, the dynamic bit-0 invariance `I = (q & B) | (CB3 & 1)` (Lemma 8.2), the carry-only evaluation of bits 17, 21, 28 in `F6` when `full=False`, the 16-plane constant factoring of `c7 - C7_CONST` in the W7 class test (`F7_OPS = 112`), the per-list `REP_ORDER`, the unrolled register-cached cube expansion and shift-register placement (`PLACE = 6`), the 4-lane exact `(lo, mid)` row-16 table filter (`SURV_FIX = 13`, `PNZ = 63,512 / 2^24`, `MU = 1/256`), the zero-base `scan_table` at word address `0..8191` with 4-lane packed `Ul`/`Um` chunk-address extraction (`CLS_LANE = 5`, `SCAN_LANE = 7`, `SURV_LANE = 6`, `PROBE = 11, 8, 8, 6`), and the calibrated characteristic-search allowance `A_C = 2^48` (Section 11.2), this filing adds half-adder carry reuse `(xy & c) | ac` in `fa_step2` and target-flag polarity alignment (`andf`, `orf`) in `f6_ok_upper` and `f6_combine_pre` (cutting `W6_OPS` from 186..313 to 181..301, `SUBF_OPS` from 11..31 to 11..28, and `vbar` from `27,911.58` to `27,775.96`), reducing total `time_log2` from 59.31513 (and 60.71121 in ad06162f) to 59.30883 (and 60.69185 under `A_C = 2^60`); this filing adds the Bernstein cap bound (Section 10), which gives 59.30006, and the exact collision event after row 21 (Section 7.7), which gives 58.02135 (60.32595 under `A_C = 2^60`).

## 3. The characteristic (from the paper, as transcribed in 6c77089c; re-checked by `experiments/lowm.py`)

### 3.1 Notation and orientation

Symbols are MSB first: `n` = bits (x, y) = (0, 1), `u` = (1, 0), `0`/`1` fixed and equal, `=` equal, `+` = equal on both members and equal to the same bit of the vertically adjacent `+` (E_i[b] = E_{i+1}[b]). Member x is the message the paper prints second (M'); with this orientation every cell holds on the published pair (checked).

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

Rows -4..3 are entirely `=`: **A0..A3 and E0..E3 carry no condition** (the chaining value is common and A0..A5, E4, E5 have no difference).

### 3.3 Two-bit conditions as printed (Table 16), with the corrected reading

```text
A15[15] != A16[15], A15[23] = A16[23], A15[25] = A16[25], A16[9] != A16[20], A16[18] != A16[6]
A16[8] = A16[17], A15[29] = A17[29] (printed: A16[29] = A17[29]), A17[29] = A18[29], E15[4] = E16[4]
E17[0] != E17[13], E16[24] = E17[24], E16[15] = E17[15], E18[6] != E18[19], E18[2] = E18[20], E20[2] != E20[16]
W6[1] = W6[12], W6[8] != W6[25], W6[14] = W6[18], W7[0] = W7[28], W7[9] = W7[30], W7[1] = W7[18]
W8[1] != W8[12], W8[8] != W8[25], W8[14] = W8[18], W22[31] != W22[1], W22[30] != W22[0]
W22[16] != W22[25], W22[14] != W22[21], W24[4] != W24[6], W24[22] = W24[31], W24[20] != W24[27]
```

The algorithm checks every cell; on rows >= 16 it also checks the printed two-bit conditions (they can only lower the success probability, and q3 is defined with them). The W6, W7 two-bit conditions are replaced by the exact filters of Section 5.1; the W8 conditions are part of the definition of G (Section 4.3).

### 3.4 The SFS pair (Table 17)

```text
CV  63b4986c 35d83dc0 c98894e4 784e08fc 78a7f752 5ed877a8 315a2db3 d5614eb4
M   4d7f86ff 32ece589 d8accfc4 2cc2e433 068b5b34 eba68a28 2fe12cad 6aa26b0c
    9f0d78e1 681b8277 faa9c7e0 56aed439 cc2dbbc2 dd2ba0fc b95d377b 5dd43a81
M'  4d7f86ff 32ece589 d8accfc4 2cc2e433 068b5b34 eba68a28 0fe12cad 6ee2630c
    bf0d78e1 6d1a90dd faa1d3e0 56aed439 cc2dbbc2 dd2ba0fc bd1d3f7b 7dd43a81
hash a856d46e 4b46eb28 4935248c 92a2fc98 e0fb2610 10a9951f 54264f5b 80954580
```

F_37(CV, M) = F_37(CV, M') = the printed hash; every cell of rows -4..36 and every printed two-bit condition holds with x = M', y = M (`experiments/lowm.py` rebuilds both members and checks the cells; the repository verifier reproduces the hash).

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

**Lemma 4.1.** With these words, F_37's steps 0..13 from CV1 reproduce the state rows A0..A13 (and the E_i) exactly, and for fixed A0..A13 the map CV1 -> (W0, ..., W7) is a bijection of (2^32)^8: W7 depends only on A_{-1}, W6 is -A_{-2} plus a function of A_{-1}, ..., W0 is -E_{-4} plus a function of the earlier coordinates (each step inverted for its new coordinate). W8..W13 do not depend on CV1. *Proof.* Substitution; `lowm.py` (`words_from_cv`, `invert_cv`, `sfs_trial`) checks the reproduction and the inverse on every constructed pair.

### 4.3 The A0-variants (itseasypop 1c368173, qkniep b947b377; re-derived here)

**Lemma 4.2 (variants).** Replace A0 of S by any a0 (both members: rows 0..5 of S carry no difference) and keep A1..A13 of both members. Then, for every chaining value: (a) E5..E13 and W9..W13 are unchanged (E_i for i >= 5 involves A_{i-4..i} with i-4 >= 1; W_i for i >= 9 involves
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

Define **G = {a0 : E4 = a0 + C4 has E4[31:29] = 000, W8x = W8C - E4 has W8x[29] = 1, W8x[1] != W8x[12], W8x[8] != W8x[25], W8x[14] = W8x[18]}**. Exhaustive count over the 2^29 values of E4 with E4[31:29] = 000 (a0 = E4 - C4 is a bijection; counted by 0db0eeb6, and 7319bba's `genum2.c` agrees):
|G| = 12,103,680 = 2^23.529 (the count of 7319bba's `genum2.c` is reproduced). The published A0 (1b21ce20) is in G.

**Lemma 4.3 (validity).** For a0 in G, every chaining value CV1 whose words (Lemma 4.1 with A0 = a0) satisfy the filters W7x in F7 and W6x in F6 (Section 5.1), and every l in L* (Section 6), the pair follows every cell of rows -4..15 of A, E and W except the XOR cells of W6 and W7, and every printed two-bit condition closing at a row <= 15 except those on W6, W7; and every modular difference that enters the message expansion (W6..W15 and s0(W6..W15), s1(W14), s1(W15)) equals that of the published pair. *Proof.* Lemma 4.2 for E4, W8 and d6, d7; the filters for s0(W6), s0(W7) (Section 5.1); everything else is S's or l's. *Checks:* every good pair of the organizer experiment `a0-online-r37` and of the end-to-end runs (Section 13.1) against all 32 l.

So a variant changes A0, E0..E4 and W0..W8 only. W8 is the only changed word that enters the expansion beyond W8 itself (W23 via s0(W8), W24 directly); Section 7 shows this is all that can change q3.

## 5. Step 2 with variants

### 5.1 The exact filters

The characteristic fixes the modular differences of W21, W22, W23; with S (or any variant) fixed, the only remaining requirements on W6, W7 (6c77089c, Lemma 3) are W6x in F6 and W7x in F7, where F_k = {w : s0(w + d_k) - s0(w) = t_k mod 2^32}, d6 = 20000000, t6 = 03c00800, d7 = fbc00800, t7 = 017f8000. |F7| = 68,157,440 and |F6| = 287,309,824
(exhaustive over all 2^32 words by 0db0eeb6, Tungsten; the counts of 7319bba's `f6chk.c` agree). By the carry pattern of w + d (s0 is linear), each set is a disjoint union of affine spaces. We use them in the following bitwise form, **checked against the definition on all 2^32 words** (0db0eeb6, Tungsten: about 10 CPU-minutes, zero mismatches for both; here `selftest` and the organizer experiments compare the plane programs with the definitions):

```text
F6: w is NOT in F6  iff  common | (w29 & (bc | (w30 & X)))  with
      common = (w14^w18) | ~(w8^w25) | (w1^w12),   bc = (w15^w19) | ~(w9^w26) | (w2^w13),
      X = (w16^w20^w31) | ~(w10^w27^w31) | (w3^w14^w31)                                  (bits are w_i; | is OR)
F7: w is in F7  iff  w1 = w18, w0 = w28, w9 = w30 and
      [ w11 = 0, w22 = 1, w26 = 1 ]                                                       2^26 words
      or [ w11 = 1, w12 = 0, w22 = 0, w23 = 1, w26 = 0, w27 = 1, w2 = w19, w1 = w29, w10 = w31 ]   2^20 words
```

(F6 is the form published in 087a18c4/1c368173 with b_bad & c_bad simplified to bc | (w30 & X); 7319bba derived the F7 constraint set from the affine hull of F7 and of its two halves (7319bba); here it is verified exhaustively against the definition.)

For a variant a0 and CV1 the filter words are (member x, from Lemma 4.1):

```text
W7x = c7(a0) - A_{-1},           c7(a0) = ab9a1763 + MAJ(A2, A1, a0) - CH(E6, E5, a0 + C4)
W6x = C6 - A_{-2} + MAJ(A1, a0, A_{-1}) - CH(E5, a0 + C4, E3),   E3 = K3C - MAJ(A2, A1, a0) + A_{-1}
C6 = E6 - 2 A2 + S0(A1) - S1(E5) - K6 = f538a8f7,   K3C = A3 - S0(A2) = 478132ed
```

### 5.2 Lemma 5.1 (distribution, per variant)

Under H1 (CV1 uniform), for every fixed variant a0: Pr[W7x in F7] = p7 = |F7|/2^32 = 2^-5.97763 and
Pr[W6x in F6 | W7x in F7] = p6 = |F6|/2^32 = 2^-3.90197 exactly; conditioned on both, (W0..W5) is uniform on
(2^32)^6, (W6, W7) is uniform on F6 x F7, and they are independent. For every l in L*, (W16, ..., W21) is then a bijective image of (W0..W5) for fixed (W6, W9..W15), hence iid uniform and independent of (W6, W7). *Proof.* Lemma 4.1 (bijection for fixed a0) and the inverse expansion W5 = W21 - s1(W19) - W14 - s0(W6), W4 = W20 - s1(W18) - W13 - s0(W5), ..., W0 = W16 - s1(W14) - W9 - s0(W1). (6c77089c's Lemma 2, for each variant.)

### 5.3 The 170 classes and their four lists

c7(a0) takes 22,976 distinct values on G (7319bba and 0db0eeb6 enumerate them). A *class* is G intersected with one value of c7; for all variants of a class and a given CV1, W7x is the same word, so one membership test decides the W7 filter of the whole class. **This filing examines the 170 classes with at least 3456 variants** (599,760 variants; 1f12a09a's selection, the family of 7319bba's registered q3 studies). Each class is {base XOR s : s subset of mask, a0 in G, c7(a0) = the class value} (the descriptors c7, base, mask, size are the table `CLASSES` of `lowm.py`).

**Fact (computed; `selftest` re-derives it for every class).** For all 170 classes base & mask = 0, so a0 = base + s = base | s = base ^ s with s a subset of the mask, and the set of s depends only on its list's mask; of the parents' **ten lists** the kept 170 classes lie in four (0, 1, 5, 6; 82 + 3 + 82 + 3 classes):

```text
list  mask      size  classes      list  mask      size  classes
 0    01fec08d  3456   82           5    01fec08d  3600   82
 1    01fec48d  3456    3           6    01fec48d  3600    3
 2    01fec09d  3456   15           7    01fec09d  3584   15
 3    01fec09d  3456    7           8    01fec09d  3584    7
 4    01fec0dd  3456    4           9    01fec0dd  3584    4
```

(111 classes of 3456, 85 of 3600 and 26 of 3584 variants; 17 bits vary in all: the union of the masks is 01fec4dd = bits 0, 2, 3, 4, 6, 7, 10, 14, 15, 17..24; the bits 0, 2, 3, 7, 14, 15, 17..24 are in every mask.) The program builds those four lists (0, 1, 5, 6) as the member sets of the first class of each list (by enumerating the 2^14 or 2^15 subsets of the mask against the definitions of G and c7) and lets every other class of the list use them; `selftest` checks, for all 170 classes and all 599,760 variants, that the variant base | s is in G, has the class's c7 and that the class has its size (0 mismatches). **The cube of a list (computed; asserted when the list is built).** The bits 0, 2, 3 of s are *free* in the lists 0, 1, 5, 6 (every member has its partner with the bit flipped), and bit 7 is free in the 164 classes of lists 0 and 5 but in none of the six of lists 1 and 6 (Section 8.1); in the parents' other six lists bit 0 is free (they are not built). B is the set of these bits (the cube of the list), and the list is the union over f subset of B of (reps xor f), where reps = the members with no cube bit:
432 reps (lists 0, 1), 450 (lists 5, 6), 1728 (lists 2, 3, 4) and 1792 (lists 7, 8, 9). The classes of the lists 0, 1, 5, 6 have a0 bit 1 set (base bit 1 = 1), which Lemma 8.2 needs for the bits 2, 3; the classes of the other lists have base bit 1 clear and use bit 0 only. A list is stored as the planes of its reps (14 or 16 bit planes per batch of 256: the cube bits are static zeros of the main run) and as packed entries (Section 9.6), 8 batches in all (the four kept lists, two each).
S0(a0) >= 8 on G and a0 < 2^29; over the 599,760 variants max S0(a0) = 0xffffbb5c (`selftest`), so (~S0(a0) & M32) <= 0xfffffff7 and no carry leaves a 64-bit lane of the packed words of Section 9.

Per first block over uniform x, every class passes the W7 test for exactly |F7| = 68,157,440 values of x, so the number of passing classes has mean 170 p7 = 2.698 and the number of variants in passing classes has mean 599,760 p7 = 9,518.
Passing classes are strongly correlated (their c7 values are close), so the counts are bursty; only expectations are used.

## 6. Step 3

### 6.1 L* (exact; from 6c77089c, re-checked)

L is the set of (W14, W15) for which rows 14, 15 of both members follow the cells (with the `+` pairs) and the four expansion differences depending only on (W14, W15) equal the published pair's; |L| = 4096. L* keeps the elements
whose row-16 modular differences equal the characteristic's: |L*| = 32, all with W14x = bd1d3f7b and W15x in

```text
 0:7dd41680  1:7dd41681  2:7dd416a0  3:7dd416a1  4:7dd41a80  5:7dd41a81  6:7dd41aa0  7:7dd41aa1
 8:7dd43680  9:7dd43681 10:7dd436a0 11:7dd436a1 12:7dd43a80 13:7dd43a81 14:7dd43aa0 15:7dd43aa1
16:fdb41680 17:fdb41681 18:fdb416a0 19:fdb416a1 20:fdb41a80 21:fdb41a81 22:fdb41aa0 23:fdb41aa1
24:fdb43680 25:fdb43681 26:fdb436a0 27:fdb436a1 28:fdb43a80 29:fdb43a81 30:fdb43aa0 31:fdb43aa1
```

(y side: W14y = W14x ^ 04400800, W15y = W15x ^ 20000000; element 13 is the published one.) Rows 12..15 of both members depend only on S and l, not on CV1 or the variant.

### 6.2 Row 16 without a mask table

For l in L*, E16x = C_l + u with u = W0 + s0(W1) (W16 = s1(W14) + W9 + s0(W1) + W0; C_l collects rows 12..15 of l, K16, s1(W14) and W9). With the cell E16[23] = 0 of Table 15, 28 elements of L* can hold row 16 (7319bba enumerated all E16x with the row's nine fixed x-bits, 2^23 per l, and found 1,052,672 pairs (u, l); l = 0, 2, 16, 18 have none).
**With R16x (Section 7.4c) the E cell of row 16 has eight fixed bits and every one of the 32 elements of L* holds row 16 for exactly 65,536 values of E16x: 2,097,152 pairs (u, l)** (`r16.c` with `r16data.h` generated from `experiments/lowm.py`, exhaustive over the 2^24 values of E16x with the eight fixed bits for each l; Appendix A). By Lemma 5.1 u is uniform for a good pair, so Pr[row 16 holds for l] = 65,536 / 2^32 = 2^-16 exactly and the expected number of row-16 hits per probed lane is 2^21 / 2^32 = 2^-11.
The earlier filings read the l-mask of u from a table of 2^32 words. **This filing decides row 16 from the cells.**

**Lemma 6.2 (the exact test).** For each of the 32 l let A16x = E16x + cxA_l with cxA_l = -A12x + S0(A15x) + MAJ(A15x, A14x, A13x) (rows 12..15 of member x for l). Then E16y = E16x and A16y = A16x - 2^29 (mod 2^32), computed for all 32 l. Row 16 holds for (u, l) iff all of the following hold (cells of row 16 and the two-bit conditions closing at row 16):

```text
E16x & 40461a80 = 00060800         the eight fixed bits 30, 22, 18, 17, 12, 11, 9, 7 of the E cell (E16 has no difference: E16y = E16x; bit 23 is free under R16x)
E16x[4] = E15x[4]                  the '+' pair of the E cells of rows 15 and 16 (E15[4] = E16[4])
A16x[29] = 1                       the A cell 'u' at bit 29: with A16y = A16x - 2^29 the XOR difference is 2^29 iff A16x[29] = 1
A16x[15] != A15x[15], A16x[23] = A15x[23], A16x[25] = A15x[25]          (A15x of l is a constant)
A16x[9] != A16x[20], A16x[18] != A16x[6], A16x[8] = A16x[17]
```

*Proof.* The cells of row 16 are the A cell (u at bit 29), the E cell (eight fixed bits, no difference), the W cell (none); the printed conditions closing at row 16 are the seven of Section 3.3 (A15/A16 three, A16 three, E15/E16 one); for all 32 l the difference of E16 is zero and cyA_l - cxA_l = e0000000, which is the statement on A16y. *Checks:* the test applied to all 2^24 values of E16x with the eight fixed bits, for each of the 32 l, gives exactly the set of u of the enumeration by `r16.c` (2,097,152 pairs, no pair missing and none added; Appendix A);
the experiments and `selftest` compare it with the generic row check (`row16_ok`) on random and near-miss values. QED.

**The table stage (top-first 15).** Put hi = u[23:9] (15 bits) and lo = u[8:0] (9 bits). For each l, compute e_lo = (lo + (C_l mod 512)) mod 512 and a_lo = (e_lo + (cxA_l mod 512)) mod 512. The interface state is (carry_e, carry_a, a_lo[6], a_lo[8]): the carries into bit 9 of E16x and A16x, which the completion fixes, and the two low A bits the couplings read. The 512-word table SECOND (index u[8:0]) enforces what lies below bit 9 -- E16x[4]=E15x[4] and fixed E16x bit 7 -- and returns the state; the 32,768-word table FIRST (index u[23:9]) enforces the other ten conditions under it: fixed E bits 9,11,12,17,18,22; A16x[15]!=A15x[15], A16x[23]=A15x[23], A16x[18]!=A16x[6], A16x[8]=A16x[17], A16x[9]!=A16x[20]. The last reads both of its bits off the high field, so the builder tests it as (v>>11^v)&1 rather than as a mask equality; the other four A conditions are one mask equality of that field against a word built from A15x and the state.

For every raw state, enumerate the 32768 high indices using its two carries. Delete states with empty high support before assigning state slots. Raw states can exceed two (maximum four at this split); after pruning at most two remain for each l, and two are used by 22 of the 32 l (10 use one). At bit 32*idx+l, SECOND[lo] records the realized viable state and FIRST[hi] records its accepting indices. For a fixed (lo,l) at most one state exists. Thus T=FIRST[hi]&SECOND[lo] decides exactly the conjunction of all thirteen conditions; neither approximation nor false positive is introduced. The fold
G=(T|(T>>32))&M32 is the original filt(u), bit for bit.

Independent enumeration decides all 2^24 u and all 32 l: zero mismatches,
2048 passing low-24 assignments per l, sum |G|=65536, nonzero G at 63512 u.
FIRST has exactly 2207 nonzero words out of 32768 (0.067352295, against 1513/8192 = 0.184692383 for the 13/11 split of R37P37 and earlier). Consequently E|G|=1/256 and Pr[G!=0]=63512/2^24 as before. No independence between lanes is used.

**Residual equivalence.** Conditional on l in G, all thirteen low-24 conditions of Lemma 6.2 already hold, leaving precisely E16x[30]=0,
A16x[25]=A15x[25], A16x[29]=1. Set VA_l=0x20000000|(A15x&0x02000000), e=u+C_l, A=e+cxA_l and test
`(e&0x40000000)|((A&0x22000000)^VA_l)==0`.
The intermediates need no mod-2^32 masks because all inspected bits are below 32, so discarded carries cannot affect them. This residual test is only called for l in G. Generic checks on rejected lanes compare `(l in G) and residual` with the full definition, retaining the leader's all-survivor/every-sixteenth-lane coverage. Independent exhaustive testing includes every high-byte extension of each low-24 survivor: 16,777,216 cases, zero residual mismatches, and 65,536 full row-16 values per l (2,097,152 total), exactly as inherited.

## 7. The Step-3 probability for the variants (H2)

### 7.1 The quantity

For a good pair (CV1, a0) and l in L*, let F_l be the event that rows 16..36 follow every cell and every printed two-bit condition closing at rows >= 16 (the cell event) and E_l the success event of this filing: rows 16..21 follow every cell and every printed two-bit condition closing at rows 16..21 and the two 37-step outputs are equal (the collision event, Section 7.7; F_l is contained in E_l).
q3c = average over the 599,760 variants of the 170 classes and over l in L* of Pr[F_l | good], the probability over CV1
(Lemma 5.1 gives the exact joint law of all second-block words); q3 = the same average of Pr[E_l | good] = q3c x R, R of Section 7.7.
The expected number of successful (variant, l) per first block is g x 32 x q3.

(For this filing the event F_l is the same except that the eight value bits of rows 18 and 19 of Table 15 are not imposed and neither are E16[23] = 0 and E16[24] = E17[24] (R16x): Sections 7.4b, 7.4c and 7.6. Sections 7.3 and 7.4 describe the estimator and report the registered studies of 7319bba for the Table 15 pattern. The studies of Sections 7.3 to 7.6 estimate q3c; Section 7.7 takes q3 from q3c.)

### 7.2 Lemma 7.1 (what a variant can change)

Rows 16..22 (all their cells and two-bit conditions) are functions of S's rows 12..15, l, and W16..W22, where W16..W21 are functions of (W0..W6, W9..W15) and W22 = s1(W20) + W15 + s0(W7) + W6. By Lemma 5.1 the law of (W16..W22) given goodness is the same for every variant (W8 does not occur). **Hence the probability that rows 16..22 pass is identical for all variants, and equal to its value for the published S.** The variant enters rows 23..36 only through W8, which occurs in W23 = s1(W21) + W16 + s0(W8) + W7 and W24 = s1(W22) + W17 + s0(W9) + W8 (and in later words through them). Its modular differences are fixed (Lemma 4.2 (d)), so only the *values* of W23, W24 move; the conditions of rows 23..36 are the four on W24 (cell `n` at bit 29 and W24[4] != W24[6], W24[22] = W24[31], W24[20] != W24[27]); all other cells of rows 23..36 are `=` and hold automatically once the differences cancel. W24x = Z + W8x with Z = s1(W22x) + W17x + s0(W9x), and Z is (nearly) uniform given rows 16..22, so the four W24 conditions have probability about 2^-4 for every W8.

### 7.3 The estimator (7319bba's design; re-implemented and re-run for this filing, Section 7.4b and Appendix F)

Stages: row 16 exact (the enumeration of 6.2: the stage mean is (1/32) sum_l |R16_l| / 2^32 = 2^-16.994, and the initial particles are drawn exactly from the passing (l, E16) pairs);
rows 17..21: each child proposes E_t^x uniformly with the row's fixed x-bits imposed (exact importance weight 2^-f), sets W_t^x = E_t^x - (the rest of step t), W_t^y = W_t^x + its exact difference, and checks the whole row; row 22: (W6, W7) drawn uniformly from F6 x F7; rows 23..36: W8 of a variant drawn uniformly from the 599,760 variants of the 170 classes of that time (the same row-22 survivor is also evaluated with the published W8 for a paired comparison). NP particles, M children per particle per stage, MT tail proposals per particle, multinomial resampling of the survivors after every stage; the product of the stage means is an unbiased estimator of q3 (the standard SMC normalising-constant estimator). The design is 6c77089c's and 087a18c4's; the program of the registered studies is 7319bba's. **This filing re-estimates q3 with its own program** (Section 7.4b, Appendix F), because it accepts four value patterns of rows 18 and 19: the family of variants, the classes, the filters and every row of the characteristic are those of 7319bba, and this filing changes only how the
good pairs are *found* (Lemmas 8.1, 8.2) and which patterns of rows 16..19 count as a success (Sections 7.4c, 7.6), not which pairs are good or how they are tested. The estimate enters as premise H2.

### 7.4 The registered studies of 7319bba (reported unchanged)

**Study A** (registered 2026-10-10T08:11:18Z, before any listed seed ran): NP = 2048, M = 512, MT = 16384, 32 replicates; rule: the one-sided 99% Student lower bound of the mean of the 32 linear estimates (t = 2.4528, 31 df), q3_model = 2^(floor(100 log2 LB)/100). Result: mean 2^-74.0187, relative standard deviation 0.0743, lower bound 2^-74.0659, q3_model(A) = 2^-74.07. **Study B** (registered after study A had been read, to tighten the spread; same program, NP = 8192): mean 2^-73.9987, relative standard deviation 0.0378, lower bound 2^-74.0225,
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
**Preregistration** (`PREREG_q3R16x.txt`, sha256 18569704b1115d99c138e641986101687836aa408e1f29d670cad354da0691d3, stamp 2026-10-12T16:13:47Z, written before any listed seed ran; reproduced in Appendix G): two independent blocks J1 (seeds 740000..740127) and J2 (seeds 741000..741127) of 128 replicates, NP = 8192, M = 512, MT = 16384; rule fixed in advance: **declared q3 = 2^x, x = floor(100 log2 min(LB_J1, LB_J2)) / 100**, LB the one-sided 99% Student lower bound of the mean of the 128 linear estimates of the block (the spread between replicates carries any overdispersion of the counts within a run). Every listed seed was run and is reported (Appendix G); none was dropped or rerun. Because these offline preregistrations, complete seed ranges, interim progress looks and prior 30-pair screening do not bind an organizer holdout nonce, the premise that they exclude material selection, optional-stopping and multiple-comparison bias beyond the margin to the declared `q3c_used = 2^-71.4162` (Appendix N; the preregistered min-of-blocks bound 2^-71.4629 and block
E’s log-scale 2^-71.4243 are carried as sensitivities) is declared explicitly as part of heuristic H2 (Section 12) and checked at reduced scale on the organizer's holdout seed in `a0-online-r37` (Section 13.2).

**Results.** J1 mean 2^-71.4296, relative sd 0.1096, **bound 2^-71.4629** (one-sided 99% upper bound 2^-71.3970); J2 mean 2^-71.4177, relative sd 0.1143, **bound 2^-71.4524** (one-sided 99% upper bound 2^-71.3838, so q3c <= 2^-71.38 < 2^-70). Rule now applied: **q3c_used = 2^-71.4162**, the one-sided 99% lower bound of the mean of the 16,384 *linear* estimates of block F on this filing's own variant list (Appendix N: seeds 800000..816383, mean(est) 2^-71.41331, relative sd of the linear estimates 0.1095, bound 2^-71.41618, rounded down; no sub-pool transfer allowance, because the measured quantity is the submitted pool's own q3c). Block E's log-scale statistic (mean 2^-71.42132 of the log2 values, sd 0.15870, bound 2^-71.42420) declares 2^-71.4243, which is 0.0087 bit weaker on the same data and is carried as the superseded sensitivity beside its claim 57.58779. The rules of this section remain stated as sensitivities: the pooled 256-replicate bound 2^-71.447381 is 2^-71.4474 (claim 57.61074) and less the 0.0020-bit allowance is 2^-71.4494 (claim 57.64841), the superseded 5x charge 0.0104 gives 2^-71.4578 and claim 57.62108, and the preregistered min-of-blocks rule gives 2^-71.4629 and claim 57.62615. The statistic of this section: the one-sided 99% Student lower bound of the mean of the **pooled** 256 linear estimates -- pooled mean 2^-71.4236, relative sd 0.1118, t(254 df) = 2.3413, i.e. mean x (1 - 2.3413 x 0.1118/16) = 2^-71.447381, rounded down to four decimals of log2 and never up, 2^-71.4474. It is one pre-specified statistic over exactly the seeds the preregistration lists: both blocks were always reported, no seed was added, dropped, replaced or rerun, and no interim look or stopping rule enters it. It is 0.0155 bit tighter than the preregistered min-of-two-block-bounds rule (2^-71.4629, claim 57.62615), which remains stated as the conservative sensitivity, 0.55 bits above the four patterns alone (2^-72.02, Section 7.4b) and 2.56 bits above Table 15 (2^-74.03); the pooled mean is 0.569 bits above the pooled mean of the four-pattern study.
Stage means (log2 averaged over the 256 replicates), rows 16..22 and the tail: 16: -16.000, 17: -12.000, 18: -8.000, 19: -11.430, 20: -7.000, 21: -2.000, 22: -11.003, tail -3.999 (row 16 is -16.000 exactly: 2^21 of 2^37 pairs (u, l)). Of the 2,149,260,669 full passes counted in the tails, 1,438,939,086 (a share of 0.6695) keep E16[23] = 0 and E16[24] = E17[24]; the rest use R16x, including the four l (0, 2, 16, 18) that have no row-16 value under Table 15. These shares are a description of the resampled particles, not a part of the bound.

### 7.5 The examined family of this filing

The registered studies of the parents drew W8 from the 782,800 variants of the 222 classes, and (W6, W7) uniformly from F6 x F7. **This filing examines a sub-family**: the 170 classes of lists 0, 1, 5 and 6 (599,760 variants), and (W6, W7) exactly as before. Every variant of every kept passing class is examined, and given a good pair the variant, W6 and W7 have the laws of the studies
(Lemma 5.1: for every variant a0, W7x is uniform on F7 and W6x uniform on F6 given that the pair is good, independent of each other and of the variant). So q3 = the mean over the 599,760 variants and the 32 elements of L* of the study's conditional probability.
The restriction is **q3-neutral**, not an x-weighting: by Lemma 7.1 the rows 16..22 cells have one probability for every variant, and the rows 23..36 cells depend on the variant only through the four W24 conditions on `W24x = Z + W8x`, with `Z = s1(W22x) + W17x + s0(W9x)`. For every fixed Z the map `W8 -> Z + W8` is a bijection of 2^32, so under the model's own `Z` near-uniformity the conditional probability of the tail is the same for every variant *exactly*, hence the mean over any sub-pool equals the mean over the whole family, and the residual is second order in the non-uniformity of Z (Section 7.8: bounded by the same 0.001 bit by which the study's own measured tail, 2^-3.999 over 782,800 variants, departs from the exact 2^-4). The parents' text prices 0.05 bit for a *weighted* subset (0db0eeb6 Section 7.6); a whole-class uniform restriction introduces no weight, so this filing does not pay that hedge, and instead charges the only *measured* transfer that exists for this quantity: fb039a6e's preregistered 128-replicate study of the same q3 over the whole family G (one-sided 99% bound 2^-74.0088) and over a kept-fibre-weighted pool (2^-73.9984), i.e. **0.0104 bit**, which is 5x the structural bound of Section 7.8 and 5x below the flat hedge.
**q3c_used = 2^-71.4162**, measured directly on the submitted pool by the preregistered study of Appendix N, so no sub-pool transfer allowance is applied (this section is the structural reason the restriction is q3-neutral at all; the measured difference of the two pools' means is 0.0003 bit). Stated sensitivities of the same ledger: the parents'-pool pooled 256-replicate bound 2^-71.4474 is 2^-71.4474 (claim 57.61074) and less the 0.0020-bit allowance is 2^-71.4494 (claim 57.61273), the superseded 5x measured charge 0.0104 gives q3c 2^-71.4578 and claim 57.62108, and the preregistered min-block bound 2^-71.4629 gives claim 57.62615 on this family; four patterns alone 2^-72.02, Section 7.4b; q3 = q3c x 2.482, Section 7.7). For the Table 15 pattern the registered floor of study B is 2^-74.03 (its one-sided 99% bound is 2^-74.0225, its mean 2^-73.9987; study A's bound is 2^-74.0659), and fb039a6e measured the same quantity over the whole family G (a preregistered 128-replicate study: one-sided 99% bound 2^-74.0088) and over a kept-fibre-weighted pool (2^-73.9984);
**Consistency note (disclosed, not silently repaired).** The operative value is `q3c_used = 2^-71.4162` in every place this text assigns a q3c, and it is the constant `Q3_LOG2` that `experiments/lowm.py ledger` executes. A reader of the previous revision found three assignments that still carried the superseded min-of-blocks floor `2^-71.4629` (Sections 7.4c and 12) and one that still carried the superseded 5x measured charge `2^-71.4578` (Section 7.8), plus the historical declaration of Appendix G.2. Each now names the quantity it actually describes; the superseded values appear only as the stated sensitivities of Section 12. No ledger constant, claim digit or certificate changes: `lowm.py ledger` prints `time_log2 = 57.58779` before and after this repair (Appendix N then moves the declaration to block F, whose ledger prints `time_log2 = 57.57975`).

our validation V reproduces the registered study (Section 7.4b). That the dependence on the variant is the four W24 conditions, about 2^-4 for every W8 (Lemma 7.1), is unchanged by the relaxations, which act on rows 16..19 only. Real first blocks (7319bba, Section 13.1, Table 15 cells): the row-16 pass rate of the attack's own good pairs is the exact 1,052,672 / 2^32 (z = +0.88 and +0.51 over 424,363 and 1,693,297 passes); this program's own simulation (Section 13.3) finds row-16 passes at its exact rate under R16x, 2^-11 per probed lane.

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

**Measurement (4ec21bf9, Appendix D.3 and D.3b; the program there is ours).** Ratio of collision events to cell events after row 21, every cell event also a collision event in every run: 2.4648 +- 0.0145 on Table 15 states; on ffbe30bb's states runs of 2^30, 2^31 and 2^31 late proposals give 2.4580, 2.4416 and 2.4674 (the last preregistered) and 2.4552 pooled; 2.46455 under the attack's kept-fibre law of (W7, W8) (preregistered, 64 seeds, 2^32 late proposals: 323,337 collision events against 131,195 cell events). The preregistered rule gives EXQ = min(2.4331, 2.4443) = 2.4331 (the inherited minimum, superseded by Appendix O), below every one-sided 99 percent bound computed from these data, the overdispersion-robust ones included (2.4408 to 2.4520). This filing took EXQ = 2.4331 from that measurement and did not repeat it; Appendix O measures the same ratio on this filing’s own law, declares the value there, and keeps 2.4331 as a stated sensitivity.

**What changes here.** q3 = q3c x EXQ, q3_used = 2^-71.4162 x 2.482 = 2^-70.10470 (1.28 bits more probability per success), and q3 <= 2^-71.38 x 2.4902 = 2^-70.0637 (the uniform-model ratio, above every measured ratio, is the upper value used in H3(b)). The program and the ledger change only in the rare path (Sections 9.9, 10, 11): rows 22..36 are computed in full for every pair that passes row 21 and the output comparison replaces the cell test of those rows; rows 16..21, the cells, the table stages and the cost of everything before the rare path are unchanged.

### 7.8 The family restriction is q3-neutral (new; exact, from the shipped program)

Why a whole-class restriction may be filed against the parents' study at all, and what it can cost. Lemma 7.1 gives the structure: the rows 16..22 cells have one probability phi_l for **every** variant, and the rows 23..36 cells are the four conditions on W24, whose x member is `W24x = Z + W8x` with `Z = s1(W22x) + W17x + s0(W9x)`. Write tau(w) = Pr[tail | variant w] = sum_z mu(z) f(z + w), with f the tail indicator and mu the law of Z given rows 16..22 pass. Then

```text
q3c(pool) = (1/32) sum_l phi_l  x  (1/|pool|) sum_{w in pool} tau(w),
```

so the pool enters only through the mean of tau, and the ratio q3c(S)/q3c(G) does not depend on phi_l, on l or on the l-sum at all. Two consequences, the second of which is the bound this filing charges:

1. **Exact neutrality under the model's own idealisation.** If mu were uniform on 2^32 then for every w the map z -> z + w is a bijection of 2^32, so tau(w) = sum_v f(v)/2^32 is the same number for every variant, and every pool -- 599,760 or 782,800 or one variant -- has exactly that q3c. The variant dimension of the estimator then costs nothing but variance, which is what the 256-replicate spread (relative sd 0.1118) is.
2. **The residual is measured, not assumed.** The deviation of q3c from the uniform-Z value is linear in the deviation of mu from uniform, and the study measures that deviation at the aggregate: the shipped tail stage mean over the fil's 782,800 variants is 2^-3.999 against the exact 2^-4, i.e. 0.001 bit. Two pools' means of a quantity that departs from its neutral value by 0.001 bit can differ by at most 0.002 bit, and the difference of the *measured* pools is smaller than that because the kept 599,760 variants are 76.6 % of the study's own list. **The restriction therefore costs at most 0.001 bit of q3c, and this filing charges 0.0104 bit**, the only preregistered measurement of this reweighting that exists (Section 7.5), i.e. 5x the bound and 5x below the 0.05-bit flat hedge of 0db0eeb6 Section 7.6.
3. **The 0.05 case, for completeness.** At q3c = 2^-71.4474 - 0.05 = 2^-71.4974 the same ledger gives time_log2 = **57.70368**, which is still below the lane's best review (57.89863). Every admissible charge between 0 and 0.05976 bit leaves a lead; the break-even charge is 0.05976 bit, 60x the structural bound.

The three texts that carry this in the program are the family's `LISTID` (170 entries), the constant `C7_CONST = 0xc086800c` and the dynamic-bit set `C7_DYN_BITS` (15 bits: bit 2 of c7 is constant on the four kept lists, so the C7 test is 29 rather than 31 operations), and `Q3_LOG2 = -71.4162`. `experiments/lowm.py selftest` re-derives the family, the variant count and the op counts from the descriptors alone (Appendix D).

## 8. The algorithm

### 8.1 Lemmas 8.1 and 8.2 (the class test, the W6 test and the cube of a list)

Let x = A_{-1}, cb = C6 - A_{-2}, q = A1 ^ x, and for a class with base and mask put

```text
CB3 = cb + (A1 & x) + (base & q),   KZ = K3C + x - (A1 & A2) - (base & FA),   FA = A1 ^ A2,   C4 = 000b362e,   e4 = a0 + C4,   e3 = KZ - (s & FA).
```

**Lemma 8.1.** (a) The class passes the W7 filter at x iff F7(c7 - x). (b) For a0 = base | s of the class, W6x = cb + phi(a0, x) = CB3 + (s & q) - H, mod 2^32, where H_j = e4_j for the bits j with E5_j = 1 and H_j = e3_j for the bits with E5_j = 0 (E5 = e7f2c81f).
Hence a0 is good (W7x in F7 and W6x in F6) iff its class passes and F6(CB3 + (s & q) - H). *Proof.* (a) Section 5.1. (b) W6x = C6 - A_{-2} + MAJ(A1, a0, x) - CH(E5, e4, e3) with e4 = a0 + C4 and e3 = K3C - MAJ(A2, A1, a0) + x (Section 5.1), and CH(E5, e4, e3) selects bit j of e4 where E5_j = 1 and of e3 where E5_j = 0.
MAJ(A1, a0, x) = (a0 & (A1 ^ x)) | (A1 & x) with disjoint bit sets, so MAJ = (a0 & q) + (A1 & x); likewise MAJ(A2, A1, a0) = (a0 & FA) + (A1 & A2). Since a0 = base + s with base & s = 0 (Section 5.3), a0 & m = (base & m) + (s & m) for every mask m.
Collecting the scalar terms gives CB3 and KZ. QED. (Checked on every lane of every pass plane of the experiments and of `selftest`, 0 mismatches.)

**Lemma 8.2 (the cube).** Let b be 0, 2 or 3, and let a0 have bit 1 set if b is 2 or 3. If q_b = 1 then F6(W6x(a0 xor 2^b)) = F6(W6x(a0)) (and W6x(a0 xor 2^b) = W6x(a0) for the bits >= 1); if q_b = 0 then W6x(a0 with bit b set) = W6x(a0 with bit b clear) - 2^b. Hence for a rep t (no cube bit set), Q0 = {b in B : q_b = 0}, cu a submask of Q0 and i a submask of I = B xor Q0: F6(W6x(t xor cu xor i)) = F6(W6x(t) - cu) (mod 2^32), cu read as the integer sum of its bits.
*Proof.* A1 = 62827866, FA = fafd5ca2, C4 = 000b362e, E5 = e7f2c81f: bits 0, 2, 3 of FA are 0, so e3 = KZ - (s & FA) does not depend on s_b; bits 0..4 of E5 are 1, so H_b = e4_b for b = 0, 2, 3 (and e3 is only evaluated from bit 5 upward with carry_5 = 1 because (s & FA)[4:0] <= 16 <= K3C[4:0] = 28). In e4 = a0 + C4: C4_0 = 0, so e4_0 = a0_0 and there is no carry out of bit 0;
for b = 2, 3 with a0_1 = 1 (and C4_1 = C4_2 = C4_3 = 1) the carry out of bit 1 is 1, a0_2 + 1 + 1 gives the sum bit a0_2 and carry 1, a0_3 + 1 + 1 gives the sum bit a0_3 and carry 1, so e4_2 = a0_2, e4_3 = a0_3 and the carry into bit 4 is 1 whatever a0_2, a0_3 are.
Thus s_b enters W6x = CB3 + (s & q) - H at bits >= 1 through (q_b - 1) s_b 2^b, which is 0 if q_b = 1 and -s_b 2^b if q_b = 0; at b = 0, F6 does not read bit 0 of W6x, and when q_0 = 1, s_0 = 1 adds 1 to (s & q)_0 and 1 to H_0 = a0_0, which cancel in W6a - H with zero net carry into bit 1. QED. (Checked on 30,720 tuples in `selftest`.)

*The cube of a list.* The bits in which a list is closed under the flip form its cube B (computed; Section 5.3): B = {0, 2, 3, 7} for the 164 classes of lists 0 and 5, B = {0, 2, 3} for the six classes of lists 1 and 6 (all of which have a0 bit 1 set) and B = {0} for the parents' other six lists. The list is the union over f subset of B of (reps xor f), reps = the members with no cube bit (216, 432, 225, 450 and 1728, 1728, 1728, 1792, 1792, 1792 reps). **The four-bit form (164 classes).** A four-bit list has 216 or 225 reps and 16 variants per rep; the two batches of Section 9.4 are the halves f_7 = 0 and f_7 = 1 of that one rep set, so each batch keeps the three low state bits of Lemma 8.2 and its plane 7 is constant (0 and 1), the second batch's stored planes are the first's with plane 7 set, and `gather` adds D_top[7] = 0x80 on it.
For a first block put I = (q & B) | (CB3 & 1) (the cube bits that do not matter at this x) and Q0 = B xor I. By Lemma 8.2, F6(W6x(t xor f)) = F6(W6x(t) - (f & Q0)) for a rep t and f subset of B, so one test of F6 on W6x(t) - cu decides the 2^|I| members t xor cu xor i, i subset of I: the program computes the sums W6x(t) once (the main run) and obtains the other 2^|Q0| - 1 runs from the stored sums and upper failure planes.
Given that a class passes the W7 test, x mod 16 is uniform: in both affine pieces of the bitwise form of F7 (Section 5.1) the bits w0..w3 of w = c7 - x are individually free (w0 = w28, w1 = w18 (= w29), w2 = w19 tie them to other free bits), so w mod 16 and hence x mod 16 = (c7 - w) mod 16 are uniform; q_0, q_2, q_3 are independent uniform bits before applying the CB3 bit-0 optimization; the executed I law is derived below.

The scalars CB3 and KZ are computed once per passing class; the planes of the reps (14 or 16 bits) are the only lane-dependent data. Both tests are programs on *planes*: a plane is a 256-bit word holding one bit of each of 256 lanes (the lanes of a batch are 256 consecutive reps of a list).

**Executed cube law under H1.** A1[0]=0, so q0=x0. Every one of the 170 c7 constants of the family is even; for w=c7-x modulo 2^32, w0=x0. Both disjoint affine pieces of F7 leave w0 free and pair w28=w0. The first piece has rank six and 2^26 words; the second rank twelve and 2^20 words. Adding constraints on w0,w2,w3 raises each rank by three, so each assignment occurs (2^26+2^20)/8=8,519,680 times and exactly 34,078,720 of 68,157,440 words have w0=0. At fixed w1, subtracting w from c7 is triangular and bijective on bits 0,2,3, even with borrows;
checking all eight assignments for each class confirms the joint cube law. Thus q0,q2,q3 are jointly uniform conditional on a class passing. Under H1, cb=C6-A_{-2} is uniform on Z/(2^32) and independent of x. For each fixed x, CB3=cb+(A1&x)+(base&q) translates cb by a constant;
therefore Pr[CB3=y | x]=2^-32 for every y. This proves that CB3 is uniform and independent of x, hence also of q0,q2,q3 and the class event F7(c7-x). Its bit 0 remains independent uniform after conditioning on
that event. In the executed `I=(q&B)|(CB3&1)`, Q0[0] requires q0=0 and CB3[0]=0, so its probability is exactly 1/4. Q0[2] and Q0[3] remain independent uniform bits. A mask Q0 on a k-bit cube therefore has weight `(1 if Q0&1 else 3)/2^(k+1)`, as in the predecessor's ledger.

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
                            for each of the four lanes: u := U lane; FIRSTw := FIRST[(u >> 9) & 32767]; if FIRSTw != 0: T := FIRSTw & SECOND[u & 511]; if T != 0: G := filt(u)
                                for each l in G: if exact(u, l): recompute W6, W7; rows 16..21 of both members with early abort    (Sections 9.8, 9.9)
                                    if rows 16..21 pass: rows 22..36; if the eight output registers are equal: build m, m'; if digest(m) = digest(m') and m != m': output, halt
    the last group of the first block is padded by repeating its last entry and processed
    V += the counted work of this first block; if V > V_MAX: halt (failure)
halt (failure)
```

The loop is the function `attack(nfb, vmax)` of `experiments/lowm.py` (`python3 lowm.py attack N V`): at most N first blocks, V the counted data-dependent operations of Section 9, halt when V exceeds the cap; an output is verified with the target digest before it is returned.

### 8.3 What is not assumed

No property of x other than being a 32-bit word is used (and, for the cube, that x mod 16 is uniform given that a class passes: Section 8.1), and nothing about the correlation of the classes of one first block: the ledger uses only the exact marginal law of each class test (probability p7 = |F7| / 2^32) and of each variant's F6 test given its class passes (p6 = |F6| / 2^32, exactly, because cb is uniform and independent of x), the law of |I|, and linearity of expectation. Padding lanes (the repeated last entry of a first block's last group) are probed and charged; a duplicated member that hit would be processed twice, which changes the cost (charged) and not the set of pairs found.

## 9. The counted program

### 9.1 Machine and pricing

256-bit word RAM, 64 registers, every executed primitive counted (loads, stores, branches and address additions included). 32-bit values are kept in the low bits; a reduction mod 2^32 is one AND; a 32-bit rotation pattern (S0, S1, s0, s1) costs 8: d = x | (x << 32) (2), three shifts and two XORs and one mask.
A conditional branch tests a register for nonzero and is one primitive. Every address that is not a register value is formed by a counted add (one add per plane or word load; a table read is an index extraction, an add of the table base and a load). The program text is straight-line code. The target compression of a first block is one unit and its internal operations are not counted again.

**Plane algebra.** The plane programs are executed by `lowm.py` on Python integers of 256 bits through a small algebra whose every call is a primitive of the straight-line text: a plane carries a *static constant tag* (all-zero, all-one: a constant of S such as C4, E5, A1 ^ A2) and an *inversion flag* (the stored word is the complement of the true plane).
These are compile-time facts of the text, not data: x ^ 0 = x, x ^ 1 = ~x (flag flips; no primitive), x & 0 = 0, x & 1 = x, x | 1 = 1, x | 0 = x cost nothing; an AND or OR of two planes with equal flags is one primitive (both flagged: De Morgan, the stored words are combined with the dual operation);
an AND or OR of unequal flags costs a NOT first (2 primitives); every other XOR, AND, OR on dynamic planes is one primitive. A full-adder bit is `xy = a ^ b; sum = xy ^ c; carry = a ^ (xy & (a ^ c))`: 5 primitives, 4 without the sum; with a static constant operand bit b: xy = a or ~a (free) and carry = a & c or a | c: 1 primitive.
The counter `CN.n` of the algebra is the count of the plane programs; `process_cv` asserts the counts of the plane programs (W6 and the subtraction runs of each batch of each list, F7 = 112) at every execution (the counts do not depend on the data, only on the batch and the list). The scalar and control steps are counted where they execute by the constants below.

### 9.2 Fixed per first block: FIXED = 490 operations

First block words: 2 random words and the 16 fields (field 0 of a word: and; fields 1..6: shr, and; field 7: shr): 30; control 16 (loop counter add and compare-branch, the cap test, address arithmetic not itemised below): 46. Then:

- **Class test, 275** (the parents' family: 299): -x mod 2^32 (2); the planes of -x, z_j = 0 - ((s >> j) & 1), consumed bit by bit (3 per plane, 2 for plane 0: 95); the dynamic planes of c7 (`C7_DYN_BITS` = bits 4..12, 19, 20 and 25..28, fifteen of them: bit 2 of c7 is `C7_CONST` bit 2 = 1 on all four kept lists, so that plane is a static constant here; 15 loads and 14 address adds: 29); the adder c7 + (-x) with sums for the 17 bits {0, 1, 2, 9, 10, 11, 12, 18, 19, 22, 23, 26, 27, 28, 29, 30, 31} and the F7 test:
  F7 is in the bitwise form of Section 5.1; F7_OPS = 106, measured on this text and split as 83 (the c7 + (-x) add over the fifteen dynamic planes) + 23 (the F7 program); the parents' sixteen-plane c7 measures 112 (89 + 23) when the same `measure_ops` is run with bit 2 restored, so the whole -6 is the family's, not a re-pricing; the mask of the 170 valid lanes (1); the scan of the plane (42 primitives: for each of the three 64-bit parts that hold a lane of the 170 the extraction of the part (1 or 2) and, of its five chunks (four of 13 bits, one of 12), the four that start before lane 170: the extraction (1 or 2) and a zero branch -- ROW_FIX(nl) of Section 9.6 with nl = 170).
- **Scalars and planes, 169:** cb = C6 - A_{-2} (2), q = A1 ^ x (1), A1 & x (1), CB2 = cb + (A1 & x) (2), KXA = K3C - (A1 & A2) + x (2); the 16 planes of q (bits 2, 3, 4, 6, 7, 10, 14, 15, 17..24; bit 0 is not read by any batch because s_0 = 0 on all reps; 48) and their stores (16 stores and 16 address adds: 32);
  `cv_pre` (81 as in 0db0eeb6 Section 9.2: e0b, kap0, C = RBASE + (kap0 - e0b), x12, n12, X, Em2, kap1 and the broadcasts of the constants to four lanes, and the unpacking of the chaining value from the compression output).

### 9.3 Per passing class: 213 + 8 + 5 operations, and per subtraction run

Per set lane of the class plane: table load 1 (the 8192-word `scan_table` is placed at word address `0..8191`, so the nonzero 13-bit chunk `c` is directly its own word address with no base add), chunk offset add 1, c & (c - 1) 2, branch 1: CLS_LANE = 5. Then: five loads of the class descriptor (base, BP = base | ((~S0(base) & M32) << 32), list pointers, batch count, cost word) with their address adds (10);
CB3 = CB2 + (base & q) + C4_MOD (3; folding the constant bits of C4 at E5 = 1 into CB3) and KZ = KXA - (base & FA) (3); the planes of CB3 for the bits 1..31 (93; the W6 programs never read bit 0) and of KZ for the 16 bits {5..9, 11..13, 15..17, 24..28} where s & FA = 0 (48; at the 8 bits {7, 10, 14, 18..22} with s_j = 1 in a batch, e3_j = KZ_j ^ s_j ^ ~borrow_j uses the scalar plane directly), 3 per plane; their stores
(the 47 planes of CB3 and KZ are a fixed set and their 141 formation primitives are per-plane derivations, so the stores are unrolled and each takes a literal displacement in one contiguous scratch area, slot 32k: no address add, 47; the code grows by 94 accesses, inside the declared memory); one work-counter update (1): 10 + 6 + 141 + 47 + 9 = 213 (including the 9 planes of KZ_j at {7, 10, 14, 18..23} formed once in registers). The cube: the mask B of the list (load and address add 2), I = (q & B) | (CB3 & 1) (1), Q0 = B xor I (1), the tests I == 0 and Q0 == 0 (2), and q_0 for bit 0 of W6a - H (2): the itemised base is 8, and the shipped `CF_CLASS = 11` adds one primitive for the run's aggregate work-counter rounding (Section 9.7b) and two for the mixed-class allowance of Section 9.6b (when I != 0, the 2^|I| - 1 <= 7 cube deltas D_top[ii] are also loaded once per class into registers: 5 x 2^|I| - 2 primitives, Section 9.6).
**The main run** (cu = 0) has no extra cost: the cube planes of s are static zeros of the text. **A subtraction run** (a nonzero submask cu of Q0, per batch, in increasing order): the next submask (cu - Q0) & Q0 and its test (3); BP_top xor D_top[cu] with D_top[cu] = (cu | (S0(cu) << 32)) << 192 read from a table of eight words (address 1, load 1, xor 1: 3);
the work-counter update (1): RUN_CU = 7, and the pass plane of F6(W - cu) (Section 9.5).

### 9.4 Sweeps of two batches

A list of r reps is processed in batches of at most 256 lanes (2 for 432 and 450 reps, 7 for 1728 and 1792), two at a time; a four-bit list is the 216- or 225-rep set of Section 8.1 and its two batches are that rep set with plane 7 clear and set (nl = (216, 216) or (225, 225)). A sweep loads the scalar planes it needs once for both batches: zq (the planes of q for the bits s_j of the two batches that are not the static zero: 11 to 15), zKZ (16), zCB3 (31) at fixed slots of that same contiguous scratch area as the unrolled stores, one load each with a literal displacement and no address add, plus 3 of control: 3 + 2 x zq + 47 = 3 + 2 x (11 to 15) + 47, i.e. 72 to 80. Per batch: the stored planes of the reps that are not constant over the batch (with their address adds) and the two pointers of the batch: 2 x (number of such planes) + 2 operations.

### 9.5 The W6 program of one batch and the subtraction runs

Straight-line on planes (Lemma 8.1), with sums produced only for the bits that are used. The cube bits of s (0, 2, 3 or 0) are static zero planes in the main run, so the constants fold. **Constant planes of a batch.** The reps of a list are stored in a fixed order (a bit-lexicographic order of the bits of s, chosen per list; `REP_ORDER` in `lowm.py`, chosen by a seeded search on this ledger and not on the success probability); in a batch of at most 256 consecutive reps some of the 14 or 16 planes of s are all-zero or all-one. Such a plane is a static constant of that batch's text (it is not stored, not loaded and folds in the algebra exactly as the cube planes do), and a W6 text is written for every distinct constant pattern: 8 batches, 24 constant planes in all, 54 distinct texts of 3,851 primitives in all (Section 14.1). The ledger prices the text of each batch of each list separately; `lowm.py` measures it (`ListData.measure`) and asserts the count at every execution.
Structure of the program (for every variant of the 170 classes, a0_1 = a0_5 = a0_11 = 1, a0_12 = a0_13 = 0, and base has 0 at all mask bits and at bits >= 14, so e4 = a0 + C4 decouples into bits 1..4 with carry_5 = 1, bits 5..10 with carry_5 = 1, and bits 14..31 = s[14..31] + C4[14..31] with carry_14 = 0; C4_MOD folds the static bits into CB3):

| step | primitives |
|---|---|
| e4 = s + C4 (carry_1 = C4_1, carry_5 = 1, carry_14 = 0; C4 static: carry = s & c or s \| c), dynamic sums for bits {2..4, 6..10, 14..28} with E5 = 1 | 23 |
| e3 = zKZ - (s & FA) from bit 5 with carry_5 = 1 (FA & mask has 9 bits: 7, 10, 14, 18..23), sums for the 13 bits with E5 = 0 (5..28) | 40 |
| W6a - H = zCB3 + (s & zq) - H merged bit-by-bit (carry-save full adder with half-adder carry reuse (xy & c) \| ac + carry-ripple at bits j >= 1; bit 0 is dead when Q0 = 0), sums for the 20 bits that F6 reads | 124 |
| F6 in the bitwise form of Section 5.1: pass = (w8 ^ w25) & ~fail with polarity-aligned andf/orf (plus upper failure planes and carry chain when Q0 != 0) | 24 |

The measured W6 counts per batch (main run / all sums): k = 3, all sums: 250 to 278 (mean 263.0); k = 3, main: 181 to 208 (mean 193.5); k = 1, all sums: 267 to 301 (mean 282.9); k = 1, main: 188 to 222 (mean 204.1); overall 181 to 301. The pass plane carries no inversion flag in the shipped text; `measure` adds one primitive if it did. A partial batch (fewer than 256 live lanes) costs one more AND with the lane mask; the four-bit lists have two per run.
**The subtraction runs.** Because cu <= 13 < 16, W - cu = (W[31:4] - c4(cu)) || (W[3:0] - cu) where c4(cu) in {0, 1} is the single borrow out of bit 3 (for k = 1, cu = 1 and W_0 = q_0 | ~a0_0 = 1 whenever q_0 = 0, so c4(1) = 0 identically!). Thus when Q0 != 0, the main run precomputes the upper failure plane for c4 = 0 (and c4 = 1 when k = 3) and stores only 15 planes (k = 3: SPILL = 30) or 9 planes (k = 1: SPILL = 18), reloaded once per batch;
for each nonzero submask cu of Q0 the pass plane combines the lower borrow chain on bits 0..3 with the pre-evaluated upper planes using polarity-aligned andf/orf; SUBF per batch: k = 3, cu = 13: 27; k = 3, cu = 12: 26; k = 3, cu = 9: 27; k = 3, cu = 8: 24; k = 3, cu = 5: 28; k = 3, cu = 4: 25; k = 3, cu = 1: 26; k = 1, cu = 1: 11 (primitives by (cube bits, cu)). Exactness: F6(W6x(rep xor cu)) = F6(W6x(rep) - cu) (Lemma 8.2), checked on every lane of every run (Section 13).
**Registers.** The two batches of a sweep are processed together bit by bit, j = 0..31; the loaded planes of bit j are dead after use. Each batch holds the carries (e4, e3, W6a, W) and the F6 operands that are kept for later bits, folded as soon as both operands of a term exist:
the pairs (w1, w12), (w2, w13), (w3, w14), (w14, w18), (w15, w19), (w9, w26), (w10, w27), (w16, w20), (w8, w25) and the three single bits w29, w30, w31; at most ten values at any bit. With at most six temporaries that is at most 20 live planes per batch, 40 for the sweep, plus about eight addresses, counters and constants: below 64, with no spill. A subtraction run holds the 15 or 9 reloaded planes, the borrow and at most six temporaries (under 25 planes); the scan state of its pass plane (about 10 values) is added only after the F6 test has released its operands: below 64.

### 9.6 Scan of the pass plane, the reps and their members

The pass plane (zero in the unused lanes) is scanned in four 64-bit parts of five chunks (four of 13 bits, one of 12); a scan of a plane of nl lanes costs ROW_FIX(nl) = 24.4081 at nl = 256, 20.8133 at 194, 17.9297 at 176, 20.3240 at 216 and 20.1968 at 225, and 42 for the 170-lane class plane. The scan tests each 64-bit row once (1) before its five chunks, so a zero row skips its chunk extraction; ROW_FIX(nl) is that charge at the measured nonzero-row rate of the shipped generator (`reports/receipts/r37-rowtest-80.out`: 2,000 first blocks, 30,430 runs, 73% empty), the row test at 21.5143/18.5067/15.8578 and the chunk base at 2.8941/2.3063/2.0717, added and rounded to four decimals. The 99% is a **block-level** bound, not a binomial one: the 170 class lanes of a first block fire together, so the runs are clustered (design effect 25.6, `r37-scanrate-85.out`), and two independent 2,000-block runs of the shipped generator move the nl = 256 charge by -6.7% (mean 21.1126 against 19.6905, `r37-rowfix4-96.out` and `…-96b.out`), which a binomial bound on 15,215 runs (a 0.84% half-width at the measured 27% nonzero rate) cannot produce: the swing is eight times it. Every ROW_FIX therefore carries the 99th percentile of a 2,000-resample bootstrap over the blocks; the filed 17.9297/20.8133/24.4081 are 1.152-1.159 x the per-run means and 2.8-3.7% above the measured block bounds, i.e. coherent and conservative (`r37-rowfix4-94.out`, `…-96.out`). A cell priced against these keys is charged at the same discipline, a block-level key against a block-level charge and never a binomial key against a filed charge (the like-for-like rule; mixing the two is what produced the -0.01090 that `r37-cube4price3-95` withdrew in favour of -0.00787). The 216/225 keys are the same discipline: block-boot 99% 20.3240 and 20.1968 under seed `cells` against 17.9870 and 19.2328 under seed `cells2`, the larger taken (`r37-rowfix4-96.out`). The plane is masked to nl lanes, so a chunk that starts at or beyond nl is identically zero and is not tested (iter25). Per set lane (a passing rep): table load of the bit index 1 (`scan_table` at word address `0..8191`, so `c` is directly its word address), add of the chunk offset 1, add of the batch word pointer 1, load of the packed word 1, table load of the successor `succ[c] = c & (c - 1)` 1
(`succ_table`, the same zero-base convention: the clear of the lowest set bit is one load, not a subtract and an AND), loop branch 1: SCAN_LANE = 5 (the chunk base is the sixth, charged per nonzero chunk). `succ_table` is 8192 words, the only new resident item (14.1); the scan body is otherwise untouched.
The packed word i of a batch holds in its 64-bit part r the entry s | (S0(s) << 32) of the rep of lane 64 r + i. The entry is extracted directly into the top 64-bit lane (bits 192..255; EXTR = 1, 2, 2, 1 for r = 0..3: `w << 192` for r = 0, `(w << 128) & M_TOP` for r = 1, `(w << 64) & M_TOP` for r = 2, `w & M_TOP` for r = 3) and XOR'ed with BP_top xor D_top[cu] (BP_top in the main run; the result is (a0 | ((~S0(a0) & M32) << 32)) << 192 for the member a0 = base | rep | cu, because S0 is linear and base, rep, cu have disjoint bits, and ~S0(a0) != 0 on all 599,760 variants so every member is nonzero in bits 192..255).
If I = 0 the member is placed by shifting the group register down by 64 (`Gw >> 64` 1), OR'ing with the top-lane entry (1), testing the low 64 bits (`Gw & M64` 1), branching on a full group (1), updating the work counter (1), plus the xor (1): PLACE = 6. If I != 0 the rep stands for m = 2^|I| members: the m - 1 <= 7 cube deltas D_top[ii] are loaded once per class into registers during class preparation (`5 m - 2` primitives in all: loop over nonzero submasks ii of I with `(ii - I) & I` 3, table address 1, load 1 per nonzero ii, plus final test), and each passing rep expands in m placements. **The placement is not walked one member at a time** (that walk is the inherited `EXTR + 5 m + 1` of d9f8833d: 1 xor + 4 shift/or/and/branch per member). The members of one rep are `e ^ D_top[ii]` for the nonzero submasks `ii` of `I`; they are produced consecutively, and every kept list has `k = 3`, so `m` is 8, 4 or 2 and a group of four never mixes two reps for `m = 8` (two full groups) and `m = 4` (one full group), and mixes exactly two for `m = 2`. Because `e` and the `D_top` are 64-bit values laid into disjoint 64-bit lanes and XOR distributes over the shift,

    sum_k (e ^ D_top[ii_k]) << 64k  =  (e | e<<64 | e<<128 | e<<192) ^ sum_k (D_top[ii_k] << 64k)

bit for bit, and the m-1 `D_top` deltas are already in registers from the class preparation above. So a group of four same-rep members costs 2 shifts + 2 ors (one doubling spread) + 1 xor with the precombined delta word + 1 full-group test + 1 store = **8 primitives, not 4 x 5 = 20** (iter49: the m = 1 accumulator's separate shift-down is not executed once the doubling spread writes all four lanes; `experiments/r37-groupfour49.py` assembles 384 group words by both disciplines, bit-identical, checks lane k of the doubling word *is* e ^ D_k, and shows the top-lane convention is the same word) (iter37: the spread is the doubling t = e | e << 64, t | t << 128, four primitives; selftest asserts it on 4,096 words); `reports/experiments/r37-cheaper-placement-23.py` checks the identity on the shipped listings (192 group words, both ways, bit-identical). Charged exactly, with no declared slack: `memcost(0) = 4` (m = 1: shift-down 1, or 1, xor of the class delta 1, work counter 1); `memcost(1) = 6` (iter46/iter53: a pair filling half a group word, priced per *group*: spread pair A 2, xor its precombined delta 1, or into the register 1, shift the accumulator by 128 1, spread pair B 2, xor its delta 1, or into the register 1, work counter 2, store the group word 1 = 12; the opening pair writes a zero register, so its or is not executed and the ledger charges `L.nr * memcost(1) - L.nr // 2`, 5.5 per rep; iter53's census of 582,014 group words on 4,000 first blocks, 187,924 of them filled by exactly two pair reps and one mixed, is the evidence for the pair discipline); `memcost(2) = 7` (iter49: a group of four same-rep members: spread 4, xor with the delta word 1, work counter 1, store 1); `memcost(3) = 9` (iter52: the same body with two words -- the spread is per *rep*, since the `e`-pattern does not depend on the word, so the second word costs an xor and a store, and the counter is per *rep*, as in `memcost(2)`: 4 + (1+1) + (1+1) + 1 = 9; `experiments/r37-groupeight50.py` assembles both words of every m = 8 rep on the shipped listings by both disciplines (128 reps, 256 words, 1,024 lanes, bit-identical)). **This filing removes the completion test and its branch from the four placement disciplines** (6 -> 4, 7 -> 6, 8 -> 7, 11 -> 9): within a class run every rep contributes exactly m = 2^|I| members, m being a property of the class and not of the data, so a group word is completed by a fixed number of placements (4 for m = 1, 2 for m = 2, 1 for m = 4, 1 for m = 8); the only control is the branch that ends the per-set-lane loop, already charged once in SCAN_LANE, and the last partial word of a run is padded by PAD_OPS = 7. The inherited itemisations above charged a test and a branch per placement because they walked members one at a time; R37P22 (this filing) walks them by the fixed schedule of the discipline. Every counting experiment cited above (iter46/49/50/52/53) is unchanged.`5 * 2^(j-1) + 1` beyond. The same identity covers the pair, `sum_k (e ^ D_k) << 64k = (e | e << 64) ^ sum_k (D_k << 64k)`, and `reports/experiments/r37-pair-24.py` checks it on the shipped listings: 4,032 pair words and 96 group-of-four words, bit-identical, and it asserts each of the four charges above item by item. A group of four members is complete after four placements (clearing Gw to 0 after GROUP_BODY); the last group of a first block is padded (PAD_OPS = 7). The `memcost` charge (placement alone, with the pair-run discount of 9.6 and the fold of 9.6b applied) at the four lists is 1,248.491 of `vbar`, split by |I| as 129.326 / 497.407 / 487.458 / 134.300. The 1,671.286 and its [238.755, 696.369, 557.095, 179.066] split that stood here were the pre-R37P22 pricing (charges 6,7,8,12 with no pair-run discount) and do not reproduce on the shipped charge; the "1,079.372 / 910.254" pair of an earlier revision matched no split of this charge at all (`r37-m8count52.py` counts the m = 8 charge on 128 shipped reps).

**9.6b The per-rep work counters fold per group word (this revision).** The counter component of each discipline (1 per placement for m = 1, 2 per pair-group for m = 2, 1 per rep for m = 4 and 8) adds a compile-time constant of the class, and the placements of one group word share the class, so `C + C + C + C` is one add with the quadrupled immediate: m = 1 costs one counter per group word (1/4 per placement), m = 2 one per pair-group (1/2 per rep). `V` is read only at the per-first-block cap test, so the batched value is never observed (the principle of 9.7b). Measured: 66,732 group words over 300 first blocks hold 4 mixed-class words (0.01%), each a 2/2 split at a class boundary, so a run's partial group plus one split cost at most two primitives per class run (`CF_CLASS` 9 -> 11). At `CF_CLASS` 9, 10, 11 (R37P29) and 12 the row is 57.21399, 57.21426, 57.21653 and 57.2825, all below the row they replace (`r37-memberbatch-60.py`, `.out`).

### 9.7 The packed group: GROUP_BODY = 28, first stage 12, continuation six

The packed-u arithmetic was inherited un-itemised as "GROUP_BODY = 31 ... unchanged from aa0e8b6"; it is itemised here under the pricing of Section 9.1, one primitive per line of the shipped `packed_u`:

```text
Sw  = Gw >> 32                              1    shift
E0  = (Gw + bc(e0b)) & LM                   2    add, per-lane mask
mj  = Gw & bc(x12)                          1    and
ch  = (E0 & bc(X)) ^ bc(Em2)                2    and, xor
d   = E0 | (E0 << 32)                       2    the doubling of a rotation pattern
S1E = ((d>>6) ^ (d>>11) ^ (d>>25)) & LM     6    3 shifts, 2 xors, mask
W1  = (KAP + Sw - mj - S1E - ch) & LM       5    4 arithmetic, mask
d1  = W1 | (W1 << 32)                       2    the doubling again
s0W = ((d1>>7) ^ (d1>>18) ^ (W1>>3))        5    3 shifts, 2 xors, mask (9.7e)
U   = E0 + s0W + bc64(C)                    2    two additions
packed-u arithmetic                        28
work-counter update per group (9.10)        0    batched into the per-rep update (9.10, 9.7b)
GROUP_BODY                                 28
```

**9.7b The group's work-counter update is batched (R37P21).** The itemisation charged one primitive per group for the update of 9.10; it is not executed. A group body's contribution to `V` is a class constant times the lanes it completes, so the per-rep update `MEMBER_CHARGE` already charges carries it (the operand changes, not the count), and the run's aggregate rounding is one primitive per class run. Measured on the shipped `process_cv`: a class run's placements are `m x passing reps` (m in {1,2,4,8}) and its group bodies `ceil(placements/4)` -- 24 runs, 864 placements, 216 bodies, every cell exact (`r37-countercollapse-60.out`); `V` is read only at the cap test, so the batched value is never observed. `GROUP_BODY` 32 -> 31 with `CF_CLASS` 8 -> 9.

**9.7c One address mask, not two (R37P23).** The itemisation charged two masks against `U`: bits 9..23 for `FIRST`, the low 9 bits for `SECOND`. Bits 0..23 are one contiguous field and an address extraction costs a shift *and* an AND either way (the shift brings the neighbouring lane's bits down, the AND isolates the lane), so one `& 0xffffff` serves both: `(Um >> 64k + 9) & 32767` for `FIRST` and `(Um >> 64k) & 511` on a hit -- the two primitives each that the probe's 3 per lane and the continuation's 6 per hit already charge.
`GROUP_BODY` 31 -> 30; `U` unchanged and the two addresses reproduce the shipped pair on 12,000 lanes (`r37-laneunmask-61.py`).

**9.7d One address mask was one too many (R37P24).** 9.7c's `Um = U & bc64(0xffffff)` is not executed either: a lane's address is extracted by the shift *and* the AND that follows it, so `(U >> 64k + 9) & 32767` (bits 9..23) and `(U >> 64k) & 511` (bits 0..8) already clear what the word mask was charged to clear, and a shift by zero is no operation (lane 0's first address was `U & 8191` under the 13/11 split). `GROUP_BODY` 30 -> 29, `PROBE` (3,3,3,3) -> (2,3,3,3), 12 -> 11 per group, which the top-first 15/9 split of R37P38 reverses to (3,3,3,3) because a shift by 9 is not a no-operation; 0 mismatches over 175,940 lanes of 43,985 group words from 300 first blocks (`r37-nomask-63.py`).

The same instrument settles the two *lanes-clean* masks, and neither can go. (i) Widening the free guard constant cannot replace the `& LM` on `S1E`: the shifts are 256-bit, so the unmasked `S1E` carries the *next* lane's low bits into its own high half and reaches 0xffffd2d3 there -- a field that no guard fits, since `Sw`'s high half can be zero -- and 7,808 of 12,000 lanes come out wrong at guard 2^26 + 8 (the guard change alone moves no bit). (ii) The `& LM` on `s0W` **is not executed** (9.7e). It is the last operation before `U`, and only a carry out of bit 63 of a lane could reach a read bit (`FIRST[U>>(64k+9) & 32767]`, `SECOND[U>>64k & 511]`, `u = U>>64k & 2^32-1`). With `w` the lane of `W1` and `n` the next lane, the high half the mask would clear is the GF(2)-linear form `H(w,n) = w[7:32] ^ ((n&127)<<25) ^ w[18:32] ^ ((n&262143)<<14) ^ ((n&7)<<29)` (checked against the shipped arithmetic, 20,000 pairs, 0 mismatches); its image over GF(2)^64 has rank 25 and excludes 2^32-1..2^32-4, so `H <= 2^32-5` and `H 2^32 + L <= 2^64 - 2^33 - 3` for `L <= 3(2^32-1)`: no lane carries, bits 0..31 of `U` are unchanged on every input, `GROUP_BODY`
29 -> 28 (`r37-s0wreach-66.out`; `r37-s0wreplay-66.out`: 293,728 lanes over 400 first blocks identical).

### 9.8 Survivors and the residual exact test

After T!=0, the original five-primitive fold and eight-primitive u extraction and mask scan remain SURV_FIX=13. SURV_LANE=6 is unchanged. Only the exact test is reduced to EX_OPS=13: address/load C_l (2), e=u+C_l (1), e&bit30 (1), address/load cxA_l (2), A=e+cxA_l (1), A&0x22000000 (1), address/load VA_l (2), XOR VA_l (1), OR the E and A failures (1), branch (1). Neither addition needs a 32-bit reduction, as proved in Section 6.2. The low-24 table predicate, survivor mask and every rare-path visit are unchanged.

### 9.9 The rare path

A pair with a row-16 pass for some l (probability at most 2^21 / 2^32 = 2^-11 per probed lane): work-counter update and lookup of the member (1 + 2); recompute W6 and W7 (RECOMP = 35); W0..W5 and W8 (201); then for each such l the y-words (8) and rows 16..21 with early abort, each row 106 + 53 + 1 (both members' W 20, CH 3, E 14, MAJ 4, A 12 per word; the cells and two-bit conditions closing at the row at most 53; the work-counter update 1).
When row 21 holds, rows 22..36 are computed with no cell test (106 each) and the pair is accepted iff the eight registers A33..A36, E33..E36 of the two members are equal (the collision event of Section 7.7; both members share CV1, so equal registers are equal outputs): the comparison is 8 xor, 7 or and 1 branch (OUTCMP = 16), and the work counter is updated once for the 15 rows and the comparison (1). `step3b` and `same_out` of `experiments/lowm.py` execute exactly this.
The ledger charges rows 16 and 17 always (c3b_l = 8 + 2 x 160 = 328 per l) and, for every l of every probed lane, with probability 2^-9 (the SMC stage factor of row 17 is 2^-12 under R16x, Section 7.4c): rows 18..21 checked in full and rows 22..36 with the comparison in full, with no early abort, c3b_t = 4 x 160 + 15 x 106 + 16 + 1 = 2,247 (the cell event charged 19 x 160 = 3,040 at the same probability). This is the rare-path charge of 4ec21bf9 (its Appendix D.5: c3b_t = 4 x 160 + 15 x 106 + 16 = 2,246 at probability 2^-11) with the work-counter update added and the 2^-9 of the base kept. The other items are the counts of 0db0eeb6 Section 9.7 and 7319bba.

### 9.10 The work counter V and the cap

V counts every executed data-dependent primitive: each of the following updates it by a constant (one primitive each, counted in the item): a passing class (its fixed price, sweeps, main run and spills), a subtraction run (its F6 test and scan), a member (its placement and, for a rep, its scan and extraction), a group (its body and four probes), a survivor lane, a survivor bit (its exact test) and every row of the rare path.
The per-group update is not a separate primitive here: a group body's charge is a class constant times the lanes it completes, so the per-rep update listed above (inside `MEMBER_CHARGE`) adds it with the same single primitive, and the run's aggregate rounding is the `CF_CLASS` allowance (9.7b). `V` is read only at the per-first-block cap test, so its intermediate value inside a class run is not observed and the batching changes no counted behaviour.
The data-independent part (FIXED) is charged per first block. The cap is tested after every first block (compare and branch, in the control of 9.2). The overshoot past V_MAX is at most the maximal data-dependent work of one first block, vmax_fb = 27454451303603/500 = 54,908,902,607.21 (every class passes with its worst |I|, every rep good, every l surviving, every probe hitting, every l charged through row 36 and the comparison), which the ledger charges.

### 9.11 The seven-lane first-block batch (P8; credited to f1163fcf, 22fc4519 and ffca313a)

The first block of a trial is one target compression and unit. This filing's text computes seven first blocks at once in one 256-bit register: lane i occupies bits 36i..36i+35, the 32-bit word in the low half of the lane and four guard bits above it. Every primitive of that text is counted (`sb_batch`, counter `SB_COUNT` in `experiments/lowm.py`), and `sb_measure()` runs 40 batches of seven at import and asserts the eight chaining words of every one of the 280 lanes against `compress(IV, w)`, the shipped 37-step compression. The count is data-independent (straight-line text) and is asserted to be the same on every batch.

| item | primitives |
|---|---|
| 23 lane masks, reloaded (2 each) | 46 |
| 16 message words packed (RAND, AND, address add, STORE) | 64 |
| IV: eight lane broadcasts (2 each) and the initial b ^ c | 17 |
| schedule: 21 words, each s1 (14) + s0 (14) + three adds + mask + store = 33 | 693 |
| steps: 37 x 52 (t1 = 14 + 3 + 4, t2 = 17 + 3, two adds, K_t and W_t loads, two masks) | 1,924 |
| feed-forward: eight lane adds to the IV | 8 |
| store the eight packed chaining words (2 each) | 16 |
| batch control | 4 |
| eight constant reloads (2 each) | 16 |
| extraction of the seven lanes' eight words (2 each, plus 2 for the hand-off) | 126 |
| **SB_OPS, per seven first blocks** | **2,914** |

The two masks per step are not optional. Every stored word is below 2^32, so one step's intermediates are h + S1 + Ch + (K_t + W_t) < 5 x 2^32, t2 = S0 + Maj < 2 x 2^32, a' = t1 + t2 < 7 x 2^32 and e' = d + t1 < 6 x 2^32, all below 8 x 2^32 < 2^35 < 2^36 = one lane: no lane can carry into its neighbour. The schedule is stored masked for the same reason; the unmasked-schedule variant of this text counts 2,893 and passed 280 random lanes, but its bound is 17 x 2^32 > 2^36, so it is not filed. Rotations are lane-exact because the low mask is lane_mask(0, 32 - n) and the high mask lane_mask(32 - n, 32) of the 36-bit lane, and the lane width is 36 rather than 32 precisely so that the two masks of a rotation cannot be one.

The charge. The batch replaces the compression charge of 9.2 for seven first blocks at once and carries the 30 word-extraction primitives of 9.2 ("First block words"), adding SB_CTL = 4 control primitives:

```text
FIXED_P7 = FIXED - 30 + SB_CTL = 490 - 30 + 4 = 464
SB_FB    = ceil(SB_OPS / 7) = ceil(2,914 / 7) = 417 word operations per first block
per first block: SB_FB/2644 + FIXED_P7/2644 + vbar/2644
               = 0.15772 + 0.17549 + 5.02550 = 5.35870 units   (R37P22: 6.09020; before P8: 6.94232)
```

The ceiling is charged, not dropped (0.71429 word operations per first block are paid for a fractional op). N_FB is unchanged: the batch changes no probability, only the price of the data-independent part, and the last, incomplete batch of seven is charged as a full one by the ceiling. The work cap, the slack and the Bernstein bound are untouched.

## 10. Success probability, independence and caps

Let a *trial* t = (f, a0, l) be a first block f, a variant a0 of a passing class and l in L*, and A_t the event that a0 is good for f, the pair follows every cell and printed two-bit condition of rows 16..21 and the two 37-step outputs are equal (this filing's success event, Section 7.7). The program examines every good pair of every processed first block (Lemma 8.1) and every l whose row 16 holds (Lemma 6.2, exact), so it finds a success iff some A_t occurs before the cap, and every output is verified (Lemma 6.1). Let X_f = sum over the trials of f of 1[A_t] and X = sum_f X_f.

- **Expectation.** E[X_f] = g x 32 x q3 (Lemma 5.1 and Section 7) with g = p7 p6 x 599,760 = 636.680 the expected number of good pairs per first block (exact: each of the 170 classes passes with probability p7 and each of its variants then passes F6 with probability p6), and E[X] = N_FB g 32 q3.
  With q3 >= q3_used = 2^-71.4162 x 2.482 = 2^-70.10470 (H2): E[X] >= mu0 = 0.49466315 (H7) for N_FB = ceil(mu0 / (g 32 q3_used)) = 30,821,562,976,875,433 = 2^54.774789541693, where mu0 is the smallest 8-decimal number strictly above -ln(0.61 - Pcap - 2^-60) / (1 - 2^-10.4), with Pcap = 11/25,000,000 = 4.40e-07 the assumed bound of the work-cap failure probability below (Appendix C).
- **One first block (H3).** By Bonferroni, Pr[X_f >= 1] >= E[X_f] - sum over pairs t < t' of f of Pr[A_t and A_t'] = E[X_f] - (1/2) sum_t Pr[A_t] E[X_f - 1 | A_t]. H3: sum_t Pr[A_t] E[X_f - 1 | A_t] <= delta E[X_f] with delta = 2^-9.4 (trial-averaged conditional expectation), so Pr[X_f >= 1] >= (1 - 2^-10.4) E[X_f].
  H3 splits into (a) the same variant with another l: at most 2^-11 (7319bba measured 0 further successes among 19,620,436 distinct Step-3 successes of its SMC, rule-of-three bound 2^-22.65; the four accepted patterns multiply the chance of passing rows 18 and 19 by about 4 and R16x the chance of the path by about 1.6, with four more l holding row 16, which gives about 2^-19.8, far below 2^-11), and (b) other good pairs of the same first block: summing over all other trials t' = (f, a0', l') of the family uses the family average of Pr[t' succeeds | t' good], which is q3 by definition, so at most rho x N_good x 32 x q3 with rho <= 2^35 (the measured factor at row 16 is 0.98 and 1.00), q3 <= 2^-71.38 x 2.4902 = 2^-70.0637 (H2, Section 7.7) and
  N_good <= 599,760 (all variants of the family, 2^19.58), so (b) <= 2^35 x 2^19.58 x 2^5 x 2^-70.0637 = 2^-10.4837 and delta <= 2^-11 + 2^-10.4837 = 2^-9.7189 < 2^-9.4. (N_good is the number of all variants of the family, as in the earlier filings on this family; no size-biased mean and no per-trial uniformity across (a0, l) is needed.)
- **Many first blocks (H1).** Distinct first blocks have independent chaining values, so the events X_f >= 1 are independent and Pr[X >= 1] >= 1 - exp(-sum_f Pr[X_f >= 1]) >= 1 - exp(-(1 - 2^-10.4) mu0).
- **Work cap.** The data-dependent work v_f of a first block (everything except its compression and its FIXED operations) has mean vbar = 12744.733171973683 (Section 11) and satisfies 0 <= v_f <= vmax_fb = 54,909,039,672.40 (= 857953744881187/15625, one first block's maximal work on the four kept lists; the parents' ten-list family gave 1433437678079/20). The v_f are independent (H1). Put m = N_FB vbar and M = vmax_fb. Then |v_f - vbar| <= M and Var(v_f) <= E[v_f^2] <= M vbar, so Bernstein's inequality for a sum of independent variables bounded by M gives, for t = s m,
  Pr[sum v_f - m >= t] <= exp(-t^2 / (2 (N_FB M vbar + M t / 3))) = Pcap, with slack s = 1/15625: the exponent is 14.65083, so Pcap = 2^-21.13668 = 4.337357e-07 (<= 4.40e-07). V_MAX = ceil((1 + s) N_FB vbar) = 392,837,736,089,609,602,185 is exceeded with probability below Pcap; the run then fails, which is accounted for here. (The earlier filings used Chebyshev's bound vmax_fb / (s^2 N_FB vbar), which forces s = 2^-11 and Pcap = 0.00023325; Bernstein's bound is the standard exponential inequality for independent bounded summands and uses nothing but H1, 0 <= v_f <= vmax_fb and the mean vbar.)
  No part of v_f depends on a conditional law of the scalars: the plane programs cost the same for every data, and the data-dependent items are linear in the numbers of passing classes, good pairs, groups, survivors and hits, whose exact means the ledger uses.
- **Success.** Pr[output a collision] >= 1 - exp(-(1 - 2^-10.4) mu0) - Pcap - 2^-60 = 0.39000000528555046 > 0.39 (the 2^-60 covers a repeated first block among N_FB draws of 512 bits). Any output is a verified collision, independent of the premises.

## 11. Ledger (exact arithmetic; participant ledger executor-checked; Appendix B mirror)

```text
T = A_C + A_S + DEV + N_FB*417/2644 + (N_FB*464 + V_MAX + ceil(vmax_fb) + PRE + FIN)/2644 + 6
A_C=2^48, A_S=2^50, DEV=2^40, PRE=2^38, FIN=1600
N_FB=30821562976875433; vbar=136845530424683277834001/10737418240000000000; vmax_fb=857953744881187/15625
SLACK=1/15625; V_MAX=392837736089609602185
Pcap=4.40E-07 <= 4.40E-07
N=423715539702882534803; T=N/2644 (the Fraction does not reduce); log2(T)=57.15315147653251...
rounded time_log2=57.15316; preprocessing_log2=50.32305
```

The independent Fraction ledger first reproduces aa0e8b6's original N exactly, 773438176907133806360 with its executed law: Q0[0] has probability 1/4 and bits 2,3 each have probability 1/2. Its time_log2 is 58.0213414138426649296682670834074841281671112606650421931692417246587004428, rounded 58.02135. Our delta from that reproduced baseline was written in the previous revision as a closed form in the placement charges of the time; iter37 changed those charges (Section 9.6), so the form is superseded and the shipped `lowm.py ledger`, printed in Appendix B, is the arithmetic of this filing. The cap slack is the interior optimum at this vbar: T(5.806644e-5) = 57.15317, T(1/15625) = 57.15316, T(8e-5) = 57.15318; the exponent is 14.65083. With mu0 = 0.49466315 and N_FB = 30,821,562,976,875,433 the success bound is 0.39000000528555046. No runtime or full-scale success claim is added. The executable participant ledger is statically cross-checked against this independent ledger and Appendix B; its executor diagnostic agrees exactly.

### 11.1 Exactness of the expectations

Each row is linear in a count whose expectation is exact: a class passes with probability p7 (Section 5.3), the number of runs of a passing class is 2^(|B| - j) with j = |I| and the executed mask weights of Section 8.1 (Q0[0] probability 1/4, other cube bits 1/2), a rep of a run is good with probability p6 (Lemma 5.1), a probed lane has exactly 1/256 survivors on average and a nonzero filter with probability exactly 63,512/2^24 (Section 6.2), and 2^21/2^32 row-16 hits (Lemma 5.1: u uniform).
One row is charged at a measured rate instead of its worst case: the number of groups is E[ceil(N / 4)] <= (E N + 3) / 4, and the shipped `process_cv`'s own `pad` counter shows that the residual word almost never executes -- `P mod 4 = {0: 4991, 2: 8, 3: 1}` over 5,000 real first blocks, 17 padded lanes in 9 partial groups (`reports/receipts/r37-cells-64.out`). The ledger therefore charges the one-sided 99% Poisson upper bound on that rate, `PAD_RATE = 117238429/2*10^10` lanes per first block, against both the extra group word (overcharging it fourfold, a group word being four lanes) and the padded body: `groups = pairs/4 + PAD_RATE`, `grp = groups (GROUP_BODY + sum(PROBE)) + PAD_RATE PAD_OPS`. `vmax_fb` keeps the worst case, as a maximum must. The row moves by 40.48 operations per first block (0.00388 bit); no constant, premise, algorithm or family moves.
It is below 0.2% of vbar.

### 11.2 The advice-construction allowances A_S and A_C (H4)

The advice is the 37-step characteristic and its two-bit conditions (Tables 15, 16), the Step-1 solution S and the semi-free-start pair (Table 17); their construction is charged A_S = 2^50 (the paper's Step-1 SAT solve is 2^41.3; completing a Step-1 solution to a 37-step semi-free-start pair takes about 25 milliseconds, organizer experiment `a0-sfs-r37`) and A_C = 2^48 (the unpublished characteristic search, calibrated from the measured complete re-run of the predecessor 35-step search accepted in 6eeefb64: 593,858 solver CPU-seconds = 2^19.18 CPU-seconds at the calibrated price of 2^21.427 units per CPU-second, giving 2^40.61 units; A_C = 2^48 units is 2^26.57 solver CPU-seconds = 3.16 CPU-years, more than 169 times that measured complete re-run, and A_C + A_S + DEV = 2^48 + 2^50 + 2^40 = 2^50.32; sensitivity is reported at A_C = 2^56 -> 58.02723, A_C = 2^60 -> 60.25371, and A_C = 2^64 -> 64.01724).
Everything derived from the advice (G, the classes, the lists, F6, F7, L*, the tables) is recomputed in the preprocessing (PRE = 2^38 operations) or is the 170 class descriptors (below 2^13 bytes of advice).

## 12. Premises

The statistical premises and their empirical support are inherited unchanged. Every row quoted here and in Appendix G is priced on R37P27's ledger and shifts down by 0.06571 bit at this revision's vbar. The sensitivity costs in Sections 11.2 and 12 and Appendix G are recomputed with P4 prices, unchanged predicates, rational 40-bit q3 mantissas and ceil N_FB at that revision's mu0=0.49466812. The primary slack is retained unless increased on the 10^-20 grid to preserve its Bernstein exponent; times round upward to five decimals. Four-pattern and Table 15 sensitivities use their probability floors in the current P4 program, not alternate predicates. Using the J2 bound alone (q3c=2^-71.4524) gives 57.65139 (60.25958 under A_C=2^60); this is a sensitivity, not a replacement for the declared min-block floor.

**H1 (score-critical).** Our theory: the first blocks M0 are fresh uniform 512-bit strings; their chaining values CV1 = F_37(IV, M0) behave as independent uniform 256-bit values; in particular x = A_{-1} is uniform on 2^32 and independent of cb = C6 - A_{-2}, which is uniform on 2^32. Consequences used: each of the 170 classes passes the W7 test with probability p7 = |F7|/2^32 exactly, each variant of a passing class then passes F6 with probability p6 = |F6|/2^32 exactly, and given both, W0..W5 are uniform and independent of (W6, W7) (proof.md Lemma 5.1); hence the expected number of good pairs per first block is g = 599,760 p7 p6 = 636.680, the expected counts of the ledger, and the independence of distinct first blocks.

*Scope.* The expected numbers of passing classes, good pairs, survivors and row-16 passes per first block; the expected operation count of the counted program; the law of the second-block words that defines q3; independence across first blocks (proof.md Section 10). Not the validity of any output: every output is verified with the target. *Evidence.* Measured by 7319bba with the attack's own filters on real first blocks in C (2^21 and 2^23 first blocks: passing classes 7,400,134 and 29,545,568 against the ten-list control's expected 222 p7 2^21 = 7,388,160 and 222 p7 2^23 = 29,552,640 (not this filing's 170 p7); good pairs ratio 1.0034 and 1.0011; row-16 pairs z = +0.88, +0.51), by this filing's simulation of the counted program on 20,000 real first blocks (passing classes per first block 3.457 against the exact 3.523, good pairs 836.3 against 831.0, mean counted operations 28377 against the ledger's 28289), by the unconditional sample in `a0-online-r37` (64 organizer-seeded first blocks per active trial: 90,682 class W7 passes in 25,600 first blocks of our 400-trial run against 90,187 expected), and by the organizer experiment `h1-cv1-filters-nonce`, which counts on 150 organizer-seeded real first blocks per trial how often the W7 filter (first class) and the W6 filter (its first four variants) pass (expected 2.38 and 40.1 per trial; our replays, 100 trials each: 244 and 214 W7 passes against 238.0, 4,011 and 3,988 W6 passes against 4,013.7; Appendix H). These are at most 2^23 real first blocks, not 2^55.8. *Limitations.* Premise (our theory), not a theorem: the filter rates are measured on at most 2^23 real first blocks and on the organizer's small samples, not at the 2^55.8 first blocks of the attack, and independence across first blocks is assumed, not tested. The class tests of one first block are strongly correlated (their c7 values are close), so per-first-block counts are overdispersed; only their expectations and the independence across first blocks are used. The class test uses the single word x, so H1 is also an assumption about that word of the digest of a 37-step compression.

**H2 (score-critical).** For a good pair, q3 = the average over the 599,760 variants of the 170 classes (each equally likely, as examined here) and the 32 elements of L* of Pr[rows 16..21 of both members follow every cell and every printed two-bit condition closing at rows 16..21 (corrected reading A15[29] = A17[29]), the eight value bits E18[1,5,10,11,18,28,29] and E19[29] of Table 15 not imposed, and (R16x) E16[23] = 0 and E16[24] = E17[24] not imposed: exactly the cells and conditions of experiments/lowm.py, and the two 37-step outputs are equal (rows 22..36 are computed without cell tests, Section 7.7)] satisfies q3_used = 2^-71.4162 x 2.482 = 2^-70.10470 <= q3 <= 2^-71.38 x 2.4902 = 2^-70.0637, where q3 = q3c x R: q3c, the probability that rows 16..36 follow every cell, satisfies q3c >= q3c_used = 2^-71.4162 <= q3c <= 2^-71.38. The operative lower bound is block F's alone: the one-sided 99 percent Student lower bound of the **linear** estimates of the 16,384 preregistered replicates (Appendix N), the estimator being unbiased on the linear scale, so the linear mean is the estimator and declaring 2^mean(log2 est) would be the geometric mean, 0.008676 bit lower on the same data. Every earlier bound of this quantity is numerically weaker and is carried here only as a stated conservative sensitivity with its own claim, never as the operative premise: the preregistered min of the two per-block bounds 2^-71.4629 (claim 57.62615; blocks J1 and J2 of 128 replicates each, NP = 8192, one-sided 99 percent upper bounds 2^-71.3970 and 2^-71.3838), block E's log-scale 2^-71.4243 (claim 57.58779) and the pooled parents'-pool bound 2^-71.4474 (claim 57.61074) with its 0.0020-bit allowance 2^-71.4494 (claim 57.64841). The estimator is a sequential Monte-Carlo program written for this filing (Appendices F and G), run on exactly this family with both relaxations as one carrier; and R = Pr[equal outputs | rows 16..21] / Pr[cells of rows 22..36 | rows 16..21] satisfies EXQ = 2.482 <= R <= 1275/512 = 2.4902, where 2.482 is the preregistered one-sided 99 percent lower bound, below every overdispersion-robust bound computed, of the ratio of collision events to cell events after row 21 measured by our 4ec21bf9-f588-4b80-bb2b-77c1ccf8c9b7 (R37R, passed review; its Appendix D.3: 2.4648 +- 0.0145 on Table 15 states, 2.4552 on ffbe30bb's states, 2.46455 under the attack's kept-fibre law of (W7, W8)) and 1275/512 is the uniform-model value of its Appendix D.2; this heuristic explicitly includes the statistical and procedural premise that the participant-reported preregistrations, complete contiguous seed lists (710000..710063, 720000..720127, 721000..721127, 740000..740127, 741000..741127), fixed two-block min(LB) rule, interim progress monitoring during execution, and prior condition-relaxation screening (adopting the four row-18/19 patterns and R16x after screening 30 candidate condition pairs) do not introduce selection, optional-stopping, or multiple-comparison bias exceeding the margin between the two disjoint-seed block estimates, the 6-seed direct full-path check and the declared floors `q3c_used = 2^-71.4162` and EXQ = 2.482 (the preregistered min-of-blocks bound 2^-71.4629 remains a stated sensitivity).

*Scope.* The expected number of successes E[X] = N_FB g 32 q3 and hence N_FB (proof.md Sections 7 and 10), including the validity of the offline SMC estimation protocol, seed selection, stopping rule, and relaxation screening that support `q3c_used = 2^-71.4162`, and the ratio EXQ = 2.482. The good pairs and the later rows are those of 7319bba; this filing changes how the good pairs are found, not which pairs are good, and which pairs count as a success: (from ffbe30bb) the value patterns of rows 18 and 19 and (new) R16x at rows 16 and 17, which also gives the four l = 0, 2, 16, 18 row-16 values, and (from 4ec21bf9) the collision event after row 21 in place of the cells of rows 22..36. *Evidence.* Lemma 7.1: rows 16..22 have exactly the same probability for every variant; a variant enters rows >= 23 only through W8 in W23 and W24, so only the four W24 conditions can depend on it (about 2^-4 for every W8x). Our estimator (exact row 16, exact importance weights at rows 17..21, (W6, W7) uniform on F6 x F7, W8 drawn uniformly from the 599,760 variants; Appendix F) was preregistered (validation V with Table 15 cells: mean 2^-73.9911, bound 2^-74.0064, z = +0.66 against the registered study B of 7319bba, mean 2^-73.9987, bound 2^-74.0225, validation PASSES both preregistered criteria (|z| <= 2.576; bound within 0.04 of -74.0225); main blocks R1 and R2 with the eight value characters of the two E cells removed: means 2^-71.9975 and 2^-71.9868, relative sd 0.0714 and 0.0681, bounds 2^-72.0191 and 2^-72.0074, declared 2^-72.02; stage factors of rows 18, 19 and 21 -8.00, -10.00 and -2.00 bits against -15.00, -6.00 and -1.00 for Table 15, structural gain 2.00) and again with R16x (constants written from the counted program; the same binary reproduces the four-pattern outputs byte for byte; joint blocks J1 and J2: means 2^-71.4296 and 2^-71.4177, relative sd 0.1096 and 0.1143, lower bounds 2^-71.4629 and 2^-71.4524, upper bounds 2^-71.3970 and 2^-71.3838, 0.55 bits above the four patterns alone; our earlier full-path test of R16x with independent rehash of all 30,814 collisions gave +0.590 bit [0.548, 0.631]). In addition, the organizer experiment `a0-sfs-r37` constructs and verifies full 37-step SFS collisions across 128 classes and all 8 pattern branches (63/64 on patterns 0..3 and 57/64 on R16x patterns 4..7 on our seeds `ours-A-0..127`; 13 of 13 returned pairs of trials 0..15 are found by the counted program), and the organizer experiment `h3-ladder-r37` runs the row-16 stage of q3 on organizer seeds: 41 exact row-16 passes among 98,216 W6 passes (4.2e-4, two seed sets) against the 4.9e-4 (2^-11) per probed lane of the ledger (Appendix H). The four-pattern relaxation (exactly four feasible patterns, three verified further collisions) is ffbe30bb's; here the three collisions are re-checked against this package's cells. R16x is ours (each of its two conditions alone is necessary; a sweep of 30 further condition pairs found no further gain). Here the examined law is the studied law (every variant of every passing class, no weighting), so no hedge is added. The collision event after row 21 (Section 7.7): given rows 16..21, the outputs are equal iff E22[29] = 1, s1(W22') - s1(W22) = 0x4fff9f30 and dW26 = 0, with the uniform-model ratio 1275/512 = 2.4902 (4ec21bf9, Appendix D.2); the measured ratio is 2.4648 +- 0.0145 (Table 15 states), 2.4552 (ffbe30bb's states, three runs, the last preregistered) and 2.46455 (the attack's kept-fibre law, preregistered), every cell event also a collision event in every run, and the preregistered rule gives EXQ = min(2.4331, 2.4443) = 2.4331 (the inherited minimum, superseded by Appendix O) (4ec21bf9, Appendices D.3, D.3b). With q3c one bit lower (q3 = 2^-72.4629 x 2.482) the claim would be 58.67775 (60.48509 under A_C = 2^60), with the four patterns alone (q3c = 2^-72.02) 58.26502 (60.37870 under A_C = 2^60), with the Table 15 value 2^-74.03 60.27060 (61.14148 under A_C = 2^60), and with the cell event of rows 22..36 instead of the collision event (EXQ = 1) 58.94181 (60.56559 under A_C = 2^60). *Limitations.* A Monte-Carlo and procedural premise, not a theorem: (1) its coverage rests on the approximate normality of the mean of 128 replicates (relative sd 0.1096 and 0.1143, about twice the Table 15 study's because few children survive the row-19 stage); row-22 survivors are heavily duplicated within a replicate; the row-22 stage draws (W6, W7) uniformly from F6 x F7, which is argued, not measured; depends on the reading of the '+' cells; (2) the offline preregistration timestamps/hashes (`PREREG_q3M.txt`, `PREREG_q3R16x.txt`) and contiguous seed lists (`710000..710063`, `720000..720127`, `721000..721127`, `740000..740127`, `741000..741127`) are participant-reported without an organizer holdout nonce, interim progress looks were taken while blocks ran (Appendices F.2 and G.2), and screening R16x against 30 other condition pairs before running J1 and J2 is not a multiplicity-adjusted holdout test, so the absence of material selection, optional-stopping, or multiple-testing bias is an explicit part of heuristic H2 rather than an externally certified guarantee; (3) no organizer experiment executes the end event of q3: rows 22..36 reach the digest only through a second-block chaining value that must be equal, which needs a reachable first block, that is the attack itself (`a0-sfs-r37` returns semi-free-start pairs and no full collision of the target); the organizer-executed `h3-ladder-r37` runs only the row-16 stage of q3 on organizer seeds; (4) EXQ is a Monte-Carlo bound from the runs of 4ec21bf9, not a theorem: those runs draw (W6, W7) uniformly from F6 x F7 and W8 from the variant list of that filing, on Table 15's and ffbe30bb's row-21 states and, in the preregistered fourth run, a pool of kept fibres of that filing's table; the ratio depends on W8 only through W24 = s1(W22) + W17 + s0(W9) + W8 and was not re-measured on this family's 599,760 variants or on the row-21 states that R16x adds; the runs share resampled row-21 states, so their counts are overdispersed (run 3: chi-square 55.4 on 31 df), which the quasi-binomial and cluster bounds allow for; no organizer experiment estimates the ratio. Premise (our theory): q3 is our computation, with the estimator, the preregistrations and the per-seed estimates printed in Appendices F and G. The count of four patterns is a solver enumeration (Bitwuzla; Z3 on smaller cases) for the published dense part with the signed cells of rows 14 and 15 kept (with rows 12..15 removed as well it admits 128 patterns); other dense parts were not explored, and our estimator does not use the solver. R16x has no solver enumeration: its value rests on the estimator, on `a0-sfs-r37`, and on our full-path test with rehashed collisions; patterns of rows 16..21 outside the program's cells (for example the E18 XOR pattern {24,23,16,15}) are not counted. A stated premise, not an established fact.

**H3 (score-critical).** Averaged over the trials t = (first block, variant, l) of a first block f weighted by their success probabilities, the expected number of other successful trials of the same first block given that t succeeds is at most 2^-9.4: sum_t Pr[A_t] E[X_f - 1 | A_t] <= 2^-9.4 E[X_f]. Equivalently: (a) the expected number of other l in L* succeeding with the same variant is at most 2^-11, and (b) for other good pairs t' of the same first block, Pr[t' succeeds | t succeeds, t' good] <= 2^35 Pr[t' succeeds | t' good].

*Scope.* The per-first-block Bonferroni bound Pr[X_f >= 1] >= (1 - 2^-10.4) E[X_f] (proof.md Section 10). The good pairs of a first block and their dependence structure are those of 7319bba; this filing changes the order in which they are processed, not the set. *Evidence.* (a) 7319bba's replay of 19,620,436 distinct Step-3 successes of the SMC: rebuilding W0..W5 and testing the other 31 elements of L* through rows 14..36 gave 0 further successes (rule-of-three 95 percent bound 2^-22.65 per success; the accepted patterns raise the chance of passing rows 18 and 19 by about 4 and R16x the chance of the whole path by about 1.6, with four more l holding row 16, so about 2^-19.8, far below 2^-11; in that replay the other l fail at row 16 or 17; the collision event changes only rows 22..36, so (a), decided at rows 16 and 17, is unchanged). (b) Summing over all other trials t' = (f, a0', l') in the family uses the family average of Pr[t' succeeds | t' good], which is q3 <= 2^-71.38 x 2.4902 = 2^-70.0637 (H2, Section 7.7; no per-trial uniformity across (a0, l) is required), so the expected number of further successes among other good pairs is at most rho x N_good x 32 x q3 with N_good <= 599,760 (all variants of the family): 2^35 x 2^19.58 x 2^5 x 2^-70.0637 = 2^-10.4837, so delta <= 2^-11 + 2^-10.4837 = 2^-9.7189 < 2^-9.4; the measured factor at the row-16 level over 2^21 and 2^23 real first blocks is 0.98 and 1.00. The organizer experiment `h3-cowpass-nonce` counts the first blocks in which several variants of one class pass F6 together, and `h3-ladder-r37` (Appendix H) counts, on organizer-seeded real first blocks, the pairs of distinct variants of one first block that both pass each level of the attack through the exact row-16 test, against the pairs expected if they passed independently: our replays (two seed sets) give the dependence factor 3.62 and 4.92 at the W6 filter (variants of one class share bits), 0.99 and 1.00 at historical aa0e8b6 LO12 and 0.95 and 0.94 at historical MID12 (P4 public-seed ladder R: W6=3.250842, FIRST13 (lo)=0.995964, SECOND11 (mid)=0.949225, exact row 16=1.048555; N/S/P/C and exact rational calculation are in the P4 executor observations section.), and 1.27 and 0.67 at the exact row-16 test (32 and 9 passes). This is the bound of the earlier filings on this family; the whole family G would give 2^-6.5 and is not used. *Limitations.* Premise (our theory): rows 17..36 are not reachable by any organizer experiment of 20 s; for them rho = 2^35 over the measured factor (0.67 to 1.27 through row 16 on organizer seeds; 0.98 and 1.00 over 2^21 and 2^23 real first blocks) is the stated allowance. Rows >= 17 of distinct good pairs cannot be measured jointly within one first block; the premise leaves a margin of 2^35 over the measured row-16 factor, and the margin over the number of examined pairs is thin (delta <= 2^-9.72 against 2^-9.4). The replay samples are correlated through SMC resampling. A stated premise, not an established fact.

**H4 (supporting).** The published characteristic, its two-bit conditions, the SFS pair's inner values S and L* are used as advice. Their construction is charged A_S = 2^50 (the Step-1 SAT solve, reported by the paper at 2^41.3, and the completion of a Step-1 solution to the SFS pair) and A_C = 2^48 (the unpublished characteristic search, calibrated from the 593,858 solver CPU-seconds of the predecessor search in 6eeefb64); all development computation at DEV = 2^40. The variant family, the 170 class descriptors (below 2^13 bytes), the lists, the filter sets, L* and the tables are recomputed in the preprocessing (2^38 operations bound, itemised in proof.md Section 14.2).

*Scope.* The preprocessing part of the ledger (2^50.32305) and the advice (below 2^13 bytes). *Evidence.* proof.md Section 11.2. A_S: 2^8.7 times the paper's reported Step-1 cost; the completion of a Step-1 solution to a full 37-step semi-free-start pair is reproduced in this package in about 25 milliseconds per pair (organizer experiment a0-sfs-r37). A_C: at the CPU-second price calibrated in the accepted filing 6eeefb64 (2^21.427 units at C = 2644 per solver CPU-second), the 593,858 solver CPU-seconds (= 2^19.18 CPU-seconds) measured for a complete re-run of the predecessor 35-step search equal 2^40.61 units; A_C = 2^48 units is 2^26.57 solver CPU-seconds (3.16 CPU-years), more than 169 times that measured complete re-run, and A_C + A_S + DEV = 2^48 + 2^50 + 2^40 = 2^50.32305. *Limitations.* The 37-step characteristic search time is unpublished; A_C = 2^48 is a calibrated bound > 169 times the accepted measurement of the predecessor search, not a direct measurement of the paper's search. Sensitivity: A_C = 2^56 gives time_log2 = 58.02723, the legacy placeholder A_C = 2^60 gives time_log2 = 60.25371, and A_C = 2^64 gives 64.01724.

**H5 (score-critical).** Under collision-frontier-v5 a word-RAM program of 256-bit primitives in which every executed load, store, logic operation, shift, addition, comparison, branch and jump is one primitive is charged by the primitives it executes. The W7 class test (106 primitives for all 170 classes) and the W6 test of a batch of 256 reps (181 to 301 primitives, and 11 to 28 for each subtraction run) are straight-line plane programs whose counts do not depend on the data, produced by a plane algebra in which static constants fold and complemented planes carry an inversion flag at no cost, and in which a NOT is paid when an AND or OR meets unequal flags; two batches are processed together bit by bit with at most 20 live planes each (64 registers, no spill). The group of four members is 28 primitives (28 packed-u; no word-level address mask is executed and the group counter is batched into the per-rep update, 9.7b/d), the first probe stage 12 per four lanes (bits 9..23 are shifted on every lane) plus six per nonzero FIRST word, the residual exact row-16 test 13, and the zero-base `scan_table` at word address `0..8191` gives `CLS_LANE = 5`, `SCAN_LANE = 5`, `SURV_LANE = 6`, with the scalar and control items of proof.md Section 9. All tables, the code (78,826 inherited bytes plus a 1,024-byte allowance) and the constants occupy 962,826 bytes = 2^19.876916, below 2^20 bytes. The 170 classes are base | s for s in the four kept lists (computed, checked for all 599,760 variants); a list is the union of 2^|B| translates of its reps by the cube B of free bits {0, 2, 3, 7}, {0, 2, 3} or {0}, and F6(W6x) does not depend on a cube bit s_b when q_b = 1 or on s_0 when CB3_0 = 1 (Lemma 8.2: proved from the constants of S and checked), which the program uses to run only the main combination and subtract the constants of the other 2^|Q0| - 1 combinations that matter.

*Scope.* The class-test, W6, scan, gather, group, probe and survivor terms of the ledger (essentially all of the 13287.41 data-dependent operations per first block), the fixed terms, the memory figure and the preprocessing bound (2^38 operations). *Evidence.* The program is experiments/lowm.py (the plane programs assert their counts at every execution; process_cv counts every scalar item where it executes; the realized operation count of every category equals its closed formula on 20,000 simulated first blocks). It is exact against the scalar definitions: every lane of every class-test plane and every pass plane equals the F7 or F6 test of its definition (34,000 and 33,570 lanes in selftest, and every lane of every processed class in a0-online-r37), the sets of good pairs (all members, after the expansion of the reps) equal the brute-force sets, the address u equals W0 + s0(W1) from the step equations, the exact row-16 test equals 7319bba's enumeration of 2,097,152 pairs on all 32 l (Appendix A) and the generic row check on random and near-miss values, and the table stage never rejects a member. *Limitations.* No organizer ruling is cited for the plane algebra (static constants and inversion flags are compile-time facts of the text; the W6 programs have 32 to 84 inversion flips that cost nothing because XORs absorb them and AND/OR of equally flagged planes use De Morgan; pricing every one of them as a NOT would give 57.74433, or 60.27400 under A_C = 2^60) or for the register argument, which is a count of live planes, not a register allocation. The code size is a bound (at most 8192 primitives of at most 8 bytes). Branch pricing follows the earlier filings (a branch on a register is one primitive). The ceiling of the group count and the survivor scan are charged at their worst case (below 0.2 percent of the data-dependent work).

**H7 (supporting).** Two constants, named separately, carry the 0.39 floor. (i) The *requirement*: with the cap assumed at Pcap = 11/25,000,000 = 4.40e-07 (the computed Bernstein bound of this family is 2^-21.13668 = 4.337357e-07, rounded up to the ledger's 1e-30 grid, so the assumption holds), mu_req = -ln(0.61 - Pcap - 2^-60) / (1 - 2^-10.4) = **0.494663141329**, rounded up to eight decimals **0.49466315**; N_FB = ceil(mu_req / (g 32 q3_cell)) then guarantees the *achieved* mean E[X] = N_FB g 32 q3_cell = 210406434388209029952627446634074885007 / 425352958651173079329218259289710264320 = 0.494663150 >= mu_req. (ii) The *bound*: 1 - exp(-(1 - 2^-10.4) mu_req) - Pcap - 2^-60 = 0.39000000528555046 > 0.39 (the shipped ledger prints 0.39000000528555046 in binary double; the two agree to 1e-15). Both constants are printed by the shipped program, `mu_req 0.49466315` and `pcap_log2 -21.13668055304557`. *No other constant is used*: the eight-decimal figure of the parents' ten-list cap (their Pcap <= 4.5e-7) is larger than the requirement here, and it appears nowhere in this package except as this sentence.

*Scope.* N_FB (the cap) in the ledger. *Evidence.* Every allowance is an explicit term of the floor equation: the Bernstein cap-failure bound Pcap (priced in proof.md Section 10 from the exact vmax_fb = 857953744881187/15625 and vbar = 136845530424683277834001/10737418240000000000 of the ledger; the computed bound is 2^-21.13668 = 4.337357e-07, against the assumed 4.40e-07), the repeated-first-block allowance 2^-60, and the H3 dependence discount as the divisor (1 - 2^-10.4). Appendix C computes mu0 and the bound with 60-digit decimals and asserts the bound > 0.39; lowm.py ledger() iterates Pcap and N_FB to a fixed point and asserts the same. *Limitations.* The 0.39 floor is the organizer's success requirement; the equation makes the success arithmetic exact rather than adding slack. The cap bound needs the independence of the first blocks (H1) and the bound vmax_fb on one first block's work; a Chebyshev bound would force the slack 2^-11 and Pcap = 0.00023325 (Section 10).

## 13. Evidence and runs

All runs for this filing on one Windows PC (24 threads) and its WSL Ubuntu: Python standard library (`experiments/lowm.py`), numpy and gcc for Appendix A. At most two processes ran at a time. The programs and numbers that are used as premises (7319bba, fb039a6e, ffbe30bb) are labelled as such; the q3 studies of Section 7.4b were run for this filing with `q3smc.c` (Appendix F, at most two processes at a time).

### 13.1 Quoted from 7319bba (end to end on real first blocks; inherited evidence for H1, H3, H2)

Inherited aa0e8b6 evidence below; not rerun for P4. P4 validation (c) completed; see the separate P4 executor observations section.

C statistics of 7319bba (random M0 from xoshiro256**, CV1 = F_37(IV, M0), the 222 W7 tests of the predecessors' 222-class ten-list family, the scalar W6 test of every variant of every passing class, u and the exact row-16 test for every l, exact checks of sampled pairs):

| run | first blocks | passing classes (expected) | good pairs (expected; ratio) | row-16 pairs (expected; z) | H3 factor: sum R(R-1) / p^2 sum G(G-1), p = 1052672/2^32 |
|---|---|---|---|---|---|
| seed 5eed0021 | 2^21 | 7,400,134 (7,388,160) | 1,748,648,111 (1,742,708,500; 1.00341) | 424,363 (422,895; +0.88) | 0.981 |
| seed 5eed0023 | 2^23 | 29,545,568 (29,552,640) | 6,978,649,557 (6,970,834,000; 1.00112) | 1,693,297 (1,691,580; +0.51) | 0.979 |

The counts are strongly overdispersed (variance-to-mean ratios 28.8 for passing classes, about 23,100 for good pairs, 6.6 for row-16 pairs) because classes are correlated; their means match. 7319bba's replay of 19,620,436 distinct Step-3 successes of the SMC found 0 co-successes across the other 31 elements of L*. These programs are not re-run here; the family and the filters of this filing are theirs.

### 13.2 Exhaustive checks and equivalence with the definitions (this filing)

Inherited aa0e8b6 evidence below; not rerun for P4. P4 validation (c) completed; see the separate P4 executor observations section.

- **F6, F7 and G (inherited).** For all 2^32 words w the definitions of F6 and F7 against their bitwise forms, |F6| = 287,309,824 and |F7| = 68,157,440, 0 mismatches (0db0eeb6, Tungsten; the bitwise forms are those used by the plane programs here, which `selftest` and the experiments compare with the definitions on the lanes below); |G| = 12,103,680.
- **The classes and the lists (`selftest`).** For all 170 classes and all 599,760 variants: the variant base | s is in G, has the class's c7, and the class has its size; 0 mismatches. Maximum S0(a0) over the variants 0xffffbb5c (lane safety of the packed words).
- **The cube (`selftest`).** For 8 classes spread over the lists, 60 random (x, cb) each and 8 random reps each: F6(W6x(rep xor f)) = F6(W6x(rep xor (f & Q0))) for all f subset of the cube B (Lemma 8.2): 30,720 tuples, 0 mismatches; all classes of the lists with bit 2 or 3 in the cube have base bit 1 set.
- **The plane programs (`selftest`).** The W6 program on 33,570 lanes (8 classes spread over the four lists, 3 random (x, cb) each, every batch and every cube combination): 1,462 F6 passes, 0 mismatches against F6(w6of(a0, x, A_{-2})) of the member rep xor f. The class test on 34,000 lanes (200 values of x, half of them constructed to pass a class): 0 mismatches against F7(c7 - x).
- **Row 16 (`selftest`, Appendix A).** The exact test of Lemma 6.2 equals the exhaustive enumeration of `r16.c` on all 32 l (2,097,152 pairs, none missing, none added) and rejects all 1,046,639 non-members among 2^20 random (u, l); filt(u) contains every l of every enumerated pair, and its sums over the 2^24 values of u mod 2^24 are the exact means of the ledger; against the generic row check (`row16_ok`) on random values, on near-miss values (the fixed bits of E16x imposed) and on single-bit changes of members: 0 mismatches; filt(u) contains every l with a row-16 pass.
- **Packed address.** The 4-lane U against the definition u = W0 + s0(W1) of the chaining value and a0 (400 lanes, extreme chaining-value words): 0 mismatches.
- **Unrestricted run of the experiment checks.** The checks of `a0-online-r37` (every lane of the class-test and pass planes, the good sets against brute force, the addresses, the table stage and the exact test against the row-16 definition, the cells of rows -4..15) on 400 first blocks with a passing class (2,590 first blocks drawn, 400 trials of at most 64 draws), **all passing classes** of each processed (9,814 classes, 2,164,111 good pairs, 8,476 survivors of the table stage): 0 mismatches of every kind; the unconditional class sample of the same trials (25,600 first blocks) has 90,682 class W7 passes against 90188 expected.
- **Organizer experiments (local replay of the request format with seeds `ours-A-<t>` and `ours-B-<t>`; each inside the organizer's 20 s and 128 MiB).**
  `a0-sfs-r37`: trial t imposes pattern t mod 8 (0..3: the four value patterns of rows 18 and 19 with E16[23] = 0; 4..7: the four R16x patterns with E16[23] = 1); 120 of the first 128 trials build a 37-step semi-free-start collision with a variant dense part (patterns 0 to 7: 15/16/16/16/14/15/14/14; 63/64 on patterns 0..3 and 57/64 on R16x patterns 4..7; the others exhaust their proposal budget); for the 13 of trials 0..15 that return a pair, the constructed chaining value is fed to the counted online program restricted to the class of a0, which finds exactly the constructed pair in **13 of 13** cases (class test, W6 test, gather, packed address, probe, exact test, rows 16..36); 3.7 s.
  `a0-online-r37` (trials 0..7): unconditional (H1): 512 first blocks (64 per trial), 1,913 class W7 passes against 1,803.75 expected (the class tests of one first block are correlated); selection (H5): 74 first blocks drawn, 24 classes processed, 1,760 good pairs, 2 survivors of the table stage; class-lane, pass-lane, good-set, address, row-16 and cell mismatches: 0, 0, 0, 0, 0, 0 (pairs checked against every cell of rows -4..15 for all 32 elements of L*: 12); 0.7 s. `h1-cv1-filters-nonce`, `h3-cowpass-nonce` (trials 0..99) and `h3-ladder-r37` (trials 0..15): Appendix H; 4.0 s and 1.9 s.

### 13.3 The counted program simulated on real first blocks (premises H1, H5)

Inherited aa0e8b6 evidence below; not rerun for P4. P4 validation (c) completed; see the separate P4 executor observations section.

`experiments/lowm.py`'s `process_cv` was run on 20,000 real first blocks (first words from SHAKE-256 of the seed `simF-1017`, real 37-step compressions, all 222 classes of the predecessors' ten lists, every operation counted), without any restriction of the family. That the run is the *unrestricted* family is not an assumption but a consequence of its own counts, below: 3.457 passing classes per first block is 28 percent above the restricted family's exact expectation 170 p7 = 2.697754, a 30-sigma excess over 20,000 blocks, and it matches the ten-list exact 222 p7 = 3.522949.
Realized counts (**a ten-list control, not this filing's family**: the run takes the predecessors' unrestricted 222 classes and 782,800 variants, so its exact expectations are 222 p7 = 3.522949 and 782,800 p7 p6 = 830.988, closed forms from |F7| = 68,157,440 and |F6| = 287,309,824 (Section 13.2) and not ledger cells of this filing, whose restricted family has 170 p7 = 2.697754 and 599,760 p7 p6 = 636.680): 69,139 passing classes (3.457 per first block against the exact 3.522949), 16,726,799 good pairs (836.3 per first block against the exact 830.988), 4,181,742 groups, 63,548 probed lanes with a nonzero table word, 65,564 survivors of the exact table stage (0.00392 per probed lane against the exact 1/256 = 0.00391), 7,954 first-block-level row-16 passes. **The restricted counterpart is this filing's own measurement.** The same counted program on 6,000 real first blocks of the shipped 170-class setup realizes 2.7500 passing classes per first block against the exact 170 p7 = 2.697754 (ratio 1.0194; `experiments/r37-recount54.py`, 6,000 blocks, all four lists), and the ten-list control above realizes 0.9813 of its own expectation: each is within 2 percent of its own expectation, and neither control is used as the other's expectation anywhere in this package.
The counted operations per first block (the 46 first-block operations included): mean 28377, against the ledger's expectation 28289 (= FIXED + vbar), ratio 1.0031; the run precedes the change of the rare path of Section 9.9, which acts only on pairs whose row 21 holds. The realized operations of every category (class test, scalars, class preparation, sweeps, W6 programs, scans, members, groups, probes, survivors, rare path) are the prices of Section 9 applied to the realized counts (`experiments/lowm.py` is the program; the check is the identity of Section 9's prices with the executed counts).

### 13.4 Development computation

Below 3,000 CPU-seconds in all (the exhaustive row-16 comparison 20 CPU-seconds in C and 60 in numpy, the simulation about 85 CPU-seconds, selftests and experiment replays under 300, aborted runs the rest), far inside DEV = 2^40 units (2^18.6 CPU-seconds at the calibrated 2^21.4 units per CPU-second).

## 14. Memory, preprocessing and advice

### 14.1 Memory

Everything resident during the online phase (`python3 experiments/lowm.py memory`; words of 32 bytes):

| item | bytes |
|---|---|
| planes of the reps that are not constant over their batch (8 batches, 76 planes; the constant planes are in the code) | 2,432 |
| packed entries of the reps: 8 batches x 64 words | 16,384 |
| cube entries D[c]: 8 words | 256 |
| spill area of the sums of a class's batches: 7 x 9 words (or 2 x 15 words) | 2,016 |
| c7 planes: 15 words (the 15 dynamic bits) | 480 |
| chunk table FIRST: 8192 words (32768 entries x 64 bits) | 262,144 |
| chunk table SECOND: 128 words (512 entries x 64 bits) | 4,096 |
| lane-scan table: 8192 words (13-bit chunks) | 262,144 |
| successor table succ[c] = c & (c - 1): 8192 words | 262,144 |
| class descriptors: 170 x 4 words (base, BP, list data, c7) | 21,760 |
| per-l constants: 32 x 4 words (C_l, cxA_l, E15x word, VA_l) | 4,096 |
| scalar planes in memory: 63 words | 2,016 |
| characteristic cells, L* rows, S: bound 1280 words | 40,960 |
| chaining-value constants (cv_pre) and the first-block buffer: 64 words | 2,048 |
| code: the earlier bound of 8192 primitives of at most 8 bytes less the 1,227 primitives of the generic plane programs (55,720), plus the 3,851 primitives of the 54 per-batch plane programs of Section 9.5 at most 6 bytes each (register-to-register 256-bit operations, VEX 4 or 5 bytes) | 78,826 |
| added probe/residual code allowance | 1,024 |
| **total** | **962,826 = 2^19.876916** |

The limit 2^20 = 1,048,576 bytes is not reached. Claimed memory: 2^20.0 bytes (rounded up). The messages (128 bytes), the registers (64 x 32 bytes) and the compression state are included in the last constants. Nonuniform advice: the characteristic, S, L* and the 170 class descriptors (170 x 12 bytes), below 2^13 bytes. The tables are built in the preprocessing and are never held twice. The seven-lane batch of Section 9.11 adds no resident item: its eight state words, sixteen schedule words and seven-lane temporaries are register-resident inside the 64 x 32-byte register file that the last row already counts.

### 14.2 Preprocessing: PRE < 2^38 operations

(i) Discovery of the family: the 2^29 values of E4 with E4[31:29] = 000 (a0 = E4 - C4), each tested against the W8x conditions (about 20 operations) and c7 (about 60), grouped by c7 and the classes of at least 3456 variants kept: 2^29 x 80 + 12.1 x 10^6 x 100 < 2^36; the descriptors (base, mask) of the 170 classes are read off their members (599,760 x 30).
(ii) The four kept lists: 4 x 2^15 subsets x about 80 operations < 2^23.4. (iii) The planes and packed entries: 8 batches x (17 x 256 bit insertions x 3 + 64 x 4 x 10) < 2^17. (iv) FIRST/SECOND: enumerate 512 low indices per l, at most 16 encoded interface states and 32768 high indices per state, then emit/prune at most two viable states. A conservative 100 primitives per tested index, plus 32 x 2 x 32768 x 10 for emission, is below 2^25. Per-l constants: 32 x 200; the scan and successor tables 2 x 8192 x 6; the c7 planes 170 x 32 x 3.
The sum remains below 2^36.1; PRE = 2^38 is charged. Tables are built before lists and scan-table initialization. Reuse the uninitialized scan-table region for at most 2^17 bytes of construction scratch (encoded low states and one-l high supports); release it before online use. No duplicate final tables coexist. Nothing depends on cb or on any other word of the chaining value.

### 14.3 Peak resident memory during construction

The submitted memory figure is the program's resident set (code, tables, messages, working state, retained randomness) together with the retained advice; the *work* of the construction phases is charged in time, and their scratch space is bounded here explicitly, so that no phase of this package needs more than the declared 962,826 bytes at any instant.

* **Family discovery** (14.2(i)). The 2^29 candidates of E4 are streamed and never stored. One
  pass holds a key table of at most 4,096 (c7, mask) entries of 16 bytes = 65,536 bytes, 520 32-bit counters = 2,080 bytes and one candidate register. A pass that exceeds the key bound is repeated over the same stream with a different key partition; four such passes cost 4 x 2^36 = 2^38 = PRE, so the streaming argument stays inside the preprocessing budget already charged. The descriptor read-off streams the kept members against 170 descriptors of 12 bytes = 2,040 bytes. Peak: 67,616 bytes.
* **List, plane and table construction** (14.2(ii)-(iv)). The 2^17 bytes of construction scratch
  are taken from the scan-table region before that table is initialised and released before the online phase; FIRST, SECOND, the scan table and its successor table are then written in place into disjoint regions of the same 962,826 bytes and no final table is ever held twice (14.1). Peak: the final tables plus at most 2^17 bytes.
* **The advice itself** (A_S, A_C). The characteristic, its printed two-bit conditions, the
  Step-1 solution S and the semi-free-start pair are the *published* tables of the cited work (Tables 15-17), used as stored data: 2^13 bytes, inside the figure, and no search is part of the submitted program. Their construction is nevertheless charged in full in time, at A_S = 2^50 and A_C = 2^48 (2^50.32 units together, more than 169 times the measured complete re-run of the predecessor search in 6eeefb64, against the paper's 2^41.3 for its own Step-1 solve). Because the program runs no solver, there is no solver transient space to charge: the
  construction phases this submission *does* run are the family discovery, the list and plane construction and the table build above, and those are inside the bound.

Peak resident memory at any instant is therefore 962,826 bytes = 2^19.876916, below 2^20 bytes.

## 15. Limitations

P4 adds no full attack run or organizer qualification. All five modified experiments and the ledger/memory diagnostic completed twice in the organizer executor; the standalone selftest was not run. The independent host tools run no participant code. Uniform-lane/padding expectations, code bounds, register feasibility, q3 and H1-H7 remain inherited limitations.

- H1, H2, H3 are premises. q3 is estimated (the cell probability q3c by Monte Carlo, with an estimator written for this filing, validated against the registered study of 7319bba, its row-16 stage reproduced on organizer seeds by `h3-ladder-r37`; the ratio EXQ of collision to cell events from the runs of 4ec21bf9, Section 7.7), not proved; because the offline preregistrations, complete seed lists, interim progress monitoring and prior 30-pair screening are participant-reported without an organizer holdout nonce, the absence of material selection, optional-stopping or multiple-testing bias in the offline q3 studies is an explicit part of heuristic H2. No full collision has been found and none is expected at the scale that can be run; the full-scale success probability cannot be observed.
- The counted program is a straight-line text whose plane programs are executed and counted by an algebra with static constants and inversion flags; the scalar and control items are counted by the constants of Section 9. There is no machine code; the register argument of Section 9.5 is a count of live planes.
- The simulation of Section 13.3 samples 20,000 first blocks of the 2^55.76 the run draws; the per-first-block counts are heavy-tailed, so its mean has a standard error of a few percent; the ledger does not use it.
- The organizer experiments run the same program on the whole family of 170 classes; to fit the sandbox a trial processes at most the first three passing classes of its first block.
- H3 (b) is measured at the row-16 level only (7319bba; `h3-ladder-r37` on organizer seeds, Appendix H) and leaves a margin of 2^35 on rho; rows 17..36 are not reachable by any organizer experiment of 20 s; its bound on the number of examined good pairs is the whole family.
- The published characteristic and SFS pair are used as advice under the allowances; the paper's SAT solve and characteristic search were not rerun.
- For 37 steps the measured q3 for the Table 15 pattern is about one bit better than the 75 conditions stated in the paper's text; the paper's own tables give 74, which the SMC matches stage by stage. With the four patterns of rows 18 and 19 accepted the count is 72, in accordance with the structural 2 bits. With q3c one bit lower, 2^-72.4629, time_log2 would be 58.67775 (or 60.48509 under A_C = 2^60).
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

Self-contained (integers and Fractions); the stage prices are the constants of Section 9, asserted by `lowm.py`. It is the exact ledger of **this** filing's four-list family — 170 classes, `FIXED = 490`, `FIXED_P7 = 464`, `SB_FB = 417`, `F7_OPS = 106`, `Q3_LOG2 = -71.4162`, `PAD_RATE = 117238429/2*10^10`, `Pcap <= 11/25,000,000` — and it reproduces `python3 experiments/lowm.py ledger`: `N_FB`, `g`, `vbar`, the cap bound, `V_MAX`, `N` and `time_log2` all agree digit for digit (`reports/experiments/r37-ledgergate-74.py` extracts and runs both). The mirror sums the rational without reducing, so it prints the same integer pair as `T_num / T_den`.

```python
from fractions import Fraction as Fr
# Exact ledger of the counted program (proof.md Sections 9-11). Integers and Fractions only.
C = 2644                                   # reference cost of one target compression, in word operations
# stage prices (primitives of the straight-line text, proof.md Section 9; the plane-program counts are measured by lowm.py and asserted at every execution)
# per-list tables (below): the W6 program of every batch of every list with the constant s planes folded, measured by lowm.py (ListData.measure) and asserted at every execution
F7_OPS, SCAN_LANE, CLS_LANE = 106, 5, 5
def scan_fix(nl):                        # the fixed part of a scan over nl lanes (Section 9.6, the row test)
  return {170: 42, 176: Fr(179297, 10000), 194: Fr(208133, 10000), 216: Fr(10161979, 500000), 225: Fr(20196831, 1000000), 256: Fr(244081, 10000)}[nl]
SCAN_FIX = scan_fix(256)
EXTR, PLACE, GROUP_BODY, PAD_OPS, PROBE = (1, 2, 2, 1), 6, 28, 7, (3, 3, 3, 3)
PAD_RATE = Fr(117238429, 20000000000)   # residual group word: 99% Poisson bound on 17 padded lanes per 5,000 first blocks (Section 11.1)
SURV_FIX, SURV_LANE, EX_OPS, RARE_LOOKUP, RECOMP, ROWCHECK, ROWCOMP, OUTCMP = 13, 6, 13, 2, 35, 53, 106, 16
CPREP, CF_CLASS, SWEEP_OVH, FIXED, RUN_CU, SPILL_K = 213, 11, 127, 490, 7, {3: 30, 1: 18}
ZC_N, KZ_N, NB_N = 31, 16, 0          # broadcast planes of CB3 (bits 1..31) and KZ (16 bits) loaded by every sweep
# the four kept lists of the ten (proof.md Sections 5.3, 9.4, 9.5): cnt classes, n variants, cube bits k, lanes of each batch nl, dynamic s planes of each batch dyn, zq planes loaded by each sweep zq,
# W6 program of each batch (main run / all sums) w6, subtraction runs sub[(batch, cu)]
LISTS = {
  0: {'cnt': 82, 'n': 3456, 'k': 3, 'nl': [216, 216], 'dyn': [9, 9], 'zq': [10], 'w6': [{False: 168, True: 236}, {False: 189, True: 262}], 'sub': [{1: 26, 4: 25, 5: 28, 8: 24, 9: 27, 12: 26, 13: 27}, {1: 26, 4: 24, 5: 27, 8: 23, 9: 27, 12: 25, 13: 26}]},
  1: {'cnt': 3, 'n': 3456, 'k': 3, 'nl': [256, 176], 'dyn': [11, 9], 'zq': [12], 'w6': [{False: 206, True: 275}, {False: 187, True: 256}], 'sub': [{1: 26, 4: 25, 5: 28, 8: 24, 9: 27, 12: 26, 13: 27}, {1: 26, 4: 25, 5: 28, 8: 24, 9: 27, 12: 26, 13: 27}]},
  5: {'cnt': 82, 'n': 3600, 'k': 3, 'nl': [225, 225], 'dyn': [9, 9], 'zq': [10], 'w6': [{False: 170, True: 239}, {False: 191, True: 263}], 'sub': [{1: 26, 4: 25, 5: 28, 8: 24, 9: 27, 12: 26, 13: 27}, {1: 26, 4: 24, 5: 27, 8: 23, 9: 27, 12: 25, 13: 26}]},
  6: {'cnt': 3, 'n': 3600, 'k': 3, 'nl': [256, 194], 'dyn': [11, 9], 'zq': [12], 'w6': [{False: 208, True: 278}, {False: 189, True: 259}], 'sub': [{1: 26, 4: 25, 5: 28, 8: 24, 9: 27, 12: 26, 13: 27}, {1: 26, 4: 25, 5: 28, 8: 24, 9: 27, 12: 26, 13: 27}]},
}
CUBE = {3: 13, 1: 1}                        # the cube bits {0, 2, 3} or {0} as a mask
NCLS = 170; NVAR = sum(L['n'] * L['cnt'] for L in LISTS.values()); NFEAS = 32; SB_FB = 417; FIXED_P7 = 464
P7 = Fr(68157440, 1 << 32); P6 = Fr(287309824, 1 << 32); R16F = Fr(2097152, 1 << 32); MU = Fr(1, 256); PNZ = Fr(63512, 1 << 24)
# calibrated A_C = 2^48 (proof.md Section 10; sensitivity at A_C = 2^56, 2^60, 2^64 in Section 12) and the success-floor constants
A_C, A_S, DEV, PRE, FIN = 1 << 48, 1 << 50, 1 << 40, 1 << 38, 1600
EXQ = Fr(2482, 1000)                           # collision event / cell event after row 21: preregistered 99% lower bound (proof.md Section 7.7; 4ec21bf9 Appendix D.3)
Q3 = Fr(1647939023468, 1 << 112) * EXQ           # q3 = q3_cell x EXQ, q3_cell = 2^-71.4162 rounded down to a 40-bit mantissa (the Fraction below is exact)
MU0 = Fr(49466315, 100000000)                     # smallest 8-decimal number above -ln(0.61 - PCAP_ASSUMED - 2^-60) / (1 - 2^-10.4)  (Appendix C); 0.49466315 at PCAP_ASSUMED = 11/25000000
SLACK = Fr(1, 15625); PCAP_ASSUMED = Fr(11, 25000000)
def subsets(mask): return [s for s in range(16) if s & ~mask == 0]
def lane_costs(nls): return sum(SCAN_LANE + EXTR[L // 64] for nl in nls for L in range(nl))   # scan and extraction of every lane of the batches of reps
MEMBER_CHARGE = (4, 6, 7, 9)       # itemised: pair 7 per rep, i.e. 13 per group of four from two pairs (iter53: 2x(spread 2, xor 1) + or 1 -- the opening pair writes a zero register, so its or is not executed -- + one accumulator shift 1 + counter 2 + test 1 + branch 1 + store 1 = 13), one spread 8 (iter49: no separate shift-down), two groups 11 (iter52: one spread per rep, two xors, two tests, two stores, one counter -- Section 9.6; the iter37 doubling identity t = e | e<<64, d = t | t<<128 replaces the 3+3 direct spread)
def memcost(j): return MEMBER_CHARGE[j] if j < 4 else 5 * (1 << (j - 1)) + 1                                  # members of a rep with |I| = j
def class_det(lid, Q0):
    # operations of a passing class (list lid) with relevant cube bits Q0 that do not depend on which reps are good (2^|Q0| runs)
    L = LISTS[lid]; nb = len(L['nl']); nsw = (nb + 1) // 2; part = sum(1 for x in L['nl'] if x < 256); full = Q0 != 0; j = L['k'] - bin(Q0).count('1')
    sweeps = sum(3 + 2 * L['zq'][sw] + KZ_N + ZC_N + NB_N for sw in range(nsw))
    tot = CPREP + CF_CLASS + (0 if j == 0 else 5 * (1 << j) - 2) + sweeps + sum(2 * L['dyn'][b] + 2 + L['w6'][b][full] + scan_fix(L['nl'][b]) for b in range(nb)) + part
    if full:
        tot += 2 * nb * SPILL_K[L['k']]
        for cu in subsets(Q0):
            if cu: tot += sum(RUN_CU + L['sub'][b][cu] + scan_fix(L['nl'][b]) for b in range(nb)) + part
    return tot
def class_run_cost(lid, Q0):
    # scan, extraction and members of one run if all reps are good (times p6 for the expectation); iter53: a pair run fills nr/2 words and each word's opening pair skips its or
    L = LISTS[lid]; j = L['k'] - bin(Q0).count('1'); nr = sum(L['nl']); f = (Fr(3, 4), Fr(1, 2), 0, 0)[j]
    return lane_costs(L['nl']) + nr * (memcost(j) - f) - (nr // 2 if j == 1 else 0)
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
groups = pairs / 4 + PAD_RATE; lanes = 4 * groups
grp = groups * (GROUP_BODY + sum(PROBE)) + PAD_RATE * PAD_OPS + lanes * 6 * Fr(2207,32768)
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
        ("N_FB x SB_FB (units, first-block batch)", NFB * SB_FB), ("fixed: N_FB x FIXED_P7 (units)", NFB * FIXED_P7), ("V_MAX: data-dependent operations", V_MAX),
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

Decomposition of the shipped ledger of **this** filing: the output of the mirror program above, verbatim, and of `python3 experiments/lowm.py ledger` (the ten cells below are the terms of Sections 11.1 and 11.2 and they sum to `N` exactly):

```text
A_C: characteristic search (units x C)  744,219,838,422,974,464
A_S: Step-1 solve (units x C)           2,976,879,353,691,897,856
DEV: development (units x C)            2,907,108,743,839,744
N_FB x SB_FB (units, first-block batch) 12,852,591,761,357,055,561
fixed: N_FB x FIXED_P7 (units)          14,301,205,221,270,200,912
V_MAX: data-dependent operations        392,837,736,089,609,602,185
overshoot past the cap: vmax_fb         54,909,039,673
PRE: preprocessing                      274,877,906,944
FIN: final verification                 1,600
6 further compressions (units x C)      15,864
N_FB = 30821562976875433, g = 636.6804599761963, vbar = 12744.733171973683, Pcap = 4.337356751854426e-07 <= 4.4e-07
N = 423715539702882534803
certificate: 2^5715315 * 2644^100000 <= N^100000 < 2^5715316 * 2644^100000
time_log2 = 57.15316
```

## Appendix C. The success floor

```python
from decimal import Decimal, getcontext
getcontext().prec = 60
PCAP = Decimal(11) / Decimal(25000000)   # the assumed cap bound PCAP_ASSUMED = 11/25000000: the computed 4.337356752e-07 is below it, and it is the same 11/25000000 the ledger and Appendix B use
EPS = Decimal(2) ** -60                      # a repeated first block among N_FB draws
D = 1 - Decimal(2) ** Decimal('-10.4')       # the H3 discount 1 - 2^-10.4
req = -(Decimal('0.61') - PCAP - EPS).ln() / D                       # the requirement
MU_REQ = Decimal(49466315) / Decimal(10 ** 8)                        # requirement rounded up to eight decimals
MU0 = Decimal(210406434388209029952627446634074885007) / Decimal(425352958651173079329218259289710264320)   # achieved: N_FB g 32 q3_cell x EXQ
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

Output (60-digit decimals; the shipped ledger's binary double prints 0.39000000528555046 for the same quantity):

```text
required 0.494663141328739
req rounded up 0.49466315
achieved mu0 0.494663150000000
success bound 0.39000000528555046
OK
```

## Appendix D. `selftest` output

```text
classes 170, variants 599760 (599,760), mismatches 0
W6_OPS (k, full): {(3, False): 211, (3, True): 281, (1, False): 231, (1, True): 310} SUBF_OPS: {(3, 1): 26, (3, 4): 25, (3, 5): 28, (3, 8): 24, (3, 9): 27, (3, 12): 26, (3, 13): 27, (1, 1): 11} F7_OPS 106 FIXED 490 FIXED_P7 464 SB_OPS 2914 SB_FB 417
spread placed by doubling: 4,096 words in 4 primitives, mismatches 0
F7 sampler violations 0
lists (size, cube bits): [(3456, 3), (3600, 3)]  classes with a cube bit 2 or 3 and base bit 1 clear: 0
invariance of F6(W6x) under the flips of the bits of I: 30720 checks, 0 mismatches
w6 plane lanes 20682, F6 passes 1085, mismatches 0
class-test lanes 34000, mismatches 0
row-16 checks: members seen 27, mismatches 0
packed u lanes 400, mismatches 0
max S0 over the 599,760 variants 0xffffbb5c True
```

The w6 lane count is 20,682 against 36,594: `selftest` indexes `reps[256 b + L]`, defined only for b = 0 on a 216/225-rep list; batch 1 is checked in the a0-online-r37 run (0 pass-lane mismatches) and on 48 real class hits (`r37-cube4machine-72.py`).

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
    tx, ty = lw.trace(cv, mx), lw.trace(cv, my) return all(lw.row_ok(tx, ty, i, i not in (6, 7)) for i in range(-4, lw.R)) and all(lw.x2_ok(tx, r) for r in range(8, lw.R))
print('%-28s %-9s %-24s %-24s' % ('pair (x = M\', y = M)', 'collides', 'cells of this lowm.py', 'cells of Table 15')) for k, (cv, my, mx) in PAIRS.items():
    c = new.compress(cv, mx) == new.compress(cv, my) and mx != my print('%-28s %-9s %-24s %-24s' % (k, c, cells(new, cv, mx, my), cells(old, cv, mx, my)))
```

## Appendix G. The joint study of the four patterns and R16x: preregistration, results

Files in `q3/` (`q3smc.c` as listed in F.4, `q3consts_r16x.h` written by `gen_consts.py` from `experiments/lowm.py` as filed, sha256 aa4356605422aa4eb070efe67e1938f071fd17e9ed60a7a5266199a62bbc6b9b; `variants.bin` unchanged; outputs in `studyX/out/`). Build: `gcc -O2 -DCONSTS='"q3consts_r16x.h"' q3smc.c -lm -o q3smc_r16x`; run: `q3smc_r16x SEED 1 8192 512 16384`.

### G.1 Preregistration (written before any listed seed ran; stamp 2026-10-12T16:13:47Z, sha256 18569704b1115d99c138e641986101687836aa408e1f29d670cad354da0691d3)

```text
preregistration: our own sequential-Monte-Carlo estimate of q3 for the 170-class A0-variant attack on 37-step SHA-256 (R37M family) with the four row-18/19 value patterns AND the R16x relaxation accepted JOINTLY (one carrier) written before any listed seed was run; the stamp is the line below.
stamp: 2026-10-12T16:13:47Z program: q3smc.c (ours; the filed R37M estimator plus a TAG line that draws no random numbers), sha256 f0e3efc8d06c58c03c7dd7fe86ef08d8d00b8868202e6c49557f85c479c61f9c.
constants: q3consts_r16x.h (sha256 aa4356605422aa4eb070efe67e1938f071fd17e9ed60a7a5266199a62bbc6b9b), written by gen_consts.py (sha256 14ea0015f43b1ea86109ccc78e86cf392c12a9a34c7ece6a1c3babc1be6b4ae7) from this package's lowm.py in the state `sha256` 9bede229cafc262027b06f91fcdde88a5778d36c4ad59e4083cc4780d8e69b7b (the 57.84086 filing); the shipped `experiments/lowm.py` is `sha256` 9be6b24ca0368de4c48b880796222946734b61de4a26404343346815f605bb52 (the state 7905c31e2ac3a9c513d75d793bf62935c6a73d62e371802a10c0a4a1ff976104 is the 57.64841 filing's and 1d59a12557b7621028c84b511d5d460f0e3effb8e45faecf19a1fce62c1ff9a3 is its predecessor's), and the revisions between them (`eb6e0065...`, `dfb848ed...`, `1d59a125...`, `f2e38973...`, `8426380c...`, which changes only comment and docstring text and `MEMBER_CHARGE[1]` 8 -> 7, and the 57.60210 filing's `782bf3fb...`, which changes only `MEMBER_CHARGE[2]` 9 -> 8, and this one, `9be6b24c...`, which changes only the pair run's charge to 13 per group word (13 = 14 - 1, Section 9.6) modify only `MEMBER_CHARGE`, `GROUP_BODY` and `scan_fix`, none of which enters this file's output. The previous package printed 5107f3f7..., the hash of an earlier lowm.py, corrected here). the carrier = R37M's relaxed cells (rows 18/19 eight value bits free) with three further changes, all in lowm.py's characteristic: CHE[16] bit 23 '0' -> '=' (E16[23] free), CHE[17] bit 24 '+' -> '=' and the two-bit condition E16[24]=E17[24] removed. The R16x parity E16[23]^E19[29]^E18[1]^E18[5]=0 and the other row-18 linear relations are NOT imposed (weaker carrier; any pass through row 36 is still a full collision: rows 22..36 cells unchanged, zero output difference).
variant list: variants.bin (sha256 6900f64cec67217eb352fd43cd0552c92b2514b892481c95f761d19619d1e3c5), unchanged from R37M. known answer (run before this stamp, disclosed): the new binary built with q3consts_relaxed.h reproduces byte-identically the filed R37M study outputs of seeds 720000 and 721000 (RESULT and STAGES lines). Smoke: seed 1 with q3consts_r16x.h (stage 16 = 2,097,152 pairs, 65,536 per l for all 32 l; log2est -71.63000). Seed 1 is not used below.
main study (binary q3smc_r16x), two independent blocks: J1 seeds 740000..740127 (128 replicates), J2 seeds 741000..741127 (128 replicates); NP = 8192, M = 512, MT = 16384 for every replicate. bound: per block LB = mean - t(0.99, 127 df) sd / sqrt(128) over the replicate linear estimates (the replicate spread carries any overdispersion of the within-run counts).
rule (fixed in advance): declared q3 = 2^x with x = floor(100 log2(min(LB_J1, LB_J2))) / 100. Gain over the filed R37M q3 2^-72.02 = x + 72.02 (bits). descriptive only: pooled mean; per-replicate TAG share (full passes whose member x keeps E16[23]=0 and E16[24]=E17[24]); comparison with r16_settle +0.590 [0.548, 0.631].
every listed seed is run and reported; none dropped or rerun except a crash not caused by the program. At most 2 processes at once; wait while load > 35.
```

The program hash named in the preregistration is that of `lowm.py` when the constants were written; the later edits of the program (the row-16 constants of the ledger, `FEASIBLE_L`, q3, and the unconditional first-block W7 sample in `online_trial`) do not touch the cells, and regenerating the constants from the program as filed gives the same file (sha256 above).

### G.2 Results

Rule applied: J1's bound is 2^-71.46286 (lower bound 2^-71.4629, upper bound 2^-71.3970) and J2's is 2^-71.4524 (upper bound 2^-71.3838); the preregistered two-decimal rule gives 2^-71.47 (claim 57.63320, Section 11) and the preregistered min-of-blocks rule gives 2^-71.4629 (claim 57.62615 on this family). The filing that first ran this study declared instead, as a **superseded historical statement**, the pooled bound over the same 256 preregistered replicates, **q3c = 2^-71.4474** (Section 7.4c), 0.0155 bit tighter than the min-of-blocks rule and using no seed outside the two listed blocks. The direct submitted-pool study of Appendix G.3 supersedes it and is 0.0119 bit tighter still. The declared q3c of this filing is 2^-71.4243 (Appendix G.3), and both the pooled 2^-71.4474 and the two-block 2^-71.4629 survive only as the stated sensitivities of Section 12 (and q3c <= 2^-71.38 < 2^-70; q3 = q3c x 2.482, Section 7.7). pooled 256 replicates: mean 2^-71.4236, relative sd 0.1118, bound 2^-71.4474 (superseded declaration, Section 7.4c). Stage means (log2): 16: -16.000, 17: -12.000, 18: -8.000, 19: -11.430, 20: -7.000, 21: -2.000, 22: -11.003, tail -3.999. TAG: 1,438,939,086 of 2,149,260,669 full passes keep E16[23] = 0 and E16[24] = E17[24] (share 0.6695).

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
RESULT seed 740000 NP 8192 M 512 MT 16384 log2est -71.64139 est 2.7151355317e-22 TAG seed 740000 full passes 8247250, of which with E16[23]=0 and E16[24]=E17[24] (member x): 5723505
STAGES -16.00000 -12.00196 -8.00105 -11.57374 -7.00012 -2.05054 -10.98947 tail -4.02452  (row-24 survivors 8247250 of 134217728, full passes 8247250)
--- seed 741000 ---
RESULT seed 741000 NP 8192 M 512 MT 16384 log2est -71.38558 est 3.2419013954e-22 TAG seed 741000 full passes 8731984, of which with E16[23]=0 and E16[24]=E17[24] (member x): 6561999
STAGES -16.00000 -11.99869 -8.00174 -11.38529 -6.99964 -2.01665 -11.04145 tail -3.94212  (row-24 survivors 8731984 of 134217728, full passes 8731984)
```

### G.3 A direct study of q3c on the submitted pool (preregistration; stamp 2026-10-18T07:09:03Z, written before any listed seed ran)

**What this is.** The organizer review of this candidate's own score-bearing submission (e13f9dae, run 39104072013) raises two objections that no rewrite of the earlier studies can answer: F-COST-02/F-CRYPT-02, that an aggregate tail mean within 0.001 bit of uniform does not bound a *sub-pool* mean, and F-EXP-02, that the pooled 256-replicate statistic was adopted after the preregistered rule had fixed the minimum of two per-block bounds. This study answers both at once. W8 is drawn from the **submitted** variant list, so nothing is transferred from the parents' family; and the statistic below is fixed before the seeds run.

**Inputs, regenerated from the shipped files, with the hashes of the states used.**

```text
lowm.py         7905c31e2ac3a9c513d75d793bf62935c6a73d62e371802a10c0a4a1ff976104   (the state of the 57.64841 filing, commit 2d0a13b; the shipped file of this filing is 06a5bf19) q3smc.c         f0e3efc8d06c58c03c7dd7fe86ef08d8d00b8868202e6c49557f85c479c61f9c   (Appendix F.4 as shipped)
gen_consts.py   721d7949d1038a6f01e8cac62eaa8ecc9362a7af105176ab56c82beef90efd5b   (Appendix F.5 as shipped) variants.bin    b767171018fb5ba2d43e55adea23b72de820d9a43ffaa780f51f8c99ae695cbd   599,760 words = 2,399,040 bytes
q3consts_orig.h efd62db9220a667258d8dbde25ec572e1104460f2a1971894292870c6ec7e4cb   (written by that gen_consts.py from that lowm.py) build           gcc -O2 -DCONSTS='"q3consts_orig.h"' q3smc.c -lm -o q3smc_orig
```

`variants.bin` is the W8x of the 599,760 variants of the 170 classes of lists 0, 1, 5 and 6, all distinct, printed by the generator (`variants 599760 distinct W8x 599760`). Every replicate uses NP = 8192, M = 512, MT = 16384, the parameters of every replicate of studies A, B, J1 and J2.

The shipped `experiments/lowm.py` (sha256 9be6b24ca0368de4c48b880796222946734b61de4a26404343346815f605bb52) differs from the state hashed above in `Q3_LOG2`, which this study produces rather than consumes, and in the itemisation-only lines of Sections 9.6 and 14.1 (the scan charge and the successor-table row), from which no constant of `q3consts_r16x.h` is computed. The generator reads only `CELLS`, `X2`, `setup_l`, `MX`, `MY`, `lstar`, `LISTID` and `CLASSES`, none of which that constant touches: regenerating from the shipped file reproduces `variants.bin` b7671710 and `q3consts_orig.h` efd62db9 unchanged (checked).

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

Run 2026-10-18T07:14Z..07:20Z (32 shards of 32 seeds, `q3smc seed0 32 8192 512 16384`), no seed dropped, replaced or rerun. Mean **-71.42391**, sd **0.15878** (relative sd of the linear estimates 0.1101), t(0.99, 1023) = 2.3300, one-sided 99% lower bound **-71.43547**, declared (rounded down) **2^-71.4355**. That declaration was this line's operative value before block F; it is superseded here and every site that still quotes it does so as a stated sensitivity (claim 57.58779 on block E's log scale, 57.70485 on this one). Shipped program, run 39104072013's follow-up: `experiments/r37-q3d-28.py`.

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

The measurement answers both objections it was written for. (i) There is no transfer: W8 is drawn from the submitted 599,760-word list, and the mean agrees with the parents'-pool study of Section 7.4c (-71.4236, 256 replicates, a 782,800-word list) to 0.0003 bit, which is 1/37 of one standard error of that study's mean -- the sub-pool restriction is q3-neutral in measurement as well as by Lemma 7.1. (ii) There is no post-hoc statistic: the rule, the seed list and the arithmetic of the rounding were committed in Appendix G.3 before the first listed seed ran.

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

**a0-sfs-r37**: P4 participant observations: 121 returned pairs and checks_passed=121; detected_by_counted_program=16 for all 16 returned trials 0..15. Organizer checked all 256 trial records (118 returned pairs), with 0 full-target collisions; SFS validity remains an internal participant check. Runtime 7.65/7.48 s versus 20 s.

**a0-online-r37**: P4 participant observations: 512 unconditional first blocks, 2070 class passes; 52 selected first blocks, 24 processed classes, 7152 good pairs, 25 survivors. class_lane_mismatches, pass_lane_mismatches, goodset_mismatches, address_mismatches, row16_mismatches and cell_mismatches each total 0. Five returned pairs, 0 organizer full-target collisions. Runtime 1.92/1.93 s versus 20 s.

**h1-cv1-filters-nonce**: P4 participant observations over 15000 blocks: W7=275, W6=3993, coW6=1267, w7_and_w6=22, w7_w6_pairs=60. No returned pairs. Runtime 6.75/6.35 s versus 20 s.

**h3-cowpass-nonce**: P4 participant observations over 15000 blocks: W7=247, W6=4036, coW6=1264, w7_and_w6=27, w7_w6_pairs=82. No returned pairs. Runtime 6.70/6.54 s versus 20 s.

**h3-ladder-r37**: P4 public-seed ladder R: W6=3.250842, FIRST13 (lo)=0.995964, SECOND11 (mid)=0.949225, exact row 16=1.048555; N/S/P/C and exact rational calculation are in the P4 executor observations section. FIRST pass rate 15131/81608=0.185410744045 versus 1513/8192=0.1846923828125 under the uniform-address model; SECOND conditional rate 307/15131=0.020289471945 versus the uniform-address reference 63512/(1513*2048)=467/22784=0.020496839888. There are 37 row-16 passes among 81608 W6 passes. Eight returned generic 4-bit witnesses pass the organizer mask event; they are not full collisions. Runtime 4.37/4.19 s versus 20 s.

| Level | N | S | P | C | E = C (S/N)^2 | R = P/E |
|---|---:|---:|---:|---:|---:|---:|
| W6 | 839,808 | 81,608 | 171,761,468 | 5,595,314,112 | 52835999.384947248 | 3.250841661 |
| FIRST13 (lo) | 81,608 | 15,131 | 5,880,837 | 171,761,468 | 5904668.720325760 | 0.995963919 |
| SECOND11 (mid) | 15,131 | 307 | 2,298 | 5,880,837 | 2420.921071884 | 0.949225494 |
| Exact row 16 | 307 | 37 | 35 | 2,298 | 33.379261318 | 1.048555259 |

N and C at each level are the preceding level's S and P; the W6 base is w6_cand and w6_candpairs. R is computed from summed counters, not averaged per-trial ratios; deterministic reruns are not counted as additional samples. Historical aa0e8b6 LO12/MID12 values in Appendix H remain historical.

The repeated participant ledger/memory diagnostic of R37P30 (the 13/11 tables) agrees exactly with the independent values of that revision: N=440444759662825425482, denominator 2644, time_log2=57.20902, N_FB=30821872648554019, V_MAX=409566683228803792559, vbar=142672493712975074674833/10737418240000000000, vmax_fb=3431806606977873/62500, and memory=1,024,266 bytes (that revision's, not this one's). FIRST/SECOND table SHA-256 of those tables: 069c55469f6a9af5a5cd33855fd13c281cd58aceec0b444fd0793806bd6d6292. Diagnostic runtime 4.03/4.31 s versus 20 s. All runs used 128 MiB / one CPU.

Provenance: executor report SHA-256 8fb29212d809996302ac123534826941415e1e109590aaac184fbf96a6dc134d. It binds the pre-Round-4 package/manifest text and executed source SHA-256 4d1449598e4eccec6961ac1f61d1718767a442fe48ea2bb3a7d714cc428c9ce0. Round 4 changes evidence text only; the participant source is byte-identical. The report is not a binding of the final edited manifest. Returned-pair event checks are organizer-recomputed; internal observations and diagnostic resource numbers are not independently established attack costs or success probabilities.
The public seed provides no holdout protection. q3/H1-H7, selected/padded-lane uniformity, register allocation and code-size bounds remain inherited limitations.

**Consistency of the H2 premise (disclosed, not silently repaired).** The premise this claim uses is `q3c >= q3c_used = 2^-71.4162`, block F's own one-sided 99% lower bound, and `q3` in the ledger is `q3c_used x EXQ`. Every other q3c figure in this document is a **sensitivity**, quoted beside the claim it produces so that the pair is checkable at a glance: the preregistered min-of-blocks bound 2^-71.4629 (claim 57.62615), the parents'-pool bound 2^-71.4474 (claim 57.61074), that bound less the 0.0020-bit allowance
(2^-71.4494, claim 57.61273), the superseded 5x charge (2^-71.4578, claim 57.62108), and block E's log-scale 17,408-replicate figure 2^-71.4243 (claim 57.58779) which is reported in G.5 and Appendix N and is **not** operative. No passage of this document asserts any of them as the operative floor.

### G.5 Block E: 16,384 more replicates, preregistered on the submitted pool, all reported

**Preregistration.** `prereg/PREREG_q3E32.txt`, sha256 `f8a8b40f6a94fad9618c0809e31224e05faf8be1229a0ddc1a414f7365862bea`, committed to git (`4c5a8b4`, amended `994e7b9`) **before any listed seed ran**; no seed of block E has a RESULT line anywhere earlier in this filing or in its history. The rule it fixes, applied once and without any branch on the outcome:

```text
block E: the 16,384 log2est values of seeds 772000..788383, and nothing else u  = floor( (mean - t(0.99, n-1) x sd / sqrt(n)) x 10^4 ) / 10^4      (rounded DOWN)
q3c_declared = 2^u
```

**History of the rule, in full.** The file committed as `4c5a8b4` fixed exactly the rule above over block E alone, before any seed of block E ran. Amendment `994e7b9`, also written before any seed ran, proposed instead *pooling* block E with Appendix G.4's 1,024 values. That amendment is **withdrawn**: 1,024 of the pooled sample's 17,408 observations had been examined before the extension was written, so a fixed-n Student bound on the pooled sample has no clean coverage claim, whereas block E's does. The pooled figure is reported below as a sensitivity and is **not** operative. The operative statistic is therefore the original preregistered one; an earlier filing of this package made the pooled figure operative and was returned `not_evaluable` for it (F-EXP-02).

**What was measured, and on what.** Nothing is transferred from the parents' pool: the estimator draws its tail variants from this filing's own list, and the artefacts are the shipped ones -- `q3smc.c` `f0e3efc8`, `gen_consts.py` `721d7949` applied to `lowm.py` `f2578183` (the previous filing's program, which differs from this filing's shipped program in the single line `Q3_LOG2`), giving `q3consts_orig.h` `efd62db9` and `variants.bin` `b7671710` with **599,760 words** (the 170 classes of lists 0, 1, 5, 6). The word count and all five hashes are asserted by the runner before a seed starts, so a run on the parents' 782,800-word pool cannot be reported as this block. Regeneration is invariant in `Q3_LOG2`: both artefact hashes come back identical from either program state, which is why the study's pool is also this filing's. Configuration unchanged from G.3 and G.4: `q3smc seed0 512 8192 512 16384`, 32 shards, one run per seed. Runner: `experiments/r37-q3e-32.py`.

**Result.** 16,384 seeds 772000..788383, none dropped, replaced or rerun: mean **2^-71.42132**, sd **0.15870** (relative sd of the linear estimates **0.1100**), t(0.99, 16383) = 2.3266, one-sided 99 percent lower bound **-71.42420**, and **q3c_declared = 2^-71.4243** on the log scale -- superseded by block F's linear statistic (2^-71.4162, Section 3 and Appendix G.5), and quoted here as the stated sensitivity it is. That is 0.01120 bit of q3c against the previous declaration 2^-71.4355, hence the same number of bits off the claim. The block is not a new model, a new estimator or a new pool; it is more of the same measurement, which is the only thing that narrows a Student bound.

**The pooled figure, stated as a sensitivity and not used.** Pooling block E with Appendix G.4's 1,024 seeds (mean 2^-71.42391, sd 0.15878) gives n = 17,408, mean 2^-71.42147, sd 0.15870, t(0.99, 17407) = 2.3266, one-sided 99 percent lower bound 2^--71.42427, i.e. 2^-71.4243 — *one ten- thousandth of a bit worse* than block E alone. It is reported here and is **not** the operative rule, for the reason the first version of this appendix had to be amended: 1,024 of its 17,408 observations were examined before the extension was written, so a fixed-n Student bound on the pooled sample has no clean coverage claim, while block E's does — it was preregistered as a block of 16,384, run once, and scored by the rule written before it. An earlier draft of this filing pooled the two and was returned `not_evaluable` for exactly this (F-EXP-02: "the fresh Block E-only statistic happens to give the same rounded exponent but was not the preregistered operative rule"). The rule is now simply the one that was preregistered.

**Optional stopping, disclosed.** The pooling rule was written in the amendment `994e7b9` after G.4's 1,024 values existed -- that is unavoidable, since the pooled estimator uses them -- but before any seed of block E ran, and git records both facts. Nothing in the rule depends on block E's outcome: the estimator, the pool and the sample size were fixed first, the rule has no branch, and the block-alone value is printed beside the pooled one so that a reviewer can see what the data alone would have given.

**What does not change.** Appendix G.3's block keeps its own reported value, 2^-71.43547 (declared 2^-71.4355), and every sensitivity of Section 7.4c is quoted at its own q3 factor and is therefore untouched by this. The declared q3c is still a one-sided 99 percent bound on the mean of the submitted pool's own per-variant tail probability, with no sub-pool transfer allowance. Block E alone gives 2^-71.4243 (floor of its own log-scale lower bound to four decimals); that weaker number is reported here and is superseded by Appendix N’s linear-scale bound on fresh seeds, which is the operative one.

**All 16,384 values, in the package.** The list is below in a form the organizer's judge-evidence budget can hold: 16,384 three-byte big-endian integers, base64, each equal to `round((log2est + 71.42) * 1e5) + 90000` in seed order (seeds 772000..788383, one per value). Three lines decode it, and the digest of the values as the estimator prints them (`%.5f`, newline-joined) is `54f26602476451e9803d1b94a55bdaa3bae7e455c919d6fb58d04929d74c448d`; the same list as a `<seed> <log2est>` file is `reports/blockE_log2est-32.txt`, sha256 `115816e0ec65f21f3391f8f799c6b5f16b4ababf78b77dd7e144b11758bdd3fc`. It is encoded rather than printed because 147 KB of decimal text does not fit beside the 106-KiB experiment report inside the 512 KiB cap, and a filing that is refused on size cannot be reviewed at all:

```python
import base64 raw = base64.b64decode(''.join(PACKED.split()))
vals = [b''.join(raw[3*i:3*i+3]).hex() for i in range(16384)]        # keep the bytes log2est = [int.from_bytes(raw[3*i:3*i+3], 'big') - 90000 for i in range(16384)]
log2est = [(-71.42 + z / 1e5) for z in log2est]                      # then '%.5f' each print('%.5f' % (sum(log2est) / 16384))                               # -71.42132
```

```text
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 Aa9cAXbqAZ2AAbOiASbRAU0+
```

The 32 per-shard means and standard deviations are printed as well, each reproducible on its own with `q3smc <seed0> 512 8192 512 16384`:

```text
shard seed0      mean       sd
  0 772000 -71.43570  0.15287
  1 772512 -71.42604  0.15231
  2 773024 -71.41225  0.15649
  3 773536 -71.43328  0.16546
  4 774048 -71.42208  0.15793
  5 774560 -71.42485  0.15492
  6 775072 -71.40966  0.15136
  7 775584 -71.42857  0.15896
  8 776096 -71.41981  0.16444
  9 776608 -71.41915  0.15952
 10 777120 -71.43450  0.15752
 11 777632 -71.42256  0.15844
 12 778144 -71.43031  0.16030
 13 778656 -71.42302  0.15419
 14 779168 -71.41946  0.16255
 15 779680 -71.41235  0.16983
 16 780192 -71.41892  0.16354
 17 780704 -71.42586  0.15719
 18 781216 -71.41976  0.15609
 19 781728 -71.41029  0.16860
 20 782240 -71.41751  0.16834
 21 782752 -71.41314  0.15663
 22 783264 -71.42029  0.15890
 23 783776 -71.42158  0.15865
 24 784288 -71.43728  0.16567
 25 784800 -71.41610  0.15317
 26 785312 -71.42093  0.14348
 27 785824 -71.42557  0.15938
 28 786336 -71.41012  0.15977
 29 786848 -71.41439  0.14856
 30 787360 -71.40873  0.15405
 31 787872 -71.42820  0.16459
```
## Appendix N. Block F: the same pool, fresh seeds, the unbiased (linear-scale) statistic

**Why a second block.** Appendix G.5 declares q3c from

```text
u = floor( (mean(x) - t(0.99, n-1) x sd(x) / sqrt(n)) x 1e4 ) / 1e4,     x_i = log2est_i,
```

i.e. from the mean of the **logarithms** of the per-seed estimates. What the ledger needs is a lower bound on q3c itself. Each per-seed estimate `e_i` = `est` is the product of that replicate's SMC stage means, which is unbiased for q3c; so `mean(e)` is unbiased, while `2^mean(log2 e)` is the geometric mean and is biased **low**. Every other study in this appendix averages the linear estimates (G.2 and G.3: "the one-sided 99% Student lower bound of the mean of the 128 **linear** estimates of the block"); G.5's rule is the exception. On block
E's own 16,384 published RESULT lines the gap is measurable and is not small:

```text
mean(log2est) = -71.421320     sd 0.158699      mean(est) = 2^-71.412644 geometric -> arithmetic gap = 0.008676 bit   (linear LB on block E alone: 2^-71.41551)
```

That gap is conservative, so the scored filing is not wrong; it is paying 0.0087 bit for it. Block F measures the same quantity on fresh seeds with the linear statistic, fixed before the data exist.

**Preregistration.** `prereg/PREREG_q3F32.txt`, sha256 `080ecd4cc51ab921d7e9c9ef203c24090f86372ff6ed1d51e1c7f6fbcd7642be`, committed `0845b50` **before any listed seed ran**: 16,384 fresh seeds 800000..816383, 32 shards of 512, one run per seed, none dropped, replaced or rerun whatever it returns, and the rule

```text
LB = mean(e) - t(0.99, n-1) x sd(e) / sqrt(n)          (linear scale, n-1 in the sd) q3c_declared = 2^( floor(10000 x log2(LB)) / 10000 )   (rounded DOWN, never up)
no gate on the outcome: the declaration is unconditional   (the prereg's comparison against block E's 2^-71.4243 is a report on the two numbers, not a
                                                          condition on which number is declared; selection note below)
```

with no pooling and no branch on the outcome, and the declaration is not conditioned on the gate. `experiments/r37-alpha55.py` re-derives the rule from the 16,384 published estimates and asserts the shipped declaration to the digit (mean(est) 2^-71.413310, relative sd 0.109498, t(0.99, 16383) = 2.3266, LB 2^-71.416184 -> 2^-71.4162). **Selection.** The ledger's q3c is one 99 percent lower bound, not the maximum of two: block E's 2^-71.4243 bounds the GEOMETRIC mean of its per-seed estimates, which the measurement above puts 0.008676 bit below their arithmetic mean, so it is not a 99 percent lower bound on q3c at all, is not a competing estimate of it, and is carried as a stated sensitivity. The gate can then only truncate the report in the event LB <= 2^-71.4243, which sits 6.58 sd below the realized bound (sd of log2 LB = 0.001234): P = 2.41e-11 = 2^-35.3, and the coverage it costs is 2.41e-11, i.e. 1.1e-12 bit of the bound. The crude alternative, holding both blocks to be equally valid 99 percent bounds and splitting Bonferroni (99.5 percent each), declares 2^-71.4165 and claims 57.58004, +0.00029 bit; the same script computes both prices, so a reviewer who prefers the crude one can adopt it without recomputation. The artefacts are pinned by sha256 in the preregistration and re-checked by the runner before the first seed starts, which also reproduces a control seed: `q3smc.c` `f0e3efc8`, `gen_consts.py` `721d7949`, `q3consts_orig.h` `efd62db9`, `variants.bin` `b7671710` = 599,760 words (the submitted pool), program `lowm.py` `b6b39663`, identical to block E's state modulo the single line `Q3_LOG2`.

**Result.** n = 16,384, `mean(e)` = 2^-71.41331, sd of the linear estimates 3.482222e-23 (relative 0.1095), t = 2.3266 at 16383 df, **LB = 2^-71.41618**, and **q3c_declared = 2^-71.4162** (floor to four decimals, never up). That is 0.0081 bit stronger than block E's log-scale declaration 2^-71.4243 (claim 57.58779) and 0.0022 bit below this block's own point estimate 2^-71.41331, which is the price of the 99 percent bound.

**All 32 shards reported** (the whole record of the run, one line per shard in seed order; `mean(est)` is `2^` of the mean of the linear estimates in that shard):

```text
  first    n   mean(est)           mean(log2est)  relsd(linear)  sd(log2est)
 800000  512  2^-71.41111  2^-71.42007  0.11202  0.16102
 800512  512  2^-71.41060  2^-71.41985  0.11222  0.16464
 801024  512  2^-71.42446  2^-71.43371  0.11337  0.16381
 801536  512  2^-71.40931  2^-71.41833  0.11143  0.16210
 802048  512  2^-71.40867  2^-71.41804  0.11371  0.16516
 802560  512  2^-71.41331  2^-71.42207  0.10941  0.16000
 803072  512  2^-71.41154  2^-71.41984  0.10705  0.15535
 803584  512  2^-71.42637  2^-71.43411  0.10297  0.15018
 804096  512  2^-71.40236  2^-71.41138  0.11058  0.16280
 804608  512  2^-71.42123  2^-71.42979  0.10834  0.15801
 805120  512  2^-71.41257  2^-71.42116  0.10935  0.15758
 805632  512  2^-71.40666  2^-71.41475  0.10501  0.15397
 806144  512  2^-71.41640  2^-71.42452  0.10528  0.15398
 806656  512  2^-71.42044  2^-71.42904  0.10861  0.15839
 807168  512  2^-71.42095  2^-71.43005  0.11200  0.16278
 807680  512  2^-71.40710  2^-71.41591  0.10997  0.16031
 808192  512  2^-71.41575  2^-71.42417  0.10775  0.15651
 808704  512  2^-71.41068  2^-71.41956  0.11063  0.16073
 809216  512  2^-71.40196  2^-71.41063  0.10940  0.15880
 809728  512  2^-71.41288  2^-71.42175  0.11060  0.16076
 810240  512  2^-71.41190  2^-71.41971  0.10353  0.15099
 810752  512  2^-71.42395  2^-71.43362  0.11569  0.16758
 811264  512  2^-71.42140  2^-71.43095  0.11465  0.16681
 811776  512  2^-71.39888  2^-71.40660  0.10382  0.14928
 812288  512  2^-71.40945  2^-71.41798  0.10794  0.15797
 812800  512  2^-71.41420  2^-71.42315  0.11106  0.16142
 813312  512  2^-71.40944  2^-71.41792  0.10799  0.15720
 813824  512  2^-71.41443  2^-71.42244  0.10476  0.15286
 814336  512  2^-71.40502  2^-71.41398  0.11099  0.16158
 814848  512  2^-71.40901  2^-71.41763  0.10868  0.15870
 815360  512  2^-71.42417  2^-71.43337  0.11261  0.16366
 815872  512  2^-71.42025  2^-71.42930  0.11112  0.16281
```

All 16,384 values, as the estimator prints them (`est`, newline-joined, seed order), have sha256 `3c125b871d3898535d4dedda31ac97b829d97256106d82c90f231d3cd0512e1b`; `python3 experiments/r37-q3f-32.py stats` re-derives every number of this appendix from the shard files and asserts the seed set exactly.

**What does not change.** The pool, the estimator, its configuration, the constants, the family (170 classes, 599,760 variants), the charge list, the characteristic, the premises H1-H3 and every other number of the ledger. EXQ is set by Appendix O (q3 = q3c x 2.482), and q3c <= 2^-71.38 < 2^-70 as H2 requires. Block E's declaration 2^-71.4243 (claim 57.58779) and every earlier sensitivity keep their own q3 factor and their own claim.

## Appendix O. Block G: EXQ measured on this filing's own law (1024 fresh seeds)

**Why.** EXQ = 2.4331 is inherited from 4ec21bf9 as `min(2.4331, 2.4443)`, a minimum taken over two *different* late-word laws of that filing, and every later measurement of the ratio came out above it (2.4552 pooled over the table-state runs, 2.46455 on the kept-fibre law). Carrying the minimum puts the declaration about 0.011 bit below what the attack's own law supports, which is conservative but is not what this package's other floors do: they are measured on the pool and the law the ledger actually uses. Block G measures

```text
R = Pr[the two 37-step outputs are equal | rows 16..21 follow every cell and printed two-bit condition] / Pr[every cell and printed two-bit condition of rows 22..36 | the same premise]
```

on **this** filing's characteristic, table cells and 599,760-variant pool.

**Preregistration.** `prereg/PREREG_exqG32.txt`, sha256 `83d917aefb0a5cf0c4db0739a62d07a0a898eb8992b853f0fe76e62cdd19145b`, committed `afc4946` **before any listed seed ran**: 1024 fresh seeds 860000..861023, 32 shards of 32, NP = 8192 and NL = 25,600 late proposals per particle (209,715,200 proposals per seed), one run per seed, none dropped, replaced or rerun, and the rule

```text
R_pooled = K/C,  se = R_pooled sqrt(1/C + 1/K),  LB_p = R_pooled - 2.3266 se LB_s     = mean(r_s) - t(0.99, 1023) sd(r_s)/sqrt(1024)      (r_s = K_s/C_s)
LB       = min(LB_p, LB_s)          EXQ_declared = floor(1000 LB)/1000 no gate on the outcome (2.4331 = the previous declaration, a reported sensitivity; the min of two 99 percent bounds is already conservative, so no split is needed here)
```

fixed before the data, both bounds declared and the more conservative one used, so no choice is made after the run. The estimator is the shipped `q3smc.c` with exactly two edits: its SMC loop stops after stage 21, and the tail is replaced by a late-proposal loop that draws (W6, W7) uniformly on F6 x F7 and W8x uniformly from the submitted pool, computes rows 22..36 of both members **in full**, and evaluates both events on the same proposal; it asserts cell => collision on every single proposal. The particles are the shipped estimator's stage-16..21 survivors
(resampled uniformly at each stage), so the proposal law is exactly the one Section 7.7 defines.

**Result.** 1024 seeds, 214,748,364,800 proposals, 6,556,489 cell events and 16,292,349 collisions (cell rate 3.0531e-05 = 2^-14.99936, against the shipped stage means 2^-11.003 x 2^-4 = 2^-15.002; row-22 rate 2^-10.99983 against 2^-11.003). R_pooled = **2.484920**, se = 0.001149, LB_p = 2.482246; per-seed ratio mean 2.485151, sd 0.038885, t(1023) = 2.3300, LB_s = 2.482320. Declared **EXQ = 2.482** (the smaller bound, floored to three decimals).

**What does not change.** q3c (Appendix N), the pool, the family, the characteristic, the charge list and the premises. The inherited minimum 2.4331 and the two measurements behind it stay in Section 7.7 as labelled sensitivities, and the H3(b) upper value 2.4902 is untouched.

